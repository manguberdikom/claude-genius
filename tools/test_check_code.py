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
    raw_skipped = run_hook(GOOD)
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


SECTIONS = [
    ("Topilishi kerak", case_topilishi),
    ("Qo'llanmaga ulanish", case_qollanma),
    ("Kalit bir nechta bo'limda", case_kalit_bolimlar),
    ("Yolg'on ishga tushish bo'lmasligi kerak", case_yolgon_topilma),
    ("Izohli catch va tranzaksiya chegarasi", case_tranzaksiya),
    ("Commit dan keyingi chaqiruv va tur nomi", case_commitdan_keyin),
    ("NOSONAR, @SuppressWarnings va test kodi", case_nosonar),
    ("Keng catch xabari", case_keng_catch),
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
