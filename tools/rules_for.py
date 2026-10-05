#!/usr/bin/env python3
"""Tegilayotgan fayllarga qaysi qoidalar tegishli ekanini bir chaqiruvda beradi.

    python3 tools/rules_for.py src/main/java/shop/OrderService.java
    python3 tools/rules_for.py --diff           # staged, unstaged va yangi fayllar (joriy repo)
    python3 tools/rules_for.py --diff --cached  # faqat staged

Nega: aktyor ikkinchi marta chaqirilsa, sababi deyarli har doim bitta -
qoidani oldindan bilmagan. Qidirib topish esa har aktyorda boshqacha
chiqadi, shuning uchun arxitektor yozgan narsani reviewer boshqa
mezon bilan tekshiradi va ish ikkinchi aylanaga tushadi.

Bu asbob shu ikkisini bitta manbaga bog'laydi. Arxitektor YOZISHDAN
OLDIN, reviewer esa TEKSHIRISHDA shu buyruqni chaqiradi: kirish bir xil,
chiqish bir xil, kelishmovchilik qolmaydi.

Nisbiy yo'l va `--diff` joriy papkadan olinadi, klondan emas: global
o'rnatishda skript klonda turadi, ish esa boshqa proyektda boradi.

Chiqish uch qism: tegishli boblar, ularning tekshiruv punktlari va
mashina allaqachon topgan muammolar.
"""

import os
import re
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

import check_code  # noqa: E402
from check_code import in_clone, strip_noise, tool_cmd  # noqa: E402
from docref import ensure_index, resolve  # noqa: E402
from state import mark  # noqa: E402

CHAPTERS = os.path.join(ROOT, "index", "chapters.tsv")
CHECKLIST = os.path.join(ROOT, "index", "checklist.tsv")
MEMORY = os.path.join(ROOT, "memory")

# Punktlar audit uchun yozilgan: ularning ko'pi butun proyektga tegishli
# ("ro'yxatla", "bir hafta kuzat"). Bitta o'zgarish uchun o'ttiztasi
# shovqin bo'ladi va o'qilmay o'tiladi. Shuning uchun kam olinadi va
# boblar bo'ylab navbatma-navbat: har mavzudan birinchi punktlar.
MAX_ITEMS = 12
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
    ("bog'liqlik", r"<dependency>|<artifactId>|implementation\s|api\s*[(']|plugins\s*\{",
     [("code-review", "33"), ("sonarqube", "39")]),

    # --- ma'lumot va tranzaksiya ---
    ("entity va ORM", r"@Entity\b|@Table\b|@ManyToOne\b|@OneToMany\b|@Column\b",
     [("patterns", "9"), ("architect", "18"), ("sonarqube", "29"),
      ("code-review", "23"), ("clean-code", "28")]),
    ("ma'lumotga kirish",
     r"\b(?:JpaRepository|CrudRepository|ListCrudRepository|PagingAndSortingRepository)\b"
     r"|@Repository\b",
     [("patterns", "9"), ("architect", "18"), ("code-review", "23"),
      ("code-review", "24")]),
    ("tranzaksiya", r"@Transactional\b",
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
    ("konkurentlik", r"\bsynchronized\b|ReentrantLock|AtomicInteger|AtomicLong|ExecutorService",
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
     [("clean-code", "6"), ("clean-code", "7")]),
]

# Build fayllari. Ular kod kabi tekshiruvga muhtoj, lekin .java emas.
BUILD_FILES = ("pom.xml", "build.gradle", "build.gradle.kts",
               "settings.gradle", "settings.gradle.kts")
BUILD_ONLY = {"bog'liqlik"}

# Qaysi fayllar ko'riladi. Migratsiya (.sql, Liquibase .xml/.yaml) va
# sozlama (application.yml) ham: ularning review bobi bor, .java dan esa
# ko'rinmaydi.
WATCHED = (".java", ".sql", ".yml", ".yaml", ".properties", ".xml") + BUILD_FILES

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
    "xavfsizlik: ruxsat": r"Security\w*\.java$",
    "entity va ORM": r"/(?:entity|entities)/[^/]+\.java$|Entity\.java$",
    "ma'lumotga kirish": r"Repository\.java$",
    "broker": r"(?:Listener|Consumer)\.java$",
    "test": r"/test/|(?:Test|Tests|IT)\.java$",
    "web qatlami": r"Controller\.java$",
    "konfiguratsiya": r"(?:Config|Configuration|Properties)\.java$",
    "mapper": r"Mapper\.java$",
    "rejalashtirilgan ish": r"(?:Job|Scheduler)\.java$",
    "servis qatlami": r"Service\.java$",
}

