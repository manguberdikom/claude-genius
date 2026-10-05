<!-- doc: sonarqube | chapter: 41 | part: X. Amaliy ma'lumotnoma -->

[Barcha hujjatlar](../../README.md) / [SonarQube](README.md)

# 41. Lombok, record va generatsiya qilingan kod (Lombok, Records and Generated Code)

<details>
<summary>Bu bobdagi 13 bo'lim</summary>

- [41.1 Lombok qanday ishlaydi: annotatsiya ishlovchisi va yaratilgan bytecode](#411-lombok-qanday-ishlaydi-annotatsiya-ishlovchisi-va-yaratilgan-bytecode)
- [41.2 Lombok generatsiya qilgan metodlar qamrovga qanday tushadi](#412-lombok-generatsiya-qilgan-metodlar-qamrovga-qanday-tushadi)
- [41.3 `lombok.config` va generatsiya qilingan kodni belgilash](#413-lombokconfig-va-generatsiya-qilingan-kodni-belgilash)
- [41.4 JaCoCo generatsiya qilingan kodni filtrlash sharti](#414-jacoco-generatsiya-qilingan-kodni-filtrlash-sharti)
- [41.5 `@Data` ning yashirin xavflari: `equals`, `hashCode` va entity](#415-data-ning-yashirin-xavflari-equals-hashcode-va-entity)
- [41.6 `@Builder` va majburiy maydonlar tekshiruvi](#416-builder-va-majburiy-maydonlar-tekshiruvi)
- [41.7 `@Slf4j` va loglash qoidalari](#417-slf4j-va-loglash-qoidalari)
- [41.8 Java record: Lombok ga nisbatan afzalligi va qamrovdagi farqi](#418-java-record-lombok-ga-nisbatan-afzalligi-va-qamrovdagi-farqi)
- [41.9 MapStruct va boshqa generatorlar: chiqarilgan fayllarni tahlildan olib tashlash](#419-mapstruct-va-boshqa-generatorlar-chiqarilgan-fayllarni-tahlildan-olib-tashlash)
- [41.10 `target/generated-sources` ni to'g'ri sozlash](#4110-targetgenerated-sources-ni-togri-sozlash)
- [41.11 OpenAPI va protobuf dan yaratilgan klasslar](#4111-openapi-va-protobuf-dan-yaratilgan-klasslar)
- [41.12 Lombok dan voz kechish qarori: qachon mantiqiy](#4112-lombok-dan-voz-kechish-qarori-qachon-mantiqiy)
- [41.13 Amalda qo'llash](#4113-amalda-qollash)

</details>



Generatsiya qilingan kod Sonar hisobotida eng ko'p chalkashlik tug'diradigan joy. Developer `@Data` yozadi, keyin coverage hisobotida o'zi yozmagan o'nlab satr "qoplanmagan" deb turganini ko'radi. Buning sababi oddiy: JaCoCo bytecode ni o'lchaydi, Sonar esa manba kodni tahlil qiladi, va Lombok bu ikki qatlam orasiga tushadi. Bu bobda shu uzilishni qanday boshqarish, qaysi sozlama nimani hal qiladi va qaysi annotatsiya qamrovdan tashqari haqiqiy xavf olib kelishini ko'rib chiqamiz.

## 41.1 Lombok qanday ishlaydi: annotatsiya ishlovchisi va yaratilgan bytecode

Lombok oddiy annotatsiya ishlovchisi emas. Standart `javax.annotation.processing` ishlovchisi yangi fayl yaratadi, Lombok esa kompilyator ichidagi AST ni bevosita o'zgartiradi. Ya'ni `@Getter` yozilgan klassning manba fayli hech qachon o'zgarmaydi, lekin `javac` chiqargan `.class` faylida `getAmount()` metodi paydo bo'ladi.

Bundan ikki muhim natija kelib chiqadi. Birinchisi: diskda ko'rib chiqadigan "generatsiya qilingan fayl" yo'q, shuning uchun `sonar.exclusions` bilan Lombok kodini chetlab o'tolmaysiz. Ikkinchisi: Lombok `javac` ning ichki API lariga tayanadi, shuning uchun har bir yangi JDK major versiyasi Lombok ning yangilanishini talab qiladi.

```java
// Manba kodda siz yozgan narsa: 4 qator
@Getter
@RequiredArgsConstructor
public class PaymentRequest {
    private final String orderId;
    private final BigDecimal amount;
}

// Bytecode da kompilyatordan chiqqan narsa (delombok ko'rinishi):
public class PaymentRequest {
    private final String orderId;
    private final BigDecimal amount;

    public PaymentRequest(String orderId, BigDecimal amount) {
        this.orderId = orderId;   // JaCoCo buni instrumentatsiya qiladi
        this.amount = amount;
    }

    public String getOrderId() { return this.orderId; }       // alohida metod
    public BigDecimal getAmount() { return this.amount; }     // alohida metod
}
```

Haqiqiy bytecode ni ko'rish uchun `delombok` dan foydalanish eng ishonchli usul. Shubha tug'ilganda taxmin qilmasdan chiqishni ko'rib oling.

```bash
# Lombok nima generatsiya qilganini aynan ko'rish
java -jar lombok.jar delombok src/main/java -d build/delomboked

# Yoki bytecode darajasida tekshirish
javap -p -c target/classes/com/shop/payment/PaymentRequest.class | head -40
```

## 41.2 Lombok generatsiya qilgan metodlar qamrovga qanday tushadi

JaCoCo Java agenti sifatida ishlaydi va klasslar yuklanayotganda bytecode ga hisoblagich qo'yadi. Unga metod qo'lda yozilgani yoki Lombok tomonidan qo'shilgani ahamiyatsiz. Shuning uchun sozlamasiz holatda `@Data` bilan belgilangan DTO qamrov hisobotiga o'nlab branch bilan kiradi.

Eng og'ir hissani `equals` va `hashCode` qo'shadi. Lombok generatsiya qilgan `equals` har bir maydon uchun `null` tekshiruvi va taqqoslash shoxlarini yozadi. Besh maydonli DTO da bu yigirmadan oshiq branch beradi va ularning hammasini test bilan qoplash uchun keraksiz mehnat ketadi.

Natija shunday bo'ladi: loyihada mazmunli biznes mantiq yaxshi qoplangan, lekin umumiy coverage raqami past, chunki yuzlab DTO getter va `equals` shoxlari hisobni pasaytiradi. Aks holat ham xavfli: agar kimdir DTO lar uchun `equals` ni to'liq sinaydigan testlar yozsa, coverage ko'tariladi, lekin bu testlar bitta ham xatoni tutmaydi.

```java
// SONAR VA JACOCO UCHUN ZARARLI TEST: raqamni ko'taradi, qiymat bermaydi
@Test
void gettersAndEqualsWork() {
    OrderDto a = new OrderDto("ORD-1", BigDecimal.TEN, "NEW");
    OrderDto b = new OrderDto("ORD-1", BigDecimal.TEN, "NEW");
    assertThat(a).isEqualTo(b);
    assertThat(a.hashCode()).isEqualTo(b.hashCode());
    assertThat(a.getOrderId()).isEqualTo("ORD-1");   // getter ni sinash
    assertThat(a.toString()).contains("ORD-1");      // toString ni sinash
}
```

To'g'ri yechim bu testni yozish emas, balki generatsiya qilingan kodni qamrov o'lchovidan chiqarib tashlash. Testni faqat o'zingiz yozgan mantiq uchun yozing.

## 41.3 `lombok.config` va generatsiya qilingan kodni belgilash

Lombok generatsiya qilgan a'zolarga maxsus annotatsiya qo'yishi mumkin. Bu `lombok.config` faylidagi bitta kalit bilan yoqiladi va keyinchalik barcha filtrlashning asosi bo'ladi. Fayl loyiha ildiziga qo'yiladi va papkalar ierarxiyasi bo'ylab pastga tarqaladi.

```properties
# Loyiha ildizidagi lombok.config
# Yuqoridagi papkalardan sozlama qidirishni to'xtatish
config.stopBubbling = true

# Eng muhim kalit: generatsiya qilingan a'zolarga @lombok.Generated qo'yish
lombok.addLombokGeneratedAnnotation = true

# @Data ni butunlay taqiqlash yoki ogohlantirish berish
lombok.data.flagUsage = WARNING

# Entity da xavfli bo'lgan annotatsiyalarni cheklash
lombok.allArgsConstructor.flagUsage = WARNING
lombok.val.flagUsage = WARNING

# equals/hashCode da ota klassni chaqirishni majburlash
lombok.equalsAndHashCode.callSuper = CALL

# Setter va getter uchun avtomatik @SuppressWarnings qo'yilishini boshqarish
lombok.addSuppressWarnings = true
```

`lombok.addLombokGeneratedAnnotation = true` kalitini yoqmaguningizcha hech qanday filtr ishlamaydi. Ko'p loyihalarda coverage bilan muammo aynan shu bitta qatorning yo'qligidan kelib chiqadi.

`flagUsage` kalitlari alohida e'tiborga loyiq. Ular Sonar qoidasi emas, balki kompilyator ogohlantirishi darajasida ishlaydi. Agar jamoada `@Data` ni entity da ishlatmaslik qarori bo'lsa, bu kalit o'sha qarorni code review ga tashlab qo'ymasdan avtomatlashtiradi.

## 41.4 JaCoCo generatsiya qilingan kodni filtrlash sharti

JaCoCo `@Generated` annotatsiyasi bilan belgilangan klass va metodlarni hisobotdan chiqarib tashlaydi. Filtr ishlashi uchun uch shart bir vaqtda bajarilishi kerak.

Birinchi shart: annotatsiyaning oddiy nomi aynan `Generated` bo'lishi kerak. Paketi ahamiyatsiz, `lombok.Generated` ham, `javax.annotation.processing.Generated` ham ishlaydi. Ikkinchi shart: annotatsiyaning retention siyosati `CLASS` yoki `RUNTIME` bo'lishi kerak, chunki `SOURCE` retention bytecode ga yetib bormaydi. Uchinchi shart: JaCoCo versiyasi bu filtrni qo'llab-quvvatlashi kerak.

Mana bu yerda halol bo'lish kerak. Bu filtr JaCoCo 0.8.x liniyasida mavjud, lekin aniq qaysi kichik versiyada qaysi holat qo'shilgani (Lombok, record, `switch` ustidagi sintetik kod) versiyadan versiyaga o'zgargan. Shuning uchun hujjatdagi raqamga ishonmasdan, o'z loyihangizda tekshirib ko'ring.

```xml
<!-- JaCoCo versiyasini aniq qotirish va hisobotni XML da chiqarish -->
<plugin>
    <groupId>org.jacoco</groupId>
    <artifactId>jacoco-maven-plugin</artifactId>
    <version>0.8.12</version>
    <executions>
        <execution>
            <id>prepare-agent</id>
            <goals><goal>prepare-agent</goal></goals>
        </execution>
        <execution>
            <id>report</id>
            <phase>verify</phase>
            <!-- Sonar aynan XML hisobotni o'qiydi -->
            <goals><goal>report</goal></goals>
        </execution>
    </executions>
</plugin>
```

Tekshirish usuli juda sodda va men har bir loyihada shuni qilishni tavsiya qilaman. `mvn verify` dan keyin `target/site/jacoco/jacoco.xml` ichida DTO klassingiz nomini qidiring.

```bash
# @Data bilan belgilangan klass hisobotga tushgan yoki yo'q
grep -c 'name="getOrderId"' target/site/jacoco/jacoco.xml
# 0 chiqsa filtr ishlayapti, 1 chiqsa lombok.config yoki versiya muammosi bor

# Sonar bu faylni ko'rishi uchun yo'l to'g'ri ko'rsatilganini tasdiqlash
mvn -q sonar:sonar -Dsonar.verbose=true 2>&1 | grep -i jacoco
```

Sonar tomonidan ham shuni bilish kerak: Sonar coverage ni o'zi o'lchamaydi, faqat JaCoCo XML ni o'qiydi. Demak JaCoCo filtrladi degani Sonar ham ko'rmaydi degani. Buni `sonar.coverage.jacoco.xmlReportPaths` parametri bilan bog'laysiz.

## 41.5 `@Data` ning yashirin xavflari: `equals`, `hashCode` va entity

`@Data` qamrovdan ham kattaroq muammo olib keladi. U `equals`, `hashCode`, `toString`, barcha getter va setter larni birdan generatsiya qiladi. JPA entity da bu uchta alohida xatoga olib boradi.

Birinchi xato: `hashCode` o'zgaruvchan maydonlarga tayanadi. Entity ni `HashSet` ga qo'shib, keyin maydonini o'zgartirsangiz, obyekt o'z to'plamida topilmay qoladi. Ikkinchi xato: `toString` bog'langan kolleksiyalarni chaqiradi va lazy yuklashni ishga tushiradi, ikki tomonlama bog'lanishda esa cheksiz rekursiyaga olib keladi. Uchinchi xato: `equals` barcha maydonni taqqoslaydi, bu esa proxy obyekt bilan noto'g'ri ishlaydi.

```java
// SONAR VA HIBERNATE SHIKOYAT QILADIGAN VARIANT
@Entity
@Data                       // equals/hashCode barcha maydon ustidan
public class Order {
    @Id @GeneratedValue
    private Long id;
    private String status;
    @OneToMany(mappedBy = "order")
    private List<OrderLine> lines;   // toString bu yerda lazy ni ochadi
}
```

Tuzatilgan variantda generatsiyani faqat xavfsiz qismga cheklaymiz va tenglikni biznes kaliti ustiga qo'yamiz.

```java
@Entity
@Getter
@Setter
@ToString(onlyExplicitlyIncluded = true)   // kolleksiya chiqmaydi
public class Order {
    @Id @GeneratedValue
    private Long id;

    @ToString.Include
    @Column(nullable = false, unique = true)
    private String orderNumber;             // o'zgarmas biznes kaliti

    @OneToMany(mappedBy = "order")
    private List<OrderLine> lines = new ArrayList<>();

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        // proxy bilan ishlash uchun getClass emas, instanceof
        if (!(o instanceof Order other)) return false;
        return orderNumber != null && orderNumber.equals(other.orderNumber);
    }

    @Override
    public int hashCode() {
        return Objects.hash(orderNumber);   // barqaror, o'zgarmaydi
    }
}
```

Bu variantda `equals` va `hashCode` qo'lda yozilgani uchun ular `@Generated` bilan belgilanmaydi va qamrovga tushadi. Bu to'g'ri, chunki ular endi sizning biznes qaroringiz va sinovga arziydi. Sonar ham merosxo'r klass maydon qo'shsa `equals` ni qayta aniqlashni talab qiladigan qoidani (`java:S2160`) shu holatda tinch qoldiradi.

## 41.6 `@Builder` va majburiy maydonlar tekshiruvi

`@Builder` hech qanday tekshiruv generatsiya qilmaydi. `Order.builder().build()` chaqirig'i barcha maydon `null` bo'lgan obyekt qaytaradi va kompilyator qarshilik ko'rsatmaydi. Sonar ham buni ko'rmaydi, chunki builder kodi manba faylda yo'q.

Yana bir tuzoq: `@Builder` maydon initsializatorini e'tiborsiz qoldiradi. `private List<Item> items = new ArrayList<>();` yozsangiz ham builder orqali yaratilgan obyektda u `null` bo'ladi. Buni `@Builder.Default` hal qiladi.

```java
public class PaymentCommand {
    private final String orderId;
    private final BigDecimal amount;
    private final Currency currency;

    @Builder.Default                       // bo'lmasa builder da null bo'ladi
    private final List<String> tags = List.of();

    // Builder ni konstruktor ustiga qo'yamiz, tekshiruv shu yerda bajariladi
    @Builder
    private PaymentCommand(String orderId, BigDecimal amount,
                           Currency currency, List<String> tags) {
        this.orderId = Objects.requireNonNull(orderId, "orderId majburiy");
        this.currency = Objects.requireNonNull(currency, "currency majburiy");
        if (amount == null || amount.signum() <= 0) {
            throw new IllegalArgumentException("amount musbat bo'lishi kerak");
        }
        this.amount = amount;
        this.tags = List.copyOf(tags);
    }
}
```

Bu yondashuvning yana bir foydasi bor. Konstruktordagi tekshiruv shoxlari sizning kodingiz hisoblanadi va ularni test bilan qoplash mantiqiy. Ya'ni coverage raqami endi haqiqiy himoyani o'lchaydi.

## 41.7 `@Slf4j` va loglash qoidalari

`@Slf4j` `private static final Logger log` maydonini generatsiya qiladi. Bu Sonar ning logger uchun ko'rinish va modifikator talab qiladigan qoidasini (`java:S1312`) avtomatik qondiradi. Shuning uchun `@Slf4j` Sonar nuqtai nazaridan qo'lda yozilgan loggerdan xavfsizroq.

Lekin `@Slf4j` loglash mazmunini tuzatmaydi. Sonar ikki narsaga e'tibor beradi: `System.out` ishlatilishiga (`java:S106`) va log argumentida qimmat hisoblash bajarilishiga (`java:S2629`). Ikkinchisi eng ko'p uchraydi.

```java
@Slf4j
@Service
public class StockService {

    public void reserve(String sku, int qty) {
        // YOMON: satr birlashtirish log o'chirilgan bo'lsa ham bajariladi
        log.debug("Zaxira band qilinmoqda: " + sku + ", miqdor: " + qty);

        // YOMON: metod chaqirig'i log darajasidan qat'i nazar ishlaydi
        log.debug("Ombor holati: " + buildWarehouseSnapshot());

        // TO'G'RI: placeholder, argument faqat kerak bo'lganda hisoblanadi
        log.debug("Zaxira band qilinmoqda: sku={}, miqdor={}", sku, qty);

        // TO'G'RI: qimmat hisoblash shart ostida
        if (log.isDebugEnabled()) {
            log.debug("Ombor holati: {}", buildWarehouseSnapshot());
        }

        // TO'G'RI: istisnoni oxirgi argument sifatida berish, konkatenatsiya yo'q
        try {
            applyReservation(sku, qty);
        } catch (StockException e) {
            log.error("Band qilish muvaffaqiyatsiz: sku={}", sku, e);
        }
    }
}
```

Loggerni testda tekshirish kerak degan talab odatda noto'g'ri. Log chiqishi biznes shart emas, shuning uchun uni sinash coverage ni ko'taradi va boshqa hech narsa bermaydi. Istisno: audit log huquqiy talab bo'lsa, u holda u biznes mantiq va sinalishi kerak.

## 41.8 Java record: Lombok ga nisbatan afzalligi va qamrovdagi farqi

Record Java 16 dan beri til qismi. Uning `equals`, `hashCode`, `toString` va accessor metodlari Lombok emas, kompilyatorning o'zi tomonidan generatsiya qilinadi. Bu juda muhim farq: tashqi kutubxona kerak emas, IDE qo'shimcha plagin so'ramaydi va yangi JDK chiqqanda hech narsa buzilmaydi.

Qamrov tomonidan ham record qulayroq. JaCoCo 0.8.x liniyasi record ning generatsiya qilingan metodlarini filtrlaydi, chunki kompilyator ularni sintetik sifatida belgilaydi. Bu yerda ham aniq versiyani tekshirish kerak, chunki qo'llab-quvvatlash bosqichma-bosqich qo'shilgan.

```java
// DTO uchun record: lombok.config kerak emas, filtr avtomatik ishlaydi
public record OrderSummary(
        String orderNumber,
        BigDecimal total,
        OrderStatus status) {

    // Kompakt konstruktor: tekshiruv shu yerda, bu SIZNING kodingiz
    public OrderSummary {
        Objects.requireNonNull(orderNumber, "orderNumber majburiy");
        if (total == null || total.signum() < 0) {
            throw new IllegalArgumentException("total manfiy bo'lmasin");
        }
    }

    // Hisoblangan qiymat: sinovga arziydigan yagona qism
    public boolean isSettled() {
        return status == OrderStatus.PAID || status == OrderStatus.REFUNDED;
    }
}
```

Record qaerda ishlamaydi: JPA entity sifatida. Entity ga argumentsiz konstruktor va o'zgaruvchan maydon kerak, record esa ikkisini ham bermaydi. Shuning uchun amaliy chiziq shunday: entity da Lombok ning tanlangan annotatsiyalari, DTO, command, event va projection da record.

| Tuzoq | Nima bo'ladi | Yechim |
| --- | --- | --- |
| `lombok.config` da `addLombokGeneratedAnnotation` yo'q | JaCoCo getter va `equals` ni qoplanmagan deb sanaydi | Faylni loyiha ildiziga qo'yib kalitni `true` qilish |
| JaCoCo versiyasi eski | Filtr umuman ishlamaydi, sozlama bekor | Versiyani 0.8.x da qotirish va `jacoco.xml` ni grep bilan tekshirish |
| Entity ustida `@Data` | `HashSet` buziladi, lazy yuklash portlaydi | `@Getter`/`@Setter` va biznes kaliti ustida qo'lda `equals` |
| `@Builder` da `@Builder.Default` yo'q | Kolleksiya maydoni `null` bo'ladi, `NullPointerException` | Initsializator bo'lgan har bir maydonga `@Builder.Default` |
| Builder da tekshiruv yo'q | Yarim bo'sh obyekt bazagacha boradi | `@Builder` ni private konstruktor ustiga qo'yish |
| `log.debug("x" + y)` | Log o'chirilgan bo'lsa ham hisoblash ketadi, Sonar issue beradi | Placeholder va `isDebugEnabled` shart |
| `generated-sources` Sonar ga kirgan | MapStruct impl kodi smell va past qamrov beradi | `sonar.exclusions` va `sonar.coverage.exclusions` |
| `sonar.exclusions` ga ishonib coverage kutish | Fayl tahlildan chiqadi, lekin eski coverage qoladi | Ikki parametrni alohida sozlash |
| DTO uchun getter testi yozish | Coverage ko'tariladi, xato tutilmaydi | Generatsiyani filtrlab, testni mantiq uchun yozish |

## 41.9 MapStruct va boshqa generatorlar: chiqarilgan fayllarni tahlildan olib tashlash

MapStruct Lombok dan farq qiladi. U haqiqiy `.java` faylini `target/generated-sources/annotations` ichida yaratadi. Agar bu papka Sonar ga manba sifatida ko'rsatilgan bo'lsa, Sonar o'sha faylni oddiy kod deb tahlil qiladi va juda ko'p issue beradi.

Yaxshi xabar shuki, MapStruct Java 9 dan boshlab generatsiya qilgan klassga `javax.annotation.processing.Generated` annotatsiyasini qo'yadi. Demak JaCoCo filtri uni ham tanib oladi. Yomon xabar shuki, Sonar ning o'z qoidalari annotatsiyaga qarab o'chmaydi, ular uchun chiqarib tashlash shablonini yozish kerak.

```properties
# sonar-project.properties yoki pom.xml dagi properties bo'limi

# Tahlildan butunlay chiqarish: issue ham, duplication ham hisoblanmaydi
sonar.exclusions=\
  **/generated/**,\
  **/generated-sources/**,\
  **/*MapperImpl.java,\
  **/com/shop/api/client/**,\
  **/*OuterClass.java

# Faqat qamrov o'lchovidan chiqarish, qoidalar baribir ishlaydi
sonar.coverage.exclusions=\
  **/dto/**,\
  **/config/**,\
  **/*Application.java,\
  **/generated/**

# Dublikat kod o'lchovidan chiqarish (protobuf uchun ayniqsa kerak)
sonar.cpd.exclusions=**/generated/**,**/*OuterClass.java

# JaCoCo hisobotining yo'li
sonar.coverage.jacoco.xmlReportPaths=target/site/jacoco/jacoco.xml
```

Ikki parametr orasidagi farqni aniq tushunish kerak. `sonar.exclusions` faylni butunlay ko'rinmas qiladi. `sonar.coverage.exclusions` faylni tahlilda qoldiradi, lekin uning qamrovini hisobga olmaydi. Entity va DTO uchun ko'pincha ikkinchisi kerak, chunki Sonar ularda `null` xavfini topishi mumkin.

MapStruct ning o'zini ham sozlash foydali. Timestamp ni o'chirish generatsiya chiqishini barqaror qiladi va keraksiz diff ni yo'qotadi.

```xml
<plugin>
    <groupId>org.apache.maven.plugins</groupId>
    <artifactId>maven-compiler-plugin</artifactId>
    <configuration>
        <annotationProcessorPaths>
            <!-- Tartib muhim: Lombok MapStruct dan oldin kelishi kerak -->
            <path>
                <groupId>org.projectlombok</groupId>
                <artifactId>lombok</artifactId>
                <version>${lombok.version}</version>
            </path>
            <path>
                <groupId>org.projectlombok</groupId>
                <artifactId>lombok-mapstruct-binding</artifactId>
                <version>0.2.0</version>
            </path>
            <path>
                <groupId>org.mapstruct</groupId>
                <artifactId>mapstruct-processor</artifactId>
                <version>${mapstruct.version}</version>
            </path>
        </annotationProcessorPaths>
        <compilerArgs>
            <arg>-Amapstruct.suppressGeneratorTimestamp=true</arg>
            <arg>-Amapstruct.unmappedTargetPolicy=ERROR</arg>
        </compilerArgs>
    </configuration>
</plugin>
```

`unmappedTargetPolicy=ERROR` alohida qimmatli. U Sonar qoidasi emas, lekin unutilgan maydon tufayli kelib chiqadigan xatoni build vaqtida tutadi. Bu Sonar dan ham kuchli himoya, chunki u statik tahlilga umuman yetib bormaydigan toifadagi xatoni to'xtatadi.

## 41.10 `target/generated-sources` ni to'g'ri sozlash

Maven standart holatda `target/generated-sources/annotations` ni kompilyatsiyaga qo'shadi, lekin uni `sonar.sources` ga qo'shmaydi. Shuning uchun ko'p loyihada MapStruct impl fayllari Sonar ga tushmaydi. Muammo odatda `build-helper-maven-plugin` yoki OpenAPI generator qo'lda qo'shgan manba papkasidan kelib chiqadi.

Tekshirish usuli: Sonar skanerining log ida indekslangan fayl sonini ko'ring. Agar `target` ichidan fayl indekslanayotgan bo'lsa, sozlama noto'g'ri.

```bash
# Qaysi fayllar indekslanayotganini ko'rish
mvn sonar:sonar -X 2>&1 | grep -E "Indexing|indexed" | head -20

# target ichidan nimadir kirganini tekshirish
mvn sonar:sonar -X 2>&1 | grep "target/generated"
```

Gradle da holat boshqacha. Gradle ning `sonarqube` yoki `sonar` plagini `sourceSets` dan manba papkalarini oladi, shuning uchun generatsiya qilingan papka ko'proq ehtimol bilan tahlilga tushadi. Buni aniq boshqarish kerak.

```properties
# gradle.properties yoki build skriptidagi sonar bloki uchun qiymatlar
systemProp.sonar.sources=src/main/java
systemProp.sonar.tests=src/test/java
systemProp.sonar.exclusions=**/generated/**,**/build/generated/**
systemProp.sonar.coverage.jacoco.xmlReportPaths=build/reports/jacoco/test/jacocoTestReport.xml
```

Ikki qurilish tizimi orasidagi bu farq amalda juda ko'p chalkashlik tug'diradi. Maven uchun yozilgan maqolani Gradle loyihasiga ko'chirganda chiqarib tashlash ishlamay qolishi odatiy hol.

## 41.11 OpenAPI va protobuf dan yaratilgan klasslar

OpenAPI generator va `protoc` bir xil muammoni keltiradi, lekin kattaroq miqyosda. Ular generatsiya qiladigan klasslar o'nlab ming qatorga yetadi va ularda Sonar juda ko'p issue topadi: uzun metodlar, yuqori kognitiv murakkablik (`java:S3776`), takrorlangan satr literallari (`java:S1192`), ishlatilmagan maydonlar (`java:S1068`).

Bu issue larni tuzatish mumkin emas, chunki kod har build da qaytadan yaratiladi. Shuning uchun yagona to'g'ri qaror ularni tahlildan chiqarish. Aytib o'tish kerak: bu halol qaror, "qoidani aylanib o'tish" emas, chunki siz o'zgartira olmaydigan kodga mas'ul emassiz.

Protobuf da yana bir nuqta bor. `*OuterClass` fayllari ichida bir xil shablon yuzlab marta takrorlanadi va bu loyihaning duplication ko'rsatkichini keskin buzadi. `sonar.cpd.exclusions` aynan shu holat uchun kerak.

Amaliy tavsiya: generatsiya chiqishini alohida Maven modulga yoki alohida paketga joylashtiring. Papka chizig'i aniq bo'lsa, chiqarib tashlash shabloni ham sodda va barqaror bo'ladi.

```xml
<!-- OpenAPI klientni alohida modulga chiqarish va uni Sonar dan olib tashlash -->
<plugin>
    <groupId>org.openapitools</groupId>
    <artifactId>openapi-generator-maven-plugin</artifactId>
    <configuration>
        <inputSpec>${project.basedir}/src/main/resources/payment-api.yaml</inputSpec>
        <generatorName>java</generatorName>
        <!-- Aniq paket: chiqarib tashlash shabloni shu nomga tayanadi -->
        <apiPackage>com.shop.generated.payment.api</apiPackage>
        <modelPackage>com.shop.generated.payment.model</modelPackage>
        <configOptions>
            <useJakartaEe>true</useJakartaEe>
            <library>resttemplate</library>
        </configOptions>
    </configuration>
</plugin>
```

Shu modulning `pom.xml` ida `sonar.skip=true` qo'ysangiz, modul butunlay tahlildan chiqadi. Bu eng toza chiziq, chunki bitta shablon xatosi tufayli asosiy kod ham tasodifan chiqib ketmaydi.

## 41.12 Lombok dan voz kechish qarori: qachon mantiqiy

Lombok dan voz kechish mafkuraviy masala emas, muhandislik hisobi. Uning foydasi aniq: kamroq yozish, kamroq shovqin. Narxi ham aniq: tashqi kutubxonaga va kompilyatorning ichki API lariga bog'liqlik.

Voz kechish mantiqiy bo'ladigan holatlar: kutubxona endi faqat `@Getter` va `@Slf4j` uchun ishlatilayotgan bo'lsa, loyiha har yili yangi JDK ga o'tadigan bo'lsa, yoki DTO larning katta qismi record ga aylantirilishi mumkin bo'lsa. Qolgan holatlarda Lombok ni tartibli sozlab ishlatish arzonroq.

Oraliq qaror ham bor va u ko'pincha eng amaliy. Lombok ni qoldirib, faqat xavfli annotatsiyalarni `lombok.config` orqali taqiqlang. Shunda jamoa `@Getter` qulayligini yo'qotmaydi, lekin `@Data` entity ga kirmaydi.

| Masala | Oddiy yondashuv | Arxitektor yondashuvi |
| --- | --- | --- |
| Lombok coverage ni pasaytirsa | DTO uchun getter testlari yoziladi | `lombok.config` va JaCoCo filtri sozlanadi, test yozilmaydi |
| Entity uchun annotatsiya | `@Data` hamma joyda | `@Getter`/`@Setter`, `equals` biznes kaliti ustida qo'lda |
| Lombok kalitlari | Faylsiz, har kim xohlaganini yozadi | `config.stopBubbling` bilan ildizda bitta `lombok.config` |
| Builder tekshiruvi | Builder dan keyin servisda `null` tekshirish | `@Builder` private konstruktor ustida, tekshiruv bir joyda |
| Generatsiya chiqishi | `target` ichida aralash turadi | Alohida modul yoki aniq paket, `sonar.skip` bilan ajratilgan |
| Chiqarib tashlash | `sonar.exclusions` ga hamma narsa tashlanadi | `exclusions`, `coverage.exclusions`, `cpd.exclusions` alohida |
| JaCoCo versiyasi | Parent pom dan nima kelsa shu | Versiya qotirilgan, filtr `jacoco.xml` da tasdiqlangan |
| DTO tanlovi | Lombok bilan klass | Record, Lombok faqat entity va service uchun |
| MapStruct xatosi | Issue Sonar dan kutiladi | `unmappedTargetPolicy=ERROR` bilan build da to'xtatiladi |
| JDK yangilanishi | Lombok buzilgach shoshilib tuzatiladi | Lombok ga bog'liqlik ro'yxatga olingan, record ga ko'chish rejada |

Oxirgi va eng muhim ogohlantirish. JaCoCo va Sonar ning Lombok hamda record ga munosabati versiyaga bog'liq, va bu bob yozilgandan keyin ham o'zgarishi mumkin. Shuning uchun bu yerdagi hech bir sozlamani ishonch asosida qabul qilmang. `jacoco.xml` ni ochib, o'z loyihangizda getter va `equals` metodlari hisobotga tushgan yoki tushmaganini o'z ko'zingiz bilan tekshiring.

## 41.13 Amalda qo'llash

- [ ] Loyiha ildiziga `lombok.config` yaratib, `config.stopBubbling = true` va `lombok.addLombokGeneratedAnnotation = true` kalitlarini qo'ying.
- [ ] `mvn verify` dan keyin `target/site/jacoco/jacoco.xml` ichida bitta DTO ning getter nomini grep bilan qidirib, filtr ishlayotganini tasdiqlang.
- [ ] JaCoCo plagin versiyasini pom da aniq qotiring va uni parent pom dan kelgan qiymatga tashlab qo'ymang.
- [ ] Barcha JPA entity da `@Data` ishlatilganini qidirib, ularni `@Getter`/`@Setter` va biznes kaliti ustidagi qo'lda `equals`/`hashCode` ga o'tkazing.
- [ ] `lombok.data.flagUsage = WARNING` kalitini yoqib, yangi `@Data` ishlatilishini build logida ko'rinadigan qiling.
- [ ] Har bir `@Builder` ni private konstruktor ustiga ko'chirib, majburiy maydonlar uchun `Objects.requireNonNull` tekshiruvini qo'shing va initsializatorli maydonlarga `@Builder.Default` qo'ying.
- [ ] `sonar.exclusions`, `sonar.coverage.exclusions` va `sonar.cpd.exclusions` ni alohida yozib, MapStruct, OpenAPI va protobuf chiqishini mos parametrga joylashtiring.
- [ ] `log.debug` va `log.info` chaqiriqlarida satr birlashtirish qolganini qidirib, ularni placeholder shakliga o'tkazing.

---

[&larr; 40. Sonar va boshqa vositalar: qachon qaysi biri](40-sonar-va-boshqa-vositalar-qachon-qaysi-biri.md) · [Mundarija](README.md) · [42. Diagnostika: tahlil ishlamaganda nima qilish &rarr;](42-diagnostika-tahlil-ishlamaganda-nima-qilish.md)
