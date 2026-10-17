<!-- doc: patterns | chapter: 23 | part:  -->

[Barcha hujjatlar](../../README.md) / [Dizayn patternlar](README.md)

> Holat: tekshirilmoqda. Da'volar hali manbaga solishtirilmoqda.

# 23. Testing patternlari (Testing Patterns)

<details>
<summary>Bu bobdagi 90 bo'lim</summary>

- [23.1 Test piramidasi / Testing Trophy / Honeycomb (Test Pyramid / Testing Trophy / Honeycomb)](#231-test-piramidasi--testing-trophy--honeycomb-test-pyramid--testing-trophy--honeycomb)
- [23.2 Test dublyorlari (Test Doubles - Dummy, Fake, Stub, Spy, Mock)](#232-test-dublyorlari-test-doubles---dummy-fake-stub-spy-mock)
- [23.3 Tayyorlash-Bajarish-Tasdiqlash (Arrange-Act-Assert)](#233-tayyorlash-bajarish-tasdiqlash-arrange-act-assert)
- [23.4 Berilgan-Qachon-Unda (Given-When-Then - BDD)](#234-berilgan-qachon-unda-given-when-then---bdd)
- [23.5 Test ma'lumot quruvchisi (Test Data Builder)](#235-test-malumot-quruvchisi-test-data-builder)
- [23.6 Obyekt-ona (Object Mother)](#236-obyekt-ona-object-mother)
- [23.7 Fixture (yangi va umumiy - Fixture: fresh vs shared)](#237-fixture-yangi-va-umumiy---fixture-fresh-vs-shared)
- [23.8 Parametrlangan testlar (Parameterized Tests)](#238-parametrlangan-testlar-parameterized-tests)
- [23.9 Xususiyatga asoslangan testlash (Property-Based Testing - jqwik)](#239-xususiyatga-asoslangan-testlash-property-based-testing---jqwik)
- [23.10 Mutatsion testlash (Mutation Testing - PIT)](#2310-mutatsion-testlash-mutation-testing---pit)
- [23.11 Test bo'laklari (Test Slices - @WebMvcTest, @DataJpaTest, @JsonTest, @RestClientTest)](#2311-test-bolaklari-test-slices---webmvctest-datajpatest-jsontest-restclienttest)
- [23.12 @SpringBootTest va context keshlash (@SpringBootTest & context caching)](#2312-springboottest-va-context-keshlash-springboottest--context-caching)
- [23.13 @MockitoBean / @MockitoSpyBean](#2313-mockitobean--mockitospybean)
- [23.14 Test konfiguratsiyasi (@TestConfiguration)](#2314-test-konfiguratsiyasi-testconfiguration)
- [23.15 Testcontainers va servis ulanishi (Testcontainers & @ServiceConnection)](#2315-testcontainers-va-servis-ulanishi-testcontainers--serviceconnection)
- [23.16 Embedded DB mos kelmasligi (Embedded DB Mismatch - anti-pattern: H2 for PostgreSQL)](#2316-embedded-db-mos-kelmasligi-embedded-db-mismatch---anti-pattern-h2-for-postgresql)
- [23.17 Kontrakt testlash (Contract Testing)](#2317-kontrakt-testlash-contract-testing)
- [23.18 Servis komponent testi (Service Component Test)](#2318-servis-komponent-testi-service-component-test)
- [23.19 Servis integratsiya kontrakti testi (Service Integration Contract Test)](#2319-servis-integratsiya-kontrakti-testi-service-integration-contract-test)
- [23.20 Iste'molchi tomonidagi kontrakt testi (Consumer-Side Contract Test)](#2320-istemolchi-tomonidagi-kontrakt-testi-consumer-side-contract-test)
- [23.21 Arxitektura testlari (Architecture Tests - ArchUnit, Spring Modulith verify)](#2321-arxitektura-testlari-architecture-tests---archunit-spring-modulith-verify)
- [23.22 Tasdiqlash / Golden Master testlash (Approval / Golden Master Testing)](#2322-tasdiqlash--golden-master-testlash-approval--golden-master-testing)
- [23.23 Snapshot testlash (Snapshot Testing)](#2323-snapshot-testlash-snapshot-testing)
- [23.24 Xarakterizatsiya testlari (Characterization Tests)](#2324-xarakterizatsiya-testlari-characterization-tests)
- [23.25 Kamtarin obyekt (Humble Object)](#2325-kamtarin-obyekt-humble-object)
- [23.26 Sahifa obyekti (Page Object)](#2326-sahifa-obyekti-page-object)
- [23.27 Servis stub (Service Stub)](#2327-servis-stub-service-stub)
- [23.28 Ma'lumotlar bazasi holatini tayyorlash (Database State Setup)](#2328-malumotlar-bazasi-holatini-tayyorlash-database-state-setup)
- [23.29 Transactional test rollback tuzoqlari (Transactional Test Rollback Pitfalls)](#2329-transactional-test-rollback-tuzoqlari-transactional-test-rollback-pitfalls)
- [23.30 Clock injection (Clock Injection)](#2330-clock-injection-clock-injection)
- [23.31 Germetik testlar (Hermetic Tests)](#2331-germetik-testlar-hermetic-tests)
- [23.32 Flaky testlarni karantinga olish (Flaky Test Quarantine)](#2332-flaky-testlarni-karantinga-olish-flaky-test-quarantine)
- [23.33 Unumdorlik va yuklama testlari (Performance / Load Testing)](#2333-unumdorlik-va-yuklama-testlari-performance--load-testing)
- [23.34 Smoke testlar (Smoke Tests)](#2334-smoke-testlar-smoke-tests)
- [23.35 Uchidan-uchiga testlar (End-to-End Tests)](#2335-uchidan-uchiga-testlar-end-to-end-tests)
- [23.36 Reactive kodni test qilish (Testing Reactive Code)](#2336-reactive-kodni-test-qilish-testing-reactive-code)
- [23.37 Xavfsizlikni test qilish (Testing Security)](#2337-xavfsizlikni-test-qilish-testing-security)
- [23.38 Event'larni test qilish (Testing Events)](#2338-eventlarni-test-qilish-testing-events)
- [23.39 Asinxron kodni test qilish (Testing Async Code)](#2339-asinxron-kodni-test-qilish-testing-async-code)
- [23.40 Dummy obyekt (Dummy Object)](#2340-dummy-obyekt-dummy-object)
- [23.41 Test stub (Test Stub)](#2341-test-stub-test-stub)
- [23.42 Test spy (Test Spy)](#2342-test-spy-test-spy)
- [23.43 Mock obyekt (Mock Object)](#2343-mock-obyekt-mock-object)
- [23.44 Soxta obyekt (Fake Object)](#2344-soxta-obyekt-fake-object)
- [23.45 To'rt fazali test (Four-Phase Test)](#2345-tort-fazali-test-four-phase-test)
- [23.46 Yaratish metodi (Creation Method)](#2346-yaratish-metodi-creation-method)
- [23.47 Delta assertion (Delta Assertion)](#2347-delta-assertion-delta-assertion)
- [23.48 Guard assertion (Guard Assertion)](#2348-guard-assertion-guard-assertion)
- [23.49 Maxsus assertion (Custom Assertion)](#2349-maxsus-assertion-custom-assertion)
- [23.50 Yangi fixture (Fresh Fixture)](#2350-yangi-fixture-fresh-fixture)
- [23.51 Umumiy Fixture (Shared Fixture)](#2351-umumiy-fixture-shared-fixture)
- [23.52 Oldindan Qurilgan Fixture (Prebuilt Fixture)](#2352-oldindan-qurilgan-fixture-prebuilt-fixture)
- [23.53 Dangasa Sozlash (Lazy Setup)](#2353-dangasa-sozlash-lazy-setup)
- [23.54 To'plam Darajasidagi Fixture Sozlash (Suite Fixture Setup)](#2354-toplam-darajasidagi-fixture-sozlash-suite-fixture-setup)
- [23.55 Fixture Bo'yicha Test Sinfi (Testcase Class per Fixture)](#2355-fixture-boyicha-test-sinfi-testcase-class-per-fixture)
- [23.56 Test Ilgagi (Test Hook)](#2356-test-ilgagi-test-hook)
- [23.57 Orqa Eshik Manipulyatsiyasi (Back Door Manipulation)](#2357-orqa-eshik-manipulyatsiyasi-back-door-manipulation)
- [23.58 Qatlam Testi (Layer Test)](#2358-qatlam-testi-layer-test)
- [23.59 Jadvalni Bo'shatish Orqali Tozalash (Table Truncation Teardown)](#2359-jadvalni-boshatish-orqali-tozalash-table-truncation-teardown)
- [23.60 Avtomatik Tozalash (Automated Teardown)](#2360-avtomatik-tozalash-automated-teardown)
- [23.61 Tasdiqlash Testi (Approval Test)](#2361-tasdiqlash-testi-approval-test)
- [23.62 Test metodi va testcase sinfi (Test Method / Testcase Class)](#2362-test-metodi-va-testcase-sinfi-test-method--testcase-class)
- [23.63 Test runner, testcase obyekti va test to'plami obyekti (Test Runner / Testcase Object / Test Suite Object)](#2363-test-runner-testcase-obyekti-va-test-toplami-obyekti-test-runner--testcase-object--test-suite-object)
- [23.64 Testlarni topish, sanash va tanlash (Test Discovery / Test Enumeration / Test Selection)](#2364-testlarni-topish-sanash-va-tanlash-test-discovery--test-enumeration--test-selection)
- [23.65 Assertion metodi va assertion xabari (Assertion Method / Assertion Message)](#2365-assertion-metodi-va-assertion-xabari-assertion-method--assertion-message)
- [23.66 Tugallanmagan test tasdigi (Unfinished Test Assertion)](#2366-tugallanmagan-test-tasdigi-unfinished-test-assertion)
- [23.67 Holatni va xulqni tekshirish (State Verification / Behavior Verification)](#2367-holatni-va-xulqni-tekshirish-state-verification--behavior-verification)
- [23.68 Fixture sozlashning uch shakli (In-line Setup / Delegated Setup / Implicit Setup)](#2368-fixture-sozlashning-uch-shakli-in-line-setup--delegated-setup--implicit-setup)
- [23.69 Setup dekoratori va zanjirli testlar (Setup Decorator / Chained Tests)](#2369-setup-dekoratori-va-zanjirli-testlar-setup-decorator--chained-tests)
- [23.70 Minimal va standart fixture (Minimal Fixture / Standard Fixture)](#2370-minimal-va-standart-fixture-minimal-fixture--standard-fixture)
- [23.71 Tozalashning uch shakli (Garbage-Collected / In-line / Implicit Teardown)](#2371-tozalashning-uch-shakli-garbage-collected--in-line--implicit-teardown)
- [23.72 Tranzaksiyani qaytarish orqali tozalash (Transaction Rollback Teardown)](#2372-tranzaksiyani-qaytarish-orqali-tozalash-transaction-rollback-teardown)
- [23.73 Konfiguratsiyalanadigan va qattiq kodlangan test dublyori (Configurable / Hard-Coded Test Double)](#2373-konfiguratsiyalanadigan-va-qattiq-kodlangan-test-dublyori-configurable--hard-coded-test-double)
- [23.74 Testga xos subklass (Test-Specific Subclass)](#2374-testga-xos-subklass-test-specific-subclass)
- [23.75 Test utility metodi va test helper (Test Utility Method / Test Helper)](#2375-test-utility-metodi-va-test-helper-test-utility-method--test-helper)
- [23.76 Test superklassi (Testcase Superclass)](#2376-test-superklassi-testcase-superclass)
- [23.77 Test sinfini sinf va feature bo'yicha tashkil qilish (Testcase Class per Class / per Feature)](#2377-test-sinfini-sinf-va-feature-boyicha-tashkil-qilish-testcase-class-per-class--per-feature)
- [23.78 Baza qumloqi (Database Sandbox)](#2378-baza-qumloqi-database-sandbox)
- [23.79 Stored procedure testi (Stored Procedure Test)](#2379-stored-procedure-testi-stored-procedure-test)
- [23.80 Bog'liqlikni izlash (Dependency Lookup)](#2380-bogliqlikni-izlash-dependency-lookup)
- [23.81 Test qiymatlari: literal, hosila va generatsiya (Literal Value / Derived Value / Generated Value)](#2381-test-qiymatlari-literal-hosila-va-generatsiya-literal-value--derived-value--generated-value)
- [23.82 Yozib olingan test va skript test (Recorded Test / Scripted Test)](#2382-yozib-olingan-test-va-skript-test-recorded-test--scripted-test)
- [23.83 Ma'lumotga asoslangan test (Data-Driven Test)](#2383-malumotga-asoslangan-test-data-driven-test)
- [23.84 Global murojaatni testga ochish (Encapsulate Global References / Replace Global Reference with Getter)](#2384-global-murojaatni-testga-ochish-encapsulate-global-references--replace-global-reference-with-getter)
- [23.85 Statik metodni test uchun ochish (Expose Static Method / Introduce Instance Delegator / Introduce Static Setter)](#2385-statik-metodni-test-uchun-ochish-expose-static-method--introduce-instance-delegator--introduce-static-setter)
- [23.86 Chaqiruvni ajratib override qilish (Extract and Override Call / Factory Method / Getter)](#2386-chaqiruvni-ajratib-override-qilish-extract-and-override-call--factory-method--getter)
- [23.87 Maydonni testda almashtirish (Supersede Instance Variable)](#2387-maydonni-testda-almashtirish-supersede-instance-variable)
- [23.88 O'zgarmas umumiy fixture (Immutable Shared Fixture)](#2388-ozgarmas-umumiy-fixture-immutable-shared-fixture)
- [23.89 Entity zanjirini kesish (Entity Chain Snipping)](#2389-entity-zanjirini-kesish-entity-chain-snipping)
- [23.90 Amalda qo'llash](#2390-amalda-qollash)

</details>



Testing patternlari - bu kodni tekshirishning emas, balki **tizim dizaynini tasdiqlashning** vositalari to'plami. Arxitektor uchun test strategiyasi arxitektura qarori darajasida muhim: qaysi qatlamda qancha test yozilishi CI quvur vaqtini, refactoring tezligini va production incidentlarning chastotasini bevosita belgilaydi. Noto'g'ri tanlangan test piramidasi yoki nazoratsiz Spring context'lar soni build vaqtini 3 daqiqadan 40 daqiqaga chiqarib, jamoaning release ritmini buzadi. Quyidagi patternlar testlarni ishonchli (deterministik), tez va o'qiladigan qilishning sinovdan o'tgan usullarini beradi.

## 23.1 Test piramidasi / Testing Trophy / Honeycomb (Test Pyramid / Testing Trophy / Honeycomb)

**Tavsif:** Test turlarini soni va narxi bo'yicha qanday nisbatda taqsimlashni belgilovchi strategik modellar. Klassik piramida ko'p unit, o'rtacha integration va juda kam E2E testni taklif qiladi; Testing Trophy (Kent C. Dodds) markazni integration testlarga suradi; Honeycomb (Spotify) esa mikroservislar uchun integrated test'larni asosiy qatlam qilib oladi. Tanlov arxitekturaga bog'liq: boy domain modeli bo'lsa piramida, nozik CRUD/adapter servis bo'lsa trophy yoki honeycomb mantiqiyroq.

**Spring'da qayerda uchraydi:** Unit qatlam - oddiy JUnit 5 (`@Test`) + Mockito, Spring context'siz; integration qatlam - Spring Boot test slice'lari (`@WebMvcTest`, `@DataJpaTest`) va Testcontainers (`@Testcontainers`, `@ServiceConnection` Spring Boot 3.1+); E2E - `@SpringBootTest(webEnvironment = RANDOM_PORT)` + `TestRestClient`/`RestTestClient` (Spring Framework 7.x) yoki `WebTestClient`. Maven'da `maven-surefire-plugin` unit, `maven-failsafe-plugin` (`*IT.java`) integration testlarni ajratadi.

**Qo'llanish keyslari:**
- Monolit boy domain bilan: hisob-kitob va business rule'lar uchun minglab tez unit test, yuzlab integration test.
- Mikroservis-adapter (DB → REST mapping): trophy modeli, asosiy ishonch `@SpringBootTest` + Testcontainers'da.
- CI quvurini bosqichlash: PR'da faqat unit + slice testlar, nightly build'da to'liq E2E suite.
- Legacy tizimni refactoring qilishdan oldin yuqori qatlamda "characterization" testlar yozib, keyin pastga tushish.
- Mobile/SPA frontend bilan ishlovchi backend uchun contract test qatlamini E2E o'rniga qo'yish.

**Ehtiyot bo'ling:** Piramidani dogma sifatida qabul qilib, 100% mock'langan unit testlar bilan "yashil" suite yasash mumkin - ammo u mapping, transaction va SQL xatolarini mutlaqo ushlamaydi. Teskari xato - "muzqaymoq koni" (ice-cream cone): ko'p sekin E2E, kam unit; bu flaky testlar va uzoq feedback loop'ga olib keladi.

## 23.2 Test dublyorlari (Test Doubles - Dummy, Fake, Stub, Spy, Mock)

**Tavsif:** Sinovdan o'tayotgan obyektning haqiqiy kollaboratorlarini o'rnini bosuvchi obyektlar taksonomiyasi (Gerard Meszaros). Dummy - faqat parametrni to'ldirish uchun, hech qachon chaqirilmaydi; Fake - ishlaydigan, lekin soddalashtirilgan implementatsiya (in-memory repository); Stub - oldindan belgilangan javob qaytaradi (state verification); Spy - haqiqiy chaqiruvlarni yozib boradi; Mock - kutilgan interaksiyalar bilan oldindan programlanadi va ularni tekshiradi (behavior verification).

**Spring'da qayerda uchraydi:** Mockito (`org.mockito`) - `mock()`, `spy()`, `when(...).thenReturn(...)`, `verify()`, `@Mock`, `@Spy`, `@InjectMocks`, `@ExtendWith(MockitoExtension.class)`. Spring'ning o'z dublyorlari: `org.springframework.mock.web.MockHttpServletRequest`, `MockHttpSession`, `MockMultipartFile`, `MockEnvironment`, `MockClientHttpRequest`. Fake sifatida - H2/HSQLDB o'rniga Testcontainers tavsiya etiladi; `MockRestServiceServer` (spring-test) tashqi REST API'ni stub qiladi; `Clock.fixed()` vaqt uchun fake.

**Qo'llanish keyslari:**
- Tashqi to'lov gateway'ini stub qilib, "declined" javobini imitatsiya qilish.
- `Clock` bean'ini `Clock.fixed()` bilan almashtirib, muddati o'tgan obuna logikasini test qilish.
- `verify(auditPublisher).publish(any())` orqali audit event chiqarilganini tasdiqlash (mock).
- `InMemoryOrderRepository` fake bilan domain servis testlarini DB'siz juda tez yurgizish.
- `spy()` bilan haqiqiy servisning bitta sekin metodini stub qilib, qolganini real qoldirish.

**Ehtiyot bo'ling:** Mock'larni ortiqcha ishlatish testni implementatsiya detaliga bog'lab qo'yadi - har refactoring'da test sinadi, lekin bug topilmaydi. O'zingga tegishli bo'lmagan tashqi kutubxona (DB driver, HTTP client ichki sinflari) uchun mock yozmang; "Don't mock what you don't own" qoidasiga amal qiling va mavjud bo'lmagan metodni mock qilmaslik uchun strict stubs'ni yoqib qo'ying.

## 23.3 Tayyorlash-Bajarish-Tasdiqlash (Arrange-Act-Assert)

**Tavsif:** Har bir testni uchta vizual ajratilgan blokka bo'lish konvensiyasi: Arrange (ma'lumot va dublyorlarni sozlash), Act (sinovdan o'tayotgan yagona amal), Assert (natijani tekshirish). Bu struktura testni o'qishni bir necha soniyaga qisqartiradi va "bir test - bir xatti-harakat" qoidasini tabiiy ravishda majburlaydi. Act blokida bir nechta chaqiruv paydo bo'lishi testni bo'lish kerakligining signalidir.

**Spring'da qayerda uchraydi:** Toza JUnit 5 konvensiyasi - kod ichida izoh (`// given`, `// when`, `// then`) yoki bo'sh satr bilan ajratiladi, hech qanday annotatsiya talab qilmaydi. AssertJ (`org.assertj.core.api.Assertions.assertThat`) Assert blokini zanjirli va o'qiladigan qiladi; `assertThatThrownBy(...)` exception'ni Act+Assert sifatida ifodalaydi. Arrange blokida `@BeforeEach`, `TestDataBuilder` yoki `@Sql` skriptlari qo'llaniladi.

**Qo'llanish keyslari:**
- Service qatlamidagi har bir business qoida uchun yagona, bir sahifaga sig'adigan test.
- Code review'da Act bloki uzun bo'lsa - testni ikkiga bo'lish kerakligini aniqlash.
- Yangi jamoa a'zosi uchun test standartini CheckStyle/PR template orqali majburlash.
- `assertThatThrownBy` bilan validatsiya xatolarini aniq va qisqa tekshirish.
- Mavjud chalkash testlarni refactoring qilishda birinchi qadam sifatida AAA'ga keltirish.

**Ehtiyot bo'ling:** Assert blokida o'nlab tasdiqni to'plash "assertion roulette"ga olib keladi - test singanda qaysi qoida buzilganini aniqlash qiyinlashadi; AssertJ `assertAll`/`SoftAssertions` yoki alohida testlar afzal. Arrange blokini `@BeforeEach`ga ko'chirishga haddan tashqari urinish testni "mystery guest"ga aylantiradi.

## 23.4 Berilgan-Qachon-Unda (Given-When-Then - BDD)

**Tavsif:** AAA'ning business tilidagi ko'rinishi: ssenariy "Given <kontekst>, When <hodisa>, Then <kutilgan natija>" shaklida yoziladi va shu matn bajariladigan testga aylanadi. Maqsad - biznes-analitik, QA va dasturchi uchun yagona, bir xil tushuniladigan spetsifikatsiya yaratish (living documentation). Texnik jihatdan AAA bilan bir xil, ammo nomlanish va artefakt (feature file) darajasida farq qiladi.

**Spring'da qayerda uchraydi:** Cucumber-JVM + `io.cucumber:cucumber-spring` (`@CucumberContextConfiguration` bilan `@SpringBootTest`ni ulash, `.feature` fayllar Gherkin'da); JBehave; Spock (Groovy, `given:`/`when:`/`then:` bloklari, `spock-spring` moduli). Mockito'ning `BDDMockito` sinfi `given(...).willReturn(...)` va `then(mock).should()` sintaksisini beradi - bu Spring loyihalarida eng arzon BDD uslubidir.

**Qo'llanish keyslari:**
- Regulyator talablarini (KYC, AML qoidalari) bajariladigan va auditorga ko'rsatiladigan ssenariylarga aylantirish.
- Murakkab narx-chegirma matritsasini Cucumber `Scenario Outline` jadvali bilan ifodalash.
- Acceptance criteria'ni Jira ticket'dan to'g'ridan-to'g'ri `.feature` faylga ko'chirish.
- Domain hodisalari ketma-ketligini (order → payment → shipment) end-to-end ssenariyda tasvirlash.
- `BDDMockito` bilan oddiy unit testlarda o'qilishni yaxshilash, Cucumber infratuzilmasisiz.

**Ehtiyot bo'ling:** Cucumber qatlami o'zi bilan katta maintenance narxini olib keladi - agar `.feature` fayllarni faqat dasturchilar o'qisa, u sof ortiqcha abstraksiya; bu holda oddiy JUnit + AssertJ afzal. Glue kod'da global mutable state ishlatish ssenariylar orasida sirli bog'liqlik hosil qiladi.

## 23.5 Test ma'lumot quruvchisi (Test Data Builder)

**Tavsif:** Test obyektlarini fluent, zanjirli API orqali yaratish patterni: barcha maydonlar uchun mantiqiy default qiymatlar beriladi va test faqat o'zi uchun muhim bo'lgan maydonni override qiladi. Bu konstruktor parametrlari o'zgarganda yuzlab testni tuzatish zaruratini yo'qotadi va testning niyatini ("bu test - faqat muddati o'tgan obuna haqida") ko'rinadigan qiladi. Odatda immutable builder: har bir `with...()` metod yangi builder qaytaradi.

**Spring'da qayerda uchraydi:** Qo'lda yozilgan builder sinflari (`OrderTestDataBuilder.anOrder().withStatus(PAID).build()`), Lombok `@Builder` / `@Builder.Default` (production sinfda), yoki Java 17+ record'lar uchun wither-metodlar. Spring'ning o'z fluent builder'lari ham shu patternga misol: `MockMvcRequestBuilders.post(...)`, `UriComponentsBuilder`, `RestClient.builder()`, `Jwt.withTokenValue(...)` (spring-security-test). `instancio` yoki `java-faker` kutubxonalari random default'lar uchun qo'shimcha bo'ladi.

```java
Order order = anOrder()
        .withCustomer(aCustomer().withTier(GOLD).build())
        .withLine(aLine().withQuantity(3).build())
        .build();
```

**Qo'llanish keyslari:**
- 15+ maydonli `Invoice` aggregate'ini testda faqat bitta maydonni o'zgartirib yaratish.
- Nested obyekt graflarini (Order → Customer → Address) builder kompozitsiyasi orqali qurish.
- Yangi required maydon qo'shilganda faqat builder'ni tuzatib, 200 testni tegmasdan qoldirish.
- Noto'g'ri (invalid) holatlarni ataylab yasab, validatsiya testlarini yozish.
- Integration testda DB'ga yozish uchun realistik entity to'plamini tez generatsiya qilish.

**Ehtiyot bo'ling:** Builder'ni production kodga qo'shib, API'ni invalid holatlarga ochib qo'yish xato - test builder'lar `src/test/java`da (yoki alohida test-fixtures modulida) yashashi kerak. Default qiymatlar "sirli" bo'lib qolmasligi uchun ularni testda muhim bo'lgan joyda har doim aniq override qiling. To'liq misol, nested builder va Lombok `@Builder` bilan farqi testing hujjatidagi [Test Data Builder pattern](../testing/10-test-malumotlarini-boshqarish.md#103-test-data-builder-pattern) mavzusida.

## 23.6 Obyekt-ona (Object Mother)

**Tavsif:** Tipik test obyektlarini nomlangan factory metodlar orqali yetkazib beruvchi markazlashgan sinf: `CustomerMother.gold()`, `CustomerMother.blockedWithOverdueInvoice()`. Builder "qanday qurish"ni, Object Mother esa "qaysi kanonik ssenariy"ni ifodalaydi - ya'ni domain tilidagi nomlangan holatlar katalogi. Ikkalasi odatda birga ishlatiladi: Mother metodi ichida Builder chaqiriladi va to'liq tayyor obyekt qaytaradi.

**Spring'da qayerda uchraydi:** Sof Java pattern - `static` factory metodlarga ega test sinflari (`OrderMother`, `UserFixtures`). Gradle `java-test-fixtures` plugin'i yoki Maven'da `test-jar` orqali bu sinflarni modullar orasida ulashish mumkin. Spring loyihalarida ko'pincha `@TestConfiguration` ichidagi bean'lar yoki `@Sql` skriptlari bilan birgalikda, DB'ga kanonik ma'lumotni joylashtirish uchun qo'llaniladi.

**Qo'llanish keyslari:**
- Domain'ning kanonik personajlarini (`premiumCustomer`, `trialUser`, `suspendedMerchant`) bir joyda saqlash.
- Bir nechta Maven moduli orasida umumiy test fixture'larni `java-test-fixtures` orqali ulashish.
- Murakkab "blokdagi hisob + 3 ta to'lanmagan invoice" holatini bitta chaqiruvga qisqartirish.
- Microservice contract testlarida ikki tomon uchun bir xil namunaviy payload'ni ta'minlash.
- Yangi dasturchiga domain holatlarini o'qib tushunadigan katalog sifatida xizmat qilish.

**Ehtiyot bo'ling:** Mother sinfi vaqt o'tib yuzlab metodli "god fixture"ga aylanib, har o'zgarish o'nlab testni sindiradigan bog'liqlik markaziga aylanadi - Mother'ni bounded context bo'yicha bo'lib yuboring. Mother qaytargan obyektni testda mutate qilish boshqa testlarga ta'sir qilmasligi uchun har chaqiruvda yangi instance qaytarilishiga ishonch hosil qiling.

## 23.7 Fixture (yangi va umumiy - Fixture: fresh vs shared)

**Tavsif:** Fixture - test bajarilishidan oldin kerak bo'ladigan boshlang'ich holat (obyektlar, DB yozuvlari, fayllar). Fresh fixture har test uchun noldan qayta yaratiladi: to'liq izolyatsiya, deterministik natija, lekin sekinroq. Shared fixture bir marta yaratilib ko'p testda qayta ishlatiladi: tez, ammo testlar orasida bog'liqlik va ishga tushish tartibiga sezgirlik xavfi bor. Arxitektorning vazifasi - qimmat resurslarni (DB container) share qilib, ma'lumot holatini fresh saqlash.

**Spring'da qayerda uchraydi:** JUnit 5 `@BeforeEach`/`@AfterEach` (fresh) va `@BeforeAll`/`@AfterAll` + `@TestInstance(PER_CLASS)` (shared); `@DirtiesContext` context'ni majburan yangilaydi. Spring TestContext Framework transaction'ni har testdan keyin rollback qiladi (`@Transactional` test metodida, `@Rollback(false)` bilan o'zgartiriladi) - bu DB uchun eng arzon fresh-fixture mexanizmi. `@Sql`, `@SqlGroup`, `@SqlMergeMode` skriptlar bilan; Testcontainers'da `static` container (shared) vs instance container (fresh), `@ServiceConnection` esa ulanishni avtomatik ulaydi.

**Qo'llanish keyslari:**
- PostgreSQL container'ni `static` qilib butun suite uchun bir marta ko'tarish (shared infra).
- Har test metodini `@Transactional` bilan o'rab, DB holatini avtomatik rollback qilish (fresh data).
- `@Sql("/reset.sql")` bilan testdan oldin jadvallarni tozalash.
- Kafka/Redis container'ni share qilib, har testda alohida topic/prefix ishlatish.
- Og'ir fayl yoki sertifikat yuklashni `@BeforeAll`ga ko'chirib, suite vaqtini qisqartirish.

**Ehtiyot bo'ling:** Shared fixture bilan testlar bir-biriga ko'rinmas bog'lanib qoladi - alohida yurganda o'tadi, suite'da sinadi (yoki teskarisi); JUnit 5'da random test tartibini (`junit.jupiter.testmethod.order.default`) yoqib tekshirib ko'ring. `@Transactional` rollback'i `TransactionTemplate` yoki yangi thread'da (async, `@Async`) bajarilgan yozuvlarni qaytarmaydi - bu yashirin flakiness manbai.

## 23.8 Parametrlangan testlar (Parameterized Tests)

**Tavsif:** Bir xil test logikasini turli input to'plamlari bilan qayta-qayta bajarish mexanizmi: copy-paste qilingan o'nlab deyarli bir xil test metodi o'rniga bitta metod va ma'lumot manbasi. Har bir parametr to'plami alohida test sifatida hisoblanadi, shuning uchun sinish aniq qaysi input'da bo'lganini ko'rsatadi. Ekvivalentlik sinflari va chegara qiymatlarini (boundary values) tizimli qoplash uchun ideal.

**Spring'da qayerda uchraydi:** JUnit 5 `@ParameterizedTest` + manbalar: `@ValueSource`, `@CsvSource`, `@CsvFileSource`, `@EnumSource`, `@MethodSource`, `@ArgumentsSource`, `@FieldSource` (JUnit 5.11+); `@ParameterizedClass` (JUnit 5.13+) butun sinfni parametrlaydi. `@DisplayName` va `name = "{0} → {1}"` bilan o'qiladigan nom beriladi. Spring context bilan birga ishlaydi - `@ParameterizedTest`ni `@SpringBootTest`/`@WebMvcTest` ichida ishlatish mumkin, Spring'ning argument resolver'lari bilan mos keladi.

**Qo'llanish keyslari:**
- Soliq hisoblashni 20 xil mamlakat kodi va summa juftligi bilan `@CsvSource` orqali tekshirish.
- Validatsiya qoidalarini chegara qiymatlarida (0, 1, max, max+1) `@ValueSource` bilan sinash.
- Barcha `OrderStatus` enum qiymatlari uchun o'tish (transition) qoidasini `@EnumSource` bilan qoplash.
- Katta CSV faylidagi real production namunalarini `@CsvFileSource` bilan regression suite sifatida yurgizish.
- `@MethodSource` orqali murakkab domain obyektlari to'plamini Test Data Builder bilan generatsiya qilish.

**Ehtiyot bo'ling:** `@CsvSource`da o'nlab ustun paydo bo'lsa test o'qilmaydigan bo'lib qoladi - bu holda `@MethodSource` + record yoki builder afzal. Parametrlar ichiga kutilgan natijani hisoblovchi logika yozib qo'yish testni implementatsiyaning nusxasiga aylantiradi va xatolikni ikkala joyda takrorlaydi.

## 23.9 Xususiyatga asoslangan testlash (Property-Based Testing - jqwik)

**Tavsif:** Aniq input/output juftliklari o'rniga kodning barcha inputlar uchun to'g'ri bo'lishi kerak bo'lgan xususiyatini (invariant) e'lon qilish: framework yuzlab-minglab random input generatsiya qilib uni buzishga urinadi. Sinish topilganda avtomatik "shrinking" ishlaydi - minimal buzuvchi misolga qisqartiradi, bu debug qilishni ancha osonlashtiradi. Eng kuchli joyi - serializatsiya round-trip, sorting, parsing, pul arifmetikasi va state machine'lar.

**Spring'da qayerda uchraydi:** `net.jqwik:jqwik` (JUnit 5 Platform engine) - `@Property`, `@ForAll`, `@Provide`, `Arbitraries`, `@StatisticsReport`, `Combinators`; shuningdek `jqwik-spring` moduli Spring context'ni (`@JqwikSpringSupport` bilan `@SpringBootTest`) ulashga imkon beradi. Alternativalar: `QuickTheories`, `vavr-test`. jqwik o'z engine'ini ishlatganligi uchun Gradle/Maven'da `useJUnitPlatform()` sozlangan bo'lishi shart.

```java
@Property
void jsonRoundTripPreservesOrder(@ForAll("orders") Order order) throws Exception {
    String json = objectMapper.writeValueAsString(order);
    assertThat(objectMapper.readValue(json, Order.class)).isEqualTo(order);
}
```

**Qo'llanish keyslari:**
- Jackson serialize → deserialize round-trip invariantini barcha DTO'lar uchun tekshirish.
- Pul/valyuta konvertatsiyasida yig'indi va yaxlitlash invariantlarini (`sum(parts) == total`) sinash.
- Custom parser (IBAN, telefon raqami, CSV) uchun hech qachon unchecked exception otmasligini kafolatlash.
- Order state machine'da ruxsat etilmagan o'tishlar hech qanday ketma-ketlikda yuz bermasligini tasdiqlash.
- Sorting/comparator implementatsiyasining tranzitivlik va antisimmetriya shartlarini tekshirish.

**Ehtiyot bo'ling:** Property testlar sekin va CI'da vaqti-vaqti bilan yangi counterexample topib "flaky" ko'rinadi - `@Property(tries = ...)` va fixed seed bilan boshqarish, hamda ularni alohida CI bosqichiga chiqarish kerak. Agar xususiyatni ifodalash uchun implementatsiyani qaytadan yozishga to'g'ri kelsa, bu pattern mos kelmaydi.

## 23.10 Mutatsion testlash (Mutation Testing - PIT)

**Tavsif:** Test suite'ning haqiqiy sifatini o'lchash usuli: tool production bytecode'ga kichik "mutatsiyalar" kiritadi (`>` ni `>=` ga almashtirish, return qiymatini o'zgartirish, shartni inkor qilish) va testlarni yurgizadi. Agar testlar sinsa - mutant "o'ldirildi" (yaxshi), agar o'tsa - mutant tirik qoldi, ya'ni o'sha kod yo'li hech qanday real tasdiq bilan qo'riqlanmagan. Bu line coverage'dan ancha ishonchli metrika, chunki "kod bajarildi" bilan "kod tekshirildi" farqini ko'rsatadi.

**Spring'da qayerda uchraydi:** PIT (`pitest-maven` yoki Gradle plugin) odatda faqat domain va service paketlariga qaratiladi, `@Configuration` va entity'lar chiqarib tashlanadi. Maven va Gradle sozlamasi, `mutationThreshold` va mutator to'plamlari SonarQube hujjatidagi [PIT ni Maven va Gradle da ishga tushirish](../sonarqube/20-mutation-testing-100-coverage-qachon-yolgon.md#205-pit-pitest-ni-maven-va-gradle-da-ishga-tushirish) mavzusida.

**Qo'llanish keyslari:**
- Narx hisoblash yoki chegirma domain paketida test sifatini obyektiv o'lchash.
- CI'da `mutationThreshold`ni belgilab, critical modulda test sifatining pasayishini bloklash.
- 95% line coverage'ga ega, ammo assert'siz "smoke" testlarni fosh qilish.
- Legacy modulni refactoring qilishdan oldin mavjud testlar yetarliligini tekshirish.
- Code review'da "bu test nimani himoya qiladi?" savoliga faktik javob olish.

**Ehtiyot bo'ling:** Mutation testing qimmat (suite yuzlab marta yuradi): butun codebase uchun har PR'da emas, tanlangan paketlar uchun va nightly build'da yurgiziladi. Spring context ko'taradigan integration testlar timeout va "false survivor" beradi. Vaqtni qisqartirish usullari: [mutation testing narxi va uni qisqartirish](../sonarqube/20-mutation-testing-100-coverage-qachon-yolgon.md#208-mutation-testing-narxi-vaqt-va-uni-qisqartirish-usullari).

## 23.11 Test bo'laklari (Test Slices - @WebMvcTest, @DataJpaTest, @JsonTest, @RestClientTest)

**Tavsif:** Spring Boot'ning qisman (sliced) context yuklash mexanizmi: to'liq application context o'rniga faqat testga kerakli infrastruktura qatlami ko'tariladi. Har bir slice annotatsiyasi `@AutoConfigureX` to'plamini va component filtrini (`TypeExcludeFilter`) belgilaydi, natijada context sekundlar emas, millisekundlarda ko'tariladi va xatolar aniq qatlamda lokallashadi. Bu piramidaning "integration" qatlami uchun eng samarali vositadir.

**Spring'da qayerda uchraydi:** `@WebMvcTest` (`MockMvc` / `MockMvcTester` Boot 3.4+, faqat `@Controller`, `@ControllerAdvice`, `WebMvcConfigurer`, `Converter`; service'lar mock qilinishi kerak), `@WebFluxTest` (`WebTestClient`), `@DataJpaTest` (embedded DB + `TestEntityManager` + avtomatik `@Transactional` rollback), `@DataJdbcTest`, `@DataMongoTest`, `@JdbcTest`, `@JsonTest` (`JacksonTester`, `JsonContentAssert`), `@RestClientTest` (`MockRestServiceServer` bilan `RestClient`/`RestTemplate` adapterlarini test qiladi). `@AutoConfigureTestDatabase(replace = NONE)` real DB (Testcontainers) bilan ishlashga imkon beradi.

**Qo'llanish keyslari:**
- Controller'ning validatsiya, status kod va JSON mapping xatti-harakatini `@WebMvcTest` + `MockMvcTester` bilan tekshirish.
- Custom JPQL/native query va `@EntityGraph` ishlashini `@DataJpaTest` + Testcontainers Postgres'da tasdiqlash.
- `@JsonTest` bilan DTO serializatsiyasi, `@JsonFormat` sanalar va `@JsonView` qoidalarini qulflash.
- `@RestClientTest` bilan tashqi API adapter'ining retry va error mapping logikasini stub javoblar ustida sinash.
- Spring Security filterlarini `@WebMvcTest` + `spring-security-test` (`@WithMockUser`, `SecurityMockMvcRequestPostProcessors`) bilan tekshirish.

**Ehtiyot bo'ling:** `@WebMvcTest`da real servis bean'i yuklanmaydi - uni `@MockitoBean` bilan ta'minlash kerak, aks holda context ishga tushmaydi; bu esa controller va servis orasidagi real integratsiya tekshirilmasligini bildiradi. `@DataJpaTest`ning default embedded H2'si production Postgres'dan sintaksis va tip jihatidan farq qiladi - shuning uchun schema/query testlarini real DB container'da yurgizish zarur.

## 23.12 @SpringBootTest va context keshlash (@SpringBootTest & context caching)

**Tavsif:** `@SpringBootTest` to'liq application context'ni ko'taradi va eng realistik, ammo eng qimmat test turini beradi. Spring TestContext Framework context'larni **kontekst kaliti** (context key) bo'yicha keshlaydi: konfiguratsiya sinflari, aktiv profillar, property'lar, `ContextCustomizer`'lar va mock bean'lar to'plami birgalikda kalitni tashkil qiladi. Bir xil kalitli barcha testlar bitta context'ni qayta ishlatadi; har bir unikal kombinatsiya esa yangi context'ni ko'taradi va JVM xotirasida saqlanadi.

**Spring'da qayerda uchraydi:** `@SpringBootTest(webEnvironment = MOCK | RANDOM_PORT | DEFINED_PORT | NONE)`, `@ActiveProfiles`, `@TestPropertySource`, `properties = {...}`, `@ContextConfiguration`, `@Import`, `@TestConfiguration`, `@DirtiesContext`. Kesh hajmi `spring.test.context.cache.maxSize` (default 32) bilan boshqariladi, LRU evict qiladi. Diagnostika uchun `logging.level.org.springframework.test.context.cache=DEBUG`. Boot 3.1+ `@ServiceConnection` va `spring-boot-testcontainers` container'larni bir marta ulashga yordam beradi; `@TestConfiguration`li base test sinfi barcha testlar uchun bitta kalitni ta'minlaydi.

**Qo'llanish keyslari:**
- Butun oqimni (HTTP → service → DB → event) `RANDOM_PORT` + `RestTestClient` bilan end-to-end tekshirish.
- Bean wiring, `@ConditionalOnProperty` va auto-configuration to'g'ri ishlashini tasdiqlovchi "context loads" testi.
- Abstract `AbstractIntegrationTest` base sinfi orqali barcha integration testlarni bitta keshlangan context'ga yig'ish.
- `properties = "feature.x.enabled=true"` bilan feature flag'ning ikkala holatini tekshirish (ongli ravishda ikkinchi context).
- Scheduler, listener va `ApplicationEvent` zanjirlarini real context'da sinash.

**Ehtiyot bo'ling:** Har bir test sinfida turlicha `properties`/`@ActiveProfiles`/mock bean to'plami yozish o'nlab context yaratadi - build vaqti bir necha barobar oshadi va `OutOfMemoryError` ehtimoli paydo bo'ladi; konfiguratsiya variantlarini minimal to'plamga standartlashtirish arxitektorning vazifasi. `@DirtiesContext` keshni buzadi, shuning uchun uni faqat context holatini qaytarib bo'lmaydigan hollarda, ideal holda test sinfining eng oxirgi metodida ishlatish kerak.

## 23.13 @MockitoBean / @MockitoSpyBean

**Tavsif:** Spring context ichidagi bean'ni Mockito mock yoki spy bilan almashtirish mexanizmi: tashqi bog'liqliklarni (to'lov API, message broker, sekin servis) real context'da neytrallashtirish uchun ishlatiladi. `@MockitoBean` bean'ni to'liq mock bilan almashtiradi (yoki yo'q bo'lsa yangisini qo'shadi), `@MockitoSpyBean` esa real bean'ni spy bilan o'raydi va faqat kerakli metodni stub qilishga imkon beradi. Spring Framework 6.2'dan boshlab bular Boot'dan Framework'ga ko'chdi va eski `@MockBean`/`@SpyBean` deprecated qilindi.

**Spring'da qayerda uchraydi:** `org.springframework.test.context.bean.override.mockito.MockitoBean` va `MockitoSpyBean` (Spring Framework 6.2+ / Spring Boot 3.4-3.5, Boot 4 da ham); eski nomlar - `org.springframework.boot.test.mock.mockito.MockBean`/`@SpyBean` (Boot 3.4'da deprecated, Boot 4 da olib tashlangan). Shu bean-override oilasiga `@TestBean` (static factory metod bilan almashtirish) ham kiradi. Parametrlar: `name`, `contextName`, `reset = MockReset.AFTER`, `enforceOverride`. `@MockitoBean` field'ni `@Nested` sinflarda ham meros qiladi.

**Qo'llanish keyslari:**
- `@WebMvcTest`da controller testi uchun service qatlamini `@MockitoBean` bilan ta'minlash.
- Tashqi to'lov provayderi client'ini mock qilib, timeout va "declined" ssenariylarini imitatsiya qilish.
- `@MockitoSpyBean` bilan real repository'ni saqlab, faqat bitta og'ir aggregation metodini stub qilish.
- Email/SMS notifikatsiya bean'ini mock qilib, integration testda real xabar yuborilmasligini kafolatlash.
- `verify()` orqali real oqimda audit yoki event publisher chaqirilganini tasdiqlash.

**Ehtiyot bo'ling:** Har xil `@MockitoBean` to'plami alohida context kalitini yaratadi - mock'larni test sinflari bo'ylab tarqatish context kesh portlashiga olib keladi; umumiy mock'larni base sinfga yoki `@TestConfiguration`ga chiqarish afzal. Mock holati testlar orasida oqib ketmasligi uchun `MockReset` semantikasiga ishonch hosil qiling, va to'liq `@SpringBootTest`da yarim-mock'langan tizimni test qilish "yashil, lekin ma'nosiz" natija berishi mumkin - bu holda slice test yoki real Testcontainers afzal.

## 23.14 Test konfiguratsiyasi (@TestConfiguration)

**Tavsif:** Test uchun qo'shimcha yoki o'rnini bosuvchi bean'larni asosiy production konfiguratsiyasiga tegmasdan e'lon qilish imkonini beradi. `@TestConfiguration` - bu `@Configuration`ning maxsus ko'rinishi: u `@ComponentScan` tomonidan avtomatik olinmaydi, shuning uchun tasodifan production context'ga tushib qolmaydi. Agar test sinfi ichida static nested class sifatida yozilsa, faqat o'sha test sinfiga qo'llanadi; alohida top-level sinf bo'lsa, `@Import` bilan tanlab ulanadi. Shu bilan context cache'ni buzmasdan, nozik nuqtalarni (clock, random, tashqi client) nazorat ostiga olasiz.

**Spring'da qayerda uchraydi:** `org.springframework.boot.test.context.TestConfiguration` (Spring Boot 3.x/4.x), `@Import(MyTestConfig.class)`, `@ContextConfiguration`. Odatda `@Bean` bilan birga `@Primary` yoki Spring Framework 6.2+ dagi `@TestBean`/`@MockitoBean`/`@MockitoSpyBean` (Spring Boot 3.4-3.5 va Boot 4 da eski `@MockBean` o'rniga) ishlatiladi. Testcontainers konfiguratsiyasi ham ko'pincha `@TestConfiguration(proxyBeanMethods = false)` ichida `@Bean @ServiceConnection` ko'rinishida saqlanadi. `@Profile("test")` yoki `@ConditionalOnMissingBean` bilan birga ham keladi; `src/test/java` ichidagi `TestcontainersConfiguration` - Spring Boot'ning o'z generatsiya qiladigan namunasi.

**Qo'llanish keyslari:**
- Vaqtga bog'liq logikani test qilish uchun `Clock.fixed(...)` bean'ini test context'iga joylash.
- Tashqi to'lov provayderining Feign/`RestClient` client'ini WireMock'ga qaratilgan stub bean bilan almashtirish.
- Bir nechta integration test sinflari uchun umumiy Testcontainers bean'larini bitta joyda saqlash va `@Import` qilish.
- Kafka yoki RabbitMQ listener'larini o'chirib, o'rniga in-memory `ApplicationEventPublisher` asosidagi sinov bean'ini qo'yish.
- Integration testlarda security filter chain'ini yengillashtirilgan `SecurityFilterChain` bean'i bilan qoplash.

**Ehtiyot bo'ling:** Har bir test sinfiga o'ziga xos `@TestConfiguration`/`@MockitoBean` kombinatsiyasi qo'shilsa, Spring'ning context cache kaliti o'zgaradi va suite'da o'nlab ApplicationContext ko'tariladi - test vaqti keskin oshadi. Shuningdek, production bean'larini ko'p qoplash testni "yashil, lekin ma'nosiz" holatga olib keladi: haqiqiy konfiguratsiya xatolari testdan o'tib ketadi.

## 23.15 Testcontainers va servis ulanishi (Testcontainers & @ServiceConnection)

**Tavsif:** Testcontainers testlarni haqiqiy PostgreSQL, Kafka, Redis yoki Kibana kabi servislarning Docker konteynerlariga qarshi ishga tushiradi, ya'ni production'dagi bilan bir xil texnologiyada tekshiradi. `@ServiceConnection` esa konteyner bean'idan `jdbcUrl`, `bootstrapServers` kabi ulanish ma'lumotlarini avtomatik olib, Spring Boot'ning auto-configuration'iga uzatadi - qo'lda `@DynamicPropertySource` yozish shart emas. Natijada test setup'i qisqaradi va konteyner turlari o'zgarganda property nomlarini qayta yozish zaruriyati yo'qoladi.

**Spring'da qayerda uchraydi:** `spring-boot-testcontainers` moduli, `org.springframework.boot.testcontainers.service.connection.ServiceConnection` (Spring Boot 3.1+), `@Testcontainers`/`@Container` (JUnit 5 kengaytmasi), `@ImportTestcontainers`, hamda `ConnectionDetails` abstraksiyasi (`JdbcConnectionDetails`, `KafkaConnectionDetails`, `R2dbcConnectionDetails`). Local development uchun `SpringApplication.from(App::main).with(TestcontainersConfiguration.class).run(args)` qo'llaniladi. Eski uslub - `@DynamicPropertySource` bilan `registry.add("spring.datasource.url", container::getJdbcUrl)` - hali ham qo'llab-quvvatlanadi. Spring Boot 3.4+ da `@ServiceConnection`ni `@TestBean`siz, oddiy `@Bean` sifatida e'lon qilish keng tarqalgan.

```java
@TestConfiguration(proxyBeanMethods = false)
class ContainersConfig {
  @Bean
  @ServiceConnection
  PostgreSQLContainer<?> postgres() {
    return new PostgreSQLContainer<>("postgres:16-alpine");
  }
}
```

**Qo'llanish keyslari:**
- Flyway yoki Liquibase migratsiyalarini haqiqiy PostgreSQL versiyasida tekshirish.
- Kafka consumer/producer oqimini real broker bilan end-to-end sinash.
- Redis cache eviction va TTL xatti-harakatini production image'da tasdiqlash.
- `jsonb`, `ltree`, window function yoki native query'larga tayanadigan repository'larni test qilish.
- CI'da bir xil, takrorlanadigan ma'lumotlar bazasi muhitini ta'minlash (developer mashinasiga bog'liqlikni yo'qotish).

**Ehtiyot bo'ling:** Har test sinfida yangi konteyner ko'tarish suite'ni daqiqalarga cho'zadi - konteynerni `static` qiling yoki singleton pattern/`withReuse(true)` va `testcontainers.reuse.enable` bilan qayta ishlatish. CI agentlarida Docker mavjudligi va image'larni tortib olish limitlari (Docker Hub rate limit) muhim shart; shuningdek konteyner image tegini `latest` qoldirmang, aks holda testlar bir kechada "o'z-o'zidan" sinadi.

Mavzuning to'liq yozuvi testlash qo'llanmasidagi [Testcontainers bilan real infratuzilmada test](../testing/08-testcontainers-bilan-real-infratuzilmada.md#82-testcontainers-asoslari-docker-api-ustida-hayot-aylanishi) bo'limida; bu yerda faqat pattern katalogi nuqtai nazari.

## 23.16 Embedded DB mos kelmasligi (Embedded DB Mismatch - anti-pattern: H2 for PostgreSQL)

**Tavsif:** Bu anti-pattern'da production PostgreSQL/Oracle/MySQL'da ishlaydi, testlar esa tezlik uchun H2 yoki HSQLDB'da yuritiladi. H2'ning PostgreSQL compatibility mode'i faqat SQL sintaksisining bir qismini qoplaydi: `jsonb`, partial index, `ON CONFLICT`, recursive CTE nuanslari, `SELECT ... FOR UPDATE SKIP LOCKED`, timezone va collation xatti-harakati farq qiladi. Natijada testlar yashil, production esa sinadi - yoki aksincha, production'da to'g'ri ishlaydigan migratsiya testda tushadi. To'g'ri yechim - Testcontainers bilan haqiqiy engine'da test qilish.

**Spring'da qayerda uchraydi:** Spring Boot `@DataJpaTest` default holatda `@AutoConfigureTestDatabase(replace = Replace.ANY)` qo'llab, DataSource'ni embedded baza bilan almashtiradi - shuning uchun `@AutoConfigureTestDatabase(replace = Replace.NONE)` ko'p hollarda majburiy bo'ladi. Boshqa belgilar: `spring.jpa.database-platform=org.hibernate.dialect.H2Dialect` test profilida, `spring.jpa.hibernate.ddl-auto=create-drop` bilan Flyway/Liquibase migratsiyalarini butunlay chetlab o'tish, `src/test/resources/application-test.properties` ichidagi `jdbc:h2:mem:testdb;MODE=PostgreSQL`. `@JdbcTest`, `@DataR2dbcTest` ham xuddi shunday almashtirishni bajaradi.

**Qo'llanish keyslari:**
- Legacy loyihada H2 testlari borligini aniqlab, repository testlarini bosqichma-bosqich Testcontainers'ga ko'chirish.
- Migratsiya pipeline'ini (Flyway) faqat haqiqiy engine'da tekshiradigan alohida test qatlamini ajratish.
- `ddl-auto` bilan yaratilgan schema va migratsiya schema'si o'rtasidagi tafovutni ochib beruvchi schema-diff testini qo'shish.
- Native query va database-specific funksiyalarga bog'liq modullarni H2'dan butunlay chiqarib tashlash.
- Tez unit test qatlami uchun H2'ni faqat domain-neutral, oddiy CRUD joylarda ataylab qoldirish qarori va uni hujjatlashtirish.

**Ehtiyot bo'ling:** "H2 tezroq" argumenti vaqtni emas, ishonchni tejamaydi: topilmagan bug'lar production incident'ga aylanadi. Agar H2 saqlanadigan bo'lsa, buni ongli qaror sifatida yozib qo'ying va albatta haqiqiy bazadagi kamida bitta "smoke" integration test qatlamini saqlang.

## 23.17 Kontrakt testlash (Contract Testing)

**Tavsif:** Kontrakt testlash iste'molchi (consumer) va provayder (provider) o'rtasidagi API shartnomasini mashina o'qiy oladigan artefakt sifatida rasmiylashtiradi va ikki tomonni ham shu artefaktga qarshi tekshiradi. Bu og'ir, sekin va mo'rt end-to-end testlarni almashtirib, "men o'zgartirdim - kimning integratsiyasi sindi?" savoliga CI'da darhol javob beradi. Kontrakt bir marta yoziladi, lekin ikki marta ishlatiladi: provayder uchun test generatsiya qilish va consumer uchun stub yasash.

**Spring'da qayerda uchraydi:** Spring Cloud Contract (`spring-cloud-starter-contract-verifier`, `spring-cloud-starter-contract-stub-runner`) Groovy DSL yoki YAML kontraktlaridan Maven/Gradle plugin orqali provayder testlarini generatsiya qiladi va WireMock stub'larini artifact repository'ga `stubs` classifier bilan joylaydi. Pact JVM tomonida `au.com.dius.pact` kutubxonalari, `@ExtendWith(PactConsumerTestExt.class)`, `@Pact`, `@PactTestFor`, provayder tomonda `@Provider`, `@PactBroker` va `PactVerificationInvocationContextProvider`. HTTP bo'lmagan kanallar uchun Spring Cloud Contract'da messaging kontraktlari (`@AutoConfigureMessageVerifier`, Spring Cloud Stream/Kafka binder) mavjud.

**Qo'llanish keyslari:**
- Mikroservislar o'rtasida REST API'ni buzadigan o'zgarishni (breaking change) merge'dan oldin aniqlash.
- Mobil/frontend jamoasi kutgan JSON strukturasini backend relizidan oldin kafolatlash.
- Kafka event schema'sining consumer kutganiga mosligini tekshirish.
- Provayder jamoasiga qaysi maydonlar haqiqatda ishlatilayotganini ko'rsatib, dead field'larni xavfsiz olib tashlash.
- Monolitdan ajratilgan yangi servis uchun API'ni "contract-first" rejimida loyihalash.

**Ehtiyot bo'ling:** Kontrakt test biznes mantiqni emas, faqat interfeys shaklini va kelishilgan ssenariylarni tekshiradi - uni integration test o'rnida ishlatish xato. Kontrakt fayllari va stub versiyalarini boshqarish jiddiy intizom talab qiladi: eskirgan stub'lar bilan ishlayotgan consumer testlari yolg'on ishonch beradi, shuning uchun `stubsMode` va versiyalash siyosatini aniq belgilang.

## 23.18 Servis komponent testi (Service Component Test)

**Tavsif:** Komponent testi bitta servisni to'liq, lekin izolyatsiyada ishga tushiradi: uning o'z HTTP qatlami, service qatlami va ma'lumotlar bazasi haqiqiy, barcha tashqi servislar esa stub yoki konteyner bilan almashtirilgan. Bu end-to-end testdan ko'ra ancha barqaror va tez, ammo unit testdan ko'ra ko'proq xatolarni (serialization, validation, transaction, security filter) ushlaydi. Microservices arxitekturasidagi test piramidasining o'rta-yuqori qatlami shu.

**Spring'da qayerda uchraydi:** `@SpringBootTest(webEnvironment = WebEnvironment.RANDOM_PORT)` + `TestRestTemplate` yoki `RestClient`/`WebTestClient`, `@LocalServerPort`. Tashqi HTTP bog'liqliklari uchun WireMock (`wiremock-standalone`, Spring Cloud Contract WireMock'ning `@AutoConfigureWireMock`) yoki Spring Framework'ning `MockRestServiceServer` (`@RestClientTest`). Ma'lumotlar bazasi va broker uchun Testcontainers `@ServiceConnection`. Fokuslangan "slice" variantlari: `@WebMvcTest`, `@WebFluxTest`, `@DataJpaTest`, `@JsonTest`, `@RestClientTest`. Spring Modulith'da bitta modulni shu uslubda sinash uchun `@ApplicationModuleTest` bor.

**Qo'llanish keyslari:**
- Buyurtma yaratish oqimini HTTP so'rovdan baza yozuviga qadar bitta testda tekshirish.
- Spring Security konfiguratsiyasini (role, JWT scope) haqiqiy filter chain bilan sinash.
- `@Transactional` chegaralari va rollback xatti-harakatini real baza ustida tasdiqlash.
- Validation xatolarida qaytadigan `ProblemDetail` (RFC 9457) javob formatini qotirib qo'yish.
- Tashqi servis 500 yoki timeout qaytarganda resilience (retry, circuit breaker) xatti-harakatini WireMock orqali tekshirish.

**Ehtiyot bo'ling:** Bu testlar sekin, shuning uchun ularni soni bilan emas, qamrovi bilan tanlang va context cache'ni buzmaslik uchun konfiguratsiyani bir xil saqlang (ortiqcha `@MockitoBean`, `properties = {...}` har xilligi yangi context yaratadi). Shuningdek, komponent testini asta-sekin "hammasi haqiqiy" end-to-end testiga aylantirib yubormang - tashqi chegara stub bo'lib qolishi kerak.

## 23.19 Servis integratsiya kontrakti testi (Service Integration Contract Test)

**Tavsif:** Bu - kontrakt testining provayder tomonidagi ko'rinishi: servis o'zi e'lon qilgan (yoki consumer'lar talab qilgan) kontraktlarga haqiqatda javob berishini tekshiradi. Kontrakt fayllaridan avtomatik testlar generatsiya qilinadi va ular servisning real controller'lariga, oldindan tayyorlangan holat (provider state) bilan murojaat qiladi. Shu bilan consumer'larni CI'ga ulamasdan, ularning kutgan xulqini buzmaslik kafolatlanadi.

**Spring'da qayerda uchraydi:** Spring Cloud Contract Verifier plugin'i `src/test/resources/contracts` ichidagi DSL'dan JUnit 5 testlarini generatsiya qiladi; test'lar `baseClassForTests` (yoki `packageWithBaseClasses`) orqali ko'rsatilgan base sinfdan meros oladi, bu sinf odatda RestAssured MockMvc setup'ini (`RestAssuredMockMvc.standaloneSetup(...)`) yoki `@SpringBootTest` context'ini tayyorlaydi. Messaging kontraktlari uchun `@AutoConfigureMessageVerifier` va `ContractVerifierMessaging`. Pact uslubida: `@Provider("orders")`, `@PactBroker(url = ...)`, `@TestTemplate @ExtendWith(PactVerificationInvocationContextProvider.class)`, `@State("buyurtma mavjud")` metodlari holatni tayyorlaydi.

**Qo'llanish keyslari:**
- Consumer-driven kontraktlarni provayder CI pipeline'ida majburiy gate sifatida ishga tushirish.
- API maydonini o'zgartirishdan oldin qaysi consumer sinishini aniqlash (Pact Broker'dagi `can-i-deploy`).
- Event schema o'zgarishini Kafka producer tomonida kontraktga qarshi tekshirish.
- Provider state'larni test ma'lumotlari bilan to'ldirib, turli javob ssenariylarini qoplash.
- Stub artefaktlarini relizga qo'shib, boshqa jamoalarga ishonchli mock manba berish.

**Ehtiyot bo'ling:** Generatsiya qilingan testlarni qo'lda tahrirlash foydasiz - ular build vaqtida qayta yoziladi; o'zgartirish faqat kontrakt yoki base sinf orqali bo'ladi. Provider state'larni haqiqiy ma'lumotlar bazasi holatiga bog'lab tashlasangiz, testlar mo'rt bo'ladi va kontrakt testning tezlik ustunligi yo'qoladi.

## 23.20 Iste'molchi tomonidagi kontrakt testi (Consumer-Side Contract Test)

**Tavsif:** Iste'molchi o'z kodini provayderning haqiqiy instance'iga emas, kontraktdan yasalgan stub'ga qarshi tekshiradi. Shu tariqa client kodi (serialization, error handling, retry, DTO mapping) izolyatsiyada, tez va deterministik sinaladi; shu bilan birga, test o'tgani kontraktning amalda ishlatilayotganini ham tasdiqlaydi. Consumer-driven yondashuvda aynan bu test kontrakt faylini tug'diradi va provayderga uzatadi.

**Spring'da qayerda uchraydi:** Spring Cloud Contract Stub Runner: `@AutoConfigureStubRunner(ids = "com.example:orders-service:+:stubs:8090", stubsMode = StubRunnerProperties.StubsMode.LOCAL)` - stub'lar Maven repository yoki Git'dan olinadi va WireMock server'da ko'tariladi; `@StubRunnerPort` bilan portni olish mumkin. Pact tomonida: `@ExtendWith(PactConsumerTestExt.class)`, `@Pact(provider = "orders", consumer = "web-bff")` metodi `PactDslWithProvider` bilan kutilgan interaksiyani tavsiflaydi, `@PactTestFor(pactMethod = "...")` esa mock server'ni ishga tushiradi va natijada `target/pacts` ichiga pact fayli yoziladi. Client sifatida `RestClient`, `WebClient` yoki Spring Cloud OpenFeign ishlatiladi.

**Qo'llanish keyslari:**
- BFF yoki gateway servisining downstream client kodini provayder deploy bo'lmasdan test qilish.
- 404, 409 va 503 javoblarida client'ning fallback hamda Resilience4j retry logikasini tekshirish.
- DTO'dagi `@JsonProperty` nomlari va sana formatlari provayder javobiga mosligini qotirib qo'yish.
- Pact fayllarini broker'ga publish qilib, provayder jamoasiga rasmiy talab yuborish.
- Yangi integratsiyani provayder hali tayyor bo'lmagan paytda "contract-first" boshlash.

**Ehtiyot bo'ling:** `StubsMode.REMOTE` bilan ishlaganda CI tarmoq va repository mavjudligiga bog'lanib qoladi - flaky test manbasi shu. Eng katta xavf: consumer stub'ni o'zi xohlagandek yozib, provayderda hech kim tekshirmasa - bu "mock bilan o'zini aldash"; kontrakt albatta provayder tomonida verify qilinishi shart.

## 23.21 Arxitektura testlari (Architecture Tests - ArchUnit, Spring Modulith verify)

**Tavsif:** Arxitektura testlari qatlam chegaralari, paket bog'liqliklari, nomlash qoidalari va annotatsiya qo'llanishi kabi dizayn qoidalarini oddiy JUnit testi sifatida ijro etadi. Qoida kodda yozilgani uchun u hujjat bilan birga eskirmaydi: hech kim `domain` paketidan `web` paketiga import qo'shib qo'ya olmaydi - build darhol sinadi. Katta jamoalarda bu code review'dagi takrorlanuvchi, subyektiv bahslarni avtomatlashtiradi.

**Spring'da qayerda uchraydi:** ArchUnit (`com.tngtech.archunit:archunit-junit5`): `@AnalyzeClasses(packages = "com.example")`, `@ArchTest`, `ArchRuleDefinition.noClasses()/classes()`, `SlicesRuleDefinition.slices()...should().beFreeOfCycles()`, `FreezingArchRule.freeze(rule)` legacy qoidalarni bosqichma-bosqich tuzatish uchun. Spring Modulith (`spring-modulith-core`): `ApplicationModules.of(Application.class).verify()` modul chegaralarini va aylanaviy bog'liqliklarni tekshiradi, `new Documenter(modules).writeDocumentation()` esa C4/PlantUML diagrammalarini generatsiya qiladi; `@ApplicationModule(allowedDependencies = ...)` ruxsat berilgan bog'liqliklarni e'lon qiladi.

```java
@ArchTest
static final ArchRule domain_is_pure =
    noClasses().that().resideInAPackage("..domain..")
        .should().dependOnClassesThat()
        .resideInAnyPackage("..web..", "..infrastructure..");
```

**Qo'llanish keyslari:**
- Hexagonal/Clean arxitekturada domain qatlamining Spring yoki JPA annotatsiyalariga bog'lanmasligini kafolatlash.
- `@Transactional` faqat service qatlamida ishlatilishini majburlash.
- Paketlar orasidagi aylanaviy bog'liqliklarni (cyclic dependency) build'da bloklash.
- Spring Modulith modullari o'zaro faqat e'lon qilingan API orqali gaplashishini tekshirish.
- `field injection` yoki `System.out.println` kabi taqiqlangan amaliyotlarni avtomatik aniqlash.

**Ehtiyot bo'ling:** Haddan ziyod qattiq va mayda qoidalar refactoring'ni sekinlashtiradi - qoidalarni haqiqiy arxitektura qarorlari darajasida saqlang, stilistik narsalarni linter'ga qoldiring. Katta kod bazasida ArchUnit sinf skanerlashi sekin bo'lishi mumkin, shuning uchun paket qamrovini toraytiring va `freeze` bilan mavjud buzilishlarni baseline qiling.

Mavzuning to'liq yozuvi testlash qo'llanmasidagi [arxitektura testlari va kod sifati darvozalari](../testing/14-arxitektura-testlari-va-kod-sifati.md#142-archunit-asoslari) bo'limida; bu yerda faqat pattern katalogi nuqtai nazari.

## 23.22 Tasdiqlash / Golden Master testlash (Approval / Golden Master Testing)

**Tavsif:** Bu uslubda kutilgan natijani assert'lar bilan qo'lda yozmasdan, chiqish natijasini bir marta "tasdiqlangan" (approved) fayl sifatida saqlab qo'yasiz; keyingi har bir yurishda yangi natija shu golden master bilan baytlab solishtiriladi. Farq chiqsa, test tushadi va diff tool orqali o'zgarishni ko'rib, ataylab qilingan bo'lsa qayta tasdiqlaysiz. Bu, ayniqsa, katta va murakkab chiqish (hisobot, JSON, HTML, generatsiya qilingan kod) uchun yuzlab assert yozishdan ancha samarali.

**Spring'da qayerda uchraydi:** ApprovalTests kutubxonasi (`com.approvaltests:approvaltests`): `Approvals.verify(String)`, `Approvals.verifyJson(...)`, `Approvals.verifyAll(...)`, `@UseReporter(DiffReporter.class)`; natija `*.received.txt` va `*.approved.txt` fayllarida saqlanadi. Spring'da odatda `MockMvc` yoki `WebTestClient` javobining to'liq body'si tasdiqlanadi: `mockMvc.perform(get("/api/report")).andReturn().getResponse().getContentAsString()` natijasini `Approvals.verifyJson(...)` ga uzatish. JSON uchun `JSONAssert` (`org.skyscreamer`) yoki `JsonUnit`ning `assertThatJson(...)` moslashuvchan solishtirish beradi; `@JsonTest` bilan serialization natijasini ham shu yo'l bilan qotirish mumkin.

**Qo'llanish keyslari:**
- Katta PDF/CSV/Excel hisobot generatorining chiqishini regressiyadan himoya qilish.
- REST API javobining to'liq JSON strukturasini (versiyalash paytida) qotirib qo'yish.
- Thymeleaf yoki email shablonidan render bo'lgan HTML'ni tekshirish.
- `Documenter` yoki OpenAPI spec generatsiyasining natijasini kuzatish va ruxsatsiz o'zgarishni ushlash.
- Legacy hisob-kitob moduli (narx, soliq, jarima) natijalarini refactoring oldidan muzlatish.

**Ehtiyot bo'ling:** Chiqishda timestamp, UUID, tartibsiz map yoki mahalliylashtirish bo'lsa, test flaky bo'ladi - bunday maydonlarni scrubber bilan normallashtiring. Eng katta xavf - "tushdi, demak qayta tasdiqlayman" odati: diff'ni o'qimasdan approved faylni yangilash golden master'ni butunlay ma'nosiz qiladi.

## 23.23 Snapshot testlash (Snapshot Testing)

**Tavsif:** Snapshot testlash golden master'ning yengil, kod ichiga yaqin varianti: birinchi yurishda natija avtomatik yoziladi va keyingi yurishlarda shu snapshot bilan solishtiriladi. Odatda snapshot'lar bitta `.snap` faylida test metodi nomiga bog'lab saqlanadi, yangilash esa maxsus flag yoki property bilan amalga oshiriladi. Frontend dunyosidan kelgan bu uslub Java'da ham serialization, DTO mapping va event payload'lari uchun qulay.

**Spring'da qayerda uchraydi:** `java-snapshot-testing` (`au.com.origin:java-snapshot-testing-junit5`): `@ExtendWith(SnapshotExtension.class)`, test maydoni sifatida `private Expect expect;` va `expect.toMatchSnapshot(obj)`; snapshot'lar `src/test/java/.../__snapshots__/*.snap` ichida yotadi. Spring kontekstida ko'pincha `@JsonTest` bilan `JacksonTester`/`ObjectMapper` chiqishini, yoki `WebTestClient.expectBody(String.class)` natijasini snapshot qilinadi. Shunga yaqin natijani `JsonUnit`ning `assertThatJson(...).isEqualTo(...)` va `@AutoConfigureJsonTesters` bilan ham olish mumkin; ApprovalTests esa aynan shu maqsadning kattaroq, fayl asosidagi ko'rinishi.

**Qo'llanish keyslari:**
- DTO -> JSON serialization natijasini Jackson konfiguratsiyasi o'zgarganda nazorat qilish.
- Kafka/`ApplicationEvent` payload strukturasini consumer'larni buzmaslik uchun qotirish.
- MapStruct mapper natijalarini katta obyektlar uchun tez qoplash.
- GraphQL (Spring for GraphQL) so'rov javobining shaklini tekshirish.
- Xato javoblari (`ProblemDetail`) formatining barcha endpoint'larda bir xilligini ta'minlash.

**Ehtiyot bo'ling:** Snapshot'lar maqsadni emas, mavjud xulqni yozib oladi - xato xulq ham osongina "tasdiqlangan" bo'lib qolishi mumkin, shuning uchun birinchi snapshot'ni albatta review'dan o'tkazing. Juda katta snapshot'lar (minglab satr) diff'ni o'qishni imkonsiz qiladi: qamrovni kichik, mazmunli bo'laklarga bo'ling.

## 23.24 Xarakterizatsiya testlari (Characterization Tests)

**Tavsif:** Xarakterizatsiya testi (Michael Feathers atamasi) kodning *to'g'ri* xulqini emas, *hozirgi* xulqini yozib oladi. Maqsad - hujjatsiz, testsiz legacy modulni refactoring qilishdan oldin xavfsizlik to'ri yaratish: nima bo'layotganini aniqlab, uni test sifatida qotirib qo'yish. Keyin refactoring davomida bu testlar har bir xulq o'zgarishini signal qiladi; aniqlangan bug'lar alohida, ongli qarorlar bilan tuzatiladi.

**Spring'da qayerda uchraydi:** Amalda `@SpringBootTest` bilan to'liq context ko'tarib, mavjud service va controller'larni real baza (Testcontainers) ustida chaqirish, natijani ApprovalTests yoki snapshot bilan muzlatish. Qamrovdagi bo'shliqlarni JaCoCo (`jacoco-maven-plugin`) hisobotlari ko'rsatadi; `PITest` mutation testing esa testlar haqiqatda xulqni ushlayotganini tekshiradi. Legacy kodni testlanadigan holatga keltirishda Spring'ning `@MockitoBean`/`@MockitoSpyBean`, `ReflectionTestUtils.setField(...)`, `MockRestServiceServer` va `@DirtiesContext` yordam beradi; `AssertJ`ning `assertThat(...).usingRecursiveComparison()` katta obyektlarni solishtirishni osonlashtiradi.

**Qo'llanish keyslari:**
- 10 yillik, testsiz hisob-kitob moduli ustidan Spring Boot migratsiyasini boshlashdan oldin xulqni muzlatish.
- Monolitdan servis ajratishda eski va yangi implementatsiya natijalarini solishtirish.
- Hujjatsiz SQL-ga asoslangan hisobotni Spring Data'ga ko'chirishdan oldin natijalarni qayd qilish.
- Noma'lum biznes qoidalarni (maxsus holatlar, null xulqi) testlar orqali "kashf qilish" va jamoaga ko'rsatish.
- `strangler fig` yondashuvida eski yo'lni o'chirishdan oldin regressiya to'rini ta'minlash.

**Ehtiyot bo'ling:** Bu testlar bug'larni ham to'g'ri xulq sifatida qotirib qo'yadi - har bir shubhali natijani izohli `// FIXME: bu xulq noto'g'ri, lekin hozir mavjud` ko'rinishida belgilab qo'ying. Ular vaqtinchalik vosita: refactoring tugagach, ularning ko'pini maqsadga yo'naltirilgan, aniq assert'li testlar bilan almashtirish kerak, aks holda suite sekin va mo'rt bo'lib qoladi.

## 23.25 Kamtarin obyekt (Humble Object)

**Tavsif:** Agar logika test qilish qiyin bo'lgan muhitga (framework callback, UI, scheduler, message listener, HTTP controller) yopishib qolgan bo'lsa, Humble Object pattern uni ikkiga ajratadi: muhitga bog'langan qism iloji boricha "kamtarin" - hech qanday qaror qabul qilmaydigan, faqat delegatsiya qiladigan yupqa qatlam bo'ladi, butun mantiq esa oddiy, bog'liqliksiz POJO'ga ko'chiriladi. Natijada mantiqni ApplicationContext ko'tarmasdan, millisekundlarda unit test qilish mumkin bo'ladi. Pattern faqat UI yoki controller uchun emas: Martin uni har qanday arxitektura chegarasining belgisi deb qaraydi va servis chegarasini alohida ko'rsatadi. Chiqishda ilova ma'lumotni oddiy strukturaga yuklab, uni formatlab tashqi servisga yuboradigan modulga uzatadi; kirishda esa service listener servis interfeysidan ma'lumotni qabul qilib, uni ilova ishlatadigan oddiy strukturaga aylantiradi va shundan keyin chegaradan o'tkazadi. Chegaradan o'tadigan narsa deyarli har doim oddiy ma'lumot strukturasi bo'ladi, va chegara test qilish qiyin qismni test qilish oson qismdan ajratadi (Martin, *Clean Architecture*, Prentice Hall, 2018, 23-bob).

**Spring'da qayerda uchraydi:** `@RestController` metodlari faqat so'rovni DTO'ga aylantirib application service'ga uzatadi; `@Scheduled` yoki `@EventListener` metodi bir satrlik delegatsiya bo'ladi; `MessageListener`/`@KafkaListener`/`@RabbitListener` va Spring Batch'ning `ItemProcessor`/`ItemWriter` implementatsiyalari ham shu tarzda yupqalashtiriladi. Spring Integration'dagi `ServiceActivator` va Spring Modulith'ning `@ApplicationModuleListener` ham xuddi shu rolni bajaradi. Mantiq ajratilgandan keyin uni oddiy JUnit 5 + Mockito/AssertJ bilan, `@SpringBootTest`siz test qilasiz; kamtarin qatlam uchun esa yengil `@WebMvcTest` yoki `MockMvcTester` (Spring Framework 6.2+) yetarli.

**Qo'llanish keyslari:**
- Controller'dagi validation va narx hisoblash mantiqini alohida domain service'ga chiqarib, tez unit testlar yozish.
- `@Scheduled` job'ning jadval mantiqini (qaysi yozuvlar tanlanadi) vaqt va cron'dan ajratish.
- Kafka listener'dagi deserialization va biznes qarorini ikki sinfga bo'lib, retry/DLQ xulqini alohida tekshirish.
- Tashqi servisga ulanadigan adapterni ikkiga bo'lish: service listener faqat protokol va mapping, qaror esa application service da.
- Spring Batch step'ining transformatsiya mantiqini `JobLauncherTestUtils` ishga tushirmasdan sinash.
- Legacy JSF/Vaadin yoki Thymeleaf controller'dan mantiqni ko'chirib, UI'ga bog'liqlikni yo'qotish.

**Ehtiyot bo'ling:** Pattern yupqa qatlamni *testsiz qoldirish* uchun bahona emas: integration test bilan delegatsiya to'g'ri simlanganini, mapping va xato ishlovini albatta tekshirish kerak. Haddan ziyod qo'llash esa mayda, bir metodli sinflar ko'payishiga va kod navigatsiyasining qiyinlashishiga olib keladi.

## 23.26 Sahifa obyekti (Page Object)

**Tavsif:** Page Object UI avtomatlashtirishda har bir sahifa yoki komponentni alohida sinf sifatida modellashtiradi: selektorlar va past darajadagi o'zaro ta'sir shu sinf ichida yashiriladi, test esa faqat biznes tilidagi metodlarni (`loginAs(...)`, `addToCart(...)`) chaqiradi. Shu tufayli markup o'zgarganda o'nlab testni emas, bitta page object'ni tuzatasiz. Natijada UI testlari o'qilishi oson va ancha kam mo'rt bo'ladi.

**Spring'da qayerda uchraydi:** Selenium WebDriver (`@FindBy` + `PageFactory.initElements(driver, this)`), Selenide (`Selenide.page(LoginPage.class)`) yoki Playwright for Java (`com.microsoft.playwright`) bilan yoziladi. Spring Boot tomonida test `@SpringBootTest(webEnvironment = WebEnvironment.RANDOM_PORT)` va `@LocalServerPort` bilan haqiqiy server ko'taradi, brauzerni Testcontainers'ning `BrowserWebDriverContainer` yoki Selenium Grid beradi. Server ko'tarmasdan ishlashning Spring'ga xos yo'li ham bor: `spring-test`ning HtmlUnit integratsiyasi - `MockMvcHtmlUnitDriverBuilder.mockMvcSetup(mockMvc).build()` orqali `WebDriver` olib, xuddi shu page object'larni `MockMvc` ustida ishlatish mumkin.

**Qo'llanish keyslari:**
- Kritik foydalanuvchi oqimlarini (login, ro'yxatdan o'tish, to'lov) brauzerda smoke test qilish.
- Thymeleaf yoki server-side render qilingan admin panelni `MockMvcHtmlUnitDriverBuilder` bilan tez tekshirish.
- Bir xil navigatsiya va header komponentini barcha UI testlarida qayta ishlatish.
- Form validation xabarlarining lokalizatsiyasini sahifa darajasida tasdiqlash.
- CI'da Testcontainers brauzeri va video yozib olish bilan barqaror E2E qatlam qurish.

**Ehtiyot bo'ling:** UI testlari eng sekin va eng mo'rt qatlam - ularni o'nlab emas, bir nechta eng qimmatli oqim bilan cheklang va business mantiqni past qatlamlarda test qiling. `Thread.sleep` bilan kutishdan voz kechib, explicit wait yoki Selenide/Playwright'ning avtomatik kutishiga tayaning; page object ichiga assert'larni to'ldirib tashlamang - u harakatlarni beradi, tekshirish testda qoladi.

## 23.27 Servis stub (Service Stub)

**Tavsif:** Tashqi HTTP servisni (payment gateway, partner API, OAuth2 provider) real emas, balki boshqariladigan stub server bilan almashtiradi. Stub kutilgan so'rovga belgilangan javob qaytaradi, shu bilan test tashqi tizim ishlashiga, tarmoqqa va test ma'lumotlariga bog'liq bo'lmaydi. Mock object'dan farqi: bu haqiqiy socket ustida ishlaydi, shuning uchun HTTP client sozlamalari, serializatsiya, timeout va retry logikasi ham test qilinadi. Xato ssenariylarini (500, 429, sekin javob, buzilgan JSON) deterministik ko'rsatish mumkin.

**Spring'da qayerda uchraydi:** WireMock (`org.wiremock:wiremock-standalone`, JUnit 5 uchun `@WireMockTest`, yoki `WireMockServer` ni `@BeforeAll` da qo'lda ko'tarish) va MockServer (`org.mockserver.integration.ClientAndServer`). Spring Cloud Contract `spring-cloud-starter-contract-stub-runner` ichida `@AutoConfigureWireMock(port = 0)` va `@AutoConfigureStubRunner` beradi. Testcontainers'da `WireMockContainer` va `MockServerContainer` modullari bor. Stub port'ini ilovaga `@DynamicPropertySource` yoki Boot 3.4+ dagi `DynamicPropertyRegistrar` bean orqali uzatiladi; client tomonda `RestClient`, `WebClient` yoki `@HttpExchange` interfeysi `RestClientAdapter`/`WebClientAdapter` bilan sinovdan o'tadi.

**Qo'llanish keyslari:**
- To'lov provayderining 402 va 429 javoblarida retry va circuit breaker to'g'ri ishlashini tekshirish.
- `WebClient` timeout va `Retry.backoff` sozlamalarini `withFixedDelay(...)` stub bilan o'lchash.
- Partner API'ning realdagi JSON namunasini `__files` ichiga qo'yib, DTO deserializatsiyasini qotirib tekshirish.
- Keycloak/Auth0 JWKS endpoint'ini stub qilib, resource server token validatsiyasini offline sinash.
- CI'da tashqi sandbox ishlamay qolganda ham integratsiya testlari yashil qolishini kafolatlash.

**Ehtiyot bo'ling:** Stub real kontraktdan "uzilib" ketishi mumkin - shuning uchun stub'larni Spring Cloud Contract yoki provider tomonidan nashr etilgan OpenAPI/stub artifact'dan generatsiya qilish afzal, aks holda test yashil, prod qizil bo'ladi. `WireMockServer` ni fixed port'da global ko'tarish parallel test'larda port conflict va stub leak keltiradi; har test uchun `resetAll()` yoki dinamik port ishlatiling.

## 23.28 Ma'lumotlar bazasi holatini tayyorlash (Database State Setup)

**Tavsif:** Test boshlanishidagi DB holatini (schema + data) aniq, takrorlanadigan ko'rinishga keltirish patterni. Schema migration bilan (Flyway/Liquibase) prod bilan bir xil holga keltiriladi, test data esa deklarativ SQL script yoki fixture builder orqali qo'yiladi. Maqsad: har test o'z ma'lumotini o'zi yaratadi va testlar bir-birining holatiga tayanmaydi.

**Spring'da qayerda uchraydi:** `@Sql` (`org.springframework.test.context.jdbc.Sql`), `@SqlGroup`, `@SqlConfig(transactionMode = ISOLATED)`, `@SqlMergeMode(MERGE)` va executionPhase `BEFORE_TEST_METHOD`/`AFTER_TEST_METHOD` (Spring Framework 6.x'da `BEFORE_TEST_CLASS` ham bor). Programmatik tarafda `ResourceDatabasePopulator` va `ScriptUtils`. Flyway tomonida `spring.flyway.locations=classpath:db/migration,classpath:db/testdata` yoki `FlywayMigrationStrategy` bean; JPA uchun `spring.jpa.hibernate.ddl-auto=validate` bilan birga ishlatish tavsiya. `@DataJpaTest` + `TestEntityManager`, real DB uchun `@Testcontainers` + `@ServiceConnection` (Spring Boot 3.1+) va `@AutoConfigureTestDatabase(replace = NONE)`.

**Qo'llanish keyslari:**
- Reporting query'sini 20 qatorlik `@Sql("/sql/orders-fixture.sql")` bilan tekshirish.
- Flyway migration'ining o'zi (masalan kolonka backfill qiluvchi script) to'g'ri ishlashini real PostgreSQL container'da sinash.
- `AFTER_TEST_METHOD` script bilan sequence va audit jadvallarini tozalab, test izolatsiyasini ta'minlash.
- Legacy view yoki stored procedure'ga tayangan repository'ni H2 emas, prod engine'ida test qilish.
- Katta ma'lumotli pagination/`Sort` xatolarini realistik hajmdagi fixture'da ushlash.

**Ehtiyot bo'ling:** H2/HSQLDB'da yozilgan testlar PostgreSQL yoki Oracle dialect xatolarini yashiradi (`jsonb`, `ON CONFLICT`, window function, lock semantikasi) - integratsiya qatlamida Testcontainers ishlating. Umumiy "katta seed script"ni barcha testlarga ulash eng keng tarqalgan anti-pattern: test nima uchun o'tganini tushunib bo'lmaydi va bitta qator o'zgarsa o'nlab test sinadi.

## 23.29 Transactional test rollback tuzoqlari (Transactional Test Rollback Pitfalls)

**Tavsif:** `@Transactional` qo'yilgan test metodi oxirida Spring transaction'ni avtomatik rollback qiladi - bu tozalikni beradi, lekin prod semantikasidan chetga chiqaradi. Test va kod bitta transaction va bitta Hibernate persistence context ichida ishlaganidan ba'zi xatolar (flush bo'lmagani, constraint buzilgani, lazy loading, `AFTER_COMMIT` listener'lar) umuman ko'rinmaydi. Pattern shundan iborat: qachon rollback'ga tayanish, qachon real commit bilan test qilish kerakligini ongli tanlash.

**Spring'da qayerda uchraydi:** `@Transactional` test metodida, `@Rollback(false)` yoki `@Commit`, `TestTransaction` (`org.springframework.test.context.transaction.TestTransaction.flagForCommit()/end()/start()`), `@BeforeTransaction`/`@AfterTransaction`. `@DataJpaTest` default'da transactional; `TestEntityManager.flush()` va `entityManager.clear()` bilan majburiy sinxronlash kerak. `@SpringBootTest(webEnvironment = RANDOM_PORT)` + `TestRestTemplate`/`WebTestClient` holatida server boshqa thread'da ishlaydi, test transaction'i unga tarqalmaydi - rollback ham bo'lmaydi, shuning uchun tozalash qo'lda yoki Testcontainers'ni qayta ko'tarish bilan qilinadi.

**Qo'llanish keyslari:**
- Unique constraint buzilishini aniqlash uchun testda `flush()` chaqirib, `DataIntegrityViolationException` ni ushlash.
- `@TransactionalEventListener(phase = AFTER_COMMIT)` ishlashini tekshirishda `@Transactional` ni olib tashlab, real commit qilish.
- `LazyInitializationException` ni ushlash uchun servis testini transaction'dan tashqarida (web layer orqali) o'tkazish.
- `TestTransaction` bilan commit qilib, keyin yangi transaction'da haqiqatan saqlanganini o'qish.
- `@DataJpaTest` da `clear()` qilib, repository query'si DB'dan emas, cache'dan o'qiyotganini fosh qilish.

**Ehtiyot bo'ling:** Eng xatarli tuzoq - rollback'li test "o'tadi", prod'da esa constraint yoki `AFTER_COMMIT` logikasi sinadi; ikkinchisi - first-level cache tufayli `save()` dan keyin `findById()` hech qanday SQL yubormaydi va mapping xatosi yashiradi. `@Commit` ni ko'p ishlatsangiz testlar bir-biriga "iflos" ma'lumot qoldiradi, shuning uchun uni faqat atayin, tozalash strategiyasi bilan birga qo'llang.

## 23.30 Clock injection (Clock Injection)

**Tavsif:** `LocalDateTime.now()` yoki `System.currentTimeMillis()` ni kod ichida qattiq chaqirish o'rniga, vaqt manbasini `java.time.Clock` bean sifatida inject qilish. Testda uni `Clock.fixed(...)` yoki mutable clock bilan almashtirib, "muddat o'tdi", "oy oxiri", "29-fevral", "soat 00:00" kabi ssenariylarni deterministik o'ynatish mumkin. Bu `Thread.sleep()` ga va vaqtga bog'liq flaky test'larga ehtiyojni yo'q qiladi.

**Spring'da qayerda uchraydi:** `@Bean Clock systemClock() { return Clock.systemDefaultZone(); }` (yoki `systemUTC()`), kodda `LocalDate.now(clock)` / `Instant.now(clock)`; Java 17+ da yengilroq abstraksiya sifatida `java.time.InstantSource` ham mos. Testda `@TestConfiguration` orqali `Clock.fixed(Instant.parse("2024-02-29T10:15:30Z"), ZoneOffset.UTC)` beriladi yoki `@MockitoBean` (Spring Boot 3.4-3.5 va Boot 4 da; undan oldin `@MockBean`) bilan stub qilinadi. Spring Data auditing'da `@EnableJpaAuditing(dateTimeProviderRef = "auditingDateTimeProvider")` va `DateTimeProvider` bean clock'dan foydalanadi; scheduling testlarida esa clock bilan birga `@Scheduled` metodini to'g'ridan-to'g'ri chaqirish ishlatiladi.

```java
@TestConfiguration
static class FixedClockConfig {
    static final Instant NOW = Instant.parse("2026-01-31T23:59:00Z");
    @Bean @Primary
    Clock clock() { return Clock.fixed(NOW, ZoneOffset.UTC); }
}
```

**Qo'llanish keyslari:**
- Subscription'ning amal qilish muddati tugashini kelasi yilga "sakrab" tekshirish.
- Oy oxiri billing cycle'ini 31-yanvar va 28/29-fevralda sinash.
- JWT/token expiry va refresh oqimini vaqtni oldinga surib test qilish.
- `createdAt`/`updatedAt` auditing qiymatlarini aniq assert qilish.
- Kechiktirilgan retry rejasini (`nextAttemptAt`) sekundlab kutmasdan tekshirish.

**Ehtiyot bo'ling:** `Clock` ni inject qilgan bo'lsangiz ham kod bazasida bitta `LocalDateTime.now()` qolgani yetarli - determinizm buziladi; ArchUnit qoidasi yoki statik tahlil bilan buni taqiqlash foydali. `Clock.fixed` butun kontekstga global qo'yilganda `@Scheduled`, cache TTL va lock timeout kabi infratuzilma mexanizmlari muzlab qolishi mumkin, shuning uchun uni odatda faqat domain bean'lariga beriladi.

## 23.31 Germetik testlar (Hermetic Tests)

**Tavsif:** Germetik test o'z ishlashi uchun kerak bo'lgan hamma narsani o'zi ko'taradi va tashqi muhitga (umumiy staging DB, jamoaviy Kafka, internet, mahalliy soat, `~/.aws` credential) bog'lanmaydi. Natijada test har qanday mashinada, har qanday tartibda va parallel ravishda bir xil natija beradi. Bu "mening mashinamda ishlaydi" muammosini va CI'dagi tasodifiy qizillarni yo'q qiladi.

**Spring'da qayerda uchraydi:** Testcontainers (`@Testcontainers`, `@Container`) + Spring Boot 3.1+ dagi `@ServiceConnection` yoki `@DynamicPropertySource` / `DynamicPropertyRegistrar` (Boot 3.4+); `spring-boot-testcontainers` moduli va `@TestConfiguration` ichidagi container bean'lar. Broker'lar uchun `spring-kafka-test` ning `@EmbeddedKafka`, yoki Testcontainers `KafkaContainer`/`RabbitMQContainer`; tashqi HTTP uchun WireMock stub. Konfiguratsiyani `@TestPropertySource`/`application-test.yml` bilan qotirib, profile'ga `cloud` secret'lari oqib kelmasligi ta'minlanadi; vaqt uchun `Clock` bean, tasodif uchun seed berilgan `Random`. Spring Modulith'da `@ApplicationModuleTest` kontekstni faqat kerakli modul bilan cheklaydi.

**Qo'llanish keyslari:**
- CI'da internet yopiq holatda ham to'liq integratsiya suite'ini o'tkazish.
- Umumiy staging DB'dagi "boshqa jamoa ma'lumotimni o'chirdi" muammosini butunlay yo'qotish.
- Testlarni `-parallel` rejimida izolatsiya buzilmasdan 4-8 fork'da yugurtirish.
- Yangi dasturchi uchun `git clone && ./mvnw verify` ni bitta buyruqda ishlaydigan qilish.
- Reproducible bug-report: muammoni aynan shu container versiyasida qayta ko'rsatish.

**Ehtiyot bo'ling:** Germetiklik tezlik hisobidan keladi - har test class'i uchun yangi container ko'tarsangiz suite daqiqalarga cho'ziladi; singleton container pattern, `reuse.enable=true` va Spring kontekst caching (bir xil konfiguratsiya → bir xil kontekst) bilan balanslang. Shuni ham bilib qo'ying: germetik testlar prod muhitidagi tarmoq, DNS, IAM va sertifikat muammolarini ushlamaydi - ularga alohida smoke/E2E qatlami kerak.

## 23.32 Flaky testlarni karantinga olish (Flaky Test Quarantine)

**Tavsif:** Beqaror (flaky) test butun pipeline ishonchini buzadi: jamoa qizil build'ni "yana shu test" deb o'tkazib yubora boshlaydi va real regressiyalar ham e'tibordan chetda qoladi. Pattern: flaky test'ni asosiy gate'dan chiqarib, alohida tag/suite ichiga "karantin"ga olish, uni owner va deadline bilan ticket qilib qayd etish, keyin tuzatib qaytarish yoki o'chirish. Muhim shart: karantin - vaqtinchalik palata, abadiy go'ristonga aylanmasligi kerak.

**Spring'da qayerda uchraydi:** JUnit 5 `@Tag("flaky")` + Maven Surefire/Failsafe `<excludedGroups>flaky</excludedGroups>` yoki Gradle `test { useJUnitPlatform { excludeTags 'flaky' } }`; alohida `flakyTest` task/profil karantin suite'ini nightly yugurtiradi. Qayta urinishlar uchun Gradle `org.gradle.test-retry` plugin'i, Maven Surefire `rerunFailingTestsCount`, yoki JUnit Pioneer `@RetryingTest`. Vaqtinchalik o'chirish uchun `@Disabled("JIRA-1234")`, muhitga qarab `@DisabledIfEnvironmentVariable`/`@EnabledIf`; barqarorlikni o'lchash uchun `@RepeatedTest(50)`. Develocity (Gradle Enterprise) va ko'p CI platformalari flaky test detection reportini beradi.

**Qo'llanish keyslari:**
- Tashqi sandbox API'ga bog'liq testni karantinga olib, uni WireMock stub'ga ko'chirish.
- Vaqt/`Thread.sleep` ga tayangan testni Awaitility'ga o'tkazishdan oldin gate'dan chiqarish.
- Test order'ga bog'liq (shared state) testni aniqlash uchun `@RepeatedTest` bilan 50 marta yugurtirish.
- Release oldidan karantin ro'yxatini ko'rib chiqib, "abadiy disabled" testlarni o'chirish yoki tiklash.
- Nightly karantin suite natijasini dashboard'ga chiqarib, texnik qarzni ko'rinadigan qilish.

**Ehtiyot bo'ling:** `rerunFailingTestsCount` yoki test-retry ni global yoqib qo'yish eng yomon variant - u flakiness'ni yashiradi va real race condition bug'lari prod'ga o'tib ketadi; retry faqat karantin suite'ida yoki aniq sabab bilan ishlatilishi kerak. Karantin ticket va egasi bo'lmasa, oylar o'tib o'nlab `@Disabled` test yig'iladi va coverage illuziyasi paydo bo'ladi.

## 23.33 Unumdorlik va yuklama testlari (Performance / Load Testing)

**Tavsif:** Funksional testlar "to'g'rimi?" degan savolga javob beradi, yuklama testlari esa "kutilgan trafikda qancha latency va throughput beradi, qachon sinadi?" degan savolga. Odatda bir necha turi ajratiladi: load (kutilgan yuklama), stress (chegarani topish), soak (uzoq muddatli memory leak/connection leak), spike (keskin o'sish). Natija SLO ko'rinishida (masalan p99 < 300ms, error rate < 0.1%) yozilib, CI yoki release gate'ga bog'lanadi.

**Spring'da qayerda uchraydi:** Gatling Java DSL (`io.gatling.javaapi.core.Simulation`, `gatling-maven-plugin`), k6 (JavaScript ssenariy, Grafana ekosistemasi, `k6 run` CI'da konteyner sifatida), Apache JMeter (`.jmx` plan + `jmeter-maven-plugin`). Ilova tomonida `spring-boot-starter-actuator` + Micrometer metrikalari (`http.server.requests`, `hikaricp.connections.pending`, `jvm.gc.pause`) Prometheus/Grafana orqali o'lchanadi; `@Timed` va `ObservationRegistry` custom metrika qo'shadi. Metod darajasidagi mikro-o'lchov uchun JMH (`@Benchmark`, `@State`) ishlatiladi, DB tomonini tahlil qilishda HikariCP pool metrikalari va `spring.jpa.properties.hibernate.generate_statistics` yordam beradi.

**Qo'llanish keyslari:**
- Yangi search endpoint'ini 500 RPS'da p99 latency SLO'ga tushishini tekshirish.
- Hikari pool size va `connection-timeout` sozlamalarini stress test bilan kalibrlash.
- 8 soatlik soak test bilan cache yoki `WebClient` connection leak'ini topish.
- Black Friday spike ssenariysida autoscaling va rate limiter xulqini sinash.
- Reactive (WebFlux) va blocking (MVC) variantlarni bir xil yuklamada taqqoslab, migratsiya qarorini asoslash.

**Ehtiyot bo'ling:** Laptop'dan prod'ga yoki noto'g'ri sizing'li test muhitiga yuklama berish ma'nosiz raqamlar beradi - load generator, tarmoq va DB sizing prod'ga yaqin bo'lishi, test ma'lumoti realistik hajmda bo'lishi shart. O'rtacha (mean) latency'ga qarab qaror qabul qilmang: p95/p99 va error rate'ni, hamda JIT warm-up va GC rejimini hisobga oling; shuningdek yuklama testini hech qachon ruxsatsiz uchinchi tomon tizimiga qaratmang.

## 23.34 Smoke testlar (Smoke Tests)

**Tavsif:** Smoke test - deploy'dan keyin "ilova umuman tirikmi?" degan savolga bir-ikki daqiqada javob beradigan juda qisqa, yuzaki tekshiruvlar to'plami. U chuqur biznes logikani emas, eng muhim yo'llarni (kontekst ko'tarildi, health yashil, login ishlaydi, asosiy endpoint 200 qaytaradi, DB va broker'ga ulanish bor) tekshiradi. Maqsad - buzilgan release'ni foydalanuvchiga yetib bormasdan, tez va arzon aniqlash.

**Spring'da qayerda uchraydi:** Eng oddiy shakli - `@SpringBootTest` bilan bo'sh `contextLoads()` testi: u barcha bean'lar yaratilishini, konfiguratsiya va `@ConfigurationProperties` validatsiyasini tekshiradi. Deploy'dan keyingi tomonda Actuator `/actuator/health` (`HealthIndicator`, `DataSourceHealthIndicator`), `health.group` bilan ajratilgan `/actuator/health/readiness` va `/liveness` (`AvailabilityChangeEvent`, `ApplicationAvailability`), hamda `/actuator/info` ishlatiladi. Testlarni `@Tag("smoke")` bilan belgilab, Maven Failsafe `-Dgroups=smoke` yoki alohida CI step'da real environment URL'iga `RestClient`/`TestRestTemplate` bilan yugurtiriladi.

**Qo'llanish keyslari:**
- Kubernetes rollout'dan keyin readiness probe va asosiy GET endpoint'ini tekshirib, canary'ni davom ettirish yoki qaytarish.
- `@SpringBootTest` context-load testi bilan noto'g'ri bean definition yoki yetishmayotgan property'ni PR darajasida ushlash.
- Migration'dan keyin DB ulanishi va Flyway `schema_history` holatini tekshirish.
- Secret rotation'dan keyin tashqi servislarga autentifikatsiya hali ishlayotganini tasdiqlash.
- Release train'da har bir mikroservisning `/actuator/health` yashilligini bitta smoke suite bilan jamlab ko'rish.

**Ehtiyot bo'ling:** Smoke suite sekin-asta "kichik regressiya suite"ga aylanib ketmasligi kerak - u daqiqalarda, minimal ma'lumot yozmasdan tugashi lozim. Prod'da yugurtirilsa, test faqat o'qish amallari bilan cheklanishi yoki aniq belgilangan test akkaunt/sandbox ma'lumotidan foydalanishi, hamda prod metrikalari va alertlarini buzmasligi shart.

## 23.35 Uchidan-uchiga testlar (End-to-End Tests)

**Tavsif:** E2E test real foydalanuvchi ssenariysini butun stack bo'ylab - UI yoki public API'dan boshlab, servislar, broker va DB orqali - bajaradi. U integratsiya nuqtalarini, konfiguratsiyani va biznes oqimining yaxlitligini tekshiradi, ya'ni boshqa hech qanday qatlam ushlay olmaydigan xatolarni topadi. Shu bilan birga eng sekin, eng qimmat va eng beqaror qatlam, shuning uchun test piramidasida eng kam sonda bo'lishi kerak.

**Spring'da qayerda uchraydi:** `@SpringBootTest(webEnvironment = WebEnvironment.RANDOM_PORT)` + `@LocalServerPort` va `TestRestTemplate` yoki `WebTestClient` (WebFlux uchun ham MVC uchun ham `bindToServer()` rejimida) - bitta servis uchun to'liq oqim. Ko'p servisli oqimda Testcontainers `ComposeContainer`/`DockerComposeContainer` yoki Kubernetes namespace ko'tariladi, tashqi tomonlar WireMock bilan stub qilinadi. Brauzer darajasida `playwright-java`, Selenium WebDriver yoki Selenide; ssenariylarni o'qiydigan qilish uchun Cucumber/JBehave; `spring-boot-starter-test` ichidagi AssertJ va JsonPath assert'lar bilan birlashtiriladi.

**Qo'llanish keyslari:**
- "Buyurtma berish → to'lov → event → email" oqimini bir testda uchidan-uchiga tasdiqlash.
- Checkout formasidan to DB'dagi yozuvgacha bo'lgan yo'lni Playwright bilan brauzerda o'ynatish.
- Mikroservislar orasidagi Kafka contract'i realda mos kelishini Compose muhitida sinash.
- Reverse proxy, CORS, cookie va session konfiguratsiyasidagi xatolarni faqat to'liq stack'da ushlash.
- Release-candidate uchun 10-15 ta eng muhim biznes oqimini "go/no-go" gate sifatida yugurtirish.

**Ehtiyot bo'ling:** E2E testni unit test o'rniga ishlatish klassik "teskari piramida" anti-pattern'i: suite soatlab ishlaydi, flaky bo'ladi va xato sababini ko'rsatmaydi. Sahifa yuklanishini `Thread.sleep` bilan kutish o'rniga explicit wait/Awaitility ishlating, test ma'lumotini har run'da o'zi yaratadigan qilib yozing va E2E sonini ongli ravishda cheklab turing.

## 23.36 Reactive kodni test qilish (Testing Reactive Code)

**Tavsif:** `Mono`/`Flux` natijani darhol qaytarmaydi - oddiy `assertEquals` bilan test qilinsa, yo `block()` chaqirib reactive semantikani buziladi, yo signal'lar (`onNext`, `onComplete`, `onError`), backpressure va vaqt bo'yicha xulq umuman tekshirilmay qoladi. `StepVerifier` publisher'ga subscribe bo'lib, kutilgan signal ketma-ketligini deklarativ tasdiqlaydi va virtual vaqt bilan `delay`/`timeout` ssenariylarini real kutmasdan o'ynatadi.

**Spring'da qayerda uchraydi:** `io.projectreactor:reactor-test` (`spring-boot-starter-webflux` bilan birga odatda test scope'da keladi): `StepVerifier.create(flux).expectNext("a","b").verifyComplete()`, `expectNextCount`, `expectError(MyException.class)`, `expectNextMatches`, `thenCancel().verify()`. Vaqt uchun `StepVerifier.withVirtualTime(...)` + `thenAwait(Duration.ofHours(1))` (ichida `VirtualTimeScheduler`). Qo'shimcha asboblar: `TestPublisher` (signal'ni qo'lda yuborish, `TestPublisher.createNoncompliant`), `PublisherProbe` (subscribe bo'ldimi, cancel bo'ldimi), `ReactorContext` uchun `contextWrite`. Web qatlamida `@WebFluxTest` + `WebTestClient`, R2DBC uchun `@DataR2dbcTest`, operator ketma-ketligini kuzatishda `Hooks.onOperatorDebug()` yoki `ReactorDebugAgent`.

```java
StepVerifier.withVirtualTime(() -> service.pollWithRetry())
    .expectSubscription()
    .thenAwait(Duration.ofSeconds(30))
    .expectNext("ok")
    .verifyComplete();
```

**Qo'llanish keyslari:**
- `retryWhen(Retry.backoff(...))` ning aniq necha marta va qanday intervalda urinishini virtual vaqtda tekshirish.
- `timeout(Duration)` ishlaganda `TimeoutException` chiqishini sekundlab kutmasdan tasdiqlash.
- `Flux` cancel bo'lganda resurs yopilishini `PublisherProbe.assertWasCancelled()` bilan tekshirish.
- SSE/streaming endpoint'ini `WebTestClient.returnResult(...).getResponseBody()` + `StepVerifier` bilan sinash.
- Reactive pipeline ichida `Context`dagi tenant yoki trace id to'g'ri tarqalishini tekshirish.

**Ehtiyot bo'ling:** `verify()` yoki `verifyComplete()` chaqirilmasa `StepVerifier` hech narsa tekshirmaydi va test soxta yashil bo'ladi; `block()` bilan test yozish esa blocking xatolarini (`BlockHound` ushlaydigan) yashiradi. `withVirtualTime` faqat o'z ichidagi `Supplier` da yaratilgan publisher'ga ta'sir qiladi - tashqarida yaratilgan yoki boshqa scheduler'ga biriktirilgan oqimda virtual vaqt ishlamaydi.

## 23.37 Xavfsizlikni test qilish (Testing Security)

**Tavsif:** Authorization qoidalari - eng xatarli, ammo eng kam test qilinadigan joy: bitta `hasRole` xatosi butun ma'lumotni ochib qo'yishi mumkin. Pattern: security qoidalarini real autentifikatsiya oqimi (login, token olish) orqali emas, testda sintetik `Authentication` o'rnatib tekshirish. Shunda har bir endpoint va metod uchun "kim kirishi mumkin, kim 401/403 oladi" matritsasi tez va deterministik sinovdan o'tadi.

**Spring'da qayerda uchraydi:** `spring-security-test` moduli: `@WithMockUser(username="ali", roles={"ADMIN"})`, `@WithAnonymousUser`, `@WithUserDetails("ali")`, custom annotatsiya uchun `@WithSecurityContext`. MockMvc tomonida `SecurityMockMvcRequestPostProcessors` (`csrf()`, `user(...)`, `jwt()`, `opaqueToken()`, `oauth2Login()`) va `SecurityMockMvcResultMatchers` (`authenticated()`, `unauthenticated()`); `MockMvcBuilders...apply(springSecurity())` yoki Boot'da `@AutoConfigureMockMvc`. WebFlux'da `WebTestClient.mutateWith(SecurityMockServerConfigurers.mockUser()/mockJwt())`. Metod darajasidagi `@PreAuthorize`/`@PostFilter` ni test qilish uchun `@EnableMethodSecurity` yoqilgan kontekst kerak; `@WebMvcTest` da security filter chain cheklangani uchun ko'pincha `@SpringBootTest` afzal.

**Qo'llanish keyslari:**
- Har bir admin endpoint uchun `@WithMockUser(roles="USER")` bilan 403 qaytishini tasdiqlash.
- CSRF himoyasi yoqilgan POST'da `csrf()` bo'lmasa 403 bo'lishini tekshirib, konfiguratsiyani qotirish.
- JWT scope va custom claim'ga asoslangan authorization'ni `jwt().authorities(...)` bilan sinash.
- `@PreAuthorize("#id == authentication.name")` kabi ownership qoidasini ikki xil user bilan tekshirish.
- Multi-tenant filterda boshqa tenant ma'lumoti ko'rinmasligini parametrlangan testlar bilan isbotlash.

**Ehtiyot bo'ling:** `@WithMockUser` real login, token validatsiyasi, JWKS, session va CORS'ni tekshirmaydi - bu qatlamlar uchun alohida integratsiya/E2E testi kerak; `roles = "ADMIN"` avtomatik `ROLE_` prefiksini qo'shadi, `authorities = "ADMIN"` esa qo'shmaydi va bu chalkashlik juda ko'p soxta yashil testga sabab bo'ladi. Testda security'ni butunlay o'chirib qo'yish (`@AutoConfigureMockMvc(addFilters = false)`) qulay, lekin shunda autorizatsiya mutlaqo test qilinmayotganini unutmang.

## 23.38 Event'larni test qilish (Testing Events)

**Tavsif:** Event-driven dizaynda biznes natija ko'pincha publisher'ning qaytargan qiymatida emas, balki chiqarilgan event va uning listener'lari ta'sirida ko'rinadi. Shuning uchun test "nima qaytdi?" emas, "qanday event chiqdi, payload'i to'g'rimi, listener qanday reaksiya qildi?" degan savolni tekshirishi kerak. Spring buning uchun kontekstdagi barcha event'larni yozib oladigan va modul darajasida ssenariy yozishga imkon beradigan asboblar beradi.

**Spring'da qayerda uchraydi:** Spring Framework 5.3.3+ dan `@RecordApplicationEvents` + test'ga inject qilinadigan `ApplicationEvents` (`events.stream(OrderPlaced.class).count()`); publisher tomonida `ApplicationEventPublisher`, `@EventListener`, `@TransactionalEventListener(phase = AFTER_COMMIT)`. Spring Modulith'da `@ApplicationModuleTest` + `Scenario` parametri: `scenario.stimulate(() -> service.place(order)).andWaitForEventOfType(OrderPlaced.class).toArriveAndVerify(e -> ...)`, hamda `PublishedEvents`/`AssertablePublishedEvents` va `@ApplicationModuleTest(mode = STANDALONE)` bilan modulni izolyatsiyada ko'tarish; Modulith event publication registry esa `IncompleteEventPublications` orqali yetib bormagan event'larni tekshirishga imkon beradi. Listener'ni alohida test qilishda uni oddiy bean sifatida to'g'ridan-to'g'ri chaqirish yoki `@MockitoBean` bilan almashtirish mumkin.

**Qo'llanish keyslari:**
- `OrderPlaced` event'i aynan bir marta va to'g'ri `orderId` bilan chiqishini tekshirish.
- `AFTER_COMMIT` listener'i rollback bo'lganda ishlamasligini tasdiqlash.
- Modulith'da buyurtma moduli event chiqargach, inventory moduli zaxirani kamaytirishini `Scenario` bilan tekshirish.
- Async `@EventListener` ning chaqirilishini `ApplicationEvents` yoki Awaitility bilan kutib tasdiqlash.
- Event payload'ining JSON serializatsiyasi (externalization) buzilmaganini kontrakt testi bilan qotirish.

**Ehtiyot bo'ling:** `ApplicationEvents` faqat test ishlayotgan thread va kontekstdagi event'larni yozadi - `@Async` listener yoki boshqa thread'dagi event uchun Awaitility bilan kutish kerak, aks holda test race condition tufayli flaky bo'ladi. Event'ni "ichki metod chaqiruvi" o'rniga tekshirish kodni test bilan juda qattiq bog'lab qo'yishi mumkin: event'ni domen kontrakti sifatida qarang va har bir refactoring'da o'zgaradigan texnik detal qilib ishlatmang.

## 23.39 Asinxron kodni test qilish (Testing Async Code)

**Tavsif:** `@Async` metod, message listener yoki scheduled job natijasi test thread'ida darhol ko'rinmaydi, shuning uchun assert "hali bo'lmagan" holatni tekshirib yiqiladi. Oson, ammo yomon yechim - `Thread.sleep(2000)`: sekin mashinada yetmaydi (flaky), tez mashinada esa bekorga vaqt yo'qotadi. To'g'ri pattern - polling bilan shartni kutish: natija kelishi bilanoq davom etish, berilgan timeout ichida kelmasa tushunarli xato bilan yiqilish.

**Spring'da qayerda uchraydi:** Awaitility (`org.awaitility:awaitility`, versiyasi `spring-boot-dependencies` BOM'da boshqariladi, dependency'ni o'zingiz qo'shasiz): `await().atMost(Duration.ofSeconds(5)).pollInterval(Duration.ofMillis(100)).untilAsserted(() -> assertThat(repo.count()).isEqualTo(1))`, shuningdek `pollDelay`, `ignoreExceptions()`, `until(...)` va timeout'da `ConditionTimeoutException`. Spring tomonida test qilinadigan mexanizmlar: `@EnableAsync` + `@Async` va `TaskExecutor` (Boot 3.2+ da virtual thread'lar `spring.threads.virtual.enabled`), `@Scheduled`, `@KafkaListener` (`spring-kafka-test` ning `@EmbeddedKafka`, `KafkaTestUtils`), `@RabbitListener`, Modulith'ning `Scenario.andWaitForStateChange(...)`. Deterministiklik kerak bo'lganda test profilida `SyncTaskExecutor`/`ThreadPoolTaskExecutor` ni almashtirish ham ishlatiladi.

**Qo'llanish keyslari:**
- `@KafkaListener` xabarni iste'mol qilib, DB'ga yozganini `untilAsserted` bilan kutish.
- `@Async` notification yuborilganini mock verify bilan 3 sekund ichida tasdiqlash.
- Scheduled reconciliation job natijasini `fixedDelay` ni test profilida qisqartirib tekshirish.
- Outbox/retry mexanizmi xabarni qayta yuborishini polling bilan kuzatish.
- Cache invalidation event'idan keyin cache bo'shashini `await().until(...)` bilan tekshirish.

**Ehtiyot bo'ling:** Faqat `until(() -> flag)` bilan boolean kutish xato sababini ko'rsatmaydi - `untilAsserted(...)` ishlating, u oxirgi assertion xatosini chiqaradi. `atMost` ni ortiqcha katta (masalan 60s) qo'ymang, aks holda real buglar sekin suite ortida yashiradi; shuningdek kutish shartini "hech qachon o'zgarmaydigan" narsa (masalan log satri) emas, kuzatiladigan holat (DB, cache, mock interaction) ustiga yozing.

## 23.40 Dummy obyekt (Dummy Object)

**Tavsif:** Dummy obyekt - test uchun zarur bo'lgan, lekin hech qachon ishlatilmaydigan parametrni to'ldirish uchun uzatiladigan obyekt. Uning hech qanday xatti-harakati yo'q: metodlari chaqirilmasligi kutiladi, chaqirilsa ham natija ahamiyatsiz. Asosiy maqsadi - konstruktor yoki metod signaturasini qoniqtirish, ya'ni "bo'sh joy to'ldiruvchi" sifatida xizmat qilish. Ko'pincha `null` o'rniga ishlatiladi, chunki `null` kodda NPE yoki yashirin shart tekshiruvlarini keltirib chiqarishi mumkin.

**Spring'da qayerda uchraydi:** Mockito'ning `Mockito.mock(Type.class)` chaqiruvi hech qanday `when(...)` sozlamasisiz amalda dummy rolini bajaradi - barcha metodlar default (`null`, `0`, `false`) qaytaradi. Spring ekosistemasida `org.springframework.mock.web.MockHttpServletRequest`, `MockHttpSession` yoki `org.springframework.mock.env.MockEnvironment` ko'p hollarda shunchaki signaturani to'ldirish uchun uzatiladi. `@MockitoBean` (Spring Framework 6.2+ / Spring Boot 3.4-3.5 va Boot 4 da, eski `@MockBean` o'rnida) bilan e'lon qilingan va test ichida hech qachon stub qilinmagan bean ham dummy hisoblanadi. Java 17+ `record` yoki `sealed interface` yordamida yengil dummy implementatsiya yozish qulay, chunki `record` bir qatorda butun DTO ni qoplaydi.

**Qo'llanish keyslari:**
- Ko'p argumentli domain konstruktorini test qilishda faqat bitta maydon tekshirilsa, qolgan hamkor obyektlarni dummy bilan to'ldirish.
- `OrderService(PaymentGateway, AuditLogger, NotificationSender)` da faqat payment yo'li tekshirilayotganda audit va notification uchun dummy uzatish.
- `Authentication` yoki `Principal` obyektini talab qiladigan, lekin uni o'qimaydigan controller metodini sinovdan o'tkazish.
- Legacy sinfning `ServletContext` kabi og'ir bog'liqligini `MockServletContext` dummy bilan almashtirib, test kompilyatsiyasini ta'minlash.
- Exception yo'lini tekshirishda, xato konstruktor validatsiyasida uzilgani uchun keyingi bog'liqliklar hech qachon chaqirilmasligi.

**Ehtiyot bo'ling:** Agar dummy obyektning metodi aslida chaqilib, `null` qaytargani uchun test "yashil" bo'lsa - bu soxta ishonch; shunday hollarda dummy emas, stub kerak bo'ladi. Dummy'lar soni ko'payib ketsa, bu sinfning juda ko'p bog'liqligi borligini (SRP buzilishini) ko'rsatuvchi signaldir, uni mock ko'paytirish bilan emas, refaktoring bilan hal qilish kerak.

## 23.41 Test stub (Test Stub)

**Tavsif:** Test stub - testga kerakli "indirect input" ni, ya'ni tashqi bog'liqlikdan keladigan oldindan belgilangan javoblarni beradigan soxta implementatsiya. Haqiqiy bog'liqlik (ma'lumotlar bazasi, HTTP mijoz, soat) o'rniga qo'yiladi va har doim bir xil, oldindan aytib bo'ladigan natija qaytaradi. Shuningdek, xato ssenariylarini modellashtirish uchun exception tashlashi mumkin (bunday variant "saboteur" deb ataladi). Stub chaqiruvlarni tekshirmaydi - u faqat ma'lumot beradi.

**Spring'da qayerda uchraydi:** Mockito'ning `when(repo.findById(1L)).thenReturn(Optional.of(order))` va `given(...).willReturn(...)` (BDDMockito) - eng keng tarqalgan stubbing usuli. HTTP darajasida `org.springframework.test.web.client.MockRestServiceServer` `RestTemplate` uchun, `MockRestServiceServer.bindTo(RestClient.builder())` esa Spring Framework 6.1+ `RestClient` uchun javoblarni stub qiladi; reaktiv tomonda `WebClient` ga `ExchangeFunction` stub berish yoki WireMock (`@AutoConfigureWireMock`, Spring Cloud Contract) ishlatiladi. Vaqtga bog'liq kodda `java.time.Clock.fixed(...)` ni bean sifatida inject qilish - klassik stub. Spring AI 1.x da `ChatModel` interfeysini stub qilib, LLM javobini determinlashtirish mumkin, shunda testda real model chaqirilmaydi.

**Qo'llanish keyslari:**
- `OrderRepository.findById` ni stub qilib, service'ning "topilmadi" tarmog'ini unit darajada tekshirish.
- Tashqi to'lov provayderining `503` javobini `MockRestServiceServer` bilan modellashtirib, retry va fallback logikasini sinash.
- `Clock.fixed` orqali "muddati o'tgan token" holatini vaqt kutmasdan reproduksiya qilish.
- Feature flag provayderini stub qilib, bir xil kodni ikki xil konfiguratsiyada tekshirish.
- `ChatModel` ni fiksirlangan javob bilan stub qilib, prompt-parsing va output-converter logikasini LLM'ga murojaat qilmasdan test qilish.

**Ehtiyot bo'ling:** Haddan ziyod stubbing testni implementatsiyaga mahkam bog'lab qo'yadi - har bir refaktoringda o'nlab test "qizil" bo'ladi; stub javoblari real API bilan sinxrondan chiqib ketishi mumkin, shuning uchun contract test (Spring Cloud Contract) yoki Testcontainers bilan qoplash kerak. `Mockito.verify` ni stub ustida ishlatish patternlarni aralashtirish hisoblanadi - bu holda siz allaqachon mock yozayotgan bo'lasiz. Butun obyektlar to'rini bitta stub bilan almashtirish kerak bo'lsa, stub ning maxsus holati [entity zanjirini kesish](#2389-entity-zanjirini-kesish-entity-chain-snipping) da yozilgan.

## 23.42 Test spy (Test Spy)

**Tavsif:** Test spy - real yoki soxta obyektning chaqiruvlarini (argumentlar, chaqiruvlar soni, tartibi) yozib oladigan, lekin tekshirishni testning assert fazasiga qoldiradigan obyekt. Mock'dan farqi shunda: spy kutilgan xatti-harakatni oldindan e'lon qilmaydi, balki "nima bo'lgani" ni qayd etadi va keyin tekshiriladi. Bu "indirect output" ni, ya'ni tizim chiqishini bevosita qaytarilgan qiymat orqali emas, hamkor obyektga bergan buyruqlar orqali kuzatish imkonini beradi.

**Spring'da qayerda uchraydi:** Mockito'ning `Mockito.spy(realObject)` va `@Spy` real implementatsiyani o'rab, chaqiruvlarni yozib oladi; `@MockitoSpyBean` (Spring Framework 6.2+ / Boot 3.4-3.5 va Boot 4 da, eski `@SpyBean` o'rnida) ApplicationContext'dagi haqiqiy beanni spy bilan o'raydi - shu bilan real logika ishlaydi, lekin chaqiruvlarni `verify(...)` bilan tekshirish mumkin. `ArgumentCaptor<T>` yoki `@Captor` uzatilgan argumentni ushlab olish uchun ishlatiladi. Spring'ning o'z test infratuzilmasida `ApplicationEvents` (`@RecordApplicationEvents`, Spring Framework 5.3.3+) - publish qilingan eventlarni yozib oladigan toza spy; `OutputCaptureExtension` (`@ExtendWith`, Spring Boot) konsol chiqishini, `MockMvc` esa `MvcResult` ichida butun request-response oqimini qayd etadi.

**Qo'llanish keyslari:**
- `@MockitoSpyBean` bilan real `PaymentService` ishlashini saqlab, `charge()` metodining necha marta chaqirilganini tekshirish.
- `ArgumentCaptor<OrderCreatedEvent>` orqali publish qilingan event ichidagi `orderId` va `occurredAt` qiymatlarini tasdiqlash.
- `@RecordApplicationEvents` + `ApplicationEvents` bilan bitta transaction'da nechta domain event chiqarilganini sanash.
- Kesh bilan ishlashda repository'ni spy qilib, ikkinchi chaqiruvda DB ga murojaat bo'lmaganini isbotlash.
- Retry policy tekshirishda tashqi mijozga aynan 3 marta murojaat qilinganini `verify(client, times(3))` bilan tasdiqlash.

**Ehtiyot bo'ling:** Chaqiruvlar sonini va tartibini juda qattiq tekshirish testni ichki implementatsiyaga bog'laydigan "overspecification" ga olib keladi - natijani tekshirish mumkin bo'lganda spy'dan voz kechish afzal. `@MockitoSpyBean` CGLIB proxy bilan o'ralgan bean ustida `final` metodlarni intercept qilmaydi va `self-invocation` chaqiruvlari ko'rinmaydi; bu jim o'tib ketadigan noto'g'ri natija beradi.

## 23.43 Mock obyekt (Mock Object)

**Tavsif:** Mock obyekt - kutilgan chaqiruvlar to'plami oldindan e'lon qilinadigan va o'zi shu kutishni tekshiradigan soxta obyekt. Spy'dan farqi shundaki, mock "behavior verification" ga mo'ljallangan: shartnoma buzilsa (kutilmagan chaqiruv yoki yetishmayotgan chaqiruv) testni o'zi muvaffaqiyatsiz qiladi. Bu, ayniqsa, metodning qaytaruvchi qiymati bo'lmagan (`void`) yoki natija faqat tashqi tizimga yuborilgan buyruqdan bilinadigan hollarda zarur.

**Spring'da qayerda uchraydi:** Mockito (`@Mock`, `@ExtendWith(MockitoExtension.class)`, `verify`, `verifyNoMoreInteractions`, `InOrder`) - Spring Boot'ning `spring-boot-starter-test` tarkibidagi standart vosita. Spring konteksti ichida `@MockitoBean` (Spring Framework 6.2+) ApplicationContext'dagi beanni mock bilan almashtiradi va kontekst keshini shu konfiguratsiya bo'yicha ajratadi. `MockitoExtension` ning `Strictness.STRICT_STUBS` rejimi ishlatilmagan stublarni xato deb belgilaydi. Messaging qatlamida `org.springframework.messaging.MessageHandler` yoki `KafkaTemplate` ni mock qilib, publish shartnomasi tekshiriladi.

**Qo'llanish keyslari:**
- `void sendEmail(...)` kabi natijasiz metodda xabar aynan bir marta va to'g'ri argument bilan yuborilganini tasdiqlash.
- `KafkaTemplate.send(topic, key, payload)` chaqiruvi kutilgan topic'ga ketganini `verify` bilan tekshirish.
- `InOrder` yordamida "avval lock oling, keyin yozing, so'ng lockni bo'shating" tartibini majburlash.
- `verifyNoInteractions(paymentGateway)` bilan validatsiya xatosida to'lov provayderiga umuman murojaat qilinmaganini isbotlash.
- Audit talabi bo'lgan domenlarda har bir muhim amal uchun `AuditLogger` ga yozuv ketganini kafolatlash.

**Ehtiyot bo'ling:** Mock'ka asoslangan testlar tez-tez "tautologik" bo'lib qoladi - siz yozgan kodning ichki tuzilishini qayta ta'riflaydi va xatoni ushlamaydi; `verify` ni natijani assert qilish mumkin bo'lgan joyda ishlatmang. `@MockitoBean` ning har bir noyob kombinatsiyasi yangi ApplicationContext yaratadi va test suite'ni sezilarli sekinlashtiradi, shuning uchun integration darajada uni minimallashtirish kerak.

## 23.44 Soxta obyekt (Fake Object)

**Tavsif:** Fake obyekt - real bog'liqlikning yengil, lekin haqiqiy ishlaydigan implementatsiyasi: u to'g'ri xatti-harakatga ega, ammo production uchun yaroqsiz (masalan, xotirada saqlaydi, tranzaksiyani qo'llamaydi, tezlik uchun soddalashtirilgan). Stub'dan farqi - fake ichida haqiqiy mantiq va holat bor, shuning uchun bir nechta chaqiruv o'zaro bog'liq ishlaydi: yozganingizni keyin o'qiy olasiz. Bu testlarni implementatsiya detallariga emas, xatti-harakatga bog'laydi.

**Spring'da qayerda uchraydi:** Spring'da fake'lar odatda qo'lda yoziladi: `OrderRepository` interfeysining `ConcurrentHashMap` ga asoslangan `InMemoryOrderRepository` implementatsiyasi `@TestConfiguration` ichida `@Bean` sifatida beriladi va `@Primary` yoki profile bilan tanlanadi. Spring ekosistemasidagi tayyor fake'lar: `org.springframework.mock.web.MockHttpServletRequest/Response` (Servlet API ning ishlaydigan soddalashtirilgan versiyasi), `MockEnvironment`, `SimpleAsyncTaskExecutor`, `ConcurrentMapCacheManager` (Redis o'rniga), `spring-kafka-test` ning `EmbeddedKafkaBroker` (`@EmbeddedKafka`), H2 yoki HSQLDB in-memory DB. E'tibor bering: `Testcontainers` (`@ServiceConnection`, Spring Boot 3.1+) fake emas - u real servisni konteynerda ishga tushiradi va aniqlik jihatidan afzal.

**Qo'llanish keyslari:**
- Domain service'ni in-memory repository fake bilan test qilib, mock stubbing'ini butunlay yo'q qilish.
- `@EmbeddedKafka` bilan producer va consumer oqimini real broker ko'tarmasdan uchdan-uchiga tekshirish.
- `ConcurrentMapCacheManager` ni Redis o'rniga qo'yib, `@Cacheable` annotatsiyasining kalit generatsiyasini tekshirish.
- Fayl saqlash abstraksiyasining in-memory fake'i bilan upload/download oqimini S3'ga ulanmasdan sinash.
- Hexagonal arxitekturada har bir port uchun fake adapter yozib, butun application layer'ni tez test qilish.

**Ehtiyot bo'ling:** Fake real implementatsiyadan asta-sekin "chetga chiqadi" - unique constraint, lazy loading, tranzaksiya izolyatsiyasi yoki SQL xususiyatlari fake'da bo'lmagani uchun testlar yashil, production qizil bo'lishi mumkin; shu sababli H2 ni PostgreSQL o'rniga ishlatish xatoli taqqoslashdir, kritik yo'llarni Testcontainers bilan qoplang. Fake'ning o'zi ham kodga aylanadi va unga o'z testlari kerak bo'lishi mumkin.

## 23.45 To'rt fazali test (Four-Phase Test)

**Tavsif:** Four-Phase Test - har bir test metodini to'rtta aniq ajratilgan fazaga bo'lish qoidasi: setup (fixture tayyorlash), exercise (SUT ni chaqirish), verify (natijani tekshirish), teardown (holatni tozalash). Bu struktura testni o'qishga oson, niyatini esa ko'rinarli qiladi: o'quvchi bir qarashda nima berilgani, nima bajarilgani va nima kutilganini ajratadi. Zamonaviy nomlari - Arrange-Act-Assert (AAA) va BDD uslubidagi Given-When-Then.

**Spring'da qayerda uchraydi:** JUnit 5 (`org.junit.jupiter`) fazalarni annotatsiyalar bilan ifodalaydi: `@BeforeEach`/`@BeforeAll` - setup, test tanasi - exercise va verify, `@AfterEach`/`@AfterAll` - teardown. Spring TestContext Framework setup fazasining katta qismini o'ziga oladi: `@SpringBootTest`, `@DataJpaTest`, `@WebMvcTest`, `@Sql` (DDL/DML skriptlari), `@DirtiesContext` va `@Transactional` bilan avtomatik rollback - ya'ni teardown deklarativ bajariladi. AssertJ (`assertThat(...)`) va `MockMvcTester` (Spring Framework 6.2+) verify fazasini ravon ifodalaydi; `@Nested` sinflar umumiy setup'ni guruhlashga yordam beradi. Java 17+ `var` va text block (`"""`) setup ma'lumotlarini ixcham yozishga imkon beradi.

**Qo'llanish keyslari:**
- Har bir test metodini `// given / // when / // then` izohlari bilan bo'lib, code review'da niyatni darhol ko'rsatish.
- `@Transactional` test bilan teardown'ni rollback'ga topshirib, DB tozalash kodini butunlay olib tashlash.
- `@Sql(scripts = "/seed-orders.sql")` orqali setup fazasini deklarativ qilish.
- `@WebMvcTest` da given - mock stublari, when - `mockMvc.perform(...)`, then - `andExpect(...)` tarzida aniq ajratish.
- `@AfterEach` da Testcontainers tomonidan yaratilgan test ma'lumotlarini tozalab, testlar orasidagi bog'liqlikni yo'q qilish.

**Ehtiyot bo'ling:** Bir metod ichida bir necha "when-then" siklini joylash fazalar chegarasini buzadi va xato sababini topishni qiyinlashtiradi - bunday testni bo'lib tashlang. `@BeforeEach` ga haddan ziyod umumiy setup to'plash "mystery guest" muammosini keltiradi: test tanasi o'z ma'lumotini ko'rsatmaydi va o'qiluvchanlik yo'qoladi.

## 23.46 Yaratish metodi (Creation Method)

**Tavsif:** Creation Method - test obyektlarini yaratishni nomlangan yordamchi metod yoki builder ortiga yashirish patterni. Testlar konstruktorning barcha argumentlarini takrorlamaydi, balki `anOrder()`, `aValidCustomer()` kabi niyatni ifodalovchi metodni chaqiradi va faqat test uchun ahamiyatli maydonni ustiga yozadi. Bu dublikatsiyani kamaytiradi va domain modeli o'zgarganda tuzatish bitta joyda bajariladi. Ko'pincha Object Mother yoki Test Data Builder shaklida amalga oshiriladi.

**Spring'da qayerda uchraydi:** Bu birinchi navbatda test kodini tashkil etish amaliyoti, Spring'ning annotatsiyasi emas: odatda `src/test/java` ichida `OrderTestFactory` yoki `OrderBuilder` sinfi yoziladi. Spring tomoni - bunday fabrikani `@TestConfiguration` ichida `@Bean` qilib e'lon qilish va testga inject qilish, yoki `TestConstructor`/`@Autowired` bilan olish. Java 17+ `record` va builder uchun yozilgan `static` fabrika metodlari, shuningdek `@TestOnly` uslubidagi `with...()` metodlari qulay; Lombok'ning `@Builder` va `toBuilder = true` varianti keng ishlatiladi. Tashqi kutubxonalar: Instancio, java-faker/Datafaker tasodifiy, ammo valid ma'lumot generatsiyasi uchun; `EasyRandom` ham shu maqsadda uchraydi.

**Qo'llanish keyslari:**
- 15 maydonli `Order` agregatini `anOrder().withStatus(PAID).build()` bilan yaratib, testlardagi uzun konstruktorlardan qutulish.
- Domain sinfiga yangi majburiy maydon qo'shilganda faqat bitta fabrika metodini tuzatish.
- `@DataJpaTest` da bir nechta bog'langan entity (Customer → Order → OrderLine) ni bitta `aPersistedOrder(em)` chaqiruvi bilan tayyorlash.
- Valid va invalid variantlarni `aValidRequest()` / `aRequestWithoutEmail()` tarzida nomlab, test niyatini sarlavhadan o'qiladigan qilish.
- Integration testlarda Datafaker bilan noyob email va hisob raqamlari generatsiya qilib, unique constraint to'qnashuvini yo'q qilish.

```java
public final class OrderMother {
    public static Order.Builder anOrder() {
        return Order.builder()
                .id(UUID.randomUUID())
                .customerId("cust-1")
                .status(OrderStatus.NEW)
                .total(Money.of("10.00", "USD"));
    }
    public static Order aPaidOrder() {
        return anOrder().status(OrderStatus.PAID).build();
    }
}
```

**Ehtiyot bo'ling:** Fabrika juda ko'p ixtiyoriy variant va shartlarni o'ziga yiqsa, u "mystery guest" ga aylanadi - test qanday ma'lumot bilan ishlayotgani ko'rinmay qoladi, shuning uchun testda ahamiyatli maydonlarni har doim oshkora ko'rsatib o'tish kerak. Tasodifiy generatsiya (Datafaker, EasyRandom) determinizmni buzishi mumkin; seed'ni fiksirlang yoki ahamiyatli maydonlarni qo'lda bering.

## 23.47 Delta assertion (Delta Assertion)

**Tavsif:** Delta Assertion - absolyut qiymatni emas, amaldan oldin va keyin o'lchangan holat orasidagi o'zgarishni (farqni) tekshirish usuli. Test boshlanishida mavjud holat noma'lum yoki boshqa testlar qoldirgan ma'lumot bo'lishi mumkin bo'lgan muhitlarda bu yondashuv ishonchli: "jadvalda 5 qator" emas, "jadvalga aynan 1 qator qo'shildi" deb tekshiriladi. Shu bilan test boshlang'ich holatga bog'liq bo'lmaydi va parallel ishlashga ko'proq chidamli bo'ladi.

**Spring'da qayerda uchraydi:** `org.springframework.test.jdbc.JdbcTestUtils.countRowsInTable(jdbcTemplate, "orders")` yoki `countRowsInTableWhere(...)` - delta o'lchash uchun eng to'g'ridan-to'g'ri vosita (`@JdbcTest`/`@DataJpaTest` bilan). Micrometer metrikalarida `MeterRegistry` (`SimpleMeterRegistry` test uchun) counter qiymatini oldin va keyin o'qib, `counter.count()` farqini tekshirish mumkin. `ApplicationEvents` (`@RecordApplicationEvents`) orqali event sonining o'sishini, `OutputCaptureExtension` orqali log qatorlari ortishini, `@EmbeddedKafka` da `KafkaTestUtils.getEndOffsets(...)` orqali topic offset deltasini o'lchash amaliyotda uchraydi. AssertJ'ning `isCloseTo(expected, within(0.01))` suzuvchi nuqta deltasi uchun ishlatiladi.

**Qo'llanish keyslari:**
- Umumiy test ma'lumotlar bazasida `orders` jadvaliga aynan bitta yozuv qo'shilganini tekshirish.
- Micrometer `orders.failed` counter qiymati operatsiyadan keyin 1 ga oshganini tasdiqlash.
- Kafka topic'dagi offset bitta xabarga o'sganini, dublikat publish bo'lmaganini isbotlash.
- Keshdagi element soni yoki hit/miss statistikasi o'zgarishini o'lchab, `@Cacheable` samaradorligini tekshirish.
- Suzuvchi nuqtali hisob-kitoblarda (valyuta kursi, foiz) natijani `isCloseTo` bilan tolerantlik oralig'ida tekshirish.

**Ehtiyot bo'ling:** Delta assertion test o'zidan keyin qoldirgan ifloslikni yashiradi - u yashil bo'lishi mumkin, holbuki ma'lumotlar bazasi bosqichma-bosqich to'lib boradi; iloji bo'lsa Fresh Fixture bilan birlashtiring. Parallel ishlaydigan testlarda boshqa thread qo'shgan qatorlar deltani buzadi, shuning uchun o'lchovni tenant yoki noyob kalit bo'yicha filtrlab oling (`countRowsInTableWhere`).

## 23.48 Guard assertion (Guard Assertion)

**Tavsif:** Guard Assertion - testning asosiy tekshiruvigacha, dastlabki shartlar haqiqatan bajarilganini tasdiqlovchi oraliq assert. Maqsadi - noto'g'ri sababga ko'ra kelib chiqqan xato haqida chalg'ituvchi xabar olmaslik: agar fixture to'g'ri tayyorlanmagan bo'lsa, test "assertion failed" o'rniga NPE yoki mantiqsiz natija bermasdan, aynan setup buzilganini aytadi. Odatda `if` sharti o'rniga qo'yiladi, chunki shartli test jim o'tib ketishi (yolg'on yashil) mumkin.

**Spring'da qayerda uchraydi:** Bu til va test kutubxonasi darajasidagi amaliyot: AssertJ `assertThat(order).isNotNull()`, JUnit 5 `assumeTrue(...)`/`assumingThat(...)` (`org.junit.jupiter.api.Assumptions`) va `org.springframework.util.Assert` yordamchisi ishlatiladi. Muhim farq: `Assumptions` testni muvaffaqiyatsiz qilmasdan "skip" qiladi - bu muhitga bog'liq shartlar uchun (masalan, Docker mavjudligi), haqiqiy guard uchun esa `assertThat` afzal. Spring'da shartli ishga tushirish uchun `@EnabledIf`, `@DisabledIfEnvironmentVariable`, `@EnabledIfSystemProperty` yoki `@IfProfileValue` deklarativ muqobil sifatida qo'llanadi; Testcontainers'da `DockerClientFactory.instance().isDockerAvailable()` tekshiruvi shu rolda uchraydi.

**Qo'llanish keyslari:**
- `@Sql` skripti ishlaganini tasdiqlash uchun asosiy assert'dan oldin `countRowsInTable` nolga teng emasligini tekshirish.
- `Optional` dan olingan entity'ni ishlatishdan avval `assertThat(found).isPresent()` bilan qo'riqlash.
- `MockMvc` javobining status kodi `200` ekanini tekshirib, keyin JSON tanasini parse qilishga o'tish.
- Testning boshida `assertThat(user.getRoles()).contains("ADMIN")` bilan fixture'ning kutilgan rolga ega bo'lishini kafolatlash.
- Docker mavjud bo'lmaganda Testcontainers testini `assumeTrue` bilan skip qilib, CI'da soxta xatolarni yo'q qilish.

**Ehtiyot bo'ling:** Guard assert'larni ko'paytirib yuborish testni shovqinli qiladi va asosiy maqsadni yashiradi - faqat xato xabari chindan ham chalg'ituvchi bo'lgan joyga qo'ying. `Assumptions` ni haqiqiy guard sifatida ishlatish xavfli: buzilgan fixture testni "skipped" holatiga o'tkazadi va CI'da hech kim sezmay qoladi.

## 23.49 Maxsus assertion (Custom Assertion)

**Tavsif:** Custom Assertion - domenga xos tekshiruvni qayta ishlatiladigan, nomlangan assert metodi yoki fluent assert sinfi ichiga joylash patterni. Bir necha maydonni alohida-alohida tekshirish o'rniga `assertThatOrder(order).isPaidWithTotal("10.00")` kabi bitta ifoda yoziladi: niyat o'qiladigan bo'ladi, xato xabari esa domen tilida chiqadi. Bu testlardagi assert dublikatsiyasini kamaytiradi va tekshiruv mantiqi o'zgarganda tuzatishni markazlashtiradi.

**Spring'da qayerda uchraydi:** AssertJ (`spring-boot-starter-test` ichida) `AbstractAssert` dan meros olib o'z assert sinfini yozishni rasman qo'llab-quvvatlaydi; shuningdek `assertThat(obj).satisfies(...)`, `extracting(...)`, `usingRecursiveComparison().ignoringFields("id")` kabi tayyor kompozitsiya vositalari bor. Spring'ning o'zida domenga xos assert'larga misol: `MockMvcResultMatchers` (`jsonPath`, `status`, `content`), `MockMvcTester` + `assertThat(result).hasStatusOk()` (Spring Framework 6.2+), `MockRestRequestMatchers`, `org.springframework.boot.test.json.JsonContentAssert` (`@JsonTest` bilan `JacksonTester`), va `ApplicationContextRunner` dagi `assertThat(context).hasSingleBean(X.class)` - auto-configuration uchun maxsus assert'lar. Reaktiv tomonda `StepVerifier` (Reactor Test) oqimlar uchun maxsus tekshiruv DSL beradi.

**Qo'llanish keyslari:**
- `OrderAssert` yozib, `status`, `total` va `auditTrail` ni bitta domen tilidagi ifodada tekshirish.
- `usingRecursiveComparison().ignoringFields("id", "createdAt")` bilan generatsiya qilinadigan maydonlarni chetlab, DTO mapping testlarini qisqartirish.
- `ApplicationContextRunner` + `assertThat(context).hasSingleBean(...)` orqali custom auto-configuration shartlarini tekshirish.
- `StepVerifier.create(flux).expectNextCount(3).verifyComplete()` bilan reaktiv pipeline xatti-harakatini ifodalash.
- Umumiy `assertValidationError(result, "email", "must not be blank")` yordamchisi bilan barcha controller validatsiya testlarini birxillashtirish.

```java
public class OrderAssert extends AbstractAssert<OrderAssert, Order> {
    public OrderAssert(Order actual) { super(actual, OrderAssert.class); }
    public static OrderAssert assertThatOrder(Order actual) { return new OrderAssert(actual); }
    public OrderAssert isPaid() {
        isNotNull();
        if (actual.status() != OrderStatus.PAID) {
            failWithMessage("Expected order <%s> to be PAID but was <%s>", actual.id(), actual.status());
        }
        return this;
    }
}
```

**Ehtiyot bo'ling:** Custom assertion ichida mantiq murakkablashsa, uning o'zi xato manbaiga aylanadi va unga ham test kerak bo'ladi; assert xabari aniq bo'lmasa, patternning asosiy foydasi yo'qoladi. `usingRecursiveComparison` ni keng ishlatish esa haddan ziyod qattiq tekshiruv beradi - har bir yangi maydon o'nlab testni buzadi.

## 23.50 Yangi fixture (Fresh Fixture)

**Tavsif:** Fresh Fixture - har bir test uchun fixture'ni noldan yaratish va test tugashi bilan uni yo'q qilish strategiyasi: testlar bir-biridan to'liq izolyatsiyalanadi va bajarilish tartibiga bog'liq bo'lmaydi. Buning teskarisi - Shared Fixture, u tezroq, lekin "flaky" testlar, yashirin bog'liqliklar va parallel ishlashdagi to'qnashuvlarning asosiy manbai. Fresh Fixture sekinroq, ammo xato lokalizatsiyasi va ishonchlilik jihatidan ustun; amalda ikkisi narx-aniqlik muvozanati bo'yicha aralashtiriladi.

**Spring'da qayerda uchraydi:** Spring TestContext Framework fixture'ni avtomatik tozalashning bir nechta mexanizmini beradi: test metodidagi `@Transactional` har bir metoddan keyin rollback qiladi (`@Commit` buni bekor qiladi), `@Sql(executionPhase = BEFORE_TEST_METHOD/AFTER_TEST_METHOD)` ma'lumotni qayta tiklaydi, `@DirtiesContext` esa ApplicationContext'ni keshdan chiqarib tashlaydi. `@DataJpaTest` va `@JdbcTest` sukut bo'yicha tranzaksion va rollback qiladigan "fresh" fixture beradi. `@TestMethodOrder` ni ishlatish tartibga bog'liqlikning belgisi; JUnit 5 ning `@TestInstance(PER_METHOD)` sukut bo'yicha har bir metod uchun yangi test instance yaratadi. Testcontainers'da `@Container` ni instance maydoni qilib qo'yish har bir test uchun yangi konteyner beradi, `static` qilish esa shared fixture hosil qiladi (`@ServiceConnection`, Spring Boot 3.1+).

**Qo'llanish keyslari:**
- `@DataJpaTest` bilan har bir repository testidan keyin rollback qilib, testlar orasidagi ma'lumot oqishini yo'q qilish.
- `@Sql` skriptini `BEFORE_TEST_METHOD` fazasida ishga tushirib, har bir testga aynan bir xil boshlang'ich holat berish.
- Parallel bajarilishga o'tishdan oldin shared fixture'ni Fresh Fixture'ga almashtirib, flaky testlarni yo'qotish.
- Noyob kalit (`UUID`) yoki tenant identifikatori bilan har bir testga o'z ma'lumot maydonini ajratib, umumiy DB da izolyatsiyaga erishish.
- Kesh yoki statik holat ishlatadigan beanni `@DirtiesContext` bilan belgilab, keyingi testlarga ifloslik o'tmasligini kafolatlash.

**Ehtiyot bo'ling:** `@DirtiesContext` ni keragidan ortiq ishlatish kontekst keshini buzadi va test suite'ni bir necha barobar sekinlashtiradi - uni faqat chindan ham kontekstni ifloslantirgan testga qo'ying. `@Transactional` rollback'i "fresh" tuyulsa ham, aslida real commit yo'lini test qilmaydi: trigger, `flush` tartibi va `AFTER_COMMIT` event'lari (`@TransactionalEventListener`) ishlamay qolishi mumkin, shuning uchun bunday holatlarda commit bilan ishlaydigan va o'zidan keyin tozalaydigan test yozish kerak.

## 23.51 Umumiy Fixture (Shared Fixture)

**Tavsif:** Bir nechta test metodi yoki test sinfi bitta tayyorlangan test muhitidan (ma'lumotlar bazasi sxemasi, konteyner, Spring context) birgalikda foydalanadi. Maqsad - qimmat resurslarni har bir test uchun qaytadan yaratmaslik va test to'plamining umumiy bajarilish vaqtini qisqartirish. Evaziga testlar orasida izolyatsiya pasayadi, shuning uchun o'zgaruvchan holatni ataylab boshqarish kerak bo'ladi.

**Spring'da qayerda uchraydi:** Spring TestContext Framework'ning `TestContext` cache'i aynan shu patternni amalga oshiradi: `@SpringBootTest` bilan ko'tarilgan `ApplicationContext` bir xil konfiguratsiya kaliti (context key) bo'lgan barcha test sinflari uchun qayta ishlatiladi va JVM ishdan to'xtaguncha cache'da saqlanadi. Testcontainers'da `@Testcontainers` + `static` konteyner maydoni, yoki Spring Boot 3.1+ dagi `@ServiceConnection` va `ConnectionDetails` orqali umumiy PostgreSQL/Kafka konteyneri butun to'plamga bir marta ko'tariladi. `@DirtiesContext` esa cache'dagi umumiy context'ni ataylab buzish (evict qilish) uchun ishlatiladi.

**Qo'llanish keyslari:**
- Yuzlab integratsion test sinflari uchun bitta `ApplicationContext`ni cache'da saqlab, build vaqtini bir necha barobar qisqartirish.
- `static` Testcontainers PostgreSQL konteynerini butun Maven/Gradle modul testlari uchun bir marta ko'tarish.
- Kafka yoki Redis kabi sekin ishga tushadigan infratuzilmani umumiy qilib, har bir testda qayta start qilmaslik.
- `@TestConfiguration` sinflarini bir xil tutib, context kalitini o'zgartirmaslik va shu orqali cache hit'ni oshirish.
- CI'da parallel test executor'lar soniga mos ravishda bitta umumiy Docker network va konteyner to'plamidan foydalanish.

**Ehtiyot bo'ling:** Umumiy fixture testlar orasida yashirin bog'liqlik tug'diradi - bir test yozgan ma'lumot ikkinchisining natijasini o'zgartirishi mumkin, natijada flaky va tartibga bog'liq testlar paydo bo'ladi. `@MockBean`/`@MockitoBean` yoki har xil `properties` qo'shish context kalitini o'zgartirib, cache'da ko'plab kontekstlar to'planishiga va OOM'ga olib kelishi mumkin. Kitob bu xavfni yo'qotadigan variantni ham beradi: fixture ni hech bir test o'zgartirmaydigan qismga va test o'zi quradigan qismga bo'lish, ya'ni [o'zgarmas umumiy fixture](#2388-ozgarmas-umumiy-fixture-immutable-shared-fixture).

## 23.52 Oldindan Qurilgan Fixture (Prebuilt Fixture)

**Tavsif:** Test ma'lumotlari test bajarilishidan oldin tashqarida tayyorlanadi: SQL skript, dump, snapshot yoki tayyor Docker image ichiga joylangan holat. Test faqat shu tayyor holatni yuklaydi, uni kod bilan qurmaydi. Bu katta va murakkab ma'lumot to'plamlarini tez yuklash imkonini beradi.

**Spring'da qayerda uchraydi:** `@Sql` va `@SqlGroup` annotatsiyalari (`org.springframework.test.context.jdbc.@Sql`) test metodidan oldin/keyin skript bajaradi; `ScriptUtils` va `ResourceDatabasePopulator` dastur ichida xuddi shuni qiladi. Spring Boot `spring.sql.init.schema-locations`/`data-locations` yoki Flyway/Liquibase migratsiyalari bilan test sxemasi va seed ma'lumotini oldindan qo'yadi. Testcontainers'da `PostgreSQLContainer.withInitScript("init.sql")` yoki ma'lumot allaqachon ichida bo'lgan custom image, hamda `DatabaseRider`/`Spring Test DBUnit` dataset XML/YAML fayllari shu patternning tipik ko'rinishi.

**Qo'llanish keyslari:**
- Legacy hisobot so'rovlarini sinash uchun minglab qatorli referens datasetni `@Sql` skript orqali yuklash.
- Reference/lookup jadvallarini (valyuta, mamlakat, soliq stavkalari) migratsiya skriptlari bilan bir marta to'ldirish.
- Katta ma'lumot bilan to'ldirilgan maxsus Docker image yasab, og'ir integratsion testlarning startini tezlashtirish.
- Produktiv bazadan anonimlashtirilgan snapshot olib, performance regression testlarida ishlatish.
- DBUnit dataset bilan murakkab bog'lanishli (FK) holatni deklarativ tasvirlab, testni qisqartirish.

**Ehtiyot bo'ling:** Oldindan qurilgan dataset vaqt o'tishi bilan sxemadan ortda qoladi va "sirli" (mysterious guest) ma'lumotga aylanadi - test nega o'tayotgani kodda ko'rinmaydi. Har bir testni bir xil katta datasetga bog'lash dataset o'zgarganda o'nlab testni bir vaqtda buzadi.

## 23.53 Dangasa Sozlash (Lazy Setup)

**Tavsif:** Fixture faqat birinchi marta haqiqatan kerak bo'lganda yaratiladi, keyin esa qayta ishlatiladi. Bu qimmat resursni hech kim so'ramasa umuman ko'tarmaslik imkonini beradi - masalan, faqat bitta test sinfi ishga tushirilganda butun infratuzilma ko'tarilmaydi. Natijada tez unit testlar og'ir integratsion fixture'dan jarima to'lamaydi.

**Spring'da qayerda uchraydi:** Spring TestContext Framework `ApplicationContext`ni test sinfi birinchi marta kerak bo'lganda ko'taradi va `ContextCache`ga qo'yadi - bu to'g'ridan-to'g'ri lazy setup. `@Lazy` bean'lar va `spring.main.lazy-initialization=true` test profilida context start vaqtini kamaytiradi. Testcontainers'da `static` konteyner maydoni JVM'da sinf birinchi yuklanganda ishga tushadi, `@Testcontainers` esa konteynerni test sinfi hayotiy davriga bog'laydi; `TestcontainersConfiguration` bilan reusable mode (`testcontainers.reuse.enable=true`) birinchi start'dan keyin konteynerni tiriklay qoldiradi.

**Qo'llanish keyslari:**
- Faqat DB testlari ishga tushganda Postgres konteynerini ko'tarish, unit testlarda esa umuman ko'tarmaslik.
- `spring.main.lazy-initialization=true` bilan `@SpringBootTest` startini sekundlarga qisqartirish.
- IDE'da bitta test metodini ishga tushirganda butun Kafka/Elasticsearch stack'i ko'tarilmasligini ta'minlash.
- Reusable Testcontainers bilan lokal development'da ketma-ket test yugurishlarini tezlashtirish.
- Og'ir mock server (WireMock) ni faqat tashqi integratsiya testlari talab qilganda start qilish.

**Ehtiyot bo'ling:** Lazy initialization bean konfiguratsiyasidagi xatolarni start vaqtidan testning o'rtasiga ko'chiradi - "fail fast" xususiyati yo'qoladi va xato sababi tushunarsiz joyda chiqadi. Parallel testlarda lazy yaratishni thread-safe qilmasa, bir nechta nusxa yoki race condition paydo bo'ladi.

## 23.54 To'plam Darajasidagi Fixture Sozlash (Suite Fixture Setup)

**Tavsif:** Fixture butun test to'plami (suite) uchun bir marta yaratiladi va oxirida bir marta yopiladi, har bir sinf yoki metod uchun emas. Bu eng qimmat resurslar - ma'lumotlar bazasi, broker, tashqi mock server - uchun maqbul strategiya. Jarayon boshida ko'tarish, oxirida tozalash aniq belgilangan nuqtalarda bajariladi.

**Spring'da qayerda uchraydi:** JUnit 5'da `@BeforeAll`/`@AfterAll` sinf darajasida, `LauncherSessionListener` yoki `TestExecutionListener` esa butun yugurish darajasida ishlaydi; `junit-platform.properties` orqali global listener ro'yxatdan o'tkaziladi. Spring'da `TestExecutionListener` (`AbstractTestExecutionListener`) va `ContextCustomizer`/`ApplicationContextInitializer` bilan to'plam darajasidagi sozlash qilinadi; `@DynamicPropertySource` bir marta ko'tarilgan konteyner URL'ini context'ga uzatadi. Testcontainers `Singleton Container` patterni (abstract base sinfdagi `static` blok) va Ryuk sidecar konteyneri JVM tugaganda tozalashni avtomatlashtiradi. Spring Boot 3.1+ `@ServiceConnection` bilan bu sozlash deklarativ ko'rinishga keladi.

**Qo'llanish keyslari:**
- Barcha integratsion testlar uchun bitta singleton Postgres + Kafka to'plamini JVM boshida ko'tarish.
- `@DynamicPropertySource` bilan konteyner portlarini bir marta hisoblab, barcha test sinflariga tarqatish.
- Global WireMock serverini suite boshida start qilib, oxirida stop qilish.
- Gradle/Maven'da test JVM'ini fork qilish strategiyasini suite fixture bilan moslab, CI vaqtini nazorat qilish.
- `LauncherSessionListener` bilan yugurish oxirida umumiy test ma'lumotlarini arxivlash yoki metrikani chiqarish.

**Ehtiyot bo'ling:** Suite darajasidagi fixture parallel test executor'lar bilan to'qnashadi - har bir fork alohida JVM bo'lgani uchun resurs bir necha marta ko'tarilishi yoki port konflikt bo'lishi mumkin. Tozalash (`@AfterAll`) bajarilmasa (JVM crash, timeout) orfan konteynerlar va ochiq ulanishlar qoladi; Ryuk yoki shutdown hook bilan himoya qilish kerak.

## 23.55 Fixture Bo'yicha Test Sinfi (Testcase Class per Fixture)

**Tavsif:** Testlar fixture holatiga qarab guruhlanadi: har bir alohida boshlang'ich holat uchun o'z test sinfi yoziladi va o'sha sinfdagi barcha testlar shu holatni ulashadi. Natijada `if`/shart bilan to'lgan sozlash kodi yo'qoladi va har bir sinf nomining o'zi holatni tasvirlaydi. Bu testlarni o'qishni va xato sababini topishni osonlashtiradi.

**Spring'da qayerda uchraydi:** JUnit 5'ning `@Nested` ichki sinflari har bir fixture uchun alohida `@BeforeEach` bilan guruh yasash uchun eng tabiiy vosita; `@DisplayName` esa holatni o'qiladigan qiladi. Spring'da har bir sinf o'z `@ActiveProfiles`, `@TestPropertySource`, `@Sql` yoki `@Import(@TestConfiguration)` to'plamiga ega bo'ladi - masalan `OrderServiceWithEmptyCartTest` va `OrderServiceWithDiscountedCartTest`. `@DataJpaTest`, `@WebMvcTest`, `@JdbcTest` kabi slice annotatsiyalari ham aslida "shu qatlam uchun fixture" bo'yicha sinf ajratishni rag'batlantiradi.

**Qo'llanish keyslari:**
- Buyurtma holatlari (NEW, PAID, SHIPPED, CANCELLED) uchun alohida test sinfi yoki `@Nested` guruh yaratish.
- Autentifikatsiyalangan va anonim foydalanuvchi ssenariylarini `@WithMockUser` bilan ikki xil sinfga ajratish.
- Bir xil servisni turli `@ActiveProfiles` (masalan `stub-payment` va `real-payment`) ostida tekshirish.
- Multi-tenant ilovada tenant mavjud/mavjud emas holatlari uchun ikki fixture sinfi tutish.
- Feature flag yoqilgan va o'chirilgan holatlarni `@TestPropertySource` bilan ajratib sinash.

**Ehtiyot bo'ling:** Har bir Spring konfiguratsiya kombinatsiyasi yangi `ApplicationContext` kaliti demak - sinflarni juda ko'p bo'lib tashlash context cache'ni to'ldiradi va test vaqti portlaydi. Fixture'lar o'zaro juda o'xshash bo'lsa, sinflar ko'payib takrorlanish (duplication) yuzaga keladi; bunda parametrlashtirilgan test (`@ParameterizedTest`) ko'proq mos keladi.

## 23.56 Test Ilgagi (Test Hook)

**Tavsif:** Ishlab chiqarish kodiga faqat test uchun mo'ljallangan kengaytirish nuqtasi qo'yiladi: almashtirilishi mumkin bo'lgan abstraksiya, inyeksiya qilinadigan bog'liqlik yoki hodisa tinglovchisi. Test shu ilgak orqali xatti-harakatni o'zgartiradi, holatni kuzatadi yoki vaqtni/tasodifni nazorat qiladi. Asosiy maqsad - kodni sinovchan (testable) qilish, uning mantiqini buzmasdan.

**Spring'da qayerda uchraydi:** `java.time.Clock` bean sifatida inyeksiya qilinishi (testda `Clock.fixed(...)`) klassik ilgak; Spring Framework'ning `ApplicationEventPublisher` va `@EventListener`/`@TransactionalEventListener` esa kuzatish nuqtasi beradi - `@RecordApplicationEvents` + `ApplicationEvents` bilan testda hodisalar tekshiriladi. `TestExecutionListener`, JUnit 5 `Extension` (`BeforeEachCallback`, `TestWatcher`), `@MockitoBean`/`@MockitoSpyBean` (Spring Boot 3.4-3.5 va Boot 4 da; undan oldin `@MockBean`/`@SpyBean`) kontekstdagi bean'ni almashtiruvchi ilgaklardir. `TaskScheduler`/`TaskExecutor`ni testda `SyncTaskExecutor` yoki `SimpleAsyncTaskScheduler` bilan almashtirish ham shu patternga kiradi.

```java
@Bean
Clock clock() { return Clock.systemUTC(); }

// testda:
@TestConfiguration
static class FixedClockConfig {
    @Bean Clock clock() {
        return Clock.fixed(Instant.parse("2026-01-01T00:00:00Z"), ZoneOffset.UTC);
    }
}
```

**Qo'llanish keyslari:**
- `Clock` bean'ini fixed qilib, muddati o'tgan obuna yoki tarif hisoblash mantiqini deterministik sinash.
- `@RecordApplicationEvents` bilan domen hodisalari to'g'ri chiqqanini tasdiqlash.
- Asinxron ishni sinash uchun `TaskExecutor`ni sinxron implementatsiyaga almashtirish.
- `UUID` yoki `Random` generatorini interfeys orqasiga olib, testda oldindan belgilangan qiymat qaytarish.
- `@MockitoSpyBean` bilan haqiqiy bean'ning bitta metodini kuzatib, chaqirilish sonini tekshirish.

**Ehtiyot bo'ling:** Faqat test uchun qo'yilgan ilgaklar ishlab chiqarish kodini test tafsilotlari bilan ifloslantiradi - `if (testMode)` kabi shartlar esa aniq anti-pattern, chunki sinalayotgan kod produktivdagidan farq qiladi. Ilgakni public API'ga chiqarish uni tasodifan real mijozlar ishlatishiga olib kelishi mumkin.

## 23.57 Orqa Eshik Manipulyatsiyasi (Back Door Manipulation)

**Tavsif:** Test holatni tizimning o'z API'si orqali emas, to'g'ridan-to'g'ri pastki qatlamga yozib yoki o'qib tayyorlaydi va tekshiradi - masalan, bazaga `INSERT`, cache'ga qiymat qo'yish, fayl tizimiga yozish. Bu uzun va sekin "oldingi eshik" yo'lini chetlab o'tib, testni qisqa va tez qiladi. Ayni paytda tizimning ichki tuzilishiga bog'liqlik kuchayadi.

**Spring'da qayerda uchraydi:** `JdbcTestUtils` (`countRowsInTable`, `deleteFromTables`) va `JdbcClient`/`JdbcTemplate` bilan to'g'ridan-to'g'ri SQL yozish/o'qish; `@Sql` skriptlari ham orqa eshik orqali holat tayyorlaydi. `TestEntityManager` (`@DataJpaTest` bilan beriladi) `persistFlushFind` kabi metodlar orqali repository qatlamini chetlab o'tadi. Kafka uchun `KafkaTemplate`/`Consumer` bilan topic'ga to'g'ridan-to'g'ri yozish-o'qish, Redis uchun `RedisTemplate`, `CacheManager.getCache(...).put(...)` bilan cache holatini qo'yish shu patternning amaliy ko'rinishlari.

**Qo'llanish keyslari:**
- Hisobot endpointini sinash uchun bazaga 10 000 qator to'g'ridan-to'g'ri `INSERT` qilish (REST orqali yaratish juda sekin bo'lar edi).
- "Muddati o'tgan token" holatini yaratish uchun bazadagi `expires_at` ustunini orqadan o'tmishga qo'yish.
- `TestEntityManager` bilan entity'ni saqlab, `flush`/`clear` qilib, lazy loading xatti-harakatini tekshirish.
- Idempotentlikni sinash uchun outbox jadvaliga qo'lda `PROCESSED` yozuv kiritish.
- Cache invalidation logikasini tekshirish uchun `CacheManager` orqali eskirgan qiymat joylash.

**Ehtiyot bo'ling:** Orqa eshik test tizimning ichki sxemasiga qattiq bog'lanib qoladi: refactoring yoki migratsiya testni yoppasiga buzadi, hamda real API validatsiyalari chetlab o'tilgani uchun amalda mumkin bo'lmagan holat yaratilib, "o'tadigan, lekin yolg'on" test paydo bo'ladi. Shu sababli acceptance testlarda emas, asosan sozlash/tekshirish tezligi muhim bo'lgan joylarda ishlatish kerak.

## 23.58 Qatlam Testi (Layer Test)

**Tavsif:** Arxitekturaning bitta qatlami (controller, service, repository, client) qolgan qatlamlardan ajratilgan holda sinaladi; qo'shni qatlamlar mock, stub yoki yengil in-memory implementatsiya bilan almashtiriladi. Bu xato joyini aniq lokalizatsiya qilish va testni tez bajarish imkonini beradi. To'liq end-to-end testlar soni esa kamayadi (test piramidasi).

**Spring'da qayerda uchraydi:** Spring Boot test slice annotatsiyalari aynan shu pattern: `@WebMvcTest` + `MockMvcTester`/`MockMvc` (web qatlami), `@WebFluxTest` + `WebTestClient`, `@DataJpaTest` + `TestEntityManager`, `@JdbcTest`, `@DataMongoTest`, `@DataRedisTest`, `@JsonTest` + `JacksonTester`, `@RestClientTest` + `MockRestServiceServer` (tashqi HTTP client qatlami). Spring Framework 6.2+ da `MockMvcTester` AssertJ uslubidagi tekshirishni beradi; Spring Cloud Contract yoki Pact esa qatlamlar orasidagi shartnomani (contract) sinab, slice testlar bir-biriga mos kelishini kafolatlaydi.

**Qo'llanish keyslari:**
- `@WebMvcTest` bilan validatsiya, status kodlar va JSON serializatsiyani service'ni ko'tarmasdan tekshirish.
- `@DataJpaTest` bilan murakkab JPQL/Specification so'rovini real (yoki Testcontainers) bazada sinash.
- `@RestClientTest` + `MockRestServiceServer` bilan tashqi to'lov provayderiga so'rov formatini tasdiqlash.
- `@JsonTest` bilan DTO'lar serializatsiya qoidalarini (sana formati, `@JsonView`) tekshirish.
- Service qatlamini oddiy JUnit + Mockito bilan Spring context'siz, millisekundlarda sinash.

**Ehtiyot bo'ling:** Har bir qatlam alohida o'tsa ham, mock'lar real xatti-harakatdan chetga chiqsa integratsiya bug'lari butunlay sezilmay qolishi mumkin - shuning uchun qatlam testlari ustiga ozgina bo'lsa ham `@SpringBootTest` yoki contract test kerak. Juda ko'p turli slice konfiguratsiyalari context cache'da yangi kontekstlar yaratib, to'plam vaqtini oshiradi.

## 23.59 Jadvalni Bo'shatish Orqali Tozalash (Table Truncation Teardown)

**Tavsif:** Test tugagach, ma'lumotlar bazasidagi jadvallar `TRUNCATE`/`DELETE` bilan to'liq bo'shatiladi, shu bilan keyingi test toza holatdan boshlanadi. Bu "qaysi yozuvni kim yaratgan" degan hisob-kitobni talab qilmaydi va qo'lda yozilgan tozalash kodidan ishonchliroq. Odatda transaction rollback imkonsiz bo'lgan hollarda (commit talab qiladigan testlar) qo'llanadi.

**Spring'da qayerda uchraydi:** `JdbcTestUtils.deleteFromTables(JdbcTemplate, String...)` va `@Sql(executionPhase = AFTER_TEST_METHOD, scripts = "cleanup.sql")` standart vositalar; `ScriptUtils` bilan truncate skriptini bajarish ham mumkin. Ko'p loyihalar `TestExecutionListener` yoki JUnit 5 `Extension` yozib, `information_schema`/`pg_tables` dan jadval ro'yxatini olib `TRUNCATE ... RESTART IDENTITY CASCADE` yuboradi. Eslatma: bu pattern Spring'ning o'zida tayyor "truncate hammasini" komponenti sifatida mavjud emas - bu ma'lumotlar bazasi darajasidagi yondashuv, Spring ilovasi unga `DataSource`/`JdbcTemplate` bean'i va test lifecycle ilgaklari orqali tayanadi. Alternativa - `@Transactional` test bilan avtomatik rollback (Spring TestContext default xatti-harakati), bu truncate'ga umuman hojat qoldirmaydi.

**Qo'llanish keyslari:**
- `@SpringBootTest(webEnvironment = RANDOM_PORT)` bilan real HTTP orqali ishlaydigan testlardan keyin bazani tozalash (rollback ishlamaydi).
- `TestRestTemplate`/`WebTestClient` bilan commit qilingan ma'lumotni testlar orasida o'chirish.
- Kafka consumer + DB yozuvini birga sinovdan o'tkazgan asinxron testlardan keyin holatni qaytarish.
- Reference jadvallarni saqlab, faqat tranzaksion jadvallarni truncate qiladigan tozalash strategiyasi qurish.
- `RESTART IDENTITY` bilan ketma-ket ID'larga tayanadigan snapshot/approval testlarni barqarorlashtirish.

**Ehtiyot bo'ling:** Noto'g'ri jadval ro'yxati bilan `TRUNCATE` ishga tushsa migratsiya qo'ygan reference ma'lumotlar ham yo'q bo'ladi va keyingi testlar sirli tarzda yiqiladi; FK bog'lanishlar tufayli `CASCADE` ishlatish esa kutilmagan jadvallarni ham bo'shatadi. Hech qachon bunday tozalashni produktiv yoki umumiy staging `DataSource`ga qaratilgan konfiguratsiya bilan ishga tushirmang.

## 23.60 Avtomatik Tozalash (Automated Teardown)

**Tavsif:** Test yaratgan har bir resurs (yozuv, fayl, topic, konteyner, ulanish) ro'yxatga olinadi va test oxirida teskari tartibda avtomatik o'chiriladi - tozalash kodi qo'lda yozilmaydi. Bu "esdan chiqib qolgan tozalash" sababli yuzaga keladigan resurs oqishi va flaky testlarni yo'q qiladi. Framework lifecycle ilgaklari bu ishni test muvaffaqiyatsiz tugaganda ham bajaradi.

**Spring'da qayerda uchraydi:** Spring TestContext Framework'ning `@Transactional` test metodlari standart holda tranzaksiyani rollback qiladi (`TransactionalTestExecutionListener`; `@Commit` bilan bu o'zgartiriladi) - bu eng keng tarqalgan avtomatik tozalash. `@DirtiesContext` buzilgan `ApplicationContext`ni cache'dan chiqarib, keyingi testga toza context beradi. Testcontainers'da Ryuk sidecar konteyner JVM tugagach barcha konteyner, network va volume'larni o'chiradi; JUnit 5 `@TempDir` esa vaqtinchalik kataloglarni avtomatik tozalaydi. `ExtensionContext.Store` ga `CloseableResource` joylash yoki `AutoCloseable` bean'lar `ApplicationContext` yopilganda tozalanishi ham shu patternga kiradi.

**Qo'llanish keyslari:**
- `@Transactional` + default rollback bilan `@DataJpaTest`larda bazani umuman tozalamaslik.
- Testcontainers Ryuk bilan CI agentida orfan Docker konteynerlar qolmasligini kafolatlash.
- `@TempDir` bilan fayl yuklash/eksport testlaridan keyin vaqtinchalik fayllarni avtomatik o'chirish.
- JUnit 5 `Extension` yozib, test yaratgan Kafka topic'lari yoki S3 obyektlarini ro'yxat bo'yicha o'chirish.
- `@DirtiesContext(classMode = AFTER_CLASS)` bilan bean holatini buzgan test sinfidan keyin context'ni tiklash.

**Ehtiyot bo'ling:** Rollback'ga tayanish `@Transactional` testlarda real commit xatti-harakatini (FK tekshiruvi, trigger, `@TransactionalEventListener(AFTER_COMMIT)`) yashiradi - bu "o'tadigan, lekin produktivda yiqiladigan" testlarga olib keladi. `@DirtiesContext`ni keragidan ortiq ishlatish context cache'ni samarasiz qilib, to'plam vaqtini bir necha barobar oshiradi.

## 23.61 Tasdiqlash Testi (Approval Test)

**Tavsif:** Kodning chiqishi (JSON, hisobot, HTML, log, diagramma) matn ko'rinishida olinib, avval inson tomonidan tasdiqlangan "approved" fayl bilan to'liq taqqoslanadi. Tasdiq fayli versiya nazoratida saqlanadi; farq chiqsa test yiqiladi va dasturchi diff'ni ko'rib yangi chiqishni tasdiqlaydi yoki bug'ni tuzatadi. Bu ko'p maydonli natijalarni bitta-bitta assert qilmasdan qamrab olishga yordam beradi (snapshot/golden master testing).

**Spring'da qayerda uchraydi:** Approval testing Spring'ning o'z imkoniyati emas - bu kutubxona darajasidagi yondashuv: `ApprovalTests` (`com.approvaltests:approvaltests`, `Approvals.verify(...)`) yoki `java-snapshot-testing`. Spring tomondan chiqish `MockMvc`/`MockMvcTester` yoki `WebTestClient` javobining tanasi (`.andReturn().getResponse().getContentAsString()`), `JacksonTester`/`ObjectMapper` serializatsiyasi, yoki `@DataJpaTest`da generatsiya qilingan SQL (Hibernate `hibernate.show_sql`/statistics) sifatida olinadi. Shuningdek `spring-restdocs` va Spring Cloud Contract yozib qo'yadigan fayllar ham approval'ga o'xshash "golden" artefaktlardir. JSON uchun `JSONAssert` (`spring-boot-starter-test` ichida) `LENIENT` rejimida moslashuvchan taqqoslash beradi.

**Qo'llanish keyslari:**
- Murakkab REST javob JSON'ini (o'nlab ichki obyekt bilan) approved fayl bilan taqqoslab, regressiyani ushlash.
- Legacy hisobot generatorini refactoring qilishdan oldin golden master snapshot olish.
- `Flyway` migratsiyalaridan keyin yakuniy sxema DDL'ini tasdiqlangan nusxa bilan solishtirish.
- PDF/CSV eksport fayl tuzilmasini matn ko'rinishiga keltirib snapshot qilish.
- OpenAPI spetsifikatsiyasi (springdoc tomonidan generatsiya qilingan) tasodifan o'zgarmaganini tekshirish.

**Ehtiyot bo'ling:** Chiqishda determinizmsiz qiymatlar (`UUID`, `Instant.now()`, tartibsiz `Set`, ketma-ket ID'lar) bo'lsa test flaky bo'ladi - ularni `Clock` bean'i, fixed generator yoki scrubber bilan normalizatsiya qilish shart. Diff'ni o'ylab ko'rmasdan "approve" bosish odati testni ma'nosiz qiladi: approval test bug'ni ushlamaydi, faqat o'zgarishni qayd etadi.

## 23.62 Test metodi va testcase sinfi (Test Method / Testcase Class)

**Tavsif:** Kitobning eng asosiy ikki patterni: har bir test bitta metod sifatida yoziladi, bir-biriga bog'liq test metodlari esa bitta sinfga guruhlanadi. Meszaros test metodining uch shablonini sanaydi: Simple Success Test (setup, exercise, verify chiziqli ketma-ketlikda), Expected Exception Test (istisno tashlanmasa test yiqiladi) va Constructor Test (obyekt yaratiladi va atributlari tekshiriladi) (Gerard Meszaros, *xUnit Test Patterns*, Addison-Wesley, 2007, 19-bob, 348-349-bet va 373-bet). Shablonni tanib olish o'quvchiga testning turini sarlavhasini o'qimasdan aytadi.

**Spring'da qayerda uchraydi:** JUnit 5 da test metodi `@Test` (yoki `@ParameterizedTest`, `@RepeatedTest`, `@TestFactory`), testcase sinfi esa oddiy sinf: `public` bo'lishi shart emas, konstruktor argumentlari `ParameterResolver` orqali to'ldiriladi. Expected Exception Test uchun JUnit 3 davridagi `try/fail/catch` o'rniga `assertThrows` yoki AssertJ `assertThatThrownBy` ishlatiladi. `@Nested` ichki sinflar bitta testcase sinfini bir nechta mantiqiy guruhga ajratadi, `@DisplayName` esa niyatni o'zbekcha matn bilan yozishga imkon beradi.

**Qo'llanish keyslari:**
- Domen qoidasining har bir shartini alohida `@Test` metodi qilib yozish va nomida kutilgan natijani ko'rsatish.
- Istisno ssenariylarini `assertThrows` bilan Expected Exception Test shaklida yozish.
- Konstruktor va factory metodining invariantlarini Constructor Test shaklida tekshirish.
- `@Nested` bilan "limit yetarli" va "limit yetmaydi" ssenariylarini bitta sinf ichida ajratish.
- Testcase sinfini SUT sinfi bilan bir paketda saqlab, package-private metodlarni ham test qilish imkonini qoldirish.

```java
class CreditLimitPolicyTest {
    private final CreditLimitPolicy policy = new CreditLimitPolicy();

    @Test
    @DisplayName("limitdan oshgan buyurtma rad etiladi")
    void rejectsOrderOverLimit() {
        var customer = new Customer("c-1", Money.of("1000", "UZS"));
        assertThatThrownBy(() -> policy.check(customer, Money.of("1500", "UZS")))
                .isInstanceOf(CreditLimitExceededException.class);
    }
}
```

**Ehtiyot bo'ling:** Bir metodda bir nechta shablonni aralashtirish (konstruktorni tekshirib, keyin biznes metodini ham sinash) Eager Test smell'iga olib keladi va qizil bo'lganda muammo joyini ko'rsatmaydi. Testcase sinfiga maydon qo'yish JUnit 5 da xavfsiz, chunki standart hayotiy davr har metod uchun yangi nusxa yaratadi, lekin `@TestInstance(PER_CLASS)` bilan bu kafolat yo'qoladi.

## 23.63 Test runner, testcase obyekti va test to'plami obyekti (Test Runner / Testcase Object / Test Suite Object)

**Tavsif:** xUnit freymvorklarining ichki mexanikasi: runner topilgan testlarni Command obyektlariga (Testcase Object) aylantiradi, ularni Composite to'plamga (Test Suite Object) yig'adi va bitta interfeys orqali yuritadi, shu bilan bitta test va ko'p qatlamli to'plam runner uchun bir xil ko'rinadi (Gerard Meszaros, *xUnit Test Patterns*, Addison-Wesley, 2007, 19-bob, 377-378-bet, 382-383-bet va 387-bet). Har test uchun alohida obyekt yaratilishi testlarni bir-biridan ajratadi. Bu uchligi birgalikda Test Automation Framework patternini tashkil qiladi: freymvork testlarni topish, to'plamga yig'ish, ketma-ket bajarish, kutilgan natijani tekshirish, xato va yiqilishlarni yig'ib hisobot berish va ularda tozalash mexanizmlarini beradi, test yozuvchi esa faqat testga xos mantiqni yozadi (o'sha kitob, 18-bob, 298-299-bet).

**Spring'da qayerda uchraydi:** JUnit 5 da bu uch pattern JUnit Platform ichida: `Launcher` runner rolini, `TestDescriptor` daraxti esa Testcase Object va Test Suite Object rolini bajaradi; `TestEngine` (jupiter, vintage, yoki jqwik) daraxtni quradi. Maven'da `maven-surefire-plugin` va `maven-failsafe-plugin` launcher'ni chaqiradi, Gradle'da `Test` task. Dasturchi bu qatlamga kamdan-kam tegadi: `TestExecutionListener` yozib natijalarni yig'ish yoki `EngineTestKit` bilan o'z extension'ini test qilish shu qatlam bilan ishlashning amaliy holatlari.

**Qo'llanish keyslari:**
- `TestExecutionListener` bilan test davomiyligini yig'ib, eng sekin testlar hisobotini chiqarish.
- `EngineTestKit` bilan o'zingiz yozgan JUnit extension'ining xatti-harakatini test qilish.
- `@Suite` (junit-platform-suite) bilan bir nechta modulning testlarini bitta to'plamga yig'ish.
- Surefire va Failsafe'ni ajratib, unit va integration to'plamlarini turli bosqichda yuritish.
- CI'da platform natija daraxtidan foydalanib flaky testlarni test darajasida hisoblash.

```java
public class SlowestTestsListener implements TestExecutionListener {
    private final Map<String, Long> started = new ConcurrentHashMap<>();

    @Override
    public void executionStarted(TestIdentifier id) {
        started.put(id.getUniqueId(), System.nanoTime());
    }

    @Override
    public void executionFinished(TestIdentifier id, TestExecutionResult result) {
        Long t0 = started.remove(id.getUniqueId());
        if (t0 != null && id.isTest()) {
            System.out.printf("%d ms %s%n", (System.nanoTime() - t0) / 1_000_000, id.getDisplayName());
        }
    }
}
```

**Ehtiyot bo'ling:** Kitobda runner va suite obyekti qo'lda yoziladigan kod sifatida tasvirlangan, JUnit 5 da esa ular freymvork ichida: bu qatlamni qo'lda qurishga urinish keraksiz ish. Listener ichida og'ir ish qilish butun to'plamni sekinlashtiradi va static holat orqali testlar orasida bog'liqlik yaratishi mumkin.

## 23.64 Testlarni topish, sanash va tanlash (Test Discovery / Test Enumeration / Test Selection)

**Tavsif:** Runner qaysi testlarni yurgizishini bilishning uch yo'li. Test Discovery da freymvork reflection bilan test metodlarini o'zi topadi; Test Enumeration da dasturchi to'plamni qo'lda yozadi; Test Selection da esa testlar atributlari bo'yicha ish vaqtida filtrlanadi (Gerard Meszaros, *xUnit Test Patterns*, Addison-Wesley, 2007, 19-bob, 393-bet, 399-bet va 403-bet). Kitobda qo'lda sanash JUnit 3 ning `suite()` metodi bilan bog'langan va Lost Test smell'ining asosiy sababi deb ko'rsatilgan.

**Spring'da qayerda uchraydi:** JUnit 5 butunlay discovery'ga o'tgan: `@Test` va boshqa annotatsiyalar metodni e'lon qiladi, `suite()` yozilmaydi. Tanlash `@Tag` va platform filtrlari bilan bajariladi: `-Dgroups=`, `-DexcludedGroups=` (Surefire), `includeTags`/`excludeTags` (Gradle), `junit.jupiter.conditions.deactivate`. Shartli o'tkazib yuborish uchun `@EnabledIf...` va `@DisabledIf...` annotatsiyalari bor; qo'lda to'plam kerak bo'lsa `junit-platform-suite` ning `@Suite` va `@SelectPackages` annotatsiyalari ishlatiladi.

**Qo'llanish keyslari:**
- `@Tag("slow")` bilan sekin testlarni PR gate'dan chiqarib, nightly build'ga qoldirish.
- `@Tag("flaky")` bilan karantin ro'yxatini kod ichida ko'rinadigan qilish.
- `@SelectPackages` bilan modul darajasidagi smoke to'plam yig'ish.
- Metod nomlash konvensiyasini buzgan testlarni topish uchun platform discovery hisobotini CI'da sanash.
- `@EnabledIfSystemProperty` bilan faqat Docker mavjud muhitda ishlaydigan testlarni ajratish.

```properties
# junit-platform.properties: tag bo'yicha tanlash standart filtri
junit.jupiter.execution.parallel.enabled=true
junit.platform.discovery.issue.severity.critical=ERROR
```

To'rtinchi, yaqin pattern - Named Test Suite: birga yurgizilishi kerak bo'lgan testlar guruhi uchun niyatni ko'rsatadigan nom bilan alohida to'plam e'lon qilinadi, masalan commit oldidan yuriladigan kichik kesim yoki butun loyihaning AllTests to'plami (Gerard Meszaros, *xUnit Test Patterns*, Addison-Wesley, 2007, 24-bob, 592-593-bet). JUnit 5 da bu `@Suite` sinfi yoki oddiygina kelishilgan `@Tag` nomi bo'ladi.

**Ehtiyot bo'ling:** Tanlash filtri noto'g'ri bo'lsa test jim o'tkazib yuboriladi va bu Lost Test smell'i: to'plam yashil, lekin test soni kamaygan. Shuning uchun CI'da test sonini o'lchab, kutilgan chegaradan pastga tushganda build'ni yiqitish kerak. `@Tag` nomlarini hujjatsiz ko'paytirish filtrlarni boshqarib bo'lmaydigan qilib qo'yadi.

## 23.65 Assertion metodi va assertion xabari (Assertion Method / Assertion Message)

**Tavsif:** Test o'zini o'zi tekshiradigan bo'lishi uchun kutilgan natija assertion metodlari chaqiruvi sifatida yoziladi; assertion xabari esa qaysi tasdiq yiqilganini aytadi. Meszaros amaliy qoida beradi: bir xil turdagi assertion metodidan birdan ko'p chaqiruv bo'lsa, hech bo'lmaganda minimal xabar qo'shiladi, aks holda Missing Assertion Message sababi orqali Assertion Roulette paydo bo'ladi (Gerard Meszaros, *xUnit Test Patterns*, Addison-Wesley, 2007, 19-bob, 362-bet va 370-371-bet).

**Spring'da qayerda uchraydi:** JUnit 5 `Assertions` sinfida xabar oxirgi argument yoki `Supplier<String>` sifatida beriladi; AssertJ da esa `as("...")` va `describedAs(...)` tasdiqni nomlaydi, `withFailMessage(...)` xabarni to'liq almashtiradi. `assertAll` bir nechta tasdiqni birga bajarib, hammasining natijasini ko'rsatadi. Spring tomonida `MockMvcTester` va `WebTestClient` AssertJ uslubidagi zanjirli tasdiqlarni beradi, `JSONAssert` esa JSON taqqoslash xabarini maydon yo'li bilan chiqaradi.

**Qo'llanish keyslari:**
- Bir obyektning uch maydonini tekshirganda har tasdiqqa `as("status")` qo'shib, qizil xabarni o'qiladigan qilish.
- `assertAll` bilan validatsiya xatolarining butun to'plamini bir yugurishda ko'rish.
- AssertJ `satisfies(...)` bilan murakkab shartni bitta nomlangan tasdiqqa yig'ish.
- `Supplier<String>` shaklidagi xabar bilan faqat yiqilganda qimmat matn yasash.
- Maxsus assertion yozib, xabarni domen tilida chiqarish.

```java
@Test
void calculatesInvoiceTotals() {
    Invoice invoice = invoiceService.build(order);
    assertAll(
            () -> assertEquals(3, invoice.lineCount(), "qatorlar soni"),
            () -> assertEquals(Money.of("450.00", "UZS"), invoice.net(), "net summa"),
            () -> assertEquals(Money.of("54.00", "UZS"), invoice.vat(), "QQS"));
}
```

**Ehtiyot bo'ling:** Xabar matnini tasdiqning o'zi bilan takrorlash (`"expected 3 but was"`) foydasiz: xabar nima tekshirilayotganini aytishi kerak, natijani freymvork o'zi chiqaradi. AssertJ da `withFailMessage` standart diffni o'chirib qo'yadi, shuning uchun odatda `as(...)` afzal.

## 23.66 Tugallanmagan test tasdigi (Unfinished Test Assertion)

**Tavsif:** Hali yozib bitirilmagan test tasodifan yashil bo'lib qolmasligi uchun uning oxiriga doim yiqiladigan tasdiq qo'yiladi. Meszaros buni odat qilishni maslahat beradi: narxi yo'q, foydasi katta, chunki yozilmagan test yashil bo'lsa u Neverfail Test ga aylanadi (Gerard Meszaros, *xUnit Test Patterns*, Addison-Wesley, 2007, 21-bob, 494-bet).

**Spring'da qayerda uchraydi:** JUnit 5 da `Assertions.fail("tugallanmagan")` shu rolni bajaradi; `assertThat(...).isNotNull()` kabi bo'sh tasdiqlar bu rolni bajarmaydi. Tugallanmagan testni belgilashning ikkinchi yo'li `@Disabled("sabab va issue")`: u testni yurgizmaydi, lekin hisobotda ko'rinadi. Uchinchi yo'l `Assumptions.abort("sabab")`, bu testni o'tkazib yuborilgan deb belgilaydi. Tanlov siyosatga bog'liq: yiqiladigan tasdiq build'ni qizil qiladi, `@Disabled` esa qarzni ko'rinadigan qiladi.

**Qo'llanish keyslari:**
- TDD da test skeletini yozib, implementatsiya boshlanmaguncha `fail` qoldirish.
- Yangi talab uchun test nomlarini oldin yozib, har biriga `fail("yozilmagan")` qo'yish.
- IDE shablonida yangi test metodiga avtomatik `fail` qo'shib qo'yish.
- Review'da `isNotNull()` dan boshqa tasdiqi yo'q testlarni tugallanmagan deb belgilash.
- Karantinga olingan testni `@Disabled` bilan emas, yiqiladigan tasdiq bilan belgilab, muddat bosimini saqlash.

```java
@Test
void refundsPartiallyShippedOrder() {
    // TODO: qaytarish qoidasi aniqlangandan keyin yoziladi (JIRA-4821)
    fail("tugallanmagan test");
}
```

**Ehtiyot bo'ling:** Tugallanmagan tasdiqni commit qilib yuborish main'ni qizil qiladi, shuning uchun bu usul lokal ish uchun; qizil main'ga chidamaydigan jamoada o'rniga sababli va egali `@Disabled` ishlatiladi. Hech qachon testni yashil qilish uchun tasdiqni butunlay olib tashlamang.

## 23.67 Holatni va xulqni tekshirish (State Verification / Behavior Verification)

**Tavsif:** Natijani tekshirishning ikki uslubi. State Verification da SUT ishlatilgandan keyin uning holati o'qiladi va kutilgan holat bilan taqqoslanadi; Behavior Verification da esa SUT o'z bog'liqliklariga qanday murojaat qilgani yozib olinadi va kutilgan chaqiruvlar bilan solishtiriladi (Gerard Meszaros, *xUnit Test Patterns*, Addison-Wesley, 2007, 21-bob, 462-463-bet va 468-469-bet). Kitob ogohlantiradi: xulq tekshiruvini ortiqcha ishlatish Overspecified Software sababi orqali Fragile Test ga olib keladi.

**Spring'da qayerda uchraydi:** State Verification Spring testlarida ustun uslub: `@DataJpaTest` da `TestEntityManager` bilan yozuvni qayta o'qish, `MockMvcTester` bilan javob tanasini tekshirish, `ApplicationContext` dan bean holatini olish. Behavior Verification Mockito bilan: `verify(repo).save(order)`, `verify(publisher, never()).publish(any())`, `ArgumentCaptor` bilan argumentni ushlab tekshirish, `InOrder` bilan tartibni tasdiqlash. `@MockitoBean` bilan qo'yilgan dublyor har ikki uslubga xizmat qiladi.

**Qo'llanish keyslari:**
- Domen hisob-kitobini State Verification bilan tekshirish: natija qiymati muhim, chaqiruvlar emas.
- Tashqi to'lov provayderiga so'rov yuborilganini Behavior Verification bilan tasdiqlash, chunki natija ko'rinmaydi.
- `ArgumentCaptor` bilan yuborilgan event tanasini tekshirib, ikki uslubni birlashtirish.
- `verify(..., never())` bilan "idempotent qayta urinishda ikkinchi debet bo'lmaydi" qoidasini tasdiqlash.
- Repository chaqiruvlarini emas, saqlangan yozuvni tekshirib, testni refaktoringga chidamli qilish.

```java
@Test
void publishesEventOnceOnRetry() {
    orderService.submit(order);
    orderService.submit(order); // idempotent qayta urinish

    ArgumentCaptor<OrderSubmitted> captor = ArgumentCaptor.forClass(OrderSubmitted.class);
    verify(publisher, times(1)).publish(captor.capture());
    assertThat(captor.getValue().orderId()).isEqualTo(order.id());
}
```

**Ehtiyot bo'ling:** Har chaqiruvni `verify` qilish testni implementatsiya nusxasiga aylantiradi: metod nomini o'zgartirsangiz test yiqiladi, xatti-harakat esa o'zgarmagan. Qoida: holatni o'qish mumkin bo'lsa State Verification, faqat ko'rinmas yon ta'sir (xabar yuborish, log, tashqi chaqiruv) uchun Behavior Verification.

## 23.68 Fixture sozlashning uch shakli (In-line Setup / Delegated Setup / Implicit Setup)

**Tavsif:** Fixture'ni qurishning uch joyi: test metodining o'zida (In-line), test metodidan chaqirilgan Creation Method'larda (Delegated) yoki freymvork avtomatik chaqiradigan `setUp` metodida (Implicit). Meszaros tanlov mezonini beradi: In-line sozlash juda sodda fixture uchun va testning birinchi qoralamasi uchun, Delegated takrorlanishni yo'qotib fixture tabiatini test ichida ko'rinadigan qoldiradi, Implicit esa bir sinfdagi barcha testlar aynan bir xil fixture talab qilganda (Gerard Meszaros, *xUnit Test Patterns*, Addison-Wesley, 2007, 20-bob, 408-409-bet, 411-412-bet va 424-425-bet).

**Spring'da qayerda uchraydi:** Implicit Setup JUnit 5 da `@BeforeEach` va `@BeforeAll`, Spring tomonida `@Sql(executionPhase = BEFORE_TEST_METHOD)`, `@TestExecutionListeners` va `@MockitoBean` ning avtomatik o'rnatilishi. Delegated Setup `src/test/java` dagi builder va `OrderMother` turidagi fabrikalar, `TestEntityManager.persistFlushFind(...)` chaqiruvlari orqali. In-line Setup esa oddiy konstruktor chaqiruvi bilan sinf maydonini to'ldirish.

**Qo'llanish keyslari:**
- Yangi testni In-line sozlash bilan yozib, uchinchi nusxadan keyin Delegated ga ko'chirish.
- `@BeforeEach` ga faqat barcha testlarga baravar kerak bo'lgan qismni qoldirish.
- Ssenariyga xos qiymatlarni (limit, summa) doim test metodining o'zida ko'rsatish.
- `@Nested` ichida lokal `@BeforeEach` yozib, guruhga xos fixture'ni ajratish.
- Bazaga tayanadigan testda umumiy reference ma'lumotni `@Sql` ga, ssenariy ma'lumotini builder'ga berish.

```java
@BeforeEach
void setUp() { // Implicit: hamma testga baravar
    policy = new CreditLimitPolicy(clock);
}

@Test
void rejectsOverLimit() {
    // Delegated: ssenariyga xos qiymatlar ko'rinib turadi
    var customer = aCustomer().withCreditLimit("1000").build();
    assertThatThrownBy(() -> policy.check(customer, Money.of("1500", "UZS")))
            .isInstanceOf(CreditLimitExceededException.class);
}
```

**Ehtiyot bo'ling:** `@BeforeEach` ga ssenariyga xos qiymat yashirsa test Mystery Guest bo'ladi: o'quvchi nega 1500 rad etilganini tushunish uchun yuqoriga qarashi kerak. Teskari xato - har testda yigirma qatorlik In-line sozlash: bu Test Code Duplication va Irrelevant Information.

## 23.69 Setup dekoratori va zanjirli testlar (Setup Decorator / Chained Tests)

**Tavsif:** Umumiy fixture'ni butun to'plam atrofida "qavs"ga olishning ikki eski yo'li. Setup Decorator to'plamni Decorator bilan o'rab, yugurishdan oldin fixture'ni quradi va tugagandan keyin buzadi; Chained Tests esa fixture'ni umuman qurmaydi va o'zidan oldin yurgan testlardan qolgan holatga tayanadi (Gerard Meszaros, *xUnit Test Patterns*, Addison-Wesley, 2007, 20-bob, 447-448-bet va 454-455-bet). Kitob Chained Tests'ni "yoki yoqtiradilar yoki yomon ko'radilar" deb ta'riflaydi va uning Interacting Tests va Lonely Test smell'lari bilan bog'liqligini ko'rsatadi.

**Spring'da qayerda uchraydi:** Setup Decorator rolini JUnit 5 da `Extension` bajaradi: `BeforeAllCallback`/`AfterAllCallback` sinf atrofida, `ExtensionContext.Store` dagi `CloseableResource` esa butun yugurish atrofida tozalashni beradi. Testcontainers'ning singleton konteyner patterni va `@Testcontainers` annotatsiyasi shu shaklni amalda ko'rsatadi. Chained Tests uchun JUnit 5 da `@TestMethodOrder(OrderAnnotation.class)` va `@TestInstance(PER_CLASS)` kerak, ya'ni tartibni ataylab e'lon qilish shart.

**Qo'llanish keyslari:**
- `Extension` yozib, butun yugurish uchun bitta konteyner yoki mock server ko'tarish.
- `ExtensionContext.Store` ga `CloseableResource` qo'yib, JVM tugaganda tozalashni kafolatlash.
- Uzun biznes ssenariysini (buyurtma yaratildi, to'landi, yetkazildi) ataylab zanjirga tizib, har bosqichni alohida tekshirish.
- Zanjirli testni faqat bitta `@Nested` sinf ichida saqlab, qolgan to'plamdan ajratish.
- Dekorator ichida fixture qurilishi muvaffaqiyatsiz bo'lsa butun to'plamni tez yiqitish.

```java
public class SharedBrokerExtension implements BeforeAllCallback {
    @Override
    public void beforeAll(ExtensionContext context) {
        context.getRoot()
               .getStore(ExtensionContext.Namespace.GLOBAL)
               .getOrComputeIfAbsent("broker", key -> new BrokerResource());
    }

    private record BrokerResource() implements ExtensionContext.Store.CloseableResource {
        @Override public void close() { /* to'plam tugagach yopiladi */ }
    }
}
```

**Ehtiyot bo'ling:** Chained Tests har qanday tartib o'zgarishida, bitta testni o'chirishda yoki uni yolg'iz yurgizishda buziladi; kitob buni Lonely Test sababi deb belgilaydi. Parallel yugurishda zanjir butunlay ishlamaydi. Dekorator esa fixture'ni butun to'plamga umumiy qiladi, ya'ni Shared Fixture ning hamma xavfini olib keladi.

## 23.70 Minimal va standart fixture (Minimal Fixture / Standard Fixture)

**Tavsif:** Minimal Fixture - har test uchun eng kichik va eng sodda fixture; Standard Fixture - bir nechta test uchun oldindan loyihalangan umumiy fixture dizayni. Meszaros Minimal Fixture'ni testni hujjat sifatida o'qish va Slow Tests'dan qutulish uchun asosiy vosita deb ataydi; Standard Fixture esa "texnologiya emas, munosabat" va aslida fixture uchun "big design upfront" (Gerard Meszaros, *xUnit Test Patterns*, Addison-Wesley, 2007, 18-bob, 302-bet va 305-306-bet). Standard Fixture dizayn qayta ishlatilishini bildiradi, Shared Fixture esa nusxa qayta ishlatilishini: har Shared Fixture Standard Fixture, teskarisi esa yo'q.

**Spring'da qayerda uchraydi:** Minimal Fixture amalda builder bilan quriladi: `anOrder().withTotal("1500").build()` faqat ssenariyga ta'sir qiladigan maydonni ko'rsatadi. Standard Fixture Spring'da ikki shaklda uchraydi: `@Sql` yoki Flyway'ning test migratsiyasi bilan yozilgan umumiy ma'lumot to'plami, va `@TestConfiguration` da e'lon qilingan standart bean to'plami. Context keshi standart konfiguratsiyalarni qayta ishlatishni rag'batlantiradi, ya'ni Standard Fixture'ni konfiguratsiya darajasida ham qo'llash foydali.

**Qo'llanish keyslari:**
- Har testga faqat kerakli entity'ni yaratib, "standart aeroport va reyslar" turidagi katta fixture'dan voz kechish.
- Loyiha bo'yicha 3-5 ta standart test konfiguratsiyasini kelishib, context keshini samarali ishlatish.
- Reference ma'lumot (valyuta, soliq stavkasi) uchun Standard Fixture, tranzaksion ma'lumot uchun Minimal Fixture ishlatish.
- Yangi test yozilganda umumiy fixture'ga maydon qo'shish o'rniga builder'da ustiga yozish.
- Fixture qurish vaqtini o'lchab, eng qimmat umumiy fixture'ni ssenariy bo'yicha bo'lish.

```java
// Minimal Fixture: faqat limit va summa ssenariyga ta'sir qiladi
Customer customer = aCustomer().withCreditLimit("1000").build();
Order order = anOrder().forCustomer(customer).withTotal("1500").build();
```

**Ehtiyot bo'ling:** Standard Fixture'ni "yangi test uchun bitta maydon qo'shaman" deb o'zgartirish boshqa testlarni yiqitadi - kitob buni Fragile Fixture sababi deb ataydi. Minimal Fixture'ni haddan tashqari qisqartirish esa teskari xatoga olib keladi: fixture SUT ning oldingi shartlarini qanoatlantirmasa test real bo'lmagan ssenariyni tekshiradi.

## 23.71 Tozalashning uch shakli (Garbage-Collected / In-line / Implicit Teardown)

**Tavsif:** Fixture'ni buzishning uch yo'li. Garbage-Collected Teardown da tozalash umuman yozilmaydi: obyektlarga havola qolmaganda ularni til mexanizmi yo'q qiladi. In-line Teardown da tozalash kodi test metodining oxirida, natija tekshirilgandan keyin turadi. Implicit Teardown da esa freymvork `tearDown` metodini har testdan keyin, test o'tdi yoki yiqildi degan farqsiz chaqiradi (Gerard Meszaros, *xUnit Test Patterns*, Addison-Wesley, 2007, 22-bob, 500-501-bet, 509-510-bet va 516-517-bet). Kitob muhim ogohlantirish beradi: xUnit a'zolarining ko'pi `setUp` xato bersa `tearDown` ni chaqirmaydi.

**Spring'da qayerda uchraydi:** Garbage-Collected Teardown JVM'da standart holat: oddiy unit testda tozalash yozilmaydi. Implicit Teardown - JUnit 5 `@AfterEach` va `@AfterAll`, Spring tomonida `@Transactional` testning avtomatik rollback'i, `@Sql(executionPhase = AFTER_TEST_METHOD)` va `@DirtiesContext`. In-line Teardown uchun `try/finally` yoki Java'ning `try-with-resources` konstruksiyasi ishlatiladi; JUnit 5 `@TempDir` va `ExtensionContext.Store` ning `CloseableResource` mexanizmi tozalashni avtomatlashtiradi.

**Qo'llanish keyslari:**
- Toza unit testda tozalash kodini umuman yozmaslik va GC'ga tayanish.
- Fayl, socket yoki `ExecutorService` kabi resurslarni `try-with-resources` bilan In-line tozalash.
- Bazaga commit qiladigan testdan keyin `@Sql` bilan Implicit tozalash.
- `@AfterEach` ichida static holatni (keshni, `ThreadLocal` ni) qaytarish.
- `setUp` yiqilishi mumkin bo'lgan joyda resursni `Store` ga qo'yib, tozalashni freymvorkka qoldirish.

```java
@Test
void writesReportFile(@TempDir Path dir) throws Exception {
    Path out = dir.resolve("report.csv");
    try (var writer = Files.newBufferedWriter(out)) { // In-line teardown
        reportService.writeTo(writer, order);
    }
    assertThat(out).content().startsWith("orderId,total");
    // @TempDir katalogni testdan keyin o'zi o'chiradi (Implicit teardown)
}
```

**Ehtiyot bo'ling:** `@BeforeEach` ichida istisno chiqsa `@AfterEach` chaqirilmasligiga tayanmang - resursni ochishni `try-with-resources` yoki extension ichiga ko'chiring, aks holda Resource Leakage boshlanadi. Static maydonda qolgan holat GC'ga tushmaydi va Interacting Tests sababi bo'ladi.

## 23.72 Tranzaksiyani qaytarish orqali tozalash (Transaction Rollback Teardown)

**Tavsif:** Test yangi tranzaksiya ochadi, fixture'ni quradi, SUT'ni ishlatadi, natijani tekshiradi va oxirida tranzaksiyani rollback qiladi, shuning uchun hech bir o'zgarish doimiy bo'lmaydi (Gerard Meszaros, *xUnit Test Patterns*, Addison-Wesley, 2007, 25-bob, 668-669-bet). Jadvalni truncate qilishga yoki yaratilgan yozuvlarni hisoblab yurishga hojat qolmaydi. Bu eng arzon tozalash, lekin eng ko'p narsani yashiradigan tozalash ham.

**Spring'da qayerda uchraydi:** Spring TestContext Framework'da `@Transactional` qo'yilgan test metodi standart holda rollback bilan tugaydi; buni `@Rollback(false)` yoki `@Commit` o'zgartiradi. `@DataJpaTest` bu xatti-harakatni avtomatik yoqadi. `TestTransaction` sinfi test ichida tranzaksiyani qo'lda tugatish va yangisini boshlash imkonini beradi, ya'ni commit'dan keyingi holatni ham tekshirish mumkin. Bu bobdagi transactional test rollback tuzoqlari bo'limi shu patternning amaliy chetga chiqishlarini batafsil yozadi.

**Qo'llanish keyslari:**
- `@DataJpaTest` da repository so'rovlarini bazani tozalamasdan ketma-ket sinash.
- Murakkab JPQL so'rovini real bazada tekshirib, ma'lumotni keyin qoldirmaslik.
- `TestTransaction.flagForCommit()` bilan commit'dan keyingi trigger va constraint ishlashini tekshirish.
- Bir nechta repository ustidagi servis metodini bitta test tranzaksiyasida sinash.
- Reference ma'lumotni migratsiyada qoldirib, faqat ssenariy yozuvlarini rollback bilan yo'qotish.

```java
@DataJpaTest
class OrderRepositoryTest {

    @Autowired private OrderRepository orders;

    @Test
        // @DataJpaTest tranzaksiyani ochadi va test oxirida rollback qiladi
    void findsOverdueOrders() {
        orders.save(anOrder().withDueDate(LocalDate.of(2020, 1, 1)).build());
        assertThat(orders.findOverdue(LocalDate.of(2020, 2, 1))).hasSize(1);
    }
}
```

**Ehtiyot bo'ling:** Rollback real commit xatti-harakatini yashiradi: deferred constraint, trigger, `AFTER_COMMIT` event listener va ikkinchi darajali keshning holati tekshirilmay qoladi. Shuningdek test tranzaksiyasi ichida ishlagan SUT o'zi tranzaksiya boshqarsa (`REQUIRES_NEW`), rollback uning yozuvlarini qaytarmaydi. HTTP orqali ishlaydigan testda rollback umuman ishlamaydi, chunki server boshqa tranzaksiyada ishlaydi.

## 23.73 Konfiguratsiyalanadigan va qattiq kodlangan test dublyori (Configurable / Hard-Coded Test Double)

**Tavsif:** Dublyorga nima qaytarishini yoki nimani kutishini aytishning ikki yo'li. Configurable Test Double qiymatlarni maydonda saqlaydi va test ularni sozlash fazasida o'rnatadi; Hard-Coded Test Double esa xatti-harakatni o'z kodiga yozib qo'yadi (Gerard Meszaros, *xUnit Test Patterns*, Addison-Wesley, 2007, 23-bob, 558-559-bet va 568-569-bet). Kitob qattiq kodlangan variantni xatti-harakat juda sodda yoki bitta testga xos bo'lganda tanlashni taklif qiladi.

**Spring'da qayerda uchraydi:** Mockito butunlay Configurable Test Double: `when(...).thenReturn(...)`, `given(...).willThrow(...)`, `doAnswer(...)`. Hard-Coded Test Double esa qo'lda yozilgan test sinfi: interfeysni amalga oshirgan `InMemoryOrderRepository` yoki `FixedRateProvider`. Spring tomonida `@MockitoBean` konfiguratsiyalanadigan dublyorni context'ga qo'yadi, `@TestConfiguration` ichidagi `@Bean` esa qo'lda yozilgan dublyorni. WireMock va `MockRestServiceServer` HTTP darajasida konfiguratsiyalanadigan dublyor beradi.

**Qo'llanish keyslari:**
- Bitta testda ikki xil javob kerak bo'lsa Mockito bilan sozlash (`thenReturn(a).thenReturn(b)`).
- Butun to'plamda bir xil ishlaydigan `Clock` yoki kurs provayderi uchun qo'lda yozilgan qattiq kodlangan dublyor.
- `Answer` bilan argumentga qarab javob qaytarish, ya'ni soddagina fake qurish.
- Qo'lda yozilgan dublyorni `@TestConfiguration` da `@Primary` bean qilib, integration testlarda tashqi tizimni almashtirish.
- Bir xil `when(...)` zanjiri o'nlab testda takrorlansa, uni qo'lda yozilgan dublyorga ko'chirish.

```java
// Hard-Coded Test Double: xatti-harakat kodga yozilgan
class FixedRateProvider implements RateProvider {
    @Override
    public BigDecimal rateFor(String currency) {
        return new BigDecimal("12500.00"); // UZS uchun qat'iy kurs
    }
}

// Configurable Test Double: test sozlash fazasida aytadi
given(rateProvider.rateFor("USD")).willReturn(new BigDecimal("12500.00"));
```

**Ehtiyot bo'ling:** Mockito `STRICT_STUBS` rejimida ishlatilmagan sozlash testni yiqitadi: bu yaxshi, chunki keraksiz sozlash Irrelevant Information. Qo'lda yozilgan dublyor real interfeys o'zgarganda kompilyatsiya bilan ogohlantiradi, lekin uning xatti-harakati real implementatsiyadan chetga chiqsa test yolg'on ishonch beradi; shu sababli unga ham kontrakt testi kerak.

## 23.74 Testga xos subklass (Test-Specific Subclass)

**Tavsif:** SUT'ning subklassi yozilib, unga faqat test uchun kerak bo'lgan control point va observation point'lar qo'shiladi: holatni ochadigan getter, ichki holatni to'g'ridan-to'g'ri o'rnatadigan setter yoki bitta metodni override qilib soddalashtirish. Dublyor test bilan birga paketlanganligi uchun SUT ning qolgan ilova uchun ko'rinishi o'zgarmaydi (Gerard Meszaros, *xUnit Test Patterns*, Addison-Wesley, 2007, 23-bob, 579-580-bet). Bu Test Logic in Production smell'idan qutulishning asosiy yo'li.

**Spring'da qayerda uchraydi:** Mockito `spy()` va `@MockitoSpyBean` shu patternning dinamik varianti: real obyekt saqlanadi, faqat ayrim metodlar almashtiriladi. Qo'lda yozish ham keng: `src/test/java` ichida `TestableOrderService extends OrderService` sinfi himoyalangan metodni ochadi. Legacy kodni testlashda Spring'ning `ReflectionTestUtils.setField(...)` bilan ichki holatni o'rnatish shu maqsadga xizmat qiladi, lekin u subklassdan ko'ra qo'polroq vosita.

**Qo'llanish keyslari:**
- `protected` hisoblash metodini ochib, uni to'g'ridan-to'g'ri test qilish.
- Tashqi tizimga murojaat qiladigan bitta `protected` metodni override qilib, qolgan mantiqni real qoldirish.
- Legacy sinfning ichki holatini test uchun o'rnatib, uni to'liq hayotiy davrdan o'tkazmaslik.
- `@MockitoSpyBean` bilan context'dagi real bean'ning bitta metodini almashtirish.
- Abstract SUT uchun minimal test implementatsiyasi yozib, shartnomani tekshirish.

```java
// src/test/java: testga xos subklass control point qo'shadi
class TestableOrderService extends OrderService {
    private boolean notified;

    TestableOrderService(OrderRepository repo) { super(repo, null); }

    @Override
    protected void notifyWarehouse(Order order) { notified = true; }

    boolean wasWarehouseNotified() { return notified; }
}
```

**Ehtiyot bo'ling:** Testga xos subklass SUT ni `final` bo'lmasligiga va metodlarini override qilish mumkin bo'lishiga majbur qiladi, bu esa dizayn qarori: ko'pincha to'g'ri yechim bog'liqlikni ajratib injection qilish. Override qilingan metod ichidagi haqiqiy mantiq hech qachon test qilinmasligi mumkin, shuning uchun u imkon qadar bo'sh va mexanik bo'lishi kerak. Subklass override qiladigan nuqtani legacy sinfda yo'qdan yasash uchun [chaqiruvni ajratib override qilish](#2386-chaqiruvni-ajratib-override-qilish-extract-and-override-call--factory-method--getter) va [maydonni testda almashtirish](#2387-maydonni-testda-almashtirish-supersede-instance-variable) ishlatiladi.

## 23.75 Test utility metodi va test helper (Test Utility Method / Test Helper)

**Tavsif:** Birdan ko'p testda uchragan mantiq nomlangan utility metodga ko'chiriladi; bir nechta test sinfiga kerak bo'lsa esa alohida Test Helper sinfiga joylashtiriladi va static chaqiruv yoki maxsus yaratilgan nusxa orqali ishlatiladi (Gerard Meszaros, *xUnit Test Patterns*, Addison-Wesley, 2007, 24-bob, 599-bet va 643-bet). Kitob utility metodlarning turlarini sanaydi, ular orasida SUT API Encapsulation ham bor: u Interface Sensitivity ga qarshi eng yaxshi himoya.

**Spring'da qayerda uchraydi:** Spring Boot test starter'i tayyor helper'lar beradi: `JdbcTestUtils`, `ReflectionTestUtils`, `TestSocketUtils`, `JacksonTester`, `TestEntityManager`. Loyiha tomonida `src/test/java` ichida `OrderFixtures`, `JsonFixtures` turidagi sinflar yoziladi; AssertJ uchun `Assertions` ni kengaytirgan `OrderAssertions` helper'i. Helper'ni `@TestConfiguration` da bean qilib e'lon qilish uni Spring testlariga inject qilish imkonini beradi. `src/test/java` dagi kodni modullar orasida ulashish uchun Maven `test-jar` yoki Gradle `testFixtures` konfiguratsiyasi ishlatiladi.

**Qo'llanish keyslari:**
- `authenticatedAs("admin")` turidagi metod bilan security kontekstini bir qatorda tayyorlash.
- SUT ning uzun API chaqiruvini bitta nomlangan metodga yashirib, API o'zgarganda bitta joyni tuzatish.
- JSON fixture'larini fayldan o'qiydigan `loadJson("order-created.json")` helper'i.
- `testFixtures` konfiguratsiyasi bilan builder'larni modul chegarasidan o'tkazib ishlatish.
- Tez-tez takrorlanadigan tekshiruvni maxsus AssertJ assertion'iga ko'chirish.

```java
public final class SecurityTestSupport { // Test Helper
    private SecurityTestSupport() {}

    public static RequestPostProcessor asAdmin() { // Test Utility Method
        return SecurityMockMvcRequestPostProcessors.user("admin").roles("ADMIN");
    }
}
```

**Ehtiyot bo'ling:** Helper'lar nomsiz "util" to'planmasiga aylansa Reinventing the Wheel boshlanadi: dasturchi mavjud metodni topa olmay o'zi yozadi. Shuning uchun helper'lar mavzu bo'yicha nomlanadi va topilishi oson joyda turadi. Helper ichida shart va tsikl ko'paysa u Untestable Test Code bo'ladi, ya'ni testning o'zi testga muhtoj bo'lib qoladi.

## 23.76 Test superklassi (Testcase Superclass)

**Tavsif:** Qayta ishlatiladigan test mantiqi abstract superklassga ko'chiriladi, metodlar subklasslarga ko'rinadigan qilinadi va bu sinf mantiqqa muhtoj barcha test sinflari uchun baza bo'ladi (Gerard Meszaros, *xUnit Test Patterns*, Addison-Wesley, 2007, 24-bob, 638-639-bet). Kitob uni Test Helper bilan solishtiradi: superklass mantiqni chaqirishni osonlashtiradi, lekin merosni sarflaydi, chunki Java'da bitta superklass bor.

**Spring'da qayerda uchraydi:** Spring testlarida bu pattern eng ko'p ishlatiladigan shakl: `abstract class AbstractIntegrationTest` sinfiga `@SpringBootTest`, konteyner e'lonlari va `@DynamicPropertySource` yoziladi, barcha integration testlar undan meros oladi. Shu bilan context keshi ham samarali bo'ladi, chunki konfiguratsiya bitta. Zamonaviy alternativa - merosdan voz kechib, meta-annotatsiya (`@IntegrationTest` deb nomlangan o'z annotatsiyangiz) yoki `@ExtendWith` orqali extension ulash; JUnit 5 da bitta sinfga bir nechta extension qo'shish mumkin, superklass esa bitta.

**Qo'llanish keyslari:**
- Barcha integration testlar uchun bitta `AbstractIntegrationTest` bazasi va bitta context konfiguratsiyasi.
- Konteyner e'lonlarini bazaga yig'ib, har testda takrorlamaslik.
- Umumiy `@BeforeEach` tozalash mantiqini bazaga chiqarish.
- Bazadan voz kechib, uni meta-annotatsiyaga aylantirish va merosni bo'shatish.
- Security testlari uchun alohida baza: autentifikatsiya qilingan `MockMvc` tayyorlaydi.

```java
@SpringBootTest
@Testcontainers
public abstract class AbstractIntegrationTest {

    @Container
    @ServiceConnection
    static final PostgreSQLContainer<?> POSTGRES = new PostgreSQLContainer<>("postgres:16");

    @Autowired protected TestEntityManager entityManager;
}
```

**Ehtiyot bo'ling:** Superklass o'sib ketsa u General Fixture ga aylanadi: har test sinfi uning 10 foizini ishlatadi, qolgani vaqtni yeydi. Merosdan foydalanish bitta slotni band qiladi, shuning uchun uni faqat context konfiguratsiyasi uchun saqlab, qolgan mantiqni helper yoki extension'ga bering. Chuqur ierarxiya (uch darajali test bazasi) testni o'qib bo'lmaydigan qiladi.

## 23.77 Test sinfini sinf va feature bo'yicha tashkil qilish (Testcase Class per Class / per Feature)

**Tavsif:** Test metodlarini sinflarga guruhlashning ikki mezoni. Testcase Class per Class da har SUT sinfi uchun bitta test sinfi yoziladi; Testcase Class per Feature da esa testlar SUT ning qaysi xususiyatini tekshirishiga qarab guruhlanadi, bu esa test sinflarini kichraytiradi va bir feature uchun barcha shartlarni bir qarashda ko'rsatadi (Gerard Meszaros, *xUnit Test Patterns*, Addison-Wesley, 2007, 24-bob, 617-618-bet va 624-625-bet). Kitob sinf bo'yicha guruhlashni boshlang'ich nuqta deb ataydi va test soni o'sgach bo'lishni taklif qiladi. Uchinchi mezon, fixture bo'yicha guruhlash, bu bobda alohida bo'limda yozilgan.

**Spring'da qayerda uchraydi:** JUnit 5 da feature bo'yicha guruhlash uchun alohida fayl ochish shart emas: `@Nested` ichki sinflari bitta faylda `OrderServiceTest.Submission`, `OrderServiceTest.Cancellation` kabi guruhlarni beradi va har biri o'z `@BeforeEach` iga ega bo'ladi. `@DisplayName` bilan guruh nomi hisobotda o'zbekcha chiqadi. Maven Surefire standart holda `*Test.java` va `*Tests.java` naqshlarini oladi, `@Nested` sinflar esa alohida nom talab qilmaydi.

**Qo'llanish keyslari:**
- Kichik sinf uchun bitta `XTest` fayli bilan boshlash.
- Test soni 20 dan oshganda `@Nested` guruhlarga bo'lish: feature bo'yicha.
- Har `@Nested` guruhga o'z fixture'ini berib, General Fixture dan qutulish.
- Hisobotda guruh nomini `@DisplayName` bilan talab tiliga yaqinlashtirish.
- Katta servis sinfining har metodiga alohida test fayli emas, alohida `@Nested` guruh berish.

```java
class OrderServiceTest {

    @Nested
    @DisplayName("buyurtma yuborish")
    class Submission {
        @Test void rejectsOverCreditLimit() { /* ... */ }
        @Test void acceptsWithinCreditLimit() { /* ... */ }
    }

    @Nested
    @DisplayName("buyurtmani bekor qilish")
    class Cancellation {
        @Test void rejectsCancelAfterShipment() { /* ... */ }
    }
}
```

**Ehtiyot bo'ling:** Feature bo'yicha bo'lish bitta SUT sinfi uchun testlarni bir nechta faylga sochib yuborishi mumkin: "bu sinfning testlari qayerda" savoliga javob qiyinlashadi, shuning uchun `@Nested` bir fayl ichida qolishi afzal. Guruhlash mezonini aralashtirish (bir joyda feature, boshqa joyda fixture) to'plamni tartibsiz qiladi.

## 23.78 Baza qumloqi (Database Sandbox)

**Tavsif:** Har bir dasturchi va har bir test yugurishiga o'z, mustaqil baza nusxasi beriladi, shunda kim qanday o'zgartirish qilsa ham boshqalarning testlariga ta'sir qilmaydi (Gerard Meszaros, *xUnit Test Patterns*, Addison-Wesley, 2007, 25-bob, 650-651-bet). Kitob buni bazaga sezilarli darajada tayanadigan har qanday ilovada qo'llashni maslahat beradi va bu Test Run War smell'iga qarshi asosiy himoya.

**Spring'da qayerda uchraydi:** Bugungi amalda qumloq konteyner bilan beriladi: har test sinfi yoki har yugurish uchun o'z Postgres konteyneri, Spring Boot tomonida `@ServiceConnection` yoki `@DynamicPropertySource` bilan ulanadi. Ikkinchi shakl - bitta serverda har foydalanuvchiga alohida schema yoki alohida baza: `spring.jpa.properties.hibernate.default_schema` yoki alohida `DataSource` URL. Flyway yoki Liquibase migratsiyalari qumloqni yaratilgandan keyin bir xil holatga keltiradi. Bu bobdagi Testcontainers bo'limi ulash mexanikasini batafsil beradi.

**Qo'llanish keyslari:**
- CI'da har build uchun yangi konteyner ko'tarib, build'lar orasidagi ta'sirni yo'q qilish.
- Parallel modullar uchun har moduldan alohida konteyner yoki alohida schema.
- Lokal ishlab chiqishda dasturchiga o'z bazasini berib, umumiy dev bazasidan voz kechish.
- Migratsiyalarni toza qumloqda yurgizib, ularning idempotentligini tekshirish.
- Bir nechta ijarachi (tenant) uchun schema darajasidagi ajratishni test bilan tasdiqlash.

```yaml
# application-test.yml: qumloq ulanishi dinamik beriladi, qat'iy yozilmaydi
spring:
  jpa:
    hibernate:
      ddl-auto: validate
  flyway:
    enabled: true
    clean-disabled: false
```

**Ehtiyot bo'ling:** Umumiy staging bazasini "qumloq" deb ishlatish eng tipik xato: u Test Run War, Unrepeatable Test va Data Sensitivity ning bir vaqtda manbai. Har test sinfi uchun yangi konteyner ko'tarish esa to'plamni sekinlashtiradi, shuning uchun odatda bitta konteyner butun yugurishga beriladi va izolyatsiya tranzaksiya yoki schema darajasida qilinadi.

## 23.79 Stored procedure testi (Stored Procedure Test)

**Tavsif:** Bazada yozilgan har bir jiddiy stored procedure va funksiya uchun klient ilovasidan mustaqil avtomatik test yoziladi; test turi protseduraning tabiatiga qarab qatlam kesib o'tuvchi yoki aylanma (round-trip) bo'ladi (Gerard Meszaros, *xUnit Test Patterns*, Addison-Wesley, 2007, 25-bob, 654-655-bet). Mantiq bazada bo'lsa, u ham kod va ham testga muhtoj.

**Spring'da qayerda uchraydi:** Java tomondan chaqirish uchun `SimpleJdbcCall`, `JdbcTemplate.execute(...)` yoki JPA `@NamedStoredProcedureQuery` va `StoredProcedureQuery`. Test muhiti real PostgreSQL bo'lishi shart, chunki PL/pgSQL embedded bazada ishlamaydi: shu sababli konteyner ishlatiladi. Migratsiya vositasi (Flyway) protsedurani ham versiyalaydi, ya'ni test protseduraning aynan joriy versiyasini sinaydi. Sof SQL darajasidagi testlar uchun pgTAP yoki oddiy `@Sql` skriptlari ham ishlatiladi.

**Qo'llanish keyslari:**
- Hisob-kitob qiladigan PL/pgSQL funksiyasini chegara qiymatlar bilan sinash.
- Trigger va constraint o'zaro ishini commit qilinadigan testda tekshirish.
- Protsedura migratsiyadan keyin o'zgarmaganini `@Sql` fixture va tasdiq bilan qayd etish.
- Katta ko'chirish (batch) protsedurasini kichik ma'lumot to'plamida sinab, natija yozuvlarini tekshirish.
- Protsedura xato holatida qanday istisno qaytarishini `assertThatThrownBy` bilan tasdiqlash.

```java
@Test
void calculatesVatInDatabase() {
    SimpleJdbcCall call = new SimpleJdbcCall(jdbcTemplate)
            .withFunctionName("calc_vat")
            .declareParameters(new SqlParameter("p_net", Types.NUMERIC));

    BigDecimal vat = call.executeFunction(BigDecimal.class, new BigDecimal("450.00"));

    assertThat(vat).isEqualByComparingTo("54.00");
}
```

**Ehtiyot bo'ling:** Bazadagi mantiq odatda tranzaksiya rollback'i bilan tozalanadi, lekin protsedura o'zi commit qilsa yoki avtonom tranzaksiya ishlatsa rollback ishlamaydi va jadvalni truncate qilish kerak bo'ladi. Bazaga ko'p mantiq ko'chirish uni testlash va versiyalashni qiyinlashtiradi: bu pattern mavjud mantiqni qoplaydi, yangi mantiqni bazaga ko'chirishga ruxsat emas.

## 23.80 Bog'liqlikni izlash (Dependency Lookup)

**Tavsif:** SUT o'ziga kerakli obyektni o'zi so'rab oladi: bog'liqlik sinfining nomi kodga yozilmaydi, buning o'rniga "komponent broker" nomi yozilib, undan tayyor obyekt so'raladi va broker testda boshqa obyektni qaytarishi mumkin (Gerard Meszaros, *xUnit Test Patterns*, Addison-Wesley, 2007, 26-bob, 686-687-bet). Bu Dependency Injection ning qarama-qarshisi: nazorat SUT qo'lida qoladi.

**Spring'da qayerda uchraydi:** Spring'da lookup shakllari bor, lekin ular istisno: `ApplicationContextAware` va `BeanFactoryAware` bilan context'ni olib `getBean(...)` chaqirish, `ObjectProvider<T>` bilan kech va ixtiyoriy bog'liqlikni olish, `@Lookup` metodi bilan har chaqiruvda yangi prototype bean olish. Testda lookup'ni almashtirish uchun `@MockitoBean` context'dagi bean'ni o'zgartiradi, ya'ni `getBean(...)` dublyorni qaytaradi. Spring'ning o'z hujjatlari va bu hujjatning field injection yozuvi konstruktor injection'ni standart deb belgilaydi, lookup esa faqat scope nomuvofiqligi uchun qoladi.

**Qo'llanish keyslari:**
- Singleton bean ichida prototype bean kerak bo'lsa `@Lookup` yoki `ObjectProvider` bilan olish.
- Ixtiyoriy bog'liqlikni `ObjectProvider.getIfAvailable()` bilan olib, `@Autowired(required = false)` dan qutulish.
- Dinamik tanlov: strategiya nomiga qarab `Map<String, Strategy>` dan implementatsiya olish.
- Legacy kodda `ServiceLocator` ni testda almashtirib, bog'liqlikni ajratish.
- Konteynerdan tashqarida yaratilgan obyektga bean berish uchun context'ni lookup qilish.

```java
@Component
public class ReportScheduler {

    private final ObjectProvider<ReportJob> jobs; // lookup, injection emas

    public ReportScheduler(ObjectProvider<ReportJob> jobs) { this.jobs = jobs; }

    public void runOnce(String reportId) {
        jobs.getObject().execute(reportId); // har chaqiruvda yangi prototype
    }
}
```

**Ehtiyot bo'ling:** Lookup SUT'ni konteynerga bog'laydi: `getBean(...)` ishlatgan sinfni Spring'siz unit test qilish uchun context yoki mock context kerak bo'ladi, bu esa Hard-to-Test Code sababi. Shuning uchun standart tanlov konstruktor injection, lookup esa faqat scope mos kelmaganda. `ApplicationContextAware` ni domen sinfiga qo'yish arxitektura xatosi: infratuzilma domen ichiga kirib keladi.

## 23.81 Test qiymatlari: literal, hosila va generatsiya (Literal Value / Derived Value / Generated Value)

**Tavsif:** Testda qiymat tanlashning uch yo'li. Literal Value - qo'lda hisoblangan va kodga yozilgan doimiy; Derived Value - boshqa qiymatlardan ifoda bilan hisoblangan qiymat, bu qiymatlar orasidagi bog'liqlikni ko'rinadigan qiladi; Generated Value - test yugurganda yasaladigan qiymat, masalan bazada noyob bo'lishi kerak bo'lgan maydon uchun (Gerard Meszaros, *xUnit Test Patterns*, Addison-Wesley, 2007, 27-bob, 714-bet, 718-bet va 723-bet). Kitob literal qiymatlarning Obscure Test ga olib kelishini va generatsiya qilingan qiymatlar Unrepeatable Test ga qarshi ishlashini ko'rsatadi.

**Spring'da qayerda uchraydi:** Literal qiymatlar `@ParameterizedTest` bilan `@CsvSource` va `@ValueSource` orqali jadvalga chiqariladi. Derived Value JUnit 5 da oddiy Java ifodasi, yoki `@MethodSource` da hisoblangan argument to'plami. Generated Value uchun `UUID.randomUUID()`, `AtomicLong` hisoblagich, Datafaker yoki Instancio; Spring tomonida `TestSocketUtils` bo'sh port beradi, `@DynamicPropertySource` esa konteyner bergan port va URL ni qiymat sifatida uzatadi. Noyoblikni kafolatlash kerak bo'lsa generatsiya qilingan qiymat eng arzon yechim.

**Qo'llanish keyslari:**
- Soliq hisoblashda kutilgan qiymatni `net.multiply(RATE)` deb yozib, bog'liqlikni ko'rsatish.
- Unique constraint'li email maydonini `UUID` prefiksi bilan generatsiya qilib, testlarni qayta yugurtiriladigan qilish.
- Chegara qiymatlarni `@CsvSource` jadvalida literal shaklda saqlab, niyatni ko'rsatish.
- Sana bilan ishlaganda `clock.instant().plus(30, DAYS)` deb hosila qiymat yasash.
- Generatsiya qilingan qiymat seed'ini loglab, yiqilgan testni qayta tiklash imkonini qoldirish.

```java
@ParameterizedTest
@CsvSource({"1000, 1500, true", "1000, 900, false"}) // Literal Value jadvali
void appliesCreditLimit(String limit, String total, boolean rejected) {
    var customer = aCustomer().withCreditLimit(limit).build();
    var order = anOrder().forCustomer(customer).withTotal(total).build();
    // Derived Value: kutilgan qoldiq ifoda bilan hisoblanadi
    Money expected = Money.of(limit, "UZS").minus(Money.of(total, "UZS"));
    assertThat(policy.isRejected(customer, order)).isEqualTo(rejected);
    if (!rejected) assertThat(policy.remaining(customer, order)).isEqualTo(expected);
}
```

**Ehtiyot bo'ling:** Hosila qiymat SUT ning hisob-kitobini test ichida takrorlasa test hech narsa tekshirmaydi: kutilgan natija mustaqil yo'l bilan olinishi kerak. Generatsiya qilingan qiymat esa determinizmni buzadi va Nondeterministic Test sababi bo'ladi: seed'ni fiksirlang yoki faqat natijaga ta'sir qilmaydigan maydonlarni generatsiya qiling.

## 23.82 Yozib olingan test va skript test (Recorded Test / Scripted Test)

**Tavsif:** Testni avtomatlashtirishning ikki asosiy strategiyasi. Recorded Test da asbob ilova bilan o'zaro ishni yozib oladi va keyin qayta o'ynatadi; Scripted Test da esa test programma sifatida qo'lda yoziladi (Gerard Meszaros, *xUnit Test Patterns*, Addison-Wesley, 2007, 18-bob, 278-279-bet va 285-bet). Kitob yozib olingan testlarning asosiy muammosini aniq ko'rsatadi: ularning ko'pi Obscure Test, chunki asbob o'quvchi uchun nima muhimligini bilmaydi, va ular Interface Sensitivity ga eng moyil.

**Spring'da qayerda uchraydi:** Bu hujjatdagi hamma misol Scripted Test: JUnit 5 kodida qo'lda yozilgan test. Recorded Test bugun brauzer darajasida uchraydi: Playwright codegen yoki Selenium IDE yozib beradigan skriptlar. Yuklama testlarida HTTP trafikni yozib olib qayta o'ynatish ham shu strategiya. Spring tomonida yozib olishga yaqin shakl - `spring-restdocs` va Spring Cloud Contract: ular testdan artefakt yozib oladi, teskarisi emas, shuning uchun Obscure Test xavfi yo'q.

**Qo'llanish keyslari:**
- Yangi E2E ssenariysining qoralamasini codegen bilan yozib olib, keyin uni qo'lda tartibga solish.
- Legacy UI uchun vaqtinchalik regressiya to'ri qurish, keyin testlarni pastki qatlamga ko'chirish.
- Yozib olingan skriptdan Page Object'lar ajratib, Interface Sensitivity ni kamaytirish.
- Real trafikni yozib olib, uni yuklama testi profiliga aylantirish.
- Scripted testni standart qilib belgilab, yozib olinganlarni faqat kirish nuqtasi sifatida ruxsat berish.

```java
// Scripted Test: niyat kodda ko'rinadi, selektor emas
@Test
void customerCompletesCheckout() {
    checkoutPage.open()
                .addItem("SKU-1", 2)
                .applyCoupon("WELCOME10")
                .submit();
    assertThat(orderRepository.findLatest()).extracting(Order::status)
            .isEqualTo(OrderStatus.PAID);
}
```

**Ehtiyot bo'ling:** Yozib olingan testni "tezda ko'p qoplama" deb saqlab qolish uzoq muddatda eng qimmat yo'l: UI ning har kichik o'zgarishi yuzlab testni yiqitadi va ularning hech biri nimani tekshirayotganini aytmaydi. Yozib olinganni qoldirish kerak bo'lsa, uni refaktoring qilib niyatni ko'rsatadigan qatlam qo'shing.

## 23.83 Ma'lumotga asoslangan test (Data-Driven Test)

**Tavsif:** Testning umumiy mantiqi interpretatorga chiqariladi, testdan testga o'zgaradigan ma'lumot esa faylda saqlanadi: interpretator faylni o'qib, har qator uchun to'rt fazani bajaradi (Gerard Meszaros, *xUnit Test Patterns*, Addison-Wesley, 2007, 18-bob, 288-289-bet). Bu dasturlash bilmaydigan odam ham test qo'shishi mumkin bo'lgan yagona shakl va Test Code Duplication ga qarshi kuchli vosita.

**Spring'da qayerda uchraydi:** JUnit 5 `@ParameterizedTest` bu patternning tayyor shakli: `@CsvFileSource` tashqi CSV faylini o'qiydi, `@MethodSource` esa argumentlarni koddan yasaydi, `ArgumentsProvider` bilan o'z manbangizni (JSON, baza, YAML) ulash mumkin. Mijoz bilan ishlashda Cucumber yoki Spring Cloud Contract ning YAML/DSL fayllari ham shu patternga kiradi. Spring tomonida `@Sql` skriptlari fixture ma'lumotini faylga chiqarishning oddiy shakli.

**Qo'llanish keyslari:**
- Soliq va chegirma jadvalini CSV faylga chiqarib, biznes egasiga qator qo'shish imkonini berish.
- Valyuta konvertatsiyasi chegaralarini `@CsvFileSource` bilan yuzlab holatda sinash.
- Validatsiya qoidalarining to'liq matritsasini bitta parametrlangan testda qamrash.
- `ArgumentsProvider` yozib, test holatlarini bazadan yoki JSON fayldan olish.
- `@DisplayName` shablonida qator qiymatlarini ko'rsatib, qizil testni darhol taniydigan qilish.

```java
@ParameterizedTest(name = "{0} UZS -> QQS {1}")
@CsvFileSource(resources = "/fixtures/vat-cases.csv", numLinesToSkip = 1)
void calculatesVatFromTable(String net, String expectedVat) {
    assertThat(vatCalculator.vatFor(Money.of(net, "UZS")))
            .isEqualTo(Money.of(expectedVat, "UZS"));
}
```

**Ehtiyot bo'ling:** Ma'lumot faylga chiqarilgandan keyin test Mystery Guest bo'lish xavfi paydo bo'ladi: kod faylni ko'rsatadi, lekin nima tekshirilayotgani ko'rinmaydi. Shuning uchun fayl testga yaqin tursin, ustun nomlari bo'lsin va `name` shablonida qiymatlar hisobotda chiqsin. Interpretatorga shart va tsikl ko'chsa u Untestable Test Code bo'ladi.

## 23.84 Global murojaatni testga ochish (Encapsulate Global References / Replace Global Reference with Getter)

**Tavsif:** Global holatga tayangan kodni test ostiga olishning uch yo'li bor: globalni test paytida boshqacha ishlashga majbur qilish, boshqa globalga ulanish, yoki globalni kapsullab bog'liqlikni uzish. Uchinchi yo'l ikki texnikaga bo'linadi. **Encapsulate Global References** doim birga ishlatiladigan globallarni bitta yangi sinfga yig'adi, keyin o'sha sinf nusxasini konstruktor orqali uzatadi; kitobning qoidasi shu: agar bir nechta global doim birga o'qilsa yoki birga o'zgartirilsa, ular bir sinfga tegishli. **Replace Global Reference with Getter** har bir global murojaat uchun sinf ichida `protected` getter yozadi, sinf ichidagi hamma murojaatni getter ga o'tkazadi, keyin testga xos subklass getter ni override qiladi (Feathers, *Working Effectively with Legacy Code*, Prentice Hall PTR, 2004 (copyright 2005), 25-bob, 339 va 399-bet). Ikkisi ham xatti-harakatni saqlaydigan mexanik qadam: mantiq ko'chmaydi, faqat murojaat yo'li o'zgaradi. Kitob tanlash mezonini ham beradi: bitta global ustida sinf ichida ko'p xil chaqiruv bo'lsa getter arzonroq, bitta chaqiruv bo'lsa chaqiruvni ajratib override qilish yetadi (o'sha kitob, 25-bob, 349-bet). Kitobdagi birinchi misol C++ da, g'oya quyida Java ga o'tkazilgan.

**Spring'da qayerda uchraydi:** Java da "global" ko'pincha statik holder sinfi: `SecurityContextHolder.getContext()`, `LocaleContextHolder.getLocale()`, `TransactionSynchronizationManager`, legacy `ConfigHolder.get(...)` yoki o'z `SpringContextHolder` i. Yakuniy manzil - bu murojaatlarni bean ga aylantirib konstruktor injection qilish, lekin testsiz kodda birdan o'tish xavfli: getter oraliq qadam bo'ladi va bitta kommitda butun sinfni ochadi. Kapsullashning Spring dagi tabiiy natijasi - `@ConfigurationProperties` sinfi (tarqoq `System.getProperty` chaqiruvlari o'rniga) yoki `Clock` bean i (`LocalDate.now()` o'rniga). Getter ni override qilish uchun sinf va metod `final` bo'lmasligi kerak, shu sabab sinf CGLIB proxy uchun ham mos qoladi.

**Qo'llanish keyslari:**
- Legacy servisdagi `SecurityContextHolder` chaqiruvlarini `protected AuthenticatedUser currentUser()` getter iga yig'ib, testda uni override qilish.
- Birga ishlatiladigan `ConfigHolder.region()` va `ConfigHolder.tenant()` globallarini bitta `TenantContext` sinfiga kapsullab, keyin uni konstruktorga uzatish.
- Tarqoq `System.getenv("PAYMENT_URL")` murojaatlarini bitta `PaymentSettings` sinfiga yig'ib, keyin `@ConfigurationProperties` ga o'tkazish.
- Statik `CacheHolder.instance()` murojaatini getter ortiga olib, testda in-memory implementatsiya qaytarish.
- Getter ni ochgandan keyin uni konstruktor parametriga aylantirib, testga xos subklassni butunlay yo'q qilish.

```java
public class InvoiceService {
    public Invoice issue(Order order) {
        // avval: ConfigHolder.region() to'g'ridan-to'g'ri chaqirilgan edi
        return new Invoice(order, vatRateFor(currentRegion()));
    }

    // testda override qilinadigan seam: tanasi bitta qator va mantiqsiz
    protected String currentRegion() {
        return ConfigHolder.region();
    }
}
```

**Ehtiyot bo'ling:** Getter oraliq holat, manzil emas: u bog'liqlikni ko'rinadigan qiladi, lekin konstruktor imzosiga chiqarmaydi, shuning uchun sinf tashqaridan hali ham "bog'liqliksiz" ko'rinadi. Getter tanasiga shart yoki hisob qo'shilsa, override qilingan testda u hech qachon bajarilmaydi va qoplama yolg'on bo'ladi. Globallarni bitta sinfga yig'ishda nom bilan ovora bo'lmang: kitob nomni keyin o'zgartirish mumkinligini aytadi, lekin mantiqni yangi sinfga ko'chirishni testlar paydo bo'lgandan keyinga qoldirishni talab qiladi.

## 23.85 Statik metodni test uchun ochish (Expose Static Method / Introduce Instance Delegator / Introduce Static Setter)

**Tavsif:** Sinfni test harness ichida yaratib bo'lmasa yoki uning statik chaqiruvini almashtirish kerak bo'lsa, uch mexanik texnika bor (Feathers, *Working Effectively with Legacy Code*, Prentice Hall PTR, 2004 (copyright 2005), 25-bob, 345, 369 va 372-bet).

- **Expose Static Method:** metod instance maydon va instance metodga tegmasa, uning tanasi `static` metodga ajratiladi va sinfni yaratmasdan test qilinadi. Kitobning dalili: sinfning statik qismi aslida sinfga tegishli emas, shuning uchun `static` qilish inkapsulyatsiyani buzmaydi, aksincha metod private holatga tegmasligini kompilyator bilan isbotlaydi. Yangi nom kerak bo'ladi, odatda parametr nomidan olinadi (`validate(Packet)` -> `validatePacket(Packet)`).
- **Introduce Instance Delegator:** faqat statik metodlardan iborat utility sinfga o'sha statikka delegat qiladigan instance metod qo'shiladi, chaqiruvchi esa sinf nomi orqali emas, obyekt orqali chaqiradi. Shunda object seam paydo bo'ladi. Vaqt o'tib hamma chaqiruv delegat orqali o'tsa, statik tanalar instance metodga ko'chiriladi va statiklar o'chiriladi.
- **Introduce Static Setter:** singleton nusxasini testda almashtirish uchun konstruktor himoyasi `protected` ga tushiriladi va sinfga nusxani almashtiradigan statik setter qo'shiladi; testda subklass yaratilib setter ga beriladi. Statik fabrika uchun ham xuddi shu: fabrika ichiga almashtiriladigan `server` maydoni va unga statik setter qo'yiladi.

**Spring'da qayerda uchraydi:** Spring ning `singleton` scope dagi bean i GoF Singleton emas, shuning uchun bu texnikalar faqat legacy statik holder bilan birga yashashda kerak. `SecurityContextHolder.setContext(...)` va `clearContext()` aslida tayyor static setter: Spring Security uni ataylab test uchun ochiq qoldirgan. `ReflectionTestUtils.setField(TargetClass.class, "instance", null)` statik maydonni testdan keyin tiklashga yaraydi. Mockito ning `mockStatic(...)` zamonaviy muqobil, lekin u `try` bloki ichida yopilishi shart va boshqa thread ga tarqamaydi, shuning uchun uni doimiy yechim deb emas, xuddi shu oraliq qadam deb ko'rish to'g'ri.

**Qo'llanish keyslari:**
- Yaratilishi qiyin legacy `RSCWorkflow` sinfidagi validatsiyani `static` qilib ajratib, sinfni ko'tarmasdan test yozish.
- Statik `BankingServices.updateAccountBalance(...)` utility siga instance delegat qo'shib, chaqiruvchiga obyektni parametr sifatida berish.
- Legacy singleton `ExternalRouter` ni testda fake subklass bilan almashtirish uchun statik setter qo'shish.
- Statik fabrika `RouterFactory.makeRouter()` ichiga almashtiriladigan `RouterServer` maydoni qo'yib, testda fake router qaytarish.
- Delegat orqali o'tgandan keyin statik metodlarni o'chirib, utility sinfni oddiy bean ga aylantirish.

```java
public class RscWorkflow { // yaratilishi qiyin legacy sinf

    public void validate(Packet packet) {
        validatePacket(packet); // imzo o'zgarmadi, chaqiruvchilar tegilmadi
    }

    // Expose Static Method: instance holatiga tegmaydi, shuning uchun `static`
    // bo'ladi va sinfni yaratmasdan test qilinadi; nom parametrdan olingan
    static void validatePacket(Packet packet) {
        if (packet.originator().equals("MIA") || !packet.hasValidChecksum()) {
            throw new InvalidFlowException(packet.id());
        }
    }
}
```

**Ehtiyot bo'ling:** Statik setter barcha testga ko'rinadigan holatni o'zgartiradi: kitob keyingi testni chalg'itishi mumkin bo'lgan holda `tearDown` da boshlang'ich qiymatni tiklashni talab qiladi, JUnit 5 da bu `@AfterEach`. Parallel test bajarilishida statik maydon umumiy resurs bo'ladi va bu yerda `@DirtiesContext` yordam bermaydi, chunki statik maydon Spring context ga tegishli emas. `Expose Static Method` bilan ochilgan metodni production kodi ishlatib ketmasligi uchun ko'rinishini package-private yoki `protected` qoldirish mumkin; `protected` bo'lsa testga xos subklass orqali chaqiriladi. Statikka delegat qilish hali ham global holatni yo'q qilmaydi: u faqat almashtirish nuqtasi beradi. Bu uch texnikani legacy kodda qanday tartibda qo'llash va qaysi shartda to'g'ridan konstruktor injection ga o'tish kerakligi [statik chaqiruv va singleton](../architect/34-legacy-kod-va-bosqichma-bosqich-refaktoring.md#3417-statik-chaqiruv-va-singleton-instance-delegator-va-static-setter) da yozilgan.

## 23.86 Chaqiruvni ajratib override qilish (Extract and Override Call / Factory Method / Getter)

**Tavsif:** Testga xalal beradigan bog'liqlik lokal bo'lsa, uni tashqi interfeys o'zgartirmasdan, faqat sinf ichida override qilinadigan nuqta yasab uzish mumkin. Uch shakl bor (Feathers, *Working Effectively with Legacy Code*, Prentice Hall PTR, 2004 (copyright 2005), 25-bob, 348, 350 va 352-bet).

- **Extract and Override Call:** bitta muammoli chaqiruv (odatda statik yoki global) o'sha sinfdagi yangi `protected` metodga ajratiladi, imzo o'zgarmaydi, keyin testga xos subklass uni override qiladi. Kitob buni eng ko'p ishlatiladigan texnika deb ataydi va global va statik bog'liqlikni uzishning ideal yo'li deydi.
- **Extract and Override Factory Method:** konstruktor ichidagi `new` va u bilan bog'liq butun tayyorlash ishi `protected` fabrika metodiga chiqariladi, testga xos subklass fabrikani override qilib fake qaytaradi.
- **Extract and Override Getter:** maydon uchun dangasa getter yoziladi (birinchi chaqiruvda yaratadi), sinf ichidagi hamma murojaat getter ga o'tadi, keyin getter override qilinadi. Kitob mezonni aniq beradi: bitta muammoli metod bo'lsa chaqiruvni ajratish osonroq, bir obyektda ko'p muammoli metod bo'lsa getter aniq foyda.

Kitobdagi getter misoli C++ da, chunki texnika o'sha tilning konstruktorda virtual chaqiruvni almashtirmaslik qoidasi uchun o'ylangan; quyida g'oya Java ga o'tkazilgan. Java da bu taqiq yo'q, lekin kitob Java da ham konstruktordan override qilinadigan metodni chaqirishni production kodida tavsiya qilmaydi (o'sha kitob, 25-bob, 406-bet).

**Spring'da qayerda uchraydi:** `@MockitoSpyBean` va Mockito `spy(...)` shu texnikaning dinamik varianti: real obyekt qoladi, faqat ajratilgan metod almashtiriladi. Legacy komponentda konstruktorda `new RestTemplate()`, `new KafkaProducer<>(...)` yoki `new JdbcTemplate(dataSource)` yozilgan bo'lsa, fabrika metodi birinchi qadam, `RestClient.Builder` yoki `DataSource` ni inject qilish esa manzil. Sinf va metod `final` bo'lmasligi shart, shuning uchun bu texnika Java `record` va `final` sinflarda ishlamaydi.

**Qo'llanish keyslari:**
- Legacy servisdagi bitta statik `StyleMaster.formStyles(...)` chaqiruvini ajratib, testda bo'sh ro'yxat qaytarish.
- Konstruktordagi `new HttpPaymentGateway(...)` ni `protected PaymentGateway createGateway()` ga chiqarib, testda fake qaytarish.
- Bitta obyektda beshta muammoli metod bo'lsa, maydon uchun `protected` getter ochib, hammasini bir joyda almashtirish.
- Jadval ichidagi `UUID.randomUUID()` yoki `LocalDate.now()` chaqiruvini ajratib, testda qat'iy qiymat berish.
- Fabrika metodini ochgandan keyin uni konstruktor parametriga aylantirib, subklassni olib tashlash.

```java
public class SettlementJob {
    private final PaymentGateway gateway;

    public SettlementJob(SettlementProperties props) {
        this.gateway = createGateway(props); // konstruktordagi `new` fabrikaga chiqdi
    }

    // Extract and Override Factory Method: tanasi faqat yaratish, qarorsiz
    protected PaymentGateway createGateway(SettlementProperties props) {
        return new HttpPaymentGateway(props.baseUrl());
    }
}
```

**Ehtiyot bo'ling:** Override qilingan metodning haqiqiy tanasi testda hech qachon bajarilmaydi, shuning uchun u imkon qadar bo'sh va mexanik bo'lishi kerak: ichida shart yoki hisob qolsa, u qoplamadan tushib qoladi. Konstruktordan chaqirilgan fabrika metodi subklassda override qilinsa, subklass maydonlari hali initsializatsiya qilinmagan bo'ladi va override qilingan tana ularni o'qisa `null` oladi; shu sabab override qilingan tana faqat parametrlarga tayansin. Uch texnikaning hammasi vaqtinchalik seam: tayyor test to'ri paydo bo'lgandan keyin bog'liqlik konstruktorga chiqarilsin, aks holda sinfda doimiy test uchun ochilgan teshik qoladi. Uchligini legacy modulda qo'llash tartibi va variantni tanlash jadvali [metod ichidagi `new` ni testda almashtirish](../architect/34-legacy-kod-va-bosqichma-bosqich-refaktoring.md#3416-metod-ichidagi-new-ni-testda-almashtirish-extract-and-override-uchligi) da.

## 23.87 Maydonni testda almashtirish (Supersede Instance Variable)

**Tavsif:** Konstruktorda yaratilgan obyektni testda almashtirish kerak, lekin konstruktorni parametrlashtirish undagi chalkash mantiq sababli qimmat va konstruktordan override qilinadigan metod chaqirishni ham xohlamaysiz. Bunda sinfga `supersedeXxx(...)` nomli metod qo'shiladi: u eski nusxani tashlab, maydonga yangi obyektni qo'yadi; test obyektni yaratib, SUT ni ishlatishdan OLDIN shu metodni chaqiradi (Feathers, *Working Effectively with Legacy Code*, Prentice Hall PTR, 2004 (copyright 2005), 25-bob, 404-bet). Nom tasodifiy tanlanmagan: `supersede` kamdan-kam uchraydigan so'z, shuning uchun production kodi bu metodni ishlatib ketganini oddiy qidiruv bilan topish mumkin (o'sha kitob, 25-bob, 407-bet). Kitob umumiy ogohlantirish ham beradi: obyektning asosiy hamkorlarini almashtiradigan setter yomon amaliyot, chunki undan keyin metod nima qilishini bilish uchun obyektning tarixini bilish kerak bo'ladi.

Kitobdagi misol C++ da va asosiy sababi ham C++ ga xos (konstruktordan virtual chaqiruv override qilinmaydi). Java da bu taqiq yo'q, lekin ikkinchi sabab qoladi: konstruktordan chaqirilgan override qilinadigan metod subklass maydonlari initsializatsiya qilinmaganda bajariladi. Shu sababli Java da ham `supersede` chaqiruvni ajratib override qilishga nisbatan xavfsizroq tanlov bo'lib qoladi. ESLATMA: bu Java uchun korpusning xulosasi, kitob Java ni bu o'rinda alohida tavsiflamaydi.

**Spring'da qayerda uchraydi:** Bean ni Spring yaratadigan joyda `ReflectionTestUtils.setField(bean, "gateway", fake)` xuddi shu ishni production kodiga metod qo'shmasdan bajaradi, lekin u maydon nomiga satr bilan bog'lanadi va refaktoringda jim sinadi; `supersedeXxx` esa kompilyator tekshiradigan variant. `@MockitoSpyBean` context dagi real bean ni o'rab metodini almashtiradi, maydonini emas, shuning uchun konstruktorda yaratilgan hamkor uchun u yetarli bo'lmaydi. Metodni package-private qoldirish odatiy: test bir xil paketda bo'ladi va production kodi uni ko'rmaydi.

**Qo'llanish keyslari:**
- Konstruktorda `new HttpPaymentGateway(...)` yaratgan legacy job ga `supersedeGateway(...)` qo'shib, testda fake berish.
- Konstruktorda ochilgan fayl yoki ulanishni testda in-memory variantga almashtirish.
- Konstruktorda `Executors.newFixedThreadPool(...)` yaratgan komponentda executor ni sinxron variantga almashtirish.
- `Clock` ni konstruktorga chiqarish hali imkonsiz bo'lsa, `supersedeClock(Clock.fixed(...))` bilan vaqtni qotirish.
- Texnikani kiritgandan keyin maydonni konstruktor parametriga ko'chirib, `supersede` metodini o'chirish.

```java
public class SettlementJob {
    private PaymentGateway gateway; // `final` bo'lishi mumkin emas

    public SettlementJob(SettlementProperties props) {
        this.gateway = new HttpPaymentGateway(props.baseUrl());
    }

    // faqat test uchun: nomi `supersede` bilan boshlanadi, production'da qidirib topiladi
    void supersedeGateway(PaymentGateway replacement) {
        this.gateway = replacement;
    }
}
```

**Ehtiyot bo'ling:** Maydon `final` bo'lishdan to'xtaydi, ya'ni immutable dizaynga qarshi qadam; bu qarz vaqtinchalik bo'lishi kerak. Eski obyektga sinf ichida boshqa havola saqlangan bo'lsa (ro'yxat, listener ro'yxati, keshdagi nusxa), almashtirish yarim ishlaydi va test yolg'on ishonch beradi: kitob almashtirishdan oldin boshqa havola yo'qligini tekshirishni talab qiladi. Metod thread-safe emas, shuning uchun u obyekt boshqa thread ga berilishidan oldin chaqirilsin; singleton bean da esa uni umuman ishlatmang. Production kodida `supersede` chaqiruvi paydo bo'lsa, bu Test Logic in Production smell i va darhol tuzatilishi kerak.

## 23.88 O'zgarmas umumiy fixture (Immutable Shared Fixture)

**Tavsif:** Umumiy fixture ning asosiy muammosi - testlar uni o'zgartirsa Erratic Tests paydo bo'lishi va Independent Test printsipi buzilishi. O'zgarmas umumiy fixture buni fixture ni ikki mantiqiy qismga bo'lib hal qiladi: birinchi qism - har bir testga kerak, lekin hech bir test o'zgartirmaydigan narsa; ikkinchi qism - testga o'zgartirish yoki o'chirish kerak bo'lgan obyektlar, va ular har bir testda yangi fixture sifatida quriladi. Meszaros ning asosiy mezoni: agar biror test boshqa test qilgan ishni o'zgarmas qismdagi obyektning o'zgarishi deb sezsa, o'sha o'zgarish fixture ni baham ko'radigan hech bir testda ruxsat etilmaydi. Amalda o'zgarmas qism ko'pincha reference ma'lumot bo'ladi va test fixture lari uning ustiga quriladi (Gerard Meszaros, *xUnit Test Patterns*, Addison-Wesley, 2007, 18-bob, 323-bet). Kitob misolida test umumiy "taklif qilingan reys" ni bekor qilib, keyin `finally` da holatni tiklashga urinadi; o'zgarmas variantda test o'zi ahamiyatsiz aeroportlar orasida reys yaratadi va tozalash umuman kerak bo'lmaydi (o'sha kitob, 18-bob, 326-bet).

**Spring'da qayerda uchraydi:** Spring TestContext Framework ning context keshi bean lar uchun aynan o'zgarmas umumiy fixture: bean lar baham ko'riladi va hech bir test ularning holatini o'zgartirmaydi deb kelishilgan. Ma'lumot tomonida o'zgarmas qism Flyway ning `R__reference_data.sql` repeatable migration i bilan beriladi (valyutalar, soliq stavkalari, rollar, mamlakatlar), o'zgaradigan qism esa har testda `@Transactional` rollback ostida quriladi. Loyiha darajasidagi strategiya va qaysi jadval qaysi qismga tegishli ekani [fixture strategiyalari](../testing/10-test-malumotlarini-boshqarish.md#102-fixture-strategiyalari) da yozilgan.

**Qo'llanish keyslari:**
- Valyuta, soliq va rol kataloglarini repeatable migration bilan bir marta yuklab, testlarda faqat o'qish.
- Har test o'ziga tegishli buyurtma va mijozni yaratib, katalogdagi mavjud valyuta kodiga tayanishi.
- Umumiy fixture dagi yozuvni o'zgartirib, keyin `finally` da tiklaydigan testlarni shu shaklga ko'chirish.
- Identifikatorni testda qo'lda bermaslik: generatsiya qilingan kalit bilan yozuvlar to'qnashmasdan to'planadi.
- Sanoqqa ta'sir qiladigan testlar uchun katalogdagi ataylab ahamiyatsiz yozuvlardan foydalanish.

```java
@SpringBootTest
@Transactional // o'zgaradigan qism: har testdan keyin rollback
class OrderPricingTest {

    @Test
    void pricesOrderInExistingCurrency() {
        // o'zgarmas qism: "UZS" R__reference_data.sql dan keladi, test uni o'zgartirmaydi
        Order order = orders.save(new Order("UZS", Money.of("100000", "UZS")));
        assertThat(pricer.totalOf(order)).isEqualTo(Money.of("112000", "UZS"));
    }
}
```

**Ehtiyot bo'ling:** "O'zgarmas" - kelishuv, kafolat emas: bitta `UPDATE` yoki `delete` butun to'plamni jim buzadi va nosozlik boshqa testda chiqadi. Shuning uchun o'zgarmas jadvallarga yozishni test rolidan tortib olish yoki to'plam oxirida qator sonini tekshirish kerak. Eng qiyin qism - nima "o'zgarish" ekanini aniqlash: aeroportdagi reyslar soni kabi hosila qiymat ham o'zgarmas qismning bir qismi bo'lib chiqadi, shuning uchun sanoqqa tayanadigan assertion lar o'zgarmas ma'lumotga emas, test o'zi yaratgan yozuvlarga qarasin. O'zgarmas qismga unique constraint li maydon kirsa, test o'z yozuvini qo'shganda to'qnashuv chiqishi mumkin.

## 23.89 Entity zanjirini kesish (Entity Chain Snipping)

**Tavsif:** Entity Chain Snipping - test stub ning Responder variantining maxsus holati: bir-biriga bog'langan obyektlarning butun to'ri bitta stub bilan almashtiriladi va o'sha stub shu to'r bo'lib ko'rinadi. Meszaros ikki foydani ko'rsatadi: fixture tayyorlash ancha tezlashadi (ayniqsa obyektlar odatda bazaga saqlanishi kerak bo'lganda) va testni o'qish osonlashadi (Gerard Meszaros, *xUnit Test Patterns*, Addison-Wesley, 2007, 23-bob, 531-bet). Texnikaning mohiyati - zanjirni eng birinchi bo'g'inida kesish: SUT ga butun graf emas, grafdan kerakli javobni beradigan yupqa shartnoma uzatiladi.

**Spring'da qayerda uchraydi:** JPA da zanjir odatiy: `Order -> Customer -> Organization -> TaxProfile`. Narx hisoblashni test qilish uchun to'rt entity ni saqlash kerak bo'ladi, holbuki SUT ga faqat soliq stavkasi kerak. Kesish Java da tor interfeys kiritish bilan bajariladi (`TaxRateSource`), keyin Mockito yoki qo'lda yozilgan implementatsiya uni stub qiladi. Qo'shimcha foyda Hibernate ga xos: lazy assotsiatsiya bo'ylab yurish tranzaksiya tashqarisida `LazyInitializationException` beradi, kesilgan zanjirda esa yurish umuman yo'q, shuning uchun testga ochiq session kerak bo'lmaydi. ESLATMA: lazy graf bilan bog'liq bu sabab korpusning qo'shimchasi, kitob JPA ni tilga olmaydi.

**Qo'llanish keyslari:**
- Narx hisoblagichni test qilishda `Order -> Customer -> Organization -> TaxProfile` zanjirini bitta `TaxRateSource` stub i bilan almashtirish.
- Hisobot generatori uchun chuqur graf o'rniga faqat kerakli maydonlarni beradigan projection interfeysini stub qilish.
- `@DataJpaTest` ichida o'nlab `save(...)` chaqiruvidan iborat fixture ni bitta stub ga aylantirib, testni unit darajasiga tushirish.
- Tranzaksiyadan tashqarida ishlaydigan listener testida lazy zanjirni kesib, ochiq session talabini yo'qotish.
- Grafning faqat bitta bo'g'ini kerak bo'lgan testlarni aniqlab, qolgan uchta entity ni fixture dan olib tashlash.

```java
// kesishdan oldin: SUT grafni o'zi kezadi, testga to'rt entity kerak
BigDecimal rate = order.getCustomer().getOrganization().getTaxProfile().getRate();

// kesishdan keyin: yupqa shartnoma, testda bitta stub
public interface TaxRateSource {
    BigDecimal rateFor(Order order);
}

given(taxRateSource.rateFor(order)).willReturn(new BigDecimal("0.12"));
```

**Ehtiyot bo'ling:** Stub SUT ni production dagidan boshqa konfiguratsiyada sinaydi, shuning uchun kitob kamida bitta testni stub siz o'tkazishni talab qiladi: kesilgan zanjirning real mapping i, `JoinColumn` lari va fetch rejimi aynan o'sha testda tekshiriladi. Ikkinchi tuzoq - SUT ning o'z qismini stub bilan almashtirib qo'yish; nima SUT, nima fixture ekani aniq bo'lishi kerak. Entity sinfining o'zini mock qilmang: `equals`, `hashCode` va proxy xulqi tufayli bu mo'rt bo'ladi, kesish uchun yangi interfeys kiritish to'g'ri yo'l. Haddan ziyod stubbing esa Overspecified Software ga olib keladi.

## 23.90 Amalda qo'llash

- [ ] Test to'plamini uch guruhga ajratib o'lchang: unit, slice va to'liq kontekst. Har birining vaqtini yozib qo'ying.
- [ ] H2 ni PostgreSQL o'rniga ishlatadigan testlarni toping va ularni Testcontainers ga o'tkazish rejasini tuzing.
- [ ] `Thread.sleep` ishlatadigan testlarni qidirib, har birini Awaitility yoki deterministik soatga o'tkazing.
- [ ] Spring kontekst keshi necha marta qayta yaratilayotganini log'dan o'lchab, kontekst konfiguratsiyalarini birlashtirish nomzodlarini belgilang.
- [ ] Mockito `STRICT_STUBS` rejimida ishlayotganini tasdiqlang va `LENIENT` ishlatadigan joylarni asoslab yozing.
- [ ] Domen va hisob-kitob paketlari uchun mutation score ni PIT bilan o'lchab, natijani yozib qo'ying.
- [ ] `@Disabled` testlarni sanab chiqib, har biriga sabab va issue havolasi qo'shilganini tasdiqlang.
- [ ] Test ma'lumotlarini yaratish usulini birlashtiring: builder yoki object mother tanlang va qolganini ko'chirish rejasini yozing.

## Manbalar

- Gerard Meszaros, *xUnit Test Patterns: Refactoring Test Code*, Addison-Wesley, 2007, 18-bob "Test Strategy Patterns" (277-345-bet) - Recorded Test, Scripted Test, Data-Driven Test, Minimal Fixture va Standard Fixture yozuvlari
- Gerard Meszaros, *xUnit Test Patterns: Refactoring Test Code*, Addison-Wesley, 2007, 19-bob "xUnit Basics Patterns" (347-406-bet) - Test Method shablonlari, Assertion Method va Assertion Message, Test Runner, Testcase Object, Test Suite Object, Test Discovery, Test Enumeration va Test Selection
- Gerard Meszaros, *xUnit Test Patterns: Refactoring Test Code*, Addison-Wesley, 2007, 20-bob "Fixture Setup Patterns" (407-459-bet) - In-line, Delegated va Implicit Setup ni tanlash mezoni, Setup Decorator va Chained Tests
- Gerard Meszaros, *xUnit Test Patterns: Refactoring Test Code*, Addison-Wesley, 2007, 21-bob "Result Verification Patterns" (461-497-bet) - State Verification va Behavior Verification farqi, Unfinished Test Assertion
- Gerard Meszaros, *xUnit Test Patterns: Refactoring Test Code*, Addison-Wesley, 2007, 22-bob "Fixture Teardown Patterns" (499-520-bet) - Garbage-Collected, In-line va Implicit Teardown; setUp xato bersa tearDown chaqirilmasligi
- Gerard Meszaros, *xUnit Test Patterns: Refactoring Test Code*, Addison-Wesley, 2007, 23-bob "Test Double Patterns" (521-590-bet) - Configurable va Hard-Coded Test Double, Test-Specific Subclass
- Gerard Meszaros, *xUnit Test Patterns: Refactoring Test Code*, Addison-Wesley, 2007, 24-bob "Test Organization Patterns" (591-648-bet) - Test Utility Method, Test Helper, Testcase Superclass, Testcase Class per Class va per Feature
- Gerard Meszaros, *xUnit Test Patterns: Refactoring Test Code*, Addison-Wesley, 2007, 25-bob "Database Patterns" (649-675-bet) - Database Sandbox, Stored Procedure Test, Transaction Rollback Teardown
- Gerard Meszaros, *xUnit Test Patterns: Refactoring Test Code*, Addison-Wesley, 2007, 26-bob "Design-for-Testability Patterns" (677-712-bet) - Dependency Lookup va uning Dependency Injection dan farqi
- Gerard Meszaros, *xUnit Test Patterns: Refactoring Test Code*, Addison-Wesley, 2007, 27-bob "Value Patterns" (713-731-bet) - Literal Value, Derived Value va Generated Value
- Michael C. Feathers, *Working Effectively with Legacy Code*, Prentice Hall PTR, 2004 (copyright 2005), 25-bob (339, 345, 348, 349, 350, 352, 369, 372, 399, 404, 406 va 407-bet) - global va statik bog'liqlikni uzish texnikalari: Encapsulate Global References, Replace Global Reference with Getter, Expose Static Method, Introduce Instance Delegator, Introduce Static Setter, Extract and Override Call, Extract and Override Factory Method, Extract and Override Getter va Supersede Instance Variable; tanlash mezoni va `supersede` nom prefiksining sababi
- Gerard Meszaros, *xUnit Test Patterns: Refactoring Test Code*, Addison-Wesley, 2007, 18-bob "Test Strategy Patterns" (323 va 326-bet) - Immutable Shared Fixture varianti: fixture ni hech bir test o'zgartirmaydigan umumiy qism va test o'zi quradigan qismga bo'lish, va "o'zgarish" nima ekanini aniqlash mezoni
- Gerard Meszaros, *xUnit Test Patterns: Refactoring Test Code*, Addison-Wesley, 2007, 23-bob "Test Double Patterns" (531-bet) - Entity Chain Snipping: obyektlar to'rini bitta Responder stub bilan almashtirish, fixture tezlashishi va stub siz kamida bitta test talabi
- Robert C. Martin, *Clean Architecture*, 28-bob - test chegarasi va testlarning arxitektura qismi ekani
- Robert C. Martin, *Clean Architecture*, 23-bob - Humble Object va uni testda ishlatish
- [JUnit 5.11, Writing Tests](https://raw.githubusercontent.com/junit-team/junit5/r5.11.0/documentation/src/docs/asciidoc/user-guide/writing-tests.adoc) - lifecycle, `@Nested`, parametrli test va `@Timeout`
- [JUnit 5.11, Extensions](https://raw.githubusercontent.com/junit-team/junit5/r5.11.0/documentation/src/docs/asciidoc/user-guide/extensions.adoc) - extension model, `TestInstancePostProcessor`, `ParameterResolver`
- [Testcontainers, Reusable Containers](https://raw.githubusercontent.com/testcontainers/testcontainers-java/9bb3c2dc175672ad33a2eafd7133212c7173ac43/docs/features/reuse.md) - reuse ning experimental ekani, `start()` qo'lda chaqirilishi va `stop()` taqiqi
- [Testcontainers, JUnit 5 Quickstart](https://raw.githubusercontent.com/testcontainers/testcontainers-java/9bb3c2dc175672ad33a2eafd7133212c7173ac43/docs/quickstart/junit_5_quickstart.md) - `@Testcontainers` va `@Container` ning ishlashi
- [Spring Framework 7.0, Context Caching](https://raw.githubusercontent.com/spring-projects/spring-framework/v7.0.0/framework-docs/modules/ROOT/pages/testing/testcontext-framework/ctx-management/caching.adoc) - kesh kaliti, default hajm 32 va fork da keshning ishlamasligi

---

[&larr; 22. Deployment va operatsion patternlar](22-deployment-va-operatsion-patternlar.md) · [Mundarija](README.md) · [24. Zamonaviy Java va funksional patternlar &rarr;](24-zamonaviy-java-va-funksional-patternlar.md)
