<!-- doc: architect | chapter: 23 | part: IV. PostgreSQL chuqur bilim -->

[Kod yozadigan arxitektorning miyyasi](../../README.md) / [Arxitektor miyyasi](README.md)

# 23. Indekslar: B-tree, GIN, GiST, BRIN va tanlov (Indexes)

<details>
<summary>Bu bobdagi 13 bo'lim</summary>

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
- [23.13 Amalda qo'llash](#2313-amalda-qollash)

</details>


Indeks so'rovni tezlashtiradigan sehr emas, balki ma'lumotning ikkinchi, tartiblangan nusxasi. Har bir indeks o'qishni tezlashtirgani uchun yozishdan, diskdan va vacuum vaqtidan to'lov oladi. Arxitektor uchun savol "indeks qo'shaylikmi" emas, balki "qaysi tur, qaysi ustunlar tartibida, qanday shart bilan va qaysi so'rovni qoplash uchun". Bu bobda PostgreSQL 15-17 dagi indeks turlarining ichki mexanikasi, ularning narxi va tanlov mezonlari ko'rib chiqiladi.

## 23.1 B-tree tuzilishi va u qaysi so'rovlarga yordam beradi

PostgreSQL ning standart indeksi B-tree, aniqrog'i B+tree ning Lehman-Yao variantidir. Daraxt 8 KB li sahifalardan iborat: yuqorida root, o'rtada internal sahifalar, pastda leaf sahifalar. Faqat leaf sahifalarda heap ga ko'rsatkichlar, ya'ni TID lar saqlanadi, va leaf qatlami ikki tomonlama bog'langan ro'yxat bo'lib, shu sababli oraliq bo'yicha skanlash bitta yo'nalishda ketma-ket boradi.

Chuqurlik juda sekin o'sadi. Taxminan 100 million qatorli `bigint` kalit uchun daraxt 4 qatlamdan oshmaydi va yuqori qatlamlar deyarli doim `shared_buffers` da yotadi.

B-tree quyidagilarga yordam beradi: `=`, `<`, `>`, `BETWEEN`, `IN`, `IS NULL`, `ORDER BY` uchun tayyor tartib, `MIN`/`MAX`, merge join, va unique constraint. U yordam bermaydigan holatlar: `LIKE '%mato%'` kabi prefiksi yo'q qidiruv, ustun ustida funksiya chaqirilgan shart, va jadvalning 10 foizidan ko'pini qaytaradigan so'rov. Oxirgi holatda planner ataylab seq scan ni tanlaydi, chunki random IO ketma-ket o'qishdan qimmatroq.

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

PostgreSQL 14 dan `minmax_multi` opclass bor: u bitta oraliq uchun bir nechta chegara to'plamini saqlaydi, shuning uchun bir nechta chetlab ketgan qiymat butun oraliqni buzmaydi. `bloom` opclass esa korrelyatsiyasiz ustunda tenglik qidiruvi uchun ishlaydi. Yangi sahifalarni avtomatik umumlashtirish uchun `autosummarize = on` yoqiladi.

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

## 23.13 Amalda qo'llash

- [ ] Eng og'ir 10 so'rovni `pg_stat_statements` dan oling va har biriga `EXPLAIN (ANALYZE, BUFFERS)` yozib, `Heap Fetches` va `Rows Removed by Filter` qiymatlarini qayd qiling.
- [ ] Mijoz kabinetidagi ro'yxat so'rovi uchun ustunlar tartibini tekshirib, tenglik ustunini oldinga, `ORDER BY` ustunini oxiriga qo'ygan bitta indeks qoldiring.
- [ ] Navbat yoki status jadvalidagi to'liq indeksni qisman indeksga aylantirib, hajm va yozuv latency sidagi farqni o'lchang.
- [ ] `jsonb` ustunidagi hamma alohida ifoda indekslarini ko'rib chiqib, ularni bitta GIN indeksi bilan almashtirish mumkinligini sinab ko'ring.
- [ ] 100 GB dan katta append-only jadvalda `pg_stats.correlation` ni o'lchab, mos bo'lsa BRIN ga o'tish rejasini tuzing.
- [ ] `pg_stat_user_indexes` so'rovini primary va hamma replikada bajarib, nomzod keraksiz indekslar ro'yxatini tuzing va choraklik ko'rikka qo'ying.
- [ ] Migratsiya quvurida `CREATE INDEX CONCURRENTLY` ni tranzaksiyadan tashqarida ishlatish imkonini sozlab, yaroqsiz indeksni tekshiruvchi qadamni qo'shing.
- [ ] Eng katta uchta indeks uchun `pgstatindex` bilan leaf zichligini o'lchab, 40 foizdan past bo'lsa `REINDEX CONCURRENTLY` ni xizmat oynasiga rejalashtiring.

---

[&larr; 22. MVCC, izolyatsiya darajalari, lock va deadlock](22-mvcc-izolyatsiya-darajalari-lock-va-deadlock.md) · [Mundarija](README.md) · [24. Planner, statistika va EXPLAIN ANALYZE o'qish &rarr;](24-planner-statistika-va-explain-analyze-oqish.md)
