#!/usr/bin/env python3
"""Ta'sirlangan testlarni topadi va modulga bog'langan buyruq bilan yurgizadi.

    python3 tools/run_tests.py --diff                  # reja: qaysi testlar, nega
    python3 tools/run_tests.py --diff --yurgiz         # yurgizadi, birinchi sababni beradi
    python3 tools/run_tests.py <fayl>... --yurgiz      # berilgan fayllar bo'yicha
    python3 tools/run_tests.py --asos main --yurgiz    # guruh: main...HEAD va ishchi o'zgarish
    python3 tools/run_tests.py --modul orders --yurgiz # bitta modulning hammasi
    python3 tools/run_tests.py --hammasi --yurgiz      # to'liq suite: partiyada bir marta
    python3 tools/run_tests.py --tashxis               # suite nega sekin
    python3 tools/run_tests.py --isit                  # fonda oldindan kompilyatsiya
    python3 tools/run_tests.py --hisobot               # test vaqti jurnali, 7 kun

Chiqish kodi: 0 yashil, 1 yiqildi, 2 noto'g'ri kirish (loyiha yo'q,
`--asos` commit emas, `--log` temp yoki loyihadan tashqarida), 3 vaqt
tugadi, 4 beqaror (yiqilgan sinf qayta yurishda o'tdi: o'zgarish emas,
flaky ehtimoli, lekin yashil ham emas).

Nega: to'liq suite 5-8 daqiqa, aktyor esa uni 2-4 marta yurgizardi.
Sabab faqat odat emas. Ko'p modulli Gradle da `test --tests X` X yo'q
har modulda "No tests found for given includes" bilan yiqiladi
(`failOnNoMatchingTests` standarti true), Maven da `-Dtest=X` esa "No
tests matching pattern" bilan. Shu yiqilishdan keyin aktyor filtrsiz
suite ga qaytardi. Asbob modulni o'zi qo'yadi: `:orders:test --tests X`,
`-pl orders -am -Dsurefire.failIfNoSpecifiedTests=false`.

Buyruqni asbobning o'zi yurgizadi: chiqish log faylga yoziladi, ekranga
`parse_test_output.py` xulosasi chiqadi. Gradle chiqishi kontekstga
tushmaydi va asbob o'rnatuvchining ruxsat ro'yxatida bo'lgani uchun har
yurishda ruxsat so'ralmaydi. Har yurish to'g'ri buyruq bilan bo'ladi:
`clean`, `--rerun-tasks` va `--no-daemon` yo'q, chunki ular inkremental
build va daemon ni yo'qotadi.

Gradle buyrug'iga init skript qo'shiladi (`-I`, build fayllariga
tegmaydi): maqsadli yurishda jacoco agenti, hisobot va coverage
tekshiruvi o'chadi, HTML hisobot yozilmaydi; har yurishda JUnit XML
majburiy. Loyiha keshni tanlamagan bo'lsa faqat kompilyatsiya lokal
keshlanadi: yangi worktree boshqa daraxt kompilyatsiya qilgan modulni
qayta kompilyatsiya qilmaydi, test esa har gal haqiqatan yuradi.

Tanlash, eng aniqdan kengiga:
  1. o'zgargan test sinfi;
  2. o'zgargan sinf nomiga mos test (FooTest, FooIT, ...);
  3. o'zgargan sinfga murojaat qilgan test;
  4. bir qadam narida: o'zgargan sinfni ishlatgan sinfning testlari;
  5. sozlama, migratsiya yoki build fayli: modulning tegishli testlari.
Bu taxminiy tanlash. Uning xavfsizlik to'ri: partiya oxirida bir marta
yuradigan to'liq suite (`--hammasi`). Tanlash biror testni o'tkazib
yuborsa, u o'sha yerda chiqadi va egasiga qaytadi.
"""

import argparse
import contextlib
import hashlib
import io
import json
import os
import re
import shlex
import subprocess
import sys
import tempfile
import time
import xml.etree.ElementTree as ET
from collections import OrderedDict

HERE = os.path.dirname(os.path.abspath(__file__))
PARSER = os.path.join(HERE, "parse_test_output.py")

# Manba fayl: <modul>/src/<to'plam>/<til>/<paket>/<Sinf>.<kengaytma>
SOURCE_RE = re.compile(
    r"(?:^|/)src/([^/]+)/(?:java|kotlin|groovy)/(.+)\.(?:java|kt|groovy)$")
# Test usuli bor sinf. Nomga emas, mazmunga qaraladi: Gradle test
# to'plamidagi har sinfni yurgizadi, nomi Test bilan tugamasa ham.
TEST_MARK_RE = re.compile(
    r"@(?:org\.junit\.(?:jupiter\.api\.)?)?"
    r"(?:Test|ParameterizedTest|RepeatedTest|TestFactory|TestTemplate)\b"
    r"|\bextends\s+(?:spock\.lang\.)?Specification\b")
ABSTRACT_RE = re.compile(r"\babstract\s+class\b")
# Failsafe standart naqshi: IT*, *IT, *ITCase.
IT_NAME_RE = re.compile(r"^(?:IT\w+|\w+IT|\w+ITCase)$")
TEST_SUFFIXES = ("Test", "Tests", "IT", "ITCase", "Spec", "TestCase")
SPRING_TEST_RE = re.compile(
    r"@(?:SpringBootTest|WebMvcTest|WebFluxTest|DataJpaTest|DataJdbcTest"
    r"|DataR2dbcTest|JdbcTest|JooqTest|JsonTest|RestClientTest|DataMongoTest"
    r"|DataRedisTest|GraphQlTest|SpringJUnitConfig|SpringJUnitWebConfig"
    r"|ContextConfiguration)\b")
DB_TEST_RE = re.compile(
    r"@(?:DataJpaTest|DataJdbcTest|DataR2dbcTest|JdbcTest|JooqTest"
    r"|SpringBootTest|Sql|Container|Testcontainers|AutoConfigureTestDatabase)\b")
CONFIG_RE = re.compile(
    r"(?:^|/)src/main/resources/(?:(?:config/)?(?:application|bootstrap)"
    r"[\w.-]*\.(?:ya?ml|properties)|META-INF/spring\.factories"
    r"|META-INF/spring/[\w.-]+\.imports)$")
# Spring kontekstini butunlay o'zgartiradigan sinf: u hech qaysi testda nomi
# bilan uchramaydi, lekin component scan orqali har Spring testiga kiradi.
# Masalan SecurityConfig o'zgarsa barcha @WebMvcTest ta'sirlanadi.
WIRING_RE = re.compile(
    r"@(?:Configuration|AutoConfiguration|ControllerAdvice|RestControllerAdvice"
    r"|Aspect|EnableWebSecurity|EnableMethodSecurity|EnableJpaRepositories"
    r"|EnableScheduling|EnableAsync|EnableCaching|ConfigurationProperties"
    r"|SpringBootApplication|ComponentScan)\b"
    r"|\bimplements\s+[^{]*\b(?:Filter|WebMvcConfigurer|WebFluxConfigurer"
    r"|HandlerInterceptor|BeanPostProcessor|BeanFactoryPostProcessor"
    r"|AuthenticationProvider|UserDetailsService)\b"
    r"|\bextends\s+(?:OncePerRequestFilter|GenericFilterBean)\b")
# Entity sxemani belgilaydi: ddl-auto=validate va repository so'rovlari
# orqali baza testlariga ta'sir qiladi, nomi bilan uchramasa ham.
ENTITY_RE = re.compile(r"@(?:Entity|Embeddable|MappedSuperclass)\b")
EXTENDS_RE = re.compile(r"\bclass\s+\w+(?:<[^>]*>)?\s+extends\s+(\w+)")
MIGRATION_RE = re.compile(
    r"(?:^|/)src/main/resources/(?:db/|.*(?:migration|changelog|liquibase|flyway))"
    r".*\.(?:sql|xml|ya?ml|json)$")
BUILD_FILE_RE = re.compile(
    r"(?:^|/)(?:build\.gradle(?:\.kts)?|pom\.xml)$")
ROOT_BUILD_RE = re.compile(
    r"^(?:settings\.gradle(?:\.kts)?|gradle\.properties|gradle/[^/]+\.toml"
    r"|gradle/wrapper/.*|\.mvn/.*|buildSrc/.*|build-logic/.*)$")

# Kataloglar faqat `src/` dan TASHQARIDA tashlanadi: `src/main/java/x/bin`
# paketi build chiqishi emas.
OUTPUT_DIRS = {".git", ".gradle", "build", "target", "out", "bin",
               "node_modules", ".idea", ".vscode", ".mvn"}

# Bitta (modul, to'plam) da shundan ko'p sinf tanlansa, filtr o'rniga
# butun vazifa yuradi: uzun filtr ham, butun vazifa ham bir xil ishlaydi,
# lekin filtr buyruq satrini cheksiz cho'zadi.
MAX_CLASSES = 60
# Bitta nom shuncha testda uchrasa, bu umumiy sinf: uning testlari
# alohida emas, modul bo'yicha olinadi.
WIDE = 40
# Bir qadam narida shundan ko'p bog'liq sinf bo'lsa qadam tashlanadi:
# bevosita testlar qoladi, qolganini to'liq suite tutadi.
MAX_DEPENDENTS = 25
# Bash asbobining eng uzun vaqti 600 s. Asbob undan oldin to'xtab,
# o'zi aytishi kerak: aks holda Bash uni jim o'ldiradi va aktyor yana
# yurgizadi.
DEFAULT_TIMEOUT = 580
MAX_SHOWN = 12
# Yiqilgan sinflar shundan ko'p bo'lsa qayta yurgizilmaydi: bu flaky emas,
# keng buzilish, qayta yurish faqat vaqt oladi.
MAX_RERUN = 30
STATE_DIR = (os.environ.get("GENIUS_STATE_DIR")
             or os.path.join(os.path.dirname(HERE), ".claude", ".state"))
