<!-- doc: clean-code | chapter: 16 | part: V. Obyekt, ma'lumot va holat -->

[Toza kod yozuvchining qoidalari](../../README.md) / [Toza kod qoidalari](README.md)

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

`final` maydon faqat **havolani** qotiradi, obyektni emas. `private final List<Order> orders` maydoniga yangi ro'yxat tayinlab bo'lmaydi, lekin `orders.add(...)` ishlaydi. Shu sababli haqiqiy o'zgarmaslik uch shartni talab qiladi.

| Shart | Nega kerak |
|---|---|
| Barcha maydonlar `final` | qayta tayinlashni to'sadi |
| Maydon turlari ham o'zgarmas | ichki obyekt o'zgarmasin |
| Sinf `final` (yoki konstruktor `private`) | voris sinf o'zgaruvchanlik qo'shmasin |
| Setter yo'q | oshkor o'zgartirish yo'li yopiladi |
| To'plamlar nusxalanadi va o'zgartirilmas | 14.7 |
| `this` chiqib ketmaydi | 14.10 |

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

---

[&larr; 15. Tenglik, hash va obyekt shartnomalari](15-tenglik-hash-va-obyekt-shartnomalari.md) · [Mundarija](README.md) · [17. Vorislik, kompozitsiya va polimorfizm mexanikasi &rarr;](17-vorislik-kompozitsiya-va-polimorfizm.md)
