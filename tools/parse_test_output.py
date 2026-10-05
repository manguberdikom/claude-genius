#!/usr/bin/env python3
"""Maven yoki Gradle test chiqishidan faqat muhimini ajratadi.

    mvn test 2>&1 | python3 tools/parse_test_output.py
    ./gradlew test 2>&1 | python3 tools/parse_test_output.py
    python3 tools/parse_test_output.py target/surefire-reports/out.txt
    gh run view <id> --log-failed | python3 tools/parse_test_output.py

Nega: yiqilgan test 200-2000 qator chiqish beradi, undan kerakli uchta
qator: qaysi test, nima kutilgan edi, loyiha kodining qaysi qatorida.
Qolgani framework ichidagi stack va takrorlangan oqibatlar.

Testni qayta ishga tushirish sababni ko'rsatmaydi, chiqishni o'qish
ko'rsatadi. Shuning uchun bu asbob bor.

Asbob jim yolg'on gapirmasligi kerak: kompilyatsiya xatosi, tanilmagan
format yoki xulosada yiqilish bor-u test nomi topilmagan holat 1 bilan
tugaydi. "Yiqilgan test topilmadi" va 0 faqat build ham yiqilmaganda.
"""

import os
import re
import sys
from collections import OrderedDict

# Stack qatoridagi shu prefikslar framework, loyiha kodi emas.
FRAMEWORK = (
    "java.", "javax.", "jakarta.", "jdk.", "sun.", "com.sun.",
    "org.junit", "junit.", "org.opentest4j", "org.hamcrest", "org.assertj",
    "org.mockito", "net.bytebuddy", "org.objenesis",
    "org.springframework", "org.apache.maven", "org.apache.tools",
    "org.gradle", "worker.org.gradle", "org.testcontainers",
    "com.intellij", "jdk.internal",
    "org.hibernate", "com.fasterxml", "com.zaxxer", "org.postgresql",
    "org.flywaydb", "liquibase", "reactor.", "io.netty", "io.micrometer",
    "io.github.resilience4j", "org.aspectj", "ch.qos.logback", "org.slf4j",
    "kotlin.", "kotlinx.", "feign.", "okhttp3.", "org.apache.catalina",
    "org.apache.tomcat", "org.apache.kafka", "io.restassured",
    "org.awaitility", "org.skyscreamer", "com.jayway.jsonpath", "org.h2.",
)
# Paket ildizi shulardan biri bo'lsa loyiha prefiksi ikki segment bo'ladi
# (com.acme.), aks holda bitta (shop.). Bitta segmentli "com." loyiha
# kodini com.fasterxml bilan adashtirardi.
GENERIC_ROOTS = {"com", "org", "net", "io", "dev", "app", "uz", "ru", "de",
                 "co", "me", "edu", "gov"}

# Modul prefiksi bo'lishi mumkin: "at app//shop.Foo.bar(...)" yoki
# "at java.base/jdk.internal...". U tashlanadi, sinf nomi qoladi.
FRAME_RE = re.compile(
    r"^\s*at (?:[\w$.]+/{1,2})?([\w$.]+)\.([\w$<>]+)\(([^)]*)\)")
# Parametrli test chaqirig'i ham alohida: computes(int, String)[3]
METHOD = r"[\w$]+(?:\([^)]*\))?(?:\[\d+\])*"
# Surefire batafsil bloki (3.x; report .txt da [ERROR] bo'lmaydi):
#   [ERROR] shop.web.OrderControllerTest.createsOrder -- Time elapsed: 0.05 s <<< FAILURE!
DETAIL_RE = re.compile(
    r"^(?:\[ERROR\]\s+)?([\w$.]+)\.(%s)\s+(?:--\s+)?Time elapsed:.*<<<" % METHOD)
# Surefire 2.x: "[ERROR] createsOrder(shop.web.OrderControllerTest)  Time elapsed: ..."
DETAIL2_RE = re.compile(
    r"^(?:\[ERROR\]\s+)?([\w$]+(?:\[\d+\])*)\(([\w$.]+)\)\s+Time elapsed:.*<<<")
# Results bo'limi: "[ERROR]   OrderControllerTest.createsOrder:58 xabar"
MAVEN_FAIL_RE = re.compile(
    r"^\[ERROR\]\s+([\w$.]+)\.(%s)(?::(\d+))?(?:\s+(.*))?$" % METHOD)
