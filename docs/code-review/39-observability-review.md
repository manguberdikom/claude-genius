<!-- doc: code-review | chapter: 39 | part: VIII. Kesishgan sifat -->

[Barcha hujjatlar](../../README.md) / [Kod review](README.md)

> Holat: AI yozgan, inson tekshirmagan.

# 39. Observability review (Observability)

<details>
<summary>Bu bobdagi 9 bo'lim</summary>

- [39.1 Uch signal va ularning vazifasi](#391-uch-signal-va-ularning-vazifasi)
- [39.2 Yangi kod uchun minimal signal to'plami](#392-yangi-kod-uchun-minimal-signal-toplami)
- [39.3 Nimani o'lchash kerak: RED va USE](#393-nimani-olchash-kerak-red-va-use)
- [39.4 Log sifati](#394-log-sifati)
- [39.5 Korrelyatsiya va trace](#395-korrelyatsiya-va-trace)
- [39.6 Health check va probe lar](#396-health-check-va-probe-lar)
- [39.7 Alert sifati](#397-alert-sifati)
- [39.8 Review checklisti: observability](#398-review-checklisti-observability)
- [39.9 Amalda qo'llash](#399-amalda-qollash)

</details>


Kod prodda ishlaganda uning holati faqat chiqargan signallar orqali ko'rinadi. Shu sababli har bir yangi kod yo'li uchun savol beriladi: bu yo'l xato ishlasa, qanday bilamiz. Agar javob "mijoz shikoyat qilganda" bo'lsa, kod to'liq emas. Observability review ning afzalligi shundaki, u incident paytida eng ko'p qaytim beradi va eng arzon qo'shiladi.

## 39.1 Uch signal va ularning vazifasi

| Signal | Savolga javob beradi | Qachon qo'shiladi |
| --- | --- | --- |
| Metrika | Nima sodir bo'layapti, qancha, qanchalik tez | Har bir muhim operatsiya |
| Log | Nega shunday bo'ldi (bitta holat uchun) | Xato va muhim qarorlar |
| Trace | Vaqt qayerga ketdi (bitta so'rov bo'ylab) | Ko'p komponentli oqim |

Review da eng ko'p uchraydigan xato - ikkisini aralashtirish: metrikada bo'lishi kerak narsa logga yoziladi (har so'rov uchun `log.info`), yoki logda bo'lishi kerak kontekst metrikaga tegga aylanadi (kardinallik portlashi, 16.7).

## 39.2 Yangi kod uchun minimal signal to'plami

```java
// Review talabi: har bir muhim operatsiya uchun uchlik.
@Service
public class PaymentService {

    private final Counter attempts;
    private final Counter failures;
    private final Timer duration;

    public PaymentService(MeterRegistry registry) {
        this.attempts = Counter.builder("payments.attempt")
            .description("to'lov urinishlari soni")
            .register(registry);
        this.failures = Counter.builder("payments.failed")
            .register(registry);
        this.duration = Timer.builder("payments.duration")
            .publishPercentiles(0.5, 0.95, 0.99)
            .register(registry);
    }

    public PaymentResult charge(ChargeCommand cmd) {
        attempts.increment();
        Timer.Sample sample = Timer.start();
        try {
            PaymentResult result = gateway.charge(cmd);
            // Natija turi teg sifatida: rad etishlar alohida ko'rinadi.
            registry.counter("payments.result", "outcome", result.kind().name()).increment();
            return result;
        } catch (Exception e) {
            failures.increment();
            // Log: bitta holat uchun kontekst. Korrelyatsiya ID bilan.
            log.error("to'lov yiqildi orderId={} idemKey={} provider={}",
                      cmd.orderId(), cmd.idempotencyKey(), cmd.provider(), e);
            throw e;
        } finally {
            sample.stop(duration);
        }
    }
}
```

Diqqat: `@Timed` annotatsiyasi va `@Observed` (Micrometer Observation) bu kodni qisqartiradi. Review da muhimi mexanizm emas, uchta savolga javob borligi: nechta urinish, nechtasi yiqildi, qancha vaqt oldi.

## 39.3 Nimani o'lchash kerak: RED va USE

| Model | Nimani o'lchaydi | Qachon |
| --- | --- | --- |
| RED (Rate, Errors, Duration) | So'rovlar oqimi | Endpoint, integratsiya, iste'molchi |
| USE (Utilization, Saturation, Errors) | Resurslar | Pool, navbat, thread, disk |
| Biznes metrikalari | Natija | Buyurtmalar, to'lovlar, konversiya |

```java
// Review da eng ko'p esdan chiqadigan: to'yinganlik (saturation).
// So'rovlar tez ishlayapti, lekin navbat o'syapti - bu yiqilishdan oldingi holat.
@Bean
MeterBinder queueMetrics(OutboxRepository outbox, ThreadPoolTaskExecutor executor) {
    return registry -> {
        // Outbox navbati: kutayotgan xabarlar va eng qadimgi yoshi (27.9).
        Gauge.builder("outbox.pending", outbox, OutboxRepository::countPending)
             .register(registry);
        Gauge.builder("outbox.oldest.seconds", outbox,
                      r -> r.oldestPendingAgeSeconds()).register(registry);
        // Thread pool to'yinganligi.
        Gauge.builder("executor.queue.size", executor,
                      e -> e.getThreadPoolExecutor().getQueue().size()).register(registry);
    };
}
// Biznes metrikasi: eng qimmatli signal.
// Agar to'lovlar soni oyning shu kunidagi o'rtachadan 40 foiz past bo'lsa,
// bu texnik metrikalar yashil bo'lsa ham incident.
```

## 39.4 Log sifati

```java
// Daraja 1: kontekstsiz log - incidentda foydasiz.
log.error("Xatolik yuz berdi");
log.error("Xato: " + e.getMessage());            // stack trace yo'q

// Daraja 2: istisno bor, kontekst yo'q.
log.error("To'lov yiqildi", e);                  // qaysi to'lov?

// Daraja 3: kontekst va istisno bor.
log.error("to'lov yiqildi orderId={} amount={} provider={}",
          orderId, amount, provider, e);

// Daraja 4: strukturali log - qidirish va agregatsiya mumkin.
// (logstash-logback-encoder bilan JSON)
log.atError()
   .setMessage("to'lov yiqildi")
   .addKeyValue("orderId", orderId)
   .addKeyValue("amount", amount.toPlainString())
   .addKeyValue("provider", provider)
   .setCause(e)
   .log();
// Natija: {"message":"to'lov yiqildi","orderId":"...","amount":"100000",
//          "provider":"payme","traceId":"...","stack_trace":"..."}
// Bu logda `orderId` bo'yicha qidirish va `provider` bo'yicha guruhlash mumkin.
```

| Log darajasi | Qachon | Review diqqati |
| --- | --- | --- |
| `ERROR` | Odam aralashuvi kerak | Alert ga ulanganmi; shovqin bo'lmasin |
| `WARN` | Kutilmagan, lekin tiklandi | Retry, fallback, degradatsiya |
| `INFO` | Muhim biznes hodisasi | Har so'rov uchun emas |
| `DEBUG` | Diagnostika | Prodda o'chirilgan |
| `TRACE` | Batafsil | Faqat lokalda |

```java
// Review izohi: xato darajasining noto'g'ri tanlanishi.
// Biznes rad etishi ERROR emas:
log.error("Karta rad etildi: {}", orderId);      // kuniga 5000 marta -> alert shovqini
log.info("karta rad etildi orderId={} reason={}", orderId, reason);   // to'g'ri
// Lekin: rad etishlar nisbati keskin oshsa - bu metrika va alert ishi,
// log emas.
```

## 39.5 Korrelyatsiya va trace

```java
// Review talabi: har log satrida so'rovni aniqlash imkoni bo'lishi kerak.
// Spring Boot 3 + Micrometer Tracing avtomatik traceId va spanId qo'shadi.
```

```yaml
management:
  tracing:
    sampling:
      probability: 0.1                 # 10% - prod uchun maqbul
  otlp:
    tracing:
      # Boot 3.x kaliti; Boot 4 da: management.opentelemetry.tracing.export.otlp.endpoint
      endpoint: http://collector:4318/v1/traces
logging:
  pattern:
    level: "%5p [${spring.application.name},%X{traceId:-},%X{spanId:-}]"
```

```java
// Asinxron chegaralarda kontekst ko'chishi - eng ko'p buziladigan joy.
// @Async, ExecutorService va Kafka listener larda traceId yo'qoladi.
@Bean
TaskDecorator contextPropagatingDecorator() {
    // Micrometer Context Propagation: MDC va trace kontekstini ko'chiradi.
    return new ContextPropagatingTaskDecorator();
}
@Bean
ThreadPoolTaskExecutor orderExecutor(TaskDecorator decorator) {
    ThreadPoolTaskExecutor ex = new ThreadPoolTaskExecutor();
    ex.setTaskDecorator(decorator);              // aks holda traceId yo'qoladi
    ...
}
// Review savoli: async ishda xato bo'lsa, uni asl so'rov bilan
// bog'lash mumkinmi? Javob "yo'q" bo'lsa, incident tahlili juda qiyin.

// Kafka da: traceId xabar header ida ko'chiriladi.
// Review savoli: produser va iste'molchi loglarini bir-biriga bog'lash
// mumkinmi?
```

## 39.6 Health check va probe lar

```java
// Naqsh: yuzaki health check - har doim "UP".
@GetMapping("/health")
public String health() { return "OK"; }
// Bu Kubernetes ga "ishlayapman" deydi, lekin DB yiqilgan bo'lsa ham.

// To'g'ri: bog'liqliklar holati bilan, lekin probe larni ajratib.
```

```yaml
management:
  endpoint:
    health:
      probes:
        enabled: true                  # /health/liveness va /health/readiness
      group:
        liveness:
          include: livenessState       # FAQAT "protsess tirikmi"
        readiness:
          include: readinessState,db   # "trafik qabul qila olamanmi"
      show-details: when-authorized
```

Review da asosiy farq: `liveness` ga tashqi bog'liqliklarni QO'SHMASLIK kerak. Agar DB vaqtincha yiqilsa va liveness unga bog'liq bo'lsa, Kubernetes barcha podlarni qayta ishga tushiradi va tiklanishni qiyinlashtiradi (kaskadli nosozlik). `readiness` esa bog'liqliklarni hisobga olishi mumkin - pod trafikdan chiqadi, lekin o'ldirilmaydi.

```java
// Maxsus health indicator: review da uning narxi tekshiriladi.
@Component
public class PaymentGatewayHealth implements HealthIndicator {
    @Override
    public Health health() {
        // DIQQAT: bu metod har health so'rovida chaqiriladi (Kubernetes
        // har 10 sekundda). Tashqi servisga so'rov yuborish - yuk.
        // To'g'ri: oxirgi muvaffaqiyatli chaqiruv vaqtiga qarash.
        Instant last = gateway.lastSuccessfulCall();
        if (last == null || last.isBefore(Instant.now().minusSeconds(120))) {
            return Health.down().withDetail("lastSuccess", last).build();
        }
        return Health.up().build();
    }
}
```

## 39.7 Alert sifati

Review da yangi alert ham ko'riladi, chunki yomon alert jamoani charchatadi va yaxshi alertlar ham e'tibordan qoladi.

| Alert mezoni | Yaxshi alert | Yomon alert |
| --- | --- | --- |
| Harakatga chaqiradi | "To'lov xatolari 5% dan oshdi" | "CPU 80%" |
| Foydalanuvchiga ta'siri bor | SLO buzilishi | Ichki texnik holat |
| Aniq egasi bor | Jamoa belgilangan | "Kimdir ko'rsin" |
| Runbook bor | Nima qilish yozilgan | Faqat ogohlantirish |
| Shovqin emas | Haftada 0-2 marta | Kuniga 20 marta |
| Oldini olish mumkin | Navbat o'syapti (saturation) | Tizim allaqachon yiqilgan |

```yaml
# Prometheus alert: review da shu shakl talab qilinadi.
groups:
  - name: payments
    rules:
      - alert: PaymentFailureRateHigh
        # Nisbat, absolyut son emas: yuk o'zgarishiga chidamli.
        expr: |
          sum(rate(payments_result_total{outcome="FAILED"}[5m]))
            / sum(rate(payments_result_total[5m])) > 0.05
        for: 10m                       # qisqa to'lqinlarda uyg'otmaydi
        labels:
          severity: critical
          team: payments               # egasi aniq
        annotations:
          summary: "To'lov xatolari 5% dan oshdi ({{ $value | humanizePercentage }})"
          runbook: "https://wiki/runbooks/payment-failures"
          dashboard: "https://grafana/d/payments"

      - alert: OutboxBacklogGrowing
        # Saturation alerti: yiqilishdan OLDIN ogohlantiradi.
        expr: outbox_oldest_seconds > 300
        for: 5m
        labels: { severity: warning, team: orders }
        annotations:
          summary: "Outbox da 5 daqiqadan ortiq kutayotgan xabar bor"
          runbook: "https://wiki/runbooks/outbox"
```

## 39.8 Review checklisti: observability

| Savol | Nega |
| --- | --- |
| Yangi operatsiya uchun urinish/xato/vaqt metrikasi bormi | Ko'r kod |
| Xato logida kontekst va istisno bormi | Diagnostika |
| Log darajasi to'g'ri tanlanganmi | Alert shovqini |
| Har so'rov uchun `INFO` log yozilmaydimi | Disk va narx |
| Metrika teglarida yuqori kardinallik yo'qmi | Xotira va narx |
| traceId async chegarasida ko'chadimi | Incident tahlili |
| Yangi tashqi integratsiya o'lchanadimi | Ko'r integratsiya |
| Navbat va pool to'yinganligi o'lchanadimi | Oldini olish |
| Biznes metrikasi bormi | Texnik yashil, biznes qizil |
| `liveness` tashqi bog'liqliklarga bog'lanmaganmi | Kaskadli qayta ishga tushish |
| Yangi alert harakatga chaqiradimi va runbook bormi | Shovqin |
| Maxfiy ma'lumot logga tushmaydimi | Oqish (32.1) |

## 39.9 Amalda qo'llash

- [ ] Har bir muhim operatsiya uchun urinish, natija (teg bilan) va davomiylik metrikalarini qo'shishni review talabiga aylantiring.
- [ ] Strukturali (JSON) logga o'tib, `traceId` va `spanId` ni log patterniga kiriting.
- [ ] `ContextPropagatingTaskDecorator` ni barcha executor larga qo'shib, async da traceId yo'qolmasligini tasdiqlang.
- [ ] Barcha navbatlar (outbox, thread pool, Kafka lag) uchun to'yinganlik metrikalarini qo'shing.
- [ ] `liveness` guruhidan tashqi bog'liqliklarni olib tashlang va `readiness` ga ko'chiring.
- [ ] Health indicator larning narxini tekshirib, tashqi so'rov yuboradiganlarini keshlangan holatga o'tkazing.
- [ ] Mavjud alertlarni ko'rib chiqib, harakatga chaqirmaydiganlarini o'chiring yoki `warning` ga tushiring.
- [ ] Har bir `critical` alert uchun egasi va runbook havolasi borligini tasdiqlang.
- [ ] Kamida uchta biznes metrikasi (buyurtmalar, to'lovlar, ro'yxatdan o'tish) va ularga anomaliya alertini qo'shing.

---

[&larr; 38. Performance review diffdan](38-performance-review-diffdan.md) · [Mundarija](README.md) · [40. Review jarayonini qurish &rarr;](40-review-jarayonini-qurish.md)
