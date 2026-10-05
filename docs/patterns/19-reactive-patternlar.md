<!-- doc: patterns | chapter: 19 | part:  -->

[Barcha hujjatlar](../../README.md) / [Dizayn patternlar](README.md)

# 19. Reactive patternlar (Reactive Patterns)

<details>
<summary>Bu bo'limdagi 26 bo'lim</summary>

- [19.1 Reactive Streams (Reactive Streams)](#191-reactive-streams-reactive-streams)
- [19.2 Backpressure strategiyalari (Backpressure Strategies)](#192-backpressure-strategiyalari-backpressure-strategies)
- [19.3 Event Loop (Event Loop)](#193-event-loop-event-loop)
- [19.4 Bloklanmaydigan I/O (Non-blocking I/O)](#194-bloklanmaydigan-io-non-blocking-io)
- [19.5 Mono va Flux (Mono / Flux)](#195-mono-va-flux-mono--flux)
- [19.6 Hot va Cold publisher'lar (Hot vs Cold Publishers)](#196-hot-va-cold-publisherlar-hot-vs-cold-publishers)
- [19.7 Scheduler'lar (Schedulers: publishOn / subscribeOn)](#197-schedulerlar-schedulers-publishon--subscribeon)
- [19.8 Reactor Context va context propagation (Reactor Context & Context Propagation)](#198-reactor-context-va-context-propagation-reactor-context--context-propagation)
- [19.9 Operatorlar kompozitsiyasi (Operator Composition)](#199-operatorlar-kompozitsiyasi-operator-composition)
- [19.10 Qayta urinish, timeout va fallback (Retry / Timeout / Fallback)](#1910-qayta-urinish-timeout-va-fallback-retry--timeout--fallback)
- [19.11 Reactive repository'lar (Reactive Repositories)](#1911-reactive-repositorylar-reactive-repositories)
- [19.12 WebClient (WebClient)](#1912-webclient-webclient)
- [19.13 WebFlux funksional endpoint'lar (WebFlux Functional Endpoints)](#1913-webflux-funksional-endpointlar-webflux-functional-endpoints)
- [19.14 Oqimli javoblar (Streaming Responses - SSE, NDJSON)](#1914-oqimli-javoblar-streaming-responses---sse-ndjson)
- [19.15 Reactive Security](#1915-reactive-security)
- [19.16 Reactive tranzaksiyalar (Reactive Transactions)](#1916-reactive-tranzaksiyalar-reactive-transactions)
- [19.17 Blocking chaqiruvlarni aniqlash (Blocking Call Detection - BlockHound)](#1917-blocking-chaqiruvlarni-aniqlash-blocking-call-detection---blockhound)
- [19.18 Blocking kodni ko'prikka olish (Bridging Blocking Code - boundedElastic)](#1918-blocking-kodni-koprikka-olish-bridging-blocking-code---boundedelastic)
- [19.19 Sinks (Reactive Event Bus - Sinks)](#1919-sinks-reactive-event-bus---sinks)
- [19.20 Reactive Kafka (reactor-kafka)](#1920-reactive-kafka-reactor-kafka)
- [19.21 Reactive va Virtual Threads tanlovi (Reactive vs Virtual Threads Decision)](#1921-reactive-va-virtual-threads-tanlovi-reactive-vs-virtual-threads-decision)
- [19.22 Reactive Manifesto tamoyillari (Reactive Manifesto Principles)](#1922-reactive-manifesto-tamoyillari-reactive-manifesto-principles)
- [19.23 java.util.concurrent.Flow](#1923-javautilconcurrentflow)
- [19.24 Observable / Reactive Extensions merosi (Observable / Reactive Extensions Heritage)](#1924-observable--reactive-extensions-merosi-observable--reactive-extensions-heritage)
- [19.25 Sovuq start va subscription hayot sikli (Cold Start & Subscription Lifecycle)](#1925-sovuq-start-va-subscription-hayot-sikli-cold-start--subscription-lifecycle)
- [19.26 Amalda qo'llash](#1926-amalda-qollash)

</details>



Reactive patternlar - bu bloklanmaydigan (non-blocking), hodisaga asoslangan va backpressure'ni hisobga oladigan asinxron oqimlar bilan ishlash uslubi: thread'ni kutib turishga sarflash o'rniga, ma'lumot tayyor bo'lganda callback/signal orqali ishlov beriladi. Arxitektor uchun bu muhim, chunki I/O-bound yuklamalarda (ko'p sonli tashqi API chaqiriqlari, streaming, SSE/WebSocket, uzoq muddatli ulanishlar) thread-per-request modeli xotira va kontekst almashinuvi bo'yicha qimmatga tushadi, reactive model esa bir nechta event loop thread bilan o'n minglab bir vaqtdagi ulanishni ushlab turadi. Shu bilan birga reactive stack butun zanjirni (driver, repository, security, logging, tracing) qamrab olmasa, foydasi yo'qoladi - bitta blocking chaqiriq event loop'ni muzlatib qo'yadi. Shuning uchun quyidagi patternlar nafaqat API'ni, balki qaror qabul qilish mezonlarini ham belgilaydi: qachon reactive, qachon virtual thread'lar yoki oddiy imperativ MVC yetarli.

## 19.1 Reactive Streams (Reactive Streams)

**Tavsif:** Reactive Streams - asinxron oqim uzatish uchun to'rtta interfeysdan iborat minimal standart: `Publisher`, `Subscriber`, `Subscription`, `Processor`. Asosiy g'oya shundaki, ma'lumotni producer "turtib" (push) yubormaydi, balki consumer `Subscription.request(n)` orqali qancha element qabul qilishga tayyorligini aytadi - bu pull-push gibridi backpressure'ni protokol darajasida ta'minlaydi. Signal ketma-ketligi qat'iy: `onSubscribe` bir marta, so'ngra `onNext`\* va oxirida `onComplete` yoki `onError` (terminal signal faqat bittasi). Bu standart turli kutubxonalar (Reactor, RxJava, Akka Streams, R2DBC driverlari) o'zaro muvofiq ishlashini ta'minlaydi.

**Spring'da qayerda uchraydi:** Java 9'dan boshlab bu interfeyslar JDK ichida `java.util.concurrent.Flow.Publisher/Subscriber/Subscription/Processor` sifatida mavjud; `org.reactivestreams` artifaktidagi asl interfeyslar hamon keng ishlatiladi va `reactor.adapter.JdkFlowAdapter` ikkisini bog'laydi. Spring Framework 6.x/7.x'da `ReactiveAdapterRegistry` turli reactive tiplarni (Reactor, RxJava 3, Mutiny, `Flow.Publisher`) umumiy `Publisher`ga keltiradi, shu sababli WebFlux controller'i `Flux`, `Observable` yoki `Flow.Publisher` qaytarsa ham ishlaydi. Reactor'dagi `Flux`/`Mono` - bu `Publisher`ning implementatsiyasi, `BaseSubscriber` esa qo'lda subscriber yozish uchun xavfsiz baza. `reactive-streams-tck` moduli o'z Publisher'ingizning spetsifikatsiyaga mosligini tekshiradi.

**Qo'llanish keyslari:**
- Turli reactive kutubxonalardan (RxJava'da yozilgan modul va Reactor'da yozilgan servis) iborat tizimlarda umumiy integratsiya nuqtasi sifatida.
- Kafka/Pulsar consumer'ini `Publisher` sifatida o'rab, pastki qismdagi iste'molchi tezligiga moslashtirish.
- R2DBC drayveri qaytargan natija oqimini servis qatlamiga standart signal protokoli bilan uzatish.
- Custom `Processor` yozib, legacy callback-based SDK'ni reactive pipeline'ga adapter qilish.
- Kutubxona API'sini `Publisher` qaytaradigan qilib e'lon qilish - iste'molchi o'zi yoqtirgan reactive kutubxonani tanlaydi.

**Ehtiyot bo'ling:** `Publisher`ni qo'lda implementatsiya qilish spetsifikatsiya qoidalarini (signal tartibi, thread-safety, `request(n)` hisobi, cancel'dan keyin signal yubormaslik) buzish xavfi juda yuqori - `Flux.create`/`Flux.push`/`Sinks` kabi tayyor fabrikalardan foydalanish xavfsizroq. Shuningdek, `Processor` interfeysi Reactor 3.5'dan boshlab deprecated hisoblanadi; uning o'rniga `Sinks.many()` API'si ishlatiladi.

## 19.2 Backpressure strategiyalari (Backpressure Strategies)

**Tavsif:** Backpressure - producer consumer'dan tez ma'lumot ishlab chiqarganda tizimni OOM'dan va cheksiz kechikishdan saqlash mexanizmi. Agar manba `request(n)`ga bo'ysunmasa (masalan, taymer, sensor, WebSocket oqimi), oraliqda qaror qabul qilish kerak: elementlarni buffer'ga yig'ish, yangilarini tashlab yuborish (drop), faqat oxirgisini saqlash (latest), ortiqchasini e'tiborsiz qoldirish (ignore) yoki xatolik bilan to'xtash (error). Har bir strategiya ma'lumot to'liqligi, xotira va kechikish o'rtasidagi savdoni (trade-off) ifodalaydi. Tanlov domen talabidan kelib chiqadi: to'lov hodisalarini tashlab bo'lmaydi, narx tickerining esa faqat oxirgi qiymati muhim.

**Spring'da qayerda uchraydi:** Reactor'da `FluxSink.OverflowStrategy` (BUFFER, DROP, LATEST, ERROR, IGNORE) `Flux.create(...)` va `Flux.push(...)`da beriladi; operator shaklida `onBackpressureBuffer(int, Consumer, BufferOverflowStrategy)`, `onBackpressureDrop(Consumer)`, `onBackpressureLatest()`, `onBackpressureError()` mavjud. `Sinks.many().multicast().onBackpressureBuffer(...)` va `Sinks.many().replay().limit(...)` sink darajasida bufer siyosatini belgilaydi. Tezlikni moslashtirish uchun `limitRate(n)`, `limitRequest(n)`, `buffer(Duration)`, `sample(Duration)`, `window(...)` operatorlari ishlatiladi. Spring Cloud Stream'ning reactive binder'i va `ReactiveKafkaConsumerTemplate` ham shu operatorlarga tayanadi.

**Qo'llanish keyslari:**
- IoT/telemetriya oqimida `onBackpressureLatest()` bilan faqat eng yangi sensor qiymatini saqlash.
- Birja narxlari dashboard'ida `sample(Duration.ofMillis(250))` orqali UI'ni ortiqcha yangilashdan saqlash.
- Audit/to'lov hodisalarida chegaralangan `onBackpressureBuffer(10_000, this::alert, DROP_OLDEST)` bilan yo'qotishni nazorat qilish.
- Sekin tashqi API'ga murojaatda `limitRate(50)` bilan prefetch oynasini kichraytirish va rate limit'ga tushib qolmaslik.
- Tez oqimni `buffer(500)` bilan batch'lab, bazaga ommaviy (bulk) yozish.

**Ehtiyot bo'ling:** Standart `onBackpressureBuffer()` chegarasiz - u xotirani asta-sekin yeb, OOM'ga olib keladi; har doim hajm va overflow siyosatini aniq ko'rsating. Shuningdek, backpressure "sekinlashtirish" degani emas: agar manba haqiqiy pull'ni qo'llab-quvvatlamasa (vaqtga bog'liq hodisalar), element yo'qotish yoki xatolik muqarrar - bu domen qarori, texnik detal emas.

## 19.3 Event Loop (Event Loop)

**Tavsif:** Event loop - oz sonli thread'lar cheksiz tsiklda tayyor bo'lgan I/O hodisalarini (selector readiness) olib, ularga mos handler'larni navbat bilan bajaradigan model. Thread-per-request'dan farqi: ulanish soni thread soniga bog'lanmaydi, shuning uchun o'n minglab bir vaqtdagi ulanish bir necha MB stack bilan emas, balki kichik event queue bilan boshqariladi. Netty'da har bir `EventLoop` bitta thread'ga bog'langan va unga biriktirilgan kanallarning (channel) butun hayot sikli shu thread'da kechadi - bu lock'siz, thread-affinity'ga asoslangan dizaynni beradi. Natijada I/O-bound yuklamalarda throughput va xotira samaradorligi sezilarli oshadi.

**Spring'da qayerda uchraydi:** Spring Boot 3.x/4.x'dagi `spring-boot-starter-webflux` standart holatda Netty'ni ko'taradi (`NettyReactiveWebServerFactory`, `ReactorNetty` `HttpServer`); thread'lar nomi `reactor-http-nio-N` ko'rinishida bo'ladi va soni standart holatda CPU yadrolari soniga teng (`reactor.netty.ioWorkerCount` bilan boshqariladi). `NettyServerCustomizer` va `ReactorResourceFactory` orqali `LoopResources`ni (umumiy yoki alohida event loop guruhi) sozlash mumkin. Client tomonida `WebClient` `ReactorClientHttpConnector` orqali xuddi shu `LoopResources`ni ulashadi. Alternativ sifatida WebFlux Undertow, Tomcat yoki Jetty'ning Servlet 3.1+ async non-blocking I/O'si ustida ham ishlay oladi.

**Qo'llanish keyslari:**
- Minglab SSE yoki WebSocket ulanishini ushlab turadigan notification gateway.
- API gateway / BFF: har bir so'rovda bir nechta downstream servisga parallel chaqiriq.
- Long-polling va chat backend'lari - ulanishlar uzoq, lekin CPU ishi kam.
- Proxy va streaming yuklash/yuklab olish servislari (katta fayllarni xotiraga to'liq yig'masdan uzatish).
- Yuqori RPS'li, lekin yengil ishlov beradigan edge servis (header boyitish, auth tekshirish, routing).

**Ehtiyot bo'ling:** Event loop thread'ida bloklovchi chaqiriq (JDBC, `Thread.sleep`, sinxron HTTP client, og'ir CPU hisob) bajarilsa, o'sha thread'ga biriktirilgan BARCHA ulanishlar muzlaydi - `BlockHound`ni test profilida yoqib, bunday chaqiriqlarni erta aniqlash kerak. Event loop thread'lari sonini "ko'paytirsam tezlashadi" degan taxmin bilan oshirish ham samarasiz: muammo odatda bloklanishda, thread sonida emas.

## 19.4 Bloklanmaydigan I/O (Non-blocking I/O)

**Tavsif:** Non-blocking I/O'da socket'dan o'qish/yozish chaqiriqlari ma'lumot tayyor bo'lishini kutib thread'ni to'xtatmaydi; o'rniga darhol qaytadi va readiness haqida selector/callback xabar beradi. Bu "thread kutmaydi, xabar keladi" modeli thread'ni faqat haqiqiy ish bor paytda band qiladi, natijada kam thread bilan ko'p ulanishga xizmat qilish imkoni tug'iladi. Reactive stack bu modelni butun zanjir bo'ylab talab qiladi: HTTP server, HTTP client, DB driver va serializatsiya ham non-blocking bo'lishi kerak. Aks holda eng sekin bloklovchi bo'g'in butun afzallikni yo'qotadi.

**Spring'da qayerda uchraydi:** Asosida `java.nio.channels.Selector`/`SocketChannel` va Netty'ning `NioEventLoopGroup`i yotadi. Spring tomonida `ServerHttpRequest`/`ServerHttpResponse` (`org.springframework.http.server.reactive`) tanani `Flux<DataBuffer>` sifatida ifodalaydi, `DataBufferUtils` esa bufer hayot siklini boshqaradi. `spring-webflux`dagi `HttpHandler`, `WebFilter`, `WebHandler` zanjiri to'liq non-blocking; `DispatcherHandler` esa `DispatcherServlet`ning reactive muqobili. Ma'lumot bazasi uchun R2DBC (`io.r2dbc` driverlari), Mongo uchun `MongoDB Reactive Streams Driver`, Redis uchun Lettuce non-blocking transport beradi. Java 21+ virtual thread'lar (`spring.threads.virtual.enabled=true`) esa bloklovchi kod bilan ham arzon konkurentlik beradigan alternativ yo'l.

**Qo'llanish keyslari:**
- Ko'p sonli tashqi HTTP integratsiyasi bo'lgan aggregator servisda thread pool tugashini oldini olish.
- Katta fayllarni `Flux<DataBuffer>` orqali streaming yuklash - xotira iste'moli fayl hajmiga bog'lanmaydi.
- Kontainerda kichik xotira limiti (masalan 256-512 MB) bilan yuqori konkurentlikni ushlab turish.
- Database natijalarini kursor bo'yicha oqim sifatida mijozga uzatish (streaming export).
- Reverse proxy yoki sidecar-ga o'xshash ko'p ulanishli, kam hisobli komponentlar.

**Ehtiyot bo'ling:** `DataBuffer`lar pool'dan olinadi - ularni iste'mol qilmasangiz yoki `DataBufferUtils.release(...)` qilmasangiz xotira leak bo'ladi; shuning uchun request body'ni o'qimay tashlab yuborish ham xavfli. Shu bilan birga, CPU-bound yoki kodingiz baribir JDBC'ga tayanadigan holatlarda non-blocking I/O deyarli hech narsa bermaydi - bunday paytda virtual thread'lar bilan oddiy MVC ko'proq mos keladi.

## 19.5 Mono va Flux (Mono / Flux)

**Tavsif:** `Mono<T>` - 0 yoki 1 element qaytaradigan asinxron natija, `Flux<T>` - 0..N elementli oqim; ikkisi ham `Publisher` implementatsiyasi va boy operator to'plamiga ega. Ular natijani emas, balki hisoblash retseptini ifodalaydi: `subscribe()` qilinmaguncha hech narsa bajarilmaydi (lazy). Bu `CompletableFuture`dan ikki jihati bilan farq qiladi - birinchisi lazy (future esa odatda eager), ikkinchisi backpressure va ko'p elementli oqimni qo'llab-quvvatlaydi. Tip tanlovi API kontraktining bir qismi: `Mono<Void>` "tugadi" signalini, `Flux<T>` esa potentsial cheksiz oqimni anglatadi.

**Spring'da qayerda uchraydi:** `reactor.core.publisher.Mono` va `reactor.core.publisher.Flux` (Reactor 3.6+/3.7+, Spring Framework 6.x/7.x bilan keladi). WebFlux controller'lari `Mono<ResponseEntity<T>>`, `Flux<T>` qaytaradi; `WebClient` `Mono<ClientResponse>`/`bodyToFlux(...)` beradi; `ReactiveCrudRepository` `Mono`/`Flux` qaytaradi; `ReactiveRedisTemplate`, `ReactiveMongoTemplate`, `R2dbcEntityTemplate`, `ReactiveTransactionManager`, `ReactiveAuthenticationManager` ham shu tiplarga tayanadi. `Mono.fromCallable(...)`, `Flux.fromIterable(...)`, `Mono.defer(...)`, `Flux.interval(...)` asosiy fabrikalar; `block()` esa reactive dunyodan imperativ dunyoga chiqish uchun (testdan tashqarida ehtiyotkorlik bilan).

**Qo'llanish keyslari:**
- Bitta entity'ni ID bo'yicha olish uchun `Mono<User>`, ro'yxat uchun `Flux<User>` qaytaradigan servis API'si.
- `Mono.zip(...)` bilan uchta downstream chaqiriqni parallel bajarib, javobni birlashtirish.
- `Flux` + `MediaType.TEXT_EVENT_STREAM` orqali SSE kanali ochish.
- `Mono<Void>` bilan "fire and complete" operatsiyalar (delete, publish) kontraktini ifodalash.
- `Flux.interval(...)` asosida davriy health/poll vazifalarini reactive pipeline ichida yuritish.

**Ehtiyot bo'ling:** `Mono`/`Flux` lazy bo'lgani uchun `subscribe()` yoki framework tomonidan iste'mol qilinmasa kod umuman ishlamaydi - "metodni chaqirdim, lekin hech narsa bo'lmadi" muammosining asosiy sababi shu. `block()`ni event loop thread'ida chaqirmang: Reactor bunda `IllegalStateException` tashlaydi yoki deadlock yuzaga keladi.

## 19.6 Hot va Cold publisher'lar (Hot vs Cold Publishers)

**Tavsif:** Cold publisher har bir subscriber uchun ishni boshidan qayta boshlaydi - masalan HTTP chaqiriq yoki DB so'rovi har bir subscription'da yangidan bajariladi va har kim to'liq ketma-ketlikni oladi. Hot publisher esa manbadan mustaqil ravishda ma'lumot ishlab chiqaradi va subscriber faqat ulangandan keyingi elementlarni ko'radi (late subscriber oldingi qiymatlarni o'tkazib yuboradi). Bu farq keshlash, qayta urinish va multicast semantikasini butunlay o'zgartiradi. Arxitektor darajasida bu "manba takrorlanadimi yoki real vaqt hodisasimi" degan savolga javob beradi.

**Spring'da qayerda uchraydi:** Cold misollari: `Flux.fromIterable`, `Mono.fromCallable`, `WebClient.get()...retrieve()` natijasi, `ReactiveCrudRepository.findAll()`. Hot/multicast uchun Reactor'da `Sinks.many().multicast().onBackpressureBuffer()`, `Sinks.many().replay().limit(n)`, `Sinks.one()`, hamda `share()`, `publish().refCount(n)`, `cache(Duration)`, `replay(n)` operatorlari bor. Spring tomonida `ReactiveRedisMessageListenerContainer`, Reactor Kafka'ning `KafkaReceiver`, `ApplicationEventPublisher`ga ulangan sink'lar odatda hot oqim yaratadi. `ConnectableFlux` esa qo'lda `connect()` chaqirib boshlanadigan hot oqimni ifodalaydi.

**Qo'llanish keyslari:**
- Bir nechta SSE mijoziga bitta ichki hodisa oqimini `Sinks.many().multicast()` orqali tarqatish.
- Qimmat konfiguratsiya chaqirig'ini `cache(Duration.ofMinutes(5))` bilan cold'dan quasi-hot keshga aylantirish.
- Chat yoki presence tizimida faqat ulangandan keyingi xabarlarni yuborish (replay qilmaslik).
- `replay(1)` bilan oxirgi holatni yangi subscriber'ga darhol berish (masalan feature flag holati).
- Bitta downstream so'rovini bir nechta parallel pipeline'da `share()` bilan qayta ishlatish.

**Ehtiyot bo'ling:** Cold publisher'ni ikki marta subscribe qilish ikki marta yon ta'sir (ikkita POST, ikkita INSERT) degani - qayta urinish yoki `Mono.zip` ichida ehtiyot bo'ling. Teskarisi ham xavfli: hot oqimda `retry()` yo'qolgan elementlarni qaytarmaydi, shuning uchun at-least-once kafolat kerak bo'lsa broker darajasida offset/ack'ka tayanish zarur.

## 19.7 Scheduler'lar (Schedulers: publishOn / subscribeOn)

**Tavsif:** Reactor thread'ni o'zi tanlamaydi - kod subscribe qilingan thread'da ishlaydi, scheduler'lar esa bu xatti-harakatni ataylab o'zgartirish vositasidir. `subscribeOn(scheduler)` butun zanjirning subscription (manba) tomonini ko'rsatilgan scheduler'ga ko'chiradi va joylashuvidan qat'i nazar bir marta ta'sir qiladi. `publishOn(scheduler)` esa o'zidan KEYINGI operatorlarni boshqa thread'ga o'tkazadi, ya'ni zanjirni nuqta-nuqta bo'lib qismlarga ajratadi. To'g'ri tanlov bloklovchi legacy kodni ajratish va CPU-bound ishni event loop'dan uzoqlashtirish uchun kalit.

**Spring'da qayerda uchraydi:** `reactor.core.scheduler.Schedulers` fabrikalari: `parallel()` (CPU-bound, cheklangan thread), `boundedElastic()` (bloklovchi chaqiriqlar uchun, Reactor 3.6+ da virtual thread variantini `Schedulers.boundedElastic()` konfiguratsiyasi yoki `Schedulers.fromExecutor(Executors.newVirtualThreadPerTaskExecutor())` bilan olish mumkin), `single()`, `immediate()`, `newParallel(...)`. Testda `VirtualTimeScheduler` va `StepVerifier.withVirtualTime(...)` vaqtni tezlashtirish uchun ishlatiladi. Spring Boot'da `spring.threads.virtual.enabled` virtual thread'larni yoqadi, `BlockHound` esa noto'g'ri thread'dagi bloklanishni aniqlaydi. `Mono.fromCallable(...).subscribeOn(Schedulers.boundedElastic())` - JDBC yoki legacy SDK'ni o'rash uchun standart idioma.

**Qo'llanish keyslari:**
- Legacy JDBC repository'ni `boundedElastic()` da o'rab, WebFlux controller'dan xavfsiz chaqirish.
- Rasm/PDF qayta ishlash kabi CPU-bound bosqichni `publishOn(Schedulers.parallel())` bilan event loop'dan chiqarish.
- Fayl tizimi bilan ishlovchi bloklovchi `java.io` kodini alohida scheduler'ga izolyatsiya qilish.
- `Flux.interval(...)`ning standart `parallel` scheduler'ini aniq `newParallel("poller", 2)` bilan almashtirib, izolyatsiya berish.
- Testda `VirtualTimeScheduler` bilan `delayElements(Duration.ofHours(1))` mantiqini millisekundda tekshirish.

**Ehtiyot bo'ling:** `boundedElastic()` cheksiz emas - standart chegarasi CPU×10 thread va navbat; uni "universal yechim" sifatida hamma joyga qo'yish bloklovchi kodni yashirib, kutilmagan navbat kechikishini keltiradi. Shuningdek zanjirda bir nechta `subscribeOn` bo'lsa faqat eng yaqin manbaga tegishlisi ta'sir qiladi - bu ko'p uchraydigan chalkashlik manbai.

## 19.8 Reactor Context va context propagation (Reactor Context & Context Propagation)

**Tavsif:** Reactive pipeline'da ish turli thread'larda bajarilgani uchun `ThreadLocal` ishonchsiz bo'ladi; Reactor buning o'rniga subscription'ga bog'langan immutable key-value xaritasi - `Context`ni beradi. Context pastdan yuqoriga (subscriber'dan manbaga) tarqaladi, shuning uchun u zanjirning oxirida yozilib, operatorlar tomonidan o'qiladi. Bu tenant ID, correlation ID, security principal va locale kabi cross-cutting ma'lumotni thread'dan mustaqil uzatish imkonini beradi. `context-propagation` kutubxonasi esa Context va `ThreadLocal` dunyolari o'rtasida ko'prik quradi.

**Spring'da qayerda uchraydi:** `reactor.util.context.Context`/`ContextView`, `Mono.deferContextual(...)`, `Flux.contextWrite(...)`, `Mono.contextWrite(Context.of(k, v))`. `io.micrometer:context-propagation` (`ContextRegistry`, `ContextSnapshot`) Reactor 3.5+ va Micrometer Tracing bilan birga ishlaydi; `Hooks.enableAutomaticContextPropagation()` ThreadLocal'larni avtomatik ko'chiradi. Spring Security reactive stack'da `ReactiveSecurityContextHolder.getContext()` aynan Reactor Context ustiga qurilgan; Micrometer Observation (`ObservationThreadLocalAccessor`) trace ID'ni uzatadi; MDC uchun `MDCContextAccessor` yoki `contextWrite` + `doOnEach` idiomasi ishlatiladi.

**Qo'llanish keyslari:**
- Multi-tenant SaaS'da tenant ID'ni `WebFilter`da Context'ga yozib, repository qatlamida o'qish.
- Correlation/trace ID'ni log'larga chiqarish uchun MDC bilan sinxronlash.
- `ReactiveSecurityContextHolder`dan foydalanuvchi principal'ini servis chuqurligida olish.
- Request-scoped feature flag yoki A/B variant kalitini butun zanjir bo'ylab uzatish.
- Testda `contextWrite` bilan soxta foydalanuvchi/tenant qo'yib, pipeline xatti-harakatini tekshirish.

**Ehtiyot bo'ling:** Context pastdan yuqoriga tarqalgani uchun `contextWrite`ni zanjirning BOSHIGA qo'yish ko'p uchraydigan xato - uni zanjir oxirida (subscribe nuqtasiga yaqin) yozish kerak, aks holda yuqoridagi operatorlar qiymatni ko'rmaydi. `ThreadLocal`ga tayangan legacy kodni (MDC, `SecurityContextHolder`) avtomatik propagation yoqilmagan holda reactive zanjirda ishlatish esa jim xatolarga - bo'sh tenant yoki aralashgan log'larga olib keladi.

## 19.9 Operatorlar kompozitsiyasi (Operator Composition)

**Tavsif:** Reactive pipeline - manba, bir qator transformatsiya operatorlari va terminal subscriber'dan iborat deklarativ zanjir; har bir operator yangi `Publisher` qaytaradi va mutatsiya qilmaydi. Asosiy mahorat to'g'ri operatorni tanlashda: `map` sinxron o'girish, `flatMap` asinxron va tartibsiz kengaytirish, `concatMap` tartibni saqlash, `flatMapSequential` parallel bajarib tartibli chiqarish, `switchMap` oldingisini bekor qilish. Kompozitsiya qayta ishlatilishi uchun `transform`/`transformDeferred` va `as` operatorlari bilan nomlangan bloklarga ajratiladi. Yaxshi tuzilgan pipeline imperativ callback do'zaxini o'qiladigan oqim diagrammasiga aylantiradi.

**Spring'da qayerda uchraydi:** Reactor operatorlari `Flux`/`Mono` API'sida: `map`, `filter`, `flatMap(f, concurrency)`, `concatMap`, `switchMap`, `zip`, `zipWhen`, `then`, `thenMany`, `expand`, `groupBy`, `window`, `buffer`, `distinct`, `takeUntil`, `doOnNext`, `doFinally`, `handle`. Xatolarni kuzatish uchun `checkpoint("name")` va `Hooks.onOperatorDebug()` (yoki `reactor-tools`ning `ReactorDebugAgent`) ishlatiladi. Spring kontekstida bu zanjirlar `@Service` metodlarida, `WebClient` javobini qayta ishlashda, `RouterFunction` handler'larida va `ReactiveMongoTemplate` natijalari ustida quriladi. `StepVerifier` (`reactor-test`) esa butun zanjirni signal-signal tekshiradi.

**Qo'llanish keyslari:**
- Mijoz ro'yxatini olib, har biri uchun `flatMap` bilan parallel profil chaqirig'i qilish (`concurrency` chegarasi bilan).
- Tartib muhim bo'lgan ledger hodisalarini `concatMap` bilan ketma-ket ishlash.
- Foydalanuvchi qidiruvida `switchMap` orqali eski so'rovni avtomatik bekor qilish.
- `groupBy` + `window` bilan hodisalarni tenant bo'yicha guruhlab, batch agregatsiya qilish.
- `transform(this::withMetrics)` bilan umumiy metrika/logging bloklarini bir nechta pipeline'da qayta ishlatish.

**Ehtiyot bo'ling:** Chegarasiz `flatMap` standart holatda 256 tagacha ichki subscription ochadi - downstream servisni DDoS qilib qo'yish mumkin, shuning uchun `flatMap(f, n)` bilan konkurentlikni aniq belgilash kerak. `doOnNext` ichida bloklovchi yoki yon ta'sirli kod yozish va `map` ichida `Mono` qaytarish (`Mono<Mono<T>>` paydo bo'lishi) ham tez-tez uchraydigan xatolar.

## 19.10 Qayta urinish, timeout va fallback (Retry / Timeout / Fallback)

**Tavsif:** Tarmoqqa tayangan reactive pipeline'da vaqtinchalik xatolar normal holat, shuning uchun bardoshlilik operatorlari zanjirning bir qismi bo'lishi kerak. `retryWhen` exponential backoff va jitter bilan takroriy urinishni, `timeout` esa osilib qolgan chaqiriqni cheklashni beradi; `onErrorResume`/`onErrorReturn` esa degradatsiya qilingan javob qaytaradi. Muhim nuqta: faqat idempotent va "transient" xatolar qayta urinilishi kerak (5xx, ulanish uzilishi), 4xx esa darhol yuqoriga uzatiladi. Circuit breaker bilan birlashtirilganda bu pattern kaskad buzilishini oldini oladi.

**Spring'da qayerda uchraydi:** Reactor'da `Retry.backoff(3, Duration.ofMillis(200)).jitter(0.5).filter(this::isTransient).transientErrors(true)` va `retryWhen(...)`, `timeout(Duration, Mono fallback)`, `onErrorResume`, `onErrorMap`, `onErrorComplete`, `defaultIfEmpty`, `switchIfEmpty`. Resilience4j'ning reactive operatorlari `CircuitBreakerOperator`, `RateLimiterOperator`, `BulkheadOperator`, `TimeLimiter` `transformDeferred(...)` bilan zanjirga qo'shiladi; Spring Cloud CircuitBreaker'da `ReactiveCircuitBreakerFactory` mavjud. `WebClient` darajasida `HttpClient.responseTimeout(...)` va `ReactorClientHttpConnector` orqali ulanish/o'qish timeout'lari beriladi. Spring Cloud Gateway'da esa `Retry` va `CircuitBreaker` filtrlari deklarativ sozlanadi.

```java
Mono<Quote> quote = webClient.get().uri("/quote/{id}", id)
    .retrieve().bodyToMono(Quote.class)
    .timeout(Duration.ofSeconds(2))
    .retryWhen(Retry.backoff(3, Duration.ofMillis(200))
        .jitter(0.5)
        .filter(ex -> ex instanceof WebClientRequestException))
    .transformDeferred(CircuitBreakerOperator.of(breaker))
    .onErrorResume(ex -> cache.lastKnown(id));
```

**Qo'llanish keyslari:**
- Downstream 503 qaytarganda backoff+jitter bilan uch marta urinish va keyin keshdagi qiymatga tushish.
- To'lov provayderi javob bermasa `timeout(2s)` bilan so'rovni uzib, foydalanuvchiga aniq xato berish.
- `switchIfEmpty` bilan asosiy manbada natija topilmasa zaxira manbaga murojaat qilish.
- Resilience4j circuit breaker bilan "yarim ochiq" holatda trafikni asta tiklash.
- Reactive Kafka consumer'da poison message'ni `onErrorResume` bilan DLQ'ga yuborib, oqimni to'xtatmaslik.

**Ehtiyot bo'ling:** Non-idempotent operatsiyani (to'lov yaratish, buyurtma berish) retry qilish ikkilangan yon ta'sirga olib keladi - idempotency key'siz hech qachon qayta urinmang. Shuningdek `retry()`ni filtrsiz ishlatish 4xx va validatsiya xatolarini ham takrorlab, downstream'ni ortiqcha yuklaydi va umumiy latency'ni retry×timeout darajasida oshirib yuboradi.

## 19.11 Reactive repository'lar (Reactive Repositories)

**Tavsif:** Reactive repository - ma'lumot bazasi bilan non-blocking driver orqali ishlab, `Mono`/`Flux` qaytaradigan data access qatlami. JDBC'ning o'zi tabiatan bloklovchi bo'lgani uchun relational bazalar uchun alohida spetsifikatsiya - R2DBC yaratilgan; MongoDB, Cassandra va Redis esa rasmiy reactive driverlarga ega. Natijada DB kursoridan kelayotgan qatorlar oqim sifatida uzatiladi va thread'lar kutib turmaydi. Biroq reactive repository'lar ORM emas: lazy loading, avtomatik join va entity graph kabi JPA imkoniyatlari yo'q.

**Spring'da qayerda uchraydi:** Spring Data R2DBC'da `ReactiveCrudRepository`, `R2dbcRepository`, `R2dbcEntityTemplate`, `DatabaseClient`, `@Query`, `ConnectionFactory` va `R2dbcTransactionManager`; tranzaksiya uchun `@Transactional` (reactive variant) yoki `TransactionalOperator`. Spring Data MongoDB Reactive'da `ReactiveMongoRepository`, `ReactiveMongoTemplate`, `@Tailable` (capped collection uchun oqim) mavjud; Redis uchun `ReactiveRedisTemplate`, Cassandra uchun `ReactiveCassandraRepository`, Elasticsearch uchun `ReactiveElasticsearchClient`. Spring Boot 3.x/4.x starter'lari: `spring-boot-starter-data-r2dbc`, `spring-boot-starter-data-mongodb-reactive`, `spring-boot-starter-data-redis-reactive`; migratsiyalar odatda Flyway/Liquibase bilan alohida JDBC ulanishi orqali bajariladi.

**Qo'llanish keyslari:**
- WebFlux servisida PostgreSQL bilan to'liq non-blocking zanjir qurish (`r2dbc-postgresql`).
- Katta jadvaldan hisobot qatorlarini `Flux` sifatida oqim bilan eksport qilish, xotirani to'ldirmasdan.
- MongoDB capped collection'ni `@Tailable` bilan real vaqt hodisa kanali sifatida ishlatish.
- `ReactiveRedisTemplate` bilan reactive kesh va pub/sub kanalini bitta stack'da yuritish.
- `DatabaseClient` orqali qo'lda yozilgan murakkab SQL'ni reactive natija bilan bajarish.

**Ehtiyot bo'ling:** R2DBC JPA o'rnini bosmaydi - lazy relation, ikkinchi darajali kesh va dirty checking yo'q, shuning uchun murakkab domen modeli ko'p qo'lda mapping va aniq so'rovlarni talab qiladi. Shuningdek reactive `@Transactional` faqat reactive zanjir ichida ishlaydi: `ThreadLocal`ga tayangan imperativ tranzaksiya bilan aralashtirsangiz tranzaksiya jim ravishda qo'llanmaydi.

## 19.12 WebClient (WebClient)

**Tavsif:** `WebClient` - Spring'ning non-blocking, reactive HTTP client'i; `RestTemplate`ning zamonaviy o'rnini bosuvchisi. U fluent builder API beradi, javobni `Mono`/`Flux` sifatida qaytaradi va butun chaqiriqni reactive pipeline'ga tabiiy tarzda qo'shadi. Bir xil client bilan ham streaming (SSE, NDJSON), ham oddiy JSON so'rovlarini bajarish mumkin, filtrlar (`ExchangeFilterFunction`) esa auth, retry va logging kabi cross-cutting mantiqni markazlashtiradi. Bloklovchi muhitda ham `block()` bilan ishlatish mumkin, lekin u holda `RestClient` ko'proq mos keladi.

**Spring'da qayerda uchraydi:** `org.springframework.web.reactive.function.client.WebClient`, `WebClient.Builder` (Spring Boot auto-configuration bilan metrika va tracing allaqachon ulangan holda beriladi), `ExchangeFilterFunction`, `ExchangeStrategies` (`maxInMemorySize`), `ClientHttpConnector` (`ReactorClientHttpConnector`, `JdkClientHttpConnector`, `JettyClientHttpConnector`). Spring Framework 6.x/7.x'da deklarativ HTTP interfeyslar `@HttpExchange`/`@GetExchange` + `HttpServiceProxyFactory` orqali `WebClientAdapter` bilan ishlaydi. OAuth2 uchun `ServerOAuth2AuthorizedClientExchangeFilterFunction`, load balancing uchun Spring Cloud'ning `@LoadBalanced` va `ReactorLoadBalancerExchangeFilterFunction`; testda `WebTestClient` va `MockWebServer`.

**Qo'llanish keyslari:**
- Microservice'lar orasida reactive gateway/BFF chaqiriqlari va javoblarni `Mono.zip` bilan agregatsiya qilish.
- Server-Sent Events oqimini `bodyToFlux(ServerSentEvent.class)` bilan iste'mol qilish.
- LLM yoki boshqa streaming API'dan token-token javob o'qish (NDJSON/text stream).
- OAuth2 client credentials bilan avtomatik token boshqaruvini filter orqali ulash.
- Katta fayllarni `BodyInserters.fromDataBuffers(...)` bilan xotiraga to'liq yuklamasdan uzatish.

**Ehtiyot bo'ling:** Har bir so'rov uchun yangi `WebClient` yaratish ulanish pool'ini qayta-qayta tiklab resurs sarflaydi - client'ni bean sifatida bir marta yasab qayta ishlating va `responseTimeout`/connection pool chegaralarini aniq sozlang. `exchange()` metodi deprecated va javob tanasini oqizmaslik (leak) xavfini tug'diradi; o'rniga `retrieve()`/`exchangeToMono(...)` ishlatiladi.

## 19.13 WebFlux funksional endpoint'lar (WebFlux Functional Endpoints)

**Tavsif:** Funksional endpoint'lar - annotatsiyalarga tayanmasdan, routing va handler mantiqini oddiy Java lambda/metod referenslari bilan e'lon qilish uslubi. `RouterFunction` so'rovni `HandlerFunction`ga moslashtiradi, `RequestPredicate` esa yo'l, metod, header va content-type bo'yicha shartni ifodalaydi. Bu model routing'ni kodda ko'rinadigan, test qilinadigan va programmatik tarzda birlashtirila oladigan qiladi; reflection va proxy'ga bog'liqlik kamayadi, bu esa startup vaqti va GraalVM native image uchun foydali. Semantik jihatdan `@RestController` bilan bir xil imkoniyat beradi, farqi - deklaratsiya uslubida.

**Spring'da qayerda uchraydi:** `org.springframework.web.reactive.function.server` paketidagi `RouterFunctions.route()`, `RouterFunction`, `HandlerFunction`, `ServerRequest`, `ServerResponse`, `RequestPredicates`, `HandlerFilterFunction`, `RouterFunctions.nest(...)`. Router bean sifatida `@Bean RouterFunction<ServerResponse>` ko'rinishida e'lon qilinadi va `RouterFunctionMapping` orqali `DispatcherHandler`ga ulanadi. Validatsiya qo'lda (`Validator`) yoki `ServerRequest.bodyToMono(...)` dan keyin bajariladi; testda `WebTestClient.bindToRouterFunction(...)` ishlatiladi. Spring Framework 6.x/7.x'da `RouterFunctions.route()` DSL'i va Kotlin `coRouter` mavjud; blocking stack uchun esa `org.springframework.web.servlet.function` ekvivalenti bor.

```java
@Bean
RouterFunction<ServerResponse> userRoutes(UserHandler handler) {
    return RouterFunctions.route()
        .GET("/users/{id}", handler::byId)
        .GET("/users", RequestPredicates.accept(MediaType.TEXT_EVENT_STREAM), handler::stream)
        .POST("/users", handler::create)
        .filter(handler::withErrorMapping)
        .build();
}
```

**Qo'llanish keyslari:**
- Kichik, aniq chegaralangan API yoki gateway'da routing'ni bitta joyda ko'rinadigan qilish.
- GraalVM native image uchun reflection'ga kam tayanadigan endpoint'lar qurish.
- Routing'ni konfiguratsiya yoki feature flag asosida programmatik tarzda yig'ish.
- Bir nechta modulning `RouterFunction`larini `.and(...)` bilan birlashtirib, kompozit API hosil qilish.
- Health, metrics yoki webhook kabi infratuzilma endpoint'larini controller sinfisiz qo'shish.

**Ehtiyot bo'ling:** Funksional stil `@Valid`, `@RequestParam` konvertatsiyasi va `@ExceptionHandler` kabi tayyor annotatsiya qulayliklarini bermaydi - validatsiya, parametr parsing va xato mapping'ini qo'lda yozish kerak, bu katta API'da takrorlanuvchi kodga olib keladi. Bitta loyihada annotatsiyali va funksional uslublarni tartibsiz aralashtirish esa routing mantiqini kuzatishni qiyinlashtiradi.

## 19.14 Oqimli javoblar (Streaming Responses - SSE, NDJSON)

**Tavsif:** Server butun javobni to'liq yig'ib kutmasdan, elementlarni tayyor bo'lgani sayin mijozga bo'lak-bo'lak uzatadi. Bu "time to first byte" ni keskin kamaytiradi va cheksiz yoki juda katta datasetlarni xotiraga sig'dirmasdan yetkazish imkonini beradi. Transport sifatida Server-Sent Events (`text/event-stream`), NDJSON (`application/x-ndjson`) yoki oddiy chunked JSON array ishlatiladi. Reactive stackda bu `Flux<T>` qaytarish bilan tabiiy ravishda hosil bo'ladi, chunki backpressure butun zanjir bo'ylab mijozning TCP oynasigacha yetadi.

**Spring'da qayerda uchraydi:** Spring WebFlux controllerida `Flux<T>` qaytarilib, `@GetMapping(produces = MediaType.TEXT_EVENT_STREAM_VALUE)` yoki `APPLICATION_NDJSON_VALUE` ko'rsatiladi; metadata qo'shish uchun `ServerSentEvent<T>` builder (`ServerSentEvent.builder().id().event().retry().data()`) mavjud. Kodek sifatida `ServerSentEventHttpMessageWriter` va `Jackson2JsonEncoder` (streaming rejimida) ishlaydi; mijoz tomonida `WebClient.get().retrieve().bodyToFlux(...)` yoki Spring Framework 6.1+ dagi `RestClient` bilan `Flux` o'qiladi. Servlet stackda ham `SseEmitter`, `ResponseBodyEmitter` va `StreamingResponseBody` bor, Spring Boot 3.2+ da esa virtual threadlar bilan birga ishlatiladi; Spring AI `ChatClient.prompt().stream().content()` orqali LLM token oqimini `Flux<String>` sifatida beradi.

**Qo'llanish keyslari:**
- LLM chat UI'ga token-token javob uzatish (Spring AI + SSE), foydalanuvchi birinchi so'zni darhol ko'radi.
- Jonli narx/kurs tickeri yoki sport natijalari dashboardiga uzluksiz push.
- Millionlab qatorli hisobotni NDJSON ko'rinishida eksport qilish - serverda OOM bo'lmaydi.
- Uzoq ishlaydigan batch job progressini (foiz, log qatorlari) real vaqtda ko'rsatish.
- Mikroservislar orasida katta natija to'plamini `WebClient` bilan oqim sifatida uzatish va darhol qayta ishlashni boshlash.

**Ehtiyot bo'ling:** SSE faqat server→mijoz yo'nalishida ishlaydi va HTTP/1.1 da brauzer per-domen ulanish limitiga uriladi, shuningdek oraliq proxy/load balancer response'ni bufferlab oqimni "o'ldirishi" mumkin (`X-Accel-Buffering: no`, proxy_buffering off kerak bo'ladi). Oqim o'rtasida HTTP status allaqachon 200 bo'lib ketgani uchun xatoni status kod bilan bildira olmaysiz - xato hodisasini oqim ichidagi alohida event turida yuborish va keep-alive heartbeat qo'shish kerak, aks holda idle timeoutlar ulanishni uzadi.

## 19.15 Reactive Security

**Tavsif:** Klassik Spring Security `SecurityContextHolder` ni `ThreadLocal` da saqlaydi, lekin reactive zanjirda bitta request bir necha threadda bajarilishi mumkin, shuning uchun `ThreadLocal` yaroqsiz. Reactive Security xavfsizlik kontekstini Reactor Contextga ko'chiradi va barcha autentifikatsiya/avtorizatsiya qarorlarini non-blocking, `Mono`-asosli qiladi. Natijada filter zanjiri, user lookup va token tekshiruvi ham to'liq asinxron bo'ladi.

**Spring'da qayerda uchraydi:** `@EnableWebFluxSecurity`, `SecurityWebFilterChain` bean va `ServerHttpSecurity` DSL (`authorizeExchange()`, `pathMatchers()`, `oauth2ResourceServer()`); kontekst `ReactiveSecurityContextHolder.getContext()` orqali olinadi. Foydalanuvchini yuklash uchun `ReactiveUserDetailsService` / `MapReactiveUserDetailsService`, autentifikatsiya uchun `ReactiveAuthenticationManager`, metod darajasida esa `@EnableReactiveMethodSecurity` bilan `@PreAuthorize` (faqat `Mono`/`Flux` qaytaruvchi metodlarda). Spring Security 6.x da JWT uchun `ReactiveJwtDecoder`, OAuth2 client uchun `ServerOAuth2AuthorizedClientExchangeFilterFunction` bilan `WebClient` integratsiyasi, sessiya uchun `WebSessionServerSecurityContextRepository` yoki Spring Session Reactive Redis ishlatiladi.

**Qo'llanish keyslari:**
- WebFlux API gatewayda (Spring Cloud Gateway) JWT ni non-blocking tekshirib, downstream'ga propagate qilish.
- `@PreAuthorize("hasRole('ADMIN')")` ni `Mono<Account>` qaytaruvchi reactive service metodlariga qo'llash.
- Reactive MongoDB/R2DBC dan foydalanuvchini `ReactiveUserDetailsService` bilan yuklash.
- `WebClient` chaqiruvlarida OAuth2 access tokenni avtomatik qo'shish va refresh qilish.
- Tenant/user ma'lumotini Reactor Context orqali audit loggerga uzatish.

**Ehtiyot bo'ling:** `SecurityContextHolder` ni WebFlux ichida ishlatish eng ko'p uchraydigan xato - u `null` qaytaradi yoki noto'g'ri foydalanuvchini beradi, chunki kontekst threadga emas, subscriptionga bog'langan. Shuningdek `@PreAuthorize` ni `void`/oddiy obyekt qaytaruvchi metodda ishlatish jim qolib ketadi, blocking `UserDetailsService` yoki blocking JWK yuklash esa event loopni to'sib qo'yadi.

## 19.16 Reactive tranzaksiyalar (Reactive Transactions)

**Tavsif:** Klassik `@Transactional` tranzaksiya holatini `ThreadLocal` da saqlaydi, reactive oqimda esa bu ishlamaydi. Reactive tranzaksiya menejeri tranzaksiya resursini Reactor Contextga joylaydi va commit/rollback ni oqim tugashi (`onComplete`/`onError`) signaliga bog'laydi. Shu bilan non-blocking driver ustida ham atomarlik saqlanadi.

**Spring'da qayerda uchraydi:** `ReactiveTransactionManager` interfeysi va uning implementatsiyalari: `R2dbcTransactionManager` (Spring Data R2DBC), `ReactiveMongoTransactionManager` (replica set bilan), `ReactiveNeo4jTransactionManager`. Deklarativ usulda `@Transactional` reactive metodlarda ishlaydi (`Mono`/`Flux` qaytarsa), programmatik usulda `TransactionalOperator.create(txManager)` va `.as(operator::transactional)` yoki `transactionalEventPublisher` ishlatiladi. Spring Framework 6.x da `@Transactional(propagation = REQUIRES_NEW)` kabi ba'zi propagationlar qo'llab-quvvatlanadi, lekin to'liq to'plam imperativ stackdagidan torroq.

**Qo'llanish keyslari:**
- R2DBC ustida bir nechta `repository.save()` ni bitta atomar birlikka yig'ish.
- Pul o'tkazmasida debet va kredit yozuvlarini birgalikda commit qilish yoki rollback qilish.
- `TransactionalOperator` bilan `Flux` batch insertni bitta tranzaksiyada bajarish.
- Reactive MongoDB multi-document tranzaksiyalarida bir nechta collection yangilash.
- Outbox pattern: domain yozuvi va outbox eventini bitta reactive tranzaksiyada saqlash.

**Ehtiyot bo'ling:** `@Transactional` ni reactive metodda yozib, oqimni `subscribe()` qilmasdan tashlab ketish - hech narsa bajarilmaydi va tranzaksiya ham ochilmaydi; blocking JDBC ni reactive `@Transactional` bilan aralashtirish esa butunlay ishlamaydi, chunki `PlatformTransactionManager` va `ReactiveTransactionManager` kontekstlari alohida. Uzun ochiq tranzaksiyalar R2DBC connection poolini tez tugatadi, shuning uchun tranzaksiya ichida tashqi HTTP chaqiruv qilmang.

## 19.17 Blocking chaqiruvlarni aniqlash (Blocking Call Detection - BlockHound)

**Tavsif:** Reactive ilovadagi eng xavfli xato - non-blocking event loop threadida blocking operatsiya bajarish; bu butun serverni bir nechta sekin chaqiruv bilan to'xtatib qo'yadi va yuk ostida yashirin qoladi. BlockHound JVM instrumentation (Java agent) orqali blocking deb belgilangan metodlarni (`Thread.sleep`, `InputStream.read`, `Socket`, JDBC) kuzatadi va ular non-blocking threadda chaqirilsa darhol `BlockingOperationError` tashlaydi. Shu tariqa muammo production'da emas, test/dev bosqichida aniqlanadi.

**Spring'da qayerda uchraydi:** `io.projectreactor.tools:blockhound` (va JUnit uchun `blockhound-junit-platform`) dependency qo'shiladi, `BlockHound.install()` test konfiguratsiyasida yoki `main` boshida chaqiriladi; Reactor `NonBlocking` marker interfeysini `reactor-netty` event loop threadlari va `Schedulers.parallel()` threadlari implement qiladi, shuning uchun BlockHound aynan ularni nazorat qiladi. Ruxsat berish uchun `BlockHound.builder().allowBlockingCallsInside("com.example.Legacy", "method").install()` yoki `BlockHoundIntegration` SPI ishlatiladi; Reactor Netty, R2DBC va Spring Data o'z integrationlarini avtomatik ro'yxatdan o'tkazadi. Java 13+ da agentni dinamik ulash uchun `-XX:+AllowRedefinitionToAddDeleteMethods` flagi kerak bo'lishi mumkin.

**Qo'llanish keyslari:**
- WebFlux integration testlarida tasodifiy qo'shilgan blocking JDBC/`RestTemplate` chaqiruvini CI'da ushlash.
- Legacy kutubxonani reactive servicega integratsiya qilganda yashirin blocking I/O ni topish.
- `Mono.block()` ni controller ichida chaqirgan yangi developerni darhol xatolik bilan to'xtatish.
- Sekin `Flux` zanjirida qaysi operator event loopni bloklayotganini lokalizatsiya qilish.
- Reactive migratsiya davrida qolgan blocking "orolchalar" ro'yxatini `allowBlockingCallsInside` bilan hujjatlashtirish.

**Ehtiyot bo'ling:** BlockHound ni production'da doimiy yoqib qo'yish tavsiya etilmaydi - instrumentation overhead beradi va kutilmagan `BlockingOperationError` bilan ishlayotgan trafikni buzishi mumkin; uni test va staging profilida ishlating. Yana bir tuzoq: `allowBlockingCallsInside` ni keng doirada qo'llab, haqiqiy muammolarni ko'rinmas qilib yuborish.

## 19.18 Blocking kodni ko'prikka olish (Bridging Blocking Code - boundedElastic)

**Tavsif:** Ko'p loyihada JDBC, fayl I/O, legacy SOAP client yoki blocking SDK ni butunlay almashtirish imkoni yo'q. Yechim - bunday chaqiruvni alohida, kengayadigan thread poolga ko'chirish va event loop threadini bo'shatish. Reactor'da bu `Schedulers.boundedElastic()` bilan amalga oshiriladi: u threadlar sonini CPU yadrolari asosida cheklab (default `10 × availableProcessors`), ishlatilmagan threadlarni tozalab turadi va shu bilan cheksiz thread yaralishidan saqlaydi.

**Spring'da qayerda uchraydi:** `Mono.fromCallable(() -> jdbcRepo.find(id)).subscribeOn(Schedulers.boundedElastic())` eng tipik shakl; `Flux.fromIterable(...)` va `publishOn(Schedulers.boundedElastic())` ham qo'llanadi. Spring Framework 6.x da `Schedulers.fromExecutor(taskExecutor)` orqali `SimpleAsyncTaskExecutor` (virtual thread rejimida, `setVirtualThreads(true)`) yoki `ThreadPoolTaskExecutor` ni scheduler sifatida ulash mumkin. `ContextPropagation` (`io.micrometer:context-propagation` + `Hooks.enableAutomaticContextPropagation()`) MDC/tracing/Security contextni thread almashganda saqlab qoladi.

```java
Mono<Order> findOrder(Long id) {
    return Mono.fromCallable(() -> jdbcOrderRepository.findById(id))
            .subscribeOn(Schedulers.boundedElastic())
            .timeout(Duration.ofSeconds(2));
}
```

**Qo'llanish keyslari:**
- WebFlux controllerdan blocking JPA/JDBC repositoryni xavfsiz chaqirish (bosqichma-bosqich migratsiya davrida).
- Blocking fayl tizimi yoki S3 SDK (sinxron versiyasi) bilan ishlash.
- Legacy JAX-WS/SOAP client chaqiruvini reactive pipeline ichiga qo'shish.
- `ImageIO` kabi CPU+I/O aralash blocking kutubxonalarni oqimdan ajratish.
- Blocking template engine yoki PDF generatorni oqim ichida ishlatish.

**Ehtiyot bo'ling:** `subscribeOn` butun yuqoridagi zanjirni ko'chiradi, `publishOn` esa faqat o'zidan keyingi qismni - joylashuvini aralashtirib yuborish blocking chaqiruvni baribir event loopda qoldiradi. `boundedElastic` cheksiz emas: yuqori yuk ostida navbat o'sib `RejectedExecutionException` yoki latency portlashi beradi, shuning uchun blocking manbani `boundedElastic` ga tashlab, bulkhead/`timeout` qo'ymaslik - reactive stackni blocking stackdan ham sekinroq qiladi.

## 19.19 Sinks (Reactive Event Bus - Sinks)

**Tavsif:** Sink - imperativ kodan reactive oqimga signal "qo'lda" yuborish uchun programmatik ko'prik: siz `tryEmitNext()` chaqirasiz, subscriberlar esa `Flux` sifatida qabul qiladi. Bu multicast event bus, in-memory pub/sub yoki callback-asosli API ni `Flux` ga aylantirish uchun ishlatiladi. Reactor 3.4+ dan `Sinks` fabrikasi eski `Processor` turlarini almashtirdi va emission natijasini (`EmitResult`) aniq qaytarib, thread-safe semantikani ravshan qildi.

**Spring'da qayerda uchraydi:** `reactor.core.publisher.Sinks` - `Sinks.many().multicast().onBackpressureBuffer()`, `Sinks.many().replay().limit(n)`, `Sinks.many().unicast()`, bitta qiymat uchun `Sinks.one()`; o'qish uchun `sink.asFlux()` / `sink.asMono()`. Xavfsiz emission uchun `emitNext(value, Sinks.EmitFailureHandler.busyLooping(Duration))` yoki `FAIL_FAST`. Spring'da bu odatda `@Service` ichida `Sinks.Many` bean sifatida saqlanib, `@EventListener` yoki `ApplicationEventPublisher` dan kelgan hodisalarni SSE/WebSocket oqimiga uzatishda ishlatiladi; WebSocket handlerida `WebSocketSession.send(sink.asFlux().map(session::textMessage))` tipik ko'rinish.

**Qo'llanish keyslari:**
- Domain eventlarni (`@EventListener`) bir nechta SSE mijoziga multicast qilish.
- WebSocket chat xonasi: har bir xona uchun bitta `Sinks.Many` multicast.
- Yangi ulangan dashboardga oxirgi N o'lchovni `replay().limit(10)` bilan darhol berish.
- Callback/listener asosli legacy SDK (JMS listener, MQTT client) ni `Flux` ga aylantirish.
- In-memory komanda navbati: `unicast().onBackpressureBuffer()` bilan bitta consumer uchun.

**Ehtiyot bo'ling:** `tryEmitNext()` natijasini tekshirmaslik eng keng tarqalgan xato - `EmitResult.FAIL_NON_SERIALIZED` yoki `FAIL_ZERO_SUBSCRIBER` holatida event jim yo'qoladi. Multicast sink default'da subscriber yo'q bo'lsa eventlarni tashlab yuboradi, cheksiz `onBackpressureBuffer()` esa sekin subscriber bo'lsa xotirani to'ldiradi; Sinks'ni ishonchli, broker o'rnini bosuvchi xabar navbati sifatida ko'rish ham xato - o'chirishda (restart) hamma narsa yo'qoladi.

## 19.20 Reactive Kafka (reactor-kafka)

**Tavsif:** Standart Kafka client blocking `poll()` modeliga asoslangan, bu esa reactive ilovada thread egallab turadi va backpressure'ni ifoda etmaydi. `reactor-kafka` consumer/producerni Reactor Publisher'lariga o'raydi: consumer `Flux<ReceiverRecord>` beradi va subscriber talabiga qarab `poll()` ni pauzalaydi/davom ettiradi, producer esa `Flux<SenderRecord>` ni qabul qilib natijalarni oqim sifatida qaytaradi. Shu bilan Kafka throughputi iste'molchi tezligiga tabiiy moslashadi.

**Spring'da qayerda uchraydi:** `io.projectreactor.kafka:reactor-kafka` kutubxonasi - `KafkaReceiver.create(ReceiverOptions)`, `receiver.receive()` / `receiveAutoAck()` / `receiveExactlyOnce()`, hamda `KafkaSender.create(SenderOptions)` va `sender.send(Flux<SenderRecord>)`. Offsetni qo'lda tasdiqlash uchun `record.receiverOffset().acknowledge()` yoki `commit()`. Spring Boot 3.x da Kafka propertylarini `KafkaProperties.buildConsumerProperties()` dan olib `ReceiverOptions` ga uzatish odatiy; alternativa sifatida Spring Cloud Stream Kafka binderining reactive rejimi (`@Bean Function<Flux<String>, Flux<String>>`) yoki `spring-kafka` ning `ReactiveKafkaConsumerTemplate` / `ReactiveKafkaProducerTemplate` sinflari ishlatiladi.

**Qo'llanish keyslari:**
- Kafka topikidan kelgan eventlarni R2DBC bazaga non-blocking yozish (butun pipeline reactive).
- `concatMap` bilan partition tartibini saqlab, ketma-ket event qayta ishlash.
- Kafka'dan o'qib `WebClient` bilan tashqi API ga enrich qilish va boshqa topikka yozish.
- `groupBy(partition)` + `flatMap` bilan partition darajasida parallel ishlov.
- SSE/WebSocket orqali Kafka oqimini brauzerga real vaqtda uzatish.

**Ehtiyot bo'ling:** `flatMap` ni cheklamasdan ishlatish Kafka'dagi partition tartibini buzadi va downstream'ni ko'mib tashlaydi - tartib muhim bo'lsa `concatMap`, parallellik kerak bo'lsa `groupBy` + cheklangan concurrency ishlating. Offsetni `acknowledge()` qilishni xatolik yo'lida ham to'g'ri boshqarish kerak, aks holda event yo'qoladi yoki cheksiz qayta o'qiladi; `receive()` oqimida `onError` kelsa subscription uzilib consumer to'xtaydi, shuning uchun `retryWhen` va DLQ strategiyasi majburiy.

## 19.21 Reactive va Virtual Threads tanlovi (Reactive vs Virtual Threads Decision)

**Tavsif:** Java 21 (JEP 444) dagi virtual threadlar blocking kod yozib turib ham yuqori I/O concurrency olish imkonini berdi, shuning uchun "scalability uchun reactive" argumenti ko'p holatda zaiflashdi. Virtual threadlar oddiy imperativ uslub, tushunarli stack trace va mavjud JDBC/JPA stackni saqlaydi; reactive esa oqim semantikasi, backpressure, kompozitsiya operatorlari va cheksiz streamlarni beradi. Arxitektor qarorni "qancha ulanish" emas, "oqim semantikasi kerakmi" savoli bilan qabul qilishi to'g'ri bo'ladi.

**Spring'da qayerda uchraydi:** Spring Boot 3.2+ da `spring.threads.virtual.enabled=true` Tomcat/Jetty request ishlovini va `SimpleAsyncTaskExecutor` ni virtual threadga o'tkazadi; Spring MVC + JDBC/JPA shu rejimda yuqori concurrency beradi. Reactive tomonda Spring WebFlux + `reactor-netty`, Spring Data R2DBC/Reactive Mongo, `WebClient`, Spring Cloud Gateway (faqat reactive) turadi. Ikkisini aralashtirishda `Schedulers.fromExecutor` va `context-propagation` kutubxonasi, Spring Framework 6.1+ dagi `RestClient` (blocking, lekin `WebClient` ga o'xshash API) muhim rol o'ynaydi.

**Qo'llanish keyslari:**
- Oddiy CRUD REST servis, JPA bilan: Spring MVC + virtual threads tanlanadi, reactive emas.
- API gateway / proxy, minglab uzoq ulanish: WebFlux + Netty, chunki per-connection thread kerak emas.
- SSE/WebSocket streaming, LLM token oqimi, telemetriya: reactive (`Flux`) tabiiy mos.
- Murakkab fan-out/fan-in orchestration, timeout va retry siyosatlari: Reactor operatorlari ustunlik beradi.
- Mavjud blocking monolitni tezlashtirish kerak bo'lsa: virtual threadlar bir qatorlik konfiguratsiya bilan foyda beradi.

**Ehtiyot bo'ling:** Virtual threadlarda `synchronized` bloki ichidagi blocking (Java 21-23 da pinning) va `ThreadLocal` ni katta obyektlar bilan ishlatish yashirin muammo tug'diradi, shuningdek connection pool hali ham haqiqiy cheklov bo'lib qoladi - virtual threadlar bazani cheksiz qila olmaydi. Teskari tomondan, butun tizimni "moda uchun" reactive qilish debugging, profiling va yangi developerlar uchun katta narx: backpressure yoki streaming semantikasi kerak bo'lmasa, reactive tanlash asossiz.

## 19.22 Reactive Manifesto tamoyillari (Reactive Manifesto Principles)

**Tavsif:** Reactive Manifesto reactive tizimning to'rt xususiyatini belgilaydi: responsive (javobgarlik - doimiy, prognozlanadigan latency), resilient (nosozlikka chidamlilik - izolyatsiya va replikatsiya orqali), elastic (yuk ostida gorizontal moslashuv) va message-driven (komponentlar o'rtasida asinxron, joylashuvdan mustaqil xabar almashinuvi). Bu kod darajasidagi "reactive programming" dan farqli, arxitektura darajasidagi tamoyillar to'plami. Reactor yoki RxJava ishlatish o'z-o'zidan tizimni reactive qilmaydi - izolyatsiya, backpressure va degradation strategiyasi kerak.

**Spring'da qayerda uchraydi:** Message-driven qismi Spring Cloud Stream, Spring for Apache Kafka/RabbitMQ va `Sinks`/`Flux` bilan quriladi; resilience uchun Resilience4j (`@CircuitBreaker`, `@Bulkhead`, `@RateLimiter`) va Reactor'ning `timeout()`, `retryWhen()`, `onErrorResume()` operatorlari; elastiklik uchun Kubernetes HPA bilan birga stateless WebFlux servislar va `spring-boot-starter-actuator` metrikalari (Micrometer). Responsiveness Micrometer + Prometheus/OpenTelemetry orqali o'lchanadi, Spring Boot 3.x da `ObservationRegistry` reactive zanjirlarni ham qamrab oladi.

**Qo'llanish keyslari:**
- Mikroservis arxitekturasini loyihalashda sinxron REST zanjirlarini event-driven integratsiyaga almashtirish qarorini asoslash.
- Har bir tashqi integratsiyaga bulkhead va circuit breaker qo'yib, nosozlikni izolyatsiya qilish.
- SLO sifatida p99 latency belgilash va yuk ostida graceful degradation (cached/partial javob) rejasini tuzish.
- Autoscaling siyosatini throughput va navbat uzunligi metrikalariga bog'lash.
- Arxitektura review'da "bu tizim haqiqatan reactive mi?" savolini to'rt tamoyil bo'yicha tekshirish.

**Ehtiyot bo'ling:** Eng keng tarqalgan yanglishuv - `Flux` ishlatishni reactive arxitektura deb hisoblash: backpressure chetga surilgan, hamma chaqiruv sinxron REST bo'lgan tizim reactive bo'lmaydi. Teskarisi ham xato: har bir ichki chaqiruvni message broker orqali o'tkazib, oddiy domen uchun ortiqcha murakkablik va eventual consistency muammolarini sotib olish.

## 19.23 java.util.concurrent.Flow

**Tavsif:** `java.util.concurrent.Flow` - Reactive Streams spetsifikatsiyasining JDK 9+ ichiga kiritilgan versiyasi: `Flow.Publisher`, `Flow.Subscriber`, `Flow.Subscription`, `Flow.Processor`. U faqat to'rt interfeys va backpressure protokolini (`request(n)`, `onNext`/`onError`/`onComplete`) belgilaydi - operatorlar, schedulerlar yoki kutubxona funksiyalari bermaydi. Shu sababli u turli reactive kutubxonalar (Reactor, RxJava, Akka Streams, Mutiny) o'rtasidagi neytral interoperability qatlami sifatida ishlatiladi.

**Spring'da qayerda uchraydi:** Reactor'da `JdkFlowAdapter.publisherToFlowPublisher(flux)` va `flowPublisherToFlux(flowPublisher)` adapterlari mavjud; `org.reactivestreams.FlowAdapters` (Reactive Streams 1.0.3+) `Publisher` va `Flow.Publisher` o'rtasida ikki tomonlama o'tkazadi. JDK ichida `SubmissionPublisher` tayyor `Flow.Publisher` implementatsiyasini beradi, `HttpClient` (JDK 11+) esa `HttpResponse.BodySubscribers.fromSubscriber(Flow.Subscriber)` va `BodyPublishers.fromPublisher(Flow.Publisher)` orqali shu modelni ishlatadi. Spring Framework 6.x reactive adapter registry (`ReactiveAdapterRegistry`) `Flow.Publisher` ni ham qo'llab-quvvatlaydi, shuning uchun WebFlux controller `Flow.Publisher<T>` qaytarsa ham ishlaydi. R2DBC SPI va JDK HTTP client integratsiyalari shu neytral tipni asos qiladi.

**Qo'llanish keyslari:**
- RxJava bilan yozilgan kutubxona natijasini Reactor zanjiriga adapter orqali qo'shish.
- JDK `HttpClient` javob tanasini `Flux` sifatida o'qib WebFlux pipeline'ga ulash.
- Reactive kutubxonaga bog'liq bo'lmagan public API (SDK) ni `Flow.Publisher` tiplari bilan e'lon qilish.
- `SubmissionPublisher` bilan yengil in-process pub/sub qurish, qo'shimcha dependency olmasdan.
- Mutiny (Quarkus) va Reactor servislarini bitta kutubxona kontrakti orqali bog'lash.

**Ehtiyot bo'ling:** `Flow` da operator yo'q, shuning uchun unda to'g'ridan-to'g'ri biznes logika yozish `request(n)` hisobini qo'lda boshqarishga olib keladi - bu xatoga juda moyil; faqat chegara (boundary) tipi sifatida ishlating. `SubmissionPublisher` default'da buffer to'lganda bloklaydi yoki tashlab yuboradi, demak uni haqiqiy backpressure yechimi deb hisoblash xato.

## 19.24 Observable / Reactive Extensions merosi (Observable / Reactive Extensions Heritage)

**Tavsif:** Zamonaviy reactive API'lar ildizi Microsoft'ning Rx (Reactive Extensions) loyihasidan, ya'ni `IObservable`/`IObserver` ikkiligidan boshlanadi; undan RxJava 1 o'sib chiqdi. RxJava 1 da backpressure yo'q edi va bu `MissingBackpressureException` muammolariga olib keldi, natijada Reactive Streams spetsifikatsiyasi yaratildi va RxJava 2 da `Observable` (backpressure yo'q) va `Flowable` (backpressure bor) ajratildi. Reactor shu tajriba asosida `Mono`/`Flux` ni Reactive Streams'ga to'liq mos qilib qurdi, shuning uchun operator nomlari (`map`, `flatMap`, `zip`, `merge`, `debounce`) ko'p jihatdan Rx terminologiyasini meros qilib oladi.

**Spring'da qayerda uchraydi:** RxJava 3 (`io.reactivex.rxjava3.core.Flowable`, `Observable`, `Single`, `Maybe`, `Completable`) hanuz keng ishlatiladi va Spring `ReactiveAdapterRegistry` ularni avtomatik adapt qiladi - WebFlux controller `Single<T>` yoki `Flowable<T>` qaytarishi mumkin, Spring Data reactive repositorylari ham RxJava 3 variantlarini (`RxJava3CrudRepository`) taqdim etadi. Android/Kotlin dunyosida Rx operator madaniyati Kotlin `Flow` ga ham o'tgan; Reactor bilan Kotlin `Flow` orasida `kotlinx-coroutines-reactor` (`asFlux()`, `asFlow()`) ko'prik qiladi.

**Qo'llanish keyslari:**
- RxJava 3 asosidagi mavjud kutubxona yoki mobil backend kodini WebFlux ga ulash.
- `RxJava3CrudRepository` bilan Spring Data reactive repositoryni Rx uslubida ishlatish.
- Rx tajribasi bor jamoaga Reactor operatorlarini o'rgatishda nomlar mosligidan foydalanish.
- Kotlin `Flow` yozilgan modulni Reactor pipeline bilan bog'lash.
- Marble diagrammalar va Rx dokumentatsiyasidan Reactor operatorini tanlashda foydalanish.

**Ehtiyot bo'ling:** Bitta loyihada RxJava, Reactor va Kotlin `Flow` ni parallel ishlatish ortiqcha adapter qatlamlari, ikki xil scheduler modeli va chalkash xato semantikasini keltiradi - bitta asosiy tipni tanlang. Shuningdek RxJava `Observable` backpressure'ni qo'llab-quvvatlamaydi, uni tez manba bilan ishlatish xotira o'sishiga olib keladi; shu holatda `Flowable` kerak.

## 19.25 Sovuq start va subscription hayot sikli (Cold Start & Subscription Lifecycle)

**Tavsif:** Reactor'da `Mono`/`Flux` - bu reja (assembly), ish emas: `subscribe()` chaqirilmaguncha hech narsa bajarilmaydi. Cold publisher har bir subscriber uchun ishni qaytadan boshlaydi (masalan har bir subscription alohida HTTP chaqiruv qiladi), hot publisher esa manbani ulashadi va kech ulangan subscriber oqimning boshini ko'rmasligi mumkin. Hayot sikli bosqichlari: assembly → subscribe → `request(n)` → `onNext`* → `onComplete`/`onError` yoki `cancel`. Shu modelni tushunmaslik "kod ishlamayapti" yoki "ikki marta bajarildi" turidagi xatolarning asosiy sababi.

**Spring'da qayerda uchraydi:** WebFlux controller qaytargan `Flux` ni framework o'zi subscribe qiladi; mijoz ulanishni uzsa `cancel` signali butun zanjir bo'ylab tarqaladi va `WebClient` chaqiruvi ham bekor qilinadi. Cold→hot aylantirish uchun `share()`, `cache()`, `publish().refCount()`, `replay()` operatorlari; ko'p marta subscribe qilinadigan `Mono` ni keshlash uchun `Mono.cache()`. Lifecycle hook'lari: `doOnSubscribe`, `doOnRequest`, `doOnNext`, `doOnCancel`, `doFinally(SignalType)`, `Hooks.onOperatorDebug()` yoki `ReactorDebugAgent` (reactor-tools) stack trace'ni tiklash uchun. Testda `StepVerifier` (`reactor-test`) subscription va signal ketma-ketligini tekshiradi; `Mono.defer()` har subscriptionda qiymatni qayta hisoblash uchun ishlatiladi.

**Qo'llanish keyslari:**
- Service metodidan `Flux` qaytarib, uni subscribe qilishni controllerga qoldirish (eager side effect bo'lmasligi uchun).
- Bir xil konfiguratsiya/token chaqiruvini `Mono.cache()` bilan bir marta bajarib, hamma subscriberga ulashish.
- SSE mijozi sahifani yopganda `doOnCancel` bilan resursni tozalash va downstream chaqiruvni to'xtatish.
- `Mono.defer()` bilan har retry urinishida yangi timestamp/ID generatsiya qilish.
- `share()` bilan bitta Kafka/WebSocket oqimini bir nechta ichki consumerga tarqatish.

**Ehtiyot bo'ling:** `subscribe()` ni unutish (`fireAndForget()` deb yozilgan, lekin hech kim subscribe qilmagan `Mono`) jim nosozlikning klassik ko'rinishi; teskarisi - bitta cold `Mono` ni ikki joyda ishlatib, tashqi API ga ikki marta so'rov yuborish. `cache()` ni muddatsiz ishlatish eskirgan ma'lumotni va xotira o'sishini beradi, `share()` esa subscriber yo'q qolganda manbani bekor qilib, keyingi subscriberga kutilmagan natija berishi mumkin.

## 19.26 Amalda qo'llash

- [ ] Reactive zanjir ichida blocking chaqiruv borligini BlockHound bilan test muhitida tekshirib, topilganlarini ro'yxat qiling.
- [ ] Har bir reactive oqim uchun backpressure strategiyasini yozib qo'ying; `onBackpressureBuffer` chegarasiz bo'lmasligi kerak.
- [ ] `subscribeOn` va `publishOn` ishlatilgan joylarni sanab chiqib, har birining nega shu yerda turganini yozing.
- [ ] Blocking kodni `boundedElastic` orqali ko'prikka olgan joylarni tekshirib, pool chegarasi borligini tasdiqlang.
- [ ] Reactive va blocking kod aralashgan joylarni aniqlang; aralash model ko'pincha ikki modeldan ham sekin.
- [ ] SSE yoki streaming endpointlar uchun mijoz uzilganda resurs bo'shatilayotganini tekshiring.
- [ ] Reactive kodda kontekst uzatish (`contextWrite`) orqali correlation ID saqlanayotganini tasdiqlang.
- [ ] WebFlux ishlatilsa, butun zanjir reactive drayverda ekanini tekshiring; bitta JDBC chaqiruvi butun foydani yo'qotadi.

---

[&larr; 18. Xavfsizlik patternlari](18-xavfsizlik-patternlari.md) · [Mundarija](README.md) · [20. Batch va scheduling patternlari &rarr;](20-batch-va-scheduling-patternlari.md)
