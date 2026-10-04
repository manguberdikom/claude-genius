<!-- doc: clean-code | chapter: 15 | part: V. Obyekt, ma'lumot va holat -->

[Toza kod yozuvchining qoidalari](../../README.md) / [Toza kod qoidalari](README.md)

# 15. Tenglik, hash va obyekt shartnomalari (Equality, Hashing and Object Contracts)

<details>
<summary>Bu bobdagi 11 bo'lim</summary>

- [15.1 `equals` shartnomasi: besh qoida](#151-equals-shartnomasi-besh-qoida)
- [15.2 `hashCode` shartnomasi va `equals` bilan bog'liqligi](#152-hashcode-shartnomasi-va-equals-bilan-bogliqligi)
- [15.3 `equals` ni yozish shabloni va `instanceof` pattern matching](#153-equals-ni-yozish-shabloni-va-instanceof-pattern-matching)
- [15.4 Vorislik ostida tenglik: `getClass()` yoki `instanceof`](#154-vorislik-ostida-tenglik-getclass-yoki-instanceof)
- [15.5 Entitet va value object tengligi farqi](#155-entitet-va-value-object-tengligi-farqi)
- [15.6 `compareTo` shartnomasi va `equals` bilan izchillik](#156-compareto-shartnomasi-va-equals-bilan-izchillik)
- [15.7 `toString`: foydali, xavfsiz, mantiqda ishlatilmaydigan](#157-tostring-foydali-xavfsiz-mantiqda-ishlatilmaydigan)
- [15.8 `clone` dan voz kechish va nusxa konstruktori](#158-clone-dan-voz-kechish-va-nusxa-konstruktori)
- [15.9 O'zgaradigan kalit va `HashMap` dagi yo'qolgan yozuv](#159-ozgaradigan-kalit-va-hashmap-dagi-yoqolgan-yozuv)
- [15.10 `Comparator` ni toza qurish](#1510-comparator-ni-toza-qurish)
- [15.11 Amalda qo'llash](#1511-amalda-qollash)

</details>


`equals`, `hashCode`, `compareTo` va `toString` - Java da eng ko'p noto'g'ri yoziladigan to'rt metod, va ularning xatosi eng qiyin topiladigan xatolar qatoriga kiradi: `HashMap` dan yozuv yo'qoladi, `TreeSet` tartibi buziladi, log da ma'lumot oqib ketadi. Bu bobda to'rt shartnomaning aniq talablari va ularni Java da to'g'ri bajarish.

## 15.1 `equals` shartnomasi: besh qoida

`equals` metodi matematik ekvivalentlik munosabatini amalga oshirishi kerak. Beshta qoida bor va ularning har biri buzilganda alohida muammo tug'iladi.

| Qoida | Talab | Buzilsa |
|---|---|---|
| Refleksivlik | `x.equals(x)` → `true` | `contains` ishlamaydi |
| Simmetriklik | `x.equals(y)` == `y.equals(x)` | to'plam tartibiga qarab natija o'zgaradi |
| Tranzitivlik | `x=y`, `y=z` → `x=z` | `HashSet` dublikat saqlaydi |
| Izchillik | qiymat o'zgarmasa natija o'zgarmaydi | yozuv yo'qoladi (15.9) |
| `null` | `x.equals(null)` → `false` | `NullPointerException` |

Eng ko'p buziladigani - simmetriklik, va u odatda vorislikda yoki turlar aralashganda chiqadi (`String` bilan `CaseInsensitiveString` ni solishtirish).

## 15.2 `hashCode` shartnomasi va `equals` bilan bog'liqligi

`hashCode` ning yagona majburiy qoidasi: `equals` bo'yicha teng obyektlar bir xil `hashCode` qaytarishi kerak. Teskarisi shart emas (turli obyektlar bir xil hash olishi mumkin).

Shundan eng ko'p uchraydigan xato kelib chiqadi: `equals` yozilgan, `hashCode` yozilmagan. Bunda obyekt `HashMap` ga qo'yiladi va keyin topilmaydi, chunki `Object.hashCode` identifikatsiya bo'yicha ishlaydi. Checkstyle `EqualsHashCode` qoidasi shu xatoni CI da bloklaydi (13.4).

```java
// yomon: equals bor, hashCode yo'q - HashMap ishlamaydi
public final class Sku {
    private final String code;
    @Override public boolean equals(Object o) { ... }
    // hashCode yo'q!
}

// yaxshi: ikkisi birga, bir xil maydonlardan
public final class Sku {

    private final String code;

    @Override
    public boolean equals(Object o) {
        return o instanceof Sku other && code.equals(other.code);
    }

    @Override
    public int hashCode() {
        return code.hashCode();
    }
}
```

## 15.3 `equals` ni yozish shabloni va `instanceof` pattern matching

Zamonaviy Java da `equals` ni yozish shabloni qisqargan: `instanceof` pattern matching bir qadamda tur tekshiruvini va o'zgaruvchi e'lonini bajaradi.

```java
@Override
public boolean equals(Object o) {
    // 1) O'zini o'zi bilan solishtirish - tez yo'l (ixtiyoriy, lekin arzon)
    if (this == o) return true;
    // 2) Tur tekshiruvi va cast bir qadamda; null avtomatik false beradi
    if (!(o instanceof Payment other)) return false;
    // 3) Muhim maydonlar: arzonidan boshlab solishtirish
    return amount.equals(other.amount)
            && currency == other.currency           // enum: == yetarli
            && paymentId.equals(other.paymentId);
}
```

Eng oson va eng xavfsiz yechim esa - `record` ishlatish: `equals`, `hashCode` va `toString` avtomatik generatsiya qilinadi va shartnomaga mos bo'ladi ([arxitektor hujjatidagi](../architect/README.md) record bo'limi).

## 15.4 Vorislik ostida tenglik: `getClass()` yoki `instanceof`

Bu klassik dilemma. `getClass() != o.getClass()` tekshiruvi simmetriklikni saqlaydi, lekin Liskov printsipini buzadi: voris sinf nusxasi hech qachon bazaviy sinf nusxasiga teng bo'lmaydi (Hibernate proxy bilan muammo shu yerdan keladi). `instanceof` esa Liskov ni saqlaydi, lekin voris sinf yangi maydon qo'shsa simmetriklik buziladi.

Amaliy yechim: **tenglik kerak bo'lgan sinflarni `final` qilish** yoki `record` ishlatish. Vorislik va qiymat tengligi birga yashamaydi; kerak bo'lsa kompozitsiya ishlatiladi (17.9).

```java
// yaxshi: final sinf - dilemma yo'q
public final class Money { ... }

// yaxshi: record - final va shartnomaga mos
public record Money(BigDecimal amount, Currency currency) { }

// JPA entiteti uchun (proxy sababli instanceof kerak, identifikator bo'yicha tenglik)
@Override
public boolean equals(Object o) {
    if (this == o) return true;
    if (!(o instanceof Payment other)) return false;
    return id != null && id.equals(other.id);     // 28.1
}

@Override
public int hashCode() {
    return getClass().hashCode();   // id o'zgarishi hash ni buzmasligi uchun
}
```

## 15.5 Entitet va value object tengligi farqi

Ikki xil tenglik bor va ularni aralashtirish eng ko'p uchraydigan domen xatosi. **Value object** tengligi qiymat bo'yicha: ikki `Money(1000, UZS)` bir xil. **Entitet** tengligi identifikator bo'yicha: ikki `Customer` bir xil `id` bilan teng, hatto ismlari farq qilsa ham.

| Jihat | Value object | Entitet |
|---|---|---|
| Tenglik | barcha maydonlar | faqat identifikator |
| O'zgaruvchanlik | o'zgarmas | o'zgaradi |
| `hashCode` | maydonlardan | `getClass()` yoki barqaror id |
| Java shakli | `record`, `final class` | `@Entity` sinf |
| Misol | `Money`, `Sku`, `DateRange` | `Order`, `Customer` |

## 15.6 `compareTo` shartnomasi va `equals` bilan izchillik

`Comparable` shartnomasi `equals` dan qat'iyroq: antisimmetriklik (`sgn(x.compareTo(y)) == -sgn(y.compareTo(x))`), tranzitivlik, va izchillik (`x.compareTo(y) == 0` bo'lsa, barcha `z` uchun natija bir xil).

Qo'shimcha **kuchli tavsiya**: `(x.compareTo(y) == 0)` va `x.equals(y)` bir xil natija berishi kerak. Buzilsa, `TreeSet` va `TreeMap` boshqacha ishlaydi: `BigDecimal("1.0")` va `BigDecimal("1.00")` `compareTo` bo'yicha teng, `equals` bo'yicha emas, shuning uchun `HashSet` da ikkita element, `TreeSet` da bitta bo'ladi (20.2).

```java
// yaxshi: Comparator.comparing bilan xavfsiz qurish, qo'lda hisob yo'q
public record SettlementKey(LocalDate date, String bankCode, long sequence)
        implements Comparable<SettlementKey> {

    private static final Comparator<SettlementKey> ORDER =
            Comparator.comparing(SettlementKey::date)
                    .thenComparing(SettlementKey::bankCode)
                    .thenComparingLong(SettlementKey::sequence);

    @Override
    public int compareTo(SettlementKey other) {
        return ORDER.compare(this, other);
    }
}
```

Qo'lda `a - b` yozmaslik kerak: butun son to'lib ketishi tartibni teskari aylantiradi (20.3).

## 15.7 `toString`: foydali, xavfsiz, mantiqda ishlatilmaydigan

`toString` log va debug uchun yoziladi, shuning uchun uch talab bor. Birinchi, foydali bo'lishi: sinf nomi va kalit maydonlar. Ikkinchi, xavfsiz bo'lishi: parol, token, karta raqami, shaxsiy ma'lumot chiqmasligi (29.8). Uchinchi, mantiqda ishlatilmasligi: `toString` natijasini parslash yoki solishtirish shartnomaga bog'lanish.

```java
// yomon: sezgir ma'lumot log'ga chiqadi
@Override public String toString() {
    return "Card{number=" + number + ", cvv=" + cvv + "}";
}

// yaxshi: maskalangan, foydali
@Override public String toString() {
    return "Card{last4=%s, expiry=%s}".formatted(number.last4(), expiry);
}
```

JPA entitetida `toString` ichida lazy assotsiatsiyani chaqirish `LazyInitializationException` yoki kutilmagan so'rov beradi; shuning uchun entitet `toString` ida faqat skalyar maydonlar bo'lishi kerak (28.1).

## 15.8 `clone` dan voz kechish va nusxa konstruktori

`Cloneable` interfeysi buzilgan dizayn: u metod e'lon qilmaydi, `Object.clone` `protected`, chuqur nusxa qo'lda yozilishi kerak va `final` maydonlar bilan ishlamaydi. Yechim: `clone` ni umuman yozmaslik.

```java
// yomon
public class Order implements Cloneable {
    @Override public Order clone() throws CloneNotSupportedException { ... }
}

// yaxshi: nusxa konstruktori yoki statik fabrika
public final class Order {
    public Order(Order source) { ... }
    public static Order copyOf(Order source) { ... }
}

// eng yaxshi: o'zgarmas obyekt - nusxa umuman kerak emas ([16-bob](16-ozgarmaslik-va-holat-boshqaruvi-kod.md))
public record Money(BigDecimal amount, Currency currency) { }
```

## 15.9 O'zgaradigan kalit va `HashMap` dagi yo'qolgan yozuv

`HashMap` kaliti sifatida ishlatilgan obyekt `put` dan keyin o'zgarsa, uning hash kodi o'zgaradi va yozuv boshqa bucket da qoladi: `get` uni topolmaydi, `containsKey` `false` qaytaradi, lekin `size()` hali ham 1. Bu xato `equals`/`hashCode` izchillik qoidasining (15.1) buzilishi.

```java
// yomon: kalit o'zgaradi
Map<MutableSku, Integer> stock = new HashMap<>();
MutableSku sku = new MutableSku("A-1");
stock.put(sku, 10);
sku.setCode("A-2");          // hash o'zgardi
stock.get(sku);              // null! yozuv yo'qoldi

// yaxshi: kalit o'zgarmas
record Sku(String code) { }
Map<Sku, Integer> stock = new HashMap<>();
```

Qoida: `Map` kaliti va `Set` elementi har doim o'zgarmas bo'lishi kerak. JPA entitetini kalit sifatida ishlatish ham xavfli, chunki `id` `persist` dan keyin tayinlanadi.

## 15.10 `Comparator` ni toza qurish

`Comparator` ni qo'lda yozish xato manbasi; `Comparator.comparing` zanjiri esa o'qiladi va xatosiz.

```java
// yomon: qo'lda, teskari tartib va null ishlovi aralashgan
orders.sort((a, b) -> {
    int c = b.getCreatedAt().compareTo(a.getCreatedAt());
    if (c != 0) return c;
    return a.getId().intValue() - b.getId().intValue();   // to'lib ketish xavfi
});

// yaxshi: deklarativ, o'qiladi, null siyosati oshkor
orders.sort(comparing(Order::createdAt).reversed()
        .thenComparing(Order::id)
        .thenComparing(Order::customerName, nullsLast(naturalOrder())));
```

Ikkinchi qoida: `Comparator` ni `static final` maydonga chiqarish - har bir chaqiruvda yangi obyekt yaratilmaydi va nom tartibni tushuntiradi (`NEWEST_FIRST`).

## 15.11 Amalda qo'llash

- [ ] `equals` yozilgan barcha sinflarda `hashCode` ham borligini Checkstyle `EqualsHashCode` bilan majburiy qiling.
- [ ] Value object larni `record` ga o'tkazib, qo'lda yozilgan `equals`/`hashCode` ni o'chiring.
- [ ] Tenglik kerak bo'lgan sinflarni `final` qilib, vorislik ostidagi simmetriklik muammosini yo'qoting.
- [ ] JPA entitetlarida tenglikni identifikator bo'yicha yozib, `hashCode` ni barqaror qiling (28.1).
- [ ] `Comparable` amalga oshirilgan sinflarda `compareTo` va `equals` izchilligini test bilan tekshiring.
- [ ] Barcha `toString` larni ko'rib, sezgir maydonlarni maskalang va lazy assotsiatsiyalarni olib tashlang.
- [ ] `Cloneable` ishlatilgan joylarni nusxa konstruktori yoki o'zgarmas turga o'tkazing.
- [ ] `Map` kaliti va `Set` elementi sifatida ishlatilgan o'zgaradigan turlarni topib, o'zgarmas turga almashtiring.

---

[&larr; 14. Obyekt va ma'lumot tuzilmasi: inkapsulyatsiya](14-obyekt-va-malumot-tuzilmasi-inkapsulyatsiya.md) · [Mundarija](README.md) · [16. O'zgarmaslik va holat boshqaruvi kod darajasida &rarr;](16-ozgarmaslik-va-holat-boshqaruvi-kod.md)
