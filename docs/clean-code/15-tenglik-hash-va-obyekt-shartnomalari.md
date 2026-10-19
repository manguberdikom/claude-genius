<!-- doc: clean-code | chapter: 15 | part: V. Obyekt, ma'lumot va holat -->

[Barcha hujjatlar](../../README.md) / [Toza kod qoidalari](README.md)

> Holat: tekshirilgan (2026-10-19). Manbalar bob oxirida.

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

`equals` ni override qilish esa har doim kerak emas, va to'rt holatda uni **yozmaslik** to'g'ri: sinf nusxasi tabiatan yakka va ikki nusxa mantiqan hech qachon teng bo'lmaydi (`Thread`), sinfdan mantiqiy tenglik umuman talab qilinmaydi, superclass allaqachon to'g'ri `equals` yozgan va u voris uchun ham amal qiladi, yoki sinf `private`/`package-private` va uning `equals` i hech qachon chaqirilmaydi. Oxirgi holatda metodni tasodifan chaqirilishdan to'sish ham mumkin: tanasi faqat `throw new AssertionError()` bo'ladi.

Izchillik qoidasi bitta qo'shimcha talabni yashiradi: `equals` faqat xotiradagi obyektlar ustida deterministik hisob bajarishi kerak va ishonchsiz resursga tayanmasligi lozim. Platformadagi qarshi namuna `java.net.URL`: uning `equals` i host nomining IP manzilini solishtiradi, ya'ni natija DNS javobiga va tarmoq holatiga bog'lanib qoladi. Shu sababli `URL` ni `Set` elementi yoki `Map` kaliti qilish xato; o'rniga `URI` ishlatiladi.

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

Ko'p maydonli sinfda `Objects.hash(a, b, c)` bir qatorda yoziladi va u to'g'ri ishlaydi, lekin tez emas: argumentlar massivga yig'iladi va primitivlar boxing dan o'tadi. Shu sababli issiq yo'lda yoki kalit sifatida ko'p ishlatiladigan sinfda hash qo'lda yoziladi (`31 * result + ...` shakli), o'zgarmas sinfda esa natijani keshlash mumkin. Keshlashda bitta ehtiyot bor: boshlang'ich qiymat (`0`) ko'p uchraydigan nusxaning haqiqiy hash i bo'lmasligi kerak, aks holda kesh hech qachon to'ldirilmaydi.

`31 * result + maydonHash` shaklidagi har bir bo'lagi tanlangan va sababi bor. Ko'paytirish natijani maydonlar **tartibiga** bog'laydi: ko'paytirishsiz faqat qo'shish qolsa, bir xil maydon qiymatlarining har qanday joylashuvi bir xil hash beradi va anagramma kabi yozuvlar bitta bucket ga tushadi. Ko'paytuvchi toq tub son qilib olinadi: juft son bo'lsa va ko'paytirish to'lib ketsa ma'lumot yo'qoladi, chunki ikkiga ko'paytirish siljitishga teng. 31 ning qo'shimcha qulayligi: `31 * i` ni `(i << 5) - i` ga aylantirish mumkin va JVM shu optimallashtirishni qiladi. Primitiv maydon uchun o'rash sinfining statik metodi ishlatiladi (`Integer.hashCode(f)`, `Long.hashCode(f)`, `Double.hashCode(f)`), shunda boxing bo'lmaydi; massiv maydoni uchun `Arrays.hashCode`.

Hash funksiyasining sifati kalitning qancha bitidan foydalanishiga bog'liq: faqat pastki bitlarga tayangan funksiya ma'lumotdagi naqshni to'g'ridan-to'g'ri to'qnashuvga aylantiradi, chunki jadval o'lchami ikki darajasi bo'lganda indeks aynan pastki bitlardan olinadi. `HashMap` ning o'zi shu sababli `hashCode` natijasini to'g'ridan-to'g'ri ishlatmaydi: yuqori bitlarni pastga tarqatuvchi qo'shimcha amal qo'llaydi. Bu himoya cheklangan, shuning uchun o'z `hashCode` ida ham kalitning hamma ahamiyatli bo'lagi ishtirok etishi kerak.

