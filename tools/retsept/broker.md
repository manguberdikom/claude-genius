# broker

Minimal shakl, `message_id` biznes kaliti (`payment_id`) va PRIMARY KEY (architect 29.7):

```java
@KafkaListener(topics = "payments", groupId = "order-service")
@Transactional
public void onPayment(PaymentCaptured event) {
    int inserted = jdbc.update("""
            INSERT INTO processed_message (message_id) VALUES (?)
            ON CONFLICT DO NOTHING""", event.paymentId());
    if (inserted == 1) {
        orders.applyPayment(event.orderId(), event.amount());
    }
}
```

Allaqachon bor, yozmang:
- qo'lda retry sikli va DLT ga yuborish o'rniga `DefaultErrorHandler` + `ExponentialBackOffWithMaxRetries` + `DeadLetterPublishingRecoverer` (architect 29.12)
- retry topic va ularning listenerlari o'rniga `@RetryableTopic` + `@DltHandler` (patterns 16.35)
- buzilgan payload uchun try/catch o'rniga `ErrorHandlingDeserializer` (architect 29.12)
- qo'lda offset commit o'rniga `enable-auto-commit: false` va `ack-mode: batch` (architect 29.6)

Tuzoqlar:
- DB commit dan keyin `KafkaTemplate.send` qilish hodisani yo'qotadi, uni shu tranzaksiyada outbox jadvaliga yozing (architect 29.11)
- doimiy xatoni (buzilgan JSON, validatsiya) qayta urinish partitionni to'xtatadi, `addNotRetryableExceptions` bilan darhol DLT ga yuboring (architect 29.9)
- `ack.acknowledge()` ni ishdan oldin chaqirish xabarni yo'qotadi: avval ishlov, keyin `ack` (code-review 22.5)
