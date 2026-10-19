<!-- doc: clean-code | chapter: 20 | part: VII. Java tilining toza ishlatilishi -->

[Barcha hujjatlar](../../README.md) / [Toza kod qoidalari](README.md)

> Holat: tekshirilgan (2026-10-19). Manbalar bob oxirida.

# 20. Primitiv, son va pul (Primitives, Numbers and Money)

<details>
<summary>Bu bobdagi 12 bo'lim</summary>

- [20.1 Pul uchun `double` ishlatmaslik](#201-pul-uchun-double-ishlatmaslik)
- [20.2 `BigDecimal` scale, rounding va `equals` tuzog'i](#202-bigdecimal-scale-rounding-va-equals-tuzogi)
- [20.3 Butun sonning to'lib ketishi va `Math.*Exact`](#203-butun-sonning-tolib-ketishi-va-mathexact)
- [20.4 Bo'lish, qoldiq va manfiy son xatti-harakati](#204-bolish-qoldiq-va-manfiy-son-xatti-harakati)
- [20.5 Primitiv va boxed tur tanlovi, `==` tuzog'i](#205-primitiv-va-boxed-tur-tanlovi--tuzogi)
- [20.6 Avtoboxing narxi va `null` unboxing](#206-avtoboxing-narxi-va-null-unboxing)
- [20.7 Pul va o'lchovni value object bilan ifodalash](#207-pul-va-olchovni-value-object-bilan-ifodalash)
- [20.8 Tasodifiy son, UUID va identifikator generatsiyasi](#208-tasodifiy-son-uuid-va-identifikator-generatsiyasi)
- [20.9 `double` ning `NaN` va `Infinity` xulqi](#209-double-ning-nan-va-infinity-xulqi)
- [20.10 Yashirin cast: qo'shma tayinlash va toraytiruvchi konversiya](#2010-yashirin-cast-qoshma-tayinlash-va-toraytiruvchi-konversiya)
- [20.11 Son literalini yozish: `L` suffiksi, bosh nol va pastki chiziq](#2011-son-literalini-yozish-l-suffiksi-bosh-nol-va-pastki-chiziq)
- [20.12 Amalda qo'llash](#2012-amalda-qollash)

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

`BigDecimal` va butun son orasidagi tanlov taxmin bilan emas, raqam soni bilan qilinadi. `BigDecimal` ikki narxga ega: u primitivdan sekinroq va chaqiruvi noqulayroq. Shuning uchun o'nlik kasrni o'zingiz hisobga olishga tayyor bo'lsangiz, qiymat hajmiga qarab tanlanadi: to'qqizta o'nlik raqamdan oshmasa `int`, o'n sakkiztadan oshmasa `long`, oshsa `BigDecimal`. Buning ustiga `BigDecimal` ning foydasi ham bor: yaxlitlash rejimi oshkor tanlanadi, bu esa qonun talab qilgan yaxlitlash qoidasi bor hisobda hal qiluvchi bo'ladi.

## 20.2 `BigDecimal` scale, rounding va `equals` tuzog'i

`BigDecimal` da uch tuzoq bor va uchtasi ham production da uchraydi.

**Birinchi**: `equals` scale ni hisobga oladi. `new BigDecimal("1.0").equals(new BigDecimal("1.00"))` → `false`. Solishtirish uchun `compareTo` ishlatiladi (15.6).

**Ikkinchi**: `divide` aniq bo'linmasa `ArithmeticException` tashlaydi. Har doim scale va `RoundingMode` berish kerak.

**Uchinchi**: yaxlitlash qoidasi (rounding) biznes qarori. `HALF_UP` odatiy, lekin bank hisobida `HALF_EVEN` (banker's rounding) talab qilinishi mumkin.

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

Eng ko'p takrorlanadigan shakl: natijani `long` ga tayinlab, o'zini himoyalangan deb o'ylash. `long millis = seconds * 1000;` to'lib ketishdan **saqlamaydi**, chunki amal ikki `int` operand ustida, ya'ni 32 bitda bajariladi va kengaytirish faqat natija hisoblangandan keyin bo'ladi. Shuning uchun operandlardan biri **ko'paytirishdan oldin** `long` ga keltiriladi: `1000L` yoki `(long) seconds`. Til spetsifikatsiyasining o'zi shu misolni beradi: `int i = 1000000;` uchun `i * i` qiymati -727379968 bo'ladi, `long l = i; l * l` esa 1000000000000 beradi.

```java
// yomon: amal 32 bitda bajariladi, keyin kengayadi
long millis = seconds * 1000;

// yaxshi: operand oldin long bo'ldi, amal 64 bitda
long millis = seconds * 1000L;
long millis = (long) seconds * 1000;
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

Xatoning eng chalg'ituvchi shakli solishtirgichda chiqadi: u ko'p testdan o'tadi va faqat kesh oralig'idan tashqarida yoki yangi obyektda yiqiladi.

```java
// yomon: ikkinchi solishtiruv havolalarni solishtiradi
Comparator<Integer> naturalOrder = (i, j) -> (i < j) ? -1 : (i == j ? 0 : 1);
// compare(new Integer(42), new Integer(42)) -> 1, holbuki 0 bo'lishi kerak

// yaxshi: boxed turni unbox qilib yoki tayyor solishtirgich bilan
Comparator<Integer> naturalOrder = Comparator.naturalOrder();
```

Birinchi shart (`i < j`) ikkisini ham unbox qiladi va to'g'ri ishlaydi, ikkinchisi (`i == j`) esa unbox qilmaydi: boxed turda `==` havolalarni solishtiradi. Shu sababli boxed tur bilan primitiv aralashgan ifodada boxed tomon unbox qilinadi, ikki boxed tomon esa qilinmaydi.

Qoida: hisob va mahalliy o'zgaruvchilarda primitiv; `null` ma'noga ega bo'lgan joyda (ixtiyoriy maydon, baza ustuni) boxed tur. Uchta haqiqiy farq bor va uchtasi ham shu bobda ko'rildi: boxed turda ayniylik (identity) bor, `null` qiymati bor, va u primitivdan ko'p vaqt va xotira oladi.

Qoidaning chegarasi ham aniq: uch joyda boxed tur **majburiy** va u yerda tanlov yo'q. Birinchi: to'plam elementi, kaliti yoki qiymati, chunki Java to'plamlari primitiv saqlay olmaydi (`List<Integer>`, `Map<String, Long>`). Ikkinchi: parametrlangan tur argumenti, chunki tur argumenti primitiv bo'lmaydi (`ThreadLocal<Integer>`, `Optional<Long>`). Uchinchi: refleksiv metod chaqiruvi, chunki `Method.invoke` argumentlarni `Object[]` sifatida oladi. Shu uchtasidan tashqari har joyda primitiv birinchi tanlov; boxed tur esa `null` ning o'z ma'nosi bo'lganda qo'shiladi.

Primitiv oqim turlari (`IntStream`, `LongStream`, `DoubleStream`) birinchi holatning qisman chetlab o'tilishi: to'plam o'rniga oqim bilan ishlaganda boxing ni butunlay yo'qotish mumkin (20.6).

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

Pul uchun value object yozish primitivlarga berilish anti-patternidan ([patternlar hujjatidagi](../patterns/README.md) primitivlarga berilish anti-patterni) chiqish yo'li va u uch foyda beradi: valyuta aralashmaydi, yaxlitlash qoidasi bir joyda, va arifmetika domen tilida o'qiladi.

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
| Ko'p threadli hisob, har thread o'z oqimi | `ThreadLocalRandom.current()` |
| Bo'linadigan parallel oqim (`parallel()`, fork/join) | `SplittableRandom` |
| Tashqi identifikator | `UUID.randomUUID()` (v4) |
| Tartiblangan identifikator | UUID v7 yoki `bigserial` |
| Idempotentlik kaliti | klient beradi, server generatsiya qilmaydi |
| Baza birlamchi kaliti | `bigint identity`/`bigserial` |

Jadvaldagi oxirgi ikki qator bir-biriga o'xshaydi, lekin ularni ajratuvchi shart aniq: generator **bo'linishi** kerakmi. `ThreadLocalRandom` har thread uchun alohida nusxa beradi va `synchronized` raqobatini yo'qotadi, shuning uchun o'z thread lari bo'lgan ko'p threadli hisobda to'g'ri tanlov. Lekin bo'linadigan (splittable) parallel oqimda vazifa fork/join bilan bo'laklanadi va har bo'lak **o'z**, statistik mustaqil generatoriga ega bo'lishi kerak: shu ishni `SplittableRandom` bajaradi, uning `split()` metodi yangi mustaqil generator qaytaradi. `Random` esa uchinchi variant va u ikki holatda ham yaramaydi: uning holati `AtomicLong` da va har `nextInt()` chaqiruvi CAS tsikliga tushadi, ya'ni parallellik qancha oshsa shuncha yomonlashadi.

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

## 20.9 `double` ning `NaN` va `Infinity` xulqi

Butun sonni nolga bo'lish `ArithmeticException` beradi, `double` ni nolga bo'lish esa
**istisno tashlamaydi**: natija `Infinity` yoki `NaN` bo'ladi va hisob davom etadi.
`Float` va `Double` shu ikki maxsus qiymat uchun `isInfinite()` va `isNaN()`
metodlarini beradi: birinchisi qiymat kattaligi cheksiz bo'lsa, ikkinchisi qiymat
son bo'lmasa `true` qaytaradi. Kitob misoli `1/0.` uchun `Infinity: true, false`
va `0/0.` uchun `NaN: false, true` chiqaradi (Schildt, *Java The Complete
Reference*, 12-nashr, McGraw Hill, 2022, 19-bob (516-517-bet)).

Xavfi shunda: bu qiymatlar jim tarqaladi. `NaN` qatnashgan har qanday arifmetika
yana `NaN` beradi, shuning uchun xato hisob boshida emas, hisobot yoki bazaga
yozish paytida ko'rinadi va sababi allaqachon yo'qolgan.

```java
// yomon: nolga bo'lish jim o'tadi, xato pastga oqib ketadi
double conversionRate = (double) converted / visits;   // visits == 0 -> NaN
double average = total / count;                        // count == 0 -> NaN yoki Infinity
if (conversionRate > ALERT_THRESHOLD) { ... }          // NaN bilan har doim false

// yaxshi: qiymat hisob chegarasida tekshiriladi
double conversionRate = visits == 0 ? 0.0 : (double) converted / visits;
if (!Double.isFinite(conversionRate)) {
    throw new IllegalStateException("konversiya chekli emas: " + conversionRate);
}
```

`NaN` ning ikkinchi oqibati tenglik va tartibga tegadi va uni yod bilish kerak,
chunki uchta mexanizm uchta boshqa javob beradi.

| Ifoda | Natija | Sabab |
|---|---|---|
| `x == x` (`x` = `NaN`) | `false` | `NaN` hech narsaga, hatto o'ziga teng emas |
| `Double.valueOf(NaN).equals(Double.valueOf(NaN))` | `true` | `equals` bit shaklini solishtiradi |
| `0.0 == -0.0` | `true` | ikkisi bir xil son |
| `Double.valueOf(0.0).equals(Double.valueOf(-0.0))` | `false` | bit shakli boshqa |
| `Double.compare(NaN, 1.0)` | musbat | `NaN` boshqa hamma qiymatdan katta deb olinadi |

Shundan uchta amaliy qoida chiqadi. Birinchi: `double` ni `NaN` ga tekshirish uchun
`==` ishlatilmaydi, `Double.isNaN(x)` yoziladi; chekli ekanini bitta tekshiruvda
bilish kerak bo'lsa `Double.isFinite(x)`. Ikkinchi: `double` maydoni bor sinfning
`equals` va `hashCode` i `Double.compare` yoki `doubleToLongBits` ustiga quriladi,
aks holda `NaN` saqlagan obyekt `HashMap` da o'zini topa olmaydi
([`equals` shartnomasi](15-tenglik-hash-va-obyekt-shartnomalari.md#151-equals-shartnomasi-besh-qoida)).
Uchinchi: solishtirgich `Double.compare` ga tayanadi, qo'lda ayirishga emas,
chunki ayirish `NaN` va `-0.0` ni noto'g'ri tartiblaydi va
[to'lib ketish](#203-butun-sonning-tolib-ketishi-va-mathexact) xavfini qo'shadi.

```java
// yomon: NaN tekshiruvi == bilan - har doim false
if (value == Double.NaN) { ... }

// yaxshi
if (Double.isNaN(value)) { ... }

// yaxshi: tartib Double.compare ustida, NaN va -0.0 izchil joylashadi
measurements.sort(Comparator.comparingDouble(Measurement::value));
```

ESLATMA: `NaN` va `Infinity` ni tashqi chegarada (REST javobi, JSON, baza
ustuni) tekshirish va u yerga chiqarmaslik shu korpusning tavsiyasi; kitob faqat
`isInfinite` va `isNaN` semantikasini beradi. Chegarada tekshirishning eng arzon
joyi - `double` ni `BigDecimal` ga yoki
[`Money` kabi value object](#207-pul-va-olchovni-value-object-bilan-ifodalash) ga
o'tkazuvchi fabrika metodi.

## 20.10 Yashirin cast: qo'shma tayinlash va toraytiruvchi konversiya

Java ikki joyda cast ni so'ramasdan o'zi qo'yadi va natijada ma'lumot jim yo'qoladi.
Ikkisi ham kompilyatsiyadan ogohlantirishsiz o'tadi, shuning uchun ularni faqat
o'qib bilish mumkin.

**Qo'shma tayinlash (`+=`, `-=`, `*=`, `/=`, `%=`) ichida cast yashiringan.**
Spetsifikatsiya buni aniq aytadi: `E1 op= E2` shakli `E1 = (T) ((E1) op (E2))`
ga teng, bu yerda `T` - `E1` ning turi, farqi faqat `E1` bir marta baholanadi.
Kitob misoli: `short x = 3; x += 4.6;` kompilyatsiyadan o'tadi va `x` ga `7`
beradi, chunki u `x = (short)(x + 4.6)` ga teng (*The Java Language
Specification, Java SE 25 Edition*, 15.26.2 (720-bet)). Oddiy tayinlash
(`x = x + 4.6`) esa shu yerda kompilyatsiya xatosi beradi, ya'ni qisqa shakl
tekshiruvni o'chiradi.

```java
// yomon: qisqa shakl cast ni yashiradi, kompilyator jim turadi
byte flags = 100;
flags += 100;                     // -56: byte chegarasidan chiqdi
int count = 0;
count += 3.7;                     // 3: kasr qismi tashlandi
long millis = 0;
millis += Duration.ofDays(1).toNanos() / 1_000;   // niyat ko'rinmaydi

// yaxshi: tur o'zgarishi oshkor yoki umuman yo'q
int flags = 100;
flags = flags + 100;              // 200
long count = 0;
count = count + Math.round(3.7);  // 4, yo'qotish ko'rinadi
```

**Toraytiruvchi konversiya (narrowing primitive conversion) ikki xil kesadi.**
Butun turlar orasida u faqat eng past bitlarni qoldiradi (`T` ning bit soniga
teng), shuning uchun kattalik ham, ba'zan belgi ham o'zgaradi. Kasrdan butunga
o'tishda esa qiymat avval nol tomon yaxlitlanadi, keyin chegarada **to'yadi**:
juda kichik qiymat `int` yoki `long` ning eng kichik qiymatini, juda katta
qiymat eng kattasini beradi, `NaN` esa **nolga** aylanadi (shu yerda, 5.1.3
(116-117-bet)).

```java
// yomon: NaN nolga aylanadi va noto'g'ri narx jim yoziladi
double price = computePrice();              // NaN bo'lishi mumkin
int priceMinor = (int) (price * 100);       // NaN -> 0, ya'ni "bepul"

// yomon: katta qiymat to'yadi, aylanmaydi
long nanos = 9_999_999_999L;
int truncated = (int) nanos;                // yuqori bitlar tashlandi

// yaxshi: cast o'rniga aniq tekshiruv va aniq yaxlitlash
if (!Double.isFinite(price)) {
    throw new IllegalStateException("narx chekli emas: " + price);
}
long priceMinor = BigDecimal.valueOf(price)
        .movePointRight(2)
        .setScale(0, RoundingMode.HALF_UP)
        .longValueExact();

int exact = Math.toIntExact(nanos);         // sig'masa ArithmeticException
```

Qoida: pul va identifikator hisobida cast yozilmaydi. Butun turlar orasida
`Math.toIntExact` ishlatiladi, kasrdan butunga o'tishda `Math.round` yoki
`BigDecimal` bilan yaxlitlash oshkor yoziladi, qo'shma tayinlash esa turni
o'zgartirmaydigan joyda qoldiriladi.

## 20.11 Son literalini yozish: `L` suffiksi, bosh nol va pastki chiziq

Son literalining yozilishi uslub masalasi emas: uchta shakl jim mantiq xatosi beradi va ularning hammasi kompilyatsiyadan o'tadi.

**`long` suffiksi bosh `L` bilan yoziladi.** Kichik `l` qonuniy, lekin ko'pchilik shriftda raqam `1` dan ko'zda farqlanmaydi: `1l` va `11` bir xil ko'rinadi. Til spetsifikatsiyasining o'zi bosh `L` ni afzal deb belgilaydi va bu review da tekshiriladigan punkt.

**`int` chegarasidan katta literalga `L` suffiksi majburiy, cast yordam bermaydi.** Literal avval `int` deb o'qiladi, shundan keyin kompilyator uni diapazondan tashqarida deb xato beradi, ya'ni `long` ga keltirish ham kompilyatsiyani qutqarmaydi: xato cast ga yetmasdan, literalni o'qishda chiqadi. Yagona yechim - suffiks: `10_000_000_000L`.

**Son literali nol bilan boshlanmaydi.** Nol bilan boshlangan butun son literali **oktal** (sakkizlik) sanoqda o'qiladi: `0177` o'nlikda 127, `010` esa 8. Bu tuzoq ayniqsa qiymatlarni ustun bo'lib tekislashda chiqadi, chunki odam nollarni to'ldiruvchi deb o'ylaydi.

```java
// yomon: kichik l - 1 dan farqlanmaydi
long timeout = 30000l;

// yomon: oktal - qiymat 127, 177 emas
int permissions = 0177;

// yaxshi
long timeout = 30_000L;
long maxAmount = 10_000_000_000L;
int permissions = 177;
```

**Pastki chiziq bilan guruhlash.** Beshdan ko'p ketma-ket raqamli literalda pastki chiziq ishlatiladi va guruh asosga mos tanlanadi: o'nlik asosda uch raqamli guruhlar (`1_000_000`), hex da bayt yoki yarim bayt chegarasi (`0xFF_EC_DE_5E`), ikkilikda nibble (`0b0101_0101`). Pastki chiziq kompilyator uchun ko'rinmaydi, ya'ni qiymatga ta'sir qilmaydi, faqat o'qiydigan odam uchun. Qoidaning chegarasi ham bor: qiymat o'zi qisqa bo'lsa (`1000`) pastki chiziq shovqin qo'shadi, va guruhlash notekis bo'lsa (`10_00_000`) o'quvchini chalg'itadi.

Shu yerda nom bilan bog'liq qoida ham ishlaydi: literalni guruhlash uni o'qiladigan qiladi, lekin **ma'nosini** aytmaydi. Takrorlanadigan yoki ma'noli qiymat nomlangan konstantaga chiqariladi (`private static final long TIMEOUT_MILLIS = 30_000L`), aks holda u [sehrli son](../patterns/25-anti-patternlar.md#258-sehrli-sonlar-va-satrlar-magic-numbers--strings) bo'lib qoladi.

## 20.12 Amalda qo'llash

- [ ] Pul va stavka bilan ishlaydigan barcha `double`/`float` maydonlarni topib, `BigDecimal` yoki `Money` ga o'tkazing.
- [ ] `new BigDecimal(<double>)` chaqiruvlarini satr yoki `valueOf` shakliga almashtiring.
- [ ] `BigDecimal.divide` chaqiruvlarida scale va `RoundingMode` borligini tekshiring.
- [ ] `BigDecimal.equals` ishlatilgan joylarni `compareTo` ga o'tkazing.
- [ ] Boxed turlar `==` bilan solishtirilgan joylarni `Objects.equals` yoki primitivga o'tkazing.
- [ ] Issiq sikllardagi boxed hisoblagichlarni primitiv turlarga almashtiring.
- [ ] `new Random()` ishlatilgan xavfsizlikka tegishli joylarni `SecureRandom` ga o'tkazing.
- [ ] ArchUnit qoidasi bilan `amount`, `price`, `total` nomli maydonlarda `double` ni taqiqlang.
- [ ] `double` bo'lish bor joylarni topib, bo'luvchi nol bo'lishi mumkin bo'lganlarini `Double.isFinite` tekshiruvi bilan yoping.
- [ ] `== Double.NaN` va `!= Double.NaN` shakllarini grep qilib, `Double.isNaN` ga o'tkazing.
- [ ] `double` maydoni bor sinflarning `equals`, `hashCode` va solishtirgichlarini `Double.compare` ustiga ko'chiring.
- [ ] `byte`, `short` va `int` o'zgaruvchilardagi `+=` va `*=` chaqiruvlarini ko'rib chiqib, yashirin cast qiymatni kesmayotganini tekshiring.
- [ ] `(int)` va `(byte)` cast larini sanab, pul va identifikator hisobidagilarini `Math.toIntExact` yoki `BigDecimal` yaxlitlashga almashtiring.

## Manbalar

- *The Java Language Specification, Java SE 25 Edition* (Gosling, Joy, Steele, Bracha, Buckley, Smith, Bierman), 3.10.1 (33-bet) - `long` literalida bosh `L` suffiksining afzal ekani, kichik `l` ning raqam `1` dan farqlanmasligi
- *The Java Language Specification, Java SE 25 Edition* (Gosling, Joy, Steele, Bracha, Buckley, Smith, Bierman), 3.10.1 (34-bet) - nol bilan boshlangan butun son literalining oktal sanoqda o'qilishi va `0177` ning o'nlikda 127 bo'lishi
- *The Java Language Specification, Java SE 25 Edition* (Gosling, Joy, Steele, Bracha, Buckley, Smith, Bierman), 4.2.2 (60-bet) - `int` ko'paytmasining 32 bitda bajarilishi va `long` ga tayinlash to'lib ketishdan saqlamasligi; `i = 1000000` uchun `i * i` ning -727379968 bo'lishi
- Boyarsky/Selikoff, *OCP Java SE 17 Study Guide*, 2-bob (78-bet) - `int` chegarasidan katta literalni `long` ga cast bilan tuzatib bo'lmasligi, chunki literal avval `int` deb o'qiladi; yechim `L` suffiksi
- Joshua Bloch, *Effective Java* 3rd, Item 22 (108-bet) - beshdan ko'p ketma-ket raqamli son literalida pastki chiziq ishlatish va guruhni asosga mos tanlash
- Joshua Bloch, *Effective Java* 3rd, Item 48 (225-bet) - bo'linadigan parallel oqimda `SplittableRandom` ishlatilishi, `ThreadLocalRandom` ning bitta thread uchun mo'ljallangani va `Random` ning har amalda sinxronlanib parallellikni yo'qotishi
- ESLATMA: 20.8 jadvalidagi ko'p threadli hisob uchun `ThreadLocalRandom` tavsiyasi va Bloch ning parallel oqim uchun `SplittableRandom` tavsiyasi qarama-qarshi ko'rinadi. Ikkisini ajratuvchi shart (generator bo'linishi kerakmi: har thread o'z oqimi bo'lsa `ThreadLocalRandom`, fork/join bilan bo'laklanadigan parallel oqimda `SplittableRandom`) korpus qo'shimchasi
- Joshua Bloch, *Effective Java* 3rd, Item 61 (275-bet) - boxed tur majburiy bo'ladigan uchta joy: to'plam elementi/kaliti/qiymati, parametrlangan tur argumenti va refleksiv metod chaqiruvi

- Joshua Bloch, *Effective Java* 3rd, Item 60 - `1.03 - 0.42` natijasi `0.6100000000000001`; to'qqiz raqamgacha `int`, o'n sakkizgacha `long`, undan ko'pi uchun `BigDecimal`
- Joshua Bloch, *Effective Java* 3rd, Item 61 - boxed turning uchta farqi va buzilgan `naturalOrder` solishtirgichi
- Joshua Bloch, *Effective Java* 3rd, Item 6 - keraksiz obyekt yaratmaslik, avtoboxing narxi
- [JLS 5.1.7, Boxing Conversion](https://docs.oracle.com/javase/specs/jls/se21/html/jls-5.html#jls-5.1.7) - `-128..127` oralig'ida bir xil obyekt qaytishi kafolati
- [Java API, `Math.floorMod`](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/lang/Math.html#floorMod(int,int)) - qoldiq belgisi bo'linuvchiga mos keladi
- [Java API, `BigDecimal.divide`](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/math/BigDecimal.html#divide(java.math.BigDecimal)) - aniq bo'linmasa `ArithmeticException`
- [Java API, `BigDecimal.equals`](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/math/BigDecimal.html#equals(java.lang.Object)) - scale ni ham solishtiradi, `compareTo` dan farqi
- Herbert Schildt, *Java The Complete Reference*, 3, 4-boblar - butun son arifmetikasi, bo'lish va qoldiq xatti-harakati
- Herbert Schildt, *Java The Complete Reference*, 12-nashr, McGraw Hill, 2022, 19-bob (516-517-betlar) - `isInfinite()` va `isNaN()` semantikasi; `1/0.` uchun `Infinity: true, false` va `0/0.` uchun `NaN: false, true` chiqishi
- [Java API, `Double.equals`](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/lang/Double.html#equals(java.lang.Object)) - `equals` `NaN` ni o'ziga teng, `0.0` va `-0.0` ni teng emas deb hisoblashi, `==` bilan farqi
- [Java API, `Double.compare`](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/lang/Double.html#compare(double,double)) - `NaN` hamma qiymatdan katta, `-0.0` `0.0` dan kichik deb olinishi
- [Java API, `Double.isFinite`](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/lang/Double.html#isFinite(double)) - argument `NaN` ham, cheksiz ham bo'lmasa `true`
- *The Java Language Specification, Java SE 25 Edition* (Gosling, Joy, Steele, Bracha, Buckley, Smith, Bierman), 15.26.2 (720-bet) - `E1 op= E2` ning `E1 = (T) ((E1) op (E2))` ga tengligi va `short x = 3; x += 4.6;` natijasi `7`
- *The Java Language Specification, Java SE 25 Edition* (Gosling, Joy, Steele, Bracha, Buckley, Smith, Bierman), 5.1.3 (116-117-betlar) - toraytiruvchi konversiyaning 22 shakli, butun turlarda eng past bitlarning qolishi va belgi o'zgarishi, kasrdan butunga o'tishda nol tomon yaxlitlash, chegarada to'yish va `NaN` ning nolga aylanishi
- ESLATMA: `NaN` va `Infinity` ni REST javobi, JSON va baza ustuniga chiqarmaslik tavsiyasi shu korpusning qo'shimchasi; manbalar faqat til va API semantikasini beradi

---

[&larr; 19. Istisno mexanikasi va resurslar](19-istisno-mexanikasi-va-resurslar.md) · [Mundarija](README.md) · [21. Satr, matn va regex &rarr;](21-satr-matn-va-regex.md)
