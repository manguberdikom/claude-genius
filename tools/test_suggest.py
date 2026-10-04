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

Ma'lum cheklov: moslik so'z darajasida ishlaydi, sinonimni bilmaydi.
"metod juda uzun, qanday bo'laklayman" so'rovi "Funksiya: kichiklik va
bitta ish" bobiga ulanmaydi, chunki umumiy so'z yo'q. Bo'lim tanasining
kalit so'zlarini indekslash sinab ko'rildi va bu holatni yechmadi, shuning
uchun u olib tashlandi: indeks 304 KB ga, build esa uch barobarga oshar,
natija esa o'zgarmas edi. Bunday so'rov uchun `doc.sh find -f` bor.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import suggest_sections as S  # noqa: E402

# So'rov -> kutilgan hujjat. Taklif ro'yxatida o'sha hujjatdan kamida
# bitta bo'lim bo'lishi kerak.
EXPECTED = [
    ("tashqi servisga chaqiruvni ishonchli qilish kerak, timeout va qayta urinish",
     "patterns"),
    ("circuit breaker qo'yaymi yoki bulkhead", "patterns"),
    ("Testcontainers bilan PostgreSQL test yozmoqchiman", "testing"),
    ("test flaky bo'lib qoldi, nima qilaman", "testing"),
    ("Sonar cognitive complexity dan shikoyat qilyapti", "sonarqube"),
    ("quality gate o'tmayapti, coverage past", "sonarqube"),
    ("deadlock chiqdi, izolyatsiya darajasini qanday tanlayman", "architect"),
    ("connection pool kattaligini qanday hisoblayman", "architect"),
    ("bu funksiya nomi to'g'rimi", "clean-code"),
    ("saga pattern kerakmi yoki outbox", "patterns"),
    ("N+1 so'rov muammosi", "patterns"),
]

# Mavzusiz so'rovlar: hook butunlay jim turishi shart.
SILENT = [
    "salom",
    "rahmat, yaxshi ishladi",
    "commit qil va push qil",
    "nima qila olasan",
    "yana bir marta ko'rib chiq",
    "bu qatorni o'chir",
    "yuqoridagini tushuntirib ber",
    # Asboblarning o'zi haqidagi meta-savollar. Bular amalda uchradi va
    # eng yomon turdagi shovqinni berdi: "tezlik", "aniqlik", "sifat"
    # kabi mavhum otlar bu korpusda kamyob (aniqlik IDF 5.1, deadlock
    # 4.4), shuning uchun chastota ularni atama deb o'ylaydi.
    "kerakli qoidani ozi topa oladimi tezlik bilan",
    "bu qoida qanday ishlaydi",
    "sifat yaxshimi yoki yo'q",
    "qidiruv qanchalik aniq ishlayapti",
]

# Chegaradagi so'rovlar: buyruq shaklida, lekin ichida haqiqiy mavzu so'zi
# bor ("test", "git", "nom"). Bu yerda jimlikni talab qilish noto'g'ri
# bo'lardi: "testni ishga tushir" uchun "Testni tanlab ishga tushirish"
# bo'limi aynan mos keladi. Talab - natija chegaralangan bo'lsin, shunda
# noto'g'ri taklifning narxi bir necha qatordan oshmaydi.
BORDERLINE = [
    "git push qilib qoy",
    "fayl nomini o'zgartir",
    "testni ishga tushir",
    # "performance" bu korpusda haqiqiy atama: "Performance regressiyasini
    # diffdan ko'rish" degan bob bor. So'rov asbob tezligi haqida bo'lsa
    # ham, so'z darajasidagi moslik buni ajrata olmaydi. Qoidani shu
    # holat uchun burish haqiqiy atamalarni yo'qotardi, shuning uchun
    # taklif chiqishi qabul qilinadi, faqat soni chegaralanadi.
    "performance, tezlik, aniqlik haqida nima deysan",
]


def main():
    if not os.path.exists(os.path.join(S.INDEX, "df.tsv")):
        print("index/df.tsv yo'q, avval: tools/doc.sh rebuild")
        return 1

    failures = 0

    print("== Taklif berishi kerak ==")
    for prompt, want_doc in EXPECTED:
        hits = S.suggest(prompt)
        docs = {h[0] for h in hits}
        ok = want_doc in docs
        failures += not ok
        print("%-4s %-58s -> %s" % (
            "OK" if ok else "XATO", prompt[:58],
            ", ".join(sorted(docs)) if docs else "(jim)"))

    print("\n== Jim turishi kerak ==")
    for prompt in SILENT:
        hits = S.suggest(prompt)
        ok = not hits
        failures += not ok
        print("%-4s %-58s -> %s" % (
            "OK" if ok else "XATO", prompt[:58],
            "(jim)" if ok else "%d ta taklif: %s" % (
                len(hits), hits[0][2][:40])))

    print("\n== Chegarada: ko'pi bilan %d ta ==" % S.MAX_SUGGESTIONS)
    for prompt in BORDERLINE:
        hits = S.suggest(prompt)
        ok = len(hits) <= S.MAX_SUGGESTIONS
        failures += not ok
        print("%-4s %-58s -> %d ta" % (
            "OK" if ok else "XATO", prompt[:58], len(hits)))

    total = len(EXPECTED) + len(SILENT) + len(BORDERLINE)
    print("\n%d/%d o'tdi" % (total - failures, total))
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
