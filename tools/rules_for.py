#!/usr/bin/env python3
"""Tegilayotgan fayllarga qaysi qoidalar tegishli ekanini bir chaqiruvda beradi.

    python3 tools/rules_for.py src/main/java/shop/OrderService.java
    python3 tools/rules_for.py --diff           # staged, unstaged va yangi fayllar (joriy repo)
    python3 tools/rules_for.py --diff --cached  # faqat staged
    python3 tools/rules_for.py --no-mark <fayllar>   # o'qish uchun, belgilamaydi

Nega: aktyor ikkinchi marta chaqirilsa, sababi deyarli har doim bitta -
qoidani oldindan bilmagan. Qidirib topish esa har aktyorda boshqacha
chiqadi, shuning uchun dasturchi yozgan narsani reviewer boshqa
mezon bilan tekshiradi va ish ikkinchi aylanaga tushadi.

Bu asbob shu ikkisini bitta manbaga bog'laydi. Dasturchi YOZISHDAN
OLDIN, reviewer esa TEKSHIRISHDA shu buyruqni chaqiradi: kirish bir xil,
chiqish bir xil, kelishmovchilik qolmaydi.

Nisbiy yo'l va `--diff` joriy papkadan olinadi, klondan emas: global
o'rnatishda skript klonda turadi, ish esa boshqa proyektda boradi.

Chiqish uch qism: tegishli boblar, ularning tekshiruv punktlari va
mashina allaqachon topgan muammolar. Kerak bo'lsa boshida ogohlantirish:
Kotlin fayl (mexanik tekshiruv yo'q), Spring bo'lmagan JVM proyekt
(Quarkus, Micronaut) yoki qo'llanma bazasidan eski Boot va Java.
"""

import os
import re
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

import check_code  # noqa: E402
import geniuslib  # noqa: E402
from check_code import in_clone, strip_noise, tool_cmd  # noqa: E402
from docref import ensure_index, resolve  # noqa: E402
from docref import project_slug as docref_slug  # noqa: E402
from docref import SHARED_MEMORY, is_clone_project, memory_home  # noqa: E402
from state import mark  # noqa: E402
import review_status  # noqa: E402

CHAPTERS = os.path.join(ROOT, "index", "chapters.tsv")
CHECKLIST = os.path.join(ROOT, "index", "checklist.tsv")
# Klondagi memory. Boshqa proyekt memorysi klondan tashqarida
# (docref.memory_home, GENIUS_MEMORY_DIR): memory_base() tanlaydi.
MEMORY = os.path.join(ROOT, "memory")

# Mashina topilmalaridan shuncha to'liq matn bilan, qolgani qisqa shaklda.
MAX_ITEMS = 12
# Tekshiruv punktlaridan shuncha. Punktlar audit uchun yozilgan: butun
# proyektga tegishlisi (`loyiha` doirasi) olib tashlanadi, qolgani ham
# bitta o'zgarish uchun ko'p. O'ttiztasi shovqin bo'ladi va o'qilmay
# o'tiladi, shuning uchun kam olinadi va boblar bo'ylab navbatma-navbat:
# har mavzudan birinchi punktlar.
MAX_POINTS = 8
# Bir chaqiruvda shuncha bob. Belgilar ko'p, lekin bitta o'zgarish uchun
# yigirmata bob ro'yxati yo'l ko'rsatmaydi, chalg'itadi. ALWAYS shundan
# tashqarida: Java faylida nomlash va funksiya shakli har doim tegishli.
MAX_CHAPTERS = 8
# Avvalgi xatolardan shuncha, eng yangisi oldin: memory o'sgani sari
# ro'yxat har chaqiruvda cho'zilmasin.
MAX_MISTAKES = 5

