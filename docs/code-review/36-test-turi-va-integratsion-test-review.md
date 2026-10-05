<!-- doc: code-review | chapter: 36 | part: VII. Test review -->

[Barcha hujjatlar](../../README.md) / [Kod review](README.md)

> Holat: AI yozgan, inson tekshirmagan.

# 36. Test turi va integratsion test review (Test Types and Integration Tests)

<details>
<summary>Bu bobdagi 9 bo'lim</summary>

- [36.1 Daraja tanlash mezoni](#361-daraja-tanlash-mezoni)
- [36.2 H2 va haqiqiy PostgreSQL](#362-h2-va-haqiqiy-postgresql)
- [36.3 Spring test slice larini to'g'ri ishlatish](#363-spring-test-slice-larini-togri-ishlatish)
- [36.4 Tashqi servislarni sinash](#364-tashqi-servislarni-sinash)
- [36.5 Kontrakt testlari](#365-kontrakt-testlari)
- [36.6 Migratsiya va sxema testlari](#366-migratsiya-va-sxema-testlari)
- [36.7 Testlar nimani qoplamasligi kerak](#367-testlar-nimani-qoplamasligi-kerak)
- [36.8 Review checklisti: test turlari](#368-review-checklisti-test-turlari)
- [36.9 Amalda qo'llash](#369-amalda-qollash)

</details>


Uchinchi test savoli - to'g'ri daraja tanlanganmi. Bitta xato ikki shaklda bo'ladi: mantiqni integratsion testda sinash (sekin va mo'rt) yoki integratsiyani unit testda sinash (hech narsa tekshirilmaydi). Review da bu tanlovni baholash oson, chunki belgilar aniq.

## 36.1 Daraja tanlash mezoni

| Nima sinaladi | To'g'ri daraja | Belgisi noto'g'ri tanlanganining |
| --- | --- | --- |
| Hisob, qoida, shart | Unit (domen) | `@SpringBootTest` bilan sinash |
| Validatsiya annotatsiyalari | `@WebMvcTest` yoki validator unit | Butun kontekst |
| So'rov mapping, status, JSON shakli | `@WebMvcTest` | Haqiqiy baza bilan |
| JPA mapping, so'rov, migratsiya | `@DataJpaTest` + Testcontainers | H2 yoki mock |
| Tranzaksiya chegarasi, qulf, poyga | Integratsion (haqiqiy PostgreSQL) | Mock repository |
| Tashqi HTTP integratsiya | WireMock bilan | Haqiqiy servis |
| Butun oqim (bir necha komponent) | Integratsion, kam sonli | Hamma narsa shu darajada |
| Xavfsizlik qoidalari | `@SpringBootTest` + MockMvc | Faqat unit |

```java
// Noto'g'ri daraja: sof hisob butun kontekst bilan sinalgan.
@SpringBootTest                                  // 8 sekund ishga tushish
class DiscountCalculatorTest {
    @Autowired DiscountCalculator calculator;
    @Test void goldGetsFifteenPercent() { ... }  // hech qanday bog'liqlik kerak emas
}
// Review izohi: DiscountCalculator ning bog'liqligi yo'q (yoki faqat sof
// funksiyalar). `new DiscountCalculator()` bilan sinash 10 ms oladi va
// 8 sekund tejaydi. 50 shunday test = pipeline da 7 daqiqa.

// To'g'ri: oddiy unit test.
class DiscountCalculatorTest {
    private final DiscountCalculator calculator = new DiscountCalculator();
    @Test void goldGetsFifteenPercent() { ... }
}
```

## 36.2 H2 va haqiqiy PostgreSQL

Bu review da eng ko'p bahs tug'diradigan mavzu, lekin javob aniq: PostgreSQL ishlatadigan loyihada testlar ham PostgreSQL da ishlashi kerak.

| Farq | H2 da | PostgreSQL da |
| --- | --- | --- |
| `jsonb` | Yo'q yoki taqlid | To'liq |
| Massiv turlari | Cheklangan | To'liq |
| `ON CONFLICT` | Qisman | To'liq |
| Partial va ifoda indekslari | Yo'q | Bor |
| `FOR UPDATE SKIP LOCKED` | Yo'q | Bor |
| Izolyatsiya xulqi | Boshqacha | Haqiqiy MVCC |
| Tur konversiyalari | Yumshoqroq | Qattiq |
| `timestamptz` semantikasi | Farq qiladi | Haqiqiy |
| Migratsiyalar | Ba'zilari ishlamaydi | Haqiqiy |
| Reja va indeks ishlashi | Ma'nosiz | Haqiqiy |
| Window funksiyalar, CTE | Qisman | To'liq |
| `citext`, `pg_trgm`, kengaytmalar | Yo'q | Bor |

```java
// To'g'ri shakl: Testcontainers, bir marta ishga tushadigan konteyner.
@TestConfiguration(proxyBeanMethods = false)
public class PostgresTestConfig {

    // @ServiceConnection: Spring Boot 3.1+ - URL va kalitlarni o'zi ulaydi.
    @Bean
    @ServiceConnection
    PostgreSQLContainer<?> postgres() {
        return new PostgreSQLContainer<>(DockerImageName.parse("postgres:16-alpine"))
            // Qayta ishlatish: lokalda testlar orasida konteyner saqlanadi
            // (~/.testcontainers.properties da testcontainers.reuse.enable=true).
            .withReuse(true);
    }
}

// Bazaviy klass: bitta kontekst, bitta konteyner - butun to'plam uchun.
@SpringBootTest
@Import(PostgresTestConfig.class)
public abstract class IntegrationTest {
    @Autowired protected MockMvcTester mvc;
    // Tozalash strategiyasi bir joyda (35.4).
    @AfterEach void clean() { jdbc.execute("TRUNCATE orders, payment CASCADE"); }
}
// Review foydasi: har test klassi o'z konfiguratsiyasini yozmaydi, ya'ni
// Spring kontekst bir marta quriladi va pipeline tez ishlaydi.
```

## 36.3 Spring test slice larini to'g'ri ishlatish

```java
// @WebMvcTest: faqat web qatlam, servis mock qilinadi - tez.
@WebMvcTest(OrderController.class)
class OrderControllerTest {
    @Autowired MockMvcTester mvc;
    @MockitoBean OrderService service;           // Spring Boot 3.4+ nomi

    @Test
    void returnsValidationErrorForEmptyLines() {
        assertThat(mvc.post().uri("/api/orders")
                      .contentType(APPLICATION_JSON)
                      .content("""
                               {"customer": {"id": "..."}, "lines": []}
                               """))
            .hasStatus(HttpStatus.BAD_REQUEST)
            .bodyJson().extractingPath("$.errors[0].field").isEqualTo("lines");
    }
    // Bu test aynan web qatlamni sinaydi: validatsiya, status, JSON shakli.
}

// @DataJpaTest: faqat JPA, haqiqiy baza bilan.
@DataJpaTest
@Import(PostgresTestConfig.class)
@AutoConfigureTestDatabase(replace = AutoConfigureTestDatabase.Replace.NONE)   // H2 ni almashtirmaslik
class OrderRepositoryTest {
    @Test
    void findsOpenOrdersWithLinesInSingleQuery() { ... }
}
// Diqqat: @DataJpaTest standart holatda @Transactional - har test rollback.
// Bu poyga va qulf testlari uchun yaroqsiz (35.4).

// @JsonTest: serializatsiya shaklini qulflash.
@JsonTest
class OrderResponseJsonTest {
    @Autowired JacksonTester<OrderResponse> json;

    @Test
    void serializesMoneyAsStringAndDateAsIso() throws Exception {
        OrderResponse r = new OrderResponse(ID, "ORD-1", "NEW",
                new BigDecimal("1000.00"), "UZS", OffsetDateTime.parse("2026-10-04T12:00:00Z"));
        assertThat(json.write(r)).isEqualToJson("""
            {"id":"...","number":"ORD-1","status":"NEW",
             "total":"1000.00","currency":"UZS","createdAt":"2026-10-04T12:00:00Z"}
            """);
    }
    // Review foydasi: API shakli test bilan qulflangan. Jackson
    // sozlamasi tasodifan o'zgarsa yoki maydon qo'shilsa, test gapiradi
    // ([37-bob](37-api-moslik-va-breaking-change-review.md): orqaga moslik).
}
```

## 36.4 Tashqi servislarni sinash

```java
// Noto'g'ri: haqiqiy tashqi servisga murojaat.
@Test void fetchesRate() {
    Rate rate = client.rateFor("USD");           // internetga chiqadi
    assertThat(rate).isNotNull();                // beqaror va ma'nosiz
}

// To'g'ri: WireMock bilan - xulqni to'liq nazorat qilish.
@SpringBootTest
@AutoConfigureWireMock(ports = 0)                // tasodifiy port
class RateClientTest {

    @Test
    void parsesSuccessfulResponse() {
        stubFor(get("/rates/USD").willReturn(okJson("""
            {"currency":"USD","rate":"12750.00","asOf":"2026-10-04"}
            """)));
        assertThat(client.rateFor("USD").value()).isEqualByComparingTo("12750.00");
    }

    @Test
    void retriesOnServerErrorThenSucceeds() {
        stubFor(get("/rates/USD").inScenario("retry")
            .whenScenarioStateIs(STARTED)
            .willReturn(serverError()).willSetStateTo("second"));
        stubFor(get("/rates/USD").inScenario("retry")
            .whenScenarioStateIs("second")
            .willReturn(okJson("""{"rate":"12750.00"}""")));

        assertThat(client.rateFor("USD")).isNotNull();
        verify(2, getRequestedFor(urlEqualTo("/rates/USD")));   // retry ishladi
    }

    @Test
    void failsFastOnTimeout() {
        stubFor(get("/rates/USD").willReturn(ok().withFixedDelay(5_000)));
        long start = System.nanoTime();
        assertThatThrownBy(() -> client.rateFor("USD"))
            .isInstanceOf(RateServiceUnavailable.class);
        // Timeout 2 sekund bo'lishi kerak: 5 sekund kutmaydi.
        assertThat(Duration.ofNanos(System.nanoTime() - start))
            .isLessThan(Duration.ofSeconds(3));
    }

    @Test
    void rejectsMalformedResponse() {
        stubFor(get("/rates/USD").willReturn(okJson("""{"rate":"not-a-number"}""")));
        assertThatThrownBy(() -> client.rateFor("USD"))
            .isInstanceOf(InvalidGatewayResponse.class);
    }
}
// Review talabi: har bir tashqi integratsiya uchun kamida shu to'rt test -
// muvaffaqiyat, xato, timeout, noto'g'ri javob (34.5).
```

## 36.5 Kontrakt testlari

```java
// Review savoli: ichki servislar orasidagi shartnoma qanday himoyalangan?
// Variant 1: iste'molchi tomonidan boshqariladigan kontrakt (Pact).
// Variant 2: sxema registri (Avro, Protobuf, JSON Schema).
// Variant 3: provayder tomonda shaklni qulflaydigan test (eng oddiy).

// Variant 3 ning amaliy shakli: API javobi shaklini snapshot qilish.
@Test
void orderResponseContractIsStable() throws Exception {
    String actual = mvc.get().uri("/api/orders/{id}", KNOWN_ID)
                       .exchange().getResponse().getContentAsString();
    // Fayl: src/test/resources/contracts/order-response.json
    assertThat(actual).isEqualToIgnoringWhitespace(
        Files.readString(Path.of("src/test/resources/contracts/order-response.json")));
}
// Review foydasi: javob shakli o'zgarsa, test yiqiladi va muallif
// ongli qaror qabul qilishga majbur bo'ladi: bu breaking change mi?
// Snapshot ni yangilash - ongli harakat, tasodifiy emas.
```

## 36.6 Migratsiya va sxema testlari

```java
// Review talabi: migratsiyalar test bilan qoplangan (25.7).
@Test
void jpaEntitiesMatchFlywaySchema() {
    // Hibernate sxema validatsiyasi: entity va jadval mos kelmasa,
    // kontekst ishga tushmaydi.
    // spring.jpa.hibernate.ddl-auto=validate (test profilida)
    // Bu test kontekst qurilishining o'zi bilan bajariladi.
}

// Qo'shimcha: ortiqcha ustun va indekslarni aniqlash.
@Test
void noUnusedColumnsInCriticalTables() {
    List<String> columns = jdbc.queryForList("""
        SELECT column_name FROM information_schema.columns
         WHERE table_name = 'orders'
        """, String.class);
    // Entity maydonlari bilan solishtirish: bazada bor, kodda yo'q
    // ustunlar - yoki meros, yoki esdan chiqqan migratsiya.
    assertThat(columns).doesNotContain("legacy_status", "temp_flag");
}
```

```yaml
# Test profilida majburiy sozlamalar: review da shu ro'yxat tekshiriladi.
spring:
  jpa:
    hibernate:
      ddl-auto: validate        # entity va sxema mosligini tekshiradi
    open-in-view: false         # lazy xatolari testda chiqadi
    properties:
      hibernate:
        generate_statistics: true    # so'rov sonini o'lchash uchun
  flyway:
    enabled: true               # sxema migratsiyalardan quriladi, ddl-auto dan emas
  sql:
    init:
      mode: never               # schema.sql bilan chalkashmaslik
```

## 36.7 Testlar nimani qoplamasligi kerak

Review da teskari xato ham bo'ladi: ortiqcha test yozish. Ortiqcha testlar qo'llab-quvvatlash yuki beradi va refactoringni qiyinlashtiradi.

| Qoplanmasligi kerak | Nega |
| --- | --- |
| Getter va setter | Hech qanday mantiq yo'q |
| Framework xulqi | Spring ni sinash bizning ishimiz emas |
| Generated kod | Mapper, DTO, protobuf |
| Konfiguratsiya qiymatlari | `@Value` ning o'qilishi |
| Bir xil mantiq ikki darajada | Unit va integratsion bir xil shartni |
| Shaxsiy metodlar to'g'ridan-to'g'ri | Public xulq orqali |
| Log xabarlari matni | Mo'rt va qiymatsiz |
| `toString` natijasi | Maskalash tashqari (32.1) |

Review mezoni: test yiqilsa, u haqiqiy xatoni ko'rsatadimi yoki shunchaki kod o'zgarganini. Ikkinchi holatda test qiymat bermaydi, lekin refactoring narxini oshiradi.

## 36.8 Review checklisti: test turlari

| Savol | Nega |
| --- | --- |
| Sof mantiq unit testdami | Sekin pipeline |
| Baza testlari haqiqiy PostgreSQL dami | H2 farqlari |
| `@SpringBootTest` soni cheklanganmi | Kontekst qurilishi |
| Kontekst kombinatsiyalari kamaytirilganmi | Har kombinatsiya yangi kontekst |
| Tashqi servis WireMock bilanmi | Beqarorlik |
| Har integratsiya uchun 4 xato yo'li bormi | Qamralmagan xato holatlari |
| Migratsiyalar test bilan qoplanganmi | Deploy xatosi |
| `ddl-auto: validate` yoqilganmi | Entity va sxema farqi |
| API javob shakli qulflangangmi | Tasodifiy breaking change |
| Tranzaksiya testlari rollback siz ishlaydimi | Yashirin xulq |
| Getter va framework xulqi sinalmayaptimi | Ortiqcha yuk |

## 36.9 Amalda qo'llash

- [ ] `@SpringBootTest` ishlatadigan testlarni sanab, ularning qanchasi sof mantiqni sinayotganini aniqlang va unit testga o'tkazing.
- [ ] H2 ishlatilayotgan bo'lsa, Testcontainers + PostgreSQL ga o'tish rejasini tuzing.
- [ ] Bitta bazaviy integratsion test klassini yaratib, barcha integratsion testlarni unga asoslang (bitta kontekst).
- [ ] Testcontainers `withReuse(true)` ni lokal ishlab chiqish uchun yoqing.
- [ ] Har bir tashqi integratsiya uchun WireMock bilan to'rt test (muvaffaqiyat, xato, timeout, noto'g'ri javob) yozing.
- [ ] Test profilida `ddl-auto: validate` va `open-in-view: false` ni yoqing.
- [ ] Asosiy API javoblari uchun shakl snapshot testlarini qo'shing.
- [ ] Getter/setter va framework xulqini sinaydigan testlarni toping va olib tashlang.
- [ ] Spring kontekst necha marta qurilayotganini o'lchab, kombinatsiyalarni kamaytirish rejasini tuzing.

---

[&larr; 35. Test sifati review: assertion, izolyatsiya, beqarorlik](35-test-sifati-review-assertion-izolyatsiya.md) · [Mundarija](README.md) · [37. API moslik va breaking change review &rarr;](37-api-moslik-va-breaking-change-review.md)
