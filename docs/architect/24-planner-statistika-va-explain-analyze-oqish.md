<!-- doc: architect | chapter: 24 | part: IV. PostgreSQL chuqur bilim -->

[Kod yozadigan arxitektorning miyyasi](../../README.md) / [Arxitektor miyyasi](README.md)

# 24. Planner, statistika va EXPLAIN ANALYZE o'qish (Planner and EXPLAIN ANALYZE)

<details>
<summary>Bu bobdagi 13 bo'lim</summary>

- [24.1 Planner nima qiladi: variantlar, narx modeli, tanlov](#241-planner-nima-qiladi-variantlar-narx-modeli-tanlov)
- [24.2 Statistika qayerdan keladi: `ANALYZE`, `pg_statistic`, `default_statistics_target`](#242-statistika-qayerdan-keladi-analyze-pg_statistic-default_statistics_target)
- [24.3 Narx parametrlari: `random_page_cost`, `seq_page_cost`, `effective_cache_size` ma'nosi](#243-narx-parametrlari-random_page_cost-seq_page_cost-effective_cache_size-manosi)
- [24.4 Skan turlari: sequential, index, index-only, bitmap heap scan](#244-skan-turlari-sequential-index-index-only-bitmap-heap-scan)
- [24.5 Join algoritmlari: nested loop, hash join, merge join va qachon qaysi biri tanlanadi](#245-join-algoritmlari-nested-loop-hash-join-merge-join-va-qachon-qaysi-biri-tanlanadi)
- [24.6 `EXPLAIN (ANALYZE, BUFFERS)` chiqishini satrma-satr o'qish](#246-explain-analyze-buffers-chiqishini-satrma-satr-oqish)
- [24.7 Taxmin qilingan va haqiqiy qator soni farqi: eng muhim signal](#247-taxmin-qilingan-va-haqiqiy-qator-soni-farqi-eng-muhim-signal)
- [24.8 Ko'p ustunli statistika (`CREATE STATISTICS`) va bog'liq ustunlar muammosi](#248-kop-ustunli-statistika-create-statistics-va-bogliq-ustunlar-muammosi)
- [24.9 Parametrlashtirilgan so'rov va generic plan muammosi (`plan_cache_mode`)](#249-parametrlashtirilgan-sorov-va-generic-plan-muammosi-plan_cache_mode)
- [24.10 `pg_stat_statements` bilan eng qimmat so'rovlarni topish](#2410-pg_stat_statements-bilan-eng-qimmat-sorovlarni-topish)
- [24.11 So'rovni qayta yozish: `EXISTS`, `LATERAL`, `DISTINCT ON`, CTE va materializatsiya](#2411-sorovni-qayta-yozish-exists-lateral-distinct-on-cte-va-materializatsiya)
- [24.12 Sekin so'rovni tekshirish tartibi: aniq qadamlar ro'yxati](#2412-sekin-sorovni-tekshirish-tartibi-aniq-qadamlar-royxati)
- [24.13 Amalda qo'llash](#2413-amalda-qollash)

</details>


PostgreSQL planner so'rovni qanday bajarishni o'zi tanlaydi va bu tanlov statistikaga asoslangan taxminlar ustiga qurilgan. Arxitektor uchun muhim narsa index qo'shish emas, balki planner nimaga ishonib shu rejani tanlaganini o'qib tushunish. `EXPLAIN (ANALYZE, BUFFERS)` chiqishi aynan shu ishonchni va haqiqatni yonma-yon ko'rsatadigan yagona vosita. Bu bobda planner mexanikasi, narx modeli, skan va join turlari, hamda sekin so'rovni tartib bilan tekshirish usuli ko'rib chiqiladi.

## 24.1 Planner nima qiladi: variantlar, narx modeli, tanlov

Parser SQL matnini daraxtga aylantiradi, rewriter view va rule'larni ochadi, keyin planner ishga tushadi. Planner bir xil natijani beradigan ko'plab jismoniy rejalarni generatsiya qiladi: har bir jadval uchun skan usuli, har bir juftlik uchun join algoritmi, join tartibi, agregatsiya va sort joyi. Har bir variantga narx beriladi va eng arzoni tanlanadi.

Narx birligi sekund emas, shartli son. Bazasi `seq_page_cost = 1.0`, ya'ni ketma-ket o'qilgan bitta 8 kB sahifa narxi. Qolgan hamma parametr shunga nisbatan o'lchanadi. Narx ikki qismdan: `startup cost` (birinchi qator chiqishidan oldingi ish) va `total cost` (barcha qatorlar). `LIMIT` bo'lsa planner total narxning faqat bir ulushini hisoblaydi, shuning uchun `LIMIT 20` bilan va `LIMIT` siz rejalar butunlay boshqacha bo'lishi mumkin.

Join tartibi uchun jadval soni 8 dan oshsa (`geqo_threshold`), to'liq dinamik programmalash o'rniga genetik algoritm ishlaydi va reja barqaror bo'lmay qoladi. 12 ta jadvalli hisobot so'rovi har deploy'dan keyin boshqa reja olishi mumkin, bu esa "kecha ishlagan, bugun ishlamaydi" muammosining tipik manbasi. Arxitektor qarori: katta hisobotni bir nechta bosqichga bo'lish yoki oldindan hisoblangan jadvaldan o'qish.

## 24.2 Statistika qayerdan keladi: `ANALYZE`, `pg_statistic`, `default_statistics_target`

Planner qator sonini jadvalni o'qib bilmaydi, u `pg_statistic` dagi namunaviy statistikaga qaraydi. Uni `ANALYZE` yig'adi: jadvaldan `300 * statistics_target` ta qator tasodifiy olinadi, ya'ni standart 100 da 30000 qator. Shu namunadan har bir ustun uchun null ulushi, o'rtacha kenglik, eng tez uchraydigan qiymatlar ro'yxati va histogram chegaralari saqlanadi.

Autovacuum o'z ichida autoanalyze ishlatadi va standart shart: o'zgargan qator soni jadval hajmining 10 foizidan oshsa. 50 million qatorli `orders` jadvalida bu 5 million qator degani, demak statistika kunlar davomida eskirgan holda qoladi. Katta jadvalda chegarani qo'lda pasaytirish kerak.

```sql
-- Namuna hajmini oshirish: notekis taqsimlangan ustunlar uchun
ALTER TABLE orders ALTER COLUMN status SET STATISTICS 500;
ALTER TABLE orders ALTER COLUMN customer_id SET STATISTICS 1000;
ANALYZE orders;              -- o'zgarish faqat ANALYZE dan keyin kuchga kiradi

-- Katta jadvalda autoanalyze tezroq ishlashi uchun
ALTER TABLE orders SET (
  autovacuum_analyze_scale_factor = 0.02,   -- 10% emas, 2%
  autovacuum_analyze_threshold = 50000
);

-- Statistika haqiqatan yangilanganini tekshirish
SELECT relname, last_analyze, last_autoanalyze, n_mod_since_analyze
FROM pg_stat_user_tables
WHERE relname IN ('orders', 'payments', 'stock_items');
```

`default_statistics_target` ni global 100 dan 200 ga oshirish OLTP bazada odatda xavfsiz, lekin `ANALYZE` vaqti va planner ishi ham ortadi. Amaliy qoida: global qiymatni tegmay, muammoli ustunga alohida target berish.

## 24.3 Narx parametrlari: `random_page_cost`, `seq_page_cost`, `effective_cache_size` ma'nosi

`random_page_cost` standart 4.0, bu aylanuvchi diskdan tasodifiy o'qish ketma-ket o'qishdan to'rt baravar qimmat degan taxmin. SSD va NVMe da bu nisbat haqiqatda 1.1 dan 1.5 gacha. Standart qiymatni qoldirish planner'ni index scan'dan qo'rqitadi va u seq scan tanlaydi.

`effective_cache_size` hech qanday xotira ajratmaydi, u faqat planner'ga "operatsion tizim page cache va shared_buffers birgalikda taxminan shuncha ma'lumotni ushlab turadi" deb aytadi. Qiymati kichik bo'lsa planner index scan'da har safar diskka borishni taxmin qiladi va uni qimmat deb baholaydi.

```sql
-- 64 GB RAM li SSD serveri uchun tipik boshlang'ich qiymatlar
ALTER SYSTEM SET random_page_cost = 1.1;        -- SSD uchun
ALTER SYSTEM SET effective_cache_size = '48GB'; -- RAM ning ~75%
ALTER SYSTEM SET effective_io_concurrency = 200;-- NVMe uchun
ALTER SYSTEM SET work_mem = '32MB';             -- har bir sort/hash uchun
SELECT pg_reload_conf();

-- Bitta so'rovni sinash uchun sessiya darajasida
SET LOCAL random_page_cost = 1.1;
EXPLAIN (ANALYZE, BUFFERS) SELECT ...;
```

`work_mem` eng xavfli parametr. U har bir sort, hash va hashagg uchun alohida ajratiladi, demak bitta so'rov 5 ta hash node bilan 5 * work_mem gacha xotira olishi mumkin. 200 ulanishli pool'da global 256MB qo'yish OOM ga olib keladi. Arxitektor yondashuvi: global 32MB, hisobot so'rovidan oldin `SET LOCAL work_mem = '256MB'`.

## 24.4 Skan turlari: sequential, index, index-only, bitmap heap scan

Sequential scan butun jadvalni ketma-ket o'qiydi. Jadval kichik bo'lsa yoki natijaga qatorlarning 10 foizidan ko'pi tushsa, bu eng arzon usul. Seq scan rejada ko'rinishi avtomatik muammo degani emas.

Index scan indeksni aylanib, har bir topilgan qator uchun heap'ga boradi. Tanlovchanlik yuqori bo'lganda (masalan `order_id = ?`) ideal. Index-only scan heap'ga bormaydi, chunki kerakli hamma ustun indeksda bor va sahifa visibility map'da "butunlay ko'rinadigan" deb belgilangan. `VACUUM` ishlamasa visibility map eskiradi va index-only scan ham heap fetch qilishga tushadi.

Bitmap heap scan ikki bosqichli: avval indeksdan mos qatorlarning sahifa bitmap'i quriladi, keyin heap jismoniy tartibda o'qiladi. Bu bir necha ming qator qaytaradigan so'rovlar uchun eng samarali usul, chunki tasodifiy o'qish ketma-ket o'qishga aylanadi. `Heap Blocks: exact=... lossy=...` satrida `lossy` ko'rinsa, bitmap `work_mem` ga sig'magan va sahifa darajasiga qo'pollashgan, natijada ortiqcha qator filtrlanadi.

## 24.5 Join algoritmlari: nested loop, hash join, merge join va qachon qaysi biri tanlanadi

Nested loop tashqi qatorning har biri uchun ichki tomonni qayta izlaydi. Ichki tomonda index bo'lsa va tashqi tomon kichik bo'lsa, bu eng tez va eng kam xotira talab qiladigan usul. Xatar: tashqi qator soni noto'g'ri taxmin qilinsa, 50 ta `loops` o'rniga 500000 ta `loops` bo'ladi va so'rov 1000 baravar sekinlashadi. Deyarli barcha "kutilmaganda sekinlashgan so'rov" hodisasi shu.

Hash join kichik tomondan xotirada hash jadval quradi, keyin katta tomonni bir marta o'tadi. Katta to'plamlarni tenglik shartida birlashtirish uchun eng yaxshi tanlov. Hash `work_mem` ga sig'masa `Batches` soni 1 dan oshadi va diskka to'kiladi, bu esa `temp read/written` bloklarida ko'rinadi.

Merge join ikki tomonni sortlangan holda parallel o'qiydi. Ikkala tomonda ham mos indeks bo'lsa yoki ma'lumot allaqachon sortlangan bo'lsa arzon, aks holda sort narxi qo'shiladi. Katta hisobotlarda `ORDER BY` bilan birga foydali.

| Holat | Planner tanlovi | Nega |
| --- | --- | --- |
| Tashqi tomon 10 qator, ichkida index | Nested loop | Har bir qidiruv arzon, startup cost nol |
| 2 mln va 500 ming qator, tenglik sharti | Hash join | Bitta o'tish, xotirada hash |
| Ikkala tomon sortlangan, `ORDER BY` bor | Merge join | Sort qayta kerak emas |
| Tenglik emas, `BETWEEN` sharti | Nested loop yoki merge | Hash faqat tenglikni biladi |
| Hash `work_mem` ga sig'maydi | Batched hash join | Diskka to'kilish, sekinlashadi |

## 24.6 `EXPLAIN (ANALYZE, BUFFERS)` chiqishini satrma-satr o'qish

Mijozning oxirgi buyurtmalarini to'lov summasi bilan ko'rsatadigan so'rov. `ANALYZE` so'rovni haqiqatan bajaradi, shuning uchun `UPDATE` yoki `DELETE` ni tekshirganda tranzaksiya ochib, oxirida `ROLLBACK` qilish kerak.

```sql
EXPLAIN (ANALYZE, BUFFERS)
SELECT o.id, o.created_at, p.amount
FROM orders o
JOIN payments p ON p.order_id = o.id
WHERE o.customer_id = 48213
  AND o.created_at >= DATE '2026-09-01'
ORDER BY o.created_at DESC
LIMIT 20;
```

Chiqish quyidagicha bo'ldi:

```text
Limit  (cost=1042.18..1042.23 rows=20 width=28)
       (actual time=318.442..318.449 rows=20 loops=1)
  Buffers: shared hit=812 read=9134
  ->  Sort  (cost=1042.18..1044.90 rows=1088 width=28)
            (actual time=318.440..318.444 rows=20 loops=1)
        Sort Key: o.created_at DESC
        Sort Method: top-N heapsort  Memory: 27kB
        ->  Nested Loop  (cost=0.43..1010.55 rows=1088 width=28)
                         (actual time=0.071..317.902 rows=1042 loops=1)
              Buffers: shared hit=812 read=9134
              ->  Seq Scan on orders o  (cost=0.00..98211.00 rows=54 width=16)
                                        (actual time=0.028..290.114 rows=1007 loops=1)
                    Filter: ((customer_id = 48213)
                             AND (created_at >= '2026-09-01'::date))
                    Rows Removed by Filter: 4198993
              ->  Index Scan using payments_order_id_idx on payments p
                    (cost=0.43..8.45 rows=1 width=20)
                    (actual time=0.023..0.025 rows=1 loops=1007)
                    Index Cond: (order_id = o.id)
Planning Time: 0.214 ms
Execution Time: 318.507 ms
```

Satrlarni ketma-ket o'qiymiz. Eng ichki node birinchi bajariladi, ya'ni pastdan yuqoriga.

`Seq Scan on orders` satri: planner 54 qator kutgan, haqiqatda 1007 qator qaytgan. `Rows Removed by Filter: 4198993` degani jadvalning 4.2 million qatori o'qilib tashlangan. `cost=0.00..98211.00` lekin `LIMIT` borligi uchun to'liq narx hisobga olinmagan. Bu yerdagi 290 ms butun so'rov vaqtining asosiy qismi.

`Index Scan using payments_order_id_idx` satri: `loops=1007`, ya'ni bu node 1007 marta ishga tushgan. Har safar 0.025 ms, umumiy taxminan 25 ms. `actual time` har doim bitta loop uchun o'rtacha qiymat, umumiy vaqtni olish uchun `loops` ga ko'paytirish kerak. Bu eng ko'p yanglishtiradigan joy.

`Nested Loop` satri: 1042 qator chiqargan, 317 ms. Planner 1088 kutgan, bu yaqin. Demak muammo join algoritmida emas.

`Sort` satri: `top-N heapsort  Memory: 27kB`. `LIMIT 20` borligi uchun to'liq sort emas, faqat 20 ta eng kattasi ushlab turilgan. Xotira `work_mem` ga sig'gan, `Disk` so'zi yo'q, demak to'kilish bo'lmagan.

`Buffers: shared hit=812 read=9134` satri: 812 sahifa `shared_buffers` dan olingan, 9134 sahifa cache'da bo'lmagan. 9134 * 8 kB taxminan 71 MB o'qish. Bu `read` soni `hit` dan 11 baravar katta, demak jadval cache'ga sig'mayapti.

`Planning Time: 0.214 ms` reja tuzish vaqti. U `Execution Time` ga yaqinlashsa, ko'p partition yoki ko'p join bor degani.

Tuzatish aniq: `orders(customer_id, created_at DESC)` composite indeksi. Undan keyin seq scan index scan'ga aylanadi va `read` soni yuzlab sahifaga tushadi.

## 24.7 Taxmin qilingan va haqiqiy qator soni farqi: eng muhim signal

Rejada birinchi qaraladigan narsa `rows=N` (taxmin) va `actual rows=M` nisbati. 10 baravardan katta farq planner yomon statistika bilan ishlaganini bildiradi. Yuqoridagi misolda 54 va 1007, ya'ni 18 baravar. Agar tashqi tomonda shunday farq bo'lsa, planner nested loop'ni arzon deb hisoblaydi va u aslida qimmat chiqadi.

Farqning tipik sabablari: eskirgan statistika, bog'liq ustunlar, `LIKE '%...'` shabloni, funksiya ustidagi filtr (`lower(email) = ?`) va ifodaga statistika yo'qligi. Oxirgisining yechimi ifoda uchun index yaratish, chunki ifoda indeksi o'zi bilan statistika ham olib keladi.

| Oddiy yondashuv | Arxitektor yondashuvi |
| --- | --- |
| Sekin so'rovga darhol index qo'shadi | Avval `EXPLAIN (ANALYZE, BUFFERS)` o'qib, qaysi node vaqt yegani aniqlanadi |
| `cost` raqamini millisekund deb o'ylaydi | `cost` shartli birlik, qaror `actual time` va `Buffers` bo'yicha |
| `loops` ni e'tiborsiz qoldiradi | `actual time` ni `loops` ga ko'paytirib haqiqiy ulushni hisoblaydi |
| Seq scan ko'rsa darhol muammo deb biladi | Tanlovchanlikni tekshiradi, 30% natijada seq scan to'g'ri |
| Index sonini oshirib boradi | Har bir index `INSERT` narxi va WAL hajmini oshirishini hisobga oladi |
| `enable_nestloop = off` bilan planner'ni majburlaydi | Statistika va `CREATE STATISTICS` bilan taxminni to'g'rilaydi |
| Prod'da `work_mem` ni global oshiradi | Global kichik qoldirib, hisobot sessiyasida `SET LOCAL` qiladi |
| Faqat o'z lokal bazasida sinaydi | Prod hajmiga yaqin ma'lumotda sinaydi, chunki reja hajmga bog'liq |
| `pg_stat_statements` ga qaramaydi | Eng qimmat 20 so'rovni `total_exec_time` bo'yicha tartiblaydi |
| Bir marta tuzatib yopadi | Reja regressiyasini monitoringga qo'yadi |

## 24.8 Ko'p ustunli statistika (`CREATE STATISTICS`) va bog'liq ustunlar muammosi

Planner standart holda ustunlarni mustaqil deb hisoblaydi va shartlar tanlovchanligini ko'paytiradi. `city = 'Toshkent' AND region = 'Toshkent'` da haqiqatda bitta shart, lekin planner ikkitasini ko'paytirib qator sonini bir necha baravar kam ko'rsatadi. Natijada hash join o'rniga nested loop tanlanadi.

```sql
-- Bog'liq ustunlar uchun kengaytirilgan statistika
CREATE STATISTICS stat_orders_city_region (dependencies, ndistinct)
  ON city, region FROM orders;

-- MCV ro'yxati bilan: qiymat juftliklarining chastotasi saqlanadi
CREATE STATISTICS stat_orders_status_channel (mcv)
  ON status, channel FROM orders;

ANALYZE orders;   -- statistika obyekti ANALYZE dan keyin to'ladi

SELECT s.stxname, d.stxdndistinct, d.stxddependencies
FROM pg_statistic_ext s
JOIN pg_statistic_ext_data d ON d.stxoid = s.oid;
```

`dependencies` funksional bog'liqlikni, `ndistinct` birlashgan unikal qiymat sonini, `mcv` esa eng ko'p uchraydigan juftliklarni saqlaydi. `GROUP BY` ikki ustun bo'yicha bo'lsa `ndistinct` hashagg xotirasini to'g'ri taxmin qilishga yordam beradi.

## 24.9 Parametrlashtirilgan so'rov va generic plan muammosi (`plan_cache_mode`)

Hibernate va JDBC `PreparedStatement` ishlatadi. PostgreSQL bir xil prepared statement bir necha marta bajarilganda custom plan (har safar parametr qiymati bilan) va generic plan (parametrsiz, o'rtacha tanlovchanlik) narxini taqqoslaydi. Beshinchi bajarilishdan keyin generic plan arzon ko'rinsa, unga o'tadi.

Muammo notekis taqsimlangan ustunda chiqadi. `status = 'NEW'` da 500 qator, `status = 'DONE'` da 40 million qator. Generic plan o'rtacha qiymat bilan tuzilgani uchun ikkisining birida juda yomon ishlaydi. Belgisi: so'rov bir necha marta tez ishlaydi, keyin birdan sekinlashadi.

```properties
# Spring Boot: ulanish ochilganda sessiya sozlamasi
spring.datasource.hikari.connection-init-sql=SET plan_cache_mode = force_custom_plan

# PgJDBC: server-side prepare chegarasi (0 bo'lsa server prepare o'chadi)
spring.datasource.hikari.data-source-properties.prepareThreshold=5

# Pool o'lchami: CPU yadrosi * 2 + disk soni, 200 emas
spring.datasource.hikari.maximum-pool-size=20
```

`force_custom_plan` har safar reja tuzadi, bu taxminan 0.2 dan 1 ms qo'shimcha xarajat. OLTP da sekundda minglab so'rov bo'lsa bu sezilarli, shuning uchun uni global emas, muammoli so'rov uchun alohida qo'llash kerak. Alternativa: shu so'rovni native query qilib, qiymatni literal sifatida qo'yish yoki `status` bo'yicha partial index yaratish.

## 24.10 `pg_stat_statements` bilan eng qimmat so'rovlarni topish

`pg_stat_statements` normalizatsiya qilingan so'rovlar bo'yicha chaqirish soni va vaqtni to'playdi. Uni `shared_preload_libraries` ga qo'shish kerak va server restart talab qiladi.

```sql
-- Umumiy vaqt bo'yicha eng qimmat 15 so'rov
SELECT substr(query, 1, 80) AS q,
       calls,
       round(total_exec_time::numeric, 1) AS total_ms,
       round(mean_exec_time::numeric, 2) AS mean_ms,
       rows / GREATEST(calls, 1) AS rows_per_call,
       round(100.0 * shared_blks_hit
             / GREATEST(shared_blks_hit + shared_blks_read, 1), 1) AS hit_pct
FROM pg_stat_statements
WHERE query NOT LIKE '%pg_stat_statements%'
ORDER BY total_exec_time DESC
LIMIT 15;

SELECT pg_stat_statements_reset();  -- deploy oldidan nolga qaytarish
```

Eng muhim tartiblash `mean_exec_time` emas, `total_exec_time`. 0.8 ms ishlaydigan lekin sekundda 5000 marta chaqirilgan so'rov 400 ms ishlaydigan kunlik hisobotdan ko'proq resurs yeydi. `rows_per_call` 1 ga teng va `calls` juda katta bo'lsa, bu Hibernate N+1 muammosining aniq izi.

`auto_explain` moduli chegaradan sekin so'rovlarning rejasini logga yozadi, bu prod'da qayta takrorlanmaydigan sekinlashishni tutish uchun yagona ishonchli yo'l.

```bash
# Logda 500 ms dan sekin so'rovlarning rejasi, namuna olish bilan
psql -c "ALTER SYSTEM SET auto_explain.log_min_duration = '500ms'"
psql -c "ALTER SYSTEM SET auto_explain.log_analyze = on"
psql -c "ALTER SYSTEM SET auto_explain.log_buffers = on"
psql -c "ALTER SYSTEM SET auto_explain.sample_rate = 0.1"   # 10% namuna
psql -c "SELECT pg_reload_conf()"

# Jadval va index hajmini ko'rish
psql -c "SELECT relname, pg_size_pretty(pg_total_relation_size(oid))
         FROM pg_class WHERE relkind='r' ORDER BY pg_total_relation_size(oid) DESC LIMIT 10"
```

## 24.11 So'rovni qayta yozish: `EXISTS`, `LATERAL`, `DISTINCT ON`, CTE va materializatsiya

Ko'pincha index emas, so'rov shakli muammo. `IN (SELECT ...)` o'rniga `EXISTS` ishlatish planner'ga semi-join imkonini beradi va birinchi mos qator topilgach ichki qidiruv to'xtaydi. `LATERAL` har bir tashqi qator uchun "eng oxirgi N ta" ni olishga imkon beradi, bu window funksiya ustidan filtrlashdan arzonroq. `DISTINCT ON` esa guruh ichidan birinchi qatorni olishning eng qisqa va tez usuli.

```sql
-- Har bir mijozning oxirgi 3 to'lovi: LATERAL
SELECT c.id, p.paid_at, p.amount
FROM customers c
CROSS JOIN LATERAL (
    SELECT paid_at, amount FROM payments
    WHERE customer_id = c.id ORDER BY paid_at DESC LIMIT 3
) p
WHERE c.segment = 'B2B';

-- Har bir buyurtmaning oxirgi holati: DISTINCT ON
SELECT DISTINCT ON (order_id) order_id, status, changed_at
FROM order_status_log ORDER BY order_id, changed_at DESC;

-- To'lovi bor buyurtmalar: EXISTS, semi-join
SELECT o.id FROM orders o
WHERE EXISTS (SELECT 1 FROM payments p WHERE p.order_id = o.id AND p.amount > 0);
```

PostgreSQL 12 dan boshlab oddiy CTE inline qilinadi, ya'ni planner uni asosiy so'rov bilan birga optimallashtiradi. `MATERIALIZED` kalit so'zi bilan CTE bir marta hisoblanib vaqtinchalik natijaga yoziladi. Bu CTE bir necha joyda ishlatilganda yoki og'ir agregatsiya bo'lganda foydali, lekin filtr CTE ichiga tushmaydi. Qaror oddiy: bir marta ishlatiladigan va filtr tushishi kerak bo'lgan CTE uchun `NOT MATERIALIZED`, qayta ishlatiladigan og'ir hisob uchun `MATERIALIZED`.

```java
// Hisobot so'rovi uchun sessiya darajasida sozlash va stream o'qish
@Transactional(readOnly = true)
public void exportDailyReport(LocalDate day, Consumer<ReportRow> sink) {
    em.createNativeQuery("SET LOCAL work_mem = '256MB'").executeUpdate();
    var q = em.createQuery(REPORT_JPQL, ReportRow.class)
              .setParameter("day", day)
              .setHint(AvailableHints.HINT_FETCH_SIZE, 500); // kursor bilan o'qish
    try (Stream<ReportRow> rows = q.getResultStream()) {
        rows.forEach(sink);   // hamma natija xotiraga yig'ilmaydi
    }
}
```

| Tuzoq | Belgisi rejada | Yechim |
| --- | --- | --- |
| Noto'g'ri nested loop | `loops` juda katta, tashqi `rows` taxmini past | Statistikani yangilash, composite index |
| Hash diskka to'kilgan | `Batches > 1`, `temp written` | Shu so'rov uchun `work_mem` oshirish |
| Funksiya ustidagi filtr | `Filter` da `lower(...)`, seq scan | Ifoda indeksi yaratish |
| Bog'liq ustunlar | Ikki shartda taxmin 10 baravar past | `CREATE STATISTICS` |
| Generic plan regressiyasi | Beshinchi chaqiruvdan keyin sekinlashish | `force_custom_plan` yoki partial index |
| Index-only scan ishlamaydi | `Heap Fetches` katta | `VACUUM`, visibility map yangilash |
| `lossy` bitmap | `Heap Blocks: lossy=...` | `work_mem` oshirish yoki shartni aniqlashtirish |
| Reja tuzish sekin | `Planning Time` ijro vaqtiga yaqin | Partition sonini kamaytirish, index sonini qisqartirish |

## 24.12 Sekin so'rovni tekshirish tartibi: aniq qadamlar ro'yxati

Tartib muhim, chunki har bir qadam keyingisini kerak qilmasligi mumkin. Birinchi navbatda so'rov haqiqatan sekinmi yoki ulanish kutishidami aniqlanadi: `pg_stat_activity` dagi `wait_event_type` buni ko'rsatadi. Keyin `pg_stat_statements` dan shu so'rovning umumiy ulushi olinadi, chunki bir marta sekin ishlagan so'rov ustida ishlash vaqtni behuda sarflash.

Undan keyin `EXPLAIN (ANALYZE, BUFFERS)` olinadi va eng ko'p `actual time` yegan node topiladi. Shu node'da taxmin va haqiqat farqi tekshiriladi. Farq katta bo'lsa yechim statistika tomonda, farq kichik va vaqt haliyam katta bo'lsa yechim index yoki so'rov shakli tomonda. `Buffers` dagi `read` ulushi yuqori bo'lsa muammo I/O da, `hit` yuqori bo'lsa muammo CPU va qator sonida.

Oxirida o'zgarish prod hajmiga yaqin ma'lumotda sinaladi, chunki 10 ming qatorli lokal bazada reja butunlay boshqacha bo'ladi. Index qo'shilsa `CREATE INDEX CONCURRENTLY` ishlatiladi va `pg_stat_user_indexes` orqali u haqiqatan ishlatilayotgani bir hafta kuzatiladi.

## 24.13 Amalda qo'llash

- [ ] Eng og'ir 20 so'rovni `pg_stat_statements` dan `total_exec_time` bo'yicha chiqarib, ularning har biri uchun `EXPLAIN (ANALYZE, BUFFERS)` rejasini saqlab qo'y.
- [ ] Har bir rejada taxmin va haqiqiy qator sonini taqqoslab, 10 baravardan ortiq farq bo'lgan node'lar ro'yxatini tuz.
- [ ] SSD serverlarda `random_page_cost` ni 1.1 ga, `effective_cache_size` ni RAM ning 75 foiziga keltir va o'zgarishdan oldin va keyin rejalarni taqqoslab yoz.
- [ ] 10 million qatordan katta jadvallarga `autovacuum_analyze_scale_factor = 0.02` qo'yib, `pg_stat_user_tables` dagi `last_autoanalyze` ni haftada bir tekshir.
- [ ] Birgalikda filtrlanadigan bog'liq ustun juftliklarini aniqlab, ularga `CREATE STATISTICS` yaratib `ANALYZE` ishlatib natijani tasdiqla.
- [ ] `auto_explain` ni `log_min_duration = 500ms` va `sample_rate = 0.1` bilan yoqib, log'dan haftalik sekin reja hisobotini chiqar.
- [ ] Notekis taqsimlangan ustun bo'yicha filtrlaydigan prepared statement'larni topib, generic plan regressiyasini sinab ko'r va kerak bo'lsa partial index yoki `force_custom_plan` qo'lla.
- [ ] `work_mem` ni global 32MB da qoldirib, hisobot va eksport yo'llarida `SET LOCAL` bilan oshirishni kod darajasida standartlashtir.

---

[&larr; 23. Indekslar: B-tree, GIN, GiST, BRIN va tanlov](23-indekslar-b-tree-gin-gist-brin-va-tanlov.md) · [Mundarija](README.md) · [25. Sxema dizayni, ma'lumot turlari va cheklovlar &rarr;](25-sxema-dizayni-malumot-turlari-va-cheklovlar.md)
