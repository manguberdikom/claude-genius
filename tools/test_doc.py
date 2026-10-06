#!/usr/bin/env python3
"""doc.sh buyruqlari uchun sinovlar.

    python3 tools/test_doc.py

Qidiruv sifatini eval_find.py o'lchaydi; bu yerda buyruqlarning o'zi
tekshiriladi: to'g'ri javob, to'g'ri xato, to'g'ri chiqish kodi.
Indeksning eskirishi tools va docs nusxasida sinaladi, haqiqiy index/
ga tegilmaydi.
"""

import os
import re
import shutil
import subprocess
import sys
import tempfile
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOC = os.path.join(ROOT, "tools", "doc.sh")
INDEX = os.path.join(ROOT, "index")
# Windows .sh ni o'zi yurgiza olmaydi (WinError 193), bash orqali beriladi.
# Yalang `bash` ni CreateProcess PATH dan oldin System32 dan qidiradi (u
# yerdagisi WSL), which esa PATH tartibida: Git Bash da Git ning bash'i.
BASH = shutil.which("bash") or "bash"
SHELL = [BASH] if os.name == "nt" else []


def clean_env(**extra):
    """Shell dagi DOC_MAX_LINES/DOC_MAX_BYTES show chegarasini o'zgartirib,
    chalg'ituvchi xato bermasin."""
    env = {k: v for k, v in os.environ.items() if not k.startswith("DOC_MAX_")}
    env.update(extra)
    return env


def run(*args, doc=DOC, env=None):
    # doc.sh UTF-8 yozadi, locale kod sahifasi (cp1251) emas.
    return subprocess.run(SHELL + [doc] + list(args), capture_output=True,
                          encoding="utf-8", cwd=os.path.dirname(os.path.dirname(doc)),
                          env=clean_env() if env is None else env)