# Gradle: "MoneyTest > addsAmounts() FAILED", "PriceTest > p(int) > [2] 5 FAILED",
# "Order Service > places order FAILED". "> Task :test FAILED" tushmaydi.
GRADLE_FAIL_RE = re.compile(r"^([^\s>][^>]*?)\s+>\s+(.+?)\s+FAILED\s*$")
GRADLE_END_RE = re.compile(
    r"^(?:\d+ tests? completed|> Task |FAILURE:|BUILD (?:FAILED|SUCCESSFUL)|\* What went wrong)")
# Gradle standart (SHORT) formati: "    org.opentest4j.AssertionFailedError at MoneyTest.java:24"
SHORT_RE = re.compile(
    r"^\s+((?:[\w$]+\.)+[\w$]+) at ([\w$]+\.(?:java|kt|groovy|scala)):(-?\d+)\s*$")
EXCEPTION_RE = re.compile(
    r"^\s*(?:Caused by:\s*)?([\w$.]*(?:Exception|Error|Failure)"
    r"|(?:[a-z_][\w$]*\.)+[A-Z][\w$]*(?=:))(?::\s*(.*))?$")
# Eng ichki "Caused by" asl sabab: Spring context yiqilishida tepadagi
# IllegalStateException hech narsa aytmaydi.
ROOT_RE = re.compile(r"^\s*Caused by:\s*([\w$.]+)(?::\s*(.*)|\s+at\s+\S+)?\s*$")
SUMMARY_RE = re.compile(
    r"Tests run:\s*(\d+),\s*Failures:\s*(\d+),\s*Errors:\s*(\d+)(?:,\s*Skipped:\s*(\d+))?")
# Gradle: "12 tests completed, 2 failed, 1 skipped"
GRADLE_SUMMARY_RE = re.compile(
    r"(\d+) tests? completed(?:,\s*(\d+) failed)?(?:,\s*(\d+) skipped)?")
# Kompilyatsiya xatosi: faqat xato, ogohlantirish emas.
COMPILE_RES = (
    re.compile(r"^\[ERROR\]\s+(\S+\.(?:java|kt|groovy|scala)):\[(\d+)(?:,\d+)?\]\s*(.*)$"),
    re.compile(r"^(\S+\.(?:java|groovy|scala)):(\d+):\s*error:\s*(.*)$"),
    re.compile(r"^e:\s+(?:file://)?(\S+\.kts?):(\d+):\d+\s*(.*)$"),
    re.compile(r"^e:\s+(\S+\.kts?):\s*\((\d+),\s*\d+\):\s*(.*)$"),
)
SYMBOL_RE = re.compile(r"^(?:\[ERROR\])?\s*symbol:\s*(.+?)\s*$")
BUILD_FAIL_RE = re.compile(
    r"BUILD FAILURE|BUILD FAILED|^\[ERROR\] Failed to execute goal"
    r"|^FAILURE: Build failed|^> Task \S+ FAILED|Execution failed for task")
CLUE_RE = re.compile(r"^\[ERROR\]\s*\S|FAILED|What went wrong|Execution failed")
# CI jurnali har qator boshiga vaqt qo'yadi: GitHub Actions xom logi
# "2026-10-05T10:11:12.1234567Z [ERROR] ...", `gh run view --log` esa
# oldiga yana "job<TAB>step<TAB>". Qator boshiga bog'langan regexlar
# (test nomi, blok chegarasi, stack qatori) prefiksni ko'rmasin.
CI_PREFIX_RE = re.compile(
    r"^\ufeff?(?:[^\t\n]*\t[^\t\n]*\t)?\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d(?:\.\d+)?Z ?")


def strip_ci_prefix(lines):
    """Birinchi bo'sh bo'lmagan qatorda CI prefiksi bo'lsa, hamma qatordan
    olinadi. Oddiy chiqishga tegilmaydi: ilova logidagi vaqt o'sha
    qatorning bir qismi.

    Prefiks qolsa Maven da xulosada yiqilish bor-u, test nomi
    tanilmasdi; Gradle da vaqt test nomiga yopishib, `> Task :test
    FAILED` qatori ham yiqilgan test deb sanalardi."""
    first = next((line for line in lines if line.strip()), "")
    if not CI_PREFIX_RE.match(first):
        return lines
    return [CI_PREFIX_RE.sub("", line, count=1) for line in lines]


def bracketed(match):
    return match.group(1), match.group(2)


