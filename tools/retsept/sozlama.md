# sozlama

Minimal shakl (architect 16.6); record ni ro'yxatga olish uchun bittasi yetadi: `@ConfigurationPropertiesScan` yoki `@EnableConfigurationProperties` (clean-code 26.3):

```java
@ConfigurationProperties("acme.payment")
@Validated
public record PaymentProperties(
        @NotNull URI baseUrl,
        @NotBlank String merchantId,
        @DefaultValue("2s") Duration connectTimeout,
        @DefaultValue("5s") Duration readTimeout,
        @Min(0) @Max(5) int maxRetries) {}

@SpringBootApplication
@ConfigurationPropertiesScan
class App {}
```

Allaqachon bor, yozmang:
- tarqoq `@Value("${...:default}")` o'rniga bitta `@ConfigurationProperties` record (code-review 21.5)
- standart qiymat uchun alohida kod emas, `@DefaultValue("5s")` (patterns 5.22)
- qo'lda yozilgan metadata o'rniga `spring-boot-configuration-processor` annotationProcessor (architect 16.6)
- pool uchun o'z `DataSource` kodi o'rniga Boot olib keladigan HikariCP va `spring.datasource.hikari.*` kalitlari (patterns 9.30)

Tuzoqlar:
- `@Validated` qo'yilmasa `@NotBlank` va `@Min` jim e'tiborsiz qoladi, xato prodda chiqadi (architect 16.6)
- parol yoki kalit yml ichida yozilsa git tarixida qoladi: `${JWT_SECRET}` bilan muhitdan oling, topilganini rotatsiya qiling (code-review 21.3)
- timeout va retry alohida tanlansa kutish ko'payib ketadi: urinishlar soni marta timeout yuqori qatlam byudjetidan kichik bo'lsin (code-review 21.2)