# (nom, argumentlar, kutilgan chiqish kodi, chiqishga shart)
# Shart: "" - tekshirilmaydi; "^..." - regex stdout ning BIRINCHI
# qatoriga; "!..." - bu matn stdout da bo'lmasligi kerak; aks holda
# matn stdout ning istalgan joyida bo'lishi kerak.
CASES = [
    # Sonar kaliti: uchala yozilish shakli ham bir xil javob berishi kerak.
    ("rule to'liq shakl", ["rule", "java:S2095"], 0, "try-with-resources"),
    ("rule S bilan", ["rule", "S2095"], 0, "try-with-resources"),
    ("rule faqat raqam", ["rule", "2095"], 0, "try-with-resources"),
    ("rule kichik harf", ["rule", "java:s2095"], 0, "try-with-resources"),
    # Reyting: tushuntirgan bo'lim yuqorida turishi kerak, shunchaki
    # tilga olgan katalog qatori emas. S3776 da birinchi qator bo'lim
    # (raqamida nuqta bor) va ulushi 1 dan kam emas yoki `qoida` (katalog
    # bo'limining birinchi qatori): katalog bobi (29, ulush 0.20) yuqoriga
    # chiqsa yiqiladi.
    ("rule S106 loglash", ["rule", "java:S106"], 0, r"^sonarqube +41\.7 "),
    ("rule S3776 bo'lim yuqorida", ["rule", "java:S3776"], 0,
     r"^sonarqube +\d+\.\d+ +(qoida|[1-9])"),
    ("rule uzun ro'yxat qisqa", ["rule", "java:S3776"], 0, "rule --all"),
    ("rule --all to'liq", ["rule", "--all", "java:S3776"], 0, "!... yana"),
    # Bob darajasidagi qator (katalog jadvali) butun bob emas, outline.
    ("rule katalog belgisi", ["rule", "java:S2259"], 0, "[katalog: outline]"),
    # Katalog bobi bali past bo'lsa ham qisqa ro'yxatda: S3776 da 29-o'rin.
    ("rule katalog doim ko'rinadi", ["rule", "java:S3776"], 0, "\nsonarqube   27 "),
    # Katalog bo'limining birinchi qatori "Qoida: `java:S1192`": tuzatish
    # retsepti ulushi baland tushuntirish bo'limidan (3.10) oldin.
    ("rule S1192 katalog bo'limi", ["rule", "S1192"], 0, r"^sonarqube +27\.8 "),
    ("rule S3776 katalog bo'limi", ["rule", "S3776"], 0, r"^sonarqube +27\.1 "),
    # Avval bo'lim qatori umuman yo'q edi, faqat bob jadvali.
    ("rule S1488 bo'limi bor", ["rule", "S1488"], 0, r"^sonarqube +27\.10 "),
    ("rule yo'q kalit", ["rule", "S99999"], 1, ""),
    ("rule raqamsiz", ["rule", "abc"], 1, ""),

    # Tekshiruv punktlari.
    ("checklist bo'lim", ["checklist", "patterns", "17.43"], 0, "timeout"),
    ("checklist bob", ["checklist", "sonarqube", "13"], 0, "- [ ]"),
    ("checklist hujjat: sanoq", ["checklist", "clean-code"], 0, "punkt"),
    ("checklist hujjat: punktsiz", ["checklist", "clean-code"], 0, "!- [ ]"),
    ("checklist --all", ["checklist", "--all", "clean-code"], 0, "- [ ]"),
    ("checklist X.10", ["checklist", "clean-code", "1.10"], 0, r"^1\.10$"),
    ("checklist yo'q bo'lim", ["checklist", "patterns", "99.99"], 1, ""),
    ("checklist yo'q hujjat", ["checklist", "yoq"], 1, ""),

    # find.
    ("find taxallus", ["find", "circuit breaker"], 0, "17.2"),
    ("find topilmadi", ["find", "zzqwertyuiop"], 1, ""),
    # Natija 64 KB dan katta: head bilan printf SIGPIPE olib 141 berardi.
    ("find ko'p natija", ["find", "-f", "spring"], 0, ""),
    # Faqat matnda bor atama: taxallus qidiruvi topmaydi, grep topishi shart.
    ("find -f matn ichidan", ["find", "-f", "testCreate1"], 0, r"^architect +4\.10 "),
    ("find -n manfiy", ["find", "-n", "-5", "va"], 1, ""),
    ("find -n nol", ["find", "-n", "0", "va"], 1, ""),
    ("find unicode apostrof", ["find", "oʻzgarmas"], 0, "4.16"),
    ("find -- bilan", ["find", "--", "-Xmx"], 0, "10.7"),
    # Ishora-yozuv to'liq yozuv raqamini ko'rsatadi.
    ("find ishora-yozuv", ["find", "memoizatsiya"], 0, "[ishora: 11.17]"),
    ("find bo'sh so'rov", ["find", " "], 1, ""),
    # Daraja: aniq moslik > butun so'z > so'z boshi > so'z ichida.
    # So'z ichidagi moslik qoladi, faqat pastga tushadi.
    ("find aniq moslik birinchi", ["find", "State"], 0, r"^patterns +3\.8 "),
    ("find kesh: Bikeshedding emas", ["find", "kesh"], 0, r"^(?!.*Bikeshed)"),
    ("find Pact: Compacted emas", ["find", "Pact"], 0, r"^testing +9\.9 "),
    ("find so'z ichidagisi qoladi", ["find", "-n", "100", "Lock"], 0, "ReentrantLock"),
    # Ko'p so'zli so'rov: ibora yo'q bo'lsa so'zlar bo'yicha (findlib.py).
    ("find so'zlar: optimistic locking", ["find", "optimistic locking"], 0,
     "18.8 Optimistik"),
    ("find so'zlar: transaction propagation", ["find", "transaction propagation"],
     0, r"^architect +19\.2 "),
    ("find so'zlar: thread safety", ["find", "thread safety"], 0, r"^architect +11\.7 "),
    ("find so'zlar: hech biri yo'q", ["find", "zzqwerty yyqwerty"], 1, ""),
    # Bitta so'zli inglizcha so'rov: transliteratsiya va inglizcha jadval.
    ("find tion -> tsiya", ["find", "-n", "60", "serialization"], 0, "Serializatsiya"),
    ("find ic -> ik", ["find", "optimistic"], 0, "18.8 Optimistik"),
    ("find jadval: isolation", ["find", "-n", "60", "isolation"], 0, "izolyatsiya"),
    # Uy-bob (docs/OWNERS.tsv): naqshga to'liq mos so'rovda birinchi,
    # o'zbekcha shakl bilan ham. 12 mavzuning hammasi check_owner_homes da.
    ("find uy-bob belgisi", ["find", "n+1"], 0, r"^architect +18\.4 .*\[uy-bob\]$"),
    ("find uy-bob: o'zbekcha", ["find", "ichki metod chaqiruvi"], 0,
     r"^architect +19\.6 .*\[uy-bob\]$"),
    ("find uy-bob: sehrli son", ["find", "sehrli son"], 0, r"^patterns +25\.8 "),
    ("find uy-bob: optimistik lock", ["find", "optimistik lock"], 0,
     r"^patterns +9\.23 .*\[uy-bob\]$"),
    # Uy-bobdan keyin boshqa hujjatlar ham qoladi (so'zlar bo'yicha).
    ("find uy-bob va 18.8", ["find", "optimistic locking"], 0, "18.8 Optimistik"),
    # Qisman moslik: ortiqcha so'z mavzuni toraytiradi, aniq natija oldin.
    ("find uy-bob qisman", ["find", "N+1 testda"], 0, r"^testing +7\.5 "),
    ("find taxallus oldin, uy-bob keyin", ["find", "Idempotent Consumer"], 0,
     r"^patterns +14\.18 "),
    # Naqsh "equals hashCode" ni emas, entity ni talab qiladi.
    ("find equals hashCode: uy emas", ["find", "equals hashCode"], 0, "![uy-bob]"),
    # docs/<hujjat>/aliases.tsv: avval "topilmadi" yoki begona birinchi.
    ("find taxallus: pool size", ["find", "connection pool size"], 0,
     r"^architect +27\.6 "),
    ("find taxallus: Optional field", ["find", "Optional field"], 0,
     r"^clean-code +25\.1 "),
    ("find taxallus: deadlock detection", ["find", "deadlock detection"], 0,
     r"^architect +22\.8 "),
    ("find taxallus: long method", ["find", "long method"], 0, r"^clean-code +32\.3 "),
    # synonyms.tsv [inglizcha]: entity -> entitet.
    ("find jadval: entity", ["find", "-n", "60", "entity"], 0, "28.1 Entitet"),

    # show va path: X.10 X.1 ga tushmasin (awk son solishtirsa 24.10 == 24.1).
    ("show bo'lim", ["show", "patterns", "17.2"], 0, "Circuit Breaker"),
    ("show X.10", ["show", "patterns", "24.10"], 0, r"^## 24\.10 "),
    ("show testing 5.10", ["show", "testing", "5.10"], 0, r"^## 5\.10 "),
    ("show testing 5.1", ["show", "testing", "5.1"], 0, r"^## 5\.1 "),
    ("show 14.30 14.3 emas", ["show", "patterns", "14.30"], 0, r"^## 14\.30 "),
    ("show 21.10 21.1 emas", ["show", "patterns", "21.10"], 0, r"^## 21\.10 "),
    ("show kichik bob", ["show", "clean-code", "43"], 0, r"^# 43\. "),
    ("show bob nol bilan", ["show", "clean-code", "01"], 0, r"^# 1\. "),
    ("show katta bob to'siladi", ["show", "patterns", "25"], 1, "25.1"),
    # 1097 satr, lekin 138 KB: satr chegarasidan o'tadi, bayt chegarasidan emas.
    ("show bayt chegarasi", ["show", "patterns", "23"], 1, "23.1"),
    ("show bob.* bob kabi", ["show", "patterns", "23.*"], 1, "23.1"),
    ("show --force", ["show", "--force", "patterns", "23"], 0, r"^# 23\. "),
    ("path anchor", ["path", "patterns", "17.2"], 0, "#172-"),
    ("path X.10", ["path", "sonarqube", "29.10"], 0, "#2910-"),
    ("path 14.30", ["path", "patterns", "14.30"], 0, "#1430-"),
    ("toc", ["toc"], 0, "patterns"),
    ("outline", ["outline", "testing", "8"], 0, "8.1"),
    ("outline nol bilan", ["outline", "patterns", "017"], 0, "17.1 "),
]


