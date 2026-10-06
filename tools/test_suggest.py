#!/usr/bin/env python3
"""suggest_sections.py uchun sinovlar.

    python3 tools/test_suggest.py

Hook har bir so'rovda ishlaydi, shuning uchun ikki xato ham qimmat:

  - Mavzuli so'rovga jim turish: model kerakli bo'limni ko'rmaydi va
    o'z umumiy bilimidan javob beradi. Bu jim sodir bo'ladi.
  - Mavzusiz so'rovga taklif berish: har navbatda shovqin qo'shiladi,
    kontekst behuda sarflanadi va taklifga ishonch yo'qoladi.

Shuning uchun ikkala tomon ham sinaladi. suggest_sections.py dagi
MIN_SCORE, MIN_RARE_IDF va MIN_SPECIFIC_LEN shu ro'yxatda sozlangan.
Hookning o'zi (stdin JSON, chiqish shakli, indekssiz klon) ham sinaladi:
suggest() to'g'ri bo'lsa ham, buzuq chiqish CI dan yashil o'tib ketardi.

Ma'lum cheklov: bitta mavhum so'z va to'ldiruvchi so'zlardan iborat
so'rov ("tranzaksiyani qayerda ochaman") jim qoladi, chunki bitta mos
so'z dalil uchun yetarli emas. Bu ataylab: shu shartni yumshatish
"tezlik", "aniqlik" kabi mavhum otlarni ham o'tkazib yuboradi, ular bu
korpusda texnik atamalardan ham kamyobroq. Yolg'iz o'zi yetadigan so'z
atama lug'atidan bo'lishi kerak: taxallus so'zi, GLOSSARY.md dagi bir
so'zli atama (deadlock, heap, latency) yoki sarlavhada CamelCase yoki
kamida 4 harfli qisqartma bilan yozilgan nom (StampedLock, OSIV). Uch
harfli qisqartma (ZGC, JVM, DTO) bunga kirmaydi. Bunday so'rov uchun
`doc.sh find` bor va u bir so'zli so'rovni mukammal bajaradi.

Bo'lim tanasining kalit so'zlarini indekslash ham sinab ko'rildi va
natijani o'zgartirmadi, shuning uchun olib tashlandi: indeks 304 KB ga,
build uch barobarga oshar edi. index/exceptions.tsv boshqa, tor g'oya:
faqat exception nomlari, nasr va sarlavhadan, misol va umumiy nomlarsiz.
"""

import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import hookio  # noqa: E402
import suggest_sections as S  # noqa: E402
import testkit  # noqa: E402

# Hook faqat Java proyektida yoki klonning o'zida ishlaydi
# (hookio.active). Sinovlar vaqtinchalik papkada yuradi, shu yerda esa
# tekshirilayotgan narsa gating emas: ildiz klonga qo'yiladi. Gating ning
# o'z sinovlari tools/test_hookio.py da.
ROOT = os.path.dirname(HERE)
os.environ["CLAUDE_PROJECT_DIR"] = ROOT