JOURNAL = os.path.join(STATE_DIR, "run_tests.jsonl")
STARTED_RE = re.compile(r"\bStarted (\S+) in ([\d.]+) seconds\b")

REASONS = OrderedDict((
    ("test", "o'zgargan test"),
    ("name", "nomi mos"),
    ("ref", "murojaat"),
    ("hop", "bir qadam"),
    ("config", "sozlama"),
    ("migration", "migratsiya"),
    ("resource", "test resursi"),
    ("helper", "test yordamchisi"),
    ("wiring", "Spring sozlamasi"),
    ("entity", "entity"),
))


def rel(path):
    return path.replace("\\", "/")


def relative_to(path, root):
    """Ildizga nisbatan yo'l, ikkalasi ham realpath dan o'tib.

    Windows da temp va uy papkasi qisqa 8.3 nom bilan kelishi mumkin
    (`RUNNER~1`), git esa ildizni uzun nom bilan beradi; POSIX da esa
    symlink orqali berilgan yo'l. realpath siz relpath `../..` bilan
    boshqa daraxtga chiqib, fayl modulsiz qolardi.
    """
    full = os.path.realpath(os.path.abspath(path))
    return rel(os.path.relpath(full, os.path.realpath(root)))


def run_git(root, *args):
    """git chiqishi yoki None. Kodirovka aniq: Windows da sukut cp1252
    non-ASCII yo'lni buzar yoki UnicodeDecodeError berardi;
    surrogateescape UTF-8 bo'lmagan nomni ham yo'qotmaydi."""
    try:
        out = subprocess.run(["git", "-C", root] + list(args),
                             capture_output=True, text=True, encoding="utf-8",
                             errors="surrogateescape", timeout=60)
    except (OSError, subprocess.SubprocessError):
        return None
    return out.stdout if out.returncode == 0 else None


def project_root(start):
    """Git ildizi yoki build fayli bor eng yaqin yuqori papka."""
    top = run_git(start, "rev-parse", "--show-toplevel")
    if top and top.strip():
        return os.path.realpath(os.path.normpath(top.strip()))
    # Yuqoriga realpath dan yuriladi: symlink yoki Windows qisqa nomi
    # orqali kirilganda ham ildiz (demak log_path kaliti) bitta bo'lsin.
    path = os.path.realpath(os.path.abspath(start))
    while True:
        if any(os.path.exists(os.path.join(path, n)) for n in
               ("settings.gradle", "settings.gradle.kts", "pom.xml",
                "build.gradle", "build.gradle.kts")):
            return os.path.realpath(path)
        parent = os.path.dirname(path)
        if parent == path:
            return os.path.realpath(os.path.abspath(start))
        path = parent


class Source:
    """Bitta Java/Kotlin/Groovy manba fayli."""

    __slots__ = ("rel", "abs", "module", "sset", "name", "fqn", "_text")

    def __init__(self, root, relpath, module, sset, dotted):
        self.rel = relpath
        self.abs = os.path.join(root, relpath)
        self.module = module
        self.sset = sset
        self.fqn = dotted.replace("/", ".")
        self.name = self.fqn.rsplit(".", 1)[-1]
        self._text = None

    @property
    def text(self):
        if self._text is None:
            try:
                with open(self.abs, encoding="utf-8", errors="replace") as handle:
                    self._text = handle.read()
            except OSError:
                self._text = ""
        return self._text

    @property
    def is_main(self):
        return self.sset == "main"

    @property
    def runnable(self):
        """Test to'plamida, abstrakt emas va test usuli bor."""
        return (not self.is_main and not self.sset.lower().endswith("fixtures")
                and bool(TEST_MARK_RE.search(self.text))
                and not ABSTRACT_RE.search(self.text))


def parse_settings(text):
    """settings.gradle dan {loyiha yo'li: papka}. Kotlin va Groovy DSL."""
    text = re.sub(r"//[^\n]*|/\*.*?\*/", "", text, flags=re.S)
    projects = OrderedDict()
    for match in re.finditer(r"\binclude\b\s*\(?", text):
        rest = text[match.end():]
        # Qavs bo'lsa yopilguncha, bo'lmasa vergul bilan davom etgan qatorlar.
        if text[match.end() - 1] == "(":
            body = rest.split(")", 1)[0]
        else:
            lines, body = rest.split("\n"), ""
            for line in lines:
                body += line + "\n"
                if not line.rstrip().endswith(","):
                    break
        for name in re.findall(r"['\"]([^'\"]+)['\"]", body):
            path = ":" + name.strip(":")
            projects[path] = path.strip(":").replace(":", "/")
    for match in re.finditer(
            r"project\(\s*['\"]([^'\"]+)['\"]\s*\)\s*\.projectDir\s*=\s*"
            r"(?:file|new\s+File)\(\s*(?:rootDir\s*,\s*|settingsDir\s*,\s*)?['\"]([^'\"]+)['\"]",
            text):
        path = ":" + match.group(1).strip(":")
        projects[path] = match.group(2).strip("./").rstrip("/")
    return projects


class Project:
    def __init__(self, root, runner=None):
        self.root = os.path.abspath(root)
        self.tool = self._tool()
        self.runner = runner or self._runner()
        self.gradle_projects = OrderedDict()     # papka -> ":a:b"
        self.maven_modules = set()
        if self.tool == "gradle":
            for name in ("settings.gradle.kts", "settings.gradle"):
                path = os.path.join(self.root, name)
                if os.path.exists(path):
                    with open(path, encoding="utf-8", errors="replace") as handle:
                        for gpath, folder in parse_settings(handle.read()).items():
                            self.gradle_projects[folder] = gpath
                    break
        self.sources = []
        self.by_rel = {}
        self.build_files = []
        self._index()

    # -- loyiha turi -------------------------------------------------------

    def _tool(self):
        has = lambda n: os.path.exists(os.path.join(self.root, n))
        if any(has(n) for n in ("gradlew", "gradlew.bat", "settings.gradle",
                                "settings.gradle.kts", "build.gradle",
                                "build.gradle.kts")):
            return "gradle"
        if any(has(n) for n in ("mvnw", "mvnw.cmd", "pom.xml")):
            return "maven"
        return None

    def _runner(self):
        """Buyruq boshi. Wrapper bo'lsa u, bo'lmasa PATH dagi asbob.

        GENIUS_TEST_RUNNER faqat testlar uchun: JSON ro'yxat.
        """
        override = os.environ.get("GENIUS_TEST_RUNNER")
        if override:
            return json.loads(override)
        if self.tool is None:
            return []
        wrapper, fallback = (("gradlew", "gradle") if self.tool == "gradle"
                             else ("mvnw", "mvn"))
        if os.name == "nt":
            script = wrapper + (".bat" if self.tool == "gradle" else ".cmd")
            if os.path.exists(os.path.join(self.root, script)):
                return ["cmd", "/c", script]
            return ["cmd", "/c", fallback]
        path = os.path.join(self.root, wrapper)
        if os.path.exists(path):
            return ["./" + wrapper] if os.access(path, os.X_OK) else ["sh", wrapper]
        return [fallback]

    # -- indeks --------------------------------------------------------------

    def _index(self):
        for current, dirs, files in os.walk(self.root):
            relative = rel(os.path.relpath(current, self.root))
            relative = "" if relative == "." else relative
            inside_src = "/src/" in "/" + relative + "/"
            dirs[:] = [d for d in dirs
                       if d != ".git" and (inside_src or d not in OUTPUT_DIRS)]
            for name in files:
                path = (relative + "/" + name).lstrip("/")
                if name == "pom.xml" and self.tool == "maven":
                    self.maven_modules.add(relative)
                if BUILD_FILE_RE.search(path):
                    self.build_files.append(path)
                match = SOURCE_RE.search(path)
                if not match:
                    continue
                src = Source(self.root, path, self.module_of(path),
                             match.group(1), match.group(2))
                self.sources.append(src)
                self.by_rel[path] = src

    def module_of(self, path):
        """Fayl qaysi modulga tegishli: '' ildiz modul."""
        path = rel(path)
        if self.tool == "gradle" and self.gradle_projects:
            best = ""
            for folder in self.gradle_projects:
                if folder and (path == folder or path.startswith(folder + "/")) \
                        and len(folder) > len(best):
                    best = folder
            return best
        # Maven va settings siz Gradle: eng yaqin build fayli bor papka.
        names = (("pom.xml",) if self.tool == "maven"
                 else ("build.gradle", "build.gradle.kts"))
        parts = path.split("/")[:-1]
        while parts:
            folder = "/".join(parts)
            if any(os.path.exists(os.path.join(self.root, folder, n)) for n in names):
                return folder
            parts.pop()
        return ""

    def gradle_path(self, module):
        if not module:
            return ""
        return self.gradle_projects.get(module) or ":" + module.replace("/", ":")

    def tests(self):
        return [s for s in self.sources if s.runnable]

    def pom_texts(self):
        texts = []
        for path in self.build_files:
            if path.endswith("pom.xml"):
                with contextlib.suppress(OSError):
                    with open(os.path.join(self.root, path), encoding="utf-8",
                              errors="replace") as handle:
                        texts.append(handle.read())
        return texts

    def failsafe(self):
        return any("maven-failsafe-plugin" in t for t in self.pom_texts())


