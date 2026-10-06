<!-- doc: code-review | chapter: 27 | part: V. PostgreSQL va ma'lumot qatlami review -->

[Barcha hujjatlar](../../README.md) / [Kod review](README.md)

> Holat: AI yozgan, inson tekshirmagan.

# 27. Izolyatsiya, poyga holatlari va xabar yetkazish (Isolation, Races and Delivery)

<details>
<summary>Bu bobdagi 11 bo'lim</summary>

- [27.1 PostgreSQL izolyatsiya darajalari va diffdagi ma'nosi](#271-postgresql-izolyatsiya-darajalari-va-diffdagi-manosi)
- [27.2 Poyga holatlarini topish usuli](#272-poyga-holatlarini-topish-usuli)
- [27.3 Qulf turlari va ularning narxi](#273-qulf-turlari-va-ularning-narxi)
- [27.4 Optimistik yoki pessimistik: tanlov mezoni](#274-optimistik-yoki-pessimistik-tanlov-mezoni)
- [27.5 Write skew: eng jim poyga](#275-write-skew-eng-jim-poyga)
- [27.6 SERIALIZABLE ishlatilganda](#276-serializable-ishlatilganda)
- [27.7 Xabar yetkazish: "kamida bir marta" ning oqibatlari](#277-xabar-yetkazish-kamida-bir-marta-ning-oqibatlari)
- [27.8 Xabarlar tartibi](#278-xabarlar-tartibi)
- [27.9 Outbox worker review](#279-outbox-worker-review)
- [27.10 Review checklisti: izolyatsiya va yetkazish](#2710-review-checklisti-izolyatsiya-va-yetkazish)
- [27.11 Amalda qo'llash](#2711-amalda-qollash)

</details>


Bu bob ma'lumot qatlamining eng qiyin qismini oladi: bir vaqtda ishlayotgan tranzaksiyalar va bir martadan ko'p yetkaziladigan xabarlar. Ularning umumiy xususiyati bor - testda ko'rinmaydi, yuk ostida ko'rinadi, va oqibati ma'lumot nomuvofiqligi bo'ladi. Reviewer uchun bitta tayanch savol: "ikki narsa bir vaqtda sodir bo'lsa yoki bir narsa ikki marta sodir bo'lsa, natija to'g'ri bo'ladimi".

## 27.1 PostgreSQL izolyatsiya darajalari va diffdagi ma'nosi

PostgreSQL ning standarti `READ COMMITTED`, va u Java kodidagi ko'p taxminlarni buzadi.

| Daraja | Nimani oldini oladi | Nimani oldini olmaydi |
| --- | --- | --- |
| `READ COMMITTED` (standart) | Yozilmagan ma'lumotni o'qish | Takrorlanmaydigan o'qish, fantom, lost update, write skew |
| `REPEATABLE READ` | Takrorlanmaydigan o'qish, fantom (PG da) | Write skew; konflikt bo'lsa xato beradi |
| `SERIALIZABLE` | Hammasi | Hech narsa, lekin xato (`40001`) berib retry talab qiladi |

```java
// READ COMMITTED da bitta tranzaksiya ichida ikki o'qish turli natija beradi.
@Transactional                                   // READ COMMITTED
public Report build(CustomerId id) {
    Money total = orders.sumByCustomer(id);      // 1 000 000
    int count = orders.countByCustomer(id);      // 11 - boshqa tranzaksiya qo'shdi
    // total 10 buyurtmaga, count 11 ga tegishli - hisobot nomuvofiq.
    return new Report(total, count, total.divide(count));   // noto'g'ri o'rtacha
}
// Review izohi: ikki so'rov orasida ma'lumot o'zgarishi mumkin. Agar
// hisobot ichki nomuvofiqligi qabul qilinmasa, bitta so'rovda hisoblash
// yoki REPEATABLE READ kerak.

// Yechim 1 (afzal): bitta so'rov - atomik ko'rinish.
@Query("select new ReportRow(sum(o.total), count(o)) from Order o where o.customer.id = :id")
ReportRow report(@Param("id") UUID id);

// Yechim 2: izolyatsiyani ko'tarish - lekin narxi bor.
@Transactional(isolation = Isolation.REPEATABLE_READ)
```

## 27.2 Poyga holatlarini topish usuli

Review da poyga holatini topishning tizimli usuli bor: har bir yozuv operatsiyasi uchun "o'qish va yozish orasida nima o'zgarishi mumkin" degan savol.

| Naqsh | Poyga turi | Himoya |
| --- | --- | --- |
| `exists` keyin `insert` | Fantom / dublikat | Unique indeks |
| `select` keyin `update` (hisoblab) | Lost update | `@Version` yoki atomik `UPDATE` |
| `select` qoldiq, keyin `update` | Write skew | `FOR UPDATE` yoki `SERIALIZABLE` |
| Ikki jadvaldan o'qib, qoida tekshirish | Write skew | Qulf yoki `SERIALIZABLE` |
| Hisoblagichni o'qib, oshirib yozish | Lost update | `UPDATE ... SET n = n + 1` |
| `delete` keyin `insert` (almashtirish) | Oraliq bo'shliq | Bitta `UPSERT` |
| Fayl yoki kesh tekshiruvi keyin yozuv | Umumiy resurs | Atomik operatsiya |

```java
// UPSERT: "bor bo'lsa yangila, yo'q bo'lsa qo'sh" - poygasiz yo'l.
@Modifying
@Query(value = """
    INSERT INTO daily_counter (day, metric, value)
    VALUES (:day, :metric, 1)
    ON CONFLICT (day, metric)
    DO UPDATE SET value = daily_counter.value + 1
    """, nativeQuery = true)
void increment(@Param("day") LocalDate day, @Param("metric") String metric);
// Bu bitta atomik operatsiya: hech qanday tekshir-keyin-yoz yo'q, hech
// qanday qulf navbati yo'q. Review da bu shakl afzal ko'riladi.
```

## 27.3 Qulf turlari va ularning narxi

```sql
-- FOR UPDATE: qator qulflanadi, boshqalar kutadi.
SELECT * FROM account WHERE id = ? FOR UPDATE;
-- Xavf: kutish cheksiz bo'lishi mumkin (lock_timeout kerak).

-- FOR UPDATE NOWAIT: kutmaydi, darhol xato.
SELECT * FROM account WHERE id = ? FOR UPDATE NOWAIT;
-- Foydali: foydalanuvchiga "hozir band, qayta urinib ko'ring" deyish.

-- FOR UPDATE SKIP LOCKED: qulflangan qatorlarni o'tkazib yuboradi.
SELECT * FROM job_queue WHERE status = 'NEW'
 ORDER BY created_at LIMIT 10 FOR UPDATE SKIP LOCKED;
-- Navbat uchun ideal: workerlar bir-birini kutmaydi.

-- FOR SHARE: o'qish qulfi - boshqalar o'qiydi, yozmaydi.
-- Kam ishlatiladi; ko'pincha FOR UPDATE yoki hech narsa to'g'ri.
```

```java
// Spring Data da qulf turlari.
public interface AccountRepository extends JpaRepository<Account, UUID> {

    @Lock(LockModeType.PESSIMISTIC_WRITE)                    // FOR UPDATE
    @Query("select a from Account a where a.id = :id")
    Optional<Account> lockById(@Param("id") UUID id);

    // Timeout bilan: cheksiz kutmaslik.
    @Lock(LockModeType.PESSIMISTIC_WRITE)
    @QueryHints(@QueryHint(name = "jakarta.persistence.lock.timeout", value = "3000"))
    @Query("select a from Account a where a.id = :id")
    Optional<Account> lockByIdWithTimeout(@Param("id") UUID id);
}
// Review savollari: qulf qancha vaqt ushlanadi (tranzaksiya oxirigacha),
// uning ichida tashqi chaqiruv bormi (19.2), va qulf tartibi barqarormi
// (15.4 - deadlock).
```

## 27.4 Optimistik yoki pessimistik: tanlov mezoni

| Mezon | Optimistik (`@Version`) | Pessimistik (`FOR UPDATE`) |
| --- | --- | --- |
| Konflikt ehtimoli | Past | Yuqori |
| Foydalanuvchi tajribasi | "Ma'lumot o'zgardi, qayta yuklang" | Kutish |
| Narxi | Konfliktda ish qaytariladi | Qulf va navbat |
| Uzoq tahrirlash (forma) | Mos | Mos emas (qulf soatlab turadi) |
| Qisqa hisob (qoldiq) | Retry ko'p bo'lishi mumkin | Mos |
| Ko'p instans | Ishlaydi | Ishlaydi |

Review qoidasi: foydalanuvchi formasi orqali tahrirlash - optimistik; pul va qoldiq hisobi - atomik `UPDATE` yoki pessimistik qulf; navbat va worker - `SKIP LOCKED`.

Mavzuning to'liq yozuvi [optimistic locking](../patterns/09-malumotlarga-kirish-va-orm-patternlari.md#923-optimistik-oflayn-qulf-optimistic-offline-lock) bo'limida; bu yerda faqat shu bo'limning nuqtai nazari.

## 27.5 Write skew: eng jim poyga

Write skew - ikki tranzaksiya turli qatorlarni o'zgartiradi, lekin birgalikda biznes qoidasini buzadi. `FOR UPDATE` ham bu holda yordam bermaydi, chunki qulflanadigan qator yo'q.

```java
// Qoida: har bir smenada kamida bitta shifokor navbatchi bo'lishi kerak.
@Transactional
public void requestLeave(DoctorId doctor, ShiftId shift) {
    long onCall = schedule.countOnCall(shift);       // T1: 2, T2: 2
    if (onCall <= 1) throw new MinimumStaffingViolated();
    schedule.removeFromShift(doctor, shift);         // T1 va T2 turli qator
}
// Ikki shifokor bir vaqtda ta'til so'rasa: ikkisi ham "2 ta bor" deb
// ko'radi, ikkisi ham o'tadi, va smenada 0 navbatchi qoladi.
// FOR UPDATE yordam bermaydi: ular turli qatorlarni o'zgartiradi.

// Yechim 1: SERIALIZABLE + retry. PostgreSQL buni aniqlaydi (40001).
@Transactional(isolation = Isolation.SERIALIZABLE)
@Retryable(retryFor = CannotAcquireLockException.class, maxAttempts = 3,
           backoff = @Backoff(delay = 50, random = true))
public void requestLeave(DoctorId doctor, ShiftId shift) { ... }
// Review diqqati: retry tranzaksiyadan TASHQARIDA bo'lishi kerak (19.9).

// Yechim 2: umumiy qatorni qulflash - "smena" qatorini qulflash.
Shift s = shifts.lockById(shift);                    // ikkisi ham shu qatorda
long onCall = schedule.countOnCall(shift);
...

// Yechim 3: qoidani bazaga ko'chirish (eng ishonchli, lekin har doim mumkin emas).
-- Hisoblangan ustun + CHECK, yoki trigger, yoki exclusion constraint.
```

## 27.6 SERIALIZABLE ishlatilganda

```java
// SERIALIZABLE da ilova retry ni ko'tarishi SHART - bu majburiy shart.
// PostgreSQL "could not serialize access due to read/write dependencies"
// xatosini beradi (SQLState 40001). Bu xato emas, normal signal.
@Service
public class TransferService {

    @Retryable(retryFor = { CannotSerializeTransactionException.class,
                            CannotAcquireLockException.class },
               maxAttempts = 5,
               backoff = @Backoff(delay = 20, multiplier = 2, random = true))
    public void transfer(TransferCommand cmd) {
        tx.doTransfer(cmd);                     // ichki bean: @Transactional(SERIALIZABLE)
    }

    @Recover
    public void onRepeatedConflict(CannotSerializeTransactionException e, TransferCommand cmd) {
        meter.counter("transfer.serialization.exhausted").increment();
        throw new TemporarilyUnavailable("qayta urinib ko'ring", e);   // 503
    }
}
// Review savollari: retry bormi, backoff da jitter bormi, urinishlar
// tugaganda nima bo'ladi, va bu holat o'lchanadimi (metrika).
// Qo'shimcha: retry qilinadigan operatsiya idempotent bo'lishi kerak -
// aks holda retry ikki marta ta'sir qiladi.
```

## 27.7 Xabar yetkazish: "kamida bir marta" ning oqibatlari

Kafka, RabbitMQ, SQS va outbox - hammasi "kamida bir marta" yetkazadi. "Aniq bir marta" yetkazish amalda iste'molchi tomonidagi idempotentlik bilan quriladi, broker bilan emas.

```java
// Review talabi: iste'molchi dublikatga chidamli bo'lishi kerak.
@KafkaListener(topics = "payments")
@Transactional
public void onPaymentCaptured(PaymentCaptured event, Acknowledgment ack) {
    // 1) Qayta ishlangan xabarlarni belgilash: unique kalit bilan.
    try {
        processed.save(new ProcessedMessage(event.messageId()));
        em.flush();                                  // konflikt shu yerda chiqadi
    } catch (DataIntegrityViolationException dup) {
        log.debug("xabar allaqachon qayta ishlangan: {}", event.messageId());
        ack.acknowledge();                           // dublikat - jim o'tkazamiz
        return;
    }
    // 2) Asosiy ish - bir xil tranzaksiyada.
    orders.applyPayment(event.orderId(), event.amount());
    ack.acknowledge();
}
```

```sql
-- Qayta ishlangan xabarlar jadvali: oyna bilan, cheksiz o'smaydi.
CREATE TABLE processed_message (
    message_id text PRIMARY KEY,
    processed_at timestamptz NOT NULL DEFAULT now()
);
CREATE INDEX processed_message_at_idx ON processed_message (processed_at);
-- Tozalash: 7 kundan eski yozuvlar (broker retention dan uzunroq bo'lsin).
```

Alternativa - tabiiy idempotentlik: operatsiyaning o'zi takrorlanganda zarar keltirmasligi. `UPDATE orders SET status = 'PAID' WHERE id = ? AND status = 'NEW'` ikki marta bajarilsa, ikkinchisi 0 qator o'zgartiradi. Bu eng toza yechim, lekin har doim mumkin emas.

## 27.8 Xabarlar tartibi

```java
// Review savoli: tartib muhimmi, va u qanday kafolatlanadi?
// Kafka da tartib FAQAT bitta partition ichida kafolatlanadi.
kafkaTemplate.send("orders", order.id().toString(), event);
//                            ^^^^^^^^^^^^^^^^^^^ kalit: bir buyurtmaning
// hamma hodisasi bitta partition ga tushadi, ya'ni tartibda keladi.

// Kalit berilmasa - round-robin, tartib yo'q:
kafkaTemplate.send("orders", event);           // OrderShipped, OrderPaid dan
                                               // oldin kelishi mumkin!

// Review izohi: `OrderPaid` va `OrderShipped` turli partition larga tushsa,
// iste'molchi ularni teskari tartibda qabul qilishi mumkin va buyurtmani
// to'lanmagan holda jo'natilgan deb belgilaydi.
// Yechim: agregat ID ni kalit sifatida ishlatish.

// Qo'shimcha himoya: iste'molchi tomonda tartibdan tashqari xabarni aniqlash.
if (event.version() <= order.lastAppliedVersion()) {
    log.debug("eski yoki takroriy hodisa, o'tkazib yuborildi");
    return;                                    // monotonik versiya tekshiruvi
}
```

## 27.9 Outbox worker review

Outbox naqshi 10.8 da kiritilgan; bu yerda worker tomonidagi review savollari.

```java
@Component
public class OutboxPublisher {

    @Scheduled(fixedDelay = 500)
    @SchedulerLock(name = "outboxPublisher")         // ikki instans emas (15.5)
    public void publish() {
        // SKIP LOCKED: bir necha worker parallel ishlashi mumkin.
        List<OutboxMessage> batch = outbox.lockPendingBatch(100);
        for (OutboxMessage m : batch) {
            try {
                broker.send(m.topic(), m.key(), m.payload());
                outbox.markPublished(m.id());
            } catch (Exception e) {
                outbox.markFailed(m.id(), e.getMessage());   // attempts++
                meter.counter("outbox.failed").increment();
                // Diqqat: bu yerda break qilmaslik kerak - bitta xabar
                // boshqalarni bloklamasligi uchun (poison pill).
            }
        }
    }
}
```

| Review savoli | Nega |
| --- | --- |
| Jadval tozalanadimi | Cheksiz o'sish |
| Ikki instans parallel ishlasa to'g'rimi | `SKIP LOCKED` yoki qulf |
| Bitta xato xabar oqimni bloklaydimi | Poison pill |
| Urinishlar soni cheklanganmi | Cheksiz retry |
| Yetkazilmagan xabarlar uchun alert bormi | Jim yo'qotish |
| Kechikish o'lchanadimi | Eng qadimgi yetkazilmagan xabar yoshi |
| Tartib kerak bo'lsa, ta'minlanganmi | Agregat bo'yicha ketma-ketlik |
| Payload sxemasi versiyalanganmi | Iste'molchi moslik |

```sql
-- Outbox holati uchun monitoring so'rovi: review da shu metrika talab qilinadi.
SELECT count(*) AS kutayotgan,
       max(now() - created_at) AS eng_qadimgi,
       count(*) FILTER (WHERE attempts > 3) AS muammoli
  FROM outbox_message WHERE published_at IS NULL;
-- Alert: eng_qadimgi > 5 daqiqa yoki muammoli > 0.
```

Mavzuning to'liq yozuvi [transactional outbox](../patterns/10-malumotlarni-boshqarish-va-taqsimlash.md#1014-tranzaksion-outbox-transactional-outbox) bo'limida; bu yerda faqat shu bo'limning nuqtai nazari.

## 27.10 Review checklisti: izolyatsiya va yetkazish

| Savol | Nega |
| --- | --- |
| Tekshir-keyin-yoz naqshi himoyalanganmi | Dublikat |
| Hisoblab yozish atomikmi | Lost update |
| Write skew ehtimoli baholanganmi | Jim qoida buzilishi |
| `SERIALIZABLE` ishlatilsa, retry bormi | 40001 xatosi |
| Retry idempotent operatsiyadami | Ikki marta ta'sir |
| Qulf tartibi barqarormi | Deadlock |
| Qulf ichida tashqi chaqiruv yo'qmi | Uzoq qulf |
| `lock_timeout` qo'yilganmi | Cheksiz kutish |
| Iste'molchi dublikatga chidamlimi | Kamida bir marta yetkazish |
| Xabar kaliti tartibni ta'minlaydimi | Teskari tartib |
| Outbox kechikishi o'lchanadimi | Jim to'xtash |
| Poison pill oqimni bloklamaydimi | To'xtab qolgan iste'molchi |

## 27.11 Amalda qo'llash

- [ ] Barcha yozuv operatsiyalari uchun "o'qish va yozish orasida nima o'zgarishi mumkin" savolini o'tkazib, poyga xavfi bor joylarni ro'yxatga oling.
- [ ] Hisoblagich va qoldiq yangilashlarini atomik `UPDATE` yoki `UPSERT` ga o'tkazing.
- [ ] Write skew ehtimoli bor biznes qoidalarini (minimal shtat, limit, kvota) aniqlab, ularga `SERIALIZABLE` + retry yoki umumiy qator qulfi qo'shing.
- [ ] `SERIALIZABLE` ishlatilgan joylarda retry, jitter, `@Recover` va metrika borligini tasdiqlang.
- [ ] Navbat va worker so'rovlarini `FOR UPDATE SKIP LOCKED` ga o'tkazing.
- [ ] Barcha Kafka produserlarida xabar kaliti agregat ID si ekanini tekshiring.
- [ ] Iste'molchilarda qayta ishlangan xabarlar jadvali yoki tabiiy idempotentlik borligini tasdiqlang va tozalash ishini qo'shing.
- [ ] Outbox uchun kutayotgan xabarlar soni va eng qadimgi xabar yoshi metrikalarini va alertni qo'shing.
- [ ] `lock_timeout` va `deadlock_timeout` qiymatlarini sozlab, deadlock loglarini bir hafta kuzatib boring.

---

[&larr; 26. Ma'lumot to'g'riligi va turlar review](26-malumot-togriligi-va-turlar-review.md) · [Mundarija](README.md) · [28. Xavfsizlik review metodikasi &rarr;](28-xavfsizlik-review-metodikasi.md)