# So'rov -> kutilgan hujjat [, qabul qilinadigan bo'limlar]. Taklif
# ro'yxatida o'sha hujjatdan kamida bitta bo'lim bo'lishi kerak; bo'limlar
# berilgan bo'lsa, ulardan biri. Raqam to'liq solishtiriladi: prefiks
# bo'yicha '1' '10.x' ga ham mos kelib qolardi.
EXPECTED = [
    ("tashqi servisga chaqiruvni ishonchli qilish kerak, timeout va qayta urinish",
     "patterns"),
    ("circuit breaker qo'yaymi yoki bulkhead", "patterns", {"17.2", "17.3"}),
    ("Testcontainers bilan PostgreSQL test yozmoqchiman", "testing", {"8.2"}),
    ("test flaky bo'lib qoldi, nima qilaman", "testing"),
    ("Sonar cognitive complexity dan shikoyat qilyapti", "sonarqube"),
    ("quality gate o'tmayapti, coverage past", "sonarqube"),
    ("deadlock chiqdi, izolyatsiya darajasini qanday tanlayman", "architect",
     {"19.3"}),
    ("connection pool kattaligini qanday hisoblayman", "architect"),
    ("bu funksiya nomi to'g'rimi", "clean-code"),
    # Qo'shimcha kesish va sinonim jadvali bilan ishlaydigan holatlar.
    ("metod juda uzun, qanday bo'laklayman", "clean-code"),
    ("keshni qachon invalidatsiya qilaman", "architect"),
    ("saga pattern kerakmi yoki outbox", "patterns"),
    ("N+1 so'rov muammosi", "patterns"),
    # GLOSSARY.md dagi bir so'zli atama yolg'iz o'zi dalil.
    ("postgresda deadlock bo'lyapti, ikki tranzaksiya bir-birini kutyapti",
     "architect", {"11.10", "19.10", "22.8"}),
    ("heap to'lib OutOfMemoryError beryapti", "architect", {"10.7", "10.9"}),
    ("API sekin, latency 2 soniya", "architect"),
    # Sarlavhadagi texnik nom (CamelCase, 4 harfli qisqartma) ham dalil.
    ("OSIV yoqilganmi tekshir", "code-review", {"19.8"}),
    ("StampedLock ishlatsam bo'ladimi", "architect", {"11.4"}),
    ("DataJpaTest qanday yoziladi", "testing", {"7.4"}),
    # Uzun raqam atama bo'lib qoladi, qisqasi esa yo'q (SILENT ga qarang).
    ("ProblemDetail RFC 9457 formatida xato qaytarish", "patterns", {"7.10"}),
    # Sonar kaliti index/rules.tsv orqali to'g'ridan bo'limga boradi.
    # Avval 1.4 (scanner mexanikasi) chiqardi: u kalitni misol sifatida
    # tilga oladi. Illustrativ eslatma pastga tushgandan keyin kalitni
    # TUSHUNTIRGAN bo'limlar qoldi (build_index.explaining).
    ("java:S2259 ni tuzat", "sonarqube", {"3.1", "13.4", "40.1"}),
    ("squid:S1192 topildi", "sonarqube"),
    # Bob taxallusi bob raqamini beradi.
    ("API compatibility buzilmaydimi", "code-review", {"37"}),
    # Regressiya qo'riqchilari: stack trace va memory tozalashi bir
    # qatorlik exception nomiga va "in-memory" ga tegmasligi kerak.
    ("LazyInitializationException chiqyapti, qanday tuzataman", "patterns"),
    ("DataAccessException hierarchy nima", "patterns"),
    ("in-memory baza bilan test yozsam bo'ladimi", "testing"),
    # Telefon va Windows o'zbek klaviaturasi apostrofi (U+02BB, U+2019):
    # avval "yo" va "qolgan" ga bo'linib, hook jim qolardi.
    ("yoʻqolgan yangilanish muammosi", "architect", {"22.5"}),
    ("yo’qolgan yangilanish muammosi", "architect", {"22.5"}),
    ("aylanma bogʻliqlik xatosi", "architect", {"15.6"}),
    # FQCN oddiy nomga: avval "org.hibernate.lazyinitializationexception"
    # bitta token edi va G1GC, RBAC kabi begona bo'limlar chiqardi.
    ("org.hibernate.LazyInitializationException chiqdi, qanday tuzataman",
     "patterns", {"25.52"}),
    # Kodda `private` mavzuning o'zi, zaxira so'z sifatida tashlanmaydi.
    ("@Transactional private metodda ishlaydimi", "sonarqube", {"29.3"}),
    ("shu kodni review qil:\n@Service\npublic class OrderService {\n"
     "    @Transactional\n    private void save(Order order) {\n"
     "        repository.save(order);\n    }\n}", "sonarqube", {"29.3"}),
    # Kod parchasi: `throws`, `void` tashlanadi, Thread.sleep qoladi.
    ("shu testni review qil:\n@Test\nvoid waits() throws Exception {\n"
     "    Thread.sleep(500);\n}", "sonarqube", {"19.4", "30.5"}),
    # Prefikssiz Sonar kaliti ham kalit.
    ("S2095 resurs yopilmagan deyapti", "sonarqube", {"13.6"}),
    # Katalog bo'limi "Qoida: `java:S1192`" bilan boshlanadi va kalitning
    # boshqa bo'limlaridan oldin turadi (avval 3.10 va 23.5 chiqardi).
    ("java:S1192 ni tuzat", "sonarqube", {"27.8"}),
    # Exception nomi index/exceptions.tsv orqali: xabar so'zlari ("single",
    # "of") avval patterns 26.28 ni birinchi qo'yardi.
    ("NoUniqueBeanDefinitionException: No qualifying bean of type "
     "'PaymentGateway' available: expected single matching bean but found 2",
     "patterns", {"5.8"}),
    ("ObjectOptimisticLockingFailureException tushdi, nima qilaman",
     "patterns", {"9.23"}),
    # Korpusda yo'q exception (PSQLException): ildiz sabab xabari qoladi.
    ("saqlashda xato:\norg.postgresql.util.PSQLException: ERROR: deadlock "
     "detected\n\tat org.postgresql.core.v3.QueryExecutorImpl.receive"
     "(QueryExecutorImpl.java:2713)", "architect", {"22.8", "19.10", "11.10"}),
]

# Ko'p qatorli stack trace: frame, paket nomlari va xabar mavzu emas.
STACK_TRACE = "\n".join([
    "test yiqildi, nega?",
    "org.springframework.dao.DataIntegrityViolationException: "
    "could not execute statement",
    "\tat org.hibernate.exception.internal.SQLStateConversionDelegate"
    ".convert(SQLStateConversionDelegate.java:97)",
    "\tat com.example.order.OrderService.save(OrderService.java:42)",
    "Caused by: org.postgresql.util.PSQLException: ERROR: duplicate key",
    "  Detail: Key (email)=(a@b) already exists.",
    "\t... 42 more",
])