# -- o'zgarishlar ------------------------------------------------------------

def is_output(path):
    """Build chiqishi: `src/` dan oldingi qismida OUTPUT_DIRS bor yo'l."""
    full = "/" + path
    parts = full.split("/src/", 1)[0].split("/")
    if "/src/" not in full:
        parts = parts[:-1]          # fayl nomining o'zi papka emas
    return any(part in OUTPUT_DIRS for part in parts)


def name_status(output):
    """`diff --name-status -z` chiqishi: (status, [yo'l]) juftlari.

    NUL bo'yicha: status tokeni, keyin R va C uchun 2 yo'l (eski, yangi),
    qolganlariga 1 yo'l. -z siz git non-ASCII nomni qo'shtirnoq va oktal
    bilan berardi va fayl os.path.exists filtrida jim tushib qolardi.
    """
    tokens = (output or "").split("\0")
    pairs, i = [], 0
    while i < len(tokens):
        status = tokens[i]
        if not status:
            i += 1
            continue
        count = 2 if status[:1] in ("R", "C") else 1
        paths = [p for p in tokens[i + 1:i + 1 + count] if p]
        i += 1 + count
        if paths:
            pairs.append((status, paths))
    return pairs


def git_changes(root, base, relative):
    """([(status, yo'llar)], [untracked]): base...HEAD, HEAD va yangi fayllar.

    relative=True: faqat ildiz ichi, yo'l ildizga nisbatan. False: butun
    repo, yo'l git ildiziga nisbatan.
    """
    scope = ["--relative"] if relative else []
    pairs = []
    for spec in (["%s...HEAD" % base] if base else []) + ["HEAD"]:
        pairs += name_status(run_git(root, "diff", "--name-status", "-z", *(scope + [spec])))
    untracked = run_git(root, "ls-files", "-z", "--others", "--exclude-standard",
                        *([] if relative else ["--full-name", ":/"]))
    return pairs, [p for p in (untracked or "").split("\0") if p]


def outside_root(root, base=None):
    """Diffdagi, lekin --ildiz dan tashqaridagi fayllar soni.

    Build ildizi git ildizidan pastda bo'lsa (monorepo, `--ildiz backend`)
    `--relative` faqat ildiz ichini beradi; qolgani shu yerda sanaladi.
    Ildiz git ildizining o'zi bo'lsa tashqari yo'q, diff qayta olinmaydi.
    """
    prefix = (run_git(root, "rev-parse", "--show-prefix") or "").strip()
    if not prefix:
        return 0
    pairs, untracked = git_changes(root, base, relative=False)
    paths = {p for _, items in pairs for p in items} | set(untracked)
    return sum(1 for p in paths if not p.startswith(prefix))


def changed_files(root, base=None):
    """(bor fayllar, o'chirilganlar), ildizga nisbatan.

    `--relative`: build ildizi git ildizidan pastda bo'lsa ham yo'l ildizga
    nisbatan keladi. Busiz `backend/...` yo'li ildizga ulanib yo'q fayl
    bo'lardi va o'zgarish "yo'q" deb rc 0 qaytardi. `base` verify_base dan
    o'tgan commit: git ga bayroq bo'lib o'tolmaydi.
    """
    existing, deleted = [], []
    pairs, untracked = git_changes(root, base, relative=True)
    for status, paths in pairs:
        if status.startswith("D"):
            deleted.append(rel(paths[-1]))
        elif status.startswith("R"):
            deleted.append(rel(paths[0]))
            existing.append(rel(paths[-1]))
        else:
            existing.append(rel(paths[-1]))
    existing += [rel(p) for p in untracked]
    keep = lambda items: list(OrderedDict.fromkeys(
        p for p in items if not is_output(p)))
    existing = keep(p for p in existing if os.path.exists(os.path.join(root, p)))
    deleted = keep(p for p in deleted if p not in existing)
    return existing, deleted


def verify_base(root, base):
    """--asos ni commit hash iga aylantiradi, bo'lmasa None.

    `-` bilan boshlangan qiymat git ga bayroq bo'lib o'tardi
    (`--asos=--output=<fayl>` fayl yaratardi), shuning uchun rad etiladi.
    `--end-of-options` qolganini ham faqat ref deb o'qitadi (git 2.24+).
    """
    if not base or base.startswith("-"):
        return None
    out = run_git(root, "rev-parse", "--verify", "--quiet", "--end-of-options",
                  "%s^{commit}" % base)
    return out.strip() if out and out.strip() else None


def inside(path, folder):
    """`path` realpath bo'yicha `folder` ichidami (Windows da registrsiz)."""
    full = os.path.normcase(os.path.realpath(os.path.abspath(path)))
    top = os.path.normcase(os.path.realpath(folder))
    try:
        return os.path.commonpath([full, top]) == top
    except ValueError:          # Windows: boshqa disk
        return False


# -- tanlash -------------------------------------------------------------------

class Plan:
    def __init__(self):
        # (modul, to'plam) -> {fqn: sabab}
        self.targets = OrderedDict()
        # (modul, to'plam) -> sabab: filtrsiz butun vazifa
        self.whole = OrderedDict()
        self.everything = None       # sabab: butun suite
        self.notes = []
        self.counts = OrderedDict((k, 0) for k in REASONS)

    def add(self, src, kind, detail=""):
        key = (src.module, src.sset)
        if key in self.whole:
            return
        bucket = self.targets.setdefault(key, OrderedDict())
        if src.fqn not in bucket:
            bucket[src.fqn] = (kind, detail)
            self.counts[kind] += 1

    def add_whole(self, module, sset, reason):
        self.targets.pop((module, sset), None)
        self.whole.setdefault((module, sset), reason)

    def empty(self):
        return not (self.targets or self.whole or self.everything)

    def size(self):
        return sum(len(v) for v in self.targets.values())


def ancestors(src, by_name, depth=5):
    """Shu test va uning test to'plamidagi ota sinflari matni."""
    seen, current = [src], src
    for _ in range(depth):
        parent = EXTENDS_RE.search(current.text)
        bases = by_name.get(parent.group(1), ()) if parent else ()
        if not bases:
            break
        current = bases[0]
        seen.append(current)
    return seen


def matches_up(src, by_name, pattern):
    """Test o'zi yoki abstrakt ota sinfi naqshga mos: `class X extends
    AbstractIT` dagi @SpringBootTest AbstractIT da turadi."""
    return any(pattern.search(s.text) for s in ancestors(src, by_name))


def word_re(names):
    names = sorted(set(names), key=len, reverse=True)
    return re.compile(r"\b(%s)\b" % "|".join(re.escape(n) for n in names))


def name_matches(name):
    return {name + s for s in TEST_SUFFIXES} | {"Test" + name}