# Kod ichidagi belgi -> tegishli boblar. Jadval qo'lda tuzilgan, lekin
# har bob ishga tushishdan oldin indeksda borligi tekshiriladi, shuning
# uchun bob ko'chsa yoki o'chsa, jim xato bo'lmaydi.
# Tartib muhim: eng aniq belgi oldinda, boblar va punktlar shu tartibda
# olinadi. Tartib fayllar bo'yicha emas, shu jadval bo'yicha: ko'p faylli
# chaqiruvda ham xavfsizlik oldinda, umumiy belgi (`List<`, `->`) esa
# oxirida turadi va MAX_CHAPTERS to'lganda u chiqib ketadi.
SIGNALS = [
    # --- xavfsizlik: eng qimmat xato turi, shuning uchun birinchi ---
    ("xavfsizlik: SQL", r"createNativeQuery|createQuery|\bStatement\b|@Query\b|jdbcTemplate",
     [("code-review", "29"), ("sonarqube", "26")]),
    ("xavfsizlik: sir va kripto",
     r"\bCipher\.|MessageDigest\.|KeyStore\b|SecretKey|getPassword\(|apiKey|secretKey",
     [("code-review", "32")]),
    ("xavfsizlik: tashqi kirish",
     r"MultipartFile|ObjectInputStream|readObject\(|new\s+URL\(|URI\.create\(",
     [("code-review", "31")]),
    ("xavfsizlik: ruxsat",
     r"@PreAuthorize\b|SecurityFilterChain|@Secured\b|@RolesAllowed\b"
     r"|@EnableWebSecurity\b|PasswordEncoder|JwtDecoder",
     [("patterns", "18"), ("code-review", "30"), ("code-review", "28"),
      ("architect", "20")]),
    # Bog'liqlik qo'shish supply chain xavfi, shuning uchun shu blokda.
    # Faqat build faylida qidiriladi (BUILD_ONLY): `implementation ` so'zi
    # Java izohida ham uchraydi.
    # TOML shakli Gradle version catalog uchun (gradle/libs.versions.toml):
    # bog'liqlik PR i ko'pincha faqat shu faylga tegadi.
    ("bog'liqlik", r"<dependency>|<artifactId>|implementation\s|api\s*[(']|plugins\s*\{"
     r"|\[libraries\]|\[plugins\]|\bmodule\s*=|version\.ref",
     [("code-review", "33"), ("sonarqube", "39")]),

    # --- ma'lumot va tranzaksiya ---
    ("entity va ORM", r"@Entity\b|@Table\b|@ManyToOne\b|@OneToMany\b|@Column\b"
     r"|@MappedSuperclass\b|@Embeddable\b|@Id\b",
     [("patterns", "9"), ("architect", "18"), ("sonarqube", "29"),
      ("code-review", "23"), ("clean-code", "28")]),
    ("ma'lumotga kirish",
     r"\b(?:JpaRepository|CrudRepository|ListCrudRepository|PagingAndSortingRepository)\b"
     r"|@Repository\b|\bRepository<|@RepositoryDefinition\b",
     [("patterns", "9"), ("architect", "18"), ("code-review", "23"),
      ("code-review", "24")]),
    ("tranzaksiya", r"@(?:[\w.]+\.)?Transactional\b",
     [("architect", "19"), ("code-review", "19")]),
    ("hodisa", r"@(?:Transactional)?EventListener\b|ApplicationEventPublisher",
     [("architect", "19"), ("patterns", "5")]),
    ("sxema migratsiyasi",
     r"Flyway|Liquibase|\bV\d+__|changeSet"
     r"|(?i:\b(?:alter|create|drop)\s+(?:table|(?:unique\s+)?index)\b)",
     [("architect", "33"), ("code-review", "25")]),

    # --- integratsiya ---
    ("tashqi chaqiruv", r"\b(?:RestTemplate|WebClient|RestClient|FeignClient)\b",
     [("patterns", "17"), ("code-review", "22")]),
    ("chidamlilik", r"@(?:Retryable|CircuitBreaker|Bulkhead|RateLimiter|TimeLimiter)\b",
     [("patterns", "17"), ("code-review", "22")]),
    ("broker",
     r"@KafkaListener\b|@RabbitListener\b|KafkaTemplate|StreamBridge"
     r"|enable-auto-commit|auto-offset-reset|\bspring\.kafka\b|(?m:^\s*kafka:)",
     [("architect", "29"), ("patterns", "16"), ("code-review", "22"),
      ("code-review", "27")]),
    ("sozlama",
     r"\bhikari\b|\bdatasource\b|management\.endpoints|\bspring\.jpa\b"
     r"|(?m:^\s*(?:jpa|management|hikari|datasource):)",
     [("architect", "27"), ("code-review", "21")]),

    # --- test: turiga qarab ajratiladi ---
    ("test: Testcontainers", r"@Testcontainers\b|@Container\b|GenericContainer|PostgreSQLContainer",
     [("testing", "8")]),
    ("test: tashqi servis taqlidi", r"WireMock|MockRestServiceServer|\bPact\b|StubRunner",
     [("testing", "9")]),
    ("test: slice", r"@SpringBootTest\b|@WebMvcTest\b|@DataJpaTest\b|@JsonTest\b",
     [("testing", "7"), ("clean-code", "30")]),
    ("test: mock", r"@MockBean\b|@MockitoBean\b|@Mock\b|Mockito\.",
     [("testing", "6")]),
    ("test: ma'lumot", r"@Sql\b|TestEntityManager|@DirtiesContext\b|@TestPropertySource\b",
     [("testing", "10")]),
    ("test: arxitektura", r"ArchUnit|ArchTest|ArchRuleDefinition",
     [("testing", "14")]),
    ("test: asinxron", r"Awaitility|CountDownLatch|@RepeatedTest\b|@Disabled\b",
     [("testing", "11"), ("testing", "16")]),
    ("test", r"@Test\b|@ParameterizedTest\b|\bassertThat\b|\bAssertions\.",
     [("testing", "5"), ("sonarqube", "19"), ("code-review", "35"),
      ("code-review", "34"), ("code-review", "36")]),

    # --- web va servis ---
    ("web qatlami", r"@RestController\b|@Controller\b|@(?:Get|Post|Put|Delete|Request)Mapping\b",
     [("patterns", "7"), ("architect", "17"), ("code-review", "20"),
      ("clean-code", "27")]),
    ("konfiguratsiya",
     r"@Configuration\b|@ConfigurationProperties\b|@Profile\b|@ConditionalOn\w+|@Value\s*\(",
     [("code-review", "21"), ("code-review", "18"), ("architect", "16")]),
    # MapStruct. Yolg'iz `@Mapper` MyBatis da ma'lumotga kirish, shuning
    # uchun paket nomi yoki `@Mapping` talab qilinadi.
    ("mapper", r"\borg\.mapstruct\b|@Mapping\b",
     [("patterns", "8"), ("sonarqube", "11")]),
    ("keshlash", r"@Cacheable\b|@CacheEvict\b|CacheManager",
     [("patterns", "11"), ("architect", "28")]),
    ("rejalashtirilgan ish", r"@Scheduled\b|JobBuilder|StepBuilder",
     [("patterns", "20")]),
    # Static o'zgaruvchan kolleksiya va SimpleDateFormat: bean singleton,
    # ya'ni bir nechta thread bitta obyektga yozadi.
    ("konkurentlik", r"\bsynchronized\b|ReentrantLock|AtomicInteger|AtomicLong|ExecutorService"
     r"|\bstatic\b[^;(){}]*\b(?:HashMap|ArrayList|SimpleDateFormat)\b",
     [("architect", "11"), ("architect", "12")]),
    ("asinxron", r"@Async\b|CompletableFuture",
     [("architect", "12"), ("patterns", "19")]),

    # --- kod shakli ---
    ("xato bilan ishlash", r"\bthrow new\b|\bcatch\s*\(|\bfinally\b",
     [("clean-code", "18"), ("clean-code", "19")]),
    ("tenglik shartnomasi", r"\bequals\s*\(|\bhashCode\s*\(|\bcompareTo\s*\(",
     [("clean-code", "15")]),
    # Sinf vorisligi. `interface X extends JpaRepository` vorislik emas.
    ("vorislik", r"\bclass\s+\w+(?:<[^>]*>)?\s+extends\s+\w|\babstract\s+class\b|\bsuper\.",
     [("clean-code", "17")]),
    ("pul va son", r"\bBigDecimal\b|\bdouble\s+\w|\bfloat\s+\w",
     [("clean-code", "20")]),
    ("sana va vaqt", r"\bLocalDate\b|\bLocalDateTime\b|\bInstant\b|\bZoneId\b|\bDuration\b",
     [("clean-code", "22")]),
    ("satr va regex", r"Pattern\.|String\.format|\breplaceAll\b|\bmatches\s*\(",
     [("clean-code", "21")]),
    ("o'zgarmaslik", r"\brecord\s+\w+\s*\(|\bfinal\s+class\b|List\.of\(|Map\.of\(",
     [("clean-code", "16")]),
    # `@Value("${...}")` Spring sozlamasi, Lombok emas.
    ("Lombok", r"@Builder\b|@Data\b|@Getter\b|@Setter\b|@Slf4j\b|@Value\b(?!\s*\()",
     [("sonarqube", "41"), ("clean-code", "26")]),
    ("loglash", r"\bLogger\b|\blog\.(?:info|warn|error|debug)\b",
     [("clean-code", "29")]),
    ("servis qatlami", r"@Service\b|@Component\b",
     [("patterns", "8")]),
    # --- umumiy: eng oxirida, aniqrog'i bo'lsa chiqib ketadi ---
    ("oqim va lambda", r"\.stream\s*\(\)|Collectors\.|\bOptional<",
     [("clean-code", "24"), ("clean-code", "23")]),
    ("shart va sikl", r"\bswitch\s*\(|\belse\s+if\b|\bfor\s*\(|\bwhile\s*\(",
     [("clean-code", "6"), ("clean-code", "7"), ("sonarqube", "15")]),
]

