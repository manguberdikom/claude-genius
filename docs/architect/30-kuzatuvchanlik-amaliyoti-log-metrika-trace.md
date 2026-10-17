<!-- doc: architect | chapter: 30 | part: V. Atrof ekotizim: operatsion haqiqat -->

[Barcha hujjatlar](../../README.md) / [Arxitektor miyasi](README.md)

> Holat: tekshirilmoqda. Da'volar hali manbaga solishtirilmoqda.

# 30. Kuzatuvchanlik amaliyoti: log, metrika, trace va ularning narxi (Observability in Practice)

<details>
<summary>Bu bobdagi 14 bo'lim</summary>

- [30.1 Uchta manba: log, metrika, trace va har biri qaysi savolga javob beradi](#301-uchta-manba-log-metrika-trace-va-har-biri-qaysi-savolga-javob-beradi)
- [30.2 Tuzilgan (strukturali) log: JSON format, maydon nomlari, trace id bog'lash](#302-tuzilgan-strukturali-log-json-format-maydon-nomlari-trace-id-boglash)
- [30.3 Log darajalari siyosati va ishlab chiqarishda nimani yozmaslik kerak](#303-log-darajalari-siyosati-va-ishlab-chiqarishda-nimani-yozmaslik-kerak)
- [30.4 Log hajmi va narxi: bitta so'rovga nechta qator yozilyapti](#304-log-hajmi-va-narxi-bitta-sorovga-nechta-qator-yozilyapti)
- [30.5 Micrometer bilan metrika: counter, gauge, timer, distribution summary](#305-micrometer-bilan-metrika-counter-gauge-timer-distribution-summary)
- [30.6 Kardinallik portlashi: metrika tegiga foydalanuvchi id qo'yish xatosi](#306-kardinallik-portlashi-metrika-tegiga-foydalanuvchi-id-qoyish-xatosi)
- [30.7 Qaysi metrikalar majburiy: so'rov soni, xato ulushi, kechikish taqsimoti, resurs](#307-qaysi-metrikalar-majburiy-sorov-soni-xato-ulushi-kechikish-taqsimoti-resurs)
- [30.8 OpenTelemetry: trace, span, kontekst tarqalishi va namuna olish (sampling)](#308-opentelemetry-trace-span-kontekst-tarqalishi-va-namuna-olish-sampling)
- [30.9 Namuna olish darajasi tanlash va xatoli so'rovlarni to'liq saqlash](#309-namuna-olish-darajasi-tanlash-va-xatoli-sorovlarni-toliq-saqlash)
- [30.10 Ogohlantirish (alert) dizayni: belgiga emas, foydalanuvchi ta'siriga qarab](#3010-ogohlantirish-alert-dizayni-belgiga-emas-foydalanuvchi-tasiriga-qarab)
- [30.11 Dashboard qanday bo'lishi kerak: birinchi ekranda nima turadi](#3011-dashboard-qanday-bolishi-kerak-birinchi-ekranda-nima-turadi)
- [30.12 Spring Boot Actuator va Micrometer sozlash amaliyoti](#3012-spring-boot-actuator-va-micrometer-sozlash-amaliyoti)
- [30.13 Statik chegara va anomaliya aniqlash: alert qoidasi qanday shaklda bo'ladi](#3013-statik-chegara-va-anomaliya-aniqlash-alert-qoidasi-qanday-shaklda-boladi)
- [30.14 Amalda qo'llash](#3014-amalda-qollash)

</details>



Kuzatuvchanlik tizim ishlayotganini emas, nega ishlamayotganini aytib berishi kerak. Ko'p jamoada bu teskari: dashboard yashil, log to'la, lekin "to'lov nega 14:20 da sekinlashdi" degan savolga javob yo'q. Sabab oddiy: uchta manba o'ylamasdan yoqilgan, holbuki har birining alohida narxi va alohida savoli bor. Bu bobda shu uchlikning mexanikasi, raqamlari va arxitektor tanlovlari ko'rib chiqiladi.

## 30.1 Uchta manba: log, metrika, trace va har biri qaysi savolga javob beradi

Log bitta hodisaning batafsil yozuvi, metrika vaqt bo'yicha agregatlangan son, trace bitta so'rovning servislar bo'ylab yo'li. Ular bir-birini almashtirmaydi. Metrika "muammo bormi va qanchalik katta" degan savolga javob beradi, trace "qaysi bo'g'inda" deydi, log "aynan nima bo'ldi" deb yopadi. Arxitektor xatosi odatda bittasini qolganlarining o'rniga ishlatishga urinishdir: metrikaga foydalanuvchi id qo'yib log o'rnida ishlatish, yoki har bir so'rovga 20 qator log yozib metrika o'rnini bosishga urinish.

| Manba | Qaysi savolga javob beradi | Narx drayveri | Saqlash muddati (taxminan) |
|---|---|---|---|
| Metrika | Muammo bormi, qancha davom etdi, trend qanday | Vaqt qatorlari (series) soni | 13-15 oy, past rezolyutsiyada |
| Trace | Kechikish qaysi servis yoki qaysi SQL da yo'qoldi | Span soni va sampling darajasi | 7-15 kun |
| Log | Aynan qaysi qiymat bilan nima qilindi | Ingest GB va indekslangan hodisa soni | 7-30 kun, arxiv 1 yil |

Metrika hamma so'rovni qamraydi, lekin detalsiz. Trace detalli, lekin faqat namuna. Log eng qimmat, demak eng tanlangan. Uchlikni bog'lovchi yagona narsa trace id, va u uchala manbada bir xil nomda bo'lsin.

## 30.2 Tuzilgan (strukturali) log: JSON format, maydon nomlari, trace id bog'lash

Matn ichiga qiymat yopishtirilgan log qidirib bo'lmaydigan log. `log.info("Payment " + id + " failed with " + code)` yozilsa, log tizimi buni 10 ming xil xabar deb ko'radi va guruhlay olmaydi. Xabar matni doimiy bo'lishi, o'zgaruvchilar alohida maydon bo'lishi kerak. SLF4J 2.x fluent API aynan shuni beradi.

```java
// To'lov servisi: xabar matni barqaror, o'zgaruvchilar maydon sifatida chiqadi
@Service
public class PaymentService {
    private static final Logger log = LoggerFactory.getLogger(PaymentService.class);

    public CaptureResult capture(PaymentCommand cmd) {
        long start = System.nanoTime();
        try {
            CaptureResult result = gateway.capture(cmd);
            log.atInfo()
               .setMessage("payment captured")          // matn hech qachon o'zgarmaydi
               .addKeyValue("orderId", cmd.orderId())
               .addKeyValue("amountMinor", cmd.amountMinor())
               .addKeyValue("gateway", result.gatewayName())
               .addKeyValue("durationMs", (System.nanoTime() - start) / 1_000_000)
               .log();
            return result;
        } catch (GatewayTimeoutException e) {
            // stack trace faqat eng yuqori qatlamda bir marta yoziladi
            log.atWarn().setMessage("payment capture timeout")
               .addKeyValue("orderId", cmd.orderId()).log();
            throw e;
        }
    }
}
```

Maydon nomlari bo'yicha kelishuv kerak, aks holda har jamoa `order_id`, `orderId`, `oid` yozadi va qidirish imkonsiz bo'ladi. Bitta sxemani tanlang va uni code review darvozasi bilan majburlang. Spring Boot 3.4 dan boshlab strukturali log framework ichida bor, qo'shimcha encoder kutubxonasi shart emas.

```properties
# Konsolga ECS formatida JSON, fayl ham bir xil formatda
logging.structured.format.console=ecs
logging.structured.format.file=ecs
logging.structured.ecs.service.name=payment-service
logging.structured.ecs.service.environment=prod
# Agar oddiy matn formati qolsa, trace id patternga qo'lda qo'shiladi
logging.pattern.level=%5p [${spring.application.name:},%X{traceId:-},%X{spanId:-}]
# Lokalda o'qish uchun strukturali log o'chiriladi (dev profilda)
```

Trace id MDC ga Micrometer Tracing tomonidan avtomatik qo'yiladi. Agar siz `@Async` yoki o'z `ExecutorService` ingizdan foydalansangiz, MDC yangi thread ga ko'chmaydi va log trace siz qoladi. Yechim: Spring taqdim etadigan context propagation mexanizmi orqali executor ni o'rash, yoki `TaskDecorator` ishlatish. Buni bir marta infratuzilma darajasida qiling, har bir servisda emas.

## 30.3 Log darajalari siyosati va ishlab chiqarishda nimani yozmaslik kerak

Daraja siyosati yozilmagan loyihada hamma narsa INFO bo'lib qoladi. Amaliy mezon: ERROR faqat odam aralashuvi kerak bo'lgan holat, WARN tizim o'zi tiklandi lekin bilish kerak, INFO biznes holati o'zgarishi, DEBUG prodda o'chiq. Eng ko'p uchraydigan xato: kutilgan biznes rad etishni ("ombor qoldig'i yetmadi") ERROR deb yozish. Bu bir oy ichida hamma ERROR ni e'tiborsiz qoldiradi.

Prodda log ga tushmasligi kerak: parol va token, karta raqami va CVV, to'liq `Authorization` header, shaxsiy ma'lumot, butun request body, entity `toString()`. Hibernate entity ni log ga bersangiz, `toString()` lazy kolleksiyani tortib yuborishi mumkin va bitta log qatori 50 ta qo'shimcha SQL ga aylanadi. Maskirovkani appender darajasida qiling, chunki har bir yangi maydon yana risk.

`DEBUG` ni prodda yoqish kerak bo'lsa, butun servis uchun emas, bitta package uchun va vaqt bilan cheklangan qiling. Actuator `loggers` endpointi buni restart siz beradi, lekin faqat himoyalangan portda turishi kerak.

## 30.4 Log hajmi va narxi: bitta so'rovga nechta qator yozilyapti

Bu savolni hech kim so'ramaydi, keyin hisob keladi. Hisob oddiy: 2000 rps, bitta so'rovga 12 qator, qator 400 bayt bo'lsa, bu 24 000 qator/s, 9.6 MB/s, kuniga taxminan 830 GB. Ingest narxi GB bo'yicha olinadigan tizimda bu yillik byudjetni yolg'iz yeb qo'yadi. 12 qator ko'p emas deb tuyuladi, lekin ko'pi "method entered" yoki "mapping dto" kabi qiymatsiz qatorlar.

```bash
# Bitta so'rovga qancha qator yozilayotganini o'lchash: bitta trace id ni sanash
TRACE=$(curl -s -D- -o /dev/null http://localhost:8080/api/orders/42 \
  | grep -i '^traceresponse' | cut -d- -f2)
grep -c "\"trace.id\":\"$TRACE\"" /var/log/app/app.json

# Qaysi xabar matnlari hajmni yeyayotganini topish (eng qimmat 10 ta)
jq -r '.message' /var/log/app/app.json | sort | uniq -c | sort -rn | head -10

# Kunlik hajm prognozi: 1 daqiqalik faylni 1440 ga ko'paytirish
ls -l --block-size=M /var/log/app/app.json
```

Arxitektor qarori: qatorlar sonini kamaytirish eng arzon optimizatsiya. Bitta so'rovga bitta yakuniy access log qatori va biznes holat o'zgarishi uchun 1-2 qator kifoya. Qolgan diagnostikani span attributlariga ko'chiring: span vaqt va ierarxiyani o'zi beradi. Ingest va indeks narxi ajratilgan tizimda esa hajmli, lekin kam qidiriladigan oqimni arzon arxivga yuborish mumkin.

## 30.5 Micrometer bilan metrika: counter, gauge, timer, distribution summary

Micrometer to'rt asosiy turni beradi va har biri o'z ishi uchun. Counter faqat o'sadi va "necha marta" savoliga javob beradi. Gauge joriy qiymatni o'qiydi va faqat shu daqiqadagi holatni biladi, tarixni emas. Timer vaqt taqsimotini yig'adi. DistributionSummary vaqt bo'lmagan kattalikni (buyurtma summasi, batch o'lchami) taqsimot sifatida yig'adi.

```java
@Component
public class OrderMetrics {
    private final Counter rejected;
    private final Timer checkout;
    private final DistributionSummary basketSize;

    public OrderMetrics(MeterRegistry registry, OrderQueue queue) {
        this.rejected = Counter.builder("orders.rejected")
                .description("rad etilgan buyurtmalar")
                .tag("reason", "out_of_stock")   // tag qiymati chekli ro'yxatdan
                .register(registry);
        this.checkout = Timer.builder("orders.checkout")
                .publishPercentileHistogram()    // server tomonda quantile hisoblash uchun
                .register(registry);
        this.basketSize = DistributionSummary.builder("orders.basket.items")
                .register(registry);
        // Gauge o'lchanadigan obyektga weak reference oladi, shuning uchun
        // obyekt tirik qolishiga ishonch kerak, aks holda qiymat NaN bo'ladi
        Gauge.builder("orders.queue.depth", queue, OrderQueue::size).register(registry);
    }

    public void recordCheckout(Duration d, int items) {
        checkout.record(d);
        basketSize.record(items);
    }
}
```

Ikki xato tez-tez uchraydi. Birinchisi: `registry.counter(...)` ni har so'rovda chaqirish, bu map lookup va tag massivini qayta yaratish degani; meter ni bir marta oling. Ikkinchisi: percentile ni client tomonda hisoblash. Bitta instansda hisoblangan p99 ni boshqa instans p99 bilan qo'shib bo'lmaydi, o'rtachasi esa ma'nosiz son. Agregatlanadigan p99 uchun histogram bucket lari chiqarilishi shart.

Bu yerda `publishPercentileHistogram` ning narxini bilib qo'yish kerak, chunki u bir qatorga o'xshaydi, lekin time series sonini ko'paytiradi. Micrometer hujjatiga ko'ra default generator 276 ta bucket beradi, Micrometer esa timer ni 1 millisekunddan 1 daqiqagacha oraliqqa qisadi va natijada **har bir timer o'lchami uchun 73 ta histogram bucket** chiqadi. Demak 73 ni teglar kombinatsiyasi soniga ko'paytirish kerak: 20 ta endpoint va 5 ta status bilan bu bitta timer dan 7300 ga yaqin qator. Bucket sonini `minimumExpectedValue` va `maximumExpectedValue` boshqaradi, ular bir vaqtda HdrHistogram strukturasining aniqligi va xotirasini ham belgilaydi.

Ikki muhim shart ham bor. Birinchi: `publishPercentileHistogram` faqat agregatlanadigan percentile ni qo'llaydigan tizimda ishlaydi, ya'ni Prometheus, Atlas va Wavefront da; boshqa tizimga histogram umuman yuborilmaydi va bu qator jim ta'sirsiz qoladi. Ikkinchi: hujjat percentile ni umumiy kutubxonada yoqmaslikni maslahat beradi, chunki u dependency sifatida kirgan hamma ilovaga qo'shimcha time series olib keladi; to'g'ri joy ilovaning o'zida meter filter bilan tanlangan timer larga yoqish. SLO bucket lari esa `serviceLevelObjectives` bilan qo'shiladi va histogram ni qo'llamaydigan tizimda faqat shu bucket lar chiqadi.

## 30.6 Kardinallik portlashi: metrika tegiga foydalanuvchi id qo'yish xatosi

Metrika narxi va xotirasi tag qiymatlarining kombinatsiyalari soniga, ya'ni vaqt qatorlari soniga bog'liq. `http.server.requests` da uri (50 variant), method (5), status (8), outcome (5) bo'lsa, taxminan 10 000 qator. Unga `userId` qo'shsangiz va 100 ming aktiv foydalanuvchi bo'lsa, qator soni millionlarga chiqadi. Prometheus da bitta aktiv qator taxminan 1-3 KB RAM yeydi, demak 5 million qator taxminan 10 GB. Scrape sekinlashadi, keyin OOM keladi. Histogram yoqilgan Timer esa bitta tag kombinatsiyasiga o'nlab bucket qatori qo'shadi, shuning uchun portlash tezligi yana bir necha barobar oshadi.

```java
// XATO: path variable va foydalanuvchi id teg qiymatiga tushadi
// registry.timer("orders.fetch", "path", "/orders/" + id, "user", userId)

// TO'G'RI: shablonli URI, chekli natija, id esa log yoki span attributiga
@Bean
MeterFilter limitTagValues() {
    return MeterFilter.maximumAllowableTags(
            "orders.fetch", "customerSegment", 20, MeterFilter.deny());
}

@Bean
MeterFilter dropNoisyMeters() {
    // tanib bo'lmaydigan URI uchun 404 oqimi alohida qator yaratmasin
    return MeterFilter.deny(id ->
            "http.server.requests".equals(id.getName())
            && "NOT_FOUND".equals(id.getTag("outcome")));
}
```

Qoida: tag qiymati oldindan ma'lum, chekli va 50 dan oshmaydigan to'plam bo'lsin. Id, email, URL, xato matni, SQL matni tegga tushmaydi, ularning joyi span attributi va log maydoni. Kardinallik yangi relizda qaytib keladi, shuning uchun qator sonining o'zini metrika qilib alert qo'ying.

## 30.7 Qaysi metrikalar majburiy: so'rov soni, xato ulushi, kechikish taqsimoti, resurs

Har bir servis uchun to'rtta oila shart. Birinchi: so'rov tezligi (rps), ikkinchi: xato ulushi (5xx va biznes xatolar alohida), uchinchi: kechikish taqsimoti (p50, p95, p99, albatta histogram orqali), to'rtinchi: to'yinganlik (connection pool band ulushi, thread pool navbati, heap, GC pauzasi, disk). Qolganlari foydali, lekin bu to'rttasi bo'lmasa incident vaqtida ko'r bo'lib qolasiz.

Java va Spring da alohida e'tibor beriladigan nuqtalar: `hikaricp.connections.pending` va `hikaricp.connections.usage`, chunki kechikishning yarmi shu yerdan chiqadi; `jvm.gc.pause`; `executor.queued`; Kafka consumer lag; va tashqi chaqiruvlar uchun `http.client.requests`. O'rtacha qiymatga qaramang: 2000 rps da p99 degani sekundda 20 ta foydalanuvchi, ya'ni kuniga yuz minglab yomon tajriba.

| Mavzu | Oddiy yondashuv | Arxitektor yondashuvi |
|---|---|---|
| Log formati | Matn ichiga qiymat yopishtirilgan `info` | Barqaror xabar, alohida maydonlar, kelishilgan sxema |
| Log hajmi | "Kerak bo'lsa yozamiz", hajm o'lchanmaydi | Bitta so'rovga qator soni byudjeti va o'lchovi bor |
| Percentile | Instans ichida p99 hisoblanadi | Histogram bucket, agregatsiya backend da |
| Metrika teglari | Nima qo'l kelsa teg qilinadi | Chekli lug'at, `MeterFilter` bilan cheklov |
| Trace | Hammasi yoki hech nima | Head sampling past, xatoli trace tail bilan to'liq |
| Alert | CPU 80 foizdan oshdi | Xato byudjeti yonish tezligi oshdi |
| Dashboard | 40 ta panel, hammasi bir xil muhim | Birinchi ekranda to'rtta signal, qolgani drill-down |
| Incident tahlili | Log ni ko'z bilan o'qish | Trace id bo'ylab uchala manbani bir zumda bog'lash |
| Yangi servis | Kuzatuv keyin qo'shiladi | Kuzatuv shablonda, ishga tushirish shartida |

## 30.8 OpenTelemetry: trace, span, kontekst tarqalishi va namuna olish (sampling)

Trace bitta so'rovning butun yo'li, span esa shu yo'ldagi bitta ish bo'lagi: HTTP handler, SQL so'rov, Kafka publish. Span ichida id, parent id, boshlanish vaqti, davomiylik va attributlar bor. Kontekst servislar orasida W3C `traceparent` header i, Kafka da message header orqali uzatiladi. Spring Boot 3.x da bu Micrometer Observation API va OTel bridge orqali ishlaydi: bitta `Observation` dan metrika ham, span ham chiqadi.

Eng ko'p yo'qotish nuqtalari: async chegaralari, message broker (header ko'chirilmaydi) va reverse proxy (header o'chirib tashlaydi). Trace servis chegarasida uzilsa, ikkita alohida trace ko'rinadi va kechikish bog'lanmaydi. Buni integratsiya testida tekshirib qo'ying: kirishga `traceparent` berilib, chiqishda bir xil trace id kutiladi.

```java
// Biznes operatsiyasini bitta Observation bilan o'rash:
// bundan ham span, ham `orders.checkout` metrikasi chiqadi
Observation.createNotStarted("orders.checkout", observationRegistry)
    .lowCardinalityKeyValue("channel", "mobile")      // metrikaga ham tushadi
    .highCardinalityKeyValue("orderId", orderId)      // faqat span attributi
    .observe(() -> checkoutService.run(orderId));
```

Kam kardinallikli key metrikaga ham, span ga ham tushadi, yuqori kardinallikli key faqat span ga. Shu ajratim kardinallik portlashining asosiy to'sig'i, va u kod yozilayotganda hal bo'ladi, keyin emas.

## 30.9 Namuna olish darajasi tanlash va xatoli so'rovlarni to'liq saqlash

Har bir so'rovni trace qilish qimmat: 2000 rps va so'rovga 15 span bo'lsa, bu 30 000 span/s. Shuning uchun head sampling qo'yiladi, masalan 5 foiz. Muammo shundaki, head sampling qarorni so'rov boshida qabul qiladi va o'sha paytda so'rov xato bilan tugashini bilmaydi. Natijada incident paytida aynan kerakli trace topilmaydi.

To'g'ri yechim ikki qatlamli. Birinchi qatlam: head sampling `parentbased_traceidratio` bilan, past darajada, lekin butun trace bo'ylab izchil (parent qarori bolalarga o'tadi, aks holda yarim trace chiqadi). Ikkinchi qatlam: Collector da tail sampling, u butun trace yig'ilgandan keyin qaror qiladi va xatoli hamda sekin trace larni to'liq saqlaydi.

```yaml
# OTel Collector: xato va sekin trace to'liq, qolgani 5 foiz
processors:
  tail_sampling:
    decision_wait: 10s          # trace yig'ilishini kutish
    num_traces: 100000
    policies:
      - name: xatolar
        type: status_code
        status_code: { status_codes: [ERROR] }
      - name: sekinlar
        type: latency
        latency: { threshold_ms: 1500 }
      - name: qolgani
        type: probabilistic
        probabilistic: { sampling_percentage: 5 }
```

Muhim nuans: tail sampling faqat o'ziga yetib kelgan trace dan tanlaydi. Agar ilovada 5 foiz head sampling bo'lsa, Collector qolgan 95 foizni ko'rmaydi. Shuning uchun tail sampling ishlatilsa, ilovada sampling 100 foiz qo'yiladi va filtr Collector ga ko'chadi. Bu ilovada taxminan bir necha foiz CPU va tarmoq qo'shadi, bu ongli to'lanadigan narx.

## 30.10 Ogohlantirish (alert) dizayni: belgiga emas, foydalanuvchi ta'siriga qarab

"CPU 80 foizdan oshdi" alert i emas, bu kuzatuv. U kechasi odamni uyg'otadi, lekin foydalanuvchi hech narsa sezmagan bo'lishi mumkin. Alert faqat foydalanuvchi ta'siri bor va odam aralashuvi kerak bo'lgan holatda chiqishi kerak. Shuning uchun alert SLO ga va xato byudjeti yonish tezligiga quriladi: "oxirgi 1 soatda xato byudjetining shunday ulushi yondi" degan shart ham tez, ham shovqinsiz ishlaydi.

```yaml
groups:
  - name: checkout-slo
    rules:
      # 99.9 foiz SLO: 1 soatda 14.4 barobar yonish tezligi tez buzilish belgisi
      - alert: CheckoutErrorBudgetFastBurn
        expr: |
          (sum(rate(http_server_requests_seconds_count{uri="/api/checkout",status=~"5.."}[1h]))
           / sum(rate(http_server_requests_seconds_count{uri="/api/checkout"}[1h]))) > 14.4 * 0.001
          and
          (sum(rate(http_server_requests_seconds_count{uri="/api/checkout",status=~"5.."}[5m]))
           / sum(rate(http_server_requests_seconds_count{uri="/api/checkout"}[5m]))) > 14.4 * 0.001
        for: 2m
        labels: { severity: page }
        annotations:
          summary: "Checkout xato byudjeti tez yonmoqda"
          runbook: "https://wiki/runbooks/checkout-5xx"
```

Ikki oynali shart (1 soat va 5 daqiqa) bitta sakrashdan kelgan yolg'on alert ni kesadi va muammo tuzatilganda alert ni tez yopadi. Har bir sahifalaydigan alert da runbook havolasi bo'lishi shart: nima qilish kerakligini aytmagan alert shunchaki xavotir. Resurs metrikalari dashboard va ticket darajasida qoladi, faqat disk to'lishi kabi qaytarib bo'lmaydigan holat istisno.

| Tuzoq | Nega og'riydi | Yechim |
|---|---|---|
| Metrika tegida id yoki URL | Qator soni millionga chiqib backend yiqiladi | Shablonli URI, `MeterFilter` bilan cheklov, id span ga |
| Client tomonda p99 | Instanslar bo'ylab agregatlanmaydi | `publishPercentileHistogram`, quantile backend da |
| Head sampling 5 foiz | Xatoli so'rovning trace i yo'q | Ilovada 100 foiz, Collector da tail sampling |
| MDC async da yo'qoladi | Log da trace id bo'sh, bog'lash uzilgan | Executor ni context propagation bilan o'rash |
| Entity ni log ga berish | Lazy yuklash, ortiqcha SQL, PII oqishi | Faqat kerakli maydonlar, maskirovka appender da |
| Kutilgan rad etish ERROR da | Alert shovqinga aylanadi va e'tibordan qoladi | Biznes rad etish INFO yoki WARN, metrikada alohida |
| CPU va heap bo'yicha alert | Kechasi uyg'otadi, ta'sir yo'q | SLO va burn rate alert, resurs faqat dashboard da |
| Histogram hamma Timer da | Bucket qatorlari ko'payib xotira yeydi | Faqat SLO li operatsiyalarda, chegaralar bilan |

## 30.11 Dashboard qanday bo'lishi kerak: birinchi ekranda nima turadi

Dashboard incident paytida 30 sekundda javob berishi kerak. Demak birinchi ekranda scroll qilmasdan faqat to'rtta narsa turadi: so'rov tezligi, xato ulushi, kechikish p95 va p99, to'yinganlik. Yonida reliz versiyasi va deploy belgilari bo'lsin, chunki buzilishlarning katta qismi deploy bilan ustma-ust tushadi. Qolgani pastda yoki drill-down dashboard da.

Amaliy talablar: har bir panelda o'q birligi va SLO chizig'i ko'rinsin, vaqt oynasi hamma panel uchun bitta bo'lsin, instans bo'yicha ajratish faqat kerakli panelda qolsin. 40 panelli dashboard hech kimga tegishli bo'lmaydi va eskiradi, shuning uchun har bir dashboard egasi bo'lishi kerak.

## 30.12 Spring Boot Actuator va Micrometer sozlash amaliyoti

Defaultlardan boshlash kerak, chunki ular ko'pincha yetarli himoyani beradi va sozlash aynan shuni buzadi. Spring Boot da HTTP va JMX orqali default holda **faqat `health` endpoint i** ochiq, `health` ning detallari esa default `never`, ya'ni ko'rinmaydi. Ya'ni xavf Actuator ning o'zida emas, `management.endpoints.web.exposure.include` ga qo'shilgan har bir qatorda. Hujjat buni to'g'ridan-to'g'ri aytadi: ro'yxatni kengaytirishdan oldin ochilgan endpoint da maxfiy ma'lumot yo'qligiga ishonch qilish, yoki uni firewall yoki Spring Security ortiga qo'yish kerak. `show-details` ning `when-authorized` qiymatida esa bitta nozik joy bor: endpoint ga rol berilmagan bo'lsa (default holat), **har qanday autentifikatsiyadan o'tgan** foydalanuvchi authorized hisoblanadi; rolni cheklash uchun `management.endpoint.health.roles` yoziladi.

Actuator ni ochish oson, xatolar ham oson. Birinchi qoida: management port ni ilova portidan ajratib tashqaridan yopish. Ikkinchi: `env`, `heapdump`, `threaddump`, `loggers` himoyalanmagan holda ochilmasin. Uchinchi: health detallari faqat autentifikatsiyadan o'tganlarga ko'rinsin, chunki u ichki infratuzilma xaritasini oshkor qiladi. To'rtinchi: liveness va readiness probe larni ajratish, aks holda baza vaqtincha yo'qolganda Kubernetes pod ni bejiz o'ldiradi.

```yaml
management:
  server.port: 9090                 # ilova porti bilan aralashmasin
  endpoints.web.exposure.include: health,info,prometheus,metrics
  endpoint.health:
    show-details: when-authorized
    probes.enabled: true            # liveness va readiness alohida
  metrics:
    tags: { application: payment-service, env: prod }
    distribution:
      percentiles-histogram:
        http.server.requests: true  # faqat kerakli metrikada
      slo:
        http.server.requests: 100ms,300ms,1s,3s
      maximum-expected-value:
        http.server.requests: 5s    # bucket sonini cheklaydi
  observations.key-values.region: eu-central-1
  tracing.sampling.probability: 1.0 # filtr Collector da tail sampling bilan
otel.exporter.otlp.endpoint: http://otel-collector:4317
```

`percentiles-histogram` ni global yoqmang: har bir histogram li Timer o'nlab bucket qatori yaratadi, `maximum-expected-value` qo'yilmasa diapazon keraksiz keng bo'ladi. Histogram faqat SLO bor operatsiyada yig'ilsin. Nihoyat, kuzatuv kodi o'zi ham taxminan bir necha foiz CPU va qo'shimcha allokatsiya yeydi, shuning uchun uni yuklama testida o'lchash kerak. Testlash qo'llanmasidagi performance test bo'limi shu o'lchov uchun asos beradi, dizayn [patternlar hujjatidagi](../patterns/README.md) observability patternlari esa strukturaviy tomonni yopadi.

JMX alohida eslatmani talab qiladi. Spring Boot Actuator metrikalarini JMX orqali ham chiqarishi mumkin va JVM ning o'z MBean lari (heap, thread, class loading, GC) shu yo'l bilan ko'rinadi. Lekin JMX ni tashqi monitoring kanali sifatida tanlash eskirgan yondashuv: u RMI portini talab qiladi, konteyner va NAT ortida sozlash og'ir, va u pull modelida ishlaydi. Qoida: ishlab chiqarishda metrika Micrometer orqali chiqadi, JMX esa lokal diagnostika uchun qoladi (`jconsole`, `jcmd`, JFR), ya'ni tashqi portga ochilmaydi.

## 30.13 Statik chegara va anomaliya aniqlash: alert qoidasi qanday shaklda bo'ladi

30.10 alert nimaga qo'yilishini aytdi: belgiga emas, foydalanuvchi ta'siriga. Bu bo'lim keyingi savolga javob beradi, ya'ni qoidaning o'zi qanday shaklda yoziladi. Orosz ikki keng tarqalgan yo'lni sanaydi: chegarani odam qo'lda belgilaydi, yoki tizim odatdagi trafik shaklini o'zi o'rganib undan chetga chiqishni topadi (Gergely Orosz, *The Software Engineer's Guidebook*, 1-nashr, Pragmatic Engineer, 2023, 24-bob, 348-bet).

Statik chegarada qoida qo'lda yoziladi. Orosz ikki misol beradi: "bu metrika 60 sekunddan ortiq nolga tushsa, alert chiqar" va "odatdagi qiymat daqiqasiga 100 bo'lgan joyda metrika 500 dan oshsa, alert chiqar" (24-bob, 348-bet). Kuchli tomoni uchta: yozish oson, alert nega ishga tushgani darhol tushunarli, va chegarani keyin sozlash oson. Zaif tomoni ham aniq: qaysi chegara to'g'ri ekanini oldindan aytish qiyin, va amalda statik chegara ko'pincha uzilishdan keyin, aynan o'sha uzilishni ushlashi mumkin bo'lgan joyga qo'yiladi (24-bob, 348-bet).

Anomaliya aniqlashda chegara umuman yozilmaydi: tizim metrikaning odatdagi shaklini o'rganadi va sozlanadigan yagona kirish qiymati sezgirlik bo'ladi (24-bob, 348-349-bet). U statik chegara ko'rmaydigan tebranishni ushlaydi, kutilmagan trafik ko'tarilishi va tushishida ham ishlaydi, va tayyor framework bo'lsa ko'p metrikaga arzonga yoyiladi. Zaif tomoni Orosz ning o'z tajribasida ko'ringan: Uber da to'lov tizimiga anomaliya aniqlashni birinchi marta yoqqanda, tizim o'rganayotgan va sozlanayotgan dastlabki bir necha hafta ichida shunchalik ko'p alert kelganki, jonli alertlarni o'chirib qo'yishga to'g'ri kelgan (24-bob, 349-bet). Teskari xato ham bor: sozlash yetarli bo'lmasa tizim haqiqiy anomaliyaga sezgir bo'lmay qoladi, hafta kunlari bo'yicha farq qiladigan odatdagi trafikni hisobga olishi kerak, va Black Friday kabi oldindan ma'lum ko'tarilish yoki tushishda ham alert chiqaradi (24-bob, 349-bet).

| Mezon | Statik chegara | Anomaliya aniqlash |
|---|---|---|
| Qoidani yozish | odam raqam qo'yadi | sezgirlik sozlanadi, chegara yo'q |
| Nega ishga tushdi | darhol ko'rinadi | izohlash qiyinroq |
| Kutilmagan shakl | sezmaydi | sezadi |
| Oldindan ma'lum cho'qqi | tinch turadi | soxta alert beradi |
| Ko'p metrikaga yoyish | har biriga alohida mehnat | framework bo'lsa arzon |
| Tipik xato | chegara uzilishdan keyin qo'yiladi | sozlanmagan davrda shovqin |

Tanlov ikkisidan biri emas. Orosz amaliy yechimni aralashma deb ataydi: ko'p metrika uchun anomaliya aniqlash, kutilayotgan trafik ko'tarilishi va tushishi uchun hamda asosiy metrikaning nolga tushishini ushlash uchun statik chegara (24-bob, 349-bet). Nolga tushish aynan statik chegaraga mos keladi, chunki u shaklga emas, mavjudlik faktiga qaraydi.

```yaml
# Statik chegara kuchli bo'ladigan holat: metrika butunlay nolga tushdi.
# Oyna uzunligi Orosz misolidagi 60 sekund, chegara esa o'z o'lchovingizdan.
groups:
  - name: payment-static
    rules:
      - alert: PaymentTrafficDroppedToZero
        expr: sum(rate(http_server_requests_seconds_count{uri="/api/payments"}[1m])) == 0
        for: 1m                      # 60 sekund davom etsa alert
        labels: { severity: page }
        annotations:
          summary: "To'lov API ga so'rov umuman kelmayapti"
          runbook_url: "https://wiki.internal/runbook/payment-no-traffic"
```

30.10 dagi burn rate alert shakli bo'yicha statik chegara: raqam SLO dan chiqadi, shuning uchun u "o'ylab topilgan chegara" emas. Anomaliya aniqlash esa shu qatorga qo'shimcha bo'lib keladi, o'rniga emas.

## 30.14 Amalda qo'llash

- [ ] Bitta tipik so'rovga nechta log qatori yozilayotganini sanang va uni 3 qatorgacha qisqartirish rejasini tuzing.
- [ ] Log maydon nomlari lug'atini yozib, strukturali formatni (ECS yoki o'z sxemangiz) hamma servisga bir xil qo'ying.
- [ ] Async chegarasida trace id MDC da saqlanishini integratsiya testi bilan tekshirib qo'ying.
- [ ] Prometheus da eng ko'p qator yaratadigan 10 ta metrikani chiqarib, id va URL li teglarni `MeterFilter` bilan kesib tashlang.
- [ ] Client tomonda hisoblanadigan percentile larni olib tashlab, SLO li operatsiyalarda histogram va `maximum-expected-value` qo'ying.
- [ ] Ilovada sampling ni 100 foizga olib chiqib, xato va 1.5 sekunddan sekin trace larni to'liq saqlaydigan tail sampling ni Collector da yoqing.
- [ ] Resurs bo'yicha sahifalaydigan alert larni o'chirib, ularning o'rniga burn rate alert va har biriga runbook havolasi qo'shing.
- [ ] Har bir servis dashboard ining birinchi ekranini to'rtta signalga qisqartirib, egasini belgilang.

## Manbalar

- Craig Walls, *Spring in Action* 6th, 15, 16, 17-boblar - Actuator, Spring Boot Admin va JMX
- [Micrometer, Histograms and percentiles](https://raw.githubusercontent.com/micrometer-metrics/micrometer-docs/06f377a95db21894939c6fff39441fe608e804a2/src/docs/concepts/histogram-quantiles.adoc) - client-side percentile ning agregatlanmasligi, default 276 bucket va timer uchun 73 bucket, `minimumExpectedValue`/`maximumExpectedValue`, `serviceLevelObjectives`, kutubxonada yoqmaslik maslahati
- [Micrometer, Gauges](https://raw.githubusercontent.com/micrometer-metrics/micrometer-docs/06f377a95db21894939c6fff39441fe608e804a2/src/docs/concepts/gauges.adoc) - gauge ning weak reference ushlashi va obyekt GC bo'lganda NaN qaytarishi
- [Spring Boot 4.0, Actuator Endpoints](https://raw.githubusercontent.com/spring-projects/spring-boot/v4.0.0/documentation/spring-boot-docs/src/docs/antora/modules/reference/pages/actuator/endpoints.adoc) - default holda faqat `health` ochiqligi, `show-details` default `never`, rol berilmaganda har qanday autentifikatsiyalangan foydalanuvchining authorized bo'lishi
- [OpenTelemetry, Tracing API](https://raw.githubusercontent.com/open-telemetry/opentelemetry-specification/bb85bf44e2c032d9958c10b78dcb88cf36e40917/specification/trace/api.md) - span, kontekst va atribut modeli
- [OpenTelemetry, SDK](https://raw.githubusercontent.com/open-telemetry/opentelemetry-specification/bb85bf44e2c032d9958c10b78dcb88cf36e40917/specification/trace/sdk.md) - sampler turlari va `ParentBased` qarorining trace bo'ylab izchilligi
- Gergely Orosz, *The Software Engineer's Guidebook*, 1-nashr, Pragmatic Engineer, 2023, 24-bob (348-349-bet) - statik chegara va anomaliya aniqlashning kuchli va zaif tomonlari, statik chegara uzilishdan keyin qo'yilishi, Uber to'lov tizimida anomaliya aniqlash sozlanmagan davrda alertlarni o'chirishga majbur qilgani, ikkisining amaliy aralashmasi

---

[&larr; 29. Kafka operatsion haqiqati: partition, lag, rebalance, idempotentlik](29-kafka-operatsion-haqiqati-partition-lag.md) · [Mundarija](README.md) · [31. Deployment haqiqati: konteyner, cgroup, JVM va probe &rarr;](31-deployment-haqiqati-konteyner-cgroup-jvm-va.md)
