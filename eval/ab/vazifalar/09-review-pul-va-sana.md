# 9-vazifa: review, tashrif narxi va sana

**Tur:** review (kod o'zgartirilmaydi). **Tartib:** A birinchi, B ikkinchi.

## Tayyorlash (sessiya boshlanishidan OLDIN)

```bash
git checkout 500158f732419217507c7656904b8e6aa1bcc0d6 -- src
git apply eval/ab/vazifalar/diff/review-2.diff
```

## Prompt (ikkala holatda aynan bir xil)

```text
Bu diffni review qil. Nimani to'xtatasan va nega. Kodni o'zgartirmang,
faqat topilmalarni yoz.
```

## Qabul mezoni

`muvaffaqiyat` = 1, agar **to'rtta kiritilgan nuqsondan kamida uchtasi**
topilgan bo'lsa.

## Kiritilgan nuqsonlar (baholovchi uchun, 4 ta)

| # | Nuqson | Nega muhim |
|---|---|---|
| R2-1 | Pul `double` bilan hisoblanadi (`totalWithVat`) | ikkilik kasr pulni aniq saqlamaydi: yaxlitlash xatosi yig'iladi. `BigDecimal` va ochiq `RoundingMode` kerak |
| R2-2 | `new java.math.BigDecimal(double)` | konstruktor ikkilik taqribiy qiymatni oladi: `0.12` aslida `0.1200000000000000011...`. `BigDecimal.valueOf` yoki satrli konstruktor kerak |
| R2-3 | `static SimpleDateFormat` | `SimpleDateFormat` thread-safe emas, static maydonda esa u bo'lishiladi: parallel so'rovda noto'g'ri sana. `DateTimeFormatter` kerak |
| R2-4 | `@Transactional` `private` metodda | proxy private metodni o'ramaydi: annotatsiya jim e'tiborsiz qoladi, tranzaksiya yo'q |

Diqqat, R2-2 ni R2-1 dan alohida sanash: ikkisi ham pulga tegishli,
lekin sabablari boshqa. Topilma faqat "BigDecimal ishlat" desa, u R2-1
hisoblanadi; `new BigDecimal(double)` ning o'zi muammo ekanini aytsa,
R2-2 ham hisoblanadi.

Yolg'on topilma deb sanaladi: `setScale(2)` ning `RoundingMode` siz
`ArithmeticException` berishi haqidagi gap **yolg'on emas**, u
haqiqiy qo'shimcha topilma va izohga yoziladi.
