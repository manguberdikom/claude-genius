<!-- doc: architect | chapter: 1 | part: I. Fikrlash va qarorlar -->

[Barcha hujjatlar](../../README.md) / [Arxitektor miyasi](README.md)

> Holat: tekshirilmoqda. Da'volar hali manbaga solishtirilmoqda.

# 1. Arxitektorning fikrlash modeli (The Architect's Mental Model)

<details>
<summary>Bu bobdagi 16 bo'lim</summary>

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
- [1.11 Qarorning ta'sir radiusi va uni kichraytirish](#111-qarorning-tasir-radiusi-va-uni-kichraytirish)
- [1.12 Loyiha kattaligining o'lchangan ta'siri: nuqson zichligi, unumdorlik va faoliyat ulushlari](#112-loyiha-kattaligining-olchangan-tasiri-nuqson-zichligi-unumdorlik-va-faoliyat-ulushlari)
- [1.13 Korporativ ilovaning belgilari: davomli ma'lumot, konkurent kirish va konseptual dissonans](#113-korporativ-ilovaning-belgilari-davomli-malumot-konkurent-kirish-va-konseptual-dissonans)
- [1.14 Eisenhower matritsasi: shoshilinch va muhimni ajratish](#114-eisenhower-matritsasi-shoshilinch-va-muhimni-ajratish)
- [1.15 Dizayn jarayonining shakli: wicked muammo, akkretsiya va dizayn darajalari](#115-dizayn-jarayonining-shakli-wicked-muammo-akkretsiya-va-dizayn-darajalari)
- [1.16 Amalda qo'llash](#116-amalda-qollash)

</details>



Arxitektorning ishi diagramma chizish emas. Richards va Ford arxitektorcha fikrlashni to'rt qismga ajratadi: arxitektura va dizayn farqini bilish, texnik chuqurlik bilan birga keng texnik bilim saqlash, yechimlar orasidagi trade-off ni tahlil qilish, biznes drayverlarini arxitektura xususiyatlariga tarjima qilish (*Fundamentals of Software Architecture*, 2-bob). Shu to'rtlik bu bobning skeleti: kontekst, trade-off, sifat atributlari, qarorning qaytarilish darajasi va qarorning eskirishi.

## 1.1 Arxitektor va senior developer o'rtasidagi haqiqiy farq

Senior developer berilgan masalani eng yaxshi tarzda yechadi. Arxitektor masalaning o'zi to'g'ri qo'yilganini tekshiradi. Birinchi farqning eng aniq ifodasi *Fundamentals of Software Architecture* ning 2-bobidagi bilim piramidasida. Piramida butun bilimni uchga bo'ladi: bilganingiz, bilmasligingizni bilganingiz va bilmasligingizni ham bilmaganingiz. Developerning qiymati yuqori qismni, ya'ni chuqurlikni o'stirishda; arxitektor uchun esa kenglik chuqurlikdan muhimroq, chunki u imkoniyatlarni texnik cheklovlarga moslashtiradi. Kitob buni ochiq aytadi: bitta yechimni mukammal bilishdan ko'ra, bitta muammo uchun beshta yechim borligini bilish qimmatroq. Shu kitob xuddi shu joyda arxitektorning kodga tegib turishi kerakligini ham talab qiladi, ya'ni kenglik chuqurlikni butunlay almashtirmaydi.

Ikkinchi farq o'sha kitobning ikkinchi qonunida: "nega" "qanday" dan muhimroq. Mualliflar seminarlarda faqat talabalar chizgan topologiyani saqlab qolganini, ya'ni qanday yechganini yozib, nega shunday tanlaganini yo'qotganini aytadi. Begona tizimga qarab uning qanday ishlashini aniqlash mumkin, nega shunday tanlanganini esa aniqlab bo'lmaydi. To'lov servisida senior idempotentlik kalitini `UNIQUE` indeks bilan amalga oshiradi. Arxitektor esa idempotentlik oynasi qancha vaqt saqlanishini, eski kalitlarni kim tozalashini va bu jadval bir yilda qancha o'sishini hisoblaydi va sababini yozib qoldiradi.

Uchinchi farq kutilayotgan vazifalarda. *Fundamentals* ning 1-bobi arxitektor rolini ta'riflash o'rniga undan kutiladigan sakkiz vazifani sanaydi: arxitektura qarorlarini qabul qilish (texnologiyani ko'rsatish emas, tanlovni yo'naltirish); arxitekturani muntazam tahlil qilish; so'nggi tendensiyalardan xabardor bo'lish; qarorlarga rioya qilinishini ta'minlash; turli texnologiya, platforma va muhitlar bilan tajriba to'plash; biznes domenini bilish; odamlar bilan ishlash qobiliyatiga ega bo'lish; tashkilot siyosatini tushunish va unda yo'l topish. Ro'yxatning yarmi texnik emas: kitob yetakchilik va muzokara qobiliyatini samarali arxitektor uchun kamida yarim ish deb baholaydi.

Arxitektura nima degan savolga bitta ta'rif yo'q. *Documenting Software Architectures* SEI to'plamida 150 dan ortiq ta'rif borligini aytadi va eng ta'sirlilarini yonma-yon keltiradi. "Arxitektura tizimni tashkil qilish haqidagi muhim qarorlar to'plami" shaklidagi mashhur ta'rif Booch, Rumbaugh va Jacobson ga tegishli (1999). Bass, Clements va Kazman ta'rifi boshqacha: arxitektura tizimning tuzilmasi yoki tuzilmalari, ularni tashkil etuvchi dasturiy elementlar, bu elementlarning tashqaridan ko'rinadigan xossalari va ular orasidagi munosabatlar. "Arxitektura muhim narsalar haqida, u nima bo'lsa ham" degan gap esa Ralph Johnson ga tegishli, Martin Fowler ga emas: Fowler uni "Who Needs an Architect?" maqolasida keltirgan va o'zi ta'rif berishdan bosh tortgan.

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

Bir xil talab ikki kompaniyada ikki xil arxitekturaga olib keladi. *Fundamentals of Software Architecture* ning 2-bobi arxitektura savollariga mashhur "bu sharoitga bog'liq" javobini aynan shu bilan izohlaydi va qaysi sharoit ekanini sanaydi: deploy muhiti, biznes drayverlari, kompaniya madaniyati, byudjet, muddat, developerlarning mahorati va boshqa o'nlab omil. Shu sababli kontekst yozilmasa, qaror asoslanmaydi: biznes maqsadi, jamoa kattaligi va tajribasi, muddat, byudjet.

Biznes maqsadi qaysi sifat atributi birinchi o'rinda turishini aytadi. To'lov servisida ma'lumot to'g'riligi latency dan ustun. Omborda qoldiq ko'rsatadigan katalog sahifasida esa latency to'g'rilikdan ustun, chunki bir soniya kechikish konversiyani yo'qotadi. Shu bitta jumla keyingi o'nta qarorni belgilaydi.

Jamoa kattaligi operatsion yukning chegarasini belgilaydi. Besh kishilik jamoa uchun o'n ikki microservice va Kafka klasteri xarajat, qobiliyat emas. Har bir mustaqil deploy qilinadigan servis o'z deploy, kuzatuv va navbatchilik yukini qo'shadi; shu yukni ko'taradigan odam yo'q bo'lsa, qaror noto'g'ri. Qo'shimcha yukning o'z loyihangizdagi miqdori o'lchanadi, taxmin qilinmaydi.

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

Bu yondashuvning chegarasi bor va u o'z yukingizda o'lchanadi, kitobdan yoki blogdan ko'chirilmaydi. Qaror yozuvida aynan shu o'lchangan chegara ko'rsatiladi: shu raqamdan oshsa broker masalasi ochiladi.

## 1.3 Trade-off tili: bepul qaror yo'q, har birining narxi bor

Richards va Ford buni "dasturiy arxitekturaning birinchi qonuni" deb nomlaydi: dasturiy arxitekturada hamma narsa trade-off (*Fundamentals of Software Architecture*, 1-bob). Qonunning natijasi ham bor: agar arxitektor trade-off emas deb o'ylagan narsani topsa, u trade-off ni hali ko'rmagan. O'sha kitobning 2-bobida Rich Hickey ning gapi keltiriladi: programmerlar hamma narsaning foydasini biladi va hech narsaning narxini bilmaydi, arxitektor esa ikkisini ham bilishi kerak. Neal Ford ning formulasi esa qisqa: arxitekturada to'g'ri yoki noto'g'ri javob yo'q, faqat trade-off bor.

Amaliy ko'rinishi: cache latency ni pasaytiradi va ma'lumot yangiligini yo'qotadi. Replika o'qish yukini bo'ladi va replication lag keltiradi. Async ishlov berish javobni tezlashtiradi va xatoni ko'rinmas qiladi. Shu sababli arxitektor "yaxshiroq" degan so'z o'rniga "nima hisobidan" deb so'raydi.

*Software Architecture: The Hard Parts* trade-off tahlilini uch qadamga ajratadi (2-bob, 26-27-betlar): qaysi qismlar bir-biriga chalkashganini topish, ular qanday coupling bilan bog'langanini tahlil qilish, keyin o'zgarishning bog'liq tizimlarga ta'sirini baholab trade-off ni chiqarish. Shu kitob coupling ning eng sodda ta'rifini beradi: ikki qism bitta o'zgarish ikkinchisida ham o'zgarish talab qilsa, bog'langan hisoblanadi.

Amaliy shakli bor: har bir qaror uchun bitta jumla yozish. "X ni oldik, chunki Y ni yaxshilaydi, buning narxi Z, va Z ni W bilan kuzatamiz." Bu jumla yozilmasa, qaror muhokama emas, didga aylanadi.

Misol: buyurtma servisida read replika qo'shish. Foyda: master dagi o'qish yuki kamayadi; qancha kamayishi o'qish va yozish nisbatiga bog'liq va o'lchanadi. Narx: foydalanuvchi buyurtma yaratgandan keyin uni ro'yxatda darhol ko'rmasligi mumkin. Lag qiymati konfiguratsiya va yukka bog'liq, uni oldindan aytib bo'lmaydi, kuzatuvdan olinadi. Yechim: yozuvdan keyingi o'qish master ga yo'naltiriladi.

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

Sifat atributi o'lchanmasa, u talab emas, istak. Richards va Ford bu muammoni uchga ajratadi: atributlarning ta'rifi noaniq, bitta tashkilot ichida ham turli bo'lim bir atamani boshqacha tushunadi, va ko'p atribut aslida bir nechta kichikroq atributdan yasalgan. Yechim bitta: tashkilot bo'ylab obyektiv, o'lchanadigan ta'rif kelishib olinadi (*Fundamentals of Software Architecture*, 6-bob). "Tizim tez bo'lsin" degan gap shu sababli qaror chiqarmaydi. "Buyurtma yaratish p99 kechikishi 300 millisekunddan oshmasin, kunlik pik yukda, 95 foiz kunlarda" degan gap qaror chiqaradi. Shu sababli arxitektor har bir atributga ssenariy, raqam va o'lchash nuqtasini beradi.

Latency ni o'rtacha qiymat bilan o'lchash eng keng tarqalgan xato va buni ikki kitob bir xil aytadi. Kleppmann javob vaqtini bitta raqam emas, taqsimot deb ko'rishni talab qiladi: o'rtacha qiymat "tipik" javob vaqtini bermaydi, chunki u bu kechikishni qancha foydalanuvchi sezganini aytmaydi; shu sababli p95, p99 va p999 ishlatiladi va ular tail latency deb nomlanadi (*Designing Data-Intensive Applications*, 1-bob, 13-15-betlar). Richards va Ford buni boshqa tomondan ko'rsatadi: jamoa faqat o'rtachani o'lchasa va chegaraviy holat so'rovlarning bir foizini o'n barobar sekinlashtirsa, trafik katta bo'lganda bu chetga chiqishlar grafikda umuman ko'rinmaydi, shuning uchun maksimal javob vaqtini ham o'lchash kerak (*Fundamentals of Software Architecture*, 6-bob).

Kleppmann yana ikki amaliy qoidani beradi. Birinchisi: yuqori persentillarda javob vaqtining katta qismi navbatda kutishdan keladi, bir nechta sekin so'rov keyingi so'rovlarni ushlab turadi (head-of-line blocking), shuning uchun javob vaqtini mijoz tomonda ham o'lchash kerak. Ikkinchisi: persentillarni o'rtachalash, masalan bir nechta mashinaning p99 ini qo'shib ikkiga bo'lish, matematik jihatdan ma'nosiz; to'g'ri yo'l histogram larni qo'shish. Shu sababli quyidagi sozlamada `percentiles-histogram` yoqiladi.

Throughput va latency bir-biriga bog'liq. Pool to'lganda navbat paydo bo'ladi va latency keskin o'sadi. Hisob oddiy va uni o'zingiz tekshirib ko'rishingiz mumkin: bir so'rov bazani 50 millisekund egallasa, bitta ulanish sekundda 20 so'rovga yetadi, 20 ta ulanish bilan nazariy maksimum 400 so'rov/sekund. Bu nazariy chegara, real qiymat undan past.

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

Availability ni foizda emas, yo'qotilgan daqiqada o'ylash foydali. Simon Brown shu hisobni to'g'ridan-to'g'ri qiladi: 99.9 foiz ("uchta to'qqiz") kunda bir daqiqadan sal ko'proq to'xtash oynasini beradi, ya'ni oyda taxminan 43 daqiqa (*Software Architecture for Developers*, 55-bet). 99.99 foiz esa oyda taxminan 4 daqiqa. Ikkinchisining narxi birinchisidan sezilarli yuqori, chunki u avtomatik failover, ko'p zona va mashq qilingan runbook talab qiladi; aniq nisbat muhitga bog'liq va u smetada hisoblanadi, kitobdan olinmaydi. Brown ning kuzatuvi shu: homiyga qancha availability kerakligini so'rasangiz, javob "100 foiz" bo'ladi, shuning uchun savolni "qancha to'xtashga toqat qilasiz" shaklida berish kerak (59-bet).

Maintainability eng qiyin holat. Simon Brown uni miqdorlashtirish qiyin deb hisoblaydi va uning o'rniga maintainable kod yozishga olib boradigan tamoyillar haqida o'ylashni taklif qiladi (*Software Architecture for Developers*, 58-bet). Richards va Ford esa chiqish yo'lini ko'rsatadi: bunday murakkab atributni kichikroq va o'lchanadigan tashkil etuvchilarga yoyish kerak, masalan agility ni modularity, deployability va testability ga (*Fundamentals of Software Architecture*, 6-bob).

ESLATMA: pastdagi uchta aniq o'lchov shu korpusning amaliy tavsiyasi, kitobdan olingan emas: o'zgarishdan prod gacha o'tgan vaqt, bitta oddiy o'zgarish uchun tegiladigan modul soni, yangi odamning birinchi PR gacha ketgan kuni.

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

Bu saralashning kitobdagi asosi risk formulasi. Fairbanks risk ni ikki noaniq qiymatning ko'paytmasi deb ta'riflaydi: nosozlikning taxmin qilingan ehtimoli va taxmin qilingan ta'siri (*Just Enough Software Architecture*, 3.3-bo'lim). Richards va Ford xuddi shu ikki o'lchovni jadvalga qo'yadi: ta'sir va ehtimol har biri past (1), o'rta (2) yoki yuqori (3) deb baholanadi, ko'paytma 1 dan 2 gacha past, 3 dan 4 gacha o'rta, 6 dan 9 gacha yuqori risk beradi; kitob avval ta'sirni, keyin ehtimolni baholashni tavsiya qiladi (*Fundamentals of Software Architecture*, 20-bob). Qaytarilishi qimmat qaror aynan ta'sir o'qi bo'yicha yuqori turadi, shuning uchun unga ko'proq tekshiruv vaqti ajratiladi.

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

"Yetarlicha" degan so'z Simon Brown dan keladi: oldindan qancha dizayn kerak degan savolga uning javobi "yetarlicha", ya'ni tuzilma va yo'nalish paydo bo'ladigan darajada, boshqa hech narsa emas (*Software Architecture for Developers*, 185-187-betlar). Brown shu yerda "yetarlicha" ni miqdorlashtirish qiyinligini tan oladi va uning o'rniga "juda kam" va "juda ko'p" belgilarini sanaydi. Juda kam belgilaridan bir qismi: tizim chegarasi qayerda ekani aniq emas, jamoada umumiy manzara yo'q, nofunksional talablar haqida o'ylanmagan, risk zonalari haqida o'ylanmagan, prototip qilinmagani uchun dizayn ishlashiga ishonch yo'q. YAGNI ("you aren't going to need it") shu kitobda arxitekturani butunlay rad etish uchun ishlatiladigan shior qatorida keltiriladi, ya'ni atamaning o'zi xato emas, undan "umid bilan kutish" uchun foydalanish xato.

Over-engineering mahoratning ortiqchasi emas, noto'g'ri yo'naltirilgan qo'rquv natijasi. Arxitektor noaniqlikni abstraksiya bilan yopishga urinadi va shu bilan noaniqlikni ko'paytiradi. Richards va Ford buning arxitektura darajasidagi ko'rinishini anti-pattern deb ataydi: barcha sifat atributini qo'llab-quvvatlaydigan universal arxitektura qurishga urinish, chunki har bir qo'shimcha atribut dizaynni murakkablashtiradi va bu murakkablik hali asosiy domen muammosiga qo'l tegmasdan to'planadi. Ularning tavsiyasi domen manfaatdorlariga eng muhim uchta atributni (tartibsiz) tanlatish (*Fundamentals of Software Architecture*, 5-bob). O'sha bobdagi Vasa misoli chegarasini ko'rsatadi: 17-asrda qurilgan shved kemasi bir vaqtda qo'shin tashuvchi ham, harbiy kema ham bo'lishi, ikki palubasi va ikki barobar katta to'plari bo'lishi kerak edi; kema portdan chiqib, salom to'pini otganda tepa qismi og'irligidan qulab cho'kdi.

Qancha arxitektura kerakligini aniqlashning kitobdagi javobi Fairbanks ning risk asosidagi modeli: uch qadam, ya'ni risklarni aniqlash va ustuvorlashtirish, ularni kamaytiradigan usullar to'plamini tanlab qo'llash, keyin risk kamayganini baholash; harakat risk hajmiga mos bo'lishi kerak (*Just Enough Software Architecture*, 3.1-bo'lim). Fairbanks shu bobda "developer vaqtining o'n foizi arxitekturaga ketsin" shaklidagi qat'iy o'lchagichlarni ham, "har bir tizim uchun to'liq hujjat to'plami tuzilsin" qoidasini ham mos kelmaydigan yo'l-yo'riq deb sanaydi: har bir loyiha boshqa risk bilan ishlaydi, shu sababli bir xil diagramma to'plami har joyda to'g'ri bo'lishi kutilmaydi.

Shu modelning bu bobdagi amaliy mezoni: keyin qo'shishning narxi hozir qo'shish narxidan qancha yuqori. Agar farq kichik bo'lsa, kutish kerak. Agar farq katta bo'lsa, hozir qilish kerak. Buyurtma jadvaliga `created_at` ustunini keyin qo'shish arzon. Monolit ichida tranzaksiya chegarasini keyin ajratish qimmat.

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

Kelajakni inkor qilish ham xato. Kleppmann chegarani ochiq aytadi: bitta yuk darajasiga mos arxitektura o'n barobar katta yukni ko'tarishi ehtimoldan uzoq, shuning uchun tez o'sayotgan servisda yuk har bir o'n barobar oshganda arxitekturani qayta ko'rish kerak bo'ladi (*Designing Data-Intensive Applications*, 1-bob, 17-bet). Demak tekshirish nuqtasi o'n baravarga qo'yiladi, oraliqdagi o'sish esa qarorni o'zgartirmaydi.

Taxminni raqam bilan yozish kerak, va o'rtacha emas, pik bilan. "Buyurtmalar o'sadi" emas, balki "kunlik buyurtma hozir 20 ming, bir yildan keyin 80 ming". Bundan o'rtacha tezlik chiqadi: 80000 ni sutkadagi 86400 sekundga bo'lsak, sekundda bitta yozuvdan kamroq. Pik soat o'rtachadan uch barobar zich bo'lsa, sekundda taxminan uch yozuv. Shu raqam bitta PostgreSQL instansi yetarli ekanini ko'rsatadi. O'n baravar oshsa, partitioning masalasi ochiladi.

Pikni o'rtachadan ajratish talabda yozilmaydi, u domen bilimidan keladi. Richards va Ford shu nuqtani universitet misolida ko'rsatadi: ming talaba va o'n soatlik ro'yxatga olish oynasi berilgan bo'lsa, arxitektor talabalar vaqt bo'ylab teng tarqaladi deb o'ylashi mumkin, lekin talabalar odatini bilgan odam ming talabaning oxirgi o'n daqiqada kelishini hisobga oladi. Bunday tafsilot talablar hujjatida kamdan-kam uchraydi, ammo dizayn qarorini belgilaydi (*Fundamentals of Software Architecture*, 5-bob).

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

Kelajak taxminining bir qismi esa umuman taxmin qilinmaydi, chunki u tebranib turadi. Martin buni cheksiz mayatnik deb ataydi: hisoblash quvvati qayerda turishi masalasi markazlashuv va tarqalish orasida to'xtovsiz tebranadi. Veb dan oldin klient-server arxitekturasi, undan oldin soqov terminallar bilan markaziy minikompyuterlar, undan oldin aqlli terminalli mainframe lar, undan oldin esa mashina xonalari va perfokartalar turgan edi; veb butun IT tarixi ko'lamida hech narsani o'zgartirmagan, u shu kurashdagi tebranishlardan faqat bittasi, va tebranish davom etadi (Martin, *Clean Architecture*, Prentice Hall, 2018, 31-bob). Arxitektorning vazifasi tebranishni bashorat qilish emas: bu qisqa muddatli masalalar biznes qoidalarining markaziy yadrosidan uzoqqa surib qo'yiladi (31-bob).

Shundan amaliy xulosa: "qaysi tomon yengadi" savoliga javob yozishning hojati yo'q, javob kerak bo'lmaydigan tuzilma qurilsa yetarli. Biznes qoidasi veb, desktop yoki mobil klientni bilmasa, mayatnik keyingi marta qaysi tomonga tebransa ham qaytarilish narxi past qoladi; [qaytarilish narxi](#15-qaytarib-boladigan-va-qaytarib-bolmaydigan-qarorlar) hisobida bu tebranadigan qarorlarni arzon tomonga olib o'tadi.

## 1.8 Arxitektura qarori qanday eskiradi va uni qachon qayta ko'rish kerak

Har bir qaror o'z farazlari ustida turadi. Faraz o'zgarganda qaror eskiradi, qaror yomon bo'lganidan emas. Shu sababli ADR da "bu qaror qaysi farazga tayanadi" degan qism eng qimmatlisi.

Qarorni qayta ko'rish arxitektorning kutilayotgan vazifalaridan biri. *Fundamentals of Software Architecture* ning 1-bobi buni arxitekturaning hayotiyligi (architecture vitality) deb ataydi: uch yoki undan ko'p yil oldin aniqlangan arxitektura biznes va texnologiyadagi o'zgarishlar fonida bugun ham yaroqlimi degan savol. Kitob bu vazifaga yetarli e'tibor berilmasligini kuzatadi va natijasini strukturaviy yemirilish (structural decay) deb nomlaydi: developerlar kod yoki dizaynni o'zgartirganda talab qilingan sifat atributlariga, masalan performance, availability va scalability ga ta'sir qiladi. Shu bobda bir ko'rinmas tomoni ham aytiladi: kodni o'zgartirish tez bo'lsa-yu, o'zgarishni test qilish haftalar, reliz oylar olsa, arxitektura darajasida chaqqonlikka erishilmaydi.

Eskirish sabablari: yuk hajmi, jamoa tarkibi, platforma imkoniyati yoki biznes modeli o'zgardi. Platforma o'zgarishiga misol: Java 21 da virtual thread lar standart imkoniyatga aylangandan keyin "blocking I/O uchun reactive ga o'tish" qarorining asosi zaiflashdi. Oldingi qaror noto'g'ri emas edi, uning farazi eskirdi.

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

Bu bo'limning asosi ikki kitobda bir xil. Robert Martin buni to'g'ridan-to'g'ri aytadi: arxitektor programmerdir va programmer bo'lib qolaveradi; arxitektorlar yuqori darajadagi masalalarga o'tib kodni tashlab ketadi degan gapga ishonmaslik kerak; ular boshqalarga qaraganda kamroq kod yozishi mumkin, lekin programmer vazifalarini bajarishdan to'xtamaydi, chunki boshqa programmerlar uchun o'zlari yaratgan muammolarni sezmasa, ishini to'g'ri bajara olmaydi (*Clean Architecture*, 15-bob). Richards va Ford ham "har bir arxitektor kod yozishi va ma'lum darajada texnik chuqurlikni saqlashi kerak" deb yozadi (*Fundamentals of Software Architecture*, 2-bob).

Sabab oddiy: diagrammada har bir strelka bir xil ko'rinadi. Kodda esa bitta strelka ikki qator, ikkinchisi ikki haftalik ish bo'ladi. Kod yozmaydigan arxitektor shu farqni ko'rmaydi, shuning uchun smetasi muntazam xato bo'ladi.

Ikkinchi sabab: ramkalarning haqiqiy xatti-harakati hujjatdan farq qiladi. `@Transactional` bitta sinf ichidagi chaqiruvda ishlamasligi, lazy collection ni tranzaksiyadan tashqarida o'qish `LazyInitializationException` berishi, `@Async` metodining self-invocation da proxy dan o'tmasligi hammasi shunday detallar. Bu detallar arxitektura qarorini o'zgartiradi, chunki ular jamoaning kunlik tezligiga ta'sir qiladi.

Uchinchi sabab: ishonch. Jamoa o'zi bilan bir kodga tegadigan odamning qaroriga boshqacha qaraydi.

Richards va Ford shu yerda qarshi tomondagi tuzoqni ham ko'rsatadi: arxitektor loyihaning kritik yo'lidagi kodni, odatda asosiy framework kodini o'z egaligiga olsa, jamoa uchun to'siqqa (bottleneck trap) aylanadi, chunki u to'liq vaqtli developer emas. Kitobning yechimi: kritik yo'l va framework kodini jamoaga topshirib, o'zi bir-uch iteratsiya oldinda turgan biznes funksiyasini yozish, ya'ni developerlar bilan bir xil kodni yozish. Agar jamoa bilan birga kod yozish imkoni bo'lmasa, kitob texnik chuqurlikni saqlashning to'rt yo'lini sanaydi: proof-of-concept qilish (va uni ishlab chiqarish sifatida yozish, chunki tashlab yuborilishi kerak bo'lgan kod repozitoriyda qolib, namuna bo'lib ketadi); texnik qarz va arxitektura hikoyalarini olish; iteratsiya ichidagi bug fix larni o'ziga olish; jamoa uchun avtomatlashtirish yozish, masalan arxitektura qoidalarini tekshiradigan fitness function yoki ArchUnit testlari (*Fundamentals of Software Architecture*, 2-bob).

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

Bu kod sintaktik to'g'ri va mantiqan buzuq. Maqsad feature yetkazish emas, mexanikaga tegib turish: eng xavfli yo'lning prototipi, texnik qarz hikoyasi, bug fix yoki jamoa uchun avtomatlashtirish. Qancha vaqt ajratish kerakligini kitoblar raqam bilan bermaydi, shuning uchun bu yerda ham raqam berilmaydi; chegarani jamoaning kritik yo'li belgilaydi, ya'ni arxitektor to'siqqa aylanmaydigan daraja.

## 1.10 O'z fikrlashini tekshirish uchun savollar ro'yxati

Fairbanks risk asosidagi modelni to'xtovsiz savol berish jarayoni deb ta'riflaydi: risklarim nima, ularni kamaytiradigan eng yaxshi usul qaysi, risk kamaydimi va kod yozishga qaytsam bo'ladimi (*Just Enough Software Architecture*, 3.1-bo'lim). U yana risk asosida ishlamayotganlikning aniq belgisini beradi: har qanday developer "qaysi feature ustida ishlayapsan" savoliga javob beradi, lekin ko'pchilik "asosiy nosozlik risklarim nima va ularga qanday usul qo'llayapman" savolida qiynaladi.

ESLATMA: pastdagi to'rt guruh savol shu korpusning amaliy checklisti, kitobdan olingan emas. Maqsadi javob topish emas, yashirin farazni ochish. Agar savolga raqam bilan javob bera olmasang, qaror hali tayyor emas.

Birinchi guruh, kontekst haqida. Bu qaror qaysi biznes maqsadiga xizmat qiladi. Kim bu tizimni bir yildan keyin qo'llab-quvvatlaydi. Jamoada bu texnologiyani ishlab ko'rgan odam bormi. Muddat qisqarsa, qaysi qism birinchi tashlab yuboriladi.

Ikkinchi guruh, narx haqida. Bu qaror nimani yaxshilaydi va nimani yomonlashtiradi. Yomonlashgan narsani qanday o'lchayman. Agar bu qaror xato bo'lsa, qaytarish qancha turadi va necha hafta oladi. Bu qaror operatsion yukni qancha oshiradi.

Uchinchi guruh, haqiqat haqida. Bu raqamni o'lchadimmi yoki taxmin qildimmi. Eng yomon holatda nima bo'ladi va tizim qanday degradatsiya qiladi. Agar yuk o'n baravar oshsa, birinchi nima sinadi. Bu qarorning farazi qachon eskiradi va kim buni sezadi.

To'rtinchi guruh, soddalik haqida. Bu komponentni olib tashlasam, nima buziladi. Shu natijani ikki baravar kam harakat bilan olish mumkinmi. Yangi odam bu yechimni bir kunda tushunadimi. Bu abstraksiyaning uchta real ishlatilish holati bormi yoki bittasi bormi.

## 1.11 Qarorning ta'sir radiusi va uni kichraytirish

Qarorni baholashda qaytarilish narxidan tashqari ikkinchi o'lcham bor: qaror nechta jamoaga va nechta mijozga tegadi. Orosz buni qarorning ta'sir radiusi (blast radius) deb ataydi. Faqat o'z jamoangiz ishlatadigan tizimni tozalash uchun qilingan refaktoring kichik radiusli qaror, chunki unga boshqa jamoa ham, mijoz ham bog'liq emas. Kompaniya ichidagi yigirma jamoa ishlatadigan API endpoint ni yopish esa o'sha yigirma jamoaga va ularga bog'liq mijozlarga tegadi, endpoint ochiq bo'lsa radius yana kengayadi (Gergely Orosz, *The Software Engineer's Guidebook*, 1-nashr, Pragmatic Engineer, 2023, 25-bob, 366-bet).

Katta radiusli qarorning qiyinligi texnik emas. Orosz ikki sababni ajratadi: o'zgarish tufayli ish qilishi kerak bo'lgan jamoalar taklif qilingan muddatga qarshi chiqadi, va mijoz tomonda ishlayotgan funksiya buzilsa, buzuvchi o'zgarish mijozni yo'qotish bilan tugaydi (366-bet). Qaytarib bo'lmaydigan qarorni orqaga qaytarish odatda aynan shu toifaga tushadi, shuning uchun [qaytarilish narxi](#15-qaytarib-boladigan-va-qaytarib-bolmaydigan-qarorlar) bilan ta'sir radiusi birga baholanadi.

Alohida e'tibor beriladigan sinf bor: dastlab arzon qaytariladigan ko'ringan, lekin mijoz kutgani uchun qimmatlashib qolgan qarorlar (365-bet).

| Qaror | Nega dastlab arzon ko'rinadi | Nega keyin qimmatlashadi |
|---|---|---|
| Protokol tanlovi (REST, GraphQL, gRPC) | Ichkarida transport almashtirish mexanik ish | Hamma mijoz migratsiya qilishi yoki eski protokolni ushlab turuvchi adapter yozilishi kerak |
| Versiyalash strategiyasi | Raqam qo'yish shartnoma emasdek tuyuladi | Mijoz bitta strategiyaga ko'nikadi, o'zgartirish ishonchni buzadi |
| Funksiyani barqaror ochiq API qilib e'lon qilish | Bitta endpoint ochish kichik ish | Barqaror deb e'lon qilingach, o'zgarish yangi endpoint yoki yangi major versiya talab qiladi |
| Mijozga ko'rinadigan yangi servis chiqarish | Servisni to'xtatish mumkindek ko'rinadi | Chiqarilgan servis zarar keltirsa ham uzoq muddat qo'llab-quvvatlanadi |

Radiusni kichraytirish yo'llari qaror mazmunidan emas, uning yetkazilish shaklidan chiqadi. Orosz ikki misol beradi: endpoint ni tashqarida tirik qoldirib, ichkarida yangisiga ko'chirish va orasiga tarjima qiluvchi adapter qo'yish, yoki mijozni yangi endpoint ga qo'shimcha imkoniyat bilan rag'batlantirib ko'chirish, shunda radius o'z-o'zidan qisqaradi (366-bet). Java tomonda bu ko'pincha eski kontrakt uchun `@Deprecated` controller ni saqlab, uni yangi servis chaqiruviga o'girishga aylanadi.

Kichik radius har doim to'g'ri tanlov degani emas. Orosz ogohlantiradi: kontekst va cheklovlarni hisobga olganda radiusi kichikroq variant noto'g'ri bo'lishi mumkin, shuning uchun barcha variant sanaladi va trade-off bilan taqqoslanadi; radiusni kamaytiradigan yechim ko'pincha qolipdan tashqari fikrlash natijasi bo'ladi (367-bet). Uzoq muddatli mezon esa shunday: yaxshi arxitektura qarori kelajakda tuzatish uchun qilinadigan qarorlarning radiusini cheklaydi (367-bet).

## 1.12 Loyiha kattaligining o'lchangan ta'siri: nuqson zichligi, unumdorlik va faoliyat ulushlari

Bu bobdagi qoidalarning aksari "qancha" savoliga tayanadi, va javob loyiha kattaligi bilan chiziqli emas. McConnell *Code Complete* ning 27-bobida uchta o'lchangan tendensiyani beradi: nuqson zichligi, bir odamga unumdorlik va faoliyat ulushlari. Arxitektor uchun bu uchlik raqamli asos, chunki u "bu loyihada qancha oldindan dizayn kerak" savolini didan hisobga ko'chiradi.

Birinchi tendensiya: nuqson zichligi kattalik bilan birga o'sadi. Ikki barobar katta mahsulotda xato ikki barobardan ko'proq bo'ladi, chunki ming satrga to'g'ri keladigan nuqson soni ham oshadi.

| Loyiha kattaligi (kod satri) | Tipik nuqson zichligi |
|---|---|
| 2K dan kichik | ming satrga 0 - 25 nuqson |
| 2K - 16K | ming satrga 0 - 40 |
| 16K - 64K | ming satrga 0.5 - 50 |
| 64K - 512K | ming satrga 2 - 70 |
| 512K va undan katta | ming satrga 4 - 100 |

Juda katta loyihada ming satrga to'g'ri keladigan xato soni kichik loyihadagidan to'rt barobarga chiqishi mumkin, ya'ni bir xil xato darajasiga yetish uchun katta loyiha ko'proq ishlashi kerak (McConnell, *Code Complete*, 2-nashr, Microsoft Press, 2004, 27.3 (652-653-betlar)). Xatoning turi ham siljiydi: kichik loyihada topilgan xatolarning taxminan 75 foizi konstruksiya xatosi, kattasida bu ulush 50 foizga tushadi va farqni talab va arxitektura xatolari egallaydi; ba'zi juda katta loyihalarda esa konstruksiya ulushi yana 75 foizda qoladi (27.3 (652-bet)).

Ikkinchi tendensiya: bir odamga unumdorlik tushadi.

| Loyiha kattaligi (kod satri) | Bir odam-yiliga kod satri (qavsda Cocomo II nominal) |
|---|---|
| 1K | 2 500 - 25 000 (4 000) |
| 10K | 2 000 - 25 000 (3 200) |
| 100K | 1 000 - 20 000 (2 600) |
| 1 000K | 700 - 10 000 (2 000) |
| 10 000K | 300 - 5 000 (1 600) |

Kitob raqamlarning tarqoqligini ochiq aytadi va ularni sanoat kesimidagi o'rtacha deb beradi, lekin tendensiya ahamiyatli: kichik loyihadagi unumdorlik kattasidan 2 - 3 barobar yuqori bo'lishi mumkin, eng kichik va eng katta loyiha orasidagi farq esa 5 - 10 barobarga yetadi (27.4 (653-bet)).

Uchinchi tendensiya: faoliyat ulushlari. Kichik loyihada konstruksiya butun ishlab chiqish vaqtining 65 foizigacha oladi, o'rta loyihada taxminan 50 foiz, juda katta loyihada esa arxitektura, integratsiya va tizim testi oldinga chiqadi (27.5 (654-bet)). Sababi oddiy: konstruksiya (batafsil dizayn, kodlash, debug, unit test) kattalik bilan deyarli chiziqli o'sadi, qolgan ishlar chiziqsiz o'sadi. Chiziqsiz o'sadigan ishlar ro'yxati kitobda aniq sanalgan: muloqot, rejalashtirish, boshqaruv, talablarni ishlab chiqish, tizim funksional dizayni, interfeys dizayni va spetsifikatsiyasi, arxitektura, integratsiya, nuqsonni yo'qotish, tizim testi va hujjat ishlab chiqarish (27.5 (655-bet)). Shu nomutanosiblik bitta misolda ko'rinadi: mahsulot o'n barobar kattalashsa, konstruksiya ishi 25 barobar, rejalashtirish 25 - 50 barobar, integratsiya 30 barobar, arxitektura va tizim testi 40 barobar oshadi (27.5 (655-bet)).

Shu yerdan arxitektor uchun eng amaliy raqam chiqadi. Boehm va Turner o'lchoviga ko'ra 10 000 satr atrofidagi loyihada arxitektura va talablarga umumiy xarajatning taxminan 5 foizini ajratish eng arzon natija bergan, 100 000 satr atrofidagi loyihada esa eng yaxshi natija 15 - 20 foiz ajratilganda chiqqan (27.5 (655-bet)). Ya'ni [yetarlicha yaxshi arxitektura](#16-yetarlicha-yaxshi-arxitektura-over-engineering-va-yagni-chegarasi) chegarasi kattalikka bog'liq: bitta servisda over-engineering bo'lgan tayyorgarlik hajmi o'n barobar katta tizimda yetarli bo'lmaydi.

```bash
# Avval o'zingizni jadvalga joylashtiring: loyiha necha ming satr kod.
# Bo'sh qator va izoh qatorlari sanoqdan chiqariladi.
find src/main/java -name '*.java' -print0 \
  | xargs -0 grep -vcE '^[[:space:]]*(//|\*|/\*|$)' \
  | awk -F: '{n += $2} END {printf "%.1f KLOC\n", n / 1000}'
```

McConnell jadvallar aniq loyihalardan olinganini va sizning raqamlaringizga o'xshamasligi mumkinligini o'zi ogohlantiradi (27.3 (653-bet)). Shuning uchun ulardan foydalanishning to'g'ri usuli bitta: o'z kattaligingizni o'lchab, shu oraliqning qayerida turganingizni ko'rish va tayyorgarlik ulushini shunga qarab belgilash.

## 1.13 Korporativ ilovaning belgilari: davomli ma'lumot, konkurent kirish va konseptual dissonans

"Yaxshi arxitektura" degan gap mavhum, chunki har sinf tizimning o'z qiyinligi bor. Fowler korporativ ilovani (enterprise application) alohida sinf deb ajratadi va uni misol bilan chegaralaydi: ish haqi, bemor yozuvlari, yuk kuzatuvi, xarajat tahlili, kredit skoring, sug'urta, ta'minot zanjiri, buxgalteriya, mijozga xizmat va valyuta savdosi korporativ ilova; avtomobil yonilg'i inyeksiyasi, matn muharriri, lift kontrolleri, telefon kommutatori, operatsion tizim, kompilyator va o'yin emas (Fowler, *Patterns of Enterprise Application Architecture*, Addison-Wesley, 2003, Kirish, 2-3-betlar).

Farq qiyinlikning joyida. Fowler o'z tajribasini taqqoslaydi: telekom dasturiga nisbatan korporativ ilovada og'ir ko'p threadli masalalar ham, apparat bilan integratsiya ham yo'q, lekin ma'lumot murakkab va ko'p, biznes qoidalari esa mantiq sinovlarining hammasidan yiqiladi (2-bet). Belgilar ro'yxati shunday:

- **Davomli ma'lumot.** Ma'lumot programmaning bir necha ishga tushishi orasida saqlanishi kerak, odatda yillar davomida. U o'zini yaratgan apparatdan, operatsion tizimdan va kompilyatordan uzoq yashaydi; shu vaqt ichida eski qismlarni buzmasdan yangi ma'lumot saqlash uchun strukturasi ko'p marta o'zgaradi, tizim butunlay almashtirilganda esa ma'lumot yangi ilovaga ko'chiriladi (3-bet).
- **Ma'lumot ko'p.** O'rtacha tizimda 1 GB dan ortiq ma'lumot va o'n millionlab yozuv bo'ladi, shuning uchun ma'lumotni boshqarish tizimning asosiy qismiga aylanadi (3-bet).
- **Konkurent kirish.** Ko'pincha ko'p odam bir vaqtda ma'lumotga tegadi. Odam soni yuzdan kam bo'lsa ham, ikki odam bir xil ma'lumotga bir vaqtda tegib xatoga olib kelmasligini ta'minlash masalasi qoladi; tranzaksiya menejeri yukning bir qismini oladi, lekin ko'pincha uni ilova dasturchisidan butunlay yashirib bo'lmaydi (3-bet).
- **Ko'p ekran va batch.** Yuzlab alohida ekran bo'lishi g'ayrioddiy emas, foydalanuvchilar esa texnik emas va ehtiyoji har xil. Foydalanuvchi bilan muloqotga qaralganda tizimlardagi batch ishlov berish ulushi oson esdan chiqadi (3-bet).
- **Integratsiya va konseptual dissonans.** Korporativ ilova yolg'iz yashamaydi: boshqa vaqtda, boshqa texnologiyada qurilgan tizimlar bilan birlashadi. Texnologiya birxillashtirilganda ham biznes jarayoni farqi va ma'lumotdagi konseptual dissonans qoladi: bir bo'lim "mijoz" deb hozirda shartnomasi bor odamni, boshqasi shartnomasi bo'lgan lekin endi yo'q odamni ham, uchinchisi mahsulot savdosini sanab xizmat savdosini sanamaydi. Har maydoni nozik farq qiladigan yuzlab yozuv bo'lganda muammoning hajmi o'zi qiyinchilikka aylanadi (3-4-betlar).
- **Biznes "mantiqsizligi".** Fowler "business logic" atamasini g'alati deb ataydi: biznes qoidasi sizga berilgan narsa, uni siyosiy kuch ishlatmasdan o'zgartirib bo'lmaydi va u kutilmagan tarzda bir-biri bilan ta'sirlashadigan tasodifiy shartlar to'plamidan iborat. Shu sababli yagona ishonchli taxmin: mantiq vaqt bilan o'zgaradi (4-bet).

```java
// Konseptual dissonans: "mijoz" har bo'limda boshqa narsani bildiradi.
// Bitta umumiy Customer sinfi o'rniga har kontekst o'z tipini e'lon qiladi,
// shunda bir bo'limdagi ta'rif o'zgarishi boshqasini buzmaydi.
record BillingCustomer(long id, Instant contractFrom, Instant contractTo) {
    boolean activeAt(Instant moment) {
        return !moment.isBefore(contractFrom)
                && (contractTo == null || moment.isBefore(contractTo));
    }
}

// Support uchun shartnoma tugaganlar ham mijoz bo'lib qoladi.
record SupportCustomer(long id, boolean everHadContract) { }
```

Oxirgi nuqta hajm haqidagi taxminni o'zgartiradi: Fowler korporativ ilova albatta katta degan tasavvurni rad etadi, kichik loyihalar ham korxonaga katta qiymat berishini va ularning kumulyativ ta'siri sezilarli bo'lishini aytadi; eng yaxshi ishlardan biri esa arxitektura va jarayonni soddalashtirib katta loyihani kichigiga aylantirish (4-bet). Hajm va o'sish taxminining o'zi [hajm va o'sish taxmini](02-muammoni-tushunish-va-togri-savol-berish.md#26-hajm-va-osish-taxmini) bo'limida, kontekst chegarasi esa [chegaralangan kontekst](../patterns/13-domain-driven-design-patternlari.md#132-chegaralangan-kontekst-bounded-context) yozuvida turadi.

## 1.14 Eisenhower matritsasi: shoshilinch va muhimni ajratish

Arxitektura ishini himoya qilish uchun bitta ramka yetadi. Martin Eisenhower ga tegishli muhimlik va shoshilinchlik matritsasidan boshlaydi: "menda ikki xil muammo bor, shoshilinch va muhim. Shoshilinchlari muhim emas, muhimlari hech qachon shoshilinch emas" (Martin, *Clean Architecture*, Prentice Hall, 2018, 2-bob). Dasturning birinchi qiymati, ya'ni xatti-harakat, shoshilinch, lekin har doim muhim emas; ikkinchi qiymati, ya'ni arxitektura, muhim, lekin hech qachon shoshilinch emas.

To'rt juftlik ustuvorlik tartibiga tiziladi:

| Tartib | Kvadrant | Nima tushadi |
|---|---|---|
| 1 | shoshilinch va muhim | ishlab turgan funksiyani tiklash, ma'lumot yo'qotish xavfi |
| 2 | shoshilinch emas, lekin muhim | arxitektura ishi: chegara, chok, migratsiya yo'li |
| 3 | shoshilinch, lekin muhim emas | talab qilinayotgan, lekin tizim qiymatini oshirmaydigan funksiya |
| 4 | shoshilinch emas va muhim emas | hech kim so'ramagan yaxshilanish |

Tartibdagi muhim kuzatish: arxitektura birinchi ikki o'rinda turadi, xatti-harakat esa birinchi va uchinchi o'rinni egallaydi (2-bob).

Kitobdagi asosiy xato ham shu tartibda. Biznes menejerlari va developerlar uchinchi kvadrantdagi narsalarni birinchisiga ko'taradi, ya'ni shoshilinch lekin muhim bo'lmagan funksiyalarni haqiqatan shoshilinch va muhim funksiyalardan ajratmaydi. Natijada tizimning muhim arxitekturasi muhim bo'lmagan funksiyalar foydasiga e'tibordan chiqadi (2-bob). Developer uchun dilemma esa shunda: biznes menejeri arxitekturaning muhimligini baholashga jihozlanmagan, buni qilish uchun ishlab chiqish jamoasi yollangan, demak funksiyalarning shoshilinchligi oldida arxitekturaning muhimligini qat'iy aytish shu jamoaning javobgarligi (2-bob).

```text
Backlog triage, kvadrant bo'yicha:
1  shoshilinch + muhim      INC-214 to'lov timeout i          -> hozir
2  muhim, shoshilinch emas  to'lov modulidagi chokni ajratish  -> rejada, egasi bor
3  shoshilinch, muhim emas  hisobot ekraniga yangi filtr       -> navbatga, 1 ga ko'tarilmaydi
4  ikkisi ham emas          admin panel rangi                  -> rad etiladi
```

Amaliy natijasi ikkita. Birinchi: har bir "shoshilinch" so'rovga ikkinchi savol beriladi, ya'ni bu muhim ham bo'ladimi, va javob yozib qo'yiladi; aks holda uchinchi kvadrant jimgina birinchisiga ko'chadi. Ikkinchi: arxitektura ishi hech qachon o'zidan shoshilinch bo'lmagani uchun uning o'rni rejada aniq ajratiladi, kuzatuvda esa [trade-off tili](#13-trade-off-tili-bepul-qaror-yoq-har-birining-narxi-bor) bilan asoslanadi. Biznes bilan shu suhbatning to'liq shakli, o'lchov va dalillari [refaktoringni biznes bilan kelishish](34-legacy-kod-va-bosqichma-bosqich-refaktoring.md#349-refaktoringni-biznes-bilan-kelishish-qiymat-tilida-tushuntirish) bo'limida.

## 1.15 Dizayn jarayonining shakli: wicked muammo, akkretsiya va dizayn darajalari

Dizayn qarorini qanday qabul qilish kerakligi haqidagi bir oila qoida McConnell da nomlangan holda turadi. Ularning hammasi bitta xulosaga olib boradi: dizayn determinatsiyalangan jarayon emas, evristik jarayon, shuning uchun bitta to'g'ri yo'l emas, bir nechta tekshirilgan yo'l ishlatiladi.

- **Dizayn wicked muammo.** Rittel va Webber "wicked" muammoni faqat uni yechib yoki qismini yechib aniq ta'riflash mumkin bo'lgan muammo deb ta'riflagan. Paradoks amalda shuni bildiradi: muammoni aniq ta'riflash uchun uni bir marta yechish kerak, keyin ishlaydigan yechim olish uchun yana yechish kerak. Kitobdagi misol Tacoma Narrows ko'prigi: ko'prik qulagunicha injenerlar aerodinamikani shu darajada hisobga olish kerakligini bilmagan, ya'ni muammoning to'liq ta'rifi uning yechimidan keyin paydo bo'lgan (McConnell, *Code Complete*, 2-nashr, Microsoft Press, 2004, 5.1 (74-75-betlar)).
- **Akkretsiya: avval skelet, keyin go'sht.** Inkremental o'sishning aniq shakli bor. Avval tizimning ishga tushadigan eng sodda versiyasi qilinadi: u real kirishni qabul qilishi, real ishlov berishi yoki real chiqish berishi shart emas, u faqat haqiqiy tizimni ushlab turishga yetarli skelet bo'lishi kerak va har bir asosiy funksiya uchun bo'sh sinfni chaqirishi mumkin. Keyin har bir bo'sh sinf haqiqiysi bilan almashtiriladi, bo'sh kirish o'rniga haqiqiy kirishni o'qiydigan kod qo'yiladi va shu tariqa tizim to'liq ishlaydigan holga keladi. McConnell dalil sifatida Brooks ni keltiradi: 1975 yilda "bittasini tashlab yuborish uchun qur" degan muallif *The Mythical Man-Month* dan keyingi o'n yilda uning amaliyotini inkremental ishlab chiqishdan ko'proq o'zgartirgan narsa bo'lmaganini aytgan (2.3 (15-16-betlar)).
- **Dizayn besh darajada bo'ladi.** Darajalar: butun tizim; tizimni quyi tizimlarga va paketlarga bo'lish; paket ichida sinflarga bo'lish; sinf ichida ma'lumot va metodlarga bo'lish; metodning ichki dizayni. Ba'zi usullar hamma darajada ishlaydi, ba'zilari faqat bir yoki ikkitasida (5.2 (82-bet)). Bu arxitektorga aniq tekshiruv beradi: hozir qaysi darajada qaror qilayotganingizni aytolmasangiz, muhokama ikki darajani aralashtirib yuborgan.
- **Yuqoridan va pastdan.** Yuqoridan pastga dizayn dekompozitsiya strategiyasi, pastdan yuqoriga esa kompozitsiya strategiyasi; kitob ularni raqib emas, bir-birini to'ldiruvchi deb ataydi. Yuqoridan boshlash oson, chunki odam katta narsani bo'laklashga yaxshi, va u konstruksiya tafsilotini keyinga qoldirishga ruxsat beradi; pastdan boshlash esa kerakli yordamchi funksionallikni erta ko'rsatadi va zich, yaxshi ajratilgan dizayn beradi. Pastdan boshlashning kuchsiz joyi uni yolg'iz ishlatib bo'lmasligi: g'ishtdan samolyot qurilmaydi. Dekompozitsiya qachon to'xtaydi degan savolga kitob amaliy javob beradi: keyingi darajani bo'lishdan ko'ra uni kodlash osonroq ko'rinsa, to'xtaysiz (5.4 (111-113-betlar)).
- **Bitta to'g'ri joy.** Plauger ning "One Right Place" printsipi: har bir jiddiy kod bo'lagini qidirish uchun bitta to'g'ri joy va ehtimoliy o'zgarishni kiritish uchun bitta to'g'ri joy bo'lishi kerak. Nazoratni sinfda, metodda yoki hatto nomlangan konstantada markazlashtirish mumkin; foydasi murakkablikda: qaraydigan joy kam bo'lsa, o'zgartirish oson va xavfsiz bo'ladi (5.3 (107-bet)).
- **Brute force ni hisobdan chiqarmaslik.** Ishlaydigan qo'pol yechim ishlamaydigan nafis yechimdan yaxshiroq, va nafis yechimni ishlaydigan holga keltirish uzoq vaqt olishi mumkin. Kitobdagi dalil Knuth dan: binary search ning birinchi tavsifi 1946 yilda chiqqan, har qanday uzunlikdagi ro'yxatni to'g'ri qidiradigan algoritm esa yana 16 yildan keyin nashr etilgan (5.3 (107-bet)).

Quyidagi misol kitobdagi g'oyani Java ga o'tkazadi, kitobda bu til uchun kod yo'q: bitta to'g'ri joy qoidasi komissiya hisobini uch chaqiruvchidan ajratib bitta sinfga yig'adi.

```java
// Bitta to'g'ri joy: komissiya qoidasi shu sinfda yashaydi.
// Controller, batch job va hisobot uni takrorlamaydi, shu yerdan so'raydi.
@Component
public class FeePolicy {

    private static final BigDecimal RATE = new BigDecimal("0.015");
    private static final BigDecimal MIN_FEE = new BigDecimal("1000");

    public BigDecimal feeFor(BigDecimal amount) {
        BigDecimal fee = amount.multiply(RATE);
        return fee.compareTo(MIN_FEE) < 0 ? MIN_FEE : fee;
    }
}
```

## 1.16 Amalda qo'llash

- [ ] Hozirgi loyihangizning uchta eng muhim arxitektura qarorini bir sahifali ADR qilib yozing, har birida kontekst, alternativa va narx bo'lsin.
- [ ] Eng muhim uchta foydalanuvchi yo'li uchun p99 latency maqsadini raqamda belgilang va `management.metrics.distribution.slo` orqali o'lchovga ulang.
- [ ] `pg_stat_statements` dan eng qimmat o'nta so'rovni oling va har biri uchun `EXPLAIN (ANALYZE, BUFFERS)` rejasini tekshiring.
- [ ] HikariCP pool kattaligini taxmin bilan emas, yuk sinovi natijasi bilan asoslang va `connection-timeout` ni 2 sekundgacha tushiring.
- [ ] Loyihadagi qarorlarni "arzon qaytariladigan" va "qimmat qaytariladigan" ikki ro'yxatga ajratib, ikkinchisiga ko'proq tekshiruv vaqti ajratganingizni tasdiqlang.
- [ ] Har bir muhim ADR ga review trigger qo'shing: metrika chegarasi yoki sana, va unga alert yoki dashboard paneli bog'lang.
- [ ] Faqat bitta implementatsiyasi bo'lgan interfeyslarni toping va haqiqiy almashuv nuqtasi bo'lmaganlarini olib tashlang.
- [ ] Texnik chuqurlikni saqlashning to'rt yo'lidan birini tanlab jadvalga qo'ying (proof-of-concept, texnik qarz hikoyasi, bug fix yoki jamoa uchun avtomatlashtirish) va kritik yo'ldagi kodni o'z egaligingizga olmaganingizni tekshiring.

## Manbalar

- Mark Richards, Neal Ford, *Fundamentals of Software Architecture*, O'Reilly, 2020, 1-bob - arxitektordan kutiladigan sakkiz vazifa, arxitekturaning hayotiyligi va strukturaviy yemirilish, birinchi va ikkinchi qonun ("hamma narsa trade-off", "nega qandaydan muhimroq"), Ralph Johnson ning ta'rifi Fowler ning "Who Needs an Architect?" maqolasi orqali
- Mark Richards, Neal Ford, *Fundamentals of Software Architecture*, O'Reilly, 2020, 2-bob - arxitektorcha fikrlashning to'rt qismi, bilim piramidasi va kenglik/chuqurlik, Rich Hickey ning trade-off haqidagi gapi, "bu sharoitga bog'liq" javobini belgilovchi omillar, bottleneck trap va kodga tegib turishning to'rt yo'li
- Mark Richards, Neal Ford, *Fundamentals of Software Architecture*, O'Reilly, 2020, 5-bob - sifat atributlarini domen manfaatdorlaridan chiqarish, ro'yxatni qisqa tutish va eng muhim uchtani tanlash, Vasa misoli, universitetga ro'yxatga olishdagi pik yuk misoli
- Mark Richards, Neal Ford, *Fundamentals of Software Architecture*, O'Reilly, 2020, 6-bob - atribut ta'riflarining uch muammosi, obyektiv ta'rif, o'rtacha qiymat chetga chiqishlarni yashirishi, murakkab atributni tashkil etuvchilarga yoyish
- Mark Richards, Neal Ford, *Fundamentals of Software Architecture*, O'Reilly, 2020, 20-bob - risk jadvali: ta'sir va ehtimol ko'paytmasi, 1-2 past, 3-4 o'rta, 6-9 yuqori
- Neal Ford, Mark Richards, Pramod Sadalage, Zhamak Dehghani, *Software Architecture: The Hard Parts*, 1-nashr, O'Reilly, 2021 (copyright 2022), 1-2-bob (13-14, 26-27-betlar) - "best practice" bo'lmagan sinf masalalar, trade-off tahlilining uch qadami, coupling ning sodda ta'rifi
- George Fairbanks, *Just Enough Software Architecture: A Risk-Driven Approach*, Marshall & Brainerd, 2010, 3.1 va 3.3-bo'limlar - risk asosidagi modelning uch qadami, harakat risk hajmiga mos bo'lishi, risk = taxmin qilingan ehtimol x taxmin qilingan ta'sir, qat'iy foiz o'lchagichlarining yaroqsizligi
- Simon Brown, *Software Architecture for Developers*, Leanpub, 2014 - 55 va 58-betlar (availability ni "to'qqizlar" va to'xtash oynasida o'lchash, maintainability ni miqdorlashtirish qiyinligi), 59-bet ("qancha availability kerak" savolini "qancha to'xtashga toqat qilasiz" ga aylantirish), 185-187-betlar ("yetarlicha" oldindan dizayn, juda kam va juda ko'p belgilari, YAGNI shiorining o'rni)
- Robert C. Martin, *Clean Architecture*, Pearson, 2018, 15-bob - arxitektor programmer bo'lib qolaveradi va kod yozishdan to'xtamaydi; arxitekturaning maqsadi variantlarni iloji boricha uzoq ochiq qoldirish
- Robert C. Martin, *Clean Architecture*, Pearson, 2018, 1-2-bob - muallif dizayn va arxitektura o'rtasida farq yo'q deb da'vo qiladi (*Fundamentals* ning 2-bobidagi qarashga qarshi), dasturning ikki qiymati xatti-harakat va tuzilish
- Martin Kleppmann, *Designing Data-Intensive Applications*, O'Reilly, 2017, 1-bob (13-17-betlar) - javob vaqti taqsimot sifatida, o'rtachaning yaroqsizligi, p95/p99/p999 va tail latency, navbat va head-of-line blocking, persentillarni o'rtachalashning ma'nosizligi, yuk har o'n barobar oshganda arxitekturani qayta ko'rish
- Paul Clements va boshqalar, *Documenting Software Architectures: Views and Beyond*, 2-nashr, Addison-Wesley, 2011, Prolog, P.1-bo'lim (3-5-betlar, "Coming to Terms: What Is Software Architecture?") - arxitektura ta'riflari to'plami: "muhim qarorlar to'plami" Booch, Rumbaugh va Jacobson ga (1999, 4-bet), tuzilmalar orqali ta'rif Bass, Clements va Kazman ga (2003, 5-bet) tegishli
- Gergely Orosz, *The Software Engineer's Guidebook*, 1-nashr, Pragmatic Engineer BV, 2023, 25-bob, 365-367-betlar - qarorning ta'sir radiusi (blast radius), katta radiusning ikki narxi (jamoalarning qarshiligi va mijozni yo'qotish), radiusni kichraytirish yo'llari (adapter bilan eski endpoint ni tirik qoldirish, mijozni rag'batlantirib ko'chirish), ikki tomonlama eshik vaqt o'tib bir tomonlama eshikka aylanishi (protokol, versiyalash, barqaror ochiq API, mijozga ko'rinadigan yangi servis)
- Steve McConnell, *Code Complete*, 2-nashr, Microsoft Press, 2004, 27.3-27.5 (652-655-betlar) - 27-1-jadval: loyiha kattaligi va tipik nuqson zichligi (2K dan kichikda ming satrga 0-25 dan 512K dan kattada ming satrga 4-100 gacha), juda katta loyihada xato zichligining to'rt barobarga chiqishi; xato turining siljishi (kichikda 75 foiz konstruksiya, kattada 50 foiz); 27-2-jadval: bir odam-yiliga kod satri va Cocomo II nominal qiymatlari, kichik loyihada unumdorlikning 2-3 barobar yuqoriligi va chetlar orasida 5-10 barobar farq; 27-3-rasm: konstruksiya ulushi 65 foizdan 50 foizga tushishi; chiziqsiz o'sadigan ishlar ro'yxati; o'n barobar kattalashgan mahsulot uchun ko'paytuvchilar (konstruksiya 25, rejalashtirish 25-50, integratsiya 30, arxitektura va tizim testi 40); Boehm va Turner bo'yicha arxitektura va talablarga 10 000 satrda 5 foiz, 100 000 satrda 15-20 foiz
- Steve McConnell, *Code Complete*, 2-nashr, Microsoft Press, 2004, 2.3 (15-16-betlar) - akkretsiya metaforasi va inkremental ishlab chiqish: ishga tushadigan eng sodda skelet, bo'sh sinflar va ularning bosqichma-bosqich almashtirilishi; Brooks ning inkremental ishlab chiqish haqidagi keyingi bahosi
- Steve McConnell, *Code Complete*, 2-nashr, Microsoft Press, 2004, 5.1-5.4 (74-75, 82, 107, 111-113-betlar) - dizayn wicked muammo (Rittel va Webber ta'rifi, Tacoma Narrows misoli); dizaynning besh darajasi; Plauger ning "One Right Place" printsipi; brute force evristikasi va binary search ning 1946 va 16 yillik tarixi; yuqoridan pastga va pastdan yuqoriga strategiyalarning kuchli va kuchsiz tomonlari, dekompozitsiyani to'xtatish mezoni
- Martin Fowler, *Patterns of Enterprise Application Architecture*, Addison-Wesley, 2003, Kirish (2-4-betlar) - korporativ ilovaning chegarasi misollar bilan; davomli ma'lumot va uning apparat, OS va kompilyatordan uzoq yashashi; 1 GB dan ortiq ma'lumot va o'n millionlab yozuv; konkurent kirish va tranzaksiya menejerining chegarasi; yuzlab ekran va batch ulushi; integratsiya, konseptual dissonans va "mijoz" ta'rifining bo'limlar bo'yicha farqi; biznes mantiqining tasodifiyligi; korporativ ilovaning katta bo'lishi shart emasligi
- Robert C. Martin, *Clean Architecture*, Prentice Hall, 2018, 2-bob - Eisenhower ning muhimlik va shoshilinchlik matritsasi, to'rt kvadrantning ustuvorlik tartibi, arxitekturaning birinchi ikki o'rinda va xatti-harakatning birinchi va uchinchi o'rinda turishi, uchinchi kvadrantni birinchisiga ko'tarish xatosi, biznes menejerining arxitektura muhimligini baholashga jihozlanmaganligi
- Robert C. Martin, *Clean Architecture*, Prentice Hall, 2018, 31-bob - cheksiz mayatnik: hisoblash quvvatining markazlashuv va tarqalish orasida tebranishi, veb dan oldingi bosqichlar, tebranishni biznes qoidalari yadrosidan uzoqqa surish
- ESLATMA: 1.1, 1.2, 1.6 va 1.10 dagi jadval va savol ro'yxatlari, 1.4 dagi maintainability o'lchovlari va 1.8 dagi `review_triggers` fayli shu korpusning amaliy tavsiyasi, kitobdan olingan emas
- ESLATMA: 1.12 dagi KLOC sanash buyrug'i, 1.13 dagi `BillingCustomer` va `SupportCustomer` misoli, 1.14 dagi backlog triage ro'yxati va 1.15 dagi `FeePolicy` misoli shu korpusning amaliy qo'shimchasi: kitoblarda bu kod yo'q

---

[Mundarija](README.md) · [2. Muammoni tushunish va to'g'ri savol berish &rarr;](02-muammoni-tushunish-va-togri-savol-berish.md)
