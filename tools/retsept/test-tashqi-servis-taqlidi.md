# test: tashqi servis taqlidi

Minimal shakl (testing 9.4):

```java
@RestClientTest(value = PaymentClient.class,
        properties = "payment.base-url=https://payments.test")
class PaymentClientTest {
    @Autowired MockRestServiceServer server;
    @Autowired PaymentClient client;

    @Test
    void serverErrorBecomesDomainException() {
        server.expect(requestTo("https://payments.test/v1/charges"))
                .andRespond(withServerError());
        assertThatThrownBy(() -> client.charge(new ChargeRequest("ord-1", 1000)))
                .isInstanceOf(PaymentGatewayException.class);
    }
}
```

Allaqachon bor, yozmang:
- qo'lda server ulash o'rniga `@RestClientTest` `MockRestServiceServer` ni o'zi sozlaydi (testing 9.4)
- qotirilgan port va qo'lda reset o'rniga `WireMockExtension` + `dynamicPort()` (testing 9.2)
- kodda test uchun URL sharti o'rniga `@DynamicPropertySource` + `wm::baseUrl` (testing 9.2)
- qo'lda chaqiruv sanagichi o'rniga `inScenario(...)` (503 keyin 200) (testing 9.2)

Tuzoqlar:
- `failOnUnmatchedRequests(true)` va `verify(...)` yo'q bo'lsa noto'g'ri URL yoki tushgan header jim o'tadi (testing 9.2)
- `MockRestServiceServer` timeout, TLS, pool'ni ko'rmaydi va `WebClient` bilan ishlamaydi: timeout va retry siyosati uchun WireMock (testing 9.4)
- qo'lda yozilgan stub provider o'zgarganda eskiradi (drift): stub tasdiqlangan contract'dan olinsin (testing 9.6)
