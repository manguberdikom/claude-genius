<!-- doc: architect | chapter: 39 | part: VI. Amaliyot va o'sish -->

[Kod yozadigan arxitektorning miyyasi](../../README.md) / [Arxitektor miyyasi](README.md)

# 39. Birinchi 90 kun va o'z-o'zini baholash (First 90 Days and Self-Assessment)

<details>
<summary>Bu bobdagi 14 bo'lim</summary>

- [39.1 Yangi loyihada birinchi hafta: nimani o'qish, kimdan so'rash, nima yozmaslik](#391-yangi-loyihada-birinchi-hafta-nimani-oqish-kimdan-sorash-nima-yozmaslik)
- [39.2 Birinchi oy: tizim xaritasini chizish va og'riqli nuqtalarni ro'yxatlash](#392-birinchi-oy-tizim-xaritasini-chizish-va-ogriqli-nuqtalarni-royxatlash)
- [39.3 Ikkinchi oy: kichik, ko'rinadigan yaxshilanish bilan ishonch qozonish](#393-ikkinchi-oy-kichik-korinadigan-yaxshilanish-bilan-ishonch-qozonish)
- [39.4 Uchinchi oy: o'rta muddatli reja taklif qilish va kelishib olish](#394-uchinchi-oy-orta-muddatli-reja-taklif-qilish-va-kelishib-olish)
- [39.5 Mavjud qarorlarni hurmat qilish: "nega shunday qilingan" savolini birinchi berish](#395-mavjud-qarorlarni-hurmat-qilish-nega-shunday-qilingan-savolini-birinchi-berish)
- [39.6 O'z bilimingizdagi bo'shliqni topish uchun o'z-o'zini tekshirish ro'yxati](#396-oz-bilimingizdagi-boshliqni-topish-uchun-oz-ozini-tekshirish-royxati)
- [39.7 Yetuklik darajalari: qaysi mavzuda qay darajada turibsiz](#397-yetuklik-darajalari-qaysi-mavzuda-qay-darajada-turibsiz)
- [39.8 Fikrlash va qarorlar bilimini o'zingizga qo'llash](#398-fikrlash-va-qarorlar-bilimini-ozingizga-qollash)
- [39.9 Java va JVM: o'zingizni sinash savollari](#399-java-va-jvm-ozingizni-sinash-savollari)
- [39.10 Spring: o'zingizni sinash savollari](#3910-spring-ozingizni-sinash-savollari)
- [39.11 PostgreSQL: o'zingizni sinash savollari](#3911-postgresql-ozingizni-sinash-savollari)
- [39.12 Operatsion tayyorlik: o'zingizni sinash savollari](#3912-operatsion-tayyorlik-ozingizni-sinash-savollari)
- [39.13 Keyingi qadam: shu hujjatni va qolgan ikki hujjatni qanday ishlatish](#3913-keyingi-qadam-shu-hujjatni-va-qolgan-ikki-hujjatni-qanday-ishlatish)
- [39.14 Amalda qo'llash](#3914-amalda-qollash)

</details>



Arxitektor yangi tizimga kelganda eng katta xatosi tezda foydali bo'lishga urinishdir. Haqiqatda esa birinchi uch oyda sizning asosiy mahsulotingiz kod emas, balki ishonchli xarita va ishonchli munosabatdir. Bu bob shu uch oyni haftalab bo'lib beradi, keyin esa diqqatni sizning o'zingizga qaratadi: bilimingizdagi bo'shliqni qanday topish va qaysi mavzuda qay darajada turganingizni qanday o'lchash. Hujjat shu bob bilan tugaydi, shuning uchun oxirida uchlikni birgalikda qanday ishlatish ham aytiladi.

## 39.1 Yangi loyihada birinchi hafta: nimani o'qish, kimdan so'rash, nima yozmaslik

Birinchi haftada kod yozmaslik qoidasi mavhum maslahat emas, u aniq hisob. Siz hali tizimning tranzaksiya chegaralarini, idempotentlik shartlarini va deploy jarayonini bilmaysiz. Shu holatda yozilgan har bir patch texnik qarz ishlab chiqaradi, uni esa keyin siz o'zingiz tozalaysiz.

O'qish tartibi quyidagicha bo'lsin. Avval deploy pipeline va runbook, chunki ular tizim qanday yashayotganini ko'rsatadi. Keyin ma'lumotlar bazasi migratsiyalari tarixi, chunki Flyway yoki Liquibase papkasi tizim evolyutsiyasining eng rost yilnomasi. Undan keyin eng ko'p o'zgargan sinflar, keyin esa incident tarixi.

```bash
# Eng ko'p tegilgan fayllar: shu yerda biznes murakkabligi to'plangan
git log --since="12 months ago" --name-only --pretty=format: \
  | grep -E '\.java$' | sort | uniq -c | sort -rn | head -30

# Tranzaksiya chegaralari qayerda e'lon qilingan
grep -rn "@Transactional" --include=*.java src/main/java | wc -l
grep -rln "@Transactional" --include=*.java src/main/java | head -20

# Migratsiya tarixi: tizim qanday o'sgani shu yerda ko'rinadi
ls -1 src/main/resources/db/migration | tail -25

# Tashqi integratsiyalar: har bir URL bu sizning SLA qaramligingiz
grep -rnE "https?://" src/main/resources/application*.y*ml | head -20
```

So'rash kerak bo'lgan odamlar ro'yxati qisqa. Birinchisi tungi chaqiruvlarga javob beradigan dejur injener, chunki u tizimning haqiqiy zaif joyini biladi. Ikkinchisi eng ko'p commit qilgan developer, uchinchisi mahsulot egasi. Dejurdan bitta savol so'rang: oxirgi uch oyda sizni nima uyqudan uyg'otdi. Bu savol odatda arxitektura muammosining aniq manzilini beradi.

Yozmaslik kerak bo'lgan narsalar ham aniq. Katta refactoring, yangi framework taklifi, va "biz buni hammasini qayta yozamiz" degan gap. Bu uchtasi birinchi haftada ishonchni eng tez yo'qotadigan harakatlardir.

## 39.2 Birinchi oy: tizim xaritasini chizish va og'riqli nuqtalarni ro'yxatlash

Birinchi oyning natijasi ikkita artefakt bo'lishi kerak: tizim xaritasi va og'riqli nuqtalar ro'yxati. Xarita chiroyli diagramma emas, u javob beradigan hujjat. Har bir servis uchun uchta narsa yozilsin: qaysi ma'lumotning egasi, qaysi tashqi tizimga sinxron bog'langan, va u o'chsa nima ishlamay qoladi.

Og'riqli nuqtalarni taxmin bilan emas, o'lchov bilan toping. PostgreSQL tarafida `pg_stat_statements` sizga bir kunda haqiqatni ko'rsatadi.

```sql
-- Umumiy vaqtni eng ko'p yeyayotgan so'rovlar: optimizatsiya navbati shu
SELECT substring(query, 1, 80) AS so_rov,
       calls,
       round(total_exec_time)       AS jami_ms,
       round(mean_exec_time, 2)     AS o_rtacha_ms,
       rows / GREATEST(calls, 1)    AS qator_per_call
FROM pg_stat_statements
ORDER BY total_exec_time DESC
LIMIT 20;

-- Sequential scan ko'p bo'lgan jadvallar: index yetishmasligi belgisi
SELECT relname, seq_scan, seq_tup_read, idx_scan,
       n_live_tup, n_dead_tup
FROM pg_stat_user_tables
WHERE seq_scan > 1000
ORDER BY seq_tup_read DESC
LIMIT 15;

-- Ishlatilmayotgan indexlar: yozish tezligini bekorga yeydi
SELECT relname, indexrelname, idx_scan, pg_size_pretty(pg_relation_size(indexrelid))
FROM pg_stat_user_indexes
WHERE idx_scan < 50
ORDER BY pg_relation_size(indexrelid) DESC
LIMIT 15;
```

Ro'yxatni tartiblashda ikkita o'qdan foydalaning: biznesga ta'siri va tuzatish narxi. Yuqori ta'sir va past narx bo'lgan bandlar ikkinchi oyning ishi bo'ladi. Yuqori ta'sir va yuqori narx bo'lganlar uchinchi oydagi rejaga tushadi. Past ta'sirli bandlarni umuman yozib qo'ying, ularga tegmang.

Shu oyda yana bitta o'lchov oling: p99 latency va connection pool to'yinganligi. Ko'p tizimda muammo so'rov sekinligida emas, pool navbatida turadi. Agar HikariCP `pending` metrikasi nolga teng bo'lmasa, siz o'lchovni topdingiz.

## 39.3 Ikkinchi oy: kichik, ko'rinadigan yaxshilanish bilan ishonch qozonish

Ikkinchi oyda bitta qoida bor: natija o'lchanadigan va bir hafta ichida ko'rinadigan bo'lsin. Yaxshi nomzodlar ro'yxati qisqa. Yetishmayotgan timeout qo'yish, bitta og'ir hisobot so'roviga index qo'shish, HikariCP pool o'lchamini to'g'rilash, va metrikani chiqarish.

Timeout eng arzon va eng ta'sirli yaxshilanishdir. Ko'p tizimda to'lov provayderiga chaqiruv timeout'siz turadi, shuning uchun provayder sekinlashganda butun thread pool to'lib qoladi.

```properties
# To'lov provayderiga chiqadigan HTTP chaqiruvlar: cheksiz kutish taqiqlanadi
payment.client.connect-timeout=2s
payment.client.read-timeout=4s

# So'rov darajasidagi himoya: bitta so'rov butun poolni ushlab turmaydi
spring.datasource.hikari.maximum-pool-size=20
spring.datasource.hikari.connection-timeout=3000
spring.datasource.hikari.validation-timeout=1000
spring.datasource.hikari.leak-detection-threshold=20000

# PostgreSQL tarafidan kafolat: osilgan so'rov o'zi uziladi
spring.jpa.properties.jakarta.persistence.query.timeout=5000
spring.datasource.hikari.data-source-properties.options=-c statement_timeout=5000 -c idle_in_transaction_session_timeout=10000

# Metrika: pool navbati ko'rinmasa, muammo ham ko'rinmaydi
management.endpoints.web.exposure.include=health,metrics,prometheus
management.metrics.tags.application=order-service
```

Pool o'lchamini tanlashda hisobni ko'rsatib bering. Agar o'rtacha so'rov bazada 5 ms turadigan bo'lsa, 20 ta connection nazariy jihatdan sekundda taxminan 4000 ta so'rovga yetadi. Shuning uchun 100 ta connection so'rash deyarli har doim xato bo'ladi, u faqat PostgreSQL tarafidagi raqobatni oshiradi.

Ko'rinadigan yaxshilanishni e'lon qilish usuli ham muhim. Oldingi va keyingi raqamni bitta jadvalda bering: p99 480 ms dan 120 ms ga tushdi, pool `pending` o'rtacha 7 dan 0 ga tushdi. Raqam bilan aytilgan natija sizga keyingi oyda kattaroq o'zgarish uchun ruxsat ochadi.

## 39.4 Uchinchi oy: o'rta muddatli reja taklif qilish va kelishib olish

Uchinchi oyda siz endi taklif qilish huquqini qozondingiz. Reja uch oydan olti oyga mo'ljallangan bo'lsin, undan uzoqroq reja ishonchni emas, shubhani keltiradi. Rejada har bir bandning uchta ustuni bo'lsin: qanday o'lchovni yaxshilaydi, qancha ishchi hafta oladi, va qanday risk tug'diradi.

Rejani yozishda eng kuchli vosita alternativani ham ko'rsatishdir. Masalan ombor qoldig'i servisini ajratish taklifida ikkinchi variant sifatida bitta bazada schema ajratishni ham bering. Bu sizni "o'z g'oyasini himoya qiladigan odam" emas, "qarorni ochib beradigan odam" qilib ko'rsatadi.

Kelishib olishning amaliy shakli qisqa qaror hujjati. Bir sahifada kontekst, variantlar, tanlangan yo'l, va natijalar. Shu hujjatni jamoa bilan o'qib chiqing, keyin uni repozitoriyga qo'ying. Og'zaki kelishuv yo'qoladi, yozilgani qoladi.

| Masala | Oddiy yondashuv | Arxitektor yondashuvi |
|---|---|---|
| Birinchi hafta | Darhol task olib kod yozadi | Deploy, migratsiya va incident tarixini o'qiydi |
| Muammoni topish | "Kod eski" deb umumlashtiradi | `pg_stat_statements` va pool metrikasi bilan o'lchaydi |
| Birinchi taklif | Katta refactoring taklif qiladi | Timeout va index kabi arzon yutuqni beradi |
| Natijani e'lon qilish | "Tezlashdi" deb aytadi | p99 480 ms dan 120 ms ga tushdi deb ko'rsatadi |
| Mavjud qarorga munosabat | "Buni kim shunday qildi" deb so'raydi | "Qanday sharoitda shunday to'g'ri edi" deb so'raydi |
| Reja ufqi | Ikki yillik maqsadni chizadi | Uch oylik o'lchanadigan bandlarni beradi |
| Alternativa | Bitta yo'lni himoya qiladi | Ikki yo'lni va tanlash mezonini beradi |
| Kelishuv shakli | Majlisda og'zaki tasdiqlaydi | Bir sahifali qaror hujjatini repozitoriyga qo'yadi |
| O'z bilimi | "Bilaman" deb o'tadi | Savol ro'yxati bilan o'zini tekshiradi |
| Jamoaga ta'sir | Qaror markazida o'zi turadi | Jamoa qaror qabul qiladigan mezonni qoldiradi |

## 39.5 Mavjud qarorlarni hurmat qilish: "nega shunday qilingan" savolini birinchi berish

Har bir g'alati kod bir paytda to'g'ri javob bo'lgan. Hisobotda denormalizatsiya qilingan jadval bo'lsa, ehtimol o'sha paytda hisobot 40 sekund ishlagan va mijoz ketib qolgan. Native SQL yozilgan joy bo'lsa, ehtimol Hibernate generatsiya qilgan so'rov planner tomonidan noto'g'ri bajarilgan.

Shu sababli birinchi savol bitta bo'lsin: qanday cheklov ostida bu qaror oqilona edi. Bu savol sizga ko'rinmagan cheklovni beradi, muallifni esa himoyaga o'tishga majburlamaydi.

Amalda bu `git log` bilan ishlashni bildiradi. Commit xabari, bog'langan ticket, va o'sha davrdagi incident bir-biriga ulanadi.

```bash
# Shubhali fayl qanday paydo bo'lgan: qator bo'yicha tarix
git log -L 40,80:src/main/java/com/shop/report/SalesReportDao.java --oneline

# Shu qator qaysi commitda yozilgan va xabari nima edi
git blame -L 40,80 src/main/java/com/shop/report/SalesReportDao.java

# O'sha commit atrofida yana nima o'zgardi: kontekst shu yerda
git show --stat <commit-sha>

# Ticket raqamlarini yig'ish: qaror sababi ko'pincha ticketda
git log --since="2 years ago" --grep="report" --oneline | head -20
```

Agar sabab topilmasa, qarorni "noto'g'ri" deb emas, "sababi hujjatlashtirilmagan" deb belgilang. Keyin o'zgartirishdan oldin sababni qayta tiklang. Bu tartib sizni eng qimmat xatodan saqlaydi: ko'rinmas talabni buzishdan.

## 39.6 O'z bilimingizdagi bo'shliqni topish uchun o'z-o'zini tekshirish ro'yxati

Bilimdagi bo'shliqni topishning eng ishonchli usuli javobni emas, tushuntirishni talab qilishdir. Agar siz mexanikani oq doskada ikki daqiqada chizib bera olmasangiz, siz bu mavzuni bilmaysiz, faqat tanib olasiz.

Tekshirishni haftada bir marta, bitta mavzuda o'tkazing. Har savol uchun uchta javob variantidan birini belgilang: chizib tushuntiraman, taniyman lekin tushuntirmayman, bilmayman. Ikkinchi variant eng xavfli, chunki u o'zini bilim deb ko'rsatadi.

| Tuzoq | Yechim |
|---|---|
| Hammasini bir vaqtda o'rganishga urinish | Haftada bitta mavzu, ikki daqiqalik tushuntirish mashqi |
| Javobni eslab qolishni bilim deb hisoblash | Oq doskada mexanikani chizishni talab qilish |
| Faqat kuchli mavzuni takrorlash | Zaif ustunni jadvaldan tanlab, shunga vaqt berish |
| Nazariyani amaliyotsiz o'qish | Har mavzuni real loyihadagi bitta muammoga ulash |
| Darajani o'zi baholab oshirib qo'yish | Jamoadagi bitta odamga tushuntirib, savolini eshitish |
| Bo'shliqni yozib qo'ymaslik | Ro'yxatni repozitoriyda saqlash va oyda bir qayta ko'rish |

## 39.7 Yetuklik darajalari: qaysi mavzuda qay darajada turibsiz

Daraja o'zini maqtash uchun emas, vaqtni to'g'ri taqsimlash uchun kerak. Pastki jadvalda har bir mavzu uchun uchta daraja bor. O'zingizni rost joylashtiring, keyin eng past ustunlardan ikkitasini tanlab, keyingi choraklik o'rganish rejangizni shundan quring.

| Mavzu | Boshlang'ich | O'rta | Yuqori |
|---|---|---|---|
| JVM xotira | Heap va stack farqini biladi | GC log o'qiydi, pause sababini topadi | Region o'lchami va allocation rate bo'yicha sozlaydi |
| Concurrency | `synchronized` ishlatadi | Thread pool o'lchamini hisoblab beradi | Virtual thread va blocking chegarasini loyihalaydi |
| Spring konteyner | Bean e'lon qiladi | Proxy va self-invocation tuzog'ini biladi | Lifecycle va startup vaqtini boshqaradi |
| Tranzaksiya | `@Transactional` qo'yadi | Propagation va isolation tanlaydi | Flush, lock va retry siyosatini loyihalaydi |
| Hibernate | Entity yozadi | N+1 ni topib tuzatadi | Fetch strategiyasi va cache chegarasini belgilaydi |
| PostgreSQL planner | `EXPLAIN` chaqiradi | `EXPLAIN ANALYZE BUFFERS` o'qiydi | Statistika va index turini qarorga aylantiradi |
| Index dizayni | B-tree qo'yadi | Composite tartibini to'g'ri beradi | Partial, GIN va covering index tanlaydi |
| API dizayni | REST endpoint yozadi | Versiyalash va xato formatini belgilaydi | Mos keluvchanlik shartnomasini boshqaradi |
| Observability | Log yozadi | Metrika va alert qo'yadi | SLO va xato budjetini belgilaydi |
| Deploy | Pipeline ishlatadi | Migratsiyani mos keluvchan yozadi | Nol to'xtovli relizni loyihalaydi |
| Xavfsizlik | Autentifikatsiya yoqadi | Avtorizatsiya chegarasini tekshiradi | Sir boshqaruvi va audit izini quradi |
| Qaror yuritish | Fikrini aytadi | Variantlarni taqqoslaydi | Mezon va qaytarish yo'lini yozib qoldiradi |

## 39.8 Fikrlash va qarorlar bilimini o'zingizga qo'llash

Fikrlash va qarorlar qismidagi vositalar faqat tizimga emas, sizning karyerangizga ham tegishli. Qaytarib bo'lmaydigan qarorni sekin qabul qilish qoidasi sizning o'zingizga ham tegadi. Masalan yangi texnologiyaga butun jamoani ko'chirish qaytarib bo'lmaydigan qarordir, uni bitta servisda sinab ko'rish esa qaytariladi.

Xato budjeti tushunchasini o'z o'rganishingizga ham qo'llang. Chorakda ikkita yangi mavzuni chuqur o'rganish realistik budjet, beshta mavzu esa yuzaki natija beradi. Ikkinchi tartibli ta'sir haqida o'ylash qoidasi ham shu yerda ishlaydi: siz tanlagan texnologiya jamoaning uch yildan keyingi ishga olish imkoniyatini belgilaydi.

Eng muhimi esa qarorni yozib qoldirish odati. O'zingiz uchun qisqa jurnal yuritib boring: qanday qaror qabul qildim, qanday kutgandim, nima bo'ldi. Olti oydan keyin shu jurnal sizning eng kuchli o'qituvchingiz bo'ladi.

## 39.9 Java va JVM: o'zingizni sinash savollari

Quyidagi savollarga oq doskada javob bera olasizmi. Heap'dagi obyekt qachon eski avlodga o'tadi va bu pause vaqtiga qanday ta'sir qiladi. Thread pool o'lchamini CPU ga bog'liq va IO ga bog'liq ish uchun qanday hisoblaysiz. Virtual thread blocking chaqiruvni qanday kutadi va qaysi holatda u foyda bermaydi.

Yana bir sinov: diagnostikani buyruq bilan ko'rsatib bera olasizmi.

```bash
# JVM xotira holati: eski avlod to'lib borayotganini shu ko'rsatadi
jcmd <pid> GC.heap_info

# Thread holati: qancha thread BLOCKED yoki WAITING turibdi
jcmd <pid> Thread.print | grep -c "java.lang.Thread.State: BLOCKED"

# Eng ko'p xotira yeyayotgan sinflar: leak izlashning birinchi qadami
jcmd <pid> GC.class_histogram | head -15

# Native xotira: heap tashqarisidagi o'sish shu yerda ko'rinadi
jcmd <pid> VM.native_memory summary
```

Buyruqni eslamaslik xato emas. Lekin "native xotira heap tashqarisida o'sishi mumkin" degan mexanikani bilmaslik bo'shliqdir.

## 39.10 Spring: o'zingizni sinash savollari

Birinchi savol klassik: nega bitta sinf ichidagi metod chaqiruvi `@Transactional` ni ishga tushirmaydi. Javobda proxy so'zi bo'lishi kerak, chunki chaqiruv proxy orqali o'tmaydi.

```java
@Service
public class OrderService {

    // BU USUL ISHLAMAYDI: ichki chaqiruv proxy orqali o'tmaydi,
    // shuning uchun tranzaksiya ochilmaydi
    public void placeOrder(OrderRequest req) {
        validate(req);
        saveOrder(req);   // @Transactional kuchga kirmaydi
    }

    @Transactional
    public void saveOrder(OrderRequest req) {
        orderRepository.save(req.toEntity());
    }
}
```

Ikkinchi savol: `@Transactional` metod ichida tashqi to'lov provayderiga sinxron HTTP chaqiruv qilish nima uchun xavfli. Javob ikkita qismdan iborat: baza connection'i kutish vaqtida band turadi, va provayder javobi noaniq bo'lsa tranzaksiya natijasi ham noaniq bo'ladi.

Uchinchi savol: Spring Boot 3.x da startup vaqtini nima sekinlashtiradi va buni qanday o'lchaysiz. To'rtinchi savol: `@Async` ishlatilganda tranzaksiya konteksti nima bo'ladi. Beshinchi savol: ikkita bean bir xil turga ega bo'lsa, konteyner qanday tanlaydi va siz buni qanday boshqarasiz.

## 39.11 PostgreSQL: o'zingizni sinash savollari

Birinchi savol: planner nega index bor bo'lsa ham sequential scan tanlaydi. Javobda tanlanuvchanlik va statistika bo'lishi kerak, chunki ko'p qator qaytaradigan so'rov uchun scan arzonroq.

```sql
-- Bu rejani o'qib, muammoni ayta olasizmi
EXPLAIN (ANALYZE, BUFFERS, COSTS)
SELECT o.id, o.total, c.name
FROM orders o
JOIN customers c ON c.id = o.customer_id
WHERE o.created_at >= now() - interval '7 days'
  AND o.status = 'PAID'
ORDER BY o.created_at DESC
LIMIT 50;

-- Savol 1: rows=... va actual rows=... orasida 100 barobar farq bo'lsa nima qilasiz
-- Savol 2: shared read ko'p, shared hit kam bo'lsa bu nimani bildiradi
-- Savol 3: shu so'rov uchun qanday composite index yozasiz va ustun tartibi nega shunday
-- Savol 4: Sort tugunida "external merge Disk" chiqsa, qaysi parametrni ko'rasiz
```

Qolgan savollar: `REPEATABLE READ` va `SERIALIZABLE` orasidagi farq amalda qanday ko'rinadi. Uzun ochiq tranzaksiya nega `VACUUM` ishini buzadi. `FOR UPDATE SKIP LOCKED` navbat ishlashida nima beradi. Katta jadvalga yangi ustun qo'shish qachon jadvalni bloklaydi va qachon bloklamaydi.

## 39.12 Operatsion tayyorlik: o'zingizni sinash savollari

Bu bo'lim ko'pincha chetda qoladi, lekin tungi chaqiruvda faqat shu bilim ishlaydi. Birinchi savol: tizimingizda bitta so'rov bo'ylab trace ID uzilmasdan o'tadimi. Ikkinchi savol: eng muhim uchta alert qanday o'lchovga asoslangan va ularning yolg'on signal darajasi qancha.

```yaml
# Minimal operatsion tayyorlik: shu uchtasi bo'lmasa, tizim ko'r
management:
  endpoint:
    health:
      probes:
        enabled: true          # liveness va readiness ajratilgan
  health:
    livenessstate:
      enabled: true
    readinessstate:
      enabled: true
  tracing:
    sampling:
      probability: 0.1         # yuqori trafikda 10 foiz yetadi
  metrics:
    distribution:
      percentiles-histogram:
        http.server.requests: true   # p99 ni serverda hisoblash uchun
```

Uchinchi savol: oxirgi migratsiyani orqaga qaytarish rejasi bormi va u sinalganmi. To'rtinchi savol: ma'lumotlar bazasidan tiklanish vaqti qancha va bu raqam o'lchanganmi yoki taxminmi. Beshinchi savol: to'lov provayderi 30 sekund javob bermasa, tizimingiz qanday yomonlashadi. Agar bu beshta savolga raqam bilan javob bera olsangiz, siz operatsion jihatdan tayyorsiz.

## 39.13 Keyingi qadam: shu hujjatni va qolgan ikki hujjatni qanday ishlatish

Uchlik bitta maqsadga xizmat qiladi, lekin uchta turli paytda ishlatiladi. Bu hujjat qaror paytida ochiladi: nima uchun shunday bo'ladi va qanday raqam bilan tanlanadi. Dizayn [patternlar hujjati](../patterns/README.md) loyihalash paytida ochiladi, chunki u shaklni beradi. Testlash qo'llanmasi esa ishonchni tekshirish paytida ochiladi.

Amaliy tartib shunday bo'lsin. Yangi talab kelganda avval bu hujjatdan tegishli mexanika bobini o'qing, chunki qaror cheklovdan chiqadi. Keyin dizayn [patternlar hujjatidan](../patterns/README.md) shaklni tanlang, masalan tashqi tizimga ishonchli xabar yuborish uchun outbox pattern. Undan keyin [testlash qo'llanmasidagi](../testing/README.md) contract testing va Testcontainers bo'limlaridan tekshirish rejasini oling.

Jamoada ishlatishning eng yaxshi usuli esa birgalikda o'qishdir. Haftada bitta bob tanlang, uni ikki kishi o'qib chiqsin, keyin 30 daqiqada jamoaga o'z tizimingiz misolida tushuntirsin. Shu tartib bilim tarqalishini tezlashtiradi, va eng muhimi, u hujjatni o'lik matndan jamoa tiliga aylantiradi.

Oxirgi gap sizning o'zingiz haqida. Arxitektor bo'lish bilim miqdorida emas, qarorning sababini ko'rsatib bera olishda. Agar siz har bir qarorni cheklov, variant va o'lchov bilan tushuntirsangiz, jamoa sizdan keyin ham to'g'ri qaror qabul qilishni davom etadi. Shu esa bu hujjatning asl maqsadi edi.

## 39.14 Amalda qo'llash

- [ ] Birinchi haftada deploy pipeline, migratsiya tarixi va oxirgi uchta incident hisobotini o'qib, dejur injenerga "sizni nima uyg'otdi" savolini bering.
- [ ] `pg_stat_statements` va `pg_stat_user_tables` dan top 20 og'ir so'rov va yetishmayotgan index ro'yxatini chiqarib, biznesga ta'siri bo'yicha tartiblang.
- [ ] Barcha tashqi HTTP chaqiruvlarga connect va read timeout qo'yib, `statement_timeout` va `idle_in_transaction_session_timeout` ni yoqing.
- [ ] HikariCP pool o'lchamini so'rov davomiyligi hisobi bilan qayta belgilab, `pending` metrikasini dashboardga chiqaring.
- [ ] Ikkinchi oyda bitta ko'rinadigan yaxshilanishni oldingi va keyingi p99 raqami bilan e'lon qiling.
- [ ] Uchinchi oyda bir sahifali qaror hujjatini yozib, ichida ikkita variant, tanlash mezoni va qaytarish yo'lini bering.
- [ ] Yetuklik matritsasidan o'zingizga eng past ikkita mavzuni tanlab, chorakka faqat shu ikkitasini rejalashtiring.
- [ ] Shu bobdagi sinov savollaridan o'tib, "taniyman lekin tushuntirmayman" deb belgilangan har bir mavzuni jamoaga 30 daqiqada tushuntirib bering.

---

[&larr; 38. Doimiy o'rganish va texnologiya tanlash](38-doimiy-organish-va-texnologiya-tanlash.md) · [Mundarija](README.md)
