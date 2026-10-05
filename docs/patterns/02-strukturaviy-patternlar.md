<!-- doc: patterns | chapter: 2 | part:  -->

[Barcha hujjatlar](../../README.md) / [Dizayn patternlar](README.md)

> Holat: AI yozgan, inson tekshirmagan.

# 2. Strukturaviy patternlar (Structural Patterns)

<details>
<summary>Bu bo'limdagi 18 bo'lim</summary>

- [2.1 Adapter (Adapter)](#21-adapter-adapter)
- [2.2 Ko'prik (Bridge)](#22-koprik-bridge)
- [2.3 Kompozit (Composite)](#23-kompozit-composite)
- [2.4 Dekorator (Decorator)](#24-dekorator-decorator)
- [2.5 Fasad (Facade)](#25-fasad-facade)
- [2.6 Flyweight (Flyweight)](#26-flyweight-flyweight)
- [2.7 Proxy (Proxy - static, JDK dynamic proxy, CGLIB)](#27-proxy-proxy---static-jdk-dynamic-proxy-cglib)
- [2.8 Marker interfeys (Marker Interface)](#28-marker-interfeys-marker-interface)
- [2.9 Modul (Module)](#29-modul-module)
- [2.10 Yopiq sinf ma'lumotlari (Private Class Data)](#210-yopiq-sinf-malumotlari-private-class-data)
- [2.11 Kengaytirish obyekti (Extension Object)](#211-kengaytirish-obyekti-extension-object)
- [2.12 Egizak (Twin)](#212-egizak-twin)
- [2.13 Delegatsiya (Delegation)](#213-delegatsiya-delegation)
- [2.14 O'rovchi (Wrapper)](#214-orovchi-wrapper)
- [2.15 Mixin / Trait default metodlar orqali (Mixin / Trait via default methods)](#215-mixin--trait-default-metodlar-orqali-mixin--trait-via-default-methods)
- [2.16 Qatlam ustki turi (Layer Supertype)](#216-qatlam-ustki-turi-layer-supertype)
- [2.17 Ajratilgan interfeys (Separated Interface)](#217-ajratilgan-interfeys-separated-interface)
- [2.18 Amalda qo'llash](#218-amalda-qollash)

</details>



Strukturaviy patternlar obyektlar va sinflarni kattaroq tuzilmalarga birlashtirish usullarini belgilaydi - ya'ni ular "nima yaratiladi" degan savolga emas, "qanday ulanadi" degan savolga javob beradi. Arxitektor uchun bu kategoriya hal qiluvchi, chunki aynan shu patternlar modullar orasidagi chegaralarni (boundary) chizadi: legacy tizimni yangi API'ga ulash, abstraksiyani implementatsiyadan ajratish, cross-cutting concern'larni biznes-logikaga tegmasdan qo'shish - barchasi shu yerdan chiqadi. Spring Framework'ning o'zi ham asosan strukturaviy patternlar ustiga qurilgan: AOP, transaction management, caching va security'ning hammasi proxy va decorator mexanizmlariga tayanadi. Shu sababli bu patternlarni bilmasdan Spring'ning "sehr"ini tushunish va debug qilish amalda imkonsiz.

## 2.1 Adapter (Adapter)

**Tavsif:** Adapter bir sinfning interfeysini client kutgan boshqa interfeysga o'giradi. Mavjud kodni (ko'pincha legacy yoki tashqi kutubxona) o'zgartirmasdan yangi tizimga ulash imkonini beradi. Ichida wrapper obyekt saqlanadi (object adapter) yoki meros orqali amalga oshiriladi (class adapter). Natijada ikki mos kelmaydigan abstraksiya bir-biri bilan gaplashadi.

**Spring'da qayerda uchraydi:** `HandlerAdapter` interfeysi va uning `RequestMappingHandlerAdapter`, `HttpRequestHandlerAdapter`, `SimpleControllerHandlerAdapter` implementatsiyalari - `DispatcherServlet` turli handler tiplarini yagona usulda chaqirishi uchun. Shuningdek `MessageSource` adapterlari, Spring Data'dagi `PagingAndSortingRepository` ustidagi moslashtiruvchilar, `SpringBeanJobFactory` (Quartz), va klassik JDK misoli - `java.io.InputStreamReader` (byte stream'ni char stream'ga adaptatsiya). Spring Boot 3.x'da `MicrometerObservationCapability` kabi sinflar tashqi kutubxona metrikalarini Micrometer `Observation` API'siga adaptatsiya qiladi.

**Qo'llanish keyslari:**
- Legacy SOAP servisni yangi REST-ga asoslangan domain interfeysi ortida yashirish.
- Uchinchi tomon payment gateway SDK'sini o'zingizning `PaymentProvider` port interfeysiga moslashtirish.
- Hexagonal (ports & adapters) arxitekturada har bir tashqi tizim uchun alohida adapter yozish.
- Eski DTO formatini yangi API contract'iga mapping qilish (masalan, migratsiya davrida ikki versiyani parallel qo'llab-quvvatlash).
- Turli xil message broker client'larini (Kafka, RabbitMQ) yagona `EventPublisher` abstraksiyasi ortiga yig'ish.

**Ehtiyot bo'ling:** Adapter faqat interfeysni o'girishi kerak - unga biznes-logika, validatsiya yoki transformatsiya qoidalarini yuklash "god adapter"ga olib keladi. Agar ikki interfeys mohiyatan bir xil bo'lsa, adapter qatlami ortiqcha indirection va debug qiyinchiligidan boshqa narsa bermaydi.

```java
// Adapter: tashqi SDK shaklini o'z portimizga moslaydi
public interface SmsGateway {                 // bizning port
    void send(PhoneNumber to, String text);
}

@Component
class TwilioSmsAdapter implements SmsGateway {
    private final TwilioRestClient twilio;    // tashqi SDK, shakli boshqa

    TwilioSmsAdapter(TwilioRestClient twilio) { this.twilio = twilio; }

    @Override
    public void send(PhoneNumber to, String text) {
        // SDK atamalari shu sinfdan tashqariga chiqmaydi
        twilio.messages().create(new MessageParams(to.e164(), text));
    }
}
```

## 2.2 Ko'prik (Bridge)

**Tavsif:** Bridge abstraksiyani uning implementatsiyasidan ajratib, ikkisini mustaqil ravishda rivojlantirish imkonini beradi. Abstraksiya ierarxiyasi implementatsiya ierarxiyasiga kompozitsiya orqali murojaat qiladi, meros orqali emas. Bu sinflar sonining kombinator portlashini (M×N o'rniga M+N) oldini oladi. Adapter'dan farqi: Bridge dizayn vaqtida ataylab rejalashtiriladi, Adapter esa mavjud nomuvofiqlikni keyin tuzatadi.

**Spring'da qayerda uchraydi:** Eng toza misol - SLF4J: `Logger` abstraksiyasi va orqadagi Logback/Log4j2 binding'lari. Spring'ning o'zida `spring-jcl` moduli xuddi shu ko'prik rolini bajaradi. Shuningdek `ResourceLoader`/`Resource` (bir abstraksiya, ko'p implementatsiya: `ClassPathResource`, `FileSystemResource`, `UrlResource`), `CacheManager` va `Cache` (Caffeine, Redis, EhCache), `PlatformTransactionManager` va uning `JpaTransactionManager`/`DataSourceTransactionManager`/`JtaTransactionManager` implementatsiyalari, hamda `JdbcTemplate` ostidagi `DataSource`. Java standartida `java.sql.Driver` va JDBC API ham Bridge namunasi.

**Qo'llanish keyslari:**
- Notification abstraksiyasini (`Notification`: oddiy, urgent, batch) yetkazib berish kanalidan (SMS, email, push) ajratish.
- Bir xil hisobot logikasini turli renderer (PDF, XLSX, HTML) ustida ishlatish.
- Multi-tenant tizimda tenant-specific storage backend'ini biznes abstraksiyasidan uzish.
- Caching strategiyasini (write-through, TTL) konkret cache provider'dan mustaqil saqlash.
- Feature-flag abstraksiyasini orqadagi provayderdan (local config, Unleash, LaunchDarkly) ajratish.

**Ehtiyot bo'ling:** Agar implementatsiya kelgusida almashmaydigan bo'lsa, Bridge faqat ortiqcha qatlam va kognitiv yuk qo'shadi - YAGNI'ni eslang. Ikkala ierarxiya bir vaqtda o'sib ketsa, ularning shartnomasini sinxron ushlab turish qimmatga tushadi.

```java
// Bridge: abstraksiya va implementatsiya alohida ierarxiyada o'sadi
public abstract class Report {                       // abstraksiya
    protected final ReportRenderer renderer;         // implementatsiyaga ko'prik
    protected Report(ReportRenderer renderer) { this.renderer = renderer; }
    public abstract byte[] render();
}

public interface ReportRenderer {                    // implementatsiya ierarxiyasi
    byte[] render(ReportModel model);
}

public class InvoiceReport extends Report {
    private final Invoice invoice;
    public InvoiceReport(ReportRenderer r, Invoice i) { super(r); this.invoice = i; }
    @Override public byte[] render() { return renderer.render(ReportModel.of(invoice)); }
}
// PdfRenderer, XlsxRenderer va HtmlRenderer Report ierarxiyasini o'zgartirmaydi
```

## 2.3 Kompozit (Composite)

**Tavsif:** Composite obyektlarni daraxt tuzilmasiga yig'ib, yakka obyekt (leaf) va obyektlar guruhi (composite) bilan client'ning bir xil muomala qilishini ta'minlaydi. Ikkisi ham bitta umumiy interfeysni implement qiladi, shuning uchun client `if (guruhmi?)` tekshiruvlaridan xalos bo'ladi. Rekursiv tuzilmalarni ifodalashning tabiiy usuli.

**Spring'da qayerda uchraydi:** `CompositeCacheManager`, `CompositeHealthContributor` va Spring Boot Actuator'dagi `CompositeHealth`, `DelegatingFilterProxy` bilan birga ishlatiladigan `FilterChainProxy` (Spring Security), `CompositeMeterRegistry` (Micrometer), `CompositePropertySource` va `MutablePropertySources` (`Environment` ichida), `CompositeMessageConverter`, Spring Security'dagi `DelegatingPasswordEncoder` hamda `CompositeUserDetailsService` uslubidagi delegatsiyalar. Bean validation'da `Validator`lar guruhini birlashtirgan `CompositeValidator`-ga o'xshash sinflar ham xuddi shu g'oyani ishlatadi.

**Qo'llanish keyslari:**
- Mahsulot katalogida kategoriya → subkategoriya → mahsulot daraxtini bir interfeys bilan aylanib chiqish.
- Buyurtma narxini hisoblashda bundle (to'plam) va yakka tovarni bir xil `calculatePrice()` chaqiruvi bilan baholash.
- Tashkilot ierarxiyasida bo'lim va xodim ustida umumlashgan hisob-kitob (masalan, umumiy maosh fondi).
- Murakkab validation qoidalarini AND/OR daraxti sifatida qurish.
- Health check'larni subsystem'lar bo'yicha guruhlab, bitta aggregated status qaytarish.

**Ehtiyot bo'ling:** Chuqur daraxtlarda rekursiv traversal kutilmagan N+1 query yoki `StackOverflowError`ga olib kelishi mumkin - chuqurlik limitini va lazy loading'ni nazorat qiling. `add()`/`remove()` metodlarini umumiy interfeysga chiqarish leaf uchun ma'nosiz operatsiyalar (`UnsupportedOperationException`) tug'diradi, shuning uchun shaffoflik va xavfsizlik orasidagi tanlovni ongli qiling.

```java
// Composite: bitta va ko'p bir xil interfeys ortida
@Component
@Primary
public class CompositeFraudCheck implements FraudCheck {
    private final List<FraudCheck> checks;

    public CompositeFraudCheck(List<FraudCheck> checks) {
        // o'zini ro'yxatga olmaslik uchun @Primary emas, filtrlangan ro'yxat kerak bo'lsa
        this.checks = checks.stream().filter(c -> c != this).toList();
    }

    @Override
    public Decision check(Payment payment) {
        for (FraudCheck c : checks) {
            Decision d = c.check(payment);
            if (d.isReject()) return d;      // birinchi rad etish yetarli
        }
        return Decision.accept();
    }
}
```

## 2.4 Dekorator (Decorator)

**Tavsif:** Decorator obyektni bir xil interfeysli wrapper ichiga o'rab, unga runtime'da yangi xatti-harakat qo'shadi. Merosdan farqli ravishda bir nechta decorator'ni zanjir qilib ulash mumkin va kombinatsiyalar compile vaqtida qotib qolmaydi. Har bir decorator o'z ishini bajarib, chaqiruvni ichki obyektga uzatadi.

**Spring'da qayerda uchraydi:** `TransactionAwareCacheDecorator`, `BeanFactoryPostProcessor` bilan emas balki `BeanPostProcessor` orqali yaratiladigan AOP wrapper'lar, `HttpServletRequestWrapper`/`HttpServletResponseWrapper` (Servlet API), `ContentCachingRequestWrapper` va `ContentCachingResponseWrapper` (Spring Web), `DelegatingDataSource` va `TransactionAwareDataSourceProxy`, `LazyConnectionDataSourceProxy`, Spring Security'dagi `SecurityContextHolderAwareRequestWrapper`. Reactive stack'da `ServerHttpRequestDecorator`/`ServerHttpResponseDecorator` va `WebFilter` zanjiri aynan shu patternni ishlatadi; JDK misoli - `BufferedInputStream`.

**Qo'llanish keyslari:**
- Request body'ni log qilish uchun uni `ContentCachingRequestWrapper` bilan o'rash (stream bir marta o'qiladi muammosini hal qilish).
- Repository ustiga retry, metrics yoki audit qatlamini biznes-koddan tashqarida qo'shish.
- `RestClient`/`WebClient` filterlari bilan har bir chiquvchi so'rovga correlation ID qo'shish.
- `DataSource`ni o'rab, sekin query'larni aniqlash yoki read-only replica'ga yo'naltirish.
- Rate limiting yoki quota tekshiruvini servis implementatsiyasini o'zgartirmasdan ulash.

```java
public class RetryingPaymentClient implements PaymentClient {
    private final PaymentClient delegate;
    public RetryingPaymentClient(PaymentClient delegate) { this.delegate = delegate; }

    @Override public Receipt charge(Order order) {
        for (int attempt = 1; ; attempt++) {
            try { return delegate.charge(order); }
            catch (TransientPaymentException e) {
                if (attempt == 3) throw e;
            }
        }
    }
}
```

**Ehtiyot bo'ling:** Uzun decorator zanjiri stack trace'ni o'qishni qiyinlashtiradi va har bir qatlam latency qo'shadi - zanjir tartibi (masalan, transaction decorator cache'dan oldinmi yoki keyinmi) natijaga ta'sir qiladi. Decorator ichida `this` orqali o'z metodini chaqirish wrapper'ni chetlab o'tadi; Spring'da ham self-invocation proxy'ni aylanib o'tib, `@Transactional` yoki `@Cacheable` ishlamay qolishiga sabab bo'ladi.

## 2.5 Fasad (Facade)

**Tavsif:** Facade murakkab quyi tizimga soddalashtirilgan, yuqori darajadagi yagona kirish nuqtasini beradi. Client ko'p sinf bilan emas, bitta interfeys bilan ishlaydi va quyi tizimning ichki tuzilishiga bog'lanmaydi. Facade quyi tizim imkoniyatlarini yashirmaydi - faqat eng ko'p ishlatiladigan use-case'larni qulay qiladi.

**Spring'da qayerda uchraydi:** `JdbcTemplate` va `JdbcClient` (Spring Framework 6.1+) - JDBC'ning `Connection`/`Statement`/`ResultSet` va resource yopish murakkabligini yashiradi. Shuningdek `RestClient` (6.1+), `RestTemplate`, `JmsTemplate`, `RabbitTemplate`, `KafkaTemplate`, `TransactionTemplate`, `MongoTemplate`, `RedisTemplate`, `SimpleJpaRepository` ustidagi Spring Data abstraksiyalari va `SpringApplication.run(...)` - butun bootstrap jarayonining fasadi. Spring Security'da `AuthenticationManager` autentifikatsiya provayderlari to'plamiga fasad bo'lib xizmat qiladi.

**Qo'llanish keyslari:**
- Application service qatlamini bir nechta domain servis va repository ustiga fasad sifatida qurish (use-case bir metod).
- Microservice'da bir nechta downstream chaqiruvni birlashtirgan aggregation endpoint.
- Legacy modul bilan integratsiyada tashqi dunyoga faqat tor, barqaror API ochish.
- Murakkab PDF/hisobot generatsiya pipeline'ini bitta `ReportService.generate(...)` ortiga yig'ish.
- Onboarding flow'da user yaratish, email yuborish va audit yozishni bitta tranzaksion metodga jamlash.

**Ehtiyot bo'ling:** Facade asta-sekin "god service"ga aylanib, yuzlab metodli va hamma narsani biladigan sinfga o'sib ketishi juda keng tarqalgan xato - uni use-case bo'yicha bo'lib tashlang. Agar facade faqat bitta metodni bitta sinfga uzatsa, u hech qanday qiymat qo'shmaydigan anemik qatlam.

```java
// Facade: JDBC murakkabligi yashiringan, resurs yopish Spring zimmasida
@Repository
public class OrderQueries {
    private final JdbcClient db;                 // Spring Framework 6.1+

    public OrderQueries(JdbcClient db) { this.db = db; }

    public Optional<OrderSummary> findSummary(long id) {
        return db.sql("SELECT id, status, total FROM orders WHERE id = :id")
                 .param("id", id)
                 .query(OrderSummary.class)
                 .optional();
    }
}
// Connection, PreparedStatement, ResultSet va try-with-resources ko'rinmaydi
```

## 2.6 Flyweight (Flyweight)

**Tavsif:** Flyweight ko'p sonli mayda obyektlarning umumiy (intrinsic) holatini ulashib, xotira iste'molini kamaytiradi. O'zgaruvchi (extrinsic) holat esa tashqaridan parametr sifatida uzatiladi. Shart - obyekt immutable bo'lishi, aks holda ulashish race condition va kutilmagan mutatsiyalarga olib keladi.

**Spring'da qayerda uchraydi:** JDK darajasida `Integer.valueOf()` cache'i (-128..127), `String` interning va `String` constant pool, `Boolean.valueOf()`, `java.time` sinflarining (`LocalDate`, `Duration`) immutable tabiati. Spring ekotizimida singleton scope'dagi bean'larning o'zi ulashilgan stateless obyekt sifatida shu g'oyaga yaqin; `MediaType` konstantalari, `HttpMethod.valueOf()` (6.x'da `HttpMethod` enum emas, lekin konstantalar ulashiladi), `ResolvableType` cache'i va `AnnotationUtils`/`ReflectionUtils` ichidagi metadata cache'lari. Java 21+ dagi `record` tiplari esa flyweight-friendly value obyektlarni yozishni osonlashtiradi.

**Qo'llanish keyslari:**
- Million qatorli importda takrorlanuvchi valyuta kodi, mamlakat kodi yoki tarif nomlarini interning orqali ulashish.
- Domain'dagi `Currency`, `Unit`, `Country` kabi value obyektlar uchun oldindan yaratilgan konstanta pool.
- Katta hisobotlarda bir xil formatlash konfiguratsiyasini (pattern, locale) qayta ishlatish.
- Rule engine'da bir xil qoida ta'rifini minglab kontekst uchun bitta nusxada saqlash.
- Stateless strategy bean'larini singleton qilib, har bir request uchun yangi obyekt yaratmaslik.

**Ehtiyot bo'ling:** `String.intern()` va cheksiz o'sadigan `HashMap` pool'lari metaspace/heap leak'ga sabab bo'ladi - chegarali cache (Caffeine, `maximumSize`) ishlating. Flyweight'ni mutable holat bilan aralashtirish eng xavfli xato: singleton bean ichida request-specific field saqlash klassik thread-safety buzilishi.

```java
// Flyweight: o'zgarmas, ko'p takrorlanadigan qiymatlar qayta ishlatiladi
public final class Currency3 {
    private static final Map<String, Currency3> CACHE = new ConcurrentHashMap<>();
    private final String code;

    private Currency3(String code) { this.code = code; }

    public static Currency3 of(String code) {     // bir xil kod -> bir xil nusxa
        return CACHE.computeIfAbsent(code, Currency3::new);
    }
    public String code() { return code; }
}

// JDK dagi tayyor flyweight'lar
Integer small = Integer.valueOf(42);   // -128..127 oralig'i keshlangan
Boolean yes = Boolean.valueOf(true);   // har doim bir xil nusxa
```

## 2.7 Proxy (Proxy - static, JDK dynamic proxy, CGLIB)

**Tavsif:** Proxy haqiqiy obyekt bilan bir xil interfeysni taqdim etib, unga murojaatni nazorat qiladi: kechiktirilgan yaratish (lazy), huquq tekshiruvi, caching, remoting yoki logging qo'shishi mumkin. Static proxy qo'lda yoziladi; JDK dynamic proxy `java.lang.reflect.Proxy` orqali runtime'da faqat interfeys asosida generatsiya qilinadi; CGLIB (Spring'da `spring-core` ichiga repackage qilingan) subclass yaratib, interfeyssiz sinflarni ham proxy qiladi. Decorator'dan farqi - maqsad: Decorator xatti-harakat qo'shadi, Proxy esa kirishni boshqaradi.

**Spring'da qayerda uchraydi:** `ProxyFactory`, `JdkDynamicAopProxy`, `CglibAopProxy` va `DefaultAopProxyFactory` tanlovi; `@EnableAspectJAutoProxy(proxyTargetClass = true)` yoki `spring.aop.proxy-target-class` property. `@Transactional`, `@Cacheable`, `@Async`, `@Retryable`, `@PreAuthorize` - barchasi proxy orqali ishlaydi. `@Configuration` sinflari CGLIB bilan subclass qilinadi (`proxyBeanMethods = true`), `@ConfigurationProperties` esa emas. Hibernate'ning lazy association'lari ham proxy (`LazyInitializationException` manbasi), `DelegatingFilterProxy` Servlet filter'ni Spring context'iga ulaydi, Spring Data repository'lari `JdkDynamicAopProxy` + `RepositoryFactorySupport` orqali yaratiladi. Spring Boot 3.x AOT/native image rejimida proxy'lar build vaqtida ro'yxatdan o'tkazilishi kerak.

**Qo'llanish keyslari:**
- Declarative transaction boundary: `@Transactional` metod chaqiruvini proxy ochib-yopadi.
- Metod natijasini `@Cacheable` bilan cache qilish va `@CacheEvict` bilan tozalash.
- Metod darajasidagi security: `@PreAuthorize("hasRole('ADMIN')")` tekshiruvi proxy ichida.
- `@Async` bilan chaqiruvni task executor'ga uzatish (fire-and-forget yoki `CompletableFuture`).
- HTTP interface client'lari (`@HttpExchange` + `HttpServiceProxyFactory`) - interfeys asosida runtime'da client generatsiyasi.

**Ehtiyot bo'ling:** Eng ko'p uchraydigan tuzoq - self-invocation: bir metod ichida `this.other()` chaqirilsa proxy chetlab o'tiladi va `@Transactional`/`@Cacheable` ishlamaydi (yechim: alohida bean, `AopContext.currentProxy()` yoki self-injection). CGLIB `final` sinf/metodni proxy qilolmaydi, parametrsiz constructor talab qiladi va `private` metodlarga ta'sir qilmaydi; JDK proxy esa faqat interfeys metodlarini qamraydi, shuning uchun konkret tipga `cast` qilish `ClassCastException` beradi.

```java
// Spring proxy qanday tanlanadi va qachon chetlab o'tiladi
@Service
public class ReportService {

    @Transactional                       // proxy orqali ishlaydi
    public void generate(long id) {
        store(id);                       // TUZOQ: self-invocation, proxy chetlab o'tiladi
    }

    @Transactional(propagation = Propagation.REQUIRES_NEW)
    public void store(long id) { /* ... */ }
}

// Yechim: chegarani boshqa bean'ga chiqarish
@Service
public class ReportFacade {
    private final ReportWriter writer;           // alohida bean = alohida proxy
    public ReportFacade(ReportWriter writer) { this.writer = writer; }

    public void generate(long id) { writer.store(id); }   // proxy ishlaydi
}
```

## 2.8 Marker interfeys (Marker Interface)

**Tavsif:** Marker interface hech qanday metod e'lon qilmaydi - uning yagona vazifasi sinfga tip darajasidagi metadata "yorliq" qo'yish. Runtime yoki framework `instanceof` tekshiruvi orqali shu yorliqni ko'rib, maxsus xatti-harakat qo'llaydi. Annotatsiyalardan avvalgi davrda metadata berishning asosiy usuli bo'lgan, hozir esa compile-time tip xavfsizligi kerak bo'lganda qiymatli.

**Spring'da qayerda uchraydi:** JDK'da `java.io.Serializable`, `Cloneable`, `RandomAccess` va `java.rmi.Remote`. Spring'da `Aware` interfeyslari semi-marker rolini o'ynaydi (`BeanNameAware`, `ApplicationContextAware`, `EnvironmentAware`), `InitializingBean`/`DisposableBean` lifecycle hook'lari, `Ordered` va `PriorityOrdered` (sorting uchun), Spring Data'dagi `Repository<T, ID>` - metodsiz marker bo'lib, scanning mexanizmi uni topadi; shuningdek `org.springframework.aop.SpringProxy` va `org.springframework.aop.framework.Advised` proxy'larni belgilash uchun. Spring Security'da `CredentialsContainer`, JPA validation'da `Default` guruh interfeyslari ham shu toifaga kiradi.

**Qo'llanish keyslari:**
- Domain event'larni `DomainEvent` marker bilan belgilab, generic publisher orqali yig'ish.
- Bean Validation guruhlarini interfeys sifatida e'lon qilish (`OnCreate`, `OnUpdate`) va `@Validated(OnCreate.class)` bilan ishlatish.
- Audit talab qiladigan entity'larni `Auditable` marker bilan ajratib, `BeanPostProcessor`da aniqlash.
- Cache'ga yozilmaydigan DTO'larni `NonCacheable` yorlig'i bilan generic cache qatlamidan chiqarish.
- Sealed interface bilan birga (Java 17+) permitted implementatsiyalarni cheklab, exhaustive `switch` pattern matching'ni ta'minlash.

**Ehtiyot bo'ling:** Zamonaviy Java'da ko'p hollarda annotatsiya (`@Retention(RUNTIME)`) yoki `sealed interface` yaxshiroq tanlov - marker interfeys meros ierarxiyasini "ifloslantiradi" va subclass'lar yorliqni xohlamasa ham oladi. `Serializable` misoli ko'rsatganidek, marker qo'yish yashirin kontrakt (serialVersionUID, security surface) yuklaydi, shuning uchun uni faqat tip darajasidagi tekshiruv haqiqatan kerak bo'lganda ishlating.

```java
// Marker interfeys: tur tizimi orqali belgi
public interface AuditedCommand {}               // metod yo'q, faqat belgi

public record CloseAccount(long accountId) implements AuditedCommand {}

@Component
class AuditingDispatcher {
    void dispatch(Object command) {
        if (command instanceof AuditedCommand) { /* audit yozuvi */ }
    }
}

// Zamonaviy alternativa: annotatsiya (meta-ma'lumot qo'shish mumkin)
@Retention(RetentionPolicy.RUNTIME)
@Target(ElementType.TYPE)
public @interface Audited { String category() default "default"; }
```

## 2.9 Modul (Module)

**Tavsif:** Bir-biriga bog'liq sinflar, interfeyslar va resurslarni yagona mantiqiy birlikka to'plab, uning faqat ozgina qismini tashqariga ochadi, qolganini yashiradi. Shu orqali kod bazasidagi bog'liqliklar yo'naltirilgan va nazoratli bo'ladi - modul ichidagi o'zgarish tashqariga sizib chiqmaydi. Strukturaviy pattern sifatida u obyektlar emas, balki butun kod birliklari darajasida kompozitsiya yaratadi. Ko'pincha "public API + internal implementation" ajratmasi ko'rinishida amalga oshiriladi.

**Spring'da qayerda uchraydi:** Java 17-25'dagi JPMS (`module-info.java`, `exports`/`requires`) va `java.util.ServiceLoader`; Spring Boot 3.x/4.x starter'lari (`spring-boot-starter-web` va uning `AutoConfiguration.imports` fayli) klassik modul chegarasi hisoblanadi. Spring Modulith (`spring-modulith`, `@ApplicationModule`, `@Modulithic`, `ApplicationModules.of(App.class).verify()`) bitta Spring Boot monolitida paket darajasidagi modul chegaralarini test vaqtida majburlaydi va `Documenter` bilan diagramma chiqaradi. Jackson'ning `com.fasterxml.jackson.databind.Module` (masalan `JavaTimeModule`, `Jackson2ObjectMapperBuilder.modules(...)`) ham xuddi shu patternning kutubxona ko'rinishi.

**Qo'llanish keyslari:**
- Monolitni `order`, `billing`, `inventory` kabi domen modullariga bo'lib, Spring Modulith `verify()` bilan noto'g'ri bog'liqlikni CI'da sindirish.
- Mikroservislarga ajratishdan oldin chegaralarni aniqlash va keyin modulni alohida deploy qilinadigan servisga chiqarish.
- Umumiy kutubxonani `api` va `impl` Gradle/Maven modullariga ajratib, iste'molchilarni implementatsiyaga bog'lanishdan to'sish.
- O'z Spring Boot auto-configuration starter'ingizni yozib, konfiguratsiyani bitta artifact sifatida tarqatish.
- `ObjectMapper`ga maxsus serializer'larni bitta Jackson `Module` sifatida ro'yxatdan o'tkazish.

**Ehtiyot bo'ling:** Modulni texnik qatlamlar (`controller`, `service`, `repository`) bo'yicha emas, domen bo'yicha ajratish kerak - aks holda har bir o'zgarish barcha modullarga tegadi. Spring Modulith event'lari bilan modullarni juda ko'p asinxron bog'lab tashlash kuzatuvchanlikni (observability) yo'qotadi, shuning uchun `@ApplicationModuleListener` va event publication registry'ni monitoring bilan birga joriy qiling.

```java
// Modul chegarasi: tashqariga faqat API paketi chiqadi
module payments.core {
    requires spring.context;
    exports com.example.payments.api;            // shartnoma
    // com.example.payments.internal eksport qilinmaydi
}

// Spring Modulith bilan bir xil g'oya, JPMS siz
@ApplicationModule(allowedDependencies = "shared")
package com.example.payments;
```

## 2.10 Yopiq sinf ma'lumotlari (Private Class Data)

**Tavsif:** Sinf holatini (state) uning xatti-harakatidan ajratib, ma'lumotlarni alohida, faqat o'qish uchun ochilgan tashuvchida saqlaydi va konstruktordan keyin o'zgartirishni butunlay to'sadi. Maqsad - ko'rinadigan atributlar sonini kamaytirish va kerak bo'lmagan `setter`'lar orqali yuzaga keladigan nomuvofiq holatni yo'q qilish. Natijada obyekt immutable bo'ladi, thread-safe bo'ladi va uni `HashMap` kaliti yoki cache qiymati sifatida xavfsiz ishlatish mumkin. Java'da bu bugun record'lar va `final` maydonlar bilan tabiiy ravishda beriladi.

**Spring'da qayerda uchraydi:** Java 17+ `record` va Spring Boot 3.x'dagi constructor binding (`@ConfigurationProperties` + `record`, `org.springframework.boot.context.properties.bind.ConstructorBinding`) - konfiguratsiya o'qilgandan keyin o'zgarmaydi. `org.springframework.http.HttpHeaders.readOnlyHttpHeaders(...)`, `ResponseEntity`, `org.springframework.data.domain.PageRequest`, `org.springframework.core.io.ClassPathResource` va Spring Security'dagi `UsernamePasswordAuthenticationToken` (`setAuthenticated(true)` ni rad etadi) - barchasi holatni yopib qo'yadi. `java.util.Collections.unmodifiableList(...)`, `List.copyOf(...)` va Lombok `@Value` ham shu yondashuvning amaliy vositalari.

**Qo'llanish keyslari:**
- `@ConfigurationProperties` ni `record` sifatida yozib, runtime'da konfiguratsiya tasodifan o'zgarishini oldini olish.
- DTO va API javob obyektlarini record qilib, controller'dan qaytgan ma'lumot keyin o'zgartirilmasligiga kafolat berish.
- Domen value object'lari (`Money`, `Email`, `IbanNumber`) ni invariant tekshiruvi konstruktorda bo'ladigan immutable sinf qilish.
- Cache (`@Cacheable`) ichida saqlanadigan qiymatlarni immutable qilib, boshqa chaqiruvchi ularni buzishini to'sish.
- Ko'p thread o'qiydigan umumiy sozlama snapshot'ini `volatile` immutable obyekt sifatida almashtirib turish.

**Ehtiyot bo'ling:** "Immutable" deb e'lon qilingan sinf ichida `List` yoki `Date` kabi mutable havolani to'g'ridan-to'g'ri qaytarish yopiqlikni buzadi - konstruktorda ham, getter'da ham defensive copy qiling (record bunga avtomatik kafolat bermaydi). JPA `@Entity` uchun esa Hibernate argumentsiz konstruktor va proxy talab qilgani uchun to'liq immutable record'ni entity qilib ishlatmang.

```java
// Private Class Data: qurilgandan keyin o'zgarmaydi
@ConfigurationProperties("psp")
public record PspProperties(
        @NotBlank String url,
        @DurationUnit(ChronoUnit.MILLIS) Duration timeout,
        @NotEmpty List<String> allowedCurrencies) {

    public PspProperties {
        // nusxa olinadi: tashqi ro'yxat keyin o'zgarsa ham bizga ta'sir qilmaydi
        allowedCurrencies = List.copyOf(allowedCurrencies);
    }
}
```

## 2.11 Kengaytirish obyekti (Extension Object)

**Tavsif:** Sinf ierarxiyasini o'zgartirmasdan obyektga runtime'da qo'shimcha interfeys va imkoniyat qo'shish imkonini beradi: iste'molchi obyektdan "sen shu rolni bajara olasanmi?" deb so'raydi va mavjud bo'lsa kengaytma obyektini oladi. Bu interfeys bo'rtib ketishini (fat interface) oldini oladi, chunki kamdan-kam kerak bo'ladigan imkoniyatlar asosiy abstraksiyaga kiritilmaydi. Plugin arxitekturalarining asosiy qurilish bloki hisoblanadi.

**Spring'da qayerda uchraydi:** JDBC'dagi `java.sql.Wrapper` (`isWrapperFor(...)`/`unwrap(...)`) va JPA'dagi `EntityManager.unwrap(Session.class)` to'g'ridan-to'g'ri shu pattern. Spring AOP introduction'lari - `org.springframework.aop.IntroductionInterceptor`, `DelegatingIntroductionInterceptor`, `@DeclareParents` - proxy'ga yangi interfeys qo'shadi, shuning uchun har qanday Spring proxy'ni `org.springframework.aop.framework.Advised`ga cast qilish mumkin. JUnit 5 Extension API (`org.junit.jupiter.api.extension.Extension`, `ParameterResolver`, `BeforeEachCallback`) va uning Spring'dagi implementatsiyasi `org.springframework.test.context.junit.jupiter.SpringExtension`, shuningdek `ApplicationContextInitializer` va `@ServletComponentScan` kabi kengaytma nuqtalari ham shu mantiqda ishlaydi.

**Qo'llanish keyslari:**
- Hibernate'ning Spring Data orqali berilmagan imkoniyatiga `entityManager.unwrap(Session.class)` bilan kirish.
- `HikariDataSource` statistikasiga `dataSource.unwrap(HikariDataSource.class)` orqali yetib borish.
- Spring AOP introduction bilan mavjud bean'larga `Auditable` yoki `Monitorable` interfeysini kod tegmasdan qo'shish.
- Plugin tizimida bir plugin "export qila oladi", boshqasi "import qila oladi" degan ixtiyoriy imkoniyatlarni e'lon qilishi.
- Test infratuzilmasida JUnit 5 extension'lari orqali Testcontainers yoki soat (clock) boshqaruvini qo'shish.

**Ehtiyot bo'ling:** Har bir `unwrap`/`instanceof` tekshiruvi abstraksiyadan chiqish (leaky abstraction) hisoblanadi - kod aniq implementatsiyaga bog'lanadi va provider almashtirilganda sinadi, shuning uchun uni bitta adapter sinf ichida saqlang. Kengaytmani oddiy ixtiyoriy bog'liqlik o'rniga ishlatmang: `ObjectProvider<T>` yoki `Optional` bilan hal bo'ladigan holatda bu pattern ortiqcha murakkablik keltiradi.

```java
// Extension Object: asosiy shartnoma toza qoladi, qo'shimcha imkoniyat so'rab olinadi
public interface Exportable {
    <T> Optional<T> as(Class<T> extension);      // kengaytirishni so'rash
}

@Service
class OrderDocument implements Exportable {
    @Override
    public <T> Optional<T> as(Class<T> ext) {
        if (ext == PdfExport.class) return Optional.of(ext.cast(new PdfExport(this)));
        return Optional.empty();
    }
}

// JDK va JPA dagi tayyor misollar
Session session = entityManager.unwrap(Session.class);
if (dataSource.isWrapperFor(HikariDataSource.class)) { /* ... */ }
```

## 2.12 Egizak (Twin)

**Tavsif:** Java'da ko'p irsiylash (multiple inheritance) yo'q bo'lgani uchun ikki alohida sinf ikki xil bazadan meros oladi va bir-biriga havola orqali bitta mantiqiy obyekt sifatida ishlaydi. Har bir "egizak" o'z ierarxiyasida to'laqonli ishtirok etadi, lekin holatni sherigi bilan bo'lishadi. Mössenböck tomonidan taklif qilingan bu yechim GoF ro'yxatiga kirmaydi, ammo framework bazaviy sinflari majburlagan holatlarda hanuz foydali. Bugun ko'p hollarda interfeys + kompozitsiya uni almashtiradi.

**Spring'da qayerda uchraydi:** Spring'da maxsus qo'llab-quvvatlash yo'q; u ikki abstract bazaviy sinfdan meros olish kerak bo'lganda qo'lda yoziladi - masalan `org.springframework.scheduling.concurrent.CustomizableThreadFactory` yoki `java.util.TimerTask` dan meros olgan obyekt bir vaqtda domen bazasiga ham tegishli bo'lishi kerak bo'lsa. Zamonaviy Spring'da esa to'g'ri yo'l - `Runnable`/`Callable` ni lambda bilan berish, `org.springframework.scheduling.annotation.@Async` va `AbstractAuthenticationProcessingFilter`, `OncePerRequestFilter` kabi bazaviy sinflarga delegatsiya orqali kompozitsiya qilish.

```java
class JobTask extends TimerTask {            // birinchi egizak
    final JobEntity twin;
    JobTask(JobEntity twin) { this.twin = twin; }
    public void run() { twin.execute(); }
}
class JobEntity extends AbstractAuditable {  // ikkinchi egizak
    JobTask twin = new JobTask(this);
    void execute() { /* domen logikasi */ }
}
```

**Qo'llanish keyslari:**
- Legacy framework'ning `final` yoki abstract bazaviy sinfidan meros olish shart bo'lgan, lekin domen bazaviy sinfi ham kerak bo'lgan kod.
- O'yin yoki simulyatsiya obyektini bir vaqtning o'zida grafik va fizika ierarxiyalarida qatnashtirish.
- Eski JPA `AbstractAuditable` ierarxiyasini saqlab, obyektga alohida thread/task xulqini qo'shish.
- Uchinchi tomon kutubxonasi `extends`ni talab qilgan integratsiya qatlamini domen modelidan ajratish.

**Ehtiyot bo'ling:** Ikki egizak o'zaro qattiq bog'langani uchun holat sinxronizatsiyasi va `equals`/`hashCode` semantikasi tez buziladi, shuning uchun uni faqat haqiqatan ikki `extends` majburiy bo'lganda ishlatish kerak. Yangi kodda avval interfeys + default metod yoki oddiy kompozitsiyani sinab ko'ring - Twin deyarli har doim dizayn muammosining belgisi.

## 2.13 Delegatsiya (Delegation)

**Tavsif:** Obyekt so'rovni o'zi bajarmasdan ichidagi boshqa obyektga uzatadi va kerak bo'lsa natijani boyitadi - irsiylash o'rniga kompozitsiyani tanlash usuli. Chaqiruvchi uchun tashqi obyekt yagona kirish nuqtasi bo'lib qoladi, ichkaridagi haqiqiy bajaruvchi esa runtime'da almashtirilishi mumkin. Bu Decorator, Proxy va Adapter patternlarining umumiy mexanizmi hisoblanadi. Qattiq ierarxiyani moslashuvchan ish vaqti bog'lanishiga aylantiradi.

**Spring'da qayerda uchraydi:** Spring'da nomlarning o'zi ham shunga ishora qiladi: `org.springframework.web.filter.DelegatingFilterProxy` (servlet filter'ni Spring bean'iga uzatadi), `org.springframework.security.web.FilterChainProxy`, `DelegatingPasswordEncoder` (`PasswordEncoderFactories.createDelegatingPasswordEncoder()`, `{bcrypt}` prefiksi bilan), `DelegatingSecurityContextExecutor` / `DelegatingSecurityContextRunnable`, `org.springframework.jdbc.datasource.DelegatingDataSource`, `DelegatingWebMvcConfiguration`, `DelegatingApplicationListener` va `DelegatingIntroductionInterceptor`. Spring'ning butun AOP infratuzilmasi (`JdkDynamicAopProxy`, `MethodInterceptor` zanjiri) ham delegatsiyaga asoslangan; Kotlin'da esa `by` kalit so'zi bilan tilga qurilgan.

**Qo'llanish keyslari:**
- `web.xml` yoki `ServletRegistrationBean` orqali ro'yxatdan o'tgan filter'ni Spring context'idagi bean'ga `DelegatingFilterProxy` bilan bog'lash.
- Parol hash algoritmini migratsiya qilish: eski `{noop}`/`{md5}` hash'larni `DelegatingPasswordEncoder` bilan o'qib, yangilarini `{bcrypt}` bilan yozish.
- `@Async` yoki `ExecutorService` ichida `SecurityContext`ni uzatish uchun `DelegatingSecurityContextExecutorService` ishlatish.
- Bir nechta `DataSource` ustidan routing qiluvchi `AbstractRoutingDataSource` bilan multi-tenancy qurish.
- Kutubxona interfeysini meros olmasdan o'rab, faqat bir-ikki metod xatti-harakatini o'zgartirish.

**Ehtiyot bo'ling:** Delegatsiya zanjiri uzayib ketsa stack trace o'qilmas bo'ladi va har bir qatlam tashlanadigan exception'ni yashirib qo'yishi mumkin. Shuningdek, Spring'da bean o'z metodini `this` orqali chaqirsa proxy chetlab o'tiladi - `@Transactional` yoki `@Cacheable` ishlamaydi, bunda `AopContext.currentProxy()` yoki alohida bean'ga ajratish kerak.

```java
// Delegatsiya: meros o'rniga ichki obyektga uzatish
@Component
public class MeteredPaymentGateway implements PaymentGateway {
    private final PaymentGateway delegate;       // merossiz kengaytirish
    private final Timer timer;

    public MeteredPaymentGateway(@Qualifier("psp") PaymentGateway delegate,
                                 MeterRegistry registry) {
        this.delegate = delegate;
        this.timer = registry.timer("payment.gateway");
    }

    @Override
    public Receipt charge(Payment p) {
        return timer.record(() -> delegate.charge(p));   // ish egasiga uzatiladi
    }
}
```

## 2.14 O'rovchi (Wrapper)

**Tavsif:** Mavjud obyektni bir xil yoki yaqin interfeysli yangi obyekt ichiga joylab, chaqiruvlarni ushlab turish, o'zgartirish yoki qo'shimcha xulq berish imkonini beradi. "Wrapper" aniq GoF pattern emas, balki Decorator, Adapter va Proxy uchun umumiy atama bo'lib, asosiy g'oya - original kodni o'zgartirmasdan uning atrofida qatlam yaratish. Ko'pincha bitta metodni almashtirish uchun butun ierarxiyani qayta yozishdan qutqaradi. Shu bilan birga yangi, cheklangan yoki xavfsizroq ko'rinish (read-only view) berish uchun ishlatiladi.

**Spring'da qayerda uchraydi:** `org.springframework.beans.BeanWrapper` / `BeanWrapperImpl` (POJO property'lariga reflektiv kirish), `org.springframework.web.util.ContentCachingRequestWrapper` va `ContentCachingResponseWrapper` (log yoki audit uchun body'ni ikki marta o'qish), `jakarta.servlet.http.HttpServletRequestWrapper`/`HttpServletResponseWrapper`, `org.springframework.jdbc.datasource.TransactionAwareDataSourceProxy` va `LazyConnectionDataSourceProxy`. Platforma darajasida `java.util.Collections.unmodifiableMap(...)`, `List.copyOf(...)`, `java.io.BufferedReader`, Micrometer'ning `TimedExecutorService` va primitiv wrapper sinflari (`Integer`, `Long`) ham shu toifaga kiradi.

**Qo'llanish keyslari:**
- HTTP so'rov body'sini `ContentCachingRequestWrapper` bilan filter'da log qilib, controller uchun uni buzmaslik.
- `DataSource`ni `TransactionAwareDataSourceProxy` bilan o'rab, legacy JDBC kodni Spring tranzaksiyalariga qo'shish.
- `ExecutorService`ni o'rab, har bir topshiriqqa metrika, MDC yoki tracing context qo'shish.
- Domen kolleksiyalarini `Collections.unmodifiable*` orqali read-only ko'rinishda tashqariga berish.
- Uchinchi tomon SDK klientini o'rab, retry, timeout va exception translation'ni bitta joyda markazlashtirish.

**Ehtiyot bo'ling:** Wrapper original obyektning barcha metodlarini to'g'ri uzatmasa (masalan `equals`, `hashCode`, `toString` yoki yangi interfeys metodlari) nozik buglar paydo bo'ladi - iloji bo'lsa `Delegating*` bazaviy sinflaridan meros oling. `ContentCachingRequestWrapper` butun body'ni xotirada saqlagani uchun katta yoki file upload so'rovlarida xotira va latency muammosi tug'diradi, shuning uchun uni o'lcham va URL bo'yicha cheklang.

```java
// Wrapper: body'ni ikki marta o'qish uchun so'rovni o'rash
@Component
public class RequestLoggingFilter extends OncePerRequestFilter {

    @Override
    protected void doFilterInternal(HttpServletRequest req, HttpServletResponse res,
                                    FilterChain chain) throws ServletException, IOException {
        ContentCachingRequestWrapper wrapped = new ContentCachingRequestWrapper(req);
        chain.doFilter(wrapped, res);            // controller body'ni o'qiydi
        // zanjirdan keyin biz ham o'qiymiz: wrapper keshlagan
        log.debug("body={}", new String(wrapped.getContentAsByteArray(), UTF_8));
    }
}
```

## 2.15 Mixin / Trait default metodlar orqali (Mixin / Trait via default methods)

**Tavsif:** Interfeysga tayyor implementatsiya (default metod) joylab, bir nechta mustaqil sinfga bazaviy sinfdan meros olmasdan umumiy xulq "aralashtiriladi". Bu gorizontal kodni qayta ishlatish usuli: sinf bir vaqtda bir nechta trait'ni implement qilib, har biridan tayyor metodlar oladi. Java'da holat (state) interfeysda saqlanmagani uchun mixin faqat xatti-harakat darajasida bo'ladi va holat kerak bo'lsa abstract getter orqali so'raladi. Shu sababli u yupqa, yon ta'sirsiz yordamchi mantiq uchun eng mos keladi.

**Spring'da qayerda uchraydi:** Spring'ning ko'plab kengaytma interfeyslari to'liq default metodlardan iborat, shuning uchun ularni "opt-in trait" sifatida ishlatish mumkin: `org.springframework.web.servlet.config.annotation.WebMvcConfigurer`, `org.springframework.web.reactive.config.WebFluxConfigurer`, `org.springframework.web.servlet.HandlerInterceptor`, `org.springframework.beans.factory.config.BeanPostProcessor` va `org.springframework.context.SmartLifecycle`. Spring Data'da custom repository fragment interfeyslari default metodlar bilan bir nechta repository'ga umumiy xulq qo'shadi. Jackson'ning mix-in mexanizmi (`ObjectMapper.addMixIn(Class, Class)`, Spring Boot'da `Jackson2ObjectMapperBuilder.mixIns(...)`) esa o'zgartirilmaydigan sinflarga annotatsiyalarni tashqaridan aralashtirish uchun ishlatiladi.

```java
public interface Auditable {
    Instant getCreatedAt();                       // holat sinfdan keladi
    default boolean isStale(Duration ttl) {        // trait xulqi
        return getCreatedAt().plus(ttl).isBefore(Instant.now());
    }
}
```

**Qo'llanish keyslari:**
- `WebMvcConfigurer` ni implement qilib faqat `addCorsMappings` yoki `addInterceptors` ni override qilish.
- Spring Data fragment interfeysiga default metod qo'yib, bir nechta repository uchun umumiy query helper'ini ulash.
- Domen obyektlariga `Auditable`, `SoftDeletable`, `Versioned` kabi yupqa trait'larni bazaviy entity sinfisiz qo'shish.
- `ObjectMapper` mix-in bilan o'zgartirish imkoni bo'lmagan tashqi DTO'ga `@JsonIgnore` qo'shish.
- `Comparator` default metodlari (`thenComparing`, `reversed`) orqali saralash qoidalarini kompozitsiya qilish.

**Ehtiyot bo'ling:** Ikki interfeys bir xil signatura bilan default metod bersa sinf kompilyatsiya qilinmaydi va `Interface.super.method()` bilan aniq hal qilish kerak bo'ladi; sinf metodi esa har doim default metoddan ustun turadi (class wins). Mixin'ga holat yoki bog'liqlik (bean inject) kiritishga urinmang - buning uchun oddiy kompozitsiya yoki alohida bean to'g'ri yechim, aks holda interfeys yashirin `static` holatga aylanib thread-safety buziladi.

## 2.16 Qatlam ustki turi (Layer Supertype)

**Tavsif:** Bitta arxitektura qatlamidagi barcha obyektlar uchun umumiy xatti-harakatni saqlovchi mavhum bazaviy tur (abstract class yoki interface) ajratiladi. Identifikator, audit maydonlari, `equals`/`hashCode`, xato javobini shakllantirish yoki umumiy log/metrika kodi har bir sinfda takrorlanmaydi - u bitta joyda yashaydi. Natijada qatlamning "shartnomasi" bir xil bo'ladi va yangi sinf qo'shish arzonlashadi. Bu pattern faqat bir qatlam ichida qo'llanadi: entity'lar uchun bir supertype, controller'lar uchun boshqa, test'lar uchun yana boshqa.

**Spring'da qayerda uchraydi:** Spring'ning o'zi bu patternni keng ishlatadi. Persistence qatlamida JPA `@MappedSuperclass` bilan `BaseEntity` yoziladi, Spring Data JPA esa tayyor `org.springframework.data.jpa.domain.AbstractPersistable` va `AbstractAuditable` sinflarini beradi; `@EnableJpaAuditing` bilan birga `@CreatedDate`, `@LastModifiedDate`, `@CreatedBy` maydonlari bazaviy sinfda to'ldiriladi. Domain qatlamida `org.springframework.data.domain.AbstractAggregateRoot` `registerEvent(...)` orqali domain event'larni yig'adi va repository `save()` chaqirilganda ularni publish qiladi. Web qatlamida `ResponseEntityExceptionHandler` (`org.springframework.web.servlet.mvc.method.annotation`) `@RestControllerAdvice` bilan global xato supertype'i bo'ladi, filter'lar uchun `OncePerRequestFilter` va `AbstractAuthenticationProcessingFilter` (Spring Security 6.x), konverterlar uchun `AbstractHttpMessageConverter`, DataSource uchun `AbstractRoutingDataSource` xizmat qiladi. Spring Data'da butun repository qatlamining supertype'i - `SimpleJpaRepository`, uni `@EnableJpaRepositories(repositoryBaseClass = MyBaseRepositoryImpl.class)` bilan o'zingizning sinfingizga almashtirish mumkin. Test qatlamida ko'pincha abstract `@SpringBootTest` sinfi Testcontainers `@ServiceConnection` (Spring Boot 3.1+) bilan barcha integration testlar uchun bazaviy tur sifatida ishlatiladi. Java 17-25'da `record` va `sealed interface` ba'zi hollarda abstract class o'rnini bosadi, lekin JPA entity'lar uchun `@MappedSuperclass` yagona ishlaydigan variant bo'lib qolmoqda.

```java
@MappedSuperclass
@EntityListeners(AuditingEntityListener.class)
public abstract class BaseEntity {
    @Id @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    @CreatedDate private Instant createdAt;
    @LastModifiedDate private Instant updatedAt;
    @Version private long version;
    public Long getId() { return id; }
}
```

**Qo'llanish keyslari:**
- Barcha entity'lar uchun `id`, `createdAt`, `updatedAt`, `version` va optimistic locking'ni bitta `@MappedSuperclass` sinfda markazlashtirish.
- `@RestControllerAdvice` + `ResponseEntityExceptionHandler` asosida butun API uchun yagona RFC 9457 `ProblemDetail` xato formatini ta'minlash.
- Multi-tenant ilovada `AbstractRoutingDataSource` subclass'i orqali tenant bo'yicha DataSource tanlash.
- Abstract integration-test bazaviy sinfi: Testcontainers konteynerlari, `@Transactional` rollback va umumiy test ma'lumotlari bir joyda.
- `AbstractAggregateRoot` orqali aggregate'larda domain event'larni to'plab, `save()` paytida avtomatik publish qilish.

**Ehtiyot bo'ling:** Supertype "hamma narsa uchun axlat qutisi"ga aylanib, chuqur inheritance daraxti va fragile base class muammosini keltirib chiqarishi mumkin - bitta bazaviy sinfni o'zgartirganda yuzlab sinf buziladi; biznes logikani emas, faqat haqiqatan umumiy infratuzilma kodini unga joylashtiring va imkon bo'lsa composition yoki interface default metodini afzal ko'ring. JPA'da `AbstractPersistable` kabi sinflarning `equals`/`hashCode` implementatsiyasi generated `id` bilan ishlaganda (hali saqlanmagan obyektlar, `HashSet` ichidagi lazy collection'lar) kutilmagan xatti-harakat beradi, shuning uchun business key bo'yicha tenglikni o'zingiz yozib chiqish ko'pincha xavfsizroq.

## 2.17 Ajratilgan interfeys (Separated Interface)

**Tavsif:** Interfeys uni ishlatuvchi mijoz tomonidagi modul/paketda e'lon qilinadi, implementatsiya esa butunlay boshqa modulda joylashadi. Shu tariqa compile-time bog'liqlik yo'nalishi teskari buriladi: domain kodi infratuzilmaga emas, infratuzilma domainga bog'lanadi (Dependency Inversion). Bu hexagonal/ports-and-adapters arxitekturasining asosi bo'lib, implementatsiyani (JPA, Kafka, HTTP mijoz, mock) domain kodini qayta kompilyatsiya qilmasdan almashtirishga imkon beradi. Runtime'da to'g'ri implementatsiyani DI container ulab beradi.

**Spring'da qayerda uchraydi:** Spring'ning butun DI modeli shu patternga qurilgan: `@Autowired` qiladigan joyda interfeys turini e'lon qilasiz, `@Component`/`@Service` bilan belgilangan implementatsiya boshqa paketda yashaydi, kerak bo'lsa `@Primary`, `@Qualifier` yoki `@ConditionalOnMissingBean` bilan tanlanadi. Eng sof misol - Spring Data: siz `UserRepository extends JpaRepository<User, Long>` interfeysini domain modulida yozasiz, implementatsiyani esa `JpaRepositoryFactoryBean` runtime'da proxy sifatida generatsiya qiladi; interfeysni `MongoRepository` yoki `CrudRepository`ga almashtirib, data store'ni o'zgartirish mumkin. Deklarativ HTTP mijozlar ham xuddi shunday: Spring Framework 6.1+ `@HttpExchange`/`@GetExchange` bilan belgilangan interfeysni `HttpServiceProxyFactory` + `RestClient`/`WebClient` orqali implement qiladi (Spring Boot 4.0'da `@ImportHttpServices` bu registratsiyani avtomatlashtiradi), Spring Cloud OpenFeign'da esa `@FeignClient` shu rolni bajaradi; RSocket uchun `@RSocketExchange` mavjud. Platform darajasida `PlatformTransactionManager`, `CacheManager`, `MessageSource`, `ApplicationEventPublisher`, `TaskExecutor` - hammasi ajratilgan interfeyslar, implementatsiyalari esa alohida modullarda (`JpaTransactionManager`, `CaffeineCacheManager` va h.k.). Modul chegaralarini majburlash uchun Spring Modulith `@NamedInterface` va `ApplicationModules.verify()` testlari, Java Platform Module System'da `module-info.java` `exports`, Spring Boot auto-configuration'da esa `META-INF/spring/org.springframework.boot.autoconfigure.AutoConfiguration.imports` fayli ishlatiladi; klassik Java SPI varianti - `java.util.ServiceLoader`.

**Qo'llanish keyslari:**
- Hexagonal arxitekturada `PaymentGateway` yoki `OrderRepository` port interfeysini domain modulida saqlab, Stripe/JPA adapterlarini infrastructure modulida yozish.
- Domain modulini Spring'ga bog'liq bo'lmagan holda ushlab turish, shunda unit testlarda ApplicationContext ko'tarmasdan oddiy fake implementatsiya berish mumkin.
- Spring Modulith modullari orasidagi aloqa uchun faqat `@NamedInterface` bilan ochilgan interfeyslarni e'lon qilib, ichki sinflarni yopiq saqlash.
- Tashqi servis bilan integratsiyani `@HttpExchange` interfeysi orqali tasvirlash va testda uni WireMock yoki in-memory implementatsiya bilan almashtirish.
- Kutubxona yozganda mijozga faqat interfeys va auto-configuration berib, implementatsiyani keyinchalik buzmasdan o'zgartirish imkonini saqlash.

**Ehtiyot bo'ling:** Har bir sinf uchun avtomatik ravishda bitta implementatsiyali interfeys yaratish ("`FooService` + `FooServiceImpl`") hech qanday foyda bermaydi, faqat navigatsiyani qiyinlashtiradi - interfeysni haqiqatan bir nechta implementatsiya, modul chegarasi yoki testda almashtirish ehtiyoji bo'lganda ajratish kerak. Interfeys imzosiga infratuzilma tiplari (JPA `Entity`, `ResultSet`, Kafka `ConsumerRecord`) sizib kirsa, bog'liqlik baribir teskari bo'lmaydi va pattern faqat qog'ozda qoladi.

```java
// Separated Interface: shartnoma domen paketida, implementatsiya infratuzilmada
// com/example/orders/domain/ExchangeRates.java
public interface ExchangeRates {                 // domen o'ziga keragini e'lon qiladi
    BigDecimal rate(Currency from, Currency to);
}

// com/example/orders/infra/CbuExchangeRates.java
@Component
class CbuExchangeRates implements ExchangeRates {
    private final RestClient client;
    CbuExchangeRates(RestClient client) { this.client = client; }

    @Override
    public BigDecimal rate(Currency from, Currency to) {
        return client.get().uri("/rates/{f}/{t}", from, to)
                     .retrieve().body(BigDecimal.class);
    }
}
// Bog'liqlik yo'nalishi: infra -> domen. Domen RestClient ni bilmaydi.
```

## 2.18 Amalda qo'llash

- [ ] Tashqi kutubxona tiplari domen paketiga kirib kelgan joylarni qidiring va har biri uchun Adapter chegarasini belgilang.
- [ ] `@Transactional`, `@Cacheable` va `@Async` annotatsiyasi bor metodlarning `public` va tashqaridan chaqirilayotganini tekshiring - self-invocation proxy'ni chetlab o'tadi.
- [ ] `final` sinf yoki `final` metodga proxy qo'llanmoqchi bo'lgan joylarni toping; CGLIB ularni proxy qila olmaydi.
- [ ] Dekorator zanjirlarini sanab chiqing va har bir zanjirning tartibi `@Order` bilan aniq belgilanganini tasdiqlang.
- [ ] Faqat bitta implementatsiyasi bor interfeyslarni ro'yxatga oling va ularning qanchasi haqiqatan chegara ekanini qaror qiling.
- [ ] Fasad deb nomlangan sinflarni tekshiring: ular soddalashtiryaptimi yoki shunchaki chaqiruvlarni uzatyaptimi.
- [ ] Ko'p nusxada yaratilgan o'zgarmas qiymat obyektlarini (valyuta, mintaqa, status) toping va ularni Flyweight sifatida keshlash foydasini o'lchang.
- [ ] Marker interfeyslarni annotatsiyaga almashtirish mumkinmi degan savolni har biri uchun hal qiling.

---

[&larr; 1. Yaratuvchi patternlar](01-yaratuvchi-patternlar.md) · [Mundarija](README.md) · [3. Xulq-atvor patternlari &rarr;](03-xulq-atvor-patternlari.md)