# Mavzusiz so'rovlar: hook butunlay jim turishi shart.
SILENT = [
    "salom",
    "rahmat, yaxshi ishladi",
    "commit qil va push qil",
    "nima qila olasan",
    "yana bir marta ko'rib chiq",
    "bu qatorni o'chir",
    "yuqoridagini tushuntirib ber",
    "qisqa javob ber",
    "tekshiruv qil",
    # Sinonim nishoni (chiroyli -> toza nomlash) yolg'iz dalil emas.
    "chiroyli qil",
    # Asboblarning o'zi haqidagi meta-savollar. Bular amalda uchradi va
    # eng yomon turdagi shovqinni berdi: "tezlik", "aniqlik", "sifat"
    # kabi mavhum otlar bu korpusda kamyob (aniqlik IDF 5.1, deadlock
    # 4.4), shuning uchun chastota ularni atama deb o'ylaydi.
    "kerakli qoidani ozi topa oladimi tezlik bilan",
    "bu qoida qanday ishlaydi",
    "sifat yaxshimi yoki yo'q",
    "qidiruv qanchalik aniq ishlayapti",
    # GLOSSARY atamasi buyruq ichida: "stack" chiqarilgan, "commit" va
    # "rule" esa yolg'iz yetarlicha kamyob emas.
    "yaxshi, endi stack ni yangila",
    "rahmat, endi commit qilib push qil",
    "bu rule nima deydi",
    # Asbobning o'ziga buyruq, qo'llanma mavzusi emas.
    "memory ga yozib qo'y",
    "memoryni tozala",
    # Yolg'iz domen oti va stack trace.
    "Notification yuborishni qo'sh",
    "OrderService da NullPointerException chiqyapti, customer null",
    STACK_TRACE,
    # Qisqa raqam: qator raqami, son, foiz.
    "OrderService.java:90 qatorda NPE, 30 ta so'rovdan 60 tasi yiqildi",
    "7 ta test yiqildi",
    # Sarlavha atamalari faqat texnik nomdan olinadi, oddiy inglizcha
    # so'z (debug, create, info, target, this) lug'atga kirmaydi.
    "debug qilib ko'r",
    "create qil yangi fayl",
    "info ber",
    "target papkani o'chir",
    "this nima",
]

# Chegaradagi so'rovlar: buyruq shaklida, lekin ichida haqiqiy mavzu so'zi
# bor ("test", "git", "nom"). Bu yerda jimlikni talab qilish noto'g'ri
# bo'lardi: "testni ishga tushir" uchun "Testni tanlab ishga tushirish"
# bo'limi aynan mos keladi. Talab - har so'rov uchun yozilgan son va
# hujjatlardan oshmasin, shunda noto'g'ri taklifning narxi bir necha
# qatordan oshmaydi. Chegara S.MAX_SUGGESTIONS ga bog'lanmaydi: aks holda
# konstanta ko'tarilsa chegara ham o'zi ko'tarilib, sinov doim o'tardi.
BORDERLINE = [
    # (so'rov, ko'pi bilan nechta, qaysi hujjatlardan, chiqishi shart bo'lim)
    ("git push qilib qoy", 1, {"clean-code"}, None),
    ("fayl nomini o'zgartir", 1, {"clean-code"}, None),
    ("testni ishga tushir", 1, {"testing"}, ("testing", "15.5")),
    # "performance" bu korpusda haqiqiy atama: "Performance regressiyasini
    # diffdan ko'rish" degan bob bor. So'rov asbob tezligi haqida bo'lsa
    # ham, so'z darajasidagi moslik buni ajrata olmaydi. Qoidani shu
    # holat uchun burish haqiqiy atamalarni yo'qotardi, shuning uchun
    # taklif chiqishi qabul qilinadi, faqat soni chegaralanadi. To'rt
    # "Performance" sarlavhasi teng ball oladi, tenglikni raqam hal qiladi
    # (avval hujjat alifbosi testing ni chetda qoldirardi).
    ("performance, tezlik, aniqlik haqida nima deysan", 4,
     {"code-review", "patterns", "testing"}, None),
]

