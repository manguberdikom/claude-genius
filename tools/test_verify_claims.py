#!/usr/bin/env python3
"""verify_claims.py uchun sinovlar.

    python3 tools/test_verify_claims.py
    python3 tools/test_verify_claims.py -k eski

Qabul sharti: 2026-10-05 da qo'lda topilgan xatolarni ("Korpus:"
commitlaridan oldingi c15a979 holati) asbob ham topadi, tuzatilgan
matnni esa tutmaydi. Fixture lar o'sha boblardan olingan qisqa
parchalar: "eski" c15a979 dagi matn, "yangi" tuzatilgan matn.
"""

import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import testkit  # noqa: E402
import verify_claims as vc  # noqa: E402

F = "```"

# --- c15a979 (eski) va tuzatilgan (yangi) parchalar ---------------------

ARCHITECT_32_ESKI = F + """properties
# Spring Boot 3.4+ markazlashgan HTTP client sozlamasi
spring.http.client.factory=jdk
spring.http.client.connect-timeout=2s
spring.http.client.read-timeout=1200ms

# Tomcat tomoni: osilgan ulanishni ushlab turmaslik
server.tomcat.connection-timeout=5s
""" + F

ARCHITECT_32_YANGI = F + """properties
# Spring Boot 3.4-3.5 markazlashgan HTTP client sozlamasi
# (Boot 4 da: spring.http.clients.imperative.factory, spring.http.clients.*)
spring.http.client.factory=jdk
spring.http.client.connect-timeout=2s
spring.http.client.read-timeout=1200ms

# Tomcat tomoni: osilgan ulanishni ushlab turmaslik
server.tomcat.connection-timeout=5s
""" + F

ARCHITECT_14_ESKI = F + """yaml
management:
  endpoints:
    web:
      exposure:
        include: health,info,metrics,prometheus,threaddump,loggers
  endpoint:
    heapdump:
      enabled: false           # kerak bo'lganda qo'lda yoqiladi
    health:
      show-details: when-authorized
""" + F

ARCHITECT_14_YANGI = ARCHITECT_14_ESKI.replace(
    "enabled: false           # kerak bo'lganda qo'lda yoqiladi",
    "access: none             # Boot 3.4+; 3.4 gacha enabled: false")

CODE_REVIEW_20_ESKI = F + """properties
# Standart Spring xato javobidan ichki detallarni olib tashlash.
server.error.include-message=never
server.error.include-stacktrace=never
server.error.include-binding-errors=never
server.error.include-exception=false
""" + F

CODE_REVIEW_20_YANGI = CODE_REVIEW_20_ESKI.replace(
    "olib tashlash.\n",
    "olib tashlash.\n# Boot 3.x kalitlari; Boot 4 da spring.web.error.include-* "
    "(pastga qarang).\n")

PATTERNS_06_ESKI = F + """yaml
// Front Controller: barcha so'rov bitta kirish nuqtasidan o'tadi
spring:
  mvc:
    servlet:
      path: /                 # DispatcherServlet qayerga ulanadi
    throw-exception-if-no-handler-found: true
  web:
    resources:
      add-mappings: false     # 404 ni handler yo'qligidan ajratish uchun
""" + F

PATTERNS_06_YANGI = PATTERNS_06_ESKI.replace("// Front", "# Front").replace(
    "    throw-exception-if-no-handler-found: true\n", "")

CODE_REVIEW_23_ESKI = """| `@Formula` | Hisoblangan maydon SQL da | Har o'qishda hisob, indekssiz |
| `@Where` | Global filtr | Jim yashirin shart - juda xavfli |
| `@SQLDelete` | Yumshoq o'chirish | O'chirilgan qatorlar hamma joyda filtrlanadimi |
| `@Cacheable` (2-daraja) | Klaster bo'ylab kesh | Invalidatsiya, klasterda mos kelish |
| `@LazyCollection(EXTRA)` | `size()` uchun alohida so'rov | Ko'pincha noto'g'ri qo'llanadi |

Uzoq izoh qatori, versiya haqida hech narsa demaydi.
Yana bir qator.
Va yana bir qator.

| `@Where`, `@SQLDelete` kabi global filtrlar bormi | Jim yashirin shart |
"""

