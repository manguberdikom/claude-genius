<!-- doc: patterns | chapter: 3 | part:  -->

[Java Spring arxitektori bilishi kerak bo'lgan barcha dizayn patternlar](../../README.md) / [Dizayn patternlar](README.md)

# 3. Xulq-atvor patternlari (Behavioral Patterns)

<details>
<summary>Bu bo'limdagi 23 bo'lim</summary>

- [3.1 Mas'uliyat zanjiri (Chain of Responsibility)](#31-masuliyat-zanjiri-chain-of-responsibility)
- [3.2 Buyruq (Command)](#32-buyruq-command)
- [3.3 Interpretator (Interpreter)](#33-interpretator-interpreter)
- [3.4 Iterator (Iterator)](#34-iterator-iterator)
- [3.5 Vositachi (Mediator)](#35-vositachi-mediator)
- [3.6 Memento (Memento)](#36-memento-memento)
- [3.7 Kuzatuvchi (Observer)](#37-kuzatuvchi-observer)
- [3.8 Holat (State)](#38-holat-state)
- [3.9 Strategiya (Strategy)](#39-strategiya-strategy)
- [3.10 Shablon metodi (Template Method)](#310-shablon-metodi-template-method)
- [3.11 Tashrifchi (Visitor)](#311-tashrifchi-visitor)
- [3.12 Bo'sh obyekt (Null Object)](#312-bosh-obyekt-null-object)
- [3.13 Spetsifikatsiya (Specification)](#313-spetsifikatsiya-specification)
- [3.14 Xizmatkor (Servant)](#314-xizmatkor-servant)
- [3.15 Ravon interfeys (Fluent Interface)](#315-ravon-interfeys-fluent-interface)
- [3.16 Callback (Callback)](#316-callback-callback)
- [3.17 Pipeline (obyekt darajasida) (Pipeline (object-level))](#317-pipeline-obyekt-darajasida-pipeline-object-level)
- [3.18 Ikki tomonlama dispatch (Double Dispatch)](#318-ikki-tomonlama-dispatch-double-dispatch)
- [3.19 Event agregatori (Event Aggregator)](#319-event-agregatori-event-aggregator)
- [3.20 O'rab bajarish (Execute Around)](#320-orab-bajarish-execute-around)
- [3.21 Chekli holatlar mashinasi (Finite State Machine (Spring Statemachine))](#321-chekli-holatlar-mashinasi-finite-state-machine-spring-statemachine)
- [3.22 Qoidalar dvigateli / Siyosat (Rules Engine / Policy)](#322-qoidalar-dvigateli--siyosat-rules-engine--policy)
- [3.23 Qora taxta (Blackboard)](#323-qora-taxta-blackboard)

</details>



Xulq-atvor patternlari obyektlar orasidagi mas'uliyat taqsimoti va o'zaro muloqot algoritmlarini tartibga soladi - ya'ni "kim kim bilan gaplashadi va qaysi qarorni kim qabul qiladi" degan savolga javob beradi. Yaratuvchi patternlar obyekt qanday paydo bo'lishini, strukturaviy patternlar ularning qanday bog'lanishini hal qilsa, xulq-atvor patternlari tizimning dinamikasini - oqimlarni, hodisalarni, holat o'tishlarini va kengaytirish nuqtalarini belgilaydi. Spring Framework'ning o'zi aslida bu patternlarning sanoat miqyosidagi katalogi: `JdbcTemplate`, `PasswordEncoder`, `@EventListener`, `SecurityFilterChain` - bularning hammasi shu bo'limdagi g'oyalarning amaliy ko'rinishi. Arxitektor uchun ularni bilish ikki tomonlama foydali: birinchidan, Spring'ning ichki mexanizmlarini (nega aynan shu extension point bor) tushunadi, ikkinchidan, o'z domen kodida `if/else` va `switch` daraxtlarini polimorfizm bilan almashtirib, o'zgarishga ochiq dizayn qura oladi.

## 3.1 Mas'uliyat zanjiri (Chain of Responsibility)

**Tavsif:** So'rovni bir nechta handler'dan iborat zanjir orqali o'tkazadi: har bir handler yoki so'rovni o'zi qayta ishlaydi, yoki keyingisiga uzatadi. Yuboruvchi qaysi handler javob berishini bilmaydi, shuning uchun zanjir tarkibi va tartibi runtime'da erkin o'zgartiriladi. Bu cross-cutting mantiqni (autentifikatsiya, logging, validatsiya, rate limiting) asosiy biznes kodidan ajratib, mustaqil bo'laklarga bo'lish imkonini beradi. Zanjir odatda dekorativ emas, balki "to'xtatish huquqi" bilan ishlaydi - har qanday bo'g'in oqimni uzib, javob qaytarishi mumkin.

**Spring'da qayerda uchraydi:** Eng toza misol - Spring Security'dagi `FilterChainProxy` va u boshqaradigan `SecurityFilterChain` (Spring Security 6.x'da `SecurityFilterChain` bean'lari `HttpSecurity` orqali yig'iladi), unda `OncePerRequestFilter` merosxo'rlari `FilterChain.doFilter()` ni chaqirib zanjirni davom ettiradi. Jakarta Servlet spetsifikatsiyasidagi `jakarta.servlet.Filter`/`FilterChain`, Spring MVC'dagi `HandlerInterceptor` ketma-ketligi (`HandlerExecutionChain`), WebFlux'dagi `WebFilter`/`WebFilterChain` ham xuddi shu pattern. Spring AOP ichida `ReflectiveMethodInvocation` `MethodInterceptor` ro'yxatini birin-ketin chaqiradi - ya'ni har bir `@Transactional`/`@Cacheable` interceptor zanjirning bir bo'g'ini. `RestClient` va `RestTemplate` uchun `ClientHttpRequestInterceptor`, WebClient uchun `ExchangeFilterFunction` ham shu modelda.

**Qo'llanish keyslari:**
- HTTP so'rov uchun autentifikatsiya, CORS, CSRF, rate limiting va audit bosqichlarini mustaqil filter'larga ajratish.
- Kiruvchi hujjat yoki to'lov buyrug'ini ketma-ket validatsiya qoidalaridan o'tkazish, birinchi xatolikda to'xtatish.
- Kelgan event'ni bir necha ixtisoslashgan handler orasidan "kim tanidi, o'sha ishlaydi" printsipida tarqatish.
- Legacy integratsiyada xabarni normalizatsiya → boyitish → yo'naltirish bosqichlariga bo'lish (Spring Integration pipeline).
- Multi-tenant tizimda tenant aniqlash va kontekst to'ldirishni biznes mantiqdan oldin bajarish.

**Ehtiyot bo'ling:** Zanjir uzun bo'lsa, debug qilish og'irlashadi va handler'lar tartibiga yashirin bog'liqlik paydo bo'ladi - shuning uchun `@Order`/`OrderComparator` bilan tartibni oshkora belgilang va zanjirni Actuator yoki log orqali ko'rinadigan qiling. Agar so'rovni albatta kimdir qayta ishlashi shart bo'lsa, zanjir oxirida default handler qo'ying; aks holda "jim yo'qolgan" so'rovlar paydo bo'ladi.

## 3.2 Buyruq (Command)

**Tavsif:** Amalni obyekt sifatida inkapsulyatsiya qiladi: bajariladigan ish, uning parametrlari va receiver bitta sinfga joylanadi. Shu sababli amalni navbatga qo'yish, kechiktirish, qayta urinish, jurnalga yozish yoki bekor qilish (undo) mumkin bo'ladi. Chaqiruvchi (invoker) amal nima qilishini bilmaydi - faqat `execute()` ni biladi, bu esa chaqiruvchini mantiqdan to'liq ajratadi.

**Spring'da qayerda uchraydi:** `java.lang.Runnable` va `java.util.concurrent.Callable` - til darajasidagi Command; Spring ularni `TaskExecutor`, `@Async` va `ThreadPoolTaskExecutor` orqali bajaradi, Java 21+ virtual thread'lar bilan esa `SimpleAsyncTaskExecutor.setVirtualThreads(true)` yoki `spring.threads.virtual.enabled=true` sozlamasi ishlatiladi. Spring Framework'ning callback interfeyslari - `TransactionCallback`, `JdbcTemplate` ichidagi `StatementCallback`, `ConnectionCallback` - resursga nisbatan bajariladigan buyruqlar. Spring Batch'dagi `Tasklet` va `Step` bajarilishi, Spring Shell'dagi `@ShellMethod`, CQRS uchun Axon Framework'ning `@CommandHandler`/`CommandGateway` ham shu patternga asoslanadi.

**Qo'llanish keyslari:**
- Uzoq davom etadigan ishni (hisobot generatsiyasi, export) command obyekti ko'rinishida navbatga qo'yib, worker'da bajarish.
- CQRS arxitekturasida `CreateOrderCommand` kabi oshkora buyruqlar bilan yozish oqimini modellashtirish.
- Audit talabi bor tizimda har bir foydalanuvchi amalini seriyalashtirib saqlash va kerak bo'lsa qayta ijro etish (replay).
- Undo/redo zarur bo'lgan hujjat yoki konfiguratsiya tahrirlash oqimlari.
- Outbox pattern bilan tranzaksiya oxirida bajarilishi kerak bo'lgan tashqi chaqiruvlarni buyruq sifatida saqlash.

**Ehtiyot bo'ling:** Har bir kichik amal uchun alohida command sinfi yozish kodni portlatib yuboradi - buni faqat navbat, retry, audit yoki undo kerak bo'lganda qo'llang. Seriyalanadigan buyruqlar API shartnomasiga aylanadi: maydon qo'shish/olib tashlashda versiyalashni oldindan o'ylamasa, navbatda yotgan eski buyruqlar deserializatsiyada sinadi.

## 3.3 Interpretator (Interpreter)

**Tavsif:** Ma'lum bir tilning grammatikasini obyekt daraxti (AST) sifatida ifodalab, shu daraxtni aylanib chiqib ifodani hisoblaydi. Har bir grammatik qoida alohida sinfga mos keladi, shuning uchun til yangi konstruksiyalar bilan kengaytiriladi. Natijada biznes qoidalari yoki filtrlar kompilyatsiya qilinmagan, matn ko'rinishida saqlanib, runtime'da bajariladi.

**Spring'da qayerda uchraydi:** Spring Expression Language (SpEL) - `org.springframework.expression.spel.standard.SpelExpressionParser`, `Expression`, `StandardEvaluationContext` - klassik Interpreter implementatsiyasi; `@Value("#{...}")`, `@Cacheable(key = "...")`, `@PreAuthorize("hasRole('ADMIN')')")` kabi annotatsiyalar shu interpretator ustida ishlaydi. Spring Data'dagi `PartTree` metod nomini (`findByLastNameAndAgeGreaterThan`) grammatik tahlil qilib query'ga aylantiradi, Hibernate 6 esa HQL/JPQL uchun Antlr asosidagi parser va semantik daraxt (SQM) ishlatadi. Spring Boot'ning `@ConditionalOnExpression` va Actuator'ning filtr ifodalari ham SpEL'ga tayanadi.

**Qo'llanish keyslari:**
- Bitta deploy ichida o'zgaradigan narx yoki chegirma qoidalarini matn ifoda sifatida bazada saqlash.
- Foydalanuvchi yozadigan hisobot filtrlari uchun xavfsiz, cheklangan DSL berish.
- Feature flag va routing shartlarini konfiguratsiyada ifoda bilan belgilash.
- Low-code forma validatsiyasi: maydonlar orasidagi shartlarni deklarativ yozish.
- Risk yoki fraud skoringda analitiklar tahrirlaydigan qoidalar to'plamini bajarish.

**Ehtiyot bo'ling:** Tashqi foydalanuvchi kiritgan SpEL'ni to'g'ridan-to'g'ri hisoblash jiddiy RCE xavfi - `SimpleEvaluationContext` yoki o'zingiz yozgan cheklangan grammatikadan foydalaning, `StandardEvaluationContext` ni ishonchsiz matn bilan ishlatmang. To'laqonli til yozishga kirishishdan oldin o'ylab ko'ring: ko'p holatda Strategy yoki tayyor rule engine (Drools, OpenPolicyAgent) arzonga tushadi.

## 3.4 Iterator (Iterator)

**Tavsif:** To'plam elementlarini uning ichki tuzilishini oshkor qilmasdan ketma-ket aylanib chiqish usulini beradi. Aylanish holati (kursor) alohida obyektda saqlanadi, shuning uchun bir to'plam ustida bir nechta mustaqil obxod bo'lishi mumkin. Katta ma'lumotlar bilan ishlaganda esa butun to'plamni xotiraga olmasdan, bo'lak-bo'lak o'qishga yo'l ochadi.

**Spring'da qayerda uchraydi:** Platforma darajasida `java.util.Iterator`, `Iterable`, `Spliterator` va `Stream`; Spring Data'da `Streamable`, `Page`/`Slice`/`Pageable` (pagination asosida kursor), MongoDB va JPA repository'laridagi `Stream<T>` qaytaruvchi metodlar va `CloseableIterator`. Spring Batch'da `ItemReader` - eng aniq ko'rinishdagi Iterator: `JdbcCursorItemReader`, `JdbcPagingItemReader`, `FlatFileItemReader` `read()` chaqirig'i bilan birin-ketin element qaytaradi va oxirida `null` beradi. Reaktiv dunyoda Project Reactor'ning `Flux` push-asosidagi, `JdbcTemplate` ning `RowCallbackHandler` esa callback-asosidagi obxodni ta'minlaydi.

**Qo'llanish keyslari:**
- Millionlab qatorli jadvalni ETL jarayonida kursor bilan oqim sifatida o'qish.
- REST API'da katta natijani `Page` yoki keyset pagination orqali qismlarga bo'lib qaytarish.
- Tashqi API'ning sahifalangan javobini bitta `Iterator`/`Stream` ortiga yashirish.
- Fayl yoki Kafka topic'ini xotiraga sig'maydigan hajmda ketma-ket qayta ishlash.
- Domen agregatida ichki kolleksiyani faqat o'qish uchun ochib berish (incapsulyatsiyani buzmasdan).

**Ehtiyot bo'ling:** Repository'dan qaytgan `Stream` yoki `CloseableIterator` ochiq DB kursorini ushlab turadi - uni `try-with-resources` ichida yoping va tranzaksiya doirasida ishlating, aks holda connection pool tez tugaydi. `Iterator` bilan aylanib turib to'plamni o'zgartirish `ConcurrentModificationException` beradi; offset-asosidagi pagination esa chuqur sahifalarda sekinlashadi va yozuvlar siljishi sababli element tashlab ketadi.

## 3.5 Vositachi (Mediator)

**Tavsif:** Ko'p komponentni bir-biri bilan to'g'ridan-to'g'ri gaplashtirish o'rniga, muloqotni bitta vositachi obyektga yuklaydi. Natijada N×N bog'liqlik to'ri N ta bog'liqlikka aylanadi va komponentlar bir-birini bilmasdan ishlaydi. Koordinatsiya mantiqi bir joyda to'planadi, bu uni test qilish va o'zgartirishni osonlashtiradi.

**Spring'da qayerda uchraydi:** `ApplicationEventPublisher` va uning ortidagi `ApplicationEventMulticaster` (`SimpleApplicationEventMulticaster`) - ilovadagi markaziy vositachi: publisher listener'larni, listener'lar publisher'ni bilmaydi. Spring Integration'da `MessageChannel`, `MessageRouter` va `IntegrationFlow`'lar endpoint'lar orasidagi muloqotni to'liq vositachiga topshiradi; Spring Cloud Stream `Binder` orqali shu rolni broker ustida bajaradi. Spring Modulith'da modullar orasidagi aloqa atayin event'lar (`@ApplicationModuleListener`) orqali, to'g'ridan-to'g'ri bean injection'siz qurilishi tavsiya etiladi. Spring MVC'dagi `DispatcherServlet` ham `HandlerMapping`, `HandlerAdapter` va `ViewResolver` orasidagi muvofiqlashtiruvchi sifatida xuddi shu vazifani bajaradi.

**Qo'llanish keyslari:**
- Modulli monolitda bounded context'lar orasidagi aloqani event bus orqali qurish va kompilyatsiya bog'liqligini uzish.
- Bir nechta tashqi servisni (to'lov, ombor, bildirishnoma) chaqiruvchi buyurtma oqimini bitta orchestrator'ga yig'ish.
- Murakkab UI/forma holatida maydonlar orasidagi o'zaro ta'sirni markazlashtirish (masalan Vaadin yoki JavaFX view controller).
- Chat yoki WebSocket xonalarida xabarlarni `SimpMessagingTemplate` orqali tarqatish.
- Legacy integratsiyada turli protokollardagi tizimlarni ESB/Spring Integration vositachisi ostida ulash.

**Ehtiyot bo'ling:** Vositachi o'sib ketsa, u "god object" ga aylanadi - barcha biznes qoidalari bitta sinfga yig'ilib, uni o'zgartirish xavfli bo'ladi; mantiqni domen servislariga qaytarib, vositachida faqat yo'naltirishni qoldiring. Event'lar orqali qurilgan vositachilik oqimni ko'rinmas qiladi: tracing (Micrometer Tracing) va oshkora event katalogi bo'lmasa, nosozlikni topish qiyinlashadi.

## 3.6 Memento (Memento)

**Tavsif:** Obyektning ichki holatini inkapsulyatsiyani buzmasdan tashqi "snapshot" sifatida saqlaydi va keyin shu holatga qaytarish imkonini beradi. Snapshot ichini faqat egasi tushunadi, boshqalar uni shunchaki saqlovchi (caretaker) sifatida ushlab turadi. Shu tufayli undo, checkpoint va davom ettirish (resume) imkoniyatlari paydo bo'ladi.

**Spring'da qayerda uchraydi:** Spring Batch'dagi `ExecutionContext` - klassik Memento: `ItemStream.update()` orqali o'qish pozitsiyasi `JobRepository` ga yoziladi va restart'da aynan shu joydan davom etiladi. Spring Statemachine'da `StateMachineContext` va `StateMachinePersister` mashina holatini tashqi omborga saqlaydi/tiklaydi. Tranzaksiya darajasida `SavepointManager` va `TransactionStatus.createSavepoint()` (`PROPAGATION_NESTED`) qisman rollback uchun checkpoint beradi; Hibernate'ning dirty checking mexanizmi esa yuklangan entity'ning snapshot'ini persistence context'da saqlaydi. HTTP sohasida `HttpSession` va Spring Session (`spring-session-data-redis`) foydalanuvchi holatining saqlangan nusxasi sifatida ishlaydi.

**Qo'llanish keyslari:**
- Uzoq batch job'ni uzilishdan keyin oxirgi checkpoint'dan qayta ishga tushirish.
- Hujjat yoki konfiguratsiya tahririda undo/redo va versiya tarixini qo'llab-quvvatlash.
- Ko'p qadamli wizard formasida har qadam holatini saqlab, orqaga qaytish imkonini berish.
- Saga yoki state machine instance'ini bazada saqlab, boshqa node'da davom ettirish.
- Domen agregatining "oldingi qiymatlari" ni audit uchun snapshot ko'rinishida yozish.

**Ehtiyot bo'ling:** Katta obyektlarning snapshot'lari xotira va I/O ni tez yeb qo'yadi - faqat zarur maydonlarni saqlang yoki event sourcing + davriy snapshot kombinatsiyasiga o'tishni ko'rib chiqing. Snapshot'ni oddiy DTO sifatida ochib qo'ysangiz, inkapsulyatsiya yo'qoladi va saqlangan formatning har bir o'zgarishi migratsiya muammosiga aylanadi.

## 3.7 Kuzatuvchi (Observer)

**Tavsif:** Bitta subyekt holati o'zgarganda unga obuna bo'lgan barcha kuzatuvchilarga avtomatik xabar beradi. Subyekt kuzatuvchilarning konkret turini bilmaydi, shuning uchun yangi reaksiyalarni mavjud kodga tegmasdan qo'shish mumkin. Bu "ochiq-yopiq" printsipini amalda ta'minlaydigan eng keng tarqalgan mexanizm.

**Spring'da qayerda uchraydi:** `ApplicationEventPublisher.publishEvent()`, `ApplicationListener<E>`, `@EventListener` va `@TransactionalEventListener` (`AFTER_COMMIT` fazasi bilan) - Spring'ning o'zidagi asosiy Observer apparati; Spring Boot ichki hodisalari (`ApplicationReadyEvent`, `ContextRefreshedEvent`, Security'dagi `AuthenticationSuccessEvent`) ham shu orqali tarqaladi. Spring Data'da `@DomainEvents` va `AbstractAggregateRoot.registerEvent()` agregat saqlanganda domen hodisalarini avtomatik e'lon qiladi. Reaktiv stack'da `Publisher`/`Subscriber` (Reactive Streams, Project Reactor) backpressure bilan ishlaydigan Observer varianti; `java.beans.PropertyChangeListener` esa platformadagi tarixiy misol.

```java
@Component
class OrderPaidListener {
    @TransactionalEventListener(phase = TransactionPhase.AFTER_COMMIT)
    void on(OrderPaidEvent e) {
        // commit'dan keyin: xabarnoma, outbox, integratsiya
    }
}
```

**Qo'llanish keyslari:**
- Buyurtma to'langandan so'ng xabarnoma, hisob-faktura va analitikani bir-biridan mustaqil ishga tushirish.
- Cache'ni ma'lumot o'zgarishi hodisasi bilan invalidatsiya qilish.
- Audit va metrikalarni biznes kodga tegmasdan hodisalar orqali yig'ish.
- Modulli monolitda modullar orasidagi "nozik" aloqa (Spring Modulith).
- WebSocket/SSE orqali frontend'ga real vaqt yangilanishlarini uzatish.

**Ehtiyot bo'ling:** Standart `@EventListener` chaqiruvi sinxron va bir xil thread'da bajariladi - og'ir listener publisher tranzaksiyasini uzaytiradi yoki uni sindiradi; shuning uchun `AFTER_COMMIT` yoki `@Async` dan foydalaning, lekin `@Async` bilan hodisa yo'qolishi mumkinligini hisobga olib outbox qo'llang. Listener'lar soni ko'paygach, oqim "yashirin" bo'lib qoladi: bir hodisa boshqa hodisani chaqiradigan kaskadlar va ro'yxatdan yechilmagan listener'lar (memory leak) ni nazorat qilish kerak.

## 3.8 Holat (State)

**Tavsif:** Obyektning xulqi uning ichki holatiga qarab o'zgarishini alohida holat sinflariga chiqaradi: har bir holat o'zining ruxsat etilgan amallarini va keyingi o'tishlarini biladi. Shu tariqa katta `switch (status)` daraxtlari polimorfizm bilan almashtiriladi. O'tishlar oshkora bo'lgani uchun noto'g'ri holat kombinatsiyalari kompilyatsiya yoki konfiguratsiya darajasida bloklanadi.

**Spring'da qayerda uchraydi:** Spring Statemachine (`spring-statemachine-core`) - holatlar, o'tishlar, guard va action'larni deklarativ e'lon qilish uchun maxsus proyekt; `StateMachineBuilder`, `@WithStateMachine`, `@OnTransition` annotatsiyalari bilan ishlatiladi. Spring Batch'da `BatchStatus`/`ExitStatus` va step oqimining shartli o'tishlari (`on("FAILED").to(...)`) holat mashinasini konfiguratsiya bilan ifodalaydi. Oddiy Java'da `sealed interface` + `record` (Java 17+) va `switch` pattern matching (Java 21+) holat modelini tilning o'zida xavfsiz yozish imkonini beradi; Spring Security'dagi autentifikatsiya oqimi (anonymous → authenticated → fully authenticated) ham holatga asoslangan xulqqa misol.

**Qo'llanish keyslari:**
- Buyurtma yoki to'lov lifecycle'ini (`NEW → PAID → SHIPPED → RETURNED`) qat'iy o'tishlar bilan modellashtirish.
- Hujjat tasdiqlash workflow'i: har bir holatda kim nima qila olishini aniq cheklash.
- Qurilma yoki IoT sessiyasining ulanish holatlarini boshqarish.
- Saga/long-running jarayonning qadamlarini holat mashinasi sifatida saqlash va tiklash.
- Subscription billing holatlari (trial, active, past due, canceled) va ularga mos ruxsatlar.

**Ehtiyot bo'ling:** To'laqonli state machine framework'ini uch-to'rt holatli oddiy oqim uchun kiritish ortiqcha murakkablik - avval enum + o'tish jadvali yoki `sealed` ierarxiyani sinab ko'ring. Holatni bazada faqat satr (`String status`) sifatida saqlab, o'tish qoidalarini kodda tarqatib yuborish eng keng tarqalgan xato: tekshiruvni bitta joyda markazlashtiring, aks holda ma'lumot bazasida "imkonsiz" holatlar paydo bo'ladi.

## 3.9 Strategiya (Strategy)

**Tavsif:** Bir vazifani bajarishning bir nechta algoritmini alohida sinflarga ajratib, umumiy interfeys ortida almashtiriladigan qiladi. Mijoz kodi qaysi algoritm ishlayotganini bilmaydi va shart operatorlari o'rniga shunchaki interfeysga tayanadi. Yangi variant qo'shish mavjud kodni o'zgartirishni talab qilmaydi - bu DI konteynerlari bilan eng tabiiy birlashadigan pattern.

**Spring'da qayerda uchraydi:** Spring'ning yarmi Strategy ustida qurilgan: `PasswordEncoder` (`BCryptPasswordEncoder`, `Argon2PasswordEncoder`, `DelegatingPasswordEncoder`), `AuthenticationProvider`, `CacheManager`/`Cache`, `TaskExecutor`, `HttpMessageConverter`, `ClientHttpRequestFactory` (`JdkClientHttpRequestFactory`, `ApacheHttpClient...`), `PlatformTransactionManager`, Spring Retry'dagi `RetryPolicy`/`BackOffPolicy`, Spring Cloud LoadBalancer'dagi `ReactorServiceInstanceLoadBalancer`. Amaliy loyihada esa strategiyalarni `Map<String, PricingStrategy>` yoki `List<Validator>` ko'rinishida inject qilish standart yondashuv; `ObjectProvider` va `@Qualifier` tanlashni nozik boshqarish uchun ishlatiladi.

```java
@Service
class PaymentRouter {
    private final Map<String, PaymentStrategy> strategies; // bean nomi -> strategiya
    PaymentRouter(Map<String, PaymentStrategy> strategies) { this.strategies = strategies; }
    Receipt pay(String provider, Money amount) {
        return strategies.get(provider).charge(amount);
    }
}
```

**Qo'llanish keyslari:**
- To'lov provayderlari (Click, Payme, Stripe) uchun bitta interfeys va provayderga qarab tanlanadigan implementatsiya.
- Narx/chegirma hisoblash algoritmlarini mijoz segmentiga qarab almashtirish.
- Fayl export formatlari (CSV, XLSX, PDF) uchun bir xil shartnoma.
- Retry va backoff siyosatlarini integratsiya turiga qarab sozlash.
- Multi-tenant tizimda tenant'ga xos biznes qoidalarini alohida strategiya bean'lari bilan berish.

**Ehtiyot bo'ling:** Faqat bitta implementatsiya bo'lgan joyda interfeys yaratish - bu "spekulyativ generallik", keraksiz qatlam; ikkinchi variant real paydo bo'lganda ajratish arzonroq. Strategiyalar orasida umumiy mutable state ulashmang va `Map` orqali tanlashda kalitni (bean nomini) oshkora `enum` yoki annotatsiya bilan bog'lang, aks holda noto'g'ri kalit runtime'da `NullPointerException` beradi.

## 3.10 Shablon metodi (Template Method)

**Tavsif:** Algoritmning umumiy skeletini bazaviy sinfda belgilab, o'zgaradigan qadamlarini abstrakt yoki hook metodlarga chiqaradi. Merosxo'r faqat kerakli qadamni amalga oshiradi, qadamlarning tartibi va invariantlari (resurs ochish/yopish, xatolikni o'girish) baza sinf nazoratida qoladi. Bu takrorlanuvchi infratuzilma kodini bir joyda markazlashtirishning eng tezkor usuli.

**Spring'da qayerda uchraydi:** `JdbcTemplate`, `JmsTemplate`, `RedisTemplate`, `TransactionTemplate`, `RestTemplate` - nomidan ko'rinib turgani kabi, resursni ochish, xatolikni `DataAccessException` ierarxiyasiga o'girish va yopishni o'z ustiga olib, faqat callback qismini sizga qoldiradi (Template Method + Callback birgalikda). `AbstractApplicationContext.refresh()` konteyner ishga tushish skeletini belgilaydi va `postProcessBeanFactory()`, `onRefresh()` kabi hook'larni qoldiradi. Spring Security'dagi `AbstractAuthenticationProcessingFilter.attemptAuthentication()`, Spring MVC'dagi `OncePerRequestFilter.doFilterInternal()`, Spring Batch'dagi `AbstractItemCountingItemStreamItemReader.doRead()` ham shu pattern; platformadagi klassik misol - `HttpServlet.service()` → `doGet()/doPost()`.

**Qo'llanish keyslari:**
- Tashqi integratsiya chaqiruvlari uchun umumiy skelet: logging, timeout, retry, metrika - faqat "so'rovni tuzish" qadami o'zgaradi.
- Import/export pipeline'ida o'qish → validatsiya → transformatsiya → yozish bosqichlarini qat'iy tartibda ushlab turish.
- Custom filter yoki interceptor yozishda Spring'ning `OncePerRequestFilter` kabi baza sinflarini kengaytirish.
- Testlarda umumiy setup/teardown skeletini bazaviy test sinfiga chiqarish.
- Hisobot generatsiyasining umumiy oqimi bilan formatga xos render qadamini ajratish.

**Ehtiyot bo'ling:** Meros qattiq bog'liqlik yaratadi - baza sinf o'zgarganda barcha merosxo'rlar sinishi mumkin va Java'da bitta sinfdan ko'p meros yo'q; shuning uchun ko'p holatda Strategy yoki funksional interfeys (lambda-callback) moslashuvchanroq. Hook metodlarni `public` qilib qo'ymang va konstruktordan chaqirilgan overridable metodlardan voz keching: subclass hali to'liq initsializatsiya bo'lmagan holatda ishlab ketadi.

## 3.11 Tashrifchi (Visitor)

**Tavsif:** Obyekt tuzilmasi (masalan AST yoki hujjat daraxti) ustida bajariladigan amalni alohida "tashrifchi" sinfga chiqaradi, shunda yangi amal qo'shish uchun element sinflarini o'zgartirish kerak bo'lmaydi. Double dispatch orqali har bir element tashrifchining o'ziga mos `visitXxx()` metodini chaqiradi. Natijada tuzilma barqaror, amallar esa erkin kengayadigan bo'ladi.

**Spring'da qayerda uchraydi:** Spring Core ichida `BeanDefinitionVisitor` bean definition'lardagi qiymatlarni aylanib chiqib placeholder'larni almashtiradi (`PropertySourcesPlaceholderConfigurer` shu orqali ishlaydi). Spring o'z ichiga repackage qilgan ASM'da `ClassVisitor`/`AnnotationVisitor` (`SimpleAnnotationMetadataReadingVisitor`) class fayllarini yuklamasdan skanerlaydi - `@ComponentScan` va `@ConditionalOn...` shartlari aynan shunga tayanadi. Platformada `java.nio.file.FileVisitor`/`SimpleFileVisitor` daraxt bo'ylab yurish uchun, `javax.lang.model.element.ElementVisitor` esa annotation processor'lar (MapStruct, Lombok) uchun; Hibernate 6 va Querydsl query daraxtlarini visitor bilan SQL'ga o'giradi, Jackson'ning `JsonNode` ustidagi obxodlari ham shu uslubda yoziladi.

**Qo'llanish keyslari:**
- Query DSL yoki filtr daraxtini turli backend'larga (SQL, Elasticsearch, Mongo) o'girish.
- Konfiguratsiya yoki hujjat daraxti bo'ylab validatsiya, statistika va transformatsiya amallarini mustaqil qo'shish.
- Annotation processing yoki kod generatsiyasida AST tahlili.
- Hisob-kitob daraxtlari (narx formulalari, soliq qoidalari) ustida bir nechta hisoblash amalini bajarish.
- Statik tahlil/lint vositalarida bir xil daraxt ustida ko'p tekshiruvni ishlatish.

**Ehtiyot bo'ling:** Visitor element turlari barqaror bo'lganda foydali: yangi element turi qo'shilsa, barcha visitor'larni o'zgartirishga majbur bo'lasiz - bu teskari yo'nalishdagi qattiqlik. Java 21'dagi `sealed` ierarxiya + `switch` pattern matching aksariyat holatda visitor boilerplate'ini butunlay o'rnini bosadi, shuning uchun yangi kodda avval shuni ko'rib chiqing.

## 3.12 Bo'sh obyekt (Null Object)

**Tavsif:** `null` qaytarish o'rniga interfeysni amalga oshiruvchi, lekin "hech nima qilmaydigan" neytral obyekt qaytaradi. Mijoz kodi `if (x != null)` tekshiruvlaridan xoli bo'ladi va xulq bir xil polimorf yo'l bilan davom etadi. Bu, ayniqsa, optional hamkor komponentlar (logger, metrika, cache, notifier) uchun kodni ancha toza qiladi.

**Spring'da qayerda uchraydi:** Spring Framework'da `NoOpCacheManager`/`NoOpCache` (cache'ni o'chirish uchun), Spring Security'da `NullRequestCache`, `NullRememberMeServices`, `NullSecurityContextRepository` va WebFlux uchun `NoOpServerSecurityContextRepository`, shuningdek `ProviderManager` ichidagi null event publisher. spring-jcl modulidagi `NoOpLog`, Micrometer'dagi `Tracer.NOOP` va noop meter'lar, SLF4J'dagi `NOPLogger` ham shu g'oyaning tayyor implementatsiyalari. Java'da `Collections.emptyList()`, `Optional.empty()` va `Function.identity()` neytral qiymatlar sifatida xizmat qiladi; Spring Data repository'lari esa `null` o'rniga `Optional<T>` qaytarishni standart qilib qo'ygan.

**Qo'llanish keyslari:**
- Test va dev profilida haqiqiy xabarnoma yoki to'lov gateway'i o'rniga no-op implementatsiya ulash.
- Cache yoki metrika ixtiyoriy bo'lgan modulda `@ConditionalOnMissingBean` bilan no-op fallback berish.
- Domenda "mehmon foydalanuvchi" yoki "chegirmasiz siyosat" kabi neytral qiymatlarni obyekt sifatida ifodalash.
- Kolleksiya qaytaruvchi metodlarda hamisha bo'sh kolleksiya qaytarib, chaqiruvchini NPE'dan saqlash.
- Feature flag o'chirilganda butun strategiyani no-op variantga almashtirish.

**Ehtiyot bo'ling:** Null Object xatoni yashirib qo'yishi mumkin - konfiguratsiya yo'qolgani sababli hamma joyda jim ishlaydigan no-op bean ulanib qolsa, muammo production'da ancha keyin ma'lum bo'ladi; shuning uchun ishga tushishda ogohlantirish logi yoki Actuator'da ko'rinadigan belgi qoldiring. Shuningdek, "hech nima qilmaslik" domen uchun to'g'ri javob bo'lmagan joyda (masalan to'lovni o'tkazish) no-op emas, oshkora xatolik kerak.

## 3.13 Spetsifikatsiya (Specification)

**Tavsif:** Biznes qoidasini (predikatni) alohida obyekt sifatida kapsulalaydi va ularni `and`, `or`, `not` operatorlari bilan kompozitsiya qilish imkonini beradi. Natijada murakkab filtrlash shartlari qayta ishlatiladigan, mustaqil testlanadigan bloklarga ajraladi va service qatlamidagi uzun `if` zanjirlari yo'qoladi. Ko'pincha ikki qiyofada bo'ladi: in-memory kolleksiyani tekshirish va ma'lumotlar bazasiga query sifatida tarjima qilish.

**Spring'da qayerda uchraydi:** Spring Data JPA'ning `org.springframework.data.jpa.domain.Specification<T>` interfeysi aynan shu pattern: `JpaSpecificationExecutor<T>` repository'ga `findAll(Specification)`, `count(Specification)`, `findBy(Specification, Function)` metodlarini qo'shadi, `Specification.where(...).and(...).or(...).not()` esa kompozitsiya beradi. Spring Data MongoDB'da `Criteria` va `Query`, Querydsl integratsiyasida `QuerydslPredicateExecutor` va `BooleanExpression` xuddi shu rolni bajaradi; sof domenda esa `java.util.function.Predicate<T>` va uning `and/or/negate` metodlari yetarli.

**Qo'llanish keyslari:**
- Admin panelidagi dinamik qidiruv: foydalanuvchi to'ldirgan filter maydonlaridan runtime'da `Specification` yig'ish.
- Murakkab biznes qoidasini ("faol, KYC o'tgan va limitdan oshmagan mijoz") bitta nomli obyektga chiqarib, bir necha service'da qayta ishlatish.
- Multi-tenant yoki soft-delete kabi doimiy shartlarni baza `Specification` sifatida har bir query'ga qo'shish.
- Buyurtma chegirmaga loyiqligini aniqlash qoidalarini alohida testlanadigan sinflarga ajratish.
- Querydsl `BooleanExpression`lari orqali type-safe hisobot filtrlarini qurish.

**Ehtiyot bo'ling:** `Specification` ichida JPA Criteria API bilan ishlash tezda o'qishga qiyin kodga aylanadi, shuning uchun uni factory metodlar bilan nomlab yashirish kerak; shuningdek in-memory `Predicate` va baza `Specification` versiyalarini bir sinfda aralashtirish semantik farq (null, `LIKE` case-sensitivity, collation) tufayli xatolarga olib keladi.

## 3.14 Xizmatkor (Servant)

**Tavsif:** Bir guruh o'xshash obyektlarga xos bo'lgan xatti-harakatni ularning har biriga metod qo'shish orqali emas, balki tashqi "servant" sinfiga chiqarish patterni. Obyektlar faqat servant'ga kerak bo'lgan minimal interfeysni taqdim etadi, logika esa bitta joyda yashaydi. Bu Visitor'dan soddaroq: hech qanday double dispatch yo'q, servant shunchaki parametr sifatida obyektni oladi.

**Spring'da qayerda uchraydi:** Spring ekosistemida bu odatda `@Service` yoki `@Component` bo'lgan stateless helper bean ko'rinishida amalga oshiriladi: masalan `PasswordEncoder` (`BCryptPasswordEncoder`) `UserDetails` obyektlariga xizmat qiladi, `ConversionService`/`Converter<S,T>` turli DTO'larga, `Validator` (`org.springframework.validation.Validator` yoki Jakarta Bean Validation `jakarta.validation.Validator`) esa model obyektlariga xizmat qiladi. JDK'dagi `java.util.Collections` va `java.util.Arrays` ham klassik servant misollari.

**Qo'llanish keyslari:**
- Bir nechta entity uchun umumiy audit maydonlarini to'ldiruvchi `AuditStampService`.
- DTO va entity o'rtasida mapping qiluvchi stateless mapper bean (MapStruct generatsiya qilgan sinflar).
- Turli hisobot obyektlarini formatlovchi `ReportFormatter` beani.
- Domain obyektlariga tashqi API uchun imzo (signature) hisoblab beruvchi `SignatureCalculator`.
- Legacy entity'larni o'zgartirmasdan ularga yangi validatsiya qo'shish.

**Ehtiyot bo'ling:** Servant'ga juda ko'p mas'uliyat yuklasa, u anemik domen modeli va "god service" ga olib keladi - obyektning o'ziga tegishli invariantlar entity ichida qolishi kerak. Servant stateless bo'lishi shart, aks holda singleton bean sifatida thread-safety muammolari paydo bo'ladi.

## 3.15 Ravon interfeys (Fluent Interface)

**Tavsif:** Metodlar `this` yoki yangi obyekt qaytarib, chaqiruvlarni zanjir shaklida yozish imkonini beradigan API dizayni. Maqsad - kodni domen tiliga yaqin, o'qishga oson qilish va ko'p parametrli konstruktorlar yoki setter to'dasidan qutulish. Ko'pincha Builder bilan birga keladi, ammo fluent interface konfiguratsiya va query qurishda ham mustaqil ishlatiladi.

**Spring'da qayerda uchraydi:** Spring Framework 6.x bunga to'la: `RestClient.create().get().uri(...).retrieve().body(X.class)`, `WebClient`, `RestTemplateBuilder`, `MockMvcRequestBuilders.get("/x").param(...)`, `UriComponentsBuilder.fromUriString(...).queryParam(...).build()`. Spring Security 6.x'dagi lambda DSL (`http.authorizeHttpRequests(a -> a.requestMatchers("/admin/**").hasRole("ADMIN")).csrf(Customizer::withDefaults)`) va Spring Data'ning `Criteria`/`Query`, hamda Java Stream API ham shu uslubda.

**Qo'llanish keyslari:**
- Tashqi HTTP integratsiyalarini `RestClient` yoki `WebClient` zanjiri bilan o'qishga oson yozish.
- `SecurityFilterChain` konfiguratsiyasini lambda DSL orqali deklarativ tasvirlash.
- Test fixture'larini `OrderTestBuilder.anOrder().paid().withItems(3).build()` ko'rinishida yaratish.
- Murakkab URI va query parametrlarini `UriComponentsBuilder` bilan xavfsiz qurish.
- Domain-specific til ko'rinishidagi validatsiya yoki hisobot konfiguratsiyasi API'si.

**Ehtiyot bo'ling:** Mutable `this` qaytaradigan fluent obyekt shared holatda xavfli - har bir qadamda yangi immutable obyekt qaytarish ishonchliroq; shuningdek zanjir yarmida qolgan obyekt (`build()` chaqirilmagan) va noto'g'ri tartibda chaqirish mumkin bo'lgan API xatolarni compile-time'da emas, runtime'da yuzaga chiqaradi.

## 3.16 Callback (Callback)

**Tavsif:** Chaqiruvchi tomon o'z kodining bir qismini funksiya yoki interfeys implementatsiyasi sifatida boshqa komponentga uzatadi, u esa kerakli paytda uni chaqiradi. Bu nazoratni teskari aylantiradi (inversion of control): infratuzilma hayotiy siklni boshqaradi, biznes logikasi faqat "foydali ish"ni beradi. Sinxron (template metod ichida) yoki asinxron (natija kelganda chaqiriladigan handler) bo'lishi mumkin.

**Spring'da qayerda uchraydi:** `JdbcTemplate` ning `RowMapper`, `ResultSetExtractor`, `PreparedStatementSetter`, `ConnectionCallback` interfeyslari; `TransactionTemplate.execute(TransactionCallback)`; `RedisTemplate`/`RabbitTemplate` callback'lari; `KafkaTemplate.send(...).whenComplete(...)` (`CompletableFuture`); Spring Boot'ning `ApplicationRunner`/`CommandLineRunner`; lifecycle callback'lari sifatida `InitializingBean`, `DisposableBean`, `BeanPostProcessor`, `@PostConstruct`. Java tomonida `java.util.function.*` interfeyslari va `CompletableFuture.thenApply/exceptionally`.

**Qo'llanish keyslari:**
- `JdbcTemplate.query(sql, rowMapper)` bilan `ResultSet` ni domen obyektiga aylantirish.
- `TransactionTemplate` orqali faqat kerakli kod blokini programmatik transaksiyaga o'rash.
- Asinxron Kafka yoki HTTP so'rov natijasini `whenComplete` callback'ida qayta ishlash.
- Retry kutubxonasiga (`RetryTemplate.execute(RetryCallback)`) qayta bajarilishi kerak bo'lgan operatsiyani berish.
- Bean yaratilgandan keyin cache'ni oldindan to'ldirish uchun lifecycle callback.

**Ehtiyot bo'ling:** Asinxron callback'larni ketma-ket ulash "callback hell" va kuzatib bo'lmaydigan stack trace'larga olib keladi - reactive operator'lar yoki `CompletableFuture` kompozitsiyasi afzal. Callback ichida `ThreadLocal`ga tayanmang: transaksiya, `SecurityContext` va MDC asinxron thread'ga avtomatik ko'chmaydi.

## 3.17 Pipeline (obyekt darajasida) (Pipeline (object-level))

**Tavsif:** Ishlov berishni ketma-ket bosqichlarga (stage) ajratadi, har bir bosqich kirishni qabul qilib, chiqishni keyingisiga uzatadi. Chain of Responsibility'dan farqi - bu yerda maqsad so'rovni "kimga tegishli" ekanini aniqlash emas, balki ma'lumotni bosqichma-bosqich transformatsiya qilish. Bosqichlar mustaqil, almashtiriladigan va alohida testlanadigan bo'ladi.

**Spring'da qayerda uchraydi:** Spring Integration'ning `IntegrationFlow` DSL'i (`IntegrationFlow.from(...).transform(...).filter(...).handle(...)`) to'g'ridan-to'g'ri pipeline; Spring Batch'da `Step` ketma-ketligi va `CompositeItemProcessor`; Spring Cloud Stream'da `Function` kompozitsiyasi (`spring.cloud.function.definition=a|b|c`); `FilterChain`/`SecurityFilterChain` ham pipeline ko'rinishida. Sof Java'da `Function.andThen`/`compose`, Stream API va `Flux`/`Mono` operator zanjirlari.

**Qo'llanish keyslari:**
- ETL: faylni o'qish → validatsiya → boyitish (enrichment) → normalizatsiya → bazaga yozish.
- Spring Batch `CompositeItemProcessor` bilan har bir yozuvga bir nechta transformatsiya ketma-ket qo'llash.
- Kiruvchi webhook payload'ini dekodlash, imzoni tekshirish va kanonik eventga aylantirish.
- Hisobot generatsiyasi: ma'lumot yig'ish → agregatsiya → formatlash → eksport.
- Spring Cloud Stream'da bir nechta `Function` beanini `|` bilan birlashtirib stream pipeline qurish.

**Ehtiyot bo'ling:** Pipeline bosqichlari orasida mutable shared kontekst obyektini uzatish yashirin bog'lanish (coupling) yaratadi va bosqich tartibiga sezgir qiladi - immutable natija obyektlari afzal. Xatolik boshqaruvi va partial failure strategiyasini oldindan belgilang, aks holda pipeline o'rtasida uzilgan ish qayerda qolganini aniqlash qiyin bo'ladi.

## 3.18 Ikki tomonlama dispatch (Double Dispatch)

**Tavsif:** Chaqiriladigan metodni bitta emas, ikkita obyektning runtime turiga qarab tanlash mexanizmi. Java faqat bitta argument bo'yicha (receiver) virtual dispatch qiladi, shuning uchun ikkinchi dispatch odatda `accept(visitor)` → `visitor.visit(this)` ko'rinishidagi ikki bosqichli chaqiruv bilan erishiladi. Bu `instanceof` zanjirlari va qo'lda tur tekshiruvini yo'q qiladi.

**Spring'da qayerda uchraydi:** Spring'ning `BeanDefinitionVisitor`, `org.springframework.asm` va `MethodVisitor` asosidagi bytecode tahlili, hamda `org.springframework.expression`/SpEL AST ichidagi node'lar shu uslubda ishlaydi; `ApplicationListener<E extends ApplicationEvent>` va `@EventListener` esa event turi bo'yicha dispatchni `GenericApplicationListener`/`ResolvableType` orqali amalga oshiradi. Java 21+ dagi `sealed` interfeyslar va pattern matching `switch` ko'pincha klassik double dispatch o'rniga zamonaviy alternativa bo'lib xizmat qiladi.

**Qo'llanish keyslari:**
- To'lov usuli va valyuta kombinatsiyasiga qarab har xil komissiya hisoblash strategiyasini tanlash.
- Hujjat turi va eksport formati (PDF/XLSX/CSV) juftligiga mos renderer tanlash.
- AST yoki query daraxti node'lari ustida bir nechta xil "tashrifchi" (optimizator, validator, printer) ishlatish.
- Domain event turi va kanal (email/SMS/push) juftligi bo'yicha xabar shablonini aniqlash.
- Collision/interaksiya qoidalari: ikki xil obyekt turi uchrashganda nima bo'lishini aniqlash.

**Ehtiyot bo'ling:** Double dispatch tur kombinatsiyalari ko'paygan sayin N×M metodga o'sadi va yangi tur qo'shilganda barcha visitor'larni o'zgartirishga majbur qiladi; Java 21+ loyihalarda `sealed` iyerarxiya ustida pattern matching `switch` ko'pincha soddaroq va compile-time to'liqlik tekshiruvini (exhaustiveness) beradi.

## 3.19 Event agregatori (Event Aggregator)

**Tavsif:** Ko'p sonli publisher va subscriber o'rtasida bitta markaziy vositachi (hub) turadi; komponentlar bir-biriga emas, faqat agregatorga bog'lanadi. Bu N×M bog'lanishni N+M ga kamaytiradi va yangi tinglovchini mavjud kodga tegmasdan qo'shish imkonini beradi. Observer'dan farqi - subscription manbasi har bir publisher emas, yagona nuqta.

**Spring'da qayerda uchraydi:** Spring Framework'ning ichki event mexanizmi aynan shu: `ApplicationEventPublisher.publishEvent(...)`, `@EventListener`, `@TransactionalEventListener(phase = AFTER_COMMIT)`, `ApplicationEventMulticaster` (standart `SimpleApplicationEventMulticaster`, `taskExecutor` bilan asinxron qilish mumkin) va `@Async` bilan birga ishlatish. Tashqi masshtabda Spring Integration'ning `PublishSubscribeChannel`, Spring Cloud Bus, hamda Kafka/RabbitMQ topic'lari shu rolni bajaradi.

**Qo'llanish keyslari:**
- `OrderPlacedEvent` ni e'lon qilib, email yuborish, ombor zahirasini kamaytirish va analitikaga yozishni mustaqil listener'larga ajratish.
- Modulith arxitekturasida modullar o'rtasida to'g'ridan-to'g'ri bean injection o'rniga event orqali aloqa.
- `@TransactionalEventListener(AFTER_COMMIT)` bilan faqat transaksiya muvaffaqiyatli tugaganda tashqi tizimga xabar yuborish.
- Cache invalidatsiyasi: ma'lumot o'zgargani haqidagi eventni bir nechta cache egasi tinglashi.
- Domain audit log'ini biznes kodga aralashmasdan event tinglash orqali to'ldirish.

**Ehtiyot bo'ling:** Event oqimi oshgach tizim "kim nimani chaqirdi" ni kuzatish qiyin bo'lgan yashirin bog'lanishga aylanadi - muhim biznes oqimini faqat eventga tayanib qurmang. Standart `ApplicationEventMulticaster` sinxron va bir xil thread'da ishlaydi, shuning uchun listener ichidagi sekin yoki exception tashlagan kod publisher'ni ham bloklaydi yoki buzadi; asinxron qilganda transaksiya va `SecurityContext` propagatsiyasini alohida sozlash kerak.

## 3.20 O'rab bajarish (Execute Around)

**Tavsif:** Takrorlanadigan "oldin/keyin" kodni (resurs olish va yopish, transaksiya boshlash va yakunlash, vaqt o'lchash) bitta metodga yashirib, foydali ishni callback sifatida uning ichida bajaradi. Mijoz faqat o'zining logikasini yozadi, resurs boshqaruvi va xatolik tozalashi kafolatlangan holda markazda qoladi. Bu Template Method'ning kompozitsiyaga asoslangan, moslashuvchan varianti.

**Spring'da qayerda uchraydi:** `TransactionTemplate.execute(TransactionCallback)`, `JdbcTemplate.execute(ConnectionCallback)`, `JdbcClient` (Spring Framework 6.1+), `RetryTemplate.execute(...)`, `RedisTemplate.execute(SessionCallback)`, `TransactionalOperator.transactional(...)` (reactive). Deklarativ ko'rinishi - `@Transactional`, `@Cacheable`, `@Retryable`, `@Timed` annotatsiyalari, ular ostida Spring AOP `MethodInterceptor`/`@Around` advice ishlaydi. Java'da `try-with-resources` ham shu g'oyaning tilga kiritilgan shakli.

**Qo'llanish keyslari:**
- Programmatik transaksiya chegarasini aniq belgilash uchun `TransactionTemplate` ishlatish.
- Tashqi API chaqiruvini retry va timeout siyosati bilan o'rash.
- Metod bajarilish vaqtini va metrikalarni Micrometer `Timer` orqali o'lchash.
- Distributed lock olish, ish bajarish va lock'ni har qanday holatda bo'shatish.
- MDC'ga correlation ID qo'yib, blok tugagach uni tozalash.

**Ehtiyot bo'ling:** Callback ichida checked exception va natija turlarini to'g'ri uzatish (generic `<T>` bilan) oldindan o'ylanmasa, API noqulay bo'lib qoladi; shuningdek `@Transactional` kabi annotatsiya proxy orqali ishlaydi, shuning uchun bir sinf ichidagi self-invocation advice'ni butunlay chetlab o'tadi.

## 3.21 Chekli holatlar mashinasi (Finite State Machine (Spring Statemachine))

**Tavsif:** Obyektning mumkin bo'lgan holatlari, ular orasidagi o'tishlar va o'tishni qo'zg'atuvchi eventlarni aniq modellashtiradi. Biznes jarayoni (buyurtma, to'lov, ariza) `if/else` va boolean flag'lar o'rniga deklarativ holat diagrammasiga aylanadi, noto'g'ri o'tishlar esa markazda bloklanadi. Har bir o'tishga guard (shart) va action (yon ta'sir) bog'lash mumkin.

**Spring'da qayerda uchraydi:** Spring Statemachine (`org.springframework.statemachine`) moduli: `@EnableStateMachine`, `StateMachineConfigurerAdapter`, `StateMachine<S,E>`, `@WithStateMachine`, `@OnTransition`, guard va action uchun `Guard<S,E>`/`Action<S,E>`, hamda holatni saqlash uchun `StateMachinePersister` (JPA, Redis). Soddaroq holatlarda `enum`ga asoslangan o'z FSM'ingiz (`enum OrderState { ... abstract boolean canTransitionTo(OrderState) }`) yoki Spring Batch/Spring Integration oqimlari yetarli bo'ladi; `@Transactional` bilan birga holat o'zgarishi atomar saqlanadi.

**Qo'llanish keyslari:**
- Buyurtma hayotiy sikli: `CREATED → PAID → SHIPPED → DELIVERED`, qaytarish va bekor qilish tarmoqlari bilan.
- Kredit arizasini ko'p bosqichli tasdiqlash workflow'i (hujjat tekshiruvi, skoring, qo'lda tasdiq).
- To'lov tranzaksiyasi holatlari: authorized, captured, refunded, chargeback.
- KYC/onboarding jarayonini bosqichlar va har bosqichdagi ruxsat etilgan amallar bilan boshqarish.
- IoT yoki qurilma sessiyasining ulanish holatlarini kuzatish.

**Ehtiyot bo'ling:** Spring Statemachine qo'shimcha infratuzilma va o'rganish narxini keltiradi - oddiy 3-4 holatli oqim uchun `enum` asosidagi o'tish jadvali yetarli va osonroq. Holat mashinasi instance'i stateful, shuning uchun uni singleton bean sifatida bir necha request orasida ulashish xato: har bir biznes obyekt uchun alohida instance oling yoki `StateMachinePersister` bilan holatni bazadan tiklang.

## 3.22 Qoidalar dvigateli / Siyosat (Rules Engine / Policy)

**Tavsif:** Biznes qoidalarini kod shoxlari o'rniga deklarativ "shart → harakat" to'plami sifatida tashqariga chiqaradi va ularni dvigatel (engine) baholaydi. Qoidalar ko'p, tez-tez o'zgaradigan va biznes tomonidan boshqariladigan domenlarda deploy qilmasdan yoki minimal o'zgartirish bilan yangilash imkonini beradi. Policy varianti esa bitta qarorni (masalan, kim nimaga ruxsatli) almashtiriladigan obyektga kapsulalaydi.

**Spring'da qayerda uchraydi:** Spring'ning o'z SpEL mexanizmi (`org.springframework.expression.spel.standard.SpelExpressionParser`) oddiy qoidalarni matn sifatida baholash uchun ishlatiladi; Spring Security'da policy aniq ko'rinadi - `AuthorizationManager<T>`, `@PreAuthorize("hasRole('ADMIN') and #order.ownerId == authentication.name")`, `PermissionEvaluator`, `AccessDecisionManager` (legacy). Tashqi kutubxonalar: Drools (KIE `KieContainer`, `KieSession`), Easy Rules (`io.github.j-easy:easy-rules`), yoki Open Policy Agent'ga tashqi chaqiruv. Oddiy holatlarda `List<Rule>` bean kolleksiyasi va `@Order` bilan tartiblangan Spring bean'lar yetarli.

**Qo'llanish keyslari:**
- Chegirma va loyalty qoidalari: marketing tez-tez o'zgartiradigan shartlar to'plami.
- Firibgarlikka qarshi skoring: har bir qoida ball qo'shadi, yig'indi bo'yicha qaror qabul qilinadi.
- Kredit so'rovini avtomatik tasdiqlash/rad etish mezonlari.
- Spring Security `@PreAuthorize` va `AuthorizationManager` bilan murakkab ruxsat siyosatlari.
- Sug'urta tarifini mijoz profiliga qarab hisoblash qoidalari.

**Ehtiyot bo'ling:** To'laqonli rules engine (Drools) katta operatsion va bilim narxiga ega - qoidalar soni o'nlab bo'lsa, oddiy `Specification`/strategy bean'lar ancha tushunarli va tez. Qoidalarni matn (SpEL, skript) sifatida tashqi manbadan olish compile-time xavfsizlikni yo'qotadi va foydalanuvchi kiritgan ifodani baholash code injection xavfini tug'diradi, shuning uchun ishonchsiz kirishni hech qachon `SpelExpressionParser`ga bermang.

## 3.23 Qora taxta (Blackboard)

**Tavsif:** Aniq algoritmi yo'q murakkab masalalarni hal qilish uchun umumiy "qora taxta" (shared knowledge base) yaratiladi; mustaqil ekspert komponentlar (knowledge source) taxtadagi hozirgi holatni o'qib, o'z hissasini qo'shadi, nazoratchi (control) esa qaysi ekspertni qachon ishlatishni belgilaydi. Yechim bir yo'lda emas, bosqichma-bosqich, qisman natijalar to'planishi orqali shakllanadi. Nutq tanish, OCR, diagnostika va murakkab skoring tizimlarida qo'llanadi.

**Spring'da qayerda uchraydi:** Spring'da maxsus modul yo'q, lekin pattern tipik tarzda quriladi: umumiy holat uchun shared store (`RedisTemplate`, `CacheManager` yoki JPA entity), ekspertlar sifatida umumiy interfeysni implementatsiya qiluvchi bean'lar (`List<KnowledgeSource>` injection va `@Order`), nazoratchi sifatida orkestrator `@Service`, hamda qadamlar o'rtasidagi muvofiqlashtirish uchun `ApplicationEventPublisher` yoki Spring Integration `MessageChannel`. Spring Batch'ning `ExecutionContext` ham bosqichlar orasida qisman natijalarni ulashuvchi kichik "blackboard" sifatida xizmat qiladi.

**Qo'llanish keyslari:**
- Firibgarlikni aniqlash: qurilma, geolokatsiya, xatti-harakat va to'lov tarixi ekspertlari umumiy risk profilini to'ldiradi.
- Hujjatni qayta ishlash: OCR, til aniqlash, maydon ajratish va validatsiya bosqichlari natijalarini umumiy kontekstga yozish.
- Ko'p manbadan kelgan ma'lumotlarni (CRM, billing, support) birlashtirib mijozning yagona profilini shakllantirish.
- Monitoring/diagnostika tizimi: turli analizatorlar umumiy taxtaga gipotezalarni yozib, root cause ni aniqlash.
- Logistikada marshrutni bir nechta evristika yordamida bosqichma-bosqich yaxshilash.

**Ehtiyot bo'ling:** Blackboard mutable shared holatga asoslangani uchun concurrency, versiyalash va "qaysi ekspert nimani o'zgartirdi" muammolari darhol paydo bo'ladi - yozishni atomar qiling va har bir hissani kim qo'shganini qayd eting. Bu pattern faqat haqiqatan determinant algoritmi yo'q masalalar uchun; aniq ketma-ketlik ma'lum bo'lsa, oddiy Pipeline yoki orkestrlangan service ancha arzon va tushunarli.

---

[&larr; 2. Strukturaviy patternlar](02-strukturaviy-patternlar.md) · [Mundarija](README.md) · [4. Concurrency patternlari &rarr;](04-concurrency-patternlari.md)
