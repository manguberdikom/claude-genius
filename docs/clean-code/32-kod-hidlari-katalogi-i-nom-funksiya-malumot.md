<!-- doc: clean-code | chapter: 32 | part: X. Hid katalogi va refaktoring harakatlari -->

[Toza kod yozuvchining qoidalari](../../README.md) / [Toza kod qoidalari](README.md)

# 32. Kod hidlari katalogi I: nom, funksiya, ma'lumot (Code Smells I)

<details>
<summary>Bu bobdagi 15 bo'lim</summary>

- [32.1 Sirli nom (Mysterious Name)](#321-sirli-nom-mysterious-name)
- [32.2 Takrorlangan kod (Duplicated Code)](#322-takrorlangan-kod-duplicated-code)
- [32.3 Uzun funksiya (Long Function)](#323-uzun-funksiya-long-function)
- [32.4 Global ma'lumot (Global Data)](#324-global-malumot-global-data)
- [32.5 O'zgaradigan ma'lumot (Mutable Data)](#325-ozgaradigan-malumot-mutable-data)
- [32.6 Ma'lumot to'dasi (Data Clumps)](#326-malumot-todasi-data-clumps)
- [32.7 Takrorlangan `switch` (Repeated Switches)](#327-takrorlangan-switch-repeated-switches)
- [32.8 Sikllar (Loops)](#328-sikllar-loops)
- [32.9 Dangasa element (Lazy Element)](#329-dangasa-element-lazy-element)
- [32.10 Vaqtinchalik maydon (Temporary Field)](#3210-vaqtinchalik-maydon-temporary-field)
- [32.11 Uzun xabar zanjiri (Message Chains)](#3211-uzun-xabar-zanjiri-message-chains)
- [32.12 Vositachi (Middle Man)](#3212-vositachi-middle-man)
- [32.13 Izohlar hid sifatida (Comments)](#3213-izohlar-hid-sifatida-comments)
- [32.14 Bu hid emas: qachon tegmaslik kerak](#3214-bu-hid-emas-qachon-tegmaslik-kerak)
- [32.15 Amalda qo'llash](#3215-amalda-qollash)

</details>


Kod hidi - xato emas, lekin muammo ehtimolini oshiradigan tuzilish. Patternlar hujjatida 83 ta anti-pattern sanalgan ([25-bob](25-java-kodidagi-umumiy-tuzoqlar.md)); bu va keyingi bob ularni **takrorlamaydi** va qolgan hidlarni beradi. Har bir hid uchun uch qism: belgisi, nega muammo, va qaysi refaktoring harakati bilan tuzatiladi (35-37 boblar).

## 32.1 Sirli nom (Mysterious Name)

**Belgisi**: nomni o'qib nima qilayotganini aytib bo'lmaydi; `proc`, `handle`, `data2`, `tmpFlag`.

**Nega muammo**: nom eng arzon hujjat va u ishlamasa, har bir o'quvchi kodni qaytadan o'qib chiqadi. Bu eng ko'p uchraydigan va eng arzon tuzatiladigan hid.

**Tuzatish**: Rename Variable / Rename Field / Change Function Declaration ([35-bob](35-refaktoring-harakatlari-katalogi-i-funksiya.md)). Agar nom o'ylab chiqmasa, bu sinfning javobgarligi noaniq ekanini bildiradi - Extract Class kerak bo'lishi mumkin.

## 32.2 Takrorlangan kod (Duplicated Code)

DRY printsipi [patternlar hujjatidagi](../patterns/README.md) DRY printsipida. Bu yerda amaliy qism: takrorlanishning **uch turi** bor va ularning har biri boshqa yechim talab qiladi.

| Tur | Ko'rinishi | Yechim |
|---|---|---|
| Aynan takrorlanish | bir xil qatorlar bir sinfda | Extract Function |
| Qardosh takrorlanish | bir xil kod ikki voris sinfda | Pull Up Method |
| Shaklli takrorlanish | tuzilish bir xil, qiymatlar boshqa | Parameterize Function |
| Soxta takrorlanish | o'xshash ko'rinadi, lekin boshqa sabab bilan o'zgaradi | **tegmaslik** |

Oxirgi qator eng muhim: tasodifan o'xshash kodni birlashtirish noto'g'ri abstraksiya yaratadi va u takrorlanishdan qimmat ([arxitektor hujjatidagi](../architect/README.md) erta abstraksiya va noto'g'ri abstraksiya narxi bo'limlari).

## 32.3 Uzun funksiya (Long Function)

Metod uzunligi [arxitektor hujjatidagi](../architect/README.md) metod uzunligi va erta qaytish bo'limida va [4-bobda](04-funksiya-kichiklik-va-bitta-ish.md) ko'rilgan. Hid sifatida uning belgisi aniq: funksiyani tushunish uchun uni bo'laklarga ajratib o'qish kerak.

**Tuzatish tartibi**: Extract Function (eng ko'p), Replace Temp with Query, Introduce Parameter Object, Decompose Conditional, Split Loop, Replace Conditional with Polymorphism.

## 32.4 Global ma'lumot (Global Data)

**Belgisi**: `public static` o'zgaradigan maydon, singleton ichidagi o'zgaradigan holat, `System.getProperties()` ni kod bo'ylab o'zgartirish.

**Nega muammo**: o'zgarishning manbasini topib bo'lmaydi - har qanday kod istalgan vaqtda o'zgartirgan bo'lishi mumkin. Debug qilish uchun butun kod bazasini ko'rish kerak.

**Tuzatish**: Encapsulate Variable ([36-bob](36-refaktoring-harakatlari-katalogi-ii-malumot.md)) - global ma'lumotni funksiya ortiga yashirish, keyin bog'liqlik sifatida uzatish (16.9).

## 32.5 O'zgaradigan ma'lumot (Mutable Data)

**Belgisi**: obyektning maydoni kod bo'ylab turli joylarda o'zgaradi; setter lar ko'p; bir maydonni kim o'zgartirganini kuzatish qiyin.

**Nega muammo**: o'zgarishning sabab-natija zanjiri yo'qoladi. Bu ayniqsa ko'p threadli kodda xavfli.

**Tuzatish**: Encapsulate Variable, Split Variable, Remove Setting Method, Replace Derived Variable with Query, Change Reference to Value ([16-bob](16-ozgarmaslik-va-holat-boshqaruvi-kod.md) va [36-bob](36-refaktoring-harakatlari-katalogi-ii-malumot.md)).

## 32.6 Ma'lumot to'dasi (Data Clumps)

**Belgisi**: bir xil uch-to'rt maydon bir necha sinfda va metod imzolarida birga paydo bo'ladi: `from`, `to`; `street`, `city`, `zip`; `amount`, `currency`.

**Nega muammo**: tushuncha nomsiz qolgan. Har bir yangi ishlatilish takrorlanish qo'shadi va validatsiya tarqaladi.

**Tuzatish**: Introduce Parameter Object yoki Extract Class (5.6, [36-bob](36-refaktoring-harakatlari-katalogi-ii-malumot.md)). Sinov: maydonlardan birini olib tashlasa, qolganlari ma'nosini yo'qotadimi? Ha bo'lsa - bu bitta tushuncha.

## 32.7 Takrorlangan `switch` (Repeated Switches)

**Belgisi**: bir xil `switch` yoki `if/else` zanjiri kod bazasining bir necha joyida takrorlanadi (6.10).

**Nega muammo**: yangi variant qo'shilganda barcha takrorlarni topish kerak va bittasi doim esdan chiqadi - xato faqat shu variant uchrashganda chiqadi.

**Tuzatish**: xatti-harakatni enum ichiga ko'chirish, Replace Conditional with Polymorphism, yoki `sealed` + pattern matching (25.3).

## 32.8 Sikllar (Loops)

**Belgisi**: filtrlash, mapping va yig'ish qo'lda sikl bilan yozilgan.

**Nega muammo**: sikl **nima** qilayotganini aytmaydi, faqat **qanday** qilayotganini ko'rsatadi. O'quvchi niyatni o'zi chiqarib olishi kerak.

**Tuzatish**: Replace Loop with Pipeline ([35-bob](35-refaktoring-harakatlari-katalogi-i-funksiya.md)) - lekin 7.7 dagi mezonni hisobga olib: erta chiqish, yon ta'sir va istisno bo'lsa sikl qoladi.

## 32.9 Dangasa element (Lazy Element)

**Belgisi**: hech narsa qo'shmaydigan abstraksiya - bitta metodi bor interfeys, faqat bazaviy sinfni chaqiradigan voris sinf, bitta qatordan iborat va bir joyda chaqiriladigan funksiya nomi o'z tanasi bilan bir xil ma'noda.

**Nega muammo**: har bir qo'shimcha daraja o'qish narxini oshiradi, lekin foyda bermaydi ([patternlar hujjatidagi](../patterns/README.md) Poltergeist va Yo-Yo bilan qardosh).

**Tuzatish**: Inline Function, Inline Class, Collapse Hierarchy ([37-bob](37-refaktoring-harakatlari-katalogi-iii-shart.md)). Ehtiyot: kelgusi o'zgarish uchun qo'yilgan abstraksiya dangasa emas ([arxitektor hujjatidagi](../architect/README.md) abstraksiyaning maqsadi bo'limi).

## 32.10 Vaqtinchalik maydon (Temporary Field)

16.8 da ko'rilgan. Hid sifatida belgisi: maydon faqat ba'zi metodlar ishlaganda to'ldirilgan, qolgan vaqt `null`.

**Tuzatish**: Extract Class (vaqtinchalik maydonlar guruhini o'z sinfiga olish) yoki mahalliy o'zgaruvchiga aylantirish; `null` holatini Introduce Special Case bilan ifodalash.

## 32.11 Uzun xabar zanjiri (Message Chains)

**Belgisi**: `a.b().c().d().e()` - chaqiruvchi tuzilmaning bir necha darajasini biladi (14.4).

**Nega muammo**: oraliq turlardan birortasi o'zgarsa, zanjir buziladi. Chaqiruvchi o'ziga kerak bo'lmagan turlarga bog'lanib qoladi.

**Tuzatish**: Hide Delegate ([36-bob](36-refaktoring-harakatlari-katalogi-ii-malumot.md)) - oraliq obyekt delegatsiya metodi beradi; yoki Extract Function (zanjirni bir metodga olib, uni egasiga ko'chirish - Move Function).

## 32.12 Vositachi (Middle Man)

**Belgisi**: sinfning metodlarining katta qismi boshqa obyektga delegatsiya qiladi va o'zi hech narsa qilmaydi.

**Nega muammo**: 32.11 ning teskarisi - delegatsiyani yashirishga urinish ortiqcha ketgan. Har bir yangi metod ikki joyda yoziladi.

**Tuzatish**: Remove Middle Man (chaqiruvchi to'g'ridan-to'g'ri murojaat qiladi) yoki Inline Function. Eslatma: fasad va adapter atayin "vositachi" - ular hid emas, chunki ular chegara vazifasini bajaradi.

## 32.13 Izohlar hid sifatida (Comments)

[9-bobda](09-yomon-izohlar-katalogi.md) izohlarning katalogi berilgan. Hid sifatida muhim nuqtasi: izohlar ko'p bo'lgan joy ko'pincha **yomon kodni oqlash** uchun ishlatiladi. Izoh "deodorant" vazifasini bajaradi: hidni yashiradi, lekin yo'qotmaydi.

**Tuzatish**: Extract Function (izoh nomga aylanadi, 8.2), Change Function Declaration (nom aniqlashadi), Introduce Assertion (taxmin kodga aylanadi).

## 32.14 Bu hid emas: qachon tegmaslik kerak

Hid ro'yxati faqat **nomzodlar** beradi, hukm bermaydi. To'rtta holatda hidga tegmaslik to'g'ri qaror.

| Holat | Nega tegmaslik |
|---|---|
| Kod ishlayapti va o'zgarmaydi | tuzatish narxi foydadan ko'p ([arxitektor hujjatidagi](../architect/README.md) "qachon tegmaslik kerak" bo'limi) |
| Testlar yo'q | refaktoring xavfli, oldin test kerak |
| Hid chegarada (adapter, DTO) | ataylab shunday |
| Soxta takrorlanish | birlashtirish noto'g'ri abstraksiya beradi (32.2) |

## 32.15 Amalda qo'llash

- [ ] Eng ko'p o'zgaradigan 10 faylni olib, shu bobdagi hidlar bo'yicha ro'yxat tuzing va har biriga refaktoring harakatini belgilang.
- [ ] Takrorlangan kod joylarini 32.2 jadvalidagi to'rt turga ajratib, soxta takrorlanishni alohida belgilang.
- [ ] Bir xil parametr guruhlarini (data clumps) grep bilan topib, har biriga record kiriting.
- [ ] Takrorlangan `switch` zanjirlarini sanab, xatti-harakatni enum yoki `sealed` ierarxiyaga ko'chiring.
- [ ] `public static` o'zgaradigan maydonlarni topib, inkapsulyatsiya qilib keyin bog'liqlikka aylantiring.
- [ ] Uch darajadan uzun chaqiruv zanjirlarini topib, Hide Delegate yoki Move Function qo'llang.
- [ ] Faqat delegatsiya qiladigan sinflarni ko'rib, chegara vazifasini bajarmaganlarini olib tashlang.
- [ ] Izohlar eng ko'p to'plangan uch faylni tanlab, izohlarni metod nomlariga aylantirishni sinab ko'ring.

---

[&larr; 31. TDD intizomi va kod dizayniga ta'siri](31-tdd-intizomi-va-kod-dizayniga-tasiri.md) · [Mundarija](README.md) · [33. Kod hidlari katalogi II: sinf, ierarxiya, bog'liqlik &rarr;](33-kod-hidlari-katalogi-ii-sinf-ierarxiya.md)
