<!-- doc: clean-code | chapter: 20 | part: VII. Java tilining toza ishlatilishi -->

[Barcha hujjatlar](../../README.md) / [Toza kod qoidalari](README.md)

# 20. Primitiv, son va pul (Primitives, Numbers and Money)

<details>
<summary>Bu bobdagi 9 bo'lim</summary>

- [20.1 Pul uchun `double` ishlatmaslik](#201-pul-uchun-double-ishlatmaslik)
- [20.2 `BigDecimal` scale, rounding va `equals` tuzog'i](#202-bigdecimal-scale-rounding-va-equals-tuzogi)
- [20.3 Butun sonning to'lib ketishi va `Math.*Exact`](#203-butun-sonning-tolib-ketishi-va-mathexact)
- [20.4 Bo'lish, qoldiq va manfiy son xatti-harakati](#204-bolish-qoldiq-va-manfiy-son-xatti-harakati)
- [20.5 Primitiv va boxed tur tanlovi, `==` tuzog'i](#205-primitiv-va-boxed-tur-tanlovi--tuzogi)
- [20.6 Avtoboxing narxi va `null` unboxing](#206-avtoboxing-narxi-va-null-unboxing)
- [20.7 Pul va o'lchovni value object bilan ifodalash](#207-pul-va-olchovni-value-object-bilan-ifodalash)
- [20.8 Tasodifiy son, UUID va identifikator generatsiyasi](#208-tasodifiy-son-uuid-va-identifikator-generatsiyasi)
- [20.9 Amalda qo'llash](#209-amalda-qollash)

</details>


Son bilan ishlash Java da eng ko'p jim xato beradigan soha: natija noto'g'ri, lekin istisno tashlanmaydi. Bu bobda pul hisobining qoidalari, `BigDecimal` mexanikasi, to'lib ketish, boxing, va identifikator generatsiyasi.

## 20.1 Pul uchun `double` ishlatmaslik

`double` va `float` ikkilik kasr sifatida saqlanadi va `0.1` ni aniq ifodalay olmaydi. Pul hisobida bu darhol xatoga olib keladi va xato yillar davomida yig'iladi.

```java
// yomon: natija 0.30000000000000004
double total = 0.1 + 0.2;

// yomon: 1.03 - 0.42 = 0.6100000000000001
double change = 1.03 - 0.42;

// yaxshi: BigDecimal satr konstruktori bilan
BigDecimal total = new BigDecimal("0.10").add(new BigDecimal("0.20"));   // 0.30

// eng yaxshi: Money value object (3.3)
Money total = Money.of("0.10", UZS).plus(Money.of("0.20", UZS));
```

Qo'shimcha muhim qoida: `new BigDecimal(0.1)` **xato** - u `double` ni oladi va noaniqlikni saqlab qoladi. Har doim `new BigDecimal("0.1")` yoki `BigDecimal.valueOf(0.1)` ishlatiladi. SonarQube buni `java:S2111` qoidasi bilan ushlaydi.

| Vazifa | To'g'ri tur |
|---|---|
| Pul summasi | `BigDecimal` yoki `Money` |
| Pulni butun sonda saqlash | `long` (tiyin), nomda birlik (3.3) |
| Foiz, stavka | `BigDecimal` |
| O'lchov (og'irlik, masofa) | `BigDecimal` yoki value object |
| Ilmiy hisob, grafika | `double` |
| Sanoq, identifikator | `long`, `int` |
| Bazadagi ustun | `numeric(19,4)`, `double precision` emas |

## 20.2 `BigDecimal` scale, rounding va `equals` tuzog'i

`BigDecimal` da uch tuzoq bor va uchtasi ham production da uchraydi.

**Birinchi**: `equals` scale ni hisobga oladi. `new BigDecimal("1.0").equals(new BigDecimal("1.00"))` → `false`. Solishtirish uchun `compareTo` ishlatiladi (15.6).

**Ikkinchi**: `divide` aniq bo'linmasa `ArithmeticException` tashlaydi. Har doim scale va `RoundingMode` berish kerak.

**Uchinchi**: yakkalash qoidasi (rounding) biznes qarori. `HALF_UP` odatiy, lekin bank hisobida `HALF_EVEN` (banker's rounding) talab qilinishi mumkin.

```java
// yomon: ArithmeticException: Non-terminating decimal expansion
BigDecimal share = total.divide(new BigDecimal("3"));

// yaxshi: scale va rounding oshkor, biznes qarori kodda ko'rinadi
private static final int MONEY_SCALE = 2;
private static final RoundingMode MONEY_ROUNDING = RoundingMode.HALF_UP;

BigDecimal share = total.divide(new BigDecimal("3"), MONEY_SCALE, MONEY_ROUNDING);

// yomon: equals scale ga sezgir
if (amount.equals(new BigDecimal("100.00"))) { ... }
// yaxshi
if (amount.compareTo(new BigDecimal("100.00")) == 0) { ... }
```

## 20.3 Butun sonning to'lib ketishi va `Math.*Exact`

Java da butun son to'lib ketganda istisno tashlanmaydi - natija aylanib ketadi va manfiy bo'ladi. Bu `compareTo` da (15.6), hisoblagichlarda va vaqt hisobida xatoga olib keladi.

```java
// yomon: to'lib ketish jim o'tadi
int millis = seconds * 1000;              // seconds > 2_147_483 bo'lsa manfiy
int diff = a.getId().intValue() - b.getId().intValue();   // tartib teskari aylanadi

// yaxshi: to'lib ketish istisno beradi
int millis = Math.multiplyExact(seconds, 1000);
long total = Math.addExact(current, increment);

// yaxshi: solishtirish uchun ayirish emas, compare
int order = Long.compare(a.id(), b.id());
```

Qoida: hisoblagich, identifikator va vaqt oraliqlarida `long` ishlatish; arifmetikada `Math.addExact`/`multiplyExact` ni standart qilish.

## 20.4 Bo'lish, qoldiq va manfiy son xatti-harakati

Butun sonlarni bo'lish natijani kesib tashlaydi (`7 / 2 == 3`) va bu ko'pincha kutilmagan. Qoldiq (`%`) esa manfiy sonlar bilan matematik modul emas: `-1 % 3 == -1`, `2` emas.

```java
// yomon: aylanma indeks manfiy bo'lib qoladi
int index = (current - 1) % size;          // -1 bo'lishi mumkin

// yaxshi: Math.floorMod matematik modul beradi
int index = Math.floorMod(current - 1, size);

// yomon: butun bo'lish kesib tashlaydi
int average = total / count;               // 7/2 = 3

// yaxshi: niyat oshkor
int average = Math.round((float) total / count);
BigDecimal exact = BigDecimal.valueOf(total)
        .divide(BigDecimal.valueOf(count), 2, RoundingMode.HALF_UP);
```

## 20.5 Primitiv va boxed tur tanlovi, `==` tuzog'i

`Integer` va `int` farqi `==` da ko'rinadi: `Integer` solishtirilganda havolalar solishtiriladi va `-128..127` oralig'ida kesh ishlaydi, shuning uchun kichik sonlarda to'g'ri, kattalarda noto'g'ri natija chiqadi.

```java
Integer a = 127, b = 127;
a == b;        // true  (kesh)
Integer c = 128, d = 128;
c == d;        // false (yangi obyektlar) - eng chalkash xatolardan biri

// yaxshi: boxed turlarni har doim equals bilan solishtirish
Objects.equals(c, d);
// eng yaxshi: primitiv ishlatish mumkin bo'lsa, primitiv
int c = 128, d = 128;
c == d;        // true
```

Qoida: hisob va mahalliy o'zgaruvchilarda primitiv; `null` ma'noga ega bo'lgan joyda (ixtiyoriy maydon, baza ustuni) boxed tur.

## 20.6 Avtoboxing narxi va `null` unboxing

Avtoboxing ikki muammo keltiradi. Birinchi - narx: sikl ichida har bir amal yangi obyekt yaratadi. Ikkinchi va xavflisi - `null` unboxing: `null` bo'lgan `Integer` ni `int` ga aylantirish `NullPointerException` beradi va u imzoda ko'rinmaydi.

```java
// yomon: issiq siklda million obyekt yaratiladi
Long sum = 0L;
for (long i = 0; i < 1_000_000; i++) {
    sum += i;                 // har iteratsiyada boxing/unboxing
}

// yaxshi
long sum = 0L;

// yomon: NullPointerException, sababi imzoda ko'rinmaydi
int quantity = order.getQuantity();       // getQuantity() Integer qaytaradi va null bo'lishi mumkin

// yaxshi: null siyosati oshkor
int quantity = Objects.requireNonNullElse(order.quantity(), 0);
```

`Map<String, Integer>` da `map.get(key)` topilmasa `null` qaytaradi va darhol `int` ga aylantirilsa NPE beradi; `getOrDefault` ishlatish kerak (23.2).

## 20.7 Pul va o'lchovni value object bilan ifodalash

Pul uchun value object yozish primitivlarga berilish anti-patternidan ([patternlar hujjatidagi](../patterns/README.md) primitivlarga berilish anti-patterni) chiqish yo'li va u uch foyda beradi: valyuta aralashmaydi, yakkalash qoidasi bir joyda, va arifmetika domen tilida o'qiladi.

```java
public record Money(BigDecimal amount, Currency currency) implements Comparable<Money> {

    private static final int SCALE = 2;
    private static final RoundingMode ROUNDING = RoundingMode.HALF_UP;

    public Money {
        Objects.requireNonNull(currency, "currency");
        amount = amount.setScale(SCALE, ROUNDING);      // scale bir joyda normallashadi
    }

    public static Money of(String amount, Currency currency) {
        return new Money(new BigDecimal(amount), currency);
    }

    public Money plus(Money other) {
        requireSameCurrency(other);
        return new Money(amount.add(other.amount), currency);
    }

    public Money multiply(Quantity quantity) {
        return new Money(amount.multiply(BigDecimal.valueOf(quantity.value())), currency);
    }

    public boolean greaterThan(Money other) {
        requireSameCurrency(other);
        return amount.compareTo(other.amount) > 0;
    }

    @Override
    public int compareTo(Money other) {
        requireSameCurrency(other);
        return amount.compareTo(other.amount);
    }

    private void requireSameCurrency(Money other) {
        if (currency != other.currency) {
            throw new CurrencyMismatchException(currency, other.currency);
        }
    }
}
```

## 20.8 Tasodifiy son, UUID va identifikator generatsiyasi

Tasodifiy son uchun `Math.random()` va `new Random()` kriptografik emas va ularni token, parol yoki idempotentlik kaliti uchun ishlatish xavfsizlik nuqsoni.

| Vazifa | To'g'ri vosita |
|---|---|
| Token, sir, parol tiklash kaliti | `SecureRandom` |
| Test ma'lumoti, taqsimot | `Random`, `ThreadLocalRandom` |
| Ko'p threadli hisob | `ThreadLocalRandom.current()` |
| Tashqi identifikator | `UUID.randomUUID()` (v4) |
| Tartiblangan identifikator | UUID v7 yoki `bigserial` |
| Idempotentlik kaliti | klient beradi, server generatsiya qilmaydi |
| Baza birlamchi kaliti | `bigint identity`/`bigserial` |

```java
// yomon: Random kriptografik emas, token taxmin qilinadi
String token = Long.toHexString(new Random().nextLong());

// yaxshi
private static final SecureRandom RANDOM = new SecureRandom();

static String newToken() {
    byte[] bytes = new byte[32];
    RANDOM.nextBytes(bytes);
    return Base64.getUrlEncoder().withoutPadding().encodeToString(bytes);
}
```

## 20.9 Amalda qo'llash

- [ ] Pul va stavka bilan ishlaydigan barcha `double`/`float` maydonlarni topib, `BigDecimal` yoki `Money` ga o'tkazing.
- [ ] `new BigDecimal(<double>)` chaqiruvlarini satr yoki `valueOf` shakliga almashtiring.
- [ ] `BigDecimal.divide` chaqiruvlarida scale va `RoundingMode` borligini tekshiring.
- [ ] `BigDecimal.equals` ishlatilgan joylarni `compareTo` ga o'tkazing.
- [ ] Boxed turlar `==` bilan solishtirilgan joylarni `Objects.equals` yoki primitivga o'tkazing.
- [ ] Issiq sikllardagi boxed hisoblagichlarni primitiv turlarga almashtiring.
- [ ] `new Random()` ishlatilgan xavfsizlikka tegishli joylarni `SecureRandom` ga o'tkazing.
- [ ] ArchUnit qoidasi bilan `amount`, `price`, `total` nomli maydonlarda `double` ni taqiqlang.

---

[&larr; 19. Istisno mexanikasi va resurslar](19-istisno-mexanikasi-va-resurslar.md) · [Mundarija](README.md) · [21. Satr, matn va regex &rarr;](21-satr-matn-va-regex.md)