# Har Java fayl uchun, belgisidan qat'i nazar.
ALWAYS = [("clean-code", "2"), ("clean-code", "4"), ("code-review", "8")]

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
    try:
        proc = subprocess.run(["git"] + args, capture_output=True,
                              text=True, cwd=cwd)
    except OSError:
        return ""
    return proc.stdout if proc.returncode == 0 else ""


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
            if slash.endswith(".java"):
                text = strip_noise(text)
        labels = set()
        for label, pattern, _ in SIGNALS:
            if re.search(PATH_SIGNALS.get(label, NEVER), slash):
                labels.add(label)
            elif text is None:
                if slash.endswith(".java") and re.search(
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


def checklist_for(wanted):
    """Berilgan boblarning tekshiruv punktlari, bob tartibida."""
    items = {}
    ensure_index("checklist.tsv")
    if not os.path.exists(CHECKLIST):
        return items
    with open(CHECKLIST, encoding="utf-8") as handle:
        handle.readline()
        for line in handle:
            parts = line.rstrip("\n").split("\t")
            if len(parts) == 4 and (parts[0], parts[1]) in wanted:
                items.setdefault((parts[0], parts[1]), []).append(parts[3])
    return items


def project_slug():
    """memory/README.md qoidasi: repo nomi kichik harfda, ikki egada bir
    xil nom bo'lsa `<egasi>__<repo>`, repo yo'q bo'lsa ildiz papka nomi."""
    here = os.getcwd()
    top = _git(["rev-parse", "--show-toplevel"], here).strip() or here
    url = _git(["remote", "get-url", "origin"], top).strip().rstrip("/")
    parts = [p for p in re.split(r"[/:]", url) if p]
    if not parts:
        return os.path.basename(os.path.normpath(top)).lower()
    repo = parts[-1].lower()
    repo = repo[:-4] if repo.endswith(".git") else repo
    if len(parts) > 1:
        both = "%s__%s" % (parts[-2].lower(), repo)
        if os.path.isdir(os.path.join(MEMORY, both)):
            return both
    return repo


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

    Fayl frontmatter bilan boshlanadi (memory-protocol.md), u tashlanadi:
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


def past_mistakes(slug=None):
    """Memorydagi feedback yozuvlari: avval nima noto'g'ri ketgan.

    Faqat joriy proyekt papkasi va `umumiy/` o'qiladi: global o'rnatishda
    memory/ hamma proyektni saqlaydi, boshqasining tuzog'i bu yerda
    shovqin. Proyekt yozuvi oldin, har papkada eng yangisi oldin. Tavsif
    indeksdan (protokol bo'yicha bir qatorli tavsif aynan o'sha yerda),
    u yo'q bo'lsa faylning birinchi gapidan.
    """
    out = []
    for sub in dict.fromkeys((slug or project_slug(), "umumiy")):
        folder = os.path.join(MEMORY, sub)
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
            text = index.get(name) or first
            note = "%s: %s" % (title, text) if title and text else title or text
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
    """check_code topgan muammolar, har biri Sonar kaliti va bo'limi bilan.

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
            ref = resolve(f.topic, f.rule, f.ref)
            tail = " ".join(x for x in (f.rule, "-> " + ref if ref else "") if x)
            out.append((line, tail))
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
        print("Tekshiriladigan fayl berilmadi (.java, .sql, sozlama yoki build fayli).",
              file=sys.stderr)
        return 2

    titles = chapter_titles()
    scanned = scan(paths)
    signals = ordered(scanned)
    # Zanjirning birinchi qadami bajarilgani belgilanadi: check_code har
    # Java yozuvidan keyin shuni tekshiradi. Belgilar ham saqlanadi:
    # yozilgan fayldan yangi belgi chiqsa, check_code uni aytadi.
    mark(paths, [label for label, _, _ in signals])

    wanted, order = set(), []
    for _, chapters, _ in signals:
        for ch in chapters:
            if ch not in wanted and len(order) < MAX_CHAPTERS:
                wanted.add(ch)
                order.append(ch)
    if any(p.endswith(".java") for p in paths):
        for ch in ALWAYS:
            if ch not in wanted:
                wanted.add(ch)
                order.append(ch)

    missing = [ch for ch in order if ch not in titles]
    if missing:
        print("OGOHLANTIRISH: jadvaldagi bob indeksda yo'q: %s"
              % ", ".join("%s %s" % c for c in missing), file=sys.stderr)
        order = [ch for ch in order if ch in titles]

    for name, exists, labels in scanned:
        if exists and not labels and not name.endswith(".java"):
            print("belgi topilmadi: %s, %s find bilan qidiring"
                  % (name, tool_cmd("doc.sh")), file=sys.stderr)

    print("# %d fayl, %d belgi\n" % (len(paths), len(signals)))
    for label, chapters, where in signals:
        print("%-22s %-14s -> %s" % (label, where,
                                     ", ".join("%s %s" % c for c in chapters)))
    absent = [name for name, exists, _ in scanned if not exists]
    if absent:
        print("hali yo'q: %s (belgi fayl nomidan)" % ", ".join(absent))
    print()

    print("# Tegishli boblar\n")
    for ch in order:
        print("  %-11s %-4s %s" % (ch[0], ch[1], titles[ch]))
    # MAX_CHAPTERS dan ortgani jim yo'qolmasin: kerak bo'lsa ochiq so'raladi.
    dropped = list(dict.fromkeys(ch for _, chapters, _ in signals
                                 for ch in chapters if ch not in wanted))
    if dropped:
        print("\n(sig'madi: %s)" % ", ".join("%s %s" % c for c in dropped))

    items = checklist_for(set(order))
    total = sum(len(v) for v in items.values())
    print("\n# Tekshiruv punktlari (%d tadan %d tasi)\n"
          % (total, min(total, MAX_ITEMS)))
    print("  (punkt faqat tegilgan kodga nisbatan qo'llanadi; butun proyekt "
          "auditi so'ralmagan bo'lsa bajarilmaydi)\n")
    shown = 0
    for round_no in range(MAX_ITEMS):
        progressed = False
        for ch in order:
            bucket = items.get(ch, [])
            if round_no < len(bucket) and shown < MAX_ITEMS:
                print("  - [ ] (%s %s) %s" % (ch[0], ch[1], bucket[round_no]))
                shown += 1
                progressed = True
        if shown >= MAX_ITEMS or not progressed:
            break
    if total > shown:
        print("\n  qolgani: %s checklist <hujjat> <bob>" % tool_cmd("doc.sh"))

    found = mechanical(paths)
    print("\n# Mashina topgani (%d)\n" % len(found))
    for line, ref in found[:MAX_ITEMS]:
        print("  " + line)
        if ref:
            print("    " + ref)
    if not found:
        print("  yo'q")

    mistakes = past_mistakes()
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
