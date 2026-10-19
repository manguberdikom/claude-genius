# konfiguratsiya

Minimal shakl (clean-code 26.2); `PaymentProperties` sozlama, `paymentClient` tashqi-chaqiruv kartasidan:

```java
@Configuration(proxyBeanMethods = false)
class PaymentConfiguration {

    @Bean
    PaymentGateway paymentGateway(@Qualifier("paymentClient") RestClient client, PaymentProperties props) {
        return new HttpPaymentGateway(client, props.merchantId());
    }
}
```

Allaqachon bor, yozmang:
- Boot bergan `ObjectMapper` modullar va `spring.jackson.*` ni saqlaydi, `new ObjectMapper()` bean yozilmaydi (code-review 18.7); avval `spring.jackson.*` xossalari (clean-code 27.6), kod kerak bo'lsa Boot 3 da `Jackson2ObjectMapperBuilderCustomizer`, Boot 4 da Jackson 3 `JsonMapper` builder customizer (architect 32.10, patterns 6.20)
- `RestClient` ni noldan qurish o'rniga Boot bergan `RestClient.Builder` parametri (patterns 1.14)
- starterda `@Configuration` va alohida `@AutoConfigureAfter` o'rniga `@AutoConfiguration(after = ...)`, `proxyBeanMethods = false` o'zi qo'yiladi (architect 16.2)

Tuzoqlar:
- `@Bean` metodini boshqa `@Bean` ichidan chaqirish proxy bor yo'qligiga qarab singleton yoki yangi obyekt beradi: bog'liqlikni metod parametri qilib oling (code-review 18.3)
- bir turdagi ikki bean (masalan ikki `RestClient`) inyeksiyada noaniq: har birini `@Qualifier` bilan oling (code-review 18.3)
- `@Profile("!prod")` bilan soxta bean prod yo'lini sinovsiz qoldiradi: muhit farqi xossa qiymatida, soxtasi `@TestConfiguration` da bo'lsin (code-review 21.4)