def matches(needle, out):
    if not needle:
        return True
    if needle.startswith("^"):
        return re.search(needle, out.split("\n", 1)[0]) is not None
    if needle.startswith("!"):
        return needle[1:] not in out
    return needle in out


def read_index(name):
    with open(os.path.join(INDEX, name), encoding="utf-8") as handle:
        handle.readline()
        return [line.rstrip("\n").split("\t") for line in handle]


def check_exact_refs():
    """Har X.10, X.20 bo'lim o'zining anchorini, punktlarini beradi.

    Bitta holat emas, butun sinf: indeksdagi nol bilan tugaydigan har
    bo'lim uchun `path` indeksdagi anchorga teng, `checklist X.1` esa
    X.10 punktlarini qo'shmaydi.
    """
    bad = []
    for row in read_index("sections.tsv"):
        doc, num = row[0], row[1]
        if not re.search(r"\.\d*0$", num):
            continue
        out = run("path", doc, num).stdout.split("\n")
        if len(out) < 2 or out[1] != "%s#%s" % (row[4], row[7]):
            bad.append("path %s %s" % (doc, num))
    twins = {(r[0], r[2].rstrip("0")) for r in read_index("checklist.tsv")
             if re.search(r"\.\d*0$", r[2])}
    for doc, num in sorted(twins):
        heads = {line for line in run("checklist", doc, num).stdout.split("\n")
                 if line and not line.startswith(" ")}
        if heads - {num}:
            bad.append("checklist %s %s" % (doc, num))
    return not bad, ", ".join(bad[:5])


