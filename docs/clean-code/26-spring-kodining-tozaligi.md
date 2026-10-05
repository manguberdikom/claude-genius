<!-- doc: clean-code | chapter: 26 | part: VIII. Spring va ma'lumot qatlamida toza kod -->

[Barcha hujjatlar](../../README.md) / [Toza kod qoidalari](README.md)

> Holat: AI yozgan, inson tekshirmagan.

# 26. Spring kodining tozaligi (Clean Code in Spring)

<details>
<summary>Bu bobdagi 11 bo'lim</summary>

- [26.1 Konstruktor inyeksiyasi va `final` maydon](#261-konstruktor-inyeksiyasi-va-final-maydon)
- [26.2 Bean ko'rinishi: `package-private` konfiguratsiya va komponentlar](#262-bean-korinishi-package-private-konfiguratsiya-va-komponentlar)
- [26.3 Konfiguratsiya: `@ConfigurationProperties` record bilan](#263-konfiguratsiya-configurationproperties-record-bilan)
- [26.4 Konfiguratsiyani validatsiya qilish va tez to'xtash](#264-konfiguratsiyani-validatsiya-qilish-va-tez-toxtash)
- [26.5 Controller ni yupqa ushlash](#265-controller-ni-yupqa-ushlash)
- [26.6 DTO va domen o'rtasidagi mapping joyi](#266-dto-va-domen-ortasidagi-mapping-joyi)
- [26.7 Service qatlamida metod nomlari va tranzaksiya chegarasi](#267-service-qatlamida-metod-nomlari-va-tranzaksiya-chegarasi)
- [26.8 `@Qualifier`, `@Primary` va bean nomlari](#268-qualifier-primary-va-bean-nomlari)
- [26.9 Shartli konfiguratsiya va `@Profile` ni kamaytirish](#269-shartli-konfiguratsiya-va-profile-ni-kamaytirish)
- [26.10 Lombok siyosati: xavfsiz va xavfli annotatsiyalar](#2610-lombok-siyosati-xavfsiz-va-xavfli-annotatsiyalar)
- [26.11 Amalda qo'llash](#2611-amalda-qollash)

</details>


Spring mexanikasi [arxitektor hujjatidagi](../architect/README.md) Spring mexanikasi boblarida, Spring patternlari esa [patternlar hujjatida](../patterns/README.md). Bu bobda Spring kodining **yozilish** qoidalari: inyeksiya shakli, bean ko'rinishi, konfiguratsiya, controller va service chegarasi, Lombok siyosati.

## 26.1 Konstruktor inyeksiyasi va `final` maydon

Maydonga inyeksiya (`@Autowired` maydonda) [patternlar hujjatida](../patterns/README.md) anti-pattern sifatida sanalgan (25.29). Bu yerda to'g'ri shaklning aniq ko'rinishi: konstruktor inyeksiyasi, `final` maydon, `@Autowired` siz.

```java
// yaxshi: bitta konstruktor - @Autowired kerak emas (Spring 4.3+)
@Service
public class SettlementService {

    private final PaymentGateway gateway;
    private final PaymentRepository payments;
    private final Clock clock;

    SettlementService(PaymentGateway gateway, PaymentRepository payments, Clock clock) {
        this.gateway = gateway;
        this.payments = payments;
        this.clock = clock;
    }
}
```

Konstruktor inyeksiyasi to'rt foyda beradi: maydonlar `final` bo'ladi (16.1), bog'liqliklar imzoda ko'rinadi, obyekt `new` bilan testda yaratiladi (framework kerak emas), va aylanali bog'liqlik ishga tushishda darhol aniqlanadi.

Bog'liqliklar soni to'rtdan oshsa, bu sinfning juda ko'p ish qilayotgani belgisi - konstruktor parametr soni tabiiy ogohlantirish beradi (5.1).

## 26.2 Bean ko'rinishi: `package-private` konfiguratsiya va komponentlar

Spring beanlari `public` bo'lishi shart emas va `package-private` qilish paket chegarasini mustahkamlaydi ([arxitektor hujjatidagi](../architect/README.md) paketni xususiyat bo'yicha bo'lish bo'limi va 5.9). Shunda boshqa paketdan tasodifiy import qilib bo'lmaydi.

```java
// yaxshi: faqat API public, implementatsiya paket ichida
public interface PaymentApi {           // paketdan chiqadigan yagona tur
    SettlementResult settle(PaymentId id);
}

@Service
class DefaultPaymentApi implements PaymentApi { ... }    // package-private

@Configuration(proxyBeanMethods = false)
class PaymentConfiguration {                              // package-private

    @Bean
    PaymentGateway paymentGateway(PaymentProperties properties) { ... }
}
```

`proxyBeanMethods = false` konfiguratsiya sinfini proxy qilishni o'chiradi: bu tezroq ishga tushishni beradi va `@Bean` metodlari orasidagi yashirin chaqiruvlarni taqiqlaydi (ular oshkor parametr orqali uzatilishi kerak).

## 26.3 Konfiguratsiya: `@ConfigurationProperties` record bilan

`@Value` ni kod bo'ylab tarqatish property tarqoqligiga olib keladi ([patternlar hujjatidagi](../patterns/README.md) property tarqoqligi anti-patterni): sozlamalar ro'yxati hech qayerda to'liq ko'rinmaydi, validatsiya yo'q, va standart qiymatlar takrorlanadi.

```java
// yomon: tarqoq, validatsiyasiz, birligi noaniq
@Value("${shop.payment.timeout:5000}")
private long timeout;

// yaxshi: bir joyda, tipik, validatsiyalangan, birlik turda (3.3)
@ConfigurationProperties("shop.payment")
@Validated
record PaymentProperties(
        @NotNull URI gatewayUrl,
        @NotNull @DurationMin(seconds = 1) @DurationMax(seconds = 30) Duration timeout,
        @Min(0) @Max(5) int maxRetries,
        @NotBlank String merchantId) {

    // Standart qiymatlar bir joyda, kompakt konstruktorda
    PaymentProperties {
        timeout = timeout != null ? timeout : Duration.ofSeconds(5);
    }
}
```

`record` bilan ishlatish uchun `@EnableConfigurationProperties` yoki `@ConfigurationPropertiesScan` kerak, va konstruktor bog'lanishi avtomatik ishlaydi.

## 26.4 Konfiguratsiyani validatsiya qilish va tez to'xtash

Noto'g'ri konfiguratsiya ishga tushishda aniqlanishi kerak, birinchi so'rovda emas. `@Validated` bilan birga Spring Boot ishga tushishni to'xtatadi va aniq xato beradi.

```yaml
# application.yml - har bir kalit prefiks bilan, birligi ko'rinadi (3.13)
shop:
  payment:
    gateway-url: https://gateway.example.uz
    timeout: 5s          # Duration formati
    max-retries: 3
    merchant-id: ${MERCHANT_ID}      # sir muhitdan keladi, kodda emas
```

Ikkinchi qoida: sirlar (`password`, `token`, `secret`) hech qachon `application.yml` da literal sifatida turmaydi - ular muhit o'zgaruvchisi yoki secret manager dan keladi (39.8).

## 26.5 Controller ni yupqa ushlash

Semiz controller [patternlar hujjatida](../patterns/README.md) anti-pattern (25.34). Clean code darajasida controller metodining aniq vazifasi bor va u uch qatordan oshmaydi: kirishni domen turiga aylantirish, use case ni chaqirish, natijani javobga aylantirish.

```java
// yomon: biznes mantiqi controller da
@PostMapping("/refunds")
ResponseEntity<?> refund(@RequestBody Map<String, Object> body) {
    Long paymentId = Long.valueOf(body.get("paymentId").toString());
    Payment payment = repository.findById(paymentId).orElse(null);
    if (payment == null) return ResponseEntity.notFound().build();
    if (!"SETTLED".equals(payment.getStatus())) return ResponseEntity.badRequest().build();
    ...
}

// yaxshi: yupqa, mantiq service da, xato ishlovi markazda (27.3)
@PostMapping("/refunds")
@ResponseStatus(HttpStatus.CREATED)
RefundResponse refund(@Valid @RequestBody RefundRequest request) {
    Refund refund = refunds.create(request.toCommand());
    return RefundResponse.from(refund);
}
```

## 26.6 DTO va domen o'rtasidagi mapping joyi

Mapping qayerda turishi aniq qaror bo'lishi kerak, aks holda u hamma joyda takrorlanadi. Uchta ishlaydigan joy bor va ularning tanlovi loyiha hajmiga bog'liq.

| Joy | Qachon | Shakli |
|---|---|---|
| DTO ichida statik fabrika | kichik va o'rta loyiha | `RefundResponse.from(refund)` |
| Alohida mapper sinfi | mapping murakkab, qoida bor | `RefundMapper` (`@Component`) |
| MapStruct | DTO ko'p, maydonlar bir xil | generatsiya, `@Mapper` |
| Domen ichida | hech qachon | domen DTO ni bilmasligi kerak |

Qoida: domen obyekti DTO ni bilmaydi (bog'liqlik yo'nalishi, [arxitektor hujjatidagi](../architect/README.md) bog'liqlik yo'nalishi bo'limi); shuning uchun mapping DTO tomonda yoki alohida sinfda turadi.

## 26.7 Service qatlamida metod nomlari va tranzaksiya chegarasi

Service metodlari **use case** nomini olishi kerak, CRUD nomini emas: `cancelOrder`, `reserveStock`, `settlePayment` - `update`, `process`, `handle` emas (2.4 va 3.9).

Tranzaksiya chegarasi va `@Transactional` mexanikasi [arxitektor hujjatidagi](../architect/README.md) Spring tranzaksiyalari bo'limida berilgan. Clean code darajasidagi ikki qoida: `@Transactional` service qatlamida turadi (controller yoki repository da emas), va `readOnly = true` o'qish metodlarida oshkor belgilanadi.

```java
@Service
class DefaultRefundService implements RefundService {

    @Override
    @Transactional                                  // yozish: standart
    public Refund create(RefundCommand command) { ... }

    @Override
    @Transactional(readOnly = true)                 // o'qish: oshkor
    public Page<RefundSummary> search(RefundCriteria criteria, Pageable pageable) { ... }
}
```

## 26.8 `@Qualifier`, `@Primary` va bean nomlari

Bir interfeysning bir nechta implementatsiyasi bo'lganda tanlovni oshkor qilish kerak. `@Primary` yashirin tanlov beradi va u faqat haqiqiy "standart" bo'lganda haqli; qolgan hollarda `@Qualifier` yoki alohida tur aniqroq.

```java
// yomon: @Primary yashirin - qaysi bean inyeksiya qilinishi kodda ko'rinmaydi
@Service @Primary class StripeGateway implements PaymentGateway { }
@Service class SandboxGateway implements PaymentGateway { }

// yaxshi: tanlov oshkor va nomlangan
@Service @Qualifier("stripe") class StripeGateway implements PaymentGateway { }

SettlementService(@Qualifier("stripe") PaymentGateway gateway) { ... }

// eng yaxshi: konfiguratsiya tanlaydi, kod bitta turni ko'radi
@Bean
PaymentGateway paymentGateway(PaymentProperties properties, ...) {
    return switch (properties.provider()) {
        case STRIPE -> new StripeGateway(...);
        case SANDBOX -> new SandboxGateway(...);
    };
}
```

## 26.9 Shartli konfiguratsiya va `@Profile` ni kamaytirish

Profil tarqoqligi [patternlar hujjatida](../patterns/README.md) anti-pattern (25.39). Clean code qoidasi: `@Profile` ni **kod** da emas, konfiguratsiyada hal qilish - xatti-harakat farqi property qiymati bilan boshqarilsa, muhitlar orasidagi farq bir faylda ko'rinadi.

```java
// yomon: profil kod bo'ylab tarqalgan, nima farq qilishi ko'rinmaydi
@Service @Profile("!prod") class FakeSmsSender implements SmsSender { }
@Service @Profile("prod") class RealSmsSender implements SmsSender { }

// yaxshi: xususiyat bayrog'i konfiguratsiyada, bitta joyda ko'rinadi
@Bean
@ConditionalOnProperty(name = "shop.sms.mode", havingValue = "real")
SmsSender realSmsSender(SmsProperties properties) { ... }

@Bean
@ConditionalOnMissingBean(SmsSender.class)
SmsSender loggingSmsSender() { ... }
```

## 26.10 Lombok siyosati: xavfsiz va xavfli annotatsiyalar

Lombok kodni qisqartiradi, lekin ba'zi annotatsiyalari yashirin xatti-harakat qo'shadi. Jamoada aniq siyosat bo'lishi kerak va u hujjatlashtirilishi lozim ([SonarQube hujjatidagi](../sonarqube/README.md) Lombok va generatsiya qilingan kod bo'limi Lombok va generatsiya qilingan kod ko'rib chiqiladi).

| Annotatsiya | Siyosat | Sabab |
|---|---|---|
| `@Getter` | ruxsat | shaffof |
| `@RequiredArgsConstructor` | ruxsat (26.1 bilan) | konstruktor inyeksiyasi |
| `@Builder` | ruxsat, validatsiya bilan (16.5) | majburiy maydonlar tekshirilmaydi |
| `@Slf4j` | ruxsat | standart logger |
| `@Value` (Lombok) | ehtiyotkorlik | `record` afzal |
| `@Data` | **taqiqlangan** | setter + `equals` + `toString` birga |
| `@EqualsAndHashCode` entitetda | **taqiqlangan** | assotsiatsiyalarni yuklaydi (28.1) |
| `@ToString` entitetda | **taqiqlangan** | lazy yuklash, sezgir ma'lumot (15.7) |
| `@SneakyThrows` | **taqiqlangan** | istisno imzodan yashiriladi (24.7) |
| `@Setter` domenda | taqiqlangan | inkapsulyatsiyani buzadi (16.7) |

## 26.11 Amalda qo'llash

- [ ] Barcha maydon inyeksiyalarini (`@Autowired` maydonda) konstruktor inyeksiyasiga o'tkazib, maydonlarni `final` qiling.
- [ ] Beanlar va konfiguratsiya sinflarini `package-private` qilib, paketdan faqat API turlarini chiqaring.
- [ ] `@Value` chaqiruvlarini `@ConfigurationProperties` record larga birlashtirib, `@Validated` qo'shing.
- [ ] Konfiguratsiya kalitlarida birlik va prefiks borligini tekshirib, sirlarni muhit o'zgaruvchisiga ko'chiring.
- [ ] Controller metodlarini uch qatorga qisqartirib, biznes mantiqini service ga ko'chiring.
- [ ] Mapping joyini bitta konvensiyaga keltirib (DTO fabrikasi yoki mapper), takrorlangan mappinglarni birlashtiring.
- [ ] `@Primary` ishlatilgan joylarni `@Qualifier` yoki konfiguratsiyadagi oshkor tanlovga almashtiring.
- [ ] Lombok siyosatini yozib, `@Data`, `@SneakyThrows` va entitetdagi `@EqualsAndHashCode` ni ArchUnit bilan taqiqlang.

---

[&larr; 25. Java kodidagi umumiy tuzoqlar](25-java-kodidagi-umumiy-tuzoqlar.md) · [Mundarija](README.md) · [27. REST API kodining o'qilishi &rarr;](27-rest-api-kodining-oqilishi.md)
