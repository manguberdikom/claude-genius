# tashqi chaqiruv

Minimal shakl (code-review 22.1):

```java
@Bean
RestClient paymentClient(RestClient.Builder builder, PaymentProperties props) {
    return builder.baseUrl(props.baseUrl())
        .defaultStatusHandler(HttpStatusCode::isError, (req, res) -> {
            throw new PaymentGatewayException(res.getStatusCode());
        })
        .build();
}
```

Allaqachon bor, yozmang:
- qo'lda mijoz klassi o'rniga `@HttpExchange` interfeysi, `HttpServiceProxyFactory` (patterns 7.29)
- timeout kodi o'rniga yaml: Boot 4 `spring.http.clients.connect-timeout`/`read-timeout`, 3.4/3.5 `spring.http.client.*` (architect 32.2)
- retry sikli, qo'lda circuit o'rniga `@Retryable`, `@CircuitBreaker`: chidamlilik kartasi (Boot 3 spring-retry, Spring 7) (code-review 22.2, 22.3)

Tuzoqlar:
- `RestClient.create()`, `new RestTemplate()` yaml timeoutni ko'rmaydi: inject qilingan `RestClient.Builder`; kodda `.requestFactory(ClientHttpRequestFactoryBuilder.detect().build(settings))` faqat yaml dan farqli byudjetga, qiymat `@ConfigurationProperties` dan (Boot 4 `HttpClientSettings`, 3.4/3.5 `ClientHttpRequestFactorySettings`) (code-review 22.1, architect 32.2)
- retry ro'yxati tor: `ResourceAccessException` va 502/503/504 uchun alohida istisno, umumiy `PaymentGatewayException` da 4xx rad ham takrorlanadi (code-review 22.2)
- kalitsiz POST retry ikki marta to'lov: `Idempotency-Key` buyruqdan, urinishlarda bir xil; provayder uni qo'llashi taxmin: `Ochiq qaror` (code-review 22.2)
- ikkinchi endpoint (`refund`) zanjirni nusxalamaydi: header, kalit, xato handler `private post(path, body, key)` da, `@HttpExchange` da `@RequestHeader("Idempotency-Key")` (code-review 7.5, patterns 7.29)
- fallback yolg'on muvaffaqiyat qaytarmaydi: `pending` kabi rost holat, metrikada sanaladi (code-review 22.3)
