#!/usr/bin/env python3
"""PreToolUse hook: qimmat amallarni to'xtatib, arzon yo'lni ko'rsatadi.

Ikki xil qimmatlik bor va ikkalasi ham shu yerda tekshiriladi, chunki
alohida hook har Bash chaqiruvida ikkinchi marta Python ishga tushirardi.

1. Kontekst qimmatligi. docs/ dagi bob o'n minglab token, bitta bo'lim
   esa ~700. Butun faylni o'qish kontekstni yoqadi, holbuki javob kichik
   bo'lakda turadi. Fayllar ro'yxati yozilmagan: har chaqiruvda o'qiladigan
   bo'lakning bayti sanaladi, shuning uchun yangi bob qo'shilsa ham ishlaydi.
   index/ dagi TSV ham shu tartibda: u grep qilinadi, kontekstga olinmaydi.

2. Pul va vaqt qimmatligi. Konteyner ko'tarish yoki bazaga ulanish bir
   necha daqiqa va katta chiqish beradi, holbuki kerakli javob ko'pincha
   kodning yoki test chiqishining o'zida. Bu amallar `ask` bilan odam
   qaroriga qo'yiladi: sabab matnida nega qimmatligi va arzon yo'l
   yoziladi, ruxsat berishni esa foydalanuvchi o'zi hal qiladi.

Nega `deny` emas: qaysi biri haqiqatan kerakligini faqat odam biladi.
Avval `COST_OK=1` qochish yo'li bor edi, lekin uni modelning o'zi
qo'yardi, ya'ni to'siq amalda o'zini-o'zi ochadigan to'siq edi. `ask`
bilan qaror egasi almashadi va qochish yo'li kerak bo'lmaydi.

Subagent ichida (payloadda `agent_id` bor) `ask` o'rniga `deny`: u yerda
so'rov muddatsiz kutadi va butun zanjirni to'xtatadi (workflow agenti
6 soat 20 daqiqa psql so'rovida qotib qolgan). Subagent ishni to'xtatib,
nima kerakligini asosiy sessiyaga qaytaradi, foydalanuvchidan esa asosiy
sessiya so'raydi. Sabab matni shuni aytadi.

`flyway:clean`, `flywayClean` va `liquibase:dropAll` ham `ask`, lekin
sababi boshqa: ular jonli bazani o'chiradi.

Katta bo'lakni o'qish esa `deny` bo'lib qoladi: u kontekstni himoya
qiladi va odam qarorini talab qilmaydi, arzon yo'l (`doc.sh show`)
har doim bir xil.

`.java` faylga Bash orqali yozish (`>`, `>>`, `tee`, `sed -i`, `perl -i`)
ham `deny`: check_code va rules_for darvozasi faqat Edit va Write da
ishlaydi, Bash bilan yozilgan kod undan jim o'tib ketardi. Heredoc
tanasidagi Java matni, faylni o'qish va `> Foo.java.txt` o'tadi. Bu ham
odatga qarshi to'siq: `python -c` bilan yozish ushlanmaydi.

Klondagi begona memory papkasini (`memory/<slug>/`, `umumiy` va
`claude-genius` dan boshqa) `git add` yoki `git commit` qilish `ask`:
klon ochiq repo, boshqa proyekt memorysi esa uning tashqarisida turadi
(GENIUS_MEMORY_DIR, R0.5).

3. Test vaqti. To'liq suite (`./gradlew test`, `mvn verify`) 5-8 daqiqa,
   `--rerun-tasks` va `--no-daemon` esa inkremental build va daemon ni
   yo'qotib, keyingi har yurishni ham sekinlashtiradi. Bular `deny`:
   arzon yo'l har doim bir xil (`run_tests.py`), u maqsadli, modul va
   to'liq rejimni ham beradi. `ask` bo'lsa zanjir har safar odamni
   kutib to'xtardi, holbuki bu yerda qaror yo'q. Filtrli yurish
   (`--tests`, `-Dtest=`) va testsiz build (`-x test`, `-DskipTests`)
   o'tadi. Yagona vazifa sifatidagi `clean` (`./gradlew clean`,
   `mvn clean`) esa `ask`: generatsiya qilingan kod eskirganda u
   haqiqatan kerak va buni faqat odam biladi. `clean` test, build yoki
   install bilan birga bo'lsa `deny` qoladi, test sharti undan oldin
   tekshiriladi: aks holda `mvn clean install` bir bosish bilan to'liq
   suite ni ochardi (HK-H12).

Chegaralangan o'qish o'lchanadi, sanalmaydi: `head -n N`, `head -c N`,
`tail -n +K`, `sed -n 'A,Bp'` va `Get-Content -TotalCount N` qaytaradigan
bayt Read dagi kabi hisoblanadi, ya'ni bir xil bo'lakka bir xil qaror.
Quvurda oxirgi bosqich hal qiladi: `cat BIG | wc -l`, `cat BIG | head`,
`nl BIG | sed -n '200,240p'` va `cat BIG > nusxa` o'tadi, `grep ''`,
`awk '1'` va `sed ''` esa butun fayl (HK-H3). Oddiy `grep naqsh` filtr
deb o'tadi. Tashxis buyruqlari ham o'tadi: docker ps, docker logs,
docker images, psql --version.

`budget.py --tiklash` `ask` (subagentda `deny`): u aktyor chegarasini
ochadi va buni model o'zi qilmasligi kerak. `--holat` va
`--yangi-vazifa` erkin (XV-O3).

Bash va PowerShell asboblari bir xil tekshiriladi: Windows da Git Bash
bo'lmasa PowerShell asbobi yoqiladi, va faqat Bash tekshirilsa docker,
baza va katta fayl to'siqlari jim o'chib qolardi.
"""

import glob
import json
import os
import re
import shlex
import sys

import hookio

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Shu papkalardagi shu kengaytmali fayllar kuzatiladi. index/ hosila,
# lekin sections.tsv ~600 KB: uni cat qilish bobni cat qilish bilan bir xil.
WATCHED_DIRS = {"docs": ".md", "dist": ".md", "index": ".tsv"}

# Bir o'qishda bundan ko'p bayt qaytsa to'siladi. Bo'lim o'rtacha 1.7 KB,
# eng kattasi 5.6 KB, ya'ni chegara bir necha bo'limga yetadi. Satr soni
# o'lchov emas: 1100 satrlik bob 138 KB (Read uni 70k token deb sanadi),
# zich bobda 300 satr esa 40 KB. doc.sh show bilan bitta o'zgaruvchi va
# bitta standart qiymat.
MAX_BYTES = int(os.environ.get("DOC_MAX_BYTES", "16000"))
# Read limit berilmasa shuncha satr qaytaradi.
READ_DEFAULT_LINES = 2000

# Buyruq boshi: ajratgichdan keyin, oldida sudo/time/env yoki VAR=qiymat
# bo'lishi mumkin. Prefiks bayrog'i qiymat olishi mumkin: `sudo -u postgres
# psql` dagi "postgres" buyruq emas. Yangi satr ham ajratgich, shuning
# uchun heredoc tanasi tekshiruvdan oldin olib tashlanadi (strip_heredoc).
# `timeout` uzun buyruqni o'rashning eng tabiiy shakli: muddati majburiy,
# `-s KILL` va `-k 5` bayrog'i esa qiymat oladi. `command` faqat bayroqsiz:
# `command -v psql` chaqiruv emas, tekshiruv. xargs, stdbuf va ionice
# ataylab yo'q: ular tabiiy shakl emas, faqat murakkablik qo'shadi.
CMD = (r"(?:^|[|;&\n(]\s*|\$\(\s*|`\s*)"
       r"(?:(?:sudo|time|env|nohup|nice|exec)(?:\s+-\S+(?:\s+[^\s|;&-][^\s|;&]*)??)*\s+"
       r"|timeout(?:\s+(?:-[sk]\s+[^\s-]\S*|--\w[\w-]*(?:=\S+)?|-(?![sk]\s)\w+))*"
       r"\s+\d[\d.]*[smhd]?\s+"
       r"|command\s+"
       r"|[A-Za-z_]\w*=\S*\s+)*")