def select(project, existing, deleted=()):
    plan = Plan()
    tests = project.tests()
    by_name = {}
    for test in tests:
        by_name.setdefault(test.name, []).append(test)
    # Ota sinflar uchun: abstrakt bazaviy sinf runnable emas, lekin
    # @SpringBootTest aynan unda turadi.
    test_sources = {}
    for src in project.sources:
        if not src.is_main:
            test_sources.setdefault(src.name, []).append(src)

    def spring_tests(module):
        return [t for t in tests if t.module == module
                and matches_up(t, test_sources, SPRING_TEST_RE)]

    def db_tests(module):
        return [t for t in tests if t.module == module
                and matches_up(t, test_sources, DB_TEST_RE)]

    main_names, helper_names, ignored = OrderedDict(), OrderedDict(), []
    for path in existing:
        src = project.by_rel.get(path)
        if src is not None:
            if src.is_main:
                main_names[src.name] = src
            elif src.runnable:
                plan.add(src, "test")
            else:
                helper_names[src.name] = src
            continue
        module = project.module_of(path)
        if ROOT_BUILD_RE.search(path) or (BUILD_FILE_RE.search(path) and module == ""
                                          and "/" not in path):
            plan.everything = "build fayli: %s" % path
        elif BUILD_FILE_RE.search(path):
            for sset in sorted({t.sset for t in tests if t.module == module}):
                plan.add_whole(module, sset, "build fayli: %s" % path)
        elif CONFIG_RE.search(path):
            for test in spring_tests(module):
                plan.add(test, "config", os.path.basename(path))
        elif MIGRATION_RE.search(path):
            for test in db_tests(module):
                plan.add(test, "migration", os.path.basename(path))
        elif re.search(r"(?:^|/)src/(?!main/)[^/]+/resources/", path):
            base = os.path.basename(path)
            hits = [t for t in tests if t.module == module and base in t.text]
            for test in hits:
                plan.add(test, "resource", base)
            if not hits:
                sset = path.split("/src/", 1)[-1].split("/", 1)[0] if "/src/" in "/" + path \
                    else "test"
                plan.add_whole(module, sset, "test resursi: %s" % base)
        else:
            ignored.append(path)
    for path in deleted:
        match = SOURCE_RE.search(path)
        if match:
            name = match.group(2).rsplit("/", 1)[-1]
            (main_names if match.group(1) == "main" else helper_names)[name] = None

    if plan.everything:
        return plan

    # 1b. Kontekstni o'zgartiradigan sinf va entity: nomi bilan emas, Spring
    # orqali ta'sir qiladi. Modulda Spring testi bo'lmasa (kutubxona modul),
    # uning sozlamasi ishlatuvchi modullarda kuchga kiradi: hamma modul.
    for name, src in main_names.items():
        if src is None:
            continue
        for regex, kind, pick in ((WIRING_RE, "wiring", spring_tests),
                                  (ENTITY_RE, "entity", db_tests)):
            if not regex.search(src.text):
                continue
            found = pick(src.module)
            if not found:
                found = [t for m in sorted({t.module for t in tests}) for t in pick(m)]
            for test in found:
                plan.add(test, kind, name)

    # 2. Nomi mos test.
    for name in main_names:
        for candidate in name_matches(name):
            for test in by_name.get(candidate, ()):
                plan.add(test, "name", name)

    # 3. Murojaat. Juda ko'p testda uchragan nom umumiy sinf: modul bo'yicha.
    def references(names, kind, via=None):
        if not names:
            return
        pattern = word_re(names)
        hits = OrderedDict((n, []) for n in names)
        for test in tests:
            for found in set(pattern.findall(test.text)):
                hits[found].append(test)
        for name, found in hits.items():
            if len(found) > WIDE:
                for module, sset in sorted({(t.module, t.sset) for t in found}):
                    plan.add_whole(module, sset, "keng ta'sir: %s %d testda" % (name, len(found)))
                continue
            for test in found:
                plan.add(test, kind, via.get(name, name) if via else name)

    references(list(main_names), "ref")
    references(list(helper_names), "helper")

    # 4. Bir qadam: o'zgargan sinfni ishlatgan asosiy kod sinflari.
    if main_names:
        pattern = word_re(main_names)
        changed = {src.rel for src in main_names.values() if src is not None}
        dependents = OrderedDict()
        for src in project.sources:
            if src.is_main and src.rel not in changed and src.name not in main_names:
                found = pattern.search(src.text)
                if found:
                    dependents[src.name] = found.group(1)
        if len(dependents) > MAX_DEPENDENTS:
            plan.notes.append(
                "bir qadam tashlandi: o'zgargan sinflarni %d sinf ishlatadi; "
                "bevosita testlar olindi, qolganini to'liq suite tutadi"
                % len(dependents))
        elif dependents:
            via = {d: "%s orqali %s" % (d, n) for d, n in dependents.items()}
            for name in dependents:
                for candidate in name_matches(name):
                    for test in by_name.get(candidate, ()):
                        plan.add(test, "hop", via[name])
            references(list(dependents), "hop", via)

    # 5. Juda ko'p sinf: filtr o'rniga butun vazifa.
    totals = {}
    for test in tests:
        totals[(test.module, test.sset)] = totals.get((test.module, test.sset), 0) + 1
    for key, chosen in list(plan.targets.items()):
        if len(chosen) > MAX_CLASSES or (len(chosen) > 10 and len(chosen) * 2 > totals.get(key, 0)):
            plan.add_whole(key[0], key[1], "%d sinf tanlandi, %d dan" % (len(chosen), totals.get(key, 0)))

    if ignored:
        plan.notes.append("testga ta'sir qilmaydi deb olindi: %s%s"
                          % (", ".join(ignored[:3]), " (+%d)" % (len(ignored) - 3)
                             if len(ignored) > 3 else ""))
    return plan


# -- buyruqlar ----------------------------------------------------------------

SENTINEL = "GeniusUnitTestYoq"


def extra_flags():
    """GENIUS_TEST_FLAGS: foydalanuvchi o'zi tanlagan qo'shimcha bayroqlar
    (`--build-cache --parallel`, `-o -T 1C`). Build ga tegmasdan yoqiladi,
    lekin ularning to'g'riligi build ning o'ziga bog'liq: shuning uchun
    standart bo'sh."""
    return shlex.split(os.environ.get("GENIUS_TEST_FLAGS", ""))


def gradle_task(sset):
    return "test" if sset == "test" else sset


# Gradle da `-Djacoco.skip` yo'q: jacoco plagin, agent va hisobot vazifasi
# build faylida. Init skript faqat shu yurishga qo'shiladi, build fayllariga
# tegmaydi. projectsEvaluated: plaginlar va build skriptining o'z sozlamasidan
# keyin ishlaydi. Gradle 7.6, 8.14, 9.8 da tekshirilgan (DECISIONS.md).
GRADLE_INIT = r"""// claude-genius run_tests.py: faqat shu yurish uchun, build fayllariga tegmaydi.
import org.gradle.util.GradleVersion

def geniusMaqsadli = %(maqsadli)s
def geniusKesh = %(kesh)s

if (GradleVersion.current() < GradleVersion.version('6.1')) {
    return
}

if (geniusKesh) {
    // Keshni asbob yoqdi: faqat lokal, loyihaning remote keshiga tegilmaydi.
    settingsEvaluated { settings ->
        def remote = settings.buildCache.remote
        if (remote != null) {
            remote.enabled = false
        }
    }
}

projectsEvaluated { gradle ->
    gradle.rootProject.allprojects { project ->
        project.tasks.withType(Test).configureEach { task ->
            task.reports.junitXml.required.set(true)
            if (geniusMaqsadli) {
                task.reports.html.required.set(false)
                def jacoco = task.extensions.findByName('jacoco')
                if (jacoco != null) {
                    jacoco.enabled = false
                }
            }
        }
        if (geniusMaqsadli) {
            project.tasks.withType(org.gradle.testing.jacoco.tasks.JacocoReportBase).configureEach { task ->
                task.enabled = false
            }
        }
        if (geniusKesh) {
            project.tasks.configureEach { task ->
                def kompilyatsiya = task instanceof org.gradle.api.tasks.compile.AbstractCompile ||
                    task.class.name.startsWith('org.jetbrains.kotlin.gradle.tasks.KotlinCompile')
                if (!kompilyatsiya) {
                    task.outputs.doNotCacheIf('claude-genius: faqat kompilyatsiya keshlanadi',
                        org.gradle.api.specs.Specs.SATISFIES_ALL)
                }
            }
        }
    }
}
"""


def gradle_props(root):
    """gradle.properties: loyiha, keyin GRADLE_USER_HOME. Gradle ham shu
    tartibda o'qiydi, foydalanuvchi faylidagi qiymat ustun."""
    home = os.environ.get("GRADLE_USER_HOME") or os.path.join(os.path.expanduser("~"), ".gradle")
    props = properties(read(os.path.join(root, "gradle.properties")))
    props.update(properties(read(os.path.join(home, "gradle.properties"))))
    return props


def gradle_version(root):
    text = read(os.path.join(root, "gradle", "wrapper", "gradle-wrapper.properties"))
    match = re.search(r"gradle-(\d+)\.(\d+)", text)
    return (int(match.group(1)), int(match.group(2))) if match else None


def gradle_cache_ours(root, flags):
    """Kompilyatsiya keshini asbob yoqadimi. Loyiha yoki foydalanuvchi
    keshni o'zi tanlagan bo'lsa (yoqilgan ham, o'chirilgan ham) uning
    qarori qoladi va asbob unga tegmaydi."""
    if "--build-cache" in flags or "--no-build-cache" in flags:
        return False
    return gradle_props(root).get("org.gradle.caching", "").lower() not in ("true", "false")


def init_script(targeted, cache):
    text = GRADLE_INIT % {"maqsadli": "true" if targeted else "false",
                          "kesh": "true" if cache else "false"}
    path = os.path.join(tempfile.gettempdir(), "genius-gradle-%s.gradle"
                        % hashlib.sha1(text.encode("utf-8")).hexdigest()[:10])
    if read(path) != text:
        tmp = "%s.%d.tmp" % (path, os.getpid())
        with open(tmp, "w", encoding="utf-8") as handle:
            handle.write(text)
        try:
            os.replace(tmp, path)
        except OSError:
            # Windows: parallel yurishning Gradle i faylni o'qiyotgan bo'lsa
            # almashtirib bo'lmaydi; nomi mazmundan, demak u allaqachon to'g'ri.
            with contextlib.suppress(OSError):
                os.remove(tmp)
            if read(path) != text:
                raise
    return path


def gradle_init(project, targeted):
    """Gradle yurishiga init skript va kesh bayrog'i.

    Maqsadli yurishda (targeted): jacoco agenti va jacoco hisobot,
    coverage tekshiruvi vazifalari o'chadi, HTML hisobot yozilmaydi.
    `test` ga finalizedBy bilan bog'langan coverage tekshiruvi bir nechta
    test bilan chegaraga yetmay yolg'on yiqilardi: Maven dagi jacoco:check
    bilan bir xil. To'liq suite da jacoco qoladi, coverage CI bilan bir xil.

    Har yurishda: JUnit XML majburiy (qayta yurish va beqarorni ajratish
    shunga tayanadi). Kesh asbobniki bo'lsa: faqat kompilyatsiya, faqat
    lokal. Yangi worktree boshqa daraxt kompilyatsiya qilgan modulni keshdan
    oladi. Test natijasi keshlanmaydi: test har gal haqiqatan yuradi.

    O'chirish: GENIUS_GRADLE_INIT=0; faqat kesh: org.gradle.caching=false
    yoki GENIUS_TEST_FLAGS=--no-build-cache.
    """
    if os.environ.get("GENIUS_GRADLE_INIT", "").strip() == "0":
        return []
    version = gradle_version(project.root)
    if version and version < (6, 1):
        return []
    cache = gradle_cache_ours(project.root, extra_flags())
    return ["-I", init_script(targeted, cache)] + (["--build-cache"] if cache else [])


