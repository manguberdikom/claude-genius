# Review: diff yo'q bo'lsa

`review` aktyori (`.claude/agents/review.md`) diff bo'sh yoki doira
modul, proyekt bo'lsa shu tartibda ishlaydi: arzondan qimmatga, har
qadam oldingisi topolmaganini qidiradi. Punkt shubha uyg'otsa
`tools/doc.sh outline <hujjat> <bob>`, keyin faqat o'sha bo'lim `show`.
Punkt kod holatiga aylanmasa (fayl yaratish, CI,
jamoa amaliyoti), u topilma emas: `Taklif:` ga bir qator.

1. **Mexanik tekshiruv**, bir marta, review asosi:
   `python3 tools/schema_from_entities.py <src> --only-findings`,
   `find <src> \( -path '*/target' -o -path '*/build' \) -prune -o -name '*.java' -print0 | xargs -0 python3 tools/check_code.py`,
   `python3 tools/metod_bormi.py <src/main/java> --audit`: tashqi yozuvchi
   `o'rta`, ochiq setter `past` (clean-code 16.6, 33.18, 36.12).
   `check_code: N fayl, M buzilish` qatorlaridagi N lar `Ko'rildi` ga
   qo'shiladi; xargs 123 topilma bor degani.
1b. **O'qish tartibi** (architect 34.2): kirish nuqtalari
   `grep -rln --include=*.java -E '@(RestController|Controller|KafkaListener|RabbitListener|JmsListener|Scheduled)' <src>`,
   churn `git log --since='1 year ago' --name-only --pretty=format: | grep '\.java$' | sort | uniq -c | sort -rn | head -20`.
   To'liq o'qiladi: kirish nuqtalari, churn boshidagi fayllar va
   `--audit` dagi uzun metodlar; qolgani punkt grep bilan, o'qilmagani
   `Ko'rilmagan` ga.
2. **Mavjud signal.** Yangi tahlil yurgizilmaydi, bor chiqish o'qiladi.
   Yiqilgan test (Maven, Gradle yoki CI logi):
   `python3 tools/parse_test_output.py <fayl>`; u Sonar ni ko'rmaydi.
   Sonar sozlangan bo'lsa `python3 tools/sonar_fetch.py gate` va `issues`
   (rc 2 bo'lsa `Ko'rilmagan: Sonar sozlanmagan`); hisobot fayli bo'lsa
   `grep -oE '[a-z]+:S[0-9]+' <hisobot> | sort | uniq -c`. Kalit:
   `tools/doc.sh rule java:Sxxxx`, boshqasida `tools/doc.sh find -f Sxxxx`.
3. **Modul mezoni**: har modul uchun alohida, test va build faylisiz
   (test 6-qadamda, build fayliga `tools/doc.sh checklist code-review 33`):
   `python3 tools/rules_for.py --no-mark --mashinasiz $(find <modul> \( -path '*/target' -o -path '*/build' -o -path '*/src/test' \) -prune -o -type f \( -name '*.java' -o -name '*.sql' -o -name 'application*.y*ml' -o -name 'application*.properties' \) -print)`.
   Papka berilmaydi.
   `(sig'madi: ...)` va `(boshqa kartalar: ...)` ham mezon: har bob
   `tools/doc.sh checklist <hujjat> <bob>`, har karta
   `sed -n '/^Tuzoqlar/,$p' <karta>`; yetilmagani `Ko'rilmagan` ga.
4. **Tuzilish**: modul va qatlam chegaralari, bog'liqlik yo'nalishi.
   `tools/doc.sh checklist code-review 6 7`, topilma chiqqan mavzuda
   faqat o'sha bo'lim.
5. **Xato katalogi**: mexanik tekshiruv tutmaydigan tipik xatolar.
   `tools/doc.sh checklist code-review 12 15 16 38` (proxy, holat,
   resurs, performance), `tools/doc.sh checklist sonarqube 25 26 27 28 29 30`
   (bug, security, tuzilish, nomlash, Spring, JPA, test kodi) va
   `tools/doc.sh checklist patterns 25` (anti-pattern).
6. **Qoplanish**: test turi mos keladimi, nima qoplanmagan (Sonar bo'lsa
   `sonar_fetch.py coverage`). `tools/doc.sh show testing 2.5`,
   `tools/doc.sh checklist testing 2`.
