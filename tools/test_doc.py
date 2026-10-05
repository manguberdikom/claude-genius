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


def run(*args, doc=DOC):
    return subprocess.run([doc] + list(args), capture_output=True,
                          text=True, cwd=os.path.dirname(os.path.dirname(doc)))


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
    # (raqamida nuqta bor) va ulushi 1 dan kam emas: katalog bobi
    # (29, ulush 0.20) yuqoriga chiqsa yiqiladi.
    ("rule S106 loglash", ["rule", "java:S106"], 0, r"^sonarqube +41\.7 "),
    ("rule S3776 bo'lim yuqorida", ["rule", "java:S3776"], 0,
     r"^sonarqube +\d+\.\d+ +[1-9]"),
    ("rule uzun ro'yxat qisqa", ["rule", "java:S3776"], 0, "rule --all"),
    ("rule --all to'liq", ["rule", "--all", "java:S3776"], 0, "!... yana"),
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
    ("find -n manfiy", ["find", "-n", "-5", "va"], 1, ""),
    ("find -n nol", ["find", "-n", "0", "va"], 1, ""),
    ("find unicode apostrof", ["find", "oʻzgarmas"], 0, "4.16"),
    ("find -- bilan", ["find", "--", "-Xmx"], 0, "10.7"),
    ("find bo'sh so'rov", ["find", " "], 1, ""),

    # show va path: X.10 X.1 ga tushmasin (awk son solishtirsa 24.10 == 24.1).
    ("show bo'lim", ["show", "patterns", "17.2"], 0, "Circuit Breaker"),
    ("show X.10", ["show", "patterns", "24.10"], 0, r"^## 24\.10 "),
    ("show kichik bob", ["show", "clean-code", "43"], 0, r"^# 43\. "),
    ("show bob nol bilan", ["show", "clean-code", "01"], 0, r"^# 1\. "),
    ("show katta bob to'siladi", ["show", "patterns", "25"], 1, "25.1"),
    # 1097 satr, lekin 138 KB: satr chegarasidan o'tadi, bayt chegarasidan emas.
    ("show bayt chegarasi", ["show", "patterns", "23"], 1, "23.1"),
    ("show bob.* bob kabi", ["show", "patterns", "23.*"], 1, "23.1"),
    ("show --force", ["show", "--force", "patterns", "23"], 0, r"^# 23\. "),
    ("path anchor", ["path", "patterns", "17.2"], 0, "#172-"),
    ("path X.10", ["path", "sonarqube", "29.10"], 0, "#2910-"),
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
    proc = run("find", "qo'shimcha zzqwerty")
    hint = [l for l in proc.stderr.split("\n") if l.startswith("kengroq")]
    if not hint:
        return False, "maslahat yo'q"
    command = hint[0].split(": ", 1)[1]
    ok = subprocess.run(["bash", "-n", "-c", command],
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


CHECKS = [
    ("X.10 butun sinf", check_exact_refs),
    ("find maslahati apostrofda", check_find_hint),
    ("bash 3.2 sintaksisi", check_bash32),
    ("indeks eskirishi", check_index_freshness),
]


def main():
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
