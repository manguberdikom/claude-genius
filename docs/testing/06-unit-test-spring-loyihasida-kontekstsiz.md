<!-- doc: testing | chapter: 6 | part:  -->

[Barcha hujjatlar](../../README.md) / [Testlash qo'llanmasi](README.md)

> Holat: AI yozgan, inson tekshirmagan.

# 6. Unit test Spring loyihasida: kontekstsiz testlash (Unit Testing in a Spring Project)

<details>
<summary>Bu bobdagi 12 bo'lim</summary>

- [6.1 Nega @SpringBootTest unit test uchun noto'g'ri tanlov](#61-nega-springboottest-unit-test-uchun-notogri-tanlov)
- [6.2 Constructor injection - testlanadigan dizayn asosi](#62-constructor-injection---testlanadigan-dizayn-asosi)
- [6.3 Qaysi sinflar Spring kontekstisiz testlanadi](#63-qaysi-sinflar-spring-kontekstisiz-testlanadi)
- [6.4 Service qatlamini mock repository bilan testlash](#64-service-qatlamini-mock-repository-bilan-testlash)
- [6.5 Mapper va DTO konvertorlarni testlash](#65-mapper-va-dto-konvertorlarni-testlash)
- [6.6 Validatsiyani Spring kontekstisiz testlash](#66-validatsiyani-spring-kontekstisiz-testlash)
- [6.7 Domain event va aggregate'ni testlash](#67-domain-event-va-aggregateni-testlash)
- [6.8 Konfiguratsiya va @ConfigurationProperties: ApplicationContextRunner](#68-konfiguratsiya-va-configurationproperties-applicationcontextrunner)
- [6.9 AOP va proxy: unit testda ushlab bo'lmaydigan xatti-harakat](#69-aop-va-proxy-unit-testda-ushlab-bolmaydigan-xatti-harakat)
- [6.10 Spring'ga bog'liqlikni kamaytiruvchi arxitektura qarorlari](#610-springga-bogliqlikni-kamaytiruvchi-arxitektura-qarorlari)
- [6.11 Qachon kontekst haqiqatan kerak (chegara)](#611-qachon-kontekst-haqiqatan-kerak-chegara)
- [6.12 Arxitektor nazorat ro'yxati](#612-arxitektor-nazorat-royxati)

</details>



Spring loyihasida yozilgan kodning katta qismi - biznes qoidalari, kalkulyatorlar, validatorlar, mapper'lar va domain modeli - Spring'ga umuman bog'liq emas va ularni tekshirish uchun ApplicationContext ko'tarish shart emas. Shunga qaramay ko'p jamoalarda har bir test `@SpringBootTest` bilan boshlanadi: natijada sekin, mo'rt va xato manbasini yashiradigan test to'plami paydo bo'ladi. Bu bobda qaysi kodni "konteynerdan tashqarida" - oddiy Java obyekti sifatida - testlash kerakligini, buning uchun kodni qanday yozishni va Spring'ning eng yengil test vositasi bo'lgan `ApplicationContextRunner` qachon o'rinli bo'lishini ko'rib chiqamiz. Oxirida kontekst haqiqatan zarur bo'ladigan chegarani aniq belgilaymiz.

## 6.1 Nega @SpringBootTest unit test uchun noto'g'ri tanlov

Birinchi sabab - vaqt. Toza unit test JVM ichida obyekt yaratib, metod chaqirib, natijani tekshiradi: bu millisekundlar tartibidagi ish. `@SpringBootTest` esa butun komponent skanerlashni, auto-configuration zanjirini, DataSource va EntityManagerFactory yaratishni, ba'zan embedded serverni ishga tushirishni talab qiladi - bu sekundlar tartibidagi ish. Quyidagi raqamlar o'rta kattalikdagi Spring Boot 3.x/4.x loyihasi uchun odatiy tartibni ko'rsatadi (aniq qiymat mashina va bean sonidan bog'liq):

| Test uslubi | Kontekst ko'tarilishi | Bitta test metodi | Nimani kafolatlaydi |
|---|---|---|---|
| Toza JUnit 5 (`new`) | yo'q | ~0.1-2 ms | logika to'g'riligi |
| `@ExtendWith(MockitoExtension.class)` | yo'q | ~1-5 ms | o'zaro ta'sir (interaction) |
| `ApplicationContextRunner` (2-5 bean) | ~30-200 ms | ~30-200 ms | wiring, conditional, binding |
| `@WebMvcTest` / `@DataJpaTest` (slice) | ~1-3 s | ~10-50 ms (kesh bilan) | qatlam kontrakti |
| `@SpringBootTest` (to'liq) | ~3-15 s | ~20-100 ms (kesh bilan) | tizim yig'ilishi |

Spring TestContext Framework kontekstni keshlaydi (`spring.test.context.cache.maxSize`, standart qiymati 32), shuning uchun ikkinchi testdan keyin narx kamayadi. Lekin kesh kaliti konfiguratsiyaga bog'liq: har bir yangi `@TestPropertySource`, `@ActiveProfiles` yoki `@MockitoBean` kombinatsiyasi yangi kontekst yaratadi, `@DirtiesContext` esa keshni buzadi. 300 ta unit testni `@SpringBootTest` bilan yozgan loyihada CI'da 20 daqiqalik to'plamlar normal holga aylanadi.

Ikkinchi, muhimroq sabab - xato manbasining noaniqligi. To'liq kontekst ko'tarilganda `OrderServiceTest` qulashi mumkin, chunki boshqa jamoa `KafkaTemplate` bean'ini o'zgartirgan, Flyway migratsiyasi buzilgan yoki yangi `@Value` xossasi `application.yml`da yo'q. Test nomi "buyurtma chegirmasi" deydi, xato esa `BeanCreationException` bo'ladi. Unit test bitta sinfning bitta qoidasini tekshirsa, qulaganda sabab bir xil aniq bo'ladi.

Uchinchi sabab - feedback halqasi. TDD yoki refactoring jarayonida test 50 ms ichida javob bersa, developer kodni fikr tezligida o'zgartiradi; 15 sekund kutish kerak bo'lsa, testlar IDE'da emas, faqat CI'da ishlay boshlaydi.

## 6.2 Constructor injection - testlanadigan dizayn asosi

Unit test imkoniyati arxitektura qarori natijasidir. Constructor injection sinfni `new` bilan yaratishga ruxsat beradi: bu Spring'ning o'zi ham rasman tavsiya qiladigan uslub. Shuningdek vaqtni `Clock` sifatida kiritish testni determinatsiyalashtiradi.

```java
@Service
public class OrderService {

    private final OrderRepository orders;
    private final DiscountPolicy discountPolicy;
    private final Clock clock;

    public OrderService(OrderRepository orders,
                        DiscountPolicy discountPolicy,
                        Clock clock) {
        this.orders = orders;
        this.discountPolicy = discountPolicy;
        this.clock = clock;
    }

    public Order place(CustomerId customerId, List<OrderLine> lines) {
        Money total = lines.stream()
                .map(OrderLine::amount)
                .reduce(Money.ZERO, Money::plus);
        Money discount = discountPolicy.discountFor(customerId, total);
        Order order = Order.create(customerId, lines, discount, clock.instant());
        return orders.save(order);
    }
}
```

Field injection (`@Autowired private OrderRepository orders;`) bu imkoniyatni yo'q qiladi: maydonni `final` qilib bo'lmaydi, obyektni to'liq holatda `new` bilan yaratib bo'lmaydi, test esa `ReflectionTestUtils.setField(...)` yoki `@InjectMocks`ning reflection magiyasiga tayanadi. Bu ikki muammoni keltiradi: maydon nomini o'zgartirsangiz test kompilyatsiya xatosi bermaydi, shunchaki `null` bilan qulaydi; va konstruktor "bu sinfga 7 ta dependency kirgan" degan dizayn signalini yashiradi. Shu sababli `@InjectMocks`ni ham imkon qadar ishlatmaslik, `@Mock` bilan olingan obyektlarni konstruktorga qo'lda berish tavsiya etiladi - `new OrderServiceImpl(mockRepo, fixedClock)` shaklidagi chaqiruv kompilyator nazoratida bo'ladi.

## 6.3 Qaysi sinflar Spring kontekstisiz testlanadi

Quyidagi jadval amaliy qaror qabul qilish uchun qo'llanma bo'ladi.

| Kod turi | Test usuli | Spring kerakmi |
|---|---|---|
| Domain entity, value object (`Money`, `Iban`) | toza JUnit 5 + AssertJ | yo'q |
| Biznes qoidasi / invariant (`Order.confirm()`) | toza JUnit 5, `assertThatThrownBy` | yo'q |
| Bean Validation annotatsiyalari bo'lgan DTO | `Validation.buildDefaultValidatorFactory()` | yo'q |
| Custom `ConstraintValidator` (Spring bean'siz) | to'g'ridan-to'g'ri `isValid(...)` | yo'q |
| MapStruct mapper | `Mappers.getMapper(...)` | yo'q |
| Qo'lda yozilgan DTO konvertor | `usingRecursiveComparison()` | yo'q |
| Kalkulyator, narx/soliq hisoblagich | `@ParameterizedTest` | yo'q |
| Policy / Strategy implementatsiyasi | toza JUnit 5 | yo'q |
| Service qatlami (orkestratsiya) | Mockito 5.x + `MockitoExtension` | yo'q |
| `@ConfigurationProperties`, `@Conditional` | `ApplicationContextRunner` | minimal |
| `@Transactional`, `@Cacheable`, `@Async`, `@Retryable` | integratsion / slice test | ha |
| Controller mapping, JSON serialization, SQL | slice test ([7-bob](07-integratsion-test-spring-boot-slice-testlari.md)) | ha |

Masalan value object uchun test hech qanday infratuzilmani talab qilmaydi:

```java
class MoneyTest {

    @Test
    void qoshish_valyutani_saqlaydi() {
        Money a = Money.of("12.50", "UZS");
        Money b = Money.of("7.50", "UZS");

        assertThat(a.plus(b)).isEqualTo(Money.of("20.00", "UZS"));
    }

    @Test
    void turli_valyutalarni_qoshish_rad_etiladi() {
        Money uzs = Money.of("10.00", "UZS");
        Money usd = Money.of("10.00", "USD");

        assertThatThrownBy(() -> uzs.plus(usd))
                .isInstanceOf(CurrencyMismatchException.class)
                .hasMessageContaining("USD");
    }
}
```

SpEL ifodalari, `Environment`ga murojaat yoki `ApplicationEventPublisher` chaqiruvlari aralashgan sinflar bu ro'yxatdan chiqib ketadi - shuning uchun sof logikani alohida sinfga ajratish testlanuvchanlikni oshiradigan eng arzon refactoring.

## 6.4 Service qatlamini mock repository bilan testlash

Service qatlami odatda orkestratsiya qiladi: repository'dan ma'lumot oladi, policy'ni chaqiradi, natijani saqlaydi. Bularni Mockito 5.x bilan Spring'siz tekshirish mumkin. `MockitoExtension` standart holda `Strictness.STRICT_STUBS` rejimida ishlaydi - ishlatilmagan stub test qulashiga olib keladi, bu ortiqcha sozlamalarni erta ushlaydi.

```java
@ExtendWith(MockitoExtension.class)
class OrderServiceTest {

    @Mock OrderRepository orders;
    @Mock DiscountPolicy discountPolicy;

    private final Clock clock =
            Clock.fixed(Instant.parse("2026-03-01T10:00:00Z"), ZoneOffset.UTC);

    @Test
    void vip_mijozga_chegirma_qollanadi() {
        OrderService service = new OrderService(orders, discountPolicy, clock);
        CustomerId customer = new CustomerId("c-1");
        List<OrderLine> lines = List.of(line("SKU-1", 2, "100.00"));
        when(discountPolicy.discountFor(customer, Money.of("100.00", "UZS")))
                .thenReturn(Money.of("15.00", "UZS"));
        when(orders.save(any(Order.class))).thenAnswer(inv -> inv.getArgument(0));

        Order order = service.place(customer, lines);

        assertThat(order.total()).isEqualTo(Money.of("85.00", "UZS"));
        assertThat(order.createdAt()).isEqualTo(Instant.parse("2026-03-01T10:00:00Z"));
        verify(orders).save(argThat(o -> o.discount().equals(Money.of("15.00", "UZS"))));
    }
}
```

Diqqat qiling: `Clock.fixed(...)` tufayli `createdAt` aniq tekshiriladi - `LocalDateTime.now()`ni to'g'ridan-to'g'ri ishlatgan kodda bunday assert yozish mumkin emas. Agar repository interfeysi domain qatlamida (port sifatida) e'lon qilingan bo'lsa, mock'lash ham tabiiy ko'rinadi; Spring Data'ning `JpaRepository`sini to'g'ridan-to'g'ri mock'lash esa 20 dan ortiq metodli interfeysni soxtalashtirishga olib keladi.

## 6.5 Mapper va DTO konvertorlarni testlash

MapStruct mapper'i kompilyatsiya vaqtida oddiy Java sinfiga aylanadi, shuning uchun uni Spring'siz olish mumkin. `componentModel = "spring"` bo'lsa ham `Mappers.getMapper(...)` ishlaydi, agar mapper boshqa mapper'larni `uses` orqali olmasa; aks holda generatsiya qilingan `XxxMapperImpl`ni `new` bilan yaratib, bog'liq mapper'ni setter yoki konstruktor orqali bering.

```java
class CustomerMapperTest {

    private final CustomerMapper mapper = Mappers.getMapper(CustomerMapper.class);

    @Test
    void entity_dto_ga_toliq_kochadi() {
        CustomerEntity entity =
                new CustomerEntity(7L, "Olim", "Qoraev", "olim@example.uz", true);

        CustomerDto dto = mapper.toDto(entity);

        assertThat(dto)
                .usingRecursiveComparison()
                .isEqualTo(new CustomerDto(7L, "Olim Qoraev", "olim@example.uz", true));
    }

    @Test
    void nomavjud_maydonlar_null_qoladi() {
        CustomerEntity entity = new CustomerEntity(7L, "Olim", null, null, false);

        assertThat(mapper.toDto(entity).email()).isNull();
    }
}
```

Qo'lda yozilgan konvertorlar uchun AssertJ'ning `usingRecursiveComparison()` usuli eng foydali: yangi maydon qo'shilib, konvertorda unutilsa, test darhol qulaydi. Maydonlarni bitta-bitta tekshiradigan test esa bunday "unutilgan maydon" xatosini aniqlamaydi. Katta obyektlarda `ignoringFields("id", "audit.createdAt")` va `withEqualsForType(...)` bilan toleranslikni boshqarish mumkin.

## 6.6 Validatsiyani Spring kontekstisiz testlash

Jakarta Bean Validation 3.x implementatsiyasi (Hibernate Validator) Spring'dan mustaqil ishlaydi. `Validator`ni qo'lda yaratish kontekstdan taxminan 50-100 marta tezroq.

```java
class CreateOrderRequestValidationTest {

    private static final ValidatorFactory FACTORY =
            Validation.buildDefaultValidatorFactory();
    private static final Validator VALIDATOR = FACTORY.getValidator();

    @AfterAll
    static void close() {
        FACTORY.close();
    }

    @Test
    void bosh_mijoz_id_va_bosh_royxat_rad_etiladi() {
        CreateOrderRequest request = new CreateOrderRequest("  ", List.of());

        Set<ConstraintViolation<CreateOrderRequest>> violations =
                VALIDATOR.validate(request);

        assertThat(violations)
                .extracting(v -> v.getPropertyPath().toString())
                .containsExactlyInAnyOrder("customerId", "lines");
    }
}
```

Custom `ConstraintValidator`ni esa to'g'ridan-to'g'ri yaratib chaqirish mumkin, chunki `initialize(A)` interfeysda standart bo'sh implementatsiyaga ega. `ConstraintValidatorContext` kerak bo'lganda (masalan custom xabar shabloni qo'shilganda) uni deep stub bilan mock qilish yetarli.

```java
class InnValidatorTest {

    private final InnValidator validator = new InnValidator();
    private final ConstraintValidatorContext context =
            mock(ConstraintValidatorContext.class, RETURNS_DEEP_STUBS);

    @ParameterizedTest
    @ValueSource(strings = {"301234567", "612345678"})
    void togri_inn_otadi(String inn) {
        assertThat(validator.isValid(inn, context)).isTrue();
    }

    @Test
    void null_qiymat_valid_hisoblanadi() {
        assertThat(validator.isValid(null, context)).isTrue();
    }

    @Test
    void qisqa_inn_rad_etiladi() {
        assertThat(validator.isValid("123", context)).isFalse();
    }
}
```

Agar validator ichida repository yoki boshqa bean ishlatilsa (masalan noyoblikni DB'dan tekshirish), uni konstruktor orqali oling - shunda mock bilan Spring'siz testlash davom etadi. Faqat `@Valid` annotatsiyasi controller'da haqiqatan ishlab turganini tekshirish uchun slice test kerak bo'ladi ([7-bob](07-integratsion-test-spring-boot-slice-testlari.md)).

## 6.7 Domain event va aggregate'ni testlash

Aggregate holat o'zgarishi natijasida event chiqarishi kerak. Spring Data Commons'ning `AbstractAggregateRoot` sinfi buni `registerEvent(...)` orqali qiladi, `@DomainEvents` bilan belgilangan `domainEvents()` metodi esa `protected` - shuning uchun testni aggregate bilan bir xil paketda joylashtiring yoki o'z domain qatlamingizda ochiq `List<DomainEvent> pullEvents()` metodini e'lon qiling. Ikkinchi variant Spring'ga bog'liqlikni butunlay yo'qotadi.

```java
class OrderAggregateTest {

    @Test
    void tasdiqlanganda_event_royxatga_olinadi() {
        Order order = Order.create(new CustomerId("c-1"), List.of(line()),
                Money.ZERO, Instant.parse("2026-03-01T10:00:00Z"));

        order.confirm();

        assertThat(order.pullEvents())
                .singleElement()
                .isInstanceOf(OrderConfirmedEvent.class)
                .extracting("orderId")
                .isEqualTo(order.id());
    }

    @Test
    void ikki_marta_tasdiqlash_rad_etiladi_va_event_takrorlanmaydi() {
        Order order = confirmedOrder();

        assertThatThrownBy(order::confirm).isInstanceOf(IllegalStateException.class);
        assertThat(order.pullEvents()).hasSize(1);
    }
}
```

Muhim chegara: event'ning haqiqatan e'lon qilinishi (publish) aggregate Spring Data repository orqali saqlanganda `@AfterDomainEventPublication` mexanizmi bilan sodir bo'ladi. Ya'ni "event ro'yxatga olindi" - unit test mavzusi, "event listener chaqirildi" - integratsion test mavzusi.

## 6.8 Konfiguratsiya va @ConfigurationProperties: ApplicationContextRunner

Konfiguratsiya sinflari, `@Conditional` qoidalari va xossalar bind'lanishi Spring mexanizmlari bo'lgani uchun ularni kontekstsiz tekshirib bo'lmaydi. Lekin to'liq kontekst ham shart emas: `org.springframework.boot.test.context.runner.ApplicationContextRunner` faqat siz ko'rsatgan konfiguratsiyani ko'taradi va har bir `run(...)` chaqiruvidan keyin kontekstni yopadi. Veb uchun `WebApplicationContextRunner` va `ReactiveWebApplicationContextRunner` variantlari bor.

```java
class PaymentRetryConfigurationTest {

    private final ApplicationContextRunner runner = new ApplicationContextRunner()
            .withUserConfiguration(PaymentRetryConfiguration.class);

    @Test
    void xossalar_bind_boladi() {
        runner.withPropertyValues("payment.retry.max-attempts=5",
                        "payment.retry.backoff=PT2S")
                .run(ctx -> {
                    assertThat(ctx).hasSingleBean(PaymentRetryProperties.class);
                    PaymentRetryProperties p = ctx.getBean(PaymentRetryProperties.class);
                    assertThat(p.maxAttempts()).isEqualTo(5);
                    assertThat(p.backoff()).isEqualTo(Duration.ofSeconds(2));
                });
    }

    @Test
    void ochirilganda_bean_yaratilmaydi() {
        runner.withPropertyValues("payment.retry.enabled=false")
                .run(ctx -> assertThat(ctx).doesNotHaveBean(PaymentRetryTemplate.class));
    }
}
```

Bu runner yana: `withBean(...)` bilan soxta bean qo'shish, `withConfiguration(AutoConfigurations.of(...))` bilan auto-configuration zanjirini sinash, `assertThat(ctx).hasFailed()` va `getFailure().hasMessageContaining(...)` bilan noto'g'ri qiymatda kontekst qulashini tasdiqlash imkonini beradi. Bir test ~30-200 ms vaqt oladi - `@SpringBootTest`ga nisbatan o'nlab marta tez.

**`ApplicationContextRunner` `application.yml` ni o'qimaydi.** `@SpringBootTest` Spring Boot ning config data yuklovchisini ishga tushiradi, runner esa yo'q: `application.yml` dagi standart qiymatlar kontekstga tushmaydi va test "kalit yo'q" deb yiqiladi (yoki, undan yomoni, record ning kod ichidagi standarti bilan yashil bo'ladi va yml ni umuman tekshirmaydi). Yml ni haqiqatan o'qitish uchun `ConfigDataApplicationContextInitializer` beriladi.

```java
// YOMON: yml o'qilmaydi, test yml dagi standartni tekshirmayapti
runner.run(ctx -> assertThat(ctx.getBean(RetryProperties.class).maxAttempts()).isEqualTo(3));

// YAXSHI: application.yml yuklanadi
runner.withInitializer(new ConfigDataApplicationContextInitializer())
        .run(ctx -> assertThat(ctx.getBean(RetryProperties.class).maxAttempts()).isEqualTo(3));
```

Ikkinchi tuzoq: konfiguratsiya sinflarini skanerlab tekshiradigan "qo'riqchi" test (har `@ConfigurationProperties` yoki `@Configuration` ni topadi) ichki `@TestConfiguration` sinfini ham topadi va ularni production konfiguratsiyasi deb hisoblaydi. Skaner filtrida `@TestConfiguration` bilan belgilangan (va test paketidagi) sinflarni chiqarib tashlang, aks holda test sinfi qo'shilishi qo'riqchini yiqitadi.

## 6.9 AOP va proxy: unit testda ushlab bo'lmaydigan xatti-harakat

Spring'ning `@Transactional`, `@Cacheable`, `@Async`, `@Retryable`, `@PreAuthorize` kabi annotatsiyalari proxy (JDK dynamic proxy yoki CGLIB) orqali ishlaydi. Unit testda obyekt `new` bilan yaratilganda proxy yo'q - annotatsiyalar shunchaki e'tiborsiz qoladi. Natijada quyidagi xato unit testda hech qachon ko'rinmaydi:

```java
@Service
class ReportService {

    @Transactional
    public void importAll(List<Row> rows) {
        rows.forEach(this::importOne); // self-invocation: proxy chetlab o'tiladi
    }

    @Transactional(propagation = Propagation.REQUIRES_NEW)
    public void importOne(Row row) {
        // yangi tranzaksiya kutiladi, lekin hosil bo'lmaydi
    }
}
```

Shuningdek `private` yoki `final` metodga qo'yilgan `@Cacheable` ishlamaydi, `@Async` metodining `void` qaytaradigan versiyasida istisno yo'qoladi, `@Retryable` self-invocation'da urinishlarni takrorlamaydi. Bu xatolar faqat haqiqiy kontekst bilan - `@DataJpaTest`, `@SpringBootTest` yoki `ApplicationContextRunner` + `@EnableTransactionManagement` muhitida ushlanadi. Shu sababli: proxy semantikasi unit testning mas'uliyati emas, u [7-bobda](07-integratsion-test-spring-boot-slice-testlari.md) ko'riladigan slice va integratsion testlarga tegishli. Unit testda esa bu metodlarning ichki logikasini proxy'siz tekshiring.

## 6.10 Spring'ga bog'liqlikni kamaytiruvchi arxitektura qarorlari

Spring'siz testlash imkoniyati - paket tuzilishining natijasi. Hexagonal (ports and adapters) yondashuvida domain va application qatlamlari hech qanday Spring annotatsiyasini bilmaydi, infratuzilma esa adapterlarga chiqariladi:

```text
com.example.orders
├── domain               // Spring'siz: entity, value object, policy, event
│   ├── model/Order.java
│   ├── model/Money.java
│   └── port/OrderRepository.java        // interfeys (port)
├── application          // use case'lar; faqat konstruktor DI
│   └── PlaceOrderUseCase.java
└── infrastructure       // barcha Spring annotatsiyalari shu yerda
    ├── persistence/JpaOrderRepository.java   // @Repository, adapter
    ├── web/OrderController.java              // @RestController
    └── config/OrderBeanConfiguration.java    // @Configuration, @Bean
```

Amaliy qoidalar: domain qatlamida `org.springframework.*` import'i bo'lmasin (buni [14-bobdagi](14-arxitektura-testlari-va-kod-sifati.md) arxitektura testlari bilan majburlash mumkin); bean'larni `@Component` skanerlash orqali emas, `@Configuration` ichida aniq `@Bean` metodlari bilan e'lon qiling - shunda domain sinflari toza qoladi; `Clock`, `IdGenerator`, `EventPublisher` kabi infratuzilma ehtiyojlarini domain interfeyslari sifatida ifodalang; `@Value`ni service'larga sepish o'rniga `@ConfigurationProperties` record'ini yasab, uni konstruktorga uzatilgan oddiy qiymat obyekti sifatida bering.

## 6.11 Qachon kontekst haqiqatan kerak (chegara)

Kontekstdan voz kechish - maqsad emas, vosita. Quyidagi besh holatda kontekst majburiy, chunki tekshirilayotgan narsa Spring'ning o'zi: birinchidan, bean wiring - bean'lar haqiqatan yaratiladimi, dependency'lar to'g'ri bog'lanadimi, circular dependency yo'qmi; ikkinchidan, konfiguratsiya va profil - xossalar bind bo'ladimi, `@Conditional` to'g'ri hal qiladimi, validatsiya cheklovlari ishlaydimi; uchinchidan, proxy xatti-harakati - tranzaksiya chegaralari, kesh, retry, security; to'rtinchidan, serialization - JSON yozish/o'qish, `ObjectMapper` sozlamalari, HTTP status va header'lar; beshinchidan, SQL - JPA mapping, generatsiya qilingan so'rovlar, migratsiyalar.

Amaliy nisbat: test piramidasining pastki qatlamida (soni bo'yicha ~70-80%) Spring'siz unit testlar, o'rtada slice testlar, yuqorida kam sonli to'liq integratsion testlar bo'lishi kerak. Agar loyihada `@SpringBootTest` bilan yozilgan testlar soni unit testlardan ko'p bo'lsa, bu test strategiyasining emas, kod dizaynining muammosi - dependency'lar konstruktorga chiqarilmaganligi va biznes logikasi infratuzilmaga aralashib ketganligi belgisi.

## 6.12 Arxitektor nazorat ro'yxati

- [ ] Barcha bean'lar constructor injection ishlatadi; `@Autowired` maydonlari va setter injection kod bazasida yo'q (statik tahlil yoki arxitektura testi bilan majburlangan).
- [ ] Domain va application paketlarida `org.springframework.*` import'lari yo'q; biznes logikasi `new` bilan yaratilib testlanadi.
- [ ] `java.time.Clock`, ID generator va tasodifiylik manbalari dependency sifatida kiritilgan, `Instant.now()` biznes kodida to'g'ridan-to'g'ri chaqirilmaydi.
- [ ] Mapper, validator, kalkulyator, policy va value object testlari `@SpringBootTest`siz yozilgan va butun to'plam lokal mashinada 10 sekunddan kam ishlaydi.
- [ ] `@ConfigurationProperties` va `@Conditional` xatti-harakati `ApplicationContextRunner` bilan qoplangan, shu jumladan noto'g'ri qiymatda kontekst qulashi (`hasFailed()`).
- [ ] `@Transactional`, `@Cacheable`, `@Async`, `@Retryable` ishlatilgan har bir joy integratsion test bilan qoplangan; self-invocation holatlari ko'rib chiqilgan.
- [ ] Repository port'lari domain qatlamida e'lon qilingan, shuning uchun service testlari Spring Data interfeyslarini mock qilishga muhtoj emas.
- [ ] CI'da unit testlar alohida, tez bosqichda (kontekstsiz) ishga tushadi va integratsion testlardan oldin natija qaytaradi.

---

[&larr; 5. Unit test: asoslar, qoidalar va JUnit 5](05-unit-test-asoslar-qoidalar-va-junit-5.md) · [Mundarija](README.md) · [7. Integratsion test: Spring Boot slice testlari &rarr;](07-integratsion-test-spring-boot-slice-testlari.md)
