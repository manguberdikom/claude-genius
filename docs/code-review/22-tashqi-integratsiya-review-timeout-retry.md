<!-- doc: code-review | chapter: 22 | part: IV. Spring kodini review qilish -->

[Barcha hujjatlar](../../README.md) / [Kod review](README.md)

> Holat: AI yozgan, inson tekshirmagan.

# 22. Tashqi integratsiya review: timeout, retry, broker (Outbound Integration)

<details>
<summary>Bu bobdagi 9 bo'lim</summary>

- [22.1 HTTP mijoz: timeout eng birinchi savol](#221-http-mijoz-timeout-eng-birinchi-savol)
- [22.2 Retry: qachon zarar keltiradi](#222-retry-qachon-zarar-keltiradi)
- [22.3 Circuit breaker va bulkhead](#223-circuit-breaker-va-bulkhead)
- [22.4 WebClient va reaktiv kod aralashuvi](#224-webclient-va-reaktiv-kod-aralashuvi)
- [22.5 Kafka va xabar brokerlari review](#225-kafka-va-xabar-brokerlari-review)
- [22.6 Xabar sxemasi va moslik](#226-xabar-sxemasi-va-moslik)
- [22.7 Tashqi ma'lumotga ishonmaslik](#227-tashqi-malumotga-ishonmaslik)
- [22.8 Review checklisti: tashqi integratsiya](#228-review-checklisti-tashqi-integratsiya)
- [22.9 Amalda qo'llash](#229-amalda-qollash)

</details>


Har bir tashqi chaqiruv - tizimingizga kirgan begona nosozlik manbasi. Review ning vazifasi: shu nosozlik sizning ilovangizni o'ziga tortib ketmasligini tekshirish. Bitta sozlanmagan timeout butun ilovani to'xtatishi mumkin, va bu diffda bir qator ko'rinadi.

## 22.1 HTTP mijoz: timeout eng birinchi savol

```java
// Naqsh: timeout sozlanmagan mijoz.
@Bean
RestClient paymentClient() {
    return RestClient.create("https://api.provider.io");   // timeout yo'q!
}
// Standart holatda JDK HttpClient da ulanish timeout i cheksiz bo'lishi
// mumkin. Provayder TCP ulanishni qabul qilib, javob bermasa, thread
// abadiy kutadi. 200 thread li ilovada 200 sekin so'rov butun ilovani
// to'xtatadi - klassik kaskadli nosozlik.

// To'g'ri: har bir mijoz uchun aniq timeout va o'lchov.
@Bean
RestClient paymentClient(RestClient.Builder builder,
                         PaymentProperties props,
                         MeterRegistry registry) {
    ClientHttpRequestFactorySettings settings = ClientHttpRequestFactorySettings.DEFAULTS
        .withConnectTimeout(Duration.ofMillis(500))     // ulanish: tez xato
        .withReadTimeout(props.timeout());              // o'qish: byudjetdan

    return builder
        .baseUrl(props.baseUrl().toString())
        .requestFactory(ClientHttpRequestFactories.get(settings))
        .requestInterceptor(new MetricsInterceptor(registry, "payment"))
        .defaultStatusHandler(HttpStatusCode::isError, (req, res) -> {
            // Xato javobini domen istisnosiga aylantirish (7.6).
            throw PaymentGatewayException.from(res.getStatusCode(), res.getBody());
        })
        .build();
}
```

Review savollari har bir yangi HTTP mijoz uchun: ulanish timeout i, o'qish timeout i, umumiy byudjet, retry siyosati, circuit breaker, metrika, va xato javobining aylantirilishi.

## 22.2 Retry: qachon zarar keltiradi

```java
// Xato 1: hamma narsani retry qilish.
@Retryable(retryFor = Exception.class, maxAttempts = 5)      // juda keng
public PaymentResult charge(ChargeCommand cmd) { ... }
// Oqibati: karta rad etilgan (biznes javobi) ham besh marta takrorlanadi.
// Provayder tomonda bu "shubhali xulq" sifatida belgilanadi va hisob
// bloklanishi mumkin. Foydalanuvchiga besh SMS keladi.

// Xato 2: idempotent bo'lmagan operatsiyani retry qilish.
// POST /payments ni timeout dan keyin qayta yuborish: birinchi so'rov
// provayderga yetib borgan bo'lishi mumkin. Natija - ikki marta to'lov.
// Qoida: retry faqat idempotentlik kaliti bilan birga (10.9).

// To'g'ri: tor ro'yxat, jitter bilan backoff, idempotentlik kaliti.
@Retryable(
    retryFor = { PaymentGatewayUnavailable.class, SocketTimeoutException.class },
    noRetryFor = { CardDeclined.class, InsufficientFunds.class, InvalidCard.class },
    maxAttempts = 3,
    backoff = @Backoff(delay = 200, multiplier = 2, random = true))
public PaymentResult charge(ChargeCommand cmd) {
    return gateway.charge(cmd, cmd.idempotencyKey());   // kalit har urinishda bir xil
}
```

| Retry qilinadi | Retry qilinmaydi |
| --- | --- |
| Ulanish xatosi, timeout | 4xx (so'rov xatosi) |
| 502, 503, 504 | 401, 403 (huquq) |
| `Retry-After` bilan 429 | 422 (biznes rad etishi) |
| Deadlock, serializatsiya xatosi (DB) | Validatsiya xatosi |
| Optimistik qulf konflikti | Ma'lumot topilmadi |

## 22.3 Circuit breaker va bulkhead

Retry nosozlikni kuchaytiradi: tashqi servis yiqilganda uch barobar ko'p so'rov yuboriladi. Shu sababli retry yolg'iz emas, circuit breaker bilan birga keladi.

```yaml
resilience4j:
  circuitbreaker:
    instances:
      payment:
        sliding-window-type: COUNT_BASED
        sliding-window-size: 50
        minimum-number-of-calls: 20          # kam chaqiruvda qaror qabul qilmaslik
        failure-rate-threshold: 50           # 50% xato - ochiladi
        slow-call-duration-threshold: 1s
        slow-call-rate-threshold: 50         # sekin javoblar ham nosozlik
        wait-duration-in-open-state: 30s
        permitted-number-of-calls-in-half-open-state: 5
        record-exceptions:
          - com.acme.payment.PaymentGatewayUnavailable
        ignore-exceptions:
          - com.acme.payment.CardDeclined    # biznes javobi nosozlik emas
  bulkhead:
    instances:
      payment:
        max-concurrent-calls: 20             # bu integratsiya butun pool ni yemasin
        max-wait-duration: 100ms
  timelimiter:
    instances:
      payment:
        timeout-duration: 2s
        cancel-running-future: true
```

Review savollari: `ignore-exceptions` da biznes xatolari bormi (bo'lishi kerak), `minimum-number-of-calls` juda kichik emasmi (aks holda ikki xatodan keyin ochiladi), circuit ochilganda nima bo'ladi (fallback, navbat, yoki foydalanuvchiga xato), va bu holat o'lchanadimi.

```java
// Fallback - review ning asosiy diqqati: u nima qiladi?
@CircuitBreaker(name = "payment", fallbackMethod = "chargeFallback")
public PaymentResult charge(ChargeCommand cmd) { return gateway.charge(cmd); }

// Yomon fallback: muvaffaqiyat qaytaradi.
private PaymentResult chargeFallback(ChargeCommand cmd, Exception e) {
    return PaymentResult.approved();            // blocker: pul olinmagan!
}
// To'g'ri fallback: holatni rost ko'rsatadi va keyin davom etish yo'li beradi.
private PaymentResult chargeFallback(ChargeCommand cmd, Exception e) {
    meter.counter("payment.fallback").increment();
    outbox.enqueueRetry(cmd);                   // keyin qayta urinamiz
    return PaymentResult.pending(cmd.idempotencyKey());
}
```

## 22.4 WebClient va reaktiv kod aralashuvi

```java
// Naqsh: reaktiv mijoz blokirovka qilib ishlatilgan.
public Rate rate(String currency) {
    return webClient.get().uri("/rates/{c}", currency)
                    .retrieve().bodyToMono(Rate.class)
                    .block();                   // event loop threadida bo'lsa - deadlock
}
// Review izohi: `block()` ni reaktiv thread da chaqirish ilovani
// qotirishi mumkin. Agar reaktiv stek kerak bo'lmasa, RestClient
// ishlatish kerak - u sinxron va shu maqsad uchun.
// Qo'shimcha: block() da timeout yo'q - cheksiz kutish.
.block(Duration.ofSeconds(2));                  // minimal tuzatish
```

## 22.5 Kafka va xabar brokerlari review

```java
// Iste'molchi tomonidagi review savollari - har biri alohida xavf.
@KafkaListener(topics = "payments", groupId = "order-service")
public void onPayment(PaymentEvent event, Acknowledgment ack) {
    orders.applyPayment(event.orderId(), event.amount());
    ack.acknowledge();
}
```

| Savol | Nega muhim |
| --- | --- |
| Xabar ikki marta kelsa nima bo'ladi | Kafka "kamida bir marta" yetkazadi - idempotentlik majburiy |
| Xabar tartibi muhimmi | Tartib faqat bitta partition ichida kafolatlanadi; kalit to'g'ri tanlanganmi |
| Xato bo'lsa nima bo'ladi | Cheksiz qayta urinish (poison pill) yoki DLQ |
| `ack` qachon chaqiriladi | Ishdan oldin bo'lsa - xabar yo'qoladi |
| Tranzaksiya bilan munosabat | DB commit va `ack` atomik emas |
| Sxema o'zgarsa | Eski iste'molchi yangi xabarni o'qiy oladimi |
| Lag o'lchanadimi | Iste'molchi orqada qolsa, qanday bilamiz |
| Qayta ishlash qancha vaqt oladi | `max.poll.interval.ms` dan oshsa, guruhdan chiqariladi |

```yaml
# Review da tekshiriladigan minimal sozlamalar.
spring:
  kafka:
    consumer:
      enable-auto-commit: false            # qo'lda ack: ish bajarilgandan keyin
      isolation-level: read_committed
      max-poll-records: 50                 # bir martada ko'p olmaslik
      properties:
        max.poll.interval.ms: 300000       # ishlov vaqtidan katta bo'lsin
    producer:
      acks: all                            # yetkazish kafolati
      enable-idempotence: true             # dublikatsiz yozish
      properties:
        max.in.flight.requests.per.connection: 5
    listener:
      ack-mode: manual_immediate
```

```java
// DLQ va cheklangan qayta urinish: poison pill butun iste'molchini to'xtatmasin.
@Bean
DefaultErrorHandler errorHandler(KafkaTemplate<String, Object> template) {
    // 3 urinishdan keyin xabarni .DLT topikiga yuborish.
    DeadLetterPublishingRecoverer recoverer = new DeadLetterPublishingRecoverer(template);
    ExponentialBackOffWithMaxRetries backoff = new ExponentialBackOffWithMaxRetries(3);
    backoff.setInitialInterval(500);
    backoff.setMultiplier(2.0);
    DefaultErrorHandler handler = new DefaultErrorHandler(recoverer, backoff);
    // Deserializatsiya xatosi - qayta urinish ma'nosiz, darhol DLQ ga.
    handler.addNotRetryableExceptions(DeserializationException.class,
                                      MessageConversionException.class);
    return handler;
}
// Review savoli: DLQ ni kim o'qiydi va u haqida alert bormi? O'qilmaydigan
// DLQ - ma'lumotni jim yo'qotishning chiroyli shakli.
```

## 22.6 Xabar sxemasi va moslik

```java
// Review talabi: event sxemasi o'zgarishi orqaga mos bo'lishi kerak.
// Mos o'zgarishlar: ixtiyoriy maydon qo'shish, standart qiymat bilan.
public record OrderPlaced(
        UUID orderId,
        BigDecimal total,
        String currency,
        @Nullable String promoCode) { }          // yangi, ixtiyoriy - mos

// Mos bo'lmagan o'zgarishlar ([37-bob](37-api-moslik-va-breaking-change-review.md) ro'yxatiga qarang):
// - maydon nomini o'zgartirish
// - maydon turini o'zgartirish
// - majburiy maydon qo'shish
// - maydon olib tashlash
// - enum qiymatini olib tashlash

// Review savoli: iste'molchilar kim? Ular yangilanmasdan eski xabarni
// o'qiy oladimi, va yangi xabarni ham? Schema registry bormi?
```

## 22.7 Tashqi ma'lumotga ishonmaslik

```java
// Naqsh: tashqi javob tekshirilmasdan domenga kiradi.
PaymentResponse r = client.get().retrieve().body(PaymentResponse.class);
order.applyPayment(r.amount(), r.currency());    // amount null yoki manfiy bo'lishi mumkin

// To'g'ri: tashqi javob ham ishonilmaydigan kirish - adapter ichida tekshiriladi.
PaymentResponse r = client.get().retrieve().body(PaymentResponse.class);
if (r == null || r.amount() == null || r.amount().signum() < 0) {
    throw new InvalidGatewayResponse("amount: " + (r == null ? "null" : r.amount()));
}
Money amount = new Money(r.amount(), Currency.getInstance(r.currency()));
order.applyPayment(amount);
```

Review da bu naqsh ko'pincha e'tibordan chetda qoladi, chunki "o'z provayderimiz" ishonchli deb hisoblanadi. Amalda esa tashqi API versiyasini o'zgartirishi, xato holatda `null` qaytarishi yoki boshqa valyutada javob berishi mumkin.

## 22.8 Review checklisti: tashqi integratsiya

| Savol | Nega |
| --- | --- |
| Ulanish va o'qish timeout i bormi | Thread va pool to'lishi |
| Retry ro'yxati tor va idempotentlik bormi | Dublikat va retry bo'roni |
| Backoff da jitter bormi | Sinxron urinishlar to'lqini |
| Circuit breaker va bulkhead bormi | Kaskadli nosozlik |
| Fallback rost holatni qaytaradimi | Yolg'on muvaffaqiyat |
| Tashqi javob tekshiriladimi | Buzilgan ma'lumot domenda |
| Vendor istisnolari domen istisnolariga aylanadimi | Oqib chiqadigan abstraksiya |
| Metrika va trace bormi | Ko'r integratsiya |
| Kafka da idempotentlik va DLQ bormi | Yo'qolgan yoki takrorlangan xabar |
| `ack` ish bajarilgandan keyinmi | Yo'qolgan xabar |
| Sxema o'zgarishi orqaga mosmi | Iste'molchilar sinishi |
| Secret va kalitlar muhitdanmi | Oshkor qilish |

## 22.9 Amalda qo'llash

- [ ] Barcha HTTP mijoz bean larini sanab, ulanish va o'qish timeout i sozlanmaganlarini aniqlang va tuzating.
- [ ] Har bir integratsiya uchun umumiy byudjet jadvalini tuzing (urinishlar x timeout) va yuqori qatlam chegarasiga sig'ishini tasdiqlang.
- [ ] `@Retryable` va Resilience4j `retry-exceptions` ro'yxatlarida biznes istisnolari yo'qligini tekshiring.
- [ ] Barcha retry siyosatlarida jitter (`random = true` yoki `enable-randomized-wait`) yoqilganini tasdiqlang.
- [ ] Fallback metodlarini ko'rib, yolg'on muvaffaqiyat qaytaradiganlarini tuzating.
- [ ] Vendor istisnolarini domen istisnolariga aylantiradigan adapter qatlamini qo'shing.
- [ ] Kafka iste'molchilarida `enable-auto-commit: false`, DLQ va deserializatsiya xatosi uchun `addNotRetryableExceptions` borligini tekshiring.
- [ ] DLQ uchun alert va uni o'qish jarayonini belgilang.
- [ ] Consumer lag va circuit breaker holati uchun dashboard paneli va alert qo'shing.

---

[&larr; 21. Konfiguratsiya, profil va feature flag review](21-konfiguratsiya-profil-va-feature-flag-review.md) · [Mundarija](README.md) · [23. JPA va Hibernate review &rarr;](23-jpa-va-hibernate-review.md)
