<!-- doc: code-review | chapter: 18 | part: IV. Spring kodini review qilish -->

[Kod review](../../README.md) / [Kod review](README.md)

# 18. Bean, kontekst va proxy mexanikasi review (Beans, Context and Proxies)

<details>
<summary>Bu bobdagi 10 bo'lim</summary>

- [18.1 Proxy ishlamaydigan to'rt holat](#181-proxy-ishlamaydigan-tort-holat)
- [18.2 Bean scope va holat](#182-bean-scope-va-holat)
- [18.3 Konfiguratsiya va bean e'lonlari](#183-konfiguratsiya-va-bean-elonlari)
- [18.4 Inyeksiya shakllari](#184-inyeksiya-shakllari)
- [18.5 Ishga tushish tartibi va `@PostConstruct`](#185-ishga-tushish-tartibi-va-postconstruct)
- [18.6 Kontekst sozlamalari diffda](#186-kontekst-sozlamalari-diffda)
- [18.7 Spring Boot avtokonfiguratsiyasi bilan kurash belgilari](#187-spring-boot-avtokonfiguratsiyasi-bilan-kurash-belgilari)
- [18.8 Proxy va tranzaksiyani test bilan tekshirish](#188-proxy-va-tranzaksiyani-test-bilan-tekshirish)
- [18.9 Review checklisti: Spring konteksti](#189-review-checklisti-spring-konteksti)
- [18.10 Amalda qo'llash](#1810-amalda-qollash)

</details>


Spring kodidagi eng jim xatolar annotatsiya ishlamaganda paydo bo'ladi: `@Transactional` qo'yilgan, lekin tranzaksiya yo'q; `@Cacheable` bor, lekin kesh ishlamaydi; `@Async` yozilgan, lekin kod sinxron ketadi. Kompilyator jim, test ko'pincha o'tadi, va xato prodda yuk ostida chiqadi. Sababi bitta: proxy mexanikasi. Shu sababli bu bob review ning Spring bo'limida birinchi turadi. Proxy ichki tuzilishi [Arxitektor miyyasi](../architect/README.md) da; bu yerda diffda ko'rinadigan buzilishlar.

## 18.1 Proxy ishlamaydigan to'rt holat

| Holat | Nega ishlamaydi | Diffdagi belgisi |
| --- | --- | --- |
| Shu klass ichidan chaqiruv | Proxy chetlab o'tiladi | `this.method()` yoki oddiy `method()` |
| `private` metod | Proxy uni o'ramaydi | `@Transactional private void` |
| `final` metod yoki klass | CGLIB meros qila olmaydi | `final` + annotatsiya |
| `static` metod | Instansga bog'liq emas | `@Cacheable static` |
| Konstruktor yoki `@PostConstruct` ichida | Proxy hali qurilmagan | `@PostConstruct` ichida `@Transactional` chaqiruvi |
| `new` bilan yaratilgan obyekt | Spring boshqarmaydi | `new OrderService(...)` |

```java
// Eng ko'p uchraydigan: ichki chaqiruv (12.3 da ko'rilgan, bu yerda yechimlar).
@Service
public class ImportService {

    public ImportReport importAll(List<Row> rows) {
        List<Failure> failures = new ArrayList<>();
        for (Row row : rows) {
            try {
                importOne(row);                    // proxy chetlab o'tiladi!
            } catch (Exception e) { failures.add(new Failure(row, e)); }
        }
        return new ImportReport(failures);
    }

    @Transactional(propagation = REQUIRES_NEW)     // ishlamaydi
    public void importOne(Row row) { ... }
}

// Yechim 1 (afzal): ikki bean ga ajratish - chegara ko'rinadi.
@Service
public class ImportService {                       // tranzaksiyasiz koordinator
    private final RowImporter importer;
    public ImportReport importAll(List<Row> rows) {
        ...
        importer.importOne(row);                   // proxy orqali, REQUIRES_NEW ishlaydi
    }
}
@Service
public class RowImporter {
    @Transactional(propagation = REQUIRES_NEW)
    public void importOne(Row row) { ... }
}

// Yechim 2: TransactionTemplate bilan aniq chegara - annotatsiya sehridan xoli.
@Service
public class ImportService {
    private final TransactionTemplate tx;          // propagation REQUIRES_NEW bilan sozlangan
    public ImportReport importAll(List<Row> rows) {
        for (Row row : rows) {
            tx.executeWithoutResult(status -> importOne(row));   // aniq, ko'rinadigan
        }
    }
}

// Yechim 3 (eng yomon, lekin uchraydi): o'z-o'ziga inyeksiya.
@Lazy @Autowired private ImportService self;       // self.importOne(row)
// Review izohi: ishlaydi, lekin niyatni yashiradi va sikl bog'liqlik
// yaratadi. Faqat refactoring imkoni bo'lmaganda vaqtinchalik.
```

## 18.2 Bean scope va holat

```java
// Naqsh: prototype bean singleton ga inyeksiya qilingan.
@Component
@Scope("prototype")
public class ReportBuilder { private List<Row> rows; }

@Service
public class ReportService {
    private final ReportBuilder builder;           // bir marta olinadi!
    // Prototype bo'lishiga qaramay, singleton ichida bitta instans qoladi
    // va holat so'rovlar orasida saqlanadi - 15.1 dagi xato.
}
// Yechim: ObjectProvider yoki fabrika.
private final ObjectProvider<ReportBuilder> builders;
ReportBuilder b = builders.getObject();            // har chaqiruvda yangi

// Naqsh: request scope bean background thread da ishlatilgan.
@Component @Scope(value = "request", proxyMode = TARGET_CLASS)
public class RequestContext { }
// @Async metodda bu bean ga murojaat - IllegalStateException:
// "No thread-bound request found". Review da @Async va request scope
// birga ishlatilishi har doim xato.
```

## 18.3 Konfiguratsiya va bean e'lonlari

```java
// Naqsh 1: @Configuration ichida bean metodini to'g'ridan-to'g'ri chaqirish.
@Configuration
class AppConfig {
    @Bean DataSource dataSource() { return new HikariDataSource(hikariConfig()); }
    @Bean HikariConfig hikariConfig() { return new HikariConfig(); }
    // dataSource() ichidan hikariConfig() chaqirilganda, @Configuration
    // proxy si uni ushlaydi va singleton qaytaradi (proxyBeanMethods=true).
    // Lekin @Configuration(proxyBeanMethods = false) bo'lsa - har chaqiruvda
    // yangi obyekt. Ikki xil xulq, diffda bir xil ko'rinadi.
}
// Review javobi: bog'liqlikni parametr orqali olish - xulq aniq bo'ladi.
@Bean DataSource dataSource(HikariConfig config) { return new HikariDataSource(config); }

// Naqsh 2: @ConditionalOnProperty bilan yashirin xulq.
@Bean
@ConditionalOnProperty(name = "feature.newPricing", havingValue = "true")
PricingStrategy newPricing() { ... }
// Review savoli: property yo'q bo'lsa nima bo'ladi? Agar boshqa
// PricingStrategy bean i bo'lmasa, ilova ishga tushmaydi yoki
// @ConditionalOnMissingBean bilan jim boshqa implementatsiya olinadi.
// Ikki holat ham diffda ko'rinmaydi - test bilan tekshirilishi kerak.

// Naqsh 3: bir xil turdagi ikki bean - qaysi biri olinadi noaniq.
@Bean RestClient paymentClient() { ... }
@Bean RestClient fraudClient() { ... }
// Inyeksiyada: RestClient client - NoUniqueBeanDefinitionException yoki
// maydon nomi bo'yicha tasodifiy mos kelish. @Qualifier majburiy.
```

## 18.4 Inyeksiya shakllari

```java
// Review da talab qilinadigan shakl: konstruktor inyeksiyasi.
@Service
public class OrderService {
    private final Orders orders;                   // final: o'zgarmaydi
    private final Clock clock;

    OrderService(Orders orders, Clock clock) {     // bitta konstruktor - @Autowired kerak emas
        this.orders = orders;
        this.clock = clock;
    }
}
// Foydasi: (1) testda `new OrderService(fakeOrders, fixedClock)` - kontekst
// kerak emas; (2) majburiy bog'liqliklar ko'rinadi; (3) sikl bog'liqlik
// ishga tushishda aniqlanadi, ish vaqtida emas.

// Taqiqlanadigan shakl: maydon inyeksiyasi.
@Autowired private Orders orders;                  // testda refleksiya kerak
// ArchUnit bilan taqiqlash (5.10 da ko'rsatilgan).

// Ixtiyoriy bog'liqlik: Optional yoki ObjectProvider, null emas.
OrderService(Orders orders, Optional<AuditSink> audit) { ... }
```

## 18.5 Ishga tushish tartibi va `@PostConstruct`

```java
// Naqsh: ishga tushishda tashqi tizimga murojaat.
@Component
public class RateLoader {
    @PostConstruct
    void load() {
        rates.putAll(rateClient.fetchAll());       // tashqi servis yiqilsa - ilova
    }                                              // ishga tushmaydi
}
// Review savollari: (1) bu ma'lumot ishga tushish uchun majburiymi?
// (2) tashqi servis javob bermasa, pod CrashLoopBackOff ga tushadimi?
// (3) timeout bormi? (4) readiness probe bilan munosabati qanday?

// Yaxshiroq: ishga tushish bloklanmaydi, ma'lumot keyin yuklanadi,
// holat health check da ko'rinadi.
@Component
public class RateLoader implements HealthIndicator {
    private final AtomicReference<Rates> rates = new AtomicReference<>();

    @Scheduled(fixedDelay = 60_000, initialDelay = 0)
    void refresh() {
        try { rates.set(rateClient.fetchAll()); }
        catch (Exception e) { log.warn("kurslar yangilanmadi", e); }
    }
    @Override public Health health() {
        Rates r = rates.get();
        return r == null ? Health.down().withDetail("rates", "yuklanmagan").build()
                         : Health.up().withDetail("asOf", r.asOf()).build();
    }
}
```

## 18.6 Kontekst sozlamalari diffda

| Belgi | Review savoli |
| --- | --- |
| `@ComponentScan` paketi kengaytirilgan | Qanday beanlar qo'shimcha topildi, ishga tushish vaqti o'zgardimi |
| `@EnableAsync`, `@EnableScheduling` qo'shilgan | Pool qaysi, xato ishlovchi bormi |
| `@EnableAspectJAutoProxy(exposeProxy = true)` | Nega kerak - bu self-invocation ni yashiradi |
| `spring.main.allow-bean-definition-overriding=true` | Qaysi bean almashtirilyapti va nega |
| `@Primary` qo'shilgan | Boshqa inyeksiya joylari ta'sirlandimi |
| `@Order` o'zgargan | Filter yoki aspekt tartibi muhimmi |
| `BeanPostProcessor` qo'shilgan | Barcha beanlarga ta'sir qiladi - juda kuchli mexanizm |
| `@Lazy` qo'shilgan | Nega: ishga tushish tezligi yoki sikl bog'liqlikni yashirish |

Oxirgi uchtasi alohida diqqat talab qiladi: ular global ta'sirga ega va diffda kichik ko'rinadi. `@Lazy` ning sikl bog'liqlikni yashirish uchun qo'yilishi tipik holat - bu muammoni yechmaydi, faqat ish vaqtiga ko'chiradi.

## 18.7 Spring Boot avtokonfiguratsiyasi bilan kurash belgilari

```java
// Belgi: avtokonfiguratsiyani o'chirish.
@SpringBootApplication(exclude = { DataSourceAutoConfiguration.class })
// Review savoli: nega? Odatda bu konfiguratsiya muammosini yashirish
// uchun qilinadi va keyinroq boshqa joyda chiqadi.

// Belgi: bean ni qo'lda qayta e'lon qilish.
@Bean ObjectMapper objectMapper() { return new ObjectMapper(); }
// Review izohi: Spring Boot ning ObjectMapper i Jackson modullarini,
// JavaTimeModule ni va `spring.jackson.*` sozlamalarini hisobga oladi.
// Qo'lda yaratilgan ObjectMapper ularni yo'qotadi: natijada sanalar
// massiv sifatida serializatsiya bo'ladi va null lar javobga chiqadi.
// To'g'risi: Jackson2ObjectMapperBuilder yoki Jackson2ObjectMapperBuilderCustomizer.
@Bean Jackson2ObjectMapperBuilderCustomizer customizer() {
    return b -> b.serializationInclusion(JsonInclude.Include.NON_NULL)
                 .featuresToDisable(SerializationFeature.WRITE_DATES_AS_TIMESTAMPS);
}
```

## 18.8 Proxy va tranzaksiyani test bilan tekshirish

Review izohida "proxy ishlamaydi" degan gapni dalil bilan quvvatlash mumkin: test yoziladi va u mavjud kodda yiqiladi.

```java
// Tranzaksiya chegarasi haqiqatda qanday ishlayotganini ko'rsatadigan test.
@SpringBootTest
class TransactionBoundaryTest {

    @Autowired ImportService service;

    @Test
    void failingRowShouldNotRollbackOthers() {
        List<Row> rows = List.of(validRow(), invalidRow(), validRow());

        service.importAll(rows);

        // Niyat: ikki qator saqlanishi kerak (REQUIRES_NEW).
        // Mavjud kodda: 0 qator - hammasi qaytadi, chunki proxy chetlab
        // o'tilgan va bitta tranzaksiya rollback bo'ladi.
        assertThat(repository.count()).isEqualTo(2);
    }

    @Test
    void transactionIsActuallyActive() {
        // Tranzaksiya haqiqatda bor-yo'qligini tekshirishning to'g'ridan-to'g'ri yo'li.
        service.doWork(() ->
            assertThat(TransactionSynchronizationManager.isActualTransactionActive())
                .as("tranzaksiya aktiv bo'lishi kerak")
                .isTrue());
    }
}
```

```java
// Arxitektura testi bilan takrorlanishni oldini olish.
@ArchTest
static final ArchRule no_transactional_on_private_or_final =
    methodsThat(are(annotatedWith(Transactional.class)))
        .should().notBePrivate()
        .andShould().notBeFinal()
        .because("proxy private va final metodlarni o'ramaydi");

@ArchTest
static final ArchRule no_self_injection =
    noFields().should().haveRawType(DescribedPredicate.describe(
            "o'z klassi turida", f -> f.getRawType().equals(f.getOwner())))
        .because("o'z-o'ziga inyeksiya niyatni yashiradi");
```

## 18.9 Review checklisti: Spring konteksti

| Savol | Nega |
| --- | --- |
| Annotatsiyali metod shu klass ichidan chaqirilmaydimi | Proxy chetlab o'tiladi |
| Annotatsiyali metod `public` va `final` emasmi | Proxy o'rashi uchun |
| Konstruktor inyeksiyasi ishlatilganmi | Testlanadigan va immutable |
| Bir xil turdagi beanlar uchun `@Qualifier` bormi | Noaniqlik |
| `@PostConstruct` tashqi tizimga chiqmaydimi | Ishga tushish mo'rtligi |
| Prototype/request scope singleton ga inyeksiya qilinmaganmi | Holat oqishi |
| Avtokonfiguratsiya o'chirilgan bo'lsa, sabab yozilganmi | Yashirin muammo |
| `ObjectMapper`, `RestClient` qo'lda yaratilgan bo'lsa, sozlamalar saqlanganmi | Konfiguratsiya yo'qolishi |
| `@Primary`, `@Order`, `BeanPostProcessor` ta'siri baholanganmi | Global o'zgarish |
| Yangi `@Enable*` annotatsiyasi uchun pool va xato ishlovchi bormi | Jim nosozlik |

## 18.10 Amalda qo'llash

- [ ] `@Transactional`, `@Cacheable`, `@Async`, `@Retryable` annotatsiyali metodlarning shu klass ichidan chaqirilgan joylarini toping - hammasi ishlamaydi.
- [ ] `private` yoki `final` metodlarga qo'yilgan proxy annotatsiyalarini aniqlab, ArchUnit qoidasi bilan taqiqlang.
- [ ] Maydon inyeksiyasini (`@Autowired` maydonda) butunlay konstruktor inyeksiyasiga o'tkazing.
- [ ] `@PostConstruct` ichida tashqi tizimga murojaat qiladigan joylarni toping va ularni `@Scheduled` + `HealthIndicator` ga o'tkazing.
- [ ] Qo'lda yaratilgan `ObjectMapper` larni `Jackson2ObjectMapperBuilder` ga o'tkazib, sana formatlarini tekshiring.
- [ ] `spring.main.allow-bean-definition-overriding` yoqilgan bo'lsa, qaysi beanlar almashtirilayotganini aniqlang.
- [ ] Prototype va request scope bean larning singleton ga inyeksiya qilinganini tekshiring.
- [ ] Tranzaksiya chegarasi uchun `isActualTransactionActive()` tekshiruvi bilan kamida bitta test yozing.

---

[&larr; 17. Zamonaviy Java review: record, sealed, pattern matching, virtual thread](17-zamonaviy-java-review-record-sealed-pattern.md) · [Mundarija](README.md) · [19. Tranzaksiya chegarasi review &rarr;](19-tranzaksiya-chegarasi-review.md)