# Build fayllari. Ular kod kabi tekshiruvga muhtoj, lekin .java emas.
# `.versions.toml` Gradle version catalog: bog'liqlik versiyasi u yerda.
BUILD_FILES = ("pom.xml", "build.gradle", "build.gradle.kts",
               "settings.gradle", "settings.gradle.kts", ".versions.toml")
BUILD_ONLY = {"bog'liqlik"}

# Manba kodi. Kotlin boblar va punktlar uchun ko'riladi, lekin check_code
# uni tekshirmaydi: chiqishda shu ochiq aytiladi (KOTLIN_NOTE).
SOURCES = (".java", ".kt")
KOTLIN_NOTE = "Kotlin: mexanik tekshiruv yo'q (check_code faqat .java ni ko'radi)."

# Qaysi fayllar ko'riladi. Migratsiya (.sql, Liquibase .xml/.yaml) va
# sozlama (application.yml) ham: ularning review bobi bor, .java dan esa
# ko'rinmaydi.
WATCHED = SOURCES + (".sql", ".yml", ".yaml", ".properties", ".xml") + BUILD_FILES

# Yo'ldan aniqlanadigan belgi, mazmundan qat'i nazar: kichik harfli
# Flyway SQL va ichma-ich YAML da matn regexi ishonchsiz.
PATH_SIGNALS = {
    "sxema migratsiyasi": r"(?:^|/)db/(?:migration|changelog)/|(?:^|/)[VUR]\d*__[^/]*\.sql$",
    "sozlama": r"(?:^|/)(?:application|bootstrap)[^/]*\.(?:ya?ml|properties)$",
}

# Hali yozilmagan Java fayl: matn yo'q, belgi nomidan olinadi. Aks holda
# yozuvchi faqat ALWAYS boblarini oladi, fayl nomi bilan chaqirgan reviewer
# esa to'liq ro'yxatni, va zanjir ikkiga ajraladi. Test yo'li check_code
# dagi is_test bilan bir xil.
NAME_SIGNALS = {
    "xavfsizlik: ruxsat": r"Security\w*\.(?:java|kt)$",
    "entity va ORM": r"/(?:entity|entities)/[^/]+\.(?:java|kt)$|Entity\.(?:java|kt)$",
    "ma'lumotga kirish": r"Repository\.(?:java|kt)$",
    "broker": r"(?:Listener|Consumer)\.(?:java|kt)$",
    "test": r"/test/|(?:Test|Tests|IT)\.(?:java|kt)$",
    "web qatlami": r"Controller\.(?:java|kt)$",
    "konfiguratsiya": r"(?:Config|Configuration|Properties)\.(?:java|kt)$",
    "mapper": r"Mapper\.(?:java|kt)$",
    "rejalashtirilgan ish": r"(?:Job|Scheduler)\.(?:java|kt)$",
    "servis qatlami": r"Service\.(?:java|kt)$",
}

