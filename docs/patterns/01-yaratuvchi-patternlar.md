<!-- doc: patterns | chapter: 1 | part:  -->

[Java Spring arxitektori bilishi kerak bo'lgan barcha dizayn patternlar](../../README.md) / [Dizayn patternlar](README.md)

# 1. Yaratuvchi patternlar (Creational Patterns)

<details>
<summary>Bu bo'limdagi 18 bo'lim</summary>

- [1.1 Yagona nusxa (Singleton)](#11-yagona-nusxa-singleton)
- [1.2 Kalit bo'yicha yagona nusxalar (Multiton)](#12-kalit-boyicha-yagona-nusxalar-multiton)
- [1.3 Yagona holat (Monostate)](#13-yagona-holat-monostate)
- [1.4 Kechiktirilgan initsializatsiya (Lazy Initialization)](#14-kechiktirilgan-initsializatsiya-lazy-initialization)
- [1.5 Talab bo'yicha initsializatsiya holder idiomasi (Initialization-on-Demand Holder Idiom)](#15-talab-boyicha-initsializatsiya-holder-idiomasi-initialization-on-demand-holder-idiom)
- [1.6 Statik fabrika metodi / Oddiy fabrika (Static Factory Method / Simple Factory)](#16-statik-fabrika-metodi--oddiy-fabrika-static-factory-method--simple-factory)
- [1.7 Fabrika metodi (Factory Method)](#17-fabrika-metodi-factory-method)
- [1.8 Abstrakt fabrika (Abstract Factory)](#18-abstrakt-fabrika-abstract-factory)
- [1.9 Fabrika to'plami (Factory Kit)](#19-fabrika-toplami-factory-kit)
- [1.10 Quruvchi (Builder, Step Builder, Lombok @Builder)](#110-quruvchi-builder-step-builder-lombok-builder)
- [1.11 Prototip (Prototype)](#111-prototip-prototype)
- [1.12 Obyektlar hovuzi (Object Pool)](#112-obyektlar-hovuzi-object-pool)
- [1.13 Bog'liqliklarni kiritish (Dependency Injection)](#113-bogliqliklarni-kiritish-dependency-injection)
- [1.14 Kompozitsiya ildizi (Composition Root)](#114-kompozitsiya-ildizi-composition-root)
- [1.15 Provider / Supplier orqali kiritish (Provider / Supplier Injection)](#115-provider--supplier-orqali-kiritish-provider--supplier-injection)
- [1.16 Servis topuvchi (Service Locator)](#116-servis-topuvchi-service-locator)
- [1.17 Reyestr (Registry)](#117-reyestr-registry)
- [1.18 Amalda qo'llash](#118-amalda-qollash)

</details>



Yaratuvchi patternlar obyektlarni "kim, qachon va qanday" yaratishini kodning qolgan qismidan ajratib beradi: ular `new` operatorini bevosita chaqirishni inkapsulyatsiya qiladi, obyekt grafini qurishni markazlashtiradi va yaratish siyosatini (yagona nusxa, hovuz, kechiktirilgan yaratish, kalit bo'yicha tanlash) alohida boshqarishga imkon beradi. Spring'ning o'zagi - IoC konteyner - aslida shu patternlarning sanoat darajasidagi kombinatsiyasi: `BeanFactory` abstrakt fabrika, `@Bean` metodi fabrika metodi, singleton scope - Singleton, `ObjectProvider` - Provider injection, `BeanDefinitionRegistry` - Registry. Arxitektor bu patternlarni chuqur bilmasa, konteyner nima qilayotganini tushunmaydi, bean yaratish tartibi, scope va lifecycle bilan bog'liq nozik xatolarni (circular dependency, prototype-in-singleton, lazy proxy) tashxislay olmaydi va o'z kutubxonalari uchun to'g'ri yaratish API'sini dizayn qila olmaydi.

## 1.1 Yagona nusxa (Singleton)

**Tavsif:** Muammo: ba'zi obyektlar (konfiguratsiya, ulanishlar fabrikasi, kesh, logger) tizimda bitta bo'lishi va hamma joydan bir xil nusxaga murojaat qilinishi kerak. Singleton sinf o'z yagona nusxasini o'zi yaratadi va saqlaydi, konstruktorni yopadi (`private`) va statik kirish nuqtasi (`getInstance()`) orqali uni beradi. Klassik GoF varianti - statik maydon + lazy yaratish; thread-safe variantlar: eager static init, holder idiomasi (1.5), enum singleton (qarang: [24-bo'lim](24-zamonaviy-java-va-funksional-patternlar.md), Enum Singleton) va double-checked locking (qarang: [4-bo'lim](04-concurrency-patternlari.md), Double-Checked Locking). Zamonaviy amaliyotda "sinf o'zini singleton qiladi" yondashuvi o'rniga "konteyner nusxa sonini boshqaradi" yondashuvi afzal ko'riladi.

**Spring'da qayerda uchraydi:** Spring'da `singleton` - bean'larning default scope'i (`@Scope(ConfigurableBeanFactory.SCOPE_SINGLETON)`); nusxa `DefaultSingletonBeanRegistry` ichidagi `singletonObjects` xaritasida saqlanadi. Muhim farq: Spring singleton - "har bir konteyner uchun bitta", JVM yoki ClassLoader uchun bitta emas; shu sababli testlarda bir nechta `ApplicationContext` bo'lsa, bir nechta nusxa bo'ladi. Boshqa misollar: `java.lang.Runtime.getRuntime()`, SLF4J `LoggerFactory.getILoggerFactory()`, `org.springframework.util.function.SingletonSupplier` (bir marta hisoblanadigan Supplier), Spring Boot'da `SpringApplication.run` bitta `ApplicationContext` yaratadi.

**Qo'llanish keyslari:**
- Stateless service/repository bean'lar - Spring default singleton scope bilan boshqariladi, hech qanday qo'lda kod talab qilmaydi.
- Qimmat resurslarni ushlab turuvchi obyektlar: `DataSource` (connection pool), `EntityManagerFactory`, `KafkaProducer`, `ObjectMapper` - bitta nusxa, hamma joyda qayta ishlatiladi.
- Ilova darajasidagi kesh yoki metrika registri (`MeterRegistry`) - yagona nuqtada agregatsiya.
- Spring'siz kutubxona/SDK ichida global konfiguratsiya yoki `ServiceLoader` orqali topilgan yagona provayder.
- Tashqi tizim bilan bitta ulanish sessiyasi (masalan, bitta WebSocket klient) bo'lishi shart bo'lgan integratsiyalar.

**Ehtiyot bo'ling:** Klassik `getInstance()` singleton - yashirin global holat: test qilish qiyin, mock qilib bo'lmaydi, kodga bog'liqlikni yashiradi (qarang: [25-bo'lim](25-anti-patternlar.md), Singleton abuse / Static Cling). Spring singleton bean'larida mutable maydon saqlash - ko'p thread'li muhitda race condition manbai (qarang: [25-bo'lim](25-anti-patternlar.md), Mutable state in singleton beans). Singleton bean ichiga prototype bean to'g'ridan-to'g'ri inject qilinsa, u ham amalda singleton bo'lib qoladi - bu holda `ObjectProvider` (1.15) yoki scoped proxy ishlating.

```java
// Spring uslubi: sinf o'zini singleton qilmaydi - konteyner boshqaradi
@Service                       // default scope = singleton
public class PricingService {
    private final RateProvider rates;   // final, immutable holat
    public PricingService(RateProvider rates) { this.rates = rates; }
}

// Spring'siz, thread-safe eager singleton (JVM class init kafolati)
public final class AppClock {
    private static final AppClock INSTANCE = new AppClock();
    private AppClock() {}
    public static AppClock getInstance() { return INSTANCE; }
}
```

## 1.2 Kalit bo'yicha yagona nusxalar (Multiton)

**Tavsif:** Singleton'ning umumlashtirilgan ko'rinishi: har bir kalit (nom, tenant, region, valyuta) uchun faqat bitta nusxa mavjud bo'ladi va ular `Map<Key, Instance>` ichida saqlanadi. `getInstance(key)` kalit bo'yicha nusxani qaytaradi, yo'q bo'lsa yaratadi va xaritaga qo'yadi. Thread-safe amalga oshirish uchun `ConcurrentHashMap.computeIfAbsent` ishlatiladi. Pattern "bir xil kalit - bir xil nusxa" kafolatini beradi va qimmat obyektlarni kalit bo'yicha qayta ishlatish imkonini yaratadi.

**Spring'da qayerda uchraydi:** `LoggerFactory.getLogger(name)` - nom bo'yicha bitta `Logger`; `ConcurrentMapCacheManager.getCache(name)` - nom bo'yicha bitta `Cache` ni lazy yaratadi; `Charset.forName`, `Currency.getInstance`, `ZoneId.of` - JDK darajasidagi multiton'lar; Micrometer'da `MeterRegistry.counter(name, tags)` nom+teg bo'yicha bitta `Meter` qaytaradi. Spring ilovalarida ko'pincha multi-tenant arxitekturada `Map<TenantId, DataSource>` yoki `Map<Region, RestClient>` ko'rinishida uchraydi (marshrutlash tafsilotlari: qarang [10-bo'lim](10-malumotlarni-boshqarish-va-taqsimlash.md), Multi-tenancy va Replication & Read Replica routing).

**Qo'llanish keyslari:**
- Multi-tenant tizimda har bir tenant uchun bitta `DataSource` yoki `EntityManagerFactory` saqlash.
- Tashqi API'ning har bir regioni/mamlakati uchun alohida konfiguratsiyalangan `RestClient` nusxasi.
- Nom bo'yicha kesh, rate-limiter yoki circuit-breaker nusxalari (`CircuitBreakerRegistry.circuitBreaker(name)` xuddi shu g'oya).
- Har bir Kafka topic yoki queue uchun bitta producer/template nusxasini saqlash.
- Logger, metrika, feature-flag kabi "nomlangan" infratuzilma obyektlari.

**Ehtiyot bo'ling:** Kalitlar to'plami cheklanmagan bo'lsa (masalan, foydalanuvchi ID), xarita cheksiz o'sadi - bu memory leak; bu holda eviction (Caffeine) yoki qat'iy TTL kerak. Nusxalar hech qachon yopilmasa, resurs (ulanish, thread) oqishi yuz beradi - yopish (close) siyosatini aniq belgilang. Spring'da buni static xarita o'rniga `@Bean` + `Map` yoki `ObjectProvider` bilan konteyner nazoratida qilish afzal.

```java
// Multiton: kalit bo'yicha bitta nusxa, konteyner nazoratida
@Component
public class TenantDataSources {
    private final Map<TenantId, DataSource> byTenant = new ConcurrentHashMap<>();
    private final DataSourceFactory factory;

    public TenantDataSources(DataSourceFactory factory) { this.factory = factory; }

    public DataSource forTenant(TenantId id) {
        // computeIfAbsent: bir xil kalit uchun bir xil nusxa, thread-safe
        return byTenant.computeIfAbsent(id, factory::create);
    }
}

// JDK darajasidagi multiton'lar: kalit -> yagona nusxa
Logger log = LoggerFactory.getLogger("audit");   // nom bo'yicha bitta Logger
ZoneId zone = ZoneId.of("Asia/Tashkent");        // ID bo'yicha bitta ZoneId
```

## 1.3 Yagona holat (Monostate)

**Tavsif:** Monostate (Borg) - Singleton'ning "teskari" varianti: sinfdan istalgancha nusxa yaratish mumkin, lekin barcha maydonlar `static`, shuning uchun hamma nusxalar bir xil holatni bo'lishadi. Chaqiruvchi kod `new` bilan odatdagidek ishlaydi, polimorfizm va meros saqlanadi, lekin semantik jihatdan tizimda "bitta holat" mavjud bo'ladi. U yagona nusxa kafolati o'rniga yagona holat kafolatini beradi va shu bilan chaqiruvchi kodni Singleton API'siga bog'lamaydi.

**Spring'da qayerda uchraydi:** Spring'da sof Monostate bean'lar deyarli ishlatilmaydi - konteyner singleton scope bilan xuddi shu natijani toza usulda beradi. Unga eng yaqin narsa - static kesh saqlovchi util sinflar (`ReflectionUtils` dagi metodlar keshi, `SpringFactoriesLoader` dagi yuklangan fabrikalar keshi) va static holder sinflar (`LocaleContextHolder`, `RequestContextHolder`, `SecurityContextHolder`), lekin ular thread'ga bog'langan holatni saqlaydi (qarang: [4-bo'lim](04-concurrency-patternlari.md), Thread-Specific Storage). Legacy kodlarda static konfiguratsiya maydonlariga ega "Config" sinflar - tipik Monostate.

**Qo'llanish keyslari:**
- Legacy kodda Singleton'ni refaktoring qilishda - chaqiruvchilar `new` ishlatishda davom etadi, lekin holat bitta bo'ladi.
- Spring'siz kichik kutubxonalarda global sozlamalar (masalan, default timeout) uchun.
- Static kesh saqlovchi util sinflar - sinf metadata'si, reflection natijalari.
- Test fixture'larida ilova bo'ylab umumiy "soat" yoki feature-flag holati (yaxshiroq alternativ: `Clock` bean, qarang: [23-bo'lim](23-testing-patternlari.md), Clock injection).

**Ehtiyot bo'ling:** Static holat - Spring test context caching bilan birga flaky testlarning klassik manbai: bir test ikkinchisining holatini ko'radi. Monostate meros bilan ishlatilsa, subclass'lar ham static holatni bo'lishadi va bu kutilmagan bog'liqlik yaratadi. Spring ilovasida asosli sabab bo'lmasa, singleton bean + DI ishlating.

```java
// Monostate: nusxa ko'p, holat bitta (static). Legacy kodda uchraydi.
public class FeatureFlags {
    private static final Map<String, Boolean> FLAGS = new ConcurrentHashMap<>();
    public boolean isOn(String key) { return FLAGS.getOrDefault(key, false); }
    public void set(String key, boolean on) { FLAGS.put(key, on); }
}

// Spring'da afzal variant: static holat yo'q, konteyner nusxa sonini boshqaradi
@Service
public class FeatureFlagService {
    private final Map<String, Boolean> flags = new ConcurrentHashMap<>();
    public boolean isOn(String key) { return flags.getOrDefault(key, false); }
}
```

## 1.4 Kechiktirilgan initsializatsiya (Lazy Initialization)

**Tavsif:** Qimmat obyekt yoki hisob-kitob darhol emas, birinchi haqiqiy talab bo'lganda yaratiladi; natija keshlanadi va keyingi murojaatlarda qayta ishlatiladi. Pattern startup vaqtini qisqartiradi, kerak bo'lmagan resurslarni band qilmaydi va ba'zan circular bog'liqliklarni uzish uchun ishlatiladi. Ko'p thread'li muhitda "faqat bir marta yaratilsin" kafolati talab qilinadi: `synchronized`, holder idiomasi (1.5), `AtomicReference` yoki tayyor `Supplier` memoizatsiyasi orqali.

**Spring'da qayerda uchraydi:** `@Lazy` annotatsiyasi bean yaratilishini birinchi murojaatgacha kechiktiradi, inject nuqtasida esa lazy-resolution proxy yaratadi (tafsilot: qarang [5-bo'lim](05-spring-core-ichidagi-patternlar-xaritasi.md), @Lazy). Spring Boot'da `spring.main.lazy-initialization=true` - butun konteyner uchun lazy rejim (`LazyInitializationBeanFactoryPostProcessor`, istisnolar `LazyInitializationExcludeFilter` orqali). Boshqa vositalar: `ObjectProvider` (1.15), `org.springframework.util.function.SingletonSupplier`, Guava `Suppliers.memoize`, Vavr `Lazy`. JPA'dagi lazy loading - alohida mavzu (qarang: [9-bo'lim](09-malumotlarga-kirish-va-orm-patternlari.md), Lazy Load); Supplier asosidagi lazy evaluation - qarang: [24-bo'lim](24-zamonaviy-java-va-funksional-patternlar.md).

**Qo'llanish keyslari:**
- Dev muhitida startup'ni tezlashtirish - `spring.main.lazy-initialization=true` faqat `dev` profilda.
- Kamdan-kam ishlatiladigan va qimmat tashqi klientlar (masalan, PDF renderer, ML model) - birinchi so'rovda yuklash.
- Sozlamaga bog'liq ravishda umuman kerak bo'lmasligi mumkin bo'lgan integratsiyalar (feature flag yoqilganda).
- Singleton ichida qimmat hisoblangan immutable qiymatni memoizatsiya qilish (`SingletonSupplier.of(this::compute)`).
- Circular bog'liqlikni vaqtincha uzish - `@Lazy` konstruktor parametrida (lekin bu dizayn muammosini yashiradi).

**Ehtiyot bo'ling:** Lazy rejim konfiguratsiya xatolarini startup'dan birinchi so'rov vaqtiga ko'chiradi - production'da "fail fast" prinsipiga zid va readiness probe'ni aldab qo'yishi mumkin. Birinchi so'rov latency'si oshadi (p99 ga ta'sir). `@Lazy` proxy faqat interfeys yoki CGLIB bilan proxy qilinadigan tiplar uchun ishlaydi; `final` sinflar va primitivlar uchun ishlamaydi.

```java
// Bean darajasida: yaratilish birinchi murojaatgacha kechiktiriladi
@Bean
@Lazy
PdfRenderer pdfRenderer() {           // og'ir obyekt, kamdan-kam kerak
    return new PdfRenderer(fontCache());
}

// Qiymat darajasida: bir marta hisoblanadi va keshlanadi
@Service
public class TaxTableService {
    private final Supplier<TaxTable> table =
            SingletonSupplier.of(this::loadFromDb);   // Spring'ning memoizatsiyasi

    public TaxTable table() { return table.get(); }

    private TaxTable loadFromDb() { /* qimmat yuklash */ return new TaxTable(); }
}
```

## 1.5 Talab bo'yicha initsializatsiya holder idiomasi (Initialization-on-Demand Holder Idiom)

**Tavsif:** Lazy va thread-safe singleton'ni hech qanday lock'siz amalga oshiruvchi Java idiomasi. Nusxa ichki `static` sinf (holder) ning `static final` maydonida saqlanadi; JVM spetsifikatsiyasi (JLS 12.4) ichki sinf faqat birinchi murojaatda, atomik va thread-safe tarzda initsializatsiya qilinishini kafolatlaydi. Natijada `getInstance()` sinxronizatsiyasiz ishlaydi, lekin nusxa faqat kerak bo'lganda yaratiladi. Double-checked locking'ning sodda va xatosiz alternativi.

**Spring'da qayerda uchraydi:** Spring boshqaradigan bean'larda bu idioma kerak emas - konteyner `@Lazy` va singleton scope orqali xuddi shu kafolatni beradi. Idioma Spring'siz yashaydigan kodda uchraydi: static util sinflar (masalan, `ObjectMapper` yoki kompilyatsiya qilingan `Pattern` ni static holder orqali bir marta yaratish), JPA `AttributeConverter` yoki Hibernate `UserType` kabi konteyner tashqarisida instansiyalanadigan sinflar, kutubxona SDK'lari. Effective Java (Item 83) static maydonlar uchun lazy initsializatsiyada aynan shu idiomani tavsiya qiladi.

**Qo'llanish keyslari:**
- Spring konteyner tashqarisida ishlaydigan kutubxona ichida qimmat singleton (masalan, kompilyatsiya qilingan regex yoki schema validator).
- Static kontekstdan (masalan, `jakarta.persistence.AttributeConverter`) `ObjectMapper` kabi qimmat resursga kirish.
- Startup vaqtida yuklanmasligi kerak bo'lgan, lekin thread-safe bo'lishi shart bo'lgan global resurs.
- Double-checked locking ishlatilgan legacy kodni soddalashtirish.

**Ehtiyot bo'ling:** Idioma faqat static (sinf darajasidagi) lazy qiymatlar uchun ishlaydi - nusxa maydonlari uchun `Supplier` memoizatsiyasi yoki `AtomicReference` kerak. Holder ichidagi konstruktor exception tashlasa, sinf `NoClassDefFoundError` holatiga tushadi va keyingi urinishlar ham xato beradi. Spring bean'lari uchun bu idiomani ishlatish - konteynerni chetlab o'tish va DI afzalliklarini yo'qotish demak.

```java
public final class SchemaValidator {
    private SchemaValidator() { /* qimmat yuklash */ }

    private static class Holder {              // birinchi murojaatda yuklanadi
        static final SchemaValidator INSTANCE = new SchemaValidator();
    }

    public static SchemaValidator get() {      // lock yo'q, thread-safe
        return Holder.INSTANCE;
    }
}
```

## 1.6 Statik fabrika metodi / Oddiy fabrika (Static Factory Method / Simple Factory)

**Tavsif:** Konstruktor o'rniga obyektni qaytaruvchi nomlangan `static` metod (Effective Java, Item 1): `of`, `from`, `valueOf`, `getInstance`, `create`. Afzalliklari: ma'noli nom, har chaqiruvda yangi obyekt yaratish shart emas (kesh, singleton), qaytariladigan tip - subtip yoki interfeys bo'lishi mumkin, generic tip inferensiyasi. "Oddiy fabrika" (Simple Factory) - GoF'ga kirmaydigan, lekin eng ko'p ishlatiladigan variant: bitta sinf/metod parametrga (enum, string, tip) qarab turli implementatsiyalardan birini qaytaradi; odatda `switch` yoki `Map` orqali.

**Spring'da qayerda uchraydi:** JDK: `List.of`, `Optional.of`, `Duration.ofSeconds`, `Executors.newFixedThreadPool`. Spring: `ResponseEntity.ok()`, `ResponseEntity.status(HttpStatus)`, `MediaType.parseMediaType`, `PageRequest.of`, `Sort.by`, `Example.of`, `RestClient.create()`, `WebClient.create()`, `UriComponentsBuilder.fromUriString`, `ServerResponse.ok()`, `RouterFunctions.route()`, Reactor `Mono.just` / `Flux.fromIterable`. Simple Factory Spring loyihalarida odatda `@Component` fabrika sinfi + `Map<Type, Impl>` ko'rinishida yoki `@Bean` metodi ichidagi `switch` (profil/property bo'yicha implementatsiya tanlash) ko'rinishida uchraydi. Java darajasidagi dizayn tafsilotlari: qarang [24-bo'lim](24-zamonaviy-java-va-funksional-patternlar.md) (Static Factory Method (Effective Java)).

**Qo'llanish keyslari:**
- Value Object va DTO'lar uchun validatsiya qiluvchi nomlangan konstruktorlar: `Money.of(amount, currency)`, `Email.from(string)`.
- `@Bean` metodida property qiymatiga qarab `StorageClient` ning S3/GCS/local implementatsiyasini tanlash.
- Immutable obyektlarni keshlash: `Boolean.valueOf`, interning qilinadigan kichik qiymatlar.
- API'da konkret sinfni yashirib, interfeys qaytarish - keyinchalik implementatsiyani o'zgartirish erkinligi.
- Tashqi event turiga (`enum EventType`) qarab tegishli `Handler` yaratish - kichik tizimlarda `switch` bilan.

**Ehtiyot bo'ling:** Static metodlar polimorfik emas - ularni mock qilish va subclass'da o'zgartirish qiyin, shuning uchun Spring bean'lari orasidagi bog'liqlik uchun DI afzal. Simple Factory'dagi `switch` har yangi tur qo'shilganda o'zgaradi (Open/Closed buziladi) - turlar ko'paysa `Map<Key, Supplier>` (1.9) yoki Factory Method / Strategy registry'ga o'ting. `public` konstruktorsiz sinflar JPA/Jackson kabi reflection asosidagi kutubxonalar bilan muammo tug'dirishi mumkin (`@JsonCreator` kerak).

```java
// Statik fabrika: konstruktorga nisbatan nomi bor, keshlashi va tur tanlashi mumkin
public record Money(BigDecimal amount, Currency currency) {
    public static Money of(String amount, String code) {
        return new Money(new BigDecimal(amount), Currency.getInstance(code));
    }
    public static Money zero(String code) {        // nom maqsadni ochib beradi
        return new Money(BigDecimal.ZERO, Currency.getInstance(code));
    }
}

// Spring va JDK dagi tanish misollar
ResponseEntity<Order> ok = ResponseEntity.ok(order);
Pageable page = PageRequest.of(0, 20, Sort.by("createdAt").descending());
Duration timeout = Duration.ofSeconds(3);
```

## 1.7 Fabrika metodi (Factory Method)

**Tavsif:** GoF: obyekt yaratish uchun interfeys (abstrakt yoki qayta yozsa bo'ladigan metod) e'lon qilinadi, lekin qaysi konkret sinf yaratilishini subclass yoki implementatsiya hal qiladi. Framework kodi "mahsulot" bilan abstrakt tip orqali ishlaydi va yaratish nuqtasini kengaytirish uchun ochiq qoldiradi. Shu tufayli yangi mahsulot turi qo'shish uchun framework kodini o'zgartirish shart emas - faqat yangi subclass yoki implementatsiya yoziladi.

**Spring'da qayerda uchraydi:** `@Bean` metodi - Spring terminologiyasida aynan "factory method" (`BeanDefinition.getFactoryMethodName()`); `FactoryBean.getObject()` va `AbstractFactoryBean.createInstance()` (qarang: [5-bo'lim](05-spring-core-ichidagi-patternlar-xaritasi.md), FactoryBean); `SpringApplication.createApplicationContext()` (Boot - `ApplicationContextFactory` orqali servlet yoki reactive kontekst tanlanadi); `AbstractRefreshableApplicationContext.createBeanFactory()`; `ClientHttpRequestFactory.createRequest(URI, HttpMethod)`; `ThreadFactory.newThread`; JDBC `DataSource.getConnection()`; JPA `EntityManagerFactory.createEntityManager()`; JMS `ConnectionFactory.createConnection()`. Spring'ning o'zi bean nusxalarini `InstantiationStrategy` (`SimpleInstantiationStrategy`, `CglibSubclassingInstantiationStrategy`) orqali yaratadi.

**Qo'llanish keyslari:**
- `@Configuration` sinfida uchinchi tomon kutubxonasi obyektini (`ObjectMapper`, `Caffeine`, `KafkaTemplate`) sozlab, bean sifatida yaratish.
- Hujjat eksporti: `ReportExporter` abstrakt sinfi `createWriter()` metodini e'lon qiladi, `PdfExporter` va `XlsxExporter` tegishli writer yaratadi.
- Thread yaratish siyosatini sozlash: nomlangan, daemon yoki virtual thread qaytaruvchi `ThreadFactory`.
- Test muhitida real klient o'rniga stub qaytaruvchi fabrika implementatsiyasini `@TestConfiguration` orqali almashtirish.
- Framework yoki kutubxona yozishda foydalanuvchiga yaratish nuqtasini `protected` metod bilan ochib berish (masalan, `createRequest`).

**Ehtiyot bo'ling:** Meros asosidagi klassik variant sinf ierarxiyasini ko'paytiradi - Spring'da ko'pincha interfeys + DI (yoki lambda `Supplier`) bilan yengilroq yechim bo'ladi. `@Bean` metodini `@Configuration` ichidan to'g'ridan-to'g'ri chaqirish faqat CGLIB proxy orqali singleton semantikasini saqlaydi; `proxyBeanMethods = false` bo'lsa, har chaqiruv yangi obyekt yaratadi. Fabrika metodida yaratish bilan birga biznes mantiqni aralashtirmang.

```java
public abstract class ReportExporter {
    public final void export(Report r, OutputStream out) {          // Template Method
        try (ReportWriter w = createWriter(out)) { w.write(r); }
    }
    protected abstract ReportWriter createWriter(OutputStream out); // Factory Method
}

public class PdfExporter extends ReportExporter {
    @Override protected ReportWriter createWriter(OutputStream out) {
        return new PdfReportWriter(out);
    }
}
```

## 1.8 Abstrakt fabrika (Abstract Factory)

**Tavsif:** Bir-biriga bog'liq yoki bir "oila"ga mansub obyektlar to'plamini (masalan, Connection + Statement + ResultSet) konkret sinflarni ko'rsatmasdan yaratish interfeysi. Klient faqat fabrika interfeysi va mahsulot interfeyslari bilan ishlaydi; konkret fabrika almashtirilsa, butun oila bir vaqtda almashadi va mahsulotlar bir-biriga mos bo'lishi kafolatlanadi. Factory Method'dan farqi - bir metod emas, bir nechta o'zaro mos mahsulot yaratuvchi metodlar to'plami.

**Spring'da qayerda uchraydi:** Spring Boot `WebServerFactory` oilasi: `ServletWebServerFactory` (`TomcatServletWebServerFactory`, `JettyServletWebServerFactory`, `UndertowServletWebServerFactory`) va `ReactiveWebServerFactory` - mahsulot `WebServer`; `ClientHttpRequestFactory` implementatsiyalari (`JdkClientHttpRequestFactory`, `HttpComponentsClientHttpRequestFactory`, `ReactorClientHttpRequestFactory`) - mahsulotlar `ClientHttpRequest` va `ClientHttpResponse`; `ApplicationContextFactory` (Boot); JDBC `DataSource -> Connection -> PreparedStatement -> ResultSet`; JPA `EntityManagerFactory -> EntityManager -> Query`; JMS `ConnectionFactory -> Connection -> Session -> MessageProducer`; Jackson `JsonFactory -> JsonParser / JsonGenerator`; `javax.xml.parsers.DocumentBuilderFactory`. `BeanFactory` nomi ham shu patternga ishora qiladi: u istalgan tipdagi bean'ni abstrakt tarzda yaratadi va qaytaradi.

**Qo'llanish keyslari:**
- Bir nechta cloud provayder (AWS/GCP/Azure) uchun bir-biriga mos `StorageClient`, `QueueClient`, `SecretsClient` oilasini bitta `CloudFactory` orqali tanlash.
- Ma'lumotlar bazasiga xos dialekt oilasi: `SqlDialect -> Paginator, UpsertBuilder, LockHint` - PostgreSQL va Oracle uchun turli implementatsiya.
- Test va production uchun bir-biriga mos infratuzilma obyektlari (real Kafka klienti vs in-memory implementatsiya) oilasini almashtirish.
- Embedded server tanlash (Tomcat/Jetty/Undertow) - Boot auto-configuration classpath'ga qarab mos `WebServerFactory` ni tanlaydi.
- Hujjat formatlari oilasi: `DocumentFactory -> Parser, Renderer, Validator` har format uchun o'zaro mos bo'lishi shart.

**Ehtiyot bo'ling:** Oila bitta mahsulotdan iborat bo'lsa, Abstract Factory - ortiqcha murakkablik; Factory Method yoki `@Bean` yetarli. Oilaga yangi mahsulot turi qo'shish barcha konkret fabrikalarni o'zgartirishni talab qiladi. Spring'da bu pattern ko'pincha `@Configuration` + `@Profile`/`@ConditionalOnProperty` orqali "oila"ni bitta konfiguratsiya sinfi sifatida almashtirish bilan tabiiy amalga oshadi - alohida fabrika interfeysi kerak bo'lmasligi mumkin.

```java
public interface CloudFactory {
    StorageClient storage();
    QueueClient queue();
    SecretsClient secrets();
}

@Configuration @Profile("aws")
class AwsCloudConfig {
    @Bean CloudFactory cloudFactory(S3Client s3, SqsClient sqs, SecretsManagerClient sm) {
        return new AwsCloudFactory(s3, sqs, sm);   // butun oila bir vaqtda almashadi
    }
}
```

## 1.9 Fabrika to'plami (Factory Kit)

**Tavsif:** Funksional uslubdagi fabrika: yaratish strategiyalari (`Supplier`/`Function`) kalit bo'yicha bitta "to'plam"ga ro'yxatdan o'tkaziladi (odatda builder yoki lambda orqali), keyin klient `kit.create(key)` bilan obyekt oladi. Factory Method'dan farqi - sinf ierarxiyasi va `switch` yo'q; yangi tur qo'shish uchun faqat yangi lambda ro'yxatdan o'tkaziladi. Simple Factory'ning Open/Closed muammosiga funksional yechim.

**Spring'da qayerda uchraydi:** `GenericApplicationContext.registerBean(Class<T>, Supplier<T>, BeanDefinitionCustomizer...)` - Spring 5+ dagi funksional bean ro'yxati aynan Supplier asosidagi fabrika to'plami; Spring Framework 7 dagi `BeanRegistrar` / `BeanRegistry` programmatik ro'yxat API'si ham shu g'oyani rivojlantiradi. Ilova kodida `Map<String, Supplier<Handler>>` yoki `Map<EventType, Function<Payload, Command>>` ko'rinishida; Spring Boot'da `ObjectProvider<T>` bilan birga lazy yaratish uchun ishlatiladi. Jackson'dagi `SimpleModule.addDeserializer` ham tip bo'yicha yaratuvchi ro'yxati.

**Qo'llanish keyslari:**
- Xabar turi bo'yicha (`"ORDER_CREATED"`, `"PAYMENT_FAILED"`) tegishli `Command` obyektini yaratish - `Map<String, Function<JsonNode, Command>>`.
- Plugin arxitekturasida har plugin o'z yaratuvchisini startup'da kit'ga ro'yxatdan o'tkazadi.
- Test ma'lumotlari uchun ssenariy nomi bo'yicha fixture yaratuvchilar to'plami.
- Prototype scope bean'larni kalit bo'yicha yaratish - `Map<Key, ObjectProvider<T>>`.
- Multi-format eksport: format nomi bo'yicha `Supplier<Exporter>`.

**Ehtiyot bo'ling:** Kalit sifatida satr ishlatish "stringly typed" xatolarga olib keladi - `enum` yoki sealed tip afzal (qarang: [25-bo'lim](25-anti-patternlar.md), Stringly Typed). Noma'lum kalit uchun aniq siyosat (exception yoki default) belgilang. Ro'yxat runtime'da o'zgaruvchan bo'lsa, thread-safety haqida o'ylang (`ConcurrentHashMap`, yoki startup'dan keyin immutable).

```java
// Factory Kit: yaratish retseptlari bitta joyda ro'yxatga olinadi
public interface NotifierKit {
    Notifier create(Channel channel);

    static NotifierKit of(Consumer<Map<Channel, Supplier<Notifier>>> recipes) {
        Map<Channel, Supplier<Notifier>> map = new EnumMap<>(Channel.class);
        recipes.accept(map);
        return channel -> Optional.ofNullable(map.get(channel))
                .orElseThrow(() -> new IllegalArgumentException("kanal yo'q: " + channel))
                .get();
    }
}

NotifierKit kit = NotifierKit.of(r -> {
    r.put(Channel.SMS, () -> new SmsNotifier(smsClient));
    r.put(Channel.EMAIL, () -> new EmailNotifier(mailSender));
});
```

## 1.10 Quruvchi (Builder, Step Builder, Lombok @Builder)

**Tavsif:** Ko'p parametrli (ayniqsa ixtiyoriy parametrli) yoki bosqichma-bosqich quriladigan murakkab obyektni yaratish jarayonini uning ko'rinishidan ajratadi: klient fluent metodlar bilan qismlarni belgilaydi, `build()` validatsiya qilib, immutable obyekt qaytaradi; "telescoping constructor" muammosini hal qiladi. **Step Builder (Staged Builder)** - har bosqich alohida interfeys qaytaradigan variant: majburiy parametrlar tartibini kompilyator kafolatlaydi, `build()` faqat oxirgi bosqichda mavjud. **Lombok `@Builder`** - builder sinfini kompilyatsiya vaqtida generatsiya qiladi; `@Builder.Default` (default qiymat), `@Singular` (kolleksiya uchun `add` metodlari), `toBuilder = true` (mavjud obyektdan nusxa builder), `@SuperBuilder` (meros ierarxiyasi), `@Jacksonized` (Jackson deserializatsiya bilan integratsiya); record'lar ustida ham ishlaydi.

**Spring'da qayerda uchraydi:** `UriComponentsBuilder`, `RestClient.builder()` / `WebClient.builder()`, `RestTemplateBuilder`, `ResponseEntity.status(...).headers(...).body(...)` (`BodyBuilder` - staged builder), `RequestEntity.post(uri).contentType(...).body(...)`, `MockMvcBuilders`, `BeanDefinitionBuilder`, `SpringApplicationBuilder`, `Jackson2ObjectMapperBuilder` (Jackson 3 bilan `JsonMapper.builder()`), `ServerResponse.ok().body(...)`. Spring Batch `JobBuilder` / `StepBuilder` - bosqichli builder'ning yaxshi namunasi (qarang: [20-bo'lim](20-batch-va-scheduling-patternlari.md)). Spring Security `HttpSecurity` DSL - builder + fluent DSL (qarang: [5-bo'lim](05-spring-core-ichidagi-patternlar-xaritasi.md), Fluent DSL builders). JDK: `StringBuilder`, `HttpRequest.newBuilder()`, `Stream.builder()`, `Locale.Builder`. Test uchun Test Data Builder - qarang: [23-bo'lim](23-testing-patternlari.md).

**Qo'llanish keyslari:**
- 4+ parametrli, ko'pi ixtiyoriy bo'lgan DTO/komanda obyektlarini yaratish (`SearchCriteria.builder().text(q).page(0).build()`).
- Konfiguratsiya obyektlarini sozlash: HTTP klient (timeout, interceptor, base URL) - `RestClient.builder()`.
- Immutable domen obyektini bosqichma-bosqich validatsiya bilan qurish; majburiy maydonlar uchun Step Builder (`customer` bosqichini tashlab ketish kompilyatsiya xatosi).
- Mavjud obyektning o'zgartirilgan nusxasini olish: `toBuilder().status(SHIPPED).build()` yoki `WebClient.mutate()`.
- Testlarda o'qilishi oson ma'lumot tayyorlash - `anOrder().withItems(3).paid().build()`.

**Ehtiyot bo'ling:** Lombok `@Builder` majburiy maydonlarni kafolatlamaydi - `build()` da hamma narsa `null` bo'lishi mumkin; yo `build()` ichida validatsiya qiling, yo Step Builder ishlating, yo record + compact constructor. `@Builder` sinfga qo'yilsa, Lombok all-args konstruktor yaratadi va JPA/Jackson uchun no-args konstruktor yo'qolishi mumkin (`@NoArgsConstructor` qo'shing). 2-3 parametrli oddiy sinf uchun builder - ortiqcha kod; record yoki static fabrika yetarli.

```java
// Step Builder: majburiy tartib kompilyator tomonidan kafolatlanadi
public interface NeedsCustomer { NeedsItem customer(CustomerId id); }
public interface NeedsItem    { Finish item(OrderLine line); }
public interface Finish       { Finish note(String n); Order build(); }

public static NeedsCustomer order() {
    return customer -> item -> new Finish() {          // lambda zanjiri
        String note;
        public Finish note(String n) { note = n; return this; }
        public Order build() { return new Order(customer, item, note); }
    };
}
// Chaqiruv: order().customer(id).item(line).note("gift").build();
```

## 1.11 Prototip (Prototype)

**Tavsif:** Yangi obyekt noldan yaratilmaydi - mavjud "namunaviy" obyektning nusxasi (clone/copy) olinadi va kerak bo'lsa o'zgartiriladi. Bu yaratish qimmat (ma'lumot yuklash, parsing) yoki konkret sinf runtime'da aniqlanadigan hollarda foydali. Java'da `Cloneable`/`clone()` muammoli hisoblanadi (Effective Java, Item 13); afzal yo'llar - copy constructor, `toBuilder()`, record uchun yangi qiymatlar bilan `new`, immutable obyekt uchun "wither" metodlar. Chuqur (deep) va yuzaki (shallow) nusxa farqini aniq belgilash shart.

**Spring'da qayerda uchraydi:** `@Scope(ConfigurableBeanFactory.SCOPE_PROTOTYPE)` - konteyner har `getBean()` chaqiruvida bean definition'dan yangi nusxa yaratadi (scope semantikasi va scoped proxy: qarang [5-bo'lim](05-spring-core-ichidagi-patternlar-xaritasi.md), Bean scopes & scoped proxy); `AbstractBeanDefinition.cloneBeanDefinition()` - Spring bean metadata'sini ko'paytirishda real Prototype; `WebClient.mutate()` / `RestClient.mutate()` - mavjud klientdan o'zgartirilgan nusxa; Jackson `ObjectMapper.copy()`; `new HttpHeaders(existing)` kabi copy constructor'lar; `BeanUtils.copyProperties` (yuzaki, reflection asosida); Apache Commons Lang `SerializationUtils.clone` (chuqur, serializatsiya orqali).

**Qo'llanish keyslari:**
- Bitta "asosiy" `ObjectMapper` ni `copy()` qilib, maxsus sozlangan variantlar (masalan, `FAIL_ON_UNKNOWN_PROPERTIES` o'chirilgan) yaratish.
- Umumiy `WebClient` dan `mutate()` orqali har tashqi servis uchun base URL va header'lari boshqa klient olish.
- Hujjat/shablon tizimi: yuklangan shablon obyektini har foydalanuvchi uchun nusxalab to'ldirish.
- Stateful, qisqa umrli yordamchi obyektlar (masalan, har so'rov uchun `ReportContext`) - Spring prototype scope + `ObjectProvider`.
- Test ma'lumotlari: bitta to'liq to'ldirilgan "golden" obyektdan `toBuilder()` bilan variantlar yasash.

**Ehtiyot bo'ling:** Yuzaki nusxa ichki mutable kolleksiyalarni bo'lishadi - bu "o'zgarmas" deb o'ylangan obyektlarda kutilmagan o'zgarishlarga olib keladi. Spring prototype bean'lari uchun konteyner `@PreDestroy` ni chaqirmaydi - resurslarni yopish klient zimmasida. Prototype bean singleton'ga to'g'ridan-to'g'ri inject qilinsa, faqat bir marta yaratiladi (qarang: 1.15).

```java
// Spring'da prototype scope + ObjectProvider orqali har safar yangi nusxa
@Component @Scope(ConfigurableBeanFactory.SCOPE_PROTOTYPE)
class ReportContext { /* so'rovga xos mutable holat */ }

@Service
class ReportService {
    private final ObjectProvider<ReportContext> contexts;
    ReportService(ObjectProvider<ReportContext> contexts) { this.contexts = contexts; }
    void run() { ReportContext ctx = contexts.getObject(); /* yangi nusxa */ }
}
```

## 1.12 Obyektlar hovuzi (Object Pool)

**Tavsif:** Yaratish va yo'q qilish qimmat bo'lgan obyektlar (ulanish, thread, katta buffer) oldindan yaratilib hovuzda saqlanadi; klient obyektni "oladi" (borrow), ishlatadi va "qaytaradi" (return), hovuz esa minimal/maksimal o'lcham, validatsiya, kutish vaqti va eskirganlarni yangilash siyosatini boshqaradi. Pattern latency'ni kamaytiradi va resurs sarfini cheklaydi - shu bilan backpressure vositasi sifatida ham xizmat qiladi.

**Spring'da qayerda uchraydi:** HikariCP (`spring.datasource.hikari.*`) - JDBC ulanishlar hovuzi (qarang: [9-bo'lim](09-malumotlarga-kirish-va-orm-patternlari.md), Connection Pool); `ThreadPoolTaskExecutor` / `ThreadPoolExecutor` (qarang: [4-bo'lim](04-concurrency-patternlari.md), Thread Pool / Executor); Spring JMS `CachingConnectionFactory` (session va producer keshi); R2DBC `ConnectionPool` (r2dbc-pool); Reactor Netty `ConnectionProvider` (HTTP ulanishlar hovuzi, `WebClient` ichida); Apache Commons Pool2 `GenericObjectPool` + `PooledObjectFactory`; Spring AOP'dagi `CommonsPool2TargetSource` (bean nusxalari hovuzi); Lettuce/Jedis Redis ulanish hovuzlari; Netty `PooledByteBufAllocator`.

**Qo'llanish keyslari:**
- Ma'lumotlar bazasi ulanishlari - HikariCP bilan `maximumPoolSize` ni CPU va DB imkoniyatiga qarab sozlash.
- Tashqi HTTP servislarga ulanishlar - Reactor Netty yoki Apache HttpClient connection pool.
- Qimmat, thread-safe bo'lmagan obyektlar: JAXB `Marshaller`/`Unmarshaller`, qimmat kriptografik kontekstlar.
- Katta `ByteBuffer`/`byte[]` bufferlarini qayta ishlatish - GC bosimini kamaytirish.
- Litsenziya yoki tashqi quota bilan cheklangan resurslar (masalan, bir vaqtda N ta SFTP sessiya).

**Ehtiyot bo'ling:** Qaytarilmagan obyekt - leak (HikariCP `leakDetectionThreshold` bilan aniqlang); hovuzga qaytarilayotgan obyekt holatini tozalash (reset) shart, aks holda bir klient holati boshqasiga "oqadi". Hovuz o'lchami noto'g'ri bo'lsa, u o'zi bottleneck bo'ladi (qarang: [25-bo'lim](25-anti-patternlar.md), Unbounded connection pool / wrong pool size). Virtual thread'lar (Java 21+) thread pool'ga ehtiyojni kamaytiradi, lekin ulanish hovuzlariga emas - DB ulanishlari hali ham cheklangan resurs.

```yaml
# Hovuz deyarli hech qachon qo'lda yozilmaydi - tayyorini sozlang
spring:
  datasource:
    hikari:
      maximum-pool-size: 20        # Little qonuni bilan hisoblangan qiymat
      minimum-idle: 20             # bir xil: pool "pulsatsiya" qilmaydi
      connection-timeout: 2000     # bo'sh ulanish yo'q bo'lsa tez xato
      max-lifetime: 1200000        # 20 daqiqa: DNS va failover uchun
```

## 1.13 Bog'liqliklarni kiritish (Dependency Injection)

**Tavsif:** Obyekt o'z bog'liqliklarini o'zi yaratmaydi yoki qidirmaydi - ular tashqaridan (konteyner yoki composition root tomonidan) beriladi. Bu Inversion of Control prinsipining obyekt yaratishga tatbiqi: sinf faqat "nimaga muhtoj"ligini e'lon qiladi, "qayerdan olish"ni bilmaydi. Turlari: **konstruktor orqali** (majburiy, immutable, test uchun eng qulay - tavsiya etiladi), **setter orqali** (ixtiyoriy yoki qayta sozlanadigan bog'liqliklar), **maydon (field) orqali** (`@Autowired` maydonga - qisqa, lekin yashirin va test uchun yomon), **metod orqali** (`@Autowired` ixtiyoriy nomli metodga yoki `@Lookup`) va Fowler bo'yicha **interfeys orqali** (Spring'dagi `*Aware` interfeyslari bunga yaqin).

**Spring'da qayerda uchraydi:** `@Autowired`, `jakarta.inject.Inject`, `@Resource` (nom bo'yicha), `@Value` (qiymatlar), `@Qualifier`/`@Primary` (bir nechta nomzod bo'lsa, qarang: [5-bo'lim](05-spring-core-ichidagi-patternlar-xaritasi.md)); yagona konstruktor bo'lsa `@Autowired` shart emas (Spring 4.3+); Lombok `@RequiredArgsConstructor` + `final` maydonlar - eng keng tarqalgan idioma; `@Bean` metod parametrlari ham inject qilinadi; kolleksiya inject: `List<Handler>` (`@Order` bo'yicha tartiblangan), `Map<String, Handler>` (bean nomi bo'yicha, qarang: [8-bo'lim](08-biznes-logika-va-service-qatlam-patternlari.md), Strategy registry via Map<String, Bean>); `Optional<T>`, `@Nullable`, `@Autowired(required = false)` - ixtiyoriy bog'liqlik; `@Lookup` - metod injection (qarang: [5-bo'lim](05-spring-core-ichidagi-patternlar-xaritasi.md)); testlarda `@TestConstructor` va JUnit 5 konstruktor injection. Boshqa DI konteynerlar: Guice, Dagger (kompilyatsiya vaqtida), Micronaut/Quarkus (AOT). Spring AOT ham bean yaratish kodini kompilyatsiya vaqtida generatsiya qiladi (GraalVM native uchun, qarang: [22-bo'lim](22-deployment-va-operatsion-patternlar.md)).

**Qo'llanish keyslari:**
- Service -> Repository -> DataSource kabi qatlamlar orasidagi bog'liqlikni konstruktor orqali e'lon qilish va `final` bilan immutable qilish.
- Interfeys orqali bog'lanib, implementatsiyani profil/property bilan almashtirish (`PaymentGateway` -> `StripeGateway` yoki `FakeGateway`).
- Barcha `Validator` implementatsiyalarini `List<Validator>` sifatida olib, zanjir qurish.
- Ixtiyoriy integratsiya (`Optional<MetricsPublisher>`) - mavjud bo'lsa ishlatish, bo'lmasa o'tkazib yuborish.
- Unit testda Spring'siz `new OrderService(fakeRepo, fixedClock)` - konstruktor injection buni bepul beradi.
- `java.time.Clock` ni inject qilib, vaqtga bog'liq mantiqni deterministik test qilish (qarang: [23-bo'lim](23-testing-patternlari.md), Clock injection).

**Ehtiyot bo'ling:** Field injection - yashirin bog'liqlik, `final` bo'la olmaydi, Spring'siz test qilish qiyin (qarang: [25-bo'lim](25-anti-patternlar.md), Field Injection); konstruktor injection circular bog'liqlikni darhol fosh qiladi - bu xato emas, dizayn signali (qarang: [25-bo'lim](25-anti-patternlar.md), Circular bean dependencies). Konstruktorda 7-8 dan ortiq parametr - sinf juda ko'p ish qilayotganining belgisi (God Object). Konteynerga bog'liq annotatsiyalarni domen qatlamiga tarqatmaslik uchun `jakarta.inject` yoki konfiguratsiya sinflari orqali wiring qilishni ko'rib chiqing (1.14).

```java
@Service
public class OrderService {
    private final OrderRepository orders;          // majburiy - konstruktor
    private final Clock clock;
    private final Optional<AuditPublisher> audit;  // ixtiyoriy

    public OrderService(OrderRepository orders, Clock clock, Optional<AuditPublisher> audit) {
        this.orders = orders; this.clock = clock; this.audit = audit;
    }

    @Autowired                                     // ixtiyoriy setter injection
    public void setRetryPolicy(RetryPolicy policy) { /* ... */ }
}
```

## 1.14 Kompozitsiya ildizi (Composition Root)

**Tavsif:** Ilovadagi obyekt grafi tarkibi (qaysi implementatsiya qaysi interfeysga bog'lanadi) bitta, ilova kirish nuqtasiga yaqin joyda jamlanadi; qolgan kod faqat konstruktor orqali bog'liqlik e'lon qiladi va konteyner haqida hech narsa bilmaydi. Mark Seemann ta'rifi bo'yicha, DI konteyner yoki qo'lda wiring faqat composition root'da chaqirilishi kerak. Bu pattern DI'ni "qayerda" amalga oshirish savoliga javob beradi va Service Locator'ga (1.16) qarshi vosita hisoblanadi.

**Spring'da qayerda uchraydi:** `@SpringBootApplication` sinfi + `SpringApplication.run(...)` va `@Configuration` sinflari jamlanmasi - Spring ilovasining composition root'i; component scanning esa uni "tarqatilgan" qiladi, shuning uchun ko'p arxitektorlar infratuzilma wiring'ini aniq `@Configuration` sinflariga (`PersistenceConfig`, `MessagingConfig`, `HttpClientConfig`) jamlashni afzal ko'radi. Hexagonal arxitekturada (qarang: [12-bo'lim](12-arxitektura-uslublari.md)) adapterlarni portlarga bog'lash aynan composition root'da bo'ladi; Spring Modulith modullari o'z konfiguratsiyasini `@Import` orqali ochadi (qarang: [5-bo'lim](05-spring-core-ichidagi-patternlar-xaritasi.md), @Import / ImportSelector). Testlarda `@TestConfiguration` - alternativ composition root (qarang: [23-bo'lim](23-testing-patternlari.md)).

**Qo'llanish keyslari:**
- Domen qatlamini Spring annotatsiyalaridan toza saqlash - domen servislari `@Configuration` ichida `@Bean` sifatida qo'lda yaratiladi.
- Bitta jar'dan turli deploy variantlari (CLI, web, batch) - har biri o'z composition root'i bilan, umumiy biznes kod bilan.
- Integratsion testlarda infratuzilma adapterlarini in-memory implementatsiyalarga almashtirish - faqat bitta konfiguratsiya sinfi o'zgaradi.
- Modular monolith'da har modulning ochiq API'si va ichki wiring'ini aniq konfiguratsiya sinfi bilan belgilash.
- Spring'siz kutubxonalarda `main` metodida qo'lda "Pure DI" wiring.

**Ehtiyot bo'ling:** Component scanning + hamma joyda `@Service` - qulay, lekin composition root yo'qoladi va "nima nimaga bog'langan"ini topish qiyinlashadi; kamida infratuzilma bog'liqliklarini aniq konfiguratsiyaga chiqaring. Bitta gigant `AppConfig` sinfi ham yomon - mavzu bo'yicha bo'ling. Over-broad component scanning (qarang: [25-bo'lim](25-anti-patternlar.md)) testlarni sekinlashtiradi va keraksiz bean'larni yuklaydi.

```java
// Composition Root: barcha wiring bitta joyda, biznes kodda `new` yo'q
@SpringBootApplication
public class PaymentsApplication {
    public static void main(String[] args) {
        SpringApplication.run(PaymentsApplication.class, args);
    }
}

// Infratuzilma wiring'ini aniq konfiguratsiyada ushlab turish, scanning'ga tashlamaslik
@Configuration(proxyBeanMethods = false)
class PaymentsInfrastructureConfig {
    @Bean
    PspClient pspClient(RestClient.Builder builder, PspProperties props) {
        return new PspClient(builder.baseUrl(props.url()).build(), props.timeout());
    }
}
```

## 1.15 Provider / Supplier orqali kiritish (Provider / Supplier Injection)

**Tavsif:** Bog'liqlikning o'zi emas, uni qaytaruvchi "fabrika tutqichi" (`Provider<T>`, `ObjectProvider<T>`, `Supplier<T>`) inject qilinadi; haqiqiy obyekt `get()` chaqirilganda olinadi. Bu bir nechta muammoni hal qiladi: singleton ichida har safar yangi prototype nusxa olish, bean'ni lazy olish, ixtiyoriy yoki bir nechta nomzodlarni xavfsiz qidirish, circular bog'liqlikni uzish. Spring'ning `ObjectProvider` qo'shimcha semantika beradi: `getIfAvailable()`, `getIfUnique()`, `getObject(args...)`, `orderedStream()`, `ifAvailable(consumer)`.

**Spring'da qayerda uchraydi:** `org.springframework.beans.factory.ObjectProvider<T>` (Spring 4.3+) va uning ota interfeysi `ObjectFactory<T>`; `jakarta.inject.Provider<T>` (classpath'da `jakarta.inject-api` bo'lsa Spring avtomatik qo'llab-quvvatlaydi); `BeanFactory.getBeanProvider(Class)` / `getBeanProvider(ResolvableType)` - programmatik variant; Spring Boot auto-configuration sinflari `ObjectProvider<RestClientCustomizer>`, `ObjectProvider<MeterRegistryCustomizer<?>>` kabi ixtiyoriy customizer'larni shu yo'l bilan oladi. `@Lookup` metod injection va `@Lazy` proxy - alternativ mexanizmlar (qarang: [5-bo'lim](05-spring-core-ichidagi-patternlar-xaritasi.md), ObjectProvider / lazy lookup va @Lookup method injection). Oddiy `Supplier<T>` avtomatik inject qilinmaydi - uni `@Bean` sifatida ro'yxatdan o'tkazish kerak.

**Qo'llanish keyslari:**
- Singleton `ReportService` ichida har hisobot uchun yangi prototype `ReportContext` olish - `provider.getObject()`.
- Ixtiyoriy bean: `metricsProvider.ifAvailable(m -> m.record(...))` - bean yo'q bo'lsa hech narsa bo'lmaydi.
- Bir nechta `Customizer` bean'larini `orderedStream()` bilan `@Order` tartibida qo'llash.
- Qimmat bean'ni faqat kerak bo'lgan kod yo'lida yuklash - startup'ni tezlashtirish.
- Ikki servis orasidagi circular bog'liqlikni vaqtincha uzish (lekin dizaynni qayta ko'rib chiqish shart).
- Prototype bean'ni runtime argumentlari bilan yaratish - `provider.getObject(arg1, arg2)` (bean'da mos konstruktor bo'lsa).

**Ehtiyot bo'ling:** Provider - bog'liqlikni yashiradi: sinfning haqiqiy bog'liqligi `T`, lekin imzoda `ObjectProvider<T>` ko'rinadi; faqat haqiqiy sabab bo'lsa ishlating. `getObject()` prototype uchun har chaqiruvda yangi nusxa yaratadi - tasodifan loop ichida chaqirilsa, ortiqcha yuk. `getIfUnique()` bir nechta nomzod bo'lib `@Primary` yo'q bo'lsa `null` qaytaradi - bu jim xato manbai bo'lishi mumkin.

```java
@Service
public class NotificationService {
    private final ObjectProvider<SmsSender> sms;       // ixtiyoriy
    private final ObjectProvider<Notifier> notifiers;  // bir nechta, tartibli

    NotificationService(ObjectProvider<SmsSender> sms, ObjectProvider<Notifier> notifiers) {
        this.sms = sms; this.notifiers = notifiers;
    }

    public void notify(Event e) {
        notifiers.orderedStream().forEach(n -> n.send(e));
        sms.ifAvailable(s -> s.send(e.phone(), e.text()));
    }
}
```

## 1.16 Servis topuvchi (Service Locator)

**Tavsif:** Markaziy obyekt (locator) kerakli servisni nom yoki tip bo'yicha topib beradi; klient bog'liqlikni "so'rab oladi" (dependency lookup), DI'da esa "qabul qiladi". Locator ichida registr, JNDI, konteyner yoki konfiguratsiya bo'lishi mumkin. Pattern konteyner yo'q yoki obyekt konteyner nazoratida yaratilmagan hollarda bog'liqliklarni olishning amaliy yo'li, lekin bog'liqlikni yashirgani uchun DI'ga nisbatan ikkinchi darajali variant hisoblanadi.

**Spring'da qayerda uchraydi:** `ApplicationContext.getBean(...)` / `BeanFactory` - Spring'ning o'zi klient uchun locator bo'la oladi (biznes kodda ishlatish anti-pattern: qarang [25-bo'lim](25-anti-patternlar.md), ApplicationContext.getBean() as Service Locator); `ApplicationContextAware` (qarang: [5-bo'lim](05-spring-core-ichidagi-patternlar-xaritasi.md), Aware interfaces); `ServiceLocatorFactoryBean` - interfeysdan avtomatik locator proxy yaratuvchi rasmiy Spring vositasi (`MyServiceFactory.getService(String name)` -> bean nomi bo'yicha qidirish); JNDI: `JndiTemplate`, `JndiObjectFactoryBean`; `java.util.ServiceLoader` va `SpringFactoriesLoader` - classpath darajasidagi locator'lar (qarang: [24-bo'lim](24-zamonaviy-java-va-funksional-patternlar.md), Service Provider Interface + ServiceLoader va [5-bo'lim](05-spring-core-ichidagi-patternlar-xaritasi.md), spring.factories (SPI)). Spring konteyner tashqarisida yaratiladigan obyektlar uchun ko'prik: Hibernate `SpringBeanContainer` (entity listener'larga bean'lar berish), Quartz `SpringBeanJobFactory`.

**Qo'llanish keyslari:**
- Konteyner tomonidan yaratilmaydigan obyektlar (JPA entity listener, Quartz job, legacy servlet filter) ichidan Spring bean'ga kirish - rasmiy ko'prik sinflari orqali.
- Runtime'da nom bo'yicha strategiya tanlash - `ServiceLocatorFactoryBean` bilan `switch`siz, konteynerga bog'lanmagan interfeys orqali.
- Legacy static kodni bosqichma-bosqich Spring'ga ko'chirishda vaqtincha `ApplicationContext` holder.
- Plugin'lar classpath'dan `ServiceLoader` orqali topilib, keyin Spring konteyneriga ro'yxatdan o'tkazilishi.
- Framework ichki kodi (`BeanFactoryUtils`, post-processor'lar) - konteyner bilan bevosita ishlash tabiiy.

**Ehtiyot bo'ling:** Locator bog'liqliklarni imzodan yashiradi: sinfni o'qib nimaga muhtojligini bilib bo'lmaydi, unit test uchun butun konteyner yoki static mock kerak. Bean nomiga satr orqali bog'lanish refaktoringni buzadi. Agar `getBean()` biznes kodda uchrayotgan bo'lsa, odatda `ObjectProvider` (1.15), `Map<String, T>` injection yoki `@Lookup` to'g'riroq yechim bo'ladi.

```java
// Anti-pattern: bog'liqlik yashiringan, test uchun mock qilish qiyin
@Service
public class BadOrderService {
    private final ApplicationContext ctx;
    public void place(Order o) {
        ctx.getBean(PricingService.class).price(o);   // locator: yashirin bog'liqlik
    }
}

// To'g'ri: bog'liqlik konstruktorda ko'rinadi
@Service
public class OrderService {
    private final PricingService pricing;
    public OrderService(PricingService pricing) { this.pricing = pricing; }
    public void place(Order o) { pricing.price(o); }
}
```

## 1.17 Reyestr (Registry)

**Tavsif:** Kalit bo'yicha obyektlarni (implementatsiya, konfiguratsiya, metadata) ro'yxatdan o'tkazish va topish uchun yaxshi ma'lum bo'lgan markaziy obyekt (Fowler, PoEAA). Reyestr yaratishni emas, "qayerda topish"ni hal qiladi, lekin ko'pincha fabrika bilan birga ishlaydi: fabrika yaratadi, reyestr saqlaydi va qaytaradi. Statik (global) yoki instance (konteyner nazoratida) bo'lishi mumkin; zamonaviy amaliyotda instance variant + DI afzal.

**Spring'da qayerda uchraydi:** `BeanDefinitionRegistry`, `SingletonBeanRegistry` / `DefaultSingletonBeanRegistry`, `AliasRegistry` - konteynerning o'zagi (qarang: [5-bo'lim](05-spring-core-ichidagi-patternlar-xaritasi.md), Bean definition & BeanDefinitionRegistry); `ConverterRegistry` / `FormatterRegistry` (qarang: [5-bo'lim](05-spring-core-ichidagi-patternlar-xaritasi.md), ConversionService); `HandlerMapping` ichidagi URL -> handler reyestri (qarang: [6-bo'lim](06-web-va-taqdimot-qatlami-patternlari.md)); Actuator `HealthContributorRegistry`; Micrometer `MeterRegistry` (qarang: [21-bo'lim](21-observability-patternlari.md)); Resilience4j `CircuitBreakerRegistry` (qarang: [17-bo'lim](17-resilience-va-cloud-dizayn-patternlari.md)); JDBC `DriverManager` - klassik statik reyestr; Kafka Schema Registry (qarang: [16-bo'lim](16-enterprise-integration-patterns-ii.md)); mikroservislarda Service Registry / Eureka (qarang: [14-bo'lim](14-microservices-patternlari.md)). Ilova kodida eng keng tarqalgan ko'rinishi - `Map<String, Strategy>` injection (qarang: [8-bo'lim](08-biznes-logika-va-service-qatlam-patternlari.md), Strategy registry via Map<String, Bean>) yoki `EnumMap<Type, Handler>`.

**Qo'llanish keyslari:**
- Barcha `PaymentHandler` bean'larini `Map<PaymentMethod, PaymentHandler>` ga yig'ib, so'rov turiga qarab tanlash.
- Plugin/modul registratsiyasi: har modul startup'da o'z `Extension` larini reyestrga qo'shadi (`SmartInitializingSingleton` ichida).
- Metadata reyestri: event turi -> schema/versiya, tenant -> konfiguratsiya.
- Dinamik ro'yxat: runtime'da yuklanadigan skript/qoida obyektlarini saqlash va almashtirish.
- Health, metrika, circuit-breaker kabi nomlangan infratuzilma obyektlarini markazlashtirish.

**Ehtiyot bo'ling:** Statik reyestr - global mutable holat, testlar orasida "oqadi" va parallel testlarni buzadi; konteyner nazoratidagi bean reyestri afzal. Satr kalitlar yozuv xatolariga olib keladi - `enum` yoki tip-xavfsiz kalit ishlating. Reyestrga ro'yxatdan o'tkazish tartibi va thread-safety (runtime'da o'zgarsa) haqida aniq qaror qabul qiling; startup'dan keyin immutable qilish eng xavfsiz.

```java
// Reyestr: nomlangan implementatsiyalar konteyner tomonidan yig'iladi
public interface PaymentHandler {
    PaymentMethod method();
    Receipt pay(Payment payment);
}

@Service
public class PaymentHandlerRegistry {
    private final Map<PaymentMethod, PaymentHandler> handlers;

    // Spring barcha PaymentHandler bean'larini ro'yxatga oladi
    public PaymentHandlerRegistry(List<PaymentHandler> all) {
        this.handlers = all.stream()
                .collect(Collectors.toUnmodifiableMap(PaymentHandler::method, h -> h));
    }

    public PaymentHandler forMethod(PaymentMethod m) {
        PaymentHandler h = handlers.get(m);
        if (h == null) throw new UnsupportedPaymentMethodException(m);
        return h;
    }
}
```

## 1.18 Amalda qo'llash

- [ ] Servis va controller sinflarida `new` bilan yaratilgan har bir obyektni ro'yxatga oling va qaysilari konteyner nazoratiga o'tishi kerakligini belgilang.
- [ ] `getInstance()` metodi bor sinflarni toping; har biri uchun DI ga o'tkazish yoki qoldirish qarorini sabab bilan yozib qo'ying.
- [ ] Singleton scope'dagi bean'larning `final` bo'lmagan maydonlarini sanab chiqing - har biri race condition nomzodi.
- [ ] 6 dan ko'p parametr oladigan konstruktorlarni toping va ularga Builder yoki parametr obyekti qo'llash rejasini tuzing.
- [ ] Prototype bean'lar singleton ichiga to'g'ridan-to'g'ri inject qilingan joylarni qidiring va `ObjectProvider` yoki scoped proxy ga o'tkazing.
- [ ] Kalit bo'yicha nusxa saqlaydigan har bir `Map` ni tekshiring: kalitlar to'plami chegaralanganmi, eviction bormi, nusxalar yopiladimi.
- [ ] `spring.main.lazy-initialization` qiymatini muhitlar bo'yicha tekshiring va production'da `false` turganini tasdiqlang.
- [ ] Service Locator ko'rinishidagi kodni (`applicationContext.getBean(...)`) qidirib, har bir chaqiruvni konstruktor injeksiyasiga aylantirish rejasini yozing.

---

[Mundarija](README.md) · [2. Strukturaviy patternlar &rarr;](02-strukturaviy-patternlar.md)
