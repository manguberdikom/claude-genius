# To'liq review

"Proyektni review qil" degan vazifa. Maqsad: qoidalarga zid joylarni
topish, har birini bo'lim raqami bilan asoslash va egasiga yo'naltirish.

Kod **o'zgartirilmaydi**. Review topilma beradi, tuzatishni `arxitektor`
va `test-muhandis` qiladi.

## Tartib: arzondan qimmatga

Har qadam o'zidan oldingisi topolmagan narsani qidiradi. Birinchi uch
qadam mashina bajaradi va deyarli bepul.

**1. Mexanik tekshiruv.** Bir marta yurgiziladi, natijasi butun review
uchun asos bo'ladi.

```bash
python3 tools/schema_from_entities.py <src> --only-findings
find <src> -name '*.java' -print0 | xargs -0 -n1 python3 tools/check_code.py
```

**2. Mavjud signal.** Sonar hisoboti, CI chiqishi yoki yiqilgan test
bo'lsa, u o'qiladi: `tools/parse_test_output.py`. Har Sonar kaliti
`tools/doc.sh rule java:Sxxxx` bilan qoidaga ulanadi. Yangi tahlil
yurgizilmaydi, konteyner ko'tarilmaydi.

**3. Tuzilish.** Modul va qatlam chegaralari, bog'liqlik yo'nalishi,
paket tuzilishi. `tools/doc.sh show code-review 6` va `7`.

**4. Diff emas, kod.** To'liq review da diff yo'q, shuning uchun
yo'nalish kerak. Qaysi joyga qarash: `tools/doc.sh checklist code-review`
va `tools/doc.sh checklist clean-code`. Ro'yxat yozilgan, o'ylab
topilmaydi.

**5. Qoplanish.** Test turi mos keladimi, nima qoplanmagan:
`tools/doc.sh show testing 2` va `doc.sh checklist testing`.

## Topilma shakli

```
[daraja] <fayl>:<qator>
    <nima noto'g'ri>
    qoida: <hujjat> <raqam> <sarlavha>
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
