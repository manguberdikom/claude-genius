#!/usr/bin/env python3
"""check_code.py uchun sinovlar.

    python3 tools/test_check_code.py

Ikki tomon ham sinaladi va ikkinchisi muhimroq. Hook har Java fayl
yozilganda ishlaydi: agar u toza kodga ogohlantirish bersa yoki izohdagi
matnni kod deb o'qisa, shovqin har yozuvda takrorlanadi va hook
o'chiriladi. Shuning uchun Good.java dan hech narsa chiqmasligi va
izoh/satr ichidagi yolg'on nusxalar sanalmasligi shart.

Holat vaqtinchalik papkada (GENIUS_STATE_DIR): sinov jonli sessiyaning
rules_for belgilarini o'chirmaydi, aks holda keyingi Java yozuvi to'siladi.
"""

import json
import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
TOOL = os.path.join(HERE, "check_code.py")
RULES = os.path.join(HERE, "rules_for.py")
BAD = os.path.join(HERE, "testdata", "java", "Bad.java")
GOOD = os.path.join(HERE, "testdata", "java", "Good.java")
CASES = os.path.join(HERE, "testdata", "check_code")
LITERALS = os.path.join(CASES, "Literals.java")
TX_OK = os.path.join(CASES, "TxOk.java")
TX = os.path.join(CASES, "Tx.java")
MEDIUM = os.path.join(CASES, "Medium.java")
LIVE_STATE = os.path.join(ROOT, ".claude", ".state")

# state import qilinishidan OLDIN: subprocesslar ham shu papkani meros oladi.
STATE = tempfile.mkdtemp(prefix="genius-state-")
os.environ["GENIUS_STATE_DIR"] = STATE
sys.path.insert(0, HERE)

import check_code  # noqa: E402
import state  # noqa: E402

# (nom, daraja, satr, matn bo'lagi)
EXPECT = [
    ("bo'sh catch", "yuqori", 31, "Bo'sh catch"),
    ("keng catch", "o'rta", 23, "catch (Exception)"),
    ("System.out", "o'rta", 36, "System.out"),
    ("printStackTrace", "yuqori", 24, "printStackTrace"),
    ("BigDecimal(double)", "yuqori", 17, "aniq qiymat bermaydi"),
    ("tranzaksiyada HTTP", "yuqori", 12, "Tranzaksiya ichida tashqi chaqiruv"),
]

# Satr literali va izoh: kod emas. Har biri bitta o'tishda ajratiladi,
# ketma-ket regexlarda URL ichidagi `//` qolgan satrni izoh qilib yuborardi.
NO_FINDING = [
    ("satrdagi printStackTrace va catch",
     'class A { String s = "e.printStackTrace(); System.out.println(1); '
     'catch (Exception e) {}"; }'),
    ("izohdagi printStackTrace", "// e.printStackTrace();\nclass A {}"),
    ("char ichidagi qo'shtirnoq",
     "class A { char q = '\"'; String t = \"catch (Exception e) {}\"; }"),
    ("text block", 'class A { String t = """\n  // "x" e.printStackTrace();\n  """; }'),
]
# URL va `/*` li satrdan keyingi kod baribir o'qiladi: yolg'on manfiy yo'q.
ONE_FINDING = [
    ("URL dan keyingi kod",
     'class A { String u = "http://x"; void f(Exception e) { e.printStackTrace(); } }'),
    ("`image/*` dan keyingi kod",
     'class A { String t = "image/*";\n void f(Exception e) { e.printStackTrace(); } }'),
]


def run_file(*paths):
    proc = subprocess.run([sys.executable, TOOL] + list(paths),
                          capture_output=True, text=True, cwd=ROOT)
    return proc.returncode, proc.stdout


def prepare(path, cwd=ROOT):
    """rules_for ni chaqirib, zanjir qadamini belgilaydi."""
    return subprocess.run([sys.executable, RULES, path],
                          capture_output=True, text=True, cwd=cwd)


def run_hook(path, tool_name="Write", cwd=ROOT, response=None):
    payload = {"tool_name": tool_name, "tool_input": {"file_path": path}}
    if response is not None:
        payload["tool_response"] = {"filePath": response}
    proc = subprocess.run([sys.executable, TOOL], input=json.dumps(payload),
                          capture_output=True, text=True, cwd=cwd)
    return proc.stdout.strip()


def decision(raw):
    return json.loads(raw).get("decision") if raw else None


def reason(raw):
    return json.loads(raw).get("reason", "") if raw else ""


def section_titles():
    """index/sections.tsv: (hujjat, bo'lim) -> sarlavha."""
    titles = {}
    path = os.path.join(ROOT, "index", "sections.tsv")
    if os.path.exists(path):
        with open(path, encoding="utf-8") as handle:
            handle.readline()
            for line in handle:
                parts = line.rstrip("\n").split("\t")
                if len(parts) >= 4:
                    titles[(parts[0], parts[1])] = parts[3]
    return titles


