<!-- doc: patterns | chapter: 12 | part:  -->

[Java Spring arxitektori bilishi kerak bo'lgan barcha dizayn patternlar](../../README.md) / [Dizayn patternlar](README.md)

# 12. Arxitektura uslublari (Architectural Styles)

<details>
<summary>Bu bo'limdagi 33 bo'lim</summary>

- [12.1 Qatlamli arxitektura (Layered / N-tier Architecture)](#121-qatlamli-arxitektura-layered--n-tier-architecture)
- [12.2 Olti burchakli arxitektura (Hexagonal Architecture / Ports & Adapters)](#122-olti-burchakli-arxitektura-hexagonal-architecture--ports--adapters)
- [12.3 Clean Architecture (Clean Architecture)](#123-clean-architecture-clean-architecture)
- [12.4 Piyoz arxitekturasi (Onion Architecture)](#124-piyoz-arxitekturasi-onion-architecture)
- [12.5 Vertikal qatlamli arxitektura (Vertical Slice Architecture)](#125-vertikal-qatlamli-arxitektura-vertical-slice-architecture)
- [12.6 Modulli monolit (Modular Monolith / Spring Modulith)](#126-modulli-monolit-modular-monolith--spring-modulith)
- [12.7 Mikroyadro / Plugin arxitekturasi (Microkernel / Plugin Architecture)](#127-mikroyadro--plugin-arxitekturasi-microkernel--plugin-architecture)
- [12.8 Quvurlar va filtrlar (Pipes and Filters)](#128-quvurlar-va-filtrlar-pipes-and-filters)
- [12.9 Hodisaga asoslangan arxitektura (Event-Driven Architecture — broker va mediator topologiyalari)](#129-hodisaga-asoslangan-arxitektura-event-driven-architecture--broker-va-mediator-topologiyalari)
- [12.10 Buyruq va so'rovlar mas'uliyatini ajratish (CQRS — Command Query Responsibility Segregation)](#1210-buyruq-va-sorovlar-masuliyatini-ajratish-cqrs--command-query-responsibility-segregation)
- [12.11 Hodisalarni saqlash (Event Sourcing)](#1211-hodisalarni-saqlash-event-sourcing)
- [12.12 Mikroservislar (Microservices)](#1212-mikroservislar-microservices)
- [12.13 O'z-o'ziga Yetarli Tizimlar (Self-Contained Systems)](#1213-oz-oziga-yetarli-tizimlar-self-contained-systems)
- [12.14 Servisga Yo'naltirilgan Arxitektura (Service-Oriented Architecture, SOA)](#1214-servisga-yonaltirilgan-arxitektura-service-oriented-architecture-soa)
- [12.15 Serverless / FaaS (Serverless / Function as a Service)](#1215-serverless--faas-serverless--function-as-a-service)
- [12.16 Kosmosga Asoslangan Arxitektura (Space-Based Architecture)](#1216-kosmosga-asoslangan-arxitektura-space-based-architecture)
- [12.17 Klient-Server (Client-Server)](#1217-klient-server-client-server)
- [12.18 Broker (Broker)](#1218-broker-broker)
- [12.19 Teng-Tengga (Peer-to-Peer)](#1219-teng-tengga-peer-to-peer)
- [12.20 Qoratakhta (Blackboard)](#1220-qoratakhta-blackboard)
- [12.21 Reaktiv Arxitektura (Reactive Architecture)](#1221-reaktiv-arxitektura-reactive-architecture)
- [12.22 Monolit (Monolith)](#1222-monolit-monolith)
- [12.23 Katta Loy To'pi (Big Ball of Mud) — anti-pattern](#1223-katta-loy-topi-big-ball-of-mud--anti-pattern)
- [12.24 Taqsimlangan Monolit (Distributed Monolith) — anti-pattern](#1224-taqsimlangan-monolit-distributed-monolith--anti-pattern)
- [12.25 Hujayra Asosidagi Arxitektura (Cell-Based Architecture)](#1225-hujayra-asosidagi-arxitektura-cell-based-architecture)
- [12.26 Hech Narsani Bo'lishmaslik (Shared-Nothing)](#1226-hech-narsani-bolishmaslik-shared-nothing)
- [12.27 Lambda / Kappa Arxitekturasi (Lambda / Kappa Architecture)](#1227-lambda--kappa-arxitekturasi-lambda--kappa-architecture)
- [12.28 Feature Bo'yicha vs Qatlam Bo'yicha Paketlash (Package-by-feature vs Package-by-layer)](#1228-feature-boyicha-vs-qatlam-boyicha-paketlash-package-by-feature-vs-package-by-layer)
- [12.29 Baqiruvchi Arxitektura (Screaming Architecture)](#1229-baqiruvchi-arxitektura-screaming-architecture)
- [12.30 Komponentga Asoslangan Arxitektura (Component-Based Architecture)](#1230-komponentga-asoslangan-arxitektura-component-based-architecture)
- [12.31 API-Birinchi (API-First)](#1231-api-birinchi-api-first)
- [12.32 Event-Birinchi (Event-First)](#1232-event-birinchi-event-first)
- [12.33 Mikro-Frontendlar (Micro-frontends) — eslatib o'tish](#1233-mikro-frontendlar-micro-frontends--eslatib-otish)

</details>


Arxitektura uslublari — bu alohida sinf darajasidagi dizayn patternlardan farqli ravishda, butun tizimning yuqori darajadagi tuzilishini, modullar orasidagi bog'liqlik yo'nalishini va o'zgarishlar qanday tarqalishini belgilovchi qoliplardir. Arxitektor uchun ular muhim, chunki aynan shu darajadagi qarorlar keyinchalik eng qimmatga tushadi: GoF patternni bir hafta ichida almashtirish mumkin, ammo layered monolitdan event-driven tizimga o'tish yillar va butun jamoaning mehnatini talab qiladi. Spring ekotizimi deyarli barcha ushbu uslublarni qo'llab-quvvatlaydi, lekin hech birini majburlamaydi — shuning uchun tanlov va uning intizomli saqlanishi arxitektor zimmasida. Quyida har bir uslubning mohiyati, Spring'dagi real ko'rinishi va tuzoqlari keltirilgan.

## 12.1 Qatlamli arxitektura (Layered / N-tier Architecture)

**Tavsif:** Tizim mas'uliyatlar bo'yicha gorizontal qatlamlarga bo'linadi: presentation, application/service, domain, persistence. Har bir qatlam faqat o'zidan pastdagi qatlamga murojaat qiladi, bu esa bog'liqliklarni bir yo'nalishli qilib, kodni tushunishni osonlashtiradi. Bu eng keng tarqalgan va eng oson o'rgatiladigan uslub, shuning uchun aksariyat korporativ Spring loyihalari aynan shundan boshlanadi. Qatlamlar "yopiq" (har biri orqali o'tish shart) yoki "ochiq" (ba'zi qatlamlarni o'tkazib yuborish mumkin) bo'lishi mumkin.

**Spring'da qayerda uchraydi:** Klassik `@RestController` → `@Service` → `@Repository` uchligi aynan shu uslubning amaliy ifodasi; `@Repository` ustidagi `PersistenceExceptionTranslationPostProcessor` persistence qatlamining exception'larini `DataAccessException` ierarxiyasiga tarjima qilib, pastki qatlam detallarini yuqoridan yashiradi. Spring Boot 3.x loyihalarida bu odatda `com.example.app.web`, `.service`, `.domain`, `.repository` paketlari ko'rinishida bo'ladi. Qatlam chegaralarini avtomatik tekshirish uchun ArchUnit (`layeredArchitecture()` qoidasi) testlari ishlatiladi. `@Transactional` ni service qatlamida joylash — bu uslubning standart konvensiyasi.

**Qo'llanish keyslari:**
- Klassik CRUD-og'ir admin panel yoki back-office tizimi, bunda domen logikasi juda yupqa.
- Jamoa yangi yoki tez o'sayotgan bo'lsa — eng past kognitiv yuk va eng ko'p tayyor misollar.
- Ichki korporativ reporting xizmatlari, bunda asosiy ish — ma'lumotni DB'dan olib JSON'ga aylantirish.
- Legacy tizimni modernizatsiya qilishda birinchi qadam: avval tartibsiz kodni qatlamlarga ajratish.
- Prototip yoki MVP, keyinchalik hexagonal/modular monolitga evolyutsiya qilish rejasi bilan.

**Ehtiyot bo'ling:** Eng ko'p uchraydigan tuzoq — "anemik domen modeli": butun logika `@Service` sinflarida to'planib, entity'lar faqat getter/setter to'plamiga aylanadi va service'lar minglab qatorga o'sadi. Shuningdek domen qatlami JPA annotatsiyalariga va `Repository` interfeyslariga bog'lanib qolsa, qatlamlar faqat paket nomida qoladi — DB'ni almashtirish yoki domenni alohida test qilish imkoni yo'qoladi.

## 12.2 Olti burchakli arxitektura (Hexagonal Architecture / Ports & Adapters)

**Tavsif:** Ilova yadrosi (domain + use case'lar) markazda turadi va tashqi dunyo bilan faqat o'zi e'lon qilgan interfeyslar — port'lar orqali gaplashadi. Har bir texnologiya (HTTP, Kafka, JPA, SMTP) shu port'ni amalga oshiruvchi adapter sifatida chetga chiqariladi, natijada bog'liqlik yo'nalishi har doim tashqaridan yadroga qarab bo'ladi. Inbound (driving) port'lar yadroni chaqiradi, outbound (driven) port'lar yadro ehtiyojini ifodalaydi. Bu yadroni Spring'dan ham, DB'dan ham mustaqil sinovdan o'tkazish imkonini beradi.

**Spring'da qayerda uchraydi:** Yadro odatda toza POJO'lardan iborat alohida Maven/Gradle moduli bo'lib, unda hech qanday Spring annotatsiyasi bo'lmaydi; adapter modullarida esa `@RestController`, `@KafkaListener`, `@Entity` va Spring Data `JpaRepository` joylashadi. Outbound port (masalan `LoadCustomerPort`) interfeysi yadroda e'lon qilinadi va `@Component` bilan belgilangan persistence adapter uni `JpaRepository` ustida implement qiladi; wiring esa `@Configuration` sinfidagi `@Bean` metodlari orqali bajariladi. Spring Framework 6.x'dagi `RestClient`/`WebClient` tashqi HTTP adapterlar uchun, `@ConfigurationProperties` esa adapter sozlamalari uchun ishlatiladi. Chegaralarni ArchUnit yoki Maven module bog'liqliklari bilan majburlash odatiy amaliyot.

**Qo'llanish keyslari:**
- Murakkab domen logikasi bo'lgan to'lov, kreditlash yoki sug'urta tizimlari.
- Bir xil use case'ni bir vaqtda REST, gRPC va message consumer orqali ochish kerak bo'lganda.
- Tashqi provayder (masalan to'lov shlyuzi yoki KYC servisi) yaqin kelajakda almashishi aniq bo'lsa.
- Domen qoidalarini DB va broker ko'tarmasdan, millisekundlarda unit test qilish talab qilinsa.
- Legacy integratsiyalarni asta-sekin anti-corruption adapterlar orqali izolyatsiya qilishda.

**Ehtiyot bo'ling:** Yupqa CRUD xizmatlar uchun bu uslub ortiqcha: har bir maydon uchun domen obyekti, DTO, entity va ikki mapper paydo bo'lib, foydali kodga nisbatan boilerplate ulushi keskin oshadi. Yana bir tuzoq — JPA entity'ni to'g'ridan-to'g'ri domen obyekti sifatida ishlatish: bu port'lar orqali hosil qilingan izolyatsiyani yashirin tarzda buzadi va lazy loading muammolarini yadroga olib kiradi.

## 12.3 Clean Architecture (Clean Architecture)

**Tavsif:** Hexagonal g'oyasini kontsentrik halqalar ko'rinishida rasmiylashtiradi: markazda Entities (domen qoidalari), keyin Use Cases, so'ng Interface Adapters, eng tashqarida Frameworks & Drivers. Asosiy qoida — Dependency Rule: source kod bog'liqligi faqat ichkariga qarab yo'naltirilishi shart, tashqi halqa nomlari ichki halqada hech qachon ko'rinmaydi. Qatlamlar o'rtasida ma'lumot oddiy struktura (DTO/record)lar orqali uzatiladi. Natijada biznes qoidalari UI, DB va framework hayot davridan uzoqroq yashaydi.

**Spring'da qayerda uchraydi:** Amalda `domain` (Java `record` va entity'lar), `application` (use case interfeyslari va ularning implementatsiyalari), `adapter-in-web`, `adapter-out-persistence` kabi Gradle subproject'lar sifatida tashkil etiladi; Spring faqat eng tashqi modullarda mavjud bo'ladi. Use case'lar bitta metodli interfeyslar (`CreateOrderUseCase`) sifatida yozilib, implementatsiyalari `@Service` va `@Transactional` bilan tashqi konfiguratsiyada bezatiladi. Java 17+ `record`, `sealed interface` va pattern matching ichki halqalarni ixcham va immutable ushlab turish uchun juda qulay. Spring Boot 3.x auto-configuration'i esa ataylab faqat `adapter`/`bootstrap` modullarida qoldiriladi.

**Qo'llanish keyslari:**
- Uzoq umr ko'rishi kutilayotgan yadroviy bank yoki billing platformasi.
- Bir nechta jamoa bir domen ustida ishlaganda, use case'lar aniq shartnoma rolini o'ynaydi.
- Framework migratsiyasi rejalashtirilgan tizimlar (masalan monolitdan modullarga o'tish).
- Regulyatsiya talab qiladigan biznes qoidalarni alohida, auditga tushunarli modulda saqlash.
- Domen logikasi uchun yuqori test qoplamasi (90%+) majburiy bo'lgan loyihalar.

**Ehtiyot bo'ling:** Clean Architecture'ni "har bir halqa uchun alohida model" deb mexanik tushunish mapping do'zaxiga olib keladi — 4 qatlamli mapping zanjirlari xatolar manbaiga aylanadi va ishlab chiqish tezligini pasaytiradi. Agar jamoa Dependency Rule'ni ArchUnit yoki modul chegaralari bilan majburlamasa, bir yildan keyin bu faqat paket nomlari qolgan oddiy layered arxitektura bo'lib chiqadi.

## 12.4 Piyoz arxitekturasi (Onion Architecture)

**Tavsif:** Clean Architecture'ning DDD'ga yaqin varianti: markazda Domain Model, uning ustida Domain Services, keyin Application Services, eng tashqarida Infrastructure va UI. Asosiy urg'u — infrastruktura (DB, ORM, messaging) hech qachon markazda emas, balki eng tashqi, almashtiriladigan halqada bo'lishi; repository interfeyslari domen ichida e'lon qilinadi. Hexagonal'dan farqi shundaki, Onion ichki halqalarni DDD terminlarida (Aggregate, Domain Service, Specification) aniq ajratadi. Bu uslub "database-centric" fikrlashdan "domain-centric" fikrlashga o'tishni rasmiylashtiradi.

**Spring'da qayerda uchraydi:** `OrderRepository` interfeysi domen paketida yashaydi, uning `JpaOrderRepository` implementatsiyasi esa infrastructure paketida Spring Data `JpaRepository` yoki `JdbcClient` (Spring Framework 6.1+) ustida yoziladi. Domen ichida `@DomainEvents`/`AbstractAggregateRoot` yoki Spring Modulith'ning `ApplicationEventPublisher` orqali domen hodisalari tarqatiladi. Application service'lar `@Service` + `@Transactional` bilan belgilanadi, infrastructure konfiguratsiyasi `@Configuration` sinflarida izolyatsiya qilinadi. `spring-boot-starter-validation` orqali input validatsiyasi tashqi halqada, biznes invariantlari esa aggregate ichida saqlanadi.

**Qo'llanish keyslari:**
- DDD bilan modellashtirilayotgan boy domen: logistika, trading, sug'urta polislari.
- Ko'p marta ishlatiladigan domen qoidalari bir nechta ilova (web + batch) tomonidan chaqirilsa.
- DB sxemasi domen modeliga mos kelmaydigan legacy bazalar ustida yangi logika qurishda.
- Domen modelini bazadan mustaqil, in-memory fake repository'lar bilan test qilish talab qilinganda.
- Monolitdan keyinchalik bounded context'larni ajratib olish rejasi bo'lganda.

**Ehtiyot bo'ling:** Onion va Clean/Hexagonal o'rtasidagi farqlar juda kichik, shuning uchun jamoada terminologiya urushiga aylanib, haqiqiy muammo — domen modelini boyitish — e'tibordan chetda qolishi mumkin. Agar domen halqasi JPA annotatsiyalari va lazy proxy'lar bilan to'lsa, "infrastructure tashqarida" degan asosiy va'da buziladi.

## 12.5 Vertikal qatlamli arxitektura (Vertical Slice Architecture)

**Tavsif:** Kod gorizontal texnik qatlamlar emas, balki feature (use case) bo'yicha vertikal "tilim"larga bo'linadi: har bir tilim o'z controller, handler, so'rov/javob modeli va DB kirishini o'zida saqlaydi. Maqsad — o'zgarishni bitta papkada lokalizatsiya qilish, ya'ni yangi funksiya qo'shganda 5 xil qatlamga tegmaslik. Tilimlar o'rtasida kodni majburan umumlashtirish ataylab minimallashtiriladi; takrorlanish bog'liqlikdan afzal deb hisoblanadi. Har bir tilim o'ziga mos murakkablik darajasini tanlashi mumkin — oddiy query uchun to'g'ridan-to'g'ri SQL, murakkab komanda uchun to'liq aggregate.

**Spring'da qayerda uchraydi:** `features/placeorder/PlaceOrderController.java`, `PlaceOrderHandler.java`, `PlaceOrderRequest.java` ko'rinishidagi paket tuzilishi; handler'lar `@Component` sifatida ro'yxatdan o'tadi. Mediator uslubi uchun Spring Framework 6.x'da o'z `CommandBus` abstraksiyasini `ObjectProvider`/generic `ResolvableType` orqali yozish yoki jmolecules/`spring-modulith` bilan birlashtirish keng tarqalgan; .NET'dagi MediatR'ning Java analoglari sifatida kichik kutubxonalar ishlatiladi, lekin ko'pincha 50 qatorli o'z bus'i yetarli bo'ladi. Query tilimlarida `JdbcClient` yoki jOOQ bilan to'g'ridan-to'g'ri proyeksiya o'qish qulay. Chegaralarni ArchUnit'ning `slices().matching("..features.(*)..")` qoidasi bilan tekshirish mumkin.

**Qo'llanish keyslari:**
- Ko'p mustaqil feature'li product-oriented jamoalar, har bir jamoa o'z tilimiga egalik qiladi.
- Read va write yo'llari juda farq qiladigan ilovalar (murakkab query'lar + sodda komandalar).
- Tez evolyutsiya qilayotgan SaaS mahsulotlari, bunda feature'lar qo'shiladi va o'chiriladi.
- Katta monolitni keyinchalik modullarga ajratishdan oldin feature chegaralarini aniqlashda.
- Ichki qatlamlararo abstraksiyalar foyda bermayotgan, "service → repository → service" zanjirlari ortiqcha bo'lgan loyihalarda.

**Ehtiyot bo'ling:** Umumiy biznes invariantlari bir necha tilimda takrorlansa, bitta qoidaning ikki xil versiyasi paydo bo'lib, nomuvofiqlik xatolari yuzaga keladi — shuning uchun haqiqiy domen qoidalari uchun umumiy domen moduli saqlanishi kerak. Shuningdek tilimlar o'rtasida DB jadvallarini erkin ulashish yashirin bog'lanish hosil qiladi va keyinchalik modullarni ajratishni qiyinlashtiradi.

## 12.6 Modulli monolit (Modular Monolith / Spring Modulith)

**Tavsif:** Ilova bitta deployment birligi (bir JAR, bir process) bo'lib qoladi, ammo ichida aniq chegaralangan, bir-biriga faqat e'lon qilingan API orqali murojaat qiluvchi modullardan iborat bo'ladi. Modullar o'z ichki modelini yashiradi va o'zaro aloqa uchun ko'pincha domen hodisalaridan foydalanadi, bu esa mikroservislarning tarqatilgan murakkabligisiz modullilik foydasini beradi. Chegaralar kompilyatsiya va test vaqtida avtomatik tekshiriladi, shuning uchun "monolit tartibsizligi" oldini olish mumkin. Kerak bo'lganda ayrim modul alohida servisga ajratilishi osonlashadi.

**Spring'da qayerda uchraydi:** Spring Modulith (1.2+/1.3+, Spring Boot 3.x bilan) bevosita shu uslub uchun yaratilgan: `ApplicationModules.of(App.class).verify()` bilan chegara buzilishlarini test sifatida tekshirish, `@ApplicationModule(allowedDependencies = ...)` bilan ruxsat etilgan bog'liqliklarni e'lon qilish, `@ApplicationModuleTest` bilan bitta modulni izolyatsiyada ko'tarish mumkin. Modullararo integratsiya `ApplicationEventPublisher` + `@ApplicationModuleListener` (transactional, async listener) orqali amalga oshiriladi; `spring-modulith-events-jpa` Event Publication Registry bilan hodisalarni ishonchli yetkazadi. `Documenter` sinfi PlantUML C4 diagrammalari va modul kanvasini generatsiya qiladi.

```java
@ApplicationModuleListener
void on(OrderCompleted event) {
    inventoryService.release(event.orderId());
}
```

**Qo'llanish keyslari:**
- Mikroservislarga o'tishdan oldingi oraliq bosqich: chegaralarni monolit ichida sinab ko'rish.
- O'rtacha hajmli jamoa (10-40 injener) bir kod bazasida ishlayotganda.
- Tranzaksion yaxlitlik muhim bo'lgan domenlar — bir DB tranzaksiyasi hali ham mumkin.
- Operatsion byudjet cheklangan startaplar: bitta deployment, bitta monitoring stack.
- Mikroservislardan "qaytish" (monolit konsolidatsiyasi) loyihalarida maqsadli arxitektura sifatida.

**Ehtiyot bo'ling:** Agar modullar bir xil DB sxemasidagi jadvallarni o'zaro erkin o'qisa, kodda modullilik bo'lsa ham ma'lumot darajasida qattiq bog'lanish saqlanadi — har bir modulga o'z jadval/sxemasi berilishi kerak. Yana bir tuzoq: `verify()` testini CI'ga qo'shmaslik, natijada chegaralar bir necha sprintdan keyin e'tiborsiz qolib buziladi.

## 12.7 Mikroyadro / Plugin arxitekturasi (Microkernel / Plugin Architecture)

**Tavsif:** Tizim minimal, barqaror yadro (core) va unga ulanadigan mustaqil plugin'lardan tashkil topadi; yadro faqat plugin'larni topish, yuklash va ularning kontraktini bajarishni biladi. Yangi imkoniyat yadroga tegmasdan, yangi plugin qo'shish bilan paydo bo'ladi, bu esa product customization va uchinchi tomon kengaytmalari uchun ideal. Plugin'lar odatda umumiy interfeys (extension point) va metadata orqali e'lon qilinadi. Yadro versiyasi barqaror, plugin'lar esa mustaqil evolyutsiya qiladi.

**Spring'da qayerda uchraydi:** Spring'ning o'zi shu uslubdan keng foydalanadi: `spring.factories`/`META-INF/spring/org.springframework.boot.autoconfigure.AutoConfiguration.imports` fayllari orqali auto-configuration plugin'lari topiladi, `@ConditionalOnClass`/`@ConditionalOnMissingBean` esa plugin aktivligini boshqaradi. O'z ilovangizda strategiya plugin'larini `List<PaymentProvider>` yoki `Map<String, PaymentProvider>` ko'rinishida inject qilish, yoki Java `ServiceLoader` va `module-info.java` (JPMS) bilan haqiqiy pluggability qurish mumkin. Spring Plugin (`spring-plugin-core`) kutubxonasi `Plugin<S>` interfeysi va `PluginRegistry` bilan aniq extension point modelini beradi — Spring Data REST shu asosda ishlaydi. Izolyatsiyalangan class loading kerak bo'lsa, PF4J yoki OSGi (Apache Karaf) tanlanadi.

**Qo'llanish keyslari:**
- Mijozga xos biznes qoidalari ko'p bo'lgan korporativ mahsulotlar (ERP, CRM moslashtirishlari).
- To'lov/yetkazib berish provayderlarini plugin sifatida qo'shiladigan e-commerce platformalari.
- Hujjat yoki fayl formatlari uchun kengaytiriladigan import/export konvertorlari.
- Qoidalar dvigateli (rules engine) uchun strategiya plugin'lari, har biri mustaqil deploy qilinadi.
- IDE/CI kabi developer tooling, uchinchi tomon kengaytmalarini qo'llab-quvvatlovchi.

**Ehtiyot bo'ling:** Plugin kontraktini noto'g'ri loyihalash eng katta xavf: interfeys juda tor bo'lsa plugin'lar yadroni "aylanib o'tish" uchun hack qiladi, juda keng bo'lsa har bir o'zgarish barcha plugin'larni buzadi. Bir JVM'da ishlayotgan plugin'lar xotira, thread va exception darajasida izolyatsiyalanmagan — ishonchsiz uchinchi tomon kodi uchun alohida class loader yoki process kerak.

## 12.8 Quvurlar va filtrlar (Pipes and Filters)

**Tavsif:** Ishlov berish mustaqil, holatsiz filter'lar ketma-ketligiga bo'linadi; har biri kirish oqimini o'zgartirib, natijani keyingi filter'ga quvur (pipe) orqali uzatadi. Filter'lar bir-biri haqida bilmaydi, faqat ma'lumot formatiga kelishadi, shuning uchun ularni qayta tartiblash, qayta ishlatish va parallellashtirish oson. Bu uslub ETL, media transkodlash va message transformation uchun tabiiy. Quvur in-memory kolleksiya, reactive stream yoki haqiqiy message queue bo'lishi mumkin.

**Spring'da qayerda uchraydi:** Spring Integration bevosita shu uslub ustiga qurilgan: `MessageChannel` (pipe), `@Transformer`, `@Filter`, `@ServiceActivator` (filterlar) va `IntegrationFlow` DSL (`IntegrationFlows.from(...).transform(...).filter(...).handle(...)`). Spring Batch'da `ItemReader → ItemProcessor → ItemWriter` zanjiri va `CompositeItemProcessor` aynan pipeline modelini beradi. Reactive stack'da Project Reactor `Flux` operatorlari (`map`, `filter`, `flatMap`, `buffer`) in-memory pipeline sifatida ishlaydi, Spring Cloud Stream esa Kafka/RabbitMQ orqali tarqatilgan quvurlarni `Function<Flux<T>, Flux<R>>` bean'lari bilan birlashtiradi. Servlet qatlamida `jakarta.servlet.Filter` va Spring Security'ning `SecurityFilterChain` ham shu patternning klassik ko'rinishi.

**Qo'llanish keyslari:**
- Kunlik ETL: fayl o'qish → validatsiya → boyitish → DB'ga yozish (Spring Batch).
- EDI/SWIFT/HL7 xabarlarini bosqichma-bosqich normalizatsiya qilish (Spring Integration).
- Kafka'dagi event oqimini filtrlash va boyitib boshqa topic'ga chiqarish.
- Rasm/video yuklash pipeline'i: virus skaner → o'lcham o'zgartirish → CDN'ga joylash.
- HTTP so'rovlari uchun kesishgan mas'uliyatlar zanjiri: auth → rate limit → audit log.

**Ehtiyot bo'ling:** Ko'p bosqichli quvurda xatolarni boshqarish va idempotentlik eng murakkab qism — qaysi bosqichda qayta urinish, qaysi birida dead-letter'ga yuborish aniq loyihalanmasa, ma'lumot yo'qolishi yoki dublikatlar paydo bo'ladi. Shuningdek har bir bosqich holatsiz bo'lishi kerak; filter'lar orasida yashirin umumiy mutable holat paydo bo'lsa, parallellashtirish va kuzatuvchanlik buziladi.

## 12.9 Hodisaga asoslangan arxitektura (Event-Driven Architecture — broker va mediator topologiyalari)

**Tavsif:** Komponentlar bir-birini to'g'ridan-to'g'ri chaqirmaydi, balki sodir bo'lgan faktlar — hodisalar orqali aloqa qiladi, bu esa vaqt va joy bo'yicha ajralishni (temporal/spatial decoupling) beradi. Broker topologiyasida hodisa shunchaki broker'ga chiqariladi va qiziqqan har bir consumer o'zi reaksiya qiladi — markaziy orkestrator yo'q, maksimal moslashuvchanlik, lekin oqimni kuzatish qiyin. Mediator topologiyasida esa markaziy mediator (yoki orchestrator) ko'p bosqichli jarayonni boshqaradi, kompensatsiya va xato holatlarini biladi. Ko'p tizimlar ikkisini birga ishlatadi: lokal reaksiyalar uchun broker, biznes saga'lari uchun mediator.

**Spring'da qayerda uchraydi:** Process ichida `ApplicationEventPublisher`, `@EventListener`, `@TransactionalEventListener(phase = AFTER_COMMIT)` va `@Async` broker-uslubidagi publish/subscribe beradi. Tarqatilgan holatda `@KafkaListener` (`spring-kafka`), `@RabbitListener` (`spring-amqp`), yoki Spring Cloud Stream binder'lari ishlatiladi; ishonchli publikatsiya uchun Spring Modulith'ning Event Publication Registry yoki transactional outbox pattern qo'llanadi. Mediator topologiyasi uchun Spring Integration'ning `IntegrationFlow`/router'lari, Spring Statemachine, yoki Camunda/Temporal kabi tashqi workflow dvigatellari bilan integratsiya tanlanadi. Kuzatuvchanlik Micrometer Tracing (Spring Boot 3.x) orqali hodisalar bo'ylab trace context tarqatish bilan ta'minlanadi.

**Qo'llanish keyslari:**
- Buyurtma yaratilganda ombor, to'lov va bildirishnoma xizmatlarini mustaqil ishga tushirish.
- Audit va analitika uchun domen hodisalarini data lake'ga oqizish.
- Mikroservislar o'rtasidagi tarqatilgan tranzaksiyalarni saga sifatida boshqarish (mediator).
- IoT yoki telemetriya oqimlarini real vaqtda qayta ishlash va alert generatsiya qilish.
- Legacy tizimni "hodisalar bilan o'rash" — strangler fig migratsiyasida.

**Ehtiyot bo'ling:** Broker topologiyasida biznes jarayonining to'liq oqimi hech bir joyda yozilmagan bo'ladi — debugging va xato tahlili uchun kuchli tracing, correlation ID va event katalogi bo'lmasa, tizim "tushunarsiz" holatga keladi. Eventual consistency'ni mahsulot talablari bilan kelishmasdan tanlash ham tipik xato: foydalanuvchi darhol ko'rishi kerak bo'lgan natijani asinxron hodisaga topshirish UX muammolari va ikki marta yuborilgan buyurtmalarga olib keladi.

## 12.10 Buyruq va so'rovlar mas'uliyatini ajratish (CQRS — Command Query Responsibility Segregation)

**Tavsif:** Yozish (command) va o'qish (query) yo'llari turli modellar, ba'zan turli ma'lumotlar bazalari bilan amalga oshiriladi. Command modeli biznes invariantlarini himoya qiladi va normalizatsiyalangan bo'ladi, query modeli esa UI ehtiyojiga moslashtirilgan denormalizatsiyalangan proyeksiyalardan iborat. Bu ikki yo'lni mustaqil optimallashtirish va mustaqil masshtablash imkonini beradi. Oddiy shaklda bu faqat kod darajasidagi ajratish (bir DB), kuchli shaklda — alohida read store va asinxron proyeksiya yangilash.

**Spring'da qayerda uchraydi:** Eng ko'p uchraydigan amaliy ko'rinish: yozish uchun JPA/Hibernate aggregate'lari (`@Entity`, `EntityManager`), o'qish uchun `JdbcClient`, `NamedParameterJdbcTemplate` yoki jOOQ bilan to'g'ridan-to'g'ri proyeksiya DTO'lari — Spring Data'ning interface-based projection'lari (`List<OrderSummary> findBy...`) ham shu maqsadda ishlatiladi. Read store sifatida Elasticsearch (`spring-data-elasticsearch`) yoki Redis (`spring-data-redis`) ishlatilganda, proyeksiyalar `@TransactionalEventListener` yoki Kafka consumer'lari orqali yangilanadi. Spring Modulith'ning `@ApplicationModuleListener` proyeksiya yangilashni ishonchli (transactional outbox bilan) bajarish uchun qulay. Axon Framework'ning Spring Boot starter'i to'liq CQRS infratuzilmasini (`@CommandHandler`, `@QueryHandler`) beradi.

**Qo'llanish keyslari:**
- O'qish yuklamasi yozishdan o'n-yuz marta ko'p bo'lgan katalog yoki dashboard tizimlari.
- Murakkab qidiruv va filtrlash talab qilinadigan UI'lar, bunda normallashtirilgan sxema sekin.
- Bir domen ustida juda ko'p turli hisobot ko'rinishlari kerak bo'lganda.
- Yozish tomoni qat'iy invariantlarga ega bo'lgan moliyaviy operatsiyalar + tez reporting.
- Event sourcing bilan birga: hodisalardan bir nechta ixtisoslashgan proyeksiya qurish.

**Ehtiyot bo'ling:** Alohida read store tanlash bilan siz avtomatik ravishda eventual consistency'ni qabul qilasiz — "saqlagandan keyin ro'yxatda ko'rinmaydi" muammosi UX va test darajasida oldindan hal qilinishi kerak. Oddiy CRUD domenida to'liq CQRS ortiqcha: ikki model, sinxronizatsiya kodi va qo'shimcha infratuzilma qo'llab-quvvatlash xarajatini keskin oshiradi, shuning uchun avval bir DB ichidagi yengil ajratishdan boshlash to'g'ri.

## 12.11 Hodisalarni saqlash (Event Sourcing)

**Tavsif:** Tizim holati joriy snapshot ko'rinishida emas, balki sodir bo'lgan o'zgarmas hodisalar ketma-ketligi sifatida saqlanadi; joriy holat shu hodisalarni qayta o'ynatish (replay) orqali tiklanadi. Bu to'liq audit tarixi, vaqt bo'ylab orqaga qaytish (temporal query) va bir xil tarixdan yangi proyeksiyalar qurish imkonini beradi. Ishlash uchun snapshot'lar, optimistic concurrency (stream versiyasi) va hodisa sxemasi evolyutsiyasi mexanizmlari zarur. Deyarli har doim CQRS bilan birga ishlatiladi, chunki event stream'dan to'g'ridan-to'g'ri o'qish amaliy emas.

**Spring'da qayerda uchraydi:** Spring'da tayyor event store yo'q, shuning uchun Axon Framework (Spring Boot starter, `@Aggregate`, `@EventSourcingHandler`, `AggregateLifecycle.apply()`) yoki EventStoreDB'ning Java client'i tanlanadi; ko'p jamoalar esa oddiy `events` jadvalini `JdbcClient`/JPA bilan o'zlari quradi (aggregate_id, version, type, payload, unique(aggregate_id, version)). Hodisalarni tashqariga ishonchli chiqarish uchun transactional outbox yoki Debezium CDC + Kafka ishlatiladi. Proyeksiyalar Spring'ning `@TransactionalEventListener` yoki `@KafkaListener` bean'lari bilan yangilanadi. Jackson `@JsonTypeInfo` va versiyalangan payload sinflari sxema evolyutsiyasini boshqarish uchun qo'llanadi.

**Qo'llanish keyslari:**
- Bank hisobvaraqlari va ledger tizimlari, bunda har bir o'zgarish sababini bilish shart.
- Regulyativ audit talab qiladigan sug'urta polisi yoki tibbiy yozuvlar tarixi.
- Murakkab holat mashinalari: buyurtma hayot sikli, logistika yuk harakati.
- Biznes analitikasi uchun o'tmishdagi ma'lumotlardan yangi proyeksiyalar qurish zaruriyati.
- Nizolarni hal qilish va "nima bo'lgan edi?" savollariga aniq javob kerak bo'lgan domenlar.

**Ehtiyot bo'ling:** Eng katta xavf — hodisa sxemasining evolyutsiyasi: hodisalar abadiy saqlanadi, shuning uchun eski versiyalarni o'qish (upcasting) strategiyasi birinchi kundan kerak, aks holda bir yildan keyin replay ishlamay qoladi. Shuningdek GDPR'dagi "o'chirish huquqi" immutable log bilan ziddiyatda (crypto-shredding talab qiladi), va bu uslubni oddiy CRUD domenga qo'llash jamoani sezilarli operatsion murakkablik bilan yuklaydi — faqat haqiqatan tarix biznes qiymatiga ega bo'lganda tanlang.

## 12.12 Mikroservislar (Microservices)

**Tavsif:** Tizim mustaqil deploy qilinadigan, o'z ma'lumot bazasiga ega bo'lgan kichik servislarga bo'linadi va ular tarmoq orqali (HTTP/gRPC yoki message broker) muloqot qiladi. Bu uslub katta monolitning deploy bog'liqligi, jamoalar o'rtasidagi kod to'qnashuvi va bitta komponentni alohida scale qilish imkonsizligi muammolarini hal qiladi. Har bir servis o'z bounded context'iga egalik qiladi, shuning uchun Domain-Driven Design bilan birga qo'llanadi. Buning narxi — tarmoq ishonchsizligi, taqsimlangan tranzaksiyalar va operatsion murakkablik.

**Spring'da qayerda uchraydi:** Har bir servis alohida Spring Boot 3.x/4.x ilovasi bo'ladi; servislar aro chaqiruvlar uchun `RestClient` (Spring Framework 6.1+), `WebClient` yoki `@HttpExchange` bilan deklarativ HTTP interface (`HttpServiceProxyFactory`); service discovery uchun `spring-cloud-starter-netflix-eureka-client` yoki Kubernetes'da `spring-cloud-starter-kubernetes-client-discovery`; konfiguratsiya uchun `spring-cloud-starter-config`; chidamlilik uchun `spring-cloud-starter-circuitbreaker-resilience4j` va `@CircuitBreaker`; API Gateway uchun `spring-cloud-gateway` (`RouteLocator`, `GatewayFilter`); kuzatuv uchun Micrometer Tracing (`io.micrometer:micrometer-tracing-bridge-otel`) va `management.tracing.sampling.probability`.

**Qo'llanish keyslari:**
- Marketplace platformasida katalog, buyurtma, to'lov va yetkazib berish servislari alohida jamoalar tomonidan mustaqil relizlanadi.
- Qora juma kunida faqat `checkout-service` 50 podga scale qilinadi, qolgan servislar o'z o'lchamida qoladi.
- Bank'da legacy core'ni bosqichma-bosqich almashtirishda yangi funksiyalar alohida servis sifatida yoziladi (Strangler Fig).
- Fraud detection servisi Python/ML stack'da, qolgan tizim Java'da — texnologiya tanlovi servis darajasida bo'linadi.
- SaaS mahsulotida har bir jamoa kuniga bir necha marta o'z servisini deploy qiladi va boshqa jamoalarni kutmaydi.

**Ehtiyot bo'ling:** Mikroservislarni tashkiliy tayyorlik (CI/CD, observability, on-call) bo'lmaganda joriy qilish "distributed monolith"ga olib keladi — servislar bir vaqtda deploy qilinishi shart bo'lib qoladi va kechikish ortadi. Bir nechta servis bitta ma'lumot bazasiga yozsa yoki servislar aro sinxron zanjir 3-4 qatlamdan oshsa, siz mikroservis emas, taqsimlangan tranzaksiyali tuzoq qurgan bo'lasiz.

## 12.13 O'z-o'ziga Yetarli Tizimlar (Self-Contained Systems)

**Tavsif:** Tizim bir nechta yirik, vertikal to'liq (UI + logika + ma'lumot bazasi) mustaqil ilovaga bo'linadi va ular bir-biriga asosan asinxron yoki UI darajasida integratsiya qilinadi. Har bir SCS o'z web UI'siga ega bo'ladi, shuning uchun sinxron servis-servis chaqiruvlari minimumga tushadi va mikroservislarning tarmoq murakkabligidan qochiladi. Integratsiya ustuvorligi: UI havolalari → asinxron replikatsiya → eng oxirida sinxron API. Bu mikroservis va monolit o'rtasidagi "o'rta yo'l" uslubi.

**Spring'da qayerda uchraydi:** Har bir SCS to'liq Spring Boot ilovasi bo'ladi: `spring-boot-starter-web` + server-side rendering uchun Thymeleaf (`spring-boot-starter-thymeleaf`) yoki JTE, o'z `DataSource`/Flyway migratsiyalari bilan. SCS'lar aro integratsiya uchun `spring-kafka` (`@KafkaListener`) yoki `spring-boot-starter-amqp` orqali event replikatsiyasi; UI kompozitsiyasi uchun `spring-cloud-gateway` yoki Edge Side Includes (nginx SSI); keshlangan ma'lumot nusxalari uchun `@Cacheable` va Caffeine/Redis.

**Qo'llanish keyslari:**
- Yirik e-commerce'da "Search", "Product", "Checkout", "Account" har biri o'z UI'si bilan mustaqil tizim bo'ladi.
- Insurance kompaniyasida "Polis sotish" va "Da'volar" tizimlari alohida jamoalarga, alohida relizga ega.
- Bir nechta mustaqil jamoa bitta portalda ishlaydi, lekin umumiy deploy oynasini kutishni xohlamaydi.
- Davlat xizmatlari portali: har bir xizmat moduli alohida tizim, umumiy faqat SSO va dizayn tizimi.
- Monolitdan chiqishda 50 ta mikroservis o'rniga 5 ta vertikal tizimga bo'lish tanlanadi.

**Ehtiyot bo'ling:** SCS'lar orasida ma'lumotni replikatsiya qilish zarur bo'lgani uchun eventual consistency bilan yashashga tayyor bo'lishingiz kerak; agar jamoalar sinxron API'larga qayta tushib ketsa, uslubning asosiy foydasi yo'qoladi. UI'da umumiy dizayn tizimi versiyalanmasa, foydalanuvchi bir portalda bir nechta "boshqa" ilovani ko'radi.

## 12.14 Servisga Yo'naltirilgan Arxitektura (Service-Oriented Architecture, SOA)

**Tavsif:** Korporativ funksiyalar qayta ishlatiladigan, shartnoma (contract) asosidagi servislar sifatida e'lon qilinadi va ularni markazlashgan integratsiya qatlami — Enterprise Service Bus — bog'laydi, yo'naltiradi va formatlarini o'giradi. Bu heterogen legacy tizimlarni (mainframe, ERP, CRM) yagona korporativ qatlam orqali bog'lash muammosini hal qiladi. Mikroservislardan farqi: servislar yirikroq, ma'lumot bazasi ko'pincha umumiy, orkestratsiya markazda (BPEL/ESB) bo'ladi. Governance va servis reyestri markaziy ahamiyatga ega.

**Spring'da qayerda uchraydi:** Spring Web Services (`spring-ws-core`) bilan contract-first SOAP endpoint'lari: `@Endpoint`, `@PayloadRoot`, `MessageDispatcherServlet`, WSDL generatsiyasi uchun `DefaultWsdl11Definition`, XSD'dan JAXB sinflari; klient tomonda `WebServiceTemplate`. Integratsiya va routing uchun Spring Integration (`IntegrationFlow`, `@ServiceActivator`, `MessageChannel`) yoki Apache Camel'ning `camel-spring-boot-starter`'i; xabar almashinuvi uchun JMS (`JmsTemplate`, `@JmsListener`) va IBM MQ/ActiveMQ. Tranzaksion integratsiya uchun `JtaTransactionManager` (Jakarta EE serverida yoki Narayana bilan).

**Qo'llanish keyslari:**
- Bankda mainframe'dagi hisob ma'lumotlari ESB orqali SOAP servis sifatida internet-banking va mobil ilovaga beriladi.
- Telekom operatorida bitta "mijozni ulash" jarayoni 6 ta backend tizimni ESB orqali orkestratsiya qiladi.
- Sug'urta kompaniyasi davlat reyestrlari bilan WS-Security talab qiladigan SOAP shartnomalar orqali integratsiyalashadi.
- ERP (SAP) va CRM o'rtasida kanonik ma'lumot modeliga o'girish Camel route'lari bilan amalga oshiriladi.
- Regulyator tomonidan WSDL/XSD shartnoma majburiy bo'lgan B2B integratsiyalar.

**Ehtiyot bo'ling:** ESB markaziy "single point of failure" va tashkiliy tiqilinchga aylanishi mumkin — har bir o'zgarish integratsiya jamoasi navbatidan o'tadi. Yangi loyihada SOAP/ESB'ni "korporativ standart" deb tanlash ko'pincha ortiqcha: REST/event-driven yetarli bo'lgan joyda XML transformatsiyalari va governance narxini to'lamang.

## 12.15 Serverless / FaaS (Serverless / Function as a Service)

**Tavsif:** Biznes logika qisqa yashovchi, holatsiz funksiyalar sifatida yoziladi va platforma ularni so'rov yoki hodisa kelganda ishga tushiradi, bo'sh turganda nolga qisqartiradi. Bu kapasitet rejalashtirish, server boshqaruvi va notekis yuklamada ortiqcha xarajat muammolarini hal qiladi. Scaling, ishga tushirish va to'lov granulyarligi platforma zimmasida bo'ladi. Qarshi tomoni — cold start, vaqt limitlari va vendor platformasiga bog'lanish.

**Spring'da qayerda uchraydi:** Spring Cloud Function biznes logikani oddiy `java.util.function.Function`, `Supplier` yoki `Consumer` bean sifatida yozishga imkon beradi va uni HTTP, Kafka yoki cloud trigger'lariga bog'laydi (`spring.cloud.function.definition`, `FunctionCatalog`). Adapterlar: `spring-cloud-function-adapter-aws` (`FunctionInvoker` handler), Azure va GCP adapterlari. Cold start uchun Spring Boot 3.x'ning GraalVM native image qo'llab-quvvatlashi (`spring-boot-maven-plugin` `native` profili, `@RegisterReflectionForBinding`) yoki Class Data Sharing (`-XX:SharedArchiveFile`, Spring Boot 3.3+ CDS qo'llab-quvvatlashi) ishlatiladi. Knative/Kubernetes'da esa oddiy Spring Boot web ilovasi nolga scale bo'ladi.

```java
@Bean
public Function<OrderEvent, Receipt> handleOrder(PricingService pricing) {
    return event -> pricing.priceAndStore(event);
}
```

**Qo'llanish keyslari:**
- S3'ga yuklangan fayl uchun thumbnail generatsiya qiluvchi funksiya kuniga bir necha ming marta ishlaydi.
- Kunda bir marta ishlaydigan hisobot eksport jarayoni doimiy pod o'rniga funksiya sifatida yuritiladi.
- Webhook qabul qiluvchi endpoint (to'lov provayderi callback'i) notekis trafikda avtomatik scale bo'ladi.
- Kafka topic'dan kelgan hodisalarni boyitib boshqa topic'ga yozadigan yengil transformator.
- Chat-bot yoki IoT telemetriya uchun qisqa, holatsiz qayta ishlash qadamlari.

**Ehtiyot bo'ling:** JVM cold start sovuq chaqiruvda yuzlab millisekunddan bir necha sekundgacha cho'zilishi mumkin — latency sezgir, doimiy trafikli API'ni FaaS'ga ko'chirish odatda noto'g'ri qaror. Funksiya ichida ulanish pool'i, uzoq tranzaksiya yoki holat saqlashga tayanmang: funksiya har qanday vaqtda to'xtatilishi va parallel nusxada qayta ishga tushishi mumkin.

## 12.16 Kosmosga Asoslangan Arxitektura (Space-Based Architecture)

**Tavsif:** Ma'lumot bazasi o'rniga markaziy nuqtaga replikatsiya qilinadigan taqsimlangan in-memory data grid ("tuple space") ishlatiladi va processing unit'lar shu grid bilan ishlaydi. Bu juda yuqori, oldindan aytib bo'lmaydigan concurrent yuklamada ma'lumot bazasi bo'g'iz bo'lib qolishi muammosini hal qiladi. Yozuvlar grid'ga tushadi, asinxron "data pump" orqali esa doimiy saqlashga oqib boradi, shuning uchun o'qish va yozish RAM tezligida bo'ladi. Narxi — murakkab consistency, cache invalidation va xotira sig'imi cheklovlari.

**Spring'da qayerda uchraydi:** Hazelcast (`hazelcast-spring`, `HazelcastInstance`, `IMap`, `spring-boot-starter-cache` bilan `HazelcastCacheManager`) yoki Apache Ignite'ning Spring integratsiyasi (`IgniteSpringBean`, `SpringCacheManager`); Redis ishlatilsa `spring-boot-starter-data-redis` va `RedisTemplate`. Keshni deklarativ boshqarish uchun `@EnableCaching`, `@Cacheable`, `@CacheEvict`; sessiyani grid'ga ko'chirish uchun Spring Session (`spring-session-hazelcast` yoki `spring-session-data-redis`). Grid'dan ma'lumot bazasiga asinxron oqim uchun `spring-kafka` va `@KafkaListener` bilan yozuvchi batch jarayonlar.

**Qo'llanish keyslari:**
- Konsert chiptalari sotuvi sekundda o'n minglab urinishni ko'taradi va o'rindiq holati grid'da saqlanadi.
- Onlayn garov (betting) platformasida koeffitsiyentlar va stavkalar in-memory grid'da yangilanadi.
- Trading tizimida order book RAM'da turadi, savdo tarixi asinxron ravishda bazaga yoziladi.
- Flash-sale e-commerce aksiyasida stok hisobi `IMap` ustida atomik operatsiyalar bilan yuritiladi.
- Yuqori hajmli real-time reyting/leaderboard hisob-kitobi.

**Ehtiyot bo'ling:** Oddiy CRUD ilovaga bu uslubni qo'llash ortiqcha — grid replikatsiyasi, split-brain va cache-to-database oqimining nosozligi tufayli ma'lumot yo'qolishi riski real. Grid'dagi barcha ma'lumot RAM'da yashashini va node yo'qolganda qayta taqsimlanishini (rebalance paytidagi latency sakrashini) hisobga olmasa, tizim eng kerakli daqiqada sekinlashadi.

## 12.17 Klient-Server (Client-Server)

**Tavsif:** Tizim so'rov yuboruvchi klientlar va ularni qayta ishlovchi markazlashgan serverga bo'linadi; biznes logika va ma'lumot serverda, taqdimot klientda bo'ladi. Bu umumiy ma'lumotga ko'p foydalanuvchining nazoratli kirishini va mantiqni bitta joyda yangilashni ta'minlaydi. Ko'pchilik web va mobil ilovalar — shu uslubning zamonaviy ko'rinishi (two-tier yoki uch qatlamli variantda). Aloqa odatda so'rov-javob protokoli (HTTP, JDBC, gRPC) ustida quriladi.

**Spring'da qayerda uchraydi:** Server tomoni: `spring-boot-starter-web` (Servlet, Tomcat) yoki `spring-boot-starter-webflux` (Netty), `@RestController`, `@GetMapping`, `HttpMessageConverter`, autentifikatsiya uchun `spring-boot-starter-security` (`SecurityFilterChain`, `@EnableWebSecurity`, OAuth2 Resource Server). Klient tomoni Java'da: `RestClient`, `WebClient`, yoki `@HttpExchange` interface'lari. Ma'lumot bazasi — klient-server munosabatining ikkinchi qatlami: `DataSource` (HikariCP), `JdbcClient`, `spring-boot-starter-data-jpa`.

**Qo'llanish keyslari:**
- React SPA Spring Boot REST API bilan ishlaydi, autentifikatsiya JWT orqali.
- Mobil ilova (iOS/Android) bitta backend API'ga murojaat qiladi.
- Korxona ichidagi desktop JavaFX mijozi markaziy Spring Boot serveriga ulanadi.
- IoT qurilmalari telemetriyani markaziy qabul qiluvchi servisga yuboradi.
- Ichki admin paneli umumiy ma'lumot bazasiga faqat server orqali kirish beradi.

**Ehtiyot bo'ling:** Server yagona nosozlik nuqtasi bo'lgani uchun horizontal scaling va stateless dizayn (sessiyani serverda saqlamaslik) boshidan rejalashtirilishi kerak. Biznes qoidalarini klientga ko'chirib qo'ymang — validatsiya va avtorizatsiya har doim serverda takrorlanishi shart, aks holda klientni o'zgartirgan har kim qoidani chetlab o'tadi.

## 12.18 Broker (Broker)

**Tavsif:** Klient va servis bir-birini bilmaydi: o'rtada broker turib, so'rovni mavjud servisga topib yo'naltiradi, javobni qaytaradi yoki xabarni mos iste'molchilarga yetkazadi. Bu komponentlarni manzil, joylashuv va mavjudlik bo'yicha decoupling qilish, shuningdek dinamik topologiyani qo'llab-quvvatlash muammosini hal qiladi. Zamonaviy ko'rinishi — message broker (Kafka, RabbitMQ) va unga asoslangan publish/subscribe yoki ish navbati. Broker yana retry, buffering va monitoring uchun yagona nuqta beradi.

**Spring'da qayerda uchraydi:** `spring-boot-starter-amqp` bilan RabbitMQ: `RabbitTemplate`, `@RabbitListener`, `Queue`/`TopicExchange`/`Binding` bean'lari, `DirectMessageListenerContainer`. Kafka uchun `spring-kafka`: `KafkaTemplate`, `@KafkaListener`, `ConcurrentKafkaListenerContainerFactory`, `DefaultErrorHandler` va `DeadLetterPublishingRecoverer`. Broker'dan abstraktsiya uchun Spring Cloud Stream (`spring-cloud-stream-binder-kafka`/`-rabbit`, funksional binding `spring.cloud.stream.bindings.*`). JMS uchun `JmsTemplate` va `@JmsListener`; WebSocket STOMP broker relay uchun `@EnableWebSocketMessageBroker` va `MessageBrokerRegistry`.

**Qo'llanish keyslari:**
- Buyurtma yaratilganda `OrderCreated` xabari broker'ga tushadi, uni ombor, hisob-faktura va notification servislari mustaqil o'qiydi.
- Og'ir PDF generatsiya ishlari navbatga qo'yiladi va worker'lar pool'i ularni iste'mol qiladi.
- Legacy tizim ishlamay turganda xabarlar navbatda saqlanadi va keyin qayta ishlanadi.
- Chat ilovasida xabarlar STOMP broker orqali obunachilarga tarqatiladi.
- Audit hodisalari bitta topic'ga yoziladi va bir nechta analitik iste'molchi tomonidan o'qiladi.

**Ehtiyot bo'ling:** Broker ko'rinmas markaziy bog'liqlikka aylanadi — uning to'xtashi butun tizimni to'xtatadi, shuning uchun klasterlash, dead-letter queue va idempotent consumer'lar majburiy. "At-least-once" yetkazish sababli bir xabar bir necha marta kelishi mumkin; iste'molchi idempotent bo'lmasa, dublikat buyurtma yoki ikki marta to'lov yuzaga keladi.

## 12.19 Teng-Tengga (Peer-to-Peer)

**Tavsif:** Markaziy server o'rniga har bir node bir vaqtning o'zida klient ham, server ham bo'ladi va resurslarni bevosita o'zaro almashadi. Bu markaziy bo'g'iz, yagona nosozlik nuqtasi va markaziy infratuzilma narxi muammolarini hal qiladi. Node'lar bir-birini discovery (gossip, DHT yoki seed ro'yxati) orqali topadi va ma'lumot replikasi tarmoq bo'ylab tarqaladi. Narxi — murakkab consistency, xavfsizlik va topologiyani kuzatish qiyinligi.

**Spring'da qayerda uchraydi:** Spring ilovalari ko'pincha P2P'ni cluster kutubxonasi orqali oladi: Hazelcast embedded rejimida (`hazelcast-spring`, `HazelcastInstance`) node'lar teng a'zo sifatida gossip bilan klaster quradi; Infinispan'ning `infinispan-spring-boot3-starter`'i JGroups ustida ishlaydi. Eureka server'lar peer-to-peer replikatsiya qiladi (`eureka.client.service-url.defaultZone` bir nechta peer bilan). Blockchain/DLT integratsiyasida esa Spring Boot ilovasi Web3j (`web3j-spring-boot-starter` yoki `core` kutubxonasi) orqali P2P tarmoq node'iga ulanadi. Shuni ta'kidlash kerak: Spring Framework'ning o'zida maxsus P2P moduli yo'q.

**Qo'llanish keyslari:**
- Bir nechta Spring Boot instance embedded Hazelcast bilan umumiy keshni teng a'zolar sifatida ushlab turadi.
- Eureka server'larning o'zaro replikatsiyasi bilan discovery qatlami markaziy masterdan xoli bo'ladi.
- Blockchain hamyoni yoki tranzaksiya monitoringi uchun backend Ethereum node'iga ulanadi.
- Edge joylashuvlardagi node'lar markaziy serverga bog'liq bo'lmay o'zaro sinxronlanadi.
- Katta fayl tarqatish (CDN o'rniga ichki P2P tarqatish) bilan deploy artefaktlarini yoyish.

**Ehtiyot bo'ling:** P2P klasterni Kubernetes kabi dinamik muhitda ishlatganda split-brain va noto'g'ri discovery eng ko'p uchraydigan tuzoq — multicast o'rniga aniq peer ro'yxati yoki Kubernetes discovery plugin'ini ishlatish kerak. Agar sizga tranzaksion, qat'iy consistency kerak bo'lsa, P2P replikatsiyaga tayanmang; markaziy ma'lumot bazasi soddaroq va xatolari oldindan bilinadi.

## 12.20 Qoratakhta (Blackboard)

**Tavsif:** Umumiy bilim omborida ("blackboard") muammoning joriy holati saqlanadi, mustaqil mutaxassis modullar ("knowledge sources") undan o'qib, o'z hissasini qo'shadi, controller esa qaysi modul keyingi navbatda ishlashini tanlaydi. Bu aniq algoritmi yo'q, bosqichma-bosqich gipotezalarni to'plash orqali hal qilinadigan masalalar (nutqni tanish, tasvirni tushunish, murakkab tashxis) uchun mo'ljallangan. Modullar bir-birini bilmaydi, faqat blackboard ustida bilvosita muloqot qiladi. Yakuniy natija — gipotezalar yetarli ishonch darajasiga yetganda qabul qilinadi.

**Spring'da qayerda uchraydi:** Standart Spring moduli yo'q, lekin uslub tipik ravishda shunday quriladi: umumiy holat Redis (`RedisTemplate`) yoki Hazelcast `IMap`da saqlanadi; knowledge source'lar bitta interface'ni amalga oshiruvchi bean'lar bo'lib, Spring ularni `List<KnowledgeSource>` sifatida inject qiladi va `@Order` bilan tartiblaydi; controller `ApplicationEventPublisher`/`@EventListener` yoki Spring Integration `MessageChannel` orqali ishga tushirish siklini boshqaradi. Qoidalar dvigateli kerak bo'lsa Drools (`drools-core` + Spring Boot bilan `KieContainer` bean) ishlatiladi; parallel ishlash uchun `@Async` va `ThreadPoolTaskExecutor`.

**Qo'llanish keyslari:**
- Tibbiy tashxis yordamchisida laboratoriya, tasvir va anamnez modullari umumiy gipoteza to'plamini boyitadi.
- Fraud scoring'da bir nechta mustaqil detektor bitta tranzaksiya bo'yicha signal qo'shadi va yakuniy qaror shundan chiqadi.
- Hujjatni tushunish quvuri: OCR, til aniqlash, entity extraction va validatsiya modullari ketma-ket emas, ishonch darajasiga qarab ishlaydi.
- Sensor fusion: bir nechta IoT manba ma'lumotidan qurilma holati haqida yagona xulosa qurish.
- Reja/marshrut optimizatsiyasida turli evristikalar umumiy yechim nomzodlarini yaxshilab boradi.

**Ehtiyot bo'ling:** Blackboard juda kam uchraydigan uslub — oddiy pipeline yoki qoidalar dvigateli yetarli bo'lgan joyda uni tanlash tizimni tushunarsiz va debug qilish qiyin qiladi. Umumiy holatga bir nechta modul parallel yozsa, race condition va aniqlanmagan yakuniy natija (nondeterminizm) paydo bo'ladi, shuning uchun versiyalash yoki optimistik lock majburiy.

## 12.21 Reaktiv Arxitektura (Reactive Architecture)

**Tavsif:** Tizim asinxron, non-blocking xabar almashinuvi ustiga quriladi va shu orqali javobgarlik (responsive), chidamlilik (resilient), elastiklik va xabarga asoslanganlik xossalariga erishadi. Asosiy maqsad — ko'p sonli parallel, I/O'ga bog'liq so'rovni kam thread bilan xizmat qilish va backpressure orqali tizimni ortiqcha yuklanishdan saqlash. Blocking thread-per-request modelida minglab bir vaqtli ulanish thread pool'ni tugatadi; reaktiv modelda esa event loop ishlatiladi. Buning narxi — debug, stack trace va kognitiv murakkablikning oshishi.

**Spring'da qayerda uchraydi:** Spring WebFlux (`spring-boot-starter-webflux`), Reactor'ning `Mono`/`Flux` turlari, Netty server; non-blocking HTTP klient `WebClient`; funksional routing `RouterFunction`/`RouterFunctions.route()`. Reaktiv ma'lumot kirishi: R2DBC (`spring-boot-starter-data-r2dbc`, `DatabaseClient`, `ReactiveCrudRepository`), reaktiv Redis va MongoDB starter'lari. Xavfsizlik uchun `@EnableWebFluxSecurity` va `SecurityWebFilterChain`; xabarlar uchun Reactor Kafka yoki RSocket (`spring-boot-starter-rsocket`, `@MessageMapping`). Muqobil yo'l: Java 21+ virtual thread'lar (`spring.threads.virtual.enabled=true`) blocking kodni saqlab turib scalability beradi.

**Qo'llanish keyslari:**
- API Gateway o'nlab mingta bir vaqtli ulanishni kam thread bilan proxy qiladi.
- Server-Sent Events orqali real-time narx yoki xabar oqimini brauzerga uzatish.
- Ko'p sonli tashqi servisga parallel chaqiruv qilib natijalarni birlashtiradigan aggregator servis.
- Katta fayl yoki ma'lumot oqimini xotiraga to'liq yuklamasdan `Flux` bilan streaming qilish.
- IoT yoki chat backend'i: uzun yashovchi ulanishlar soni serverdagi thread sonidan ancha ko'p.

**Ehtiyot bo'ling:** Reaktiv zanjir ichida bitta blocking chaqiruv (JDBC, `RestTemplate`, `Thread.sleep`) butun event loop'ni to'xtatadi — `BlockHound` bilan tekshirmasa bu xato ishlab chiqarishda topiladi. Oddiy CRUD ilovada WebFlux ko'pincha asossiz murakkablik: Java 21+ virtual thread'lar bilan MVC ko'p hollarda shu scalability'ni ancha soddaroq kod bilan beradi.

## 12.22 Monolit (Monolith)

**Tavsif:** Butun ilova bitta deploy birligi sifatida quriladi va ishga tushiriladi; modullar bir xil process ichida oddiy metod chaqiruvi orqali muloqot qiladi. Bu tarmoq kechikishi, taqsimlangan tranzaksiya va operatsion murakkablik muammolarini butunlay yo'q qiladi va ishlab chiqish tezligini maksimal qiladi. Zamonaviy ko'rinishi — modular monolith: ichki modul chegaralari qat'iy nazorat qilinadi, lekin deploy bitta bo'lib qoladi. Ko'p loyiha uchun bu to'g'ri boshlang'ich nuqta.

**Spring'da qayerda uchraydi:** Oddiy Spring Boot ilovasi: `@SpringBootApplication`, package bo'yicha modul ajratish, `@Transactional` bilan bitta ma'lumot bazasida ACID tranzaksiyalar, modul ichidagi hodisalar uchun `ApplicationEventPublisher` va `@TransactionalEventListener`. Modul chegaralarini majburlash uchun Spring Modulith (`spring-modulith-starter-core`, `@ApplicationModule`, `ApplicationModules.verify()` testi, `spring-modulith-events-api` bilan hodisa publikatsiyasi va `spring-modulith-starter-test`'ning `@ApplicationModuleTest`'i). Modullarni Maven/Gradle multi-module loyiha sifatida ajratish ham amalda ishlatiladi.

```java
@Test
void modullarChegarasiBuzilmagan() {
    ApplicationModules.of(ShopApplication.class).verify();
}
```

**Qo'llanish keyslari:**
- Startup MVP'ni bir jamoa bilan tez yetkazishda monolit deploy va debug narxini minimumga tushiradi.
- Ichki korporativ ilova (HR, hisobot, admin) kichik yuklamada mikroservisga hojat qoldirmaydi.
- Kelajakda mikroservisga bo'linishi mumkin bo'lgan tizim avval Spring Modulith bilan modular monolit sifatida quriladi.
- Qat'iy ACID talab qiladigan moliyaviy hisob-kitob bitta tranzaksiyada qoladi.
- Kichik jamoa (3-8 kishi) uchun operatsion yuk mikroservislardan ancha past bo'ladi.

**Ehtiyot bo'ling:** Modul chegaralari kod darajasida majburlanmasa, monolit tezda "big ball of mud"ga aylanadi — bir modul boshqasining repository'si va jadvaliga to'g'ridan-to'g'ri murojaat qila boshlaydi. Monolitni qo'rqib mikroservisga ko'chirishdan oldin haqiqiy sababni (deploy chastotasi, alohida scaling, jamoalar mustaqilligi) aniqlang; faqat "zamonaviy" bo'lish uchun bo'lish ko'pincha tizimni sekinlashtiradi.

## 12.23 Katta Loy To'pi (Big Ball of Mud) — anti-pattern

**Tavsif:** Bu aniq tanilgan strukturasi yo'q, moduldan modulga tartibsiz bog'lanishlar, takrorlangan kod va global holat bilan to'lgan tizim. Hech kim uni ataylab loyihalashtirmaydi — u vaqt tanqisligi, almashinuvchi jamoalar va "hozircha shunday qo'yib turamiz" qarorlari natijasida o'sib boradi. Har bir o'zgarish kutilmagan joyda sinadi, chunki qatlamlar orasida chegaralar mavjud emas. Bu pattern emas, balki boshqa barcha arxitektura uslublarining yo'qligi.

**Spring'da qayerda uchraydi:** Tipik ko'rinishi: `@Controller` ichida to'g'ridan-to'g'ri `JdbcTemplate`/`EntityManager` chaqiriladi, `@Service` sinflari bir-birini aylana bo'ylab inject qiladi (Spring Framework 6.x constructor injection'da buni `BeanCurrentlyInCreationException` bilan rad etadi, shuning uchun `@Lazy` yoki setter injection bilan "tuzatiladi"), 3000 qatorli `UtilService`, hamma joyda `@Transactional` va `@Autowired` field injection. Nazorat vositalari bor: ArchUnit (`classes().that().resideInAPackage("..web..").should().onlyDependOnClassesThat()`), Spring Modulith `ApplicationModules.of(App.class).verify()`, Maven `jdepend`/`SpotBugs`, va `@SpringBootTest` ni butun context uchun ishlatish o'rniga slice testlar (`@WebMvcTest`, `@DataJpaTest`).

**Qo'llanish keyslari:**
- Legacy monolitni strangler fig bilan bosqichma-bosqich bo'lishdan oldin uning bog'lanish grafigini ArchUnit bilan o'lchash.
- Prototip yoki hackathon kodi — ataylab tartibsiz, lekin muddati tugagach tashlab yuboriladi.
- Due diligence: sotib olinayotgan mahsulotning texnik qarzini baholash.
- Jamoa chegaralarini aniqlash uchun "o'zgarish birgalikda sodir bo'ladigan" fayllarni git tarixidan topish.
- Refaktoring budjetini asoslash uchun o'lchanadigan metrikalar (cyclic dependency soni) yig'ish.

**Ehtiyot bo'ling:** Katta "big rewrite" deyarli har doim muvaffaqiyatsiz bo'ladi — o'rniga chegaralarni avval test bilan qotirib, keyin modullarni ajrating. Shuningdek, toza arxitektura nomidan 5 kishilik jamoa uchun 12 qatlam yaratish ham xuddi shunday zarar: tartibsizlikning yechimi ortiqcha abstraksiya emas, balki aniq chegaralardir.

## 12.24 Taqsimlangan Monolit (Distributed Monolith) — anti-pattern

**Tavsif:** Bu tashqi ko'rinishda microservice bo'lgan, lekin ichkarida barcha servislar bir-biriga qattiq bog'langan va mustaqil deploy qilinmaydigan tizim. Bitta biznes operatsiyasi 7 ta sinxron HTTP chaqiruvini talab qiladi, servislar umumiy ma'lumotlar bazasini bo'lishadi va bitta DTO o'zgarsa hamma servisni birga relizga chiqarish kerak bo'ladi. Natijada monolitning barcha kamchiliklari (bog'lanish) tarmoqning barcha muammolari (latency, partial failure) bilan qo'shiladi. Mustaqillik yo'qoladi, lekin operatsion murakkablik qoladi.

**Spring'da qayerda uchraydi:** Belgilari: barcha servislar bitta `common-dto` yoki `shared-entity` Maven modulini import qiladi; har bir servisda bir xil `spring.datasource.url`; `@FeignClient` yoki `RestClient` zanjiri bilan 5 daraja chuqur sinxron chaqiruvlar; `@SharedEntity` sifatida bir xil JPA `@Entity` sinflari takrorlanadi. Yechim tomoni: har bir servis o'z schema'si (Flyway/Liquibase bilan alohida migratsiya), kontraktni OpenAPI + Spring Cloud Contract bilan versiyalash, sinxron chaqiruvlar o'rniga Spring Kafka/`spring-cloud-stream` orqali asinxron eventlar, `spring-cloud-circuitbreaker-resilience4j` bilan izolyatsiya, va Micrometer Tracing (OpenTelemetry) bilan chaqiruv zanjirining real chuqurligini o'lchash.

**Qo'llanish keyslari:**
- Mavjud microservice landshaftini audit qilib, "bitta so'rov necha servisga tegadi" ni Zipkin/Tempo trace'lari bilan o'lchash.
- Umumiy DTO kutubxonasini olib tashlab, har bir consumer uchun alohida kontrakt yaratish rejasini tuzish.
- Deploy bog'liqligini sinash: bitta servisni yakka o'zi relizga chiqarib ko'rish (coupling testi).
- Sinxron zanjirni event-driven saga'ga o'tkazish uchun nomzod oqimlarni tanlash.
- Shared database'dan database-per-service'ga o'tishda o'tish davri uchun view'lar yaratish.

**Ehtiyot bo'ling:** Eng xavfli holat — servis chegaralari biznes qobiliyatlari emas, texnik qatlamlar bo'yicha chizilgani (`user-api`, `user-logic`, `user-dao` alohida servis). Agar servislarni mustaqil deploy qila olmayotgan bo'lsangiz, ularni qaytib monolitga birlashtirish ko'pincha to'g'ri qaror.

## 12.25 Hujayra Asosidagi Arxitektura (Cell-Based Architecture)

**Tavsif:** Tizim bir-biridan to'liq izolyatsiya qilingan "hujayra"larga (cell) bo'linadi, har bir hujayra butun stack'ning mustaqil nusxasi bo'lib, foydalanuvchilarning aniq bir qismiga xizmat qiladi. Trafik cell router orqali shard kaliti (tenant ID, foydalanuvchi ID) bo'yicha yo'naltiriladi. Bitta hujayra ishdan chiqsa, faqat o'sha hujayradagi foydalanuvchilar ta'sirlanadi — bu "blast radius" ni cheklash usuli. AWS va Slack kabi yirik SaaS platformalari aynan shu model bilan ishlaydi.

**Spring'da qayerda uchraydi:** Spring'da maxsus annotatsiya yo'q — bu infratuzilma va routing darajasidagi pattern. Amalda: har bir cell alohida Kubernetes namespace yoki alohida AWS region/AZ guruhida ishlaydigan bir xil Spring Boot 3.x image; routing Spring Cloud Gateway (`spring-cloud-starter-gateway`) ichida `RoutePredicateFactory` yoki custom `GlobalFilter` bilan tenant kaliti bo'yicha amalga oshiriladi; cell ichida konfiguratsiya Spring Cloud Config yoki Kubernetes ConfigMap orqali profile (`spring.profiles.active=cell-eu-1`) bilan beriladi. Multi-tenant ma'lumot izolyatsiyasi uchun `AbstractRoutingDataSource` yoki Hibernate 6 `MultiTenantConnectionProvider` + `CurrentTenantIdentifierResolver` ishlatiladi; har bir cell uchun Micrometer tag (`cell=eu-1`) bilan alohida metrikalar yig'iladi.

**Qo'llanish keyslari:**
- Yirik B2B SaaS: har bir enterprise tenant guruhi o'z hujayrasida, shovqinli qo'shni (noisy neighbour) ta'sirini yo'qotish.
- Reliability maqsadi: deployni bitta hujayradan boshlab (canary cell) bosqichma-bosqich chiqarish.
- Ma'lumot suvereniteti: EU mijozlari uchun alohida hujayra, GDPR talablariga javob berish.
- Juda yirik mijozni alohida (single-tenant) hujayraga ko'chirish, kodni o'zgartirmasdan.
- Load testda hujayra sig'imini o'lchab, o'sishni "yana bitta cell qo'shish" bilan rejalashtirish.

**Ehtiyot bo'ling:** Operatsion narx yuqori — N hujayra degani N marta monitoring, migratsiya va reliz jarayoni, shuning uchun to'liq avtomatlashtirilgan CI/CD va IaC bo'lmasa boshlamang. Shuningdek, hujayralar orasida tenant'ni ko'chirish (rebalancing) alohida, murakkab muammo bo'lib, uni loyihaning boshida o'ylab qo'yish kerak.

## 12.26 Hech Narsani Bo'lishmaslik (Shared-Nothing)

**Tavsif:** Har bir node o'z CPU, xotira va diskiga ega bo'lib, boshqa node'lar bilan hech qanday mutable resursni bo'lishmaydi; koordinatsiya faqat tarmoq xabarlari orqali. Bu gorizontal masshtablashning asosiy sharti — umumiy resurs bo'lmaganda, bottleneck va lock contention ham yo'qoladi. Node'lar bir-birining holatini bilmaganligi uchun node qo'shish deyarli chiziqli ishlash o'sishini beradi. Amaliyotda to'liq "nothing" kam uchraydi, odatda umumiy ma'lumotlar bazasi qoladi, lekin application layer stateless bo'ladi.

**Spring'da qayerda uchraydi:** Spring Boot'da stateless ilovaning standart yo'li: HTTP session'ni node xotirasida saqlamaslik — Spring Session (`spring-session-data-redis`, `spring-session-jdbc`) orqali tashqariga chiqarish, yoki JWT bilan umuman session'siz ishlash (`SessionCreationPolicy.STATELESS` Spring Security 6.x `SecurityFilterChain` ichida). Lokal `ConcurrentMapCacheManager` o'rniga taqsimlangan cache (`spring-boot-starter-data-redis`, Hazelcast, Caffeine faqat lokal read-only ma'lumot uchun); `@Scheduled` job'lar har bir node'da takrorlanmasligi uchun ShedLock yoki Quartz JDBC JobStore; fayllarni lokal diskka emas, S3/MinIO ga yozish. `@Async` va virtual threadlar (Java 21+, `spring.threads.virtual.enabled=true`) node ichidagi parallelizm uchun, lekin node'lar o'rtasida holat bo'lishilmaydi.

**Qo'llanish keyslari:**
- Kubernetes'da HPA bilan avtomatik masshtablanadigan stateless REST servis.
- Batch ishlovni partitionlab bir nechta worker pod'ga tarqatish (Spring Batch remote partitioning).
- Blue/green yoki rolling deploy: node'larni istalgan vaqtda o'ldirish mumkin, chunki ularda noyob holat yo'q.
- Ko'p AZ bo'ylab tarqatilgan API gateway backendlari.
- Serverless (AWS Lambda + Spring Cloud Function) muhiti, bunda instance umri qisqa.

**Ehtiyot bo'ling:** "Stateless" degan ilovalar amalda yashirin holat saqlaydi — lokal fayl cache, static mutable field, in-memory rate limiter yoki scheduler lock — va bu faqat ikkinchi instance qo'shilganda ko'rinadi. Ma'lumotlar bazasi hamon umumiy resurs bo'lib qolgani uchun, shared-nothing application layer DB bottleneck'ini hal qilmaydi: sharding yoki read replica alohida qaror talab qiladi.

## 12.27 Lambda / Kappa Arxitekturasi (Lambda / Kappa Architecture)

**Tavsif:** Lambda arxitekturasi ma'lumotni ikki yo'ldan o'tkazadi: batch layer to'liq tarixni qayta hisoblab aniq natija beradi, speed layer esa real vaqtda taxminiy natija beradi, serving layer ularni birlashtiradi. Bu aniqlik va tezlikni bir vaqtda beradi, lekin bitta biznes logikani ikki marta — batch va stream uchun — yozishni talab qiladi. Kappa arxitekturasi batch layer'dan voz kechib, hammasini bitta stream pipeline bilan hal qiladi: tarixni qayta hisoblash kerak bo'lsa, log'ni boshidan qayta o'ynatiladi (replay). Kappa soddaroq, lekin uzoq saqlanadigan, qayta o'ynaladigan log (Kafka) talab qiladi.

**Spring'da qayerda uchraydi:** Spring ekotizimida: stream layer uchun Spring for Apache Kafka (`@KafkaListener`, `KafkaTemplate`) yoki Spring Cloud Stream (`spring-cloud-stream-binder-kafka`) funksional model bilan (`Function<KStream<K,V>, KStream<K,V>>` bean'lari Kafka Streams binder orqali); batch layer uchun Spring Batch 5.x (`Job`, `Step`, `ItemReader`/`ItemWriter`) yoki Spring Cloud Data Flow orqali task orkestratsiyasi. Kappa'da replay uchun consumer group offset'ini `KafkaConsumerBackoffManager` emas, balki `seekToBeginning` yoki yangi consumer group bilan boshqariladi; `spring-cloud-stream` da `spring.cloud.stream.kafka.bindings.<name>.consumer.resetOffsets=true` ishlatiladi. Serving layer odatda Spring Data (Cassandra, Elasticsearch, Redis) orqali o'qiladi.

**Qo'llanish keyslari:**
- Real vaqtda fraud detection (speed layer) + kechqurun aniq hisob-kitob va reconciliation (batch layer).
- IoT telemetriya: daqiqalik dashboard stream'dan, kunlik hisobot batch'dan.
- Marketing analitikasi: sessiya hodisalaridan agregat metrikalar, logika o'zgarsa Kappa bilan to'liq replay.
- Event-sourced tizimda yangi read model yaratish — eventlarni boshidan o'ynatib projection qurish.
- Clickstream'dan rekomendatsiya featurelarini real vaqtda yangilash.

**Ehtiyot bo'ling:** Lambda'da eng katta xavf — ikki pipeline logikasining asta-sekin bir-biridan uzoqlashishi (training/serving skew), shuning uchun agar Kafka'da yetarli retention bera olsangiz Kappa'ni afzal ko'ring. Kappa'da esa replay vaqti va downstream'ga tushadigan yuk oldindan hisoblangan bo'lishi kerak, aks holda "kichik bir tuzatish" production'ni bosib qoladi.

## 12.28 Feature Bo'yicha vs Qatlam Bo'yicha Paketlash (Package-by-feature vs Package-by-layer)

**Tavsif:** Package-by-layer kodni texnik rolga ko'ra guruhlaydi (`controller`, `service`, `repository`, `dto`), package-by-feature esa biznes qobiliyatiga ko'ra (`order`, `payment`, `shipping`) — har bir paket ichida o'zining controller, service va repository'si bo'ladi. Feature bo'yicha paketlashda bitta o'zgarish bitta paket ichida qoladi, cohesion yuqori, coupling past bo'ladi va paketni keyinchalik alohida modul yoki servisga ajratish oson. Qatlam bo'yicha paketlash kichik loyihada tushunarli, lekin o'sgan sari har bir feature kodi 4-5 paket bo'ylab sochilib ketadi.

**Spring'da qayerda uchraydi:** Spring Boot'da `@SpringBootApplication` component scan root paketdan boshlanganligi uchun ikkala struktura ham ishlaydi, lekin feature bo'yicha paketlash Java `package-private` ko'rinishini real himoyaga aylantiradi: `OrderRepository` ni `package-private` qilib, faqat `com.app.order` ichidan foydalanish mumkin. Spring Modulith (1.x) aynan shu modelga qurilgan — har bir to'g'ridan-to'g'ri sub-paket bitta modul, `package-info.java` da `@ApplicationModule(allowedDependencies = "shared")` bilan chegaralar belgilanadi, `ApplicationModules.of(App.class).verify()` buzilishlarni testda ushlaydi, `@ApplicationModuleTest` esa modulni yakka test qiladi. Modullar orasidagi aloqa `ApplicationEventPublisher` + `@ApplicationModuleListener` orqali, hamda `Documenter` bilan C4 diagrammalari generatsiya qilinadi.

**Qo'llanish keyslari:**
- Modulli monolit qurish: kelajakda ajratilishi mumkin bo'lgan chegaralarni bugundan belgilash.
- Katta jamoada kod egaligini belgilash (`CODEOWNERS` paket bo'yicha).
- Microservice'ga ajratish: `com.app.billing` paketini butunlay yangi servisga ko'chirish.
- Legacy layered kodni refaktoring qilishda bitta feature'ni "vertikal tilim" qilib ajratib olish.
- ArchUnit/Modulith bilan "order paketi payment internal sinflarini chaqirmasin" qoidasini CI'da qotirish.

**Ehtiyot bo'ling:** Feature paketlari ichida yana to'liq qatlam ierarxiyasini takrorlab, 3 qatlamli kichik monolitlar yasash ortiqcha ceremoniya bo'ladi — kichik feature uchun 2-3 sinf yetadi. Shuningdek, `common`/`shared` paketi tez orada yangi Big Ball of Mud markaziga aylanadi: unga nima tushishini qat'iy cheklang.

## 12.29 Baqiruvchi Arxitektura (Screaming Architecture)

**Tavsif:** Robert Martin tomonidan ifodalangan g'oyaga ko'ra, loyihaning yuqori darajadagi strukturasi framework haqida emas, balki tizimning biznes maqsadi haqida "baqirib" turishi kerak. Ya'ni paket daraxtini ko'rgan kishi "bu Spring MVC loyihasi" emas, "bu sug'urta polisi boshqaruv tizimi" degan xulosaga kelishi lozim. Bu package-by-feature'ning falsafiy asosi: katalog nomlari use-case va domen tilidan olinadi, framework esa detal bo'lib chetga suriladi. Natijada yangi injener kodga kirganda domenni o'rganadi, texnologiyani keyin.

**Spring'da qayerda uchraydi:** Amalda bu `com.insurance.policy.underwriting`, `com.insurance.claims.settlement` kabi paketlar bo'lib, ularning ichida `UnderwritePolicyUseCase` kabi sinflar turadi; framework kodi esa `adapter/web` va `adapter/persistence` ga siqiladi (hexagonal bilan tabiiy birlashadi). Spring Boot buni qo'llab-quvvatlaydi: `@SpringBootApplication(scanBasePackages = "com.insurance")`, domen sinflarida Spring annotatsiyalari bo'lmaydi, konfiguratsiya `@Configuration` sinflarida markazlashadi. Spring Modulith `Documenter` va `@ApplicationModule(displayName = "Claims Settlement")` orqali bu nomlarni jonli dokumentatsiyaga aylantiradi; ArchUnit qoidalari esa domen paketining `org.springframework` ga bog'lanishini taqiqlaydi (`noClasses().that().resideInAPackage("..domain..").should().dependOnClassesThat().resideInAPackage("org.springframework..")`).

**Qo'llanish keyslari:**
- Yangi jamoa a'zosini onboarding qilish vaqtini qisqartirish — struktura domen xaritasi bo'lib xizmat qiladi.
- DDD bounded context'larini kod strukturasida to'g'ridan-to'g'ri aks ettirish.
- Uzoq umr ko'radigan enterprise tizim: 10 yildan keyin framework o'zgarsa ham domen strukturasi qoladi.
- Monolitni biznes chegaralari bo'yicha bo'lishda nomzod servislarni paket daraxtidan o'qib olish.
- Biznes analitik bilan kod strukturasi ustida bir tilda gaplashish (ubiquitous language).

**Ehtiyot bo'ling:** Nomlarni haqiqiy domen tilidan olish kerak — `manager`, `processor`, `helper` kabi umumiy nomlar strukturani yana "baqirmaydigan" holatga qaytaradi. Va bu toza domenni framework'dan ajratishni talab qilgani uchun qo'shimcha mapping kodi tug'diradi: oddiy CRUD servis uchun bu ortiqcha bo'lishi mumkin.

## 12.30 Komponentga Asoslangan Arxitektura (Component-Based Architecture)

**Tavsif:** Tizim mustaqil, almashtiriladigan komponentlardan quriladi; har bir komponent o'z ichki amalga oshirishini yashirib, faqat aniq belgilangan interfeys (provided/required) orqali muloqot qiladi. Komponentlar binar darajada qayta ishlatiladi va o'rnini bir xil kontraktni bajaruvchi boshqa implementatsiya egallashi mumkin. Bu dependency injection va interfeysga programmalashning amaliy asosi; microservice'dan farqi — komponentlar bir process ichida ham yashashi mumkin.

**Spring'da qayerda uchraydi:** Spring'ning o'zagi aynan shu: `@Component` (va `@Service`, `@Repository`, `@Controller` stereotiplari), `ApplicationContext` komponent konteyner, constructor injection esa required interfeyslarni e'lon qilish usuli. Bir interfeysning bir nechta implementatsiyasi `@Qualifier`, `@Primary` yoki `@ConditionalOnProperty`/`@ConditionalOnMissingBean` bilan tanlanadi; ro'yxat sifatida `List<PaymentProvider>` inject qilib strategy registry quriladi. Auto-configuration mexanizmi (`META-INF/spring/org.springframework.boot.autoconfigure.AutoConfiguration.imports`, Spring Boot 3.x) komponentlarni starter sifatida qadoqlashning standart usuli; Java modullari (JPMS) yoki alohida Maven modul va `@AutoConfiguration` bilan o'zingizning qayta ishlatiladigan komponentingizni yarata olasiz.

```java
public interface PaymentProvider { boolean supports(Currency c); Receipt charge(Order o); }

@Service
class PaymentRouter {
    private final List<PaymentProvider> providers;
    PaymentRouter(List<PaymentProvider> providers) { this.providers = providers; }
    Receipt pay(Order o) {
        return providers.stream().filter(p -> p.supports(o.currency()))
            .findFirst().orElseThrow(() -> new IllegalStateException("no provider"))
            .charge(o);
    }
}
```

**Qo'llanish keyslari:**
- Ko'p loyihada qayta ishlatiladigan ichki starter (audit logging, tenant resolver) yaratish.
- To'lov, SMS yoki fayl saqlash provayderini kodni o'zgartirmasdan almashtirish.
- Test uchun real komponentni `@TestConfiguration` da fake implementatsiya bilan almashtirish.
- Mijozga qarab xususiyatlarni yoqish/o'chirish (`@ConditionalOnProperty` bilan feature modullar).
- Plugin modeli: uchinchi tomon o'z `PaymentProvider` ni classpath'ga qo'shib tizimni kengaytiradi.

**Ehtiyot bo'ling:** Interfeysni faqat bitta implementatsiya uchun yaratish (speculative generality) hech qanday foyda bermasdan kodni ikki barobar oshiradi. Ortiqcha `@Conditional` zanjirlari esa context'ning nima uchun shunday yig'ilganini tushunishni qiyinlashtiradi — `--debug` bilan auto-configuration report'ini o'qishga odatlaning.

## 12.31 API-Birinchi (API-First)

**Tavsif:** Bu yondashuvda API kontrakti (OpenAPI, gRPC `.proto`, GraphQL schema) kod yozilishidan oldin loyihalashtiriladi va u yagona haqiqat manbai (source of truth) bo'ladi. Kontrakt kelishilgandan so'ng server va client jamoalari parallel ishlay oladi, mock server kontraktdan generatsiya qilinadi, buzuvchi o'zgarishlar esa CI'da avtomatik aniqlanadi. Bu ichki servislar orasidagi integratsiya xatolarini loyihaning eng arzon bosqichiga — dizaynga — ko'chiradi.

**Spring'da qayerda uchraydi:** Spring'da ikki yo'nalish bor. Contract-first: `openapi-generator-maven-plugin` (yoki `swagger-codegen`) bilan OpenAPI faylidan Spring interfeys va DTO'larni generatsiya qilish (`spring` generator, `interfaceOnly=true` → controller shu interfeysni implement qiladi); gRPC uchun `protobuf-maven-plugin` + `grpc-spring-boot-starter`; GraphQL uchun Spring for GraphQL (`spring-boot-starter-graphql`) `.graphqls` schema fayli bilan ishlaydi va `@SchemaMapping`/`@QueryMapping` ni unga bog'laydi. Code-first tomoni: `springdoc-openapi-starter-webmvc-ui` (Spring Boot 3.x uchun `springdoc-openapi` 2.x) kontraktni koddan generatsiya qiladi. Kontrakt buzilmasligini Spring Cloud Contract (`spring-cloud-starter-contract-verifier`) provider tomonda testlar generatsiya qilib, consumer tomonda stub berib ta'minlaydi; HTTP interfeys clientlari `@HttpExchange` + `HttpServiceProxyFactory` (Spring Framework 6.x) bilan deklarativ yoziladi.

**Qo'llanish keyslari:**
- Mobil va backend jamoalari parallel boshlashi uchun kontraktni oldin kelishib, mock server berish.
- Public API: versiyalash siyosati va buzuvchi o'zgarishlarni `openapi-diff` bilan CI'da nazorat qilish.
- Partner integratsiyasi: tashqi tomonga SDK'ni OpenAPI'dan generatsiya qilib berish.
- Microservice'lar orasida consumer-driven contract testlar bilan regressiyani ushlash.
- API gateway'da routing, rate limit va validatsiyani OpenAPI spetsifikatsiyasidan avtomatik sozlash.

**Ehtiyot bo'ling:** Kontraktni avval yozib, keyin uni koddan sekin-asta uzoqlashtirish eng keng tarqalgan xato — generatsiyani build'ning majburiy qadamiga aylantirmasa, spetsifikatsiya hujjatga aylanadi va yolg'on gapira boshlaydi. Shuningdek, DTO'ni to'g'ridan-to'g'ri JPA `@Entity` dan generatsiya qilib, ma'lumotlar bazasi strukturasini public API'ga chiqarib qo'yish keyinchalik orqaga qaytmas bog'lanish yaratadi.

## 12.32 Event-Birinchi (Event-First)

**Tavsif:** Tizimni loyihalash ma'lumotlar bazasi jadvallari yoki REST endpointlardan emas, biznesda sodir bo'ladigan hodisalardan (domain events) boshlanadi: `OrderPlaced`, `PaymentCaptured`, `ShipmentDispatched`. Event'lar birinchi darajali kontrakt bo'lib, servislar bir-birini chaqirmaydi, balki o'zi uchun muhim hodisalarga obuna bo'ladi — bu temporal coupling'ni yo'qotadi va yangi consumer'ni mavjud kodga tegmasdan qo'shishga imkon beradi. Event Storming shu yondashuvning standart dizayn amaliyoti.

**Spring'da qayerda uchraydi:** Process ichida: `ApplicationEventPublisher.publishEvent()`, `@EventListener` va `@TransactionalEventListener(phase = AFTER_COMMIT)` — tranzaksiya commit bo'lgandan keyin reaksiya qilish uchun. Process tashqarisida: Spring for Apache Kafka (`KafkaTemplate`, `@KafkaListener`, `DefaultErrorHandler` + `DeadLetterPublishingRecoverer`), Spring AMQP (RabbitMQ), yoki Spring Cloud Stream funksional binding'lari. Spring Modulith event publication registry (`spring-modulith-events-jpa`/`-jdbc`) transactional outbox pattern'ini beradi: event DB'ga commit bilan birga yoziladi va `@ApplicationModuleListener` muvaffaqiyatli bajarilmaguncha "incomplete" holatda qoladi, qayta yuborish esa restart'da avtomatik. Event schema'ni Avro/Protobuf + Confluent Schema Registry bilan versiyalash, idempotentlikni consumer tomonda qayta ishlangan event ID jadvali bilan ta'minlash standart amaliyot.

**Qo'llanish keyslari:**
- E-commerce: `OrderPlaced` dan keyin inventar, to'lov, bildirishnoma va analitika mustaqil reaksiya qiladi.
- Audit va compliance: hodisalar ketma-ketligi o'zgarmas jurnal sifatida saqlanadi.
- Yangi read model yoki analitik pipeline'ni mavjud event log'dan replay qilib qurish.
- Legacy tizimdan CDC (Debezium) orqali event chiqarib, yangi servislarni unga ulash.
- Saga bilan taqsimlangan tranzaksiya: har bir qadam event'ga javob beradi, kompensatsiya ham event.

**Ehtiyot bo'ling:** Event'larni CRUD bildirishnomasiga aylantirib (`UserUpdated` ichida butun entity) yuborish yashirin bog'lanish yaratadi — event biznes faktini, nima sodir bo'lganini ifodalashi kerak. Eventual consistency'ni biznes bilan kelishmasdan tanlamang: "buyurtma darhol ko'rinmaydi" degani UI va qo'llab-quvvatlash jarayonlariga ham ta'sir qiladi, hamda debugging uchun distributed tracing majburiy bo'ladi.

## 12.33 Mikro-Frontendlar (Micro-frontends) — eslatib o'tish

**Tavsif:** Backend'dagi microservice g'oyasini brauzer tomoniga ko'chirish: yagona katta SPA o'rniga, har bir jamoa o'z UI bo'lagini mustaqil ishlab chiqadi va deploy qiladi, shell (host) ilova esa ularni runtime'da birlashtiradi. Birlashtirish Webpack/Rspack Module Federation, Web Components, iframe yoki server-side include orqali amalga oshiriladi. Bu vertikal jamoalarga (backend + frontend bitta biznes qobiliyati uchun) to'liq mustaqillik beradi.

**Spring'da qayerda uchraydi:** Spring bu pattern'ning backend va kompozitsiya qismida qatnashadi: Spring Cloud Gateway har bir fragment yoki remote bundle'ni o'z servisiga yo'naltiradi; server-side kompozitsiya uchun Thymeleaf fragment'lari (`th:replace`) yoki `WebClient` bilan boshqa servis HTML bo'lagini olib birlashtirish ishlatiladi; statik bundle'lar Spring Boot'ning `WebMvcConfigurer#addResourceHandlers` yoki CDN orqali beriladi. Xavfsizlik tomoni muhim: Spring Security 6.x `SecurityFilterChain` ichida `headers().contentSecurityPolicy(...)`, `CorsConfigurationSource` bilan cross-origin remote'larga ruxsat, va OAuth2 token'ni shell bilan bo'lishish uchun `oauth2Login` yoki BFF (Backend-For-Frontend) pattern'i `spring-cloud-gateway` + `TokenRelay` filtri bilan.

**Qo'llanish keyslari:**
- Yirik B2B portal: billing, reporting va admin bo'limlari alohida jamoalar tomonidan deploy qilinadi.
- Legacy JSP/Thymeleaf ilovasini sahifa-sahifa yangi frontend'ga ko'chirish (strangler).
- Bir nechta mahsulot bitta brend ostida yagona navigatsiya bilan birlashtirilishi.
- Har bir jamoaga o'z reliz tezligini berish — UI o'zgarishi butun monorepo relizini kutmaydi.
- A/B test: bitta fragment'ning yangi versiyasini faqat ayrim foydalanuvchilarga ko'rsatish.

**Ehtiyot bo'ling:** Narxi juda yuqori: umumiy dizayn tizimi, versiya nomuvofiqligi, takrorlangan kutubxonalar va yaxlit UX uchun qattiq boshqaruv kerak — 2-3 jamoadan kichik tashkilotda bu deyarli har doim ortiqcha. Autentifikatsiya, routing va global holatni fragmentlar o'rtasida bo'lishish eng ko'p muammo tug'diradigan joy, shuning uchun BFF bilan boshlang va fragmentlarni biznes chegarasi bo'yicha, komponent darajasida emas, bo'ling.

---

[&larr; 11. Keshlash patternlari](11-keshlash-patternlari.md) · [Mundarija](README.md) · [13. Domain-Driven Design patternlari &rarr;](13-domain-driven-design-patternlari.md)
