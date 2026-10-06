<!-- doc: patterns | chapter: 24 | part:  -->

[Barcha hujjatlar](../../README.md) / [Dizayn patternlar](README.md)

> Holat: AI yozgan, inson tekshirmagan.

# 24. Zamonaviy Java va funksional patternlar (Modern Java & Functional Patterns)

<details>
<summary>Bu bo'limdagi 41 bo'lim</summary>

- [24.1 Records qiymat obyekti va DTO sifatida (Records as Value Objects / DTOs)](#241-records-qiymat-obyekti-va-dto-sifatida-records-as-value-objects--dtos)
- [24.2 Sealed interfeyslar va pattern matching (Sealed Interfaces + Pattern Matching / Algebraic Data Types)](#242-sealed-interfeyslar-va-pattern-matching-sealed-interfaces--pattern-matching--algebraic-data-types)
- [24.3 Exhaustive switch Visitor o'rnida (Exhaustive Switch as Visitor Replacement)](#243-exhaustive-switch-visitor-ornida-exhaustive-switch-as-visitor-replacement)
- [24.4 Record patternlar (Record Patterns)](#244-record-patternlar-record-patterns)
- [24.5 Optional Maybe monad sifatida (Optional as Maybe Monad)](#245-optional-maybe-monad-sifatida-optional-as-maybe-monad)
- [24.6 Result / Either tipi (Result / Either Type, Vavr Try)](#246-result--either-tipi-result--either-type-vavr-try)
- [24.7 Immutable obyekt va immutable kolleksiyalar (Immutable Object & Immutable Collections)](#247-immutable-obyekt-va-immutable-kolleksiyalar-immutable-object--immutable-collections)
- [24.8 Fluent interfeys va metod zanjiri (Fluent Interface / Method Chaining)](#248-fluent-interfeys-va-metod-zanjiri-fluent-interface--method-chaining)
- [24.9 Statik fabrika metodi (Static Factory Method, Effective Java)](#249-statik-fabrika-metodi-static-factory-method-effective-java)
- [24.10 Enum Singleton (Enum Singleton)](#2410-enum-singleton-enum-singleton)
- [24.11 Strategiya lambdalar va funksional interfeyslar orqali (Strategy via Lambdas / Functional Interfaces)](#2411-strategiya-lambdalar-va-funksional-interfeyslar-orqali-strategy-via-lambdas--functional-interfaces)
- [24.12 Funksiya kompozitsiyasi (Function Composition)](#2412-funksiya-kompozitsiyasi-function-composition)
- [24.13 Currying va qismiy qo'llash (Currying / Partial Application)](#2413-currying-va-qismiy-qollash-currying--partial-application)
- [24.14 Oliy tartibli funksiyalar (Higher-Order Functions)](#2414-oliy-tartibli-funksiyalar-higher-order-functions)
- [24.15 Stream oqimi quvuri (Stream pipeline / Pipes & Filters in Java)](#2415-stream-oqimi-quvuri-stream-pipeline--pipes--filters-in-java)
- [24.16 Yig'uvchi (Collector / accumulator-builder)](#2416-yiguvchi-collector--accumulator-builder)
- [24.17 Stream Gatherer'lari (Stream Gatherers)](#2417-stream-gathererlari-stream-gatherers)
- [24.18 O'rab bajarish / qarz patterni (Execute Around / Loan Pattern)](#2418-orab-bajarish--qarz-patterni-execute-around--loan-pattern)
- [24.19 Tur bo'yicha xavfsiz geterogen konteyner (Type-Safe Heterogeneous Container)](#2419-tur-boyicha-xavfsiz-geterogen-konteyner-type-safe-heterogeneous-container)
- [24.20 Enum asosidagi holat mashinasi va strategiya (Enum-based State Machine / Strategy)](#2420-enum-asosidagi-holat-mashinasi-va-strategiya-enum-based-state-machine--strategy)
- [24.21 Interfeys default metodlari (Interface default methods / Mixin, Trait)](#2421-interfeys-default-metodlari-interface-default-methods--mixin-trait)
- [24.22 Servis provayder interfeysi va ServiceLoader (Service Provider Interface + ServiceLoader)](#2422-servis-provayder-interfeysi-va-serviceloader-service-provider-interface--serviceloader)
- [24.23 Memoizatsiya (Memoization)](#2423-memoizatsiya-memoization)
- [24.24 Kechiktirilgan hisoblash (Lazy evaluation / Supplier)](#2424-kechiktirilgan-hisoblash-lazy-evaluation--supplier)
- [24.25 Null-xavfsizlik (Null-safety / JSpecify, Objects.requireNonNull)](#2425-null-xavfsizlik-null-safety--jspecify-objectsrequirenonnull)
- [24.26 Himoyali nusxalash (Defensive Copying)](#2426-himoyali-nusxalash-defensive-copying)
- [24.27 Mutabilligni minimallashtirish (Minimize Mutability)](#2427-mutabilligni-minimallashtirish-minimize-mutability)
- [24.28 Merosdan ko'ra kompozitsiyani afzal bilish (Favor Composition over Inheritance)](#2428-merosdan-kora-kompozitsiyani-afzal-bilish-favor-composition-over-inheritance)
- [24.29 Abstrakt sinflardan ko'ra interfeyslarni afzal bilish (Prefer Interfaces to Abstract Classes)](#2429-abstrakt-sinflardan-kora-interfeyslarni-afzal-bilish-prefer-interfaces-to-abstract-classes)
- [24.30 Checked va unchecked exception strategiyasi (Checked vs Unchecked Exception Strategy)](#2430-checked-va-unchecked-exception-strategiyasi-checked-vs-unchecked-exception-strategy)
- [24.31 Exception tarjimasi va zanjiri (Exception Translation / Chaining)](#2431-exception-tarjimasi-va-zanjiri-exception-translation--chaining)
- [24.32 Java platforma modullar tizimi (Java Platform Module System - JPMS)](#2432-java-platforma-modullar-tizimi-java-platform-module-system---jpms)
- [24.33 O'qiluvchanlik uchun text block va switch ifodalari (Text Blocks & Switch Expressions for Readability)](#2433-oqiluvchanlik-uchun-text-block-va-switch-ifodalari-text-blocks--switch-expressions-for-readability)
- [24.34 Virtual thread'lar (Virtual Threads)](#2434-virtual-threadlar-virtual-threads)
- [24.35 Strukturalangan concurrency (Structured Concurrency)](#2435-strukturalangan-concurrency-structured-concurrency)
- [24.36 Scoped Values (Scoped Values)](#2436-scoped-values-scoped-values)
- [24.37 Moslashuvchan konstruktor tanalari (Flexible Constructor Bodies)](#2437-moslashuvchan-konstruktor-tanalari-flexible-constructor-bodies)
- [24.38 Nomsiz o'zgaruvchilar va pattern'lar (Unnamed Variables & Patterns)](#2438-nomsiz-ozgaruvchilar-va-patternlar-unnamed-variables--patterns)
- [24.39 Funktor (Functor)](#2439-funktor-functor)
- [24.40 Temir Yo'l Uslubidagi Dasturlash (Railway Oriented Programming)](#2440-temir-yol-uslubidagi-dasturlash-railway-oriented-programming)
- [24.41 Amalda qo'llash](#2441-amalda-qollash)

</details>



Zamonaviy Java (17-25) klassik GoF patternlarining katta qismini til darajasidagi konstruksiyalarga aylantirdi: records, sealed interfaces, pattern matching va lambdalar ko'p holatda butun bir sinf iyerarxiyasini bir necha qatorga siqadi. Funksional patternlar esa holatni (state) o'zgarmas qilib, xatolarni qiymat sifatida uzatib, kodni test qilish va parallellashtirish uchun ancha xavfsiz qiladi. Arxitektor uchun bu muhim, chunki Spring Boot 3.x/4.x ning o'zi ham shu yo'nalishda harakatlanmoqda: configuration properties records sifatida, functional web endpoints, `Function` asosidagi Spring Cloud Function, HTTP interfaces. Qaysi klassik pattern endi keraksiz va qaysi biri hali ham o'z o'rnida qolganini ajrata bilish - bu bugungi Java arxitektorining asosiy mahorati.

## 24.1 Records qiymat obyekti va DTO sifatida (Records as Value Objects / DTOs)

**Tavsif:** Record - bu immutable, nominal tuple: kompilyator konstruktor, accessor metodlar, `equals`, `hashCode` va `toString` ni avtomatik yaratadi. Bu Value Object patternini (identifikator emas, balki qiymat bo'yicha tenglik) deyarli nol boilerplate bilan amalga oshiradi. Compact constructor orqali validatsiya qo'shib, record'ni "har doim to'g'ri holatda" bo'lgan tipga aylantirish mumkin. Natijada DTO, API javob modeli, komanda va event obyektlari uchun Lombok'ga ehtiyoj yo'qoladi.

**Spring'da qayerda uchraydi:** Spring Boot 3.x `@ConfigurationProperties` ni record sifatida to'liq qo'llab-quvvatlaydi (constructor binding avtomatik). Spring MVC/WebFlux `@RequestBody` va `@ResponseBody` uchun Jackson 2.12+ records'ni native deserializatsiya qiladi; `@ModelAttribute` va query parametrlar uchun ham constructor binding ishlaydi. Spring Data JDBC va JPA (Jakarta Persistence) projection interfeyslari o'rniga record'lardan DTO projection sifatida foydalaniladi: `interface UserRepo { List<UserView> findByActive(boolean a); }` yoki JPQL'da `select new com.app.UserView(u.id, u.name)`. Spring Security `Authentication` principal'lari va Spring Modulith domain event'lari ham odatda record bo'ladi.

**Qo'llanish keyslari:**
- REST API request/response DTO'lari - Jackson bilan hech qanday qo'shimcha annotatsiya talab qilinmaydi.
- `@ConfigurationProperties` orqali `application.yml` dan immutable, validatsiya qilingan konfiguratsiya o'qish.
- Domain Value Object'lar: `Money`, `EmailAddress`, `DateRange` - compact constructor ichida invariantlar tekshiriladi.
- Spring Modulith yoki `ApplicationEventPublisher` uchun domain event payload'lari.
- JPQL/Criteria API da read-only projection - butun entity'ni yuklamasdan faqat kerakli maydonlarni olish.

**Ehtiyot bo'ling:** Record'ni JPA `@Entity` sifatida ishlatish mumkin emas - Hibernate no-arg konstruktor va mutable maydonlarni talab qiladi; record faqat projection/DTO uchun. Shuningdek record maydoni mutable obyekt (`List`, massiv) bo'lsa, record faqat "shallow immutable" bo'lib qoladi - accessor'da `List.copyOf()` qaytaring.

## 24.2 Sealed interfeyslar va pattern matching (Sealed Interfaces + Pattern Matching / Algebraic Data Types)

**Tavsif:** `sealed interface` iyerarxiyani yopib, uning barcha implementatsiyalarini kompilyatsiya vaqtida ro'yxatga oladi (`permits`). Bu Java'ga sum type (algebraic data type) olib keladi: "bu qiymat A yoki B yoki C bo'lishi mumkin, boshqasi emas". `switch` pattern matching bilan birga ishlatilganda kompilyator barcha variantlar qoplanganini tekshiradi, yangi variant qo'shilsa kod kompilyatsiya qilinmay qoladi. Natijada noto'g'ri holatlarni umuman ifodalab bo'lmaydigan modellar quriladi.

**Spring'da qayerda uchraydi:** Toza Java 17+ tili konstruksiyasi, Spring Framework 6.x/7.x va Boot 3.x/4.x da service layer domain modellarida keng qo'llaniladi. Amaliyotda: `sealed interface PaymentResult permits Approved, Declined, Pending` - service metodi shuni qaytaradi, `@RestControllerAdvice` yoki controller esa `switch` bilan HTTP status'ga map qiladi. Jackson 2.16+ `@JsonSubTypes` bilan sealed iyerarxiyani polimorf JSON sifatida serializatsiya qiladi. Spring Statemachine yoki oddiy state modellari uchun ham tabiiy vositadir.

**Qo'llanish keyslari:**
- Service natijasini modellashtirish: `Success | ValidationError | NotFound` - exception'larsiz boshqaruv oqimi.
- Domain event yoki command iyerarxiyalari (CQRS/event sourcing) - handler'da exhaustive `switch`.
- State machine holatlari: `Draft | Submitted | Approved | Rejected`, har biri o'ziga xos maydonlar bilan.
- Expression tree / DSL parser tugunlari (query builder, rule engine).
- Tashqi API javoblarini tiplangan variantlarga aylantirish (`OkResponse | RateLimited | ServerError`).

**Ehtiyot bo'ling:** Sealed iyerarxiya variantlari kam va barqaror bo'lganda kuchli; agar variantlar doimiy qo'shilib tursa, har bir `switch` ni qayta yozish kerak bo'ladi - bunda klassik polimorfizm afzal. Shuningdek sealed tiplar bir modulda/paketda bo'lishi talab qilinadi, bu library'ning public API'si uchun kengaytirish erkinligini yopadi.

## 24.3 Exhaustive switch Visitor o'rnida (Exhaustive Switch as Visitor Replacement)

**Tavsif:** Klassik Visitor pattern Java'da ikki marta dispatch (double dispatch) qilish uchun `accept(Visitor)` metodlari va interfeys-per-operatsiya talab qilardi. Sealed tip ustidagi exhaustive `switch` xuddi shu xavfsizlikni beradi: kompilyator barcha variantlar qoplanganini tekshiradi, lekin domain sinflariga hech qanday `accept` metodi qo'shish shart emas. Bu "expression problem" ning operatsiya qo'shish tomonini yengillashtiradi - yangi operatsiya shunchaki yangi metod, domain tiplariga tegmaysiz.

**Spring'da qayerda uchraydi:** Java 21+ (`switch` pattern matching final bo'lgan) til imkoniyati; Spring kodbazalarida odatda `@Service` ichidagi domain logikasi yoki `@RestControllerAdvice` ichidagi xato-mapping uchun ishlatiladi. Spring Framework'ning o'zi hali ham klassik Visitor'dan foydalanadigan joylar bor: `org.springframework.beans.factory.config.BeanDefinitionVisitor` va `org.springframework.jdbc.core.PreparedStatementSetter` ga o'xshash callback'lar - yangi kodda esa ularning o'rniga sealed + switch tanlanadi.

**Qo'llanish keyslari:**
- Domain event'larni handler ichida turga qarab yo'naltirish, `if instanceof` zinapoyasi o'rniga.
- Domain xatolarini HTTP status / ProblemDetail ga map qilish (`ProblemDetail` Spring 6.x).
- AST yoki query DSL ustidan bir necha operatsiya (validate, optimize, render) bajarish.
- Hisob-kitob: tariff yoki chegirma turiga qarab narx formulasini tanlash.
- Tashqi integratsiya javob variantlarini ichki modelga aylantirish (adapter layer).

**Ehtiyot bo'ling:** `default` tarmog'ini qo'shib qo'ysangiz, exhaustiveness tekshiruvi yo'qoladi va yangi variant jimgina e'tiborsiz qoladi - sealed tiplar ustida `default` yozmang. Agar bitta operatsiya ko'p joyda takrorlansa, `switch` ni bitta mapper komponentga ajratmasa, mantiq kodbaza bo'ylab tarqalib ketadi.

## 24.4 Record patternlar (Record Patterns)

**Tavsif:** Record pattern - Java 21 da final bo'lgan deconstruction sintaksisi: `if (obj instanceof Point(int x, int y))` ko'rinishida record maydonlarini bevosita lokal o'zgaruvchilarga ajratib oladi. Pattern'lar ichma-ich (nested) bo'lishi mumkin, shuning uchun murakkab obyekt grafini bir ifodada tekshirib, kerakli ichki qiymatlarni chiqarib olish mumkin. Bu accessor chaqiruvlari va null-tekshiruvlar zanjirini olib tashlaydi hamda sealed tiplar bilan birga to'liq ADT-style kod yozishga imkon beradi.

**Spring'da qayerda uchraydi:** Toza Java 21+ til imkoniyati - Spring Boot 3.2+ / 4.x loyihalarida (baseline Java 17, lekin ko'pchilik 21 LTS da) service va mapper layerlarida ishlatiladi. Tipik joylar: sealed natija tiplarini `switch` ichida dekonstruksiya qilish, Spring `ApplicationEvent` payload'larini ochish, Kafka yoki RabbitMQ'dan kelgan deserializatsiya qilingan record message'larni handler ichida ajratish, hamda `@RestControllerAdvice` ichida xato record'laridan `ProblemDetail` qurish.

**Qo'llanish keyslari:**
- `switch (result) { case Approved(var txId, var amount) -> ... }` - natija variantini va maydonlarini bir vaqtda olish.
- Ichma-ich DTO'lardan chuqur maydonni olish: `case Order(Customer(var id, _), var items)`.
- Message/event handler'larda payload turini aniqlab, darhol maydonlarga bo'lish.
- Guard bilan birga shartli biznes qoidalari: `case Payment(var amt) when amt.compareTo(LIMIT) > 0 -> ...`.
- Konfiguratsiya yoki rule DSL tugunlarini interpretatsiya qilish.

**Ehtiyot bo'ling:** Juda chuqur ichma-ich pattern'lar o'qilishi qiyin bo'lib qoladi va record'ning maydon tartibiga qattiq bog'lanadi - record maydonlari o'rin almashsa, kod jim turib buziladi (tiplar bir xil bo'lsa). Ikki-uch darajadan chuqurroq ketmang va ma'nosiz maydonlar uchun `_` (unnamed pattern) dan foydalaning.

## 24.5 Optional Maybe monad sifatida (Optional as Maybe Monad)

**Tavsif:** `Optional<T>` - "qiymat bor yoki yo'q" ni tipda ifodalovchi konteyner; `map`, `flatMap`, `filter`, `or`, `orElseGet` metodlari bilan monadik zanjir quriladi. Maqsadi - API shartnomasida "natija topilmasligi mumkin" degan ma'lumotni aniq ko'rsatish va `NullPointerException` ni kompilyatsiya vaqtidagi tanlovga aylantirish. To'g'ri ishlatilganda null-tekshiruv zinapoyalari bir oqimli, deklarativ ifodaga aylanadi.

**Spring'da qayerda uchraydi:** Spring Data repository metodlari `Optional<T> findById(ID id)` qaytaradi (`CrudRepository`), hamda derived query'lar ham `Optional` ni qo'llab-quvvatlaydi. `org.springframework.core.env.Environment` ustida `Optional.ofNullable(env.getProperty(...))`; `@Autowired(required=false)` o'rniga `Optional<MyBean>` ni konstruktorga inject qilish mumkin (Spring Framework ichki qo'llab-quvvatlashi). `ObjectProvider#getIfAvailable`, Spring Security `AuditorAware<T>` interfeysi `Optional<T> getCurrentAuditor()` qaytaradi, Spring HATEOAS va `ResponseEntity.of(Optional)` ham shu patternga tayanadi.

**Qo'llanish keyslari:**
- `repository.findById(id).map(mapper::toDto).orElseThrow(NotFoundException::new)` - topilmagan resursni 404 ga aylantirish.
- `ResponseEntity.of(optional)` bilan controller'da 200/404 ni bir qatorda hal qilish.
- Ixtiyoriy bean yoki konfiguratsiya qiymati mavjudligiga qarab xatti-harakatni o'zgartirish.
- Bir nechta ixtiyoriy manbadan birinchi mavjudini olish: `primary().or(this::fallback)`.
- `AuditorAware` orqali hozirgi foydalanuvchi bo'lmasa ham audit maydonlarini xavfsiz to'ldirish.

**Ehtiyot bo'ling:** `Optional` ni maydon, konstruktor parametri yoki JPA entity atributi sifatida ishlatmang - u `Serializable` emas va faqat qaytaruv tipi uchun mo'ljallangan; `Optional<List<T>>` o'rniga bo'sh `List` qaytaring. `optional.get()` ni `isPresent()` tekshiruvisiz chaqirish esa null-check'ni shunchaki boshqa exception'ga aylantiradi, foyda keltirmaydi.

## 24.6 Result / Either tipi (Result / Either Type, Vavr Try)

**Tavsif:** Result (Either) - muvaffaqiyat yoki xatoni bitta qaytaruv qiymatida ifodalovchi tip: `Either<Error, Value>` yoki `Try<Value>`. Maqsadi - kutilgan biznes xatolarini exception sifatida otmaslik, balki tipda ko'rinadigan qiymatga aylantirish; shunda chaqiruvchi xatoni e'tiborsiz qoldira olmaydi. Zanjirli `map`/`flatMap` operatsiyalari xato holatini avtomatik "qisqa tutashtiradi" (short-circuit), shuning uchun try/catch bloklari yo'qoladi va xato oqimi deklarativ bo'ladi.

**Spring'da qayerda uchraydi:** JDK'da tayyor Either yo'q, shuning uchun Java 21+ da sealed interface bilan o'zimiz yozamiz (`sealed interface Result<T> permits Ok, Err`), yoki kutubxona olinadi: Vavr (`io.vavr.control.Either`, `io.vavr.control.Try`) eng mashhuri. Spring tomonida xatolarni HTTP ga map qilish uchun `ProblemDetail` va `ErrorResponse` (Spring Framework 6.x) ishlatiladi; Spring Retry/Resilience4j bilan birga `Try` ni `CircuitBreaker` natijasi sifatida o'rash keng tarqalgan. Reaktiv stack'da esa bu rolni `Mono#onErrorResume` va `Mono<Either<...>>` bajaradi.

**Qo'llanish keyslari:**
- Validatsiya natijalarini yig'ish: bir nechta xatoni exception otmasdan ro'yxat sifatida qaytarish.
- Tashqi HTTP/`RestClient` chaqiruvi natijasini `Try` ga o'rab, retry va fallback mantiqini toza saqlash.
- Biznes qoidasi buzilishini (yetarli balans yo'q) exception emas, kutilgan natija sifatida modellash.
- Batch ishlovida har bir element uchun natija to'plash - bitta xato butun batch'ni to'xtatmasligi uchun.
- Service'dan controller'ga xato sababini (`code`, `message`) tiplangan holda uzatish.

**Ehtiyot bo'ling:** Result va exception'larni bir loyihada aralashtirib yuborish eng katta xato - chegarani aniq belgilang: kutilgan biznes xatolari Result, haqiqiy nosozliklar (DB uzilishi) exception. Yana muhimi: Spring'ning `@Transactional` rollback'i exception'ga asoslanadi, shuning uchun `Result.Err` qaytarilsa tranzaksiya rollback bo'lmaydi - bunday holatda `TransactionAspectSupport` orqali `setRollbackOnly()` chaqirish yoki `rollbackFor` strategiyasini qayta ko'rib chiqish kerak.

## 24.7 Immutable obyekt va immutable kolleksiyalar (Immutable Object & Immutable Collections)

**Tavsif:** Immutable obyekt yaratilgandan keyin holati o'zgarmaydi: barcha maydonlar `final`, setterlar yo'q, mutable ichki qiymatlar nusxalanadi (defensive copy). Bu thread-safety ni bepul beradi, `hashCode` ni keshlashga imkon yaratadi va "obyekt mening ostimdan o'zgarib ketdi" turidagi xatolarni butunlay yo'qotadi. O'zgartirish kerak bo'lsa, yangi nusxa qaytariladi (`withX` yoki builder orqali copy).

**Spring'da qayerda uchraydi:** `List.of`, `Map.of`, `Set.of`, `List.copyOf` (Java 9+) va `Collectors.toUnmodifiableList` - JDK vositalari. Spring Framework'da immutable patternning namunalari ko'p: `org.springframework.http.HttpHeaders#readOnlyHttpHeaders`, `MediaType`, `org.springframework.core.io.ClassPathResource`, `ServerRequest`/`ServerResponse` (WebFlux functional), `RequestEntity` va Spring Security'ning `Authentication` implementatsiyalari (`UsernamePasswordAuthenticationToken` - amalda immutable). Spring Boot'ning `@ConfigurationProperties` constructor binding ham immutable config uchun mo'ljallangan. Guava `ImmutableList` ham keng ishlatiladi.

**Qo'llanish keyslari:**
- Singleton-scoped `@Service`/`@Component` ichida shared konfiguratsiya yoki lookup jadvalini immutable `Map` sifatida saqlash.
- Domain Value Object'lar (`Money`, `Address`) - bir xil qiymat obyektini xavfsiz ulashish.
- Cache (`@Cacheable`) ga qo'yiladigan obyektlar - mutable bo'lsa, bir chaqiruvchi keshdagi qiymatni buzadi.
- Thread pool'lar va `CompletableFuture` oqimlari orasida uzatiladigan payload'lar.
- Event publishing: `ApplicationEventPublisher` orqali tarqatilgan event'ni listener'lar o'zgartirib yubormasligi uchun.

**Ehtiyot bo'ling:** `Collections.unmodifiableList(src)` faqat view qaytaradi - asl `src` o'zgarsa, view ham o'zgaradi; haqiqiy nusxa uchun `List.copyOf()` ishlatiladi. Shuningdek `Map.of`/`List.of` `null` elementni qabul qilmaydi va element tartibini kafolatlamaydi (`Map.of`), bu mavjud kodni ko'chirishda kutilmagan `NullPointerException` ga olib keladi.

## 24.8 Fluent interfeys va metod zanjiri (Fluent Interface / Method Chaining)

**Tavsif:** Fluent interface - har bir metod `this` yoki yangi immutable nusxani qaytarib, chaqiruvlarni zanjir shaklida yozishga imkon beradigan API dizayni. Natijada kod domain-specific tilga (DSL) o'xshab o'qiladi va parametrlar ko'p bo'lgan konfiguratsiyani nomlangan qadamlarga ajratadi. Ko'pincha Builder pattern bilan birga keladi, lekin fluent bo'lish Builder bo'lishni talab qilmaydi.

**Spring'da qayerda uchraydi:** Spring API'lari fluent bilan to'la: `RestClient.builder().baseUrl(...).defaultHeader(...).build()` va `WebClient.builder()` (Spring Framework 6.1+/6.x), `MockMvcRequestBuilders.get("/x").param(...).accept(...)`, `UriComponentsBuilder.fromUriString(...).queryParam(...).build()`, `BodyInserters`, `ServerResponse.ok().contentType(...).body(...)`. Spring Security 6.x lambda DSL: `http.authorizeHttpRequests(a -> a.requestMatchers("/admin/**").hasRole("ADMIN")).csrf(Customizer::withDefaults)`. Spring Data'da `MongoTemplate` `Query.query(where("age").gt(18))` va `JdbcClient.sql("...").param(...).query(...)` (Spring Framework 6.1+). Assertion kutubxonalari (AssertJ) ham shu uslubda.

**Qo'llanish keyslari:**
- HTTP client konfiguratsiyasi: base URL, interceptor'lar, timeout'larni bir zanjirda o'rnatish.
- Test uchun murakkab request yoki test ma'lumot (`test data builder`) qurish.
- Dinamik query qurish: shartlarga qarab filter'lar qo'shib borish.
- Spring Security filter chain va CORS/CSRF konfiguratsiyasini o'qiladigan shaklda yozish.
- Ko'p ixtiyoriy parametrli domain obyektlarini yaratish (telescoping constructor o'rniga).

**Ehtiyot bo'ling:** Mutable fluent builder'ni singleton bean sifatida ulashib bo'lmaydi - `WebClient.Builder` ni bir necha joyda `build()` dan oldin o'zgartirsangiz, konfiguratsiyalar bir-biriga aralashadi; `clone()` yoki har safar yangi builder oling. Shuningdek zanjir juda uzun bo'lsa, stack trace va debug qiyinlashadi, hamda yarim-qurilgan obyektni qaytarish xavfi paydo bo'ladi.

## 24.9 Statik fabrika metodi (Static Factory Method, Effective Java)

**Tavsif:** Konstruktor o'rniga nomlangan `static` metod orqali instansiya yaratish: `of`, `from`, `valueOf`, `getInstance`, `create`. Afzalliklari - metod nomi niyatni tushuntiradi, bir xil signature'li bir nechta fabrika bo'lishi mumkin, nusxa keshlanishi yoki subtype qaytarilishi mumkin, hamda generic tiplar uchun type inference soddalashadi. Bu Effective Java (Item 1) ning birinchi tavsiyasi va zamonaviy JDK API'larining asosiy uslubi.

**Spring'da qayerda uchraydi:** JDK: `List.of`, `Optional.of/empty`, `Duration.ofSeconds`, `Instant.now`. Spring Framework'da: `ResponseEntity.ok()`, `ResponseEntity.status(...)`, `ProblemDetail.forStatus(...)`, `MediaType.valueOf(...)`, `UriComponentsBuilder.fromUriString(...)`, `ServerResponse.ok()`, `PageRequest.of(page, size)` (Spring Data), `BeanUtils.instantiateClass(...)`, `Mono.just` / `Flux.fromIterable` (Reactor). Spring konteyneri uchun esa `@Bean` metodining o'zi statik fabrika rolini bajaradi, hamda XML/programmatic konfiguratsiyada `factory-method` va `FactoryBean<T>` interfeysi mavjud.

**Qo'llanish keyslari:**
- Value Object yaratishda validatsiya qilib, nomlangan konstruktor berish: `Money.ofUsd(10)`, `Email.parse(str)`.
- Bir xil parametr tiplari bilan turli semantikali yaratuvchilar: `Range.ofLength(int)` va `Range.ofEnd(int)`.
- Tez-tez ishlatiladigan nusxalarni keshlash (`Boolean.valueOf`, enum yoki konstanta qaytarish).
- Interfeys qaytarib, konkret implementatsiyani yashirish (strategiyani runtime'da tanlash).
- `@Bean` metodlari orqali tashqi kutubxona obyektlarini Spring konteksiga kiritish.

**Ehtiyot bo'ling:** Statik fabrika Javadoc'da aniq ko'rsatilmasa, foydalanuvchi uni topa olmaydi (konstruktor IDE'da ko'rinadi) - shuning uchun standart nomlanish konvensiyasiga qat'iy rioya qiling. Statik metodlarni mock qilish qiyin, shuning uchun biznes logikasini statik fabrika ichiga joylashtirmang - faqat obyekt yaratish qolsin.

## 24.10 Enum Singleton (Enum Singleton)

**Tavsif:** Yagona elementli `enum` - Java'da singleton yaratishning eng xavfsiz usuli: JVM instansiya yagonaligini kafolatlaydi, serializatsiya va reflection orqali ikkinchi nusxa yaratishdan himoyalangan, hamda thread-safe lazy initialization bepul keladi. Effective Java (Item 3) aynan shu usulni tavsiya qiladi, chunki klassik `double-checked locking` xatolarga moyil. Holatsiz utility'lar va strategiya konstantalari uchun ideal.

**Spring'da qayerda uchraydi:** Spring'da bean'lar sukut bo'yicha singleton scope'da, shuning uchun enum singleton asosan konteynerdan tashqarida ishlatiladi: utility'lar, `Comparator` konstantalari, stateless converter'lar. JDK'da namunalar: `java.util.function.Function#identity` ga o'xshash konstantalar, `java.time.temporal.ChronoUnit` va `ChronoField` - enum bo'lib, xatti-harakatga ega. Spring'da enum'lar ko'p joyda strategiya sifatida uchraydi: `org.springframework.http.HttpMethod` (6.x dan sinf), `HttpStatus`, `RetryPolicy` turlari, Spring Data `Sort.Direction`, `@Scope` konstantalari. `@ConfigurationProperties` ichida enum maydon bo'lsa, Spring Boot `Relaxed Binding` bilan `my.mode=fast` ni avtomatik map qiladi.

**Qo'llanish keyslari:**
- Stateless converter yoki `Comparator` ni yagona nusxa sifatida ekspoz qilish.
- Strategiya konstantalari: `enum TaxRule { VAT { apply(..) }, NONE { apply(..) } }`.
- Konfiguratsiya rejimlari (`mode`, `strategy`) - `@ConfigurationProperties` da tiplangan tanlov.
- `EnumMap`/`EnumSet` asosidagi tez lookup jadvallari (ordinal asosida, `HashMap` dan tezroq).
- Test uchun deterministik null-object yoki no-op implementatsiya.

**Ehtiyot bo'ling:** Enum singleton'ga dependency inject qilish mumkin emas - konstruktor konteyner tomonidan boshqarilmaydi, shuning uchun hamkorlik (collaborator) kerak bo'lgan komponentni enum qilmang, oddiy `@Component` oling. Shuningdek enum ichida mutable `static` holat saqlash butun JVM uchun global o'zgaruvchi yaratadi va testlar orasida sizib o'tadi.

## 24.11 Strategiya lambdalar va funksional interfeyslar orqali (Strategy via Lambdas / Functional Interfaces)

**Tavsif:** Klassik Strategy pattern algoritmni interfeys ortiga yashirib, runtime'da almashtirishga imkon beradi; Java 8+ da bu interfeysning bitta abstrakt metodi bo'lsa, butun implementatsiya lambda yoki metod referensiga aylanadi. Shunday qilib har bir strategiya uchun alohida sinf yozish kerak emas - strategiya shunchaki parametr bo'lib uzatiladigan funksiya. `Function`, `Predicate`, `Consumer`, `Supplier`, `BiFunction`, `UnaryOperator` kabi tayyor interfeyslar aksariyat holatlarni qoplaydi.

**Spring'da qayerda uchraydi:** Spring API'lari ichida lambda-strategiya hamma joyda: `JdbcTemplate.query(sql, rowMapper)` va `RowMapper<T>` (lambda), `TransactionTemplate.execute(status -> ...)`, `RestClient` `.onStatus(predicate, handler)`, `RetryTemplate.execute(ctx -> ...)` (Spring Retry), `CacheManager` uchun `Cache#get(key, Callable)`, Spring Security 6.x lambda DSL va `Customizer<T>` interfeysi, `ApplicationRunner`/`CommandLineRunner`. Spring Cloud Function esa butun endpoint'ni `Function<T,R>` bean sifatida ekspoz qiladi. Shuningdek `List<MyStrategy>` yoki `Map<String, MyStrategy>` ni konstruktorga inject qilib, Spring bean'laridan strategiya registri qurish standart yondashuv.

**Qo'llanish keyslari:**
- `Map<PaymentType, Function<Order, Receipt>>` orqali to'lov usulini tanlash - `if/else` zanjirini yo'qotish.
- `JdbcTemplate`/`JdbcClient` da `RowMapper` ni lambda sifatida inline berish.
- Validatsiya qoidalarini `List<Predicate<Order>>` sifatida konfiguratsiyadan yig'ish.
- Retry yoki circuit-breaker ga bajariladigan operatsiyani `Supplier` sifatida uzatish.
- Test'da fake strategiya berish - mock framework'siz, bitta lambda bilan.

**Ehtiyot bo'ling:** Lambda strategiyasining nomi va stack trace'i ma'nosiz bo'ladi (`lambda$0`), shuning uchun murakkab yoki uzun logikani lambda ichida qoldirmang - nomlangan `@Component` ga chiqaring. Agar strategiya o'z dependency'lariga (repository, client) ehtiyoj sezsa, u Spring bean bo'lishi kerak; lambda ichidan tashqi bean'ni ushlab olish (capture) tranzaksiya va proxy xatti-harakatini chalkashtirib yuborishi mumkin.

## 24.12 Funksiya kompozitsiyasi (Function Composition)

**Tavsif:** Kompozitsiya - kichik, bir vazifali funksiyalarni ulab, kattaroq transformatsiya quvuri (pipeline) qurish: `f.andThen(g)` yoki `f.compose(g)`. Har bir qadam alohida test qilinadi va qayta ishlatiladi, umumiy oqim esa deklarativ ko'rinadi. `Predicate` uchun `and`/`or`/`negate`, `Consumer` uchun `andThen` - shu printsipning turli ko'rinishlari. Natijada "transformation pipeline" arxitekturasi til darajasida ifodalanadi.

**Spring'da qayerda uchraydi:** JDK `Function#andThen`, `Function#compose`, `Predicate#and`, `UnaryOperator#identity`. Spring'da: `Customizer<T>` ni ketma-ket qo'llash, `org.springframework.core.convert.converter.Converter` larni `ConversionService` ichida zanjirlash, Spring Batch `CompositeItemProcessor` va `CompositeItemWriter`, Spring Integration'ning `IntegrationFlow` DSL'i, Spring Data `Specification#and`/`or` (JPA Criteria predikatlarini kompozitsiya qilish), `Sort#and`. Reactor'da `Mono`/`Flux` operator zanjiri va `transform(Function)`, hamda `FilterFunction`/`HandlerFilterFunction` (WebFlux functional endpoints) `andThen` bilan ulanadi. Spring Cloud Function `spring.cloud.function.definition=upper|reverse` orqali bean'larni deklarativ kompozitsiya qiladi.

**Qo'llanish keyslari:**
- ETL/import quvuri: `parse.andThen(normalize).andThen(enrich).andThen(validate)`.
- Spring Data `Specification` larni shartlarga qarab birlashtirib dinamik filter qurish.
- `Predicate` larni `and`/`or` bilan qo'shib, konfiguratsiyadan boshqariladigan qoida to'plami yaratish.
- Spring Batch'da bir nechta `ItemProcessor` ni `CompositeItemProcessor` orqali ketma-ket qo'llash.
- WebFlux functional router'da filter'larni (auth, logging, metrics) zanjirlash.

```java
Function<Order, Order> pipeline =
        Normalizer::normalize;
pipeline = pipeline.andThen(enricher::enrich)
                   .andThen(validator::validate);
Order ready = pipeline.apply(incoming);
```

**Ehtiyot bo'ling:** Uzun kompozitsiya zanjirlarida xato yuz berganda stack trace qaysi qadamda uzilganini ko'rsatmaydi - har bir qadamni nomlangan metod referensi qiling va kritik joylarda logging/`peek` qo'shing. Shuningdek yon ta'sirli (side-effecting) funksiyalarni kompozitsiya qilish tartib bog'liqligini yashiradi va qayta ishlatishni xavfli qiladi.

## 24.13 Currying va qismiy qo'llash (Currying / Partial Application)

**Tavsif:** Currying - ko'p argumentli funksiyani har biri bitta argument qabul qiladigan funksiyalar zanjiriga aylantirish: `Function<A, Function<B, R>>`. Qismiy qo'llash (partial application) esa argumentlarning bir qismini oldindan "muzlatib", qolganini keyin qabul qiladigan yangi funksiya olish. Bu konfiguratsiya yoki kontekst (tenant id, currency, API key) ni funksiyaga oldindan bog'lab, chaqiruv joyini soddalashtiradi va Factory'ning funksional ko'rinishini beradi.

**Spring'da qayerda uchraydi:** Java'da maxsus sintaksis yo'q, lekin `Function<A, Function<B, R>>` va lambda capture bilan amalga oshiriladi; Vavr `io.vavr.Function3#curried` va `apply(a)` orqali partial application beradi. Spring kontekstida tipik ko'rinish - `@Bean` metodidan allaqachon konfiguratsiyalangan funksiya qaytarish: `@Bean Function<String, Receipt> usdCharger(PaymentGateway gw) { return id -> gw.charge(id, Currency.USD); }`. Spring Cloud Function `Function<T,R>` bean'larini endpoint sifatida ekspoz qiladi, shuning uchun partial application konfiguratsiyani endpoint ichiga "pishirish" uchun ishlatiladi. Shuningdek `RetryTemplate`, `TransactionTemplate` va `JdbcClient` callback'lariga kontekst bog'langan lambda uzatish - amalda shu pattern.

**Qo'llanish keyslari:**
- Tenant yoki locale kabi kontekstni oldindan bog'lab, service metodini soddalashtirish.
- `@Bean` orqali konfiguratsiyalangan funksiya qaytarish (base URL, currency, API key bog'langan).
- Test'da bir argumenti fiksirlangan yordamchi funksiyalar yaratib, takrorlanishni kamaytirish.
- Spring Cloud Function'da bitta umumiy logikadan bir nechta konfiguratsiyalangan endpoint hosil qilish.
- Retry/timeout kabi cross-cutting parametrlarni oldindan bog'lab, chaqiruv joyini toza saqlash.

**Ehtiyot bo'ling:** Java'da chuqur currying (`Function<A,Function<B,Function<C,R>>>`) sintaktik jihatdan og'ir va o'qilishi juda qiyin - ikki darajadan oshsa, oddiy obyekt yoki record parametr afzal. Shuningdek lambda ichida mutable kontekstni capture qilish yashirin holat yaratadi va bir nechta thread'da kutilmagan natija beradi.

## 24.14 Oliy tartibli funksiyalar (Higher-Order Functions)

**Tavsif:** Oliy tartibli funksiya - funksiyani argument sifatida qabul qiladigan yoki natija sifatida qaytaradigan funksiya. Java'da bu `java.util.function` paketidagi interfeyslar (`Function`, `BiFunction`, `Supplier`, `Consumer`, `Predicate`, `UnaryOperator`) va lambda/method reference orqali amalga oshiriladi. Bu Strategy va Template Method patternlarining sinfsiz, yengil ko'rinishi: xatti-harakatni sinf ierarxiyasi qurmasdan parametr qilib uzatasiz. `Function.andThen`, `compose` va `Predicate.and/or/negate` kombinatorlari kichik funksiyalardan katta mantiq yig'ishga imkon beradi.

**Spring'da qayerda uchraydi:** `JdbcTemplate.query(String, RowMapper<T>)` va `JdbcClient` RowMapper'ni funksiya sifatida oladi; `TransactionTemplate.execute(TransactionCallback<T>)`; `RestTemplate.execute(..., RequestCallback, ResponseExtractor<T>)`; `WebClient.exchangeToMono(Function<ClientResponse, Mono<T>>)`; `RestClient` va `ClientHttpRequestInterceptor`. Spring Security 6.x/7.x lambda DSL butunlay `Customizer<T>` funksional interfeysiga asoslangan (`http.csrf(csrf -> csrf.disable())`). Spring Cloud Function'da `java.util.function.Function` bean'ning o'zi HTTP endpoint'ga aylanadi (`FunctionCatalog`), Spring Batch'da `ItemProcessor` ham funksional interfeys. Reactor'dagi `map`, `flatMap`, `filter` operatorlari - toza oliy tartibli funksiyalar.

**Qo'llanish keyslari:**
- `JdbcClient.sql(...).query(RowMapper)` bilan ResultSet'ni domain obyektga o'girish, resurs boshqaruvini template'ga qoldirish.
- Spring Security konfiguratsiyasini `Customizer` lambda'lari orqali modulli bo'laklarga ajratish va test profillarida qayta ishlatish.
- Validatsiya qoidalarini `Predicate<Order>` ro'yxati sifatida saqlab, `and`/`negate` bilan dinamik birlashtirish.
- Retry/fallback mantiqini `Supplier<T>` qabul qiladigan generic metodga ko'chirish (Resilience4j `Retry.decorateSupplier`).
- Pricing yoki chegirma strategiyalarini `Map<PromoType, UnaryOperator<BigDecimal>>` ko'rinishida saqlash.

**Ehtiyot bo'ling:** Lambda'lar ichida checked exception tashlab bo'lmaydi, shuning uchun o'z `ThrowingFunction` interfeysingizni yoki Spring'ning `ThrowingFunction` yordamchisini kerak bo'lsa ishlatasiz; aks holda hamma joyda `try/catch` bilan `RuntimeException`ga o'rab, stack trace'ni buzasiz. Juda chuqur funksiya kompozitsiyasi debug qilishni og'irlashtiradi - lambda stack frame'lari anonim bo'ladi, shu sababli murakkab va qayta ishlatiladigan mantiqni nomlangan sinf yoki bean sifatida qoldirish ma'qul.

## 24.15 Stream oqimi quvuri (Stream pipeline / Pipes & Filters in Java)

**Tavsif:** Stream pipeline - ma'lumotni manbadan (source) oraliq operatorlar (`filter`, `map`, `flatMap`, `sorted`) zanjiri orqali o'tkazib, terminal operatsiya (`collect`, `reduce`, `forEach`) bilan yakunlaydigan deklarativ quvur. Bu klassik Pipes & Filters arxitektura patterni'ning til darajasidagi ko'rinishi: har bir operator mustaqil, holatsiz filtr. Oraliq operatorlar lazy - hech narsa terminal operatsiya chaqirilmaguncha hisoblanmaydi, bu esa short-circuit (`findFirst`, `anyMatch`, `limit`) imkonini beradi.

**Spring'da qayerda uchraydi:** Spring Data JPA repository metodi `Stream<T>` qaytarishi mumkin - bunda `@Transactional(readOnly = true)` va try-with-resources shart, aks holda cursor yopilmaydi; `Streamable<T>` esa `Iterable` ustida stream-ga o'xshash API beradi. `org.springframework.util.StreamUtils`, `CollectionUtils` yordamchilari; `Environment` va `BeanFactoryUtils.beanNamesForTypeIncludingAncestors` natijalari odatda stream bilan qayta ishlanadi. Reaktiv dunyoda ekvivalenti - Project Reactor'ning `Flux`/`Mono` operator zanjiri (`spring-webflux`, `R2DBC`), unda backpressure ham bor. Spring Batch `reader → processor → writer` oqimi aynan Pipes & Filters, lekin chunk-oriented va restart qilinadigan ko'rinishda.

**Qo'llanish keyslari:**
- Katta hisobotni `Stream<Entity>` bilan bazadan oqim sifatida o'qib, xotiraga to'liq yuklamasdan CSV'ga yozish.
- DTO mapping va guruhlash: `orders.stream().collect(groupingBy(Order::customerId, summingLong(Order::total)))`.
- Konfiguratsiyadagi vergul bilan ajratilgan qiymatlarni normalizatsiya qilib `Set`ga yig'ish.
- `flatMap` bilan ichki kolleksiyalarni yoyish (masalan, har bir buyurtmaning qatorlari bo'yicha yagona ro'yxat).
- Kirish faylini `Files.lines` bilan satrlab o'qib, filtrlab, batch'larga bo'lib yuborish.

**Ehtiyot bo'ling:** Stream bir martalik - ikkinchi bor terminal operatsiya chaqirsangiz `IllegalStateException`; shuningdek repository'dan kelgan stream'ni yopmaslik connection leak'ga olib keladi. `parallelStream()`ni Spring MVC request thread'ida yoki tranzaksiya ichida ishlatmang: u umumiy `ForkJoinPool.commonPool`da ishlaydi, `ThreadLocal` asosidagi transaction, security context va MDC uzatilmaydi; shunchaki 10-20 elementli ro'yxat uchun esa parallel oqim sof zarar.

## 24.16 Yig'uvchi (Collector / accumulator-builder)

**Tavsif:** `Collector<T, A, R>` - stream elementlarini mutable konteynerga yig'ish strategiyasini to'rt-besh bo'lakka (supplier, accumulator, combiner, finisher, characteristics) ajratadigan abstraksiya. Bu Builder va Reduce patternlarining birlashmasi: yig'ish mantiqi stream'dan ajralib, mustaqil, testlanadigan va kompozitsiya qilinadigan obyektga aylanadi. `Collectors` sinfidagi tayyor yig'uvchilar bir-biriga ulanadi (downstream collector), bu esa SQL'dagi `GROUP BY ... HAVING`ga o'xshash ifodalar yozishga imkon beradi.

**Spring'da qayerda uchraydi:** `Collectors.groupingBy`, `partitioningBy`, `toMap`, `joining`, `flatMapping`, `filtering`, `collectingAndThen`, `teeing` (Java 12+) va `Collector.of(...)` bilan maxsus yig'uvchi; Java 16+ da `Stream.toList()` immutable ro'yxat qaytaradi. Spring'da `Collectors.joining(", ")` konfiguratsiya va log xabarlarini qurishda, `toMap` esa `List<Converter>` yoki `List<MessageHandler>` bean'larini kalit bo'yicha indekslashda keng ishlatiladi (`ObjectProvider.orderedStream().collect(...)`). Spring Data'ning `Streamable` va `Window`/`Slice` natijalarini ham maxsus collector bilan yig'ish mumkin; `MultiValueMap` uchun `LinkedMultiValueMap`ni supplier qilib `Collector.of` yozish odatiy amaliyot.

**Qo'llanish keyslari:**
- Bean'lar ro'yxatini tur bo'yicha registry'ga aylantirish: `handlers.stream().collect(toMap(Handler::type, identity()))`.
- Hisobot uchun ikki o'lchovli guruhlash: `groupingBy(Order::region, groupingBy(Order::status, counting()))`.
- `teeing` bilan bitta o'tishda ham summa, ham o'rtacha yoki min/max hisoblash.
- `collectingAndThen(toList(), Collections::unmodifiableList)` orqali o'zgarmas natija qaytarish.
- `Collector.of` bilan domainga xos agregat (masalan, `MoneyTotal` yoki `HistogramBuilder`) yig'ish.

**Ehtiyot bo'ling:** `Collectors.toMap` takrorlangan kalitda `IllegalStateException` tashlaydi va `null` qiymatni qabul qilmaydi - merge funksiyali variantini ishlatish kerak; `groupingBy` esa `HashMap` qaytarib tartibni yo'qotadi (`LinkedHashMap` supplier bering). O'zingizning collector'ingizda `CONCURRENT` characteristic'ini faqat accumulator haqiqatan thread-safe bo'lsa belgilang, aks holda parallel stream'da ma'lumot buziladi.

## 24.17 Stream Gatherer'lari (Stream Gatherers)

**Tavsif:** `Gatherer` - oraliq operatorlarni o'zingiz yozish imkonini beradigan API: `Collector` terminal operatsiyalarni kengaytirgani kabi, `Gatherer` oraliq qadamni kengaytiradi. U `initializer`, `integrator`, `combiner` va `finisher` bo'laklaridan iborat bo'lib, holatli (stateful), bir elementdan ko'p element chiqaradigan yoki short-circuit qiladigan transformatsiyalarni standart usulda ifodalashga yo'l beradi. Avval sliding window yoki "kalit bo'yicha dedup" kabi amallar uchun qo'lbola kod yozishga majbur bo'lgan joylar endi `stream.gather(...)` bilan yechiladi.

**Spring'da qayerda uchraydi:** Bu sof JDK imkoniyati: JEP 461 (Java 22 preview), JEP 473 (Java 23 ikkinchi preview), JEP 485 bilan Java 24'da yakuniy (final) bo'ldi; Java 25 LTS'da standart API sifatida mavjud. `java.util.stream.Gatherer`, `Stream.gather(Gatherer)` va tayyor `Gatherers.windowFixed`, `Gatherers.windowSliding`, `Gatherers.fold`, `Gatherers.scan`, `Gatherers.mapConcurrent`. Spring Framework 7.x / Spring Boot 4.x Java 17+ ni talab qiladi, shuning uchun Gatherer'lardan faqat runtime Java 24/25 bo'lsa foydalaniladi - asosan servis qatlamidagi batch va oqim qayta ishlashda. `Gatherers.mapConcurrent` virtual thread'lar ustida ishlaydi va tartibni saqlaydi, shu bilan `Flux.flatMap(..., concurrency)`ning imperativ muqobili bo'ladi.

**Qo'llanish keyslari:**
- Bazaga yozishdan oldin elementlarni `windowFixed(500)` bilan batch'larga bo'lish (`JdbcClient` batch update).
- Vaqt seriyasida harakatlanuvchi o'rtachani `windowSliding` bilan hisoblash (metrika, moliyaviy ko'rsatkichlar).
- Kalit bo'yicha takrorlanishni olib tashlash (`distinctBy`) - `Gatherer` holatida ko'rilgan kalitlar to'plamini saqlash.
- Tashqi API'ga parallel, lekin chegaralangan sonli so'rov yuborish: `gather(Gatherers.mapConcurrent(8, this::fetch))`.
- Oqimda to'plangan natijani bosqichma-bosqich ko'rsatish uchun `Gatherers.scan` bilan kumulyativ summa.

```java
List<List<Order>> batches = orders.stream()
        .filter(Order::isPending)
        .gather(Gatherers.windowFixed(500))
        .toList();
batches.forEach(orderRepository::saveAllAndFlush);
```

**Ehtiyot bo'ling:** Java 22/23'da bu API preview bo'lgani uchun `--enable-preview` talab qiladi va binar moslik kafolatlanmaydi - production kodida faqat Java 24+ da ishlatish kerak, aks holda LTS'ga ko'chishda kod sinadi. `mapConcurrent` har element uchun virtual thread yaratadi. API final bo'lgan Java 24 da [JEP 491](https://openjdk.org/jeps/491) ham keldi: `synchronized` blok va `Object.wait()` ichida bloklangan virtual thread endi carrier thread ni pin qilmaydi, shuning uchun `synchronized` ishlatadigan legacy kod (masalan ba'zi eski JDBC driver'lari) Java 24+ da o'z-o'zidan muammo emas. Pin faqat Java 22/23 preview da `synchronized` ichida bloklanganda, Java 24+ da esa native metod yoki Foreign Function chaqiruvi ichida bloklanganda qoladi.

## 24.18 O'rab bajarish / qarz patterni (Execute Around / Loan Pattern)

**Tavsif:** Resursni ochish, ishlatish va qanday yakunlanganidan qat'i nazar yopish mantiqini bitta joyga yig'adigan pattern: chaqiruvchi faqat "o'rtadagi" ishni callback sifatida uzatadi, resurs hayot tsiklini esa framework "qarzga beradi". Java'da bu `AutoCloseable` + try-with-resources sintaksisi va callback qabul qiladigan `execute(...)` metodlari ko'rinishida uchraydi. Natijada resource leak, noto'g'ri yopish tartibi va takrorlangan `finally` bloklari yo'qoladi.

**Spring'da qayerda uchraydi:** Spring'ning butun `*Template` oilasi shu patternga qurilgan: `JdbcTemplate.execute(ConnectionCallback)`, `JdbcClient`, `TransactionTemplate.execute(TransactionCallback)` va `TransactionOperations.executeWithoutResult`, `JmsTemplate.execute(SessionCallback)`, `RedisTemplate.execute(RedisCallback)` yoki `SessionCallback`, `RestTemplate.execute(...)`, `WebClient`ning response yopilishini o'zi boshqarishi. `DataSourceUtils.getConnection/releaseConnection` tranzaksiyaga bog'langan connection'ni to'g'ri qaytaradi. Shu bilan birga `@Transactional` AOP'ning o'zi ham deklarativ Execute Around: proxy begin/commit/rollback'ni o'rab oladi. JDK tomonidan `Files.lines`, `ExecutorService` (Java 19+ `AutoCloseable`) va `StructuredTaskScope` ham try-with-resources bilan ishlatiladi.

**Qo'llanish keyslari:**
- Bir nechta JDBC amalini bitta connection'da bajarish uchun `JdbcTemplate.execute(ConnectionCallback)`.
- Programmatik tranzaksiya kerak bo'lganda (masalan, tsikl ichida kichik tranzaksiyalar) `TransactionTemplate`.
- Fayl/S3 stream'ini try-with-resources bilan o'qib, parsing mantiqini callback'ga berish.
- Maxsus metrika yoki tracing span'ini `withSpan(name, Supplier<T>)` ko'rinishidagi yordamchi metodga o'rash.
- `Lock` yoki distributed lock (Spring Integration `LockRegistry`) olishni `executeWithLock(key, Runnable)` metodida markazlashtirish.

**Ehtiyot bo'ling:** Spring boshqaradigan resursni qo'lda yopmang - `@Transactional` ichida `Connection`ni `close()` qilish yoki `EntityManager`ni yopish tranzaksiyani buzadi; DataSource'dan olingan connection'ni `DataSourceUtils.releaseConnection` orqali qaytaring. try-with-resources'da asosiy exception yopilish xatosini "suppressed" qilib yashiradi, shuning uchun log'da `getSuppressed()`ni ham chiqarishga tayyor bo'ling.

## 24.19 Tur bo'yicha xavfsiz geterogen konteyner (Type-Safe Heterogeneous Container)

**Tavsif:** Oddiy `Map<String, Object>` turdan ajralgan, cast bilan to'la bo'ladi. Bu patternda kalit sifatida qiymatning turi - `Class<T>` (yoki tur bilan parametrlangan maxsus `Key<T>`) ishlatiladi, shuning uchun konteyner har xil turdagi qiymatlarni saqlaydi, lekin olish paytida cast xavfsiz bo'ladi. Odatda `Map<Class<?>, Object>` ichida saqlanib, `type.cast(value)` bilan qaytariladi, bu runtime'da ham tekshiruv beradi.

**Spring'da qayerda uchraydi:** `ApplicationContext.getBean(Class<T>)` va `BeanFactory.getBeanProvider(Class<T>)` - eng ko'p uchraydigan misol; `Environment.getProperty(String, Class<T>)`; `ConversionService.convert(Object, Class<T>)`; `ApplicationContext.getBeansOfType(Class<T>)`. `org.springframework.core.AttributeAccessor` va uning `AttributeAccessorSupport` implementatsiyasi (`BeanDefinition`, `MessageHeaders`) nomli atributlar uchun ishlatiladi. Reactor'ning `Context`/`ContextView` (`contextWrite`, `deferContextual`) kalit-obyekt asosidagi geterogen konteyner bo'lib, reaktiv oqimda tenant yoki trace ma'lumotini uzatadi. Generiklar uchun `ParameterizedTypeReference<T>` (`RestClient`, `WebClient`) va `ResolvableType` to'liq generic turni saqlaydi.

**Qo'llanish keyslari:**
- Plugin registry: `Map<Class<? extends Event>, Handler<?>>` ko'rinishida event handler'larni turga bog'lash.
- Request-scope kontekstida tenant, feature flag va audit ma'lumotini turga xavfsiz saqlash.
- Reactive oqimda `Mono.deferContextual` bilan korrelyatsiya ID'sini `ThreadLocal`siz uzatish.
- Test yordamchisida har xil turdagi mock bean'larni `Class` kalit bilan tutib turish.
- `RestClient` bilan `ParameterizedTypeReference<List<OrderDto>>` qaytarish, ya'ni generic javobni turda yo'qotmaslik.

**Ehtiyot bo'ling:** Type erasure sababli `List<String>.class` mavjud emas - generic turlar uchun `Class<T>` yetarli emas, `ParameterizedTypeReference` yoki `ResolvableType` kerak bo'ladi. Bunday konteynerni global, hamma joydan o'qiladigan "service locator"ga aylantirmang: u dependency'larni yashirib, DI'ni yemiradi va testlarni mo'rt qiladi.

## 24.20 Enum asosidagi holat mashinasi va strategiya (Enum-based State Machine / Strategy)

**Tavsif:** Java enum'lari konstanta emas, to'laqonli obyektlar: ularda maydon, konstruktor, abstract metod va konstantaga xos implementatsiya bo'lishi mumkin. Shuning uchun har bir holat (yoki strategiya) enum konstantasi sifatida ifodalanadi va o'tish qoidalari (`canTransitionTo`) yoxud xatti-harakat (`apply`) shu konstantaning o'zida yashaydi. Bu kompilyatsiya vaqtida to'liqlikni (`switch` ustida exhaustiveness), singleton kafolatini va `EnumMap`/`EnumSet` kabi tez, kam xotira talab qiladigan tuzilmalarni beradi.

**Spring'da qayerda uchraydi:** Sof Java tomonda: abstract metodli enum, `EnumMap`, `EnumSet`, Java 21+ `switch` pattern matching bilan holat o'tishlari. JPA'da holat maydoni `@Enumerated(EnumType.STRING)` bilan saqlanadi, Spring Data konvertorlari esa `Converter<MyState, String>` orqali sozlanadi. Murakkab, ierarxik yoki persistent holat mashinasi kerak bo'lsa Spring Statemachine (`spring-statemachine-core`, `StateMachineBuilder`, `StateMachineFactory`, `@WithStateMachine`, `StateMachinePersister`) ishlatiladi. Framework ichida ham ko'p enum-strategiya bor: `HttpStatus`, `Propagation`, `Isolation`, `RequestMethod`, `CacheMode`; `@ConfigurationProperties` esa `application.yml`dagi matnni enum'ga avtomatik bind qiladi.

**Qo'llanish keyslari:**
- Buyurtma hayot tsikli (`NEW → PAID → SHIPPED → DELIVERED`) o'tishlarini enum ichida tekshirish va noto'g'ri o'tishda exception tashlash.
- To'lov provayderi tanlash: `enum PaymentProvider { STRIPE { Receipt charge(...) } ... }`.
- `EnumMap<Status, Set<Status>>` bilan ruxsat etilgan o'tishlar matritsasini e'lon qilish.
- Hujjat tasdiqlash workflow'ini Spring Statemachine bilan persist qilib, restart'dan keyin davom ettirish.
- Feature strategiyalarini enum sifatida yozib, `@ConfigurationProperties` orqali profil bo'yicha tanlash.

**Ehtiyot bo'ling:** Enum'lar JVM darajasidagi singleton - ularda mutable holat (counter, cache, `EntityManager`) saqlamang, aks holda thread'lar orasida ma'lumot oqib ketadi. `@Enumerated` ni default (`ORDINAL`) qoldirsangiz, kelajakda konstanta tartibini o'zgartirish bazadagi barcha yozuvlarni buzadi; shuningdek o'nlab holat va shartli o'tish paydo bo'lsa, enum ichidagi mantiq o'sib ketadi - bu paytda alohida state machine kutubxonasi tozaroq.

## 24.21 Interfeys default metodlari (Interface default methods / Mixin, Trait)

**Tavsif:** `default` metodlar interfeysga tayyor implementatsiya qo'shib, mavjud implementatsiyalarni sindirmasdan API'ni rivojlantirish (interface evolution) imkonini beradi. Shu bilan birga ular mixin/trait uslubini keltiradi: sinf bir nechta "qobiliyat" interfeysini implement qilib, meros ierarxiyasiga bog'lanmasdan xatti-harakatni yig'adi. `static` metodlar esa interfeysga factory va yordamchi funksiyalarni joylashtiradi (`Comparator.comparing`, `Predicate.not`).

**Spring'da qayerda uchraydi:** Spring 5'dan boshlab ko'p callback interfeyslari `*Adapter` sinflarini default metodlar bilan almashtirdi: `WebMvcConfigurer`, `WebSocketConfigurer`, `HandlerInterceptor`, `SmartLifecycle`, `BeanPostProcessor` (`postProcessBeforeInitialization` default no-op), `Converter`/`GenericConverter`, `ApplicationListener`. Spring Security'da `UserDetails`, `AuthenticationProvider` kabi interfeyslarda ham default'lar bor. Spring Data repository'larida default metod yozib, bir nechta derived query'ni birlashtirish keng tarqalgan amaliyot; `Specification.and/or` va `Streamable` esa default metodli kompozitsiya misoli. JDK tomonda `Function.andThen`, `Iterable.forEach`, `Map.getOrDefault`, `Collection.removeIf`.

**Qo'llanish keyslari:**
- `WebMvcConfigurer`ni faqat kerakli metodini override qilib implement qilish, abstract adapter sinfidan voz kechish.
- Spring Data repository ichida default metod bilan "bir nechta so'rovni birlashtirgan" qulay API berish.
- Audit yoki `toString`/`describe` kabi umumiy xatti-harakatni `Auditable` mixin interfeysida berish.
- Legacy interfeysga yangi metod qo'shganda default implementatsiya bilan orqaga moslikni saqlash.
- `Comparator.comparing(...).thenComparing(...)` bilan tartiblash qoidalarini kompozitsiya qilish.

**Ehtiyot bo'ling:** Ikki interfeysda bir xil signatura'li default metod bo'lsa kompilyator xato beradi - `Iface.super.method()` bilan aniq hal qilish kerak; default metodlarda holat yo'q, shuning uchun ularni "yarim abstract sinf" sifatida suiiste'mol qilish mantiqni tarqoq qiladi. Eng muhimi: Spring Data repository'ning default metodi proxy'dan o'tmaydi, ya'ni undagi `@Transactional`, `@Cacheable`, `@Async` annotatsiyalari ishlamaydi - bu annotatsiyalarni amaliy ta'sir qilishi uchun bean'ning tashqi chaqiriladigan metodiga qo'yish kerak.

## 24.22 Servis provayder interfeysi va ServiceLoader (Service Provider Interface + ServiceLoader)

**Tavsif:** SPI - kutubxona interfeysni (service) e'lon qiladi, uchinchi tomon esa uning implementatsiyasini (provider) alohida JAR'da beradi va runtime classpath orqali topiladi. `java.util.ServiceLoader` `META-INF/services/<to'liq.interfeys.nomi>` faylini (yoki JPMS'da `provides ... with` deklaratsiyasini) o'qib, implementatsiyalarni lazy yuklaydi. Natijada asosiy kod implementatsiyaga compile-time bog'lanmaydi - bu plugin arxitekturasining eng klassik mexanizmi.

**Spring'da qayerda uchraydi:** Spring'ning o'z varianti - `SpringFactoriesLoader` va `META-INF/spring.factories`: `ApplicationContextInitializer`, `ApplicationListener`, `EnvironmentPostProcessor`, `FailureAnalyzer`, `TemplateAvailabilityProvider` shu yerda ro'yxatdan o'tadi. Auto-configuration esa Spring Boot 2.7'dan boshlab `META-INF/spring/org.springframework.boot.autoconfigure.AutoConfiguration.imports` faylida e'lon qilinadi (Boot 3.x/4.x'da faqat shu usul qoldi). Klassik JDK SPI misollari: `java.sql.Driver` (JDBC avtomatik topilishi), SLF4J 2.x provider'lari, Jackson modullari (`ObjectMapper.findAndRegisterModules()`), `jakarta.validation` provider'lari, JPA `PersistenceProvider`.

**Qo'llanish keyslari:**
- O'z starter kutubxonangizda auto-configuration sinfini `AutoConfiguration.imports` orqali e'lon qilish.
- Spring context ko'tarilishidan oldin ishlashi kerak bo'lgan `EnvironmentPostProcessor` bilan maxfiy konfiguratsiyani yuklash (DI hali yo'q, shuning uchun SPI kerak).
- Hisobot formatlari (PDF/XLSX/CSV) uchun plugin JAR'lari qo'shib, asosiy ilovani qayta kompilyatsiya qilmaslik.
- Modulli monolitda har bir modul o'z `DomainEventHandler` provider'ini ro'yxatdan o'tkazishi.
- Mijozga xos biznes qoidalari implementatsiyasini alohida artifact sifatida deploy qilish.

**Ehtiyot bo'ling:** ServiceLoader DI bermaydi - provider'lar no-arg konstruktor bilan yaratiladi, shuning uchun bean'larni ularga qo'lda uzatish kerak (Boot shu sababli `EnvironmentPostProcessor` uchun maxsus konstruktor qoidalarini qo'llaydi). `META-INF/services` fayllari shaded/fat JAR yasashda bir-birini o'chirib tashlashi mumkin (Maven Shade uchun `ServicesResourceTransformer` kerak), GraalVM native image'da esa reflection/SPI ro'yxatga olinmasa provider topilmaydi.

## 24.23 Memoizatsiya (Memoization)

**Tavsif:** [Keshlash patternlari bobidagi memoizatsiya yozuvi](11-keshlash-patternlari.md#1117-memoizatsiya-memoization) bu patternning to'liq yozuvi, bu yerda faqat funksional uslubdagi ko'rinishi: toza `Function<K,V>` ni ichida `Map<K,V>` saqlaydigan dekorator bilan o'rab, natijani `computeIfAbsent` bilan bir marta hisoblash.

**Spring'da qayerda uchraydi:** Qo'lda `ConcurrentHashMap.computeIfAbsent` yoki Caffeine `LoadingCache`, bitta qiymat uchun `org.springframework.data.util.Lazy`, deklarativ darajada `@Cacheable(sync = true)`.

**Qo'llanish keyslari:**
- Toza funksiyani dekorator bilan o'rab, qimmat hisoblashni (regex kompilyatsiyasi, format parsing) argument bo'yicha bir martaga qisqartirish.

**Ehtiyot bo'ling:** Funksiya toza bo'lmasa yoki argument to'plami chegarasiz bo'lsa memoizatsiya bug va xotira oqishi beradi, tafsiloti kanonik yozuvda.

## 24.24 Kechiktirilgan hisoblash (Lazy evaluation / Supplier)

**Tavsif:** Qiymatni e'lon qilish payti emas, haqiqatan kerak bo'lgan payt hisoblash. Java'da bu `Supplier<T>` orqali ifodalanadi: qimmat hisoblash lambda'ga o'raladi va faqat `get()` chaqirilganda bajariladi. Bu startup vaqtini qisqartiradi, kerak bo'lmagan ishni butunlay yo'q qiladi va "faqat xato bo'lganda qurilishi kerak" bo'lgan xabar/obyektlar uchun ideal.

**Spring'da qayerda uchraydi:** `@Lazy` annotatsiyasi (bean'ni birinchi murojaatda yaratish; `spring.main.lazy-initialization=true` bilan global), `ObjectProvider<T>` va `ObjectFactory<T>` (ixtiyoriy yoki prototype bean'ni kerak bo'lganda olish), `org.springframework.data.util.Lazy` (thread-safe bir martalik hisoblash). JDK tomonda `Optional.orElseGet(Supplier)`, `Objects.requireNonNullElseGet`, `Objects.requireNonNull(obj, Supplier<String>)`, `Map.computeIfAbsent`. Reactor'da `Mono.defer`/`Mono.fromSupplier` oqim subscribe qilinmaguncha hech narsa bajarilmasligini ta'minlaydi; `Assert.state(condition, Supplier<String>)` va SLF4J 2.x fluent API (`log.atDebug().log(() -> buildMessage())`) xabarni faqat kerak bo'lganda quradi. JPA'da `FetchType.LAZY` va Hibernate proxy'lari ham shu g'oyaning persistence qatlamidagi ko'rinishi.

**Qo'llanish keyslari:**
- Exception xabarini `orElseThrow(() -> new NotFoundException(id))` bilan faqat xato yuz berganda qurish.
- Startup'ni tezlashtirish uchun kamdan-kam ishlatiladigan integratsiya client'ini `@Lazy` qilish.
- Ixtiyoriy bean'ni `ObjectProvider.getIfAvailable(() -> defaultImpl)` orqali olish.
- Og'ir debug log xabarini `Supplier` bilan o'rab, production'da hisoblamaslik.
- `Mono.defer` bilan har subscribe'da yangi so'rov yuborilishini (retry uchun) kafolatlash.

**Ehtiyot bo'ling:** `@Lazy` va global lazy initialization konfiguratsiya xatolarini startup'dan runtime'ga suradi - ilova "ko'tarildi" deb ko'rinadi, lekin birinchi request'da yiqiladi; shuning uchun uni ehtiyotkorlik bilan va yaxshi health check bilan ishlatish kerak. O'z qo'lbola lazy holder'ingizda double-checked locking'ni to'g'ri (`volatile` bilan) yozish oson emas - `Lazy.of(...)` yoki `Suppliers.memoize` tipidagi tayyor yechimni afzal ko'ring.

## 24.25 Null-xavfsizlik (Null-safety / JSpecify, Objects.requireNonNull)

**Tavsif:** `NullPointerException`ni runtime'dan kompilyatsiya/analiz vaqtiga ko'chirish strategiyasi: API shartnomasida qaysi qiymat `null` bo'lishi mumkinligini annotatsiyalar bilan e'lon qilish va chegaralarda (konstruktor, public metod) tezda "fail fast" tekshirish. Deklarativ qism statik analizatorlar va Kotlin/IDE uchun mo'ljallangan, imperativ qism esa `Objects.requireNonNull` yoki `Assert` bilan noto'g'ri holatni darhol to'xtatadi.

**Spring'da qayerda uchraydi:** Spring Framework 5.x/6.x'da `org.springframework.lang.Nullable`, `@NonNull`, `@NonNullApi`, `@NonNullFields` paket darajasidagi annotatsiyalari ishlatilgan; Spring Framework 7.0 esa butun kod bazasini JSpecify'ga ko'chirdi - `org.jspecify.annotations.Nullable`, `@NonNull`, `@NullMarked`, `@NullUnmarked` (eski `org.springframework.lang` annotatsiyalari deprecated). Imperativ tekshiruvlar: `java.util.Objects.requireNonNull`, `requireNonNullElse`, `org.springframework.util.Assert.notNull/hasText/state`, `Optional` (qaytuvchi qiymat uchun). Validatsiya chegarasida `jakarta.validation.constraints.NotNull` + `@Valid`/`@Validated`. Statik analiz uchun NullAway (Error Prone) yoki IDE inspection'lari JSpecify annotatsiyalarini o'qiydi; Kotlin kompilyatori esa Spring API'ning nullability'sini to'g'ridan-to'g'ri ishlatadi.

**Qo'llanish keyslari:**
- Public API va SDK'da `@NullMarked` paket deklaratsiyasi bilan "default: non-null" shartnomasini e'lon qilish.
- Immutable domain obyekti konstruktorida `this.id = Objects.requireNonNull(id, "id")` bilan invariantni kafolatlash.
- Kotlin'dan chaqiriladigan Java kutubxonasida platform type'larni yo'qotib, `String?`/`String` aniqligini berish.
- Repository metodlarida "topilmasligi mumkin" holatni `Optional<T>` bilan ifodalash.
- CI'da NullAway'ni yoqib, yangi `null` oqishlarini build vaqtida bloklash.

**Ehtiyot bo'ling:** Annotatsiyalar runtime tekshiruv emas - ular faqat analizator/kompilyatorga ishora, shuning uchun tashqi (deserializatsiya, JDBC, reflection) ma'lumot chegarasida imperativ tekshiruv ham kerak. `Optional`ni maydon, konstruktor parametri yoki entity atributi sifatida ishlatmang (Serializable emas va ortiqcha allocation beradi) - u asosan qaytuvchi qiymat uchun; `@NotNull` esa Bean Validation annotatsiyasi bo'lib, JSpecify `@NonNull` bilan bir xil vazifani bajarmaydi.

## 24.26 Himoyali nusxalash (Defensive Copying)

**Tavsif:** Tashqaridan kelgan mutable obyektni (kolleksiya, massiv, `Date`) ichki holatga to'g'ridan-to'g'ri saqlamaslik va ichki holatni tashqariga to'g'ridan-to'g'ri qaytarmaslik: konstruktorda kiruvchi qiymat nusxalanadi, getter esa o'zgarmas ko'rinish yoki nusxa qaytaradi. Bu immutability va invariantlarni saqlashning asosiy shartidir - aks holda chaqiruvchi obyekt ichidagi holatni bilmasdan buzib qo'yadi. Nusxa olish uchun `List.copyOf`, `Map.copyOf`, `Set.copyOf`, `Arrays.copyOf` yoki `Collections.unmodifiableList` ishlatiladi.

**Spring'da qayerda uchraydi:** `List.copyOf`/`Map.copyOf` (Java 10+) va `Stream.toList()` (Java 16+) immutable natija beradi; record'lar maydonlarni avtomatik nusxalamaydi, shuning uchun canonical konstruktorni qo'lda yozish kerak. Spring tomonda `HttpHeaders.readOnlyHttpHeaders(...)`, `Collections.unmodifiableMap` ishlatilgan `MessageHeaders`, `ServletRequestAttributes` snapshot'lari; `@ConfigurationProperties` constructor binding bilan immutable konfiguratsiya record'lari yaratish tavsiya etiladi (`@ConstructorBinding` Boot 3.x'da bitta konstruktor bo'lsa shart emas). JPA entity'larida esa `@OneToMany` kolleksiyasini `List.copyOf` bilan almashtirish Hibernate'ning dirty checking'ini buzadi - bu yerda himoyali nusxa getter darajasida (`Collections.unmodifiableList(items)`) beriladi.

**Qo'llanish keyslari:**
- Value object / DTO record'ida kolleksiya maydonini `List.copyOf(items)` bilan muzlatish.
- `@ConfigurationProperties` record'lari orqali o'zgarmas, thread-safe konfiguratsiya olish.
- Cache'dan qaytarilgan obyektni nusxalab berish, chaqiruvchi keshdagi nusxani o'zgartirmasligi uchun.
- JPA entity getter'ida ichki kolleksiyani `unmodifiableList` qilib qaytarish va `addItem()` metodi bilan boshqarish.
- Massiv qabul qiladigan public API'da `Arrays.copyOf` bilan kiruvchi massivni izolyatsiya qilish.

**Ehtiyot bo'ling:** `List.copyOf` sayoz (shallow) nusxa - ichidagi elementlar mutable bo'lsa, immutability illyuziyaga aylanadi; shuningdek `null` elementga ruxsat bermaydi va `NullPointerException` tashlaydi. Juda katta kolleksiyalarni har getter chaqiruvida nusxalash sezilarli GC yuki beradi, Hibernate boshqaradigan kolleksiyani almashtirish esa `orphanRemoval` va lazy loading'ni sindiradi - bunday joylarda nusxa o'rniga faqat o'qiladigan ko'rinish (unmodifiable view) qaytarish to'g'riroq.

## 24.27 Mutabilligni minimallashtirish (Minimize Mutability)

**Tavsif:** Obyekt holatini yaratilgandan keyin o'zgartirib bo'lmaydigan qilib loyihalash - barcha maydonlar `final`, setter'lar yo'q, defensive copy orqali tashqi havolalar izolyatsiya qilinadi. Bu thread-safety muammolarini butunlay yo'q qiladi, chunki o'zgarmas obyektni sinxronizatsiyasiz bir nechta thread o'qishi mumkin. Shuningdek `equals`/`hashCode` kontrakti barqaror bo'ladi, shu sababli obyektni `HashMap` kaliti yoki `Set` elementi sifatida xavfsiz ishlatish mumkin. Java 16+ dagi `record` bu patternni til darajasida rasmiylashtirgan.

**Spring'da qayerda uchraydi:** `java.lang.String`, `java.time.*` (`LocalDate`, `Instant`, `Duration`), `List.of()`/`Map.of()` immutable kolleksiyalari. Spring'da `@ConfigurationProperties` konstruktor binding bilan (`@ConstructorBinding` Boot 3.x da immutable record uchun standart), `HttpHeaders.readOnlyHttpHeaders()`, `MessageHeaders`, `ServerRequest`/`ServerResponse` (WebFlux funksional model), `Collections.unmodifiableList()` va Spring Security'dagi `Authentication` implementatsiyalari (`UsernamePasswordAuthenticationToken` autentifikatsiyadan keyin). DTO va event payload'lar uchun `record` - Spring Boot 3.x/4.x da JSON deserializatsiya (Jackson 2.12+) record'ni to'liq qo'llab-quvvatlaydi.

**Qo'llanish keyslari:**
- REST API request/response DTO'larini `record` sifatida yozib, qatlamlar orasida tasodifiy mutatsiyani oldini olish.
- `@ConfigurationProperties` konfiguratsiya obyektlarini immutable qilib, runtime'da sozlamalarning o'zgarmasligini kafolatlash.
- Domain'dagi Value Object'lar (`Money`, `EmailAddress`, `DateRange`) uchun immutable record ishlatish.
- `ApplicationEvent` payload'larini immutable qilib, bir nechta listener'ga bir xil ma'lumot borishini ta'minlash.
- Cache'ga (`@Cacheable`) qaytariladigan obyektlarni immutable qilib, cache ichidagi qiymatni chaqiruvchi buzmasligini kafolatlash.

**Ehtiyot bo'ling:** `final` maydon faqat havolani muzlatadi - agar u mutable `List` yoki `Date` ga ishora qilsa, obyekt haqiqatda immutable emas, shu sababli konstruktorda ham, getter'da ham defensive copy kerak (record'da `List.copyOf()` ni compact constructor ichida qilish). Juda ko'p maydonli immutable obyektni har safar to'liq qayta qurish GC bosimini oshiradi, shuning uchun katta, tez-tez o'zgaruvchi buffer'lar uchun mutable struktura to'g'riroq.

## 24.28 Merosdan ko'ra kompozitsiyani afzal bilish (Favor Composition over Inheritance)

**Tavsif:** Funksionallikni superclass'dan meros olish o'rniga, kerakli obyektni maydon sifatida saqlab, unga delegatsiya qilish. Meros subclass'ni superclass'ning implementatsiya detallariga bog'laydi - superclass'dagi o'zgarish subclass'ni jimgina buzishi mumkin (fragile base class muammosi). Kompozitsiya esa faqat public shartnomaga tayanadi va runtime'da xatti-harakatni almashtirishga imkon beradi. Delegatsiya + interface kombinatsiyasi Decorator va Strategy patternlarining asosidir.

**Spring'da qayerda uchraydi:** Spring'ning o'zi kompozitsiyaga asoslangan: `JdbcTemplate` `DataSource` ni meros olmaydi, balki inject qiladi; `RestClient`/`WebClient` ichida `ClientHttpRequestFactory` va `ExchangeFunction` saqlanadi. `DelegatingFilterProxy`, `DelegatingPasswordEncoder` (Spring Security), `HandlerMethodArgumentResolverComposite`, `CompositeHealthContributor` (Boot Actuator), `TransactionAwareDataSourceProxy` - barchasi delegatsiya. Konstruktor injection (`@Autowired` konstruktor orqali) kompozitsiyaning asosiy mexanizmi; `@Service` sinflarini bir-biridan meros qilish o'rniga bir-biriga inject qilish idiomatik yo'l.

**Qo'llanish keyslari:**
- `AbstractBaseService` ierarxiyasi o'rniga umumiy logikani alohida bean sifatida ajratib, kerakli servislarga inject qilish.
- Repository'ga retry, audit yoki metrik qo'shish uchun `Repository` interfeysini implement qilgan wrapper (decorator) yozish.
- `CompositeHealthIndicator` uslubida bir nechta tekshiruvni bitta komponentga yig'ish.
- Validatsiya qoidalarini `Validator` bean'lar to'plami sifatida inject qilib, qoida qo'shilganda mavjud kodni o'zgartirmaslik.
- Test'da real bog'liqlikni mock bilan almashtirish - kompozitsiya buni osonlashtiradi, meros esa qiyinlashtiradi.

**Ehtiyot bo'ling:** Kompozitsiya ko'proq boilerplate (delegatsiya metodlari) talab qiladi, shuning uchun haqiqiy "is-a" munosabati bo'lgan va superclass meros uchun maxsus loyihalangan hollarda (masalan `RuntimeException` dan meros) merosni ishlatish to'g'ri. Spring'da `@Transactional` yoki `@Cacheable` metodni o'z sinfi ichidan chaqirsangiz, proxy chetlab o'tiladi - self-injection yoki haqiqiy delegatsiya kerak bo'ladi.

## 24.29 Abstrakt sinflardan ko'ra interfeyslarni afzal bilish (Prefer Interfaces to Abstract Classes)

**Tavsif:** Tipni interface bilan e'lon qilish sinfga bir nechta tipni birdan implement qilish imkonini beradi va yagona meros cheklovidan xalos qiladi. Interface mavjud ierarxiyaga retroaktiv qo'shilishi mumkin, abstrakt sinf esa yo'q. Java 8+ `default` metodlari interfeyslarga evolutsiya qobiliyatini berdi, Java 17 `sealed interface` esa implementatsiyalar to'plamini nazorat qilish va pattern matching'da to'liq (exhaustive) `switch` yozish imkonini beradi. Natijada "interface + skeletal implementation" (masalan `AbstractXxx`) juftligi eng moslashuvchan dizayn bo'lib qoladi.

**Spring'da qayerda uchraydi:** `BeanFactory`/`ApplicationContext`, `Environment`, `Resource`, `ApplicationEventPublisher` - hammasi interface; skeletal implementatsiyalar `AbstractApplicationContext`, `AbstractAutowireCapableBeanFactory` ko'rinishida beriladi. Spring Data'da `CrudRepository`/`JpaRepository` interfeysini e'lon qilasiz, implementatsiyani framework generatsiya qiladi. `HandlerInterceptor`, `WebMvcConfigurer`, `Converter<S,T>`, `Filter` - `default` metodli interfeyslar, shu sababli faqat kerakli metodni override qilasiz. Spring Framework 6.x da `@FunctionalInterface` va `sealed` tiplar keng ishlatiladi; `ProblemDetail` bilan ishlovchi `ErrorResponse` ham interface.

**Qo'llanish keyslari:**
- Servis qatlamini interface bilan e'lon qilib, bir nechta implementatsiya (`StripePaymentGateway`, `MockPaymentGateway`) ni profil bo'yicha almashtirish.
- Spring Data repository'lari uchun faqat interface yozib, custom fragment interfeysini qo'shish.
- `sealed interface` + `record` bilan domain natijalarini (`Success`, `Validation Failure`, `Retryable Error`) modellab, `switch` da to'liq qamrovni compiler'ga tekshirtirish.
- Mavjud legacy sinfga yangi qobiliyat qo'shish uchun interface'ni retroaktiv implement qilish.
- `default` metod orqali interfeysga yangi metod qo'shib, barcha implementatsiyalarni buzmaslik.

**Ehtiyot bo'ling:** Faqat bitta implementatsiyasi bo'lgan va hech qachon almashtirilmaydigan sinf uchun interface yozish ortiqcha abstraksiya - Spring Boot 3.x da proxy uchun ham interface shart emas (CGLIB ishlaydi). `default` metodga holat (field) joylash imkoni yo'q, shuning uchun umumiy holat va konstruktor logikasi kerak bo'lsa abstrakt sinf yoki alohida komponent to'g'riroq.

## 24.30 Checked va unchecked exception strategiyasi (Checked vs Unchecked Exception Strategy)

**Tavsif:** Checked exception chaqiruvchini xatoni e'tiborga olishga majburlaydi va tiklanishi mumkin bo'lgan holatlar uchun mo'ljallangan; unchecked (`RuntimeException`) esa programming error yoki tiklanmaydigan holat uchun. Amaliyotda checked exception API ni ifloslantiradi, qatlamlar bo'ylab `throws` zanjirini tarqatadi va lambda/stream ichida ishlamaydi, shu sababli zamonaviy Java/Spring kodi asosan unchecked'ga tayanadi. To'g'ri strategiya: chaqiruvchi haqiqatan ham ma'noli tiklash harakati qilishi mumkin bo'lsa checked, aks holda unchecked.

**Spring'da qayerda uchraydi:** Spring ataylab barcha infratuzilma xatolarini unchecked qiladi: `DataAccessException` ierarxiyasi (`SQLException` ni almashtiradi), `TransactionException`, `RestClientException`/`WebClientResponseException`, `BeansException`, Spring Framework 6.x dagi `HttpStatusCodeException`. `@Transactional` standart holatda faqat `RuntimeException` va `Error` da rollback qiladi - checked exception'da rollback uchun `rollbackFor` kerak. Spring MVC'da `@ExceptionHandler` va `ResponseEntityExceptionHandler` unchecked exception'larni `ProblemDetail` (RFC 9457) ga o'giradi; `@ResponseStatus` bilan domain exception'ni HTTP statusga biriktirish mumkin.

**Qo'llanish keyslari:**
- Validatsiya va business qoidalari buzilishi uchun unchecked `DomainException` ierarxiyasini yaratib, `@RestControllerAdvice` da markazlashgan tarzda ishlash.
- `@Transactional(rollbackFor = Exception.class)` ni checked exception tashlaydigan metodlarda ataylab qo'yish.
- Tashqi integratsiya xatolarini unchecked `IntegrationException` ga o'rab, servis qatlamini `IOException` dan tozalash.
- Lambda/stream ichida ishlaydigan kod uchun checked exception'ni unchecked'ga o'raydigan `uncheck()` yordamchisini qo'llash.
- Chaqiruvchi retry yoki fallback qila oladigan kam sonli holatlar (masalan optimistic lock konflikti) uchun checked exception qoldirish.

**Ehtiyot bo'ling:** Unchecked exception'ga to'liq o'tish xatolarni "ko'rinmas" qiladi - har bir chegarada (controller advice, message listener, scheduled task) global handler bo'lishi shart, aks holda xato jimgina yo'qoladi. `@Transactional` ning checked exception'da rollback qilmasligi eng ko'p uchraydigan ma'lumot buzilishi sababi; shuningdek `catch (Exception e)` bilan hammasini yutib yuborish `InterruptedException` va virtual thread cancellation signalini ham o'chiradi.

## 24.31 Exception tarjimasi va zanjiri (Exception Translation / Chaining)

**Tavsif:** Quyi qatlamning exception'ini joriy abstraksiyaga mos yuqori darajadagi exception'ga o'girib, originalni `cause` sifatida saqlash. Bu chaqiruvchini implementatsiya detallaridan (JDBC, JPA, HTTP kutubxonasi) izolyatsiya qiladi, ammo diagnostika uchun to'liq stack trace zanjiri saqlanib qoladi. Agar quyi exception yuqori qatlam uchun ma'nosiz bo'lsa - tarjima qiling; agar foydali bo'lsa - zanjirlab yuqoriga uzatish kifoya.

**Spring'da qayerda uchraydi:** Spring'ning klassik namunasi - `SQLExceptionTranslator` / `SQLErrorCodeSQLExceptionTranslator` vendor xatolarini `DataIntegrityViolationException`, `DuplicateKeyException`, `CannotAcquireLockException` ga o'giradi. `@Repository` annotatsiyasi `PersistenceExceptionTranslationPostProcessor` orqali JPA `PersistenceException` ni `DataAccessException` ga tarjima qiladi. `JdbcTemplate`, `JpaTransactionManager`, `RestClient` (Boot 3.2+) ham shu yondashuvni qo'llaydi; `NestedRuntimeException.getMostSpecificCause()` zanjirning tubini topish uchun ishlatiladi. Spring Boot 3.x da controller qatlamida `ErrorResponseException` / `ProblemDetail` ga tarjima qilish standart.

**Qo'llanish keyslari:**
- Repository'dagi `DuplicateKeyException` ni domain'ning `EmailAlreadyRegisteredException` ga o'girib, controller'ga 409 qaytarish.
- Tashqi API'ning `WebClientResponseException` ni `PaymentProviderUnavailableException` ga tarjima qilib, retry/circuit breaker qarorini soddalashtirish.
- JPA/Hibernate detallarini servis qatlamidan yashirish uchun `@Repository` tarjimasidan foydalanish.
- `getMostSpecificCause()` bilan log'da haqiqiy SQL xatosini chiqarish, foydalanuvchiga esa umumiy xabar berish.
- Legacy kutubxonaning checked exception'ini unchecked domain exception'ga o'rash.

**Ehtiyot bo'ling:** `cause` ni uzatmaslik (`throw new MyException(msg)` - originalsiz) diagnostikani deyarli imkonsiz qiladi, shuning uchun har doim `new MyException(msg, e)` yozing. Har bir qatlamda ketma-ket qayta o'rash stack trace'ni o'nlab "caused by" bloklariga aylantiradi va foydali signalni ko'mib tashlaydi - tarjimani faqat haqiqiy abstraksiya chegaralarida qiling.

## 24.32 Java platforma modullar tizimi (Java Platform Module System - JPMS)

**Tavsif:** Java 9 da kiritilgan modullar tizimi `module-info.java` orqali paketlarning qaysi biri eksport qilinishi va qaysi modullarga bog'liqlik borligini compile va runtime darajasida majburlaydi. Bu "public lekin ichki" muammosini hal qiladi: eksport qilinmagan paketdagi public sinfga tashqaridan murojaat qilinmaydi. Natijada haqiqiy enkapsulyatsiya, aniq bog'liqlik grafi va `jlink` bilan minimal runtime image olish imkoniyati paydo bo'ladi.

**Spring'da qayerda uchraydi:** Spring Framework 6.x va Spring Boot 3.x jar'lari `Automatic-Module-Name` (masalan `spring.core`, `spring.beans`, `spring.web`) bilan keladi, lekin to'liq named module emas - shu sababli Spring ilovalari odatda classpath'da yoki automatic module sifatida ishlaydi. JDK modullari (`java.base`, `java.sql`, `java.net.http`, `jdk.httpserver`) to'liq modullashgan. Reflection'ga tayangan Spring uchun `opens` direktivasi zarur: `opens com.example.domain to spring.core;`. Amalda ko'pchilik Boot loyihalari JPMS o'rniga fat jar + `spring-boot-maven-plugin` ni, native image uchun esa GraalVM va `RuntimeHints`/`@RegisterReflectionForBinding` ni ishlatadi.

**Qo'llanish keyslari:**
- Kutubxona (SDK) nashr etayotganda `exports` bilan faqat public API ni ochib, `internal` paketlarni muhrlab qo'yish.
- Monolit ichida modullar orasidagi tasodifiy bog'liqliklarni compile vaqtida to'xtatish.
- `jlink` bilan faqat kerakli JDK modullaridan iborat kichik runtime image qurib, konteyner hajmini kamaytirish.
- `jdeps` bilan legacy loyihadagi yashirin JDK-internal API ishlatilishini aniqlash.
- CLI yoki desktop vositalari uchun o'zini-o'zi ta'minlovchi (self-contained) runtime tarqatish.

**Ehtiyot bo'ling:** Spring, Hibernate va Jackson reflection'ga kuchli tayanadi, shuning uchun `opens` ni to'g'ri sozlamaslik `InaccessibleObjectException` ga olib keladi; split package'lar esa modullashgan qurilishni butunlay to'xtatadi. Oddiy Spring Boot web ilovasi uchun JPMS ko'pincha foyda bermaydi - modulyar monolit chegaralari uchun Spring Modulith (`spring-modulith` 1.x) yoki ArchUnit amaliyroq tanlov.

## 24.33 O'qiluvchanlik uchun text block va switch ifodalari (Text Blocks & Switch Expressions for Readability)

**Tavsif:** Text block (`"""`, Java 15+) ko'p qatorli matnni escape va konkatenatsiyasiz, haqiqiy shaklini saqlab yozishga imkon beradi - indentatsiya avtomatik tozalanadi. Switch expression (Java 14+) esa `switch` ni qiymat qaytaruvchi ifodaga aylantiradi: `->` shoxlari fall-through'ni yo'q qiladi, `yield` blok natijasini beradi, enum va sealed tiplar uchun compiler to'liq qamrovni tekshiradi. Ikkisi birgalikda SQL/JSON generatsiyasi va holat mapping kodini ancha qisqartiradi.

**Spring'da qayerda uchraydi:** `JdbcTemplate`/`JdbcClient` (Spring Framework 6.1+) va `@Query` ichidagi SQL/JPQL'ni text block bilan yozish keng tarqalgan; `MockMvc` testlarida `content().json("""...""")`, `WebTestClient` da expected JSON, `RestClient` body'si ham shunday. Switch expression `HttpStatus`/`HttpStatusCode` ni ishlashda, `@ExceptionHandler` ichida exception tipini `ProblemDetail` ga mapping qilishda, Spring Statemachine yoki oddiy enum-driven logikada ishlatiladi. Java 21+ da `switch` pattern matching bilan birga `sealed interface` natijalarini ishlashda standart usul.

**Qo'llanish keyslari:**
- `JdbcClient.sql("""...""")` bilan uzun native SQL so'rovlarini o'qiluvchan ko'rinishda yozish.
- Integratsiya testlarida kutilgan JSON payload'ni text block sifatida inline berish.
- `sealed interface` natijalarini `switch` ifodasi bilan to'liq, `default` shoxisiz ishlash.
- Enum'dan HTTP status yoki xabar matniga mapping qilishni bitta ifoda bilan yozish.
- GraphQL so'rovlari yoki ko'p qatrorli Kafka/`@Scheduled` cron izohlarini aniq ko'rsatish.

```java
String sql = """
    SELECT id, email FROM users
    WHERE status = :status
    ORDER BY created_at DESC
    """;
int code = switch (order.state()) {
    case NEW, PENDING -> 202;
    case SHIPPED -> 200;
    case CANCELLED -> 409;
};
```

**Ehtiyot bo'ling:** Text block'da indentatsiya eng kam bo'shliqli qatorga qarab hisoblanadi, shuning uchun yopuvchi `"""` ning joyi natijaga ta'sir qiladi va oxirgi qatorga `\n` qo'shilib qolishi mumkin - `.stripIndent()` xatti-harakatini tushunib ishlang. Text block ichiga foydalanuvchi ma'lumotini konkatenatsiya qilish SQL injection'ga yo'l ochadi; har doim named/positional parametr ishlatilsin.

## 24.34 Virtual thread'lar (Virtual Threads)

**Tavsif:** [Concurrency patternlari bobidagi virtual thread'lar yozuvi](04-concurrency-patternlari.md#423-virtual-threadlar-virtual-threads) bu patternning to'liq yozuvi, bu yerda faqat zamonaviy Java nuqtai nazari: Java 21 da stabillashgan yengil thread bloklanganda carrier thread'ni bo'shatadi va thread-per-request modelini reaktiv murakkabliksiz qaytaradi.

**Spring'da qayerda uchraydi:** Spring Boot 3.2+ da `spring.threads.virtual.enabled=true`, qo'lda `Executors.newVirtualThreadPerTaskExecutor()` va `Thread.ofVirtual().start()`.

**Qo'llanish keyslari:**
- JDBC va tashqi HTTP chaqiruvlariga tayangan bloklovchi kodni WebFlux'ga ko'chirmasdan I/O concurrency'ni oshirish.

**Ehtiyot bo'ling:** Virtual thread pool qilinmaydi va CPU-bound ishni tezlashtirmaydi, downstream (HikariCP, tashqi servis) uchun backpressure esa baribir aniq qo'yiladi.

## 24.35 Strukturalangan concurrency (Structured Concurrency)

**Tavsif:** [Concurrency patternlari bobidagi strukturaviy concurrency yozuvi](04-concurrency-patternlari.md#424-strukturaviy-concurrency-structured-concurrency) bu patternning to'liq yozuvi, bu yerda faqat zamonaviy Java nuqtai nazari: `StructuredTaskScope` subtask'lar hayot muddatini try-with-resources blokiga bog'laydi, xato va cancellation bir joyda boshqariladi.

**Spring'da qayerda uchraydi:** Java 25 da ham preview (`StructuredTaskScope.open(Joiner.allSuccessfulOrThrow())`, `--enable-preview`), Spring'da maxsus abstraksiya yo'q, production uchun stabil muqobil `CompletableFuture.allOf()`.

**Qo'llanish keyslari:**
- Bitta so'rov uchun bir nechta servisga parallel murojaat qilib (fan-out/fan-in), biri yiqilsa qolganini avtomatik bekor qilish.

**Ehtiyot bo'ling:** API preview bo'lgani uchun Java versiyalari orasida shakli o'zgaradi, scope esa metod chegarasidan tashqariga chiqarilmaydi.

## 24.36 Scoped Values (Scoped Values)

**Tavsif:** [Concurrency patternlari bobidagi qamrovli qiymatlar yozuvi](04-concurrency-patternlari.md#425-qamrovli-qiymatlar-scoped-values) bu patternning to'liq yozuvi, bu yerda faqat zamonaviy Java nuqtai nazari: `ScopedValue` immutable kontekstni faqat dinamik qamrov davomida ko'rinadigan qilib, `ThreadLocal` ni almashtiradi.

**Spring'da qayerda uchraydi:** `java.lang.ScopedValue` Java 25 da final (JEP 506), Spring kontekst holderlari esa hali `ThreadLocal` da, shuning uchun virtual thread bilan Security kontekstini uzatishda `DelegatingSecurityContextExecutor` yoki Micrometer context propagation ishlatiladi.

**Qo'llanish keyslari:**
- Tenant yoki `traceId` ni metod imzolarini ifloslantirmasdan chaqiruv daraxti bo'ylab uzatish.

**Ehtiyot bo'ling:** Qamrovdan chiqqan kodda (`@Async` task, keshlangan callback) qiymat yo'q, muhim biznes parametri esa metod argumenti sifatida uzatiladi.

## 24.37 Moslashuvchan konstruktor tanalari (Flexible Constructor Bodies)

**Tavsif:** Java 25 da final bo'lgan (JEP 513) imkoniyat: `super(...)` yoki `this(...)` chaqiruvidan oldin ham kod yozish mumkin - bu "prologue" deb ataladi. Shu joyda argumentlarni validatsiya qilish, hisoblash yoki normalizatsiya qilish mumkin, biroq `this` ning hali initsializatsiya qilinmagan maydonlariga murojaat qilinmaydi. Ilgari bu ish statik yordamchi metodlar yoki murakkab ternary ifodalar bilan aylanib o'tilardi; endi validatsiya noto'g'ri obyekt yaratilishidan va superclass konstruktori ishga tushishidan oldin bajariladi.

**Spring'da qayerda uchraydi:** Bu til imkoniyati, Spring API'si emas - Java 25 (`--release 25`) talab qiladi. Spring kontekstida eng foydali joyi: konstruktor injection bilan ishlaydigan `@Service`/`@Component` sinflarida inject qilingan bog'liqlikni `super(...)` dan oldin tekshirish, `RuntimeException` ierarxiyasidan meros olgan custom exception'larda xabarni `super(message)` ga uzatishdan avval shakllantirish, `@ConfigurationProperties` record'larining compact constructor'ida qiymatlarni normalizatsiya qilish. Mavjud muqobillar: `Assert.notNull()` (Spring `org.springframework.util.Assert`), `Objects.requireNonNull()` va record compact constructor.

**Qo'llanish keyslari:**
- `super(...)` ga uzatiladigan argumentni avval validatsiya qilib, noto'g'ri qiymat bilan superclass initsializatsiyasini boshlamaslik.
- Custom exception sinfida xato xabarini bir nechta maydondan yig'ib, keyin `super(message, cause)` chaqirish.
- Konstruktorga kelgan kolleksiyani normalizatsiya qilish (trim, lowercase, `List.copyOf`) va keyin `this(...)` ga uzatish.
- Value Object'da `Assert` tekshiruvlarini statik `validate(...)` metodga ajratmasdan, bevosita konstruktor boshida yozish.
- Bir nechta konstruktor overload'ini `this(...)` bilan zanjirlashda argumentni oldindan hisoblash.

**Ehtiyot bo'ling:** Prologue'da `this` ning maydonlarini o'qish yoki instance metodini chaqirish compile xatosi - faqat statik kontekst va lokal o'zgaruvchilar bilan ishlash mumkin. Java 25 dan quyi target bilan qurilgan loyihalarda mavjud emas, shuning uchun kutubxona yozayotganda minimal JDK talabini oshirib yuborish xavfini hisobga oling.

## 24.38 Nomsiz o'zgaruvchilar va pattern'lar (Unnamed Variables & Patterns)

**Tavsif:** Java 22 da final bo'lgan (JEP 456) `_` belgisi "bu qiymat kerak emas" degan niyatni compiler va o'quvchiga aniq bildiradi. U lokal o'zgaruvchi, `catch` parametri, lambda parametri, for-each o'zgaruvchisi, `try-with-resources` resursi va record deconstruction pattern komponentlari o'rnida ishlatiladi. Natijada `ignored`, `unused` kabi shovqinli nomlar yo'qoladi va static analiz "ishlatilmagan o'zgaruvchi" ogohlantirishini bermaydi.

**Spring'da qayerda uchraydi:** Til imkoniyati; Java 22+ (Spring Boot 3.3+/4.x bilan muammosiz). Spring kodida tipik joylari: `@EventListener` yoki `ApplicationListener` lambda'larida ishlatilmaydigan parametr, `RestClient`/`WebClient` ning `onStatus((req, _) -> ...)` uslubidagi BiFunction'lari, `JdbcTemplate` `RowCallbackHandler` lambda'lari, `ItemProcessor` (Spring Batch) va `@ExceptionHandler` ichidagi `catch (SpecificException _)`. Shuningdek `sealed interface` natijalarini `switch` bilan deconstruct qilganda keraksiz record komponentlarini `_` bilan tashlab ketish mumkin.

**Qo'llanish keyslari:**
- `catch (NumberFormatException _)` - exception obyekti kerak bo'lmagan parse fallback'larida.
- Record pattern'da faqat bitta komponent kerak bo'lganda: `case Payment(var amount, _, _) -> ...`.
- `map.forEach((key, _) -> keys.add(key))` kabi lambda'larda ishlatilmaydigan parametrni belgilash.
- `for (var _ : items) count++` - faqat elementlar sonini sanaganda.
- `try (var _ = MDC.putCloseable("traceId", id)) { ... }` kabi faqat side effect uchun ochilgan resurslarda.

**Ehtiyot bo'ling:** `_` ni maydon (field), metod parametri yoki record komponenti nomi sifatida ishlatish mumkin emas - faqat yuqorida sanalgan lokal kontekstlarda. Eski kodda `_` identifikator sifatida ishlatilgan bo'lsa (Java 8 dan beri ogohlantirilgan, Java 9 dan xato), migratsiyada uni almashtirish kerak; shuningdek `_` ni haqiqatan kerak bo'lgan qiymatni yashirish uchun ishlatish xatoni ko'mib tashlashi mumkin.

## 24.39 Funktor (Functor)

**Tavsif:** Functor - ichida qiymat saqlaydigan konteynerni "ochmasdan" uning tarkibidagi qiymatga funksiya qo'llash imkonini beruvchi abstraksiya; amalda bu `map`-ga o'xshash operatsiyani qo'llab-quvvatlovchi har qanday generik tip. Asosiy muammo shundaki, `Optional`, `List`, `CompletableFuture`, `Flux` kabi turli kontekstlarda joylashgan qiymatlar uchun har xil kod yozish kerak bo'ladi - Functor esa transformatsiya mantiqini kontekstni boshqarish mantiqidan ajratadi. Qoida sodda: `map` konteynerning shaklini (hajmi, xatolik holati, asinxronligi) o'zgartirmaydi, faqat ichidagi qiymatni almashtiradi. Shuning uchun `map` identity qonuni (`map(x -> x)` hech narsani o'zgartirmaydi) va kompozitsiya qonuniga (`map(f).map(g)` ≡ `map(f.andThen(g))`) bo'ysunadi - bu esa zanjirli transformatsiyalarni xavfsiz refaktor qilishga asos beradi.

**Spring'da qayerda uchraydi:** Java'da Functor alohida interfeys sifatida mavjud emas, lekin `java.util.Optional.map`, `java.util.stream.Stream.map`, `java.util.concurrent.CompletableFuture.thenApply` - hammasi aynan shu patternning konkret ko'rinishlari. Reaktiv Spring'da (`spring-webflux`, Project Reactor 3.x) `Mono.map` va `Flux.map` eng ko'p ishlatiladigan Functor operatorlari; `Mono.map` bloklovchi bo'lmagan oqimda DTO mapping uchun standart vosita. Spring Data'da `org.springframework.data.domain.Page.map(Function)` metodi sahifalash metadatasini (total elements, pageable) saqlab turib, faqat kontentni DTO'ga aylantiradi - bu Functor qonunining amaliy namunasi. `org.springframework.core.convert.converter.Converter<S,T>` va `ConversionService` ham `map` uchun qayta ishlatiladigan funksiyalar manbasi bo'lib xizmat qiladi, Java 21+ esa `record` va `Stream.gatherers` (JEP 485, Java 24'da final) bilan transformatsiya zanjirlarini yanada ixcham qiladi.

```java
public Page<UserDto> findAll(Pageable pageable) {
    return userRepository.findAll(pageable)   // Page<UserEntity>
            .map(UserDto::from);              // Page<UserDto>, metadata saqlanadi
}
```

**Qo'llanish keyslari:**
- Spring Data `Page<Entity>`ni `Page<Dto>`ga aylantirish, `totalElements` va sahifa raqamlarini qo'lda ko'chirmasdan.
- `Optional<User>` ichidan `Optional<String>` email olish - `isPresent()`/`get()` tekshiruvlarini butunlay yo'q qilish.
- WebFlux controller'da `Mono<Entity>`ni `Mono<ResponseEntity<Dto>>`ga map qilib, bloklovchi kod yozmaslik.
- `CompletableFuture.thenApply` bilan asinxron REST (`RestClient`/`WebClient`) javobini domen modeliga o'tkazish.
- `Stream.map` orqali CSV yoki Kafka'dan kelgan qatorlarni validatsiyadan oldin normalizatsiya qilish.

**Ehtiyot bo'ling:** `map` ichida `Optional` yoki `Mono` qaytaruvchi funksiya chaqirsangiz, `Optional<Optional<T>>` yoki `Mono<Mono<T>>` kabi ichma-ich joylashgan tip paydo bo'ladi - bu holatda `flatMap` ishlatish kerak (monad). Shuningdek `map` ichida bloklovchi I/O yoki yon ta'sir (DB yozish, log, exception tashlash) bajarmang: reaktiv oqimda bu event loop thread'ini bloklaydi, `Optional.map`da esa kutilmagan `NullPointerException` yoki yashirin xatoliklarga olib keladi.

## 24.40 Temir Yo'l Uslubidagi Dasturlash (Railway Oriented Programming)

**Tavsif:** Railway Oriented Programming - biznes mantiqni ikki yo'nalishli temir yo'l sifatida modellashtiradi: "muvaffaqiyat" relsi va "xatolik" relsi. Har bir qadam `Result<Success, Error>` (yoki `Either<L, R>`) tipini qaytaradi va zanjirga `flatMap` orqali ulanadi; agar biror qadam xato bersa, keyingi barcha qadamlar avtomatik o'tkazib yuboriladi va xatolik oxirigacha o'zgarmasdan "xatolik relsida" yetib boradi. Bu exception'larni boshqaruv oqimi (control flow) sifatida ishlatishni, chuqur `if (error != null) return ...` ichma-ichliklarini va har bosqichda `try/catch` yozishni yo'q qiladi. Natijada metodning signaturasi qaysi xatoliklar bo'lishi mumkinligini ochiq e'lon qiladi - kutilayotgan biznes xatoliklari tipda ko'rinadi, kutilmagan texnik nosozliklar esa exception sifatida qoladi.

**Spring'da qayerda uchraydi:** JDK'da `Result`/`Either` tipi yo'q, shuning uchun amalda Vavr (`io.vavr.control.Either`, `io.vavr.control.Try`) yoki `org.jooq:jool` kutubxonasi ishlatiladi; ko'p jamoalar esa Java 21 `sealed interface` + `record` bilan o'z `Result` tipini yozib, `switch` pattern matching (JEP 441) orqali ajratadi. Reaktiv stack'da Project Reactor'ning `Mono.flatMap` + `onErrorResume` + `Mono.error` juftligi aynan shu ikki relsni ifodalaydi, `Flux`da esa `Flux<Either<Error, Item>>` batch ishlov berishda keng tarqalgan. Spring MVC chegarasida `Result` HTTP javobiga `@RestControllerAdvice` emas, balki controller ichidagi `switch`/`fold` bilan aylantiriladi va `ProblemDetail` (`org.springframework.http.ProblemDetail`, Spring Framework 6+, RFC 9457) xatolik relsi uchun standart javob formati bo'lib xizmat qiladi. `@Transactional` bilan birga ishlatganda muhim nuqta: Spring'ning deklarativ tranzaksiyasi faqat exception'da rollback qiladi, qaytarilgan xatolik obyektini ko'rmaydi.

**Qo'llanish keyslari:**
- Ko'p bosqichli buyurtma yaratish: validatsiya → inventar rezervi → to'lov → tasdiqlash, har bosqich o'z xatolik tipini qaytaradi.
- Foydalanuvchi kiritgan ma'lumotni bosqichma-bosqich tekshirish va birinchi xatoda to'xtash, exception tashlamasdan.
- Tashqi API (to'lov gateway, KYC provayderi) javobini `Either`ga o'rab, retry qilinadigan va qilinmaydigan xatolikni tipda ajratish.
- Kafka consumer'da har bir xabarni `Result`ga aylantirib, muvaffaqiyatlilarni commit, xatolilarni DLQ'ga yuborish.
- Spring Batch `ItemProcessor`da yaroqsiz yozuvlarni butun chunk'ni yiqitmasdan xatolik relsiga o'tkazish.

**Ehtiyot bo'ling:** Eng keng tarqalgan xato - `Result` qaytaradigan metodni `@Transactional` ichida ishlatib, xatolik holatida rollback bo'lishini kutish: bunda tranzaksiya muvaffaqiyatli commit bo'ladi, shuning uchun `TransactionAspectSupport.currentTransactionStatus().setRollbackOnly()` chaqirish yoki chegarada exception'ga aylantirish kerak. Bu patternni butun kodbazaga majburan tatbiq etmang - infratuzilma nosozliklari (DB uzilishi, timeout) uchun exception tabiiyroq, `Result` esa faqat kutilayotgan biznes xatoliklari uchun; aks holda har bir metod signaturasi va zanjir shovqinli bo'lib, o'qilishi exception'li koddan ham qiyinlashadi.

## 24.41 Amalda qo'llash

- [ ] `record` ga o'tkazilishi mumkin bo'lgan DTO va qiymat obyektlarini ro'yxatga oling.
- [ ] Yopiq ierarxiya bo'lishi kerak bo'lgan interfeyslarni toping va `sealed` qo'llash foydasini qaror qiling.
- [ ] `Optional` ni maydon yoki parametr sifatida ishlatadigan joylarni qidirib tuzating - u qaytish turi uchun.
- [ ] `switch` bloklarini pattern matching bilan soddalashtirish nomzodlarini belgilang va `default` shoxi kerak emasligini tekshiring.
- [ ] Stream zanjirlarini ko'rib chiqing: ular oddiy siklga nisbatan o'qilishi osonmi, yo'qsa qaytaring.
- [ ] `var` ishlatilgan joylarni tekshirib, tur o'ng tomondan aniq ko'rinmaydigan holatlarni tuzating.
- [ ] Loyihaning Java versiyasini `pom.xml` dan tasdiqlab, keyingi LTS ga o'tish uchun to'siqlar ro'yxatini tuzing.
- [ ] Tekshirilgan istisnolarni (`checked exception`) oqimlar ichida ishlatadigan joylarni toping va ularni o'rash usulini birlashtiring.

---

[&larr; 23. Testing patternlari](23-testing-patternlari.md) · [Mundarija](README.md) · [25. Anti-patternlar &rarr;](25-anti-patternlar.md)
