<!-- doc: architect | chapter: 21 | part: IV. PostgreSQL chuqur bilim -->

[Barcha hujjatlar](../../README.md) / [Arxitektor miyyasi](README.md)

# 21. PostgreSQL arxitekturasi: process model, WAL, checkpoint, vacuum (PostgreSQL Architecture)

<details>
<summary>Bu bobdagi 12 bo'lim</summary>

- [21.1 Protsess modeli: postmaster, backend protsess, fon ishchilari](#211-protsess-modeli-postmaster-backend-protsess-fon-ishchilari)
- [21.2 Har ulanishga bitta protsess: bundan kelib chiqadigan ulanish narxi](#212-har-ulanishga-bitta-protsess-bundan-kelib-chiqadigan-ulanish-narxi)
- [21.3 Umumiy xotira: `shared_buffers` va operatsion tizim keshi bilan munosabati](#213-umumiy-xotira-shared_buffers-va-operatsion-tizim-keshi-bilan-munosabati)
- [21.4 Sahifa (page) tuzilishi, tuple va `ctid`](#214-sahifa-page-tuzilishi-tuple-va-ctid)
- [21.5 WAL: yozuv tartibi, `wal_level`, `synchronous_commit` va ma'lumot xavfsizligi](#215-wal-yozuv-tartibi-wal_level-synchronous_commit-va-malumot-xavfsizligi)
- [21.6 Checkpoint: qachon boshlanadi, I/O cho'qqisi va `checkpoint_timeout` sozlash](#216-checkpoint-qachon-boshlanadi-io-choqqisi-va-checkpoint_timeout-sozlash)
- [21.7 Vacuum nima qiladi: o'lik tuple, visibility map, index-only scan bilan bog'liqligi](#217-vacuum-nima-qiladi-olik-tuple-visibility-map-index-only-scan-bilan-bogliqligi)
- [21.8 Autovacuum sozlamalari va u yetishmay qolganda nima bo'ladi](#218-autovacuum-sozlamalari-va-u-yetishmay-qolganda-nima-boladi)
- [21.9 Transaction ID o'ralishi (wraparound) va freeze jarayoni](#219-transaction-id-oralishi-wraparound-va-freeze-jarayoni)
- [21.10 Jadval va indeks shishishi (bloat): o'lchash va tuzatish](#2110-jadval-va-indeks-shishishi-bloat-olchash-va-tuzatish)
- [21.11 `TOAST`: katta qiymatlar qanday saqlanadi](#2111-toast-katta-qiymatlar-qanday-saqlanadi)
- [21.12 Amalda qo'llash](#2112-amalda-qollash)

</details>



PostgreSQL ko'pchilik Java dasturchisi uchun "JDBC orqasidagi qora quti" bo'lib qoladi, lekin production muammolarining katta qismi aynan shu qutining ichidagi mexanikadan kelib chiqadi: ulanish narxi, WAL yozuvi, checkpoint I/O cho'qqisi, vacuum qarzi. Bu bobda PostgreSQL 15-17 ichida nima sodir bo'lishini qarab chiqamiz va har bir mexanizmdan arxitektor qanday qaror chiqarishini ko'rsatamiz. Misollar bitta tizim ustida boradi: to'lov servisi, buyurtma jadvali, ombor qoldig'i va kunlik hisobot. Har bir bo'limda sozlash parametrining haqiqiy nomi va uni kuzatadigan katalog so'rovi bor.

## 21.1 Protsess modeli: postmaster, backend protsess, fon ishchilari

PostgreSQL thread modelida emas, protsess modelida ishlaydi. `postmaster` deb ataladigan asosiy protsess portni tinglaydi, umumiy xotirani yaratadi va har bir yangi ulanish uchun `fork()` qiladi. Natijada hosil bo'lgan backend protsess faqat o'sha bitta ulanishga xizmat qiladi va uzilganda o'ladi. Bu dizayn izolyatsiya beradi: bitta backend segfault bo'lsa, postmaster butun instansni qayta tiklaydi, lekin bitta buzilgan session boshqa sessionlarning stackini buzolmaydi.

Backendlardan tashqari doimiy fon ishchilari bor. `checkpointer` iflos sahifalarni diskka tushiradi, `background writer` buffer poolni oldindan bo'shatadi, `walwriter` WAL buferini fayl tizimiga oqizadi, `autovacuum launcher` ishchilarni ishga tushiradi, `archiver` WAL segmentlarini arxivga beradi, `logical replication launcher` esa logical slotlarni boshqaradi. PostgreSQL 15 dan boshlab statistika yig'uvchi alohida protsess emas, statistika umumiy xotirada saqlanadi, shuning uchun `pg_stat_*` ko'rinishlari arzonroq va restartda yo'qolmaydi.

```bash
# Instansdagi barcha protsesslarni ko'rish: kim backend, kim fon ishchisi
ps -o pid,etime,rss,cmd -u postgres | grep -E 'postgres:' | head -20

# Tipik natija (qisqartirilgan):
# postgres: checkpointer
# postgres: background writer
# postgres: walwriter
# postgres: autovacuum launcher
# postgres: logical replication launcher
# postgres: payments app 10.0.3.14(51322) idle in transaction
```

Arxitektor uchun muhim xulosa: `idle in transaction` holatidagi backend bu shunchaki bo'sh ulanish emas. U snapshot ushlab turadi va vacuum ishini to'sadi. Spring tomonida bu `@Transactional` metod ichida tashqi HTTP chaqiriq qilinganda yuzaga keladi.

## 21.2 Har ulanishga bitta protsess: bundan kelib chiqadigan ulanish narxi

`fork()` arzon emas. Yangi backend yaratilishi taxminan 1 dan 5 millisekundgacha oladi, uning ustiga ulanish autentifikatsiyasi, katalog keshini isitish va `search_path` o'rnatish qo'shiladi. Har bir bo'sh backend taxminan 2 dan 10 MB gacha xususiy xotira egallaydi, murakkab so'rovlardan keyin esa `work_mem` va katalog keshi hisobiga 50 MB dan oshishi mumkin. Shuning uchun `max_connections = 1000` qo'yish xatodir: PostgreSQL 1000 ta parallel backendda lock manager va snapshot hisob-kitoblari ustida o'zini yeb qo'yadi.

Amaliy qoida: haqiqiy parallel ishlayotgan backendlar soni CPU yadrosi sonidan 2-4 barobar ko'p bo'lmasin. 16 yadroli serverda 40-60 ta faol backend ko'pincha maksimal throughput beradi. Qolgan hamma narsa pool va PgBouncer vazifasi.

```properties
# Spring Boot 3.x: pool kattaligi PostgreSQL imkoniyatiga qarab tanlanadi
# 16 yadro, 4 ta instans => har instansga 10 ta ulanish, jami 40
spring.datasource.hikari.maximum-pool-size=10
spring.datasource.hikari.minimum-idle=10
# Pooldan ulanish kutish timeouti: tez fail qilish uchun qisqa
spring.datasource.hikari.connection-timeout=3000
# Backendni cheksiz band qilib turmaslik uchun
spring.datasource.hikari.max-lifetime=1800000
# Server tomonida himoya: tranzaksiya ichida qotib qolgan sessionni uzish
# postgresql.conf: idle_in_transaction_session_timeout = '30s'
# postgresql.conf: statement_timeout = '15s'
```

PgBouncer `transaction` rejimida 2000 ta application ulanishini 50 ta backendga siqadi. Buning narxi bor: session darajasidagi narsalar (`SET LOCAL` dan tashqari `SET`, advisory lock, prepared statement nomlari) ishonchsiz bo'ladi. Hibernate ishlatganda `prepareThreshold=0` yoki PgBouncer 1.21+ dagi prepared statement qo'llashini tekshirish kerak.

```sql
-- Ulanishlarning holati bo'yicha taqsimlanishi: pool muammosini shu ko'rsatadi
SELECT state, count(*), max(now() - state_change) AS eng_uzun
FROM pg_stat_activity
WHERE backend_type = 'client backend'
GROUP BY state ORDER BY 2 DESC;

-- Vacuum'ni to'sayotgan eng qadimgi tranzaksiya
SELECT pid, usename, application_name,
       now() - xact_start AS xact_davomiyligi, state, left(query, 60)
FROM pg_stat_activity
WHERE xact_start IS NOT NULL
ORDER BY xact_start LIMIT 5;
```

## 21.3 Umumiy xotira: `shared_buffers` va operatsion tizim keshi bilan munosabati

`shared_buffers` bu PostgreSQL ning o'z buffer pooli, 8 KB li sahifalardan iborat. Backend diskdan sahifa o'qiganda uni avval shu poolga joylaydi, o'zgartirsa sahifani "iflos" (dirty) deb belgilaydi. PostgreSQL ikki qatlamli keshga tayanadi: o'z pooli va operatsion tizim page cache. Shuning uchun `shared_buffers` ni RAM ning 80 foiziga qo'yish zarar keltiradi, chunki bir xil ma'lumot ikki joyda yotadi va OS ga joy qolmaydi.

Boshlang'ich nuqta: `shared_buffers` RAM ning taxminan 25 foizi, 64 GB li serverda 16 GB. `effective_cache_size` esa hech narsa ajratmaydi, u faqat plannerga "disk keshida shuncha joy bor" deb aytadi, uni RAM ning 50-75 foiziga qo'yish mumkin. `work_mem` har bir sort yoki hash node uchun ajratiladi, shuning uchun 100 ta backend va 4 ta sort node bo'lsa, real iste'mol `work_mem` ning 400 barobariga chiqishi mumkin.

```sql
-- pg_buffercache: kesh ichida qaysi jadvallar o'tiribdi
CREATE EXTENSION IF NOT EXISTS pg_buffercache;

SELECT c.relname,
       count(*) * 8192 / 1024 / 1024 AS kesh_mb,
       round(100.0 * count(*) FILTER (WHERE b.isdirty) / count(*), 1) AS iflos_foiz
FROM pg_buffercache b
JOIN pg_class c ON c.relfilenode = b.relfilenode
GROUP BY c.relname ORDER BY 2 DESC LIMIT 10;

-- Kesh hit ratio: 0.99 dan past bo'lsa shared_buffers yoki indeks muammosi
SELECT sum(heap_blks_hit) * 100.0 / nullif(sum(heap_blks_hit + heap_blks_read), 0)
         AS heap_hit_foiz
FROM pg_statio_user_tables;
```

16 GB dan katta `shared_buffers` da `huge_pages = try` qo'yish TLB bosimini kamaytiradi va taxminan 2-5 foiz CPU tejaydi. PostgreSQL 16 dan boshlab `pg_stat_io` ko'rinishi o'qish va yozishni kontekst bo'yicha ajratib beradi, bu checkpoint va vacuum I/O sini aralashtirmasdan o'lchash imkonini beradi.

## 21.4 Sahifa (page) tuzilishi, tuple va `ctid`

Heap fayl 8 KB li sahifalarga bo'lingan. Har sahifa boshida 24 baytli header, keyin sahifa oxiridan o'sib keladigan tuple ma'lumotlari va boshidan o'sib keladigan 4 baytli line pointer massivi joylashadi. Har bir tuple o'z headerida `xmin` (qaysi tranzaksiya yaratgan) va `xmax` (qaysi tranzaksiya o'chirgan) ni saqlaydi, header hajmi taxminan 23 bayt, hizalanish bilan 24 bayt.

`ctid` bu tuple ning fizik manzili: `(sahifa_raqami, sahifa_ichidagi_slot)`. UPDATE PostgreSQL da joyida o'zgartirish emas, balki yangi tuple yozish va eskisining `xmax` ini to'ldirishdir. Shuning uchun `ctid` barqaror identifikator emas va uni application darajasida saqlash xato.

```sql
-- ctid va tizim ustunlari: bitta buyurtma qatori qaysi sahifada yotadi
SELECT ctid, xmin, xmax, buyurtma_id, holat
FROM buyurtmalar WHERE buyurtma_id = 10045;

-- Sahifa ichini bayt darajasida ko'rish
CREATE EXTENSION IF NOT EXISTS pageinspect;
SELECT lp, lp_off, lp_len, t_xmin, t_xmax, t_ctid
FROM heap_page_items(get_raw_page('buyurtmalar', 0)) LIMIT 10;

-- Bitta satrga qancha sahifa va o'rtacha necha bayt to'g'ri keladi
SELECT relname, relpages, reltuples::bigint,
       pg_size_pretty(pg_relation_size(oid)) AS heap_hajm,
       round(pg_relation_size(oid)::numeric / nullif(reltuples, 0), 1) AS bayt_per_satr
FROM pg_class WHERE relname = 'buyurtmalar';
```

HOT (Heap Only Tuple) update yangi tuple ni shu sahifaning o'zida yaratadi va indeksni umuman yangilamaydi. Buning sharti ikkita: o'zgaruvchi ustunlarning birortasi indekslanmagan bo'lsin va sahifada bo'sh joy qolgan bo'lsin. Tez-tez yangilanadigan `ombor_qoldiq` jadvalida `ALTER TABLE ... SET (fillfactor = 80)` qo'yish va `oxirgi_ozgarish` ustunini indekslamaslik WAL hajmini sezilarli kamaytiradi.

## 21.5 WAL: yozuv tartibi, `wal_level`, `synchronous_commit` va ma'lumot xavfsizligi

WAL (Write Ahead Log) qoidasi oddiy: ma'lumot sahifasi diskka tushishidan oldin uning o'zgarishini tasvirlaydigan WAL yozuvi diskda bo'lishi shart. COMMIT paytida PostgreSQL ma'lumot fayllarini emas, faqat WAL ni `fsync` qiladi. Shuning uchun commit narxi jadval kattaligiga emas, disk `fsync` latensiyasiga bog'liq. NVMe diskda bu taxminan 0.05-0.2 ms, tarmoqli diskda 1-5 ms bo'lishi mumkin.

`wal_level` uch qiymat oladi. `minimal` eng kam yozadi, lekin replika ham, PITR ham bo'lmaydi. `replica` standart qiymat, streaming replication va arxivdan tiklash uchun yetarli. `logical` qo'shimcha ma'lumot yozadi va logical replication yoki CDC uchun kerak. Outbox naqshini Debezium bilan ishlatish rejasi bo'lsa, `logical` ni boshidan yoqib qo'yish kerak, chunki uni o'zgartirish restart talab qiladi.

```sql
-- WAL bilan bog'liq hamma sozlamani bir ko'rishda tekshirish
SELECT name, setting, unit, context
FROM pg_settings
WHERE name IN ('wal_level','synchronous_commit','full_page_writes','wal_compression',
               'wal_buffers','max_wal_size','min_wal_size','checkpoint_timeout',
               'checkpoint_completion_target','archive_mode')
ORDER BY name;

-- WAL generatsiya tezligi: ikki o'lchov orasidagi farqni oling
SELECT pg_current_wal_lsn() AS lsn, pg_walfile_name(pg_current_wal_lsn()) AS segment;

-- Replikatsiya kechikishi va slot ushlab turgan WAL hajmi
SELECT slot_name, active, pg_size_pretty(
         pg_wal_lsn_diff(pg_current_wal_lsn(), restart_lsn)) AS ushlangan_wal
FROM pg_replication_slots;
```

`synchronous_commit` ma'lumot xavfsizligining asosiy tugmasi. `on` (standart) commit ni mahalliy WAL diskka tushmaguncha kutadi. `off` kutmaydi, natijada commit 10-50 barobar tez bo'ladi, lekin crash paytida oxirgi `wal_writer_delay` ichidagi commitlar yo'qoladi; tranzaksiya atomikligi buzilmaydi, faqat tasdiqlangan commit yo'qolishi mumkin. `local` replikani kutmaydi, `remote_write` va `remote_apply` esa sinxron replikadan tasdiq kutadi.

Arxitektorning asosiy qarori shu yerda: xavfsizlik darajasi butun instans uchun bir xil bo'lishi shart emas. To'lov tranzaksiyasi `synchronous_commit = on` bilan ketadi, audit log yoki metrika yozuvi esa o'sha sessionda `SET LOCAL synchronous_commit = off` qilib tezlashtiriladi. `full_page_writes` ni o'chirish esa deyarli har doim xato, chunki u qisman yozilgan sahifadan himoya qiladi.

| Tuzoq | Nimaga olib keladi | Yechim |
|---|---|---|
| `@Transactional` ichida tashqi HTTP chaqiriq | `idle in transaction`, vacuum to'xtaydi, bloat o'sadi | Tranzaksiyani HTTP dan oldin yopish, `idle_in_transaction_session_timeout = 30s` |
| `max_connections = 500`, pool yo'q | Lock manager va snapshot CPU ni yeydi, latency sakraydi | PgBouncer transaction rejimi, backend soni yadro sonidan 2-4 barobar |
| Faol bo'lmagan replication slot qolgan | WAL to'planadi, `pg_wal` disk to'ladi, instans to'xtaydi | `pg_replication_slots` monitoringi, `max_slot_wal_keep_size` o'rnatish |
| `checkpoint_timeout = 5min`, katta yozuv | Har 5 daqiqada I/O cho'qqisi, p99 ikki barobar | `checkpoint_timeout = 15min`, `max_wal_size` kattalashtirish |
| Uzoq ishlaydigan hisobot tranzaksiyasi | Barcha jadvalda o'lik tuple tozalanmaydi | Hisobotni replikada bajarish, `hot_standby_feedback` ni o'ylab qo'yish |
| Tez-tez yangilanadigan ustun indekslangan | HOT update buziladi, indeks shishadi, WAL ko'payadi | Keraksiz indeksni olib tashlash, `fillfactor = 80` |
| Toast ustuniga `LIKE '%...%'` qidiruv | Har satr uchun dekompressiya, CPU yonadi | Alohida qidiruv ustuni yoki GIN indeksli `tsvector` |
| `autovacuum_vacuum_cost_delay` standart qoldirilgan | Katta jadvalda vacuum yetib ulgurmaydi | Jadval darajasida `cost_delay = 0`, `cost_limit = 1000` |

## 21.6 Checkpoint: qachon boshlanadi, I/O cho'qqisi va `checkpoint_timeout` sozlash

Checkpoint bu barcha iflos sahifalarni diskka tushirish va WAL da "shu nuqtadan tiklash boshlanadi" degan belgi qo'yish jarayoni. U uch holatda boshlanadi: `checkpoint_timeout` vaqti o'tganda (standart 5 daqiqa), `max_wal_size` chegarasiga yetilganda (standart 1 GB), yoki `CHECKPOINT` buyrug'i va to'g'ri to'xtatish paytida.

Ikki tur orasidagi farq muhim. Vaqt bo'yicha (`timed`) checkpoint rejali va yoyilgan, talab bo'yicha (`requested`) checkpoint esa yozuv hajmi bosganini bildiradi va odatda keskin I/O cho'qqisi yaratadi. Sog'lom instansda `requested` checkpointlar deyarli bo'lmasligi kerak.

```sql
-- PostgreSQL 17: checkpointer statistikasi alohida ko'rinishda
SELECT num_timed, num_requested,
       round(write_time / 1000.0) AS yozish_sek,
       round(sync_time / 1000.0) AS sync_sek, buffers_written
FROM pg_stat_checkpointer;

-- PostgreSQL 15 va 16 da shu ma'lumot pg_stat_bgwriter ichida
SELECT checkpoints_timed, checkpoints_req,
       checkpoint_write_time, checkpoint_sync_time, buffers_checkpoint
FROM pg_stat_bgwriter;

-- Oxirgi checkpoint qachon va qaysi LSN da bo'lgani
SELECT checkpoint_lsn, redo_lsn, checkpoint_time,
       pg_size_pretty(pg_wal_lsn_diff(pg_current_wal_lsn(), redo_lsn)) AS redo_dan_keyin
FROM pg_control_checkpoint();
```

Sozlash mantiqi: `checkpoint_timeout` ni 15 daqiqaga ko'tarish iflos sahifalarni ko'proq qayta ishlatish imkonini beradi, ya'ni bir xil sahifa 5 daqiqada uch marta emas, 15 daqiqada bir marta yoziladi. Narxi crash dan keyin tiklanish vaqtining uzayishi. `max_wal_size` ni shunday tanlash kerakki, `checkpoint_timeout` ichida generatsiya bo'ladigan WAL undan kichik bo'lsin. Yozuv og'ir to'lov tizimida `checkpoint_timeout = 15min`, `max_wal_size = 16GB`, `checkpoint_completion_target = 0.9` kombinatsiyasi ko'p holatda p99 latency ni tekislaydi. `wal_compression = lz4` esa checkpointdan keyingi full page image larni 2-4 barobar siqib, WAL hajmini kamaytiradi.

## 21.7 Vacuum nima qiladi: o'lik tuple, visibility map, index-only scan bilan bog'liqligi

MVCC tufayli DELETE va UPDATE hech narsani darhol o'chirmaydi, faqat tuple ni o'lik deb belgilaydi. VACUUM uch ish qiladi. Birinchi, hech bir snapshot ko'rmaydigan o'lik tuple larning joyini qayta ishlatish uchun bo'shatadi. Ikkinchi, indekslardan o'sha tuple larga bo'lgan ko'rsatkichlarni olib tashlaydi. Uchinchi, visibility map ni yangilaydi.

Visibility map har sahifa uchun ikki bit saqlaydi: `all-visible` va `all-frozen`. `all-visible` biti index-only scan uchun hayotiy ahamiyatga ega: agar sahifa to'liq ko'rinarli bo'lsa, planner heap ga murojaat qilmasdan faqat indeksdan javob beradi. Shuning uchun covering indeks qo'ygan odam `EXPLAIN` da `Heap Fetches: 900000` ko'rsa, muammo indeksda emas, vacuum qarzida.

```sql
-- O'lik tuple nisbati va oxirgi vacuum qachon bo'lgani
SELECT relname, n_live_tup, n_dead_tup,
       round(100.0 * n_dead_tup / nullif(n_live_tup + n_dead_tup, 0), 1) AS olik_foiz,
       last_autovacuum, autovacuum_count
FROM pg_stat_user_tables
WHERE n_dead_tup > 10000 ORDER BY olik_foiz DESC LIMIT 10;

-- Visibility map holati: index-only scan samarasi shunga bog'liq
CREATE EXTENSION IF NOT EXISTS pg_visibility;
SELECT * FROM pg_visibility_map_summary('buyurtmalar');

-- Ketayotgan vacuum qaysi fazada va qancha qilgani
SELECT pid, relid::regclass, phase, heap_blks_total, heap_blks_scanned,
       index_vacuum_count FROM pg_stat_progress_vacuum;
```

VACUUM tuple larni siqib, faylni kichraytirmaydi, faqat sahifa ichida joy bo'shatadi. Faylni qisqartirish uchun `VACUUM FULL` kerak, lekin u `ACCESS EXCLUSIVE` lock oladi va jadvalni butunlay bloklaydi.

## 21.8 Autovacuum sozlamalari va u yetishmay qolganda nima bo'ladi

Autovacuum launcher har `autovacuum_naptime` (standart 1 daqiqa) da bazalarni ko'rib chiqadi va ishchi ishga tushiradi. Jadval vacuum ga tushish sharti: o'lik tuple soni `autovacuum_vacuum_threshold` (50) plus `autovacuum_vacuum_scale_factor` (0.2) karra satr sonidan oshsa. Ya'ni 100 million satrli buyurtma jadvali 20 million o'lik tuple to'planmaguncha tozalanmaydi. Bu katta jadvallar uchun juda kech.

Ikkinchi muammo tezlik. `autovacuum_vacuum_cost_delay` standart qiymati 2 ms va `vacuum_cost_limit` 200, bu throughput ni taxminan sekundiga bir necha MB ga cheklaydi. Katta jadvalda bu vacuum ning yetib ulgurmasligiga olib keladi: o'lik tuple lar vacuum tozalaganidan tez to'planadi, jadval shishadi, so'rovlar sekinlashadi va bu o'z navbatida yana ko'proq lock yaratadi.

```sql
-- Katta va tez o'zgaradigan jadvalga individual autovacuum rejimi
ALTER TABLE buyurtmalar SET (
  autovacuum_vacuum_scale_factor = 0.02,   -- 20% emas, 2%
  autovacuum_vacuum_threshold = 5000,
  autovacuum_vacuum_cost_delay = 0,        -- throttling'ni olib tashlash
  autovacuum_vacuum_cost_limit = 2000,
  autovacuum_analyze_scale_factor = 0.01
);

-- Faqat INSERT bo'ladigan log jadvalida visibility map uchun (PG 13+)
ALTER TABLE tolov_audit SET (autovacuum_vacuum_insert_threshold = 50000);

-- Instans darajasi (postgresql.conf): 16 yadroli serverda
-- autovacuum_max_workers = 6
-- autovacuum_naptime = '15s'
-- maintenance_work_mem = '1GB'
-- log_autovacuum_min_duration = '1s'
```

Autovacuum ni butunlay o'chirish deyarli har doim halokatga olib keladi, chunki u nafaqat joy bo'shatadi, balki transaction ID freeze ishini ham bajaradi. `maintenance_work_mem` vacuum ning o'lik tuple identifikatorlari uchun ishlatadigan xotirasi; u kichik bo'lsa vacuum indekslarni bir necha marta aylanib o'tadi. PostgreSQL 17 da bu struktura samaraliroq bo'ldi va bir xil xotirada ko'proq TID saqlaydi.

## 21.9 Transaction ID o'ralishi (wraparound) va freeze jarayoni

Transaction ID 32 bitli, ya'ni taxminan 4 milliard qiymat, undan amalda 2 milliardi ishlatiladi. Tuple ning ko'rinishi `xmin` ni hozirgi XID bilan taqqoslash orqali aniqlanadi, shuning uchun XID hisoblagich aylanib ketsa, eski tuple "kelajakdan" ko'rinib qoladi. Buning oldini olish uchun yetarlicha qadimgi tuple lar `frozen` deb belgilanadi, ya'ni ular doim ko'rinarli hisoblanadi va XID taqqoslashga muhtoj emas.

`vacuum_freeze_min_age` (standart 50 million) qanchalik qadimgi tuple freeze bo'lishini, `autovacuum_freeze_max_age` (standart 200 million) esa autovacuum majburan aggressive vacuum boshlash chegarasini belgilaydi. Agar freeze orqada qolsa, PostgreSQL avval ogohlantirish log yozadi, keyin `vacuum_failsafe_age` (standart 1.6 milliard) da barcha throttling va indeks tozalashni tashlab, faqat freeze ga kirishadi. 2 milliardga yetilsa instans yozuvni rad etadi va faqat single user rejimda tiklanadi.

```sql
-- Baza darajasida wraparound'ga qancha qolgani
SELECT datname, age(datfrozenxid) AS xid_yoshi,
       round(100.0 * age(datfrozenxid) / 2000000000, 1) AS sarflangan_foiz
FROM pg_database ORDER BY 2 DESC;

-- Eng xavfli jadvallar: freeze orqada qolganlari
SELECT c.relname, age(c.relfrozenxid) AS xid_yoshi,
       pg_size_pretty(pg_total_relation_size(c.oid)) AS hajm
FROM pg_class c JOIN pg_namespace n ON n.oid = c.relnamespace
WHERE c.relkind IN ('r','m','t') AND n.nspname NOT LIKE 'pg\_%'
ORDER BY 2 DESC LIMIT 10;

-- Qo'lda tezkor freeze: oynadagi vaqtda, parallel bilan
VACUUM (FREEZE, VERBOSE, PARALLEL 4) buyurtmalar;
```

Monitoringda bitta alert yetarli: `age(datfrozenxid)` 500 million dan oshsa ogohlantirish, 1 milliarddan oshsa jiddiy hodisa. Yuqori yozuvli tizimda XID sarfi kuniga 50-100 million bo'lishi mumkin, demak zaxira vaqti haftalar bilan o'lchanadi, oylar bilan emas.

## 21.10 Jadval va indeks shishishi (bloat): o'lchash va tuzatish

Bloat bu jadval yoki indeks fayli ichidagi, ishlatilmayotgan lekin bo'shatilmagan joy. Manbasi uchta: vacuum qarzi, uzoq tranzaksiyalar va tez-tez UPDATE qilinadigan keng satrlar. Natijasi oddiy: bir xil ma'lumotni o'qish uchun ko'proq sahifa o'qiladi, kesh samarasi tushadi, sequential scan sekinlashadi.

Aniq o'lchov uchun `pgstattuple` ishlatiladi, lekin u butun jadvalni o'qiydi, shuning uchun katta jadvalda `pgstattuple_approx` yoki past yuklangan vaqtni tanlash kerak.

```sql
CREATE EXTENSION IF NOT EXISTS pgstattuple;

-- Jadval bloat: free_percent va dead_tuple_percent muhim
SELECT * FROM pgstattuple_approx('buyurtmalar');

-- Indeks bloat: avg_leaf_density 70% dan past bo'lsa reindex foydali
SELECT index_size, avg_leaf_density, leaf_fragmentation
FROM pgstatindex('buyurtmalar_mijoz_id_idx');

-- Hech ishlatilmaydigan indekslar: ularni o'chirish bloat va WAL ni kamaytiradi
SELECT relname, indexrelname, idx_scan,
       pg_size_pretty(pg_relation_size(indexrelid)) AS hajm
FROM pg_stat_user_indexes WHERE idx_scan = 0
ORDER BY pg_relation_size(indexrelid) DESC LIMIT 10;
```

Tuzatishda uch yo'l bor. `REINDEX INDEX CONCURRENTLY` indeksni yozuvni bloklamasdan qayta quradi va ko'pincha yetarli. `pg_repack` extension jadvalni ham online qayta zichlashtiradi, lekin oxirida qisqa vaqt exclusive lock oladi. `VACUUM FULL` eng samarali siqadi, lekin jadvalni to'liq bloklaydi va shuning uchun faqat rejali oynada qo'llanadi. Vaqt bo'yicha o'sadigan `tolov_audit` kabi jadvalda eng to'g'ri yechim umuman boshqacha: partitioning va eski partition ni `DROP TABLE` qilish, chunki u bloat masalasini butunlay yo'q qiladi.

## 21.11 `TOAST`: katta qiymatlar qanday saqlanadi

Tuple sahifadan katta bo'lishi mumkin emas, shuning uchun PostgreSQL satr hajmi taxminan 2 KB (`toast_tuple_target`, standart 2032 bayt) dan oshsa, katta ustunlarni siqadi va kerak bo'lsa alohida TOAST jadvaliga 2 KB ga yaqin chunk larga bo'lib chiqaradi. TOAST jadvali `pg_toast` sxemasida yashaydi va o'z indeksiga ega.

Har bir ustun uchun strategiya tanlanadi: `EXTENDED` (standart, siqadi va kerak bo'lsa chiqaradi), `EXTERNAL` (siqmaydi, lekin chiqaradi), `MAIN` (imkon qadar ichida qoldiradi), `PLAIN` (umuman TOAST qilmaydi). JSONB hisobot payload ida `substring` yoki prefiks qidiruv ko'p bo'lsa, `EXTERNAL` tezroq bo'ladi, chunki dekompressiya kerak emas. PostgreSQL 14 dan `default_toast_compression = lz4` mavjud va u `pglz` dan 2-4 barobar tez siqadi.

```sql
-- Jadvalning TOAST qismi qancha joy egallaydi
SELECT c.relname,
       pg_size_pretty(pg_relation_size(c.oid)) AS heap,
       pg_size_pretty(pg_relation_size(t.oid)) AS toast,
       pg_size_pretty(pg_indexes_size(c.oid)) AS indekslar
FROM pg_class c LEFT JOIN pg_class t ON t.oid = c.reltoastrelid
WHERE c.relname = 'hisobot_natija';

-- Ustun darajasida strategiya va siqish usuli
ALTER TABLE hisobot_natija ALTER COLUMN payload SET STORAGE EXTERNAL;
ALTER TABLE hisobot_natija ALTER COLUMN payload SET COMPRESSION lz4;

-- Qiymat TOAST bo'lganini tekshirish
SELECT pg_column_size(payload) AS saqlangan_bayt,
       octet_length(payload) AS haqiqiy_bayt
FROM hisobot_natija LIMIT 5;
```

TOAST ning yashirin narxi: `SELECT *` bilan 200 KB li JSONB ni har safar tortib olish tarmoq va CPU yeydi, hatto application unga qaramasa ham. Hibernate da bunday ustunni `@Basic(fetch = FetchType.LAZY)` yoki alohida entity ga ajratish kerak. Shuningdek TOAST jadvalining o'z vacuum i bor; uni `VACUUM (PROCESS_TOAST on)` boshqaradi va katta payload li jadvalda TOAST bloat asosiy jadvaldan kattaroq bo'lishi mumkin.

Quyidagi jadval butun bob bo'yicha ikki xil fikrlashni qiyoslaydi.

| Masala | Oddiy yondashuv | Arxitektor yondashuvi |
|---|---|---|
| Ulanish soni | `max_connections` ni 500 ga ko'tarish | Pool ni yadro soniga bog'lash, PgBouncer transaction rejimi, 40-60 faol backend |
| `shared_buffers` | RAM ning 75 foizi, "ko'proq yaxshi" | RAM ning 25 foizi plus `effective_cache_size`, `pg_buffercache` bilan tasdiqlash |
| Commit tezligi | Butun bazaga `synchronous_commit = off` | To'lov yo'lida `on`, audit yo'lida sessiya darajasida `off` |
| Checkpoint | Standart 5 daqiqa, tegmaslik | `checkpoint_timeout = 15min`, `max_wal_size` ni WAL tezligiga moslash, `requested` ni nolga tushirish |
| Vacuum | Kecha kerak bo'lganda `VACUUM FULL` | Jadval darajasida `scale_factor = 0.02`, `cost_delay = 0`, o'lik tuple monitoringi |
| Wraparound | Esga ham kelmaydi | `age(datfrozenxid)` ga alert, XID sarf tezligini o'lchash, freeze oynasi |
| Bloat | Hajm o'sganda indeks qo'shish | `pgstattuple` bilan o'lchash, `REINDEX CONCURRENTLY`, vaqt bo'yicha partitioning |
| Katta JSONB | Entity ga oddiy ustun qilib qo'yish | TOAST strategiyasi, `lz4`, lazy fetch, alohida jadval |
| UPDATE yuki | Hamma ustunga indeks qo'yish | HOT update ni saqlash, `fillfactor = 80`, keraksiz indeksni o'chirish |
| Hisobot so'rovi | Asosiy bazada uzoq tranzaksiya | Replikada bajarish, snapshot ushlab turmaslik, vacuum ni erkin qoldirish |

## 21.12 Amalda qo'llash

- [ ] `pg_stat_activity` dan `idle in transaction` sessionlarini sanab chiqing va `idle_in_transaction_session_timeout` ni 30 sekundga qo'ying.
- [ ] HikariCP `maximum-pool-size` ni barcha instanslar bo'yicha qo'shib, PostgreSQL yadro sonining 2-4 barobaridan oshmasligini tekshiring.
- [ ] `pg_stat_checkpointer` (yoki 16 va pastda `pg_stat_bgwriter`) dagi `num_requested` ni o'lchab, nolga yaqin bo'lmasa `checkpoint_timeout` va `max_wal_size` ni kattalashtiring.
- [ ] Eng katta uchta jadvalga individual `autovacuum_vacuum_scale_factor = 0.02` va `autovacuum_vacuum_cost_delay = 0` qo'yib, o'lik tuple nisbatini bir hafta kuzating.
- [ ] `age(datfrozenxid)` uchun monitoringga alert qo'shing: 500 million da ogohlantirish, 1 milliardda jiddiy hodisa.
- [ ] Index-only scan kutilgan so'rovlarda `EXPLAIN (ANALYZE, BUFFERS)` dagi `Heap Fetches` ni tekshirib, `pg_visibility_map_summary` bilan vacuum qarzini tasdiqlang.
- [ ] `pgstattuple_approx` bilan top 10 jadvalning bloat foizini o'lchab, 30 foizdan oshganlar uchun `pg_repack` yoki partitioning rejasini yozing.
- [ ] Katta JSONB yoki matn ustunlari uchun `pg_column_size` ni o'lchab, `lz4` siqish va lazy fetch ni joriy qiling.

---

[&larr; 20. Spring Security: filter chain, OAuth2, JWT](20-spring-security-filter-chain-oauth2-jwt.md) · [Mundarija](README.md) · [22. MVCC, izolyatsiya darajalari, lock va deadlock &rarr;](22-mvcc-izolyatsiya-darajalari-lock-va-deadlock.md)
