<!-- doc: code-review | chapter: 19 | part: IV. Spring kodini review qilish -->

[Barcha hujjatlar](../../README.md) / [Kod review](README.md)

# 19. Tranzaksiya chegarasi review (Transaction Boundaries)

<details>
<summary>Bu bobdagi 11 bo'lim</summary>

- [19.1 Chegara qayerda turishi kerak](#191-chegara-qayerda-turishi-kerak)
- [19.2 Tranzaksiya ichida tashqi chaqiruv - eng xavfli naqsh](#192-tranzaksiya-ichida-tashqi-chaqiruv---eng-xavfli-naqsh)
- [19.3 readOnly: nima beradi, nima bermaydi](#193-readonly-nima-beradi-nima-bermaydi)
- [19.4 Propagation: diffdagi ma'nosi](#194-propagation-diffdagi-manosi)
- [19.5 Rollback qoidalari](#195-rollback-qoidalari)
- [19.6 Tranzaksiya uzunligi va PostgreSQL ga ta'siri](#196-tranzaksiya-uzunligi-va-postgresql-ga-tasiri)
- [19.7 Commit dan keyin bajarilishi kerak bo'lgan ish](#197-commit-dan-keyin-bajarilishi-kerak-bolgan-ish)
- [19.8 OSIV va lazy loading](#198-osiv-va-lazy-loading)
- [19.9 Tranzaksiya, kesh, event va async aralashuvi](#199-tranzaksiya-kesh-event-va-async-aralashuvi)
- [19.10 Review checklisti: tranzaksiyalar](#1910-review-checklisti-tranzaksiyalar)
- [19.11 Amalda qo'llash](#1911-amalda-qollash)

</details>


Tranzaksiya chegarasi - Spring loyihasida eng ko'p xato qilinadigan dizayn qarori, va eng qimmat oqibat beradigan joy: noto'g'ri chegara ma'lumot nomuvofiqligi, uzoq qulflar yoki butun ilovaning to'xtashiga olib keladi. Bu bob chegarani diffdan baholashni beradi. Izolyatsiya darajalari va PostgreSQL MVCC mexanikasi [27-bobda](27-izolyatsiya-poyga-holatlari-va-xabar.md) va [Arxitektor miyasi](../architect/README.md) da.

## 19.1 Chegara qayerda turishi kerak

Qoida: tranzaksiya biznes operatsiyasining chegarasi bo'ladi - bitta foydalanuvchi niyatining chegarasi. Amalda bu application servis metodi.

| Joy | Chegara bo'lishi | Sabab |
| --- | --- | --- |
| Controller | Yo'q | Web detallari tranzaksiyani uzaytiradi, OSIV muammolari |
| Application servis | Ha | Biznes operatsiyasi chegarasi |
| Domen servis | Odatda yo'q | Domen tranzaksiyani bilmasligi kerak |
| Repository | Yo'q (faqat o'z ichida) | Juda mayda chegara, invariant himoyalanmaydi |
| `@Scheduled` metod | Ha, lekin bo'laklab | Katta tranzaksiya qulflarni to'playdi |
| Kafka listener | Ha | Xabarni qayta ishlash chegarasi |

```java
// Chegara juda mayda: har repository chaqiruvi alohida tranzaksiyada.
public void transfer(AccountId from, AccountId to, Money amount) {
    accounts.debit(from, amount);      // tranzaksiya 1 - commit bo'ldi
    accounts.credit(to, amount);       // tranzaksiya 2 - yiqilsa, pul yo'qoladi
}
// Review izohi (blocker): bu ikki operatsiya atomik bo'lishi shart.
// Ikkinchisi yiqilsa, birinchisi qaytmaydi va hisobdan pul ketadi.

// Chegara juda keng: butun import bitta tranzaksiyada.
@Transactional
public void importAll(List<Row> rows) {     // 100 000 qator
    rows.forEach(this::importOne);
}
// Review izohlari: (1) bitta noto'g'ri qator butun importni qaytaradi;
// (2) 100k qator uchun qulflar tranzaksiya oxirigacha ushlanadi;
// (3) Hibernate birinchi daraja keshi 100k obyektni ushlaydi - OOM;
// (4) PostgreSQL da uzoq tranzaksiya VACUUM ni bloklaydi va jadval
//     bo'rtadi (bloat).
```

## 19.2 Tranzaksiya ichida tashqi chaqiruv - eng xavfli naqsh

Bu naqsh shu hujjatda bir necha marta uchraydi, chunki u review da eng ko'p topiladigan va eng qimmat xato.

```java
@Transactional
public void confirmOrder(OrderId id) {
    Order order = orders.findById(id).orElseThrow();
    order.confirm();                                  // DB qulfi olindi
    PaymentResult result = paymentGateway.capture(order.paymentId());  // tashqi!
    if (result.isDeclined()) throw new PaymentDeclined();
    notifications.send(order.customerEmail());        // yana tashqi!
}
```

Review izohi to'rt oqibatni sanab o'tadi:

1. DB ulanishi tashqi servis javobini kutib turadi. Pool 20 ta bo'lsa, 20 parallel so'rov butun ilovani to'xtatadi.
2. Qator qulfi shu vaqt ushlanadi: boshqa so'rovlar shu buyurtmaga tegishi kutadi.
3. To'lov o'tib, keyin commit yiqilsa - pul olingan, buyurtma tasdiqlanmagan. Teskarisi ham mumkin.
4. Tashqi servis timeout i DB tranzaksiya timeout idan katta bo'lsa, tranzaksiya avval uziladi va holat noaniq bo'ladi.

```java
// Yechim: tranzaksiyani uchga bo'lish - tashqi chaqiruv tashqarida.
public void confirmOrder(OrderId id) {
    // 1-tranzaksiya: niyatni qayd qilish (qisqa).
    Order order = orderTx.markConfirming(id);

    // Tranzaksiyadan tashqarida: tashqi chaqiruv, timeout bilan.
    PaymentResult result = paymentGateway.capture(order.paymentId());

    // 2-tranzaksiya: natijani yozish (qisqa).
    orderTx.applyPaymentResult(id, result);
    // Xabar yuborish outbox orqali (10.8) - commit bilan atomik.
}
```

## 19.3 readOnly: nima beradi, nima bermaydi

```java
@Transactional(readOnly = true)
public List<OrderView> recent(CustomerId id) { ... }
```

`readOnly = true` nima beradi: Hibernate flush ni o'tkazib yuboradi va dirty checking qilmaydi (tezlik), ba'zi marshrutlovchilar so'rovni replikaga yuboradi, va PostgreSQL da tranzaksiya `READ ONLY` sifatida belgilanadi.

Nima bermaydi: u yozuvni taqiqlashning ishonchli usuli emas - JDBC orqali to'g'ridan-to'g'ri yozuv o'tishi mumkin, va `readOnly` bilan belgilangan metod ichidan boshqa yozadigan metod chaqirilsa, xulq propagation ga bog'liq.

Review savollari: o'qish metodlarida `readOnly` qo'yilganmi (katta o'qishlarda sezilarli farq beradi), va `readOnly` metod ichida yozuv yo'qligi tasdiqlanganmi.

## 19.4 Propagation: diffdagi ma'nosi

| Propagation | Ma'nosi | Review diqqati |
| --- | --- | --- |
| `REQUIRED` (standart) | Bor bo'lsa qo'shiladi, yo'q bo'lsa boshlaydi | Ichkarida istisno tashlansa, tashqi tranzaksiya ham rollback-only bo'ladi |
| `REQUIRES_NEW` | Har doim yangi tranzaksiya | Ikki ulanish egallanadi; proxy orqali chaqirilishi shart |
| `NESTED` | Savepoint | PostgreSQL da savepoint narxi bor; JPA bilan cheklovlar |
| `SUPPORTS` | Bor bo'lsa qo'shiladi, yo'q bo'lsa tranzaksiyasiz | Noaniq xulq: ikki rejimda ishlaydi |
| `NOT_SUPPORTED` | Tranzaksiyani to'xtatib turadi | Uzoq o'qish uchun foydali |
| `MANDATORY` | Tranzaksiya bo'lishi shart | Domen qoidasini majburlash uchun yaxshi |
| `NEVER` | Tranzaksiya bo'lmasligi shart | Kam ishlatiladi |

```java
// Eng ko'p uchraydigan yashirin xato: REQUIRED ichida ushlangan istisno.
@Transactional
public ImportReport importAll(List<Row> rows) {
    List<String> errors = new ArrayList<>();
    for (Row row : rows) {
        try {
            importOne(row);                 // @Transactional(REQUIRED) - bir xil tranzaksiya
        } catch (DataIntegrityViolationException e) {
            errors.add(row.id());           // istisno ushlandi, davom etamiz
        }
    }
    return new ImportReport(errors);        // bu nuqtada tranzaksiya rollback-only!
}
// Oqibati: metod oxirida commit urinilganda
// UnexpectedRollbackException: "Transaction silently rolled back" -
// hamma narsa qaytadi, hatto muvaffaqiyatli qatorlar ham.
// Sabab: ichki tranzaksiya REQUIRED bo'lgani uchun bir xil fizik
// tranzaksiyada ishlaydi va istisno uni rollback-only deb belgilaydi.
// Yechim: REQUIRES_NEW (alohida bean orqali) yoki qatorlarni oldin
// validatsiya qilib, keyin yozish.
```

## 19.5 Rollback qoidalari

```java
// Standart xulq: RuntimeException va Error - rollback;
// checked Exception - COMMIT (ko'pchilik buni bilmaydi).
@Transactional
public void process() throws IOException {
    orders.save(order);
    throw new IOException("fayl yozilmadi");     // tranzaksiya COMMIT bo'ladi!
}
// Review izohi: checked istisno tashlanganda Spring standart holatda
// rollback qilmaydi. Buyurtma saqlanadi, lekin fayl yozilmagan - holatlar
// ajralib ketadi. Agar rollback kerak bo'lsa, aniq ko'rsatish shart:
@Transactional(rollbackFor = Exception.class)

// Teskari holat: biznes istisnosida rollback kerak emas.
@Transactional(noRollbackFor = InsufficientFundsException.class)
public void withdraw(...) {
    attempts.record(accountId);           // urinish yozuvi saqlanishi kerak
    if (balance < amount) throw new InsufficientFundsException();
}
// Diqqat: bu nozik naqsh. Review da savol - urinish yozuvi haqiqatan
// saqlanishi kerakmi, va u alohida tranzaksiyada (REQUIRES_NEW) bo'lishi
// aniqroq bo'lmaydimi.
```

## 19.6 Tranzaksiya uzunligi va PostgreSQL ga ta'siri

Uzoq tranzaksiya nafaqat qulf ushlaydi, balki butun bazaga ta'sir qiladi: `VACUUM` eski versiyalarni tozalay olmaydi va jadvallar bo'rtadi.

```sql
-- Review paytida tekshirish: eng uzoq ishlayotgan tranzaksiyalar.
SELECT pid, now() - xact_start AS davomiyligi, state,
       left(query, 80) AS sorov
  FROM pg_stat_activity
 WHERE xact_start IS NOT NULL
   AND now() - xact_start > interval '30 seconds'
 ORDER BY xact_start;

-- Idle in transaction - eng xavfli holat: ulanish band, qulf bor, ish yo'q.
-- Bu deyarli har doim kod xatosi: tranzaksiya ochilib, tashqi chaqiruv
-- kutilyapti yoki commit chaqirilmagan.
SELECT count(*) FROM pg_stat_activity WHERE state = 'idle in transaction';
```

```properties
# Himoya chegaralarini qo'yish: review da shu sozlamalar borligini tekshirish.
# Ilova tomonda:
spring.transaction.default-timeout=10            # sekund
# PostgreSQL tomonda (foydalanuvchi yoki ulanish darajasida):
#   SET statement_timeout = '10s';
#   SET idle_in_transaction_session_timeout = '30s';
#   SET lock_timeout = '3s';
# Bu uchlik nazoratdan chiqqan tranzaksiyani o'zi to'xtatadi.
```

Review da `@Transactional(timeout = ...)` ning yo'qligi uzoq operatsiyalar uchun savol: agar bu metod odatda 100 ms ishlasa va bir kun 10 daqiqa ishlab qolsa, nima bo'ladi.

## 19.7 Commit dan keyin bajarilishi kerak bo'lgan ish

```java
// Xato: commit dan oldin tashqi ta'sir.
@Transactional
public void place(PlaceOrder cmd) {
    Order o = orders.save(Order.from(cmd));
    cache.evict("orders");                   // commit yiqilsa - kesh bekorga tozalangan
    searchIndex.index(o);                    // commit yiqilsa - indeksda yo'q buyurtma
}

// To'g'ri: commit dan keyin, aniq mexanizm bilan.
@Transactional
public void place(PlaceOrder cmd) {
    Order o = orders.save(Order.from(cmd));
    TransactionSynchronizationManager.registerSynchronization(
        new TransactionSynchronization() {
            @Override public void afterCommit() {
                cache.evict("orders");
                searchIndex.index(o);        // bu yiqilsa - log va metrika kerak
            }
        });
}
// Yoki deklarativ: @TransactionalEventListener(phase = AFTER_COMMIT) (11.5).
// Muhim ma'lumot uchun esa outbox (10.8) - afterCommit kafolat bermaydi:
// protsess shu oraliqda o'lsa, ish bajarilmaydi.
```

## 19.8 OSIV va lazy loading

```properties
# Spring Boot da standart holatda YOQILGAN:
spring.jpa.open-in-view=true
# Bu nima qiladi: Hibernate sessiyasi butun HTTP so'rov davomida ochiq
# qoladi, shuning uchun view (yoki JSON serializatsiya) paytida lazy
# maydonlarni yuklash mumkin.
```

Review da bu sozlama uchun aniq pozitsiya bo'lishi kerak:

| `open-in-view` | Foydasi | Narxi |
| --- | --- | --- |
| `true` (standart) | `LazyInitializationException` chiqmaydi | DB ulanishi so'rov oxirigacha band; serializatsiya paytida yashirin so'rovlar (N+1); xatolar javob yozilayotganda chiqadi |
| `false` | Ulanish tranzaksiya bilan birga bo'shaydi; so'rovlar ko'rinadigan joyda | Lazy maydonlarga tegilsa istisno - DTO yoki `JOIN FETCH` majburiy |

Review tavsiyasi: `false` qilib qo'yish va DTO/projection ishlatish. Bu N+1 muammolarini review paytida ko'rinadigan qiladi, chunki ular test yoki lokal ishga tushirishda darhol istisno bilan chiqadi.

## 19.9 Tranzaksiya, kesh, event va async aralashuvi

| Aralashuv | Xavf |
| --- | --- |
| `@Cacheable` + `@Transactional` | Rollback bo'lsa kesh eski qiymatni ushlab qoladi yoki yangi noto'g'ri qiymatni keshlaydi |
| `@CacheEvict` commit dan oldin | Rollback bo'lsa kesh bekorga tozalangan (zararsiz) yoki teskarisi (xavfli) |
| `@Async` + `@Transactional` | Async thread yangi tranzaksiya oladi; chaqiruvchi hali commit qilmagan ma'lumotni o'qiy olmaydi |
| `@EventListener` sinxron | Tranzaksiya ichida ishlaydi, uni uzaytiradi |
| `@Retryable` + `@Transactional` | Tartib muhim: retry tranzaksiyadan tashqarida bo'lishi kerak, aks holda rollback-only tranzaksiyada qayta urinish |
| `@Scheduled` + `@Transactional` | Ikki instansda bir vaqtda; qulf kerak (15.5) |

```java
// Retry va tranzaksiya tartibi: eng ko'p xato qilinadigan kombinatsiya.
// Yomon: retry tranzaksiya ichida - rollback bo'lgan tranzaksiyada qayta urinish.
@Transactional
@Retryable(retryFor = OptimisticLockingFailureException.class)
public void update(OrderId id) { ... }        // ishlamaydi: tranzaksiya allaqachon o'lgan

// To'g'ri: retry tashqarida, har urinishda yangi tranzaksiya.
@Service
public class OrderUpdater {                   // tashqi bean: retry chegarasi
    @Retryable(retryFor = OptimisticLockingFailureException.class, maxAttempts = 3)
    public void update(OrderId id) { tx.update(id); }
}
@Service
public class OrderTx {                        // ichki bean: tranzaksiya chegarasi
    @Transactional
    public void update(OrderId id) { ... }
}
```

## 19.10 Review checklisti: tranzaksiyalar

| Savol | Nega |
| --- | --- |
| Chegara application servisdami | Controller va repository da bo'lmasligi kerak |
| Tranzaksiya ichida tashqi chaqiruv bormi | Ulanish va qulf ushlanishi |
| Tashqi chaqiruvda timeout bormi | Tranzaksiya cheksiz cho'zilmasligi |
| O'qish metodlarida `readOnly` bormi | Tezlik va replika marshrutlash |
| `REQUIRES_NEW` proxy orqali chaqirilyaptimi | Aks holda ishlamaydi |
| Ichkarida ushlangan istisno bormi | `UnexpectedRollbackException` xavfi |
| Checked istisno uchun `rollbackFor` kerakmi | Standart xulq commit qiladi |
| Commit dan keyingi ish to'g'ri mexanizm bilanmi | `afterCommit` yoki outbox |
| `open-in-view` pozitsiyasi aniqmi | N+1 va ulanish ushlanishi |
| Uzoq operatsiyada `timeout` bormi | Nazoratdan chiqishni oldini olish |
| Batch ishlarda tranzaksiya bo'laklanganmi | Qulf va xotira |
| `@Version` yoki qulf bormi | Parallel yangilanish (15.3) |

## 19.11 Amalda qo'llash

- [ ] `@Transactional` metodlar ichida tashqi chaqiruvlarni (HTTP mijoz, Kafka, SMS, S3) grep bilan toping va ro'yxat tuzing.
- [ ] Barcha o'qish metodlariga `readOnly = true` qo'shilganini tekshiring.
- [ ] `@Transactional` bilan belgilangan controller metodlarini toping va chegarani servis qatlamiga ko'chiring.
- [ ] Ichkarida istisno ushlaydigan tranzaksion metodlarni aniqlab, `UnexpectedRollbackException` xavfini baholang.
- [ ] `throws` ro'yxatida checked istisno bo'lgan tranzaksion metodlarda `rollbackFor` ko'rsatilganini tekshiring.
- [ ] `spring.transaction.default-timeout`, `statement_timeout`, `lock_timeout` va `idle_in_transaction_session_timeout` qiymatlarini sozlang.
- [ ] `spring.jpa.open-in-view` bo'yicha jamoa pozitsiyasini `REVIEW.md` ga yozing (tavsiya: `false`).
- [ ] `pg_stat_activity` dan 30 sekunddan uzoq tranzaksiyalar va `idle in transaction` holatlarini bir hafta kuzatib boring.
- [ ] `@Retryable` va `@Transactional` birga ishlatilgan joylarda tartibni tekshirib, retry ni tashqi bean ga chiqaring.

---

[&larr; 18. Bean, kontekst va proxy mexanikasi review](18-bean-kontekst-va-proxy-mexanikasi-review.md) · [Mundarija](README.md) · [20. Web qatlami review: DTO, validatsiya, xato javobi &rarr;](20-web-qatlami-review-dto-validatsiya-xato.md)