# synonyms.tsv dagi har juftlik uchun musbat va manfiy holat (TZ-T6, QD-Q10).
# (kalit, so'rov, shu bo'limlardan biri bo'lsin yoki None, bo'lmasin).
# Musbat holat sinonimsiz o'tmaydi (sinonim olib tashlanib tekshirilgan).
# Manfiy holat: sinonim yolg'iz dalil emas va begona mavzuni tortmaydi.
SYNONYM_CASES = [
    ("entity", "entity tengligi qanday ta'minlanadi",
     {("clean-code", "15.5")}, set()),
    ("entity", "entity yarat", None, {("clean-code", "15.5")}),
    ("entitet", "entitet holatlari detached managed",
     {("code-review", "23.9")}, set()),
    ("entitet", "entitet klassini yarat", None,
     {("architect", "18.2"), ("code-review", "23.9")}),
    ("qulf", "pessimistik qulf qachon kerak", {("architect", "18.8")}, set()),
    ("qulf", "qulfni och", None, {("architect", "18.8"), ("architect", "22.6")}),
    ("lock", "lock tartibi qanday bo'lishi kerak", {("code-review", "15.4")}, set()),
    ("lock", "lock faylini o'chir", None, "jim"),
    ("inyeksiya", "field inyeksiya nega yomon",
     {("sonarqube", "14.1"), ("patterns", "25.29")}, set()),
    ("inyeksiya", "SQL inyeksiya xavfi", None,
     {("sonarqube", "14.1"), ("patterns", "25.29")}),
    # Ikki tilli sarlavha ("Maydonga Injeksiya (Field Injection)") bitta
    # tushunchani ikki marta sanamaydi.
    ("injection", "SQL injection review", None, {("patterns", "25.29")}),
    ("izchillik", "yakuniy izchillik qachon yetarli", {("patterns", "28.17")}, set()),
    ("izchillik", "kod uslubida izchillik", None, "jim"),
    ("consistency", "consistency va availability tanlovi", None,
     {("clean-code", "15.6")}),
    ("o'chirilgan qator", "jadvalda o'chirilgan qatorlar ko'p joy egallayapti",
     {("architect", "21.10")}, set()),
    # Ibora so'zlari ketma-ket bo'lishi shart.
    ("o'chirilgan qator", "qatorlar o'chirilgan", None, "jim"),
]
# Sinonim faqat qidiruvni kengaytiradi: kengaytma darajasidagi holatlar
# (so'rov, kutilgan nishon, bo'lmasligi kerak nishon).
EXPAND_CASES = [
    ("injection", "inyeksiya", None),
    ("consistency", "izchillik", None),
    ("izchillik", "consistency", None),
    ("o'chirilgan qatorlar", "bloat", None),
    ("o'chirilgan fayl", None, "bloat"),
    ("qatorlar o'chirilgan", None, "bloat"),
]

# Ishora-yozuv (sections.tsv `ishora` ustuni to'la) to'liq yozuvni
# takrorlaydi: bitta mavzuga ikki raqam berilmasin, faqat to'liq yozuv.
POINTERS = [
    # (so'rov, hujjat, chiqishi shart bo'lim, chiqmasligi shart bo'lim)
    ("memoization qanday qilinadi", "patterns", "11.17", "24.23"),
    ("structured concurrency misol", "patterns", "4.24", "24.35"),
]

# Ma'lum bo'shliqlar: chop etiladi, lekin xato hisoblanmaydi.
KNOWN_GAPS = [
    ("saga pattern kerakmi yoki outbox", "patterns 10.14 / 14.12",
     "outbox bo'limi chiqmaydi, saga bo'limlari to'rt o'rinni egallaydi"),
    ("ZGC qachon kerak", "architect 10.4",
     "uch harfli qisqartma ataylab dalil emas, aks holda 'JVM nima' ham ochiladi"),
]

# Hook chiqishida bo'lim raqami ikki marta: "17.2    17.2 Zanjirni ...".
DOUBLED_RE = re.compile(r"(\d+\.\d+)\s+\1\b")
# Indekssiz nusxaga kerak fayllar: hook, indeks yasovchi va uning importi,
# buyruq yo'lini beradigan docref.
HOOK_FILES = ("suggest_sections.py", "build_index.py", "check_docs.py",
              "review_status.py", "sonar_snapshot.py", "synonyms.tsv",
              "docref.py", "hookio.py")
# Klondan tashqarida nisbiy buyruq: oldida `/` yo'q `tools/doc.sh`.
RELATIVE_CMD_RE = re.compile(r"(?<![/\\\w])tools/doc\.sh")


def run_hook(root, raw, cwd=None):
    """raw str yoki bayt: bayt bilan BOM va UTF-8 aynan beriladi."""
    data = raw if isinstance(raw, bytes) else raw.encode("utf-8")
    # Ko'chirilgan klon shu sinovda proyekt ildizi. hookio.active() uni
    # tanimasa hook jim o'tib ketadi va har holat bo'sh chiqish bilan
    # yiqilardi; `cwd` esa ataylab boshqa papka bo'lishi mumkin.
    environ = dict(os.environ, CLAUDE_PROJECT_DIR=root)
    proc = subprocess.run(
        [sys.executable, os.path.join(root, "tools", "suggest_sections.py")],
        input=data, capture_output=True, timeout=60, cwd=cwd, env=environ)
    return proc.returncode, proc.stdout.decode("utf-8", "replace")


def context(stdout):
    """(hookEventName, additionalContext) yoki JSON buzuq bo'lsa (None, '')."""
    try:
        data = json.loads(stdout)["hookSpecificOutput"]
        return data["hookEventName"], data["additionalContext"]
    except (ValueError, KeyError, TypeError):
        return None, ""


