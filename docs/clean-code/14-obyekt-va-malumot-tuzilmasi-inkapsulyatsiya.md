<!-- doc: clean-code | chapter: 14 | part: V. Obyekt, ma'lumot va holat -->

[Barcha hujjatlar](../../README.md) / [Toza kod qoidalari](README.md)

# 14. Obyekt va ma'lumot tuzilmasi: inkapsulyatsiya (Objects vs Data Structures)

<details>
<summary>Bu bobdagi 11 bo'lim</summary>

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
- [14.11 Amalda qo'llash](#1411-amalda-qollash)

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

Xuddi shu qoida konstruktorga tegishli: tashqaridan kelgan to'plamni nusxa qilmasdan saqlash chaqiruvchiga ichki holatni o'zgartirish imkonini qoldiradi.

```java
public Order(List<OrderItem> items) {
    this.items = new ArrayList<>(items);   // himoyalangan nusxa, kirishda
}
```

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

## 14.11 Amalda qo'llash

- [ ] Barcha getter lari to'plam qaytaradigan sinflarni topib, `List.copyOf` yoki o'zgartirilmas ko'rinishga o'tkazing.
- [ ] Konstruktorda tashqaridan kelgan to'plam va massivlarni nusxa qilib saqlashni ta'minlang.
- [ ] Setter lari va biznes mantiqi birga turgan gibrid sinflarni ro'yxatlab, holatni yashirishga o'tkazing.
- [ ] Barcha maydonlarni `private final` qilib, faqat zarur joyda ko'rinishni kengaytiring.
- [ ] Utility sinflarini `final` va `private` konstruktor bilan yoping; statik o'zgaradigan holatni yo'qoting.
- [ ] Value object larda invariantni konstruktorga ko'chirib, tarqalgan validatsiyani olib tashlang.
- [ ] Konstruktorda `this` ni tashqariga beradigan joylarni statik fabrikaga yoki `@PostConstruct` ga ko'chiring.
- [ ] Har bir DTO da biznes mantiqi yo'qligini, har bir domen obyektida esa oshkor setter yo'qligini tekshiring.

---

[&larr; 13. Formatlashni avtomatlashtirish va diff gigiyenasi](13-formatlashni-avtomatlashtirish-va-diff.md) · [Mundarija](README.md) · [15. Tenglik, hash va obyekt shartnomalari &rarr;](15-tenglik-hash-va-obyekt-shartnomalari.md)