Shartnomaning ikkinchi tomoni ham bor: `hashCode` natijasi **bitta ishga tushish** ichida izchil bo'lishi shart, lekin ikki ishga tushish orasida bir xil bo'lishi shart emas va platforma buni ataylab kafolatlamaydi. Shuning uchun hash qiymatini bazaga, faylga yoki keshga yozib keyingi ishga tushishda qayta ishlatish xato: JVM versiyasi yoki `String` hash ining ichki tafsiloti o'zgarsa, saqlangan qiymat mos kelmay qoladi. Barqaror kalit kerak bo'lsa, o'zingiz hujjatlashtirgan funksiya yoziladi (masalan kanonik satrdan SHA-256) va u `hashCode` dan alohida metod bo'ladi.

Shu yerdan API qoidasi kelib chiqadi: `hashCode` qaytaradigan **aniq qiymatni hujjatlashtirmang**. Hujjatlashtirsangiz, klient unga tayanadi va keyingi relizda hash funksiyasini yaxshilash (to'qnashuvni kamaytirish) buzuvchi o'zgarishga aylanadi. Javadoc da faqat shartnoma yoziladi: natija qaysi maydonlardan hisoblanishi, aniq formula emas.

Teskari tomoni ham qoida: **ahamiyatli maydonni hash hisobidan tezlik uchun chiqarib tashlash xato**. Hash tezlashadi, lekin sifati tushadi: faqat chiqarib tashlangan maydon bilan farq qiladigan nusxalar bir xil hash oladi va `HashMap` chiziqli vaqtdan kvadratik vaqtga o'tadi. `equals` da solishtirilgan maydonlar to'plami hash da ham bo'ladi (ortiqcha, ya'ni `equals` da ishlatilmaydigan maydon esa hash ga kirmaydi).

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

Maydon turiga qarab solishtirish usuli o'zgaradi va ikki tur istisno talab qiladi. `float` va `double` maydonlarni `==` bilan solishtirish xato: `Float.compare(a, b)` va `Double.compare(a, b)` ishlatiladi, chunki `==` `NaN` ni o'ziga teng emas deb beradi va `0.0` bilan `-0.0` ni teng deb beradi, ikkisi ham `equals` shartnomasini buzadi. `Float.equals(other.field)` ham ishlaydi, lekin har solishtirishda boxing beradi, shuning uchun issiq yo'lda `compare` afzal. Massiv maydoni uchun `Arrays.equals`, obyekt maydoni uchun `Objects.equals` (`null` bo'lishi mumkin bo'lsa).

```java
// yomon: NaN o'ziga teng bo'lmaydi, -0.0 bilan 0.0 teng bo'lib qoladi
return rate == other.rate;

// yaxshi
return Float.compare(rate, other.rate) == 0;
```

Pattern o'zgaruvchining nomi ham tanlanadi, chunki u maydonni **soya qiladi** (shadowing): `o instanceof Payment amount` yozilsa, blok ichida `amount` maydon emas, pattern o'zgaruvchisi bo'ladi va kod jim boshqa narsani solishtiradi. Konvensiya shu sababli bitta: pattern o'zgaruvchi `other` deb nomlanadi va maydon nomlari bilan to'qnashmaydi.

Eng oson va eng xavfsiz yechim esa - `record` ishlatish: `equals`, `hashCode` va `toString` avtomatik generatsiya qilinadi va shartnomaga mos bo'ladi ([arxitektor hujjatidagi](../architect/README.md) record bo'limi).

## 15.4 Vorislik ostida tenglik: `getClass()` yoki `instanceof`

Bu klassik dilemma. `getClass() != o.getClass()` tekshiruvi simmetriklikni saqlaydi, lekin Liskov printsipini buzadi: voris sinf nusxasi hech qachon bazaviy sinf nusxasiga teng bo'lmaydi (Hibernate proxy bilan muammo shu yerdan keladi). `instanceof` esa Liskov ni saqlaydi, lekin voris sinf yangi maydon qo'shsa simmetriklik buziladi.