def output_shape_ok(stdout):
    event, text = context(stdout)
    lines = text.splitlines()
    return (event == "UserPromptSubmit" and len(lines) > 1
            and lines[0].startswith("Nomzod bo'limlar") and "doc.sh show" in lines[0]
            and not any(DOUBLED_RE.search(line) for line in lines[1:])
            and "majburiyat emas" not in text)


def hook_cases():
    """Hookni subprocess bilan yurgizadi, (nom, ok, izoh) ro'yxatini beradi.

    Hammasi vaqtinchalik nusxada: indekssiz klon holatini sinash uchun
    index/ yo'q bo'lishi kerak, haqiqiy index/ dan esa boshqa jarayonlar
    shu payt o'qiyotgan bo'lishi mumkin.
    """
    out = []
    with tempfile.TemporaryDirectory() as tmp:
        os.makedirs(os.path.join(tmp, "tools"))
        for name in HOOK_FILES:
            shutil.copy2(os.path.join(HERE, name), os.path.join(tmp, "tools", name))
        shutil.copy2(os.path.join(S.ROOT, "GLOSSARY.md"), tmp)
        shutil.copytree(os.path.join(S.ROOT, "docs"), os.path.join(tmp, "docs"))
        sections = os.path.join(tmp, "index", "sections.tsv")
        prompt = EXPECTED[1][0]

        rc, stdout = run_hook(tmp, json.dumps({"prompt": prompt}))
        out.append(("indekssiz klon: o'zi yasaydi", rc == 0
                    and os.path.exists(sections) and output_shape_ok(stdout),
                    "rc=%d, %d belgi" % (rc, len(stdout))))

        index = os.path.dirname(sections)
        for name in (os.listdir(index) if os.path.isdir(index) else ()):
            os.utime(os.path.join(index, name), (1, 1))   # har qanday bobdan eski
        rc, stdout = run_hook(tmp, json.dumps({"prompt": prompt}))
        fresh = os.path.exists(sections) and os.path.getmtime(sections) > 1
        out.append(("eskirgan indeks qayta yasaladi", rc == 0 and fresh
                    and output_shape_ok(stdout), "rc=%d" % rc))

        rc, stdout = run_hook(tmp, json.dumps({"prompt": "java:S2259 ni tuzat"}))
        _, text = context(stdout)
        out.append(("Sonar kaliti: bo'lim va doc.sh rule", rc == 0
                    and output_shape_ok(stdout) and "3.1 " in text
                    and "doc.sh rule java:S2259" in text, "rc=%d" % rc))

        # Buyruq yo'li: klon ichida nisbiy (har navbat narxi o'zgarmaydi),
        # boshqa proyektda mutlaq, aks holda u yerda "No such file".
        rc, stdout = run_hook(tmp, json.dumps({"prompt": prompt}), cwd=tmp)
        _, text = context(stdout)
        out.append(("klon ichida: nisbiy tools/doc.sh", rc == 0
                    and output_shape_ok(stdout)
                    and text.startswith("Nomzod bo'limlar (tools/doc.sh show "),
                    text.splitlines()[0] if text else "rc=%d" % rc))
        other = tempfile.mkdtemp()
        try:
            rc, stdout = run_hook(tmp, json.dumps({"prompt": "java:S2259 ni tuzat"}),
                                  cwd=other)
        finally:
            shutil.rmtree(other, ignore_errors=True)
        _, text = context(stdout)
        full = os.path.join(tmp, "tools", "doc.sh").replace("\\", "/")
        out.append(("boshqa proyekt: mutlaq doc.sh", rc == 0
                    and output_shape_ok(stdout) and full in text
                    and not RELATIVE_CMD_RE.search(text),
                    text.splitlines()[0] if text else "rc=%d" % rc))

        # Windows PowerShell 5.1 pipe boshiga BOM qo'yadi, satr oxiri CRLF.
        # Avval json.load undan yiqilib, o'rnatuvchi sinovi bo'sh qolardi.
        raw = b"\xef\xbb\xbf" + json.dumps({"prompt": prompt}).encode() + b"\r\n"
        rc, stdout = run_hook(tmp, raw)
        out.append(("BOM va CRLF li stdin", rc == 0 and output_shape_ok(stdout),
                    "rc=%d, %d belgi" % (rc, len(stdout))))
        # UTF-8 dekodlashni test_hookio.py qo'riqlaydi (cp1252 oqim taqlidi).

        for name, raw in (("mavzusiz so'rov", json.dumps({"prompt": "salom"})),
                          ("buzuq JSON", "not json"),
                          ("obyekt emas", "[]")):
            rc, stdout = run_hook(tmp, raw)
            out.append((name + ": jim", rc == 0 and stdout == "",
                        "rc=%d, %d belgi" % (rc, len(stdout))))
    return out


def call_hook(prompt, state, session="s1"):
    """Hook jarayon ichida, holat papkasi vaqtinchalik: (rc, stdout)."""
    raw = json.dumps({"prompt": prompt, "session_id": session})
    res = testkit.call_main(S.main, raw, argv=["suggest_sections.py"], cwd=ROOT,
                            env={"GENIUS_STATE_DIR": state, "CLAUDE_PROJECT_DIR": ROOT})
    return res.returncode, res.stdout