def expecting(match):
    # AssertJ: actual birinchi, keyin "to contain:" va kutilgan qiymat.
    return "%s %s" % (match.group(2), match.group(3)), match.group(1)


# Tartib muhim: birinchi mos kelgani olinadi.
EXPECTED_PATTERNS = (
    # JUnit 5/4: "expected: <201> but was: <500>"
    (re.compile(r"expect(?:ed)?[:\s]*[<\[](.*?)[>\]].*?but was[:\s]*[<\[](.*?)[>\]]",
                re.I | re.S), bracketed),
    # AssertJ: "expected: \"Alice\"" / " but was: \"Bob\""
    (re.compile(r"^\s*expected:\s*(.+?)\s*\n\s*but was:\s*(.+?)\s*$", re.I | re.M),
     bracketed),
    # Hamcrest: "Expected: is <90>" / "     but: was <100>"
    (re.compile(r"^\s*Expected:\s*(.+?)\s*\n\s*but:\s*(.+?)\s*$", re.M), bracketed),
    # AssertJ: "Expecting actual:" / X / "to contain:" / Y
    (re.compile(r"^\s*Expecting(?: actual)?:\s*\n\s*(.+?)\s*\n\s*(to [^\n]+?):\s*\n\s*(.+?)\s*$",
                re.M), expecting),
    # AssertJ hasSize: "Expected size: 2 but was: 1"
    (re.compile(r"expected size:\s*(\S+)\s+but was:\s*(\S+)", re.I), bracketed),
)

MAX_SHOWN = 3


def is_project_frame(cls):
    return not cls.startswith(FRAMEWORK)


def project_prefix(test):
    """`com.acme.shop.web.XTest.m` -> "com.acme.", `shop.web.XTest.m` -> "shop."."""
    package = test.split(" ")[0].split("(")[0].split(".")[:-2]
    width = 2 if package and package[0] in GENERIC_ROOTS else 1
    return ".".join(package[:width]) + "." if len(package) >= width else ""


def simple(name):
    return name.rsplit(".", 1)[-1]


class Failure:
    def __init__(self, test):
        self.test = test
        self.exception = ""
        self.message = ""
        self.expected = None
        self.actual = None
        self.frame = ""
        self.root = ""
        self.short = False

    def key(self):
        """Bir xil sabab bir marta ko'rsatiladi."""
        return (self.exception, self.message[:120], self.frame,
                self.expected, self.actual, self.root)

    def render(self):
        out = ["%s" % self.test]
        head = ""
        if self.exception or self.message:
            head = self.exception or ""
            if self.message:
                head = ("%s: %s" % (head, self.message)).strip(": ")
            out.append("    %s" % head[:300])
        if self.expected is not None:
            out.append("    kutilgan: %s" % self.expected[:120])
            out.append("    olingan : %s" % self.actual[:120])
        if self.root and self.root != head:
            out.append("    asl sabab: %s" % self.root[:300])
        if self.frame:
            out.append("    kod     : %s" % self.frame)
        return "\n".join(out)


def detail_header(line):
    match = DETAIL_RE.match(line)
    if match:
        return "%s.%s" % (match.group(1), match.group(2))
    match = DETAIL2_RE.match(line)
    if match:
        return "%s.%s" % (match.group(2), match.group(1))
    return None


def identity(name):
    """`shop.PriceTest.computes(int, String)[1]` -> ("PriceTest", "computes")."""
    cls, _, method = re.sub(r"[(\[].*$", "", name).rpartition(".")
    return simple(cls), method