def check_find_hint():
    """'Kengroq qidirish' maslahati apostrofli so'rovda ham buyruq bo'lib qoladi."""
    # Ikkala so'z ham hech qayerda yo'q: so'zlar bo'yicha qidiruv ham bo'sh.
    proc = run("find", "zzqo'shimcha zzqwerty")
    hint = [l for l in proc.stderr.split("\n") if l.startswith("kengroq")]
    if not hint:
        return False, "maslahat yo'q"
    command = hint[0].split(": ", 1)[1]
    ok = subprocess.run([BASH, "-n", "-c", command],
                        capture_output=True).returncode == 0
    return ok, "" if ok else command


def check_bash32():
    """macOS dagi bash 3.2 da ishlamaydigan sintaksis yo'q.

    CI da bash 3.2 yo'q, shuning uchun ikki ma'lum tuzoq matndan
    tekshiriladi: kichik/katta harf kengaytmasi va buyruq o'rni ichidagi
    izoh (bash 3.2 undagi qavs va apostrofni sintaksis deb o'qiydi).
    """
    with open(DOC, encoding="utf-8") as handle:
        lines = handle.read().split("\n")
    bad = []
    inside = False
    for lineno, line in enumerate(lines, 1):
        text = line.strip()
        if re.search(r"\$\{[^}]*(,,|\^\^)[^}]*\}", line):
            bad.append("%d: harf kengaytmasi" % lineno)
        if inside and text.startswith(")"):
            inside = False
        elif inside and text.startswith("#"):
            bad.append("%d: $( ) ichida izoh" % lineno)
        if text.endswith("$("):
            inside = True
    return not bad, ", ".join(bad)


def check_find_rank():
    """Taxallus ko'p bo'lsa ham backtick ichidagi aniq nom yuqorida.

    `find Transactional` da avval 10 ta patterns taxallusi oldinda edi,
    architect 19.1 (`@Transactional` qanday ishlaydi) 12-o'rinda.
    """
    rows = [line.split()[:2] for line in run("find", "Transactional").stdout.split("\n")
            if line.strip()]
    keys = ["%s %s" % tuple(r) for r in rows if len(r) == 2]
    ok = "architect 19.1" in keys[:5]
    return ok, "" if ok else "19.1 o'rni: %s" % (
        keys.index("architect 19.1") + 1 if "architect 19.1" in keys else "yo'q")


def owner_rows():
    """docs/OWNERS.tsv: (mavzu, uy_bob) ro'yxati."""
    out, header = [], None
    with open(os.path.join(ROOT, "docs", "OWNERS.tsv"), encoding="utf-8") as handle:
        for line in handle:
            line = line.rstrip("\n")
            if not line.strip() or line.startswith("#"):
                continue
            parts = line.split("\t")
            if header is None:
                header = parts
                continue
            out.append((parts[0], parts[1]))
    return out


def check_owner_homes():
    """OWNERS dagi har mavzu `find` da uy-bobni top-3 da beradi.

    Avval 12 mavzudan 6 tasida uy-bob 1-o'rinda edi, 3 tasi "topilmadi".
    """
    bad = []
    rows = owner_rows()
    for topic, home in rows:
        out = run("find", "-n", "3", topic).stdout
        keys = [" ".join(line.split()[:2]) for line in out.split("\n") if line.strip()]
        if home not in keys:
            bad.append("%s -> %s" % (topic, ", ".join(keys) or "topilmadi"))
    return not bad and len(rows) >= 12, "; ".join(bad) or "%d qator" % len(rows)