def error_lines(state):
    try:
        with open(os.path.join(state, hookio.ERRORS_LOG), encoding="utf-8") as handle:
            return handle.read().splitlines()
    except OSError:
        return []


def state_cases():
    """format.json ogohlantirishi (PL-CC3) va hook xatosi izi (R6.3)."""
    out = []
    prompt = EXPECTED[1][0]
    notice = ("usage: transkript formati o'zgargan (usage qatori yo'q), "
              "python3 tools/doctor.py")
    state = tempfile.mkdtemp(prefix="suggest_state_")
    saved = os.environ.get("GENIUS_STATE_DIR")
    try:
        _, stdout = call_hook(prompt, state)
        out.append(("format.json yo'q: ogohlantirish yo'q",
                    output_shape_ok(stdout) and "usage:" not in stdout, "-"))

        with open(os.path.join(state, S.FORMAT_FILE), "w", encoding="utf-8") as handle:
            json.dump({"sabab": "usage qatori yo'q", "transkript": "x.jsonl"}, handle)
        _, stdout = call_hook(prompt, state)
        _, text = context(stdout)
        lines = text.splitlines()
        out.append(("format.json: birinchi qator ogohlantirish",
                    lines[:1] == [notice] and len(lines) > 1
                    and lines[1].startswith("Nomzod bo'limlar"),
                    lines[0] if lines else "(jim)"))
        _, stdout = call_hook(prompt, state)
        out.append(("format.json: sessiyada bir marta",
                    output_shape_ok(stdout) and "usage:" not in stdout, "-"))
        rc, stdout = call_hook("salom", state, session="s2")
        out.append(("format.json: yangi sessiya, mavzusiz so'rov",
                    rc == 0 and context(stdout) == ("UserPromptSubmit", notice),
                    context(stdout)[1][:60] or "(jim)"))

        # Kutilmagan xato: hook jim (fail-open), iz esa log da.
        real = S.suggest
        S.suggest = lambda _prompt: 1 / 0
        try:
            rc, stdout = call_hook(prompt, state, session="s2")
        finally:
            S.suggest = real
        logged = error_lines(state)
        out.append(("xato: hook jim, hook_errors.log da qator",
                    rc == 0 and stdout == "" and len(logged) == 1
                    and "\tsuggest_sections\tZeroDivisionError: " in logged[0],
                    logged[-1] if logged else "(log yo'q)"))

        # handoff ning keng except i ham shu izni qoldiradi.
        import handoff
        real_hook = handoff._hook
        handoff._hook = lambda: {}["yoq"]
        os.environ["GENIUS_STATE_DIR"] = state
        try:
            code = handoff.hook()
        finally:
            handoff._hook = real_hook
        logged = error_lines(state)
        out.append(("handoff xatosi: 0 va log qatori",
                    code == 0 and "\thandoff\tKeyError: " in logged[-1],
                    logged[-1] if logged else "(log yo'q)"))

        with open(os.path.join(state, hookio.ERRORS_LOG), "w", encoding="utf-8") as handle:
            handle.writelines("eski %d\n" % n for n in range(250))
        hookio.fail_open("sinov", ValueError("ko'p\nqatorli"))
        logged = error_lines(state)
        out.append(("hook_errors.log 200 qatorda kesiladi",
                    len(logged) == hookio.ERRORS_KEEP and logged[0] == "eski 51"
                    and logged[-1].endswith("\tsinov\tValueError: ko'p qatorli"),
                    "%d qator" % len(logged)))
    finally:
        if saved is None:
            os.environ.pop("GENIUS_STATE_DIR", None)
        else:
            os.environ["GENIUS_STATE_DIR"] = saved
        shutil.rmtree(state, ignore_errors=True)
    return out


def invariant_cases():
    """Jadval va indeks orasidagi shartlar, (nom, ok, izoh) ro'yxati.

    Sinonim nishoni sarlavhalarda yo'q so'z bo'lsa, u hech qachon mos
    kelmaydi va shunchaki shovqin: synonyms.tsv boshidagi qoida shu.
    """
    vocab = set()
    for row in S.read_tsv("sections.tsv"):
        vocab.update(S.tokens(row["title"]))
    missing = sorted("%s -> %s" % (key, target)
                     for key, targets in S.load_synonyms().items()
                     for target in targets if target not in vocab)
    # Ishora-yozuv o'z sarlavhasi bilan so'ralganda ham taklif qilinmaydi.
    leaked = sorted("%s %s" % (row["doc"], row["section"])
                    for row in S.read_tsv("sections.tsv")
                    if row.get("ishora") and (row["doc"], row["section"]) in
                    {(h[0], h[1]) for h in S.suggest(row["title"])})
    return [("sinonim nishonlari sarlavhalarda bor", not missing,
             ", ".join(missing[:5]) or "hammasi bor"),
            ("ishora-yozuv taklif qilinmaydi", not leaked,
             ", ".join(leaked) or "hech biri")]