def commands(project, plan, everything=False):
    """[(argv, izoh)]: ketma-ket yurgiziladigan buyruqlar."""
    if project.tool == "gradle":
        return gradle_commands(project, plan, everything)
    if project.tool == "maven":
        return maven_commands(project, plan, everything)
    return []


def gradle_commands(project, plan, everything):
    argv = list(project.runner)
    if everything or plan.everything:
        tasks = ["test"] + sorted({gradle_task(s.sset) for s in project.tests()} - {"test"})
        return [(argv + tasks + ["--continue", "--console=plain"]
                 + gradle_init(project, False) + extra_flags(), "to'liq suite")]
    for (module, sset), reason in plan.whole.items():
        argv.append("%s:%s" % (project.gradle_path(module), gradle_task(sset)))
    for (module, sset), chosen in plan.targets.items():
        argv.append("%s:%s" % (project.gradle_path(module), gradle_task(sset)))
        for fqn in chosen:
            argv += ["--tests", fqn]
    return [(argv + ["--continue", "--console=plain"] + gradle_init(project, True)
             + extra_flags(), "maqsadli")]


def maven_commands(project, plan, everything):
    base = list(project.runner) + ["-B", "-fae"]
    # Maqsadli yurishda jacoco yo'q: agent testni sekinlashtiradi, verify ga
    # bog'langan jacoco:check esa bir nechta test bilan coverage chegarasiga
    # yetmay yolg'on yiqiladi. Coverage to'liq suite va CI niki.
    quick = ["-Djacoco.skip=true"]
    pre = []
    poms = project.pom_texts()
    failsafe = project.failsafe()
    if any("spring-javaformat-maven-plugin" in t for t in poms):
        # validate fazasidagi spring-javaformat:validate har Maven test
        # yurishini, maqsadlisini ham yiqitadi. apply faqat bo'sh joyni
        # o'zgartiradi va yiqilgan yurishdan arzon.
        pre.append((list(project.runner) + ["-B", "-q", "spring-javaformat:apply"],
                    "formatlash: spring-javaformat validate fazasida tekshiradi"))
    if everything or plan.everything:
        phase = "verify" if failsafe else "test"
        if phase == "verify" and any("spotless-maven-plugin" in t for t in poms):
            pre.append((list(project.runner) + ["-B", "-q", "spotless:apply"],
                        "formatlash: spotless:check verify fazasida"))
        return pre + [(base + [phase] + extra_flags(), "to'liq suite")]

    def module_args(modules):
        modules = sorted(m or "." for m in modules)
        return [] if modules == ["."] else ["-pl", ",".join(modules), "-am"]

    out = list(pre)
    if plan.whole:
        out.append((base + module_args({m for m, _ in plan.whole}) + ["test"]
                    + quick + extra_flags(),
                    "butun modul: " + "; ".join(plan.whole.values())))
    units, its = [], []
    for (module, sset), chosen in plan.targets.items():
        for fqn in chosen:
            simple = fqn.rsplit(".", 1)[-1]
            (its if failsafe and IT_NAME_RE.match(simple) else units).append(fqn)
    if units or its:
        modules = {m for m, _ in plan.targets}
        props = ["-Dtest=%s" % ",".join(units or [SENTINEL]),
                 "-Dsurefire.failIfNoSpecifiedTests=false"]
        phase = "test"
        if its:
            phase = "verify"
            props += ["-Dit.test=%s" % ",".join(its),
                      "-Dfailsafe.failIfNoSpecifiedTests=false",
                      "-Dit.failIfNoSpecifiedTests=false",
                      # verify package ni ham quradi: javadoc va source jar
                      # test natijasiga ta'sir qilmaydi, faqat vaqt oladi.
                      "-Dmaven.javadoc.skip=true", "-Dmaven.source.skip=true"]
            if any("spotless-maven-plugin" in t for t in poms):
                out.insert(len(pre), (list(project.runner) + ["-B", "-q", "spotless:apply"],
                                      "formatlash: spotless:check verify fazasida"))
        out.append((base + module_args(modules) + [phase] + props + quick
                    + extra_flags(), "maqsadli"))
    return out


def warmup_commands(project):
    """Fonda kompilyatsiya: guruh ochilgach aktyor kod o'qiyotgan paytda
    yangi worktree ning birinchi to'liq kompilyatsiyasi tugaydi."""
    if project.tool == "gradle":
        tasks = sorted({gradle_task(s.sset) + "Classes" for s in project.tests()}
                       | {"testClasses"})
        return [(list(project.runner) + tasks + ["--console=plain", "-q"]
                 + gradle_init(project, False) + extra_flags(), "isitish")]
    return [(list(project.runner) + ["-B", "-q", "test-compile", "-Djacoco.skip=true",
                                     "-Dspring-javaformat.validate.skip=true"]
             + extra_flags(), "isitish")]


def show(argv):
    return " ".join(shlex.quote(a) if re.search(r"[^\w@%+=:,./-]", a) else a
                    for a in argv)


# -- yurgizish -----------------------------------------------------------------

def state_key(root):
    common = run_git(root, "rev-parse", "--git-common-dir")
    base = os.path.abspath(os.path.join(root, common.strip())) if common else root
    return hashlib.sha1(base.encode("utf-8")).hexdigest()[:10]


@contextlib.contextmanager
def queue_lock(root):
    """Bir repo ning barcha worktree lari uchun bitta navbat.

    Testlar qat'iy port yoki lokal baza ishlatsa, parallel guruhlarning
    test yurishi bir-birini buzadi: --navbat ularni ketma-ket qiladi.
    Qulf jarayon o'lganda OS tomonidan yechiladi.
    """
    path = os.path.join(tempfile.gettempdir(), "genius-test-%s.lock" % state_key(root))
    handle = open(path, "a+")
    try:
        if os.name == "nt":
            import msvcrt
            while True:
                try:
                    msvcrt.locking(handle.fileno(), msvcrt.LK_LOCK, 1)
                    break
                except OSError:
                    time.sleep(1)
        else:
            import fcntl
            fcntl.flock(handle.fileno(), fcntl.LOCK_EX)
        yield
    finally:
        with contextlib.suppress(OSError):
            if os.name == "nt":
                import msvcrt
                msvcrt.locking(handle.fileno(), msvcrt.LK_UNLCK, 1)
        handle.close()


@contextlib.contextmanager
def root_lock(root):
    """Bitta daraxtda bir vaqtda bitta build: fondagi --isit va aktyorning
    --yurgiz i bir-birining build/ papkasiga yozmasin. Keyingisi kutadi."""
    key = hashlib.sha1(os.path.realpath(root).encode("utf-8")).hexdigest()[:10]
    path = os.path.join(tempfile.gettempdir(), "genius-root-%s.lock" % key)
    handle = open(path, "a+")
    try:
        if os.name == "nt":
            import msvcrt
            while True:
                try:
                    msvcrt.locking(handle.fileno(), msvcrt.LK_LOCK, 1)
                    break
                except OSError:
                    time.sleep(1)
        else:
            import fcntl
            fcntl.flock(handle.fileno(), fcntl.LOCK_EX)
        yield
    finally:
        with contextlib.suppress(OSError):
            if os.name == "nt":
                import msvcrt
                msvcrt.locking(handle.fileno(), msvcrt.LK_UNLCK, 1)
        handle.close()


def log_path(root, everything):
    """Bitta loyiha uchun bitta nom: Windows da qisqa (8.3) yo'l va
    harf registri boshqa hash bermasin."""
    key = os.path.normcase(os.path.realpath(root))
    name = "genius-test-%s%s.log" % (hashlib.sha1(key.encode("utf-8")).hexdigest()[:10],
                                     "-hammasi" if everything else "")
    return os.path.join(tempfile.gettempdir(), name)


def execute(project, cmds, log, timeout, queue=False, mode="w"):
    """(exit, soniya). exit 124: vaqt tugadi. Qulf tartibi doim bir xil
    (avval repo, keyin ildiz): teskari tartib o'zaro kutib qolishga olib
    kelardi."""
    start = time.time()
    code = 0
    lock = queue_lock(project.root) if queue else contextlib.nullcontext()
    with lock, root_lock(project.root), \
            open(log, mode, encoding="utf-8", errors="replace") as out:
        for argv, note in cmds:
            out.write("$ %s\n" % show(argv))
            out.flush()
            left = timeout - (time.time() - start)
            if left <= 0:
                return 124, time.time() - start
            try:
                proc = subprocess.run(argv, cwd=project.root, stdout=out,
                                      stderr=subprocess.STDOUT, timeout=left)
            except subprocess.TimeoutExpired:
                out.write("\n[run_tests] vaqt tugadi: %d s\n" % timeout)
                return 124, time.time() - start
            except OSError as exc:
                out.write("\n[run_tests] yurgizib bo'lmadi: %s\n" % exc)
                return 127, time.time() - start
            if proc.returncode and not note.startswith("formatlash"):
                code = code or proc.returncode
            elif proc.returncode:
                out.write("\n[run_tests] formatlash yiqildi, testlar baribir yuradi\n")
    return code, time.time() - start


