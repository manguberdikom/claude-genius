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

3. Test vaqti. To'liq suite (`./gradlew test`, `mvn verify`) 5-8 daqiqa,
   `clean`, `--rerun-tasks` va `--no-daemon` esa inkremental build va
   daemon ni yo'qotib, keyingi har yurishni ham sekinlashtiradi. Bular
   ham `deny`: arzon yo'l har doim bir xil (`run_tests.py`), u
   maqsadli, modul va to'liq rejimni ham beradi. `ask` bo'lsa zanjir
   har safar odamni kutib to'xtardi, holbuki bu yerda qaror yo'q.
   Filtrli yurish (`--tests`, `-Dtest=`) va testsiz build (`-x test`,
   `-DskipTests`) o'tadi.

Chegaralangan o'qish o'tadi: kichik bo'lakli Read, sed oralig'i, grep, head,
`Get-Content -TotalCount`. Tashxis buyruqlari ham o'tadi: docker ps,
docker logs, docker images, psql --version.

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

# Faylni boshdan oxirigacha oqizadigan buyruqlar. Argumentlar oralig'ida
# '>' bo'lishi mumkin emas: shunda `cat > fayl <<EOF ...` kabi YOZISH
# buyrug'i noto'g'ri to'silmaydi.
SLURP_RE = re.compile(CMD + r"(?:cat|bat|less|more|most|view|tac|nl)\s+([^|;&\n>]*)")
# PowerShell da o'qish fe'li registrga befarq; `cat` va `type` ham
# Get-Content taxallusi. Bash da `type` faylni o'qimaydi, shuning uchun bu
# naqsh faqat PowerShell asbobiga qo'llanadi.
PS_SLURP_RE = re.compile(CMD + r"(?:get-content|gc|type|cat)\s+([^|;&\n>]*)", re.I)
# Get-Content ning satr chegarasi (First va Head TotalCount taxallusi,
# Last esa Tail taxallusi): bo'lak cheklangan, o'qish o'tadi.
PS_BOUNDED_RE = re.compile(r"(?:^|\s)-(?:TotalCount|Head|Tail|First|Last)\b", re.I)

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


def build_problem(tool, args):
    """(nima, nega) yoki None. tool: gradle yoki maven."""
    words, i = [], 0
    filtered = skipped = False
    while i < len(args):
        arg = args[i]
        if arg in ("--rerun-tasks", "--no-daemon") or arg == "-Dorg.gradle.daemon=false":
            return (arg, "%s inkremental build va daemon ni yo'qotadi: keyingi har "
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
    if any(w == "clean" or w.endswith(":clean") for w in words):
        return ("clean", "clean inkremental build ni o'chiradi: keyingi har yurish "
                         "hammasini qaytadan kompilyatsiya qiladi. Gradle va Maven "
                         "o'zgargan faylni o'zi kuzatadi; build holati haqiqatan "
                         "buzilgan bo'lsa, buni foydalanuvchiga ayting")
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
        return ("filtrsiz test: %s" % " ".join(runs), why)
    return None


def check_build(command):
    """Buyruq o'rni qo'shtirnoqsiz matndan topiladi (`grep 'gradle test'`
    chaqiruv emas), argumentlar esa asl matndan o'qiladi: `-Dtest='A,B'`
    filtri bo'shatilsa, maqsadli yurish filtrsiz deb to'silardi.
    strip_quoted uzunlikni saqlaydi, shuning uchun oraliq bir xil."""
    base = strip_heredoc(command)
    wipes = []
    for match in BUILD_RE.finditer(strip_quoted(base)):
        exe = os.path.basename(match.group(1).replace("\\", "/")).lower()
        tool = "gradle" if exe.startswith("gradle") else "maven"
        # `(cd app && ./gradlew test)`: subshell qavsi argument emas.
        args = split_args(base[match.start(2):match.end(2)].rstrip().rstrip(")`"))
        problem = build_problem(tool, args)
        if problem:
            what, why = problem
            decide("deny", "Test vaqti: %s.\n%s." % (what, why), BUILD_HINT)
        wipes += [a for a in args if a in DB_WIPE_TASKS]
    # deny dan keyin: to'liq suite ham bo'lsa, ruxsat uni ochib yubormasin.
    if wipes:
        ask("Jonli bazani o'chiradi: %s." % ", ".join(wipes), DB_WIPE_HINT)


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


def slice_bytes(path, offset=None, limit=None):
    """Read qaytaradigan bo'lakning bayt hajmi: offset dan limit satr."""
    start = max(offset if isinstance(offset, int) else 1, 1) - 1
    stop = start + (limit if isinstance(limit, int) and limit > 0 else READ_DEFAULT_LINES)
    total = 0
    try:
        with open(path, "rb") as handle:
            for number, line in enumerate(handle):
                if number >= stop:
                    break
                if number >= start:
                    total += len(line)
    except OSError:
        return 0
    return total


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


def check_bash(tool_input, powershell=False):
    command = tool_input.get("command") or ""
    check_java_write(command)
    check_cost(command)
    check_build(command)
    regex = PS_SLURP_RE if powershell else SLURP_RE
    for match in regex.finditer(strip_heredoc(command)):
        args = match.group(1)
        if powershell:
            if PS_BOUNDED_RE.search(args):
                continue
            # `docs\patterns\x.md` va vergul bilan bir nechta yo'l.
            args = args.replace("\\", "/").replace(",", " ")
        files = sorted({f for arg in args.split() for f in slurped(arg)})
        size = sum(os.path.getsize(f) for f in files)
        if size > MAX_BYTES:
            deny("Bu buyruq %d KB ni butunligicha oqizadi: %s"
                 % (size // 1000, ", ".join(os.path.relpath(f, ROOT) for f in files[:3])))


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
