# To'liq review

"Proyektni review qil" degan vazifa. Maqsad: qoidalarga zid joylarni
topish, har birini bo'lim raqami bilan asoslash va egasiga yo'naltirish.

Kod **o'zgartirilmaydi**. Review topilma beradi, tuzatishni `arxitektor`
va `test-muhandis` qiladi.

## Tartib: arzondan qimmatga

Har qadam o'zidan oldingisi topolmagan narsani qidiradi. Birinchi ikki
qadam mashina bajaradi va deyarli bepul. Qolganlari tekshiruv punktini
o'qiydi, bob butunligicha o'qilmaydi: punkt shubha uyg'otsa
`tools/doc.sh outline <hujjat> <bob>`, keyin faqat o'sha bo'lim `show`
qilinadi.

**1. Mexanik tekshiruv** (`tahlil`). Bir marta yurgiziladi, natijasi
butun review uchun asos bo'ladi.

```bash
python3 tools/schema_from_entities.py <src> --only-findings
find <src> -name '*.java' -print0 | xargs -0 -n1 python3 tools/check_code.py | grep -v ': qoida buzilishi topilmadi\.$'
find <src> -name '*.java' | wc -l
```

Toza fayl qatori chiqarilmaydi: yuzlab faylda chiqish kesiladi va
topilma o'rtada yo'qoladi. Oxirgi qator hisobotdagi `Ko'rildi` uchun
fayl sonini beradi. xargs 123 qaytarsa, bu topilma borligini bildiradi,
xato emas.

**2. Mavjud signal** (`tahlil`). Yangi tahlil yurgizilmaydi, konteyner
ko'tarilmaydi, bor chiqish o'qiladi.

- Yiqilgan test (Maven yoki Gradle chiqishi):
  `python3 tools/parse_test_output.py <chiqish-fayli>`.
- CI logi: qator boshidagi vaqt prefiksi avval olib tashlanadi, aks
  holda asbob yiqilishni ko'rmaydi:
  `python3 tools/parse_test_output.py <(sed -E 's/^.*[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9:.]+Z ?//' <log>)`.
- Sonar hisoboti: bu asbob uni o'qimaydi. Kalitlar ajratiladi
  (`grep -oE '[a-z]+:S[0-9]+' <hisobot> | sort | uniq -c`) va har biri
  `tools/doc.sh rule java:Sxxxx` bilan bo'limga ulanadi, boshqa prefiksli
  kalit uchun `tools/doc.sh find -f Sxxxx`.

`Yiqilgan test topilmadi.` signal yo'q degani emas: kompilyatsiya
xatosini va Sonar topilmasini asbob ko'rmaydi.

**3. Modul mezoni.** Diff yo'q, shuning uchun `rules_for.py --diff` hech
narsa bermaydi. O'rniga har modul uchun
`python3 tools/rules_for.py $(find <modul> -name '*.java')`: papka
berilmaydi, asbob faqat fayl qabul qiladi. U oltita qo'llanmadan
tegishli boblarni, tekshiruv punktlarini va avvalgi xatolarni beradi.
Uning "Mashina topgani" qismi 1-qadamni takrorlaydi, qayta yozilmaydi.
Chiqqan boblar uchun to'liq ro'yxat: `tools/doc.sh checklist <hujjat> <bob>`.

**4. Tuzilish.** Modul va qatlam chegaralari, bog'liqlik yo'nalishi,
paket tuzilishi: `tools/doc.sh checklist code-review 6` va `7`. Topilma
chiqqan mavzu uchun faqat o'sha bo'lim o'qiladi, masalan
`tools/doc.sh show code-review 6.2`.

**5. Xato katalogi.** Mexanik tekshiruv tutmaydigan tipik xatolar:
`tools/doc.sh checklist sonarqube 25` dan `29` gacha (bug, security,
tuzilish, nomlash, Spring, JPA va PostgreSQL) va anti-patternlar uchun
`tools/doc.sh checklist patterns 25`. Butun hujjat checklisti (bob
raqamisiz) chaqirilmaydi: u chiqish chegarasidan katta va kesiladi.

**6. Qoplanish.** Test turi mos keladimi, nima qoplanmagan:
`tools/doc.sh show testing 2.5` va `tools/doc.sh checklist testing 2`,
test kodidagi xatolar uchun `tools/doc.sh checklist sonarqube 30`.

## Topilma shakli

```
[daraja] <fayl>:<qator>
    <nima noto'g'ri>
    qoida: <hujjat> <raqam> <sarlavha>
    tuzatish: <aniq taklif>
    egasi: arxitektor | test-muhandis | rejalashtiruvchi
```

Daraja: `yuqori` xato yoki xavf, `o'rta` qarz yig'adi, `past` uslub.

## Hisobot

```
Ko'rildi: <N> fayl, <M> entity, <K> test
Topildi : <yuqori> yuqori, <o'rta> o'rta, <past> past

<topilmalar, darajasi bo'yicha>

Toza: <qaysi sohalarda kamchilik topilmadi>
Ko'rilmagan: <nimaga yetilmadi va nega>
```

Oxirgi ikki qator majburiy. "Toza" ro'yxatisiz hisobot faqat yomon
xabar beradi; "ko'rilmagan" ro'yxatisiz esa u to'liq ko'rinadi,
holbuki emas.

## Nimani topilma deb yozmaslik kerak

- Did masalasi: qoida raqami yo'q bo'lsa, bu topilma emas, taklif.
  Alohida ro'yxatga yoziladi.
- Mavjud va ishlayotgan yechimni boshqasiga almashtirish taklifi, agar
  qoida buni talab qilmasa.
- Takrorlangan topilma: bir xil sabab o'n faylda bo'lsa, bir marta
  yoziladi va fayllar sanaladi.
- Topilma soni ish sifatining o'lchovi emas. Toza kodda kam topilma
  bo'ladi va bu to'g'ri natija.