REPORT_DIR_RE = re.compile(
    r"^(?:(.*)/)?(?:build/test-results/([^/]+)|target/(surefire|failsafe)-reports)$")


def failed_classes(project, since):
    """{(modul, to'plam): [fqn]}: shu yurishda yozilgan JUnit XML dagi
    yiqilgan sinflar. Konsol chiqishi oddiy nomni beradi, XML esa to'liq
    nom va modulni: qayta yurish aynan shu sinflarni oladi."""
    found = OrderedDict()
    for current, dirs, files in os.walk(project.root):
        dirs[:] = [d for d in dirs if d not in (".git", ".gradle", "node_modules", "src")]
        match = REPORT_DIR_RE.match(rel(os.path.relpath(current, project.root)))
        if not match:
            continue
        module = match.group(1) or ""
        sset = match.group(2) or "test"
        for name in files:
            if not (name.startswith("TEST-") and name.endswith(".xml")):
                continue
            path = os.path.join(current, name)
            with contextlib.suppress(OSError, ET.ParseError, ValueError):
                if os.path.getmtime(path) < since:
                    continue
                suite = ET.parse(path).getroot()
                bad = int(suite.get("failures", "0") or 0) + int(suite.get("errors", "0") or 0)
                if bad and suite.get("name"):
                    found.setdefault((module, sset), []).append(suite.get("name"))
    return found


def has_compile_error(log):
    try:
        import parse_test_output as pto
        with open(log, encoding="utf-8", errors="replace") as handle:
            lines = pto.strip_ci_prefix(handle.read().split("\n"))
        return bool(pto.compile_errors(lines))
    except Exception:     # tasnif qo'shimcha: xatosi asosiy natijani buzmasin
        return False


def rerun_plan(failed):
    plan = Plan()
    for (module, sset), names in failed.items():
        bucket = plan.targets.setdefault((module, sset), OrderedDict())
        for fqn in names:
            bucket[fqn] = ("test", "qayta")
    return plan


def record(root, mode, plan, code, seconds, flaky=0):
    """Har yurish jurnalga: tezlashuv taxmin emas, o'lchov bo'lsin."""
    entry = {"ts": int(time.time()), "root": root, "mode": mode,
             "classes": plan.size(), "whole": len(plan.whole), "exit": code,
             "seconds": round(seconds, 1), "flaky": flaky}
    with contextlib.suppress(OSError):
        os.makedirs(STATE_DIR, exist_ok=True)
        with open(JOURNAL, "a", encoding="utf-8") as handle:
            handle.write(json.dumps(entry) + "\n")


