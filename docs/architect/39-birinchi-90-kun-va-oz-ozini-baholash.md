<!-- doc: architect | chapter: 39 | part: VI. Amaliyot va o'sish -->

[Barcha hujjatlar](../../README.md) / [Arxitektor miyasi](README.md)

> Holat: tekshirilgan (2026-10-19). Manbalar bob oxirida.

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
- [39.13 Keyingi qadam: shu hujjatni qolgan beshtasi bilan qanday ishlatish](#3913-keyingi-qadam-shu-hujjatni-qolgan-beshtasi-bilan-qanday-ishlatish)
- [39.14 Amalda qo'llash](#3914-amalda-qollash)

</details>



Arxitektor yangi tizimga kelganda eng katta xatosi tezda foydali bo'lishga urinishdir. Haqiqatda esa birinchi oylarda sizning asosiy mahsulotingiz kod emas, balki ishonchli xarita va ishonchli munosabatdir. Kutish muddatini Google'ning injenerlik amaliyoti ochiq aytadi: yangi kelgan injenerga katta va murakkab infratuzilmaga kirib olish taxminan olti oy olishi oldindan tushuntiriladi, va bu o'rganish uzluksiz, iterativ jarayon ekanini ham eslatib turadi (Software Engineering at Google, 3-bob). Ya'ni uch oy oxirida siz tizimni "biladigan" odam bo'lmaysiz, faqat xaritasi bor odam bo'lasiz.

Quyidagi oylarga bo'linish (birinchi hafta, birinchi oy, ikkinchi oy, uchinchi oy) shu korpusning amaliy rejasi, kitobdan olingan metodologiya emas; manbalar ro'yxatidagi ESLATMA da shu aytilgan. Bobning ikkinchi yarmi diqqatni sizning o'zingizga qaratadi: bilimingizdagi bo'shliqni qanday topish va qaysi mavzuda qay darajada turganingizni qanday o'lchash. Hujjat shu bob bilan tugaydi, shuning uchun oxirida oltita hujjatni birgalikda qanday ishlatish ham aytiladi.

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

So'rash kerak bo'lgan odamlar ro'yxati qisqa. Birinchisi tungi chaqiruvlarga javob beradigan dejur injener, chunki u tizimning haqiqiy zaif joyini biladi. Ikkinchisi eng ko'p commit qilgan developer, uchinchisi mahsulot egasi. Dejurdan bitta savol so'rang: oxirgi oylarda sizni nima uyqudan uyg'otdi. Bu savol odatda arxitektura muammosining aniq manzilini beradi.

So'rashning o'zi ko'nikma. Google kitobining shu mavzudagi bobidan bitta gap qolsa, u shu: doim o'rganing, doim savol bering. Yangi kelganlarning eng katta xatosi tiqilib qolganda yordam so'ramaslik, "savolim juda sodda" deb o'ylab o'zi urinishdir; ayni paytda "bilmayman, tushuntirib bera olasizmi" deyish yetakchi odamdan kelsa, u boshqalarga ham shu erkinlikni beradi (Software Engineering at Google, 3-bob). Shu bob yana bir amaliyotni ko'rsatadi: yangi a'zoga menejer yoki tech lead bo'lmagan alohida mentor tayinlash, shunda savol berish birovning vaqtini olish hisoblanmaydi.

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

Ro'yxatning o'zi tasodifiy artefakt emas. Fairbanks arxitektura ishini xatarga bog'laydi: arxitekturaga sarflanadigan kuch loyihaning xatariga mos bo'lishi kerak, va usul uch qadamdan iborat - xatarlarni aniqlab ustuvorlashtirish, ularga mos texnikani tanlab qo'llash, keyin xatar kamayganini baholash. U yana telltale belgini aytadi: ko'p developer o'zini xatarga tayangan deb hisoblaydi, lekin "qaysi xatarlar bilan kurashyapsiz va qanday texnika qo'llayapsiz" savoliga javob bera olmaydi, holbuki "qaysi funksiya ustida ishlayapsiz" savoliga hamma javob beradi (Just Enough Software Architecture, 3-bob). Birinchi oydagi og'riq ro'yxati aslida shu javobning yozma shakli.

Ro'yxatni tartiblashda ikkita o'qdan foydalaning: biznesga ta'siri va tuzatish narxi. Yuqori ta'sir va past narx bo'lgan bandlar ikkinchi oyning ishi bo'ladi. Yuqori ta'sir va yuqori narx bo'lganlar uchinchi oydagi rejaga tushadi. Past ta'sirli bandlarni umuman yozib qo'ying, ularga tegmang.

Shu oyda yana bitta o'lchov oling: p99 latency va connection pool to'yinganligi. Ko'p tizimda muammo so'rov sekinligida emas, pool navbatida turadi. Agar HikariCP `pending` metrikasi nolga teng bo'lmasa, siz o'lchovni topdingiz.

## 39.3 Ikkinchi oy: kichik, ko'rinadigan yaxshilanish bilan ishonch qozonish

Ikkinchi oyda bitta qoida bor: natija o'lchanadigan va bir hafta ichida ko'rinadigan bo'lsin. Yaxshi nomzodlar ro'yxati qisqa. Yetishmayotgan timeout qo'yish, bitta og'ir hisobot so'roviga index qo'shish, HikariCP pool o'lchamini to'g'rilash, va metrikani chiqarish.

Bitta oldingi shart bor va u texnik emas. Brown arxitektura tushunarli (accessible) bo'lishini talab qiladi: "logical view" yoki "physical view" kabi atamalarni ishlatishdan oldin jamoa arxitektura nima ekanini va u haqida o'ylamaslikning oqibatini tushunishi shart; menejment ham shuni tushunishi kerak, aks holda "arxitekturani to'xtat va kod yoz" degan ko'rsatma chiqadi (Simon Brown, *Software Architecture for Developers*, Leanpub, 66-bob, 191-192-betlar). Amaliy qadam arzon: ikkinchi oyning birinchi haftasida umumiy lug'at o'rnatiladi, ya'ni jamoa bilan bir sahifada "biz arxitektura deganda nimani tushunamiz" va "u yo'q bo'lsa nima bo'ladi" yoziladi, keyin shu sahifaga qarorlar havola beradi. Bu qadam tashlanib ketilsa, keyingi barcha hujjat atamalar tortishuviga aylanadi va [qarorlarni tarqatish](36-code-review-va-jamoada-texnik-yetakchilik.md#368-arxitektura-qarorlarini-jamoaga-tarqatish-hujjat-ichki-suhbat-namuna-kod) kanali ishlamaydi.

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

Ko'rinadigan yaxshilanishni e'lon qilish usuli ham muhim. Oldingi va keyingi raqamni bitta jadvalda bering, shaklni shunday tuting: o'lchov nomi, o'zgarishdan oldingi qiymat, keyingi qiymat, o'lchov oynasi. Raqam bilan aytilgan natija sizga keyingi oyda kattaroq o'zgarish uchun ruxsat ochadi.

## 39.4 Uchinchi oy: o'rta muddatli reja taklif qilish va kelishib olish

Uchinchi oyda siz endi taklif qilish huquqini qozondingiz. Reja uch oydan olti oyga mo'ljallangan bo'lsin, undan uzoqroq reja ishonchni emas, shubhani keltiradi. Rejada har bir bandning uchta ustuni bo'lsin: qanday o'lchovni yaxshilaydi, qancha ishchi hafta oladi, va qanday risk tug'diradi.

Rejani yozishda eng kuchli vosita alternativani ham ko'rsatishdir. Masalan ombor qoldig'i servisini ajratish taklifida ikkinchi variant sifatida bitta bazada schema ajratishni ham bering. Bu sizni "o'z g'oyasini himoya qiladigan odam" emas, "qarorni ochib beradigan odam" qilib ko'rsatadi.

Variantlarni ko'rsatishning ham shakli bor. Ford va sheriklari taqqoslanadigan variantlar ro'yxatini MECE qilib tuzishni tavsiya qiladi: o'zaro kesishmaydigan va sohani to'liq qoplaydigan ro'yxat, aks holda taqqoslash noto'g'ri narsalarni solishtiradi (The Hard Parts, 15-bob, 404-bet). Ko'rsatishda esa teskari qoida ishlaydi: yig'ilgan hamma dalilni yoyish o'rniga tahlilni bir nechta asosiy nuqtaga siqish kerak, chunki texnik tafsilotning ko'pi biznes tomoni uchun begona va u qarorga hissa qo'shmaydi (15-bob, 409-410-bet).

Kelishib olishning amaliy shakli qisqa qaror hujjati. Bir sahifada kontekst, variantlar, tanlangan yo'l, va natijalar. Shu hujjatni jamoa bilan o'qib chiqing, keyin uni repozitoriyga qo'ying. Og'zaki kelishuv yo'qoladi, yozilgani qoladi.

| Masala | Oddiy yondashuv | Arxitektor yondashuvi |
|---|---|---|
| Birinchi hafta | Darhol task olib kod yozadi | Deploy, migratsiya va incident tarixini o'qiydi |
| Muammoni topish | "Kod eski" deb umumlashtiradi | `pg_stat_statements` va pool metrikasi bilan o'lchaydi |
| Birinchi taklif | Katta refactoring taklif qiladi | Timeout va index kabi arzon yutuqni beradi |
| Natijani e'lon qilish | "Tezlashdi" deb aytadi | p99 ning oldingi va keyingi qiymatini ko'rsatadi |
| Mavjud qarorga munosabat | "Buni kim shunday qildi" deb so'raydi | "Qanday sharoitda shunday to'g'ri edi" deb so'raydi |
| Reja ufqi | Ikki yillik maqsadni chizadi | Uch oylik o'lchanadigan bandlarni beradi |
| Alternativa | Bitta yo'lni himoya qiladi | Ikki yo'lni va tanlash mezonini beradi |
| Kelishuv shakli | Majlisda og'zaki tasdiqlaydi | Bir sahifali qaror hujjatini repozitoriyga qo'yadi |
| O'z bilimi | "Bilaman" deb o'tadi | Savol ro'yxati bilan o'zini tekshiradi |
| Jamoaga ta'sir | Qaror markazida o'zi turadi | Jamoa qaror qabul qiladigan mezonni qoldiradi |

Reja qabul qilingandan keyin keyingi ish uni jamoaning ish usuliga aylantirish bo'ladi, va bu alohida mahorat. Brown arxitekturani joriy etishning beshta amaliy yo'lini sanaydi: odamlarni o'qitish, ya'ni arxitektura nima, nega muhim va qanday amaliyot qabul qilinadi degan savollarni yopish; retrospektivada arxitekturani muhokama mavzulari ro'yxatiga qo'shish; `definition of done` ga arxitekturani kiritish; rolni aniq bir odamga biriktirish (avval bitta egasi bo'lsin, keyin bo'lishiladi); va arxitektura kata o'tkazish, ya'ni jamoa oddiy talablar uchun birga yechim loyihalaydi va uni diagramma bilan tushuntiradi (Simon Brown, *Software Architecture for Developers*, Leanpub, 66-bob, 192-193-betlar). Beshtasi bir-birini almashtirmaydi: birinchisi bilimni, ikkinchi va uchinchisi odatni, to'rtinchisi javobgarlikni, beshinchisi mahoratni beradi. Uchinchi yo'lning testlash tomonidagi shakli [sifat darvozalari va definition of done](../testing/01-sifat-strategiyasi-va-arxitektorning-roli.md#15-sifat-darvozalari-va-definition-of-done) bo'limida yozilgan: `definition of done` ga qo'shilgan band o'lchanadigan bo'lishi kerak, aks holda u reliz kuni e'tiborsiz qoladi.

O'zgarishni qanday boshlash esa jamoaning holatiga bog'liq, va Brown ikki yo'lni ajratadi. Reaktiv yo'lda jamoa faqat yomon narsa yuz bergandan keyin o'zgaradi, ya'ni katalizator kerak bo'ladi, va ko'pchilik jamoa shunday. Proaktiv yo'lda hali hech narsa buzilmagan, lekin yaxshilash ko'rinadi, va ironik tarzda bu yo'ldan boradigan jamoalar allaqachon yaxshi jamoalar (66-bob, 193-195-betlar). Ikki yo'lda taktika ham boshqa. Reaktiv holatda o'zgarishni sotish kerak: hozirgi holat, risk va oqibat qaror qabul qiluvchilarga aniq va qisqa ko'rsatiladi, ya'ni yuqoridagi reja jadvalining uch ustuni aynan shu ish uchun. Proaktiv holatda ruxsat so'rash o'rniga namuna bilan yetaklanadi: bitta muammo topiladi, u mayda qadamlar bilan o'zingiz tuzatiladi va natija ko'rsatiladi; bu [namuna kod](36-code-review-va-jamoada-texnik-yetakchilik.md#368-arxitektura-qarorlarini-jamoaga-tarqatish-hujjat-ichki-suhbat-namuna-kod) yo'lining aynan o'zi.

## 39.5 Mavjud qarorlarni hurmat qilish: "nega shunday qilingan" savolini birinchi berish

Har bir g'alati kod bir paytda to'g'ri javob bo'lgan. Hisobotda denormalizatsiya qilingan jadval bo'lsa, ehtimol o'sha paytda hisobot 40 sekund ishlagan va mijoz ketib qolgan. Native SQL yozilgan joy bo'lsa, ehtimol Hibernate generatsiya qilgan so'rov planner tomonidan noto'g'ri bajarilgan.

Shu sababli birinchi savol bitta bo'lsin: qanday cheklov ostida bu qaror oqilona edi. Bu savol sizga ko'rinmagan cheklovni beradi, muallifni esa himoyaga o'tishga majburlamaydi.

Richards va Ford buni qoida darajasiga ko'taradi: arxitekturaning ikkinchi qonuni "nega" ning "qanday" dan muhimroq ekani. Ular sababini shunday ko'rsatadi: begona tizimga qarab uning tuzilishi QANDAY ishlashini aniqlash mumkin, lekin NEGA aynan shu tanlov qilinganini tushuntirish qiyin, chunki aynan shu yozib qoldirilmagan (Fundamentals of Software Architecture, 1-bob). Google kitobi shu munosabatning yetakchilik tomonini qo'shadi: jamoaga ishonish, ya'ni a'zolarning oldingi yutuqlari va qobiliyatini hurmat qilish, hatto ular sizning jamoangizga yangi bo'lsa ham; va maslahat so'ralganda darhol yechim rejimiga o'tmasdan savol berish (Software Engineering at Google, 5-bob).

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

Shu uchlikning kaliti halollik. McConnell intellektual halollikni kasbiy yetuklikning bir qismi deb ataydi va uning birinchi ikki alomatini shunday beradi: ekspert bo'lmagan joyda ekspert bo'lib ko'rinmaslik va xatoni darhol tan olish. U o'lchov ham beradi: har masalada o'z ishonchingiz darajasini raqamlashga tayyor bo'ling, va agar u odatda 100 foiz chiqsa, bu ogohlantirish signali (Code Complete, 2-nashr, 33.4, 826-bet). Google kitobi shu nuqtada bir gapni qo'shadi: qancha ko'p bilsangiz, bilmagan narsangizni shuncha ko'p bilasiz (3-bob).

| Tuzoq | Yechim |
|---|---|
| Hammasini bir vaqtda o'rganishga urinish | Haftada bitta mavzu, ikki daqiqalik tushuntirish mashqi |
| Javobni eslab qolishni bilim deb hisoblash | Oq doskada mexanikani chizishni talab qilish |
| Faqat kuchli mavzuni takrorlash | Zaif ustunni jadvaldan tanlab, shunga vaqt berish |
| Nazariyani amaliyotsiz o'qish | Har mavzuni real loyihadagi bitta muammoga ulash |
| Darajani o'zi baholab oshirib qo'yish | Jamoadagi bitta odamga tushuntirib, savolini eshitish |
| Bo'shliqni yozib qo'ymaslik | Ro'yxatni repozitoriyda saqlash va oyda bir qayta ko'rish |

## 39.7 Yetuklik darajalari: qaysi mavzuda qay darajada turibsiz

Daraja o'zini maqtash uchun emas, vaqtni to'g'ri taqsimlash uchun kerak. Ball yoki foiz yo'q: bu yerda faqat uchta nomlangan daraja bor, va ularning orasidagi chegara o'lchov emas, tavsif.

Darajalarga bo'lish g'oyasining o'zi kitobdan keladi. McConnell o'z kompaniyasida ishlatilgan kasbiy o'sish zinapoyasini to'rt darajada beradi: boshlang'ich (bitta tilning asosiy imkoniyatlarini ishlatadi), kirish (bir necha tilning asosini biladi, kamida bittasida erkin), kompetentlik (til yoki muhitda chuqur ekspertiza; ko'p programmist shu darajada qolib ketadi) va yetakchilik (ekspertizaga qo'shimcha ravishda programmalashning kattaroq qismi odamlar bilan muloqot ekanini biladi va kodni mashina uchun emas, odam uchun yozadi). Uning xulosasi ham o'z joyida: boshlang'ich yoki kompetent bo'lish gunoh emas, nima qilish kerakligini bilib ham shu darajada uzoq turib qolish gunoh (Code Complete, 2-nashr, 33.3, 825-bet).

Quyidagi jadval shu g'oyani shu korpusning mavzulariga ko'chiradi: qatorlar va daraja tavsiflari korpusning o'zi tuzgan, McConnell ning zinapoyasi emas. O'zingizni rost joylashtiring, keyin eng past qatorlardan ikkitasini tanlab, keyingi choraklik o'rganish rejangizni shundan quring; har qatorning oxirgi ustunida tegishli bob bor, tekshiruv shu bobdan boshlanadi.

| Mavzu | Boshlang'ich | O'rta | Yuqori | Bob |
|---|---|---|---|---|
| JVM xotira | Heap va stack farqini biladi | GC log o'qiydi, pause sababini topadi | Region o'lchami va allocation rate bo'yicha sozlaydi | [10](10-garbage-collection-va-xotira-sozlash.md) |
| Concurrency | `synchronized` ishlatadi | Thread pool o'lchamini hisoblab beradi | Virtual thread va blocking chegarasini loyihalaydi | [11](11-concurrency-thread-lock-atomic-happens.md), [12](12-virtual-threads-structured-concurrency-va.md) |
| Spring konteyner | Bean e'lon qiladi | Proxy va self-invocation tuzog'ini biladi | Lifecycle va startup vaqtini boshqaradi | [15](15-spring-core-mexanikasi-ioc-konteyner-bean.md) |
| Tranzaksiya | `@Transactional` qo'yadi | Propagation va isolation tanlaydi | Flush, lock va retry siyosatini loyihalaydi | [19](19-spring-tranzaksiyalari-va-ularning.md) |
| Hibernate | Entity yozadi | N+1 ni topib tuzatadi | Fetch strategiyasi va cache chegarasini belgilaydi | [18](18-spring-data-jpa-va-hibernate-chuqur.md) |
| PostgreSQL planner | `EXPLAIN` chaqiradi | `EXPLAIN ANALYZE BUFFERS` o'qiydi | Statistika va index turini qarorga aylantiradi | [24](24-planner-statistika-va-explain-analyze-oqish.md) |
| Index dizayni | B-tree qo'yadi | Composite tartibini to'g'ri beradi | Partial, GIN va covering index tanlaydi | [23](23-indekslar-b-tree-gin-gist-brin-va-tanlov.md) |
| API dizayni | REST endpoint yozadi | Versiyalash va xato formatini belgilaydi | Mos keluvchanlik shartnomasini boshqaradi | [13](13-zamonaviy-java-tili-va-api-dizayni.md) |
| Observability | Log yozadi | Metrika va alert qo'yadi | SLO va xato budjetini belgilaydi | [30](30-kuzatuvchanlik-amaliyoti-log-metrika-trace.md) |
| Deploy | Pipeline ishlatadi | Migratsiyani mos keluvchan yozadi | Nol to'xtovli relizni loyihalaydi | [31](31-deployment-haqiqati-konteyner-cgroup-jvm-va.md), [33](33-sxema-migratsiyasi-va-toxtashsiz-reliz.md) |
| Xavfsizlik | Autentifikatsiya yoqadi | Avtorizatsiya chegarasini tekshiradi | Sir boshqaruvi va audit izini quradi | [20](20-spring-security-filter-chain-oauth2-jwt.md) |
| Qaror yuritish | Fikrini aytadi | Variantlarni taqqoslaydi | Mezon va qaytarish yo'lini yozib qoldiradi | [03](03-qaror-qabul-qilish-va-uni-hujjatlashtirish.md) |

Yuqoridagi jadval mavzu bo'yicha baholaydi. Ikkinchi o'q rolning qismlari bo'yicha boradi va u ishga olish suhbatida ham, o'z-o'zini baholashda ham ishlaydi. Brown tajribani yaxshi ko'rsatkich, lekin yetarli emas deb hisoblaydi va rolning oltita qismini alohida baholashni taklif qiladi: nofunksional talabni tutib olish va uni shubha ostiga olish; noldan dizayn qilish yoki mavjudni kengaytirish; texnik riskni isbotlash yoki shunchaki umid qilish; arxitekturani doimiy rivojlantirish yoki uni implementatsiya jamoasiga topshirib qo'yish; qo'l bilan ishlash yoki chetdan kuzatish; sifatni ta'minlash va standart tanlash yoki o'zi baholanish (Simon Brown, *Software Architecture for Developers*, Leanpub, 11-bob, 32-33-betlar).

| Rol qismi | Zaif tomoni | Kuchli tomoni | Tekshirish savoli |
|---|---|---|---|
| Nofunksional talab | berilganini qabul qiladi | tutib oladi va shubha ostiga oladi | oxirgi marta qaysi talabni rad etdingiz va nega |
| Dizayn | faqat noldan quradi | mavjudni ham kengaytiradi | oxirgi uch qaror mavjud tizim ichida bo'ldimi |
| Texnik risk | umid qiladi | prototip yoki o'lchov bilan isbotlaydi | qaysi risk spike bilan yopildi |
| Evolyutsiya | topshirib qo'yadi | davomiy rivojlantiradi | reliz chiqqandan keyin arxitektura kim bilan qoldi |
| Ishtirok | chetdan kuzatadi | qo'l bilan ishlaydi | oxirgi oyda qaysi kodga tegdingiz |
| Sifat va standart | o'zi baholanadi | standart tanlaydi va ta'minlaydi | qaysi standart sizning tanlovingiz bilan kuchga kirdi |

Jadvalning ikki ustuni ataylab "yoki" shaklida yozilgan, chunki har qatorda ikki tomondan biri ustun bo'ladi va baholash ballda emas, tomon tanlashda bo'ladi. Ishga olish suhbatida shu savollar tajriba yillarini almashtiradi: javob konkret hodisa bilan kelsa qism kuchli, umumiy tavsif bilan kelsa zaif.

## 39.8 Fikrlash va qarorlar bilimini o'zingizga qo'llash

Fikrlash va qarorlar qismidagi vositalar faqat tizimga emas, sizning karyerangizga ham tegishli. Qaytarib bo'lmaydigan qarorni sekin qabul qilish qoidasi sizning o'zingizga ham tegadi. Masalan yangi texnologiyaga butun jamoani ko'chirish qaytarib bo'lmaydigan qarordir, uni bitta servisda sinab ko'rish esa qaytariladi.

Vaqt budjetini o'ylab topmang, kitobdagi oynani oling: kuniga kamida 20 daqiqa, ertalab, email'ni ochishdan oldin (Fundamentals of Software Architecture, 24-bob; shu korpusda [38.11](38-doimiy-organish-va-texnologiya-tanlash.md#3811-java-va-spring-ekotizimini-kuzatib-borish-usullari)). Ikkinchi tartibli ta'sir haqida o'ylash qoidasi ham shu yerda ishlaydi: siz tanlagan texnologiya jamoaning keyingi yillardagi ishga olish imkoniyatini belgilaydi.

Eng muhimi esa qarorni yozib qoldirish odati. O'zingiz uchun qisqa jurnal yuritib boring: qanday qaror qabul qildim, qanday kutgandim, nima bo'ldi. Bir muncha vaqtdan keyin shu jurnal sizning eng kuchli o'qituvchingiz bo'ladi.

Odatning o'zi nega hal qiluvchi ekanini McConnell alohida bo'limda tushuntiradi: programmist qiladigan ishning ko'pi ongli o'ylamasdan, odat bilan bajariladi, va agar siz tezlik bilan o'qiluvchanlik orasida har safar bir xil tanlov qilsangiz, siz tanlamayapsiz, odat bilan javob berayapsiz. Yomon odatni "hech qanday odat" bilan almashtirib bo'lmaydi, uni boshqa odat bilan almashtirish kerak (Code Complete, 2-nashr, 33.9, 833-834-bet).

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
      probability: 0.1         # namuna ulushi: trafik hajmiga qarab o'lchanib tanlanadi
  metrics:
    distribution:
      percentiles-histogram:
        http.server.requests: true   # p99 ni serverda hisoblash uchun
```

Uchinchi savol: oxirgi migratsiyani orqaga qaytarish rejasi bormi va u sinalganmi. To'rtinchi savol: ma'lumotlar bazasidan tiklanish vaqti qancha va bu raqam o'lchanganmi yoki taxminmi. Beshinchi savol: to'lov provayderi 30 sekund javob bermasa, tizimingiz qanday yomonlashadi. Agar bu beshta savolga raqam bilan javob bera olsangiz, siz operatsion jihatdan tayyorsiz.

## 39.13 Keyingi qadam: shu hujjatni qolgan beshtasi bilan qanday ishlatish

Oltita hujjat bitta maqsadga xizmat qiladi, lekin har biri boshqa paytda ochiladi; qaysi biri qaysi savolga javob berishi [umumiy README dagi jadvalda](../../README.md) bor. Bu hujjat qaror paytida ochiladi: nima uchun shunday bo'ladi va qanday raqam bilan tanlanadi. Dizayn [patternlar hujjati](../patterns/README.md) loyihalash paytida ochiladi, chunki u shaklni beradi. Testlash qo'llanmasi esa ishonchni tekshirish paytida ochiladi.

Amaliy tartib shunday bo'lsin. Yangi talab kelganda avval bu hujjatdan tegishli mexanika bobini o'qing, chunki qaror cheklovdan chiqadi. Keyin dizayn [patternlar hujjatidan](../patterns/README.md) shaklni tanlang, masalan tashqi tizimga ishonchli xabar yuborish uchun outbox pattern. Undan keyin [testlash qo'llanmasidagi](../testing/README.md) contract testing va Testcontainers bo'limlaridan tekshirish rejasini oling. Kod yozilayotganda [toza kod qoidalari](../clean-code/README.md), PR ochilganda [kod review hujjati](../code-review/README.md), CI quality gate yiqilganda esa [SonarQube hujjati](../sonarqube/README.md) ochiladi.

Jamoada ishlatishning eng yaxshi usuli esa birgalikda o'qishdir. Haftada bitta bob tanlang, uni ikki kishi o'qib chiqsin, keyin qisqa uchrashuvda jamoaga o'z tizimingiz misolida tushuntirsin. Shu tartib bilim tarqalishini tezlashtiradi, va eng muhimi, u hujjatni o'lik matndan jamoa tiliga aylantiradi. Bu tartib tasodifiy emas: yozilgan bilim tashkilot darajasiga ko'tariladi, odamdagi bilim esa kontekstga moslanadi, va ular bir-birini almashtirmaydi (Software Engineering at Google, 3-bob).

Shu olti hujjat yopiq ro'yxat emas. McConnell o'z kitobining oxirgi bobini aynan shu masalaga ajratadi: qurilish amaliyoti, qurilishdan tashqaridagi mavzular, darajalarga bo'lingan o'qish rejasi va kasbiy tashkilotga qo'shilish (Code Complete, 2-nashr, 35.1-35.5, 856-862-bet). Ya'ni korpusdan keyingi qadam tasodifiy blog emas, o'zingiz tuzgan va yozib qo'yilgan o'qish rejasi bo'ladi.

Oxirgi gap sizning o'zingiz haqida. Arxitektor bo'lish bilim miqdorida emas, qarorning sababini ko'rsatib bera olishda. Richards va Ford kitobini shu uch so'z bilan yopadi: doim o'rganing, doim mashq qiling, va borib arxitektura qiling; ularning ta'kidi shu yerda ham bir xil - yechimning QANDAY qilinganini saqlash voqeaning yarmi, trade-off larni ushlab turgan NEGA esa qolgan yarmi (Fundamentals of Software Architecture, 24-bob). Agar siz har bir qarorni cheklov, variant va o'lchov bilan tushuntirsangiz, jamoa sizdan keyin ham to'g'ri qaror qabul qilishni davom etadi. Shu esa bu hujjatning asl maqsadi edi.

## 39.14 Amalda qo'llash

- [ ] Birinchi haftada deploy pipeline, migratsiya tarixi va oxirgi uchta incident hisobotini o'qib, dejur injenerga "sizni nima uyg'otdi" savolini bering.
- [ ] `pg_stat_statements` va `pg_stat_user_tables` dan top 20 og'ir so'rov va yetishmayotgan index ro'yxatini chiqarib, biznesga ta'siri bo'yicha tartiblang.
- [ ] Barcha tashqi HTTP chaqiruvlarga connect va read timeout qo'yib, `statement_timeout` va `idle_in_transaction_session_timeout` ni yoqing.
- [ ] HikariCP pool o'lchamini so'rov davomiyligi hisobi bilan qayta belgilab, `pending` metrikasini dashboardga chiqaring.
- [ ] Ikkinchi oyda bitta ko'rinadigan yaxshilanishni oldingi va keyingi p99 qiymati va o'lchov oynasi bilan e'lon qiling.
- [ ] Uchinchi oyda bir sahifali qaror hujjatini yozib, ichida ikkita variant, tanlash mezoni va qaytarish yo'lini bering.
- [ ] Yetuklik matritsasidan o'zingizga eng past ikkita mavzuni tanlab, chorakka faqat shu ikkitasini rejalashtiring.
- [ ] Shu bobdagi sinov savollaridan o'tib, "taniyman lekin tushuntirmayman" deb belgilangan har bir mavzuni jamoaga qisqa uchrashuvda tushuntirib bering.

## Manbalar

- *Software Engineering at Google*, O'Reilly, 2020, 3-bob - yangi injenerning kirib
  olishi taxminan olti oy davom etishi, "always be learning, always be asking questions",
  menejer bo'lmagan alohida mentor tayinlash, yozilgan va odamdagi bilimning bir-birini
  to'ldirishi, "qancha ko'p bilsangiz, bilmaganingizni shuncha ko'p bilasiz"
- *Software Engineering at Google*, O'Reilly, 2020, 5-bob - "lose the ego": jamoaga
  ishonish va a'zolarning oldingi yutuqlarini hurmat qilish; maslahat so'ralganda darhol
  yechim rejimiga o'tmasdan savol berish
- Steve McConnell, *Code Complete*, 2-nashr, Microsoft Press, 2004, 33.3 (825-bet) -
  to'rt darajali kasbiy o'sish zinapoyasi va "darajada qolib ketish" haqidagi xulosa
- Steve McConnell, *Code Complete*, 2-nashr, Microsoft Press, 2004, 33.4 (826-bet) -
  intellektual halollik; ishonch darajasini raqamlash va 100 foizning ogohlantirish
  signali ekani
- Steve McConnell, *Code Complete*, 2-nashr, Microsoft Press, 2004, 33.9 (833-834-bet) -
  ishning ko'pi odat bilan bajariladi, yomon odat faqat boshqa odat bilan almashtiriladi
- Steve McConnell, *Code Complete*, 2-nashr, Microsoft Press, 2004, 35.1-35.5
  (856-862-bet) - qurilish va undan tashqaridagi manbalar, darajalarga bo'lingan o'qish
  rejasi, kasbiy tashkilotga qo'shilish
- Mark Richards, Neal Ford, *Fundamentals of Software Architecture*, O'Reilly, 2020,
  1-bob - arxitekturaning ikkinchi qonuni: "nega" "qanday" dan muhimroq; begona tizimning
  qanday ishlashini aniqlash mumkin, nega shunday tanlanganini esa yo'q
- Mark Richards, Neal Ford, *Fundamentals of Software Architecture*, O'Reilly, 2020,
  24-bob - 20 daqiqa qoidasi va uni ertalab email'dan oldin bajarish; "doim o'rganing,
  doim mashq qiling"; QANDAY ni saqlash voqeaning yarmi, NEGA qolgan yarmi
- Neal Ford, Mark Richards, Pramod Sadalage, Zhamak Dehghani, *Software Architecture:
  The Hard Parts*, 1-nashr, O'Reilly, 2021 (copyright 2022), 15-bob (404-bet, 409-410-bet) - taqqoslash uchun MECE
  ro'yxat; dalil to'dasi o'rniga bir nechta asosiy nuqtani ko'rsatish
- George Fairbanks, *Just Enough Software Architecture*, Marshall & Brainerd, 2010,
  3-bob - xatarga tayangan model: xatarlarni aniqlab ustuvorlashtirish, texnikani tanlab
  qo'llash, xatar kamayganini baholash; "qaysi xatarlar bilan kurashyapsiz" savoliga
  javob bera olmaslik belgisi
- ESLATMA: bobning birinchi yarmidagi oylarga bo'linish (birinchi hafta, birinchi oy,
  ikkinchi oy, uchinchi oy) va 39.14 dagi tekshiruv ro'yxati shu korpusning amaliy
  rejasi, kitobdan olingan metodologiya emas
- ESLATMA: 39.7 dagi jadval qatorlari va daraja tavsiflari shu korpusning o'z
  mavzularidan tuzilgan; kitobdan olingani faqat darajalarga bo'lish g'oyasining o'zi.
  Ball va foiz yo'q, tekshiruv har qatorning oxirgi ustunidagi bobdan boshlanadi
- ESLATMA: 39.1-39.4 dagi buyruqlar, SQL so'rovlari va `application.properties` /
  `application.yml` qiymatlari shu korpusning amaliy misollari; qiymatlar o'z muhitingizda
  o'lchanib tanlanadi
- ESLATMA: 39.9-39.12 dagi sinov savollari shu korpusning o'z ro'yxati; javoblar tegishli
  boblarda (Java va JVM uchun 09-14, Spring uchun 15-20, PostgreSQL uchun 21-27,
  operatsion tayyorlik uchun 30-35)
- Simon Brown, *Software Architecture for Developers*, Leanpub, 11-bob (32-33-betlar) - tajriba yaxshi ko'rsatkich, lekin yetarli emasligi va rolning oltita qismini alohida baholash (nofunksional talabni tutib olish va shubha ostiga olish, noldan dizayn yoki mavjudni kengaytirish, texnik riskni isbotlash yoki umid qilish, arxitekturani rivojlantirish yoki topshirish, qo'l bilan ishlash yoki chetdan kuzatish, standart tanlash yoki o'zi baholanish)
- Simon Brown, *Software Architecture for Developers*, Leanpub, 66-bob (191-195-betlar) - arxitekturaning tushunarli (accessible) bo'lishi va atamalardan oldin umumiy lug'at o'rnatish, menejment tushunmasa "arxitekturani to'xtat va kod yoz" ko'rsatmasi chiqishi; joriy etishning beshta yo'li (o'qitish, retrospektiva mavzusi, `definition of done`, rolni bitta odamga biriktirish, arxitektura kata); reaktiv va proaktiv o'zgarish yo'llari, reaktiv yo'lda katalizator va o'zgarishni sotish, proaktiv yo'lda bitta muammoni mayda qadamlar bilan tuzatib namuna bilan yetaklash

---

[&larr; 38. Doimiy o'rganish va texnologiya tanlash](38-doimiy-organish-va-texnologiya-tanlash.md) · [Mundarija](README.md) · [40. Qidiruv: PostgreSQL FTS chegarasi va alohida dvigatelga o'tish &rarr;](40-qidiruv-postgresql-fts-va-alohida-dvigatel.md)