# Kod yopishtirilganda Java zaxira so'zlari olib boradigan bo'limlar:
# "`public` maydon", "`package-private`". Avval testdata/java dagi 7
# faylning 7 tasida 14.6, 5 tasida 26.2 chiqardi.
KEYWORD_NOISE = {("clean-code", "14.6"), ("clean-code", "26.2")}


def clean_cases():
    """clean_prompt, rule_keys va rank_key: (nom, ok, izoh) ro'yxati."""
    out = []
    text = S.clean_prompt("org.hibernate.LazyInitializationException va "
                          "com.example.order.items")
    out.append(("FQCN oddiy nomga, kichik harfli yo'l joyida",
                 "LazyInitializationException" in text and "org." not in text
                 and "com.example.order.items" in text, text))
    text = S.clean_prompt("bogʻliqlik yo’q")
    out.append(("ʻ va ’ ASCII apostrofga", text == "bog'liqlik yo'q", text))
    text = S.clean_prompt("@Transactional\npublic void save() {")
    out.append(("kod qatorida tuzilish so'zi tashlanadi",
                 "public" not in text and "void" not in text
                 and "save" in text and "@Transactional" in text, text))
    text = S.clean_prompt("record ishlatsam bo'ladimi, public API uchun")
    out.append(("oddiy gapda zaxira so'z qoladi",
                 "record" in text and "public" in text, text))

    noisy = []
    folder = os.path.join(HERE, "testdata", "java")
    for name in sorted(os.listdir(folder)):
        with open(os.path.join(folder, name), encoding="utf-8") as handle:
            code = handle.read()
        hits = {(h[0], h[1]) for h in S.suggest("shu kodni review qil:\n" + code)}
        if hits & KEYWORD_NOISE:
            noisy.append("%s: %s" % (name, sorted(hits & KEYWORD_NOISE)))
    hits = {(h[0], h[1]) for h in S.suggest("public enum OrderStatus { NEW }")}
    if hits & KEYWORD_NOISE:
        noisy.append("enum: %s" % sorted(hits & KEYWORD_NOISE))
    out.append(("kod parchasida `public`/`package` bo'limi yo'q", not noisy,
                ", ".join(noisy) or "hech birida"))

    cases = (("S1192 string literal takrorlanyapti", ["java:S1192"]),
             ("java:S2259 va squid:S1192", ["java:S1192", "java:S2259"]),
             ("S3 bucket, AS400, s1192", []))
    bad = ["%r -> %s" % (p, S.rule_keys(p)) for p, want in cases
           if S.rule_keys(p) != want]
    out.append(("prefikssiz Sonar kaliti", not bad, "; ".join(bad) or "uchala holat"))

    table = S.exception_rows()
    leaked = [name for name in ("runtimeexception", "illegalstateexception",
                                "sqlexception", "ordernotfoundexception",
                                "insufficientfundsexception")
              if name in table]
    kept = all(name in table for name in ("nouniquebeandefinitionexception",
                                          "lazyinitializationexception"))
    out.append(("exceptions.tsv: umumiy va misol nomlarsiz",
                not leaked and kept, ", ".join(leaked) or "toza"))

    # Bo'lim qatori yo'q kalit: bob qatori (katalog jadvali) qaytadi.
    fake = [{"rule": "java:S9", "doc": "sonarqube", "chapter": "27",
             "section": "", "marta": "1", "ulush": "0.1", "qoida": "0"}]
    real = S.read_tsv
    S.read_tsv = lambda name: fake if name == "rules.tsv" else real(name)
    try:
        hits = S.rule_hits(["java:S9"], {("sonarqube", "27"): "27. Katalog"})
    finally:
        S.read_tsv = real
    out.append(("bo'limsiz kalit: bob qatori", [h[:2] for h in hits]
                == [("sonarqube", "27")], str(hits)))

    items = [(("architect", "2.10"), [5.0, 3.0, 2]),
             (("testing", "2.9"), [5.0, 3.0, 2]),
             (("patterns", "1.1"), [5.0, 4.0, 2]),
             (("clean-code", "9.9"), [6.0, 3.0, 2])]
    order = ["%s %s" % key for key, _ in sorted(items, key=S.rank_key)]
    want = ["clean-code 9.9", "patterns 1.1", "testing 2.9", "architect 2.10"]
    out.append(("teng ball: max-idf, keyin raqam son sifatida", order == want,
                ", ".join(order)))
    return out


