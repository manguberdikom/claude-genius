# tranzaksiya

Minimal shakl (code-review 19.1, architect 19.8):

```java
@Service
class OrderService {
    private final OrderRepository orders;
    private final ApplicationEventPublisher events;
    OrderService(OrderRepository orders, ApplicationEventPublisher events) {
        this.orders = orders;
        this.events = events;
    }

    @Transactional
    public void confirm(long id) {
        orders.findById(id).orElseThrow().confirm();
        events.publishEvent(new OrderConfirmed(id));
    }
}
```

Allaqachon bor, yozmang:
- Commit dan keyingi ishni metod ichida qilish o'rniga `@TransactionalEventListener(phase = AFTER_COMMIT)` (architect 19.8)
- Bir metodda bir nechta tranzaksiya yoki retry uchun `TransactionTemplate.executeWithoutResult` (architect 19.11)
- O'qish metodida bekor dirty check o'rniga `@Transactional(readOnly = true)` (architect 19.5)
- Bitta repository chaqiruvini (`save`) o'rash o'rniga uning o'z tranzaksiyasi; qadam ikki baza amaliga o'sgandagina `TransactionTemplate` (code-review 19.1)

Tuzoqlar:
- `this.x()` yoki `private` metod proxy dan o'tmaydi va tranzaksiya jim yo'qoladi; metodni boshqa bean ga oling yoki `TransactionTemplate` (architect 19.6)
- Tranzaksiya ichidagi HTTP yoki to'lov chaqiruvi connection va qulfni ushlaydi; qisqa tranzaksiya, tashqi chaqiruv, qisqa tranzaksiya qilib bo'ling (code-review 19.2)
- Boot 3 da `TransactionTemplate.execute` natijasi `@Nullable`, tekshiruvsiz `java:S2259`; natija kerak bo'lmasa `executeWithoutResult`, kerak bo'lsa `Objects.requireNonNull(r, "xabar")`. Boot 4 da nullability callback turidan (sonarqube 25.2, architect 13.10)
- Checked istisno standartda commit qiladi; rollback kerak bo'lsa `rollbackFor = Exception.class` yoki domen istisnosini `RuntimeException` dan oling (architect 19.4)
