<!-- doc: testing | chapter: 7 | part:  -->

[Java Spring loyihasida testlash](../../README.md) / [Testlash qo'llanmasi](README.md)

# 7. Integratsion test: Spring Boot slice testlari (Integration Testing - Spring Boot Test Slices)

<details>
<summary>Bu bobdagi 13 bo'lim</summary>

- [7.1 Slice test g'oyasi: butun ilovani emas, bitta qatlamni ko'tarish](#71-slice-test-goyasi-butun-ilovani-emas-bitta-qatlamni-kotarish)
- [7.2 @WebMvcTest: web qatlamni izolyatsiyada testlash](#72-webmvctest-web-qatlamni-izolyatsiyada-testlash)
- [7.3 @WebFluxTest va WebTestClient bilan reactive controller](#73-webfluxtest-va-webtestclient-bilan-reactive-controller)
- [7.4 @DataJpaTest: persistence qatlami va TestEntityManager](#74-datajpatest-persistence-qatlami-va-testentitymanager)
- [7.5 N+1 va generatsiya qilingan SQL'ni testda ushlash](#75-n1-va-generatsiya-qilingan-sqlni-testda-ushlash)
- [7.6 @JdbcTest, @DataJdbcTest, @JsonTest, @RestClientTest](#76-jdbctest-datajdbctest-jsontest-restclienttest)
- [7.7 @SpringBootTest: qachon kerak va webEnvironment variantlari](#77-springboottest-qachon-kerak-va-webenvironment-variantlari)
- [7.8 Kontekst keshi: eng katta tezlik omili](#78-kontekst-keshi-eng-katta-tezlik-omili)
- [7.9 @TestConfiguration, bean override va property manbalari](#79-testconfiguration-bean-override-va-property-manbalari)
- [7.10 @ActiveProfiles bilan test konfiguratsiyasini ajratish](#710-activeprofiles-bilan-test-konfiguratsiyasini-ajratish)
- [7.11 @Sql, @SqlMergeMode va tranzaksion testning tuzoqlari](#711-sql-sqlmergemode-va-tranzaksion-testning-tuzoqlari)
- [7.12 Slice test anti-patternlari](#712-slice-test-anti-patternlari)
- [7.13 Arxitektor nazorat ro'yxati](#713-arxitektor-nazorat-royxati)

</details>



Unit testlar biznes qoidalarini tasdiqlaydi, ammo Spring ilovasining katta qismi - HTTP mapping, JSON serialization, validatsiya, JPA mapping va generatsiya qilingan SQL - framework bilan integratsiyada yashaydi va unit testda umuman tekshirilmaydi. Spring Boot bu bo'shliqni slice testlar bilan to'ldiradi: butun ilovani ko'tarmasdan, faqat bitta qatlamning auto-configuration'ini yoqadi. Bu bobda har bir slice annotatsiyasi nimani ko'taradi, nimani ko'tarmaydi, qanday yozilishi va qanday tuzoqlari borligini ko'rib chiqamiz. Barcha misollar Spring Boot 3.4+/4.x, Spring Framework 6.2+/7.x va JUnit 5 uchun.

## 7.1 Slice test g'oyasi: butun ilovani emas, bitta qatlamni ko'tarish

Oddiy `@SpringBootTest` `@SpringBootApplication`'ni topadi va uning barcha auto-configuration'larini qo'llaydi: DataSource, JPA, Flyway, Security, Kafka, cache, scheduler. Bu 5-15 sekundlik startup va yuzlab bean degani. Slice annotatsiyalari esa boshqa yo'ldan boradi - ular `@BootstrapWith` + `TypeExcludeFilter` + aniq auto-configuration ro'yxati ustiga qurilgan. Masalan `@WebMvcTest` `spring-boot-test-autoconfigure` ichidagi `spring.factories`/`AutoConfiguration.imports` metadatasidan faqat web qatlamiga tegishli auto-configuration'larni tanlaydi, qolganini o'chiradi. Shu bilan birga component scanning ham cheklanadi: slice o'z filtri ruxsat bergan stereotype'lardan boshqasini kontekstga kiritmaydi.

Arxitektor uchun muhim xulosa: slice test tezlik uchun emas, **cheklangan mas'uliyat** uchun kerak. `@WebMvcTest`'da repository mavjud emas, demak unda service logikasini test qilishning imkoni ham, ma'nosi ham yo'q. Har bir slice bitta kontraktni tekshiradi.

| Annotatsiya | Nima ko'tariladi | Qachon ishlatiladi |
| --- | --- | --- |
| `@WebMvcTest` | DispatcherServlet, `@Controller`, `@ControllerAdvice`, `Converter`/`GenericConverter`, `Filter`, `HandlerInterceptor`, `WebMvcConfigurer`, Jackson, MockMvc, Spring Security config | HTTP kontrakti: status, JSON shakli, header, validatsiya, xato mapping |
| `@WebFluxTest` | WebFlux infra, `@Controller`, `@ControllerAdvice`, `WebFilter`, codec'lar, `WebTestClient` | Reactive controller va stream kontrakti |
| `@DataJpaTest` | `@Entity`, Spring Data JPA repository, `EntityManager`, `TestEntityManager`, embedded DB, tranzaksiya + rollback | Query, mapping, fetch strategiya, projection |
| `@JdbcTest` | `JdbcTemplate`, `DataSource`, tranzaksiya | Qo'lda yozilgan SQL, DAO |
| `@DataJdbcTest` | Spring Data JDBC repository + aggregate mapping | Spring Data JDBC loyihalari |
| `@JsonTest` | `ObjectMapper`, `@JsonComponent`, `Module`, `JacksonTester` | Serialization/deserialization kontrakti |
| `@RestClientTest` | `RestClient.Builder`/`RestTemplateBuilder`, `MockRestServiceServer` | Chiquvchi HTTP client logikasi |
| `@SpringBootTest` | Butun kontekst (+ ixtiyoriy real server) | Qatlamlar kesishgan oqim, real HTTP, konfiguratsiya tekshiruvi |

## 7.2 @WebMvcTest: web qatlamni izolyatsiyada testlash

`@WebMvcTest(OrderController.class)` argumenti berilsa faqat shu controller ro'yxatga olinadi; argumentsiz chaqirilsa barcha controller'lar ko'tariladi (sekinroq va ko'proq mock talab qiladi). `@Service`, `@Repository`, `@Component` bean'lari **ko'tarilmaydi** - controller bog'liqliklari `@MockitoBean` orqali almashtiriladi. Spring Boot 3.4'dan `@MockBean` va `@SpyBean` deprecated, Spring Boot 4'da olib tashlangan; o'rniga Spring Framework 6.2'ning `org.springframework.test.context.bean.override.mockito.MockitoBean` va `MockitoSpyBean` ishlatiladi.

```java
@WebMvcTest(OrderController.class)
class OrderControllerWebMvcTest {

    @Autowired MockMvc mockMvc;

    @MockitoBean OrderService orderService;

    @Test
    void returnsOrderAsJson() throws Exception {
        given(orderService.findById(42L))
                .willReturn(new OrderView(42L, "NEW", new BigDecimal("199.90")));

        mockMvc.perform(get("/api/orders/42").accept(APPLICATION_JSON))
                .andExpect(status().isOk())
                .andExpect(header().string("Cache-Control", "no-store"))
                .andExpect(content().contentTypeCompatibleWith(APPLICATION_JSON))
                .andExpect(jsonPath("$.id").value(42))
                .andExpect(jsonPath("$.status").value("NEW"))
                .andExpect(jsonPath("$.total").value(199.90))
                .andExpect(jsonPath("$.internalCost").doesNotExist());

        then(orderService).should().findById(42L);
    }
}
```

Oxirgi `doesNotExist()` tekshiruvi - bu web qatlam testining eng qimmatli turi: API tashqariga chiqmasligi kerak bo'lgan maydonni ushlaydi. Xato yo'llari ham shu yerda tekshiriladi. Spring Framework 6'dan boshlab standart xato formati RFC 9457 `ProblemDetail`; `spring.mvc.problemdetails.enabled=true` bo'lsa framework xatolari `application/problem+json` sifatida qaytadi, maydon xatolari ro'yxati esa odatda `ResponseEntityExceptionHandler`'dan meros olgan `@ControllerAdvice`'da `properties`'ga qo'shiladi.

```java
@Test
void rejectsInvalidPayloadWithProblemDetail() throws Exception {
    mockMvc.perform(post("/api/orders")
                    .contentType(APPLICATION_JSON)
                    .content("""
                            {"customerId": null, "quantity": 0}
                            """))
            .andExpect(status().isBadRequest())
            .andExpect(content().contentTypeCompatibleWith("application/problem+json"))
            .andExpect(jsonPath("$.status").value(400))
            .andExpect(jsonPath("$.errors[*].field",
                    containsInAnyOrder("customerId", "quantity")));
}

@Test
void returns404WhenOrderMissing() throws Exception {
    given(orderService.findById(7L)).willThrow(new OrderNotFoundException(7L));

    mockMvc.perform(get("/api/orders/7"))
            .andExpect(status().isNotFound())
            .andExpect(jsonPath("$.type").value("urn:problem-type:order-not-found"))
            .andExpect(jsonPath("$.detail").value("Order 7 not found"));
}
```

Spring Framework 6.2'dan `MockMvcTester` ham mavjud - AssertJ uslubida: `assertThat(mvc.get().uri("/api/orders/42")).hasStatusOk().bodyJson().extractingPath("$.status").isEqualTo("NEW")`. Yangi loyihalarda u o'qilishi osonroq, eski `MockMvc` esa to'liq qo'llab-quvvatlanadi.

## 7.3 @WebFluxTest va WebTestClient bilan reactive controller

`@WebFluxTest` WebFlux infrastrukturasini va `WebTestClient`'ni ko'taradi, `@Controller`/`@ControllerAdvice`/`WebFilter`/codec'larni skanerlaydi, service va repository'ni esa yo'q. Muhim nuans: `RouterFunction` bean'lari orqali e'lon qilingan functional endpoint'lar skanerlanmaydi - ularni `@Import(OrderRoutes.class)` bilan aniq keltirish kerak.

```java
@WebFluxTest(controllers = ReactiveOrderController.class)
class ReactiveOrderControllerTest {

    @Autowired WebTestClient webTestClient;

    @MockitoBean ReactiveOrderService service;

    @Test
    void streamsOrders() {
        given(service.findAll()).willReturn(Flux.just(
                new OrderView(1L, "NEW", BigDecimal.ONE),
                new OrderView(2L, "PAID", BigDecimal.TEN)));

        webTestClient.get().uri("/api/orders")
                .accept(MediaType.APPLICATION_JSON)
                .exchange()
                .expectStatus().isOk()
                .expectHeader().contentTypeCompatibleWith(MediaType.APPLICATION_JSON)
                .expectBodyList(OrderView.class)
                .hasSize(2)
                .value(list -> assertThat(list).extracting(OrderView::status)
                        .containsExactly("NEW", "PAID"));
    }
}
```

`WebTestClient` faqat reactive uchun emas: `@SpringBootTest(webEnvironment = RANDOM_PORT)` bilan birga real HTTP ustida ham, `@AutoConfigureWebTestClient` bilan MVC ilovasida mock server ustida ham ishlaydi.

## 7.4 @DataJpaTest: persistence qatlami va TestEntityManager

`@DataJpaTest` `@Entity` sinflarini, Spring Data JPA repository'larini, `EntityManager` va `TestEntityManager`'ni ko'taradi; service qatlamini ko'tarmaydi. Har bir test metodi default'da tranzaksiya ichida ishlaydi va oxirida **rollback** qilinadi, shuning uchun testlar bir-biriga ta'sir qilmaydi.

Asosiy xavf - `@AutoConfigureTestDatabase`. `@DataJpaTest` uni `replace = Replace.ANY` bilan qo'llaydi, ya'ni sizning haqiqiy DataSource'ingizni classpath'dagi embedded bazaga (odatda H2) **jimgina** almashtiradi. Natijada siz PostgreSQL uchun yozilgan native query, `jsonb`, `ON CONFLICT` yoki partial index'ni H2'da test qilgan bo'lib qolasiz. Real bazada ishlash uchun `@AutoConfigureTestDatabase(replace = Replace.NONE)` yoki Spring Boot 3.4+'dagi `Replace.NON_TEST` (test o'zi e'lon qilgan DataSource'ni saqlaydi) ishlatiladi; real baza bilan ishlash [8-bobning](08-testcontainers-bilan-real-infratuzilmada.md) mavzusi.

```java
public interface OrderRepository extends JpaRepository<Order, Long>,
        JpaSpecificationExecutor<Order> {

    @Query("""
           select o.id as id, c.name as customerName, o.total as total
           from Order o join o.customer c
           where o.status = :status and o.createdAt < :before
           """)
    List<OrderSummary> findOverdue(Status status, LocalDate before);

    @Query("select o from Order o join fetch o.items")
    List<Order> findAllWithItems();

    interface OrderSummary {
        Long getId();
        String getCustomerName();
        BigDecimal getTotal();
    }
}
```

```java
@DataJpaTest
class OrderRepositoryTest {

    @Autowired TestEntityManager em;
    @Autowired OrderRepository repository;

    @Test
    void findsOverdueOrdersWithProjection() {
        Customer customer = em.persistFlushFind(new Customer("ACME"));
        em.persist(new Order(customer, Status.NEW, LocalDate.of(2026, 1, 1)));
        em.persist(new Order(customer, Status.PAID, LocalDate.of(2026, 1, 1)));
        em.flush();
        em.clear();

        var result = repository.findOverdue(Status.NEW, LocalDate.of(2026, 2, 1));

        assertThat(result).hasSize(1).first().satisfies(s -> {
            assertThat(s.getCustomerName()).isEqualTo("ACME");
            assertThat(s.getId()).isNotNull();
        });
    }

    @Test
    void specificationFiltersByStatusIn() {
        assertThat(repository.findAll(OrderSpecs.statusIn(Status.NEW))).isEmpty();
    }
}
```

`em.flush()` va `em.clear()` juftligi majburiy odat bo'lishi kerak: ularsiz query first-level cache'dan javob olishi mumkin va siz SQL'ni emas, Hibernate keshini test qilasiz.

## 7.5 N+1 va generatsiya qilingan SQL'ni testda ushlash

Fetch strategiyasi - bu kod review'da emas, testda ushlanadigan narsa. Eng arzon usul: Hibernate `Statistics`'ni yoqib, query sonini tasdiqlash. Shunda `join fetch` yoki `@EntityGraph` olib tashlansa test qizil bo'ladi.

```java
@DataJpaTest(properties = "spring.jpa.properties.hibernate.generate_statistics=true")
class OrderFetchPlanTest {

    @Autowired OrderRepository repository;
    @Autowired EntityManagerFactory emf;

    private Statistics stats() {
        return emf.unwrap(SessionFactory.class).getStatistics();
    }

    @Test
    void fetchJoinAvoidsNPlusOneOnItems() {
        // ... 3 order, har birida 2 item saqlangan, keyin em.clear()
        stats().clear();

        List<Order> orders = repository.findAllWithItems();
        orders.forEach(order -> order.getItems().size());

        assertThat(stats().getPrepareStatementCount())
                .as("items uchun qo'shimcha select bo'lmasligi kerak")
                .isEqualTo(1);
        assertThat(stats().getCollectionFetchCount()).isZero();
    }
}
```

Ikkinchi variant - `net.ttddyy:datasource-proxy` bilan DataSource'ni o'rab, `QueryCountHolder` orqali SELECT/INSERT/UPDATE sonini alohida tekshirish; u JPA'siz (`@JdbcTest`, `@DataJdbcTest`) ham ishlaydi va SQL matnini ham ko'rsatadi. Qaysi vositani tanlasangiz ham, qoida bitta: query sonini **aniq raqam** bilan tasdiqlang, "ko'p emas" deb emas.

## 7.6 @JdbcTest, @DataJdbcTest, @JsonTest, @RestClientTest

`@JdbcTest` faqat `DataSource` + `JdbcTemplate` + tranzaksiya beradi, bean skanerlash yo'q - qo'lda yozilgan SQL va DAO uchun ideal. `@DataJdbcTest` bunga Spring Data JDBC repository va aggregate mapping'ni qo'shadi. Ikkisi ham `@AutoConfigureTestDatabase`'ni `@DataJpaTest` kabi qo'llaydi, demak H2 xavfi aynan shu yerda ham bor.

`@JsonTest` serialization kontraktini arzon tekshiradi: `ObjectMapper`, `@JsonComponent`, custom `Module` va `JacksonTester` ko'tariladi. Bu API versiyalanishi uchun juda muhim - `isEqualToJson` referens fayl bilan solishtiradi va maydon nomi tasodifan o'zgarsa darhol sinadi.

```java
@JsonTest
class OrderViewJsonTest {

    @Autowired JacksonTester<OrderView> json;

    @Test
    void serializesContract() throws Exception {
        OrderView view = new OrderView(42L, "NEW", new BigDecimal("199.90"));

        assertThat(json.write(view)).isEqualToJson("/contract/order-view.json");
        assertThat(json.write(view)).hasJsonPathStringValue("@.status");
    }

    @Test
    void toleratesUnknownFieldsFromProducer() throws Exception {
        String payload = """
                {"id": 42, "status": "NEW", "total": 199.90, "addedInV2": true}
                """;

        assertThat(json.parseObject(payload).id()).isEqualTo(42L);
    }
}
```

`@RestClientTest` chiquvchi client'ni test qiladi: `RestClient.Builder`/`RestTemplateBuilder` va `MockRestServiceServer` auto-configure qilinadi. Shart: client o'z `RestClient`'ini **inject qilingan builder**'dan qurishi kerak, aks holda mock server hech narsani ushlamaydi.

```java
@RestClientTest(PricingClient.class)
class PricingClientTest {

    @Autowired PricingClient client;
    @Autowired MockRestServiceServer server;

    @Test
    void sendsApiKeyAndParsesResponse() {
        server.expect(requestTo("https://pricing.internal/v1/quote?sku=A-1"))
                .andExpect(method(HttpMethod.GET))
                .andExpect(header("X-Api-Key", "test-key"))
                .andRespond(withSuccess("""
                        {"sku":"A-1","price":12.50}
                        """, MediaType.APPLICATION_JSON));

        Quote quote = client.quote("A-1");

        assertThat(quote.price()).isEqualByComparingTo("12.50");
        server.verify();
    }
}
```

`MockRestServiceServer` bitta client sinfining kontraktini tekshirish uchun yetarli; retry, timeout va butun protokol xatti-harakatini real HTTP ustida tekshirish [9-bobdagi](09-tashqi-servislarni-taqlid-qilish-va.md) WireMock vazifasi.

## 7.7 @SpringBootTest: qachon kerak va webEnvironment variantlari

`@SpringBootTest` faqat qatlamlar kesishgan joyda kerak: tranzaksiya chegaralari, event'lar, security filter chain, konfiguratsiya binding, Flyway migratsiyasi bilan mapping muvofiqligi. `webEnvironment` to'rtta qiymatga ega: `MOCK` (default - mock servlet muhiti, real port yo'q, `@AutoConfigureMockMvc` bilan MockMvc), `RANDOM_PORT` (real server, bo'sh port, `@LocalServerPort`), `DEFINED_PORT` (`server.port` - CI'da port to'qnashuvi sababli tavsiya etilmaydi), `NONE` (web muhiti umuman yo'q - batch, scheduler, messaging uchun).

```java
@SpringBootTest(webEnvironment = WebEnvironment.RANDOM_PORT)
@ActiveProfiles("test")
class OrderCheckoutHttpTest {

    @Autowired TestRestTemplate restTemplate;
    @LocalServerPort int port;

    @Test
    void createsOrderAndReturnsLocationHeader() {
        var response = restTemplate.postForEntity(
                "/api/orders", new CreateOrderRequest(1L, 2), Void.class);

        assertThat(response.getStatusCode()).isEqualTo(HttpStatus.CREATED);
        URI location = response.getHeaders().getLocation();
        assertThat(location).asString()
                .startsWith("http://localhost:" + port + "/api/orders/");

        var created = restTemplate.getForEntity(location, OrderView.class);
        assertThat(created.getBody().status()).isEqualTo("NEW");
    }
}
```

`TestRestTemplate` 4xx/5xx'da exception tashlamaydi - bu xato javoblarini tekshirishni osonlashtiradi. Muqobil variant `WebTestClient` (`@AutoConfigureWebTestClient` yoki `RANDOM_PORT` bilan): fluent assertion va JSON ustida ishlash qulayroq.

## 7.8 Kontekst keshi: eng katta tezlik omili

Spring TestContext Framework kontekstlarni keshlaydi, kalit esa `MergedContextConfiguration`'dan hosil bo'ladi: konfiguratsiya sinflari/locations, active profile'lar, `@TestPropertySource` locations va inlined properties, `ApplicationContextInitializer`'lar, `ContextCustomizer`'lar (shu jumladan har bir `@MockitoBean`/`@MockitoSpyBean`/`@TestBean` e'loni va `@DynamicPropertySource`), parent kontekst va web resource base path. Ya'ni bitta qo'shimcha `@TestPropertySource(properties = "feature.x=true")` ham **butunlay yangi kontekst** yaratadi.

Raqamli ta'sir: tasavvur qiling, 40 ta integratsion test sinfi bor va har biri bir oz boshqacha konfiguratsiyaga ega. Startup 5 sekund bo'lsa - 40 x 5 = 200 sekund faqat kontekst ko'tarishga ketadi. Shu 40 sinf 3 ta umumiy konfiguratsiyaga keltirilsa, xarajat 15 sekundga tushadi, ya'ni suite'ning sof foydasiz vaqti ~13 barobar qisqaradi. Bundan tashqari kesh hajmi default'da 32 (`spring.test.context.cache.maxSize`); undan oshsa LRU evicting boshlanadi va chiqarib yuborilgan kontekst keyinroq **qaytadan** quriladi. `org.springframework.test.context.cache` logger'ini DEBUG'ga qo'yib kesh statistikasini (hit/miss/size) ko'rish mumkin.

`@DirtiesContext` eng qimmat annotatsiya: u kontekstni keshdan o'chiradi, demak keyingi test uni noldan ko'taradi. Uni "ehtiyot uchun" qo'yish suite'ni sekinlashtirishning eng tez usuli; holatni testning o'zida tozalash deyarli har doim arzonroq. Strategiya oddiy: bitta umumiy abstract bazaviy sinf, bitta profil, mock'lar faqat shu bazaviy sinfda yoki umuman yo'q.

```java
@SpringBootTest
@AutoConfigureMockMvc
@ActiveProfiles("test")
public abstract class AbstractIntegrationTest {
    // Bu yerda @TestPropertySource, @MockitoBean yoki @DirtiesContext YO'Q:
    // ularning har bir kombinatsiyasi yangi kontekst kaliti demakdir.
    @Autowired protected MockMvc mockMvc;
}

class OrderApiTest extends AbstractIntegrationTest { /* ... */ }

class PaymentApiTest extends AbstractIntegrationTest { /* ... */ }
```

## 7.9 @TestConfiguration, bean override va property manbalari

`@TestConfiguration` - `@Configuration`'ning test variantidir: test sinfi ichidagi static nested klass avtomatik qo'llanadi, top-level sinf esa `@Import` bilan keltiriladi va component scan tomonidan olinmaydi. U yangi bean qo'shish uchun ideal (masalan fixed `Clock`). Mavjud bean'ni **almashtirish** uchun esa ehtiyot bo'lish kerak: Spring Boot'da bean definition overriding default'da o'chirilgan, shuning uchun bir xil nomdagi `@Bean` xatoga olib keladi. To'g'ri yechim - `@TestBean` (static factory metod bilan almashtirish), `@MockitoBean` (mock bilan), yoki `@MockitoSpyBean` (real bean, lekin chaqiruvlarni tasdiqlash imkoni bilan).

```java
@SpringBootTest
@ActiveProfiles("test")
class PaymentFlowTest {

    @TestConfiguration
    static class FixedClockConfig {
        @Bean Clock testClock() {
            return Clock.fixed(Instant.parse("2026-01-15T10:00:00Z"), ZoneOffset.UTC);
        }
    }

    @DynamicPropertySource
    static void props(DynamicPropertyRegistry registry) {
        registry.add("payment.timeout", () -> "250ms");
    }

    @MockitoBean PaymentGateway gateway;        // tashqi tizim: mock
    @MockitoSpyBean OrderNotifier notifier;     // real bean + verify

    @Test
    void notifiesCustomerOnce() {
        given(gateway.charge(any())).willReturn(PaymentResult.approved("tx-1"));
        // ... oqim ishga tushiriladi
        then(notifier).should().notifyPaid(anyLong());
    }
}
```

Property'lar uchun uch qatlam bor: `@TestPropertySource(properties = ...)` - bir nechta test uchun statik qiymatlar; `@DynamicPropertySource` - runtime'da hisoblangan qiymatlar (port, URL); `src/test/resources/application-test.yml` - profil bilan faollashadigan umumiy test konfiguratsiyasi. Muhim tuzoq: `src/test/resources/application.yml` test classpath'da birinchi bo'lgani uchun asosiy `application.yml`'ni **to'liq soya qiladi**, qo'shilmaydi. Shu sababli test sozlamalarini profilga bog'langan alohida faylda saqlash xavfsizroq.

## 7.10 @ActiveProfiles bilan test konfiguratsiyasini ajratish

`@ActiveProfiles("test")` nafaqat `application-test.yml`'ni yoqadi, balki `@Profile` bilan belgilangan bean'larni almashtirish imkonini beradi: `@Profile("!test")` bilan real email sender, `@Profile("test")` bilan no-op sender. Bu kontekst kalitining qismi, shuning uchun profil nomlari sonini minimumda tutish kerak - har bir yangi profil kombinatsiyasi yangi kontekst. Ikkinchi qoida: production konfiguratsiyasida test uchun maxsus shart bo'lmasin. `@Profile("test")` tekshiruvi production sinfida paydo bo'lishi - arxitekturaviy nuqson, buni test-only konfiguratsiya sinfiga ko'chirish kerak.

## 7.11 @Sql, @SqlMergeMode va tranzaksion testning tuzoqlari

`@Sql` deklarativ ravishda script ishga tushiradi: sinf va metod darajasida, `executionPhase` bilan test oldidan yoki keyin. Default'da metod darajasidagi `@Sql` sinf darajasini **almashtiradi**; `@SqlMergeMode(MergeMode.MERGE)` ikkisini birlashtiradi (avval sinf, keyin metod).

```java
@SpringBootTest
@ActiveProfiles("test")
@Sql("/sql/reference-data.sql")
@SqlMergeMode(SqlMergeMode.MergeMode.MERGE)
class OrderArchiveJobTest {

    @Autowired OrderArchiveJob job;
    @Autowired JdbcTemplate jdbc;

    @Test
    @Sql("/sql/orders-2025.sql")
    @Sql(scripts = "/sql/cleanup-orders.sql",
         executionPhase = Sql.ExecutionPhase.AFTER_TEST_METHOD)
    void archivesOnlyClosedOrdersAndPublishesEventAfterCommit() {
        job.run();   // ichida @Transactional va AFTER_COMMIT listener bor

        Integer archived = jdbc.queryForObject(
                "select count(*) from order_archive", Integer.class);
        assertThat(archived).isEqualTo(2);
    }
}
```

E'tibor bering: bu sinfda `@Transactional` **yo'q**, tozalash esa `@Sql`'ning AFTER fazasi bilan bajariladi. Buning sababi tranzaksion testning to'rtta tuzog'i: (1) lazy loading test ichida ishlaydi, chunki Session ochiq - production'da esa `LazyInitializationException` chiqadi; (2) `flush` bo'lmagani uchun constraint va trigger xatolari yashirinadi; (3) real commit bo'lmagani uchun `@TransactionalEventListener(phase = AFTER_COMMIT)` va `afterCommit` callback'lari hech qachon ishlamaydi; (4) `webEnvironment = RANDOM_PORT`'da test tranzaksiyasi server thread'iga umuman tegmaydi, demak rollback illyuziya bo'ladi. Shu hollarda `@Transactional`'ni olib tashlab, tozalashni aniq qilish kerak; oraliq variant - `TestTransaction.flagForCommit()`/`end()`/`start()` bilan tranzaksiya chegaralarini test ichida qo'lda boshqarish yoki `@Commit` ishlatish.

## 7.12 Slice test anti-patternlari

**Hamma joyda `@SpringBootTest`.** Eng keng tarqalgan xato: controller mapping'ini tekshirish uchun butun kontekst ko'tariladi. Natija - sekin suite va noaniq xato sabablari. Qoida: `@WebMvcTest` yetsa, `@SpringBootTest` ishlatilmasin.

**Kontekstni har testda iflos qilish.** `@DirtiesContext`, test-ga xos `@TestPropertySource`, har sinfda boshqa `@MockitoBean` to'plami - bularning har biri yangi kontekst. Bu "biz CI'ni kuchaytirmoqchimiz" muammosining asl sababi.

**H2'da PostgreSQL xatti-harakatini kutish.** `@DataJpaTest`'ning jimgina DataSource almashtirishi eng xavfli default. H2 boshqa SQL dialekti, boshqa tip tizimi, boshqa lock va isolation semantikasi. H2 mapping va oddiy query uchun yaroqli, lekin baza xatti-harakati haqidagi hech bir xulosaga asos bo'lmaydi.

**MockMvc bilan biznes logikani testlash.** Agar `@WebMvcTest`'da narx hisoblash yoki chegirma qoidalari tekshirilayotgan bo'lsa, demak logika controller'da qolib ketgan yoki test noto'g'ri qatlamda yozilgan. HTTP testi faqat kontraktni tekshirsin.

**Slice'ni mock bilan to'ldirish.** `@WebMvcTest`'da o'nta `@MockitoBean` bo'lsa, controller haddan tashqari ko'p bog'liqlikka ega. Test dizayn muammosini ko'rsatib turadi - buni tuzatish kerak, mock qo'shish emas.

## 7.13 Arxitektor nazorat ro'yxati

- [ ] Har bir test o'z qatlamiga mos slice annotatsiyasidan foydalanadi; `@SpringBootTest` faqat qatlamlar kesishgan oqimlar uchun qoldirilgan.
- [ ] `@MockBean`/`@SpyBean` butun kod bazasidan olib tashlangan, o'rniga `@MockitoBean`/`@MockitoSpyBean`/`@TestBean` ishlatiladi.
- [ ] Integratsion testlar bitta umumiy abstract bazaviy sinfdan meros oladi; kontekstlar soni o'lchangan va 3-5 atrofida ushlab turiladi.
- [ ] `@DirtiesContext` ishlatilgan har bir joy asoslangan; aks holda holat testning o'zida tozalanadi.
- [ ] `@DataJpaTest` qaysi bazada ishlayotgani aniq: H2 faqat mapping uchun, baza xatti-harakatiga bog'liq query'lar real bazada tekshiriladi.
- [ ] Kritik query'lar uchun query soni (Hibernate statistics yoki datasource-proxy) aniq raqam bilan tasdiqlangan, N+1 regressiya testda ushlanadi.
- [ ] API kontrakti (JSON maydonlari, status kodlari, `ProblemDetail` formati) `@WebMvcTest`/`@JsonTest` bilan qoplangan, ichki maydonlar sizib chiqmasligi tekshirilgan.
- [ ] Commit'dan keyingi xatti-harakat (AFTER_COMMIT event, trigger, constraint) tranzaksiyasiz testda tekshiriladi, tozalash esa `@Sql` yoki aniq cleanup bilan bajariladi.

---

[&larr; 6. Unit test Spring loyihasida: kontekstsiz testlash](06-unit-test-spring-loyihasida-kontekstsiz.md) · [Mundarija](README.md) · [8. Testcontainers bilan real infratuzilmada test &rarr;](08-testcontainers-bilan-real-infratuzilmada.md)