# Har Java fayl uchun, belgisidan qat'i nazar.
ALWAYS = [("clean-code", "2"), ("clean-code", "4"), ("code-review", "8")]

# `@org.springframework...Transactional` kabi to'liq nomli annotatsiya
# qisqa shaklga keltiriladi: aks holda har `@X\b` naqshi uni ko'rmaydi.
FQN_ANNOTATION_RE = re.compile(r"@(?:[a-z_]\w*\.)+(?=[A-Z])")

NEVER = r"(?!)"


def chapter_titles():
    titles = {}
    ensure_index("chapters.tsv")
    if not os.path.exists(CHAPTERS):
        return titles
    with open(CHAPTERS, encoding="utf-8") as handle:
        handle.readline()
        for line in handle:
            parts = line.rstrip("\n").split("\t")
            if len(parts) >= 3 and parts[1]:
                titles[(parts[0], parts[1])] = parts[2]
    return titles


def _full(path):
    """Mutlaq yo'l. Nisbiy yo'l joriy papkaga nisbatan, klonga emas."""
    return os.path.abspath(path)


def _git(args, cwd):
    proc = geniuslib.run_git(args, cwd=cwd, timeout=None)
    return proc.stdout if proc and proc.returncode == 0 else ""


def changed_files(args):
    """Ko'riladigan fayllar, mutlaq yo'l bilan."""
    if "--diff" in args:
        # Diff joriy papkaning reposidan: global o'rnatishda klonning diffi
        # ishga tegishli emas. Git yo'lni repo ildiziga nisbatan beradi,
        # shuning uchun hammasi ildizda yurgiziladi va unga ulanadi.
        top = _git(["rev-parse", "--show-toplevel"], os.getcwd()).strip()
        if not top:
            return []
        diff = ["diff", "--name-only", "-z", "--diff-filter=d"]
        if "--cached" in args:
            outs = [_git(diff + ["--cached"], top)]
        else:
            # Staged, unstaged va yangi (untracked) fayl birga: yangi sinf
            # `git diff` da ko'rinmaydi, lekin review uni ko'rishi shart.
            # HEAD hali yo'q repoda `diff HEAD` bo'sh, qolgan ikkitasi yopadi.
            outs = [_git(diff + ["HEAD"], top), _git(diff + ["--cached"], top),
                    _git(diff, top),
                    _git(["ls-files", "-z", "--others", "--exclude-standard"], top)]
        names = {n for out in outs for n in out.split("\0") if n.strip()}
        candidates = sorted(os.path.normpath(os.path.join(top, n)) for n in names)
    else:
        candidates = [_full(a) for a in args if not a.startswith("--")]
    # Faqat kuzatiladigan turlar. Boshqa faylni jim qabul qilish
    # chalg'itadi: javob beriladi, lekin u o'sha faylga tegishli emas.
    return [f for f in candidates if f.endswith(WATCHED)]


def scan(paths):
    """Har fayl uchun (nom, mavjudmi, belgilar to'plami).

    Java da izoh va satr literali avval o'chiriladi: izohdagi `@KafkaListener`
    yoki satrdagi `createQuery` belgi emas.
    """
    out = []
    for path in paths:
        full = _full(path)
        slash = full.replace("\\", "/")
        exists = os.path.isfile(full)
        text = None
        if exists:
            try:
                with open(full, encoding="utf-8", errors="replace") as handle:
                    text = handle.read()
            except OSError:
                continue
            if slash.endswith(SOURCES):
                text = FQN_ANNOTATION_RE.sub("@", strip_noise(text))
        labels = set()
        for label, pattern, _ in SIGNALS:
            if re.search(PATH_SIGNALS.get(label, NEVER), slash):
                labels.add(label)
            elif text is None:
                if slash.endswith(SOURCES) and re.search(
                        NAME_SIGNALS.get(label, NEVER), slash):
                    labels.add(label)
            elif ((label not in BUILD_ONLY or slash.endswith(BUILD_FILES))
                  and re.search(pattern, text)):
                labels.add(label)
        out.append((os.path.basename(full), exists, labels))
    return out


def ordered(scanned):
    """Belgilar SIGNALS tartibida: (belgi, boblar, uni bergan birinchi fayl).

    Tartib fayllar bo'yicha bo'lsa, birinchi faylning umumiy belgilari
    MAX_CHAPTERS ni egallab, keyingi faylning xavfsizlik bobini siqib
    chiqarardi va natija fayl tartibiga bog'liq bo'lardi.
    """
    found = []
    for label, _, chapters in SIGNALS:
        where = next((name for name, _, labels in scanned if label in labels), None)
        if where is not None:
            found.append((label, chapters, where))
    return found


def detect(paths):
    """Fayllardan belgilarni topadi: (belgi, boblar, fayl)."""
    return ordered(scan(paths))


