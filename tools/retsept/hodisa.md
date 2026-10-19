# hodisa

Minimal shakl (patterns 8.26, code-review 11.5):

```java
public record OrderPlaced(long orderId) {}

@Transactional
public void place(Order order) {
    orders.save(order);
    events.publishEvent(new OrderPlaced(order.getId()));
}

@TransactionalEventListener(phase = TransactionPhase.AFTER_COMMIT)
void onPlaced(OrderPlaced e) {
    mailer.sendConfirmation(e.orderId());
}
```

Allaqachon bor, yozmang:
- `ApplicationEvent` dan meros o'rniga oddiy record va `publishEvent(Object)` (patterns 8.26)
- Qo'lda `TransactionSynchronizationManager.registerSynchronization` o'rniga `@TransactionalEventListener(phase = AFTER_COMMIT)` (architect 19.8)
- Qo'lda listener ro'yxati va notify sikli o'rniga `ApplicationEventPublisher` va `@EventListener` (patterns 5.20)
- Yo'qolmasligi kerak bo'lgan event uchun o'z retry jadvali o'rniga Spring Modulith event publication registry (patterns 8.26)

Tuzoqlar:
- Oddiy `@EventListener` sinxron va publisher tranzaksiyasi ichida ishlaydi: tashqi chaqiruv tranzaksiyani cho'zadi, istisno uni rollback qiladi; yon ta'sir `AFTER_COMMIT` da bo'lsin (architect 15.10)
- `AFTER_COMMIT` listener tranzaksiyasiz ishlaydi va DB yozuvi jim yo'qoladi; yozish kerak bo'lsa `@Transactional(propagation = REQUIRES_NEW)` qo'shing, istisnoni o'zingiz log qiling (architect 19.8)
- Eventga entity qo'yilsa boshqa thread da `LazyInitializationException` yoki eskirgan holat chiqadi; faqat id va immutable qiymat uzating (code-review 11.5)
