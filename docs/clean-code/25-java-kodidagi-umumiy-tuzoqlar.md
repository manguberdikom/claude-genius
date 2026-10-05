<!-- doc: clean-code | chapter: 25 | part: VII. Java tilining toza ishlatilishi -->

[Barcha hujjatlar](../../README.md) / [Toza kod qoidalari](README.md)

> Holat: AI yozgan, inson tekshirmagan.

# 25. Java kodidagi umumiy tuzoqlar (Common Java Pitfalls)

<details>
<summary>Bu bobdagi 11 bo'lim</summary>

- [25.1 `Optional` maydon, parametr va seriyalash](#251-optional-maydon-parametr-va-seriyalash)
- [25.2 Statik ishga tushirish tartibi va sinf yuklanishi](#252-statik-ishga-tushirish-tartibi-va-sinf-yuklanishi)
- [25.3 `instanceof` zanjiri va `getClass()` solishtirish](#253-instanceof-zanjiri-va-getclass-solishtirish)
- [25.4 Seriyalash: `serialVersionUID`, `readObject` va undan qochish](#254-seriyalash-serialversionuid-readobject-va-undan-qochish)
- [25.5 Refleksiya narxi va uni chegaralash](#255-refleksiya-narxi-va-uni-chegaralash)
- [25.6 `finalize`, `Cleaner` va resurs oxiri](#256-finalize-cleaner-va-resurs-oxiri)
- [25.7 Ichki sinf va yashirin tashqi havola](#257-ichki-sinf-va-yashirin-tashqi-havola)
- [25.8 Anonim sinf va lambda tanlovi](#258-anonim-sinf-va-lambda-tanlovi)
- [25.9 `enum` da xatti-harakat, `EnumMap`, `EnumSet`, `valueOf`](#259-enum-da-xatti-harakat-enummap-enumset-valueof)
- [25.10 Kompilyator ogohlantirishlari: `-Xlint`, `-Werror`, Error Prone, NullAway](#2510-kompilyator-ogohlantirishlari--xlint--werror-error-prone-nullaway)
- [25.11 Amalda qo'llash](#2511-amalda-qollash)

</details>


Bu bob oldingi boblarga sig'magan, lekin kundalik kodda uchraydigan Java tuzoqlarini yig'adi: `Optional` ning chegaralari, statik ishga tushirish, seriyalash, refleksiya, ichki sinflar, enum mexanikasi va kompilyator ogohlantirishlari.

## 25.1 `Optional` maydon, parametr va seriyalash

`Optional` qaytish qiymati uchun mo'ljallangan. Maydon sifatida ishlatish uch muammo keltiradi: `Optional` `Serializable` emas, har bir obyekt uchun qo'shimcha o'ram yaratiladi, va JPA/Jackson bilan muammo chiqadi.

```java
// yomon: Optional maydon
public class Order {
    private Optional<Discount> discount;      // Serializable emas, JPA bilan ishlamaydi
}

// yaxshi: maydon null bo'lishi mumkin, getter Optional qaytaradi
public class Order {

    private Discount discount;                // null bo'lishi mumkin

    public Optional<Discount> discount() { return Optional.ofNullable(discount); }
}

// yomon: Optional parametr - chaqiruv joyi shovqinli
void apply(Order order, Optional<Discount> discount);
apply(order, Optional.empty());

// yaxshi: overload (5.9)
void apply(Order order);
void apply(Order order, Discount discount);
```

## 25.2 Statik ishga tushirish tartibi va sinf yuklanishi

Statik initializator (`static { }`) sinf birinchi marta ishlatilganda bajariladi va uning vaqti oldindan aniq emas. Agar unda tashqi resursga murojaat bo'lsa (fayl, baza, tarmoq), xato kutilmagan joyda `ExceptionInInitializerError` sifatida chiqadi va diagnostikasi qiyin bo'ladi.

```java
// yomon: statik blokda I/O - xato ExceptionInInitializerError bo'lib chiqadi
public class TaxRates {
    private static final Map<Region, BigDecimal> RATES;
    static {
        RATES = loadFromDatabase();      // qachon bajariladi - aniq emas
    }
}

// yaxshi: yuklash oshkor, boshqariladigan joyda (Spring bean, lazy supplier)
@Component
public class TaxRates {

    private final Map<Region, BigDecimal> rates;

    TaxRates(TaxRateRepository repository) {
        this.rates = Map.copyOf(repository.loadAll());    // konteyner boshqaradi
    }
}
```

Statik maydonlarning ishga tushish tartibi e'lon tartibida boradi va bu tartibga bog'lanish nozik xato beradi: pastda e'lon qilingan maydon yuqoridagi initializatorda `null` bo'ladi.

## 25.3 `instanceof` zanjiri va `getClass()` solishtirish

Uzun `instanceof` zanjiri turga qarab shoxlanish hidi (6.10) va zamonaviy Java da uning to'g'ri shakli bor: `sealed` interfeys va pattern matching bilan `switch`, bunda to'liqlik kompilyator tomonidan tekshiriladi ([arxitektor hujjatidagi](../architect/README.md) sealed interfeys bo'limi).

```java
// yomon: zanjir, to'liqligi tekshirilmaydi
if (event instanceof PaymentSettled s) { ... }
else if (event instanceof PaymentRejected r) { ... }
else { throw new IllegalStateException("noma'lum hodisa"); }

// yaxshi: sealed + switch - yangi tur qo'shilsa kompilyator eslatadi
sealed interface PaymentEvent permits PaymentSettled, PaymentRejected, PaymentRefunded { }

String describe(PaymentEvent event) {
    return switch (event) {
        case PaymentSettled s -> "yopildi: " + s.amount();
        case PaymentRejected r -> "rad etildi: " + r.reason();
        case PaymentRefunded f -> "qaytarildi: " + f.amount();
    };
}
```

## 25.4 Seriyalash: `serialVersionUID`, `readObject` va undan qochish

Java seriyalash mexanizmi (`Serializable`) xavfsizlik nuqsonlari va moslik muammolari manbai: deseriyalash konstruktorni chetlab o'tadi (invariant tekshirilmaydi), va ishonchsiz ma'lumotni deseriyalash masofadan kod bajarilishiga olib keladi.

Qoida: yangi kodda `Serializable` ishlatmaslik. Ma'lumot almashish uchun JSON yoki Protobuf; kesh uchun ham seriyalanadigan format tanlanadi.

```java
// Agar Serializable majbur bo'lsa (legacy, RMI, HttpSession):
public final class SessionData implements Serializable {

    // Versiya oshkor: aks holda sinf o'zgarganda deseriyalash buziladi
    private static final long serialVersionUID = 1L;

    // Sezgir maydon seriyalanmaydi
    private transient String accessToken;

    // Invariant deseriyalashdan keyin ham tekshiriladi
    private void readObject(ObjectInputStream in) throws IOException, ClassNotFoundException {
        in.defaultReadObject();
        if (userId == null) throw new InvalidObjectException("userId bo'sh");
    }
}
```

## 25.5 Refleksiya narxi va uni chegaralash

Refleksiya tur xavfsizligini ish vaqtiga suradi: xato kompilyatsiyada emas, production da chiqadi. Bundan tashqari, refleksiya bilan yozilgan kod refaktoringga chidamsiz - nom o'zgarsa IDE uni topmaydi.

```java
// yomon: nom satrda - refaktoring buzadi, xato ish vaqtida chiqadi
Method method = service.getClass().getMethod("settle", Long.class);
method.invoke(service, paymentId);

// yaxshi: interfeys yoki funksional tur
PaymentOperation operation = service::settle;
operation.apply(paymentId);
```

Refleksiya haqli joylar: framework ichida (Spring, Jackson, JPA), test yordamchilarida, va plugin yuklashda. Biznes kodida esa deyarli har doim boshqa yechim bor.

## 25.6 `finalize`, `Cleaner` va resurs oxiri

`Object.finalize()` Java 9 dan deprecated va Java 18 dan o'chirilish yo'lida: uning bajarilishi kafolatlanmaydi, vaqti aniq emas, va GC ni sekinlashtiradi. `Cleaner` esa faqat **oxirgi himoya** sifatida haqli.

Qoida: resursni `AutoCloseable` va `try-with-resources` bilan boshqarish (19.4); `Cleaner` ni faqat native resurs (JNI buferi) uchun qo'shimcha xavfsizlik to'ri sifatida ishlatish.

## 25.7 Ichki sinf va yashirin tashqi havola

Nostatik ichki sinf (`inner class`) tashqi sinf nusxasiga yashirin havola saqlaydi. Natijada ichki sinf nusxasi yashasa, tashqi obyekt ham xotirada qoladi - bu klassik xotira oqishi (memory leak) sababi.

```java
// yomon: Listener tashqi Service ga havola saqlaydi, u GC qilinmaydi
public class SettlementService {
    class Listener implements EventListener { ... }       // nostatik
}

// yaxshi: statik ichki sinf - yashirin havola yo'q
public class SettlementService {
    static final class Listener implements EventListener { ... }
}
```

Qoida: ichki sinf tashqi nusxaga murojaat qilmasa, u `static` bo'lishi kerak. Bu qoidani Error Prone `ClassCanBeStatic` qoidasi topadi.

## 25.8 Anonim sinf va lambda tanlovi

Lambda qisqa va `this` ni tashqi sinfga bog'laydi; anonim sinf esa o'z `this` iga ega va holat saqlashi mumkin. Tanlov qoidasi oddiy.

| Ehtiyoj | Tanlov |
|---|---|
| Bitta abstrakt metod, holat yo'q | lambda |
| Bir nechta metod | anonim sinf yoki nomlangan sinf |
| Holat kerak | nomlangan sinf |
| `this` o'ziga tegishli bo'lishi kerak | anonim sinf |
| Qayta ishlatiladi | nomlangan sinf |
| Uch qatordan uzun | nomlangan metod yoki sinf (24.1) |

## 25.9 `enum` da xatti-harakat, `EnumMap`, `EnumSet`, `valueOf`

Enum Java da oddiy konstanta to'plamidan ancha ko'proq: u xatti-harakat saqlashi mumkin (6.10) va o'ziga mos to'plamlari bor.

`EnumMap` va `EnumSet` oddiy `HashMap`/`HashSet` dan tez va kam xotira oladi, chunki ular massivga asoslangan. Enum kalit ishlatilganda ularni tanlash standart bo'lishi kerak.

```java
// yaxshi: EnumMap - tartib enum e'loni bo'yicha, tez
Map<SettlementStatus, Long> counts = new EnumMap<>(SettlementStatus.class);
Set<SettlementStatus> terminal = EnumSet.of(SETTLED, REJECTED);
```

`valueOf` tuzog'i: noma'lum nom uchun `IllegalArgumentException` tashlaydi va bu tashqi ma'lumotni parslaganda kutilmagan 500 xatoga olib keladi.

```java
// yomon: tashqi qiymat uchun IllegalArgumentException
SettlementStatus status = SettlementStatus.valueOf(input);

// yaxshi: xavfsiz parslash
static Optional<SettlementStatus> parse(String input) {
    return Arrays.stream(values())
            .filter(s -> s.name().equalsIgnoreCase(input))
            .findFirst();
}
```

## 25.10 Kompilyator ogohlantirishlari: `-Xlint`, `-Werror`, Error Prone, NullAway

Kompilyator eng arzon statik tahlilchi va u ko'pincha o'chirilgan holda qoldiriladi. Ogohlantirishlarni xatoga aylantirish eng yuqori foyda beradigan bir martalik sozlama.

```xml
<plugin>
  <artifactId>maven-compiler-plugin</artifactId>
  <configuration>
    <compilerArgs>
      <!-- Barcha ogohlantirishlar yoqilgan va xatoga aylantirilgan -->
      <arg>-Xlint:all</arg>
      <arg>-Werror</arg>
      <!-- Parametr nomlari saqlanadi: Spring va Jackson uchun kerak -->
      <arg>-parameters</arg>
      <!-- Error Prone va NullAway ulanishi -->
      <arg>-XDcompilePolicy=simple</arg>
      <arg>--should-stop=ifError=FLOW</arg>
      <arg>-Xplugin:ErrorProne -Xep:NullAway:ERROR -XepOpt:NullAway:AnnotatedPackages=uz.shop</arg>
    </compilerArgs>
    <annotationProcessorPaths>
      <path>
        <groupId>com.google.errorprone</groupId>
        <artifactId>error_prone_core</artifactId>
        <version>2.42.0</version>
      </path>
      <path>
        <groupId>com.uber.nullaway</groupId>
        <artifactId>nullaway</artifactId>
        <version>0.12.10</version>
      </path>
    </annotationProcessorPaths>
  </configuration>
</plugin>
```

Error Prone bu hujjatdagi ko'p qoidalarni avtomatik tekshiradi: `EqualsHashCode`, `Finally`, `ClassCanBeStatic`, `StringSplitter`, `DefaultCharset`, `JavaUtilDate`, `BigDecimalEquals`, `UnusedVariable` (42.2).

## 25.11 Amalda qo'llash

- [ ] `Optional` tipidagi maydon va parametrlarni topib, maydonni `null` ga va getter ni `Optional` ga o'tkazing.
- [ ] Statik initializator ichidagi I/O va tashqi chaqiruvlarni bean konstruktoriga yoki lazy supplier ga ko'chiring.
- [ ] Uzun `instanceof` zanjirlarini `sealed` interfeys va `switch` pattern matching ga o'tkazing.
- [ ] `Serializable` ishlatilgan joylarni ro'yxatlab, yangi kodda taqiqlang; qolganlarida `serialVersionUID` va `transient` ni tekshiring.
- [ ] Biznes kodidagi refleksiyani interfeys yoki funksional turga almashtiring.
- [ ] Nostatik ichki sinflarni `static` qilib, Error Prone `ClassCanBeStatic` ni yoqing.
- [ ] `Enum.valueOf` tashqi ma'lumot bilan chaqirilgan joylarni xavfsiz parslashga o'tkazing.
- [ ] `-Xlint:all -Werror` va Error Prone + NullAway ni build ga qo'shib, chiqqan ogohlantirishlarni bosqichma-bosqich tuzating.

---

[&larr; 24. Lambda, oqim va funksional uslub tozaligi](24-lambda-oqim-va-funksional-uslub-tozaligi.md) · [Mundarija](README.md) · [26. Spring kodining tozaligi &rarr;](26-spring-kodining-tozaligi.md)
