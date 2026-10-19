<!-- doc: clean-code | chapter: 14 | part: V. Obyekt, ma'lumot va holat -->

[Barcha hujjatlar](../../README.md) / [Toza kod qoidalari](README.md)

> Holat: tekshirilgan (2026-10-19). Manbalar bob oxirida.

# 14. Obyekt va ma'lumot tuzilmasi: inkapsulyatsiya (Objects vs Data Structures)

<details>
<summary>Bu bobdagi 13 bo'lim</summary>

- [14.1 Ma'lumot abstraksiyasi: getter/setter inkapsulyatsiya emas](#141-malumot-abstraksiyasi-gettersetter-inkapsulyatsiya-emas)
- [14.2 Obyekt va ma'lumot tuzilmasining teskariligi](#142-obyekt-va-malumot-tuzilmasining-teskariligi)
- [14.3 Gibrid tuzilma: yarim obyekt, yarim struktura](#143-gibrid-tuzilma-yarim-obyekt-yarim-struktura)
- [14.4 Poyezd avariyasi va tuzilmani yashirish](#144-poyezd-avariyasi-va-tuzilmani-yashirish)
- [14.5 DTO, Active Record va ularning o'rni](#145-dto-active-record-va-ularning-orni)
- [14.6 Maydon ko'rinishi: `public` maydon, `package-private`, `final`](#146-maydon-korinishi-public-maydon-package-private-final)
- [14.7 Ichki to'plamni oshkor qilish va himoyalangan nusxa](#147-ichki-toplamni-oshkor-qilish-va-himoyalangan-nusxa)
- [14.8 Statik holat, utility sinf va `private` konstruktor](#148-statik-holat-utility-sinf-va-private-konstruktor)
- [14.9 Obyekt o'z invariantini qanday himoya qiladi](#149-obyekt-oz-invariantini-qanday-himoya-qiladi)
- [14.10 `this` ning konstruktordan qochib ketishi](#1410-this-ning-konstruktordan-qochib-ketishi)
- [14.11 Chegara interfeysini tizim bo'ylab uzatmaslik](#1411-chegara-interfeysini-tizim-boylab-uzatmaslik)
- [14.12 Hali yozilmagan API o'rniga o'zing xohlagan interfeysni yozish](#1412-hali-yozilmagan-api-orniga-ozing-xohlagan-interfeysni-yozish)
- [14.13 Amalda qo'llash](#1413-amalda-qollash)

</details>


Abstraksiya va chegara [arxitektor hujjatidagi](../architect/README.md) abstraksiya, bog'liqlik va chegara bo'limida ko'rib chiqilgan, Demeter qonuni va Tell-Don't-Ask [patternlar hujjatidagi](../patterns/README.md) Demeter qonuni va "aytib qo'y, so'ramay" printsiplarida. Bu bobda kod darajasidagi qoidalar: inkapsulyatsiyaning haqiqiy ma'nosi, obyekt va struktura farqi, ichki holatni oshkor qilmaslik, va obyektning o'z invariantini himoya qilishi.

## 14.1 Ma'lumot abstraksiyasi: getter/setter inkapsulyatsiya emas

Har bir maydonga getter va setter yozish inkapsulyatsiya emas: u maydonlarni `public` qilishning uzun yo'li. Haqiqiy inkapsulyatsiya ichki ko'rinishni yashiradi va **abstraksiya** taklif qiladi.

```java
// yomon: ichki ko'rinish to'liq oshkor, abstraksiya yo'q
public class Vehicle {
    public double getFuelTankCapacityInGallons() { ... }
    public double getGallonsOfGasoline() { ... }
}
// chaqiruvchi hisoblashni o'zi qiladi - mantiq tarqaladi

// yaxshi: abstraksiya berilgan, ichki ko'rinish yashirin
public class Vehicle {
    public Percentage getPercentFuelRemaining() { ... }
}
```

Test: agar maydon turini o'zgartirsangiz (`double` → `Money`), nechta chaqiruvchi buziladi? Javob "hammasi" bo'lsa, inkapsulyatsiya yo'q.

## 14.2 Obyekt va ma'lumot tuzilmasining teskariligi

Ikki yondashuv bir-biriga teskari va ikkisi ham o'z o'rnida to'g'ri. **Obyekt** ma'lumotini yashiradi va xatti-harakat taklif qiladi: yangi tur qo'shish oson (mavjud kodga tegmaysiz), yangi funksiya qo'shish qiyin (barcha turlarni o'zgartirasiz). **Ma'lumot tuzilmasi** ma'lumotini oshkor qiladi va xatti-harakati yo'q: yangi funksiya qo'shish oson, yangi tur qo'shish qiyin.

| Ehtiyoj | To'g'ri tanlov |
|---|---|
| Yangi tur tez-tez qo'shiladi | obyekt (polimorfizm) |
| Yangi amal tez-tez qo'shiladi | ma'lumot tuzilmasi + `switch` yoki visitor |
| Domen qoidasi bor | obyekt |
| Faqat ma'lumot tashiydi | `record` (DTO) |
| Tashqi shakl (JSON, jadval) | `record` yoki entitet |
| Hisob va siyosat | obyekt |

Eng ko'p xato - ikkisini aralashtirish, ya'ni gibrid yaratish (14.3).

## 14.3 Gibrid tuzilma: yarim obyekt, yarim struktura

Gibrid - getter va setter lari bor, lekin ichida biznes mantiqi ham bor sinf. U ikki dunyoning kamchiligini oladi: yangi tur qo'shish ham, yangi funksiya qo'shish ham qiyin.

```java
// yomon: gibrid - holat oshkor, lekin mantiq ham ichida
public class Order {
    private List<OrderItem> items;
    private BigDecimal total;

    public List<OrderItem> getItems() { return items; }      // ichki holat oshkor
    public void setTotal(BigDecimal total) { this.total = total; }
    public BigDecimal calculateTotal() { ... }               // mantiq ham shu yerda
}

// yaxshi: obyekt - holat yashirin, xatti-harakat oshkor
public final class Order {
    private final List<OrderItem> items;
    private Money total;

    public void addItem(Sku sku, Quantity quantity, Money unitPrice) {
        requireNotConfirmed();
        items.add(new OrderItem(sku, quantity, unitPrice));
        total = recalculateTotal();
    }

    public List<OrderItem> items() { return List.copyOf(items); }   // himoyalangan nusxa
    public Money total() { return total; }
}
```

## 14.4 Poyezd avariyasi va tuzilmani yashirish

`a.getB().getC().doSomething()` shaklidagi zanjir - poyezd avariyasi (train wreck) va u Demeter qonunini buzadi ([patternlar hujjatidagi](../patterns/README.md) Demeter qonuni). Clean code darajasidagi muhim nuqta: muammo zanjirning uzunligida emas, **kim nimani bilishi kerakligida**.

```java
// yomon: chaqiruvchi uch darajali tuzilmani biladi
String city = order.getCustomer().getAddress().getCity();

// yaxshi (obyekt bo'lsa): so'rash emas, aytish
order.shipTo(shipmentService);

// yaxshi (ma'lumot tuzilmasi bo'lsa): zanjir muammo emas
// record da getter yo'q, maydonga kirish normal
String city = orderDto.customer().address().city();
```

Shuning uchun qoida shunday: **obyekt** da zanjir hid, **ma'lumot tuzilmasi** da zanjir normal.

## 14.5 DTO, Active Record va ularning o'rni

DTO (`record`) - sof ma'lumot tuzilmasi: maydonlar, mantiq yo'q. U tashqi chegarada (HTTP, Kafka, fayl) to'g'ri tanlov va unga biznes qoidasini qo'shish xato.

Active Record - DTO ustiga `save`, `find` metodlari qo'shilgan shakl (JPA entiteti ko'pincha shunday ishlatiladi). U kichik CRUD da ishlaydi, lekin biznes qoidalari ko'payganda gibridga aylanadi. Qoida: Active Record ga biznes qoidasi qo'shila boshlasa, domen obyektini ajratish vaqti keldi.

## 14.6 Maydon ko'rinishi: `public` maydon, `package-private`, `final`

Ko'rinish darajasi eng arzon inkapsulyatsiya vositasi va u ko'pincha ishlatilmaydi. Amaliy tartib: hamma narsa eng kichik ko'rinish bilan boshlanadi va faqat ehtiyoj paydo bo'lganda kengaytiriladi.

| Element | Standart ko'rinish |
|---|---|
| Instans maydoni | `private final` |
| Konstanta | `private static final` (tashqariga kerak bo'lsa `public`) |
| Yordamchi metod | `private` |
| Sinf ichidagi API | `package-private` |
| Modul tashqarisidagi API | `public` |
| Test uchun ochilgan metod | `package-private` (`public` emas) |
| `record` komponenti | avtomatik `private final` |
| JPA entitet maydoni | `private` (Hibernate refleksiya bilan o'qiydi) |

`public` maydon faqat bir holatda haqli: `record` ichidagi komponentlar (ular allaqachon `final` va getter avtomatik).

Shu qoidaning chegarasi muhim va u ko'pincha o'tkazib yuboriladi: qoida maydonga emas, **sinfning o'z ko'rinishiga** bog'liq. `public` sinfda maydon oshkor qilinsa, u API ga chiqadi: ichki tasvir shartnomaga aylanadi, uni keyin almashtirib bo'lmaydi va invariantni himoya qilish uchun joy qolmaydi. `package-private` sinfning yoki `private` ichki sinfning maydonini oshkor qilishda esa yomon narsa yo'q, agar maydonlar abstraksiyani yetarli tasvirlasa. Sabab mexanik: bunday sinfning hamma mijozi paket (yoki tashqi sinf) ichida, demak maydon o'zgarsa ta'sir shu paket yoki shu fayl bilan chegaralanadi va accessor yozish faqat shovqin qo'shadi. Ikki yo'lni ajratadigan savol bitta: **maydon o'zgarsa, nechta joy qayta yoziladi**.

| Sinf ko'rinishi | Maydonga nima qilinadi |
|---|---|
| `public` sinf | maydon `private`, tashqariga accessor |
| `record` | komponent: avtomatik `private final` va accessor |
| `package-private` sinf | maydonni oshkor qilish mumkin, agar u abstraksiyani tasvirlasa |
| `private` ichki sinf (holat tashuvchi) | maydonni oshkor qilish mumkin, ko'pincha eng toza shakl |

```java
// yaxshi: private ichki sinf - accessor shovqin qo'shadi, maydon oshkor
public final class SettlementLedger {

    private static final class Entry {
        final SettlementRow row;       // oshkor: faqat shu fayl ko'radi
        final Instant recordedAt;

        Entry(SettlementRow row, Instant recordedAt) {
            this.row = row;
            this.recordedAt = recordedAt;
        }
    }
}
```

## 14.7 Ichki to'plamni oshkor qilish va himoyalangan nusxa

Eng ko'p uchraydigan yashirin inkapsulyatsiya buzilishi: getter ichki `List` ni to'g'ridan-to'g'ri qaytaradi va chaqiruvchi uni o'zgartiradi. Obyekt invarianti buziladi va buzilish joyi stack trace da ko'rinmaydi.

```java
// yomon: tashqi kod ichki ro'yxatni o'zgartira oladi
public List<OrderItem> getItems() { return items; }
order.getItems().clear();      // invariant buzildi, Order bilmaydi

// yaxshi: o'zgartirilmas nusxa
public List<OrderItem> items() { return List.copyOf(items); }

// yaxshi: o'zgartirilmas ko'rinish (nusxa qilmaydi, lekin yozishni to'sadi)
public List<OrderItem> items() { return Collections.unmodifiableList(items); }
```

Nusxa olish keraksiz obyekt yaratadi va shuning uchun "ishlash" dalili bilan tashlanadi. Lekin ikki xatoning narxi teng emas va qarorni shu farq hal qiladi: nusxa olmaslik xatoga va **xavfsizlik tuynugiga** olib keladi, keraksiz obyekt yaratish esa faqat uslub va tezlikka tegadi. Birinchisini tuzatish uchun xato chiqishini kutish kerak, ikkinchisini esa profiler ko'rsatganda tuzatish mumkin. Shuning uchun shubha bo'lsa nusxa olinadi.

Xuddi shu qoida konstruktorga tegishli: tashqaridan kelgan to'plamni nusxa qilmasdan saqlash chaqiruvchiga ichki holatni o'zgartirish imkonini qoldiradi.

```java
public Order(List<OrderItem> items) {
    this.items = new ArrayList<>(items);   // himoyalangan nusxa, kirishda
}
```

Konstruktorda nusxa olish **tartibi** ham qoida: nusxa tekshiruvdan OLDIN olinadi va tekshiruv nusxa ustida bajariladi. Teskari tartibda tekshiruv va saqlash orasida oyna qoladi: boshqa thread (yoki niyati buzuq chaqiruvchi) shu oynada obyektni o'zgartirib, tekshiruvdan o'tgan, lekin yaroqsiz holatni saqlab qo'yadi. Xavfsizlikda bu TOCTOU (time-of-check/time-of-use) deb ataladi.

```java
// yomon: tekshiruv asl obyekt ustida, keyin nusxa olinadi
final class DateRangeYomon {
    private final Date start;
    private final Date end;

    DateRangeYomon(Date start, Date end) {
        if (start.after(end)) { throw new IllegalArgumentException(); }
        this.start = new Date(start.getTime());   // orada start o'zgargan bo'lishi mumkin
        this.end = new Date(end.getTime());
    }
}

// yaxshi: avval nusxa, keyin nusxa ustida tekshiruv
final class DateRange {
    private final Date start;
    private final Date end;

    DateRange(Date start, Date end) {
        this.start = new Date(start.getTime());
        this.end = new Date(end.getTime());
        if (this.start.after(this.end)) { throw new IllegalArgumentException(); }
    }
}
```

Nusxani qanday olish ham ahamiyatli: parametr turi voris olinishi mumkin bo'lsa, nusxa `clone` bilan olinmaydi. `Date` `final` emas, demak `clone` `java.util.Date` nusxasini qaytarishi kafolatlanmagan: u ishonchsiz voris sinf nusxasini qaytarib, o'ziga havolani chetga yozib qo'yishi mumkin. Getterda esa `clone` haqli, chunki u yerda ichki obyektning aniq turi ma'lum; shunda ham nusxa konstruktori yoki statik fabrika afzal.

Nusxa olish kerak bo'lgan turlarning ro'yxati ko'rinishdan kengroq: `final` bo'lmagan **har qanday** tur o'zgaradigan voris sinfga ega bo'lishi mumkin. `BigInteger` va `BigDecimal` shu toifaga kiradi: ikkisi ham `final` emas, demak ularning metodlari override qilinishi mumkin va "o'zgarmas" degan taxmin kafolat emas. Shuning uchun xavfsizligi argumentning o'zgarmasligiga bog'liq kod ikki yo'ldan birini tanlaydi: argument haqiqatan shu sinfdan ekanini tekshirish (`arg.getClass() == BigInteger.class`), yoki argumentni himoyalangan nusxa qilish (`new BigInteger(arg.toByteArray())`). Ishonchsiz manbadan kelgan qiymat uchun bu majburiy ([code-review hujjatidagi](../code-review/README.md) xavfsizlik review i).

Nusxa olish narxi hamisha haqli ham emas, va uni tashlashning yagona qonuniy sharti **ishonch**: chaqiruvchi va sinf bir xil paket ichida bo'lsa yoki chaqiruvchining kodini siz nazorat qilsangiz, nusxa tashlanishi mumkin. Lekin unda shart qo'shiladi: hujjatda chaqiruvchi parametrni uzatgandan keyin uni o'zgartirmasligi **aniq yozilishi** kerak. Yozilmagan taxmin keyingi dasturchida yo'qoladi va xato ikki yil keyin, boshqa paketdan chaqirilganda chiqadi.

`Date`, massiv va `Calendar` kabi o'zgaradigan turlar ham shu qoidaga kiradi (22.1 da `Date` dan voz kechish sababi).

## 14.8 Statik holat, utility sinf va `private` konstruktor

Statik metodlar to'plami (utility sinf) sof funksiyalar uchun to'g'ri: `StringUtils.capitalize`. Ikki shart bor: sinf `final` va konstruktori `private` (instantiate qilib bo'lmaydi), va ichida **statik holat yo'q**.

```java
// yaxshi: haqiqiy utility
public final class Ibans {

    private Ibans() { throw new AssertionError("instantiate qilinmaydi"); }

    public static boolean isValid(String iban) { ... }
}

// yomon: statik o'zgaradigan holat - thread xavfi va test izolyatsiyasining buzilishi
public final class Counters {
    public static int processed;          // har bir test oldingisiga ta'sir qiladi
}
```

`private` konstruktor tanlovining sababi ham aniq. Sinfni `abstract` qilish instantiate qilishni **to'smaydi**: voris sinf yozib, uning nusxasi yaratiladi. Bundan tashqari `abstract` noto'g'ri signal beradi, ya'ni sinf vorislik uchun mo'ljallangandek ko'rinadi (17.1). `private` konstruktor esa ikki ishni birga bajaradi: nusxa yaratilmaydi, va yon ta'sir sifatida sinf voris olinmaydi ham, chunki voris chaqiradigan oshkor superclass konstruktori yo'q. Tanadagi `throw new AssertionError(...)` esa sinf ichidan tasodifan chaqirishni ham to'sadi.

Statik holat qachon haqli: `static final` konstantalar, `Logger`, va `Pattern` kabi thread-safe o'zgarmas obyektlar (21.6).

## 14.9 Obyekt o'z invariantini qanday himoya qiladi

Invariant - obyekt hayoti davomida har doim to'g'ri bo'lishi kerak bo'lgan shart. Uni himoya qilish uchun uch nuqta yopiladi: konstruktor (yaratishda), har bir o'zgartiruvchi metod (o'zgarishda), va seriyalash/deseriyalash (tashqi yo'ldan).

```java
public final class DateRange {

    private final LocalDate fromInclusive;
    private final LocalDate toExclusive;

    public DateRange(LocalDate fromInclusive, LocalDate toExclusive) {
        // Invariant konstruktorda: yaroqsiz obyekt umuman tug'ilmaydi
        if (!fromInclusive.isBefore(toExclusive)) {
            throw new IllegalArgumentException(
                    "boshlanish tugashdan oldin bo'lishi kerak: %s..%s"
                            .formatted(fromInclusive, toExclusive));
        }
        this.fromInclusive = fromInclusive;
        this.toExclusive = toExclusive;
    }

    // O'zgartirish yo'q: har bir amal yangi obyekt qaytaradi (16.4)
    public DateRange extendTo(LocalDate newEnd) {
        return new DateRange(fromInclusive, newEnd);
    }
}
```

Invariant bir nechta maydonni **bog'lab** turgan bo'lsa (masalan `x` va `y` juftligi, yoki `from`/`to` oralig'i), himoya o'qish tomoniga ham kerak bo'ladi. Bog'liq qiymatlar uchun alohida getter berilmaydi: ular bitta chaqiruvda birga qaytariladi. Alohida getter berilsa, chaqiruvchi `x` ni o'qib, keyin `y` ni o'qiydi va orada boshqa thread ikkisini ham yangilab qo'yishi mumkin: natijada chaqiruvchi obyekt hech qachon bo'lmagan juftlikni ko'radi. Ya'ni invariant atomar **yozilishi** kerak bo'lsa, u atomar **o'qilishi** ham kerak.

```java
// yomon: ikki getter - chaqiruvchi mos kelmagan juftlikni ko'radi
public synchronized int x() { return x; }
public synchronized int y() { return y; }

// yaxshi: juftlik bitta chaqiruvda, bitta o'qishda
public synchronized Point location() { return new Point(x, y); }

public synchronized void moveTo(int x, int y) {   // yozish ham atomar
    this.x = x;
    this.y = y;
}
```

O'zgarmas tur bilan bu muammo umuman tug'ilmaydi: `record Point(int x, int y)` juftlikni bitta havolaga bog'laydi va atomar o'qish bepul keladi. Shuning uchun birinchi yechim o'zgarmaslik, `synchronized` juft getter esa faqat o'zgaradigan obyekt majburiy bo'lganda ([arxitektor hujjatidagi](../architect/11-concurrency-thread-lock-atomic-happens.md#113-umumiy-holat-shared-state-muammosi-poyga-sharti-va-korinuvchanlik) umumiy holat muammosi).

Qoida: "yaroqsiz obyekt yaratib bo'lmaydi" tamoyili validatsiyani butun kod bazasidan bir joyga yig'adi.

## 14.10 `this` ning konstruktordan qochib ketishi

Konstruktor tugamasdan obyekt havolasini tashqariga berish yarim qurilgan obyektni oshkor qiladi: maydonlar hali tayinlanmagan, invariant hali tekshirilmagan. Bu xato `final` maydonlar kafolatini ham buzadi.

```java
// yomon: this konstruktordan chiqib ketdi
public class PaymentListener {
    public PaymentListener(EventBus bus) {
        bus.register(this);        // bus boshqa thread'dan darhol chaqirishi mumkin
        this.retryPolicy = new RetryPolicy();   // hali tayinlanmagan!
    }
}

// yaxshi: ro'yxatdan o'tish konstruktordan tashqarida
public final class PaymentListener {

    private final RetryPolicy retryPolicy;

    private PaymentListener(RetryPolicy retryPolicy) { this.retryPolicy = retryPolicy; }

    public static PaymentListener registeredOn(EventBus bus) {
        PaymentListener listener = new PaymentListener(new RetryPolicy());
        bus.register(listener);    // obyekt to'liq qurilgandan keyin
        return listener;
    }
}
```

Spring kontekstida bu qoida `@PostConstruct` yoki `ApplicationReadyEvent` da ro'yxatdan o'tish shaklida qo'llanadi (26.1).

## 14.11 Chegara interfeysini tizim bo'ylab uzatmaslik

`Map`, `JsonNode`, `ResultSet` va kutubxona turlari keng: ularda sizga kerak bo'lmagan metodlar ham bor. Shu turni tizim bo'ylab uzatsangiz, har bir qabul qiluvchi uning hamma imkoniyatini oladi, shu bilan birga kutubxona imzosi o'zgarganda tuzatiladigan joy soni ham shuncha bo'ladi. Qoida: chegara turi uni ishlatadigan sinf ichida qoladi, `public` API dan qaytarilmaydi va argument sifatida qabul qilinmaydi.

```java
// yomon: Map butun tizim bo'ylab yuradi, har kim clear() chaqira oladi
Map<String, Sensor> sensors = new HashMap<>();
registry.register(sensors);

// yaxshi: chegara turi sinf ichida, tashqariga kerakli uchta metod chiqadi
public final class Sensors {

    private final Map<String, Sensor> bySerial = new HashMap<>();

    public Sensor byId(String id) {
        Sensor sensor = bySerial.get(id);
        if (sensor == null) {
            throw new UnknownSensorException(id);
        }
        return sensor;
    }
}
```

Bu o'ramning ikkinchi foydasi: `Sensors` endi biznes qoidasini majburlashi mumkin (noma'lum id da istisno, qo'shishda tekshiruv), `Map` esa buni qila olmaydi. Har bir `Map` ni o'rash shart emas, lekin chegara turi bir sinf yoki yaqin sinflar guruhidan chiqmasligi shart. To'plamni qaytarish shakli alohida mavzu: [ichki to'plamni oshkor qilish](#147-ichki-toplamni-oshkor-qilish-va-himoyalangan-nusxa).

## 14.12 Hali yozilmagan API o'rniga o'zing xohlagan interfeysni yozish

Chegaraning ikkinchi turi bilim bilan noma'lumlikni ajratadi: qo'shni jamoa interfeysini hali belgilamagan, tashqi servis shartnomasi hali tayyor emas. Kutib turish o'rniga o'zingiz xohlagan interfeysni yozasiz: nomi va metodlari sizning kodingiz ehtiyojidan chiqadi, chaqiruvchi tomon shu nom bilan o'qiladi.

```java
// bizning ehtiyojimizdan chiqqan interfeys, tashqi API hali yo'q
public interface Transmitter {
    void transmit(Frequency frequency, DataStream stream);
}

// tashqi API kelganda faqat bitta sinf o'zgaradi
final class VendorTransmitterAdapter implements Transmitter {

    private final VendorRadioApi api;

    @Override
    public void transmit(Frequency frequency, DataStream stream) {
        api.keyOn(frequency.hertz());       // vendor imzosi shu sinfda qoladi
        api.emitAnalog(stream.bytes());
    }
}
```

Shu bilan tashqi API bilan ishlash bitta sinfga to'planadi va test uchun tikuv (seam) paydo bo'ladi: `Transmitter` ning fake implementatsiyasi bilan chaqiruvchini tashqi tizimsiz sinash mumkin. Adapter patternining to'liq yozuvi [Adapter](../patterns/02-strukturaviy-patternlar.md#21-adapter-adapter) da.

## 14.13 Amalda qo'llash

- [ ] Barcha getter lari to'plam qaytaradigan sinflarni topib, `List.copyOf` yoki o'zgartirilmas ko'rinishga o'tkazing.
- [ ] Konstruktorda tashqaridan kelgan to'plam va massivlarni nusxa qilib saqlashni ta'minlang.
- [ ] Setter lari va biznes mantiqi birga turgan gibrid sinflarni ro'yxatlab, holatni yashirishga o'tkazing.
- [ ] Barcha maydonlarni `private final` qilib, faqat zarur joyda ko'rinishni kengaytiring.
- [ ] Utility sinflarini `final` va `private` konstruktor bilan yoping; statik o'zgaradigan holatni yo'qoting.
- [ ] Value object larda invariantni konstruktorga ko'chirib, tarqalgan validatsiyani olib tashlang.
- [ ] Konstruktorda `this` ni tashqariga beradigan joylarni statik fabrikaga yoki `@PostConstruct` ga ko'chiring.
- [ ] Har bir DTO da biznes mantiqi yo'qligini, har bir domen obyektida esa oshkor setter yo'qligini tekshiring.
- [ ] `public` metod imzolarida `Map`, `JsonNode` va kutubxona turlarini qidirib, ularni o'z turingiz bilan almashtiring.
- [ ] Tashqi API ga to'g'ridan-to'g'ri murojaat qiladigan sinflarni sanab, ularni bitta adapter ortiga yig'ing.

## Manbalar

- Joshua Bloch, *Effective Java* 3rd, Item 4 (19-bet) - sinfni `abstract` qilish instantiate qilishni to'smasligi va vorislik uchun mo'ljallangan degan noto'g'ri signal berishi; `private` konstruktorning yon ta'sir sifatida sinfni voris olishdan ham to'sishi
- Joshua Bloch, *Effective Java* 3rd, Item 6 (25-bet) - nusxa olmaslikning jazosi (xato va xavfsizlik tuynugi) keraksiz obyekt yaratishning jazosidan (uslub va ishlash) katta bo'lishi
- Joshua Bloch, *Effective Java* 3rd, Item 16 (78-bet) - `package-private` sinf yoki `private` ichki sinf maydonini oshkor qilishda yomon narsa yo'qligi, agar maydonlar abstraksiyani yetarli tasvirlasa
- ESLATMA: `public` maydon faqat `record` da haqli degan qoida bilan Bloch ning `package-private` istisnosi qarama-qarshi ko'rinadi. Ikkisini ajratuvchi shart (maydon ko'rinishi SINFNING o'z ko'rinishiga bog'liq: `public` API da accessor, paket ichida qolgan yoki `private` ichki sinfda maydon) va uning jadvali korpus qo'shimchasi, kitobda shu shaklda yo'q
- Joshua Bloch, *Effective Java* 3rd, Item 17 (85-bet) - `BigInteger` va `BigDecimal` ning `final` emasligi, metodlari override qilinishi va ishonchsiz voris sinf uchun tur tekshiruvi yoki himoyalangan nusxa talabi
- Joshua Bloch, *Effective Java* 3rd, Item 50 (234-bet) - nusxa olish narxini chaqiruvchiga ishonib tashlash sharti va bu holda hujjatda chaqiruvchi parametrni o'zgartirmasligini aniq yozish talabi
- Brian Goetz va boshqalar, *Java Concurrency in Practice*, Addison-Wesley, 2006, 4-bob (46-bet) - bir-biriga bog'liq ikki qiymat uchun alohida getter berilmasligi va ularning bitta chaqiruvda birga qaytarilishi

- Robert C. Martin, *Clean Code*, 6-bob - obyekt va ma'lumot tuzilmasi teskariligi, Demeter qonuni, DTO va Active Record
- Robert C. Martin, *Clean Code*, 8-bob - chegara turini tizim bo'ylab uzatmaslik va hali yozilmagan API uchun interfeys
- Joshua Bloch, *Effective Java* 3rd, Item 15, 16, 17 - a'zolar ko'rinishini kamaytirish, accessor metod, o'zgarmaslik
- Joshua Bloch, *Effective Java* 3rd, Item 50 - kerak bo'lganda himoyalangan nusxa olish
- Joshua Bloch, *Effective Java* 3rd, Item 50 - nusxa tekshiruvdan oldin olinishi (TOCTOU), voris olinadigan turda `clone` bilan nusxa olmaslik
- Robert C. Martin, *Clean Code*, 6-bob ("The Law of Demeter", "Hiding Structure") - poyezd avariyasi va tuzilmani yashirish

---

[&larr; 13. Formatlashni avtomatlashtirish va diff gigiyenasi](13-formatlashni-avtomatlashtirish-va-diff.md) · [Mundarija](README.md) · [15. Tenglik, hash va obyekt shartnomalari &rarr;](15-tenglik-hash-va-obyekt-shartnomalari.md)