def rule_ref(out, rule):
    """`(java:Sxxxx)` bilan tugagan hint qatoridagi `<hujjat> <raqam>`."""
    for line in out.split("\n"):
        if line.rstrip().endswith("(%s)" % rule) and "show " in line:
            return " ".join(line.split("show ", 1)[1].split()[:2])
    return ""


def ref_title(out, needle, titles):
    """`needle` li topilmadan keyingi `doc.sh show <hujjat> <raqam>` sarlavhasi."""
    lines = out.split("\n")
    for i, line in enumerate(lines):
        if needle in line and i + 1 < len(lines) and "show " in lines[i + 1]:
            parts = lines[i + 1].split("show ", 1)[1].split()
            return titles.get((parts[0], parts[1]), "")
    return ""


def live_snapshot():
    """Jonli holat papkasidagi belgilar: sinovdan oldin va keyin bir xil."""
    snap = {}
    for sub in ("rules_for", "rules_for.json"):
        full = os.path.join(LIVE_STATE, sub)
        if os.path.isdir(full):
            snap[sub] = sorted(os.listdir(full))
        elif os.path.exists(full):
            snap[sub] = os.path.getmtime(full)
    return snap


def report(rows):
    bad = 0
    for label, ok in rows:
        bad += not ok
        print("%-4s %s" % ("OK" if ok else "XATO", label))
    return bad


