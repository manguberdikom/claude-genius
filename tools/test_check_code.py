#!/usr/bin/env python3
"""check_code.py uchun sinovlar.

    python3 tools/test_check_code.py [-k bo'lim] [--vaqt [ms]]

Ikki tomon ham sinaladi va ikkinchisi muhimroq. Hook har Java fayl
yozilganda ishlaydi: agar u toza kodga ogohlantirish bersa yoki izohdagi
matnni kod deb o'qisa, shovqin har yozuvda takrorlanadi va hook
o'chiriladi. Shuning uchun Good.java dan hech narsa chiqmasligi va
izoh/satr ichidagi yolg'on nusxalar sanalmasligi shart.

Holat vaqtinchalik papkada (GENIUS_STATE_DIR): sinov jonli sessiyaning
rules_for belgilarini o'chirmaydi, aks holda keyingi Java yozuvi to'siladi.
"""

import io
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
TX_AFTER = os.path.join(CASES, "TxAfterCommit.java")
TX_VERSION = os.path.join(CASES, "TxHttpVersion.java")
TX_FACTORY = os.path.join(CASES, "TxStaticFactory.java")
SUPPRESSED = os.path.join(CASES, "Suppressed.java")
LIVE_STATE = os.path.join(ROOT, ".claude", ".state")

# state import qilinishidan OLDIN: subprocesslar ham shu papkani meros oladi.
STATE = tempfile.mkdtemp(prefix="genius-state-")
os.environ["GENIUS_STATE_DIR"] = STATE

# Hook faqat Java proyektida yoki klonning o'zida ishlaydi
# (hookio.active). Sinovlar vaqtinchalik papkada yuradi, shu yerda esa
# tekshirilayotgan narsa gating emas: ildiz klonga qo'yiladi. Gating ning
# o'z sinovlari tools/test_hookio.py da va shu fayldagi alohida
# holatlarda.
os.environ["CLAUDE_PROJECT_DIR"] = ROOT
sys.path.insert(0, HERE)

import check_code  # noqa: E402
import rules_for  # noqa: E402
import state  # noqa: E402
import testkit  # noqa: E402
sys.path.insert(0, os.path.join(ROOT, "install"))
import rewrite_paths as RP  # noqa: E402

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
    """CLI rejimi jarayon ichida: (chiqish kodi, stdout)."""
    res = testkit.call_main(check_code.main, argv=["check_code.py"] + list(paths),
                            cwd=ROOT)
    return res.returncode, res.stdout


def run_file_proc(*paths):
    """CLI rejimi alohida jarayonda: chiqish kodi haqiqiy sys.exit dan."""
    proc = subprocess.run([sys.executable, TOOL] + list(paths),
                          capture_output=True, text=True, cwd=ROOT)
    return proc.returncode, proc.stdout


def prepare(path, cwd=ROOT):
    """rules_for ni chaqirib, zanjir qadamini belgilaydi (jarayon ichida)."""
    return testkit.call_main(rules_for.main, argv=["rules_for.py", path], cwd=cwd)


def hook_payload(path, tool_name, response, original):
    payload = {"tool_name": tool_name, "tool_input": {"file_path": path}}
    if response is not None:
        payload["tool_response"] = {"filePath": response}
    if original is not False:
        payload.setdefault("tool_response", {"filePath": path})
        payload["tool_response"]["originalFile"] = original
    return json.dumps(payload)


def run_hook(path, tool_name="Write", cwd=ROOT, response=None, env=None,
             original=False):
    """Hook jarayon ichida. `original` berilsa tool_response.originalFile
    (None ham qiymat)."""
    return testkit.call_main(
        check_code.main, hook_payload(path, tool_name, response, original),
        argv=["check_code.py"], cwd=cwd, env=env).stdout.strip()


def run_hook_proc(path, tool_name="Write", cwd=ROOT, env=None):
    """Hook alohida jarayonda: stdin, muhit va stdout haqiqiy."""
    proc = subprocess.run([sys.executable, TOOL],
                          input=hook_payload(path, tool_name, None, False),
                          capture_output=True, text=True, cwd=cwd,
                          env=None if env is None else dict(os.environ, **env))
    return proc.stdout.strip()


def decision(raw):
    return json.loads(raw).get("decision") if raw else None


def reason(raw):
    return json.loads(raw).get("reason", "") if raw else ""


def context_of(raw):
    """block sababi yoki additionalContext: ikkisidan qaysi biri bo'lsa."""
    if not raw:
        return ""
    data = json.loads(raw)
    return (data.get("reason")
            or data.get("hookSpecificOutput", {}).get("additionalContext", ""))


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


_memo = {}


def bad_output():
    """Bad.java ning CLI chiqishi: bir necha bo'lim shunga tayanadi.

    Alohida jarayonda (E2E): CLI ning haqiqiy stdout va chiqish kodi.
    """
    if "bad" not in _memo:
        _memo["bad"] = run_file_proc(BAD)
    return _memo["bad"][1]


def case_topilishi():
    out_bad = bad_output()
    rows = []
    for name, level, line, needle in EXPECT:
        marker = "[%s] Bad.java:%d" % (level, line)
        rows.append(("%-22s %s" % (name, marker), marker in out_bad and needle in out_bad))
    return rows


def case_qollanma():
    out_bad = bad_output()
    refs = [line for line in out_bad.split("\n") if "doc.sh show" in line]
    titles = section_titles()
    # Raqam emas, sarlavha tekshiriladi: qayta raqamlashda sinov qizarmaydi,
    # lekin havola boshqa mavzuga (Transaction Script, Money pattern) ketsa
    # ushlanadi.
    tx_title = ref_title(out_bad, "Tranzaksiya ichida", titles).lower()
    money_title = ref_title(out_bad, "BigDecimal(double)", titles).lower()
    return [
        ("%d ta topilma bo'lim raqamiga ulandi" % len(refs), len(refs) >= 5),
        ("tranzaksiya havolasi tashqi chaqiruv bo'limiga",
         "tranzaksiya" in tx_title and ("remote" in tx_title or "tashqi" in tx_title)),
        ("BigDecimal havolasi pul va double bo'limiga",
         "pul" in money_title and "double" in money_title),
    ]


def case_kalit_bolimlar():
    # S1148 va S2221 ulush bo'yicha yo'l-yo'lakay eslatgan bo'limga (26.14,
    # 29.13) ketardi. term topilmadagi so'z bo'yicha tanlaydi va ikkalasi
    # S108 kabi istisnolarni ushlash bo'limiga boradi. printStackTrace
    # bo'yicha farq 3:2, ya'ni jim teskari ketish shu yerda ushlanadi.
    titles = section_titles()
    snippet = ("class A { void f() { try { g(); } "
               "catch (Exception e) { e.printStackTrace(); } "
               "try { g(); } catch (IllegalStateException e) {} } }")
    out_term = check_code.render("A.java", check_code.check_text(snippet, "A.java"))
    empty_ref = rule_ref(out_term, "java:S108")
    catch_title = titles.get(tuple(empty_ref.split()), "").lower()
    return [
        ("S108 istisnolarni ushlash bo'limiga",
         "istisno" in catch_title and "ushla" in catch_title),
        ("S2221 S108 bilan bir bo'limga (%s)" % rule_ref(out_term, "java:S2221"),
         bool(empty_ref) and rule_ref(out_term, "java:S2221") == empty_ref),
        ("S1148 S108 bilan bir bo'limga (%s)" % rule_ref(out_term, "java:S1148"),
         bool(empty_ref) and rule_ref(out_term, "java:S1148") == empty_ref),
    ]


def case_yolgon_topilma():
    # Bad.java da izoh ichida System.out.println va catch (Exception e) {}
    # bor. Ular sanalmasligi kerak: har biri aynan bir marta topilishi
    # lozim. Satr literallari quyida alohida, check_text bilan sinaladi.
    out_bad = bad_output()
    rows = []
    for name, needle, want in (("izohdagi System.out", "System.out", 1),
                               ("printStackTrace bir marta", "printStackTrace", 1),
                               ("izohdagi bo'sh catch", "Bo'sh catch", 1)):
        got = out_bad.count(needle)
        rows.append(("%-26s %d marta (kutilgan %d)" % (name, got, want), got == want))
    rows += [(name, check_code.check_text(text, "A.java") == [])
             for name, text in NO_FINDING]
    rows += [(name, len(check_code.check_text(text, "A.java")) == 1)
             for name, text in ONE_FINDING]
    # Literals.java: URL, `image/*`, char, text block va Javadoc dan keyin
    # bitta haqiqiy bo'sh catch. Aynan shu bitta chiqishi kerak.
    code_lit, out_lit = run_file(LITERALS)
    rows.append(("Literals.java: faqat haqiqiy bo'sh catch",
                 code_lit == 1 and "1 ta qoida" in out_lit
                 and "[yuqori] Literals.java:23" in out_lit))
    return rows


def case_tranzaksiya():
    code_ok, out_ok = run_file(TX_OK)
    _, out_tx = run_file(TX)
    return [
        # Izohli catch Sonar uchun bo'sh emas (S108); sinf darajasidagi
        # annotatsiyada maydon e'loni va NOT_SUPPORTED metodi chaqiruv emas;
        # tanasiz metod va `rollbackFor = {...}` tana emas.
        ("TxOk.java toza", code_ok == 0 and "topilmadi" in out_ok),
        ("`record` nomli parametr metod hisoblanadi", "[yuqori] Tx.java:13" in out_tx),
        ("`rollbackFor = {...}` dan keyingi tana", "[yuqori] Tx.java:18" in out_tx),
        ("sinf darajasida chaqiruv joyi", "[yuqori] Tx.java:28" in out_tx),
        ("Tx.java da aynan uchta", "3 ta qoida" in out_tx),
    ]


