<!-- doc: sonarqube | chapter: 25 | part: VII. Xato katalogi: qanday kod qanday xato hisoblanadi -->

[SonarQube](../../README.md) / [SonarQube](README.md)

# 25. Xato katalogi: reliability (bug) toifasi (Catalog: Reliability)

<details>
<summary>Bu bobdagi 19 bo'lim</summary>

- [25.1 Toifa va jiddiylik qanday o'qiladi](#251-toifa-va-jiddiylik-qanday-oqiladi)
- [25.2 null bo'lishi mumkin bo'lgan qiymatga murojaat qilish](#252-null-bolishi-mumkin-bolgan-qiymatga-murojaat-qilish)
- [25.3 Optional ni tekshirmasdan get() chaqirish](#253-optional-ni-tekshirmasdan-get-chaqirish)
- [25.4 Yopilmagan resurs: InputStream, Connection, Statement](#254-yopilmagan-resurs-inputstream-connection-statement)
- [25.5 equals va hashCode ni birgalikda yozmaslik](#255-equals-va-hashcode-ni-birgalikda-yozmaslik)
- [25.6 Boxed turlarni == bilan solishtirish](#256-boxed-turlarni--bilan-solishtirish)
- [25.7 Suzuvchi nuqtali sonlarni == bilan solishtirish va pul uchun double](#257-suzuvchi-nuqtali-sonlarni--bilan-solishtirish-va-pul-uchun-double)
- [25.8 Metod natijasini e'tiborsiz qoldirish](#258-metod-natijasini-etiborsiz-qoldirish)
- [25.9 InterruptedException ni yutib yuborish](#259-interruptedexception-ni-yutib-yuborish)
- [25.10 Har doim bir xil natija beradigan shart va yetib bo'lmaydigan kod](#2510-har-doim-bir-xil-natija-beradigan-shart-va-yetib-bolmaydigan-kod)
- [25.11 To'plamni iteratsiya paytida o'zgartirish](#2511-toplamni-iteratsiya-paytida-ozgartirish)
- [25.12 Collectors.toMap da takroriy kalit](#2512-collectorstomap-da-takroriy-kalit)
- [25.13 Sanani noto'g'ri formatlash va SimpleDateFormat ni baham ko'rish](#2513-sanani-notogri-formatlash-va-simpledateformat-ni-baham-korish)
- [25.14 compareTo va equals nomuvofiqligi](#2514-compareto-va-equals-nomuvofiqligi)
- [25.15 Sikl o'zgaruvchisini ichkarida o'zgartirish yoki cheksiz sikl xavfi](#2515-sikl-ozgaruvchisini-ichkarida-ozgartirish-yoki-cheksiz-sikl-xavfi)
- [25.16 Tuzoq va yechim](#2516-tuzoq-va-yechim)
- [25.17 Oddiy yondashuv va arxitektor yondashuvi](#2517-oddiy-yondashuv-va-arxitektor-yondashuvi)
- [25.18 Katalogni loyihada tekshirish](#2518-katalogni-loyihada-tekshirish)
- [25.19 Amalda qo'llash](#2519-amalda-qollash)

</details>



Reliability toifasi Sonar uchun eng qattiq toifa, chunki bu yerdagi issue "kod ishlamaydi yoki kutilmagan holatda sinadi" degan ma'noni bildiradi. Quality gate ko'pincha aynan yangi bug soniga nol chek qo'yadi, shuning uchun bu katalogdagi holatlar birinchi navbatda tuzatiladi. Quyida har bir holat uchun shikoyat qilinadigan kod, shikoyat sababi va tuzatilgan variant berilgan. Misollar to'lov servisi, buyurtma va ombor qoldig'i ustida.

| Kod holati | Sonar nima deydi | Toifa | Jiddiylik (taxminan) | Ta'siri |
|---|---|---|---|---|
| `null` qaytishi mumkin metod natijasini tekshirmasdan ishlatish | null dereference xavfi (`java:S2259`) | reliability (bug) | Major yoki Blocker | So'rov `NullPointerException` bilan tushadi |
| `Optional.get()` ni `isPresent()` dan oldin chaqirish | Optional qiymati tekshirilmagan (`java:S3655`) | reliability (bug) | Major | `NoSuchElementException` |
| `InputStream`, `Connection`, `Statement` yopilmaydi | resurs yopilishi shart (`java:S2095`) | reliability (bug) | Blocker yoki Major | Connection pool tugaydi, servis muzlaydi |
| `equals` bor, `hashCode` yo'q | ikkisi birga qayta yozilishi kerak (`java:S1206`) | reliability (bug) | Blocker | `HashMap` va `HashSet` da yozuv yo'qoladi |
| `Long` yoki `Integer` ni `==` bilan solishtirish | obyekt havolasi solishtirilmoqda | reliability (bug) | Major | 127 dan katta ID lar teng emas deb chiqadi |
| `double` ni `==` bilan solishtirish | suzuvchi nuqta tengligi (`java:S1244`) | reliability (bug) | Major | Pul summasi hech qachon teng kelmaydi |
| Pul uchun `double` maydon | aniqlik yo'qolishi, `BigDecimal` kerak | reliability (bug) yoki code smell | Major | Hisob-kitobda tiyin yo'qoladi |
| `String.trim()` natijasi ishlatilmaydi | metod natijasi e'tiborsiz (`java:S2201`) | reliability (bug) | Major | Tozalash amalda bajarilmaydi |
| `catch (InterruptedException e) {}` | interrupt holati yutilgan (`java:S2142`) | reliability (bug) | Major | Thread to'xtatilmaydi, graceful shutdown buziladi |
| Shart har doim `true` yoki `false` | shart o'zgarmas (`java:S2583`) | reliability (bug) | Major | Tekshiruv amalda ishlamaydi |
| `if` dan keyin yetib bo'lmaydigan kod | unreachable code (`java:S1763`) | reliability (bug) | Major | Mantiq hech qachon bajarilmaydi |
| `for-each` ichida `list.remove(...)` | to'plam iteratsiya paytida o'zgartirilgan | reliability (bug) | Major | `ConcurrentModificationException` |
| `Collectors.toMap` da takroriy kalit | merge funksiyasi berilmagan | reliability (bug) | Major | `IllegalStateException`, hisobot tushadi |
| `static SimpleDateFormat` ni baham ko'rish | thread-safe bo'lmagan maydon static | reliability (bug) | Blocker yoki Major | Yuk ostida sana buzilib chiqadi |
| `compareTo` bor, `equals` moslanmagan | ikkisi mos kelishi kerak (`java:S1210`) | reliability (bug) | Major | `TreeSet` va `List.contains` turlicha javob beradi |
| Sikl o'zgaruvchisi tanada o'zgartirilgan (`java:S127`) | counter tanada o'zgartirilmasin | reliability (bug) | Major | Qatorlar o'tkazib yuboriladi |
| Sikl shartiga ta'sir qilmaydigan tana (`java:S2189`) | cheksiz sikl | reliability (bug) | Blocker | CPU 100 foiz, pod restart |

## 25.1 Toifa va jiddiylik qanday o'qiladi

Toifa qoidaga biriktirilgan va o'zgarmaydi, jiddiylik esa faol quality profile da sozlanadi. Shuning uchun jadvaldagi jiddiylik "taxminan": bir loyihada Major, boshqasida Blocker bo'lishi mumkin. 2025 LTA liniyasidagi yangi "software quality" modelida bitta issue bir vaqtda reliability va maintainability ta'siriga ega bo'lib ko'rinishi mumkin, eski 9.9 LTA da esa faqat bitta toifa ko'rsatiladi.

## 25.2 null bo'lishi mumkin bo'lgan qiymatga murojaat qilish

```java
// SHIKOYAT: findByOrderId null qaytarishi mumkin
public BigDecimal paidAmount(String orderId) {
    Payment payment = paymentRepository.findByOrderId(orderId);
    return payment.getAmount(); // null dereference
}
```

Sonar metodning qaytish yo'llarini kuzatadi va `null` qaytarish imkoni bor yo'lni topadi. Agar shu qiymat tekshirilmasdan ishlatilsa, u null dereference deb belgilanadi. `@Nullable` annotatsiyasi yoki `Optional` qaytish turi tahlilni yanada aniq qiladi.

```java
// TUZATILGAN: yo'qlik holati aniq ifodalangan
public BigDecimal paidAmount(String orderId) {
    return paymentRepository.findByOrderId(orderId)
            .map(Payment::getAmount)
            .orElse(BigDecimal.ZERO);
}
```

Repository metodlari `Optional` qaytarsin, shunda yo'qlik holati kompilyatsiya darajasida ko'rinadi.

## 25.3 Optional ni tekshirmasdan get() chaqirish

```java
// SHIKOYAT: get() himoyalanmagan
Optional<Order> found = orderRepository.findById(id);
Order order = found.get(); // NoSuchElementException xavfi
```

Sonar `Optional` ustida `isPresent()` yoki `isEmpty()` tekshiruvi bo'lmasa `get()` ni bug deb belgilaydi. Bu qoida `orElseThrow()` ga ham tegishli emas, chunki unda xato turi aniq.

```java
// TUZATILGAN: yo'qlik holati domen istisnosiga aylantirilgan
Order order = orderRepository.findById(id)
        .orElseThrow(() -> new OrderNotFoundException(id));
```

`get()` ni loyiha bo'ylab taqiqlang va `orElseThrow` ni standart qiling.

## 25.4 Yopilmagan resurs: InputStream, Connection, Statement

```java
// SHIKOYAT: istisno bo'lsa resurs ochiq qoladi
public int stockOf(String sku) throws SQLException {
    Connection c = dataSource.getConnection();
    PreparedStatement ps = c.prepareStatement(STOCK_SQL);
    ps.setString(1, sku);
    ResultSet rs = ps.executeQuery();
    return rs.next() ? rs.getInt(1) : 0;
}
```

Sonar `AutoCloseable` ni amalga oshiruvchi obyekt yaratilib, barcha chiqish yo'llarida yopilmaganini ko'radi. Connection pool da bu eng og'ir xato: ochiq connection qaytarilmaydi va bir necha daqiqada servis butunlay to'xtaydi.

```java
// TUZATILGAN: try-with-resources barcha yo'llarda yopadi
public int stockOf(String sku) throws SQLException {
    try (Connection c = dataSource.getConnection();
         PreparedStatement ps = c.prepareStatement(STOCK_SQL)) {
        ps.setString(1, sku);
        try (ResultSet rs = ps.executeQuery()) {
            return rs.next() ? rs.getInt(1) : 0;
        }
    }
}
```

Shu so'rovni sinash uchun ombor jadvali ustidagi SQL ni alohida ushlab turing.

```sql
-- ombor qoldig'i: sku bo'yicha bitta qator
SELECT quantity
FROM warehouse_stock
WHERE sku = ?
  AND warehouse_id = current_setting('app.warehouse')::bigint;
```

Har qanday `AutoCloseable` ni faqat try-with-resources ichida yarating.

## 25.5 equals va hashCode ni birgalikda yozmaslik

```java
// SHIKOYAT: hashCode yo'q
public class Sku {
    private final String code;
    @Override public boolean equals(Object o) {
        return o instanceof Sku s && code.equals(s.code);
    }
}
```

Sonar bu juftlikni qattiq nazorat qiladi, chunki kontrakt buzilganda `HashSet` ikkita teng obyektni ikki xil deb qabul qiladi. Ombor qoldig'ini `Map<Sku, Integer>` da yig'sangiz, bitta SKU bir necha marta sanaladi.

```java
// TUZATILGAN: ikkisi birga
@Override public boolean equals(Object o) {
    return o instanceof Sku s && code.equals(s.code);
}
@Override public int hashCode() {
    return Objects.hash(code);
}
```

Qiymat obyektlari uchun `record` ishlatsangiz, bu juftlik avtomatik to'g'ri bo'ladi.

## 25.6 Boxed turlarni == bilan solishtirish

```java
// SHIKOYAT: havola solishtirilmoqda
Long paymentId = payment.getId();
Long expectedId = request.getPaymentId();
if (paymentId == expectedId) {   // 127 dan katta qiymatlarda false
    confirm(payment);
}
```

Sonar operandlarning turi boxed ekanini ko'radi va `==` qiymat emas, havola solishtirishini aytadi. Integer cache faqat kichik qiymatlarda tasodifan ishlaydi, shuning uchun xato test ma'lumotida ko'rinmaydi va production da chiqadi.

```java
// TUZATILGAN: qiymat solishtirish
if (Objects.equals(paymentId, expectedId)) {
    confirm(payment);
}
```

Boxed turlar uchun har doim `Objects.equals`, primitive uchun `==` ishlating.

## 25.7 Suzuvchi nuqtali sonlarni == bilan solishtirish va pul uchun double

```java
// SHIKOYAT: pul double da va tenglik aniq emas
double total = 0.1 + 0.2;
if (total == 0.3) {           // false
    markOrderPaid(orderId);
}
```

Sonar suzuvchi nuqta tengligini alohida qoida bilan belgilaydi, chunki ikkilik kasr o'nlik summani aniq ifodalay olmaydi. Pul uchun esa muammo kattaroq: yuzlab tranzaksiyadan keyin yig'indi tiyinlarga xato beradi va hisobot bilan bank ekstrakti mos kelmaydi.

```java
// TUZATILGAN: BigDecimal va aniq masshtab
BigDecimal total = new BigDecimal("0.10").add(new BigDecimal("0.20"));
if (total.compareTo(new BigDecimal("0.30")) == 0) {
    markOrderPaid(orderId);
}
```

Pulni `BigDecimal` da, bazada `numeric(19,4)` da saqlang va `equals` emas `compareTo` bilan solishtiring.

## 25.8 Metod natijasini e'tiborsiz qoldirish

```java
// SHIKOYAT: natija tashlab ketilgan
public void normalize(PaymentRequest request) {
    request.getReference().trim();          // natija yo'qoladi
    BigDecimal.ONE.add(request.getFee());   // natija yo'qoladi
}
```

Sonar o'zgarmas obyektlarning metodlari natijasiz chaqirilganini ko'radi va buni bug deb belgilaydi. `String` va `BigDecimal` immutable, shuning uchun bunday chaqiruv hech narsani o'zgartirmaydi va kod yolg'on ishonch beradi.

```java
// TUZATILGAN: natija ishlatilgan
public PaymentRequest normalize(PaymentRequest request) {
    return request
            .withReference(request.getReference().trim())
            .withFee(BigDecimal.ONE.add(request.getFee()));
}
```

Immutable turlar bilan ishlaganda har bir chaqiruv natijasini o'zlashtiring yoki qaytaring.

## 25.9 InterruptedException ni yutib yuborish

```java
// SHIKOYAT: interrupt holati yo'qotilgan
try {
    Thread.sleep(retryDelayMs);
} catch (InterruptedException e) {
    log.warn("kutish uzildi");   // holat tiklanmagan
}
```

Sonar bu istisnoni maxsus holat deb biladi: uni yutib yuborsangiz, thread ga berilgan to'xtash signali yo'qoladi. Natijada to'lov retry sikli shutdown paytida ham aylanishda davom etadi va pod majburan o'ldiriladi.

```java
// TUZATILGAN: holat tiklangan va sikl to'xtagan
try {
    Thread.sleep(retryDelayMs);
} catch (InterruptedException e) {
    Thread.currentThread().interrupt();
    throw new PaymentRetryAbortedException(e);
}
```

`InterruptedException` ni ushlasangiz, `Thread.currentThread().interrupt()` ni chaqirib keyin chiqib keting.

## 25.10 Har doim bir xil natija beradigan shart va yetib bo'lmaydigan kod

```java
// SHIKOYAT: ikkinchi tekshiruv har doim false, keyingi qator yetib bo'lmaydi
if (order == null) {
    return Status.REJECTED;
}
if (order == null) {              // har doim false
    log.error("buyurtma yo'q");
    return Status.REJECTED;       // unreachable
}
```

Sonar oqim tahlili bilan shartning qiymati allaqachon aniqlanganini isbotlaydi. Bunday joy odatda copy-paste yoki yarim tuzatilgan refactoring izi bo'ladi va haqiqiy tekshiruv o'rnini egallaydi.

```java
// TUZATILGAN: bitta tekshiruv, keyin haqiqiy mantiq
if (order == null) {
    log.error("buyurtma yo'q: {}", orderId);
    return Status.REJECTED;
}
return order.isPaid() ? Status.SHIPPED : Status.WAITING_PAYMENT;
```

Bu qoidani ogohlantirish emas, mantiqiy xato signali deb o'qing.

## 25.11 To'plamni iteratsiya paytida o'zgartirish

```java
// SHIKOYAT: iteratsiya paytida o'chirish
for (OrderLine line : order.getLines()) {
    if (line.getQuantity() == 0) {
        order.getLines().remove(line);   // ConcurrentModificationException
    }
}
```

Sonar `for-each` ichida xuddi shu to'plamga modifikatsiya chaqirig'ini ko'radi. Xato ba'zan chiqmaydi, masalan oxirgidan bitta oldingi elementda, shuning uchun test yashil bo'lib production da tushadi.

```java
// TUZATILGAN: removeIf yoki Iterator
order.getLines().removeIf(line -> line.getQuantity() == 0);
```

Filtrlash uchun `removeIf` yoki yangi ro'yxat yig'ishni ishlating.

## 25.12 Collectors.toMap da takroriy kalit

```java
// SHIKOYAT: bir SKU bir necha qatorda uchraydi
Map<String, Integer> stock = lines.stream()
        .collect(Collectors.toMap(
                StockLine::getSku,
                StockLine::getQuantity));   // IllegalStateException
```

Ikki argumentli `toMap` takroriy kalitda istisno tashlaydi va Sonar merge funksiyasi yo'qligini xavf deb belgilaydi. Ombor hisobotida bitta SKU bir necha javonda turishi odatiy hol, demak bu xato ertami kechmi chiqadi.

```java
// TUZATILGAN: merge mantiqi aniq ko'rsatilgan
Map<String, Integer> stock = lines.stream()
        .collect(Collectors.toMap(
                StockLine::getSku,
                StockLine::getQuantity,
                Integer::sum));
```

`toMap` ni har doim uchinchi, merge argumenti bilan yozing.

## 25.13 Sanani noto'g'ri formatlash va SimpleDateFormat ni baham ko'rish

```java
// SHIKOYAT: static va thread-safe emas, format naqshi ham xato
private static final SimpleDateFormat FMT =
        new SimpleDateFormat("YYYY-mm-DD");   // yil, daqiqa, kun xato
public String settlementDay(Date d) {
    return FMT.format(d);
}
```

Sonar ikki narsani belgilaydi: thread-safe bo'lmagan obyekt static maydonda saqlanmoqda va format naqshi mantiqan xato. `YYYY` hafta asosidagi yil, `mm` daqiqa, `DD` yil kuni, demak yil oxirida to'lov kuni butunlay boshqa chiqadi.

```java
// TUZATILGAN: immutable formatter va to'g'ri naqsh
private static final DateTimeFormatter FMT =
        DateTimeFormatter.ofPattern("yyyy-MM-dd");
public String settlementDay(LocalDate d) {
    return FMT.format(d);
}
```

`java.time` ga o'ting, `DateTimeFormatter` immutable va thread-safe.

## 25.14 compareTo va equals nomuvofiqligi

```java
// SHIKOYAT: compareTo faqat summani, equals esa id ni solishtiradi
public int compareTo(Payment other) {
    return amount.compareTo(other.amount);
}
@Override public boolean equals(Object o) {
    return o instanceof Payment p && id.equals(p.id);
}
```

Sonar `Comparable` va `equals` kontraktlari mos kelmasligini aytadi. `TreeSet` tenglikni `compareTo` orqali aniqlaydi, shuning uchun bir xil summali ikki boshqa to'lovdan bittasi yo'qoladi.

```java
// TUZATILGAN: compareTo tartibni, equals identifikatorni, ikkisi mos
public int compareTo(Payment other) {
    int byAmount = amount.compareTo(other.amount);
    return byAmount != 0 ? byAmount : id.compareTo(other.id);
}
```

Tartiblash kaliti oxirida identifikatorni qo'shib, nol faqat haqiqiy tenglikda chiqishini ta'minlang.

## 25.15 Sikl o'zgaruvchisini ichkarida o'zgartirish yoki cheksiz sikl xavfi

```java
// SHIKOYAT: counter tanada o'zgartirilgan, shart esa o'zgarmaydi
for (int i = 0; i < lines.size(); i++) {
    if (lines.get(i).isCancelled()) {
        i++;                 // qator o'tkazib yuboriladi
    }
}
int attempt = 0;
while (attempt < maxAttempts) {
    send(payment);           // attempt hech qachon oshmaydi
}
```

Birinchi holatda Sonar sikl counteri tanada o'zgartirilganini, ikkinchisida sikl shartiga ta'sir qiluvchi hech narsa o'zgarmasligini aniqlaydi. Cheksiz sikl to'lov yuborishni takrorlab, bir buyurtmani o'nlab marta hisobdan chiqarishi mumkin.

```java
// TUZATILGAN: niyat aniq ifodalangan
lines.stream().filter(line -> !line.isCancelled()).forEach(this::ship);
for (int attempt = 1; attempt <= maxAttempts; attempt++) {
    if (send(payment)) {
        return;
    }
}
```

Sikl o'rniga stream yoki aniq qadamli `for` yozing, counter faqat bitta joyda o'zgarsin.

## 25.16 Tuzoq va yechim

| Tuzoq | Nega yuzaga keladi | Yechim |
|---|---|---|
| Bug ni `@SuppressWarnings` bilan yopish | tezda yashil gate kerak | sababini tuzatish, bostirishni code review da taqiqlash |
| Null tekshiruvni hamma joyga qo'shish | oqim tahlili tushunmaydi | `Optional` va `@Nullable` bilan kontraktni aniq qilish |
| Resurs qoidasini faqat SonarLint da ko'rish | lokal profil farq qiladi | profilni serverdan ulash, `sonar.qualityProfile` ni bir xil tutish |
| Test yozmasdan bug ni tuzatish | issue yopildi deb hisoblash | har bir reliability tuzatishga regress test qo'shish |
| `double` ni faqat yangi kodda almashtirish | migratsiya qiyin ko'rinadi | DTO chegarasida konvertatsiya qilib, ichkarida `BigDecimal` saqlash |
| Cheksiz sikl ni timeout bilan yashirish | simptom yo'qoladi | shartni o'zgartiruvchi qadamni siklga qaytarish |

## 25.17 Oddiy yondashuv va arxitektor yondashuvi

| Mavzu | Oddiy yondashuv | Arxitektor yondashuvi |
|---|---|---|
| Null | kerak joyda `if (x != null)` | kontraktda `Optional`, chegarada validatsiya |
| Pul turi | `double` yetadi | `BigDecimal` va bazada `numeric`, konvertatsiya bitta joyda |
| Resurs | `finally` da `close()` | try-with-resources majburiy, ArchUnit bilan nazorat |
| Tenglik | `==` tez yozish | `Objects.equals`, qiymat obyekti `record` |
| Istisno | `catch (Exception e) { log }` | tur bo'yicha ushlash, interrupt holatini tiklash |
| Takroriy kalit | ishlayapti, demak yo'q | `toMap` da merge funksiyasi standart talab |
| Bug ni yopish | bostirish annotatsiyasi | sababni tuzatish, regress test, gate o'zgarmaydi |
| Qoidalar to'plami | default profil | loyiha profili versiyalanadi va o'zgarishi review qilinadi |
| O'lchov | umumiy issue soni | yangi kod reliability rating va bug soni |

## 25.18 Katalogni loyihada tekshirish

Bu holatlarni qo'lda qidirmang, skan natijasini yangi kod bo'yicha filtrlang.

```bash
# faqat yangi kod bo'yicha skan, PR branch uchun
./mvnw -B verify sonar:sonar \
  -Dsonar.projectKey=payment-service \
  -Dsonar.pullrequest.key="$PR_NUMBER" \
  -Dsonar.pullrequest.branch="$BRANCH" \
  -Dsonar.pullrequest.base=main
```

```properties
# sonar-project.properties: reliability qoidalari uchun kerakli minimal sozlama
sonar.java.source=21
sonar.sources=src/main/java
sonar.tests=src/test/java
sonar.coverage.jacoco.xmlReportPaths=target/site/jacoco/jacoco.xml
sonar.qualitygate.wait=true
```

```xml
<!-- JaCoCo hisoboti bo'lmasa Sonar coverage ni nol deb ko'rsatadi -->
<plugin>
  <groupId>org.jacoco</groupId>
  <artifactId>jacoco-maven-plugin</artifactId>
  <version>0.8.12</version>
  <executions>
    <execution><goals><goal>prepare-agent</goal></goals></execution>
    <execution><id>report</id><phase>verify</phase>
      <goals><goal>report</goal></goals></execution>
  </executions>
</plugin>
```

```yaml
# CI: gate qizil bo'lsa pipeline to'xtaydi
jobs:
  sonar:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with: { fetch-depth: 0 }   # yangi kod hisobi uchun butun tarix kerak
      - run: ./mvnw -B verify sonar:sonar
        env:
          SONAR_TOKEN: ${{ secrets.SONAR_TOKEN }}
```

Har bir tuzatishga test kerak, lekin test uslublari [testlash qo'llanmasidagi](../testing/README.md) unit test va Testcontainers mavzularida yoritilgan.

## 25.19 Amalda qo'llash

- [ ] Faol quality profile dan reliability qoidalari ro'yxatini eksport qilib, bu katalogdagi 14 holat yoqilganini tekshiring.
- [ ] Repository va servis metodlarida `null` qaytaradigan signaturalarni `Optional` ga o'tkazing va `get()` chaqiruvlarini `orElseThrow` ga almashtiring.
- [ ] Kod bazasida `new SimpleDateFormat` va `static` formatter maydonlarini qidirib, `DateTimeFormatter` ga ko'chiring.
- [ ] Pul maydonlarini sanab chiqing: `double` yoki `float` bo'lsa `BigDecimal` ga, bazada `numeric(19,4)` ga o'tkazing.
- [ ] Barcha `Collectors.toMap` chaqiruvlariga merge funksiyasi qo'shing yoki `groupingBy` ga almashtiring.
- [ ] `catch (InterruptedException` ni qidirib, har birida `Thread.currentThread().interrupt()` borligini tasdiqlang.
- [ ] Har bir yopilgan reliability issue uchun xatoni qayta chiqaradigan regress test yozib, uni PR ga qo'shing.
- [ ] Quality gate ga "yangi kod bug soni = 0" shartini qo'ying va `sonar.qualitygate.wait=true` bilan pipeline ni bloklang.

---

[&larr; 24. False positive, suppression va o'z qoidangiz](24-false-positive-suppression-va-oz-qoidangiz.md) · [Mundarija](README.md) · [26. Xato katalogi: security &rarr;](26-xato-katalogi-security-vulnerability-va.md)