CODE_REVIEW_23_YANGI = """| `@Formula` | Hisoblangan maydon SQL da | Har o'qishda hisob, indekssiz |
| `@SQLRestriction` (Hibernate 6.3+; 6.3 gacha `@Where`, u 7.0 da olib tashlangan) | Global filtr | Jim yashirin shart - juda xavfli |
| `@SQLDelete` | Yumshoq o'chirish | O'chirilgan qatorlar hamma joyda filtrlanadimi |
| `@LazyCollection(EXTRA)` (6.2 dan deprecated, 7.0 da olib tashlangan) | `size()` uchun alohida so'rov | Diffda ko'rinsa: Hibernate 7 (Boot 4) da kompilyatsiya bo'lmaydi |

Uzoq izoh qatori, versiya haqida hech narsa demaydi.
Yana bir qator.
Va yana bir qator.

| `@SQLRestriction`, `@SoftDelete`, `@Filter`, `@SQLDelete` kabi global shartlar bormi (eski kodda `@Where`) | Jim yashirin shart |
"""

TESTING_08_ESKI = F + """xml
<dependency>
  <groupId>org.springframework.boot</groupId>
  <artifactId>spring-boot-testcontainers</artifactId>
  <scope>test</scope>
</dependency>
<dependency>
  <groupId>org.testcontainers</groupId>
  <artifactId>junit-jupiter</artifactId>
  <scope>test</scope>
</dependency>
<dependency>
  <groupId>org.testcontainers</groupId>
  <artifactId>postgresql</artifactId>
  <scope>test</scope>
</dependency>
""" + F + """

| Texnologiya | Testcontainers moduli | Konteyner sinfi | Spring'da ulash usuli |
|---|---|---|---|
| PostgreSQL | org.testcontainers:postgresql | `PostgreSQLContainer` | `@ServiceConnection` |
"""

TESTING_08_YANGI = "Spring Boot 3.5 (Testcontainers 1.21):\n\n" + TESTING_08_ESKI.replace(
    "| PostgreSQL | org.testcontainers:postgresql |",
    "| PostgreSQL | `org.testcontainers:postgresql` | "
    "`org.testcontainers:testcontainers-postgresql` |")

SONARQUBE_26_ESKI = F + """xml
<!-- SHIKOYAT: shunday payload default parserda ishlaydi -->
<?xml version="1.0"?>
<!DOCTYPE invoice [
  <!ENTITY secret SYSTEM "file:///opt/app/application.properties">
]>
<invoice><note>&secret;</note></invoice>
""" + F

SONARQUBE_26_YANGI = SONARQUBE_26_ESKI.replace(
    '<!-- SHIKOYAT: shunday payload default parserda ishlaydi -->\n<?xml version="1.0"?>',
    '<?xml version="1.0"?>\n<!-- SHIKOYAT: shunday payload default parserda ishlaydi -->')

ARCHITECT_13_ESKI = F + """java
// Yangi variant qo'shilsa, bu switch kompilyatsiya qilinmaydi: default yo'q
String auditLine(PaymentResult result) {
    return switch (result) {
        case Captured(var ref, var amount) ->
                "olindi ref=" + ref + " summa=" + amount;
        case Declined(DeclineReason.INSUFFICIENT_FUNDS, var msg) ->
                "mablag' yetmadi: " + msg;
        case Declined(var reason, var msg) ->
                "rad etildi " + reason + ": " + msg;
    };
}
""" + F

ARCHITECT_13_YANGI = ARCHITECT_13_ESKI.replace(
    "case Declined(DeclineReason.INSUFFICIENT_FUNDS, var msg) ->",
    "case Declined(var reason, var msg)\n"
    "                when reason == DeclineReason.INSUFFICIENT_FUNDS ->")

