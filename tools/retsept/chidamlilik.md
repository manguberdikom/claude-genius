# chidamlilik

Minimal shakl (code-review 10.5, 22.3):

```java
@CircuitBreaker(name = "payment", fallbackMethod = "chargeLater")
public PaymentResult charge(ChargeCommand cmd) {
    return gateway.charge(cmd, cmd.idempotencyKey());
}

private PaymentResult chargeLater(ChargeCommand cmd, CallNotPermittedException e) {
    outbox.enqueueRetry(cmd);
    return PaymentResult.pending(cmd.idempotencyKey());
}
// yaml instances.payment.ignore-exceptions: com.acme.payment.CardDeclined
```

Allaqachon bor, yozmang:
- retry sikli va `Thread.sleep` o'rniga `@Retryable` aniq ro'yxat bilan: Spring 7 yadrosida `maxRetries, multiplier, jitter, includes = {...}` (patterns 17.40), spring-retry da `retryFor = {...}, noRetryFor, maxAttempts, backoff = @Backoff(random = true)` (code-review 22.2)
- qo'lda semafor o'rniga `@ConcurrencyLimit(n)` (patterns 17.40)
- qo'lda xato hisoblagich o'rniga `resilience4j.circuitbreaker.instances.<nom>` yaml, umumiy qiymat `configs`/`baseConfig` da, holat `/actuator/circuitbreakers` da (patterns 17.39)

Tuzoqlar:
- fallback `Exception` olsa `ignore-exceptions` dagi biznes xatosi ham `pending` bo'ladi: parametr `CallNotPermittedException` (code-review 10.5, 22.3)
- `Exception` ni yoki kalitsiz POST ni retry qilish rad etishni takrorlaydi va ikki marta to'lov beradi (code-review 22.2)
- `this.charge()` proxyni chetlab o'tadi: chaqiruv boshqa bean orqali kelsin (patterns 17.39)
- har qatlamda jitter'siz retry bo'ron beradi: retry bitta qatlamda, jitter va circuit breaker bilan (patterns 17.42)
- chaqiruvchi `@Transactional` ichida bo'lsa retry har urinish va backoff da connection va qulfni ushlaydi: chaqiruvchini `grep -rn '\.<metod>(' src/main` bilan toping; tashqi chaqiruv tranzaksiyadan tashqarida yoki `Ochiq qaror` (code-review 19.9, 19.2)
