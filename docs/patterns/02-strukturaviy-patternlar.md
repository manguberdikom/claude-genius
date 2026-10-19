<!-- doc: patterns | chapter: 2 | part:  -->

[Barcha hujjatlar](../../README.md) / [Dizayn patternlar](README.md)

> Holat: tekshirilgan (2026-10-19). Manbalar bob oxirida.

# 2. Strukturaviy patternlar (Structural Patterns)

<details>
<summary>Bu bobdagi 23 bo'lim</summary>

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
- [2.18 Obyekt interfeysini spetsifikatsiyalash (Specifying Object Interfaces)](#218-obyekt-interfeysini-spetsifikatsiyalash-specifying-object-interfaces)
- [2.19 Sinf merosi va interfeys merosi (Class versus Interface Inheritance)](#219-sinf-merosi-va-interfeys-merosi-class-versus-interface-inheritance)
- [2.20 Qayta ishlatish mexanizmlari: white-box, black-box va parametrlangan turlar (Putting Reuse Mechanisms to Work)](#220-qayta-ishlatish-mexanizmlari-white-box-black-box-va-parametrlangan-turlar-putting-reuse-mechanisms-to-work)
- [2.21 Ish vaqtidagi va kompilyatsiya vaqtidagi struktura (Run-Time and Compile-Time Structures)](#221-ish-vaqtidagi-va-kompilyatsiya-vaqtidagi-struktura-run-time-and-compile-time-structures)
- [2.22 Kompozitni qurish qarorlari (Implementing Composite)](#222-kompozitni-qurish-qarorlari-implementing-composite)
- [2.23 Amalda qo'llash](#223-amalda-qollash)

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

**Qurish qarorlari:** Ikki variant orasidagi tanlov murosa bilan keladi, shuning uchun uni oldin hal qilish kerak. Sinf adapteri (meros) konkret Adaptee'ga bog'lanadi va uning subclass'larini adaptatsiya qilmaydi, lekin Adaptee xulqini qayta yozishga ruxsat beradi. Obyekt adapteri (kompozitsiya) teskari: bitta adapter Adaptee va uning barcha subclass'lari bilan ishlaydi, lekin xulqni qayta yozish uchun avval Adaptee'dan voris olish kerak bo'ladi. ESLATMA: Java'da bitta sinfdan meros olish mumkin bo'lgani uchun obyekt adapteri default tanlov, sinf adapteri esa interfeysni implement qilib default metodlarni qayta yozish ko'rinishida qoladi.

Ikkinchi qaror adaptatsiya yuzasining kattaligiga tegishli: adaptee'dan kerak bo'lgan eng kichik amallar to'plamini, ya'ni tor interfeysni tanlang. Ikki-uch metodli interfeysni adaptatsiya qilish o'nlab metodlini adaptatsiya qilishdan beqiyos oson, va tor interfeys adapterni test qilishni ham arzonlashtiradi (qarang: [26-bo'lim](26-dizayn-printsiplari-solid-grasp-va-umumiy.md#264-interfeys-ajratish-printsipi-interface-segregation-principle), Interfeys ajratish printsipi). Shu yerdan uchinchi qaror chiqadi: adaptatsiyani sinfning o'ziga qurib, boshqa sinflarga "mening interfeysimni implement qil" talabini qo'ymaslik mumkin - sinf adaptatsiya nuqtasini parametr sifatida qabul qiladi va kutilmagan interfeyslarga ega tizimlarga ulanadi. ESLATMA: Java'da bu `Function`, `Supplier` yoki metod havolasini parametr qilib olish bilan yoziladi, alohida adapter sinfi kerak bo'lmaydi. Oxirgi tafsilot shaffoflikka tegishli: adaptatsiya qilingan obyekt endi Adaptee interfeysiga mos kelmaydi, demak adapter hamma klient uchun shaffof emas; ikki klient uni ikki xil ko'rishi kerak bo'lsa adapter ikkala interfeysni implement qiladi.

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

**Qurish qarorlari:** Birinchi savol yuqoridagi YAGNI ogohlantirishi bilan to'qnashadi: implementatsiya bitta bo'lsa ham ajratish kerakmi. GoF "ha" deydi, sababi implementatsiya o'zgarganda klient qayta kompilyatsiya qilinmaydi, faqat qayta linklanadi. Ikki javob ham to'g'ri, ajratuvchi shart esa iste'molchini kim qayta qurishida: iste'molchini siz qayta kompilyatsiya qilasizmi. Alohida deploy qilinadigan va boshqa jamoalar bog'lanadigan kutubxonada ajratish haqli - bu Java'da binar moslik masalasi, chunki abstraksiya va implementatsiya bitta sinfda bo'lsa implementatsiyadagi har o'zgarish iste'molchining artefaktini qayta qurishni talab qiladi. Bitta ilova bitta build ichida, hamma modul birga kompilyatsiya qilinadigan joyda esa yuqoridagi YAGNI amal qiladi va ikkinchi implementatsiya paydo bo'lganda ajratish arzonroq tushadi.

Ikkinchi qaror: Implementor obyektini kim, qachon va qayerda yaratadi. Uch yo'l bor. Abstraction konstruktorida parametrga qarab tanlash eng oddiy, lekin Abstraction konkret implementatsiya sinflarini biladi. Default bilan boshlab keyin ishlatishga qarab almashtirish (kolleksiya o'sganda bir tuzilmadan boshqasiga o'tish) moslashuvchan, lekin almashtirish momentini kodda ushlab turish kerak. Qarorni fabrikaga topshirish esa Abstraction'ni Implementor sinflaridan butunlay uzadi va kengaytirishni konfiguratsiyaga chiqaradi. ESLATMA: Spring'da uchinchi yo'l standart - implementatsiya `@ConditionalOnProperty` yoki `@Profile` bilan tanlanadi, kerak bo'lsa `ObjectProvider` orqali kech olinadi, shuning uchun abstraksiya ichida tanlov kodi qolmaydi.

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

**Ehtiyot bo'ling:** Uzun decorator zanjiri stack trace'ni o'qishni qiyinlashtiradi va har bir qatlam latency qo'shadi - zanjir tartibi (masalan, transaction decorator cache'dan oldinmi yoki keyinmi) natijaga ta'sir qiladi. Decorator ichida `this` orqali o'z metodini chaqirish wrapper'ni chetlab o'tadi; Spring'da ham self-invocation proxy'ni aylanib o'tib, `@Transactional` yoki `@Cacheable` ishlamay qolishiga sabab bo'ladi. Shu muammoning umumiy shakli o'rovchi sinflarni callback framework'ida yaroqsiz qiladi: o'ralgan obyekt o'rovchini bilmaydi va callback'ni ro'yxatdan o'tkazganda `this` ni, ya'ni o'zini uzatadi, shuning uchun qaytib kelgan chaqiruv o'rovchini butunlay chetlab o'tadi. Bu SELF muammosi deb ataladi va o'rash orqali qo'shilgan xulq (retry, audit, metrika) callback yo'lida yo'qoladi.

**Qurish qarorlari:** Abstrakt Decorator sinfi har doim kerak emas: faqat bitta mas'uliyat qo'shilsa, uzatish mas'uliyatini to'g'ridan-to'g'ri konkret dekoratorga joylash kifoya va bu mavjud ierarxiya bilan ishlaganda ko'pincha shunday bo'ladi. Abstrakt dekorator ikki yoki undan ko'p dekorator paydo bo'lgandan keyin, uzatish kodining takrorlanishini yo'qotish uchun ochiladi. Ikkinchi qaror umumiy Component sinfiga tegishli va uni buzish qimmat tushadi: Component interfeysni belgilashi kerak, ma'lumot saqlashi emas. Og'ir Component dekoratorlarni ham og'ir qiladi, chunki har o'rov qatlami shu ma'lumotni qayta oladi, va ko'p sonli dekorator bilan ishlash imkonsiz bo'lib qoladi; ma'lumot saqlash kerak bo'lsa u konkret sinfga tushadi.

Uchinchi qaror Decorator bilan Strategy orasidagi tanlov: Decorator obyektning terisini, Strategy esa ichini o'zgartiradi. Component og'ir bo'lsa uni o'rash qimmat tushadi va Strategy afzal; Strategy o'zining maxsus interfeysiga ega bo'la oladi, dekorator esa komponent interfeysiga bog'langan. Teskari tomoni bor: Strategy ishlatish uchun komponent o'z kengaytirishlarini bilishi va ularga yuza ochishi kerak, dekorator esa komponentdan hech narsa talab qilmaydi (qarang: [Strategiya](03-xulq-atvor-patternlari.md#39-strategiya-strategy)). Oxirgi va amalda eng ko'p tishlaydigan oqibat: dekorator va u o'ragan komponent bir xil obyekt EMAS, shuning uchun dekorator ishlatilgan joyda obyekt identifikatoriga tayanmaslik kerak (qarang: [`==` emas, `equals`](../clean-code/21-satr-matn-va-regex.md#211--emas-equals-intern-va-literal-pool)). ESLATMA: Spring'da bu aniq ko'rinadi - AOP proxy'langan bean `==` bilan o'z target'iga teng emas, shuning uchun bean'larni `==` bilan solishtirish yoki `IdentityHashMap` da kalit qilish proxy yoqilganda jim sinadi.

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

**Qurish qarorlari:** Klient bog'lanishini yana bir pog'ona kamaytirish mumkin: fasadni abstrakt sinf yoki interfeys qilib, quyi tizimning har implementatsiyasi uchun alohida konkret fasad yozish - shunda klient quyi tizimning qaysi variantda ishlayotganini ham bilmaydi. Bu qimmat yechim, shuning uchun arzonroq muqobil ko'pincha yetadi: bitta fasad obyektini turli quyi tizim obyektlari bilan sozlash, ya'ni implementatsiyani konstruktorga berish. ESLATMA: Spring'da arzon variant default - fasad bean'i bitta, uning bog'liqliklari esa profil yoki property bilan almashtiriladi; abstrakt fasad faqat chaqiruv shakli ham o'zgarganda kerak bo'ladi.

Ikkinchi qaror arxitektura darajasida ishlaydi va fasadning kam eslanadigan vazifasi shu: fasad quyi tizimlarni qatlamlashga va aylanma bog'liqlikni yo'q qilishga xizmat qiladi. Bir-biriga bog'liq ikki quyi tizim faqat o'z fasadlari orqali gaplashsa, ularning ichki sinflari orasida havola qolmaydi va bog'liqlik grafigi yo'naltirilgan bo'lib turadi. Modulli monolitda bu qoida modul chegarasini belgilashning eng arzon vositasi: har modul bitta ochiq fasad beradi, qolgani `package-private` qoladi (qarang: [Modulli monolit](12-arxitektura-uslublari.md#126-modulli-monolit-modular-monolith--spring-modulith)). Fasadni orkestratordan ajratadigan chiziq esa alohida yozilgan (qarang: [Orkestrator vs fasad](08-biznes-logika-va-service-qatlam-patternlari.md#825-orkestrator-vs-fasad-orchestrator-vs-facade)).
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

**Qurish qarorlari:** Tashqi holatni ajratish bepul emas, shuning uchun u foyda berishini oldin tekshirish kerak: ajratish faqat tashqi holat turlari obyekt sonidan ancha kam bo'lganda tejaydi. Eng yaxshi hol - tashqi holatni umuman saqlamasdan hisoblab olish; shunda xotira vaqtga almashadi va bu almashtirish ongli qilinadi, chunki hisoblash har murojaatda takrorlanadi. Ikkinchi qaror bo'lishishni kim boshqarishiga tegishli va uni buzish patternni butunlay yo'q qiladi: klient flyweight'ni o'zi yaratmasligi kerak. Fabrika yagona olish nuqtasi bo'lib, bor nusxani qaytaradi va yo'q bo'lsa yaratadi; klientga `new` qoldirilsa, bo'lishish jim buziladi va kesh ikki xil nusxa saqlaydi. ESLATMA: Java'da bu konventsiya `valueOf` nomi bilan belgilangan va `new Integer(42)` ning deprecate qilinishi aynan shu qoidani tilning o'zida majburlash uchun.

Uchinchi qaror Composite bilan birga ishlatganda chiqadi va u shunchaki tafsilot emas, ierarxiyadagi muloqotni butunlay o'zgartiradi: bo'lishilgan barg o'z otasini saqlay olmaydi, chunki u bir vaqtda ko'p otaga tegishli. Demak ota havolasi tashqi holatga aylanadi va obxod paytida parametr sifatida pastga uzatiladi; daraxt ustidagi har amal "men qayerdaman" degan ma'lumotni o'zi olib yurishi kerak bo'ladi (qarang: [Kompozitni qurish qarorlari](#222-kompozitni-qurish-qarorlari-implementing-composite)).
## 2.7 Proxy (Proxy - static, JDK dynamic proxy, CGLIB)

**Tavsif:** Proxy haqiqiy obyekt bilan bir xil interfeysni taqdim etib, unga murojaatni nazorat qiladi: kechiktirilgan yaratish (lazy), huquq tekshiruvi, caching, remoting yoki logging qo'shishi mumkin. Static proxy qo'lda yoziladi; JDK dynamic proxy `java.lang.reflect.Proxy` orqali runtime'da faqat interfeys asosida generatsiya qilinadi; CGLIB (Spring'da `spring-core` ichiga repackage qilingan) subclass yaratib, interfeyssiz sinflarni ham proxy qiladi. Decorator'dan farqi - maqsad: Decorator xatti-harakat qo'shadi, Proxy esa kirishni boshqaradi.

**Spring'da qayerda uchraydi:** `ProxyFactory`, `JdkDynamicAopProxy`, `CglibAopProxy` va `DefaultAopProxyFactory` tanlovi; `@EnableAspectJAutoProxy(proxyTargetClass = true)` yoki `spring.aop.proxy-target-class` property. `@Transactional`, `@Cacheable`, `@Async`, `@Retryable`, `@PreAuthorize` - barchasi proxy orqali ishlaydi. `@Configuration` sinflari CGLIB bilan subclass qilinadi (`proxyBeanMethods = true`), `@ConfigurationProperties` esa emas. Hibernate'ning lazy association'lari ham proxy (`LazyInitializationException` manbasi), `DelegatingFilterProxy` Servlet filter'ni Spring context'iga ulaydi, Spring Data repository'lari `JdkDynamicAopProxy` + `RepositoryFactorySupport` orqali yaratiladi. Spring Boot 3.x AOT/native image rejimida proxy'lar build vaqtida ro'yxatdan o'tkazilishi kerak.

**Qo'llanish keyslari:**
- Declarative transaction boundary: `@Transactional` metod chaqiruvini proxy ochib-yopadi.
- Metod natijasini `@Cacheable` bilan cache qilish va `@CacheEvict` bilan tozalash.
- Metod darajasidagi security: `@PreAuthorize("hasRole('ADMIN')")` tekshiruvi proxy ichida.
- `@Async` bilan chaqiruvni task executor'ga uzatish (fire-and-forget yoki `CompletableFuture`).
- HTTP interface client'lari (`@HttpExchange` + `HttpServiceProxyFactory`) - interfeys asosida runtime'da client generatsiyasi.

**Ehtiyot bo'ling:** Eng ko'p uchraydigan tuzoq - self-invocation: bir metod ichida `this.other()` chaqirilsa proxy chetlab o'tiladi va `@Transactional`/`@Cacheable` ishlamaydi (yechim: alohida bean, `AopContext.currentProxy()` yoki self-injection). CGLIB `final` sinf va `final` metodni proxy qilolmaydi va `private` metodlarga ta'sir qilmaydi. Parametrsiz konstruktor talabi esa **Spring da yo'q**: Spring 4.0 dan beri CGLIB proxy nusxasi Objenesis bilan, konstruktorni umuman chaqirmasdan yaratiladi (`ObjenesisCglibAopProxy`, sukut bo'yicha ishlatiladi), shuning uchun maydonlar proxy nusxasida `null` bo'ladi va ular faqat delegatga uzatish uchun ishlatiladi. Yalang'och CGLIB ni Spring dan tashqarida ishlatganda parametrsiz konstruktor kerak bo'ladi; JDK proxy esa faqat interfeys metodlarini qamraydi, shuning uchun konkret tipga `cast` qilish `ClassCastException` beradi.

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

**Qurish qarorlari:** Birinchi qadam - qanday proxy qurayotganingizni nomlash, chunki to'rt tur bir xil tuzilishga ega bo'lsa ham turli masalani yechadi va turlicha sinadi.

| Tur | Nima qiladi | Spring yoki platformadagi ko'rinishi |
|---|---|---|
| Remote proxy | Boshqa adres maydonidagi obyektning mahalliy vakili | `@HttpExchange` + `HttpServiceProxyFactory`, eski RMI eksportyorlari |
| Virtual proxy | Qimmat obyektni talab bo'yicha yaratadi | Hibernate lazy association, `LazyConnectionDataSourceProxy` |
| Protection proxy | Murojaat huquqini tekshiradi | `@PreAuthorize` va `@Secured` uchun yasalgan proxy |
| Smart reference | Murojaatda qo'shimcha ish bajaradi | `@Transactional`, `@Cacheable`, `@Observed` interceptor zanjiri |

Ikkinchi qaror proxy'ning subject haqidagi bilimiga tegishli: proxy haqiqiy obyektning konkret turini bilishi shart emas. Abstrakt interfeys orqali ishlasa bitta proxy barcha subject sinflariga yetadi; konkret turni faqat subject'ni o'zi yaratadigan virtual proxy bilishi kerak. ESLATMA: Java'da bu ajratish mexanizm darajasida ko'rinadi - JDK dynamic proxy interfeysga, CGLIB esa subclass'ga tayanadi, shuning uchun interfeysga qurilgan proxy avtomatik ravishda umumiyroq bo'ladi.

Uchinchi qaror virtual proxy uchun hal qiluvchi: subject hali yaratilmagan paytda proxy unga qanday murojaat qiladi. Javob - adres maydonidan mustaqil identifikator saqlanadi: fayl nomi, ID yoki host va manzil. ESLATMA: Hibernate'ning lazy proxy'si aynan shunday ishlaydi, u faqat identifikatorni ushlaydi va `getId()` chaqirig'i uchun bazaga bormaydi; `LazyInitializationException` esa shu identifikatordan haqiqiy obyektga o'tish yo'li yopilganda chiqadi. Oxirgi tafsilot shartnomaga tegishli: protection proxy interfeysi subject interfeysining qism to'plami bo'lib qolishi mumkin, chunki u subject bajaradigan amalni rad etishi mumkin. Demak "proxy bir xil interfeys beradi" da'vosi aslida "ko'pi bilan bir xil" degani va klient rad etishni kutishi shart - `@PreAuthorize` rad etgan metod aynan shu holat.
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

**Qurish qarorlari:** Yuqoridagi "zamonaviy Java'da annotatsiya afzal" tavsiyasi umumiy qoida, lekin tanlov mezoni aniq va u ikki savoldan iborat. Birinchi savol: belgi sinf va interfeysdan boshqa elementga (maydon, metod, parametr, paket) qo'yiladimi. Qo'yilsa annotatsiya majburiy, chunki marker interfeys faqat turga yopishadi. Ikkinchi savol: faqat shu belgini olgan obyektlarni qabul qiladigan metod yozish ehtimoli bormi. Bor bo'lsa marker interfeys tanlanadi, chunki u turni beradi va kompilyator parametrni tekshiradi; annotatsiya bilan bu tekshiruv ish vaqtiga suriladi. `@Target(ElementType.TYPE)` li marker annotatsiya yozayotgan bo'lsangiz, shu ikkinchi savolga javob berib ko'rish arzon tekshiruv: javob "ha" bo'lsa interfeys to'g'ri tanlov.

Marker interfeysning yana bir afzalligi aniqroq nishonlash: u o'zi qo'llanadigan yagona interfeysni kengaytirib, barcha markerlangan turlar shu interfeysning subtipi bo'lishini kafolatlaydi; `@Target(TYPE)` li annotatsiya esa har qanday sinf va interfeysga tushadi va noto'g'ri joyda turganini hech kim aytmaydi.

Annotatsiyaga tayanganda ikki chegarani bilish kerak. Birinchi: annotatsiya annotatsiyalangan kodning semantikasini o'zgartirmaydi, u faqat asboblarga ma'lumot beradi - xulq o'zgarishi annotatsiyani o'qiydigan kodda (framework, processor, proxy) yuz beradi, annotatsiyaning o'zida emas. Ikkinchi: ko'p qiymatli annotatsiyaning ikki shakli bor, massiv parametri va `@Repeatable`, va ikkinchisi jim tuzoq beradi - takrorlangan annotatsiya konteyner turiga aylangani uchun `isAnnotationPresent` uni KO'RMAYDI. Shuning uchun refleksiya bilan o'qiganda ikki turni ham tekshirish kerak (takrorlanadigan annotatsiyaning mexanikasi va Spring'dagi ko'rinishi: qarang [Meta-annotatsiyalar va kompozit annotatsiyalar](05-spring-core-ichidagi-patternlar-xaritasi.md#538-meta-annotatsiyalar-va-kompozit-annotatsiyalar-meta-annotations--composed-annotations)).
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

## 2.18 Obyekt interfeysini spetsifikatsiyalash (Specifying Object Interfaces)

**Tavsif:** Strukturaviy patternlarning hammasi interfeys ustida ishlaydi, shuning uchun atamalar aniq bo'lishi kerak. Metod e'lon qilganda uning nomi, parametr tiplari va qaytaruvchi qiymati birga signatura deyiladi. Obyektning barcha signaturalari to'plami uning interfeysi; interfeysga berilgan nom esa tur (type). Bitta obyekt bir nechta turga ega bo'lishi mumkin, bir-biriga umuman o'xshamagan obyektlar bir xil turni bo'lishishi mumkin, va agar bir turning interfeysi ikkinchisining interfeysini to'liq o'z ichiga olsa, birinchisi ikkinchisining subtype'i bo'ladi. So'rovni qaysi metod bajarishi ish vaqtida so'rov va qabul qiluvchi obyektga qarab hal qilinadi: bu dynamic binding, va uning natijasi - bir xil interfeysli obyektlarni ish vaqtida bir-birining o'rniga qo'yish mumkinligi, ya'ni polimorfizm (qarang: [26-bo'lim](26-dizayn-printsiplari-solid-grasp-va-umumiy.md#2611-polimorfizm-polymorphism), Polimorfizm). Patternlar interfeysni nafaqat tavsiflaydi, balki unga shartlar ham qo'yadi va ba'zan nima kiritmaslik kerakligini aytadi: Decorator va Proxy o'ralgan obyekt bilan bir xil interfeysga ega bo'lishi shart, aks holda klient almashtirishni sezadi; Visitor interfeysi tashrif qilinadigan barcha element sinflarini aks ettirishi kerak; Memento esa ataylab ikki interfeys beradi, biri klient uchun tor, ikkinchisi faqat egasi uchun keng. Ya'ni interfeys dizayni patterndan kelib chiqadi, patternni tanlagandan keyin interfeys "erkin" qolmaydi.

**Spring'da qayerda uchraydi:** Spring interfeysga tayangan deyarli hamma joyda bir xil interfeysli almashtirishdan foydalanadi: `DataSource` ni `TransactionAwareDataSourceProxy` bilan o'rash, `CacheManager` ni `TransactionAwareCacheManagerProxy` bilan o'rash, `@Transactional` va `@Cacheable` uchun yasaladigan proxy. Aynan shu sabab `@Transactional` ni `private` yoki `final` metodga qo'yish ishlamaydi: proxy interfeysni yoki ochiq metodni takrorlay olmasa, almashtirish buziladi. `BeanWrapper`, `Environment`, `ConversionService`, `HttpMessageConverter` va `ClientHttpRequestFactory` - bularning har biri "tur" sifatida e'lon qilinib, implementatsiyasi konfiguratsiya orqali tanlanadi. Java'da tur va implementatsiya ajratilgani uchun GoF ta'rifidagi farq tilning o'zida ko'rinadi: `interface` turni, `class` esa implementatsiyani beradi.

**Qo'llanish keyslari:**
- Decorator yoki Proxy qo'shishdan oldin asl tipning interfeysi mavjudligini tekshirish; bo'lmasa, uni avval ajratish.
- Memento uslubida ikki yuza berish: tashqariga faqat o'qiladigan `Snapshot`, egasiga esa holatni tiklash metodi.
- Tashqi jamoaga beriladigan interfeysga faqat zarur signaturalarni qoldirish va qolganini `package-private` qilish.
- Bir nechta implementatsiyani almashtirish uchun klient faqat turga tayanishini tasdiqlash: konstruktor parametrida konkret sinf bo'lmasligi.
- Visitor qo'shishda element ierarxiyasining to'liqligini `sealed` bilan kompilyatorga tekshirtirish.

**Ehtiyot bo'ling:** Interfeysni implementatsiyadan nusxa olib yozish eng tez-tez uchraydigan xato: `getJdbcTemplate()` yoki `getEntityManager()` interfeysda paydo bo'lsa, almashtirish imkoniyati yo'qoladi. Teskari chekka ham bor: har sinf uchun bitta foydalanuvchisi bo'lgan interfeys yasash faqat fayl sonini oshiradi. Interfeysga qarab programmalash printsipi va uning chegaralari alohida yozilgan (qarang: [26-bo'lim](26-dizayn-printsiplari-solid-grasp-va-umumiy.md#2625-interfeysga-qarab-programmalash-program-to-an-interface), Interfeysga qarab programmalash). `default` metod qo'shish interfeysni kengaytirishning arzon yo'li, lekin u subtype shartnomasini jimgina o'zgartiradi: mavjud implementatsiyalar yangi xulqni o'zi bilmay oladi.

```java
// Memento ikki interfeys beradi: klient uchun tor, egasi uchun keng
public interface EditorSnapshot { }                 // klient faqat ushlab turadi

public final class TextEditor {
    private String text = "";

    private static final class Snapshot implements EditorSnapshot {
        private final String text;                  // faqat egasi ko'radi
        private Snapshot(String text) { this.text = text; }
    }

    public EditorSnapshot save() { return new Snapshot(text); }

    public void restore(EditorSnapshot snapshot) {
        this.text = ((Snapshot) snapshot).text;     // keng yuza bu yerda
    }
}
// Klient Snapshot ichiga kira olmaydi: interfeys ataylab bo'sh.
```

## 2.19 Sinf merosi va interfeys merosi (Class versus Interface Inheritance)

**Tavsif:** Obyektning sinfi va turi ikki boshqa narsa. Sinf obyektning qanday amalga oshirilganini belgilaydi: ichki holat va metodlar tanasi. Tur esa faqat interfeysga, ya'ni obyekt javob bera oladigan so'rovlar to'plamiga ishora qiladi. Shundan ikki xil meros chiqadi. Sinf merosi bitta sinf implementatsiyasini boshqasi orqali ta'riflaydi: bu kod va ma'lumot tasvirini bo'lishish mexanizmi. Interfeys merosi (subtyping) esa butunlay boshqa savolga javob beradi: qachon bitta obyektni ikkinchisining o'rniga qo'yish mumkin. C++ va Smalltalk bu farqni tilda ko'rsatmagani uchun GoF uni alohida tushuntirishga majbur bo'lgan; Java'da farq sintaksisda turadi (`implements` va `extends`), shuning uchun uni yo'qotish qiyinroq, lekin `extends` bilan implementatsiyani ham, turni ham birga olish hali ham mumkin va shu yerda chalkashlik qoladi. Patternlarning ko'pi aynan shu farqqa tayanadi: Chain of Responsibility ishtirokchilari umumiy turga ega bo'lishi shart, lekin umumiy implementatsiyani bo'lishishi shart emas; Composite'da `Component` umumiy interfeysni beradi, `Composite` esa ko'pincha umumiy implementatsiyani ham beradi; Command, Observer, State va Strategy esa odatda sof interfeys sifatida yoziladi. Demak "meros qilamizmi" savoli ikkiga bo'linadi: turni bo'lishish kerakmi, va implementatsiyani bo'lishish kerakmi.

**Spring'da qayerda uchraydi:** Spring ikki merosni ataylab ajratadi. Turni bo'lishish uchun sof interfeyslar: `ApplicationListener`, `Converter`, `HealthIndicator`, `AuthenticationProvider`, `HandlerInterceptor`. Implementatsiyani bo'lishish uchun esa `Abstract` prefiksli yordamchi sinflar: `AbstractAuthenticationProcessingFilter`, `AbstractRoutingDataSource`, `AbstractErrorWebExceptionHandler`. Juftlikning ma'nosi shu: interfeys shartnoma, `Abstract` sinf esa ixtiyoriy yordam. `OncePerRequestFilter` xuddi shu uslubda `Filter` turini beradi va takroriy bajarilishdan himoyani implementatsiya sifatida qo'shadi. Spring Data `JpaRepository` esa teskari misol: u turni ham, generatsiya qilinadigan implementatsiyani ham birga beradi, shuning uchun uni domen interfeysi sifatida tashqariga chiqarish bog'liqlikni oshiradi.

**Qo'llanish keyslari:**
- Kengaytirish nuqtasini ikki qavat qilib berish: majburiy interfeys va ixtiyoriy `Abstract` yordamchi sinf.
- `Abstract` bazaviy sinfdan meros olgan domen sinfini interfeys va delegatsiyaga ko'chirish (qarang: [Delegatsiya](#213-delegatsiya-delegation)).
- Test'da almashtirish uchun faqat tur kerak bo'lgan joyni aniqlash: u yerda bazaviy sinfdan meros shart emas.
- Repository interfeysini domen porti sifatida o'zi yozib, Spring Data interfeysini faqat infratuzilma qatlamida qoldirish.
- `sealed interface` bilan turni yopib, implementatsiyalar ro'yxatini kompilyatsiya vaqtida belgilash.

**Ehtiyot bo'ling:** Faqat kodni qayta ishlatish uchun meros olish eng qimmat xato: subclass superclass'ning ichki tuzilishiga bog'lanadi va superclass o'zgarsa jimgina buziladi (fragile base class). Buning o'rnini kompozitsiya egallaydi (qarang: [26-bo'lim](26-dizayn-printsiplari-solid-grasp-va-umumiy.md#2617-vorislikdan-ustun-kompozitsiya-composition-over-inheritance), Vorislikdan ustun kompozitsiya). Spring'da yana bitta aniq tuzoq bor: `Abstract` sinfdan meros olib, `@Transactional` yoki `@Cacheable` metodni o'sha ierarxiya ichidan chaqirish proxy'ni chetlab o'tadi. Va subtype bo'lish faqat signatura mosligi emas: shartnoma ham saqlanishi kerak, aks holda almashtirish kompilyatsiya qilinadi, lekin ish vaqtida buziladi.

```java
// Tur va implementatsiya ajratilgan: interfeys shartnoma, Abstract yordam
public interface NotificationChannel {
    boolean supports(NotificationType type);
    void send(Notification notification);
}

// Ixtiyoriy yordam: faqat takrorlanadigan qismni beradi, shartnomani emas
public abstract class RetryingChannel implements NotificationChannel {
    @Override public final void send(Notification notification) {
        for (int attempt = 1; attempt <= 3; attempt++) {
            try { deliver(notification); return; }
            catch (TransientChannelException e) { if (attempt == 3) throw e; }
        }
    }
    protected abstract void deliver(Notification notification);
}

// Yordamdan foydalanmaydigan implementatsiya ham to'liq haqli
@Component
class WebhookChannel implements NotificationChannel { /* ... */ }
```

## 2.20 Qayta ishlatish mexanizmlari: white-box, black-box va parametrlangan turlar (Putting Reuse Mechanisms to Work)

**Tavsif:** Funksionallikni qayta ishlatishning uch mexanizmi bor va ular bir-birining o'rnini bosa oladi. Birinchisi - sinf merosi. Unda ota sinfning ichki tuzilishi subclass'ga ko'rinadi, shuning uchun bu usul white-box reuse deb ataladi: "oq quti", ichi ko'rinadi. U kompilyatsiya vaqtida qotadi, tilning o'zi qo'llab-quvvatlaydi, lekin ota sinfning implementatsiyasi o'zgarsa subclass o'zgarishga majbur bo'ladi. Ikkinchisi - obyekt kompozitsiyasi. Yangi xulq mavjud obyektlarni yig'ish orqali olinadi va yig'ilayotgan obyektlar faqat o'z interfeysi orqali ko'rinadi, shuning uchun bu black-box reuse: "qora quti", ichi ko'rinmaydi. U ish vaqtida tuziladi, inkapsulyatsiyani buzmaydi, lekin ko'proq obyekt va ko'proq bilvosita chaqiruv beradi. Uchinchisi - parametrlangan turlar. GoF bu mexanizmni Ada generiklari va C++ shablonlari misolida ko'rsatadi; Java'dagi javobi generiklar, va quyidagi misollar kitob kodidan emas, shu g'oyadan olingan. Parametrlangan turda tur boshqa turlarni to'liq ko'rsatmasdan ta'riflanadi va yetishmagani ishlatish nuqtasida parametr sifatida beriladi. Bir xil masalani uchtasi bilan ham hal qilish mumkin, va klassik misoli - saralashda taqqoslashni parametrlash: taqqoslashni subclass metodi qilib berish Template Method bo'ladi, taqqoslashni tashqaridan uzatiladigan obyekt qilib berish Strategy bo'ladi, taqqoslashni tur parametri qilib berish esa generik yechim bo'ladi. Farqi aniq: kompozitsiya xulqni ish vaqtida almashtiradi, lekin bilvosita qatlam qo'shadi; meros standart implementatsiya berib, uni override qilishga imkon beradi; parametrlangan turlar sinf ishlatadigan turlarni o'zgartiradi, biroq meros ham, generiklar ham ish vaqtida o'zgarmaydi. Delegatsiya kompozitsiyaning eng keskin shakli (qarang: [Delegatsiya](#213-delegatsiya-delegation)) va u merosni kod qayta ishlatish mexanizmi sifatida har doim almashtira olishini ko'rsatadi.

**Spring'da qayerda uchraydi:** Uchtasi bir vaqtda `JdbcTemplate` atrofida ko'rinadi: `JdbcTemplate` ning o'zi kompozitsiya orqali `DataSource` ni oladi (black-box), `RowMapper` strategiya sifatida tashqaridan beriladi, `RowMapper<T>` esa parametrlangan tur bo'lib natija tipini kompilyatsiya vaqtida bog'laydi. `Comparator.comparing(...).thenComparing(...)` kompozitsiya va generiklarning birga ishlashi; `AbstractRoutingDataSource` esa white-box kengaytirishning saqlanib qolgan misoli. `TransactionTemplate.execute(TransactionCallback<T>)`, `RestClient` va `ResponseEntity<T>` ham shu uchligiga tayanadi. Spring Data `JpaRepository<T, ID>` parametrlangan tur bilan butun CRUD yuzasini bir marta ta'riflab beradi.

**Qo'llanish keyslari:**
- Kutubxona API'sida kengaytirishni meros emas, callback yoki strategiya obyekti sifatida berish.
- Bir xil algoritmni turli tiplar ustida ishlatish uchun generik parametr kiritish va `instanceof` tekshiruvlarini olib tashlash.
- `AbstractBaseService` ierarxiyasini bosqichma-bosqich kompozitsiyaga ko'chirish va har qadamda testlarni ishlatish.
- Taqqoslash yoki validatsiya qoidasini bean sifatida inject qilib, uni muhit bo'yicha almashtirish.
- Framework kodida ikki qavat berish: generik interfeys va uning ustida ixtiyoriy `Abstract` yordamchisi.

**Ehtiyot bo'ling:** Uch mexanizmdan birini "har doim to'g'ri" deb tanlash xato. Meros va kompozitsiya tanlovining to'liq yozuvi alohida turadi (qarang: [26-bo'lim](26-dizayn-printsiplari-solid-grasp-va-umumiy.md#2617-vorislikdan-ustun-kompozitsiya-composition-over-inheritance), Vorislikdan ustun kompozitsiya). Kompozitsiyaning narxi: obyekt soni oshadi, xulq bitta sinfda emas aloqalarda yashaydi va stack trace uzayadi. Generiklarning narxi Java'da alohida: type erasure sababli ish vaqtida tur parametri yo'q, shuning uchun `new T()`, `instanceof T` va `T[]` ishlamaydi va Spring'da `ParameterizedTypeReference` yoki `ResolvableType` kerak bo'ladi. Bir masalani uchta mexanizm bilan bir vaqtda hal qilish esa o'qib bo'lmaydigan kod beradi.

```java
// Bitta masala, uch mexanizm. Tanlov: nima qachon o'zgarishi kerak.

// 1. Template Method: taqqoslash subclass'da, kompilyatsiya vaqtida qotadi
abstract class SortedReport {
    protected abstract int compare(Row a, Row b);
    final List<Row> rows(List<Row> in) { return in.stream().sorted(this::compare).toList(); }
}

// 2. Strategy: taqqoslash obyekt, ish vaqtida almashadi
record ReportSorter(Comparator<Row> order) {
    List<Row> rows(List<Row> in) { return in.stream().sorted(order).toList(); }
}

// 3. Parametrlangan tur: element tipi parametr, xulq emas
static <T> List<T> sorted(List<T> in, Comparator<? super T> order) {
    return in.stream().sorted(order).toList();
}
```

## 2.21 Ish vaqtidagi va kompilyatsiya vaqtidagi struktura (Run-Time and Compile-Time Structures)

**Tavsif:** Obyektga yo'naltirilgan programmaning ish vaqtidagi tuzilishi uning kod tuzilishiga kam o'xshaydi. Kod tuzilishi kompilyatsiya vaqtida qotadi: sinflar va ular orasidagi o'zgarmas meros munosabatlari. Ish vaqtidagi tuzilish esa tez o'zgaradigan, bir-biriga xabar yuboradigan obyektlar tarmog'i. Ikkisi asosan mustaqil va birini ikkinchisidan kelib chiqarib tushunishga urinish natija bermaydi. Shu farqning ikki muhim ko'rinishi bor. Agregatsiya bitta obyekt ikkinchisiga egalik qilishini yoki uning uchun javobgar ekanini bildiradi va odatda ikkisining hayot muddati bir xil bo'ladi. Tanishlik (acquaintance) esa obyekt ikkinchisidan faqat "xabardor" ekanini bildiradi; uni assotsiatsiya yoki "ishlatish" munosabati deb ham atashadi. Tanishlik agregatsiyadan kuchsizroq va kamroq bog'lanish beradi: tanishlik aloqalari tez-tez yasaladi va yo'qoladi, ba'zan faqat bitta amal davomida yashaydi. Java'da ikkisi ham oddiy ishora bilan amalga oshadi, shuning uchun farq tilda ko'rinmaydi va faqat niyat bilan belgilanadi. Obyekt qamrovidagi patternlarning ko'pi aynan shu farqni ushlaydi: Composite va Decorator murakkab ish vaqtidagi tuzilmalarni qurish uchun ishlatiladi, Observer'ning ish vaqtidagi tuzilishini patternni bilmasdan tushunib bo'lmaydi, Chain of Responsibility esa meros ierarxiyasida umuman ko'rinmaydigan aloqa yo'llarini yasaydi.

**Spring'da qayerda uchraydi:** Spring'da ish vaqtidagi tuzilish bean grafi bo'lib, u kod tuzilishidan ancha boshqa ko'rinadi: `@Component` ro'yxati statik, lekin kim kimga ulanishi `@Profile`, `@ConditionalOnProperty`, `@Order` va `@Primary` bilan deployment paytida hal bo'ladi. Shuning uchun grafni koddan emas, ishlab turgan ilovadan o'qish kerak: Actuator'ning `/actuator/beans` endpoint'i bean grafini, `/actuator/conditions` esa qaysi auto-configuration nega qo'llangani yoki qo'llanmaganini beradi; `--debug` bilan ishga tushirish xuddi shu hisobotni konsolga chiqaradi. Filter va interceptor zanjirlari, `SecurityFilterChain` va `HandlerInterceptor` tartibi ham faqat ish vaqtida ko'rinadi. Agregatsiya va tanishlik farqi JPA'da esa to'g'ridan-to'g'ri xulqqa aylanadi: `cascade` va `orphanRemoval` agregatsiyani bildiradi, oddiy `@ManyToOne` esa tanishlikni.

**Qo'llanish keyslari:**
- Dekorator yoki interceptor zanjiri chalkashganda grafni Actuator orqali chiqarib, tartibni tasdiqlash.
- Yangi bog'liqlik qo'shishda ongli qaror: bu egalikmi yoki shunchaki xabardorlikmi, va shunga mos JPA `cascade` sozlamasi.
- Observer asosidagi oqimni hujjatlashtirishda kim kimni eshitayotganini alohida diagrammada ko'rsatish, chunki koddan ko'rinmaydi.
- `@Order` yoki `Ordered` qiymatlarini ochiq konstantaga chiqarib, zanjir tartibini kodda ko'rinadigan qilish.
- Incident tahlilida chaqiruv grafini tracing orqali o'lchab, kod tuzilishidan chiqqan taxminni tekshirish.

**Ehtiyot bo'ling:** Eng ko'p uchraydigan xato - ish vaqtidagi tuzilishni kod o'qish orqali bilish mumkin deb o'ylash: paket diagrammasi bean grafini bermaydi. Ikkinchi xato - agregatsiya va tanishlikni ongsiz aralashtirish: `cascade = CascadeType.ALL` ni tanishlik munosabatiga qo'yish boshqa agregatning ma'lumotini o'chirib yuboradi. Uchinchisi - zanjirni juda uzun qilish: har qatlam alohida to'g'ri, lekin birgalikda hech kim kutmagan tartibda ishlaydi va xatolikni qaysi qatlam keltirganini aniqlash qiyinlashadi. Ish vaqtidagi tuzilishni tilga tashlab qo'ymang: uni dizayner ongli ravishda belgilaydi.

```text
Bir xil kod, ikki xil ish vaqtidagi tuzilish:

  Kod tuzilishi (kompilyatsiya vaqtida qotgan)
    interface NotificationChannel
      EmailChannel, SmsChannel, WebhookChannel   -> uchta sinf, meros grafi

  Ish vaqtidagi tuzilish (profil bilan hal bo'ladi)
    prod:   Retrying(Metered(EmailChannel))
            Retrying(Metered(SmsChannel))
    test:   RecordingChannel

Birinchisini `grep` ko'rsatadi. Ikkinchisini faqat
`/actuator/beans` va `/actuator/conditions` ko'rsatadi.
```

## 2.22 Kompozitni qurish qarorlari (Implementing Composite)

**Tavsif:** [Kompozit](#23-kompozit-composite) niyati sodda, lekin uni qurishda beshta qaror bor va ularning har biri keyinchalik qimmat tushadi. Birinchisi - ota havolasi. Component'da otaga havola saqlash obxodni va o'chirishni soddalashtiradi, bolaga "men qayerdaman" degan savolga javob beradi va yuqoriga ko'tariladigan so'rov uchun tayyor zanjir yasaydi ([Mas'uliyat zanjiri](03-xulq-atvor-patternlari.md#31-masuliyat-zanjiri-chain-of-responsibility) shu havolalar ustida ishlashi mumkin). Narxi invariantda: bolaning otasi faqat `add` va `remove` ichida o'zgaradi, boshqa hech bir joyda. Invariant buzilsa daraxt ikki xil haqiqatni saqlaydi - ota bolani ko'radi, bola boshqa otani ko'rsatadi - va bu xato obxodda emas, o'chirish yoki ko'chirish paytida chiqadi. Ikkinchi qaror - Component interfeysining kengligi. Patternning maqsadi klient Leaf va Composite farqini bilmasligi bo'lgani uchun interfeys maksimal qilinadi: Leaf uchun ma'nosiz ko'rinadigan amal ham Component'ga default implementatsiya bilan chiqariladi, masalan bolalarni so'rash Leaf'da bo'sh ro'yxat qaytaradi. Uchinchi qaror esa teskari yo'nalishda cheklaydi: bolalar ro'yxatini Component'da maydon sifatida saqlamang. Har Leaf hech qachon ishlatilmaydigan maydonni ko'tarib yuradi va bargi ko'p daraxtda bu sof xotira yo'qotishi; ro'yxat Composite'da turadi, Component'da faqat uni o'qiydigan amal qoladi. To'rtinchi qaror tartibga tegishli: bolalar tartibi ahamiyatli bo'lsa (menyu, hujjat bo'limlari, filter zanjiri), kirish va boshqarish interfeysi shu ketma-ketlikni oshkora ifodalashi kerak, aks holda tartib `List` ning tasodifiy xulqiga qoladi. Beshinchi qaror - keshlash. Composite obxod yoki qidiruv natijasini keshlashi mumkin, lekin bola o'zgarganda ota keshi invalidatsiya qilinishi shart, demak bolada otaga "keshing eskirdi" deb aytadigan amal bo'lishi kerak; aynan shu talab yuqoridagi ota havolasini majburiy qiladi.

**Spring'da qayerda uchraydi:** Spring'ning kompozitlari odatda bu qarorlarning soddalashtirilgan shaklini oladi: `CompositeHealthContributor` va `CompositeMeterRegistry` bolalarni faqat o'qish uchun ushlaydi, ota havolasi yo'q va tartib ahamiyatsiz. Tartib ahamiyatli bo'lgan joyda Spring uni interfeys darajasiga chiqaradi: `FilterChainProxy` ichidagi `SecurityFilterChain` ro'yxati va `MutablePropertySources` ning `addFirst`, `addLast`, `addBefore` metodlari ketma-ketlikni oshkora boshqaradi. Keshlash va invalidatsiya juftligi `ResolvableType` va `AnnotationUtils` keshlarida ko'rinadi: kesh o'zgarmas tuzilma ustida qurilgani uchun invalidatsiya kerak emas, o'zgaradigan tuzilmada esa `ConfigurableApplicationContext.refresh()` keshni butunlay tashlab yuboradi. JPA tomonida `@OneToMany(mappedBy = ...)` bilan ikki tomonlama bog'lanish aynan ota havolasi invariantini talab qiladi va uni `addChild` yordamchi metodi ichida saqlash odatiy amaliyot.

**Qo'llanish keyslari:**
- Kategoriya daraxtida mahsulot narxini yuqoriga agregatlash va natijani ota tugunda keshlash, bola o'zgarganda zanjirni ildizga qadar invalidatsiya qilish.
- Hujjat tuzilmasida bo'limlar tartibini saqlash: `addAfter(existing, node)` kabi amal bilan ketma-ketlikni interfeysga chiqarish.
- Tashkilot ierarxiyasida xodimdan yuqoriga ko'tarilib mas'ul rahbarni topish - ota havolasi ustidagi zanjir.
- Katta daraxtda bargi juda ko'p bo'lganda bolalar ro'yxatini faqat kompozit tugunlarda saqlab, xotirani o'lchab ko'rish.
- Takrorlanadigan barg tugunlarini (bir xil o'lchov birligi, bir xil tarif) bo'lishib, otani obxod parametri sifatida uzatish.

**Ehtiyot bo'ling:** Komponentlarni bo'lishish bitta ota cheklovi sababli qiyin: bo'lishilgan tugun bir vaqtda ko'p joyda turgani uchun o'z otasini saqlay olmaydi. [Flyweight](#26-flyweight-flyweight) bu muammoni ota havolasini tashqi holatga chiqarib yechadi, lekin yechimning narxi bor - endi har amal otani parametr sifatida olib yurishi kerak va ota havolasiga tayangan qulaylik (yuqoriga ko'tarilish, invalidatsiya) yo'qoladi. Ikkinchi tuzoq - `add` va `remove` ni Leaf ga kelganda nima qilish. Bu yerda ikki qarama-qarshi tavsiya bor va ajratuvchi shart bitta: shu amalni kim chaqiradi. Klient butun daraxtni bir xil ko'rishi kerak bo'lsa (masalan generic daraxt tahrirlovchisi) `add` Component'da qoladi va Leaf'da istisno tashlaydi, lekin bu xulq shartnomada OSHKORA yoziladi: Javadoc "bu amal barg tugunda `UnsupportedOperationException` tashlaydi" deb aytsa, subtip kutilgan xulqdan chetga chiqmaydi va [Liskov almashtirish printsipi](26-dizayn-printsiplari-solid-grasp-va-umumiy.md#263-liskov-almashtirish-printsipi-liskov-substitution-principle) buzilmaydi; yozilmagan istisno esa aynan shu printsipni buzadi va [rad etilgan meros](../clean-code/17-vorislik-kompozitsiya-va-polimorfizm.md#176-rad-etilgan-meros-va-interfeysni-bolish) belgisi bo'ladi. Daraxt qurish koddan ajratilgan bo'lsa (konfiguratsiya yoki fabrika daraxtni bir marta yig'adi, klient faqat o'qiydi) `add` Component'da umuman kerak emas va Composite'da qoladi - shunda istisno masalasi yo'q. ESLATMA: Java 17+ da uchinchi yo'l bor - `sealed` ierarxiya va pattern matching bilan klient Leaf va Composite ni tur darajasida ajratadi, demak `add` ni umumiy interfeysga chiqarish zarurati yo'qoladi.

```java
// Ota havolasi faqat add/remove ichida o'zgaradi, kesh esa yuqoriga invalidatsiya qilinadi
public sealed interface CatalogNode permits Category, Product {
    Money total();
}

public final class Category implements CatalogNode {
    private final List<CatalogNode> children = new ArrayList<>();   // faqat kompozitda
    private Category parent;                                       // ota havolasi
    private Money cachedTotal;                                     // obxod keshi

    public void add(CatalogNode child, int index) {                 // tartib oshkora
        children.add(index, child);
        if (child instanceof Category c) c.parent = this;           // invariant shu yerda
        invalidateUpwards();
    }

    public void remove(CatalogNode child) {
        if (children.remove(child) && child instanceof Category c) c.parent = null;
        invalidateUpwards();
    }

    private void invalidateUpwards() {
        cachedTotal = null;
        if (parent != null) parent.invalidateUpwards();              // ildizga qadar
    }

    @Override public Money total() {
        if (cachedTotal == null) {
            cachedTotal = children.stream().map(CatalogNode::total)
                    .reduce(Money.zero("UZS"), Money::add);
        }
        return cachedTotal;
    }
}
// Product barg: bolalar ro'yxati ham, ota havolasi ham yo'q - maydon narxini to'lamaydi
```

## 2.23 Amalda qo'llash

- [ ] Tashqi kutubxona tiplari domen paketiga kirib kelgan joylarni qidiring va har biri uchun Adapter chegarasini belgilang.
- [ ] `@Transactional`, `@Cacheable` va `@Async` annotatsiyasi bor metodlarning `public` va tashqaridan chaqirilayotganini tekshiring - self-invocation proxy'ni chetlab o'tadi.
- [ ] `final` sinf yoki `final` metodga proxy qo'llanmoqchi bo'lgan joylarni toping; CGLIB ularni proxy qila olmaydi.
- [ ] Dekorator zanjirlarini sanab chiqing va har bir zanjirning tartibi `@Order` bilan aniq belgilanganini tasdiqlang.
- [ ] Faqat bitta implementatsiyasi bor interfeyslarni ro'yxatga oling va ularning qanchasi haqiqatan chegara ekanini qaror qiling.
- [ ] Fasad deb nomlangan sinflarni tekshiring: ular soddalashtiryaptimi yoki shunchaki chaqiruvlarni uzatyaptimi.
- [ ] Ko'p nusxada yaratilgan o'zgarmas qiymat obyektlarini (valyuta, mintaqa, status) toping va ularni Flyweight sifatida keshlash foydasini o'lchang.
- [ ] Marker interfeyslarni annotatsiyaga almashtirish mumkinmi degan savolni har biri uchun hal qiling.

## Manbalar

- Freeman/Robson, *Head First Design Patterns* 2nd, 3-bob - Decorator va o'rash orqali xatti-harakat qo'shish
- Freeman/Robson, *Head First Design Patterns* 2nd, 7-bob - Adapter va Facade
- Freeman/Robson, *Head First Design Patterns* 2nd, 9-bob - Composite
- Freeman/Robson, *Head First Design Patterns* 2nd, 11-bob - Proxy va uning turlari
- Joshua Bloch, *Effective Java* 3rd, Item 18 - vorislik o'rniga kompozitsiya va o'rovchi sinf
- Joshua Bloch, *Effective Java* 3rd, Item 41 - marker interfeys bilan tur belgilash
- [Spring Framework, AOP Proxies](https://docs.spring.io/spring-framework/reference/core/aop/proxying.html) - JDK dinamik proxy va CGLIB farqi
- [Spring Framework v7.0.0, ObjenesisCglibAopProxy](https://raw.githubusercontent.com/spring-projects/spring-framework/v7.0.0/spring-aop/src/main/java/org/springframework/aop/framework/ObjenesisCglibAopProxy.java) - CGLIB proxy konstruktorni chaqirmasdan yaratiladi, 4.0 dan beri sukut bo'yicha
- [Java API, `java.lang.reflect.Proxy`](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/lang/reflect/Proxy.html) - JDK dinamik proxy faqat interfeys asosida ishlashi
- Erich Gamma, Richard Helm, Ralph Johnson, John Vlissides, *Design Patterns: Elements of Reusable Object-Oriented Software*, Addison-Wesley, 1995, 1.6-bo'lim (13-14-bet) - signatura, interfeys, tur va subtype ta'riflari; Decorator va Proxy interfeysi o'ralgan obyekt bilan bir xil bo'lishi sharti
- Erich Gamma, Richard Helm, Ralph Johnson, John Vlissides, *Design Patterns*, Addison-Wesley, 1995, 1.6-bo'lim (16-17-bet) - sinf merosi va interfeys merosi farqi; Chain of Responsibility umumiy tur talab qiladi, umumiy implementatsiyani esa yo'q
- Erich Gamma, Richard Helm, Ralph Johnson, John Vlissides, *Design Patterns*, Addison-Wesley, 1995, 1.6-bo'lim (18-22-bet) - white-box va black-box qayta ishlatish, hamda parametrlangan turlar uchinchi mexanizm sifatida
- Erich Gamma, Richard Helm, Ralph Johnson, John Vlissides, *Design Patterns*, Addison-Wesley, 1995, 1.6-bo'lim (22-23-bet) - ish vaqtidagi va kompilyatsiya vaqtidagi tuzilish mustaqilligi, agregatsiya va tanishlik farqi
- [Spring Boot, Beans endpoint](https://docs.spring.io/spring-boot/api/rest/actuator/beans.html) - `/actuator/beans` ish vaqtidagi bean grafini beradi
- [JLS 4.6, Type Erasure](https://docs.oracle.com/javase/specs/jls/se21/html/jls-4.html#jls-4.6) - generik tur parametri kompilyatsiyada o'chirilishi, shuning uchun ish vaqtida mavjud emasligi
- Erich Gamma, Richard Helm, Ralph Johnson, John Vlissides, *Design Patterns*, Addison-Wesley, 1995, Adapter, Implementation (141-145-bet) - sinf va obyekt adapteri murosasi, tor interfeysni tanlash, pluggable adapter va ikki interfeysli adapter
- Erich Gamma, Richard Helm, Ralph Johnson, John Vlissides, *Design Patterns*, Addison-Wesley, 1995, Bridge, Implementation (154-bet) - implementatsiya bitta bo'lganda ham ajratish: iste'molchi qayta kompilyatsiya qilinmaydi
- Erich Gamma, Richard Helm, Ralph Johnson, John Vlissides, *Design Patterns*, Addison-Wesley, 1995, Bridge, Implementation (155-bet) - Implementor obyektini kim, qachon va qayerda yaratishining uch varianti
- Erich Gamma, Richard Helm, Ralph Johnson, John Vlissides, *Design Patterns*, Addison-Wesley, 1995, Composite, Implementation (166-168-bet) - ota havolasi va uning `add`/`remove` ichidagi invarianti, Component interfeysini maksimal qilish
- Erich Gamma, Richard Helm, Ralph Johnson, John Vlissides, *Design Patterns*, Addison-Wesley, 1995, Composite, Implementation (171-bet) - bolalar ro'yxatini Component'da saqlamaslik, bolalar tartibini interfeysga chiqarish, obxod keshi va invalidatsiya
- Erich Gamma, Richard Helm, Ralph Johnson, John Vlissides, *Design Patterns*, Addison-Wesley, 1995, Composite, Implementation (167-bet) - komponentlarni bo'lishish bitta ota cheklovi bilan qiyin, Flyweight ota havolasini tashqi holatga chiqaradi
- Erich Gamma, Richard Helm, Ralph Johnson, John Vlissides, *Design Patterns*, Addison-Wesley, 1995, Composite, Implementation (170-bet) - Component'dagi default `add` barg tugunda xato tashlashi
- Erich Gamma, Richard Helm, Ralph Johnson, John Vlissides, *Design Patterns*, Addison-Wesley, 1995, Decorator, Implementation (177-178-bet) - bitta mas'uliyatda abstrakt Decorator kerak emasligi, Component sinfini yengil ushlash, dekorator va komponent bir xil obyekt emasligi
- Erich Gamma, Richard Helm, Ralph Johnson, John Vlissides, *Design Patterns*, Addison-Wesley, 1995, Decorator, Related Patterns (178-180-bet) - teri va ich qiyosi: Decorator va Strategy orasidagi tanlov
- Erich Gamma, Richard Helm, Ralph Johnson, John Vlissides, *Design Patterns*, Addison-Wesley, 1995, Facade, Implementation (186-187-bet) - abstrakt facade bilan klient bog'lanishini kamaytirish, quyi tizimlarni qatlamlash va aylanma bog'liqlikni yo'q qilish
- Erich Gamma, Richard Helm, Ralph Johnson, John Vlissides, *Design Patterns*, Addison-Wesley, 1995, Flyweight, Implementation (199-200-bet) - tashqi holatni ajratish qachon foyda berishi va fabrikaning yagona olish nuqtasi bo'lishi
- Erich Gamma, Richard Helm, Ralph Johnson, John Vlissides, *Design Patterns*, Addison-Wesley, 1995, Flyweight, Applicability (196-bet) - Composite bilan birga ishlatilganda ota havolasi tashqi holatga aylanishi
- Erich Gamma, Richard Helm, Ralph Johnson, John Vlissides, *Design Patterns*, Addison-Wesley, 1995, Proxy, Applicability (208-209-bet) - proxy'ning to'rt turi: remote, virtual, protection va smart reference
- Erich Gamma, Richard Helm, Ralph Johnson, John Vlissides, *Design Patterns*, Addison-Wesley, 1995, Proxy, Implementation (213-214-bet) - proxy subject'ning konkret turini bilishi shart emasligi va yaratilmagan subject'ga identifikator orqali murojaat
- Erich Gamma, Richard Helm, Ralph Johnson, John Vlissides, *Design Patterns*, Addison-Wesley, 1995, Proxy, Consequences (216-bet) - protection proxy interfeysi subject interfeysining qism to'plami bo'lishi
- Joshua Bloch, *Effective Java* 3rd, Item 18 (91-bet) - SELF muammosi: o'rovchi sinf callback framework'ida yaramaydi
- Joshua Bloch, *Effective Java* 3rd, Item 39 (182-bet) - annotatsiya annotatsiyalangan kodning semantikasini o'zgartirmasligi
- Joshua Bloch, *Effective Java* 3rd, Item 39 (186-bet) - `@Repeatable` da `isAnnotationPresent` takrorlangan annotatsiyani ko'rmasligi
- Joshua Bloch, *Effective Java* 3rd, Item 41 (191-bet) - marker interfeysning aniqroq nishonlanishi: u faqat o'zi kengaytirgan interfeys ostida qoladi
- Joshua Bloch, *Effective Java* 3rd, Item 41 (192-bet) - marker annotatsiya va marker interfeys orasidagi tanlov mezoni: belgi qaysi elementga qo'yiladi va faqat belgilanganlarni qabul qiladigan metod kerakmi
- ESLATMA: kitoblarda yo'q, korpus qo'shgan qism - obyekt adapteri Java'da default ekani va pluggable adapterning `Function`/`Supplier` bilan yozilishi; Bridge uchun `@ConditionalOnProperty`, `@Profile` va `ObjectProvider` ko'rinishi; proxy to'rt turining Spring mexanizmlariga xaritasi va Hibernate lazy proxy misoli; AOP proxy'langan bean'ning `==` bilan teng emasligi; Composite qarorlari uchun Spring va JPA ko'rinishi, `CatalogNode` kod misoli va `sealed` uchinchi yo'li; marker tanlovining `sealed` bilan bog'lanishi

---

[&larr; 1. Yaratuvchi patternlar](01-yaratuvchi-patternlar.md) · [Mundarija](README.md) · [3. Xulq-atvor patternlari &rarr;](03-xulq-atvor-patternlari.md)