def main():
    for path in (BAD, GOOD, LITERALS, TX_OK, TX, MEDIUM):
        if not os.path.exists(path):
            print("sinov fayli yo'q: %s" % path)
            return 1

    live_before = live_snapshot()
    failures = total = 0
    code_bad, out_bad = run_file(BAD)

    print("== Topilishi kerak ==")
    for name, level, line, needle in EXPECT:
        marker = "[%s] Bad.java:%d" % (level, line)
        ok = marker in out_bad and needle in out_bad
        failures += not ok
        total += 1
        print("%-4s %-22s %s" % ("OK" if ok else "XATO", name, marker))

    print("\n== Qo'llanmaga ulanish ==")
    refs = [l for l in out_bad.split("\n") if "doc.sh show" in l]
    titles = section_titles()
    # Raqam emas, sarlavha tekshiriladi: qayta raqamlashda sinov qizarmaydi,
    # lekin havola boshqa mavzuga (Transaction Script, Money pattern) ketsa
    # ushlanadi.
    tx_title = ref_title(out_bad, "Tranzaksiya ichida", titles).lower()
    money_title = ref_title(out_bad, "BigDecimal(double)", titles).lower()
    rows = [
        ("%d ta topilma bo'lim raqamiga ulandi" % len(refs), len(refs) >= 5),
        ("tranzaksiya havolasi tashqi chaqiruv bo'limiga",
         "tranzaksiya" in tx_title and ("remote" in tx_title or "tashqi" in tx_title)),
        ("BigDecimal havolasi pul va double bo'limiga",
         "pul" in money_title and "double" in money_title),
    ]
    failures += report(rows)
    total += len(rows)

    print("\n== Kalit bir nechta bo'limda ==")
    # S1148 va S2221 ulush bo'yicha yo'l-yo'lakay eslatgan bo'limga (26.14,
    # 29.13) ketardi. term topilmadagi so'z bo'yicha tanlaydi va ikkalasi
    # S108 kabi istisnolarni ushlash bo'limiga boradi. printStackTrace
    # bo'yicha farq 3:2, ya'ni jim teskari ketish shu yerda ushlanadi.
    snippet = ("class A { void f() { try { g(); } "
               "catch (Exception e) { e.printStackTrace(); } "
               "try { g(); } catch (IllegalStateException e) {} } }")
    out_term = check_code.render("A.java", check_code.check_text(snippet, "A.java"))
    empty_ref = rule_ref(out_term, "java:S108")
    catch_title = titles.get(tuple(empty_ref.split()), "").lower()
    rows = [
        ("S108 istisnolarni ushlash bo'limiga",
         "istisno" in catch_title and "ushla" in catch_title),
        ("S2221 S108 bilan bir bo'limga (%s)" % rule_ref(out_term, "java:S2221"),
         bool(empty_ref) and rule_ref(out_term, "java:S2221") == empty_ref),
        ("S1148 S108 bilan bir bo'limga (%s)" % rule_ref(out_term, "java:S1148"),
         bool(empty_ref) and rule_ref(out_term, "java:S1148") == empty_ref),
    ]
    failures += report(rows)
    total += len(rows)

    print("\n== Yolg'on ishga tushish bo'lmasligi kerak ==")
    # Bad.java da izoh ichida System.out.println va catch (Exception e) {}
    # bor. Ular sanalmasligi kerak: har biri aynan bir marta topilishi
    # lozim. Satr literallari quyida alohida, check_text bilan sinaladi.
    for name, needle, want in (("izohdagi System.out", "System.out", 1),
                               ("printStackTrace bir marta", "printStackTrace", 1),
                               ("izohdagi bo'sh catch", "Bo'sh catch", 1)):
        got = out_bad.count(needle)
        ok = got == want
        failures += not ok
        total += 1
        print("%-4s %-26s %d marta (kutilgan %d)"
              % ("OK" if ok else "XATO", name, got, want))
    rows = [(name, check_code.check_text(text, "A.java") == [])
            for name, text in NO_FINDING]
    rows += [(name, len(check_code.check_text(text, "A.java")) == 1)
             for name, text in ONE_FINDING]
    # Literals.java: URL, `image/*`, char, text block va Javadoc dan keyin
    # bitta haqiqiy bo'sh catch. Aynan shu bitta chiqishi kerak.
    code_lit, out_lit = run_file(LITERALS)
    rows.append(("Literals.java: faqat haqiqiy bo'sh catch",
                 code_lit == 1 and "1 ta qoida" in out_lit
                 and "[yuqori] Literals.java:23" in out_lit))
    failures += report(rows)
    total += len(rows)

    print("\n== Izohli catch va tranzaksiya chegarasi ==")
    code_ok, out_ok = run_file(TX_OK)
    code_tx, out_tx = run_file(TX)
    rows = [
        # Izohli catch Sonar uchun bo'sh emas (S108); sinf darajasidagi
        # annotatsiyada maydon e'loni va NOT_SUPPORTED metodi chaqiruv emas;
        # tanasiz metod va `rollbackFor = {...}` tana emas.
        ("TxOk.java toza", code_ok == 0 and "topilmadi" in out_ok),
        ("`record` nomli parametr metod hisoblanadi", "[yuqori] Tx.java:13" in out_tx),
        ("`rollbackFor = {...}` dan keyingi tana", "[yuqori] Tx.java:18" in out_tx),
        ("sinf darajasida chaqiruv joyi", "[yuqori] Tx.java:28" in out_tx),
        ("Tx.java da aynan uchta", "3 ta qoida" in out_tx),
    ]
    failures += report(rows)
    total += len(rows)

    print("\n== Toza fayl ==")
    code_good, out_good = run_file(GOOD)
    rows = [("chiqish kodi 0", code_good == 0),
            ("topilma yo'q", "topilmadi" in out_good)]
    failures += report(rows)
    total += len(rows)

    print("\n== Ko'p fayl ==")
    # Avval faqat argv[1] tekshirilardi: qolganlari jim tashlanib rc 0
    # chiqardi. Toza fayl qatori chiqmaydi (800 faylda shovqin), yig'ma
    # qatordagi fayl soni esa tekshiruv birinchi topilmada to'xtamaganini
    # ko'rsatadi.
    code_gb, out_gb = run_file(GOOD, BAD)
    code_bg, out_bg = run_file(BAD, GOOD)
    code_clean, out_clean = run_file(GOOD, TX_OK)
    code_mix, out_mix = run_file(BAD, os.path.join(ROOT, "README.md"), LITERALS, GOOD)
    rows = [
        ("Good Bad: rc 1, Bad.java ning 6 ta buzilishi",
         code_gb == 1 and "Bad.java: 6 ta qoida buzilishi" in out_gb),
        ("Good Bad: yig'ma qator ikkala faylni sanaydi",
         "check_code: 2 fayl, 6 buzilish" in out_gb),
        ("Bad Good: Good.java ham tekshirildi",
         code_bg == 1 and "Bad.java: 6 ta qoida buzilishi" in out_bg
         and "check_code: 2 fayl, 6 buzilish" in out_bg),
        ("toza fayl qatori chiqmaydi",
         "topilmadi" not in out_gb + out_bg and "Good.java" not in out_gb + out_bg),
        ("hammasi toza: rc 0, faqat yig'ma qator",
         code_clean == 0 and out_clean.strip() == "check_code: 2 fayl, 0 buzilish"),
        ("yig'ma qator oxirida, java bo'lmagan fayl sanalmaydi",
         code_mix == 1
         and out_mix.strip().split("\n")[-1] == "check_code: 3 fayl, 7 buzilish"
         and "Literals.java: 1 ta qoida buzilishi" in out_mix),
    ]
    failures += report(rows)
    total += len(rows)

    print("\n== Zanjir majburlanadi ==")
    state.clear()
    raw_skipped = run_hook(GOOD)
    tmp = tempfile.mkdtemp()
    try:
        alien = os.path.join(tmp, "Unmarked.java")
        shutil.copy(GOOD, alien)
        raw_alien = run_hook(alien, cwd=tmp)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    alien_cmd = os.path.join(ROOT, "tools", "rules_for.py").replace("\\", "/")
    rows = [
        ("rules_for chaqirilmasa block", decision(raw_skipped) == "block"),
        # Klon ichida nisbiy buyruq: allow ro'yxatiga mos.
        ("sabab rules_for buyrug'ini beradi",
         "python3 tools/rules_for.py " in reason(raw_skipped)),
        # Boshqa proyektda nisbiy buyruq "No such file" beradi.
        ("boshqa papkada sabab mutlaq yo'lni beradi",
         decision(raw_alien) == "block" and alien_cmd in reason(raw_alien)
         and os.path.isfile(alien_cmd)),
    ]
    failures += report(rows)
    total += len(rows)

    print("\n== Hook javobi (zanjir bajarilgan) ==")
    for path in (BAD, GOOD, MEDIUM):
        prepare(path)
    raw_bad = run_hook(BAD)
    raw_good = run_hook(GOOD)
    raw_medium = run_hook(MEDIUM)
    medium = json.loads(raw_medium).get("hookSpecificOutput", {}) if raw_medium else {}
    rows = [
        ("yuqori daraja block qaytaradi", decision(raw_bad) == "block"),
        ("block sababida bo'lim raqami bor", "doc.sh show" in reason(raw_bad)),
        ("toza faylda jim", raw_good == ""),
        # O'rta daraja to'smaydi, kontekst sifatida qaytadi.
        ("o'rta daraja additionalContext beradi",
         medium.get("hookEventName") == "PostToolUse"
         and "System.out" in medium.get("additionalContext", "")
         and decision(raw_medium) is None),
        ("java bo'lmagan faylda jim", run_hook(os.path.join(ROOT, "README.md")) == ""),
        ("mavjud bo'lmagan faylda jim", run_hook("/yoq/Fayl.java") == ""),
        # Yo'l tool_response dan olinadi, tool_input esa zaxira.
        ("tool_response.filePath ustun",
         decision(run_hook("/yoq/X.java", response=BAD)) == "block"),
        ("tool_response toza faylda jim",
         run_hook(os.path.join(ROOT, "README.md"), tool_name="Edit",
                  response=GOOD) == ""),
    ]
    failures += report(rows)
    total += len(rows)

    print("\n== Boshqa papkadan (global o'rnatish) ==")
    # Skript klonda, ish boshqa proyektda: nisbiy yo'l va hook dagi mutlaq
    # yo'l bitta belgiga tushishi kerak, aks holda har Java yozuvi to'siladi.
    tmp = tempfile.mkdtemp()
    try:
        java = os.path.join(tmp, "src", "main", "java", "shop", "Toza.java")
        os.makedirs(os.path.dirname(java))
        shutil.copy(GOOD, java)
        rel = prepare(os.path.join("src", "main", "java", "shop", "Toza.java"), cwd=tmp)
        raw_rel = run_hook(java, cwd=tmp)
        # Fayl hali yo'q paytda belgilanadi, keyin boshqacha mazmun bilan
        # yoziladi: reviewer ko'radigan yangi belgi yozuvchiga aytilishi kerak.
        later = os.path.join(tmp, "src", "main", "java", "shop", "PayController.java")
        prepare(later, cwd=tmp)
        with open(later, "w", encoding="utf-8") as handle:
            handle.write("@RestController\nclass PayController {\n"
                         "    @Transactional\n    void pay() { repository.save(1); }\n}\n")
        raw_drift = run_hook(later, cwd=tmp)
        drift = (json.loads(raw_drift).get("hookSpecificOutput", {})
                 .get("additionalContext", "") if raw_drift else "")
        prepare(later, cwd=tmp)
        raw_same = run_hook(later, cwd=tmp)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    rows = [
        ("nisbiy yo'l bilan belgi qo'yildi, rc 0", rel.returncode == 0),
        ("nisbiy yo'l belgilari topildi", "# 1 fayl, 0 belgi" not in rel.stdout
         and "loglash" in rel.stdout),
        ("hook mutlaq yo'lda jim", raw_rel == ""),
        ("yozilgandan keyingi yangi belgi aytiladi",
         "tranzaksiya" in drift and "web qatlami" not in drift),
        ("qayta chaqirilgandan keyin jim", raw_same == ""),
    ]
    failures += report(rows)
    total += len(rows)

    print("\n== Jonli holatga tegilmadi ==")
    rows = [("jonli .claude/.state o'zgarmadi", live_snapshot() == live_before)]
    failures += report(rows)
    total += len(rows)

    print("\n%d/%d o'tdi" % (total - failures, total))
    return 1 if failures else 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    finally:
        shutil.rmtree(STATE, ignore_errors=True)
