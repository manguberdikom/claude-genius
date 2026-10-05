<!-- doc: architect | chapter: 8 | part: I. Fikrlash va qarorlar -->

[Barcha hujjatlar](../../README.md) / [Arxitektor miyyasi](README.md)

# 8. Ishlash va resurs hissi: napkin math (Performance Intuition and Napkin Math)

<details>
<summary>Bu bobdagi 11 bo'lim</summary>

- [8.1 Har bir arxitektor yodda tutishi kerak bo'lgan kechikish raqamlari](#81-har-bir-arxitektor-yodda-tutishi-kerak-bolgan-kechikish-raqamlari)
- [8.2 Oddiy hisob: kuniga N so'rov nechta RPS bo'ladi, cho'qqi koeffitsienti](#82-oddiy-hisob-kuniga-n-sorov-nechta-rps-boladi-choqqi-koeffitsienti)
- [8.3 Little qonuni: parallellik, kechikish va throughput bog'liqligi](#83-little-qonuni-parallellik-kechikish-va-throughput-bogliqligi)
- [8.4 Thread pool va connection pool kattaligini hisoblash](#84-thread-pool-va-connection-pool-kattaligini-hisoblash)
- [8.5 Ma'lumot hajmini hisoblash: qator kattaligi, indeks hajmi, bir yillik o'sish](#85-malumot-hajmini-hisoblash-qator-kattaligi-indeks-hajmi-bir-yillik-osish)
- [8.6 O'rtacha emas, p95 va p99 ga qarash sababi](#86-ortacha-emas-p95-va-p99-ga-qarash-sababi)
- [8.7 Tarmoq safari soni: bitta so'rovda nechta tashqi chaqiruv bor](#87-tarmoq-safari-soni-bitta-sorovda-nechta-tashqi-chaqiruv-bor)
- [8.8 Serializatsiya, JSON va ortiqcha ma'lumot tashishning narxi](#88-serializatsiya-json-va-ortiqcha-malumot-tashishning-narxi)
- [8.9 Qachon kesh kerak emas: ma'lumotlar bazasi allaqachon yetarli](#89-qachon-kesh-kerak-emas-malumotlar-bazasi-allaqachon-yetarli)
- [8.10 O'lchovsiz optimallashtirish: taxmin qilib emas, o'lchab tuzatish](#810-olchovsiz-optimallashtirish-taxmin-qilib-emas-olchab-tuzatish)
- [8.11 Amalda qo'llash](#811-amalda-qollash)

</details>



Arxitektorni developerdan ajratadigan eng arzon ko'nikma: qog'oz burchagida hisoblash. Yuklamani, kechikishni va hajmni oldin hisoblab keyin kod yozish sprintni emas, yillarni tejaydi. Bu bobda to'lov servisi, buyurtma oqimi va ombor qoldig'i misolida aniq raqamlar bilan ishlaymiz. Maqsad formulani yodlash emas, kattalik tartibini (order of magnitude) sezish.

## 8.1 Har bir arxitektor yodda tutishi kerak bo'lgan kechikish raqamlari

Napkin math uchun aniq raqam kerak emas, kattalik tartibi kerak. Quyidagi jadval oddiy cloud muhiti uchun taxminiy qiymatlar, ularni yodlab oling.

| Operatsiya | Taxminiy kechikish | Nisbati (L1 = 1) |
|---|---|---|
| L1 cache o'qish | 1 ns | 1x |
| Main memory (RAM) tasodifiy o'qish | 80 ns | 80x |
| HashMap `get` (JVM, issiq kod) | 20-50 ns | ~30x |
| Bitta obyekt allokatsiyasi + keyingi young GC ulushi | 20-100 ns | ~50x |
| 1 KB JSON serializatsiya (Jackson) | 2-5 mcs | ~3 000x |
| NVMe SSD tasodifiy 4 KB o'qish | 100-200 mcs | ~150 000x |
| Bir xil AZ ichida tarmoq round-trip | 0.3-0.7 ms | ~500 000x |
| PostgreSQL oddiy indeks bo'yicha `SELECT` (issiq buffer) | 0.3-1 ms | ~700 000x |
| PostgreSQL `INSERT` + `COMMIT` (WAL fsync bilan) | 1-5 ms | ~3 000 000x |
| AZ'lar orasida round-trip (bir region) | 1-2 ms | ~1 500 000x |
| Region'lar orasi (masalan, Frankfurt va Virginia) | 80-100 ms | ~90 000 000x |
| Kafka'ga `acks=all` bilan yozish | 3-10 ms | ~6 000 000x |
| Tashqi HTTPS API chaqiruvi (TLS handshake bilan) | 50-300 ms | ~100 000 000x |

Xulosa: process ichidagi hisob deyarli bepul, tarmoq va disk qimmat. 10 000 marta `HashMap.get` bitta `SELECT` dan arzon, shuning uchun optimallashtirish tarmoq safarlari va fsync'lardan boshlanadi.

PostgreSQL'da `COMMIT` narxi asosan WAL'ni diskka yozishdir. `synchronous_commit = off` bilan commit 0.1 ms ga tushadi, lekin crash paytida oxirgi `wal_writer_delay` oraligidagi tranzaksiyalar yo'qoladi. Audit jurnali uchun bu yaramaydi, analitik event jadvali uchun to'g'ri savdo.

## 8.2 Oddiy hisob: kuniga N so'rov nechta RPS bo'ladi, cho'qqi koeffitsienti

Bir kunda 86 400 sekund bor. Napkin math uchun uni 100 000 deb olsa bo'ladi, xato 15 foizdan oshmaydi.

```java
// Buyurtma servisi uchun yuklama hisobi.
// Berilgan: kuniga 4 million buyurtma ko'rish so'rovi.
long kunlikSorov = 4_000_000L;
long sekundlar   = 86_400L;

double ortachaRps = (double) kunlikSorov / sekundlar;   // ~46 RPS

// Trafik sutka bo'ylab tekis emas. Amaliy koeffitsientlar:
//   B2B ichki sistema: cho'qqi = o'rtacha * 3 (ish kuni 8 soatga siqilgan)
//   ommaviy e-commerce: cho'qqi = o'rtacha * 5..8 (kechki soat 20:00-22:00)
//   aksiya yoki Black Friday: o'rtacha * 20..50
double cheqqiRps = ortachaRps * 6;                      // ~278 RPS

// Zaxira (headroom): hech qachon 100% sig'imga rejalashtirmang.
double rejaRps = cheqqiRps / 0.6;                       // ~463 RPS, 40% zaxira
```

4 million degan raqam katta ko'rinadi, lekin 46 RPS bitta Spring Boot instansiyasi uchun hech narsa emas. Arxitektor shu yerda "Kafka va sharding kerak" degan taklifni to'xtatadi. Teskari holat ham bor: kuniga 2 milliard event 23 000 RPS beradi, bu bitta PostgreSQL yozuv node'i uchun jiddiy chegara.

## 8.3 Little qonuni: parallellik, kechikish va throughput bog'liqligi

Little qonuni sig'im rejalashtirishning asosi: bir vaqtda bajarilayotgan ishlar soni (L) teng kelish tezligi (lambda) ko'paytiriladi ishning sistemada turish vaqti (W).

```java
// L = lambda * W
//   L      = bir vaqtda ishlayotgan so'rovlar soni (concurrency)
//   lambda = throughput, sekundiga so'rov (RPS)
//   W      = bitta so'rovning to'liq davomiyligi (sekund)
// Misol: to'lov servisi. Bitta so'rov o'rtacha 120 ms ishlaydi.
// Shundan: 15 ms bizning CPU, 25 ms PostgreSQL, 80 ms tashqi bank API.
double w = 0.120;          // sekund
double lambda = 400;       // kerakli RPS

double l = lambda * w;     // 48 ta so'rov bir vaqtda "havoda" turadi

// Teskari yo'nalish: 200 ta thread bor, har so'rov 120 ms.
// Nazariy maksimum throughput:
double maxRps = 200 / 0.120;   // ~1666 RPS, agar pastdagi resurs cheklamasa

// Agar tashqi bank API bir vaqtda faqat 50 ta ulanishga ruxsat bersa,
// haqiqiy chegara: 50 / 0.080 = 625 RPS. Thread sonini oshirish yordam bermaydi.
```

Amaliy xulosa: kechikish oshsa, o'sha throughput'ni saqlash uchun parallellik ham oshadi. Tashqi bank API 80 ms dan 400 ms ga sekinlashsa, 400 RPS uchun 48 emas, 160 ta so'rov bir vaqtda ushlanib turadi. Thread pool 100 ta bo'lsa, navbat o'sadi, timeout ishga tushadi va kaskad nosozlik boshlanadi. Bulkhead va timeout bo'yicha qarorlar aynan shu hisobdan kelib chiqadi.

## 8.4 Thread pool va connection pool kattaligini hisoblash

Ikki xil pool, ikki xil formula. CPU'ga bog'liq ishda thread soni yadro sonidan ko'p bo'lishi behuda, I/O kutadigan ishda esa thread soni kutish nisbatiga qarab oshadi.

```java
// 1) CPU-bound pool (masalan, hisobot aggregatsiyasi, PDF generatsiya)
int yadro = Runtime.getRuntime().availableProcessors();   // konteynerda: cpu limit
int cpuPool = yadro + 1;                                  // 8 yadro -> 9 thread

// 2) I/O-bound pool. Brian Goetz formulasi:
//    threads = yadro * targetUtilization * (1 + kutish / hisob)
// To'lov so'rovi: 15 ms CPU, 105 ms kutish (DB + bank API)
double kutish = 105, hisob = 15;
int ioPool = (int) (8 * 1.0 * (1 + kutish / hisob));      // 8 * 8 = 64 thread

// 3) Connection pool (HikariCP). Bu yerda formula BOSHQA.
// Faqat DB da o'tgan vaqtni oling: 25 ms DB, so'rovning qolgan 95 ms da
// ulanish band bo'lmasligi kerak (tranzaksiyani tashqi chaqiruv bilan bog'lamang).
// Little qonuni: L = 400 RPS * 0.025 s = 10 ta ulanish.
// Zaxira bilan: 10 / 0.7 = taxminan 15.
```

```properties
# To'lov servisi, 400 RPS, 25 ms DB vaqti, 4 instansiya.
spring.datasource.hikari.maximum-pool-size=15
spring.datasource.hikari.minimum-idle=15
# Pool bo'sh bo'lsa 2 sekunddan ko'p kutmaymiz: tez xato yaxshi.
spring.datasource.hikari.connection-timeout=2000
# Ulanishni 20 daqiqada yangilash: NAT va firewall timeout'idan oldin.
spring.datasource.hikari.max-lifetime=1200000
spring.datasource.hikari.leak-detection-threshold=10000
# Jami: 4 * 15 = 60 ulanish. PostgreSQL max_connections=200 ga sig'adi.
# Agar 4 ta servis har biri 50 so'rasa, 200 chegaradan oshadi: pgbouncer kerak.
```

Katta pool sekinlashtiradi. PostgreSQL'da har bir aktiv ulanish alohida backend process, 8 yadroli serverda 200 ta aktiv so'rov kontekst almashish va lock contention ustida vaqt yo'qotadi. 20 ta ulanish bilan umumiy throughput ko'pincha yuqori chiqadi.

## 8.5 Ma'lumot hajmini hisoblash: qator kattaligi, indeks hajmi, bir yillik o'sish

Qator kattaligini ustunlar yig'indisidan katta deb hisoblang. Har qatorda 23 baytlik tuple header, null bitmap va 8 bayt chegaraga tekislash bor, har sahifada (8 KB) item pointer uchun 4 bayt ketadi.

```sql
-- Buyurtma qatori: id bigint(8) + user_id bigint(8) + status smallint(2)
-- + amount numeric(12,2) ~ 10 + created_at timestamptz(8)
-- + idempotency_key uuid(16) = 52 bayt ma'lumot
-- + 23 bayt header + tekislash ~ 80 bayt/qator
-- Sahifaga: 8192 / (80 + 4) = taxminan 97 qator

-- Kuniga 200 000 buyurtma, bir yil:
--   200000 * 365 = 73 mln qator
--   73e6 * 80 bayt = 5.8 GB heap
--   fillfactor va o'lik qatorlar (bloat) uchun * 1.3 = taxminan 7.6 GB

-- Indekslar. B-tree yozuvi = kalit + 6 bayt TID + header, taxminan 16 bayt.
--   PK (bigint):              73e6 * 16  = 1.2 GB
--   (user_id, created_at):    73e6 * 32  = 2.3 GB
--   idempotency_key (uuid):   73e6 * 40  = 2.9 GB
-- Jami indeks 6.4 GB, jadvaldan bir xil kattalikda. Bu normal.

-- Haqiqatni tekshirish (taxmin emas, o'lchov):
SELECT pg_size_pretty(pg_relation_size('orders'))        AS heap,
       pg_size_pretty(pg_indexes_size('orders'))         AS indekslar,
       pg_size_pretty(pg_total_relation_size('orders'))  AS jami;
```

Hisob darhol qaror beradi: 14 GB jami hajm 64 GB RAM'li serverda to'liq cache'ga sig'adi, demak partitioning kerak emas. Kuniga 20 million qator kelsa bir yilda 1.4 TB chiqadi va oylik partitioning majburiy bo'ladi.

## 8.6 O'rtacha emas, p95 va p99 ga qarash sababi

O'rtacha kechikish haqiqatni yashiradi. Agar 95 foiz so'rov 10 ms da, 5 foizi 2000 ms da bajarilsa, o'rtacha 109 ms chiqadi va grafik "yaxshi" ko'rinadi. Lekin har yigirmanchi mijoz to'lov sahifasida ikki sekund kutadi.

```java
// Micrometer: faqat o'rtacha emas, taqsimot chop etilsin.
@Bean
MeterRegistryCustomizer<MeterRegistry> persentillar() {
    return registry -> registry.config().meterFilter(
        new MeterFilter() {
            @Override
            public DistributionStatisticConfig configure(
                    Meter.Id id, DistributionStatisticConfig config) {
                if (!id.getName().startsWith("payment.")) return config;
                return DistributionStatisticConfig.builder()
                        // p95/p99 ni server tomonda emas, histogram'dan hisoblash
                        .percentilesHistogram(true)
                        .serviceLevelObjectives(
                            Duration.ofMillis(50).toNanos(),
                            Duration.ofMillis(200).toNanos(),
                            Duration.ofMillis(1000).toNanos())
                        .build().merge(config);
            }
        });
}
```

Ikkinchi sabab fan-out. Bitta sahifa 20 ta servisga parallel murojaat qilsa va har birining p99 si 500 ms bo'lsa, kamida bittasi sekin chiqish ehtimoli 1 - 0.99^20 = taxminan 18 foiz. Servis darajasidagi p99 sahifa darajasida p82 ga aylanadi. Uchinchi sabab: "p99 < 300 ms" degan SLO tekshiriladi, "o'rtacha tez bo'lsin" degani esa yo'q.

Yana bir qoida: bir nechta instansiyaning p99 qiymatini o'rtachalashtirish matematik jihatdan xato. Persentil faqat xom histogram bucket'lar qo'shilgandan keyin hisoblanadi, Prometheus'da buni `histogram_quantile` qiladi.

## 8.7 Tarmoq safari soni: bitta so'rovda nechta tashqi chaqiruv bor

Kechikish manbasi ko'pincha bitta sekin so'rov emas, ketma-ket kelgan o'nlab tez so'rov. N+1 muammosi aynan shu: 50 buyurtma uchun 51 ta `SELECT`.

```java
// YOMON: ketma-ket safarlar. Kechikish qo'shiladi.
// 1 (buyurtma) + 50 (pozitsiyalar) + 1 (mijoz) + 1 (bank) = 53 safar
// 53 * 0.8 ms (DB) + 80 ms (bank) = taxminan 122 ms, bunda CPU deyarli bo'sh.

// YAXSHI: safarlar sonini kamaytirish va qolganini parallellashtirish.
var mijoz = CompletableFuture.supplyAsync(() -> mijozRepo.topish(id), pool);
var limit = CompletableFuture.supplyAsync(() -> limitClient.olish(id), pool);
// Pozitsiyalarni bitta so'rov bilan: @EntityGraph yoki join fetch
var buyurtma = buyurtmaRepo.topishPozitsiyalarBilan(buyurtmaId);
CompletableFuture.allOf(mijoz, limit).join();
// Yangi hisob: 1 + 1 + max(1 ta parallel safar) + 80 ms = taxminan 82 ms

// Java 21+ da strukturali variant (virtual thread'lar bilan):
try (var scope = new StructuredTaskScope.ShutdownOnFailure()) {
    var m = scope.fork(() -> mijozRepo.topish(id));
    var l = scope.fork(() -> limitClient.olish(id));
    scope.join().throwIfFailed();
}
```

Arxitektor har bir muhim endpoint uchun bitta raqamni biladi: safarlar soni. Uni taxmin qilish shart emas, trace bor. Jaeger yoki Zipkin'da span daraxtini ochib sanash yetarli, 8 dan ko'p ketma-ket span bo'lsa batching yoki parallellashtirish imkoni bor.

## 8.8 Serializatsiya, JSON va ortiqcha ma'lumot tashishning narxi

JSON arzon ko'rinadi, lekin hajm oshganda narx ikki joyda to'lanadi: CPU va tarmoq.

```java
// Hisobot endpoint'i: 50 000 qator, har biri 40 maydon.
// Taxminiy JSON hajmi: 50_000 * 40 * 25 bayt = 50 MB
// Jackson serializatsiya tezligi: taxminan 150-250 MB/s bitta yadroda
//   -> 50 MB / 200 MB/s = 250 ms faqat yozishga, CPU 100% band
// Mijoz tomonda parse: yana taxminan 300 ms
// 1 Gbit/s tarmoqda uzatish: 50 MB / 125 MB/s = 400 ms
// Jami taxminan 1 sekund, va 50 MB byte[] to'g'ridan-to'g'ri old gen'ga tushadi.

// Yechim 1: gzip. JSON 6-10 barobar siqiladi -> 50 MB dan 6 MB ga.
//   Qo'shimcha CPU: taxminan 30 ms. Bu juda foydali savdo.
// Yechim 2: faqat kerakli maydonlarni tanlash (projection).
//   40 maydondan 6 tasi kerak bo'lsa, hajm 50 MB dan 8 MB ga tushadi.
// Yechim 3: 50 000 qatorni umuman bitta javobda bermaslik.
//   Keyset pagination yoki fayl eksporti (CSV + S3 link).
```

Eng ko'p uchraydigan xato: entity'ni to'g'ridan-to'g'ri JSON qilib qaytarish, u ortiqcha maydonlarni va bog'lanishlarni tortib keladi. 100 qatorda sezilmaydi, 50 000 qatorda servisni yiqitadi: ro'yxat va hisobot endpoint'larida doim DTO yoki projection ishlatiladi.

## 8.9 Qachon kesh kerak emas: ma'lumotlar bazasi allaqachon yetarli

Kesh bepul emas: u invalidatsiya muammosini, nomuvofiqlik oynasini (stale window) va yangi nosozlik nuqtasini olib keladi. Shuning uchun kesh qo'shishdan oldin raqam bilan isbot kerak.

```sql
-- Oldin shuni tekshiring: ma'lumotlar bazasi allaqachon kesh.
-- shared_buffers + OS page cache = aslida sizning L2 keshingiz.
SELECT heap_blks_hit, heap_blks_read,
       round(100.0 * heap_blks_hit /
             nullif(heap_blks_hit + heap_blks_read, 0), 2) AS hit_foiz
FROM pg_statio_user_tables WHERE relname = 'ombor_qoldigi';
-- hit_foiz 99.5 bo'lsa, so'rov RAM'dan o'qiyapti: Redis 0.4 ms tarmoq
-- safarini qo'shadi, PostgreSQL esa 0.3 ms da javob beradi. Kesh ZARAR.

-- Keyin aniq raqamni ko'ring:
EXPLAIN (ANALYZE, BUFFERS)
SELECT qoldiq FROM ombor_qoldigi WHERE sku = 'A-1024' AND ombor_id = 7;
-- Execution Time: 0.21 ms, Buffers: shared hit=4
```

Kesh kerak bo'lmaydigan holatlar: so'rov 1 ms dan tez; ma'lumot tez o'zgaradi (ombor qoldig'i); o'qish soni past (kuniga 500 marta); nomuvofiqlik narxi yuqori (hisob balansi). Kesh foydali bo'ladigan holat: o'qish/yozish nisbati 100:1 dan yuqori, hisob qimmat, va bir necha sekundlik eskilik qabul qilinadi, masalan valyuta kursi yoki mahsulot katalogi.

| Vaziyat | Oddiy yondashuv | Arxitektor yondashuvi |
|---|---|---|
| Kuniga 4 mln so'rov keldi | "Kafka va sharding kerak" | 46 RPS, bitta instansiya yetadi, hisob qilib isbotlaydi |
| Sekin endpoint | Random joyga Redis qo'yadi | Trace ochadi, safarlar sonini sanaydi, N+1 ni tuzatadi |
| Thread pool sozlash | 200 qo'yadi, "ko'p yaxshi" deydi | Little qonuni bilan 64 chiqaradi, DB pool'ni alohida hisoblaydi |
| Connection pool | Har servisga 50, jami 300 | DB vaqtidan 15 chiqaradi, `max_connections` ga sig'dirib tekshiradi |
| Monitoring | O'rtacha latency grafigi | p95, p99 va histogram, fan-out ta'sirini hisoblaydi |
| Jadval o'sishi | "Keyinroq ko'ramiz" | qator kattaligi * kunlik oqim * 365, partitioning qarori bugun |
| Hisobot 50 000 qator | Entity ro'yxatini JSON qiladi | Projection + gzip, yoki CSV eksport, hajmni oldin hisoblaydi |
| Tashqi API sekinlashdi | Thread pool'ni oshiradi | Bulkhead va timeout, chegara API tomonda ekanini biladi |
| Optimallashtirish | Kodga qarab taxmin qiladi | profiler va `EXPLAIN ANALYZE` bilan o'lchab topadi |
| GC pauzasi | Heap'ni ikki barobar oshiradi | allokatsiya tezligini o'lchaydi, ortiqcha obyektni yo'qotadi |

## 8.10 O'lchovsiz optimallashtirish: taxmin qilib emas, o'lchab tuzatish

Napkin math qaysi joyni o'lchashni aytadi, lekin o'lchov o'rnini bosmaydi. Tartibi shunday: hisobla, o'lch, tuzat, yana o'lch.

```bash
# 1) Qaysi so'rov jami vaqtni yeyayotganini toping (taxmin emas, fakt).
psql -c "SELECT calls, round(mean_exec_time::numeric,2) AS ortacha_ms,
                round(total_exec_time::numeric/1000,1) AS jami_sek, query
         FROM pg_stat_statements ORDER BY total_exec_time DESC LIMIT 10;"
# Diqqat: 0.4 ms lekin 2 mln marta chaqirilgan so'rov,
# 900 ms lekin kuniga 3 marta ishlaganidan 600 barobar qimmat.

# 2) JVM tomonida: async-profiler bilan 30 sekundlik wall-clock profil.
./profiler.sh -d 30 -e wall -f /tmp/payment.html <pid>

# 3) Allokatsiya tezligi va GC. 300 MB/s dan yuqori bo'lsa, sabab izlang.
jcmd <pid> GC.heap_info
java -Xlog:gc*:file=/var/log/gc.log:time,uptime:filecount=5,filesize=20M ...

# 4) Yuklama testi. O'zgarishdan oldin va keyin bir xil skript bilan.
#    k6 yoki Gatling, p95/p99 ni solishtirish uchun.
```

Eng ko'p vaqt "bu yer sekin bo'lsa kerak" degan taxminga ketadi. Haqiqiy sabab ko'pincha boshqa joyda: ortiqcha log, `toString` ichidagi JSON, katta kolleksiyada dirty checking yoki `ThreadLocal` to'planishi. Shuning uchun har bir performance o'zgarishidan oldin bitta son yoziladi (p99 = 480 ms) va keyin qayta o'lchanadi. Son o'zgarmasa, o'zgarish bekor qilinadi.

| Tuzoq | Nega yuzaga keladi | Yechim |
|---|---|---|
| Connection pool DB sig'imidan katta | Har servis alohida sozlangan | Jami pool'ni `max_connections` ga sig'dirish, pgbouncer |
| Tranzaksiya ichida tashqi HTTP chaqiruv | `@Transactional` metodga client qo'shilgan | Chaqiruvni tranzaksiyadan tashqariga chiqarish, outbox |
| O'rtacha latency yashiradi | Dashboard faqat `mean` ko'rsatadi | Histogram va p95/p99, SLO ni persentilda yozish |
| Keraksiz kesh nomuvofiqlik keltirdi | Kesh profilaktika uchun qo'yilgan | `EXPLAIN ANALYZE` bilan isbot, 1 ms so'rovga kesh qo'ymaslik |
| N+1 faqat prod'da ko'rinadi | Test ma'lumoti 5 qator | Testda so'rov sonini tekshirish, statistikani o'lchash |
| Indeks jadvaldan katta | Har ustunga indeks qo'yilgan | Ishlatilmagan indekslarni `pg_stat_user_indexes` dan topib olib tashlash |
| Katta JSON old gen'ni to'ldiradi | Butun ro'yxat bir javobda | Pagination, streaming yoki fayl eksporti |
| Thread pool o'sishi yordam bermaydi | Chegara pastdagi resursda | Little qonuni bilan haqiqiy bottleneck'ni topish |

## 8.11 Amalda qo'llash

- [ ] Eng yuklamali 5 endpoint uchun kunlik so'rov sonini oling, RPS va cho'qqi koeffitsientini (o'rtacha * 6) hisoblab, hujjatga yozib qo'ying.
- [ ] Har bir servisning HikariCP `maximum-pool-size` qiymatini Little qonuni bilan qayta hisoblang, instansiya soniga ko'paytirib PostgreSQL `max_connections` bilan solishtiring.
- [ ] Asosiy 3 jadval uchun qator kattaligi, indeks hajmi va bir yillik o'sishni hisoblab, natijani `pg_total_relation_size` bilan tekshiring.
- [ ] Dashboard'dagi o'rtacha latency grafiklarini p95 va p99 ga almashtiring, muhim endpoint'lar uchun SLO qiymatini persentilda yozing.
- [ ] `pg_stat_statements` ni yoqib, `total_exec_time` bo'yicha top 10 so'rovni haftada bir ko'rib chiqishni jarayonga kiriting.
- [ ] Eng muhim 2 endpoint uchun trace ochib, ketma-ket tarmoq safarlari sonini sanang va 8 dan ko'p bo'lsa batching rejasini tuzing.
- [ ] 1 MB dan katta javob qaytaradigan endpoint'larni toping, gzip yoqilganini tekshirib, entity o'rniga projection ga o'tkazing.
- [ ] Mavjud har bir kesh uchun o'sha so'rovning `EXPLAIN (ANALYZE, BUFFERS)` natijasini yozib qo'ying, 1 ms dan tez bo'lsa keshni olib tashlashni taklif qiling.

---

[&larr; 7. Nosozlik haqida fikrlash](07-nosozlik-haqida-fikrlash.md) · [Mundarija](README.md) · [9. JVM ichki tuzilishi: class loading, memory model, JIT &rarr;](09-jvm-ichki-tuzilishi-class-loading-memory.md)