def checklist_for(wanted, skip=None):
    """Berilgan boblarning `kod` doirasidagi punktlari, bob tartibida.

    Qaytaradi: (punktlar, tashlangan loyiha punktlari soni). `loyiha`
    punkti butun proyekt auditi (build_index.SCOPE_RE): bitta o'zgarishda
    u bajarilmaydi, faqat diff punktini ko'mib qo'yadi. U `doc.sh
    checklist` da qoladi. `skip` naqshiga mos punkt ham tashlanadi
    (Spring bo'lmagan proyektda `spring.` va `@Autowired`).
    """
    items, project = {}, 0
    ensure_index("checklist.tsv")
    if not os.path.exists(CHECKLIST):
        return items, project
    with open(CHECKLIST, encoding="utf-8") as handle:
        handle.readline()
        for line in handle:
            parts = line.rstrip("\n").split("\t")
            if len(parts) < 4 or (parts[0], parts[1]) not in wanted:
                continue
            if len(parts) > 4 and parts[4] == "loyiha":
                project += 1
                continue
            if skip and re.search(skip, parts[3]):
                continue
            items.setdefault((parts[0], parts[1]), []).append(parts[3])
    return items, project


# --- Proyekt versiyasi va framework ------------------------------------

# Qo'llanma bazasi (docs/<hujjat>/README.md): Boot 3.2+ va Java 17+.
# Undan eski proyektda Boot 3.4+ API (`@MockitoBean`) kompilyatsiya
# bo'lmaydi, shuning uchun banner va ko'chish bo'limi beriladi.
BOOT_FLOOR, JAVA_FLOOR = (3, 2), 17
MIGRATION_REF = "architect 16.11"
PROJECT_FILES = ("pom.xml", "build.gradle", "build.gradle.kts",
                 os.path.join("gradle", "libs.versions.toml"))
BOOT_RES = (
    # Maven: parent, xossa va BOM
    r"<parent>(?:(?!</parent>).)*?org\.springframework\.boot(?:(?!</parent>).)*?"
    r"<version>\s*([^<\s]+)\s*</version>",
    r"<spring-boot\.version>\s*([^<\s]+)\s*<",
    r"<artifactId>spring-boot-dependencies</artifactId>\s*<version>\s*([^<\s]+)",
    # Gradle: plagin, buildscript classpath, ext
    r"""id\s*\(?\s*["']org\.springframework\.boot["']\s*\)?\s*version\s*\(?\s*["']([^"']+)""",
    r"spring-boot-gradle-plugin:([\w.\-]+)",
    r"""springBootVersion\s*=\s*["']([^"']+)""",
)
JAVA_RES = (
    r"<java\.version>\s*([\d.]+)\s*<",
    r"<maven\.compiler\.(?:release|source)>\s*([\d.]+)\s*<",
    r"<release>\s*(\d+)\s*</release>",
    r"JavaVersion\.VERSION_(\d+(?:_\d+)?)",
    r"JavaLanguageVersion\.of\(\s*(\d+)",
    r"jvmToolchain\(\s*(\d+)",
    r"""sourceCompatibility\s*=\s*['"]?([\d.]+)""",
)
OTHER_JVM = (("io.quarkus", "Quarkus"), ("io.micronaut", "Micronaut"))
# Spring bo'lmagan proyektda shu punktlar boshqa framework uchun.
SPRING_ONLY_RE = r"\bspring\.|@Autowired\b"


def _numbers(text):
    """"2.7.18" -> (2, 7, 18); "1.8" Java da 8. Raqam yo'q bo'lsa None."""
    nums = tuple(int(n) for n in re.findall(r"\d+", text.split("-")[0])[:3])
    return nums or None


def _catalog(text):
    """libs.versions.toml: (Boot versiyasi, Java versiyasi) yoki None."""
    versions, table = {}, ""
    for raw in text.split("\n"):
        line = raw.split("#", 1)[0].strip()
        head = re.match(r"\[([\w.-]+)\]$", line)
        if head:
            table = head.group(1)
            continue
        pair = re.match(r"""([\w.-]+)\s*=\s*["']([^"']+)["']$""", line)
        if table == "versions" and pair:
            versions[pair.group(1)] = pair.group(2)
    boot = None
    for line in text.split("\n"):
        if "org.springframework.boot" not in line:
            continue
        direct = re.search(r"""\bversion\s*=\s*["']([^"']+)""", line)
        ref = re.search(r"""version\.ref\s*=\s*["']([^"']+)""", line)
        boot = direct.group(1) if direct else versions.get(ref.group(1)) if ref else None
        if boot:
            break
    norm = {re.sub(r"[-_.]", "", k).lower(): v for k, v in versions.items()}
    boot = boot or norm.get("springboot")
    java = norm.get("java") or norm.get("jdk")
    return boot, java


def _resolve(value, text):
    """Maven `${xossa}` qiymatini o'sha fayldan oladi."""
    ref = re.match(r"\$\{([\w.-]+)\}$", value or "")
    if not ref:
        return value
    found = re.search(r"<%s>\s*([^<\s]+)\s*<" % re.escape(ref.group(1)), text)
    return found.group(1) if found else None


def _project_texts(paths):
    """Fayllardan yuqoriga, git ildizigacha: build fayllar matni, yaqini oldin."""
    texts, seen = [], set()
    for path in paths:
        folder = os.path.dirname(_full(path))
        while folder not in seen:
            seen.add(folder)
            for name in PROJECT_FILES:
                full = os.path.join(folder, name)
                try:
                    with open(full, encoding="utf-8", errors="replace") as handle:
                        texts.append((name, handle.read(262144)))
                except OSError:
                    continue
            parent = os.path.dirname(folder)
            if os.path.exists(os.path.join(folder, ".git")) or parent == folder:
                break
            folder = parent
    return texts


