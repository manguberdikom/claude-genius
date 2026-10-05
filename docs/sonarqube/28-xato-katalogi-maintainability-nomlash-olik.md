<!-- doc: sonarqube | chapter: 28 | part: VII. Xato katalogi: qanday kod qanday xato hisoblanadi -->

[Barcha hujjatlar](../../README.md) / [SonarQube](README.md)

# 28. Xato katalogi: maintainability, nomlash, o'lik kod va uslub (Catalog: Maintainability, Naming)

<details>
<summary>Bu bobdagi 17 bo'lim</summary>

- [28.1 Nomlash shabloniga mos kelmaydigan klass, metod, maydon va konstanta](#281-nomlash-shabloniga-mos-kelmaydigan-klass-metod-maydon-va-konstanta)
- [28.2 Bitta harfli va ma'nosiz nomlar](#282-bitta-harfli-va-manosiz-nomlar)
- [28.3 Ishlatilmaydigan import, maydon, parametr va mahalliy o'zgaruvchi](#283-ishlatilmaydigan-import-maydon-parametr-va-mahalliy-ozgaruvchi)
- [28.4 Ishlatilmaydigan private metod va o'lik kod](#284-ishlatilmaydigan-private-metod-va-olik-kod)
- [28.5 Kommentariyaga olingan kod bloki](#285-kommentariyaga-olingan-kod-bloki)
- [28.6 `TODO` va `FIXME` izohlari va ularning hisobi](#286-todo-va-fixme-izohlari-va-ularning-hisobi)
- [28.7 Eskirgan (deprecated) API ishlatish](#287-eskirgan-deprecated-api-ishlatish)
- [28.8 `public` maydon va kapsullashning buzilishi](#288-public-maydon-va-kapsullashning-buzilishi)
- [28.9 `final` qo'yilmagan o'zgarmas maydon](#289-final-qoyilmagan-ozgarmas-maydon)
- [28.10 Ortiqcha modifikator (interfeysda `public abstract`)](#2810-ortiqcha-modifikator-interfeysda-public-abstract)
- [28.11 Satr birlashtirishni sikl ichida bajarish](#2811-satr-birlashtirishni-sikl-ichida-bajarish)
- [28.12 Loglashda satr birlashtirish va formatlangan xabarga o'tish](#2812-loglashda-satr-birlashtirish-va-formatlangan-xabarga-otish)
- [28.13 Ortiqcha `toString` va `String.valueOf` chaqiruvi](#2813-ortiqcha-tostring-va-stringvalueof-chaqiruvi)
- [28.14 Bir xil ishni bajaradigan ikkita metod](#2814-bir-xil-ishni-bajaradigan-ikkita-metod)
- [28.15 Oddiy yondashuv va arxitektor yondashuvi](#2815-oddiy-yondashuv-va-arxitektor-yondashuvi)
- [28.16 Tuzoqlar va yechimlar](#2816-tuzoqlar-va-yechimlar)
- [28.17 Amalda qo'llash](#2817-amalda-qollash)

</details>



Bu bob Sonar hisobotida eng ko'p uchraydigan, lekin eng arzon tuzatiladigan shikoyatlar katalogi. Bu yerdagi deyarli hamma narsa `maintainability` toifasiga tushadi, ya'ni code smell, va ko'pchiligi dastur ishlashiga bugun ta'sir qilmaydi. Shuning uchun ularni e'tiborsiz qoldirish oson, keyin esa ular technical debt ratio va `Maintainability Rating` orqali quality gate ni yiqitadi. Katalog Spring servis va repository klasslari ustida qurilgan, chunki real loyihada bu shikoyatlarning asosiy qismi aynan shu ikki qatlamda yig'iladi.

| Kod holati | Sonar nima deydi | Toifa | Jiddiylik (taxminan) | Ta'siri |
|---|---|---|---|---|
| `class payment_service` | klass nomi nomlash shablonga mos emas (`java:S101`) | maintainability | minor | Kod bazasi bo'ylab nom izlash qiyinlashadi |
| `void Process_Payment()` | metod nomi shablonga mos emas (`java:S100`) | maintainability | minor | IDE va code review da shovqin |
| `static final int maxRetry` | konstanta nomi shablonga mos emas (`java:S115`) | maintainability | minor | Konstanta o'zgaruvchidan ajralmaydi |
| `private String Customer_Id` | maydon nomi shablonga mos emas (`java:S116`) | maintainability | minor | Qatlamlar orasida uslub buziladi |
| `BigDecimal s = ...` | mahalliy o'zgaruvchi va parametr nomi shablonga mos emas (`java:S117`) | maintainability | minor | Mantiqni o'qish sekinlashadi |
| Ishlatilmagan `import` | keraksiz import o'chirilishi kerak (`java:S1128`) | maintainability | minor | Soxta bog'liqlik, kompilyatsiya shovqini |
| Ishlatilmagan `private` maydon | foydalanilmagan private maydon (`java:S1068`) | maintainability | major | O'quvchi uni ishlatilayotgan deb o'ylaydi |
| Ishlatilmagan metod parametri | foydalanilmagan parametr (`java:S1172`) | maintainability | major | Chaqiruvchi noto'g'ri shartnoma ko'radi |
| Ishlatilmagan mahalliy o'zgaruvchi | qiymat o'qilmaydi (`java:S1481`) | maintainability | major | Yashirin mantiqiy xato alomati |
| Ishlatilmagan `private` metod | o'lik kod (`java:S1144`) | maintainability | major | Qo'llab-quvvatlash va test yuki |
| Kommentariyaga olingan kod | kommentdagi kod o'chirilsin (`java:S125`) | maintainability | major | Qaysi variant to'g'ri ekani bilinmaydi |
| `// TODO` izohi | bajarilmagan ish belgisi (`java:S1135`) | maintainability | info | Debt ko'rinmas bo'lib qoladi |
| `// FIXME` izohi | tuzatilmagan nuqson belgisi (`java:S1134`) | maintainability | major | Ma'lum xato release ga ketadi |
| Eskirgan API chaqiruvi | deprecated element ishlatilgan (`java:S1874`) | maintainability | major | Keyingi major versiyada kod buziladi |
| `public BigDecimal balance` | maydon public bo'lmasligi kerak (`java:S1104`) | maintainability | major | Invariantni hech kim himoya qilmaydi |
| `public static Map CACHE` | public static o'zgaruvchan maydon (`java:S2386`) | maintainability (ba'zi profilda vulnerability) | critical | Tashqaridan holatni buzish mumkin |
| Konstruktorda bir marta beriladigan maydon `final` emas | o'zgarmas maydon `final` bo'lsin | maintainability | minor | Tasodifiy qayta tayinlash xavfi |
| Interfeysda `public abstract` | ortiqcha modifikator (`java:S2333`) | maintainability | minor | Shovqin, uslub nomuvofiqligi |
| Sikl ichida `str += x` | siklda satr birlashtirish (`java:S1643`) | maintainability | major | O(n^2) xotira va vaqt |
| `log.debug("id=" + id)` | argument har safar hisoblanadi (`java:S2629`) | maintainability | major | O'chirilgan log darajasida ham CPU sarfi |
| `name.toString()` | `String` ustida `toString()` (`java:S1858`) | maintainability | minor | Ma'nosiz chaqiruv, noto'g'ri tasavvur |
| `"x" + String.valueOf(n)` | ortiqcha `String.valueOf` (`java:S1153`) | maintainability | minor | Kod shovqini |
| Ikki metod bir xil tanaga ega | identik implementatsiya (`java:S4144`) | maintainability | major | Tuzatish bitta joyda qoladi |

## 28.1 Nomlash shabloniga mos kelmaydigan klass, metod, maydon va konstanta

Sonar nomlashni to'rtta alohida qoida bilan tekshiradi va har biri o'z regex parametriga ega. Klass uchun `java:S101`, metod uchun `java:S100`, konstanta uchun `java:S115`, oddiy maydon uchun `java:S116`, mahalliy o'zgaruvchi va parametr uchun `java:S117`. Shikoyat qilinadigan servis odatda shunday ko'rinadi.

```java
// Sonar: bitta klassda beshta nomlash qoidasi buzilgan
@Service
public class payment_service {                      // java:S101

    private static final int maxRetry = 3;          // java:S115

    private String Customer_Id;                     // java:S116

    public void Process_Payment(long Order_Id) {    // java:S100 va java:S117
        int Attempt = 0;                            // java:S117
        while (Attempt < maxRetry) {
            Attempt++;
        }
    }
}
```

Bu qoidalar kompilyatsiyaga ham, ishlashga ham ta'sir qilmaydi. Ular jamoaning kod o'qish tezligi uchun muhim. Regex standart holatda Java konvensiyasini talab qiladi: klass `PascalCase`, metod va maydon `camelCase`, `static final` konstanta `UPPER_SNAKE_CASE`.

```java
@Service
public class PaymentService {

    private static final int MAX_RETRY_COUNT = 3;   // konstanta: UPPER_SNAKE_CASE

    private String customerId;                      // maydon: camelCase

    public void processPayment(long orderId) {      // metod: camelCase
        int attempt = 0;
        while (attempt < MAX_RETRY_COUNT) {
            attempt++;
        }
    }
}
```

Tavsiya: nomlash qoidalarini birinchi kunda yoqing, chunki keyin minglab qatorni qayta nomlash review ni bo'g'ib qo'yadi.

## 28.2 Bitta harfli va ma'nosiz nomlar

Bu yerda halol bo'lish kerak. Standart `java:S117` regex `^[a-z][a-zA-Z0-9]*$` ko'rinishida bo'lgani uchun `s`, `l`, `x` kabi nomlar odatda shikoyatga tushmaydi. Ya'ni pastdagi kod default profilda nomlash bo'yicha toza ko'rinadi, lekin o'qishga og'ir.

```java
// Default profilda Sonar jim turadi, lekin bu kod o'qilmaydi
public BigDecimal calc(List<OrderLine> l) {
    BigDecimal s = BigDecimal.ZERO;
    for (OrderLine x : l) {
        BigDecimal p = x.getPrice()
                .multiply(BigDecimal.valueOf(x.getQuantity()));
        s = s.add(p);
    }
    return s;
}
```

Buni Sonar bilan ushlash uchun qoidaning `format` parametrini quality profile da qattiqlashtirish kerak. Masalan kamida ikki belgi talab qilish. Profile backup XML da bu shunday ko'rinadi.

```xml
<!-- Quality profile backup: mahalliy o'zgaruvchi nomi kamida 2 belgi -->
<profile>
  <name>Team Java</name>
  <language>java</language>
  <rules>
    <rule>
      <repositoryKey>java</repositoryKey>
      <key>S117</key>
      <priority>MINOR</priority>
      <parameters>
        <parameter>
          <key>format</key>
          <value>^[a-z][a-zA-Z0-9]+$</value>
        </parameter>
      </parameters>
    </rule>
  </rules>
</profile>
```

Tuzatilgan variant nomlarni domen tilida ataydi va metod nomini ham aniqlashtiradi.

```java
public BigDecimal calculateOrderTotal(List<OrderLine> orderLines) {
    BigDecimal total = BigDecimal.ZERO;
    for (OrderLine line : orderLines) {
        BigDecimal lineAmount = line.getPrice()
                .multiply(BigDecimal.valueOf(line.getQuantity()));
        total = total.add(lineAmount);
    }
    return total;
}
```

Tavsiya: sikl indeksi uchun `i` ni qoldiring, qolgan hamma joyda nomni domen atamasi bilan ataydigan regex ni profilga yozib qo'ying.

## 28.3 Ishlatilmaydigan import, maydon, parametr va mahalliy o'zgaruvchi

To'rtta alohida qoida bir xil muammoni ko'rsatadi: kod o'quvchiga yolg'on ma'lumot beradi. `java:S1128` keraksiz import, `java:S1068` foydalanilmagan private maydon, `java:S1172` foydalanilmagan parametr, `java:S1481` qiymati o'qilmagan mahalliy o'zgaruvchi.

```java
import java.util.Optional;          // java:S1128: ishlatilmaydi
import java.time.Duration;          // java:S1128: ishlatilmaydi

@Service
public class StockService {

    private final StockRepository stockRepository;
    private int lastCheckedCount;                  // java:S1068

    public void reserve(long productId, int qty, String reasonCode) {
        int available = stockRepository.available(productId);  // java:S1481
        stockRepository.decrease(productId, qty);              // reasonCode: java:S1172
    }
}
```

`java:S1481` ayniqsa qimmatli signal. Ko'pincha o'zgaruvchi o'qilmagani demak, muallif tekshiruvni yozishni unutgan. Shuning uchun bu shikoyatni avtomatik o'chirib tashlamang, avval mantiqni qayta o'qing.

```java
@Service
public class StockService {

    private final StockRepository stockRepository;

    public void reserve(long productId, int quantity) {
        int available = stockRepository.available(productId);
        if (available < quantity) {                 // o'zgaruvchi endi ishlatiladi
            throw new InsufficientStockException(productId, quantity, available);
        }
        stockRepository.decrease(productId, quantity);
    }
}
```

Tavsiya: `java:S1481` chiqsa birinchi savol "o'chiramanmi" emas, "qanday tekshiruv yozilmay qolgan" bo'lsin.

## 28.4 Ishlatilmaydigan private metod va o'lik kod

`java:S1144` hech qayerdan chaqirilmaydigan `private` metodni belgilaydi. Bu Sonar eng ishonchli topadigan o'lik kod turi, chunki `private` ko'rinish doirasi fayl bilan chegaralangan.

```java
@Service
public class ReportService {

    public Report monthly(YearMonth month) {
        return build(month);
    }

    private Report build(YearMonth month) { /* ... */ }

    private Report buildLegacy(YearMonth month) {   // java:S1144: chaqirilmaydi
        return new Report(month, List.of());
    }

    private String formatHeader(Report r) {         // java:S1144: chaqirilmaydi
        return "Report " + r.getMonth();
    }
}
```

Repository da bunga o'xshash holat ko'proq uchraydi: hech kim chaqirmaydigan `@Query`. Sonar uni `private` bo'lmagani uchun o'lik kod deb atamaydi, lekin u ham qo'llab-quvvatlash yuki.

```sql
-- Hech kim chaqirmaydigan native query: Sonar ko'rmaydi, lekin baribir o'lik kod
SELECT o.id, o.total
  FROM orders o
 WHERE o.status = 'LEGACY_HOLD'
   AND o.created_at < now() - interval '2 years';
```

Tuzatish oddiy: metodni o'chirib, git tarixiga tayanish. Tarix allaqachon zaxira nusxa, shuning uchun kodni "ehtimol kerak bo'ladi" deb saqlash asossiz.

```java
@Service
public class ReportService {

    public Report monthly(YearMonth month) {
        return build(month);
    }

    private Report build(YearMonth month) { /* ... */ }
}
```

Tavsiya: o'lik kodni o'chirishni alohida commit qiling, shunda review diff da mantiq o'zgarishi bilan aralashmaydi.

## 28.5 Kommentariyaga olingan kod bloki

`java:S125` kommentariya ichidagi kodni aniqlaydi. Parser kommentni tahlil qiladi va u Java sintaksisiga o'xshasa shikoyat yozadi. Bu qoida major darajada bo'ladi, chunki o'quvchi qaysi variant haqiqiy ekanini bilmaydi.

```java
public void refund(long paymentId, BigDecimal amount) {
    // java:S125: quyidagi blok kommentga olingan kod
    // if (amount.compareTo(payment.getTotal()) > 0) {
    //     throw new IllegalArgumentException("Refund exceeds total");
    // }
    gateway.refund(paymentId, amount);
}
```

Ikkita yo'l bor. Agar tekshiruv kerak bo'lsa, uni tiriltiring va testini yozing. Kerak bo'lmasa, o'chiring va nega olib tashlanganini bitta jumla bilan izohlang.

```java
public void refund(long paymentId, BigDecimal amount) {
    Payment payment = paymentRepository.getById(paymentId);
    if (amount.compareTo(payment.getTotal()) > 0) {
        throw new RefundExceedsTotalException(paymentId);
    }
    gateway.refund(paymentId, amount);
}
```

Tavsiya: kommentda kod saqlashni taqiqlang, chunki versiya nazorati buni sizdan yaxshiroq bajaradi.

## 28.6 `TODO` va `FIXME` izohlari va ularning hisobi

`java:S1135` `TODO` ni, `java:S1134` esa `FIXME` ni belgilaydi. Ikkisining farqi muhim: `TODO` odatda info darajasida va quality gate ga kirmaydi, `FIXME` esa major bo'ladi va `Maintainability Rating` ga ta'sir qiladi.

```java
@Service
public class InvoiceService {

    public Invoice issue(long orderId) {
        // TODO: valyuta kursini kesh orqali olish      java:S1135, info
        // FIXME: yakkalangan tranzaksiyada ikki marta yozilmoqda   java:S1134, major
        return invoiceRepository.save(buildInvoice(orderId));
    }
}
```

Hisobni ko'rish uchun Sonar ni kutish shart emas. Lokal `grep` bilan tendensiyani kuzatish mumkin, bu CI da ham arzon.

```bash
# TODO va FIXME hisobini chiqarish, faqat asosiy manba daraxti
grep -rn --include='*.java' -E '//\s*(TODO|FIXME)' src/main/java | wc -l
grep -rn --include='*.java' -E '//\s*FIXME' src/main/java

# FIXME soni noldan katta bo'lsa buildni to'xtatish
if grep -rq --include='*.java' -E '//\s*FIXME' src/main/java; then
  echo "FIXME qolgan, release bloklanadi" >&2
  exit 1
fi
```

Tavsiya: `TODO` ni issue tracker raqami bilan yozishni majburiy qiling va `FIXME` ni release bloklovchi belgi deb kelishib oling.

## 28.7 Eskirgan (deprecated) API ishlatish

Sonar bu mavzuda ikki tomondan yuradi. `java:S1874` eskirgan elementni chaqirgan kodni, `java:S1133` esa o'zingiz `@Deprecated` deb belgilagan va hali o'chirmagan kodni ko'rsatadi.

```java
@Service
public class OrderService {

    @Deprecated                                  // java:S1133: o'chirish rejasi yo'q
    public void placeOrder(OrderDto dto) {
        placeOrder(dto, Channel.WEB);
    }

    public BigDecimal fee(double amount) {
        BigDecimal value = new BigDecimal(amount);   // aniqlik yo'qoladi
        return value.multiply(new BigDecimal("0.02"));
    }
}
```

Spring Boot 3.x ga ko'chishda `java:S1874` oqimi odatda keskin oshadi, chunki 2.x API lari eskiradi. Tuzatishda `@Deprecated` ga `since` va `forRemoval` qo'shish Sonar ga ham, jamoaga ham aniq signal beradi.

```java
@Deprecated(since = "3.4.0", forRemoval = true)
public void placeOrder(OrderDto dto) {
    placeOrder(dto, Channel.WEB);
}

public BigDecimal fee(BigDecimal amount) {
    return amount.multiply(new BigDecimal("0.02"));   // double ishlatilmaydi
}
```

Tavsiya: har bir `@Deprecated` ga `forRemoval` va o'chirish versiyasini yozing, aks holda eskirgan kod abadiy yashaydi.

## 28.8 `public` maydon va kapsullashning buzilishi

`java:S1104` har qanday `public` nostatik maydonni belgilaydi. `java:S2386` esa alohida va og'irroq holat: `public static` o'zgaruvchan kolleksiya yoki massiv. Ikkinchisi ba'zi profilda security tomonga ham tortiladi, chunki tashqi kod global holatni almashtirib yuborishi mumkin.

```java
@Service
public class PricingService {

    public BigDecimal lastMargin;                      // java:S1104

    public static final Map<String, BigDecimal> RATES  // java:S2386
            = new HashMap<>();                         // final, lekin mazmuni o'zgaradi
}
```

`final` so'zi bu yerda yetarli emas. `final` havolani qotiradi, kolleksiya ichini emas. Shuning uchun `Map.copyOf` yoki `Collections.unmodifiableMap` kerak.

```java
@Service
public class PricingService {

    private BigDecimal lastMargin;                     // kapsullangan

    private static final Map<String, BigDecimal> RATES =
            Map.of("UZS", new BigDecimal("1.00"));     // o'zgarmas

    public BigDecimal getLastMargin() {
        return lastMargin;
    }
}
```

Tavsiya: `public` maydonni faqat `record` ichida yoki `static final` immutable qiymat uchun qoldiring, boshqa hamma joyda `private` qiling.

## 28.9 `final` qo'yilmagan o'zgarmas maydon

Sonar da bu holat bir nechta qoida orqali ko'rinadi, shuning uchun aniq kalitni faqat profilda ko'rganingizda yozing. Eng ishonchlisi `java:S1170`: deklaratsiyada qiymat beriladigan `public` maydon `static final` bo'lishi kerak. Konstruktor orqali injeksiya qilingan Spring bog'liqliklari esa `final` bo'lmasa, Sonar odatda minor code smell beradi va ba'zi profilda bu qoida o'chirilgan bo'ladi.

```java
@Service
public class ShipmentService {

    public int maxParcelWeight = 30;        // java:S1170: static final bo'lishi kerak

    private ShipmentRepository repository;  // konstruktorda beriladi, lekin final emas

    public ShipmentService(ShipmentRepository repository) {
        this.repository = repository;
    }
}
```

`final` ning foydasi stilistik emas. U maydon faqat konstruktorda tayinlanganini kompilyator darajasida kafolatlaydi va klassni ko'p oqimli muhitda xavfsiz qiladi.

```java
@Service
public class ShipmentService {

    private static final int MAX_PARCEL_WEIGHT_KG = 30;

    private final ShipmentRepository repository;

    public ShipmentService(ShipmentRepository repository) {
        this.repository = repository;
    }
}
```

Tavsiya: barcha konstruktor injeksiyasi maydonlarini `final` qiling, bu bir vaqtning o'zida Sonar shikoyatini ham, kelajakdagi `@Autowired` setter vasvasasini ham yopadi.

## 28.10 Ortiqcha modifikator (interfeysda `public abstract`)

`java:S2333` kontekstdan kelib chiqib ortiqcha bo'lgan modifikatorni belgilaydi. Interfeys metodi allaqachon `public abstract`, interfeys maydoni allaqachon `public static final`, `final` klass metodiga `final` qo'yish ham ortiqcha.

```java
public interface PaymentGateway {

    public static final int TIMEOUT_MS = 5_000;   // java:S2333: uchta ortiqcha so'z

    public abstract Receipt charge(ChargeRequest request);   // java:S2333

    abstract void refund(long paymentId);                    // java:S2333
}
```

Tuzatish faqat olib tashlash. Mazmun o'zgarmaydi, shuning uchun bu o'zgarish uchun test yozish shart emas.

```java
public interface PaymentGateway {

    int TIMEOUT_MS = 5_000;

    Receipt charge(ChargeRequest request);

    void refund(long paymentId);
}
```

Tavsiya: bu qoidani IDE ning save action yoki `spotless` formatlovchisi bilan avtomatlashtiring, qo'lda tuzatish vaqt yo'qotish.

## 28.11 Satr birlashtirishni sikl ichida bajarish

`java:S1643` siklda `+` bilan satr yig'ishni belgilaydi. Sababi aniq: har iteratsiyada yangi `String` obyekti yaratiladi, natijada murakkablik elementlar soniga kvadratik bog'lanadi. Hisobot generatsiyasida bu eng tez sezilaradigan muammo.

```java
public String buildCsv(List<OrderRow> rows) {
    String csv = "";
    for (OrderRow row : rows) {
        csv += row.getId() + ";" + row.getTotal() + "\n";   // java:S1643
    }
    return csv;
}
```

Zamonaviy JVM bitta ifoda ichidagi birlashtirishni optimallashtiradi, lekin sikl iteratsiyalari orasida buni qila olmaydi. Shuning uchun `StringBuilder` yoki `Collectors.joining` kerak.

```java
public String buildCsv(List<OrderRow> rows) {
    return rows.stream()
            .map(row -> row.getId() + ";" + row.getTotal())
            .collect(Collectors.joining("\n", "", "\n"));
}
```

Tavsiya: siklda satr yig'ish ko'rsangiz darhol `StringBuilder` yoki `joining` ga o'tkazing, bu tuzatish deyarli hech qachon xatarli emas.

## 28.12 Loglashda satr birlashtirish va formatlangan xabarga o'tish

`java:S2629` log chaqiruvining argumenti chaqiruvdan oldin hisoblanishini belgilaydi. Ya'ni `log.debug("id=" + id)` da satr birlashtirish `debug` darajasi o'chirilgan bo'lsa ham bajariladi. Issiq kod yo'lida bu real CPU sarfi.

```java
public void process(Order order) {
    // java:S2629: argument har safar qurib chiqiladi
    log.debug("Buyurtma qayta ishlanmoqda: " + order.toLongDescription());
    log.info("Buyurtma " + order.getId() + " holati " + order.getStatus());
}
```

SLF4J ning `{}` shabloni muammoni yopadi, chunki formatlash faqat daraja yoqilgan bo'lsa bajariladi. Qimmat argument uchun `Supplier` variantini yoki `isDebugEnabled` tekshiruvini ishlatish mumkin.

```java
public void process(Order order) {
    if (log.isDebugEnabled()) {                     // qimmat argument uchun
        log.debug("Buyurtma qayta ishlanmoqda: {}", order.toLongDescription());
    }
    log.info("Buyurtma {} holati {}", order.getId(), order.getStatus());
}
```

Tavsiya: loglarda `+` ni butunlay taqiqlang va `{}` shablonini jamoa standarti qilib yozib qo'ying.

## 28.13 Ortiqcha `toString` va `String.valueOf` chaqiruvi

Ikki alohida qoida bir xil odatdan kelib chiqadi. `java:S1858` allaqachon `String` bo'lgan qiymatda `toString()` chaqirilganini belgilaydi. `java:S1153` esa satr birlashtirish ichida `String.valueOf` ishlatilganini ko'rsatadi, chunki `+` operatori konvertatsiyani o'zi bajaradi.

```java
public String describe(Order order) {
    String code = order.getCode();
    String a = "Kod: " + code.toString();                 // java:S1858
    String b = "Jami: " + String.valueOf(order.getTotal()); // java:S1153
    return a + " " + b;
}
```

Bu shikoyatlar minor, lekin ular ko'pincha chuqurroq muammoning izi. `code.toString()` yozgan odam `code` ning turini bilmagan, ya'ni kod o'qilmaydi.

```java
public String describe(Order order) {
    return "Kod: " + order.getCode()
            + " Jami: " + order.getTotal();   // konvertatsiya avtomatik
}
```

Tavsiya: bu ikki qoidani avtomatik tuzatish ro'yxatiga qo'ying, lekin tuzatish paytida o'zgaruvchi turi aniq ko'rinishiga ham e'tibor bering.

## 28.14 Bir xil ishni bajaradigan ikkita metod

`java:S4144` tanasi identik bo'lgan ikki metodni belgilaydi. Bu Sonar ning duplication o'lchovidan boshqa narsa: `Duplications` metrikasi blok darajasida ishlaydi, `java:S4144` esa metod darajasida ishlaydi va kichik metodlarda ham chiqadi.

```java
@Service
public class WarehouseService {

    public int availableQty(long productId) {
        return stockRepository.sumOnHand(productId)
                - stockRepository.sumReserved(productId);
    }

    public int freeQty(long productId) {              // java:S4144: identik tana
        return stockRepository.sumOnHand(productId)
                - stockRepository.sumReserved(productId);
    }
}
```

Repository da bu holat yana osonroq paydo bo'ladi: ikki derived query bir xil SQL ga aylanadi. Tuzatish bitta nom qoldirib, ikkinchisini delegatsiya qilish yoki butunlay o'chirish.

```java
@Service
public class WarehouseService {

    public int availableQty(long productId) {
        return stockRepository.sumOnHand(productId)
                - stockRepository.sumReserved(productId);
    }

    @Deprecated(since = "2.7.0", forRemoval = true)
    public int freeQty(long productId) {
        return availableQty(productId);     // yagona manba
    }
}
```

Tavsiya: identik metodlardan birini darhol o'chiring, o'chirish mumkin bo'lmasa delegatsiya qilib `forRemoval` belgisini qo'ying.

## 28.15 Oddiy yondashuv va arxitektor yondashuvi

| Savol | Oddiy yondashuv | Arxitektor yondashuvi |
|---|---|---|
| Minor code smell lar bilan nima qilish | "Keyin tuzatamiz" deb butun loyihaga qoldiradi | New Code gate ni nolga qo'yadi, eski qarzni alohida reja bilan yopadi |
| Nomlash qoidalari | Default profilni o'zgarishsiz qoldiradi | `format` parametrini jamoa konvensiyasiga moslab yozadi |
| Ishlatilmagan o'zgaruvchi | Darhol o'chirib tashlaydi | Avval "qanday tekshiruv yozilmagan" deb so'raydi, keyin qaror qiladi |
| `TODO` va `FIXME` | Ikkisini bir xil ko'radi | `TODO` ni issue raqamiga bog'laydi, `FIXME` ni release blokeri qiladi |
| Deprecated API | Ogohlantirishni e'tiborsiz qoldiradi | `forRemoval` va migratsiya muddatini kodga yozadi |
| O'lik kod | "Ehtimol kerak bo'ladi" deb saqlaydi | Git tarixiga tayanib o'chiradi, alohida commit qiladi |
| Loglash | `+` bilan yozadi, chunki ishlaydi | `{}` shablonini standart qilib, qimmat argumentni shartga oladi |
| Uslub shikoyatlari | Qo'lda, review da tuzatadi | Formatlovchi va save action bilan avtomatlashtiradi |
| Issue larni yopish | `// NOSONAR` qo'yadi | Qoidani profilda ongli ravishda o'chiradi va sababini yozadi |
| Metrika maqsadi | "Hamma issue nol bo'lsin" | Rating va New Code shartlarini ajratib, realistik maqsad qo'yadi |

## 28.16 Tuzoqlar va yechimlar

| Tuzoq | Nega yuzaga keladi | Yechim |
|---|---|---|
| Butun loyihaga ommaviy "auto-fix" PR | Minglab qator o'zgaradi, review imkonsiz | Faqat o'zgargan fayllarda tuzating, New Code gate ga tayaning |
| `// NOSONAR` ning tarqalishi | Eng tez yo'l shu ko'rinadi | Qoida haqiqatan keraksiz bo'lsa profilda o'chiring, izoh bilan |
| `@SuppressWarnings` ning keng doirasi | Klass ustiga qo'yiladi | Faqat metod yoki o'zgaruvchi darajasida, aniq kalit bilan |
| Generatsiya qilingan kod shikoyat beradi | Analiz doirasiga kirib qolgan | `sonar.exclusions` bilan generatsiya papkasini chiqarib tashlang |
| Lombok dan keyin "ishlatilmagan maydon" | Analizda annotation processing ishlamagan | `sonar.java.binaries` ni kompilyatsiya natijasiga qarating |
| Test kodida nomlash shikoyatlari | Bitta profil ikki manba uchun ishlatilgan | Test fayllariga alohida profil yoki `sonar.test.exclusions` |
| `FIXME` ni o'chirib, muammoni qoldirish | Gate o'tsin deb qilinadi | Issue tracker ga ko'chirib, havolani kodga yozing |
| Rating yaxshilanmaydi | Faqat minor smell lar tuzatilgan | Remediation effort katta bo'lgan major issue larni avval oling |

Analizni to'g'ri sozlash ham shu katalogning bir qismi. Pastdagi sozlash generatsiya qilingan kodni va migratsiya skriptlarini analizdan chiqaradi, shuning uchun soxta shikoyatlar kamayadi.

```properties
# sonar-project.properties: shovqinni kamaytirish
sonar.sources=src/main/java
sonar.tests=src/test/java
sonar.java.binaries=target/classes
sonar.exclusions=**/generated/**,**/*MapperImpl.java,**/db/migration/**
sonar.test.exclusions=**/*IT.java
sonar.issue.ignore.multicriteria=e1
sonar.issue.ignore.multicriteria.e1.ruleKey=java:S1135
sonar.issue.ignore.multicriteria.e1.resourceKey=**/legacy/**
```

CI da esa yangi kod uchun qattiq, eski kod uchun yumshoq siyosat yuritish mumkin. Quality gate shartlari har loyihada boshqacha sozlanadi, shuning uchun bu yerda universal retsept yo'q. Quyidagi pipeline faqat analizni yuboradi va gate natijasini kutadi.

```yaml
# .github/workflows/sonar.yml dan qism
- name: Build va analiz
  run: >
    ./mvnw -B verify sonar:sonar
    -Dsonar.projectKey=shop-backend
    -Dsonar.qualitygate.wait=true
  env:
    SONAR_TOKEN: ${{ secrets.SONAR_TOKEN }}

- name: FIXME tekshiruvi
  run: |
    ! grep -rq --include='*.java' -E '//\s*FIXME' src/main/java
```

## 28.17 Amalda qo'llash

- [ ] Quality profile da `java:S100`, `java:S101`, `java:S115`, `java:S116`, `java:S117` yoqilganini tekshiring va `format` parametrini jamoa konvensiyasiga moslang.
- [ ] `java:S1068`, `java:S1128`, `java:S1172`, `java:S1481`, `java:S1144` bo'yicha hozirgi issue sonini yozib oling, bu sizning boshlang'ich nuqtangiz.
- [ ] Har bir `java:S1481` shikoyatini qo'lda ko'rib chiqing va yozilmay qolgan tekshiruv bor-yo'qligini aniqlang.
- [ ] Barcha konstruktor injeksiyasi maydonlarini `final` qilib, `public` nostatik maydonlarni `private` ga o'tkazing.
- [ ] Loglardagi `+` birlashtirishlarni `{}` shabloniga ko'chiring va qimmat argumentlarni `isDebugEnabled` ichiga oling.
- [ ] `FIXME` sonini CI da nolga majburlang va mavjud `FIXME` larni issue tracker ga ko'chirib, havolasini `TODO` ga yozing.
- [ ] `sonar.exclusions` va `sonar.java.binaries` ni to'g'rilab, generatsiya qilingan kod shikoyatlarini yo'q qiling.
- [ ] Formatlovchi va IDE save action ni sozlab, `java:S2333`, `java:S1858`, `java:S1153` kabi uslub shikoyatlari qayta paydo bo'lmasligiga erishing.

---

[&larr; 27. Xato katalogi: maintainability, tuzilish va murakkablik](27-xato-katalogi-maintainability-tuzilish-va.md) · [Mundarija](README.md) · [29. Xato katalogi: Spring, JPA va PostgreSQL ga xos xatolar &rarr;](29-xato-katalogi-spring-jpa-va-postgresql-ga.md)
