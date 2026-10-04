<!-- doc: patterns | chapter: 17 | part:  -->

[Java Spring arxitektori bilishi kerak bo'lgan barcha dizayn patternlar](../../README.md) / [Dizayn patternlar](README.md)

# 17. Resilience va cloud dizayn patternlari (Resilience & Cloud Design Patterns)

<details>
<summary>Bu bo'limdagi 42 bo'lim</summary>

- [17.1 Qayta urinish (Retry — exponential backoff, jitter)](#171-qayta-urinish-retry--exponential-backoff-jitter)
- [17.2 Zanjirni uzgich (Circuit Breaker)](#172-zanjirni-uzgich-circuit-breaker)
- [17.3 To'siq (Bulkhead)](#173-tosiq-bulkhead)
- [17.4 Timeout (Timeout)](#174-timeout-timeout)
- [17.5 Chastota cheklovchi (Rate Limiter)](#175-chastota-cheklovchi-rate-limiter)
- [17.6 Bo'g'ish (Throttling)](#176-bogish-throttling)
- [17.7 Zaxira yechim (Fallback)](#177-zaxira-yechim-fallback)
- [17.8 Tez ishdan chiqish (Fail Fast)](#178-tez-ishdan-chiqish-fail-fast)
- [17.9 Barqaror holat (Steady State)](#179-barqaror-holat-steady-state)
- [17.10 Qo'l berib so'rashuv (Handshaking)](#1710-qol-berib-sorashuv-handshaking)
- [17.11 Sinov qurilmasi (Test Harness)](#1711-sinov-qurilmasi-test-harness)
- [17.12 Ajratuvchi middleware (Decoupling Middleware)](#1712-ajratuvchi-middleware-decoupling-middleware)
- [17.13 Qulashiga yo'l ber (Let It Crash)](#1713-qulashiga-yol-ber-let-it-crash)
- [17.14 Yuklamani tashlash (Shed Load / Load Shedding)](#1714-yuklamani-tashlash-shed-load--load-shedding)
- [17.15 Orqa bosim (Back Pressure)](#1715-orqa-bosim-back-pressure)
- [17.16 Hokim / tezlik cheklovchi nazoratchi (Governor)](#1716-hokim--tezlik-cheklovchi-nazoratchi-governor)
- [17.17 Salomatlik endpoint monitoringi (Health Endpoint Monitoring)](#1717-salomatlik-endpoint-monitoringi-health-endpoint-monitoring)
- [17.18 Queue asosida yukni tekislash (Queue-Based Load Leveling)](#1718-queue-asosida-yukni-tekislash-queue-based-load-leveling)
- [17.19 Prioritetli navbat (Priority Queue)](#1719-prioritetli-navbat-priority-queue)
- [17.20 Yetakchini saylash (Leader Election)](#1720-yetakchini-saylash-leader-election)
- [17.21 Rejalashtiruvchi–Agent–Nazoratchi (Scheduler Agent Supervisor)](#1721-rejalashtiruvchiagentnazoratchi-scheduler-agent-supervisor)
- [17.22 Asinxron so'rov-javob (Asynchronous Request-Reply)](#1722-asinxron-sorov-javob-asynchronous-request-reply)
- [17.23 Statik kontentni hosting qilish (Static Content Hosting)](#1723-statik-kontentni-hosting-qilish-static-content-hosting)
- [17.24 Valet kaliti (Valet Key)](#1724-valet-kaliti-valet-key)
- [17.25 Darvozabon (Gatekeeper)](#1725-darvozabon-gatekeeper)
- [17.26 Federatsiyalangan identifikatsiya (Federated Identity)](#1726-federatsiyalangan-identifikatsiya-federated-identity)
- [17.27 Deploy shtamplari (Deployment Stamps)](#1727-deploy-shtamplari-deployment-stamps)
- [17.28 Geode (Geode)](#1728-geode-geode)
- [17.29 Edge ish yuklamasi konfiguratsiyasi (Edge Workload Configuration)](#1729-edge-ish-yuklamasi-konfiguratsiyasi-edge-workload-configuration)
- [17.30 Tashqi konfiguratsiya ombori (External Configuration Store)](#1730-tashqi-konfiguratsiya-ombori-external-configuration-store)
- [17.31 Gateway agregatsiyasi (Gateway Aggregation)](#1731-gateway-agregatsiyasi-gateway-aggregation)
- [17.32 Gateway offloading (Gateway Offloading)](#1732-gateway-offloading-gateway-offloading)
- [17.33 Gateway routing (Gateway Routing)](#1733-gateway-routing-gateway-routing)
- [17.34 Ketma-ket konvoy (Sequential Convoy)](#1734-ketma-ket-konvoy-sequential-convoy)
- [17.35 Xoreografiya (Choreography)](#1735-xoreografiya-choreography)
- [17.36 Hedged so'rovlar (Hedged Requests)](#1736-hedged-sorovlar-hedged-requests)
- [17.37 Bosqichma-bosqich funksionallikni pasaytirish (Graceful Degradation)](#1737-bosqichma-bosqich-funksionallikni-pasaytirish-graceful-degradation)
- [17.38 Chaos engineering (Chaos Engineering)](#1738-chaos-engineering-chaos-engineering)
- [17.39 Resilience4j va Spring Cloud Circuit Breaker (Resilience4j & Spring Cloud Circuit Breaker)](#1739-resilience4j-va-spring-cloud-circuit-breaker-resilience4j--spring-cloud-circuit-breaker)
- [17.40 Spring Framework 7 yadrosidagi resilience (Spring Framework 7 core resilience: @Retryable, @ConcurrencyLimit)](#1740-spring-framework-7-yadrosidagi-resilience-spring-framework-7-core-resilience-retryable-concurrencylimit)
- [17.41 Timeout budjeti / deadline propagatsiyasi (Timeouts Budget / Deadline Propagation)](#1741-timeout-budjeti--deadline-propagatsiyasi-timeouts-budget--deadline-propagation)
- [17.42 Retry bo'roni (Retry Storm — anti-pattern)](#1742-retry-boroni-retry-storm--anti-pattern)

</details>


Taqsimlangan tizimlarda nosozlik istisno emas, balki normal holat: tarmoq kechikadi, downstream servis javob bermaydi, ma'lumotlar bazasi connection pool'i to'lib qoladi. Resilience va cloud dizayn patternlari aynan shu haqiqat bilan ishlashga qaratilgan — ular nosozlikni yo'q qilmaydi, balki uni lokalizatsiya qiladi, tez aniqlaydi va tizimning qolgan qismini himoyalaydi. Arxitektor uchun bu patternlar kritik, chunki mikroservis muhitida bitta sekin servis cascading failure orqali butun platformani to'xtatib qo'yishi mumkin. Spring ekotizimida bu patternlar Resilience4j, Spring Cloud Gateway, Spring Retry va Spring Framework 6.x'ning `@HttpExchange`/`RestClient` infratuzilmasi orqali deklarativ tarzda qo'llanadi.

## 17.1 Qayta urinish (Retry — exponential backoff, jitter)

**Tavsif:** Vaqtinchalik (transient) nosozliklar — tarmoq paketining yo'qolishi, qisqa muddatli DB deadlock, HTTP 503 — ko'pincha o'z-o'zidan tuzaladi, shuning uchun operatsiyani bir necha marta qayta bajarish muvaffaqiyat ehtimolini oshiradi. Exponential backoff har urinish orasidagi kutish vaqtini geometrik ravishda oshiradi (100ms, 200ms, 400ms...), bu downstream servisga tiklanish uchun vaqt beradi. Jitter — kutish vaqtiga tasodifiy og'ish qo'shish — ko'p mijozning bir vaqtda qayta urinishidan kelib chiqadigan "thundering herd" effektini yo'q qiladi. Retry faqat idempotent yoki xavfsiz qayta bajarilishi mumkin bo'lgan operatsiyalar uchun qo'llanadi.

**Spring'da qayerda uchraydi:** Spring Retry kutubxonasi `@EnableRetry` va `@Retryable`/`@Recover` annotatsiyalarini beradi, programmatik yondashuv uchun `RetryTemplate` bilan `ExponentialBackOffPolicy` va `ExponentialRandomBackOffPolicy` (jitter) mavjud. Spring Framework 6.1+ o'zining `org.springframework.core.retry.RetryTemplate` va `RetryPolicy` abstraksiyasini kiritdi, shuningdek `@Retryable` Spring Framework 7.x'da core'ga ko'chirildi. Resilience4j'da `io.github.resilience4j.retry.Retry` va `RetryConfig` (`intervalFunction(IntervalFunction.ofExponentialRandomBackoff(...))`), Spring Boot 3.x uchun `resilience4j-spring-boot3` starter'i `@Retry(name = "...")` annotatsiyasini taqdim etadi. Kafka tomonida `DefaultErrorHandler` + `ExponentialBackOffWithMaxRetries` va `@RetryableTopic`, JDBC uchun `spring.datasource.hikari` darajasida emas, balki `TransactionTemplate` ustida retry qo'llanadi.

**Qo'llanish keyslari:**
- To'lov provayderining REST API'si 503 qaytarganda buyurtmani tasdiqlash chaqiruvini 3 marta exponential backoff bilan qayta yuborish.
- PostgreSQL'da `40001` serialization failure xatosi bo'lganda tranzaksiyani avtomatik qayta bajarish.
- Kafka consumer'ida deserializatsiya emas, balki downstream HTTP xatosi sababli muvaffaqiyatsiz bo'lgan message'ni `@RetryableTopic` orqali kechiktirib qayta ishlash.
- S3 yoki boshqa object storage'ga fayl yuklashda tarmoq timeout'idan keyin qayta urinish.
- Service discovery'dan yangi instance ko'tarilayotganda `Connection refused` xatosini qisqa retry bilan yashirish.

**Ehtiyot bo'ling:** Non-idempotent operatsiyalarni (masalan, `POST /payments` idempotency key'siz) retry qilish dublikat to'lovlarga olib keladi; retry'ni har bir qatlamda takrorlash (gateway + client + service) urinishlar sonini ko'paytirib, downstream'ni butunlay cho'ktiradi. Retry'ni albatta timeout va circuit breaker bilan birga ishlatish, hamda 4xx (client xatosi) uchun retry qilmaslik kerak.

## 17.2 Zanjirni uzgich (Circuit Breaker)

**Tavsif:** Downstream servis barqaror ishdan chiqqanda har bir chaqiruvni timeout'gacha kutish thread'larni va resurslarni behuda sarflaydi. Circuit Breaker nosozlik foizini kuzatadi va belgilangan chegaradan oshganda "ochiq" holatga o'tib, chaqiruvlarni darhol rad etadi (fail fast). Belgilangan vaqtdan keyin "yarim ochiq" holatga o'tib, bir nechta sinov chaqiruvini o'tkazadi va servis tiklangan bo'lsa zanjirni yopadi. Shu tariqa cascading failure to'xtatiladi va downstream'ga tiklanish imkoniyati beriladi.

**Spring'da qayerda uchraydi:** Standart yechim — Resilience4j: `io.github.resilience4j.circuitbreaker.CircuitBreaker`, `CircuitBreakerConfig` (`slidingWindowType`, `failureRateThreshold`, `slowCallRateThreshold`, `waitDurationInOpenState`) va `@CircuitBreaker(name = "paymentApi", fallbackMethod = "fallback")` annotatsiyasi `resilience4j-spring-boot3` starter'i orqali. Spring Cloud Circuit Breaker abstraksiyasi `CircuitBreakerFactory`/`ReactiveCircuitBreakerFactory` va `spring-cloud-starter-circuitbreaker-resilience4j` bilan implementatsiyani almashtirishga imkon beradi; Spring Cloud Gateway'da `CircuitBreaker` filtri mavjud. Holat o'zgarishlari Micrometer orqali `resilience4j.circuitbreaker.state` metrikasi va Spring Boot Actuator'ning `/actuator/health` va `/actuator/circuitbreakerevents` endpoint'larida ko'rinadi. Netflix Hystrix allaqachon end-of-life, yangi loyihalarda ishlatilmaydi.

**Qo'llanish keyslari:**
- Tashqi KYC yoki credit scoring provayderi ishdan chiqqanda onboarding oqimini sekinlashtirmasdan rad etish.
- Mikroservislar orasidagi sinxron REST chaqiruvlarda bitta sekin servis sababli thread pool'ning to'lib qolishini oldini olish.
- Spring Cloud Gateway'da route darajasida circuit breaker qo'yib, nosoz backend uchun statik degraded javob qaytarish.
- Recommendation engine javob bermaganda mahsulot sahifasini personalizatsiyasiz ko'rsatish.
- Legacy SOAP integratsiyasining sekin javoblarini `slowCallRateThreshold` bilan nosozlik deb hisoblab zanjirni uzish.

**Ehtiyot bo'ling:** Juda kichik sliding window yoki juda past threshold tasodifiy xatolar sababli zanjirni noo'rin ochadi (flapping), juda katta `waitDurationInOpenState` esa servis tiklangandan keyin ham trafikni bloklaydi. Circuit breaker'ni har bir downstream uchun alohida nomlash shart — bitta umumiy breaker barcha integratsiyalarni birga o'chiradi.

## 17.3 To'siq (Bulkhead)

**Tavsif:** Kema korpusidagi suv o'tkazmas bo'limlar nomidan olingan bu pattern resurslarni (thread pool, connection, semaphore permit) izolyatsiyalangan qismlarga bo'ladi, shunda bitta integratsiyaning resurs tanqisligi qolganlariga yuqmaydi. Semaphore bulkhead bir vaqtda ishlayotgan chaqiruvlar sonini cheklaydi, thread pool bulkhead esa har bir downstream uchun alohida executor ajratadi. Natijada sekin servis faqat o'ziga ajratilgan kvotani iste'mol qiladi, umumiy thread pool'ni egallab olmaydi.

**Spring'da qayerda uchraydi:** Resilience4j'da `io.github.resilience4j.bulkhead.Bulkhead` (semaphore asosida, `maxConcurrentCalls`, `maxWaitDuration`) va `ThreadPoolBulkhead` (`coreThreadPoolSize`, `queueCapacity`), deklarativ ko'rinishda `@Bulkhead(name = "ledger", type = Bulkhead.Type.THREADPOOL)`. Spring MVC'da Tomcat'ning `server.tomcat.threads.max` va HikariCP'ning `maximum-pool-size` sozlamalari orqali fizik bulkhead quriladi — masalan har bir DataSource uchun alohida pool. Java 21+ virtual thread'lar (`spring.threads.virtual.enabled=true`) thread tanqisligini kamaytiradi, lekin downstream'ni himoyalash uchun semaphore bulkhead baribir kerak; reaktiv stack'da `Schedulers.newBoundedElastic(...)` bilan izolyatsiya qilinadi.

**Qo'llanish keyslari:**
- Reporting uchun og'ir analitik so'rovlarni alohida DataSource va alohida Hikari pool'ga ajratish.
- Sekin tashqi PDF generatsiya servisiga bir vaqtda maksimum 10 chaqiruv ruxsat berib, qolgan API'larni himoyalash.
- Admin va public API'larni turli Tomcat connector yoki turli deployment'da ajratish.
- Kafka consumer group'lari uchun alohida `concurrency` sozlab, kritik va kritik bo'lmagan topic'larni izolyatsiyalash.
- Multi-tenant SaaS'da bitta yirik tenant'ning batch yuklamasi boshqa tenant'larni sekinlashtirmasligi uchun kvota ajratish.

**Ehtiyot bo'ling:** Haddan tashqari mayda bulkhead'lar resurslarni fragmentlashtiradi va umumiy throughput'ni pasaytiradi, chunki bo'sh turgan permit'lar boshqa yo'nalishga ishlatilmaydi. Thread pool bulkhead'ni `ThreadLocal`'ga (SecurityContext, MDC, transaction) tayanadigan kodda ehtiyotkorlik bilan ishlatish kerak — kontekst avtomatik ko'chmaydi.

## 17.4 Timeout (Timeout)

**Tavsif:** Cheksiz kutish taqsimlangan tizimdagi eng xavfli xatolardan biri: javob kelmasa thread, connection va memory band bo'lib qoladi. Timeout har bir tashqi chaqiruvga qat'iy vaqt budjeti belgilaydi va u o'tganda operatsiyani uzib, xatoni yuqoriga uzatadi. To'g'ri loyihalashda timeout'lar zanjir bo'ylab kamayib boradi (end-to-end budget > downstream timeout), shunda yuqori qatlam quyi qatlamdan oldin uzilmaydi.

**Spring'da qayerda uchraydi:** `RestClient`/`RestTemplate` uchun `ClientHttpRequestFactorySettings` yoki `JdkClientHttpRequestFactory`/`ReactorClientHttpConnector` orqali connect va read timeout; Spring Boot 3.x'da `spring.http.client.connect-timeout` va `spring.http.client.read-timeout` property'lari mavjud. `WebClient` uchun `.responseTimeout(...)` va reaktiv `Mono.timeout(...)`, `@Transactional(timeout = 5)` va `JpaRepository` so'rovlarida `jakarta.persistence.query.timeout` hint'i, HikariCP'da `connectionTimeout` va `validationTimeout`. Resilience4j'da `TimeLimiter` va `@TimeLimiter(name = "...")` (`CompletableFuture`/reaktiv tiplar bilan ishlaydi), Spring MVC'da asinxron so'rovlar uchun `spring.mvc.async.request-timeout`.

**Qo'llanish keyslari:**
- Tashqi narx hisoblash servisiga 800ms budjet qo'yib, undan oshsa cache'dagi narxga o'tish.
- HTTP so'rov uchun umumiy SLA 2s bo'lganda ichki uchta chaqiruvga 600ms'lik timeout taqsimlash.
- Uzun ishlaydigan analitik so'rovni `@Transactional(timeout = 30)` bilan cheklab, DB connection'ni bo'shatish.
- Webhook qabul qiluvchi endpoint'da downstream yozuvni 1s bilan cheklab, qolganini asinxron navbatga surish.
- Mobil klient uchun gateway darajasida global response timeout belgilash.

**Ehtiyot bo'ling:** Default timeout'larga tayanmaslik kerak — ko'p HTTP client va driver'larda u cheksiz yoki juda katta; shuningdek timeout'ni retry bilan ko'paytirganda umumiy kutish vaqti `timeout × urinishlar` bo'lib, foydalanuvchi SLA'sidan oshib ketadi. Timeout uzilgandan keyin server tomonda ish davom etishi mumkin, shuning uchun non-idempotent operatsiyalarda "noaniq holat" (unknown outcome) ni hisobga olish zarur.

## 17.5 Chastota cheklovchi (Rate Limiter)

**Tavsif:** Rate limiter ma'lum vaqt oynasida ruxsat etilgan chaqiruvlar sonini cheklab, resursni haddan tashqari yuklamadan himoyalaydi va adolatli taqsimotni ta'minlaydi. Odatda token bucket, leaky bucket yoki sliding window algoritmlari bilan amalga oshiriladi va limit oshganda HTTP 429 `Too Many Requests` hamda `Retry-After` header'i qaytariladi. U ham kiruvchi trafikni (API quota), ham chiquvchi chaqiruvlarni (tashqi provayder kvotasi) boshqarish uchun qo'llanadi.

**Spring'da qayerda uchraydi:** Spring Cloud Gateway'da `RequestRateLimiter` filtri `RedisRateLimiter` (token bucket, `replenishRate`/`burstCapacity`) va `KeyResolver` bean'i bilan ishlaydi. Resilience4j'da `io.github.resilience4j.ratelimiter.RateLimiter`, `RateLimiterConfig` (`limitForPeriod`, `limitRefreshPeriod`, `timeoutDuration`) va `@RateLimiter(name = "providerApi")`; distributed limit uchun Bucket4j kutubxonasi Redis/Hazelcast backend bilan keng ishlatiladi. Spring Security'ning o'zi rate limiting bermaydi, shuning uchun odatda `OncePerRequestFilter` yoki gateway qatlami ishlatiladi; API kalit bo'yicha limitni `KeyResolver` orqali `X-API-Key` header'idan olish mumkin.

**Qo'llanish keyslari:**
- Public REST API'da har bir API kalit uchun daqiqada 600 so'rov limitini qo'yish.
- Tashqi SMS provayderining sekundiga 50 xabar kvotasini chiquvchi tomonda hurmat qilish.
- Login va parolni tiklash endpoint'larida brute-force hujumini IP bo'yicha cheklash.
- Free va premium tarif foydalanuvchilariga turli limit berib monetizatsiya qilish.
- Batch import job'ining downstream API'ga bosimini sekundiga belgilangan darajada ushlab turish.

**Ehtiyot bo'ling:** In-memory rate limiter bir nechta instance'da gorizontal scaling vaqtida limitni instance soniga ko'paytirib yuboradi — distributed hisoblash uchun Redis kerak. Limit kalitini noto'g'ri tanlash (masalan, NAT ortidagi barcha foydalanuvchilar uchun bitta IP) real foydalanuvchilarni bloklab qo'yadi.

## 17.6 Bo'g'ish (Throttling)

**Tavsif:** Throttling rate limiting'ga yaqin, lekin diqqati — so'rovni butunlay rad etmasdan, uning tezligini pasaytirish yoki navbatga qo'yish orqali tizimni barqaror yuklamada ushlab turish. Amalda bu chaqiruvni kechiktirish (backpressure), kamroq muhim ishni past prioritetga o'tkazish yoki degraded rejimda xizmat ko'rsatishni bildiradi. Maqsad — pik yuklamada tizim butunlay qulamasligi, balki sekinroq, ammo ishlashda davom etishi.

**Spring'da qayerda uchraydi:** Resilience4j `RateLimiter`'ning `timeoutDuration` parametri permit kutishni tashkil qilib, amalda throttling beradi (rad etish o'rniga bloklash). Reaktiv stack'da `Flux.limitRate(...)`, `onBackpressureBuffer(...)`, `delayElements(...)` va `Schedulers`'ning bounded navbatlari bilan backpressure amalga oshiriladi; `ThreadPoolTaskExecutor`'da `queueCapacity` va `CallerRunsPolicy` rejection policy'si producer'ni sekinlashtiradi. Kafka tomonida `max.poll.records`, `fetch.max.bytes` va `ConcurrentKafkaListenerContainerFactory`'ning `concurrency` sozlamasi iste'mol tezligini boshqaradi, Spring Batch'da esa `chunkSize` va throttle qilingan `TaskExecutor` ishlatiladi.

**Qo'llanish keyslari:**
- Kechaki hisobot generatsiyasini ish vaqtida sekinlashtirib, OLTP yuklamasini himoyalash.
- Kafka consumer'ni downstream API kvotasiga moslab sekundiga belgilangan message'ga tushirish.
- Migration yoki backfill job'ini DB CPU 70% dan oshganda avtomatik sekinlashtirish.
- Bepul tarif foydalanuvchilariga javobni ataylab kechiktirib (soft throttle) premium'ga rag'batlantirish.
- Reaktiv SSE stream'ida sekin klient uchun `onBackpressureBuffer` bilan element tezligini moslashtirish.

**Ehtiyot bo'ling:** Throttling'ni bloklovchi kutish bilan amalga oshirish thread'larni band qilib, bulkhead buzilishiga olib keladi — reaktiv yoki asinxron modelni afzal ko'rish kerak. Cheksiz buffer bilan backpressure qilish esa `OutOfMemoryError`'ga va kechikishning portlashiga sabab bo'ladi.

## 17.7 Zaxira yechim (Fallback)

**Tavsif:** Fallback asosiy yo'l ishlamaganda tizimga to'liq xato qaytarish o'rniga pastroq sifatli, ammo maqbul javob berish imkonini beradi (graceful degradation). Bu cache'dagi eski ma'lumot, statik default qiymat, bo'sh ro'yxat yoki soddalashtirilgan hisob-kitob bo'lishi mumkin. Fallback odatda circuit breaker, retry yoki timeout bilan birga, ular zanjir uzilganini aniqlagandan keyin ishga tushadi.

**Spring'da qayerda uchraydi:** Resilience4j annotatsiyalarining `fallbackMethod` atributi (`@CircuitBreaker(name="x", fallbackMethod="fallbackX")`) — fallback metod bir xil imzoga ega bo'lib, oxirida `Throwable` parametri qabul qiladi. Spring Cloud Circuit Breaker API'da `circuitBreakerFactory.create("x").run(supplier, throwable -> fallbackValue)`, Spring Cloud Gateway'da `CircuitBreaker` filtrining `fallbackUri` (masalan `forward:/fallback/products`) sozlamasi. Spring Cache abstraksiyasi (`@Cacheable`, `CacheManager`, Caffeine yoki Redis) stale ma'lumotni fallback sifatida saqlash uchun ishlatiladi, `@Recover` esa Spring Retry'da barcha urinishlar tugaganda chaqiriladigan fallback'ni belgilaydi.

```java
@CircuitBreaker(name = "pricing", fallbackMethod = "cachedPrice")
public Price fetch(String sku) {
    return restClient.get().uri("/price/{sku}", sku)
            .retrieve().body(Price.class);
}

private Price cachedPrice(String sku, Throwable ex) {
    return priceCache.get(sku, () -> Price.listPrice(sku));
}
```

**Qo'llanish keyslari:**
- Personalizatsiya servisi ishlamaganda bestseller mahsulotlarning statik ro'yxatini ko'rsatish.
- Valyuta kursi API'si javob bermaganda oxirgi muvaffaqiyatli olingan kursni cache'dan ishlatish.
- Fraud scoring servisi o'chganda tranzaksiyani qo'lda ko'rib chiqish navbatiga yuborish.
- Recommendation yoki reyting bo'limini mahsulot sahifasida butunlay yashirib, qolgan sahifani ko'rsatish.
- Gateway'da backend o'chganda `fallbackUri` orqali "xizmat vaqtincha mavjud emas" JSON javobini qaytarish.

**Ehtiyot bo'ling:** Moliyaviy yoki huquqiy ahamiyatga ega ma'lumotlarda (balans, limit, narx) eski cache'ni jim fallback sifatida berish noto'g'ri qarorlarga olib keladi — bunday joylarda fail fast afzal. Fallback'ning o'zi tashqi resursga murojaat qilsa, u ham ishdan chiqishi mumkin, shuning uchun fallback iloji boricha lokal va deterministik bo'lishi va albatta metrikaga yozilishi kerak.

## 17.8 Tez ishdan chiqish (Fail Fast)

**Tavsif:** Agar operatsiya muvaffaqiyatsiz bo'lishi oldindan ma'lum bo'lsa, uni boshlamasdan darhol xato qaytarish — resursni va vaqtni tejaydi. Bu konfiguratsiyani startup'da validatsiya qilish, kiruvchi so'rovni ishlashdan oldin tekshirish yoki zanjir ochiq bo'lganda chaqiruvni rad etishni o'z ichiga oladi. Fail fast sekin nosozlikdan (slow failure) afzal, chunki sekin nosozlik thread'larni ushlab qolib, cascading failure'ni kuchaytiradi.

**Spring'da qayerda uchraydi:** `@Validated` va Jakarta Bean Validation (`@NotNull`, `@Valid`) kiruvchi DTO'ni controller darajasida darhol rad etadi; `@ConfigurationProperties` + `@Validated` noto'g'ri konfiguratsiyada kontekstni ko'tarilishiga yo'l qo'ymaydi. `spring.datasource.hikari.initialization-fail-timeout` va `spring.main.lazy-initialization=false` (default) ilova ishga tushganda bog'liqliklarni tekshiradi; `spring.config.import` va `spring.cloud.config.fail-fast=true` Config Server mavjud bo'lmaganda startup'ni to'xtatadi. `Assert.notNull(...)`, `Objects.requireNonNull(...)` va Spring Boot Actuator'ning readiness probe'i (`/actuator/health/readiness`) ham shu pattern xizmatida; Resilience4j'ning ochiq zanjiri `CallNotPermittedException` bilan darhol fail qiladi.

**Qo'llanish keyslari:**
- Majburiy environment variable yo'q bo'lsa ilovani startup'da to'xtatib, yarim ishlaydigan deployment'ni oldini olish.
- So'rov body'si validatsiyadan o'tmaganda DB'ga tegmasdan 400 qaytarish.
- Kafka listener'da noto'g'ri schema'li message'ni darhol DLT'ga yuborish.
- Zanjir ochiq bo'lganda tashqi chaqiruvni urinmasdan 503 bilan rad etish.
- Liquibase/Flyway migratsiyasi muvaffaqiyatsiz bo'lsa ilovani ishga tushirmaslik.

**Ehtiyot bo'ling:** Fail fast'ni haddan tashqari qo'llash vaqtinchalik nosozlikda ham foydalanuvchiga xato ko'rsatadi — transient xatolar uchun retry yoki fallback bilan muvozanatlash kerak. Shuningdek, kritik bo'lmagan bog'liqlik (masalan, metrics backend) uchun startup'ni to'xtatish ilovaning mavjudligini asossiz kamaytiradi.

## 17.9 Barqaror holat (Steady State)

**Tavsif:** Michael Nygard'ning "Release It!" kitobidagi bu pattern tizim inson aralashuvisiz uzoq muddat ishlashi kerakligini talab qiladi: har qanday o'suvchi resurs (log, cache, temp fayl, DB jadvali, session) uchun avtomatik tozalash mexanizmi bo'lishi shart. Aks holda disk to'ladi, cache memory'ni yeb qo'yadi yoki jadval shunchalik o'sadiki, so'rovlar sekinlashadi. Maqsad — resurs iste'moli vaqt o'tishi bilan barqaror darajada qolishi.

**Spring'da qayerda uchraydi:** Caffeine cache'da `maximumSize`, `expireAfterWrite`, `expireAfterAccess` (`spring.cache.caffeine.spec`), Redis'da TTL (`RedisCacheConfiguration.entryTtl(...)`); Spring Session'da `spring.session.timeout` va Redis/JDBC session cleanup job'i. Spring Batch metadata jadvallarini tozalash uchun `JobRepository` bilan ishlaydigan rejali job, `@Scheduled` + `TaskScheduler` yoki Quartz orqali purge vazifalari yoziladi; Logback'ning `SizeAndTimeBasedRollingPolicy` va `maxHistory`/`totalSizeCap` log o'sishini cheklaydi (`logging.logback.rollingpolicy.*` property'lari). Hikari'da `maxLifetime` va `idleTimeout` connection'lar eskirishini oldini oladi, Micrometer metrikalari (`jvm.memory.used`, `hikaricp.connections.active`) esa drift'ni kuzatish uchun ishlatiladi.

**Qo'llanish keyslari:**
- Audit log jadvalini 90 kundan keyin arxivlab, partitsiyani o'chiradigan rejali job.
- Caffeine cache'ga `maximumSize` qo'yib, heap'ning cheksiz o'sishini to'xtatish.
- Yuklangan vaqtinchalik fayllarni kecha bo'yi tozalaydigan `@Scheduled` vazifa.
- Kafka topic'lar uchun retention va compaction policy'sini aniq belgilash.
- Spring Batch'ning `BATCH_JOB_EXECUTION` jadvallarini davriy ravishda qisqartirish.

**Ehtiyot bo'ling:** Tozalash job'ining o'zi katta `DELETE` bilan jadvalni bloklab, ishlab chiqarishda incident keltirib chiqarishi mumkin — batch'lab, kichik porsiyalarda va kam yuklamali vaqtda bajarish kerak. "Faqat o'sadigan" jadval va cheksiz cache'lar odatda yuklamani oshirgandan bir necha oy o'tib, eng noqulay paytda sinadi.

## 17.10 Qo'l berib so'rashuv (Handshaking)

**Tavsif:** Handshaking — chaqiruvchi ish yuklamasini yuborishdan oldin server o'zining qabul qilishga qodirligini e'lon qilishi. Server o'zini "band" deb belgilab, load balancer yoki klientga yangi so'rov yubormaslikni aytadi va shu bilan o'zini haddan tashqari yuklamadan himoyalaydi. Bu pattern health check, readiness probe va protokol darajasidagi flow control (masalan TCP window, HTTP/2 flow control) orqali amalga oshadi.

**Spring'da qayerda uchraydi:** Spring Boot Actuator'ning `/actuator/health/liveness` va `/actuator/health/readiness` endpoint'lari `ApplicationAvailability` va `AvailabilityChangeEvent` bilan ishlaydi — `AvailabilityState.REFUSING_TRAFFIC` holatiga o'tgan instance Kubernetes readiness probe orqali Service endpoint'laridan chiqariladi. Custom `HealthIndicator`/`ReactiveHealthIndicator` bean'lari pool to'lganda `Status.OUT_OF_SERVICE` qaytarishi mumkin; graceful shutdown (`server.shutdown=graceful`, `spring.lifecycle.timeout-per-shutdown-phase`) yangi so'rovlarni qabul qilishni to'xtatib, mavjudlarini tugatadi. Spring Cloud LoadBalancer'da `HealthCheckServiceInstanceListSupplier` nosog'lom instance'larni chetlab o'tadi, reaktiv stack'da esa Reactive Streams'ning `request(n)` signali protokol darajasidagi handshaking rolini bajaradi.

**Qo'llanish keyslari:**
- Kubernetes'da readiness probe orqali DB migratsiyasi tugamagan pod'ga trafik yubormaslik.
- Deployment vaqtida graceful shutdown bilan ishlayotgan so'rovlarni yo'qotmasdan pod'ni almashtirish.
- Thread pool to'lganda `HealthIndicator`'ni `OUT_OF_SERVICE` qilib, load balancer'dan vaqtincha chiqib turish.
- gRPC yoki HTTP/2 flow control orqali stream tezligini klient qabul qilish qobiliyatiga moslashtirish.
- Batch worker'ning "men yana bitta chunk olaman" signalini orchestrator'ga yuborishi.

**Ehtiyot bo'ling:** Health check'ni downstream bog'liqliklarga bog'lab qo'yish (masalan, tashqi API o'chganda readiness'ni fail qilish) butun klaster bir vaqtda trafikdan chiqishiga olib keladi — liveness va readiness semantikasini aniq ajratish zarur. Og'ir health check'lar o'zi yuklamaga aylanadi, shuning uchun ularni cache'lash (`management.endpoint.health.cache.time-to-live`) tavsiya etiladi.

## 17.11 Sinov qurilmasi (Test Harness)

**Tavsif:** Test harness — real integratsiyalarning "yomon xulq-atvorini" ataylab simulyatsiya qiluvchi sinov infratuzilmasi: sekin javoblar, yarim o'qilgan connection, noto'g'ri formatdagi javob, TCP reset. Oddiy mock faqat protokolning "baxtli yo'lini" tekshiradi, test harness esa tarmoq va protokol darajasidagi nosozliklarni qayta ishlab, resilience kodining haqiqatda ishlashini isbotlaydi. Bu patternsiz timeout, retry va circuit breaker sozlamalari faqat nazariy qoladi.

**Spring'da qayerda uchraydi:** WireMock (`spring-cloud-contract-wiremock` yoki `wiremock-standalone`) `withFixedDelay`, `withChunkedDribbleDelay` va `Fault.CONNECTION_RESET_BY_PEER` bilan nosoz downstream'ni modellashtiradi; `MockRestServiceServer` va `MockWebServer` (OkHttp) ham shu maqsadda ishlatiladi. Testcontainers (`org.testcontainers:postgresql`, `kafka`, `toxiproxy`) real infratuzilmani ko'taradi va ToxiproxyContainer orqali latency, bandwidth cheklovi va connection uzilishini kiritadi; Spring Boot 3.1+ `@ServiceConnection` va `@DynamicPropertySource` bilan konteyner ulanishini avtomatik ulaydi. Spring Boot Test'da `@SpringBootTest`, `@MockitoBean` (3.4+) va Spring Cloud Contract Stub Runner, xaos injection uchun esa Spring Cloud'ning Chaos Monkey for Spring Boot kutubxonasi qo'llanadi.

**Qo'llanish keyslari:**
- WireMock'da 5 sekundlik kechikish qo'yib, `RestClient` read timeout'ining haqiqatda ishlashini tekshirish.
- Toxiproxy bilan DB connection'ni uzib, HikariCP va retry xatti-harakatini kuzatish.
- Circuit breaker'ning ochilish va yarim ochiq holatga o'tishini WireMock scenario'lari bilan tasdiqlash.
- Kafka konteynerini qayta ishga tushirib, consumer rebalance va offset commit mantiqini sinash.
- Noto'g'ri JSON yoki kutilmagan HTTP 500 javobida fallback metodning chaqirilishini tekshirish.

**Ehtiyot bo'ling:** Test harness sekin va beqaror (flaky) testlar manbasi bo'lishi mumkin, shuning uchun uni unit test emas, alohida integratsiya yoki resilience test suite'ida saqlash kerak. Harness real protokol darajasida ishlamasa (faqat Java exception tashlasa), tarmoq darajasidagi muammolarni — masalan yarim ochiq connection'ni — aniqlay olmaydi.

## 17.12 Ajratuvchi middleware (Decoupling Middleware)

**Tavsif:** Sinxron chaqiruv chaqiruvchi va chaqiriluvchining mavjudligini bir vaqtda talab qiladi — biri o'chsa, ikkinchisi ham bloklanadi. Decoupling middleware (message broker, event bus, navbat) ikki tomonni vaqt bo'yicha ajratadi: producer xabarni qo'yadi va ketadi, consumer tayyor bo'lganda o'qiydi. Natijada temporal coupling yo'qoladi, yuklama pik vaqtida navbat buffer rolini bajaradi va consumer'ni mustaqil scale qilish mumkin bo'ladi.

**Spring'da qayerda uchraydi:** Spring for Apache Kafka (`KafkaTemplate`, `@KafkaListener`, `ConcurrentKafkaListenerContainerFactory`), Spring AMQP/RabbitMQ (`RabbitTemplate`, `@RabbitListener`), Spring JMS (`JmsTemplate`, `@JmsListener`) va Spring Cloud Stream'ning funksional modeli (`Supplier`, `Function`, `Consumer` bean'lari + binder'lar). Tranzaksion ishonchlilik uchun Transactional Outbox pattern'i `@Transactional` ichida outbox jadvaliga yozish va Debezium CDC bilan publish qilish orqali quriladi; ichki ajratish uchun `ApplicationEventPublisher` + `@TransactionalEventListener(phase = AFTER_COMMIT)` ishlatiladi. Spring Integration esa channel, adapter va `MessageChannel` abstraksiyalari bilan broker ustida yuqori darajali oqim qurish imkonini beradi.

**Qo'llanish keyslari:**
- Buyurtma yaratilgandan keyin email, SMS va analitikani event orqali asinxron ishlash.
- Hisob-kitob (billing) servisi o'chganda ham buyurtmalarni qabul qilishni davom ettirish.
- Black Friday pik yuklamasini Kafka navbatida buffer qilib, consumer'larni asta-sekin ishlatish.
- Legacy monolit bilan integratsiyani broker orqali qurib, versiyalarni mustaqil deploy qilish.
- Outbox pattern bilan DB yozuvi va event publish'ni atomik qilib, yo'qolgan xabarlarni oldini olish.

**Ehtiyot bo'ling:** Asinxronlik yakuniy izchillik (eventual consistency), dublikat xabarlar va tartibsiz yetib kelish muammolarini keltiradi — consumer'lar idempotent bo'lishi va DLT/DLQ strategiyasi oldindan o'ylanishi shart. Darhol javob talab qiladigan so'rov-javob oqimini (masalan, login) broker orqali qurish keraksiz murakkablik va kechikish qo'shadi.

## 17.13 Qulashiga yo'l ber (Let It Crash)

**Tavsif:** Erlang/OTP falsafasidan kelgan bu yondashuv har bir kutilmagan xatoni joyida tuzatishga urinish o'rniga, buzilgan komponentni o'ldirib, toza holatdan qayta ishga tushirishni taklif qiladi. Noma'lum holatda ishlashni davom ettirish ma'lumotlar buzilishiga olib keladi, toza restart esa deterministik va oson tushunarli. Bu supervisor (yoki orchestrator) tomonidan avtomatik qayta ishga tushirish va holatsiz (stateless) dizaynga tayanadi.

**Spring'da qayerda uchraydi:** Spring Boot'da `/actuator/health/liveness` muvaffaqiyatsiz bo'lganda Kubernetes liveness probe pod'ni restart qiladi — bu pattern'ning amaldagi ko'rinishi. `SpringApplication.exit(...)` va `ExitCodeGenerator`, `management.endpoint.restart` (Spring Cloud Actuator'da) hamda `@Scheduled` task'dagi tuzalmas xatoda `System.exit(1)` bilan ataylab tushish qo'llanadi; Kafka'da `CommonContainerStoppingErrorHandler` container'ni to'xtatib, orchestrator'ga restart imkonini beradi. `Thread.UncaughtExceptionHandler`, `OutOfMemoryError` uchun `-XX:+ExitOnOutOfMemoryError` JVM flag'i va Java 21 virtual thread'larda har bir task'ning izolyatsiyalangan failure'i ham shu falsafaga mos keladi.

**Qo'llanish keyslari:**
- `OutOfMemoryError`dan keyin JVM'ni darhol tugatib, Kubernetes'ga toza pod ko'tarishga ruxsat berish.
- Kafka consumer tuzalmas holatga tushganda container'ni to'xtatib, rebalance orqali boshqa instance'ga topshirish.
- Konfiguratsiya refresh muvaffaqiyatsiz bo'lsa ilovani restart qilib, noaniq sozlamada ishlamaslik.
- Batch job'ning tuzalmas xatosida non-zero exit code bilan chiqib, scheduler'ning retry mantiqiga tayanish.
- Stateless mikroservisda har qanday kutilmagan `Error` turida instance'ni almashtirish.

**Ehtiyot bo'ling:** Bu pattern faqat holat tashqarida (DB, broker, cache) saqlanganda va restart tez bo'lganda ishlaydi — stateful, sekin ko'tariladigan ilovada restart loop (`CrashLoopBackOff`) nosozlikni kuchaytiradi. Shuningdek, oddiy biznes xatolarini (validatsiya, 404) crash sababi deb hisoblash mutlaqo noto'g'ri: let it crash faqat tuzalmas, noma'lum holat uchun.

## 17.14 Yuklamani tashlash (Shed Load / Load Shedding)

**Tavsif:** Tizim imkoniyatidan ortiq yuklama kelganda barcha so'rovni qabul qilish kechikishni portlatadi va hammaga yomon xizmat beradi; load shedding esa so'rovlarning bir qismini ataylab rad etib (odatda HTTP 503 yoki 429), qolganiga normal SLA bilan xizmat ko'rsatadi. Rad etish tasodifiy bo'lishi mumkin, lekin yaxshi dizaynda prioritetga tayanadi: kritik bo'lmagan yoki past prioritetli trafik birinchi tashlanadi. Ko'pincha navbat uzunligi, kechikish yoki CPU kabi signal asosida adaptiv tarzda yoqiladi.

**Spring'da qayerda uchraydi:** Tomcat'ning `server.tomcat.max-connections`, `accept-count` va `threads.max` sozlamalari chegaradan oshgan connection'larni rad etib, eng past darajadagi shedding'ni beradi. Spring Cloud Gateway'da `RequestRateLimiter` filtri 429 qaytaradi, Resilience4j `Bulkhead`'ning `maxWaitDuration=0` sozlamasi permit bo'lmaganda `BulkheadFullException` bilan darhol rad etadi — bu amalda load shedding. Custom `OncePerRequestFilter` yoki `WebFilter` ichida Micrometer'dan olingan navbat kechikishi yoki `ThreadPoolTaskExecutor.getQueueSize()` qiymatiga qarab past prioritetli so'rovlarni 503 bilan qaytarish, hamda `Retry-After` header'ini qo'yish keng tarqalgan yondashuv; Kubernetes HPA bilan birgalikda shedding scale-up tugaguncha vaqt sotib beradi.

**Qo'llanish keyslari:**
- Flash sale paytida mahsulot ko'rish trafigining bir qismini rad etib, checkout oqimini butun saqlash.
- Navbatda 2 sekunddan ko'p kutgan so'rovni ishlashdan oldin bekor qilish (deadline-aware shedding).
- Bot va crawler trafigini yuklama pikida birinchi navbatda bloklash.
- Analitika va reporting API'sini DB yuklamasi kritik darajaga chiqqanda vaqtincha o'chirish.
- Autoscaling yangi instance ko'targuncha 503 va `Retry-After` bilan klientlarni kechiktirish.

**Ehtiyot bo'ling:** Shedding qoidasini noto'g'ri tanlash eng qimmatli foydalanuvchilarni yoki to'lov oqimini rad etib, biznesga retry bo'roni (retry storm) orqali qaytib keladigan zarar keltiradi — prioritet va `Retry-After` semantikasi aniq bo'lishi kerak. Rad etilgan so'rovlarni albatta alohida metrikaga yozish lozim, aks holda tizim "sog'lom" ko'rinib, muammo yashirin qoladi.

## 17.15 Orqa bosim (Back Pressure)

**Tavsif:** Producer consumer'dan tezroq ma'lumot ishlab chiqarganda tizim xotirasi to'lib ketadi yoki queue cheksiz o'sib ketadi. Back Pressure patterni consumer'ga "sekinlashtir" signalini producer tomon qaytarish mexanizmini beradi: demand-based (pull) model, buffer limiti, yoki ataylab sekinlashtirish. Resilience nuqtai nazaridan bu OutOfMemoryError va kaskadli ishdan chiqishdan saqlaydigan eng asosiy himoya chizig'i. Reactive Streams spetsifikatsiyasining mag'zi aynan shu: `Subscription.request(n)` orqali consumer o'zi qancha element qabul qilishini e'lon qiladi.

**Spring'da qayerda uchraydi:** Project Reactor va Reactive Streams (`org.reactivestreams.Subscription#request`) Spring WebFlux'da default mexanizm — `Flux`/`Mono` ichida `onBackpressureBuffer()`, `onBackpressureDrop()`, `onBackpressureLatest()`, `onBackpressureError()` operatorlari mavjud; `limitRate(n)` prefetch hajmini boshqaradi. `Flux.create(sink, FluxSink.OverflowStrategy.DROP)` push manbalari uchun strategiya belgilaydi. Spring Kafka'da `ConcurrentMessageListenerContainer` uchun `ContainerProperties#setMaxPollRecords` va `MessageListenerContainer#pause()`/`resume()` (`ConsumerSeekAware` bilan birga) ishlaydi; `KafkaMessageListenerContainer` idle holatda `Consumer#pause` chaqirib brokerdan oqimni to'xtatadi. Spring Integration'da `QueueChannel` sig'imi (`new QueueChannel(100)`) va `PollerMetadata` orqali pull tezligi cheklanadi. Java 21+ `java.util.concurrent.Flow` API va `SubmissionPublisher` ham shu modelni beradi; `ThreadPoolExecutor` + `ArrayBlockingQueue` + `CallerRunsPolicy` esa klassik, bloklovchi back pressure usuli.

**Qo'llanish keyslari:**
- WebFlux'da sekin HTTP client'ga katta ma'lumot stream qilishda `limitRate()` bilan DB kursorini sekinlashtirish.
- Kafka consumer'da tashqi API sekinlashganda `container.pause()` chaqirib rebalansdan saqlanish.
- R2DBC'dan million qatorli natijani fayl eksportiga quyib, xotirani 200 MB ichida ushlab turish.
- Fayl yuklash endpoint'ida `DataBuffer` oqimini disk yozish tezligiga bog'lash.
- Thread pool'ni `CallerRunsPolicy` bilan to'ldirib, batch job'ni o'z-o'zidan sekinlashtirish.

**Ehtiyot bo'ling:** `onBackpressureBuffer()` ni limitsiz ishlatish back pressure'ni butunlay yo'q qiladi — muammoni faqat OOM'ga suradi, shuning uchun har doim `maxSize` va overflow strategiyasini bering. Blocking I/O (JDBC, `RestTemplate`) reactive pipeline ichida ishlatilsa demand signali ma'nosini yo'qotadi: event loop thread'i bloklanadi va back pressure o'rniga butun server muzlaydi.

## 17.16 Hokim / tezlik cheklovchi nazoratchi (Governor)

**Tavsif:** Governor patterni tizimdagi resurs iste'molini uzluksiz kuzatib, belgilangan chegaraga yaqinlashganda ishlash tezligini avtomatik ravishda pasaytiradi yoki oshiradi — bug' mashinasidagi markazdan qochma regulyator kabi. Oddiy rate limiter'dan farqi: statik limit emas, balki o'lchangan metrikaga (latency, xato foizi, CPU, queue uzunligi) qarab adaptiv tarzda sozlanadi. Bu ortiqcha yuklanishni oldini oladi va downstream servisni himoya qiladi. Ko'pincha AIMD (additive increase, multiplicative decrease) yoki Little qonuni asosidagi konkurensiya limiti ko'rinishida amalga oshiriladi.

**Spring'da qayerda uchraydi:** Netflix `concurrency-limits` kutubxonasi (`com.netflix.concurrency.limits.limit.VegasLimit`, `GradientLimit`, `Limiter`) adaptiv konkurensiya governor'ini beradi va `ConcurrencyLimitServletFilter` sifatida Spring Boot'ga filter bo'lib ulanadi. Resilience4j'ning `Bulkhead`/`RateLimiter` konfiguratsiyasini `RateLimiterRegistry#rateLimiter(name, config)` orqali runtime'da almashtirish mumkin — Micrometer metrikasini o'qiydigan `@Scheduled` komponent bilan birgalikda governor hosil bo'ladi. Spring Batch'da `TaskExecutorRepeatTemplate` va `ThrottledTaskExecutor`, Spring Integration'da `PollerMetadata` trigger intervalini dinamik o'zgartirish ishlatiladi. Micrometer `MeterRegistry` + `Gauge` metrikalari qaror uchun kirish ma'lumotini beradi; Kubernetes muhitida HPA (external metrics) infratuzilma darajasidagi governor rolini bajaradi.

**Qo'llanish keyslari:**
- Downstream servis p99 latency oshganda konkurent so'rovlar sonini avtomatik kamaytirish.
- Batch migratsiyada ishlab chiqarish DB CPU 70%'dan oshsa chunk tezligini pasaytirish.
- Tashqi API 429 javoblari ko'paysa so'rov tezligini AIMD bilan moslashtirish.
- Kafka consumer'da lag o'sganda concurrency'ni oshirib, lag tushganda qaytarib kamaytirish.
- Ko'p tenant'li tizimda bir tenant resursni egallab olganda uning kvotasini vaqtincha siqish.

**Ehtiyot bo'ling:** Governor nazorat halqasi noto'g'ri sozlansa tebranish (oscillation) paydo bo'ladi — tezlik ko'tarilib-tushib tizim beqaror ishlaydi; hysteresis va smoothing (EWMA) qo'shing hamda sensor oynasi reaksiya vaqtidan kattaroq bo'lsin. Har bir instance mustaqil governor yuritganda umumiy yuk kutilganidan N barobar oshishi mumkin, shuning uchun global chegara uchun markazlashgan koordinatsiya yoki instance'ga bo'lingan kvota kerak.

## 17.17 Salomatlik endpoint monitoringi (Health Endpoint Monitoring)

**Tavsif:** Servis o'z holati haqida mashina o'qiy oladigan HTTP endpoint ochadi va tashqi monitoring tizimi, load balancer yoki orkestrator shu endpoint orqali instance'ning trafik qabul qilishga tayyorligini aniqlaydi. Tekshiruv faqat "process tirikmi" emas, balki kritik bog'liqliklar (DB, broker, cache) ishlayotganini ham qamraydi. Liveness (qayta ishga tushirish kerakmi) va readiness (trafik berish mumkinmi) ni ajratish muhim, chunki ular butunlay boshqa qarorlarga xizmat qiladi.

**Spring'da qayerda uchraydi:** Spring Boot Actuator `/actuator/health` endpoint'ini beradi; `HealthIndicator` va `ReactiveHealthIndicator` interfeyslari (yoki `AbstractHealthIndicator`) o'z tekshiruvini yozish uchun ishlatiladi, natija `Health.up()/down()/outOfService()` bilan qaytariladi. Auto-konfiguratsiya qilingan indikatorlar: `DataSourceHealthIndicator`, `RedisHealthIndicator`, `MongoHealthIndicator`, `KafkaHealthIndicator` (Spring Kafka), `DiskSpaceHealthIndicator`. Kubernetes uchun `management.endpoint.health.probes.enabled=true` `/actuator/health/liveness` va `/actuator/health/readiness` guruhlarini yoqadi; `ApplicationAvailability`, `LivenessState`, `ReadinessState` va `AvailabilityChangeEvent` kod ichidan holatni boshqarishga imkon beradi. `management.endpoint.health.group.*` bilan maxsus guruh tuzish, `management.server.port` bilan alohida port ajratish mumkin. Spring Boot 3.x'da graceful shutdown (`server.shutdown=graceful`) readiness'ni avtomatik `REFUSING_TRAFFIC` holatiga o'tkazadi.

**Qo'llanish keyslari:**
- Kubernetes readiness probe uchun DB connection pool tayyor bo'lishini kutib trafikni kechiktirish.
- AWS ALB target group health check bilan nosog'lom instance'ni rotatsiyadan chiqarish.
- Deploy paytida graceful shutdown bilan 503 xatolarsiz pod almashtirish.
- Kritik tashqi provayder uzilganda `outOfService` qaytarib avtomatik alert chiqarish.
- Blue-green deploy'da yangi versiya o'z-o'zini tekshirib, so'ngra trafik almashtirish.

**Ehtiyot bo'ling:** Liveness probe'ga DB yoki tashqi API tekshiruvini qo'shish eng keng tarqalgan xato — DB qisqa vaqt uzilganda butun klaster o'z-o'zini cheksiz restart qila boshlaydi (restart bo'roni); bog'liqlik tekshiruvi faqat readiness'da bo'lsin. Health endpoint'ni autentifikatsiyasiz ommaviy ochish tizim ichki tuzilishini fosh qiladi, shuning uchun `management.endpoint.health.show-details=when-authorized` qo'ying va management portni tashqi tarmoqdan yoping.

## 17.18 Queue asosida yukni tekislash (Queue-Based Load Leveling)

**Tavsif:** Producer va consumer o'rtasiga queue qo'yilib, kelayotgan so'rovlar portlashi (burst) buffer'da to'planadi va consumer o'z barqaror tezligida ishlov beradi. Shu bilan backend eng yuqori cho'qqiga emas, o'rtacha yukka mo'ljallab o'lchamlanadi va vaqtinchalik yuk portlashi xizmatni sindirmaydi. Qo'shimcha foyda: producer va consumer bir-biridan vaqt bo'yicha ajratiladi, ya'ni consumer vaqtincha o'chsa ham so'rovlar yo'qolmaydi.

**Spring'da qayerda uchraydi:** Spring for Apache Kafka (`KafkaTemplate`, `@KafkaListener` + `ConcurrentKafkaListenerContainerFactory`), Spring AMQP/RabbitMQ (`RabbitTemplate`, `@RabbitListener`, `SimpleMessageListenerContainer` yoki `DirectMessageListenerContainer`), Spring JMS (`JmsTemplate`, `@JmsListener`, `DefaultMessageListenerContainer`). Spring Cloud Stream `spring-cloud-stream-binder-kafka`/`-rabbit` bilan `Supplier`/`Function`/`Consumer` funksional bind'larini beradi. Jarayon ichidagi variant uchun Spring Integration `QueueChannel` + `PollerMetadata`, yoki `ThreadPoolTaskExecutor` ning `LinkedBlockingQueue` navbati. Davomiylik talab qilinsa `JdbcChannelMessageStore` yoki Spring Batch `JobRepository` ishlatiladi; concurrency `ContainerProperties`/`SimpleRabbitListenerContainerFactory#setConcurrency` bilan boshqariladi.

**Qo'llanish keyslari:**
- Qora juma sotuvida buyurtma qabulini tezkor saqlab, to'lov va ombor ishlovini queue orqali tekislash.
- Hisobot/PDF generatsiyasi kabi og'ir vazifalarni HTTP so'rovdan ajratib fon ishchisiga uzatish.
- SMS/email yuborish provayderining sekundiga limitiga queue drenaji orqali moslashish.
- IoT qurilmalaridan kelgan telemetriyani portlashlar bilan qabul qilib, barqaror tezlikda DB'ga yozish.
- Legacy mainframe integratsiyasida kunlik oynaga to'plangan so'rovlarni bosqichma-bosqich uzatish.

**Ehtiyot bo'ling:** Queue cheksiz o'ssa kechikish ham cheksiz o'sadi — bu "yashirin ishdan chiqish": tizim ishlayotgandek ko'rinadi, lekin javoblar allaqachon foydasiz; queue uzunligi va xabar yoshiga alert qo'ying, TTL va dead-letter queue belgilang. Queue sinxron so'rov-javob semantikasini o'zgartiradi, shuning uchun client eventual natijaga va takroriy yetkazishga (at-least-once) tayyor bo'lishi, consumer esa idempotent yozilishi shart.

## 17.19 Prioritetli navbat (Priority Queue)

**Tavsif:** Barcha so'rovlar bir xil emas: ba'zilari biznes uchun muhimroq yoki qat'iy SLA'ga ega. Priority Queue patterni xabarlarni muhimlik darajasiga qarab ajratib, yuqori prioritetli ishlarni oldin bajaradi. Amaliyotda ikki yo'l bor: brokerning o'z prioritet maydoni, yoki har bir prioritet uchun alohida queue va alohida (ko'pincha kattaroq) consumer pool. Ikkinchi yondashuv taqsimlangan tizimlarda ancha bashoratli ishlaydi.

**Spring'da qayerda uchraydi:** Spring AMQP RabbitMQ'ning prioritet queue'sini qo'llab-quvvatlaydi: `QueueBuilder.durable("tasks").maxPriority(10).build()` va `MessageProperties#setPriority(int)` (yoki `MessagePostProcessor` ichida). JMS uchun `JmsTemplate#setPriority` va `setExplicitQosEnabled(true)`. Kafka'da prioritet maydoni yo'q, shuning uchun topic-per-priority modeli ishlatiladi: `orders.high`, `orders.normal` topiclari va har biriga alohida `@KafkaListener(topics = "...", concurrency = "...")`. Jarayon ichida `PriorityBlockingQueue` bilan `ThreadPoolTaskExecutor`, Spring Integration'da `PriorityChannel` (+ `MessageGroupQueue`/`Comparator`) mavjud. Spring Scheduling'da `@Order` yoki maxsus `Comparator<Runnable>` ham yordam beradi.

**Qo'llanish keyslari:**
- To'lov tranzaksiyalarini analitik event'lardan ustun qo'yib ishlov berish.
- Premium (enterprise) mijoz so'rovlarini bepul tarif foydalanuvchilaridan oldin bajarish.
- Incident/alert xabarlarini oddiy bildirishnomalardan oldin yuborish.
- Interaktiv foydalanuvchi so'rovini fon qayta hisoblash (reindex) ishidan ustun qo'yish.
- Muddati tugayotgan SLA'li buyurtmalarni navbat boshiga ko'tarish.

**Ehtiyot bo'ling:** Eng keng tarqalgan tuzoq — starvation: yuqori prioritet oqimi to'xtamasa, past prioritetli ishlar hech qachon bajarilmaydi; shu sababli past queue uchun kafolatlangan ulush (weighted fair share) yoki navbatda kutish vaqtiga qarab prioritet oshirish (aging) kiritiladi. RabbitMQ prioriteti faqat queue ichida kutib turgan xabarlarga ta'sir qiladi — consumer prefetch katta bo'lsa xabarlar allaqachon client'da bo'lib, prioritet amalda ishlamaydi, shuning uchun `prefetch` ni kichik qiymatga (1-5) tushiring.

## 17.20 Yetakchini saylash (Leader Election)

**Tavsif:** Bir nechta bir xil instance ishlayotganda ayrim vazifalar faqat bitta joyda bajarilishi kerak: scheduled job, cache yangilash, migratsiya yoki tashqi tizim bilan yakka kanal. Leader Election patterni instance'lar o'rtasida kelishuv orqali bitta yetakchini tanlaydi, qolganlari kuzatuvchi bo'lib turadi va yetakchi ishdan chiqsa yangisi saylanadi. Asos sifatida taqsimlangan lock (TTL bilan) yoki konsensus algoritmi (Raft, ZAB) ishlatiladi.

**Spring'da qayerda uchraydi:** Spring Integration `spring-integration-core` `LockRegistryLeaderInitiator` sinfini beradi va u `LockRegistry` implementatsiyalari bilan ishlaydi: `JdbcLockRegistry` (`spring-integration-jdbc`, `INT_LOCK` jadvali), `RedisLockRegistry` (`spring-integration-redis`), `ZookeeperLockRegistry` (`spring-integration-zookeeper`), `HazelcastLockRegistry`. Hodisalar `OnGrantedEvent`/`OnRevokedEvent` `ApplicationEvent` lari bilan yetib keladi, `Candidate`/`Context#yield()` esa yetakchilikni ixtiyoriy topshirishga imkon beradi. Spring Cloud Zookeeper `LeaderInitiator` wrapper'ini, Spring Cloud Kubernetes `spring-cloud-kubernetes-fabric8-leader` esa ConfigMap/Lease asosidagi saylovni taqdim etadi. Alternativa: ShedLock (`net.javacrumbs.shedlock`) `@SchedulerLock` annotatsiyasi bilan — bu to'liq saylov emas, lekin "bir martalik bajarish" talabini soddaroq hal qiladi. Quartz klaster rejimi (`org.quartz.jobStore.isClustered=true`) ham shu muammoni DB lock bilan yechadi.

**Qo'llanish keyslari:**
- `@Scheduled` kunlik hisobot job'ini 10 ta pod ichida faqat bitta marta ishga tushirish.
- Tashqi SFTP/legacy tizimga yakka polling ulanishini ushlab turish.
- Kafka topic'dan global agregatsiya hisoblovchi yakka ishchi tanlash.
- Taqsimlangan cache uchun yakka warm-up/invalidation koordinatori.
- DB sxema migratsiyasini klaster ishga tushganda faqat bir instance'da bajarish.

**Ehtiyot bo'ling:** Split-brain xavfi real: lock TTL tugaganda eski yetakchi hali o'zini yetakchi deb o'ylab turishi mumkin, shuning uchun har bir yozuvda fencing token yoki optimistik versiya tekshiruvi bo'lsin va GC pauzasi/tarmoq uzilishi TTL'dan uzun bo'lmasligini ta'minlang. Leader election'ni oddiy idempotent ishlar uchun ishlatish ortiqcha murakkablik — ko'p holatda DB'dagi unique constraint yoki ShedLock yetarli.

## 17.21 Rejalashtiruvchi–Agent–Nazoratchi (Scheduler Agent Supervisor)

**Tavsif:** Ko'p qadamli taqsimlangan ish oqimini uchta rolga bo'ladi: Scheduler qadamlar ketma-ketligini boshqaradi va holatni saqlaydi, Agent har bir qadamni masofaviy resursda bajaradi, Supervisor esa holatni kuzatib qotib qolgan yoki muvaffaqiyatsiz qadamlarni qayta urinish, kompensatsiya yoki eskalatsiya bilan tiklaydi. Bu pattern uzoq davom etuvchi, qisman ishdan chiqishga moyil jarayonlar uchun ishonchlilikni ta'minlaydi. Holat doimiy saqlangani uchun tizim istalgan nuqtadan tiklanishi mumkin.

**Spring'da qayerda uchraydi:** Spring Batch bu patternning tayyor amalga oshirilishi: `Job`/`Step`, `JobRepository` (holat saqlash), `JobLauncher`, `JobOperator#restart`, `StepExecution` va `ExitStatus`, `SkipPolicy`/`RetryPolicy`, `JobExplorer` orqali qotib qolgan execution'larni topish; remote partitioning/remote chunking (`spring-batch-integration`, `MessageChannelPartitionHandler`) agent rolini ajratadi. Spring Cloud Task + Spring Cloud Data Flow task launcher va `TaskRepository` bilan taqsimlangan agentlarni boshqaradi. Supervisor roli ko'pincha `@Scheduled` reaper komponenti bo'lib, `JobExplorer.findRunningJobExecutions(...)` natijasini `lastUpdated` bo'yicha tekshiradi. Murakkab oqimlar uchun Spring bilan yaxshi integratsiyalanadigan Temporal (`io.temporal:temporal-spring-boot-starter`) yoki Camunda/Flowable BPMN engine'lari ishlatiladi; Resilience4j `Retry` esa qadam darajasidagi qayta urinishni beradi.

**Qo'llanish keyslari:**
- Buyurtma bajarilishida to'lov, ombor va yetkazib berish qadamlarini holat bilan boshqarish va qotganini tiklash.
- Kechaki ETL pipeline'ini ishdan chiqqan qadamidan qayta ishga tushirish (restart from failed step).
- Tashqi KYC provayderidan javob kelmagan hollarda timeout bo'yicha qayta so'rov yuborish.
- Cloud resurs provisioning oqimini (VM, DNS, sertifikat) kompensatsiya bilan orqaga qaytarish.
- Uzoq davom etuvchi migratsiyani partitsiyalab ko'p agentga tarqatish va progressni nazorat qilish.

**Ehtiyot bo'ling:** Agent qadamlari idempotent bo'lmasa, supervisor qayta urinishi ikki marta to'lov yoki dublikat yozuv keltiradi — har bir qadamga idempotency key va natija yozuvini qo'shing. Supervisor "qotib qolgan" deb hisoblash chegarasi juda qisqa bo'lsa, hali ishlayotgan agent bilan ikkinchisi parallel ishlaydi: timeout qadamning real p99 vaqtidan ancha katta va lock bilan himoyalangan bo'lsin.

## 17.22 Asinxron so'rov-javob (Asynchronous Request-Reply)

**Tavsif:** Client sinxron javob kutmasligi kerak bo'lgan uzoq operatsiyalarda server so'rovni qabul qilib `202 Accepted` va status resursiga havola qaytaradi, keyin client shu havolani polling qiladi yoki callback/webhook orqali xabardor qilinadi. Shu bilan HTTP ulanishi uzoq ushlanmaydi, timeout va proxy cheklovlari muammosi yo'qoladi. Cloud nuqtai nazaridan bu backend'ni gorizontal masshtablash va queue bilan birlashtirish uchun standart shakl.

**Spring'da qayerda uchraydi:** Spring MVC'da `ResponseEntity.accepted().location(uri).build()` bilan 202 + `Location` header qaytariladi; uzoq so'rovlar uchun `DeferredResult<T>`, `Callable<T>`, `WebAsyncTask`, `StreamingResponseBody` va SSE uchun `SseEmitter` mavjud. Reactive tomonda `Mono`/`Flux` qaytaruvchi `@RestController` va `ServerSentEvent`; `@Async` + `CompletableFuture` (`AsyncConfigurer`, `ThreadPoolTaskExecutor`) fon bajarilishini beradi. Holatni saqlash uchun oddiy `JdbcTemplate`/JPA jadvali yoki Redis; ishni queue'ga uzatish uchun `KafkaTemplate`/`RabbitTemplate`. Callback yuborishda `RestClient` (Spring Framework 6.1+) yoki `WebClient` ishlatiladi; WebSocket orqali push uchun `SimpMessagingTemplate` (STOMP).

```java
@PostMapping("/reports")
ResponseEntity<Void> create(@RequestBody ReportRequest req) {
    String id = jobs.enqueue(req);              // queue + holat yozuvi
    return ResponseEntity.accepted()
            .location(URI.create("/reports/" + id))
            .build();
}

@GetMapping("/reports/{id}")
ResponseEntity<?> status(@PathVariable String id) {
    Job job = jobs.find(id);
    return job.done() ? ResponseEntity.ok(job.result())
                      : ResponseEntity.accepted().body(job.progress());
}
```

**Qo'llanish keyslari:**
- Katta hisobot yoki video transkodlash so'rovini 202 bilan qabul qilib, keyin yuklab olish havolasini berish.
- Tashqi API gateway 30 soniyalik timeout'iga sig'maydigan operatsiyalarni polling modeliga o'tkazish.
- To'lov provayderidan webhook callback kutib, buyurtma holatini keyinchalik yangilash.
- Mobil ilovada uzoq import jarayonini progress bar bilan ko'rsatish (SSE yoki polling).
- Bulk foydalanuvchi importini fon job'ga uzatib, natija faylini keyin taqdim etish.

**Ehtiyot bo'ling:** Polling intervalini client ixtiyoriga qoldirmang — `Retry-After` header bering, aks holda minglab client sekundiga bir marta so'rab status servisini yuklaydi. Holat resursi uchun TTL va tozalash siyosati bo'lmasa status jadvali cheksiz o'sadi; shuningdek status endpoint'i avtorizatsiyani tekshirmasa, ID taxmin qilib boshqa foydalanuvchi natijasini o'qish mumkin bo'ladi.

## 17.23 Statik kontentni hosting qilish (Static Content Hosting)

**Tavsif:** Rasm, CSS, JS, shrift va yuklab olinadigan fayllarni ilova server'i orqali berish o'rniga to'g'ridan-to'g'ri obyekt saqlash (S3, Azure Blob, GCS) va CDN'dan taqdim etish. Bu ilova instance'laridagi CPU, thread va tarmoq yukini keskin kamaytiradi, kechikishni foydalanuvchiga yaqin edge'ga olib boradi va arzon masshtablashni beradi. Backend faqat dinamik ma'lumot va biznes mantiqi bilan shug'ullanadi.

**Spring'da qayerda uchraydi:** Spring Boot default `/static`, `/public`, `/resources`, `/META-INF/resources` kataloglaridan statik resurs beradi; `WebMvcConfigurer#addResourceHandlers` va `ResourceHandlerRegistration#setCacheControl(CacheControl.maxAge(365, DAYS).cachePublic())` bilan cache boshqariladi. Cache-busting uchun `spring.web.resources.chain.strategy.content.enabled=true` (`VersionResourceResolver`, `ContentVersionStrategy`) ishlatiladi. Haqiqiy tashqi hostingga o'tishda Spring Cloud AWS (`io.awspring.cloud:spring-cloud-aws-starter-s3`) `S3Template`/`S3Resource` va `s3://` protokolli `Resource` ni beradi; AWS SDK v2 `S3Presigner` esa pre-signed URL yasaydi. Azure uchun `spring-cloud-azure-starter-storage-blob` (`BlobServiceClient`), GCP uchun `spring-cloud-gcp-starter-storage` (`Storage`, `GoogleStorageResource`). Ko'pincha controller faqat CDN URL yoki 302 redirect qaytaradi.

**Qo'llanish keyslari:**
- SPA (React/Angular) bundle'ini S3 + CloudFront'dan berib, Spring Boot'ni faqat REST API qoldirish.
- Mahsulot rasmlari va avatarlarni CDN orqali global kechikishni kamaytirib taqdim etish.
- Katta PDF hisobotlarni blob storage'ga yozib, foydalanuvchiga vaqtinchalik havola berish.
- Mobil ilova uchun versiyalangan konfiguratsiya/asset fayllarini edge'dan tarqatish.
- Ko'p tenant'li tizimda tenant brending fayllarini ilova deploy'idan ajratib saqlash.

**Ehtiyot bo'ling:** Bucket'ni ommaviy o'qishga ochib qo'yish eng ko'p uchraydigan xavfsizlik xatosi — maxfiy fayllar uchun pre-signed URL yoki CDN signed URL ishlatib, bucket'ni private qoldiring. Cache-busting versiyalanmagan fayl nomlari bilan uzoq `max-age` berish deploy'dan keyin eski asset'lar qotib qolishiga olib keladi; dinamik yoki foydalanuvchiga xos kontentni esa CDN'da keshlash ma'lumot aralashib ketish xavfini tug'diradi.

## 17.24 Valet kaliti (Valet Key)

**Tavsif:** Client ma'lumotni ilova server'i orqali o'tkazmasdan to'g'ridan-to'g'ri saqlash xizmatiga yuklashi yoki undan o'qishi uchun cheklangan huquqli, muddati chegaralangan token (pre-signed URL yoki SAS) beriladi. Token aniq bir obyektga, aniq amalga (GET yoki PUT) va qisqa vaqtga bog'langani uchun xavf minimal bo'ladi. Natijada ilova server'i katta fayl oqimini o'tkazish yukidan butunlay xalos bo'ladi.

**Spring'da qayerda uchraydi:** AWS SDK for Java v2 `S3Presigner` (`presignPutObject`, `presignGetObject` + `PutObjectPresignRequest`) — Spring Cloud AWS'ning `S3Template#createSignedGetURL(bucket, key, Duration)` va `createSignedPutURL(...)` metodlari shuni o'raydi. Azure'da `spring-cloud-azure-starter-storage-blob` orqali olingan `BlobClient#generateSas(BlobServiceSasSignatureValues)`, GCP'da `Storage#signUrl(BlobInfo, duration, unit, SignUrlOption...)`. Spring tomonida bu odatda `@RestController`'da avtorizatsiyadan keyin URL qaytaruvchi endpoint bo'ladi (`@PreAuthorize` bilan himoyalangan), va yuklash tugaganini bilish uchun S3 event notification → SQS/SNS → `@SqsListener` (Spring Cloud AWS) zanjiri qo'yiladi.

**Qo'llanish keyslari:**
- Foydalanuvchi 2 GB video faylni to'g'ridan-to'g'ri S3'ga yuklashi (browser'dan PUT).
- Xususiy hisobot faylini 5 daqiqa amal qiladigan havola bilan yuklab olishga berish.
- Mobil ilovada rasm yuklashni backend proxy'siz amalga oshirib mobil trafikni tezlashtirish.
- Hamkor tizimga faqat bitta prefiks ichidagi fayllarni o'qish huquqini vaqtincha berish.
- Katta CSV import faylini client'dan olib, keyin fon job bilan ishlov berish.

**Ehtiyot bo'ling:** Token muddatini uzoq qilish (kunlar) yoki URL'ni log, analitika yoki Referer orqali oqib ketishiga yo'l qo'yish — havola o'zi hokimiyat bo'lgani uchun uni qo'lga kiritgan har kim foydalanadi; muddatni daqiqalar bilan o'lchang va URL'ni hech qachon log'ga yozmang. Valet key bilan kelgan faylni ishonchli deb hisoblamang: content-type, hajm limiti (`ContentLengthRange`/SAS shartlari) va virus skanerlashni yuklashdan keyingi event orqali majburiy qiling.

## 17.25 Darvozabon (Gatekeeper)

**Tavsif:** Client bilan ilova o'rtasiga maxsus, imtiyozsiz vositachi instance qo'yiladi: u so'rovni qabul qiladi, tekshiradi, tozalaydi va faqat shundan keyin ichki servisga yo'naltiradi. Gatekeeper'da hech qanday maxfiy kalit yoki ma'lumot saqlanmaydi, shuning uchun u buzib kirilsa ham hujumchi ichki tizimga to'g'ridan-to'g'ri yeta olmaydi. Bu Bulkhead'ning xavfsizlik o'lchovidagi ko'rinishi: hujum sathi tashqi perimetr bilan cheklanadi.

**Spring'da qayerda uchraydi:** Spring Cloud Gateway (`spring-cloud-starter-gateway`, Spring Boot 3.x'da reactive `RouteLocator`/`GatewayFilter`, yoki `spring-cloud-starter-gateway-mvc` servlet varianti) tipik gatekeeper rolini bajaradi: `RequestRateLimiter`, `CircuitBreaker`, `StripPrefix`, `RemoveRequestHeader` filterlari va `GlobalFilter` implementatsiyalari. Spring Security `SecurityFilterChain` (`HttpSecurity#oauth2ResourceServer`, `csrf`, `headers`, `cors`) token tekshiruvi va header qattiqlashtirishni ta'minlaydi; `OncePerRequestFilter` o'z validatsiya qatlamini qo'shadi. Kirish ma'lumotini tozalash uchun `@Validated` + Jakarta Bean Validation (`jakarta.validation` annotatsiyalari) va `@ControllerAdvice` xato normalizatsiyasi. Ichki servislar faqat mTLS yoki tarmoq policy orqali gateway'dan kirishga ruxsat beradi; service mesh (Istio sidecar) ham shu rolni infratuzilma darajasida bajaradi.

**Qo'llanish keyslari:**
- Public API trafigini DMZ'dagi gateway orqali o'tkazib, ichki microservislarni tarmoqdan yashirish.
- Token validatsiyasi, rate limiting va payload hajmi tekshiruvini bir joyda markazlashtirish.
- Legacy backend oldiga zamonaviy autentifikatsiya va TLS terminatsiyasini qo'shish.
- Hamkor (B2B) integratsiyalarida IP allowlist va schema validatsiyasini perimetrda bajarish.
- Ichki admin servislarni faqat VPN'dan kiradigan alohida gateway orqasiga qo'yish.

**Ehtiyot bo'ling:** Gatekeeper'ga DB credential, API kalit yoki biznes mantiqi joylashtirish uning butun ma'nosini yo'q qiladi — u imtiyozsiz va "ahmoq" qolishi kerak. Shuningdek gateway yagona ishdan chiqish nuqtasi va bo'g'iz bo'lib qolmasligi uchun kamida ikki instance, o'z circuit breaker'i va health check'i bo'lsin; ichki servislar esa gateway'ni aylanib o'tish mumkin emasligini tarmoq darajasida ta'minlasin (zero trust: ichkarida ham autentifikatsiya qoldiring).

## 17.26 Federatsiyalangan identifikatsiya (Federated Identity)

**Tavsif:** Ilova foydalanuvchi parolini o'zi saqlamaydi va tekshirmaydi, balki autentifikatsiyani ishonchli tashqi identity provider'ga (IdP) topshiradi va undan kelgan token yoki assertion asosida qarorlar qabul qiladi. Cloud nuqtai nazaridan bu ko'p ilova va ko'p tenant bo'ylab SSO, markazlashgan MFA va xodim ketganda bir joydan bloklashni beradi. Protokollar: OpenID Connect (OAuth 2.x ustida), SAML 2.0, va servis-servis uchun client credentials.

**Spring'da qayerda uchraydi:** Spring Security 6.x: `spring-boot-starter-oauth2-client` (`HttpSecurity#oauth2Login`, `ClientRegistrationRepository`, `OAuth2AuthorizedClientManager`, `spring.security.oauth2.client.registration.*`), `spring-boot-starter-oauth2-resource-server` (`oauth2ResourceServer(o -> o.jwt(...))`, `JwtDecoder`, `JwtAuthenticationConverter`, `issuer-uri` orqali JWKS discovery), va `spring-security-saml2-service-provider` (`saml2Login`, `RelyingPartyRegistrationRepository`). Servis-servis chaqiruvlarida `RestClient`/`WebClient` ga token qo'shish uchun `OAuth2ClientHttpRequestInterceptor` yoki `ServletOAuth2AuthorizedClientExchangeFilterFunction`. O'z IdP'ingizni qurish kerak bo'lsa Spring Authorization Server (`spring-boot-starter-oauth2-authorization-server`, `RegisteredClientRepository`) mavjud; amalda ko'proq Keycloak, Okta yoki Entra ID ishlatiladi. Rollar uchun `JwtGrantedAuthoritiesConverter` claim'larni `GrantedAuthority` ga aylantiradi.

**Qo'llanish keyslari:**
- Korporativ Entra ID/Okta bilan SSO qilib, xodimlar uchun alohida parol saqlamaslik.
- Ko'p tenant'li SaaS'da har bir mijozga o'z IdP'si (SAML yoki OIDC) bilan ulanish imkonini berish.
- Mobil va SPA client'lari uchun PKCE bilan Authorization Code flow'ni qo'llash.
- Microservislar o'rtasida client credentials token bilan servis identifikatsiyasi.
- MFA va shartli kirish siyosatini IdP darajasida markazlashtirib, ilova kodini o'zgartirmaslik.

**Ehtiyot bo'ling:** Tokenni faqat imzo bo'yicha tekshirish yetarli emas — `iss`, `aud`, `exp` va kerakli `scope`/claim'larni albatta validatsiya qiling (`JwtValidators`, `audience` konfiguratsiyasi), aks holda boshqa tenant yoki boshqa ilova uchun berilgan token qabul qilinadi. IdP yagona ishdan chiqish nuqtasi bo'lgani uchun uning uzilishi hamma ilovani to'xtatadi: JWKS keshi, token muddati va graceful degradation rejasi bo'lsin; shuningdek IdP'dan kelgan rollarni ko'r-ko'rona avtorizatsiya qarori sifatida ishlatmang, muhim huquqlarni o'z tomoningizda ham tekshiring.

## 17.27 Deploy shtamplari (Deployment Stamps)

**Tavsif:** Bitta katta umumiy (multi-tenant) tizim o'rniga butun stack'ning bir xil, mustaqil nusxalari ("stamp" yoki "cell") deploy qilinadi va har bir nusxa ma'lum tenant guruhi yoki region'ga xizmat qiladi. Masshtablash yangi stamp qo'shish bilan amalga oshadi, ishdan chiqish esa bitta stamp bilan cheklanadi — bu "blast radius" ni kichraytiradi. Trafikni to'g'ri stamp'ga yo'naltirish uchun oldinda traffic routing qatlami va tenant→stamp xaritasi bo'ladi.

**Spring'da qayerda uchraydi:** Bu avvalo infratuzilma patterni, lekin Spring tomonidan: har bir stamp o'z `spring.profiles.active` va alohida konfiguratsiyasi bilan ishlaydi (Spring Cloud Config `label`/profile, yoki Kubernetes ConfigMap/`spring-cloud-kubernetes-config`); `@ConfigurationProperties` orqali stamp identifikatori va DB ulanishi beriladi. Router qatlami Spring Cloud Gateway bo'lib, `GlobalFilter` ichida tenant claim'i yoki host nomiga qarab `ServerWebExchangeUtils.GATEWAY_REQUEST_URL_ATTR` ni stamp URL'iga o'rnatadi; service discovery uchun `DiscoveryClient` yoki Kubernetes Service. Observability'da stamp nomini `management.metrics.tags.stamp` (Micrometer common tag) yoki `MeterRegistryCustomizer` bilan barcha metrikaga qo'shish amaliyoti muhim. Har bir stamp uchun bir xil Helm/Terraform shabloni va bir xil Spring Boot artifact ishlatiladi — faqat konfiguratsiya farq qiladi.

**Qo'llanish keyslari:**
- Enterprise mijozlar uchun ma'lumot izolyatsiyasi talab qilinganda har biriga alohida stamp berish.
- Bitta stamp'ning Azure/AWS obuna limitiga (quota) urilishini yangi stamp qo'shib hal qilish.
- Ma'lumot rezidentligi talabi bo'yicha EU va US uchun alohida to'liq stack yuritish.
- Yangi versiyani bitta "canary stamp"da sinab, so'ngra qolganlarga tarqatish.
- Shovqinli qo'shni (noisy neighbor) muammosini tenant'larni stamp'larga bo'lib bartaraf etish.

**Ehtiyot bo'ling:** Operatsion narx chiziqli o'sadi: 20 ta stamp = 20 ta deploy, 20 ta migratsiya, 20 ta monitoring dashboard — avtomatlashtirish (IaC, GitOps) va versiyalarni bir xil ushlash disiplinasi bo'lmasa bu tezda boshqarib bo'lmas holga keladi. Tenant'ni bir stamp'dan boshqasiga ko'chirish ko'pincha eng og'ir ish bo'ladi, shuning uchun migratsiya yo'lini loyihaning boshida rejalashtiring; shuningdek stamp'lar orasida umumiy (shared) komponent ko'paygan sari izolyatsiya afzalligi yo'qoladi.

## 17.28 Geode (Geode)

**Tavsif:** Geode (geographical node) patterni ilovaning bir xil nusxalarini bir nechta geografik region'ga joylashtirib, ularning har biri har qanday so'rovga javob bera oladigan "active-active" tizim yasaydi. Trafik foydalanuvchiga eng yaqin yoki eng sog'lom geode'ga yo'naltiriladi, ma'lumot esa geo-replikatsiya qilingan global saqlashda turadi. Natijada juda past kechikish va region butunlay yo'qolganda ham ishlashda davom etish ta'minlanadi.

**Spring'da qayerda uchraydi:** Spring Boot ilovasi darajasida geode — bu bir xil artifact'ning bir necha region'da ishga tushirilishi, oldinda geo-DNS yoki anycast (Azure Front Door, AWS Global Accelerator, Cloudflare) bilan. Ma'lumot qatlami sifatida global-replikatsiyalangan saqlash ishlatiladi va Spring tomonida mos starter'lar mavjud: `spring-data-cosmos` (Azure Cosmos DB, multi-region writes), `spring-data-dynamodb`/AWS SDK v2 `DynamoDbEnhancedClient` (Global Tables), `spring-data-cassandra` (`CqlSessionBuilderCustomizer`, `LoadBalancingPolicy` bilan local-DC marshrutlash). Keshlash uchun Hazelcast WAN replication yoki Redis Enterprise active-active (`spring-boot-starter-data-redis`), event tarqatish uchun Kafka MirrorMaker 2 / cluster linking + Spring for Apache Kafka. Observability: `management.metrics.tags.region` common tag, `spring-boot-starter-actuator` health group'lari har bir region uchun.

**Qo'llanish keyslari:**
- Global iste'molchi ilovasida har bir qit'adagi foydalanuvchiga 50 ms'dan kam kechikish berish.
- Butun bir cloud region uzilganda trafikni DNS failover bilan avtomatik boshqa geode'ga o'tkazish.
- O'yin yoki real-time chat backend'ini o'yinchilarga yaqin joyda ishga tushirish.
- Qora juma kabi mintaqaviy yuk cho'qqilarini mahalliy geode bilan yutib yuborish.
- Ko'p regionli o'qishga mo'ljallangan katalog/narx servisini edge'ga yaqinlashtirish.

**Ehtiyot bo'ling:** Active-active yozuv konfliktlari (last-write-wins yoki CRDT) ma'lumot yo'qolishiga olib kelishi mumkin — konflikt hal qilish strategiyasini biznes qoidasi darajasida ongli tanlang, yoki yozuvni bitta region'da (write-leader) qoldirib faqat o'qishni tarqating. Geode juda qimmat va murakkab: faqat haqiqiy global auditoriya yoki qat'iy RTO/RPO talabi bo'lganda ma'noga ega, shuningdek ma'lumot rezidentligi (GDPR) qoidalari ba'zi ma'lumotni region'dan chiqarishni butunlay taqiqlaydi.

## 17.29 Edge ish yuklamasi konfiguratsiyasi (Edge Workload Configuration)

**Tavsif:** Edge (zavod, do'kon, filial, IoT gateway) qurilmalarida ishlayotgan yuzlab yoki minglab ilova instansiyalarini markazdan boshqarilgan konfiguratsiya bilan ta'minlash patterni. Markazda konfiguratsiya manbasi (hierarchiya: global → region → qurilma guruhi → qurilma) saqlanadi, edge esa uni tortib oladi va lokal nusxada keshlaydi, shu bilan tarmoq uzilganda ham ishlashni davom ettiradi. Asosiy muammo: har bir qurilmaga qo'lda sozlama kiritish imkonsiz, lekin har bir qurilmaning o'z xususiyatlari (sensorlar, tariflar, til) bor.

**Spring'da qayerda uchraydi:** Spring Cloud Config Server bilan profile va label hierarchiyasi (`spring.cloud.config.profile=plant-ankara`, `label`), `spring.cloud.config.fail-fast=false` va `spring.cloud.config.retry` — tarmoq yo'q bo'lsa lokal `application.yml` fallback'i bilan. Spring Cloud Bus (`spring-cloud-starter-bus-amqp`/`-kafka`) va `@RefreshScope` + `/actuator/refresh` orqali konfiguratsiya o'zgarishini qurilmalarga tarqatish. Spring Cloud Kubernetes `ConfigMap`/`Secret` PropertySource'lari K3s/MicroK8s edge klasterlarida; Spring Boot 3.x'da `ConfigDataLocationResolver` bilan o'z edge manbangizni (masalan, lokal SQLite yoki MQTT topic) ulash mumkin.

**Qo'llanish keyslari:**
- Retail tarmog'ida 2000 ta kassa terminaliga yangi soliq stavkasini markazdan tarqatish.
- Zavod sexlaridagi PLC gateway ilovalariga sensor kalibrovka koeffitsiyentlarini yuborish.
- Telekom bazaviy stansiyalarida joylashgan agent ilovalarning log darajasini (`logging.level`) masofadan o'zgartirish.
- Elektromobil zaryadlash stansiyalarida tarif jadvalini kunning vaqtiga qarab yangilash.
- Bank filiallaridagi lokal servislarga feature flag'larni bosqichma-bosqich yoqish.

**Ehtiyot bo'ling:** Edge qurilma soatlar yoki kunlar davomida offline bo'lishi mumkin, shuning uchun konfiguratsiya yangilanishi atomik va versiyalangan bo'lishi kerak — yarim qo'llanilgan konfiguratsiya qurilmani "o'lik" qoldiradi. Markaziy Config Server'ni qattiq dependency qilib qo'ymang (`fail-fast=true` edge'da xato); har doim lokal keshlangan oxirgi ishlagan versiyaga qaytish yo'li bo'lsin.

## 17.30 Tashqi konfiguratsiya ombori (External Configuration Store)

**Tavsif:** Konfiguratsiyani deployment artefaktidan (JAR, konteyner image) ajratib, tashqi markazlashgan omborda saqlash patterni. Shu bilan bir xil image'ni dev/stage/prod muhitlarida qayta build qilmasdan ishlatish, maxfiy ma'lumotlarni (secret) kod repositoriysidan chiqarib tashlash va konfiguratsiyani restart qilmasdan yangilash imkoniyati paydo bo'ladi. Odatda ombor versiyalangan (Git) yoki kalit-qiymat bazasi (Consul, etcd, Vault) bo'ladi.

**Spring'da qayerda uchraydi:** Spring Cloud Config Server (Git, JDBC, Vault, AWS S3 backend'lari), `spring-cloud-starter-config` client tomonida; Spring Cloud Consul Config, Spring Cloud Vault, Spring Cloud Kubernetes Config. Spring Boot 3.x'da `spring.config.import=configserver:`, `vault://`, `aws-parameterstore:`, `aws-secretsmanager:` (Spring Cloud AWS 3.x) — `ConfigData` API orqali. `@ConfigurationProperties` + `@RefreshScope`, `Environment`, `PropertySource` abstraksiyasi; `EnvironmentChangeEvent` va `RefreshScopeRefreshedEvent` hodisalari.

**Qo'llanish keyslari:**
- Bir xil konteyner image'ni dev, UAT va prod'da faqat environment'ga qarab turli DB URL bilan ishga tushirish.
- DB parollari va API kalitlarini Vault'da saqlab, ilovaga faqat ish vaqtida berish.
- Rate limit va timeout qiymatlarini deploy qilmasdan prod'da tuzatish (incident paytida).
- Feature flag'larni Consul KV'da boshqarish va `@RefreshScope` bean'larni qayta yaratish.
- Multi-tenant SaaS'da har bir tenant uchun alohida konfiguratsiya branch/label.

**Ehtiyot bo'ling:** Tashqi ombor single point of failure bo'lib qolmasin — client tomonda retry, timeout va lokal fallback bo'lishi shart; Config Server o'zi ham HA rejimda ishlashi kerak. `@RefreshScope` har qanday bean'ni "jonli" qilmaydi: `DataSource` connection pool'i yoki allaqachon ochilgan Kafka consumer'lar refresh'dan keyin kutilganidek qayta ulanmay qolishi mumkin, shuning uchun nimani refresh qilish mumkinligini aniq belgilang.

## 17.31 Gateway agregatsiyasi (Gateway Aggregation)

**Tavsif:** Client bir nechta backend servisga alohida-alohida so'rov yuborish o'rniga, gateway'ga bitta so'rov yuboradi; gateway esa kerakli servislarni (ko'pincha parallel) chaqirib, javoblarni bitta aggregate javobga birlashtiradi. Bu mobil va sekin tarmoqlarda chatty aloqa (N+1 HTTP so'rov) muammosini hal qiladi, latency va batareya sarfini kamaytiradi. Gateway shu bilan birga client'ni backend dekompozitsiyasidan izolyatsiya qiladi.

**Spring'da qayerda uchraydi:** Spring Cloud Gateway (`spring-cloud-starter-gateway`, Spring Boot 3.x) — reaktiv variant; Spring Cloud Gateway MVC (`spring-cloud-starter-gateway-mvc`) virtual thread'lar bilan. Agregatsiya mantig'i odatda alohida BFF (Backend for Frontend) servisda: `WebClient` + `Mono.zip()`/`Flux.zip()`, yoki Java 21+ `StructuredTaskScope` bilan `RestClient` chaqiruvlari. Spring GraphQL (`spring-boot-starter-graphql`) `@SchemaMapping`/`@BatchMapping` bilan agregatsiyaning deklarativ shakli; `DataLoader` N+1 muammosini bartaraf etadi.

```java
Mono<Dashboard> load(String userId) {
    return Mono.zip(
        client.get().uri("/profile/{id}", userId).retrieve().body(Profile.class),
        client.get().uri("/orders?user={id}", userId).retrieve().body(Orders.class),
        client.get().uri("/loyalty/{id}", userId).retrieve().body(Loyalty.class)
    ).map(t -> new Dashboard(t.getT1(), t.getT2(), t.getT3()));
}
```

**Qo'llanish keyslari:**
- Mobil ilova bosh ekranini bitta `/api/home` so'rovi bilan to'ldirish (profil + buyurtmalar + bonuslar).
- E-commerce mahsulot sahifasi uchun narx, qoldiq, sharh va tavsiyalarni birlashtirish.
- Bank ilovasida barcha hisob turlarini (karta, depozit, kredit) yagona balans ko'rinishiga yig'ish.
- Smart TV yoki IoT client'lari uchun kam sonli, yirik payload'li endpoint'lar yaratish.
- Legacy SOAP va yangi REST servislarni bitta zamonaviy JSON API ortida birlashtirish.

**Ehtiyot bo'ling:** Agregator eng sekin backend tezligida ishlaydi va bir nechta servisning birgalikdagi nosozligi ehtimolini oshiradi — har bir chaqiruvga alohida timeout, circuit breaker va partial-response (ba'zi bo'limlar `null`) strategiyasi kerak. Agregatsiya mantig'ini Gateway filter'lari ichiga yozib tashlamang: u tez business logic'ga aylanadi va gateway'ni deploy bog'liqligiga olib keladi — alohida BFF servis afzal.

## 17.32 Gateway offloading (Gateway Offloading)

**Tavsif:** Barcha servislarga umumiy bo'lgan ko'ndalang (cross-cutting) vazifalarni — TLS terminatsiyasi, autentifikatsiya, rate limiting, siqish, kesh, audit log — har bir servisda takrorlash o'rniga gateway yoki proxy qatlamiga ko'chirish patterni. Natijada business servislar yengillashadi, umumiy siyosatlar bir joyda markazlashadi va ularni bir marta yangilash kifoya. Bu, ayniqsa, legacy servislarni zamonaviy xavfsizlik talablariga moslashtirishda qulay.

**Spring'da qayerda uchraydi:** Spring Cloud Gateway built-in filter'lari: `RequestRateLimiter` (Redis bilan, `RedisRateLimiter`), `TokenRelay`, `RemoveRequestHeader`, `Retry`, `CircuitBreaker`, `ModifyResponseBody`. Spring Security Resource Server gateway darajasida (`spring-boot-starter-oauth2-resource-server`) JWT validatsiyasi, keyin downstream'ga header orqali identity uzatish. `GlobalFilter`/`GatewayFilterFactory` bilan custom offload; `spring.cloud.gateway.httpclient.ssl` va `server.ssl` TLS uchun. Ko'p holatda infrastruktura darajasida Envoy/NGINX Ingress yoki service mesh sidecar ham shu rolni bajaradi.

**Qo'llanish keyslari:**
- Barcha mikroservislar uchun JWT tekshiruvini gateway'da bir marta bajarish.
- Per-API-key rate limiting'ni Redis asosida markazlashtirish.
- TLS sertifikatlarini faqat gateway'da rotatsiya qilish, ichki trafikni mTLS mesh'ga topshirish.
- Gzip/Brotli siqish va response caching'ni edge'da bajarish.
- Legacy HTTP servisga tashqi dunyo uchun CORS va security header'larni qo'shish.

**Ehtiyot bo'ling:** Gateway'ni "hamma narsa" qatlamiga aylantirsangiz, u monolit va bottleneck'ga aylanadi — faqat haqiqatan universal vazifalarni ko'chiring. Autentifikatsiyani faqat gateway'da qoldirish xavfli: ichki trafik gateway'ni chetlab o'tishi mumkin, shuning uchun zero-trust tamoyili bilan servislar ham o'z tekshiruvini (hech bo'lmasa mTLS yoki ichki token) saqlashi kerak.

## 17.33 Gateway routing (Gateway Routing)

**Tavsif:** Bir nechta backend servisni bitta tashqi endpoint (bitta host va port) ortida yashirib, so'rovni path, header, metod, query yoki boshqa predikatlar asosida tegishli servisga yo'naltirish patterni. Client faqat bitta manzilni biladi, backend topologiyasi esa (servis bo'linishi, versiyalar, migratsiya) ichkarida erkin o'zgaradi. Shu bilan canary release, blue-green va strangler fig migratsiyalari ham mumkin bo'ladi.

**Spring'da qayerda uchraydi:** Spring Cloud Gateway `RouteLocator` / `RouteLocatorBuilder`, YAML'da `spring.cloud.gateway.routes[]` (`predicates: Path, Host, Method, Header, Weight, Cookie`; `filters: StripPrefix, RewritePath, SetPath`). `lb://service-id` URI sxemasi Spring Cloud LoadBalancer va discovery (Eureka, Consul, Spring Cloud Kubernetes) bilan; `DiscoveryClientRouteDefinitionLocator` avtomatik route yaratadi. `Weight` predikati canary uchun; Spring Cloud Gateway MVC esa `RouterFunctions` asosida bloklanuvchi stack'da bir xil imkoniyat beradi.

**Qo'llanish keyslari:**
- `/api/orders/**` → order-service, `/api/users/**` → user-service marshrutlash.
- Yangi versiyaga trafikning 5%ini `Weight` predikati bilan yuborish (canary).
- Monolitdan ajratilgan endpoint'ni yangi mikroservisga ko'chirish (strangler fig) client'ga sezdirmasdan.
- Mobil va web client'larni `Header=X-Client` bo'yicha turli backend'larga yo'naltirish.
- Multi-region deployment'da `Host` predikati orqali eng yaqin klasterga yuborish.

**Ehtiyot bo'ling:** Route tartibi (`order`) muhim — keng `Path=/**` route'i yuqorida turib qolsa, qolgan barcha qoidalar o'lik bo'ladi. Route konfiguratsiyasi ichiga murakkab shart va transformatsiyalar yozish kuzatilishi qiyin "yashirin logic"ga olib keladi; marshrutlashni oddiy saqlab, murakkab mantiqni servislarga qoldiring.

## 17.34 Ketma-ket konvoy (Sequential Convoy)

**Tavsif:** Parallel ishlovchi tizimda ma'lum guruhga tegishli xabarlarni (masalan, bitta buyurtma yoki bitta mijoz ID'si bo'yicha) kelgan tartibda, ketma-ket qayta ishlashni kafolatlaydigan pattern. Butun oqimni bitta thread'ga siqib qo'ymasdan, faqat bir guruh ichida tartib saqlanadi — turli guruhlar baribir parallel ishlanadi. Odatda bu partition kaliti yoki session identifikatori orqali amalga oshiriladi.

**Spring'da qayerda uchraydi:** Spring for Apache Kafka: partition kaliti (`ProducerRecord` key, `KafkaTemplate.send(topic, key, value)`) bir kalitni doimo bitta partitionga tushiradi, `@KafkaListener` + `ConcurrentKafkaListenerContainerFactory` esa har bir partitionni bitta consumer thread'da ishlaydi. Spring AMQP'da RabbitMQ consistent-hash exchange yoki single-active-consumer queue (`SingleActiveConsumer`). Spring Integration'da `Resequencer` (`@ServiceActivator` bilan `ResequencingMessageHandler`), `Aggregator` va `correlationId`; Spring Cloud Stream'da `partitionKeyExpression` va `partitionCount`. Spring JMS'da ActiveMQ message group (`JMSXGroupID`).

**Qo'llanish keyslari:**
- Bir buyurtma uchun `created → paid → shipped` hodisalarini tartibda qayta ishlash.
- Bankda bitta hisob bo'yicha debet/kredit operatsiyalarini ketma-ket qo'llash.
- CDC (Change Data Capture) oqimida bir row'ning UPDATE'larini tartibda replikatsiya qilish.
- IoT qurilmaning telemetriya o'zgarishlarini qurilma ID bo'yicha tartiblash.
- Chat yoki hamkorlikdagi hujjat tahririda bir xona ichidagi xabarlarni tartiblash.

**Ehtiyot bo'ling:** Partition kalitining notekis taqsimlanishi "hot partition" yaratadi — bitta yirik mijoz butun throughput'ni bloklaydi. Retry va dead-letter strategiyasini ehtiyotkorlik bilan tuzing: bitta xabarni cheksiz qayta urinish butun guruhni to'xtatadi (head-of-line blocking), shuning uchun `DefaultErrorHandler` + DLT va `maxAttempts` cheklovi kerak.

## 17.35 Xoreografiya (Choreography)

**Tavsif:** Taqsimlangan business jarayonni markaziy orkestrator boshqarmasdan, har bir servis o'z hodisalariga (event) reaksiya bildirib, keyingi hodisani chiqarishi orqali olib borish usuli. Servislar bir-birini bilmaydi — faqat event bus'dagi hodisalarga obuna bo'ladi, bu esa bo'sh bog'lanish (loose coupling) va mustaqil deploy imkonini beradi. Saga pattern'ining event-driven ko'rinishi odatda aynan xoreografiya asosida quriladi.

**Spring'da qayerda uchraydi:** Spring for Apache Kafka (`@KafkaListener`, `KafkaTemplate`), Spring AMQP (`@RabbitListener`), Spring Cloud Stream (`Function`/`Consumer` bean'lari funksional binding bilan). Ichki jarayonlarda `ApplicationEventPublisher` + `@EventListener`/`@TransactionalEventListener(phase = AFTER_COMMIT)`; ishonchli publikatsiya uchun transactional outbox (`@Transactional` + outbox jadvali + Debezium). Spring Modulith (`spring-modulith-events`) `@ApplicationModuleListener`, event publication registry va Kafka/AMQP externalization bilan xoreografiyani modul darajasida qo'llab-quvvatlaydi.

**Qo'llanish keyslari:**
- Buyurtma yaratildi → to'lov servisi reaksiya qiladi → ombor zahirani band qiladi → yetkazib berish rejalashtiriladi.
- Foydalanuvchi ro'yxatdan o'tdi → welcome email, analytics event va CRM yozuvi mustaqil yaratiladi.
- To'lov bekor qilindi → zahira bo'shatish va bonus qaytarish compensating hodisalari.
- Audit va analytics servislarini asosiy oqimga tegmasdan yangi consumer sifatida qo'shish.
- Spring Modulith bilan monolit ichida modullarni event orqali ajratish (keyinchalik mikroservisga chiqarish uchun).

**Ehtiyot bo'ling:** Xoreografiyada jarayonning "umumiy surati" hech qayerda yozilmaydi — oqim 5-6 servisdan oshsa, debug va kuzatish juda qiyinlashadi, shuning uchun distributed tracing (Micrometer Tracing + OpenTelemetry) va correlation ID majburiy. Murakkab shartli tarmoqlanish, timeout va compensation kerak bo'lsa, orkestratsiya (masalan, state machine yoki Temporal/Camunda) ko'pincha to'g'riroq tanlov; event'lar ham idempotent va versiyalangan bo'lishi shart.

## 17.36 Hedged so'rovlar (Hedged Requests)

**Tavsif:** Tail latency (p99) ni kamaytirish uchun bitta so'rovni bir nechta replikaga yuborib, eng birinchi kelgan javobni olish va qolganlarini bekor qilish patterni. Ko'pincha "tied/deferred hedging" shaklida qo'llaniladi: avval bitta so'rov yuboriladi, agar p95 vaqt ichida javob kelmasa, ikkinchi nusxa boshqa replikaga yuboriladi. Bu sekin node, GC pauzasi yoki vaqtincha tarmoq muammosini yashiradi, ammo yuklamani oshiradi.

**Spring'da qayerda uchraydi:** Spring Framework'da tayyor `@Hedged` annotatsiyasi YO'Q — reaktiv stack'da Reactor operatorlari bilan quriladi: `Mono.firstWithSignal(primary, secondary.delaySubscription(Duration.ofMillis(50)))` yoki `WebClient` chaqiruvlarida `timeout()` + `onErrorResume()`. Imperativ stack'da Java 21+ `StructuredTaskScope.ShutdownOnSuccess` bilan bir nechta `RestClient` chaqiruvini boshlab, birinchi muvaffaqiyatlisini olish. gRPC ishlatilsa, `grpc-java` o'zining hedging siyosatini service config orqali beradi (`spring-boot-starter-grpc`/grpc-spring-boot-starter bilan). Load balancer tomonida Spring Cloud LoadBalancer `ReactiveLoadBalancer` bilan turli instansiyalarni tanlash mumkin.

**Qo'llanish keyslari:**
- Ko'p replikali read-only katalog yoki search servisidan p99 latency'ni pasaytirish.
- Geo-taqsimlangan kesh klasterining ikki regionidan parallel o'qish.
- ML inference servisida bir nechta GPU node'ga bir vaqtda so'rov yuborish.
- DNS yoki konfiguratsiya kabi kichik, idempotent lookup chaqiruvlari.
- SLA qattiq bo'lgan real-time bidding yoki narx hisoblash oqimlari.

**Ehtiyot bo'ling:** Hedging faqat idempotent (odatda read) operatsiyalar uchun xavfsiz — yozish so'rovini ikkilantirish ikki marta to'lov yoki ikki marta buyurtmaga olib keladi. Yuklama yuqori bo'lganda hedging tizimni o'zi cho'ktiradi (retry storm'ga aylanadi), shuning uchun hedge ulushini cheklang (masalan, so'rovlarning 5%idan oshmasin) va bekor qilingan so'rovlarni haqiqatan cancel qiling.

## 17.37 Bosqichma-bosqich funksionallikni pasaytirish (Graceful Degradation)

**Tavsif:** Tizimning bir qismi ishdan chiqqanda butunlay to'xtamasdan, kam muhim funksiyalarni o'chirib yoki soddalashtirilgan javob berib asosiy business oqimni tirik qoldirish strategiyasi. Masalan, tavsiyalar servisi yiqilsa, mahsulot sahifasi statik "ommabop mahsulotlar" ro'yxatini ko'rsatadi; narx servisi javob bermasa, keshdagi oxirgi narx "taxminiy" yorlig'i bilan beriladi. Muhim nuqta: degradatsiya ongli ravishda loyihalanadi, tasodifiy xato sahifasi emas.

**Spring'da qayerda uchraydi:** Resilience4j fallback mexanizmlari: `@CircuitBreaker(name = "pricing", fallbackMethod = "cachedPrice")`, `@RateLimiter`, `@Bulkhead` (`resilience4j-spring-boot3`); Spring Cloud Circuit Breaker API'da `circuitBreakerFactory.create("id").run(supplier, throwable -> fallback())`. Spring Cache (`@Cacheable`, `@Cacheable(unless=...)`) stale-while-error uchun; `CacheErrorHandler` bilan kesh xatolarini yutish. Spring Cloud Gateway'da `CircuitBreaker` filter + `fallbackUri: forward:/fallback`. Feature toggle'lar `@ConfigurationProperties` + `@RefreshScope` bilan panic switch sifatida; `@ControllerAdvice`/`ProblemDetail` (RFC 9457) bilan foydalanuvchiga tushunarli partial javob.

**Qo'llanish keyslari:**
- Tavsiya yoki reyting servisi ishlamasa ham mahsulot sahifasini va "Sotib olish" tugmasini ishlashda qoldirish.
- Hisob-faktura PDF generatori band bo'lsa, foydalanuvchiga "keyinroq emailga yuboriladi" deb javob berish.
- Personalizatsiya yiqilsa, barcha foydalanuvchilarga umumiy bosh sahifa ko'rsatish.
- Loyalty bonus hisobi ishlamasa, to'lovni bonussiz o'tkazib, keyin compensating job bilan tuzatish.
- Qidiruv servisi sekinlashganda faqat kesh bo'yicha natija berib, filtrlarni vaqtincha o'chirish.

**Ehtiyot bo'ling:** Fallback'lar jim bo'lmasligi kerak — degradatsiya holati metrikaga (`Micrometer` counter) va alertga chiqmasa, tizim haftalar davomida "yarim ishlagan" holatda qolishi mumkin. Moliyaviy yoki huquqiy ahamiyatga ega qiymatlarni (balans, narx, tibbiy natija) eski keshdan "haqiqat" sifatida qaytarmang: bunday joyda to'g'ri xatolik berish noto'g'ri javobdan xavfsizroq.

## 17.38 Chaos engineering (Chaos Engineering)

**Tavsif:** Tizimning nosozliklarga bardoshligini taxmin qilish o'rniga, boshqarilgan tajribalar bilan nosozlik kiritib (latency, exception, pod o'ldirish, tarmoq uzish) amalda tekshirish amaliyoti. Har bir tajriba gipoteza bilan boshlanadi ("payment-service 2 sekund sekinlashsa, checkout p99 3 sekunddan oshmaydi"), kichik blast radius bilan o'tkaziladi va o'lchanadi. Maqsad — buzish emas, balki yashirin bog'liqliklarni va yetishmayotgan timeout/fallback'larni prod'gacha topish.

**Spring'da qayerda uchraydi:** Chaos Monkey for Spring Boot (`de.codecentric:chaos-monkey-spring-boot`) — `chaos-monkey` profili bilan `@Controller`, `@Service`, `@Repository` bean'lariga latency, exception, memory va `AppKiller` hujumlarini qo'yadi, `/actuator/chaosmonkey` endpoint'i orqali runtime'da boshqariladi. Infrastruktura darajasida Chaos Mesh yoki LitmusChaos Kubernetes'da pod/network chaos uchun; Testcontainers (`ToxiproxyContainer`) bilan integration testlarda tarmoq latency va uzilishini simulyatsiya qilish. Natijalarni kuzatish uchun Micrometer + Prometheus/Grafana va Micrometer Tracing.

**Qo'llanish keyslari:**
- Staging'da DB latency'ni 500 ms oshirib, connection pool to'lib ketishini va timeout'lar yetarliligini tekshirish.
- Kafka broker'ni o'chirib, consumer lag va DLT mexanizmining ishlashini tasdiqlash.
- Testcontainers + Toxiproxy bilan CI'da "downstream 3 s javob bermaydi" senariysini doimiy regress test qilish.
- Kubernetes'da tasodifiy pod o'chirib, readiness/liveness probe va graceful shutdown (`server.shutdown=graceful`) to'g'riligini sinash.
- GameDay mashqlarida on-call jamoasining runbook va alertlarini real sharoitda tekshirish.

**Ehtiyot bo'ling:** Chaos Monkey dependency'si prod artefaktiga tasodifan faol holda tushib qolmasin — uni faqat alohida profil va alohida muhit bilan yoqing, `/actuator/chaosmonkey` endpoint'ini esa himoyalang. Kuzatuvchanlik (metrics, tracing, alert), avtomatik rollback va aniq to'xtatish shartlari bo'lmasa chaos tajribasi o'tkazmang — aks holda bu tajriba emas, oddiy incident bo'ladi.

## 17.39 Resilience4j va Spring Cloud Circuit Breaker (Resilience4j & Spring Cloud Circuit Breaker)

**Tavsif:** Resilience4j — Java 17+ uchun funksional, yengil fault-tolerance kutubxonasi: Circuit Breaker, Retry, Rate Limiter, Bulkhead, TimeLimiter va Cache modullarini beradi (Netflix Hystrix o'rnini bosgan). Spring Cloud Circuit Breaker esa bu amalga oshirishlar ustida abstraksiya: kodingiz `CircuitBreakerFactory` API'siga bog'lanadi, implementatsiyani (Resilience4j, Spring Retry) esa starter almashtiradi. Dekoratorlarni zanjirlab, bir chaqiruvga bir vaqtda timeout, retry va circuit breaker qo'llash mumkin.

**Spring'da qayerda uchraydi:** `spring-cloud-starter-circuitbreaker-resilience4j` (imperativ) va `...-reactor-resilience4j` (reaktiv); yoki to'g'ridan-to'g'ri `io.github.resilience4j:resilience4j-spring-boot3`. Annotatsiyalar: `@CircuitBreaker`, `@Retry`, `@RateLimiter`, `@Bulkhead(type = THREADPOOL|SEMAPHORE)`, `@TimeLimiter` — har biri `fallbackMethod` bilan. Konfiguratsiya `resilience4j.circuitbreaker.instances.<name>.*` (`slidingWindowType`, `failureRateThreshold`, `waitDurationInOpenState`, `slowCallRateThreshold`). Actuator integratsiyasi: `/actuator/health` indicator, `/actuator/circuitbreakers`, `/actuator/circuitbreakerevents` va Micrometer metrikalari (`resilience4j_circuitbreaker_state`). Spring Cloud Gateway'da `CircuitBreaker` filter, Spring Cloud OpenFeign bilan ham integratsiya qilinadi.

```yaml
resilience4j.circuitbreaker.instances.pricing:
  slidingWindowType: COUNT_BASED
  slidingWindowSize: 50
  failureRateThreshold: 50
  slowCallDurationThreshold: 1s
  slowCallRateThreshold: 60
  waitDurationInOpenState: 10s
  permittedNumberOfCallsInHalfOpenState: 5
```

**Qo'llanish keyslari:**
- Tashqi to'lov provayderi yiqilganda chaqiruvlarni tez to'xtatib, keshlangan yoki navbatga qo'yilgan rejimga o'tish.
- Sekin downstream'ni `slowCallRateThreshold` bilan "nosoz" deb hisoblab, thread'larni bo'shatish.
- Bulkhead bilan har bir integratsiyaga alohida thread pool berib, bitta sekin servis butun ilovani bloklashini oldini olish.
- `@RateLimiter` orqali partner API'ning kontraktdagi limitidan oshmaslik.
- `@TimeLimiter` + `CompletableFuture` bilan majburiy timeout joriy etish.

**Ehtiyot bo'ling:** Annotatsiyalar Spring AOP proxy orqali ishlaydi — bir sinf ichidagi self-invocation (`this.method()`) chetlab o'tiladi, shuning uchun chaqiruv boshqa bean orqali kelishi kerak. Retry va circuit breaker tartibini e'tiborsiz qoldirmang (aspect order: `Retry` tashqarida, `CircuitBreaker` ichkarida bo'lsa retry'lar circuit'ni tez ochadi) va circuit breaker'ni biznes xatolari (`validation`, `404`) uchun ochilmasligi uchun `ignoreExceptions` sozlang.

## 17.40 Spring Framework 7 yadrosidagi resilience (Spring Framework 7 core resilience: @Retryable, @ConcurrencyLimit)

**Tavsif:** Spring Framework 7 resilience'ning eng asosiy ikki primitivini yadroga olib kirdi: deklarativ retry va deklarativ concurrency cheklovi. Endi oddiy retry yoki bulkhead uchun tashqi kutubxona (Spring Retry, Resilience4j) qo'shish shart emas — `spring-core`/`spring-context` ichidagi annotatsiyalar va `@EnableResilientMethods` kifoya. Bu "yengil" ehtiyojlarni qoplaydi; murakkab circuit breaker, rate limiter va metrikalar uchun baribir Resilience4j o'z o'rnida qoladi.

**Spring'da qayerda uchraydi:** `org.springframework.resilience.annotation.@Retryable` (atributlari: `maxAttempts`, `delay`, `multiplier`, `maxDelay`, `jitter`, `includes`, `excludes`, `predicate`) va `@ConcurrencyLimit(int)` — ikkisi ham `@EnableResilientMethods` bilan yoqiladi (Spring Boot 4.x bu infrastrukturani avtomatik sozlaydi). Ular ostida `RetryTemplate`/`RetryPolicy` (`org.springframework.core.retry`) va `ConcurrencyThrottleInterceptor` turadi; reaktiv qaytish turlari (`Mono`, `Flux`) ham qo'llab-quvvatlanadi. `@Retryable` metod darajasida ham, sinf darajasida ham qo'yiladi; eski `spring-retry` modulining `@Retryable`/`@Recover` annotatsiyalari bilan aralashtirib yubormaslik kerak — bular turli paketlarda.

```java
@Service
public class RatesClient {
    @Retryable(maxAttempts = 4, delay = 200, multiplier = 2.0, jitter = 100,
               includes = ResourceAccessException.class)
    @ConcurrencyLimit(10)
    public Rate fetch(String pair) {
        return restClient.get().uri("/rates/{p}", pair).retrieve().body(Rate.class);
    }
}
```

**Qo'llanish keyslari:**
- Vaqtincha tarmoq xatosida (`ResourceAccessException`) HTTP client chaqiruvini exponential backoff bilan qayta urinish.
- Optimistic locking konflikti (`OptimisticLockingFailureException`) bo'lganda transactionni qayta bajarish.
- Reyting yoki hisobot generatori kabi og'ir metodga `@ConcurrencyLimit(4)` qo'yib, CPU'ni himoya qilish.
- Virtual thread'lar bilan cheksiz parallelizm paydo bo'lganda downstream'ni bulkhead sifatida cheklash.
- Kichik servislarda qo'shimcha dependency kiritmasdan asosiy retry siyosatini joriy etish.

**Ehtiyot bo'ling:** `@Retryable` faqat idempotent operatsiyalarga qo'yilsin va `includes`/`excludes` aniq ko'rsatilsin — aks holda business validation xatolari ham qayta urinilib, yon effektlar takrorlanadi; `jitter` bo'lmasa retry'lar sinxronlashib retry storm hosil qiladi. `@ConcurrencyLimit` semafor asosida ishlaydi va kutib turgan thread'larni bloklaydi, shuning uchun uni timeout bilan birga ishlatmasa, cheklov o'zi navbat va latency manbasiga aylanadi.

## 17.41 Timeout budjeti / deadline propagatsiyasi (Timeouts Budget / Deadline Propagation)

**Tavsif:** Har bir chaqiruvga mustaqil timeout qo'yish o'rniga, butun so'rov uchun yagona "budjet" (masalan, 2000 ms) belgilanadi va u zanjir bo'ylab kamayib boradi: downstream chaqiruv faqat qolgan vaqt ichida bajarilishi mumkin. Deadline (absolyut vaqt nuqtasi) so'rov kontekstida downstream'ga uzatiladi, shunda hech bir servis mijoz allaqachon ketib qolgan ishni bajarib o'tirmaydi. Bu timeout'larning ichma-ich noto'g'ri sozlanishi (ichki timeout tashqisidan katta) muammosini hal qiladi va behuda resurs sarfini kamaytiradi.

**Spring'da qayerda uchraydi:** Spring'da avtomatik deadline propagatsiyasi YO'Q — qo'lda quriladi. Timeout'lar: `RestClient`/`RestTemplate` uchun `ClientHttpRequestFactorySettings` yoki `JdkClientHttpRequestFactory` (`HttpClient.newBuilder().connectTimeout(...)`, `HttpRequest.timeout(...)`), `WebClient`'da `Mono.timeout(...)` va `ReactorClientHttpConnector` bilan `HttpClient.responseTimeout(...)`; `@Transactional(timeout = 2)`, JPA `jakarta.persistence.query.timeout`, `TaskExecutionProperties`. Propagatsiya uchun `ClientHttpRequestInterceptor` yoki `ExchangeFilterFunction` bilan `X-Request-Deadline` header'ini yozish/o'qish, qiymatni `ThreadLocal`/`ScopedValue` (Java 21+) yoki Reactor `Context` orqali tashish; Micrometer `ObservationRegistry` context'i bilan ham bog'lash mumkin. gRPC ishlatilsa, `Deadline` protokol darajasida tayyor keladi.

**Qo'llanish keyslari:**
- API gateway'da 3 s SLA berib, downstream zanjirga faqat qolgan vaqtni uzatish.
- Gateway Aggregation'da parallel chaqiruvlarga umumiy budjetni bo'lib berish.
- Foydalanuvchi so'rovni bekor qilganda (`AsyncRequestTimeoutException`, client disconnect) downstream ishini to'xtatish.
- Batch job ichida har bir element uchun qoldiq vaqtni hisoblab, umumiy oynadan oshmaslik.
- DB query timeout'ini HTTP timeout'dan kichik qilib, connection pool'ni himoya qilish.

**Ehtiyot bo'ling:** Timeout'lar ichma-ich bo'lishi shart: downstream timeout + retry'lar soni upstream timeout'idan oshmasligi kerak, aks holda upstream baribir uzilib, downstream'da "yetim" ish qoladi. Deadline'ni mijoz yubora oladigan header sifatida ishonchsiz qabul qilmang (juda katta yoki manfiy qiymat) — serverda clamp qiling, va soat siljishini (clock skew) hisobga olib absolyut deadline o'rniga "qolgan ms" uzatish ko'pincha xavfsizroq.

## 17.42 Retry bo'roni (Retry Storm — anti-pattern)

**Tavsif:** Downstream servis sekinlashganda yoki xato qaytarganda barcha client'lar bir vaqtda, agressiv va koordinatsiyasiz qayta urinishi natijasida yuklamaning bir necha barobar oshishi va tizimning o'zini-o'zi cho'ktirishi. Ko'p qatlamli arxitekturada retry'lar ko'payadi: har qatlam 3 marta urinsa, uch qatlamda bitta so'rov 27 chaqiruvga aylanadi. Nosozlik tiklanishni ham to'xtatadi — servis ko'tarilishga urinsa, kutib turgan retry to'lqini uni yana yiqitadi (metastable failure).

**Spring'da qayerda uchraydi:** Oldini olish vositalari: Resilience4j `IntervalFunction.ofExponentialRandomBackoff(...)` (jitter bilan), `resilience4j.retry.instances.<name>.{maxAttempts, waitDuration, enableExponentialBackoff, enableRandomizedWait}`; Spring Framework 7 `@Retryable(multiplier, jitter, maxDelay)`; Spring Retry `ExponentialRandomBackOffPolicy`. Circuit breaker retry'larni kesib tashlaydi (`@CircuitBreaker` + `ignoreExceptions`), `@Bulkhead` bir vaqtdagi chaqiruvlarni cheklaydi, Gateway'da `RequestRateLimiter` va `Retry` filter'ining `retries`/`statuses` sozlamalari. Kafka'da `DefaultErrorHandler` + `ExponentialBackOffWithMaxRetries` va `@RetryableTopic` (non-blocking retry + DLT). Monitoring: Micrometer `resilience4j_retry_calls` va `http.client.requests` metrikalari, `Retry-After` header'iga hurmat.

**Qo'llanish keyslari:**
- Faqat idempotent operatsiyalarga retry qo'yib, `POST /payments` kabi chaqiruvlarni idempotency key bilan himoyalash.
- Har bir qatlamda retry qilmaslik: retry'ni faqat bitta (odatda eng tashqi yoki eng ichki) qatlamga belgilash.
- Jitter'li exponential backoff bilan client'lar sinxronlashib "to'lqin" yaratishini buzish.
- 429/503 va `Retry-After` javoblarida backoff'ni server aytgan vaqtga moslash.
- Retry budjetini joriy etish: umumiy so'rovlarning masalan 10%idan ko'pi retry bo'lmasin (adaptive retry).

**Ehtiyot bo'ling:** Default retry sozlamalarini "xavfsiz" deb o'ylamang — jitter'siz fixed delay va ko'p qatlamli retry eng ko'p uchraydigan prod incident sababidir; retry'ni har doim circuit breaker, concurrency limit va timeout budjeti bilan birga joylashtiring. Kafka'da bloklanuvchi retry (`DefaultErrorHandler` uzoq backoff bilan) butun partitionni to'xtatadi va rebalance'ga olib keladi — bunday holda `@RetryableTopic` asosidagi non-blocking retry'ni tanlang.

---

[&larr; 16. Enterprise Integration Patterns II: transformatsiya, endpointlar, boshqaruv, event patternlar](16-enterprise-integration-patterns-ii.md) · [Mundarija](README.md) · [18. Xavfsizlik patternlari &rarr;](18-xavfsizlik-patternlari.md)