def case_commitdan_keyin():
    # Qo'llanma tashqi chaqiruvni afterCommit ga yoki AFTER_COMMIT
    # listeneriga ko'chirishni tavsiya qiladi: hook o'z maslahatini
    # to'smasligi kerak. `HttpClient.Version` tur nomi, chaqiruv emas;
    # metod ichidagi `RestClient.create().get()` esa haqiqiy chaqiruv.
    code_after, out_after = run_file(TX_AFTER)
    code_ver, out_ver = run_file(TX_VERSION)
    code_fac, out_fac = run_file(TX_FACTORY)
    listener_tx = ("@Transactional\nclass A {\n"
                   "  @TransactionalEventListener(phase = TransactionPhase.BEFORE_COMMIT)\n"
                   "  void on(E e) { restTemplate.postForObject(\"/x\", e, Void.class); }\n"
                   "  @TransactionalEventListener\n"
                   "  @Transactional(propagation = Propagation.REQUIRES_NEW)\n"
                   "  void again(E e) { restTemplate.postForObject(\"/y\", e, Void.class); }\n}\n")
    after_call = ("class A {\n  @Transactional\n  void f() {\n"
                  "    restClient.post().retrieve();\n"
                  "    sync.afterCommit();\n  }\n}\n")
    return [
        ("TxAfterCommit.java: 0 topilma (afterCommit, afterCompletion, listener)",
         code_after == 0 and "topilmadi" in out_after),
        ("TxHttpVersion.java: 0 topilma (tur nomi chaqiruv emas)",
         code_ver == 0 and "topilmadi" in out_ver),
        ("TxStaticFactory.java: metod ichidagi statik fabrika 1 yuqori",
         code_fac == 1 and "1 ta qoida" in out_fac
         and "[yuqori] TxStaticFactory.java:13" in out_fac),
        ("BEFORE_COMMIT va REQUIRES_NEW listener istisno emas",
         [f.line for f in check_code.check_text(listener_tx, "A.java")] == [4, 7]),
        ("`sync.afterCommit();` chaqiruvi tana emas: oldingi chaqiruv topiladi",
         [f.line for f in check_code.check_text(after_call, "A.java")] == [4]),
    ]


def case_nosonar():
    code_sup, out_sup = run_file(SUPPRESSED)
    test_out = ("class OrderServiceTest { void t() { System.out.println(1); "
                "Thread.sleep(10); } }")
    return [
        # Kalit mos kelgan e'londa va NOSONAR satrida o'tkaziladi; boshqa
        # kalit, izohdagi annotatsiya va satrdagi "NOSONAR" o'tkazmaydi.
        ("Suppressed.java: aynan 3 ta qolgan", code_sup == 1 and "3 ta qoida" in out_sup),
        ("@SuppressWarnings boshqa kalitni o'tkazmaydi (S2221)",
         "[o'rta] Suppressed.java:10" in out_sup),
        ("satr literalidagi NOSONAR hisoblanmaydi",
         "[yuqori] Suppressed.java:23" in out_sup),
        ("izohdagi @SuppressWarnings hisoblanmaydi",
         "[o'rta] Suppressed.java:32" in out_sup),
        ("S106 kaliti, NOSONAR va bo'sh catch NOSONAR o'tkazildi",
         all("Suppressed.java:%d " % n not in out_sup for n in (7, 16, 19))),
        ("test kodida System.out belgilanmaydi, Thread.sleep qoladi",
         [f.rule for f in check_code.check_text(
             test_out, "src/test/java/shop/OrderServiceTest.java")] == ["java:S2925"]),
    ]


def case_keng_catch():
    rethrow = ("class A { void f() throws Exception { try { g(); } "
               "catch (Exception ex) { log.error(\"x\", ex); throw ex; } } }")
    throwable = ("class A { void f() { try { g(); } "
                 "catch (Throwable t) { throw new IllegalStateException(t); } } }")
    out_re = check_code.render("A.java", check_code.check_text(rethrow, "A.java"))
    found_t = check_code.check_text(throwable, "A.java")
    return [
        ("log va qayta otish: xabarda \"yut\" so'zi yo'q",
         "java:S2221" in out_re and "yut" not in out_re),
        ("catch (Throwable): java:S1181, java:S2221 emas",
         [f.rule for f in found_t] == ["java:S1181"]),
    ]


def case_toza_fayl():
    code_good, out_good = run_file(GOOD)
    return [("chiqish kodi 0", code_good == 0),
            ("topilma yo'q", "topilmadi" in out_good)]


def case_kop_fayl():
    # Avval faqat argv[1] tekshirilardi: qolganlari jim tashlanib rc 0
    # chiqardi. Toza fayl qatori chiqmaydi (800 faylda shovqin), yig'ma
    # qatordagi fayl soni esa tekshiruv birinchi topilmada to'xtamaganini
    # ko'rsatadi.
    code_gb, out_gb = run_file(GOOD, BAD)
    code_bg, out_bg = run_file(BAD, GOOD)
    code_clean, out_clean = run_file(GOOD, TX_OK)
    code_mix, out_mix = run_file(BAD, os.path.join(ROOT, "README.md"), LITERALS, GOOD)
    # Kotlin fayl tekshirilmaydi: "topilmadi" deyish yolg'on hisobot.
    code_kt, out_kt = run_file("src/main/kotlin/shop/Bad.kt")
    code_kt2, out_kt2 = run_file(GOOD, "Bad.kt")
    return [
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
        (".kt: tekshirilmadi va rc 3",
         code_kt == 3 and out_kt.strip()
         == "src/main/kotlin/shop/Bad.kt: tekshirilmadi (faqat .java)"),
        ("ko'p faylda .kt: qator, yig'ma va rc 3",
         code_kt2 == 3 and "Bad.kt: tekshirilmadi (faqat .java)" in out_kt2
         and out_kt2.strip().split("\n")[-1] == "check_code: 1 fayl, 0 buzilish"),
        ("buzilish bo'lsa .kt bilan ham rc 1",
         code_mix == 1 and "README.md: tekshirilmadi" in out_mix),
    ]


def case_zanjir():
    state.clear()
    # Klondagi oddiy .java: shart shu yerda. testdata/ dagi fixture undan
    # tashqarida (HK-H5), shuning uchun nusxa klon ildizidagi vaqtinchalik
    # papkada.
    inside = tempfile.mkdtemp(prefix=".tmp-zanjir-", dir=ROOT)
    try:
        own = os.path.join(inside, "Unmarked.java")
        shutil.copy(GOOD, own)
        raw_skipped = run_hook(own)
    finally:
        shutil.rmtree(inside, ignore_errors=True)
    raw_fixture = run_hook(GOOD)
    raw_fixture_bad = run_hook(BAD)
    tmp = tempfile.mkdtemp()
    try:
        alien = os.path.join(tmp, "Unmarked.java")
        shutil.copy(GOOD, alien)
        raw_alien = run_hook(alien, cwd=tmp)
        # Windows o'rnatishi: Python o'rnatuvchi tanlagan to'liq yo'l bilan.
        win_py = "C:\\Program Files\\Python312\\python.exe"
        raw_win = run_hook(alien, cwd=tmp, env={"GENIUS_PYTHON": win_py})
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    alien_cmd = os.path.join(ROOT, "tools", "rules_for.py").replace("\\", "/")
    return [
        ("rules_for chaqirilmasa block", decision(raw_skipped) == "block"),
        # Fixture rules_for shartidan tashqarida: toza fixture jim, buzug'i
        # esa mexanik tekshiruvdan o'tmaydi.
        ("testdata fixture: rules_for sharti yo'q", raw_fixture == ""),
        ("testdata fixture: mexanik block qoladi",
         decision(raw_fixture_bad) == "block"
         and "Yozishdan oldin qoidalar olinmagan" not in reason(raw_fixture_bad)),
        # Zanjir qoidasi shu proyektning konvensiyasi: boshqa repoda hech
        # kim unga rozi bo'lmagan, shuning uchun u yerda to'smaydi.
        ("boshqa papkada block emas, eslatma",
         decision(raw_alien) is None
         and "Yozishdan oldin qoidalar olinmagan"
         in json.loads(raw_alien)["hookSpecificOutput"]["additionalContext"]
         and json.loads(raw_alien)["hookSpecificOutput"]["hookEventName"]
         == "PostToolUse"),
        # Klon ichida nisbiy buyruq: allow ro'yxatiga mos.
        ("sabab rules_for buyrug'ini beradi",
         "python3 tools/rules_for.py " in reason(raw_skipped)),
        # Boshqa proyektda nisbiy buyruq "No such file" beradi.
        ("boshqa papkada sabab mutlaq yo'lni beradi",
         alien_cmd in context_of(raw_alien) and os.path.isfile(alien_cmd)),
        # Hint allow qoidasi bilan bir xil boshlanadi: rewrite_paths.tool_cmd.
        ("GENIUS_PYTHON: hint allow qoidasiga mos",
         RP.tool_cmd(ROOT.replace("\\", "/"), win_py, "rules_for.py")
         in context_of(raw_win)),
    ]


