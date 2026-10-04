<!-- doc: clean-code | chapter: 35 | part: X. Hid katalogi va refaktoring harakatlari -->

[Toza kod yozuvchining qoidalari](../../README.md) / [Toza kod qoidalari](README.md)

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

**Qachon**: kod bo'lagi alohida nom olishga arziydi; izoh yozish ehtiyoji tug'ilgan (8.2).

**Mexanika**: yangi funksiya yaratish va unga maqsadni aytuvchi nom berish → kod bo'lagini ko'chirish → mahalliy o'zgaruvchilarni parametr yoki qaytish qiymatiga aylantirish → kompilyatsiya va test → chaqiruvchini almashtirish.

**Teskari**: Inline Function (35.2).

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

**Qachon**: funksiya tanasi nomidan ravshanroq; keraksiz vositachilik (32.9).

**Mexanika**: barcha chaqiruvchilarni topish → har birini tana bilan almashtirish → funksiyani o'chirish → test.

**Teskari**: Extract Function.

## 35.3 O'zgaruvchi ajratish (Extract Variable)

**Qachon**: ifoda tushunish uchun nom talab qiladi (6.1, G19).

**Mexanika**: ifodadan oldin `final` o'zgaruvchi e'lon qilish → ifodani ko'chirish → asl joyni o'zgaruvchi bilan almashtirish.

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

**Teskari**: Inline Variable.

## 35.4 O'zgaruvchini ichkariga kiritish (Inline Variable)

**Qachon**: o'zgaruvchi nomi ifodadan ko'proq ma'lumot bermaydi (`boolean result = order.isPaid();`).

**Mexanika**: o'zgaruvchi `final` ekanini tekshirish → har bir ishlatilishni ifoda bilan almashtirish → e'lonni o'chirish.

## 35.5 Funksiya e'lonini o'zgartirish (Change Function Declaration)

**Qachon**: nom noaniq (32.1); parametr qo'shish yoki olib tashlash kerak; parametr turini kuchaytirish kerak (21.8).

**Mexanika (migratsiya bilan)**: eski funksiya tanasini yangi nomli funksiyaga ko'chirish → eski funksiyani yangisiga delegatsiya qiluvchi qilib qoldirish va `@Deprecated` qilish → chaqiruvchilarni bosqichma-bosqich ko'chirish → eski funksiyani o'chirish.

