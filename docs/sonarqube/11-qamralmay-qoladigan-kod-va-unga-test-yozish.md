<!-- doc: sonarqube | chapter: 11 | part: III. Qamrov (coverage) -->

[Barcha hujjatlar](../../README.md) / [SonarQube](README.md)

# 11. Qamralmay qoladigan kod va unga test yozish (Code That Stays Uncovered)

<details>
<summary>Bu bobdagi 15 bo'lim</summary>

- [11.1 Private konstruktorli utility klass va unga test yozish](#111-private-konstruktorli-utility-klass-va-unga-test-yozish)
- [11.2 `equals`, `hashCode`, `toString`: qamrash yoki record ga o'tish](#112-equals-hashcode-tostring-qamrash-yoki-record-ga-otish)
- [11.3 Getter va setter: nega ular qamrovni suyultiradi](#113-getter-va-setter-nega-ular-qamrovni-suyultiradi)
- [11.4 Istisno tarmoqlari: `catch` bloklarini qanday ishga tushirish](#114-istisno-tarmoqlari-catch-bloklarini-qanday-ishga-tushirish)
- [11.5 Mudofaa tekshiruvlari (`if (x == null) throw`): ularni sinash yoki olib tashlash](#115-mudofaa-tekshiruvlari-if-x--null-throw-ularni-sinash-yoki-olib-tashlash)
- [11.6 Konfiguratsiya klasslari va `@Bean` metodlari](#116-konfiguratsiya-klasslari-va-bean-metodlari)
- [11.7 Mapper va konvertorlar: qo'lda yozilgani va generatsiya qilingani](#117-mapper-va-konvertorlar-qolda-yozilgani-va-generatsiya-qilingani)
- [11.8 `main` metodi va Spring Boot ishga tushirish klassi](#118-main-metodi-va-spring-boot-ishga-tushirish-klassi)
- [11.9 Yetib bo'lmaydigan kod: uni test bilan emas, o'chirish bilan hal qilish](#119-yetib-bolmaydigan-kod-uni-test-bilan-emas-ochirish-bilan-hal-qilish)
- [11.10 Interfeys standart metodlari va abstrakt klasslar](#1110-interfeys-standart-metodlari-va-abstrakt-klasslar)
- [11.11 Qamrash qiyin kodni qayta loyihalash: dizayn signali sifatida qarash](#1111-qamrash-qiyin-kodni-qayta-loyihalash-dizayn-signali-sifatida-qarash)
- [11.12 Oddiy yondashuv va arxitektor yondashuvi](#1112-oddiy-yondashuv-va-arxitektor-yondashuvi)
- [11.13 Tuzoq va yechim](#1113-tuzoq-va-yechim)
- [11.14 Hisobotni tekshirish](#1114-hisobotni-tekshirish)
- [11.15 Amalda qo'llash](#1115-amalda-qollash)

</details>



Har bir loyihada coverage hisobotining pastida bir to'da klass turadi: ularga hech kim test yozmaydi, lekin ular quality gate raqamini pastga tortadi. Bu bobda shunday kodning har bir turini ko'ramiz: qayerda test kerak, qayerda dizaynni o'zgartirish arzonroq, qayerda esa eng to'g'ri yo'l kodni o'chirish. Asosiy qoida bitta: qamrash qiyin bo'lgan kod ko'pincha noto'g'ri joylashgan kod.

## 11.1 Private konstruktorli utility klass va unga test yozish

Sonar `java:S1118` qoidasi bilan faqat static metodli klassda private konstruktor talab qiladi. Siz uni qo'shasiz va JaCoCo darhol o'sha konstruktorni qamralmagan qator deb belgilaydi. Qoidani qondirish coverage ni buzadi: bu Sonar va JaCoCo o'rtasidagi eng mashhur ziddiyat.

```java
// Sonar S1118 shikoyat qiladi: default konstruktor ochiq qolgan
public final class MoneyUtils {
    public static BigDecimal withVat(BigDecimal net, BigDecimal rate) {
        return net.multiply(BigDecimal.ONE.add(rate));
    }
}

// Tuzatilgan variant: konstruktor yopildi
public final class MoneyUtils {
    private MoneyUtils() {
        // utility klass, instansiya yaratilmaydi
        throw new AssertionError("instansiya yaratish mumkin emas");
    }

    public static BigDecimal withVat(BigDecimal net, BigDecimal rate) {
        return net.multiply(BigDecimal.ONE.add(rate));
    }
}
```

Birinchi variant: reflection bilan konstruktorni ataylab chaqirish. Bu ishlaydi, lekin test xatti-harakatni tekshirmaydi, faqat raqamni bo'yaydi.

```java
@Test
void konstruktorYopiq() throws Exception {
    var ctor = MoneyUtils.class.getDeclaredConstructor();
    // modifikator chindan private ekanini tekshiramiz, bu ma'noli shart
    assertThat(Modifier.isPrivate(ctor.getModifiers())).isTrue();
    ctor.setAccessible(true);
    // chaqiruv AssertionError tashlashi kerak
    assertThatThrownBy(ctor::newInstance)
        .hasCauseInstanceOf(AssertionError.class);
}
```

Ikkinchi variant, va arxitektor tanlovi: utility klassni yo'q qilish. `MoneyUtils.withVat` aslida `Money` value object ning metodi. Shunda konstruktor bekor qator bo'lmaydi, chunki u har bir testda ishlaydi.

```java
public record Money(BigDecimal amount, Currency currency) {
    public Money {
        // mudofaa emas, invariant: pul manfiy bo'lmaydi
        if (amount.signum() < 0) {
            throw new IllegalArgumentException("manfiy summa");
        }
    }

    public Money withVat(BigDecimal rate) {
        return new Money(amount.multiply(BigDecimal.ONE.add(rate)), currency);
    }
}
```

Uchinchi yo'l: klassni `sonar.coverage.exclusions` ga qo'shish. Bu halol, agar klassda chindan mantiq bo'lmasa. Mantiq bo'lsa, exclusion yolg'on tinchlik beradi.

## 11.2 `equals`, `hashCode`, `toString`: qamrash yoki record ga o'tish

Qo'lda yozilgan `equals` ko'p tarmoqli metod: null tekshiruv, tip tekshiruv, har bir maydon solishtiruvi. JaCoCo branch coverage uni ayovsiz hisoblaydi va bitta entity o'nlab qamralmagan tarmoq beradi. Sonar `java:S1206` bilan `equals` va `hashCode` ni juft yozishni talab qiladi.

```java
// Qamrash qimmat: har bir maydon uchun ikki tarmoq
public class OrderLine {
    private String sku;
    private int qty;

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        OrderLine that = (OrderLine) o;
        return qty == that.qty && Objects.equals(sku, that.sku);
    }

    @Override
    public int hashCode() {
        return Objects.hash(sku, qty);
    }
}
```

Dizayn yechimi: o'zgarmas ma'lumot uchun `record`. Kompilyator `equals`, `hashCode`, `toString` ni yasaydi va JaCoCo bytecode da generatsiya qilingan deb belgilangan a'zolarni hisobga olmaydi.

```java
// Uchta metod ham bepul keladi, coverage da ko'rinmaydi
public record OrderLine(String sku, int qty) { }
```

Agar `record` ga o'tish imkoni yo'q bo'lsa, EqualsVerifier bir nechta instansiya yasab barcha tarmoqni bosib o'tadi.

```java
@Test
void equalsKontrakti() {
    // simmetriya, tranzitivlik, null va tip tarmoqlarini birdan bosadi
    EqualsVerifier.forClass(OrderLine.class)
        .suppress(Warning.NONFINAL_FIELDS)
        .verify();
}
```

`toString` uchun test yozish deyarli har doim behuda. Agar log formati shartnoma bo'lsa, u oddiy metod va unga test kerak. Aks holda uni Lombok yoki record ga topshiring.

## 11.3 Getter va setter: nega ular qamrovni suyultiradi

Getter bitta `return` qatoridan iborat: u qamralsa ham sifat haqida hech narsa aytmaydi. Lekin ular sonli jihatdan ko'p: 30 maydonli DTO 60 ta qamralmagan qator beradi va bu butun modul foizini pasaytiradi.

Muammo Sonar qoidasida emas, JaCoCo hisobotida paydo bo'ladi, keyin Sonar o'sha raqamni gate ga olib chiqadi. Shuning uchun yechim test yozishda emas, hisobot sozlashda.

```xml
<!-- JaCoCo oddiy aksessorlarni filtrlaydi, agar Lombok ishlatilsa -->
<plugin>
  <groupId>org.jacoco</groupId>
  <artifactId>jacoco-maven-plugin</artifactId>
  <version>0.8.12</version>
  <executions>
    <execution><goals><goal>prepare-agent</goal></goals></execution>
    <execution>
      <id>report</id>
      <phase>verify</phase>
      <goals><goal>report</goal></goals>
    </execution>
  </executions>
</plugin>
```

Lombok bilan yasalgan getter `@lombok.Generated` annotatsiyasini oladi. JaCoCo 0.8.x shu annotatsiyani ko'rib qatorni hisobdan chiqaradi, lekin buning uchun `lombok.config` da bitta satr kerak.

```properties
# lombok.config, loyiha ildizida
# generatsiya qilingan kodga @Generated qo'yiladi, JaCoCo uni o'tkazib yuboradi
lombok.addLombokGeneratedAnnotation = true
config.stopBubbling = true
```

Qo'lda yozilgan getter uchun bu ishlamaydi. Unda ikki yo'l bor: DTO ni `record` ga aylantirish, yoki DTO paketini coverage dan chiqarish.

```properties
# sonar-project.properties
# faqat ma'lumot tashuvchi paketlar, ularda shart va hisob yo'q
sonar.coverage.exclusions=**/dto/**,**/config/**,**/*Application.java
# bu qatorni har safar kod qo'shilganda qayta ko'rib chiqing
```

## 11.4 Istisno tarmoqlari: `catch` bloklarini qanday ishga tushirish

`catch` bloki test paytida ishga tushmasa, u qamralmagan qoladi. Ko'p jamoa shu yerda "istisnoni sinab bo'lmaydi" deydi. Aslida mock bilan istisnoni ataylab keltirish oddiy ish.

```java
@Service
public class PaymentService {
    private final PaymentGateway gateway;
    private final PaymentLogRepository logs;

    public PaymentResult charge(Order order) {
        try {
            return gateway.charge(order.total());
        } catch (GatewayTimeoutException e) {
            // bu tarmoq ham sinalishi kerak, u biznes qarori
            logs.saveFailure(order.id(), e.getMessage());
            return PaymentResult.retryLater(order.id());
        }
    }
}
```

Mock gateway ga istisno tashlashni buyuramiz. Eng muhimi: `catch` ichidagi yon ta'sirni ham tasdiqlaymiz, aks holda test faqat qatorni bo'yaydi.

```java
@Test
void timeoutBolsaKeyinUrinishQaytadi() {
    when(gateway.charge(any())).thenThrow(new GatewayTimeoutException("3s"));

    var result = service.charge(new Order("ORD-1", Money.of("120.00")));

    assertThat(result.status()).isEqualTo(RETRY_LATER);
    // yon ta'sir: nosozlik log ga yozilgan
    verify(logs).saveFailure(eq("ORD-1"), contains("3s"));
}
```

Agar `catch` bloki faqat `log.error` qilsa, Sonar istisno yutilgani haqida shikoyat qiladi. Bunday blokni sinash emas, olib tashlash kerak: istisnoni yuqoriga chiqaring yoki ma'noli qarorga aylantiring.

```java
// Yomon: istisno yutildi, test yozish ham ma'nosiz
catch (SQLException e) {
    log.error("xato", e);
}

// Yaxshi: kontekst qo'shib yuqoriga chiqariladi
catch (SQLException e) {
    throw new StockReadException("ombor qoldig'i o'qilmadi: " + sku, e);
}
```

## 11.5 Mudofaa tekshiruvlari (`if (x == null) throw`): ularni sinash yoki olib tashlash

Har bir public metod boshida null tekshiruv turgan kod ikki marta jarima oladi: JaCoCo har tekshiruvni ikki tarmoq deb sanaydi, Sonar esa metod murakkabligi oshganini aytadi. Savol bitta: bu tekshiruv kimdan himoya qiladi. Agar metod tashqi API chegarasida bo'lsa, tekshiruv ham, test ham kerak. Ichki servislar orasida esa chaqiruvchi sizning kodingiz, tekshiruv ortiqcha.

```java
// Chegara: controller, kelgan ma'lumot ishonchsiz
@PostMapping("/orders")
public ResponseEntity<OrderView> create(@Valid @RequestBody CreateOrderRequest req) {
    // qo'lda null tekshiruv yo'q, Bean Validation bajaradi
    return ResponseEntity.ok(orderService.create(req.toCommand()));
}

// Ichki servis: tekshiruv olib tashlandi, o'rniga invariant turda
public OrderView create(CreateOrderCommand cmd) {
    // cmd o'zi record, maydonlari konstruktorda tekshirilgan
    var order = Order.open(cmd.customerId(), cmd.lines());
    return OrderView.from(repository.save(order));
}
```

Validatsiyani turga ko'chirish eng kuchli usul: qiymat `record` konstruktorida bir marta tekshiriladi va bitta test butun oqimni qamraydi.

```java
@ParameterizedTest
@MethodSource("yaroqsizBuyruqlar")
void yaroqsizBuyruqRadEtiladi(CreateOrderCommand cmd, String xabar) {
    assertThatThrownBy(() -> orderService.create(cmd))
        .isInstanceOf(IllegalArgumentException.class)
        .hasMessageContaining(xabar);
}

static Stream<Arguments> yaroqsizBuyruqlar() {
    return Stream.of(
        arguments(cmdWithNoLines(), "kamida bitta qator"),
        arguments(cmdWithNegativeQty(), "miqdor musbat")
    );
}
```

## 11.6 Konfiguratsiya klasslari va `@Bean` metodlari

`@Configuration` klassidagi `@Bean` metodi odatda bitta `return new Something(...)` dan iborat. Unga unit test yozish bean ni qo'lda yasashdan boshqa narsa emas. Lekin Spring context ko'tariladigan test uni tabiiy ravishda qamraydi.

```java
@Configuration
public class StockClientConfig {

    @Bean
    RestClient stockRestClient(StockProperties props) {
        // mantiq bor: timeout va base URL shartnoma qismi
        return RestClient.builder()
            .baseUrl(props.baseUrl())
            .requestFactory(factory(props.timeout()))
            .build();
    }

    private ClientHttpRequestFactory factory(Duration timeout) {
        var f = new SimpleClientHttpRequestFactory();
        f.setConnectTimeout((int) timeout.toMillis());
        return f;
    }
}
```

Sinashning to'g'ri yo'li `ApplicationContextRunner`: u to'liq ilovani ko'tarmaydi, faqat kerakli konfiguratsiyani yuklaydi.

```java
@Test
void stockClientSozlanadi() {
    new ApplicationContextRunner()
        .withUserConfiguration(StockClientConfig.class)
        .withPropertyValues(
            "stock.base-url=http://stock:8080",
            "stock.timeout=2s")
        .run(ctx -> {
            // bean yaratilgani va xususiyat bog'langani tekshiriladi
            assertThat(ctx).hasSingleBean(RestClient.class);
            assertThat(ctx.getBean(StockProperties.class).timeout())
                .isEqualTo(Duration.ofSeconds(2));
        });
}
```

Agar `@Bean` metodida shart bo'lmasa, konfiguratsiya paketini coverage dan chiqarish halol. `@ConditionalOnProperty` paydo bo'lishi bilan uni qaytarib kiritish kerak, chunki o'sha shart xato qiladigan joy.

## 11.7 Mapper va konvertorlar: qo'lda yozilgani va generatsiya qilingani

Qo'lda yozilgan mapper uzun va bir xil. Sonar unda duplication ko'radi, JaCoCo esa har bir `set` chaqiruvini qator deb sanaydi. Eng ko'p uchraydigan bug: yangi maydon qo'shildi, mapper ga qo'shilmadi, test esa sezmadi.

```java
// Qo'lda: 20 qator, har biri alohida qamralishi kerak
public OrderView toView(Order o) {
    var v = new OrderView();
    v.setId(o.getId());
    v.setTotal(o.getTotal());
    v.setStatus(o.getStatus().name());
    // customerName qo'shilishi esdan chiqdi, test ham sezmaydi
    return v;
}
```

Yechim ikki qatlamli. Birinchi: MapStruct bilan generatsiya qilish, u `@Generated` qo'yadi va yo'qotilgan maydonni kompilyatsiya vaqtida ushlaydi.

```java
@Mapper(componentModel = "spring",
        unmappedTargetPolicy = ReportingPolicy.ERROR)
public interface OrderMapper {
    // yo'qotilgan maydon build ni buzadi, runtime da emas
    OrderView toView(Order order);
}
```

Ikkinchi: qo'lda qolgan mapper uchun "hamma maydon to'ldirilgan" degan bitta test. U butun metodni qamraydi va kelgusi maydonni ham ushlaydi.

```java
@Test
void barchaMaydonlarKochiriladi() {
    var order = TestData.fullOrder();   // barcha maydoni to'ldirilgan
    var view = mapper.toView(order);

    // hech bir maydon null qolmasligi kerak
    assertThat(view).hasNoNullFieldsOrProperties();
    assertThat(view.getTotal()).isEqualByComparingTo(order.getTotal());
}
```

## 11.8 `main` metodi va Spring Boot ishga tushirish klassi

`SpringApplication.run` chaqiruvi bitta qator, lekin u deyarli har bir loyihada qamralmagan qoladi. Ko'p jamoa `contextLoads` degan bo'sh test yozadi, u `main` ni emas, context ni qamraydi.

```java
@SpringBootApplication
public class WarehouseApplication {
    public static void main(String[] args) {
        SpringApplication.run(WarehouseApplication.class, args);
    }
}
```

Agar gate shu bitta qator uchun qizarsa, eng toza yechim uni exclusion ro'yxatiga qo'shish. `main` da mantiq bo'lmasligi kerak, shu holda uni sinashning qiymati nolga teng.

```properties
# sonar-project.properties
sonar.coverage.exclusions=**/*Application.java,**/config/**
# agar main ichida mantiq paydo bo'lsa, uni alohida klassga chiqaring
```

Agar `main` ichida argument tahlili yoki profil tanlash bo'lsa, mantiqni alohida klassga ko'chiring. Shunda `main` bitta qator bo'lib qoladi va mantiq to'liq qamraladi.

```java
@SpringBootApplication
public class WarehouseApplication {
    public static void main(String[] args) {
        // mantiq StartupArgs ichida, u alohida sinaladi
        new SpringApplicationBuilder(WarehouseApplication.class)
            .profiles(StartupArgs.profilesFrom(args))
            .run(args);
    }
}
```

## 11.9 Yetib bo'lmaydigan kod: uni test bilan emas, o'chirish bilan hal qilish

Yetib bo'lmaydigan kodga test yozish mumkin emas, chunki uni ishga tushiradigan yo'l yo'q. Sonar bunday holatni bir nechta qoida bilan belgilaydi: har doim `true` bo'ladigan shart, erishilmaydigan `default`, qaytganidan keyingi qator. Yechimi bitta: o'chirish.

```java
// Yomon: enum to'liq qoplangan, default hech qachon ishlamaydi
public BigDecimal discount(CustomerTier tier) {
    switch (tier) {
        case BRONZE: return new BigDecimal("0.00");
        case SILVER: return new BigDecimal("0.05");
        case GOLD:   return new BigDecimal("0.10");
        default:
            // bu qator qamralmaydi va qamralishi ham kerak emas
            throw new IllegalStateException("noma'lum daraja");
    }
}

// Yaxshi: switch expression, kompilyator to'liqligini tekshiradi
public BigDecimal discount(CustomerTier tier) {
    return switch (tier) {
        case BRONZE -> new BigDecimal("0.00");
        case SILVER -> new BigDecimal("0.05");
        case GOLD   -> new BigDecimal("0.10");
    };
}
```

Java 17 dan boshlab enum ustidagi `switch` expression da barcha variant qoplangan bo'lsa `default` kerak emas. Yangi enum qiymati qo'shilsa, build buziladi. Bu runtime istisnodan yaxshi, coverage ham toza bo'ladi.

## 11.10 Interfeys standart metodlari va abstrakt klasslar

`default` metod interfeysda tanaga ega, ya'ni JaCoCo uni qamralishi kerak deb sanaydi. Agar hech bir implementatsiya uni ishlatmasa, qator bekor turadi. Abstrakt klassdagi `protected` yordamchi metodlar bilan ham shunday.

```java
public interface StockPolicy {
    boolean allows(String sku, int qty);

    default boolean allowsAll(Map<String, Integer> lines) {
        // standart metod, uni ham sinash kerak
        return lines.entrySet().stream()
            .allMatch(e -> allows(e.getKey(), e.getValue()));
    }
}
```

Standart metodni sinashning eng arzon yo'li: test ichida lambda implementatsiya yasab, shu orqali chaqirish.

```java
@Test
void allowsAllBarchaQatorniTekshiradi() {
    // test uchun minimal implementatsiya: faqat qty <= 10 ruxsat
    StockPolicy policy = (sku, qty) -> qty <= 10;

    assertThat(policy.allowsAll(Map.of("A", 5, "B", 10))).isTrue();
    assertThat(policy.allowsAll(Map.of("A", 5, "B", 11))).isFalse();
}
```

Abstrakt klass uchun shartnoma testini vorislar orasida ulashing: abstrakt test klass yoziladi, har bir voris uni meros qilib oladi.

```java
abstract class StockPolicyContractTest {
    abstract StockPolicy policy();   // har bir voris o'zini beradi

    @Test
    void manfiyMiqdorHechQachonRuxsatEtilmaydi() {
        assertThat(policy().allows("A", -1)).isFalse();
    }
}

class StrictStockPolicyTest extends StockPolicyContractTest {
    StockPolicy policy() { return new StrictStockPolicy(); }
}
```

## 11.11 Qamrash qiyin kodni qayta loyihalash: dizayn signali sifatida qarash

Agar metodga test yozish uchun beshta mock, static mocking va `ReflectionTestUtils` kerak bo'lsa, muammo testda emas. Qamrash qiyinligi deyarli har doim bog'liqlik yoki javobgarlik muammosining o'lchovi.

```java
// Qamrash qiyin: static chaqiruv, vaqt, tasodif va I/O bir joyda
public Invoice issue(Order order) {
    var now = LocalDateTime.now();                 // vaqtni almashtirib bo'lmaydi
    var no = "INV-" + UUID.randomUUID();           // har safar boshqa natija
    var pdf = PdfRenderer.render(order);           // static, mock qilish og'ir
    Files.write(Path.of("/data", no + ".pdf"), pdf); // fayl tizimi
    return new Invoice(no, now, order.total());
}
```

`Clock`, nomer generatori va saqlovchi interfeys sifatida kiritiladi, shundan keyin test oddiy va deterministik bo'ladi.

```java
public Invoice issue(Order order) {
    // uchta bog'liqlik ham konstruktor orqali kiradi
    var no = numbers.next();
    var invoice = new Invoice(no, clock.instant(), order.total());
    storage.put(no, renderer.render(order));
    return invoice;
}

@Test
void hisobFakturaYaratiladi() {
    var fixed = Clock.fixed(Instant.parse("2025-03-01T10:00:00Z"), UTC);
    var service = new InvoiceService(fixed, () -> "INV-1", storage, renderer);

    var invoice = service.issue(TestData.order("150.00"));

    assertThat(invoice.number()).isEqualTo("INV-1");
    verify(storage).put(eq("INV-1"), any());
}
```

Qoida: test og'irlashgan joyda avval dizaynni so'roq qiling. Mock soni uchtadan oshsa, metod juda ko'p ish qilyapti.

## 11.12 Oddiy yondashuv va arxitektor yondashuvi

| Holat | Oddiy yondashuv | Arxitektor yondashuvi |
|---|---|---|
| Private konstruktor | Reflection bilan chaqirib coverage bo'yaladi | Utility klass value object ga aylantiriladi, konstruktor ishlaydigan kodga kiradi |
| `equals` va `hashCode` | Har maydon uchun qo'lda test yoziladi | `record` ishlatiladi yoki EqualsVerifier bilan kontrakt bir testda sinaladi |
| Getter va setter | Har biriga alohida test yoziladi | Lombok `@Generated` filtri yoki `record`, DTO paketi exclusion da |
| `catch` bloki | "Istisnoni sinab bo'lmaydi" deb qoldiriladi | Mock istisno tashlaydi, yon ta'sir ham `verify` bilan tasdiqlanadi |
| Null tekshiruv | Har metod boshida `if` va unga test | Validatsiya turga va chegaraga ko'chiriladi, ichkarida tekshiruv olib tashlanadi |
| `@Bean` metodi | `new` bilan qo'lda yasab test yoziladi | `ApplicationContextRunner` bilan sozlash va bog'lanish sinaladi |
| Mapper | Har maydon uchun assert yoziladi | MapStruct `ReportingPolicy.ERROR`, yo'qotilgan maydon build ni buzadi |
| `main` metodi | Bo'sh `contextLoads` testi qo'shiladi | `main` da mantiq qoldirilmaydi, klass exclusion ga kiradi |
| Yetib bo'lmaydigan `default` | Istisno tashlanadi va test yozilmaydi | `switch` expression, kompilyator to'liqligini kafolatlaydi |
| Qamrash qiyin metod | Static mocking va reflection bilan sindiriladi | Bog'liqlik inject qilinadi, metod sof funksiyaga yaqinlashtiriladi |

## 11.13 Tuzoq va yechim

| Tuzoq | Nima bo'ladi | Yechim |
|---|---|---|
| Keng exclusion patterni (`**/model/**`) | Mantiq bor klasslar ham hisobdan chiqadi, gate yolg'on yashil bo'ladi | Exclusion ni faqat mantiqsiz paketga qo'yish va har sprint qayta ko'rish |
| Reflection bilan private konstruktor testi | Coverage o'sadi, sifat o'smaydi, test hech nimani ushlamaydi | Dizaynni o'zgartirish yoki exclusion, lekin halol yozib qo'yish |
| Lombok bor, `lombok.config` yo'q | Getter lar `@Generated` olmaydi va qamralmagan qoladi | `lombok.addLombokGeneratedAnnotation = true` qo'shish |
| `catch` da faqat log | Sonar istisno yutilganini belgilaydi, test ma'nosiz bo'ladi | Istisnoni kontekst bilan yuqoriga chiqarish yoki qarorga aylantirish |
| `default` da `IllegalStateException` | Qamralmagan tarmoq doimiy qoladi | Enum ustida `switch` expression, `default` olib tashlanadi |
| Konfiguratsiya to'liq exclusion da | `@ConditionalOnProperty` xatosi hech qachon sezilmaydi | Shart bor konfiguratsiyani `ApplicationContextRunner` bilan sinash |
| `toString` ga assert yozish | Format o'zgarsa test buziladi, bug esa o'tib ketadi | Faqat log shartnoma bo'lsa sinash, aks holda generatsiyaga topshirish |
| Faqat umumiy coverage ga qarash | Yangi kodda nol qamrov bo'lsa ham umumiy raqam yashil turadi | Gate ni "new code" coverage va duplication shartlariga bog'lash |

## 11.14 Hisobotni tekshirish

Qaysi klass qancha zarar keltirayotganini bilish uchun JaCoCo hisobotini bevosita ko'rish foydali. Bu Sonar ga yuborishdan oldingi eng tez tekshiruv.

```bash
# hisobotni yasash va qamralmagan klasslarni ko'rish
mvn -q clean verify
# har bir klassning nomi va qamralmagan qator soni
xmllint --xpath "//class/@name" target/site/jacoco/jacoco.xml \
  | tr " " "\n" | sed -n "1,40p"
# batafsil tahlil uchun HTML hisobot
xdg-open target/site/jacoco/index.html
```

Ro'yxatning tepasida DTO, mapper va konfiguratsiya turgan bo'lsa, ishni exclusion va `record` bilan boshlang. Tepada servis va domen klasslari bo'lsa, exclusion emas, test yozish kerak. Gate shartlarini sozlash shu hujjatning quality gate mavzusida, test tuzilishi esa [testlash qo'llanmasidagi](../testing/README.md) unit test mavzusida.

## 11.15 Amalda qo'llash

- [ ] JaCoCo XML hisobotidan eng ko'p qamralmagan qator bergan 15 klassni chiqarib, ularni "mantiq bor" va "mantiq yo'q" ikki guruhga ajrating.
- [ ] `lombok.config` ga `lombok.addLombokGeneratedAnnotation = true` qo'shib, hisobotdagi getter va setter qatorlari yo'qolganini tasdiqlang.
- [ ] Mantiqsiz DTO larni `record` ga o'tkazing va `equals`, `hashCode`, `toString` ni qo'lda yozilgan joydan olib tashlang.
- [ ] `sonar.coverage.exclusions` ni qayta yozib, faqat `**/dto/**`, `**/config/**` va `**/*Application.java` kabi aniq mantiqsiz yo'llarni qoldiring.
- [ ] Har bir `catch` blokini ko'rib chiqing: faqat log qiladiganlarini istisno chiqarishga aylantiring, qaror qabul qiladiganlariga mock orqali test yozing.
- [ ] Enum ustidagi barcha `switch` ni expression shakliga o'tkazing va qamralmaydigan `default` tarmoqlarini o'chirib tashlang.
- [ ] Qo'lda yozilgan mapperlarni MapStruct ga `unmappedTargetPolicy = ReportingPolicy.ERROR` bilan ko'chiring yoki `hasNoNullFieldsOrProperties` testi qo'shing.
- [ ] Testida uchtadan ko'p mock talab qiladigan metodlarni ro'yxatga oling va ularni `Clock` hamda interfeys injection bilan qayta loyihalashni rejaga kiriting.

---

[&larr; 10. JaCoCo va SonarQube ulanishi: Maven va Gradle sozlash](10-jacoco-va-sonarqube-ulanishi-maven-va.md) · [Mundarija](README.md) · [12. Exclusion: nimani chiqarish halol, nimani chiqarish aldov &rarr;](12-exclusion-nimani-chiqarish-halol-nimani.md)