def split_blocks(lines):
    """Chiqishni yiqilish bloklariga bo'ladi.

    Blok yiqilgan test nomidan boshlanib, keyingi test nomigacha yoki
    blokka tegishli bo'lmagan qatorgacha davom etadi. Shu tufayli stack
    qatorlari o'z testiga tegishli bo'ladi.

    Surefire bitta yiqilishni ikki marta aytadi: batafsil blokda
    (`-- Time elapsed ... <<< FAILURE!`) va oxiridagi Results ro'yxatida.
    Results qatori faqat batafsil bloki yo'q test uchun olinadi.
    `[INFO] Results:` belgisiga tayanilmaydi: `mvn -q` uni chiqarmaydi.
    """
    detailed, short = OrderedDict(), OrderedDict()
    current, target, gradle_block = None, None, False
    for line in lines:
        header = detail_header(line)
        gradle = None if header else GRADLE_FAIL_RE.match(line)
        if header or gradle:
            if gradle:
                method = gradle.group(2).strip()
                header = "%s.%s" % (gradle.group(1).strip(),
                                    method[:-2] if method.endswith("()") else method)
            current, target, gradle_block = header, detailed, bool(gradle)
            target.setdefault(current, [])
            continue
        maven = MAVEN_FAIL_RE.match(line)
        if maven and not line.startswith("[ERROR] Tests run"):
            current, target, gradle_block = "%s.%s" % maven.group(1, 2), short, False
            target.setdefault(current, [])
            if maven.group(4):
                target[current].append(maven.group(4))
            continue
        if current is None:
            continue
        if (GRADLE_END_RE.match(line) if gradle_block
                else re.match(r"\[(?:INFO|WARNING|ERROR)\]", line)):
            current = None
            continue
        target[current].append(line)

    covered = {identity(name) for name in detailed}
    for name, body in short.items():
        if identity(name) not in covered:
            detailed[name] = body
    return detailed


def expected_actual(text):
    for pattern, extract in EXPECTED_PATTERNS:
        match = pattern.search(text)
        if match:
            expected, actual = extract(match)
            return " ".join(expected.split()), " ".join(actual.split())
    return None, None


def parse_block(test, body):
    failure = Failure(test)
    failure.expected, failure.actual = expected_actual("\n".join(body))
    prefix = project_prefix(test)
    if not prefix:
        # Gradle sarlavhasida paket yo'q (`OrderServiceTest > m() FAILED`):
        # prefiks test sinfining o'z kadridan. Aks holda FRAMEWORK da yo'q
        # birinchi kutubxona qatori (Guava) "kod" deb ko'rsatilardi.
        test_cls = identity(test)[0]
        for line in body:
            frame = FRAME_RE.match(line)
            if frame and simple(frame.group(1)) == test_cls:
                prefix = project_prefix(frame.group(1) + ".m")
                break
    fallback = short_frame = ""
    wants_message = False

    for line in body:
        frame = FRAME_RE.match(line)
        root = ROOT_RE.match(line)
        if root:
            failure.root = simple(root.group(1))
            if root.group(2):
                failure.root += ": " + " ".join(root.group(2).split())
        if not failure.exception and not frame:
            short = SHORT_RE.match(line)
            exc = None if short else EXCEPTION_RE.match(line)
            if short:
                failure.exception = simple(short.group(1))
                failure.short = True
                short_frame = "%s:%s" % (short.group(2), short.group(3))
                continue
            if exc and exc.group(1):
                failure.exception = simple(exc.group(1))
                failure.message = " ".join((exc.group(2) or "").split())
                wants_message = not failure.message
                continue
        if wants_message and line.strip() and not frame:
            # AssertJ/Mockito: xabar istisno nomidan keyingi qatorda.
            if failure.expected is None:
                failure.message = " ".join(line.split())[:200]
            wants_message = False
        if frame:
            wants_message = False
            cls = frame.group(1)
            text = "%s.%s(%s)" % (simple(cls), frame.group(2), frame.group(3))
            if not failure.frame and prefix and cls.startswith(prefix):
                failure.frame = text
            if not fallback and is_project_frame(cls):
                fallback = text

    failure.frame = failure.frame or fallback or short_frame
    if not failure.exception and failure.expected is None:
        first = next((l.strip() for l in body if l.strip()), "")
        failure.message = " ".join(first.split())[:200]
    return failure


def summarize(lines):
    """[jami, yiqildi, xato, o'tkazildi] yoki None.

    Maven har sinf uchun (`Time elapsed` bilan) va har modul uchun
    (`Time elapsed` siz) qator chiqaradi. Modul qatorlari yig'iladi, ular
    bo'lmasa (masalan surefire-reports/*.txt) sinf qatorlari. Gradle har
    test vazifasi uchun bitta qator beradi, ular ham yig'iladi.
    """
    sums = {"module": None, "class": None, "gradle": None}

    def add(kind, values):
        sums[kind] = [a + b for a, b in zip(sums[kind] or [0, 0, 0, 0], values)]

    for line in lines:
        gradle = GRADLE_SUMMARY_RE.search(line)
        if gradle:
            run, fail, skip = (int(g or 0) for g in gradle.groups())
            add("gradle", (run, fail, 0, skip))
            continue
        match = SUMMARY_RE.search(line)
        if match:
            add("class" if "Time elapsed" in line else "module",
                [int(g or 0) for g in match.groups()])
    return sums["module"] or sums["class"] or sums["gradle"]