def project_profile(paths):
    """(Boot versiyasi, Java versiyasi, Spring bo'lmagan framework nomi).

    Har biri topilmasa None: noma'lum versiya eski deb hisoblanmaydi.
    """
    boot = java = other = None
    for name, text in _project_texts(paths):
        if name.endswith(".toml"):
            cat_boot, cat_java = _catalog(text)
        else:
            cat_boot = next((_resolve(m.group(1), text) for m in
                             (re.search(r, text, re.S) for r in BOOT_RES) if m), None)
            cat_java = next((_resolve(m.group(1), text) for m in
                             (re.search(r, text) for r in JAVA_RES) if m), None)
        boot = boot or (cat_boot if cat_boot and _numbers(cat_boot) else None)
        java = java or (cat_java if cat_java and _numbers(cat_java) else None)
        other = other or next((label for key, label in OTHER_JVM if key in text), None)
    if java:
        nums = _numbers(java.replace("_", "."))
        java = str(nums[1] if nums[0] == 1 and len(nums) > 1 else nums[0])
    return boot, java, other


def profile_notes(paths):
    """Chiqish boshidagi ogohlantirishlar: Kotlin, Spring emas, eski versiya."""
    notes = []
    if any(p.endswith(".kt") for p in paths):
        notes.append(KOTLIN_NOTE)
    boot, java, other = project_profile(paths)
    if other:
        notes.append("Spring emas (%s): Spring boblari bu proyektga to'g'ridan-to'g'ri "
                     "qo'llanmaydi, `spring.*` va `@Autowired` punktlari olib "
                     "tashlandi." % other)
    old = []
    if boot and _numbers(boot) < BOOT_FLOOR:
        old.append("Spring Boot %s" % boot)
    if java and int(java) < JAVA_FLOOR:
        old.append("Java %s" % java)
    if old:
        notes.append("ESKI VERSIYA: %s. Qo'llanma bazasi Boot 3.2+ va Java 17+: "
                     "undan yangi API (masalan `@MockitoBean`, Boot 3.4+) bu yerda "
                     "yo'q. Ko'chish: %s." % (", ".join(old), MIGRATION_REF))
    return notes, other


def memory_base():
    """Proyekt memorysi ildizi: klonning o'zida MEMORY (sinovda
    almashtiriladi), boshqa proyektda docref.memory_home()."""
    return MEMORY if is_clone_project() else memory_home()


def memory_folder(sub):
    """`umumiy` va `claude-genius` har doim klonda, qolgani memory_base da."""
    return os.path.join(MEMORY if sub in SHARED_MEMORY else memory_base(), sub)


def project_slug():
    """memory slugi (docref.project_slug), memory_base ga nisbatan."""
    return docref_slug(memory=memory_base())


INDEX_ROW_RE = re.compile(r"^- `([^`]+\.md)` - (.+)$")


def _index_notes(folder):
    """MEMORY.md dagi bir qatorli tavsiflar, o'ralgan davomi bilan."""
    notes, current = {}, None
    try:
        with open(os.path.join(folder, "MEMORY.md"), encoding="utf-8") as handle:
            lines = handle.read().split("\n")
    except OSError:
        return notes
    for line in lines:
        match = INDEX_ROW_RE.match(line.rstrip())
        if match:
            current = match.group(1)
            notes[current] = match.group(2).strip()
        elif current and line.startswith("  ") and line.strip():
            notes[current] += " " + line.strip()
        else:
            current = None
    return notes


def _topic(path):
    """Topic fayl: (modified, sarlavha, birinchi gap yoki punkt).

    Fayl frontmatter bilan boshlanadi (memory/README.md), u tashlanadi:
    aks holda aktyorga `---` yetib boradi.
    """
    with open(path, encoding="utf-8", errors="replace") as handle:
        lines = handle.read().split("\n")
    modified = ""
    if lines and lines[0].strip() == "---":
        end = next((i for i, l in enumerate(lines[1:], 1) if l.strip() == "---"), 0)
        for line in lines[1:end]:
            if line.startswith("modified:"):
                modified = line.split(":", 1)[1].strip()
        lines = lines[end + 1:]
    title = next((l.strip()[2:].strip() for l in lines
                  if l.strip().startswith("# ")), "")
    first = []
    for line in lines:
        text = line.strip()
        if not text or text.startswith("#"):
            if first:
                break
            continue
        if first and text.startswith("- "):
            break   # birinchi punkt tugadi
        first.append(text[2:] if text.startswith("- ") else text)
    return modified, title, " ".join(first).replace("**", "")


def _short(text, limit=160):
    if len(text) <= limit:
        return text
    return text[:limit - 3].rsplit(" ", 1)[0] + "..."


def relevant(text, labels, names=()):
    """Feedback matni shu chaqiruv belgilariga tegadimi.

    Uch yo'l: belgi naqshi matnda uchraydi (`@Transactional`), belgi nomi
    so'z sifatida uchraydi ("tranzaksiya", "test") yoki tegilgan fayl nomi
    tilga olingan. Hech biri bo'lmasa yozuv boshqa mavzuda: Java faylga
    hujjat yig'ish tuzog'i chiqmasin.
    """
    low = text.lower()
    for label, pattern, _ in SIGNALS:
        if label not in labels:
            continue
        if re.search(pattern, text):
            return True
        words = [w.strip() for w in label.split(":")]
        if any(w and re.search(r"(?<!\w)%s(?!\w)" % re.escape(w), low) for w in words):
            return True
    stems = {os.path.splitext(n)[0].lower() for n in names}
    return any(len(s) > 2 and re.search(r"(?<!\w)%s(?!\w)" % re.escape(s), low)
               for s in stems)


