<!-- doc: architect | chapter: 21 | part: IV. PostgreSQL chuqur bilim -->

[Barcha hujjatlar](../../README.md) / [Arxitektor miyasi](README.md)

> Holat: tekshirilgan (2026-10-19). Manbalar bob oxirida.

# 21. PostgreSQL arxitekturasi: process model, WAL, checkpoint, vacuum (PostgreSQL Architecture)

<details>
<summary>Bu bobdagi 25 bo'lim</summary>

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
- [21.12 Buffer cache ichida: clock sweep, buffer ring va keshni isitish](#2112-buffer-cache-ichida-clock-sweep-buffer-ring-va-keshni-isitish)
- [21.13 Sahifani tozalash (page pruning), HOT zanjiri va `fillfactor`](#2113-sahifani-tozalash-page-pruning-hot-zanjiri-va-fillfactor)
- [21.14 `pg_xact`, hint bit, virtual transaction va subtransaction](#2114-pg_xact-hint-bit-virtual-transaction-va-subtransaction)
- [21.15 Nosozlikdan tiklanish: startup protsess, full page write va checksum](#2115-nosozlikdan-tiklanish-startup-protsess-full-page-write-va-checksum)
- [21.16 Xotira tuzilmalari qulfi: spinlock, lightweight lock va wait event](#2116-xotira-tuzilmalari-qulfi-spinlock-lightweight-lock-va-wait-event)
- [21.17 Vacuum fazalari: heap scan, index vacuuming va heap truncation](#2117-vacuum-fazalari-heap-scan-index-vacuuming-va-heap-truncation)
- [21.18 Autovacuum ichida: ishchi soni, `cost_limit` bo'linishi va kuzatish](#2118-autovacuum-ichida-ishchi-soni-cost_limit-bolinishi-va-kuzatish)
- [21.19 Freeze mexanikasi: hint bit, aggressive freezing, freeze map va CLOG](#2119-freeze-mexanikasi-hint-bit-aggressive-freezing-freeze-map-va-clog)
- [21.20 Boshlang'ich yuklashda freeze: `COPY FREEZE` va `index_cleanup`](#2120-boshlangich-yuklashda-freeze-copy-freeze-va-index_cleanup)
- [21.21 Checkpoint bosqichlari va `log_checkpoints` bilan kuzatish](#2121-checkpoint-bosqichlari-va-log_checkpoints-bilan-kuzatish)
- [21.22 Background writer: `bgwriter_delay` va `bgwriter_lru_maxpages`](#2122-background-writer-bgwriter_delay-va-bgwriter_lru_maxpages)
- [21.23 WAL segmentlari, `pg_waldump` va `wal_skip_threshold`](#2123-wal-segmentlari-pg_waldump-va-wal_skip_threshold)
- [21.24 Klaster fayllari: `template0`, forklar va UNLOGGED jadval](#2124-klaster-fayllari-template0-forklar-va-unlogged-jadval)
- [21.25 Amalda qo'llash](#2125-amalda-qollash)

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

Amaliy qoida: haqiqiy parallel ishlayotgan backendlar soni CPU yadrosi sonidan bir necha barobar ko'p bo'lmasin. Boshlang'ich mo'ljal yadro sonining 2 dan 4 barobariga teng, ya'ni 16 yadroli serverda 40 dan 60 gacha faol backend, lekin bu o'lchanmagan taxmin: maksimal throughput nuqtasi yuklamaning CPU va IO nisbatiga bog'liq va faqat o'lchov bilan topiladi. Qolgan hamma narsa pool va PgBouncer vazifasi.

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

`huge_pages` ning standart qiymati allaqachon `try`, shuning uchun uni `try` ga qo'yish hech narsani o'zgartirmaydi: `try` da server huge page so'raydi, olmasa oddiy sahifaga jim qaytadi va sozlama ishlamaganini hech kim bilmaydi. 16 GB dan katta `shared_buffers` da haqiqiy qadam ikki bosqichli: avval OS da huge page hovuzini sozlash, keyin `huge_pages = on` qo'yish. Kerakli sahifa sonini PostgreSQL o'zi hisoblaydi, serverni ko'tarmasdan ham: `postgres -D $PGDATA -C shared_memory_size_in_huge_pages` chiqargan sonni `sysctl -w vm.nr_hugepages=<son>` ga berib, `/etc/sysctl.conf` ga yozib qo'yiladi. `on` da huge page olinmasa server ishga tushmaydi va bu aynan kerakli xulq: xato startupda ko'rinadi, prodda tushunarsiz sekinlashuv bo'lib emas. Parametr `postmaster` kontekstida, ya'ni restart talab qiladi, va faqat Linux bilan Windows da ishlaydi. Foyda tomoni: huge page sahifa jadvalini kichraytiradi va xotira boshqaruviga ketadigan CPU vaqtini kamaytiradi; rasmiy hujjat aniq foiz bermaydi, shuning uchun yutuqni o'z yuklamangizda o'lchash kerak. PostgreSQL 16 dan boshlab `pg_stat_io` ko'rinishi o'qish va yozishni kontekst bo'yicha ajratib beradi, bu checkpoint va vacuum I/O sini aralashtirmasdan o'lchash imkonini beradi.

`pg_statio_user_tables` kabi ko'rinishlar bufer kesh hisoblagichlarini doim beradi, lekin ulardagi I/O VAQTI faqat `track_io_timing` yoqilgan bo'lsa to'ladi; standart holatda bu parametr o'chiq (Rogov, 9.4, 154-bet). Shuning uchun "disk sekin" degan gipotezani tekshirish birinchi qadamdan boshlanadi: `track_io_timing = on` qo'yib, `EXPLAIN (ANALYZE, BUFFERS)` dan `I/O Timings` qatorini olish, aks holda sabab o'rniga faqat o'qilgan bloklar soni ko'rinadi.

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

Yuqoridagi so'rovdagi `reltuples` va `relpages` ni aniq son deb o'qish xato. Bular `pg_class` dagi asosiy statistika, ya'ni relationdagi tuple soni, sahifalar soni va visibility map da belgilangan sahifalar soni (`relallvisible`); ularni analiz yig'adi va vacuum aniqlashtiradi (Rogov, 17.1, 271-bet). Filtrsiz so'rovda planner kardinallik bahosini to'g'ridan-to'g'ri `reltuples` dan oladi, shuning uchun eskirgan statistika darhol noto'g'ri planga aylanadi; hech analiz qilinmagan jadvalda `reltuples` qiymati -1 bo'ladi (Rogov, 17.1, 272-bet).

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

`synchronous_commit` ma'lumot xavfsizligining asosiy tugmasi. `on` (standart) commit ni mahalliy WAL diskka tushmaguncha kutadi. `off` kutmaydi, natijada commit sezilarli tez bo'ladi (qo'llanma buni raqam bilan bermaydi: kritik bo'lmagan tranzaksiyalar uchun `synchronous_commit` ni o'chirish `fsync` ni o'chirishdan keladigan foydaning katta qismini beradi, lekin ma'lumot buzilishi xavfisiz deb yozilgan), lekin crash paytida oxirgi `3 x wal_writer_delay` ichidagi commitlar yo'qoladi (standart sozlamada 0.6 sekund); tranzaksiya atomikligi buzilmaydi, faqat tasdiqlangan commit yo'qolishi mumkin. `local` replikani kutmaydi, `remote_write` va `remote_apply` esa sinxron replikadan tasdiq kutadi.

Sinxron rejimdan chiqmasdan ham commitlarni paketlash mumkin. Tranzaksiyani yakunlayotgan backend WAL ni diskka tushirishdan oldin `commit_delay` (standart 0) davomida kichik pauza qilishi mumkin, lekin faqat tizimda kamida `commit_siblings` (standart 5) ta faol tranzaksiya bo'lsa: pauza ichida ulardan bir qismi tugaydi va server hamma WAL yozuvini bitta sinxronlashda tushiradi. Rogov buni liftning eshigini yugurib kelayotgan odam uchun ushlab turishga qiyoslaydi va standart holatda pauza yo'qligini, bu parametrni faqat qisqa OLTP tranzaksiyalari ko'p bo'lgan tizimda o'zgartirish mantiqan to'g'riligini aytadi (Rogov, 11.1, 183-bet).

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

Visibility map har sahifa uchun ikki bit saqlaydi: `all-visible` va `all-frozen`. `all-visible` biti index-only scan uchun hayotiy ahamiyatga ega: agar sahifa to'liq ko'rinarli bo'lsa, planner heap ga murojaat qilmasdan faqat indeksdan javob beradi. Shuning uchun covering indeks qo'ygan odam `EXPLAIN` da `Heap Fetches: 900000` ko'rsa, muammo indeksda emas, vacuum qarzida. Ikkinchi bit, `all-frozen`, freeze map deb ataladi va uning vazifasi boshqa: u tufayli freeze uchun butun jadvalni skan qilish shart emas ([Freeze mexanikasi](#2119-freeze-mexanikasi-hint-bit-aggressive-freezing-freeze-map-va-clog) bo'limiga qarang).

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

VACUUM tuple larni siqmaydi va ularni ko'chirmaydi, shuning uchun fayl o'rtasida bo'shagan joy faylning ichida qoladi va faqat yangi qatorlar uchun qayta ishlatiladi. O'rtadagi joyni operatsion tizimga qaytarish uchun `VACUUM FULL` kerak, lekin u `ACCESS EXCLUSIVE` lock oladi va jadvalni butunlay bloklaydi. Fayl oxiridagi uzluksiz bo'sh sahifalar esa istisno: ularni oddiy vacuum ham kesib tashlaydi va bu qaysi shartlarda bo'lishi [Vacuum fazalari](#2117-vacuum-fazalari-heap-scan-index-vacuuming-va-heap-truncation) bo'limida yozilgan.

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
-- autovacuum_vacuum_cost_limit = 2000   -- ishchi soni bilan BIRGA oshadi
-- autovacuum_work_mem = '256MB'
-- autovacuum_naptime = '15s'
-- maintenance_work_mem = '1GB'
-- log_autovacuum_min_duration = '1s'
```

Autovacuum ni butunlay o'chirish deyarli har doim halokatga olib keladi, chunki u nafaqat joy bo'shatadi, balki transaction ID freeze ishini ham bajaradi. `maintenance_work_mem` vacuum ning o'lik tuple identifikatorlari uchun ishlatadigan xotirasi; u kichik bo'lsa vacuum indekslarni bir necha marta aylanib o'tadi. PostgreSQL 17 da bu struktura samaraliroq bo'ldi va bir xil xotirada ko'proq TID saqlaydi.

Yuqoridagi konfiguratsiyada `autovacuum_max_workers` va `autovacuum_vacuum_cost_limit` ataylab yonma-yon turadi: ishchi sonini yolg'iz oshirish autovacuum ni tezlashtirmaydi, chunki ish birliklari chegarasi barcha ishchilar orasida bo'linadi. Sabab va to'g'ri nisbat [Autovacuum ichida](#2118-autovacuum-ichida-ishchi-soni-cost_limit-bolinishi-va-kuzatish) bo'limida.

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

To'rtinchi yo'l `CLUSTER` buyrug'i. U `VACUUM FULL` bilan bir xil ishlaydi, ya'ni eski fayllarni o'chirib jadvalni qaytadan yozadi, lekin tuple larni tanlangan indeks tartibida joylashtiradi va ba'zi hollarda planner index scan dan samaraliroq foydalanishiga yordam beradi. Ikki shart yodda tursin: jadval butun davomida eksklyuziv qulflanadi va klasterlangan tartib saqlanmaydi, ya'ni keyingi har bir yangilash fizik tartibni buzib boradi. `VACUUM FULL` ning o'zi dasturiy jihatdan `CLUSTER` ning tuple larni qayta tartiblamaydigan maxsus holati (Rogov, 8.2, 140-bet).

## 21.11 `TOAST`: katta qiymatlar qanday saqlanadi

Tuple sahifadan katta bo'lishi mumkin emas, shuning uchun PostgreSQL satr hajmi taxminan 2 KB (`toast_tuple_target`, standart 2032 bayt) dan oshsa, katta ustunlarni siqadi va kerak bo'lsa alohida TOAST jadvaliga 2 KB ga yaqin chunk larga bo'lib chiqaradi. TOAST jadvali `pg_toast` sxemasida yashaydi va o'z indeksiga ega.

Har bir ustun uchun strategiya tanlanadi: `EXTENDED` (standart, siqadi va kerak bo'lsa chiqaradi), `EXTERNAL` (siqmaydi, lekin chiqaradi), `MAIN` (imkon qadar ichida qoldiradi), `PLAIN` (umuman TOAST qilmaydi). JSONB hisobot payload ida `substring` yoki prefiks qidiruv ko'p bo'lsa, `EXTERNAL` tezroq bo'ladi, chunki dekompressiya kerak emas. PostgreSQL 14 dan `default_toast_compression = lz4` mavjud (default esa hamon `pglz`). lz4 odatda tezroq siqadi, lekin tezlik nisbati bu yerda raqam bilan berilmaydi: qo'llanma uni bermaydi va u ma'lumot shakliga bog'liq, shuning uchun o'z payload ingizda o'lchash kerak.

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

## 21.12 Buffer cache ichida: clock sweep, buffer ring va keshni isitish

Har bir bufer ikki qismdan iborat: 8 KB li sahifa va uning headeri. Header sahifaning fizik manzilini (fayl, fork, blok raqami), `dirty` bayrog'ini, foydalanish hisoblagichini va pin sonini saqlaydi. Sahifa ishlatilayotganda buferga pin qo'yiladi; pin uni siqib chiqarishdan himoya qiladi va har bir pin hisoblagichni oshiradi.

Bo'sh bufer qolmaganda PostgreSQL clock sweep algoritmini ishlatadi: strelka buferlar bo'ylab aylanadi va har o'tganda foydalanish hisoblagichini bittaga kamaytiradi; pin qo'yilmagan va hisoblagichi nolga tushgan birinchi bufer tozalanadi. Hisoblagich 5 bilan cheklangan, aks holda strelka bir necha aylanish qilishga majbur bo'lar edi.

Ommaviy operatsiyalar butun keshni yuvib yubormasligi uchun ular kichik buffer ring ichida ishlaydi va siqib chiqarish faqat shu ring chegarasida boradi. Kitob uchta strategiyani sanaydi: kesh hajmining choragidan katta jadvalni ketma-ket o'qishda ring 256 KB (32 sahifa); `COPY FROM`, `CREATE TABLE AS SELECT`, `CREATE MATERIALIZED VIEW` va jadvalni qayta yozadigan `ALTER TABLE` uchun standart 16 MB (2048 sahifa), lekin hech qachon kesh hajmining sakkizdan biridan oshmaydi; vacuum uchun yana 256 KB. Muhim istisno: ko'p qator o'zgartiradigan `UPDATE` yoki `DELETE` da sahifalar doim o'zgarib turgani uchun ring amalda foyda bermay qoladi. Ketma-ket o'qishda esa qo'shimcha yutuq bor: jadval allaqachon skan qilinayotgan bo'lsa, ikkinchi skanni boshlagan protsess mavjud ring ga qo'shiladi va hozir ochiq turgan ma'lumotdan qo'shimcha I/O siz foydalanadi, birinchi protsess skanni tugatgach esa o'tkazib yuborilgan qismiga qaytadi (Rogov, 9.5, 156-bet). Shuning uchun bitta katta jadvalni bir vaqtda o'qiydigan ikkita hisobot diskni ikki barobar o'qimaydi.

```sql
-- Buferlarning foydalanish hisoblagichi bo'yicha taqsimlanishi
SELECT usagecount, count(*) FROM pg_buffercache
GROUP BY usagecount ORDER BY usagecount;

-- Restartdan keyin issiq jadvalni oldindan yuklash
CREATE EXTENSION IF NOT EXISTS pg_prewarm;
SELECT pg_prewarm('buyurtmalar');
```

`pg_prewarm` kutubxonasi `shared_preload_libraries` ga qo'shilsa, `autoprewarm leader` protsessi keshdagi sahifalar ro'yxatini vaqti-vaqti bilan `autoprewarm.blocks` fayliga yozadi va restartdan keyin tiklaydi. Vaqtinchalik jadvallar umumiy keshga tushmaydi: ular protsessning lokal keshida yashaydi, hajmi `temp_buffers` bilan cheklanadi va `EXPLAIN (ANALYZE, BUFFERS)` ularni `shared` emas, `local hit=` deb ko'rsatadi.

Spring tomonidagi xulosa: tungi hisobotning katta sequential scan i OLTP ish to'plamini siqib chiqarmaydi, chunki u ring ichida ishlaydi; lekin Spring Batch ning ommaviy `UPDATE` chunk i ringni foydasiz qiladi va keshni haqiqatan yuvadi. Shuning uchun ommaviy yangilashga alohida oyna ajratiladi va undan keyin issiq jadvallar `pg_prewarm` bilan qaytariladi.

## 21.13 Sahifani tozalash (page pruning), HOT zanjiri va `fillfactor`

Vacuum dan tashqari yana bitta, ancha arzon tozalash bor: page pruning. U bitta heap sahifasi ichida ishlaydi va ikki holatda ishga tushadi: oldingi `UPDATE` shu sahifada yangi tuple uchun joy topmagan bo'lsa (bu sahifa headerida qayd etiladi) yoki sahifada `fillfactor` ruxsat berganidan ko'p ma'lumot bo'lsa.

Pruning baza gorizontidan orqada qolgan, ya'ni hech bir snapshotga ko'rinmaydigan tuple larni olib tashlaydi, lekin ularning line pointer larini joyida qoldiradi, chunki ularga indeksdan havola bo'lishi mumkin. Shu sababli u visibility map ni ham, free space map ni ham yangilamaydi: bo'shagan joy yangi `INSERT` uchun emas, shu sahifadagi `UPDATE` uchun saqlanadi. Yana bir natija: sahifa o'qilayotganda ham tozalanishi mumkin, ya'ni oddiy `SELECT` sahifani o'zgartirib, uni iflos qilib qo'yadi.

HOT zanjirining boshiga indeksdan havola bor, shuning uchun uni ko'chirib bo'lmaydi. PostgreSQL ikki bosqichli adreslash ishlatadi: indeks ko'rsatadigan line pointer `redirect` holatiga o'tib, zanjirning joriy boshiga ishora qiladi, oradagi pointer lar esa `unused` ga o'tkaziladi, chunki ularga tashqi havola yo'qligi aniq. Agar sahifada umuman joy qolmasa, zanjir uziladi va boshqa sahifadagi yangi tuple uchun indeksga alohida yozuv qo'shiladi.

```sql
-- Sahifa ichidagi holat: redirect, unused va HOT bayroqlari
CREATE EXTENSION IF NOT EXISTS pageinspect;
SELECT lp, lp_flags, t_ctid
FROM heap_page_items(get_raw_page('ombor_qoldiq', 0));

-- Tez-tez yangilanadigan jadvalda sahifada joy qoldirish
ALTER TABLE ombor_qoldiq SET (fillfactor = 80);
```

`fillfactor` ni pasaytirish HOT ni saqlab qoladi, lekin sahifalarda ko'proq bo'sh joy qolgani uchun jadvalning fizik hajmini oshiradi: bu ataylab qilinadigan almashtirish.

Java tomonida eng ko'p uchraydigan xato Hibernate dan keladi: standart holatda u `UPDATE` ni entity ning hamma ustuni bilan yozadi, shuning uchun o'zgarmagan indekslangan ustun ham "o'zgargan" bo'lib ko'rinadi va HOT sharti buziladi. `@DynamicUpdate` Hibernate ni faqat haqiqatan o'zgargan ustunni yozishga majbur qiladi.

```java
@Entity
@Table(name = "ombor_qoldiq")
@DynamicUpdate
public class StockItem {

    @Id
    private Long id;

    @Column(name = "qoldiq")
    private int quantity;

    @Column(name = "oxirgi_ozgarish")
    private Instant updatedAt;
}
```

PostgreSQL 14 dan B-tree da bottom-up index deletion bor: sahifa bo'linishidan oldin indeks avval o'lik deb belgilangan yozuvlarni tozalaydi, keyin MVCC yangilanishlari hosil qilgan "istiqbolli" dublikatlarni heap orqali tekshiradi. Bu tekshiruv qimmat, lekin ortiqcha sahifa bo'linishidan arzonroq.

## 21.14 `pg_xact`, hint bit, virtual transaction va subtransaction

Tranzaksiya holati `PGDATA/pg_xact` katalogidagi fayllarda saqlanadi (10-versiyagacha katalog nomi `pg_clog` edi) va har bir tranzaksiya uchun ikki bit ajratiladi: committed va aborted. Tuple ni ko'rish uchun `xmin` tranzaksiyasi tugaganmi degan savolga javob kerak: hali faolmi degan qismni umumiy xotiradagi `ProcArray` beradi, tugagan bo'lsa yakuniy holat `pg_xact` dan olinadi.

Har safar `pg_xact` ga borish qimmat, shuning uchun aniqlangan holat tuple headeridagi hint bit larga yoziladi va keyingi o'quvchi na `pg_xact` ga, na `ProcArray` ga boradi. Bitlarni yozuvchi tranzaksiyaning o'zi qo'ya olmaydi: commit paytida qaysi sahifalar o'zgarganini kuzatib yurish qimmat, ular esa keshda bo'lmasligi ham mumkin. Natijada arxitektor uchun muhim oqibat: yangi yuklangan jadvalni birinchi marta o'qiydigan `SELECT` sahifalarni iflos qiladi, checksum yoqilgan bo'lsa (yoki `wal_log_hints` yoqilgan bo'lsa) bu o'zgarishlar WAL ga full page image bo'lib tushadi. Ommaviy yuklashdan keyin "birinchi hisobot sekin, ikkinchisi tez" hodisasining sababi aynan shu.

Faqat o'qiydigan tranzaksiya XID sarflamaydi: unga avval virtual XID beriladi (backend protsess identifikatori va ketma-ket raqam) va haqiqiy XID faqat ma'lumot o'zgartirilganda ajratiladi. Virtual XID lar faqat xotirada yashaydi va hech qachon diskka tushmaydi. Shuning uchun uzoq hisobot tranzaksiyasi XID zaxirasini sarflamaydi, lekin baribir snapshot ushlab turib vacuum ni to'sadi.

Savepoint subtransaction orqali amalga oshiriladi: subtransaction asosiy tranzaksiyanikidan katta o'z XID ini oladi, holati `pg_xact` ga yoziladi, qo'shimcha ma'lumot esa `PGDATA/pg_subtrans` da `pg_xact` kabi bufer orqali saqlanadi. Commit qilingan subtransaction ikkala bitni ham birdan oladi va yakuniy qaror asosiy tranzaksiya holatiga qarab chiqariladi: asosiysi abort bo'lsa hammasi abort hisoblanadi.

```java
@Service
public class PaymentService {

    @Transactional
    public void processBatch(List<PaymentRequest> requests) {
        for (PaymentRequest request : requests) {
            paymentWriter.writeOne(request);
        }
    }
}

@Service
class PaymentWriter {

    // NESTED Spring da JDBC savepoint ochadi, savepoint esa subtransaction
    @Transactional(propagation = Propagation.NESTED)
    void writeOne(PaymentRequest request) {
        // xatolik bo'lsa faqat shu savepoint qaytariladi
    }
}
```

Shu kod 10000 elementli batch da 10000 ta subtransaction ochadi. Kitob subtransaction mexanikasini tavsiflaydi va raqamli chegara bermaydi, lekin mexanizmdan kelib chiqadigan xulosa aniq: har bir savepoint qo'shimcha XID va `pg_subtrans` ga qo'shimcha yozuv degani. Shuning uchun sikl ichida `Propagation.NESTED` ishlatish o'rniga xatoni batch darajasida ushlash arzonroq.

Xato bo'lganda tranzaksiya qanday holatga tushishini ham shu mexanika tushuntiradi. Statement ichida xato chiqsa butun tranzaksiya abort holatiga o'tadi, undan keyingi har qanday buyruq rad etiladi va `COMMIT` ning o'zi `ROLLBACK` bo'lib qaytadi. Sababi atomiklik: allaqachon bajarilgan amallar orqaga qaytarilmaydi, shuning uchun davom etishga ruxsat berilsa, xatodan oldin yozilgan o'zgarishlar ko'rinib qolar va statement atomikligi, demak tranzaksiya atomikligi ham buzilar edi (Rogov, 3.7, 78-bet). ESLATMA: JDBC va Spring tomonida bu holat `SQLSTATE 25P02` bilan keladi; SQLSTATE kodi korpusning qo'shimchasi, kitob uni bermaydi. psql ning `ON_ERROR_ROLLBACK` rejimi har buyruqdan oldin yashirin savepoint qo'yib shu cheklovni yumshatadi, lekin u standart emas, chunki savepoint ochishning o'zi, unga qaytilmasa ham, sezilarli qo'shimcha narx (Rogov, 3.7, 79-bet). Bu narx yuqoridagi `Propagation.NESTED` sikli uchun ham o'sha narx.

## 21.15 Nosozlikdan tiklanish: startup protsess, full page write va checksum

Server ishga tushganda postmaster birinchi bo'lib startup protsessini yaratadi. U `pg_control` faylini o'qiydi va klaster holatini tekshiradi: to'g'ri to'xtatilgan server `shut down` holatida bo'ladi, ishlamayotgan serverdagi `in production` esa nosozlik bo'lganini bildiradi. Shunda tiklanish oxirgi tugagan checkpoint ning REDO pozitsiyasidan boshlanadi; zaxira nusxadan tiklanayotgan bo'lsa pozitsiya `backup_label` faylidan olinadi.

WAL yozuvi sahifaga faqat sahifaning LSN i yozuv LSN idan kichik bo'lsa qo'llanadi. Full page image istisno: u sahifani butunlay qayta yozgani uchun idempotent va LSN tekshirilmasdan qo'llanadi. PostgreSQL da klassik ikki bosqichli tiklanishning ikkinchi bosqichi, ya'ni roll-back, umuman yo'q: tugallanmagan tranzaksiya `pg_xact` da na commit, na abort bitini oladi va u endi ishlamayotgani aniq bo'lgani uchun abort qilingan deb hisoblanadi.

```bash
# Klaster holati va oxirgi checkpoint pozitsiyasi
pg_controldata -D "$PGDATA" | egrep 'cluster state|Latest.*location'

# Sinxronlash usulini o'z diskingizda o'lchash
pg_test_fsync
```

Ikki sozlamani aralashtirmaslik kerak. `fsync = off` sinxronlashni butunlay o'chiradi va har qanday nosozlik ma'lumotni qaytarib bo'lmaydigan darajada buzadi. `synchronous_commit = off` esa izchil holatgacha tiklanishni kafolatlaydi va faqat eng oxirgi commit lar yo'qolishi mumkin. Birinchisi prodda ishlatilmaydi, ikkinchisi esa ongli almashtirish.

Yuqoridagi `pg_test_fsync` nima uchun kerakligi shundan kelib chiqadi. Ma'lumot diskka yetguncha operatsion tizim keshi, qurilmaning o'z keshi va RAID kontrolleri keshidan o'tadi, WAL yozuvi esa darhol ishonchli saqlanishi shart. Operatsion tizim buni ikki yo'l bilan beradi: yozuvdan keyin alohida sinxronlash buyrug'i (`fsync`, `fdatasync`) yoki faylni ochish va yozishda sinxronlik talabini ko'rsatish. Qaysi biri tezroq ekani OS va fayl tizimiga bog'liq va aynan shuni `pg_test_fsync` o'lchaydi; tanlangan usul `wal_sync_method` ga yoziladi, qolgan amallar uchun esa usulni server o'zi tanlaydi va uni sozlab bo'lmaydi (Rogov, 11.2, 186-187-bet). Batareyali RAID kontrollerida kontroller keshiga tayanish mumkin, chunki batareya elektr uzilganda ma'lumotni saqlab qoladi.

Sahifa checksum lari prodda doim yoqilgan bo'lishi kerak, lekin ularning chegaralarini bilish shart. Checksum faqat sahifa o'qilganda tekshiriladi, demak buzilish uzoq vaqt sezilmay qolishi va hamma zaxira nusxaga tushib ketishi mumkin; nolga to'ldirilgan sahifa to'g'ri hisoblanadi; va checksum faqat relation ning asosiy fork iga qo'yiladi, `pg_xact` kabi boshqa fayllar himoyalanmagan. Shuning uchun checksum zaxira nusxani muntazam tiklab sinashning o'rnini bosmaydi.

`full_page_writes` sahifa checkpoint boshlangandan keyin birinchi marta o'zgarganda uning to'liq nusxasini WAL ga yozadi va shu bilan qisman yozilgan sahifadan himoya qiladi. Narxi katta: kitobdagi `pgbench` tajribasida full page image lar hosil bo'lgan WAL hajmining taxminan 71 foizini egallagan, chunki test checkpoint dan darhol keyin boshlangan. Checkpoint lar orasida sahifa bir necha marta o'zgarsa bu nisbat kichrayadi, shuning uchun checkpoint ni siyraklashtirish va `wal_compression` ni yoqish bitta muammoning ikki yechimi.

## 21.16 Xotira tuzilmalari qulfi: spinlock, lightweight lock va wait event

Relation va qator darajasidagi og'ir qulflardan tashqari PostgreSQL umumiy xotiradagi tuzilmalarni ikki xil yengil qulf bilan himoya qiladi. Spinlock atomar protsessor buyrug'iga (masalan compare-and-swap) tayanadi, faqat eksklyuziv rejimni biladi va band resursni kutayotgan protsess sikl ichida aylanadi. Unda na deadlock aniqlash, na instrumentatsiya bor, shuning uchun uni kuzatib bo'lmaydi. Lightweight lock eksklyuziv va umumiy rejimni qo'llaydi, navbati yo'q (kutayotganlardan qaysi biri o'tishi deyarli tasodifiy), deadlock tekshiruvi ham yo'q, lekin instrumentatsiyasi bor va shuning uchun kuzatuvda ko'rinadi.

Butun qulf oilasini ikkiga ajratadigan mezon qulfning davomiyligi. Uzoq muddatli qulflar potensial uzoq vaqtga, ko'pincha tranzaksiya oxirigacha olinadi va odatda relation hamda qatorlarni himoya qiladi; ularda bir nechta rejim, navbat, deadlock aniqlash va instrumentatsiya bor, chunki bu infratuzilmaning narxi himoyalanayotgan ma'lumot ustidagi amallardan baribir arzon. Qisqa muddatli qulflar esa sekundning ulushiga olinadi, ko'pincha bir nechta protsessor buyrug'idan uzoq cho'zilmaydi va umumiy xotiradagi tuzilmalarni himoya qiladi; ularda rejim kam va instrumentatsiya umuman bo'lmasligi mumkin. Shu bo'linishda heavyweight va qator qulflari uzoq muddatli, shu bo'limda tasvirlanayotgan xotira tuzilmalari qulflari esa qisqa muddatli guruhga kiradi, predicate lock lar esa nomiga qaramay umuman qulf emas va alohida guruh hisoblanadi (Rogov, 12.1, 200-201-bet).

Ikkita amaliy misol. Buffer cache dagi hash jadvalga kirish uchun `BufferMapping` qulfi olinadi; u bitta qulf emas, 128 ta qulfdan iborat tranche, chunki bu jadvalga murojaat juda tez-tez bo'ladi va donadorlik yetishmasa u darhol bo'g'iz joyga aylanadi. WAL tomonida sahifani diskka yozishni bitta `WALWrite` qulfi serializatsiya qiladi, WAL yozuvi uchun joy band qilishni `insert position` spinlocki himoya qiladi, band qilingan joyni to'ldirish esa 8 ta qulfdan iborat `WALInsert` tranche i orqali parallel ketadi.

```sql
-- Hozirgi kutishlar. Turlari: Lock, LWLock, BufferPin, IO, Client,
-- IPC, Extension, Activity va Timeout
SELECT backend_type, wait_event_type, wait_event, count(*)
FROM pg_stat_activity
GROUP BY 1, 2, 3 ORDER BY 4 DESC;
```

`pg_stat_activity` faqat shu lahzani ko'rsatadi va tarix to'plamaydi. Tarix kerak bo'lsa `pg_wait_sampling` kengaytmasi ishlatiladi: u `shared_preload_libraries` ga qo'shiladi va sessiya bo'yicha kutish profilini yig'adi. Kitobdagi misolda standart namuna olish chastotasi sekundiga 100 marta, ya'ni `count` ustunini 100 ga bo'lsangiz kutish davomiyligini sekundda olasiz. Qisqa sessiyalar uchun bu usul ishlamaydi, chunki namuna olish statistik.

Diagnostikada ikki narsa yodda turishi kerak. Birinchisi: ko'rinishda faqat kodda nomlangan kutishlar aks etadi, qolgan vaqt hisobga olinmagan bo'lib qoladi va bu "protsess hech narsa kutmayapti" degani emas. Ikkinchisi Spring uchun muhim: HikariCP metrikasi `hikaricp.connections.pending` ni ko'rsatsa, sabab har doim pool kichikligida emas. Server tomonidagi profil `IO / WALSync` yoki `LWLock / WALWrite` ni ko'rsatsa, chegarani disk sinxronlashi qo'yadi va pool ni kattalashtirish faqat navbatni serverga ko'chiradi.

## 21.17 Vacuum fazalari: heap scan, index vacuuming va heap truncation

VACUUM bitta o'tish emas, bir nechta fazadan iborat, chunki jadval va indekslar boshqa protsesslarni bloklamasdan qayta ishlanishi kerak (Rogov, 6.3, 107-bet). Fazalarni bilish ikki amaliy savolga javob beradi: vacuum nega indekslarni bir necha marta aylanib o'tadi va u qachon faylni qisqartiradi.

- **Heap scan.** Jadval o'lik tuple qidirib skan qilinadi, visibility map da belgilangan sahifalar esa butunlay o'tkazib yuboriladi: ularda eskirgan tuple yo'qligi aniq. Gorizontdan orqada qolgan tuple larning TID i lokal xotiradagi massivga yig'iladi; massiv hajmini `maintenance_work_mem` (standart 64 MB) belgilaydi va u bir yo'la ajratiladi (Rogov, 6.3, 107-bet).
- **Index vacuuming.** Har bir indeks to'liq skan qilinadi va TID massividagi tuple larga ishora qiladigan yozuvlar olib tashlanadi. `min_parallel_index_scan_size` (standart 512 kB) dan katta indekslarni fon ishchilari parallel tozalashi mumkin: har mos indeksga bitta ishchi, bitta indeksni esa bir nechta ishchi bo'lisha olmaydi; darajani `PARALLEL N` bandi aniq belgilaydi (Rogov, 6.3, 108-bet). Bu parallellik faqat qo'lda chaqirilgan `VACUUM` da bor, autovacuum ga ruxsat etilmagan (Rogov, 6.5, 111-bet).
- **Faqat INSERT bo'ladigan jadval.** Index vacuuming fazasi free space map ni yangilaydi va vacuum statistikasini hisoblaydi, lekin qatorlar faqat qo'shilgan (o'chirilmagan va yangilanmagan) bo'lsa jadvalda o'lik tuple yo'q va bu faza butunlay o'tkazib yuboriladi; indekslar eng oxirida, alohida index cleanup fazasida bir marta skan qilinadi (Rogov, 6.3, 108-bet).
- **Heap vacuuming.** Jadval ikkinchi marta skan qilinadi, TID massividagi tuple lar va ularning pointerlari bo'shatiladi; bo'shagan joy free space map da, faqat joriy tuple qolgan sahifalar esa visibility map da aks etadi (Rogov, 6.3, 108-bet).

TID massivi heap scan tugamasdan to'lib qolsa, index vacuuming shu yerda boshlanadi, keyin heap scan to'xtagan joyidan davom etadi. Shuning uchun `pg_stat_progress_vacuum.index_vacuum_count` birdan katta bo'lishi `maintenance_work_mem` kichikligining to'g'ridan-to'g'ri alomati: har qo'shimcha aylanish barcha indekslarni boshidan o'qiydi.

```sql
-- Ketayotgan vacuum qaysi fazada va indekslarni necha marta aylangan
SELECT pid, relid::regclass, phase, index_vacuum_count,
       heap_blks_scanned, heap_blks_total
FROM pg_stat_progress_vacuum;

-- Rejali oynada: ko'proq xotira va parallel indeks tozalash
SET maintenance_work_mem = '1GB';
VACUUM (VERBOSE, PARALLEL 4) buyurtmalar;

-- Truncation qulfi xalaqit bersa, uni jadval darajasida o'chirish
ALTER TABLE buyurtmalar SET (vacuum_truncate = off);
```

**Heap truncation va "vacuum faylni qisqartirmaydi" da'vosi.** [Vacuum nima qiladi](#217-vacuum-nima-qiladi-olik-tuple-visibility-map-index-only-scan-bilan-bogliqligi) bo'limi vacuum tuple larni siqmasligini va faylni kichraytirish uchun `VACUUM FULL` kerakligini aytadi; Rogov esa oxirgi faza sifatida heap truncation ni tasvirlaydi: fayl oxirida bir nechta butunlay bo'sh sahifa to'planib qolsa, vacuum shu dumni kesib, joyni operatsion tizimga qaytaradi (Rogov, 6.3, 108-bet). Ikki da'vo zid emas, ularni ajratadigan shart bo'sh joyning fayl ichida qayerda turgani: vacuum tuple larni ko'chirmaydi, shuning uchun fayl o'rtasidagi bo'sh joy faylda qoladi va faqat fayl oxiridagi uzluksiz bo'sh dum kesiladi. Kesish ham har safar bo'lavermaydi: bo'sh dum jadvalning kamida o'n oltidan bir qismi bo'lishi yoki 1000 sahifaga yetishi kerak, bu chegaralar kodda qattiq yozilgan va sozlanmaydi; ustiga truncation qisqa `ACCESS EXCLUSIVE` qulf oladi va qulfni kutishga besh sekunddan ortiq sarflamaydi (Rogov, 6.3, 109-bet). `VACUUM FULL` esa butun faylni qayta yozadi, shuning uchun o'rtadagi bo'sh joyni ham yo'qotadi va aynan shu farq ikkala buyruqning o'z o'rnini belgilaydi.

## 21.18 Autovacuum ichida: ishchi soni, `cost_limit` bo'linishi va kuzatish

Autovacuum launcher har `autovacuum_naptime` da har bir faol baza uchun bitta ishchi ishga tushiradi, parallel ishlaydigan ishchilar soni esa `autovacuum_max_workers` (standart 3) bilan cheklangan. Ishchi o'z ro'yxatini naptime ichida tugatolmasa, launcher o'sha bazaga yana bitta ishchi qo'shadi. Muhimi: jadval darajasida parallellik yo'q, bir vaqtda faqat turli jadvallar ishlanadi (Rogov, 6.5, 110-bet).

**Ishchi sonini oshirishning o'zi tezlashtirmaydi.** Autovacuum ning ish birliklari har siklda `autovacuum_vacuum_cost_limit` bilan cheklanadi va bu chegara barcha ishchilar o'rtasida bo'linadi, shuning uchun ishchilar nechta bo'lishidan qat'i nazar tizimga tushadigan umumiy yuk taxminan o'zgarmaydi. Rogov xulosani to'g'ridan-to'g'ri aytadi: autovacuum ni tezlashtirish kerak bo'lsa `autovacuum_max_workers` va `autovacuum_vacuum_cost_limit` proportsional ravishda birga oshiriladi (Rogov, 6.6, 118-bet). [Autovacuum sozlamalari](#218-autovacuum-sozlamalari-va-u-yetishmay-qolganda-nima-boladi) bo'limidagi instans qatori shuning uchun yolg'iz kelmaydi: ishchi soni bilan birga `cost_limit` ham ko'tariladi, aks holda alohida jadval emas, butun instans o'sha eski tezlikda qoladi. Ishchi sonini oshirish bir vaqtda nechta boshqa-boshqa jadval tozalanishini oshiradi, bitta katta jadvalning tozalanish tezligini emas. Chegaraning qanchalik past ekanini kitobning o'z hisobi ko'rsatadi: standart `vacuum_cost_limit` da vacuum bir siklda eng yaxshi holatda, ya'ni hamma sahifa keshda va hech biri iflos qilinmaganda, 200 sahifani ishlaydi, eng yomon holatda esa, ya'ni hamma sahifa diskdan o'qilib iflos qilinganda, atigi to'qqiz sahifani (Rogov, 6.6, 118-bet).

```sql
-- Instans darajasi (postgresql.conf): ikkalasi birga oshiriladi
-- autovacuum_max_workers = 6
-- autovacuum_vacuum_cost_limit = 2000
-- autovacuum_work_mem = '256MB'
-- log_autovacuum_min_duration = '1s'

-- Trigger formulasi tayanadigan baho: analiz qilinmagan jadvalda -1
SELECT relname, reltuples, relpages, relallvisible,
       pg_stat_get_dead_tuples(oid) AS olik_tuple
FROM pg_class WHERE relname = 'buyurtmalar';
```

- **`autovacuum_work_mem`** (standart -1, ya'ni `maintenance_work_mem` qiymatiga tushadi) har bir ishchining TID massivi uchun ajratiladi. Har ishchi butun bo'lakni bir yo'la oladi, shuning uchun ishchi sonini oshirganda bu parametrni alohida qo'yish kerak, aks holda xotira iste'moli ishchi soniga ko'payadi (Rogov, 6.5, 111-bet).
- **`autovacuum_enabled`** va **`toast.autovacuum_enabled`** saqlash parametrlari autovacuum ni bitta jadval darajasida o'chiradi. Rogov buning nega kerak bo'lishini tasavvur qilish qiyinligini aytadi (Rogov, 6.5, 111-bet): bu parametr tajriba uchun, prod jadvali uchun emas.
- **Trigger `pg_class.reltuples` ga tayanadi.** Vacuum sharti `n_dead_tup > autovacuum_vacuum_threshold + autovacuum_vacuum_scale_factor x pg_class.reltuples` ko'rinishida yoziladi (Rogov, 6.5, 112-bet). `reltuples` esa aniq son emas, analiz va vacuum yangilab turadigan baho; hech analiz qilinmagan jadvalda u -1 bo'ladi (Rogov, 17.1, 271-272-bet). Demak statistikasi eskirgan jadvalda trigger kutilgan nuqtada emas, eski satr soniga qarab ishlaydi.
- **`log_autovacuum_min_duration`** (standart -1; 0 barcha yurishni yozadi) autovacuum ning har bir yurishini server logiga chiqaradi: indeks skanlari soni, o'chirilgan va qolgan sahifalar, o'chirilgan va qolgan tuple lar, hali olib tashlab bo'lmaydigan o'lik tuple lar, eng eski `xmin`, o'qish va yozish tezligi, bufer va WAL sarfi (Rogov, 6.7, 122-bet).

Kuzatuv mantig'i shunday: vacuum kutayotgan jadvallar ro'yxati o'sib borsa, autovacuum yuklamani uddalay olmayapti; Rogov ning yechimi uch qadamdan iborat, ya'ni `autovacuum_vacuum_cost_delay` ni kamaytirish, `autovacuum_vacuum_cost_limit` ni oshirish va ehtimol `autovacuum_max_workers` ni ham ko'tarish (Rogov, 6.7, 122-bet).

## 21.19 Freeze mexanikasi: hint bit, aggressive freezing, freeze map va CLOG

Freeze `xmin` ni o'zgartirmaydi. Tuple muzlatilgani ikkita hint bit ning birikmasi bilan belgilanadi: committed va aborted bitlari birga qo'yiladi va bu kombinatsiya "bu tuple hamma snapshotda ko'rinadi" degan ma'noni bildiradi. `xmin` esa tuple da o'z qiymati bilan qoladi, bu debug va qo'llab-quvvatlash uchun qulay (Rogov, 7.2, 124-bet). `xmax` freeze da umuman qatnashmaydi: u faqat eskirgan tuple da bo'ladi va bunday tuple gorizontdan chiqqanda vacuum uni butunlay olib tashlaydi.

Asosiy mexanizm `vacuum_freeze_min_age` emas, uning yonidagi ikkita yosh:

- **`vacuum_freeze_table_age`** (standart 150 million) vacuum ga visibility map ni e'tiborsiz qoldirishga ruxsat beradi, ya'ni har qanday sahifa muzlatilishi mumkin bo'ladi. Oddiy vacuum to'liq ko'rinadigan sahifaga kirmaydi, shuning uchun bu parametrsiz eski tuple lar muzlamay qolaveradi. Qaror jadvalning `relfrozenxid` yoshini shu chegara bilan solishtirib chiqariladi (Rogov, 7.3, 129-bet).
- **Freeze map.** Visibility map ning ikkinchi biti, ya'ni `all-frozen`, aynan shu yerda ishlaydi: u tufayli aggressive freezing da ham butun jadvalni skan qilish shart emas, faqat mapda belgilanmagan sahifalar tekshiriladi. Bundan tashqari u nosozlikka chidamlilik beradi: vacuum uzilib qolsa, keyingi yurish allaqachon ishlangan sahifalarga qaytmaydi (Rogov, 7.3, 129-bet).
- **CLOG ni autovacuum kesadi.** `autovacuum_freeze_max_age` (standart 200 million) nafaqat majburiy autovacuum ni qo'zg'aydi, balki `pg_xact` hajmini ham belgilaydi: muzlatilgan tranzaksiyalarning holatini saqlash shart emas, shuning uchun klasterdagi eng eski `datfrozenxid` dan oldingi CLOG fayllarini autovacuum olib tashlaydi (Rogov, 7.3, 132-bet). Parametrning yuqori chegarasi 2 milliard, standart qiymat esa undan o'n barobar kichik va bu ataylab shunday tanlangan: katta qiymat tuple larni o'z vaqtida muzlatib ulgurmaslik, ya'ni wraparound xavfini oshiradi (Rogov, 7.3, 131-bet). Demak bu parametrni ko'tarishning ikki narxi bor: wraparound xavfi va `pg_xact` ning o'sishi.
- **Multixact ham muzlatiladi.** Bir qatorni bir nechta tranzaksiya umumiy rejimda qulflasa, `xmax` ga alohida ID beriladigan multixact yoziladi. Multixact ID lar ham 32 bitli va ular ham o'ralishga tobe, shuning uchun eski multixact ID lar yangisi bilan (yoki qulf bitta tranzaksiyada qolgan bo'lsa oddiy XID bilan) almashtiriladi. Bu yerda `xmin` emas, aynan `xmax` muzlatiladi, chunki qatorning joriy versiyasi yangi tranzaksiyalar tomonidan qayta-qayta qulflanishi mumkin; parametrlari `vacuum_multixact_freeze_min_age`, `vacuum_multixact_freeze_table_age`, `autovacuum_multixact_freeze_max_age` va `vacuum_multixact_failsafe_age` (Rogov, 13.3, 215-bet).

```sql
-- Jadval va baza darajasidagi freeze qarzi yonma-yon
SELECT c.relname, age(c.relfrozenxid) AS xid_yoshi,
       mxid_age(c.relminmxid) AS multixact_yoshi
FROM pg_class c
WHERE c.relkind = 'r' ORDER BY 2 DESC LIMIT 10;

-- Freeze map qancha ishlaganini ko'rish
SELECT all_visible, all_frozen FROM pg_visibility_map_summary('buyurtmalar');

-- Freeze chegaralarini bitta jadvalga pasaytirish (nomlar "auto" bilan boshlanadi)
ALTER TABLE buyurtmalar SET (
  autovacuum_freeze_min_age = 10000000,
  autovacuum_freeze_table_age = 50000000
);
```

Yuqori yozuvli jadvalda eng ko'p uchraydigan kasallik shu: `age(relfrozenxid)` sekin o'sib boradi, chunki jadvalning issiq qismi doim visibility map da va vacuum uni ochmaydi; keyin `vacuum_freeze_table_age` ga yetganda birdan to'liq jadval skan qilinadi va I/O cho'qqisi paydo bo'ladi. Shuning uchun bu chegarani kichraytirib, freeze ni mayda bo'laklarga yoyish katta jadvalda bir marta katta aggressive vacuum kutishdan arzonroq.

## 21.20 Boshlang'ich yuklashda freeze: `COPY FREEZE` va `index_cleanup`

`VACUUM FREEZE` tuple larning yoshiga qaramasdan hammasini muzlatadi, ya'ni `vacuum_freeze_min_age = 0` bilan ishlagandek bo'ladi. Agar maqsad tezda muzlatish bo'lsa, failsafe rejimidagi kabi indeks tozalashni butunlay o'chirish mantiqan to'g'ri: buni `VACUUM (freeze, index_cleanup false)` buyrug'i yoki `vacuum_index_cleanup` saqlash parametri qiladi. Rogov buni muntazam qilmaslik kerakligini alohida ta'kidlaydi, chunki bunda vacuum o'zining asosiy ishini, sahifani tozalashni bajarmay qoladi (Rogov, 7.4, 133-bet).

O'zgarmaydigan ma'lumotni esa umuman keyin muzlatmaslik mumkin: uni yuklash paytining o'zida muzlatib yuboriladi. Buning uchun `COPY ... WITH FREEZE` ishlatiladi, lekin bitta qattiq shart bor: jadval shu tranzaksiyaning ichida yaratilgan yoki `TRUNCATE` qilingan bo'lishi kerak. Sabab oddiy, ikkala amal ham jadvalga eksklyuziv qulf qo'yadi va boshqa tranzaksiyalar jadvalga kira olmaydi; aks holda muzlatilgan tuple lar izolyatsiya darajasidan qat'i nazar hammaga darhol ko'rinib qolar edi (Rogov, 7.4, 133-bet).

```sql
-- Ma'lumotni darhol muzlatib yuklash: TRUNCATE va COPY bitta tranzaksiyada
BEGIN;
TRUNCATE valyuta_kurslari;
COPY valyuta_kurslari (sana, kod, kurs) FROM '/tmp/kurslar.csv' WITH (FORMAT csv, FREEZE);
COMMIT;

-- Tekshirish: sahifalar darhol freeze map ga tushgan bo'lishi kerak
SELECT all_visible, all_frozen
FROM pg_visibility_map_summary('valyuta_kurslari');
```

Yutuq ikki tomonlama: visibility map darhol yaratiladi va sahifa headerlariga ko'rinish atributi qo'yiladi, shuning uchun ma'lumot o'zgarmas ekan, jadval umuman vacuum ga tushmaydi (Rogov, 7.4, 134-bet). Ikki cheklovni yodda tutish kerak. Birinchisi, bu usul izolyatsiyani texnik jihatdan buzadi: `REPEATABLE READ` dagi tranzaksiya o'z snapshotidan keyin yuklangan qatorlarni ko'rib qolishi mumkin, Rogov buni ko'rsatib, yuklash kamdan-kam bo'lgani uchun ko'p holatda muammo tug'dirmasligini aytadi. Ikkinchisi, TOAST jadvallari qo'llab-quvvatlanmaydi: katta qiymat yuklansa, vacuum keyinchalik butun TOAST jadvalini qayta yozishga majbur bo'ladi (Rogov, 7.4, 134-bet). Java tomonida bu migratsiya va reference data yuklash uchun to'g'ridan-to'g'ri qoida beradi: `CREATE TABLE` yoki `TRUNCATE` va `COPY ... FREEZE` bitta tranzaksiyada ketsa, keyinroq bu jadval autovacuum navbatida turmaydi.

## 21.21 Checkpoint bosqichlari va `log_checkpoints` bilan kuzatish

Checkpoint bir lahzalik hodisa emas, vaqtga yoyilgan uch bosqichli jarayon va uni `checkpointer` protsessi bajaradi (Rogov, 10.3, 170-bet).

- **Boshlanish.** Checkpointer darhol yozib bo'ladigan hamma narsani diskka tushiradi: CLOG dagi tranzaksiya holati, subtransaction metadatasi va yana bir nechta tuzilma. Shu nuqta kelajakdagi tiklanishning REDO pozitsiyasi bo'lib qoladi.
- **Bajarilish.** Vaqtning asosiy qismi iflos sahifalarni yozishga ketadi. Avval checkpoint boshlanishida iflos bo'lgan barcha buferlarning headerlariga belgi qo'yiladi, bu I/O talab qilmagani uchun juda tez bo'ladi. Keyin checkpointer buferlarni aylanib, belgilanganlarini diskka yozadi; sahifalar keshdan chiqarilmaydi, shuning uchun usage va pin hisoblagichlari ahamiyatsiz. Tasodifiy yozuvdan qochish uchun sahifalar ID tartibida ishlanadi va yuk tekis tushishi uchun turli tablespace lar orasida navbatlashtiriladi. Belgilangan buferni backend ham yozib yuborishi mumkin, belgi esa shu bosqichda olib tashlanadi: har bufer checkpoint uchun faqat bir marta yoziladi. Checkpoint davomida iflos bo'lgan yangi buferlar belgilanmagani uchun ular keyingi checkpointga qoladi.
- **Tugash.** Boshlanishda iflos bo'lgan hamma bufer yozilgandan keyin checkpoint tugagan hisoblanadi va faqat shundan keyin uning boshlanish nuqtasi yangi tiklanish nuqtasi bo'ladi; undan oldingi WAL yozuvlari endi kerak emas. Checkpointer oxirida WAL ga checkpoint tugaganini bildiruvchi yozuv qo'yadi va unda checkpoint boshlangan LSN ko'rsatiladi (Rogov, 10.3, 171-bet).

```sql
-- Checkpoint sozlamasi: kitobning hisob yo'li
-- 1) ikki checkpoint orasida qancha WAL yig'ilishini o'lchang
-- 2) o'sha vaqtni checkpoint_timeout qilib qo'ying
-- 3) max_wal_size ni yuk sakraganda qo'shimcha checkpoint chaqiradigan
--    chegara sifatida tanlang
SELECT name, setting, unit FROM pg_settings
WHERE name IN ('checkpoint_timeout','checkpoint_completion_target',
               'max_wal_size','min_wal_size','checkpoint_warning',
               'log_checkpoints')
ORDER BY name;
```

Rogov ning tavsiya qilgan yo'li: avval ikki checkpoint orasida saqlanadigan WAL hajmini tanlash, uni hosil qilishga ketadigan vaqtni o'lchash va shu vaqtni `checkpoint_timeout` qilib qo'yish; standart 5 daqiqa odatda kichik va uni masalan 30 daqiqaga ko'tarish kerak bo'ladi (Rogov, 10.6, 177-bet). Tiklanish uchun kerak bo'ladigan WAL hajmi esa ikki checkpoint orasidagi hajmni `1 + checkpoint_completion_target` ga ko'paytirib baholanadi. `max_wal_size` qattiq chegara emas, faqat maqsadli qiymat: yuk sakrasa yozuv rejadan orqada qolishi mumkin, replikaga yoki arxivga ketmagan segmentlarni esa server o'chirishga haqli emas (Rogov, 10.6, 179-bet).

Kuzatuv ikki asbobdan iborat. `checkpoint_warning` (standart 30 sekund) dan tez-tez hajm bo'yicha checkpoint bo'lsa server ogohlantirish yozadi. `log_checkpoints` esa har checkpointning yozilgan bufer soni, qo'shilgan va o'chirilgan WAL fayllari, `write`, `sync` va umumiy vaqti hamda ikki checkpoint orasidagi masofasini logga chiqaradi (Rogov, 10.6, 179-180-bet). ESLATMA: kitobdagi PostgreSQL 14 da `log_checkpoints` standart holatda `off`, shuning uchun uni ataylab yoqish kerak; o'z instansingizdagi haqiqiy qiymatni yuqoridagi `pg_settings` so'rovi ko'rsatadi.

## 21.22 Background writer: `bgwriter_delay` va `bgwriter_lru_maxpages`

Backend iflos sahifani buferdan siqib chiqarishi kerak bo'lsa, uni o'zi diskka yozishga majbur bo'ladi va bu kutish degani. Shu kutishni yo'qotish uchun `bgwriter` protsessi bor. U siqib chiqarish bilan bir xil bufer qidirish algoritmiga tayanadi, lekin ikki farq bilan: o'zining alohida strelkasi bor va bu strelka siqib chiqarish strelkasidan hech qachon orqada qolmaydi, odatda esa undan o'zib ketadi; ikkinchidan, buferlarni aylanib o'tganda foydalanish hisoblagichini kamaytirmaydi (Rogov, 10.5, 176-bet).

Iflos sahifa buferi pin qilinmagan va hisoblagichi nolga teng bo'lsa diskka yoziladi. Ya'ni bgwriter siqib chiqarishdan oldinda yuradi va tez orada siqib chiqarilishi ehtimoli yuqori bo'lgan sahifalarni oldindan yozib qo'yadi; natijada siqib chiqarish uchun tanlangan buferning toza bo'lish ehtimoli oshadi.

```sql
-- bgwriter sozlamalari va u qancha ish qilayotgani
SELECT name, setting, unit FROM pg_settings
WHERE name LIKE 'bgwriter%' ORDER BY name;

-- buffers_clean bgwriter yozgan sahifalar, maxwritten_clean esa
-- bgwriter_lru_maxpages ga tegib to'xtagan yurishlar soni
SELECT buffers_clean, maxwritten_clean, buffers_alloc FROM pg_stat_bgwriter;
```

Uch parametr xulqni belgilaydi (Rogov, 10.6, 179-bet). `bgwriter_delay` (standart 200 ms) ikki yurish orasidagi pauza. Bir yurishda yoziladigan sahifa soni backendlar oldingi yurishdan beri murojaat qilgan buferlarning harakatlanuvchi o'rtachasiga asoslanadi va u `bgwriter_lru_multiplier` (standart 2) ga ko'paytiriladi. Natija qanday bo'lishidan qat'i nazar, bitta yurishda yoziladigan sahifa soni `bgwriter_lru_maxpages` (standart 100) dan oshmaydi. Iflos bufer umuman topilmasa bgwriter uxlaydi va biror backend buferga murojaat qilganda uyg'onadi.

Sozlash qoidasi amaliy: `maxwritten_clean` muntazam o'sib borsa, bgwriter har yurishda chegaraga tegib to'xtayapti, demak `bgwriter_lru_maxpages` kichik yoki `bgwriter_delay` katta. Kitobdagi `pg_stat_bgwriter` da `buffers_backend` ustuni ham bor va uning `buffers_clean` dan sezilarli katta bo'lishi yomonroq alomat: iflos sahifani asosan backendlar yozyapti, ya'ni yozuv narxi so'rov latency siga tushyapti (Rogov, 10.6, 180-bet). ESLATMA: bu ko'rinishning ustun tarkibi versiyalar orasida o'zgargan, shuning uchun o'z instansingizda avval `\d pg_stat_bgwriter` bilan tekshiring. Checkpointer va bgwriter birga sozlanadi, chunki ikkalasining vazifasi bitta, iflos buferni backend unga muhtoj bo'lgunga qadar diskka tushirish.

## 21.23 WAL segmentlari, `pg_waldump` va `wal_skip_threshold`

WAL `PGDATA/pg_wal` katalogida segment deb ataladigan alohida fayllarda yotadi. Segment hajmini faqat o'qish uchun mo'ljallangan `wal_segment_size` ko'rsatadi, standart qiymati 16 MB; uni faqat klasterni initsializatsiya qilishda o'zgartirish mumkin (`initdb --wal-segsize`) va yuqori yuklamali tizimda kattaroq segment qo'shimcha xarajatni kamaytirishi mumkin (Rogov, 10.2, 168-bet). Fayl nomining yuqori sakkiz o'n oltilik raqami timeline ni, qolgani esa LSN ning yuqori 32 bitini beradi (Rogov, 10.2, 169-bet).

Checkpointdan keyin kerak bo'lmay qolgan segmentlar o'chiriladi, lekin `min_wal_size` (standart 80 MB) gacha bo'lgan bir nechta fayl qayta ishlatish uchun nomi o'zgartirilib saqlanadi; bu doimiy fayl yaratish va o'chirish xarajatini kamaytiradi va `wal_recycle` bilan o'chiriladi (Rogov, 10.6, 178-bet). Diskda WAL uchun joy zaxiralash kerak bo'lsa `wal_keep_size` (standart 0) ishlatiladi (Rogov, 10.6, 179-bet).

```bash
# WAL ichida nima yotganini va FPI ulushini o'lchash: postgres OS useridan
pg_waldump --stats -p "$PGDATA/pg_wal" -s 0/44D4C228 -e 0/457653B0

# Tipik natija oxirgi qatori (kitobdagi pgbench o'lchovi):
# Total   119581   7831904 [76,14%]   2453755 [23,86%]
#                  ^ yozuv hajmi      ^ full page image hajmi
```

`pg_waldump` WAL yozuvlarini LSN oralig'i yoki tranzaksiya ID bo'yicha filtrlaydi va `--stats` bilan resurs menejerlari kesimida hajm beradi (Rogov, 10.2, 169-bet va 11.2, 191-bet). Bu `wal_compression` yoqish yoki `checkpoint_timeout` ni ko'tarish qarorini taxminga emas, o'lchovga bog'lab qo'yadi: FPI ulushi katta bo'lsa, ikkala qadam ham ishlaydi, chunki ular bir muammoning ikki yechimi ([Nosozlikdan tiklanish](#2115-nosozlikdan-tiklanish-startup-protsess-full-page-write-va-checksum) bo'limiga qarang).

Yana bitta WAL hajmi tugmasi `minimal` darajada. Bu darajada joriy tranzaksiyada yaratilgan yoki `TRUNCATE` qilingan relationlar ustidagi katta hajmli yozuv amallari (`CREATE TABLE AS SELECT`, `CREATE INDEX` kabi) WAL ga umuman yozilmaydi: ma'lumot to'g'ridan-to'g'ri diskka tushiriladi va katalog o'zgarishi commitdan keyin ko'rinadi. Bu optimizatsiya ishlashi uchun yangi relationga yoziladigan hajm `wal_skip_threshold` (standart 2 MB) dan oshishi kerak (Rogov, 11.3, 192-bet). Amalda bu ETL va reporting bazalari uchun real variant, lekin narxi qattiq: `minimal` da replikatsiya ham, PITR ham bo'lmaydi va `max_wal_senders = 0` qo'yish talab qilinadi, shuning uchun u asosiy OLTP instansi uchun emas, alohida hisobot klasteri uchun qarordir.

## 21.24 Klaster fayllari: `template0`, forklar va UNLOGGED jadval

Klaster initsializatsiya qilinganda `PGDATA` da uchta bir xil baza paydo bo'ladi. `template0` logical zaxiradan tiklash va boshqa kodlashli baza yaratish uchun ishlatiladi va hech qachon o'zgartirilmaydi; `template1` foydalanuvchi yaratadigan barcha bazalar uchun shablon; `postgres` esa oddiy ishchi baza (Rogov, 1.1, 20-bet). Amaliy xulosa: migratsiya skriptlari `template1` ga extension yoki jadval qo'shib qo'ysa, u keyingi har bir yangi bazaga jim ko'chadi, shuning uchun test bazasini yaratish `TEMPLATE template0` bilan ketadi.

Bitta relation diskda bitta fayl emas: u bir nechta forkdan iborat (Rogov, 1.1, 25-bet).

- **Main fork** haqiqiy ma'lumotni, ya'ni jadval yoki indeks qatorlarini saqlaydi va fayl nomi `pg_class.relfilenode` dan olinadi.
- **Free space map** (`_fsm` qo'shimchasi) sahifalar ichidagi bo'sh joyni kuzatadi va yangi qator qo'shilganda mos sahifani tez topish uchun ishlatiladi. Uning hajmi doim o'zgarib turadi: vacuumdan keyin o'sadi, yangi qator versiyalari paydo bo'lganda kichrayadi. Fayllar darhol yaratilmaydi, ular kerak bo'lganda, eng oson yo'li vacuum paytida paydo bo'ladi; tez qidirish uchun map daraxt shaklida tuzilgani sababli u kamida uchta sahifa egallaydi. Indekslar uchun ham bor, lekin u yerda faqat butunlay bo'shagan va qayta ishlatiladigan sahifalar kuzatiladi (Rogov, 1.1, 26-27-bet).
- **Visibility map** (`_vm`) har sahifa uchun ikki bit beradi va u faqat jadvallarda bo'ladi, indekslarda emas (Rogov, 1.1, 27-bet).
- **Initialization fork** (`_init`) faqat `UNLOGGED` jadvallarda va ularning indekslarida bo'ladi.

```sql
-- UNLOGGED: tez, lekin nosozlikdan keyin bo'sh qoladi va replikaga ketmaydi
CREATE UNLOGGED TABLE hisobot_vaqtinchalik (
  id    bigint PRIMARY KEY,
  hisob jsonb
);

-- Relation fayllari qayerda yotadi va forklar qanday nomlanadi
SELECT pg_relation_filepath('hisobot_vaqtinchalik');   -- base/<db oid>/<relfilenode>
SELECT pg_size_pretty(pg_relation_size('hisobot_vaqtinchalik', 'main')) AS main,
       pg_size_pretty(pg_relation_size('hisobot_vaqtinchalik', 'fsm'))  AS fsm,
       pg_size_pretty(pg_relation_size('hisobot_vaqtinchalik', 'vm'))   AS vm;
```

`UNLOGGED` jadval ustidagi hech bir amal WAL ga yozilmaydi. Bu operatsiyalarni sezilarli tezlashtiradi, lekin nosozlikdan keyin izchil ma'lumotni tiklab bo'lmaydi, shuning uchun tiklanish paytida PostgreSQL bunday obyektning barcha forklarini o'chiradi va main forkni initialization fork bilan qayta yozadi, ya'ni jadval bo'sh qoladi (Rogov, 1.1, 26-bet). Arxitektor uchun chegara shundan kelib chiqadi: WAL ga yozilmagani uchun bunday jadval streaming replikaga ham ketmaydi va replikada o'qib bo'lmaydi. Demak `UNLOGGED` import uchun staging jadvali, qayta hisoblanadigan material va sessiya tashqarisidagi vaqtinchalik natija uchun to'g'ri, lekin biznes ma'lumoti yoki idempotentlik kaliti uchun emas.

## 21.25 Amalda qo'llash

- [ ] `pg_stat_activity` dan `idle in transaction` sessionlarini sanab chiqing va `idle_in_transaction_session_timeout` ni 30 sekundga qo'ying.
- [ ] HikariCP `maximum-pool-size` ni barcha instanslar bo'yicha qo'shib, PostgreSQL yadro sonining 2-4 barobaridan oshmasligini tekshiring.
- [ ] `pg_stat_checkpointer` (yoki 16 va pastda `pg_stat_bgwriter`) dagi `num_requested` ni o'lchab, nolga yaqin bo'lmasa `checkpoint_timeout` va `max_wal_size` ni kattalashtiring.
- [ ] Eng katta uchta jadvalga individual `autovacuum_vacuum_scale_factor = 0.02` va `autovacuum_vacuum_cost_delay = 0` qo'yib, o'lik tuple nisbatini bir hafta kuzating.
- [ ] `age(datfrozenxid)` uchun monitoringga alert qo'shing: 500 million da ogohlantirish, 1 milliardda jiddiy hodisa.
- [ ] Index-only scan kutilgan so'rovlarda `EXPLAIN (ANALYZE, BUFFERS)` dagi `Heap Fetches` ni tekshirib, `pg_visibility_map_summary` bilan vacuum qarzini tasdiqlang.
- [ ] `pgstattuple_approx` bilan top 10 jadvalning bloat foizini o'lchab, 30 foizdan oshganlar uchun `pg_repack` yoki partitioning rejasini yozing.
- [ ] Katta JSONB yoki matn ustunlari uchun `pg_column_size` ni o'lchab, `lz4` siqish va lazy fetch ni joriy qiling.
- [ ] `autovacuum_max_workers` ni oshirgan bo'lsangiz, `autovacuum_vacuum_cost_limit` ni ham shu nisbatda oshirganingizni tekshiring: chegara ishchilar orasida bo'linadi.
- [ ] `log_checkpoints` yoqilganini tasdiqlab, logdagi `distance` va `write` vaqtini bir hafta kuzating; `maxwritten_clean` o'sib borsa `bgwriter_lru_maxpages` ni ko'taring.
- [ ] O'zgarmas reference data va migratsiya yuklamalarini `TRUNCATE` va `COPY ... FREEZE` bilan bitta tranzaksiyada yuklab, bu jadvallarni autovacuum navbatidan chiqaring.

## Manbalar

- [PostgreSQL, Resource consumption: `huge_pages`](https://www.postgresql.org/docs/current/runtime-config-resource.html#GUC-HUGE-PAGES) - "Valid values are `try` (the default), `on`, and `off`"; `on` da huge page olinmasa server ishga tushmaydi; faqat Linux va Windows
- [PostgreSQL, Linux Huge Pages](https://www.postgresql.org/docs/current/kernel-resources.html#LINUX-HUGE-PAGES) - `shared_memory_size_in_huge_pages` va `vm.nr_hugepages` bilan hovuzni sozlash
- [postgres, `guc.c` (REL_15_STABLE)](https://raw.githubusercontent.com/postgres/postgres/REL_15_STABLE/src/backend/utils/misc/guc.c) - `huge_pages` `PGC_POSTMASTER`, standarti `HUGE_PAGES_TRY`
- [postgres, `system_views.sql`](https://raw.githubusercontent.com/postgres/postgres/REL_16_STABLE/src/backend/catalog/system_views.sql) - `pg_stat_io` 16 da bor, 15 da yo'q
- [PostgreSQL 17, WAL (wal.sgml)](https://raw.githubusercontent.com/postgres/postgres/REL_17_STABLE/doc/src/sgml/wal.sgml) - WAL, checkpoint va fsync xatti-harakati
- [PostgreSQL 17, Routine Maintenance (maintenance.sgml)](https://raw.githubusercontent.com/postgres/postgres/REL_17_STABLE/doc/src/sgml/maintenance.sgml) - vacuum, analyze va tranzaksiya id aylanishi
- Egor Rogov, *PostgreSQL 14 Internals*, Postgres Professional, 2022, 9-bob "Buffer Cache", 147-163-betlar - bufer headeri, clock sweep, buffer ring strategiyalari, `pg_prewarm` va lokal kesh
- Egor Rogov, *PostgreSQL 14 Internals*, Postgres Professional, 2022, 5-bob "Page Pruning and HOT Updates", 92-101-betlar - page pruning sharti, `redirect` pointer, HOT zanjirining uzilishi, bottom-up index deletion
- Egor Rogov, *PostgreSQL 14 Internals*, Postgres Professional, 2022, 3-bob "Pages and Tuples", 70-79-betlar - `pg_xact` ikki biti, hint bit, virtual transaction, savepoint va subtransaction
- Egor Rogov, *PostgreSQL 14 Internals*, Postgres Professional, 2022, 10-bob "Write-Ahead Log" 173-176-betlar va 11-bob "WAL Modes" 185-191-betlar - startup protsess, `pg_control`, roll-back bosqichining yo'qligi, checksum chegaralari, full page write ulushi
- Egor Rogov, *PostgreSQL 14 Internals*, Postgres Professional, 2022, 15-bob "Locks on Memory Structures", 240-247-betlar - spinlock va lightweight lock farqi, `BufferMapping` va `WALInsert` tranche lari, wait event turlari, `pg_wait_sampling`
- Egor Rogov, *PostgreSQL 14 Internals*, Postgres Professional, 2022, 1.1-bo'lim (20, 25-27-betlar) - `template0` va `template1` vazifasi, main, free space map va visibility map forklari, initialization fork va `UNLOGGED` jadvalning tiklanishda bo'shashi
- Egor Rogov, *PostgreSQL 14 Internals*, Postgres Professional, 2022, 3.7-bo'lim (78-79-betlar) - xatodan keyin tranzaksiyaning abort holatiga o'tishi, `COMMIT` ning `ROLLBACK` qaytarishi va `ON_ERROR_ROLLBACK` dagi savepoint narxi
- Egor Rogov, *PostgreSQL 14 Internals*, Postgres Professional, 2022, 6.3-bo'lim (107-109-betlar) - vacuum fazalari, TID massivi va `maintenance_work_mem`, `min_parallel_index_scan_size`, insert-only jadvalda index cleanup, heap truncation sharti va `vacuum_truncate`
- Egor Rogov, *PostgreSQL 14 Internals*, Postgres Professional, 2022, 6.5-bo'lim (110-113-betlar) - autovacuum ishchilari va jadval darajasida parallellik yo'qligi, `autovacuum_work_mem`, `autovacuum_enabled`, vacuum trigger formulasi
- Egor Rogov, *PostgreSQL 14 Internals*, Postgres Professional, 2022, 6.6-bo'lim (118-bet) - `autovacuum_vacuum_cost_limit` barcha ishchilar orasida bo'linishi va uni `autovacuum_max_workers` bilan proportsional oshirish talabi
- Egor Rogov, *PostgreSQL 14 Internals*, Postgres Professional, 2022, 6.7-bo'lim (122-bet) - `log_autovacuum_min_duration` va log qatorining tarkibi, autovacuum yetishmaganda uch qadamli yechim
- Egor Rogov, *PostgreSQL 14 Internals*, Postgres Professional, 2022, 7.2-7.3-bo'limlar (124-132-betlar) - freeze ikki hint bitning birikmasi ekani va `xmin` o'zgarmasligi, `vacuum_freeze_table_age` (150 million), freeze map, `autovacuum_freeze_max_age` va CLOG ni autovacuum kesishi
- Egor Rogov, *PostgreSQL 14 Internals*, Postgres Professional, 2022, 7.4-bo'lim (133-134-betlar) - `VACUUM (freeze, index_cleanup false)` va `vacuum_index_cleanup`, `COPY FREEZE` sharti, visibility map ning darhol yaratilishi va TOAST cheklovi
- Egor Rogov, *PostgreSQL 14 Internals*, Postgres Professional, 2022, 8.2-bo'lim (140-bet) - `CLUSTER` ning indeks tartibida qayta yozishi, tartib saqlanmasligi va `VACUUM FULL` ning uning maxsus holati ekani
- Egor Rogov, *PostgreSQL 14 Internals*, Postgres Professional, 2022, 9.4-9.5-bo'limlar (154, 156-betlar) - `track_io_timing` standart holatda o'chiqligi, ikkinchi skanning mavjud buffer ring ga qo'shilishi
- Egor Rogov, *PostgreSQL 14 Internals*, Postgres Professional, 2022, 10.2-10.3-bo'limlar (168-171-betlar) - `wal_segment_size` 16 MB va uni faqat `initdb` da o'zgartirish, `pg_waldump` filtrlari, checkpointning boshlanish, bajarilish va tugash bosqichlari
- Egor Rogov, *PostgreSQL 14 Internals*, Postgres Professional, 2022, 10.5-10.6-bo'limlar (176-180-betlar) - bgwriter algoritmi va alohida strelkasi, `bgwriter_delay` (200 ms), `bgwriter_lru_multiplier` (2) va `bgwriter_lru_maxpages` (100), `checkpoint_timeout` ni o'lchov bilan tanlash, `min_wal_size`, `wal_keep_size`, `checkpoint_warning` va `log_checkpoints`
- Egor Rogov, *PostgreSQL 14 Internals*, Postgres Professional, 2022, 11.1-bo'lim (183-bet) - `commit_delay` va `commit_siblings` bilan commitlarni paketlash
- Egor Rogov, *PostgreSQL 14 Internals*, Postgres Professional, 2022, 11.2-11.3-bo'limlar (186-192-betlar) - `pg_test_fsync` va `wal_sync_method`, `pg_waldump --stats` dagi full page image ulushi, `minimal` darajada ommaviy amallarning WAL ga yozilmasligi va `wal_skip_threshold`
- Egor Rogov, *PostgreSQL 14 Internals*, Postgres Professional, 2022, 12.1-bo'lim (200-201-betlar) - uzoq va qisqa muddatli qulflar taksonomiyasi va predicate lock larning alohida guruhi
- Egor Rogov, *PostgreSQL 14 Internals*, Postgres Professional, 2022, 13.3-bo'lim (215-bet) - multixact ID larining o'ralishi, `xmax` ning muzlatilishi va `vacuum_multixact_*` parametrlari
- Egor Rogov, *PostgreSQL 14 Internals*, Postgres Professional, 2022, 17.1-bo'lim (271-272-betlar) - `reltuples`, `relpages` va `relallvisible` ning baho ekani, analiz qilinmagan jadvalda `reltuples = -1`

---

[&larr; 20. Spring Security: filter chain, OAuth2, JWT](20-spring-security-filter-chain-oauth2-jwt.md) · [Mundarija](README.md) · [22. MVCC, izolyatsiya darajalari, lock va deadlock &rarr;](22-mvcc-izolyatsiya-darajalari-lock-va-deadlock.md)
