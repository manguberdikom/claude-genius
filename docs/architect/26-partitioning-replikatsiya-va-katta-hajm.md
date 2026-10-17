<!-- doc: architect | chapter: 26 | part: IV. PostgreSQL chuqur bilim -->

[Barcha hujjatlar](../../README.md) / [Arxitektor miyasi](README.md)

> Holat: tekshirilmoqda. Da'volar hali manbaga solishtirilmoqda.

# 26. Partitioning, replikatsiya va katta hajm (Partitioning, Replication and Scale)

<details>
<summary>Bu bobdagi 20 bo'lim</summary>

- [26.1 Jadval qachon katta hisoblanadi: qaror uchun raqamlar](#261-jadval-qachon-katta-hisoblanadi-qaror-uchun-raqamlar)
- [26.2 Deklarativ partitioning: range, list, hash va kalit tanlash](#262-deklarativ-partitioning-range-list-hash-va-kalit-tanlash)
- [26.3 Partition pruning qachon ishlaydi va qachon ishlamaydi](#263-partition-pruning-qachon-ishlaydi-va-qachon-ishlamaydi)
- [26.4 Eski ma'lumotni o'chirish: `DETACH PARTITION` ning tezligi](#264-eski-malumotni-ochirish-detach-partition-ning-tezligi)
- [26.5 Mavjud katta jadvalni to'xtashsiz partitsiyalashga o'tkazish](#265-mavjud-katta-jadvalni-toxtashsiz-partitsiyalashga-otkazish)
- [26.6 Streaming replikatsiya: primary va standby, lag o'lchash](#266-streaming-replikatsiya-primary-va-standby-lag-olchash)
- [26.7 Sinxron va asinxron replikatsiya tanlovi va uning narxi](#267-sinxron-va-asinxron-replikatsiya-tanlovi-va-uning-narxi)
- [26.8 O'qishni standby ga yo'naltirish va replikatsiya lag dan kelib chiqadigan xatolar](#268-oqishni-standby-ga-yonaltirish-va-replikatsiya-lag-dan-kelib-chiqadigan-xatolar)
- [26.9 Mantiqiy replikatsiya va CDC uchun asos](#269-mantiqiy-replikatsiya-va-cdc-uchun-asos)
- [26.10 Failover va yuqori mavjudlik vositalari haqida qisqacha](#2610-failover-va-yuqori-mavjudlik-vositalari-haqida-qisqacha)
- [26.11 Spring da o'qish va yozish uchun alohida DataSource sozlash](#2611-spring-da-oqish-va-yozish-uchun-alohida-datasource-sozlash)
- [26.12 Sharding qachon zarur bo'ladi va nega eng oxirgi chora](#2612-sharding-qachon-zarur-boladi-va-nega-eng-oxirgi-chora)
- [26.13 Analitik yukni OLTP dan ajratish: read replica, CDC va ombor](#2613-analitik-yukni-oltp-dan-ajratish-read-replica-cdc-va-ombor)
- [26.14 Izchil prefiks o'qishi: bitta WAL oqimi kafolat beradi, ko'p manba bermaydi](#2614-izchil-prefiks-oqishi-bitta-wal-oqimi-kafolat-beradi-kop-manba-bermaydi)
- [26.15 Replikatsiya logining to'rt turi va PostgreSQL versiya yangilashdagi oqibati](#2615-replikatsiya-logining-tort-turi-va-postgresql-versiya-yangilashdagi-oqibati)
- [26.16 Qiyshiq yuklama va issiq partition: hash bo'yicha bo'lish yetmaydi](#2616-qiyshiq-yuklama-va-issiq-partition-hash-boyicha-bolish-yetmaydi)
- [26.17 Sekundar indeksni bo'lish: lokal va global indeks](#2617-sekundar-indeksni-bolish-lokal-va-global-indeks)
- [26.18 Qayta balanslash strategiyalari va `hash mod N` nega yaramaydi](#2618-qayta-balanslash-strategiyalari-va-hash-mod-n-nega-yaramaydi)
- [26.19 So'rovni yo'naltirish: uch yondashuv va PostgreSQL dagi ko'rinishi](#2619-sorovni-yonaltirish-uch-yondashuv-va-postgresql-dagi-korinishi)
- [26.20 Amalda qo'llash](#2620-amalda-qollash)

</details>



Katta hajm hech qachon bir kunda kelmaydi. Buyurtma jadvali ikki yil ichida 300 million qatorga chiqadi, hisobot so'rovi 40 ms dan 9 sekundga o'tadi, va kechagi `DELETE` tungi oynani to'ldirib qo'yadi. Bu bobda PostgreSQL ning partitioning va replikatsiya mexanikasi, uning ichida nima sodir bo'lishi va arxitektor shu bilimdan qanday raqamli qaror chiqarishi ko'rib chiqiladi. Taqsimlangan ma'lumot patternlari bu yerda emas, dizayn [patternlar hujjatida](../patterns/README.md).

## 26.1 Jadval qachon katta hisoblanadi: qaror uchun raqamlar

Partitioning qarori "jadval katta ko'rinadi" degan tuyg'udan emas, to'rt o'lchovdan chiqadi. Birinchi o'lchov: jadval va uning indekslari `shared_buffers` ga sig'adimi. Odatda `shared_buffers` RAM ning 25 foizi, ya'ni 64 GB serverda taxminan 16 GB. Agar faol indekslar yig'indisi shundan katta bo'lsa, har bir index lookup diskka tushadi va latency 0.1 ms dan 2 ms ga o'tadi.

Ikkinchi o'lchov: autovacuum bir jadvalni necha vaqtda aylanib chiqadi. 200 GB jadvalda `autovacuum_vacuum_cost_limit` standart qiymatda qolsa, bitta tsikl bir necha sutka davom etishi mumkin. Uchinchi o'lchov: eski ma'lumotni o'chirish yo'li bormi. To'rtinchi: `REINDEX` va backup oynasi.

```sql
-- jadval va index hajmini birgalikda ko'rish, eng kattalari yuqorida
SELECT relname,
       pg_size_pretty(pg_table_size(oid))        AS heap,
       pg_size_pretty(pg_indexes_size(oid))      AS indekslar,
       pg_size_pretty(pg_total_relation_size(oid)) AS jami,
       n_live_tup
FROM pg_class c
JOIN pg_stat_user_tables s ON s.relid = c.oid
WHERE relkind = 'r'
ORDER BY pg_total_relation_size(oid) DESC
LIMIT 10;
```

Amaliy chegara: 10 GB dan kichik jadvalni partitsiyalash deyarli har doim zarar. 50 GB dan katta va vaqt bo'yicha o'qiladigan jadval partitioning uchun yaxshi nomzod. 100 GB dan katta va retention siyosati bor jadvalda partitioning tanlov emas, majburiyat.

## 26.2 Deklarativ partitioning: range, list, hash va kalit tanlash

PostgreSQL 10 dan beri deklarativ partitioning bor, 15-17 versiyalarda esa u ishlab chiqarishga to'liq yaroqli. Range eng ko'p ishlatiladi: vaqt bo'yicha bo'lish. List tenant yoki region bo'yicha ajratishga to'g'ri keladi. Hash kalit qiymatlari teng tarqalishini xohlaganda, masalan `customer_id` bo'yicha yuklamani 16 ta bo'lakka yoyganda ishlatiladi.

Eng muhim qoida: partition kaliti har bir unique constraint va primary key tarkibida bo'lishi shart. Shuning uchun `orders` jadvalining PK si `(id)` emas, `(id, created_at)` bo'lib qoladi. 
```sql
CREATE TABLE orders (
    id          bigint GENERATED BY DEFAULT AS IDENTITY,
    customer_id bigint      NOT NULL,
    status      text        NOT NULL,
    amount      numeric(19,4) NOT NULL,
    created_at  timestamptz NOT NULL,
    PRIMARY KEY (id, created_at)      -- kalit PK ichida bo'lishi shart
) PARTITION BY RANGE (created_at);

CREATE TABLE orders_2026_09 PARTITION OF orders
    FOR VALUES FROM ('2026-09-01') TO ('2026-10-01');
CREATE TABLE orders_2026_10 PARTITION OF orders
    FOR VALUES FROM ('2026-10-01') TO ('2026-11-01');

-- chegaradan tashqari qolgan qator yo'qolmasligi uchun
CREATE TABLE orders_default PARTITION OF orders DEFAULT;

-- index har bir partitionga avtomatik tarqaladi
CREATE INDEX ON orders (customer_id, created_at DESC);
```

Partition sonini nazorat qiling. 12-60 ta partition sog'lom. 1000 dan oshsa, planning vaqti va lock soni sezilarli o'sadi, chunki planner har bir partitionni ko'rib chiqadi va `max_locks_per_transaction` chegarasiga yaqinlashadi. Yangi partitionni qo'lda yaratish esdan chiqadi, shuning uchun `pg_partman` kabi vosita yoki scheduled job kerak. Default partition unutilgan oyni xatodan saqlaydi, lekin unga qator tushgach yangi partition `ATTACH` qilish qiyinlashadi.

## 26.3 Partition pruning qachon ishlaydi va qachon ishlamaydi

Pruning planner yoki executor darajasida ishlaydi. Planner darajasida `WHERE created_at >= '2026-10-01'` kabi konstanta bilan taqqoslash kerak. `EXPLAIN` chiqishida faqat kerakli partition ko'rinadi. Executor darajasida pruning esa parametrli so'rov va nested loop ichida ishlaydi, `EXPLAIN ANALYZE` da `Subplans Removed: 11` qatori shundan xabar beradi.

Pruning buziladigan uch holat bor. Birinchi: kalit ustiga funksiya qo'yilgan, masalan `date_trunc('month', created_at) = '2026-10-01'`. Bu yerda planner chegaralarni hisoblay olmaydi. Ikkinchi: filtr kalitda emas, faqat `status` bo'yicha. Uchinchi: join kaliti partition kaliti emas, bu holda barcha partitionlar skanerdan o'tadi.

```sql
-- yaxshi: faqat bitta partition o'qiladi
EXPLAIN (ANALYZE, BUFFERS)
SELECT sum(amount) FROM orders
WHERE created_at >= '2026-10-01' AND created_at < '2026-11-01';

-- yomon: funksiya kalitni yashiradi, hamma partition skanerdan o'tadi
EXPLAIN SELECT sum(amount) FROM orders
WHERE date_trunc('month', created_at) = '2026-10-01';

-- partition kaliti bo'yicha joinda partitionwise join kerak
SET enable_partitionwise_join = on;      -- standart holatda off
SET enable_partitionwise_aggregate = on; -- katta hisobotlar uchun
```

`enable_partitionwise_join` planning vaqtini oshirgani uchun o'chirilgan: hisobot bazasida yoqish mantiqiy, OLTP da ehtiyot bo'lish kerak. `now()` funksiyasi STABLE, shuning uchun `created_at > now() - interval '7 days'` executor darajasida to'g'ri prune bo'ladi.

## 26.4 Eski ma'lumotni o'chirish: `DETACH PARTITION` ning tezligi

Mana partitioning ning eng katta amaliy foydasi. 50 million qatorli bir oylik ma'lumotni `DELETE` qilish taxminan 15-40 daqiqa oladi, WAL ga o'n gigabayt yozadi, so'ng autovacuum shu joyni tozalashga yana soatlar sarflaydi. Bo'sh joy operatsion tizimga qaytmaydi. `DROP TABLE` esa katalog operatsiyasi, taxminan 50 ms da tugaydi va fayllarni butunlay o'chiradi.

```sql
-- 1-qadam: uzoq lock olmasdan ajratish (PostgreSQL 14+)
-- bu buyruq tranzaksiya bloki ichida bo'lmasligi kerak
ALTER TABLE orders DETACH PARTITION orders_2025_10 CONCURRENTLY;

-- 2-qadam: arxivga ko'chirish yoki butunlay o'chirish
-- avval sovuq saqlashga eksport
-- COPY orders_2025_10 TO PROGRAM 'gzip > /arxiv/orders_2025_10.csv.gz' CSV;
DROP TABLE orders_2025_10;

-- oddiy DETACH ishlatilsa, parentga ACCESS EXCLUSIVE lock tushadi,
-- shuning uchun kutish vaqtini cheklab qo'yish kerak
SET lock_timeout = '3s';
ALTER TABLE orders DETACH PARTITION orders_2025_11;
```

`CONCURRENTLY` variantida PostgreSQL ikki fazada ishlaydi va uzoq muddatli ACCESS EXCLUSIVE lock olmaydi. Buning sharti: buyruq avtomatik commit rejimida, tranzaksiya bloki tashqarisida bajarilsin. Agar buyruq to'xtab qolsa, partition `DETACH PENDING` holatida qoladi va uni `FINALIZE` bilan tugatish kerak.

## 26.5 Mavjud katta jadvalni to'xtashsiz partitsiyalashga o'tkazish

Bu ish bir buyruq bilan bo'lmaydi. 400 GB `payments` jadvalini `CREATE TABLE ... PARTITION BY` ga aylantirish imkoni yo'q, chunki oddiy jadvalni partitsiyalangan jadvalga joyida o'zgartirish mumkin emas. Ishonchli yo'l to'rt qadamdan iborat.

Birinchi qadam: yangi partitsiyalangan parent yaratish va kelgusi oylar uchun bo'sh partitionlar qo'shish. Ikkinchi: eski jadvalni o'sha parentga partition sifatida `ATTACH` qilish. Bu yerda muhim nozik joy bor. `ATTACH PARTITION` chegarani tekshirish uchun to'liq skan qiladi, agar jadvalda mos `CHECK` constraint oldindan bo'lmasa.

```sql
-- eski jadvalga NOT VALID check qo'yib, keyin fonda validatsiya qilamiz
ALTER TABLE payments_old
  ADD CONSTRAINT payments_old_range
  CHECK (created_at >= '2019-01-01' AND created_at < '2026-10-01') NOT VALID;

-- VALIDATE faqat SHARE UPDATE EXCLUSIVE lock oladi, yozish davom etadi
ALTER TABLE payments_old VALIDATE CONSTRAINT payments_old_range;

-- endi ATTACH to'liq skan qilmaydi, bir necha yuz millisekundda tugaydi
ALTER TABLE payments ATTACH PARTITION payments_old
  FOR VALUES FROM ('2019-01-01') TO ('2026-10-01');

-- oxirgi qadam: qisqa tranzaksiyada nom almashtirish
SET lock_timeout = '2s';
BEGIN;
  ALTER TABLE payments_live RENAME TO payments_legacy;
  ALTER TABLE payments RENAME TO payments_live;
COMMIT;
```

Nom almashtirish tranzaksiyasi millisekundlar ichida tugaydi, lekin ACCESS EXCLUSIVE lock talab qiladi. Shuning uchun `lock_timeout` qo'yiladi va buyruq yuklama past paytda takroriy urinish bilan bajariladi. `SPLIT PARTITION` va `MERGE PARTITIONS` buyruqlari PostgreSQL 17 ishlab chiqish davrida qo'shilgan, lekin chiqarilishdan oldin qaytarib olingan: 17 va 18 ning `ALTER TABLE` sintaksisida ular yo'q, faqat `ATTACH PARTITION` va `DETACH PARTITION` bor ([REL_17_0](https://github.com/postgres/postgres/blob/REL_17_0/doc/src/sgml/ref/alter_table.sgml), [REL_18_0](https://github.com/postgres/postgres/blob/REL_18_0/doc/src/sgml/ref/alter_table.sgml)). Shuning uchun partitsiyani bo'lish yoki birlashtirish yangi partitsiya yaratish, ma'lumotni ko'chirish va `DETACH`/`ATTACH` bilan qilinadi.

## 26.6 Streaming replikatsiya: primary va standby, lag o'lchash

Streaming replikatsiyada primary dagi `walsender` process WAL yozuvlarini standby dagi `walreceiver` ga uzatadi. Standby ularni diskka yozadi, so'ng `startup` process qayta ijro etadi. Shu uch bosqich uchta alohida lag beradi: `write_lag`, `flush_lag`, `replay_lag`.

```sql
-- primary da: har bir standby uchun bayt va vaqt bo'yicha lag
SELECT application_name,
       state,
       sync_state,
       pg_wal_lsn_diff(pg_current_wal_lsn(), replay_lsn) AS lag_bayt,
       write_lag, flush_lag, replay_lag
FROM pg_stat_replication;

-- standby da: replikatsiya kechikishi sekundda
SELECT CASE WHEN pg_is_in_recovery()
            THEN extract(epoch FROM now() - pg_last_xact_replay_timestamp())
       END AS lag_sek;

-- slot WAL ni ushlab qolib diskni to'ldirmasligi uchun
-- postgresql.conf: max_slot_wal_keep_size = '64GB'
SELECT slot_name, active, wal_status,
       pg_size_pretty(pg_wal_lsn_diff(pg_current_wal_lsn(), restart_lsn))
FROM pg_replication_slots;
```

Bir data markazda normal `replay_lag` 1 ms dan 50 ms gacha, baytda bir necha megabayt. Lag o'nlab sekundga chiqsa, sabab odatda ikkitadan biri: standby da og'ir `SELECT` replay ni bloklagan, yoki primary da bitta katta tranzaksiya WAL ni to'kib tashlagan. Replication slot himoya beradi, lekin standby o'lsa WAL to'planib diskni to'ldiradi, shuning uchun `max_slot_wal_keep_size` majburiy.

## 26.7 Sinxron va asinxron replikatsiya tanlovi va uning narxi

`synchronous_commit` ning narxi bitta raqam bilan o'lchanadi: commit ga qo'shiladigan tarmoq RTT. Bir availability zone ichida bu taxminan 0.3-1 ms, zonalar orasida 1-2 ms, regionlar orasida 20-80 ms. To'lov servisida sekundiga 500 commit bo'lsa, cross-region sinxron rejim to'g'ridan to'g'ri throughput ni o'n baravar pasaytiradi.

| Rejim | Kafolat | Qo'shimcha latency |
| --- | --- | --- |
| `off` | hatto primary diskiga ham kafolat yo'q | 0 ga yaqin |
| `local` | faqat primary WAL diskda | fsync vaqti, 0.1-1 ms |
| `remote_write` | standby OS buferida | 1 RTT |
| `on` | standby WAL diskda | 1 RTT + fsync |
| `remote_apply` | standby da ko'rinadi | 1 RTT + replay |

Eng xavfli xato: bitta sinxron standby qo'yish. U o'lsa, barcha commitlar muddatsiz kutib qoladi va baza yozish uchun yopiladi. To'g'ri sozlash kvorum bilan bo'ladi.

```ini
# postgresql.conf, primary da
# ikki nomzoddan bittasi javob bersa commit o'tadi
synchronous_standby_names = 'ANY 1 (standby_a, standby_b)'
synchronous_commit = on
wal_level = replica
max_wal_senders = 10
max_slot_wal_keep_size = '64GB'
```

Butun bazani bitta rejimga majburlash shart emas: to'lov tranzaksiyasi sinxron, audit logi asinxron bo'lishi mumkin. Buni tranzaksiya darajasida `SET LOCAL synchronous_commit = 'local'` bilan qilinadi, Spring da esa shu buyruqni `@Transactional` metod boshida yuborish yetarli.

## 26.8 O'qishni standby ga yo'naltirish va replikatsiya lag dan kelib chiqadigan xatolar

Standby dan o'qish ikki turdagi muammo keltiradi. Birinchisi texnik xato: `ERROR: canceling statement due to conflict with recovery`. Bu replay primary da `VACUUM` tozalagan qatorni o'chirmoqchi bo'lganda, standby dagi uzun `SELECT` esa shu qatorni hali o'qiyotganda yuz beradi. Yechim ikkita: `max_standby_streaming_delay` ni oshirish, yoki `hot_standby_feedback = on` qo'yish. Ikkinchisi primary da bloat o'sishiga olib keladi, chunki `VACUUM` standby dagi eng eski snapshot ni kutadi.

Ikkinchi muammo mantiqiy: foydalanuvchi to'lovni yaratdi, keyingi so'rov standby ga tushdi va to'lov hali ko'rinmaydi. Buni lag o'lchab hal qilib bo'lmaydi, chunki lag o'zgaruvchan. To'g'ri yechim: yozishdan keyingi N sekund ichida o'sha foydalanuvchining o'qishlarini primary ga yuborish, yoki commit LSN ni saqlab standby shu LSN ga yetganini tekshirish.

| Tuzoq | Nima sodir bo'ladi | Yechim |
| --- | --- | --- |
| Bitta sinxron standby | standby o'lsa yozish to'xtaydi | `ANY 1 (a, b)` kvorumi |
| `max_slot_wal_keep_size` yo'q | slot WAL ni ushlab disk to'ladi | chegara qo'yish va slot monitoringi |
| Standby da uzun hisobot | recovery conflict, so'rov o'ldiriladi | alohida standby, `hot_standby_feedback` |
| `readOnly=true` ga ishonib yozish | silent routing xatosi, UPDATE yo'qoladi | standby da PostgreSQL o'zi xato beradi, testda tekshirish |
| Connection darhol olinadi | routing qarori kech, har doim primary | `LazyConnectionDataSourceProxy` |
| Funksiya partition kalitida | pruning yo'q, hamma partition skan | filtrni xom ustunga yozish |
| `DELETE` bilan retention | bloat, uzoq vacuum, WAL to'lishi | `DETACH` + `DROP TABLE` |
| Logical slot iste'molchisi o'chgan | WAL cheksiz o'sadi | slot lag alert, eskisini `DROP` |

## 26.9 Mantiqiy replikatsiya va CDC uchun asos

Streaming replikatsiya butun klasterni bayt darajasida ko'chiradi. Mantiqiy replikatsiya esa jadval darajasida ishlaydi va `pgoutput` plaginidan foydalanadi. Debezium ham shu plagin orqali o'qiydi, ya'ni CDC uchun tashqi C kutubxona o'rnatish shart emas.

```sql
-- postgresql.conf: wal_level = logical, keyin restart kerak
CREATE PUBLICATION cdc_pub FOR TABLE orders, payments;

-- PK yo'q jadvalda UPDATE/DELETE uchun identifikator kerak
ALTER TABLE order_items REPLICA IDENTITY FULL;

-- faqat kerakli qatorlarni uzatish (PostgreSQL 15+)
CREATE PUBLICATION paid_pub FOR TABLE orders
  WHERE (status = 'PAID');

-- Debezium uchun slot qo'lda ham yaratilishi mumkin
SELECT pg_create_logical_replication_slot('debezium_orders', 'pgoutput');
```

To'rtta cheklovni bilish shart. DDL replikatsiya qilinmaydi, ya'ni yangi ustun qo'shilsa, iste'molchi tomonda ham qo'lda qo'shish kerak. TOAST ga tushgan va o'zgarmagan ustun qiymati stream ga chiqmaydi, shuning uchun katta JSON ustunga tayangan CDC pipeline kutilmagan `null` ko'radi. Sequence qiymatlari ko'chmaydi. Va eng xavflisi: iste'molchi o'chsa, slot WAL ni ushlab turadi. Slot lag ni monitoringga qo'yish bu yerda ixtiyoriy emas. CDC ni outbox o'rniga ishlatish qarori dizayn [patternlar hujjatidagi](../patterns/README.md) outbox pattern bilan solishtirib olinadi.

## 26.10 Failover va yuqori mavjudlik vositalari haqida qisqacha

PostgreSQL o'zida avtomatik failover yo'q. Bu tashqi vosita ishi. Eng keng tarqalgani Patroni, u etcd yoki Consul kabi distributed konfiguratsiya saqlagichdan leader election oladi. Alternativalar: repmgr va pg_auto_failover. Boshqariladigan servislarda (RDS, Cloud SQL) bu qatlam provayder tomonida.

Uch nuqta muhim. Birinchi: split brain faqat kvorumli DCS va watchdog bilan oldini olinadi, "ping ishlamasa promote qil" skripti emas. Ikkinchi: eski primary qaytganda uni `pg_rewind` bilan yangi timeline ga moslash kerak, aks holda ma'lumot ayriladi. Uchinchi: RTO taxminan 10-30 sekund, ya'ni ilova shu vaqtni xatosiz o'tkazishga qodir bo'lishi shart.

```properties
# PgJDBC o'zi primary ni topadi, failover dan keyin qayta ulanadi
spring.datasource.url=jdbc:postgresql://pg-a:5432,pg-b:5432/shop\
?targetServerType=primary&loadBalanceHosts=false\
&connectTimeout=3&socketTimeout=30

# failover paytida pool uzun kutmasin
spring.datasource.hikari.connection-timeout=3000
spring.datasource.hikari.validation-timeout=2000
spring.datasource.hikari.keepalive-time=120000
```

Failover testi ishlab chiqarishga chiqishdan oldin bajarilishi kerak: [testlash qo'llanmasidagi](../testing/README.md) resilience testlari bo'limida standby ni promote qilib tiklanish vaqtini o'lchash ssenariysi bor.

## 26.11 Spring da o'qish va yozish uchun alohida DataSource sozlash

`AbstractRoutingDataSource` routing kalitini `determineCurrentLookupKey()` da aniqlaydi va `TransactionSynchronizationManager.isCurrentTransactionReadOnly()` shu kalit uchun tabiiy manba. Lekin bitta jiddiy tuzoq bor: Spring tranzaksiya boshlanishida connection ni darhol oladi, ya'ni routing qarori `readOnly` flagi o'rnatilishidan oldin bo'lishi mumkin. Shuning uchun routing DataSource ni `LazyConnectionDataSourceProxy` ichiga o'rash shart.

```java
public class ReadWriteRoutingDataSource extends AbstractRoutingDataSource {
    @Override
    protected Object determineCurrentLookupKey() {
        // readOnly tranzaksiya standby ga, qolgani primary ga
        return TransactionSynchronizationManager.isCurrentTransactionReadOnly()
                ? "replica" : "primary";
    }
}

@Configuration
class DataSourceConfig {
    @Bean
    DataSource dataSource(@Qualifier("primaryDs") DataSource primary,
                          @Qualifier("replicaDs") DataSource replica) {
        var router = new ReadWriteRoutingDataSource();
        router.setTargetDataSources(Map.of("primary", primary, "replica", replica));
        router.setDefaultTargetDataSource(primary);
        router.afterPropertiesSet();
        // lazy o'ram bo'lmasa routing qarori har doim primary ga tushadi
        return new LazyConnectionDataSourceProxy(router);
    }
}
```

Pool o'lchamini ikki tomonga alohida bering. Yozish pooli kichik bo'lsin, masalan 10 ta connection, chunki primary dagi yozish lock bilan cheklangan. O'qish pooli kattaroq, masalan 20-30 ta, chunki hisobot so'rovlari uzoq. `@Transactional(readOnly = true)` nafaqat routing beradi, balki Hibernate flush ni o'chiradi va dirty checking ishini kamaytiradi, ya'ni katta `SELECT` da taxminan 10-20 foiz CPU tejaydi.

## 26.12 Sharding qachon zarur bo'ladi va nega eng oxirgi chora

Sharding bitta primary ning yozish quvvati tugaganda kerak bo'ladi. Shu chegara aniq raqam bilan ko'rinadi: `pg_stat_statements` da yozish so'rovlari jami vaqti CPU ni to'ldirgan, WAL hajmi sekundiga o'nlab megabayt, va vertikal o'sish uchun joy qolmagan. Zamonaviy serverda bu taxminan sekundiga bir necha o'n ming yozish operatsiyasi va bir necha terabayt faol ma'lumot.

| Vaziyat | Oddiy yondashuv | Arxitektor yondashuvi |
| --- | --- | --- |
| Jadval 200 GB ga yetdi | darhol shard qilish rejasi | avval range partitioning va retention |
| Hisobot so'rovi sekin | primary ga yana index qo'shish | hisobotni alohida standby ga ko'chirish |
| Eski buyurtma kerak emas | tungi `DELETE` job | `DETACH PARTITION` + arxivga `COPY` |
| Replikatsiya lag o'sdi | standby ni kuchaytirish | uzun so'rov va katta tranzaksiyani topish |
| Standby dan eski ma'lumot | lag ni e'tiborsiz qoldirish | yozishdan keyin primary ga yo'naltirish |
| Sinxron kafolat kerak | hammasini `remote_apply` | faqat to'lov yo'lida, kvorum bilan |
| CDC kerak bo'ldi | jadvalni poll qilish | `pgoutput` slot va slot lag alerti |
| Connection soni 2000 | `max_connections` ni oshirish | PgBouncer transaction pooling |
| Yozish quvvati tugadi | darhol sharding | avval batching, partition, arxivlash |
| Shard kaliti tanlanmoqda | `id` bo'yicha hash | `tenant_id` yoki `customer_id` bo'yicha |

Sharding dan oldin to'rtta arzon qadam bor: partitioning, read replica, arxivlash va PgBouncer orqali connection konsentratsiyasi. Narxi esa doimiy: cross-shard join yo'qoladi, global unique constraint yo'qoladi, tranzaksiya bir shard bilan cheklanadi, rebalance esa alohida loyiha bo'ladi. Shard kaliti biznes agregatiga mos tushishi kerak, ya'ni `tenant_id` yoki `customer_id`. Agar so'rovlarning 10 foizi ikki shardga tegsa, bu arxitektura ishlaydi. 50 foizi tegsa, kalit noto'g'ri tanlangan. Citus kabi kengaytma bu ishni osonlashtiradi, lekin qarorni o'zgartirmaydi: sharding oxirgi chora.

## 26.13 Analitik yukni OLTP dan ajratish: read replica, CDC va ombor

Katta jadval muammosining ikkinchi yarmi partitioning bilan hal bo'lmaydi: hisobot va analitika so'rovlari OLTP yuki bilan bir xil bazada yurganda ikkisi bir-birini buzadi. Sabab arxitekturada: OLTP so'rovi bir nechta qatorni indeks bo'yicha oladi, analitik so'rov esa million qatorni skanerlab agregat qiladi. Ikkinchisi buffer cache ni to'ldirib yuboradi, uzoq tranzaksiya ushlab vacuum ni to'xtatadi va I/O navbatini egallaydi.

Ajratishning to'rt darajasi bor va narxi ortib boradi. Tartib bo'yicha yuriladi: keyingi darajaga faqat avvalgisi yetmaganda o'tiladi.

| Daraja | Nima qilinadi | Qachon yetarli | Narxi |
|---|---|---|---|
| 1 | So'rovni tuzatish, indeks, materiallashgan ko'rinish | hisobot soni kam, ma'lumot hajmi o'rtacha | arzon, kod va migratsiya |
| 2 | O'qish uchun standby ga yo'naltirish (26.8, 26.11) | hisobot eskirgan ma'lumotga toqat qiladi | replikatsiya lag va uning oqibatlari |
| 3 | Alohida hisobot bazasi, mantiqiy replikatsiya yoki CDC bilan to'ldiriladi (26.9) | sxema analitika uchun boshqacha bo'lishi kerak | ikkinchi baza, lag, sxema ikkilanishi |
| 4 | Ustun ko'rinishida saqlaydigan ombor (warehouse), CDC quvuri bilan | hajm terabaytga chiqdi yoki so'rov minutlab yuradi | yangi tizim, yangi operatsion yuk |

Ikkinchi darajada eng ko'p qiladigan xato: hisobotni standby ga yuborib, lag ni hisobga olmaslik. Standby da ochilgan uzun hisobot tranzaksiyasi primary dagi vacuum natijasini qo'llashni to'sadi va `max_standby_streaming_delay` tugaganda so'rov `ERROR: canceling statement due to conflict with recovery` bilan uziladi. Ikki yo'l bor: `hot_standby_feedback` ni yoqib primary da kerakli versiyalarni ushlab turish (bloat o'sadi) yoki standby da kechikish chegarasini oshirish (lag o'sadi). Ikkisi ham bepul emas va tanlov hisobotning eskirishga toqati bilan o'lchanadi.

Uchinchi va to'rtinchi darajada qaror sxema haqida bo'ladi, nusxa haqida emas: analitik sxema normal shaklda emas, u takrorlangan va oldindan agregat qilingan bo'ladi. Shu sababli "bir xil sxemani ikkinchi bazaga nusxalash" oraliq yechim bo'lib qoladi: so'rovlar baribir join qilaveradi. CDC quvuri qurilganda esa hodisa tartibi va aniq bir marta semantikasi masalasi chiqadi, u [tranzaksion outbox](../patterns/10-malumotlarni-boshqarish-va-taqsimlash.md#1014-tranzaksion-outbox-transactional-outbox) va Kafka kafolatlari bilan birga qaror qilinadi.

Qaysi darajada turish kerakligini ikki raqam aytadi: eng sekin hisobotning p95 vaqti va shu hisobot yurganda OLTP so'rovlarining p95 ga qo'shilgan vaqt. Ikkinchisi sezilarli bo'lsa, darajani oshirish vaqti keldi.

## 26.14 Izchil prefiks o'qishi: bitta WAL oqimi kafolat beradi, ko'p manba bermaydi

Replikatsiya kechikishining uchinchi anomaliyasi sabab-natija tartibini buzadi. Kleppmann misolda savol va javobni ko'rsatadi: javob kichik lag bilan kelgan replikadan, savol katta lag bilan kelgan replikadan o'qilsa, kuzatuvchi javobni savoldan oldin ko'radi. Buni to'sadigan kafolat izchil prefiks o'qishi deb ataladi: yozuvlar ma'lum tartibda sodir bo'lgan bo'lsa, ularni o'qigan har kim shu tartibda ko'rishi kerak (*Designing Data-Intensive Applications*, 5-bob, 165-166-betlar).

Muhim shart kitobda aniq aytilgan: agar baza yozuvlarni har doim bir xil tartibda qo'llasa, o'qish har doim izchil prefiks ko'radi va bu anomaliya umuman yuzaga kelmaydi; muammo partitsiyalangan bazada chiqadi, chunki partition lar mustaqil ishlaydi va yozuvlarning global tartibi yo'q (5-bob, 166-bet). Yechim sifatida kitob sabab bilan bog'langan yozuvlarni bitta partition ga yozishni taklif qiladi (5-bob, 166-bet).

PostgreSQL arxitektori uchun bundan ikki aniq xulosa chiqadi. Birinchi: bitta primary va uning standby lari bu anomaliyadan xoli, chunki uzatiladigan narsa bitta ketma-ket WAL oqimi va standby uni ayni shu tartibda replay qiladi. Ya'ni [standby dan o'qishdagi muammo](#268-oqishni-standby-ga-yonaltirish-va-replikatsiya-lag-dan-kelib-chiqadigan-xatolar) eskirgan ma'lumot, teskari tartib emas.

Ikkinchi: anomaliya ikki mustaqil manbadan o'qiganda qaytib keladi. Buyurtma PostgreSQL da, uning hodisalari Kafka da bo'lsa yoki ikki shard ikki alohida klaster bo'lsa, ikki oqimning lag i boshqa va UI javobni savoldan oldin ko'rsatadi. Shuning uchun bitta ekranda ikki manbani birlashtirish qarori lag farqini hisobga olishi kerak.

```java
// Bir ekran ikki manbadan o'qisa, tartibni manbaga tashlab qo'yish xato.
// Ikki yo'l bor: bitta manbaga yopish, yoki yozuvni LSN bilan filtrlash.
@Transactional(readOnly = true)
public OrderView load(long orderId, long minVisibleLsn) {
    // Standby shu LSN ga yetmagan bo'lsa, primary dan o'qiymiz.
    String lsn = jdbc.queryForObject("SELECT pg_last_wal_replay_lsn()::text",
                                     String.class);
    DataSource target = isBehind(lsn, minVisibleLsn) ? primary : replica;
    return orderQuery.on(target).byId(orderId);
}
```

O'z yozuvini o'qish va monoton o'qish kafolatlarining to'liq yozuvi dizayn patternlar hujjatida: [o'z yozuvingni o'qish konsistentligi](../patterns/28-taqsimlangan-malumot-replikatsiya-va.md#2815-oz-yozuvingni-oqish-konsistentligi-read-your-writes-consistency) va [monoton o'qishlar](../patterns/28-taqsimlangan-malumot-replikatsiya-va.md#2816-monoton-oqishlar-monotonic-reads).

## 26.15 Replikatsiya logining to'rt turi va PostgreSQL versiya yangilashdagi oqibati

Kleppmann leader asosidagi replikatsiyani to'rt xil log formati bilan ko'rsatadi va har birining buziladigan joyini sanaydi (*Designing Data-Intensive Applications*, 5-bob, 158-161-betlar). Statement asosidagi replikatsiyada leader bajargan SQL ni izdoshga yuboradi va u `now()` yoki `random()` kabi nodeterministik funksiyada, autoincrement ustunda va trigger yon ta'sirida buziladi (5-bob, 158-159-betlar). WAL shipping da storage engine ning o'z formati uzatiladi, logical log da satr darajasidagi o'zgarishlar uzatiladi, trigger asosidagi replikatsiyada esa o'zgarish ilova kodi bilan alohida jadvalga yoziladi (5-bob, 159-161-betlar).

Arxitektor uchun eng qimmat gap WAL shipping haqida: u storage engine ichki tuzilishiga bog'langani uchun leader va izdoshning bir xil versiyada ishlashini talab qiladi, logical log esa shu bog'liqlikdan xoli va leader bilan izdoshga turli versiyada ishlash imkonini beradi (5-bob, 159-160-betlar). Shu sababli PostgreSQL da major versiya yangilash streaming replikatsiya bilan qilinmaydi va mantiqiy replikatsiya bilan qilinadi: PostgreSQL hujjati turli major versiyalar orasida replikatsiyani mantiqiy replikatsiyaning maqsadli holatlaridan biri deb sanaydi.

| Log turi | PostgreSQL dagi ko'rinishi | Nima beradi | Nimada buziladi |
|---|---|---|---|
| Statement | Yo'q | - | Nodeterministik funksiya, trigger |
| WAL shipping | [Streaming replikatsiya](#266-streaming-replikatsiya-primary-va-standby-lag-olchash) | Bayt aniqligida nusxa, eng arzon | Bir xil major versiya, butun klaster yoki hech narsa |
| Logical (satr) | [`pgoutput` va mantiqiy replikatsiya](#269-mantiqiy-replikatsiya-va-cdc-uchun-asos) | Jadval tanlash, versiyalar orasi, CDC | DDL ko'chmaydi, sequence ko'chmaydi |
| Trigger | Bucardo kabi vositalar | To'liq moslashuv va konflikt mantiqi | Yuqori xarajat, xatoga moyil |

```sql
-- Major versiyani to'xtashsiz yangilash yo'li: mantiqiy replikatsiya.
-- 16 da (manba):
ALTER SYSTEM SET wal_level = 'logical';   -- keyin restart
CREATE PUBLICATION upgrade_pub FOR ALL TABLES;

-- 17 da (yangi klaster): sxema oldin qo'lda ko'chiriladi, keyin
CREATE SUBSCRIPTION upgrade_sub
  CONNECTION 'host=pg16 dbname=app user=repl'
  PUBLICATION upgrade_pub;

-- Yetib olganini tekshirish: lag nolga yaqinlashishi kerak
SELECT subname, latest_end_lsn, latest_end_time
FROM pg_stat_subscription;
```

Trigger asosidagi replikatsiyani bugun yangi loyihada tanlash deyarli har doim xato: Kleppmann uning xarajati boshqa usullardan yuqori va xato hamda cheklovlarga moyilroq ekanini aytadi, lekin moslashuvchanligi tufayli ba'zan foydali deb qo'shadi (5-bob, 161-bet). Amalda u faqat `pgoutput` yetmagan holatda, masalan konflikt yechimi ilova mantiqini talab qilganda qoladi.

## 26.16 Qiyshiq yuklama va issiq partition: hash bo'yicha bo'lish yetmaydi

Kalitni hash qilish issiq nuqtani kamaytiradi, lekin yo'q qilmaydi: hamma o'qish va yozish bitta kalitga tushsa, bir xil ID ning hash i ham bir xil bo'lgani uchun hamma so'rov baribir bitta partition ga boradi; Kleppmann misol sifatida millionlab obunachisi bor mashhur foydalanuvchini keltiradi (*Designing Data-Intensive Applications*, 6-bob, 205-bet).

Kitob javobni ham beradi va uning narxini ham. Bugungi ko'p tizim qiyshiq yuklamani o'zi muvozanatlay olmaydi, shuning uchun qiyshiqlikni kamaytirish ilovaning ishi: issiq kalit oldiga yoki orqasiga tasodifiy son qo'shiladi, ikki raqamli tasodifiy son yozuvlarni 100 ta turli kalitga teng yoyadi. Narxi uchta: o'qish endi 100 kalitdan o'qib natijani birlashtirishi kerak; bu usul faqat kam sonli issiq kalit uchun oqlanadi; va qaysi kalit bo'linganini hisobga olib yurish uchun alohida yozuv kerak bo'ladi (6-bob, 205-bet).

PostgreSQL da bu ikki boshqa muammoga ajraladi va ularni aralashtirmaslik kerak. Birinchisi partition hajmi qiyshiqligi: hash partitioning distinct kalitlarni yoyadi, shuning uchun bitta tenant butun jadvalning yarmini egallasa, hash ham yordam bermaydi. Ikkinchisi issiq qator: bitta qatorga tushgan parallel `UPDATE` lar partition emas, lock navbati muammosi va uni [qator lock lari bobi](22-mvcc-izolyatsiya-darajalari-lock-va-deadlock.md#226-qator-darajasidagi-lock-for-update-for-no-key-update-skip-locked) hal qiladi.

```sql
-- 1-qadam: qiyshiqlikni o'lchash, taxmin qilmaslik.
SELECT c.relname AS partition,
       s.n_live_tup,
       pg_size_pretty(pg_total_relation_size(c.oid)) AS hajm
FROM pg_class c
JOIN pg_stat_user_tables s ON s.relid = c.oid
WHERE c.relispartition
ORDER BY s.n_live_tup DESC;

-- 2-qadam: issiq hisoblagichni Kleppmann usuli bilan yoyish.
-- Bitta qator o'rniga 16 ta bo'lak, yozuv tasodifiy bo'lakka tushadi.
CREATE TABLE post_like_counter (
    post_id  bigint NOT NULL,
    shard_id smallint NOT NULL CHECK (shard_id BETWEEN 0 AND 15),
    cnt      bigint NOT NULL DEFAULT 0,
    PRIMARY KEY (post_id, shard_id)
);

-- Yozuv: lock faqat bitta bo'lakka tushadi.
INSERT INTO post_like_counter (post_id, shard_id, cnt)
VALUES (4215, floor(random() * 16)::smallint, 1)
ON CONFLICT (post_id, shard_id) DO UPDATE SET cnt = post_like_counter.cnt + 1;

-- O'qish: endi agregat kerak, bu kitobda aytilgan narxning aynan o'zi.
SELECT sum(cnt) FROM post_like_counter WHERE post_id = 4215;
```

Qoida: bo'laklashni butun jadvalga qo'ymang. Faqat o'lchov issiq kalitni ko'rsatganda va shu kalitlar ro'yxati alohida saqlanganda qo'llang, aks holda har o'qishga qo'shilgan agregat bepul kelgan sekinlikka aylanadi.

## 26.17 Sekundar indeksni bo'lish: lokal va global indeks

Partitsiyalangan jadvalda sekundar indeks ikki xil joylashtiriladi va Kleppmann ularni ajratib nomlaydi. Hujjat bo'yicha bo'lish (lokal indeks) da har bir partition faqat o'zidagi qatorlar uchun indeks yuritadi: yozish arzon, chunki faqat bitta partition ga tegiladi, lekin indeks ustidan qidirish hamma partition ga so'rov yuborib natijalarni birlashtirishni talab qiladi va bu scatter/gather deb ataladi hamda tail latency kuchayishiga moyil (*Designing Data-Intensive Applications*, 6-bob, 206-207-betlar). Term bo'yicha bo'lish (global indeks) da indeks butun ma'lumotni qamraydi va o'zi alohida bo'linadi: o'qish bitta partition ga boradi, lekin bitta hujjat yozilishi indeks ning bir nechta partition iga tegadi, demak yozish sekinlashadi va ideal holda taqsimlangan tranzaksiya talab qiladi; shu sababli amalda global indeks yangilanishi ko'pincha asinxron bo'ladi (6-bob, 208-209-betlar).

PostgreSQL bu tanlovni bermaydi: deklarativ partitioning da indeks har doim lokal. Partitsiyalangan jadvalda yaratilgan indeks "virtual", haqiqiy ma'lumot esa har partition ning o'z child indeksida yashaydi. Shundan `UNIQUE` cheklovining ma'lum chegarasi kelib chiqadi: PostgreSQL hujjati sababni ochiq yozadi, cheklovni tashkil etuvchi alohida indekslar faqat o'z partition i ichida yakkalikni ta'minlay oladi, shuning uchun cheklov ustunlari partition kalitini to'liq o'z ichiga olishi shart.

```sql
-- Bu ishlamaydi: email bo'yicha global yakkalik mumkin emas.
CREATE TABLE app_user (
    id         bigserial,
    email      text NOT NULL,
    created_at timestamptz NOT NULL,
    UNIQUE (email)                  -- ERROR: unique constraint on partitioned
) PARTITION BY RANGE (created_at);  -- table must include all partitioning columns

-- Global yakkalik kerak bo'lsa: alohida, partitsiyalanmagan indeks jadvali.
CREATE TABLE user_email_index (
    email   text PRIMARY KEY,
    user_id bigint NOT NULL
);
-- Yozuv ikki jadvalga bitta mahalliy tranzaksiyada tushadi.

-- Lokal indeks ustidan qidirish scatter/gather beradi: EXPLAIN da
-- Append ostida har partition uchun alohida Index Scan ko'rinadi.
EXPLAIN (ANALYZE, COSTS OFF)
SELECT * FROM app_user WHERE email = 'a@b.uz';
```

Arxitektor qarori ikki qatorda yoziladi. Agar so'rovlarning katta qismi partition kalitini bermasa, partitioning o'qishni sekinlashtiradi, chunki har so'rov hamma partition ga tarqaydi; bu holda partitioning qarori qayta ko'riladi. Agar global yakkalik biznes talabi bo'lsa, u sxemaga alohida indeks jadvali sifatida kiritiladi va uning yozuvi asosiy jadval bilan bir tranzaksiyada ketadi; pattern yozuvi [indeks jadvali bo'limida](../patterns/10-malumotlarni-boshqarish-va-taqsimlash.md#1019-indeks-jadvali-index-table).

## 26.18 Qayta balanslash strategiyalari va `hash mod N` nega yaramaydi

Qayta balanslash deganda yuklamani bir node dan boshqasiga ko'chirish tushuniladi va Kleppmann uning uchta minimal talabini beradi: natijada yuk node lar orasida adolatli taqsimlanadi, jarayon davomida baza o'qish va yozishni qabul qilishda davom etadi, va zarur bo'lganidan ko'p ma'lumot ko'chirilmaydi (*Designing Data-Intensive Applications*, 6-bob, 209-bet).

Shundan keyin kitob to'rtta strategiyani solishtiradi. `hash mod N` yaramaydi, chunki N o'zgarsa kalitlarning katta qismi joyini o'zgartiradi: kitob misolida `hash(key) = 123456` 10 node da 6-node ga, 11 node da 3-node ga, 12 node da 0-node ga tushadi (6-bob, 210-bet). Belgilangan partition soni ishlaydi: node lardan ancha ko'p partition yaratiladi va yangi node har mavjud node dan bir nechta partition ni oladi, partition larning kalitga bog'lanishi esa umuman o'zgarmaydi (6-bob, 210-211-betlar). Dinamik partitioning da partition hajmi oshganda bo'linadi, node soniga proportsional strategiyada esa har node ga qat'iy sondagi partition to'g'ri keladi (6-bob, 211-212-betlar).

Qayta balanslashni avtomatlashtirish haqida kitobning ogohlantirishi aniq: avtomatik qayta balanslash avtomatik nosozlik aniqlash bilan birga xavfli, chunki ortiqcha yuklangan node sekin javob bersa, qolganlar uni o'lgan deb hisoblab yukni ko'chira boshlaydi va bu kaskadli nosozlikka olib keladi; shu sababli jarayonda odam bo'lishi foydali (6-bob, 213-214-betlar).

PostgreSQL ning deklarativ hash partitioning i aynan `hash mod N`: partition `MODULUS` va `REMAINDER` bilan belgilanadi va kalit hash ining shu modulusga bo'lingandagi qoldig'i partition ni tanlaydi. Demak modulusni keyin oshirish ma'lumotni ko'chirishni talab qiladi va bu o'sha kitobda tasvirlangan qimmat holat.

```sql
-- Modulus boshida tanlanadi va keyin o'zgartirish qimmat: kitobdagi
-- "belgilangan partition soni" strategiyasini oldindan qo'llash kerak.
CREATE TABLE event (id bigserial, tenant_id bigint NOT NULL, payload jsonb)
    PARTITION BY HASH (tenant_id);

-- 4 node uchun 4 ta emas, 32 ta partition: keyin node qo'shilsa
-- butun partition ko'chadi, kalit taqsimoti o'zgarmaydi.
DO $$
BEGIN
  FOR i IN 0..31 LOOP
    EXECUTE format(
      'CREATE TABLE event_p%s PARTITION OF event
         FOR VALUES WITH (MODULUS 32, REMAINDER %s)', i, i);
  END LOOP;
END $$;
```

Amaliy xulosa: hash partitioning tanlangan bo'lsa, modulus kelgusi eng katta node soniga qarab emas, undan ancha katta va bo'linadigan sonda olinadi (32 yoki 64 amaliy boshlang'ich nuqta, o'lchanmagan taxmin), chunki keyin uni o'zgartirish `DETACH`, ko'chirish va `ATTACH` zanjirini talab qiladi. Partition soni bepul emas: har biri planlashtirish va autovacuum xarajati qo'shadi, shuning uchun [partition pruning](#263-partition-pruning-qachon-ishlaydi-va-qachon-ishlamaydi) ishlashi tekshirilgan bo'lishi kerak.

## 26.19 So'rovni yo'naltirish: uch yondashuv va PostgreSQL dagi ko'rinishi

Ma'lumot node lar bo'ylab bo'lingandan keyin ochiq savol qoladi: mijoz qaysi node ga ulanishini qanday biladi. Kleppmann buni service discovery muammosining bir holati deb ataydi va uchta yondashuvni sanaydi: mijoz istalgan node ga murojaat qiladi va node kerak bo'lsa so'rovni egasiga uzatadi; hamma so'rov avval marshrutlash qatlamiga boradi va u partition dan xabardor load balancer rolini o'ynaydi; yoki mijozning o'zi partition taqsimotini biladi va to'g'ridan to'g'ri kerakli node ga ulanadi (*Designing Data-Intensive Applications*, 6-bob, 214-215-betlar). Hamma holatda asosiy muammo bitta: marshrut qarorini qabul qiladigan komponent taqsimot o'zgarishini qanday bilib oladi (6-bob, 214-bet).

PostgreSQL ekosistemasida uchala yondashuv ham bor va tanlov operatsion og'irlik bilan o'lchanadi. Marshrutlash qatlami eng tanish variant: PgBouncer yoki HAProxy primary ni biladi va failover dan keyin konfiguratsiya yangilanadi. Mijoz tomonida yo'naltirish esa JDBC drayverining o'zida mavjud: ulanish satrida bir nechta host yoziladi va drayver yozishga ruxsat beradigan host ni topib oladi.

```properties
# Mijoz tomonida yo'naltirish: drayver primary ni o'zi topadi.
# targetServerType default qiymati any, shuning uchun uni aniq yozish shart.
spring.datasource.url=jdbc:postgresql://pg-a:5432,pg-b:5432/app?targetServerType=primary
spring.datasource.hikari.maximum-pool-size=10

# O'qish uchun ikkinchi pool: ikkilamchi host ga moyillik va tasodifiy tanlov.
# loadBalanceHosts default false, hostRecheckSeconds default 10.
app.read.url=jdbc:postgresql://pg-a:5432,pg-b:5432/app?targetServerType=preferSecondary&loadBalanceHosts=true
```

Uchinchi yondashuv, ya'ni node ning o'zi so'rovni uzatishi, PostgreSQL da Citus coordinator node ko'rinishida uchraydi: ilova coordinator ga ulanadi, u shard taqsimotini biladi va so'rovni worker node larga tarqatadi. Narxi shu bitta coordinator ning yangi nosozlik nuqtasi bo'lishida.

Kitob bu bo'limni parallel so'rov bajarilishi bilan yopadi: MPP bazalarda so'rov optimizatori murakkab so'rovni bir nechta bajarilish bosqichiga ajratadi va ularning ko'pini turli node larda parallel bajaradi, bu esa ma'lumotning katta qismini skan qiladigan so'rovlarga ayniqsa foyda beradi (6-bob, 216-bet). Bitta PostgreSQL ichida bunga mos narsa `Gather` va `Parallel Seq Scan` tugunlari, ya'ni bitta mashina ichidagi parallellik; uning chegaralari [planner bobida](24-planner-statistika-va-explain-analyze-oqish.md) va [sozlash bobida](27-sozlash-connection-pool-va-monitoring.md) ko'rib chiqiladi.

Qoida: yo'naltirish qarori bitta joyda yozilgan va testda tekshirilgan bo'lishi kerak. Ikki joyda, masalan ham PgBouncer da ham `targetServerType` da, bir-biriga qarama-qarshi yo'naltirish bo'lsa, failover paytida yozuvlar standby ga tushib xato beradi va sabab topilmaydi.

## 26.20 Amalda qo'llash

- [ ] Eng katta 10 jadval uchun `pg_total_relation_size` va `n_live_tup` ni o'lchab, 50 GB dan katta va vaqt bo'yicha o'qiladiganlar ro'yxatini tuzing.
- [ ] Bitta nomzod jadvalni range partitioning ga o'tkazish rejasini yozing: kalit, PK o'zgarishi, `NOT VALID` check, `ATTACH`, nom almashtirish qadamlari bilan.
- [ ] Retention jobni `DELETE` dan `DETACH PARTITION CONCURRENTLY` + `DROP TABLE` ga almashtiring va `lock_timeout` qo'ying.
- [ ] Eng og'ir 5 ta hisobot so'rovini `EXPLAIN ANALYZE` bilan tekshirib, `Subplans Removed` qatorini ko'rib pruning ishlashini tasdiqlang.
- [ ] `pg_stat_replication` dagi `replay_lag` va `pg_replication_slots` dagi slot lag uchun alert qo'ying, `max_slot_wal_keep_size` ni belgilang.
- [ ] `synchronous_standby_names` ni `ANY 1 (a, b)` shaklida kvorumga o'tkazing va bitta standby o'chganda yozish to'xtamasligini sinab ko'ring.
- [ ] O'qish uchun alohida DataSource ni `LazyConnectionDataSourceProxy` bilan sozlang, pool o'lchamlarini yozish uchun 10, o'qish uchun 20 qilib ajratib qo'ying.
- [ ] Yozishdan keyingi o'qishni primary ga yo'naltiruvchi qoida kiritib, lag sababli ko'rinmagan yozuv ssenariysini testda qayd eting.
- [ ] Eng sekin hisobotni toping va u yurganda OLTP so'rovlarining p95 ga qancha qo'shilayotganini o'lchang.
- [ ] Standby da hisobot yuritayotgan bo'lsangiz, `hot_standby_feedback` va `max_standby_streaming_delay` qarorini yozib qo'ying.

## Manbalar

- Martin Kleppmann, *Designing Data-Intensive Applications*, 6-bob - partitioning strategiyalari va qayta balanslash
- Martin Kleppmann, *Designing Data-Intensive Applications*, O'Reilly, 2017, 5-bob (158-166-betlar) - replikatsiya logining to'rt turi, WAL shipping ning bir xil versiya talabi, logical log ning versiyalar orasida ishlashi va izchil prefiks o'qishi
- Martin Kleppmann, *Designing Data-Intensive Applications*, O'Reilly, 2017, 6-bob (205-216-betlar) - qiyshiq yuklama va issiq kalitni tasodifiy son bilan yoyish, sekundar indeksni hujjat va term bo'yicha bo'lish, `hash mod N` ning kamchiligi, belgilangan partition soni, avtomatik qayta balanslashning xavfi va so'rovni yo'naltirishning uch yondashuvi
- [PostgreSQL 17, Table Partitioning limitations (ddl.sgml)](https://raw.githubusercontent.com/postgres/postgres/REL_17_STABLE/doc/src/sgml/ddl.sgml) - partitsiyalangan jadvaldagi indeks virtual va har partition ning o'z child indeksida yashashi, `UNIQUE` cheklovi partition kalitini to'liq o'z ichiga olishi shartligi, `MODULUS` va `REMAINDER` bilan hash partitioning
- [PostgreSQL 17, Logical Replication (logical-replication.sgml)](https://raw.githubusercontent.com/postgres/postgres/REL_17_STABLE/doc/src/sgml/logical-replication.sgml) - turli major versiyalar orasida replikatsiya mantiqiy replikatsiyaning maqsadli holatlaridan biri ekani
- [pgjdbc 42.7.4, Connecting to the Database (use.md)](https://raw.githubusercontent.com/pgjdbc/pgjdbc/REL42.7.4/docs/content/documentation/use.md) - `targetServerType` default `any`, `loadBalanceHosts` default `false`, `hostRecheckSeconds` default 10
- Martin Kleppmann, *Designing Data-Intensive Applications*, 5-bob - replikatsiya: yetakchi-izdosh, replikatsiya kechikishi
- [PostgreSQL 17, Table Partitioning (ddl.sgml)](https://raw.githubusercontent.com/postgres/postgres/REL_17_STABLE/doc/src/sgml/ddl.sgml) - partitioning turlari va chegaralari
- [PostgreSQL 17, High Availability (high-availability.sgml)](https://raw.githubusercontent.com/postgres/postgres/REL_17_STABLE/doc/src/sgml/high-availability.sgml) - streaming replikatsiya, sinxron rejim va failover
- [PostgreSQL 17, Hot Standby (high-availability.sgml)](https://raw.githubusercontent.com/postgres/postgres/REL_17_STABLE/doc/src/sgml/high-availability.sgml) - `hot_standby_feedback`, `max_standby_streaming_delay` va tiklanish bilan konflikt
- Martin Kleppmann, *Designing Data-Intensive Applications*, 3-bob - OLTP va analitik yuk farqi, ustunli saqlash

---

[&larr; 25. Sxema dizayni, ma'lumot turlari va cheklovlar](25-sxema-dizayni-malumot-turlari-va-cheklovlar.md) · [Mundarija](README.md) · [27. Sozlash, connection pool va monitoring &rarr;](27-sozlash-connection-pool-va-monitoring.md)