CODE_REVIEW_36_ESKI = F + '''java
@Test
void retriesOnServerError() {
    stubFor(get("/rates/USD").inScenario("retry")
        .whenScenarioStateIs("second")
        .willReturn(okJson("""{"rate":"12750.00"}""")));

    assertThat(client.rateFor("USD")).isNotNull();
}
''' + F

CODE_REVIEW_36_YANGI = CODE_REVIEW_36_ESKI.replace(
    '"""{"rate":"12750.00"}"""', '"{\\"rate\\":\\"12750.00\\"}"')


# --- yordamchilar --------------------------------------------------------

def make_root(docs):
    """{nom: matn} -> vaqtinchalik ROOT/docs/fixture/<nom>.md."""
    root = tempfile.mkdtemp(prefix="verify_claims_t_")
    os.makedirs(os.path.join(root, "docs", "fixture"))
    for name, text in docs.items():
        with open(os.path.join(root, "docs", "fixture", name + ".md"), "w",
                  encoding="utf-8") as handle:
            handle.write("# Sinov\n\nKirish matni.\n\n" + text + "\n")
    return root


def run(text, kinds=vc.DEFAULT_KINDS, data_dir=None, notes=None):
    root = make_root({"01-bob": text})
    try:
        return vc.collect(root, kinds=kinds, data_dir=data_dir, notes=notes)
    finally:
        shutil.rmtree(root, ignore_errors=True)


def line_of(text, needle):
    """Fixture faylidagi satr raqami (make_root 4 qator sarlavha qo'shadi)."""
    for n, l in enumerate(text.split("\n"), 1):
        if needle in l:
            return n + 4
    raise AssertionError("fixture da yo'q: " + needle)


def has(found, tur, needle, line=None):
    return any(f.tur == tur and needle in f.xabar and (line is None or f.line == line)
               for f in found)


def pair(eski, yangi, tur, needles, kinds=vc.DEFAULT_KINDS):
    """Eski matnda har needle topiladi, yangisida shu turdan hech narsa yo'q."""
    def case():
        old, new = run(eski, kinds), run(yangi, kinds)
        rows = [("eski: %s [%s] topildi" % (n, tur), has(old, tur, n)) for n in needles]
        rows.append(("yangi: [%s] topilma yo'q (%s)" % (
            tur, "; ".join(vc.fmt(f) for f in new if f.tur == tur) or "toza"),
            not any(f.tur == tur for f in new)))
        return rows
    return case


def java_pair(eski, yangi, needle):
    def case():
        if vc.java_tools() is None:
            return [("javac yo'q: java holati o'tkazildi", True)]
        old, new = run(eski, ("java",)), run(yangi, ("java",))
        return [("eski: javac xatosi '%s'" % needle, has(old, "java", needle)),
                ("yangi: javac toza (%s)" % "; ".join(vc.fmt(f) for f in new),
                 not new)]
    return case


# --- holatlar ------------------------------------------------------------

def kalit_qatori():
    found = run(ARCHITECT_32_ESKI)
    want = line_of(ARCHITECT_32_ESKI, "spring.http.client.factory")
    return [("qator raqami to'g'ri", has(found, "kalit", "spring.http.client.factory", want)),
            ("almashtirish aytiladi", has(found, "kalit", "spring.http.clients.imperative.factory")),
            ("tomcat kaliti tutilmaydi", not has(found, "kalit", "server.tomcat"))]


def version_notes():
    cases = [("Spring Boot 3.4+ markazlashgan", False),
             ("Spring Boot 3.4-3.5 markazlashgan", True),
             ("Boot 4 da: spring.http.clients.*", True),
             ("Boot 3.2 dan beri", False),
             ("Boot 3.x+ da ishlaydi", False),
             ("Boot 3.x kalitlari", True),
             ("4.0 gacha ClientHttpRequestFactorySettings", True),
             ("JUnit 5 integratsiyasi", False),
             ("Spring Boot 3.5 (Testcontainers 1.21):", True),
             ("10 gacha retry", False)]
    return [("%r -> %s" % (text, want), vc.version_note(text) == want)
            for text, want in cases]