# Buyruq boshidagi prefiks (sudo, timeout, VAR=...): bosqich matnida.
PREFIX_RE = re.compile(CMD)

# Bash orqali .java ga yozish: qayta yo'naltirish, tee, joyida sed/perl.
# Nom oxirida `(?![\w.])`: `Foo.java.txt` va `Foo.javadoc` Java fayl emas.
# perl bayrog'i `-pi`, `-0pi` ham bo'ladi, lekin `-Mstrict` emas.
JAVA_FILE = r"[^\s|;&<>()`]*\.java['\"]?(?![\w.])"
JAVA_WRITE_RE = re.compile(
    r">>?\s*" + JAVA_FILE
    + r"|" + CMD + r"tee\s+(?:[^|;&\n]*?\s)?" + JAVA_FILE
    + r"|" + CMD + r"(?:sed|perl)\s+(?:[^|;&\n]*?\s)?"
    r"(?:-[A-Za-z0-9]{0,2}i|--in-place)[^|;&\n]*?\s" + JAVA_FILE)
JAVA_WRITE_HINT = ("Kichik o'zgarish uchun Edit, yangi fayl uchun Write. "
                   "Yozishdan oldin: {rules_for} <fayl>")

HEREDOC_RE = re.compile(
    r"<<-?\s*(['\"]?)(\w+)\1[^\n]*(?:\n.*?)??(?:\n[ \t]*\2[ \t]*(?=\n|$)|\Z)", re.S)

# docker fe'li. Fe'ldan keyin yo'l yoki fayl nomi belgisi kelmasin:
# `-f build/compose.yml ps` dagi "build" fe'l emas.
VERB = r"(?:up|run|build|pull|start|create)(?![\w./-])"
# Bayroq qiymat bilan yoki qiymatsiz: `-f x.yml`, `--profile dev`, `-d`.
# `--?\w` bir ma'noli, shuning uchun regex qaytish (backtracking) qilib
# osilib qolmaydi.
DOCKER_FLAG = r"\s+--?\w[\w-]*(?:[ =](?!" + VERB + r")[^\s|;&-][^\s|;&]*)?"
DB_CLIENT = r"(?:psql|mysql|mariadb|mongosh|mongo|redis-cli)\b"
# Konteyner yoki pod ichida buyruq yurgizish: `docker compose -f x.yml exec`,
# `kubectl -n prod exec`.
EXEC = (r"(?:(?:docker|podman)(?:-compose|\s+compose)?|kubectl)(?:" + DOCKER_FLAG
        + r")*\s+exec\b")

# Pul va vaqt sarflaydigan amallar. Tashxis fe'llari (ps, logs, images,
# inspect, version) ataylab yo'q: ular arzon va ko'pincha aynan kerak.
EXPENSIVE = (
    (re.compile(CMD + r"(?:docker|podman)(?:-compose|\s+compose)?(?:" + DOCKER_FLAG
                + r")*\s+(?:container\s+|image\s+)?" + VERB),
     "Konteyner ko'tarish yoki yig'ish",
     "Daqiqalar va katta chiqish. Arzon yo'l: test chiqishidagi birinchi "
     "xato\nsababni aytadi, jadval va ustun uchun esa {schema} <src>."),
    # Skript nomi buyruq o'rnida turishi shart. Aks holda uni shunchaki
    # ATAGAN buyruq ham to'siladi: `wc -l install/x.ps1`, `git add x.ps1`.
    # Bu amalda uchradi, o'rnatuvchi faylni yozayotganda.
    # Papkali yo'l ham: `.\\install\\x.ps1`, `C:/a/x.ps1`. PowerShell
    # asbobida ham to'siladi: proyekt qoidasi skript yurgizishni taqiqlaydi,
    # oddiy PowerShell buyrug'i (Get-ChildItem) esa o'tadi.
    (re.compile(CMD + r"(?:pwsh|powershell(?:\.exe)?)\b"
                r"|" + CMD + r"(?:[.]{1,2}[/\\])?(?:[\w.:~-]+[/\\])*[\w.-]*\.ps1\b"),
     "PowerShell skripti",
     "Boshqa mashinada tekshirilmagan bo'ladi va shu yerda sinalmaydi.\n"
     "Arzon yo'l: shu ishni python3 yoki bash bilan bajarish."),
    # Har qanday ulanish, lokal ham: hostsiz `psql shop` ham jonli bazani
    # ochadi. Faqat versiya va yordam o'tadi. Konteyner yoki pod ichidagi
    # klient ham ulanish. Naqsh qo'shtirnoq olib tashlangandan keyin
    # qo'llanadi (strip_quoted): `grep 'psql' .` to'silmaydi, qo'shtirnoqli
    # URI bilan `psql` esa to'siladi. Tekshiruv keyingi buyruqqa o'tmaydi.
    (re.compile(CMD + DB_CLIENT + r"(?!\s+(?:--version|--help|-V)\b)"
                r"|" + CMD + EXEC + r"[^|;&\n]*?\s" + DB_CLIENT),
     "Bazaga ulanish",
     "Sekin va jonli bazaga tegadi. Jadval, ustun va FK uchun ulanish\n"
     "shart emas: {schema} <src>. Indeks, constraint va plan esa faqat\n"
     "bazada, ularni bilish kerak bo'lsa ulanish o'rinli."),
)

# Gradle va Maven chaqiruvi: bajariluvchi nom va shu buyruqning qolgani.
# `sh gradlew test` ham chaqiruv: wrapper bajariluvchi bo'lmasa shunday yoziladi.
BUILD_RE = re.compile(
    CMD + r"(?:(?:sh|bash)\s+)?"
    r"((?:[\w.~-]*[/\\])*(?:gradlew(?:\.bat)?|gradle|mvnw(?:\.cmd)?|mvn))"
    r"(?![\w.-])([^|;&\n]*)")
# Gradle da test yurgizadigan vazifa: test, check, build, *Test (integrationTest).
GRADLE_TEST_TASK = re.compile(r"(?:^|:)(?:test|check|build|\w+Test)$")
# Qiymat oladigan bayroqlar: qiymati vazifa nomi deb o'qilmasin.
GRADLE_VALUED = {"--tests", "-x", "--exclude-task", "--console", "--warning-mode",
                 "-p", "--project-dir", "-c", "--settings-file", "-I",
                 "--init-script", "--max-workers", "-g", "--gradle-user-home",
                 "--priority", "--include-build"}
MAVEN_VALUED = {"-pl", "--projects", "-rf", "--resume-from", "-f", "--file",
                "-s", "--settings", "-gs", "--global-settings", "-t",
                "--toolchains", "-T", "--threads", "-P", "--activate-profiles",
                "-l", "--log-file", "-b", "--builder"}
MAVEN_TEST_PHASES = {"test", "integration-test", "verify", "install",
                     "package", "deploy"}
# Artefakt yig'adigan buyruq: maqsad test emas, paket bo'lishi mumkin.
MAVEN_PACKAGE_PHASES = {"package", "install", "deploy"}
GRADLE_PACKAGE_TASK = re.compile(r"(?:^|:)build$")
PACKAGE_NOTE = ("Maqsad artefakt bo'lsa: testlar run_tests bilan o'tgan bo'lsa "
                "-DskipTests bilan package (Gradle: assemble yoki bootJar)")
