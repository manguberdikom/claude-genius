<!-- doc: architect | chapter: 24 | part: IV. PostgreSQL chuqur bilim -->

[Barcha hujjatlar](../../README.md) / [Arxitektor miyasi](README.md)

> Holat: tekshirilgan (2026-10-19). Manbalar bob oxirida.

# 24. Planner, statistika va EXPLAIN ANALYZE o'qish (Planner and EXPLAIN ANALYZE)

<details>
<summary>Bu bobdagi 28 bo'lim</summary>

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
- [24.13 Join tartibini boshqarish: `join_collapse_limit`, `from_collapse_limit` va genetik optimizator](#2413-join-tartibini-boshqarish-join_collapse_limit-from_collapse_limit-va-genetik-optimizator)
- [24.14 `Memoize`: parametrlashtirilgan nested loop uchun qator keshi](#2414-memoize-parametrlashtirilgan-nested-loop-uchun-qator-keshi)
- [24.15 `Sort` node ichida: quicksort, top-N heapsort, external merge va incremental sort](#2415-sort-node-ichida-quicksort-top-n-heapsort-external-merge-va-incremental-sort)
- [24.16 Parallel reja: `Gather`, ishchi soni formulasi va parallellashmaydigan so'rovlar](#2416-parallel-reja-gather-ishchi-soni-formulasi-va-parallellashmaydigan-sorovlar)
- [24.17 Asosiy statistika va `pg_stats`: `reltuples`, `n_distinct`, `null_frac`, `avg_width`](#2417-asosiy-statistika-va-pg_stats-reltuples-n_distinct-null_frac-avg_width)
- [24.18 `most_common_vals` va `histogram_bounds` dan selektivlik qanday chiqadi](#2418-most_common_vals-va-histogram_bounds-dan-selektivlik-qanday-chiqadi)
- [24.19 Narx formulasi: seq scan, index scan va bitmap scan nimadan yig'iladi](#2419-narx-formulasi-seq-scan-index-scan-va-bitmap-scan-nimadan-yigiladi)
- [24.20 Join turlari: inner, outer, semi, anti va dekart ko'paytma](#2420-join-turlari-inner-outer-semi-anti-va-dekart-kopaytma)
- [24.21 `HashAggregate` va `GroupAggregate`: `DISTINCT` va `GROUP BY` ni bajarishning ikki yo'li](#2421-hashaggregate-va-groupaggregate-distinct-va-group-by-ni-bajarishning-ikki-yoli)
- [24.22 Kengaytirilgan so'rov protokoli: tayyorlash, parametr bog'lash va natijani bo'laklab olish](#2422-kengaytirilgan-sorov-protokoli-tayyorlash-parametr-boglash-va-natijani-bolaklab-olish)
- [24.23 Parallel narx: `parallel_setup_cost`, `parallel_tuple_cost` va `Parallel Seq Scan`](#2423-parallel-narx-parallel_setup_cost-parallel_tuple_cost-va-parallel-seq-scan)
- [24.24 Parallel restricted: faqat lider bajaradigan qism va `force_parallel_mode`](#2424-parallel-restricted-faqat-lider-bajaradigan-qism-va-force_parallel_mode)
- [24.25 Parallel skan tugunlari: index, index-only va bitmap](#2425-parallel-skan-tugunlari-index-index-only-va-bitmap)
- [24.26 Parallel join va `Gather Merge`: tartibni saqlab yig'ish](#2426-parallel-join-va-gather-merge-tartibni-saqlab-yigish)
- [24.27 `WITH RECURSIVE`: o'zgaruvchan chuqurlikdagi ierarxiya va graf yurish](#2427-with-recursive-ozgaruvchan-chuqurlikdagi-ierarxiya-va-graf-yurish)
- [24.28 Amalda qo'llash](#2428-amalda-qollash)

</details>



PostgreSQL planner so'rovni qanday bajarishni o'zi tanlaydi va bu tanlov statistikaga asoslangan taxminlar ustiga qurilgan. Arxitektor uchun muhim narsa index qo'shish emas, balki planner nimaga ishonib shu rejani tanlaganini o'qib tushunish. `EXPLAIN (ANALYZE, BUFFERS)` chiqishi aynan shu ishonchni va haqiqatni yonma-yon ko'rsatadigan yagona vosita. Bu bobda planner mexanikasi, narx modeli, skan va join turlari, hamda sekin so'rovni tartib bilan tekshirish usuli ko'rib chiqiladi.

## 24.1 Planner nima qiladi: variantlar, narx modeli, tanlov

Parser SQL matnini daraxtga aylantiradi, rewriter view va rule'larni ochadi, keyin planner ishga tushadi. Planner bir xil natijani beradigan ko'plab jismoniy rejalarni generatsiya qiladi: har bir jadval uchun skan usuli, har bir juftlik uchun join algoritmi, join tartibi, agregatsiya va sort joyi. Har bir variantga narx beriladi va eng arzoni tanlanadi.

Narx birligi sekund emas, shartli son. Bazasi `seq_page_cost = 1.0`, ya'ni ketma-ket o'qilgan bitta 8 kB sahifa narxi. Qolgan hamma parametr shunga nisbatan o'lchanadi. Narx ikki qismdan: `startup cost` (birinchi qator chiqishidan oldingi ish) va `total cost` (barcha qatorlar). `LIMIT` bo'lsa planner total narxning faqat bir ulushini hisoblaydi, shuning uchun `LIMIT 20` bilan va `LIMIT` siz rejalar butunlay boshqacha bo'lishi mumkin.

Join tartibi uchun bir darajadagi element soni `geqo_threshold` (standart 12) dan oshsa, to'liq dinamik programmalash o'rniga genetik algoritm ishlaydi va reja barqaror bo'lmay qoladi. 12 ta jadvalli hisobot so'rovi har deploy'dan keyin boshqa reja olishi mumkin, bu esa "kecha ishlagan, bugun ishlamaydi" muammosining tipik manbasi. Bundan oldin `from_collapse_limit` va `join_collapse_limit` (ikkalasi ham standart 8) so'rov daraxtini yassilaydi, ya'ni genetik algoritmga tushadigan element soni shu ikki chegaradan keyin hisoblanadi. Arxitektor qarori: katta hisobotni bir nechta bosqichga bo'lish yoki oldindan hisoblangan jadvaldan o'qish.

Planner ga shu erkinlik qayerdan kelganini bir jumlada aytish mumkin va undan amaliy qoida chiqadi. Kleppmann deklarativ so'rov tilining asosiy afzalligini shunday beradi: u baza dvigatelining implementatsiya tafsilotlarini yashiradi, shuning uchun baza so'rovlarni o'zgartirmasdan unumdorlikni yaxshilashi mumkin. Misoli esa aniq shu bobga tegishli: imperativ kodda natijalar ro'yxati ma'lum tartibda keladi, va agar baza ishlatilmayotgan disk joyini qaytarish uchun yozuvlarni joyidan ko'chirishi kerak bo'lsa, qatorlarning chiqish tartibi o'zgaradi; SQL misoli hech qanday tartibni kafolatlamagani uchun bunga qarshilik qilmaydi, imperativ kod bo'lsa esa baza kod tartibga tayanayotganini hech qachon bila olmaydi (2-bob, 43-bet).

Amaliy natija qat'iy: `ORDER BY` yozilmagan so'rovning tartibi tasodifiy va u reja o'zgarganda o'zgaradi. Bu bobdagi hamma mexanizm shu o'zgarishni keltirib chiqaradi: indeks skanidan sequential skanga o'tish, parallel reja yoqilishi, `geqo` ning boshqa join tartibini tanlashi, hatto `VACUUM` dan keyin qatorlarning sahifa ichida joyi o'zgarishi. Shuning uchun tartib kerak bo'lgan har joyda `ORDER BY` yoziladi, va sahifalash uchun u yetarli emas: barqaror tartib uchun unique ustun ham kalitga qo'shilishi kerak ([code-review 20.5](../code-review/20-web-qatlami-review-dto-validatsiya-xato.md#205-pagination-va-chegarasiz-royxatlar) sahifalashdagi barqaror tartibni beradi, bu yerda esa qoidaning umumiy shakli).

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

`effective_cache_size` hech qanday xotira ajratmaydi, u faqat planner'ga "operatsion tizim page cache va shared_buffers birgalikda taxminan shuncha ma'lumotni ushlab turadi" deb aytadi. Qo'llanmadagi default qiymat 4 GB va u hech narsa ajratmaydi; RAM ning 75 foizi degan raqam esa qo'llanmada yo'q, u jamoa amaliyotidan kelgan boshlang'ich taxmin. Qiymati kichik bo'lsa planner index scan'da har safar diskka borishni taxmin qiladi va uni qimmat deb baholaydi.

```sql
-- 64 GB RAM li SSD serveri uchun tipik boshlang'ich qiymatlar
ALTER SYSTEM SET random_page_cost = 1.1;        -- SSD uchun
ALTER SYSTEM SET effective_cache_size = '48GB'; -- RAM ning ~75%, o'lchanmagan taxmin
ALTER SYSTEM SET effective_io_concurrency = 200;-- NVMe uchun
ALTER SYSTEM SET work_mem = '32MB';             -- har bir sort/hash uchun
SELECT pg_reload_conf();

-- Bitta so'rovni sinash uchun sessiya darajasida
SET LOCAL random_page_cost = 1.1;
EXPLAIN (ANALYZE, BUFFERS) SELECT ...;
```

`work_mem` eng xavfli parametr. U har bir sort, hash va hashagg uchun alohida ajratiladi, demak bitta so'rov 5 ta hash node bilan 5 * work_mem gacha xotira olishi mumkin. 200 ulanishli pool'da global 256MB qo'yish OOM ga olib keladi. Arxitektor yondashuvi: global 32MB, hisobot so'rovidan oldin `SET LOCAL work_mem = '256MB'`.

## 24.4 Skan turlari: sequential, index, index-only, bitmap heap scan

Sequential scan butun jadvalni ketma-ket o'qiydi. Jadval kichik bo'lsa yoki natijaga qatorlarning katta ulushi tushsa, bu eng arzon usul. Aniq chegara yo'q: kitob skan usullarining narxini selektivlikka qarab egri chiziq shaklida beradi va raqam ko'rsatmaydi. Seq scan narxi selektivlikka umuman bog'liq emas, qolgan usullarniki esa selektivlik oshgani sari o'sadi, shuning uchun ma'lum bir ulushdan keyin seq scan ustun chiqadi (Rogov, 20.5, 348-349-bet). Chegara qayerda yotishi korrelyatsiyaga, `effective_cache_size` ga va index-only scan mumkinligiga bog'liq: korrelyatsiya ideal bo'lsa index scan juda katta ulushda ham arzon qoladi, korrelyatsiya past bo'lsa u tez orada seq scan dan qimmatlashadi (Rogov, 20.5, 349-bet). Seq scan rejada ko'rinishi avtomatik muammo degani emas.

Index scan indeksni aylanib, har bir topilgan qator uchun heap'ga boradi. Tanlovchanlik yuqori bo'lganda (masalan `order_id = ?`) ideal. Index-only scan heap'ga bormaydi, chunki kerakli hamma ustun indeksda bor va sahifa visibility map'da "butunlay ko'rinadigan" deb belgilangan. `VACUUM` ishlamasa visibility map eskiradi va index-only scan ham heap fetch qilishga tushadi.

Bitmap heap scan ikki bosqichli: avval indeksdan mos qatorlarning sahifa bitmap'i quriladi, keyin heap jismoniy tartibda o'qiladi. Bu bir necha ming qator qaytaradigan so'rovlar uchun eng samarali usul, chunki tasodifiy o'qish ketma-ket o'qishga aylanadi. `Heap Blocks: exact=... lossy=...` satrida `lossy` ko'rinsa, bitmap `work_mem` ga sig'magan va sahifa darajasiga qo'pollashgan, natijada ortiqcha qator filtrlanadi.

Bitmap ning yana bir xossasi bor: uni mantiqiy amal bilan birlashtirish mumkin. Bir nechta indeksdan qurilgan bitmap lar `BitmapAnd` node ida kesishtiriladi va `BitmapOr` node ida birlashtiriladi, shuning uchun `WHERE status = ? AND kanal = ?` shartiga ikki alohida bitta ustunli indeks ham yetishi mumkin. Rejada shu node larni ko'rish amaliy signal: ko'p ustunli indeks qo'shishdan oldin planner mavjud indekslarni allaqachon birga ishlatayotganini tekshirish kerak.

## 24.5 Join algoritmlari: nested loop, hash join, merge join va qachon qaysi biri tanlanadi

Nested loop tashqi qatorning har biri uchun ichki tomonni qayta izlaydi. Ichki tomonda index bo'lsa va tashqi tomon kichik bo'lsa, bu eng tez va eng kam xotira talab qiladigan usul. Xatar: tashqi qator soni noto'g'ri taxmin qilinsa, 50 ta `loops` o'rniga 500000 ta `loops` bo'ladi va so'rov 1000 baravar sekinlashadi. Deyarli barcha "kutilmaganda sekinlashgan so'rov" hodisasi shu.

Hash join kichik tomondan xotirada hash jadval quradi, keyin katta tomonni bir marta o'tadi. Katta to'plamlarni tenglik shartida birlashtirish uchun eng yaxshi tanlov. Hash `work_mem` ga sig'masa `Batches` soni 1 dan oshadi va diskka to'kiladi, bu esa `temp read/written` bloklarida ko'rinadi.

Merge join ikki tomonni sortlangan holda parallel o'qiydi. Ikkala tomonda ham mos indeks bo'lsa yoki ma'lumot allaqachon sortlangan bo'lsa arzon, aks holda sort narxi qo'shiladi. Katta hisobotlarda `ORDER BY` bilan birga foydali.

Merge join ning qattiq sharti bor: uning merge shartida faqat tenglik operatori ishlatiladi, ya'ni u faqat equi-join ni biladi (Rogov, 23.1, 388-bet). Shuning uchun `BETWEEN` yoki boshqa oraliq sharti merge join ni o'zi hosil qila olmaydi; u faqat tenglik sharti yonida, qo'shimcha `Join Filter` bo'lib keladi. Tenglik sharti umuman bo'lmasa qoladigan yagona usul nested loop, chunki faqat u ixtiyoriy shart bilan ishlay oladi (Rogov, 21.2, 365-bet).

| Holat | Planner tanlovi | Nega |
| --- | --- | --- |
| Tashqi tomon 10 qator, ichkida index | Nested loop | Har bir qidiruv arzon, startup cost nol |
| 2 mln va 500 ming qator, tenglik sharti | Hash join | Bitta o'tish, xotirada hash |
| Ikkala tomon sortlangan, `ORDER BY` bor | Merge join | Sort qayta kerak emas |
| Faqat `BETWEEN`, tenglik sharti yo'q | Nested loop | Hash ham, merge ham faqat tenglikni biladi |
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
| Seq scan ko'rsa darhol muammo deb biladi | Tanlovchanlik va korrelyatsiyani tekshiradi, katta ulushda seq scan to'g'ri |
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

Ustun statistikasi faqat taqqoslashning bir tomoni ustunning o'zi bo'lganda ishlaydi. Ustun ustida funksiya chaqirilsa planner uning semantikasini bilmaydi va `funksiya(ustun) = konstanta` shakli uchun selektivlikni har doim 0.5 foiz deb oladi (Rogov, 17.9, 285-bet). PostgreSQL 14 da buning ikki yechimi bor va ikkalasi ham statistikani ifoda ustida yig'adi.

```sql
-- 1-yo'l: ifoda ustida kengaytirilgan statistika
CREATE STATISTICS stat_orders_oy ON (extract(month FROM created_at)) FROM orders;
ANALYZE orders;

-- Yig'ilgan qiymatlar alohida ko'rinishda o'qiladi
SELECT left(expr, 40) AS expr, null_frac, n_distinct, most_common_vals
FROM pg_stats_ext_exprs WHERE statistics_name = 'stat_orders_oy';

-- Statistika obyektining hajmini alohida sozlash
ALTER STATISTICS stat_orders_oy SET STATISTICS 500;

-- 2-yo'l: ifoda indeksi. Statistika indeks bilan birga avtomatik keladi
CREATE INDEX orders_oy_idx ON orders (extract(month FROM created_at));
ANALYZE orders;
```

Tanlov oddiy. Indeks baribir kerak bo'lsa ifoda indeksi olinadi, chunki u statistikani tekin olib keladi. Indeks kerak emas, faqat taxmin to'g'rilanishi kerak bo'lsa `CREATE STATISTICS` arzonroq, chunki u `INSERT` narxini va WAL hajmini oshirmaydi. Bitta shart ikkalasiga ham tegishli: yig'ilgan statistika ishlashi uchun so'rovdagi ifoda `CREATE STATISTICS` yoki indeksda yozilgani bilan AYNAN bir xil shaklda bo'lishi kerak (Rogov, 17.9, 286-bet).

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

## 24.13 Join tartibini boshqarish: `join_collapse_limit`, `from_collapse_limit` va genetik optimizator

Join tartibi variantlari soni jadval soniga qarab portlaydi, shuning uchun planner avval parse daraxtini yassilaydi: har bir `JOIN` tuguni o'z elementlarining tekis ro'yxati bilan almashtiriladi va shundan keyin hamma juftlik ko'rib chiqiladi. Yassilash faqat natija ro'yxatida `join_collapse_limit` dan ko'p element bo'lmasa bajariladi.

Buning amaliy ma'nosi aniq. `FROM a, b JOIN c ON ..., d, e` yozilganda limit yetarli bo'lsa planner tartibni o'zi tanlaydi; limit kichik bo'lsa `JOIN` tuguni ochilmaydi va `b` bilan `c` majburan birinchi birlashtiriladi, qolganlari esa shu natija bilan ixtiyoriy tartibda qo'shiladi. `join_collapse_limit = 1` qo'yilsa, `JOIN` bilan yozilgan tartib butunlay saqlanadi. `FULL OUTER JOIN` esa limit qiymatidan qat'i nazar hech qachon yassilanmaydi. Pastki so'rovlar uchun xuddi shu vazifani `from_collapse_limit` bajaradi, chunki parse daraxti darajasida pastki so'rov ham shunday tugun bo'lib ko'rinadi.

```sql
-- Reja tuzish vaqti ijro vaqtiga yaqinlashsa: tartibni qo'lda belgilash
SET LOCAL join_collapse_limit = 1;
SET LOCAL from_collapse_limit = 1;

-- Reja tuzish vaqtini alohida o'lchash
EXPLAIN (ANALYZE, SUMMARY ON) SELECT ...;
```

Yassilashdan keyin bitta darajada juda ko'p element qolsa, planner genetik algoritmga o'tadi: `geqo` yoqilgan va element soni `geqo_threshold` dan oshganda. Genetik algoritm dinamik programmalashdan ancha tez, lekin topilgan reja optimal ekanini kafolatlamaydi. Shuning uchun amaliy maqsad undan qochish, ya'ni optimallashtiriladigan element sonini kamaytirish.

Kitob buning uch yo'lini sanaydi va uchalasi ham qidiruv doirasini toraytirish hisobiga ishlaydi: CTE ni `MATERIALIZED` deb e'lon qilish (shunda u asosiy so'rovdan alohida optimallashtiriladi), so'rovni SQL bo'lmagan funksiya ichiga olish (SQL funksiyalari ba'zan asosiy so'rovga singdiriladi, shuning uchun ular kafolat bermaydi) va yuqoridagi ikki limit.

Spring Data JPA da bu muammo ikki joyda chiqadi. Birinchisi: `@EntityGraph` yoki bir nechta `JOIN FETCH` bilan yozilgan so'rov Hibernate tomonidan o'nlab jadvalli bitta SQL ga aylanadi va planner genetik algoritmga tushadi; natijada bir xil so'rov har safar boshqa reja olishi mumkin. Ikkinchisi: Criteria API bilan dinamik qurilgan so'rovda jadval soni foydalanuvchi filtriga qarab o'zgaradi, shuning uchun regressiya faqat ayrim filtr kombinatsiyalarida ko'rinadi. Ikkala holatda ham yechim bitta: fetch grafini kichraytirish yoki so'rovni ikki bosqichga bo'lish.

## 24.14 `Memoize`: parametrlashtirilgan nested loop uchun qator keshi

PostgreSQL 14 da yangi reja node i paydo bo'ldi: `Memoize`. U parametrlashtirilgan nested loop da ichki tomon bir xil parametr qiymati bilan qayta-qayta skanlanayotganini ko'rsa, natijani keshlab qo'yadi. `Materialize` dan ikki farqi bor: `Materialize` farzand node ning hamma qatorini bir butun qilib saqlaydi, `Memoize` esa har bir parametr qiymati uchun alohida saqlaydi; va `Materialize` joy yetmaganda diskka to'kiladi, `Memoize` esa faqat xotirada ishlaydi, chunki aks holda keshlashning ma'nosi qolmaydi.

Kesh uchun ajratiladigan xotira `work_mem` va `hash_mem_multiplier` ko'paytmasiga teng. Kalitlar ro'yxat bo'lib bog'lanadi: ro'yxatning bir uchi sovuq (uzoq ishlatilmagan kalitlar), ikkinchisi issiq, va joy kerak bo'lganda sovuq uchidagi qatorlar chiqarib yuboriladi. Bitta parametr qiymatiga juda ko'p qator to'g'ri kelsa va ular xotiraga sig'masa, shu parametr umuman keshlanmaydi: qatorlarning bir qismini saqlashning foydasi yo'q.

```text
-> Memoize (actual rows=1 loops=113)
     Cache Key: f.aircraft_code
     Cache Mode: logical
     Hits: 112  Misses: 1  Evictions: 0  Overflows: 0  Memory Usage: 1kB
```

Rejani o'qishda to'rtta son muhim. `Hits` va `Misses` keshning foydasini ko'rsatadi. `Evictions` va `Overflows` nolga yaqin bo'lmasa, ajratilgan kesh kichik; bu odatda alohida parametr qiymatlari sonining noto'g'ri baholanishidan kelib chiqadi va shunda `Memoize` foyda emas, qo'shimcha narx beradi. Node ning rejadagi narxi ham aldamchi: u farzand node narxiga `cpu_tuple_cost` qo'shilgani, ya'ni keshning haqiqiy narxini aks ettirmaydi.

Java tomonida `Memoize` eng ko'p [n+1 so'rov muammosi](18-spring-data-jpa-va-hibernate-chuqur.md#184-n1-sorov-muammosi-topish-usuli-va-tort-xil-yechim) shaklida uchraydi. Hibernate `JOIN FETCH` siz lug'at entity ni (valyuta, status, shahar) har qator uchun qayta so'raganda SQL darajasida parametrlashtirilgan nested loop hosil bo'ladi va `Memoize` uni yumshatadi. Lekin bu yechim emas, faqat yumshatish: rejada `Memoize` ko'rinishi "bu yerda takrorlanuvchi qidiruv bor" degan signal va to'g'ri javob so'rovni `JOIN` yoki `@EntityGraph` bilan qayta yozish. Node ning hissasini o'lchash uchun uni `enable_memoize = off` bilan o'chirib, ikki rejani taqqoslash mumkin.

## 24.15 `Sort` node ichida: quicksort, top-N heapsort, external merge va incremental sort

`Sort` node rejada bitta satr bo'lib ko'rinadi, lekin uning ichida to'rt xil algoritm bo'lishi mumkin va `EXPLAIN ANALYZE` qaysi biri ishlaganini `Sort Method` satrida aytadi.

Ma'lumot `work_mem` ga sig'sa quicksort ishlaydi va `Memory: NkB` ko'rsatiladi. `LIMIT` bo'lsa to'liq saralash shart emas va top-N heapsort tanlanadi: u faqat kerakli N ta qatorni ushlab turadi, shuning uchun xotira talabi kichik. Sig'masa node external merge ga o'tadi: xotiraga sig'gan qism quicksort bilan saralanib vaqtinchalik faylga yoziladi, bo'shagan xotiraga keyingi qatorlar o'qiladi va shu takrorlanadi; oxirida fayllar birlashtiriladi. Birlashtirish ko'p xotira talab qilmaydi, chunki har fayldan bitta qator yetarli, lekin hamma fayl bitta o'tishda birlashmasa iteratsiya takrorlanadi va har iteratsiya diskka qo'shimcha o'qish va yozish qo'shadi. Shuning uchun xotira qancha ko'p bo'lsa, external sort shuncha tez tugaydi.

```sql
-- Qaysi algoritm ishlagani va diskka qancha to'kilgani
EXPLAIN (ANALYZE, BUFFERS)
SELECT * FROM parvozlar ORDER BY rejalashtirilgan_vaqt;
-- Sort Method: external merge  Disk: 17136kB
-- Buffers: shared hit=2627, temp read=2142 written=2150

-- Vaqtinchalik fayllarni logga yozish
ALTER SYSTEM SET log_temp_files = 0;
```

To'rtinchi variant PostgreSQL 13 dan bor: incremental sort. Agar to'plam bir nechta kalit bo'yicha saralanishi kerak bo'lsa va u boshlang'ich kalitlar bo'yicha allaqachon tartiblangan bo'lsa (masalan indeks skanidan kelayotgan bo'lsa), uni shu kalitlar bo'yicha guruhlarga bo'lib, har bir guruhni faqat qolgan kalitlar bo'yicha saralash yetarli. Bu kamroq xotira yeydi va birinchi guruh tayyor bo'lishi bilan natija qaytara boshlaydi, ya'ni `LIMIT` bilan juda yaxshi ishlaydi. Rejada u `Incremental Sort` node i, `Presorted Key` satri va guruhlar statistikasi bilan ko'rinadi.

Spring tomonida bundan aniq qoida chiqadi: `Pageable` bilan sahifalanadigan ro'yxatda `Sort` ustunlarining boshlang'ich qismi mavjud indeks tartibiga mos kelsa, planner incremental sort ni tanlay oladi va `LIMIT 20` uchun butun jadvalni saralamaydi. Mos kelmasa har sahifa so'rovi to'liq saralashni qaytadan bajaradi; `temp read/written` bloklarining noldan farqli bo'lishi aynan shuning signali.

## 24.16 Parallel reja: `Gather`, ishchi soni formulasi va parallellashmaydigan so'rovlar

So'rovni bajarayotgan asosiy protsess postmaster orqali bir nechta ishchi protsess ochadi, ular rejaning parallel qismini bir vaqtda bajaradi va natijalar `Gather` node ida yig'iladi. Asosiy protsess ma'lumot qabul qilmayotgan paytda o'zi ham parallel qismda qatnashadi; buni `parallel_leader_participation` bilan o'chirish mumkin. `Gather` dan pastdagi hamma narsa parallel qism, yuqoridagi hamma narsa ketma-ket qism.

Ishchi soni uchta parametr ierarxiyasi bilan cheklanadi: `max_worker_processes` umuman fon ishchilari soni, `max_parallel_workers` ulardan parallel so'rovga ajratilgani, `max_parallel_workers_per_gather` esa bitta `Gather` ga tegishlisi. Jadval uchun ishchi soni `parallel_workers` saqlash parametri qo'yilmagan bo'lsa formuladan hisoblanadi va formulaning ma'nosi oddiy: jadval hajmi `min_parallel_table_scan_size` ga nisbatan har uch barobar oshganda yana bitta ishchi qo'shiladi. Jadval `min_parallel_table_scan_size` dan kichik bo'lsa planner parallel rejani umuman ko'rib chiqmaydi.

Rejada `Workers Planned` va `Workers Launched` sonlari farq qilishi mumkin: ishga tushirish paytida bo'sh slot yetmasa, mavjud soni ishga tushadi va so'rov sekinroq bajariladi. Shuning uchun bitta katta hisobot so'rovi emas, bir vaqtda kelgan bir nechtasi muammo tug'diradi.

```sql
-- Jadval uchun ishchi sonini qo'lda belgilash
ALTER TABLE audit_log SET (parallel_workers = 4);

-- Rejalashtirilgan va haqiqatda ishga tushgan ishchi soni
EXPLAIN (ANALYZE, COSTS OFF)
SELECT count(*) FROM audit_log;
-- Gather (actual rows=3 loops=1)
--   Workers Planned: 2
--   Workers Launched: 2
```

Hamma so'rov ham parallellashmaydi. Kitob aniq cheklovlarni sanaydi: ma'lumotni o'zgartiradigan yoki qulflaydigan so'rovlar (`INSERT`, `UPDATE`, `DELETE`, `SELECT FOR UPDATE`); to'xtatib turish mumkin bo'lgan so'rovlar, ya'ni cursor ichida bajariladiganlar va PL/pgSQL dagi `FOR` sikllari; `PARALLEL UNSAFE` deb belgilangan funksiyani chaqiradigan so'rovlar, standart holatda esa foydalanuvchi yozgan hamma funksiya shunday hisoblanadi; va parallel so'rov ichidan chaqirilgan funksiya ichidagi so'rovlar.

Spring uchun birinchi ikki band eng muhimi. Spring Data ning `Stream<T>` qaytaradigan metodi yoki `ScrollableResults` serverda cursor ochadi, demak hisobot so'rovi parallel bajarilmaydi; katta eksport uchun cursor emas, kalit bo'yicha sahifalash (keyset pagination) tanlanadi. Ikkinchisi: o'z PL/pgSQL funksiyangizni so'rov shartida ishlatsangiz, uni `PARALLEL SAFE` deb e'lon qilmaguningizcha butun so'rov ketma-ket bajariladi.

```sql
CREATE OR REPLACE FUNCTION hisobot_koeffitsiyenti(summa numeric)
RETURNS numeric
LANGUAGE sql
IMMUTABLE
PARALLEL SAFE
AS $$ SELECT summa * 0.13 $$;
```

## 24.17 Asosiy statistika va `pg_stats`: `reltuples`, `n_distinct`, `null_frac`, `avg_width`

Planner har bir baholashni ikki qavatli statistikadan quradi. Birinchi qavat jadval darajasida `pg_class` da turadi: `reltuples` (qator soni), `relpages` (sahifa soni) va `relallvisible` (visibility map da butunlay ko'rinadigan deb belgilangan sahifa soni). Filtr bo'lmasa planner to'g'ridan to'g'ri `reltuples` ni qator soni deb oladi (Rogov, 17.1, 271-bet).

Ikki nozik joy bor. PostgreSQL 14 da `reltuples = -1` hali `ANALYZE` qilinmagan jadvalni haqiqatan bo'sh jadvaldan ajratadi, va statistikasi yo'q jadval uchun planner 10 sahifa deb taxmin qiladi. Agar fayl hajmi `relpages` dan katta bo'lsa, planner `reltuples` ni shu nisbatda kattalashtiradi, ya'ni ma'lumot zichligi o'zgarmagan deb hisoblaydi; qator o'chirilganda bu tuzatish ishlamaydi (Rogov, 17.1, 272-274-bet).

Ikkinchi qavat ustun darajasida `pg_statistic` da saqlanadi va `pg_stats` ko'rinishi orqali qulay shaklda o'qiladi (Rogov, 17.2, 275-bet). Arxitektorga kerak bo'ladigan maydonlar:

- **`null_frac`** - NULL ulushi. `IS NULL` shartining natijasi `reltuples * null_frac` (Rogov, 17.2, 275-bet).
- **`n_distinct`** - unikal qiymat soni. Manfiy qiymat sonni emas, ULUSHNI bildiradi: `-1` hamma qiymat unikal, `-3` har qiymat o'rtacha uch qatorda uchraydi. Analizator baholangan unikal qiymat soni jami qatorning 10 foizidan oshsa ulush shakliga o'tadi, chunki keyingi o'zgarishlar bu nisbatni buzmaydi (Rogov, 17.3, 276-bet). Tekis taqsimlash taxmini bilan `ustun = ifoda` shartining natijasi `reltuples / n_distinct` (Rogov, 17.3, 276-bet).
- **`avg_width`** - qiymatning o'rtacha hajmi. Sort va hash uchun kerak bo'ladigan xotira shu maydondan baholanadi (Rogov, 17.7, 284-bet).
- **`most_common_elems`, `most_common_elem_freqs`, `elem_count_histogram`** - skalyar bo'lmagan turlar uchun: massiv va `tsvector` ustida qiymat emas, ELEMENT darajasidagi statistika. Oxirgisi faqat massiv uchun yig'iladi (Rogov, 17.6, 283-bet).

Range va multirange turlari uchun ham taqsimot histogrammalari quriladi, lekin ular `pg_stats` da ko'rinmaydi (Rogov, 17.6, 284-bet).

```sql
-- Ikki qavat yonma-yon: jadval darajasi va ustun darajasi
SELECT c.reltuples, c.relpages, c.relallvisible,
       s.attname, s.null_frac, s.n_distinct, s.avg_width
FROM pg_class c
  JOIN pg_stats s ON s.tablename = c.relname
WHERE c.relname = 'orders'
  AND s.attname IN ('status', 'customer_id', 'shipped_at');

-- Namuna kichik bo'lgani uchun n_distinct xato chiqsa, uni majburlash mumkin
ALTER TABLE orders ALTER COLUMN customer_id SET (n_distinct = 200000);
ANALYZE orders;
```

Java tomonida bundan ikki xulosa chiqadi. `jsonb` yoki `text[]` ustuniga qurilgan GIN indeks bilan ishlaydigan so'rovning taxmini `most_common_elems` ga tayanadi, ya'ni ustun statistikasi emas, element statistikasi kerak; bu ustunlarda `SET STATISTICS` ni oshirish boshqa natija beradi. Ikkinchisi: `n_distinct` manfiy chiqsa bu xato emas, shunchaki ulush shakli, va uni monitoring skriptida musbat deb o'qish noto'g'ri hisobot beradi.

## 24.18 `most_common_vals` va `histogram_bounds` dan selektivlik qanday chiqadi

Tekis taqsimlash taxmini amalda kamdan kam to'g'ri keladi, shuning uchun planner ikki qo'shimcha tuzilmaga tayanadi va ikkalasi ham `pg_stats` da ochiq turadi.

**Eng tez uchraydigan qiymatlar.** `most_common_vals` massivi qiymatlarni, `most_common_freqs` esa ularning chastotasini bir xil indeksda saqlaydi. `ustun = qiymat` sharti uchun selektivlik shunchaki shu massivdan topilgan chastota (Rogov, 17.4, 277-278-bet). Tengsizlik uchun ham shu ro'yxat ishlatiladi: `ustun < qiymat` da shartga mos keladigan hamma MCV chastotasi qo'shiladi (Rogov, 17.5, 279-bet).

Ro'yxat uzunligi `default_statistics_target` bilan chegaralangan. Hajmi 1 kB dan katta qiymatlar tahlilga ham, statistikaga ham kiritilmaydi; bunday qiymatlar odatda unikal bo'lgani uchun ular baribir MCV ga tushmaydi (Rogov, 17.4, 279-bet).

**Histogram.** Unikal qiymat juda ko'p bo'lsa MCV yetmaydi va planner histogramga o'tadi. Chegaralar `histogram_bounds` massivida turadi, bucket soni yana `default_statistics_target` bilan cheklangan va bucket kengligi har biriga taxminan bir xil miqdorda qiymat tushadigan qilib tanlanadi (Rogov, 17.5, 279-280-bet).

Ikki narsa histogramga KIRMAYDI: MCV ro'yxatidagi qiymatlar va NULL lar. Shuning uchun `ustun > qiymat` ning yakuniy baholashi ikki qismdan yig'iladi: shartga mos MCV ulushi, va histogramga qolgan ulushning (bir minus jami MCV ulushi minus `null_frac`) shartga tushgan bucket lar ulushi. Qiymat bucket chegarasida turmasa planner bucket ichida chiziqli interpolatsiya qiladi (Rogov, 17.5, 281-282-bet).

```sql
-- Planner aynan shu uch maydonni o'qiydi
SELECT null_frac, n_distinct,
       most_common_vals,
       left(most_common_freqs::text, 60) AS mcf,
       left(histogram_bounds::text, 60) AS hist
FROM pg_stats
WHERE tablename = 'orders' AND attname = 'status';

-- Bitta qiymat uchun planner hisobini qo'lda takrorlash
SELECT round(c.reltuples * s.most_common_freqs[
         array_position(s.most_common_vals::text::text[], 'NEW')
       ]) AS kutilgan_qator
FROM pg_class c
  JOIN pg_stats s ON s.tablename = c.relname
WHERE c.relname = 'orders' AND s.attname = 'status';
```

Amaliy xulosa aniq. `status` kabi kam qiymatli notekis ustun MCV ga butunlay sig'adi va taxmin yaxshi chiqadi; qiymat soni `default_statistics_target` dan oshganda qolganlari histogramga tushadi va taxmin qo'pollashadi. `SET STATISTICS` ni oshirish aynan shu holatda foyda beradi. Kitob buni ochiq cheklaydi: aniqlikni oshirish faqat u yaxshiroq rejaga olib kelsa ma'noli, o'ylamay oshirish esa planlashtirish va `ANALYZE` ni sekinlashtiradi (Rogov, 17.5, 283-bet).

## 24.19 Narx formulasi: seq scan, index scan va bitmap scan nimadan yig'iladi

`cost` raqami bir nechta parametr ko'paytmasining yig'indisi. Formulani bilish ikki narsa beradi: rejadagi raqam nega shuncha ekanini tushuntiradi va qaysi parametr qarorni siljitishini ko'rsatadi.

**Sequential scan.** I/O qismi `relpages * seq_page_cost`, CPU qismi `reltuples * cpu_tuple_cost`, startup narxi nol, chunki seq scan hech narsani oldindan tayyorlamaydi. Filtr bo'lsa har bir shart operatori uchun `cpu_operator_cost` qo'shiladi (Rogov, 18.2, 296-298-bet).

**Index scan.** Indeks qismi: o'qiladigan indeks sahifasi soni indeks hajmini selektivlikka ko'paytirish bilan baholanadi va bu sahifalar tasodifiy o'qiladi, ya'ni `random_page_cost` bilan; ustiga har bir indeks yozuvi uchun `cpu_index_tuple_cost` va har bir shart hisobi uchun `cpu_operator_cost` qo'shiladi. Heap qismi esa korrelyatsiyaga bog'liq: korrelyatsiya ideal bo'lsa sahifalar ketma-ket o'qiladi, korrelyatsiya nol bo'lsa eng yomon holatda sahifaga murojaat soni olingan qator soniga yetadi. Planner ikki chekka holat uchun narxni hisoblab, haqiqiy korrelyatsiyaga qarab oraliq qiymat oladi; `effective_cache_size` qancha katta bo'lsa, kerakli sahifa keshda topilishi shuncha ehtimolli deb hisoblanadi (Rogov, 20.1, 331-336-bet).

**Bitmap scan.** `Bitmap Index Scan` narxi heap siz index scan kabi hisoblanadi. `Bitmap Heap Scan` da o'qiladigan sahifa soni alohida formuladan chiqadi, bitta sahifa narxi esa olinadigan sahifa ulushiga qarab `seq_page_cost` bilan `random_page_cost` orasida yotadi. Baholashga `lossy` segmentlar ulushi va qayta tekshirish narxi ham qo'shiladi (Rogov, 20.3, 344-345-bet).

PostgreSQL 14 dagi standart narx parametrlari:

| Parametr | Standart | Nimani o'lchaydi |
| --- | --- | --- |
| `seq_page_cost` | 1 | ketma-ket o'qilgan bitta sahifa |
| `random_page_cost` | 4 | tasodifiy o'qilgan bitta sahifa |
| `cpu_tuple_cost` | 0.01 | bitta qatorni qayta ishlash |
| `cpu_index_tuple_cost` | 0.005 | bitta indeks yozuvini qayta ishlash |
| `cpu_operator_cost` | 0.0025 | bitta operator yoki funksiya chaqiruvi |

Manba: `seq_page_cost` va `random_page_cost` (Rogov, 18.2, 297-bet), `cpu_tuple_cost` va `cpu_operator_cost` (Rogov, 18.2, 298-bet), `cpu_index_tuple_cost` (Rogov, 20.1, 333-bet).

```sql
-- Rejadagi seq scan narxini qo'lda takrorlash
SELECT relpages * current_setting('seq_page_cost')::real +
       reltuples * current_setting('cpu_tuple_cost')::real AS seq_scan_cost
FROM pg_class WHERE relname = 'orders';
```

Bundan uch amaliy natija chiqadi. Birinchisi: jadval shishsa `relpages` o'sadi va seq scan narxi tirik qator soniga qaramay ko'tariladi, ya'ni vacuum kechikishi to'g'ridan to'g'ri reja tanloviga ta'sir qiladi (Rogov, 18.2, 297-bet). Ikkinchisi: SSD da [`random_page_cost` ni pasaytirish](#243-narx-parametrlari-random_page_cost-seq_page_cost-effective_cache_size-manosi) index scan ning indeks qismini ham, korrelyatsiyasi past heap qismini ham arzonlashtiradi, shuning uchun u eng kuchli bitta sozlama. Uchinchisi: `cpu_operator_cost` juda kichik ko'rinadi, lekin so'rov shartidagi funksiya har qator uchun chaqiriladi va millionlab qatorda u sezilarli hissa beradi.

## 24.20 Join turlari: inner, outer, semi, anti va dekart ko'paytma

Join turi va join usuli ikki alohida narsa. Tur mantiqiy amal (`INNER`, `LEFT`, `FULL`, semi, anti), usul esa uni bajaradigan algoritm (nested loop, hash, merge). Har bir algoritm hamma turni qo'llab quvvatlamaydi va rejadagi tugun nomi aynan shu juftlikni aytadi (Rogov, 21.1, 350-351-bet).

- **Inner join.** Shart ikki to'plamning kalitlari tengligini talab qilsa bu equi-join, eng keng tarqalgan shakl.
- **Dekart ko'paytma.** `CROSS JOIN` bu sharti doim rost bo'lgan inner join ning xususiy holi. Uni bajarishning eng samarali usuli to'plamlar hajmidan qat'i nazar nested loop; ichki tomon odatda `Materialize` tugunining ortida turadi, ya'ni bir marta o'qilib saqlanadi va qayta skanlanmaydi (Rogov, 21.2, 352-bet).
- **Outer join.** Nested loop faqat inner va left outer ni biladi: rejada `Nested Loop` va `Nested Loop Left Join`. Right va full join nested loop da umuman yo'q, chunki algoritm tashqi va ichki to'plamga boshqacha munosabatda bo'ladi (Rogov, 21.2, 363-bet). Outer join natijasining qator soni hech qachon tashqi to'plamnikidan kam bo'lmaydi: planner ikki baholashdan kattasini oladi (Rogov, 21.2, 362-bet).
- **Semi-join.** `EXISTS` shartida ichki to'plamdan bitta mos qator topilishi yetarli, keyin skan to'xtaydi. Rejada `Nested Loop Semi Join`.
- **Anti-join.** `NOT EXISTS`, yoki unga teng kuchli `LEFT JOIN ... WHERE ... IS NULL` uchun bir xil reja quriladi: `Nested Loop Anti Join` (Rogov, 21.2, 363-364-bet).

```sql
-- Semi-join
EXPLAIN SELECT o.id FROM orders o
WHERE EXISTS (SELECT 1 FROM payments p WHERE p.order_id = o.id);
-- Nested Loop Semi Join

-- Anti-join: ikkala shakl ham bir xil rejaga tushadi
EXPLAIN SELECT o.id FROM orders o
WHERE NOT EXISTS (SELECT 1 FROM payments p WHERE p.order_id = o.id);

EXPLAIN SELECT o.id FROM orders o
  LEFT JOIN payments p ON p.order_id = o.id
WHERE p.order_id IS NULL;
-- Nested Loop Anti Join
```

Rejadagi baholash bu yerda aldamchi ko'rinadi: semi va anti join tugunining ichki tomonida `rows` mos keladigan jami qator sonini ko'rsatadi, garchi ijroda birinchi qator topilgach skan to'xtasa ham. Haqiqatni `actual rows` va `loops` juftligi aytadi (Rogov, 21.2, 364-bet).

Spring tomonida bundan aniq qoida chiqadi. Spring Data ning `existsBy...` metodi va JPQL dagi `EXISTS` semi-join beradi, ya'ni planner erta to'xtay oladi. Mavjudlikni `count(*) > 0` bilan tekshirish esa shu imkonni yo'qotadi, chunki hamma mos qator sanalishi kerak.

## 24.21 `HashAggregate` va `GroupAggregate`: `DISTINCT` va `GROUP BY` ni bajarishning ikki yo'li

Guruhlash va takrorlarni olib tashlash algoritmlari join algoritmlariga juda o'xshaydi: ikkalasi ham yo hash jadval quradi, yo sortlangan oqimdan bir o'tishda guruh ajratadi (Rogov, 22.2, 384-bet; 23.3, 403-bet).

**Hash yo'li.** Tugun nomi `HashAggregate`. U `GROUP BY` da ham, `DISTINCT` da ham, `UNION` da ham paydo bo'ladi; `UNION` da `Append` ikki to'plamni qo'shadi, takrorlarni esa `HashAggregate` olib tashlaydi. Hash jadvalga ajratilgan xotira `work_mem` ni `hash_mem_multiplier` ga ko'paytirganiga teng, ya'ni hash join dagidek (Rogov, 22.2, 384-385-bet).

PostgreSQL 13 dan boshlab bu tugun diskka to'kila oladi: xotira to'lgach qolgan qiymatlar hash qiymatining bir necha biti bo'yicha partitsiyalarga bo'linib vaqtinchalik faylga yoziladi. Partitsiya soni ikkining darajasi bo'ladi va hisoblangan son yana 1.5 ga ko'paytiriladi, chunki statistika aniq emas va partitsiyalar kichikroq bo'lgani yaxshi (Rogov, 22.2, 386-bet). Rejada bu `Batches`, `Memory Usage` va `Disk Usage` qatorlarida ko'rinadi.

**Sort yo'li.** Kirish allaqachon sortlangan bo'lsa, masalan index skanidan kelsa, takrorlarni olib tashlash juda sodda `Unique` tuguni bilan, agregatsiya esa `GroupAggregate` tuguni bilan bajariladi. Parallel rejada ular `Partial GroupAggregate` va `Finalize GroupAggregate` deb ataladi (Rogov, 23.3, 403-404-bet).

Uchinchi variant ham bor: `GROUPING SETS`, `CUBE` yoki `ROLLUP` bilan bir nechta ustun to'plami bo'yicha guruhlanganda bitta `MixedAggregate` tugunida hash va sort strategiyalari birga ishlatiladi (Rogov, 23.3, 404-bet).

```sql
-- Hash yo'li: xotira yetmasa Batches 1 dan oshadi va Disk Usage chiqadi
EXPLAIN (ANALYZE, COSTS OFF, TIMING OFF)
SELECT customer_id, count(*) FROM orders GROUP BY customer_id;
-- HashAggregate
--   Group Key: customer_id
--   Batches: N  Memory Usage: ...  Disk Usage: ...

-- Sort yo'li: index tartibidan kelgan oqim, qo'shimcha sort kerak emas
EXPLAIN (COSTS OFF)
SELECT customer_id, count(*) FROM orders
GROUP BY customer_id ORDER BY customer_id;
-- GroupAggregate
--   -> Index Only Scan using orders_customer_id_idx on orders
```

Arxitektor uchun signal aniq: `HashAggregate` da `Disk Usage` chiqsa yechim ikkita, ya'ni shu so'rov uchun `work_mem` ni `SET LOCAL` bilan oshirish yoki guruhlash kalitiga mos indeks berib planner'ni `GroupAggregate` yo'liga o'tkazish. Ikkinchisi natija `ORDER BY` bilan qaytadigan hisobotlarda ikki foyda beradi, chunki sort qayta bajarilmaydi.

## 24.22 Kengaytirilgan so'rov protokoli: tayyorlash, parametr bog'lash va natijani bo'laklab olish

Oddiy so'rov protokolida har bir buyruq, hatto bir xil bo'lsa ham, to'rt bosqichning hammasidan o'tadi: parse, transformatsiya, planlashtirish, ijro. Bundan tashqari mijoz natijani qancha qator bo'lsa ham bir yo'la oladi. Shu ikki cheklovni `PREPARE` va `DECLARE CURSOR` bilan ham yengish mumkin, lekin unda nomlarni mijoz boshqarishi kerak va serverga qo'shimcha buyruqni parse qilish tushadi. Kengaytirilgan protokol xuddi shu nazoratni protokolning o'z darajasida beradi (Rogov, 16.3, 266-bet).

**Tayyorlash.** So'rov odatdagidek parse va transformatsiya qilinadi, natija daraxti esa backend xotirasida qoladi. PostgreSQL da so'rovlar uchun global kesh yo'q: har bir backend o'zi parse qiladi. Kamchiligi ko'rinib turibdi, lekin foydasi ham bor, chunki global kesh qulflar tufayli butun instansiyaning tor joyiga aylanadi va faqat konstantasi bilan farq qiladigan ko'p so'rov yuboradigan klient boshqalarga ta'sir qilmaydi (Rogov, 16.3, 266-bet). Nomlangan `PREPARE` lar `pg_prepared_statements` da ko'rinadi; protokol darajasidagi nomsizlari va boshqa sessiyalarnikilar ko'rinmaydi (Rogov, 16.3, 267-bet).

**Parametr bog'lash.** Ijro oldidan parametr qiymatlari bog'lanadi. Bu literalni so'rov matniga yopishtirishdan nafaqat tez, balki xavfsiz: bog'langan qiymat allaqachon qurilgan parse daraxtini hech qanday yo'l bilan o'zgartira olmaydi, ya'ni SQL inyeksiya imkonsiz bo'ladi (Rogov, 16.3, 267-bet).

**Natijani olish.** Ijro paytida executor backend xotirasida portal ochadi: bu joriy so'rovning holatini saqlaydigan obyekt, uning ichida reja daraxtini takrorlaydigan tugunlar daraxti turadi va tugunlar bir biridan qator so'rab oladi (Rogov, 16.2, 264-bet). Shu holat saqlangani uchun kengaytirilgan protokol natijani bo'lak bo'lak qaytara oladi. SQL kursori ham shunga yaqin natija beradi, lekin ikki farq bilan: serverga qo'shimcha ish tushadi va planner butun natijani emas, birinchi `cursor_tuple_fraction` ulushini (PostgreSQL 14 da standarti 0.1) olishni optimallashtiradi (Rogov, 16.2, 262-bet; 16.3, 270-bet). Bo'lak hajmi throughput ga sezilarli ta'sir qiladi: qatorma-qator olish bilan o'nlab qator olish orasidagi farq juda katta, lekin yuzta va mingta orasidagi farq ancha kichik (Rogov, 16.3, 270-bet).

```properties
# PgJDBC: nechanchi bajarilishdan keyin server-side prepare ishlatiladi
spring.datasource.hikari.data-source-properties.prepareThreshold=5

# Natijani bo'lak bo'lak olish uchun avtomatik commit o'chirilishi kerak
spring.datasource.hikari.auto-commit=false
```

ESLATMA: `prepareThreshold` va `auto-commit` qiymatlari PgJDBC va HikariCP sozlamalari, kitobning qoidasi emas. Kitobdan kelib chiqadigan qoida boshqa va u Spring kodiga to'g'ridan to'g'ri tegadi: kursor ochilgan so'rov planner oldiga boshqa maqsad qo'yadi va [parallel bajarilmaydi](#2416-parallel-reja-gather-ishchi-soni-formulasi-va-parallellashmaydigan-sorovlar), shuning uchun katta eksportda kursor bilan o'qish va parallel reja bir vaqtda bo'lmaydi.

## 24.23 Parallel narx: `parallel_setup_cost`, `parallel_tuple_cost` va `Parallel Seq Scan`

`Parallel Seq Scan` nomi ziddiyatli ko'rinadi, lekin u aniq narsani aytadi: fayl darajasida sahifalar odatdagi seq scan tartibida o'qiladi, faqat buni bir nechta protsess birga qiladi va ular bir sahifani ikki marta o'qimaslik uchun umumiy xotira orqali sinxronlanadi (Rogov, 18.4, 301-bet).

Bitta nozik oqibat bor. Operatsion tizim bu manzarani ko'rmaydi, u bir nechta protsessning tasodifiy o'qishini ko'radi, shuning uchun seq scan ni tezlashtiradigan prefetch deyarli foyda bermaydi. Buni yumshatish uchun PostgreSQL har bir protsessga bitta emas, bir nechta ketma-ket sahifa beradi (Rogov, 18.4, 301-bet). Shu sababdan sof parallel skan o'zi yutuq bermaydi: foyda ishchilar olingan qatorlar ustida ish qilganda, masalan agregatsiya qilganda chiqadi.

`Parallel Seq Scan` satridagi `rows` bitta protsessga tushadigan o'rtacha qator soni. Lider ishchilardan kam qator oladi va uning ulushi ishchi soni ortgani sari kichrayadi (Rogov, 18.4, 302-bet). Narx hisobida CPU qismi protsesslar orasida bo'linadi, I/O qismi esa to'liq qoladi, chunki jadval baribir butunligicha, sahifama-sahifa o'qiladi (Rogov, 18.4, 302-bet).

`Gather` tuguni ikki yangi parametr olib keladi (Rogov, 18.4, 303-bet):

- **`parallel_setup_cost`**, standarti 1000. Protsesslarni ishga tushirish narxi, ularning sonidan qat'i nazar bir marta hisoblanadi.
- **`parallel_tuple_cost`**, standarti 0.1. Protsessdan protsessga uzatilgan har bir qatorning narxi.

```sql
-- Gather dan pastdagi hamma narsa ishchilarda, yuqoridagisi liderda bajariladi
EXPLAIN SELECT count(*) FROM audit_log;
-- Finalize Aggregate
--   -> Gather
--       Workers Planned: 2
--       -> Partial Aggregate
--           -> Parallel Seq Scan on audit_log
```

Bu ikki raqamdan arxitektor qarori chiqadi. 1000 lik setup narxi degani: ketma-ket rejaning narxi mingdan sezilarli katta bo'lmasa planner parallelni umuman tanlamaydi, ya'ni kichik jadvalda parallel reja kutish ortiqcha. 0.1 lik qator narxi esa `Gather` orqali ko'p qator qaytarish qimmat ekanini aytadi: parallel reja `count`, `sum` va `GROUP BY` kabi natijani kichraytiradigan so'rovda foyda beradi, million qator qaytaradigan `SELECT *` da emas.

## 24.24 Parallel restricted: faqat lider bajaradigan qism va `force_parallel_mode`

Parallellashmaydigan so'rov va parallel restricted amal ikki boshqa narsa. Birinchisi butun so'rovni ketma-ket qiladi. Ikkinchisi so'rovning parallel bo'lishiga prinsipial xalaqit bermaydi, lekin o'zi faqat lider protsessda bajariladi, ya'ni reja daraxtida `Gather` tugunidan PASTDA tura olmaydi (Rogov, 18.5, 309-bet).

- **Kengaytirib bo'lmaydigan pastki so'rovlar.** Eng ko'rinadigan misoli `CTE Scan`, ya'ni `MATERIALIZED` deb e'lon qilingan CTE natijasini o'qish. CTE materializatsiya qilinmasa rejada `CTE Scan` bo'lmaydi va bu cheklov ham ishlamaydi; CTE ning o'zi esa arzon chiqsa parallel hisoblanishi mumkin (Rogov, 18.5, 309-310-bet).
- **`SubPlan` va `InitPlan`.** `SubPlan` natijasiga tayanadigan yuqoridagi tugun parallel ishtirok eta olmaydi. `InitPlan` esa bir marta hisoblanadi: uning ota tuguni parallel bo'lmaydi, lekin natijani qabul qiladigan tugunlar parallel bo'laveradi (Rogov, 18.5, 310-311-bet).
- **Vaqtinchalik jadvallar.** Temporary table ni faqat uni yaratgan protsess ko'radi va uning sahifalari lokal buffer cache da ishlanadi, shuning uchun parallel skan yo'q (Rogov, 18.5, 311-bet).
- **`PARALLEL RESTRICTED` funksiyalar.** Ular rejaning faqat ketma-ket qismida chaqirila oladi; ro'yxat katalogdan olinadi (Rogov, 18.5, 312-bet).

```sql
-- Restricted va unsafe funksiyalar ro'yxati
SELECT proname, proparallel FROM pg_proc WHERE proparallel = 'r';  -- restricted
SELECT proname, proparallel FROM pg_proc WHERE proparallel = 'u';  -- unsafe

-- So'rov prinsipial parallellasha oladimi: vaqtincha majburlab tekshirish
SET force_parallel_mode = on;
EXPLAIN SELECT * FROM orders;
-- Gather
--   Workers Planned: 1
--   Single Copy: true
RESET force_parallel_mode;
```

`force_parallel_mode` (PostgreSQL 14 dagi nomi, standarti `off`) ishlab chiqarish sozlamasi emas, diagnostika vositasi: u planner'ga imkon bo'lgan joyda parallel reja qurishni buyuradi, shunda so'rov umuman parallellasha oladimi yoki yo'qmi ko'rinadi (Rogov, 18.5, 309-bet).

Spring tomonida bu uch joyda uriladi. `@Query` ichidagi `WITH ... AS MATERIALIZED` hisobotni ketma-ket qismga qamaydi; batch job ichidagi `CREATE TEMPORARY TABLE` oraliq jadvali parallel skanni butunlay yopadi; korrelyatsiyalangan pastki so'rov esa yuqoridagi skanni `SubPlan` orqali lider protsessga bog'laydi. Uchalasi uchun yechim bir xil: oraliq natijani haqiqiy jadvalga yozish yoki pastki so'rovni `JOIN` ga aylantirish.

## 24.25 Parallel skan tugunlari: index, index-only va bitmap

Uchala indeks skan rejimi ham parallel rejada o'z shakliga ega. Narx hisobi ketma-ket variantiga o'xshaydi, bitta muhim farq bilan: CPU qismi protsesslar orasida bo'linadi, I/O qismi esa bo'linmaydi, chunki sahifaga murojaat sinxronlangan holda ketma-ket bajariladi (Rogov, 20.4, 347-bet).

- **`Parallel Index Scan`.** B-tree parallel skani davomida joriy indeks sahifasining ID si serverning umumiy xotirasida turadi. Skanni boshlagan protsess ildizdan birinchi mos bargga tushib uning ID sini yozadi; ishchilar keyingi sahifalarni navbat bilan olib, saqlangan ID ni almashtiradi va topilgan yozuvlar bo'yicha heap qatorlarini o'qiydi (Rogov, 20.4, 347-bet).
- **`Parallel Index Only Scan`.** Yagona farqi shundaki, u butunlay ko'rinadigan sahifalar uchun heap ga bormaydi (Rogov, 20.4, 348-bet).
- **`Parallel Bitmap Heap Scan`.** Bitmap har doim ketma-ket, bitta lider protsess tomonidan quriladi. Aynan shuning uchun pastdagi tugun nomida `Parallel` so'zi yo'q, u oddiy `Bitmap Index Scan` bo'lib qoladi. Bitmap tayyor bo'lgach heap ni ishchilar parallel o'qiydi (Rogov, 20.4, 348-bet).

```sql
EXPLAIN SELECT sum(amount) FROM payments WHERE paid_at < DATE '2026-01-01';
-- Finalize Aggregate
--   -> Gather
--       Workers Planned: 2
--       -> Partial Aggregate
--           -> Parallel Bitmap Heap Scan on payments
--               -> Bitmap Index Scan on payments_paid_at_idx
```

Reja o'qishda bundan ikki xulosa chiqadi. Birinchisi: `Bitmap Index Scan` nomida `Parallel` yo'qligi xato emas, u mexanikaning o'zi. Ikkinchisi: I/O bo'linmagani uchun diskka bog'liq so'rovda ishchi sonini oshirish kutilgan tezlanishni bermaydi; ishchi soni faqat CPU ga bog'liq qismni, ya'ni filtr va agregatsiyani tezlashtiradi.

## 24.26 Parallel join va `Gather Merge`: tartibni saqlab yig'ish

Join algoritmlarining parallel rejadagi xulqi bir xil emas va reja o'qishda buni bilish kerak.

- **Nested loop.** Parallel bajariladigan qism faqat tashqi to'plam: uni bir nechta ishchi bo'lib skanlaydi. Tashqi qatorni olgan har bir ishchi ichki to'plamdagi mos qatorlarni o'zi, ketma-ket qidiradi (Rogov, 21.2, 366-bet).
- **Hash join.** Oddiy hash join ham parallel rejada ishlaydi, lekin unda har bir protsess o'ziga bir xil hash jadval quradi. Demak xotira chegarasi har bir protsessga alohida qo'llanadi va jami sarf rejadagi `Memory Usage` dan protsess soniga ko'ra katta bo'ladi (Rogov, 22.1, 377-378-bet).
- **`Parallel Hash`.** Katta to'plam uchun alohida algoritm bor: hash jadval umumiy xotirada, bitta nusxada quriladi va unga hamma protsessga ajratilgan xotira yig'indisi, ya'ni `work_mem` ni `hash_mem_multiplier` ga va protsess soniga ko'paytirgani tegadi. Shu sababdan join bir o'tishda tugash ehtimoli ortadi. Rejada bu `Parallel Hash` va `Parallel Hash Join` tugunlari, boshqarish kaliti `enable_parallel_hash` (Rogov, 22.1, 378-380-bet). Right va full join uchun parallel hash join qo'llab quvvatlanmaydi (Rogov, 22.1, 384-bet).
- **Merge join.** Uning parallel shakli umuman yo'q, lekin u parallel rejada qatnasha oladi: tashqi to'plam ishchilar orasida bo'linadi, ichki to'plamni esa har bir ishchi butunligicha o'qiydi (Rogov, 23.1, 390-bet).

**`Gather Merge`.** `Gather` ishchilarning tartibini bilmaydi va qatorlarni kelgan tartibida yig'adi. Tartib saqlanishi kerak bo'lsa executor `Gather Merge` ishlatadi: u binar uyum bilan bir nechta sortlangan oqimni birlashtiradi (Rogov, 23.2, 401-bet). Narxi `Gather` nikidek `parallel_setup_cost` dan boshlanadi, qator uzatish esa `parallel_tuple_cost` ning 5 foiz oshirilgan qiymati bilan hisoblanadi, chunki keyingi qiymatni kutish ehtimoli bor (Rogov, 23.2, 401-402-bet).

```sql
EXPLAIN (ANALYZE, COSTS OFF, TIMING OFF)
SELECT * FROM orders ORDER BY created_at LIMIT 10;
-- Limit
--   -> Gather Merge
--       Workers Planned: 1
--       -> Sort
--           Sort Key: created_at
--           Sort Method: top-N heapsort
--           -> Parallel Seq Scan on orders
```

Amaliy signal shu: rejada `Gather` turgan bo'lsa undan yuqoridagi `Sort` butun natijani qayta saralaydi, `Gather Merge` turgan bo'lsa saralash ishchilarda bajarilgan va lider faqat birlashtiradi. Ikkinchisi [`LIMIT` bilan](#2415-sort-node-ichida-quicksort-top-n-heapsort-external-merge-va-incremental-sort) ancha arzon, chunki har bir ishchi o'z ulushidan faqat kerakli qatorlarni beradi.

## 24.27 `WITH RECURSIVE`: o'zgaruvchan chuqurlikdagi ierarxiya va graf yurish

Java loyihalarida kategoriya daraxti, tashkiliy ierarxiya yoki bog'liqlik grafi odatda ilovada sikl bilan yuriladi va har bosqichda yangi so'rov yuboriladi: chuqurlik qancha bo'lsa, shuncha round-trip. Kleppmann sababini aniq aytadi: oddiy relyatsion so'rovda qaysi join lar kerakligi oldindan ma'lum, graf yoki ierarxiya so'rovida esa qidirilgan tugunga yetish uchun nechta qirradan o'tish kerakligi oldindan ma'lum emas, ya'ni join soni qotib qolmaydi (*Designing Data-Intensive Applications*, 2-bob, 53-bet). SQL:1999 dan beri bu yurish rekursiv CTE, ya'ni `WITH RECURSIVE` bilan yoziladi va PostgreSQL uni qo'llab-quvvatlaydi; Kleppmann sintaksis maxsus graf so'rov tiliga nisbatan noqulay ekanini qo'shadi (2-bob, 53-54-betlar), lekin natija bitta so'rov va bitta round-trip bo'ladi. Materiallashtirish qarori esa [so'rovni qayta yozish](#2411-sorovni-qayta-yozish-exists-lateral-distinct-on-cte-va-materializatsiya) bo'limidagi oddiy CTE bilan bir xil emas: rekursiv CTE inline qilinmaydi.

```sql
-- Ierarxiya: berilgan kategoriyaning hamma avlodi, bitta so'rovda.
-- categories(id bigint primary key, parent_id bigint references categories, name text)
WITH RECURSIVE subtree(id, parent_id, name, depth, path) AS (
        SELECT c.id, c.parent_id, c.name, 0, ARRAY[c.id]
        FROM categories c
        WHERE c.id = $1
    UNION ALL
        SELECT c.id, c.parent_id, c.name, s.depth + 1, s.path || c.id
        FROM categories c
        JOIN subtree s ON c.parent_id = s.id
        WHERE NOT c.id = ANY(s.path)     -- sikl himoyasi: yo'l massivi
          AND s.depth < 50               -- chegara qiymati namuna, loyihaga qarab
)
SELECT id, name, depth FROM subtree ORDER BY depth, name;
```

Mexanikasi reja o'qish uchun ham kerak. Rekursiv `WITH` so'rovi doim uch bo'lakdan iborat: rekursiv bo'lmagan had, `UNION` yoki `UNION ALL`, keyin rekursiv had; faqat rekursiv had so'rovning o'z natijasiga murojaat qila oladi. Ichida u rekursiv emas, iterativ bajariladi: avval rekursiv bo'lmagan had hisoblanib natija vaqtinchalik working table ga tushadi, keyin working table bo'sh bo'lmagan vaqtgacha rekursiv had uning joriy mazmuni bilan qayta hisoblanadi. `UNION` har qadamda takrorlangan qatorlarni tashlab yuboradi, `UNION ALL` esa tashlamaydi, shuning uchun siklni to'xtatishning birinchi chorasi `UNION`. Lekin natijada `depth` kabi ustun bo'lsa, qatorlar aynan takrorlanmaydi va `UNION` ham aylanishni to'xtatmaydi. PostgreSQL hujjati shu holat uchun standart usulni beradi: o'tilgan qiymatlarni massivga yig'ish va rekursiv hadda shu massivni tekshirish; massiv o'zi ham foydali, chunki qatorga qaysi yo'l bilan kelinganini ko'rsatadi. Sikl bir necha maydon bo'yicha aniqlansa massiv elementi `ROW(...)` bo'ladi, bitta maydon yetsa oddiy massiv tezroq.

```sql
-- Graf: checkout servisidan boriladigan tugunlar, sikl bilan birga.
-- service_edges(source text, target text)
WITH RECURSIVE reach(node, path, is_cycle) AS (
        SELECT e.target, ARRAY[e.source, e.target], false
        FROM service_edges e WHERE e.source = 'checkout'
    UNION ALL
        SELECT e.target, r.path || e.target, e.target = ANY(r.path)
        FROM service_edges e JOIN reach r ON e.source = r.node
        WHERE NOT r.is_cycle
)
SELECT DISTINCT node FROM reach WHERE NOT is_cycle;
```

```java
// Spring tomonida bu oddiy native so'rov: ilovadagi sikl va N+1 yo'qoladi.
@Query(value = SUBTREE_SQL, nativeQuery = true)
List<CategoryNode> findSubtree(@Param("rootId") long rootId,
                               @Param("maxDepth") int maxDepth);
```

Chegara qo'yish majburiy: ma'lumotda sikl yoki buzilgan `parent_id` bo'lsa, chegarasiz rekursiv so'rov to'xtamaydi va vaqtinchalik natija o'sib boradi. Shuning uchun har rekursiv so'rovda ikki himoya birga turadi, yo'l massivi va chuqurlik chegarasi, va ikkisi ham `EXPLAIN (ANALYZE, BUFFERS)` da ko'rinadigan qatorlar sonini cheklaydi.

## 24.28 Amalda qo'llash

- [ ] Eng og'ir 20 so'rovni `pg_stat_statements` dan `total_exec_time` bo'yicha chiqarib, ularning har biri uchun `EXPLAIN (ANALYZE, BUFFERS)` rejasini saqlab qo'y.
- [ ] Har bir rejada taxmin va haqiqiy qator sonini taqqoslab, 10 baravardan ortiq farq bo'lgan node'lar ro'yxatini tuz.
- [ ] SSD serverlarda `random_page_cost` ni 1.1 ga, `effective_cache_size` ni RAM ning 75 foiziga keltir va o'zgarishdan oldin va keyin rejalarni taqqoslab yoz.
- [ ] 10 million qatordan katta jadvallarga `autovacuum_analyze_scale_factor = 0.02` qo'yib, `pg_stat_user_tables` dagi `last_autoanalyze` ni haftada bir tekshir.
- [ ] Birgalikda filtrlanadigan bog'liq ustun juftliklarini aniqlab, ularga `CREATE STATISTICS` yaratib `ANALYZE` ishlatib natijani tasdiqla.
- [ ] `auto_explain` ni `log_min_duration = 500ms` va `sample_rate = 0.1` bilan yoqib, log'dan haftalik sekin reja hisobotini chiqar.
- [ ] Notekis taqsimlangan ustun bo'yicha filtrlaydigan prepared statement'larni topib, generic plan regressiyasini sinab ko'r va kerak bo'lsa partial index yoki `force_custom_plan` qo'lla.
- [ ] `work_mem` ni global 32MB da qoldirib, hisobot va eksport yo'llarida `SET LOCAL` bilan oshirishni kod darajasida standartlashtir.

## Manbalar

- [PostgreSQL 17, Recursive Queries (queries.sgml)](https://raw.githubusercontent.com/postgres/postgres/REL_17_STABLE/doc/src/sgml/queries.sgml) - rekursiv `WITH` ning uch bo'lagi va iterativ bajarilishi, working table, `UNION` ning takrorlangan qatorni tashlashi, sikl uchun yo'l massivi va `ROW(...)` varianti, rekursiv bo'lmagan CTE ning inline qilinishi sharti
- ESLATMA: 24.27 dagi `s.depth < 50` chegara qiymati va Spring repozitoriy misoli shu korpusning qo'shimchasi, kitob va PostgreSQL hujjati bunday son bermaydi
- Martin Kleppmann, *Designing Data-Intensive Applications*, O'Reilly, 2017, 2-bob (53-54-betlar, `Graph Queries in SQL`) - graf so'rovida join soni oldindan ma'lum emasligi, SQL:1999 dan beri `WITH RECURSIVE` bilan o'zgaruvchan uzunlikdagi yurish va sintaksisning graf so'rov tiliga nisbatan noqulayligi
- [PostgreSQL 17, Performance Tips (perform.sgml)](https://raw.githubusercontent.com/postgres/postgres/REL_17_STABLE/doc/src/sgml/perform.sgml) - `EXPLAIN` chiqishini o'qish va planner statistikasi
- [PostgreSQL 17, Planner Cost Constants (config.sgml)](https://raw.githubusercontent.com/postgres/postgres/REL_17_STABLE/doc/src/sgml/config.sgml) - `random_page_cost` default 4, `effective_cache_size` default 4GB va u xotira ajratmasligi
- Egor Rogov, *PostgreSQL 14 Internals*, Postgres Professional, 2022, 16-bob "Query Execution Stages", 257-263-betlar - join daraxtini yassilash, `join_collapse_limit`, `from_collapse_limit`, genetik optimizator, startup va total narx
- Egor Rogov, *PostgreSQL 14 Internals*, Postgres Professional, 2022, 21-bob "Nested Loop", 359-361-betlar - `Memoize` node i, `Materialize` dan farqi, `Hits`, `Misses`, `Evictions` va `Overflows` o'qilishi
- Egor Rogov, *PostgreSQL 14 Internals*, Postgres Professional, 2022, 23-bob "Sorting and Merging", 392-401-betlar - quicksort, top-N heapsort, external merge va incremental sort
- Egor Rogov, *PostgreSQL 14 Internals*, Postgres Professional, 2022, 18-bob "Table Access Methods", 300-310-betlar - `Gather`, ishchi soni ierarxiyasi va formulasi, parallellashmaydigan so'rovlar ro'yxati
- Egor Rogov, *PostgreSQL 14 Internals*, Postgres Professional, 2022, 20-bob "Index Scans", 340-346-betlar - bitmap aniqligi, `BitmapAnd` va `BitmapOr` amallari
- Egor Rogov, *PostgreSQL 14 Internals*, Postgres Professional, 2022, 16.2-16.3-bo'limlar (262, 266-270-betlar) - kengaytirilgan so'rov protokoli, tayyorlash va parametr bog'lash, natijani bo'laklab olish, `cursor_tuple_fraction` standarti 0.1
- Egor Rogov, *PostgreSQL 14 Internals*, Postgres Professional, 2022, 17.1-17.3-bo'limlar (271-276-betlar) - `reltuples`, `relpages`, `relallvisible`, `reltuples = -1`, statistikasiz jadval uchun 10 sahifa taxmini, `null_frac`, `n_distinct` va uning manfiy shakli
- Egor Rogov, *PostgreSQL 14 Internals*, Postgres Professional, 2022, 17.4-17.7-bo'limlar (277-284-betlar) - `most_common_vals` va `most_common_freqs`, 1 kB chegarasi, `histogram_bounds` va bucket hisobi, `most_common_elems`, `avg_width`
- Egor Rogov, *PostgreSQL 14 Internals*, Postgres Professional, 2022, 17.9-bo'lim (285-287-betlar) - ifoda ustidagi selektivlik 0.5 foiz, `CREATE STATISTICS` ifoda ustida, `pg_stats_ext_exprs`, ifoda indeksi statistikasi
- Egor Rogov, *PostgreSQL 14 Internals*, Postgres Professional, 2022, 18.2-bo'lim (296-298-betlar) - seq scan narx formulasi, `seq_page_cost`, `random_page_cost`, `cpu_tuple_cost`, `cpu_operator_cost`, shishgan jadvalning narxga ta'siri
- Egor Rogov, *PostgreSQL 14 Internals*, Postgres Professional, 2022, 18.4-bo'lim (301-303-betlar) - `Parallel Seq Scan` mexanikasi, prefetch yo'qolishi, CPU bo'linib I/O bo'linmasligi, `parallel_setup_cost` 1000 va `parallel_tuple_cost` 0.1
- Egor Rogov, *PostgreSQL 14 Internals*, Postgres Professional, 2022, 18.5-bo'lim (309-312-betlar) - parallel restricted amallar, `CTE Scan`, `SubPlan` va `InitPlan`, vaqtinchalik jadvallar, `PARALLEL RESTRICTED` funksiyalar, `force_parallel_mode`
- Egor Rogov, *PostgreSQL 14 Internals*, Postgres Professional, 2022, 20.1-20.5-bo'limlar (331-349-betlar) - index scan narxi va korrelyatsiya, `cpu_index_tuple_cost` 0.005, bitmap narxi, parallel index va bitmap skan, skan usullarini selektivlik bo'yicha taqqoslash egri chizig'i
- Egor Rogov, *PostgreSQL 14 Internals*, Postgres Professional, 2022, 21.1-21.2-bo'limlar (350-366-betlar) - join turlari va usullari, dekart ko'paytma, outer join cheklovlari va kardinalligi, semi va anti join, parallel nested loop
- Egor Rogov, *PostgreSQL 14 Internals*, Postgres Professional, 2022, 22.1-22.2-bo'limlar (377-386-betlar) - parallel rejada hash join, `Parallel Hash` va `enable_parallel_hash`, `HashAggregate` va uning diskka to'kilishi
- Egor Rogov, *PostgreSQL 14 Internals*, Postgres Professional, 2022, 23.1-23.3-bo'limlar (388-404-betlar) - merge join faqat tenglik shartini qo'llashi, parallel rejada merge join, `Gather Merge` va uning narxi, `Unique`, `GroupAggregate` va `MixedAggregate`
- Martin Kleppmann, *Designing Data-Intensive Applications*, 1-nashr, O'Reilly, 2017, 2-bob (43-bet) - deklarativ so'rov tilining baza dvigateli tafsilotlarini yashirishi va shu sababli so'rovlarni o'zgartirmasdan unumdorlikni yaxshilash imkoniyati, hamda SQL natija tartibini kafolatlamasligi (baza yozuvlarni joyidan ko'chirishi mumkin)
- ESLATMA: 24.1 dagi tartib o'zgarishiga olib keladigan mexanizmlar ro'yxati (skan turi, parallel reja, `geqo`, `VACUUM`) shu korpusning qo'shimchasi

---

[&larr; 23. Indekslar: B-tree, GIN, GiST, BRIN va tanlov](23-indekslar-b-tree-gin-gist-brin-va-tanlov.md) · [Mundarija](README.md) · [25. Sxema dizayni, ma'lumot turlari va cheklovlar &rarr;](25-sxema-dizayni-malumot-turlari-va-cheklovlar.md)