def mahsulot_izohi():
    row = {"nima": "Hibernate 6.3 da deprecated", "tur": "annotatsiya"}
    return [("Boot 4 izohi Hibernate qatorini oqlamaydi",
             not vc.version_note("Boot 3.5 da", vc.row_products(row))),
            ("Hibernate 7 izohi oqlaydi",
             vc.version_note("Hibernate 7 da yo'q", vc.row_products(row)))]


def yaml_yassilash():
    lines = ["spring:", "  cloud:", "    gateway:", "      routes:",
             "        - id: a", "          uri: http://x", "  datasource:",
             "    url: |", "      jdbc:postgresql://h/db", "      x: y",
             "    hikari:", "      maximum-pool-size: 10", "// izoh emas"]
    keys, slashes = vc.yaml_keys(lines, 1)
    paths = {k for k, _ in keys}
    return [("ro'yxat elementi ichidagi kalit",
             "spring.cloud.gateway.routes.uri" in paths),
            ("blok skalyar tanasi kalit emas", "spring.datasource.url.x" not in paths),
            ("skalyardan keyingi kalit",
             "spring.datasource.hikari.maximum-pool-size" in paths),
            ("'//' qatori ajratildi", slashes == [13])]


def relaxed_binding():
    return [("camelCase = kebab",
             vc.norm_key("spring.http.client.connectTimeout")
             == vc.norm_key("spring.http.client.connect-timeout")),
            ("indeks olib tashlanadi",
             vc.norm_key("a.b[0].c-d") == vc.norm_key("a.b.c_d"))]


def yaml_kalit_camel():
    text = F + "yaml\nspring:\n  http:\n    client:\n      connectTimeout: 2s\n" + F
    return has(run(text), "kalit", "connectTimeout")


BOM_POM = F + """xml
<dependency>
  <groupId>com.fasterxml.jackson.core</groupId>
  <artifactId>jackson-databindx</artifactId>
</dependency>
<dependency>
  <groupId>com.fasterxml.jackson.core</groupId>
  <artifactId>jackson-coreyo</artifactId>
  <version>2.17.0</version>
</dependency>
<dependency>
  <groupId>com.tngtech.archunit</groupId>
  <artifactId>archunit-junit5</artifactId>
</dependency>
<dependency>
  <groupId>com.fasterxml.jackson.core</groupId>
  <artifactId>jackson-databind</artifactId>
</dependency>
""" + F


def bom_holatlari():
    found = [f for f in run(BOM_POM) if f.tur == "bom"]
    gradle = F + 'groovy\ntestImplementation "org.testcontainers:testcontainers-postgresqlx"\n' + F
    return [("BOM da yo'q artifactId topiladi", has(found, "bom", "jackson-databindx")),
            ("versiyali bog'liqlik tekshirilmaydi", not has(found, "bom", "jackson-coreyo")),
            ("Boot boshqarmaydigan guruh tekshirilmaydi", not has(found, "bom", "archunit")),
            ("boshqariladigani toza", not has(found, "bom", "jackson-databind ")),
            ("gradle satri ham", has(run(gradle), "bom", "testcontainers-postgresqlx"))]


def bom_eski_nom():
    """Boot 3.5 da boshqarilgan, 4.1 da yo'q nom: izoh bo'lsa o'tadi."""
    data = vc.Data()
    gone = sorted((g, a) for g, arts in data.managed.get("3.5", {}).items()
                  for a in arts if g in data.managed.get("4.1", {}))
    if not gone:
        return [("3.5 da bo'lib 4.1 da yo'q nom ma'lumotda bor", False)]
    group, art = next((g, a) for g, a in gone if g != "org.testcontainers")
    pom = (F + "xml\n<dependency>\n  <groupId>%s</groupId>\n  <artifactId>%s</artifactId>\n"
           "</dependency>\n" + F) % (group, art)
    bare = run(pom)
    noted = run("Spring Boot 3.5 da:\n\n" + pom)
    return [("izohsiz: %s:%s topiladi" % (group, art), has(bare, "bom", art)),
            ("'Spring Boot 3.5 da' izohi bilan o'tadi", not has(noted, "bom", art))]