Amaliy yechim: **tenglik kerak bo'lgan sinflarni `final` qilish** yoki `record` ishlatish. Vorislik va qiymat tengligi birga yashamaydi; kerak bo'lsa kompozitsiya ishlatiladi (17.9).

Dilemmaning bitta qonuniy istisnosi bor: **abstrakt** sinfning vorisiga qiymat maydoni qo'shish `equals` shartnomasini buzmaydi. Sabab mexanik: superclass nusxasini bevosita yaratish mumkin emas, demak "yangi maydoni bor voris" va "yalang'och superclass" juftligi hech qachon solishtirilmaydi va simmetriklik buziladigan holat tug'ilmaydi. Shuning uchun qiymat ierarxiyasi kerak bo'lganda ildiz instantiate qilinmaydigan qilinadi (teglangan sinf o'rniga ierarxiya shu yo'lda quriladi, 17.10).

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

Uchinchi holat ham bor va u ikkisidan ham arzon: **nusxa nazoratli** (instance-controlled) o'zgarmas sinf. Agar sinf har bir mantiqiy qiymat uchun ko'pi bilan bitta nusxa yaratilishini kafolatlasa, `a.equals(b)` faqat `a == b` bo'lganda `true` beradi va `equals` ni yozish umuman kerak bo'lmaydi: `Object` dan merosdagi ayniylik (identity) tengligi to'g'ri javob beradi. `enum` aynan shu kafolatni beradi, shuning uchun enum ustida `==` ishlatish nafaqat ruxsat, balki afzal shakl. Xuddi shu kafolatni statik fabrika va ichki kesh bilan o'z sinfingizda ham qurish mumkin, lekin unda kafolat hujjatlashtiriladi, aks holda klient `equals` ni kutadi.
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

`compareTo` ning `equals` dan ikkita farqi bor va ikkisi ham qoidaga aylanadi. Birinchi: `compareTo` turlar bo'ylab ishlashi **shart emas**. `equals` boshqa turdagi argument uchun `false` qaytarishi kerak, `compareTo` esa mos kelmagan tur uchun `ClassCastException` tashlashi mumkin va odatda shunday qiladi (parametri `Comparable<T>` bo'lgani uchun kompilyator ko'p holatni o'zi to'sadi). Ikkinchi: izchillikning buzilishi **hujjatlashtiriladi**. `compareTo` tartibi `equals` bilan izchil bo'lmasa, Javadoc da shu ochiq yoziladi, platformadagi shakl bilan: "Bu sinfning tabiiy tartibi `equals` bilan izchil emas". Yozilmasa, sinfni `TreeSet` ga qo'ygan odam yozuv yo'qolishiga tushuntirish topa olmaydi.

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

To'rtinchi talab qaror shaklida keladi: **formatni hujjatlashtirish yoki hujjatlashtirmaslik**, va ikkisining ham narxi bor. Formatni hujjatlashtirsangiz, u API ga aylanadi: klient unga tayanib parslaydi, satr yozadi va saqlaydi, shundan keyin formatni o'zgartirish buzuvchi o'zgarish bo'lib qoladi. Platformada shu yo'ldan ketgan sinflar bor (`BigInteger`, `BigDecimal` kabi qiymat sinflari) va ular formatini endi o'zgartira olmaydi. Hujjatlashtirmasangiz, formatni erkin o'zgartirasiz, lekin klient uni baribir parslashga urinadi va o'zgarish paytida yiqiladi. Shuning uchun qaror ongli qabul qilinadi va **Javadoc da aytiladi**: format belgilanganmi yoki belgilanmaganmi.

Qarorning qaysi tomoni tanlanganidan qat'i nazar bitta majburiy qism bor: `toString` ko'rsatadigan har bir ma'lumotga **programmatik kirish** (accessor) berilishi kerak. Accessor bo'lmasa, klient uchun satrni parslash yagona yo'l bo'lib qoladi va format hujjatlashtirilmagan bo'lsa ham de-fakto API ga aylanadi.