MAVEN_SKIP_RE = re.compile(r"^-D(?:skipTests(?:=true)?|maven\.test\.skip=true)$")
MAVEN_FILTER_RE = re.compile(r"^-D(?:it\.)?test=\S+")
# Migratsiya asbobining bazani tozalovchi vazifasi. Bu `clean` emas:
# inkremental build ga emas, jonli bazaga tegadi, ya'ni qaror odamniki.
# Gradle liquibase plaginida xuddi shu vazifa `dropAll`.
DB_WIPE_TASKS = {"flyway:clean", "flywayClean", "liquibase:dropAll", "dropAll"}
DB_WIPE_HINT = ("Jadval va ma'lumot qaytarib bo'lmaydigan tarzda yo'qoladi. Test uchun\n"
                "Testcontainers bazasi yetadi, sxema uchun esa {schema} <src>.")

BUILD_HINT = (
    "Arzon yo'l bitta asbob, u modulni o'zi qo'yadi va logni faylga yozadi:\n"
    "  {run_tests} --diff --yurgiz          - o'zgarishga ta'sir qilgan testlar\n"
    "  {run_tests} --modul <papka> --yurgiz - bitta modulning hammasi\n"
    "  {run_tests} --ildiz <papka> --diff --yurgiz - build ichki papkada (backend/pom.xml)\n"
    "  {run_tests} --hammasi --yurgiz       - to'liq suite: partiya oxirida bir marta, fonda"
)


def split_args(text):
    try:
        return shlex.split(text)
    except ValueError:
        return text.split()


CLEAN_WHY = ("clean inkremental build ni o'chiradi: keyingi har yurish hammasini "
             "qaytadan kompilyatsiya qiladi. Gradle va Maven o'zgargan faylni o'zi "
             "kuzatadi")
CLEAN_HINT = (
    "Generatsiya qilingan kod yoki annotation processor natijasi eskirgan\n"
    "bo'lsa o'rinli. Keyin test maqsadli yuradi:\n"
    "  {run_tests} --diff --yurgiz")


def is_clean(word):
    return word == "clean" or word.endswith(":clean")


def build_problem(tool, args):
    """(qaror, nima, nega) yoki None. tool: gradle yoki maven.

    Test sharti `clean` dan oldin: `mvn clean install` to'liq suite, va
    clean ning `ask` i uni ochib yubormasligi kerak (HK-H12). Yagona
    vazifa sifatidagi clean `ask`, boshqa vazifa bilan birga `deny`.
    """
    words, i = [], 0
    filtered = skipped = False
    while i < len(args):
        arg = args[i]
        if arg in ("--rerun-tasks", "--no-daemon") or arg == "-Dorg.gradle.daemon=false":
            return ("deny", arg, "%s inkremental build va daemon ni yo'qotadi: keyingi har "
                         "yurish hammasini qaytadan kompilyatsiya qiladi" % arg)
        if tool == "gradle" and arg == "--tests":
            filtered = True
        if tool == "gradle" and arg in ("-x", "--exclude-task") and i + 1 < len(args):
            skipped = skipped or bool(GRADLE_TEST_TASK.search(args[i + 1]))
        if tool == "maven" and (MAVEN_FILTER_RE.match(arg)):
            filtered = True
        if tool == "maven" and MAVEN_SKIP_RE.match(arg):
            skipped = True
        valued = GRADLE_VALUED if tool == "gradle" else MAVEN_VALUED
        if arg in valued:
            i += 2
            continue
        if not arg.startswith("-") and arg not in DB_WIPE_TASKS:
            words.append(arg)
        i += 1
    if tool == "gradle":
        runs = [w for w in words if GRADLE_TEST_TASK.search(w)]
    else:
        runs = [w for w in words if w in MAVEN_TEST_PHASES
                or w.endswith(("surefire:test", "failsafe:integration-test"))]
    if runs and not filtered and not skipped:
        why = ("to'liq suite 5-8 daqiqa; aktyor uni qayta-qayta yurgizsa guruh "
               "soatga cho'ziladi. Ko'p modulli loyihada modulsiz --tests ham "
               "yiqiladi, asbob esa modulni o'zi qo'yadi")
        packaging = (any(GRADLE_PACKAGE_TASK.search(w) for w in runs) if tool == "gradle"
                     else any(w in MAVEN_PACKAGE_PHASES for w in runs))
        if packaging:
            why += ".\n" + PACKAGE_NOTE
        return ("deny", "filtrsiz test: %s" % " ".join(runs), why)
    if any(is_clean(w) for w in words):
        if all(is_clean(w) for w in words):
            return ("ask", "clean", CLEAN_WHY)
        return ("deny", "clean boshqa vazifa bilan birga",
                CLEAN_WHY + ". Build holati haqiqatan buzilgan bo'lsa clean ni "
                "alohida buyruq qiling (foydalanuvchi tasdiqlaydi), keyin vazifani")
    return None


def check_build(command):
    """Buyruq o'rni qo'shtirnoqsiz matndan topiladi (`grep 'gradle test'`
    chaqiruv emas), argumentlar esa asl matndan o'qiladi: `-Dtest='A,B'`
    filtri bo'shatilsa, maqsadli yurish filtrsiz deb to'silardi.
    strip_quoted uzunlikni saqlaydi, shuning uchun oraliq bir xil.

    deny shu yerda beriladi, `ask` lar esa (sabab, maslahat) ro'yxati
    bo'lib qaytadi: ular boshqa deny tekshiruvlaridan keyin so'raladi,
    aks holda ruxsat to'liq suite yoki katta o'qishni ochib yuborardi."""
    base = strip_heredoc(command)
    asks, wipes = [], []
    for match in BUILD_RE.finditer(strip_quoted(base)):
        exe = os.path.basename(match.group(1).replace("\\", "/")).lower()
        tool = "gradle" if exe.startswith("gradle") else "maven"
        # `(cd app && ./gradlew test)`: subshell qavsi argument emas.
        args = split_args(base[match.start(2):match.end(2)].rstrip().rstrip(")`"))
        problem = build_problem(tool, args)
        if problem:
            verdict, what, why = problem
            reason = "Test vaqti: %s.\n%s." % (what, why)
            if verdict == "deny":
                decide("deny", reason, BUILD_HINT)
            asks.append((reason, CLEAN_HINT))
        wipes += [a for a in args if a in DB_WIPE_TASKS]
    if wipes:
        asks.append(("Jonli bazani o'chiradi: %s." % ", ".join(wipes), DB_WIPE_HINT))
    return asks


# Maslahat matnlari shablon: yo'llar to'siq paytida qo'yiladi (commands).
HINT = (
    "Butun faylni o'qish o'rniga indeksdan foydalaning:\n"
    "  {doc} find [-f] <so'rov>      - bo'limni topish\n"
    "  {doc} show <hujjat> <raqam>   - faqat o'sha bo'limni o'qish\n"
    "  {doc} outline <hujjat> [bob]  - ichidagi bo'limlar\n"
    "Batafsil: {claude_md}"
)


def commands():
    """Maslahatdagi yo'llar: klon ichida nisbiy, boshqa proyektda mutlaq.

    Global o'rnatishda hook boshqa proyektda yuradi, u yerda
    `tools/doc.sh` va `CLAUDE.md` yo'q: maslahat "No such file" ga olib
    borardi. Shuning uchun matn modul darajasida emas, to'siq paytida
    yasaladi. Yordamchi ham faqat shu paytda yuklanadi: hook har Read va
    Bash chaqiruvida ishlaydi, ruxsat holatida import kerak emas.
    """
    from docref import in_clone, tool_cmd
    claude_md = "CLAUDE.md"
    if not in_clone():
        claude_md = os.path.join(ROOT, claude_md).replace("\\", "/")
    return {"doc": tool_cmd("doc.sh"),
            "schema": tool_cmd("schema_from_entities.py"),
            "run_tests": tool_cmd("run_tests.py"),
            "rules_for": tool_cmd("rules_for.py"),
            "budget": tool_cmd("budget.py"),
            "claude_md": claude_md}


