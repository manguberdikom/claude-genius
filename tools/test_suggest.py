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
build uch barobarga oshar edi.
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
import suggest_sections as S  # noqa: E402

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
    # taklif chiqishi qabul qilinadi, faqat soni chegaralanadi.
    ("performance, tezlik, aniqlik haqida nima deysan", 4,
     {"code-review", "patterns"}, None),
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

    print("\n== Ishora-yozuv o'rniga to'liq yozuv ==")
    for prompt, doc, want, pointer in POINTERS:
        keys = {(h[0], h[1]) for h in S.suggest(prompt)}
        ok = (doc, want) in keys and (doc, pointer) not in keys
        failures += not ok
        total += 1
        print("%-4s %-58s -> %s" % (
            "OK" if ok else "XATO", prompt[:58],
            ", ".join("%s %s" % k for k in sorted(keys)) or "(jim)"))

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