def compile_errors(lines):
    """{(fayl, qator, xabar): symbol}. Maven har xatoni ikki marta
    chiqaradi (COMPILATION ERROR va Failed to execute goal ostida),
    shuning uchun kalit bo'yicha takrorsiz."""
    found = OrderedDict()
    for i, line in enumerate(lines):
        match = compile_error(line)
        if not match:
            continue
        path, number, message = match.groups()
        key = (os.path.basename(path), number, re.sub(r"^error:\s*", "", message.strip()))
        symbol = ""
        for after in lines[i + 1:i + 4]:
            # Keyingi xato yoki goal qatori boshqa xatoning symbol'ini bermasin.
            if compile_error(after) or BUILD_FAIL_RE.search(after):
                break
            hit = SYMBOL_RE.match(after)
            if hit:
                symbol = hit.group(1)
                break
        if not found.get(key):
            found[key] = symbol
    return found


def compile_error(line):
    for pattern in COMPILE_RES:
        match = pattern.match(line.rstrip())
        if match:
            return match
    return None


def unrecognised(lines, totals):
    """Test bloki topilmadi, lekin build yiqilgan: jim 0 o'rniga sabab
    qidirish uchun birinchi belgilar. Yiqilish yo'q bo'lsa None."""
    failed = totals[1] + totals[2] if totals else 0
    if not failed and not any(BUILD_FAIL_RE.search(l) for l in lines):
        return None
    if failed:
        head = ("Xulosada %d ta yiqilish bor, lekin format tanilmadi: "
                "chiqishning o'zini o'qing." % failed)
    else:
        head = "Build yiqilgan, lekin sabab ajratilmadi: chiqishning o'zini o'qing."
    clues = []
    for line in lines:
        text = line.strip()
        if CLUE_RE.search(text) and text not in clues:
            clues.append(text)
        if len(clues) == 5:
            break
    return [head] + ["    %s" % c[:200] for c in clues]


def main():
    if len(sys.argv) > 1:
        path = sys.argv[1]
        if not os.path.exists(path):
            print("fayl yo'q: %s" % path, file=sys.stderr)
            return 2
        with open(path, encoding="utf-8", errors="replace") as handle:
            lines = handle.read().split("\n")
    else:
        lines = sys.stdin.read().split("\n")
    lines = strip_ci_prefix(lines)

    totals = summarize(lines)
    compiled = compile_errors(lines)
    blocks = split_blocks(lines)
    failures = [parse_block(t, b) for t, b in blocks.items()]

    unique = OrderedDict()
    for failure in failures:
        unique.setdefault(failure.key(), failure)
    unique = list(unique.values())

    if totals:
        print("Tests: %d, yiqildi: %d, xato: %d, o'tkazildi: %d"
              % tuple(totals))

    if compiled:
        print("Kompilyatsiya xatosi: %d ta%s\n"
              % (len(compiled), "." if unique else ", testlar yurmadi."))
        for (name, number, message), symbol in list(compiled.items())[:MAX_SHOWN]:
            print(message[:300])
            if symbol:
                print("    symbol  : %s" % symbol)
            print("    kod     : %s:%s" % (name, number))
            print()
        if len(compiled) > MAX_SHOWN:
            print("... yana %d ta xato\n" % (len(compiled) - MAX_SHOWN))

    if not unique:
        if compiled:
            print("Birinchisidan boshlang: keyingilari ko'pincha shuning oqibati.")
            return 1
        report = unrecognised(lines, totals)
        if report:
            print("\n".join(report))
            return 1
        print("Yiqilgan test topilmadi.")
        return 0

    print("Noyob sabab: %d ta (jami %d ta yiqilish)\n"
          % (len(unique), len(failures)))
    for failure in unique[:MAX_SHOWN]:
        print(failure.render())
        print()
    if len(unique) > MAX_SHOWN:
        print("... yana %d ta sabab" % (len(unique) - MAX_SHOWN))
    if any(f.short for f in unique[:MAX_SHOWN]):
        print("Gradle qisqa formati xabarni bermaydi: to'liq matn "
              "build/test-results/test/*.xml da yoki testLogging "
              "{ exceptionFormat 'full' } bilan.")
    print("Birinchisidan boshlang: keyingilari ko'pincha shuning oqibati.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
