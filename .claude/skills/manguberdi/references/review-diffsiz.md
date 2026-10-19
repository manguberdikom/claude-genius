# Review: diff yo'q bo'lsa

`review` aktyori diff bo'sh bo'lganda yoki doira modul yoki butun
proyekt bo'lganda shu tartibni o'qiydi (`.claude/agents/review.md`).

"Proyektni review qil" kabi vazifada diff bo'lmaydi va
`rules_for.py --diff` 2 qaytaradi. Tartib arzondan qimmatga: har qadam
o'zidan oldingisi topolmaganini qidiradi. Birinchi ikkitasi mashina ishi
va deyarli bepul. Qolganlari tekshiruv punktini o'qiydi, bob butunligicha
o'qilmaydi: punkt shubha uyg'otsa `tools/doc.sh outline <hujjat> <bob>`,
keyin faqat o'sha bo'lim `show` bilan.

1. **Mexanik tekshiruv**, bir marta, butun review uchun asos:
   `python3 tools/schema_from_entities.py <src> --only-findings` va
   `find <src> -name '*.java' -print0 | xargs -0 python3 tools/check_code.py`.
   Toza fayl qatori chiqarilmaydi, shuning uchun yuzlab faylda ham
   topilma kesilib qolmaydi: faqat buzilishi bor fayl, oxirida
   `check_code: N fayl, M buzilish`. N `Ko'rildi` uchun fayl soni; juda
   ko'p faylda xargs bir necha chaqiruvga bo'ladi, har biri o'z yig'ma
   qatorini beradi va N lar qo'shiladi. xargs 123 qaytarsa, bu topilma
   borligini bildiradi, xato emas.
2. **Mavjud signal.** Yangi tahlil yurgizilmaydi, konteyner
   ko'tarilmaydi, bor chiqish o'qiladi. Yiqilgan test (Maven yoki Gradle
   chiqishi): `python3 tools/parse_test_output.py <fayl>`. CI logi ham
   to'g'ridan beriladi: qator boshidagi vaqt prefiksini asbob o'zi
   olib tashlaydi.
   Sonar hisobotini bu asbob o'qimaydi: kalitlar
   `grep -oE '[a-z]+:S[0-9]+' <hisobot> | sort | uniq -c` bilan olinadi,
   keyin `tools/doc.sh rule java:Sxxxx`, boshqa prefiksda
   `tools/doc.sh find -f Sxxxx`. `Yiqilgan test topilmadi.` signal yo'q
   degani emas: Sonar topilmasini u ko'rmaydi.
3. **Modul mezoni**: har modul uchun alohida
   `python3 tools/rules_for.py --no-mark $(find <modul> -type f \( -name '*.java' -o -name '*.sql' -o -name 'application*.y*ml' -o -name 'application*.properties' -o -name 'pom.xml' -o -name 'build.gradle*' \))`.
   Papka berilmaydi, asbob faqat fayl qabul qiladi. Migratsiya, sozlama
   va build fayli ham beriladi: ularning boblari `.java` dan ko'rinmaydi. Bitta chaqiruv 8 bob
   va 3 doimiy bob, ularning tekshiruv punktlari va avvalgi xatolarni
   beradi. Uning "Mashina topgani" qismi 1-qadamni takrorlaydi, qayta
   yozilmaydi. Chiqqan bob uchun to'liq ro'yxat:
   `tools/doc.sh checklist <hujjat> <bob>`.
4. **Tuzilish**: modul va qatlam chegaralari, bog'liqlik yo'nalishi,
   paket tuzilishi. `tools/doc.sh checklist code-review 6` va `7`, topilma
   chiqqan mavzu uchun faqat o'sha bo'lim, masalan
   `tools/doc.sh show code-review 6.2`.
5. **Xato katalogi**: mexanik tekshiruv tutmaydigan tipik xatolar.
   `tools/doc.sh checklist sonarqube 25` dan `29` gacha (bug, security,
   tuzilish, nomlash, Spring, JPA va PostgreSQL) va anti-patternlar uchun
   `tools/doc.sh checklist patterns 25`. Bob raqamisiz
   `tools/doc.sh checklist <hujjat>` faqat bob bo'yicha punkt sonini beradi.
   To'liq ro'yxat (`--all`) chegaradan katta, u chaqirilmaydi.
6. **Qoplanish**: test turi mos keladimi, nima qoplanmagan.
   `tools/doc.sh show testing 2.5` va `tools/doc.sh checklist testing 2`,
   test kodidagi xatolar uchun `tools/doc.sh checklist sonarqube 30`.
