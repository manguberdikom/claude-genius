<!-- doc: architect | chapter: 8 | part: I. Fikrlash va qarorlar -->

[Barcha hujjatlar](../../README.md) / [Arxitektor miyasi](README.md)

> Holat: tekshirilmoqda. Da'volar hali manbaga solishtirilmoqda.

# 8. Ishlash va resurs hissi: napkin math (Performance Intuition and Napkin Math)

<details>
<summary>Bu bobdagi 16 bo'lim</summary>

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
- [8.11 Amdahl qonuni: ketma-ket ulush masshtablanishning chegarasi](#811-amdahl-qonuni-ketma-ket-ulush-masshtablanishning-chegarasi)
- [8.12 O'sish tartibi: n ortganda narx qanday o'zgaradi (Order of Growth, Big O)](#812-osish-tartibi-n-ortganda-narx-qanday-ozgaradi-order-of-growth-big-o)
- [8.13 Amortizatsiyalangan narx: bitta operatsiya qimmat, ketma-ketlik arzon (Amortized Analysis)](#813-amortizatsiyalangan-narx-bitta-operatsiya-qimmat-ketma-ketlik-arzon-amortized-analysis)
- [8.14 Fowler ning ishlash atamalari: responsiveness, load sensitivity va efficiency](#814-fowler-ning-ishlash-atamalari-responsiveness-load-sensitivity-va-efficiency)
- [8.15 Kritik yo'l atrofida qayta loyihalash va past darajali chegara](#815-kritik-yol-atrofida-qayta-loyihalash-va-past-darajali-chegara)
- [8.16 Amalda qo'llash](#816-amalda-qollash)

</details>



Arxitektorni developerdan ajratadigan eng arzon ko'nikma: qog'oz burchagida hisoblash. Yuklamani, kechikishni va hajmni oldin hisoblab keyin kod yozish sprintni emas, yillarni tejaydi. Bu bobda to'lov servisi, buyurtma oqimi va ombor qoldig'i misolida aniq raqamlar bilan ishlaymiz. Maqsad formulani yodlash emas, kattalik tartibini (order of magnitude) sezish.

## 8.1 Har bir arxitektor yodda tutishi kerak bo'lgan kechikish raqamlari

Napkin math uchun aniq raqam emas, kattalik tartibi kerak. Lekin kattalik tartibi ham manbadan olinadi. Internetda keng tarqalgan "latency raqamlari" ro'yxati (L1 = 0.5 ns, disk seek = 10 ms va shunga o'xshash) taqdimot materialidan keladi, kitobdan emas, shuning uchun bu bobda u ishlatilmaydi. Quyida faqat shu korpusdagi kitoblar tasdiqlagan qiymatlar turadi.

| Operatsiya | Kitobdagi qiymat | Manba |
|---|---|---|
| L1 cache o'qish | bir necha CPU takti | Gregg, 6.4.1, 202-bet |
| L2 cache o'qish | o'n ikkiga yaqin takt | Gregg, 6.4.1, 202-bet |
| Main memory (DRAM) o'qish | taxminan 60 ns, 4 GHz protsessorda taxminan 240 takt | Gregg, 6.4.1, 202-bet |
| Kontekst almashish | 5 000 - 10 000 takt, zamonaviy protsessorlarda bir necha mikrosekund | Goetz, 11.3.1, 144-bet |
| PostgreSQL commit, synchronous (pgbench TPC-B, bitta klient) | o'rtacha latency 1.491 ms, 670 tps | Rogov, 11.1, 184-185-betlar |
| PostgreSQL commit, `synchronous_commit = off` | o'rtacha latency 0.485 ms, 2 060 tps | Rogov, 11.1, 185-bet |

Jadvalda SSD, availability zone orasidagi round-trip, Kafka yozuvi va tashqi HTTPS chaqiruvi yo'q: bu qiymatlar korpusdagi kitoblarda berilmagan, shuning uchun yozilmaydi. Ularni o'z muhitingizda o'lchash kerak.

Ikki uchi aniq. Main memory 60 ns va synchronous commit 1.491 ms orasida taxminan yigirma besh ming barobar farq bor: process ichidagi xotira murojaati bilan diskka sinxronizatsiya qilinadigan commit bir xil kattalik tartibida emas. Shuning uchun optimallashtirish mikro-sekundlarni emas, diskka yozish va tarmoq safarlarini sanashdan boshlanadi.

Gregg bir nechta cache darajasi hajm va kechikishning optimal kombinatsiyasini berish uchun ishlatilishini aytadi, shuningdek MMU orqali adres translyatsiyasi ham kechikish qo'shadi (6.4.1, 202-bet). Shu yerda muhim ogohlantirish ham bor: protsessoringizning cache kechikishini micro-benchmarking bilan eksperimental aniqlash kerak. Gregg buni LMbench bilan Intel Xeon E5620 2.4 GHz da o'lchab ko'rsatadi: grafikdagi pog'onalar cache darajasi oshib ketgan nuqtalarni beradi (6.4.1, 202-203-betlar).

PostgreSQL commit narxi WAL ni diskka yozishdir. Sinxron rejimda commit disk sinxronizatsiyasi tugaganini kutadi, va Rogov buning narxini ochiq aytadi: uzunroq latency va past throughput, ayniqsa OLTP yuklamasida (11.1, 183-bet). `synchronous_commit = off` bilan commit darhol qaytadi, WAL ni esa `walwriter` keyinroq yozadi. Narxi: nosozlikdan oldingi `3 x wal_writer_delay` oraligida commit qilingan ma'lumot yo'qoladi, default sozlamada bu 0.6 sekund (Rogov, 11.1, 184-bet). Audit jurnali uchun bu yaramaydi, analitik event jadvali uchun to'g'ri savdo. Yuqoridagi pgbench raqamlari bitta tizimda olingan: Rogov ning o'zi har bir tizim o'z raqamini beradi deb ogohlantiradi (11.1, 185-bet).

## 8.2 Oddiy hisob: kuniga N so'rov nechta RPS bo'ladi, cho'qqi koeffitsienti

Bir kunda 86 400 sekund bor, shuning uchun kunlik so'rov sonini RPS ga aylantirish bitta bo'lish amali. Qiyin joy bu emas, cho'qqi va sig'im.

Nygard atamalarni aniq ajratadi (8.1, 161-bet): performance tizim bitta tranzaksiyani qancha tez bajarishini o'lchaydi; throughput ma'lum vaqt oralig'ida nechta tranzaksiya bajarilishini; capacity esa berilgan workload uchun har bir tranzaksiyaning javob vaqti qabul qilinadigan darajada qolgan holda tizim ushlab turadigan maksimal throughput. Shu ta'rifdan muhim xulosa kelib chiqadi: capacity deb yozib qo'yiladigan bitta qat'iy raqam yo'q, workload o'zgarsa sig'im ham o'zgaradi (8.1, 162-bet).

```java
// Buyurtma servisi uchun yuklama hisobi.
// Berilgan: kuniga 4 million buyurtma ko'rish so'rovi.
long kunlikSorov = 4_000_000L;
double ortachaRps = (double) kunlikSorov / 86_400;   // ~46 RPS

// Cho'qqi koeffitsienti universal emas, uni o'z trafigingizdan olasiz.
// Korpusdagi yagona real o'lchov - Twitter, 2012 yil noyabr:
// tweet joylash o'rtacha 4.6k RPS, cho'qqida 12k RPS dan oshgan
// (Kleppmann, 1-bob, 11-bet). Nisbat taxminan 2.6, lekin bu
// Twitter ning raqami, sizning tizimingizning koeffitsienti emas.
double choqqiRps = ortachaRps * (12_000.0 / 4_600.0);
```

Cho'qqi raqamidan sig'imga o'tishning kitobdagi yo'li bor. Gregg sig'im rejalashtirishning oddiy usulini uch qadamda beradi (6.5.12, 223-224-betlar): maqsadli foydalanuvchi soni yoki so'rov tezligini aniqlash; har bir foydalanuvchi yoki so'rovga to'g'ri keladigan CPU sarfini ifodalash (mavjud tizimda monitoring bilan, hali yo'q tizimda yuklama generatori bilan o'lchab); CPU resursi 100 foiz utilization ga yetadigan so'rov sonini ekstrapolyatsiya qilish. Oxirgi raqam tizimning nazariy chegarasi bo'ladi.

Shu yerda eng ko'p uchraydigan xato ham aytilgan. Nygard sig'im haqidagi afsonalar ro'yxatini chiziqli ekstrapolyatsiyadan boshlaydi: "10 000 foydalanuvchini 50 foiz CPU da ushlab turgan bo'lsak, 20 000 ni ham ushlaymiz" degan savol har safar beriladi va har safar xato (8.2, 163-bet). Sabab: har bir tizimda sig'imni aynan bitta cheklov belgilaydi, va u o'z chegarasiga birinchi yetgan omil bo'ladi; cheklovga yetgandan keyin tizimning qolgan qismi ishni navbatga qo'yadi yoki tashlab yuboradi. Cheklov bo'lmagan metrika sig'imni bashorat qilish uchun befoyda (8.2, 162-163-betlar).

Shuning uchun 46 RPS yoki kuniga 2 milliard event uchun chiqadigan taxminan 23 150 RPS raqamining o'zi hech narsa aytmaydi. Keyingi savol doim bitta: bu yuklamada birinchi to'ladigan resurs qaysi. Nygard buni to'g'ridan-to'g'ri aytadi: hamma narsani qamrab oladigan bitta "sig'im raqami" beradigan formula yo'q (8.2, 163-bet).

Nygard ning o'zi bitta napkin math misolini oxirigacha olib boradi va u yodda tutishga arziydi: har bir tranzaksiyaga qo'shilgan 250 ms qo'shimcha ishlov kuniga bir million tranzaksiyada kuniga 69.4 soat CPU vaqtiga aylanadi; har bir serverda 80 foiz load factor bilan hisoblanganda bu to'rt qo'shimcha server degani (8.5, 167-168-betlar).

## 8.3 Little qonuni: parallellik, kechikish va throughput bog'liqligi

Little qonunining kitobdagi shakli shunday: barqaror tizimdagi mijozlarning o'rtacha soni ularning o'rtacha kelish tezligi va tizimda o'rtacha turish vaqti ko'paytmasiga teng (Goetz, 11.4, 145-bet, Little, 1961 ga havola bilan). Ya'ni L = lambda * W.

```java
// L = lambda * W
//   L      = bir vaqtda ishlayotgan so'rovlar soni (concurrency)
//   lambda = throughput, sekundiga so'rov (RPS)
//   W      = bitta so'rovning tizimda turish vaqti (sekund)
// Quyidagi kirish qiymatlari o'lchanmagan taxmin, misol uchun olingan:
// to'lov so'rovi o'rtacha 120 ms, kerakli yuklama 400 RPS.
double w = 0.120;
double lambda = 400;

double l = lambda * w;     // 48 ta so'rov bir vaqtda "havoda" turadi

// Teskari yo'nalish: 200 ta thread bor, har so'rov 120 ms
// (yana o'lchanmagan taxmin). Nazariy maksimum throughput:
double maxRps = 200 / 0.120;   // ~1666 RPS, agar pastdagi resurs cheklamasa
```

Formulaning amaliy ma'nosi: kechikish oshsa, o'sha throughput'ni saqlash uchun parallellik ham oshadi. Kutish vaqti uch barobar oshsa, bir vaqtda ushlanib turadigan so'rov soni ham uch barobar oshadi, va pool shuncha katta bo'lmasa navbat o'sadi. Nygard buning nochiziqli tomonini ko'rsatadi: so'rovni ishlovchi thread pool dan qancha uzoq band bo'lsa, kelayotgan so'rovning darhol bajarilmay navbatga tushish ehtimoli shuncha yuqori (8.5, 168-bet). Navbat o'sgandan keyin keyingi qadam timeout bo'ladi, shuning uchun bu hisob [timeout byudjeti](32-tarmoq-timeout-va-integratsiya-haqiqati.md#324-timeout-byudjeti-zanjirdagi-har-bir-chaqiruvga-vaqt-taqsimlash) bilan birga o'qiladi.

Teskari tomoni ham bor: thread qo'shish chegarani ko'tarmaydi, agar chegara boshqa joyda bo'lsa. Goetz buni qulf misolida aniq raqam bilan beradi: agar operatsiya qulfni 2 ms ushlab tursa va har bir operatsiya shu qulfni talab qilsa, throughput sekundiga 500 operatsiyadan oshmaydi, protsessor soni qancha bo'lsa ham; ushlash vaqtini 1 ms ga tushirish chegarani sekundiga 1 000 operatsiyaga ko'taradi (11.4.1, 145-bet). Xuddi shu mantiq tashqi resursga tegishli: agar har bir vazifa ulanish talab qilsa, thread pool ning amaldagi o'lchami connection pool o'lchami bilan cheklanadi (Goetz, 8.2, 107-bet).

## 8.4 Thread pool va connection pool kattaligini hisoblash

Ikki xil pool, ikki xil hisob. Goetz pool o'lchamini hard-code qilmaslikni va uni konfiguratsiyadan yoki `Runtime.availableProcessors` dan olishni talab qiladi, chunki to'g'ri qiymat deployment muhitiga bog'liq (8.2, 106-bet). Ikki chetning narxi ham aytilgan: pool juda katta bo'lsa threadlar tanqis CPU va xotira uchun raqobatlashadi, xotira sarfi oshadi va resurs tugashi mumkin; juda kichik bo'lsa ish bor bo'lsa ham protsessorlar bo'sh turadi va throughput tushadi (8.2, 106-bet).

```java
// 1) CPU-bound pool. Goetz: Ncpu protsessorli tizimda compute-intensive
// vazifalar uchun optimal utilization odatda Ncpu + 1 thread da chiqadi,
// chunki compute thread ham vaqti-vaqti bilan page fault oladi va
// "ortiqcha" runnable thread CPU taktini bo'sh ketishdan saqlaydi
// (Goetz, 8.2, 107-bet).
int yadro = Runtime.getRuntime().availableProcessors();
int cpuPool = yadro + 1;

// 2) I/O-bound pool. Goetz ning formulasi (8.2, 107-bet):
//    N_threads = N_cpu * U_cpu * (1 + W / C)
//      N_cpu = protsessor soni
//      U_cpu = maqsadli CPU utilization, 0 dan 1 gacha
//      W / C = kutish vaqtining hisob vaqtiga nisbati
// Nisbat aniq bo'lishi shart emas: Goetz uni profiling yoki
// instrumentation dan olishni aytadi. Quyidagi 105 va 15 ms
// o'lchanmagan taxmin, misol uchun olingan.
double kutish = 105, hisob = 15;
int ioPool = (int) (yadro * 1.0 * (1 + kutish / hisob));

// 3) Connection pool. Goetz: CPU dan boshqa resurslar uchun hisob
// oddiyroq - har bir vazifa talab qiladigan miqdorni qo'shib, mavjud
// umumiy miqdorga bo'lasiz; natija pool o'lchamining yuqori chegarasi
// bo'ladi (8.2, 107-bet). Little qonuni bilan: faqat DB da o'tgan
// vaqtni olasiz, tranzaksiyani tashqi chaqiruv bilan bog'lamaysiz.
```

Konteyner muhitida `availableProcessors` yetarli emas. Gregg CPU limit yoki quota qo'yilgan muhitlarda utilization ni fizik chegaradan tashqari qo'yilgan chegaraga nisbatan ham o'lchash kerakligini aytadi: tizim CPU quotasini fizik protsessorlar 100 foizga yetmasdan tugatib, kutilganidan erta saturation ga tushishi mumkin (6.5.2, 216-bet).

Connection pool uchun chegara ma'lumotlar bazasi tomonida. PostgreSQL har bir klient uchun alohida backend process ochadi, va Rogov bunday arxitekturaning uch narxini sanaydi (1.3, 34-35-betlar): har bir process katalog jadvallari, prepared statement va oraliq natijalarni keshlash uchun xotira talab qiladi, shuning uchun ulanish ko'paysa xotira sarfi ham ko'payadi; qisqa va tez-tez ochiladigan ulanishlarda ulanish o'rnatish va process yaratish narxi asossiz yuqori chiqadi; process soni oshgani sayin ularning ro'yxatini skanerlashga ketadigan vaqt ham oshadi, va bu operatsiya juda tez-tez bajariladi, natijada klient soni o'sishi bilan ishlash tushishi mumkin. Rogov ning yechimi: ochiladigan backend sonini chegaralaydigan connection pooling. PostgreSQL da bu built-in emas, shuning uchun application server ichidagi pool yoki tashqi vosita (PgBouncer, Odyssey) ishlatiladi; bunda bitta backend turli klientlarning tranzaksiyalarini navbatma-navbat bajaradi, demak faqat tranzaksiyaga lokal resurslardan foydalanish mumkin.

```properties
# Pool o'lchami Little qonuni bilan hisoblangan DB vaqtidan chiqadi
# (8.3 ga qarang), qolgan qiymatlar shu korpusning amaliy tavsiyasi.
spring.datasource.hikari.maximum-pool-size=15
spring.datasource.hikari.minimum-idle=15
# Pool bo'sh bo'lsa uzoq kutmaymiz: tez xato yaxshi.
spring.datasource.hikari.connection-timeout=2000
# Ulanishni NAT va firewall timeout'idan oldin yangilash.
spring.datasource.hikari.max-lifetime=1200000
spring.datasource.hikari.leak-detection-threshold=10000
```

Oxirgi tekshiruv arifmetik: instansiya soni ko'paytiriladi pool o'lchamiga, natija PostgreSQL `max_connections` ga sig'ishi kerak. Default qiymat 100 (Rogov, 12.2-bo'lim, 201-bet). Sig'masa yechim pool'ni oshirish emas, Rogov aytgan tashqi pooler.

## 8.5 Ma'lumot hajmini hisoblash: qator kattaligi, indeks hajmi, bir yillik o'sish

Qator kattaligini ustunlar yig'indisidan katta deb hisoblang va bu taxmin emas, struktura. Rogov PostgreSQL sahifasining tuzilishini beradi: page header, item pointer massivi, bo'sh joy, tuple'lar (qator versiyalari) va special space (3.1, 62-63-betlar). Sahifa o'lchami `page_header` chiqishida ko'rinadi va standart konfiguratsiyada 8 192 bayt (3.1, 62-bet). Har bir item pointer aynan to'rt bayt egallaydi va tuple'ning sahifa boshidan offsetini, uzunligini va holat bitlarini saqlaydi (3.1, 64-bet). Indeks heap tuple'ga olti baytlik tuple identifier (TID) bilan murojaat qiladi: TID main fork sahifa raqami va shu sahifadagi qator versiyasiga havoladan iborat (3.1, 64-bet).

Qator versiyasining header'i haqida Rogov ning xulosasi aniq: header katta chiqadi, va "tor" jadvalda turli metadata hajmi haqiqiy saqlanayotgan ma'lumot hajmidan oson oshib ketadi (3.2, 65-bet). Ustun tartibi ham hajmga ta'sir qiladi, chunki tekislash (alignment) majburiy. Rogov ning o'lchovi: `(boolean, integer, boolean, integer)` ustunlari bilan qator 40 bayt chiqadi, xuddi shu to'rt ustun `(integer, integer, boolean, boolean)` tartibida 34 bayt (3.2, 65-66-betlar).

```sql
-- Qator hajmini taxmin qilmang, o'lchang: pageinspect bitta qatorning
-- real uzunligini beradi (Rogov, 3.2, 65-bet).
SELECT lp_len FROM heap_page_items(get_raw_page('orders', 0));

-- Jadval va indekslarning hozirgi hajmi (Rogov, 8.1, 136-bet):
SELECT pg_size_pretty(pg_table_size('orders'))   AS jadval,
       pg_size_pretty(pg_indexes_size('orders')) AS indekslar;
```

Bir yillik o'sish shundan keyin oddiy ko'paytma bo'ladi: o'lchangan qator hajmi ko'paytiriladi kunlik qator oqimiga, ko'paytiriladi 365 ga. Indekslarni alohida sanash kerak va natija kutilganidan katta chiqishi normal: Rogov ning misolida jadval 67 MB, uning indekslari 109 MB, ya'ni indekslar jadvaldan katta (8.1, 136-bet).

Partitioning qarori shu o'lchangan raqamdan keladi, taxmindan emas. Hisob jadval ishchi to'plami buffer cache va OS cache ga sig'adimi degan savolga javob berganda qaror ham tayyor bo'ladi, va bu savol [keshning o'rni](#89-qachon-kesh-kerak-emas-malumotlar-bazasi-allaqachon-yetarli) bo'limida davom etadi.

## 8.6 O'rtacha emas, p95 va p99 ga qarash sababi

O'rtachaning yaroqsizligi va persentil ta'riflari [sifat atributlarini o'lchash](01-arxitektorning-fikrlash-modeli.md#14-sifat-atributlari-va-ularni-olchash) bo'limida yozilgan. Bu yerda napkin math uchun kerak bo'lgan to'rt qo'shimcha nuqta turadi. Javob vaqtini so'rovni tan olish vaqtidan ajratadigan atama esa boshqa: u [responsiveness](#814-fowler-ning-ishlash-atamalari-responsiveness-load-sensitivity-va-efficiency) bo'limida.

Birinchi: latency va response time bir narsa emas. Kleppmann response time ni mijoz ko'rgan vaqt deb beradi, u so'rovni ishlash vaqtidan (service time) tashqari tarmoq kechikishini va navbat kechikishini ham o'z ichiga oladi; latency esa so'rovning xizmat kutib turgan davri (1-bob, 14-bet). Hisobda ikkisini aralashtirsangiz, timeout byudjeti xato chiqadi.

Ikkinchi: persentilni qaysi raqamda yozish kerakligini biznes aytadi, grafik emas. Kleppmann Amazon misolini beradi: Amazon ichki servislar uchun talabni p999 da yozadi, chunki eng sekin so'rovlar odatda eng ko'p ma'lumotga ega mijozlarda, ya'ni eng qimmatli mijozlarda chiqadi; Amazon javob vaqtining 100 ms oshishi savdoni 1 foizga kamaytirganini kuzatgan; p9999 ni optimallashtirish esa juda qimmat va foydasi kam deb topilgan (1-bob, 15-bet). SLA ning kitobdagi shakli ham shunday: servis median javob vaqti 200 ms dan kam va p99 1 sekunddan kam bo'lsa ishlayotgan hisoblanadi, va servis vaqtning kamida 99.9 foizida ishlashi talab qilinadi (1-bob, 15-bet).

Uchinchi: yuqori persentillarning katta qismi navbatdan keladi. Server bir vaqtda kam sonli ishni bajargani uchun bir nechta sekin so'rov keyingilarini ushlab turadi (head-of-line blocking), shuning uchun javob vaqtini mijoz tomonda o'lchash kerak (Kleppmann, 1-bob, 15-16-betlar). Shu sababli yuklama testida klient oldingi so'rov tugashini kutib yangi so'rov yubormasligi kerak: kutsa navbat sun'iy qisqa bo'lib qoladi va o'lchov haqiqatdan uzoqlashadi (1-bob, 16-bet).

To'rtinchi: fan-out. Bitta foydalanuvchi so'rovi bir nechta backend chaqiruvini talab qilsa, chaqiruvlar parallel bo'lsa ham javob eng sekinini kutadi; bitta sekin chaqiruv butun so'rovni sekinlashtiradi, va backend chaqiruvlari soni oshgani sayin sekin tugaydigan foydalanuvchi so'rovlari ulushi ham oshadi. Kleppmann buni tail latency amplification deb nomlaydi (1-bob, 16-bet). Mustaqillik farazidagi o'lchanmagan taxmin bilan kattalik tartibini ko'rish mumkin: 20 ta chaqiruv va har birining p99 si bir xil bo'lsa, kamida bittasi p99 dan sekin chiqish ehtimoli 1 - 0.99^20, ya'ni taxminan 18 foiz.

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
                        // Histogram bucket'larini chop etish: persentil
                        // monitoring tizimida bucket'lardan hisoblanadi.
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

Nega server tomonda hisoblangan persentil emas, xom histogram kerak: Kleppmann persentillarni o'rtachalashni, masalan vaqt o'lchamini kamaytirish yoki bir nechta mashinaning natijasini birlashtirish uchun, matematik jihatdan ma'nosiz deb ataydi; javob vaqti ma'lumotini birlashtirishning to'g'ri yo'li histogram larni qo'shish (1-bob, 16-bet). Micrometer hujjati xuddi shuni API darajasida takrorlaydi: client-side persentillarni taglar bo'ylab birlashtirish mumkin emas, histogram asosidagi persentillarni esa bucket qiymatlarini qo'shib birlashtirish mumkin, Prometheus'da `histogram_quantile` shuni qiladi. Arzon taqribiy algoritmlar ham sanab o'tilgan: forward decay, t-digest, HdrHistogram (Kleppmann, 1-bob, 16-bet).

## 8.7 Tarmoq safari soni: bitta so'rovda nechta tashqi chaqiruv bor

Fan-out ning ta'rifi aniq: tranzaksiya ishlovchi tizimlarda u bitta kelgan so'rovga xizmat qilish uchun boshqa servislarga qilinadigan so'rovlar sonini bildiradi (Kleppmann, 1-bob, 11-bet, izoh). Shuning uchun har bir muhim endpoint uchun arxitektor bitta raqamni biladi: safarlar soni.

Kechikish manbasi ko'pincha bitta sekin so'rov emas, ketma-ket kelgan o'nlab tez so'rov. Shirazi bunga real misol keltiradi: web server loglarini o'qib IP adreslar uchun reverse lookup qiladigan programmaning birinchi versiyasi juda sekin ishlagan; tahlil reverse lookup vaqtining asosiy qismi tarmoq so'roviga ketayotganini ko'rsatgan; bu so'rovlarni ketma-ket bajarish shart emas edi, shuning uchun ikkinchi versiya lookup larni multithread qilib parallel bajardi va ancha tez ishladi (1.3-bo'lim). Tuzatish ikki qadamdan iborat: safarlar sonini kamaytirish va qolganini parallellashtirish.

```java
// Mustaqil chaqiruvlarni parallellashtirish.
var mijoz = CompletableFuture.supplyAsync(() -> mijozRepo.topish(id), pool);
var limit = CompletableFuture.supplyAsync(() -> limitClient.olish(id), pool);
// Pozitsiyalarni bitta so'rov bilan: @EntityGraph yoki join fetch
var buyurtma = buyurtmaRepo.topishPozitsiyalarBilan(buyurtmaId);
CompletableFuture.allOf(mijoz, limit).join();

// Strukturali variant. StructuredTaskScope preview API, default
// o'chirilgan; ShutdownOnFailure shutdown siyosati bitta subtask
// yiqilsa qolganini bekor qiladi (JEP 453).
try (var scope = new StructuredTaskScope.ShutdownOnFailure()) {
    var m = scope.fork(() -> mijozRepo.topish(id));
    var l = scope.fork(() -> limitClient.olish(id));
    scope.join().throwIfFailed();
}
```

Safarlar sonini taxmin qilish shart emas, trace bor: Jaeger yoki Zipkin'da span daraxtini ochib sanash yetarli. Eng ko'p uchraydigan shakl N+1: bitta ro'yxat so'rovi va har bir element uchun alohida so'rov. Uning topish usuli va yechimlari [n+1 so'rov muammosi](18-spring-data-jpa-va-hibernate-chuqur.md#184-n1-sorov-muammosi-topish-usuli-va-tort-xil-yechim) bo'limida to'liq yozilgan; napkin math uchun muhimi shu: ketma-ket safarlar kechikishni qo'shadi, parallel safarlar esa eng sekinini kutadi (8.6 dagi fan-out).

## 8.8 Serializatsiya, JSON va ortiqcha ma'lumot tashishning narxi

Qo'shimcha ishlov arzon ko'rinadi va bu eng qimmat afsona. Nygard uni alohida ajratib tanqid qiladi: mikrochip o'zi arzon bo'lishi CPU taktini arzon qilmaydi, chunki har bir CPU takti clock time yeydi, clock time esa latency; behuda ishlaydigan ilova foydalanuvchini keragidan uzoq kutadi (8.5, 167-bet). Web tizimlarda ta'sir ikki tomonlama: qo'shimcha ishlov application server yuklamasini oshiradi, va yuqorida keltirilgan hisob shundan chiqadi (har bir tranzaksiyaga 250 ms, kuniga bir million tranzaksiya, kuniga 69.4 soat CPU vaqti, 80 foiz load factor bilan to'rt qo'shimcha server). Ikkinchi tomoni ko'rinmaydi: application server javobini kutayotgan web server bo'sh turgan resurslarni ushlab turadi, kamida ikki socket, so'rov holati uchun xotira va qisman buferlangan javob uchun xotira; ya'ni application server CPU sarfi to'g'ridan-to'g'ri web server xotira sarfini oshiradi (8.5, 168-bet).

Javob hajmi va so'rov soni alohida parametr ekanini Kleppmann aniq ko'rsatadi: sekundiga 100 000 so'rovni, har biri 1 kB, ishlashga mo'ljallangan tizim bilan daqiqada 3 so'rovni, har biri 2 GB, ishlashga mo'ljallangan tizim bir xil ma'lumot throughput ida bo'lsa ham butunlay boshqacha ko'rinadi (1-bob, 18-bet). Shuning uchun hisob ikki raqamdan boshlanadi: nechta so'rov va bitta javob qancha bayt.

```java
// Hisobot endpoint'i. Quyidagi kirish qiymatlari o'lchanmagan taxmin:
// 50 000 qator, har biri 40 maydon, maydon o'rtacha 25 bayt.
// JSON hajmi: 50_000 * 40 * 25 = 50 MB
// 1 Gbit/s tarmoq 125 MB/s beradi, demak faqat uzatish 0.4 sekund.
// Serializatsiya va parse narxini o'z profilingizdan oling: bu
// korpusdagi kitoblarda Jackson uchun bayt/sekund qiymati yo'q.
```

Yechim tartibi Shirazi ning qoidasidan chiqadi: eng samarali tuning yaxshi ishlayotgan narsani o'zgartirmaslik, ikkinchi eng samaralisi esa kerak bo'lmagan ishni butunlay tashlab yuborish (1.8-bo'lim). Demak birinchi savol "qanday tezlashtiramiz" emas, "bu maydonlar kerakmi" bo'ladi. Projection yoki DTO 40 maydondan faqat kerakligini oladi; keyset pagination yoki fayl eksporti esa 50 000 qatorni bitta javobda bermaslik imkonini beradi. Entity'ni to'g'ridan-to'g'ri JSON qilib qaytarish eng yomon variant, chunki u kerak bo'lmagan maydon va bog'lanishlarni tortib keladi: Nygard aytgan "clock time" ni ham, web server xotirasini ham shu ortiqcha ma'lumot yeydi.

## 8.9 Qachon kesh kerak emas: ma'lumotlar bazasi allaqachon yetarli

Kesh invalidatsiya muammosini, nomuvofiqlik oynasini va yangi nosozlik nuqtasini olib keladi, shuning uchun uni qo'shishdan oldin dalil kerak. Dalilning birinchi qismi: ma'lumotlar bazasi allaqachon kesh. Rogov buffer cache hajmi `shared_buffers` bilan berilishini va default qiymat past ekanini aytadi, lekin shu yerda muhim qo'shimcha ham bor: PostgreSQL da cache miss har doim fizik I/O ni keltirib chiqarmaydi, chunki buffer cache kichik bo'lsa OS cache qolgan bo'sh xotiradan foydalanib vaziyatni yumshatadi (9.6, 158-159-betlar).

```sql
-- Buffer cache ishlatilishi: pg_statio_all_tables to'liq statistika
-- beradi (Rogov, 9-bob, 154-bet).
SELECT heap_blks_read, heap_blks_hit
FROM pg_statio_all_tables
WHERE relname = 'ombor_qoldigi';

-- So'rovning o'z narxi va o'qilgan bloklar:
EXPLAIN (ANALYZE, BUFFERS)
SELECT qoldiq FROM ombor_qoldigi WHERE sku = 'A-1024' AND ombor_id = 7;
```

Dalilning ikkinchi qismi: kesh qo'yiladigan joy bottleneck bo'lishi kerak. Nygard ning qoidasi bu yerda to'g'ridan-to'g'ri ishlaydi: throughput doim tizimdagi bitta cheklov bilan chegaralangan va cheklov bo'lmagan qismning performance'ini optimallashtirish throughput ni oshirmaydi (8.2, 162-bet). So'rov bottleneck bo'lmasa, kesh throughput ga hech narsa qo'shmaydi, lekin nomuvofiqlik va yangi nosozlik nuqtasini qo'shadi.

Uchinchi qism: qarorni sezgi emas, o'lchov beradi. Goetz ning ogohlantirishi aniq: ko'p developerning performance muammosi qayerda ekani yoki qaysi yondashuv tezroq bo'lishi haqidagi sezgisi ko'pincha xato, shuning uchun har bir tuning aniq performance talabi va o'lchov programmasi bilan borishi kerak; kitobdagi shior "Measure, don't guess" (11.1, 139-bet). Shirazi ham xuddi shu tomondan keladi: ishlab turgan narsaga tegmaslik eng samarali tuning (1.8-bo'lim).

Kesh hajmi haqida universal qiymat izlash ham befoyda. Rogov buffer cache uchun ochiq yozadi: optimal hajm tizimdan tizimga farq qiladi, mavjud xotira hajmi, ma'lumot profili va yuklama turiga bog'liq, va hammaga bir xil mos keladigan sehrli qiymat yoki formula yo'q; odatiy tavsiya RAM ning chorak qismidan boshlab keyin sozlash, eng yaxshi yo'l esa eksperiment (9.6, 159-bet). Ilova keshi uchun ham javob shu: o'qish va yozish nisbatini, kesh hit rate ini o'z tizimingizdan oling. Kleppmann kesh hit rate ini yuk parametrlari ro'yxatida sanaydi va parametrning to'g'ri tanlovi tizim arxitekturasiga bog'liq ekanini aytadi (1-bob, 11-bet).

| Vaziyat | Nega xato | Kitobdagi yo'l |
|---|---|---|
| Sekin endpoint'ga Redis qo'yish | cheklov qayerda ekani aniqlanmagan | cheklovni topish, cheklov bo'lmagan joyni optimallashtirish throughput ni oshirmaydi (Nygard, 8.2) |
| "Kesh har doim tezlashtiradi" | PostgreSQL ning o'zida buffer cache va OS cache bor | `pg_statio_all_tables` va `EXPLAIN (ANALYZE, BUFFERS)` bilan o'lchash (Rogov, 9-bob) |
| Kesh hajmini formula bilan tanlash | hammaga mos keladigan formula yo'q | eksperiment, RAM ning chorak qismidan boshlash (Rogov, 9.6) |
| Sezgi bilan "bu yer sekin" deyish | sezgi ko'pincha xato | "Measure, don't guess" (Goetz, 11.1) |

## 8.10 O'lchovsiz optimallashtirish: taxmin qilib emas, o'lchab tuzatish

Napkin math qaysi joyni o'lchashni aytadi, lekin o'lchov o'rnini bosmaydi. Shirazi buni talab shaklida yozadi: bottleneck sababini aniqlashga doim san'at emas, fan deb qarash kerak. Uning tartibi: profiler, benchmark va kod instrumentatsiyasi bilan o'lchash; bottleneck joyini aniqlash; sabab uchun gipoteza tuzish; gipotezani rad qilishi mumkin bo'lgan omillarni ko'rib chiqish; o'sha omilni izolyatsiya qiladigan test yasash; gipotezani tekshirish; ilovani o'zgartirish; o'zgarish performance'ni yaxshilaganini tekshirish va yaxshilanishni o'lchash, tegilgan kodni regression test bilan qoplash; keyin boshidan (1.4-bo'lim).

Nimadan boshlashni ham kitob aytadi. Shirazi uch resursni sanaydi: hamma ilovani CPU tezligi va mavjudligi, tizim xotirasi, disk va tarmoq I/O cheklaydi; birinchi qadam shu uchtadan qaysi biri ilovani sekinlashtirayotganini aniqlash (1.3-bo'lim). Keyingi bottleneck chiqishi esa normal holat: Shirazi memory muammosi tuzatilgandan keyin ilova disk-bound, keyin CPU-bound bo'lishi odatiy ekanini aytadi, shuning uchun bir vaqtda faqat asosiy bottleneck lar bilan ishlash kerak. Uning misoli ogohlantirish sifatida yaxshi: unbuffered stream sababli yuzaga kelgan disk I/O muammosi tuzatilgandan keyin jamoa keyingi bottleneck ni izlash o'rniga hamma joyga buffer qo'ya boshladi; haqiqiy keyingi bottleneck esa data-conversion qismida edi, va natijada ular katta memory-allocation muammosini yasadi (1.3-bo'lim). Tartib: top beshta bottleneck ni toping va eng tez tuzatiladiganini oling, chunki bitta bottleneck yo'qolgandan keyin ilovaning xarakteristikasi o'zgaradi; taqsimlangan ilovada esa eng yuqori bottleneck ni oling (1.4-bo'lim).

```bash
# 1) Qaysi so'rov jami vaqtni yeyayotganini toping (taxmin emas, fakt).
psql -c "SELECT calls, round(mean_exec_time::numeric,2) AS ortacha_ms,
                round(total_exec_time::numeric/1000,1) AS jami_sek, query
         FROM pg_stat_statements ORDER BY total_exec_time DESC LIMIT 10;"
# Tartib ortacha_ms bo'yicha emas, total bo'yicha: 0.4 ms lekin 2 mln
# marta chaqirilgan so'rov jami 800 sekund, 900 ms lekin kuniga 3 marta
# ishlagani esa 2.7 sekund, ya'ni taxminan 300 barobar arzon.
# (Chaqiruv sonlari o'lchanmagan taxmin, misol uchun olingan.)

# 2) JVM tomonida wall-clock profil. Shirazi: asosiy o'lchov
#    wall-clock time (1.7-bo'lim).
./profiler.sh -d 30 -e wall -f /tmp/payment.html <pid>

# 3) GC va heap holati.
jcmd <pid> GC.heap_info
java -Xlog:gc*:file=/var/log/gc.log:time,uptime:filecount=5,filesize=20M ...

# 4) Yuklama testi. O'zgarishdan oldin va keyin bir xil skript bilan.
#    Shirazi: yugurishlar orasida kichik farq doim bo'ladi, shuning
#    uchun farqni o'rtacha bilan o'lchab variance ni hisoblang
#    (1.7-bo'lim).
```

Qaysi metodologiyani qachon ishlatish kerakligi uchun Gregg tayyor tartib beradi: performance monitoring, USE metodi, profiling, micro-benchmarking, static analysis (6.5, 215-bet). USE metodi bottleneck va xatolarni chuqur strategiyalarga o'tishdan oldin topish uchun: har bir CPU uchun Utilization (CPU band bo'lgan vaqt), Saturation (navbatda o'z navbatini kutayotgan runnable threadlar darajasi) va Errors (CPU xatolari, tuzatiladiganlari ham) tekshiriladi; xatolarni birinchi ko'rish mumkin, chunki ularni tekshirish va tushunish eng oson (6.5.2, 216-bet). Tez tekshiruvlar ham sanab o'tilgan: `uptime` da load average CPU sonidan oshsa bu odatda saturation belgisi, `vmstat` da idle 10 foizdan kam bo'lsa muammo bo'lishi mumkin (6.5.1, 215-bet).

Ikki o'lchov tuzog'i alohida aytilgan. Birinchi, interval: ba'zi monitoring vositalari 5 daqiqalik interval ishlatadi va bu qisqa CPU cho'qqilarini yashiradi, shuning uchun sekundlik o'lchov afzal, lekin sekund ichida ham cho'qqi bo'lishi mumkin va u saturation dan bilinadi (Gregg, 6.5.6, 220-bet). Ikkinchi, benchmark: Gregg benchmark lar ko'pincha benchmark kodini yoki CPU tezligini emas, kompilyator versiyalari orasidagi optimizatsiyani o'lchab qo'yishini, va ko'p benchmark bitta thread da ishlagani uchun natija ko'p CPU li tizimda ma'nosini yo'qotishini aytadi (6.5.11, 223-bet). Shirazi shu fikrni vendor tomonidan beriladigan raqamlarga qo'llaydi: vendor benchmark lari ma'lum bir ilova uchun odatda befoyda, uchinchi tomon komponentini o'z ishlatish shaklingizni yaxshi simulyatsiya qiladigan benchmark bilan o'lchash kerak (1.8-bo'lim).

Shuning uchun har bir performance o'zgarishi aniq talab va aniq son bilan boshlanadi. Goetz buni shart qilib qo'yadi: tuning aniq performance talablari bilan borishi kerak, shunda qachon tuning qilish va qachon to'xtash ma'lum bo'ladi, va o'lchov real konfiguratsiya va real yuk profilida olinadi; tuning dan keyin qayta o'lchab kutilgan yaxshilanish olinganini tekshirish kerak (11.1, 139-bet). Son o'zgarmasa, o'zgarish bekor qilinadi.

| Tuzoq | Nega yuzaga keladi | Kitobdagi yechim |
|---|---|---|
| Connection pool DB sig'imidan katta | har servis alohida sozlangan | jami pool'ni `max_connections` ga sig'dirish, tashqi pooler (Rogov, 1.3) |
| Chiziqli ekstrapolyatsiya bilan sig'im aytish | cheklov aniqlanmagan | cheklovni topish, CPU/so'rov dan 100 foizga ekstrapolyatsiya (Nygard 8.2, Gregg 6.5.12) |
| O'rtacha latency yashiradi | dashboard faqat mean ko'rsatadi | histogram va yuqori persentil, SLA ni persentilda yozish (Kleppmann, 1-bob) |
| Monitoring cho'qqini yashiradi | 5 daqiqalik interval | sekundlik o'lchov, saturation ni kuzatish (Gregg, 6.5.6) |
| Thread pool o'sishi yordam bermaydi | chegara pastdagi resursda | Little qonuni va cheklov tahlili (Goetz 11.4, Nygard 8.2) |
| "Bu yer sekin bo'lsa kerak" | sezgiga ishonish | o'lchash, gipoteza, izolyatsiya qiluvchi test (Shirazi, 1.4) |
| Benchmark natijasi ko'chmaydi | bitta thread, boshqa kompilyator, vendor raqami | o'z yuk profilingizda o'lchash (Gregg 6.5.11, Shirazi 1.8) |

## 8.11 Amdahl qonuni: ketma-ket ulush masshtablanishning chegarasi

Little qonuni tizim ichidagi parallellikni hisoblaydi, Amdahl qonuni esa parallellik qancha foyda berishini aytadi. Kitobdagi shakl: agar `F` hisobning ketma-ket bajarilishi shart bo'lgan ulushi bo'lsa, `N` protsessorli mashinada tezlanish ko'pi bilan `1 / (F + (1 - F) / N)` bo'ladi; `N` cheksizlikka borganda maksimal tezlanish `1 / F` ga yaqinlashadi (Goetz, 11.2, 139-bet). Muhim xulosa `N` da emas, `F` da: ketma-ket qoladigan ulush tezlanishning yuqori chegarasini belgilaydi va `N` qancha katta bo'lsa ham u o'zgarmaydi.

| Ketma-ket ulush `F` | Cheksiz protsessorda maksimal tezlanish |
|---|---|
| 1 foiz | 100 barobar (`1 / F` chegarasidan) |
| 5 foiz | 20 barobar (`1 / F` chegarasidan) |
| 10 foiz | 10 barobar (Goetz, 11.2, 139-bet) |
| 50 foiz | 2 barobar (Goetz, 11.2, 139-bet) |

Kitob serializatsiyaning samaradorlik narxini ham beradi va bu jadvaldan ko'ra ta'sirli: 10 foiz serializatsiya bilan 10 protsessorda tezlanish ko'pi bilan 5.3 chiqadi, utilization esa 53 foiz; 100 protsessorda tezlanish ko'pi bilan 9.2, utilization 9 foiz. Ya'ni o'n barobar chegarasiga yetmasdan oldin juda ko'p samarasiz ishlatilgan CPU kerak bo'ladi (Goetz, 11.2, 139-140-betlar).

Amaliy ma'nosi: masshtablash rejasi "nechta instance qo'yamiz" savolidan emas, "ketma-ket qolgan joy qayerda" savolidan boshlanadi. Goetz asosiy aybdorni nomlaydi: concurrent ilovalarda masshtablanishga asosiy tahdid eksklyuziv resurs qulfi (11.4, 145-bet). Kitobdagi serializatsiya manbalari ro'yxati ham shu: umumiy ish navbatidan vazifa olish sinxronizatsiya talab qiladi; natijani qayta ishlash, masalan log fayliga yozish yoki umumiy natija to'plamiga qo'yish, ham serializatsiya manbasi; har bir thread o'z natija strukturasini yuritsa, oxirgi merge serializatsiya bo'ladi. Umumiy qoida shundan: istalgan umumiy ma'lumot strukturasiga murojaat programmaga serializatsiya elementini kiritadi (11.2, 140-141-betlar). Goetz ning xulosasi qisqa: hamma concurrent ilovada serializatsiya manbalari bor, o'zingizda yo'q deb o'ylasangiz yana qarang (11.2, 141-bet).

Ikkinchi xulosa o'lchovga tegishli: yuk oshganda throughput chiziqli o'smasa va kechikish o'sa boshlasa, sabab odatda yadro yetishmasligi emas, ketma-ket bo'lak. Bu [qulf raqobati](11-concurrency-thread-lock-atomic-happens.md#1115-qulf-raqobatini-kamaytirish-qamrov-bolish-striping-va-issiq-maydon) o'lchovi bilan birga o'qiladi: qaysi resurs navbat yasayotganini topmasdan qo'shilgan har bir thread faqat kontekst almashinuvini oshiradi, va uning narxi 8.1 dagi jadvalda turadi.

## 8.12 O'sish tartibi: n ortganda narx qanday o'zgaradi (Order of Growth, Big O)

Oldingi bo'limlar aniq raqam bilan ishladi: RPS, millisekund, bayt. Napkin math ning ikkinchi o'qi esa raqam emas, funksiya: kirish hajmi `n` ikki barobar oshsa narx necha barobar oshadi. CLRS buni o'sish tartibi (order of growth) deb ataydi va maqsadni aniq qo'yadi: ishlash vaqti kirish hajmi chegarasiz o'sganda qanday ortishini o'rganish, ya'ni asimptotik samaradorlik (CLRS, 3-bob, 43-bet).

Ta'rif to'plam ta'rifi. `O(g(n))` - shunday `f(n)` funksiyalar to'plami, ular uchun musbat `c` va `n0` konstantalari topiladi va hamma `n >= n0` da `0 <= f(n) <= c * g(n)` bajariladi (CLRS, 3.1, 47-bet). Ya'ni `O` konstanta ko'paytuvchi aniqligida yuqori chegara. Ikki qo'shnisi shu shaklda: `Theta` funksiyani `c1 * g(n)` va `c2 * g(n)` orasiga qisadi (asimptotik aniq chegara), `Omega` esa pastki chegara beradi (CLRS, 3.1, 45-bet, 3.1-rasm). Teorema 3.1: `f(n) = Theta(g(n))` faqat va faqat `f(n) = O(g(n))` va `f(n) = Omega(g(n))` bo'lganda (CLRS, 3.1, 48-bet).

Arxitektor uchun amaliy ma'nosi uchta.

Birinchi: katta `n` da konstantalar yo'qoladi. Yetarlicha katta kirishda aniq ishlash vaqtining ko'paytuvchi konstantalari va past tartibli hadlari kirish hajmining ta'siri ostida qolib ketadi (CLRS, 3-bob, 43-bet), shuning uchun `O(n)`, `O(n/2)` va `O(100n)` bir xil tartib (Liang, 24.2, 855-bet).

Ikkinchi: kichik `n` da teskarisi, va shuning uchun konstanta muhim. CLRS ning o'z shakli: asimptotik samaraliroq algoritm "juda kichik kirishdan boshqa hammasi uchun" eng yaxshi tanlov (3-bob, 43-bet). "Juda kichik" qayerda tugashini asimptotika aytmaydi, buni [o'lchov](#810-olchovsiz-optimallashtirish-taxmin-qilib-emas-olchab-tuzatish) aytadi. O'n elementli ro'yxat uchun `Map` qurish chiziqli izlashdan qimmat chiqishi `O` ga zid emas: `O` faqat chegarada gapiradi.

Uchinchi: tartiblar orasidagi farq foiz emas, kattalik tartibi. `n` 25 dan 50 ga, ya'ni ikki barobar oshganda:

| O'sish tartibi | `n` = 25 | `n` = 50 | o'sish |
|---|---|---|---|
| `O(1)` | 1 | 1 | 1 barobar |
| `O(log n)` | 4.64 | 5.64 | 1.21 barobar |
| `O(n)` | 25 | 50 | 2 barobar |
| `O(n log n)` | 116 | 282 | 2.43 barobar |
| `O(n^2)` | 625 | 2 500 | 4 barobar |
| `O(n^3)` | 15 625 | 125 000 | 8 barobar |

Jadval Liang ning 24.3-jadvalidan (24.4.6, 861-bet); eksponensial qator qoldirilgan. Shu farq katta `n` da nimaga aylanadi: `O(n^2)` algoritm million elementli massivda trillion operatsiya talab qiladi va bu bir necha soat bo'lishi mumkin, milliard elementda kvintillion operatsiya, ya'ni o'n yillar (Deitel, 19.2.1, 803-804-betlar). Teskari tomoni ham shunday: 1 023 elementli saralangan massivda binary search eng yomon holatda 10 solishtirish qiladi, 1 048 575 elementda 20, milliarddan ortiq elementda 30, xuddi shu milliard element uchun chiziqli izlash esa o'rtacha 500 million solishtirish qiladi (Deitel, 19.2.2, 809-bet).

Amalda bu bitta savolga aylanadi: issiq yo'ldagi narx `n` ga qanday bog'langan. Ikkita ichma-ich sikl, siklda baza so'rovi va siklda satr birlashtirish - `O(n^2)` ning uch ko'rinishi.

```java
// yomon: har bir buyurtma uchun ro'yxat bo'ylab izlash - O(n * m)
public List<Shipment> match(List<Order> orders, List<Shipment> shipments) {
    List<Shipment> matched = new ArrayList<>();
    for (Order order : orders) {
        for (Shipment shipment : shipments) {               // indexOf/contains: O(n)
            if (shipment.orderId().equals(order.id())) {
                matched.add(shipment);
            }
        }
    }
    return matched;
}

// yaxshi: bir marta indeks quriladi, izlash O(1) ga tushadi
public List<Shipment> matchIndexed(List<Order> orders, List<Shipment> shipments) {
    Map<OrderId, Shipment> byOrder = shipments.stream()
            .collect(toMap(Shipment::orderId, identity()));  // O(m)
    return orders.stream()
            .map(order -> byOrder.get(order.id()))           // hashing: O(1)
            .filter(Objects::nonNull)
            .toList();
}
```

Java to'plamlarining narxi shu til bilan yozilgan: `ArrayList.get(index)` `O(1)`, `contains` va `indexOf` `O(n)`, `addFirst` `ArrayList` da `O(n)` lekin `LinkedList` da `O(1)` (Liang, 26.1-jadval, 950-bet); hashing bilan izlash, qo'shish va o'chirish `O(1)` (Liang, 28.1, 998-bet). To'plam tanlashning toza kod tomoni [to'plam turini tanlash](../clean-code/23-toplamlar-va-generiklar-gigiyenasi.md#231-togri-toplam-turini-tanlash) bo'limida.

O'sish tartibi [Little qonuni](#83-little-qonuni-parallellik-kechikish-va-throughput-bogliqligi) va [Amdahl qonuni](#811-amdahl-qonuni-ketma-ket-ulush-masshtablanishning-chegarasi) bilan aralashmaydi: Little qonuni tizimdagi bir vaqtdagi ishlar sonini bog'laydi, Amdahl qonuni ketma-ket ulush tufayli tezlanish chegarasini beradi, o'sish tartibi esa bitta operatsiyaning narxini kirish hajmiga bog'laydi.

## 8.13 Amortizatsiyalangan narx: bitta operatsiya qimmat, ketma-ketlik arzon (Amortized Analysis)

O'sish tartibi bitta operatsiyaning narxini aytadi. Lekin ko'p to'plam shunday qurilgan: operatsiyalarning deyarli hammasi arzon, ba'zi birlari esa butun strukturani qayta quradi. Bunday holatni amortizatsiyalangan tahlil o'lchaydi: ketma-ketlikdagi hamma operatsiya bo'yicha o'rtacha olinadi va ketma-ketlik ichidagi bitta operatsiya qimmat bo'lsa ham o'rtacha narx kichik chiqishi ko'rsatiladi. CLRS muhim farqni ham qo'yadi: bu o'rtacha-holat tahlili emas, ehtimollik qatnashmaydi; amortizatsiyalangan tahlil eng yomon holatda ham har bir operatsiyaning o'rtacha narxini kafolatlaydi (CLRS, 17-bob, 451-bet).

Uch usul bor. Agregat tahlil `n` operatsiyaning umumiy narxiga `T(n)` yuqori chegara topadi, operatsiyaga o'rtacha narx esa `T(n) / n` bo'ladi. Accounting usuli har bir operatsiyaga amortizatsiyalangan narx tayinlaydi: ketma-ketlikning boshida ba'zi operatsiyalardan ortiq olinadi va bu "oldindan to'langan kredit" sifatida struktura obyektlarida saqlanadi, keyinroq o'sha kredit haqiqiy narxidan kam hisoblangan operatsiyalarni to'laydi. Potensial usuli ayni shu kreditni alohida obyektlarda emas, butun strukturaning "potensial energiyasi" sifatida yuritadi (CLRS, 17-bob, 451-bet).

Kanonik misol - dinamik jadval, ya'ni to'lganda o'zini ikkilantiradigan massiv. Jadval to'la bo'lsa `i`-qo'shish narxi `i` ga teng: bitta elementar joylashtirish va `i - 1` ta elementni ko'chirish. Eng yomon bitta operatsiya `O(n)`, sodda yuqori chegara esa `n` operatsiya uchun `O(n^2)`. Bu chegara qo'pol, chunki kengayish `i - 1` aynan ikkining darajasi bo'lganda bo'ladi: geometrik qator yig'indisi `3n` dan oshmaydi, demak bitta qo'shishning amortizatsiyalangan narxi ko'pi bilan 3 (CLRS, 17.4.1, 463-465-betlar). Accounting intuitsiyasi ham shuni beradi: har bir element uchta elementar joylashtirish uchun to'laydi - o'zini joylashtirish, kengayishda o'zini ko'chirish va bir marta ko'chirilgan boshqa elementni ko'chirish (CLRS, 17.4.1, 465-466-betlar). Faqat qo'shish bo'lsa load factor hech qachon `1/2` dan tushmaydi, ya'ni behuda joy umumiy joyning yarmidan oshmaydi (CLRS, 17.4.1, 464-bet).

Shu yerda arxitektorga kerakli tuzoq bor. "To'lganda ikkilantiraman, yarmidan kam bo'lganda ikkiga bo'laman" strategiyasi intuitiv, lekin CLRS uning narxini hisoblab beradi: `insert, delete, delete, insert, insert, ...` ketma-ketligi har safar kengayish va qisqarishni chaqiradi, har biri `Theta(n)`, va ularning soni `Theta(n)`, demak `n` operatsiyaning jami narxi `Theta(n^2)` va bitta operatsiyaning amortizatsiyalangan narxi `Theta(n)`. Yechim - kengayish va qisqarish chegaralarini ajratish: ikkilantirish to'lganda, ikkiga bo'lish esa `1/2` emas, `1/4` dan kam to'lganda (CLRS, 17.4.2, 468-bet). Bu qoida faqat massivga tegishli emas: avtomatik masshtablash, kesh sig'imi va connection pool ning o'sish-qisqarish chegarasi bir nuqtada bo'lsa, tizim shu nuqtada tebranadi.

Java'da shu mexanika uch joyda ko'rinadi. `ArrayList` sig'imi elementlar qo'shilgan sayin avtomatik oshadi, lekin `ensureCapacity` bilan uni bir marta oldin oshirish mumkin va kitob sababni ochiq aytadi: qayta allokatsiya vaqt jihatidan qimmat, shuning uchun keyingi bir nechta qayta allokatsiyaning oldini olish ishlashni yaxshilaydi (Schildt, 19-bob). `StringBuilder` va `StringBuffer` default holatda 16 belgi uchun joy oladi, `String` bilan qurilganda esa shu satr ustiga yana 16 belgi; sabab aynan shu - qayta allokatsiya qimmat va tez-tez qayta allokatsiya xotirani fragmentlaydi (Schildt, 17-bob). `HashMap` ning default sig'imi 16 va default fill ratio (load factor) 0.75; elementlar soni sig'im va fill ratio ko'paytmasidan oshsa jadval kengayadi (Schildt, 19-bob).

```java
// Hajmi oldindan ma'lum bo'lgan to'plam oldindan o'lchamlanadi:
// kengayish narxi bitta so'rovga tushmasin.
public List<OrderLine> toLines(List<OrderRow> rows) {
    List<OrderLine> lines = new ArrayList<>(rows.size());
    // 48: bitta audit yozuvining uzunligi, o'lchanmagan taxmin
    StringBuilder audit = new StringBuilder(rows.size() * 48);
    for (OrderRow row : rows) {
        lines.add(new OrderLine(row.sku(), row.quantity()));
        audit.append(row.sku()).append('=').append(row.quantity()).append(';');
    }
    auditLog.write(audit.toString());
    return lines;
}
```

Arxitektura xulosasi bitta: amortizatsiyalangan `O(1)` o'rtachani kafolatlaydi, lekin kengayish tushgan aynan o'sha so'rov to'liq `O(n)` ni to'laydi, va u o'rtacha latency da emas, [p99 da](#86-ortacha-emas-p95-va-p99-ga-qarash-sababi) ko'rinadi. Shuning uchun katta va kattaligi oldindan ma'lum to'plam oshkor sig'im bilan quriladi, va shu sabab [kesh](#89-qachon-kesh-kerak-emas-malumotlar-bazasi-allaqachon-yetarli) hamda buffer o'lchamini sozlashda ham amal qiladi.

## 8.14 Fowler ning ishlash atamalari: responsiveness, load sensitivity va efficiency

Ishlash haqidagi suhbat ko'pincha atama ustida buziladi. Fowler buni ochiq aytadi: ko'p atama izchilsiz ishlatiladi, eng ko'p jabr ko'rgani esa "scalability", u muntazam yarim o'nta turli ma'noda qo'llanadi (Fowler, *Patterns of Enterprise Application Architecture*, Addison-Wesley, 2003, Kirish, 7-bet). Korpusda javob vaqti, latency, throughput, capacity va scalability [napkin math kechikish raqamlari](#81-har-bir-arxitektor-yodda-tutishi-kerak-bolgan-kechikish-raqamlari) va [o'rtacha emas, p95 va p99](#86-ortacha-emas-p95-va-p99-ga-qarash-sababi) bo'limlarida ishlatiladi; Fowler ning ro'yxatidan uchtasi esa korpusda yo'q edi va ularning har biri boshqa qarorni boshqaradi.

**Responsiveness** tizim so'rovni qanchalik tez tan olishi haqida, uni bajarishi haqida emas. Bu ko'p tizimda muhim, chunki javob vaqti yaxshi bo'lsa ham responsiveness past bo'lsa foydalanuvchi asabiylashadi. Tizim butun so'rov davomida kutib tursa, responsiveness va javob vaqti bir xil bo'ladi; so'rovni olganingizni tugatishdan oldin bildirsangiz, responsiveness yaxshilanadi. Fowler ning misoli: fayl ko'chirish paytidagi progress bar interfeysning responsiveness ini oshiradi, javob vaqtini esa oshirmaydi (7-bet). Xulosa ham bor: foydalanuvchi nuqtai nazaridan responsiveness javob vaqtidan muhimroq bo'lishi mumkin, shuning uchun javob vaqti yoki throughput hisobidan responsiveness ni yaxshilash ishlashni oshiradi (8-bet).

```java
// Responsiveness: so'rovni tan olishni uni bajarishdan ajratish.
// Hisobot 40 sekund tayyorlanadi, lekin javob darhol qaytadi.
@PostMapping("/reports")
ResponseEntity<Void> requestReport(@RequestBody @Valid ReportRequest body) {
    UUID id = reports.enqueue(body);          // faqat navbatga yozadi
    return ResponseEntity.accepted()          // 202, bajarilgan emas
            .location(URI.create("/reports/" + id))
            .build();
}
```

Bu yerda o'lchov ikkiga bo'linadi: 202 ni qaytarish vaqti responsiveness, hisobot tayyor bo'lgan vaqt esa javob vaqti. Ikkisini bitta metrikaga qo'shsangiz, navbat uzayganini ko'rmaysiz.

**Load sensitivity** javob vaqtining yuk bilan qanday o'zgarishi. Avval yuk ta'riflanadi: Fowler da load tizim qancha bosim ostida ekanining ifodasi, masalan hozir ulangan foydalanuvchi soni, va u odatda boshqa o'lchov uchun kontekst bo'ladi ("bu so'rovning javob vaqti 10 foydalanuvchida 0.5 sekund, 20 foydalanuvchida 2 sekund") (8-bet). Load sensitivity shu bog'liqlikning o'zi, va uning farqi kitobning misolida ko'rinadi:

| Tizim | 10 foydalanuvchi | 20 foydalanuvchi | Load sensitivity |
|---|---|---|---|
| A | 0.5 s | 0.5 s | past |
| B | 0.2 s | 2 s | yuqori, ya'ni degradatsiyasi kuchli |

Fowler degradatsiya atamasini aynan shu farq uchun ishlatadi: B tizimi A dan ko'proq degradatsiya qiladi (8-bet). Amaliy xulosa: bitta yuk darajasida o'lchangan benchmark B ni tanlaydi, chunki u past yukda tezroq. Tanlovni to'g'ri qilish uchun o'lchov kamida ikki yuk darajasida olinadi, va yuk oshirilganda qaysi birining egri chizig'i tikroq ko'tarilgani qaraladi.

**Efficiency** ishlashni resursga bo'lgan qiymat. Fowler ning misoli: ikki CPU da 30 tps beradigan tizim to'rt bir xil CPU da 40 tps beradigan tizimdan samaraliroq (8-bet). Bu capacity dan boshqa savolga javob beradi: capacity "qancha ko'taradi" deydi, efficiency "qancha pulga ko'taradi" deydi. Shuning uchun xarajat suhbatida throughput yolg'iz keltirilmaydi, u resurs soniga bo'linadi.

Fowler atama ro'yxatining oldiga bitta shart qo'yadi va u bu bobdagi hamma raqamga tegishli: ishlash haqidagi har qanday maslahat sizning konfiguratsiyangizda o'lchanmaguncha fakt deb qabul qilinmaydi, va konfiguratsiyadagi sezilarli o'zgarish (JVM versiyasi, apparat, baza) ishlash haqidagi har qanday faktni bekor qilishi mumkin, shuning uchun optimizatsiyalar qaytadan tekshiriladi; ba'zan o'tmishda yordam bergan optimizatsiya yangi muhitda zarar keltirayotgani aniqlanadi (7-bet). Shu talabning amaliy shakli [o'lchovsiz optimallashtirish](#810-olchovsiz-optimallashtirish-taxmin-qilib-emas-olchab-tuzatish) bo'limida.

## 8.15 Kritik yo'l atrofida qayta loyihalash va past darajali chegara

O'lchov sekin joyni ko'rsatgandan keyin birinchi tanlov tuzatishning darajasi bo'ladi. Ousterhout tartibni aniq qo'yadi: eng yaxshi yo'l fundamental o'zgarish, masalan kesh kiritish yoki boshqa algoritmik yondashuvga o'tish (ro'yxat o'rniga balanslangan daraxt); fundamental tuzatish topilsa, u oddiy dizayn usullari bilan amalga oshiriladi (Ousterhout, *A Philosophy of Software Design*, 1-nashr, Yaknyam Press, 2018, 20.3). Fundamental tuzatish yo'q bo'lsa, mavjud kodni tezroq ishlashi uchun qayta loyihalash qoladi, va kitob buni oxirgi chora deb ataydi.

Usulning o'zi teskari tartibda ishlaydi: mavjud koddan boshlamaydi, ideal koddan boshlaydi.

- Savol: oddiy holatda vazifani bajarish uchun bajarilishi SHART bo'lgan eng kichik kod qanday. Mavjud kod strukturasi hisobga olinmaydi.
- Ideal kod bitta metod sifatida tasavvur qilinadi: hozir kritik yo'lda bir nechta metod chaqiruvi bo'lsa ham.
- Faqat kritik yo'lga kerak bo'lgan ma'lumot olinadi va unga eng qulay ma'lumot strukturasi tanlanadi; bir nechta o'zgaruvchini bitta qiymatga birlashtirish ham shu yerda ko'riladi.
- Chiqqan kod "ideal" deb ataladi. U mavjud sinf strukturasi bilan ziddiyatga tushishi va amaliy bo'lmasligi mumkin, lekin u maqsad: kod bo'lishi mumkin bo'lgan eng sodda va eng tez holat.
- Keyin idealga iloji boricha yaqin, lekin toza strukturaga ega yangi dizayn qidiriladi. Toza abstraksiya uchun idealga bir oz kod qo'shish mumkin, masalan umumiy maqsadli hash jadvaliga qo'shimcha metod chaqiruvi (20.3).

Eng muhim qadam esa alohida: maxsus holatlarni kritik yo'ldan chiqarish. Kod sekin bo'lishining tez-tez uchraydigan sababi shu: u har xil vaziyatni ko'tarishi kerak va struktura shu vaziyatlarni qulay ko'tarish uchun qurilgan, har bir maxsus holat esa kritik yo'lga qo'shimcha shart yoki metod chaqiruvi qo'shadi. Ideal shakl shunday: boshida bitta `if` hamma maxsus holatni bitta tekshiruvda aniqlaydi, oddiy holatda faqat shu tekshiruv bajariladi, maxsus holat chiqsa esa kod yo'ldan chetga, alohida joyga tarmoqlanadi. Maxsus holat uchun ishlash muhim emas, shuning uchun u ishlash uchun emas, soddalik uchun tuziladi (20.3).

```java
// Kritik yo'l: hamma oddiy buyurtmada bajariladigan eng kichik kod.
// Maxsus holatlar boshidagi bitta tekshiruv bilan yo'ldan chiqariladi.
public BigDecimal total(Order order) {
    if (order.hasDiscount() || order.isMultiCurrency() || order.isPartial()) {
        return slowPath(order);        // sodda bo'lsin, tez bo'lishi shart emas
    }
    BigDecimal sum = BigDecimal.ZERO;
    for (OrderLine line : order.lines()) {
        sum = sum.add(line.price().multiply(line.quantity()));
    }
    return sum;
}
```

Qayta loyihalash qayerda to'xtashi kerakligini Martin belgilaydi, va uning da'vosi tor: ishlash albatta arxitektura masalasi, lekin ma'lumot saqlashga kelganda u biznes qoidalaridan butunlay ajratib, o'z ichiga yopib qo'yiladigan masala. Ma'lumotni saqlovchidan tez olish va tez yozish kerak, lekin bu past darajali tashvish va u past darajali ma'lumotga kirish mexanizmlari bilan hal qilinadi; tizimning umumiy arxitekturasiga uning aloqasi yo'q (Martin, *Clean Architecture*, Prentice Hall, 2018, 30-bob). Bu korpusdagi "ishlash arxitektura masalasi" qarashiga zid emas, uning qamrovini aniqlashtiradi: indeks qo'shish, batch qilish, kesh yoki o'qish uchun denormalizatsiyalangan model repository chegarasining ichida qoladi va domen modelining shaklini o'zgartirmaydi. Agar tezlik uchun domen modelini buzish taklif qilinayotgan bo'lsa, demak chegara noto'g'ri joyda; chegara o'rni [sxema chegarasi](05-abstraksiya-hissi-bogliqlik-va-chegaralar.md#59-sxema-chegarasi-boshqa-servisning-jadvaliga-tegmaslik-qoidasi) bo'limida.

## 8.16 Amalda qo'llash

- [ ] Eng yuklamali 5 endpoint uchun kunlik so'rov sonini oling va RPS ga aylantiring; cho'qqi koeffitsientini kitobdan emas, o'z monitoring ma'lumotingizdan chiqarib hujjatga yozib qo'ying.
- [ ] Shu endpoint'lar uchun Gregg ning uch qadamini bajaring: so'rov tezligini aniqlash, bitta so'rovga to'g'ri keladigan CPU sarfini o'lchash, 100 foiz utilization ga ekstrapolyatsiya qilish.
- [ ] Har bir servisning HikariCP `maximum-pool-size` qiymatini DB da o'tgan vaqtdan Little qonuni bilan qayta hisoblang, instansiya soniga ko'paytirib `max_connections` bilan solishtiring; sig'masa tashqi pooler rejasini yozing.
- [ ] CPU limit qo'yilgan konteynerlarda utilization ni fizik CPU emas, qo'yilgan quota ga nisbatan o'lchayotganingizni tekshiring.
- [ ] Asosiy 3 jadval uchun qator hajmini `heap_page_items` bilan o'lchab, kunlik oqimga va 365 ga ko'paytiring; natijani `pg_table_size` va `pg_indexes_size` bilan solishtiring.
- [ ] Dashboard'dagi o'rtacha latency grafiklarini histogram va yuqori persentilga almashtiring; SLA matnini median va p99 shaklida yozing.
- [ ] Yuklama test skriptini tekshiring: klient oldingi javobni kutib yangi so'rov yubormasligi kerak, aks holda navbat sun'iy qisqa chiqadi.
- [ ] Eng muhim 2 endpoint uchun trace ochib ketma-ket tarmoq safarlari sonini sanang; mustaqil chaqiruvlarni parallellashtirish yoki bitta so'rovga yig'ish rejasini tuzing.
- [ ] Katta javob qaytaradigan endpoint'larni toping: javob hajmini qator soni va maydon hajmidan hisoblab, entity o'rniga projection yoki eksportga o'tkazing.
- [ ] Mavjud har bir kesh uchun o'sha so'rovning `EXPLAIN (ANALYZE, BUFFERS)` va `pg_statio_all_tables` natijasini yozib qo'ying; kesh cheklov bo'lmagan joyda turgan bo'lsa olib tashlashni taklif qiling.
- [ ] Tizimdagi ketma-ket qoladigan joylarni (umumiy qulf, umumiy navbat, log yoki natija to'plami, yakuniy merge) ro'yxatlab, har biri uchun `F` ulushini taxmin qilib `1 / F` chegarasini hisoblang.
- [ ] Eng yuklamali endpoint'lar kodida ichma-ich sikl, siklda baza so'rovi va siklda satr birlashtirishni toping: har biri uchun `n` ni nomlang va narx `n` ga qanday bog'langanini bitta jumlada yozib qo'ying.
- [ ] Kattaligi oldindan ma'lum `ArrayList`, `HashMap` va `StringBuilder` larni oshkor sig'im bilan qurilganini tekshiring; kengayish narxi p99 ga tushib turgan joylarni o'lchovdan toping.

## Manbalar

- Brendan Gregg, *Systems Performance: Enterprise and the Cloud*, Prentice Hall, 2014, 6.4.1-bo'lim (202-203-betlar) - L1 cache bir necha takt, L2 o'n ikkiga yaqin takt, main memory taxminan 60 ns va 4 GHz da taxminan 240 takt; MMU translyatsiyasi ham kechikish qo'shadi; cache kechikishini micro-benchmarking bilan o'lchash (LMbench, Intel Xeon E5620 2.4 GHz)
- Brendan Gregg, *Systems Performance*, Prentice Hall, 2014, 6.5-6.5.2-bo'limlar (215-216-betlar) - metodologiya tartibi (performance monitoring, USE, profiling, micro-benchmarking, static analysis); USE metodining uch o'lchovi utilization, saturation, errors; load average CPU sonidan oshsa saturation, `vmstat` idle 10 foizdan kam bo'lsa muammo; CPU quota fizik 100 foizga yetmasdan tugashi
- Brendan Gregg, *Systems Performance*, Prentice Hall, 2014, 6.5.6, 6.5.11 va 6.5.12-bo'limlar (220, 223-224-betlar) - 5 daqiqalik monitoring intervali cho'qqini yashiradi, sekundlik o'lchov afzal; benchmark ko'pincha kompilyator optimizatsiyasini o'lchaydi va bitta thread natijasi ko'p CPU da ma'nosini yo'qotadi; sig'im rejalashtirishning uch qadami
- Martin Kleppmann, *Designing Data-Intensive Applications*, O'Reilly, 2017, 1-bob (11, 13-18-betlar) - yuk parametrlari va Twitter 2012 (tweet joylash 4.6k RPS o'rtacha, 12k RPS dan oshgan cho'qqi, home timeline 300k RPS), fan-out ning ta'rifi, latency va response time farqi, p999 da yozilgan Amazon talabi va 100 ms uchun 1 foiz savdo, SLA ning median va p99 shakli, head-of-line blocking va mijoz tomonda o'lchash, yuklama generatori qoidasi, tail latency amplification, persentillarni o'rtachalashning ma'nosizligi va histogram qo'shish, forward decay / t-digest / HdrHistogram, 100 000 x 1 kB va 3 x 2 GB tizimlarining farqi
- Brian Goetz va boshqalar, *Java Concurrency in Practice*, Addison-Wesley Professional, 8.2-bo'lim (106-107-betlar) - pool o'lchamini hard-code qilmaslik va `Runtime.availableProcessors`; juda katta va juda kichik pool narxi; compute-intensive uchun Ncpu + 1; `N_threads = N_cpu * U_cpu * (1 + W / C)` formulasi va uning uchta kattaligi; boshqa resurslar uchun yuqori chegara hisobi; thread pool o'lchamining connection pool bilan chegaralanishi
- Brian Goetz va boshqalar, *Java Concurrency in Practice*, Addison-Wesley Professional, 11.1-11.2-bo'limlar (138-141-betlar) - "Measure, don't guess", aniq performance talabi va real yuk profilida o'lchov; Amdahl qonuni `1 / (F + (1 - F) / N)` va `1 / F` chegarasi, 50 foiz uchun 2 barobar va 10 foiz uchun 10 barobar, 10 protsessorda 5.3 (53 foiz utilization) va 100 protsessorda 9.2 (9 foiz utilization); serializatsiya manbalari va "yana qarang" xulosasi
- Brian Goetz va boshqalar, *Java Concurrency in Practice*, Addison-Wesley Professional, 11.3.1 va 11.4-11.4.1-bo'limlar (144-145-betlar) - kontekst almashish narxi 5 000 - 10 000 takt, bir necha mikrosekund; Little qonunining matni (barqaror tizimdagi o'rtacha mijoz soni = o'rtacha kelish tezligi x tizimda turish vaqti, Little, 1961); eksklyuziv qulf masshtablanishga asosiy tahdid; 2 ms qulf 500 ops/s, 1 ms qulf 1 000 ops/s chegarasi
- Michael T. Nygard, *Release It! Design and Deploy Production-Ready Software*, 1-nashr, Pragmatic Bookshelf, 2007, 8.1-8.2-bo'limlar (161-164-betlar) - performance, throughput, scalability va capacity ta'riflari; qat'iy "sig'im raqami" yo'qligi; throughput ni bitta cheklov chegaralashi va cheklov bo'lmagan qismni optimallashtirishning foydasizligi; chiziqli ekstrapolyatsiya afsonasi
- Michael T. Nygard, *Release It!*, 1-nashr, 2007, 8.5-bo'lim (167-168-betlar) - "CPU is cheap" afsonasi, CPU takti clock time va latency ekani; 250 ms x kuniga 1 mln tranzaksiya = kuniga 69.4 soat CPU va 80 foiz load factor bilan to'rt qo'shimcha server; thread uzoq band bo'lsa navbatga tushish ehtimoli oshishi; kutayotgan web server ushlab turgan socket va xotira
- Egor Rogov, *PostgreSQL 14 Internals*, Postgres Professional, 2022, 1.3-bo'lim (34-35-betlar) va 12.2-bo'lim (201-bet) - har bir klient uchun alohida backend process, ulanish ko'paygandagi xotira narxi, qisqa ulanishlarning narxi, process ro'yxatini skanerlash va klient soni o'sishi bilan ishlashning tushishi; connection pooling va PgBouncer / Odyssey; tranzaksiyaga lokal resurslar sharti; `max_connections` default 100
- Egor Rogov, *PostgreSQL 14 Internals*, Postgres Professional, 2022, 3.1-3.2-bo'limlar (62-66-betlar) - sahifa tuzilishi, 8 192 baytlik sahifa, item pointer aynan to'rt bayt, olti baytlik TID, qator header'i katta va "tor" jadvalda metadata ma'lumotdan oshib ketishi, tekislash va ustun tartibining ta'siri (40 bayt va 34 bayt)
- Egor Rogov, *PostgreSQL 14 Internals*, Postgres Professional, 2022, 8.1-bo'lim (136-bet) va 9-bob (154, 158-159-betlar) - `pg_table_size` va `pg_indexes_size` bilan o'lchash, indeks jadvaldan katta chiqishi (67 MB va 109 MB); `pg_statio_all_tables` va `heap_blks_hit` / `heap_blks_read`; `shared_buffers`, cache miss har doim fizik I/O emasligi, optimal hajm uchun sehrli formula yo'qligi va eksperiment tavsiyasi
- Egor Rogov, *PostgreSQL 14 Internals*, Postgres Professional, 2022, 11.1-bo'lim (182-185-betlar) - sinxron commit disk sinxronizatsiyasini kutishi va uning latency / throughput narxi; `synchronous_commit = off` da `3 x wal_writer_delay` oraligidagi ma'lumot yo'qolishi (default 0.6 sekund); pgbench o'lchovi 1.491 ms / 670 tps va 0.485 ms / 2 060 tps
- Jack Shirazi, *Java Performance Tuning*, 2-nashr, O'Reilly, 2003, 1.3, 1.4, 1.7 va 1.8-bo'limlar - faqat metodologiya uchun: uch cheklovchi resurs (CPU, xotira, disk va tarmoq I/O), bottleneck ketma-ket almashishi va buffer ni hamma joyga qo'yish xatosi, reverse lookup ni parallellashtirish misoli, bottleneck ni fan sifatida aniqlashning to'qqiz qadami, top beshta bottleneck tartibi, wall-clock time va variance, kerak bo'lmagan ishni tashlash, vendor benchmark larining foydasizligi
- JEP 453: Structured Concurrency (Preview) - `StructuredTaskScope` preview API ekani va default o'chirilgani, `ShutdownOnFailure` shutdown siyosati bitta subtask yiqilganda qolganini bekor qilishi
- Micrometer hujjati, "Histograms and percentiles" - `percentilesHistogram` / `publishPercentileHistogram` va `serviceLevelObjectives` kalitlari; client-side persentilni taglar bo'ylab birlashtirib bo'lmasligi, histogram bucket'larini esa qo'shib birlashtirish mumkinligi, Prometheus'da `histogram_quantile`
- Thomas H. Cormen, Charles E. Leiserson, Ronald L. Rivest, Clifford Stein, *Introduction to Algorithms*, 3-nashr, MIT Press, 2009, 3-bob va 3.1-bo'lim (43-48-betlar) - o'sish tartibi va asimptotik samaradorlikning ta'rifi; konstantalar va past tartibli hadlar katta kirishda yo'qolishi; asimptotik samaraliroq algoritm juda kichik kirishdan boshqa hammasi uchun afzal bo'lishi; `O`, `Theta` va `Omega` ning rasmiy ta'riflari va 3.1-teorema
- Thomas H. Cormen, Charles E. Leiserson, Ronald L. Rivest, Clifford Stein, *Introduction to Algorithms*, 3-nashr, MIT Press, 2009, 17-bob (451-bet) - amortizatsiyalangan tahlilning ta'rifi va o'rtacha-holat tahlilidan farqi; agregat tahlil, accounting usuli va potensial usuli
- Thomas H. Cormen, Charles E. Leiserson, Ronald L. Rivest, Clifford Stein, *Introduction to Algorithms*, 3-nashr, MIT Press, 2009, 17.4.1-17.4.2-bo'limlar (463-468-betlar) - dinamik jadvalning ikkilantirish bilan kengayishi, bitta operatsiyaning eng yomon narxi `O(n)` va sodda `O(n^2)` chegarasi, jami narx `3n` dan oshmasligi va amortizatsiyalangan narx ko'pi bilan 3 bo'lishi; faqat qo'shishda load factor `1/2` dan tushmasligi; `1/2` chegarasida qisqartirish `Theta(n^2)` ga olib kelishi va `1/4` chegarasi
- Paul Deitel va Harvey Deitel, *Java How to Program*, 9-nashr, Pearson, 19.2.1-19.2.2-bo'limlar (803-804, 809-betlar) - `O(1)`, `O(n)` va `O(n^2)` ning amaliy ta'riflari; `O(n^2)` algoritm million elementda trillion operatsiya (bir necha soat) va milliard elementda kvintillion operatsiya (o'n yillar); binary search 1 023 elementda 10, 1 048 575 elementda 20, milliarddan ortiq elementda 30 solishtirish, chiziqli izlash esa milliard elementda o'rtacha 500 million solishtirish
- Y. Daniel Liang, *Introduction to Java Programming*, 9-nashr, Pearson, 2013, 24.2 va 24.4.6-bo'limlar (855, 861-862-betlar) - ko'paytuvchi konstantaning o'sish tartibiga ta'sir qilmasligi (`O(n) = O(n/2) = O(100n)`); 24.3-jadval: `n` 25 dan 50 ga oshganda o'sish koeffitsientlari va tartiblar ketma-ketligi
- Y. Daniel Liang, *Introduction to Java Programming*, 9-nashr, Pearson, 2013, 26.1-jadval (950-bet) va 28.1-bo'lim (998-bet) - `ArrayList` va `LinkedList` metodlarining murakkabligi (`get(index)` `O(1)` va `O(n)`, `addFirst` `O(n)` va `O(1)`, `contains` / `indexOf` `O(n)`); hashing bilan izlash, qo'shish va o'chirish `O(1)`
- Herbert Schildt, *Java The Complete Reference*, 11-nashr, McGraw-Hill, 2019, 17 va 19-boblar - `StringBuffer` default holatda 16 belgiga joy olishi va `String` bilan qurilganda yana 16 belgi, sababi qayta allokatsiyaning qimmatligi va xotira fragmentatsiyasi; `ArrayList` sig'imining avtomatik o'sishi va `ensureCapacity` bilan oldindan oshirish; `HashMap` ning default sig'imi 16, default fill ratio 0.75 va kengayish sharti
- Martin Fowler, *Patterns of Enterprise Application Architecture*, Addison-Wesley, 2003, Kirish (7-8-betlar) - "scalability" atamasining izchilsiz ishlatilishi; responsiveness ning javob vaqtidan farqi va progress bar misoli; responsiveness ni javob vaqti yoki throughput hisobidan oshirish ishlashni oshirishi; load ning ta'rifi va boshqa o'lchov uchun kontekst bo'lishi; load sensitivity va degradatsiya (0.5 s / 0.5 s va 0.2 s / 2 s misoli); efficiency ning ta'rifi (ikki CPU da 30 tps va to'rt CPU da 40 tps); ishlash haqidagi maslahat o'lchanmaguncha fakt emasligi va konfiguratsiya o'zgarishi faktni bekor qilishi
- John Ousterhout, *A Philosophy of Software Design*, 1-nashr, Yaknyam Press, 2018, 20.3 - fundamental tuzatish (kesh, boshqa algoritm) birinchi tanlov bo'lishi va kritik yo'lni qayta loyihalash oxirgi chora bo'lishi; "ideal" kodni mavjud strukturadan qat'i nazar tasavvur qilish qadamlari; maxsus holatlarni boshidagi bitta tekshiruv bilan kritik yo'ldan chiqarish va maxsus holat kodini soddalik uchun tuzish
- Robert C. Martin, *Clean Architecture*, Prentice Hall, 2018, 30-bob - ishlash arxitektura masalasi bo'lishi, lekin ma'lumot saqlash tezligi biznes qoidalaridan ajratib yopiladigan past darajali tashvish ekani
- ESLATMA: 8.4 dagi `connection-timeout`, `max-lifetime` va `leak-detection-threshold` qiymatlari, 8.16 dagi tekshiruv ro'yxatining tartibi shu korpusning amaliy tavsiyasi, kitobdan olingan emas
- ESLATMA: 8.14 dagi 202 bilan javob qaytaradigan `requestReport` misoli va 8.15 dagi `total` misoli shu korpusning Java tarjimasi: Fowler va Ousterhout bu kodni bermaydi

---

[&larr; 7. Nosozlik haqida fikrlash](07-nosozlik-haqida-fikrlash.md) · [Mundarija](README.md) · [9. JVM ichki tuzilishi: class loading, memory model, JIT &rarr;](09-jvm-ichki-tuzilishi-class-loading-memory.md)