def decide(decision, reason, hint):
    json.dump(
        {
            "hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "permissionDecision": decision,
                "permissionDecisionReason": reason + "\n" + hint.format(**commands()),
            }
        },
        sys.stdout,
    )
    sys.exit(0)


def deny(reason):
    """Kontekstni himoya qiladi: arzon yo'l bir xil, qaror kerak emas."""
    decide("deny", reason, HINT)


def deny_with(reason, hint):
    """deny, o'z maslahati bilan (HINT kontekst haqida)."""
    decide("deny", reason, hint)


# main() payloaddan qo'yadi: subagent ichida `ask` muddatsiz kutardi.
IN_SUBAGENT = False
SUBAGENT_NOTE = ("Bu qaror foydalanuvchiniki: ishni shu yerda to'xtatib, asosiy "
                 "sessiyaga nima kerakligini va nega arzon yo'l yetmaganini qaytaring.")


def ask(reason, hint):
    """Pul va vaqt sarflaydi: qarorni odam qiladi.

    Subagentda so'rovga hech kim javob bermaydi va zanjir osilib qoladi,
    shuning uchun u yerda `deny` va qaror asosiy sessiyaga qaytariladi.
    """
    if IN_SUBAGENT:
        decide("deny", reason + "\n" + SUBAGENT_NOTE, hint)
    decide("ask", reason, hint)


def watched_path(candidate):
    """Kuzatiladigan fayl (WATCHED_DIRS) ning to'liq yo'li, aks holda None."""
    if not candidate.endswith(tuple(WATCHED_DIRS.values())):
        return None
    for base in (os.getcwd(), ROOT):
        full = os.path.normpath(os.path.join(base, candidate))
        try:
            rel = os.path.relpath(full, ROOT)
        except ValueError:
            continue
        head = rel.split(os.sep)[0]
        if (head in WATCHED_DIRS and full.endswith(WATCHED_DIRS[head])
                and os.path.isfile(full)):
            return full
    return None


_LINES = {}


def file_lines(path):
    """Fayl satrlarining bayt uzunligi (satr oxiri bilan). Read va Bash
    o'lchovi shu bitta ro'yxatdan: bir xil bo'lak bir xil bayt."""
    if path not in _LINES:
        try:
            with open(path, "rb") as handle:
                _LINES[path] = [len(line) for line in handle]
        except OSError:
            _LINES[path] = []
    return _LINES[path]


def slice_bytes(path, offset=None, limit=None):
    """Read qaytaradigan bo'lakning bayt hajmi: offset dan limit satr."""
    start = max(offset if isinstance(offset, int) else 1, 1) - 1
    stop = start + (limit if isinstance(limit, int) and limit > 0 else READ_DEFAULT_LINES)
    return sum(file_lines(path)[start:stop])