def main():
    # Indeks hosila va git ga kirmaydi, ya'ni toza checkout da yo'q.
    # Avval bu yerda "yo'q, qo'lda yasang" deb yiqilardi: lokalda indeks
    # allaqachon turgani uchun sezilmay qolgan, CI da esa birinchi
    # yurgizishda qizil berardi. Endi o'zi yasaydi, eval_find kabi.
    # build_index.py to'g'ridan: doc.sh orqali bash siz muhitda yiqilardi.
    if not os.path.exists(os.path.join(S.INDEX, "df.tsv")):
        print("indeks yo'q, yasalmoqda: tools/build_index.py")
        subprocess.run([sys.executable, os.path.join(HERE, "build_index.py")],
                       capture_output=True, check=True)

    failures = 0
    total = 0

    print("== Taklif berishi kerak ==")
    for prompt, want_doc, *rest in EXPECTED:
        secs = rest[0] if rest else None
        hits = S.suggest(prompt)
        ok = any(h[0] == want_doc and (not secs or h[1] in secs) for h in hits)
        failures += not ok
        total += 1
        print("%-4s %-58s -> %s" % (
            "OK" if ok else "XATO", prompt[:58],
            ", ".join("%s %s" % (h[0], h[1]) for h in hits) if hits else "(jim)"))

    print("\n== Jim turishi kerak ==")
    for prompt in SILENT:
        hits = S.suggest(prompt)
        ok = not hits
        failures += not ok
        total += 1
        print("%-4s %-58s -> %s" % (
            "OK" if ok else "XATO", prompt.replace("\n", " | ")[:58],
            "(jim)" if ok else "%d ta taklif: %s" % (
                len(hits), hits[0][2][:40])))

    print("\n== Chegarada: so'rov bo'yicha chegara ==")
    ok = S.MAX_SUGGESTIONS <= 4
    failures += not ok
    total += 1
    print("%-4s %-58s -> %d" % ("OK" if ok else "XATO",
                                "MAX_SUGGESTIONS <= 4", S.MAX_SUGGESTIONS))
    for prompt, limit, docs, must in BORDERLINE:
        hits = S.suggest(prompt)
        got = {h[0] for h in hits}
        ok = (len(hits) <= limit and got <= docs
              and (must is None or any((h[0], h[1]) == must for h in hits)))
        failures += not ok
        total += 1
        print("%-4s %-58s -> %d ta (chegara %d) %s" % (
            "OK" if ok else "XATO", prompt[:58], len(hits), limit,
            ", ".join("%s %s" % (h[0], h[1]) for h in hits)))

    print("\n== Sinonimlar: musbat va manfiy ==")
    for key, prompt, want, banned in SYNONYM_CASES:
        keys = [(h[0], h[1]) for h in S.suggest(prompt)]
        if banned == "jim":
            ok = not keys
        else:
            ok = ((want is None or bool(want & set(keys)))
                  and not banned & set(keys))
        failures += not ok
        total += 1
        print("%-4s %-16s %-41s -> %s" % (
            "OK" if ok else "XATO", key, prompt[:41],
            ", ".join("%s %s" % k for k in keys) or "(jim)"))
    idf = S.load_idf(len(S.read_tsv("sections.tsv")))
    synonyms = S.load_synonyms()
    for prompt, want, banned in EXPAND_CASES:
        words = S.expand(prompt, idf, synonyms)
        ok = (want is None or want in words) and (banned is None or banned not in words)
        failures += not ok
        total += 1
        print("%-4s %-58s -> %s" % ("OK" if ok else "XATO", "kengaytma: " + prompt,
                                    "+%s" % want if want else "-%s" % banned))

    print("\n== Ishora-yozuv o'rniga to'liq yozuv ==")
    for prompt, doc, want, pointer in POINTERS:
        keys = {(h[0], h[1]) for h in S.suggest(prompt)}
        ok = (doc, want) in keys and (doc, pointer) not in keys
        failures += not ok
        total += 1
        print("%-4s %-58s -> %s" % (
            "OK" if ok else "XATO", prompt[:58],
            ", ".join("%s %s" % k for k in sorted(keys)) or "(jim)"))

    print("\n== Kirishni tozalash va tartib ==")
    for name, ok, note in clean_cases():
        failures += not ok
        total += 1
        print("%-4s %-58s -> %s" % ("OK" if ok else "XATO", name,
                                     str(note).replace("\n", " | ")[:60]))

    print("\n== Invariantlar ==")
    for name, ok, note in invariant_cases():
        failures += not ok
        total += 1
        print("%-4s %-58s -> %s" % ("OK" if ok else "XATO", name, note))

    print("\n== Hookning o'zi ==")
    for name, ok, note in hook_cases():
        failures += not ok
        total += 1
        print("%-4s %-58s -> %s" % ("OK" if ok else "XATO", name, note))

    print("\n== Holat fayllari: format.json va xato izi ==")
    for name, ok, note in state_cases():
        failures += not ok
        total += 1
        print("%-4s %-58s -> %s" % ("OK" if ok else "XATO", name, str(note)[:60]))

    print("\n== Ma'lum bo'shliqlar (xato hisoblanmaydi) ==")
    for prompt, want, why in KNOWN_GAPS:
        hits = S.suggest(prompt)
        print("     %-58s -> %s (kutilgan %s: %s)" % (
            prompt[:58],
            ", ".join("%s %s" % (h[0], h[1]) for h in hits) or "(jim)", want, why))

    print("\n%d/%d o'tdi" % (total - failures, total))
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
