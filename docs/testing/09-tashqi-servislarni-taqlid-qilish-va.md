<!-- doc: testing | chapter: 9 | part:  -->

[Barcha hujjatlar](../../README.md) / [Testlash qo'llanmasi](README.md)

> Holat: AI yozgan, inson tekshirmagan.

# 9. Tashqi servislarni taqlid qilish va contract testing (Faking External Services & Contract Testing)

<details>
<summary>Bu bobdagi 14 bo'lim</summary>

- [9.1 Muammo va yechim variantlari ierarxiyasi](#91-muammo-va-yechim-variantlari-ierarxiyasi)
- [9.2 WireMock bilan HTTP stub server](#92-wiremock-bilan-http-stub-server)
- [9.3 MockServer va Hoverfly: qachon qaysi biri](#93-mockserver-va-hoverfly-qachon-qaysi-biri)
- [9.4 MockRestServiceServer bilan client'ni testlash](#94-mockrestserviceserver-bilan-clientni-testlash)
- [9.5 Record and replay: foydasi va xavfi](#95-record-and-replay-foydasi-va-xavfi)
- [9.6 Stub drift muammosi](#96-stub-drift-muammosi)
- [9.7 Contract testing nazariyasi](#97-contract-testing-nazariyasi)
- [9.8 Spring Cloud Contract: buyurtma va to'lov servisi](#98-spring-cloud-contract-buyurtma-va-tolov-servisi)
- [9.9 Pact: consumer test, broker, can-i-deploy](#99-pact-consumer-test-broker-can-i-deploy)
- [9.10 Messaging contract va schema evolution](#910-messaging-contract-va-schema-evolution)
- [9.11 OpenAPI'ni contract sifatida ishlatish](#911-openapini-contract-sifatida-ishlatish)
- [9.12 Contract testni CI'ga qo'yish](#912-contract-testni-ciga-qoyish)
- [9.13 Anti-patternlar](#913-anti-patternlar)
- [9.14 Arxitektor nazorat ro'yxati](#914-arxitektor-nazorat-royxati)

</details>



Mikroservisda kodning katta qismi o'z bazasi bilan emas, boshqa servislar bilan gaplashadi: to'lov gateway, KYC provayderi, ichki buyurtma yoki hisob servisi. Shu integratsiyalarni qanday testlash - arxitektura qarori: u build vaqtini, test barqarorligini va integratsiya nosozligini qancha erta ushlashni belgilaydi. Bu bobda stub vositalaridan (WireMock, MockRestServiceServer) boshlab, stub drift orqali contract testing'ga (Spring Cloud Contract, Pact) va schema evolution nazoratiga o'tamiz.

## 9.1 Muammo va yechim variantlari ierarxiyasi

Integratsion testda haqiqiy tashqi servisga murojaat qilish bir vaqtda to'rt xil narx to'laydi. Tezlik: har bir so'rov tarmoq orqali ketadi va suite minutlarga cho'ziladi. Barqarorlik: vendor sandbox'i tushsa yoki rate limit bersa, build qizil bo'ladi va jamoa "qayta ishga tushir" madaniyatiga o'tadi. Nazorat: 503, read timeout, buzilgan JSON kabi holatlarni buyurtma bilan chaqirib bo'lmaydi, aslida eng ko'p incident shu yo'llardan keladi. Narx: har bir chaqiruv tariflanishi mumkin.

Shuning uchun integratsiya nuqtasini testlashda bir necha qatlamni bosqichma-bosqich qo'llash kerak:

1. **Mock (unit daraja)** - client interfeysini Mockito bilan almashtirish. Eng tez, lekin HTTP, serializatsiya va xato mapping'ini tekshirmaydi; faqat biznes logikani client'dan ajratish uchun.
2. **In-process stub (`MockRestServiceServer`)** - socket ochilmaydi, lekin URL, header, body serializatsiyasi va javob deserializatsiyasi tekshiriladi. Client sinfining o'zini testlash uchun ideal.
3. **Out-of-process stub server (WireMock, MockServer, Hoverfly)** - haqiqiy TCP port, haqiqiy HTTP client stack: connection pool, timeout, retry, TLS. Kechikish va tarmoq xatolarini simulyatsiya qilish mumkin.
4. **Contract test** - stub endi qo'lda yozilmaydi, provider tomonidan verifikatsiya qilingan contract'dan generatsiya qilinadi. Stub drift'ni ushlaydigan yagona qatlam.
5. **Vendor sandbox** - kunda bir marta, alohida pipeline'da, release gate emas: vendor bilan haqiqiy muvofiqlikni tekshirish uchun.
6. **Real servis** - faqat production'dagi synthetic monitoring va smoke sifatida, PR build'ida emas.

Arxitektorning asosiy qarori shu: 2 va 3 qatlam "mening kodim to'g'ri ishlaydi" ishonchini beradi, 4-qatlam esa "mening kutganim provayderning haqiqatiga mos" deganini. Bu ikki xil savol.

## 9.2 WireMock bilan HTTP stub server

WireMock 3.x - JVM dunyosida eng keng tarqalgan HTTP stub server. Ikki rejimi bor: standalone jar (`java -jar wiremock-standalone-3.x.jar --port 8089`, mapping'lar `mappings/` papkasidan o'qiladi - lokal development va QA muhiti uchun) va test ichidagi JUnit 5 extension. Testda `@RegisterExtension` bilan `WireMockExtension` tavsiya etiladi: har bir testdan keyin stub'larni reset qiladi, `dynamicPort()` esa parallel build'da port konfliktini yo'qotadi.

Spring Boot bilan ulashning to'g'ri usuli - base URL'ni property orqali berib, testda `@DynamicPropertySource` bilan WireMock port'iga yo'naltirish. Shunda production kodida test-aware shart qolmaydi.

```java
@SpringBootTest
class PaymentClientWireMockTest {

    @RegisterExtension
    static WireMockExtension wm = WireMockExtension.newInstance()
            .options(wireMockConfig().dynamicPort())
            .failOnUnmatchedRequests(true)
            .build();

    @DynamicPropertySource
    static void props(DynamicPropertyRegistry registry) {
        registry.add("payment.base-url", wm::baseUrl);
    }

    @Autowired PaymentClient client;

    @Test
    void chargeIsAuthorized() {
        wm.stubFor(post(urlPathEqualTo("/v1/charges"))
                .withHeader("Content-Type", containing("application/json"))
                .withRequestBody(matchingJsonPath("$.amount", equalTo("1000")))
                .willReturn(okJson("{\"id\":\"ch_1\",\"status\":\"AUTHORIZED\"}")));

        assertThat(client.charge(new ChargeRequest("ord-1", 1000)).status())
                .isEqualTo("AUTHORIZED");
        wm.verify(1, postRequestedFor(urlPathEqualTo("/v1/charges")));
    }
}
```

WireMock'ning asl qiymati happy path emas, yomon yo'llarni arzon simulyatsiya qilishda. `withFixedDelay(ms)` client'ning read timeout sozlamasini tekshiradi, `withChunkedDribbleDelay` javobni bo'lib yuboradi, `withFault(...)` connection reset chaqiradi. `inScenario(...)` stateful stub yaratadi: birinchi chaqiruvda 503, ikkinchisida 200 - retry va circuit breaker siyosati uchun zarur.

```java
@Test
void retriesAfterTransientFailure() {
    wm.stubFor(get(urlPathEqualTo("/v1/rates")).inScenario("flaky")
            .whenScenarioStateIs(Scenario.STARTED)
            .willReturn(aResponse().withStatus(503).withFixedDelay(200))
            .willSetStateTo("recovered"));

    wm.stubFor(get(urlPathEqualTo("/v1/rates")).inScenario("flaky")
            .whenScenarioStateIs("recovered")
            .willReturn(okJson("{\"usd\":12650}")));

    assertThat(client.rate("usd")).isEqualTo(12650);
    wm.verify(2, getRequestedFor(urlPathEqualTo("/v1/rates")));
}

@Test
void connectionResetBecomesDomainException() {
    wm.stubFor(get(urlPathEqualTo("/v1/rates"))
            .willReturn(aResponse().withFault(Fault.CONNECTION_RESET_BY_PEER)));

    assertThatThrownBy(() -> client.rate("usd"))
            .isInstanceOf(RateUnavailableException.class);
}
```

Amaliy qoidalar: `failOnUnmatchedRequests(true)` yoqilgan bo'lsin, aks holda noto'g'ri URL jim o'tib ketadi; `verify(...)` bilan yuborilgan so'rovni ham tasdiqlang (idempotency key, correlation va auth header ketdimi); umumiy `mappings/` papkasi vaqt o'tib hech kim tushunmaydigan global holatga aylanadi.

## 9.3 MockServer va Hoverfly: qachon qaysi biri

MockServer (`org.mock-server:mockserver-junit-jupiter`) WireMock'ga funksional jihatdan yaqin; kuchli tomoni - expectation/verification DSL'i va forward proxy rejimi: trafikni o'tkazib yuborib bir qismini ushlab qolish mumkin. Hoverfly (`io.specto:hoverfly-java`) boshqa falsafada: capture mode'da real trafikni yozib oladi, simulate mode'da qaytaradi, latency va xato injection'ni (chaos) qulay beradi - hujjatlashtirilmagan legacy servis bilan eng tez natija beradi.

Default tanlov - WireMock: eng katta ecosystem va Spring Cloud Contract ham stub'larni WireMock orqali serve qiladi, ya'ni contract testing'ga o'tish uzluksiz bo'ladi. MockServer'ni proxy va ko'p protokolli ehtiyoj paydo bo'lganda, Hoverfly'ni record-and-replay asosiy rejim bo'lganda qo'shing.

## 9.4 MockRestServiceServer bilan client'ni testlash

Agar maqsad client sinfining o'zi bo'lsa - URL qurish, header, DTO serializatsiyasi, xato status'ni domen exception'ga aylantirish - socket ochish shart emas. `MockRestServiceServer` `RestTemplate` va `RestClient` uchun in-process stub beradi, `@RestClientTest` uni avtomatik sozlaydi: eng tez variant.

```java
@RestClientTest(value = PaymentClient.class,
        properties = "payment.base-url=https://payments.test")
class PaymentClientSliceTest {

    @Autowired MockRestServiceServer server;
    @Autowired PaymentClient client;

    @Test
    void mapsResponseBodyToDto() {
        server.expect(once(), requestTo("https://payments.test/v1/charges"))
                .andExpect(method(HttpMethod.POST))
                .andExpect(jsonPath("$.orderId").value("ord-1"))
                .andRespond(withSuccess("{\"id\":\"ch_1\",\"status\":\"AUTHORIZED\"}",
                        MediaType.APPLICATION_JSON));

        assertThat(client.charge(new ChargeRequest("ord-1", 1000)).id())
                .isEqualTo("ch_1");
        server.verify();
    }

    @Test
    void mapsServerErrorToDomainException() {
        server.expect(requestTo("https://payments.test/v1/charges"))
                .andRespond(withServerError());
        assertThatThrownBy(() -> client.charge(new ChargeRequest("ord-1", 1000)))
                .isInstanceOf(PaymentGatewayException.class);
    }
}
```

Cheklovi: haqiqiy HTTP stack chetlab o'tiladi, demak connection timeout, TLS, redirect, connection pool tugashi ko'rinmaydi. Reactive `WebClient` uchun u ishlamaydi - WireMock yoki `ExchangeFunction` almashtirish kerak. Taqsimot: client sinfi uchun `@RestClientTest`, resilience siyosati uchun WireMock.

## 9.5 Record and replay: foydasi va xavfi

Stub'ni qo'lda yozish qimmat bo'lganda javobni real servisdan yozib olish mumkin: WireMock'da `--proxy-all="https://api.vendor.com" --record-mappings` rejimi yoki `/__admin/recorder` admin API, Hoverfly'da capture mode. Foydasi - real, to'liq payload'lar, chunki qo'lda yozilgan stub provayder javobidan soddalashtirilgan bo'ladi va bug aynan shu soddalashtirish ichida yashiringan bo'ladi.

Xavfi: fayllarda token, karta raqami, shaxsiy ma'lumot qolib ketadi va repo'ga tushadi; fixture'lar keraksiz maydonlar bilan o'sadi; eng muhimi - stub yozilgan kundan boshlab eskiradi, lekin test yashil turadi. Qoidalar: maxfiy maydonlarni avtomatik tozalash, faqat ishlatiladigan maydonlarni qoldirish, fixture yoniga sana va provider API versiyasini yozish, rejali qayta yozib olish. Record-and-replay - boshlash vositasi, strategiya emas.

## 9.6 Stub drift muammosi

Stub drift - integratsion testlashning markaziy nosozligi. Provider `status` maydonini `state` ga o'zgartiradi, `201` o'rniga `200` qaytaradi, xato formatini RFC 9457 (7807 ni almashtirgan) `problem+json` ga ko'chiradi yoki enum'ga yangi qiymat qo'shadi. Consumer tomonidagi stub buni bilmaydi: eski shaklni qaytaradi, testlar yashil, deploy o'tadi, production'da esa deserializatsiya sinadi. Ko'proq stub yozish muammoni yomonlashtiradi - har bir yangi stub provider haqida yana bir tasdiqlanmagan taxmin.

Sabab arxitektura darajasida: stub consumer repo'sida yashaydi, haqiqat esa provider repo'sida o'zgaradi va ikkisi o'rtasida avtomatik bog'lanish yo'q. Nightly sandbox smoke bu bog'lanishni kech va noaniq signal bilan beradi. To'g'ri yechim - stub'ni tasdiqlangan contract'dan olish: provider contract'ni buzsa, provider'ning o'z build'i qizil bo'ladi. Aynan shu contract testing'ning mavjudlik sababi.

## 9.7 Contract testing nazariyasi

Consumer-driven contract'da consumer o'z kutganini misollar ko'rinishida yozadi: shu so'rovga shu shakldagi javob kerak. Bu misollar mashina o'qiydigan, versiyalangan artefaktga aylanadi. Provider tomonda verification bo'ladi: provider haqiqiy implementatsiyasini ko'tarib, har bir interaction'ni qayta o'ynaydi va javob kutilgan shaklga mosligini tekshiradi. Broker (Pact Broker/PactFlow, SCC holatida Maven repository) o'rtada turadi: contract, versiya, muhit holati va verification natijalarini saqlaydi.

Integratsion testdan farqi: integratsion test ikki real tizimni bir muhitda, bir vaqtda ishlatishni talab qiladi va "hozir ishladi" deydi. Contract test juftlik muvofiqligini mustaqil tekshiradi - ikki servis bir vaqtda ishlashi shart emas, shuning uchun tez va deterministik. Narxi: u provider biznes logikasini tekshirmaydi, faqat kelishilgan interaction shakli va semantikasini. Ya'ni contract test E2E'ni emas, stub'larni almashtiradi.

## 9.8 Spring Cloud Contract: buyurtma va to'lov servisi

Ish oqimi: contract DSL (Groovy yoki YAML) provider repo'sida `src/test/resources/contracts/` ostida yashaydi va odatda consumer tomonidan pull request sifatida qo'shiladi. `spring-cloud-contract-maven-plugin` undan provider testlarini generatsiya qiladi (`MockMvc`, `WebTestClient` yoki `EXPLICIT` rejim), ular `verify` fazasida ishlaydi. Testlar o'tgach plugin `payment-service-1.4.0-stubs.jar` artefaktini Nexus/Artifactory'ga joylaydi.

```groovy
import org.springframework.cloud.contract.spec.Contract

Contract.make {
    description "1000 tiyinlik to'lov avtorizatsiya qilinadi"
    request {
        method POST()
        url "/v1/charges"
        headers { contentType applicationJson() }
        body(orderId: "ord-1", amount: 1000)
        bodyMatchers {
            jsonPath('$.orderId', byRegex('[a-z0-9\\-]+'))
            jsonPath('$.amount', byRegex(number()))
        }
    }
    response {
        status OK()
        headers { contentType applicationJson() }
        body(id: "ch_1", status: "AUTHORIZED")
        bodyMatchers {
            jsonPath('$.id', byRegex('ch_[a-z0-9]+'))
            jsonPath('$.status', byRegex('AUTHORIZED|DECLINED'))
        }
    }
}
```

YAML variantini Groovy bilmagan jamoalar afzal ko'radi va u xuddi shu imkoniyatlarni beradi:

```yaml
description: "limitdan oshgan to'lov DECLINED bo'ladi"
request:
  method: POST
  url: /v1/charges
  headers:
    Content-Type: application/json
  body:
    orderId: ord-2
    amount: 5000000
  matchers:
    body:
      - path: $.amount
        type: by_regex
        predefined: number
response:
  status: 200
  headers:
    Content-Type: application/json
  body:
    id: ch_2
    status: DECLINED
```

Generatsiya qilingan testlar base class'dan meros oladi - unda application ishga tushadi va tashqi bog'liqliklar (DB, downstream) boshqariladi:

```java
@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT)
public abstract class PaymentContractBase {

    @LocalServerPort int port;
    @MockitoBean ChargeService chargeService;

    @BeforeEach
    void setUp() {
        RestAssured.port = port;
        given(chargeService.charge(argThat(r -> r.amount() <= 1_000_000)))
                .willReturn(new Charge("ch_1", ChargeStatus.AUTHORIZED));
        given(chargeService.charge(argThat(r -> r.amount() > 1_000_000)))
                .willReturn(new Charge("ch_2", ChargeStatus.DECLINED));
    }
}
```

Consumer (order-service) tomonda esa stub runner shu jar'ni Maven repository'dan yuklab, WireMock'da ko'taradi. Qo'lda yozilgan stub umuman qolmaydi:

```java
@SpringBootTest
@AutoConfigureStubRunner(
        ids = "com.example:payment-service:+:stubs:8090",
        stubsMode = StubRunnerProperties.StubsMode.REMOTE,
        repositoryRoot = "https://nexus.internal/repository/maven-releases")
class OrderServiceContractTest {

    @Autowired OrderService orderService;

    @Test
    void orderIsPaidUsingRealProviderContract() {
        var order = orderService.place(new PlaceOrder("ord-1", 1000));
        assertThat(order.status()).isEqualTo(OrderStatus.PAID);
    }
}
```

Muhim nuqta: `ids` ichidagi `+` eng yangi versiyani oladi; production'da aniq versiya yoki oraliq ko'rsating, aks holda consumer build'i provider release'i bilan tasodifiy sinadi.

## 9.9 Pact: consumer test, broker, can-i-deploy

Pact JVM'da contract consumer testining yon mahsuloti: test Pact mock server'ga qarshi ishlaydi va `target/pacts/order-service-payment-service.json` fayli yoziladi.

```java
@ExtendWith(PactConsumerTestExt.class)
@PactTestFor(providerName = "payment-service", pactVersion = PactSpecVersion.V3)
class PaymentPactConsumerTest {

    @Pact(consumer = "order-service")
    public RequestResponsePact authorizedCharge(PactDslWithProvider builder) {
        return builder.given("merchant has sufficient limit")
                .uponReceiving("a charge request")
                .path("/v1/charges").method("POST")
                .body(new PactDslJsonBody()
                        .stringType("orderId", "ord-1")
                        .numberType("amount", 1000))
                .willRespondWith().status(200)
                .body(new PactDslJsonBody()
                        .stringMatcher("id", "ch_[a-z0-9]+", "ch_1")
                        .stringValue("status", "AUTHORIZED"))
                .toPact();
    }

    @Test
    @PactTestFor(pactMethod = "authorizedCharge")
    void chargeIsAuthorized(MockServer mockServer) {
        var client = new PaymentClient(RestClient.create(mockServer.getUrl()));
        assertThat(client.charge(new ChargeRequest("ord-1", 1000)).status())
                .isEqualTo("AUTHORIZED");
    }
}
```

Pact fayli broker'ga `pact:publish` bilan yuboriladi, provider uni broker'dan olib o'z implementatsiyasiga qarshi tekshiradi. `given(...)` matni provider tomonda `@State` metodiga bog'lanadi - test ma'lumotlarini kerakli holatga keltirish nuqtasi.

```java
@Provider("payment-service")
@PactBroker(url = "https://pact-broker.internal")
@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT)
class PaymentPactProviderTest {

    @LocalServerPort int port;

    @BeforeEach
    void target(PactVerificationContext context) {
        context.setTarget(new HttpTestTarget("localhost", port));
    }

    @TestTemplate
    @ExtendWith(PactVerificationSpringProvider.class)
    void verifyContracts(PactVerificationContext context) {
        context.verifyInteraction();
    }

    @State("merchant has sufficient limit")
    void merchantHasSufficientLimit() {
        merchantRepository.save(new Merchant("m-1", 10_000_000L));
    }
}
```

| Mezon | Spring Cloud Contract | Pact (Pact JVM) |
| --- | --- | --- |
| Contract manbasi | Alohida DSL fayl (provider repo'sida, consumer PR qiladi) | Consumer testining yon mahsuloti |
| Format | Groovy yoki YAML DSL, Java DSL | Pact JSON spetsifikatsiyasi (V3/V4) |
| Stub tarqatish | `*-stubs.jar` Maven/Nexus orqali, WireMock serve qiladi | Broker'dan pact, mock server test ichida |
| Markaziy registry | Maven repository (versiyalash bor, muhit holati yo'q) | Pact Broker/PactFlow: matritsa, tag, environment |
| Deploy gate | Yo'q (build va versiya tartibi bilan qo'lda) | `can-i-deploy` CLI - tayyor gate |
| Polyglot | JVM-markazli (boshqa tillar uchun cheklangan) | Kuchli: JS, .NET, Go, Python, Ruby |
| Messaging | Qo'llab-quvvatlanadi (Kafka, AMQP, Spring Cloud Stream) | Qo'llab-quvvatlanadi (async message pact) |
| Spring integratsiyasi | Juda chuqur, Boot bilan tabiiy | Yaxshi (`pact-jvm-provider-spring`), lekin tashqi |
| Kirish narxi | Spring jamoasi uchun past | O'rta: broker infrastrukturasi kerak |
| Eng mos holat | Faqat JVM, bir xil CI, stub'ni ham qayta ishlatish kerak | Ko'p tilli landshaft, qat'iy deploy gate kerak |

Tanlov mezoni: barcha servislar JVM va bitta Maven infrastrukturasida bo'lsa Spring Cloud Contract kamroq qo'shimcha tizim talab qiladi va stub'larni bonus beradi. Frontend, Go yoki Python consumer'lar bo'lsa va deploy avtomatik gate bilan to'xtatilishi kerak bo'lsa, Pact Broker'ning `can-i-deploy` va deployment matritsasi raqobatsiz.

## 9.10 Messaging contract va schema evolution

Asinxron integratsiyada drift yanada jim kechadi: producer message shaklini o'zgartiradi, consumer deserializatsiya xatosi bilan DLQ'ni to'ldiradi. Spring Cloud Contract messaging contract'ni `input`/`outputMessage` juftligi bilan ifodalaydi: provider testi `triggeredBy` metodini chaqirib chiqqan xabarni tekshiradi, consumer tomonda `StubTrigger` bean'i `trigger("order_created")` bilan listener'ga real shakldagi xabarni yuboradi.

```groovy
import org.springframework.cloud.contract.spec.Contract

Contract.make {
    label "order_created"
    input {
        triggeredBy("publishOrderCreated()")
    }
    outputMessage {
        sentTo "orders.created"
        headers { messagingContentType(applicationJson()) }
        body([orderId: "ord-1", amount: 1000, status: "CREATED"])
        bodyMatchers {
            jsonPath('$.orderId', byRegex('ord-[0-9]+'))
            jsonPath('$.amount', byRegex(number()))
        }
    }
}
```

Avro yoki Protobuf ishlatilsa, ikkinchi himoya qatlami - schema registry. Confluent Schema Registry terminologiyasida BACKWARD compatibility yangi schema eski ma'lumotni o'qiy olishini bildiradi (consumer birinchi yangilanadi), FORWARD esa yangi schema bilan yozilgan ma'lumotni eski schema o'qiy olishini (producer birinchi yangilanadi), FULL ikkisini birga talab qiladi, `_TRANSITIVE` variantlari esa faqat oldingi emas, barcha tarixiy versiyalarga nisbatan tekshiradi. CI'da `kafka-schema-registry-maven-plugin`ning `test-compatibility` goal'i yoki Protobuf uchun breaking-change linter'i schema o'zgarishini merge'dan oldin to'xtatadi.

Ogohlantirish: schema compatibility semantik contract emas. `status` maydoniga yangi enum qiymati qo'shilishi Avro uchun mos, lekin consumer'dagi `switch` uchun halokat. Shuning uchun schema registry va messaging contract test bir-birini almashtirmaydi: biri strukturani, ikkinchisi kelishilgan ma'noni himoya qiladi.

## 9.11 OpenAPI'ni contract sifatida ishlatish

Agar provider spec-first ishlasa, OpenAPI fayli tabiiy contract bo'lib xizmat qiladi. Birinchi foydalanish - `openapi-generator-maven-plugin` bilan consumer uchun client generatsiya qilish: spec o'zgarsa, consumer kodi kompilyatsiya bosqichida sinadi, ya'ni signal eng arzon joyda keladi. Ikkinchisi - provider javoblarini spec'ga qarshi validatsiya qilish, buning uchun `swagger-request-validator` kutubxonasi ishlatiladi.

```java
@WebMvcTest(OrderController.class)
class OrderApiSpecComplianceTest {

    @Autowired MockMvc mockMvc;
    @MockitoBean OrderService orderService;

    @Test
    void responseConformsToOpenApiSpec() throws Exception {
        given(orderService.find("ord-1"))
                .willReturn(new OrderView("ord-1", "CREATED", 1000));

        mockMvc.perform(get("/v1/orders/{id}", "ord-1"))
                .andExpect(status().isOk())
                .andExpect(openApi().isValid("openapi/orders-v1.yaml"));
    }
}
```

Uchinchisi - CI'da spec diff'ini breaking change sifatida ushlash: `oasdiff`/`openapi-diff` maydon olib tashlanganini, required qo'shilganini, status kod o'zgarganini aniqlaydi va pipeline'ni to'xtatadi. Cheklovi: OpenAPI provider-driven, ya'ni provider nima qila olishini aytadi, lekin qaysi consumer qaysi maydonga tayanganini bilmaydi. Shuning uchun OpenAPI - keng qamrov, consumer-driven contract - kritik juftliklar uchun.

## 9.12 Contract testni CI'ga qo'yish

Pipeline javobgarligi aniq taqsimlanadi. Consumer build'i contract'ni (yoki pact'ni) yaratadi va broker'ga consumer versiyasi va branch bilan publish qiladi. Provider build'i har commit'da aktual consumer contract'larini verifikatsiya qilib natijani broker'ga qaytaradi; bundan tashqari broker webhook'i yangi contract paydo bo'lganda verification'ni alohida ishga tushiradi - consumer kutganini o'zgartirsa, provider darhol biladi. Deploy oldidan gate `can-i-deploy` bilan qo'yiladi.

```yaml
jobs:
  verify-contracts:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: ./mvnw -B verify -Ppact-provider
        env:
          PACT_BROKER_BASE_URL: ${{ secrets.PACT_BROKER_URL }}
          PACT_BROKER_TOKEN: ${{ secrets.PACT_BROKER_TOKEN }}
          PACT_PROVIDER_VERSION: ${{ github.sha }}
          PACT_PUBLISH_RESULTS: "true"
  can-i-deploy:
    needs: verify-contracts
    runs-on: ubuntu-latest
    steps:
      - run: |
          pact-broker can-i-deploy \
            --pacticipant payment-service \
            --version ${{ github.sha }} \
            --to-environment production \
            --retry-while-unknown 6
```

Provider consumer contract'ini buzsa, provider build'i qizil bo'ladi - bu nosozlik emas, tizimning maqsadi. Hali release qilinmagan kutganlar provider jamoasini bloklamasligi uchun Pact'da pending va WIP pacts bor: yangi contract avval ogohlantiradi, release'dan keyin qattiq gate'ga aylanadi. Deploy tartibi: additive o'zgarishda provider birinchi deploy qilinadi, maydon olib tashlanganda esa avval barcha consumer'lar undan voz kechadi - expand-and-contract (parallel change) usuli. Contract'larni consumer versiyasi va branch bo'yicha versiyalash, muhitlarni tag qilish bu tartibni kuzatiladigan qiladi.

## 9.13 Anti-patternlar

Provider contract'ni o'zi yozib qo'yishi - eng ko'p uchraydigan nosozlik: contract implementatsiyaning ko'zgusiga aylanadi va yangi signal bermaydi, provider o'zini o'zi tasdiqlaydi. Contract manbasi consumer bo'lishi kerak, hatto provider repo'siga pull request sifatida kelsa ham.

Stub'ni qo'lda yangilash: provider o'zgargani haqida Slack'dan bilib, consumer repo'sidagi JSON faylni tahrirlash - contract testing emas, drift'ni qo'lda kuzatish.

Contract testni E2E bilan almashtirish yoki teskarisi. E2E butun oqimni kech va beqaror tekshiradi, contract test juftlik muvofiqligini erta va deterministik; ular turli xavflarni yopadi.

Har bir integratsiyani real servisga urib testlash: suite sekin va flaky bo'ladi, vendor rate limit'iga tiqiladi va oxirida testlar `@Disabled` bo'ladi.

Contract'da hamma narsani aniq qiymat bilan qotirish. Timestamp, UUID, hisoblangan maydonlarni exact match qilish contract'ni mo'rt qiladi - matcher (regex, type) ishlatish kerak.

Verification natijasini e'tiborsiz qoldirish: qizil provider verification'ini `@Disabled` yoki doimiy pending flag bilan yashirish contract testing'ni dekoratsiyaga aylantiradi.

## 9.14 Arxitektor nazorat ro'yxati

- [ ] Har bir tashqi integratsiya uchun qaysi qatlam ishlatilayotgani (mock, in-process stub, WireMock, contract test, sandbox) ro'yxatlangan va asoslangan.
- [ ] Barcha stub server port'lari dinamik va Spring'ga `@DynamicPropertySource` orqali beriladi; test kodida qotirilgan port yo'q.
- [ ] Faqat happy path emas: har bir kritik client uchun timeout, 5xx, buzilgan javob va retry ssenariylari WireMock bilan qoplangan.
- [ ] Kritik servis juftliklari uchun consumer-driven contract bor va stub qo'lda yozilmaydi, balki tasdiqlangan contract'dan generatsiya qilinadi.
- [ ] Provider pipeline'i har commit'da va broker webhook'ida consumer contract'larini verifikatsiya qiladi, natija broker'ga publish qilinadi.
- [ ] Deploy oldidan gate mavjud (`can-i-deploy` yoki stub versiyasi va provider verification tartibi) va u qo'lda chetlab o'tilmaydi.
- [ ] Kafka/AMQP integratsiyalari uchun messaging contract va schema registry compatibility tekshiruvi (BACKWARD/FORWARD siyosati tanlangan) CI'da ishlaydi.
- [ ] Record-and-replay fixture'lari maxfiy ma'lumotdan tozalangan, sanasi belgilangan va qayta yozib olish jadvali bor.

---

[&larr; 8. Testcontainers bilan real infratuzilmada test](08-testcontainers-bilan-real-infratuzilmada.md) · [Mundarija](README.md) · [10. Test ma'lumotlarini boshqarish &rarr;](10-test-malumotlarini-boshqarish.md)
