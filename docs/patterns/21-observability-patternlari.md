<!-- doc: patterns | chapter: 21 | part:  -->

[Barcha hujjatlar](../../README.md) / [Dizayn patternlar](README.md)

# 21. Observability patternlari (Observability Patterns)

<details>
<summary>Bu bo'limdagi 26 bo'lim</summary>

- [21.1 Loglarni markazlashtirish (Log Aggregation)](#211-loglarni-markazlashtirish-log-aggregation)
- [21.2 Strukturalangan loglash (Structured Logging)](#212-strukturalangan-loglash-structured-logging)
- [21.3 Korrelyatsiya ID / Trace ID tarqatish (Correlation ID / Trace ID Propagation)](#213-korrelyatsiya-id--trace-id-tarqatish-correlation-id--trace-id-propagation)
- [21.4 Taqsimlangan trassirovka (Distributed Tracing)](#214-taqsimlangan-trassirovka-distributed-tracing)
- [21.5 Baggage - kontekstni olib yurish (Baggage)](#215-baggage---kontekstni-olib-yurish-baggage)
- [21.6 Ilova metrikalari (Application Metrics)](#216-ilova-metrikalari-application-metrics)
- [21.7 RED / USE / To'rtta oltin signal (RED / USE / Four Golden Signals)](#217-red--use--tortta-oltin-signal-red--use--four-golden-signals)
- [21.8 SLI / SLO / Xato budjeti (SLI / SLO / Error Budget)](#218-sli--slo--xato-budjeti-sli--slo--error-budget)
- [21.9 Salomatlik tekshiruvi API (Health Check API)](#219-salomatlik-tekshiruvi-api-health-check-api)
- [21.10 Audit loglash (Audit Logging)](#2110-audit-loglash-audit-logging)
- [21.11 Xatolarni kuzatish (Exception Tracking)](#2111-xatolarni-kuzatish-exception-tracking)
- [21.12 Deploy va o'zgarishlarni qayd etish (Log Deployments and Changes)](#2112-deploy-va-ozgarishlarni-qayd-etish-log-deployments-and-changes)
- [21.13 Dashboardlar (Dashboards)](#2113-dashboardlar-dashboards)
- [21.14 Ogohlantirish (Alerting)](#2114-ogohlantirish-alerting)
- [21.15 Namuna olish (Sampling (head, tail))](#2115-namuna-olish-sampling-head-tail)
- [21.16 Micrometer Observation API (Micrometer Observation API)](#2116-micrometer-observation-api-micrometer-observation-api)
- [21.17 Kontekstni tarqatish (Context propagation (MDC, ThreadLocal, Reactor))](#2117-kontekstni-tarqatish-context-propagation-mdc-threadlocal-reactor)
- [21.18 Sintetik monitoring (Synthetic Monitoring)](#2118-sintetik-monitoring-synthetic-monitoring)
- [21.19 Log darajasini ish vaqtida o'zgartirish (Runtime log level change (Actuator loggers))](#2119-log-darajasini-ish-vaqtida-ozgartirish-runtime-log-level-change-actuator-loggers)
- [21.20 Metrika teglari kardinalligini nazorat qilish (Metrics tag cardinality control)](#2120-metrika-teglari-kardinalligini-nazorat-qilish-metrics-tag-cardinality-control)
- [21.21 Heartbeat / Watchdog (Heartbeat / Watchdog)](#2121-heartbeat--watchdog-heartbeat--watchdog)
- [21.22 Uzluksiz profiling (Continuous Profiling (JFR))](#2122-uzluksiz-profiling-continuous-profiling-jfr)
- [21.23 Biznes metrikalari / KPI (Business metrics / KPIs)](#2123-biznes-metrikalari--kpi-business-metrics--kpis)
- [21.24 OpenTelemetry Collector (OpenTelemetry Collector (agent, sidecar))](#2124-opentelemetry-collector-opentelemetry-collector-agent-sidecar)
- [21.25 Exemplar'lar (Exemplars (logs-metrics-traces correlation))](#2125-exemplarlar-exemplars-logs-metrics-traces-correlation)
- [21.26 Amalda qo'llash](#2126-amalda-qollash)

</details>



Observability (kuzatuvchanlik) patternlari - tizimning ichki holatini tashqariga chiqayotgan signallar (loglar, metrikalar, trace'lar) orqali tiklab tushunish imkonini beruvchi yechimlar to'plami. Mikroservislar, async messaging va elastik bulut muhitida bitta foydalanuvchi so'rovi o'nlab process va thread orqali o'tadi, shuning uchun "aslida nima sindi va qayerda sekinlashdi?" degan savolga javob faqat oldindan loyihalangan telemetriya bilan beriladi. Arxitektor uchun bu patternlar "keyin qo'shamiz" turidagi qo'shimcha emas: signal modeli, metrika kardinalligi, trace sampling, retention va telemetriya cost'i arxitektura qarori sifatida tizim dizayni bilan birga qabul qilinadi. Spring ekotizimida bu sohaning deyarli barchasi Micrometer, Micrometer Tracing/OpenTelemetry va Spring Boot Actuator abstraksiyalari orqali standartlashtirilgan, shu sababli asosiy ish - to'g'ri patternni tanlash va uni izchil qo'llash.

## 21.1 Loglarni markazlashtirish (Log Aggregation)

**Tavsif:** Har bir instance o'z diskiga yozadigan loglar taqsimlangan tizimda foydasiz bo'lib qoladi: pod o'chadi, fayl yo'qoladi, bitta so'rov esa bir nechta servisda iz qoldiradi. Log Aggregation patterni barcha servis va instance loglarini bitta markaziy tizimga (indeks + qidiruv + saqlash) yuboradi, shu orqali bir joydan qidirish, filtrlash va alert qo'yish mumkin bo'ladi. Odatda ilova loglarni faqat `stdout`ga yozadi, infrastruktura darajasidagi collector (sidecar yoki node agent) ularni yig'ib backend'ga uzatadi. Natijada log hayot aylanishi ilovadan ajratiladi va ilova kodi transport detallarini bilmaydi.

**Spring'da qayerda uchraydi:** Spring Boot default'da Logback (`spring-boot-starter-logging`, SLF4J API) bilan keladi; `logging.file.name`/`logging.file.path`, `logging.level.*`, `logging.logback.rollingpolicy.*` propertylari va `logback-spring.xml` orqali appender'lar sozlanadi (`<springProfile>` tag'i bilan muhitga qarab). Log4j2'ga o'tish uchun `spring-boot-starter-log4j2` ishlatiladi. Markazlashtirish uchun amalda keng tarqalgan yo'llar: konteyner `stdout` + Fluent Bit/Fluentd/Grafana Alloy/Promtail agentlari, yoki to'g'ridan-to'g'ri `net.logstash.logback.appender.LogstashTcpSocketAppender` (logstash-logback-encoder kutubxonasi), Loki uchun `com.github.loki4j:loki-logback-appender`. Spring Cloud muhitida bu patternning "o'qish" tomoni Kibana/Grafana/OpenSearch Dashboards orqali bajariladi.

**Qo'llanish keyslari:**
- 40 ta pod orasidan bitta `orderId` bo'yicha barcha log yozuvlarini bir soniyada topish.
- Incident paytida servislar bo'ylab xronologik timeline tuzish (log scaling, pod restartlari bilan birga).
- `ERROR` darajali loglar oqimi ustiga alert qo'yish (masalan 5 daqiqada 50 dan oshsa).
- PCI/ISO audit talabi uchun loglarni o'zgartirilmaydigan (WORM) saqlashga uzatish.
- Kubernetes'da `kubectl logs` bilan yetib bo'lmaydigan o'chgan pod loglarini tekshirish.

**Ehtiyot bo'ling:** Log hajmi va indeks narxi tez o'sadi - `DEBUG`ni productionda yoqib qo'yish yoki har bir HTTP so'rov body'sini loglash hisobni va latency'ni portlatadi; sensitiv ma'lumot (token, PAN, parol, shaxsiy ma'lumot) markaziy logga tushsa, uni o'chirish juda qiyin bo'ladi, shuning uchun maskirovka loglash nuqtasida bo'lishi kerak. Logni asosiy metrika manbasiga aylantirmang: "count by log line" yondashuvi metrikadan qimmat va sekin.

## 21.2 Strukturalangan loglash (Structured Logging)

**Tavsif:** Erkin matnli log qatorini regex bilan ajratish mo'rt va qimmat; strukturalangan loglashda har bir yozuv kalit-qiymat juftliklaridan iborat JSON (yoki boshqa machine-readable format) sifatida chiqadi. Bu log aggregation backend'iga parsing'siz indekslash, aniq field bo'yicha filtrlash (`user_id`, `tenant`, `http.status`) va aggregatsiya qilish imkonini beradi. Timestamp, log level, logger nomi, trace kontekst va biznes atributlari alohida fieldlar bo'ladi, shuning uchun so'rovlar deterministik ishlaydi. Amalda bu pattern korrelyatsiya va dashboard patternlarining poydevori hisoblanadi.

**Spring'da qayerda uchraydi:** Spring Boot 3.4'dan boshlab structured logging platformaning o'zida bor: `logging.structured.format.console` va `logging.structured.format.file` propertylari `ecs` (Elastic Common Schema), `logstash` va `gelf` formatlarini beradi, qo'shimcha sozlashlar `logging.structured.ecs.service.name`, `logging.structured.gelf.host` va `logging.structured.json.add`/`rename`/`exclude` orqali qilinadi (Boot 3.x/4.x). Maxsus format uchun `org.springframework.boot.logging.structured.StructuredLogFormatter` interfeysi implement qilinadi va `logging.structured.format.console` ga to'liq sinf nomi beriladi. Boot 3.4'dan oldingi loyihalarda yoki ko'proq nazorat kerak bo'lsa `net.logstash.logback.encoder.LogstashEncoder`/`LoggingEventCompositeJsonEncoder` ishlatiladi. Kontekst fieldlari SLF4J `MDC` yoki SLF4J 2.x fluent API (`log.atInfo().addKeyValue("orderId", id).log("order placed")`) bilan qo'shiladi.

**Qo'llanish keyslari:**
- Kibana/Grafana'da `tenant_id` va `http.response.status_code` bo'yicha aniq filtrlangan log paneli qurish.
- Bitta `traceId` bo'yicha barcha servis loglarini avtomatik birlashtirish.
- Loglardan xatoliklar taqsimotini `error.type` field bo'yicha hisoblash.
- SIEM tizimiga ECS sxemasida tayyor hodisalar yuborish (parser yozmasdan).
- Lokal development'da odam o'qiydigan format, productionda JSON - bitta profil o'zgarishi bilan.

**Ehtiyot bo'ling:** JSON log odam uchun o'qishga noqulay, shuning uchun `local`/`dev` profilda plain pattern qoldirish deyarli har doim to'g'ri; MDC'ga ko'p va dinamik field solish log hajmini va indeks kardinalligini keskin oshiradi. Multiline exception stack trace'lar JSON ichida bitta field bo'lib ketishiga e'tibor bering - aks holda collector har qatorni alohida event sifatida parchalab yuboradi.

## 21.3 Korrelyatsiya ID / Trace ID tarqatish (Correlation ID / Trace ID Propagation)

**Tavsif:** Taqsimlangan tizimda bitta mantiqiy so'rovga tegishli barcha loglarni bog'lash uchun unikal identifikator kerak: u chetki nuqtada (edge/API gateway) yaratiladi yoki tashqi so'rovdan qabul qilinadi va keyingi barcha chaqiruvlarga (HTTP header, message property) uzatiladi. Har bir servis bu ID'ni log kontekstiga qo'yadi, shuning uchun bir so'rov bo'ylab yakka qidiruv ishlaydi. Zamonaviy stack'da bu rol `traceId`/`spanId` ga o'tgan, lekin biznes-darajadagi alohida `correlationId` (masalan client request ID) ham ko'p saqlanadi. Asosiy qiyinchilik - kontekstni thread'lar, thread pool'lar va reactive oqimlar orasida yo'qotmaslik.

**Spring'da qayerda uchraydi:** Micrometer Tracing (`micrometer-tracing-bridge-brave` yoki `micrometer-tracing-bridge-otel`) ulanganda Spring Boot 3.x `traceId`/`spanId`ni avtomatik MDC'ga joylaydi va default log pattern'ga `logging.pattern.correlation` (`[${spring.application.name:},%X{traceId:-},%X{spanId:-}]`) qo'shadi. Qo'lda boshqarish uchun `org.slf4j.MDC`, `OncePerRequestFilter`, `HandlerInterceptor`, `RestClient`/`WebClient`/`RestTemplate` interceptorlari va Kafka/Rabbit uchun `RecordInterceptor`/`MessagePostProcessor` ishlatiladi. Kontekst ko'chirish uchun `TaskDecorator` (`ThreadPoolTaskExecutor#setTaskDecorator`), `DelegatingSecurityContextExecutor` uslubidagi wrapper'lar, reactive tomonda `Micrometer`'ning `ContextSnapshot`/`ContextRegistry` (context-propagation kutubxonasi) va `Hooks.enableAutomaticContextPropagation()` qo'llanadi.

```java
public class CorrelationIdFilter extends OncePerRequestFilter {
  @Override
  protected void doFilterInternal(HttpServletRequest req, HttpServletResponse res,
      FilterChain chain) throws ServletException, IOException {
    String cid = Optional.ofNullable(req.getHeader("X-Correlation-Id"))
        .filter(StringUtils::hasText).orElseGet(() -> UUID.randomUUID().toString());
    MDC.put("correlationId", cid);
    res.setHeader("X-Correlation-Id", cid);
    try { chain.doFilter(req, res); } finally { MDC.remove("correlationId"); }
  }
}
```

**Qo'llanish keyslari:**
- Support jamoasi foydalanuvchi bergan request ID bo'yicha incidentni bir so'rovda topishi.
- Gateway → order-service → payment-service zanjiridagi xatoni oxirigacha kuzatish.
- Kafka consumer loglarini uni chaqirgan HTTP so'rov bilan bog'lash.
- `@Async` va `CompletableFuture` ichidagi loglarni ham asosiy so'rovga biriktirish.
- Xato javobida `traceId`ni qaytarib, mijoz murojaatini tezroq tekshirish.

**Ehtiyot bo'ling:** MDC `ThreadLocal`da yashaydi - thread pool, `@Async`, reactive yoki virtual thread bilan ishlaganda `finally`da tozalamaslik begona so'rovning ID'si boshqa log'ga "yopishib qolishi"ga olib keladi. Tashqi mijozdan kelgan ID'ni ko'r-ko'rona ishonib log/metrika tag sifatida ishlatmang: uzunligini va formatini validatsiya qiling, aks holda bu log injection va kardinallik portlashi yo'liga aylanadi.

## 21.4 Taqsimlangan trassirovka (Distributed Tracing)

**Tavsif:** Distributed Tracing bitta so'rovni servislar bo'ylab daraxt shaklidagi span'lar ketma-ketligi sifatida yozib oladi: har bir span nomi, davomiyligi, atributlari va ota-span havolasiga ega. Bu latency'ning qayerda yo'qolganini (DB chaqiruvi, tashqi API, serialization) aniq ko'rsatadi va servis bog'liqliklari xaritasini avtomatik chizadi. Kontekst W3C Trace Context standartidagi `traceparent`/`tracestate` headerlari bilan uzatiladi, shuning uchun turli til va vendorlardagi servislar bir-birini tushunadi. Hajmni boshqarish uchun sampling (head-based yoki tail-based) qo'llanadi.

**Spring'da qayerda uchraydi:** Spring Boot 3.x'da Micrometer Observation API markaziy abstraksiya: `ObservationRegistry`, `Observation`, `@Observed` (ishlashi uchun `ObservedAspect` bean kerak) va avtomatik instrumentatsiya (`ServerHttpObservationFilter`, `RestClient`/`WebClient`/`RestTemplate`, `JdbcTemplate`, Spring Kafka, Spring AMQP, Spring Data). Tracing backend `micrometer-tracing-bridge-brave` (Brave + `zipkin-reporter-brave`) yoki `micrometer-tracing-bridge-otel` (OpenTelemetry SDK + `opentelemetry-exporter-otlp`/`opentelemetry-exporter-zipkin`) bilan ulanadi; sozlamalar `management.tracing.sampling.probability`, `management.tracing.propagation.type` (`W3C`, `B3`), `management.otlp.tracing.endpoint`, `management.zipkin.tracing.endpoint`. Kodsiz variant - OpenTelemetry Java agent (`-javaagent:opentelemetry-javaagent.jar`) yoki `opentelemetry-spring-boot-starter`; Spring Cloud Sleuth esa deprecated va Micrometer Tracing'ga ko'chgan.

**Qo'llanish keyslari:**
- p99 latency qaysi downstream chaqiruvdan kelib chiqqanini aniqlash.
- N+1 so'rov muammosini trace ichidagi yuzlab bir xil DB span'i orqali fosh qilish.
- Servislar orasidagi real bog'liqlik grafigini (service map) olish va "kim kimni chaqiryapti" savoliga javob berish.
- Retry va timeout zanjirining kaskadini (bitta foydalanuvchi so'roviga 9 ta urinish) ko'rish.
- Async Kafka pipeline'ida producer va consumer'ni bitta trace'da bog'lash.

**Ehtiyot bo'ling:** 100% sampling yuqori trafikda storage va CPU jihatidan qimmat, 0.01% esa kerakli xatoni ushlamaydi - odatda past head sampling + xatoga asoslangan tail sampling (OTel Collector'da) birlashtiriladi; span atributlariga katta body yoki PII solish xavfli va qimmat. Bitta ilovada bir vaqtda OTel Java agent va Micrometer Tracing bridge'ini yoqib qo'yish ikki xil instrumentatsiya va ikki marta hisoblangan span'larga olib keladi.

## 21.5 Baggage - kontekstni olib yurish (Baggage)

**Tavsif:** Baggage - trace kontekstiga ilashtirilgan kalit-qiymat juftliklari to'plami bo'lib, servislar chegarasidan o'tib keyingi barcha downstream chaqiruvlarga avtomatik uzatiladi. Bu `tenantId`, `region`, `feature-flag`, `syntheticTest=true` kabi "butun so'rov bo'ylab kerak bo'ladigan" ma'lumotni har bir metodga parametr qilib tashlamasdan tarqatish imkonini beradi. W3C Baggage standarti `baggage` header'ini belgilaydi va u `traceparent` bilan birga ketadi. Qiymatlarni kerak joyda log fieldi yoki span atributi sifatida chiqarish mumkin.

**Spring'da qayerda uchraydi:** Micrometer Tracing'da `io.micrometer.tracing.BaggageManager`/`Tracer#createBaggageInScope(...)` va `BaggageInScope` API'si mavjud; konfiguratsiya `management.tracing.baggage.enabled`, `management.tracing.baggage.remote-fields` (tashqariga uzatiladigan fieldlar) va `management.tracing.baggage.correlation.fields` (MDC'ga avtomatik ko'chiriladigan fieldlar) propertylari bilan qilinadi. Brave bridge ostida bu `BaggagePropagation`/`BaggageField` ustidagi, OTel bridge ostida esa `io.opentelemetry.api.baggage.Baggage` va `W3CBaggagePropagator` ustidagi qoplama bo'lib ishlaydi. Reactive va async kodda baggage `ContextSnapshot`/context-propagation orqali ko'chiriladi.

**Qo'llanish keyslari:**
- Multi-tenant SaaS'da `tenantId`ni butun chaqiruv zanjiri bo'ylab olib yurib, loglar va metrikalarda ishlatish.
- Yuk testi trafigini `syntheticTest` flag bilan belgilab, downstream'da real biznes hisobotidan ajratish.
- Canary release'da `release=canary` belgisini zanjir bo'ylab uzatib, xatolarni versiyaga bog'lash.
- Qaysi kanal (mobile/web/partner API) orqali kelgan so'rov sekin ishlayotganini kuzatish.
- Debug uchun `verboseLogging=true` ni faqat bitta so'rov zanjirida yoqish.

**Ehtiyot bo'ling:** Baggage har bir tashqi chaqiruvda header sifatida ketadi - ko'p yoki katta field tarmoq overhead'i va header limitlariga urilish demak, shuning uchun bir nechta qisqa kalit bilan cheklaning. Baggage'ni hech qachon ishonch (authorization) qarorlari uchun manba qilib olmang va unga PII/sensitiv qiymat solmang: u tashqi tizimlarga ham oqib ketishi mumkin, chegarada esa tozalash (sanitize) qoidasi bo'lishi shart.

## 21.6 Ilova metrikalari (Application Metrics)

**Tavsif:** Metrikalar - vaqt bo'yicha agregatlangan sonli o'lchovlar (counter, gauge, timer, distribution) bo'lib, arzon saqlanadi va alert hamda trend tahlili uchun eng mos signal turi. Loglardan farqli ravishda ular oldindan agregatlanadi, shuning uchun yuqori trafikda ham cost oldindan bashorat qilinadi. Ilova o'z biznes va texnik o'lchovlarini e'lon qiladi, time-series baza (Prometheus) esa ularni scrape qilib saqlaydi. Yaxshi metrika modeli nomlanish konvensiyasi va tag (label) dizayni bilan boshlanadi.

**Spring'da qayerda uchraydi:** Micrometer - Spring Boot'ning metrika fasadi: `MeterRegistry`, `Counter`, `Timer`, `Gauge`, `DistributionSummary`, `LongTaskTimer`, deklarativ `@Timed`/`@Counted` (ularga `TimedAspect`/`CountedAspect` bean kerak) va `@Observed` orqali metrika+trace birgalikda chiqadi. Actuator avtomatik ravishda `http.server.requests`, `jvm.memory.used`, `hikaricp.connections`, `system.cpu.usage`, `logback.events`, `jdbc.connections.*`, `spring.data.repository.invocations` kabi meter'larni beradi; `/actuator/metrics` va `micrometer-registry-prometheus` bilan `/actuator/prometheus` endpointi ochiladi. Moslashtirish uchun `MeterRegistryCustomizer<MeterRegistry>` (umumiy taglar), `MeterFilter` (deny/rename/limit kardinallik), `MeterBinder` (maxsus binder) va `management.metrics.distribution.percentiles-histogram.*` propertylari ishlatiladi.

**Qo'llanish keyslari:**
- HTTP endpointlar bo'yicha RPS, xato ulushi va latency histogramini kuzatish.
- HikariCP pool to'lib qolishini (`hikaricp.connections.pending`) alert bilan ushlash.
- Biznes metrikasi: muvaffaqiyatsiz to'lovlar soni, savat tashlab ketish darajasi, kutilayotgan buyurtmalar navbati.
- Kubernetes HPA yoki KEDA uchun custom metrika (masalan Kafka consumer lag) berish.
- JVM GC pauza va heap trendini release'lar kesimida solishtirish.

**Ehtiyot bo'ling:** Eng ko'p uchraydigan xato - tag kardinalligini portlatish: `userId`, `orderId`, raw URI yoki exception message'ni tag qilib qo'yish Prometheus'ni ham, byudjetni ham o'ldiradi (`MeterFilter.maximumAllowableTags` va `/{id}` uslubidagi URI template bilan cheklang). Metrikadan aniq bitta hodisani tiklashni kutmang - u agregat signal; sababni topish uchun trace va log kerak bo'ladi.

## 21.7 RED / USE / To'rtta oltin signal (RED / USE / Four Golden Signals)

**Tavsif:** Bu uchta framework "nimani o'lchash kerak?" savoliga tayyor javob beradi va metrika chalg'ituvchi ko'pligidan qutqaradi. RED (Rate, Errors, Duration) - so'rovga asoslangan servislar uchun; USE (Utilization, Saturation, Errors) - resurslar (CPU, disk, pool, thread) uchun; Google SRE'ning to'rtta oltin signali (latency, traffic, errors, saturation) ikkisini birlashtiradi. Amalda har bir servis uchun RED va har bir muhim resurs uchun USE panellari standart shablon sifatida tuziladi. Bu dashboard va alert dizaynini bir xillashtiradi va yangi servisni kuzatuvga olish vaqtini qisqartiradi.

**Spring'da qayerda uchraydi:** RED to'g'ridan-to'g'ri Actuator'ning `http.server.requests` (Prometheus'da `http_server_requests_seconds_count`/`_sum`/`_bucket`) timeridan olinadi - `uri`, `method`, `status`, `outcome`, `exception` taglari bilan; kiruvchi so'rovlar `ServerHttpObservationFilter`, chiquvchilar `http.client.requests` orqali. Latency kvantillari uchun `management.metrics.distribution.percentiles-histogram.http.server.requests=true` yoqiladi (Prometheus `histogram_quantile` uchun). USE tomoni JVM va pool binderlaridan keladi: `jvm.threads.live`, `executor.queued`/`executor.active` (`ThreadPoolTaskExecutor` uchun `ExecutorServiceMetrics`), `hikaricp.connections.usage`/`.pending`, `system.cpu.usage`, `process.files.open`. Xato signali uchun `logback.events{level="error"}` va `outcome="SERVER_ERROR"` filtrlari qo'shiladi.

**Qo'llanish keyslari:**
- Har bir mikroservis uchun bir xil "RED" dashboard shablonini joriy qilish.
- Thread pool navbati o'sishini (saturation) CPU to'lmasidan oldin ushlash.
- Alertlarni infrastruktura emas, foydalanuvchi ko'radigan signal (xato ulushi, latency) ustiga qurish.
- Yuk testida bottleneck resursni USE jadvali orqali bir qarashda aniqlash.
- Release'dan keyin `outcome="SERVER_ERROR"` ulushini oldingi versiya bilan solishtirish.

**Ehtiyot bo'ling:** O'rtacha (mean) latency'ga tayanish eng tipik xato - foydalanuvchi og'rig'i p95/p99 va histogram'da ko'rinadi, shuning uchun timer'larda histogram yoqilgan bo'lishi kerak. Faqat resurs utilizatsiyasiga (CPU 80%) alert qo'yish yolg'on signal keltiradi: utilizatsiya yuqori bo'lsa ham servis sog'lom bo'lishi mumkin, muhimi - saturation va xato ulushi.

## 21.8 SLI / SLO / Xato budjeti (SLI / SLO / Error Budget)

**Tavsif:** SLI - foydalanuvchi tajribasini ifodalovchi aniq o'lchov (masalan 300 ms ichida muvaffaqiyatli javob bergan so'rovlar ulushi), SLO - shu SLI uchun belgilangan maqsad (masalan 30 kunda 99.9%), Error Budget esa SLO ruxsat beradigan "buzilish zaxirasi" (99.9% uchun ~43 daqiqa/oy). Bu pattern "hamma narsa yashil bo'lsin" degan imkonsiz talabni o'rniga muhandislik qarori uchun sonli mezon qo'yadi: budjet qolgan bo'lsa tez relizlar, tugagan bo'lsa barqarorlikka o'tish. Alertlar statik threshold o'rniga budjet sarflanish tezligiga (burn rate) bog'lanadi, bu shovqinni keskin kamaytiradi. Natijada SRE va biznes bir xil tilda gaplashadi.

**Spring'da qayerda uchraydi:** SLI'lar Actuator/Micrometer metrikalaridan hisoblanadi - `http.server.requests` histogrami bilan `management.metrics.distribution.slo.http.server.requests=100ms,300ms,500ms` va `management.metrics.distribution.percentiles-histogram.*` propertylari kerakli bucket'larni beradi (Micrometer'da bu `ServiceLevelObjectiveBoundary` sifatida ifodalanadi). Haqiqiy SLO/burn-rate hisob-kitobi ilovada emas, Prometheus recording/alerting rule'lari, Grafana SLO yoki Sloth/Pyrra kabi generatorlarda yuritiladi; Micrometer `MeterFilter` bilan faqat SLO uchun kerak bo'lgan endpointlarga histogram yoqib, cost'ni cheklash odatiy amaliyot. Availability SLI uchun `outcome`/`status` taglari, dependency SLI uchun esa `http.client.requests` va Resilience4j metrikalari ishlatiladi.

**Qo'llanish keyslari:**
- "Checkout API 99.9% so'rovni 500 ms ichida bajaradi" SLO'sini metrikadan avtomatik hisoblash.
- Multi-window multi-burn-rate alert qo'yib, tungi soatlarda bejiz chaqiriqlarni kamaytirish.
- Error budget tugaganda feature relizlarni to'xtatib, reliability ishlariga o'tish qoidasini joriy qilish.
- Mijoz bilan tuzilgan SLA'ni ichki SLO (qattiqroq) bilan himoyalash.
- Platforma jamoasining kvartal maqsadlarini budjet sarfi bo'yicha baholash.

**Ehtiyot bo'ling:** SLI'ni foydalanuvchi sezmaydigan ichki ko'rsatkichdan (CPU, queue size) qurish SLO'ni ma'nosiz qiladi - o'lchov so'rov natijasi yoki journey muvaffaqiyati bo'lishi kerak; shuningdek `/actuator/health`, bot va synthetic trafikni SLI hisobidan chiqarib tashlash zarur. SLO'ni 100% yoki haddan tashqari qattiq belgilash error budget'ni ishlamas holga keltiradi va jamoani signalga ishonchini yo'qotadi.

## 21.9 Salomatlik tekshiruvi API (Health Check API)

**Tavsif:** Health Check API - orkestrator, load balancer va deploy pipeline uchun ilova holatini mashina o'qiydigan shaklda qaytaruvchi endpoint. Muhim ajrim: liveness ("process tirikmi, restart kerakmi?") va readiness ("trafik qabul qilishga tayyormi?") bir-biridan mustaqil bo'lishi kerak, aks holda vaqtinchalik downstream nosozligi butun klasterni restart qilishga olib keladi. Tekshiruv natijasi odatda holat + tarkibiy qismlar detallari (DB, cache, broker) ko'rinishida bo'ladi. Startup probe esa sekin ko'tariladigan ilovalarni erta o'ldirishdan saqlaydi.

**Spring'da qayerda uchraydi:** `spring-boot-starter-actuator` `/actuator/health` endpointini beradi; `HealthIndicator`/`ReactiveHealthIndicator`, `AbstractHealthIndicator`, `HealthContributor` va `CompositeHealthContributor` interfeyslari bilan o'z tekshiruvi qo'shiladi, built-in indikatorlar esa `DataSourceHealthIndicator`, `RedisHealthIndicator`, `MongoHealthIndicator`, `DiskSpaceHealthIndicator` kabilar. Liveness/readiness uchun `management.endpoint.health.probes.enabled=true` (Kubernetes'da avtomatik) `/actuator/health/liveness` va `/actuator/health/readiness` yo'llarini ochadi, ular ortida `LivenessStateHealthIndicator`/`ReadinessStateHealthIndicator`, `ApplicationAvailability` va `AvailabilityChangeEvent` turadi; guruhlar `management.endpoint.health.group.readiness.include/exclude` bilan sozlanadi. Graceful shutdown uchun `server.shutdown=graceful` va `spring.lifecycle.timeout-per-shutdown-phase` readiness bilan birga ishlatiladi.

```java
@Component("cacheWarmup")
class CacheWarmupHealth implements HealthIndicator {
  private final AtomicBoolean ready = new AtomicBoolean(false);

  @EventListener(ApplicationReadyEvent.class)
  void warmUp() { /* cache'ni to'ldirish */ ready.set(true); }

  @Override
  public Health health() {
    return ready.get() ? Health.up().build()
        : Health.outOfService().withDetail("stage", "warming").build();
  }
}
```

**Qo'llanish keyslari:**
- Kubernetes liveness/readiness/startup probe'larini to'g'ri ajratib sozlash.
- Deploy paytida pod cache yoki migration tugamaguncha trafik olmasligini ta'minlash.
- Load balancer'dan nosog'lom instance'ni avtomatik chiqarib tashlash.
- Graceful shutdown'da readiness'ni `DOWN` qilib, in-flight so'rovlarni yo'qotmaslik.
- Tashqi bog'liqlik (payment provider) uzilganda degraded holatni alohida guruhda ko'rsatish.

**Ehtiyot bo'ling:** Downstream bog'liqliklarni liveness probe'ga qo'shish eng xavfli antipattern - DB bir daqiqa javob bermasa Kubernetes barcha podlarni restart qilib, nosozlikni kaskadga aylantiradi; readiness ham faqat chinakam o'z trafik qobiliyatiga ta'sir qiladigan bog'liqliklarni tekshirishi kerak. `management.endpoint.health.show-details`ni autentifikatsiyasiz `always` qilib qo'ymang: u ichki hostlar, versiya va konfiguratsiya detallarini oshkor qiladi va health endpointi ham timeout bilan cheklangan bo'lishi lozim.

## 21.10 Audit loglash (Audit Logging)

**Tavsif:** [Xavfsizlik patternlari bobidagi audit log yuritish yozuvi](18-xavfsizlik-patternlari.md#1834-audit-log-yuritish-audit-logging) bu patternning to'liq yozuvi, bu yerda faqat observability nuqtai nazari: audit yozuvi diagnostik logdan farqli ravishda namunalanmaydi, o'chmaydi va formati o'zgarmaydi, shuning uchun alohida store'ga (DB jadvali, append-only topic) yoziladi.

**Spring'da qayerda uchraydi:** Kanonik yozuvdagidan tashqari Actuator'ning `AuthenticationAuditListener` va `AuthorizationAuditListener` login va ruxsat hodisalarini `AuditEvent` sifatida chiqaradi, Envers'da `@AuditTable` va tarixni o'qiydigan `AuditReader` bor, ishonchli yetkazish uchun esa audit yozuvi domen tranzaksiyasi bilan bitta commitda yozilib Transactional Outbox + Debezium/Kafka yoki `@TransactionalEventListener` orqali tashqariga uzatiladi.

**Qo'llanish keyslari:**
- Shaxsiy ma'lumotga kirish (PII access) hodisalarini GDPR uchun hisobga olish va mijoz shikoyatida buyurtma holati zanjirini versiyalar bo'yicha tiklash.

**Ehtiyot bo'ling:** Default `InMemoryAuditEventRepository` restartda hammasini yo'qotadigan demo varianti, fire-and-forget async yuborish esa hodisani jimgina yo'qotadi, shuning uchun audit yozuvi biznes amali bilan atomik bo'lsin.

## 21.11 Xatolarni kuzatish (Exception Tracking)

**Tavsif:** Exception Tracking xatolarni log oqimidagi matn sifatida emas, agregatlangan va deduplikatsiya qilingan "issue"lar sifatida boshqaradi: bir xil stack trace bitta guruhga yig'iladi, uning chastotasi, birinchi/oxirgi ko'rinishi, ta'sirlangan foydalanuvchilar soni va release versiyasi kuzatiladi. Bu minglab takrorlangan qatorlar ichidan haqiqatan yangi yoki o'sib borayotgan xatoni ajratib beradi va regressiyani release bilan bog'laydi. Kontekst (so'rov, user, trace ID, breadcrumbs) xatoga ilashtiriladi, shuning uchun reproduksiya osonlashadi. Natijada xatolar triage qilinadigan ish oqimiga (assign, resolve, ignore) tushadi.

**Spring'da qayerda uchraydi:** Markazlashtirilgan handler sifatida `@ControllerAdvice` + `@ExceptionHandler`, `ResponseEntityExceptionHandler`, `ErrorResponseException` va RFC 9457 `ProblemDetail` ishlatiladi; default xato kontrakti `DefaultErrorAttributes`/`ErrorAttributes` va `/error` (`BasicErrorController`) orqali shakllanadi. Xatolar signal sifatida Micrometer'da `http.server.requests` timerining `exception` tagi va `logback.events{level="error"}` counteri orqali ko'rinadi; Observation API'da `Observation#error(Throwable)` xatoni span'ga biriktiradi (OTel tomonida `recordException`). Tashqi tracker'lar uchun Spring Boot starterlar mavjud: Sentry (`io.sentry:sentry-spring-boot-starter-jakarta` + `sentry-logback`), shuningdek Logback appender orqali boshqa platformalarga yuborish; fon thread'lari uchun `Thread.setDefaultUncaughtExceptionHandler` va `@Async` uchun `AsyncUncaughtExceptionHandler` (`AsyncConfigurer`), scheduler uchun `ErrorHandler` sozlanadi.

**Qo'llanish keyslari:**
- Yangi release'dan keyin paydo bo'lgan yangi exception turini bir necha daqiqada aniqlash.
- `NullPointerException`larni ta'sirlangan foydalanuvchilar soni bo'yicha prioritetlash.
- `@Async`/`@Scheduled` ichida jim yo'qolayotgan xatolarni ushlab olish.
- Xato bilan birga `traceId`ni olib, to'liq trace'ga sakrash.
- Mijozga barqaror `ProblemDetail` kontraktini qaytarib, ichki stack trace'ni yashirish.

**Ehtiyot bo'ling:** Exception'ni log qilib, keyin yana yuqoriga tashlash (log-and-rethrow) bir xatoni bir necha marta hisoblaydi va tracker statistikasini buzadi - mas'uliyatni bitta qatlamda belgilang. Business validation xatolarini (kutilgan 4xx) texnik xato sifatida tracker'ga yubormang: shovqin alert charchoqqa olib keladi; shuningdek xato kontekstiga body va PII solishda maskirovka qoidalarini unutmang.

## 21.12 Deploy va o'zgarishlarni qayd etish (Log Deployments and Changes)

**Tavsif:** Productiondagi incidentlarning katta qismi o'zgarishdan (deploy, config o'zgarishi, feature flag, migration, infra o'zgarishi) keyin yuzaga keladi, shuning uchun o'zgarishlarni telemetriya bilan bir vaqt o'qida ko'rish diagnostikani tezlashtiradi. Bu pattern har bir o'zgarishni mashina o'qiydigan hodisa sifatida qayd etadi (versiya, commit, kim, qachon, qaysi muhit) va uni dashboard'larda annotatsiya yoki metrika tagi sifatida ko'rsatadi. Natijada "latency 14:32 da oshdi" savoliga "14:31 da v2.14.0 chiqdi" javobi darhol topiladi. Shuningdek rollback qarori uchun ob'ektiv asos paydo bo'ladi.

**Spring'da qayerda uchraydi:** Build va git metadata'sini ilova o'zi e'lon qiladi: `spring-boot-maven-plugin`ning `build-info` goal'i (yoki Gradle `springBoot { buildInfo() }`) `META-INF/build-info.properties` yaratadi va `BuildProperties` bean'ini beradi, `io.github.git-commit-id:git-commit-id-maven-plugin` esa `git.properties` → `GitProperties`; bular `/actuator/info` da ko'rinadi (`management.info.git.mode=full`, `management.info.env.enabled`). Versiyani metrikalarga bog'lash uchun `MeterRegistryCustomizer<MeterRegistry>` bilan umumiy tag qo'shiladi (masalan `registry.config().commonTags("version", buildProperties.getVersion())`) yoki `management.metrics.tags.*` propertylari ishlatiladi; OTel tomonida bu `service.version`/`deployment.environment` resource atributlariga mos keladi. Konfiguratsiya o'zgarishlari uchun Spring Cloud Config + `/actuator/refresh`, `@RefreshScope` va `EnvironmentChangeEvent` hodisasi, flag o'zgarishlari uchun esa flag platformasining audit log'i qayd manbasi bo'ladi.

**Qo'llanish keyslari:**
- Grafana'da deploy annotatsiyalarini latency grafigi ustiga chizib, regressiyani versiyaga bog'lash.
- Xato ulushini `version` tagi bo'yicha ajratib, canary va stable'ni solishtirish.
- `/actuator/info` dan commit SHA olib, productionda aynan qaysi kod ishlayotganini tasdiqlash.
- Feature flag yoqilgan vaqtni metrika bilan tenglashtirib, flag'ni aybdor deb aniqlash.
- Incident hisobotida o'zgarishlar xronologiyasini avtomatik to'plash.

**Ehtiyot bo'ling:** `/actuator/info` va `/actuator/env` ni ochiq qoldirish ichki versiya, bog'liqlik va konfiguratsiya detallarini oshkor qiladi - bu endpointlar autentifikatsiya ortida bo'lishi kerak (`management.endpoints.web.exposure.include` ni ehtiyotkorlik bilan sozlang). `version` tagini metrikalarga qo'shish har relizda yangi time-series yaratadi, shuning uchun uni faqat zarur meter'larda yoki qisqa retention bilan ishlatish ma'qul.

## 21.13 Dashboardlar (Dashboards)

**Tavsif:** Dashboard - xom telemetriyani qarorga aylantiradigan qatlam: bir nechta signal (RED, USE, SLO burn rate, deploy annotatsiyalari) bir ekranda, izchil tartibda ko'rsatiladi. Yaxshi dashboard "chiroyli grafiklar to'plami" emas, balki aniq auditoriya va savolga mo'ljallangan vosita: on-call uchun triage paneli, jamoa uchun servis sog'lig'i, biznes uchun funnel. Ular odatda kod sifatida (JSON/Jsonnet/Terraform) saqlanadi va servislar bo'ylab shablonlashtiriladi, shuning uchun yangi servis birinchi kunidan kuzatiladi. Alertlar bilan bitta manba ustida qurilishi tahlil va reaksiyani bir xillashtiradi.

**Spring'da qayerda uchraydi:** Spring Boot tomoni oddiy: `micrometer-registry-prometheus` bilan `/actuator/prometheus` (yoki `management.otlp.metrics.export.url` orqali OTLP) metrikalarni beradi, keyin Prometheus/Mimir ularni saqlaydi va Grafana vizualizatsiya qiladi; `management.endpoints.web.exposure.include=health,info,prometheus` va `management.metrics.tags.application` kabi propertylar panellar uchun barqaror label'larni ta'minlaydi. Grafana'da JVM (Micrometer) va Spring Boot uchun tayyor community dashboardlari mavjud, lekin amalda ular Actuator meter nomlari (`http.server.requests`, `jvm.gc.pause`, `hikaricp.connections`) asosida loyihaga moslashtiriladi. Loglar tomoni Kibana/Grafana Loki, trace tomoni Tempo/Jaeger/Zipkin paneli bilan ulanadi va `traceId` orqali log → trace → metrika o'tishi (exemplars) sozlanadi; Spring Boot Admin esa Actuator ma'lumotlari ustida operatsion UI beradi.

**Qo'llanish keyslari:**
- On-call uchun bitta "golden" triage dashboard: xato ulushi, p99, saturation, deploy annotatsiyalari.
- Har bir servis uchun shablondan avtomatik generatsiya qilinadigan RED paneli.
- Release kuni canary va stable versiyalarni yonma-yon solishtirish.
- Biznes paneli: buyurtmalar oqimi, to'lov muvaffaqiyati, navbat uzunligi.
- Capacity planning uchun oylik trend va bosh vaqt (peak) tahlili.

**Ehtiyot bo'ling:** Dashboard'lar tez "o'lik" bo'lib qoladi - o'nlab panel va 50 ta grafik incident paytida yordam bermaydi, shuning uchun har bir panel aniq savolga javob berishi va kam sonli asosiy ko'rsatkich tepada turishi kerak. Dashboard'ni alert o'rniga ishlatmang (hech kim ekranga qarab turmaydi) va ularni qo'lda tahrirlab qoldirmang: kod sifatida saqlanmagan panellar versiyalanmaydi, nusxalanmaydi va yo'qolib ketadi.

## 21.14 Ogohlantirish (Alerting)

**Tavsif:** Alerting - metrikalar, loglar yoki trace'lar asosida muayyan shart buzilganda javobgar jamoani avtomatik xabardor qilish patterni. Asosiy muammo shundaki, dashboard'ga doim odam qarab o'tirmaydi, shuning uchun anomaliya o'zi "qo'ng'iroq qilishi" kerak. Zamonaviy yondashuv alert'larni resource (CPU, RAM) emas, balki SLO va foydalanuvchi tajribasi (error budget burn rate, p99 latency) ustiga quradi. Har bir alert ortida aniq runbook va aniq egasi bo'lishi shart, aks holda u shovqinga aylanadi.

**Spring'da qayerda uchraydi:** Spring Boot 3.x ilovasi `micrometer-registry-prometheus` orqali `/actuator/prometheus` endpoint'ini beradi, alert qoidalari esa Prometheus Alertmanager yoki Grafana Alerting tomonida PromQL bilan yoziladi. Ilova ichida `HealthIndicator`/`ReactiveHealthIndicator` va `/actuator/health` natijasini Kubernetes liveness/readiness probe'lari kuzatadi; `MeterRegistry` bilan maxsus `Counter`/`Timer` yaratib, ularni alert manbasi qilish mumkin. Spring Boot Admin (`de.codecentric:spring-boot-admin-server`) `InstanceStatusChangeEvent` va `Notifier` interfeysi (`SlackNotifier`, `MailNotifier`) orqali ilova darajasida bildirishnoma yuboradi; `spring-boot-starter-mail` yoki `micrometer-tracing` bilan integratsiya ham keng tarqalgan.

**Qo'llanish keyslari:**
- To'lov servisida 5xx xatolar ulushi 5 daqiqa ichida 1% dan oshganda on-call injenerga PagerDuty orqali qo'ng'iroq qilish.
- SLO error budget burn rate 14x bo'lganda darhol page qilish, 2x bo'lganda esa faqat ticket ochish.
- Kafka consumer lag muayyan chegaradan oshib ketganda integratsiya jamoasiga Slack xabari yuborish.
- HikariCP connection pool'da `hikaricp.connections.pending` nolga teng bo'lmay qolganda DB bo'g'ilishi haqida ogohlantirish.
- Sertifikat yoki JWT signing key amal qilish muddati 14 kundan kam qolganda oldindan eslatma yuborish.

**Ehtiyot bo'ling:** Juda ko'p va noaniq alert "alert fatigue"ga olib keladi - jamoa bildirishnomalarni o'qishni to'xtatadi, natijada haqiqiy incident ham sezilmay qoladi. Har bir alert'ni harakatga undovchi (actionable) qilib yozing: agar alert kelganda qiladigan ishi yo'q bo'lsa, u alert emas, dashboard panelidir.

## 21.15 Namuna olish (Sampling (head, tail))

**Tavsif:** Sampling - barcha trace yoki loglarni saqlamasdan, ularning statistik vakil qismini yig'ish orqali observability xarajatini va overhead'ni kamaytirish patterni. Head-based sampling qarorni trace boshida (root span'da) qabul qiladi va butun trace bo'ylab propagate qiladi, shuning uchun arzon, lekin qiziq xatolarni o'tkazib yuborishi mumkin. Tail-based sampling esa trace to'liq yig'ilgandan keyin qaror qiladi - masalan "xato bo'lgan yoki 2 sekunddan sekin barcha trace'larni saqlash" - bu aniqroq, lekin buffer va collector resursini talab qiladi.

**Spring'da qayerda uchraydi:** Spring Boot 3.x'da `micrometer-tracing-bridge-otel` yoki `-brave` bilan `management.tracing.sampling.probability` property'si head-based ehtimoliy sampler'ni boshqaradi (standart qiymat 0.1). Brave'da bu `brave.sampler.Sampler.create(...)`, OpenTelemetry'da esa `io.opentelemetry.sdk.trace.samplers.Sampler` (`traceIdRatioBased`, `parentBased`, `alwaysOn`) sinflariga mos keladi; maxsus mantiq uchun o'z `Sampler` yoki `SpanExportingPredicate` bean'ini yozish mumkin. Tail-based sampling ilovada emas, OpenTelemetry Collector'ning `tail_sampling` processor'ida amalga oshiriladi; log tomonida esa Logback'ning `ch.qos.logback.classic.turbo.DuplicateMessageFilter` va maxsus `TurboFilter` bilan shovqinni kamaytirish mumkin.

**Qo'llanish keyslari:**
- Kuniga milliardlab so'rov oladigan API'da trace'larning 1% ini saqlab, backend xarajatini keskin tushirish.
- Collector'da tail sampling bilan barcha xatoli va sekin trace'larni 100% saqlash, muvaffaqiyatlilarini 1% qilish.
- Health check va `/actuator/**` endpoint'lari uchun trace'ni butunlay o'chirib, shovqinni yo'qotish.
- Yangi reliz paytida sampling ehtimolini vaqtincha 100% ga oshirib, muammoni chuqur tahlil qilish.
- VIP mijoz yoki debug header kelgan so'rovlar uchun majburiy `alwaysOn` sampling qo'llash.

**Ehtiyot bo'ling:** Agar sampling qarori servislar o'rtasida bir xil propagate qilinmasa, "singan" (incomplete) trace'lar paydo bo'ladi - doim `parentBased` sampler ishlatib, chegara servisida bitta qaror qabul qiling. Shuningdek, past sampling stavkasida metrikani trace'dan hisoblamang: aggregatsiya uchun Micrometer metrikalaridan foydalaning, aks holda raqamlar noto'g'ri chiqadi.

## 21.16 Micrometer Observation API (Micrometer Observation API)

**Tavsif:** Observation API - bitta instrumentatsiya nuqtasidan bir vaqtning o'zida metrika, trace span va log kontekstini chiqarishga imkon beradigan birlashtirilgan abstraksiya. Avval developer `Timer` va `Span`ni alohida yozishi kerak edi va ular bir-biriga mos kelmasligi mumkin edi; Observation bitta "observe" blokidan barcha signal'larni generatsiya qiladi. Ishlash printsipi: `Observation` boshlanadi, unga `KeyValues` (low/high cardinality) qo'shiladi, ro'yxatga olingan `ObservationHandler`lar esa bu hodisalarni o'z backend'iga (Micrometer metrics, Micrometer Tracing, logging) yozadi.

**Spring'da qayerda uchraydi:** `io.micrometer:micrometer-observation` moduli Spring Framework 6.x va Spring Boot 3.x'da markaziy rol o'ynaydi: `ObservationRegistry`, `Observation`, `ObservationHandler`, `ObservationConvention` va `@Observed` annotatsiyasi (`ObservedAspect` bean bilan birga) asosiy API'ni tashkil etadi. Spring Boot avtomatik ravishda `ObservationRegistry` bean'ini sozlaydi va `RestTemplate`, `RestClient`, `WebClient`, Spring MVC/WebFlux, `@Scheduled`, Spring Kafka, Spring AMQP, Spring Data Redis, JDBC hamda Spring Security'ni instrument qiladi; `management.observations.*` property'lari va `ObservationPredicate`/`ObservationFilter` bean'lari orqali filtrlash mumkin. `ServerRequestObservationConvention` kabi convention sinflarini almashtirib tag nomlarini loyihaga moslashtirish mumkin.

```java
@Observed(name = "order.process", contextualName = "process-order")
public Order process(OrderRequest req) { ... }

// yoki imperativ:
Observation.createNotStarted("order.process", registry)
    .lowCardinalityKeyValue("channel", req.channel())
    .observe(() -> repository.save(req.toOrder()));
```

**Qo'llanish keyslari:**
- Biznes metodini `@Observed` bilan belgilab, bir yo'la timer metrikasi va trace span olish.
- Maxsus `ObservationConvention` yozib, barcha HTTP metrikalariga `tenant` kabi yagona tag qo'shish.
- `ObservationPredicate` bilan `/actuator` va health endpoint'larini observability'dan chiqarib tashlash.
- Legacy `@Timed` kodini Observation API'ga ko'chirib, metrika va trace nomlarini birlashtirish.
- Maxsus `ObservationHandler` yozib, har bir observation boshida MDC'ga biznes identifikatorini qo'yish.

**Ehtiyot bo'ling:** Har bir metodga `@Observed` qo'yish katta metrika kardinalligi va sezilarli overhead beradi - faqat arxitektura jihatidan muhim chegaralarni (controller, servis fasadi, tashqi integratsiya) instrument qiling. High-cardinality qiymatlarni (userId, orderId) `lowCardinalityKeyValue` ga hech qachon qo'ymang: ular faqat `highCardinalityKeyValue` orqali trace'ga ketishi kerak.

## 21.17 Kontekstni tarqatish (Context propagation (MDC, ThreadLocal, Reactor))

**Tavsif:** Context propagation - traceId, tenant, correlationId kabi so'rovga bog'liq ma'lumotni chaqiruv zanjiri va thread chegaralari bo'ylab avtomatik olib yurish patterni. Imperativ kodda bu `ThreadLocal` va logging MDC orqali ishlaydi, lekin thread pool, `@Async`, Reactor yoki virtual thread'larga o'tganda kontekst yo'qoladi va loglar "yetim" qolib qoladi. Pattern kontekstni bitta joyda yozib, barcha o'tish nuqtalarida (executor, reactive operator, messaging listener) uzatish vositalarini beradi.

**Spring'da qayerda uchraydi:** `io.micrometer:context-propagation` kutubxonasi `ThreadLocalAccessor` va `ContextSnapshot` abstraksiyalarini beradi; Spring Boot 3.x `ObservationThreadLocalAccessor` ni avtomatik ro'yxatga oladi. Loglash tomonida SLF4J `org.slf4j.MDC` va Logback'ning `%X{traceId}` pattern'i ishlatiladi; Micrometer Tracing `Slf4JEventListener`/`MDCScopeDecorator` bilan `traceId`/`spanId` ni MDC'ga o'zi qo'yadi. Imperativ async uchun `TaskDecorator` va `ContextPropagatingTaskDecorator` (Spring Framework 6.1+) `ThreadPoolTaskExecutor` bilan ishlatiladi; reactive stack'da `Hooks.enableAutomaticContextPropagation()`, `Context`/`ContextView`, `contextWrite`, `deferContextual` va `Mono.transformDeferredContextual` qo'llanadi. Spring Security kontekstini uzatish uchun `DelegatingSecurityContextExecutor` va `SecurityContextHolder.MODE_INHERITABLETHREADLOCAL` mavjud.

**Qo'llanish keyslari:**
- Barcha log satrlariga `traceId` va `tenantId` ni avtomatik qo'shib, Kibana'da bitta so'rovni to'liq ko'rish.
- `@Async` metodlarda `TaskDecorator` orqali MDC va observation kontekstini saqlab qolish.
- WebFlux pipeline'ida `contextWrite` bilan correlationId uzatib, reactive loglarni bog'lash.
- Kafka `@KafkaListener`da header'dan `traceparent` ni olib, producer trace'ini davom ettirish.
- Virtual thread'larga (Java 21+) ko'chganda `ScopedValue`/context propagation bilan `ThreadLocal` leak'laridan qutulish.

**Ehtiyot bo'ling:** `ThreadLocal`ni thread pool'da tozalamaslik eng mashhur xato - qiymat keyingi so'rovga "yopishib" qoladi va noto'g'ri tenant ma'lumoti log yoki biznes mantiqqa o'tib ketishi mumkin; har doim `try/finally` yoki `Observation.Scope`ning `close()` ga tayanch qiling. Reactive kodda `ThreadLocal`ga ishonib bo'lmaydi: kontekstni Reactor `Context` ichida olib yuring va avtomatik propagation'ni yoqishni unutmang.

## 21.18 Sintetik monitoring (Synthetic Monitoring)

**Tavsif:** Synthetic monitoring - real foydalanuvchini kutib o'tirmasdan, tashqaridan sun'iy (robot) so'rovlar yuborib tizim ishlashini doimiy tekshirish patterni. Bu "unknown unknowns"ni va past trafikli vaqtda yuzaga keladigan muammolarni ochadi: DNS, TLS, CDN, login flow, to'lov yo'li. Odatda belgilangan interval bilan kritik foydalanuvchi yo'llari (user journey) bajariladi va natija latency, availability metrikasiga aylanadi. Real User Monitoring (RUM) dan farqi - sintetik test boshqariladigan, takrorlanadigan va trafik yo'q bo'lsa ham ishlaydi.

**Spring'da qayerda uchraydi:** Spring Boot ilovasi uchun probe maqsadi `/actuator/health`, `/actuator/health/readiness` va `HealthIndicator` bilan yozilgan maxsus tekshiruvlar bo'ladi; tashqi tekshiruvchini esa alohida Spring Boot "canary" ilovasi sifatida `@Scheduled` + `RestClient`/`WebClient` bilan yozib, natijani `MeterRegistry`ga `Timer`/`Gauge` sifatida yozish mumkin. Kengroq ekotizimda Blackbox Exporter, Grafana Synthetic Monitoring, k6, Playwright yoki Selenium skriptlari ishlatiladi; API kontraktini tekshirish uchun `spring-boot-starter-test` va `RestAssured` bilan yozilgan smoke test'larni CI'dan keyin production'ga qarshi ishga tushirish keng tarqalgan. Spring Boot Admin ham ilovalar ro'yxatini davriy ravishda tekshirib turadi.

**Qo'llanish keyslari:**
- Har 60 sekundda login → savatga qo'shish → checkout yo'lini sun'iy bajarib, konversiya yo'li tirikligini tasdiqlash.
- Bir nechta geografik region'dan probe yuborib, CDN yoki DNS muammolarini aniqlash.
- Deploy'dan keyin avtomatik smoke test ishga tushirib, nosoz reliz'ni darhol rollback qilish.
- Tungi past trafik paytida ham SLA availability raqamini o'lchash uchun doimiy probe yuritish.
- TLS sertifikat va tashqi to'lov provayderi integratsiyasini kunlik sintetik tranzaksiya bilan tekshirish.

**Ehtiyot bo'ling:** Sintetik trafik production metrikalari va biznes KPI'larini buzishi mumkin - probe so'rovlarini maxsus header yoki user-agent bilan belgilab, analitika va konversiya hisob-kitobidan chiqarib tashlang. Sintetik test real foydalanuvchi xilma-xilligini qoplamaydi, shuning uchun uni RUM o'rniga emas, qo'shimcha sifatida ishlatish kerak.

## 21.19 Log darajasini ish vaqtida o'zgartirish (Runtime log level change (Actuator loggers))

**Tavsif:** Bu pattern ilovani qayta ishga tushirmasdan, ishlab turgan jarayonda log darajasini (DEBUG, TRACE) vaqtincha ko'tarish imkonini beradi. Muammo oddiy: production'da hamma narsani DEBUG'da yozib bo'lmaydi (xarajat va shovqin), lekin incident paytida aynan batafsil log kerak bo'ladi. Yechim - logger konfiguratsiyasini boshqaruvchi management endpoint orqali bitta package yoki sinfning darajasini dinamik o'zgartirish, muammo hal bo'lgach qaytarib qo'yish.

**Spring'da qayerda uchraydi:** Spring Boot 3.x'da `org.springframework.boot.actuate.logging.LoggersEndpoint` `/actuator/loggers` ni ta'minlaydi: `GET /actuator/loggers/com.acme.payment` joriy holatni ko'rsatadi, `POST` bilan `{"configuredLevel":"DEBUG"}` yuborilsa daraja o'zgaradi, `null` yuborilsa asl holatga qaytadi. Buning ostida `LoggingSystem` abstraksiyasi (`LogbackLoggingSystem`, `Log4J2LoggingSystem`) yotadi; endpoint `management.endpoints.web.exposure.include=loggers` bilan ochiladi va `logging.level.*` property'lari boshlang'ich qiymatni beradi. Spring Boot Admin UI aynan shu endpoint ustida grafik logger boshqaruvini beradi; Logback'ning `scan=true` konfiguratsiyasi va Log4j2'ning `monitorInterval` atributi esa fayl orqali qayta yuklash variantini beradi.

**Qo'llanish keyslari:**
- Incident paytida faqat `com.acme.integration.swift` package'ini DEBUG'ga ko'tarib, tashqi integratsiya xatosini aniqlash.
- Spring Security yoki `org.hibernate.SQL` loglarini vaqtincha yoqib, autentifikatsiya yoki query muammosini tekshirish.
- Spring Boot Admin UI'dan bir klik bilan ma'lum pod'da TRACE yoqib, so'ng qaytarib qo'yish.
- CI/CD pipeline'dan API chaqirib, canary pod'da debug loglarni avtomatik yoqish.
- Mijoz shikoyati bo'yicha muayyan modulni batafsil kuzatib, keyin `null` yuborib standart darajaga qaytish.

**Ehtiyot bo'ling:** `/actuator/loggers` - kuchli vosita, shuning uchun u hech qachon autentifikatsiyasiz ochiq bo'lmasligi kerak: Spring Security bilan himoyalang va faqat ichki management port'da (`management.server.port`) chiqaring. DEBUG'ni keng package'ga (`org.springframework` yoki root) yoqib qo'yib esdan chiqarish disk va log backend xarajatini portlatadi hamda latency'ni oshiradi - doim vaqt chegarasi bilan ishlatib, qaytarishni unutmang.

## 21.20 Metrika teglari kardinalligini nazorat qilish (Metrics tag cardinality control)

**Tavsif:** Har bir unikal tag qiymatlari kombinatsiyasi alohida time series yaratadi, shuning uchun nazoratsiz teglar metrika backend'ini "portlatib" yuboradi (cardinality explosion). Pattern teg qiymatlarini ataylab cheklashni talab qiladi: faqat chegaralangan to'plamdan (status kodi, metod, outcome) foydalanish, userId/orderId/URL path kabi cheksiz qiymatlarni esa metrikadan chiqarib, trace yoki logga yuborish. Amalda bu URI'ni template'ga normalizatsiya qilish, noma'lum qiymatlarni `UNKNOWN` ga yig'ish va registry darajasida filtr qo'yish bilan amalga oshiriladi.

**Spring'da qayerda uchraydi:** Micrometer'da `MeterFilter` asosiy vosita: `MeterFilter.maximumAllowableTags(...)`, `MeterFilter.maximumAllowableMetrics(...)`, `MeterFilter.ignoreTags(...)`, `MeterFilter.denyNameStartsWith(...)` va `MeterFilter.replaceTagValues(...)` bean sifatida e'lon qilinsa `MeterRegistry`ga avtomatik qo'llanadi. Spring MVC `http.server.requests` metrikasida URI `@PathVariable` template'i (`/orders/{id}`) sifatida yoziladi - buni `ServerRequestObservationConvention` yoki `DefaultServerRequestObservationConvention` ni kengaytirib boshqarish mumkin; `management.metrics.tags.*` property'lari umumiy teg qo'shadi. Observation API tomonida `lowCardinalityKeyValue` va `highCardinalityKeyValue` ajratmasi aynan shu muammoni hal qiladi, chunki low-cardinality teglar metrikaga, high-cardinality esa faqat span'ga ketadi.

```java
@Bean
MeterFilter cardinalityGuard() {
    return MeterFilter.maximumAllowableTags(
        "http.server.requests", "uri", 200, MeterFilter.deny());
}
```

**Qo'llanish keyslari:**
- Noto'g'ri yozilgan controller tufayli `uri` tegiga ID'lar tushib ketganda cheklov qo'yib Prometheus'ni saqlab qolish.
- Multi-tenant SaaS'da minglab tenant ID o'rniga faqat tenant tier (`free`, `pro`) tegidan foydalanish.
- `MeterFilter.ignoreTags("exception")` bilan cheksiz exception sinf nomlarini metrikadan chiqarish.
- Faqat kerakli metrikalarni qoldirib, qolganini `denyUnless` bilan o'chirib scrape hajmini kamaytirish.
- Legacy integratsiyadan kelgan dinamik metrika nomlarini `replaceTagValues` bilan normalizatsiya qilish.

**Ehtiyot bo'ling:** Kardinallik portlashi odatda sekin-asta keladi va faqat Prometheus OOM bo'lganda sezila boshlaydi - `prometheus_tsdb_symbol_table_size_bytes` va series sonini oldindan kuzatib turing. `maximumAllowableTags` chegarasi oshganda ma'lumot jim yo'qoladi, shuning uchun bu himoya chorasi bo'lsin, asosiy dizayn emas: teg to'plamini boshidan chegaralangan qilib loyihalashtirish to'g'riroq.

## 21.21 Heartbeat / Watchdog (Heartbeat / Watchdog)

**Tavsif:** Heartbeat - komponent muntazam interval bilan "men tirikman" signalini yuborishi, Watchdog esa bu signal kelmay qolganda choragni ko'rish (restart, failover, alert) mexanizmi. Bu pattern passiv health check yetarli bo'lmagan holatlarda kerak: jarayon tirik, port javob beradi, lekin ichki worker o'lgan yoki thread deadlock'da qotgan. Signal yo'qligi muammoning o'zi bo'lib hisoblanadi - shuning uchun "dead man's switch" mantiqi ishlatiladi: xabar kelmasa, tizim nosoz deb qabul qilinadi.

**Spring'da qayerda uchraydi:** Eng oddiy ko'rinishi - `@Scheduled(fixedDelay = ...)` metodi `MeterRegistry`ga `Gauge` yoki `Counter` yozib turishi va monitoring tomonida `absent()`/`time() - last_heartbeat` alert'i bo'lishi. Spring Boot 3.x'da `HealthIndicator`/`AbstractHealthIndicator` va `HealthContributor` maxsus liveness tekshiruvi yozishga, `AvailabilityChangeEvent` bilan `LivenessState.BROKEN` ni e'lon qilish esa Kubernetes liveness probe'ni muvaffaqiyatsiz qilishga imkon beradi (`management.endpoint.health.probes.enabled=true`). Spring Integration'da `spring-integration-core` ichidagi heartbeat kanal pattern'i, Spring Cloud Bus va Spring Cloud Consul/Eureka client'lari (`eureka.instance.lease-renewal-interval-in-seconds`) registry'ga davriy heartbeat yuboradi; Spring Cloud Stream Kafka binder'da consumer `heartbeat.interval.ms` va `session.timeout.ms` orqali guruh a'zoligini ushlab turadi.

**Qo'llanish keyslari:**
- Batch worker har daqiqada heartbeat yozadi, 5 daqiqa jim qolsa watchdog pod'ni restart qiladi.
- Eureka/Consul'da instance lease yangilanmasa, load balancer uni avtomatik ro'yxatdan chiqaradi.
- Kafka consumer thread'i qotganda `AvailabilityChangeEvent` bilan liveness probe'ni "fail" qilib pod'ni almashtirish.
- Scheduler (quartz) job'ining oxirgi ishlagan vaqtini gauge qilib, cron o'tkazib yuborilganini aniqlash.
- WebSocket yoki long-lived gRPC ulanishida ping/pong heartbeat bilan "yarim ochiq" socket'larni tozalash.

**Ehtiyot bo'ling:** Haddan ziyod qattiq watchdog "restart loop"ga olib keladi: vaqtinchalik DB sekinligi heartbeat'ni kechiktiradi, pod restart bo'ladi, holat yanada yomonlashadi - timeout'ni real p99 dan ancha katta qilib, grace period qo'shing. Liveness probe'ga tashqi bog'liqliklarni (DB, boshqa servis) qo'shmang: bu kaskadli restart'lar va butun klasterning qulashiga sabab bo'ladi - tashqi bog'liqliklar readiness'ga tegishli.

## 21.22 Uzluksiz profiling (Continuous Profiling (JFR))

**Tavsif:** Continuous profiling - production'da doimiy, juda past overhead bilan CPU, allocation, lock va I/O profilini yig'ib turish patterni. Metrika "qancha sekin" degan savolga javob beradi, trace "qaysi servisda" deydi, profiling esa "qaysi metod va qaysi qatorda" degan eng chuqur darajani ochadi. Java'da buning asosi JDK Flight Recorder (JFR) - JVM ichiga qurilgan, event asosida ishlaydigan va odatda 1-2% dan kam overhead beradigan mexanizm. Yig'ilgan rekordlar flame graph sifatida tahlil qilinadi va reliz'lar o'rtasida qiyoslanadi.

**Spring'da qayerda uchraydi:** JFR JVM darajasida yoqiladi: `-XX:StartFlightRecording=duration=60s,filename=app.jfr,settings=profile` yoki ishlab turgan jarayonda `jcmd <pid> JFR.start`. Spring Boot 3.x'da `/actuator/startup` (`BufferingApplicationStartup` bilan) va `ApplicationStartup` API ishga tushish bosqichlarini o'lchaydi, `FlightRecorderApplicationStartup` (`org.springframework.core.metrics.jfr`) esa startup qadamlarini to'g'ridan-to'g'ri JFR event sifatida yozadi. Java 17-25 oralig'ida JFR'ning `jdk.ObjectAllocationSample`, `jdk.ExecutionSample` event'lari standart; `jdk.jfr.Event` ni kengaytirib o'z biznes event'laringizni yozishingiz mumkin, `/actuator/heapdump` va `/actuator/threaddump` esa bir martalik diagnostika beradi. Ekotizimda `async-profiler`, Grafana Pyroscope, Datadog yoki JFR Event Streaming API (`jdk.jfr.consumer.RecordingStream`) bilan uzluksiz yig'ish qo'llanadi.

**Qo'llanish keyslari:**
- Production'da CPU 80% ga chiqqan paytda flame graph olib, aybdor regex yoki serializatsiya metodini topish.
- Allocation profiling bilan ortiqcha garbage yaratayotgan DTO mapping kodini aniqlash.
- Lock contention event'lari orqali `synchronized` bo'g'ilish nuqtasini (bottleneck) ochish.
- Reliz oldidan va keyin profil olib, regressiyani metod darajasida qiyoslash.
- `FlightRecorderApplicationStartup` bilan Spring Boot startup vaqtini bean darajasida qisqartirish.

**Ehtiyot bo'ling:** `settings=profile` profili `default`ga qaraganda ancha qimmat - uni tekshirmasdan butun flotga yoqish latency'ga ta'sir qilishi mumkin; avval bitta canary instance'da o'lchab ko'ring. JFR fayllari stack trace, SQL va ba'zan parametr qiymatlarini o'z ichiga oladi, shuning uchun ularni maxfiy ma'lumot sifatida saqlang va ruxsatsiz joyga yuklamang.

## 21.23 Biznes metrikalari / KPI (Business metrics / KPIs)

**Tavsif:** Bu pattern texnik metrikalar yonida biznes ma'nosiga ega o'lchovlarni (buyurtmalar soni, muvaffaqiyatli to'lovlar ulushi, ro'yxatdan o'tish konversiyasi, savat tashlab ketish) bir xil observability quvuri bilan yig'ishni taklif qiladi. Sababi aniq: CPU va latency normal bo'lsa ham, biznes to'xtab qolgan bo'lishi mumkin - masalan to'lov provayderi jim ravishda hamma tranzaksiyani rad etadi. Biznes metrikasi incident'ni foydalanuvchi nuqtai nazaridan aniqlaydi va texnik dashboard bilan bitta vaqt o'qida solishtirishga imkon beradi.

**Spring'da qayerda uchraydi:** Micrometer'ning `Counter`, `Timer`, `Gauge`, `DistributionSummary` primitivlari `MeterRegistry` orqali servis sinflarida to'g'ridan-to'g'ri ishlatiladi; `@Counted` va `@Timed` annotatsiyalari (`CountedAspect`/`TimedAspect` bean'lari bilan) deklarativ variantni beradi. `Gauge.builder("orders.pending", repo, OrderRepository::countPending).register(registry)` ko'rinishida DB holatini kuzatish mumkin; `@Observed` bilan biznes operatsiyasini metrika va trace'ga bir vaqtda chiqarish mumkin. Spring Modulith'ning `spring-modulith-observability` moduli modul chegaralarini avtomatik instrument qiladi, `ApplicationEventPublisher` va `@TransactionalEventListener` esa domen hodisalarini metrikaga aylantirish uchun qulay nuqta beradi.

**Qo'llanish keyslari:**
- Daqiqada yaratilgan buyurtmalar sonini `Counter` qilib, kutilgan darajadan pastga tushsa alert berish.
- To'lov provayderi bo'yicha muvaffaqiyat/xato nisbatini `Counter` tegida (`provider`, `outcome`) kuzatish.
- Ro'yxatdan o'tish funnel'ining har bosqichini o'lchab, konversiya pasayishini aniqlash.
- Navbatdagi (pending) hujjatlar sonini `Gauge` bilan ko'rsatib, backlog o'sishini oldini olish.
- Reliz paytida biznes KPI'ni kuzatib, texnik ko'rsatkichlar yaxshi bo'lsa ham regressiyani sezish.

**Ehtiyot bo'ling:** Biznes metrikasi hisob-kitob (billing) manbai emas - Micrometer metrikalari sampling, restart va scrape oynasi tufayli yo'qolishi mumkin, shuning uchun moliyaviy hisobot uchun doim tranzaksion ma'lumotdan foydalaning. Teglarga mijoz identifikatori yoki email kabi shaxsiy va cheksiz qiymatlarni qo'ymang: bu ham kardinallik portlashi, ham maxfiylik (PII) muammosi.

## 21.24 OpenTelemetry Collector (OpenTelemetry Collector (agent, sidecar))

**Tavsif:** Collector - ilovalardan telemetriyani (trace, metrika, log) qabul qilib, uni qayta ishlab (filtr, batch, sampling, atribut qo'shish) bir yoki bir nechta backend'ga yuboruvchi mustaqil jarayon. Asosiy foydasi - ilovani backend'dan ajratish: exporter konfiguratsiyasi, autentifikatsiya va yo'naltirish ilova kodidan tashqariga chiqadi, shuning uchun vendor almashtirish uchun deploy qilish shart emas. Deployment ko'rinishlari: agent (har node'da DaemonSet), sidecar (har pod ichida) va gateway (markaziy klaster).

**Spring'da qayerda uchraydi:** Spring Boot 3.x'da `micrometer-tracing-bridge-otel` + `opentelemetry-exporter-otlp` bog'liqliklari bilan OTLP eksporti yoqiladi va `management.otlp.tracing.endpoint`, `management.otlp.metrics.export.url` hamda `management.otlp.logging.endpoint` (Boot 3.4+) property'lari Collector manzilini ko'rsatadi. Kod o'zgartirmasdan ishlatish uchun `opentelemetry-javaagent.jar` ni `-javaagent:` bilan ulash mumkin - u Spring MVC, WebFlux, JDBC, Kafka va boshqa kutubxonalarni avtomatik instrument qiladi (`OTEL_EXPORTER_OTLP_ENDPOINT`, `OTEL_SERVICE_NAME`, `OTEL_RESOURCE_ATTRIBUTES` environment o'zgaruvchilari bilan). Collector tomonida `otlp` receiver, `batch`, `memory_limiter`, `resourcedetection`, `tail_sampling`, `attributes` processor'lari va Tempo/Jaeger/Prometheus exporter'lari sozlanadi; Kubernetes'da OpenTelemetry Operator `Instrumentation` CRD bilan sidecar va agent injection'ni avtomatlashtiradi.

**Qo'llanish keyslari:**
- Barcha mikroservislar telemetriyasini bitta gateway Collector'ga yuborib, Jaeger'dan Tempo'ga deploy'siz ko'chish.
- Sidecar Collector bilan tarmoq uzilishida telemetriyani buferlab, ma'lumot yo'qotishini kamaytirish.
- Collector'da `tail_sampling` processor bilan faqat xatoli va sekin trace'larni saqlash.
- `attributes` processor orqali PII (email, token) maydonlarini backend'ga chiqishdan oldin o'chirish.
- `resourcedetection` bilan `k8s.pod.name`, `cloud.region` kabi atributlarni markazda avtomatik qo'shish.

**Ehtiyot bo'ling:** Markaziy gateway Collector'ni bitta replika qilib qo'yish yagona nosozlik nuqtasi (SPOF) yaratadi va u o'lgan paytda butun observability ko'r bo'ladi - gorizontal scale, `memory_limiter` va `sending_queue` bilan backpressure'ni sozlang. OpenTelemetry javaagent'ni Micrometer Tracing bridge bilan birga ishlatganda bir operatsiya uchun ikki marta span paydo bo'lishi mumkin, shuning uchun bitta instrumentatsiya yo'lini tanlang.

## 21.25 Exemplar'lar (Exemplars (logs-metrics-traces correlation))

**Tavsif:** Exemplar - agregat metrika namunasiga (masalan latency histogram bucket'iga) aniq bir so'rovning `traceId`si ilova qilib qo'yilishi. Bu "p99 latency sakrab ketdi" degan grafikdan bir klik bilan aynan shu sekin so'rovning trace'iga o'tish imkonini beradi, ya'ni agregatdan individual holatga ko'prik quradi. Loglar bilan korrelyatsiya esa MDC'ga yozilgan `traceId`/`spanId` orqali ishlaydi, natijada uch signal (metrics → traces → logs) bir-biriga bog'lanadi. Shu tarzda debug qilish vaqti (MTTR) sezilarli qisqaradi, chunki "qaysi so'rovni ko'rish kerak" degan izlanish yo'qoladi.

**Spring'da qayerda uchraydi:** Spring Boot 3.x'da `micrometer-registry-prometheus` (Prometheus Java client 1.x) va `micrometer-tracing` birga bo'lganda exemplar'lar avtomatik qo'shiladi: histogram uchun `management.metrics.distribution.percentiles-histogram.http.server.requests=true` yoqilib, `/actuator/prometheus` OpenMetrics formatida (`Accept: application/openmetrics-text`) `# {trace_id="..."}` qo'shimchasini chiqaradi; eski versiyalarda `SpanContextSupplier` bean'i kerak bo'lgan. Log korrelyatsiyasi `logging.pattern.level` ning standart `%5p [${spring.application.name:},%X{traceId:-},%X{spanId:-}]` ko'rinishi bilan ta'minlanadi - bu `MDCScopeDecorator`/`Slf4JEventListener` MDC'ga qo'ygan qiymatlarni o'qiydi. Grafana tomonida Prometheus data source'da "Exemplars" va Tempo'ning "Traces to logs"/"Logs to traces" sozlamalari, OTLP yo'lida esa `management.otlp.metrics` eksporti ishlatiladi.

**Qo'llanish keyslari:**
- Grafana'dagi latency grafigining eng baland nuqtasidan to'g'ridan-to'g'ri sekin so'rov trace'iga o'tish.
- Xato darajasi (error rate) grafigidan muvaffaqiyatsiz tranzaksiyaning aniq span'ini topish.
- Loki'da `traceId` bo'yicha filtr qilib, bitta so'rovning barcha servislardagi loglarini yig'ish.
- Trace'dan tegishli pod loglariga "Traces to logs" havolasi bilan sakrab, root cause'ni tasdiqlash.
- Yuklama testida p99'ga tushgan namunalarni exemplar orqali ochib, qaysi downstream aybdor ekanini aniqlash.

**Ehtiyot bo'ling:** Exemplar faqat sampling natijasida saqlangan trace'ga ishora qilsa foydali - agar sampling ehtimoli past bo'lsa, havola "trace topilmadi" degan natija beradi, shuning uchun xatoli va sekin so'rovlar uchun tail sampling bilan birga ishlatish kerak. Exemplar'lar scrape hajmini oshiradi va faqat histogram/counter turlari hamda OpenMetrics formatida ishlaydi, shuning uchun ularni barcha metrikalarga yoqish o'rniga kritik SLI'lar bilan cheklang.

## 21.26 Amalda qo'llash

- [ ] Har bir so'rov uchun correlation ID yaratilayotganini va u tashqi chaqiruvlarga uzatilayotganini tasdiqlang.
- [ ] Log yozuvlarini tekshiring: struktura (JSON) bormi, maxfiy ma'lumot log'ga tushmayaptimi.
- [ ] Log darajalarini qayta ko'rib chiqing: `INFO` da har so'rov uchun necha qator chiqadi, bu hajm qancha turadi.
- [ ] Biznes metrikalarini sanab chiqing; faqat texnik metrika bo'lsa, nosozlikni biznes tomonidan ko'rib bo'lmaydi.
- [ ] Trace sampling darajasini yozib qo'ying va xato bo'lgan so'rovlar har doim saqlanayotganini tasdiqlang.
- [ ] Health endpoint'lari tashqi tizim holatini qaytarmasligini tekshiring - aks holda bitta tashqi uzilish butun klasterni yiqitadi.
- [ ] Har bir alert uchun savolga javob yozing: bu alert kelganda odam nima qiladi. Javob yo'q bo'lsa, alertni olib tashlang.
- [ ] Kuzatuvchanlik narxini oyiga hisoblab chiqing va eng qimmat uch manbani aniqlang.

---

[&larr; 20. Batch va scheduling patternlari](20-batch-va-scheduling-patternlari.md) · [Mundarija](README.md) · [22. Deployment va operatsion patternlar &rarr;](22-deployment-va-operatsion-patternlar.md)
