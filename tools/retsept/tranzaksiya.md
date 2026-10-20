# tranzaksiya

Minimal shakl (code-review 19.1):

```java
@Service
class OrderService {
    private final OrderRepository orders;
    OrderService(OrderRepository orders) { this.orders = orders; }

    @Transactional
    public void confirm(long id) {
        orders.findById(id).orElseThrow().confirm();
    }
}
```

Allaqachon bor, yozmang:
- Commit dan keyingi ish: `@TransactionalEventListener(phase = AFTER_COMMIT)`, tuzoqlari hodisa kartasida (architect 19.8)
- O'qish metodida bekor dirty check o'rniga `@Transactional(readOnly = true)` (architect 19.5)
- Bitta `save` ni o'rash o'rniga uning o'z tranzaksiyasi (tashqi chaqiruvdan keyin ham); `TransactionTemplate` faqat chunk, retry yoki bir qadamda ikki yozuv uchun (code-review 19.1, architect 19.11)

Tuzoqlar:
- `this.x()` yoki `private` metod proxy dan o'tmaydi, tranzaksiya jim yo'qoladi: boshqa bean yoki `TransactionTemplate` (architect 19.6)
- Tranzaksiya ichida HTTP, to'lov chaqiruvi connection va qulfni ushlaydi: qisqa tranzaksiya, tashqi chaqiruv, qisqa tranzaksiya; to'lov o'tib keyingi `save` yiqilsa pul yechilgan, holat eski: `Ochiq qaror`, reconcile (code-review 19.2, patterns 20.26)
- `@Retryable` va `@Transactional` bitta metodda ishlamaydi: retry tashqarida (architect 19.11)
- Ichki `REQUIRED` metod istisnosi `catch` qilinsa commit `UnexpectedRollbackException`: kechirimli qism `REQUIRES_NEW` yoki tranzaksiyadan tashqarida (architect 19.4)
- Boot 3 da `TransactionTemplate.execute` natijasi `@Nullable` (`java:S2259`): natijasiz `executeWithoutResult`, natijali `Objects.requireNonNull(r, "xabar")`; Boot 4 da nullability callback turidan (sonarqube 25.2, architect 13.10)
- Checked istisno standartda commit qiladi: `rollbackFor = Exception.class` yoki domen istisnosi `RuntimeException` dan (architect 19.4)
