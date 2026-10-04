<!-- doc: patterns | chapter: 8 | part:  -->

[Java Spring arxitektori bilishi kerak bo'lgan barcha dizayn patternlar](../../README.md) / [Dizayn patternlar](README.md)

# 8. Biznes logika va Service qatlam patternlari (Business & Service Layer Patterns)

<details>
<summary>Bu bo'limdagi 27 bo'lim</summary>

- [8.1 Tranzaksiya skripti (Transaction Script)](#81-tranzaksiya-skripti-transaction-script)
- [8.2 Domen modeli (Domain Model)](#82-domen-modeli-domain-model)
- [8.3 Jadval moduli (Table Module)](#83-jadval-moduli-table-module)
- [8.4 Service qatlami (Service Layer)](#84-service-qatlami-service-layer)
- [8.5 Application Service va Domain Service (Application Service vs Domain Service)](#85-application-service-va-domain-service-application-service-vs-domain-service)
- [8.6 Biznes delegati (Business Delegate)](#86-biznes-delegati-business-delegate)
- [8.7 Sessiya fasadi (Session Facade)](#87-sessiya-fasadi-session-facade)
- [8.8 Biznes obyekti (Business Object)](#88-biznes-obyekti-business-object)
- [8.9 Kompozit entity (Composite Entity)](#89-kompozit-entity-composite-entity)
- [8.10 Ma'lumot uzatish obyekti (Transfer Object / DTO)](#810-malumot-uzatish-obyekti-transfer-object--dto)
- [8.11 Transfer Object yig'uvchi (Transfer Object Assembler)](#811-transfer-object-yiguvchi-transfer-object-assembler)
- [8.12 Qiymatlar ro'yxati boshqaruvchisi (Value List Handler)](#812-qiymatlar-royxati-boshqaruvchisi-value-list-handler)
- [8.13 Masofaviy fasad (Remote Facade)](#813-masofaviy-fasad-remote-facade)
- [8.14 Mapper (Mapper - MapStruct, ModelMapper)](#814-mapper-mapper---mapstruct-modelmapper)
- [8.15 Buyruq / Use Case Handler (Command / Use Case Handler - Interactor)](#815-buyruq--use-case-handler-command--use-case-handler---interactor)
- [8.16 Buyruq shinasi / Mediator (Command Bus / Mediator)](#816-buyruq-shinasi--mediator-command-bus--mediator)
- [8.17 Tranzaksiya chegarasi (Transaction Boundary - @Transactional on service)](#817-tranzaksiya-chegarasi-transaction-boundary---transactional-on-service)
- [8.18 Notification (Notification - validatsiya xatolarini yig'ish)](#818-notification-notification---validatsiya-xatolarini-yigish)
- [8.19 Natija obyekti vs Exception (Result Object vs Exceptions)](#819-natija-obyekti-vs-exception-result-object-vs-exceptions)
- [8.20 Siyosat obyekti (Policy Object)](#820-siyosat-obyekti-policy-object)
- [8.21 Strategiyalar registri Map<String, Bean> orqali (Strategy Registry via Map<String, Bean>)](#821-strategiyalar-registri-mapstring-bean-orqali-strategy-registry-via-mapstring-bean)
- [8.22 Plugin tanlash @Qualifier orqali (Plugin Selection via @Qualifier)](#822-plugin-tanlash-qualifier-orqali-plugin-selection-via-qualifier)
- [8.23 Boy domain modeli vs Anemik (Rich Domain Model vs Anemic)](#823-boy-domain-modeli-vs-anemik-rich-domain-model-vs-anemic)
- [8.24 Aggregate-ga bitta service (Service-per-Aggregate)](#824-aggregate-ga-bitta-service-service-per-aggregate)
- [8.25 Orkestrator vs Fasad (Orchestrator vs Facade)](#825-orkestrator-vs-fasad-orchestrator-vs-facade)
- [8.26 Service'dan domain event chiqarish (Domain Event Publishing from Service)](#826-servicedan-domain-event-chiqarish-domain-event-publishing-from-service)
- [8.27 Amalda qo'llash](#827-amalda-qollash)

</details>



Biznes logika va Service qatlam patternlari - ilovaning eng qimmatbaho qismi, ya'ni domen qoidalari, use-case'lar va tranzaksion chegaralar qanday tashkil etilishini belgilaydi. Bu patternlar aynan shu savolga javob beradi: logika SQL so'rovlarida, `@Service` sinflarida yoki boy domen obyektlarida yashashi kerakmi, va tranzaksiya qayerda boshlanib, qayerda tugaydi. Arxitektor uchun bu muhim, chunki noto'g'ri tanlov "anemic domain model" yoki 3000 qatorli "god service" kabi texnik qarzga olib keladi - bunday kodni test qilish ham, o'zgartirish ham qimmatga tushadi. Quyidagi entry'lar Fowler'ning PoEAA va Core J2EE Patterns kataloglaridan olingan klassik yechimlarni zamonaviy Spring Boot 3.x/4.x konteksti bilan bog'laydi.

## 8.1 Tranzaksiya skripti (Transaction Script)

**Tavsif:** Har bir biznes so'rovni (use-case'ni) bir protsedura - bitta ketma-ket skript sifatida tashkil etadi: validatsiya, hisob-kitob va ma'lumotlar bazasiga yozish hammasi shu metod ichida bajariladi. Domen obyektlari deyarli bo'lmaydi, ma'lumotlar oddiy DTO yoki `Map` ko'rinishida uzatiladi. Oddiy va tushunarli, ammo use-case'lar soni ortishi bilan takrorlanuvchi logika ko'payadi. Odatda bitta tranzaksiya chegarasi aynan shu skriptga to'g'ri keladi.

**Spring'da qayerda uchraydi:** `@Service` sinfidagi `@Transactional` metod ichida `JdbcClient` (Spring Framework 6.1+) yoki `NamedParameterJdbcTemplate` orqali to'g'ridan-to'g'ri SQL yozish - klassik Transaction Script. Shuningdek jOOQ yoki MyBatis (`spring-boot-starter-mybatis` orqali) bilan birga ishlatiladi; tranzaksiyani `PlatformTransactionManager` yoki `TransactionTemplate` boshqaradi. Spring Batch'dagi `Tasklet` implementatsiyasi ham mohiyatan bitta tranzaksion skript.

**Qo'llanish keyslari:**
- CRUD'ga yaqin admin panel backend'i, bu yerda domen qoidalari deyarli yo'q.
- Hisobotlar va eksport endpoint'lari: bir nechta jadvaldan agregat o'qib, CSV tayyorlash.
- Legacy ma'lumotlar bazasidan migratsiya skriptlari, bu yerda ORM mapping ortiqcha xarajat.
- Yuqori yuklamali, bitta jadval bilan ishlovchi "ledger entry qo'shish" kabi tor operatsiyalar.
- Prototip yoki MVP: domen hali noma'lum, ortiqcha abstraksiya zararli.

**Ehtiyot bo'ling:** Biznes qoidalari o'sgach skriptlar o'rtasida logika copy-paste bo'lib ketadi va bitta qoidani o'zgartirish uchun o'nlab joyni tahrirlashga to'g'ri keladi. Murakkab, ko'p invariantli domen (sug'urta, narxlash, buxgalteriya) uchun ishlatmang - bunda Domain Model afzal.

```java
// Transaction Script: bitta amal, boshdan oxir protsedura
@Service
public class TopUpScript {
    private final JdbcClient db;

    @Transactional
    public void topUp(long accountId, Money amount) {
        int updated = db.sql("UPDATE accounts SET balance = balance + :a WHERE id = :id")
                .param("a", amount.amount()).param("id", accountId).update();
        if (updated == 0) throw new AccountNotFoundException(accountId);
        db.sql("INSERT INTO ledger(account_id, amount, kind) VALUES (:id, :a, 'TOPUP')")
                .param("id", accountId).param("a", amount.amount()).update();
    }
}
// Oddiy CRUD uchun yetarli. Qoida ko'paysa takrorlanish boshlanadi.
```

## 8.2 Domen modeli (Domain Model)

**Tavsif:** Biznes logikani ma'lumot va xatti-harakatni birlashtirgan obyektlar to'ri sifatida ifodalaydi: har bir obyekt o'z invariantlarini o'zi qo'riqlaydi. Service qatlam faqat yupqa koordinator bo'lib qoladi - tranzaksiyani ochadi, aggregate'ni yuklaydi, unga metod chaqiradi va saqlaydi. Murakkab, tez o'zgaruvchi qoidalar uchun eng kuchli yechim, ammo o'rganish narxi va mapping murakkabligi yuqori.

**Spring'da qayerda uchraydi:** JPA `@Entity` sinflari xatti-harakat bilan boyitiladi, `@Embeddable` orqali Value Object yasaladi, Spring Data JPA `Repository`'lari aggregate'ni yuklaydi. Domen hodisalari `AbstractAggregateRoot.registerEvent(...)` (Spring Data) yoki `ApplicationEventPublisher` + `@TransactionalEventListener` bilan tarqatiladi. Java 17+ `record` va `sealed interface` Value Object va domen natijalarini modellashda qulay; Spring Modulith esa modul chegaralarini `@ApplicationModule` bilan majburlaydi.

**Qo'llanish keyslari:**
- Sug'urta polisining narxlash va amal qilish qoidalari, bu yerda o'nlab shart o'zaro bog'liq.
- Buyurtma aggregate'i: status o'tishlari, bekor qilish va qaytarish qoidalari bitta joyda.
- Bank hisobidagi limit va overdraft invariantlari, hech qachon buzilmasligi kerak.
- Ko'p bosqichli approval workflow'i, har bir o'tish o'z shartlariga ega.
- Subscription billing: plan o'zgarishi, proration, grace period hisoblash.

**Ehtiyot bo'ling:** Eng keng tarqalgan xato - "anemic domain model": entity'lar faqat getter/setter bo'lib, logika yana service'da qolib ketadi, natijada Domain Model nomi ostida aslida Transaction Script ishlaydi. JPA lazy loading va `LazyInitializationException` tufayli domen metodlarini tranzaksiyadan tashqarida chaqirmang.

```java
// Domain Model: qoida ma'lumot bilan birga turadi
@Entity
public class Account {
    @Id private Long id;
    private BigDecimal balance;
    private AccountStatus status;

    public void withdraw(Money amount) {
        if (status != AccountStatus.ACTIVE) throw new AccountFrozenException(id);
        if (balance.compareTo(amount.amount()) < 0) throw new InsufficientFundsException(id);
        this.balance = balance.subtract(amount.amount());   // invariant ichda
    }
}
// Servis endi faqat orkestratsiya qiladi: yuklash, chaqirish, saqlash
```

## 8.3 Jadval moduli (Table Module)

**Tavsif:** Bitta jadval yoki view uchun bitta sinf yaratiladi va shu jadvaldagi barcha satrlar bilan ishlovchi biznes logika shu sinfga joylanadi. Domain Model'dan farqi: har bir satr uchun alohida obyekt emas, balki butun to'plam ustidan ishlaydigan bitta modul mavjud. Ko'pincha ma'lumotlar `RecordSet`/`ResultSet` kabi tabular strukturada saqlanadi.

**Spring'da qayerda uchraydi:** Spring'da bu `@Repository` yoki `@Service` sinfining "bitta jadval = bitta komponent" ko'rinishi: masalan `ProductTableModule` ichida `JdbcClient` yoki jOOQ'ning generatsiya qilingan `DAO` sinflari (`ProductDao extends DAOImpl`) ishlatiladi. jOOQ `Record` va `Result<Record>` turlari aynan tabular ma'lumot ustida metodlar yozishga mos keladi; Spring Data JDBC'ning `@Query` metodlari ham shu uslubga yaqin.

**Qo'llanish keyslari:**
- Narx jadvali ustida ommaviy chegirma qo'llash, satrlarni bittalab yuklamasdan.
- Reporting/BI qatlami: bitta fakt jadvali bo'yicha agregatsiya va filtrlash metodlari.
- Reference/lookup ma'lumotlari (valyuta kurslari, soliq stavkalari) bilan ishlovchi modul.
- Legacy Oracle/DB2 sxemasi ustida ORM'siz, jadvalga yo'naltirilgan ishlash.
- Dedupe yoki ommaviy tozalash operatsiyalari: bir jadval ustida to'plamli SQL.

**Ehtiyot bo'ling:** Boy invariantlar va obyektlar o'rtasidagi murakkab munosabatlar bo'lsa, Table Module tez orada protsedural "SQL'ga o'ralgan god class"ga aylanadi. Domen chegaralari jadval chegaralaridan farq qilsa (bitta aggregate bir necha jadvalga yoyilgan bo'lsa) bu patterndan voz kechish kerak.

```java
// Table Module: bitta jadval uchun bitta modul, nusxa emas
@Service
public class ContractTable {
    private final JdbcClient db;

    public BigDecimal totalRevenue(int year) {
        return db.sql("SELECT coalesce(sum(amount),0) FROM contracts WHERE year = :y")
                .param("y", year).query(BigDecimal.class).single();
    }

    public List<ContractRow> expiring(LocalDate until) { /* ... */ }
}
// Hisobot va ommaviy ishlov uchun qulay: obyekt grafini yuklamaydi
```

## 8.4 Service qatlami (Service Layer)

**Tavsif:** Ilovaning tashqi chegarasida use-case'lar to'plamini ifodalovchi aniq API o'rnatadi: tranzaksiya, security, orkestrovka va domen chaqiruvlari shu qatlamda birlashtiriladi. Controller, scheduler yoki message listener kabi barcha kiruvchi adapterlar aynan shu qatlam bilan gaplashadi, shuning uchun bitta logika turli kanallarda takrorlanmaydi. Service qatlam yupqa (domen boy bo'lganda) yoki qalin (Transaction Script uslubida) bo'lishi mumkin.

**Spring'da qayerda uchraydi:** `@Service` stereotype, `@Transactional` (declarative tranzaksiya, `AnnotationTransactionAttributeSource` va AOP proxy orqali), metod darajasidagi `@PreAuthorize`/`@Secured` (Spring Security 6.x), hamda `@Validated` + Bean Validation 3.x (Jakarta `jakarta.validation`) argument tekshiruvi uchun. Spring Boot 3.x'da `@Observed` yoki Micrometer `ObservationRegistry` bilan service metodlarini kuzatish ham shu qatlamga qo'yiladi.

**Qo'llanish keyslari:**
- Bitta `placeOrder` use-case'i REST controller, Kafka listener va CLI job'dan bir xil chaqiriladi.
- Tranzaksion chegarani controller'dan ajratib, bir nechta repository chaqiruvini atomar qilish.
- Metod darajasidagi avtorizatsiya: faqat `ROLE_MANAGER` buyurtmani bekor qilishi mumkin.
- Tashqi integratsiyalarni (payment gateway, email) use-case ichida koordinatsiya qilish.
- Audit va metrikalarni bitta joyda, use-case granularligida yig'ish.

**Ehtiyot bo'ling:** `@Transactional` self-invocation (shu sinf ichidagi metodni `this.` orqali chaqirish) proxy'ni chetlab o'tadi va tranzaksiya ochilmaydi - bu eng ko'p uchraydigan tuzoq. Service qatlamni repository metodlarini shunchaki qayta chaqiruvchi "pass-through" sinflar bilan to'ldirmang: qiymat qo'shmaydigan qatlam faqat shovqin.

```java
// Service Layer: tranzaksiya chegarasi va use-case kirish nuqtasi
@Service
public class TransferService {
    private final AccountRepository accounts;
    private final DomainEventBus events;

    @Transactional
    public Receipt transfer(long fromId, long toId, Money amount) {
        Account from = accounts.findByIdForUpdate(fromId).orElseThrow();
        Account to = accounts.findByIdForUpdate(toId).orElseThrow();
        from.withdraw(amount);                  // qoida domenda
        to.deposit(amount);
        events.publish(new MoneyTransferred(fromId, toId, amount));
        return Receipt.of(from, to, amount);
    }
}
```

## 8.5 Application Service va Domain Service (Application Service vs Domain Service)

**Tavsif:** Application Service tashqi dunyo uchun use-case'ni boshqaradi: tranzaksiya ochadi, DTO'ni domen turlariga aylantiradi, repository'dan aggregate yuklaydi va natijani qaytaradi - lekin o'zida biznes qoidasi saqlamaydi. Domain Service esa aksincha, bitta aggregate'ga sig'maydigan sof domen qoidasini (masalan bir necha aggregate ustidagi hisob-kitobni) ifodalaydi va infrastrukturaga bog'lanmaydi. Bu ikkisini ajratish domen logikasini framework'dan mustaqil va test qilishga oson holda saqlaydi.

**Spring'da qayerda uchraydi:** Application Service - `@Service` + `@Transactional`, controller'ga eng yaqin qatlam; Domain Service - ko'pincha oddiy POJO yoki `@Component` bo'lib, `@Transactional` yoki repository'ga bog'liqligi minimal. Hexagonal/Spring Modulith uslubida domen paketda port interfeyslari (oddiy Java interface) e'lon qilinadi, adapterlar esa `@Repository`/`@Component` sifatida infrastruktura paketida bo'ladi; `ArchUnit` testlari bu yo'nalishni majburlaydi.

```java
@Service
class PlaceOrderService {                     // Application Service
    private final OrderRepository orders;
    private final PricingPolicy pricing;      // Domain Service (POJO)

    @Transactional
    public OrderId handle(PlaceOrderCommand cmd) {
        var order = Order.draft(cmd.customerId());
        order.applyPrice(pricing.quote(cmd.lines()));
        return orders.save(order).getId();
    }
}
```

**Qo'llanish keyslari:**
- `PricingPolicy` yoki `FxConversionService` kabi bir necha aggregate'ga tegishli hisob-kitoblar.
- Mablag' o'tkazmasi: ikki hisob aggregate'i ustidagi qoida Domain Service'da, tranzaksiya Application Service'da.
- DTO ↔ domen mapping va input validatsiyani domen logikasidan ajratish.
- Domen qoidalarini Spring konteksti ko'tarmasdan, sof JUnit 5 unit test bilan sinash.
- Bir use-case'ni bir nechta kanal (REST, gRPC, batch) uchun qayta ishlatish.

**Ehtiyot bo'ling:** Domain Service'ga `EntityManager`, HTTP client yoki `@Transactional` kirib kelsa, u aslida Application Service'ga aylanadi va ajratishning ma'nosi yo'qoladi. Shuningdek har bir aggregate uchun avtomatik "...DomainService" yasash anemic model belgisi - qoida avval aggregate ichida joy izlashi kerak.

## 8.6 Biznes delegati (Business Delegate)

**Tavsif:** Client (masalan web qatlam) bilan remote biznes service o'rtasiga abstraksiya qo'yadi: lookup, remote chaqiruv tafsilotlari va texnik exception'lar delegate ichida yashiriladi. Natijada presentation qatlam transport texnologiyasini bilmaydi va service joyi o'zgarsa client kodi o'zgarmaydi. Ko'pincha caching va retry ham shu yerda amalga oshiriladi.

**Spring'da qayerda uchraydi:** Zamonaviy ekvivalenti - deklarativ HTTP client interfeyslari: Spring Framework 6.x `@HttpExchange` + `HttpServiceProxyFactory` (`RestClient` yoki `WebClient` ustida) va Spring Cloud OpenFeign'dagi `@FeignClient`. Resilience `spring-retry` (`@Retryable`) yoki Resilience4j (`@CircuitBreaker`) annotatsiyalari bilan qo'shiladi; klassik EJB/RMI davrida esa `JndiObjectFactoryBean` va `RmiProxyFactoryBean` shu rolni bajargan.

**Qo'llanish keyslari:**
- Microservice'lar o'rtasidagi chaqiruvni interfeys ortida yashirib, HTTP tafsilotlarini izolyatsiya qilish.
- Tashqi payment yoki KYC provayderi API'sini domen tiliga yaqin interfeysga o'rash.
- Retry, timeout va circuit breaker siyosatini bitta joyda saqlash.
- Monolitdan microservice'ga ko'chirishda client kodini o'zgartirmasdan transportni almashtirish.
- Legacy EJB/SOAP service'ni zamonaviy Spring ilovasiga ulash.

**Ehtiyot bo'ling:** Delegate ichida biznes qoidasi paydo bo'lsa, u yashirin ikkinchi service qatlamga aylanadi - uni faqat transport va resilience uchun saqlang. Bitta jarayon ichidagi chaqiruvlar uchun ortiqcha delegate qo'shish keraksiz indirection beradi.

```java
// Business Delegate: mijoz tomonidagi kod masofaviy tafsilotni bilmaydi
@Component
public class PaymentDelegate {
    private final RestClient psp;

    public Receipt charge(Payment p) {
        try {
            return psp.post().uri("/charge").body(p).retrieve().body(Receipt.class);
        } catch (ResourceAccessException e) {       // tarmoq xatosi
            throw new PaymentUnavailableException(e);
        }
    }
}
// Chaqiruvchi HTTP, retry va serializatsiyani ko'rmaydi
```

## 8.7 Sessiya fasadi (Session Facade)

**Tavsif:** Bir nechta mayda biznes komponent (entity, DAO, helper) ustida bitta yirik, use-case'ga yo'naltirilgan interfeys yaratadi va shu chaqiruvni bitta tranzaksiyada bajaradi. Maqsad - client va server o'rtasidagi "chatty" chaqiruvlar sonini kamaytirish va tranzaksion/security chegarasini bir joyga to'plash. J2EE'da bu Stateless Session Bean sifatida amalga oshirilgan.

**Spring'da qayerda uchraydi:** Spring'da Session Facade roli coarse-grained `@Service` fasadiga to'g'ri keladi: bitta `@Transactional` metod ichida bir necha repository va domen chaqiruvi bajariladi, natijada client faqat bitta chaqiruv qiladi. Jakarta EE tomonida ekvivalenti `@Stateless` EJB; Spring Boot 3.x'da esa odatda `@RestController` ortidagi `ApplicationFacade`/`...UseCase` sinfi va `@Transactional(readOnly = true)` bilan o'qish fasadlari.

**Qo'llanish keyslari:**
- "Dashboard yuklash" use-case'i: bitta chaqiruvda profil, buyurtmalar va bildirishnomalar qaytariladi.
- Mobil client uchun N+1 HTTP chaqiruvni bitta coarse-grained endpoint'ga yig'ish.
- Checkout jarayoni: inventar, to'lov va buyurtma yaratish bitta tranzaksion fasad ichida.
- Legacy entity bean'lar ustida tranzaksion chegara o'rnatish.
- Security va audit tekshiruvini use-case darajasida markazlashtirish.

**Ehtiyot bo'ling:** Fasad vaqt o'tib "god service"ga aylanishi oson - har bir yangi ekran uchun metod qo'shilib, sinf minglab qatorga yetadi; fasadlarni use-case bo'yicha bo'lib saqlang. Agar fasad faqat bitta repository metodini chaqirsa, u keraksiz qatlam.

```java
// Session Facade: bir nechta ichki chaqiruvni bitta tranzaksiyada yig'adi
@Service
public class CheckoutFacade {
    private final CartService carts;
    private final InventoryService inventory;
    private final OrderService orders;

    @Transactional
    public OrderId checkout(long cartId) {
        Cart cart = carts.load(cartId);
        inventory.reserve(cart.items());        // uchta chaqiruv, bitta chegara
        return orders.create(cart);
    }
}
// Mijoz uchta servisni ketma-ket chaqirmaydi: chaqiruv soni va xato yuzasi kamayadi
```

## 8.8 Biznes obyekti (Business Object)

**Tavsif:** Domen tushunchasini (Customer, Invoice) ma'lumot va unga tegishli qoidalar bilan birga ifodalovchi obyekt - persistence va presentation tafsilotlaridan mustaqil bo'lishi kerak. Core J2EE kataloglarida bu Domain Model'ning konkret qurilish bloki sifatida keltiriladi: holat + validatsiya + xatti-harakat. DTO'dan farqi - Business Object logika saqlaydi, DTO esa faqat ma'lumot tashiydi.

**Spring'da qayerda uchraydi:** JPA `@Entity`/`@Embeddable` sinflari yoki Spring Data JDBC aggregate sinflari, hamda sof POJO domen sinflari. Invariantlarni Bean Validation 3.x (`@NotNull`, `@Positive`, `jakarta.validation`) va konstruktor ichidagi tekshiruvlar bilan qo'riqlash mumkin; Java 17+ `record` o'zgarmas Value Object uchun, `sealed interface` esa domen holat ierarxiyasi uchun ishlatiladi.

**Qo'llanish keyslari:**
- `Money`, `Email`, `Iban` kabi o'zgarmas Value Object'lar, ular o'z formatini o'zi tekshiradi.
- `Invoice` obyekti ichida umumiy summa va soliq hisoblash metodlari.
- Status mashinasi: `Order.cancel()` faqat ruxsat etilgan holatdan ishlaydi.
- Bir nechta kanal (REST, batch) tomonidan qayta ishlatiluvchi domen qoidalari.
- JPA'siz, sof domen sinflarini unit test bilan tez tekshirish.

**Ehtiyot bo'ling:** Business Object'ni Jackson yoki JPA talablariga moslashtirib, hamma maydonga setter va bo'sh konstruktor qo'shish invariantlarni buzadi - API chegarasida alohida DTO ishlating. Shuningdek domen sinfiga `@Autowired` yoki repository bog'liqligini kiritish uni test qilishni qiyinlashtiradi.

```java
// Business Object: domen tushunchasi, saqlash tafsilotidan mustaqil
public class Invoice {
    private final InvoiceId id;
    private final List<LineItem> lines;
    private InvoiceStatus status;

    public Money total() {
        return lines.stream().map(LineItem::amount)
                .reduce(Money.zero("UZS"), Money::plus);
    }

    public void issue() {
        if (lines.isEmpty()) throw new EmptyInvoiceException(id);
        this.status = InvoiceStatus.ISSUED;
    }
}
```

## 8.9 Kompozit entity (Composite Entity)

**Tavsif:** Bir nechta o'zaro bog'liq persistent obyektni bitta coarse-grained entity ostida birlashtiradi, shunda client ichki obyektlarga alohida murojaat qilmaydi. Ichki obyektlar mustaqil identifikatsiyaga ega bo'lmaydi va faqat "root" orqali boshqariladi - bu tranzaksion yaxlitlikni va remote chaqiruvlar sonini yaxshilaydi. DDD'dagi Aggregate va Aggregate Root g'oyasining bevosita ajdodi.

**Spring'da qayerda uchraydi:** JPA'da `@OneToMany(cascade = CascadeType.ALL, orphanRemoval = true)` va `@ElementCollection` bilan root entity ostidagi bolalar boshqariladi. Spring Data JDBC bu modelni yanada qat'iy qo'llaydi: aggregate root saqlanganda butun ichki graf qayta yoziladi va repository faqat root uchun yaratiladi. Spring Data MongoDB'da esa `@Document` ichida nested obyektlar bitta yozuv sifatida saqlanadi.

**Qo'llanish keyslari:**
- `Order` + `OrderLine`: satrlar faqat buyurtma orqali qo'shiladi va o'chiriladi.
- `Invoice` + `InvoiceItem` + `TaxBreakdown` bitta tranzaksion birlik sifatida saqlanishi.
- Anketa yoki forma: savol va javoblar root'dan ajralgan holda ma'noga ega emas.
- Konfiguratsiya aggregate'i: bir nechta sozlama bloki bitta versiyalangan yozuvda.
- MongoDB'da nested dokument sifatida saqlanadigan buyurtma yoki profil.

**Ehtiyot bo'ling:** Aggregate chegarasini juda katta qilib belgilash lock contention va og'ir yuklanishga olib keladi - bir aggregate'da minglab bola yozuv bo'lsa, pagination va partial update imkonsiz bo'ladi. Ichki obyektlarga tashqaridan to'g'ridan-to'g'ri repository berish Composite Entity'ning butun ma'nosini yo'qotadi.

```java
// Composite Entity: qo'pol donali ildiz, mayda bo'laklar ichda
@Entity
public class Order {
    @Id private Long id;

    @OneToMany(mappedBy = "order", cascade = CascadeType.ALL, orphanRemoval = true)
    private final List<OrderLine> lines = new ArrayList<>();   // faqat ildiz orqali

    public void addLine(Product p, int qty) {
        lines.add(new OrderLine(this, p, qty));   // invariant ildizda tekshiriladi
    }
}
// OrderLine uchun alohida repository bo'lmasligi kerak: u ildizga tegishli
```

## 8.10 Ma'lumot uzatish obyekti (Transfer Object / DTO)

**Tavsif:** Qatlamlar yoki jarayonlar o'rtasida ma'lumotni bitta serializable obyektda tashiydi, shunda har bir maydon uchun alohida chaqiruv qilish kerak bo'lmaydi. DTO biznes logikasiz bo'lib, aniq bir client ehtiyojiga moslashtiriladi va domen modelini tashqi API'dan ajratadi. Bu ajratish tufayli domen refaktoringi API contract'ini buzmaydi.

**Spring'da qayerda uchraydi:** `@RestController` metodlarining request/response turlari - odatda Java 17+ `record`, Jackson (`@JsonProperty`, `@JsonView`) bilan serializatsiya qilinadi va `@Valid` + Bean Validation 3.x bilan tekshiriladi. Mapping uchun MapStruct (compile-time) yoki qo'lda yozilgan static factory metodlari ishlatiladi; Spring Data'ning interface/class-based projection'lari (`findAllBy...` natijasi) esa DTO'ni to'g'ridan-to'g'ri so'rovdan olish imkonini beradi.

**Qo'llanish keyslari:**
- REST API response contract'ini JPA entity'dan ajratib, entity o'zgarishini client'dan yashirish.
- Faqat kerakli maydonlarni tanlab, Spring Data projection orqali og'ir entity yuklamaslik.
- Kafka yoki RabbitMQ xabar payload'i uchun versiyalangan, barqaror sxema.
- Parol yoki ichki ID kabi maydonlarni javobdan chiqarib tashlash.
- Mobil va web client uchun bir domen asosida turli shakldagi javob berish.

**Ehtiyot bo'ling:** Entity'ni to'g'ridan-to'g'ri controller'dan qaytarish lazy loading muammolari va ma'lumot oshkor bo'lishiga olib keladi - DTO'ni o'tkazib yubormang. Boshqa chekka - har bir qatlam uchun bir xil DTO'larni ko'paytirish; mapping xarajati foydadan oshsa, projection yoki yagona API DTO yetarli.

```java
// DTO: tashqi shartnoma, entity emas
public record OrderDto(long id, String status, String total, List<LineDto> lines) {
    public static OrderDto of(Order o) {
        return new OrderDto(o.id(), o.status().name(), o.total().toString(),
                o.lines().stream().map(LineDto::of).toList());
    }
}
// Entity'ni API da qaytarish: lazy load xatolari, maydon oqishi va
// sxema o'zgarishi bilan birga API o'zgarishi degani.
```

## 8.11 Transfer Object yig'uvchi (Transfer Object Assembler)

**Tavsif:** Bir nechta manbadan (turli business object, service yoki microservice'dan) ma'lumot yig'ib, client uchun yagona kompozit DTO yasaydi. Client model butunligini bilishi shart emas: u faqat bitta chaqiruv bilan tayyor "view model" oladi. Odatda faqat o'qish uchun ishlatiladi va bir nechta chaqiruvni parallel bajarish mumkin.

**Spring'da qayerda uchraydi:** `@Service` ichidagi assembler metodi bir necha repository va HTTP client (`RestClient`, `WebClient`) natijalarini birlashtiradi; parallel yig'ish uchun `CompletableFuture` yoki Java 21+ `StructuredTaskScope`, reaktiv stack'da esa `Mono.zip(...)` ishlatiladi. Mapping uchun MapStruct, GraphQL uslubida esa Spring for GraphQL'ning `@SchemaMapping`/`@BatchMapping` metodlari aynan assembler rolini bajaradi.

**Qo'llanish keyslari:**
- BFF (Backend For Frontend) endpoint'i: profil, buyurtmalar va tavsiyalar bitta javobda.
- Dashboard view model'ini 4-5 microservice javobidan parallel yig'ish.
- Hisobot sahifasi uchun DB agregatlari va tashqi kurs ma'lumotini birlashtirish.
- GraphQL `@BatchMapping` bilan N+1 chaqiruvni oldini olib, bog'liq ma'lumot yig'ish.
- Mobil ilova uchun chaqiruv sonini kamaytiruvchi coarse-grained read endpoint.

**Ehtiyot bo'ling:** Assembler ichida yozish operatsiyalari yoki biznes qoidasi paydo bo'lsa, u tranzaksion mas'uliyati noaniq hybrid'ga aylanadi - uni read-only saqlang. Ketma-ket (sequential) remote chaqiruvlar latency'ni ko'paytiradi: timeout va fallback siyosatini albatta belgilang.

```java
// Transfer Object Assembler: bir nechta manbadan bitta DTO yig'adi
@Service
public class CustomerOverviewAssembler {
    private final CustomerRepository customers;
    private final OrderClient orders;
    private final BillingClient billing;

    public CustomerOverview assemble(long id) {
        Customer c = customers.findById(id).orElseThrow();
        return new CustomerOverview(
                CustomerDto.of(c),
                orders.recent(id, 5),
                billing.balance(id));
    }
}
```

## 8.12 Qiymatlar ro'yxati boshqaruvchisi (Value List Handler)

**Tavsif:** Katta natija to'plamini client'ga bo'lak-bo'lak (page) yetkazadi: butun ro'yxatni xotiraga yuklamasdan, faqat so'ralgan oynani qaytaradi. So'rov holatini (sort, filter, kursor) boshqarib, "keyingi sahifa" chaqiruvlarini samarali bajaradi. Bu pattern pagination va iteratsiyani service qatlamining aniq mas'uliyatiga aylantiradi.

**Spring'da qayerda uchraydi:** Spring Data'ning `Pageable`, `Page<T>`, `Slice<T>` va `Sort` abstraksiyalari; `PageableHandlerMethodArgumentResolver` HTTP `?page=&size=&sort=` parametrlarini avtomatik bog'laydi. Katta to'plamlar uchun `Window<T>` + `ScrollPosition` (keyset pagination, Spring Data 3.1+) yoki `Stream<T>` qaytaruvchi repository metodi va `@QueryHints(@QueryHint(name = HINT_FETCH_SIZE, ...))` ishlatiladi; Spring Batch'da esa `JdbcPagingItemReader`/`JdbcCursorItemReader`.

**Qo'llanish keyslari:**
- Admin panelidagi million satrli jadvalni sahifalab, sortlab ko'rsatish.
- Infinite scroll uchun `Slice` qaytarib, ortiqcha `count(*)` so'rovidan qutulish.
- Keyset (cursor) pagination bilan chuqur sahifalarda `OFFSET` sekinlashuvini yo'q qilish.
- Katta eksport job'ida `Stream` yoki paging reader orqali xotirani barqaror ushlash.
- Qidiruv natijalarini filtrlar bilan birga, barqaror tartibda sahifalash.

**Ehtiyot bo'ling:** `OFFSET`ga asoslangan pagination chuqur sahifalarda sekinlashadi va ma'lumot o'zgarganda satrlar takrorlanib yoki tushib qolishi mumkin - barqaror sort kaliti yoki keyset ishlating. `findAll()` bilan butun jadvalni yuklash va xotirada sahifalash esa to'g'ridan-to'g'ri `OutOfMemoryError`ga yo'l.

```java
// Value List Handler: katta ro'yxatni sahifalab beradi, hammasini yuklamaydi
@Service
public class OrderListHandler {
    private final OrderRepository repo;

    public Slice<OrderRow> page(OrderFilter filter, Pageable pageable) {
        // Slice: umumiy sonni hisoblamaydi, shuning uchun COUNT so'rovi yo'q
        return repo.findProjectedBy(filter.toSpec(), pageable);
    }
}
// Katta jadvalda `Page` ni `Slice` ga almashtirish COUNT(*) ni olib tashlaydi
```

## 8.13 Masofaviy fasad (Remote Facade)

**Tavsif:** Mayda granulali domen obyektlari ustida coarse-grained, tarmoq uchun optimallashtirilgan interfeys yaratadi: bitta chaqiruvda ko'p ma'lumot uzatiladi va remote chaqiruvlar soni minimallashadi. Remote Facade o'zida biznes logika saqlamaydi - u faqat tarjimon va to'plovchi: DTO yasaydi, domenga delegatsiya qiladi. Tarmoq latency'si eng katta xarajat bo'lgan joyda muhim.

**Spring'da qayerda uchraydi:** `@RestController`/`@GraphQlController` yoki gRPC service implementatsiyasi aynan Remote Facade vazifasini bajaradi: so'rovni DTO'ga bog'laydi (`@RequestBody`, `@Valid`), use-case'ga delegatsiya qiladi va DTO qaytaradi. Spring Framework 6.x'da `@HttpExchange` interfeyslari client tomonda shu fasadning oynasi bo'ladi; `@RestControllerAdvice` + `ProblemDetail` (RFC 9457) esa xatolarni remote contract'ga mos shaklga keltiradi.

**Qo'llanish keyslari:**
- Public REST API: ichki domen modelini yashirib, barqaror coarse-grained contract berish.
- Mobil client uchun bitta chaqiruvda ekranga kerakli hamma ma'lumotni qaytarish.
- gRPC yoki GraphQL fasadi orqali bir xil use-case'larni turli transportda ochish.
- Ichki exception'larni `ProblemDetail` ko'rinishidagi standart xato javobiga aylantirish.
- Versiyalangan API (`/v1`, `/v2`) ni bitta domen modeli ustida parallel saqlash.

**Ehtiyot bo'ling:** Fasadga biznes qoidasi, tranzaksiya boshqaruvi yoki SQL kirib kelsa, u test qilinishi qiyin "fat controller"ga aylanadi - logikani service/domen qatlamida qoldiring. Shuningdek domen entity'larini fasaddan to'g'ridan-to'g'ri serializatsiya qilish API'ni domen refaktoringiga qattiq bog'lab qo'yadi.

```java
// Remote Facade: qo'pol donali interfeys, chaqiruv soni kam
@RestController
@RequestMapping("/checkout")
class CheckoutApi {

    // Yomon: mijoz 5 marta chaqiradi (setAddress, setPayment, addItem, ...)
    // Yaxshi: bitta chaqiruvda butun niyat
    @PostMapping
    ResponseEntity<OrderDto> checkout(@Valid @RequestBody CheckoutCommand cmd) {
        return ResponseEntity.status(201).body(facade.checkout(cmd));
    }
}
// Masofaviy chaqiruv qimmat: mayda donali API latency'ni ko'paytiradi
```

## 8.14 Mapper (Mapper - MapStruct, ModelMapper)

**Tavsif:** Mapper pattern bir qatlamning model obyektini boshqa qatlamning modeliga (entity → DTO, DTO → domain command) aylantirish mantiqini alohida komponentga ajratadi. Bu service metodlarini qo'lda yozilgan o'nlab setter chaqiruvlaridan xalos qiladi va konvertatsiya qoidalarini bitta joyda saqlaydi. MapStruct bu kodni compile-time'da generatsiya qiladi, ModelMapper esa runtime'da reflection bilan ishlaydi. Natijada qatlamlar orasidagi model chegarasi aniq bo'lib, entity'lar API kontraktiga "oqib" ketmaydi.

**Spring'da qayerda uchraydi:** MapStruct (`org.mapstruct:mapstruct` + `mapstruct-processor`) `@Mapper(componentModel = "spring")` orqali mapper'ni oddiy Spring bean sifatida generatsiya qiladi, shu bilan uni `@Service` ichiga constructor injection bilan olish mumkin; `@Mapping`, `@MappingTarget`, `@AfterMapping`, `uses = {...}` bilan murakkab holatlar boshqariladi. ModelMapper/Dozer runtime variantlari `@Bean ModelMapper modelMapper()` sifatida ro'yxatga olinadi. Spring'ning o'zida ham konvertatsiya infratuzilmasi bor: `Converter<S,T>`, `ConversionService`, `@Component` bilan ro'yxatga olingan `GenericConverter`, hamda Spring Data REST/Projection interface'lari. Java 17+ `record` DTO'lari MapStruct tomonidan constructor orqali to'liq qo'llab-quvvatlanadi.

**Qo'llanish keyslari:**
- JPA entity'ni REST javob DTO'siga aylantirish va `password`, `internalNotes` kabi maydonlarni javobdan chiqarib tashlash.
- Tashqi integratsiya (SOAP/REST partner API) modelini ichki domain modeliga tarjima qilish.
- Bir nechta entity'ni bitta aggregated response DTO'ga yig'ish (`@Mapping(source = "user.profile.city", target = "city")`).
- PATCH so'rovida faqat kelgan maydonlarni mavjud entity ustiga yozish (`@MappingTarget` + `NullValuePropertyMappingStrategy.IGNORE`).
- Kafka/event payload'ini domain command obyektiga map qilish.

**Ehtiyot bo'ling:** ModelMapper kabi reflection-based mapper'lar maydon nomi o'zgarganda compile-time'da xato bermaydi va noto'g'ri yoki `null` map natijasi faqat production'da chiqadi - shuning uchun MapStruct afzal. Mapper ichiga biznes qoidasi (narx hisoblash, status tekshirish) yozmang; lazy JPA assotsiatsiyalarini map qilish esa transaction tashqarisida `LazyInitializationException` yoki N+1 so'rovga olib keladi.

```java
// Mapper: aylantirish kodi generatsiya qilinadi, qo'lda yozilmaydi
@Mapper(componentModel = "spring",
        unmappedTargetPolicy = ReportingPolicy.ERROR)   // yangi maydon unutilmaydi
public interface OrderMapper {

    @Mapping(target = "total", expression = "java(order.total().toString())")
    OrderDto toDto(Order order);

    List<OrderDto> toDtos(List<Order> orders);
}
// unmappedTargetPolicy = ERROR: DTO ga maydon qo'shilsa build yiqiladi,
// jimgina `null` qolib ketmaydi.
```

## 8.15 Buyruq / Use Case Handler (Command / Use Case Handler - Interactor)

**Tavsif:** Har bir biznes amali (use case) o'zining alohida handler sinfiga joylashtiriladi: input sifatida immutable command obyekti keladi, handler uni bajaradi va natija qaytaradi. Bu "god service" (1000 qatorli `UserService`) muammosini hal qiladi - har bir sinf bitta javobgarlikka ega bo'ladi va mustaqil test qilinadi. Clean Architecture va Hexagonal arxitekturada bu qatlam "application layer" deb ataladi. Handler faqat orkestratsiya qiladi: domain obyektlarini yuklaydi, ularning metodlarini chaqiradi, repository orqali saqlaydi.

**Spring'da qayerda uchraydi:** Odatiy amalga oshirish - `CommandHandler<C, R>` yoki `UseCase<I, O>` generic interface va uni implement qiluvchi `@Service`/`@Component` sinflar (`PlaceOrderHandler implements UseCase<PlaceOrderCommand, OrderId>`), command'lar Java `record` sifatida. Spring tranzaksiyani `@Transactional` bilan handler'ning `handle` metodiga qo'yadi, validatsiya esa `@Validated` + `jakarta.validation` annotatsiyalari bilan command'da amalga oshiriladi. Spring Modulith (`spring-modulith-core`) bu uslubni modul-ichi application service sifatida rasmiylashtiradi; Axon Framework'da esa `@CommandHandler` annotatsiyasi bor. Controller handler'ni to'g'ridan-to'g'ri inject qiladi yoki Command Bus orqali chaqiradi.

**Qo'llanish keyslari:**
- `PlaceOrderHandler`, `CancelOrderHandler`, `RefundOrderHandler` - har bir buyurtma amali alohida sinf.
- Katta monolitda `OrderService`ni o'nlab mustaqil use case'ga bo'lib, merge conflict va regressiyani kamaytirish.
- CQRS'da yozish tomonini (command handler) o'qish tomonidan (query service) ajratish.
- Bir xil use case'ni HTTP controller, Kafka consumer va scheduled job'dan qayta ishlatish.
- Audit log: har bir command obyektini bajarilishdan oldin serialize qilib saqlash.

**Ehtiyot bo'ling:** Kichik CRUD loyihada har bir metod uchun alohida sinf yaratish sun'iy murakkablik keltiradi - bu pattern domain mantiqi boy bo'lganda foyda beradi. Handler'lar bir-birini chaqira boshlasa, tranzaksiya chegarasi va nested use case bog'liqliklari chigallashadi; umumiy mantiqni domain service'ga chiqaring.

```java
// Use case handler: bitta sinf, bitta amal, aniq kirish va chiqish
public record CancelOrder(long orderId, String reason) {}

@Service
public class CancelOrderHandler {
    private final OrderRepository orders;

    @Transactional
    public void handle(CancelOrder cmd) {
        Order order = orders.findById(cmd.orderId()).orElseThrow();
        order.cancel(cmd.reason());          // qoida domenda
        orders.save(order);
    }
}
// 300 qatorlik OrderService o'rniga 10 ta kichik handler
```

## 8.16 Buyruq shinasi / Mediator (Command Bus / Mediator)

**Tavsif:** Command Bus chaqiruvchi (controller) va handler o'rtasida vositachi bo'lib, command tipiga qarab mos handler'ni topadi va unga yuboradi. Chaqiruvchi aniq handler sinfiga bog'liq bo'lmaydi - faqat `bus.send(command)` deb chaqiradi. Shina ustiga kesishgan mantiq (validatsiya, logging, metrika, retry, tranzaksiya) decorator/pipeline sifatida qo'shiladi. Bu Mediator pattern'ning application qatlamidagi ko'rinishi.

**Spring'da qayerda uchraydi:** Spring'ning o'zida command bus yo'q, lekin uni oson yasash mumkin: barcha `CommandHandler<C,R>` bean'larini `List<CommandHandler<?,?>>` yoki `Map<Class<?>, CommandHandler<?,?>>` sifatida inject qilib, `ResolvableType`/`GenericTypeResolver` bilan generic tipni aniqlash. Tayyor kutubxonalar: Axon Framework (`CommandGateway`, `@CommandHandler`), `an.awesome:pipelinr`, `io.github.jkratz55:spring-mediatr`. Spring'ning native alternativalari - `ApplicationEventPublisher` + `@EventListener` (fire-and-forget uchun) va `@Async`. Pipeline bosqichlari Spring AOP (`@Around` advice) yoki qo'lda yozilgan decorator bean'lar bilan ulanadi.

**Qo'llanish keyslari:**
- Controller'larda o'nlab service dependency o'rniga bitta `CommandBus` inject qilish.
- Barcha command'lar uchun markazlashgan validatsiya va `MDC` correlation-id to'ldirish.
- Tranzaksiya, retry va rate-limit'ni pipeline bosqichi sifatida bir joyda qo'llash.
- Axon bilan event-sourced aggregate'larga command yuborish.
- Command'larni bajarishdan oldin ruxsat (authorization) tekshiruvini bitta interceptor'da qilish.

**Ehtiyot bo'ling:** Bus stack trace'ni va IDE'dagi "find usages" navigatsiyasini buzadi - kichik loyihada handler'ni to'g'ridan-to'g'ri inject qilish ancha ravshan. Generic tipni runtime'da yechish type-safety'ni yo'qotadi, shuning uchun handler ro'yxatini ilova ishga tushganda tekshiruvdan o'tkazing (har bir command uchun aynan bitta handler bor-yo'qligini).

```java
// Command bus: chaqiruvchi handler'ni bilmaydi
public interface CommandHandler<C> { void handle(C command); }

@Service
public class CommandBus {
    private final Map<Class<?>, CommandHandler<Object>> handlers;

    @SuppressWarnings("unchecked")
    public CommandBus(List<CommandHandler<?>> all) {
        this.handlers = all.stream().collect(Collectors.toMap(
                h -> GenericTypeResolver.resolveTypeArgument(h.getClass(), CommandHandler.class),
                h -> (CommandHandler<Object>) h));
    }

    public void dispatch(Object command) {
        handlers.get(command.getClass()).handle(command);
    }
}
```

## 8.17 Tranzaksiya chegarasi (Transaction Boundary - @Transactional on service)

**Tavsif:** Tranzaksiya chegarasi - bu "biznes amali atomar bajariladigan" aniq belgilangan nuqta. To'g'ri joyi service (use case) qatlami: controller juda yuqori (HTTP so'rov DB tranzaksiyasiga teng emas), repository juda past (bir use case bir nechta repository chaqiradi). Spring buni declarative tarzda `@Transactional` bilan amalga oshiradi va proxy orqali `begin/commit/rollback`ni boshqaradi. Shu chegara ichida JPA persistence context, optimistik lock va domain event'larni commit'ga bog'lash ishlaydi.

**Spring'da qayerda uchraydi:** `org.springframework.transaction.annotation.@Transactional` service metodida; `PlatformTransactionManager` (`JpaTransactionManager`, `DataSourceTransactionManager`) yoki reaktiv `ReactiveTransactionManager`. Atributlar: `propagation` (`REQUIRED`, `REQUIRES_NEW`, `NESTED`), `isolation`, `readOnly = true`, `timeout`, `rollbackFor`, `noRollbackFor`. Programmatic variant - `TransactionTemplate` va Spring Framework 6'dagi `TransactionalOperator` (reaktiv). Spring Boot 3.x/4.x'da `spring-boot-starter-data-jpa` tranzaksiyani avtomatik sozlaydi; `@TransactionalEventListener(phase = AFTER_COMMIT)` esa event'ni commit'dan keyin ishlatadi. Spring Boot 3.x'da AOP default sifatida CGLIB proxy ishlatadi.

**Qo'llanish keyslari:**
- Bir use case ichida bir nechta jadvalga yozishni atomar qilish (buyurtma + ombor rezervi + to'lov yozuvi).
- `readOnly = true` bilan o'qish metodlarida Hibernate flush/dirty-check'ni o'chirib, replica'ga yo'naltirish.
- `REQUIRES_NEW` bilan audit yoki xato log yozuvini asosiy tranzaksiya rollback bo'lsa ham saqlash.
- Optimistik lock (`@Version`) konfliktini bitta tranzaksiya chegarasida ushlab, retry qilish.
- Outbox jadvaliga xabar yozishni biznes o'zgarishi bilan bitta commit'ga bog'lash.

**Ehtiyot bo'ling:** Proxy sababli bir sinf ichida `this.otherTransactionalMethod()` chaqirilsa `@Transactional` ishlamaydi, `private`/`final` metodlarga ham ta'sir qilmaydi; shuningdek default holatda faqat unchecked exception rollback qiladi (checked uchun `rollbackFor` kerak). Tranzaksiya ichida HTTP chaqiruv yoki uzoq hisob-kitob qilish connection pool'ni bo'g'adi - tashqi I/O'ni chegaradan tashqariga chiqaring.

```java
// Chegara servisda: bitta biznes amal = bitta tranzaksiya
@Service
public class OrderService {

    @Transactional                           // chegara shu yerda boshlanadi
    public void place(CreateOrder cmd) {
        Order order = Order.from(cmd);
        orders.save(order);
        inventory.reserve(order.items());    // bir xil tranzaksiyada
    }

    @Transactional(readOnly = true)          // o'qish uchun aniq belgilanadi
    public OrderDto view(long id) { /* ... */ }
}
// Controller va repository darajasida @Transactional qo'ymang:
// biri juda keng, ikkinchisi juda tor chegara beradi.
```

## 8.18 Notification (Notification - validatsiya xatolarini yig'ish)

**Tavsif:** Birinchi xatoda exception tashlash o'rniga, barcha validatsiya muammolari `Notification` obyektiga yig'iladi va oxirida birgalikda qaytariladi. Bu foydalanuvchiga formadagi hamma xatoni bir martada ko'rsatish imkonini beradi va "bir xato tuzatdim - ikkinchisi chiqdi" aylanishini yo'q qiladi. Martin Fowler ta'rifiga ko'ra Notification - bu xatolar ro'yxatini saqlovchi, `hasErrors()` va `addError(...)` metodlariga ega oddiy obyekt. Domain qoidalari ham exception'siz tekshirilib, natija shu obyektga yoziladi.

**Spring'da qayerda uchraydi:** Spring'ning tabiiy Notification analogi - `org.springframework.validation.Errors`/`BindingResult` va `Validator` interface'i (`validate(Object target, Errors errors)`), hamda `ValidationUtils.rejectIfEmpty(...)`. Bean Validation (`jakarta.validation`) `@Valid`/`@Validated` bilan barcha constraint'larni bir yo'la tekshirib `MethodArgumentNotValidException` yoki `ConstraintViolationException` ichida `Set<ConstraintViolation<?>>` qaytaradi - bu ham yig'ilgan xatolar ro'yxati. Ularni `@RestControllerAdvice` + `@ExceptionHandler` ichida `ProblemDetail` (RFC 9457, Spring Framework 6+) formatiga aylantirish standart yo'l. Service qatlamida o'z `Notification` record'ingizni yozib, uni `Result` obyektiga joylash mumkin.

**Qo'llanish keyslari:**
- Ko'p maydonli registratsiya yoki to'lov formasining barcha xatolarini bitta 400 javobda qaytarish.
- CSV/Excel import: har bir qator uchun xatolarni yig'ib, oxirida to'liq hisobot berish.
- Bir nechta biznes qoidasini (limit, muddat, status) ketma-ket tekshirib, hammasini ko'rsatish.
- Ko'p qadamli wizard'da qadam yakunida to'plangan ogohlantirish va xatolarni ajratish.
- Batch job'da muvaffaqiyatsiz yozuvlar sababini yig'ib, dead-letter jadvaliga yozish.

**Ehtiyot bo'ling:** Notification'ni invariant buzilishi uchun ishlatmang - domain holatini noto'g'ri qilib qo'yadigan holatda exception to'g'riroq; Notification kirish ma'lumotini tekshirish uchun. Shuningdek `hasErrors()` natijasini tekshirishni unutib, xatoli ma'lumot bilan davom etish - bu pattern'ning eng ko'p uchraydigan tuzog'i.

```java
// Notification: bir nechta xatoni yig'ib bir marta qaytarish
public final class Notification {
    private final List<String> errors = new ArrayList<>();

    public void require(boolean condition, String message) {
        if (!condition) errors.add(message);
    }
    public boolean hasErrors() { return !errors.isEmpty(); }
    public List<String> errors() { return List.copyOf(errors); }
}

public Notification validate(TransferRequest r) {
    Notification n = new Notification();
    n.require(r.amount().signum() > 0, "Summa noldan katta bo'lishi kerak");
    n.require(!Objects.equals(r.from(), r.to()), "Hisoblar bir xil");
    return n;                                 // foydalanuvchi hammasini birga ko'radi
}
```

## 8.19 Natija obyekti vs Exception (Result Object vs Exceptions)

**Tavsif:** Kutilgan biznes muvaffaqiyatsizligi (balans yetarli emas, kod muddati o'tgan) exception emas - u metodning normal natijalaridan biri. Result obyekti muvaffaqiyat qiymatini yoki xato sababini explicit tarzda qaytaradi, shuning uchun chaqiruvchi uni ignore qila olmaydi va control flow o'qilishi oson bo'ladi. Exception'lar esa haqiqiy anomal holatlar uchun qoldiriladi: DB uzilishi, bug, invariant buzilishi. Bu ayirma performance (stack trace qimmat) va API kontraktining ravshanligi uchun ham muhim.

**Spring'da qayerda uchraydi:** Java'da Result'ni `sealed interface` + `record` bilan yozish Java 17+ `switch` pattern matching bilan juda qulay; kutubxonalar - Vavr `Either<L,R>`/`Try<T>`, `io.vavr.control.Validation`. Spring ekosistemasida Result obyekti controller qatlamida `ResponseEntity` yoki `ProblemDetail`ga aylantiriladi. Exception yo'li esa Spring'ning `@RestControllerAdvice`, `ResponseStatusException`, `ErrorResponseException` va `@ExceptionHandler` infratuzilmasi bilan yaxshi integratsiyalashgan; Spring'ning o'zi `DataAccessException` ierarxiyasida unchecked exception'larni afzal ko'radi. Diqqat: `@Transactional` rollback exception'ga bog'langani uchun Result qaytarilganda tranzaksiya commit bo'ladi.

**Qo'llanish keyslari:**
- To'lov provayderidan "insufficient funds" javobi - Result bilan, tarmoq uzilishi - exception bilan.
- Promo-kod tekshirish: `Invalid`, `Expired`, `AlreadyUsed` holatlarini sealed tip bilan modellashtirish.
- Batch qayta ishlashda har bir element natijasini `List<Result<T>>` sifatida yig'ish.
- Autentifikatsiya: noto'g'ri parol kutilgan natija, LDAP server o'chgani - exception.
- Hot path'da (minutda yuz minglab chaqiruv) exception yaratish narxidan qochish.

**Ehtiyot bo'ling:** Result'ni qaytarib, biznes xatosida tranzaksiya rollback bo'lishini kutish - klassik xato: `TransactionAspectSupport.currentTransactionStatus().setRollbackOnly()` yoki exception kerak. Barcha narsani Result'ga o'tkazish ham zarar: har bir chaqiruvda `if (result.isFailure())` tekshiruvi kod shovqinini oshiradi, shuning uchun faqat kutilgan, ma'noli muvaffaqiyatsizliklar uchun ishlating.

```java
// Natija obyekti: kutilgan xato oqimning bir qismi
public sealed interface TransferResult {
    record Success(Receipt receipt) implements TransferResult {}
    record InsufficientFunds(Money available) implements TransferResult {}
    record AccountFrozen(long accountId) implements TransferResult {}
}

// Chaqiruvchi barcha holatni qamrab olishga majbur
String message = switch (service.transfer(cmd)) {
    case TransferResult.Success s -> "Bajarildi: " + s.receipt().reference();
    case TransferResult.InsufficientFunds f -> "Mablag' yetarli emas: " + f.available();
    case TransferResult.AccountFrozen a -> "Hisob bloklangan";
};
// Istisno kutilmagan holat uchun qoladi, kutilgan natija uchun emas
```

## 8.20 Siyosat obyekti (Policy Object)

**Tavsif:** Policy object - bitta biznes qoidasini (chegirma shartlari, kredit limiti, qaytarish siyosati) alohida, nomlangan va test qilinadigan obyektga ajratish. Qoida service metodining ichidagi chigal `if` zanjiridan chiqib, domenning birinchi darajali tushunchasiga aylanadi: `RefundPolicy.isRefundable(order)`. Odatda Specification/Rules pattern'lari bilan birgalikda ishlatiladi va qoidalarni `and`/`or` bilan kompozitsiya qilish mumkin. Qoida o'zgarganda faqat bitta sinf o'zgaradi, service esa tegilmaydi.

**Spring'da qayerda uchraydi:** Oddiy `@Component` sinf yoki domain qatlamidagi framework'siz POJO/`record` sifatida; bir nechta policy'ni `List<DiscountPolicy>` sifatida inject qilib, `@Order`/`Ordered` bilan tartiblash mumkin. Spring Data JPA'da ma'lumot bazasi darajasidagi policy'lar `Specification<T>` (`org.springframework.data.jpa.domain.Specification`) sifatida yozilib `and()`/`or()` bilan birlashtiriladi. Xavfsizlik policy'lari uchun Spring Security `AuthorizationManager`, `PermissionEvaluator` va `@PreAuthorize` SpEL ifodalari mavjud. Murakkab, biznes tomonidan boshqariladigan qoidalar uchun Drools yoki Easy Rules integratsiya qilinadi.

**Qo'llanish keyslari:**
- Mijoz segmentiga qarab chegirma hisoblash qoidalarini alohida policy'larga ajratish.
- Buyurtmani bekor qilish shartlari (muddat, status, to'lov holati) uchun `CancellationPolicy`.
- Spring Data `Specification` bilan dinamik filtr qoidalarini qayta ishlatiladigan bo'laklarga bo'lish.
- Kredit berish/limit oshirish qarorlari uchun bir nechta policy'ni ketma-ket qo'llash.
- Ko'p tenant'li tizimda har bir tenant uchun boshqa policy implementatsiyasini ulash.

**Ehtiyot bo'ling:** Har bir kichik `if` uchun sinf yaratish policy portlashiga olib keladi - faqat o'zgarib turuvchi yoki biznes tomonidan muhokama qilinadigan qoidalarni ajratish kerak. Policy ichida repository chaqirib DB'ga murojaat qilish uni sekin va test qilish qiyin qiladi; kerakli ma'lumotni parametr sifatida bering.

```java
// Policy obyekti: qoida alohida, almashtirilishi mumkin
public interface RefundPolicy {
    boolean allows(Order order, Instant now);
}

@Component
class StandardRefundPolicy implements RefundPolicy {
    @Override public boolean allows(Order order, Instant now) {
        return order.status() == OrderStatus.DELIVERED
                && Duration.between(order.deliveredAt(), now).toDays() <= 14;
    }
}
// Qoida o'zgarsa yangi Policy qo'shiladi, servis kodi o'zgarmaydi
```

## 8.21 Strategiyalar registri Map<String, Bean> orqali (Strategy Registry via Map<String, Bean>)

**Tavsif:** Spring bir interface'ning barcha implementatsiyalarini `Map<String, T>` sifatida inject qila oladi, bu yerda kalit - bean nomi. Shu xususiyat tufayli `switch`/`if-else` zanjiri yo'qoladi: kelgan tipga mos strategiya map'dan olinadi. Yangi strategiya qo'shish uchun faqat yangi `@Component` yozish kifoya - mavjud kodni o'zgartirish shart emas (Open/Closed). Bu Spring'dagi eng ko'p ishlatiladigan Strategy pattern ko'rinishi.

**Spring'da qayerda uchraydi:** `ApplicationContext` collection/map injection'ni qo'llab-quvvatlaydi: `Map<String, PaymentProcessor>` (kalit = bean nomi) yoki `List<PaymentProcessor>` (`@Order` bilan tartiblangan). Bean nomini `@Component("CARD")` yoki `@Bean(name = "CARD")` bilan belgilash mumkin; yanada ishonchli yo'l - interface'ga `supports()`/`getType()` metodi qo'shib, `@PostConstruct` ichida `Map`ni `Collectors.toMap`bilan o'zingiz qurish. Shuningdek `ObjectProvider<T>` lazy olish uchun, `@ConditionalOnProperty`/`@Profile` esa faqat kerakli strategiyalarni registratsiya qilish uchun ishlatiladi.

```java
@Service
class PaymentService {
    private final Map<PaymentType, PaymentProcessor> registry;
    PaymentService(List<PaymentProcessor> all) {
        this.registry = all.stream()
            .collect(Collectors.toMap(PaymentProcessor::type, p -> p));
    }
    void pay(PaymentType type, Money amount) {
        var p = registry.get(type);
        if (p == null) throw new UnsupportedPaymentTypeException(type);
        p.process(amount);
    }
}
```

**Qo'llanish keyslari:**
- To'lov usuli (karta, Click, Payme, bank o'tkazmasi) bo'yicha processor tanlash.
- Fayl formatiga qarab parser/exporter tanlash (CSV, XLSX, XML, JSON).
- Notifikatsiya kanali bo'yicha sender tanlash (SMS, email, push, Telegram).
- Hujjat turi bo'yicha validator yoki tax-calculator strategiyasini tanlash.
- Event tipiga qarab mos handler'ni dispatch qilish.

**Ehtiyot bo'ling:** Bean nomini kalit sifatida ishlatish mo'rt - refactoring yoki `@Component` nomini o'zgartirish map kalitini jimgina buzadi, shuning uchun enum yoki interface metodidan olingan kalit afzal. Kalit topilmaganda `null` qaytishini tekshirmaslik `NullPointerException`ga olib keladi; ilova ishga tushganda barcha kutilgan kalitlar borligini tekshirish foydali.

## 8.22 Plugin tanlash @Qualifier orqali (Plugin Selection via @Qualifier)

**Tavsif:** Bir interface'ning bir nechta implementatsiyasi bo'lganda Spring qaysi birini inject qilishni bilmaydi va `NoUniqueBeanDefinitionException` tashlaydi. `@Qualifier` injection nuqtasida aniq bean'ni nomi yoki custom annotatsiya bilan ko'rsatadi, `@Primary` esa default'ni belgilaydi. Bu statik, konfiguratsiya vaqtida hal qilinadigan plugin tanlash: strategiya runtime'da emas, ilova yuklanganda bog'lanadi. Natijada muhit yoki profil bo'yicha boshqa implementatsiyaga o'tish kodga tegmasdan amalga oshadi.

**Spring'da qayerda uchraydi:** `@Qualifier("stripeGateway")`, `@Primary`, hamda `@Qualifier` bilan meta-annotatsiyalangan o'z annotatsiyangiz (`@PaymentProvider(STRIPE)`); Jakarta'ning `@Named`/`@Inject` ham qo'llanadi. Shartli registratsiya uchun - `@Profile("prod")`, `@ConditionalOnProperty`, `@ConditionalOnMissingBean` (Spring Boot auto-configuration'ning asosi) va `@ConditionalOnClass`. Spring Framework 6.2+ `@Fallback` annotatsiyasini qo'shdi - `@Primary`ning teskarisi, ya'ni boshqa nomzod bo'lmasa ishlatiladigan bean. Test'da `@MockitoBean`/`@TestConfiguration` bilan kerakli implementatsiya almashtiriladi.

**Qo'llanish keyslari:**
- `dev` profilda `InMemoryFileStorage`, `prod`da `S3FileStorage` ulanishi.
- Bir nechta `DataSource`/`TransactionManager` bo'lganda to'g'risini inject qilish.
- `application.yml` property'si bo'yicha SMS provayderini tanlash (`@ConditionalOnProperty`).
- Starter kutubxonada default implementatsiya berib, foydalanuvchiga `@ConditionalOnMissingBean` bilan uni almashtirish imkonini qoldirish.
- Legacy va yangi implementatsiyani parallel saqlab, `@Primary`ni ko'chirish orqali migratsiya qilish.

**Ehtiyot bo'ling:** `@Qualifier`ni string nomi bilan ishlatish compile-time xavfsizligini yo'qotadi - custom qualifier annotatsiyasi afzal. `@Primary`ni ko'p joyda ishlatish qaysi bean haqiqatda ulanganini tushunishni qiyinlashtiradi; runtime'da har so'rov uchun boshqa implementatsiya kerak bo'lsa `@Qualifier` emas, Strategy registry kerak.

```java
public interface TaxCalculator { Money tax(Order order); }

@Component("uz") class UzTaxCalculator implements TaxCalculator { /* ... */ }
@Component("kz") class KzTaxCalculator implements TaxCalculator { /* ... */ }

@Service
public class PricingService {
    private final Map<String, TaxCalculator> byCountry;   // Spring nom bo'yicha yig'adi

    public PricingService(Map<String, TaxCalculator> byCountry) {
        this.byCountry = byCountry;
    }

    public Money tax(Order o) {
        TaxCalculator c = byCountry.get(o.countryCode());
        if (c == null) throw new UnsupportedCountryException(o.countryCode());
        return c.tax(o);
    }
}
```

## 8.23 Boy domain modeli vs Anemik (Rich Domain Model vs Anemic)

**Tavsif:** Anemik modelda entity'lar faqat getter/setter'dan iborat ma'lumot sumkasi bo'lib, barcha biznes mantiqi service'larda yashaydi; boy (rich) modelda esa xatti-harakat o'z ma'lumoti bilan birga turadi - `order.cancel()`, `account.withdraw(amount)`. Rich model invariantlarni obyektning o'zi himoya qilishini ta'minlaydi: holat faqat ma'noli metodlar orqali o'zgaradi, setter'lar yopiladi. Service qatlami esa yupqa orkestratorga aylanadi. Anemik model sodda CRUD uchun yetarli, lekin murakkab qoidalar o'sganda mantiq service'lar bo'ylab dublikat bo'lib tarqaydi.

**Spring'da qayerda uchraydi:** JPA entity'lar (`@Entity`) ichiga biznes metodlarini yozish, `protected` no-arg constructor qoldirib, public setter'larni olib tashlash; qiymat obyektlari uchun `@Embeddable` yoki Hibernate 6 `@JavaType`/`AttributeConverter`, Java `record` esa DTO va value object uchun. Lifecycle'da `@PrePersist`/`@PreUpdate`, optimistik lock uchun `@Version`. Domain event'larni entity ichida yig'ish uchun Spring Data'ning `AbstractAggregateRoot<T>` (`registerEvent(...)`) va `@DomainEvents`/`@AfterDomainEventPublication` mexanizmi bor. Spring Modulith aggregate chegaralarini modul darajasida tekshiradi.

**Qo'llanish keyslari:**
- `Order.cancel()` ichida status o'tish qoidalarini (state machine) himoya qilish.
- `Money`, `Email`, `Iban` kabi value object'lar bilan noto'g'ri qiymatni konstruktor darajasida bloklash.
- Hisob balansini faqat `deposit`/`withdraw` orqali o'zgartirib, salbiy balansni imkonsiz qilish.
- Murakkab narx/chegirma hisobini aggregate ichida saqlab, bir nechta service'dagi dublikatni yo'q qilish.
- Oddiy ma'lumotnoma (reference data) jadvallari uchun ataylab anemik CRUD qoldirish.

**Ehtiyot bo'ling:** JPA entity ichiga repository yoki tashqi service inject qilish (`@Configurable`, `@Autowired` field) kuchli bog'liqlik va test qiyinligini keltiradi - kerakli ma'lumotni metod parametri sifatida bering. Rich modelni har joyda majburlash ham xato: oddiy CRUD mikroservisda bu ortiqcha qatlam, va JPA lazy loading bilan domain metodlari kutilmagan DB so'rovlarini keltirib chiqarishi mumkin.

```java
// Anemik: qoida servisda, obyekt faqat ma'lumot tashiydi
class AnemicOrder { private OrderStatus status; /* getter va setter */ }

class AnemicOrderService {
    void cancel(AnemicOrder o) {
        if (o.getStatus() != OrderStatus.NEW) throw new IllegalStateException();
        o.setStatus(OrderStatus.CANCELLED);   // qoida tashqarida, takrorlanadi
    }
}

// Boy model: qoida ma'lumot bilan birga, buzib bo'lmaydi
class Order {
    private OrderStatus status;
    void cancel() {
        if (status != OrderStatus.NEW) throw new OrderNotCancellableException(status);
        this.status = OrderStatus.CANCELLED;
    }
}
```

## 8.24 Aggregate-ga bitta service (Service-per-Aggregate)

**Tavsif:** Service'larni texnik qatlam bo'yicha emas, domain aggregate (consistency chegarasi) bo'yicha bo'lish: `OrderService` faqat `Order` aggregate'ini, `InventoryService` faqat `Inventory`ni boshqaradi. Har bir service o'z aggregate'ining tranzaksion chegarasiga egalik qiladi va boshqa aggregate'ni to'g'ridan-to'g'ri o'zgartirmaydi - faqat o'z service'i yoki event orqali. Bu DDD'ning "bir tranzaksiya - bir aggregate" qoidasini kodda aks ettiradi va kelajakda modulni mikroservisga ajratishni osonlashtiradi. Natijada bog'liqliklar grafigi yo'naltirilgan va tushunarli bo'ladi.

**Spring'da qayerda uchraydi:** Har bir aggregate uchun alohida package (`com.app.order`, `com.app.inventory`), ichida `@Service`, `Repository` (`JpaRepository<Order, OrderId>`) va domain sinflari; tashqariga faqat interface va DTO chiqariladi. Spring Modulith (`@ApplicationModule`, `ApplicationModules.verify()`) modullar orasidagi noto'g'ri bog'liqlikni test paytida aniqlaydi, ArchUnit ham shu maqsadda ishlatiladi. Aggregate'lar orasidagi aloqa `ApplicationEventPublisher` + `@TransactionalEventListener` yoki Spring Modulith'ning event publication registry'si (`spring-modulith-events-jpa`) orqali amalga oshiriladi. Spring Data REST va `@RepositoryRestResource` ham aggregate-markazli modelga mos keladi.

**Qo'llanish keyslari:**
- Modulli monolitda `order`, `payment`, `inventory` modullarini mustaqil service'lar bilan ajratish.
- Keyinchalik mikroservisga ajratiladigan modul chegarasini oldindan belgilash.
- Aggregate'lar orasidagi eventual consistency'ni domain event bilan boshqarish.
- Jamoalar orasida egalik (ownership) chegarasini kod strukturasida aks ettirish.
- Cross-aggregate yozishni taqiqlab, tarqoq tranzaksiya (distributed transaction) ehtiyojini kamaytirish.

**Ehtiyot bo'ling:** Service'lar orasida ikki tomonlama (circular) bog'liqlik paydo bo'lsa, aggregate chegarasi noto'g'ri qo'yilgan - Spring konstruktor injection'da bunday tsiklda ishga tushishdan bosh tortadi. Bitta tranzaksiyada bir nechta aggregate'ni o'zgartirishni odatga aylantirish bu pattern'ning foydasini yo'q qiladi va lock konfliktlarini oshiradi.

```java
// Agregatga bitta servis: chegara aniq, tranzaksiya bitta agregatga tegadi
@Service
public class OrderApplicationService {        // faqat Order agregati
    private final OrderRepository orders;

    @Transactional
    public void cancel(long id, String reason) {
        Order order = orders.findById(id).orElseThrow();
        order.cancel(reason);
        orders.save(order);
    }
}
// Boshqa agregat kerak bo'lsa (Inventory), u o'z servisi orqali va
// ko'pincha hodisa bilan, bir xil tranzaksiyada emas.
```

## 8.25 Orkestrator vs Fasad (Orchestrator vs Facade)

**Tavsif:** Facade bir nechta ichki komponentni sodda, qulay interface ortiga yashiradi - unda biznes qarori yo'q, faqat delegatsiya va qulaylik. Orchestrator esa ketma-ketlikni, shartlarni va muvaffaqiyatsizlik holatida kompensatsiyani boshqaradi - ya'ni process mantiqiga ega. Ularni aralashtirish eng keng tarqalgan arxitektura xatosi: "facade" deb nomlangan sinf asta-sekin biznes qoidalari to'planadigan god object'ga aylanadi. Shuning uchun nomlash va javobgarlikni oldindan ajratish kerak: `OrderFacade` - API uchun qulaylik, `CheckoutOrchestrator` - jarayon egasi.

**Spring'da qayerda uchraydi:** Facade odatda `@Service` yoki `@Component` bo'lib, bir nechta domain service'ni inject qiladi va controller uchun DTO-markazli metodlar beradi (ba'zan "application service" deb ataladi). Orchestrator uchun Spring'da bir nechta vosita bor: oddiy `@Transactional` service metodi (qisqa jarayon), Spring Statemachine (`spring-statemachine-core`), Spring Integration (`IntegrationFlow`, `@ServiceActivator`), Spring Batch (`Job`, `Step`, `JobLauncher`), yoki uzoq davom etuvchi saga uchun Temporal/Camunda integratsiyasi. Tarqoq jarayonlarda `@TransactionalEventListener` + outbox bilan choreography, markazlashgan boshqaruv kerak bo'lsa orchestration tanlanadi.

**Qo'llanish keyslari:**
- `CheckoutOrchestrator`: rezerv → to'lov → yuborish, har bir qadam uchun kompensatsiya bilan.
- `ReportFacade`: controller uchun bir nechta repository va service natijasini bitta DTO'ga yig'ish.
- Spring Batch job'i bilan ko'p qadamli tungi hisob-kitob jarayonini orkestratsiya qilish.
- Legacy tizimga qulay yagona kirish nuqtasi yaratish (facade) uni refactoring qilmasdan.
- Mikroservislar orasidagi sagani Temporal workflow sifatida markazlashgan boshqarish.

**Ehtiyot bo'ling:** Facade ichiga shart va qoida yozilsa, u testlanmaydigan orkestratorga aylanadi - qaroringizni nom bilan mustahkamlab, facade'ni mantiqsiz qoldiring. Orchestrator'ni esa bitta `@Transactional` metod ichida tashqi HTTP chaqiruvlari bilan qurish xavfli: tarmoq xatosi yarim bajarilgan holatni qoldiradi, shuning uchun saga/outbox va idempotentlik kerak.

```java
// Fasad: faqat uzatadi, qaror qabul qilmaydi
@Service
class ReportFacade {
    OrderReport monthly(YearMonth m) { return reportService.monthly(m); }
}

// Orkestrator: tartib, xato va kompensatsiya uchun javobgar
@Service
class CheckoutOrchestrator {
    @Transactional
    public OrderId run(CheckoutCommand cmd) {
        Reservation r = inventory.reserve(cmd.items());
        try {
            Receipt receipt = payments.charge(cmd.payment());
            return orders.create(cmd, receipt, r);
        } catch (PaymentFailedException e) {
            inventory.release(r);                 // kompensatsiya
            throw e;
        }
    }
}
```

## 8.26 Service'dan domain event chiqarish (Domain Event Publishing from Service)

**Tavsif:** Biznes amali yakunlangach, service "nima sodir bo'ldi" faktini event sifatida e'lon qiladi (`OrderPlaced`, `PaymentCaptured`), yon ta'sirlarni esa tinglovchilar bajaradi. Bu service'ni email yuborish, cache tozalash, analitika kabi vazifalardan ajratadi va yangi reaksiya qo'shishni asosiy kodga tegmasdan imkonli qiladi. Eng muhim nuqta - event'ni commit bilan to'g'ri bog'lash: tranzaksiya rollback bo'lsa, event chiqmasligi kerak. Shu sababli `AFTER_COMMIT` fazasi va outbox pattern birgalikda ishlatiladi.

**Spring'da qayerda uchraydi:** `ApplicationEventPublisher.publishEvent(...)` (yoki Spring Framework 6'dan oddiy POJO event'lar, `ApplicationEvent`dan meros shart emas), tinglovchilar `@EventListener` va `@TransactionalEventListener(phase = TransactionPhase.AFTER_COMMIT)`; asinxron ishlash uchun `@Async` + `@EnableAsync` yoki `@EventListener` ustida `ApplicationEventMulticaster` sozlamasi. Spring Data JPA tomonida `AbstractAggregateRoot.registerEvent(...)` va `@DomainEvents`/`@AfterDomainEventPublication` event'ni `save()` vaqtida chiqaradi. Ishonchli yetkazish uchun Spring Modulith `spring-modulith-events-jpa`/`-kafka` event publication registry'sini beradi (nashr etilmagan event'lar jadvalda saqlanib, qayta urinib ko'riladi); Kafka/RabbitMQ'ga chiqarish `KafkaTemplate`/`RabbitTemplate` bilan.

**Qo'llanish keyslari:**
- `OrderPlaced` event'idan keyin tasdiq email va push notifikatsiya yuborish.
- Entity o'zgarganda cache'ni invalidate qilish (`@CacheEvict` tinglovchi ichida).
- Modulli monolitda modullar orasidagi bog'liqlikni event bilan susaytirish.
- Outbox orqali Kafka'ga integratsiya event'larini commit bilan atomar yozish.
- Audit va analitika yozuvlarini asosiy biznes oqimidan ajratish.

**Ehtiyot bo'ling:** Default `@EventListener` sinxron va chaqiruvchi tranzaksiyasida ishlaydi - tinglovchidagi exception butun biznes amalini rollback qilishi mumkin; yon ta'sirlar uchun `AFTER_COMMIT` ishlating, lekin unda DB yozuvi yangi tranzaksiya talab qiladi (`REQUIRES_NEW`). `@Async` event'lar esa jarayon qulaganda yo'qoladi va tartibi kafolatlanmaydi - ishonchlilik kerak bo'lsa Modulith event registry yoki outbox jadvalini qo'shing.

```java
// Hodisa servisdan chiqadi, lekin commit'dan keyin yetkaziladi
@Service
public class OrderService {
    private final ApplicationEventPublisher events;

    @Transactional
    public void place(CreateOrder cmd) {
        Order order = orders.save(Order.from(cmd));
        events.publishEvent(new OrderPlaced(order.id(), order.total()));
    }
}

@Component
class WarehouseNotifier {
    @TransactionalEventListener(phase = TransactionPhase.AFTER_COMMIT)
    void on(OrderPlaced e) { warehouse.send(e); }   // rollback bo'lsa yuborilmaydi
}
```

## 8.27 Amalda qo'llash

- [ ] Servis sinflarining qator sonini o'lchab, 300 qatordan oshganlarini use-case bo'yicha bo'lish nomzodi sifatida belgilang.
- [ ] Faqat getter va setter'dan iborat domen sinflarini toping (anemik model) va ularga tegishli mantiqni ko'chirish rejasini yozing.
- [ ] `@Transactional` qo'yilgan metodlarni sanab chiqing va har birining chegarasi bitta biznes operatsiyaga mos kelishini tasdiqlang.
- [ ] Tranzaksiya ichida tashqi HTTP chaqiruvi yoki xabar yuborish bor joylarni toping - ular tranzaksiyani uzaytiradi va noizchillik yaratadi.
- [ ] Qo'lda yozilgan mapping kodini ro'yxatga olib, MapStruct yoki aniq nomli mapper sinfiga o'tkazish nomzodlarini belgilang.
- [ ] Validatsiya qayerda bajarilayotganini xaritalang: DTO da, servisda yoki domenda. Takrorlanganlarini bitta joyga yig'ing.
- [ ] Bir nechta xatoni yig'ib qaytarishi kerak bo'lgan oqimlarni toping va ularga Notification patternini qo'llang.
- [ ] Har bir servis metodi uchun savolga javob yozing: u nima qaytaradi, xato holatida nima bo'ladi, qayta chaqirilsa xavfsizmi.

---

[&larr; 7. API dizayn patternlari](07-api-dizayn-patternlari.md) · [Mundarija](README.md) · [9. Ma'lumotlarga kirish va ORM patternlari &rarr;](09-malumotlarga-kirish-va-orm-patternlari.md)
