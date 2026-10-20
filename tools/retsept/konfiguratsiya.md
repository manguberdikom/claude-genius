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
- `new ObjectMapper()` bean yo'q: avval `spring.jackson.*`, kod kerak bo'lsa Boot 3 `Jackson2ObjectMapperBuilderCustomizer`, Boot 4 Jackson 3 `JsonMapper` builder customizer (code-review 18.7, clean-code 27.6)
- tarqoq `@Value("${..:default}")` o'rniga bitta `@ConfigurationProperties` + `@Validated` record, standart qiymat `@DefaultValue` (code-review 21.5, architect 16.6)
- `RestClient` ni noldan qurish o'rniga Boot bergan `RestClient.Builder` parametri (patterns 1.14)
- starterda `@Configuration` va alohida `@AutoConfigureAfter` o'rniga `@AutoConfiguration(after = ...)`, `proxyBeanMethods = false` o'zi qo'yiladi (architect 16.2)

Tuzoqlar:
- `@Bean` metodini boshqa `@Bean` ichidan chaqirish proxy bor yo'qligiga qarab singleton yoki yangi obyekt beradi: bog'liqlikni metod parametri qilib oling (code-review 18.3)
- bir turdagi ikki bean (masalan ikki `RestClient`) inyeksiyada noaniq: har birini `@Qualifier` bilan oling (code-review 18.3)
- `@Profile("!prod")` bilan soxta bean prod yo'lini sinovsiz qoldiradi: muhit farqi xossa qiymatida, soxtasi `@TestConfiguration` da bo'lsin (code-review 21.4)