def _related(path, labels, names):
    try:
        with open(path, encoding="utf-8", errors="replace") as handle:
            return relevant(handle.read(), labels, names)
    except OSError:
        return False


def past_mistakes(slug=None, labels=None, names=()):
    """Memorydagi feedback yozuvlari: avval nima noto'g'ri ketgan.

    Faqat joriy proyekt papkasi va `umumiy/` o'qiladi: boshqa proyektning
    tuzog'i bu yerda shovqin. Global o'rnatishda proyekt papkasi klonda
    emas, GENIUS_MEMORY_DIR da (memory_folder). Proyekt yozuvi oldin, har papkada eng yangisi oldin. Tavsif
    indeksdan (protokol bo'yicha bir qatorli tavsif aynan o'sha yerda),
    u yo'q bo'lsa faylning birinchi gapidan.

    `labels` berilsa faqat shu belgilarga tegadigan yozuv olinadi
    (relevant): sarlavha va butun matn tekshiriladi.
    """
    out = []
    for sub in dict.fromkeys((slug or project_slug(), "umumiy")):
        folder = memory_folder(sub)
        if not os.path.isdir(folder):
            continue
        index = _index_notes(folder)
        rows = []
        for name in os.listdir(folder):
            if not (name.startswith("feedback_") and name.endswith(".md")):
                continue
            full = os.path.join(folder, name)
            try:
                modified, title, first = _topic(full)
                stamp = modified or time.strftime(
                    "%Y-%m-%dT%H:%M:%SZ", time.gmtime(os.path.getmtime(full)))
            except OSError:
                continue
            if labels is not None and not _related(full, labels, names):
                continue
            text = index.get(name) or first
            note ="%s: %s" % (title, text) if title and text else title or text
            # Global rejimda `memory/...` proyekt papkasidan ochilmaydi.
            rel = full
            if in_clone():
                try:
                    rel = os.path.relpath(full, ROOT)
                except ValueError:
                    pass  # Windows: boshqa disk
            rows.append((stamp, rel, _short(note or name)))
        rows.sort(reverse=True)
        out.extend((rel, note) for _, rel, note in rows)
    return out


def mechanical(paths):
    """check_code topgan muammolar: (qator, kalit va bo'lim, fayl, qisqa).

    Qisqa shakl (`qator kalit`) MAX_ITEMS dan keyingilar uchun: dasturchi
    eski topilmani yangisidan shu ro'yxat bo'yicha ajratadi, kesilgan
    ro'yxatda esa eskisi yangi bo'lib ko'rinardi.

    Kalit va bo'lim yonma-yon turadi: skillning birinchi qoidasi, qoidasiz
    topilma yo'q. check_code jarayon ichida chaqiriladi. Avval u har fayl
    uchun alohida jarayonda yurib, matn chiqishi qayta ajratilardi: har
    faylga ~30 ms qo'shilardi va MAX_SHOWN dan keyingi topilmalar jim
    tashlanardi.
    """
    out = []
    for path in paths:
        full = _full(path)
        for f in check_code.analyse(full):
            line = "[%s] %s:%d  %s" % (f.level, os.path.basename(full),
                                      f.line, f.message)
            ref = resolve(f.topic, f.rule, f.ref, getattr(f, "term", ""))
            tail = " ".join(x for x in (f.rule, "-> " + ref if ref else "") if x)
            out.append((line, tail, os.path.basename(full),
                        "%d %s" % (f.line, f.rule or f.topic)))
    return out


