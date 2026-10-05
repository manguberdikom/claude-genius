<!-- doc: architect | chapter: 1 | part: I. Fikrlash va qarorlar -->

[Barcha hujjatlar](../../README.md) / [Arxitektor miyasi](README.md)

# 1. Arxitektorning fikrlash modeli (The Architect's Mental Model)

<details>
<summary>Bu bobdagi 11 bo'lim</summary>

- [1.1 Arxitektor va senior developer o'rtasidagi haqiqiy farq](#11-arxitektor-va-senior-developer-ortasidagi-haqiqiy-farq)
- [1.2 Kontekst birinchi: biznes maqsadi, jamoa kattaligi, muddat, byudjet](#12-kontekst-birinchi-biznes-maqsadi-jamoa-kattaligi-muddat-byudjet)
- [1.3 Trade-off tili: bepul qaror yo'q, har birining narxi bor](#13-trade-off-tili-bepul-qaror-yoq-har-birining-narxi-bor)
- [1.4 Sifat atributlari va ularni o'lchash](#14-sifat-atributlari-va-ularni-olchash)
- [1.5 Qaytarib bo'ladigan va qaytarib bo'lmaydigan qarorlar](#15-qaytarib-boladigan-va-qaytarib-bolmaydigan-qarorlar)
- [1.6 "Yetarlicha yaxshi" arxitektura, over-engineering va YAGNI chegarasi](#16-yetarlicha-yaxshi-arxitektura-over-engineering-va-yagni-chegarasi)
- [1.7 Hozirgi talab va kelajak taxmini orasidagi muvozanat](#17-hozirgi-talab-va-kelajak-taxmini-orasidagi-muvozanat)
- [1.8 Arxitektura qarori qanday eskiradi va uni qachon qayta ko'rish kerak](#18-arxitektura-qarori-qanday-eskiradi-va-uni-qachon-qayta-korish-kerak)
- [1.9 Kod yozmaydigan arxitektor nega haqiqatdan uzoqlashadi](#19-kod-yozmaydigan-arxitektor-nega-haqiqatdan-uzoqlashadi)
- [1.10 O'z fikrlashini tekshirish uchun savollar ro'yxati](#110-oz-fikrlashini-tekshirish-uchun-savollar-royxati)
- [1.11 Amalda qo'llash](#111-amalda-qollash)

</details>



Arxitektorning ishi diagramma chizish emas. Uning ishi noaniq biznes talabini o'lchanadigan texnik cheklovga aylantirish va har bir qarorning narxini oldindan aytib berish. Shu sababli arxitektorning fikrlash modeli kod yozish mahoratidan emas, kontekstni o'qish va trade-off ni raqamda ko'rsatish qobiliyatidan boshlanadi. Bu bobda shu model ichidan o'tamiz: kontekst, trade-off, sifat atributlari, qarorning qaytarilish darajasi va qarorning eskirishi.

## 1.1 Arxitektor va senior developer o'rtasidagi haqiqiy farq

Senior developer berilgan masalani eng yaxshi tarzda yechadi. Arxitektor masalaning o'zi to'g'ri qo'yilganini tekshiradi. Farq mahoratda emas, javobgarlik ufqida. Senior bitta servis va bitta sprint doirasida o'ylaydi, arxitektor esa uch yildan keyin shu servisni kim qo'llab-quvvatlaydi deb o'ylaydi.

Ikkinchi farq: senior "qanday qilib" degan savolga javob beradi, arxitektor "nega aynan shunday" degan savolga javob beradi. To'lov servisida senior idempotentlik kalitini `UNIQUE` indeks bilan amalga oshiradi. Arxitektor esa idempotentlik oynasi qancha vaqt saqlanishini, eski kalitlarni kim tozalashini va bu jadval bir yilda qancha o'sishini hisoblaydi.

Uchinchi farq: arxitektor o'z qarorini yozib qoldiradi. Yozilmagan qaror olti oydan keyin yo'qoladi. Shu sababli arxitektorning asosiy chiqishi kod emas, qaror yozuvi va o'lchov mezoni.

| Vaziyat | Oddiy yondashuv | Arxitektor yondashuvi |
| --- | --- | --- |
| Yangi talab keldi | Darhol texnik yechim tanlaydi | Avval biznes maqsadi va cheklovlarni so'raydi |
| Texnologiya tanlash | "Zamonaviy" va mashhur variantni oladi | Jamoa tajribasi va operatsion narxni hisoblaydi |
| Performance muammosi | Kodni optimallashtirishga kirishadi | Avval o'lchaydi, keyin eng qimmat qismni tanlaydi |
| Microservice bo'lish | Domen bo'ylab darhol ajratadi | Modulli monolit bilan boshlab, chegarani tekshiradi |
| Cache qo'shish | TTL ni 5 daqiqa qilib qo'yadi | Stale ma'lumot biznesga qancha turishini so'raydi |
| Kutubxona qo'shish | Tez yechim uchun qo'shadi | Yangilash, CVE va transitive bog'liqlikni ko'radi |
| Qaror yozuvi | Og'zaki aytib o'tadi | ADR yozadi, alternativani va narxini qayd qiladi |
| Kelajak talabi | "Keyin kerak bo'ladi" deb mavhum qoldiradi | Taxminni yozadi va qachon tekshirishni belgilaydi |
| Latency maqsadi | "Tez bo'lsin" deydi | p99 uchun aniq raqam va o'lchash usulini beradi |
| Xato holati | Happy path ni yopadi | Timeout, retry va degradatsiya rejimini aniqlaydi |

## 1.2 Kontekst birinchi: biznes maqsadi, jamoa kattaligi, muddat, byudjet

Bir xil talab ikki kompaniyada ikki xil arxitekturaga olib keladi. Sababi kontekst: biznes maqsadi, jamoa kattaligi va tajribasi, muddat, byudjet. Shu to'rttasini yozmagan arxitektor taxmin bilan ishlaydi.

Biznes maqsadi qaysi sifat atributi birinchi o'rinda turishini aytadi. To'lov servisida ma'lumot to'g'riligi latency dan ustun. Omborda qoldiq ko'rsatadigan katalog sahifasida esa latency to'g'rilikdan ustun, chunki bir soniya kechikish konversiyani yo'qotadi. Shu bitta jumla keyingi o'nta qarorni belgilaydi.

Jamoa kattaligi operatsion yukning chegarasini belgilaydi. Besh kishilik jamoa uchun o'n ikki microservice va Kafka klasteri xarajat, qobiliyat emas. Taxminan har bir mustaqil deploy qilinadigan servis haftada bir necha soat operatsion yuk qo'shadi. Shu yukni ko'taradigan odam yo'q bo'lsa, qaror noto'g'ri.

Muddat va byudjet qarorni kesadi. Uch oyda MVP kerak bo'lsa, PostgreSQL ichidagi `FOR UPDATE SKIP LOCKED` navbati broker o'rnini bosadi. Bu ongli vaqtinchalik yechim.

```sql
-- Oddiy navbat: PostgreSQL ichida, broker o'rnatmasdan.
-- SKIP LOCKED bir nechta worker bir-birini kutmasligini ta'minlaydi.
CREATE TABLE payment_outbox (
    id          bigserial PRIMARY KEY,
    aggregate_id uuid        NOT NULL,
    payload     jsonb       NOT NULL,
    status      text        NOT NULL DEFAULT 'NEW',
    attempts    int         NOT NULL DEFAULT 0,
    next_try_at timestamptz NOT NULL DEFAULT now()
);

-- Faqat ishlov berilmagan qatorlar uchun indeks: jadval o'sganda ham kichik qoladi.
CREATE INDEX payment_outbox_pending_idx
    ON payment_outbox (next_try_at)
    WHERE status = 'NEW';

-- Worker bir martada 100 qator oladi, boshqa worker ularni ko'rmaydi.
SELECT id, payload
  FROM payment_outbox
 WHERE status = 'NEW' AND next_try_at <= now()
 ORDER BY next_try_at
 LIMIT 100
 FOR UPDATE SKIP LOCKED;
```

Bu yondashuv taxminan sekundda bir necha mingta xabarga yetadi. Shundan keyin broker kerak bo'ladi. Qaror yozuvida aynan shu chegara ko'rsatilishi kerak.

## 1.3 Trade-off tili: bepul qaror yo'q, har birining narxi bor

Arxitektura qarorining birinchi qonuni oddiy: har bir foyda biror narsa hisobidan keladi. Cache latency ni pasaytiradi va ma'lumot yangiligini yo'qotadi. Replika o'qish yukini bo'ladi va replication lag keltiradi. Async ishlov berish javobni tezlashtiradi va xatoni ko'rinmas qiladi. Shu sababli arxitektor "yaxshiroq" degan so'z o'rniga "nima hisobidan" deb so'raydi.

Amaliy shakli bor: har bir qaror uchun bitta jumla yozish. "X ni oldik, chunki Y ni yaxshilaydi, buning narxi Z, va Z ni W bilan kuzatamiz." Bu jumla yozilmasa, qaror muhokama emas, didga aylanadi.

Misol: buyurtma servisida read replika qo'shish. Foyda: master dagi o'qish yuki taxminan 60 foizga kamayadi. Narx: foydalanuvchi buyurtma yaratgandan keyin uni ro'yxatda darhol ko'rmasligi mumkin. Lag odatda 10 dan 200 millisekundgacha, lekin yuk ostida sekundlarga chiqadi. Yechim: yozuvdan keyingi o'qish master ga yo'naltiriladi.

```java
// Tranzaksiya darajasida qaysi ma'lumotlar bazasiga borishni tanlash.
// readOnly = true bo'lgan tranzaksiya replika ga yo'naltiriladi.
@Service
public class OrderQueryService {

    private final OrderRepository orders;

    // Ro'yxat eskirishi mumkin: 200 ms lag biznes uchun qabul qilinadi.
    @Transactional(readOnly = true)
    public List<OrderView> recentOrders(long customerId) {
        return orders.findTop20ByCustomerIdOrderByCreatedAtDesc(customerId);
    }

    // Yangi yaratilgan buyurtmani ko'rsatish: lag qabul qilinmaydi.
    // readOnly berilmaydi, shuning uchun master ga boradi.
    @Transactional
    public OrderView justCreated(long orderId) {
        return orders.findById(orderId)
                     .map(OrderView::from)
                     .orElseThrow();
    }
}
```

Bu yerda muhimi marshrutlash mexanizmi emas, balki shu: qaysi so'rov eskirgan ma'lumotga toqat qiladi degan savolga biznes javob bergan.

## 1.4 Sifat atributlari va ularni o'lchash

Sifat atributi o'lchanmasa, u talab emas, istak. "Tizim tez bo'lsin" degan gap qaror chiqarmaydi. "Buyurtma yaratish p99 kechikishi 300 millisekunddan oshmasin, kunlik pik yukda, 95 foiz kunlarda" degan gap qaror chiqaradi. Shu sababli arxitektor har bir atributga stsenariy, raqam va o'lchash nuqtasini beradi.

Latency ni o'rtacha qiymat bilan o'lchash eng keng tarqalgan xato. O'rtacha 80 millisekund bo'lgan tizimda p99 ikki sekund bo'lishi mumkin. Foydalanuvchi o'rtachani sezmaydi, u o'z so'rovini sezadi. Shu sababli p95 va p99 o'lchanadi, mean esa faqat qo'shimcha sifatida.

Throughput va latency bir-biriga bog'liq. Pool to'lganda navbat paydo bo'ladi va latency keskin o'sadi. Agar bir so'rov bazani 50 millisekund egallasa, 20 ta ulanish bilan nazariy maksimum taxminan 400 so'rov/sekund bo'ladi.

```properties
# Pool kattaligini "kattaroq yaxshiroq" deb emas, hisob bilan qo'yamiz.
# PostgreSQL da har bir ulanish alohida backend process, xotira hisobi bor.
spring.datasource.hikari.maximum-pool-size=20
spring.datasource.hikari.minimum-idle=20
# Pool bo'sh bo'lmasa, 2 sekunddan ko'p kutmaymiz: tez xato yaxshi.
spring.datasource.hikari.connection-timeout=2000
# Ulanishni 20 daqiqada yangilaymiz, DNS va failover uchun.
spring.datasource.hikari.max-lifetime=1200000
# Ochiq qolgan ulanishni 10 sekundda log ga yozadi.
spring.datasource.hikari.leak-detection-threshold=10000

# Histogram va SLO chegaralari: p99 ni server tomonda o'lchaymiz.
management.metrics.distribution.percentiles-histogram.http.server.requests=true
management.metrics.distribution.slo.http.server.requests=200ms,300ms,500ms,1s
management.endpoints.web.exposure.include=health,metrics,prometheus
```

Availability ni foizda emas, yo'qotilgan daqiqada o'ylash foydali. 99.9 foiz oyda taxminan 43 daqiqa to'xtash degani. 99.99 foiz esa taxminan 4 daqiqa. Ikkinchisi odatda ikki baravar emas, besh baravar qimmat, chunki u avtomatik failover, ko'p zona va mashq qilingan runbook talab qiladi.

Maintainability ham o'lchanadi: o'zgarishdan prod gacha o'tgan vaqt, bitta oddiy o'zgarish uchun tegiladigan modul soni, yangi odam birinchi PR ni qancha kunda yuboradi. Bu raqamlar ko'rinmasa, "toza arxitektura" suhbati did bo'lib qoladi.

```bash
# Sifat atributini o'lchashni gapdan emas, skriptdan boshlang.
# 1) Bazadagi eng qimmat so'rovlarni toping (pg_stat_statements kerak).
psql -c "SELECT calls, round(mean_exec_time::numeric,2) AS avg_ms,
                round(total_exec_time::numeric/1000,1) AS total_s, query
           FROM pg_stat_statements
          ORDER BY total_exec_time DESC LIMIT 10;"

# 2) Konkret so'rovning rejasini real buferlar bilan ko'ring.
psql -c "EXPLAIN (ANALYZE, BUFFERS) SELECT * FROM orders
          WHERE customer_id = 42 ORDER BY created_at DESC LIMIT 20;"

# 3) Pool chegarasini yuk ostida tekshiring, taxminiy emas.
pgbench -c 40 -j 4 -T 60 -S orders_db

# 4) Servis tomonidagi p99 ni Prometheus formatidan o'qing.
curl -s localhost:8080/actuator/metrics/http.server.requests \
  | head -c 400
```

## 1.5 Qaytarib bo'ladigan va qaytarib bo'lmaydigan qarorlar

Qarorlarni muhimlik bo'yicha emas, qaytarilish narxi bo'yicha saralash kerak. Qaytarib bo'ladigan qaror uchun uzoq muhokama vaqtni behuda sarflaydi. Qaytarib bo'lmaydigan qaror uchun tez qaror esa yillarga cho'ziladigan qarz yaratadi.

Odatda arzon qaytariladigan qarorlar: ichki kutubxona tanlovi, cache TTL, log formati, bitta endpoint ning shakli. Qimmat qaytariladigan qarorlar: ma'lumot modeli va jadval bo'linishi, servis chegaralari, public API kontrakti, autentifikatsiya modeli, multi-tenancy strategiyasi. Eng qimmati odatda ma'lumotga tegishli bo'ladi, chunki ma'lumot migratsiya qilinadi, kod esa qayta yoziladi.

Qaytarilish narxini kamaytirishning amaliy usuli bor: qarorni interfeys ortiga yashirish. Agar to'lov provayderi tanlovi noaniq bo'lsa, domen kodi provayder SDK sini ko'rmasligi kerak.

```java
// Domen faqat shu portni biladi, provayder nomini bilmaydi.
// Shu sababli provayderni almashtirish adapter almashtirishga aylanadi.
public interface PaymentGateway {
    PaymentResult charge(ChargeCommand command);
    RefundResult refund(RefundCommand command);
}

// Idempotentlik kaliti domen qarori, provayder detali emas.
public record ChargeCommand(
        String idempotencyKey,
        long orderId,
        BigDecimal amount,
        String currency) { }

// Adapter qatlamida provayderning xato kodlari domen xatosiga ko'chiriladi.
@Component
class AcquirerPaymentGateway implements PaymentGateway {

    @Override
    public PaymentResult charge(ChargeCommand command) {
        // Timeout va retry siyosati shu yerda, domen ichida emas.
        // Tarmoq xatosi "noma'lum natija" deb qaytariladi, "xato" deb emas.
        return PaymentResult.unknownIfTimeout(command.idempotencyKey());
    }
    // refund ham shu adapter ichida, bir xil tamoyil bilan amalga oshiriladi.
}
```

Bu abstraksiya bepul emas, u qo'shimcha qatlam va model qo'shadi. Narxi oqlanadi, chunki aynan qaytarilishi qimmat joyni himoya qiladi. O'sha abstraksiyani har bir CRUD repository uchun qo'yish esa oqlanmaydi.

## 1.6 "Yetarlicha yaxshi" arxitektura, over-engineering va YAGNI chegarasi

Over-engineering mahoratning ortiqchasi emas, noto'g'ri yo'naltirilgan qo'rquv natijasi. Arxitektor noaniqlikni abstraksiya bilan yopishga urinadi va shu bilan noaniqlikni ko'paytiradi. Yetarlicha yaxshi arxitektura esa bugungi talabni bajaradi va ertangi o'zgarishni to'sib qo'ymaydi. Ikkinchi shart birinchisidan muhimroq.

YAGNI chegarasini belgilashning amaliy mezoni: keyin qo'shishning narxi hozir qo'shish narxidan qancha yuqori. Agar farq kichik bo'lsa, kutish kerak. Agar farq katta bo'lsa, hozir qilish kerak. Buyurtma jadvaliga `created_at` ustunini keyin qo'shish arzon. Monolit ichida tranzaksiya chegarasini keyin ajratish qimmat.

Shu mezon ikkita ro'yxat beradi. Hozir: ma'lumot modelining normal shakli, ID strategiyasi, audit maydonlari, migratsiya vositasi, korrelyatsiya ID. Keyin: ikkinchi baza, CQRS read modeli, event sourcing, o'z service mesh i.

| Tuzoq | Nega yuzaga keladi | Yechim |
| --- | --- | --- |
| Har bir servisga alohida baza "kelajak uchun" | Microservice qoidasini kontekstsiz qo'llash | Modulli monolit, schema bo'yicha ajratish, chegara test bilan tekshirilsin |
| Barcha narsaga interfeys va bitta implementatsiya | Testlash uchun kerak degan noto'g'ri odat | Interfeys faqat haqiqiy almashuv nuqtasida qoldirilsin |
| Event sourcing ni hisobot uchun tanlash | Audit talabini noto'g'ri o'qish | Audit jadvali yoki temporal ustunlar yetadi |
| Cache ni o'lchamasdan qo'shish | Latency muammosi taxmin qilingan | Avval so'rov rejasi va indeks tekshirilsin |
| Mavhum "konfiguratsiya dvigateli" | Kelajakdagi talab taxmin qilingan | Kodda qattiq yozilsin, uchinchi holatda umumlashtirilsin |
| Barcha chaqiruvni async qilish | Javob vaqtini yashirish istagi | Async faqat biznes toqat qiladigan joyda, outbox bilan |
| Pool va thread sonini katta qo'yish | "Ko'proq parallel tezroq" degan taxmin | Pool past yuk sinovidan kelib chiqib, backpressure bilan |
| Qaror yozuvining yo'qligi | Yozish vaqt oladi deb hisoblash | Bir sahifali ADR, kontekst, alternativa, narx |

## 1.7 Hozirgi talab va kelajak taxmini orasidagi muvozanat

Kelajakni inkor qilish ham xato. To'g'ri yondashuv kelajakni taxmin sifatida yozib qo'yish va unga tekshirish nuqtasi belgilash. Taxmin yozilganda u muhokama qilinadigan narsaga aylanadi. Yozilmaganda u kodda yashiringan farazga aylanadi.

Taxminni raqam bilan yozish kerak. "Buyurtmalar o'sadi" emas, balki "kunlik buyurtma hozir 20 ming, bir yilda 80 ming, bu sekundda taxminan 3 yozuv". Shu raqam bitta PostgreSQL instansi yetarli ekanini ko'rsatadi. O'n baravar oshsa, partitioning masalasi ochiladi.

Amaliy usul: bugungi kodni sodda qoldirib, kelajakni kengaytirish nuqtasi bilan ta'minlash. Jadvalni hozir bo'lmagan, lekin bo'linishga tayyor qilib loyihalash shunga misol.

```sql
-- Hozir bitta jadval yetadi, lekin kalit partition ga tayyor.
-- Birlamchi kalitga created_at kiritilgani keyingi migratsiyani arzonlashtiradi.
CREATE TABLE orders (
    id          bigserial,
    customer_id bigint      NOT NULL,
    status      text        NOT NULL,
    total       numeric(14,2) NOT NULL,
    created_at  timestamptz NOT NULL DEFAULT now(),
    PRIMARY KEY (id, created_at)
);

-- Eng ko'p ishlatiladigan so'rov uchun kompozit indeks.
CREATE INDEX orders_customer_recent_idx
    ON orders (customer_id, created_at DESC);

-- Kelajakda oylik partition ga o'tish: struktura allaqachon mos.
-- ALTER TABLE orders ... PARTITION BY RANGE (created_at) to'g'ridan-to'g'ri
-- ishlamaydi, shuning uchun yangi partitioned jadval va ma'lumot ko'chirish kerak.
-- Shuning uchun bu qaror "kelajakda qimmat" ro'yxatida turadi.
```

Ba'zi kelajak qarorlari uchun hozir to'liq yechim kerak emas, lekin yo'lni yopmaslik kerak. Arxitektorning ishi shu ikki holatni ajratish.

## 1.8 Arxitektura qarori qanday eskiradi va uni qachon qayta ko'rish kerak

Har bir qaror o'z farazlari ustida turadi. Faraz o'zgarganda qaror eskiradi, qaror yomon bo'lganidan emas. Shu sababli ADR da "bu qaror qaysi farazga tayanadi" degan qism eng qimmatlisi.

Eskirish sabablari: yuk hajmi, jamoa tarkibi, platforma imkoniyati yoki biznes modeli o'zgardi. Misol: Java 21 da virtual thread lar barqarorlashgandan keyin "blocking I/O uchun reactive ga o'tish" qarorining asosi zaiflashdi. Oldingi qaror noto'g'ri emas edi, uning farazi eskirdi.

Qayta ko'rishni tasodifga qoldirmaslik kerak. Har bir muhim qarorga trigger qo'yiladi: metrika chegarasi yoki sana. Chegara buzilsa, qaror qayta ko'riladi.

```yaml
# ADR ga ilova qilinadigan "qayta ko'rish sharti" fayli.
# Bu hujjat emas, kuzatuv uchun mashina o'qiydigan ro'yxat.
decision: ADR-014-single-postgres-for-orders
assumptions:
  - daily_orders_max: 80000          # bir yilga qilingan taxmin
  - write_tps_peak: 10               # pik yozuv tezligi
  - orders_table_rows_max: 30000000  # partitioning chegarasi
review_triggers:
  - metric: orders_table_rows
    threshold: 25000000
    action: "partitioning rejasini ADR sifatida ochish"
  - metric: db_write_tps_p99
    threshold: 25
    action: "yozuv yo'lini qayta o'lchash, batch imkoniyatini ko'rish"
  - metric: replica_lag_seconds_p99
    threshold: 2
    action: "o'qish marshrutlashni qayta ko'rish"
  - date: 2027-01-15
    action: "farazlarni real raqamlar bilan solishtirish"
owner: orders-team
status: accepted
```

Chegaralar kuzatuvga ulanmasa, bu fayl o'lik hujjat. Har bir trigger uchun dashboard paneli yoki alert bo'lishi kerak. Kuzatuv tomoni dizayn [patternlar hujjatidagi](../patterns/README.md) observability bo'limida ko'rilgan.

## 1.9 Kod yozmaydigan arxitektor nega haqiqatdan uzoqlashadi

Diagrammada har bir strelka bir xil ko'rinadi. Kodda esa bitta strelka ikki qator, ikkinchisi ikki haftalik ish bo'ladi. Kod yozmaydigan arxitektor shu farqni ko'rmaydi, shuning uchun smetasi muntazam xato bo'ladi.

Ikkinchi sabab: ramkalarning haqiqiy xatti-harakati hujjatdan farq qiladi. `@Transactional` bitta sinf ichidagi chaqiruvda ishlamasligi, lazy collection ni tranzaksiyadan tashqarida o'qish `LazyInitializationException` berishi, `@Async` metodining self-invocation da proxy dan o'tmasligi hammasi shunday detallar. Bu detallar arxitektura qarorini o'zgartiradi, chunki ular jamoaning kunlik tezligiga ta'sir qiladi.

Uchinchi sabab: ishonch. Jamoa o'zi bilan bir kodga tegadigan odamning qaroriga boshqacha qaraydi.

```java
// Arxitektor uchun "kichik detal" emas, qaror darajasidagi tuzoq.
@Service
public class OrderService {

    // Shu metod ichidagi self-invocation proxy dan o'tmaydi,
    // shuning uchun ikkinchi metodning tranzaksiyasi YARATILMAYDI.
    public void importBatch(List<OrderRequest> requests) {
        for (OrderRequest r : requests) {
            saveOne(r);          // @Transactional e'tiborsiz qoladi
        }
    }

    @Transactional
    public void saveOne(OrderRequest r) {
        // ...
    }
}
```

Bu kod sintaktik to'g'ri va mantiqan buzuq. Amaliy chegara shunday: haftada bir necha soat real kod, odatda eng xavfli yo'lning prototipi yoki murakkab PR ni chuqur ko'rib chiqish. Feature yetkazish emas, mexanikaga tegib turish.

## 1.10 O'z fikrlashini tekshirish uchun savollar ro'yxati

Quyidagi savollarning maqsadi javob topish emas, yashirin farazni ochish. Agar savolga raqam bilan javob bera olmasang, qaror hali tayyor emas.

Birinchi guruh, kontekst haqida. Bu qaror qaysi biznes maqsadiga xizmat qiladi. Kim bu tizimni bir yildan keyin qo'llab-quvvatlaydi. Jamoada bu texnologiyani ishlab ko'rgan odam bormi. Muddat qisqarsa, qaysi qism birinchi tashlab yuboriladi.

Ikkinchi guruh, narx haqida. Bu qaror nimani yaxshilaydi va nimani yomonlashtiradi. Yomonlashgan narsani qanday o'lchayman. Agar bu qaror xato bo'lsa, qaytarish qancha turadi va necha hafta oladi. Bu qaror operatsion yukni qancha oshiradi.

Uchinchi guruh, haqiqat haqida. Bu raqamni o'lchadimmi yoki taxmin qildimmi. Eng yomon holatda nima bo'ladi va tizim qanday degradatsiya qiladi. Agar yuk o'n baravar oshsa, birinchi nima sinadi. Bu qarorning farazi qachon eskiradi va kim buni sezadi.

To'rtinchi guruh, soddalik haqida. Bu komponentni olib tashlasam, nima buziladi. Shu natijani ikki baravar kam harakat bilan olish mumkinmi. Yangi odam bu yechimni bir kunda tushunadimi. Bu abstraksiyaning uchta real ishlatilish holati bormi yoki bittasi bormi.

## 1.11 Amalda qo'llash

- [ ] Hozirgi loyihangizning uchta eng muhim arxitektura qarorini bir sahifali ADR qilib yozing, har birida kontekst, alternativa va narx bo'lsin.
- [ ] Eng muhim uchta foydalanuvchi yo'li uchun p99 latency maqsadini raqamda belgilang va `management.metrics.distribution.slo` orqali o'lchovga ulang.
- [ ] `pg_stat_statements` dan eng qimmat o'nta so'rovni oling va har biri uchun `EXPLAIN (ANALYZE, BUFFERS)` rejasini tekshiring.
- [ ] HikariCP pool kattaligini taxmin bilan emas, yuk sinovi natijasi bilan asoslang va `connection-timeout` ni 2 sekundgacha tushiring.
- [ ] Loyihadagi qarorlarni "arzon qaytariladigan" va "qimmat qaytariladigan" ikki ro'yxatga ajratib, ikkinchisiga ko'proq tekshiruv vaqti ajratganingizni tasdiqlang.
- [ ] Har bir muhim ADR ga review trigger qo'shing: metrika chegarasi yoki sana, va unga alert yoki dashboard paneli bog'lang.
- [ ] Faqat bitta implementatsiyasi bo'lgan interfeyslarni toping va haqiqiy almashuv nuqtasi bo'lmaganlarini olib tashlang.
- [ ] Haftada ikki soatni real kodga ajratib, eng xavfli yo'lning prototipini yoki eng murakkab PR ni o'zingiz ko'rib chiqing.

---

[Mundarija](README.md) · [2. Muammoni tushunish va to'g'ri savol berish &rarr;](02-muammoni-tushunish-va-togri-savol-berish.md)