def sarlavha_va_mundarija():
    text = ("- [6.29 Lokal (LocaleResolver / ThemeResolver)](#629-lokal)\n\n"
            "## 6.29 Lokal va tema (ThemeResolver)\n\n"
            "Tema uchun `ThemeResolver` ishlating.\n")
    found = run(text)
    return [("sarlavha va mundarija tutilmaydi",
             len([f for f in found if f.tur == "api"]) == 1),
            ("matndagisi tutiladi", has(found, "api", "ThemeResolver",
                                        line_of(text, "ishlating")))]


def almashtirish_izohi():
    text = "Har xil `@MockBean`/`@MockitoBean` kombinatsiyasi yangi kontekst yaratadi.\n"
    bare = "Har xil `@MockBean` kombinatsiyasi yangi kontekst yaratadi.\n"
    return [("yonida @MockitoBean bo'lsa o'tadi", not run(text)),
            ("yolg'iz @MockBean topiladi", has(run(bare), "api", "@MockBean"))]


def artifact_jadvali():
    row = ("| Kafka | `org.testcontainers:kafka` | `org.testcontainers:testcontainers-kafka` |\n")
    return [("bir qatorda yangi nom bo'lsa o'tadi", not run(row)),
            ("org.postgresql:postgresql tutilmaydi",
             not run("`org.postgresql:postgresql` JDBC drayver.\n"))]


def java_allowlist():
    if vc.java_tools() is None:
        return [("javac yo'q: allowlist holati o'tkazildi", True)]
    body = ARCHITECT_13_ESKI.split("\n")[1:-1]
    data_dir = tempfile.mkdtemp(prefix="verify_claims_d_")
    try:
        for name in ("boot_deprecated.tsv", "boot_managed.tsv", "removed_api.tsv"):
            shutil.copy(os.path.join(vc.DATA, name), data_dir)
        with open(os.path.join(data_dir, "java_allow.tsv"), "w", encoding="utf-8") as h:
            h.write("fayl\tsha1\tsabab\ndocs/fixture/01-bob.md\t%s\tsinov\n"
                    % vc.block_sha1(body))
        notes = []
        found = run(ARCHITECT_13_ESKI, ("java",), data_dir, notes)
    finally:
        shutil.rmtree(data_dir, ignore_errors=True)
    return [("allowlistdagi blok o'tkaziladi", not found),
            ("eslatmada allowlist soni", any("1 tasi allowlistda" in n for n in notes))]


def ellipsis_va_varargs():
    if vc.java_tools() is None:
        return [("javac yo'q: holat o'tkazildi", True)]
    dots = F + "java\nvoid a() { ... }\ncase X(Y.Z, var m) -> 1;\n" + F
    varargs = F + "java\nvoid log(String... parts) { }\n" + F
    notes = []
    found = run(dots, ("java",), notes=notes)
    return [("`...` li blok o'tkaziladi", not found),
            ("varargs `...` o'rinbosar emas", not vc.PLACEHOLDER_RE.search(varargs)),
            ("o'rinbosar topiladi", bool(vc.PLACEHOLDER_RE.search("{ ... }")))]


def javac_yoq():
    saved = vc.shutil.which
    vc.shutil.which = lambda name: None
    try:
        notes = []
        found = run(ARCHITECT_13_ESKI, ("java",), notes=notes)
    finally:
        vc.shutil.which = saved
    return [("javac yo'q: topilma yo'q", not found),
            ("javac yo'q: shu aytiladi", any("javac topilmadi" in n for n in notes))]


