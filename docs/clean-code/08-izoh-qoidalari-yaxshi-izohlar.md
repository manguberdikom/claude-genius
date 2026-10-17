<!-- doc: clean-code | chapter: 8 | part: III. Izoh va hujjat -->

[Barcha hujjatlar](../../README.md) / [Toza kod qoidalari](README.md)

> Holat: tekshirilmoqda. Da'volar hali manbaga solishtirilmoqda.

# 8. Izoh qoidalari: yaxshi izohlar (Comments: The Good Ones)

<details>
<summary>Bu bobdagi 11 bo'lim</summary>

- [8.1 Izoh - muvaffaqiyatsizlikni tan olish](#81-izoh---muvaffaqiyatsizlikni-tan-olish)
- [8.2 O'zini kodda tushuntirish: izohni funksiyaga aylantirish](#82-ozini-kodda-tushuntirish-izohni-funksiyaga-aylantirish)
- [8.3 Huquqiy va litsenziya izohlari](#83-huquqiy-va-litsenziya-izohlari)
- [8.4 Ma'lumot beruvchi va maqsadni tushuntiruvchi izoh](#84-malumot-beruvchi-va-maqsadni-tushuntiruvchi-izoh)
- [8.5 Aniqlashtiruvchi izoh va uning xavfi](#85-aniqlashtiruvchi-izoh-va-uning-xavfi)
- [8.6 Oqibat haqida ogohlantirish](#86-oqibat-haqida-ogohlantirish)
- [8.7 TODO, FIXME va ularning hayot muddati](#87-todo-fixme-va-ularning-hayot-muddati)
- [8.8 Kuchaytiruvchi izoh](#88-kuchaytiruvchi-izoh)
- [8.9 Formula, standart va huquqiy asos havolasi](#89-formula-standart-va-huquqiy-asos-havolasi)
- [8.10 Izohni qachon va qaysi darajada yozish](#810-izohni-qachon-va-qaysi-darajada-yozish)
- [8.11 Amalda qo'llash](#811-amalda-qollash)

</details>


Izohning "nima" emas "nega" yozish qoidasi [arxitektor hujjatidagi](../architect/README.md) izohning "nega" qoidasida berilgan. Bu bobda qolgan qism: izoh qanday holatlarda haqli ekanining to'liq ro'yxati. Keyingi bob esa yomon izohlarning katalogi. Ikkisi birga review paytida izohni qoldirish yoki o'chirish qarorini bir necha soniyada beradi.

## 8.1 Izoh - muvaffaqiyatsizlikni tan olish

Izohning har bir qo'llanishi kichik mag'lubiyat: niyatni kod bilan ifodalay olmaganimiz uchun tabiiy tilga murojaat qilyapmiz. Shu qarash izohga to'g'ri munosabat beradi - izohni yozishdan oldin ikki marta kodni o'zgartirishga urinish kerak.

Shundan kelib chiqadigan ikkinchi haqiqat: izoh eskiradi, kod esa eskirmaydi. Kompilyator izohni tekshirmaydi, test izohni tasdiqlamaydi. Shu sababli kod bazasidagi eng yosh izoh ham yolg'on bo'lishi mumkin, va o'quvchi izohga ishonib xato qiladi. Izohni saqlash uchun **egalik** kerak: kim o'zgartirsa, izohni ham o'zgartiradi.

## 8.2 O'zini kodda tushuntirish: izohni funksiyaga aylantirish

Ko'p izohlarni mexanik ravishda kodga aylantirish mumkin. Eng tez usul: izohni funksiya nomiga yoki o'zgaruvchi nomiga ko'chirish.

```java
// yomon: izoh shartni tushuntiradi
// xodim nafaqa olishga haqli ekanini tekshir
if (employee.flags & HOURLY_FLAG) != 0 && employee.age > 65) { ... }

// yaxshi: izoh metod nomiga aylandi
if (employee.isEligibleForFullBenefits()) { ... }
```

Shu almashtirishning uchta shakli bor: izoh → metod nomi, izoh → mahalliy o'zgaruvchi nomi, izoh → nomlangan konstanta. Uchtasi ham izohni yo'qotib, ma'noni kodda qoldiradi.

## 8.3 Huquqiy va litsenziya izohlari

Fayl boshidagi litsenziya, mualliflik va patent izohlari haqli va majburiy bo'lishi mumkin. Ularning qoidasi: qisqa bo'lishi va tashqi hujjatga havola qilishi, butun litsenziya matnini har faylga ko'chirmaslik.

```java
/*
 * Copyright (c) 2026 Shop LLC. Barcha huquqlar himoyalangan.
 * Litsenziya shartlari: LICENSE faylida.
 */
```

Agar litsenziya sarlavhasi majburiy bo'lsa, uni qo'lda yozish emas, Spotless `licenseHeader` qoidasi bilan avtomatlashtirish kerak (13.3).

## 8.4 Ma'lumot beruvchi va maqsadni tushuntiruvchi izoh

Ikki haqli toifa. **Ma'lumot beruvchi** izoh kodda ko'rinmaydigan faktni beradi: formatning ma'nosi, tashqi tizim xatti-harakati, kutilayotgan natija shakli. **Maqsadni tushuntiruvchi** izoh esa qarorning asosini aytadi: nega shu yondashuv tanlangan.

```java
// Format: kk:dd:ss AAA, MM-kk-yyyy  (bank fayli spetsifikatsiyasi, 3.4-bo'lim)
private static final Pattern TIME_MATCHER =
        Pattern.compile("\\d*:\\d*:\\d* \\w*, \\w*-\\d*-\\d*");

// Bu yerda tartiblash kerak: bank fayli yozuvlari tartibsiz keladi,
// lekin settlement ketma-ketligi hisobga ta'sir qiladi (shartnoma 5.1).
rows.sort(comparing(SettlementRow::sequenceNumber));
```

Ikkinchi shakl eng qimmatli izoh turi, chunki uni kodga ko'chirish mumkin emas: kod nima qilayotganini aytadi, nega shu variant tanlanganini aytmaydi.

## 8.5 Aniqlashtiruvchi izoh va uning xavfi

Ba'zan tushunarsiz, lekin o'zgartirib bo'lmaydigan kod bo'ladi: standart kutubxona chaqiruvi, tashqi API javobi, murakkab matematik ifoda. Bunda aniqlashtiruvchi izoh haqli.

```java
assertTrue(a.compareTo(a) == 0);    // a == a
assertTrue(a.compareTo(b) != 0);    // a != b
assertTrue(a.compareTo(ab) == -1);  // a < ab
```

Xavfi shunda: izoh noto'g'ri bo'lsa, u xatoni ikki marta kuchaytiradi. Shuning uchun aniqlashtiruvchi izoh yozishdan oldin savol berish kerak: shu kodni o'zgartirib tushunarli qilib bo'lmaydimi. Javob "yo'q" bo'lsa, izoh qoladi.

## 8.6 Oqibat haqida ogohlantirish

Boshqa ishlab chiquvchini xatodan to'sadigan izoh haqli, chunki u aniq va qimmat ma'lumot beradi.

```java
// Bu testni mahalliy ishga tushirmang: 5 daqiqa ketadi va real bank
// sandbox'ida 200 ta tranzaksiya yaratadi. Faqat nightly pipeline'da.
@Tag("slow")
@Test
void settlesTwoHundredPayments() { ... }

// SimpleDateFormat thread-safe emas: har bir chaqiruvda yangi nusxa kerak.
// (Bu kod legacy integratsiyada qolgan, yangi kodda DateTimeFormatter ishlatiladi.)
public static SimpleDateFormat legacyFormatter() {
    return new SimpleDateFormat("dd-MM-yyyy");
}
```

## 8.7 TODO, FIXME va ularning hayot muddati

`TODO` izohi haqli, lekin faqat uchta shart bilan: nima qilinishi kerakligi aniq yozilgan, kim mas'ul ekani ko'rinadi (yoki ticket havolasi bor), va qachongacha amal qilishi aytilgan. Shartsiz `TODO` arxeologiyaga aylanadi va yillar davomida yashaydi.

```java
// yomon
// TODO: buni tuzatish kerak

// yaxshi: ticket, sabab va olib tashlash sharti
// TODO(SHOP-4821): vaqtinchalik yechim. Bank yangi API (v3) ni 2026-Q3 da chiqaradi,
// shundan keyin bu mapping va retry kodi butunlay o'chiriladi.
```

Amaliy intizom: `TODO` lar sonini CI da o'lchash va o'sishini bloklash; `FIXME` ni esa umuman taqiqlash (u "buzilgan kod merge qilindi" degani). Har chorakda `TODO` ro'yxatini ko'rib chiqish va eskirganini o'chirish.

## 8.8 Kuchaytiruvchi izoh

Ba'zan kodning bir qismi ahamiyatsiz ko'rinadi, lekin aslida kritik. Kuchaytiruvchi izoh shu ahamiyatni ta'kidlaydi va keyingi odamni "optimizatsiya" qilib buzishdan to'sadi.

```java
// trim() shart: boshida bo'sh joy bo'lsa, bank fayli kaliti noto'g'ri
// hisoblanadi va yozuv dublikat sifatida rad etiladi. Olib tashlamang.
String key = line.substring(0, 16).trim();
```

## 8.9 Formula, standart va huquqiy asos havolasi

Hisoblash qoidasi tashqi manbadan kelganda, manbani ko'rsatish izohning eng foydali shakli: u kodni tekshirish imkonini beradi va qoida o'zgarganda qayerga qarashni aytadi.

```java
// QQS stavkasi: Soliq kodeksi 258-moddasi, 2026-01-01 dan 12%.
// O'zgarish bo'lsa qonun hujjatlari portalidan tekshiriladi va bu yerda yangilanadi.
private static final BigDecimal VAT_RATE = new BigDecimal("0.12");

// IBAN tekshiruv algoritmi: ISO 13616 va ISO 7064 MOD-97-10.
public boolean isValid(String iban) { ... }
```

## 8.10 Izohni qachon va qaysi darajada yozish

Avvalgi bo'limlar qaysi izoh haqli ekanini aytdi. Qolgan ikki savol izohning sifatini belgilaydi: izoh qachon yoziladi va qanchalik yuqori darajada yoziladi.

**Keyinga qoldirilgan izoh yomon izoh bo'ladi.** Ko'pchilik izohni oxiriga, kod barqarorlashgandan keyinga qoldiradi. Ousterhout buning oqibatini aniq ko'rsatadi: kechiktirish ko'pincha izoh umuman yozilmasligi bilan tugaydi, chunki kod ko'paygan sari ish hajmi kattalashadi va to'xtab izoh yozish uchun qulay payt hech qachon kelmaydi. Agar yozilsa ham, yaxshi chiqmaydi: bu paytda muallif aqlan boshqa ishga o'tgan, dizayn qarorlarini eslamaydi va koddan ko'chirib yozadi, natijada izoh kodni takrorlaydi va eng muhim narsalar yozilmay qoladi (Ousterhout, *A Philosophy of Software Design*, 1-nashr, Yaknyam Press, 2018, 15.1).

Shundan tartib chiqadi: interfeys izohi metod tanasidan OLDIN yoziladi. Yangi sinf uchun avval sinf izohi, keyin muhim public metodlarning izohi va imzosi (tanasi bo'sh), keyin maydonlar, keyin tanalar; har yangi metod uchun izoh yana tanadan oldin yoziladi, shuning uchun yozilmagan izoh qarzi yig'ilmaydi (shu yerda, 15.2).

**Yuqori darajadagi izoh kamroq eskiradi.** Izoh koddan abstraktroq bo'lsa, u kodning tafsilotlarini takrorlamaydi va mayda o'zgarishdan buzilmaydi: faqat xatti-harakatning o'zi o'zgarsa tegish kerak bo'ladi (shu yerda, 16.6). Shu sababli umumiy qoida: izoh tasvirlayotgan koddan qancha uzoqda tursa, shuncha abstrakt bo'lishi kerak (shu yerda, 16.2). Bu 8.1 dagi "izoh eskiradi" muammosining eng arzon yechimi: izohni o'chirish emas, uning darajasini ko'tarish.

```java
public SettlementResult settle(SettlementBatch batch) {
    // yaxshi: metod ustidagi yuqori daraja, ichki o'zgarishdan buzilmaydi
    // Uch bosqich: (1) valyuta va summa tekshiruvi, (2) bank bilan
    // yopish, (3) rad etilgan qatorlarni audit log'ga yozish.
    List<SettlementRow> valid = validator.accept(batch.rows());

    // yomon: kodni so'zma-so'z takrorlaydi va har refaktoringda eskiradi
    // valid ro'yxati bo'yicha aylanib, har qatorni bankka yuboradi
    for (SettlementRow row : valid) {
        bank.close(row);
    }
    return SettlementResult.of(valid, batch.rejected());
}
```

**Izoh sonining mo'ljali bor, lekin u maqsad emas.** IBM da o'tkazilgan va Capers Jones keltirgan o'lchovga ko'ra o'n gapga taxminan bitta izoh zichligida kodning tushunarliligi eng yuqori bo'lgan: izoh kamayganda kod qiyin o'qilgan, ko'paytirilganda ham tushunarlilik pasaygan (McConnell, *Code Complete*, 2-nashr, Microsoft Press, 2004, 32.4 (792-bet)). Shu bilan birga McConnell bu raqamni standartga aylantirishdan ogohlantiradi: "har besh qatorga bitta izoh" talabi programmist aniq kod yozmasligining simptomini davolaydi, sababini emas. Izoh soni to'g'ri jarayonning yon natijasi bo'lishi kerak, mezon esa boshqa: har bir izoh foydali ekanmi (shu yerda, 32.4 (792-bet)).

Izoh uzun chiqqan holat alohida signal: u izohni qisqartirish emas, abstraksiyaga qaytish kerakligini bildiradi. Bu signal Javadoc bobidagi [hujjatni tasvirlash qiyinligi](10-javadoc-va-api-hujjati.md#1011-hujjatni-tasvirlash-qiyinligi-red-flag-hard-to-describe) qoidasida ko'rilgan.

## 8.11 Amalda qo'llash

- [ ] Kod bazasidagi barcha izohlarni sanab, har birini 8-9 boblardagi toifalarga ajratib belgilang.
- [ ] Shartni yoki hisobni tushuntiradigan izohlarni metod yoki o'zgaruvchi nomiga aylantirib o'chiring.
- [ ] Har bir `TODO` ga ticket havolasi, sabab va olib tashlash shartini qo'shing; shartsizlarini o'chiring.
- [ ] `FIXME` larni ro'yxatlab, har birini yo tuzating, yo ticketga aylantirib izohni olib tashlang.
- [ ] CI da `TODO` sonini o'lchab, o'sishini ogohlantirishga aylantiring.
- [ ] Soliq, tarif va huquqiy hisoblar yonida rasmiy asos havolasi borligini tekshirib, yo'qlarini qo'shing.
- [ ] Litsenziya sarlavhalarini Spotless `licenseHeader` bilan avtomatlashtiring.
- [ ] Tashqi tizim cheklovlari (limit, format, thread-safety) kodda izohlanganini tekshirib, yetishmaganini qo'shing.
- [ ] Yangi sinf va metodda interfeys izohini tanadan oldin yozish tartibini joriy qilib, past darajadagi izohlarni yuqori darajaga ko'taring (8.10).

## Manbalar

- Robert C. Martin, *Clean Code*, 4-bob - izoh yomon kodni qoplamasligi, o'zini kodda tushuntirish
- Robert C. Martin, *Clean Code*, 4-bob ("Good Comments") - huquqiy, ma'lumot beruvchi, maqsadni tushuntiruvchi, aniqlashtiruvchi, ogohlantiruvchi izoh, TODO va kuchaytirish
- Robert C. Martin, *Clean Code*, 17-bob, C1-C5 - izoh evristikalari
- John Ousterhout, *A Philosophy of Software Design*, 1-nashr, Yaknyam Press,
  2018, 15.1, 15.2 - izohni keyinga qoldirishning oqibatlari va interfeys
  izohini metod tanasidan oldin yozish tartibi
- John Ousterhout, *A Philosophy of Software Design*, 1-nashr, Yaknyam Press,
  2018, 16.2, 16.6 - izoh koddan qancha uzoq bo'lsa shuncha abstrakt
  bo'lishi va yuqori darajadagi izohning kamroq eskirishi
- Steve McConnell, *Code Complete*, 2-nashr, Microsoft Press, 2004, 32.4
  (792) - Capers Jones keltirgan IBM o'lchovi: o'n gapga bitta izoh
  zichligida tushunarlilik eng yuqori; izoh sonini standartga aylantirish
  simptomni davolashi

---

[&larr; 7. Sikl, iteratsiya va to'plam bilan ishlash](07-sikl-iteratsiya-va-toplam-bilan-ishlash.md) · [Mundarija](README.md) · [9. Yomon izohlar katalogi &rarr;](09-yomon-izohlar-katalogi.md)
