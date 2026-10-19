<!-- doc: clean-code | chapter: 16 | part: V. Obyekt, ma'lumot va holat -->

[Barcha hujjatlar](../../README.md) / [Toza kod qoidalari](README.md)

> Holat: tekshirilgan (2026-10-19). Manbalar bob oxirida.

# 16. O'zgarmaslik va holat boshqaruvi kod darajasida (Immutability in Code)

<details>
<summary>Bu bobdagi 10 bo'lim</summary>

- [16.1 `final` maydon, `final` sinf va haqiqiy o'zgarmaslik](#161-final-maydon-final-sinf-va-haqiqiy-ozgarmaslik)
- [16.2 Chuqur va sayoz o'zgarmaslik](#162-chuqur-va-sayoz-ozgarmaslik)
- [16.3 O'zgarmas to'plamlar: `List.of`, `unmodifiable*`, nusxa](#163-ozgarmas-toplamlar-listof-unmodifiable-nusxa)
- [16.4 `with` uslubidagi o'zgartiruvchilar](#164-with-uslubidagi-ozgartiruvchilar)
- [16.5 Builder: validatsiya va majburiy maydonlar](#165-builder-validatsiya-va-majburiy-maydonlar)
- [16.6 Mutatsiyani bir joyga to'plash](#166-mutatsiyani-bir-joyga-toplash)
- [16.7 Setter ni olib tashlash yo'li](#167-setter-ni-olib-tashlash-yoli)
- [16.8 Vaqtinchalik maydon va uni yo'qotish](#168-vaqtinchalik-maydon-va-uni-yoqotish)
- [16.9 Global va statik o'zgaradigan holat](#169-global-va-statik-ozgaradigan-holat)
- [16.10 Amalda qo'llash](#1610-amalda-qollash)

</details>


Holatni kamaytirish murakkablikni boshqarish vositasi sifatida [arxitektor hujjatidagi](../architect/README.md) holatni kamaytirish bo'limida ko'rib chiqilgan. Bu bobda shu qarorning kod darajasidagi mexanikasi: `final` ning haqiqiy kuchi, chuqur va sayoz o'zgarmaslik, o'zgarmas to'plamlar, nusxalab o'zgartirish, va setter larni yo'qotish yo'li.

## 16.1 `final` maydon, `final` sinf va haqiqiy o'zgarmaslik

`final` maydon faqat **havolani** qotiradi, obyektni emas. `private final List<Order> orders` maydoniga yangi ro'yxat tayinlab bo'lmaydi, lekin `orders.add(...)` ishlaydi. Shu sababli haqiqiy o'zgarmaslik beshta shartni talab qiladi, va ularning har biri boshqa teshikni yopadi.

| Shart | Nega kerak |
|---|---|
| Holatni o'zgartiradigan metod yo'q | setter va `addX` o'zgartirish yo'lini ochadi |
| Sinf voris olinmaydi: `final`, yoki konstruktor `private` va statik fabrika | voris sinf o'zini o'zgarganday tutishi mumkin |
| Barcha maydonlar `final` | qayta tayinlashni to'sadi; thread ga sinxronlashsiz uzatishda to'g'ri ko'rinishni ham kafolatlaydi |
| Barcha maydonlar `private` | mijoz maydondagi o'zgaradigan obyektga to'g'ridan-to'g'ri yetib bormaydi va ichki tuzilishni keyin almashtirish mumkin bo'ladi |
| O'zgaradigan komponentga yakka kirish | konstruktorda va getterda nusxa olinadi ([himoyalangan nusxa](14-obyekt-va-malumot-tuzilmasi-inkapsulyatsiya.md#147-ichki-toplamni-oshkor-qilish-va-himoyalangan-nusxa)) |

Ikki qo'shimcha shart Java ga xos: maydon turlarining o'zi ham o'zgarmas bo'lishi (16.2) va `this` ning konstruktordan [chiqib ketmasligi](14-obyekt-va-malumot-tuzilmasi-inkapsulyatsiya.md#1410-this-ning-konstruktordan-qochib-ketishi).

```java
// yomon: final bor, lekin obyekt o'zgaradi
public final class Order {
    private final List<OrderItem> items = new ArrayList<>();
    public List<OrderItem> items() { return items; }   // tashqi kod add qiladi
}

// yaxshi: haqiqiy o'zgarmaslik
public final class Order {

    private final List<OrderItem> items;

    public Order(List<OrderItem> items) {
        this.items = List.copyOf(items);     // nusxa + o'zgartirilmas
    }

    public List<OrderItem> items() { return items; }   // o'zgartirilmas, nusxa kerak emas
}
```

**Enum maydonlari ham `final` bo'ladi.** Enum konstantasining maydonini yaratilgandan keyin o'zgartirish Java da qonuniy: `enum` tanasida oddiy maydon e'lon qilib, unga setter yozish kompilyatsiya qilinadi. Lekin bu tavsiya etilmaydi, chunki enum maydoni semantik jihatdan oddiy maydondan boshqacha ishlaydi: **har bir konstantaning o'z nusxasi bor**, ya'ni setter chaqiruvi faqat shu konstantaning qiymatini o'zgartiradi va qolganlari o'z qiymatini saqlaydi. Natijada enum global, bir martalik yuklanadigan va hamma joyda ulashiladigan obyekt bo'lgani uchun o'zgarish butun JVM bo'ylab ko'rinadi va uni kim o'zgartirganini topish qiyin.

```java
// yomon: enum maydoni o'zgaruvchan, o'zgarish global ko'rinadi
enum Bird {
    CHICKEN(20), PENGUIN(75);

    private int numDays;
    Bird(int numDays) { this.numDays = numDays; }
    void setNumDays(int numDays) { this.numDays = numDays; }   // qonuniy, lekin yo'q
}

// yaxshi: maydon final, hisob-kitob metodda
enum Bird {
    CHICKEN(20), PENGUIN(75);

    private final int incubationDays;
    Bird(int incubationDays) { this.incubationDays = incubationDays; }
    int incubationDays() { return incubationDays; }
}
```

## 16.2 Chuqur va sayoz o'zgarmaslik

Sayoz o'zgarmaslik - obyektning o'zi o'zgarmas, lekin ichidagi obyektlar o'zgaradi. Bu holat eng xavfli, chunki kod o'zgarmas ko'rinadi va dasturchi himoyaga ishonadi.

```java
// yomon: record o'zgarmas ko'rinadi, lekin ichidagi Date o'zgaradi
public record Shipment(String trackingNumber, Date dispatchedAt) { }
shipment.dispatchedAt().setTime(0);    // o'zgardi!

// yaxshi: ichki turlar ham o'zgarmas
public record Shipment(TrackingNumber trackingNumber, Instant dispatchedAt) { }
```

Qoida: o'zgarmas sinf ichida faqat o'zgarmas turlar bo'lishi kerak - `String`, `Instant`, `LocalDate`, `BigDecimal`, `record`, enum, `List.of`. `Date`, `Calendar`, massiv, `ArrayList` esa chegarada nusxalanadi.

Chuqur o'zgarmaslikning qaytim tomoni ham bor va u optimallashtirish imkoni beradi: **o'zgarmas obyektlar ichki tuzilmasini bir-biri bilan erkin ulashishi mumkin**. Ichki tuzilma hech qachon o'zgarmagani uchun ulashish hech qanday xavf tug'dirmaydi va nusxa olish keraksiz bo'lib qoladi. Platformadagi namuna: `BigInteger.negate()` yangi obyekt qaytaradi, lekin kattalikni saqlaydigan ichki massivni nusxalamaydi, faqat ishorani almashtiradi. O'z o'zgarmas sinfingizda ham shu yo'ldan borish mumkin, bitta shart bilan: ulashiladigan tuzilma ham chindan o'zgarmas bo'lishi kerak (`List.of`, `record`, primitiv massiv faqat ichkarida qolsa), aks holda optimallashtirish sayoz o'zgarmaslikka aylanadi.

## 16.3 O'zgarmas to'plamlar: `List.of`, `unmodifiable*`, nusxa

Java da to'plam o'zgarmasligining uch darajasi bor va ularni ajratish muhim.

| Shakl | Xatti-harakat | `null` element |
|---|---|---|
| `List.of(a, b)` | haqiqiy o'zgarmas, yangi obyekt | taqiqlangan |
| `List.copyOf(src)` | manbadan nusxa, o'zgarmas | taqiqlangan |
| `Collections.unmodifiableList(src)` | **ko'rinish**: manba o'zgarsa o'zgaradi | ruxsat |
| `new ArrayList<>(src)` | nusxa, lekin o'zgaradi | ruxsat |
| `Arrays.asList(a, b)` | fiksirlangan hajm, `set` ishlaydi | ruxsat |
| `stream().toList()` | o'zgarmas | ruxsat |
| `Collectors.toList()` | kafolat yo'q | ruxsat |

Eng ko'p uchraydigan tuzoq - `Collections.unmodifiableList` ni haqiqiy o'zgarmaslik deb o'ylash: u faqat **ko'rinish** beradi va manba o'zgarsa ko'rinish ham o'zgaradi.

```java
List<String> source = new ArrayList<>(List.of("a"));
List<String> view = Collections.unmodifiableList(source);
source.add("b");
view.size();   // 2 - "o'zgarmas" ko'rinish o'zgardi
```

## 16.4 `with` uslubidagi o'zgartiruvchilar

O'zgarmas obyektni "o'zgartirish" - yangi nusxa qaytarish. Konvensiya: metod nomi `with`, `plus`, `minus` yoki domen fe'li bilan boshlanadi va `this` ni o'zgartirmaydi.

```java
public record Money(BigDecimal amount, Currency currency) {

    public Money plus(Money other) {
        requireSameCurrency(other);
        return new Money(amount.add(other.amount), currency);
    }

    public Money withScale(int scale) {
        return new Money(amount.setScale(scale, RoundingMode.HALF_UP), currency);
    }
}

// Domen obyektida: har bir o'tish yangi holat qaytaradi
public record Order(OrderId id, OrderStatus status, List<OrderItem> items) {

    public Order confirmed() {
        if (status != DRAFT) throw new IllegalStateException("faqat DRAFT tasdiqlanadi");
        return new Order(id, CONFIRMED, items);
    }
}
```

Maydon soni ko'p bo'lsa, har bir `with` metodi uzun bo'lib ketadi; bunda builder dan nusxa olish (`toBuilder()`) ishlatiladi.

`with` uslubining ma'lum narxi bor: ko'p qadamli amal har qadamda yangi obyekt yaratadi va faqat oxirgisi saqlanadi, qolganlari darhol axlatga aylanadi. Qisqa zanjirda bu ahamiyatsiz, lekin siklda yoki uzun zanjirda sezilarli bo'ladi. Narxni yopishning ikki yo'li bor va tanlov amalning **oldindan bilinishiga** bog'liq. Agar eng ko'p kerak bo'ladigan ko'p qadamli amallarni oldindan sanab chiqish mumkin bo'lsa, ularning har biri sinfning primitiv amali qilib beriladi: `money.plus(a).plus(b).plus(c)` o'rniga `Money.sum(a, b, c)`, shunda oraliq obyekt umuman yaratilmaydi. Agar amallarni oldindan bilish mumkin bo'lmasa, o'zgarmas sinfga **o'zgaradigan hamroh sinf** (companion class) beriladi: platformadagi namuna `String` va `StringBuilder` juftligi (21.2). Hamroh sinf `public` bo'lishi shart emas: ko'pincha u sinf ichida qolib, faqat natijani qaytaradi.

```java
// yaxshi: oldindan bilinadigan amal primitiv sifatida berilgan
public static Money sum(Collection<Money> amounts) {
    BigDecimal total = BigDecimal.ZERO;          // oraliq Money yaratilmaydi
    for (Money each : amounts) { total = total.add(each.amount()); }
    return new Money(total, currencyOf(amounts));
}
```

## 16.5 Builder: validatsiya va majburiy maydonlar

Builder pattern ning o'zi [patternlar hujjatida](../patterns/README.md); bu yerda clean code tomoni: validatsiya **qayerda** turishi. Eng ko'p uchraydigan xato - validatsiyani builder metodlarida qilish va `build()` da unutish, natijada yarim to'ldirilgan obyekt yaratiladi.

```java
public final class ReservationRequest {

    private final CustomerId customer;
    private final Sku sku;
    private final Quantity quantity;

    private ReservationRequest(Builder builder) {
        // Validatsiya bir joyda: build() yo'li orqali
        this.customer = Objects.requireNonNull(builder.customer, "customer");
        this.sku = Objects.requireNonNull(builder.sku, "sku");
        this.quantity = Objects.requireNonNull(builder.quantity, "quantity");
        if (quantity.isZeroOrLess()) {
            throw new IllegalArgumentException("quantity musbat bo'lishi kerak: " + quantity);
        }
    }

    public static Builder builder() { return new Builder(); }

    public static final class Builder {
        private CustomerId customer;
        private Sku sku;
        private Quantity quantity;

        public Builder customer(CustomerId customer) { this.customer = customer; return this; }
        public Builder sku(Sku sku) { this.sku = sku; return this; }
        public Builder quantity(Quantity quantity) { this.quantity = quantity; return this; }

        public ReservationRequest build() { return new ReservationRequest(this); }
    }
}
```

Agar majburiy maydonlar kam bo'lsa, builder o'rniga konstruktor yoki `record` yaxshiroq: builder faqat ixtiyoriy maydonlar ko'p bo'lganda haqli.

## 16.6 Mutatsiyani bir joyga to'plash

Butun tizimni o'zgarmas qilish amalda mumkin emas: ma'lumotlar bazasi, kesh, hisoblagich o'zgaradi. To'g'ri strategiya - o'zgarishni **chegaraga** siqish: hisob va qoidalar o'zgarmas obyektlarda, o'zgarish esa bir-ikki aniq joyda.

```java
// yaxshi: hisob sof, o'zgarish bitta joyda
public final class SettlementBatch {

    // Sof hisob: kirish o'zgarmas, chiqish yangi obyekt
    public SettlementPlan planFor(List<Payment> payments) {
        return new SettlementPlan(payments.stream().filter(Payment::isSettleable).toList());
    }
}

@Service
class SettlementRunner {

    // O'zgarish faqat shu yerda: tranzaksiya chegarasida
    @Transactional
    void apply(SettlementPlan plan) {
        paymentRepository.markSettled(plan.paymentIds());
    }
}
```

## 16.7 Setter ni olib tashlash yo'li

Mavjud kod bazasida setter lar ko'p bo'lsa, ularni bir kunda olib tashlab bo'lmaydi. Ishlaydigan ketma-ketlik: setter ni domen fe'liga aylantirish, keyin o'zgarmas nusxaga o'tish.

```java
// 1-qadam: setter domen fe'liga aylanadi (ma'no paydo bo'ladi, imzo torayadi)
// oldin: order.setStatus(SHIPPED);
public void markShipped(Instant shippedAt) {
    if (status != CONFIRMED) throw new IllegalStateException(...);
    this.status = SHIPPED;
    this.shippedAt = shippedAt;
}

// 2-qadam: o'zgartirish yangi obyekt qaytaradi
public Order shipped(Instant shippedAt) { ... }

// 3-qadam: entitetda saqlanadigan holat uchun o'zgarish qoladi,
// lekin faqat domen fe'llari orqali: oshkor setter yo'q
```

## 16.8 Vaqtinchalik maydon va uni yo'qotish

Vaqtinchalik maydon (temporary field) - faqat ma'lum metod ishlaganda to'ldiriladigan, qolgan vaqt `null` turadigan maydon. U o'quvchini chalg'itadi: maydonni ko'rgan odam uning har doim to'ldirilganini o'ylaydi.

```java
// yomon: ikki maydon faqat calculate() ichida ishlatiladi
public class PriceCalculator {
    private Money subtotal;      // faqat calculate() davomida to'ldiriladi
    private Money discount;      // qolgan vaqt null

    public Money calculate(Order order) {
        subtotal = subtotalOf(order);
        discount = discountFor(order, subtotal);
        return subtotal.minus(discount);
    }
}

// yaxshi: vaqtinchalik holat metod ichida yoki alohida obyektda
public final class PriceCalculator {

    public Money calculate(Order order) {
        Money subtotal = subtotalOf(order);
        Money discount = discountFor(order, subtotal);
        return subtotal.minus(discount);
    }
}
```

## 16.9 Global va statik o'zgaradigan holat

Statik o'zgaradigan maydon uch muammoni bir vaqtda keltiradi: testlar bir-biriga ta'sir qiladi (tartibga bog'liq yiqilish), thread xavfi paydo bo'ladi, va bog'liqlik kodda ko'rinmaydi.

```java
// yomon: global holat
public class CurrentUser {
    public static String username;      // kim o'rnatdi, kim o'chirdi - ko'rinmaydi
}

// yaxshi: kontekst oshkor uzatiladi yoki framework mexanizmi ishlatiladi
public record RequestContext(UserId user, TraceId trace) { }
// yoki Spring Security: SecurityContextHolder (thread-local, framework boshqaradi)
```

`ThreadLocal` ham global holatning shakli va u faqat framework darajasida (MDC, tranzaksiya konteksti) haqli; biznes kodida uzatilgan parametr har doim afzal. Ishlatilsa, `finally` da tozalash majburiy (29.7).

## 16.10 Amalda qo'llash

- [ ] Barcha maydonlarni `final` qilib, qolganlarini (o'zgarishi kerak bo'lganlarini) ro'yxatlab sababini yozib qo'ying.
- [ ] O'zgarmas deb hisoblangan sinflar ichida `Date`, massiv va `ArrayList` borligini tekshirib, o'zgarmas turga almashtiring.
- [ ] `Collections.unmodifiableList` ishlatilgan joylarni `List.copyOf` ga o'tkazib, ko'rinish tuzog'ini yo'qoting.
- [ ] Domen obyektlaridagi oshkor setter larni domen fe'llariga aylantiring (16.7 dagi uch qadam).
- [ ] Faqat bir metod davomida to'ldiriladigan maydonlarni mahalliy o'zgaruvchiga ko'chiring.
- [ ] Statik o'zgaradigan maydonlarni topib (`static` + `final` emas), kontekst parametriga yoki framework mexanizmiga o'tkazing.
- [ ] `ThreadLocal` ishlatilgan joylarda `finally` da tozalash borligini tekshiring.
- [ ] Yangi value object lar uchun `record` ni standart tanlov qilib, uni jamoa kelishuviga yozib qo'ying.

## Manbalar

- Joshua Bloch, *Effective Java* 3rd, Item 17 (83-bet) - o'zgarmas obyektlarning ichki tuzilmasini bir-biri bilan ulashishi mumkinligi va `BigInteger.negate` ning massivni nusxalamasligi
- Joshua Bloch, *Effective Java* 3rd, Item 17 (84-bet) - ko'p qadamli amal narxini yopishning ikki yo'li: eng ko'p kerak bo'ladigan amallarni primitiv sifatida berish yoki o'zgaradigan hamroh sinf berish (`String` uchun `StringBuilder`)

- Boyarsky/Selikoff, *OCP Java SE 17 Developer Practice Tests*, 3-bob javoblari (106-savol) - enum maydonini yaratilgandan keyin o'zgartirish qonuniy, lekin tavsiya etilmasligi; har enum konstantasining maydon nusxasi alohida bo'lishi va setter faqat bittasini o'zgartirishi
- Joshua Bloch, *Effective Java* 3rd, Item 17 - o'zgarmas sinfning besh qoidasi, `final` maydonning xotira modeli bilan bog'liqligi
- Joshua Bloch, *Effective Java* 3rd, Item 15, 16 - a'zolar ko'rinishini kamaytirish, `public` maydon o'rniga accessor
- Joshua Bloch, *Effective Java* 3rd, Item 50 - o'zgaradigan komponentga himoyalangan nusxa
- Joshua Bloch, *Effective Java* 3rd, Item 2 - ko'p parametrli konstruktor o'rniga builder
- [Java API, `List.of`](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/List.html#of()) - `null` element taqiqlangan, o'zgarmas ro'yxat
- [Java API, `Collections.unmodifiableList`](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/Collections.html#unmodifiableList(java.util.List)) - o'zgartirilmas KO'RINISH, manba o'zgarsa o'zgaradi
- [Java API, `Stream.toList`](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/stream/Stream.html#toList()) - o'zgartirilmas, `null` ga ruxsat beradi

---

[&larr; 15. Tenglik, hash va obyekt shartnomalari](15-tenglik-hash-va-obyekt-shartnomalari.md) · [Mundarija](README.md) · [17. Vorislik, kompozitsiya va polimorfizm mexanikasi &rarr;](17-vorislik-kompozitsiya-va-polimorfizm.md)
