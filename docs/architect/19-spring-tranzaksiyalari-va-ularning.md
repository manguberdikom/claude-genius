<!-- doc: architect | chapter: 19 | part: III. Spring chuqur bilim -->

[Barcha hujjatlar](../../README.md) / [Arxitektor miyasi](README.md)

> Holat: AI yozgan, inson tekshirmagan.

# 19. Spring tranzaksiyalari va ularning chegaralari (Spring Transactions)

<details>
<summary>Bu bobdagi 13 bo'lim</summary>

- [19.1 `@Transactional` qanday ishlaydi: proxy, `TransactionInterceptor`, `PlatformTransactionManager`](#191-transactional-qanday-ishlaydi-proxy-transactioninterceptor-platformtransactionmanager)
- [19.2 Propagation turlari: `REQUIRED`, `REQUIRES_NEW`, `NESTED` va amaliy farqi](#192-propagation-turlari-required-requires_new-nested-va-amaliy-farqi)
- [19.3 Isolation darajasini Spring da belgilash va PostgreSQL dagi haqiqiy xatti-harakat](#193-isolation-darajasini-spring-da-belgilash-va-postgresql-dagi-haqiqiy-xatti-harakat)
- [19.4 Rollback qoidasi: nega tekshiriladigan istisnoda rollback bo'lmaydi](#194-rollback-qoidasi-nega-tekshiriladigan-istisnoda-rollback-bolmaydi)
- [19.5 `readOnly = true` nima beradi va nima bermaydi](#195-readonly--true-nima-beradi-va-nima-bermaydi)
- [19.6 Ichki metod chaqiruvi tuzog'i va undan chiqish yo'llari](#196-ichki-metod-chaqiruvi-tuzogi-va-undan-chiqish-yollari)
- [19.7 Tranzaksiya uzunligi: tashqi HTTP chaqiruvni tranzaksiya ichiga qo'ymaslik](#197-tranzaksiya-uzunligi-tashqi-http-chaqiruvni-tranzaksiya-ichiga-qoymaslik)
- [19.8 `TransactionSynchronization` va `@TransactionalEventListener` bilan commit dan keyin ish](#198-transactionsynchronization-va-transactionaleventlistener-bilan-commit-dan-keyin-ish)
- [19.9 Tranzaksiya va kesh, tranzaksiya va xabar yuborish nomuvofiqligi](#199-tranzaksiya-va-kesh-tranzaksiya-va-xabar-yuborish-nomuvofiqligi)
- [19.10 Timeout, lock kutish vaqti va deadlock bilan uchrashish](#1910-timeout-lock-kutish-vaqti-va-deadlock-bilan-uchrashish)
- [19.11 Dasturiy tranzaksiya: `TransactionTemplate` qachon aniqroq](#1911-dasturiy-tranzaksiya-transactiontemplate-qachon-aniqroq)
- [19.12 Katta batch operatsiyalarda tranzaksiya chegarasini tanlash](#1912-katta-batch-operatsiyalarda-tranzaksiya-chegarasini-tanlash)
- [19.13 Amalda qo'llash](#1913-amalda-qollash)

</details>



Tranzaksiya arxitektorning qo'lidagi eng arzon va eng xavfli asbob. Arzon, chunki bitta annotatsiya yozasan. Xavfli, chunki o'sha annotatsiya connection'ni egallaydi, PostgreSQL da lock ushlaydi va snapshot muzlatadi, buning hammasi kodda ko'rinmaydi. Bu bobda `@Transactional` ning ichki mexanikasi, uning chegaralari va o'sha chegaralarni qanday joylashtirish kerakligi haqida gaplashamiz.

## 19.1 `@Transactional` qanday ishlaydi: proxy, `TransactionInterceptor`, `PlatformTransactionManager`

`@Transactional` tilning imkoniyati emas, Spring AOP ning natijasi. `@EnableTransactionManagement` (Spring Boot da `TransactionAutoConfiguration` orqali avtomatik) `BeanFactoryTransactionAttributeSourceAdvisor` ni ro'yxatga oladi. Bean yaratilayotganda `InfrastructureAdvisorAutoProxyCreator` sinfda yoki metodda tranzaksiya atributi borligini `AnnotationTransactionAttributeSource` yordamida aniqlaydi va bean o'rniga proxy qaytaradi. Interfeys bo'lsa JDK dynamic proxy, bo'lmasa CGLIB subclass.

Chaqiruv proxy ga kelganda `TransactionInterceptor` ishga tushadi. U `TransactionAttribute` ni o'qiydi, `PlatformTransactionManager` dan `getTransaction(definition)` so'raydi, maqsadli metodni chaqiradi, keyin `commit` yoki `rollback` qiladi. JPA uchun bu `JpaTransactionManager`, faqat `JdbcTemplate` uchun `DataSourceTransactionManager`. Ikkalasi ham `AbstractPlatformTransactionManager` dan keladi va connection yoki `EntityManager` ni `TransactionSynchronizationManager` ning thread-local resurs xaritasiga bog'laydi.

```java
// Spring Boot avtomatik beradi, lekin arxitektor nimani sozlashini bilishi kerak
@Configuration
@EnableTransactionManagement // Boot da default; AdviceMode.PROXY
public class TxConfig {

    @Bean
    public JpaTransactionManager transactionManager(EntityManagerFactory emf) {
        JpaTransactionManager tm = new JpaTransactionManager(emf);
        // default timeout: hech qanday @Transactional da timeout ko'rsatilmasa shu ishlaydi
        tm.setDefaultTimeout(5); // sekund
        // DataSourceTransactionManager da savepoint uchun kerak; JPA da ko'pincha qo'llanmaydi
        tm.setNestedTransactionAllowed(false);
        return tm;
    }

    @Bean
    public TransactionTemplate paymentTxTemplate(PlatformTransactionManager tm) {
        TransactionTemplate t = new TransactionTemplate(tm);
        t.setIsolationLevel(TransactionDefinition.ISOLATION_REPEATABLE_READ);
        t.setTimeout(3);
        return t;
    }
}
```

Shu mexanikadan ikki natija kelib chiqadi. Birinchi: tranzaksiya faqat proxy orqali o'tgan chaqiruvda boshlanadi. Ikkinchi: `EntityManager` thread ga bog'langan, demak boshqa thread ga o'tgan ish (masalan `CompletableFuture.supplyAsync`) tashqaridagi tranzaksiyani ko'rmaydi.

## 19.2 Propagation turlari: `REQUIRED`, `REQUIRES_NEW`, `NESTED` va amaliy farqi

`REQUIRED` default. Tranzaksiya bo'lsa unga qo'shiladi, bo'lmasa yangisini boshlaydi. "Qo'shiladi" so'zi aldaydi: ichki metodda `rollback` sodir bo'lsa, u o'z o'zini bekor qila olmaydi, faqat umumiy tranzaksiyani `rollback-only` deb belgilaydi. Tashqi metod istisnoni yutib yuborib commit qilmoqchi bo'lsa, Spring `UnexpectedRollbackException` tashlaydi. Bu eng ko'p uchraydigan "nega ma'lumot saqlanmadi" sababi.

`REQUIRES_NEW` tashqi tranzaksiyani to'xtatib (suspend qilib) butunlay yangi tranzaksiya oladi. Bu yangi connection degani: pool dan ikkinchi connection olinadi va ikkisi ham bir vaqtda band bo'ladi. Shuning uchun `REQUIRES_NEW` ni rekursiv yoki loop ichida ishlatish pool ni tugatadigan klassik xato. 20 ta connection li pool da 10 ta parallel so'rov bitta joyda `REQUIRES_NEW` qilsa, pool to'la bo'ladi va qolgan so'rovlar `HikariPool-1 - Connection is not available` bilan tushadi.

`NESTED` savepoint ishlatadi: ichki qism bekor bo'lsa faqat savepoint ga qaytadi, tashqi tranzaksiya davom etadi. Lekin bu `SavepointManager` ni talab qiladi. `DataSourceTransactionManager` da `nestedTransactionAllowed = true` bo'lsa ishlaydi, `JpaTransactionManager` da esa odatda `NestedTransactionNotSupportedException` olasan. Agar savepoint kerak bo'lsa, `JdbcTemplate` qatlamida yoki `EntityManager.unwrap(Session.class)` orqali aniq boshqarish amaliyroq.

```java
@Service
public class PaymentService {

    private final PaymentRepository payments;
    private final AuditLogService audit;

    @Transactional // REQUIRED: buyurtma va to'lov bitta atomar birlik
    public void charge(Long orderId, BigDecimal amount) {
        Payment p = payments.save(Payment.pending(orderId, amount));
        // Audit yozuvi to'lov bekor bo'lsa ham qolishi kerak: alohida tranzaksiya
        audit.record(orderId, "CHARGE_STARTED");
        gateway.authorize(p); // istisno chiqsa to'lov rollback, audit qoladi
    }
}

@Service
public class AuditLogService {
    // REQUIRES_NEW: pool dan ikkinchi connection oladi, buni hisobga ol
    @Transactional(propagation = Propagation.REQUIRES_NEW, timeout = 2)
    public void record(Long orderId, String event) {
        auditRepo.save(new AuditLog(orderId, event, Instant.now()));
    }
}
```

Amaliy qoida: `REQUIRES_NEW` ni faqat "bu yozuv asosiy ish bekor bo'lsa ham qolishi kerak" holatida ishlat. Audit, xatolar jurnali, retry hisoblagichi. Boshqa barcha holatda `REQUIRED` yetarli.

## 19.3 Isolation darajasini Spring da belgilash va PostgreSQL dagi haqiqiy xatti-harakat

`@Transactional(isolation = Isolation.REPEATABLE_READ)` yozganingda Spring `Connection.setTransactionIsolation` chaqiradi, keyin tranzaksiya oxirida eski qiymatni qaytaradi. PostgreSQL da to'rtta nomdan amalda uchtasi ishlaydi: `READ UNCOMMITTED` `READ COMMITTED` ga aylanadi, chunki PostgreSQL da dirty read umuman mavjud emas.

`READ COMMITTED` default va har bir statement o'z snapshot ini oladi. Ya'ni bitta tranzaksiya ichidagi ikkita `SELECT` boshqa natija berishi mumkin. `REPEATABLE READ` PostgreSQL da snapshot isolation sifatida amalga oshirilgan: tranzaksiya boshidagi snapshot oxirigacha saqlanadi va yozuv to'qnashuvida `40001 serialization_failure` keladi. `SERIALIZABLE` esa Serializable Snapshot Isolation ishlatadi va predicate darajasidagi anomaliyani ham tutadi, lekin ko'proq `40001` beradi.

Muhim nuqta: `40001` va `40P01` dasturchi kodida retry qilinadigan xatolar. Spring ularni `CannotAcquireLockException` yoki `ConcurrencyFailureException` ga aylantiradi. Retry esa tranzaksiya tashqarisida bo'lishi kerak, aks holda bekor qilingan tranzaksiyani qayta ishlatishga urinasan.

```sql
-- Ombor qoldig'ini tekshirish: REPEATABLE READ da bu ikki SELECT bir xil natija beradi
BEGIN ISOLATION LEVEL REPEATABLE READ;
SELECT quantity FROM stock WHERE sku = 'SKU-1001';
-- boshqa tranzaksiya shu qatorni o'zgartirib commit qildi
UPDATE stock SET quantity = quantity - 1 WHERE sku = 'SKU-1001';
-- ERROR: 40001 could not serialize access due to concurrent update
ROLLBACK;

-- READ COMMITTED da xuddi shu ishni atomar qilish yo'li: shartni SQL ga ko'chirish
UPDATE stock SET quantity = quantity - 1
 WHERE sku = 'SKU-1001' AND quantity >= 1;
-- 0 qator qaytsa qoldiq yetmagan; hech qanday race yo'q
```

Arxitektor qarori oddiy: kamayadigan resurs (ombor qoldig'i, balans, limit) uchun yuqori isolation emas, atomar `UPDATE ... WHERE` yoki `SELECT ... FOR UPDATE` ishlatiladi. `SERIALIZABLE` ni faqat murakkab invariant (masalan "bitta smenada ikki shifokor bo'lmasin") SQL ga sig'masa tanlaymiz va retry bilan birga tanlaymiz.

## 19.4 Rollback qoidasi: nega tekshiriladigan istisnoda rollback bo'lmaydi

Spring ning default qoidasi `RuleBasedTransactionAttribute` ichida: `RuntimeException` va `Error` da rollback, qolganida commit. Bu EJB dan kelgan tarixiy meros, mantiq esa shunday edi: checked exception biznes natijasining bir qismi, demak ma'lumot saqlanishi kerak. Amalda esa bu kutilmagan commit lar manbasi, chunki hech kim `IOException` dan keyin yarim yozilgan buyurtma qolishini xohlamaydi.

Yechim uchta. Birinchi: loyihada checked exception ni biznes qatlamida umuman ishlatmaslik va `RuntimeException` dan meros olgan domen istisnolarini qurish. Ikkinchi: `@Transactional(rollbackFor = Exception.class)` ni aniq yozish. Uchinchi: istisno tutilgan, lekin ish bekor bo'lishi kerak bo'lgan joyda `TransactionAspectSupport.currentTransactionStatus().setRollbackOnly()`.

```java
@Service
public class OrderService {

    // Checked istisnoda ham rollback kerak: aniq yozamiz
    @Transactional(rollbackFor = Exception.class, noRollbackFor = StockReservedException.class)
    public void place(OrderRequest req) throws InventoryUnavailableException {
        Order order = orderRepo.save(Order.from(req));
        try {
            inventory.reserve(order);
        } catch (PartialReservationException e) {
            // Yozuv qolsin, lekin tranzaksiya commit bo'lmasin degan holat:
            TransactionAspectSupport.currentTransactionStatus().setRollbackOnly();
            log.warn("Buyurtma {} qisman band qilindi, bekor qilinadi", order.getId());
        }
    }
}
```

Alohida tuzoq: ichki `REQUIRED` metod istisno tashlab, tashqi metod uni `catch` qilsa, tranzaksiya allaqachon `rollback-only`. Tashqi metod commit qilmoqchi bo'ladi va `UnexpectedRollbackException` oladi. Agar ichki qismning muvaffaqiyatsizligi kechirimli bo'lsa, u `REQUIRES_NEW` bo'lishi kerak, yoki umuman tranzaksiyadan tashqariga chiqarilishi kerak.

## 19.5 `readOnly = true` nima beradi va nima bermaydi

`readOnly = true` ning eng aniq samarasi Hibernate qatlamida: Spring `Session` ning flush mode ini `MANUAL` ga qo'yadi, natijada commit da avtomatik flush bo'lmaydi va dirty checking amalda bajarilmaydi. Katta `SELECT` lar uchun bu sezilarli yutuq: 10 000 entity o'qilgan hisobot metodida dirty check ga ketadigan vaqt va snapshot xotirasi yo'qoladi.

Nimani bermaydi: u ma'lumotni o'zgartirishdan himoya qilmaydi degan tushuncha noto'g'ri emas, lekin yarim to'g'ri. Native query yoki `JdbcTemplate` orqali `UPDATE` bajarish mumkin bo'lib qolishi mumkin, chunki JDBC connection ning `readOnly` flagi har doim DB tomoniga yetib bormaydi. Shuningdek `readOnly` o'zi bilan replika ga yo'naltirish qilmaydi. Yo'naltirishni o'zing qurasan: `AbstractRoutingDataSource` da `TransactionSynchronizationManager.isCurrentTransactionReadOnly()` ni o'qib key tanlaysan.

```java
// Read-only tranzaksiyani replika ga yo'naltirish: Spring o'zi qilmaydi
public class ReplicaRoutingDataSource extends AbstractRoutingDataSource {
    @Override
    protected Object determineCurrentLookupKey() {
        // readOnly = true bo'lsa replika, aks holda primary
        return TransactionSynchronizationManager.isCurrentTransactionReadOnly()
                ? "replica" : "primary";
    }
}
```

```properties
# Hisobot so'rovlari uchun DB tomonidan kafolat: faqat shu yerda haqiqiy himoya bor
spring.datasource.hikari.read-only=false
spring.jpa.open-in-view=false
# Har bir statement uchun qattiq chegara (PostgreSQL tomonida ishlaydi)
spring.datasource.hikari.connection-init-sql=SET statement_timeout = '5s'
spring.jpa.properties.hibernate.jdbc.batch_size=50
spring.jpa.properties.hibernate.order_inserts=true
```

Tekshirish usuli oddiy: metod ichida `SELECT current_setting('transaction_read_only')` bajar va natijani ko'r. Taxmin qilma, o'lchab ko'r.

## 19.6 Ichki metod chaqiruvi tuzog'i va undan chiqish yo'llari

Proxy faqat tashqaridan kelgan chaqiruvni ushlaydi. Shuning uchun `this.saveAudit()` ko'rinishidagi ichki chaqiruvda `@Transactional` butunlay e'tiborsiz qoladi. Xuddi shu sabab `@Async`, `@Cacheable` va `@Retryable` da ham ishlaydi. Eng yomoni, xato jim: hech qanday ogohlantirish chiqmaydi, faqat tranzaksiya yo'q.

To'rtta chiqish yo'li bor. Metodni boshqa bean ga ko'chirish eng toza yechim va men shuni tanlayman. `TransactionTemplate` orqali chegarani kodda ochish ikkinchi tanlov, u ayniqsa loop ichida yaxshi. O'ziga `@Lazy` bilan inject qilish (self-injection) ishlaydi, lekin kodni o'qiyotgan odamni chalg'itadi. `@EnableTransactionManagement(mode = AdviceMode.ASPECTJ)` proxy muammosini butunlay yo'q qiladi, lekin build ga weaving qo'shadi va kichik loyiha uchun bu juda qimmat.

```java
@Service
public class ReportService {

    private final TransactionTemplate txTemplate;

    public void rebuildDaily(LocalDate day) {
        // XATO bo'lardi: this.persistChunk(...) -> proxy chetlab o'tiladi, tranzaksiya yo'q
        for (List<Row> chunk : partition(load(day), 500)) {
            // TO'G'RI: chegara aniq va ko'rinadigan joyda
            txTemplate.executeWithoutResult(status -> persistChunk(chunk));
        }
    }

    // @Transactional bu yerda keraksiz: chegarani txTemplate boshqaradi
    private void persistChunk(List<Row> chunk) {
        jdbcTemplate.batchUpdate("INSERT INTO report_daily(...) VALUES (?,?,?)", toArgs(chunk));
    }
}
```

## 19.7 Tranzaksiya uzunligi: tashqi HTTP chaqiruvni tranzaksiya ichiga qo'ymaslik

Tranzaksiya ochilgan paytdan commit gacha bitta connection band, PostgreSQL da `xmin` ushlanib turadi va yozilgan qatorlar ustidagi row lock saqlanadi. Shuning uchun tranzaksiya uzunligi arxitektura ko'rsatkichi. OLTP yo'lida maqsad: 50 ms dan kam, 200 ms dan oshmasin. Ichida tashqi HTTP chaqiruv bo'lsa, bu raqam to'lov gateway ining javob vaqtiga bog'lanib qoladi, ya'ni taxminan 300 ms dan 10 sekundgacha.

Hisob oddiy. 20 ta connection li pool, har bir tranzaksiya 2 sekund turadi. Demak tizim sekundiga 10 ta tranzaksiyadan ko'p bajara olmaydi. Gateway sekinlashsa, pool to'ladi, keyin HTTP thread lar `Connection is not available` bilan tushadi, keyin health check ham yiqiladi. Bitta tashqi servis sekinlashuvi butun dasturni o'ldiradi. Bu bog'lanishni faqat chegarani to'g'ri qo'yish uzadi.

```java
@Service
public class CheckoutService {

    // Hech qanday @Transactional yo'q: bu orkestrator metod
    public void checkout(Long orderId) {
        // 1-qadam: qisqa tranzaksiya, holatni PENDING ga o'tkazamiz
        Payment p = txTemplate.execute(s -> payments.markPending(orderId));

        // 2-qadam: tranzaksiyadan TASHQARIDA, connection band emas
        GatewayResult result = gateway.authorize(p.getExternalId(), p.getAmount());

        // 3-qadam: yana qisqa tranzaksiya, natijani yozamiz
        txTemplate.executeWithoutResult(s -> payments.applyResult(orderId, result));
    }
}
```

Bu uch qadamli shakl "tranzaksiya ichida tashqi chaqiruv yo'q" qoidasini kodda ko'rsatadi. Ikkinchi qadam uzilib qolsa, yozuv `PENDING` holatda qoladi va reconciliation jarayoni uni gateway dan so'rab aniqlaydi. Bu yerda idempotency key va holat mashinasi kerak bo'ladi, buni dizayn [patternlar hujjatidagi](../patterns/README.md) saga va idempotent receiver bo'limlari qoplaydi.

## 19.8 `TransactionSynchronization` va `@TransactionalEventListener` bilan commit dan keyin ish

Ko'p holatda ish commit dan keyin bajarilishi kerak: email yuborish, kesh tozalash, Kafka ga xabar qo'yish. Buni `@Transactional` metod ichida to'g'ridan to'g'ri qilsang, commit muvaffaqiyatsiz bo'lganda ham xabar ketgan bo'ladi. Spring ikki vosita beradi. Past daraja: `TransactionSynchronizationManager.registerSynchronization(new TransactionSynchronization() { ... })` va uning `afterCommit`, `afterCompletion` metodlari. Yuqori daraja: `ApplicationEventPublisher` bilan event chiqarish va `@TransactionalEventListener(phase = TransactionPhase.AFTER_COMMIT)`.

```java
@Service
public class ShipmentService {

    @Transactional
    public void confirm(Long orderId) {
        Shipment s = shipments.confirm(orderId);
        // Event tranzaksiya ichida chiqadi, listener commit dan keyin ishlaydi
        events.publishEvent(new ShipmentConfirmed(s.getId(), s.getTrackingNo()));
    }
}

@Component
public class ShipmentNotifier {

    @TransactionalEventListener(phase = TransactionPhase.AFTER_COMMIT)
    public void onConfirmed(ShipmentConfirmed e) {
        // Bu yerda yangi tranzaksiya YO'Q. DB ga yozish kerak bo'lsa aniq ochish shart.
        notifier.send(e.trackingNo());
    }

    @TransactionalEventListener(phase = TransactionPhase.AFTER_COMMIT)
    @Transactional(propagation = Propagation.REQUIRES_NEW)
    public void writeOutbox(ShipmentConfirmed e) {
        outbox.save(OutboxRecord.of(e)); // yangi tranzaksiya bilan yoziladi
    }
}
```

Ikki muhim detal. `AFTER_COMMIT` listener default holda yangi tranzaksiyada emas, shuning uchun u ichida DB ga yozish jim yo'qoladi; `REQUIRES_NEW` aniq kerak. Ikkinchi: `AFTER_COMMIT` listener istisno tashlasa, commit allaqachon bo'lgan, hech narsa qaytmaydi. Demak listener ichidagi ish o'z retry va o'z monitoringi bilan kelishi kerak.

## 19.9 Tranzaksiya va kesh, tranzaksiya va xabar yuborish nomuvofiqligi

Kesh va DB turli tizimlar, demak atomarlik yo'q. `@CacheEvict` default holda metod tugashi bilan ishlaydi, ya'ni commit dan oldin. Tranzaksiya keyin bekor bo'lsa, kesh allaqachon tozalangan va DB da eski ma'lumot. Teskari holda, kesh ga yangi qiymat yozilgan bo'lsa, DB rollback bo'lgandan keyin kesh butunlay yolg'on gapiradi. Spring da yechim `TransactionAwareCacheManagerProxy`: u yozuv va eviction ni commit gacha kutadi.

```java
@Bean
public CacheManager cacheManager(RedisConnectionFactory cf) {
    RedisCacheManager delegate = RedisCacheManager.builder(cf).build();
    // Kesh operatsiyalari faqat commit dan keyin qo'llanadi
    return new TransactionAwareCacheManagerProxy(delegate);
}
```

Xabar yuborishda ham xuddi shu nomuvofiqlik. Kafka ga `send` qilib keyin DB rollback bo'lsa, consumer mavjud bo'lmagan buyurtmani ko'radi. `AFTER_COMMIT` da yuborish bu muammoni kamaytiradi, lekin yo'q qilmaydi: commit bo'lgan, so'ng broker ga ulanish uzilgan bo'lsa xabar yo'qoladi. Yagona ishonchli yo'l xabarni DB ning o'zida, bitta tranzaksiyada jadvalga yozish va alohida jarayon bilan uzatish. Buning tafsilotlari dizayn [patternlar hujjatidagi](../patterns/README.md) transactional outbox bo'limida. Bu bobning hissasi bitta: xabarni tranzaksiya ichida broker ga yuborish har doim xato, va bu xato yuk oshganda ko'rinadi.

## 19.10 Timeout, lock kutish vaqti va deadlock bilan uchrashish

Spring ning `@Transactional(timeout = 3)` qiymati DB tomonidan majburlanmaydi. Spring uni `ResourceHolderSupport` da deadline sifatida saqlaydi va JDBC statement larga `setQueryTimeout` qo'yish orqali qo'llaydi. Agar vaqt tranzaksiya ichidagi Java kodida ketayotgan bo'lsa yoki statement allaqachon ketgan bo'lsa, u darhol to'xtamaydi. Qattiq kafolat PostgreSQL tomonida.

Uchta parametr muhim. `statement_timeout` bitta statement ni uzadi, OLTP uchun 3 dan 10 sekund oralig'i oqilona. `lock_timeout` lock kutishni cheklaydi, 1 dan 3 sekund yaxshi boshlang'ich qiymat, u deadlock ni kutmasdan tez xato beradi. `idle_in_transaction_session_timeout` ochiq qolib ketgan tranzaksiyani o'ldiradi, 30 sekunddan 60 sekundgacha. Deadlock ni PostgreSQL `deadlock_timeout` (default 1 sekund) dan keyin aniqlaydi va qurbonlardan birini `40P01` bilan uzadi.

```sql
-- Hisobot va batch roli uchun alohida chegaralar
ALTER ROLE report_user SET statement_timeout = '60s';
ALTER ROLE app_user   SET statement_timeout = '5s';
ALTER ROLE app_user   SET lock_timeout = '2s';
ALTER ROLE app_user   SET idle_in_transaction_session_timeout = '30s';

-- Kim kimni kutayotganini ko'rish: deadlock tahlilining birinchi qadami
SELECT a.pid, a.state, a.wait_event_type, a.wait_event,
       now() - a.xact_start AS tx_age, left(a.query, 60) AS q
  FROM pg_stat_activity a
 WHERE a.datname = current_database() AND a.xact_start IS NOT NULL
 ORDER BY tx_age DESC LIMIT 10;
```

Deadlock ning amaliy sababi deyarli har doim bitta: lock lar turli tartibda olinadi. Buyurtma qatorlarini `id` bo'yicha tartiblab yangilash, ya'ni `ORDER BY id FOR UPDATE`, deadlock ning katta qismini yo'q qiladi. Navbat jadvallarida `FOR UPDATE SKIP LOCKED` ishlatish esa kutishning o'zini yo'q qiladi.

| Tuzoq | Nima bo'ladi | Yechim |
| --- | --- | --- |
| Ichki `this.method()` chaqiruvi | Tranzaksiya jim ochilmaydi | Alohida bean yoki `TransactionTemplate` |
| Tashqi HTTP tranzaksiya ichida | Pool tugaydi, kaskad nosozlik | Chegarani uch qadamga bo'lish |
| Checked istisno | Kutilmagan commit, yarim ma'lumot | `rollbackFor = Exception.class` |
| Ichki `REQUIRED` da istisno tutildi | `UnexpectedRollbackException` | Ichki qismni `REQUIRES_NEW` qilish |
| `REQUIRES_NEW` loop ichida | Har iteratsiyada yangi connection | Chegarani loop tashqarisiga chiqarish |
| Kesh commit dan oldin tozalanadi | Kesh va DB mos emas | `TransactionAwareCacheManagerProxy` |
| `AFTER_COMMIT` da DB ga yozish | Yozuv jim yo'qoladi | Listener ga `REQUIRES_NEW` qo'shish |
| `@Transactional` + yangi thread | Tranzaksiya kontekst ko'chmaydi | Chegarani thread ichida ochish |
| Bitta ulkan batch tranzaksiya | WAL o'sadi, lock uzoq ushlanadi | 500-1000 qatorli chunk lar |
| `timeout` faqat Spring da | Statement DB da davom etadi | `statement_timeout`, `lock_timeout` |

## 19.11 Dasturiy tranzaksiya: `TransactionTemplate` qachon aniqroq

`@Transactional` deklarativ va shuning uchun ko'rinmas. `TransactionTemplate` esa chegarani kodda ko'rsatadi. Uni to'rt holatda tanlaymiz. Birinchi: bitta metod ichida bir nechta mustaqil tranzaksiya kerak bo'lganda, masalan chunk lar bo'yicha yurganda. Ikkinchi: tranzaksiya chegarasi shartga bog'liq bo'lganda. Uchinchi: retry mantig'i tranzaksiyani to'liq qamrab olishi kerak bo'lganda. To'rtinchi: proxy muammosidan qochish kerak bo'lganda.

```java
@Service
public class StockAdjuster {

    private final TransactionTemplate tx;

    // Serialization xatosida retry: tranzaksiya har urinishda qaytadan ochiladi
    public void adjust(String sku, int delta) {
        for (int attempt = 1; attempt <= 3; attempt++) {
            try {
                tx.executeWithoutResult(s -> stockRepo.applyDelta(sku, delta));
                return;
            } catch (ConcurrencyFailureException e) { // 40001 yoki 40P01
                // Taxminan 50 ms dan boshlab eksponensial kutish
                sleepQuietly(50L * attempt);
            }
        }
        throw new StockAdjustmentFailedException(sku);
    }
}
```

E'tibor ber: `@Transactional` va `@Retryable` ni bitta metodga qo'yish ishlamaydi, chunki retry tranzaksiya ichida qoladi va bekor qilingan tranzaksiyani qayta ishlatadi. Tartib muhim: retry tashqarida, tranzaksiya ichkarida.

## 19.12 Katta batch operatsiyalarda tranzaksiya chegarasini tanlash

Million qatorlik hisobotni bitta tranzaksiyada yozish bir necha narsani buzadi. WAL o'sadi, autovacuum eski versiyalarni tozalay olmaydi, connection soatlab band bo'ladi, va xato chiqsa butun ish nolga qaytadi. To'g'ri shakl: chunk lar, har biri o'z tranzaksiyasida, va qayerga yetganini saqlab turadigan checkpoint. 500 dan 1000 qatorgacha chunk ko'pchilik holatda yaxshi muvozanat beradi.

JPA bilan batch yozishda `EntityManager` ni vaqti-vaqti bilan `flush()` va `clear()` qilish shart, aks holda persistence context o'sib xotirani yeydi. Agar entity hayotiy sikli kerak bo'lmasa, Hibernate ning `StatelessSession` i yoki to'g'ridan to'g'ri `JdbcTemplate.batchUpdate` ancha tezroq: taxminan 3 dan 10 barobargacha.

```java
@Service
public class InvoiceImporter {

    @PersistenceContext private EntityManager em;
    private final TransactionTemplate tx;

    public void importAll(Iterator<InvoiceRow> rows) {
        List<InvoiceRow> chunk = new ArrayList<>(500);
        while (rows.hasNext()) {
            chunk.add(rows.next());
            if (chunk.size() == 500) { flushChunk(List.copyOf(chunk)); chunk.clear(); }
        }
        if (!chunk.isEmpty()) flushChunk(chunk);
    }

    private void flushChunk(List<InvoiceRow> chunk) {
        tx.executeWithoutResult(s -> {
            for (InvoiceRow r : chunk) em.persist(Invoice.from(r));
            em.flush();  // SQL ni DB ga yuboramiz
            em.clear();  // persistence context ni bo'shatamiz, xotira o'smaydi
        });
    }
}
```

| Savol | Oddiy yondashuv | Arxitektor yondashuvi |
| --- | --- | --- |
| Chegara qayerda | Service ning har metodida `@Transactional` | Chegara biznes operatsiyasi bo'yicha, orkestrator tranzaksiyasiz |
| Tashqi chaqiruv | Tranzaksiya ichida qulay bo'lgani uchun | Tranzaksiyadan tashqarida, holat mashinasi bilan |
| Istisno siyosati | Default qoldiriladi | `rollbackFor` aniq, domen istisnolari runtime |
| Isolation | Muammo chiqsa `SERIALIZABLE` ga ko'tariladi | `READ COMMITTED` + atomar `UPDATE ... WHERE` |
| Timeout | `@Transactional(timeout = ...)` yetarli deb o'ylanadi | DB rolida `statement_timeout`, `lock_timeout` |
| Commit dan keyingi ish | Metod oxirida darhol bajariladi | `AFTER_COMMIT` listener yoki outbox jadvali |
| Kesh | `@CacheEvict` ga ishoniladi | Tranzaksiyaga bog'langan cache manager |
| Batch | Bitta katta tranzaksiya | 500-1000 qatorli chunk va checkpoint |
| Retry | `@Retryable` tranzaksiya ichida | Retry tashqarida, `40001` ga aniq ishlov |
| Nazorat | Xato chiqsa log qaraladi | Tranzaksiya davomiyligi metrikasi va uzoq tranzaksiya alerti |

Testlashda arxitektor uchta narsani tekshiradi: rollback haqiqatan sodir bo'ladimi, `AFTER_COMMIT` listener chaqiriladimi, va parallel ikki tranzaksiya kutilgan natija beradimi. Buning texnikasi [testlash qo'llanmasidagi](../testing/README.md) tranzaksiya testlari bo'limida.

## 19.13 Amalda qo'llash

- [ ] Loyihadagi barcha `@Transactional` metodlarni ro'yxatla va ichida tashqi HTTP yoki broker chaqiruvi borlarini ajratib, uch qadamli shaklga ko'chir.
- [ ] `rollbackFor = Exception.class` siyosatini kelishib ol yoki biznes istisnolarini `RuntimeException` dan meros qilib qayta qur.
- [ ] `app_user` va `report_user` rollariga alohida `statement_timeout`, `lock_timeout` va `idle_in_transaction_session_timeout` qiymatlarini qo'y.
- [ ] `pg_stat_activity` asosida 5 sekunddan uzoq ochiq tranzaksiyalar uchun alert yarat va bir hafta kuzat.
- [ ] `CacheManager` ni `TransactionAwareCacheManagerProxy` ga o'ra va kesh bilan DB nomuvofiqligini qayta tekshir.
- [ ] Broker ga tranzaksiya ichida yuborilayotgan har bir xabarni outbox jadvaliga ko'chirish rejasini tuz.
- [ ] Barcha batch va import joblarini 500-1000 qatorli chunk tranzaksiyalariga bo'lib, qayerga yetganini saqlaydigan checkpoint qo'sh.
- [ ] `40001` va `40P01` xatolari uchun tranzaksiyadan tashqaridagi retry ni `TransactionTemplate` bilan joylashtir va urinishlar sonini metrika sifatida chiqar.

---

[&larr; 18. Spring Data JPA va Hibernate chuqur](18-spring-data-jpa-va-hibernate-chuqur.md) · [Mundarija](README.md) · [20. Spring Security: filter chain, OAuth2, JWT &rarr;](20-spring-security-filter-chain-oauth2-jwt.md)