def check_translit_same():
    """doc.sh (awk) va findlib.py (Python) transliteratsiyasi bir xil."""
    sys.path.insert(0, os.path.join(ROOT, "tools"))
    import findlib
    words = ("migration", "replication", "serialization", "optimistic",
             "configuration", "version", "transaction", "lock")
    with open(DOC, encoding="utf-8") as handle:
        text = handle.read()
    begin = text.index("BEGIN {", text.index("name_hits()"))
    last = "if (t != q) v[++nv] = t"
    rules = text[begin:text.index(last, begin) + len(last)] + "\n} }\n"
    bad = []
    for word in words:
        proc = subprocess.run(["awk", "-v", "q=" + word,
                               rules + 'END { print (t == "" ? q : t) }'],
                              capture_output=True, encoding="utf-8", stdin=subprocess.DEVNULL)
        awk_out = proc.stdout.strip()
        want = findlib.translit(word) or word
        if awk_out != want:
            bad.append("%s: awk %s, python %s" % (word, awk_out, want))
    return not bad, "; ".join(bad)


def check_posix_awk():
    """doc.sh awk qismida gawk kengaytmasi va regex interval yo'q.

    mawk (Debian/Ubuntu standarti) va macOS BWK awk ularni bilmaydi:
    IGNORECASE jim e'tiborsiz qoladi, gensub esa sintaksis xatosi.
    """
    with open(DOC, encoding="utf-8") as handle:
        lines = handle.read().split("\n")
    bad = []
    for lineno, line in enumerate(lines, 1):
        if re.search(r"\b(gensub|IGNORECASE|asorti?|strftime|systime|PROCINFO|"
                     r"patsplit|BEGINFILE|ENDFILE)\b", line):
            bad.append("%d: gawk kengaytmasi" % lineno)
        if re.search(r"(?:~|match\(|sub\(|split\()[^#]*/[^/]*\{\d+(,\d*)?\}[^/]*/", line):
            bad.append("%d: regex interval" % lineno)
    return not bad, ", ".join(bad)


def sandbox():
    """tools va docs nusxasi, indekssiz. copytree mtime ni saqlaydi."""
    tmp = tempfile.mkdtemp(prefix="test_doc_")
    shutil.copytree(os.path.join(ROOT, "docs"), os.path.join(tmp, "docs"))
    shutil.copytree(os.path.join(ROOT, "tools"), os.path.join(tmp, "tools"),
                    ignore=shutil.ignore_patterns("__pycache__", "testdata"))
    return tmp


def check_index_freshness():
    """Yarim indeks, eski indeks va build_index.py o'zgarishi seziladi.

    Indeks fayllari atomik yoziladi (*.tmp qolmaydi), .stamp vaqti build
    boshlangan payt (fayllardan keyin emas), docref ham eskirishni ko'radi.
    """
    tmp = sandbox()
    doc = os.path.join(tmp, "tools", "doc.sh")
    idx = os.path.join(tmp, "index")
    stamp = os.path.join(idx, ".stamp")

    def rebuilt():
        proc = run("toc", doc=doc)
        return proc.returncode == 0 and "index:" in proc.stderr

    def age_stamp():
        old = time.time() - 60
        os.utime(stamp, (old, old))

    steps = []
    try:
        steps.append(("indeks yo'q", rebuilt()))
        names = os.listdir(idx)
        steps.append(("*.tmp qolmadi", not [n for n in names if n.endswith(".tmp")]))
        first = min(os.path.getmtime(os.path.join(idx, n))
                    for n in names if n.endswith(".tsv"))
        steps.append((".stamp vaqti build boshi", os.path.getmtime(stamp) <= first))
        steps.append(("yangi indeks qayta yasalmaydi", not rebuilt()))
        age_stamp()
        os.utime(os.path.join(tmp, "tools", "build_index.py"), None)
        steps.append(("build_index.py o'zgardi", rebuilt()))
        os.remove(stamp)
        steps.append((".stamp yo'q", rebuilt()))
        os.remove(os.path.join(idx, "rules.tsv"))
        steps.append(("rules.tsv yo'q", rebuilt()))
        age_stamp()
        os.utime(os.path.join(tmp, "docs", "manifest.json"), None)
        before = os.path.getmtime(stamp)
        subprocess.run([sys.executable, "-c",
                        "import sys; sys.path.insert(0, 'tools'); "
                        "import docref; docref.by_rule('java:S106')"],
                       cwd=tmp, capture_output=True, timeout=120)
        steps.append(("docref eskirganni yasaydi",
                      os.path.getmtime(stamp) > before))
    except OSError as error:   # masalan .stamp umuman yasalmadi
        steps.append(("istisno: %s" % error, False))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    failed = [name for name, ok in steps if not ok]
    return not failed, ", ".join(failed)