def data_fayllari():
    data = vc.Data()
    dep = data.deprecated
    tc_new = data.managed.get("4.1", {}).get("org.testcontainers", set())
    tc_old = data.managed.get("3.5", {}).get("org.testcontainers", set())
    first = open(os.path.join(vc.DATA, "boot_deprecated.tsv"), encoding="utf-8").read(600)
    return [("boot_deprecated: http.client.factory 4.1 warning",
             dep.get(vc.norm_key("spring.http.client.factory"), {}).get("daraja") == "warning"),
            ("boot_deprecated: server.error.include-message 4.1 error",
             dep.get(vc.norm_key("server.error.include-message"), {}).get("daraja") == "error"),
            ("boot_deprecated: heapdump.enabled 4.1 da yo'q",
             dep.get(vc.norm_key("management.endpoint.heapdump.enabled"), {}).get("daraja")
             == "removed"),
            ("boot_deprecated: manba versiyasi fayl boshida",
             vc.BOOT_OLD in first and vc.BOOT_NEW in first),
            ("boot_managed: TC 2 nomi 4.1 da", "testcontainers-postgresql" in tc_new),
            ("boot_managed: eski TC nomi faqat 3.5 da",
             "postgresql" in tc_old and "postgresql" not in tc_new),
            ("removed_api: har qatorda manba",
             all(row.get("manba") for _, _, row in data.api)),
            ("java_allow: har qatorda sabab",
             all(r.get("sabab") for r in vc.read_tsv("java_allow.tsv")))]


