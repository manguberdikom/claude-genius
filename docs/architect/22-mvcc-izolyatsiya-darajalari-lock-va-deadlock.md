<!-- doc: architect | chapter: 22 | part: IV. PostgreSQL chuqur bilim -->

[Barcha hujjatlar](../../README.md) / [Arxitektor miyasi](README.md)

# 22. MVCC, izolyatsiya darajalari, lock va deadlock (MVCC and Isolation)

<details>
<summary>Bu bobdagi 12 bo'lim</summary>

- [22.1 MVCC mexanikasi: `xmin`, `xmax`, snapshot va ko'rinuvchanlik qoidasi](#221-mvcc-mexanikasi-xmin-xmax-snapshot-va-korinuvchanlik-qoidasi)
- [22.2 PostgreSQL da Read Committed haqiqatda qanday ishlaydi](#222-postgresql-da-read-committed-haqiqatda-qanday-ishlaydi)
- [22.3 Repeatable Read va serialization xatosi, qayta urinish zarurati](#223-repeatable-read-va-serialization-xatosi-qayta-urinish-zarurati)
- [22.4 Serializable izolyatsiya: predikat lock va uning narxi](#224-serializable-izolyatsiya-predikat-lock-va-uning-narxi)
- [22.5 Yo'qolgan yangilanish (lost update) va uni oldini olish usullari](#225-yoqolgan-yangilanish-lost-update-va-uni-oldini-olish-usullari)
- [22.6 Qator darajasidagi lock: `FOR UPDATE`, `FOR NO KEY UPDATE`, `SKIP LOCKED`](#226-qator-darajasidagi-lock-for-update-for-no-key-update-skip-locked)
- [22.7 Jadval darajasidagi lock turlari va DDL ning lock talabi](#227-jadval-darajasidagi-lock-turlari-va-ddl-ning-lock-talabi)
- [22.8 Deadlock qanday yuzaga keladi, log da qanday ko'rinadi, qanday oldini olinadi](#228-deadlock-qanday-yuzaga-keladi-log-da-qanday-korinadi-qanday-oldini-olinadi)
- [22.9 Uzoq ochiq tranzaksiya: vacuum ni to'xtatishi va bloat keltirishi](#229-uzoq-ochiq-tranzaksiya-vacuum-ni-toxtatishi-va-bloat-keltirishi)
- [22.10 `pg_locks` va `pg_stat_activity` bilan bloklanishni topish](#2210-pg_locks-va-pg_stat_activity-bilan-bloklanishni-topish)
- [22.11 Navbat jadvali qurish: `SKIP LOCKED` bilan ishonchli ishlov berish](#2211-navbat-jadvali-qurish-skip-locked-bilan-ishonchli-ishlov-berish)
- [22.12 Amalda qo'llash](#2212-amalda-qollash)

</details>



Tranzaksiya izolyatsiyasi arxitektor uchun eng ko'p pul yo'qotadigan joy. Buyurtma ikki marta to'lanadi, ombor qoldig'i manfiy bo'ladi, hisobot jami summasi balansga to'g'ri kelmaydi. Bu xatolar testda ko'rinmaydi, chunki bitta sessiyada hamma narsa ishlaydi. Shu bob PostgreSQL ichida aniq nima sodir bo'layotganini va shu mexanikadan qanday qaror chiqarishni ko'rsatadi.

## 22.1 MVCC mexanikasi: `xmin`, `xmax`, snapshot va ko'rinuvchanlik qoidasi

PostgreSQL da `UPDATE` hech qachon qatorni joyida o'zgartirmaydi. U yangi versiya (tuple) yozadi va eskisini o'lgan deb belgilaydi. Har bir tuple da yashirin ustunlar bor: `xmin` ya'ni qaysi tranzaksiya bu versiyani yaratgan, `xmax` ya'ni qaysi tranzaksiya uni o'chirgan yoki yangilagan, `ctid` ya'ni jismoniy manzil.

Snapshot ichida uch narsa bor: pastki chegara, yuqori chegara va shu paytda ochiq tranzaksiyalar ro'yxati. Tuple ko'rinadi, agar `xmin` tranzaksiyasi commit qilgan va snapshot dan oldin tugagan bo'lsa, va `xmax` yo bo'sh, yo abort qilgan, yo snapshot dan keyin tugagan bo'lsa.

```sql
CREATE TABLE payment (id bigserial PRIMARY KEY, amount numeric, status text);
INSERT INTO payment (amount, status) VALUES (100, 'NEW');

SELECT ctid, xmin, xmax, status FROM payment;
--  (0,1) | 812 | 0 | NEW

UPDATE payment SET status = 'PAID' WHERE id = 1;

-- eski versiya diskda qoldi, yangi versiya yangi ctid oldi
SELECT ctid, xmin, xmax, status FROM payment;
--  (0,2) | 813 | 0 | PAID

-- o'lik versiyalar soni statistikada ko'rinadi
SELECT n_live_tup, n_dead_tup FROM pg_stat_user_tables
WHERE relname = 'payment';
```

Shundan ikki xulosa chiqadi. Birinchi: `UPDATE` narxi `INSERT` ga yaqin, chunki yangi tuple va unga tegishli hamma index yozuvi yangilanadi. Istisno HOT update: yangilangan ustunlar bironta ham index da bo'lmasa va sahifada joy bo'lsa, index tegilmaydi. Shuning uchun tez-tez yangilanadigan `last_seen_at` ga index qo'yish katta xato.

Ikkinchi: o'lik tuple lar o'zidan o'zi yo'qolmaydi, ularni `VACUUM` tozalaydi. Va `VACUUM` eng qadimgi ochiq snapshot dan keyingi hech narsani tozalay olmaydi.

## 22.2 PostgreSQL da Read Committed haqiqatda qanday ishlaydi

Read Committed default izolyatsiya. Ko'pchilik uni "commit qilingan ma'lumotni o'qiydi" deb biladi va shu bilan to'xtaydi. Mexanika boshqacha: har bir statement O'ZIGA yangi snapshot oladi. Bitta tranzaksiya ichidagi ikki `SELECT` turli natija qaytarishi normal holat.

Eng nozik joy `UPDATE` da. Kutilayotgan qatorni boshqa tranzaksiya o'zgartirib commit qilsa, PostgreSQL abort qilmaydi: u eng yangi versiyani oladi va `WHERE` shartini qayta tekshiradi. Buni EvalPlanQual deb ataladi.

```sql
-- SESSIYA A                          -- SESSIYA B
BEGIN;                                BEGIN;
UPDATE stock SET qty = qty - 1
  WHERE sku = 'SKU-1' AND qty > 0;
-- 1 qator, qator lock olindi
                                      UPDATE stock SET qty = qty - 1
                                        WHERE sku = 'SKU-1' AND qty > 0;
                                      -- B bloklangan, kutadi
COMMIT;
                                      -- B yangi versiyani oldi, WHERE qayta
                                      -- tekshirildi: qty hali > 0, UPDATE 1
                                      COMMIT;
```

Bu yerda `qty = qty - 1` ko'rinishi qutqardi, chunki yangi qiymatdan hisoblandi. Agar kod Java da hisoblangan tayyor qiymat yozsa, B ning yozuvi A ning ustidan bosadi va bitta birlik qoldiq yo'qoladi. Shu farq lost update ning asosi.

Yana bir tuzoq: yangi versiyada `WHERE` to'g'ri kelmasa, `UPDATE 0` qaytadi va hech qanday xato bo'lmaydi. Java kodi affected rows ni tekshirmasa, jim ravishda hech narsa yangilanmaydi.

```java
@Modifying
@Query("""
    update Stock s set s.qty = s.qty - :n
    where s.sku = :sku and s.qty >= :n
    """)
int reserve(String sku, int n);

// chaqiruvchi joy: affected rows majburiy tekshiriladi
int updated = stockRepository.reserve(sku, qty);
if (updated == 0) {
    throw new InsufficientStockException(sku);  // qoldiq yetmadi
}
```

## 22.3 Repeatable Read va serialization xatosi, qayta urinish zarurati

Repeatable Read da snapshot tranzaksiya boshida olinadi va oxirigacha o'zgarmaydi, hamma `SELECT` bir xil holatni ko'radi. Hisobot va ko'p bosqichli o'qish uchun ideal.

Yozishda narx paydo bo'ladi. Agar snapshot olgandan keyin boshqa kim o'zgartirgan qatorni yangilamoqchi bo'lsangiz, EvalPlanQual ishlamaydi va `40001` keladi: `could not serialize access due to concurrent update`. Tranzaksiya butunlay bekor bo'ladi.

Qoida: Repeatable Read yoki Serializable ishlatgan har bir yozuv yo'li qayta urinish mantiqiga ega bo'lishi shart. Retry tranzaksiyadan TASHQARIDA turishi kerak, chunki abort qilingan tranzaksiya ichida hech narsa qilib bo'lmaydi.

```java
@Service
public class SettlementRunner {
    private final SettlementService service;  // @Transactional shu ichida

    public void runWithRetry(long batchId) {
        int attempt = 0;
        while (true) {
            try {
                service.settle(batchId);     // har urinishda yangi tranzaksiya
                return;
            } catch (CannotSerializeTransactionException
                     | CannotAcquireLockException e) {
                if (++attempt >= 5) throw e;
                sleepQuiet(20L * (1L << (attempt - 1)));  // 20ms..320ms
            }
        }
    }
}
```

Spring da izolyatsiya `@Transactional(isolation = Isolation.REPEATABLE_READ)` bilan beriladi. Hibernate ning `@Version` optimistic locking ham aynan shunday retry talab qiladi.

## 22.4 Serializable izolyatsiya: predikat lock va uning narxi

Serializable PostgreSQL da Serializable Snapshot Isolation orqali amalga oshirilgan. U bloklamaydi va o'qishni sekinlashtirmaydi. U o'qish va yozish bog'liqliklarini kuzatadi, natija hech qanday ketma-ket bajarilishga to'g'ri kelmasa, tranzaksiyalardan birini `40001` bilan abort qiladi.

Kuzatish predikat lock orqali ketadi. `WHERE account_id = 7` bajarilsa, shu predikat eslab qolinadi, boshqa tranzaksiya unga tushadigan qator yozsa konflikt qayd etiladi. Predikat lock index darajasida bo'ladi, shuning uchun index borligi aniqlikka ta'sir qiladi: sequential scan da butun jadval kuzatiladi va yolg'on konflikt soni keskin oshadi.

```sql
-- write skew: mijozning jami balansi musbat qolishi kerak
-- SESSIYA A                                -- SESSIYA B
BEGIN ISOLATION LEVEL SERIALIZABLE;         BEGIN ISOLATION LEVEL SERIALIZABLE;
SELECT sum(balance) FROM account
  WHERE customer_id = 7;  -- 100
                                            SELECT sum(balance) FROM account
                                              WHERE customer_id = 7;  -- 100
UPDATE account SET balance = balance - 100
  WHERE id = 71;
                                            UPDATE account SET balance = balance - 100
                                              WHERE id = 72;
COMMIT;  -- muvaffaqiyat
                                            COMMIT;
-- ERROR: could not serialize access due to read/write dependencies
-- HINT: The transaction might succeed if retried.
```

Narxi uchta. Birinchi: SSI holati xotira talab qiladi, `max_pred_locks_per_transaction` default 64 va yetmasa lock sahifa yoki relation darajasiga ko'tariladi, aniqlik yo'qoladi. Ikkinchi: abort darajasi yuklama bilan o'sadi, hot qatorga ko'p yozuv tushsa 10 foizdan ortiq abort bo'lishi mumkin. Uchinchi: yashirin retry hisobiga latency oshadi.

Arxitektor qarori: Serializable ni butun ilovaga qo'ymang, faqat invariant haqiqatan global bo'lgan bir-ikki yo'lga qo'ying, masalan kredit limitini tekshirish. Qolgan joyda Read Committed plus aniq lock arzonroq va bashoratliroq.

## 22.5 Yo'qolgan yangilanish (lost update) va uni oldini olish usullari

Sxema bitta: ikki tranzaksiya bir qatorni o'qiydi, har biri Java da hisoblaydi, ikkisi ham yozadi, ikkinchisi birinchisini yo'q qiladi. Read Committed da bu hech qanday xato bermaydi.

To'rt yechim bor. Birinchi: hisoblashni SQL ichiga ko'chirish, `qty = qty - :n`, eng arzon. Ikkinchi: `@Version` optimistic locking. Uchinchi: `SELECT ... FOR UPDATE` pessimistic locking. To'rtinchi: izolyatsiyani ko'tarish plus retry.

```java
@Entity
public class Order {
    @Id private Long id;
    @Version private long version;   // Hibernate o'zi WHERE ga qo'shadi
    private BigDecimal total;
}

public interface StockRepository extends JpaRepository<Stock, Long> {
    @Lock(LockModeType.PESSIMISTIC_WRITE)   // SELECT ... FOR UPDATE
    Optional<Stock> findBySku(String sku);
}
```

Tanlov qoidasi: konflikt ehtimoli past bo'lsa optimistic, chunki kutish yo'q. Konflikt deyarli har safar bo'lsa, masalan bir xil ombor qatoriga yuzlab buyurtma, pessimistic kerak, aks holda retry bo'roni boshlanadi va throughput tushadi.

## 22.6 Qator darajasidagi lock: `FOR UPDATE`, `FOR NO KEY UPDATE`, `SKIP LOCKED`

`FOR UPDATE` eng kuchli qator lock i. U boshqa `FOR UPDATE`, `FOR SHARE`, `UPDATE` va `DELETE` ni bloklaydi. Nozik joyi: u shu qatorga foreign key qo'yadigan child insert ni ham bloklaydi.

`FOR NO KEY UPDATE` kuchsizroq. U key ustunlari o'zgarmasligini bildiradi, shuning uchun FK tekshiruvi bilan birga yashay oladi. Oddiy `UPDATE` o'zi default shu lock ni oladi. Parent qatorni non-key ustun uchun lock qilsangiz, shu variant child insert larni bekorga to'xtatmaydi.

```sql
-- interaktiv UI: kutish o'rniga darhol xato
SELECT * FROM invoice WHERE id = 42 FOR UPDATE NOWAIT;
-- ERROR: could not obtain lock on row ...  (SQLSTATE 55P03)

-- batch worker: band qatorlarni jimgina tashlab ketish
BEGIN;
SELECT id FROM invoice WHERE status = 'DRAFT'
ORDER BY id LIMIT 10 FOR UPDATE SKIP LOCKED;
COMMIT;
```

Advisory lock alohida mexanizm. `pg_advisory_xact_lock(key)` tranzaksiya oxirida o'zi bo'shaydi, `pg_advisory_lock(key)` sessiya oxirigacha turadi. Ikkinchisi connection pool bilan xavfli, chunki connection pool ga qaytganda lock qolib ketadi. Spring da faqat birinchi variantni ishlatish qoidasi bo'lsin.

## 22.7 Jadval darajasidagi lock turlari va DDL ning lock talabi

Jadval lock lari sakkiz turga bo'linadi, amalda uchtasi yetadi. `ACCESS SHARE` ni `SELECT` oladi. `ROW EXCLUSIVE` ni `INSERT`, `UPDATE`, `DELETE` oladi. `ACCESS EXCLUSIVE` ni `ALTER TABLE`, `DROP`, `TRUNCATE`, `VACUUM FULL`, `REINDEX` oladi va u hamma narsa bilan konflikt qiladi, hatto `SELECT` bilan.

Shundan produksiyadagi eng xavfli ketma-ketlik chiqadi. `ALTER TABLE` lock kutadi, u kutayotganda ortidan kelgan `SELECT` lar ham navbatga tushadi, chunki lock navbati FIFO. Natijada bitta uzun `SELECT` tufayli butun jadval bir necha daqiqa o'lik bo'ladi.

```sql
SET lock_timeout = '3s';          -- migratsiyada MAJBURIY
SET statement_timeout = '30s';

-- ustun qo'shish metadata-only, DEFAULT bilan ham jadval qayta yozilmaydi
ALTER TABLE orders ADD COLUMN channel text NOT NULL DEFAULT 'WEB';

-- NOT NULL cheklov ikki qadamda, uzun lock siz
ALTER TABLE orders ADD CONSTRAINT orders_ch_nn
  CHECK (channel IS NOT NULL) NOT VALID;
ALTER TABLE orders VALIDATE CONSTRAINT orders_ch_nn;

-- index: hech qachon oddiy CREATE INDEX emas
CREATE INDEX CONCURRENTLY idx_orders_channel ON orders (channel);
-- CONCURRENTLY tranzaksiya ichida ishlamaydi va xato bo'lsa INVALID
-- index qoldiradi, uni DROP INDEX CONCURRENTLY bilan tozalash kerak
```

`lock_timeout` ni migratsiyada majburiy qilish arxitektura qarori: 3 soniyada ololmasa migratsiya tushadi va keyin qayta urinadi, bu butun ilovaning o'lishidan yaxshi.

## 22.8 Deadlock qanday yuzaga keladi, log da qanday ko'rinadi, qanday oldini olinadi

Shart bitta: ikki tranzaksiya resurslarni teskari tartibda lock qiladi. PostgreSQL buni o'zi topadi: `deadlock_timeout` (default 1 soniya) o'tgach kutish grafigini tekshiradi, tsikl topsa biror tranzaksiyani `40P01` bilan o'ldiradi.

```text
ERROR:  deadlock detected
DETAIL:  Process 2841 waits for ShareLock on transaction 9123; blocked by process 2902.
         Process 2902 waits for ShareLock on transaction 9124; blocked by process 2841.
         Process 2841: UPDATE account SET balance = balance - 50 WHERE id = 2;
         Process 2902: UPDATE account SET balance = balance - 50 WHERE id = 1;
CONTEXT:  while updating tuple (0,14) in relation "account"
```

Oldini olishning uch usuli. Birinchi va eng kuchli: har doim bir xil tartibda lock qilish. Ikkinchi: `IN (...)` ro'yxatiga tayanmaslik, chunki ichki tartib kafolatlanmaydi, `ORDER BY` plus `FOR UPDATE` ishlatish. Uchinchi: tranzaksiyani qisqa tutish.

```java
@Transactional
public void transfer(long fromId, long toId, BigDecimal amount) {
    // lock tartibi id bo'yicha, deadlock tuzilmaviy yo'q qilindi
    List<Long> ids = Stream.of(fromId, toId).sorted().toList();
    List<Account> locked = accountRepository.lockOrdered(ids);

    Account from = pick(locked, fromId);
    Account to   = pick(locked, toId);
    if (from.getBalance().compareTo(amount) < 0) throw new InsufficientFunds();
    from.debit(amount);
    to.credit(amount);
}
// lockOrdered ichidagi SQL:
// select * from account where id = any(:ids) order by id for update
```

## 22.9 Uzoq ochiq tranzaksiya: vacuum ni to'xtatishi va bloat keltirishi

Bu bobdagi eng qimmat tuzoq. `VACUUM` o'lik tuple ni faqat hech kim ko'rmasligi aniq bo'lsa tozalaydi, bu esa eng qadimgi ochiq snapshot bilan aniqlanadi. Bitta `idle in transaction` sessiya soatlab turib butun bazadagi tozalashni to'xtatadi.

Zanjir shunday: o'lik tuple soni o'sadi, jadval va index hajmi o'sadi, scan sekinlashadi, shared buffers o'lik sahifa saqlaydi, statistika eskiradi, so'rov rejasi buziladi. 2 GB jadval ikki kunda 20 GB bo'lishi real hodisa.

Eng ko'p uchraydigan sabab Java tomonida: `@Transactional` metod ichida HTTP chaqiruv turadi, tranzaksiya 50 ms emas, 8 soniya yashaydi. Ikkinchi sabab: `readOnly` hisobot tranzaksiyasi butun pagination tsiklini o'rab olgan.

```sql
-- global himoya, buzilgan kodni oshkor qiladi
ALTER SYSTEM SET idle_in_transaction_session_timeout = '60s';
ALTER SYSTEM SET statement_timeout = '30s';
ALTER SYSTEM SET log_lock_waits = on;
SELECT pg_reload_conf();

-- eng qadimgi xavfli sessiyalar
SELECT pid, state, now() - xact_start AS xact_age,
       now() - state_change AS idle_age, left(query, 50) AS q
FROM pg_stat_activity
WHERE xact_start IS NOT NULL AND now() - xact_start > interval '1 minute'
ORDER BY xact_start;
```

## 22.10 `pg_locks` va `pg_stat_activity` bilan bloklanishni topish

Hodisa paytida birinchi savol: kim kimni bloklayapti. Eng tez javob `pg_blocking_pids()` dan keladi.

```sql
SELECT w.pid AS kutayotgan, b.pid AS bloklovchi, b.state,
       now() - b.xact_start AS bloklovchi_yoshi,
       left(b.query, 40) AS bloklovchi_q
FROM pg_stat_activity w
JOIN pg_stat_activity b ON b.pid = ANY (pg_blocking_pids(w.pid))
WHERE w.wait_event_type = 'Lock'
ORDER BY bloklovchi_yoshi DESC;

-- kutilayotgan lock lar
SELECT locktype, relation::regclass, mode, pid
FROM pg_locks WHERE NOT granted ORDER BY pid;

SELECT pg_cancel_backend(2902);     -- avval so'rovni bekor qilish
SELECT pg_terminate_backend(2902);  -- oxirgi chora, sessiyani uzish
```

Monitoringda ikki metrikani alertga qo'ying: `wait_event_type = 'Lock'` bo'lgan sessiyalar soni va eng uzun ochiq tranzaksiya yoshi. `log_lock_waits = on` bilan 1 soniyadan uzun kutishlar log ga tushadi.

## 22.11 Navbat jadvali qurish: `SKIP LOCKED` bilan ishonchli ishlov berish

PostgreSQL navbat uchun yaxshi vosita, agar to'g'ri yozilsa. `FOR UPDATE SKIP LOCKED` bilan worker lar bir-birini kutmaydi va bir xil ishni ikki marta olmaydi.

```sql
CREATE TABLE outbox_job (
  id bigserial PRIMARY KEY, payload jsonb NOT NULL,
  status text NOT NULL DEFAULT 'READY', attempts int NOT NULL DEFAULT 0,
  run_after timestamptz NOT NULL DEFAULT now(), locked_at timestamptz
);
-- faqat ishlanishi kerak bo'lgan qatorlar index da
CREATE INDEX idx_outbox_ready ON outbox_job (run_after, id)
  WHERE status = 'READY';

-- tanlash va belgilash bitta atomik statement da
UPDATE outbox_job j
SET status = 'IN_PROGRESS', locked_at = now(), attempts = attempts + 1
FROM (
  SELECT id FROM outbox_job
  WHERE status = 'READY' AND run_after <= now()
  ORDER BY run_after, id LIMIT 20
  FOR UPDATE SKIP LOCKED
) AS picked
WHERE j.id = picked.id
RETURNING j.id, j.payload;
```

Uch qoida. Birinchi: partial index shart, aks holda navbat o'sgani sari olish so'rovi sekinlashadi. Ikkinchi: reaper kerak, chunki worker o'lsa status qaytmaydi, `locked_at` 5 daqiqadan oshganlarni `READY` ga qaytaradi. Uchinchi: ishlangan qatorni o'chirish yoki arxivga ko'chirish kerak, `DONE` holida qoldirsangiz jadval cheksiz o'sadi.

Hajm chegarasini bilib turing: bitta PostgreSQL navbat taxminan minutda 10 mingdan 50 minggacha ish uchun qulay, undan yuqorisida Kafka kerak. Lekin outbox uchun (dizayn [patternlar hujjatidagi](../patterns/README.md) outbox pattern) shu jadval to'g'ri tanlov, chunki u biznes yozuvi bilan bir tranzaksiyada turadi.

| Tuzoq | Nima sodir bo'ladi | Yechim |
|---|---|---|
| Java da qiymatni hisoblab yozish | Lost update, qoldiq yo'qoladi | SQL ichida `qty = qty - :n` |
| Affected rows ni tekshirmaslik | `UPDATE 0` jim o'tadi | 0 holatida biznes exception |
| Repeatable Read ni retry siz ishlatish | `40001` foydalanuvchiga 500 bo'ladi | Tranzaksiyadan tashqarida retry |
| `@Transactional` ichida HTTP chaqiruv | Vacuum to'xtaydi, bloat o'sadi | I/O ni tranzaksiyadan chiqarish |
| `CREATE INDEX` CONCURRENTLY siz | Jadval yozishga yopiq | `CREATE INDEX CONCURRENTLY` |
| `ALTER TABLE` ni `lock_timeout` siz | Navbat yig'iladi, `SELECT` ham o'ladi | `SET lock_timeout = '3s'` |
| Lock larni turli tartibda olish | Deadlock, `40P01` | `ORDER BY id ... FOR UPDATE` |
| Sessiya advisory lock plus pool | Lock connection da qolib ketadi | Tranzaksiyaga bog'langan variant |
| Navbatda partial index yo'q | Olish so'rovi sekinlashadi | `WHERE status = 'READY'` index |

| Savol | Oddiy yondashuv | Arxitektor yondashuvi |
|---|---|---|
| Izolyatsiya tanlash | Hamma joyda default | Yo'l bo'yicha: hisobotga Repeatable Read, invariantga Serializable |
| Lost update | "Baza o'zi hal qiladi" | Atomik `UPDATE`, `@Version` yoki `FOR UPDATE` ni ongli tanlash |
| Serialization xatosi | Stack trace ni log ga tashlaydi | Idempotent retry, urinish soni o'lchanadi |
| Lock turi | Har joyda `FOR UPDATE` | Konflikt profiliga qarab `FOR NO KEY UPDATE` yoki `SKIP LOCKED` |
| DDL deploy | Migratsiyani ish vaqtida yuboradi | `lock_timeout`, `CONCURRENTLY`, ikki qadamli cheklov |
| Deadlock | Retry qo'shib unutadi | Lock tartibini tuzilmaviy majburlaydi, retry ikkinchi himoya |
| Uzun tranzaksiya | Sezmaydi | Timeout plus tranzaksiya yoshi alerti |
| Diagnostika | `pg_stat_activity` ni qo'lda ko'radi | `pg_blocking_pids` dashboard, `log_lock_waits = on` |
| Navbat | `SELECT` plus `UPDATE` ikki qadamda | Bitta atomik statement plus reaper |

## 22.12 Amalda qo'llash

- [ ] Hamma yozuv yo'llarini ro'yxatlab chiq va har biri lost update dan nima bilan himoyalanganini yoz. Himoyasiz yo'llarni darhol tuzat.
- [ ] Har bir shartli `UPDATE` ning affected rows ini tekshirishni majburiy qil va 0 holatida aniq biznes exception tashla.
- [ ] Repeatable Read yoki Serializable ishlatadigan yo'llarga tranzaksiyadan tashqarida 3-5 urinishli retry qo'y va urinish sonini metrika qilib chiqar.
- [ ] `@Transactional` metodlar ichidagi hamma tashqi HTTP, fayl va queue chaqiruvini audit qilib, tranzaksiyadan tashqariga ko'chir.
- [ ] Bazada `idle_in_transaction_session_timeout = 60s`, `statement_timeout = 30s`, `log_lock_waits = on` ni yoq va eng uzun ochiq tranzaksiya yoshiga alert qo'y.
- [ ] Migratsiya shabloniga `SET lock_timeout = '3s'` ni majburiy qator sifatida kirit va index yaratishni faqat `CONCURRENTLY` bilan ruxsat et.
- [ ] Pul yoki qoldiq o'zgartiradigan kodda lock lar `id` bo'yicha saralangan tartibda olinishini tekshir va buni test bilan qotir.
- [ ] Navbat jadvaliga partial index, `SKIP LOCKED` bilan atomik olish va qolib ketgan ishlar uchun reaper job qo'sh.

---

[&larr; 21. PostgreSQL arxitekturasi: process model, WAL, checkpoint, vacuum](21-postgresql-arxitekturasi-process-model-wal.md) · [Mundarija](README.md) · [23. Indekslar: B-tree, GIN, GiST, BRIN va tanlov &rarr;](23-indekslar-b-tree-gin-gist-brin-va-tanlov.md)
