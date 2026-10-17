<!-- doc: architect | chapter: 22 | part: IV. PostgreSQL chuqur bilim -->

[Barcha hujjatlar](../../README.md) / [Arxitektor miyasi](README.md)

> Holat: tekshirilmoqda. Da'volar hali manbaga solishtirilmoqda.

# 22. MVCC, izolyatsiya darajalari, lock va deadlock (MVCC and Isolation)

<details>
<summary>Bu bobdagi 17 bo'lim</summary>

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
- [22.12 ACID ta'rifi nega noaniq va anomaliyalar taksonomiyasi](#2212-acid-tarifi-nega-noaniq-va-anomaliyalar-taksonomiyasi)
- [22.13 Bir obyektli va ko'p obyektli operatsiya: atomiklik qayerda tugaydi](#2213-bir-obyektli-va-kop-obyektli-operatsiya-atomiklik-qayerda-tugaydi)
- [22.14 Fantomni lock obyektiga aylantirish: materializing conflicts](#2214-fantomni-lock-obyektiga-aylantirish-materializing-conflicts)
- [22.15 Serializability ga uch yo'l va PostgreSQL faqat bittasini beradi](#2215-serializability-ga-uch-yol-va-postgresql-faqat-bittasini-beradi)
- [22.16 `PREPARE TRANSACTION`: shubhadagi tranzaksiya lock ni ushlab turadi](#2216-prepare-transaction-shubhadagi-tranzaksiya-lock-ni-ushlab-turadi)
- [22.17 Amalda qo'llash](#2217-amalda-qollash)

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

Repeatable Read da snapshot bir marta olinadi va tranzaksiya oxirigacha o'zgarmaydi, hamma `SELECT` bir xil holatni ko'radi. Aniq payti muhim: snapshot `BEGIN` da emas, tranzaksiyadagi **birinchi** statementda (tranzaksiyani boshqaruvchi buyruqlardan boshqasida) olinadi. Shu sababli `BEGIN` dan keyin uzoq kutib turgan tranzaksiya kutish davomida commit bo'lgan o'zgarishlarni baribir ko'radi. Hisobot va ko'p bosqichli o'qish uchun ideal.

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

Jadval darajasiga chiqishning ikkinchi yo'li ham bor va uning nomi lock escalation. Fowler tranzaksiya ishlatganda aynan nima lock qilinayotganidan xabardor bo'lishni talab qiladi: ko'p baza amalida tranzaksiya tizimi tegishli qatorlarni lock qiladi va shu sababli bir nechta tranzaksiya bitta jadval bilan ishlay oladi, lekin tranzaksiya jadvalda juda ko'p qatorni lock qilsa, bazada ko'tara oladiganidan ko'p lock to'planadi va lock butun jadvalga ko'tariladi, ya'ni boshqa tranzaksiyalarni jadvaldan chiqarib yuboradi (Fowler, *Patterns of Enterprise Application Architecture*, Addison-Wesley, 2003, 5-bob, 72-73-betlar).

Shu mexanizmdan Fowler bitta aniq sxema qoidasini chiqaradi: lock escalation konkurentlikka jiddiy ta'sir qilishi mumkin, va aynan shu sababli domenning [qatlam ustki turi](../patterns/02-strukturaviy-patternlar.md#216-qatlam-ustki-turi-layer-supertype) darajasidagi ma'lumot uchun umumiy "obyekt" jadvali qurmaslik kerak; bunday jadval lock escalation ning birinchi nomzodi bo'ladi, uni lock qilish esa hammani bazadan chiqarib yuboradi (5-bob, 73-bet).

```sql
-- Qochiladigan shakl: hamma agregat bitta jadvalda.
-- Har bir biznes oqimi shu jadvalga tegadi, demak har lock hammaga tegadi.
CREATE TABLE object (
    id      bigserial PRIMARY KEY,
    type    text NOT NULL,          -- 'ORDER', 'PAYMENT', 'INVOICE'
    payload jsonb NOT NULL
);

-- To'g'ri shakl: har agregat o'z jadvalida, lock ham o'sha jadvalda qoladi.
CREATE TABLE orders  (id bigserial PRIMARY KEY, customer_id bigint NOT NULL);
CREATE TABLE payment (id bigserial PRIMARY KEY, order_id    bigint NOT NULL);
```

Bu qoidaning sxema tomonidagi sababi lock dan ham keng: umumiy `object` jadvali turni ustun qiymatiga aylantirib cheklovlarni ham, indeksni ham ishlatib bo'lmaydigan qiladi, va bu [ichki platforma effekti](../patterns/25-anti-patternlar.md#2524-ichki-platforma-effekti-inner-platform-effect) ko'rinishi; turni to'g'ri tanlash [sxema dizayni bobida](25-sxema-dizayni-malumot-turlari-va-cheklovlar.md#251-turni-togri-tanlash-text-varchar-numeric-timestamptz-uuid-boolean).

PostgreSQL da escalation uchun sabab yo'q, chunki qator lock i umuman lock jadvalida yashamaydi. Qaysi qator lock qilingani haqidagi ma'lumot faqat o'sha qatorning joriy versiyasi, ya'ni heap tuple headerida saqlanadi: lock qo'ygan tranzaksiyaning `xid` i `xmax` maydoniga yoziladi va qo'shimcha hint bitlari bilan birga lock belgisi bo'lib xizmat qiladi. Demak qator lock lari amalda heap sahifasidagi atribut, haqiqiy lock emas: ular xotirada joy egallamaydi va `pg_locks` da hech qanday ko'rinmaydi, va shu mexanizm kerak bo'lgan qadar qatorni qo'shimcha narxsiz lock qilish imkonini beradi. Escalation esa o'sha yerda "ba'zi baza tizimlari" ning yechimi sifatida tasvirlanadi: qator lock lari juda ko'payganda ular bitta yirikroq granularitetdagi (sahifa yoki jadval darajasidagi) lock bilan almashtiriladi, bu implementatsiyani soddalashtiradi, lekin tizim throughput ini keskin cheklashi mumkin (Egor Rogov, *PostgreSQL 14 Internals*, 13-bob, 210-bet). Chegaradan oshib ketadigan hisob ham yo'q: navbatga turish uchun protsess qatorni emas, o'sha qator bilan band tranzaksiyaning `xid` ini lock qiladi, shuning uchun heavyweight lock soni o'zgartirilayotgan qator soniga emas, parallel protsess soniga proportsional (13-bob, 210-bet); `max_locks_per_transaction` chegaralaydigan pul ham (`max_locks_per_transaction` ni `max_connections` ga ko'paytirilgani, default 64 va 100) aynan shu obyekt darajasidagi heavyweight lock lar uchun (12-bob, 201-bet). Kitobning granularity haqidagi umumiy kirishida escalation lock metadatasiga ketadigan xotirani kamaytirish usullari qatorida bir marta eslatib o'tiladi (12-bob, 200-bet), lekin PostgreSQL ning qator lock i aynan tasvirlangan joyda yo'l `xmax` ekani va uning qo'shimcha narxi yo'qligi aytiladi. Natijada Fowler ning escalation mexanizmi PostgreSQL ga tegishli emas, uning sxema qoidasi esa kuchda qoladi: umumiy "obyekt" jadvali qurilmaydi, ammo sababi escalation emas, yuqorida sanalgani, ya'ni har bir biznes oqimining shu bitta jadvalga tegishi va cheklov bilan indeksni ishlatib bo'lmasligi.

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

## 22.12 ACID ta'rifi nega noaniq va anomaliyalar taksonomiyasi

ACID 1983 yilda Theo Harder va Andreas Reuter tomonidan aniq terminologiya yaratish uchun kiritilgan, lekin bugun bir bazaning ACID i boshqasining ACID iga teng emas va eng ko'p noaniqlik aynan isolation harfida: "ACID compliant" da'vosi qanday kafolat berilganini aytmaydi va Kleppmann atamani asosan marketing atamasiga aylangan deb baholaydi (*Designing Data-Intensive Applications*, 7-bob, 223-bet). ACID ga qarshi qo'yiladigan BASE yana ham noaniq: uning yagona mazmunli ta'rifi "ACID emas" (7-bob, 223-bet).

Arxitektor uchun shundan ikki aniqlik chiqadi. Birinchi: ACID dagi atomiklik concurrency haqida emas. U bir nechta yozuvning o'rtasida xato chiqsa nima bo'lishini bildiradi, ya'ni abort qilish va qilingan yozuvlarni bekor qilish qobiliyatini; Kleppmann "atomicity" o'rniga "abortability" to'g'riroq atama bo'lar edi deydi (7-bob, 223-bet). Bir vaqtda ishlayotgan tranzaksiyalar bir-biriga ta'siri esa I harfining ishi.

Ikkinchi: C harfi bazaga tegishli emas. Atomiklik, izolyatsiya va bardoshlilik bazaning xossasi, ACID ma'nosidagi konsistentlik esa ilovaning xossasi: invariantni ilova ta'riflaydi, baza esa invariantni buzadigan ma'lumotni yozishdan to'smaydi (7-bob, 224-225-betlar). Shuning uchun "baza konsistent" degan hisobot bandi hech narsani tasdiqlamaydi, `CHECK`, `FOREIGN KEY` va `UNIQUE` esa tasdiqlaydi: invariantni kodga emas, sxemaga ko'chirish shu farqdan kelib chiqadi.

Anomaliyalarni nomlab chiqish qarorni osonlashtiradi, chunki har bir daraja boshqa ro'yxatni to'sadi. PostgreSQL uchta daraja beradi va `READ UNCOMMITTED` ni `READ COMMITTED` deb qabul qiladi.

| Anomaliya | Nima sodir bo'ladi (DDIA 7-bob) | PostgreSQL da qaysi daraja to'sadi |
|---|---|---|
| Dirty read | Commit qilinmagan yozuv o'qiladi (234-bet) | Read Committed |
| Dirty write | Commit qilinmagan yozuv ustiga yoziladi (235-bet) | Read Committed |
| Read skew | Bitta tranzaksiya ikki xil holatni ko'radi (237-bet) | Repeatable Read |
| Lost update | Read-modify-write tsikli bir-birini bosadi (242-bet) | Repeatable Read (`40001`) yoki aniq lock |
| Write skew | Qaror eskirgan premissaga asoslanadi (246-bet) | Faqat Serializable |
| Phantom | Yozuv boshqa tranzaksiyaning qidiruv natijasini o'zgartiradi (250-bet) | O'qishda Repeatable Read, yozuv yo'lida faqat Serializable |

```sql
-- Sessiya qaysi darajada ishlayotganini tekshirish: taxmin qilinmaydi.
SHOW transaction_isolation;   -- read committed

-- Butun ilovaga emas, faqat kerakli yo'lga ko'tarish.
BEGIN ISOLATION LEVEL SERIALIZABLE;
-- ... kredit limiti tekshiruvi ...
COMMIT;
```

Qoida: daraja tanlashdan oldin qaysi anomaliya biznesga pul yo'qotishini ayting. "Serializable xavfsizroq" degan gap qaror emas, chunki u narxni hisobga olmaydi.

## 22.13 Bir obyektli va ko'p obyektli operatsiya: atomiklik qayerda tugaydi

Bitta `INSERT`, `UPDATE` yoki `DELETE` PostgreSQL da `BEGIN` yozilmasa ham atomik: statement o'z tranzaksiyasida ketadi. Kleppmann bu kafolatni storage engine darajasidagi atomiklik va izolyatsiya deb ataydi va ogohlantiradi: bir obyektli amallar, masalan atomik increment yoki compare-and-set, ko'pincha "transaction" deb sotiladi, lekin bu chalg'ituvchi, chunki ACID ma'nosidagi tranzaksiya bir nechta obyektni bitta guruhga biriktirishni bildiradi (*Designing Data-Intensive Applications*, 7-bob, 230-bet).

Ko'p obyektli tranzaksiya qachon haqiqatan kerak bo'ladi: foreign key bilan bog'langan qatorlarni birga yozishda, denormallashtirilgan nusxani (hisoblangan son, materiallashtirilgan ko'rinish) asl ma'lumot bilan birga yangilashda, va sekundar indeks jadval bilan bir vaqtda o'zgarishi kerak bo'lganda (7-bob, 231-bet).

Eng nozik joy guruhlashning o'zida. Relyatsion bazada tranzaksiya `BEGIN` va `COMMIT` orasidagi hamma narsa deb olinadi va bu TCP ulanishiga bog'langan; Kleppmann buni ideal emas deb ataydi: ulanish `COMMIT` so'ralgandan keyin, lekin javob kelmasidan uzilsa, mijoz tranzaksiya commit bo'lgan yoki bo'lmaganini bilmaydi (7-bob, 229-bet). Spring da bu holat `@Transactional` metod `CannotGetJdbcConnectionException` yoki `TransactionSystemException` bilan tushishi ko'rinishida chiqadi va "qayta urinaymi" savolini javobsiz qoldiradi.

Shundan qayta urinishning aniq chegaralari chiqadi. Kleppmann retry ni abort ning asl maqsadi deb ataydi, lekin to'rt tuzoqni sanaydi: commit haqiqatda o'tib faqat javob yo'qolgan bo'lsa retry ishni ikki marta qiladi; xato overload dan bo'lsa retry holatni yomonlashtiradi; doimiy xatoda (constraint buzilishi) retry ma'nosiz; bazadan tashqaridagi yon ta'sir (email, HTTP chaqiruv) tranzaksiya abort bo'lsa ham sodir bo'lib qoladi (7-bob, 231-232-betlar).

```java
@Service
public class PaymentFacade {
    private final PaymentService service;   // @Transactional shu ichida

    public PaymentResult pay(String idempotencyKey, PayCommand cmd) {
        int attempt = 0;
        while (true) {
            try {
                // Kalit bazada unique: ikkinchi urinish dublikat yaratmaydi.
                return service.payOnce(idempotencyKey, cmd);
            } catch (CannotSerializeTransactionException
                     | CannotAcquireLockException
                     | TransactionSystemException e) {
                // O'tkinchi xato: faqat shu sinf qayta urinishga arziydi.
                if (++attempt >= 3) throw e;
            } catch (DataIntegrityViolationException e) {
                // Doimiy xato: retry hech qachon natijani o'zgartirmaydi.
                throw new PaymentRejectedException(idempotencyKey, e);
            }
        }
    }
}
```

Yon ta'sirni tranzaksiya ichida qoldirmaslik qoidasi shu yerdan keladi: email va HTTP chaqiruv commit dan keyin, `@TransactionalEventListener(phase = AFTER_COMMIT)` orqali ketadi.

## 22.14 Fantomni lock obyektiga aylantirish: materializing conflicts

Fantom muammosining sababi lock qo'yadigan obyekt yo'qligida: tranzaksiya "bu xona bu vaqtda bo'shmi" deb qidiradi, natija bo'sh keladi va lock qo'yish uchun hech qanday qator yo'q. Kleppmann yechimni sun'iy lock obyekti kiritishda ko'radi: xona va 15 daqiqalik oraliqlarning hamma kombinatsiyasi uchun qatorlar oldindan yaratiladi, tranzaksiya kerakli qatorlarni `SELECT ... FOR UPDATE` bilan lock qiladi, keyin ustma-ust tushishni tekshiradi. Bu usul materializing conflicts deb ataladi, chunki u fantomni bazada mavjud aniq qatorlar ustidagi lock konfliktiga aylantiradi (*Designing Data-Intensive Applications*, 7-bob, 251-bet).

Kitob darhol narxini ham aytadi: konfliktni qanday materiallashtirish kerakligini topish qiyin va xatoga moyil, concurrency control ning ilova ma'lumot modeliga sizib kirishi esa xunuk; shu sababli bu usul boshqa yo'l qolmaganda ishlatiladigan oxirgi chora, ko'p holatda serializable daraja afzal (7-bob, 251-bet).

PostgreSQL da ikkinchi va uchinchi yo'l bor, shuning uchun lock jadvali kamdan kam oqlanadi. Eng toza yo'l invariantni cheklovga aylantirish: `btree_gist` kengaytmasi bilan `EXCLUDE` cheklovi ustma-ust tushgan oraliqni indeks darajasida rad etadi va hech qanday aniq lock talab qilmaydi.

```sql
CREATE EXTENSION IF NOT EXISTS btree_gist;

CREATE TABLE room_booking (
    id          bigserial PRIMARY KEY,
    room_id     bigint NOT NULL,
    period      tstzrange NOT NULL,
    -- Ustma-ust tushish endi fantom emas, cheklov buzilishi.
    EXCLUDE USING gist (room_id WITH =, period WITH &&)
);

-- Ikkinchi sessiya shu oraliqni yozsa:
-- ERROR: conflicting key value violates exclusion constraint
--        "room_booking_room_id_period_excl"   (SQLSTATE 23P01)
```

Java tomonida bu `DataIntegrityViolationException` bo'lib keladi va uni biznes xatosiga aylantirish kerak, chunki retry hech narsa bermaydi.

```java
try {
    bookingRepository.saveAndFlush(booking);
} catch (DataIntegrityViolationException e) {
    // 23P01: xona shu oraliqda band. Qayta urinish foydasiz.
    throw new RoomAlreadyBookedException(booking.getRoomId(), e);
}
```

Qaror tartibi: birinchi `EXCLUDE` yoki `UNIQUE` cheklovi, bo'lmasa Serializable plus retry, va faqat ikkisi ham imkonsiz bo'lganda lock jadvali. Lock jadvali tanlangan bo'lsa, u ma'lumot saqlamasligi va faqat lock yig'indisi ekani kod izohida yozilishi kerak.

## 22.15 Serializability ga uch yo'l va PostgreSQL faqat bittasini beradi

Kleppmann serializable izolyatsiyaga uchta amaliy yo'l borligini ko'rsatadi: tranzaksiyalarni haqiqatan ketma-ket bajarish, ikki fazali qulflash (2PL) va serializable snapshot isolation (SSI) (*Designing Data-Intensive Applications*, 7-bob, 251-266-betlar). Farqni bilish kerak, chunki PostgreSQL ularning faqat bittasini beradi va qolgan ikkitasini ilova darajasida taqlid qilish kerak bo'ladi.

Haqiqatan ketma-ket bajarish bitta thread da ishlaydi va shuning uchun to'rtta qattiq shartga bog'langan: har bir tranzaksiya kichik va tez bo'lishi shart, chunki bitta sekin tranzaksiya butun ishni to'xtatadi; faol ma'lumot xotiraga sig'ishi kerak; yozish throughput i bitta CPU yadrosiga sig'ishi kerak, aks holda partitsiyalash majburiy bo'ladi; partition lar o'rtasidagi tranzaksiyalar mumkin, lekin ularning ulushi qattiq cheklangan (7-bob, 256-bet). PostgreSQL bunday rejim bermaydi, lekin uning amaliy ko'rinishi bor: bitta agregat kalitiga bitta worker, ya'ni `pg_advisory_xact_lock(hashtext(key))` yoki kalit bo'yicha navbat.

2PL da yozuvchilar faqat yozuvchilarni emas, o'quvchilarni ham bloklaydi va teskarisi ham to'g'ri: snapshot izolyatsiyasining "o'quvchi yozuvchini bloklamaydi" mantrasi aynan shu nuqtada buziladi (7-bob, 257-bet). Buning narxi bashoratsiz latency va deadlock soni (7-bob, 258-bet). PostgreSQL o'qilgan qatorga avtomatik shared lock qo'ymaydi, ya'ni u 2PL ni amalga oshirmaydi; 2PL ga yaqin xulq faqat qo'lda, `FOR SHARE` va `FOR UPDATE` bilan quriladi. Pattern sifatida yozuvi [ikki fazali qulflash bo'limida](../patterns/28-taqsimlangan-malumot-replikatsiya-va.md#2822-ikki-fazali-qulflash-two-phase-locking).

SSI optimistik: u bloklamaydi, konfliktni commit paytida topadi va tranzaksiyani abort qiladi. PostgreSQL ning `SERIALIZABLE` darajasi aynan shu va uning mexanikasi [predikat lock bo'limida](#224-serializable-izolyatsiya-predikat-lock-va-uning-narxi) ko'rsatilgan.

| Yo'l | Bloklaydi | Narxi | PostgreSQL da |
|---|---|---|---|
| Ketma-ket bajarish | Hammani navbatga qo'yadi | Bitta yadro, kichik tranzaksiya | Yo'q; advisory lock yoki navbat bilan taqlid |
| 2PL | O'qish va yozish bir-birini | Latency bashoratsiz, deadlock | Yo'q; `FOR SHARE` plus `FOR UPDATE` bilan qo'lda |
| SSI | Bloklamaydi | Abort darajasi, `40001` retry | `SERIALIZABLE` darajasi |

```sql
-- Ketma-ket bajarishning PostgreSQL dagi amaliy ko'rinishi:
-- bitta agregat kaliti ustida bir vaqtda bitta tranzaksiya.
BEGIN;
SELECT pg_advisory_xact_lock(hashtext('order:' || 4215));
-- ... shu buyurtma ustidagi hamma o'qish va yozish ...
COMMIT;   -- advisory lock shu yerda o'zi bo'shaydi
```

Tanlov qoidasi: konflikt kamdan kam bo'lsa SSI, konflikt deyarli har safar bo'lsa va invariant bitta kalit atrofida yopilsa advisory lock bilan ketma-ketlashtirish arzonroq, chunki retry bo'roni bo'lmaydi.

## 22.16 `PREPARE TRANSACTION`: shubhadagi tranzaksiya lock ni ushlab turadi

Ikki fazali commit da ishtirokchi `prepared` holatga o'tgandan keyin coordinator qarorini kutadi va shu holat "shubhadagi" (in doubt) deb ataladi. Kleppmann asosiy xavf aynan lock da ekanini ko'rsatadi: tranzaksiya shubhada turgan butun davr mobaynida o'zgartirgan qatorlari ustidagi exclusive lock ni ushlab turishi shart; coordinator qulab 20 daqiqada ko'tarilsa lock lar 20 daqiqa ushlanadi, coordinator logi butunlay yo'qolsa esa lock lar administrator qo'lda hal qilmaguncha, ya'ni amalda cheksiz ushlanadi (*Designing Data-Intensive Applications*, 9-bob, 362-bet).

Yana ikki fakt qarorni belgilaydi. Bazani qayta ishga tushirish yordam bermaydi, chunki to'g'ri 2PC amalga oshirilishi shubhadagi tranzaksiyaning lock larini restart dan keyin ham saqlashi shart, aks holda atomiklik buziladi (9-bob, 362-bet). Va ko'p XA amalga oshirilishida "heuristic decision" degan zaxira yo'l bor: ishtirokchi coordinator qarorisiz o'zi commit yoki abort qiladi, bu esa Kleppmann ning so'zi bilan atomiklikni ehtimol buzish degani va faqat halokatli holat uchun (9-bob, 363-bet).

PostgreSQL da bu mexanizm `PREPARE TRANSACTION` orqali ochiladi va standart holatda o'chirilgan: `max_prepared_transactions` default qiymati 0, ya'ni 2PC ni ishlatish uchun uni ataylab yoqish va serverni qayta ishga tushirish kerak. Yoqilgan bo'lsa, tashlab ketilgan prepared tranzaksiya ikki zarar keltiradi: lock larni ushlaydi va `xmin` gorizontini orqada tutib `VACUUM` ni to'sadi, demak bloat o'sadi va transaction ID wraparound xavfi yaqinlashadi.

```sql
-- Tashlab ketilgan prepared tranzaksiyani topish: monitoringda majburiy panel.
SELECT gid, prepared, owner, database,
       now() - prepared AS yoshi
FROM pg_prepared_xacts
ORDER BY prepared;

-- Qaror faqat ikkita: ishtirokchilarning holatini tekshirib, keyin
COMMIT PREPARED 'tx-4215';
-- yoki
ROLLBACK PREPARED 'tx-4215';
```

Spring da `JtaTransactionManager` va XA DataSource shu yo'lni ochadi, lekin PostgreSQL va Kafka ni bitta XA tranzaksiyaga bog'lash arxitektura qarori sifatida deyarli har doim xato: shubhadagi tranzaksiya bazadagi eng issiq qatorlarni bloklab qo'yadi. To'g'ri yo'l bazani bitta mahalliy tranzaksiyada qoldirib, tashqi tizimga yuborishni [tranzaksion outbox](../patterns/10-malumotlarni-boshqarish-va-taqsimlash.md#1014-tranzaksion-outbox-transactional-outbox) orqali ajratish; Kafka tomonidagi ko'rinishi [Kafka bobida](29-kafka-operatsion-haqiqati-partition-lag.md#2911-tranzaksiya-va-xabar-yuborish-nomuvofiqligi-nega-ikki-fazali-commit-emas).

Operatsion qoida: `max_prepared_transactions > 0` bo'lsa, `pg_prepared_xacts` da bir necha daqiqadan uzoq turgan yozuv critical alert bo'lishi kerak (chegara uchun 5 daqiqa amaliy boshlang'ich nuqta, o'lchanmagan taxmin), chunki uni faqat odam hal qiladi.

## 22.17 Amalda qo'llash

- [ ] Hamma yozuv yo'llarini ro'yxatlab chiq va har biri lost update dan nima bilan himoyalanganini yoz. Himoyasiz yo'llarni darhol tuzat.
- [ ] Har bir shartli `UPDATE` ning affected rows ini tekshirishni majburiy qil va 0 holatida aniq biznes exception tashla.
- [ ] Repeatable Read yoki Serializable ishlatadigan yo'llarga tranzaksiyadan tashqarida 3-5 urinishli retry qo'y va urinish sonini metrika qilib chiqar.
- [ ] `@Transactional` metodlar ichidagi hamma tashqi HTTP, fayl va queue chaqiruvini audit qilib, tranzaksiyadan tashqariga ko'chir.
- [ ] Bazada `idle_in_transaction_session_timeout = 60s`, `statement_timeout = 30s`, `log_lock_waits = on` ni yoq va eng uzun ochiq tranzaksiya yoshiga alert qo'y.
- [ ] Migratsiya shabloniga `SET lock_timeout = '3s'` ni majburiy qator sifatida kirit va index yaratishni faqat `CONCURRENTLY` bilan ruxsat et.
- [ ] Pul yoki qoldiq o'zgartiradigan kodda lock lar `id` bo'yicha saralangan tartibda olinishini tekshir va buni test bilan qotir.
- [ ] Navbat jadvaliga partial index, `SKIP LOCKED` bilan atomik olish va qolib ketgan ishlar uchun reaper job qo'sh.

## Manbalar

- Martin Kleppmann, *Designing Data-Intensive Applications*, 7-bob - tranzaksiyalar, izolyatsiya darajalari va anomaliyalar (lost update, write skew, phantom)
- Martin Fowler, *Patterns of Enterprise Application Architecture*, Addison-Wesley, 2003, 5-bob (72-73-betlar) - tranzaksiyada aynan nima lock qilinayotganidan xabardor bo'lish talabi; qator lock lari soni dvigatel ko'targanidan oshganda lock ning butun jadvalga ko'tarilishi (lock escalation) va uning konkurentlikka ta'siri; qatlam ustki turi darajasidagi umumiy "obyekt" jadvalini qurmaslik qoidasi va bunday jadvalning hammani bazadan chiqarib yuborishi
- Egor Rogov, *PostgreSQL 14 Internals*, Postgres Professional, 2022, 13-bob "Row-Level Locks", 210-bet va 12-bob "Relation-Level Locks", 200-201-betlar - qator lock i faqat heap tuple headeridagi `xmax` maydonida saqlanishi, uning xotirada joy egallamasligi va `pg_locks` da ko'rinmasligi, kerakli qadar qatorni qo'shimcha narxsiz lock qilish, lock escalation "ba'zi baza tizimlari" ning yechimi ekani, heavyweight lock soni parallel protsess soniga proportsionalligi va `max_locks_per_transaction` ni `max_connections` ga ko'paytirilgan pul
- Martin Kleppmann, *Designing Data-Intensive Applications*, O'Reilly, 2017, 7-bob (223-232-betlar) - ACID atamasining noaniqligi va BASE ning "ACID emas" ma'nosi, atomiklik aslida abort qilish qobiliyati ekani, C harfi ilovaga tegishliligi, bir obyektli va ko'p obyektli operatsiya farqi, qayta urinishning to'rt chegarasi
- Martin Kleppmann, *Designing Data-Intensive Applications*, O'Reilly, 2017, 7-bob (234-266-betlar) - anomaliyalar taksonomiyasi, konfliktni materiallashtirish (251-bet) va serializability ga uch yo'l: ketma-ket bajarish, 2PL, SSI
- Martin Kleppmann, *Designing Data-Intensive Applications*, O'Reilly, 2017, 9-bob (362-363-betlar) - shubhadagi tranzaksiya lock ni ushlab turishi, restart yordam bermasligi va heuristic decision ning ma'nosi
- [PostgreSQL 17, `max_prepared_transactions` (config.sgml)](https://raw.githubusercontent.com/postgres/postgres/REL_17_STABLE/doc/src/sgml/config.sgml) - default qiymat nol va u prepared-transaction imkoniyatini butunlay o'chiradi
- [PostgreSQL 17, `PREPARE TRANSACTION` (ref/prepare_transaction.sgml)](https://raw.githubusercontent.com/postgres/postgres/REL_17_STABLE/doc/src/sgml/ref/prepare_transaction.sgml) - `pg_prepared_xacts` ko'rinishi, `COMMIT PREPARED` va `ROLLBACK PREPARED`, ochiq qolgan prepared tranzaksiya `VACUUM` ni to'sishi va lock larni ushlab turishi
- [PostgreSQL 17, Exclusion constraints (ddl.sgml)](https://raw.githubusercontent.com/postgres/postgres/REL_17_STABLE/doc/src/sgml/ddl.sgml) - `EXCLUDE USING gist` bilan ustma-ust tushgan oraliqni rad etish
- [PostgreSQL 17, Transaction Isolation (mvcc.sgml)](https://raw.githubusercontent.com/postgres/postgres/REL_17_STABLE/doc/src/sgml/mvcc.sgml) - Read Committed default ekani, har statement o'z snapshotini olishi, Repeatable Read snapshoti birinchi statementda olinishi, Serializable ning qo'shimcha bloklash kiritmasligi
- [PostgreSQL 17, Explicit Locking (mvcc.sgml)](https://raw.githubusercontent.com/postgres/postgres/REL_17_STABLE/doc/src/sgml/mvcc.sgml) - lock turlari va ularning mosligi

---

[&larr; 21. PostgreSQL arxitekturasi: process model, WAL, checkpoint, vacuum](21-postgresql-arxitekturasi-process-model-wal.md) · [Mundarija](README.md) · [23. Indekslar: B-tree, GIN, GiST, BRIN va tanlov &rarr;](23-indekslar-b-tree-gin-gist-brin-va-tanlov.md)