def diff_rejimi():
    if shutil.which("git") is None:
        return [("git yo'q: holat o'tkazildi", True)]
    root = make_root({"01-bob": "toza", "02-bob": "toza"})
    try:
        def git(*args):
            subprocess.run(["git", "-C", root] + list(args), check=True,
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        git("init", "-q")
        git("-c", "user.email=t@t", "-c", "user.name=t", "add", "-A")
        git("-c", "user.email=t@t", "-c", "user.name=t", "commit", "-qm", "x")
        with open(os.path.join(root, "docs", "fixture", "02-bob.md"), "a",
                  encoding="utf-8") as handle:
            handle.write(CODE_REVIEW_20_ESKI)
        with open(os.path.join(root, "docs", "fixture", "03-yangi.md"), "w",
                  encoding="utf-8") as handle:
            handle.write("yangi\n")
        changed = vc.changed_files(root, "HEAD")
        found = vc.collect(root, changed)
    finally:
        shutil.rmtree(root, ignore_errors=True)
    return [("faqat o'zgargan va yangi bob",
             changed == ["docs/fixture/02-bob.md", "docs/fixture/03-yangi.md"]),
            ("o'zgargan bobdagi topilma", has(found, "kalit", "server.error"))]


def check_docs_ogohlantirish():
    """check_docs topilmani XATO emas, OGOHLANTIRISH qiladi."""
    import check_docs
    import test_check_docs as tcd
    tmp = tempfile.mkdtemp(prefix="verify_claims_cd_")
    try:
        errs = tcd.run(tmp, "dalil", (tcd.CH1, "Matn.", "Matn.\n\n" + CODE_REVIEW_20_ESKI))
        warns = list(check_docs.warnings)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    return [("xato qo'shilmaydi", errs == []),
            ("ogohlantirishda da'vo bor",
             any("da'vo:" in w and "server.error.include-message" in w for w in warns))]


def cli_chiqish_kodi():
    root = make_root({"01-bob": CODE_REVIEW_20_ESKI})
    saved = vc.ROOT
    vc.ROOT = root
    try:
        bad = testkit.call_main(lambda: vc.main(["--faqat", "kalit"]))
        good = testkit.call_main(lambda: vc.main(["--faqat", "xml"]))
    finally:
        vc.ROOT = saved
        shutil.rmtree(root, ignore_errors=True)
    return [("topilma bo'lsa 1", bad.returncode == 1 and "4 topilma" in bad.stdout),
            ("topilma bo'lmasa 0", good.returncode == 0)]


CASES = [
    # Qabul: c15a979 dagi qo'lda topilgan xatolar va ularning tuzatilgani.
    ("eski/yangi architect 32 spring.http.client.* (KR-Q7, KR-T-K1)",
     pair(ARCHITECT_32_ESKI, ARCHITECT_32_YANGI, "kalit",
          ["spring.http.client.factory", "spring.http.client.connect-timeout",
           "spring.http.client.read-timeout"])),
    ("eski/yangi architect 14 heapdump.enabled (KR-Q7)",
     pair(ARCHITECT_14_ESKI, ARCHITECT_14_YANGI, "kalit",
          ["management.endpoint.heapdump.enabled"])),
    ("eski/yangi code-review 20 server.error.include-* (KR-Q7)",
     pair(CODE_REVIEW_20_ESKI, CODE_REVIEW_20_YANGI, "kalit",
          ["server.error.include-message", "server.error.include-exception"])),
    ("eski/yangi patterns 6 throw-exception-if-no-handler-found (KR-Q7)",
     pair(PATTERNS_06_ESKI, PATTERNS_06_YANGI, "kalit",
          ["spring.mvc.throw-exception-if-no-handler-found"])),
    ("eski/yangi patterns 6 YAML dagi '//' (KR-Q7)",
     pair(PATTERNS_06_ESKI, PATTERNS_06_YANGI, "yaml", ["'//'"])),
    ("eski/yangi code-review 23 @Where va @LazyCollection (KR-Q4)",
     pair(CODE_REVIEW_23_ESKI, CODE_REVIEW_23_YANGI, "api",
          ["@Where", "@LazyCollection"])),
    ("eski/yangi testing 8 TC artifactId (KR-Q5)",
     pair(TESTING_08_ESKI, TESTING_08_YANGI, "api",
          ["org.testcontainers:junit-jupiter", "org.testcontainers:postgresql"])),
    ("eski/yangi sonarqube 26 XXE payload (KR-T-K2)",
     pair(SONARQUBE_26_ESKI, SONARQUBE_26_YANGI, "xml", ["declaration"])),
    ("eski/yangi architect 13 record pattern konstanta (KR-Q6)",
     java_pair(ARCHITECT_13_ESKI, ARCHITECT_13_YANGI, "<identifier> expected")),
    ("eski/yangi code-review 36 bir qatorli text block (KR-Q6)",
     java_pair(CODE_REVIEW_36_ESKI, CODE_REVIEW_36_YANGI, "text block")),
    # Qoidalar.
    ("kalit qatori va xabari", kalit_qatori),
    ("versiya izohi: ochiq va yopiq", version_notes),
    ("versiya izohi topilma mahsulotiga tegishli", mahsulot_izohi),
    ("YAML yassilash", yaml_yassilash),
    ("relaxed binding", relaxed_binding),
    ("YAML dagi camelCase kalit", yaml_kalit_camel),
    ("BOM tekshiruvi", bom_holatlari),
    ("BOM: 3.5 dagi eski nom izoh bilan", bom_eski_nom),
    ("sarlavha va mundarija da'vo emas", sarlavha_va_mundarija),
    ("almashtiruvchi nom yonida", almashtirish_izohi),
    ("artifactId jadvali va JDBC drayver", artifact_jadvali),
    ("java allowlist (fayl + sha1)", java_allowlist),
    ("java `...` va varargs", ellipsis_va_varargs),
    ("javac yo'q bo'lsa", javac_yoq),
    ("claims_data fayllari", data_fayllari),
    ("--diff faqat o'zgargan boblar", diff_rejimi),
    ("check_docs da ogohlantirish", check_docs_ogohlantirish),
    ("CLI chiqish kodi", cli_chiqish_kodi),
]


if __name__ == "__main__":
    sys.exit(testkit.run_cases(CASES, sys.argv[1:]))
