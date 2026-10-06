<!-- doc: architect | chapter: 17 | part: III. Spring chuqur bilim -->

[Barcha hujjatlar](../../README.md) / [Arxitektor miyasi](README.md)

> Holat: AI yozgan, inson tekshirmagan.

# 17. Spring MVC va WebFlux: so'rov yo'li, thread modeli, REST dizayni (Spring MVC and WebFlux)

<details>
<summary>Bu bobdagi 12 bo'lim</summary>

- [17.1 So'rovning to'liq yo'li: konteyner, filter, `DispatcherServlet`, handler, converter](#171-sorovning-toliq-yoli-konteyner-filter-dispatcherservlet-handler-converter)
- [17.2 Thread modeli: har so'rovga bitta thread va uning chegarasi](#172-thread-modeli-har-sorovga-bitta-thread-va-uning-chegarasi)
- [17.3 Tomcat sozlamalari: `max-threads`, `accept-count`, `connection-timeout` va ularning ma'nosi](#173-tomcat-sozlamalari-max-threads-accept-count-connection-timeout-va-ularning-manosi)
- [17.4 WebFlux va event loop modeli: qachon haqiqatan foyda beradi](#174-webflux-va-event-loop-modeli-qachon-haqiqatan-foyda-beradi)
- [17.5 Virtual thread bilan MVC: WebFlux ga ehtiyoj qanday kamayadi](#175-virtual-thread-bilan-mvc-webflux-ga-ehtiyoj-qanday-kamayadi)
- [17.6 REST dizayni: resurs nomlari, HTTP metodlari, holat kodlari, versiyalash](#176-rest-dizayni-resurs-nomlari-http-metodlari-holat-kodlari-versiyalash)
- [17.7 So'rov va javob modellari: DTO chegarasi va entity ni tashqariga chiqarmaslik](#177-sorov-va-javob-modellari-dto-chegarasi-va-entity-ni-tashqariga-chiqarmaslik)
- [17.8 Validatsiya va xato javobi formati (`ProblemDetail`, RFC 9457)](#178-validatsiya-va-xato-javobi-formati-problemdetail-rfc-9457)
- [17.9 Katta javoblar: sahifalash, oqim (streaming), siqish](#179-katta-javoblar-sahifalash-oqim-streaming-siqish)
- [17.10 `RestClient` va `WebClient`: timeout, connection pool, qayta urinish sozlamalari](#1710-restclient-va-webclient-timeout-connection-pool-qayta-urinish-sozlamalari)
- [17.11 Filter va interceptor: qayerda kontekst (trace id, foydalanuvchi) o'rnatiladi](#1711-filter-va-interceptor-qayerda-kontekst-trace-id-foydalanuvchi-ornatiladi)
- [17.12 Amalda qo'llash](#1712-amalda-qollash)

</details>



Web qatlami arxitektor uchun eng ko'p noto'g'ri tushunilgan joy, chunki u tashqaridan oddiy ko'rinadi: annotatsiya qo'yasan, JSON chiqadi. Haqiqatda bitta HTTP so'rov konteyner socket'idan boshlab, thread pool, filter zanjiri, `DispatcherServlet`, argument resolver, message converter va javob buferi orqali o'tadi. Shu yo'lning har bir bo'g'inida o'z limiti, o'z timeout'i va o'z xotira narxi bor. Quyida mexanikani, aniq sozlash raqamlarini va eng ko'p uchraydigan tuzoqlarni ko'rib chiqamiz.

## 17.1 So'rovning to'liq yo'li: konteyner, filter, `DispatcherServlet`, handler, converter

Tomcat'da `NioEndpoint` acceptor thread socket ulanishini qabul qiladi va uni poller'ga beradi. Poller ulanishda o'qishga tayyor ma'lumot paydo bo'lganda ishni worker thread pool'ga uzatadi. Shu nuqtadan boshlab so'rov bitta worker thread'ni egallab oladi. Keyin `FilterChain` ishga tushadi: Spring Boot'da bu odatda `CharacterEncodingFilter`, `FormContentFilter`, Micrometer'ning observation filtri, Spring Security filter zanjiri va sizning filtrlaringiz.

`DispatcherServlet` ichida tartib qat'iy: `HandlerMapping` URL va metodga qarab handler topadi (`RequestMappingHandlerMapping`), `HandlerAdapter` uni chaqiradi, argument resolver'lar `@RequestBody`, `@PathVariable`, `@RequestParam` qiymatlarini tayyorlaydi, qaytgan obyektni `HttpMessageConverter` serializatsiya qiladi. Xato chiqsa `HandlerExceptionResolver` zanjiri ishlaydi.

Muhim mexanika: `@RequestBody` uchun Jackson butun JSON'ni o'qiydi va obyekt daraxtini xotirada quradi. 5 MB JSON yuborilgan so'rov deserializatsiya paytida taxminan 15-40 MB heap talab qiladi, chunki string'lar, map'lar va boxing qo'shimcha xarajat beradi. Shuning uchun `spring.servlet.multipart.max-request-size` va body limitini ataylab qo'yish kerak, aks holda bitta mijoz 50 ta parallel so'rov bilan heap'ni to'ldiradi.

Javob tomonida ham tuzoq bor. Converter natijani to'g'ridan-to'g'ri response output stream'ga yozadi, lekin buferlash Tomcat darajasida (`server.tomcat.max-http-response-header-size` emas, balki socket buferi) sodir bo'ladi. Agar serializatsiya o'rtasida exception chiqsa, status kodi allaqachon 200 bo'lib ketgan bo'ladi va mijoz yarim JSON oladi. Bu `@Transactional` ichida lazy collection'ni serializatsiya qilishga urinishning klassik natijasi.

## 17.2 Thread modeli: har so'rovga bitta thread va uning chegarasi

Platform thread bilan servlet modeli oddiy: so'rov boshida thread beriladi, javob yozilgandan keyin qaytariladi. Blocking chaqiruv (JDBC, HTTP client, fayl) davomida thread kutadi va boshqa hech kimga xizmat qilmaydi. Shu sababli parallellik chegarasi thread pool kattaligiga teng.

Little qonuni bu yerda to'g'ridan-to'g'ri ishlaydi: kerakli thread soni taxminan RPS ni o'rtacha javob vaqtiga ko'paytirishga teng. To'lov servisi sekundda 300 so'rov qabul qilsa va o'rtacha 120 ms ishlasa, 300 × 0.12 = 36 thread yetadi. Lekin p99 latency 800 ms bo'lsa, burst paytida 240 thread kerak bo'lib qoladi. Arxitektor o'rtacha emas, tail latency bo'yicha hisoblaydi.

Ikkinchi chegara xotira. Har bir platform thread stack'i uchun default 1 MB virtual manzil ajratiladi (`-Xss`), amalda 80-200 KB tegiladi. 200 thread uchun bu taxminan 20-40 MB, bu muammo emas. Haqiqiy muammo thread'ga bog'langan obyektlar: har bir so'rovning DTO'lari, Hibernate persistence context, JDBC statement buferlari. 200 parallel so'rovda har biri 2 MB ishlatsa, 400 MB heap faqat ishlab turgan so'rovlar uchun ketadi.

Uchinchi chegara va eng xavflisi: thread pool'ning to'lib qolishi. Downstream servis sekinlashsa, barcha 200 thread shu chaqiruvda kutib turadi, keyin health endpoint ham javob bermaydi va orkestrator pod'ni o'chiradi. Shuning uchun har bir tashqi chaqiruvda timeout majburiy va bulkhead (alohida limit) kerak.

## 17.3 Tomcat sozlamalari: `max-threads`, `accept-count`, `connection-timeout` va ularning ma'nosi

Bu to'rt parametr aslida bitta navbat tizimini tasvirlaydi: OS accept queue, Tomcat ulanish limiti, worker pool, va keep-alive siyosati.

```yaml
server:
  tomcat:
    threads:
      max: 200            # bir vaqtda ishlaydigan worker thread chegarasi
      min-spare: 20       # bo'sh turadigan minimum, burst'da yaratish kechikmasligi uchun
    max-connections: 8192 # ochiq socket chegarasi, worker'dan ancha katta
    accept-count: 100     # OS backlog: ulanish kutadigan navbat uzunligi
    connection-timeout: 5s        # birinchi so'rov baytini kutish muddati
    keep-alive-timeout: 20s       # keyingi so'rovni kutish muddati
    max-keep-alive-requests: 100  # bitta ulanishdagi so'rov soni
  # so'rovni butunlay tashlab yuborish uchun emas, diagnostika uchun
  tomcat.mbeanregistry.enabled: true
```

`max-connections` (default 8192) va `threads.max` (default 200) orasidagi farq ataylab qo'yilgan: keep-alive ulanish ochiq turadi, lekin thread egallamaydi. 8192 ochiq ulanish va 200 worker bo'lsa, tizim 8000 ta bekor turgan ulanishni arzon ushlab turadi. `accept-count` (default 100) esa `max-connections` ham to'lganda OS backlog'ida kutadigan navbat. U to'lsa yangi ulanish darhol rad etiladi va mijoz "connection refused" oladi.

`connection-timeout` default qiymati 20 s va bu juda uzun. Mijoz TCP ulanishni ochib, so'rov yozmasa, 20 s davomida slot egallanadi. Ommaviy API uchun 5 s yetarli. `accept-count` ni kattalashtirish vasvasasiga tushmaslik kerak: uzun navbat latency'ni oshiradi, lekin throughput'ni oshirmaydi. To'lgan navbat o'rniga tez rad etish (fail fast) mijozga retry qilish imkonini beradi, uzoq kutish esa timeout'dan keyin ishni behuda qiladi.

`threads.max` ni 800 ga ko'tarish ham odatda xato. Agar bottleneck DB connection pool bo'lsa (masalan HikariCP 20 ta ulanish), 800 thread shunchaki 780 tasini pool navbatida kutishga majbur qiladi. Natijada latency oshadi, context switch ko'payadi va xato diagnostikasi qiyinlashadi. Qoida: worker thread soni DB pool'dan 4-10 barobar katta bo'lsin, undan ortiq emas.

## 17.4 WebFlux va event loop modeli: qachon haqiqatan foyda beradi

WebFlux Netty ustida ishlaydi va event loop thread soni CPU yadrosi soniga teng (default `max(4, yadro soni)`). Har bir so'rov thread egallamaydi, balki callback zanjiri sifatida ro'yxatga olinadi. Shuning uchun 20 000 ochiq ulanishni 8 thread bilan ushlab turish mumkin.

Foyda aniq uchta holatda keladi. Birinchisi: ko'p sonli uzoq yashaydigan ulanish (SSE, WebSocket, long polling). Ikkinchisi: servis asosan boshqa servislarga proxy bo'lsa va o'zi hisob-kitob qilmasa (API gateway, aggregator). Uchinchisi: oqim sifatida kelayotgan katta ma'lumotni backpressure bilan uzatish kerak bo'lsa.

Foyda kelmaydigan holat ham aniq: oddiy CRUD servis, JDBC bilan ishlaydi, sekundda 200 so'rov oladi. Bu yerda WebFlux faqat zarar keltiradi, chunki blocking JDBC chaqiruvi event loop thread'ini bloklaydi va butun servis to'xtaydi. `Mono.fromCallable(...).subscribeOn(Schedulers.boundedElastic())` bilan o'rab chiqish mumkin, lekin natija oddiy thread pool'ning qimmat va murakkab taqlidi bo'ladi.

Reactive stack'ning yashirin narxi: stack trace o'qilmas holga keladi, `ThreadLocal` ishlamaydi (kontekst `Context` orqali uzatiladi), debugger'da qadamlab yurish imkonsiz, va har bir yangi dasturchi uchun o'rganish vaqti haftalar bilan hisoblanadi. Arxitektor bu narxni faqat o'lchangan ehtiyoj bo'lganda to'laydi.

## 17.5 Virtual thread bilan MVC: WebFlux ga ehtiyoj qanday kamayadi

Java 21 dan boshlab virtual thread barqaror. Spring Boot'da bitta sozlama bilan yoqiladi va Tomcat worker'lari virtual thread executor'ga o'tadi.

```properties
# Java 21+ va Boot 3.2+ talab qiladi
spring.threads.virtual.enabled=true

# virtual thread yoqilganda bu limit ma'nosini yo'qotadi,
# shuning uchun chegarani boshqa joyda qo'yish kerak
server.tomcat.threads.max=200
# haqiqiy chegara endi shu: DB pool va downstream bulkhead
spring.datasource.hikari.maximum-pool-size=25
spring.datasource.hikari.connection-timeout=3000
```

Mexanika: virtual thread blocking I/O'da park bo'ladi va carrier (platform) thread'ni bo'shatadi. Shu sababli 10 000 parallel so'rovni 8 carrier thread bilan bajarish mumkin, kod esa oddiy blocking uslubda qoladi. Ya'ni WebFlux bergan scalability'ning katta qismi reactive kodsiz olinadi.

Lekin ikki muhim nuqta bor. Birinchisi: virtual thread I/O'ni arzonlashtiradi, CPU ishini emas. Hisobot generatsiyasi CPU'ga bog'liq bo'lsa, foyda nolga teng. Ikkinchisi: chegara yo'qoladi. Ilgari 200 thread tabiiy bulkhead bo'lgan, endi 10 000 virtual thread bir vaqtda DB pool'ga yopiriladi va `connection-timeout` xatolari yog'iladi. Shuning uchun virtual thread yoqilganda semaphore yoki rate limiter bilan aniq limit qo'yish majburiy bo'ladi.

Pinning masalasi: `synchronized` blok ichida blocking I/O bo'lsa, JDK 21-23 da virtual thread carrier'ga qotib qoladi. JDK 24 dan bu muammo asosan hal qilindi, lekin eski kutubxonalarda `ReentrantLock` ga o'tish hali ham to'g'ri qadam. `ThreadLocal` ishlaydi, lekin har bir virtual thread o'z nusxasini oladi, shuning uchun thread-local cache (masalan `SimpleDateFormat` pool) endi foydasiz va faqat xotira yeydi.

## 17.6 REST dizayni: resurs nomlari, HTTP metodlari, holat kodlari, versiyalash

Resurs nomi ko'plikda va ot bo'lsin: `/api/orders`, `/api/orders/{id}/payments`. Fe'l URL'da emas, HTTP metodida. Istisno: haqiqiy harakatlar uchun subresurs maqbul, masalan `POST /api/orders/{id}/cancellation`.

Status kodlarida eng ko'p xato qilinadigan joylar: 400 va 422 farqi (400 noto'g'ri formatlangan so'rov, 422 format to'g'ri lekin semantik xato), 404 va 403 farqi (resurs yo'qligini yashirish kerak bo'lsa 404), 409 (konflikt, masalan optimistic lock) va 412 (`If-Match` bajarilmadi). `POST` muvaffaqiyatli bo'lsa 201 va `Location` header qaytarilsin.

Idempotency muhim mexanika. `PUT` va `DELETE` tabiiy idempotent, `POST` emas. To'lov yaratishda mijoz `Idempotency-Key` header yuborsin, server esa shu kalitni unique index bilan saqlab, takroriy so'rovga avvalgi javobni qaytarsin. Bu retry va timeout bo'lganda ikki marta pul olishdan saqlaydi.

Versiyalash uchun amalda ishlaydigani URL prefiksi (`/api/v1/`, `/api/v2/`). Header orqali versiyalash nazariy toza, lekin cache, log va debug'da og'riq keltiradi. Qoida: yangi maydon qo'shish buzmaydigan o'zgarish, maydonni o'chirish yoki tipini o'zgartirish buzadi. Buzmaydigan o'zgarishlar uchun yangi versiya chiqarmang. Ikki versiyani bir vaqtda ushlash muddatini oldindan e'lon qiling, masalan 6 oy.

## 17.7 So'rov va javob modellari: DTO chegarasi va entity ni tashqariga chiqarmaslik

Entity'ni controller'dan qaytarish eng keng tarqalgan arxitektura xatosi. Sabablari mexanik: lazy proxy serializatsiya paytida `LazyInitializationException` beradi yoki yashirin SELECT yog'diradi, DB sxemasi o'zgarishi API contract'ini buzadi, va `password_hash` kabi maydon tasodifan tashqariga chiqadi.

```java
// Javob DTO: record yetarli, o'zgarmas va Jackson bilan ishlaydi
public record OrderResponse(
        Long id,
        String status,
        BigDecimal total,           // pul uchun hech qachon double ishlatilmaydi
        OffsetDateTime createdAt,
        List<OrderLineResponse> lines) {

    static OrderResponse from(Order order) {
        // lines allaqachon fetch qilingan bo'lishi shart,
        // shu yerda lazy yuklash bo'lsa N+1 kelib chiqadi
        return new OrderResponse(
                order.getId(),
                order.getStatus().name(),
                order.getTotal(),
                order.getCreatedAt(),
                order.getLines().stream().map(OrderLineResponse::from).toList());
    }
}
```

Mapping qayerda bo'lishi kerak? Service qatlamining chegarasida, tranzaksiya hali ochiq bo'lganda. Agar mapping controller'da bo'lsa, `@Transactional` yopilgandan keyin lazy maydonlarga tegish xatoga olib keladi. Ko'p maydonli DTO uchun MapStruct qulay, chunki u compile vaqtida kod generatsiya qiladi va reflection ishlatmaydi. Reflection'ga asoslangan mapper'lar har bir chaqiruvda taxminan 1-5 mikrosekund qo'shadi, bu 1000 obyektli javobda sezilarli bo'ladi.

Alohida so'rov DTO'si ham kerak. `OrderCreateRequest` ichida `id` va `createdAt` bo'lmasin, aks holda mijoz server boshqaradigan maydonni yuborishga harakat qiladi. Projection (interface yoki record based) read tomonida DTO'ni DB darajasida to'g'ridan-to'g'ri qurish imkonini beradi va keraksiz ustunlarni o'qishni oldini oladi.

## 17.8 Validatsiya va xato javobi formati (`ProblemDetail`, RFC 9457)

Spring Framework 6 dan `ProblemDetail` mavjud va RFC 9457 formatini beradi ([RFC 9457](https://www.rfc-editor.org/rfc/rfc9457), 2023 da 7807 ni almashtirgan; maydonlar va media type o'zgarmagan, Spring 6.0 javadoci hali eski raqamni aytadi): `type`, `title`, `status`, `detail`, `instance`, plus qo'shimcha maydonlar. `Content-Type` esa `application/problem+json` bo'ladi.

```java
@RestControllerAdvice
class ApiExceptionHandler extends ResponseEntityExceptionHandler {

    // Bean Validation xatolarini maydon bo'yicha ro'yxatga aylantiramiz
    @Override
    protected ResponseEntity<Object> handleMethodArgumentNotValid(
            MethodArgumentNotValidException ex, HttpHeaders headers,
            HttpStatusCode status, WebRequest request) {

        ProblemDetail body = ProblemDetail.forStatus(HttpStatus.UNPROCESSABLE_ENTITY);
        body.setTitle("Validatsiya xatosi");
        body.setType(URI.create("https://api.example.com/problems/validation"));
        body.setProperty("errors", ex.getBindingResult().getFieldErrors().stream()
                .map(fe -> Map.of("field", fe.getField(), "message", fe.getDefaultMessage()))
                .toList());
        body.setProperty("traceId", MDC.get("traceId"));   // qo'llab-quvvatlash uchun
        return ResponseEntity.unprocessableEntity().body(body);
    }

    @ExceptionHandler(InsufficientBalanceException.class)
    ProblemDetail handleBalance(InsufficientBalanceException ex) {
        ProblemDetail pd = ProblemDetail.forStatusAndDetail(
                HttpStatus.CONFLICT, "Hisobdagi mablag' yetarli emas");
        pd.setProperty("accountId", ex.getAccountId());
        return pd;
    }
}
```

Mexanik detallar: `@Valid` `@RequestBody` ustida `MethodArgumentNotValidException` beradi, `@Validated` service metodida esa `ConstraintViolationException`. Ikkinchisi default holda 500 ga aylanadi, shuning uchun uni alohida ushlash kerak. `spring.mvc.problemdetails.enabled=true` qo'yilsa Spring o'zi standart xatolarni `ProblemDetail` ko'rinishida qaytaradi.

Muhim xavfsizlik qoidasi: `detail` ichiga exception message'ni to'g'ridan-to'g'ri yozmang. SQL xatosi, fayl yo'li yoki ichki sinf nomi tashqariga chiqadi. Mijozga barqaror `type` URI va inson o'qiydigan xabar bersin, texnik detal log'da `traceId` bilan qolsin.

## 17.9 Katta javoblar: sahifalash, oqim (streaming), siqish

Birinchi qoida: chegarasiz ro'yxat endpoint'i bo'lmasin. `GET /api/orders` default 20 element qaytarsin va `size` parametri uchun maksimum (masalan 200) qattiq qo'yilsin. `spring.data.web.pageable.max-page-size` shuni ta'minlaydi.

Offset pagination chuqur sahifalarda sekinlashadi, chunki PostgreSQL tashlab yuboriladigan qatorlarni ham o'qishga majbur. Keyset (cursor) pagination bu muammoni yo'q qiladi.

```sql
-- Yomon: 100 000 qatorni o'qib tashlaydi, taxminan 200-800 ms
SELECT id, created_at, total FROM orders
WHERE customer_id = $1
ORDER BY created_at DESC, id DESC
LIMIT 20 OFFSET 100000;

-- Yaxshi: index bo'yicha to'g'ridan-to'g'ri sakraydi, taxminan 1-3 ms
SELECT id, created_at, total FROM orders
WHERE customer_id = $1
  AND (created_at, id) < ($2, $3)   -- oxirgi ko'rilgan qator kursori
ORDER BY created_at DESC, id DESC
LIMIT 20;

-- Shu so'rov uchun kerak bo'ladigan index
CREATE INDEX idx_orders_cust_created ON orders (customer_id, created_at DESC, id DESC);
```

Hisobot eksporti uchun esa sahifalash ham to'g'ri emas. 2 million qatorli CSV'ni ro'yxatga yig'ib qaytarish OOM beradi. Yechim: `StreamingResponseBody` bilan qatorni o'qib darhol yozish, DB tomonida `fetchSize` qo'yish.

```java
@GetMapping(value = "/api/reports/orders.csv", produces = "text/csv")
ResponseEntity<StreamingResponseBody> export(@RequestParam LocalDate from) {
    StreamingResponseBody body = out -> {
        var writer = new BufferedWriter(new OutputStreamWriter(out, StandardCharsets.UTF_8));
        writer.write("id,created_at,total\n");
        // Stream tranzaksiya ichida ochiladi, fetchSize kursor bilan ishlashni majbur qiladi
        try (Stream<OrderRow> rows = reportService.streamOrders(from)) {
            rows.forEach(r -> writeRow(writer, r));
        }
        writer.flush();   // flush bo'lmasa oxirgi bufer yo'qoladi
    };
    return ResponseEntity.ok()
            .header("Content-Disposition", "attachment; filename=orders.csv")
            .body(body);
}
```

Siqish arzon va samarali: JSON odatda 5-10 barobar kichrayadi. Lekin kichik javoblar uchun siqish CPU'ni behuda yeydi, shuning uchun minimal hajm chegarasi bor.

```yaml
server:
  compression:
    enabled: true
    min-response-size: 2KB     # bundan kichik javob siqilmaydi
    mime-types: application/json,application/problem+json,text/csv,text/plain
  # streaming javobda async timeout ni oshirish kerak bo'ladi
spring:
  mvc:
    async:
      request-timeout: 300s
  jackson:
    default-property-inclusion: non_null   # null maydonlar javobni shishiradi
```

Streaming javobda ikki tuzoq bor. Birinchisi: javob boshlangandan keyin status kodini o'zgartirish imkonsiz, shuning uchun barcha validatsiya oqim boshlanishidan oldin bajarilsin. Ikkinchisi: tranzaksiya oqim butun davomida ochiq turadi va bu PostgreSQL'da uzun transaction, ya'ni vacuum kechikishi. Katta eksport uchun `readOnly` tranzaksiya va 5 daqiqadan oshmaydigan muddat maqbul.

## 17.10 `RestClient` va `WebClient`: timeout, connection pool, qayta urinish sozlamalari

`RestClient` (Spring Framework 6.1+) blocking, `RestTemplate` o'rnini oladi va virtual thread bilan mukammal ishlaydi. `WebClient` reactive, lekin MVC ilovasida ham ishlatiladi. Tanlov qoidasi: blocking stack'da `RestClient`, reactive stack'da `WebClient`.

Eng xavfli default: timeout yo'q. JDK'ning `HttpClient` da connect timeout o'rnatilmasa OS darajasiga tushadi, read timeout esa cheksiz bo'ladi. Bitta sekin downstream butun thread pool'ni yeyishi uchun shu yetarli.

```java
@Bean
RestClient paymentClient(RestClient.Builder builder) {
    // Boot 4.0 da bu tur HttpClientSettings deb nomlanadi
    var settings = HttpClientSettings.defaults()
            .withConnectTimeout(Duration.ofSeconds(2))   // TCP + TLS uchun
            .withReadTimeout(Duration.ofSeconds(3));     // javob baytlarini kutish
    return builder
            .baseUrl("https://payments.internal")
            .requestFactory(ClientHttpRequestFactoryBuilder.jdk().build(settings))
            .defaultHeader("Accept", "application/json")
            .requestInterceptor((request, body, execution) -> {
                // trace id ni downstream'ga uzatamiz
                request.getHeaders().add("X-Trace-Id", MDC.get("traceId"));
                return execution.execute(request, body);
            })
            .build();
}
```

`WebClient` uchun reactor-netty connection pool muhim. Default `max-connections` taxminan `max(16, 2 × yadro soni)` ga teng, `pendingAcquireTimeout` esa 45 s. Bu 45 s juda uzun: so'rov pool navbatida yarim daqiqa kutib, keyin baribir xato beradi.

```java
@Bean
WebClient inventoryClient() {
    ConnectionProvider provider = ConnectionProvider.builder("inventory")
            .maxConnections(50)
            .pendingAcquireTimeout(Duration.ofSeconds(2))  // navbatda uzoq kutmaslik
            .pendingAcquireMaxCount(100)
            .maxIdleTime(Duration.ofSeconds(20))   // LB idle timeout'dan kichik bo'lsin
            .maxLifeTime(Duration.ofMinutes(5))    // DNS o'zgarishini ushlash uchun
            .evictInBackground(Duration.ofSeconds(30))
            .build();

    HttpClient httpClient = HttpClient.create(provider)
            .option(ChannelOption.CONNECT_TIMEOUT_MILLIS, 2000)
            .responseTimeout(Duration.ofSeconds(3));

    return WebClient.builder()
            .clientConnector(new ReactorClientHttpConnector(httpClient))
            .build();
}
```

Timeout budjeti hisoblanadi, taxmin qilinmaydi. Tashqi so'rovga 5 s ajratilgan bo'lsa va ichida ketma-ket ikki chaqiruv bor bo'lsa, har biriga 3 s berib bo'lmaydi. Retry ham budjetga kiradi: 3 s read timeout va 2 marta retry 9 s degani. Shuning uchun retry faqat idempotent chaqiruvda, exponential backoff va jitter bilan, umumiy deadline nazoratida qilinadi. `maxIdleTime` ni load balancer idle timeout'idan kichik qo'yish majburiy, aks holda yopilgan ulanishga yozishga urinib tasodifiy `connection reset` xatolari olinadi.

## 17.11 Filter va interceptor: qayerda kontekst (trace id, foydalanuvchi) o'rnatiladi

Farq mexanik: filter servlet darajasida ishlaydi va barcha so'rovlarni (static resurs, xato sahifasi, hatto handler topilmasa ham) ko'radi. `HandlerInterceptor` esa `DispatcherServlet` ichida, handler aniqlangandan keyin ishlaydi va `HandlerMethod` ga kirish imkoni bor.

Shuning uchun taqsimlash shunday: trace id, correlation id, request log, response header filter'da; handler haqida bilim talab qiladigan ish (ruxsat tekshirish annotatsiya bo'yicha, metrika endpoint nomi bilan) interceptor'da.

```java
@Component
@Order(Ordered.HIGHEST_PRECEDENCE + 10)   // Security filtridan oldin turishi mumkin
class TraceIdFilter extends OncePerRequestFilter {

    @Override
    protected void doFilterInternal(HttpServletRequest req, HttpServletResponse res,
                                    FilterChain chain) throws IOException, ServletException {
        String traceId = Optional.ofNullable(req.getHeader("X-Trace-Id"))
                .filter(s -> s.length() <= 64)      // tashqi qiymatni validatsiya qilamiz
                .orElseGet(() -> UUID.randomUUID().toString());
        MDC.put("traceId", traceId);
        res.setHeader("X-Trace-Id", traceId);
        try {
            chain.doFilter(req, res);
        } finally {
            MDC.clear();   // thread pool'da qaytariladi, tozalamasa kontekst oqib ketadi
        }
    }
}
```

`MDC.clear()` ni `finally` da yozmaslik eng ko'p uchraydigan xato. Platform thread pool'da thread qaytariladi va keyingi so'rov eski `traceId` bilan log yozadi. Virtual thread'da bu muammo kamayadi, chunki thread bir martalik, lekin `finally` baribir to'g'ri odat.

Ikkinchi tuzoq: `@Async` yoki `ExecutorService` ga o'tganda `MDC` va `SecurityContext` ko'chmaydi, chunki ular `ThreadLocal`. Spring'da `DelegatingSecurityContextExecutor` va `TaskDecorator` bu masalani hal qiladi. Micrometer ishlatilayotgan bo'lsa, `ObservationRegistry` kontekstni avtomatik uzatadi va qo'lda `MDC` boshqarish ehtiyoji kamayadi.

Uchinchi tuzoq: filter'da `request.getInputStream()` ni o'qish. Stream bir marta o'qiladi, keyin `@RequestBody` bo'sh qoladi. Body'ni log qilish kerak bo'lsa `ContentCachingRequestWrapper` ishlatiladi, lekin u butun body'ni xotirada saqlaydi, shuning uchun limit qo'yish shart.

| Mavzu | Oddiy yondashuv | Arxitektor yondashuvi |
|---|---|---|
| Thread pool o'lchami | `threads.max` ni 500 ga ko'tarish | Little qonuni bilan p99 bo'yicha hisoblash, DB pool'ga nisbatda 4-10x |
| Tashqi chaqiruv | default timeout bilan `RestTemplate` | connect 2 s, read 3 s, bulkhead va umumiy deadline budjeti |
| Javob modeli | entity'ni to'g'ridan-to'g'ri qaytarish | DTO/record, mapping tranzaksiya ichida, projection bilan ustun tanlash |
| Xato javobi | `Map.of("error", ex.getMessage())` | `ProblemDetail` + barqaror `type` URI + `traceId`, ichki detal log'da |
| Ro'yxat endpoint | chegarasiz `findAll()` | default 20, max 200, chuqur sahifa uchun keyset kursor |
| Katta eksport | `List` ga yig'ib JSON qaytarish | `StreamingResponseBody`, `fetchSize` bilan kursor, async timeout |
| Scalability muammosi | darhol WebFlux ga ko'chish | avval virtual thread va blocking kod, WebFlux faqat o'lchangan ehtiyojda |
| Versiyalash | har o'zgarishda `/v2` | buzmaydigan o'zgarishda versiya o'zgarmaydi, eskisi uchun muddat e'lon qilinadi |
| `POST` takrori | mijozga ishonish | `Idempotency-Key` va unique index bilan natijani saqlash |
| Trace id | controller'da log'ga yozish | filter'da `MDC`, javob header'ida va downstream header'ida uzatish |

| Tuzoq | Nima bo'ladi | Yechim |
|---|---|---|
| `MDC` tozalanmaydi | keyingi so'rov eski `traceId` bilan log yozadi | `finally` da `MDC.clear()`, yoki `TaskDecorator` |
| Serializatsiya paytida lazy fetch | yarim JSON va 200 status bilan xato | mapping'ni tranzaksiya ichida bajarish, fetch join |
| `accept-count` juda katta | latency oshadi, throughput oshmaydi | navbatni qisqa tutib tez rad etish, mijozga retry qoldirish |
| `maxIdleTime` > LB idle timeout | tasodifiy `connection reset` | pool idle vaqtini LB dan kichik qo'yish, `maxLifeTime` 5 min |
| Virtual thread + `synchronized` I/O | carrier thread pinning, throughput tushadi | `ReentrantLock` ga o'tish, JDK 24+ ga ko'tarilish |
| Filter'da body o'qish | `@RequestBody` bo'sh keladi | `ContentCachingRequestWrapper` va hajm limiti |
| Reactive'da blocking JDBC | event loop bloklanadi, butun servis to'xtaydi | blocking kodni MVC'da qoldirish yoki alohida scheduler |
| Retry budjetsiz | downstream'ga yuk ko'payadi, cascade failure | idempotent chaqiruvda, backoff + jitter, umumiy deadline |

## 17.12 Amalda qo'llash

- [ ] Har bir tashqi HTTP client uchun `connect` va `read` timeout qiymatini aniq yozib chiqing, default qolgan joy bo'lmasin.
- [ ] `threads.max` ni Little qonuni bo'yicha p99 latency asosida qayta hisoblang va DB pool o'lchami bilan nisbatini tekshiring.
- [ ] `server.tomcat.connection-timeout` ni 20 s dan 5 s ga tushirib, yuk testida rad etilgan ulanish sonini kuzatib ko'ring.
- [ ] Barcha ro'yxat endpoint'lariga default va maksimal `size` qo'ying, chuqur sahifa uchun bitta endpoint'ni keyset kursorga o'tkazing.
- [ ] Xato javoblarini `ProblemDetail` ga ko'chiring, `type` URI katalogini hujjatlashtiring va `traceId` maydonini qo'shing.
- [ ] Controller qaytaradigan tiplarni audit qiling: entity qaytaradigan joy qolmasin, test sifatida JSON sxemasini qotirib qo'yish yetarli.
- [ ] Java 21+ da `spring.threads.virtual.enabled=true` ni staging'da yoqib, DB pool timeout va bulkhead limitlarini qayta o'lchang.
- [ ] `MDC` va `SecurityContext` async chaqiruvlarda ko'chayotganini bitta integratsiya testi bilan qotirib qo'ying.

---

[&larr; 16. Spring Boot mexanikasi: auto-configuration, starter, Actuator](16-spring-boot-mexanikasi-auto-configuration.md) · [Mundarija](README.md) · [18. Spring Data JPA va Hibernate chuqur &rarr;](18-spring-data-jpa-va-hibernate-chuqur.md)