```java
// Format belgilangan: hujjatda yozilgan, demak barqaror va parslanishi mumkin
/**
 * IBAN ning guruhlangan ko'rinishini qaytaradi, format "UZ00 XXXX ...".
 * Bu format barqaror; qismlariga {@link #countryCode()} va
 * {@link #checksum()} bilan ham kirish mumkin.
 */
@Override public String toString() { ... }

// Format belgilanmagan: o'zgarishi mumkinligi oshkor aytilgan
/**
 * Buyurtmaning diagnostika uchun qisqa ko'rinishi. Format belgilanmagan
 * va relizlar orasida o'zgarishi mumkin, shuning uchun parslanmaydi:
 * qiymatlar {@link #id()} va {@link #status()} bilan olinadi.
 */
@Override public String toString() { ... }
```

`toString` har sinfda kerak ham emas. Statik utility sinfda u ma'nosiz (nusxasi bo'lmaydi), ko'pchilik `enum` turida platforma bergan ko'rinish (konstanta nomi) yetarli. Aksincha, vorislari umumiy satr ko'rinishiga ega abstrakt sinfda `toString` bir marta ildizda yoziladi, shunda har voris uni qaytarmaydi.

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

Ikki holatda `clone` ni baribir yozishga to'g'ri keladi: `Cloneable` ni allaqachon amalga oshirgan sinfni qo'llab-quvvatlashda, va `clone` ni kutadigan tashqi API bilan ishlashda. O'shanda protokol qat'iy. Qaytariladigan obyekt **`super.clone()` dan** olinadi, konstruktor bilan yasalmaydi: konstruktor bilan yasalsa, voris sinf `super.clone()` ni chaqirganda noto'g'ri turdagi obyekt qaytadi va voris `clone` i jim buziladi. `super.clone()` dan kelgan obyektda keyin o'zgaradigan maydonlar chuqur nusxalanadi, chunki `Object.clone` faqat maydonlarni baytma-bayt ko'chiradi va ikki nusxa bitta ichki ro'yxatga ishora qilib qoladi. `final` maydonga `clone` ichida yangi qiymat yozib bo'lmaydi, shuning uchun chuqur nusxa talab qiladigan maydon `final` bo'la olmaydi: bu `Cloneable` ning o'zgarmaslik bilan sig'ishmasligining asosiy sababi.

```java
// Qo'llab-quvvatlash kerak bo'lganda: super.clone() dan boshlash shart
@Override
public Stack clone() {
    try {
        Stack result = (Stack) super.clone();   // tur to'g'ri, voris uchun ham
        result.elements = elements.clone();     // o'zgaradigan maydon chuqur nusxalanadi
        return result;
    } catch (CloneNotSupportedException e) {
        throw new AssertionError(e);            // Cloneable amalga oshirilgan, bo'lmaydi
    }
}
```

`clone` ning yagona shubhasiz to'g'ri ishlatilishi - **massiv**. `array.clone()` turni saqlaydi, bir qatorda yoziladi va massivni nusxalashning eng yaxshi yo'li; `Arrays.copyOf` esa o'lchamni o'zgartirish kerak bo'lganda ishlatiladi. Massiv maydonni getterda yoki konstruktorda himoyalangan nusxa qilish ham shu yo'l bilan bajariladi ([himoyalangan nusxa](14-obyekt-va-malumot-tuzilmasi-inkapsulyatsiya.md#147-ichki-toplamni-oshkor-qilish-va-himoyalangan-nusxa)).
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

