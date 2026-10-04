<!-- doc: architect | chapter: 16 | part: III. Spring chuqur bilim -->

[Kod yozadigan arxitektorning miyyasi](../../README.md) / [Arxitektor miyyasi](README.md)

# 16. Spring Boot mexanikasi: auto-configuration, starter, Actuator (Spring Boot Mechanics)

<details>
<summary>Bu bobdagi 12 bo'lim</summary>

- [16.1 Auto-configuration qanday ishlaydi: `AutoConfiguration.imports` va shartli annotatsiyalar](#161-auto-configuration-qanday-ishlaydi-autoconfigurationimports-va-shartli-annotatsiyalar)
- [16.2 `@ConditionalOnClass`, `@ConditionalOnMissingBean` va tartib (`@AutoConfigureAfter`)](#162-conditionalonclass-conditionalonmissingbean-va-tartib-autoconfigureafter)
- [16.3 Auto-configuration ni tekshirish: `--debug` va shartlar hisoboti](#163-auto-configuration-ni-tekshirish---debug-va-shartlar-hisoboti)
- [16.4 Starter yozish: o'z jamoangiz uchun umumiy kutubxona qurish qoidalari](#164-starter-yozish-oz-jamoangiz-uchun-umumiy-kutubxona-qurish-qoidalari)
- [16.5 Konfiguratsiya manbalari tartibi va ustunlik qoidasi](#165-konfiguratsiya-manbalari-tartibi-va-ustunlik-qoidasi)
- [16.6 `@ConfigurationProperties` va validatsiya, `application.yaml` tuzilishi](#166-configurationproperties-va-validatsiya-applicationyaml-tuzilishi)
- [16.7 Profil (profile) dan to'g'ri foydalanish va uning tuzoqlari](#167-profil-profile-dan-togri-foydalanish-va-uning-tuzoqlari)
- [16.8 Actuator: health, metrics, env, httpexchanges va ularning xavfsizligi](#168-actuator-health-metrics-env-httpexchanges-va-ularning-xavfsizligi)
- [16.9 Health indicator yozish va readiness va liveness farqi](#169-health-indicator-yozish-va-readiness-va-liveness-farqi)
- [16.10 Ishga tushish vaqti: lazy initialization, AOT va native image ta'siri](#1610-ishga-tushish-vaqti-lazy-initialization-aot-va-native-image-tasiri)
- [16.11 Spring Boot 3 ga o'tish: Jakarta nomlari va konfiguratsiya o'zgarishlari](#1611-spring-boot-3-ga-otish-jakarta-nomlari-va-konfiguratsiya-ozgarishlari)
- [16.12 Amalda qo'llash](#1612-amalda-qollash)

</details>


Spring Boot ko'pchilik uchun "sehr" bo'lib ko'rinadi, lekin ichida sehr yo'q. Bor-yo'g'i classpath da nima borligini o'qiydigan shartli konfiguratsiya mexanizmi va bean ni faqat foydalanuvchi o'zi bermagan holda yaratadigan qoida bor. Arxitektor uchun bu mexanikani bilish ikki narsani beradi: ishga tushmayotgan kontekstni daqiqalarda emas, sekundlarda tushuntirish, va o'z jamoasi uchun to'g'ri sozlanadigan umumiy kutubxona qurish. Quyida auto-configuration ning ichki ishlashi, konfiguratsiya ustunligi, Actuator ning xavfsiz qismi va startup vaqtini qisqartirish yo'llari ko'rib chiqiladi.

## 16.1 Auto-configuration qanday ishlaydi: `AutoConfiguration.imports` va shartli annotatsiyalar

`@SpringBootApplication` ichida `@EnableAutoConfiguration` bor, u esa `AutoConfigurationImportSelector` ni ishga soladi. Bu selector classpath dagi barcha jar lardan `META-INF/spring/org.springframework.boot.autoconfigure.AutoConfiguration.imports` faylini o'qiydi. Fayl oddiy matn: har qatorda bitta konfiguratsiya sinfining to'liq nomi. Spring Boot 2.7 gacha bu ro'yxat `META-INF/spring.factories` ichida edi, 3.x da faqat yangi format o'qiladi.

Keyingi qadam filtrlash. Boot ro'yxatdagi yuzlab sinfni darhol yuklamaydi, avval `spring-autoconfigure-metadata.properties` orqali `@ConditionalOnClass` shartlarini ASM bilan tekshiradi. Shu sababli `DataSourceAutoConfiguration` sizda JDBC driver bo'lmasa, umuman sinf sifatida yuklanmaydi. Bu startup ni sezilarli tezlashtiradi: tipik servisda ro'yxatdagi 150 dan ortiq nomzoddan odatda 25-40 tasi qoladi.

```properties
# to'lov servisi uchun o'z starter faylimiz
# src/main/resources/META-INF/spring/
#   org.springframework.boot.autoconfigure.AutoConfiguration.imports
com.acme.payment.autoconfigure.PaymentClientAutoConfiguration
com.acme.payment.autoconfigure.PaymentRetryAutoConfiguration
com.acme.payment.autoconfigure.PaymentMetricsAutoConfiguration
```

Muhim nuance: auto-configuration sinflari oddiy `@Configuration` dan keyin qayta ishlanadi. Ya'ni sizning ilovangizdagi `@Configuration` va `@Component` lar har doim birinchi ro'yxatga olinadi, auto-configuration esa oxirida "bo'sh joylarni to'ldiradi". Shuning uchun `@ConditionalOnMissingBean` ishlaydi: sizning bean ingiz allaqachon registratsiyada bo'ladi.

## 16.2 `@ConditionalOnClass`, `@ConditionalOnMissingBean` va tartib (`@AutoConfigureAfter`)

`@ConditionalOnClass` javobgarligi: "bu integratsiya umuman mumkinmi". `@ConditionalOnMissingBean` javobgarligi: "foydalanuvchi o'zi bermaganmi". `@ConditionalOnProperty` javobgarligi: "buni yoqishni xohlashdimi". Uchtasini aralashtirmaslik kerak. Masalan Kafka client classpath da bo'lsa ham, ombor qoldig'i eventlarini yuborish `acme.inventory.events.enabled=true` bo'lmaganda yoqilmasligi kerak.

Spring Boot 3.x da auto-configuration sinfi `@Configuration` emas, `@AutoConfiguration` bilan belgilanadi. Bu annotatsiya `proxyBeanMethods = false` ni o'zi o'rnatadi va tartibni to'g'ridan-to'g'ri atributlarda qabul qiladi: `@AutoConfiguration(after = DataSourceAutoConfiguration.class)`. Alohida `@AutoConfigureAfter` va `@AutoConfigureBefore` ham ishlaydi, lekin yangi kodda atributlar afzal.

```java
@AutoConfiguration(after = { DataSourceAutoConfiguration.class })
@ConditionalOnClass(name = "com.acme.payment.sdk.PaymentGateway")
@ConditionalOnProperty(prefix = "acme.payment", name = "enabled",
                       matchIfMissing = true)
@EnableConfigurationProperties(PaymentProperties.class)
public class PaymentClientAutoConfiguration {

    // foydalanuvchi o'z PaymentGateway ini bersa, biz chetga chiqamiz
    @Bean
    @ConditionalOnMissingBean
    PaymentGateway paymentGateway(PaymentProperties props,
                                  RestClient.Builder builder) {
        RestClient client = builder
                .baseUrl(props.baseUrl())
                .requestFactory(timeouts(props))   // connect 2s, read 5s
                .build();
        return new HttpPaymentGateway(client, props.merchantId());
    }
}
```

Tartib faqat auto-configuration lar orasidagi `@ConditionalOnMissingBean` natijasiga ta'sir qiladi. Agar `A` auto-config `B` ning bean iga qarab qaror qilsa, `A` majburan `B` dan keyin ishlashi kerak, aks holda shart tasodifiy natija beradi. Bu eng ko'p uchraydigan xato: tartib ko'rsatilmagan, lokal mashinada ishlaydi, CI da sinadi.

## 16.3 Auto-configuration ni tekshirish: `--debug` va shartlar hisoboti

`--debug` flagi bilan ishga tushirish `ConditionEvaluationReport` ni konsolga chiqaradi. U uch blokdan iborat: `Positive matches` (nima yoqildi va nima uchun), `Negative matches` (nima yoqilmadi va qaysi shart bajarilmadi), `Exclusions` va `Unconditional classes`. Bu hisobot "nega mening `DataSource` im yaratilmadi" savoliga to'g'ridan-to'g'ri javob beradi.

```bash
# shartlar hisobotini olish va kerakli qismni filtrlash
java -jar payment-service.jar --debug 2>&1 | tee startup.log
grep -A 5 "DataSourceAutoConfiguration" startup.log

# Actuator orqali ishlayotgan ilovada
curl -s localhost:8081/actuator/conditions \
  | jq '.contexts.application.negativeMatches
        | to_entries | map(select(.key | test("Payment")))'
```

Ishlab chiqarishda `--debug` ishlatish o'rinli emas, chunki u root logger ni DEBUG ga o'tkazmaydi lekin hisobot hajmi katta. Buning o'rniga `conditions` endpoint ni staging da yoqib qo'yish yetarli. Test darajasida esa auto-configuration ni to'liq kontekst ko'tarmasdan `ApplicationContextRunner` bilan tekshirish mumkin: u shartlarni real tarzda baholaydi va taxminan 20-50 ms da natija beradi.

```java
private final ApplicationContextRunner runner = new ApplicationContextRunner()
        .withConfiguration(AutoConfigurations.of(PaymentClientAutoConfiguration.class));

@Test
void foydalanuvchiBeani_ustunlikQiladi() {
    runner.withUserConfiguration(CustomGatewayConfig.class)
          .withPropertyValues("acme.payment.base-url=https://pay.local")
          .run(ctx -> assertThat(ctx).getBean(PaymentGateway.class)
                                     .isSameAs(ctx.getBean("myGateway")));
}

@Test
void ocharishMumkin() {
    runner.withPropertyValues("acme.payment.enabled=false")
          .run(ctx -> assertThat(ctx).doesNotHaveBean(PaymentGateway.class));
}
```

## 16.4 Starter yozish: o'z jamoangiz uchun umumiy kutubxona qurish qoidalari

Starter ikki artefaktdan iborat bo'lishi kerak: `acme-payment-spring-boot-autoconfigure` (kod va shartlar) va `acme-payment-spring-boot-starter` (faqat dependency ro'yxati, kodsiz). Nomlash qoidasi qat'iy: `spring-boot-starter-` prefiksi Spring jamoasiga tegishli, sizning starter `acme-payment-spring-boot-starter` ko'rinishida bo'lishi kerak. Bu shunchaki odob emas, Maven koordinatalarining kim tomonidan qo'llab-quvvatlanishini aytib turadi.

Starter ichida hech qachon `spring-boot-starter-web` yoki boshqa katta starter ni majburiy dependency qilib qo'ymang. Foydalanuvchi reactive stack da bo'lishi mumkin. Integratsiya kutubxonasini `optional` yoki `provided` qilib, mavjudligini `@ConditionalOnClass` bilan tekshirish to'g'ri yo'l. Shuningdek `@ComponentScan` ni starter ichida ishlatmang: u foydalanuvchi paketini skanerlashga urinadi va kutilmagan bean lar keltirib chiqaradi. Faqat aniq `@Bean` metodlari va `@Import`.

| Qaror | Oddiy yondashuv | Arxitektor yondashuvi |
|---|---|---|
| Starter tuzilishi | bitta jar, hammasi ichida | autoconfigure va starter alohida, dependency lar `optional` |
| Bean e'lon qilish | `@Component` va `@ComponentScan` | `@Bean` + `@ConditionalOnMissingBean`, skan yo'q |
| Yoqish/o'chirish | kod o'zgartirib o'chiriladi | `@ConditionalOnProperty` va `matchIfMissing` |
| Sozlash | statik `final` konstantalar | `@ConfigurationProperties` + metadata generator |
| Versiya boshqaruvi | har joyda qo'lda versiya | `spring-boot-dependencies` BOM + o'z BOM |
| Tartib | tasodifga tashlanadi | `@AutoConfiguration(after = ...)` aniq ko'rsatiladi |
| Tekshirish | qo'lda ilova ko'tarib sinaladi | `ApplicationContextRunner` bilan shart matritsasi |
| Monitoring | starter metrikasiz chiqadi | `MeterBinder` beriladi, prefiks `acme.payment.*` |
| Buzuvchi o'zgarish | xossa nomi jim o'zgaradi | eski nom deprecated metadata bilan 2 relizda saqlanadi |

## 16.5 Konfiguratsiya manbalari tartibi va ustunlik qoidasi

Spring Boot konfiguratsiyani `Environment` ichidagi tartiblangan `PropertySource` ro'yxatidan o'qiydi. Yuqoridagi manba pastdagini yopadi. Amalda eng ko'p kerak bo'ladigan tartib yuqoridan pastga: command line argumentlar, `SPRING_APPLICATION_JSON`, JVM system property lari (`-D`), OS environment o'zgaruvchilari, jar tashqarisidagi profil fayllari, jar tashqarisidagi `application.yaml`, jar ichidagi profil fayllari, jar ichidagi `application.yaml`, `@PropertySource`, va oxirida `SpringApplication.setDefaultProperties` bilan berilgan qiymatlar.

Bu tartibdan kelib chiqadigan amaliy qoida: Kubernetes da sirlarni environment o'zgaruvchisi sifatida bering, chunki u jar ichidagi har qanday qiymatni yopadi va image ni qayta qurishni talab qilmaydi. Relaxed binding tufayli `ACME_PAYMENT_BASE_URL` o'zgaruvchisi `acme.payment.base-url` xossasiga avtomatik tushadi.

```yaml
# application.yaml - bitta fayl, profil bo'limlari `---` bilan ajratiladi
acme:
  payment:
    base-url: https://pay.sandbox.acme.internal
    connect-timeout: 2s          # Duration tipi, 2s / 500ms / PT2S qabul qiladi
    read-timeout: 5s
    max-retries: 3
spring:
  config:
    # tashqi fayl va vault: topilmasa yiqilmasin
    import: "optional:file:/etc/acme/payment.yaml,optional:configtree:/run/secrets/"
---
spring:
  config:
    activate:
      on-profile: prod
acme:
  payment:
    base-url: https://pay.acme.com
    max-retries: 5
```

`spring.config.import` Boot 2.4 dan beri mavjud va `spring.config.location` ni ko'p holatda almashtiradi. `optional:` prefiksi fayl yo'q bo'lsa ishga tushishni to'xtatmaydi. `configtree:` esa Kubernetes Secret ni fayl sifatida mount qilganda har bir faylni xossaga aylantiradi, bu sirlarni yaml ga yozishdan xavfsizroq.

## 16.6 `@ConfigurationProperties` va validatsiya, `application.yaml` tuzilishi

`@Value` bitta-ikkita qiymat uchun yetarli, lekin to'rt-besh xossadan keyin `@ConfigurationProperties` ga o'tish kerak. Sababi: guruhlangan tipli obyekt, IDE da avtomatik to'ldirish, va eng muhimi ishga tushish paytida validatsiya. Boot 3.x da record bilan constructor binding standart holat: bir dona konstruktor bo'lsa `@ConstructorBinding` yozish shart emas, natijada immutable konfiguratsiya obyekti chiqadi.

```java
@ConfigurationProperties(prefix = "acme.payment")
@Validated
public record PaymentProperties(
        @NotBlank String merchantId,
        @NotNull URI baseUrl,
        @DefaultValue("2s") Duration connectTimeout,
        @DefaultValue("5s") Duration readTimeout,
        @Min(0) @Max(5) int maxRetries,
        @Valid Circuit circuit) {

    public record Circuit(
            @DefaultValue("50") @Min(1) @Max(100) int failureRatePercent,
            @DefaultValue("30s") Duration openStateDuration) {}
}
```

`@Validated` bo'lmasa `@NotBlank` hech narsa qilmaydi, bu juda keng tarqalgan jim xato. Validatsiya ishga tushishda bajariladi va noto'g'ri konfiguratsiya pod ni Readiness ga chiqarmaydi. Bu xohlangan xatti-harakat: noto'g'ri sozlangan to'lov servisi ishlamagani yaxshi, yarim ishlagandan ko'ra. `spring-boot-configuration-processor` ni `annotationProcessor` sifatida qo'shsangiz, `META-INF/spring-configuration-metadata.json` generatsiya bo'ladi va jamoa IDE da xossa nomlarini taklif sifatida ko'radi.

Yaml tuzilishi haqida: bitta ildiz prefiks (`acme`) ostida barcha o'z xossalaringizni saqlang, `spring.*` ichiga hech narsa qo'shmang. Bu konflikt ehtimolini nolga tushiradi va `configprops` endpoint da sizning sozlamalaringiz bir joyda ko'rinadi.

## 16.7 Profil (profile) dan to'g'ri foydalanish va uning tuzoqlari

Profil ikki xil narsa uchun ishlatiladi va faqat bittasi to'g'ri. To'g'ri ishlatish: muhitga bog'liq QIYMATLARNI almashtirish (URL, pool kattaligi, log darajasi). Noto'g'ri ishlatish: `@Profile` bilan bean larni almashtirib, muhitlar o'rtasida har xil kod yo'lini yaratish. Ikkinchi holatda prod da ishlaydigan kod hech qachon test qilinmagan bo'lib chiqadi.

`spring.profiles.active` ni `application.yaml` ichida yozish zararli odat, chunki u bilan dev profil jar ga kirib ketadi. Faqat tashqaridan bering: `SPRING_PROFILES_ACTIVE=prod`. `spring.profiles.group` bilan bir profil ostida bir nechtasini birlashtirish mumkin, masalan `prod` ichiga `prod-db` va `prod-cache` kiradi. Profilga xos faylda `spring.profiles.active` ni qayta e'lon qilish mumkin emas, Boot bunda xato bilan to'xtaydi.

| Tuzoq | Nega sodir bo'ladi | Yechim |
|---|---|---|
| `@Profile("!prod")` bilan mock to'lov gateway | prod yo'li hech qachon ishlatilmaydi | yondashuv xossaga o'tkaziladi, barcha muhitda bir kod |
| `application.yaml` da `spring.profiles.active: dev` | jar ichidagi standart dev bo'lib qoladi | faqat `SPRING_PROFILES_ACTIVE` orqali |
| Yaml ro'yxati profil bilan "birlashadi" deb o'ylash | ro'yxat merge bo'lmaydi, butunlay almashadi | to'liq ro'yxatni har profilda qayta yozish |
| `@ConfigurationProperties` validatsiyasi ishlamaydi | `@Validated` qo'yilmagan | sinfga `@Validated`, ichki obyektga `@Valid` |
| `@ConditionalOnMissingBean` tasodifiy ishlaydi | auto-config tartibi ko'rsatilmagan | `@AutoConfiguration(after = ...)` |
| Actuator barcha endpoint ni ochib yuboradi | `exposure.include: "*"` yozilgan | faqat kerakli ro'yxat, `management.server.port` alohida |
| Liveness probe DB ni tekshiradi | custom indicator liveness guruhida | DB faqat readiness guruhida bo'ladi |
| Lazy init prod da xatoni kechiktiradi | `spring.main.lazy-initialization=true` hammaga | lazy faqat lokal dev uchun |
| Boot 3 ga o'tishda xossa jim o'chadi | nomi o'zgargan, xato chiqmaydi | `spring-boot-properties-migrator` bir relizga qo'shiladi |

## 16.8 Actuator: health, metrics, env, httpexchanges va ularning xavfsizligi

Actuator ning standart holati konservativ: web orqali faqat `health` ochiq. Qolganini `management.endpoints.web.exposure.include` bilan ataylab ochish kerak. Bu ro'yxatga `*` yozish eng tez yo'l va eng xavfli qaror, chunki `env`, `configprops`, `heapdump` va `threaddump` birdan ochiladi. `heapdump` butun xotirani, ya'ni karta raqamlari va token larni diskka yozadi.

```yaml
management:
  server:
    port: 8081                 # asosiy trafikdan ajratilgan port
  endpoints:
    web:
      exposure:
        include: health,info,metrics,prometheus,loggers
  endpoint:
    health:
      show-details: when-authorized
      probes:
        enabled: true
      group:
        readiness:
          include: readinessState,db,paymentGateway
        liveness:
          include: livenessState
    env:
      show-values: never       # Boot 3.x: never | always | when-authorized
    configprops:
      show-values: never
  httpexchanges:
    recording:
      include: request-headers,response-headers,time-taken
```

`management.server.port` ni alohida qilish arxitektura darajasidagi qaror: shunda Ingress faqat 8080 ni tashqariga chiqaradi, 8081 esa cluster ichida qoladi. `httpexchanges` ishlashi uchun `HttpExchangeRepository` bean kerak, `InMemoryHttpExchangeRepository` standart holda taxminan oxirgi 100 ta so'rovni saqlaydi. Uni debug uchun yoqish mumkin, lekin `authorization` va `cookie` header larini hech qachon include ro'yxatiga qo'shmang.

Metrikalar tomonida `http.server.requests` timer eng qimmatli signal. Latency taqsimotini olish uchun `management.metrics.distribution.percentiles-histogram.http.server.requests=true` ni yoqish kerak, aks holda Prometheus da faqat o'rtacha qiymat bo'ladi. Histogram har bir tag kombinatsiyasi uchun taxminan 70 ta qo'shimcha seriya yaratadi, shuning uchun `uri` tag ida yuqori kardinallik (masalan buyurtma ID si yo'lda) bo'lmasligini tekshirish kerak.

## 16.9 Health indicator yozish va readiness va liveness farqi

Farq oddiy va qat'iy. Liveness: "bu process tirikmi, restart kerakmi". Readiness: "bu instance hozir trafik qabul qila oladimi". Shuning uchun tashqi bog'liqlik (PostgreSQL, to'lov gateway, Kafka) hech qachon liveness ga kirmasligi kerak. Agar kirsa, baza bir daqiqa sekinlashganda Kubernetes butun pod larni ketma-ket restart qiladi va vaziyat yomonlashadi.

Boot `probes.enabled: true` bilan `/actuator/health/liveness` va `/actuator/health/readiness` yo'llarini beradi. Bular `LivenessStateHealthIndicator` va `ReadinessStateHealthIndicator` ga asoslanadi, holatni esa `AvailabilityChangeEvent` orqali kod ichidan o'zgartirish mumkin. Masalan ombor qoldig'i cache i hali to'lmagan paytda instance ni readiness dan olib qo'yish mumkin.

```java
@Component("paymentGateway")   // bean nomi health kalitiga aylanadi
class PaymentGatewayHealthIndicator implements HealthIndicator {

    private final PaymentGateway gateway;

    @Override
    public Health health() {
        long start = System.nanoTime();
        try {
            gateway.ping();     // ichida read-timeout 1s bo'lishi shart
            long ms = (System.nanoTime() - start) / 1_000_000;
            return (ms < 500 ? Health.up() : Health.status("DEGRADED"))
                    .withDetail("latencyMs", ms)
                    .build();
        } catch (Exception e) {
            // xabar ichida URL va kalit bo'lmasin
            return Health.down().withDetail("reason", "gateway unreachable").build();
        }
    }
}
```

Health indicator ichida timeout bo'lmasa, health endpoint ning o'zi osilib qoladi va probe timeout ga tushadi. Qoida: har bir indicator 1 sekunddan tez javob berishi kerak, umumiy health javobi 2 sekunddan oshmasligi kerak. `management.endpoint.health.validate-group-membership` standart holda `true`, shuning uchun guruhda yo'q indicator nomini yozsangiz ishga tushishda xato chiqadi, bu foydali himoya.

## 16.10 Ishga tushish vaqti: lazy initialization, AOT va native image ta'siri

Tipik Spring Boot 3.x servis JVM da taxminan 2-5 sekundda ko'tariladi. Bu vaqtning katta qismi classpath skanerlash, annotatsiya metadata o'qish va bean yaratishga ketadi. `spring.main.lazy-initialization=true` bean larni birinchi murojaatga qoldiradi va startup ni taxminan 30-50 foizga qisqartiradi, lekin konfiguratsiya xatolari ishga tushishda emas, birinchi so'rovda chiqadi. Shu sababli bu flag lokal dev uchun, prod uchun emas.

AOT boshqa yondashuv: `spring-boot-maven-plugin` ning `process-aot` goal i build vaqtida bean definition larni Java kodiga aylantiradi va reflection ehtiyojini kamaytiradi. JVM da AOT ni `-Dspring.aot.enabled=true` bilan yoqish startup ni taxminan 20-30 foiz tezlashtiradi, lekin dinamik qarorlarni (profil bilan bean almashtirish, shartlarni runtime da hal qilish) build vaqtiga muzlatadi.

```bash
# 1) AOT bilan oddiy JVM jar: shartlar build vaqtida hisoblanadi
./mvnw -Pnative spring-boot:process-aot package
java -Dspring.aot.enabled=true -jar target/payment-service.jar

# 2) GraalVM native image: taxminan 50-120 ms startup, build 3-8 daqiqa
./mvnw -Pnative native:compile
./target/payment-service          # RSS taxminan 80-150 MB

# 3) CDS bilan o'rta yechim: kod o'zgarmaydi, startup taxminan 30% tez
java -XX:ArchiveClassesAtExit=app.jsa -Dspring.context.exit=onRefresh \
     -jar target/payment-service.jar
java -XX:SharedArchiveFile=app.jsa -jar target/payment-service.jar
```

Native image da reflection, dynamic proxy va resource yuklash build vaqtida ma'lum bo'lishi kerak. Spring buni ko'p holatda o'zi hal qiladi, qolganini `RuntimeHintsRegistrar` va `@ImportRuntimeHints` bilan qo'lda ko'rsatasiz. Arxitektorning qarori oddiy: agar servis kuniga bir marta deploy bo'lsa va uzoq ishlasa, JVM ni JIT bilan qoldirish tezroq ishlaydi (peak throughput JIT da yuqori). Agar scale-to-zero yoki tez avtoskaling kerak bo'lsa, native image yoki hech bo'lmasa CDS mantiqiy. Native ga o'tishdan oldin Testcontainers bilan native binary ustida integratsiya testlari o'tkazilishi shart, chunki klassik unit testlar native muammolarini ko'rmaydi.

## 16.11 Spring Boot 3 ga o'tish: Jakarta nomlari va konfiguratsiya o'zgarishlari

Eng katta o'zgarish kod darajasida: `javax.persistence`, `javax.servlet`, `javax.validation` paketlari `jakarta.*` ga ko'chdi. Bu Spring ning qarori emas, Java EE dan Jakarta EE ga o'tishning natijasi. Amalda bu import larni almashtirish va barcha uchinchi tomon kutubxonalarini jakarta ni qo'llab-quvvatlaydigan versiyaga ko'tarishni talab qiladi. Java baseline 17 ga ko'tarildi, Hibernate 6.x standart ORM bo'ldi.

Konfiguratsiya tomonida ko'p xossa nomi o'zgardi va eng xavfli jihati shu: eski nom jim e'tiborsiz qoldiriladi, xato chiqmaydi. Masalan `management.metrics.export.prometheus.*` endi `management.prometheus.metrics.export.*`, `spring.redis.*` endi `spring.data.redis.*`. Buni qo'lda topish mumkin emas, shuning uchun migratsiya davomida `spring-boot-properties-migrator` ni runtime dependency sifatida qo'shish kerak: u ishga tushishda eski nomlarni WARN bilan ro'yxatlaydi.

```properties
# faqat migratsiya davriga, keyin olib tashlanadi
# pom.xml: org.springframework.boot:spring-boot-properties-migrator (runtime)

# Boot 2.x -> 3.x nomlar misoli
# spring.redis.host                      -> spring.data.redis.host
# management.metrics.export.prometheus.enabled
#   -> management.prometheus.metrics.export.enabled
# spring.mvc.pathmatch.matching-strategy: endi PATH_PATTERN_PARSER standart
# trailing slash ("/orders/") avtomatik mos kelmaydi, aniq yozish kerak
```

Yana ikki nuqta e'tibor talab qiladi. Birinchisi: URL oxiridagi slash avtomatik moslashtirish olib tashlandi, ya'ni `/api/orders` va `/api/orders/` endi bir xil emas. Agar mijozlar eski formatda so'rov yuborsa, 404 oladi. Ikkinchisi: Hibernate 6 da identifikator generatsiyasi va ba'zi SQL generatsiya qoidalari o'zgardi, shu sababli migratsiyadan keyin yaratilgan SQL ni log orqali solishtirish kerak. Migratsiya tartibi amalda shunday bo'ladi: avval Boot 2.7 ga ko'tarilish, keyin dependency larni jakarta versiyalariga olib chiqish, so'ngra Boot 3.x, va har qadamda to'liq test to'plami. Shartnoma buzilmaganini tekshirish uchun [testlash qo'llanmasidagi](../testing/README.md) contract testing bo'limida tavsiflangan yondashuv qo'l keladi.

## 16.12 Amalda qo'llash

- [ ] Servisni `--debug` bilan bir marta ishga tushirib, `Negative matches` ro'yxatini ko'rib chiqing va kutilmagan tarzda o'chib qolgan auto-configuration borligini aniqlang.
- [ ] `management.endpoints.web.exposure.include` qiymatini tekshiring: `*` bo'lsa aniq ro'yxatga almashtiring va `management.server.port` ni 8081 ga ajratib, Ingress dan olib tashlang.
- [ ] `env` va `configprops` endpoint larida `show-values: never` o'rnatilganini tasdiqlang, `heapdump` va `threaddump` tashqariga ochiq emasligini tekshiring.
- [ ] Health guruhlarini qayta ko'rib chiqing: readiness ichida DB va tashqi gateway bo'lsin, liveness ichida faqat `livenessState` qolsin, har bir indicator ga 1 sekundlik timeout qo'shing.
- [ ] Barcha `@Value` guruhlarini bitta `@ConfigurationProperties` record ga birlashtirib, `@Validated` va `@Min`/`@NotBlank` cheklovlarini qo'shing, `spring-boot-configuration-processor` ni build ga ulang.
- [ ] `application.yaml` ichida `spring.profiles.active` yozilgan bo'lsa olib tashlang va uni faqat `SPRING_PROFILES_ACTIVE` orqali bering.
- [ ] Jamoaning umumiy kodini `acme-*-spring-boot-starter` va `acme-*-spring-boot-autoconfigure` juftligiga ajratib, `ApplicationContextRunner` bilan kamida uchta shart holatini (bean bor, bean yo'q, o'chirilgan) qamrab oling.
- [ ] Startup vaqtini o'lchang va 3 sekunddan oshsa avval CDS arxivi bilan sinab ko'ring, native image ga o'tish qarorini faqat scale-to-zero talabi bo'lganda qabul qiling.

---

[&larr; 15. Spring Core mexanikasi: IoC konteyner, bean lifecycle, AOP proxy](15-spring-core-mexanikasi-ioc-konteyner-bean.md) · [Mundarija](README.md) · [17. Spring MVC va WebFlux: so'rov yo'li, thread modeli, REST dizayni &rarr;](17-spring-mvc-va-webflux-sorov-yoli-thread.md)