def main():
    args = sys.argv[1:]
    if not args:
        print(__doc__.strip().split("\n\n")[1].strip())
        return 2

    paths = changed_files(args)
    for name in args:
        if not name.startswith("--") and not name.endswith(WATCHED):
            print("ko'rilmadi: %s" % name, file=sys.stderr)
    if not paths:
        print("Tekshiriladigan fayl berilmadi (.java, .kt, .sql, sozlama yoki build fayli).",
              file=sys.stderr)
        return 2

    titles = chapter_titles()
    scanned = scan(paths)
    signals = ordered(scanned)
    # Zanjirning birinchi qadami bajarilgani belgilanadi: check_code Java
    # yozuvidan keyin shu belgini tekshiradi. Belgilar ham saqlanadi:
    # yozilgan fayldan yangi belgi chiqsa, check_code uni aytadi.
    # Belgini faqat yozuvchi qo'yadi. Rejalashtiruvchi va reviewer
    # --no-mark bilan chaqiradi, aks holda dasturchi uchun darvoza o'chadi.
    if "--no-mark" not in args:
        mark(paths, [label for label, _, _ in signals])

    wanted, order = set(), []
    for _, chapters, _ in signals:
        for ch in chapters:
            if ch not in wanted and len(order) < MAX_CHAPTERS:
                wanted.add(ch)
                order.append(ch)
    # Test fayli berilsa uning testing boblari chegaradan tashqarida:
    # aks holda sinalayotgan kodning entity, tranzaksiya va HTTP belgilari
    # MAX_CHAPTERS ni to'ldirib, test-muhandis birorta test bobini olmasdi.
    if any(re.search(NAME_SIGNALS["test"], "/" + p.replace("\\", "/")) for p in paths):
        for label, chapters, _ in signals:
            for ch in chapters:
                if label.startswith("test") and ch[0] == "testing" and ch not in wanted:
                    wanted.add(ch)
                    order.append(ch)
    if any(p.endswith(SOURCES) for p in paths):
        for ch in ALWAYS:
            if ch not in wanted:
                wanted.add(ch)
                order.append(ch)

    # Indeks umuman yo'q bo'lsa sabab bitta: har bob uchun "indeksda yo'q"
    # deyish jadvalni aybdor qilib ko'rsatadi va haqiqiy sababni yashiradi.
    missing = [ch for ch in order if ch not in titles]
    if not titles:
        print("OGOHLANTIRISH: indeks yo'q va yasab bo'lmadi: %s"
              % tool_cmd("build_index.py"), file=sys.stderr)
    elif missing:
        print("OGOHLANTIRISH: jadvaldagi bob indeksda yo'q: %s"
              % ", ".join("%s %s" % c for c in missing), file=sys.stderr)
    order = [ch for ch in order if ch in titles]

    for name, exists, labels in scanned:
        if exists and not labels and not name.endswith(SOURCES):
            print("belgi topilmadi: %s, %s find bilan qidiring"
                  % (name, tool_cmd("doc.sh")), file=sys.stderr)

    notes, other = profile_notes(paths)
    for note in notes:
        print(note)
    if notes:
        print()
    print("# %d fayl, %d belgi\n" % (len(paths), len(signals)))
    for label, chapters, where in signals:
        print("%-22s %-14s -> %s" % (label, where,
                                     ", ".join("%s %s" % c for c in chapters)))
    absent = [name for name, exists, _ in scanned if not exists]
    if absent:
        print("hali yo'q: %s (belgi fayl nomidan)" % ", ".join(absent))
    print()

    print("# Tegishli boblar\n")
    # Holat belgisi: `!` tekshirilmagan bob (AI yozgan), `?`
    # tekshirilmoqda. Tekshirilgan bobda belgi yo'q. Nega kerak: qoida
    # noto'g'ri bo'lsa, xato yozilayotgan kodga darhol o'tadi.
    # Belgi qator OXIRIDA: boshida bo'lsa `<hujjat> <raqam>` ustunlari
    # siljib ketardi va chiqishni o'qiydiganlar (eval_skill, test) ni
    # buzardi. Tekshirilgan bobda belgi yo'q.
    review = review_status.read_review()
    marks = {"ai-draft": "  [tekshirilmagan]",
             "tekshirilmoqda": "  [tekshirilmoqda]"}
    unverified = 0
    for ch in order:
        holat = (review.get((ch[0], str(ch[1]))) or {}).get("holat", "")
        suffix = marks.get(holat, "")
        unverified += holat == "ai-draft"
        print("  %-11s %-4s %s%s" % (ch[0], ch[1], titles[ch], suffix))
    if unverified:
        # Chapdan bo'sh joysiz: ro'yxat qatorlari ikki bo'sh joy bilan
        # boshlanadi va chiqishni o'qiydiganlar shuni ajratgich sifatida
        # ishlatadi (eval_skill, test_rules_for).
        print("\n(%d bob [tekshirilmagan]: AI yozgan, inson tekshirmagan.\n"
              "Qoidaga tayanganda shuni aytib o'ting va imkon bo'lsa\n"
              "birlamchi manbaga solishtiring: docs/review.tsv)" % unverified)
    # MAX_CHAPTERS dan ortgani jim yo'qolmasin: kerak bo'lsa ochiq so'raladi.
    dropped = list(dict.fromkeys(ch for _, chapters, _ in signals
                                 for ch in chapters if ch not in wanted))
    if dropped:
        print("\n(sig'madi: %s)" % ", ".join("%s %s" % c for c in dropped))

    items, project = checklist_for(set(order), SPRING_ONLY_RE if other else None)
    total = sum(len(v) for v in items.values())
    print("\n# Tekshiruv punktlari (%d tadan %d tasi)\n"
          % (total, min(total, MAX_POINTS)))
    print("  (faqat tegilgan kodga qo'llanadi)\n")
    shown = 0
    for round_no in range(MAX_POINTS):
        progressed = False
        for ch in order:
            bucket = items.get(ch, [])
            if round_no < len(bucket) and shown < MAX_POINTS:
                print("  - [ ] (%s %s) %s" % (ch[0], ch[1], bucket[round_no]))
                shown += 1
                progressed = True
        if shown >= MAX_POINTS or not progressed:
            break
    if total > shown or project:
        print("\n  qolgani va loyiha auditi punktlari (%d): %s checklist <hujjat> <bob>"
              % (project, tool_cmd("doc.sh")))

    found = mechanical(paths)
    print("\n# Mashina topgani (%d)\n" % len(found))
    for line, ref, _, _ in found[:MAX_ITEMS]:
        print("  " + line)
        if ref:
            print("    " + ref)
    if not found:
        print("  yo'q")
    rest = {}
    for _, _, name, short in found[MAX_ITEMS:]:
        rest.setdefault(name, []).append(short)
    if rest:
        print("\n  qolgani %d ta (matni: %s <fayl>):"
              % (len(found) - MAX_ITEMS, tool_cmd("check_code.py")))
        for name, shorts in rest.items():
            print("    %s: %s" % (name, ", ".join(shorts)))

    mistakes = past_mistakes(labels={label for label, _, _ in signals},
                             names=[name for name, _, _ in scanned])
    if mistakes:
        head = "# Avval yo'l qo'yilgan xatolar"
        if len(mistakes) > MAX_MISTAKES:
            head += " (%d tadan %d tasi)" % (len(mistakes), MAX_MISTAKES)
        print("\n%s\n" % head)
        for rel, note in mistakes[:MAX_MISTAKES]:
            print("  %s\n      %s" % (rel, note))
    return 0


if __name__ == "__main__":
    sys.exit(main())
