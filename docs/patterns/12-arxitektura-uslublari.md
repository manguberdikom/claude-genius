<!-- doc: patterns | chapter: 12 | part:  -->

[Barcha hujjatlar](../../README.md) / [Dizayn patternlar](README.md)

> Holat: tekshirilmoqda. Da'volar hali manbaga solishtirilmoqda.

# 12. Arxitektura uslublari (Architectural Styles)

<details>
<summary>Bu bobdagi 38 bo'lim</summary>

- [12.1 Qatlamli arxitektura (Layered / N-tier Architecture)](#121-qatlamli-arxitektura-layered--n-tier-architecture)
- [12.2 Olti burchakli arxitektura (Hexagonal Architecture / Ports & Adapters)](#122-olti-burchakli-arxitektura-hexagonal-architecture--ports--adapters)
- [12.3 Clean Architecture (Clean Architecture)](#123-clean-architecture-clean-architecture)
- [12.4 Piyoz arxitekturasi (Onion Architecture)](#124-piyoz-arxitekturasi-onion-architecture)
- [12.5 Vertikal qatlamli arxitektura (Vertical Slice Architecture)](#125-vertikal-qatlamli-arxitektura-vertical-slice-architecture)
- [12.6 Modulli monolit (Modular Monolith / Spring Modulith)](#126-modulli-monolit-modular-monolith--spring-modulith)
- [12.7 Mikroyadro / Plugin arxitekturasi (Microkernel / Plugin Architecture)](#127-mikroyadro--plugin-arxitekturasi-microkernel--plugin-architecture)
- [12.8 Quvurlar va filtrlar (Pipes and Filters)](#128-quvurlar-va-filtrlar-pipes-and-filters)
- [12.9 Hodisaga asoslangan arxitektura (Event-Driven Architecture - broker va mediator topologiyalari)](#129-hodisaga-asoslangan-arxitektura-event-driven-architecture---broker-va-mediator-topologiyalari)
- [12.10 Buyruq va so'rovlar mas'uliyatini ajratish (CQRS - Command Query Responsibility Segregation)](#1210-buyruq-va-sorovlar-masuliyatini-ajratish-cqrs---command-query-responsibility-segregation)
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
- [12.23 Katta Loy To'pi (Big Ball of Mud) - anti-pattern](#1223-katta-loy-topi-big-ball-of-mud---anti-pattern)
- [12.24 Taqsimlangan Monolit (Distributed Monolith) - anti-pattern](#1224-taqsimlangan-monolit-distributed-monolith---anti-pattern)
- [12.25 Hujayra Asosidagi Arxitektura (Cell-Based Architecture)](#1225-hujayra-asosidagi-arxitektura-cell-based-architecture)
- [12.26 Hech Narsani Bo'lishmaslik (Shared-Nothing)](#1226-hech-narsani-bolishmaslik-shared-nothing)
- [12.27 Lambda / Kappa Arxitekturasi (Lambda / Kappa Architecture)](#1227-lambda--kappa-arxitekturasi-lambda--kappa-architecture)
- [12.28 Feature Bo'yicha vs Qatlam Bo'yicha Paketlash (Package-by-feature vs Package-by-layer)](#1228-feature-boyicha-vs-qatlam-boyicha-paketlash-package-by-feature-vs-package-by-layer)
- [12.29 Baqiruvchi Arxitektura (Screaming Architecture)](#1229-baqiruvchi-arxitektura-screaming-architecture)
- [12.30 Komponentga Asoslangan Arxitektura (Component-Based Architecture)](#1230-komponentga-asoslangan-arxitektura-component-based-architecture)
- [12.31 API-Birinchi (API-First)](#1231-api-birinchi-api-first)
- [12.32 Event-Birinchi (Event-First)](#1232-event-birinchi-event-first)
- [12.33 Mikro-Frontendlar (Micro-frontends) - eslatib o'tish](#1233-mikro-frontendlar-micro-frontends---eslatib-otish)
- [12.34 Servis Asosidagi Arxitektura (Service-Based Architecture)](#1234-servis-asosidagi-arxitektura-service-based-architecture)
- [12.35 Data Mesh va analitik ma'lumot tekisligi (Data Mesh)](#1235-data-mesh-va-analitik-malumot-tekisligi-data-mesh)
- [12.36 Arxitektura uslubini tanlash tartibi (Choosing an Architecture Style)](#1236-arxitektura-uslubini-tanlash-tartibi-choosing-an-architecture-style)
- [12.37 Taqsimlangan obyekt dizaynining birinchi qonuni (First Law of Distributed Object Design)](#1237-taqsimlangan-obyekt-dizaynining-birinchi-qonuni-first-law-of-distributed-object-design)
- [12.38 Amalda qo'llash](#1238-amalda-qollash)

</details>



Arxitektura uslublari - bu alohida sinf darajasidagi dizayn patternlardan farqli ravishda, butun tizimning yuqori darajadagi tuzilishini, modullar orasidagi bog'liqlik yo'nalishini va o'zgarishlar qanday tarqalishini belgilovchi qoliplardir. Richards va Ford uslublarni ikki sinfga ajratadi: monolit (butun kod bitta deploy birligi) va tarqatilgan (bir nechta deploy birligi masofaviy protokol orqali ulangan); ular monolit sinfiga qatlamli, quvurli va mikroyadro uslublarini, tarqatilgan sinfga esa servis asosidagi, hodisaga asoslangan, kosmosga asoslangan, servisga yo'naltirilgan va mikroservis uslublarini kiritadi. Shu kitob har bir uslub uchun arxitektura xossalarini bir yulduzdan besh yulduzgacha baholaydi: bir yulduz - xossa bu uslubda yaxshi qo'llab-quvvatlanmaydi, besh yulduz - xossa uslubning eng kuchli tomoni. Shu sababli bu bobda uslublarni taqqoslovchi baholar o'ylab topilmaydi: kitob reytingi bor uslublarda "Reyting" qatori aynan shu jadvaldan olinadi, kitobda yo'q uslublarda esa baho qo'yilmaydi. Spring ekotizimi deyarli barcha uslublarni qo'llab-quvvatlaydi, lekin hech birini majburlamaydi - shuning uchun tanlov va uning intizomli saqlanishi arxitektor zimmasida.

## 12.1 Qatlamli arxitektura (Layered / N-tier Architecture)

**Tavsif:** Tizim mas'uliyatlar bo'yicha gorizontal qatlamlarga bo'linadi. Richards va Ford aksariyat qatlamli arxitektura to'rt standart qatlamdan iborat deydi: presentation, business, persistence, database; persistence mantiqi business ichiga ko'chsa uchta qatlam qoladi, yirik tizimlarda esa besh yoki undan ko'p qatlam bo'ladi. Fowler korporativ ilova uchun uch asosiy qatlamni ajratadi: presentation, domain, data source. Har bir qatlam o'zidan pastdagi qatlam xizmatlaridan foydalanadi, pastki qatlam esa yuqoridagisidan bexabar bo'ladi. Qatlam "yopiq" bo'lsa so'rov hech bir qatlamni o'tkazib yubora olmaydi va to'g'ridan-to'g'ri quyidagi qatlamga tushadi, "ochiq" bo'lsa o'tkazib yuborish mumkin; yopiq qatlam Richards va Ford atamasi bilan "layers of isolation" beradi, ya'ni bir qatlamdagi o'zgarish qo'shni qatlamdan nariga o'tmaydi. Uslubning keng tarqalganligi Conway qonuni bilan izohlanadi: tashkilotda UI, backend, qoidalar va DBA mutaxassislari alohida bo'lgani uchun kod ham shunday qatlamlanadi.

**Reyting (*Fundamentals of Software Architecture*, 10-bob, arxitektura xossalari yulduz jadvali):** kuchli tomoni umumiy narx va soddalik; deployability juda past, testability ikki yulduz, reliability uch yulduz, elasticity va scalability bir yulduz, performance ikki yulduz, fault tolerance past. Monolit kattalashgani sari bu baholar tezda pasayadi.

**Spring'da qayerda uchraydi:** Klassik `@RestController` → `@Service` → `@Repository` uchligi aynan shu uslubning amaliy ifodasi; `@Repository` ustidagi `PersistenceExceptionTranslationPostProcessor` persistence qatlamining exception'larini `DataAccessException` ierarxiyasiga tarjima qilib, pastki qatlam detallarini yuqoridan yashiradi. Spring Boot 3.x loyihalarida bu odatda `com.example.app.web`, `.service`, `.domain`, `.repository` paketlari ko'rinishida bo'ladi. Qatlam chegaralarini avtomatik tekshirish uchun ArchUnit (`layeredArchitecture()` qoidasi) testlari ishlatiladi. `@Transactional` ni service qatlamida joylash - bu uslubning standart konvensiyasi.

**Qo'llanish keyslari:**
- Klassik CRUD-og'ir admin panel yoki back-office tizimi, bunda domen logikasi juda yupqa.
- Jamoa yangi yoki tez o'sayotgan bo'lsa - eng past kognitiv yuk va eng ko'p tayyor misollar.
- Ichki korporativ reporting xizmatlari, bunda asosiy ish - ma'lumotni DB'dan olib JSON'ga aylantirish.
- Legacy tizimni modernizatsiya qilishda birinchi qadam: avval tartibsiz kodni qatlamlarga ajratish.
- Prototip yoki MVP, keyinchalik hexagonal/modular monolitga evolyutsiya qilish rejasi bilan. Richards va Ford qaysi uslub tanlanishi hali aniq bo'lmaganda qatlamli uslubni boshlang'ich nuqta sifatida tavsiya qiladi, lekin keyin boshqa uslubga o'tish oson bo'lishi uchun qayta ishlatishni minimumda va inheritance daraxtini yuza saqlashni shart qiladi.

**Ehtiyot bo'ling:** Uslubning kitobda nomlangan asosiy tuzog'i - architecture sinkhole anti-pattern: so'rov qatlamdan qatlamga hech qanday biznes mantiqisiz o'tib ketadi va faqat ortiqcha obyekt yaratilishi bilan xotira va performance'ga zarar beradi. Richards va Ford buni 80-20 qoidasi bilan o'lchashni taklif qiladi: so'rovlarning 20 foizi shunday bo'lsa qabul qilinadi, 80 foizi bo'lsa bu uslub bu domenga to'g'ri kelmaydi. Ikkinchi tuzoq - uslub texnik bo'linishga asoslangani uchun bitta domen barcha qatlamlar bo'ylab sochiladi va shu sababli DDD yondashuvi bu uslub bilan yaxshi ishlamaydi; Fowler ham xuddi shu narxni ko'rsatadi, UI'da bitta yangi maydon paydo bo'lsa, u oradagi har bir qatlamga qo'shilishi kerak. Spring amaliyotida bu "anemik domen modeli" ko'rinishida chiqadi: butun logika `@Service` sinflarida to'planib, entity'lar getter/setter to'plamiga aylanadi. Domen qatlami JPA annotatsiyalariga va `Repository` interfeyslariga bog'lanib qolsa, qatlamlar faqat paket nomida qoladi.

```text
com.example.orders
  web/          OrderController, OrderDto
  service/      OrderService
  repository/   OrderRepository
  domain/       Order

Bog'liqlik yo'nalishi faqat pastga: web -> service -> repository -> domain.
ArchUnit bilan majburlash:
  noClasses().that().resideInAPackage("..domain..")
    .should().dependOnClassesThat().resideInAPackage("..web..")

Kamchiligi: har biznes o'zgarishi to'rt paketga tegadi, shuning uchun
koheziya past va qaysi funksiya borligi tuzilmadan ko'rinmaydi.
```

## 12.2 Olti burchakli arxitektura (Hexagonal Architecture / Ports & Adapters)

**Tavsif:** Ilova yadrosi (domain + use case'lar) markazda turadi va tashqi dunyo bilan faqat o'zi e'lon qilgan interfeyslar - port'lar orqali gaplashadi. Har bir texnologiya (HTTP, Kafka, JPA, SMTP) shu port'ni amalga oshiruvchi adapter sifatida chetga chiqariladi, natijada bog'liqlik yo'nalishi har doim tashqaridan yadroga qarab bo'ladi. Inbound (driving) port'lar yadroni chaqiradi, outbound (driven) port'lar yadro ehtiyojini ifodalaydi. Bu yadroni Spring'dan ham, DB'dan ham mustaqil sinovdan o'tkazish imkonini beradi.

**Spring'da qayerda uchraydi:** Yadro odatda toza POJO'lardan iborat alohida Maven/Gradle moduli bo'lib, unda hech qanday Spring annotatsiyasi bo'lmaydi; adapter modullarida esa `@RestController`, `@KafkaListener`, `@Entity` va Spring Data `JpaRepository` joylashadi. Outbound port (masalan `LoadCustomerPort`) interfeysi yadroda e'lon qilinadi va `@Component` bilan belgilangan persistence adapter uni `JpaRepository` ustida implement qiladi; wiring esa `@Configuration` sinfidagi `@Bean` metodlari orqali bajariladi. Spring Framework 6.x'dagi `RestClient`/`WebClient` tashqi HTTP adapterlar uchun, `@ConfigurationProperties` esa adapter sozlamalari uchun ishlatiladi. Chegaralarni ArchUnit yoki Maven module bog'liqliklari bilan majburlash odatiy amaliyot.

**Qo'llanish keyslari:**
- Murakkab domen logikasi bo'lgan to'lov, kreditlash yoki sug'urta tizimlari.
- Bir xil use case'ni bir vaqtda REST, gRPC va message consumer orqali ochish kerak bo'lganda.
- Tashqi provayder (masalan to'lov shlyuzi yoki KYC servisi) yaqin kelajakda almashishi aniq bo'lsa.
- Domen qoidalarini DB va broker ko'tarmasdan, millisekundlarda unit test qilish talab qilinsa.
- Legacy integratsiyalarni asta-sekin anti-corruption adapterlar orqali izolyatsiya qilishda.

**Ehtiyot bo'ling:** Yupqa CRUD xizmatlar uchun bu uslub ortiqcha: har bir maydon uchun domen obyekti, DTO, entity va ikki mapper paydo bo'lib, foydali kodga nisbatan boilerplate ulushi keskin oshadi. Yana bir tuzoq - JPA entity'ni to'g'ridan-to'g'ri domen obyekti sifatida ishlatish: bu port'lar orqali hosil qilingan izolyatsiyani yashirin tarzda buzadi va lazy loading muammolarini yadroga olib kiradi.

```java
// Port: domen o'ziga keragini e'lon qiladi (domen paketida)
public interface PaymentPort {
    Receipt charge(Payment payment);
}

// Adapter: tashqi dunyo (infra paketida)
@Component
class PspPaymentAdapter implements PaymentPort {
    private final RestClient psp;
    @Override public Receipt charge(Payment p) { /* HTTP tafsiloti faqat shu yerda */ }
}

// Domen servisi faqat portni biladi
public class PlaceOrderUseCase {
    private final PaymentPort payments;                 // interfeys
    public PlaceOrderUseCase(PaymentPort payments) { this.payments = payments; }
}
// Bog'liqlik yo'nalishi: infra -> domen. Domen Spring ni ham bilmaydi.
```

## 12.3 Clean Architecture (Clean Architecture)

**Tavsif:** Hexagonal g'oyasini kontsentrik halqalar ko'rinishida rasmiylashtiradi: markazda Entities (domen qoidalari), keyin Use Cases, so'ng Interface Adapters, eng tashqarida Frameworks & Drivers. Asosiy qoida - Dependency Rule: source kod bog'liqligi faqat ichkariga qarab yo'naltirilishi shart, tashqi halqa nomlari ichki halqada hech qachon ko'rinmaydi. Qatlamlar o'rtasida ma'lumot oddiy struktura (DTO/record)lar orqali uzatiladi. Natijada biznes qoidalari UI, DB va framework hayot davridan uzoqroq yashaydi.

Kitob bu rasmga ikki aniqlik kiritadi va ikkisi ham amalda ko'p o'tkazib yuboriladi. Birinchisi halqa soniga tegishli: *Clean Architecture* ning 22-bobidagi "Only Four Circles?" bo'limi diagrammani sxematik deb ataydi, to'rttadan ko'proq halqa kerak bo'lishi mumkin va "doim aynan shu to'rttasi bo'lsin" degan qoida yo'q. O'zgarmas narsa faqat Dependency Rule, ya'ni bog'liqlikning doim ichkariga qarashi va ichkariga borgan sari abstraksiya hamda siyosat darajasining oshishi: eng tashqi halqa past darajali konkret detal, eng ichkisi esa eng umumiy va eng yuqori daraja. Bu ikki tomonga ishlaydi - to'rtta halqani majburiy sanab, har biri uchun alohida model yasash ham, kerakli beshinchi chegarani "sxemada yo'q" deb rad etish ham xato.

Ikkinchisi arxitekturaning birinchi vazifasiga tegishli. Kitobning 16-bobi yaxshi arxitektura qo'llab-quvvatlashi kerak bo'lgan narsalarni sanaydi va ro'yxatning birinchisi - use case lar: arxitektura tizimning niyatini qo'llab-quvvatlashi shart va bu arxitektorning birinchi tashvishi hamda arxitekturaning birinchi prioriteti. Arxitektura tizim xatti-harakatiga kuchli ta'sir qilmaydi, lekin uning qila oladigan eng muhim ishi bor: xatti-harakatni ochiq ko'rsatish. Savat ilovasi yaxshi arxitektura bilan savat ilovasiga O'XSHAB turadi, use case lar tizim tuzilmasida ko'rinib turadi va dasturchi xulqni qidirib yurmaydi, chunki u tizimning yuqori darajasida birinchi darajali element, ya'ni funksiyasini aniq aytadigan nom bilan sinf, funksiya yoki modul sifatida turadi. Amalda bu `usecase` paketidagi nom `OrderManager` emas, `PlaceOrder` va `CancelOrder` bo'lishini bildiradi; talabning kuchli shakli [baqiruvchi arxitektura](#1229-baqiruvchi-arxitektura-screaming-architecture) bo'limida.

**Spring'da qayerda uchraydi:** Amalda `domain` (Java `record` va entity'lar), `application` (use case interfeyslari va ularning implementatsiyalari), `adapter-in-web`, `adapter-out-persistence` kabi Gradle subproject'lar sifatida tashkil etiladi; Spring faqat eng tashqi modullarda mavjud bo'ladi. Use case'lar bitta metodli interfeyslar (`CreateOrderUseCase`) sifatida yozilib, implementatsiyalari `@Service` va `@Transactional` bilan tashqi konfiguratsiyada bezatiladi. Java 17+ `record`, `sealed interface` va pattern matching ichki halqalarni ixcham va immutable ushlab turish uchun juda qulay. Spring Boot 3.x auto-configuration'i esa ataylab faqat `adapter`/`bootstrap` modullarida qoldiriladi.

**Qo'llanish keyslari:**
- Uzoq umr ko'rishi kutilayotgan yadroviy bank yoki billing platformasi.
- Bir nechta jamoa bir domen ustida ishlaganda, use case'lar aniq shartnoma rolini o'ynaydi.
- Framework migratsiyasi rejalashtirilgan tizimlar (masalan monolitdan modullarga o'tish).
- Regulyatsiya talab qiladigan biznes qoidalarni alohida, auditga tushunarli modulda saqlash.
- Domen logikasi uchun yuqori test qoplamasi majburiy bo'lgan loyihalar.

**Ehtiyot bo'ling:** Clean Architecture'ni "har bir halqa uchun alohida model" deb mexanik tushunish mapping do'zaxiga olib keladi - 4 qatlamli mapping zanjirlari xatolar manbaiga aylanadi va ishlab chiqish tezligini pasaytiradi. Agar jamoa Dependency Rule'ni ArchUnit yoki modul chegaralari bilan majburlamasa, bir yildan keyin bu faqat paket nomlari qolgan oddiy layered arxitektura bo'lib chiqadi.

```text
com.example
  domain/        Order, Money            (hech kimga bog'liq emas)
  usecase/       PlaceOrder, CancelOrder (domain ga bog'liq)
  adapter/
    in/web/      OrderController         (usecase ga bog'liq)
    out/persistence/ OrderJpaAdapter     (usecase portlarini amalga oshiradi)

Qoida bitta: bog'liqlik har doim ichkariga qaraydi.
ArchUnit bilan:
  layeredArchitecture().consideringAllDependencies()
    .layer("domain").definedBy("..domain..")
    .layer("usecase").definedBy("..usecase..")
    .layer("adapter").definedBy("..adapter..")
    .whereLayer("domain").mayOnlyBeAccessedByLayers("usecase", "adapter")
    .whereLayer("adapter").mayNotBeAccessedByAnyLayer()
```

## 12.4 Piyoz arxitekturasi (Onion Architecture)

**Tavsif:** Clean Architecture'ning DDD'ga yaqin varianti: markazda Domain Model, uning ustida Domain Services, keyin Application Services, eng tashqarida Infrastructure va UI. Asosiy urg'u - infrastruktura (DB, ORM, messaging) hech qachon markazda emas, balki eng tashqi, almashtiriladigan halqada bo'lishi; repository interfeyslari domen ichida e'lon qilinadi. Hexagonal'dan farqi shundaki, Onion ichki halqalarni DDD terminlarida (Aggregate, Domain Service, Specification) aniq ajratadi. Bu uslub "database-centric" fikrlashdan "domain-centric" fikrlashga o'tishni rasmiylashtiradi.

**Spring'da qayerda uchraydi:** `OrderRepository` interfeysi domen paketida yashaydi, uning `JpaOrderRepository` implementatsiyasi esa infrastructure paketida Spring Data `JpaRepository` yoki `JdbcClient` (Spring Framework 6.1+) ustida yoziladi. Domen ichida `@DomainEvents`/`AbstractAggregateRoot` yoki Spring Modulith'ning `ApplicationEventPublisher` orqali domen hodisalari tarqatiladi. Application service'lar `@Service` + `@Transactional` bilan belgilanadi, infrastructure konfiguratsiyasi `@Configuration` sinflarida izolyatsiya qilinadi. `spring-boot-starter-validation` orqali input validatsiyasi tashqi halqada, biznes invariantlari esa aggregate ichida saqlanadi.

**Qo'llanish keyslari:**
- DDD bilan modellashtirilayotgan boy domen: logistika, trading, sug'urta polislari.
- Ko'p marta ishlatiladigan domen qoidalari bir nechta ilova (web + batch) tomonidan chaqirilsa.
- DB sxemasi domen modeliga mos kelmaydigan legacy bazalar ustida yangi logika qurishda.
- Domen modelini bazadan mustaqil, in-memory fake repository'lar bilan test qilish talab qilinganda.
- Monolitdan keyinchalik bounded context'larni ajratib olish rejasi bo'lganda.

**Ehtiyot bo'ling:** Onion va Clean/Hexagonal o'rtasidagi farqlar juda kichik, shuning uchun jamoada terminologiya urushiga aylanib, haqiqiy muammo - domen modelini boyitish - e'tibordan chetda qolishi mumkin. Agar domen halqasi JPA annotatsiyalari va lazy proxy'lar bilan to'lsa, "infrastructure tashqarida" degan asosiy va'da buziladi.

```java
// Onion: markazda domen modeli, tashqarida infratuzilma
// 1-qatlam (markaz): Order, Money - hech qanday import yo'q
// 2-qatlam: OrderRepository interfeysi (domen xizmatlari)
// 3-qatlam: PlaceOrderService (ilova xizmatlari)
// 4-qatlam (tashqi): JPA, REST, Kafka adapterlari

// Farqi hexagonal dan: Onion qatlamlarni aniq sanab beradi,
// hexagonal esa faqat "ichkari va tashqari" deydi. Amalda ikkisi
// bir xil natijaga olib keladi: domen hech narsaga bog'liq emas.
@Entity class OrderEntity { }        // 4-qatlam
public record Order(OrderId id) { }  // 1-qatlam, JPA annotatsiyasi yo'q
```

## 12.5 Vertikal qatlamli arxitektura (Vertical Slice Architecture)

**Tavsif:** Kod gorizontal texnik qatlamlar emas, balki feature (use case) bo'yicha vertikal "tilim"larga bo'linadi: har bir tilim o'z controller, handler, so'rov/javob modeli va DB kirishini o'zida saqlaydi. Maqsad - o'zgarishni bitta papkada lokalizatsiya qilish, ya'ni yangi funksiya qo'shganda 5 xil qatlamga tegmaslik. Tilimlar o'rtasida kodni majburan umumlashtirish ataylab minimallashtiriladi; takrorlanish bog'liqlikdan afzal deb hisoblanadi. Har bir tilim o'ziga mos murakkablik darajasini tanlashi mumkin - oddiy query uchun to'g'ridan-to'g'ri SQL, murakkab komanda uchun to'liq aggregate.

**Spring'da qayerda uchraydi:** `features/placeorder/PlaceOrderController.java`, `PlaceOrderHandler.java`, `PlaceOrderRequest.java` ko'rinishidagi paket tuzilishi; handler'lar `@Component` sifatida ro'yxatdan o'tadi. Mediator uslubi uchun Spring Framework 6.x'da o'z `CommandBus` abstraksiyasini `ObjectProvider`/generic `ResolvableType` orqali yozish yoki jmolecules/`spring-modulith` bilan birlashtirish keng tarqalgan; .NET'dagi MediatR'ning Java analoglari sifatida kichik kutubxonalar ishlatiladi, lekin ko'p loyihada qo'lda yozilgan ixcham bus ham yetarli bo'ladi. Query tilimlarida `JdbcClient` yoki jOOQ bilan to'g'ridan-to'g'ri proyeksiya o'qish qulay. Chegaralarni ArchUnit'ning `slices().matching("..features.(*)..")` qoidasi bilan tekshirish mumkin.

**Qo'llanish keyslari:**
- Ko'p mustaqil feature'li product-oriented jamoalar, har bir jamoa o'z tilimiga egalik qiladi.
- Read va write yo'llari juda farq qiladigan ilovalar (murakkab query'lar + sodda komandalar).
- Tez evolyutsiya qilayotgan SaaS mahsulotlari, bunda feature'lar qo'shiladi va o'chiriladi.
- Katta monolitni keyinchalik modullarga ajratishdan oldin feature chegaralarini aniqlashda.
- Ichki qatlamlararo abstraksiyalar foyda bermayotgan, "service → repository → service" zanjirlari ortiqcha bo'lgan loyihalarda.

**Ehtiyot bo'ling:** Umumiy biznes invariantlari bir necha tilimda takrorlansa, bitta qoidaning ikki xil versiyasi paydo bo'lib, nomuvofiqlik xatolari yuzaga keladi - shuning uchun haqiqiy domen qoidalari uchun umumiy domen moduli saqlanishi kerak. Shuningdek tilimlar o'rtasida DB jadvallarini erkin ulashish yashirin bog'lanish hosil qiladi va keyinchalik modullarni ajratishni qiyinlashtiradi.

```text
com.example.orders
  placeorder/
    PlaceOrderController.java
    PlaceOrderService.java
    PlaceOrderRequest.java
    PlaceOrderTest.java
  cancelorder/
    CancelOrderController.java
    CancelOrderService.java

Bitta o'zgarish bitta papkaga tegadi, shuning uchun koheziya yuqori.
Narxi: umumiy kod qayerda turishi haqida qaror kerak, aks holda
takrorlanish boshlanadi. Umumiy qismni `shared/` ga chiqarish qoidasi
oldindan yozilgan bo'lishi kerak.
```

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
- Bir nechta jamoa bitta kod bazasida ishlayotganda, chegara kodda majburlanadi.
- Tranzaksion yaxlitlik muhim bo'lgan domenlar - bir DB tranzaksiyasi hali ham mumkin. Ford va boshqalar servisni bo'lmaslik sabablari (granularity integrators) ro'yxatida ACID tranzaksiya talabini birinchi o'ringa qo'yadi.
- Operatsion byudjet cheklangan startaplar: bitta deployment, bitta monitoring stack.
- Mikroservislardan "qaytish" (monolit konsolidatsiyasi) loyihalarida maqsadli arxitektura sifatida.

**Ehtiyot bo'ling:** Agar modullar bir xil DB sxemasidagi jadvallarni o'zaro erkin o'qisa, kodda modullilik bo'lsa ham ma'lumot darajasida qattiq bog'lanish saqlanadi - har bir modulga o'z jadval/sxemasi berilishi kerak. Yana bir tuzoq: `verify()` testini CI'ga qo'shmaslik, natijada chegaralar bir necha sprintdan keyin e'tiborsiz qolib buziladi.

## 12.7 Mikroyadro / Plugin arxitekturasi (Microkernel / Plugin Architecture)

**Tavsif:** Richards va Ford bu uslubni ikki komponentdan iborat deb ta'riflaydi: core system va plug-in komponentlar. Core system rasmiy ta'rifga ko'ra tizimni ishga tushirish uchun zarur minimal funksionallik; muqobil ta'rif - ilovadagi "happy path", ya'ni maxsus ishlovi deyarli yo'q umumiy oqim. Cyclomatic complexity'ni core'dan olib plugin'larga ko'chirish kengaytirilishi, qo'llab-quvvatlanishi va test qilinishini yaxshilaydi. Plugin'lar mustaqil va o'zi yetarli bo'lishi, ideal holda bir-biriga bog'liq bo'lmasligi kerak; ular compile-based (o'zgarsa butun monolit qayta deploy qilinadi) yoki runtime-based (OSGi, Jigsaw kabi mexanizm bilan ishlash vaqtida qo'shiladi va olinadi) bo'ladi. Plugin'ni topish uchun plug-in registry ishlatiladi: unda plugin nomi, data kontrakti va chaqirish usuli yoziladi. Yadro odatda layered yoki modulli monolit sifatida quriladi va butun monolit bitta bazani bo'lishadi. Plugin'ni REST yoki messaging orqali alohida servis qilish ham mumkin, lekin kitob ogohlantiradi: bu arxitekturani tarqatilganga aylantiradi va shunda ham har bir so'rov core'dan o'tgani uchun quantum bitta bo'lib qoladi.

**Reyting (*Fundamentals of Software Architecture*, 12-bob):** kuchli tomoni soddalik va umumiy narx; testability, deployability, reliability, modularity, extensibility va performance uch yulduz (o'rtadan bir oz yuqori); scalability va fault tolerance zaif, chunki deploy monolit bo'ladi. Bu kitobda bir vaqtda domen va texnik bo'linish bo'lishi mumkin bo'lgan yagona uslub deb ko'rsatilgan.

**Spring'da qayerda uchraydi:** Spring'ning o'zi shu uslubdan keng foydalanadi: `spring.factories`/`META-INF/spring/org.springframework.boot.autoconfigure.AutoConfiguration.imports` fayllari orqali auto-configuration plugin'lari topiladi, `@ConditionalOnClass`/`@ConditionalOnMissingBean` esa plugin aktivligini boshqaradi. O'z ilovangizda strategiya plugin'larini `List<PaymentProvider>` yoki `Map<String, PaymentProvider>` ko'rinishida inject qilish, yoki Java `ServiceLoader` va `module-info.java` (JPMS) bilan haqiqiy pluggability qurish mumkin. Spring Plugin (`spring-plugin-core`) kutubxonasi `Plugin<S>` interfeysi va `PluginRegistry` bilan aniq extension point modelini beradi - Spring Data REST shu asosda ishlaydi. Izolyatsiyalangan class loading kerak bo'lsa, PF4J yoki OSGi (Apache Karaf) tanlanadi.

**Qo'llanish keyslari:**
- Mijozga xos biznes qoidalari ko'p bo'lgan korporativ mahsulotlar (ERP, CRM moslashtirishlari).
- To'lov/yetkazib berish provayderlarini plugin sifatida qo'shiladigan e-commerce platformalari.
- Hujjat yoki fayl formatlari uchun kengaytiriladigan import/export konvertorlari.
- Qoidalar dvigateli (rules engine) uchun strategiya plugin'lari, har biri mustaqil deploy qilinadi.
- IDE/CI kabi developer tooling, uchinchi tomon kengaytmalarini qo'llab-quvvatlovchi.

**Ehtiyot bo'ling:** Plugin kontraktini noto'g'ri loyihalash eng katta xavf: interfeys juda tor bo'lsa plugin'lar yadroni "aylanib o'tish" uchun hack qiladi, juda keng bo'lsa har bir o'zgarish barcha plugin'larni buzadi. Richards va Ford kontraktni butun plugin to'plami uchun standart ushlashni, uchinchi tomon o'z kontrakti bilan kelganda esa adapter qo'yishni tavsiya qiladi. Bir JVM'da ishlayotgan plugin'lar xotira, thread va exception darajasida izolyatsiyalanmagan - ishonchsiz uchinchi tomon kodi uchun alohida class loader yoki process kerak.

```java
// Mikroyadro: o'zak kichik, imkoniyat plugin bilan qo'shiladi
public interface ReportPlugin {
    String format();                                 // "pdf", "xlsx"
    byte[] render(ReportModel model);
}

@Service
public class ReportKernel {
    private final Map<String, ReportPlugin> plugins;

    public ReportKernel(List<ReportPlugin> all) {     // konteyner yig'adi
        this.plugins = all.stream()
                .collect(Collectors.toMap(ReportPlugin::format, p -> p));
    }

    public byte[] render(String format, ReportModel m) {
        return plugins.getOrDefault(format, plugins.get("pdf")).render(m);
    }
}
// Yangi format = yangi bean. O'zak kodi o'zgarmaydi.
```

## 12.8 Quvurlar va filtrlar (Pipes and Filters)

**Tavsif:** [Enterprise Integration Patterns I bobidagi quvurlar va filtrlar yozuvi](15-enterprise-integration-patterns-i-xabarlar.md#153-quvurlar-va-filtrlar-pipes-and-filters) bu patternning to'liq yozuvi, bu yerda faqat arxitektura uslubi nuqtai nazari: butun tizim holatsiz filter'lar zanjiri sifatida quriladi va quvur in-memory kolleksiya, reactive stream yoki haqiqiy message queue bo'lishi mumkin. Richards va Ford quvurni bir yo'nalishli va odatda point-to-point deb ta'riflaydi (broadcast emas, performance uchun), filter'ni esa o'zi yetarli, boshqalardan mustaqil, odatda holatsiz va faqat bitta vazifani bajaradigan deb belgilaydi; murakkab vazifa bitta filter emas, filter ketma-ketligi bilan yechiladi. Kitob to'rt tur filter sanaydi: producer (boshlanish nuqtasi, faqat chiqish), transformer (kirishni o'zgartirib uzatadi, funksional dunyoda `map`), tester (mezonni tekshirib natijani shartli chiqaradi, `reduce` ga o'xshash) va consumer (oqimning tugash nuqtasi). Hohpe va Woolf bu uslubni messaging tizimlari uchun fundamental arxitektura uslubi deb beradi va uni Regine Meunier yozuvi hamda POSA katalogiga bog'laydi; ularda filter umumiy tashqi interfeysga ega bo'lgani uchun filter'ni qo'shish, olib tashlash va tartibini o'zgartirish filter kodiga tegmasdan bo'ladi.

**Reyting (*Fundamentals of Software Architecture*, 11-bob):** kuchli tomoni umumiy narx, soddalik va modullilik (filter turlari orasidagi mas'uliyat ajratilishi); deployability va testability o'rtacha, lekin qatlamli uslubdan bir pog'ona yuqori; reliability uch yulduz; elasticity va scalability bir yulduz va fault tolerance yo'q, chunki deploy monolit bo'ladi va butun birlik bitta filter'ning xatosidan yiqiladi.

**Spring'da qayerda uchraydi:** Kanonik yozuvdagi Spring Integration va Spring Cloud Stream'dan tashqari Spring Batch'ning `ItemReader → ItemProcessor → ItemWriter` zanjiri, in-memory pipeline sifatida Project Reactor `Flux` operatorlari (`map`, `filter`, `flatMap`, `buffer`), tarqatilgan quvur uchun reaktiv `Function<Flux<T>, Flux<R>>` bean'lari va Servlet qatlamidagi `jakarta.servlet.Filter` hamda Spring Security `SecurityFilterChain`.

**Qo'llanish keyslari:**
- Kunlik ETL (fayl o'qish, validatsiya, boyitish, DB'ga yozish) yoki HTTP so'rovidagi kesishgan mas'uliyatlar zanjiri (auth, rate limit, audit log) kabi bosqichlari mustaqil almashtiriladigan oqimni qurish.

**Ehtiyot bo'ling:** Qaysi bosqichda qayta urinish, qaysi birida dead-letter'ga yuborish aniq loyihalanmasa ma'lumot yo'qoladi yoki dublikat paydo bo'ladi, holatsizlik va kanal hop xarajati tafsiloti esa kanonik yozuvda.

## 12.9 Hodisaga asoslangan arxitektura (Event-Driven Architecture - broker va mediator topologiyalari)

**Tavsif:** Komponentlar bir-birini to'g'ridan-to'g'ri chaqirmaydi, balki sodir bo'lgan faktlar - hodisalar orqali aloqa qiladi. Richards va Ford uslubda ikki asosiy topologiyani ajratadi. Broker topologiyasida markaziy mediator yo'q va xabar oqimi event processor'lar bo'ylab zanjirsimon tarqaladi; uning to'rt komponenti: initiating event (oqimni boshlaydigan hodisa), event broker, event processor va processing event. Initiating event'ni bitta processor qabul qiladi, o'z vazifasini bajaradi va nima qilganini processing event sifatida e'lon qiladi; boshqalari shu hodisani tinglab reaksiya qiladi va o'z navbatida yangi processing event chiqaradi, hodisa hech kimni qiziqtirmay qolguncha. Kitob buni estafeta poygasiga qiyoslaydi: tayoqchani uzatgan yuguruvchi poygadan chiqadi. Mediator topologiyasida markazda event mediator turadi va uning komponentlari: initiating event, event queue, event mediator, event channel'lar va event processor'lar. Mediator faqat hodisani qayta ishlash qadamlarini biladi, mos processing event'larni point-to-point kanallarga yuboradi va processor'lar ishni tugatganini unga qaytaradi - broker topologiyasidan farqli ravishda ular tizimga hech narsa e'lon qilmaydi. Amalda mediator bitta bo'lmaydi: kitob har bir domen yoki hodisa guruhi uchun alohida mediator qo'yishni tavsiya qiladi, bu yagona nosozlik nuqtasini kamaytiradi va o'tkazuvchanlikni oshiradi.

**Reyting (*Fundamentals of Software Architecture*, 14-bob):** performance, scalability, fault tolerance va evolyutsion rivojlanish besh yulduz; soddalik va testability nisbatan past, chunki hodisa oqimi deterministik emas va "event tree" diagrammalari yuzlab, hatto minglab ssenariyga yoyiladi. Quantum soni bittadan ko'pga qarab o'zgaradi: processor'lar bitta baza nusxasini bo'lishsa yoki request-reply bilan bir-birini kutsa, ular bitta quantum ichida qoladi.

**Spring'da qayerda uchraydi:** Process ichida `ApplicationEventPublisher`, `@EventListener`, `@TransactionalEventListener(phase = AFTER_COMMIT)` va `@Async` broker-uslubidagi publish/subscribe beradi. Tarqatilgan holatda `@KafkaListener` (`spring-kafka`), `@RabbitListener` (`spring-amqp`), yoki Spring Cloud Stream binder'lari ishlatiladi; ishonchli publikatsiya uchun Spring Modulith'ning Event Publication Registry yoki transactional outbox pattern qo'llanadi. Mediator topologiyasi uchun Spring Integration'ning `IntegrationFlow`/router'lari, Spring Statemachine, yoki Camunda/Temporal kabi tashqi workflow dvigatellari bilan integratsiya tanlanadi. Kuzatuvchanlik Micrometer Tracing (Spring Boot 3.x) orqali hodisalar bo'ylab trace context tarqatish bilan ta'minlanadi.

**Qo'llanish keyslari:**
- Buyurtma yaratilganda ombor, to'lov va bildirishnoma xizmatlarini mustaqil ishga tushirish.
- Audit va analitika uchun domen hodisalarini data lake'ga oqizish.
- Mikroservislar o'rtasidagi tarqatilgan tranzaksiyalarni saga sifatida boshqarish (mediator).
- IoT yoki telemetriya oqimlarini real vaqtda qayta ishlash va alert generatsiya qilish.
- Legacy tizimni "hodisalar bilan o'rash" - strangler fig migratsiyasida.

**Ehtiyot bo'ling:** Richards va Ford broker topologiyasining kamchiliklarini aniq sanaydi: oqimni boshqarish yo'q, xatoni ushlash qiyin, biznes tranzaksiyasini tiklash (recoverability) va qaytadan boshlash imkoni yo'q, ma'lumot nomuvofiqligi paydo bo'ladi. Sabab oddiy: hech bir komponent asl biznes so'rovining holatiga egalik qilmaydi, shuning uchun to'lov processor'i yiqilsa hech kim bundan xabar topmaydi, ombor esa zaxirani kamaytirib ishini davom ettiradi. Shu sababli bu topologiyada tracing, correlation ID va hodisa katalogi majburiy. Eventual consistency'ni mahsulot talablari bilan kelishmasdan tanlash ham tipik xato: foydalanuvchi darhol ko'rishi kerak bo'lgan natijani asinxron hodisaga topshirish UX muammolari va ikki marta yuborilgan buyurtmalarga olib keladi.

```java
// Broker topologiyasi: ishtirokchilar bir-birini bilmaydi
@Component
class OrderPlacedListener {
    @KafkaListener(topics = "orders.placed", groupId = "warehouse")
    void on(OrderPlaced e) { warehouse.reserve(e.orderId()); }
}
// Afzalligi: yangi iste'molchi qo'shish hech kimga tegmaydi.
// Narxi: butun oqimni hech kim ko'rmaydi, nosozlikni kuzatish qiyin.

// Mediator topologiyasi: markazda orkestrator, qadamlar aniq
@Component
class CheckoutSaga {
    void on(OrderPlaced e) {
        commands.send(new ReserveStock(e.orderId()));      // 1
        commands.send(new ChargePayment(e.orderId()));     // 2
    }
    void on(PaymentFailed e) {
        commands.send(new ReleaseStock(e.orderId()));      // kompensatsiya
    }
}
```

## 12.10 Buyruq va so'rovlar mas'uliyatini ajratish (CQRS - Command Query Responsibility Segregation)

**Tavsif:** Yozish (command) va o'qish (query) yo'llari turli modellar, ba'zan turli ma'lumotlar bazalari bilan amalga oshiriladi. Command modeli biznes invariantlarini himoya qiladi va normalizatsiyalangan bo'ladi, query modeli esa UI ehtiyojiga moslashtirilgan denormalizatsiyalangan proyeksiyalardan iborat. Bu ikki yo'lni mustaqil optimallashtirish va mustaqil masshtablash imkonini beradi. Oddiy shaklda bu faqat kod darajasidagi ajratish (bir DB), kuchli shaklda - alohida read store va asinxron proyeksiya yangilash.

**Spring'da qayerda uchraydi:** Eng ko'p uchraydigan amaliy ko'rinish: yozish uchun JPA/Hibernate aggregate'lari (`@Entity`, `EntityManager`), o'qish uchun `JdbcClient`, `NamedParameterJdbcTemplate` yoki jOOQ bilan to'g'ridan-to'g'ri proyeksiya DTO'lari - Spring Data'ning interface-based projection'lari (`List<OrderSummary> findBy...`) ham shu maqsadda ishlatiladi. Read store sifatida Elasticsearch (`spring-data-elasticsearch`) yoki Redis (`spring-data-redis`) ishlatilganda, proyeksiyalar `@TransactionalEventListener` yoki Kafka consumer'lari orqali yangilanadi. Spring Modulith'ning `@ApplicationModuleListener` proyeksiya yangilashni ishonchli (transactional outbox bilan) bajarish uchun qulay. Axon Framework'ning Spring Boot starter'i to'liq CQRS infratuzilmasini (`@CommandHandler`, `@QueryHandler`) beradi.

**Qo'llanish keyslari:**
- O'qish yuklamasi yozishdan sezilarli ko'p bo'lgan katalog yoki dashboard tizimlari.
- Murakkab qidiruv va filtrlash talab qilinadigan UI'lar, bunda normallashtirilgan sxema sekin.
- Bir domen ustida juda ko'p turli hisobot ko'rinishlari kerak bo'lganda.
- Yozish tomoni qat'iy invariantlarga ega bo'lgan moliyaviy operatsiyalar + tez reporting.
- Event sourcing bilan birga: hodisalardan bir nechta ixtisoslashgan proyeksiya qurish.

**Ehtiyot bo'ling:** Alohida read store tanlash bilan siz avtomatik ravishda eventual consistency'ni qabul qilasiz - "saqlagandan keyin ro'yxatda ko'rinmaydi" muammosi UX va test darajasida oldindan hal qilinishi kerak. Newman CQRS'ni masshtablash vositasi sifatida qaraganda eng qiyin shakllardan biri deb hisoblaydi va avval arzonroq variantlarni sinashni tavsiya qiladi: agar muammo faqat o'qishda bo'lsa, read replica ancha kam riskli va tezroq yo'l. U yana CQRS ham, event sourcing ham dasturchining fikrlash tarzini o'zgartirishni talab qilishini va bu kognitiv yukni oqlash kerakligini ta'kidlaydi. Oddiy CRUD domenida to'liq CQRS ortiqcha, shuning uchun avval bir DB ichidagi yengil ajratishdan boshlash to'g'ri.

```java
// Yozuv modeli: invariant va tranzaksiya
@Service
class OrderCommandService {
    @Transactional
    public void place(PlaceOrder cmd) {
        Order order = Order.from(cmd);       // boy domen modeli
        orders.save(order);
    }
}

// O'qish modeli: so'rovga mos, denormallashtirilgan, invariant yo'q
@Service
class OrderQueryService {
    public List<OrderListRow> list(OrderFilter f) {
        return jdbc.sql("SELECT id, customer_name, total FROM order_list_view WHERE ...")
                   .query(OrderListRow.class).list();
    }
}
// CQRS ikki ombor degani emas: bir bazada ikki model ham CQRS.
// Ikki ombor bo'lsa sinxronlash kechikishi paydo bo'ladi va u
// foydalanuvchiga ko'rinishi kerak.
```

## 12.11 Hodisalarni saqlash (Event Sourcing)

**Tavsif:** Tizim holati joriy snapshot ko'rinishida emas, balki sodir bo'lgan o'zgarmas hodisalar ketma-ketligi sifatida saqlanadi; joriy holat shu hodisalarni qayta o'ynatish (replay) orqali tiklanadi. Bu to'liq audit tarixi, vaqt bo'ylab orqaga qaytish (temporal query) va bir xil tarixdan yangi proyeksiyalar qurish imkonini beradi. Ishlash uchun snapshot'lar, optimistic concurrency (stream versiyasi) va hodisa sxemasi evolyutsiyasi mexanizmlari zarur. Deyarli har doim CQRS bilan birga ishlatiladi, chunki event stream'dan to'g'ridan-to'g'ri o'qish amaliy emas.

**Spring'da qayerda uchraydi:** Spring'da tayyor event store yo'q, shuning uchun Axon Framework (Spring Boot starter, `@Aggregate`, `@EventSourcingHandler`, `AggregateLifecycle.apply()`) yoki EventStoreDB'ning Java client'i tanlanadi; ko'p jamoalar esa oddiy `events` jadvalini `JdbcClient`/JPA bilan o'zlari quradi (aggregate_id, version, type, payload, unique(aggregate_id, version)). Hodisalarni tashqariga ishonchli chiqarish uchun transactional outbox yoki Debezium CDC + Kafka ishlatiladi. Proyeksiyalar Spring'ning `@TransactionalEventListener` yoki `@KafkaListener` bean'lari bilan yangilanadi. Jackson `@JsonTypeInfo` va versiyalangan payload sinflari sxema evolyutsiyasini boshqarish uchun qo'llanadi.

**Qo'llanish keyslari:**
- Bank hisobvaraqlari va ledger tizimlari, bunda har bir o'zgarish sababini bilish shart.
- Regulyativ audit talab qiladigan sug'urta polisi yoki tibbiy yozuvlar tarixi.
- Murakkab holat mashinalari: buyurtma hayot sikli, logistika yuk harakati.
- Biznes analitikasi uchun o'tmishdagi ma'lumotlardan yangi proyeksiyalar qurish zaruriyati.
- Nizolarni hal qilish va "nima bo'lgan edi?" savollariga aniq javob kerak bo'lgan domenlar.

**Ehtiyot bo'ling:** Newman event sourcing uchun o'rni juda mos keladigan holatlar borligini, lekin u bilan birga hisobga olinishi shart bo'lgan bir qator bosh og'riq kelishini aytadi, shuning uchun uni tanlash ongli qaror bo'lishi kerak. Amalda eng katta xavf - hodisa sxemasining evolyutsiyasi: hodisalar abadiy saqlanadi, shuning uchun eski versiyalarni o'qish (upcasting) strategiyasi birinchi kundan kerak, aks holda bir yildan keyin replay ishlamay qoladi. Shuningdek GDPR'dagi "o'chirish huquqi" immutable log bilan ziddiyatda (crypto-shredding talab qiladi), va bu uslubni oddiy CRUD domenga qo'llash jamoani sezilarli operatsion murakkablik bilan yuklaydi - faqat haqiqatan tarix biznes qiymatiga ega bo'lganda tanlang.

```java
// Holat saqlanmaydi, hodisalar saqlanadi
public class Account {
    private final List<DomainEvent> pending = new ArrayList<>();
    private BigDecimal balance = BigDecimal.ZERO;
    private long version;

    public void withdraw(Money amount) {
        if (balance.compareTo(amount.amount()) < 0) throw new InsufficientFundsException();
        apply(new MoneyWithdrawn(amount, version + 1));   // qoida tekshirildi
    }

    void apply(DomainEvent e) {                           // holatni yangilash
        switch (e) {
            case MoneyWithdrawn w -> balance = balance.subtract(w.amount().amount());
            case MoneyDeposited d -> balance = balance.add(d.amount().amount());
            default -> throw new IllegalStateException();
        }
        version = e.version();
        pending.add(e);
    }
}
// Hodisa sxemasi abadiy o'qiladi: uni versiyalash rejasi boshidan kerak
```

## 12.12 Mikroservislar (Microservices)

**Tavsif:** Tizim mustaqil deploy qilinadigan, o'z ma'lumot bazasiga ega bo'lgan kichik servislarga bo'linadi va ular tarmoq orqali (HTTP/gRPC yoki message broker) muloqot qiladi. Richards va Ford uslub nomini Martin Fowler va James Lewis'ning 2014 yil mart oyida chiqqan "Microservices" maqolasi mashhur qilganini, g'oyaning o'zi esa Domain-Driven Design'dan, xususan bounded context tushunchasidan oziqlanganini yozadi: bounded context ichidagi kod va sxema bir-biri bilan bog'langan, lekin tashqariga hech qachon bog'lanmaydi. Shu sababli uslub qayta ishlatish o'rniga takrorlanishni afzal ko'radi, chunki qayta ishlatishning narxi - bog'lanish. Newman esa uslubning o'zagi sifatida mustaqil deploy qilinishini ko'rsatadi: bitta servisga o'zgarish kiritib, boshqa hech narsani deploy qilmasdan uni foydalanuvchiga chiqarish - shunchaki imkoniyat emas, balki qabul qilingan odat bo'lishi kerak. Buning sharti - servislar bo'sh bog'langan bo'lishi, kontrakt aniq va barqaror bo'lishi; bazani bo'lishish esa alohida muammoli. Uchinchi tamoyil - servis o'z holatiga egalik qiladi: boshqa servisning ma'lumoti kerak bo'lsa, u ma'lumotni emas, servisning o'zini so'raydi.

**Reyting (*Fundamentals of Software Architecture*, 17-bob):** kuchli tomoni scalability, elasticity va evolyutsion rivojlanish; avtomatlashtirilgan deploy va testability ham yuqori baholangan. Fault tolerance normal sharoitda yuqori (mustaqil, bir vazifali servislar), lekin servislar aro sinxron aloqa ko'payganda fault tolerance ham reliability ham pasayadi. Performance ko'pincha muammo: tarmoq chaqiruvlari metod chaqiruvidan ancha qimmat va har bir endpoint'da xavfsizlik tekshiruvi qo'shimcha vaqt oladi. Kitob taqsimlangan uslub bo'lgani uchun servis chegarasidan o'tuvchi tranzaksiyadan voz kechishni maslahat beradi va shu sababli granularlik tanlovini bu uslubda muvaffaqiyat kaliti deb ataydi.

**Spring'da qayerda uchraydi:** Har bir servis alohida Spring Boot 3.x/4.x ilovasi bo'ladi; servislar aro chaqiruvlar uchun `RestClient` (Spring Framework 6.1+), `WebClient` yoki `@HttpExchange` bilan deklarativ HTTP interface (`HttpServiceProxyFactory`); service discovery uchun `spring-cloud-starter-netflix-eureka-client` yoki Kubernetes'da `spring-cloud-starter-kubernetes-client-discovery`; konfiguratsiya uchun `spring-cloud-starter-config`; chidamlilik uchun `spring-cloud-starter-circuitbreaker-resilience4j` va `@CircuitBreaker`; API Gateway uchun `spring-cloud-gateway` (`RouteLocator`, `GatewayFilter`); kuzatuv uchun Micrometer Tracing (`io.micrometer:micrometer-tracing-bridge-otel`) va `management.tracing.sampling.probability`.

**Qo'llanish keyslari:**
- Marketplace platformasida katalog, buyurtma, to'lov va yetkazib berish servislari alohida jamoalar tomonidan mustaqil relizlanadi.
- Qora juma kunida faqat `checkout-service` nusxalari ko'paytiriladi, qolgan servislar o'z o'lchamida qoladi.
- Bank'da legacy core'ni bosqichma-bosqich almashtirishda yangi funksiyalar alohida servis sifatida yoziladi (Strangler Fig).
- Fraud detection servisi Python/ML stack'da, qolgan tizim Java'da - texnologiya tanlovi servis darajasida bo'linadi.
- SaaS mahsulotida har bir jamoa kuniga bir necha marta o'z servisini deploy qiladi va boshqa jamoalarni kutmaydi.

**Ehtiyot bo'ling:** Mikroservislarni tashkiliy tayyorlik (CI/CD, observability, on-call) bo'lmaganda joriy qilish "distributed monolith"ga olib keladi - servislar bir vaqtda deploy qilinishi shart bo'lib qoladi va kechikish ortadi. Bir nechta servis bitta ma'lumot bazasiga yozsa, Ford va boshqalarining o'lchoviga ko'ra ular bitta arxitektura quantum'i bo'lib qoladi: mustaqil deploy ham, mustaqil masshtablash ham yo'qoladi.

```text
Servisni BO'LISH sabablari (Hard Parts, granularity disintegrators):
  service scope    - servis bir-biriga aloqasiz ishlarni qilayotganmi
  code volatility  - o'zgarish faqat bitta qismga tegayotganmi
  scalability      - qismlar turlicha masshtablanishi kerakmi
  fault tolerance  - bir qismdagi xato kritik funksiyani yiqitadimi
  security access  - ayrim qismga qattiqroq kirish nazorati kerakmi
  extensibility    - servisga doim yangi kontekst qo'shilayotganmi

Servisni BIRLASHTIRISH sabablari (granularity integrators):
  database transactions - servislar orasida ACID tranzaksiya kerakmi
  workflow              - servislar bir-biri bilan gaplashishi shartmi
  shared code           - umumiy kodni bo'lishish kerakmi
  data relationships    - ma'lumotning o'zi bo'linadimi

To'g'ri granularlik shu ikki kuch muvozanatidan chiqadi: faqat
bo'lish sabablariga qarab, birlashtirish sabablarini e'tiborsiz
qoldirish kitobda keng tarqalgan xato deb ko'rsatilgan.
```

## 12.13 O'z-o'ziga Yetarli Tizimlar (Self-Contained Systems)

**Tavsif:** Tizim bir nechta yirik, vertikal to'liq (UI + logika + ma'lumot bazasi) mustaqil ilovaga bo'linadi va ular bir-biriga asosan asinxron yoki UI darajasida integratsiya qilinadi. Har bir SCS o'z web UI'siga ega bo'ladi, shuning uchun sinxron servis-servis chaqiruvlari minimumga tushadi va mikroservislarning tarmoq murakkabligidan qochiladi. Integratsiya ustuvorligi: UI havolalari → asinxron replikatsiya → eng oxirida sinxron API. Bu mikroservis va monolit o'rtasidagi "o'rta yo'l" uslubi.

**Spring'da qayerda uchraydi:** Har bir SCS to'liq Spring Boot ilovasi bo'ladi: `spring-boot-starter-web` + server-side rendering uchun Thymeleaf (`spring-boot-starter-thymeleaf`) yoki JTE, o'z `DataSource`/Flyway migratsiyalari bilan. SCS'lar aro integratsiya uchun `spring-kafka` (`@KafkaListener`) yoki `spring-boot-starter-amqp` orqali event replikatsiyasi; UI kompozitsiyasi uchun `spring-cloud-gateway` yoki Edge Side Includes (nginx SSI); keshlangan ma'lumot nusxalari uchun `@Cacheable` va Caffeine/Redis.

**Qo'llanish keyslari:**
- Yirik e-commerce'da "Search", "Product", "Checkout", "Account" har biri o'z UI'si bilan mustaqil tizim bo'ladi.
- Insurance kompaniyasida "Polis sotish" va "Da'volar" tizimlari alohida jamoalarga, alohida relizga ega.
- Bir nechta mustaqil jamoa bitta portalda ishlaydi, lekin umumiy deploy oynasini kutishni xohlamaydi.
- Davlat xizmatlari portali: har bir xizmat moduli alohida tizim, umumiy faqat SSO va dizayn tizimi.
- Monolitdan chiqishda ko'p mayda servis o'rniga bir nechta yirik vertikal tizimga bo'lish tanlanadi.

**Ehtiyot bo'ling:** SCS'lar orasida ma'lumotni replikatsiya qilish zarur bo'lgani uchun eventual consistency bilan yashashga tayyor bo'lishingiz kerak; agar jamoalar sinxron API'larga qayta tushib ketsa, uslubning asosiy foydasi yo'qoladi. UI'da umumiy dizayn tizimi versiyalanmasa, foydalanuvchi bir portalda bir nechta "boshqa" ilovani ko'radi.

```yaml
# Self-contained system: har tizim o'z UI, logika va bazasi bilan to'liq
checkout-scs:
  ui: server-side rendered (o'z sahifalari)
  logic: o'z servislari
  data: o'z bazasi
  integration: havola va asinxron hodisa (sinxron chaqiruv emas)

# Microservice dan farqi: SCS UI ni ham o'z ichiga oladi, shuning uchun
# bitta jamoa funksiyani boshdan oxir yetkazadi va sinxron chaqiruvlar
# zanjiri paydo bo'lmaydi. Integratsiya eng kuchsiz bog'liqlik bilan:
# brauzerda havola yoki fragment.
```

## 12.14 Servisga Yo'naltirilgan Arxitektura (Service-Oriented Architecture, SOA)

**Tavsif:** Korporativ funksiyalar qayta ishlatiladigan, shartnoma asosidagi servislar sifatida e'lon qilinadi va ularni markazlashgan integratsiya qatlami bog'laydi, yo'naltiradi va formatlarini o'giradi. Richards va Ford bu uslubni (ular orchestration-driven service-oriented architecture deb ataydi) o'z davri kontekstida izohlaydi: 1990-yillar oxirida operatsion tizim va baza litsenziyalari qimmat bo'lgani uchun arxitektorlardan maksimal qayta ishlatish talab qilindi va qayta ishlatish uslubning hukmron falsafasiga aylandi. Kitob servislarning aniq taksonomiyasini keltiradi: business services (eng yuqorida, kodsiz, faqat kirish, chiqish va sxema; `ExecuteTrade`, `PlaceOrder` kabi, ularni biznes foydalanuvchilari belgilaydi), enterprise services (mayda granulali umumiy implementatsiyalar; `CreateCustomer`, `CalculateQuote`), application services (bitta ilovaga tegishli, qayta ishlatilmaydigan servislar) va infrastructure services (monitoring, logging, autentifikatsiya, avtorizatsiya). Markazda orchestration engine turadi: u business servislarni enterprise servislar ustida yig'adi, tranzaksiya chegaralarini belgilaydi va integratsiya hub'i rolini o'ynaydi; baza esa servis-per-database emas, bitta yoki bir nechta umumiy relyatsion baza bo'ladi.

**Reyting (*Fundamentals of Software Architecture*, 16-bob):** deployability va testability halokatli past, chunki bu maqsadlar o'sha davrda muhim ham sanalmagan; elasticity va scalability ma'lum darajada qo'llab-quvvatlangan (vendor'lar sessiya replikatsiyasiga ko'p kuch sarflagani uchun); performance juda past, chunki har bir biznes so'rovi arxitekturaning juda ko'p qismiga bo'linadi; soddalik va narx esa arxitektor xohlaganining teskarisi - murakkab va qimmat. Kitob uni distributed uslub bo'lsa-da bitta quantum deb hisoblaydi: umumiy baza va orkestratsiya dvigateli gigant bog'lanish nuqtasi bo'lib, arxitekturaning hech bir qismi mediatordan boshqa xossaga ega bo'la olmaydi; shu bilan uslub monolit va tarqatilgan arxitekturaning kamchiliklarini bir vaqtda to'playdi.

**Spring'da qayerda uchraydi:** Spring Web Services (`spring-ws-core`) bilan contract-first SOAP endpoint'lari: `@Endpoint`, `@PayloadRoot`, `MessageDispatcherServlet`, WSDL generatsiyasi uchun `DefaultWsdl11Definition`, XSD'dan JAXB sinflari; klient tomonda `WebServiceTemplate`. Integratsiya va routing uchun Spring Integration (`IntegrationFlow`, `@ServiceActivator`, `MessageChannel`) yoki Apache Camel'ning `camel-spring-boot-starter`'i; xabar almashinuvi uchun JMS (`JmsTemplate`, `@JmsListener`) va IBM MQ/ActiveMQ. Tranzaksion integratsiya uchun `JtaTransactionManager` (Jakarta EE serverida yoki Narayana bilan).

**Qo'llanish keyslari:**
- Bankda mainframe'dagi hisob ma'lumotlari ESB orqali SOAP servis sifatida internet-banking va mobil ilovaga beriladi.
- Telekom operatorida bitta "mijozni ulash" jarayoni bir nechta backend tizimni ESB orqali orkestratsiya qiladi.
- Sug'urta kompaniyasi davlat reyestrlari bilan WS-Security talab qiladigan SOAP shartnomalar orqali integratsiyalashadi.
- ERP (SAP) va CRM o'rtasida kanonik ma'lumot modeliga o'girish Camel route'lari bilan amalga oshiriladi.
- Regulyator tomonidan WSDL/XSD shartnoma majburiy bo'lgan B2B integratsiyalar.

**Ehtiyot bo'ling:** ESB markaziy "single point of failure" va tashkiliy tiqilinchga aylanadi. Richards va Ford buni Conway qonuni bilan bog'laydi: orkestratsiya dvigatelini saqlovchi integratsiya arxitektorlari jamoasi tashkilotda siyosiy kuchga, oxirida esa byurokratik tiqilinchga aylanadi. Newman esa SOA va microservices farqini soddaroq qo'yadi: servislar kichraytirilgan bo'lsa ham, agar hammasi bitta bazaga bog'langan va birga deploy qilinadigan bo'lsa, bu microservices emas. Tranzaksiyani orkestratsiya vositasiga topshirish nazariyada yaxshi ko'rinsa ham, amalda to'g'ri tranzaksiya granularligini topish asta-sekin imkonsiz bo'lib boradi. Yangi loyihada SOAP/ESB'ni "korporativ standart" deb tanlash ko'pincha ortiqcha: REST/event-driven yetarli bo'lgan joyda XML transformatsiyalari va governance narxini to'lamang.

```java
// SOA: korxona darajasidagi umumiy servislar va shartnomalar
// Microservice dan asosiy farqi: umumiy ESB va umumiy kanonik model.
@Component
public class CustomerServiceGateway {          // ESB orqali chaqiruv
    private final WebServiceTemplate soap;

    public CustomerInfo lookup(String taxId) {
        GetCustomerRequest req = new GetCustomerRequest();
        req.setTaxId(taxId);                   // kanonik korxona modeli
        return ((GetCustomerResponse) soap.marshalSendAndReceive(req)).getCustomer();
    }
}
// Kanonik model afzalligi: bir marta kelishiladi. Narxi: uni o'zgartirish
// barcha tizimni bog'laydi, shuning uchun o'zgarish sekinlashadi.
```

## 12.15 Serverless / FaaS (Serverless / Function as a Service)

**Tavsif:** Biznes logika qisqa yashovchi, holatsiz funksiyalar sifatida yoziladi va platforma ularni so'rov yoki hodisa kelganda ishga tushiradi. Burns FaaS foydasini asosan dasturchi tomonida ko'radi: koddan ishlayotgan servisgacha bo'lgan masofa qisqaradi, chunki manba kodidan boshqa artefakt yasash yoki yuborish kerak emas; trafik ortganda funksiya nusxalari avtomatik ko'payadi, xato yoki mashina nosozligida funksiya boshqa mashinada qayta ishga tushadi. Funksiyalar holatsiz bo'lgani uchun ular ustiga qurilgan tizim bir binarga qurilganidan ko'proq modulli va bo'sh bog'langan bo'ladi. Burns "serverless" va "event-driven FaaS" ni ajratishni so'raydi: ko'p ijarali konteyner orkestratori serverless, lekin event-driven emas; o'z mashinalaringizda ishlayotgan open source FaaS esa event-driven, lekin serverless emas.

**Spring'da qayerda uchraydi:** Spring Cloud Function biznes logikani oddiy `java.util.function.Function`, `Supplier` yoki `Consumer` bean sifatida yozishga imkon beradi va uni HTTP, Kafka yoki cloud trigger'lariga bog'laydi (`spring.cloud.function.definition`, `FunctionCatalog`). Adapterlar: `spring-cloud-function-adapter-aws` (`FunctionInvoker` handler), Azure va GCP adapterlari. Cold start uchun Spring Boot 3.x'ning GraalVM native image qo'llab-quvvatlashi (`spring-boot-maven-plugin` `native` profili, `@RegisterReflectionForBinding`) yoki Class Data Sharing (`-XX:SharedArchiveFile`, Spring Boot 3.3+ CDS qo'llab-quvvatlashi) ishlatiladi. Knative/Kubernetes'da esa oddiy Spring Boot web ilovasi nolga scale bo'ladi.

```java
@Bean
public Function<OrderEvent, Receipt> handleOrder(PricingService pricing) {
    return event -> pricing.priceAndStore(event);
}
```

**Qo'llanish keyslari:**
- S3'ga yuklangan fayl uchun thumbnail generatsiya qiluvchi funksiya yuklash hodisasida ishga tushadi.
- Kunda bir marta ishlaydigan hisobot eksport jarayoni doimiy pod o'rniga funksiya sifatida yuritiladi.
- Webhook qabul qiluvchi endpoint (to'lov provayderi callback'i) notekis trafikda avtomatik scale bo'ladi.
- Kafka topic'dan kelgan hodisalarni boyitib boshqa topic'ga yozadigan yengil transformator.
- Chat-bot yoki IoT telemetriya uchun qisqa, holatsiz qayta ishlash qadamlari.

**Ehtiyot bo'ling:** Burns FaaS'ning to'rt cheklovini aniq sanaydi. Birinchisi - majburiy ajralish narxi: har bir funksiya butunlay mustaqil, yagona aloqa tarmoq orqali va funksiya nusxasida lokal xotira bo'lishi mumkin emas, shuning uchun butun holat tashqi saqlash servisida turadi; natijada servisning yaxlit manzarasini ko'rish, funksiyalar bir-biri bilan qanday bog'langanini va nima uchun buzilganini aniqlash qiyinlashadi (kitobdagi misol: bir-birini chaqiruvchi uch funksiya cheksiz tsikl yasaydi va buni koddan sezish qiyin). Ikkinchisi - funksiya nusxasining ishlash vaqti cheklangan, shuning uchun video transkodlash yoki log arxivlash kabi uzoq fon ishlari uchun FaaS yomon moslashgan. Uchinchisi - so'rovga javob berish uchun xotiraga ko'p ma'lumot yuklash kerak bo'lsa (masalan qidiruv indeksi), funksiya foydalanuvchi kutib turgan paytda ko'tarilgani uchun bu seziladigan kechikish beradi. To'rtinchisi - narx modeli: so'rov kam bo'lganda per-request to'lov foydali, ammo trafik protsessorni doimiy band qiladigan darajaga o'sganda bu model yomonlashadi, chunki so'rov narxi so'rov soniga qarab chiziqli o'sadi, virtual mashina narxi esa yadro qo'shilgani sari arzonlashadi. Shuning uchun funksiya ichida ulanish pool'i, uzoq tranzaksiya yoki holat saqlashga tayanmang.

## 12.16 Kosmosga Asoslangan Arxitektura (Space-Based Architecture)

**Tavsif:** Uslub nomini tuple space tushunchasidan oladi: umumiy xotira orqali gaplashadigan bir nechta parallel protsessor. Richards va Ford uning maqsadini aniq qo'yadi - markaziy bazani sinxron cheklov sifatida olib tashlash va o'rniga replikatsiya qilinadigan in-memory data grid'dan foydalanish; ma'lumot xotirada turadi va barcha faol processing unit'lar o'rtasida replikatsiya qilinadi, processing unit ma'lumotni o'zgartirganda uni asinxron ravishda, odatda doimiy navbat orqali bazaga yuboradi. Kitob besh komponentni sanaydi: processing unit (ilova kodi hamda in-memory data grid va replikatsiya dvigateli), virtualized middleware (ichida messaging grid, data grid, processing grid va deployment manager), data pump (o'zgargan ma'lumotni asinxron yuboradi), data writer (shu o'zgarishlarni bazaga yozadi) va data reader (ishga tushishda bazadan ma'lumotni o'qib processing unit'ga beradi). Kitobga ko'ra bazaning bo'g'iz bo'lishi yo'qolgani uchun ilova ichida deyarli cheksiz masshtablanish ochiladi va millionlab bir vaqtli foydalanuvchini qayta ishlash mumkin bo'ladi.

**Reyting (*Fundamentals of Software Architecture*, 15-bob):** elasticity, scalability va performance besh yulduz - bu uslubning asosiy sababi. Buning evaziga soddalik past, testability bitta yulduz (yuz minglab bir vaqtli foydalanuvchini sinab ko'rish qimmat va murakkab, shuning uchun yuqori hajmli test ko'pincha haqiqiy production yuklamasida bajariladi), narx esa yuqori: kesh mahsulotlari litsenziyasi va yuqori resurs sarfi hisobiga.

**Spring'da qayerda uchraydi:** Hazelcast (`hazelcast-spring`, `HazelcastInstance`, `IMap`, `spring-boot-starter-cache` bilan `HazelcastCacheManager`) yoki Apache Ignite'ning Spring integratsiyasi (`IgniteSpringBean`, `SpringCacheManager`); Redis ishlatilsa `spring-boot-starter-data-redis` va `RedisTemplate`. Keshni deklarativ boshqarish uchun `@EnableCaching`, `@Cacheable`, `@CacheEvict`; sessiyani grid'ga ko'chirish uchun Spring Session (`spring-session-hazelcast` yoki `spring-session-data-redis`). Grid'dan ma'lumot bazasiga asinxron oqim uchun `spring-kafka` va `@KafkaListener` bilan yozuvchi batch jarayonlar.

**Qo'llanish keyslari:**
- Konsert chiptalari sotuvida bir vaqtli urinishlar soni oldindan noma'lum va o'rindiq holati grid'da saqlanadi.
- Onlayn garov (betting) platformasida koeffitsiyentlar va stavkalar in-memory grid'da yangilanadi.
- Trading tizimida order book RAM'da turadi, savdo tarixi asinxron ravishda bazaga yoziladi.
- Flash-sale e-commerce aksiyasida stok hisobi `IMap` ustida atomik operatsiyalar bilan yuritiladi.
- Yuqori hajmli real-time reyting/leaderboard hisob-kitobi.

**Ehtiyot bo'ling:** Oddiy CRUD ilovaga bu uslubni qo'llash ortiqcha - grid replikatsiyasi, split-brain va cache-to-database oqimining nosozligi tufayli ma'lumot yo'qolishi riski real. Grid'dagi barcha ma'lumot RAM'da yashashini va node yo'qolganda qayta taqsimlanishini (rebalance paytidagi latency sakrashini) hisobga olmasa, tizim eng kerakli daqiqada sekinlashadi.

```java
// Space-based: holat taqsimlangan xotira panjarasida, baza orqa planda
@Bean
Config hazelcastConfig() {
    Config config = new Config();
    config.getMapConfig("sessions")
            .setBackupCount(1)                  // nusxa: bitta node yiqilsa saqlanadi
            .setInMemoryFormat(InMemoryFormat.OBJECT)
            .setTimeToLiveSeconds(1800);
    config.getMapConfig("cart")
            .setMapStoreConfig(new MapStoreConfig()
                    .setImplementation(new CartMapStore())
                    .setWriteDelaySeconds(5));  // bazaga asinxron ko'chadi
    return config;
}
// Maqsad: baza tor joy bo'lishdan chiqadi. Narxi: izchillik murakkab,
// split-brain xavfi va xotira narxi.
```

## 12.17 Klient-Server (Client-Server)

**Tavsif:** Richards va Ford bu uslubni fundamental qoliplar qatorida beradi: texnik funksionallikni frontend va backend o'rtasida ajratish, ya'ni two-tier yoki client/server arxitektura. Kitob uning uch ko'rinishini sanaydi: desktop ilova va alohida baza serveri (taqdimot mantiqi ish stolida, og'ir hisob-kitob mustahkam baza serverida), brauzer va web server (baza alohida bo'lsa ham, web va baza serverlari bir sinf mashinada ishlagani uchun bu hamon ikki qatlamli deb qaraladi) hamda 1990-yillar oxirida mashhur bo'lgan uch qatlamli variant: baza qatlami, application server boshqaradigan ilova qatlami va generatsiya qilingan HTML bilan frontend. Fowler buni tarqatish nuqtai nazaridan baholaydi: foydalanuvchi mashinasi va umumiy ma'lumot ombori boshqa-boshqa node bo'lgani uchun client-server ajralishi tipik va qochib bo'lmaydigan protsesslararo chegara.

**Spring'da qayerda uchraydi:** Server tomoni: `spring-boot-starter-web` (Servlet, Tomcat) yoki `spring-boot-starter-webflux` (Netty), `@RestController`, `@GetMapping`, `HttpMessageConverter`, autentifikatsiya uchun `spring-boot-starter-security` (`SecurityFilterChain`, `@EnableWebSecurity`, OAuth2 Resource Server). Klient tomoni Java'da: `RestClient`, `WebClient`, yoki `@HttpExchange` interface'lari. Ma'lumot bazasi - klient-server munosabatining ikkinchi qatlami: `DataSource` (HikariCP), `JdbcClient`, `spring-boot-starter-data-jpa`.

**Qo'llanish keyslari:**
- React SPA Spring Boot REST API bilan ishlaydi, autentifikatsiya JWT orqali.
- Mobil ilova (iOS/Android) bitta backend API'ga murojaat qiladi.
- Korxona ichidagi desktop JavaFX mijozi markaziy Spring Boot serveriga ulanadi.
- IoT qurilmalari telemetriyani markaziy qabul qiluvchi servisga yuboradi.
- Ichki admin paneli umumiy ma'lumot bazasiga faqat server orqali kirish beradi.

**Ehtiyot bo'ling:** Server yagona nosozlik nuqtasi bo'lgani uchun horizontal scaling va stateless dizayn (sessiyani serverda saqlamaslik) boshidan rejalashtirilishi kerak. Biznes qoidalarini klientga ko'chirib qo'ymang - validatsiya va avtorizatsiya har doim serverda takrorlanishi shart, aks holda klientni o'zgartirgan har kim qoidani chetlab o'tadi.

```java
// Klient-server: eng oddiy taqsimlash. Chegarada ikki narsa shart.
@Bean
RestClient pspClient(RestClient.Builder builder, PspProperties props) {
    return builder
            .baseUrl(props.url())
            // Boot 4.x: HttpClientSettings + ClientHttpRequestFactoryBuilder
            .requestFactory(ClientHttpRequestFactoryBuilder.detect().build(
                    HttpClientSettings.defaults()
                            .withConnectTimeout(Duration.ofSeconds(2))   // 1) timeout
                            .withReadTimeout(Duration.ofSeconds(5))))
            .defaultStatusHandler(HttpStatusCode::isError,
                    (req, res) -> { throw new PspException(res.getStatusCode()); })
            .build();                                                    // 2) xato tarjimasi
}
```

## 12.18 Broker (Broker)

**Tavsif:** Klient va servis bir-birini bilmaydi: o'rtada broker turib, xabarni mos iste'molchilarga yetkazadi. Hodisaga asoslangan arxitekturada bu [12.9](#129-hodisaga-asoslangan-arxitektura-event-driven-architecture---broker-va-mediator-topologiyalari) da keltirilgan broker topologiyasiga to'g'ri keladi: markaziy mediator yo'q, oqim yengil message broker orqali event processor'lar bo'ylab tarqaladi va bu topologiya hodisa oqimi nisbatan sodda bo'lganda, markaziy orkestratsiya kerak bo'lmaganda tanlanadi. Hohpe va Woolf xuddi shu tushunchani Message Broker yozuvi sifatida beradi. Broker yana retry, buffering va monitoring uchun yagona nuqta beradi; narxi - oqimni hech kim yaxlit ko'rmaydi.

**Spring'da qayerda uchraydi:** `spring-boot-starter-amqp` bilan RabbitMQ: `RabbitTemplate`, `@RabbitListener`, `Queue`/`TopicExchange`/`Binding` bean'lari, `DirectMessageListenerContainer`. Kafka uchun `spring-kafka`: `KafkaTemplate`, `@KafkaListener`, `ConcurrentKafkaListenerContainerFactory`, `DefaultErrorHandler` va `DeadLetterPublishingRecoverer`. Broker'dan abstraktsiya uchun Spring Cloud Stream (`spring-cloud-stream-binder-kafka`/`-rabbit`, funksional binding `spring.cloud.stream.bindings.*`). JMS uchun `JmsTemplate` va `@JmsListener`; WebSocket STOMP broker relay uchun `@EnableWebSocketMessageBroker` va `MessageBrokerRegistry`.

**Qo'llanish keyslari:**
- Buyurtma yaratilganda `OrderCreated` xabari broker'ga tushadi, uni ombor, hisob-faktura va notification servislari mustaqil o'qiydi.
- Og'ir PDF generatsiya ishlari navbatga qo'yiladi va worker'lar pool'i ularni iste'mol qiladi.
- Legacy tizim ishlamay turganda xabarlar navbatda saqlanadi va keyin qayta ishlanadi.
- Chat ilovasida xabarlar STOMP broker orqali obunachilarga tarqatiladi.
- Audit hodisalari bitta topic'ga yoziladi va bir nechta analitik iste'molchi tomonidan o'qiladi.

**Ehtiyot bo'ling:** Broker ko'rinmas markaziy bog'liqlikka aylanadi - uning to'xtashi butun tizimni to'xtatadi, shuning uchun klasterlash, dead-letter queue va idempotent consumer'lar majburiy. "At-least-once" yetkazish sababli bir xabar bir necha marta kelishi mumkin; iste'molchi idempotent bo'lmasa, dublikat buyurtma yoki ikki marta to'lov yuzaga keladi.

```java
// Broker: jo'natuvchi va qabul qiluvchi bir-birini bilmaydi
@Service
public class OrderEventPublisher {
    private final KafkaTemplate<String, OrderPlaced> kafka;

    public void publish(OrderPlaced e) {
        // Kalit: bir xil buyurtma uchun tartib saqlanadi (bir partition)
        kafka.send("orders.placed", String.valueOf(e.orderId()), e);
    }
}
// Broker yangi nosozlik rejimi qo'shadi: lag, rebalance, takroriy
// yetkazish va DLQ. Har iste'molchi idempotent bo'lishi shart.
```

## 12.19 Teng-Tengga (Peer-to-Peer)

**Tavsif:** Markaziy server o'rniga har bir node bir vaqtning o'zida klient ham, server ham bo'ladi va resurslarni bevosita o'zaro almashadi. Bu markaziy bo'g'iz, yagona nosozlik nuqtasi va markaziy infratuzilma narxi muammolarini hal qiladi. Node'lar bir-birini discovery (gossip, DHT yoki seed ro'yxati) orqali topadi va ma'lumot replikasi tarmoq bo'ylab tarqaladi. Narxi - murakkab consistency, xavfsizlik va topologiyani kuzatish qiyinligi.

**Spring'da qayerda uchraydi:** Spring ilovalari ko'pincha P2P'ni cluster kutubxonasi orqali oladi: Hazelcast embedded rejimida (`hazelcast-spring`, `HazelcastInstance`) node'lar teng a'zo sifatida gossip bilan klaster quradi; Infinispan'ning `infinispan-spring-boot3-starter`'i JGroups ustida ishlaydi. Eureka server'lar peer-to-peer replikatsiya qiladi (`eureka.client.service-url.defaultZone` bir nechta peer bilan). Blockchain/DLT integratsiyasida esa Spring Boot ilovasi Web3j (`web3j-spring-boot-starter` yoki `core` kutubxonasi) orqali P2P tarmoq node'iga ulanadi. Shuni ta'kidlash kerak: Spring Framework'ning o'zida maxsus P2P moduli yo'q.

**Qo'llanish keyslari:**
- Bir nechta Spring Boot instance embedded Hazelcast bilan umumiy keshni teng a'zolar sifatida ushlab turadi.
- Eureka server'larning o'zaro replikatsiyasi bilan discovery qatlami markaziy masterdan xoli bo'ladi.
- Blockchain hamyoni yoki tranzaksiya monitoringi uchun backend Ethereum node'iga ulanadi.
- Edge joylashuvlardagi node'lar markaziy serverga bog'liq bo'lmay o'zaro sinxronlanadi.
- Katta fayl tarqatish (CDN o'rniga ichki P2P tarqatish) bilan deploy artefaktlarini yoyish.

**Ehtiyot bo'ling:** P2P klasterni Kubernetes kabi dinamik muhitda ishlatganda split-brain va noto'g'ri discovery eng ko'p uchraydigan tuzoq - multicast o'rniga aniq peer ro'yxati yoki Kubernetes discovery plugin'ini ishlatish kerak. Agar sizga tranzaksion, qat'iy consistency kerak bo'lsa, P2P replikatsiyaga tayanmang; markaziy ma'lumot bazasi soddaroq va xatolari oldindan bilinadi.

```java
// P2P: tengdoshlar bir-birini topadi, markaz yo'q
// Java dunyosida bu ko'pincha klaster a'zoligi ko'rinishida uchraydi:
@Bean
Config p2pConfig() {
    Config c = new Config();
    JoinConfig join = c.getNetworkConfig().getJoin();
    join.getMulticastConfig().setEnabled(false);          // konteynerda ishlamaydi
    join.getKubernetesConfig().setEnabled(true)
            .setProperty("service-dns", "payments-headless.default.svc");
    return c;
}
// Biznes ilovalarida sof P2P kam uchraydi: operatsion murakkablik yuqori.
```

## 12.20 Qoratakhta (Blackboard)

**Tavsif:** [Xulq-atvor patternlari bobidagi qora taxta yozuvi](03-xulq-atvor-patternlari.md#323-qora-taxta-blackboard) bu patternning to'liq yozuvi, bu yerda faqat arxitektura uslubi nuqtai nazari: butun tizim umumiy bilim ombori atrofida quriladi, knowledge source modullari bir-birini bilmasdan faqat blackboard orqali muloqot qiladi va gipotezalar yetarli ishonch darajasiga yetganda yakuniy natija qabul qilinadi.

**Spring'da qayerda uchraydi:** Kanonik yozuvdagi `RedisTemplate`, `List<KnowledgeSource>` va event orqali boshqariladigan controller'dan tashqari umumiy holat uchun Hazelcast `IMap`, qoidalar dvigateli kerak bo'lsa Drools (`KieContainer` bean) va modullarni parallel ishlatish uchun `@Async` bilan `ThreadPoolTaskExecutor`.

**Qo'llanish keyslari:**
- Tibbiy tashxis yordamchisida laboratoriya, tasvir va anamnez modullari umumiy gipoteza to'plamini bosqichma-bosqich boyitadi.

**Ehtiyot bo'ling:** Umumiy holatga bir nechta modul parallel yozsa race condition va nondeterministik yakuniy natija paydo bo'ladi, shuning uchun versiyalash yoki optimistik lock majburiy, oddiy pipeline yetarli joyda esa bu uslub tanlanmaydi.

## 12.21 Reaktiv Arxitektura (Reactive Architecture)

**Tavsif:** Tizim asinxron, non-blocking xabar almashinuvi ustiga quriladi va shu orqali javobgarlik (responsive), chidamlilik (resilient), elastiklik va xabarga asoslanganlik xossalariga erishadi. Asosiy maqsad - ko'p sonli parallel, I/O'ga bog'liq so'rovni kam thread bilan xizmat qilish va backpressure orqali tizimni ortiqcha yuklanishdan saqlash. Blocking thread-per-request modelida minglab bir vaqtli ulanish thread pool'ni tugatadi; reaktiv modelda esa event loop ishlatiladi. Buning narxi - debug, stack trace va kognitiv murakkablikning oshishi.

**Spring'da qayerda uchraydi:** Spring WebFlux (`spring-boot-starter-webflux`), Reactor'ning `Mono`/`Flux` turlari, Netty server; non-blocking HTTP klient `WebClient`; funksional routing `RouterFunction`/`RouterFunctions.route()`. Reaktiv ma'lumot kirishi: R2DBC (`spring-boot-starter-data-r2dbc`, `DatabaseClient`, `ReactiveCrudRepository`), reaktiv Redis va MongoDB starter'lari. Xavfsizlik uchun `@EnableWebFluxSecurity` va `SecurityWebFilterChain`; xabarlar uchun Reactor Kafka yoki RSocket (`spring-boot-starter-rsocket`, `@MessageMapping`). Muqobil yo'l: Java 21+ virtual thread'lar (`spring.threads.virtual.enabled=true`) blocking kodni saqlab turib scalability beradi.

**Qo'llanish keyslari:**
- API Gateway ko'p sonli bir vaqtli ulanishni kam thread bilan proxy qiladi.
- Server-Sent Events orqali real-time narx yoki xabar oqimini brauzerga uzatish.
- Ko'p sonli tashqi servisga parallel chaqiruv qilib natijalarni birlashtiradigan aggregator servis.
- Katta fayl yoki ma'lumot oqimini xotiraga to'liq yuklamasdan `Flux` bilan streaming qilish.
- IoT yoki chat backend'i: uzun yashovchi ulanishlar soni serverdagi thread sonidan ancha ko'p.

**Ehtiyot bo'ling:** Reaktiv zanjir ichida bitta blocking chaqiruv (JDBC, `RestTemplate`, `Thread.sleep`) butun event loop'ni to'xtatadi - `BlockHound` bilan tekshirmasa bu xato ishlab chiqarishda topiladi. Oddiy CRUD ilovada WebFlux ko'pincha asossiz murakkablik: Java 21+ virtual thread'lar bilan MVC ko'p hollarda shu scalability'ni ancha soddaroq kod bilan beradi.

```java
// Reaktiv arxitektura: to'liq non-blocking zanjir
@RestController
class OrderReactiveApi {
    private final OrderReactiveRepository repo;        // R2DBC

    @GetMapping("/orders")
    Flux<OrderDto> stream() {
        return repo.findAll()                          // hech bir qadam bloklamaydi
                   .map(OrderDto::of)
                   .limitRate(100);                    // backpressure
    }
}
// Shart: butun zanjir reaktiv bo'lishi kerak. Bitta JDBC chaqiruvi
// event loop ni bloklaydi va butun foyda yo'qoladi.
```

## 12.22 Monolit (Monolith)

**Tavsif:** Richards va Ford arxitektura uslublarini ikki sinfga ajratadi: monolit (butun kod bitta deploy birligi) va tarqatilgan (bir nechta deploy birligi masofaviy protokol orqali ulangan); monolit sinfiga qatlamli, quvurli va mikroyadro uslublari kiradi. Monolitda modullar bir process ichida metod chaqiruvi bilan gaplashadi, shuning uchun tarqatilgan arxitekturalarning umumiy muammolari - kitob sanab o'tgan tarqatilgan hisoblash xatolari (fallacies of distributed computing, L. Peter Deutsch va Sun Microsystems hamkasblari, 1994) - bu yerda yo'q. Fowler buni qoida darajasiga ko'taradi: uning [taqsimlangan obyekt dizaynining birinchi qonuni](#1237-taqsimlangan-obyekt-dizaynining-birinchi-qonuni-first-law-of-distributed-object-design) "obyektlaringizni tarqatmang" deydi, chunki protsess ichidagi chaqiruv juda tez, protsesslar orasidagisi esa bir necha tartib sekin; ko'p protsessordan foydalanishning to'g'ri yo'li sifatida u klasterlashni, ya'ni barcha sinflarni bitta protsessga joylab, o'sha protsessning bir nechta nusxasini turli node'da ishlatishni ko'rsatadi. Zamonaviy ko'rinishi - modulli monolit: ichki modul chegaralari qat'iy nazorat qilinadi, lekin deploy bitta bo'lib qoladi.

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
- Kichik jamoa uchun operatsion yuk mikroservislardan ancha past bo'ladi.

**Ehtiyot bo'ling:** Modul chegaralari kod darajasida majburlanmasa, monolit tezda "big ball of mud"ga aylanadi - bir modul boshqasining repository'si va jadvaliga to'g'ridan-to'g'ri murojaat qila boshlaydi. Monolitni qo'rqib mikroservisga ko'chirishdan oldin haqiqiy sababni (deploy chastotasi, alohida scaling, jamoalar mustaqilligi) aniqlang; faqat "zamonaviy" bo'lish uchun bo'lish ko'pincha tizimni sekinlashtiradi.

## 12.23 Katta Loy To'pi (Big Ball of Mud) - anti-pattern

**Tavsif:** Atama Brian Foote va Joseph Yoder'ning 1997 yilda chiqqan maqolasidan olingan; Richards va Ford uni "hech qanday ko'rinadigan arxitektura strukturasining yo'qligi" deb izohlaydi va mualliflar ta'rifini keltiradi: tartibsiz qurilgan, yoyilgan, chala, skotch va sim bilan ushlab turilgan spagetti-kod; ma'lumot tizimning uzoq elementlari orasida tartibsiz bo'lishiladi, natijada muhim ma'lumotning deyarli hammasi global yoki takrorlangan bo'lib qoladi. Kitobga ko'ra tizimning umumiy strukturasi hech qachon aniq belgilanmagan, yoki belgilangan bo'lsa, tanib bo'lmas darajada yemirilgan. Hech kim uni ataylab loyihalashtirmaydi: sabab kod sifati va strukturasi ustidan boshqaruvning yo'qligi. Struktura yo'qligi o'zgarishni borgan sari qiyinlashtiradi va uslub deploy, testability, scalability hamda performance bo'yicha ham yutqazadi.

**Spring'da qayerda uchraydi:** Tipik ko'rinishi: `@Controller` ichida to'g'ridan-to'g'ri `JdbcTemplate`/`EntityManager` chaqiriladi, `@Service` sinflari bir-birini aylana bo'ylab inject qiladi (Spring Framework 6.x constructor injection'da buni `BeanCurrentlyInCreationException` bilan rad etadi, shuning uchun `@Lazy` yoki setter injection bilan "tuzatiladi"), hamma narsani qiladigan `UtilService`, hamma joyda `@Transactional` va `@Autowired` field injection. Nazorat vositalari bor: ArchUnit (`classes().that().resideInAPackage("..web..").should().onlyDependOnClassesThat()`), Spring Modulith `ApplicationModules.of(App.class).verify()`, Maven `jdepend`/`SpotBugs`, va `@SpringBootTest` ni butun context uchun ishlatish o'rniga slice testlar (`@WebMvcTest`, `@DataJpaTest`).

**Qo'llanish keyslari:**
- Legacy monolitni strangler fig bilan bosqichma-bosqich bo'lishdan oldin uning bog'lanish grafigini ArchUnit bilan o'lchash.
- Prototip yoki hackathon kodi - ataylab tartibsiz, lekin muddati tugagach tashlab yuboriladi.
- Due diligence: sotib olinayotgan mahsulotning texnik qarzini baholash.
- Jamoa chegaralarini aniqlash uchun "o'zgarish birgalikda sodir bo'ladigan" fayllarni git tarixidan topish.
- Refaktoring budjetini asoslash uchun o'lchanadigan metrikalar (cyclic dependency soni) yig'ish.

**Ehtiyot bo'ling:** Chegaralarni avval test bilan qotirib, keyin modullarni ajratish - tartibsizlikni kamaytirishning kam riskli yo'li. Teskari xato ham bor: tartibsizlikning yechimi ortiqcha abstraksiya emas, balki aniq chegaralardir, shuning uchun kichik jamoa uchun ko'p qatlamli ierarxiya qurish foyda bermaydi.

```text
Belgilari (o'lchanadigan, chegara qiymatini loyiha o'zi belgilaydi):
  - paket bog'liqligi grafida tsikl bor (jdeps yoki ArchUnit aniqlaydi)
  - bitta o'zgarish ko'p paketga tegadi (git tarixidan ko'rinadi)
  - eng katta sinf boshqalardan tartib farqi bilan kattaroq
  - test yozish uchun butun kontekstni ko'tarish kerak

ArchUnit bilan tsiklni to'sish:
  slices().matching("com.example.(*)..").should().beFreeOfCycles()

Davolash: butunlay qayta yozish emas, chegara qo'yishdan boshlanadi.
Eng ko'p o'zgaradigan modulni ajratib, unga aniq interfeys beriladi.
```

## 12.24 Taqsimlangan Monolit (Distributed Monolith) - anti-pattern

**Tavsif:** Bu tashqi ko'rinishda microservice bo'lgan, lekin ichkarida barcha servislar bir-biriga qattiq bog'langan va mustaqil deploy qilinmaydigan tizim. Belgisi: bitta biznes operatsiyasi uzun sinxron chaqiruvlar zanjirini talab qiladi, servislar umumiy bazani bo'lishadi va bitta DTO o'zgarsa hamma servisni birga relizga chiqarish kerak bo'ladi. Newman'ning o'lchovida bu uslub microservices emas, chunki mustaqil deploy - uslubning asosiy sharti, bazani bo'lishish esa unga eng ko'p to'sqinlik qiladigan tanlov. Ford va boshqalarining arxitektura quantum o'lchovi buni rasmiylashtiradi: mustaqil deploy qilinadigan artefakt yuqori funksional koheziyaga va statik bog'lanishga ega bo'lishi kerak, shuning uchun bitta bazani bo'lishgan servislar har doim bitta quantum bo'lib chiqadi. Richards va Ford orkestratsiyaga asoslangan SOA haqida aytgan xulosa shu holatga ham to'g'ri keladi: arxitektura monolit va tarqatilgan uslubning kamchiliklarini bir vaqtda to'playdi.

**Spring'da qayerda uchraydi:** Belgilari: barcha servislar bitta `common-dto` yoki `shared-entity` Maven modulini import qiladi; har bir servisda bir xil `spring.datasource.url`; `@FeignClient` yoki `RestClient` zanjiri bilan ko'p darajali sinxron chaqiruvlar; `@SharedEntity` sifatida bir xil JPA `@Entity` sinflari takrorlanadi. Yechim tomoni: har bir servis o'z schema'si (Flyway/Liquibase bilan alohida migratsiya), kontraktni OpenAPI + Spring Cloud Contract bilan versiyalash, sinxron chaqiruvlar o'rniga Spring Kafka/`spring-cloud-stream` orqali asinxron eventlar, `spring-cloud-circuitbreaker-resilience4j` bilan izolyatsiya, va Micrometer Tracing (OpenTelemetry) bilan chaqiruv zanjirining real chuqurligini o'lchash.

**Qo'llanish keyslari:**
- Mavjud microservice landshaftini audit qilib, "bitta so'rov necha servisga tegadi" ni Zipkin/Tempo trace'lari bilan o'lchash.
- Umumiy DTO kutubxonasini olib tashlab, har bir consumer uchun alohida kontrakt yaratish rejasini tuzish.
- Deploy bog'liqligini sinash: bitta servisni yakka o'zi relizga chiqarib ko'rish (coupling testi).
- Sinxron zanjirni event-driven saga'ga o'tkazish uchun nomzod oqimlarni tanlash.
- Shared database'dan database-per-service'ga o'tishda o'tish davri uchun view'lar yaratish.

**Ehtiyot bo'ling:** Eng xavfli holat - servis chegaralari biznes qobiliyatlari emas, texnik qatlamlar bo'yicha chizilgani (`user-api`, `user-logic`, `user-dao` alohida servis). Agar servislarni mustaqil deploy qila olmayotgan bo'lsangiz, ularni qaytib monolitga birlashtirish ko'pincha to'g'ri qaror.

```text
Belgilari:
  - bitta foydalanuvchi so'rovi uzun sinxron servis zanjirini chaqiradi
  - servislar bitta bazani bo'lishadi (demak bitta quantum)
  - bitta funksiyani chiqarish uchun bir nechta servisni birga deploy qilish kerak
  - bitta servis yiqilsa hammasi yiqiladi

Tekshiruv: trace dan sinxron chaqiruv zanjiri uzunligini o'lchang.
  SELECT trace_id, count(*) FROM spans WHERE kind = 'client'
  GROUP BY 1 ORDER BY 2 DESC LIMIT 20;

Davolash: zanjirni asinxron hodisaga aylantirish yoki servislarni
qayta birlashtirish. Microservice nomi natijani o'zgartirmaydi.
```

## 12.25 Hujayra Asosidagi Arxitektura (Cell-Based Architecture)

**Tavsif:** Tizim bir-biridan to'liq izolyatsiya qilingan "hujayra"larga (cell) bo'linadi, har bir hujayra butun stack'ning mustaqil nusxasi bo'lib, foydalanuvchilarning aniq bir qismiga xizmat qiladi. Trafik cell router orqali shard kaliti (tenant ID, foydalanuvchi ID) bo'yicha yo'naltiriladi. Bitta hujayra ishdan chiqsa, faqat o'sha hujayradagi foydalanuvchilar ta'sirlanadi - bu "blast radius" ni cheklash usuli. Bu yerdagi tavsif korpusning amaliy umumlashtirmasi: uslub bu korpusdagi kitoblarda alohida bob sifatida yozilmagan, shuning uchun uning xossalari yulduz reytingi bilan taqqoslanmaydi.

**Spring'da qayerda uchraydi:** Spring'da maxsus annotatsiya yo'q - bu infratuzilma va routing darajasidagi pattern. Amalda: har bir cell alohida Kubernetes namespace yoki alohida AWS region/AZ guruhida ishlaydigan bir xil Spring Boot 3.x image; routing Spring Cloud Gateway (`spring-cloud-starter-gateway-server-webflux`) ichida `RoutePredicateFactory` yoki custom `GlobalFilter` bilan tenant kaliti bo'yicha amalga oshiriladi; cell ichida konfiguratsiya Spring Cloud Config yoki Kubernetes ConfigMap orqali profile (`spring.profiles.active=cell-eu-1`) bilan beriladi. Multi-tenant ma'lumot izolyatsiyasi uchun `AbstractRoutingDataSource` yoki Hibernate 6 `MultiTenantConnectionProvider` + `CurrentTenantIdentifierResolver` ishlatiladi; har bir cell uchun Micrometer tag (`cell=eu-1`) bilan alohida metrikalar yig'iladi.

**Qo'llanish keyslari:**
- Yirik B2B SaaS: har bir enterprise tenant guruhi o'z hujayrasida, shovqinli qo'shni (noisy neighbour) ta'sirini yo'qotish.
- Reliability maqsadi: deployni bitta hujayradan boshlab (canary cell) bosqichma-bosqich chiqarish.
- Ma'lumot suvereniteti: EU mijozlari uchun alohida hujayra, GDPR talablariga javob berish.
- Juda yirik mijozni alohida (single-tenant) hujayraga ko'chirish, kodni o'zgartirmasdan.
- Load testda hujayra sig'imini o'lchab, o'sishni "yana bitta cell qo'shish" bilan rejalashtirish.

**Ehtiyot bo'ling:** Operatsion narx yuqori - N hujayra degani N marta monitoring, migratsiya va reliz jarayoni, shuning uchun to'liq avtomatlashtirilgan CI/CD va IaC bo'lmasa boshlamang. Shuningdek, hujayralar orasida tenant'ni ko'chirish (rebalancing) alohida, murakkab muammo bo'lib, uni loyihaning boshida o'ylab qo'yish kerak.

```yaml
# Cell-based: nosozlik bitta hujayra ichida qoladi
cells:
  - name: cell-a
    tenants: [t1, t2, t3]
    stack: {app: 3 pod, db: own instance, cache: own}
  - name: cell-b
    tenants: [t4, t5]
    stack: {app: 3 pod, db: own instance, cache: own}

router:
  strategy: tenant-id-hash      # tenant har doim bir xil hujayraga tushadi

# Afzalligi: blast radius bitta hujayra. Reliz ham hujayra-hujayra.
# Narxi: infratuzilma nusxalanadi va marshrutlash qatlami qo'shiladi.
```

## 12.26 Hech Narsani Bo'lishmaslik (Shared-Nothing)

**Tavsif:** Kleppmann uchta masshtablash arxitekturasini qiyoslaydi. Shared-memory arxitekturada ko'p CPU, RAM va disk bitta operatsion tizim ostida birlashadi, lekin narx chiziqlidan tez o'sadi, ikki barobar katta mashina ikki barobar yuklamani ko'tarmaydi va u bitta geografik joyga bog'langan. Shared-disk arxitekturada mashinalarning CPU va RAM'i alohida, lekin disk massivi umumiy; bu yerda contention va locking overhead masshtablashni cheklaydi. Shared-nothing arxitekturada (u yana horizontal scaling yoki scaling out deb ataladi) har bir node o'z CPU, RAM va diskini mustaqil ishlatadi va node'lar orasidagi koordinatsiya faqat dasturiy darajada, oddiy tarmoq orqali bo'ladi. Kleppmann foydasini ham, narxini ham ko'rsatadi: maxsus apparat kerak emas, shuning uchun narx/samaradorlik nisbati eng yaxshi mashinalarni tanlash, ma'lumotni bir nechta regionga tarqatish va butun datacenter yo'qolishidan omon qolish mumkin; buning evaziga ilovaga qo'shimcha murakkablik tushadi va ma'lumot modelining ifodaviyligi cheklanadi. Amaliyotda to'liq "nothing" kam uchraydi: application layer stateless bo'ladi, umumiy baza esa qoladi.

**Spring'da qayerda uchraydi:** Spring Boot'da stateless ilovaning standart yo'li: HTTP session'ni node xotirasida saqlamaslik - Spring Session (`spring-session-data-redis`, `spring-session-jdbc`) orqali tashqariga chiqarish, yoki JWT bilan umuman session'siz ishlash (`SessionCreationPolicy.STATELESS` Spring Security 6.x `SecurityFilterChain` ichida). Lokal `ConcurrentMapCacheManager` o'rniga taqsimlangan cache (`spring-boot-starter-data-redis`, Hazelcast, Caffeine faqat lokal read-only ma'lumot uchun); `@Scheduled` job'lar har bir node'da takrorlanmasligi uchun ShedLock yoki Quartz JDBC JobStore; fayllarni lokal diskka emas, S3/MinIO ga yozish. `@Async` va virtual threadlar (Java 21+, `spring.threads.virtual.enabled=true`) node ichidagi parallelizm uchun, lekin node'lar o'rtasida holat bo'lishilmaydi.

**Qo'llanish keyslari:**
- Kubernetes'da HPA bilan avtomatik masshtablanadigan stateless REST servis.
- Batch ishlovni partitionlab bir nechta worker pod'ga tarqatish (Spring Batch remote partitioning).
- Blue/green yoki rolling deploy: node'larni istalgan vaqtda o'ldirish mumkin, chunki ularda noyob holat yo'q.
- Ko'p AZ bo'ylab tarqatilgan API gateway backendlari.
- Serverless (AWS Lambda + Spring Cloud Function) muhiti, bunda instance umri qisqa.

**Ehtiyot bo'ling:** "Stateless" degan ilovalar amalda yashirin holat saqlaydi - lokal fayl cache, static mutable field, in-memory rate limiter yoki scheduler lock - va bu faqat ikkinchi instance qo'shilganda ko'rinadi. Ma'lumotlar bazasi hamon umumiy resurs bo'lib qolgani uchun, shared-nothing application layer DB bottleneck'ini hal qilmaydi: sharding yoki read replica alohida qaror talab qiladi.

```yaml
# Shared-nothing: nusxalar hech narsani bo'lishmaydi.
# Sessiya ilovada saqlanmaydi (Spring Security da SessionCreationPolicy.STATELESS).
spring:
  jpa:
    open-in-view: false

# Shart bo'lgan narsalar:
#  - lokal fayl tizimiga yozilmaydi (yuklangan fayl -> S3)
#  - lokal kesh faqat qisqa TTL bilan, haqiqat manbasi emas
#  - rejalashtirilgan ish qulf bilan (ShedLock)
#  - sticky session kerak emas
# Shundan keyin gorizontal masshtab shunchaki nusxa sonini oshirish bo'ladi.
```

## 12.27 Lambda / Kappa Arxitekturasi (Lambda / Kappa Architecture)

**Tavsif:** Lambda arxitekturasi ma'lumotni ikki yo'ldan o'tkazadi: batch layer to'liq tarixni qayta hisoblab aniq natija beradi, speed layer esa real vaqtda taxminiy natija beradi, serving layer ularni birlashtiradi. Bu aniqlik va tezlikni bir vaqtda beradi, lekin bitta biznes logikani ikki marta - batch va stream uchun - yozishni talab qiladi. Kappa arxitekturasi batch layer'dan voz kechib, hammasini bitta stream pipeline bilan hal qiladi: tarixni qayta hisoblash kerak bo'lsa, log'ni boshidan qayta o'ynatiladi (replay). Kappa soddaroq, lekin uzoq saqlanadigan, qayta o'ynaladigan log (Kafka) talab qiladi.

**Spring'da qayerda uchraydi:** Spring ekotizimida: stream layer uchun Spring for Apache Kafka (`@KafkaListener`, `KafkaTemplate`) yoki Spring Cloud Stream (`spring-cloud-stream-binder-kafka`) funksional model bilan (`Function<KStream<K,V>, KStream<K,V>>` bean'lari Kafka Streams binder orqali); batch layer uchun Spring Batch 5.x (`Job`, `Step`, `ItemReader`/`ItemWriter`) yoki Spring Cloud Data Flow orqali task orkestratsiyasi. Kappa'da replay uchun consumer group offset'ini `KafkaConsumerBackoffManager` emas, balki `seekToBeginning` yoki yangi consumer group bilan boshqariladi; `spring-cloud-stream` da `spring.cloud.stream.kafka.bindings.<name>.consumer.resetOffsets=true` ishlatiladi. Serving layer odatda Spring Data (Cassandra, Elasticsearch, Redis) orqali o'qiladi.

**Qo'llanish keyslari:**
- Real vaqtda fraud detection (speed layer) + kechqurun aniq hisob-kitob va reconciliation (batch layer).
- IoT telemetriya: daqiqalik dashboard stream'dan, kunlik hisobot batch'dan.
- Marketing analitikasi: sessiya hodisalaridan agregat metrikalar, logika o'zgarsa Kappa bilan to'liq replay.
- Event-sourced tizimda yangi read model yaratish - eventlarni boshidan o'ynatib projection qurish.
- Clickstream'dan rekomendatsiya featurelarini real vaqtda yangilash.

**Ehtiyot bo'ling:** Bu bo'limdagi tavsiflar korpusning amaliy umumlashtirmasi; uslub bu korpusdagi kitoblarda alohida uslub sifatida yozilmagan va yulduz reytingi bilan taqqoslanmaydi. Lambda'da eng katta xavf - ikki pipeline logikasining asta-sekin bir-biridan uzoqlashishi, shuning uchun agar Kafka'da yetarli retention bera olsangiz Kappa'ni afzal ko'ring. Kappa'da esa replay vaqti va downstream'ga tushadigan yuk oldindan hisoblangan bo'lishi kerak, aks holda "kichik bir tuzatish" production'ni bosib qoladi.

```yaml
# Lambda: ikki yo'l - batch (aniq) va stream (tez)
batch_layer:   {input: s3://events/, output: daily_aggregates, schedule: "0 2 * * *"}
speed_layer:   {input: kafka://events, output: realtime_counters, window: 5m}
serving_layer: {query: "batch UNION ALL speed"}

# Narxi: bir xil mantiq ikki marta yoziladi va ikkisi bir-biridan farq qiladi.

# Kappa: faqat oqim. Tarixni qayta hisoblash kerak bo'lsa,
# hodisalar boshidan qayta o'qiladi.
kappa: {input: "kafka://events (retention: infinite)", reprocess: "offset 0 dan"}
```

## 12.28 Feature Bo'yicha vs Qatlam Bo'yicha Paketlash (Package-by-feature vs Package-by-layer)

**Tavsif:** Package-by-layer kodni texnik rolga ko'ra guruhlaydi (`controller`, `service`, `repository`, `dto`), package-by-feature esa biznes qobiliyatiga ko'ra (`order`, `payment`, `shipping`) - har bir paket ichida o'zining controller, service va repository'si bo'ladi. Feature bo'yicha paketlashda bitta o'zgarish bitta paket ichida qoladi, cohesion yuqori, coupling past bo'ladi va paketni keyinchalik alohida modul yoki servisga ajratish oson. Newman qatlamli tuzilmaning aynan shu narxini ko'rsatadi: faqat taqdimot qatlamiga tegadigan o'zgarish arzon, lekin tajriba shuni ko'rsatadi, funksionallikdagi o'zgarish odatda bir nechta qatlamga - taqdimot, ilova va ma'lumot qatlamiga - birga tegadi va qatlam soni ortgani sari muammo kuchayadi; shuning uchun microservices'da texnik funksionallik koheziyasi emas, biznes funksionallik koheziyasi ustun qo'yiladi. Richards va Ford xuddi shu holatni texnik bo'linish sifatida ta'riflaydi: bitta domen barcha qatlamlar bo'ylab sochilib ketadi va shu domenga o'zgarish kiritish qiyinlashadi.

**Spring'da qayerda uchraydi:** Spring Boot'da `@SpringBootApplication` component scan root paketdan boshlanganligi uchun ikkala struktura ham ishlaydi, lekin feature bo'yicha paketlash Java `package-private` ko'rinishini real himoyaga aylantiradi: `OrderRepository` ni `package-private` qilib, faqat `com.app.order` ichidan foydalanish mumkin. Spring Modulith (1.x) aynan shu modelga qurilgan - har bir to'g'ridan-to'g'ri sub-paket bitta modul, `package-info.java` da `@ApplicationModule(allowedDependencies = "shared")` bilan chegaralar belgilanadi, `ApplicationModules.of(App.class).verify()` buzilishlarni testda ushlaydi, `@ApplicationModuleTest` esa modulni yakka test qiladi. Modullar orasidagi aloqa `ApplicationEventPublisher` + `@ApplicationModuleListener` orqali, hamda `Documenter` bilan C4 diagrammalari generatsiya qilinadi.

**Qo'llanish keyslari:**
- Modulli monolit qurish: kelajakda ajratilishi mumkin bo'lgan chegaralarni bugundan belgilash.
- Katta jamoada kod egaligini belgilash (`CODEOWNERS` paket bo'yicha).
- Microservice'ga ajratish: `com.app.billing` paketini butunlay yangi servisga ko'chirish.
- Legacy layered kodni refaktoring qilishda bitta feature'ni "vertikal tilim" qilib ajratib olish.
- ArchUnit/Modulith bilan "order paketi payment internal sinflarini chaqirmasin" qoidasini CI'da qotirish.

**Ehtiyot bo'ling:** Feature paketlari ichida yana to'liq qatlam ierarxiyasini takrorlab, har biriga mini-monolit yasash ortiqcha ceremoniya bo'ladi - kichik feature uchun bir nechta sinf yetadi. Shuningdek, `common`/`shared` paketi tez orada yangi Big Ball of Mud markaziga aylanadi: unga nima tushishini qat'iy cheklang.

```text
Qatlam bo'yicha (package-by-layer):
  web/OrderController, web/InvoiceController
  service/OrderService, service/InvoiceService
  repository/OrderRepository, repository/InvoiceRepository

Funksiya bo'yicha (package-by-feature):
  order/OrderController, OrderService, OrderRepository, Order
  invoice/InvoiceController, InvoiceService, InvoiceRepository, Invoice

Ikkinchisi afzal: bitta o'zgarish bitta papkada qoladi, `package-private`
ishlaydi va chegara haqiqiy bo'ladi. Buni git tarixidan tekshiring:
  git log --name-only --since="6 months" | grep "^src" | xargs -n1 dirname |
    sort | uniq -c | sort -rn | head
```

## 12.29 Baqiruvchi Arxitektura (Screaming Architecture)

**Tavsif:** Robert Martin *Clean Architecture* ning 21-bobida ifodalagan g'oyaga ko'ra, loyihaning yuqori darajadagi strukturasi framework haqida emas, balki tizimning biznes maqsadi haqida "baqirib" turishi kerak; shu kitobning VI qismida (30, 31 va 32-boblar) baza, veb va framework detal ekani alohida asoslanadi. Ya'ni paket daraxtini ko'rgan kishi "bu Spring MVC loyihasi" emas, "bu sug'urta polisi boshqaruv tizimi" degan xulosaga kelishi lozim. Bu package-by-feature'ning falsafiy asosi: katalog nomlari use-case va domen tilidan olinadi, framework esa detal bo'lib chetga suriladi. Natijada yangi injener kodga kirganda domenni o'rganadi, texnologiyani keyin.

**Spring'da qayerda uchraydi:** Amalda bu `com.insurance.policy.underwriting`, `com.insurance.claims.settlement` kabi paketlar bo'lib, ularning ichida `UnderwritePolicyUseCase` kabi sinflar turadi; framework kodi esa `adapter/web` va `adapter/persistence` ga siqiladi (hexagonal bilan tabiiy birlashadi). Spring Boot buni qo'llab-quvvatlaydi: `@SpringBootApplication(scanBasePackages = "com.insurance")`, domen sinflarida Spring annotatsiyalari bo'lmaydi, konfiguratsiya `@Configuration` sinflarida markazlashadi. Spring Modulith `Documenter` va `@ApplicationModule(displayName = "Claims Settlement")` orqali bu nomlarni jonli dokumentatsiyaga aylantiradi; ArchUnit qoidalari esa domen paketining `org.springframework` ga bog'lanishini taqiqlaydi (`noClasses().that().resideInAPackage("..domain..").should().dependOnClassesThat().resideInAPackage("org.springframework..")`).

**Qo'llanish keyslari:**
- Yangi jamoa a'zosini onboarding qilish vaqtini qisqartirish - struktura domen xaritasi bo'lib xizmat qiladi.
- DDD bounded context'larini kod strukturasida to'g'ridan-to'g'ri aks ettirish.
- Uzoq umr ko'radigan enterprise tizim: framework o'zgarsa ham domen strukturasi qoladi.
- Monolitni biznes chegaralari bo'yicha bo'lishda nomzod servislarni paket daraxtidan o'qib olish.
- Biznes analitik bilan kod strukturasi ustida bir tilda gaplashish (ubiquitous language).

**Ehtiyot bo'ling:** Nomlarni haqiqiy domen tilidan olish kerak - `manager`, `processor`, `helper` kabi umumiy nomlar strukturani yana "baqirmaydigan" holatga qaytaradi. Va bu toza domenni framework'dan ajratishni talab qilgani uchun qo'shimcha mapping kodi tug'diradi: oddiy CRUD servis uchun bu ortiqcha bo'lishi mumkin.

```java
// Tuzilma nima qilayotganini aytishi kerak, qaysi framework ekanini emas
// Baqirmaydigan tuzilma:
//   controller/, service/, repository/, config/, util/
// Baqiradigan tuzilma:
//   placeorder/, cancelorder/, refund/, settlement/, fraudcheck/

// Tekshiruv: yangi dasturchi ildiz papkani ko'rib, tizim nima qilishini
// bir daqiqada aytib bera oladimi? Yo'q bo'lsa, tuzilma texnologiyani
// aks ettiryapti, domenni emas.
```

## 12.30 Komponentga Asoslangan Arxitektura (Component-Based Architecture)

**Tavsif:** Richards va Ford komponentni modulning fizik ko'rinishi deb ta'riflaydi: modul - bog'liq kod to'plami, komponent esa shu modulning fizik qadoqlanishi (Java'da jar, .NET'da dll, Ruby'da gem). Kitobga ko'ra komponent bir necha ko'rinishda uchraydi: eng oddiysi - library, u chaqiruvchi kod bilan bir xotira manzilida ishlaydi va til funksiya chaqiruvi mexanizmi orqali gaplashadi, hamda odatda compile-time bog'liqlik bo'ladi; komponent yana arxitekturadagi subsystem yoki qatlam, event processor uchun deploy birligi, yoki o'z manzil maydonida ishlaydigan servis bo'lishi mumkin. Shu sababli microservice'dan farqi aniq: komponent bir process ichida ham yashashi mumkin. Amalda komponent o'z ichki amalga oshirishini yashirib, faqat aniq belgilangan interfeys orqali muloqot qiladi va o'rnini bir xil kontraktni bajaruvchi boshqa implementatsiya egallashi mumkin.

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

**Ehtiyot bo'ling:** Komponent chegarasini bazadagi jadval munosabatlaridan ko'chirish Richards va Ford nomlagan entity trap anti-pattern'i: bunday komponentlar juda yirik bo'lib chiqadi va nima qilishi haqida hech qanday yo'l-yo'riq bermaydi. Teskari xato - interfeysni faqat bitta implementatsiya uchun yaratish (speculative generality): hech qanday foyda bermasdan kodni ko'paytiradi. Ortiqcha `@Conditional` zanjirlari esa context'ning nima uchun shunday yig'ilganini tushunishni qiyinlashtiradi - `--debug` bilan auto-configuration report'ini o'qishga odatlaning.

## 12.31 API-Birinchi (API-First)

**Tavsif:** Ford va boshqalar kontraktni qattiqdan bo'shgacha cho'zilgan spektr sifatida qaraydi: qattiq kontrakt nom, tur va tartibga qat'iy rioya qilishni talab qiladi (eng qattiq namunasi - RMI kabi masofaviy metod chaqiruvi, gRPC ham sukut bo'yicha qattiq kontrakt beradi), bo'sh kontrakt esa name-value juftliklaridan iborat bo'ladi, lekin unga ham sxema ma'lumotini tanlab qo'shish mumkin. Kitob ogohlantiradi: qattiq kontrakt ichki metod chaqiruvi semantikasini takrorlagani uchun arxitektorlarga yoqadi, ammo integratsiya arxitekturasini mo'rt qiladi, chunki kontrakt tarqatilgan arxitekturada yelimdek ishlaydi va qancha tez o'zgarsa, shuncha ko'p servisga to'lqin yuboradi. Shuning uchun API-first yondashuvda kontrakt (OpenAPI, gRPC `.proto`, GraphQL schema) kod yozilishidan oldin loyihalashtiriladi, yagona haqiqat manbai bo'ladi va uning qattiqlik darajasi ongli tanlanadi. Kontrakt kelishilgandan so'ng server va client jamoalari parallel ishlay oladi, mock server kontraktdan generatsiya qilinadi, buzuvchi o'zgarishlar esa CI'da avtomatik aniqlanadi. Bu ichki servislar orasidagi integratsiya xatolarini loyihaning eng arzon bosqichiga - dizaynga - ko'chiradi.

**Spring'da qayerda uchraydi:** Spring'da ikki yo'nalish bor. Contract-first: `openapi-generator-maven-plugin` (yoki `swagger-codegen`) bilan OpenAPI faylidan Spring interfeys va DTO'larni generatsiya qilish (`spring` generator, `interfaceOnly=true` → controller shu interfeysni implement qiladi); gRPC uchun `protobuf-maven-plugin` + `grpc-spring-boot-starter`; GraphQL uchun Spring for GraphQL (`spring-boot-starter-graphql`) `.graphqls` schema fayli bilan ishlaydi va `@SchemaMapping`/`@QueryMapping` ni unga bog'laydi. Code-first tomoni: `springdoc-openapi-starter-webmvc-ui` (Spring Boot 3.x uchun `springdoc-openapi` 2.x) kontraktni koddan generatsiya qiladi. Kontrakt buzilmasligini Spring Cloud Contract (`spring-cloud-starter-contract-verifier`) provider tomonda testlar generatsiya qilib, consumer tomonda stub berib ta'minlaydi; HTTP interfeys clientlari `@HttpExchange` + `HttpServiceProxyFactory` (Spring Framework 6.x) bilan deklarativ yoziladi.

**Qo'llanish keyslari:**
- Mobil va backend jamoalari parallel boshlashi uchun kontraktni oldin kelishib, mock server berish.
- Public API: versiyalash siyosati va buzuvchi o'zgarishlarni `openapi-diff` bilan CI'da nazorat qilish.
- Partner integratsiyasi: tashqi tomonga SDK'ni OpenAPI'dan generatsiya qilib berish.
- Microservice'lar orasida consumer-driven contract testlar bilan regressiyani ushlash.
- API gateway'da routing, rate limit va validatsiyani OpenAPI spetsifikatsiyasidan avtomatik sozlash.

**Ehtiyot bo'ling:** Kontraktni avval yozib, keyin uni koddan sekin-asta uzoqlashtirish eng keng tarqalgan xato - generatsiyani build'ning majburiy qadamiga aylantirmasa, spetsifikatsiya hujjatga aylanadi va yolg'on gapira boshlaydi. Shuningdek, DTO'ni to'g'ridan-to'g'ri JPA `@Entity` dan generatsiya qilib, ma'lumotlar bazasi strukturasini public API'ga chiqarib qo'yish keyinchalik orqaga qaytmas bog'lanish yaratadi.

```yaml
# API-first: shartnoma kod'dan oldin kelishiladi
# openapi.yaml (versiya nazoratida, review qilinadi)
openapi: 3.1.0
paths:
  /orders:
    post:
      operationId: placeOrder
      requestBody:
        required: true
        content:
          application/json:
            schema: {$ref: '#/components/schemas/PlaceOrderRequest'}
      responses:
        '201': {description: Yaratildi}
        '409': {description: Takroriy idempotentlik kaliti}

# Keyin interfeys generatsiya qilinadi (openapi-generator, interfaceOnly=true)
# va CI da spetsifikatsiya bilan kod mosligi tekshiriladi.
```

## 12.32 Event-Birinchi (Event-First)

**Tavsif:** Tizimni loyihalash ma'lumotlar bazasi jadvallari yoki REST endpointlardan emas, biznesda sodir bo'ladigan hodisalardan (domain events) boshlanadi: `OrderPlaced`, `PaymentCaptured`, `ShipmentDispatched`. Event'lar birinchi darajali kontrakt bo'lib, servislar bir-birini chaqirmaydi, balki o'zi uchun muhim hodisalarga obuna bo'ladi - bu temporal coupling'ni yo'qotadi va yangi consumer'ni mavjud kodga tegmasdan qo'shishga imkon beradi. Event Storming shu yondashuvning standart dizayn amaliyoti.

**Spring'da qayerda uchraydi:** Process ichida: `ApplicationEventPublisher.publishEvent()`, `@EventListener` va `@TransactionalEventListener(phase = AFTER_COMMIT)` - tranzaksiya commit bo'lgandan keyin reaksiya qilish uchun. Process tashqarisida: Spring for Apache Kafka (`KafkaTemplate`, `@KafkaListener`, `DefaultErrorHandler` + `DeadLetterPublishingRecoverer`), Spring AMQP (RabbitMQ), yoki Spring Cloud Stream funksional binding'lari. Spring Modulith event publication registry (`spring-modulith-events-jpa`/`-jdbc`) transactional outbox pattern'ini beradi: event DB'ga commit bilan birga yoziladi va `@ApplicationModuleListener` muvaffaqiyatli bajarilmaguncha "incomplete" holatda qoladi, qayta yuborish esa restart'da avtomatik. Event schema'ni Avro/Protobuf + Confluent Schema Registry bilan versiyalash, idempotentlikni consumer tomonda qayta ishlangan event ID jadvali bilan ta'minlash standart amaliyot.

**Qo'llanish keyslari:**
- E-commerce: `OrderPlaced` dan keyin inventar, to'lov, bildirishnoma va analitika mustaqil reaksiya qiladi.
- Audit va compliance: hodisalar ketma-ketligi o'zgarmas jurnal sifatida saqlanadi.
- Yangi read model yoki analitik pipeline'ni mavjud event log'dan replay qilib qurish.
- Legacy tizimdan CDC (Debezium) orqali event chiqarib, yangi servislarni unga ulash.
- Saga bilan taqsimlangan tranzaksiya: har bir qadam event'ga javob beradi, kompensatsiya ham event.

**Ehtiyot bo'ling:** Event'larni CRUD bildirishnomasiga aylantirib (`UserUpdated` ichida butun entity) yuborish yashirin bog'lanish yaratadi - event biznes faktini, nima sodir bo'lganini ifodalashi kerak. Eventual consistency'ni biznes bilan kelishmasdan tanlamang: "buyurtma darhol ko'rinmaydi" degani UI va qo'llab-quvvatlash jarayonlariga ham ta'sir qiladi, hamda debugging uchun distributed tracing majburiy bo'ladi.

```java
// Event-first: avval hodisalar aniqlanadi, keyin servislar
// Hodisa ro'yxati domen tilida va o'tgan zamonda:
public sealed interface CheckoutEvent {
    record OrderPlaced(long orderId, Money total, Instant at) implements CheckoutEvent {}
    record StockReserved(long orderId, List<Item> items) implements CheckoutEvent {}
    record PaymentCaptured(long orderId, String reference) implements CheckoutEvent {}
    record OrderShipped(long orderId, String tracking) implements CheckoutEvent {}
}
// Servis chegarasi shu ro'yxatdan chiqadi: kim hodisa chiqaradi,
// kim tinglaydi. Event storming aynan shu ro'yxatni tuzish uchun.
```

## 12.33 Mikro-Frontendlar (Micro-frontends) - eslatib o'tish

**Tavsif:** Newman mikro-frontend'ni tashkiliy pattern deb ataydi: frontend'ning turli qismlari mustaqil ishlanadi va deploy qilinadi, ya'ni backend uchun talab qilinadigan mustaqil deploy xossasi frontend'ga ham yoyiladi. U patternning mashhur bo'lishini yirik, bir butun SPA'lar tug'dirgan muammolar bilan izohlaydi va implementatsiya variantlari sifatida widget asosidagi va sahifa asosidagi kompozitsiyani sanaydi; uning xulosasi - stream-aligned, boshdan oxirgacha mas'ul jamoalar kerak bo'lsa, bu pattern shart. Amalda: yagona katta SPA o'rniga, har bir jamoa o'z UI bo'lagini mustaqil ishlab chiqadi va deploy qiladi, shell (host) ilova esa ularni runtime'da birlashtiradi. Birlashtirish Webpack/Rspack Module Federation, Web Components, iframe yoki server-side include orqali amalga oshiriladi. Bu vertikal jamoalarga (backend + frontend bitta biznes qobiliyati uchun) to'liq mustaqillik beradi.

**Spring'da qayerda uchraydi:** Spring bu pattern'ning backend va kompozitsiya qismida qatnashadi: Spring Cloud Gateway har bir fragment yoki remote bundle'ni o'z servisiga yo'naltiradi; server-side kompozitsiya uchun Thymeleaf fragment'lari (`th:replace`) yoki `WebClient` bilan boshqa servis HTML bo'lagini olib birlashtirish ishlatiladi; statik bundle'lar Spring Boot'ning `WebMvcConfigurer#addResourceHandlers` yoki CDN orqali beriladi. Xavfsizlik tomoni muhim: Spring Security 6.x `SecurityFilterChain` ichida `headers().contentSecurityPolicy(...)`, `CorsConfigurationSource` bilan cross-origin remote'larga ruxsat, va OAuth2 token'ni shell bilan bo'lishish uchun `oauth2Login` yoki BFF (Backend-For-Frontend) pattern'i `spring-cloud-gateway` + `TokenRelay` filtri bilan.

**Qo'llanish keyslari:**
- Yirik B2B portal: billing, reporting va admin bo'limlari alohida jamoalar tomonidan deploy qilinadi.
- Legacy JSP/Thymeleaf ilovasini sahifa-sahifa yangi frontend'ga ko'chirish (strangler).
- Bir nechta mahsulot bitta brend ostida yagona navigatsiya bilan birlashtirilishi.
- Har bir jamoaga o'z reliz tezligini berish - UI o'zgarishi butun monorepo relizini kutmaydi.
- A/B test: bitta fragment'ning yangi versiyasini faqat ayrim foydalanuvchilarga ko'rsatish.

**Ehtiyot bo'ling:** Narxi juda yuqori: umumiy dizayn tizimi, versiya nomuvofiqligi, takrorlangan kutubxonalar va yaxlit UX uchun qattiq boshqaruv kerak - bir nechta mustaqil frontend jamoasi bo'lmagan tashkilotda bu deyarli har doim ortiqcha. Autentifikatsiya, routing va global holatni fragmentlar o'rtasida bo'lishish eng ko'p muammo tug'diradigan joy, shuning uchun BFF bilan boshlang va fragmentlarni biznes chegarasi bo'yicha, komponent darajasida emas, bo'ling.

```html
<!-- Micro-frontend: har jamoa o'z bo'lagini mustaqil deploy qiladi -->
<!-- Eng oddiy va eng ishonchli variant: server tomonida fragment qo'shish -->
<div id="cart">
  <!--#include virtual="/cart-service/fragment" -->
</div>

<!-- Qoidalar:
     - CSS nom maydoni ajratilgan bo'lsin (prefiks yoki shadow DOM)
     - fragment yiqilsa sahifa yiqilmasin (timeout va fallback)
     - umumiy holat brauzerda bo'lishilmasin: aloqa hodisa orqali
     Narxi: ishlab chiqish muhiti va test murakkablashadi. Backend
     ajratilmagan bo'lsa, bu faqat qo'shimcha murakkablik qo'shadi. -->
```

## 12.34 Servis Asosidagi Arxitektura (Service-Based Architecture)

**Tavsif:** Richards va Ford bu uslubni mikroservis uslubining gibridi va eng pragmatik uslublardan biri deb ataydi: u taqsimlangan uslub, lekin mikroservis yoki hodisaga asoslangan uslub darajasidagi murakkablik va narxga ega emas. Asosiy topologiyasi uch qismdan iborat: alohida deploy qilinadigan user interface, alohida deploy qilinadigan yirik granulali masofaviy domain service'lar va bitta monolit baza. Domain service "ilovaning bir bo'lagi" bo'ladi va monolit ilova kabi deploy qilinadi, konteyner talab qilmaydi; umumiy baza bitta bo'lgani uchun kitob bitta ilova konteksti uchun 4 dan 12 gacha servisni, o'rtacha yettitani ko'rsatadi. Umumiy baza SQL join'ni saqlab qoladi, lekin jadval sxemasining o'zgarishi har bir servisga tegishi mumkin; kitobning yechimi bazani mantiqiy domenlarga bo'lib, har domenga alohida entity obyektlari kutubxonasi berish, yagona umumiy kutubxona esa uslubni amalga oshirishning eng samarasiz usuli deb ataladi (yondosh anti-pattern: [Shared Library bog'liqligi](14-microservices-patternlari.md#1436-shared-library-bogliqligi-shared-library-coupling---antipattern)). Har bir domain service ichida API facade qatlami turadi va biznes so'rovini servis ichida orkestratsiya qiladi, shuning uchun tranzaksiya oddiy ACID commit va rollback bo'lib qoladi; mikroservisda xuddi shu checkout so'rovi bir nechta masofaviy servis orkestratsiyasiga va BASE semantikasiga aylanadi. Topologiya variantlari: UI ni domenlarga bo'lish, monolit bazani domen bazalariga bo'lish va UI bilan servislar orasiga API layer qo'yish.

**Reyting (*Fundamentals of Software Architecture*, 13-bob, arxitektura xossalari yulduz jadvali):** kitob bu uslubda birorta ham besh yulduzli xossa yo'qligini aytadi. To'rt yulduz: agility, testability, deployability, hamda fault tolerance va umumiy availability. Scalability uch yulduz, elasticity ikki yulduz, sababi servislarning yirik granulali ekani. Soddalik va umumiy narx aynan shu uslubni mikroservis, hodisaga asoslangan va kosmosga asoslangan uslublardan ajratib turadigan ikki sabab deb ko'rsatiladi, reliability esa yirik servislar tarmoqqa kamroq yuk bergani uchun boshqa taqsimlangan uslublardan yuqori. Uslub domenga bo'lingan (domain-partitioned), quantum soni birdan katta yoki teng: 4 dan 12 gacha servis bitta baza yoki bitta UI ni bo'lishsa, butun tizim bitta quantum bo'lib qoladi.

**Spring'da qayerda uchraydi:** Har bir domain service alohida Spring Boot ilovasi bo'ladi, lekin hammasi bitta PostgreSQL bazasiga ulanadi: `spring.datasource.url` bir xil, `@Transactional` esa servis ichida haqiqiy ACID tranzaksiya beradi. Domen ichidagi tuzilma odatda [modulli monolit](#126-modulli-monolit-modular-monolith--spring-modulith) dagi kabi sub-domenga bo'linadi yoki API facade, business va persistence qatlamlariga ajratiladi. Entity obyektlarining domen kutubxonalari alohida Gradle yoki Maven moduli bo'ladi (`order-entities`, `invoicing-entities`), umumiy jadvallar uchun `common-entities`. Migratsiya bitta egada turadi: Flyway faqat bitta ilovada ishlaydi, qolganlarida `spring.flyway.enabled=false`. UI oldidagi API layer uchun `spring-cloud-gateway`, umumiy cross-cutting ishlar (metrics, security, audit) shu yerga ko'chiriladi.

**Qo'llanish keyslari:**
- Mikroservis uchun tashkiliy tayyorlik yo'q, lekin monolitni bo'lish kerak: 5 dan 10 gacha domen servisi arzon o'rta yechim beradi.
- Hisob-kitob va buyurtma kabi biznes so'rovida ACID tranzaksiya shart, saga esa qabul qilinmaydi.
- Ko'p sahifali, oldingi sahifa kontekstiga tayanadigan forma: semantik bog'lanish yuqori va mayda servisga bo'linmaydi.
- Faqat ayrim domen (masalan narx so'rovi va holat ko'rsatish) yuklama oladi, qolganlariga bitta instance yetadi.

**Ehtiyot bo'ling:** Servislar orasida masofaviy chaqiruv paydo bo'lsa, uslub buziladi: kitob bu uslubda interservice communication'dan qochish kerakligini aniq aytadi, chunki umumiy baza va umumiy kutubxona ustiga tarmoq bog'lanishi qo'shilsa, natija [taqsimlangan monolit](#1224-taqsimlangan-monolit-distributed-monolith---anti-pattern) bo'ladi. Ikkinchi tuzoq: yirik servis ichidagi bitta o'zgarish butun servisni, demak to'lov qismini ham, qayta test qilishni talab qiladi.

```java
// Service-based: yirik domain service, umumiy baza, servis ichida ACID
@Service
class OrderService {

    private final OrderRepository orders;
    private final PaymentGateway payments;
    private final InventoryRepository inventory;

    OrderService(OrderRepository orders, PaymentGateway payments,
                 InventoryRepository inventory) {
        this.orders = orders;
        this.payments = payments;
        this.inventory = inventory;
    }

    // API facade qatlami shu metodni chaqiradi: bitta biznes so'rovi
    @Transactional
    public OrderId placeOrder(CheckoutRequest request) {
        OrderId id = orders.insert(request);
        payments.charge(id, request.card());   // karta eskirgan bo'lsa exception
        inventory.decrease(request.items());   // rollback uchalasini qaytaradi
        return id;
    }
}
// Mikroservisda bu uchlik uch masofaviy chaqiruv va saga bo'lardi.
// Narxi: servis yirik, shuning uchun har o'zgarish butun servisni test qiladi.
```

## 12.35 Data Mesh va analitik ma'lumot tekisligi (Data Mesh)

**Tavsif:** Khononov analitik (OLAP) va tranzaksion (OLTP) modelni ajratadi: operatsion model biznes entity'lari va ularning lifecycle'i atrofida quriladi, analitik model esa allaqachon bo'lib o'tgan biznes faoliyatini modellashtiradi. Uning ikki qurilish bloki bor: fact jadvali (o'tgan faoliyat yozuvi, faqat append qilinadi) va dimension jadvali (fact atributlarini tavsiflaydi); ularning ko'pdan-birga munosabati star schema ni, dimension'ning qo'shimcha normallashuvi snowflake schema ni beradi. Shu modelni ikki eski platforma to'ldiradi: data warehouse (ETL bilan operatsion ma'lumotni analitik modelga aylantirib markaziy bazaga yuklash, kerak bo'lsa data mart bilan) va data lake (xom shaklda yuklab, keyin aylantirish). Khononov ikkisining asosiy muammosini bir xil deb ko'rsatadi: ETL operatsion sxemaga, ya'ni public interface emas, ichki detalga bog'lanadi, shuning uchun kichik sxema o'zgarishi analitik quvurni buzadi; sxemasiz data lake esa masshtabda data swamp ga aylanadi. Ford va boshqalar xuddi shu xulosani arxitektura tilida aytadi: ikkisi ham texnik bo'linish, ular ma'lumotni domen kontekstidan ajratadi.

Data mesh domain-driven design ni analitik ma'lumotga qo'llaydi va to'rt printsipga tayanadi. Birinchi, domenga egalik: analitik model bounded context chegarasi bilan tekislanadi va uni ishlab chiqarish shu context jamoasining mas'uliyati bo'ladi. Ikkinchi, ma'lumot mahsulot sifatida: analitik ma'lumot aniq sxemasi, o'lchanadigan SLA si va versiyasi bor output port orqali, xuddi public API kabi beriladi; iste'molchilar turlicha bo'lgani uchun portlar polyglot bo'ladi. Uchinchi, o'z-xizmat platformasi: data product qurish, topish va kuzatish murakkabligini yashiradigan platforma va uning uchun alohida infratuzilma jamoasi kerak. To'rtinchi, federativ boshqaruv: domen data product egalaridan tuzilgan guruh interoperability qoidalarini belgilaydi, Ford va boshqalarida bu qoidalar har bir data product ichida kod sifatida bajariladi. Shu kitob arxitektura o'zagi sifatida data product quantum (DPQ) ni ko'rsatadi: servis yoniga qo'yilgan, o'z kodi va ma'lumotiga ega, operatsion jihatdan mustaqil lekin domen bilan qattiq bog'langan birlik. DPQ uch turda bo'ladi: source-aligned, aggregate va fit-for-purpose (aniq bir hisobot, BI yoki ML talabi uchun).

**Reyting:** yo'q, va bu ataylab. *The Hard Parts* data mesh ni arxitektura uslubi emas, analitik ma'lumotni boshqarish patterni deb beradi va yulduz jadvali o'rniga afzallik va kamchilik jadvalini keltiradi: afzalliklari mikroservis arxitekturasiga mos kelishi, analitik va operatsion ma'lumotni yaxshi ajratishi hamda ehtiyotkor tuzilgan kontrakt analitik imkoniyatlarni bo'sh bog'langan holda rivojlantirishga ruxsat berishi; kamchiliklari data product quantum bilan kontraktni muvofiqlashtirish zarurati va yakuniy izchillikka tayanishi. Shu kitob uni analitik va operatsion ma'lumot doim sinxron bo'lishi shart bo'lgan joyga mos emas deb yozadi. Bu bobning qoidasi bo'yicha reyting faqat kitob reyting bergan uslubda beriladi, shuning uchun bu yerda yulduz qo'yilmaydi. Analitik yukni OLTP bazasidan ajratishning arzondan qimmatga boradigan to'rt darajasi [analitik yukni OLTP dan ajratish](../architect/26-partitioning-replikatsiya-va-katta-hajm.md#2613-analitik-yukni-oltp-dan-ajratish-read-replica-cdc-va-ombor) bo'limida yozilgan va takrorlanmaydi: u mexanika va narx haqida, bu bo'lim esa egalik va kontrakt haqida.

**Spring'da qayerda uchraydi:** Data product domen servisi ichida ikki shaklda chiqadi. Birinchisi hodisa oqimi: `spring-kafka` bilan `KafkaTemplate` orqali versiyalangan topic'ga fact yozuvi yuboriladi, sxema esa registry'da turadi; tranzaksiya bilan birga chiqarish uchun [tranzaksion outbox](10-malumotlarni-boshqarish-va-taqsimlash.md#1014-tranzaksion-outbox-transactional-outbox) yoki `@TransactionalEventListener` ishlatiladi. Ikkinchisi so'rov portasi: shu domen ichidagi materialized view yoki alohida analitik schema `JdbcTemplate` bilan yangilanadi va read-only `@RestController` orqali beriladi. Bir ma'lumotning ikki modelini chiqarish uchun [CQRS](#1210-buyruq-va-sorovlar-masuliyatini-ajratish-cqrs---command-query-responsibility-segregation), operatsion sxemadan oqim olish uchun Debezium bilan CDC qo'llanadi. Yirik to'ldirish ishlari Spring Batch da, jadval bo'yicha yangilanish `@Scheduled` da yuritiladi; port holati `micrometer` bilan o'lchanadi, chunki SLA e'lon qilingan bo'ladi.

**Qo'llanish keyslari:**
- Mikroservislar soni o'sgan va har bir hisobot uchun markaziy jamoa ETL yozib bera olmay qolgan tashkilot.
- ML jamoasi bir nechta domendan ma'lumot oladi va xom sxemaga emas, kontraktga tayanmoqchi.
- PII ni domen o'zi bilgani uchun maskalash va kirish nazorati shu domen portida bajarilishi kerak.
- Operatsion sxemani tez-tez o'zgartiradigan DDD loyihasi: analitik iste'molchi ichki sxemaga emas, published language'ga ulanadi.

**Ehtiyot bo'ling:** Data mesh tashkiliy qaror, faqat texnik emas: domen jamoasiga ma'lumot bo'yicha mutaxassis qo'shilmasa va platforma jamoasi tuzilmasa, natija har bir servis o'z usulida chiqargan, bir-biriga ulanmaydigan oqimlar bo'ladi. Kichik tashkilotda narx ortiqcha: ikki yoki uch domen uchun read replica va bir nechta materialized view yetadi. Yana bir xato: operatsion jadvalni o'zgarmagan shaklda Kafka orqali uzatib, uni data product deb atash; bu ichki sxemani public qilish, ya'ni data warehouse ning eski bog'lanish muammosini yangi transport bilan qaytarish.

```java
// Data mesh: domen o'z analitik mahsulotini versiyalangan output port bilan beradi
@Component
class SalesDataProduct {

    private final KafkaTemplate<String, SalesFact> kafka;
    private final JdbcTemplate jdbc;

    SalesDataProduct(KafkaTemplate<String, SalesFact> kafka, JdbcTemplate jdbc) {
        this.kafka = kafka;
        this.jdbc = jdbc;
    }

    // output port 1: fact oqimi; nomida versiya, sxemasi registry da
    @TransactionalEventListener
    void onOrderPlaced(OrderPlaced event) {
        kafka.send("sales.fact.v1", event.orderId().value(), SalesFact.from(event));
    }

    // output port 2: shu domen ichida yuritiladigan agregat ko'rinish
    @Scheduled(cron = "0 5 * * * *")
    void refreshDailySales() {
        jdbc.execute("REFRESH MATERIALIZED VIEW CONCURRENTLY sales_daily");
    }
}
// Egalik domenda: sxema, SLA va versiya shu jamoaning mas'uliyati.
// Narxi: kontrakt muvofiqlashtirish va yakuniy izchillik.
```

## 12.36 Arxitektura uslubini tanlash tartibi (Choosing an Architecture Style)

**Tavsif:** Richards va Ford bu savolga javobni "bu kontekstga bog'liq" deb boshlaydi va qaysi uslubni ishlatishni aytib bera olmasligini ochiq yozadi: tanlov arxitektura xossalari, domen mulohazalari va strategik maqsadlar bo'yicha trade-off tahlilining natijasi. Lekin tartib bor. Avval kitob uslub modasining nega siljiyotganini sanaydi: o'tmishdagi tizimlardan chiqqan kuzatuv va og'riq nuqtalari, ekotizimning doimiy o'zgarishi, yangi imkoniyatlar, o'zgarish tezligining o'sishi, domenning o'zgarishi, texnologiyaning o'zgarishi va tashqi omillar, masalan litsenziya narxining ko'tarilishi. Keyin qaror mezonlari keladi: arxitektor domenni (ayniqsa operatsion xossalarga ta'sir qiladigan tomonlarini) tushunishi, strukturaga ta'sir qiladigan arxitektura xossalarini aniqlab yozishi, ma'lumot arxitekturasi bo'yicha DBA bilan ishlashi, tashkiliy omillarni (cloud vendor narxi, qo'shilish va sotib olish rejalari) hisobga olishi, jarayon, jamoa va operatsion holatni bilishi hamda domen va arxitektura izomorfizmini ko'rishi kerak; Agile injenerlik yetukligi bo'lmagan tashkilotda shunga tayanadigan uslub qiyinchilik tug'diradi. Izomorfizm ikki tomonga ishlaydi: moslashuvchanlik talab qilgan domen microkernel'ga, ko'p diskret operatsiya space-based uslubga mos keladi; ko'p sahifali va har sahifasi oldingisining kontekstiga tayanadigan sug'urta formasi esa semantik bog'lanishi yuqori bo'lgani uchun mikroservisda og'ir, [servis asosidagi uslub](#1234-servis-asosidagi-arxitektura-service-based-architecture) unga ko'proq mos keladi.

Shundan keyin arxitektor uchta qarorni shu tartibda qiladi. Birinchi va eng katta qaror: monolit yoki taqsimlangan. O'lchov quantum tushunchasi bilan beriladi: bitta arxitektura xossalari to'plami butun tizimga yetsa monolit yetarli, tizimning turli qismlariga turli xossalar kerak bo'lsa taqsimlangan uslub kerak. Ikkinchi: ma'lumot qayerda yashaydi. Monolitda bu odatda bitta relyatsion baza, taqsimlangan uslubda esa qaysi servis saqlaydi va ma'lumot workflow bo'ylab qanday oqadi degan savol, ya'ni struktura va xulq birga loyihalanadi. Uchinchi: aloqa sinxronmi yoki asinxron. Kitob qoidani ochiq qo'yadi: default sinxron, zarurat bo'lganda asinxron, chunki sinxron aloqa dizayn, implementatsiya va debug jihatidan arzonroq, asinxron esa performance va masshtab beradi lekin ma'lumot sinxronizatsiyasi, deadlock, race condition va debug muammolarini olib keladi. Jarayonning chiqishi uch narsa: arxitektura topologiyasi, eng ko'p mehnat talab qilgan qismlar uchun ADR va muhim printsiplarni qo'riqlaydigan fitness function.

**Spring'da qayerda uchraydi:** Spring hech bir uslubni majburlamaydi, shuning uchun tanlov kodda emas, loyiha tuzilishida ko'rinadi. Monolit qarori bitta Spring Boot deploy birligi va uning ichidagi modul chegarasi bo'ladi: Spring Modulith `ApplicationModules.of(App.class).verify()` testi va ArchUnit `layeredArchitecture()` yoki `slices()` qoidalari aynan kitob aytgan fitness function vazifasini bajaradi. Taqsimlangan qarorga o'tilganda sinxron default `RestClient` yoki `@HttpExchange` bilan, asinxronga o'tish esa `spring-kafka` yoki `spring-rabbit` bilan amalga oshadi, ya'ni uchinchi qaror dependency ro'yxatida ko'rinadi. Ma'lumot qayerda yashashi `spring.datasource` konfiguratsiyalari soniga aylanadi: bitta `DataSource` bitta quantum.

**Qo'llanish keyslari:**
- Yangi loyiha boshida uslub tanlanmoqda va jamoada mikroservis bilan monolit o'rtasida bahs ketmoqda.
- Mavjud monolitni bo'lish taklifi keldi: avval turli qismlarga haqiqatan turli xossalar kerakmi degan savol beriladi.
- Yangi texnologiya moda bo'lgani uchun taklif qilinmoqda va uni mezonga solib tekshirish kerak.
- Asinxron aloqa taklif qilingan va uning narxi hali o'lchanmagan.

**Ehtiyot bo'ling:** Eng ko'p uchraydigan xato tartibni teskari bajarish: avval uslub tanlanadi, keyin arxitektura xossalari shu uslubga moslab yozib qo'yiladi. Ikkinchisi: asinxron aloqani default qilish. Uchinchisi: tanlovni yozib qoldirmaslik, natijada bir yildan keyin nega shunday qilinganini hech kim bilmaydi va uslub jim buziladi. Kitob tanlovni himoya qiladigan fitness function ni jarayonning chiqishi deb sanaydi, ya'ni tanlov CI da tekshirilmasa, u faqat niyat bo'lib qoladi.

```text
Uslub tanlash tartibi (Fundamentals of Software Architecture, 18-bob)

0. Kirish sharti: domen tushunilgan, arxitektura xossalari yozilgan,
   ma'lumot arxitekturasi DBA bilan ko'rilgan, tashkiliy omillar va
   jamoa yetukligi ma'lum.

1. Monolit yoki taqsimlangan?
   bitta xossalar to'plami butun tizimga yetadi      -> monolit
   turli qismga turli xossa kerak (quantum soni > 1) -> taqsimlangan

2. Ma'lumot qayerda yashaydi?
   monolit        -> bitta relyatsion baza
   taqsimlangan   -> qaysi servis saqlaydi va workflow bo'ylab
                     ma'lumot qanday oqadi

3. Servislar orasidagi aloqa?
   default        -> sinxron
   zarurat bo'lsa -> asinxron (narxi: sinxronizatsiya, deadlock,
                     race condition, debug)

Chiqish: arxitektura topologiyasi, eng og'ir qismlar uchun ADR va
tanlovni qo'riqlaydigan fitness function.
```

## 12.37 Taqsimlangan obyekt dizaynining birinchi qonuni (First Law of Distributed Object Design)

**Tavsif:** Fowler qoidani bitta gapda beradi: **obyektlaringizni taqsimlamang** (Martin Fowler, *Patterns of Enterprise Application Architecture*, Addison-Wesley, 2003, 7-bob "Distribution Strategies", 89-bet). Qoida sinf bo'yicha taqsimlashga qarshi qaratilgan: Customer, Order, Product va Delivery ni alohida node ga qo'yib, "yuk oshsa qo'shimcha box qo'shamiz" deb kutilgan performance aslida teskari chiqadi. Sabab kompyuterning fundamental fakti: protsess ichidagi chaqiruv juda tez, ikki protsess orasidagisi bir necha tartib sekin, boshqa mashinadagi protsess esa yana bir-ikki tartib sekin. Fowler buni ko'p ko'rgan dizayn sifatida tasvirlaydi va natijani ikki so'z bilan aytadi: bunday dizayn performance ni buzadi, tizimni qurish va deploy qilishni qiyinlashtiradi, ko'pincha esa ikkisini birga qiladi.

Qoidaning operativ qismi interfeys granularligida:

- **Protsess ichida fine-grained interfeys.** Address sinfi uchun city, state va zip ni alohida olish va qo'yish metodlari to'g'ri shakl: mayda bo'laklar kombinatsiya va override qilinadi, dizayn kelajakka ochiq qoladi.
- **Chegarada coarse-grained interfeys.** Chaqiruv sekin bo'lganda city, state va zip bitta chaqiruvda olinadi: `getAddressDetails`, `updateAddressDetails`. Bu interfeys moslashuvchanlik uchun emas, chaqiruv sonini kamaytirish uchun qurilgan va unga programma yozish ancha noqulay.
- **Tanlov majburiy.** Ikki obyekt gaplashganda qaysi interfeys ishlatilishini tanlash kerak, va obyekt hech qachon alohida protsessda bo'lishi mumkin bo'lsa, coarse-grained interfeysni olish va qiyinroq programmalash modelining narxini to'lash shart. Shuning uchun protsesslar aro kollaboratsiya sonini minimallash kerak.

Shundan kelib chiqib, bir protsess uchun loyihalangan sinflar guruhini olib, ustiga masofaviy texnologiya tashlab, taqsimlangan model olish mumkin emas: natijada har remotable sinfda coarse-grained interfeys bo'lsa ham, masofaviy chaqiruv soni baribir ko'p bo'ladi va tizimni o'zgartirish qiyinlashadi. Ko'p protsessordan foydalanishning to'g'ri yo'li sifatida kitob **klasterlashni** ko'rsatadi: hamma sinfni bitta protsessga joylab, o'sha protsessning bir nechta nusxasini turli node da ishlatish. Har nusxa ichida chaqiruvlar lokal bo'ladi, hamma sinf fine-grained interfeys bilan qoladi va programmalash modeli soddaroq bo'ladi.

Kitob chegarani butunlay yo'q qilish mumkin emasligini ham tan oladi va zarur bo'lgan joylarni sanaydi (90-91-betlar): klient va server, ilova serveri va baza (SQL ning o'zi masofaviy interfeys deb loyihalangani narxni tushiradi), veb server va ilova serveri, boshqa vendor paketining o'z protsessi, va oxirgi chora sifatida ilova server kodining o'zini bo'lish. Chegara qolgan joyda ichkarida fine-grained obyektlar saqlanadi, chegarada esa ularning ustiga faqat masofaviy interfeys berish uchun yashaydigan delegatsiya obyekti qo'yiladi: [masofaviy fasad](08-biznes-logika-va-service-qatlam-patternlari.md#813-masofaviy-fasad-remote-facade).

**Spring'da qayerda uchraydi:** Klasterlash amalda bitta Spring Boot ilovasining bir nechta nusxasini load balancer yoki Kubernetes `Deployment` ortida ishlatish va holatni ilovada emas, bazada yoki Redis da saqlash bo'ladi; modul chegarasi saqlanib, deploy bitta qolishi uchun Spring Modulith (`ApplicationModules.verify()`) ishlatiladi. Chegaradagi coarse-grained interfeys - REST controller va uning javob `record` i: bitta chaqiruv butun aggregate ni qaytaradi, maydon darajasidagi endpoint berilmaydi. Servislar aro chaqiruv `RestClient` yoki `@HttpExchange` bilan deklarativ interfeys sifatida yoziladi va bu interfeys ataylab yirik donali bo'ladi. Fine-grained interfeys protsess ichida qoladi: domen obyektlari va `@Service` metodlari.

**Qo'llanish keyslari:**
- "Har entity alohida servis" dizayn taklifini review da shu qoida nomi bilan rad etish va uni modulli monolitga aylantirish.
- Performance uchun servis ajratish taklifiga javob: avval bitta protsessning nusxalarini ko'paytirib o'lchash.
- Bitta use case uchun ketma-ket bir nechta masofaviy chaqiruv qiladigan chatty integratsiyani belgilash.
- Servis kontraktini loyihalashda DTO ni aggregate darajasida yig'ib, maydon darajasidagi endpoint bermaslik.
- Monolitni bo'lish rejasida har chegara uchun sababni yozib, "shunchaki toza bo'ladi" degan sababni rad etish.

**Ehtiyot bo'ling:** Qoida "taqsimlangan tizim qurmang" degani emas: u sinf bo'yicha taqsimlashga va chegarani sababsiz ko'paytirishga qarshi. Mustaqil deploy, alohida masshtablash yoki jamoa mustaqilligi uchun chegara haqli bo'lishi mumkin, lekin narx aynan shu bo'limda sanalgan narx va uni oldindan aytib qo'yish kerak. Ikkinchi tuzoq - middleware ning "transparency" va'dasiga ishonish: lokal va masofaviy chaqiruvni bir xil ko'rsatish mumkin, lekin performance ni shaffof qilish mumkin emas. Qoida buzilganda natija [taqsimlangan monolit](#1224-taqsimlangan-monolit-distributed-monolith---anti-pattern) bo'ladi.

```text
Sinf bo'yicha taqsimlash (kitob tavsiya etmaydi):
  node A: Customer   node B: Order   node C: Product   node D: Delivery
  bitta use case -> ko'p masofaviy chaqiruv -> har sinf coarse-grained
  bo'lishga majbur -> programmalash qiyin, performance yomon

Klasterlash (tavsiya etilgan):
  node A: [Customer Order Product Delivery]   <- lokal, fine-grained
  node B: [Customer Order Product Delivery]   <- o'sha protsessning nusxasi
  yuk oshsa node qo'shiladi, interfeys o'zgarmaydi

Chegara zarur bo'ladigan joylar:
  klient <-> server             foydalanuvchi mashinasi va umumiy ombor
  ilova <-> baza                SQL ning o'zi masofaviy interfeys
  veb server <-> ilova server   birga ishlatish afzal, lekin doim mumkin emas
  ilova <-> vendor paketi       paket o'z protsessida ishlaydi
  ilova server kodini bo'lish   eng qimmat variant, oxirgi chora
```

## 12.38 Amalda qo'llash

- [ ] Loyihaning hozirgi arxitektura uslubini bir gapda yozing va kodda unga zid bo'lgan joylarni ro'yxatga oling.
- [ ] Modullar o'rtasidagi bog'liqlik yo'nalishini chizib, domenga kiradigan strelkalarni toping.
- [ ] Modular monolit ishlatilsa, Spring Modulith `verify()` testini CI ga qo'shing va buzilgan chegaralarni ro'yxat qiling.
- [ ] Microservice'ga o'tish taklif qilingan har bir modul uchun savolga javob yozing: uning o'z ma'lumotlari bormi.
- [ ] CQRS taklif qilinsa, o'qish va yozish modeli alohida ekanini va sinxronlash kechikishi qabul qilinganini hujjatlashtiring.
- [ ] Hexagonal uslub ishlatilsa, port interfeyslari domen paketida, adapterlar tashqarida turganini tekshiring.
- [ ] Har bir sinxron servis chaqiruvi uchun timeout, retry va fallback qiymatini yozib qo'ying.
- [ ] Uslublarni taqqoslaganda baholarni o'zingizdan qo'ymang: *Fundamentals of Software Architecture* da reytingi bor uslub uchun shu jadvalni, bo'lmagan uslub uchun esa "o'lchanmagan" deb yozing.
- [ ] Servisni bo'lish yoki birlashtirish taklifini *Hard Parts* dagi disintegrator va integrator sabablari ro'yxatiga solib tekshiring.
- [ ] Arxitektura qarorini ADR sifatida yozib, ko'rib chiqilgan variantlar va rad etish sabablarini qo'shing.

## Manbalar

- Mark Richards, Neal Ford, *Fundamentals of Software Architecture*, O'Reilly, 2020, 8 va 9-boblar - komponent modulning fizik ko'rinishi ekani va entity trap anti-pattern'i; fundamental qoliplar, Big Ball of Mud ta'rifi va uning Brian Foote hamda Joseph Yoder'ning 1997 yildagi maqolasiga tegishliligi, client/server va uch qatlamli variantlar, monolit va tarqatilgan uslublar tasnifi, tarqatilgan hisoblash xatolari (L. Peter Deutsch va hamkasblar, 1994)
- Mark Richards, Neal Ford, *Fundamentals of Software Architecture*, O'Reilly, 2020, 10-bob - qatlamli uslub: to'rt standart qatlam, yopiq va ochiq qatlam, layers of isolation, architecture sinkhole anti-pattern va uni 80-20 qoidasi bilan o'lchash, texnik bo'linish va DDD bilan mos kelmasligi, Conway qonuni, yulduz reytinglari
- Mark Richards, Neal Ford, *Fundamentals of Software Architecture*, O'Reilly, 2020, 11-bob - quvurli uslub: bir yo'nalishli point-to-point quvur, holatsiz va bir vazifali filter, to'rt tur filter (producer, transformer, tester, consumer), yulduz reytinglari
- Mark Richards, Neal Ford, *Fundamentals of Software Architecture*, O'Reilly, 2020, 12-bob - mikroyadro: core system ta'rifi, plugin mustaqilligi, plug-in registry, kontrakt va adapter, compile va runtime plugin, masofaviy plugin bitta quantum qolishi, yulduz reytinglari
- Mark Richards, Neal Ford, *Fundamentals of Software Architecture*, O'Reilly, 2020, 14-bob - hodisaga asoslangan uslub: broker va mediator topologiyalarining komponentlari, broker topologiyasining kamchiliklari (oqim nazorati, xato ishlash, tiklanish, qayta boshlash, ma'lumot nomuvofiqligi), domen bo'yicha bir nechta mediator, yulduz reytinglari
- Mark Richards, Neal Ford, *Fundamentals of Software Architecture*, O'Reilly, 2020, 15-bob - kosmosga asoslangan uslub: tuple space, processing unit, virtualized middleware tarkibi, data pump, data writer va data reader, yulduz reytinglari
- Mark Richards, Neal Ford, *Fundamentals of Software Architecture*, O'Reilly, 2020, 16-bob - orkestratsiyaga asoslangan SOA: qayta ishlatish falsafasi, servis taksonomiyasi (business, enterprise, application, infrastructure), orchestration engine, Conway qonuni va integratsiya jamoasining tiqilinchga aylanishi, yulduz reytinglari
- Mark Richards, Neal Ford, *Fundamentals of Software Architecture*, O'Reilly, 2020, 17-bob - mikroservislar: nomning Martin Fowler va James Lewis'ning 2014 yil mart maqolasidan tarqalishi, bounded context, qayta ishlatish o'rniga takrorlanish, granularlik va performance narxi, yulduz reytinglari
- Mark Richards, Neal Ford, *Fundamentals of Software Architecture*, O'Reilly, 2020, 13-bob - servis asosidagi uslub: mikroservis gibridi ta'rifi, alohida deploy qilinadigan UI, yirik granulali domain service va monolit baza topologiyasi, servis soni 4 dan 12 gacha va o'rtacha yetti, topologiya variantlari (federativ UI, federativ baza, API layer), API facade qatlami va servis ichidagi orkestratsiya, ACID va BASE qiyosi, bazani mantiqiy bo'lish hamda federativ entity kutubxonalari, domain-partitioned va quantum hisobi, interservice communication'dan qochish, yulduz reytinglari
- Mark Richards, Neal Ford, *Fundamentals of Software Architecture*, O'Reilly, 2020, 18-bob - uslub tanlash: moda siljishining yetti omili, oltita qaror mezoni (domen, arxitektura xossalari, ma'lumot arxitekturasi, tashkiliy omillar, jarayon va jamoa bilimi, domen va arxitektura izomorfizmi), uchta ketma-ket qaror (monolit yoki taqsimlangan, ma'lumot qayerda yashaydi, sinxron yoki asinxron), "default sinxron, zarurat bo'lganda asinxron" qoidasi, chiqish sifatida topologiya, ADR va fitness function
- ESLATMA: *Fundamentals of Software Architecture* ning shu korpusdagi PDF nusxasida chop etilgan bet raqamlari yo'q, shuning uchun bu kitob bob darajasida iqtibos qilingan
- Martin Fowler, *Patterns of Enterprise Application Architecture*, Addison-Wesley, 2003, 1-bob (17-24-betlar) - qatlamlash foydasi va narxi, uch asosiy qatlam (presentation, domain, data source), UI'dagi yangi maydonning barcha qatlamga tarqalishi
- Martin Fowler, *Patterns of Enterprise Application Architecture*, Addison-Wesley, 2003, 7-bob (87-90-betlar) - Taqsimlangan Obyekt Dizayni Birinchi Qonuni ("obyektlaringizni tarqatmang"), protsess ichidagi va protsesslar orasidagi chaqiruv narxi farqi, klasterlash tavsiyasi, client-server protsesslararo chegara
- Neal Ford, Mark Richards, Pramod Sadalage, Zhamak Dehghani, *Software Architecture: The Hard Parts*, 1-nashr, O'Reilly, 2021 (copyright 2022), 2-bob (28-30-betlar) - arxitektura quantum ta'rifi: mustaqil deploy, yuqori funksional koheziya va statik bog'lanish; umumiy baza bitta quantum berishi
- Neal Ford, Mark Richards, Pramod Sadalage, Zhamak Dehghani, *Software Architecture: The Hard Parts*, 1-nashr, O'Reilly, 2021 (copyright 2022), 7-bob (187-204-betlar) - servis granularligi: oltita disintegrator va to'rtta integrator sababi hamda ular orasidagi muvozanat
- Neal Ford, Mark Richards, Pramod Sadalage, Zhamak Dehghani, *Software Architecture: The Hard Parts*, 1-nashr, O'Reilly, 2021 (copyright 2022), 13-bob (367-375-betlar) - kontraktning qattiqdan bo'shgacha spektri va qattiq kontraktning mo'rtligi
- Neal Ford, Mark Richards, Pramod Sadalage, Zhamak Dehghani, *Software Architecture: The Hard Parts*, 1-nashr, O'Reilly, 2021 (copyright 2022), 14-bob (381-393-betlar) - analitik ma'lumotni boshqarish: Data Warehouse patterni xossalari va uning nosozliklari (integratsiya mo'rtligi, domen bilimining ajralishi, murakkablik, maqsadga yetmagan funksionallik), Star Schema, Data Lake patterni va uning kamchiliklari, ikkisining ham texnik bo'linish ekani, data mesh ta'rifi va to'rt printsipi, data product quantum hamda uning uch turi, data mesh ning afzallik va kamchilik jadvali
- Vlad Khononov, *Learning Domain-Driven Design*, O'Reilly, 2021, 16-bob (249-265-betlar) - analitik (OLAP) va tranzaksion (OLTP) model farqi, fact va dimension jadvali, star va snowflake schema, data warehouse, data mart va data lake arxitekturalari hamda ularning operatsion sxemaga bog'lanish muammosi, data mesh ning to'rt printsipi, analitik ma'lumotni output port orqali mahsulot sifatida berish, open-host va CQRS ning data mesh ga qo'shilishi
- Sam Newman, *Building Microservices: Designing Fine-Grained Systems*, 2-nashr, O'Reilly, 2021, 1-bob - mikroservis o'zagi sifatida mustaqil deploy, biznes domeni bo'yicha modellash, servisning o'z holatiga egalik qilishi, qatlamli tuzilmada o'zgarishning bir nechta qatlamga tegishi, SOA bilan farqi
- Sam Newman, *Building Microservices: Designing Fine-Grained Systems*, 2-nashr, O'Reilly, 2021, 13-bob - CQRS va event sourcing'ning amalda qiyinligi va read replica kabi arzonroq muqobil
- Sam Newman, *Building Microservices: Designing Fine-Grained Systems*, 2-nashr, O'Reilly, 2021, 14-bob - mikro-frontend tashkiliy pattern, frontend uchun mustaqil deploy, widget va sahifa asosidagi kompozitsiya
- Brendan Burns, *Designing Distributed Systems*, O'Reilly, 2018, 8-bob (81-87-betlar) - FaaS foydasi, serverless va event-driven farqi, hamda to'rt cheklov: majburiy ajralish va kuzatuvchanlik, ishlash vaqtining cheklanganligi, xotiraga ko'p ma'lumot yuklash narxi, doimiy trafikda per-request narx modelining yomonlashishi
- Gregor Hohpe, Bobby Woolf, *Enterprise Integration Patterns*, Addison-Wesley, 2003, Pipes and Filters va Message Broker yozuvlari - quvur va filtr uslubining messaging kontekstidagi ta'rifi, filter'ni kodga tegmasdan qo'shish va tartibini o'zgartirish, patternning Regine Meunier va POSA katalogiga bog'liqligi
- Robert C. Martin, *Clean Architecture*, Prentice Hall, 2018, 22-bob - Clean Architecture va Dependency Rule
- Robert C. Martin, *Clean Architecture*, Prentice Hall, 2018, 22-bob, "Only Four Circles?" - halqa soni sxematik, to'rttadan ko'p bo'lishi mumkin va qat'iy qoida yo'q; o'zgarmas narsa Dependency Rule va ichkariga borgan sari abstraksiya hamda siyosat darajasining oshishi (12.3)
- Robert C. Martin, *Clean Architecture*, Prentice Hall, 2018, 16-bob - arxitektura qo'llab-quvvatlashi kerak bo'lgan narsalar ro'yxatining birinchisi use case lar ekani, arxitekturaning xatti-harakatni ochiq ko'rsatishi va use case larning tizim tuzilmasida birinchi darajali element sifatida ko'rinib turishi (12.3)
- Martin Fowler, *Patterns of Enterprise Application Architecture*, Addison-Wesley, 2003, 7-bob (88-91-betlar) - lokal fine-grained va masofaviy coarse-grained interfeys farqi, sinf bo'yicha taqsimlashning performance va deploy narxi, klasterlash tavsiyasi, chegara zarur bo'ladigan besh joy va chegarada Remote Facade (12.37)
- Robert C. Martin, *Clean Architecture*, Prentice Hall, 2018, 17 va 18-boblar - chegara chizish va chegara anatomiyasi
- Robert C. Martin, *Clean Architecture*, Prentice Hall, 2018, 21-bob - Screaming Architecture
- Robert C. Martin, *Clean Architecture*, Prentice Hall, 2018, 30, 31, 32-boblar - baza, veb va framework detal ekani
- Martin Kleppmann, *Designing Data-Intensive Applications*, O'Reilly, 2017, II qism kirishi - shared-memory, shared-disk va shared-nothing arxitekturalari qiyosi va shared-nothing narxi
- Chris Richardson, *Microservices Patterns*, Manning, 2019, 1 va 2-boblar (1-betdan boshlab) - monolitdan chiqish va dekompozitsiya
- John Carnell, *Spring Microservices in Action*, Manning, 2017, 1-bob (1-34-betlar) - bulut uchun servis arxitekturasi
- ESLATMA: 12.2 (hexagonal), 12.4 (onion), 12.5 (vertical slice) va 12.13 (self-contained systems) bo'limlaridagi uslub tavsiflari shu korpusning amaliy bayoni - bu uslublar yuqoridagi kitoblarda alohida uslub sifatida yozilmagan, shuning uchun ularga yulduz reytingi berilmaydi
- ESLATMA: 12.19 (peer-to-peer), 12.21 (reaktiv), 12.25 (cell-based), 12.27 (lambda/kappa) va 12.32 (event-first) bo'limlaridagi tavsiflar ham shu korpusning amaliy bayoni va o'lchangan arxitektura xossalariga ega emas
- ESLATMA: 12.35 (data mesh) kitoblarga tayangan, lekin unga yulduz reytingi berilmaydi: *The Hard Parts* data mesh ni arxitektura uslubi emas, analitik ma'lumotni boshqarish patterni deb beradi va yulduz jadvali o'rniga afzallik va kamchilik jadvalini keltiradi
- ESLATMA: barcha bo'limlardagi Spring sinf, annotatsiya, starter va property nomlari framework hujjatidan olingan amaliy ma'lumot, kitobdan emas; shuningdek har bo'limdagi "Qo'llanish keyslari" va "Ehtiyot bo'ling" dagi amaliy tavsiyalar manba ko'rsatilmagan joyda shu korpusning o'z checklisti

---

[&larr; 11. Keshlash patternlari](11-keshlash-patternlari.md) · [Mundarija](README.md) · [13. Domain-Driven Design patternlari &rarr;](13-domain-driven-design-patternlari.md)
