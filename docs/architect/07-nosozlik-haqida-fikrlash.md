<!-- doc: architect | chapter: 7 | part: I. Fikrlash va qarorlar -->

[Barcha hujjatlar](../../README.md) / [Arxitektor miyasi](README.md)

> Holat: tekshirilgan (2026-10-19). Manbalar bob oxirida.

# 7. Nosozlik haqida fikrlash (Thinking About Failure)

<details>
<summary>Bu bobdagi 15 bo'lim</summary>

- [7.1 Hamma narsa buziladi: tarmoq, disk, protsess, boshqa servis](#71-hamma-narsa-buziladi-tarmoq-disk-protsess-boshqa-servis)
- [7.2 Nosozlik turlari: to'liq to'xtash, sekinlashuv, qisman javob, yolg'on javob](#72-nosozlik-turlari-toliq-toxtash-sekinlashuv-qisman-javob-yolgon-javob)
- [7.3 Sekin servis o'lgan servisdan xavfliroq: navbat to'lishi va orqaga bosim](#73-sekin-servis-olgan-servisdan-xavfliroq-navbat-tolishi-va-orqaga-bosim)
- [7.4 Qayta urinish qachon zarar keltiradi: retry bo'roni va retry byudjeti](#74-qayta-urinish-qachon-zarar-keltiradi-retry-boroni-va-retry-byudjeti)
- [7.5 Idempotentlik: bir xil so'rovni ikki marta bajarish xavfsiz bo'lsin](#75-idempotentlik-bir-xil-sorovni-ikki-marta-bajarish-xavfsiz-bolsin)
- [7.6 Qisman nosozlikda nima qilish: degradatsiya rejasi va zaxira javob](#76-qisman-nosozlikda-nima-qilish-degradatsiya-rejasi-va-zaxira-javob)
- [7.7 Ma'lumot yo'qolishi va buzilishi: qaysi biri ko'proq qo'rqinchli](#77-malumot-yoqolishi-va-buzilishi-qaysi-biri-koproq-qorqinchli)
- [7.8 Nosozlik ta'sirini cheklash: bulkhead va alohida resurs hovuzlari](#78-nosozlik-tasirini-cheklash-bulkhead-va-alohida-resurs-hovuzlari)
- [7.9 Tiklanish vaqti: RTO va RPO raqamlarini kelishib olish](#79-tiklanish-vaqti-rto-va-rpo-raqamlarini-kelishib-olish)
- [7.10 Nosozlik ssenariylarini oldindan yozish: "nima bo'lsa, nima qilamiz" jadvali](#710-nosozlik-ssenariylarini-oldindan-yozish-nima-bolsa-nima-qilamiz-jadvali)
- [7.11 Risk-storming: xavfni jamoa bilan diagramma ustida topish](#711-risk-storming-xavfni-jamoa-bilan-diagramma-ustida-topish)
- [7.12 Chidamlilikning to'rt qismi: kutilmagan vaziyat va doimiy moslashish](#712-chidamlilikning-tort-qismi-kutilmagan-vaziyat-va-doimiy-moslashish)
- [7.13 Xavfni taqsimlash: bitta host, bitta fizik quti, bitta zona](#713-xavfni-taqsimlash-bitta-host-bitta-fizik-quti-bitta-zona)
- [7.14 Riskni baholashdan keyin: yo'nalish, yig'indi, texnika va backlog](#714-riskni-baholashdan-keyin-yonalish-yigindi-texnika-va-backlog)
- [7.15 Amalda qo'llash](#715-amalda-qollash)

</details>



Nosozlik haqida fikrlash arxitektorni developerdan ajratadigan eng aniq chegara. Developer "bu kod ishlaydi" deb o'ylaydi, arxitektor "bu kod qachon va qanday ishlamaydi" deb so'raydi. Bu bob pattern katalogi emas: bu yerda nosozlikning mexanikasi, uning raqamlari va shu raqamlardan chiqadigan qarorlar bor. Har bir bo'limda siz jamoadan nimani so'rashingiz va qanday son kelishib olishingiz kerakligi ko'rsatilgan.

## 7.1 Hamma narsa buziladi: tarmoq, disk, protsess, boshqa servis

Taqsimlangan tizimda nosozlik hodisa emas, doimiy holat. Tarmoq paketi yo'qoladi, TCP ulanish firewall ning ulanish jadvalidan tushib qoladi, disk fsync'ni 400 ms kechiktiradi, JVM 3 sekundlik full GC ga ketadi, Kubernetes node'ni evict qiladi. Bu ro'yxatning har bir bandi oyda bir necha marta sodir bo'ladi, va ularning hech biri sizning kodingizdagi bug emas.

Arxitektor har bir tashqi chaqiruv uchun uchta savolga javob tayyorlaydi. Bu chaqiruv eng ko'p qancha kutadi. Kutish tugagach nima bo'ladi. Chaqiruv ikkinchi marta bajarilsa, biznes natija buziladimi.

Bu savollarga javob berishning narxi haqida bitta e'tirozni oldindan yopish kerak, chunki u har suhbatda chiqadi. Nygard narx farqini aniq aytadi: yuqori barqarorlikdagi dizayn barqarorsiz dizayn bilan deyarli bir xil narxga tushadi (Michael T. Nygard, *Release It!*, 1-nashr, Pragmatic Bookshelf, 2007, 3-bob, 36-bet). Sabab shaklda: timeout qo'yish, retry siyosatini yozish va fallback ni belgilash kodda qo'shimcha qator emas, boshqa qator. `restClient.get()` ni timeout bilan sozlash timeout siz sozlashdan qimmat emas, lekin ikkinchisi birinchi sekinlashuvda butun thread pool ini yo'qotadi. Shuning uchun barqarorlik byudjetdan emas, diqqatdan chiqadi, va "hozir vaqtimiz yo'q" degan dalil bu bo'limdagi qarorlarga qo'llanmaydi. Bu Nygard ning o'z chegarasini ham ko'rsatadi: gap bitta chaqiruv darajasidagi qarorlar haqida, [ko'p zona va ko'p region](#713-xavfni-taqsimlash-bitta-host-bitta-fizik-quti-bitta-zona) kabi infratuzilma qarorlari esa real pul turadi.

Eng ko'p uchraydigan xato: timeout belgilanmagan chaqiruv. Spring'da `RestClient` yoki `WebClient` da timeout qo'yilmasa, OS darajasidagi TCP retransmission limitiga tayanadi. Linux'da `tcp_retries2` ning default qiymati 15 ta qayta uzatish bo'lib, bu taxminan YIGIRMA DAQIQALIK timeout beradi - 15 raqami qayta uzatish soni, daqiqa emas, bu ikkisi tez-tez aralashtiriladi.

```yaml
spring:
  datasource:
    hikari:
      # pool'dan ulanish kutish: tez xato yaxshi, uzoq kutish yomon
      connection-timeout: 2000
      maximum-pool-size: 20
      max-lifetime: 1200000      # 20 daqiqa, PgBouncer/LB dan qisqa bo'lsin
      keepalive-time: 120000
      validation-timeout: 1000
      leak-detection-threshold: 20000
      data-source-properties:
        # JDBC socket darajasi: server o'lsa 5 sekundda bilamiz
        socketTimeout: 5
        connectTimeout: 2
        tcpKeepAlive: true
```

PostgreSQL tomonida ham chegara kerak. `statement_timeout` uzoq so'rovni uzadi, `lock_timeout` navbatda qotib qolishni to'xtatadi, `idle_in_transaction_session_timeout` ochiq tranzaksiyani tashlab ketgan protsessni tozalaydi. Hisobot servisi uchun `statement_timeout` ni 30 sekund, OLTP to'lov servisi uchun 3 sekund qilib ajratish normal qaror.

Timeout qiymatlarining o'zi ham abadiy emas. *Fundamentals of Software Architecture* taqsimlangan hisoblashning yolg'onlari ro'yxatida alohida bandni shu joyga qo'yadi: topologiya hech qachon o'zgarmaydi degan faraz yolg'on. Tarmoqdagi "kichik" yangilanish, qurilma almashtirish yoki marshrut o'zgarishi latency haqidagi farazlarni buzadi va production da timeout hamda circuit breaker larni ishga tushirib yuboradi, holbuki kodda hech narsa o'zgarmagan. Kitobning tavsiyasi tashkiliy: arxitektor operations va tarmoq administratorlari bilan doimiy aloqada bo'lsin, ya'ni tarmoq o'zgarishlari haqida oldindan bilsin. Amalda bu shunday ko'rinadi: p99 latency ning sabablari ro'yxatida "tarmoq o'zgarishi" doim bo'ladi, va reja bo'yicha tarmoq ishi oldidan integratsiya timeout lari qayta ko'riladi.

Oxirgi va eng umumiy savol: nosozlikni ko'tarishga urinish kerakmi yoki oldini olish. Kleppmann javobni ikki toifaga ajratadi va mezon davolash imkoniyati: davolab bo'ladigan nosozlikda chidamlilik afzal, davolab bo'lmaydigan joyda esa oldini olish (7-bet). Ikkinchi toifaning asosiy misoli xavfsizlik: hujumchi tizimga kirib maxfiy ma'lumotga ega bo'lsa, bu hodisani qaytarib bo'lmaydi, shuning uchun bu yerda chidamlilik emas, to'siq ishlatiladi. Bu bobdagi butun apparat (retry, bulkhead, degradatsiya) birinchi toifa uchun; ikkinchi toifaning yozuvi [20-bob](20-spring-security-filter-chain-oauth2-jwt.md) va [7.7](#77-malumot-yoqolishi-va-buzilishi-qaysi-biri-koproq-qorqinchli) da.

## 7.2 Nosozlik turlari: to'liq to'xtash, sekinlashuv, qisman javob, yolg'on javob

Quyidagi to'rt turlik ajratish shu korpusning amaliy taksonomiyasi. Nygard ning *Release It!* kitobi asosiy farqni ikki turda qo'yadi - tez xato va sekin xato - va sekin javobni ancha xavfliroq deb ataydi; kaskad nosozlik belgilari sifatida esa "crashing, hung threads, empty responses, or nonsense replies" ni sanaydi. Ya'ni pastdagi "yolg'on javob" tushunchasi kitobdagi "nonsense replies" ga yaqin, lekin alohida atama sifatida kitobda yo'q.

Turlardan tashqari yuklamaning shaklini ham ajratish kerak, chunki u qaysi nosozlik chiqishini belgilaydi. Nygard materiallar mexanikasidan ikki atama oladi: impulse (zarba) bu tez va qisqa kuch, stress esa uzoq davomli kuch, va stress strain, ya'ni deformatsiya hosil qiladi (Michael T. Nygard, *Release It!*, 1-nashr, Pragmatic Bookshelf, 2007, 3-bob, 37-bet). Ikkisining amaliy farqi joyda: zarba tegilgan joyda sinadi, strain esa tizimning uzoq nuqtasida ko'rinadi. Misoli tanish: marketing xabari yuborilgandan keyingi bir daqiqalik trafik portlashi zarba va u kirish qatlamida ko'rinadi; shu trafikning ikki soat davom etishi stress, va u navbat to'lishi, connection pool ning charchashi yoki replikatsiya lag i shaklida uchinchi servisda chiqadi. Shu sababli yuk testi ikki shaklda o'tkaziladi va [cho'qqi koeffitsienti](08-ishlash-va-resurs-hissi-napkin-math.md#82-oddiy-hisob-kuniga-n-sorov-nechta-rps-boladi-choqqi-koeffitsienti) hisobi faqat zarbani qoplaydi, stress emas.

To'rt turdagi nosozlik bir xil emas, va ularni aniqlash qiyinligi ham bir xil emas. To'liq to'xtash eng oson tur: ulanish rad etiladi, xato darhol ko'rinadi, alert ishlaydi. Sekinlashuv qiyinroq: servis javob beradi, lekin p99 latency 80 ms dan 4 sekundga chiqadi.

Qisman javob yana qiyin. Katalog servisi 1000 ta mahsulotdan 940 tasini qaytaradi, qolgani uchun ichki timeout bo'ldi, lekin HTTP status 200 keladi. Sizning kodingiz buni muvaffaqiyat deb hisoblaydi.

Yolg'on javob eng xavfli tur. Cache'da eski narx turibdi, replica 40 sekund orqada qolgan, yoki xato tutilib `catch` ichida bo'sh ro'yxat qaytarilgan. Alert chiqmaydi, metrikada xato ko'rinmaydi, lekin biznes zarar ko'radi.

```java
// Yolg'on javob ishlab chiqaruvchi klassik anti-qaror
try {
    return warehouseClient.getStock(sku); // timeout bo'lsa?
} catch (Exception e) {
    log.warn("ombor javob bermadi", e);
    return 0; // "qoldiq nol" deb yozdik, aslida bilmaymiz
}
```

Nol qoldiq va "bilmayman" bir xil ma'no emas. Birinchisi mijozga "tugadi" deb ko'rsatadi, ikkinchisi "hozir aytolmaymiz" deb ko'rsatadi. Arxitektor qaytariladigan tipni shunday loyihalaydi: `Optional`, `Result` yoki alohida `UNKNOWN` holati bo'lsin, nol bilan aralashmasin.

| Nosozlik turi | Aniqlash vositasi | Tipik aniqlash vaqti | Biznes zarari |
|---|---|---|---|
| To'liq to'xtash | health check, 5xx hisoblagich | 10-30 sekund | katta, lekin ko'rinadi |
| Sekinlashuv | p99 latency, thread pool to'lishi | 1-5 daqiqa | kaskadga aylanadi |
| Qisman javob | natija hajmi metrikasi, element soni | soatlar | sekin va yashirin |
| Yolg'on javob | ma'lumot solishtirish, reconciliation | kunlar | eng qimmat |

Yuqoridagi to'rtlik amaliy, lekin u yagona taksonomiya emas. Newman Tanenbaum va Steen ning *Distributed Systems* kitobidan jarayonlararo aloqadagi besh nosozlik turini keltiradi va bu ro'yxat boshqa o'qda turadi: u biznes ta'siri emas, protokol xulqi bo'yicha ajratadi.

| Tanenbaum va Steen turi | Nima ko'rinadi | Yuqoridagi to'rtlikda qaysi qator |
|---|---|---|
| Crash failure | server qulaguncha hammasi yaxshi edi, keyin javob yo'q | to'liq to'xtash |
| Omission failure | yubordingiz, javob kelmadi; yoki event yuborib turgan servis shunchaki to'xtadi | to'liq to'xtash va qisman javob orasida |
| Timing failure | biror narsa kech yoki juda erta sodir bo'ldi | sekinlashuv |
| Response failure | javob keldi, lekin noto'g'ri yoki kerakli maydonlar yo'q | qisman javob, yolg'on javob |
| Arbitrary (Byzantine) failure | nosozlik bo'lganini ham, sababini ham qatnashchilar kelishib ola olmaydi | to'rtlikda yo'q |

Ikki qator alohida ahamiyatli. **Omission failure** ning ikkinchi yarmi, ya'ni event oqimining jim to'xtashi, odatda hech qanday xato belgisi bermaydi: iste'molchi kutishda turadi va metrikada xato ko'rinmaydi, shuning uchun bu holat uchun "oxirgi event vaqti" metrikasi va yo'qlik alerti kerak bo'ladi. **Arbitrary failure** esa korpusning to'rtligida yo'q va bu ataylab: u ichki tizimlarda kamdan kam uchraydi.

Kitobdan keladigan xulosa esa mijoz tomoniga tegishli: bu xatolarning ko'pi vaqtinchalik, ya'ni o'tib ketadigan muammo. Shuning uchun mijoz xatoni ikki guruhga ajrata olishi kerak, qayta urinish ma'noga egami yoki inson aralashuvi kerakmi. HTTP ni Newman shu talabning namunasi deb keltiradi: 400 toifasi so'rovning o'zida muammo borligini aytadi, demak `404 Not Found` ni qayta urinishdan ma'no yo'q; 500 toifasi quyi tomondagi muammoni bildiradi va uning bir qismi vaqtinchalik, shuning uchun `503 Service Unavailable` da qayta urinish o'rinli, `501 Not Implemented` da esa yordam bermaydi. Qayta urinishning o'z qoidalari [7.4](#74-qayta-urinish-qachon-zarar-keltiradi-retry-boroni-va-retry-byudjeti) da.

## 7.3 Sekin servis o'lgan servisdan xavfliroq: navbat to'lishi va orqaga bosim

Buni raqam bilan ko'rsatish kerak, aks holda jamoa ishonmaydi. Little qonuni: bir vaqtda band bo'lgan ishlovchilar soni teng kelayotgan oqim ko'paytirilgan javob vaqtiga. Buyurtma servisi sekundda 200 so'rovni qabul qiladi va o'rtacha 50 ms ishlaydi. Demak bir vaqtda taxminan 10 thread band.

Endi downstream to'lov servisi sekinlashdi va javob vaqti 50 ms dan 2 sekundga chiqdi. Bir xil 200 rps da band thread soni 400 ga ko'tariladi. Tomcat'da `server.tomcat.threads.max` default 200. Demak 200 thread to'ladi, qolgan so'rovlar `accept-count` navbatiga tushadi, navbat ham to'lgach TCP ulanish rad etiladi.

Natija: to'lov servisi sekinlashgani uchun buyurtma servisi butunlay ishlamay qoldi, hatto to'lovga aloqasi yo'q "buyurtma tarixini ko'rish" endpoint'i ham o'ldi. O'lgan servis bunday zarar keltirmaydi, chunki undan kelgan xato darhol qaytadi va thread bo'shaydi.

```properties
# Navbat chuqurligini ataylab cheklash: tez rad etish, sekin o'lishdan yaxshi
server.tomcat.threads.max=200
server.tomcat.accept-count=50
server.tomcat.connection-timeout=5s
server.tomcat.max-connections=2000
# Async MVC uchun javob kutish chegarasi
spring.mvc.async.request-timeout=4s
# Graceful shutdown: navbatdagi so'rovni tugatib keyin o'chish
server.shutdown=graceful
spring.lifecycle.timeout-per-shutdown-phase=25s
```

Asosiy qoida: har bir chaqiruvning timeout'i chaqiruvchi tomonning SLO sidan kichik bo'lsin. Agar API o'z mijoziga 1 sekund ichida javob berishga majbur bo'lsa, ichki uchta chaqiruvning timeout yig'indisi 1 sekundan oshmasligi kerak. Ko'pincha bu 300 ms, 300 ms va 250 ms degan taqsimot bo'ladi.

Orqaga bosim (backpressure) kutishni navbatga yashirishni to'xtatadi. Kafka consumer'da `max.poll.records` ni kamaytirish, reactive oqimda bounded buffer, HTTP darajasida 429 qaytarish: bularning hammasi bitta fikrni amalga oshiradi. Tizim imkonidan ko'p ish qabul qilmasin.

Nygard bu hodisalar zanjiriga aniq nomlar bergan va ularni bilish suhbatni tezlashtiradi. **Blocked Threads**: barcha thread'lar bloklanib qolsa, server tashqaridan o'lgan ko'rinadi. **Chain Reactions**: bitta node yiqilsa uning yuklamasi qolganlarga tushadi va ular ham navbat bilan yiqiladi, ya'ni nosozlik bitta qatlam ICHIDA tarqaladi. **Cascading Failures**: nosozlik qatlamlar ORASIDA, integratsiya nuqtasi orqali o'tadi. **Unbalanced Capacities**: front-end back-end imkonidan ko'p so'rov yuborishi. Nygard ning yechimlaridan biri shu yerga tegishli: **Handshaking** - back-end o'zi "hozir qabul qilolmayman" deb aytishi, ya'ni orqaga bosimning protokol darajasidagi shakli. Yana biri **Fail Fast**: kitob "doim tez yiqilish yaxshiroq" deb yozadi, chunki eng yomoni sekin xato javobi.

Uzoq ishlaydigan protsess uchun alohida pattern bor: **Steady State**. Ma'lumot cheksiz o'ssa yoki xotira oqsa, tizim hech qanday tashqi sabab bo'lmasa ham vaqt o'tishi bilan yiqiladi. Shuning uchun har bir o'suvchi narsaga (log, cache, jadval, sessiya) tozalash mexanizmi kerak va u ilovaning o'zida bo'lishi kerak, qo'lda emas.

Timeout bu zanjirning yarmi. Nygard timeout va circuit breaker ni juft sifatida ko'radi: timeout nosozlikni ANIQLAYDI, circuit breaker esa shu signalga qarab qayta urinishni TO'XTATADI; ikkinchisisiz birinchisi faqat kutish vaqtini qisqartiradi, lekin yiqilgan servisga yuklama berishni davom etadi. Arxitektor uchun bu yerda ikki qaror bor. Birinchisi - kalit ochiq bo'lganda nima qaytarish, va bu muhandis yolg'iz hal qiladigan narsa emas: kitob buni biznes qarori deb ataydi, chunki variantlar (eski keshdagi qiymat, bo'sh ro'yxat, ochiq xato, yoki navbatga qo'yib keyin bajarish) biznes uchun bir xil emas. Ikkinchisi - kalitning qamrovi: bitta circuit breaker butun tashqi servis uchun emas, uning har bir muhim operatsiyasi uchun alohida bo'lsin, aks holda katalogni o'qish yiqilgani uchun to'lov yo'li ham yopilib qoladi. Mexanikasi va Resilience4j dagi sozlamalari uchun: [patterns 17.2](../patterns/17-resilience-va-cloud-dizayn-patternlari.md#172-zanjirni-uzgich-circuit-breaker).

## 7.4 Qayta urinish qachon zarar keltiradi: retry bo'roni va retry byudjeti

Retry foydali vosita, lekin u yuklamani ko'paytiradigan vosita. Uch marta urinish siyosati tizim allaqachon qiynalgan paytda yuklamani uch barobar oshiradi. Bu aynan eng yomon vaqtda sodir bo'ladi.

Ko'p qatlamli retry yana xavfliroq. Gateway 3 marta, buyurtma servisi 3 marta, JDBC qatlami 2 marta urinadi. Natijada bitta foydalanuvchi so'rovi bazaga 18 ta chaqiruvga aylanadi. Qoida: retry faqat bitta qatlamda bo'lsin.

Ikkinchi qoida: faqat retry qilish mumkin bo'lgan xatolar qaytarilsin. HTTP 503 va ulanish rad etilishi qaytariladi. HTTP 400 va validatsiya xatosi qaytarilmaydi. PostgreSQL'da `40001` (serialization failure) va `40P01` (deadlock detected) qaytariladi, `23505` (unique violation) qaytarilmaydi.

Uchinchi qoida: jitter majburiy. Jittersiz exponential backoff barcha mijozlarni bir xil daqiqada qayta urinishga majbur qiladi, va bu to'lqinni takrorlaydi. Tasodifiy tarqatish bilan birinchi urinish 100-200 ms, ikkinchisi 200-400 ms, uchinchisi 400-800 ms oralig'ida bo'ladi.

Retry byudjeti eng kuchli, lekin kamdan kam qo'llanadigan g'oya. Mohiyati: oxirgi 10 sekunddagi umumiy chaqiruvlardan ko'pi bilan 10 foizi retry bo'lishi mumkin. Byudjet tugasa retry butunlay o'chadi va xato darhol qaytariladi. Bu cheklov nosozlik paytida yuklama 3 barobar emas, 1.1 barobar oshishini kafolatlaydi. Resilience4j yoki shunga o'xshash kutubxona tanlanganda arxitektor shu byudjet imkoniyati bor-yo'qligini tekshiradi.

## 7.5 Idempotentlik: bir xil so'rovni ikki marta bajarish xavfsiz bo'lsin

Retry haqida gapirish idempotentlikni kelishib olmasdan ma'nosiz. Timeout bo'lganda siz ikkita holatni ajratib olmaysiz: so'rov umuman yetib bormadimi, yoki yetib borib bajarildi, faqat javob yo'qoldimi. Ikkinchi holatda qayta urinish ikkinchi to'lovni amalga oshiradi.

Yechim mijoz tomonidan beriladigan idempotency key va ma'lumotlar bazasidagi unique constraint. Muhim nuqta: constraint ilova kodida emas, bazada bo'lsin. Ilovadagi "avval tekshir, keyin yoz" mantig'i ikki instance parallel ishlaganda buziladi.

```sql
-- Idempotentlik kalitini bazada majburiy qilamiz
CREATE TABLE payment (
    id            bigserial PRIMARY KEY,
    order_id      bigint      NOT NULL,
    idem_key      text        NOT NULL,
    amount        numeric(18,2) NOT NULL,
    status        text        NOT NULL,
    response_body jsonb,
    created_at    timestamptz NOT NULL DEFAULT now()
);

-- Bitta kalit bitta to'lov: poyga (race) bo'lsa baza hal qiladi
CREATE UNIQUE INDEX ux_payment_idem ON payment (idem_key);

-- Takroriy urinishda yozmaymiz, lekin eski javobni topamiz
INSERT INTO payment (order_id, idem_key, amount, status)
VALUES (:orderId, :idemKey, :amount, 'PENDING')
ON CONFLICT (idem_key) DO NOTHING
RETURNING id;
```

`RETURNING` bo'sh qaytdi degani: bu kalit allaqachon bor. Shundan keyin kod yangi to'lov boshlamaydi, saqlangan javobni o'qib qaytaradi. Agar eski yozuv hali `PENDING` bo'lsa, mijozga 409 yoki "hozir ishlanmoqda" holati qaytariladi, lekin yangi debet qilinmaydi.

Idempotentlikning ikkinchi shakli natural kalitlar orqali keladi. Ombor qoldig'ini `stock = stock - 5` deb emas, hodisa identifikatori bilan yozib keyin yig'indini hisoblash qayta urinishga chidamli bo'ladi. Bu yerda outbox va hodisa jurnali kerak bo'ladi, dizayn [patternlar hujjatidagi](../patterns/README.md) outbox pattern bo'limi mexanikani tushuntiradi.

Tashqi tizim o'zi idempotent bo'lmasa, uni siz idempotent qilasiz: har chaqiruvga `request_id` saqlab, javobni yozib, retry'ni o'sha saqlangan natija orqali boshqarasiz.

Mavzuning to'liq yozuvi [idempotency](../patterns/07-api-dizayn-patternlari.md#79-idempotentlik-kaliti-idempotency-key) bo'limida; bu yerda faqat shu bo'limning nuqtai nazari.

## 7.6 Qisman nosozlikda nima qilish: degradatsiya rejasi va zaxira javob

Degradatsiya texnik masala emas, biznes qaror. Arxitektorning ishi har bir funksiya uchun "bu yo'q bo'lsa nima ko'rsatamiz" javobini product egasidan yozma olish, va buni insidentdan oldin qilish.

Funksiyalarni uch guruhga bo'lish yetarli. Majburiy guruh ishlamasa, servis ishlamagan deb hisoblanadi: to'lovni qabul qilish, buyurtma yozish. Muhim guruh ishlamasa, xizmat davom etadi lekin sifat tushadi: tavsiyalar, yetkazib berish vaqti prognozi. Qo'shimcha guruh ishlamasa, foydalanuvchi sezmaydi ham: bonus ballar ko'rsatkichi, ko'rilgan mahsulotlar tarixi.

```java
// Degradatsiya: aniq uch holat, "nol" bilan aralashmaydi
public DeliveryEstimate estimate(Order order) {
    try {
        return deliveryClient.estimate(order); // 300 ms timeout
    } catch (TimeoutException | ServiceUnavailableException e) {
        metrics.counter("delivery.degraded").increment();
        // zaxira javob: shahar bo'yicha statik o'rtacha, aniqligi past
        return DeliveryEstimate.approximate(
                staticTable.averageDays(order.cityCode()),
                Confidence.LOW);
    }
}
```

Zaxira javobning uchta shartidan hech biri tushib qolmasligi kerak. Birinchi shart: zaxira javob o'z manbasiga bog'liq bo'lmasin, ya'ni u ham o'sha o'lgan servisdan kelmasin. Ikkinchi shart: zaxira javob ekanligi javob ichida ko'rinsin, `Confidence.LOW` yoki shunga o'xshash maydon bilan. Uchinchi shart: degradatsiya hisoblagichi alohida metrika bo'lsin, aks holda siz haftalab degradatsiyada ishlab, buni bilmasligingiz mumkin.

## 7.7 Ma'lumot yo'qolishi va buzilishi: qaysi biri ko'proq qo'rqinchli

Ma'lumot yo'qolishi ko'rinadi va o'lchanadi. Oxirgi 30 sekundlik tranzaksiyalar yo'qoldi, siz buni biladigan nuqtani topasiz, mijozlarga aytasiz, qayta yuklashni so'raysiz. Jarayon og'riqli, lekin chegarasi aniq.

Ma'lumot buzilishi ko'rinmaydi. Noto'g'ri migratsiya hisob qoldig'ini ikki barobar qildi, va bu uch hafta davomida hisobotlarga, to'lov hujjatlariga, soliq deklaratsiyasiga ko'chib ketdi. Backup'lar ham buzilgan ma'lumot bilan to'ldi. Shuning uchun arxitektor uchun buzilish har doim xavfliroq.

Buzilishga qarshi himoya to'rt qatlamdan iborat. Birinchi qatlam: bazadagi constraint'lar. `NOT NULL`, `CHECK (amount > 0)`, foreign key, unique index ilovaga bog'liq emas va deploy xatosidan omon qoladi. Ikkinchi qatlam: PostgreSQL data checksums. PostgreSQL 15-17 da bu `initdb` paytida yoqiladi, keyin `pg_checksums` yordamida to'xtatilgan klasterda o'zgartirish mumkin. Checksum yoqilmagan bo'lsa, diskdagi jimgina buzilish (silent corruption) sizga umuman xabar bermaydi.

Uchinchi qatlam: muntazam solishtirish. Kunda bir marta to'lov provayderi hisoboti bilan ichki jurnalni taqqoslash farqni bir kun ichida topadi. To'rtinchi qatlam: nuqtaga tiklanish imkoniyati, ya'ni PITR. Buzilish vaqti topilgach, shu nuqtaga qadar tiklash kerak bo'ladi.

```bash
# Bazaviy nusxa va WAL arxivi: PITR uchun asos
pg_basebackup -h db-primary -U replicator -D /backup/base \
  --wal-method=stream --checkpoint=fast --progress

# Tiklash nuqtasini belgilash (recovery sozlamalarida)
# restore_command = 'cp /backup/wal/%f %p'
# recovery_target_time = '2026-10-03 14:22:00+05'
# recovery_target_action = 'promote'

# Nusxaning haqiqatan tiklanishini har hafta tekshirish
pg_verifybackup /backup/base
```

Tekshirilmagan backup backup emas. Bu jumlani jamoa devoriga yozib qo'yish kerak. Har hafta avtomatik tiklash testi bo'lsin, va u faqat "fayl bor" emas, "baza ko'tarildi va kalit jadvallarda kutilgan qator soni bor" darajasida tekshirsin.

## 7.8 Nosozlik ta'sirini cheklash: bulkhead va alohida resurs hovuzlari

Kemadagi suv o'tkazmaydigan bo'limlar g'oyasi: bitta bo'lim suvga to'lsa, kema cho'kmaydi. Ilovada bu alohida resurs hovuzlari degani. Hisobot so'rovlari va to'lov so'rovlari bitta HikariCP pool'ini bo'lishmasin.

Amalda bu ikki `DataSource` bean degani. To'lov uchun 20 ulanish, hisobot uchun 5 ulanish. Hisobot og'ir so'rovlar bilan o'z 5 ta ulanishini band qilsa, to'lov hali ham 20 ulanishga ega. Bitta 25 lik umumiy pool'da hisobot hammasini yeb ketishi mumkin.

```java
@Bean
@Primary
@ConfigurationProperties("app.datasource.oltp")
public HikariDataSource oltpDataSource() {
    // to'lov va buyurtma: qisqa tranzaksiyalar, ko'p ulanish
    return DataSourceBuilder.create().type(HikariDataSource.class).build();
}

@Bean
@ConfigurationProperties("app.datasource.reporting")
public HikariDataSource reportingDataSource() {
    // hisobot: uzoq so'rovlar, kam ulanish, alohida pool
    return DataSourceBuilder.create().type(HikariDataSource.class).build();
}
```

Thread pool darajasida ham shu mantiq ishlaydi. Tashqi to'lov provayderiga chaqiruvlar alohida executor'da bo'lsa, provayder sekinlashganda umumiy web thread'lar band bo'lmaydi. Java 21+ dagi virtual thread'lar thread sonini arzonlashtiradi, lekin bulkhead zaruriyatini yo'qotmaydi: chegara endi thread sonida emas, pool ulanishlari va semaphore'larda bo'ladi.

Ajratish mezoni oddiy: so'rovning latency profili, biznes muhimligi va downstream bog'liqligi. Uchalasidan biri boshqalardan keskin farq qilsa, alohida hovuz oqlanadi.

Chegarani qayerdan o'tkazish kerakligini esa Nygard boshqa o'qda qo'yadi: bo'linish chegarasi biznes ta'siri bilan arxitekturani kesishtirib topiladi, va amalda uch shakldan biri chiqadi, ya'ni chegara chaqiruvchi bo'yicha, funksionallik bo'yicha yoki topologiya bo'yicha o'tadi (Michael T. Nygard, *Release It!*, 1-nashr, Pragmatic Bookshelf, 2007, 5-bob, 121-bet). Uchalasi bir xil narsani ajratmaydi va tanlov "nima yiqilsa kim zarar ko'radi" savolidan chiqadi.

| Chegara shakli | Nima bo'yicha ajratiladi | To'lov tizimidagi misol |
|---|---|---|
| Chaqiruvchi bo'yicha | kim so'rov yuborayotgani | mobil ilova va ichki admin paneli alohida pool va alohida rate limit oladi |
| Funksionallik bo'yicha | so'rov qanday ish qilayotgani | to'lov va hisobot alohida `DataSource` oladi (yuqoridagi kod) |
| Topologiya bo'yicha | so'rov qayerda bajarilayotgani | o'qish standby ga, yozish primary ga ketadi; nusxalar zona bo'yicha tarqaladi |

Ikki qadamli tekshiruv shu jadvalni qarorga aylantiradi. Birinchi qadam: har chegara nomzodi uchun "u yiqilsa qaysi biznes amali ishlashda davom etadi" degan savolga javob yoziladi. Ikkinchi qadam: javob "hech biri" bo'lsa chegara qiymat bermaydi va u faqat murakkablik qo'shadi, ya'ni ikki pool o'rniga bitta pool va aniq timeout yetadi.

## 7.9 Tiklanish vaqti: RTO va RPO raqamlarini kelishib olish

RTO: nosozlikdan keyin xizmat qancha vaqtda qayta ishlashi kerak. RPO: qancha ma'lumot yo'qolishiga ruxsat berilgan. Bu ikki raqam arxitekturani belgilaydi, aksi emas. Shuning uchun ular jamoa xohishi emas, biznes bilan yozma kelishuv bo'lishi kerak.

RPO nolga teng bo'lishi sinxron replikatsiyani talab qiladi. PostgreSQL'da bu `synchronous_commit = remote_apply` yoki `remote_write` va `synchronous_standby_names` sozlanishi. Buning narxi bor: har bir commit replica javobini kutadi, bu bir xil ma'lumot markazida taxminan 1-3 ms, boshqa regionda 30-80 ms qo'shadi. To'lov servisi uchun bu narx oqlanadi, hodisa jurnali uchun ko'pincha oqlanmaydi.

```sql
-- Replikatsiya orqada qolishini RPO raqami sifatida o'lchash
SELECT application_name,
       sync_state,
       write_lag,            -- WAL replicaga yozildi
       flush_lag,            -- diskka fsync qilindi
       replay_lag,           -- so'rovlar ko'radigan holat
       pg_wal_lsn_diff(pg_current_wal_lsn(), replay_lsn) AS bytes_behind
FROM pg_stat_replication;

-- Agar flush_lag > 2 sekund bo'lsa, RPO 2 sekunddan katta: alert kerak
```

RTO ni hisoblashda eng ko'p uchraydigan xato: faqat baza ko'tarilish vaqtini sanash. Haqiqiy RTO besh qismdan iborat: aniqlash, qaror, failover, ilovalarni qayta ulash, cache'ni isitish. Aniqlash 2 daqiqa, qaror 5 daqiqa, failover 1 daqiqa, qayta ulanish 2 daqiqa, cache isishi 10 daqiqa bo'lsa, RTO 20 daqiqa.

| Tizim qismi | RPO maqsadi | RTO maqsadi | Buni ta'minlaydigan qaror |
|---|---|---|---|
| To'lov tranzaksiyalari | 0 | 5 daqiqa | sinxron replica, avtomatik failover |
| Buyurtma holati | 10 sekund | 15 daqiqa | asinxron replica, WAL arxivi |
| Ombor qoldig'i | 1 daqiqa | 30 daqiqa | asinxron replica va qayta hisoblash |
| Hisobot omborxonasi | 24 soat | 8 soat | kunlik backup, qayta yuklash |
| Audit jurnali | 0 | 1 soat | append-only saqlash, ikki nusxa |

## 7.10 Nosozlik ssenariylarini oldindan yozish: "nima bo'lsa, nima qilamiz" jadvali

Insident paytida fikrlash sifati tushadi. Shuning uchun fikrlashni oldin bajarib, natijani jadvalga yozib qo'yish kerak. Bu jadval dizayn hujjatining majburiy qismi bo'lsin va har chorakda qayta ko'rilsin.

Jadvalda besh ustun bo'ladi: ssenariy, qanday bilib olamiz, avtomatik nima bo'ladi, odam nima qiladi, foydalanuvchi nimani ko'radi. Oxirgi ustun eng ko'p tashlab ketiladigan, lekin eng muhim ustun. Agar foydalanuvchi nimani ko'rishini yozib qo'yolmasangiz, degradatsiya rejasi hali tayyor emas.

| Tuzoq | Nega yuzaga keladi | Yechim |
|---|---|---|
| Timeout'siz tashqi chaqiruv | default qiymat OS darajasida, ~20 daqiqagacha | har client uchun aniq timeout, SLO dan kichik |
| Ko'p qatlamli retry | har qatlam mustaqil 3 marta urinadi | retry bitta qatlamda, byudjet bilan cheklangan |
| Bo'sh ro'yxat qaytaradigan catch | xato yashiriladi, metrika toza ko'rinadi | alohida UNKNOWN holati va degradatsiya hisoblagichi |
| Umumiy connection pool | hisobot va OLTP bitta hovuzda | alohida DataSource, bulkhead |
| Takroriy to'lov | timeout'dan keyin retry, kalit yo'q | idem_key va unique index bazada |
| Tekshirilmagan backup | tiklash hech qachon sinalmagan | haftalik avtomatik tiklash testi |
| Replica lag nazoratsiz | RPO raqam sifatida o'lchanmagan | flush_lag alert, sinxron rejim kerakli joyda |
| Cache isishi hisobga olinmagan | RTO faqat baza vaqti deb o'lchangan | RTO ga isitish vaqti qo'shiladi |
| Checksum o'chirilgan baza | initdb default bilan ketilgan | data checksums yoqish, pg_verifybackup |

| Mavzu | Oddiy yondashuv | Arxitektor yondashuvi |
|---|---|---|
| Tashqi chaqiruv | "ishlaydi deb o'ylaymiz" | timeout, retry siyosati va zaxira javob oldindan yozilgan |
| Timeout qiymati | bitta umumiy 30 sekund | SLO dan kelib chiqib har chaqiruvga alohida budjet |
| Retry | har joyda 3 marta | bitta qatlamda, jitter bilan, byudjet cheklovida |
| Sekin downstream | "latency oshdi, kutamiz" | thread va pool to'lishini hisoblab, tez rad etishga o'tiladi |
| Xato tutish | log yozib bo'sh natija qaytarish | aniq UNKNOWN holati va degradatsiya metrikasi |
| Takroriy so'rov | "ikki marta kelmaydi" | idempotency key va bazadagi unique constraint |
| Resurs hovuzlari | bitta katta pool | latency profili bo'yicha ajratilgan hovuzlar |
| Backup | nusxa olinadi | nusxa olinadi va har hafta tiklanishi sinaladi |
| Tiklanish vaqti | "tez tiklaymiz" | RTO va RPO raqamlari biznes bilan yozma kelishilgan |
| Nosozlik rejasi | insident paytida o'ylanadi | ssenariy jadvali dizayn hujjatida tayyor |

Ssenariylarni izlash joyi aniq. Har bir tashqi bog'liqlik ikki ssenariy beradi: o'ldi va sekinlashdi. Har bir ma'lumot ombori uchta ssenariy beradi: o'qish, yozish, buzilish. Har bir navbat ikki ssenariy beradi: consumer orqada qoldi, xabar takrorlandi. O'rtacha servisda 15-25 ta ssenariy chiqadi.

Ssenariyni yozgandan keyin uni sinab ko'rish kerak. Bu yerda chaos testlari va nosozlikni ataylab kiritish ishga kiradi, [testlash qo'llanmasidagi](../testing/README.md) resilience testlari bo'limi texnikani ko'rsatadi. Arxitektor uchun muhimi: har bir yozilgan ssenariyning kamida bittasi haqiqatan tekshirilgan bo'lsin, aks holda jadval ishonch emas, qog'oz bo'lib qoladi.

## 7.11 Risk-storming: xavfni jamoa bilan diagramma ustida topish

Yuqoridagi ssenariy jadvalini kim to'ldiradi? Agar uni arxitektor yolg'iz yozsa, jadval faqat uning tajribasidagi xavflarni oladi. Simon Brown shu ish uchun alohida texnika beradi: risk-storming - jamoa bilan birga, diagramma ustida bajariladigan tez va ko'rinadigan mashq. Diqqat: bu bobning qolgan qismi Nygard ning *Release It!* 1-nashriga tayanadi, risk-storming esa boshqa kitobdan, Brown ning *Software Architecture for Developers* idan olingan.

Brown to'rt qadam sanaydi.

| Qadam | Nima qilinadi | Nega shunday |
|---|---|---|
| 1. Diagramma chizish | arxitektura diagrammalari doskaga yoki katta qog'ozga chiziladi, Brown boshlang'ich nuqta sifatida C4 ni tavsiya qiladi | turli abstraksiya darajasi turli xavfni ko'rsatadi; katta diagramma yaxshiroq |
| 2. Xavfni mustaqil yozish | har kim (arxitektor, dasturchi, menejer, operatsiya xodimi) diagramma oldida turib, bitta stikerga bitta xavf yozadi va uni ehtimol va ta'sir bo'yicha baholaydi | xavfni sezish tajribaga bog'liq; sukutda va yashirin yozish jamoaning haqiqiy qarashini beradi, yetakchining qarashini emas |
| 3. Xavfni diagrammaga yopishtirish | stiker xavf topilgan joyga, masalan sekin ishlashi mumkin bo'lgan komponent ustiga qo'yiladi | bir qarashda eng xavfli hudud ko'rinadi; o'xshash xavflar bir joyda to'planadi |
| 4. Ustuvorlash | har stiker yoki stikerlar to'dasi uchun ehtimol va ta'sir jamoa bilan kelishiladi | chetga chiqqan baholarning sababi so'raladi, Planning Poker dagi kabi umumiy raqamga kelinadi |

Brown ikkinchi qadamni vaqt bilan cheklashni (5-10 daqiqa) va stiker rangini ustuvorlik uchun ishlatishni tavsiya qiladi. Ehtimol va ta'sirning ko'paytmasi [risk formulasi](01-arxitektorning-fikrlash-modeli.md#15-qaytarib-boladigan-va-qaytarib-bolmaydigan-qarorlar) bo'limida, test chuqurligini shu bo'yicha tanlash esa [risk-ga asoslangan testlash](../testing/01-sifat-strategiyasi-va-arxitektorning-roli.md#13-risk-ga-asoslangan-testlash) bo'limida berilgan, bu yerda takrorlanmaydi.

Xavfni topish ishning yarmi: Brown uchta yumshatish yo'lini sanaydi. O'qitish yoki jamoani to'ldirish, tajriba yetmagan joyda. Prototip: stiker to'plangan yo'lni kichik tajriba bilan sinash. Arxitekturani o'zgartirish, masalan yagona nosozlik nuqtasini olib tashlash; o'zgarishdan keyin mashq qayta o'tkaziladi va ta'sir kutilganidek bo'lgani tekshiriladi.

Natija yozib qolinadi. Brown ehtimoli yoki ta'siri "yo'q" deb baholangan xavflarni ham jurnalda saqlashni aytadi, chunki keyin shart o'zgaradi. Texnik xavf egasi masalasida uning tavsiyasi aniq: xavf reyestri ko'pincha texnik bo'lmagan loyiha menejeri qo'lida bo'ladi, texnik xavflarning egasi esa arxitektura roli bo'lishi kerak. Mashqni loyiha boshida bir marta emas, iteratsiya rejalashtirish va retrospektivada ham o'tkazish mumkin.

## 7.12 Chidamlilikning to'rt qismi: kutilmagan vaziyat va doimiy moslashish

Bu bobning qolgan qismi kutilgan nosozliklar bilan ishlaydi: timeout, retry, bulkhead va degradatsiya rejasi oldindan ma'lum muammolar uchun qo'yiladi. Newman shu nuqtada atamani keng oladi va chidamlilik (resiliency) so'zi juda erkin ishlatilishi tufayli soha tor tushunilishini aytadi; keyin IT dan tashqaridagi resilience engineering sohasiga, aniqrog'i David D. Woods ning tasnifiga murojaat qiladi (Sam Newman, *Building Microservices: Designing Fine-Grained Systems*, 2-nashr, O'Reilly, 2021, 12-bob, "What Is Resiliency?" bo'limi).

| Qism | Ta'rifi | Bu bobdagi o'rni |
| --- | --- | --- |
| Robustness | kutilgan buzilishni yutib yuborish qobiliyati | bobning asosiy qismi: timeout, retry, bulkhead, zaxira javob |
| Rebound | og'ir hodisadan keyin tiklanish qobiliyati | [tiklanish vaqti](#79-tiklanish-vaqti-rto-va-rpo-raqamlarini-kelishib-olish) va tiklash rejasi |
| Graceful extensibility | kutilmagan vaziyat bilan qanchalik yaxshi kurashish | shu bo'limning birinchi yarmi |
| Sustained adaptability | o'zgarib turgan muhit, manfaatdor tomonlar va talablarga doimiy moslashish | shu bo'limning ikkinchi yarmi |

Robustness oldingi bilimni talab qiladi va u faqat kodga tegishli emas: Newman odamlarni ham shu qatorga qo'yadi, ya'ni on-call da bitta odam bo'lsa va u kasal bo'lib qolsa yoki incident paytida bog'lanib bo'lmasa, tizim robust emas (12-bob, "Robustness"). Yana bir eslatma qarshi tomondan keladi: robustness ni oshirish tizimga murakkablik qo'shadi va bu yangi muammolarning manbasi bo'ladi, shuning uchun har bir bunday qadam oddiy xarajat va foyda hisobi bilan emas, "natijada chiqadigan murakkabroq tizim bilan kelishaman" degan savol bilan baholanadi.

**Graceful extensibility: avtomatlashtirish kutilmaganga yetmaydi.** Kutilmaganga tayyor bo'lmagan tizim mo'rt bo'ladi: kutgan chegaraga yaqinlashganda u yetarli ishlay olmasdan parchalanadi. Newman tashkiliy omilni birinchi qo'yadi: mas'uliyat markazda emas, tashkilot ichiga taqsimlangan yassi tuzilmalar kutilmaganga yaxshiroq tayyorlanadi, chunki odam nima qilishi kerakligida cheklangan bo'lsa va qat'iy qoidalar to'plamiga ergashishga majbur bo'lsa, uning kutilmaganni hal qilish qobiliyati keskin qisqaradi (12-bob, "Graceful Extensibility"). Keyin avtomatlashtirish haqidagi nozik fikr keladi: avtomatlashtirish ajoyib narsa, u bor odam bilan ko'proq ish qilish imkonini beradi, lekin shu bilan odam sonini kamaytirish imkonini ham beradi, va aynan shu joyda xavf bor, chunki avtomatlashtirish kutilmaganni boshqarmaydi. Newman ning xulosasi aniq: tizimni yoqimli ravishda kengaytirish, ya'ni kutilmaganni hal qilish qobiliyati to'g'ri ko'nikma, tajriba va mas'uliyatga ega odamlarning joyida turishidan keladi. Amalda bu on-call rotatsiyasini "eng arzon odam" bo'yicha emas, tizimni biladigan odamlar bo'yicha tuzish, va runbook ni qadam ro'yxati emas, qaror bera oladigan odam uchun kontekst deb yozish degani.

**Sustained adaptability: muvaffaqiyatga ishonib qolmaslik.** Bu qism o'zini oqlab qo'ymaslikni talab qiladi. Newman Woods ning gapini keltiradi: ilgari qanchalik yaxshi ishlagan bo'lsak ham, qanchalik muvaffaqiyatli bo'lsak ham, kelajak boshqacha bo'lishi mumkin va biz unga yaxshi moslanmagan bo'lishimiz mumkin; hali katastrofik uzilishni ko'rmagan bo'lsak, bu uning bo'lmasligini bildirmaydi (12-bob, "Sustained Adaptability"). Shu yerda chaos engineering foydali vosita bo'lib keladi, lekin asosiy shart boshqa: tizimga butun holda qarash kerak, va Newman paradoksni ko'rsatadi, ya'ni kichik, mustaqil va mahalliy mas'uliyati yuqori jamoalarga intilish katta rasmni ko'rishni yo'qotish bilan tugashi mumkin. Ikkinchi shart madaniyat: incidentdan keyin odamlar jazodan qo'rqmasdan ma'lumot bo'lishadigan muhit bo'lishi kerak, kutilmaganni haqiqatan tekshirib saboq chiqarish uchun esa vaqt, energiya va odam kerak, ya'ni qisqa muddatda funksiya yetkazishga ketadigan resurs kamayadi. Shuning uchun bu qarorning o'zi muvozanat: qisqa muddatli yetkazib berish va uzoq muddatli moslashish orasidagi nuqtani topish, va bu bir martalik tadbir emas, doimiy sarmoya.

Bobning asosiy xulosasi shu yerda o'zgaradi. Newman ochiq yozadi: mikroservis arxitekturasi robustness ga yordam beradi, lekin chidamlilik uchun bu yetarli emas; kengroq ma'noda chidamlilik dasturning emas, tizimni quradigan va yurituvchi odamlarning xususiyati (12-bob, "And Microservice Architecture"). Ya'ni bu bobdagi timeout va circuit breaker ro'yxati to'liq bajarilgan tizim ham faqat bitta qismdan o'tgan bo'ladi.

## 7.13 Xavfni taqsimlash: bitta host, bitta fizik quti, bitta zona

Chidamlilik uchun masshtablashning bir yo'li hammasini bitta savatga solmaslik. Newman eng sodda shakldan boshlaydi: bitta hostda bir nechta servis turmasin, chunki shu hostning uzilishi bir vaqtda bir nechta servisga tegadi. Keyin esa savolni aniqlashtiradi, ya'ni "host" nimani bildiradi (Sam Newman, *Building Microservices: Designing Fine-Grained Systems*, 2-nashr, O'Reilly, 2021, 12-bob, "Spreading Your Risk" bo'limi). Bu [bulkhead](#78-nosozlik-tasirini-cheklash-bulkhead-va-alohida-resurs-hovuzlari) bilan bir xil g'oya emas: bulkhead resurs hovuzlarini ajratadi, bu bo'lim esa nusxalarning fizik joylashuvini ajratadi.

Newman uchta yashirin umumiylikni sanaydi va ularning har biri "biz ajratdik" degan ishonchni buzadi.

| Yashirin umumiylik | Nima bo'ladi | Nima tekshiriladi |
| --- | --- | --- |
| Virtual host lar bitta fizik qutida | servislar alohida host da, lekin quti yiqilsa bir nechtasi birga ketadi | virtualizatsiya platformasi host larni turli fizik qutiga tarqatishni qo'llab-quvvatlaydimi |
| VM ildiz bo'limi bitta SAN ga bog'langan | SAN yiqilsa unga ulangan hamma VM ketadi | SAN ning yagona nosozlik nuqtasi ekani hujjatda tan olinganmi |
| Hamma nusxa bitta rack yoki bitta ma'lumot markazida | rack yoki markaz darajasidagi uzilish hammasini oladi | nusxalar rack va markaz bo'yicha taqsimlanganmi |

Ikkinchi qator ayniqsa qiymatli, chunki u odatda e'tirozsiz qabul qilinadigan taxminni buzadi. Newman ichki virtualizatsiya platformalarida VM ning ildiz bo'limini bitta SAN ga biriktirish keng tarqalgan amaliyot ekanini aytadi va qo'shadi: SAN lar katta, qimmat va yiqilmaydigan qilib loyihalangan, shunga qaramay uning o'z tajribasida oxirgi o'n yilda kamida ikki marta katta va qimmat SAN yiqilgan, va har safar natija jiddiy bo'lgan (12-bob, "Spreading Your Risk").

Yashirin umumiylikning statistik oqibati ham bor va u hisobda eng ko'p qilinadigan xato. Nygard nosozliklarning mustaqil emasligini alohida ta'kidlaydi: bir qatlamdagi nosozlik boshqa qatlamdagi nosozlikning ehtimolini oshiradi, shuning uchun ehtimollarni bir-biriga ko'paytirib "bunday bo'lmaydi" degan xulosa chiqarilmaydi (Michael T. Nygard, *Release It!*, 1-nashr, Pragmatic Bookshelf, 2007, 3-bob, 41-bet). "Ikki nusxaning ikkisi ham yiqilish ehtimoli 0.001 ni 0.001 ga ko'paytiradi" shaklidagi hisob mustaqillik farazini talab qiladi, yuqoridagi jadval esa shu farazning uch marta buzilishini ko'rsatadi: bitta fizik quti, bitta SAN, bitta rack. Shu sababli risk hisobida ehtimollar ko'paytirilmaydi, balki umumiy nosozlik nuqtalari sanab chiqiladi va har biri alohida qator bo'ladi. Bir xil xato SLA larni ko'paytirishda ham chiqadi: uch bog'liqlikning har biri 99.9 foiz bo'lsa, yig'indi 99.7 foizdan yaxshi bo'lmaydi, va bog'liq nosozlik bo'lsa bu raqam ham optimistik.

Bulutda bu masala provayderning tuzilmasiga bog'lanadi. Newman AWS misolini beradi: AWS region larga bo'linadi va ularni alohida bulut deb o'ylash mumkin, har bir region esa ikki yoki undan ko'p availability zone ga bo'linadi, va bu zonalar AWS ning ma'lumot markaziga teng keladi. Xulosasi majburiy shaklda yozilgan: servislarni bir nechta availability zone ga tarqatish shart, chunki AWS yakka node ning, hatto butun bir availability zone ning mavjudligi bo'yicha hech qanday kafolat bermaydi; hisoblash servisi uchun u faqat region uchun butun holda oylik davrda 99.95 foiz ish vaqtini taklif qiladi, shuning uchun yuklarni bitta region ichidagi bir nechta zonaga tarqatish kerak bo'ladi, ba'zilar uchun esa bu ham yetmaydi va servislar bir nechta region da yuritiladi (12-bob, "Spreading Your Risk"). Ko'p region qarorining o'z narxi va shartlari bor: korpusdagi yozuvi [aktiv-passiv va aktiv-aktiv tanlovi](41-kop-region-kechikish-rezidentlik-failover.md#414-aktiv-passiv-va-aktiv-aktiv-orasidagi-tanlov) bo'limida.

Kubernetes da bu qoida sozlamaga tushadi, va asosiy xato bitta: `replicas: 3` yozib, uchta pod bitta node yoki bitta zonaga tushganini tekshirmaslik.

```yaml
# Uchta nusxa uchta zonaga va turli node ga tarqatiladi.
# topologySpreadConstraints bo'lmasa scheduler uchalasini bitta node ga qo'yishi mumkin.
apiVersion: apps/v1
kind: Deployment
metadata:
  name: order-service
spec:
  replicas: 3
  template:
    spec:
      topologySpreadConstraints:
        - maxSkew: 1
          topologyKey: topology.kubernetes.io/zone   # availability zone bo'yicha
          whenUnsatisfiable: DoNotSchedule
          labelSelector:
            matchLabels: { app: order-service }
        - maxSkew: 1
          topologyKey: kubernetes.io/hostname        # node bo'yicha
          whenUnsatisfiable: ScheduleAnyway
          labelSelector:
            matchLabels: { app: order-service }
```

Oxirgi qism shartnomaga tegishli va u texnik emas. Newman provayderning SLA sini bilib, unga qarab rejalashtirishni talab qiladi va aniq misol beradi: har chorakda servislaringiz to'rt soatdan ko'p o'chmasligi kerak bo'lsa, provayder esa chorakda maksimal sakkiz soat uzilishni kafolatlasa, siz yo o'z SLA ni o'zgartirasiz, yo boshqa yechim topasiz. Bundan tashqari provayder "kafolat" bergani uchun o'z javobgarligini cheklab qo'yadi, shuning uchun provayder majburiyatini bajarmasa buning sizga qanday ta'siri bo'lishini oldindan tushunib, B yoki C rejasi kerakligini aniqlab qo'yish kerak; Newman bir nechta mijozining avariyadan tiklash platformasini ataylab boshqa provayderda ushlab turganini keltiradi (12-bob, "Spreading Your Risk"). Shu raqamlarning o'z tomoningizdagi shakli [mavjudlik raqamlari](37-xarajat-slo-va-biznes-bilan-muloqot.md#377-mavjudlik-raqamlari-999-va-9999-orasidagi-amaliy-farq-va-narxi) bo'limida hisoblangan.

## 7.14 Riskni baholashdan keyin: yo'nalish, yig'indi, texnika va backlog

[7.11](#711-risk-storming-xavfni-jamoa-bilan-diagramma-ustida-topish) mashqning o'zini beradi: diagramma, mustaqil baholash, yopishtirish, kelishuv. Mashq tugagandan keyin esa stiker to'dasi qoladi va uni hisobotga, keyin ishga aylantirish kerak bo'ladi. Bu bo'lim shu ikkinchi yarmini yozadi; manbalar *Fundamentals of Software Architecture* ning risk bobi va Fairbanks ning risk-driven modeli.

**Yig'indi va vaqt bo'yicha kuzatish.** Risk matritsasidan chiqqan raqamlar risk assessment hisobotiga yig'iladi: qatorlar baholash mezonlari (mavjudlik, ishlash, masshtab, ma'lumot izchilligi), ustunlar servis yoki domen hududlari. Raqamlar ikki yo'nalishda jamlanadi, mezon bo'yicha va servis bo'yicha; kitob misolida ma'lumot izchilligi mezoni 17 ball bilan eng yuqori, mavjudlik 10 ball bilan eng past riskli, hududlar bo'yicha esa mijozni ro'yxatga olish eng ko'p, buyurtmani bajarish eng kam risk ko'taradi. Shu nisbiy raqamlarni vaqt bo'yicha kuzatish aniq foyda beradi: ular ma'lum mezon yoki hudud ichida yaxshilanish yoki yomonlashishni ko'rsatadi.

**Hisobotni filtrlab ko'rsatish.** Kitob to'liq jadvalni taqdim etmaslikni aytadi: filtrlash kontekst ichida aniq xabarni ko'rsatish uchun zarur. Yig'ilish maqsadi tizimning yuqori riskli hududlarini ko'rsatish bo'lsa, faqat yuqori risk qatorlari qoldiriladi, bu signal va shovqin nisbatini yaxshilaydi va holat haqida tiniq rasm beradi.

**Yo'nalishni belgilash.** Hisobot bitta vaqt kesimini ko'rsatadi va yaxshilanish yoki yomonlashishni aytmaydi. Yo'nalishni qo'shishda kitob tajribadan chiqqan ogohlantirish beradi: yuqoriga o'q nimani bildirishini so'raganda odamlarning qariyb 50 foizi "yomonlashmoqda", qariyb 50 foizi "yaxshilanmoqda" deb o'qiydi, chap va o'ng o'qlar bilan ham shunday. Kalit (legend) qo'shish yordam bermaydi, chunki foydalanuvchi kalitdan pastga o'tgandan keyin chalkashlik qaytadi. Shuning uchun ikki ishlaydigan shakl bor: risk bahosi yoniga universal plyus va minus belgisi, yoki o'q bilan birga u yo'naltirilgan raqamni yozish, chunki raqam kalitni keraksiz qiladi. Yo'nalishning o'zi taxmindan olinmaydi: u fitness function lar orqali uzluksiz o'lchov bilan aniqlanadi, ya'ni har mezon obyektiv tahlil qilinib trend chiqariladi.

**Noma'lum texnologiya alohida qoida.** Kitobning aniq tavsiyasi: sinalmagan yoki noma'lum texnologiyaga har doim eng yuqori risk bahosi (9) beriladi, chunki risk matritsasi bu o'lchamda ishlamaydi. Misol ham ta'limiy: bitta qatnashchi Redis keshini 9 ball bilan belgilagan, boshqalar esa unda umuman risk ko'rmagan; sababini so'raganda javob "Redis nima?" bo'lgan. Bundan ikki xulosa chiqadi. Birinchisi, dasturchilarni mashqqa olib kirish muhim: jamoadagi dasturchi texnologiyani bilmasligi arxitektor uchun umumiy risk haqidagi qimmatli ma'lumot. Ikkinchisi, bitta qatnashchi ko'rgan riskni boshqalar ko'rmasligi normal holat va u aynan muhokama qilinishi kerak bo'lgan qator.

**Ustuvorlikni manfaatdorlar bilan tasdiqlash.** Fairbanks bitta shart qo'yadi: agar arxitekturaga sarflanayotgan vaqt byudjetda sezilarli bo'lsa, vaqt va pul manfaatdorlarning ustuvorligiga mos sarflanayotganini tasdiqlash kerak. Jamoaning risk tasavvuri manfaatdorlarning tasavvuri bilan bir xil bo'lmasligi mumkin. Risk ikki o'lchamda tasniflanadi, manfaatdorlar uchun ustuvorlik va dasturchilar sezgan qiyinlik. Chegara ham aytilgan: platforma tanlovi kabi ba'zi texnik risklarni manfaatdorlar baholay olmaydi, demak ikkinchi o'lchov dasturchilarda qoladi.

**Texnikaning riskka mosligi.** Risk aniqlangandan keyin uni kamaytiradigan texnika tanlanadi, va texnikalar universal emas. Fairbanks jismoniy dunyo bilan taqqoslaydi: bolg'a mix uchun, tornavida vint uchun; vintni bolg'alash mumkin, lekin natija yomon. Dasturiy tomonda moslik shunday ko'rinadi.

| Risk | Mos texnika |
|---|---|
| Ishonchlilik (reliability) | rate monotonic analysis |
| Xavfsizlik (security) | threat modeling |
| Ishlash (performance) | queueing theory, throughput modellashtirish |

Qo'shimcha mezon viewtype bo'yicha moslik: modifiability ni modul ko'rinishidan, ishlashni runtime ko'rinishidan, xavfsizlikni deployment va modul ko'rinishidan o'ylash osonroq, yagona nosozlik nuqtalarini esa modul ko'rinishi emas, allocation ko'rinishi ochadi. Bu korpusda shu uchta ko'rinish [03-bob](03-qaror-qabul-qilish-va-uni-hujjatlashtirish.md) dagi qaror yozuvi bilan birga ishlatiladi.

**Risk backlog va story darajasi.** Iteratsiya oxirida har risk uchun "faoliyat riskni yetarlicha kamaytirdimi" degan savol beriladi. Ko'p holda risk radardan tushadi, lekin tushmasa Fairbanks ni qoidasi aniq: risk tizim uchun **testlanadigan** element sifatida yozib qo'yiladi, va shu risk backlog ining boshlanishi bo'ladi. Kichik risklar iteratsiya ichida hal qilinadi va backlog ga umuman chiqmaydi, kattalari esa xususiyat kabi rejalashtiriladi. Bitta backlog da xususiyat va riskni birga yuritish ustuvorlashni murakkablashtiradi, lekin kitobning tavsiyasi shunday: product owner ga arxitektura risklarini ham ustuvorlash mas'uliyati beriladi va dasturchilar unga texnik riskni tushuntiradi. Misol ham tanish: product owner backlog ning pastida "xavfsizlik" ni ko'radi, dasturchilar esa uni xavfsizlikni keyin qo'shib bo'lmasligini tushuntirishi kerak.

Shu bilan birga *Fundamentals of Software Architecture* risk matritsasini user story ga ham qo'llaydi: birinchi o'lcham story iteratsiya ichida bajarilmasa umumiy ta'siri, ikkinchisi bajarilmaslik ehtimoli. Story grooming da shu ikki o'lchov bilan yuqori riskli story lar ajratiladi, ularni diqqat bilan kuzatish va ustuvorlashtirish mumkin bo'ladi, hamda iteratsiyaning umumiy risk bahosi chiqadi.

Natijada [7.10](#710-nosozlik-ssenariylarini-oldindan-yozish-nima-bolsa-nima-qilamiz-jadvali) dagi ssenariy jadvali, 7.11 dagi mashq va bu bo'limdagi hisobot bitta zanjir bo'ladi: mashq risk topadi, hisobot uni yig'indi va yo'nalish bilan ko'rsatadi, backlog esa uni testlanadigan ishga aylantiradi. Zanjirning har qadamida mezon bir xil, ehtimol va ta'sir ko'paytmasi.

## 7.15 Amalda qo'llash

- [ ] Servisdagi barcha tashqi chaqiruvlarni sanab, timeout qo'yilmaganlarini topib, har biriga SLO dan kelib chiqqan aniq qiymat belgilash.
- [ ] Little qonuni bilan hisoblab ko'rish: eng muhim downstream o'n barobar sekinlashgan ssenariyni oling, thread pool va connection pool qachon to'ladi va qancha so'rov rad etiladi.
- [ ] Retry siyosatini bitta qatlamga yig'ish, jitter qo'shish va retry byudjetini umumiy oqimning 10 foizi darajasida cheklash.
- [ ] To'lov va buyurtma yozuvlariga idempotency key maydoni va unique index qo'shib, takroriy so'rovni baza darajasida to'xtatish.
- [ ] Funksiyalarni majburiy, muhim va qo'shimcha guruhlarga ajratib, har bir muhim funksiya uchun zaxira javobni product egasi bilan yozma kelishib olish.
- [ ] Hisobot va OLTP uchun alohida DataSource bean'lari ajratib, pool o'lchamlarini mustaqil belgilash.
- [ ] `pg_stat_replication` dagi `flush_lag` bo'yicha alert yoqib, haqiqiy RPO ni o'lchangan raqam sifatida hujjatga yozish.
- [ ] Backup'dan tiklashni haftalik avtomatik test qilib, RTO ni besh qismi bilan (aniqlash, qaror, failover, qayta ulanish, cache isishi) o'lchash.
- [ ] Dizayn hujjatiga besh ustunli ssenariy jadvalini kiritib, kamida 15 ta ssenariy yozish va ulardan uchtasini haqiqatan sinab ko'rish.

## Manbalar

- Michael T. Nygard, *Release It! Design and Deploy Production-Ready Software*, 1-nashr, Pragmatic Bookshelf, 2007, 4-bob - Integration Points (54-57-betlar: timeout'siz chaqiruv, Linux `tcp_retries2` default 15 qayta uzatish taxminan 20 daqiqalik timeout beradi, firewall ulanish jadvali), Chain Reactions (61-bet), Cascading Failures (65-bet), Blocked Threads (81-bet), Unbalanced Capacities (98-bet), Slow Responses (100-bet), degradatsiya (104-bet)
- Michael T. Nygard, *Release It!*, 1-nashr, 2007, 4.1, 50-bet - sekin javob javob bermaslikdan yomonroq; tez va sekin xatoni ajratish; kaskad nosozlik belgilari
- Michael T. Nygard, *Release It!*, 1-nashr, 2007, 5-bob - Use Timeouts (111-114-betlar: "hope is not a design method", navbatga qo'yib keyin qayta urinish), Circuit Breaker (115-118-betlar: timeout bilan juftlik, kalit ochiq bo'lgandagi javob biznes qarori), Bulkheads (119 va 122-betlar: kema bo'limlari analogiyasi, thread pool'ni ajratish), Steady State (124-bet), Fail Fast (131-bet), Handshaking (134-bet), Test Harness (136-bet)
- Simon Brown, *Software Architecture for Developers*, Leanpub, 2014, 64-bob - Risk-storming (181-183-betlar: to'rt qadam, xavfni mustaqil va sukutda yozish, 5-10 daqiqalik cheklov, stikerni diagrammaga yopishtirish, Planning Poker uslubida umumiy bahoga kelish, uchta yumshatish yo'li, ehtimoli yoki ta'siri "yo'q" bo'lgan xavfni ham jurnalda saqlash)
- Simon Brown, *Software Architecture for Developers*, Leanpub, 2014, 64-bob, "Collective ownership" (184-bet: xavf reyestri odatda texnik bo'lmagan loyiha menejerida bo'ladi, texnik xavflarning egasi esa arxitektura roli bo'lishi kerak)
- Sam Newman, *Building Microservices: Designing Fine-Grained Systems*, 2-nashr, O'Reilly, 2021, 12-bob ("What Is Resiliency?", "Robustness", "Rebound", "Graceful Extensibility", "Sustained Adaptability", "And Microservice Architecture" bo'limlari) - David D. Woods ning chidamlilik tasnifi va to'rt qismi; robustness oldingi bilimni talab qilishi va odamlarga ham tegishli ekani (yakka on-call), robustness ni oshirish murakkablik qo'shishi; yassi tashkilotning kutilmaganga yaxshiroq tayyorligi, avtomatlashtirishning kutilmaganni boshqarmasligi va odam ko'nikmasi bilan mas'uliyatining zarurati; Woods ning "ilgari muvaffaqiyatli bo'lganimiz kelajak uchun kafolat emas" gapi, chaos engineering ning o'rni, butun tizimga qarash va ayblamaslik madaniyati talabi, qisqa muddatli yetkazib berish bilan uzoq muddatli moslashish muvozanati; mikroservisning faqat robustness ga yordam berishi va chidamlilik odamlarning xususiyati ekani. Bu nashrning qo'limizdagi elektron nusxasida barqaror bet raqami yo'q, shuning uchun faqat bob va bo'lim nomi ko'rsatilgan
- Sam Newman, *Building Microservices: Designing Fine-Grained Systems*, 2-nashr, O'Reilly, 2021, 12-bob ("Spreading Your Risk" bo'limi) - bitta hostda bir nechta servis turmasligi, "host" ning virtual tushuncha ekani va virtual host larni turli fizik qutiga tarqatish, VM ildiz bo'limining bitta SAN ga bog'lanishi va muallif tajribasida o'n yilda kamida ikki marta SAN yiqilgani, rack va ma'lumot markazi bo'yicha tarqatish, AWS region va availability zone tuzilmasi, yakka node yoki butun zona uchun kafolat yo'qligi va hisoblash servisi uchun region bo'yicha oylik 99.95 foiz ko'rsatkichi, provayder SLA sidagi to'rt va sakkiz soat misoli, provayderning javobgarlikni cheklashi va boshqa provayderdagi zaxira platforma
- Mark Richards, Neal Ford, *Fundamentals of Software Architecture*, O'Reilly, 2020, 9-bob ("Fallacy #5: The Topology Never Changes" bo'limi) - tarmoq topologiyasi doim o'zgarishi, "kichik" yangilanish latency farazlarini buzib timeout va circuit breaker larni ishga tushirishi, arxitektorning operations va tarmoq administratorlari bilan doimiy aloqasi
- Mark Richards, Neal Ford, *Fundamentals of Software Architecture*, O'Reilly, 2020, 20-bob ("Risk Assessments", "Consensus", "Agile Story Risk Analysis" bo'limlari) - risk assessment hisoboti, mezon va domen bo'yicha yig'indi hamda vaqt bo'yicha kuzatish, yuqori riskni filtrlab ko'rsatish (signal va shovqin), yo'nalishni plyus-minus yoki o'q bilan raqam orqali belgilash va odamlarning o'qni turlicha o'qishi, yo'nalishni fitness function lardan olish, noma'lum yoki sinalmagan texnologiyaga eng yuqori risk (9) berish va Redis misoli, risk matritsasini user story ga qo'llash. Qo'limizdagi nusxada chop etilgan bet raqami yo'q, shuning uchun faqat bob va bo'lim nomi ko'rsatilgan
- George Fairbanks, *Just Enough Software Architecture*, 1-nashr, 2010, 3.3 - arxitektura sarfi byudjetda sezilarli bo'lsa risk ustuvorligini manfaatdorlar bilan tasdiqlash, riskning ikki o'lchami (manfaatdor ustuvorligi va dasturchi sezgan qiyinlik) va platforma tanlovi kabi texnik riskni manfaatdorlar baholay olmasligi; 3.5 - texnikalarning riskka mosligi (rate monotonic analysis va reliability, threat modeling va security, queueing theory va performance) hamda viewtype bo'yicha moslik; 3.11 - riskni testlanadigan element sifatida backlogga yozish, kichik riskni iteratsiya ichida hal qilish, katta riskni xususiyat kabi rejalashtirish va bitta feature-risk backlog
- Martin Kleppmann, *Designing Data-Intensive Applications*, 1-nashr, O'Reilly, 2017, 1-bob (7-bet) - davolab bo'ladigan nosozlikda chidamlilik, davolab bo'lmaydigan joyda (maxfiy ma'lumot sizib chiqishi) oldini olish afzalligi
- Sam Newman, *Building Microservices: Designing Fine-Grained Systems*, 2-nashr, O'Reilly, 2021, 4-bob - Tanenbaum va Steen ning *Distributed Systems* kitobidan jarayonlararo aloqadagi besh nosozlik turi (crash, omission, timing, response, arbitrary yoki Byzantine), ularning ko'pi vaqtinchalik ekani va mijozning qayta urinish hamda inson aralashuvini ajrata olishi talabi, HTTP ning 400 va 500 toifalari misolida. Bu nashrning qo'limizdagi elektron nusxasida barqaror bet raqami yo'q, shuning uchun faqat bob ko'rsatilgan
- Michael T. Nygard, *Release It!*, 1-nashr, Pragmatic Bookshelf, 2007, 3-bob (36, 37 va 41-betlar) - yuqori barqarorlikdagi dizayn barqarorsiz dizayn bilan deyarli bir xil narxga tushishi; impulse (zarba) va stress (uzoq davomli kuch) farqi hamda stress hosil qiladigan strain ning tizimning uzoq nuqtasida ko'rinishi; nosozliklarning mustaqil emasligi, bir qatlamdagi nosozlikning boshqasining ehtimolini oshirishi va ehtimollarni ko'paytirib xulosa chiqarib bo'lmasligi
- Michael T. Nygard, *Release It!*, 1-nashr, Pragmatic Bookshelf, 2007, 5-bob (121-bet) - bo'linish chegarasini biznes ta'siri bilan arxitekturani kesishtirib topish va chegaraning chaqiruvchi, funksionallik yoki topologiya bo'yicha o'tishi
- ESLATMA: 7.1 dagi `statement_timeout` qiymatlari va p99 sabablari ro'yxati haqidagi tavsiya, 7.2 dagi Tanenbaum turlarini korpus to'rtligiga moslash jadvali va "oxirgi event vaqti" metrikasi, 7.14 dagi viewtype va qaror yozuvi bog'lanishi shu korpusning qo'shimchasi
- ESLATMA: mavjud nusxa 1-nashr (2007). 2-nashrda (2018) pattern ro'yxati kengaytirilgan va bir qismi qayta nomlangan (masalan "Attacks of Self-Denial" va "Use Timeouts" nomlari o'zgargan), shuning uchun 2-nashrga xos nomlar bu yerda iqtibos qilinmaydi
- ESLATMA: 7.2 dagi to'rt turlik taksonomiya, 7.3 dagi Little qonuni va timeout byudjeti, 7.4 dagi retry byudjeti foizi va jitter oraliqlari, 7.5 dagi idempotentlik yechimlari, 7.7 dagi backup qatlamlari, 7.9 dagi RTO va RPO raqamlari 7.10 dagi ssenariy soni, 7.12 dagi on-call va runbook tavsiyasi hamda 7.13 dagi Kubernetes `topologySpreadConstraints` misoli shu korpusning amaliy tavsiyasi, kitobdan olingan emas
- ESLATMA: 7.11 dagi risk-storming Brown kitobidan olingan; Nygard ning *Release It!* 1-nashrida bu texnika yo'q

---

[&larr; 6. Murakkablikni boshqarish](06-murakkablikni-boshqarish.md) · [Mundarija](README.md) · [8. Ishlash va resurs hissi: napkin math &rarr;](08-ishlash-va-resurs-hissi-napkin-math.md)