def case_hook_javobi():
    for path in (BAD, GOOD, MEDIUM, TX_AFTER):
        prepare(path)
    # Block alohida jarayonda (E2E): JSON haqiqiy stdout dan o'qiladi.
    raw_bad = run_hook_proc(BAD)
    raw_good = run_hook(GOOD)
    raw_medium = run_hook(MEDIUM)
    raw_after = run_hook(TX_AFTER)
    medium = json.loads(raw_medium).get("hookSpecificOutput", {}) if raw_medium else {}
    return [
        ("yuqori daraja block qaytaradi", decision(raw_bad) == "block"),
        ("block sababida bo'lim raqami bor", "doc.sh show" in reason(raw_bad)),
        ("toza faylda jim", raw_good == ""),
        ("afterCommit fixture da jim", raw_after == ""),
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


def case_edit_yangi():
    # Eski kodga har Edit da block modelni tegilmagan qatorni tuzatishga
    # undaydi. originalFile bilan solishtiriladi: mazmun bo'yicha, shuning
    # uchun yuqorida satr qo'shilsa ham eski topilma eski bo'lib qoladi.
    # Belgilar oldingi bo'limdan qolmasligi mumkin (-k): zanjir shu yerda.
    for path in (BAD, MEDIUM):
        prepare(path)
    with open(BAD, encoding="utf-8") as handle:
        bad_text = handle.read()
    with open(MEDIUM, encoding="utf-8") as handle:
        medium_text = handle.read()
    unrelated = bad_text.replace('"e.printStackTrace() satr ichida"', '"boshqa matn"')
    shifted = "// sarlavha\n\n" + bad_text
    no_trace = bad_text.replace("e.printStackTrace();", 'log.warn("x", e);')
    twice = bad_text.replace("e.printStackTrace();",
                             "e.printStackTrace();\n            e.printStackTrace();")
    raw_unrel = run_hook(BAD, tool_name="Edit", original=unrelated)
    raw_shift = run_hook(BAD, tool_name="Edit", original=shifted)
    raw_new = run_hook(BAD, tool_name="Edit", original=no_trace)
    raw_null = run_hook(BAD, tool_name="Write", original=None)
    raw_med = run_hook(MEDIUM, tool_name="Edit", original=medium_text)
    raw_med_new = run_hook(MEDIUM, tool_name="Edit",
                           original=medium_text.replace('System.out.println("x");', ""))
    return [
        ("aloqasiz Edit: block yo'q, jim", raw_unrel == ""),
        ("satrlar surilgan: baribir jim", raw_shift == ""),
        ("printStackTrace qo'shgan Edit: block",
         decision(raw_new) == "block" and "printStackTrace" in reason(raw_new)),
        ("block da faqat yangi topilma",
         "1 ta qoida buzilishi" in reason(raw_new)
         and "Bo'sh catch" not in reason(raw_new)),
        ("originalFile null (yangi fayl): hammasi", decision(raw_null) == "block"
         and "6 ta qoida buzilishi" in reason(raw_null)),
        ("o'rta daraja eski: additionalContext ham yo'q", raw_med == ""),
        ("o'rta daraja yangi: additionalContext",
         "System.out" in context_of(raw_med_new) and decision(raw_med_new) is None),
        # Eski faylda ikkita bir xil satr, yangisida bitta: hech biri yangi
        # emas. Teskarisi: bittasi bor joyga ikkinchisi qo'shilsa, bittasi yangi.
        ("multiset: bir xil satrdan biri o'chsa yangi topilma yo'q",
         check_code.only_new(check_code.check_text(bad_text, BAD), bad_text,
                             twice, BAD) == []),
        ("multiset: bir xil satr qo'shilsa bittasi yangi",
         len(check_code.only_new(check_code.check_text(twice, BAD), twice,
                                 bad_text, BAD)) == 1),
    ]


def case_erta_chiqish():
    # .md, .py yozuvi ko'pchilik: docref va state yuklanmasdan chiqiladi.
    # sys.modules toza bo'lishi kerak: shuning uchun alohida jarayon.
    probe = ("import sys; sys.path.insert(0, %r); sys.argv = ['check_code.py']; "
             "import check_code; rc = check_code.main(); "
             "print(rc, 'docref' in sys.modules, 'state' in sys.modules)" % HERE)
    payload = json.dumps({"tool_name": "Edit",
                          "tool_input": {"file_path": os.path.join(ROOT, "README.md")}})
    proc = subprocess.run([sys.executable, "-c", probe], input=payload,
                          capture_output=True, text=True, cwd=ROOT)
    reexport = subprocess.run(
        [sys.executable, "-c", "import sys; sys.path.insert(0, %r); "
         "from check_code import hint, in_clone, quote, tool_cmd; "
         "print(callable(tool_cmd) and callable(hint))" % HERE],
        capture_output=True, text=True, cwd=ROOT)
    return [
        (".md yozuvi: chiqish yo'q, docref va state yuklanmadi",
         proc.stdout.strip() == "0 False False"),
        ("docref nomlari check_code dan import qilinadi (rules_for, budget)",
         reexport.stdout.strip() == "True"),
    ]


def case_boshqa_papka():
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
    return [
        ("nisbiy yo'l bilan belgi qo'yildi, rc 0", rel.returncode == 0),
        ("nisbiy yo'l belgilari topildi", "# 1 fayl, 0 belgi" not in rel.stdout
         and "loglash" in rel.stdout),
        ("hook mutlaq yo'lda jim", raw_rel == ""),
        ("yozilgandan keyingi yangi belgi aytiladi",
         "tranzaksiya" in drift and "web qatlami" not in drift),
        ("qayta chaqirilgandan keyin jim", raw_same == ""),
    ]


def case_java_emas():
    # Global o'rnatishda PostToolUse hooki har proyektda yuradi. Python yoki
    # JS proyektida .java yozuvi ham, zanjir qoidasi ham o'rinsiz: hook
    # chiqishsiz o'tadi (hookio.active). Klon ichida avvalgidek qoladi.
    tmp = tempfile.mkdtemp(prefix="cc_gate_")
    try:
        plain = os.path.join(tmp, "A.java")
        shutil.copy(BAD, plain)                 # buzilishi ko'p fayl
        io.open(os.path.join(tmp, "package.json"), "w",
                encoding="utf-8").write("{}\n")
        state.clear()                           # rules_for chaqirilmagan
        raw_plain = run_hook(plain, cwd=tmp, env={"CLAUDE_PROJECT_DIR": tmp})
        maven = os.path.join(tmp, "maven")
        os.makedirs(maven)
        java = os.path.join(maven, "A.java")
        shutil.copy(BAD, java)
        io.open(os.path.join(maven, "pom.xml"), "w",
                encoding="utf-8").write("<project/>\n")
        raw_maven = run_hook(java, cwd=maven, env={"CLAUDE_PROJECT_DIR": maven})
        # Muhit jarayonga meros o'tishi E2E da: alohida jarayon.
        raw_off = run_hook_proc(BAD, env={"GENIUS_HOOKS": "off"})
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    return [
        ("Java emas: belgisiz .java yozuvi block bermaydi", raw_plain == ""),
        # Java proyektida hook ishlaydi. To'smaydi (klondan tashqarida
        # zanjir qoidasi eslatma), lekin topilmalar va ro'yxat beriladi.
        ("pom.xml li papkada hook ishlaydi",
         raw_maven != "" and "Yozishdan oldin qoidalar olinmagan"
         in context_of(raw_maven)),
        ("GENIUS_HOOKS=off: klonda ham jim", raw_off == ""),
    ]


LIVE_BEFORE = {}


def case_jonli_holat():
    return [("jonli .claude/.state o'zgarmadi", live_snapshot() == LIVE_BEFORE)]


# Sonar qoidalari: (nom, qoida, yo'l, kod, kutilgan topilma bormi).
# Musbat holatda kamida bitta topilma, manfiyda hech biri. Kod sinf
# tanasiga o'raladi; test qoidalari uchun yo'l /test/ ichida.
MAIN = "src/main/java/shop/A.java"
TEST = "src/test/java/shop/ATest.java"


def wrap(body, imports=""):
    return imports + "class A {\n" + body + "\n}\n"


SIMILAR_TESTS = "".join(
    "@Test\nvoid rejects%s() {\n  assertThatThrownBy(() -> parse(\"%s\"))\n"
    "      .isInstanceOf(BadInput.class);\n  assertThat(counter.get()).isEqualTo(%d);\n}\n"
    % (name, text, n) for name, text, n in (("A", "a", 1), ("B", "b", 2), ("C", "c", 3)))

SONAR_CASES = [
    # java:S1128 ishlatilmagan import
    ("S1128 ishlatilmagan import", "java:S1128", MAIN,
     wrap("void f() {}", "import java.util.Set;\n"), True),
    ("S1128 ishlatilmagan statik import", "java:S1128", TEST,
     wrap("void f() {}", "import static org.mockito.Mockito.never;\n"), True),
    ("S1128 ishlatilgan import toza", "java:S1128", MAIN,
     wrap("Set<String> s;", "import java.util.Set;\n"), False),
    ("S1128 FQN dagi nom import ni ishlatmaydi", "java:S1128", MAIN,
     wrap("void f(x.Row r) {}", "import org.apache.poi.ss.usermodel.Row;\n"), True),
    ("S1128 javadoc {@link} parametri ishlatish", "java:S1128", MAIN,
     wrap("/** {@link Util#f(LocalDate, Set)} */ void f() {}",
          "import java.time.LocalDate;\nimport java.util.Set;\n"), False),
    ("S1128 @throws ishlatish", "java:S1128", MAIN,
     wrap("/** @throws IOException xato */ void f() {}", "import java.io.IOException;\n"), False),
    ("S1128 statik import chaqiruvda", "java:S1128", TEST,
     wrap("void f() { when(x); }", "import static org.mockito.Mockito.when;\n"), False),
    ("S1128 statik import `::nom` havola ishlatish emas", "java:S1128", TEST,
     wrap("void f() { a.filter(b::contains); }",
          "import static org.mockito.ArgumentMatchers.contains;\n"), True),
    ("S1128 wildcard import tegilmaydi", "java:S1128", MAIN,
     wrap("void f() {}", "import java.util.*;\n"), False),
    ("S1128 annotatsiyada ishlatish", "java:S1128", MAIN,
     wrap("@Marker void f() {}", "import shop.Marker;\n"), False),
    # java:S8694 oy int literal
    ("S8694 LocalDate.of oy literali", "java:S8694", MAIN,
     wrap("Object d = LocalDate.of(2026, 10, 7);"), True),
    ("S8694 LocalDateTime.of oy literali", "java:S8694", TEST,
     wrap("Object d = LocalDateTime.of(2026, 10, 7, 9, 0);"), True),
    ("S8694 YearMonth.of oy literali", "java:S8694", MAIN,
     wrap("Object d = YearMonth.of(2026, 3);"), True),
    ("S8694 MonthDay.of birinchi argument oy", "java:S8694", MAIN,
     wrap("Object d = MonthDay.of(2, 29);"), True),
    ("S8694 Month enum bilan toza", "java:S8694", MAIN,
     wrap("Object d = LocalDate.of(2026, Month.OCTOBER, 7);"), False),
    ("S8694 oy o'zgaruvchi bo'lsa tegilmaydi", "java:S8694", MAIN,
     wrap("Object d = LocalDate.of(year, month, 7);"), False),
    ("S8694 LocalDateTime.of(date, time)", "java:S8694", MAIN,
     wrap("Object d = LocalDateTime.of(date, LocalTime.of(9, 0));"), False),
    # java:S6213 cheklangan identifikator
    ("S6213 record nomli parametr", "java:S6213", MAIN,
     wrap("void f(AuditRecord record) { use(record); }"), True),
    ("S6213 record nomli mahalliy o'zgaruvchi", "java:S6213", MAIN,
     wrap("void f() { Row record = next(); }"), True),
    ("S6213 for-each o'zgaruvchisi", "java:S6213", TEST,
     wrap("void f() { for (ConsumerRecord<String, String> record : rows) { use(record); } }"), True),
    ("S6213 lambda parametri", "java:S6213", MAIN,
     wrap("void f() { run((record, exception) -> go(record)); }"), True),
    ("S6213 yagona lambda parametri", "java:S6213", MAIN,
     wrap("void f() { rows.forEach(record -> go(record)); }"), True),
    ("S6213 pattern o'zgaruvchisi", "java:S6213", MAIN,
     wrap("void f(Object o) { if (o instanceof Row record) { go(record); } }"), True),
    ("S6213 record e'loni tegilmaydi", "java:S6213", MAIN,
     wrap("record Point(int x, int y) {}"), False),
    ("S6213 return record; tegilmaydi", "java:S6213", MAIN,
     wrap("Row f() { return record; }"), False),
    ("S6213 oddiy nom tegilmaydi", "java:S6213", MAIN,
     wrap("void f(Row row) { rows.forEach(event -> go(event)); }"), False),
    ("S6213 permits o'zgaruvchi nomi bo'lishi mumkin", "java:S6213", MAIN,
     wrap("void f() { int permits = 3; }"), False),
    ("S6213 `-> record;` tegilmaydi", "java:S6213", MAIN,
     wrap("void f() { Supplier<Row> s = () -> record; }"), False),
    # java:S5778 assertThrows lambdasida bir nechta chaqiruv
    ("S5778 ikki chaqiruv", "java:S5778", TEST,
     wrap("void t() { assertThatThrownBy(() -> parser.parse(load(\"a\")))"
          ".isInstanceOf(IllegalStateException.class); }"), True),
    ("S5778 konstruktor va chaqiruv", "java:S5778", TEST,
     wrap("void t() { assertThatThrownBy(() -> Foo.of(new Bar(), 1))"
          ".isInstanceOf(IllegalStateException.class); }"), True),
    ("S5778 JUnit assertThrows", "java:S5778", TEST,
     wrap("void t() { assertThrows(IllegalStateException.class, "
          "() -> service.run(order.getId())); }"), True),
    ("S5778 bitta chaqiruv toza", "java:S5778", TEST,
     wrap("void t() { assertThatThrownBy(() -> service.run(ID))"
          ".isInstanceOf(IllegalStateException.class); }"), False),
    ("S5778 isInstanceOfSatisfying Sonar bayroqlamaydi", "java:S5778", TEST,
     wrap("void t() { assertThatThrownBy(() -> service.run(order.getId()))"
          ".isInstanceOfSatisfying(CommonException.class, ex -> check(ex)); }"), False),
    ("S5778 List.of qiymat fabrikasi hisoblanmaydi", "java:S5778", TEST,
     wrap("void t() { assertThatThrownBy(() -> service.update(List.of(ID)))"
          ".isInstanceOf(IllegalStateException.class); }"), False),
    ("S5778 main kodda tegilmaydi", "java:S5778", MAIN,
     wrap("void t() { assertThrows(X.class, () -> a(b())); }"), False),
    # java:S8692 testda tizim soati
    ("S8692 Instant.now()", "java:S8692", TEST,
     wrap("void t() { Instant at = Instant.now(); }"), True),
    ("S8692 LocalDate.now(ZONE)", "java:S8692", TEST,
     wrap("LocalDate d = LocalDate.now(AttendanceTime.ZONE);"), True),
    ("S8692 Clock.systemUTC()", "java:S8692", TEST,
     wrap("Clock c = Clock.systemUTC();"), True),
    ("S8692 Clock.system(zone)", "java:S8692", TEST,
     wrap("Clock c = Clock.system(ZONE);"), True),
    ("S8692 Clock.fixed toza", "java:S8692", TEST,
     wrap("Clock c = Clock.fixed(Instant.parse(\"2026-10-07T00:00:00Z\"), ZONE);"), False),
    ("S8692 now(clock) toza", "java:S8692", TEST,
     wrap("LocalDate d = LocalDate.now(clock); Instant i = Instant.now(fixedClock);"), False),
    ("S8692 main kodda tegilmaydi", "java:S8692", MAIN,
     wrap("Instant at = Instant.now();"), False),
    # java:S1612 metod havolasi
    ("S1612 x -> x == null", "java:S1612", TEST,
     wrap("void t() { assertThat(rows).filteredOn(outcome -> outcome == null).hasSize(1); }"), True),
    ("S1612 x -> x != null", "java:S1612", MAIN,
     wrap("void t() { rows.removeIf(row -> row != null); }"), True),
    ("S1612 x -> x.foo()", "java:S1612", MAIN,
     wrap("void t() { rows.stream().filter(s -> s.isUpdatable()).toList(); }"), True),
    ("S1612 () -> obj.foo()", "java:S1612", MAIN,
     wrap("void t() { run(() -> resolver.visibleScope()); }"), True),
    ("S1612 x -> Util.f(x)", "java:S1612", MAIN,
     wrap("void t() { rows.stream().map(r -> Mapper.toDto(r)).toList(); }"), True),
    ("S1612 x -> new T(x)", "java:S1612", MAIN,
     wrap("void t() { rows.stream().map(r -> new Dto(r)).toList(); }"), True),
    ("S1612 argumentli chaqiruv tegilmaydi", "java:S1612", MAIN,
     wrap("void t() { rows.stream().filter(m -> m.startsWith(\"a\")).toList(); }"), False),
    ("S1612 zanjir davomi tegilmaydi", "java:S1612", MAIN,
     wrap("void t() { rows.stream().filter(c -> c.getDay().isAfter(d)).toList(); }"), False),
    ("S1612 allaqachon havola", "java:S1612", MAIN,
     wrap("void t() { rows.stream().filter(Objects::nonNull).map(Row::id).toList(); }"), False),
    ("S1612 satr ichidagi lambda matni tegilmaydi", "java:S1612", MAIN,
     wrap("String s = \"x -> x.foo()\";"), False),
    # java:S5838 maxsus assertion
    ("S5838 isEqualTo(\"\")", "java:S5838", TEST,
     wrap("void t() { assertThat(cell.getStringCellValue()).as(\"bo'sh\").isEqualTo(\"\"); }"), True),
    ("S5838 size()", "java:S5838", TEST,
     wrap("void t() { assertThat(list.size()).isEqualTo(3); }"), True),
    ("S5838 toString()", "java:S5838", TEST,
     wrap("void t() { assertThat(x.toString()).isEqualTo(\"X[1]\"); }"), True),
    ("S5838 Map.get", "java:S5838", TEST,
     wrap("void t() { Map<String, String> labels = load();\n"
          "assertThat(labels.get(\"a\")).isEqualTo(\"b\"); }"), True),
    ("S5838 hasSize toza", "java:S5838", TEST,
     wrap("void t() { assertThat(list).hasSize(3); assertThat(cell).isEmpty(); }"), False),
    ("S5838 List.get(0) tegilmaydi", "java:S5838", TEST,
     wrap("void t() { List<String> items = load();\n"
          "assertThat(items.get(0)).isEqualTo(\"a\"); }"), False),
    ("S5838 toString zanjir davomi bilan tegilmaydi", "java:S5838", TEST,
     wrap("void t() { assertThat(x.toString()).isEqualTo(\"X\").doesNotContain(\"Y\"); }"), False),
    ("S5838 main kodda tegilmaydi", "java:S5838", MAIN,
     wrap("void t() { assertThat(list.size()).isEqualTo(3); }"), False),
    # java:S3415 argument tartibi
    ("S3415 AssertJ konstanta actual o'rnida", "java:S3415", TEST,
     wrap("void t() { assertThat(EXPECTED).isEqualTo(compute()); }"), True),
    ("S3415 AssertJ Sinf.KONSTANTA actual o'rnida", "java:S3415", TEST,
     wrap("void t() { assertThat(DbLocks.TIMEOUT).isEqualTo(Duration.ofSeconds(3)); }"), True),
    ("S3415 AssertJ literal actual o'rnida", "java:S3415", TEST,
     wrap("void t() { assertThat(\"abc\").isEqualTo(name()); }"), True),
    ("S3415 JUnit literal ikkinchi argumentda", "java:S3415", TEST,
     wrap("void t() { assertEquals(service.count(), 3); }"), True),
    ("S3415 JUnit satr literal ikkinchi argumentda", "java:S3415", TEST,
     wrap("void t() { assertEquals(result.name(), \"Ali\"); }"), True),
    ("S3415 JUnit to'g'ri tartib toza", "java:S3415", TEST,
     wrap("void t() { assertEquals(3, service.count()); }"), False),
    ("S3415 JUnit ikkalasi o'zgaruvchi toza", "java:S3415", TEST,
     wrap("void t() { assertEquals(expected, actual); }"), False),
    ("S3415 JUnit delta bilan tegilmaydi", "java:S3415", TEST,
     wrap("void t() { assertEquals(value(), 1.5, 0.01); }"), False),
    ("S3415 AssertJ to'g'ri tartib toza", "java:S3415", TEST,
     wrap("void t() { assertThat(compute()).isEqualTo(EXPECTED); assertThat(A).isEqualTo(B); }"), False),
    # java:S8696 value-based tur ==
    ("S8696 LocalDate o'zgaruvchisi ==", "java:S8696", MAIN,
     wrap("boolean f(LocalDate a, LocalDate b) { return a == b; }"), True),
    ("S8696 Instant !=", "java:S8696", MAIN,
     wrap("boolean f() { Instant seen = last(); return seen != other(); }"), True),
    ("S8696 Optional ==", "java:S8696", MAIN,
     wrap("boolean f(Optional<String> a) { return a == EMPTY; }"), True),
    ("S8696 DayOfWeek ==", "java:S8696", TEST,
     wrap("boolean f(LocalDate d) { return d.getDayOfWeek() == DayOfWeek.SUNDAY; }"), True),
    ("S8696 null bilan toza", "java:S8696", MAIN,
     wrap("boolean f(LocalDate a) { return a == null || a != null; }"), False),
    ("S8696 equals bilan toza", "java:S8696", MAIN,
     wrap("boolean f(LocalDate a, LocalDate b) { return a.equals(b); }"), False),
    ("S8696 boshqa tur ==", "java:S8696", MAIN,
     wrap("boolean f(Long a, Status s) { return a == 0 || s == Status.OPEN; }"), False),
    # java:S1135 TODO
    ("S1135 //TODO", "java:S1135", MAIN,
     wrap("void f() { // TODO: keshlash\n }"), True),
    ("S1135 javadocdagi TODO", "java:S1135", MAIN,
     wrap("/**\n * <p>TODO: replika\n */ void f() {}"), True),
    ("S1135 satrdagi TODO tegilmaydi", "java:S1135", MAIN,
     wrap("String s = \"TODO list\";"), False),
    ("S1135 so'z ichidagi todo tegilmaydi", "java:S1135", MAIN,
     wrap("// mastodon va todos emas\nvoid f() {}"), False),
    ("S1135 Cheklov izohi toza", "java:S1135", MAIN,
     wrap("// Cheklov: replikada ikki marta yuradi.\nvoid f() {}"), False),
    # java:S1068 va java:S1144 ishlatilmagan private
    ("S1068 ishlatilmagan private maydon", "java:S1068", TEST,
     wrap("private static final Long ADMIN_ID = 30L;\nvoid f() {}"), True),
    ("S1068 ishlatilgan private maydon", "java:S1068", TEST,
     wrap("private final Long id = 3L;\nLong f() { return id; }"), False),
    ("S1068 annotatsiyali maydon tegilmaydi", "java:S1068", MAIN,
     wrap("@Autowired\nprivate Service service;\nvoid f() {}"), False),
    ("S1068 serialVersionUID tegilmaydi", "java:S1068", MAIN,
     wrap("private static final long serialVersionUID = 1L;"), False),
    ("S1068 Lombok sinfi tegilmaydi", "java:S1068", MAIN,
     "import lombok.Data;\n@Data class A {\n private String name;\n}\n", False),
    ("S1144 ishlatilmagan private metod", "java:S1144", TEST,
     wrap("private static Day cell(Long id) { return null; }\nvoid f() {}"), True),
    ("S1144 chaqirilgan private metod", "java:S1144", TEST,
     wrap("private int two() { return 2; }\nint f() { return two(); }"), False),
    ("S1144 @MethodSource satrida nomlangan metod", "java:S1144", TEST,
     wrap("@ParameterizedTest\n@MethodSource(\"cells\")\nvoid f(int c) {}\n"
          "private static Stream<Integer> cells() { return null; }"), False),
    ("S1144 metod havolasi bilan ishlatilgan", "java:S1144", MAIN,
     wrap("private int two() { return 2; }\nvoid f() { run(this::two); }"), False),
    ("S1144 annotatsiyali private metod tegilmaydi", "java:S1144", MAIN,
     wrap("@PostConstruct\nprivate void init() {}"), False),
    # java:S5853 ketma-ket assertThat
    ("S5853 bir xil subyekt ketma-ket", "java:S5853", TEST,
     wrap("void t() {\nassertThat(ids).containsAll(A);\nassertThat(ids).containsAll(B);\n}"), True),
    ("S5853 turli subyekt toza", "java:S5853", TEST,
     wrap("void t() {\nassertThat(ids).containsAll(A);\nassertThat(names).containsAll(B);\n}"), False),
    ("S5853 extracting bilan tegilmaydi", "java:S5853", TEST,
     wrap("void t() {\nassertThat(rows).extracting(Row::id).contains(1);\n"
          "assertThat(rows).extracting(Row::name).contains(\"a\");\n}"), False),
    ("S5853 orasida boshqa gap bo'lsa tegilmaydi", "java:S5853", TEST,
     wrap("void t() {\nassertThat(ids).isNotEmpty();\nrun();\nassertThat(ids).contains(1);\n}"), False),
    # java:S1488 vaqtinchalik o'zgaruvchi
    ("S1488 T x = ...; return x;", "java:S1488", MAIN,
     wrap("Service f() {\n  Service s = build(a, b);\n  return s;\n}"), True),
    ("S1488 darhol return toza", "java:S1488", MAIN,
     wrap("Service f() {\n  return build(a, b);\n}"), False),
    ("S1488 o'zgaruvchi oraliqda ishlatilsa toza", "java:S1488", MAIN,
     wrap("Service f() {\n  Service s = build(a, b);\n  s.init();\n  return s;\n}"), False),
    ("S1488 boshqa nom qaytarilsa toza", "java:S1488", MAIN,
     wrap("Service f() {\n  Service s = build(a, b);\n  return other;\n}"), False),
    # java:S1845 faqat registr bilan farq
    ("S1845 RETRIES va retries", "java:S1845", MAIN,
     wrap("static final String RETRIES = \"x\";\n"
          "private final AtomicLong retries = new AtomicLong();"), True),
    ("S1845 final bo'lmagan juft Sonar bayroqlamadi", "java:S1845", MAIN,
     wrap("private static final int DOORS = 3;\nprivate List<Door> doors;"), False),
    ("S1845 turli nomlar toza", "java:S1845", MAIN,
     wrap("static final String RETRIES = \"x\";\n"
          "private final AtomicLong attempts = new AtomicLong();"), False),
    # java:S8694 va S5778 kengaytmalari (ikkinchi va uchinchi aylana)
    ("S8694 LocalDateTime.of(2026, 10, 2, 8, 30) testda", "java:S8694", TEST,
     wrap("void t() { var at = LocalDateTime.of(2026, 10, 2, 8, 30); }"), True),
    ("S5778 argumentdagi getId() ikkinchi chaqiruv", "java:S5778", TEST,
     wrap("void t() { assertThatThrownBy(() -> service.overrideDay(tabel.getId(), request))"
          ".isInstanceOf(IllegalStateException.class); }"), True),
    ("S5778 ichki lambda: tashqi zanjir ikki chaqiruv", "java:S5778", TEST,
     wrap("void t() { assertThatThrownBy(() -> rethrowing(failure).run(() -> \"unused\"))"
          ".isInstanceOf(IllegalStateException.class); }"), True),
    ("S5778 ichki lambdadagi chaqiruv sanalmaydi", "java:S5778", TEST,
     wrap("void t() { assertThrows(X.class, () -> rows.forEach(r -> use(r))); }"), False),
    ("S5778 argumentdagi qiymat fabrikasi sanalmaydi", "java:S5778", TEST,
     wrap("void t() { assertThatThrownBy(() -> service.run(Duration.ofDays(1)))"
          ".isInstanceOf(IllegalStateException.class); }"), False),
    # java:S6126 \n li satr konkatenatsiyasi
    ("S6126 \\n li literallar + bilan", "java:S6126", MAIN,
     wrap("String s = \"1 0 obj\\n\"\n    + \"stream\\nA\\nendstream\";"), True),
    ("S6126 faqat ikkinchisida \\n", "java:S6126", TEST,
     wrap("String s = \"head\"\n    + \"x\\ny\";"), True),
    ("S6126 \\n siz konkatenatsiya toza", "java:S6126", MAIN,
     wrap("String s = \"a\"\n    + \"b\";"), False),
    ("S6126 o'zgaruvchi bilan qo'shish toza", "java:S6126", MAIN,
     wrap("String s = \"a\\n\" + name;"), False),
    ("S6126 o'zgaruvchidan keyingi literal zanjiri toza", "java:S6126", MAIN,
     wrap("String s = HEADER\n    + \"a\\r\\n\"\n    + \"b\\r\\n\";"), False),
    ("S6126 boshidagi literal zanjiri, keyin o'zgaruvchi", "java:S6126", MAIN,
     wrap("String s = \"a\\n\"\n    + \"b\\n\" + name\n    + \"c\";"), True),
    ("S6126 text block toza", "java:S6126", MAIN,
     wrap("String s = \"\"\"\n    a\n    b\n    \"\"\";"), False),
    ("S6126 izohdagi literal sanalmaydi", "java:S6126", MAIN,
     wrap("// \"a\\n\" + \"b\"\nString s = null;"), False),
    ("S6126 escape qilingan teskari chiziq toza", "java:S6126", MAIN,
     wrap("String s = \"a\\\\n\" + \"b\";"), False),
    # java:S3457 format satrida \n
    ("S3457 String.format da \\n", "java:S3457", MAIN,
     wrap("String s = String.format(\"x=%s\\n\", x);"), True),
    ("S3457 printf da \\n", "java:S3457", MAIN,
     wrap("void f() { out.printf(\"x=%s\\n\", x); }"), True),
    ("S3457 Locale birinchi argument", "java:S3457", MAIN,
     wrap("String s = String.format(Locale.ROOT, \"x=%s\\n\", x);"), True),
    ("S3457 formatted da \\n", "java:S3457", MAIN,
     wrap("String s = \"x=%s\\n\".formatted(x);"), True),
    ("S3457 %n bilan toza", "java:S3457", MAIN,
     wrap("String s = String.format(\"x=%s%n\", x);"), False),
    ("S3457 format o'zgaruvchi, \\n argumentda toza", "java:S3457", MAIN,
     wrap("String s = String.format(fmt, \"a\\n\");"), False),
    ("S3457 format ichida \\n yo'q, append('\\n') toza", "java:S3457", MAIN,
     wrap("void f() { sb.append(String.format(\"x=%s\", x)).append('\\n'); }"), False),
    # java:S2093 finally da qo'lda close
    ("S2093 reader finally da close", "java:S2093", TEST,
     wrap("void t() throws Exception {\n  PdfReader reader = new PdfReader(bytes);\n"
          "  try {\n    use(reader);\n  } finally {\n    reader.close();\n  }\n}"), True),
    ("S2093 catch bilan ham", "java:S2093", MAIN,
     wrap("void f() {\n  Connection c = ds.getConnection();\n  try {\n    use(c);\n"
          "  } catch (SQLException e) {\n    log(e);\n  } finally {\n    c.close();\n  }\n}"), True),
    ("S2093 try-with-resources toza", "java:S2093", TEST,
     wrap("void t() throws Exception {\n  try (PdfReader reader = new PdfReader(bytes)) {\n"
          "    use(reader);\n  }\n}"), False),
    ("S2093 null bilan boshlangan o'zgaruvchi toza", "java:S2093", MAIN,
     wrap("void f() {\n  Reader r = null;\n  try {\n    r = open();\n  } finally {\n"
          "    r.close();\n  }\n}"), False),
    ("S2093 shartli close toza", "java:S2093", MAIN,
     wrap("void f() {\n  Reader r = open();\n  try {\n    use(r);\n  } finally {\n"
          "    if (r != null) {\n      r.close();\n    }\n  }\n}"), False),
    ("S2093 finally da boshqa o'zgaruvchi toza", "java:S2093", MAIN,
     wrap("void f() {\n  Reader r = open();\n  try {\n    use(r);\n  } finally {\n"
          "    other.close();\n  }\n}"), False),
    # java:S4087 try-with-resources resursini qo'lda yopish
    ("S4087 resurs tanada close", "java:S4087", TEST,
     wrap("void t() throws Exception {\n  try (Document target = new Document()) {\n"
          "    target.open();\n    target.close();\n    assertThat(target.isOpen()).isFalse();\n  }\n}"), True),
    ("S4087 ikkinchi resurs", "java:S4087", MAIN,
     wrap("void f() throws Exception {\n  try (A a = open(); B b = open2(a)) {\n"
          "    use(b);\n    b.close();\n  }\n}"), True),
    ("S4087 tanada close yo'q", "java:S4087", MAIN,
     wrap("void f() throws Exception {\n  try (A a = open()) {\n    use(a);\n  }\n}"), False),
    ("S4087 boshqa o'zgaruvchi close", "java:S4087", MAIN,
     wrap("void f() throws Exception {\n  try (A a = open()) {\n    other.close();\n  }\n}"), False),
    ("S4087 maydon nomi bilan (this.a.close) toza", "java:S4087", MAIN,
     wrap("void f() throws Exception {\n  try (A a = open()) {\n    this.a.close();\n  }\n}"), False),
    # java:S5976 bir xil shakldagi testlar
    ("S5976 uchta bir xil shakl", "java:S5976", TEST,
     wrap(SIMILAR_TESTS), True),
    ("S5976 ikkita bir xil shakl toza", "java:S5976", TEST,
     wrap(SIMILAR_TESTS.rsplit("@Test", 1)[0]), False),
    ("S5976 shakli turlicha toza", "java:S5976", TEST,
     wrap("@Test\nvoid a() {\n  var r = parser.parse(\"x\");\n  assertThat(r.size()).isEqualTo(1);\n}\n"
          "@Test\nvoid b() {\n  var r = parser.read(\"y\");\n  assertThat(r.isEmpty()).isTrue();\n}\n"
          "@Test\nvoid c() {\n  var r = parser.dump(\"z\");\n  assertThat(r.name()).isEqualTo(\"q\");\n}"), False),
    ("S5976 @ParameterizedTest tegilmaydi", "java:S5976", TEST,
     wrap(SIMILAR_TESTS.replace("@Test", "@ParameterizedTest")), False),
    ("S5976 main kodda tegilmaydi", "java:S5976", MAIN,
     wrap(SIMILAR_TESTS), False),
]


# space-hrm Sonar ida chiqqan holatlar (2026-10-09): "oldin" kod musbat,
# tuzatilgani manfiy.
HRM_CASES = [
    # java:S125 izoh qatori `;`, `{`, `}` bilan tugaydi
    ("S125 // izoh `;` bilan tugaydi", "java:S125", MAIN,
     wrap("void f() {\n// FIRED_TRIGGERS is NOT touched: a peer runs it right now;\nrun();\n}"), True),
    ("S125 blok izoh qatori `{` bilan tugaydi", "java:S125", MAIN,
     wrap("void f() {\n/* open the block {\n more text */\nrun();\n}"), True),
    ("S125 // izoh `}` bilan tugaydi", "java:S125", TEST,
     wrap("void f() {\n// }\nrun();\n}"), True),
    ("S125 nuqta bilan tugagan izoh toza", "java:S125", MAIN,
     wrap("void f() {\n// FIRED_TRIGGERS is NOT touched: a peer runs it right now.\nrun();\n}"), False),
    ("S125 juft {@link} bilan tugagan izoh toza", "java:S125", MAIN,
     wrap("void f() {\n// see {@link Other}\nrun();\n}"), False),
    ("S125 HTML entity bilan tugagan izoh toza", "java:S125", MAIN,
     wrap("void f() {\n// returns List&lt;String&gt;\nrun();\n}"), False),
    ("S125 Javadoc qatori toza (space-hrm Sonar i o'tkazadi)", "java:S125", MAIN,
     wrap("/**\n * Written by the same path;\n * never derived on read.\n */\nvoid f() {}"), False),
    ("S125 fayl boshidagi sarlavha toza", "java:S125", MAIN,
     wrap("void f() {}", "/* Licensed under X;\n */\n"), False),
    ("S125 satr ichidagi // toza", "java:S125", MAIN,
     wrap("String u = \"http://x;\";"), False),
    ("S125 @SuppressWarnings bilan o'ralgan toza", "java:S125", MAIN,
     wrap("@SuppressWarnings(\"java:S125\")\nvoid f() {\n// kept as a note;\nrun();\n}"), False),
    # java:S2245 bashorat qilinadigan generator, faqat main
    ("S2245 ThreadLocalRandom.current()", "java:S2245", MAIN,
     wrap("long jitter(long b) { return ThreadLocalRandom.current().nextLong(b); }"), True),
    ("S2245 new Random(", "java:S2245", MAIN,
     wrap("int roll() { return new Random().nextInt(6); }"), True),
    ("S2245 Math.random()", "java:S2245", MAIN,
     wrap("double roll() { return Math.random(); }"), True),
    ("S2245 SecureRandom toza", "java:S2245", MAIN,
     wrap("private static final SecureRandom SPREAD = new SecureRandom();\n"
          "long jitter(long b) { return SPREAD.nextLong(b); }"), False),
    ("S2245 test kodida tegilmaydi", "java:S2245", TEST,
     wrap("int roll() { return new Random(42).nextInt(6); }"), False),
    ("S2245 satr ichidagi nom tegilmaydi", "java:S2245", MAIN,
     wrap("String s = \"new Random() Math.random()\";"), False),
    # java:S2133 new X().getClass()
    ("S2133 new X().getClass()", "java:S2133", TEST,
     wrap("void t() { var enabled = new FeignConfig().getClass().getAnnotation(Enable.class); }"), True),
    ("S2133 argumentli konstruktor", "java:S2133", MAIN,
     wrap("Class<?> c() { return new Foo(a, b()).getClass(); }"), True),
    ("S2133 X.class toza", "java:S2133", TEST,
     wrap("void t() { var enabled = FeignConfig.class.getAnnotation(Enable.class); }"), False),
    ("S2133 obyektning boshqa metodi toza", "java:S2133", MAIN,
     wrap("String n() { return new Foo().getName(); }"), False),
    ("S2133 o'zgaruvchi getClass() toza", "java:S2133", MAIN,
     wrap("Class<?> c(Foo foo) { return foo.getClass(); }"), False),
    # java:S6068 hamma argument eq(...)
    ("S6068 when hamma eq", "java:S6068", TEST,
     wrap("void t() { when(importer.prepare(eq(TYPE), eq(null), eq(null),\n eq(PINFL), eq(owner))).thenReturn(x); }"), True),
    ("S6068 verify hamma eq", "java:S6068", TEST,
     wrap("void t() { verify(repo).save(eq(row)); }"), True),
    ("S6068 verify times hamma eq", "java:S6068", TEST,
     wrap("void t() { verify(repo, times(2)).find(eq(1L), eq(\"a\")); }"), True),
    ("S6068 doReturn.when hamma eq", "java:S6068", TEST,
     wrap("void t() { Mockito.doReturn(x).when(repo).find(eq(1L)); }"), True),
    ("S6068 Mockito.when hamma eq", "java:S6068", TEST,
     wrap("void t() { Mockito.when(repo.find(eq(1L))).thenReturn(x); }"), True),
    ("S6068 bittasi any() toza", "java:S6068", TEST,
     wrap("void t() { when(repo.find(eq(1L), any())).thenReturn(x); }"), False),
    ("S6068 xom qiymatlar toza", "java:S6068", TEST,
     wrap("void t() { when(importer.prepare(TYPE, null, null, PINFL, owner)).thenReturn(x);\n"
          "verify(repo).save(row); }"), False),
    ("S6068 verify aralash toza", "java:S6068", TEST,
     wrap("void t() { verify(repo).find(eq(1), anyString()); }"), False),
    ("S6068 argumentsiz chaqiruv toza", "java:S6068", TEST,
     wrap("void t() { when(repo.findAll()).thenReturn(x); verify(repo).flush(); }"), False),
    ("S6068 eq ga o'xshash nom toza", "java:S6068", TEST,
     wrap("void t() { when(repo.find(eqOf(1L))).thenReturn(x); }"), False),
    # java:S5838 kengaytma
    ("S5838 massiv length isGreaterThan", "java:S5838", TEST,
     wrap("void t() { byte[] withPhoto = load(); byte[] without = load();\n"
          "assertThat(withPhoto.length).isGreaterThan(without.length); }"), True),
    ("S5838 massiv length isEqualTo", "java:S5838", TEST,
     wrap("void t() { byte[] data = load();\nassertThat(data.length).isEqualTo(3); }"), True),
    ("S5838 size() isGreaterThan", "java:S5838", TEST,
     wrap("void t() { assertThat(rows.size()).isGreaterThan(2); }"), True),
    ("S5838 contains isFalse as bilan", "java:S5838", TEST,
     wrap("void t() { assertThat(violated.contains(\"endDate\")).as(\"violated: %s\", violated).isFalse(); }"), True),
    ("S5838 contains isTrue", "java:S5838", TEST,
     wrap("void t() { assertThat(names.contains(\"a\")).isTrue(); }"), True),
    ("S5838 massiv bo'lmagan length maydoni toza", "java:S5838", TEST,
     wrap("void t() { assertThat(dto.length).isGreaterThan(0); }"), False),
    ("S5838 hasSizeGreaterThan toza", "java:S5838", TEST,
     wrap("void t() { assertThat(withPhoto).hasSizeGreaterThan(without.length); }"), False),
    ("S5838 doesNotContain toza", "java:S5838", TEST,
     wrap("void t() { assertThat(violated).doesNotContain(\"endDate\"); }"), False),
    ("S5838 contains zanjir davomi bilan tegilmaydi", "java:S5838", TEST,
     wrap("void t() { assertThat(names.contains(\"a\")).isTrue().describedAs(\"x\"); }"), False),
    # java:S5841 bo'sh kolleksiyada o'tadigan assertionlar
    ("S5841 var to'plam doesNotContain", "java:S5841", TEST,
     wrap("void t() { var violated = checks.stream().map(Check::path).collect(Collectors.toSet());\n"
          "assertThat(violated).doesNotContain(\"endDate\"); }"), True),
    ("S5841 List allMatch", "java:S5841", TEST,
     wrap("void t() { List<String> names = load();\nassertThat(names).allMatch(n -> n.startsWith(\"a\")); }"), True),
    ("S5841 allSatisfy as bilan", "java:S5841", TEST,
     wrap("void t() { List<Row> rows = load();\nassertThat(rows).as(\"rows\").allSatisfy(r -> check(r)); }"), True),
    ("S5841 noneMatch", "java:S5841", TEST,
     wrap("void t() { Set<String> names = load();\nassertThat(names).noneMatch(String::isBlank); }"), True),
    ("S5841 doesNotContainAnyElementsOf", "java:S5841", TEST,
     wrap("void t() { List<String> names = load();\nassertThat(names).doesNotContainAnyElementsOf(banned); }"), True),
    ("S5841 hasSize(0) keyin ham", "java:S5841", TEST,
     wrap("void t() { List<String> names = load();\nassertThat(names).hasSize(0).doesNotContain(\"a\"); }"), True),
    ("S5841 isNotEmpty oldin toza", "java:S5841", TEST,
     wrap("void t() { List<String> names = load();\nassertThat(names).isNotEmpty().doesNotContain(\"a\"); }"), False),
    ("S5841 hasSize oldin toza", "java:S5841", TEST,
     wrap("void t() { List<String> names = load();\nassertThat(names).hasSize(2).allMatch(n -> ok(n)); }"), False),
    ("S5841 hasSizeGreaterThan oldin toza", "java:S5841", TEST,
     wrap("void t() { List<String> names = load();\n"
          "assertThat(names).as(\"n\").hasSizeGreaterThan(0).noneMatch(String::isBlank); }"), False),
    ("S5841 contains oldin toza", "java:S5841", TEST,
     wrap("void t() { List<String> names = load();\nassertThat(names).contains(\"a\").doesNotContain(\"b\"); }"), False),
    ("S5841 oldingi statementda hasSize toza", "java:S5841", TEST,
     wrap("void t() { List<String> names = load();\nassertThat(names).hasSize(2);\n"
          "assertThat(names).doesNotContain(\"a\"); }"), False),
    ("S5841 satr doesNotContain toza", "java:S5841", TEST,
     wrap("void t() { String sql = build();\nassertThat(sql).doesNotContain(\"DROP\"); }"), False),
    ("S5841 noma'lum tur toza", "java:S5841", TEST,
     wrap("void t(CapturedOutput output) { assertThat(output).doesNotContain(\"secret\"); }"), False),
    ("S5841 metod chaqiruvi actual toza", "java:S5841", TEST,
     wrap("List<String> names() { return load(); }\n"
          "void t() { assertThat(names()).doesNotContain(\"a\"); }"), False),
    ("S5841 isEmpty toza", "java:S5841", TEST,
     wrap("void t() { List<String> names = load();\nassertThat(names).isEmpty(); }"), False),
    ("S5841 List.of(a) bo'sh emas toza", "java:S5841", TEST,
     wrap("void t() { assertThat(List.of(first, second)).allSatisfy(r -> check(r)); }"), False),
    ("S5841 extracting dan keyin toza", "java:S5841", TEST,
     wrap("void t() { List<Row> rows = load();\nassertThat(rows).extracting(Row::id).doesNotContainNull(); }"), False),
    ("S5841 main kodda tegilmaydi", "java:S5841", MAIN,
     wrap("void t() { List<String> names = load();\nassertThat(names).doesNotContain(\"a\"); }"), False),
    # java:S3415 konstanta actual o'rnida, kutilgan qiymatli boshqa metodlar
    ("S3415 hasToString konstanta actual", "java:S3415", TEST,
     wrap("void t() { assertThat(IdentityDocument.EMPTY).hasToString(\"IdentityDocument[series=absent]\"); }"), True),
    ("S3415 hasSameHashCodeAs konstanta actual", "java:S3415", TEST,
     wrap("void t() { assertThat(EMPTY).hasSameHashCodeAs(copy()); }"), True),
    ("S3415 isEqualToIgnoringCase konstanta actual", "java:S3415", TEST,
     wrap("void t() { assertThat(Status.ACTIVE).isEqualToIgnoringCase(name()); }"), True),
    ("S3415 hasToString lokal o'zgaruvchi toza", "java:S3415", TEST,
     wrap("void t() { var empty = IdentityDocument.EMPTY;\nassertThat(empty).hasToString(\"IdentityDocument[]\"); }"), False),
    ("S3415 hasToString haqiqiy qiymat toza", "java:S3415", TEST,
     wrap("void t() { assertThat(document).hasToString(\"IdentityDocument[]\"); }"), False),
    ("S3415 hasToString ikkalasi konstanta toza", "java:S3415", TEST,
     wrap("void t() { assertThat(Type.EMPTY).hasToString(EXPECTED_TEXT); }"), False),
    # java:S4144 bir xil tanali metodlar
    ("S4144 ikki metod bir xil tana", "java:S4144", MAIN,
     wrap("void normalizeCreate(Dto d) {\n if (d == null) {\n return;\n }\n fill(d);\n log(d);\n}\n"
          "void normalizeUpdate(Dto d) {\n if (d == null) {\n return;\n }\n fill(d);\n log(d);\n}"), True),
    ("S4144 bo'sh joyi boshqacha bo'lsa ham bir xil", "java:S4144", TEST,
     wrap("@Test void a() {\n  load();\n  check(1);\n}\n@Test void b() { load();   check(1); }"), True),
    ("S4144 literal farq qiladi toza", "java:S4144", MAIN,
     wrap("void a() { load(); check(1); }\nvoid b() { load(); check(2); }"), False),
    ("S4144 bitta statement toza", "java:S4144", MAIN,
     wrap("int a() { return load(); }\nint b() { return load(); }"), False),
    ("S4144 parametr turi boshqa toza", "java:S4144", MAIN,
     wrap("void a(CreateDto d) { fill(d); log(d); }\nvoid b(UpdateDto d) { fill(d); log(d); }"), False),
    ("S4144 bir nomli overload toza", "java:S4144", MAIN,
     wrap("void a(int x) { fill(x); log(x); }\nvoid a(long x) { fill(x); log(x); }"), False),
    ("S4144 turli ichki sinflar toza", "java:S4144", MAIN,
     wrap("static class P { void a() { load(); check(); } }\nstatic class Q { void b() { load(); check(); } }"), False),
    ("S4144 konstruktorlar toza", "java:S4144", MAIN,
     wrap("A(int x) { this.x = x; init(); }\nA(long y) { this.x = y; init(); }"), False),
    ("S4144 @SuppressWarnings bilan toza", "java:S4144", MAIN,
     wrap("void a() { load(); check(); }\n@SuppressWarnings(\"java:S4144\")\nvoid b() { load(); check(); }"), False),
    # java:S6878 faqat accessor ishlatilgan pattern o'zgaruvchisi (record shu faylda)
    ("S6878 case Rec r -> r.delay()", "java:S6878", MAIN,
     wrap("record Retry(long delay) {}\nlong f(Object d) { return switch (d) {\n"
          "case Retry r -> r.delay();\ndefault -> 0;\n}; }"), True),
    ("S6878 case blokida barcha accessorlar", "java:S6878", MAIN,
     wrap("record Pair(long a, long b) {}\nlong f(Object d) { return switch (d) {\n"
          "case Pair p -> {\n long s = p.a();\n yield s + p.b();\n}\ndefault -> 0;\n}; }"), True),
    ("S6878 ichki Decision.RetryAfter", "java:S6878", MAIN,
     wrap("sealed interface Decision { record RetryAfter(long delay) implements Decision {} }\n"
          "void f(Decision d) { switch (d) {\ncase Decision.RetryAfter retry -> save(retry.delay());\ndefault -> {}\n} }"), True),
    ("S6878 instanceof Rec r", "java:S6878", MAIN,
     wrap("record Retry(long delay) {}\nboolean g(Object d) { if (d instanceof Retry r) { return r.delay() > 0; } return false; }"), True),
    ("S6878 komponentlarning bittasi o'qilgan toza", "java:S6878", MAIN,
     wrap("record Place(long unit, int day) {}\nvoid f(Object s) { if (s instanceof Place p) { use(p.unit()); } }"), False),
    ("S6878 butun obyekt uzatilgan toza", "java:S6878", MAIN,
     wrap("record Retry(long delay) {}\nlong f(Object d) { return switch (d) {\ncase Retry r -> use(r) + r.delay();\ndefault -> 0;\n}; }"), False),
    ("S6878 komponent bo'lmagan metod toza", "java:S6878", MAIN,
     wrap("record Retry(long delay) {}\nString f(Object d) { return switch (d) {\ncase Retry r -> r.delay() + r.toString();\ndefault -> \"\";\n}; }"), False),
    ("S6878 record emas (sinf) toza", "java:S6878", MAIN,
     wrap("class Retry { long delay() { return 1; } }\nlong f(Object d) { return switch (d) {\ncase Retry r -> r.delay();\ndefault -> 0;\n}; }"), False),
    ("S6878 noma'lum tur toza", "java:S6878", MAIN,
     wrap("long f(Object d) { return switch (d) {\ncase Retry r -> r.delay();\ndefault -> 0;\n}; }"), False),
    ("S6878 argumentli chaqiruv toza", "java:S6878", MAIN,
     wrap("record Retry(long delay) {}\nlong f(Object d) { return switch (d) {\ncase Retry r -> r.delay(1);\ndefault -> 0;\n}; }"), False),
    ("S6878 record pattern allaqachon toza", "java:S6878", MAIN,
     wrap("record Retry(long delay) {}\nlong f(Object d) { return switch (d) {\ncase Retry(var delay) -> delay;\ndefault -> 0;\n}; }"), False),
    # java:S1640 kaliti enum bo'lgan HashMap (enum shu faylda)
    ("S1640 new HashMap<Enum, V>()", "java:S1640", TEST,
     wrap("enum Language { EN, UZ }\nvoid t() { var raw = new HashMap<Language, String>(); raw.put(null, \"x\"); }"), True),
    ("S1640 Map<Enum, V> = new HashMap<>()", "java:S1640", MAIN,
     wrap("enum Language { EN, UZ }\nMap<Language, List<String>> names = new HashMap<>();"), True),
    ("S1640 @SuppressWarnings bilan toza", "java:S1640", TEST,
     wrap("enum Language { EN, UZ }\n@Test\n@SuppressWarnings(\"java:S1640\") // null key is under test\n"
          "void t() { var raw = new HashMap<Language, String>(); raw.put(null, \"x\"); }"), False),
    ("S1640 EnumMap toza", "java:S1640", MAIN,
     wrap("enum Language { EN, UZ }\nMap<Language, String> names = new EnumMap<>(Language.class);"), False),
    ("S1640 kalit enum emas toza", "java:S1640", MAIN,
     wrap("Map<String, String> names = new HashMap<>();\nvar ids = new HashMap<Long, String>();"), False),
    ("S1640 noma'lum kalit turi toza", "java:S1640", MAIN,
     wrap("Map<Language, String> names = new HashMap<>();"), False),
]
SONAR_CASES += HRM_CASES


def _project(files):
    """Vaqtinchalik loyiha: {nisbiy yo'l: matn}; (ildiz, yozilgan yo'llar)."""
    root = tempfile.mkdtemp(prefix="genius-proj-")
    paths = {}
    for rel, body in files.items():
        full = os.path.join(root, rel)
        os.makedirs(os.path.dirname(full), exist_ok=True)
        with open(full, "w", encoding="utf-8") as handle:
            handle.write(body)
        paths[rel] = full
    return root, paths


def case_hrm_loyiha_turlari():
    """S6878 va S1640: record va enum boshqa faylda e'lon qilingan (loyiha src i)."""
    root, paths = _project({
        "src/main/java/x/Retry.java": "package x;\npublic record Retry(long delay) {}\n",
        "src/main/java/x/Language.java": "package x;\npublic enum Language { EN, UZ }\n",
        "src/main/java/x/Plain.java": "package x;\npublic class Plain { long delay() { return 1; } }\n",
        "src/main/java/x/Use.java": (
            "package x;\nclass Use {\n"
            "  long f(Object d) { return switch (d) { case Retry r -> r.delay(); default -> 0; }; }\n"
            "  long g(Object d) { return switch (d) { case Plain p -> p.delay(); default -> 0; }; }\n"
            "  java.util.Map<Language, String> names = new java.util.HashMap<>();\n"
            "  java.util.Map<String, String> ids = new java.util.HashMap<>();\n}\n"),
    })
    try:
        got = check_code.analyse(paths["src/main/java/x/Use.java"])
        by_rule = {}
        for f in got:
            by_rule.setdefault(f.rule, []).append(f.line)
        missing = os.path.join(root, "src/main/java/x/Missing.java")
        unknown = ("class U { long f(Object d) { return switch (d) "
                   "{ case Retry r -> r.delay(); default -> 0; }; } }")
        return [
            ("S6878 boshqa fayldagi record (3-qator)", by_rule.get("java:S6878") == [3]),
            ("S1640 boshqa fayldagi enum (5-qator)", by_rule.get("java:S1640") == [5]),
            ("fayl diskda yo'q bo'lsa faqat o'z matni",
             not [f for f in check_code.check_text(unknown, missing)
                  if f.rule == "java:S6878"]),
        ]
    finally:
        shutil.rmtree(root, ignore_errors=True)


def case_hrm_xabarlar():
    """Xabar tuzatish yo'lini aytadi: S5838 -> S5841 ogohlantirishi, S1640 -> null kalit."""
    def msg(rule, path, code):
        return " ".join(f.message for f in check_code.check_text(code, path) if f.rule == rule)
    contains = msg("java:S5838", TEST,
                   wrap("void t() { assertThat(violated.contains(\"a\")).isFalse(); }"))
    empty_enum = msg("java:S1640", MAIN,
                     wrap("enum L { EN }\nMap<L, String> m = new HashMap<>();"))
    s5841 = msg("java:S5841", TEST,
                wrap("void t() { List<String> n = load();\nassertThat(n).doesNotContain(\"a\"); }"))
    return [
        ("S5838 doesNotContain xabari S5841 ni eslatadi",
         "doesNotContain" in contains and "java:S5841" in contains and "isEmpty()" in contains),
        ("S5838 contains isTrue xabarida S5841 ogohlantirishi yo'q",
         "S5841" not in msg("java:S5838", TEST,
                            wrap("void t() { assertThat(n.contains(\"a\")).isTrue(); }"))),
        ("S1640 xabari null kalit va @SuppressWarnings ni aytadi",
         "Null kalit" in empty_enum and "java:S1640" in empty_enum),
        ("S5841 xabari tuzatish yo'lini aytadi",
         "isEmpty()" in s5841 and "isNotEmpty()" in s5841),
    ]


def case_sonar_qoidalari():
    rows = []
    for name, rule, path, code, expect in SONAR_CASES:
        got = [f for f in check_code.check_text(code, path) if f.rule == rule]
        rows.append(("%s (topildi: %d)" % (name, len(got)), bool(got) == expect))
    return rows


def case_sonar_havolalar():
    """Har Sonar topilmasining ref= bo'limi indeksda bor va mavzuga mos."""
    import docref
    expect = {
        "sonarqube 28.3": "import",
        "sonarqube 28.4": "private",
        "sonarqube 28.6": "todo",
        "sonarqube 28.17": "main kod",
        "sonarqube 30.3": "assertthrows",
        "sonarqube 30.15": "test qoidalari",
        "sonarqube 13.6": "resurslarni yopish",
        "clean-code 24.2": "metod havolasi",
        "clean-code 22.3": "clock",
        "sonarqube 28.5": "kommentariyaga",
        "sonarqube 26.5": "random",
        "sonarqube 28.14": "bir xil ishni",
    }
    titles = section_titles()
    seen = {}
    for _, rule, path, code, _ in SONAR_CASES:
        for f in check_code.check_text(code, path):
            if f.rule == rule:
                seen.setdefault(f.ref, set()).add(rule)
    rows = []
    for ref, rules in sorted(seen.items()):
        title = titles.get(tuple(ref.split()), "").lower()
        rows.append(("%s (%s) -> %s" % (ref, ", ".join(sorted(rules)), title[:50]),
                     docref.by_ref(ref) == ref and expect.get(ref, "?") in title))
    rows.append(("kutilgan havolalarning hammasi ishlatilgan",
                 set(expect) == set(seen)))
    return rows


FLAKY_CASES = [
    # (nom, yo'l, kod, kutilgan topilmalar soni)
    ("getSystemProperties().put", TEST,
     wrap("void t() { env.getSystemProperties().put(\"a\", \"b\"); }"), 1),
    ("getSystemEnvironment().put", TEST,
     wrap("void t() { env.getSystemEnvironment().put(\"A\", \"b\"); }"), 1),
    ("System.setProperty tiklashsiz", TEST,
     wrap("void t() { System.setProperty(\"a\", \"b\"); }"), 1),
    ("System.setProperty + clearProperty toza", TEST,
     wrap("void t() { System.setProperty(\"a\", \"b\"); }\n"
          "void u() { System.clearProperty(\"a\"); }"), 0),
    ("MapPropertySource addFirst toza", TEST,
     wrap("void t() { env.getPropertySources().addFirst(new MapPropertySource(\"x\", m)); }"), 0),
    ("getSystemProperties().get toza", TEST,
     wrap("String t() { return env.getSystemProperties().get(\"a\"); }"), 0),
    ("main kodda tegilmaydi", MAIN,
     wrap("void t() { System.setProperty(\"a\", \"b\"); }"), 0),
    ("static final JavaClasses importi", TEST,
     wrap("static final JavaClasses CLASSES = new ClassFileImporter().importPackages(\"x\");"), 1),
    ("static maydon + @BeforeAll importi", TEST,
     wrap("static JavaClasses classes;\n"
          "@BeforeAll static void load() { classes = new ClassFileImporter().importPackages(\"x\"); }"), 1),
    ("SoftReference keshi toza", TEST,
     wrap("static SoftReference<JavaClasses> CACHE = new SoftReference<>(null);"), 0),
    ("static maydon umumiy yordamchidan toza", TEST,
     wrap("static final JavaClasses CLASSES = ArchCache.production();"), 0),
    ("lokal o'zgaruvchi toza", TEST,
     wrap("void t() { JavaClasses c = new ClassFileImporter().importPackages(\"x\"); }"), 0),
    ("main kodda static graf tegilmaydi", MAIN,
     wrap("static final JavaClasses CLASSES = new ClassFileImporter().importPackages(\"x\");"), 0),
]


def case_flaky_qoidalar():
    rows = []
    for name, path, code, expect in FLAKY_CASES:
        got = [f for f in check_code.check_text(code, path)
               if f.ref == "testing 15.14"]
        rows.append(("%s (topildi: %d)" % (name, len(got)), len(got) == expect))
    import docref
    rows.append(("testing 15.14 indeksda bor", docref.by_ref("testing 15.14") == "testing 15.14"))
    return rows


SECTIONS = [
    ("Topilishi kerak", case_topilishi),
    ("Qo'llanmaga ulanish", case_qollanma),
    ("Kalit bir nechta bo'limda", case_kalit_bolimlar),
    ("Yolg'on ishga tushish bo'lmasligi kerak", case_yolgon_topilma),
    ("Izohli catch va tranzaksiya chegarasi", case_tranzaksiya),
    ("Commit dan keyingi chaqiruv va tur nomi", case_commitdan_keyin),
    ("NOSONAR, @SuppressWarnings va test kodi", case_nosonar),
    ("Keng catch xabari", case_keng_catch),
    ("Sonar qoidalari: musbat va manfiy", case_sonar_qoidalari),
    ("Sonar qoidalari: qo'llanma havolasi", case_sonar_havolalar),
    ("Sonar qoidalari: space-hrm loyiha turlari", case_hrm_loyiha_turlari),
    ("Sonar qoidalari: space-hrm xabarlar", case_hrm_xabarlar),
    ("Test sizishi va static ArchUnit grafi", case_flaky_qoidalar),
    ("Toza fayl", case_toza_fayl),
    ("Ko'p fayl", case_kop_fayl),
    ("Zanjir majburlanadi", case_zanjir),
    ("Hook javobi (zanjir bajarilgan)", case_hook_javobi),
    ("Edit: faqat yangi topilma", case_edit_yangi),
    ("Java bo'lmagan yo'l: erta chiqish", case_erta_chiqish),
    ("Boshqa papkadan (global o'rnatish)", case_boshqa_papka),
    ("Java bo'lmagan proyektda jim", case_java_emas),
    ("Jonli holatga tegilmadi", case_jonli_holat),
]


def main(argv=()):
    for path in (BAD, GOOD, LITERALS, TX_OK, TX, MEDIUM, TX_AFTER, TX_VERSION,
                 TX_FACTORY, SUPPRESSED):
        if not os.path.exists(path):
            print("sinov fayli yo'q: %s" % path)
            return 1
    LIVE_BEFORE.update(live_snapshot())
    return testkit.run_cases(SECTIONS, argv, headers=True)


if __name__ == "__main__":
    try:
        sys.exit(main(sys.argv[1:]))
    finally:
        shutil.rmtree(STATE, ignore_errors=True)
