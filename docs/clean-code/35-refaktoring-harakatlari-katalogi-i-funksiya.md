<!-- doc: clean-code | chapter: 35 | part: X. Hid katalogi va refaktoring harakatlari -->

[Barcha hujjatlar](../../README.md) / [Toza kod qoidalari](README.md)

> Holat: tekshirilmoqda. Da'volar hali manbaga solishtirilmoqda.

# 35. Refaktoring harakatlari katalogi I: funksiya va o'zgaruvchi (Refactoring Moves I)

<details>
<summary>Bu bobdagi 21 bo'lim</summary>

- [35.1 Funksiya ajratish (Extract Function)](#351-funksiya-ajratish-extract-function)
- [35.2 Funksiyani ichkariga kiritish (Inline Function)](#352-funksiyani-ichkariga-kiritish-inline-function)
- [35.3 O'zgaruvchi ajratish (Extract Variable)](#353-ozgaruvchi-ajratish-extract-variable)
- [35.4 O'zgaruvchini ichkariga kiritish (Inline Variable)](#354-ozgaruvchini-ichkariga-kiritish-inline-variable)
- [35.5 Funksiya e'lonini o'zgartirish (Change Function Declaration)](#355-funksiya-elonini-ozgartirish-change-function-declaration)
- [35.6 O'zgaruvchini inkapsulyatsiya qilish (Encapsulate Variable)](#356-ozgaruvchini-inkapsulyatsiya-qilish-encapsulate-variable)
- [35.7 O'zgaruvchini qayta nomlash (Rename Variable / Rename Field)](#357-ozgaruvchini-qayta-nomlash-rename-variable--rename-field)
- [35.8 Parametr obyektini kiritish (Introduce Parameter Object)](#358-parametr-obyektini-kiritish-introduce-parameter-object)
- [35.9 Funksiyalarni sinfga birlashtirish (Combine Functions into Class)](#359-funksiyalarni-sinfga-birlashtirish-combine-functions-into-class)
- [35.10 Funksiyalarni transformatsiyaga birlashtirish (Combine Functions into Transform)](#3510-funksiyalarni-transformatsiyaga-birlashtirish-combine-functions-into-transform)
- [35.11 Bosqichlarni ajratish (Split Phase)](#3511-bosqichlarni-ajratish-split-phase)
- [35.12 Funksiyani ko'chirish (Move Function)](#3512-funksiyani-kochirish-move-function)
- [35.13 Gaplarni funksiyaga ko'chirish va chaqiruvchiga chiqarish](#3513-gaplarni-funksiyaga-kochirish-va-chaqiruvchiga-chiqarish)
- [35.14 Inline kodni funksiya chaqiruviga almashtirish](#3514-inline-kodni-funksiya-chaqiruviga-almashtirish)
- [35.15 Gaplarni surish (Slide Statements)](#3515-gaplarni-surish-slide-statements)
- [35.16 Siklni bo'lish (Split Loop)](#3516-siklni-bolish-split-loop)
- [35.17 Siklni quvurga almashtirish (Replace Loop with Pipeline)](#3517-siklni-quvurga-almashtirish-replace-loop-with-pipeline)
- [35.18 O'lik kodni o'chirish (Remove Dead Code)](#3518-olik-kodni-ochirish-remove-dead-code)
- [35.19 O'zgaruvchini bo'lish (Split Variable)](#3519-ozgaruvchini-bolish-split-variable)
- [35.20 Hosila o'zgaruvchini so'rovga almashtirish](#3520-hosila-ozgaruvchini-sorovga-almashtirish)
- [35.21 Amalda qo'llash](#3521-amalda-qollash)

</details>


Legacy kodni refaktoring qilish strategiyasi, chok (seam) topish va strangler usuli [arxitektor hujjatidagi](../architect/README.md) legacy kod va bosqichma-bosqich refaktoring bo'limida. Bu va keyingi ikki bob boshqa narsani beradi: **mexanik harakatlar katalogi**. Har bir harakat uchun nima qilinishi, qachon qo'llanishi va teskari harakati berilgan. Teskari harakat muhim, chunki refaktoring ikki yo'nalishda ham to'g'ri bo'lishi mumkin.

## 35.1 Funksiya ajratish (Extract Function)

**Nom**: 1-nashr - Extract Method (89, 6-bob); 2-nashr - Extract Function (106, 6-bob).

**Qachon**: metod uzun, yoki kod bo'lagini tushuntirish uchun izoh yozish ehtiyoji tug'ilgan (8.2). 1-nashr mezoni uzunlik emas: nom bilan tana orasidagi ma'no masofasi. Ajratish ravshanlikni oshirsa, hatto nom ajratilgan koddan uzun bo'lsa ham ajratiladi.

**Mexanika (1-nashr, 89-90)**: yangi metod yaratish va unga maqsadni aytuvchi nom berish - nima qilishi bo'yicha, qanday qilishi bo'yicha emas → kodni yangi metodga ko'chirish → ko'chirilgan kodda manba metodga mahalliy bo'lgan o'zgaruvchilarni sanash → faqat shu bo'lak ichida ishlatiladigan vaqtinchalik o'zgaruvchilarni yangi metodda e'lon qilish → o'qiladigan mahalliy o'zgaruvchilarni parametr qilib uzatish → mahalliy o'zgaruvchilar hal bo'lgach kompilyatsiya → asl joyni chaqiruv bilan almashtirish → kompilyatsiya va test.

**Chegara (1-nashr, 90)**: ko'chirilgan kod bitta mahalliy o'zgaruvchini o'zgartirsa, bo'lakni so'rov deb qarab natijani shu o'zgaruvchiga tayinlash mumkin. Bittadan ko'p o'zgaruvchi o'zgartirilsa, ajratish shu holida bo'lmaydi: avval Split Variable (35.19) yoki Replace Temp with Query (36.9) qo'llanadi.

**Teskari**: Inline Function (35.2).

**Testsiz va IDE siz**: yuqoridagi mexanika kompilyatsiya va testga tayanadi. Test ham, ishlaydigan refaktoring asbobi ham yo'q bo'lsa, boshqa taktika kerak: sezgir o'zgaruvchi, coupling count va kichik bo'laklardan boshlash ([testsiz monstr metodni qo'lda bo'lish](38-refaktoringni-xavfsiz-bajarish.md#3813-testsiz-monstr-metodni-qolda-bolish-introduce-sensing-variable-extract-what-you-know-coupling-count-gleaning-dependencies)), hamda shart va tanani qanday bo'lish qarori ([qo'lda ajratish strategiyasi](38-refaktoringni-xavfsiz-bajarish.md#3814-qolda-ajratish-strategiyasi-skeletonize-methods-find-sequences-extract-to-the-current-class-first-be-prepared-to-redo-extractions)).

```java
// Oldin
void printOwing(Invoice invoice) {
    System.out.println("***********************");
    System.out.println("**** Mijoz qarzi *****");
    System.out.println("***********************");
    Money outstanding = invoice.outstanding();
    System.out.println("Nomi: " + invoice.customer());
    System.out.println("Summa: " + outstanding);
}

// Keyin
void printOwing(Invoice invoice) {
    printBanner();
    printDetails(invoice, invoice.outstanding());
}
```

## 35.2 Funksiyani ichkariga kiritish (Inline Function)

**Nom**: 1-nashr - Inline Method (95, 6-bob); 2-nashr - Inline Function (115, 6-bob).

**Qachon**: funksiya tanasi nomidan ravshanroq; keraksiz vositachilik (32.9).

**Mexanika (1-nashr, 95)**: metod polimorf emasligini tekshirish → barcha chaqiruvlarni topish → har bir chaqiruvni metod tanasi bilan almashtirish → kompilyatsiya va test → metod e'lonini o'chirish.

**Chegara (1-nashr, 95)**: voris metodni override qilsa, inline qilinmaydi - mavjud bo'lmagan metod override qilinmaydi. 1-nashr yana shuni aytadi: rekursiya, bir nechta return nuqtasi yoki akssessori yo'q boshqa obyektga inline qilish kabi murakkablik chiqsa, bu refaktoringni umuman qilmaslik kerak.

**Teskari**: Extract Function (35.1).

## 35.3 O'zgaruvchi ajratish (Extract Variable)

**Nom**: 1-nashr - Introduce Explaining Variable (101, 6-bob); 2-nashr - Extract Variable (119, 6-bob).

**Qachon**: ifoda tushunish uchun nom talab qiladi (6.1, G19).

**Mexanika (1-nashr, 101)**: `final` vaqtinchalik o'zgaruvchi e'lon qilib, unga murakkab ifodaning bir qismining natijasini berish → ifodadagi shu qismni o'zgaruvchi bilan almashtirish; qism takrorlangan bo'lsa bittadan almashtirish → kompilyatsiya va test → ifodaning qolgan qismlari uchun takrorlash.

```java
// Oldin
return order.quantity() * order.itemPrice()
        - Math.max(0, order.quantity() - 500) * order.itemPrice() * 0.05
        + Math.min(order.quantity() * order.itemPrice() * 0.1, 100);

// Keyin
Money basePrice = order.basePrice();
Money quantityDiscount = order.quantityDiscount();
Money shipping = order.shipping();
return basePrice.minus(quantityDiscount).plus(shipping);
```

**Teskari**: Inline Variable (35.4).

## 35.4 O'zgaruvchini ichkariga kiritish (Inline Variable)

**Nom**: 1-nashr - Inline Temp (96, 6-bob); 2-nashr - Inline Variable (123, 6-bob).

**Qachon**: 1-nashr motivatsiyasi tor: vaqtinchalik bir marta oddiy ifoda bilan tayinlangan va boshqa refaktoringga to'sqinlik qilgan holda. Ko'pincha u zarar qilmaydi va joyida qoldiriladi; Extract Method kabi harakatga to'sqinlik qilsa, inline qilish vaqti keladi.

**Mexanika (1-nashr, 96)**: o'zgaruvchi `final` bo'lmasa `final` deb e'lon qilib kompilyatsiya qilish - bu uning faqat bir marta tayinlanganini tasdiqlaydi → har bir murojaatni tayinlashning o'ng tomoni bilan almashtirish → har o'zgarishdan keyin kompilyatsiya va test → e'lon va tayinlashni o'chirish → kompilyatsiya va test.

## 35.5 Funksiya e'lonini o'zgartirish (Change Function Declaration)

**Nom**: 2-nashr - Change Function Declaration (124, 6-bob). 1-nashrda bu bitta harakat emas, uchta alohida harakat: Rename Method (221, 10-bob), Add Parameter (222, 10-bob) va Remove Parameter (223, 10-bob). Uchovining mexanikasi bir xil shaklda berilgan.

**Qachon**: nom noaniq (32.1); parametr qo'shish yoki olib tashlash kerak; parametr turini kuchaytirish kerak (21.8).

**Mexanika (1-nashr, 221-223)**: signatura super yoki voris sinfda ham amalga oshirilganini tekshirish, bo'lsa har bir implementatsiya uchun takrorlash → yangi nom yoki yangi signatura bilan yangi metod e'lon qilish va eski tanani unga ko'chirish → kompilyatsiya → eski metod tanasini yangisini chaqiradigan qilish → kompilyatsiya va test → eski metodga barcha murojaatlarni yangisiga o'tkazish, har o'zgarishdan keyin kompilyatsiya va test → eski metodni o'chirish → kompilyatsiya va test.

1-nashr qo'shimchalari: eski metod interfeysning qismi bo'lib o'chirilmasa, u joyida qoldirilib `deprecated` deb belgilanadi (Java da `@Deprecated`). Parametr qo'shish yoki olib tashlash bir nechtadan bo'lsa, ularni birga qilish osonroq. Olib tashlashdan oldin esa parametr sinfda yoki super sinfda ishlatilmasligi tekshiriladi: ishlatilsa, refaktoring qilinmaydi.

ESLATMA: public API uchun eski funksiyani `@Deprecated` holda qoldirib "parallel o'zgarish" yo'lidan borish shu korpusning tavsiyasi; 1-nashr bu qadamni faqat olib tashlanmaydigan interfeys metodi uchun aytadi ([arxitektor hujjatidagi](../architect/README.md) orqaga moslik bo'limi).

## 35.6 O'zgaruvchini inkapsulyatsiya qilish (Encapsulate Variable)

**Nom**: 1-nashr - Encapsulate Field (167, 8-bob) va Self Encapsulate Field (138, 8-bob); 2-nashr - Encapsulate Variable (132, 6-bob).

**Qachon**: ma'lumotga kirish joylari ko'p va uni o'zgartirish kerak; global ma'lumot (32.4).

**Mexanika (1-nashr, 167)**: maydon uchun getter va setter yaratish → sinf tashqarisidagi barcha mijozlarni topish: qiymatni o'qisa getter, qiymatni o'zgartirsa setter chaqiruvi bilan almashtirish → har o'zgarishdan keyin kompilyatsiya va test → barcha mijozlar ko'chgach maydonni `private` qilish → kompilyatsiya va test.

1-nashr nozikligi (167): maydon obyekt bo'lsa va mijoz shu obyektning o'zgartiruvchi metodini chaqirsa, bu o'qish hisoblanadi; setter faqat tayinlashni almashtirish uchun ishlatiladi. Self Encapsulate Field (138) esa bir qadam uzoqroq boradi: sinfning o'zi ham maydonga faqat getter va setter orqali murojaat qiladi.

```java
// Oldin: global ma'lumot
public static List<Order> defaultOrders = new ArrayList<>();

// Keyin: kirish inkapsulyatsiyalangan, keyingi qadam - bog'liqlikka aylantirish
private static final List<Order> defaultOrders = new ArrayList<>();

public static List<Order> defaultOrders() { return List.copyOf(defaultOrders); }

public static void addDefaultOrder(Order order) { defaultOrders.add(order); }
```

## 35.7 O'zgaruvchini qayta nomlash (Rename Variable / Rename Field)

**Nom**: 2-nashr - Rename Variable (137, 6-bob) va Rename Field (244, 9-bob). 1-nashrda o'zgaruvchi yoki maydonni qayta nomlash alohida harakat sifatida yo'q: u faqat Rename Method (221, 10-bob) ni beradi, maydon nomini o'zgartirish esa Split Temporary Variable (104) va Pull Up Field (259) mexanikalari ichida qadam sifatida uchraydi.

**Qachon**: nom maqsadni aytmaydi (32.1).

**Qadamlar (shu korpus amaliyoti, kitobdan iqtibos emas)**: IDE refaktoringi bilan bajarish (3.15) → satr literallarini va reflektiv havolalarni alohida tekshirish → alohida commit qilish.

## 35.8 Parametr obyektini kiritish (Introduce Parameter Object)

**Nom**: ikki nashrda bir xil - 1-nashr Introduce Parameter Object (238, 10-bob); 2-nashr Introduce Parameter Object (140, 6-bob).

**Qachon**: parametrlar guruhi birga sayohat qiladi (32.6); argument soni to'rtdan oshgan (5.1).

**Mexanika (1-nashr, 238)**: parametrlar guruhini ifodalovchi yangi sinf yaratish va uni **o'zgarmas** qilish → kompilyatsiya → Add Parameter bilan yangi parametrni qo'shib, chaqiruvchilarda vaqtincha `null` berish; chaqiruvchi ko'p bo'lsa eski signaturani qoldirib yangisiga delegatsiya qildirish → guruhdagi parametrlarni signaturadan bittadan olib tashlash va chaqiruvchi bilan tanani parametr obyektidan o'qishga o'tkazish → har olib tashlashdan keyin kompilyatsiya va test → oxirida parametr obyektiga ko'chirilishi mumkin bo'lgan xatti-harakatni Move Method bilan ko'chirish; agar u metodning qismi bo'lsa, oldin Extract Method.

1-nashr (242) ta'kidlaydi: asosiy qiymat parametr obyektini kiritishning o'zida emas, keyin boshqa metodlardan xatti-harakatni shu yangi obyektga ko'chirishda.

## 35.9 Funksiyalarni sinfga birlashtirish (Combine Functions into Class)

**Nom**: 2-nashrda yangi - Combine Functions into Class (144, 6-bob). 1-nashrda bu nomdagi harakat yo'q; eng yaqin qarindoshi Extract Class (122, 7-bob), lekin u mavjud sinfni bo'lish haqida.

**Qachon**: bir necha funksiya bir xil ma'lumot bilan ishlaydi va har biri shu ma'lumotni parametr sifatida oladi.

**Qadamlar (shu korpus amaliyoti, kitobdan iqtibos emas)**: umumiy ma'lumotni maydon sifatida saqlaydigan sinf yaratish → funksiyalarni sinfga ko'chirish → parametrlarni maydonga aylantirish.

```java
// Oldin: har bir funksiya bir xil ma'lumotni oladi
Money baseCharge(Reading reading) { ... }
Money taxableCharge(Reading reading) { ... }
BigDecimal calculateBaseRate(Reading reading) { ... }

// Keyin: ma'lumot va mantiq birga
public final class ReadingCalculator {
    private final Reading reading;
    ReadingCalculator(Reading reading) { this.reading = reading; }
    Money baseCharge() { ... }
    Money taxableCharge() { ... }
}
```

## 35.10 Funksiyalarni transformatsiyaga birlashtirish (Combine Functions into Transform)

**Nom**: 2-nashrda yangi - Combine Functions into Transform (149, 6-bob). 1-nashrda yo'q.

**Qachon**: bir xil kirish ma'lumotidan bir necha hosila qiymat hisoblanadi va hisob bir necha joyda takrorlanadi.

**Qadamlar (shu korpus amaliyoti, kitobdan iqtibos emas)**: kirish ma'lumotidan boyitilgan nusxa qaytaruvchi funksiya yaratish → har bir hosila hisobni shu funksiyaga ko'chirish → chaqiruvchilarni natijadan o'qishga o'tkazish.

Bu Combine Functions into Class ning funksional varianti; o'zgarmas ma'lumot bilan ishlaganda afzal ([16-bob](16-ozgarmaslik-va-holat-boshqaruvi-kod.md)).

## 35.11 Bosqichlarni ajratish (Split Phase)

**Nom**: 2-nashrda yangi - Split Phase (154, 6-bob). 1-nashrda yo'q.

**Qachon**: funksiya ikki ketma-ket ishni bajaradi - parslash keyin hisoblash, tayyorlash keyin yuborish.

**Qadamlar (shu korpus amaliyoti, kitobdan iqtibos emas)**: ikkinchi bosqichni alohida funksiyaga ajratish → bosqichlar orasida oraliq ma'lumot tuzilmasi kiritish → birinchi bosqichni oraliq tuzilmani qaytaradigan qilish.

```java
// Keyin: ikki bosqich va ular orasidagi oraliq tur
record PriceData(int quantity, Money itemPrice, ShippingMethod shipping) { }

Money price(Order order) {
    return applyPrices(parsePriceData(order));
}
```

## 35.12 Funksiyani ko'chirish (Move Function)

**Nom**: 1-nashr - Move Method (115, 7-bob); 2-nashr - Move Function (198, 8-bob).

**Qachon**: funksiya o'zi turgan sinfdan boshqa sinf ma'lumotiga ko'proq murojaat qiladi (noto'g'ri joylashgan javobgarlik, 33.12; feature envy).

**Mexanika (1-nashr, 115-117)**: manba metod ishlatadigan va manba sinfda e'lon qilingan barcha elementlarni ko'rib chiqish, ularni ham ko'chirish kerakmi deb qarash → manba sinfning super va voris sinflarida metodning boshqa e'lonlari bormi tekshirish → metodni maqsad sinfda e'lon qilish, kerak bo'lsa maqsad sinfda mazmunliroq nom bilan → kodni ko'chirib yangi joyga moslashtirish → maqsad sinfni kompilyatsiya qilish → manbadan to'g'ri maqsad obyektga qanday murojaat qilishni aniqlash → asl metodni delegatsiya metodiga aylantirish → kompilyatsiya va test → asl metodni o'chirish yoki delegatsiya sifatida qoldirishni hal qilish → o'chirilsa barcha murojaatlarni maqsad metodga o'tkazish → kompilyatsiya va test.

1-nashr nozikliklari (116): metodning boshqa e'lonlari bo'lsa, polimorfizm maqsad sinfda ham ifodalanmasa ko'chirish bo'lmaydi; metod o'z manbasiga murojaat qilsa va maqsad sinfda mexanizm bo'lmasa, manba obyekt havolasi parametr sifatida uzatiladi; istisno ishlovchilari qolishi kerakmi degan qaror alohida qabul qilinadi. Murojaat ko'p bo'lsa, asl metodni delegatsiya sifatida qoldirish osonroq.

## 35.13 Gaplarni funksiyaga ko'chirish va chaqiruvchiga chiqarish

**Nom**: ikkisi ham 2-nashrda yangi - Move Statements into Function (213, 8-bob) va Move Statements to Callers (217, 8-bob). 1-nashrda bu nomlar yo'q.

**Move Statements into Function**: bir xil gap har bir chaqiruv joyida funksiyadan oldin yoki keyin takrorlanadi → uni funksiya ichiga ko'chirish.

**Move Statements to Callers**: teskari holat - funksiya ichidagi gap chaqiruvchilarning bir qismi uchun to'g'ri emas → uni chaqiruvchilarga chiqarish.

Ikkisi juft harakat va ular funksiya chegarasini aniqlashtirishga xizmat qiladi.

## 35.14 Inline kodni funksiya chaqiruviga almashtirish

**Nom**: 2-nashrda yangi - Replace Inline Code with Function Call (222, 8-bob). 1-nashrda yo'q.

**Qachon**: kod bo'lagi mavjud funksiya bilan bir xil ishni qiladi (takrorlanish, 32.2).

**Qadamlar (shu korpus amaliyoti, kitobdan iqtibos emas)**: kod bo'lagi va funksiya aynan bir xil xatti-harakat berishini tekshirish → kodni chaqiruv bilan almashtirish → test.

## 35.15 Gaplarni surish (Slide Statements)

**Nom**: 2-nashrda yangi - Slide Statements (223, 8-bob). 1-nashrda yo'q.

**Qachon**: bog'liq kod bir joyda to'planmagan; e'lon va ishlatish orasida masofa bor (11.5, G10).

**Qadamlar (shu korpus amaliyoti, kitobdan iqtibos emas)**: ko'chirilayotgan gap va orasidagi gaplar o'rtasida bog'liqlik yo'qligini tekshirish (o'qish va yozish ziddiyati) → gapni surish → test.

Bu harakat ko'pincha Extract Function dan oldin bajariladi: oldin bog'liq kod yoniga yig'iladi, keyin ajratiladi.

## 35.16 Siklni bo'lish (Split Loop)

**Nom**: 2-nashrda yangi - Split Loop (227, 8-bob). 1-nashrda yo'q.

**Qachon**: bir sikl ikki mustaqil ishni bajaradi (7.3).

**Qadamlar (shu korpus amaliyoti, kitobdan iqtibos emas)**: siklni nusxalash → har bir nusxada faqat bitta ishni qoldirish → test → har bir siklni Extract Function bilan nomlash.

Siklni nusxalash 1-nashrda ham uchraydi: Replace Temp with Query (97) mexanikasida bir sikl bir nechta qiymatni yig'sa, har bir vaqtinchalik uchun sikl nusxalanadi, chunki sikl juda oddiy bo'lgani uchun nusxalash xavfli emas.

## 35.17 Siklni quvurga almashtirish (Replace Loop with Pipeline)

**Nom**: 2-nashrda yangi - Replace Loop with Pipeline (231, 8-bob). 1-nashrda yo'q; 1999 yilda Java da quvur API si hali yo'q edi.

**Qachon**: sikl filtrlash va mapping qiladi (32.8), va 7.7 mezoni quvurni afzal ko'rsatadi.

**Qadamlar (shu korpus amaliyoti, kitobdan iqtibos emas)**: sikldan oldin to'plamni `stream()` ga olish → har bir sikl ichidagi amalni mos quvur amaliga aylantirish (filtr → `filter`, o'zgartirish → `map`, yig'ish → `collect`) → sikl bo'sh qolganda o'chirish.

## 35.18 O'lik kodni o'chirish (Remove Dead Code)

**Nom**: 2-nashrda yangi - Remove Dead Code (237, 8-bob). 1-nashrda alohida nomlangan harakat sifatida yo'q.

**Qachon**: kod chaqirilmaydi yoki shart hech qachon bajarilmaydi (33.10, G9).

**Qadamlar (shu korpus amaliyoti, kitobdan iqtibos emas)**: IDE inspeksiyasi va qamrov hisoboti bilan tasdiqlash → o'chirish → **izohga olmaslik** (9.8) → test.

Refleksiya, Spring, Jackson va test orqali chaqirilishi mumkin bo'lgan kodni tekshirish kerak: statik tahlil ularni "o'lik" deb ko'rsatadi.

## 35.19 O'zgaruvchini bo'lish (Split Variable)

**Nom**: 1-nashr - Split Temporary Variable (104, 6-bob); 2-nashr - Split Variable (240, 9-bob).

**Qachon**: bitta o'zgaruvchi bir necha maqsadda ishlatiladi (`temp` ikki marta boshqa qiymat uchun).

**Mexanika (1-nashr, 104)**: o'zgaruvchining e'lonidagi va birinchi tayinlashdagi nomini o'zgartirish → yangi o'zgaruvchini `final` qilish → ikkinchi tayinlashgacha bo'lgan barcha murojaatlarni yangi nomga o'tkazish → ikkinchi tayinlash joyida o'zgaruvchini qaytadan e'lon qilish → kompilyatsiya va test → qolgan tayinlashlar uchun shu bosqichni takrorlash.

**Chegara (1-nashr, 104)**: keyingi tayinlashlar `i = i + ifoda` shaklida bo'lsa, bu yig'uvchi o'zgaruvchi va u bo'linmaydi. 1-nashr yig'uvchi operatorlar sifatida qo'shish, satr biriktirish, oqimga yozish va to'plamga qo'shishni sanaydi.

```java
// Oldin: temp ikki maqsadda
double temp = 2 * (height + width);
System.out.println(temp);
temp = height * width;
System.out.println(temp);

// Keyin
final double perimeter = 2 * (height + width);
final double area = height * width;
```

## 35.20 Hosila o'zgaruvchini so'rovga almashtirish

**Nom**: 2-nashrda yangi - Replace Derived Variable with Query (248, 9-bob). 1-nashrda bu nom yo'q; vaqtinchalik o'zgaruvchi uchun o'xshash harakat Replace Temp with Query (97, 6-bob) nomi bilan beriladi va u 36.9 da.

**Qachon**: maydon boshqa maydonlardan hisoblanadi, lekin alohida saqlanadi va sinxron ushlash kerak (32.5).

**Qadamlar (shu korpus amaliyoti, kitobdan iqtibos emas)**: hosila maydonni hisoblaydigan metod yaratish → o'qish joylarini metodga o'tkazish → maydonni va uni yangilaydigan kodni o'chirish.

```java
// Oldin: total maydoni va uni yangilash mantiqi
private Money total;
public void addLine(OrderLine line) { lines.add(line); total = total.plus(line.amount()); }

// Keyin: hisob so'rov vaqtida
public Money total() {
    return lines.stream().map(OrderLine::amount).reduce(Money.ZERO, Money::plus);
}
```

Unumdorlik tashvishi bo'lsa, 1-nashrning Replace Temp with Query bo'limidagi (98) maslahati shu yerda ham amal qiladi: hozircha e'tibor bermaslik kerak, ko'p holatda u ahamiyat qilmaydi; ahamiyat qilganda muammo optimizatsiya bosqichida tuzatiladi, va yaxshi ajratilgan koddan kuchliroq optimizatsiyalar topiladi. Keshlash qo'shish qarori o'lchovdan keyin keladi (1.5).

## 35.21 Amalda qo'llash

- [ ] Eng uzun 10 metodda Extract Function ni ketma-ket qo'llab, har qadamdan keyin test ishga tushiring.
- [ ] Murakkab ifodalarni Extract Variable bilan nomlab, keyin ularni domen metodlariga ko'chirishni ko'rib chiqing.
- [ ] Bir necha maqsadda ishlatilgan mahalliy o'zgaruvchilarni Split Variable bilan ajratib, nomlarini aniqlashtiring; yig'uvchi o'zgaruvchilarni tegmasdan qoldiring.
- [ ] Hosila maydonlarni (`total`, `count`) so'rov metodlariga almashtirib, sinxronlash kodini o'chiring.
- [ ] Noto'g'ri sinfda turgan funksiyalarni Move Function bilan egasiga ko'chiring; murojaat ko'p bo'lsa asl joyni delegatsiya sifatida qoldiring.
- [ ] Ikki ishni bajaradigan sikllarni Split Loop bilan bo'lib, har birini nomlang.
- [ ] 7.7 mezoniga mos sikllarni Replace Loop with Pipeline bilan quvurga o'tkazing.
- [ ] O'lik kodni qamrov hisoboti bilan tasdiqlab o'chiring va alohida commit qiling.

## Manbalar

- Martin Fowler, *Refactoring: Improving the Design of Existing Code*, 1-nashr, Addison-Wesley, 1999, 6-bob (89-114) - Extract Method, Inline Method, Inline Temp, Introduce Explaining Variable va Split Temporary Variable mexanikasi, chegaralari va motivatsiyasi
- Martin Fowler, *Refactoring: Improving the Design of Existing Code*, 1-nashr, Addison-Wesley, 1999, 7-bob (115-117) - Move Method mexanikasi: element tekshiruvi, polimorfizm chegarasi, delegatsiya qoldirish qarori
- Martin Fowler, *Refactoring: Improving the Design of Existing Code*, 1-nashr, Addison-Wesley, 1999, 8-bob (138-139, 167) - Self Encapsulate Field va Encapsulate Field mexanikasi, obyekt maydonidagi nozik holat
- Martin Fowler, *Refactoring: Improving the Design of Existing Code*, 1-nashr, Addison-Wesley, 1999, 10-bob (221-224, 238-242) - Rename Method, Add Parameter, Remove Parameter va Introduce Parameter Object mexanikasi, `deprecated` qoldirish qadami
- Martin Fowler, *Refactoring: Improving the Design of Existing Code*, 1-nashr, Addison-Wesley, 1999, 6-bob (97-98) - Replace Temp with Query ichidagi sikl nusxalash va unumdorlik maslahati
- Martin Fowler, *Refactoring: Improving the Design of Existing Code*, 2-nashr, Addison-Wesley, 2019, "List of Refactorings" va 6, 8, 9-boblar mundarijasi - 2-nashrdagi nomlar va betlar: Extract Function (106), Inline Function (115), Extract Variable (119), Inline Variable (123), Change Function Declaration (124), Encapsulate Variable (132), Rename Variable (137), Introduce Parameter Object (140), Combine Functions into Class (144), Combine Functions into Transform (149), Split Phase (154), Move Function (198), Move Statements into Function (213), Move Statements to Callers (217), Replace Inline Code with Function Call (222), Slide Statements (223), Split Loop (227), Replace Loop with Pipeline (231), Remove Dead Code (237), Split Variable (240), Rename Field (244), Replace Derived Variable with Query (248)
- ESLATMA: 1-nashr betlari shu korpusda ishlatilgan elektron nusxaning raqamlanishi bo'yicha va kitobning o'z mundarijasi bilan mos; qog'oz nashrining bet raqamlari boshqa bo'lishi mumkin
- ESLATMA: 35.7, 35.9, 35.10, 35.11, 35.13, 35.14, 35.15, 35.16, 35.17, 35.18 va 35.20 dagi qadamlar ro'yxati shu korpusning amaliy tavsiyasi, kitobdan olingan emas - bu harakatlar 2-nashrda yangi, 2-nashrning matni esa bizda yo'q (faqat mundarija bor), 1-nashrda esa bu nomlar uchramaydi

---

[&larr; 34. Toza kod evristikalarining to'liq ro'yxati](34-toza-kod-evristikalarining-toliq-royxati.md) · [Mundarija](README.md) · [36. Refaktoring harakatlari katalogi II: ma'lumot va inkapsulyatsiya &rarr;](36-refaktoring-harakatlari-katalogi-ii-malumot.md)