def check_python_stub():
    """PATH dagi birinchi python3 Windows stub'i bo'lsa ham rebuild ishlaydi.

    WindowsApps stub'i PATH da bor, lekin hech narsa yurgizmaydi. doc.sh
    Python ni nom bo'yicha emas, ishga tushirib tanlaydi: avval
    GENIUS_PYTHON, keyin python3, python, py. Hech biri ishlamasa aniq xabar.
    """
    tmp = sandbox()
    doc = os.path.join(tmp, "tools", "doc.sh")
    stubs = os.path.join(tmp, "stubs")
    os.makedirs(stubs)

    def put(name, body):
        path = os.path.join(stubs, name)
        with open(path, "w", encoding="utf-8") as handle:
            handle.write("#!/bin/sh\n%s\n" % body)
        os.chmod(path, 0o755)

    for name in ("python3", "python", "py"):
        put(name, "echo 'Python was not found; run without arguments to "
                  "install from the Microsoft Store' >&2\nexit 49")
    env = clean_env(PATH=stubs + os.pathsep + os.environ.get("PATH", ""))
    env.pop("GENIUS_PYTHON", None)

    def rebuilt(proc):
        return proc.returncode == 0 and "index:" in proc.stderr

    steps = []
    try:
        proc = run("toc", doc=doc, env=env)
        steps.append(("hammasi stub: aniq xabar", proc.returncode == 1
                      and "ishlaydigan Python topilmadi" in proc.stderr))
        proc = run("toc", doc=doc, env=dict(env, GENIUS_PYTHON=sys.executable))
        steps.append(("GENIUS_PYTHON", rebuilt(proc)))
        shutil.rmtree(os.path.join(tmp, "index"))
        put("python", 'exec "%s" "$@"' % sys.executable)
        steps.append(("python3 stub birinchi", rebuilt(run("toc", doc=doc, env=env))))
    except OSError as error:
        steps.append(("istisno: %s" % error, False))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    failed = [name for name, ok in steps if not ok]
    return not failed, ", ".join(failed)


def check_byte_limit():
    """doc.sh show va guard.py Read chegarasi bitta qiymat.

    Avval 20000 va 16000 edi: 16-20 KB lik bob show bilan butun chiqar,
    xuddi shu oraliqni Read qilish esa to'silardi.
    """
    with open(os.path.join(ROOT, "tools", "doc.sh"), encoding="utf-8") as h:
        sh = re.search(r"DOC_MAX_BYTES:-(\d+)", h.read())
    with open(os.path.join(ROOT, "tools", "guard.py"), encoding="utf-8") as h:
        py = re.search(r"\"DOC_MAX_BYTES\", \"(\d+)\"", h.read())
    if not sh or not py:
        return False, "standart qiymat topilmadi"
    return sh.group(1) == py.group(1), "doc.sh %s, guard.py %s" % (sh.group(1), py.group(1))


CHECKS = [
    ("show va Read chegarasi teng", check_byte_limit),
    ("X.10 butun sinf", check_exact_refs),
    ("find maslahati apostrofda", check_find_hint),
    ("bash 3.2 sintaksisi", check_bash32),
    ("find Transactional: 19.1 top-5", check_find_rank),
    ("OWNERS: uy-bob top-3 da", check_owner_homes),
    ("transliteratsiya awk = Python", check_translit_same),
    ("awk: gawk kengaytmasi yo'q", check_posix_awk),
    ("indeks eskirishi", check_index_freshness),
    ("python3 stub PATH da", check_python_stub),
]


def main():
    # Argumentdagi `ʻ` Windows quvuridagi kod sahifasida yo'q.
    sys.stdout.reconfigure(encoding="utf-8")
    failures = 0
    for name, args, want_code, needle in CASES:
        proc = run(*args)
        hit = matches(needle, proc.stdout)
        ok = proc.returncode == want_code and hit
        failures += not ok
        detail = ""
        if not ok:
            detail = "  (kod=%d, kutilgan=%d%s)" % (
                proc.returncode, want_code, "" if hit else ", matn mos emas")
        print("%-4s %-28s %s%s" % ("OK" if ok else "XATO", name,
                                   " ".join(args)[:34], detail))

    for name, check in CHECKS:
        ok, detail = check()
        failures += not ok
        print("%-4s %-28s %s" % ("OK" if ok else "XATO", name,
                                 "" if ok else "(%s)" % detail))

    total = len(CASES) + len(CHECKS)
    print("\n%d/%d o'tdi" % (total - failures, total))
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