def check_read(tool_input):
    full = watched_path(tool_input.get("file_path") or "")
    if full is None:
        return
    limit = tool_input.get("limit")
    limit = limit if isinstance(limit, int) and limit > 0 else None
    size = slice_bytes(full, tool_input.get("offset"), limit)
    if size <= MAX_BYTES:
        return
    what = "chegarasiz o'qilmoqda" if limit is None else "limit=%d" % limit
    deny("%s - %s, %d KB qaytadi (chegara %d KB)."
         % (os.path.relpath(full, ROOT), what, size // 1000, MAX_BYTES // 1000))


QUOTED_RE = re.compile(r"'[^']*'|\"[^\"]*\"")


def strip_quoted(command):
    """Qo'shtirnoq ichidagi matnni bo'sh joyga almashtiradi.

    `grep -n 'docker run' .` buyrug'i konteyner ko'tarmaydi, u shu haqda
    QIDIRADI. Naqsh ichidagi so'zni chaqiruv deb o'qish qidiruvning
    o'zini to'sib qo'yadi. Bu amalda uchradi: qo'riqchi shu repoda
    o'z sozlamalarini qidirgan buyruqni to'xtatdi.
    """
    return QUOTED_RE.sub(lambda m: " " * len(m.group(0)), command)


def strip_heredoc(command):
    """Heredoc tanasini olib tashlaydi, `<<EOF` qatori qoladi.

    Tana buyruq emas, matn: `cat > notes <<EOF` ichidagi "docker run"
    yoki fayl nomi chaqiruv deb o'qilmasligi kerak.
    """
    return HEREDOC_RE.sub(lambda m: m.group(0).split("\n", 1)[0], command)


def check_cost(command):
    """Konteyner, baza va PowerShell: qarorni odamga qo'yadi.

    Bu odatga qarshi to'siq, xavfsizlik chegarasi emas: `bash -c` ichiga
    yashirilgan buyruqni u ko'rmaydi va ko'rishga urinmaydi ham. Shuning
    uchun ham `deny` emas `ask`: chetlab o'tish oson ekan, qat'iy to'siq
    faqat arzon yo'lni yashirardi.
    """
    command = strip_quoted(strip_heredoc(command))
    for pattern, what, hint in EXPENSIVE:
        match = pattern.search(command)
        if match:
            found = match.group(0).lstrip(" \t\n|;&(`$").strip()
            ask("%s qimmat amal: %s" % (what, found), hint)


def slurped(arg):
    """Argument ko'rsatgan kuzatiladigan fayllar: qo'shtirnoq va glob bilan.

    `(cat x.md)` va `$(cat x.md)` da yopuvchi qavs argumentga yopishadi.
    """
    arg = arg.strip("'\"`)")
    if not any(ch in arg for ch in "*?["):
        full = watched_path(arg)
        return {full} if full else set()
    found = set()
    for base in (os.getcwd(), ROOT):
        for path in glob.glob(os.path.join(base, arg)):
            full = watched_path(path)
            if full:
                found.add(full)
    return found


def mask_quoted(command):
    """Qo'shtirnoq ichidagi ajratgich va bo'sh joyni `_` ga almashtiradi.

    strip_quoted dan farqi: matn qoladi. `> "src/Foo.java"` dagi nom
    ko'rinadi, `echo 'x > Foo.java'` dagi `>` esa operator emas, sed
    skriptidagi `;` ham buyruqni bo'lmaydi.
    """
    return QUOTED_RE.sub(lambda m: re.sub(r"[\s|;&<>()`]", "_", m.group(0)), command)


def check_java_write(command):
    """Heredoc tanasi va qo'shtirnoq ichidagi matn yozuv emas, tekshiruv
    ulardan keyin. `cat > X.java <<EOF` qatori strip_heredoc dan keyin
    ham qoladi."""
    match = JAVA_WRITE_RE.search(mask_quoted(strip_heredoc(command)))
    if match:
        decide("deny", "Java faylni Edit yoki Write bilan yozing: check_code va "
               "rules_for faqat shu asboblarda ishlaydi (%s)."
               % match.group(0).lstrip(" \t\n|;&(`$").strip(), JAVA_WRITE_HINT)


# Ochiq klonga yoziladigan memory papkalari (docref.SHARED_MEMORY bilan bir
# xil, test_guard solishtiradi). Boshqa proyekt memorysi klondan tashqarida
# turadi: GENIUS_MEMORY_DIR, sukut ~/.claude/genius-memory (R0.5).
SHARED_MEMORY = ("umumiy", "claude-genius")
# `git [-C yo'l] [-c k=v] add|commit ...`. Global bayroqlar va argumentlar
# asl matndan olinadi, o'rni esa niqoblangan matndan (mask_quoted).
GIT_STAGE_RE = re.compile(
    CMD + r"git((?:\s+(?:-[Cc]\s+[^\s|;&]+|--[\w-]+(?:=[^\s|;&]+)?|-[pP]))*)"
    r"\s+(add|commit)(?![\w-])([^|;&\n]*)")
# commit bayroqlari, qiymat oladigani: xabar matni yo'l deb o'qilmasin.
COMMIT_VALUED = {"-m", "-F", "-c", "-C", "-t", "--message", "--file",
                 "--reuse-message", "--reedit-message", "--author", "--date",
                 "--fixup", "--squash", "--cleanup", "--template", "--trailer",
                 "--pathspec-from-file"}
MEMORY_HINT = (
    "Klon ochiq repo: boshqa proyektning vazifa, qaror va fayl nomlari\n"
    "unga yozilmaydi (memory/README.md, \"Qayerga va qanday\"). Proyekt\n"
    "memorysi klondan tashqarida: GENIUS_MEMORY_DIR, sukut\n"
    "~/.claude/genius-memory/<slug>/, push siz. Klonga faqat memory/umumiy/\n"
    "va memory/claude-genius/ yoziladi.")


def clone_dir():
    """Klon: git add va commit tekshiruvi shu daraxtga nisbatan. Global
    o'rnatishda ROOT snapshot, klon GENIUS_CLONE (geniuslib, R7.8 XV-Y1).
    Hook fail-open: geniuslib yuklanmasa ROOT."""
    try:
        import geniuslib
        return geniuslib.clone_root(ROOT)
    except ImportError:
        return ROOT


def foreign_memory_dirs():
    """Klondagi `memory/` ostidagi begona slug papkalari."""
    base = os.path.join(clone_dir(), "memory")
    try:
        names = os.listdir(base)
    except OSError:
        return set()
    return {n for n in names if n not in SHARED_MEMORY and not n.startswith(".")
            and os.path.isdir(os.path.join(base, n))}


def staged_targets(args, verb):
    """(yo'llar, butun daraxtmi). `add -A`, `add .`, `commit -a` butun daraxt."""
    paths, broad, i, only_paths = [], False, 0, False
    while i < len(args):
        arg = args[i]
        i += 1
        if only_paths or not arg.startswith("-") or arg == "-":
            paths.append(arg)
            continue
        if arg == "--":
            only_paths = True
        elif arg in ("-A", "--all") or (verb == "commit" and arg == "-a"):
            broad = True
        elif verb == "commit" and arg in COMMIT_VALUED:
            i += 1
        elif verb == "commit" and not arg.startswith("--") and len(arg) > 2:
            # `-am "xabar"`: birlashgan bayroqlar, oxirgisi qiymat olishi mumkin.
            broad = broad or "a" in arg[1:]
            i += arg[-1] in "mFcCt"
    return paths, broad


def check_memory_git(command):
    """Klondagi begona memory papkasini git ga qo'shish yoki commit: `ask`.

    Global o'rnatishda har proyekt shu klonni ishlatadi, klon esa ochiq
    repo: xususiy proyekt nomi, qarorlari va fayl yo'llari uning tarixiga
    tushsa, o'chirish qimmat. Faqat aniq ko'ringan yo'l tekshiriladi:
    `memory/<slug>`, shuningdek `add -A`, `add .` va `commit -a` klonda
    begona papka bo'lsa. Bu ham odatga qarshi to'siq, `bash -c` ichini
    ko'rmaydi.
    """
    if "git" not in command:
        return
    base_cmd = strip_heredoc(command)
    for match in GIT_STAGE_RE.finditer(mask_quoted(base_cmd)):
        base = os.getcwd()
        flags = split_args(base_cmd[match.start(1):match.end(1)])
        for flag, value in zip(flags, flags[1:]):
            if flag == "-C":
                base = os.path.join(base, os.path.expanduser(value))
        verb = match.group(2)
        args = split_args(base_cmd[match.start(3):match.end(3)].rstrip().rstrip(")`"))
        paths, broad = staged_targets(args, verb)
        found = set()
        clone = clone_dir()
        for path in paths:
            full = os.path.normpath(os.path.join(base, os.path.expanduser(path)))
            try:
                rel = os.path.relpath(full, clone)
            except ValueError:
                continue   # Windows: boshqa disk
            parts = rel.split(os.sep)
            if parts[0] == "..":
                continue
            if rel == "." or parts == ["memory"]:
                broad = True   # klon ildizi yoki butun memory/
            elif (parts[0] == "memory" and parts[1] not in SHARED_MEMORY
                  and not (len(parts) == 2 and os.path.isfile(full))):
                found.add(parts[1])
        try:
            in_clone = not os.path.relpath(
                os.path.normpath(base), clone).split(os.sep)[0] == ".."
        except ValueError:
            in_clone = False
        if broad and in_clone:
            found |= foreign_memory_dirs()
        if found:
            ask("Begona memory ochiq klonga: git %s, memory/%s."
                % (verb, ", memory/".join(sorted(found))), MEMORY_HINT)


# --- Proyekt commit xabari: oddiy inglizcha, muallifsiz ------------------
#
# Foydalanuvchi qoidasi: xabar qisqa, inson tilida; "Co-Authored-By", model
# yoki vosita nomi, "Generated with", "AI" va ichki reja raqami ("Faza 3:")
# yo'q. Harness attribution eslatmasidan bu qoida ustun, shuning uchun
# eslatma xabarga qo'shgan satr `deny` oladi. Faqat inline xabar (`-m`,
# `--message`, heredoc) tekshiriladi, `-F fayl` o'qilmaydi. Klonning o'zida
# qoida qo'llanmaydi.
COMMIT_WORDS_RE = re.compile(
    r"co-authored-by|(?<![./\w])claude(?![\w/])|\banthropic\b"
    r"|\b(?:opus|sonnet|haiku|fable)\b|generated\s+(?:with|by)|\bai\b"
    r"|\bassistant\b|\bfaza\s*\d+\s*:", re.IGNORECASE)
COMMIT_MESSAGE_FLAGS = ("-m", "--message")
COMMIT_HINT = (
    "Xabar inglizcha, oddiy, bir qator (kerak bo'lsa qisqa tana):\n"
    "  git commit -m \"Retry payment calls on timeout\"\n"
    "Muallif satri, model yoki vosita nomi, \"AI\" va reja raqami yozilmaydi.")


def commit_messages(command):
    """Har `git commit` ning inline xabarlari (`-m`, `--message`, `-am`) va
    buyruqdagi heredoc matnlari."""
    base_cmd = strip_heredoc(command)
    found, has_commit = [], False
    for match in GIT_STAGE_RE.finditer(mask_quoted(base_cmd)):
        if match.group(2) != "commit":
            continue
        has_commit = True
        args = split_args(base_cmd[match.start(3):match.end(3)].rstrip().rstrip(")`"))
        for i, arg in enumerate(args):
            value = None
            if arg in COMMIT_MESSAGE_FLAGS and i + 1 < len(args):
                value = args[i + 1]
            elif arg.startswith("--message="):
                value = arg.split("=", 1)[1]
            elif arg.startswith("-m") and len(arg) > 2 and not arg.startswith("--"):
                value = arg[2:]
            elif (arg.startswith("-") and not arg.startswith("--") and len(arg) > 2
                  and arg.endswith("m") and i + 1 < len(args)):
                value = args[i + 1]   # `-am "xabar"`
            if value is not None:
                found.append(value)
    if has_commit:
        found += [m.group(0) for m in HEREDOC_RE.finditer(command)]
    return found


def check_commit_message(command):
    """Proyekt repolarida commit xabari qoidasi: taqiqlangan so'z bo'lsa `deny`."""
    if "commit" not in command or "git" not in command:
        return
    base = os.getcwd()
    for match in GIT_STAGE_RE.finditer(mask_quoted(strip_heredoc(command))):
        flags = split_args(command[match.start(1):match.end(1)])
        for flag, value in zip(flags, flags[1:]):
            if flag == "-C":
                base = os.path.join(base, os.path.expanduser(value))
    try:
        if os.path.relpath(os.path.normpath(base), clone_dir()).split(os.sep)[0] != "..":
            return   # genius klonining o'zi: qoida proyektlar uchun
    except ValueError:
        pass         # Windows: boshqa disk, klon emas
    for text in commit_messages(command):
        found = COMMIT_WORDS_RE.search(text)
        if found:
            deny_with("Commit xabarida taqiqlangan so'z: \"%s\"." % found.group(0).strip(),
                      COMMIT_HINT)


# --- Bash va PowerShell da o'qish hajmi (HK-H3) -------------------------
#
# Oqim kuzatiladigan fayllar satrlarining bayt uzunligi ro'yxati, bosqich
# uni o'zgartiradi: `head -n 40` boshidagi 40 tasini qoldiradi, `wc` va
# oddiy `grep` uni None ga (kichik yoki noma'lum) aylantiradi. Quvurning
# oxirgi bosqichidan chiqqan oqim kontekstga tushadi va o'shaning bayti
# MAX_BYTES bilan solishtiriladi, Read dagi slice_bytes kabi.

# Buyruqlar va quvur bosqichlari orasidagi ajratgich (qo'shtirnoq
# niqoblangan matnda). `2>&1`, `&>` va `>&2` dagi `&` ajratgich emas.
SPLIT_RE = re.compile(r"\|\||&&|\|&?|[;\n()`]|(?<![<>&])&(?![>&])")
# Qayta yo'naltirish: [fd]op[&fd] [nishon]. fd faqat so'z boshida:
# `a2>x` dagi 2 fayl nomining qismi.
REDIRECT_RE = re.compile(r"(?:(?<![^\s])(\d+|&))?(>>|>\||>|<<<|<<-?|<)(&[\d-]*)?"
                         r"[ \t]*([^\s<>]*)")
# Fayl o'rniga stdout: yo'naltirilgan bo'lsa ham kontekstga tushadi.
STDOUT_FILES = ("/dev/stdout", "/dev/stderr", "/dev/tty", "/dev/fd/1", "/dev/fd/2")

# Faylni boshdan oxirigacha chiqaradigan o'quvchilar. tee argumenti esa
# CHIQISH fayli, u oqimni o'zgartirmaydi.
WHOLE_READERS = {"cat", "bat", "batcat", "less", "more", "most", "view", "nl", "tac"}
# Chiqishi kichik: oqim kontekstga tushmaydi.
SMALL_OUTPUT = {"wc", "md5sum", "sha1sum", "sha256sum", "sha512sum", "b2sum",
                "cksum", "file", "stat", "du", "ls", "test", "[", "true", "false"}
GREP_FAMILY = {"grep", "egrep", "fgrep", "rg"}
AWK_FAMILY = {"awk", "gawk", "mawk", "nawk"}
# Butun faylga mos keladigan naqsh: `grep ''` cat bilan bir xil.
GREP_WHOLE = {"", "^", "$", ".*", "^.*", ".*$", "."}
GREP_SMALL_FLAGS = set("clLq")
GREP_SHORT_VALUED = set("mABCdD")
GREP_LONG_SMALL = {"count", "files-with-matches", "files-without-match", "quiet",
                   "silent"}
GREP_LONG_VALUED = {"max-count", "after-context", "before-context", "context",
                    "include", "exclude", "exclude-dir", "label", "devices",
                    "directories", "binary-files", "color", "colour"}
# awk dasturi butun satrni chiqaradi: `awk 1`, `awk '{print}'`.
AWK_WHOLE = {"1", "1;", "{print}", "{print;}", "{print$0}", "{print$0;}", "NR"}
AWK_RANGE_RE = re.compile(r"NR(>=?)(\d+)&&NR(<=?)(\d+)(?:\{print(?:\$0)?;?\})?")
AWK_LINE_RE = re.compile(r"NR==(\d+)(?:\{print(?:\$0)?;?\})?")
# sed buyrug'i: [manzil[,manzil]]buyruq. Manzil son, `$` yoki `+N`.
SED_CMD_RE = re.compile(r"(?:(?<![\d$+])(\d+|\$)(?:,(\d+|\$|\+\d+))?)?([pdqQ=])")
SED_MAX_COMMANDS = 64
COUNT_RE = re.compile(r"([+-]?)(\d+)([a-zA-Z]{0,2})")
COUNT_UNITS = {"": 1, "b": 512, "k": 1024, "kb": 1000, "kib": 1024,
               "m": 1024 ** 2, "mb": 1000 ** 2, "g": 1024 ** 3, "gb": 1000 ** 3}
# PowerShell: o'qish fe'li va quvur cmdlet lari (registrga befarq).
PS_READERS = {"get-content", "gc", "type", "cat"}
PS_GC_VALUED = {"-path", "-literalpath", "-pspath", "-encoding", "-readcount",
                "-delimiter", "-stream", "-filter", "-include", "-exclude"}
PS_PATH_FLAGS = {"-path", "-literalpath", "-pspath"}
PS_HEAD_FLAGS = {"-totalcount", "-head", "-first"}
PS_TAIL_FLAGS = {"-tail", "-last"}
PS_SELECT = {"select-object", "select"}
PS_SMALL = {"select-string", "sls", "where-object", "where", "?", "findstr",
            "measure-object", "measure", "out-null", "out-file", "set-content",
            "add-content"}


def parse_count(value):
    """`40`, `+5`, `-5`, `300k` -> (ishora, son) yoki None."""
    match = COUNT_RE.fullmatch(value or "")
    if not match or match.group(3).lower() not in COUNT_UNITS:
        return None
    return match.group(1), int(match.group(2)) * COUNT_UNITS[match.group(3).lower()]


def clip_head(lines, size):
    """Boshidagi `size` bayt, satr tuzilishi bilan."""
    out, left = [], size
    for length in lines:
        if left <= 0:
            break
        out.append(min(length, left))
        left -= length
    return out


def clip_tail(lines, size):
    return clip_head(lines[::-1], size)[::-1]


def watched_args(args):
    """Argumentlardagi kuzatiladigan fayllar, tartib bilan, takrorsiz."""
    found = []
    for arg in args:
        for path in sorted(slurped(arg)):
            if path not in found:
                found.append(path)
    return found


def source(files):
    """Fayllardan oqim: (satrlar, fayllar) yoki None."""
    if not files:
        return None
    return [n for path in files for n in file_lines(path)], set(files)


def head_tail(args, tail):
    """(qism, ishora, son, fayl argumentlari). qism: 'n' satr yoki 'c' bayt.

    Son o'qilmasa (`-n $N`) son None: oqim butunligicha qoladi.
    """
    part, sign, count, files, i = "n", "", 10, [], 0
    while i < len(args):
        arg = args[i]
        i += 1
        value = None
        if arg == "--":
            files += args[i:]
            break
        if re.fullmatch(r"-\d+", arg):
            part, value = "n", arg[1:]
        elif tail and not files and re.fullmatch(r"\+\d+", arg):
            part, value = "n", arg
        elif arg in ("-n", "-c", "--lines", "--bytes"):
            part = "c" if arg in ("-c", "--bytes") else "n"
            value = args[i] if i < len(args) else ""
            i += 1
        elif arg[:2] in ("-n", "-c") and len(arg) > 2:
            part, value = arg[1], arg[2:]
        elif arg.startswith(("--lines=", "--bytes=")):
            part = "c" if arg.startswith("--bytes") else "n"
            value = arg.split("=", 1)[1]
        elif arg in ("-s", "--sleep-interval", "--pid", "--max-unchanged-stats"):
            i += 1
            continue
        elif arg.startswith("-") and arg != "-":
            continue
        else:
            files.append(arg)
            continue
        parsed = parse_count(value)
        sign, count = parsed if parsed else ("", None)
    return part, sign, count, files


def apply_head_tail(lines, part, sign, count, tail):
    if count is None:
        return lines
    if part == "c":
        if tail and sign == "+":
            return clip_tail(lines, max(sum(lines) - max(count - 1, 0), 0))
        if not tail and sign == "-":
            return clip_head(lines, max(sum(lines) - count, 0))
        return clip_tail(lines, count) if tail else clip_head(lines, count)
    if tail and sign == "+":
        return lines[max(count - 1, 0):]
    if not tail and sign == "-":
        return lines[:len(lines) - count] if count else lines
    if tail:
        return lines[len(lines) - count:] if count else []
    return lines[:count]


def stage_head_tail(args, stdin, tail):
    part, sign, count, names = head_tail(args, tail)
    files = watched_args(names)
    if files:   # har fayl alohida kesiladi
        out = [n for path in files
               for n in apply_head_tail(file_lines(path), part, sign, count, tail)]
        return out, set(files)
    if names or stdin is None:
        return None
    return apply_head_tail(stdin[0], part, sign, count, tail), stdin[1]


def sed_parts(args):
    """(jim, skript yoki None, fayl argumentlari, joyida). Skript None:
    `-f` bilan fayldan, ya'ni o'qib bo'lmaydi."""
    quiet = inplace = False
    scripts, names, i = [], [], 0
    while i < len(args):
        arg = args[i]
        i += 1
        if arg == "--":
            names += args[i:]
            break
        if arg in ("-n", "--quiet", "--silent"):
            quiet = True
        elif arg in ("-e", "--expression"):
            scripts.append(args[i] if i < len(args) else "")
            i += 1
        elif arg.startswith("--expression="):
            scripts.append(arg.split("=", 1)[1])
        elif arg in ("-f", "--file") or arg.startswith("--file="):
            return quiet, None, names, inplace
        elif arg.startswith("--in-place"):
            inplace = True
        elif arg in ("-l", "--line-length"):
            i += 1
        elif arg.startswith("--"):
            continue
        elif arg.startswith("-") and len(arg) > 1:
            flags = arg[1:]
            if flags.startswith("i"):
                inplace = True
                continue   # `-i.bak`: qolgani kengaytma
            quiet = quiet or "n" in flags
            inplace = inplace or "i" in flags
            if "f" in flags:
                return quiet, None, names, inplace
            if flags.endswith("e"):
                scripts.append(args[i] if i < len(args) else "")
                i += 1
        elif not scripts:
            scripts.append(arg)
        else:
            names.append(arg)
    return quiet, "\n".join(scripts), names, inplace


def sed_substitution(cmd):
    """`s/a/b/g`: satrni almashtiradi, sonini emas. `p` va `w` bayrog'i yo'q."""
    if len(cmd) < 4 or cmd[0] != "s" or cmd[1].isalnum() or cmd[1] in " \\\n":
        return False
    parts = cmd[2:].split(cmd[1])
    return len(parts) == 3 and not set(parts[2]) & set("pwe")


def sed_select(lines, quiet, script):
    """sed chiqishidagi satrlar. Raqamli manzil, p/d/q/Q/= va
    almashtirish tushuniladi; boshqasi (regex manzil, `y`, guruh) None,
    ya'ni filtr deb olinadi, `grep naqsh` kabi."""
    commands = []
    for raw in re.split(r"[;\n]", script):
        cmd = raw.replace(" ", "").replace("\t", "")
        if not cmd:
            continue
        match = SED_CMD_RE.fullmatch(cmd)
        if match:
            commands.append(match.groups())
        elif sed_substitution(cmd):
            continue
        else:
            return None
    if len(commands) > SED_MAX_COMMANDS:
        return None   # bunday skript o'qish emas, dastur
    last = len(lines)

    def address(value, start=0):
        if value == "$":
            return last
        if value.startswith("+"):
            return start + int(value[1:])
        return int(value)

    ranges = []
    for first, second, verb in commands:
        low = 1 if first is None else address(first)
        high = (last if first is None else
                max(low, address(second, low)) if second else low)
        ranges.append((low, high, verb))
    if not any(verb in "dqQ" for _, _, verb in ranges):
        out = [] if quiet else list(lines)
        for low, high, verb in ranges:
            part = lines[low - 1:high]
            out += part if verb == "p" else [len(str(high)) + 1] * len(part)
        return out
    out = []
    for number, length in enumerate(lines, 1):
        printed, stop = not quiet, False
        for low, high, verb in ranges:
            if not low <= number <= high:
                continue
            if verb == "p":
                out.append(length)
            elif verb == "=":
                out.append(len(str(number)) + 1)
            elif verb == "d":
                printed = False
                break
            else:
                printed = printed and verb == "q"
                stop = True
                break
        if printed:
            out.append(length)
        if stop:
            break
    return out


def stage_sed(args, stdin):
    quiet, script, names, inplace = sed_parts(args)
    if inplace or script is None:
        return None
    files = watched_args(names)
    flow = source(files) if files else (None if names else stdin)
    if flow is None:
        return None
    lines = sed_select(flow[0], quiet, script)
    return None if lines is None else (lines, flow[1])


def stage_grep(args, stdin):
    """`grep ''`, `grep ^` butun oqim; boshqa naqsh filtr (None)."""
    patterns, positional, small, invert, i = [], [], False, False, 0
    while i < len(args):
        arg = args[i]
        i += 1
        if arg == "--":
            positional += args[i:]
            break
        if arg.startswith("--"):
            key, _, value = arg[2:].partition("=")
            if key == "regexp":
                patterns.append(value if "=" in arg else (args[i] if i < len(args) else ""))
                i += "=" not in arg
            elif key == "file":
                return None
            elif key in GREP_LONG_SMALL:
                small = True
            elif key == "invert-match":
                invert = True
            elif key in GREP_LONG_VALUED and "=" not in arg:
                i += 1
            continue
        if arg.startswith("-") and len(arg) > 1:
            for at, flag in enumerate(arg[1:], 1):
                if flag in "ef" or flag in GREP_SHORT_VALUED:
                    value = arg[at + 1:]
                    if not value:
                        value = args[i] if i < len(args) else ""
                        i += 1
                    if flag == "f":
                        return None
                    if flag == "e":
                        patterns.append(value)
                    break
                small = small or flag in GREP_SMALL_FLAGS
                invert = invert or flag == "v"
            continue
        positional.append(arg)
    if not patterns:
        if not positional:
            return None
        patterns, positional = [positional[0]], positional[1:]
    if small or invert or not any(p in GREP_WHOLE for p in patterns):
        return None
    files = watched_args(positional)
    return source(files) if files else (None if positional else stdin)


def stage_awk(args, stdin):
    """`awk 1` va `awk '{print}'` butun oqim, `NR>=A&&NR<=B` oraliq."""
    program, names, i = None, [], 0
    while i < len(args):
        arg = args[i]
        i += 1
        if arg == "--":
            names += args[i:]
            break
        if arg in ("-F", "-v"):
            i += 1
        elif arg == "-f" or arg.startswith("-f"):
            return None
        elif arg.startswith("-") and len(arg) > 1:
            continue
        elif program is None:
            program = arg
        else:
            names.append(arg)
    if program is None:
        return None
    files = watched_args(names)
    flow = source(files) if files else (None if names else stdin)
    if flow is None:
        return None
    code = re.sub(r"\s+", "", program)
    lines = flow[0]
    if code in AWK_WHOLE:
        return flow
    match = AWK_RANGE_RE.fullmatch(code)
    if match:
        low = int(match.group(2)) + (match.group(1) == ">")
        high = int(match.group(4)) - (match.group(3) == "<")
        return lines[max(low - 1, 0):max(high, 0)], flow[1]
    match = AWK_LINE_RE.fullmatch(code)
    if match:
        number = int(match.group(1))
        return lines[number - 1:number] if number else [], flow[1]
    return None


def stage_bash(argv, stdin):
    name = os.path.basename(argv[0])
    args = argv[1:]
    if name in WHOLE_READERS:
        files = watched_args(a for a in args if a != "-")
        if not files:
            return None if [a for a in args if not a.startswith("-")] else stdin
        flow = source(files)
        if "-" in args and stdin is not None:
            flow = (stdin[0] + flow[0], stdin[1] | flow[1])
        return flow
    if name in ("head", "tail"):
        return stage_head_tail(args, stdin, name == "tail")
    if name == "sed":
        return stage_sed(args, stdin)
    if name in GREP_FAMILY:
        return stage_grep(args, stdin)
    if name in AWK_FAMILY:
        return stage_awk(args, stdin)
    if name in SMALL_OUTPUT:
        return None
    # Noma'lum buyruq (sort, tee, uniq): oqimni o'zgartirmaydi deb olinadi,
    # avvalgi `cat BIG | ...` to'sig'i kabi. Fayl argumenti esa uning
    # ishi, kontekstga tushishi noma'lum.
    return stdin


def ps_flag(arg):
    """`-TotalCount:80` -> ('-totalcount', '80'), `-Raw` -> ('-raw', None)."""
    name, colon, value = arg.partition(":")
    return name.lower(), (value if colon else None)


def stage_powershell(argv, stdin):
    name = argv[0].lower()
    args = argv[1:]
    if name in PS_READERS:
        names, cut, i = [], None, 0
        while i < len(args):
            flag, value = ps_flag(args[i])
            i += 1
            if not flag.startswith("-"):
                names.append(args[i - 1])
                continue
            if flag in PS_GC_VALUED | PS_HEAD_FLAGS | PS_TAIL_FLAGS and value is None:
                value = args[i] if i < len(args) else ""
                i += 1
            if flag in PS_PATH_FLAGS:
                names.append(value)
            elif flag in PS_HEAD_FLAGS | PS_TAIL_FLAGS:
                parsed = parse_count(value)
                cut = (flag in PS_TAIL_FLAGS, parsed[1] if parsed else None)
        files = watched_args(names)
        if not files:
            return None
        if cut is None:
            return source(files)
        tail, count = cut
        lines = [n for path in files
                 for n in apply_head_tail(file_lines(path), "n", "", count, tail)]
        return lines, set(files)
    if stdin is None or name in PS_SMALL:
        return None
    if name in PS_SELECT:
        lines, i = stdin[0], 0
        while i < len(args):
            flag, value = ps_flag(args[i])
            i += 1
            if flag in ("-first", "-last", "-skip") and value is None:
                value = args[i] if i < len(args) else ""
                i += 1
            parsed = parse_count(value) if flag in ("-first", "-last", "-skip") else None
            if parsed is None:
                continue
            count = parsed[1]
            if flag == "-skip":
                lines = lines[count:]
            else:
                lines = apply_head_tail(lines, "n", "", count, flag == "-last")
        return lines, stdin[1]
    return stdin


def unquote(word):
    return split_args(word)[0] if word.strip() else ""


def parse_stage(text, powershell):
    """(argv, kirish fayli, stdout faylga, stdin boshqa narsadan) yoki None."""
    text = text.strip()
    masked = mask_quoted(text)
    prefix = PREFIX_RE.match(masked)
    start = prefix.end() if prefix else 0
    infile, to_file, other_stdin = None, False, False
    pieces, last = [], start
    for match in REDIRECT_RE.finditer(masked, start):
        fd, op, dup, target = match.groups()
        pieces.append(text[last:match.start()])
        last = match.end()
        word = unquote(text[match.start(4):match.end(4)])
        if op.startswith("<<"):
            other_stdin = True
        elif op == "<":
            infile = word
        elif fd in (None, "1", "&") and not dup and word not in STDOUT_FILES:
            to_file = True
    pieces.append(text[last:])
    rest = " ".join(pieces)
    if powershell:
        # `docs\patterns\x.md` va vergul bilan bir nechta yo'l.
        argv = [w.strip("'\"") for w in rest.replace("\\", "/").replace(",", " ").split()]
    else:
        argv = split_args(rest)
    if not argv:
        return None
    return argv, infile, to_file, other_stdin


def pipelines(command):
    """Buyruq -> [[bosqich matni, ...], ...]. Heredoc tanasi matn, u olinadi."""
    base = strip_heredoc(command)
    masked = mask_quoted(base)
    out, stages, start = [], [], 0
    for match in SPLIT_RE.finditer(masked):
        stages.append(base[start:match.start()])
        start = match.end()
        if match.group(0) not in ("|", "|&"):
            out.append(stages)
            stages = []
    stages.append(base[start:])
    out.append(stages)
    return out


def read_volume(command, powershell=False):
    """(bayt, fayllar): buyruq kontekstga chiqaradigan kuzatiladigan bo'lak."""
    total, files = 0, set()
    for stages in pipelines(command):
        flow = None
        for text in stages:
            stage = parse_stage(text, powershell) if text.strip() else None
            if stage is None:
                flow = None
                continue
            argv, infile, to_file, other_stdin = stage
            stdin = None if other_stdin else flow
            if infile is not None:
                stdin = source(watched_args([infile]))
            flow = (stage_powershell if powershell else stage_bash)(argv, stdin)
            if to_file:
                flow = None
        if flow is not None:
            total += sum(flow[0])
            files |= flow[1]
    return total, sorted(files)


def check_reads(command, powershell=False):
    size, files = read_volume(command, powershell)
    if size > MAX_BYTES:
        deny("Bu buyruq %d KB qaytaradi (chegara %d KB): %s"
             % (size // 1000, MAX_BYTES // 1000,
                ", ".join(os.path.relpath(f, ROOT) for f in files[:3])))


# `budget.py --tiklash`: aktyor chegarasini ochadi. Nom so'z boshida:
# `xbudget.py` emas. Qo'shtirnoq ichidagi matn (commit xabari) niqoblanadi.
# Qidiruv keyingi `budget.py` dan o'tmaydi: takror nomli 10 KB kirishda
# kvadratik qaytish bo'lmasin.
BUDGET_RESET_RE = re.compile(r"(?<![\w.-])budget\.py['\"]?(?=\s)"
                             r"(?:(?!budget\.py)[^|;&\n])*?\s--tiklash(?![\w-])")
BUDGET_HINT = (
    "Budjet aktyorni bitta vazifada 2 marta chaqirishga ruxsat beradi.\n"
    "Tiklash chaqiruv behuda ketganda o'rinli (aktyor boshqa sababdan\n"
    "yiqildi yoki foydalanuvchi to'xtatdi). Aks holda uchinchi urinish\n"
    "o'rniga sababni ayting. Holat: {budget} --holat")


def check_budget_reset(command):
    match = BUDGET_RESET_RE.search(mask_quoted(strip_heredoc(command)))
    if match:
        ask("Aktyor budjetini qo'lda tiklash: %s." % match.group(0).strip(), BUDGET_HINT)


def check_bash(tool_input, powershell=False):
    """Avval deny lar, keyin ask lar: ruxsat deny ni ochib yubormasin."""
    command = tool_input.get("command") or ""
    check_java_write(command)
    asks = check_build(command)
    check_reads(command, powershell)
    check_memory_git(command)
    check_commit_message(command)
    check_cost(command)
    check_budget_reset(command)
    for reason, hint in asks:
        ask(reason, hint)


def main():
    payload = hookio.read_payload()
    if payload is None:
        return  # hook hech qachon chaqiruvni o'z xatosi tufayli to'smaydi
    if not hookio.active(payload):
        return  # Java proyekti ham, klon ham emas: to'siq o'rinsiz
    global IN_SUBAGENT
    IN_SUBAGENT = bool(payload.get("agent_id"))
    tool_input = payload.get("tool_input") or {}
    name = payload.get("tool_name")
    if name == "Read":
        check_read(tool_input)
    elif name in ("Bash", "PowerShell"):
        check_bash(tool_input, powershell=name == "PowerShell")


if __name__ == "__main__":
    main()
