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
- qo'lda mijoz klassi o'rniga `@HttpExchange` interfeysi va `HttpServiceProxyFactory` (patterns 7.29)
- har mijozda timeout kodi o'rniga yaml: Boot 4 `spring.http.clients.connect-timeout`/`read-timeout`, 3.4/3.5 `spring.http.client.*` (architect 32.2)
- retry sikli o'rniga `@Retryable(includes = ..., jitter = ...)` va `@EnableResilientMethods` (patterns 17.40)
- qo'lda holat hisoblagich o'rniga Resilience4j `@CircuitBreaker` va yaml (code-review 22.3)

Tuzoqlar:
- `RestClient.create()` timeout qo'ymaydi; alohida byudjetga `.requestFactory(ClientHttpRequestFactoryBuilder.detect().build(settings))`, settings Boot 4 `HttpClientSettings`, 3.4/3.5 `ClientHttpRequestFactorySettings` (code-review 22.1)
- `includes` tor: `ResourceAccessException` (ulanish, timeout) va 502/503/504 uchun alohida domen istisnosi; umumiy `PaymentGatewayException` retry da 4xx rad javobi ham takrorlanadi (code-review 22.2)
- kalitsiz POST retry ikki marta to'lov: `Idempotency-Key` buyruqdan olinadi, urinishlarda bir xil (code-review 22.2)
- qo'lda mijozda `refund` kabi ikkinchi endpoint zanjirni nusxalamaydi (bir sababga o'zgaradi): header, kalit `private post(path, body, key)` da, xato handlerda; `@HttpExchange` da `@RequestHeader("Idempotency-Key")` (code-review 7.5, 22.1, patterns 7.29)
- fallback muvaffaqiyat qaytarsa yolg'on natija domenga kiradi: `pending` kabi rost holat, metrikada sanang (code-review 22.3)
