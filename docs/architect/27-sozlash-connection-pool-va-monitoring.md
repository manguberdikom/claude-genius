<!-- doc: architect | chapter: 27 | part: IV. PostgreSQL chuqur bilim -->

[Barcha hujjatlar](../../README.md) / [Arxitektor miyasi](README.md)

> Holat: AI yozgan, inson tekshirmagan.

# 27. Sozlash, connection pool va monitoring (Configuration, Pooling and Monitoring)

<details>
<summary>Bu bobdagi 13 bo'lim</summary>

- [27.1 Asosiy `postgresql.conf` parametrlari va ularni server resursidan kelib chiqib hisoblash](#271-asosiy-postgresqlconf-parametrlari-va-ularni-server-resursidan-kelib-chiqib-hisoblash)
- [27.2 `shared_buffers`, `work_mem`, `maintenance_work_mem`, `effective_cache_size` tanlash](#272-shared_buffers-work_mem-maintenance_work_mem-effective_cache_size-tanlash)
- [27.3 `work_mem` tuzog'i: u har bir operatsiya uchun ajratiladi](#273-work_mem-tuzogi-u-har-bir-operatsiya-uchun-ajratiladi)
- [27.4 `max_connections` nega katta bo'lmasligi kerak](#274-max_connections-nega-katta-bolmasligi-kerak)
- [27.5 HikariCP sozlash: `maximum-pool-size`, `connection-timeout`, `max-lifetime`, `leak-detection-threshold`](#275-hikaricp-sozlash-maximum-pool-size-connection-timeout-max-lifetime-leak-detection-threshold)
- [27.6 Pool kattaligini hisoblash formulasi va amaliy raqamlar](#276-pool-kattaligini-hisoblash-formulasi-va-amaliy-raqamlar)
- [27.7 PgBouncer: transaction va session rejimi, prepared statement masalasi](#277-pgbouncer-transaction-va-session-rejimi-prepared-statement-masalasi)
- [27.8 `statement_timeout`, `lock_timeout`, `idle_in_transaction_session_timeout` o'rnatish](#278-statement_timeout-lock_timeout-idle_in_transaction_session_timeout-ornatish)
- [27.9 Monitoring uchun asosiy ko'rsatkichlar: `pg_stat_database`, `pg_stat_activity`, kesh hit nisbati](#279-monitoring-uchun-asosiy-korsatkichlar-pg_stat_database-pg_stat_activity-kesh-hit-nisbati)
- [27.10 `pg_stat_statements` ni yoqish va undan muntazam foydalanish](#2710-pg_stat_statements-ni-yoqish-va-undan-muntazam-foydalanish)
- [27.11 Sekin so'rov logi va `auto_explain` sozlash](#2711-sekin-sorov-logi-va-auto_explain-sozlash)
- [27.12 Zaxira nusxa va tiklanish: `pg_basebackup`, PITR, tiklanishni sinab ko'rish majburiyati](#2712-zaxira-nusxa-va-tiklanish-pg_basebackup-pitr-tiklanishni-sinab-korish-majburiyati)
- [27.13 Amalda qo'llash](#2713-amalda-qollash)

</details>



PostgreSQL ning standart sozlamalari 1 GB operativ xotirali mashinada ishga tushsin degan maqsadda yozilgan, shuning uchun 16 GB li production serverda ular to'g'ridan to'g'ri zarar keltiradi. Arxitektorning vazifasi har bir parametrni server resursidan kelib chiqib hisoblash, keyin ulanishlar sonini pool orqali cheklab, oqibatini monitoring bilan o'lchab turishdir. Sozlash, pool va kuzatuv bir zanjir: noto'g'ri `work_mem` sekin so'rovga, noto'g'ri pool kattaligi timeout'ga olib keladi. Oxirida eng ko'p e'tibordan chetda qoladigan narsa bor: zaxira nusxa emas, balki tiklanishni sinab ko'rish.

## 27.1 Asosiy `postgresql.conf` parametrlari va ularni server resursidan kelib chiqib hisoblash

Har bir parametrning `context` xossasi uni qanday o'zgartirish mumkinligini belgilaydi. `postmaster` kontekstidagi parametr (`shared_buffers`, `max_connections`, `shared_preload_libraries`) faqat restart bilan kuchga kiradi. `sighup` kontekstidagi parametr (`work_mem`, `log_min_duration_statement`) konfiguratsiyani qayta yuklash bilan yetadi. `user` kontekstidagi parametrni esa tranzaksiya ichida o'zgartirish mumkin, bu hisobot so'rovlari uchun eng kuchli vosita.

```sql
-- Qaysi parametr restart talab qiladi, qaysi biri yo'q: shuni avval tekshir
SELECT name, setting, unit, context, source
FROM pg_settings
WHERE name IN ('shared_buffers','work_mem','maintenance_work_mem',
               'effective_cache_size','max_connections','random_page_cost')
ORDER BY context, name;

-- ALTER SYSTEM postgresql.auto.conf ga yozadi, asl faylga tegmaydi
ALTER SYSTEM SET work_mem = '32MB';
ALTER SYSTEM SET effective_cache_size = '12GB';
SELECT pg_reload_conf();            -- sighup parametrlari darhol kuchga kiradi
```

16 GB RAM, 4 vCPU va SSD li OLTP server uchun boshlang'ich nuqta quyidagicha.

| Parametr | Standart | 16 GB server uchun | Nega shunday |
|---|---|---|---|
| `shared_buffers` | 128MB | 4GB | RAM ning taxminan 25 foizi |
| `effective_cache_size` | 4GB | 12GB | Planner uchun ishora, RAM ning 70 foizi |
| `work_mem` | 4MB | 24MB | Har bir sort/hash node uchun |
| `maintenance_work_mem` | 64MB | 1GB | Index va VACUUM tezligi |
| `max_connections` | 100 | 150 | Qolgani pool ustida |
| `random_page_cost` | 4.0 | 1.1 | SSD da tasodifiy o'qish qimmat emas |
| `effective_io_concurrency` | 1 | 200 | NVMe parallel o'qishni ko'taradi |
| `max_wal_size` | 1GB | 8GB | Checkpoint ni siyraklashtirish |
| `wal_compression` | off | on | WAL hajmi va replika trafigi kamayadi |

## 27.2 `shared_buffers`, `work_mem`, `maintenance_work_mem`, `effective_cache_size` tanlash

`shared_buffers` bu PostgreSQL ning o'z buffer cache'i, sahifalar bu yerda OS page cache'dan tashqari yana bir marta saqlanadi. Shuning uchun RAM ning hammasini bermaslik kerak: bir xil sahifa ikki joyda yotadi va OS cache'ga joy qolmaydi. Amalda 25 foiz yaxshi boshlanish, 40 foizdan oshirish faqat o'lchov natijasi bilan asoslanadi.

`effective_cache_size` hech qanday xotira ajratmaydi. Bu faqat planner'ga "shu sahifalar ehtimol cache'da bor" degan ishora, vazifasi index scan narxini arzonlashtirish. Kichik qiymat planner'ni sequential scan tomon suradi, bu 50 million qatorli buyurtma jadvalida falokat.

```properties
# 16 GB RAM, 4 vCPU, SSD, OLTP + kechqurun hisobot
shared_buffers = 4GB
effective_cache_size = 12GB
work_mem = 24MB                   # har bir sort/hash node uchun
maintenance_work_mem = 1GB        # CREATE INDEX, VACUUM, ALTER TABLE
max_parallel_workers_per_gather = 2
wal_buffers = 64MB
max_wal_size = 8GB
random_page_cost = 1.1
effective_io_concurrency = 200
default_statistics_target = 200   # plan aniqligi uchun
```

`maintenance_work_mem` ni saxiy qo'yish arzon, chunki uni faqat autovacuum worker'lari va DDL ishlatadi. 1 GB bilan `CREATE INDEX CONCURRENTLY` tez bitadi. Lekin `autovacuum_max_workers` ni 10 taga ko'tarsang, eng yomon holatda shu qiymat 10 ga ko'payishini unutma.

## 27.3 `work_mem` tuzog'i: u har bir operatsiya uchun ajratiladi

`work_mem` sessiya uchun emas, ulanish uchun ham emas, balki rejadagi har bir sort, hash join va hash aggregate node uchun alohida ajratiladi. Uchta hash join va ikkita sort bo'lgan hisobot so'rovi bitta ulanishda 5 x `work_mem` yeydi. Parallel plan bo'lsa, har bir worker ham o'z ulushini oladi. 150 ulanish x 5 node x 24 MB qog'ozda 18 GB, ya'ni serverdan ko'proq.

```sql
-- Diskka tushgan sort: "external merge" va "Disk:" belgilari muhim
EXPLAIN (ANALYZE, BUFFERS)
SELECT customer_id, sum(total_amount) FROM orders
WHERE created_at >= now() - interval '90 days'
GROUP BY customer_id ORDER BY 2 DESC;
-- Sort Method: external merge  Disk: 86784kB   <-- work_mem yetmagan

-- To'g'ri yechim: global emas, faqat shu tranzaksiya uchun ko'tarish
BEGIN;
SET LOCAL work_mem = '256MB';          -- faqat shu tranzaksiya ichida
SET LOCAL statement_timeout = '120s';  -- hisobot uzoq, lekin cheksiz emas
-- ... hisobot so'rovi ...
COMMIT;

-- Hash operatsiyalari uchun alohida koeffitsient bor (PostgreSQL 13+)
SHOW hash_mem_multiplier;   -- standart 2.0, ya'ni hash node 2 x work_mem oladi
```

Arxitektorning qarori shu: global `work_mem` ni past tut (16 MB dan 32 MB), hisobot va batch uchun alohida role yaratib, unga `ALTER ROLE ... SET work_mem` bilan katta qiymat ber. Shunda kechqurungi hisobot kunduzgi to'lov oqimining xotirasini o'g'irlamaydi.

## 27.4 `max_connections` nega katta bo'lmasligi kerak

PostgreSQL har bir ulanish uchun alohida OS process ochadi. Bo'sh process ham bir necha MB xotira ushlaydi, lekin asosiy narx xotirada emas: snapshot olish, lock jadvalini tekshirish va shared memory strukturalariga kirish ulanishlar soni bilan qimmatlashadi. Natijada 1000 ulanishli serverda CPU ning sezilarli qismi foydali ishga emas, koordinatsiyaga ketadi.

Ikkinchi sabab amaliy: 1000 parallel so'rov 4 vCPU da baribir navbatda turadi, lekin har biri o'z `work_mem` ini va lock'larini ushlaydi. Navbat pool'da turishi kerak, chunki uni o'lchash va cheklash mumkin. Qoida: `max_connections` ni 100 dan 300 orasida tut, parallellikni HikariCP va PgBouncer ustida boshqar.

| Oddiy yondashuv | Arxitektor yondashuvi |
|---|---|
| `max_connections = 1000` qo'yib muammoni yopish | 150 da qoldirish va pool bilan navbat qurish |
| `work_mem` ni global 256MB qilish | Global 24MB, hisobot role'ida 256MB |
| `effective_cache_size` ni xotira ajratish deb bilish | Uni planner narx modeli ishorasi deb bilish |
| Pool kattaligini 50 deb "ehtiyot uchun" qo'yish | Little qonuni bilan hisoblab 10 deb qo'yish |
| Hikari timeout'ini 30s qoldirish | 3s qilib fail fast va circuit breaker ulash |
| PgBouncer'ni session rejimida yoqish | Transaction rejimi va prepared statement masalasini hal qilish |
| Timeout'siz tranzaksiya qoldirish | Role darajasida uchta timeout o'rnatish |
| Sekin so'rovni foydalanuvchi shikoyatidan bilish | `pg_stat_statements` snapshot'ini kunlik solishtirish |
| Backup muvaffaqiyatli bo'lsa xotirjam bo'lish | Chorakda bir marta restore drill o'tkazish |
| Kesh hit nisbatini umuman qaramaslik | 99 foizdan tushishini alert qilish |

## 27.5 HikariCP sozlash: `maximum-pool-size`, `connection-timeout`, `max-lifetime`, `leak-detection-threshold`

`minimum-idle` ni `maximum-pool-size` ga teng qo'yish to'g'ri, chunki ulanish ochish narxi (TCP, TLS, autentifikatsiya) spike paytida eng kerakli daqiqada qo'shiladi. `connection-timeout` esa pool'dan kutish muddati: 30 sekundda qoldirsang, DB sekinlashganda thread'lar o'ttiz sekund band turadi va servis to'xtaydi. 3 sekundlik qiymat tez xato berib, retry va fallback'ga yo'l ochadi.

```yaml
spring:
  datasource:
    hikari:
      maximum-pool-size: 10          # pod uchun, hisoblangan qiymat
      minimum-idle: 10               # production: pool o'lchami doimiy bo'lsin
      connection-timeout: 3000       # pool'dan kutish, ms: fail fast
      validation-timeout: 2000
      max-lifetime: 1500000          # 25 daqiqa, LB/DB limitidan kichik
      keepalive-time: 120000         # bo'sh ulanishni jim o'lishdan saqlaydi
      leak-detection-threshold: 20000 # 20s ushlangan ulanish uchun stack trace
      pool-name: payment-pool
      auto-commit: false             # tranzaksiyani Spring boshqaradi
      data-source-properties:
        reWriteBatchedInserts: true  # JDBC batch insert'ni tezlashtiradi
```

`max-lifetime` infratuzilmadagi eng qisqa muddatdan kichik bo'lishi shart: NAT yoki load balancer bo'sh TCP ulanishni 30 daqiqada uzsa, `max-lifetime` 25 daqiqa bo'ladi. Aks holda ilova o'lgan ulanishni oladi va foydalanuvchi tasodifiy xato ko'radi. `leak-detection-threshold` esa uzoq ushlangan ulanish uchun stack trace yozadi, va bu odatda tranzaksiya ichida HTTP chaqiruv qilingan joyni ochadi.

## 27.6 Pool kattaligini hisoblash formulasi va amaliy raqamlar

Pool kattaligini Little qonuni bilan hisoblash ishonchli: `pool = kutilgan_RPS x o'rtacha_DB_vaqti`. To'lov servisi sekundiga 600 so'rovni ko'tarsa va bir so'rov DB da taxminan 8 ms tursa, kerakli parallellik 600 x 0.008 = 4.8 ta ulanish. Zahira qo'shib 8 yoki 10 deb belgilash yetarli. Klassik `yadro x 2 + disk soni` formulasi ham shu tartibdagi raqam beradi.

| Servis | RPS | O'rtacha DB vaqti | Hisob | Pool (pod) | Pod soni | Jami |
|---|---|---|---|---|---|---|
| To'lov API | 600 | 8 ms | 4.8 | 10 | 4 | 40 |
| Buyurtma API | 300 | 12 ms | 3.6 | 8 | 3 | 24 |
| Ombor qoldig'i | 150 | 5 ms | 0.75 | 5 | 2 | 10 |
| Hisobot worker | 2 | 900 ms | 1.8 | 4 | 1 | 4 |
| Batch import | 1 | 2000 ms | 2.0 | 4 | 1 | 4 |

Jami 82 ta ulanish, ustiga migratsiya va monitoring uchun zahira: `max_connections = 150` yetadi. Eng muhim nazorat shu: barcha pod'lardagi pool'lar yig'indisi `max_connections` dan kam bo'lishi kerak, aks holda autoscaling paytida DB "too many clients already" deb qaytaradi. Kichik pool qo'rqinchli ko'rinadi, lekin amalda katta pool'dan tez ishlaydi, chunki DB navbatda emas, bajarishda bo'ladi.

## 27.7 PgBouncer: transaction va session rejimi, prepared statement masalasi

`session` rejimida client ulanishi uzilguncha server ulanishi band qoladi, ya'ni multiplexing deyarli yo'q va foyda kam. `transaction` rejimida server ulanishi faqat tranzaksiya davomida band bo'ladi, shuning uchun 500 client 25 ta server ulanishiga sig'adi. Ko'p pod'li Kubernetes muhitida PgBouncer'ning asl qiymati shu rejimdagina ochiladi.

```properties
# pgbouncer.ini: 500 client -> 25 server ulanishi
[databases]
orders = host=pg-primary port=5432 dbname=orders

[pgbouncer]
pool_mode = transaction
max_client_conn = 500
default_pool_size = 25
reserve_pool_size = 5
server_idle_timeout = 600
max_prepared_statements = 200   # transaction rejimida prepared statement uchun
ignore_startup_parameters = extra_float_digits
```

Transaction rejimining narxi bor: sessiyaga bog'liq hamma narsa buziladi. `SET` natijasi keyingi tranzaksiyaga o'tmaydi, session darajasidagi advisory lock boshqa client'ga tegib ketadi, `LISTEN/NOTIFY`, temp jadval va `WITH HOLD` cursor ishlamaydi. Eng ko'p uchraydigan muammo server tomonidagi prepared statement: JDBC driver so'rovni bir necha marta bajargandan keyin uni server tomonda nomlab qo'yadi, yangi server ulanishida esa o'sha nom yo'q. Yangi PgBouncer versiyalari buni `max_prepared_statements` bilan protokol darajasida qo'llab-quvvatlaydi. Versiyangiz qodir bo'lmasa, JDBC URL da `prepareThreshold=0` qo'yib server tomonidagi prepared statement'ni o'chirish kerak, narxi esa har safar qayta parse qilish.

HikariCP ilova ichidagi parallellikni cheklaydi, PgBouncer esa pod'lar yig'indisini. Ikkisi bir vazifani bajarmaydi, shuning uchun pod soni o'zgarib turadigan tizimda ikkisi ham kerak.

## 27.8 `statement_timeout`, `lock_timeout`, `idle_in_transaction_session_timeout` o'rnatish

Bu uchta timeout'ni global `postgresql.conf` da qo'yish xato, chunki migratsiya va `VACUUM` ham shu cheklovga tushadi. To'g'ri joy role darajasi: ilovaga qisqa, migratsiyaga uzun, hisobotga o'rtacha qiymat.

```sql
-- OLTP ilovasi: tez xato, uzoq kutish yo'q
ALTER ROLE app_payment SET statement_timeout = '5s';
ALTER ROLE app_payment SET lock_timeout = '2s';
ALTER ROLE app_payment SET idle_in_transaction_session_timeout = '30s';

-- Hisobot role'i: uzoq so'rov ruxsat, lekin cheksiz emas
ALTER ROLE app_report SET statement_timeout = '180s';
ALTER ROLE app_report SET work_mem = '256MB';

-- Migratsiya: DDL navbatda uzoq turmasin
ALTER ROLE app_migrator SET lock_timeout = '3s';

-- Ochiq lekin bo'sh tranzaksiyalar: VACUUM ni bloklaydi
SELECT pid, usename, now() - xact_start AS tx_age, query FROM pg_stat_activity
WHERE state = 'idle in transaction' AND now() - xact_start > interval '1 min';
```

`idle_in_transaction_session_timeout` ning mexanikasi eng muhim: ochiq tranzaksiya o'z `xmin` ini ushlab turadi, shuning uchun VACUUM shu paytdan keyin o'lgan qatorlarni tozalay olmaydi. Bitta unutilgan tranzaksiya bir necha soatda jadvalni bloat qilib, barcha so'rovlarni sekinlashtiradi. `lock_timeout` esa `ALTER TABLE` ning `ACCESS EXCLUSIVE` lock navbatini kutib, orqasida butun o'qish trafigini to'plab qo'yishidan saqlaydi. Spring tomonida `@Transactional(timeout = 5)` foydali, lekin u JDBC query timeout'i bo'lib, server tomonidagi `statement_timeout` ni almashtirmaydi.

## 27.9 Monitoring uchun asosiy ko'rsatkichlar: `pg_stat_database`, `pg_stat_activity`, kesh hit nisbati

`pg_stat_database` birinchi panel. Kesh hit nisbati `blks_hit / (blks_hit + blks_read)` OLTP bazada 99 foizdan yuqori bo'lishi kerak, 95 foizga tushishi `shared_buffers` kichik yoki ishchi ma'lumot hajmi o'sgan degani. `temp_files` va `temp_bytes` o'sishi `work_mem` yetmayotganini, `deadlocks` o'sishi esa kodda lock tartibi buzilganini ko'rsatadi.

```sql
-- Kesh hit nisbati, temp fayl va deadlock
SELECT datname, temp_files, deadlocks,
       round(100.0 * blks_hit / nullif(blks_hit + blks_read, 0), 2) AS cache_hit_pct,
       pg_size_pretty(temp_bytes) AS temp_size
FROM pg_stat_database WHERE datname NOT LIKE 'template%';

-- Hozir nima kutilmoqda: wait_event eng foydali ustun
SELECT state, wait_event_type, wait_event, count(*)
FROM pg_stat_activity WHERE backend_type = 'client backend'
GROUP BY 1,2,3 ORDER BY 4 DESC;
```

`pg_stat_activity` da eng qimmatli ustun `wait_event_type`: `Lock` lock raqobatini, `IO` disk muammosini, `LWLock` ichki raqobatni, `Client` esa ilova sekin o'qiyotganini bildiradi. Jadval darajasida `pg_stat_user_tables` dagi `seq_scan` va `n_dead_tup` kuzatiladi: birinchisining o'sishi yo'qolgan index, ikkinchisining o'sishi autovacuum yetishmayotgani haqida gapiradi.

## 27.10 `pg_stat_statements` ni yoqish va undan muntazam foydalanish

Bu extension production diagnostikasining asosi va restart talab qiladi, shuning uchun uni birinchi kundan yoqish kerak. U so'rovlarni normallashtirib `queryid` bo'yicha yig'adi, natijada "sekin so'rov" emas, "umumiy vaqtni eng ko'p yeydigan so'rov" ko'rinadi. Tizimni sekinlashtirgan narsa odatda bitta 3 sekundli hisobot emas, kuniga 2 million marta bajarilgan 4 ms li so'rovdir.

```sql
-- shared_preload_libraries = 'pg_stat_statements'  (restart kerak)
-- pg_stat_statements.max = 5000 ; .track = top
CREATE EXTENSION IF NOT EXISTS pg_stat_statements;

-- Umumiy vaqt bo'yicha top 10: optimizatsiya shu ro'yxatdan boshlanadi
SELECT round(total_exec_time)::bigint AS total_ms, calls, rows,
       round(mean_exec_time, 2) AS mean_ms,
       round(stddev_exec_time, 2) AS stddev_ms,
       left(query, 80) AS query
FROM pg_stat_statements
ORDER BY total_exec_time DESC LIMIT 10;

-- Relizdan oldin va keyin solishtirish uchun nolga tushirish
SELECT pg_stat_statements_reset();
```

Muntazam amaliyot: har kuni bir vaqtda snapshot olib alohida jadvalga yozish, keyin oldingi snapshot bilan ayirmasini hisoblash. Shunda "bu so'rov relizdan keyin 3 barobar ko'p chaqirilyapti" degan xulosa chiqadi, N+1 esa `calls` ustunidagi keskin o'sish sifatida ko'rinadi. `stddev_exec_time` ning kattaligi so'rov plan almashtirayotganini bildiradi.

## 27.11 Sekin so'rov logi va `auto_explain` sozlash

Sekin so'rov logi `pg_stat_statements` ni to'ldiradi, chunki u konkret parametr qiymatlari bilan konkret holatni ko'rsatadi. `log_min_duration_statement` ni 200 ms ga qo'yish OLTP da yaxshi muvozanat, log hajmi katta bo'lsa `log_min_duration_sample` va `log_statement_sample_rate` bilan namuna olinadi.

```properties
log_min_duration_statement = 200ms   # 200 ms dan uzoq hamma so'rov
log_lock_waits = on                  # deadlock_timeout dan uzoq lock kutishlari
log_temp_files = 0                   # har qanday temp fayl: work_mem signali
log_line_prefix = '%m [%p] %u@%d app=%a '   # korrelyatsiya uchun shart

shared_preload_libraries = 'pg_stat_statements,auto_explain'
auto_explain.log_min_duration = '500ms'
auto_explain.log_analyze = on        # haqiqiy qatorlar, lekin overhead bor
auto_explain.log_timing = off        # overhead ni kamaytirish uchun o'chiriladi
auto_explain.log_buffers = on
auto_explain.log_nested_statements = on   # ORM ichidagi so'rovlar uchun
auto_explain.sample_rate = 0.05      # yuklamali tizimda 5 foiz yetarli
```

`auto_explain.log_analyze = on` haqiqiy qator sonlarini yozadi, ya'ni planner taxmini bilan reallik orasidagi farq ko'rinadi, va shu farq statistika eskirganini aniqlaydi. Lekin `log_timing` har bir node uchun vaqt o'lchaydi va yuklamali serverda sezilarli overhead beradi, shuning uchun uni off qoldirib `sample_rate` ni past tutish to'g'ri. `log_line_prefix` da `app=%a` bo'lsa, so'rov qaysi servisdan kelganini log'dan ajratish mumkin.

| Tuzoq | Oqibat | Yechim |
|---|---|---|
| Global `work_mem` ni 256MB qilish | OOM, server o'ladi | Global 24MB, role darajasida ko'tarish |
| `connection-timeout` 30s | Thread'lar band, kaskad nosozlik | 3s va fallback |
| `max-lifetime` LB limitidan katta | Tasodifiy "connection reset" | LB limitidan 5 daqiqa kichik qilish |
| PgBouncer transaction rejimi + server prepared statement | "prepared statement does not exist" | `max_prepared_statements` yoki `prepareThreshold=0` |
| Timeout'siz `idle in transaction` | Bloat, VACUUM ishlamaydi | `idle_in_transaction_session_timeout = 30s` |
| `auto_explain.log_timing = on` | Katta CPU overhead | off + `sample_rate = 0.05` |
| Pool'lar yig'indisi > `max_connections` | "too many clients already" | Pod soni x pool ni hisoblab chegaralash |
| Backup bor, restore sinovdan o'tmagan | RTO noma'lum, tiklanish amalda ishlamaydi | Chorakda restore drill |

## 27.12 Zaxira nusxa va tiklanish: `pg_basebackup`, PITR, tiklanishni sinab ko'rish majburiyati

Streaming replikatsiya backup emas, chunki u mantiqiy xatoni ham ko'chiradi: noto'g'ri `DELETE` replikada ham bajariladi. Fizik backup va WAL arxivi kerak: `pg_basebackup` to'liq nusxa oladi, WAL arxivi esa shu nuqtadan keyin istalgan vaqtga qaytish imkonini beradi, ya'ni PITR.

```bash
# To'liq fizik backup: tar + gzip, WAL ni oqim bilan
pg_basebackup -h pg-primary -U replicator -D /backup/base-$(date +%F) \
  -Ft -z -Xs -c fast -P --write-recovery-conf

pg_verifybackup /backup/base-2026-10-04   # butunlikni tekshirish: majburiy

# PITR: bazani tiklab, kerakli vaqtga to'xtatish
# postgresql.conf ichida:
#   restore_command = 'cp /archive/%f %p'
#   recovery_target_time = '2026-10-04 11:42:00+05'
#   recovery_target_action = 'promote'
touch /var/lib/postgresql/data/recovery.signal   # recovery rejimini yoqadi
pg_ctl -D /var/lib/postgresql/data start
psql -c "SELECT pg_is_in_recovery(), pg_last_wal_replay_lsn();"
```

Raqamlarni oldindan belgilash kerak. WAL arxivini har 60 sekundda yuborsang, RPO taxminan 1 daqiqa. 500 GB bazani 1 GB/s tarmoqda tiklash taxminan 10 daqiqa, ustiga WAL replay qo'shilib, RTO realistik holda 30 daqiqadan 60 daqiqagacha. Bu raqamlarni taxmin qilish mumkin emas, ularni o'lchash kerak, o'lchashning yagona yo'li esa haqiqiy tiklanish mashqi: chorakda bir marta alohida serverga backup'dan tiklab, to'lov va buyurtma jadvallaridagi qator sonini va oxirgi tranzaksiya vaqtini tekshirish. Katta bazalarda `pgBackRest` yoki `barman` inkremental backup, parallel siqish va saqlash siyosatini o'zi boshqaradi, shuning uchun qo'lda skript yozishdan ko'ra ularni tanlash oqilona.

## 27.13 Amalda qo'llash

- [ ] Serverning RAM va vCPU miqdoridan kelib chiqib `shared_buffers`, `effective_cache_size`, `work_mem`, `maintenance_work_mem` ni hisoblab qo'y va `pg_settings` orqali tasdiqla.
- [ ] Hisobot va batch uchun alohida role yarat, ularga `work_mem` va `statement_timeout` ni `ALTER ROLE` bilan belgila, OLTP role'ini qisqa timeout'da qoldir.
- [ ] Har bir servis uchun pool kattaligini `RPS x DB_vaqti` bilan hisobla, pod soniga ko'paytirib yig'indisi `max_connections` dan kichik ekanini tekshir.
- [ ] HikariCP da `connection-timeout` ni 3000 ms, `max-lifetime` ni infratuzilma limitidan 5 daqiqa kichik, `leak-detection-threshold` ni 20000 ms qilib qo'y.
- [ ] `idle_in_transaction_session_timeout` va `lock_timeout` ni ilova role'ida yoq, bir hafta log'dagi uzilgan tranzaksiyalarni ko'rib chiqib sabablarini tuzat.
- [ ] `pg_stat_statements` va `auto_explain` ni yoq, kunlik snapshot yig'adigan ish qo'y, top 10 so'rovni haftalik ko'rikka kirit.
- [ ] Kesh hit nisbati, `temp_bytes`, `deadlocks`, eng uzun tranzaksiya yoshi va pool kutish vaqti uchun alert qoidalarini yoz.
- [ ] Chorakda bir marta `pg_basebackup` dan PITR mashqini o'tkaz, RTO va RPO ni o'lchab hujjatga yoz.

---

[&larr; 26. Partitioning, replikatsiya va katta hajm](26-partitioning-replikatsiya-va-katta-hajm.md) · [Mundarija](README.md) · [28. Keshlash amaliyoti: invalidatsiya, stampede, Redis haqiqati &rarr;](28-keshlash-amaliyoti-invalidatsiya-stampede.md)
