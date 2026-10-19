<!-- doc: architect | chapter: 23 | part: IV. PostgreSQL chuqur bilim -->

[Barcha hujjatlar](../../README.md) / [Arxitektor miyasi](README.md)

> Holat: tekshirilgan (2026-10-19). Manbalar bob oxirida.

# 23. Indekslar: B-tree, GIN, GiST, BRIN va tanlov (Indexes)

<details>
<summary>Bu bobdagi 23 bo'lim</summary>

- [23.1 B-tree tuzilishi va u qaysi so'rovlarga yordam beradi](#231-b-tree-tuzilishi-va-u-qaysi-sorovlarga-yordam-beradi)
- [23.2 Ko'p ustunli indeks va ustunlar tartibining ahamiyati](#232-kop-ustunli-indeks-va-ustunlar-tartibining-ahamiyati)
- [23.3 Qamrab oluvchi indeks (`INCLUDE`) va index-only scan sharti](#233-qamrab-oluvchi-indeks-include-va-index-only-scan-sharti)
- [23.4 Qisman indeks (`WHERE` bilan) va uning amaliy foydasi](#234-qisman-indeks-where-bilan-va-uning-amaliy-foydasi)
- [23.5 Ifoda bo'yicha indeks va funksiya bilan qidirish](#235-ifoda-boyicha-indeks-va-funksiya-bilan-qidirish)
- [23.6 GIN: massiv, `jsonb` va to'liq matn qidiruvi uchun](#236-gin-massiv-jsonb-va-toliq-matn-qidiruvi-uchun)
- [23.7 GiST, matn o'xshashligi va oraliq turlar](#237-gist-matn-oxshashligi-va-oraliq-turlar)
- [23.8 BRIN: katta, tartibli jadvallar uchun arzon indeks](#238-brin-katta-tartibli-jadvallar-uchun-arzon-indeks)
- [23.9 Indeks narxi: yozuv sekinlashuvi, disk, vacuum yuki](#239-indeks-narxi-yozuv-sekinlashuvi-disk-vacuum-yuki)
- [23.10 Keraksiz indekslarni topish va o'chirish (`pg_stat_user_indexes`)](#2310-keraksiz-indekslarni-topish-va-ochirish-pg_stat_user_indexes)
- [23.11 `CREATE INDEX CONCURRENTLY` va ishlab chiqarishda indeks qo'shish](#2311-create-index-concurrently-va-ishlab-chiqarishda-indeks-qoshish)
- [23.12 Indeks shishishi va `REINDEX CONCURRENTLY`](#2312-indeks-shishishi-va-reindex-concurrently)
- [23.13 Saqlash dvigateli oilalari: B-tree va LSM, o'qish va yozish kuchayishi](#2313-saqlash-dvigateli-oilalari-b-tree-va-lsm-oqish-va-yozish-kuchayishi)
- [23.14 Indeks interfeysi: `pg_am`, operator class va operator family](#2314-indeks-interfeysi-pg_am-operator-class-va-operator-family)
- [23.15 Indeks xossalari: qaysi tur nimani qo'llaydi](#2315-indeks-xossalari-qaysi-tur-nimani-qollaydi)
- [23.16 Hash indeks: qachon mantiqiy, qachon B-tree afzal](#2316-hash-indeks-qachon-mantiqiy-qachon-b-tree-afzal)
- [23.17 SP-GiST: quadtree, k-d tree va radix tree](#2317-sp-gist-quadtree-k-d-tree-va-radix-tree)
- [23.18 B-tree ichida: deduplication va suffix truncation](#2318-b-tree-ichida-deduplication-va-suffix-truncation)
- [23.19 Operator class tanlov sifatida: `text_pattern_ops`, collation va `LIKE` prefiksi](#2319-operator-class-tanlov-sifatida-text_pattern_ops-collation-va-like-prefiksi)
- [23.20 Korrelyatsiya: bir xil tanlanuvchanlik, boshqa narx](#2320-korrelyatsiya-bir-xil-tanlanuvchanlik-boshqa-narx)
- [23.21 GIN qidiruvi: leksema chastotasi, majburiy bitmap va `gin_fuzzy_search_limit`](#2321-gin-qidiruvi-leksema-chastotasi-majburiy-bitmap-va-gin_fuzzy_search_limit)
- [23.22 BRIN ni sozlash: `pages_per_range`, `autosummarize` va qo'lda summarizatsiya](#2322-brin-ni-sozlash-pages_per_range-autosummarize-va-qolda-summarizatsiya)
- [23.23 Amalda qo'llash](#2323-amalda-qollash)

</details>



Indeks so'rovni tezlashtiradigan sehr emas, balki ma'lumotning ikkinchi, tartiblangan nusxasi. Har bir indeks o'qishni tezlashtirgani uchun yozishdan, diskdan va vacuum vaqtidan to'lov oladi. Arxitektor uchun savol "indeks qo'shaylikmi" emas, balki "qaysi tur, qaysi ustunlar tartibida, qanday shart bilan va qaysi so'rovni qoplash uchun". Bu bobda PostgreSQL 15-17 dagi indeks turlarining ichki mexanikasi, ularning narxi va tanlov mezonlari ko'rib chiqiladi.

## 23.1 B-tree tuzilishi va u qaysi so'rovlarga yordam beradi

PostgreSQL ning standart indeksi B-tree, aniqrog'i B+tree ning Lehman-Yao variantidir. Daraxt 8 KB li sahifalardan iborat: yuqorida root, o'rtada internal sahifalar, pastda leaf sahifalar. Faqat leaf sahifalarda heap ga ko'rsatkichlar, ya'ni TID lar saqlanadi, va leaf qatlami ikki tomonlama bog'langan ro'yxat bo'lib, shu sababli oraliq bo'yicha skanlash bitta yo'nalishda ketma-ket boradi.

Chuqurlik juda sekin o'sadi. Taxminan 100 million qatorli `bigint` kalit uchun daraxt 4 qatlamdan oshmaydi va yuqori qatlamlar deyarli doim `shared_buffers` da yotadi.

B-tree quyidagilarga yordam beradi: `=`, `<`, `>`, `BETWEEN`, `IN`, `IS NULL`, `ORDER BY` uchun tayyor tartib, `MIN`/`MAX`, merge join, va unique constraint. U yordam bermaydigan holatlar: `LIKE '%mato%'` kabi prefiksi yo'q qidiruv, ustun ustida funksiya chaqirilgan shart, va jadvalning katta ulushini qaytaradigan so'rov. Oxirgi holatda planner ataylab seq scan ni tanlaydi, chunki random IO ketma-ket o'qishdan qimmatroq. Bu yerda aniq foiz chegarasi yo'q: seq scan narxi selektivlikka bog'liq emas, index scan narxi esa selektivlik oshgani sari o'sadi, shuning uchun ma'lum ulushdan keyin seq scan ustun chiqadi, chegara esa korrelyatsiyaga, `effective_cache_size` ga va index-only scan mumkinligiga bog'liq (Rogov, 20.5, 348-349-betlar). Qiyoslashning to'liq yozuvi [skan turlari bo'limida](24-planner-statistika-va-explain-analyze-oqish.md#244-skan-turlari-sequential-index-index-only-bitmap-heap-scan), korrelyatsiyaning narxga ta'siri esa [quyida](#2320-korrelyatsiya-bir-xil-tanlanuvchanlik-boshqa-narx).

```sql
-- buyurtmalar jadvali: taxminan 80 mln qator
CREATE TABLE orders (
    id           bigserial PRIMARY KEY,
    customer_id  bigint      NOT NULL,
    status       text        NOT NULL,   -- NEW, PAID, SHIPPED, CANCELLED
    total_amount numeric(14,2) NOT NULL,
    created_at   timestamptz NOT NULL DEFAULT now()
);

-- status past kardinallikda: PG 13 dan boshlab deduplication
-- bir xil kalitlarni bitta posting list ga yig'adi va indeksni kichraytiradi
CREATE INDEX idx_orders_status ON orders (status);

EXPLAIN (ANALYZE, BUFFERS)
SELECT id, total_amount FROM orders WHERE created_at > now() - interval '1 day';
```

## 23.2 Ko'p ustunli indeks va ustunlar tartibining ahamiyati

Ko'p ustunli B-tree da tartib hal qiluvchi. Indeks `(a, b, c)` kalitlari leksikografik tartibda saqlanadi, shuning uchun u faqat chapdan boshlangan prefiks uchun samarali: `a`, keyin `a, b`, keyin `a, b, c`. Agar so'rovda `a` bo'yicha shart bo'lmasa, PostgreSQL indeksni butunlay skanlashi mumkin, lekin bu seq scan dan kam farq qiladi, chunki tanlab o'tish imkoniyati yo'qoladi.

Amaliy qoida: tenglik shartidagi ustunlar oldinda, oraliq yoki tartiblash ustuni oxirida. Mijoz kabinetidagi "oxirgi 20 buyurtma" so'rovi uchun `(customer_id, created_at DESC)` to'g'ri tartib. Teskari tartib `(created_at, customer_id)` da planner avval sana oralig'ini oladi, keyin har bir qatorni mijoz bo'yicha filtrlaydi, ya'ni ortiqcha minglab heap o'qish paydo bo'ladi.

Ikkinchi mezon: ustun soni. Har bir qo'shimcha ustun indeks qatorini kengaytiradi va leaf sahifaga sig'adigan kalit sonini kamaytiradi. To'rt va undan ko'p ustunli indeks ko'pincha foydasini oqlamaydi, chunki yozuv narxi hamma so'rovga tegadi, tezlik esa bittasiga.

```sql
-- noto'g'ri: created_at oldinda, customer_id filtrga tushadi
CREATE INDEX idx_bad ON orders (created_at DESC, customer_id);

-- to'g'ri: tenglik oldinda, tartiblash oxirida
CREATE INDEX idx_good ON orders (customer_id, created_at DESC);

-- bu so'rov idx_good bilan 20 ta leaf qatorini o'qib to'xtaydi,
-- idx_bad bilan esa butun kunlik oraliqni skanlaydi
SELECT id, status, total_amount
FROM orders
WHERE customer_id = 48213
ORDER BY created_at DESC
LIMIT 20;
```

Uchinchi mezon ustunlarning emas, TARTIBNING o'zi. Bitta ustunli indeksda yo'nalish ahamiyatsiz, chunki uni ikki tomonga ham skanlash mumkin; ko'p ustunli indeksda esa yo'nalish muhim bo'lib qoladi. `(a, b)` indeksi `ORDER BY a, b` ni ham, `ORDER BY a DESC, b DESC` ni ham to'liq qoplaydi (ikkinchisi teskari skan bilan), lekin `ORDER BY a ASC, b DESC` ni qoplamaydi: indeks qisman tartiblangan ma'lumot beradi va reja ustiga `Incremental Sort` qo'yiladi (Rogov, 25.4, 440-bet). Aralash yo'nalish kerak bo'lsa, u indeks ta'rifining o'zida yoziladi.

`NULL` larning joyi ham shu qatorga kiradi. Standart holatda `NULL` saralash uchun oddiy qiymatlardan "katta" hisoblanadi, ya'ni o'sish tartibida daraxtning o'ng tomonida, kamayish tartibida chap tomonida turadi; joyni `NULLS FIRST` va `NULLS LAST` bilan o'zgartirish mumkin (Rogov, 25.4, 441-bet). So'rovda `NULLS FIRST` turib, indeksda turmasa, reja `Sort` node qo'yadi va `LIMIT` ning foydasi yo'qoladi.

```sql
-- So'rov: ORDER BY passenger_name NULLS FIRST, book_ref DESC
-- Mos kelmaydigan indeks: reja Gather Merge ustida Sort qo'yadi
CREATE INDEX idx_name_bref ON tickets (passenger_name, book_ref);

-- Mos indeks: Index Scan, saralash yo'q
CREATE INDEX idx_name_bref_2
    ON tickets (passenger_name NULLS FIRST, book_ref DESC);
```

Tenglik va oraliq farqi indeksdan tashqarida ham davom etadi va bu join rejasiga tegadi: merge join faqat tenglik operatorini qo'llaydi, ya'ni u faqat equi-join uchun ishlaydi (Rogov, 23.1, 388-bet). Demak `BETWEEN` yoki `<` kabi oraliq shartli join uchun indeks skanni tezlashtiradi, lekin merge join variantini ochmaydi; join algoritmlarining to'liq tanlovi [planner bobida](24-planner-statistika-va-explain-analyze-oqish.md#245-join-algoritmlari-nested-loop-hash-join-merge-join-va-qachon-qaysi-biri-tanlanadi).

## 23.3 Qamrab oluvchi indeks (`INCLUDE`) va index-only scan sharti

`INCLUDE` PostgreSQL 11 dan beri mavjud va indeksga qidiruv kaliti bo'lmagan ustunlarni qo'shadi. Bu ustunlar faqat leaf sahifalarda yotadi, daraxt tartibiga qatnashmaydi va `ORDER BY` uchun ishlatilmaydi. Maqsadi bitta: so'rov qaytaradigan hamma ustun indeksda bo'lsa, PostgreSQL heap ga bormasdan javob beradi, ya'ni index-only scan bajariladi.

Lekin index-only scan ning ikkinchi sharti bor va ko'pchilik shuni e'tiborsiz qoldiradi: visibility map da tegishli sahifa all-visible deb belgilangan bo'lishi kerak. Yangi yozilgan yoki yangilangan sahifalar uchun bu belgi yo'q, shuning uchun vacuum ishlamagan jadvalda index-only scan amalda heap fetch ga aylanadi. `EXPLAIN (ANALYZE, BUFFERS)` chiqishidagi `Heap Fetches: 0` yagona ishonchli dalil.

Unique indeksda `INCLUDE` ayniqsa foydali, chunki unikallik faqat kalit ustunlar bo'yicha tekshiriladi, qolgan ustunlar esa yuk sifatida boradi.

```sql
-- hisobot so'rovi faqat shu uch ustunni qaytaradi
CREATE INDEX idx_orders_cust_covering
    ON orders (customer_id, created_at DESC)
    INCLUDE (status, total_amount);

-- Heap Fetches: 0 bo'lsagina index-only scan haqiqatan ishlagan
EXPLAIN (ANALYZE, BUFFERS)
SELECT created_at, status, total_amount
FROM orders
WHERE customer_id = 48213
ORDER BY created_at DESC
LIMIT 50;

-- visibility map ni yangilash: aggressiv autovacuum yoki qo'lda
VACUUM (ANALYZE) orders;

-- unikallik faqat (tenant_id, email) bo'yicha, ism yuk sifatida
CREATE UNIQUE INDEX uq_users_email
    ON users (tenant_id, lower(email)) INCLUDE (full_name);
```

## 23.4 Qisman indeks (`WHERE` bilan) va uning amaliy foydasi

Qisman indeks jadvalning faqat bir qismini qamraydi. Eng kuchli qo'llanishi navbat jadvali: 80 million buyurtmaning faqat 20 mingtasi `NEW` holatida bo'lsa, `WHERE status = 'NEW'` sharti bilan qurilgan indeks taxminan 1 MB joy oladi, to'liq indeks esa 2 GB dan oshadi. Kichik indeks to'liq cache da yotadi va yozuv narxi ham deyarli nolga tushadi, chunki `PAID` holatiga o'tgan qator indeksdan chiqib ketadi.

Ikkinchi kuchli qo'llanishi shartli unikallik: "bitta foydalanuvchida faqat bitta aktiv karta bo'lsin" qoidasini `WHERE deleted_at IS NULL` sharti bilan unique indeks orqali ifodalash mumkin. Buni `CHECK` yoki application logikasi bilan ishonchli qilib bo'lmaydi.

Tuzoq shu yerda: planner qisman indeksni faqat so'rov sharti indeks shartidan kelib chiqishini isbotlay olsa ishlatadi. `status = 'NEW'` literal bilan ishlaydi, lekin JPA yuboradigan `status = $1` bind parameter bilan isbot tuzilmaydi va indeks e'tiborga olinmaydi. Shuning uchun qisman indeks shartini application so'rovida literal sifatida yozish yoki shartni `created_at > '2026-01-01'` kabi turg'un chegara bilan qurish kerak.

```sql
-- navbat: faqat qayta ishlanmagan buyurtmalar
CREATE INDEX idx_orders_queue
    ON orders (created_at)
    WHERE status = 'NEW';

-- shartli unikallik: o'chirilmagan kartalar orasida bitta primary
CREATE UNIQUE INDEX uq_card_primary
    ON payment_cards (customer_id)
    WHERE is_primary AND deleted_at IS NULL;

-- ombor qoldig'ining faqat muammoli qatorlari
CREATE INDEX idx_stock_negative
    ON stock_balance (warehouse_id, sku)
    WHERE quantity < 0;
```

## 23.5 Ifoda bo'yicha indeks va funksiya bilan qidirish

Ustun ustida funksiya chaqirilgan shart oddiy indeksni o'ldiradi, chunki indeksda `email` yotadi, so'rov esa `lower(email)` ni so'raydi. Yechim ifoda bo'yicha indeks: indeks kaliti sifatida ifodaning o'zi saqlanadi. Shart bitta, ifoda `IMMUTABLE` bo'lishi kerak, ya'ni bir xil kirish uchun doim bir xil natija bersin.

Shu sababli `date_trunc('day', created_at)` ni `timestamptz` ustida indekslash mumkin emas: natija session ning time zone sozlamasiga bog'liq, demak funksiya `STABLE`, `IMMUTABLE` emas. Bu holatda kundalik agregatsiya uchun oddiy `created_at` indeksini qurib, so'rovni yarim ochiq oraliqqa aylantirish to'g'ri yo'l.

Qo'shimcha foyda: ifoda bo'yicha indeks qurilganda `ANALYZE` shu ifoda uchun alohida statistika yig'adi. `jsonb` dan chiqarilgan `status` maydonining selektivligini planner shu statistikadan biladi, aks holda u qattiq kodlangan taxminni ishlatadi.

```sql
-- registratsiyada katta-kichik harf farqi bo'lmasin
CREATE UNIQUE INDEX uq_customer_email_ci
    ON customers (lower(email));
SELECT id FROM customers WHERE lower(email) = lower('Alisher@Mail.Uz');

-- jsonb payload ichidagi tashqi ID bo'yicha qidiruv
CREATE INDEX idx_payment_ext_id
    ON payments ((payload ->> 'external_id'));

-- date_trunc timestamptz ustida IMMUTABLE emas, shuning uchun
-- oraliq shartini ishlatamiz va oddiy indeks yetarli bo'ladi
CREATE INDEX idx_orders_created ON orders (created_at);
SELECT date_trunc('day', created_at) AS d, sum(total_amount)
FROM orders
WHERE created_at >= '2026-09-01' AND created_at < '2026-10-01'
GROUP BY 1;
```

## 23.6 GIN: massiv, `jsonb` va to'liq matn qidiruvi uchun

GIN teskari indeks: u qiymatni emas, qiymat ichidagi elementlarni kalit qilib oladi va har bir kalit uchun TID lar ro'yxatini saqlaydi. Shuning uchun u bitta ustunda ko'p elementli qiymat yotganda ishlaydi: massiv, `jsonb`, `tsvector`, va `pg_trgm` orqali trigrammalarga ajratilgan matn. Qo'llanadigan operatorlar `@>`, `?`, `?|`, `?&`, `&&` va to'liq matn uchun `@@`.

`jsonb` uchun ikki opclass bor. Standart `jsonb_ops` hamma kalit va qiymatni indekslaydi, shuning uchun `?` operatori ham ishlaydi, lekin hajmi katta. `jsonb_path_ops` faqat yo'l va qiymat hash ini saqlaydi, taxminan ikki barobar kichik va `@>` so'rovlarida tezroq, lekin kalit mavjudligini tekshiruvchi operatorlarni qo'llamaydi.

Hajm haqida ogohlik: `tsvector` ustidagi GIN jadval hajmining taxminan 20-40 foizini oladi va qurilishi B-tree dan bir necha barobar uzoq davom etadi, shuning uchun uni `maintenance_work_mem` ni kamida 1 GB qilib qo'ygan sessiyada qurish kerak.

GIN ning ikkita mexanik chegarasi to'liq matn qidiruvida sezilarli. Birinchisi: `tsvector` leksemaning pozitsiyasini saqlasa ham, bu ma'lumot indeksga tushmaydi, shuning uchun GIN ibora bo'yicha qidiruvni tezlashtira olmaydi. Ikkinchisi: GIN tartiblash operatorlarini qo'llamaydi, demak relevantlik bo'yicha tartiblashda `ts_rank` har bir natija qatori uchun alohida hisoblanadi. Ikkala chegarani `rum` kengaytmasi yopadi, lekin u yadro tarkibida emas va alohida o'rnatiladi; qidiruv sifati haqidagi qaror esa [PostgreSQL FTS ning qattiq chegaralari](40-qidiruv-postgresql-fts-va-alohida-dvigatel.md#403-postgresql-fts-ning-qattiq-chegaralari) bo'limida ko'riladi.

Mexanikaning muhim qismi: GIN da `fastupdate` yoqilgan va yangi yozuvlar avval pending list ga tushadi. Ro'yxat `gin_pending_list_limit` (standart 4 MB) ga yetganda yoki vacuum vaqtida asosiy tuzilmaga ko'chiriladi. Natijada ommaviy `INSERT` dan keyingi birinchi qidiruv kutilmaganda sekin bo'ladi, chunki u pending list ni ketma-ket o'qiydi. Yuqori yozuv oqimida `fastupdate = off` qilish yoki pending limitni kamaytirish kerak bo'ladi.

```sql
CREATE EXTENSION IF NOT EXISTS pg_trgm;

-- to'lov payload i bo'yicha containment qidiruvi
CREATE INDEX idx_payments_payload
    ON payments USING gin (payload jsonb_path_ops);
SELECT id FROM payments WHERE payload @> '{"provider":"click"}';

-- mahsulot teglari massivi
CREATE INDEX idx_product_tags ON products USING gin (tags);
SELECT id FROM products WHERE tags && ARRAY['aksiya','yangi'];

-- ichki qidiruv: ILIKE '%...%' uchun yagona ishlaydigan variant
CREATE INDEX idx_products_name_trgm
    ON products USING gin (name gin_trgm_ops);
SELECT id, name FROM products WHERE name ILIKE '%simsiz quloqchin%';

-- yuqori yozuv oqimida pending list ni o'chirish
ALTER INDEX idx_payments_payload SET (fastupdate = off);
```

GIN ni yadrodan tashqaridagi turlarga kengaytiradigan uchta kengaytma bor va ular ko'pincha unutiladi. `intarray` butun sonlar massivi uchun `gin__int_ops` operator classini beradi: u standart `array_ops` ga juda o'xshaydi, lekin hujjatni qidiruv so'roviga solishtiradigan `@@` operatorini qo'llaydi. `hstore` kalit-qiymat saqlagichini va `gin_hstore_ops` ni beradi, bunda kalit ham, qiymat ham indekslanadi. `jsquery` esa `jsonb` uchun o'z so'rov tilini va GIN qo'llovini beradi, lekin kitob uni tavsiya qilmaydi: SQL/JSON standarti qabul qilinib PostgreSQL da SQL/JSON path tili amalga oshirilgandan keyin standart ichki imkoniyatlar yaxshiroq tanlov bo'lib ko'rinadi (Rogov, 28.6, 516-bet). Qidiruv tartibi, bitmap majburiyligi va natija sonini cheklash haqidagi qaror [GIN qidiruvining uch xossasi bo'limida](#2321-gin-qidiruvi-leksema-chastotasi-majburiy-bitmap-va-gin_fuzzy_search_limit).

## 23.7 GiST, matn o'xshashligi va oraliq turlar

GiST umumlashgan qidiruv daraxti: har bir ichki tugun o'z farzandlarini qamrab oluvchi predikatni saqlaydi. Bu tuzilma lossy, ya'ni indeks faqat nomzod qatorlarni qaytaradi va yakuniy tekshiruv heap da bajariladi. Shuning uchun GiST tenglik qidiruvida B-tree dan sekin, lekin u B-tree ifodalay olmaydigan munosabatlarni ifodalaydi: kesishish, qamrash, masofa.

Arxitektor uchun eng qimmatli qo'llanishi exclusion constraint. "Bitta xonaga ustma-ust tushgan ikki bron bo'lmasin" yoki "bitta mahsulotning narx amal qilish davrlari kesishmasin" qoidasini `tstzrange` va `&&` operatori bilan baza darajasida majburlash mumkin. Skalyar ustunni (xona ID si) oraliq bilan bitta constraint ga qo'shish uchun `btree_gist` kengaytmasi kerak.

Ikkinchi qo'llanishi KNN tartiblash: `ORDER BY name <-> 'qidiruv matni' LIMIT 10` so'rovi GiST da indeks orqali bajariladi va "eng o'xshash 10 ta" javobini butun jadvalni saralamasdan beradi. GIN bunday tartiblashni qo'llamaydi, shuning uchun o'xshashlik reytingi kerak bo'lsa GiST tanlanadi.

```sql
CREATE EXTENSION IF NOT EXISTS btree_gist;

-- narx amal qilish davrlari kesishmasligi kafolati
ALTER TABLE price_periods
    ADD CONSTRAINT no_overlap_price
    EXCLUDE USING gist (product_id WITH =, valid_period WITH &&);

-- ombor bronlari uchun ham shu yondashuv
ALTER TABLE reservations
    ADD CONSTRAINT no_overlap_slot
    EXCLUDE USING gist (warehouse_id WITH =, period WITH &&)
    WHERE (status <> 'CANCELLED');

-- o'xshashlik bo'yicha tartiblash: GiST, GIN emas
CREATE INDEX idx_customers_name_gist
    ON customers USING gist (full_name gist_trgm_ops);
SELECT id, full_name
FROM customers
ORDER BY full_name <-> 'alisher navoiev'
LIMIT 10;
```

## 23.8 BRIN: katta, tartibli jadvallar uchun arzon indeks

BRIN qator emas, blok oraliqlarini indekslaydi. Har `pages_per_range` sahifa (standart 128, ya'ni 1 MB) uchun u shu oraliqdagi minimal va maksimal qiymatni saqlaydi. Natijada indeks hayratlanarli kichik: 300 GB li audit log jadvali uchun `created_at` ustida BRIN taxminan bir necha MB joy oladi, xuddi shu ustundagi B-tree esa 8 GB dan oshadi.

BRIN lossy indeks: u mos kelishi mumkin bo'lgan blok oraliqlarini qaytaradi, keyin har bir qator heap da qayta tekshiriladi. Shuning uchun u nuqtali qidiruv uchun emas, kunlik yoki oylik oraliq bo'yicha agregatsiya uchun mo'ljallangan.

Shart bitta va qattiq: jadvalning fizik tartibi ustun qiymati bilan korrelyatsiya qilishi kerak. Append-only log, `created_at` yoki `bigserial` ID buni tabiiy beradi. Korrelyatsiyani `pg_stats.correlation` dan tekshirish mumkin, qiymat 1 ga yaqin bo'lsa BRIN ishlaydi, 0 ga yaqin bo'lsa foydasiz. Ko'p `UPDATE` bo'ladigan jadvalda tartib buziladi va BRIN sekin asta o'z ma'nosini yo'qotadi.

PostgreSQL 14 dan `minmax_multi` opclass bor: u bitta oraliq uchun bir nechta chegara to'plamini saqlaydi, shuning uchun bir nechta chetlab ketgan qiymat butun oraliqni buzmaydi. `bloom` opclass esa korrelyatsiyasiz ustunda tenglik qidiruvi uchun ishlaydi. Yangi sahifalarni avtomatik umumlashtirish uchun `autosummarize = on` yoqiladi, lekin uning standarti o'chiq va narxi bor: `pages_per_range`, `autosummarize` va qo'lda summarizatsiya tanlovi [BRIN ni sozlash bo'limida](#2322-brin-ni-sozlash-pages_per_range-autosummarize-va-qolda-summarizatsiya).

```sql
-- audit log: append-only, 300 GB, kunlik oraliq so'rovlari
CREATE TABLE audit_log (
    id         bigserial,
    entity     text        NOT NULL,
    payload    jsonb,
    created_at timestamptz NOT NULL DEFAULT now()
);

CREATE INDEX idx_audit_created_brin
    ON audit_log USING brin (created_at)
    WITH (pages_per_range = 64, autosummarize = on);

-- korrelyatsiya 1 ga yaqin bo'lsagina foyda bor
SELECT attname, correlation
FROM pg_stats
WHERE tablename = 'audit_log' AND attname = 'created_at';

-- oraliq so'rov: BRIN nomzod bloklarni beradi, heap recheck qiladi
EXPLAIN (ANALYZE, BUFFERS)
SELECT count(*) FROM audit_log
WHERE created_at >= '2026-10-01' AND created_at < '2026-10-02';
```

| Holat | Mos indeks turi | Sabab |
|---|---|---|
| ID yoki kod bo'yicha nuqtali qidiruv | B-tree | eng kichik latency, unikallikni ham beradi |
| Sana oralig'i va `ORDER BY ... LIMIT` | B-tree | tartib tayyor, saralash kerak emas |
| Jadvalning 1 foizi qiziq (navbat) | Qisman B-tree | indeks kichik, cache da, yozuv narxi past |
| `lower(email)`, `payload ->> 'id'` | Ifoda bo'yicha B-tree | so'rov ifodasi indeks kaliti bilan bir xil |
| `jsonb @>`, massiv `&&` | GIN | elementlar bo'yicha teskari ro'yxat |
| `ILIKE '%matn%'` | GIN + `gin_trgm_ops` | trigramma bo'yicha nomzodlar |
| To'liq matn qidiruvi `@@` | GIN + `tsvector` | leksemalar bo'yicha indeks |
| O'xshashlik reytingi `<->` | GiST + `gist_trgm_ops` | KNN tartiblashni qo'llaydi |
| Oraliqlar kesishmasligi | GiST exclusion | `&&` operatori faqat GiST da |
| 100 GB dan katta append-only log | BRIN | hajmi MB larda, oraliq so'rovga yetarli |
| Yuqori kardinallik va tez `UPDATE` | B-tree | BRIN korrelyatsiyani yo'qotadi |

## 23.9 Indeks narxi: yozuv sekinlashuvi, disk, vacuum yuki

Har bir `INSERT` jadvalga bitta, indekslarga esa har biriga bittadan yozuv qo'shadi. Bu yozuvlar WAL ga ham tushadi, va agar sahifa checkpoint dan keyin birinchi marta o'zgarsa, WAL ga butun sahifa tasviri yoziladi. Taxminan har bir qo'shimcha indeks insert-og'ir jadvalda 5 dan 15 foizgacha sekinlashuv beradi, sakkiz indeksli jadvalda yozuv latency si indekssiz holatga nisbatan ikki barobarga chiqishi normal.

Ikkinchi, ko'rinmas narx HOT update ni buzish. PostgreSQL yangilangan ustun hech bir indeksda qatnashmasa, yangi versiyani o'sha sahifada qoldiradi va indekslarga tegmaydi. Bu HOT update deyiladi. Agar siz tez-tez o'zgaradigan `last_seen_at` yoki `status` ustuniga indeks qo'ysangiz, har bir `UPDATE` hamma indeksga yangi yozuv qo'shadi, bloat tezlashadi, vacuum ko'proq ishlaydi.

Uchinchi narx vacuum ning o'zi. Vacuum har bir indeksni ko'rib chiqadi, demak uning davomiyligi indekslar soniga chiziqli bog'liq va ortiqcha indekslar wraparound xavfini yaqinlashtiradi.

| Jihat | Oddiy yondashuv | Arxitektor yondashuvi |
|---|---|---|
| Indeks qo'shish qarori | Sekin so'rov ko'rindi, indeks qo'shildi | `EXPLAIN (ANALYZE, BUFFERS)` o'qiladi, mavjud indeks kengaytiriladi |
| Ustunlar tartibi | Yozilish tartibida | Tenglik oldinda, oraliq va `ORDER BY` oxirida |
| Qamrov | Har bir so'rovga alohida indeks | Bitta `INCLUDE` li indeks bir nechta so'rovni qoplaydi |
| Hajm | Butun jadval indekslanadi | `WHERE` sharti bilan faqat kerakli qism |
| Katta log jadvali | `created_at` ustida B-tree | BRIN, korrelyatsiya o'lchangandan keyin |
| `jsonb` qidiruv | Har bir maydonga alohida indeks | Bitta GIN, kerak bo'lsa `jsonb_path_ops` |
| Ishlab chiqarishga chiqarish | Oddiy `CREATE INDEX`, jadval bloklanadi | `CONCURRENTLY`, `lock_timeout`, uzun tranzaksiyalar tekshiriladi |
| Eskirgan indeks | Hech kim tegmaydi | `pg_stat_user_indexes` choraklik ko'rikda, replikalar ham |
| Shishish | Sezilganda `REINDEX`, jadval bloklanadi | `pgstatindex` bilan o'lchash, `REINDEX CONCURRENTLY` |
| O'lchov | "Tez bo'ldi shekilli" | p95 latency va indeks hajmi dashboard da kuzatiladi |

## 23.10 Keraksiz indekslarni topish va o'chirish (`pg_stat_user_indexes`)

`pg_stat_user_indexes` har bir indeks bo'yicha `idx_scan` hisoblagichini beradi. Nol yoki juda kichik qiymat indeks ishlatilmayotganini bildiradi, lekin ikki shartni esdan chiqarmaslik kerak. Birinchisi: statistika `pg_stat_reset` yoki major upgrade dan beri yig'iladi, shuning uchun `pg_stat_database.stats_reset` sanasini ko'rib, kamida bir necha hafta, hisobot mavsumini qamrab oluvchi muddat kutish kerak. PostgreSQL 16 dan `last_idx_scan` ustuni bor va u qarorni ancha osonlashtiradi.

Ikkinchi shart ko'pincha xatolikka olib keladi: statistika har bir instansda alohida yig'iladi. Agar hisobot so'rovlari read replica ga yuborilsa, primary da `idx_scan = 0` bo'lgan indeks replika da faol ishlatilayotgan bo'lishi mumkin. Qarorni hamma instansdan yig'ilgan ma'lumot bilan qabul qilish kerak.

Unique yoki constraint ortidagi indeksni va foreign key ustunidagi indeksni skanlanmagani uchun o'chirmang: birinchisi qoidani majburlaydi, ikkinchisi ota jadvaldagi `DELETE` ni tezlashtiradi. PostgreSQL da MySQL dagi "invisible index" yo'q, shuning uchun xavfsiz tekshiruv usuli `hypopg` kengaytmasi yoki tranzaksiya ichida `DROP INDEX` qilib, planni ko'rib, `ROLLBACK` qilish.

```sql
-- ishlatilmayotgan va katta indekslar
SELECT s.relname AS tbl, s.indexrelname AS idx, s.idx_scan,
       pg_size_pretty(pg_relation_size(s.indexrelid)) AS size
FROM pg_stat_user_indexes s
JOIN pg_index i ON i.indexrelid = s.indexrelid
WHERE s.idx_scan < 50
  AND NOT i.indisunique
  AND NOT i.indisprimary
  AND pg_relation_size(s.indexrelid) > 50 * 1024 * 1024
ORDER BY pg_relation_size(s.indexrelid) DESC;

-- statistika qachondan yig'ilgan
SELECT datname, stats_reset FROM pg_stat_database WHERE datname = current_database();

-- takrorlangan indekslar: bir xil ustun to'plami
SELECT indrelid::regclass AS tbl, count(*), array_agg(indexrelid::regclass)
FROM pg_index
GROUP BY indrelid, indkey
HAVING count(*) > 1;
```

## 23.11 `CREATE INDEX CONCURRENTLY` va ishlab chiqarishda indeks qo'shish

Oddiy `CREATE INDEX` jadvalga `SHARE` lock oladi va butun qurilish davomida `INSERT`, `UPDATE`, `DELETE` ni to'xtatadi. 80 million qatorli jadvalda bu bir necha daqiqa to'liq to'xtash degani. `CONCURRENTLY` esa `SHARE UPDATE EXCLUSIVE` lock bilan ishlaydi, DML ni to'xtatmaydi, lekin jadvalni ikki marta skanlaydi va taxminan ikki barobar uzoq davom etadi.

Ikki muhim cheklov bor. Birinchisi: `CONCURRENTLY` tranzaksiya blokida bajarilmaydi. Flyway har bir migratsiyani tranzaksiyada ishlatadi, shuning uchun bunday migratsiyani Java migratsiyasi sifatida yozib, `canExecuteInTransaction()` dan `false` qaytarish kerak. Liquibase da `runInTransaction="false"` atributi bor. Ikkinchisi: qurilish o'zidan oldin boshlangan hamma tranzaksiya tugashini kutadi, shuning uchun soatlab ochiq turgan analitik tranzaksiya indeks qurilishini cheksiz kechiktiradi.

Xato bo'lsa `CONCURRENTLY` jadvalda yaroqsiz indeks qoldiradi. U so'rovlarda ishlatilmaydi, lekin yozuv narxini oladi va vacuum ni sekinlashtiradi, shuning uchun uni topib o'chirish shart. Partition qilingan jadvalda ota jadval ustida `CONCURRENTLY` qo'llanmaydi: har bir partitionda alohida quriladi, keyin ota jadvalda `ONLY` bilan indeks yaratilib, `ATTACH PARTITION` orqali bog'lanadi.

```sql
-- qurishdan oldin uzun tranzaksiyalarni tekshirish
SELECT pid, now() - xact_start AS xact_age, left(query, 50)
FROM pg_stat_activity
WHERE now() - xact_start > interval '5 min';

-- quruvchi sessiya uchun resurs va navbat sozlamalari
SET maintenance_work_mem = '2GB';
SET max_parallel_maintenance_workers = 4;
SET lock_timeout = '5s';

CREATE INDEX CONCURRENTLY idx_orders_cust_created
    ON orders (customer_id, created_at DESC);

-- yaroqsiz qolgan indekslarni topish va tozalash
SELECT indexrelid::regclass FROM pg_index WHERE NOT indisvalid;
DROP INDEX CONCURRENTLY IF EXISTS idx_orders_cust_created;
```

## 23.12 Indeks shishishi va `REINDEX CONCURRENTLY`

B-tree indeks o'chirilgan qatorlarni darhol bo'shatmaydi: leaf sahifadagi joy faqat vacuum indeks yozuvini olib tashlagandan keyin qayta ishlatiladi. Tasodifiy kalit bo'yicha yozuv, masalan UUID v4 primary key, sahifa bo'linishlarini ko'paytiradi va indeksni parchalaydi. Shu sababli yangi loyihalarda vaqt bo'yicha o'sadigan kalit, ya'ni UUID v7 yoki ULID, yoki `bigserial` tanlanadi.

Shishishni taxmin qilmasdan o'lchash kerak. `pgstattuple` kengaytmasidagi `pgstatindex` funksiyasi `avg_leaf_density` va `leaf_fragmentation` qiymatlarini beradi. Sog'lom B-tree da leaf zichligi taxminan 70-90 foiz, 40 foizdan past qiymat qayta qurish vaqti kelganini ko'rsatadi.

`REINDEX CONCURRENTLY` PostgreSQL 12 dan beri mavjud va indeksni DML ni to'xtatmasdan qayta quradi. Uchta narsani hisobga olish kerak. Birinchisi: vaqtincha ikkinchi nusxa quriladi, demak disk da indeks hajmidan ko'proq bo'sh joy kerak. Ikkinchisi: xato bo'lsa `_ccnew` qo'shimchali yaroqsiz indeks qoladi va uni tozalash lozim. Uchinchisi: exclusion constraint ortidagi indeksni `CONCURRENTLY` qayta qurib bo'lmaydi, u uchun xizmat oynasi kerak. Append-only jadvalda `fillfactor = 100` qo'yish indeksni zichlashtiradi, tez-tez yangilanadigan jadvalda esa standart 90 qoldiriladi.

```sql
CREATE EXTENSION IF NOT EXISTS pgstattuple;

-- shishishni o'lchash: zichlik 40 foizdan past bo'lsa qayta qurish kerak
SELECT avg_leaf_density, leaf_fragmentation, index_size
FROM pgstatindex('idx_orders_cust_created');

-- DML ni to'xtatmasdan qayta qurish
REINDEX INDEX CONCURRENTLY idx_orders_cust_created;

-- yarim qolgan nusxalarni topish
SELECT indexrelid::regclass FROM pg_index
WHERE NOT indisvalid AND indexrelid::regclass::text LIKE '%_ccnew%';
```

| Tuzoq | Nima bo'ladi | Yechim |
|---|---|---|
| `INCLUDE` qo'yildi, lekin vacuum yo'q | Index-only scan ishlamaydi, `Heap Fetches` katta | Autovacuum ni agressivlashtirish, `Heap Fetches: 0` ni tekshirish |
| Qisman indeks sharti bind parameter bilan | Planner isbot tuzmaydi, indeks tashlanadi | Shartni literal yozish yoki turg'un chegara qo'yish |
| Tez o'zgaradigan ustunga indeks | HOT update buziladi, bloat o'sadi | Indeksni olib tashlash yoki ustunni alohida jadvalga chiqarish |
| BRIN uncorrelated ustunda | Deyarli butun jadval qayta tekshiriladi | `pg_stats.correlation` ni o'lchash, B-tree ga o'tish |
| GIN ga ommaviy `INSERT` | Pending list o'sadi, birinchi qidiruv sekin | `fastupdate = off` yoki `gin_pending_list_limit` ni kamaytirish |
| `CONCURRENTLY` uzun tranzaksiya paytida | Qurilish soatlab kutadi yoki uziladi | `pg_stat_activity` tekshiruvi, keyin qayta urinish |
| Yaroqsiz indeks e'tibordan chetda | Yozuv sekin, vacuum og'ir, foyda yo'q | `pg_index.indisvalid` monitoringi, `DROP INDEX CONCURRENTLY` |
| `idx_scan = 0` deb primary da o'chirildi | Replika dagi hisobot sekinlashadi | Hamma instansdan statistika yig'ish |
| UUID v4 primary key | Sahifa bo'linishi, indeks parchalanishi | UUID v7 yoki `bigserial` ga o'tish |

## 23.13 Saqlash dvigateli oilalari: B-tree va LSM, o'qish va yozish kuchayishi

PostgreSQL indekslari B-tree asosida ishlaydi, lekin boshqa saqlash dvigatellari boshqa tanlov qiladi va bu tanlov ma'lumot bazasini tanlashda ko'rinadi. Shuning uchun ikki oilaning farqini bilish kerak: u "qaysi baza tez" degan savolga emas, "qaysi yuk uchun qaysi baza" degan savolga javob beradi.

B-tree yozuvni **joyida** o'zgartiradi: sahifa topiladi, o'qiladi, o'zgartiriladi va qaytib yoziladi. LSM (log-structured merge) esa yozuvni xotiradagi tartiblangan tuzilmaga qo'yadi, u to'lganda diskka ketma-ket yozadi va keyin fon jarayoni fayllarni birlashtiradi (compaction). PostgreSQL ning WAL i ham ketma-ket yozadi, lekin ma'lumot fayllari baribir joyida o'zgaradi.

| O'lchov | B-tree | LSM |
|---|---|---|
| Yozish | tasodifiy I/O, sahifa to'liq yoziladi | ketma-ket I/O, keyin compaction |
| O'qish | bitta yo'l, barqaror kechikish | bir necha qatlam, Bloom filtri bilan tezlashtiriladi |
| Yozish kuchayishi | sahifa darajasida | compaction hisobiga, umumiy hajmi kattaroq |
| Bo'sh joy | sahifalarda bo'shliq (bloat) | tiqizroq, lekin compaction vaqtincha joy oladi |
| Kechikish barqarorligi | ancha barqaror | compaction paytida cho'qqi |

Ikki atama shu yerdan chiqadi va ikkisi ham o'lchanadi. Yozish kuchayishi (write amplification) - bitta mantiqiy yozuv diskka necha bayt bo'lib tushishi; o'qish kuchayishi (read amplification) - bitta so'rov necha marta diskka borishi. PostgreSQL da yozish kuchayishining o'ziga xos manbasi bor: qator o'zgarganda yangi versiya yoziladi va unga tegishli hamma indeks ham yangilanadi, shuning uchun ortiqcha indeks yozishni ham sekinlashtiradi. Buning yumshatuvchisi HOT update: o'zgargan ustun hech bir indeksda bo'lmasa, indekslar yangilanmaydi.

Amaliy xulosa: yozuv og'ir va kalit bo'yicha oddiy qidiruvli yuk (metrika, hodisa jurnali, vaqt qatori) LSM asosidagi tuzilmaga mos keladi; murakkab so'rov, join, tranzaksiya va barqaror kechikish kerak bo'lsa B-tree asosidagi relyatsion baza mos. Bu tanlov [texnologiya tanlash mezonlari](38-doimiy-organish-va-texnologiya-tanlash.md#384-yangi-kutubxonani-baholash-mezonlari-qollab-quvvatlash-bogliqlik-chiqish-yoli) bilan birga qilinadi va ko'p holatda PostgreSQL ikkisiga ham yetadi.

## 23.14 Indeks interfeysi: `pg_am`, operator class va operator family

PostgreSQL yadrosida oltita indeks access method bor: `btree`, `hash`, `gist`, `gin`, `spgist` va `brin`. Kengaytiriluvchanlik yadroni o'zgartirmasdan yangi usul qo'shishga imkon beradi va standart modullar to'plamidagi `bloom` indeksi shunga misol.

Har qanday turdagi indeks oxir-oqibat kalitni heap tuple lariga bog'laydi va olti baytli TID qaytaradi. Qolgan ishni umumiy indexing engine bajaradi: TID bo'yicha heap dan o'qiydi, tuple ni snapshotga qarab ko'rinuvchanlikka tekshiradi va access method ning javobi qat'iy bo'lmasa shartni qayta tekshiradi. Aynan shu qayta tekshirish rejada `Recheck Cond` bo'lib ko'rinadi.

Access method yangi ma'lumot turi haqida oldindan hech narsa bilmaydi, shuning uchun u o'z interfeysini ochadi. Turni indeks bilan bog'laydigan operatorlar va yordamchi funksiyalar to'plami operator class deb ataladi va `pg_opclass` da yashaydi. Har bir tur uchun bitta class standart deb belgilanadi, shuning uchun odatdagi buyruq qisqartma bo'lib chiqadi.

```sql
-- Bu ikki buyruq bir xil indeksni yaratadi
CREATE INDEX ON mijozlar (email);
CREATE INDEX ON mijozlar USING btree (email text_ops);

-- text uchun mavjud B-tree classlari va qaysi biri standart
SELECT opcname, opcdefault
FROM pg_am am JOIN pg_opclass opc ON opcmethod = am.oid
WHERE amname = 'btree' AND opcintype = 'text'::regtype;

-- Mavjud access method lar ro'yxati
SELECT amname FROM pg_am WHERE amtype = 'i';
```

Har bir operator class operator family ga tegishli, family esa bir xil semantikadagi turlarni birlashtiradi: `integer_ops` ga `int2_ops`, `int4_ops` va `int8_ops` kiradi, `datetime_ops` ga `date_ops`, `timestamp_ops` va `timestamptz_ops`. Buning amaliy ma'nosi katta: family tufayli planner turlari har xil bo'lgan shartda ham indeksni ishlata oladi va cast qo'shishga majbur emas.

Bundan aniq qoida chiqadi: entity maydonining turi ustun turiga mos kelmasa va ikki tur bitta family da bo'lmasa, solishtirishda cast paydo bo'ladi va indeks ishlamay qolishi mumkin. Hibernate bunday nomuvofiqlikni jim yutadi, chunki JDBC darajasida konvertatsiya bajariladi. `EXPLAIN` da buni `Index Cond` o'rniga `Filter` satri paydo bo'lishidan yoki shartdagi `::` belgisidan bilish mumkin, shuning uchun migratsiya ko'rigida entity turi bilan ustun turi solishtiriladi.

## 23.15 Indeks xossalari: qaysi tur nimani qo'llaydi

Reja tuzishdan oldin planner access method nimani qo'llashini bilishi kerak: natijani tartiblangan holda qaytara oladimi, index-only scan mumkinmi, bitmap qura oladimi. Bu ma'lumot interfeysda uch darajada e'lon qilinadi va uchta funksiya bilan so'raladi. Ajratish kelajak uchun qilingan: hozircha bitta access method ga asoslangan hamma indeks birinchi ikki darajada bir xil xossaga ega.

```sql
-- Access method darajasi: tur umuman nimani qo'llaydi
SELECT p.name, pg_indexam_has_property(a.oid, p.name)
FROM pg_am a, unnest(array['can_order','can_unique','can_multi_col',
                           'can_exclude','can_include']) p(name)
WHERE a.amname = 'gin';

-- Indeks darajasi
SELECT p.name, pg_index_has_property('idx_buyurtma_sana', p.name)
FROM unnest(array['clusterable','index_scan','bitmap_scan',
                  'backward_scan']) p(name);

-- Ustun darajasi: returnable index-only scan imkonini bildiradi
SELECT p.name, pg_index_column_has_property('idx_buyurtma_sana', 1, p.name)
FROM unnest(array['orderable','distance_orderable','returnable',
                  'search_array','search_nulls']) p(name);
```

Bu uchta so'rov amalda ko'p bahsni yopadi. `can_order` faqat B-tree da rost, demak `ORDER BY` ni indeks bilan qoplash boshqa turlarda mumkin emas va reja baribir `Sort` node qo'yadi. `can_unique` ham faqat B-tree da, shuning uchun unikal cheklov boshqa turda qurilmaydi. `can_include`, ya'ni `INCLUDE` ustunlari qo'shish, hamma turda yo'q. `returnable` esa eng aniq savolga javob beradi: shu ustun bo'yicha index-only scan umuman mumkinmi.

Indeks darajasidagi to'rtta xossaning ma'nosi ko'pincha nomidan taxmin qilinadi va shu yerda xato chiqadi, shuning uchun ularni aniq ta'riflash kerak (Rogov, 19.3, 326-bet).

- **`clusterable`** heap tuple larini indeks skani qaytaradigan `TID` tartibida jismonan ko'chirish imkonini bildiradi, ya'ni shu indeks ustida `CLUSTER` buyrug'i qo'llanadimi yoki yo'q.
- **`index_scan`** indeks `TID` larni bittalab qaytara olishini bildiradi. Hamma indeks buni qila olmaydi va bu birinchi qarashda g'alati tuyuladi.
- **`bitmap_scan`** indeks hamma `TID` ni bir yo'la bitmap qilib qura olishini bildiradi.
- **`backward_scan`** natijani indeks yaratilgandagi tartibga teskari yo'nalishda qaytara olishni bildiradi va u faqat `index_scan` qo'llanganda ma'noga ega.

B-tree da to'rttasi ham rost (Rogov, 25.5, 442-bet), BRIN da esa faqat `bitmap_scan` rost: `clusterable`, `index_scan` va `backward_scan` yolg'on, chunki BRIN doim bitmap qaytaradi (Rogov, 29.6, 529-bet). Amaliy xulosa shundan chiqadi: `CLUSTER` ni BRIN ustida bajarib bo'lmaydi, `Index Scan` node ini BRIN rejasida hech qachon ko'rmaysiz, va GIN ham xuddi shunday faqat bitmap beradi.

Unikal indeks bilan unikal cheklov farqini ham shu yerda aytish kerak. Cheklov hech qachon buzilmasligi kerak bo'lgan xossani e'lon qiladi, indeks esa uni ta'minlaydigan mexanizm. Farq amaliy: partitsiyalangan jadvalda global indeks yo'q, lekin partition kalitini o'z ichiga olgan unikal cheklov qo'yish mumkin va global unikallikni har bir partition ning lokal indeksi ta'minlaydi.

JPA tomonida bundan ikki xulosa chiqadi. Birinchisi: `Pageable` bilan berilgan `Sort` ustuni B-tree indeksida bo'lishi shart, GIN yoki BRIN bu ishni bajarmaydi. Ikkinchisi: projection interfeysida faqat indeksdagi ustunlarni so'rash index-only scan uchun nomzod yaratadi, lekin faqat `returnable` rost bo'lgan tur uchun.

```java
public interface OrderSummary {
    Long getId();
    Instant getCreatedAt();
}

public interface OrderRepository extends JpaRepository<Order, Long> {

    // Faqat indeksdagi ustunlar: index-only scan uchun nomzod
    List<OrderSummary> findByCustomerIdOrderByCreatedAtDesc(Long customerId);
}
```

## 23.16 Hash indeks: qachon mantiqiy, qachon B-tree afzal

Hash indeks diskda saqlanadigan hash jadval. Kalitning hash funksiyasi hisoblanadi, uning quyi bitlari bucket raqamini beradi va bucket ga TID bilan birga kalitning hash kodi yoziladi. Kalitning o'zi saqlanmaydi, chunki kichik va qat'iy uzunlikdagi qiymat bilan ishlash qulayroq. Jadval dinamik kengayadi: minimal bucket soni ikkita, o'sish paytida bitta bucket ikkiga bo'linadi va elementlar faqat shu ikki bucket o'rtasida qayta taqsimlanadi.

Kalit saqlanmagani uchun kelib chiqadigan ikki oqibat bor. Birinchisi: hash to'qnashuvi sababli access method ortiqcha TID qaytarishi mumkin, shuning uchun natija heap da qayta tekshiriladi. Ikkinchisi: index-only scan umuman mumkin emas.

Xossalari qattiq cheklangan: tartiblash yo'q, unikal cheklov yo'q, ko'p ustunli indeks yo'q, `INCLUDE` yo'q, `NULL` bo'yicha qidiruv yo'q, massiv ichidan qidiruv yo'q, `CLUSTER` yo'q. Yagona qo'llaydigan operatori tenglik. Shunga qaramay exclusion constraint qo'llanadi va tenglik operatori bilan u amalda unikallik ma'nosini oladi. Yana bitta operatsion cheklov bor: hash indeks kichraymaydi, bucket sahifalari bo'sh bo'lsa ham operatsion tizimga qaytarilmaydi va hajmni faqat `REINDEX` kamaytiradi.

```sql
-- Uzun matnli kalit bo'yicha faqat tenglik qidiruvi
CREATE INDEX idx_hodisa_kalit ON hodisalar USING hash (idempotency_key);

-- Rejada indeks turi ko'rinmaydi: oddiy Bitmap Index Scan deb yoziladi
EXPLAIN SELECT * FROM hodisalar WHERE idempotency_key = '3f2a7c';

-- Unikallik kerak bo'lsa yagona yo'l exclusion constraint
ALTER TABLE hodisalar
    ADD CONSTRAINT hodisa_kalit_unikal
    EXCLUDE USING hash (idempotency_key WITH =);
```

PostgreSQL 10 gacha hash indeks WAL ga yozilmagan, ya'ni nosozlikdan himoyalanmagan va replikatsiya qilinmagan edi, shuning uchun uni ishlatish tavsiya etilmasdi; 10 dan boshlab bu cheklov yo'q. Kitob hash va B-tree ni tezlik bo'yicha taqqoslamaydi, shuning uchun bu yerda raqam berilmaydi. Mexanizmdan kelib chiqadigan xulosa esa shunday: hash indeks kalitni saqlamagani uchun uzun kalitlarda kichikroq chiqadi, lekin oraliq, tartib va index-only scan ni bermaydi, demak u faqat uzun kalit faqat tenglik bo'yicha qidiriladigan tor holatga mos keladi. Spring da bunga idempotentlik kaliti yoki webhook imzosi ustuni misol bo'ladi, lekin bunday ustun odatda unikal bo'lishi kerak va unikallikni hash faqat exclusion constraint orqali beradi.

## 23.17 SP-GiST: quadtree, k-d tree va radix tree

SP-GiST nomidagi SP qismi Space Partitioning, ya'ni fazoni bo'lish degani; GiST qismi esa ikkala usul ham umumlashgan qidiruv daraxti ekanini bildiradi. Fazo bu yerda ikki o'lchovli tekislik emas, balki qidiruv olib boriladigan ixtiyoriy qiymatlar to'plami. Usulning g'oyasi fazoni kesishmaydigan sohalarga bo'lish va har bir sohani rekursiv ravishda yana bo'lish.

Natijada hosil bo'ladigan daraxt muvozanatlanmagan: B-tree va GiST dan farqli, uning shoxlari kam va chuqurligi katta, shuning uchun tugunlarni sahifalarga zich joylashtirish alohida vazifa bo'lib qoladi. Shu asosda uchta klassik tuzilma quriladi: nuqtalar uchun quadtree (tekislik tanlangan nuqta, ya'ni centroid atrofida to'rt kvadrantga bo'linadi), yana nuqtalar uchun k-d tree (har qadamda gorizontal va vertikal bo'lish navbatlashadi, demak har tugunda ikkita farzand) va satrlar uchun radix tree, unda ichki tugunning prefiksi haqiqatan ham farzandlarning umumiy prefiksi bo'ladi.

```sql
-- Satr uchun radix tree: prefiks bo'yicha qidiruv ^@ operatori bilan
CREATE INDEX idx_hujjat_raqam ON hujjatlar USING spgist (raqam);
SELECT * FROM hujjatlar WHERE raqam ^@ 'UZ-2026-';

-- IP manzil uchun radix tree
CREATE INDEX idx_kirish_ip ON kirish_jurnali USING spgist (ip_manzil inet_ops);

-- Oraliqlar uchun quadtree: pastki va yuqori chegara ikki o'lchovli nuqta
CREATE INDEX idx_narx_davri ON narx_davrlari USING spgist (amal_davri);
```

Xossalari GiST dan sezilarli farq qiladi va tanlovda ko'pincha shu farq hal qiladi: tartiblash va unikallik yo'q, ko'p ustunli indeks yo'q, `CLUSTER` yo'q, teskari skan yo'q. Exclusion constraint va `INCLUDE` ustunlari esa bor. `NULL` qiymatlar asosiy daraxtda emas, indeksning uchinchi sahifasidan boshlanadigan alohida daraxtda saqlanadi.

GiST bilan SP-GiST o'rtasidagi tanlov ma'lumot tabiatiga bog'liq: kitob PostGIS hujjatiga havola qilib, bir-biri bilan ko'p kesishadigan obyektlar uchun SP-GiST tavsiya etilishini aytadi. Java tomonidagi tipik qo'llanishlar: hujjat raqami yoki mahsulot artikuli kabi prefiksli kodlar (`^@` operatori `startsWith` semantikasini beradi), `inet` ustunidagi IP manzil va `tstzrange` ustunidagi narx yoki bron davrlari. Masofa operatori satrlar uchun aniqlanmagan, shuning uchun o'xshashlik bo'yicha tartiblash kerak bo'lsa baribir GiST va `pg_trgm` tanlanadi.

## 23.18 B-tree ichida: deduplication va suffix truncation

Nounikal indeksda bitta kalit ko'p marta takrorlanishi mumkin va har takror joy oladi. PostgreSQL 13 dan buni deduplication hal qiladi: bir xil kalitli yozuvlar bitta yozuvga yig'iladi va unda kalit bilan birga TID lar ro'yxati saqlanadi. Unikal indeksda ham dublikat bo'ladi, chunki MVCC tufayli indeks qatorning hamma versiyasiga havola saqlaydi; HOT update buni yumshatadi, lekin har doim ham qo'llanmaydi.

Deduplication resursni behuda sarflamasligi uchun u doim emas, faqat leaf sahifada navbatdagi tuple uchun joy qolmaganda ishga tushadi. Shunda sahifa tozalanadi va dublikatlar yig'iladi, natijada sahifa bo'linishi kechiktiriladi yoki umuman kerak bo'lmaydi.

Hamma indeks ham buni qo'llamaydi. Asosiy shart: kalitlarning tengligi ularning ichki tasvirini baytma-bayt solishtirish bilan aniqlanishi kerak. Shuning uchun deduplication `float` va `double precision` uchun ishlamaydi (nolning ikki tasviri bor), `numeric` uchun ham ishlamaydi (bir son har xil masshtabda yozilishi mumkin) va shunday sonlarni ishlatishi mumkin bo'lgan `jsonb` uchun ham; nodeterministik collation li matn, kompozit turlar, oraliqlar, massivlar va `INCLUDE` bilan e'lon qilingan indekslar ham tashqarida qoladi.

```sql
-- Shu indeksda deduplication mumkinmi
CREATE EXTENSION IF NOT EXISTS pageinspect;
SELECT allequalimage FROM bt_metap('idx_buyurtma_mijoz');

-- Dublikat kam bo'lsa deduplication ni o'chirish mumkin
ALTER INDEX idx_buyurtma_mijoz SET (deduplicate_items = off);
```

Ikkinchi zichlashtirish mexanizmi ichki sahifalarda ishlaydi. Ichki yozuvdagi kalit faqat qaysi pastki daraxtga tushishni aniqlash uchun kerak, shuning uchun ko'p ustunli indeksda ko'pincha birinchi atribut yetadi va qolganlari kesib tashlanadi. Bu suffix truncation deb ataladi va leaf sahifa bo'linayotganda bajariladi. Foydasi to'g'ridan-to'g'ri: ichki sahifaga ko'proq yozuv sig'adi, daraxt sayozroq bo'ladi va qidiruv kamroq sahifa o'qiydi. Hozircha kesish atribut darajasida: yozuv atributni yo butunlay saqlaydi, yo butunlay tashlab yuboradi.

Arxitektor uchun xulosa: ustun turini tanlash indeks hajmiga bevosita ta'sir qiladi. Pul qiymati uchun `numeric` to'g'ri tanlov, lekin unga qo'yilgan nounikal indeks deduplication dan foyda ko'rmaydi; `jsonb` ustiga qo'yilgan B-tree ham shunday. Takrorlanadigan kalitli ustunlar (status, mijoz identifikatori) `bigint` yoki `text` bo'lsa esa deduplication indeks hajmini sezilarli kamaytiradi va buni `pgstatindex` bilan o'lchab tasdiqlash mumkin.

## 23.19 Operator class tanlov sifatida: `text_pattern_ops`, collation va `LIKE` prefiksi

[Indeks interfeysi bo'limida](#2314-indeks-interfeysi-pg_am-operator-class-va-operator-family) operator class mexanizm sifatida ko'rsatilgan. Bu yerda u QAROR sifatida ko'riladi, chunki bir xil ma'lumot turini ko'pincha bir nechta operator class qo'llaydi va ulardan eng mos xulqlisini foydalanuvchi tanlaydi (Rogov, 19.1, 315-bet). `text` turi uchun B-tree da to'rtta class bor: `text_ops` (standart), `varchar_ops`, `text_pattern_ops` va `varchar_pattern_ops` (Rogov, 19.2, 316-bet).

Farq collation da. Har bir B-tree operator class beshta majburiy taqqoslash operatorini e'lon qiladi va ularning semantikasi strategiya raqami bilan belgilanadi: 1 kichik, 2 kichik yoki teng, 3 teng, 4 katta yoki teng, 5 katta (Rogov, 19.2, 317-bet; 25.4, 432-433-betlar). `text_ops` buning uchun odatdagi `<`, `<=`, `=`, `>=`, `>` ni ishlatadi, `text_pattern_ops` esa tildali `~<~`, `~<=~`, `=`, `~>=~`, `~>~` ni: ikkinchi to'plam collation ni hisobga olmaydi va satrlarni baytma-bayt taqqoslaydi (Rogov, 19.2, 317-bet).

Shundan amaliy natija chiqadi. `C` dan boshqa collation ishlatadigan bazada `LIKE 'ELENA%'` sharti oddiy indeksni ishlata olmaydi va reja `Seq Scan` bo'ladi. `text_pattern_ops` bilan qurilgan indeks esa shartni taqqoslash operatorlariga qayta yozadi va `Bitmap Index Scan` beradi, bunda `%` dan oldingi prefiks ishlatiladi, yolg'on moslar esa `Filter` bilan qayta tekshiruvda tashlanadi (Rogov, 19.2, 318-bet).

```sql
SHOW lc_collate;   -- en_US.UTF-8

-- Standart class: LIKE prefiksi indeksni ishlatmaydi, Seq Scan
CREATE INDEX idx_tickets_name ON tickets (passenger_name);

-- Pattern class: Index Cond
--   (passenger_name ~>=~ 'ELENA' AND passenger_name ~<~ 'ELENB')
CREATE INDEX idx_tickets_name_pattern
    ON tickets (passenger_name text_pattern_ops);

EXPLAIN (COSTS OFF)
SELECT * FROM tickets WHERE passenger_name LIKE 'ELENA%';
```

ESLATMA: korpus qo'shimchasi. Kitob buni bevosita aytmaydi, lekin mexanizmdan kelib chiqadi: `text_pattern_ops` indeksi bayt tartibida saralangani uchun u baza collation idagi `ORDER BY passenger_name` ni qoplamaydi. Demak prefiks qidiruvi ham, tartiblash ham kerak bo'lsa ikkita indeks turadi va bu yozuv narxiga qo'shiladi. Shu sababli birinchi savol doim bitta: prefiks qidiruvi haqiqatan kerakmi yoki `ILIKE '%...%'` uchun baribir `gin_trgm_ops` kerakmi.

| Qaror | Tanlanadigan operator class | Nega |
|---|---|---|
| `LIKE 'prefiks%'`, collation `C` emas | `text_pattern_ops` (B-tree) | tildali operatorlar collation ni hisobga olmaydi |
| `ILIKE '%ichki%'` | `gin_trgm_ops` (GIN) | prefiks yo'q, trigramma bo'yicha nomzod |
| `jsonb @>` ustunlik qiladi | `jsonb_path_ops` (GIN) | kichikroq va `@>` da tezroq |
| `jsonb ?`, `?|`, `?&` ham kerak | `jsonb_ops` (GIN) | kalit mavjudligini tekshiradi |
| Korrelyatsiyasi past, lekin tenglik | `bloom` (BRIN) | minmax oraliq bermaydi |
| Chetlab ketgan qiymatlari bor oraliq | `minmax_multi` (BRIN) | bitta oraliqqa bir nechta chegara to'plami |

Operator class faqat indeks uchun emasligini ham bilish kerak. Hash algoritmi hash join va guruhlash uchun ham ishlatiladi, va tizim qaysi tur uchun qaysi hash funksiyasi borligini aynan hash indeksining operator classidan biladi, chunki PostgreSQL yangi turlarni ish davomida qo'shishga ruxsat beradi va bu moslikni bir marta qotirib qo'yib bo'lmaydi (Rogov, 24.3, 417-bet). Hash operator class esa faqat tenglik operatorini beradi (Rogov, 24.3, 418-bet).

## 23.20 Korrelyatsiya: bir xil tanlanuvchanlik, boshqa narx

Indeks skanining narxi ikki qismdan iborat: indeksga murojaat va heap sahifalarini o'qish. Ikkinchi qism faqat tanlanuvchanlikka emas, diskdagi tuple larning jismoniy tartibi bilan access method `TID` larni qaytaradigan tartib orasidagi korrelyatsiyaga ham bog'liq (Rogov, 20.1, 331-bet). Korrelyatsiya ideal bo'lsa har bir sahifaga faqat bir marta murojaat qilinadi va `Index Scan` node sahifadan sahifaga ketma-ket o'tadi (Rogov, 20.1, 331-bet).

Farqning kattaligini kitob ikki o'lchov bilan ko'rsatadi, ikkalasida ham jadvalning taxminan bir xil ulushi qaytadi. `book_ref` ustunida korrelyatsiya 1, tanlanuvchanlik 0.0630, 132999 qator: `Index Scan` narxi 4638.91 (Rogov, 20.1, 332-bet). `book_date` ustunida korrelyatsiya 8.02188e-05, 132403 qator: o'sha jadvalda `Index Scan` narxi 56957.48, va planner bu rejani faqat seq scan ham, bitmap scan ham ataylab o'chirilganda tanlaydi (Rogov, 20.1, 334-bet). Sabab mexanik: korrelyatsiya past bo'lganda keyingi tuple boshqa sahifada bo'lish ehtimoli oshadi, shuning uchun `Index Scan` sahifalar orasida sakraydi va eng yomon holatda sahifaga murojaatlar soni olingan tuple lar soniga tenglashadi (Rogov, 20.1, 334-bet).

```sql
-- Qaror shu ustundan boshlanadi, EXPLAIN dan emas
SELECT attname, correlation, n_distinct
FROM pg_stats
WHERE tablename = 'orders'
ORDER BY abs(correlation) DESC;

-- 1 ga yaqin: index scan katta ulushda ham arzon
-- 0 ga yaqin: index scan tez orada seq scan dan qimmatlashadi
```

Korrelyatsiya o'zgarmas xossa emas. Har qanday qator yangilanishi natijaviy tuple ni jadval oxiriga ko'chiradi, shuning uchun tez-tez `UPDATE` bo'ladigan ustunda korrelyatsiya asta buziladi; bundan tashqari ideal korrelyatsiya ham natijaning tartibini KAFOLATLAMAYDI, chunki boshqa ustun bo'yicha index scan boshqa tartib beradi va seq scan jadvalning boshidan boshlamasligi mumkin, demak tartib kerak bo'lsa u `ORDER BY` da aniq yoziladi (Rogov, 20.1, 332-bet).

Arxitektor uchun uchta aniq qaror chiqadi. Birinchi: korrelyatsiyasi past ustunda keng oraliq so'rovi uchun indeks qo'shish ko'pincha foyda bermaydi, chunki planner uni baribir tanlamaydi. Ikkinchi: shunday so'rov uchun to'g'ri yechim heap ga borishni butunlay yo'q qilish, ya'ni [qamrab oluvchi indeks bilan index-only scan](#233-qamrab-oluvchi-indeks-include-va-index-only-scan-sharti). Uchinchi: korrelyatsiya tabiiy bo'lgan jadvalda (append-only log) arzon variant [BRIN](#238-brin-katta-tartibli-jadvallar-uchun-arzon-indeks), chunki u aynan shu xossaga tayanadi.

## 23.21 GIN qidiruvi: leksema chastotasi, majburiy bitmap va `gin_fuzzy_search_limit`

GIN ning qidiruv tezligi so'rovdagi eng KAM uchraydigan elementga bog'liq. Agar so'rovda ham tez-tez, ham kam uchraydigan leksema bo'lsa, kam uchraydigani majburiy deb olinadi, tez-tez uchraydigani esa ixtiyoriy: algoritm leksemalarni chastota bo'yicha saralaydi, ularni birin-ketin majburiylar ro'yxatiga qo'shadi va qolganlari natijani kafolatlay olmay qolganda to'xtaydi (Rogov, 28.2, 499-bet). Natijada skan kam uchraydigan leksemaning `TID` lari bo'yicha boradi va tez-tez uchraydiganining butun boshli sahifa oraliqlarini o'tkazib yuboradi (Rogov, 28.2, 500-bet).

Kitob buni o'lchov bilan ko'rsatadi: pgsql-hackers arxividagi `wrote` 231173 hujjatda, `tattoo` esa 2 hujjatda uchraydi. `wrote & tattoo` so'rovi 0.631 ms, yolg'iz `tattoo` 2.227 ms, yolg'iz `wrote` esa 343.556 ms ketadi (Rogov, 28.2, 501-bet). Ya'ni tez-tez uchraydigan so'zni so'rovdan olib tashlash emas, unga kam uchraydigan so'zni QO'SHISH tezlashtiradi.

Ikkinchi xossa rejani belgilaydi: GIN natijani doim bitmap ko'rinishida qaytaradi va `TID` larni bittalab berolmaydi, ya'ni `bitmap_scan` xossasi rost, `index_scan` esa yolg'on (Rogov, 28.2, 503-bet). Sababi tartibsiz pending list: skan paytida u asosiy daraxt bilan birlashsa, bitta qiymat ikki marta qaytishi mumkin, bitmap da esa bir bit ikki marta o'rnatilgani zarar qilmaydi (Rogov, 28.2, 503-bet).

Buning amaliy oqibati `LIMIT` ga tegadi: GIN bilan `LIMIT` ishlatish samarasiz, chunki bitmap baribir to'liq quriladi va uning narxi umumiy narxning katta qismini tashkil qiladi (Rogov, 28.2, 504-bet). Shuning uchun FTS sahifalashini `LIMIT` ga tayanib "tez" deb hisoblash xato.

```sql
-- Natija sonini cheklash: standart 0, ya'ni o'chiq
SHOW gin_fuzzy_search_limit;

SET gin_fuzzy_search_limit = 1000;
SELECT count(*) FROM mail_messages WHERE tsv @@ to_tsquery('hacker');
-- 727
SELECT count(*) FROM mail_messages WHERE tsv @@ to_tsquery('hacker');
-- 791   ayni so'rov, boshqa natija
RESET gin_fuzzy_search_limit;
```

`gin_fuzzy_search_limit` indeks skani qaytaradigan natija sonini cheklaydi va PostgreSQL 14 da standart holatda o'chirilgan (qiymati nol). Yoqilsa, access method taxminan ko'rsatilgan songa yetish uchun ba'zi qiymatlarni TASODIFIY tashlab ketadi, shuning uchun bir xil so'rov bir xil natija bermaydi; planner esa bu parametr haqida hech narsa bilmaydi va uni narx baholashda hisobga olmaydi (Rogov, 28.2, 504-bet).

Arxitektura qoidasi shundan chiqadi va u qat'iy: `gin_fuzzy_search_limit` sahifalash vositasi emas va determinizm talab qiladigan hech qaysi yo'lda ishlatilmaydi. U faqat "yetarlicha natija bo'lsa bo'ldi" degan qidiruv ekranida mantiqli, va u yerda ham `count(*)` ko'rsatkichini buzadi. Sifat va relevantlik bo'yicha qaror [PostgreSQL FTS ning qattiq chegaralari](40-qidiruv-postgresql-fts-va-alohida-dvigatel.md#403-postgresql-fts-ning-qattiq-chegaralari) bo'limida.

## 23.22 BRIN ni sozlash: `pages_per_range`, `autosummarize` va qo'lda summarizatsiya

BRIN da sozlanadigan asosiy parametr bitta: oraliqdagi sahifalar soni, `pages_per_range`, PostgreSQL 14 da standarti 128 (Rogov, 29.1, 517-bet). Uni tanlash uchun `EXPLAIN` emas, bitta o'lchov kerak: bitta so'rov oralig'iga tushadigan ma'lumot necha sahifani egallaydi.

Kitobning o'lchovi aniq. `flights_bi` jadvalida bir kunlik ma'lumot 1192 dan 1512 gacha sahifani egallaydi, o'rtacha 1447 (Rogov, 29.6, 526-bet). Bir kunlik so'rov uchun uch xil oraliq hajmi solishtirilganda indeks hajmi shunday chiqadi: 32 sahifa uchun 529 kB, standart 128 sahifa uchun 184 kB, 512 sahifa uchun 72 kB; samaradorlik esa katta oraliqlarda ham yuqori qoladi (Rogov, 29.6, 528-bet). Ya'ni savdo bir tomonlama emas: oraliqni kichraytirish aniqlikni oshiradi, lekin indeks hajmi shunga yarasha o'sadi va BRIN ning asosiy afzalligi, ya'ni kichikligi yo'qoladi.

```sql
-- Bitta kunlik oraliq necha sahifada yotadi: pages_per_range shu yerdan chiqadi
SELECT min(numblk), round(avg(numblk)) AS avg, max(numblk)
FROM (
  SELECT count(DISTINCT (ctid::text::point)[0]::integer) AS numblk
  FROM audit_log
  GROUP BY created_at::date
) t;
```

Yangi sahifalar masalasi alohida. PostgreSQL 14 da standart holatda indeks qurilgandan keyin paydo bo'lgan yangi oraliqlar darhol umumlashtirilmaydi va bu indeks to'g'riligiga ta'sir qilmaydi, chunki summary ma'lumoti yo'q oraliq doim skanlanadi; umumlashtirish asinxron, ya'ni jadval vacuum i paytida yoki `brin_summarize_new_values` (bitta oraliq uchun `brin_summarize_range`) chaqirilganda bajariladi (Rogov, 29.5, 523-bet). `autosummarize = on` yoqilsa yangi oraliq darhol umumlashtiriladi, lekin ma'lumot omborida, ya'ni qatorlar bittalab emas katta paket bilan qo'shiladigan joyda bu rejim qo'shishni jiddiy sekinlashtirishi mumkin (Rogov, 29.5, 523-bet).

```sql
CREATE INDEX idx_audit_created_brin
    ON audit_log USING brin (created_at) WITH (pages_per_range = 64);

-- Paketli yuklashdan keyin: autosummarize o'rniga aniq chaqiruv
SELECT brin_summarize_new_values('idx_audit_created_brin');

-- Faqat bitta oraliqni qayta hisoblash kerak bo'lsa
SELECT brin_desummarize_range('idx_audit_created_brin', 128);
SELECT brin_summarize_range('idx_audit_created_brin', 128);
```

Yana bir xossa qarorga ta'sir qiladi: summary ma'lumoti hech qachon qisqarmaydi, u faqat kengayadi, va qaysi oraliqni qayta hisoblash foyda berishini aytadigan belgi yo'q (Rogov, 29.5, 523-bet). Demak BRIN ko'p `UPDATE` va `DELETE` bo'ladigan jadvalda asta ma'nosini yo'qotadi va uni qayta tiklashning avtomatik yo'li yo'q. Kitobning o'z xulosasi ham shu: BRIN birinchi navbatda juda katta, ya'ni yo faqat oxiriga yangi qator qo'shiladigan, yo umuman yangilanmaydigan jadvallar uchun va asosan analitik hisobotlar uchun mo'ljallangan (Rogov, 29.5, 523-bet).

Spring tomonida bundan bitta operatsion qoida chiqadi: paketli yuklovchi job `autosummarize` ga tayanmaydi, balki yuklash tugagach `brin_summarize_new_values` ni aniq chaqiradi. Shunda yuklash tezligi tushmaydi va keyingi hisobot to'liq summary ustida ishlaydi.

## 23.23 Amalda qo'llash

- [ ] Eng og'ir 10 so'rovni `pg_stat_statements` dan oling va har biriga `EXPLAIN (ANALYZE, BUFFERS)` yozib, `Heap Fetches` va `Rows Removed by Filter` qiymatlarini qayd qiling.
- [ ] Mijoz kabinetidagi ro'yxat so'rovi uchun ustunlar tartibini tekshirib, tenglik ustunini oldinga, `ORDER BY` ustunini oxiriga qo'ygan bitta indeks qoldiring.
- [ ] Navbat yoki status jadvalidagi to'liq indeksni qisman indeksga aylantirib, hajm va yozuv latency sidagi farqni o'lchang.
- [ ] `jsonb` ustunidagi hamma alohida ifoda indekslarini ko'rib chiqib, ularni bitta GIN indeksi bilan almashtirish mumkinligini sinab ko'ring.
- [ ] 100 GB dan katta append-only jadvalda `pg_stats.correlation` ni o'lchab, mos bo'lsa BRIN ga o'tish rejasini tuzing.
- [ ] `pg_stat_user_indexes` so'rovini primary va hamma replikada bajarib, nomzod keraksiz indekslar ro'yxatini tuzing va choraklik ko'rikka qo'ying.
- [ ] Migratsiya quvurida `CREATE INDEX CONCURRENTLY` ni tranzaksiyadan tashqarida ishlatish imkonini sozlab, yaroqsiz indeksni tekshiruvchi qadamni qo'shing.
- [ ] Eng katta uchta indeks uchun `pgstatindex` bilan leaf zichligini o'lchab, 40 foizdan past bo'lsa `REINDEX CONCURRENTLY` ni xizmat oynasiga rejalashtiring.
- [ ] Yozuv og'ir jadvallarda indeks sonini qayta ko'rib chiqing: har bir ortiqcha indeks yozish kuchayishini oshiradi.
- [ ] HOT update ishlayotganini tekshirish uchun tez-tez o'zgaradigan ustunlar indeksda yo'qligini ta'minlang.

## Manbalar

- Martin Kleppmann, *Designing Data-Intensive Applications*, 3-bob - B-tree va LSM dvigatellari, o'qish va yozish kuchayishi
- [PostgreSQL, Heap-Only Tuples (HOT)](https://www.postgresql.org/docs/current/storage-hot.html) - indeks yangilanmasligi sharti
- [PostgreSQL 17, Indexes (indices.sgml)](https://raw.githubusercontent.com/postgres/postgres/REL_17_STABLE/doc/src/sgml/indices.sgml) - indeks turlari, qaysi operatorga yordam berishi, partial va covering indeks
- Egor Rogov, *PostgreSQL 14 Internals*, Postgres Professional, 2022, 19-bob "Index Access Methods", 313-328-betlar - oltita access method, indexing engine vazifasi, operator class va family, indeks xossalari
- Egor Rogov, *PostgreSQL 14 Internals*, Postgres Professional, 2022, 24-bob "Hash", 411-420-betlar - bucket va overflow sahifalari, kalit saqlanmasligi, hash indeks xossalari va cheklovlari
- Egor Rogov, *PostgreSQL 14 Internals*, Postgres Professional, 2022, 27-bob "SP-GiST", 472-491-betlar - quadtree, k-d tree, satrlar uchun radix tree, `inet` va oraliq operator classlari
- Egor Rogov, *PostgreSQL 14 Internals*, Postgres Professional, 2022, 25-bob "B-tree", 429-431-betlar - deduplication sharti va `allequalimage`, ichki yozuvlarda suffix truncation
- Egor Rogov, *PostgreSQL 14 Internals*, Postgres Professional, 2022, 28-bob "GIN", 505-506-betlar - GIN xossalari, leksema pozitsiyasi indeksga tushmasligi va `rum` kengaytmasi
- Egor Rogov, *PostgreSQL 14 Internals*, Postgres Professional, 2022, 19-bob "Index Access Methods", 315-318-betlar - bir turni bir nechta operator class qo'llashi va tanlov foydalanuvchida bo'lishi, `text` uchun to'rtta B-tree class, tildali operatorlar collation ni hisobga olmasligi, `text_pattern_ops` bilan `LIKE 'prefiks%'` indeksga tushishi
- Egor Rogov, *PostgreSQL 14 Internals*, Postgres Professional, 2022, 19-bob "Index Access Methods", 326-bet - `clusterable`, `index_scan`, `bitmap_scan` va `backward_scan` xossalarining ta'rifi
- Egor Rogov, *PostgreSQL 14 Internals*, Postgres Professional, 2022, 20-bob "Index Scans", 331-334-betlar - indeks skan narxining korrelyatsiyaga bog'liqligi, `pg_stats.correlation`, yuqori korrelyatsiyada 4638.91 va past korrelyatsiyada 56957.48 narx, yangilanish korrelyatsiyani buzishi va tartib uchun `ORDER BY` majburiyligi
- Egor Rogov, *PostgreSQL 14 Internals*, Postgres Professional, 2022, 20-bob "Index Scans", 348-349-betlar - seq scan va index scan narxining selektivlikka bog'liqligi egri chiziq sifatida, aniq foiz chegarasi yo'qligi
- Egor Rogov, *PostgreSQL 14 Internals*, Postgres Professional, 2022, 23-bob "Sorting and Merging", 388-bet - merge join faqat tenglik operatorini qo'llashi
- Egor Rogov, *PostgreSQL 14 Internals*, Postgres Professional, 2022, 24-bob "Hash", 417-418-betlar - hash funksiyasini tur bilan bog'lashni operator class qilishi va uning hash join hamda guruhlashda ishlatilishi, hash classda faqat tenglik operatori
- Egor Rogov, *PostgreSQL 14 Internals*, Postgres Professional, 2022, 25-bob "B-tree", 432-442-betlar - taqqoslash semantikasi va beshta strategiya, ko'p ustunli indeksda `ASC`/`DESC` aralashuvi va `Incremental Sort`, `NULL` larning standart joyi hamda `NULLS FIRST` va `NULLS LAST`, B-tree ning to'rtta indeks darajasidagi xossasi
- Egor Rogov, *PostgreSQL 14 Internals*, Postgres Professional, 2022, 28-bob "GIN", 499-504-betlar va 516-bet - kam uchraydigan leksemaning majburiy bo'lishi va o'lchovlar (`wrote` 231173, `tattoo` 2 hujjat; 0.631, 2.227 va 343.556 ms), GIN doim bitmap qaytarishi va `LIMIT` ning samarasizligi, `gin_fuzzy_search_limit` standarti nol va tasodifiy tashlab ketishi, `intarray`, `hstore` va `jsquery` kengaytmalari
- Egor Rogov, *PostgreSQL 14 Internals*, Postgres Professional, 2022, 29-bob "BRIN", 517-529-betlar - `pages_per_range` standarti 128, `autosummarize` standarti o'chiq va paketli yuklashni sekinlashtirishi, `brin_summarize_new_values` va `brin_desummarize_range`, summary ning qisqarmasligi, oraliq hajmi va indeks hajmi savdosi (32 sahifa 529 kB, 128 sahifa 184 kB, 512 sahifa 72 kB), BRIN ning indeks darajasidagi xossalari

---

[&larr; 22. MVCC, izolyatsiya darajalari, lock va deadlock](22-mvcc-izolyatsiya-darajalari-lock-va-deadlock.md) · [Mundarija](README.md) · [24. Planner, statistika va EXPLAIN ANALYZE o'qish &rarr;](24-planner-statistika-va-explain-analyze-oqish.md)