Quruvchi zanjirining bitta amaliy tuzog'i bor: primitiv variantlarda (`comparingInt`, `comparingLong`, `comparingDouble`) **birinchi** lambda ning parametr turi oshkor yozilishi kerak, aks holda tur xulosasi (type inference) yetmaydi va kod kompilyatsiya bo'lmaydi. Keyingi `thenComparingInt` bo'g'inlarida bu kerak emas, chunki o'shanda tur zanjirdan ma'lum bo'ladi. Metod havolasi (`Order::amount`) ishlatilganda ham muammo tug'ilmaydi, shuning uchun eng oson yechim - lambda o'rniga metod havolasi.

```java
// kompilyatsiya bo'lmaydi: birinchi lambda parametrining turi noma'lum
Comparator<Order> byAmount = comparingInt(o -> o.amount());

// yaxshi: tur oshkor
Comparator<Order> byAmount = comparingInt((Order o) -> o.amount());

// eng yaxshi: metod havolasi
Comparator<Order> byAmount = comparingInt(Order::amount);
```

Uchinchi qoida solishtirgichdan emas, saralash algoritmidan keladi: **barqaror
saralash** (stable sort). Barqaror saralash teng kalitli elementlarning
bir-biriga nisbatan tartibini saqlaydi, ya'ni kirishda oldin kelgan element
chiqishda ham oldin turadi (Cormen va boshqalar, *Introduction to Algorithms*,
3-nashr, MIT Press, 2009, 8.2-bo'lim (196-bet)). Bu xususiyat ko'p maydonli
saralashning eng arzon shaklini beradi: sanani, so'ng oyni, so'ng yilni
barqaror saralash bilan uch marta saralash bir martada uchta kalitni
solishtiradigan funksiya bilan saralash bilan bir xil natija beradi (shu yerda,
8.3-bo'lim (198-bet)).

Java da kafolat API ga bog'liq va bu farq hujjatlashtirilgan.

| Chaqiruv | Barqarormi | Izoh |
|---|---|---|
| `Collections.sort(list)`, `list.sort(cmp)` | ha, kafolatlangan | teng elementlar qayta tartiblanmaydi |
| `Arrays.sort(T[])`, `Arrays.sort(T[], cmp)` | ha, kafolatlangan | obyekt massivi uchun merge sort |
| `stream.sorted()` | tartiblangan oqimda ha | tartibsiz (unordered) oqimda kafolat yo'q |
| `Arrays.sort(int[])` va boshqa primitiv massivlar | kafolat yo'q | quicksort variantida teng elementlar joyini almashtiradi |

Primitiv massiv qatori amalda zararsiz: teng `int` lar bir-biridan farq
qilmaydi, shuning uchun ularning tartibi ko'rinmaydi. Qoida obyektlar
saralanganda ishlaydi va ikki joyda qimmatga tushadi. Birinchi: ko'p maydonli
saralashni ikki qadamda qilish (`sort` ni ikki marta chaqirish) faqat barqaror
API da to'g'ri ishlaydi; `thenComparing` zanjiri esa barqarorlikka tayanmaydi va
shu sababli afzal. Ikkinchi: sahifalash. Tartib to'liq emas bo'lsa (teng
kalitlar bor), ketma-ket sahifalar bir elementni ikki marta berishi yoki butunlay
tushirib qoldirishi mumkin, chunki ikki so'rov orasida tartib bir xil
bo'lishi kafolatlanmaydi. Bu ayniqsa bazada saralashda muhim: SQL `ORDER BY`
barqaror emas, demak sahifalangan so'rovda tartib yagona (unique) ustun bilan
to'ldiriladi.

```java
// yomon: tartib to'liq emas, sahifalar orasida element sakrab ketadi
Page<Order> page = repository.findAll(PageRequest.of(n, 20, Sort.by("createdAt")));

// yaxshi: oxirgi kalit yagona, tartib to'liq va qaytariladigan
Page<Order> page = repository.findAll(
        PageRequest.of(n, 20, Sort.by("createdAt").descending().and(Sort.by("id"))));

// yaxshi: xotirada ham tartib bir chaqiruvda to'liq aytiladi
orders.sort(comparing(Order::createdAt).reversed().thenComparing(Order::id));
```

## 15.11 Amalda qo'llash

- [ ] `equals` yozilgan barcha sinflarda `hashCode` ham borligini Checkstyle `EqualsHashCode` bilan majburiy qiling.
- [ ] Value object larni `record` ga o'tkazib, qo'lda yozilgan `equals`/`hashCode` ni o'chiring.
- [ ] Tenglik kerak bo'lgan sinflarni `final` qilib, vorislik ostidagi simmetriklik muammosini yo'qoting.
- [ ] JPA entitetlarida tenglikni identifikator bo'yicha yozib, `hashCode` ni barqaror qiling (28.1).
- [ ] `Comparable` amalga oshirilgan sinflarda `compareTo` va `equals` izchilligini test bilan tekshiring.
- [ ] Barcha `toString` larni ko'rib, sezgir maydonlarni maskalang va lazy assotsiatsiyalarni olib tashlang.
- [ ] `Cloneable` ishlatilgan joylarni nusxa konstruktori yoki o'zgarmas turga o'tkazing.
- [ ] `Map` kaliti va `Set` elementi sifatida ishlatilgan o'zgaradigan turlarni topib, o'zgarmas turga almashtiring.

## Manbalar

- Joshua Bloch, *Effective Java* 3rd, Item 1 (6-bet) - nusxa nazoratli o'zgarmas sinfda `a.equals(b)` faqat `a == b` bo'lganda bajarilishi va `enum` shu kafolatni berishi
- Joshua Bloch, *Effective Java* 3rd, Item 10 - `equals` shartnomasining besh qoidasi, `CaseInsensitiveString` simmetriklik buzilishi, qiymat komponentini vorislik bilan qo'shib bo'lmasligi
- Joshua Bloch, *Effective Java* 3rd, Item 10 (37-bet) - `equals` ni override qilmaslik to'g'ri bo'ladigan to'rt holat
- Joshua Bloch, *Effective Java* 3rd, Item 10 (45-bet) - abstrakt sinf vorisiga qiymat maydoni qo'shish shartnomani buzmasligi va `equals` ning ishonchsiz resursga tayanmasligi (`java.net.URL` ning DNS ga bog'langan `equals` i)
- Joshua Bloch, *Effective Java* 3rd, Item 10 (47-bet) - `float` va `double` maydonlarni `Float.compare`/`Double.compare` bilan solishtirish, `Float.equals` ning boxing narxi
- Joshua Bloch, *Effective Java* 3rd, Item 11 - `hashCode` shartnomasi, `Objects.hash` ning narxi, hash ni keshlash va ahamiyatli maydonni chiqarib tashlamaslik
- Joshua Bloch, *Effective Java* 3rd, Item 11 (50-bet) - `hashCode` bitta ishga tushish ichida izchil bo'lishi, ishga tushishlar orasida esa bir xil bo'lishi shart emasligi
- Joshua Bloch, *Effective Java* 3rd, Item 11 (52-bet) - 31 ning toq tub son qilib tanlanishi, ko'paytirishning natijani maydon tartibiga bog'lashi va `31 * i` ning `(i << 5) - i` ga aylanishi
- Joshua Bloch, *Effective Java* 3rd, Item 11 (54-bet) - `hashCode` qaytaradigan aniq qiymatni hujjatlashtirmaslik, aks holda hash funksiyasini keyingi relizda yaxshilash imkoni yo'qolishi
- Thomas H. Cormen, Charles E. Leiserson, Ronald L. Rivest, Clifford Stein, *Introduction to Algorithms*, 3-nashr, MIT Press, 2009, 11.3-bo'lim (263-bet) - hash funksiyasi kalitning hamma bitidan foydalanishi talabi va faqat pastki bitlarga tayangan funksiyaning ma'lumotdagi naqshni to'qnashuvga aylantirishi
- Joshua Bloch, *Effective Java* 3rd, Item 12 (57-bet) - `toString` da nimani ko'rsatish, formatni hujjatlash qarorining ikki tomoni va format qanday bo'lsa ham `toString` dagi ma'lumotga accessor berish talabi
- Joshua Bloch, *Effective Java* 3rd, Item 12 (57-bet) - statik utility sinfda va ko'pchilik `enum` turida `toString` yozish keraksizligi, umumiy satr ko'rinishiga ega abstrakt sinfda esa yozilishi
- Joshua Bloch, *Effective Java* 3rd, Item 13 - `clone` dan voz kechish va nusxa konstruktori
- Joshua Bloch, *Effective Java* 3rd, Item 13 (59-bet) - `clone` qaytaradigan obyekt `super.clone()` dan olinishi sharti va konstruktor bilan yasalganda voris sinfning buzilishi
- Joshua Bloch, *Effective Java* 3rd, Item 13 (65-bet) - massivni nusxalashning eng yaxshi yo'li `clone` bo'lishi va bu `clone` ning yagona shubhasiz ishlatilishi
- Joshua Bloch, *Effective Java* 3rd, Item 14 - `compareTo` shartnomasi va `BigDecimal("1.0")` ning `HashSet` va `TreeSet` dagi farqi
- Joshua Bloch, *Effective Java* 3rd, Item 14 (67-bet) - `compareTo` ning turlar bo'ylab ishlashi shart emasligi, mos kelmagan tur uchun `ClassCastException` tashlashi va `equals` bilan izchil emasligini hujjatlash talabi
- Joshua Bloch, *Effective Java* 3rd, Item 14 (70-bet) - `comparingInt` zanjirida birinchi lambda parametrining turi oshkor yozilmasa tur xulosasi yetmasligi
- [JEP 394: Pattern Matching for instanceof](https://openjdk.org/jeps/394) - pattern o'zgaruvchining qamrovi va uning bir xil nomli maydonni soya qilishi
- Joshua Bloch, *Effective Java* 3rd, Item 40 - `@Override` imzo xatosini ushlashi
- [Java API, `Object.hashCode`](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/lang/Object.html#hashCode()) - teng obyektlar bir xil hash qaytarishi talabi
- [Hibernate User Guide, equals/hashCode](https://docs.jboss.org/hibernate/orm/6.6/userguide/html_single/Hibernate_User_Guide.html#entity-pojo-equals-hashcode) - entitetda identifikator bo'yicha tenglik va proxy bilan `instanceof`
- Thomas H. Cormen, Charles E. Leiserson, Ronald L. Rivest, Clifford Stein, *Introduction to Algorithms*, 3-nashr, MIT Press, 2009, 8.2-bo'lim (196-bet) - barqaror saralash ta'rifi: teng qiymatli elementlar chiqishda kirishdagi tartibda turishi va bu xususiyat satellit ma'lumot bo'lganda ahamiyatli bo'lishi
- Thomas H. Cormen, Charles E. Leiserson, Ronald L. Rivest, Clifford Stein, *Introduction to Algorithms*, 3-nashr, MIT Press, 2009, 8.3-bo'lim (198-bet) - ko'p kalitli yozuvlarni (kun, oy, yil) barqaror saralash bilan uch marta saralash bir martada uch kalitni solishtirishga teng kelishi
- [Java API, `Collections.sort`](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/Collections.html#sort(java.util.List)) - saralash barqarorligi kafolati: teng elementlar qayta tartiblanmaydi
- [Java API, `Arrays.sort(T[], Comparator)`](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/Arrays.html#sort(T%5B%5D,java.util.Comparator)) - obyekt massivi uchun barqarorlik kafolati
- [Java API, `Stream.sorted`](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/stream/Stream.html#sorted(java.util.Comparator)) - tartiblangan oqimda saralash barqaror bo'lishi

---

[&larr; 14. Obyekt va ma'lumot tuzilmasi: inkapsulyatsiya](14-obyekt-va-malumot-tuzilmasi-inkapsulyatsiya.md) · [Mundarija](README.md) · [16. O'zgarmaslik va holat boshqaruvi kod darajasida &rarr;](16-ozgarmaslik-va-holat-boshqaruvi-kod.md)
