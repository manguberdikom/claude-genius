<!-- doc: architect | chapter: 3 | part: I. Fikrlash va qarorlar -->

[Barcha hujjatlar](../../README.md) / [Arxitektor miyasi](README.md)

> Holat: tekshirilmoqda. Da'volar hali manbaga solishtirilmoqda.

# 3. Qaror qabul qilish va uni hujjatlashtirish (Decisions and ADRs)

<details>
<summary>Bu bobdagi 22 bo'lim</summary>

- [3.1 ADR (Architecture Decision Record) tuzilishi: kontekst, qaror, oqibat, holat](#31-adr-architecture-decision-record-tuzilishi-kontekst-qaror-oqibat-holat)
- [3.2 Variantlarni taqqoslash: mezon jadvali va og'irlik berish](#32-variantlarni-taqqoslash-mezon-jadvali-va-ogirlik-berish)
- [3.3 Oxirgi mas'ul daqiqa (last responsible moment) tamoyili](#33-oxirgi-masul-daqiqa-last-responsible-moment-tamoyili)
- [3.4 Taxminlarni yozib qo'yish va keyin ularni tekshirish](#34-taxminlarni-yozib-qoyish-va-keyin-ularni-tekshirish)
- [3.5 Spike va prototip: qarorni ma'lumot bilan quvvatlash](#35-spike-va-prototip-qarorni-malumot-bilan-quvvatlash)
- [3.6 Jamoadagi kelishmovchilik va "rozi emasman, lekin bajaraman" qoidasi](#36-jamoadagi-kelishmovchilik-va-rozi-emasman-lekin-bajaraman-qoidasi)
- [3.7 Qaror oqibatini kuzatish: metrika va qayta ko'rish sanasi](#37-qaror-oqibatini-kuzatish-metrika-va-qayta-korish-sanasi)
- [3.8 ADR ni repoda saqlash, raqamlash va eskirganini belgilash](#38-adr-ni-repoda-saqlash-raqamlash-va-eskirganini-belgilash)
- [3.9 Yomon ADR belgilari: allaqachon qilingan ishni oqlash uchun yozilgan hujjat](#39-yomon-adr-belgilari-allaqachon-qilingan-ishni-oqlash-uchun-yozilgan-hujjat)
- [3.10 To'liq misol: PostgreSQL da qolish yoki alohida qidiruv tizimi qo'shish qarori](#310-toliq-misol-postgresql-da-qolish-yoki-alohida-qidiruv-tizimi-qoshish-qarori)
- [3.11 Nega eskiz kerak va nega ko'pchilik diagramma ishlamaydi](#311-nega-eskiz-kerak-va-nega-kopchilik-diagramma-ishlamaydi)
- [3.12 C4 modeli: to'rt daraja va har darajaning o'quvchisi](#312-c4-modeli-tort-daraja-va-har-darajaning-oquvchisi)
- [3.13 Kontekst diagrammasi: tizim chegarasi va tashqi aktyorlar](#313-kontekst-diagrammasi-tizim-chegarasi-va-tashqi-aktyorlar)
- [3.14 Konteyner diagrammasi: alohida deploy qilinadigan birliklar](#314-konteyner-diagrammasi-alohida-deploy-qilinadigan-birliklar)
- [3.15 Komponent diagrammasi va nega kod darajasiga tushmaslik kerak](#315-komponent-diagrammasi-va-nega-kod-darajasiga-tushmaslik-kerak)
- [3.16 "Kodda shunday qilasizmi" sinovi va model bilan kod orasidagi uzilish](#316-kodda-shunday-qilasizmi-sinovi-va-model-bilan-kod-orasidagi-uzilish)
- [3.17 Samarali eskiz: sarlavha, legend, javobgarlik va strelka](#317-samarali-eskiz-sarlavha-legend-javobgarlik-va-strelka)
- [3.18 Arxitektura ko'rinishi (view) va uni hujjatlashtirish qoidalari](#318-arxitektura-korinishi-view-va-uni-hujjatlashtirish-qoidalari)
- [3.19 Software guidebook: kod aytmagan narsani yozish](#319-software-guidebook-kod-aytmagan-narsani-yozish)
- [3.20 RFC: dizayn hujjatini fikr yig'ish uchun tarqatish](#320-rfc-dizayn-hujjatini-fikr-yigish-uchun-tarqatish)
- [3.21 Muhokama tiqilib qolganda qarorni ochish yo'llari](#321-muhokama-tiqilib-qolganda-qarorni-ochish-yollari)
- [3.22 Amalda qo'llash](#322-amalda-qollash)

</details>



Arxitektorning asosiy mahsuloti kod emas, qaror. Kod qaytarilishi mumkin, qaror esa jamoaning keyingi ikki yilini belgilaydi. Qaror yozilmasa, u yo'q: olti oydan keyin "nega bu yerda Kafka turibdi" degan savolga javob beradigan hujjat kerak. Bu bob qarorni qanday pishitish, qanday yozib qo'yish va keyin uning natijasini qanday kuzatish haqida.

## 3.1 ADR (Architecture Decision Record) tuzilishi: kontekst, qaror, oqibat, holat

ADR bitta arxitektura qarorini tasvirlaydigan qisqa matn fayli, odatda bir-ikki bet. Uni Michael Nygard blog postida birinchi bo'lib targ'ib qilgan, keyin u Thoughtworks Technology Radar da "adopt" belgisini olgan. Fayl oddiy matn bo'lishi mumkin, lekin odatda AsciiDoc yoki Markdown da, yoki wiki sahifa shabloni sifatida yoziladi (Neal Ford va boshqalar, *Software Architecture: The Hard Parts*, 1-bob, 5-bet).

Nygard shaklida sarlavha va uchta bo'lim bor. Sarlavha qarorni nomlaydigan qisqa ot iborasi. Kontekst muammoni bir-ikki gapda bayon qiladi va muqobil yechimlarni sanaydi. Qaror qarorning o'zini aytadi va uni batafsil asoslaydi: asoslash aynan shu bo'limda turadi, alohida "sabab" bo'limi kerak emas. Oqibatlar qaror qo'llangandan keyingi natijalarni va ko'rib chiqilgan trade-off larni yozadi (*The Hard Parts*, 1-bob, 5-bet).

Holat (Status) maydoni Nygard shakliga *Fundamentals of Software Architecture* 19-bobida qo'shilgan va uning qiymatlaridan biri Proposed. Korpusdagi nusxada shu kitobning 19-bob tanasi yo'q, faqat ilovadagi o'z-o'zini tekshirish savollari bor, shuning uchun bu yerda maydonlarning to'liq ro'yxati emas, faqat savollar tasdiqlagani iqtibos qilinadi: 19-bob ADR ning besh asosiy bo'limini tasvirlaydi, asoslash Qaror bo'limida turadi, alohida Alternatives bo'limi bo'lmasa muqobillar Kontekst da sanaladi, va Proposed holatini qo'yishning uch mezoni bor (Mark Richards, Neal Ford, *Fundamentals of Software Architecture*, ilova "Self-Assessment Questions", 19-bob savollari).

Eng ko'p xato qilinadigan joy kontekst. "Tizim tez ishlashi kerak" kontekst emas, chunki uni tekshirish mumkin emas: arxitektor "yuqori unumli" deb ayta olmaydi, u test yoki monitor o'lchay oladigan obyektiv qiymat berishi shart (*The Hard Parts*, 1-bob, 7-bet). Shunga ko'ra kontekst o'lchanadigan qiymat bilan yoziladi: qidiruvning hozirgi p95 si, maqsad qiymati, kunlik so'rov soni, baza hajmi. Kontekst o'qilganda qaror o'z-o'zidan kelib chiqishi kerak. Agar o'qiganingizda "unda nega boshqasini tanlamadilar" degan savol tug'ilsa, kontekst to'liq emas.

Oqibat bo'limi ADR ni boshqa hujjatdan ajratib turadi. *Fundamentals* ning birinchi qonuni shunday: arxitekturada hamma narsa trade-off, va arxitektor trade-off topilmadi deb o'ylasa, demak u hali topilmagan (1-bob, "Laws of Software Architecture" va Corollary 1). Rich Hickey ning shu kitobda keltirilgan gapi buni ochadi: dasturchi hamma narsaning foydasini biladi, trade-off ini bilmaydi, arxitektor ikkisini ham bilishi kerak (2-bob, "Analyzing Trade-Offs"). Shuning uchun "salbiy oqibat yo'q" degan ADR tahlil qilinmagan ADR. Qaytarish narxini ham shu yerga yozing: qaytarish kichik ishmi yoki migratsiyami.

Quyidagi shablon kitobdagi to'rt qismning (sarlavha, Kontekst, Qaror, Oqibatlar) ustiga shu korpusning qo'shimcha maydonlarini qo'yadi. Holat qiymatlaridan faqat "Taklif qilindi" (Proposed) kitobdan tasdiqlangan; qolgan qiymatlar va Sana, Qaror egasi, Qayta ko'rish sanasi, Taxminlar, Kuzatiladigan metrika maydonlari korpusning amaliy tanlovi.

```markdown
# ADR-0042: <Qaror sarlavhasi, qisqa ot iborasi>

- Holat: Taklif qilindi | Qabul qilindi | Rad etildi | Eskirdi | O'rnini bosdi
- Sana: 2026-03-11
- Qaror egasi: <ism>, ishtirokchilar: <jamoa>
- Qayta ko'rish sanasi: 2026-09-01
- Bog'liq ADR: ADR-0012 (o'rnini bosadi)

## Kontekst
Majburlovchi holat raqamlar bilan: latency, hajm, o'sish, muddat, cheklovlar.

## Qaror
Biz <X> ni tanlaymiz.

## Ko'rib chiqilgan variantlar
1. <Variant A>: rad etildi, sababi ...
2. <Variant B>: rad etildi, sababi ...

## Oqibatlar
- Ijobiy: ...
- Salbiy: ...
- Qaytarish narxi: <taxminan N kun / N oy>

## Taxminlar
- T1: <taxmin>. Tekshirish usuli: <o'lchov>. Muddat: <sana>.

## Kuzatiladigan metrika
- <metrika nomi>, hozirgi qiymat, maqsad qiymat, dashboard havolasi
```

| Masala | Oddiy yondashuv | Arxitektor yondashuvi |
|---|---|---|
| Qaror sababi | Chat xabarida qoladi | Repoda ADR fayli, kontekst raqamlari bilan |
| Variantlar | Bitta tanlangan variant aytiladi | Rad etilganlar va rad sababi yoziladi |
| Oqibat | Faqat foyda sanaladi | Narx, cheklov va qaytarish narxi yoziladi |
| Taxminlar | Boshda qoladi | Yozib qo'yiladi va tekshirish muddati beriladi |
| Qaror vaqti | Sprint boshida hammasi hal qilinadi | Oxirgi mas'ul daqiqaga qoldiriladi |
| Ma'lumot | "Men shunday o'ylayman" | Spike natijasi, EXPLAIN chiqishi, yuklama testi |
| Kelishmovchilik | Ovoz berish yoki eng baland ovoz | Yozma e'tiroz, qaror egasi, bajarish majburiyati |
| Natija | Deploy dan keyin unutiladi | Metrika va qayta ko'rish sanasi bilan kuzatiladi |
| Eskirgan qaror | Hujjat jimgina o'zgartiriladi | Yangi ADR yoziladi, eskisi "O'rnini bosdi" bo'ladi |

## 3.2 Variantlarni taqqoslash: mezon jadvali va og'irlik berish

Taqqoslashni jadvalga aylantirish muhokamani fikrdan mezonga ko'chiradi. Kitoblardagi trade-off jadvali ball yig'maydi: u yoki ustunlarni "afzallik" va "kamchilik" sifatida yozadi, yoki har mezonga sifat darajasini (juda past, past, o'rta, yuqori, juda yuqori) beradi va "qaysi biri muhimroq" savolini odamga qoldiradi. *Fundamentals of Software Architecture* 2-bobidagi topic va queue taqqoslashi shu shaklda va yakuniy javob "it depends" bo'lib qoladi; *The Hard Parts* 15-bobidagi jadvallar ham sifat darajalari bilan to'ldiriladi (402-403-betlar, Table 15-1 va Table 15-2).

Mezonlarni variantlarni ko'rib chiqishdan OLDIN yozing, aks holda mezonlar o'zingiz yoqtirgan variantga moslashib qoladi. *The Hard Parts* bu ro'yxatga MECE talabini qo'yadi: mutually exclusive, collectively exhaustive, ya'ni taqqoslanadigan narsalar bir-birining imkoniyatini qoplamasin va qaror maydonida ochiq qolgan variant qolmasin. Oddiy message queue ni butun enterprise service bus bilan taqqoslash noto'g'ri, chunki ular bir kategoriya emas; yuqori unumli navbatlarni baholaganda Kafka ni ro'yxatga kiritmaslik esa ro'yxatni to'liq qilmaydi (404-405-betlar).

Ikkita tuzoqdan saqlaning. Birinchisi kontekstdan chiqib ketish: yechimning ko'p yaxshi tomoni bo'lishi mumkin, lekin muvaffaqiyatga to'sqinlik qiladigan bitta imkoniyati yetishmasa, jadvaldagi umumiy ustunlik yolg'on ustunlik bo'lib chiqadi, shuning uchun mavjud barcha trade-off emas, to'g'ri to'plami tarozilanadi (405-407-betlar). Ikkinchisi dalilga ko'mib tashlash: arxitektor yiqqan texnik tafsilot nontexnik tarafga begona, shuning uchun tahlil bir necha kalit nuqtaga qisqartirib beriladi (410-bet).

Jadval qarorni chiqarmaydi, u qaror qayerda tug'ilishini ko'rsatadi. Umumiy va abstrakt mulohaza arxitektorni faqat ma'lum joygacha olib boradi: *The Hard Parts* domendagi aniq ssenariylarni modellashtirishni tavsiya qiladi, ya'ni har variant uchun bir nechta real ish oqimini chizib, haqiqiy trade-off nimaga borib taqalishini ochish (408-409-betlar). Formal metodika ham bor, masalan ATAM (Architecture Tradeoff Analysis Method), lekin *The Hard Parts* uni arxitektorning kundalik muammolaridan uzoq deb baholaydi (26-bet).

| Variant | Qidiruv sifati | Operatsion murakkablik | Ma'lumot izchilligi | Jamoadagi tajriba |
|---|---|---|---|---|
| PostgreSQL FTS | o'rta | past | yuqori | yuqori |
| Alohida qidiruv tizimi | yuqori | yuqori | past | past |

Sarlavhadagi "og'irlik berish" haqida ogohlantirish: mezonlarga raqamli og'irlik qo'yib og'irlangan yig'indi hisoblash usuli bu bobda iqtibos qilingan kitoblarning birortasida yo'q. Ular jadvalni sifat darajasi bilan to'ldiradi va ustuvorlikni ochiq savol sifatida qoldiradi, chunki og'irlangan ball bitta raqam chiqarib, aynan muhokama qilinishi kerak bo'lgan ustuvorlik tortishuvini yashirib qo'yadi. Og'irlik qo'ymoqchi bo'lsangiz, uni qaror hujjatida alohida yozing va ballni qaror sifatida emas, muhokama kirish nuqtasi sifatida ishlatib qo'ying.

## 3.3 Oxirgi mas'ul daqiqa (last responsible moment) tamoyili

Kechiktirish g'oyasining kitobdagi asosi aniq. *Clean Code* 11-bobi shunday deydi: qarorni oxirgi imkon bo'lgan daqiqaga qoldirish dangasalik emas, u eng yaxshi ma'lumot bilan xabardor tanlov qilish imkonini beradi, chunki muddatidan oldin qilingan qaror bu kam ma'lumot bilan qilingan qaror (Robert C. Martin, *Clean Code*, 11-bob "Systems", "Optimize Decision Making", 167-168-betlar). *Clean Architecture* buni mexanizm bilan bog'laydi: siyosat (business rules) detallardan ajratilsa, detallar haqidagi qaror kechiktirilishi mumkin, va variantlar qancha uzoq ochiq qolsa, qarorni qilish paytida qo'lda shuncha ko'p ma'lumot va shuncha ko'p o'tkazilgan eksperiment bo'ladi (Robert C. Martin, *Clean Architecture*, 15-bob, "Keeping Options Open", 140-142-betlar).

Tamoyil bahona bo'lib ham ishlatiladi. Simon Brown treninglarda arxitektura diagrammasida texnologiya qarori ko'rsatilmaganini so'raganida eng ko'p eshitgan javoblaridan biri aynan "biz 'last responsible moment' tamoyiliga amal qilamiz" bo'lgan; uning xulosasi: "har qanday texnologiyada qurish mumkin" degani "qurish kerak" degani emas, nofunksional talab yoki cheklov bo'lsa texnologiya tanlovi implementation detail emas (Simon Brown, *Software Architecture for Developers*, 26-bob, 67-bet va 39-bob, 116-118-betlar).

Qaysi qarorni kechiktirish mumkinligini Booch ning ta'rifi hal qiladi: arxitektura bu tizimni shakllantiruvchi muhim qarorlar, muhimlik esa o'zgartirish narxi bilan o'lchanadi, ya'ni arxitektura qarori bu tushdan keyingi bitta refactoring bilan qaytarib bo'lmaydigan qaror (Brown, 5-bob, 12-13-betlar). *Clean Architecture* detal deb aniq nomlaganlari: baza turi, web server, REST, dependency injection framework (140-142-betlar). Teskari tarafda *The Hard Parts* ogohlantiradi: bazani servis chegarasi ichiga ko'chirgandan keyin tranzaksionallik birinchi darajali arxitektura masalasiga aylanadi (26-bet), ya'ni tranzaksiya chegarasi kechiktirib bo'lmaydigan qarorlar qatorida.

Amalda bu shunday ko'rinadi. Buyurtma servisida "qanday message broker" savolini birinchi sprintda hal qilish shart emas, agar hodisani chiqarish interfeys orqasiga yashirilgan va dizayn [patternlar hujjatidagi](../patterns/README.md) outbox pattern bilan qurilgan bo'lsa. Lekin "buyurtma identifikatori UUID bo'ladimi yoki bigint" savoli sxemaga, indeks hajmiga va tashqi integratsiyaga kirib ketadi: uni keyin o'zgartirish kichik refactoring emas, migratsiya bo'ladi. ADR da "nega hozir" degan bir qatorni yozib qo'ying: bu qaror vaqtini ham hujjatlashtiradi.

## 3.4 Taxminlarni yozib qo'yish va keyin ularni tekshirish

Har bir qaror ostida tekshirilmagan taxminlar yotadi: "kunlik buyurtma soni shu chegaradan oshmaydi", "hisobot kechikishi bir necha daqiqa bo'lishi mumkin", "ombor qoldig'i faqat bitta mintaqada o'zgaradi". Taxmin aslida risk, va George Fairbanks ning risk-driven modeli aynan shu ro'yxatni talab qiladi: model tinimsiz savol berishdan boshlanadi, "risklarim nima, ularni kamaytirishning eng yaxshi usuli qaysi, risk yetarlicha yumshatildimi va kodga qaytsam bo'ladimi" (George Fairbanks, *Just Enough Software Architecture*, 3.1). Fairbanks risk-driven ishlamayotganining birinchi belgisini ham aytadi: dasturchi o'z risklarini va ularga qarshi qo'llagan usullarini sanab bera olmasligi (3.2). Taxmin yozilmasa, u shunchaki haqiqatga aylanib qoladi va hech kim uni shubha ostiga olmaydi.

Har bir taxminga uch narsa biriktiring: qanday o'lchanadi, qachon tekshiriladi, buzilsa nima qilinadi. Uchinchisi eng qimmatli: "chegara oshsa partitsiyalashga o'tamiz" degan qator keyingi arxitektorga tayyor yo'l xaritasi beradi. O'lchov tarafini *Fundamentals* ning talabi bilan yozing: arxitektura xarakteristikasi obyektiv ta'riflanmasa, u haqida muhokama ham bo'lmaydi, chunki bitta tashkilot ichida ham bo'limlar "unum" so'zini boshqacha tushunadi (Mark Richards, Neal Ford, *Fundamentals of Software Architecture*, 6-bob, "Measuring Architecture Characteristics").

Taxminni o'lchash ko'pincha bitta so'rov bilan hal bo'ladi. Ishlab chiqarish bazasida o'sish tezligini ko'rish uchun quyidagicha yozing, keyin natijani ADR ga nusxa qiling.

```sql
-- Taxmin T1: kunlik buyurtma soni 50 mingdan oshmaydi.
-- Oxirgi 90 kunning kunlik hajmi va o'sish trendi.
SELECT date_trunc('day', created_at)::date AS kun,
       count(*)                            AS buyurtma_soni,
       pg_size_pretty(sum(pg_column_size(o.*))) AS taxminiy_hajm
FROM orders o
WHERE created_at >= now() - interval '90 days'
GROUP BY 1
ORDER BY 1 DESC
LIMIT 10;

-- Jadval va indeks hajmi: qidiruv indeksi qancha joy egallaydi.
SELECT relname,
       pg_size_pretty(pg_relation_size(oid))       AS jadval,
       pg_size_pretty(pg_indexes_size(oid))        AS indekslar
FROM pg_class
WHERE relname IN ('orders', 'order_items')
  AND relkind = 'r';
```

Taxminni tekshirishni odamning esiga tayanib qoldirmang. Agar taxmin raqam bo'lsa, uni metrikaga aylantirib, chegara o'tilganda signal bering. Shunda taxmin o'z-o'zini tekshiradi.

## 3.5 Spike va prototip: qarorni ma'lumot bilan quvvatlash

Spike bu vaqti chegaralangan tadqiqot: maqsadi mahsulot emas, javob. Spike ni boshlashdan oldin uch narsani yozing: qaysi savolga javob izlayapmiz, qancha vaqt beramiz, qanday natija javob hisoblanadi. Vaqt chegarasi bo'lmasa spike loyihaga aylanadi.

Qachon to'xtash kerakligini Fairbanks aytadi: usulni qo'llash ko'pincha qog'ozda yoki doskada model qurish demakdir, model esa oraliq mahsulot, va arxitektura risklarni yopishga yaraydi degan ishonch paydo bo'lgan zahoti model ustida ishlashni to'xtatish mumkin. Uning asosiy printsipi ham shu: arxitektura ishiga ketadigan kuch nosozlik riski bilan mutanosib bo'lishi kerak (George Fairbanks, *Just Enough Software Architecture*, 3.6).

Spike natijasi ADR ga kirishi shart. *Documenting Software Architectures* ning qoidasi aniq: agar siz dizayn variantlarini baholash uchun texnik eksperiment, tadqiqot o'tkazgan yoki prototip qurgan bo'lsangiz, shu ishning xulosasi tanlangan variantning rationale si sifatida yozib qo'yilishi kerak (Paul Clements va boshqalar, *Documenting Software Architectures: Views and Beyond*, 2-nashr, Prolog, "Rule 5: Record Rationale", 44-bet). Simon Brown ham decision log da proof of concept, unum testi natijasi va mahsulot baholash hujjatlariga havola berishni aytadi (*Software Architecture for Developers*, 60-bob, 172-173-betlar).

Qidiruv qarori uchun spike shunday ko'rinadi: haqiqiy ma'lumotning nusxasini oling, indeks quring, o'nta tipik so'rovni o'lchang. Sun'iy ma'lumotda o'lchash behuda, chunki PostgreSQL planner statistikaga qarab boshqa plan tanlaydi.

```sql
-- Spike S-07: PostgreSQL full text search 300 ms ga sig'adimi.
-- 1. Generated ustun va GIN indeks.
ALTER TABLE orders
  ADD COLUMN search_doc tsvector
  GENERATED ALWAYS AS (
    to_tsvector('simple',
      coalesce(customer_name, '') || ' ' ||
      coalesce(order_number, '') || ' ' ||
      coalesce(notes, ''))
  ) STORED;

CREATE INDEX CONCURRENTLY idx_orders_search
  ON orders USING gin (search_doc);

-- 2. Haqiqiy so'rovni o'lchash. Buffer va vaqt bilan.
EXPLAIN (ANALYZE, BUFFERS)
SELECT id, order_number, created_at,
       ts_rank(search_doc, q) AS reyting
FROM orders, websearch_to_tsquery('simple', 'alisher toshkent') q
WHERE search_doc @@ q
ORDER BY reyting DESC, created_at DESC
LIMIT 20;
```

Natijani o'qiyotganda ikki raqamga qarang: Execution Time va shared read bloklari soni. Agar plan Bitmap Index Scan ko'rsatsa va bloklar soni cache ga sig'sa, bu yondashuv ishlaydi. Agar Seq Scan qolsa yoki ORDER BY katta natija to'plamini saralashga majbur qilsa, raqam yuklama ostida yomonlashadi.

## 3.6 Jamoadagi kelishmovchilik va "rozi emasman, lekin bajaraman" qoidasi

Texnik kelishmovchilikni yo'q qilish kerak emas, uni muhokama qilinadigan shaklga keltirish kerak. Fairbanks ning yechimi qaror qabul qilish jarayonini ochiq qo'yish: "A varianti yaxshi" va "B varianti yaxshi" degan ikki fikr orasida tanlash qiyin, lekin har biri sabab shabloni bilan yozilsa, A usability ga, B esa testability ga yordam berishi ko'rinadi va savol "kim yaxshi dizayner" dan "loyiha uchun qaysi sifat ustuvor" ga ko'chadi. Fairbanks buni muhokamadan ego ni olib tashlash deb ataydi (George Fairbanks, *Just Enough Software Architecture*, 5.4).

Shablonning o'zi ham shu bo'limda: "<x> ustuvor, shuning uchun <y> dizaynini tanladik va <z> kamchiligini qabul qildik" (5.4). Risk tarafida Fairbanks shuni ham ko'rsatadi: risk-driven model baholab ko'rish mumkin bo'lgan dalil beradi, ya'ni "A, B, C ni risk deb bildik, B birlamchi, uni kamaytirish uchun X va Y usullarini qo'lladik, natijani baholadik va yetarli deb topdik" shaklidagi argument. Boshqa dasturchi bunga qarshi shu shakldagi argument qo'yib, masalan D riskini qo'shishni taklif qilib, muhokamani injenerlik muhokamasiga aylantira oladi (3.1, "Logical rationale").

Shuning uchun muhokama davrida har kim e'tirozini yozma shaklda, ADR ga izoh sifatida qo'yishi kerak. Yozma e'tiroz og'zakisidan foydaliroq, chunki u shu shaklni tutishga majbur qiladi: "menga yoqmaydi" dan "bu yondashuvda hisobot so'rovi asosiy bazaga yuk beradi" ga o'tadi. Rad etilgan e'tiroz ADR ichida ko'rinadigan joyda qoladi, chunki *Documenting Software Architectures* rad etilgan muqobillarni va rad sababini yozib qo'yishni talab qiladi (Paul Clements va boshqalar, *Documenting Software Architectures: Views and Beyond*, 2-nashr, Prolog, "Rule 5: Record Rationale", 44-bet).

Sarlavhadagi "rozi emasman, lekin bajaraman" qoidasi va har ADR ga bitta qaror egasini tayinlash shu korpusning amaliy tanlovi: yuqoridagi kitoblarda bu nom bilan qoida yo'q. Mazmuni oddiy: e'tiroz yozib qoldiriladi, lekin qaror chiqqandan keyin hamma bir xil qarorni bajaradi va unga qarshi ishlamaydi, e'tiroz esa qayta ko'rish sanasida metrika bilan birga qayta ochiladi.

## 3.7 Qaror oqibatini kuzatish: metrika va qayta ko'rish sanasi

Qarorni hujjatlash bilan uning to'g'ri qo'llanishini nazorat qilish ikki boshqa ish. *The Hard Parts* buni ADR bo'limidan keyin darhol aytadi: qarorni yozib qo'yish arxitektor uchun muhim, lekin qarorning to'g'ri ishlatilishini boshqarish alohida mavzu, va zamonaviy injenerlik amaliyoti bu boshqaruvning ko'p qismini architecture fitness function lar bilan avtomatlashtiradi (Neal Ford va boshqalar, *Software Architecture: The Hard Parts*, 1-bob, 5-6-betlar). Fitness function ning ta'rifi "biror arxitektura xarakteristikasining obyektiv butunlik bahosini beradigan har qanday mexanizm", va shu ta'rifning kalit sharti: arxitektor "yuqori unumli" deb ayta olmaydi, u test yoki monitor o'lchay oladigan obyektiv qiymat berishi shart (7-bet). Shuning uchun ADR da kamida bitta o'lchanadigan metrika bo'lishi kerak va u qarorning asosiy da'vosini o'lchasin: "qidiruv tezlashadi" degan qaror uchun qidiruv latency si o'lchanadi, umumiy CPU emas.

Metrikaning shaklini tanlashda *Fundamentals* ikki ogohlantirish beradi. Birinchisi: faqat o'rtachani o'lchash chegaradagi holatni yashiradi, so'rovlarning kichik ulushi bir necha barobar sekin ketsa u o'rtachada ko'rinmaydi, shuning uchun outlier ni ushlaydigan o'lchov ham kerak. Ikkinchisi: yetuk jamoalar maqsad qiymatni o'zboshimchalik bilan tanlamaydi, uni statistik tahlilga tayantiradi va real metrika modeldan chiqib ketsa signal beradi (Mark Richards, Neal Ford, *Fundamentals of Software Architecture*, 6-bob, "Operational Measures" va "The Many Flavors of Performance").

Metrikani kod yozilgan paytda joylashtiring, keyin emas. Micrometer bilan bu bir necha qatorlik ish va natijasi ADR ning haqiqiy nazoratchisi bo'ladi.

```java
@Service
public class OrderSearchService {
    private final Timer qidiruvVaqti;
    private final Counter boshNatija;
    private final OrderSearchRepository repository;

    public OrderSearchService(MeterRegistry registry, OrderSearchRepository repository) {
        this.repository = repository;
        // ADR-0042 metrikasi: p95 maqsad 300 ms.
        this.qidiruvVaqti = Timer.builder("order.search.duration")
                .description("Buyurtma qidiruvi davomiyligi")
                .publishPercentiles(0.5, 0.95, 0.99)
                .tag("engine", "postgres_fts")
                .register(registry);
        this.boshNatija = Counter.builder("order.search.empty")
                .register(registry);
    }

    public List<OrderView> search(String query, Pageable page) {
        return qidiruvVaqti.record(() -> {
            List<OrderView> natija = repository.search(query, page);
            if (natija.isEmpty()) {
                boshNatija.increment();  // sifat signali, tezlik emas
            }
            return natija;
        });
    }
}
```

Natijasiz qidiruvlar ulushi muhim, chunki tezlik yaxshilanib, sifat yomonlashishi mumkin. Qayta ko'rish sanasi kelganda uchta javobdan birini yozasiz: qaror o'zini oqladi, qaror qisman ishladi va tuzatish kerak, yoki qaror xato bo'ldi va yangi ADR yoziladi. Uchinchi javob eng qimmatli, lekin uni faqat sana va metrika bo'lgan jamoa chiqara oladi.

## 3.8 ADR ni repoda saqlash, raqamlash va eskirganini belgilash

Saqlash joyi haqida kitob ikki variantni teng qo'yadi: ADR matn fayli (AsciiDoc yoki Markdown) yoki wiki sahifa shabloni bo'lishi mumkin (Neal Ford va boshqalar, *Software Architecture: The Hard Parts*, 1-bob, 5-bet). Shu korpus kod bilan bir repoda, `docs/adr/` papkasida saqlashni tanlaydi, chunki pull request ichidagi fayl review ga tushadi. Nom shabloni `NNNN-qisqa-sarlavha.md`, raqam to'rt xonali va ketma-ket; raqam qayta ishlatilmaydi, hatto ADR rad etilgan bo'lsa ham. Nom shabloni va raqamlash qoidasi korpusning tanlovi, kitobda bunday shablon yo'q.

Qaysi joyni tanlasangiz ham, asosiy shart hujjatning yangiligi. *Documenting Software Architectures* buni alohida qoida qilib qo'yadi: to'liq bo'lmagan yoki eskirgan hujjat haqiqatni aks ettirmaydi va ishlatilmaydi, yangilanib turgan hujjat esa ishlatiladi, chunki tizim haqidagi savolga eng tez javob shu hujjatdan topiladi (Paul Clements va boshqalar, *Documenting Software Architectures: Views and Beyond*, 2-nashr, Prolog, "Rule 6: Keep Documentation Current but Not Too Current", 44-45-betlar).

Eskirgan ADR o'chirilmaydi va tahrirlanmaydi. Uning holati `Eskirdi` yoki `O'rnini bosdi: ADR-0057` ga o'zgaradi va shu bitta qator qo'shiladi. Mazmuni esa o'sha paytdagi haqiqat sifatida qoladi. Buning sababi "Rule 5" da yozilgan: qaror keyinchalik shubha ostiga olinganda yoki o'zgartirish bosimi paydo bo'lganda siz o'sha dalillarni yana boshidan ko'rib chiqasiz va nega boshqa yo'ldan bormaganingizni o'ylab qolasiz, sababni yozib qo'yish esa uzoq muddatda katta vaqt tejaydi (44-bet).

```bash
#!/usr/bin/env bash
# docs/adr/new.sh: keyingi ADR raqamini topib, shablondan fayl yaratadi.
set -euo pipefail

DIR="$(dirname "$0")"
LAST=$(ls "$DIR" | grep -E '^[0-9]{4}-' | sort | tail -n 1 | cut -c1-4)
NEXT=$(printf "%04d" $((10#${LAST:-0} + 1)))
SLUG=$(echo "$*" | tr '[:upper:] ' '[:lower:]-' | tr -cd 'a-z0-9-')

cp "$DIR/template.md" "$DIR/$NEXT-$SLUG.md"
sed -i "s/ADR-0000/ADR-$NEXT/; s/<SANA>/$(date +%F)/" "$DIR/$NEXT-$SLUG.md"
echo "Yaratildi: $DIR/$NEXT-$SLUG.md"
```

CI da ikkita oddiy tekshiruv katta foyda beradi: har bir ADR da `Holat` qatori borligi va qayta ko'rish sanasi o'tgan ADR lar ro'yxatini chiqarish.

```yaml
# .github/workflows/adr-check.yml dagi qadamlar
- name: ADR holat qatori bormi
  run: |
    for f in docs/adr/[0-9]*.md; do
      grep -q '^- Holat:' "$f" || { echo "Holat yo'q: $f"; exit 1; }
    done

- name: Qayta ko'rish sanasi o'tgan ADR lar
  run: |
    BUGUN=$(date +%F)
    grep -H '^- Qayta ko.rish sanasi:' docs/adr/[0-9]*.md \
      | awk -v t="$BUGUN" -F': ' '$2 != "" && $2 < t {print "Muddati o-tdi: " $0}'
```

## 3.9 Yomon ADR belgilari: allaqachon qilingan ishni oqlash uchun yozilgan hujjat

Eng keng tarqalgan nosog'lom ADR bu keyin yozilgan oqlash hujjati. Uni tanib olish oson: unda bitta variant bor, salbiy oqibatlar bo'limi bo'sh yoki "jiddiy salbiy oqibat yo'q" deb yozilgan, va kontekstda o'lchanadigan qiymat yo'q. Uchta belgining uchtasi ham kitobdagi talabni buzadi: muqobillar Kontekst da sanalishi kerak (*The Hard Parts*, 1-bob, 5-bet), rad etilgan muhim muqobillar va rad sababi yozilishi kerak (*Documenting Software Architectures*, 2-nashr, Prolog, "Rule 5", 44-bet), trade-off topilmagan bo'lsa demak u hali topilmagan (*Fundamentals of Software Architecture*, 1-bob, Corollary 1). Agar qaror chindan ham allaqachon qilingan bo'lsa, buni ochiq yozing: "bu qaror avval amalga oshirilgan, ADR retrospektiv yozilmoqda". Shu bir gap hujjatning ishonchini saqlaydi.

*Fundamentals* 19-bobi arxitektura qarorining alohida antipatternlarini nomlaydi, ular ichida "covering your assets" va "email-driven architecture" bor. Korpusdagi nusxada 19-bobning tanasi yo'q, faqat ilovadagi savollar bu nomlarni tasdiqlaydi, shuning uchun bu yerda ularning tavsifi berilmaydi: nomlari sanaladi va tavsif uchun asl 19-bobga murojaat qilish kerak (*Fundamentals of Software Architecture*, ilova "Self-Assessment Questions", 19-bob savollari).

| Tuzoq | Nega xavfli | Yechim |
|---|---|---|
| Bitta variantli ADR | Muqobil ko'rib chiqilmaganini yashiradi | Kamida ikki rad etilgan variant va rad sababi |
| Salbiy oqibatsiz ADR | Narx yashiringan, keyin kutilmagan bo'lib chiqadi | "Salbiy" bo'limi bo'sh ADR review dan o'tmaydi |
| O'lchovsiz kontekst | Qaror did asosida qilinganini bildiradi | Test yoki monitor o'lchay oladigan qiymat yoziladi (*The Hard Parts*, 7-bet) |
| Eski ADR ni tahrirlash | Tarix yo'qoladi, sabab izi uziladi | Yangi ADR, eskisiga "O'rnini bosdi" |
| Uzun ADR | Hech kim o'qimaydi | Odatdagi ADR bir-ikki bet (*The Hard Parts*, 5-bet), chuqur tahlil ilova havolasida |
| Sanasiz qayta ko'rish | Qaror hech qachon tekshirilmaydi | Majburiy maydon, CI tekshiradi (korpus tavsiyasi) |
| Egasi yo'q ADR | Javobgarlik tarqaladi | Bitta ism, jamoa nomi yetarli emas (korpus tavsiyasi) |
| Spike natijasiz qaror | Taxmin ma'lumot o'rniga qo'yiladi | Eksperiment va prototip xulosasi rationale sifatida yoziladi (*Documenting Software Architectures*, 44-bet) |

## 3.10 To'liq misol: PostgreSQL da qolish yoki alohida qidiruv tizimi qo'shish qarori

Bu bo'lim shartli misol: quyidagi barcha raqam o'lchanmagan taxmin, ular ADR ning shaklini ko'rsatish uchun qo'yilgan, biror kitob yoki o'lchovdan olingan emas. Holat shunday. Buyurtma qidiruvi admin panelda ishlatiladi, kunlik taxminan 40 ming so'rov, `orders` jadvalida 42 million qator, jadval hajmi taxminan 180 GB. Hozirgi qidiruv `ILIKE '%...%'` bilan qurilgan va p95 da 1.8 soniya beradi. Maqsad 300 ms. Jamoa uch kishi, alohida infratuzilma injeneri yo'q. Spike S-07 natijasi: generated `tsvector` ustun va GIN indeks bilan p95 taxminan 90 ms, indeks hajmi taxminan 11 GB, yozish tezligi sezilarli darajada pasaydi.

```markdown
# ADR-0042: Buyurtma qidiruvini PostgreSQL FTS da qoldirish

- Holat: Qabul qilindi
- Sana: 2026-03-11
- Qaror egasi: A. Qoraev. Ishtirokchilar: order-platform jamoasi
- Qayta ko'rish sanasi: 2026-09-01

## Kontekst
42 mln qator, 180 GB, kunlik 40 ming qidiruv. ILIKE bilan p95 = 1.8 s,
maqsad 300 ms. Jamoa 3 kishi. Spike S-07: GIN + tsvector da p95 = 90 ms.

## Qaror
Qidiruvni PostgreSQL full text search ustida qoldiramiz.

## Ko'rib chiqilgan variantlar
1. Alohida qidiruv klasteri: qidiruv sifati yuqori, lekin operatsion
   murakkablik yuqori va izchillik eventual bo'lib qoladi.
2. Faqat trigram (pg_trgm): opechatkaga chidamli, lekin ranking yo'q.

## Oqibatlar
- Ijobiy: yangi tizim yo'q, qidiruv tranzaksiya bilan izchil.
- Salbiy: morfologiya cheklangan, facet va fuzzy qidiruv zaif.
- Qaytarish narxi: migratsiya darajasida (outbox bilan indeksga ko'chirish).

## Taxminlar
- T1: qidiruv hajmi yil davomida belgilangan chegaradan oshmaydi.
  O'lchov: QPS metrikasi.

## Kuzatiladigan metrika
- order.search.duration p95 maqsad qiymati, order.search.empty ulushi
```

Qaror sozlash bilan to'liq bo'ladi. Qidiruv so'rovi analitik xarakterda, shuning uchun uni alohida connection pool va qisqa statement timeout ortiga qo'yish kerak, aks holda bitta og'ir so'rov asosiy buyurtma oqimini to'sib qo'yadi.

```properties
# Qidiruv uchun alohida pool: asosiy oqimdan ajratilgan.
spring.datasource.search.hikari.maximum-pool-size=8
spring.datasource.search.hikari.connection-timeout=2000
spring.datasource.search.hikari.pool-name=search-pool

# Qidiruv so'rovi 1 soniyadan oshsa uzilsin, foydalanuvchi kutmasin.
spring.datasource.search.hikari.data-source-properties.options=-c statement_timeout=1000

# Hibernate ni bu pool da faqat o'qish uchun ishlatamiz.
spring.jpa.properties.hibernate.jdbc.fetch_size=50
```

Bu ADR nimani ko'rsatdi: tanlov "yaxshi texnologiya" bilan "yomon texnologiya" orasida emas edi. Tanlov jamoa o'lchami, izchillik talabi va spike natijasi orasida edi, ya'ni savol "qaysi biri yaxshi" emas, "qaysi biri muhimroq" edi - *Fundamentals* 2-bobida trade-off tahlili aynan shu savol bilan yopiladi va javob "it depends" bo'ladi. Agar keyinchalik facet qidiruv mahsulot talabiga aylansa, qidiruv sifati haqidagi taxmin buziladi, ADR-0042 "O'rnini bosdi" bo'ladi va yangi ADR alohida indeks hamda outbox orqali sinxronizatsiyani yozadi. Bu muvaffaqiyatsizlik emas, bu ADR ning maqsadga muvofiq ishlashi.

## 3.11 Nega eskiz kerak va nega ko'pchilik diagramma ishlamaydi

Jamoalar jarayonni vizuallashtirishni o'rgandi: Kanban taxtasi bir qarashda nima boshlanmagan, nima ishda va nima tugaganini ko'rsatadi. Simon Brown ning kuzatuvi shu: biz qurayotgan dasturning o'zini vizuallashtirishni unutib qo'ydik, va arxitekturani tushunish bilan uni muloqotda yetkazib bera olish bir narsa emas. Minglab odam bilan arxitektura mashg'uloti o'tkazgandan keyin uning xulosasi aniq: tizim arxitekturasini vizuallashtirish juda kam odamda bor ko'nikma, diagramma chizadiganlar ko'p, lekin bu diagrammalar ko'p narsani o'quvchining tasavvuriga qoldiradi (Simon Brown, *Software Architecture for Developers*, Leanpub, 32-bob, 79-bet).

Brown qutilar va chiziqlardan iborat norasmiy eskizning sakkiz tipik nuqsonini sanaydi: rang kodi tushuntirilmagan yoki izchil emas; qutilar va chiziqlarning turli uslublari nimani bildirishi aytilmagan; elementlar orasidagi kalit munosabat yo'q yoki noaniq; "business logic" kabi umumiy atamalar ishlatilgan; texnologiya tanlovi tushirib qoldirilgan; abstraksiya darajalari aralashtirilgan; diagramma juda ko'p tafsilot ko'rsatishga urinadi; diagrammada kontekst yoki mantiqiy boshlanish nuqtasi yo'q (32-bob, 80-bet). Shu yerdan bitta amaliy sinov chiqadi: kimdir sizga eskiz bilan dizayn ko'rsatsa, o'zingizdan so'rang, u eskizda turgan narsani aytayaptimi yoki o'z boshidagi narsani.

Eskiz chizish rassomlik emas. Brown bu haqda ochiq yozadi: muhimi san'at asari yasash emas, narsaning tubiga tez tushib, muhim nuqtalarni boshqalar tushunadigan shaklda qisqa bayon qilish. Gap batafsil modellashtirish yoki model asosida kod generatsiya qilish haqida ham emas (33-bob, 83-bet). Eskizning foydasi ro'yxat bilan beriladi: jamoada umumiy ko'rinish va umumiy maqsad tasavvuri paydo bo'ladi; texnik suhbat uchun bitta fokus nuqtasi bo'ladi; dasturchi kod ichida yurganda eskiz xarita bo'lib ishlaydi; jamoadan tashqaridagi odamlarga (operatsiya, qo'llab-quvvatlash, biznes) tushuntirish osonlashadi; yangi dasturchining jamoaga kirishi tezlashadi. Brown ning o'z xulosasi: kontekst, konteyner va komponent diagrammalari odatda yetarli (83-bet).

Brown mashg'ulotlarda to'plangan samarasiz eskizlarni nomlab chiqadi, va bu nomlar tashxis qo'yish uchun qulay (34-bob, 84-97-betlar).

| Eskiz turi | Nimasi yetishmaydi |
|---|---|
| "Xarid ro'yxati" (the shopping list) | Faqat texnologiya nomlari turadi; qaysi mahsulot nima qilayotgani va ular orasidagi ulanish yo'q |
| "Qutilar bor, chiziq yo'q" (boxes and no lines) | Javobgarlik va o'zaro ta'sir yo'q; arxitektura narsalar bilan birga ularning ta'sirini ham bildiradi |
| "Funksional ko'rinish" (the functional view) | Funksional bo'linish chizilgan, lekin javobgarlik, ta'sir va rang kodining ma'nosi yo'q |
| "Aviachipta marshrut xaritasi" (the airline route map) | Markazda tushunarli oqim bor, atrofida izohsiz belgi, turli rang va uslubdagi chiziqlar |
| "Umumiy ma'noda to'g'ri" (generically true) | Markazda "business logic" qutisi turadi; domen nomi yo'q, shuning uchun hech narsa aytmaydi |
| "Mantiqiy ko'rinish" (the logical view) | Shakl va javobgarlik bor, texnologiya tanlovi tasavvurga qoldirilgan |
| Nomlanmagan aktyorlar | Foydalanuvchi qutisi bor, lekin u kim ekani yozilmagan: yuzsiz nusxalar |

Uchinchi sabab ham bor va u tashkiliy: Brown ko'pchilik jamoa agile ga shoshilishda modellashtirish va hujjatni reja asosidagi metodologiya bilan birga uloqtirib yuborganini, UML ni tashlaganini va bu ko'nikmani o'rgatadigan odam juda kam ekanini aytadi (34-bob, 84-bet).

## 3.12 C4 modeli: to'rt daraja va har darajaning o'quvchisi

Dasturni rasm bilan tushuntirganda odamlarning tipik xatosi bitta "uber-diagramma" yasash: unda barcha abstraksiya darajasidagi barcha tafsilot bir vaqtda bo'lishi kerak. Natija tirband, murakkab va chalkash rasm bo'ladi. Brown ning yechimi oddiy: bitta murakkab diagramma o'rniga turli abstraksiya darajasida bir nechta sodda diagramma chiziladi (Simon Brown, *Software Architecture for Developers*, Leanpub, 35-bob, 98-bet).

Buning uchun umumiy abstraksiyalar to'plami kerak. Brown ning ierarxiyasi: tizim bir nechta konteynerdan tashkil topadi, konteyner bir nechta komponentdan, komponent esa bir yoki bir nechta sinf bilan amalga oshiriladi. Sinf OO tilda eng kichik qurilish bloki. Komponent bir yoki bir nechta sinfning mantiqiy guruhi, yuqori darajali shartnoma ortida turadi. Konteyner komponentlar bajariladigan yoki ma'lumot yashaydigan narsa: web server, ilova serveri, boy klient yoki baza. Tizim eng yuqori daraja va kimgadir qiymat yetkazadigan narsani bildiradi (35-bob, 99-bet).

Shu abstraksiyalar ustida Brown dasturning statik ko'rinishini to'rt turdagi diagramma bilan xulosalaydi: kontekst (sahnani qo'yadi, kalit bog'liqlik va aktyorlarni ko'rsatadi), konteyner (yuqori darajali texnologiya tanlovi, javobgarlikning taqsimlanishi, konteynerlar qanday muloqot qilishi), komponent (har konteyner uchun kalit mantiqiy komponentlar va ularning munosabati) va sinf (ixtiyoriy daraja, faqat biror pattern yoki komponent qanday amalga oshirilganini tushuntirish kerak bo'lsa) (35-bob, 100-bet). O'quvchi har darajada boshqacha, va Brown uni har bobda alohida yozadi.

| Daraja | Nimani ko'rsatadi | O'quvchi | Manba |
|---|---|---|---|
| Kontekst | Tizim chegarasi, foydalanuvchilar, qo'shni tizimlar | Texnik va notexnik, jamoa ichi va tashqarisi | 36-bob, 104-bet |
| Konteyner | Alohida deploy qilinadigan birliklar va texnologiya tanlovi | Jamoa ichi va tashqarisidagi texnik odamlar, operatsiya va qo'llab-quvvatlash xodimi ham | 37-bob, 108-bet |
| Komponent | Bitta konteyner ichidagi mantiqiy komponentlar | Faqat ishlab chiqish jamoasi ichidagi texnik odamlar | 38-bob, 113-bet |
| Sinf | Bitta pattern yoki komponentning ichki tuzilishi | Ishlab chiqish jamoasi; ixtiyoriy daraja | 35-bob, 100-bet |

Brown uchun umumiy abstraksiya to'plami umumiy notatsiyadan muhimroq: UML ikkisini ham beradi, lekin uni samarali ishlatadigan jamoa kam uchraydi. Xarita analogiyasi shu fikrni ochadi: barcha xarita yo'l, daryo, ko'l va shahar ko'rsatadi, lekin rang, chiziq uslubi va belgilar har xil; ularni tushunish kaliti burchakdagi legend (35-bob, 100-bet). Shuning uchun norasmiy eskiz izchillikni moslashuvchanlikka almashtiradi va har diagrammada kichik legend bo'lishi kerak. Yana bir maslahat: faqat nomlangan qutilar to'plamidan iborat diagramma yasamang, qutiga javobgarlikni yozish noaniqlikni olib tashlaydi (101-bet).

C4 bitta tizimga qaraydi. Agar tashkilotdagi barcha tizim qanday joylashganini ko'rsatish kerak bo'lsa, Brown C4 ustiga yana bitta diagramma qo'yadi va model C5 ga aylanadi: tashkilot chegarasi, ichki va tashqi foydalanuvchilar, ichki va tashqi tizimlar (javobgarlik xulosasi va kimga qanday ma'lumot tegishli ekani bilan). Har qiziqtirgan tizim uchun esa C4 bo'yicha pastga tushiladi (44-bob, 138-bet).

Mark Richards va Neal Ford ning *Fundamentals of Software Architecture* kitobida C4 ga alohida bob (21-bob, "Diagramming and Presenting Architecture") bag'ishlangan, lekin korpusdagi nusxada shu bobning tanasi yo'q: PDF 20-bobdan 24-bobga o'tadi. Faqat ilovadagi o'z-o'zini tekshirish savollari C4 ning "to'rt C" si haqida savol borligini tasdiqlaydi. Shuning uchun bu yerda shu kitobdan hech narsa iqtibos qilinmaydi, C4 ning butun bayoni Brown dan olingan (Mark Richards, Neal Ford, *Fundamentals of Software Architecture*, ilova "Self-Assessment Questions", 21-bob savollari).

## 3.13 Kontekst diagrammasi: tizim chegarasi va tashqi aktyorlar

Kontekst diagrammasi uch savolga javob beradi: biz qanday tizim qurayapmiz yoki qurganmiz, undan kim foydalanadi, va u mavjud IT muhitiga qanday joylashadi (Simon Brown, *Software Architecture for Developers*, Leanpub, 36-bob, 102-bet). Shakli juda oddiy: markazda tizimingiz bitta quti bo'lib turadi, atrofida foydalanuvchilar va u bilan integratsiyaga kiradigan boshqa tizimlar. Brown bu yerda tafsilot muhim emasligini ta'kidlaydi: bu keng burchakli ko'rinish, va fokus texnologiya va protokolda emas, odam va tizimda (102-bet, 105-bet).

Chiziqlarni izohsiz qoldirmang. Brown har o'zaro ta'sirni maqsad bilan annotatsiya qilishni tavsiya qiladi, foydalanuvchi va tizim orasidagi chiziqqa esa shu turdagi foydalanuvchi tizimdan qanday foydalanishini xulosalaydigan bir necha muhim use case ni qisqa ro'yxat qilib yozib qo'yadi (36-bob, 103-bet).

Nega bu oddiy rasm foydali ekanini Brown to'rt punktda beradi: kontekst ochiq yoziladi, demak taxmin qolmaydi; mavjud IT muhitiga nima qo'shilayotgani ko'rinadi; texnik va notexnik odam birga ishlatadigan boshlanish nuqtasi paydo bo'ladi; tizimlar orasidagi interfeysni tushunish uchun kim bilan gaplashish kerakligi ma'lum bo'ladi. Uni chizish ikki daqiqada bo'ladi, shuning uchun chizmaslikka bahona yo'q (36-bob, 103-bet).

Quyidagi misol buyurtma platformasi uchun. Diagramma matni korpusning namunasi, kitobdagi rasm emas: Brown ning misoli financial risk system va techtribes.je.

```text
Kontekst diagrammasi: Buyurtma platformasi

  [Xaridor]                         [Omborchi]            [Qo'llab-quvvatlash operatori]
      |                                 |                             |
      | buyurtma beradi,                | yig'ish ro'yxatini          | buyurtmani qidiradi,
      | holatini kuzatadi               | oladi va yopadi            | bekor qiladi
      v                                 v                             v
  +---------------------------------------------------------------------------+
  |                        BUYURTMA PLATFORMASI                               |
  |      buyurtmani qabul qiladi, to'lovni boshlaydi, holatni yuritadi        |
  +---------------------------------------------------------------------------+
      |                        |                       |                 |
      | to'lovni avtorizatsiya | yetkazib berish       | hisob-faktura   | identifikatsiya
      | qiladi (HTTPS/REST)    | buyurtmasi (HTTPS)    | (fayl, SFTP)    | (OIDC)
      v                        v                       v                 v
  [To'lov provayderi]   [Logistika hamkori]      [Buxgalteriya tizimi]  [Keycloak]

Legend: to'rtburchak - tizim; kvadrat qavs - tashqi aktyor yoki tashqi tizim;
strelka - bog'liqlik yo'nalishi (chaqiruvchidan chaqirilganga);
chiziq yozuvi - o'zaro ta'sirning maqsadi va protokoli.
```

Kontekst diagrammasidagi aktyorlar ro'yxati [kim foydalanadi](02-muammoni-tushunish-va-togri-savol-berish.md#27-kim-foydalanadi-tashqi-foydalanuvchi-ichki-jamoa-boshqa-servis) bo'limidagi iste'molchi ro'yxatidan chiqadi: o'sha ro'yxat tayyor bo'lsa, diagramma uni rasm qilib ko'rsatadi. C4 kontekst diagrammasini DDD dagi [kontekst xaritasi](../patterns/13-domain-driven-design-patternlari.md#133-kontekst-xaritasi-context-map) bilan aralashtirmang: xarita bitta tizim ichidagi bounded context lar va jamoalar orasidagi munosabat turini ko'rsatadi, kontekst diagrammasi esa bitta tizimning tashqi dunyo bilan chegarasini.

## 3.14 Konteyner diagrammasi: alohida deploy qilinadigan birliklar

Kontekst diagrammasi tizimni bitta quti qilib ko'rsatadi, konteyner diagrammasi shu qutini ochadi. U besh savolga javob beradi: tizimning umumiy shakli qanday, yuqori darajadagi texnologiya qarorlari nima, javobgarlik qanday taqsimlangan, konteynerlar bir-biri bilan qanday muloqot qiladi, va dasturchi sifatida men funksiyani qaysi joyga yozishim kerak (Simon Brown, *Software Architecture for Developers*, Leanpub, 37-bob, 106-bet).

Brown konteyner deganda tizimni tashkil qiladigan mantiqiy bajariladigan birlik yoki processni tushunadi: web server, ilova serveri, SQL va NoSQL baza, fayl tizimi, `public static void main` uslubidagi mustaqil ilova, web brauzer, cron va shunga o'xshash rejalashtiruvchi (37-bob, 107-bet). Har konteyner uchun uch narsa yoziladi: nom, texnologiya va javobgarlikning juda yuqori darajali bayoni. Brown konteyner ichidagi komponentlarni ko'rsatish mumkin, lekin odatda bu diagrammani tirband qilib qo'yadi, deb ogohlantiradi (107-bet).

Quti diagrammaga tushadimi yoki yo'qmi degan savolga Brown bitta sinov beradi: o'zingizdan so'rang, bu quti alohida fizik yoki virtual apparatga deploy qilinadimi yoki qilinishi mumkinmi. Konteyner diagrammasida ko'rsatilgan har narsa alohida deploy qilinishi kerak. Bu ularni alohida infratuzilmaga qo'yish shart degani emas, qo'yish imkoni borligi yetarli (37-bob, 107-bet).

Chiziqlar bu yerda processlar orasidagi muloqot. Brown qo'shishni tavsiya qiladigan ma'lumot: o'zaro ta'sirning maqsadi ("ma'lumot o'qiydi va yozadi", "hisobot yuboradi"), muloqot usuli, muloqot uslubi (sinxron, asinxron, batch) va protokol bilan port (37-bob, 107-108-betlar). Agar diagrammaga tashqi foydalanuvchi va tizimlarni ham qo'ygan bo'lsangiz, o'z konteynerlaringiz atrofiga quti chizib tizim chegarasini ochiq ajratib qo'ying: shu chegara kontekst diagrammasidagi bitta qutiga to'g'ri keladi (108-bet).

```text
Konteyner diagrammasi: Buyurtma platformasi (tizim chegarasi ichida)

  [Xaridor]                                   [Omborchi]
      | HTTPS                                     | HTTPS
      v                                           v
  +=============================================================================+
  |  +----------------------------+        +-----------------------------+       |
  |  | order-api                  |  REST  | warehouse-ui                |       |
  |  | Spring Boot 3, embedded    |<-------| Spring Boot 3 + Thymeleaf   |       |
  |  | Tomcat, port 8080          |  HTTPS |                             |       |
  |  | buyurtmani qabul qiladi,   |        | yig'ish ro'yxatini beradi   |       |
  |  | holat o'zgarishini e'lon   |        +-----------------------------+       |
  |  | qiladi                     |                                             |
  |  +----------------------------+                                             |
  |     |  JDBC          |  produce           |  RESP                           |
  |     |  (HikariCP)    |  (order.events)    |  (Lettuce)                      |
  |     v                v                    v                                 |
  |  +------------+  +------------------+  +---------------+                     |
  |  | PostgreSQL |  | Kafka            |  | Redis         |                     |
  |  | 16, buyurt-|  | 3 partition,     |  | katalog keshi |                     |
  |  | ma va out- |  | order.events     |  | va idempoten- |                     |
  |  | box jadvali|  | topic            |  | tlik kaliti   |                     |
  |  +------------+  +------------------+  +---------------+                     |
  |                         ^ consume (order-notifier, Spring Boot, cron emas)   |
  +=============================================================================+

Legend: qo'sh chiziqli quti - tizim chegarasi; ichkaridagi har quti alohida
deploy qilinadigan konteyner; chiziq yozuvi - protokol va maqsad.
```

Konteyner diagrammasi nusxa soni haqida hech narsa aytmaydi. Brown web server fermasi yoki klaster bu diagrammada ko'rinmasligini, fizik nusxa, failover va klasterlash alohida deployment diagrammasida turishini aniq yozadi (37-bob, 110-bet). Korpusda deploy tomoni [konteyner va cgroup](31-deployment-haqiqati-konteyner-cgroup-jvm-va.md#311-konteyner-nima-va-nima-emas) bobida ko'rilgan; diqqat qiling, C4 dagi "konteyner" Docker konteyneri degani emas, u Brown ning atamasi va bazani ham qamraydi.

## 3.15 Komponent diagrammasi va nega kod darajasiga tushmaslik kerak

Konteyner diagrammasidan keyin har konteynerni ichkaridan ochish navbati keladi. Komponent diagrammasi uch savolga javob beradi: tizim qanday komponentlardan tashkil topgan, tizim yuqori darajada qanday ishlashi tushunarlimi, va har komponentning uyi bormi, ya'ni u qaysi konteynerda yashaydi (Simon Brown, *Software Architecture for Developers*, Leanpub, 38-bob, 111-bet). Brown bitta muhim cheklov qo'yadi: komponent diagrammasi odatda faqat bitta konteyner ichidagi komponentlarni ko'rsatadi. Bu qat'iy qoida emas, kichik tizimda hammasini bitta diagrammaga sig'dirish mumkin, lekin tirband bo'lsa bo'lish vaqti keldi (112-bet).

Komponent nima degan savolga javob 41-bobda: komponent interfeys ortidagi bog'liq xatti-harakatlar to'plami, u bir yoki bir nechta hamkorlik qiladigan sinf bilan amalga oshiriladi. Yaxshi komponent yaxshi sinf bilan bir xil xususiyatga ega: yuqori kogeziya, past bog'liqlik, aniq belgilangan ochiq interfeys va yaxshi enkapsulyatsiya (41-bob, 122-bet). Har komponent uchun diagrammada nom, texnologiya va javobgarlikning qisqa bayoni yoziladi (38-bob, 112-bet).

Nega sinf darajasiga tushmaslik kerak. Brown ning javobi: komponent darajasida ishlash sinf va koddan bir pog'ona yuqoridagi dizayn, va u tizimning ichki tuzilishini, qayerda qayta ishlatish imkoni borligini, komponentlar orasida va komponent bilan konteyner orasida qanday bog'liqlik borligini ko'rish uchun eng qulay daraja. Bu darajada dizayn haftalar emas, bir necha soat yoki kun ishi, va u sinf darajasidagi ishga umumiy tuzilish haqida qayg'urmasdan o'tishga tayyorlab qo'yadi (38-bob, 113-bet). Shu bilan birga bu to'liqlikni tekshirish usuli ham: har use case ni bir yoki bir nechta komponent orqali kuzatib chiqa olish kerak, va masalan audit talabi bo'lib audit komponenti yoki javobgarligi yo'q bo'lsa, demak nimadir o'tkazib yuborilgan (112-113-betlar).

Spring da komponent chegarasi paket bilan beriladi va ichki sinflar paket darajasida yopiladi. Quyidagi misolda bitta komponent (`pricing`) ichida Spring stereotiplari turadi, tashqariga faqat interfeys chiqadi.

```java
// src/main/java/com/shop/order/pricing/PricingFacade.java
package com.shop.order.pricing;

// Komponentning ochiq shartnomasi: diagrammadagi "Pricing" qutisi shu.
public interface PricingFacade {
    Money quote(OrderDraft draft);
}

// src/main/java/com/shop/order/pricing/PricingService.java
package com.shop.order.pricing;

import org.springframework.stereotype.Service;

@Service
class PricingService implements PricingFacade {   // paket darajasida: tashqaridan ko'rinmaydi

    private final DiscountRepository discounts;   // @Repository, ham paket darajasida

    PricingService(DiscountRepository discounts) {
        this.discounts = discounts;
    }

    @Override
    public Money quote(OrderDraft draft) {
        return discounts.findActive(draft.customerId())
                .map(discount -> discount.applyTo(draft.subtotal()))
                .orElseGet(draft::subtotal);
    }
}
```

Shu shakl kod tashkil etishning paket bo'yicha emas, komponent bo'yicha variantini bildiradi; tanlovning afzalligi va narxi [feature bo'yicha vs qatlam bo'yicha paketlash](../patterns/12-arxitektura-uslublari.md#1228-feature-boyicha-vs-qatlam-boyicha-paketlash-package-by-feature-vs-package-by-layer) yozuvida, uslubning o'zi esa [komponentga asoslangan arxitektura](../patterns/12-arxitektura-uslublari.md#1230-komponentga-asoslangan-arxitektura-component-based-architecture) yozuvida ko'rilgan.

Ikki tipik savolga Brown ning javobi bor. Umumiy komponent (masalan ikki konteyner ishlatadigan baza kirish qatlami) har mos komponent diagrammasida chiziladi va "bu umumiy komponent" degan izoh bilan belgilanadi. Utility komponent (masalan hamma ishlatadigan logging) uchun ikki variant bor va biri aniq toza: uni markazga qo'yib hamma komponentdan chiziq tortish to'g'ri, lekin diagrammani tez tirband qiladi; uni chetga qo'yib "bu hamma komponent ishlatadigan utility komponent" deb izohlash ma'qul (44-bob, 137-138-betlar).

## 3.16 "Kodda shunday qilasizmi" sinovi va model bilan kod orasidagi uzilish

Diagramma qanday chizilishi kerakligi haqidagi ko'p savolga Brown bitta savol bilan javob beradi: kodda ham shunday qilasizmi. Mashg'ulotdagi tipik dialog shunday ketadi. Savol: logging komponentini web server va ilova serveridan tashqariga chizaylikmi, ikkisi ham ishlatadi. Brown ning javobi: kodda shunday qilasizmi, u chindan ham alohida process bo'lib ikkisidan tashqarida ishlaydimi. Javob yo'q bo'lsa va u ikki serverga deploy qilinadigan umumiy JAR bo'lsa, diagrammada ham shunday chiziladi: har server ichida logging komponenti turadi va u annotatsiya bilan umumiy komponent deb belgilanadi (Simon Brown, *Software Architecture for Developers*, Leanpub, 40-bob, 120-bet).

Ikkinchi dialog qatlamlar haqida. Savol: UI dan bazaga hamma murojaat servis qatlami orqali o'tishini ko'rsataylikmi. Brown ning javobi yana bir xil: siz uni shunday amalga oshirasizmi yoki UI bazaga to'g'ridan-to'g'ri boradimi. Agar jamoa CQRS ni mo'ljallayotgan bo'lsa va UI servis qatlamini chetlab o'tib data access ni ishlatsa, diagramma aynan shunday chiziladi, UI dan ikki chiziq bilan, va chiziqlar niyat va sabab bilan annotatsiya qilinadi (40-bob, 120-121-betlar).

Qoida umumiy: diagramma haqiqatni aks ettiradigan abstraksiya berishi kerak, mavjud bo'lmagan konseptual tasvir emas. Diagramma elementlarining kod bazasida qanday aks etganini va teskarisini ko'rish imkoni bo'lishi kerak. Allaqachon qurilgan tizimni retrospektiv chizayotgan bo'lsangiz, savol "biz uni shunday kodladikmi" ga aylanadi, printsip esa o'zgarmaydi (40-bob, 121-bet).

Bu sinov kerak bo'lishining sababi Brown da ochiq aytilgan: biz komponent haqida gaplashamiz, lekin sinf yozamiz. Odamlar tizimni komponent sifatida muhokama qiladi, lekin bu tuzilish kodda aks etmaydi, va shu yerdan arxitektura bilan kod orasidagi uzilish chiqadi: devordagi diagramma bir narsa, kod boshqa narsa aytadi. George Fairbanks buni o'z kitobida "model-code gap" deb nomlaydi (41-bob, 123-124-betlar). Sababi ko'pincha paketlash uslubi: qatlam bo'yicha paketlashda diagrammadagi bitta komponent bir necha paketga sochilib ketadi, va pastki qatlam sinflari ochiq ko'rinishda bo'lgani uchun istalgan joydan chaqirilishi mumkin (41-bob, 124-125-betlar). Brown ning xulosasi qisqa: agar tizim tuzilishini tushuntirish qiyin bo'lsa, tuzilishni o'zgartiring (41-bob, 127-bet).

Diagramma bilan kodning mos kelishini odamning diqqatiga tashlab qo'ymang. Bu moslikni avtomatik tekshirish korpusning tanlovi, kitobda bunday vosita yo'q: Brown 2014 da bu ishni qo'lda ko'rib chiqish deb qoldiradi. Java da chegarani [ArchUnit asoslari](../testing/14-arxitektura-testlari-va-kod-sifati.md#142-archunit-asoslari) bobidagi test sifatida yozib qo'yish mumkin, va shunda diagrammadagi strelka yo'nalishi CI da qo'riqlanadi.

```java
// Diagrammadagi da'vo: order-api konteynerida pricing komponenti
// checkout komponentini CHAQIRMAYDI, faqat teskarisi.
@AnalyzeClasses(packages = "com.shop.order", importOptions = DoNotIncludeTests.class)
class KomponentChegarasiTest {

    @ArchTest
    static final ArchRule pricing_checkoutga_bogliq_emas =
            noClasses().that().resideInAPackage("..order.pricing..")
                    .should().dependOnClassesThat().resideInAPackage("..order.checkout..");

    // Komponent ichki sinflari tashqariga chiqmasin: diagrammadagi quti
    // haqiqatan ham interfeys ortida yopilgan bo'lsin.
    @ArchTest
    static final ArchRule faqat_fasad_ochiq =
            classes().that().resideInAPackage("..order.pricing..")
                    .and().areNotInterfaces()
                    .should().notBePublic();
}
```

## 3.17 Samarali eskiz: sarlavha, legend, javobgarlik va strelka

UML dan voz kechib qutilar va chiziqlarga o'tgan jamoa izchillikni moslashuvchanlikka almashtiradi, va natijada diagramma elementlari bir xil ishlatilmaydi hamda rasm yonida og'zaki bayon kerak bo'lib qoladi. Brown "NoUML" diagramma chizadiganlar uchun aniq ro'yxat beradi (Simon Brown, *Software Architecture for Developers*, Leanpub, 43-bob, 131-bet).

Sarlavha. Diagrammada sarlavha bo'lishi birinchi yordam beradigan narsa: qisqa va ma'noli bo'lsin, diagrammalar ma'lum tartibda o'qilishi kerak bo'lsa raqamlab qo'yiladi (131-bet). Yorliqlar. Qisqartmadan saqlaning, kerak bo'lsa ularni loyiha glossariysida yoki diagrammadagi legendda yozib qo'ying; sanoatda keng ishlatiladigan texnologiya qisqartmalari (JMS, POJO) bundan mustasno, lekin shubha bo'lsa to'liq nom yozing (131-bet). Shakllar. Ko'pchilik silindrni baza deb o'qiydi, lekin shu taxmin to'g'rimi yoki yo'qmi, diagrammaning o'zi tasdiqlashi kerak (131-bet).

Javobgarlik. Faqat nom yozilgan qutilar bilan to'ldirilgan diagramma vasvasasiga berilmang: tizim va komponentga javobgarlikning juda qisqa bayonini qo'shish noaniqlikni olib tashlaydi. Brown shakl beradi: etti qo'shuv-ayirish ikki banddan oshmaydigan ro'yxat yoki bitta qisqa gap, kichik shriftda (43-bob, 132-bet).

Chiziqlar. Brown chiziqlarni diagrammaning eng e'tiborsiz qolgan qismi deb hisoblaydi: ular qutilarni ushlab turadi, lekin o'zlariga diqqat qaratilmaydi. Ikki savolga javob kerak: chiziq uslubi (uzluksiz, nuqtali, chizikli) ahamiyatlimi va nimani bildiradi; strelkalar bog'liqlik yo'nalishini ko'rsatadimi yoki ma'lumot oqimi yo'nalishini. Chiziqqa yozilgan izoh ("ishlatadi", "ma'lumot yuboradi", "hisobotni yuklab oladi") ko'pincha shu noaniqlikni yopadi, lekin ikki tomoni ham strelkali chiziqdan ehtiyot bo'lish kerak (43-bob, 132-133-betlar). Rang, chegara, joylashuv va yo'nalish uchun ham bir xil talab: rang kodi legendda bo'lsin, element atrofidagi chegara nimani bildirishi yozilsin; "to'g'ri" yo'nalish yo'q, lekin odatdagidan teskari chizilgan diagramma yoki chalkashtiradi yoki ataylab ishlaydi (133-135-betlar).

Legend hammasini bog'laydi. Brown legendga shakl, chiziq, rang, chegara va qisqartmalarning izohi tushishini aytadi, va ko'rinib turgan narsa ham boshqa tajribaga ega odam tomonidan boshqacha o'qilishi mumkinligi uchun legendni qo'shishni tavsiya qiladi (43-bob, 135-bet). Oxirgi maslahat amaliy: diagramma chizilayotganda berilgan savollarga quloq soling, agar o'zingiz "aniqlik uchun aytaman, bu strelkalar ma'lumot oqimi" deb tushuntirayotgan bo'lsangiz, shu ma'lumot legendda turishi kerak (136-bet).

```text
Legend (har diagrammaga qo'yiladigan minimal to'plam)

  To'rtburchak           deploy qilinadigan konteyner (nom + texnologiya + javobgarlik)
  Yumaloq burchakli quti mantiqiy komponent (interfeys ortidagi xatti-harakat to'plami)
  Kvadrat qavs [ ]       tizim chegarasidan tashqaridagi aktyor yoki tizim
  Qo'sh chiziqli quti    tizim chegarasi (kontekst diagrammasidagi bitta qutiga teng)
  Uzluksiz strelka       sinxron chaqiruv; yo'nalish: chaqiruvchidan chaqirilganga
  Nuqtali strelka        asinxron hodisa; yo'nalish: chiqaruvchidan iste'molchiga
  Kulrang to'ldirish     mavjud tizim, bu ishda o'zgarmaydi
  Qisqartmalar           OIDC - OpenID Connect; DLQ - dead letter queue
```

Brown bobni diagrammani review qilish ro'yxati bilan yopadi va u to'qqiz banddan iborat: yechimni bir necha abstraksiya darajasida ko'ra olaman va tushunaman; katta manzarani tushunaman, kim ishlatishini va mavjud IT muhitiga qanday bog'liqlik borligini bilaman; mantiqiy konteynerlarni va yuqori darajali texnologiya tanlovini tushunaman; asosiy komponentlar nima va ular muhim use case larni qanday qoplaydi, buni tushunaman; barcha komponentning nima qilishini va har birining uyi borligini ko'raman; notatsiya, konvensiya va rang kodini tushunaman; diagrammalar orasidagi izchillikni ko'raman va elementlar bir xil ishlatilgan; biznes domen nimaligini tushunaman; amalga oshirish strategiyasini (framework, kutubxona, API) tushunaman va tizim qanday qurilishini deyarli tasavvur qila olaman (43-bob, 135-136-betlar). Bu ro'yxat ham yangi dizayn uchun, ham mavjud tizimni retrospektiv hujjatlash uchun ishlaydi. Diagrammani review ga qo'yish tartibi [arxitektura qarorlarini jamoaga tarqatish](36-code-review-va-jamoada-texnik-yetakchilik.md#368-arxitektura-qarorlarini-jamoaga-tarqatish-hujjat-ichki-suhbat-namuna-kod) bo'limidagi yo'l bilan bir xil: diagramma pull request ichidagi fayl bo'lsa, u review ga tushadi.

*Fundamentals of Software Architecture* 21-bobi bu mavzuda yana uch nomni beradi: "irrational artifact attachment", komponentlar orasidagi nuqtali chiziqning ma'nosi va taqdimotdagi "bullet-riddled corpse" antipatterni. Korpusdagi nusxada shu bobning tanasi yo'q, faqat ilovadagi savollar bu nomlarni tasdiqlaydi, shuning uchun bu yerda ularning tavsifi berilmaydi: nomlari sanaladi va tavsif uchun asl 21-bobga murojaat qilish kerak (Mark Richards, Neal Ford, *Fundamentals of Software Architecture*, ilova "Self-Assessment Questions", 21-bob savollari).

## 3.18 Arxitektura ko'rinishi (view) va uni hujjatlashtirish qoidalari

C4 bitta yondashuv, lekin arxitektura hujjatlashning umumiy apparati "ko'rinish" (view) tushunchasi ustida qurilgan. *Documenting Software Architectures* uni eng muhim tushuncha deb ataydi va ta'rifni qisqa beradi: ko'rinish bu tizim elementlarining bir to'plami va ular bilan bog'liq munosabatlarning tasviri (Paul Clements va boshqalar, *Documenting Software Architectures: Views and Beyond*, 2-nashr, Addison-Wesley, 2010, Prolog, P.3, 22-bet). Kitobning analogiyasi qush qanoti: patlar, skelet, qon aylanishi, mushaklar ko'rinishlari bor, va qaysi biri qanotning arxitekturasi degan savolga javob hech biri, qaysilari arxitekturani yetkazadi degan savolga javob esa hammasi (22-bet).

Shundan kitobning asosiy printsipi chiqadi: arxitekturani hujjatlashtirish bu tegishli ko'rinishlarni hujjatlashtirish va ustiga bir nechta ko'rinishga tegishli hujjatni qo'shish (P.3, 22-bet). Qaysi ko'rinish tegishli ekani maqsadga bog'liq. Kitob buni sifat atributlari bilan bog'laydi: har ko'rinish turli sifat atributini turli darajada ochadi, qatlamli ko'rinish portativlik haqida gapiradi, deployment ko'rinishi esa unum va ishonchlilik haqida mulohaza yuritishga imkon beradi (22-bet). Bitta ko'rinish arxitekturani to'liq ifodalay olmaydi, va bu kamchilik emas: arxitekturaning mohiyati hozirgi vazifaga kerak bo'lmagan ma'lumotni bosib turish, shuning uchun har ko'rinish ba'zi tomonlarni ta'kidlab, boshqalarini e'tibordan chetga suradi (23-bet).

Eng amaliy qism bu ko'rinishni hujjatlashtirish tarkibi. Kitob bitta ko'rinish hujjatiga besh element qo'yadi: birlamchi taqdimot (odatda grafik, ko'rinishning asosiy elementlari va munosabatlarini ko'rsatadi); element katalogi (diagrammada ko'rsatilgan elementlarni tushuntiradi, ta'riflaydi va ularning xususiyatlarini sanaydi); elementlarning interfeysi va xatti-harakatining spetsifikatsiyasi; variativlik qo'llanmasi (arxitekturani moslashtirish uchun qurilgan mexanizmlar); sabab va dizayn ma'lumoti (P.3, 23-bet). Barcha ko'rinishga tegishli hujjat esa to'rt narsani o'z ichiga oladi: butun to'plamga kirish va o'quvchi qo'llanmasi; ko'rinishlar bir-biri bilan va tizim bilan qanday bog'liqligi; umumiy arxitektura uchun cheklovlar va sabab; to'plamni yuritish uchun kerakli boshqaruv ma'lumoti (23-bet).

Ko'rinish, uslub (style) va ko'rinish turi aralashtirilmasin. Kitobda uslub elementlar va munosabat turlarining ixtisoslashishi hamda ularni qanday ishlatish mumkinligi haqidagi cheklovlar to'plami (P.4, 25-bet), va uslubni tizimga qo'llaganda natija ko'rinish bo'ladi. Kitob uslublarni uch kategoriyaga ajratadi, chunki arxitektor dasturi haqida bir vaqtda uch xil o'ylashi kerak: u amalga oshirish birliklari to'plami sifatida qanday tuzilgan, runtime da xatti-harakat va o'zaro ta'siri bor elementlar to'plami sifatida qanday tuzilgan, va atrof-muhitdagi dastur bo'lmagan tuzilmalar bilan qanday bog'langan (P.4.1, 29-bet).

| Kategoriya | Nimani hujjatlashtiradi | Java va Spring da nima bo'ladi |
|---|---|---|
| Module styles | Tizimning asosiy amalga oshirish birliklari | Maven yoki Gradle modul, Java paket, Spring Modulith moduli |
| Component-and-connector (C&C) styles | Tizimning bajarilish birliklari | Bean, ishga tushgan Spring Boot process, Kafka consumer group, ulanish: REST, topic |
| Allocation styles | Dastur bilan dastur bo'lmagan resurs orasidagi munosabat | Pod va node, jamoa egaligi (`docs/OWNERS.tsv` kabi), CI muhiti |

Modul bilan komponentni farqlash shu uch kategoriyaning asosi. Kitob modulni avvalo amalga oshirish birligi deb ta'riflaydi (Parnas da javobgarlikni modulga berish mezoni information hiding), komponentni esa runtime birligi deb ta'riflaydi va Szyperski ning ta'rifini keltiradi: komponent mustaqil deploy qilinishi mumkin va uchinchi taraf uni kompozitsiyaga kirita oladi (P.4.1, 29-30-betlar). Shu farq C4 da ham ko'rinadi: Brown ning "komponent" i interfeys ortidagi mantiqiy guruh, ya'ni Clements ma'nosida modulga yaqinroq, "konteyner" i esa bajarilish birligi. Diqqat qiling, ikki kitob bir xil so'zni boshqacha ishlatadi, va hujjatda qaysi ma'noda ishlatayotganingizni aytib qo'yish kerak.

Brown bu terminologiyadan ogohlantiradi: IEEE 1471, ISO/IEC/IEEE 42010 va Kruchten ning 4+1 modeli ko'rinishlar beradi, lekin atamaga ko'nikmagan odam uchun "konseptual ko'rinish" bilan "mantiqiy ko'rinish" farqi haqidagi tortishuv tez boshlanadi. Uning maslahati: nimani yetkazayotganingizni aniq bilib, bo'limni shunga mos nomlang (Simon Brown, *Software Architecture for Developers*, Leanpub, 47-bob, 147-148-betlar).

## 3.19 Software guidebook: kod aytmagan narsani yozish

Kod hamma narsani aytmaydi. Brown yangi loyihaga kelgan dasturchining holatidan boshlaydi: kod bazasini ochib, paket va papka tuzilishidan, nom konvensiyasidan arxitektura haqida bir narsa chiqarish mumkin, lekin bir qancha savol javobsiz qoladi. Uning ro'yxati: tizim mavjud tizim manzarasiga qanday joylashadi; nega aynan shu texnologiya tanlangan; tizimning umumiy tuzilishi qanday; komponentlar runtime da qayerda deploy qilinadi va qanday muloqot qiladi; logging, konfiguratsiya va xatolarni qayta ishlashga qanday yondashilgan va u kod bo'ylab izchilmi; kod bazasida qanday pattern va printsiplar ishlatiladi; yangi funksiyani qayerga va qanday qo'shiladi; xavfsizlik stack bo'ylab qanday amalga oshirilgan; masshtablanish qanday erishiladi; boshqa tizimlar bilan interfeys qanday ishlaydi (Simon Brown, *Software Architecture for Developers*, Leanpub, 46-bob, 142-bet). Javobni koddan ham topish mumkin, lekin bu og'ir ish, va to'g'ri savol bermasa to'g'ri javob chiqmaydi: nimani bilmasligingizni bilmaysiz (142-bet).

Brown yechimni shabloni bilan beradi va metafora tanlaydi: qo'shimcha hujjat 1990-yillardagi arxitektura hujjati shabloni emas, o'zgarib turadigan sayohat qo'llanmasi (guidebook) bo'lishi kerak (47-bob, 144-bet). Qo'llanmaning to'rt qismi: xaritalar (turli abstraksiya darajasidagi kichik sondagi sodda diagramma, kod bazasida yurish uchun), diqqatga sazovor joylar (hamma narsani emas, qiziqish nuqtalarini sanash: web sahifa patterni, ma'lumotga kirish strategiyasi, xavfsizlik va masshtablanish), tarix va madaniyat (nega tizim shunday ekanini tushuntiradigan sabab, yangi odam uchun ayniqsa qimmatli), va amaliy ma'lumot (kod qayerda, qanday build qilinadi, qanday deploy qilinadi, jamoa qanday printsiplarga amal qiladi) (145-147-betlar).

Brown qo'llanmaga o'n uch bo'lim taklif qiladi: Context, Functional Overview, Quality Attributes, Constraints, Principles, Software Architecture, External Interfaces, Code, Data, Infrastructure Architecture, Deployment, Operation and Support, Decision Log (47-bob, 147-bet). Uchtasi majburiy va Brown har biri uchun "Required: Yes" deb yozadi. Context sahnani qo'yadi, bir-ikki bet yetarli va kontekst diagrammasi hikoyaning ko'p qismini aytib beradi (48-bob, 149-bet). Functional Overview tizim nima qilishini xulosalaydi va qaysi funksiya, use case yoki rol arxitektura uchun ahamiyatli ekanini hamda nega ahamiyatli ekanini ochiq bog'laydi (49-bob, 150-bet). Software Architecture bo'limi "katta manzara": Brown unda konteyner va komponent diagrammalarini asosiy fokus qilib qo'yadi, yoniga qisqa bayon va har konteyner bilan komponentning xulosasini yozadi (53-bob, 158-bet).

Qo'llanma mahsulot haqida, loyiha haqida emas. Brown yigirma yillik tizimlarni ko'rgan: ularda loyiha darajasidagi hujjat bor, lekin mahsulot qanday ishlashi va qanday evolyutsiya qilgani haqida hech narsa yo'q. Uning tavsiyasi: har tizim uchun bitta software guidebook, va keyin har loyiha yoki o'zgarish oqimi shu qo'llanmaga kichik delta bo'ladi (47-bob, 148-bet). Hujjat yangilanib turishi sharti [ADR ni repoda saqlash](#38-adr-ni-repoda-saqlash-raqamlash-va-eskirganini-belgilash) bo'limida "Rule 6" bilan birga ko'rilgan.

Korpusda qo'llanmaning aksar bo'limi uchun to'liq yozuv allaqachon bor, shuning uchun quyidagi daraxt faqat joylashuvni ko'rsatadi: bu korpusning tanlovi, kitobda papka tuzilishi yo'q.

```text
docs/
  guidebook/
    01-context.md               kontekst diagrammasi + aktyorlar ro'yxati
    02-functional-overview.md   kalit funksiya va arxitektura uchun ahamiyatlilari
    03-quality-attributes.md    -> architect 1.4 sifat atributlari va ularni o'lchash
    04-constraints.md           -> architect 1.2 kontekst va cheklovlar
    05-principles.md            -> patterns 26 dizayn printsiplari
    06-software-architecture.md konteyner + komponent diagrammasi, har qutining xulosasi
    07-external-interfaces.md   -> architect 32 tarmoq va integratsiya haqiqati
    08-code.md                  pattern va framework ishlatilishi
    09-data.md                  -> architect 25 sxema dizayni; migratsiya: architect 33
    10-infrastructure.md        -> architect 31 konteyner va cgroup
    11-deployment.md            -> architect 31, 33 reliz va migratsiya
    12-operation-support.md     -> architect 30 kuzatuvchanlik, 35 on-call
  adr/
    0001-...md                  -> Decision Log: 3.1 va 3.8 shu bo'limning o'rnini bosadi
```

Qo'llanma va ADR orasida bitta tirqish qoladi: bir nechta modulga tarqalgan, lekin ADR uchun juda kichik qaror. Ousterhout muammoni aynan shu joyda qo'yadi: ideal holda har bir muhim dizayn qarori bitta sinf ichida yashiringan bo'lardi, lekin haqiqiy tizimda bir nechta sinfga tegadigan qarorlar bo'lmasligi mumkin emas (tarmoq protokolining dizayni jo'natuvchiga ham, qabul qiluvchiga ham tegadi), bunday qarorlar esa murakkab, nozik va ko'p xatoning manbasi. Qiyinligi hujjatning mazmunida emas, joyida: dasturchi uni tabiiy ravishda topadigan joy kerak (Ousterhout, *A Philosophy of Software Design*, 1-nashr, Yaknyam Press, 2018, 13.7).

Ousterhout ikki holatni ajratadi. Agar aniq markaziy joy bo'lsa, hujjat shu yerga qo'yiladi: uning misolida yangi xato holati qo'shish bir nechta faylga tegadi, lekin dasturchi albatta `Status` sanog'ini ochadi, shuning uchun qolgan hamma joyni sanab chiqadigan izoh aynan shu sanoqqa, yangi qiymatlar qo'shiladigan oxirgi qatorga yozilgan (13.7). Agar aniq markaziy joy bo'lmasa (uning misolida bir nechta modulga tarqalgan va bir-biriga bog'liq "zombi server" mantig'i), u markaziy `designNotes` faylini sinab ko'rganini aytadi: fayl aniq nomlangan bo'limlarga bo'linadi, har bo'lim bitta mavzuni oladi, kodda esa qisqa ishora qoladi (13.7). Shu yondashuvni u izohni takrorlashdan qochish qoidasida ham qaytaradi: hujjat uchun aniq bitta joy bo'lmasa, `designNotes` fayli yaratiladi, aks holda mavjud joylarning eng yaxshisi tanlanadi va qolgan joylarda markaziy izohga havola yoziladi (16.4).

Ousterhout bu usulning narxini o'zi aytadi: hujjatning bitta nusxasi bo'ladi va uni topish oson, lekin u o'ziga bog'liq kodning yonida turmaydi, shuning uchun tizim rivojlanganda uni yangilab turish qiyin bo'lishi mumkin (13.7). Shu sababli korpusdagi tartib shunday: chegara yoki texnologiya tanlovi darajasidagi qaror ADR ga, mahsulot darajasidagi bayon guidebook ga, bir nechta moduldagi kodni bir vaqtda o'zgartirishni talab qiladigan mayda qaror esa `designNotes` ga tushadi va kodda unga ishora qoladi.

Quyidagi misol kitobdagi g'oyani Java ga o'tkazadi, kitobda u boshqa tilda berilgan: ro'yxatga yangi qiymat qo'shadigan odam ko'radigan joyga tekshiruv punktlari yoziladi.

```java
public enum PaymentStatus {

    PENDING,
    AUTHORIZED,
    CAPTURED,
    REFUNDED;

    // DIQQAT: yangi holat qo'shilsa, quyidagilar ham o'zgaradi.
    // (1) PaymentStatusMessages: foydalanuvchiga ko'rinadigan matn.
    // (2) PaymentStateMachine.ALLOWED: ruxsat etilgan o'tishlar jadvali.
    // (3) V12__payment_status_check.sql: bazadagi CHECK cheklovi.
    // (4) PaymentStatusDto: tashqi API nomi (eski nomlar o'zgarmaydi).
    // Kesib o'tuvchi qarorning bayoni: docs/designNotes.md, "To'lov holati".
}
```

Uzun yozishdan saqlaning. Brown ning o'z ogohlantirishi: juda chuqur texnik tafsilotga tushish vasvasasiga berilmang, chunki shu darajani tushunadigan texnik odam uni kod bazasidan o'zi topa oladi (47-bob, 147-bet).

## 3.20 RFC: dizayn hujjatini fikr yig'ish uchun tarqatish

ADR qabul qilingan qarorni yozib qo'yadi, RFC esa qaror hali chiqmaganda fikr yig'adi. Orosz farqni ochiq qo'yadi: arxitektura hujjatlari qabul qilingan qarorni qayd etish uchun yoziladi va ulardan fikr kutilmaydi, RFC esa aynan fikr olish uchun tarqatiladi (Gergely Orosz, *The Software Engineer's Guidebook*, 1-nashr, Pragmatic Engineer, 2023, 15-bob, 209-bet). RFC "Request for Comments" dan olingan va ko'p kompaniyada shunchaki dizayn hujjati ma'nosida ishlatiladi: muhandis jiddiy ish boshlashdan oldin kontekstni, taklif qilgan yondashuvini va trade-off larni yozib, izoh so'raydi; qat'iy shakl talabi yo'q (207-208-betlar).

Hujjatning asl maqsadi yozish emas, vaqt yutish: kalit fikrni erta olib, loyihani tugatish muddatini qisqartirish (208-bet). Shundan RFC ni ish oqimiga qo'yishning to'rt shakli chiqadi.

| Shakl | Qachon mos keladi | Orosz ning izohi |
|---|---|---|
| Prototip, keyin RFC, keyin qurish | Noma'lum ko'p, masalan yangi framework ustida qurilyapti | Prototip noma'lumlarni ochadi, RFC qisman to'ldirilgan rejani ulashadi |
| RFC, fikrni kutish, keyin qurish | Bog'liqlik ko'p yoki boshqa jamoalar natijaga bog'liq | Hamma manfaatdordan fikr oldin yig'ilsa, umumiy tezlik yuqoriroq bo'ladi |
| RFC, fikr kutilayotganda qurish | Murakkablik bor, lekin ko'p savol kutilmaydi | Fikrni yo'l-yo'lakay singdirish mumkin, o'zgarish kerak bo'lsa ham ko'p vaqt yo'qolmaydi |
| Avval qurish, keyin RFC | Ish allaqachon qilingan yoki ichki qoida talab qiladi | Xatarli: hujjat "katak belgilash" ga aylanadi va jamoa haqiqiy fikrni qabul qilmaydi; Orosz bu shakl amalda ancha keng tarqalganini aytadi |

Yozishning foydasi faqat o'quvchida emas. Orosz to'rt foydani sanaydi: fikringiz tiniqlashadi, chunki hujjat yondashuvingizni o'zingizga ham, boshqaga ham tushunarli qilib aytishga majbur qiladi; muhim fikr tezroq keladi, chunki yetishmagan chekka holat yoki noto'g'ri use case kod yozilgunga qadar aytiladi; g'oyangiz masshtablanadi, chunki hujjat bo'lmasa beshta muhandis sizning fikringizni tushunish uchun beshta alohida suhbat talab qiladi; va jamoada yozish madaniyati tarqaladi (208-209-betlar).

Fikr yig'ishning uch yo'li bor: hujjat ichidagi izohlar orqali asinxron, RFC ni muhokama qiladigan uchrashuv orqali sinxron, va aralash shakl, ya'ni hujjat tarqatiladi va murakkablik yoki izohlar soni talab qilsa uchrashuv chaqiriladi (209-bet). Shaklni loyiha tanlaydi: yigirma jamoaga tegadigan loyiha uchun kerakli yondashuv sizning jamoangiz va bitta hamkor jamoa ishlatadigan servis uchun keraklisidan boshqacha bo'ladi (209-bet).

Korpusdagi joyi oddiy: RFC qaror pishayotgan paytdagi hujjat, [ADR](#31-adr-architecture-decision-record-tuzilishi-kontekst-qaror-oqibat-holat) esa qaror chiqqandan keyingi yozuv. RFC muhokamasida aytilgan e'tiroz va rad etilgan variant ADR ning "Ko'rib chiqilgan variantlar" qismiga ko'chadi, shunda muhokama repoda qoladi va [eskirganini belgilash](#38-adr-ni-repoda-saqlash-raqamlash-va-eskirganini-belgilash) qoidasiga bo'ysunadi.

## 3.21 Muhokama tiqilib qolganda qarorni ochish yo'llari

Ba'zan muhokama sifatli, dalillar yozilgan, lekin guruh ikkiga bo'linib qoladi va qaror chiqmaydi. [Kelishmovchilik qoidasi](#36-jamoadagi-kelishmovchilik-va-rozi-emasman-lekin-bajaraman-qoidasi) e'tirozni shaklga soladi, bu bo'lim esa tiqilishni ochadi. Orosz besh usulni sanaydi (Gergely Orosz, *The Software Engineer's Guidebook*, 1-nashr, Pragmatic Engineer, 2023, 15-bob, 214-bet).

Birinchisi eng kuchlisi: imkoniyat talablarini (capability requirements) yozish. Bu talablar natijani belgilaydi, amalga oshirishni emas. Ular tizim darajasidagi cheklov bo'lishi mumkin, masalan kutilayotgan latency yoki qabul qilinadigan consistency darajasi; UX tomonidagi cheklov, masalan javob vaqti 500 ms dan oshmasligi; yoki biznes cheklovi, masalan ikki marta pul yechish mumkin emasligi. Ular yechimdan oldin yoziladi, shunda har bir taklif shu linza orqali tekshiriladi va "muammoni tushunmasdan yechim rejimiga o'tish" yo'qoladi (214-bet). Korpus tilida bu [sifat atributlari](01-arxitektorning-fikrlash-modeli.md#14-sifat-atributlari-va-ularni-olchash) ning qaror oldidan o'lchanadigan shaklga keltirilishi.

Qolgan to'rttasi tartib bo'yicha: qaror egasi muhokamadan oldin tayinlansin, chunki nizo paytida kiritilgan qaror egasi neytralligi haqidagi savolni ochadi va ishqalanish qo'shadi, ayniqsa ishtirokchi o'z menejerini olib kirsa; eng sodda va adolatli teng hisobni buzuvchi mezon kodni kim yozsa, chunki yechimni keyin u yuritadi; muhokama turib qolganda prototip qurilsin, shunda gap tiqilish haqida emas, ko'rinadigan narsa haqida boradi (prototipni vaqt bilan cheklash [3.5](#35-spike-va-prototip-qarorni-malumot-bilan-quvvatlash) da); va mahsulot tomonidagi hamkordan homiylik olinsin, chunki product manager ham qisqa muddatli yechimdan, ham uzoq muddatli yuritish narxidan manfaatdor (214-bet).

Oxirgi tayanch nuqtasi fikrlashda. Orosz ning qoidasi: dasturiy ta'minotda deyarli har bir qaror keyin qaytariladi, faqat qaytarish narxi har xil, shuning uchun qaytarilishi arzon qaror bo'yicha turib qolgandan ko'ra bittasini tanlab oldinga yurish yaxshiroq (215-bet). Shu yerda yana bitta amaliy talab bor: qarordan qaytilganda nega yondashuv ishlamaganini yozib, tegishli odamlarga tarqatish kerak (215-bet). Korpusda bu yozuv ADR ning `Superseded` holati va [qayta ko'rish](#37-qaror-oqibatini-kuzatish-metrika-va-qayta-korish-sanasi) qismiga tushadi.

## 3.22 Amalda qo'llash

- [ ] `docs/adr/` papkasini va `template.md` shablonini repoga qo'shing, raqamlash skriptini ishga tushiring.
- [ ] Yaqin o'tmishdagi eng katta qarorlarni retrospektiv ADR sifatida yozing va retrospektiv ekanini ochiq belgilang; tanlash mezoni "Rule 5" dan: qaror sifat talabiga erishish uchun kalit bo'lgan, uzoq muhokama talab qilgan yoki prototip bilan tekshirilgan bo'lsa, u yozishga arziydi.
- [ ] Har bir ochiq ADR ga qaror egasining ismini va qayta ko'rish sanasini qo'ying, egasiz ADR ni merge qilmang.
- [ ] CI ga ikki tekshiruv qo'shing: `Holat` qatori majburiy, muddati o'tgan qayta ko'rish sanalari ro'yxati haftalik chiqsin.
- [ ] Keyingi arxitektura qarori uchun variantlar ro'yxatini MECE qilib tekshiring (bir-birini qoplamasin, ochiq variant qolmasin), keyin trade-off jadvalini sifat darajalari bilan to'ldiring.
- [ ] Hozir muhokamada turgan bitta savolni spike ga aylantiring: savol, vaqt chegarasi va javob mezonini yozib qo'ying.
- [ ] Har bir qabul qilingan ADR uchun bitta Micrometer metrikasi va bitta alert chegarasini kod bilan birga joylashtiring.
- [ ] Jamoa bilan "rozi emasman, lekin bajaraman" qoidasini kelishib oling va rad etilgan e'tirozlarni ADR ichida saqlaydigan bo'lim qo'shing.

## Manbalar

- Neal Ford, Mark Richards, Pramod Sadalage, Zhamak Dehghani, *Software Architecture: The Hard Parts*, 1-nashr, O'Reilly, 2021 (copyright 2022), 1-bob, 5-bet - ADR ni Michael Nygard blog postida targ'ib qilgani va Thoughtworks Technology Radar da "adopt" belgisini olgani; ADR odatda bir-ikki bet; AsciiDoc, Markdown yoki wiki shabloni; sarlavha qisqa ot iborasi, Kontekst muqobillarni sanaydi, Qaror asoslashni o'z ichiga oladi, Oqibatlar trade-off larni yozadi
- Neal Ford va boshqalar, *Software Architecture: The Hard Parts*, 1-nashr, 2021, 1-bob, 5-7-betlar - qarorni hujjatlash va uning qo'llanishini boshqarish ikki alohida ish; fitness function "obyektiv butunlik bahosi"; "yuqori unumli" yaramaydi, o'lchanadigan qiymat kerak
- Neal Ford va boshqalar, *Software Architecture: The Hard Parts*, 1-nashr, 2021, 2-bob, 26-27-betlar - murakkab real tizimlar uchun universal qoida yo'q, best practice mavjud emas; ATAM kabi metodikalar kundalik muammolardan uzoq; trade-off tahlilining uch qadami
- Neal Ford va boshqalar, *Software Architecture: The Hard Parts*, 1-nashr, 2021, 15-bob, 399-412-betlar - sifat darajali trade-off jadvali (402-403-betlar, Table 15-1 va Table 15-2); MECE ro'yxati (404-405-betlar); kontekstdan chiqib ketish tuzog'i (405-407-betlar); domen ssenariylarini modellashtirish (408-409-betlar); dalilni kalit nuqtalarga qisqartirish (410-bet)
- Mark Richards, Neal Ford, *Fundamentals of Software Architecture*, 1-nashr, O'Reilly, 2020, 1-bob - birinchi qonun: arxitekturada hamma narsa trade-off; Corollary 1: trade-off topilmagan bo'lsa u hali topilmagan; ikkinchi qonun: "why" "how" dan muhimroq
- Mark Richards, Neal Ford, *Fundamentals of Software Architecture*, 1-nashr, 2020, 2-bob - trade-off tahlili afzallik va kamchilik jadvali bilan yoziladi va javob "it depends" bo'ladi; Rich Hickey ning gapi: dasturchi foydani biladi, arxitektor trade-off ni ham bilishi kerak
- Mark Richards, Neal Ford, *Fundamentals of Software Architecture*, 1-nashr, 2020, 6-bob - obyektiv ta'rif bo'lmasa xarakteristika haqida muhokama bo'lmaydi; o'rtacha outlier ni yashiradi; maqsad qiymat o'zboshimchalik bilan emas, statistik tahlil bilan qo'yiladi
- Mark Richards, Neal Ford, *Fundamentals of Software Architecture*, 1-nashr, 2020, ilova "Self-Assessment Questions", 19-bob savollari - 19-bobda ADR ning besh asosiy bo'limi borligi, asoslash Qaror bo'limida turishi, alohida Alternatives bo'limi bo'lmasa muqobillar Kontekst da sanalishi, Proposed holatining uch mezoni, va "covering your assets" hamda "email-driven architecture" antipatternlarining nomlari
- Paul Clements, Felix Bachmann, Len Bass, David Garlan va boshqalar, *Documenting Software Architectures: Views and Beyond*, 2-nashr, Addison-Wesley, 2010, Prolog, 44-bet ("Rule 5: Record Rationale") - eng muhim qarorlar uchun sababni yozish; rad etilgan muhim muqobillarni va rad sababini yozish; sababni yozishga arziydigan uch holat (sifat talabiga erishish uchun kalit qaror, uzoq muhokama talab qilgan qaror, eksperiment yoki prototip bilan baholangan qaror)
- Paul Clements va boshqalar, *Documenting Software Architectures: Views and Beyond*, 2-nashr, 2010, Prolog, 44-45-betlar ("Rule 6") - eskirgan hujjat ishlatilmaydi, yangilanib turgan hujjat ishlatiladi
- George Fairbanks, *Just Enough Software Architecture: A Risk-Driven Approach*, 1-nashr, Marshall & Brainerd, 2010, 3-bob - risk-driven model: "risklarim nima, qaysi usul ularni kamaytiradi, risk yopildimi" (3.1); risk-driven ishlamayotganining belgisi risklarni sanab bera olmaslik (3.2); arxitektura ishi nosozlik riski bilan mutanosib bo'lishi va model oraliq mahsulot ekani (3.6); "Logical rationale" argument shakli (3.1)
- George Fairbanks, *Just Enough Software Architecture*, 1-nashr, 2010, 5.4 - rasional arxitektura tanlovi shabloni "<x> ustuvor, shuning uchun <y> ni tanladik va <z> kamchiligini qabul qildik"; sababni ochiq yozish kelishmovchilikni injenerlik savoliga aylantiradi va muhokamadan ego ni olib tashlaydi
- George Fairbanks, *Just Enough Software Architecture*, 1-nashr, 2010, 12.5 - faqat sanoqli qaror pivotal, qolganlari yozishga arzimaydi; qaror yozuvi qaror va sabab juftligidan iborat
- Simon Brown, *Software Architecture for Developers*, Leanpub, 5-bob, 12-13-betlar - Booch ta'rifi: arxitektura tizimni shakllantiruvchi muhim qarorlar, muhimlik o'zgartirish narxi bilan o'lchanadi; arxitektura qarori tushdan keyingi bitta refactoring bilan qaytarilmaydi
- Simon Brown, *Software Architecture for Developers*, 26-bob, 67-bet va 39-bob, 116-118-betlar - "last responsible moment" texnologiya qarorini chetlab o'tish bahonasi sifatida ishlatilishi; "har qanday texnologiyada qurish mumkin" degani "qurish kerak" degani emas
- Simon Brown, *Software Architecture for Developers*, 60-bob, 172-173-betlar - decision log: texnologiya va arxitektura tanlovini, qanday tekshirilganini (product evaluation yoki proof of concept) va ko'rib chiqilgan boshqa variantlarni yozish; proof of concept va unum testi natijalariga havola berish
- Robert C. Martin, *Clean Architecture*, 1-nashr, Prentice Hall, 2017, 15-bob, 140-142-betlar ("Keeping Options Open") - siyosatni detaldan ajratish qarorni kechiktirishga imkon beradi; detal deb nomlanganlar: baza, web server, REST, DI framework; variantlar uzoq ochiq qolsa ma'lumot ko'p bo'ladi
- Gergely Orosz, *The Software Engineer's Guidebook*, 1-nashr, Pragmatic Engineer BV, 2023, 15-bob, 207-209 va 214-215-betlar - RFC ning maqsadi (kalit fikrni erta olib loyiha muddatini qisqartirish), RFC ni ish oqimiga qo'yishning to'rt shakli, yozishning to'rt foydasi, fikr yig'ishning asinxron, sinxron va aralash shakllari, arxitektura hujjati RFC dan farqli ravishda fikr uchun emas qayd uchun yozilishi, muhokamani ochadigan besh usul (imkoniyat talablari, oldindan tayinlangan qaror egasi, kodni yozadigan odam mezoni, prototip, mahsulot homiyligi), qaytarilishi arzon qarorda tiqilib qolmaslik va qaytish sababini yozib tarqatish
- Robert C. Martin, *Clean Code*, 1-nashr, Prentice Hall, 2008, 11-bob "Systems", "Optimize Decision Making", 167-168-betlar - qarorni oxirgi imkon bo'lgan daqiqaga qoldirish dangasalik emas; muddatidan oldin qilingan qaror kam ma'lumot bilan qilingan qaror
- Simon Brown, *Software Architecture for Developers*, Leanpub, 32-bob, 79-81-betlar - arxitekturani tushunish bilan uni muloqotda yetkazish bir narsa emas; norasmiy eskizning sakkiz nuqsoni (rang kodi, qutilar va chiziqlar ma'nosi, yo'q munosabat, umumiy atama, tushirib qoldirilgan texnologiya, aralashgan abstraksiya darajalari, ortiqcha tafsilot, kontekst yo'qligi)
- Simon Brown, *Software Architecture for Developers*, Leanpub, 33-bob, 82-83-betlar - eskiz rassomlik emas va to'liq model emas; eskizning foydalari ro'yxati; kontekst, konteyner va komponent diagrammalari odatda yetarli
- Simon Brown, *Software Architecture for Developers*, Leanpub, 34-bob, 84-97-betlar - jamoalar nega vizuallashtira olmaydi (uchta sabab, 84-bet); samarasiz eskiz turlarining nomlari: shopping list, boxes and no lines, functional view, airline route map, generically true, logical view, deployment vs execution context, nomlanmagan aktyorlar (95-bet)
- Simon Brown, *Software Architecture for Developers*, Leanpub, 35-bob, 98-101-betlar - bitta uber-diagramma muammosi va turli abstraksiya darajasidagi bir nechta diagramma; tizim, konteyner, komponent, sinf ierarxiyasi (99-bet); to'rt turdagi diagramma va sinf darajasining ixtiyoriyligi (100-bet); umumiy abstraksiya umumiy notatsiyadan muhimroq, xarita va legend analogiyasi (100-bet); qutiga javobgarlik yozish (101-bet)
- Simon Brown, *Software Architecture for Developers*, Leanpub, 36-bob, 102-105-betlar - kontekst diagrammasining uch savoli; markazda bitta quti, atrofida foydalanuvchi va qo'shni tizimlar; fokus texnologiya emas, odam va tizimda; o'zaro ta'sirni maqsad bilan annotatsiya qilish va use case ro'yxati (103-bet); to'rt motivatsiya va "ikki daqiqada chiziladi" (103-bet); o'quvchisi texnik va notexnik (104-bet)
- Simon Brown, *Software Architecture for Developers*, Leanpub, 37-bob, 106-110-betlar - konteyner diagrammasining besh savoli; konteyner turlari ro'yxati va har konteyner uchun nom, texnologiya, javobgarlik (107-bet); "alohida deploy qilinadimi" sinovi (107-bet); chiziqqa maqsad, usul, uslub, protokol va port yozish (107-108-betlar); tizim chegarasi qutisi va u kontekst diagrammasidagi bitta qutiga to'g'ri kelishi (108-bet); o'quvchisi operatsiya va qo'llab-quvvatlash ham (108-bet); nusxa soni, failover va klasterlash alohida deployment diagrammasida (110-bet)
- Simon Brown, *Software Architecture for Developers*, Leanpub, 38-bob, 111-115-betlar - komponent diagrammasining uch savoli; odatda faqat bitta konteyner ichi ko'rsatiladi (112-bet); har komponent uchun nom, texnologiya, javobgarlik (112-bet); use case ni komponentlar bo'ylab kuzatish to'liqlik sinovi, audit komponenti misoli (112-113-betlar); komponent darajasi sinfdan bir pog'ona yuqori va dizayn soat yoki kun ishi, o'quvchisi faqat ishlab chiqish jamoasi (113-bet)
- Simon Brown, *Software Architecture for Developers*, Leanpub, 40-bob, 120-121-betlar - "kodda shunday qilasizmi" sinovi; umumiy logging komponenti va CQRS dagi qatlam dialoglari; diagramma haqiqatni aks ettiruvchi abstraksiya berishi va element bilan kod o'zaro kuzatiladigan bo'lishi; retrospektiv chizishda savol "biz uni shunday kodladikmi" ga aylanadi
- Simon Brown, *Software Architecture for Developers*, Leanpub, 41-bob, 122-127-betlar - komponent interfeys ortidagi bog'liq xatti-harakatlar to'plami, yuqori kogeziya va past bog'liqlik (122-bet); "komponent haqida gaplashamiz, sinf yozamiz" va Fairbanks ning "model-code gap" atamasi (123-124-betlar); qatlam bo'yicha paketlashda komponent paketlar bo'ylab sochilishi (124-125-betlar); komponent bo'yicha paketlash (126-bet); "tuzilishni tushuntirish qiyin bo'lsa, tuzilishni o'zgartiring" (127-bet)
- Simon Brown, *Software Architecture for Developers*, Leanpub, 43-bob, 131-136-betlar - sarlavha, yorliq va qisqartma, shakl (131-bet); javobgarlikni etti qo'shuv-ayirish ikki banddan oshmaydigan ro'yxat yoki bitta gap bilan yozish (132-bet); chiziq uslubi va strelka bog'liqlikni yoki ma'lumot oqimini ko'rsatishi, ikki tomoni strelkali chiziqdan ehtiyot bo'lish (132-133-betlar); rang, chegara, joylashuv va yo'nalish (133-135-betlar); legend tarkibi (135-bet); diagramma review ro'yxatining to'qqiz bandi (135-136-betlar); chizish paytidagi savollarga quloq solish (136-bet)
- Simon Brown, *Software Architecture for Developers*, Leanpub, 44-bob, 137-138-betlar - konteyner va komponent diagrammalarini qo'shish faqat sodda tizimda, aks holda konteyner diagrammasiga javobgarlik ro'yxati yoziladi (137-bet); umumiy komponentni har diagrammada izoh bilan ko'rsatish; utility komponentni chetga qo'yib izohlash (138-bet); C4 ustiga tashkilot kontekst diagrammasi qo'shilsa model C5 ga aylanadi (138-bet)
- Simon Brown, *Software Architecture for Developers*, Leanpub, 46-bob, 141-143-betlar - kod hamma narsani aytmaydi; koddan javob topilmaydigan savollar ro'yxati va "nimani bilmasligingizni bilmaysiz" (142-bet); kod ustidagi qo'shimcha ma'lumot qatlami (143-bet)
- Simon Brown, *Software Architecture for Developers*, Leanpub, 47-bob, 144-148-betlar - qo'shimcha hujjatni sayohat qo'llanmasi sifatida ko'rish (144-bet); qo'llanmaning to'rt qismi: xaritalar, diqqatga sazovor joylar, tarix va madaniyat, amaliy ma'lumot (145-147-betlar); o'n uch bo'limli ro'yxat va chuqur texnik tafsilotdan saqlanish (147-bet); "beware of the views" va bo'limni yetkazilayotgan narsaga mos nomlash (147-148-betlar); mahsulot uchun bitta qo'llanma, loyiha esa delta (148-bet)
- Simon Brown, *Software Architecture for Developers*, Leanpub, 48-bob, 149-bet - Context bo'limi majburiy, bir-ikki bet yetarli va kontekst diagrammasi hikoyaning ko'p qismini aytadi
- Simon Brown, *Software Architecture for Developers*, Leanpub, 49-bob, 150-151-betlar - Functional Overview bo'limi majburiy; tizim nima qilishini xulosalaydi va qaysi funksiya yoki rol arxitektura uchun ahamiyatli ekanini hamda nega ahamiyatli ekanini bog'laydi
- Simon Brown, *Software Architecture for Developers*, Leanpub, 53-bob, 158-159-betlar - Software Architecture bo'limi majburiy; asosiy fokus konteyner va komponent diagrammalari, yoniga qisqa bayon va har konteyner bilan komponentning xulosasi
- Paul Clements va boshqalar, *Documenting Software Architectures: Views and Beyond*, 2-nashr, Addison-Wesley, 2010, Prolog, P.3, 22-23-betlar - ko'rinish ta'rifi: tizim elementlarining to'plami va ular bilan bog'liq munosabatlarning tasviri; qush qanoti analogiyasi; asosiy printsip "tegishli ko'rinishlarni hujjatlashtirish va ustiga bir nechta ko'rinishga tegishli hujjatni qo'shish"; qatlamli ko'rinish portativlik, deployment ko'rinishi unum va ishonchlilik haqida gapiradi; bitta ko'rinish hujjatining besh elementi va barcha ko'rinishga tegishli hujjatning to'rt elementi (23-bet)
- Paul Clements va boshqalar, *Documenting Software Architectures: Views and Beyond*, 2-nashr, 2010, Prolog, P.4 va P.4.1, 25 va 29-30-betlar - uslub (style) elementlar va munosabat turlarining ixtisoslashishi hamda cheklovlar to'plami (25-bet); arxitektor bir vaqtda uch xil o'ylashi va uch kategoriya: module, component-and-connector, allocation; uslubni tizimga qo'llaganda natija ko'rinish bo'ladi (29-bet); modul avvalo amalga oshirish birligi, komponent runtime birligi, Szyperski ta'rifi (29-30-betlar)
- Mark Richards, Neal Ford, *Fundamentals of Software Architecture*, 1-nashr, 2020, ilova "Self-Assessment Questions", 21-bob savollari - 21-bob ("Diagramming and Presenting Architecture") C4 ning "to'rt C" si, komponentlar orasidagi nuqtali chiziqning ma'nosi, "irrational artifact attachment" va taqdimotdagi "bullet-riddled corpse" antipatterni haqida gapirishi
- ESLATMA: korpusdagi *Fundamentals of Software Architecture* nusxasida 19-bob ("Architecture Decisions") ning tanasi yo'q, faqat ilovadagi o'z-o'zini tekshirish savollari bor. Shuning uchun ADR maydonlarining to'liq ro'yxati, antipatternlarning tavsifi va "architecturally significant" ning Nygard bergan besh omili bu bobda iqtibos qilinmaydi. "Architecturally significant" ta'rifi uchun Booch ning Brown keltirgan ta'rifi ishlatilgan
- ESLATMA: korpusdagi *Fundamentals of Software Architecture* nusxasida 21-bob ("Diagramming and Presenting Architecture") ning tanasi ham yo'q: PDF 20-bobdan 24-bobga o'tadi. Shuning uchun 3.12 va 3.17 da shu kitobdan faqat ilovadagi savollar tasdiqlagan nomlar sanaladi, mazmuni iqtibos qilinmaydi. C4 ning butun bayoni Simon Brown dan olingan
- ESLATMA: 3.13, 3.14 va 3.17 dagi diagramma va legend matni korpusning namunasi, kitobdagi rasm emas: Brown ning misollari financial risk system va techtribes.je. 3.15 dagi Java misoli va 3.16 dagi ArchUnit testi ham korpusning tanlovi, kitobda kod yoki avtomatik tekshiruv yo'q. 3.19 dagi `docs/guidebook/` papka daraxti korpusning joylashuv tanlovi, Brown faqat o'n uch bo'lim nomini beradi
- ESLATMA: 3.1 dagi shablon maydonlari (Sana, Qaror egasi, Qayta ko'rish sanasi, Bog'liq ADR, Taxminlar, Kuzatiladigan metrika), Proposed dan boshqa holat qiymatlari, 3.3 dagi erta va kech qaror ro'yxati, 3.6 dagi "rozi emasman, lekin bajaraman" qoidasi va qaror egasi, 3.7 dagi qayta ko'rish sanasi va uchta javob, 3.8 dagi `docs/adr/` joyi va `NNNN-` nom shabloni, 3.9 jadvalidagi "korpus tavsiyasi" deb belgilangan qatorlar, 3.11 dagi checklist shu korpusning amaliy tavsiyasi, kitobdan olingan emas
- John Ousterhout, *A Philosophy of Software Design*, 1-nashr, Yaknyam Press, 2018, 13.7 va 16.4 - bir nechta modulga tegadigan dizayn qarorlari va ularni hujjatlashtirish joyi; aniq markaziy joy bo'lsa izohni shu yerga qo'yish (yangi qiymat qo'shiladigan sanoqning oxiri), bo'lmasa bo'limlarga ajratilgan markaziy `designNotes` fayli va koddagi qisqa ishora; usulning narxi: bitta nusxa topish oson, lekin kod yonida turmagani uchun yangilash qiyin
- ESLATMA: 3.19 dagi `PaymentStatus` misoli va `designNotes` ni ADR va guidebook orasiga joylashtirish tartibi korpusning tanlovi: Ousterhout misolini boshqa tilda va boshqa domenda beradi
- ESLATMA: 3.10 dagi barcha raqam (so'rov soni, qator soni, hajm, p95, indeks hajmi) o'lchanmagan taxmin: ular ADR shaklini ko'rsatish uchun qo'yilgan shartli misol

---

[&larr; 2. Muammoni tushunish va to'g'ri savol berish](02-muammoni-tushunish-va-togri-savol-berish.md) · [Mundarija](README.md) · [4. Kod - muloqot vositasi: nomlash, aniqlik, kognitiv yuk &rarr;](04-kod-muloqot-vositasi-nomlash-aniqlik.md)