Bu "parallel o'zgarish" usuli public API uchun majburiy ([arxitektor hujjatidagi](../architect/README.md) orqaga moslik bo'limi).

## 35.6 O'zgaruvchini inkapsulyatsiya qilish (Encapsulate Variable)

**Qachon**: ma'lumotga kirish joylari ko'p va uni o'zgartirish kerak; global ma'lumot (32.4).

**Mexanika**: ma'lumot uchun getter va setter funksiya yaratish → barcha to'g'ridan-to'g'ri murojaatlarni funksiya chaqiruviga almashtirish → ma'lumot ko'rinishini toraytirish → endi turni yoki tuzilishni xavfsiz o'zgartirish mumkin.

```java
// Oldin: global ma'lumot
public static List<Order> defaultOrders = new ArrayList<>();

// Keyin: kirish inkapsulyatsiyalangan, keyingi qadam - bog'liqlikka aylantirish
private static final List<Order> defaultOrders = new ArrayList<>();

public static List<Order> defaultOrders() { return List.copyOf(defaultOrders); }

public static void addDefaultOrder(Order order) { defaultOrders.add(order); }
```

## 35.7 O'zgaruvchini qayta nomlash (Rename Variable / Rename Field)

**Qachon**: nom maqsadni aytmaydi (32.1).

**Mexanika**: IDE refaktoringi bilan bajarish (3.15) → satr literallarini va reflektiv havolalarni alohida tekshirish → alohida commit qilish.

## 35.8 Parametr obyektini kiritish (Introduce Parameter Object)

**Qachon**: parametrlar guruhi birga sayohat qiladi (32.6); argument soni to'rtdan oshgan (5.1).

**Mexanika**: yangi `record` yaratish → yangi parametr bilan overload qo'shish → eski metodni yangisiga delegatsiya qilish → chaqiruvchilarni ko'chirish → eski metodni o'chirish → validatsiyani record ga ko'chirish (5.6).

## 35.9 Funksiyalarni sinfga birlashtirish (Combine Functions into Class)

**Qachon**: bir necha funksiya bir xil ma'lumot bilan ishlaydi va har biri shu ma'lumotni parametr sifatida oladi.

**Mexanika**: umumiy ma'lumotni maydon sifatida saqlaydigan sinf yaratish → funksiyalarni sinfga ko'chirish → parametrlarni maydonga aylantirish.

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

**Qachon**: bir xil kirish ma'lumotidan bir necha hosila qiymat hisoblanadi va hisob bir necha joyda takrorlanadi.

**Mexanika**: kirish ma'lumotidan boyitilgan nusxa qaytaruvchi funksiya yaratish → har bir hosila hisobni shu funksiyaga ko'chirish → chaqiruvchilarni natijadan o'qishga o'tkazish.

Bu Combine Functions into Class ning funksional varianti; o'zgarmas ma'lumot bilan ishlaganda afzal ([16-bob](16-ozgarmaslik-va-holat-boshqaruvi-kod.md)).

## 35.11 Bosqichlarni ajratish (Split Phase)

**Qachon**: funksiya ikki ketma-ket ishni bajaradi - parslash keyin hisoblash, tayyorlash keyin yuborish.

**Mexanika**: ikkinchi bosqichni alohida funksiyaga ajratish → bosqichlar orasida oraliq ma'lumot tuzilmasi kiritish → birinchi bosqichni oraliq tuzilmani qaytaradigan qilish.

```java
// Keyin: ikki bosqich va ular orasidagi oraliq tur
record PriceData(int quantity, Money itemPrice, ShippingMethod shipping) { }

Money price(Order order) {
    return applyPrices(parsePriceData(order));
}
```

## 35.12 Funksiyani ko'chirish (Move Function)

**Qachon**: funksiya o'zi turgan sinfdan boshqa sinf ma'lumotiga ko'proq murojaat qiladi (noto'g'ri joylashgan javobgarlik, 33.12; feature envy).

**Mexanika**: funksiya ishlatadigan elementlarni tekshirish → maqsad sinfga nusxa ko'chirish → asl joyni delegatsiyaga aylantirish → chaqiruvchilarni ko'chirish → asl funksiyani o'chirish.

## 35.13 Gaplarni funksiyaga ko'chirish va chaqiruvchiga chiqarish

**Move Statements into Function**: bir xil gap har bir chaqiruv joyida funksiyadan oldin/keyin takrorlanadi → uni funksiya ichiga ko'chirish.

**Move Statements to Callers**: teskari holat - funksiya ichidagi gap chaqiruvchilarning bir qismi uchun to'g'ri emas → uni chaqiruvchilarga chiqarish.

Ikkisi juft harakat va ular funksiya chegarasini aniqlashtirishga xizmat qiladi.

## 35.14 Inline kodni funksiya chaqiruviga almashtirish

**Qachon**: kod bo'lagi mavjud funksiya bilan bir xil ishni qiladi (takrorlanish, 32.2).

**Mexanika**: kod bo'lagi va funksiya aynan bir xil xatti-harakat berishini tekshirish → kodni chaqiruv bilan almashtirish → test.

## 35.15 Gaplarni surish (Slide Statements)

**Qachon**: bog'liq kod bir joyda to'planmagan; e'lon va ishlatish orasida masofa bor (11.5, G10).

**Mexanika**: ko'chirilayotgan gap va orasidagi gaplar o'rtasida bog'liqlik yo'qligini tekshirish (o'qish/yozish ziddiyati) → gapni surish → test.

Bu harakat ko'pincha Extract Function dan oldin bajariladi: oldin bog'liq kod yoniga yig'iladi, keyin ajratiladi.

## 35.16 Siklni bo'lish (Split Loop)

**Qachon**: bir sikl ikki mustaqil ishni bajaradi (7.3).

**Mexanika**: siklni nusxalash → har bir nusxada faqat bitta ishni qoldirish → test → har bir siklni Extract Function bilan nomlash.

## 35.17 Siklni quvurga almashtirish (Replace Loop with Pipeline)

**Qachon**: sikl filtrlash va mapping qiladi (32.8), va 7.7 mezoni quvurni afzal ko'rsatadi.

**Mexanika**: sikldan oldin to'plamni `stream()` ga olish → har bir sikl ichidagi amalni mos quvur amaliga aylantirish (filtr → `filter`, o'zgartirish → `map`, yig'ish → `collect`) → sikl bo'sh qolganda o'chirish.

## 35.18 O'lik kodni o'chirish (Remove Dead Code)

**Qachon**: kod chaqirilmaydi yoki shart hech qachon bajarilmaydi (33.10, G9).

**Mexanika**: IDE inspeksiyasi va qamrov hisoboti bilan tasdiqlash → o'chirish → **izohga olmaslik** (9.8) → test.

Refleksiya, Spring, Jackson va test orqali chaqirilishi mumkin bo'lgan kodni tekshirish kerak: statik tahlil ularni "o'lik" deb ko'rsatadi.

## 35.19 O'zgaruvchini bo'lish (Split Variable)

**Qachon**: bitta o'zgaruvchi bir necha maqsadda ishlatiladi (`temp` ikki marta boshqa qiymat uchun).

**Mexanika**: har bir maqsad uchun yangi `final` o'zgaruvchi kiritish → mos ishlatilishlarni almashtirish → test → nomlarni aniqlashtirish.

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

**Qachon**: maydon boshqa maydonlardan hisoblanadi, lekin alohida saqlanadi va sinxron ushlash kerak (32.5).

**Mexanika**: hosila maydonni hisoblaydigan metod yaratish → o'qish joylarini metodga o'tkazish → maydonni va uni yangilaydigan kodni o'chirish.

```java
// Oldin: total maydoni va uni yangilash mantiqi
private Money total;
public void addLine(OrderLine line) { lines.add(line); total = total.plus(line.amount()); }

// Keyin: hisob so'rov vaqtida
public Money total() {
    return lines.stream().map(OrderLine::amount).reduce(Money.ZERO, Money::plus);
}
```

Agar hisob qimmat bo'lsa va o'lchov muammo ko'rsatsa, keshlash qo'shiladi - lekin oldin o'lchov (1.5).

## 35.21 Amalda qo'llash

- [ ] Eng uzun 10 metodda Extract Function ni ketma-ket qo'llab, har qadamdan keyin test ishga tushiring.
- [ ] Murakkab ifodalarni Extract Variable bilan nomlab, keyin ularni domen metodlariga ko'chirishni ko'rib chiqing.
- [ ] Bir necha maqsadda ishlatilgan mahalliy o'zgaruvchilarni Split Variable bilan ajratib, nomlarini aniqlashtiring.
- [ ] Hosila maydonlarni (`total`, `count`) so'rov metodlariga almashtirib, sinxronlash kodini o'chiring.
- [ ] Noto'g'ri sinfda turgan funksiyalarni Move Function bilan egasiga ko'chiring.
- [ ] Ikki ishni bajaradigan sikllarni Split Loop bilan bo'lib, har birini nomlang.
- [ ] 7.7 mezoniga mos sikllarni Replace Loop with Pipeline bilan quvurga o'tkazing.
- [ ] O'lik kodni qamrov hisoboti bilan tasdiqlab o'chiring va alohida commit qiling.

---

[&larr; 34. Toza kod evristikalarining to'liq ro'yxati](34-toza-kod-evristikalarining-toliq-royxati.md) · [Mundarija](README.md) · [36. Refaktoring harakatlari katalogi II: ma'lumot va inkapsulyatsiya &rarr;](36-refaktoring-harakatlari-katalogi-ii-malumot.md)
