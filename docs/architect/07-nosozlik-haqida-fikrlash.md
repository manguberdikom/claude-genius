<!-- doc: architect | chapter: 7 | part: I. Fikrlash va qarorlar -->

[Barcha hujjatlar](../../README.md) / [Arxitektor miyasi](README.md)

> Holat: AI yozgan, inson tekshirmagan.

# 7. Nosozlik haqida fikrlash (Thinking About Failure)

<details>
<summary>Bu bobdagi 11 bo'lim</summary>

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
- [7.11 Amalda qo'llash](#711-amalda-qollash)

</details>



Nosozlik haqida fikrlash arxitektorni developerdan ajratadigan eng aniq chegara. Developer "bu kod ishlaydi" deb o'ylaydi, arxitektor "bu kod qachon va qanday ishlamaydi" deb so'raydi. Bu bob pattern katalogi emas: bu yerda nosozlikning mexanikasi, uning raqamlari va shu raqamlardan chiqadigan qarorlar bor. Har bir bo'limda siz jamoadan nimani so'rashingiz va qanday son kelishib olishingiz kerakligi ko'rsatilgan.

## 7.1 Hamma narsa buziladi: tarmoq, disk, protsess, boshqa servis

Taqsimlangan tizimda nosozlik hodisa emas, doimiy holat. Tarmoq paketi yo'qoladi, TCP ulanish NAT jadvalidan tushib qoladi, disk fsync'ni 400 ms kechiktiradi, JVM 3 sekundlik full GC ga ketadi, Kubernetes node'ni evict qiladi. Bu ro'yxatning har bir bandi oyda bir necha marta sodir bo'ladi, va ularning hech biri sizning kodingizdagi bug emas.

Arxitektor har bir tashqi chaqiruv uchun uchta savolga javob tayyorlaydi. Bu chaqiruv eng ko'p qancha kutadi. Kutish tugagach nima bo'ladi. Chaqiruv ikkinchi marta bajarilsa, biznes natija buziladimi.

Eng ko'p uchraydigan xato: timeout belgilanmagan chaqiruv. Spring'da `RestClient` yoki `WebClient` da timeout qo'yilmasa, OS darajasidagi TCP retransmission limitiga tayanadi, bu Linux'da taxminan 15 minutgacha cho'ziladi.

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

## 7.2 Nosozlik turlari: to'liq to'xtash, sekinlashuv, qisman javob, yolg'on javob

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
| Timeout'siz tashqi chaqiruv | default qiymat OS darajasida, 15 minutgacha | har client uchun aniq timeout, SLO dan kichik |
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

## 7.11 Amalda qo'llash

- [ ] Servisdagi barcha tashqi chaqiruvlarni sanab, timeout qo'yilmaganlarini topib, har biriga SLO dan kelib chiqqan aniq qiymat belgilash.
- [ ] Little qonuni bilan hisoblab ko'rish: eng muhim downstream 10 barobar sekinlashsa, thread pool va connection pool qachon to'ladi va qancha so'rov rad etiladi.
- [ ] Retry siyosatini bitta qatlamga yig'ish, jitter qo'shish va retry byudjetini umumiy oqimning 10 foizi darajasida cheklash.
- [ ] To'lov va buyurtma yozuvlariga idempotency key maydoni va unique index qo'shib, takroriy so'rovni baza darajasida to'xtatish.
- [ ] Funksiyalarni majburiy, muhim va qo'shimcha guruhlarga ajratib, har bir muhim funksiya uchun zaxira javobni product egasi bilan yozma kelishib olish.
- [ ] Hisobot va OLTP uchun alohida DataSource bean'lari ajratib, pool o'lchamlarini mustaqil belgilash.
- [ ] `pg_stat_replication` dagi `flush_lag` bo'yicha alert yoqib, haqiqiy RPO ni o'lchangan raqam sifatida hujjatga yozish.
- [ ] Backup'dan tiklashni haftalik avtomatik test qilib, RTO ni besh qismi bilan (aniqlash, qaror, failover, qayta ulanish, cache isishi) o'lchash.
- [ ] Dizayn hujjatiga besh ustunli ssenariy jadvalini kiritib, kamida 15 ta ssenariy yozish va ulardan uchtasini haqiqatan sinab ko'rish.

---

[&larr; 6. Murakkablikni boshqarish](06-murakkablikni-boshqarish.md) · [Mundarija](README.md) · [8. Ishlash va resurs hissi: napkin math &rarr;](08-ishlash-va-resurs-hissi-napkin-math.md)