def report(days):
    since = time.time() - days * 86400
    rows = []
    with contextlib.suppress(OSError):
        with open(JOURNAL, encoding="utf-8") as handle:
            for line in handle:
                with contextlib.suppress(ValueError):
                    row = json.loads(line)
                    if row.get("ts", 0) >= since:
                        rows.append(row)
    print("Test yurishlari, oxirgi %d kun: %d ta" % (days, len(rows)))
    if not rows:
        return 0
    print("\n%-10s %6s %9s %9s %8s %8s" % ("rejim", "soni", "jami, daq", "median, s",
                                          "yiqildi", "beqaror"))
    for mode in ("maqsadli", "modul", "hammasi", "isitish"):
        part = [r for r in rows if r.get("mode") == mode]
        if not part:
            continue
        times = sorted(r.get("seconds", 0) for r in part)
        print("%-10s %6d %9.1f %9.0f %8d %8d" % (
            mode, len(part), sum(times) / 60, times[len(times) // 2],
            sum(1 for r in part if r.get("exit") not in (0, 4)),
            sum(1 for r in part if r.get("exit") == 4)))
    full = [r for r in rows if r.get("mode") == "hammasi"]
    print("\nTo'liq suite kuniga o'rtacha: %.1f marta. Maqsad: partiyada bir marta."
          % (len(full) / float(days)))
    return 0


def context_starts(paths):
    """Spring Boot har yangi test konteksti uchun `Started X in N seconds`
    yozadi: kesh bo'linishining aniq o'lchovi, kalitni taxmin qilmasdan."""
    for path in paths:
        if not os.path.exists(path):
            continue
        starts = []
        with open(path, encoding="utf-8", errors="replace") as handle:
            for line in handle:
                match = STARTED_RE.search(line)
                if match:
                    starts.append((match.group(1), float(match.group(2))))
        if starts:
            return path, starts
    return None, []


def summarize(log):
    try:
        out = subprocess.run([sys.executable, PARSER, log], capture_output=True,
                             text=True, encoding="utf-8", errors="replace", timeout=120)
    except (OSError, subprocess.SubprocessError) as exc:
        return "xulosa olinmadi: %s" % exc
    return (out.stdout or out.stderr).strip()


# -- chiqish -------------------------------------------------------------------

def describe(project, plan, cmds, everything):
    lines = []
    if everything or plan.everything:
        lines.append("Reja: to'liq suite (%s)" % (plan.everything or "--hammasi"))
    else:
        parts = ["%s %d" % (REASONS[k], v) for k, v in plan.counts.items() if v]
        lines.append("Reja: %d test sinfi, %d vazifa%s%s" % (
            plan.size(), len(plan.targets) + len(plan.whole),
            " (%s)" % ", ".join(parts) if parts else "",
            "; butun vazifa: %d" % len(plan.whole) if plan.whole else ""))
        rows = []
        for (module, sset), reason in plan.whole.items():
            rows.append("  %-22s butun vazifa   %s" % (task_label(project, module, sset), reason))
        for (module, sset), chosen in plan.targets.items():
            for fqn, (kind, detail) in chosen.items():
                rows.append("  %-22s %s   %s%s" % (
                    task_label(project, module, sset), fqn, REASONS[kind],
                    ": " + detail if detail and kind != "test" else ""))
        lines += rows[:MAX_SHOWN]
        if len(rows) > MAX_SHOWN:
            lines.append("  ... yana %d ta" % (len(rows) - MAX_SHOWN))
    for argv, note in cmds:
        lines.append("Buyruq (%s): %s" % (note, show(argv)))
    init = next((read(a[a.index("-I") + 1]) for a, _ in cmds if "-I" in a), "")
    parts = (["jacoco va HTML hisobot o'chiq"] if "geniusMaqsadli = true" in init else []) + \
        (["kesh faqat kompilyatsiya, lokal"] if "geniusKesh = true" in init else [])
    if parts:
        lines.append("Gradle init: %s (GENIUS_GRADLE_INIT=0 o'chiradi)" % ", ".join(parts))
    for note in plan.notes:
        lines.append("Eslatma: %s" % note)
    return "\n".join(lines)


def task_label(project, module, sset):
    if project.tool == "gradle":
        return "%s:%s" % (project.gradle_path(module), gradle_task(sset))
    return "%s (%s)" % (module or ".", sset)


# -- tashxis -------------------------------------------------------------------

def read(path):
    try:
        with open(path, encoding="utf-8", errors="replace") as handle:
            return handle.read()
    except OSError:
        return ""


def properties(text):
    props = {}
    for line in text.splitlines():
        line = line.strip()
        if line and not line.startswith(("#", "!")) and "=" in line:
            key, value = line.split("=", 1)
            props[key.strip()] = value.strip()
    return props


MOCK_RE = re.compile(r"@(?:MockBean|MockitoBean|SpyBean|MockitoSpyBean)\b[^;{]*?\s(\w+(?:<[^>]*>)?)\s+\w+\s*;")
CONTEXT_ANN_RE = re.compile(
    r"@(?:SpringBootTest|WebMvcTest|WebFluxTest|DataJpaTest|DataJdbcTest|JdbcTest"
    r"|JsonTest|RestClientTest|ActiveProfiles|TestPropertySource|Import"
    r"|ContextConfiguration|AutoConfigureMockMvc|AutoConfigureTestDatabase"
    r"|DirtiesContext)\b(?:\([^)]*\))?")
CONTAINER_RE = r"@(?:[\w.]+\.)?Container\b"
CONTAINER_FIELD_RE = re.compile(CONTAINER_RE + r"\s*(?:@[\w.]+(?:\([^)]*\))?\s*)*([^;=\n]*?)\s\w+\s*=")


def context_key(src, by_name, depth=0):
    """Spring kontekst keshi kalitining taxminiy tasviri."""
    text = src.text
    own = sorted(set(re.sub(r"\s+", "", m) for m in CONTEXT_ANN_RE.findall(text)))
    mocks = sorted(set(MOCK_RE.findall(text)))
    parent = EXTENDS_RE.search(text)
    inherited = ()
    if parent and depth < 5:
        for base in by_name.get(parent.group(1), ()):
            inherited = context_key(base, by_name, depth + 1)
            break
    return tuple(own) + tuple("mock:" + m for m in mocks) + tuple(inherited)


def slowest_reports(root):
    """Oxirgi yurishning JUnit XML hisobotlari: (sinf, soniya)."""
    found = []
    for current, dirs, files in os.walk(root):
        dirs[:] = [d for d in dirs if d not in (".git", "node_modules", ".gradle")]
        if not (current.endswith(os.sep + "test-results") or os.sep + "test-results" + os.sep in current + os.sep
                or current.endswith("surefire-reports") or current.endswith("failsafe-reports")):
            continue
        for name in files:
            if name.startswith("TEST-") and name.endswith(".xml"):
                with contextlib.suppress(ET.ParseError, OSError, ValueError):
                    suite = ET.parse(os.path.join(current, name)).getroot()
                    found.append((suite.get("name", name), float(suite.get("time", "0") or 0)))
    return sorted(found, key=lambda x: -x[1])


def diagnose(project):
    findings = []

    def add(level, title, why, fix, ref, where=()):
        findings.append((level, title, why, fix, ref, list(where)))

    tests = project.tests()
    test_files = [s for s in project.sources if not s.is_main]
    if project.tool == "gradle":
        props = gradle_props(project.root)
        multi = len(project.gradle_projects) > 0
        if props.get("org.gradle.daemon", "").lower() == "false":
            add("yuqori", "Gradle daemon o'chirilgan",
                "har yurish JVM va build konfiguratsiyasini noldan ko'taradi",
                "gradle.properties dan org.gradle.daemon=false ni olib tashlash", "testing 16.10")
        if multi and props.get("org.gradle.parallel", "").lower() != "true":
            add("o'rta", "Gradle modullari ketma-ket yig'iladi",
                "%d modul bor, org.gradle.parallel yoqilmagan" % len(project.gradle_projects),
                "gradle.properties: org.gradle.parallel=true", "testing 15.3")
        if props.get("org.gradle.caching", "").lower() == "false":
            add("o'rta", "Gradle build cache o'chirilgan",
                "run_tests ham keshni yoqmaydi: yangi worktree har modulni noldan "
                "kompilyatsiya qiladi",
                "org.gradle.caching=false ni olib tashlash: run_tests o'zi faqat "
                "kompilyatsiyani lokal keshlaydi, test natijasini emas", "testing 16.10")
        cc = props.get("org.gradle.configuration-cache",
                       props.get("org.gradle.unsafe.configuration-cache", ""))
        if len(project.gradle_projects) >= 10 and cc.lower() != "true":
            add("past", "Har yurish %d modulni qayta konfiguratsiya qiladi"
                % len(project.gradle_projects),
                "configuration cache yo'q: build skriptlari har buyruqda qayta bajariladi",
                "avval GENIUS_TEST_FLAGS=--configuration-cache bilan sinash, muammosiz "
                "bo'lsa gradle.properties: org.gradle.configuration-cache=true", "testing 16.10")
        builds = "\n".join(read(os.path.join(project.root, p)) for p in project.build_files)
        if re.search(r"upToDateWhen\s*\{\s*false\s*\}", builds):
            add("past", "Vazifa hech qachon UP-TO-DATE emas",
                "outputs.upToDateWhen { false }: o'zgarmagan kodda ham qayta yuradi",
                "test tashqi holatga bog'liq bo'lmasa olib tashlash", "testing 16.10")
        if re.search(r"showStandardStreams\s*=\s*true", builds):
            add("past", "testLogging.showStandardStreams yoqilgan",
                "har testning stdout va stderr i konsolga: log katta, yurish sekinroq",
                "faqat yiqilganda: events 'failed', exceptionFormat 'full'", "testing 16.10")
        scans = builds + "".join(read(os.path.join(project.root, n)) for n in
                                 ("settings.gradle", "settings.gradle.kts"))
        if re.search(r"com\.gradle\.(?:develocity|enterprise|build-scan)\b", scans) and \
                "--no-scan" not in extra_flags():
            add("past", "Build scan har yurishda yuklanadi",
                "Develocity yoki build scan plagini: yurish oxirida natija serverga yuboriladi",
                "agent yurishida kerak bo'lmasa GENIUS_TEST_FLAGS=--no-scan", "testing 16.10")
        if re.search(r"\bforkEvery\b", builds):
            add("yuqori", "forkEvery yoqilgan",
                "har N sinfda yangi JVM: Spring kontekst keshi har gal yo'qoladi",
                "forkEvery ni olib tashlash; izolyatsiya muammosini testning o'zida hal qilish",
                "testing 7.8")
        if not re.search(r"\bmaxParallelForks\b", builds) and len(tests) > 200:
            add("past", "Test JVM lari bitta",
                "%d test sinfi bitta forkda" % len(tests),
                "test { maxParallelForks = ... }: testlar umumiy port va bazasiz bo'lsa",
                "testing 15.3")
    elif project.tool == "maven":
        poms = "\n".join(project.pom_texts())
        if re.search(r"<reuseForks>\s*false\s*</reuseForks>", poms):
            add("yuqori", "Surefire reuseForks=false",
                "har sinf yangi JVM da: Spring kontekst keshi har gal yo'qoladi",
                "reuseForks ni olib tashlash (standart true)", "testing 7.8")
        if re.search(r"<forkCount>\s*0\s*</forkCount>", poms):
            add("o'rta", "Surefire forkCount=0", "testlar Maven JVM ining o'zida",
                "forkCount ni olib tashlash yoki 1C", "testing 15.3")

    # Spring kontekst keshi.
    dirties = [s for s in test_files if "@DirtiesContext" in s.text]
    if dirties:
        add("yuqori" if len(dirties) > 5 else "o'rta",
            "@DirtiesContext: %d sinfda" % len(dirties),
            "kontekst keshdan o'chadi, keyingi sinf uni noldan ko'taradi",
            "holatni testning o'zida tozalash; @DirtiesContext faqat haqiqatan "
            "kontekstni buzadigan testda", "testing 7.8", (s.rel for s in dirties))
    by_name = {}
    for src in test_files:
        by_name.setdefault(src.name, []).append(src)
    spring = [t for t in tests if SPRING_TEST_RE.search(t.text) or (
        EXTENDS_RE.search(t.text) and context_key(t, by_name))]
    keys = {}
    for test in spring:
        keys.setdefault(context_key(test, by_name), []).append(test)
    if len(keys) > 32:
        add("yuqori", "Spring kontekst kalitlari: taxminan %d xil" % len(keys),
            "kesh standarti 32 (spring.test.context.cache.maxSize): undan ortig'i "
            "LRU bilan chiqib ketadi va qayta quriladi",
            "umumiy abstrakt bazaviy sinf; @MockitoBean va @TestPropertySource "
            "faqat unda yoki umuman yo'q", "testing 7.8")
    elif len(keys) > 10:
        add("o'rta", "Spring kontekst kalitlari: taxminan %d xil" % len(keys),
            "har xil kalit alohida kontekst ko'tarilishi",
            "konfiguratsiyani bir nechta bazaviy sinfga yig'ish", "testing 7.8")

    # Testcontainers.
    per_method = []
    for src in test_files:
        for match in CONTAINER_FIELD_RE.finditer(src.text):
            if "static" not in match.group(1).split():
                per_method.append(src)
                break
    if per_method:
        add("yuqori", "@Container instance maydonda: %d sinfda" % len(per_method),
            "Testcontainers: instance maydondagi konteyner har test metodidan oldin "
            "ishga tushadi va keyin to'xtaydi",
            "static maydon yoki singleton container", "testing 8.4",
            (s.rel for s in per_method))
    starters = [s for s in test_files if re.search(CONTAINER_RE, s.text)]
    if len(starters) > 3:
        add("o'rta", "Konteyner %d sinfda alohida e'lon qilingan" % len(starters),
            "har sinf o'z konteynerini ko'taradi",
            "bitta singleton container yoki @ServiceConnection li umumiy konfiguratsiya",
            "testing 8.4", (s.rel for s in starters))

    sleeps = [s for s in test_files if re.search(r"\bThread\.sleep\s*\(", s.text)]
    if sleeps:
        add("o'rta", "Thread.sleep: %d test faylida" % len(sleeps),
            "har chaqiruv belgilangan vaqtni yo'qotadi va flaky test manbai",
            "Awaitility yoki boshqariladigan Clock", "sonarqube 30.5",
            (s.rel for s in sleeps))

    junit = ""
    for src in ("src/test/resources/junit-platform.properties",):
        for module in sorted({s.module for s in tests}):
            junit += read(os.path.join(project.root, module, src))
    if tests and "junit.jupiter.execution.parallel.enabled" not in junit:
        add("past", "JUnit parallel bajarish sozlanmagan",
            "bitta fork ichida sinflar ketma-ket",
            "junit.jupiter.execution.parallel.enabled=true faqat umumiy holatsiz "
            "testlarda; avval sinflar darajasida", "testing 12.8")

    return findings


def print_diagnosis(project):
    tests = project.tests()
    print("Tashxis: %s (%s, %d modul, %d test sinfi)" % (
        project.root, project.tool,
        max(len(project.gradle_projects), len(project.maven_modules), 1), len(tests)))
    findings = diagnose(project)
    order = {"yuqori": 0, "o'rta": 1, "past": 2}
    for level, title, why, fix, ref, where in sorted(findings, key=lambda f: order[f[0]]):
        print("\n[%s] %s" % (level, title))
        print("    nega: %s" % why)
        print("    nima qilish: %s" % fix)
        if where:
            print("    joylar: %s%s" % (", ".join(where[:3]),
                                        " (+%d)" % (len(where) - 3) if len(where) > 3 else ""))
        print("    qoida: %s" % ref)
    if not findings:
        print("\nBuild va test sozlamasida sekinlik belgisi topilmadi.")
    log, starts = context_starts([log_path(project.root, True),
                                  log_path(project.root, False)])
    if starts:
        total = sum(s for _, s in starts)
        print("\nSpring kontekst ishga tushishi (%s): %d marta, jami %.0f s, "
              "o'rtacha %.1f s" % (os.path.basename(log), len(starts), total,
                                   total / len(starts)))
        for name, seconds in sorted(starts, key=lambda x: -x[1])[:5]:
            print("    %6.1f s  %s" % (seconds, name))
        print("    har yangi kontekst kesh kaliti farqi: qoida testing 7.8")
    slow = slowest_reports(project.root)
    if slow:
        total = sum(t for _, t in slow)
        print("\nOxirgi yurish hisobotlari: %d sinf, jami %.0f s (sinflar yig'indisi)"
              % (len(slow), total))
        for name, seconds in slow[:10]:
            print("    %6.1f s  %s" % (seconds, name))
    else:
        print("\nOxirgi yurish hisoboti yo'q (build/test-results, target/surefire-reports).")
    print("\nKo'rilmagan: haqiqiy vaqt taqsimoti. Gradle da `--profile`, Maven da "
          "surefire XML hisoboti uni beradi. Tashxis o'zgartirish kiritmaydi.")
    return 0


# -- kirish --------------------------------------------------------------------

def main(argv=None):
    parser = argparse.ArgumentParser(
        prog="run_tests.py", description=__doc__.split("\n\n")[0],
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("files", nargs="*", help="o'zgargan fayllar")
    parser.add_argument("--diff", action="store_true", help="git dagi o'zgarishlar")
    parser.add_argument("--asos", metavar="REF", help="REF...HEAD va ishchi o'zgarish")
    parser.add_argument("--modul", action="append", default=[], metavar="PAPKA",
                        help="modulning barcha testlari (takrorlanadi)")
    parser.add_argument("--hammasi", action="store_true", help="to'liq suite")
    parser.add_argument("--yurgiz", action="store_true", help="buyruqni yurgizish")
    parser.add_argument("--tashxis", action="store_true", help="suite nega sekin")
    parser.add_argument("--isit", action="store_true",
                        help="oldindan kompilyatsiya (fonda, guruh ochilgach)")
    parser.add_argument("--hisobot", action="store_true", help="test vaqti jurnali")
    parser.add_argument("--kun", type=int, default=7, help="--hisobot oralig'i")
    parser.add_argument("--qayta", type=int, default=1, metavar="N",
                        help="yiqilgan sinflarni N marta qayta yurgizish (beqarorni ajratadi)")
    parser.add_argument("--navbat", action="store_true",
                        help="worktree lar orasida ketma-ket (umumiy port yoki baza)")
    parser.add_argument("--ildiz", metavar="PAPKA", help="loyiha ildizi")
    parser.add_argument("--vaqt", type=int, default=DEFAULT_TIMEOUT, metavar="S",
                        help="yurish chegarasi, soniya (standart %d)" % DEFAULT_TIMEOUT)
    parser.add_argument("--log", metavar="FAYL", help="log fayli")
    args = parser.parse_args(argv)
    sys.stdout.reconfigure(encoding="utf-8")

    if args.hisobot:
        return report(max(1, args.kun))
    root = (os.path.realpath(os.path.abspath(args.ildiz)) if args.ildiz
            else project_root(os.getcwd()))
    # Log build chiqishi bilan qayta yoziladi: ixtiyoriy yo'l (~/.bashrc,
    # manba fayl) shu chiqish bilan almashardi. Faqat temp yoki loyiha.
    if args.log and not (inside(args.log, tempfile.gettempdir()) or inside(args.log, root)):
        print("--log faqat temp papka (%s) yoki loyiha (%s) ichida bo'ladi: %s"
              % (tempfile.gettempdir(), root, args.log), file=sys.stderr)
        return 2
    project = Project(root)
    if project.tool is None:
        print("Gradle yoki Maven loyihasi topilmadi: %s" % root)
        return 2
    if args.tashxis:
        return print_diagnosis(project)
    if args.isit:
        log = args.log or log_path(root, False).replace(".log", "-isit.log")
        code, seconds = execute(project, warmup_commands(project), log, args.vaqt)
        record(root, "isitish", Plan(), code, seconds)
        print("Isitish: exit=%d, %d s, log: %s" % (code, seconds, log))
        if code and code != 124:
            print(summarize(log))
        return 0 if code == 0 else (3 if code == 124 else 1)

    plan = Plan()
    if args.modul and not args.hammasi:
        tests = project.tests()
        for folder in args.modul:
            folder = relative_to(folder, root) if os.path.isdir(folder) \
                else rel(folder).strip("/")
            module = "" if folder in ("", ".") else folder.strip("/")
            sets = sorted({s.sset for s in tests if s.module == module})
            if not sets:
                print("Modulda test yo'q: %s" % (module or "."))
                return 2
            for sset in sets:
                plan.add_whole(module, sset, "--modul %s" % (module or "."))
    elif not args.hammasi:
        if args.files:
            existing = [relative_to(path, root) for path in args.files]
            deleted = [p for p in existing if not os.path.exists(os.path.join(root, p))]
            existing = [p for p in existing if p not in deleted]
        elif args.diff or args.asos:
            base = None
            if args.asos:
                base = verify_base(root, args.asos)
                if base is None:
                    print("--asos commit emas yoki '-' bilan boshlanadi: %s" % args.asos,
                          file=sys.stderr)
                    return 2
            existing, deleted = changed_files(root, base)
            outside = outside_root(root, base)
            if outside:
                print("Eslatma: %d fayl --ildiz dan tashqarida, hisobga olinmadi" % outside)
        else:
            parser.print_usage()
            print("fayl, --diff, --asos yoki --hammasi kerak", file=sys.stderr)
            return 2
        plan = select(project, existing, deleted)
        if plan.empty():
            print("Ta'sirlangan test yo'q: %s" % (
                "o'zgarish yo'q" if not (existing or deleted)
                else "o'zgargan fayllar testga tegmaydi"))
            for note in plan.notes:
                print("Eslatma: %s" % note)
            return 0

    everything = args.hammasi or bool(plan.everything)
    cmds = commands(project, plan, args.hammasi)
    print(describe(project, plan, cmds, args.hammasi))
    if not args.yurgiz:
        print("Yurgizish: shu buyruqqa --yurgiz qo'shiladi (Bash timeout 600000)%s."
              % ("; to'liq suite fonda yurgiziladi" if everything else ""))
        return 0

    log = args.log or log_path(root, everything)
    summary_log = log
    mode = "hammasi" if everything else ("modul" if args.modul else "maqsadli")
    started = time.time()
    code, seconds = execute(project, cmds, log, args.vaqt, args.navbat)
    flaky = []
    if code not in (0, 124, 127) and args.qayta > 0 and not has_compile_error(log):
        failed = failed_classes(project, started)
        count = sum(len(v) for v in failed.values())
        if 0 < count <= MAX_RERUN:
            again = [c for c in commands(project, rerun_plan(failed))
                     if not c[1].startswith("formatlash")]
            # Alohida log: bitta logda ikki yurish xulosani ikki marta sanaydi.
            rerun_log = log[:-4] + "-qayta.log" if log.endswith(".log") else log + ".qayta"
            for _ in range(args.qayta):
                rerun_start = time.time()
                code2, more = execute(project, again, rerun_log, args.vaqt, args.navbat)
                seconds += more
                if code2 == 0:
                    break
            still = failed_classes(project, rerun_start)
            if code2 == 0:
                flaky = [f for names in failed.values() for f in names]
                code = 4
            else:
                flaky = [f for k, names in failed.items() for f in names
                         if f not in still.get(k, ())]
                summary_log = rerun_log
    state = {0: "yashil", 4: "beqaror", 124: "vaqt tugadi",
             127: "yurgizib bo'lmadi"}.get(code, "yiqildi")
    record(root, mode, plan, code, seconds, len(flaky))
    print("\nNatija: %s, exit=%d, %d s, log: %s%s" % (
        state, code, seconds, log,
        "" if summary_log == log else ", qayta yurish: %s" % summary_log))
    if code == 124:
        print("Vaqt chegarasi %d s. To'liq suite bo'lsa uni fonda yurgizing "
              "(Bash run_in_background) va --vaqt ni oshiring." % args.vaqt)
    if flaky:
        print("Beqaror (birinchi yurishda yiqildi, qayta yurishda o'tdi): %s"
              % ", ".join(flaky[:10]))
        print("O'zgarish bilan bog'liq bo'lsa (o'zgargan test yoki o'zgargan kodga "
              "murojaat) bu poyga xatosi bo'lishi mumkin: egasi test-muhandis.")
    if code != 4:
        summary = summarize(summary_log)
        if summary:
            print(summary)
    return {0: 0, 4: 4, 124: 3}.get(code, 1)


if __name__ == "__main__":
    sys.exit(main())
