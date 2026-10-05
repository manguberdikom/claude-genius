<!-- doc: code-review | chapter: 24 | part: V. PostgreSQL va ma'lumot qatlami review -->

[Barcha hujjatlar](../../README.md) / [Kod review](README.md)

> Holat: AI yozgan, inson tekshirmagan.

# 24. SQL, so'rov rejasi va indeks review (SQL, Plans and Indexes)

<details>
<summary>Bu bobdagi 10 bo'lim</summary>

- [24.1 Indeks ishlatilmaydigan naqshlar](#241-indeks-ishlatilmaydigan-naqshlar)
- [24.2 Yangi indeks qo'shilganda review savollari](#242-yangi-indeks-qoshilganda-review-savollari)
- [24.3 So'rov rejasini o'qish: review uchun minimal bilim](#243-sorov-rejasini-oqish-review-uchun-minimal-bilim)
- [24.4 JOIN va agregat so'rovlari](#244-join-va-agregat-sorovlari)
- [24.5 Dinamik SQL review](#245-dinamik-sql-review)
- [24.6 Katta jadvallar bilan ishlash](#246-katta-jadvallar-bilan-ishlash)
- [24.7 JSONB review](#247-jsonb-review)
- [24.8 Review paytida so'rovni o'lchash](#248-review-paytida-sorovni-olchash)
- [24.9 Review checklisti: SQL va indekslar](#249-review-checklisti-sql-va-indekslar)
- [24.10 Amalda qo'llash](#2410-amalda-qollash)

</details>


Review stolida so'rov rejasini ko'rish imkoni bo'lmaydi, lekin uni taxmin qilish imkoni bor. Bu bob shu malakani beradi: SQL ga qarab PostgreSQL nima qilishini aytish, va qachon `EXPLAIN` so'rash kerakligini bilish. PostgreSQL planner mexanikasi [Arxitektor miyasi](../architect/README.md) da.

## 24.1 Indeks ishlatilmaydigan naqshlar

Bu ro'yxat review ning eng tez qaytim beradigan qismi: har bir naqsh indeksni o'chiradi va seq scan keltiradi.

| Naqsh | Nega indeks ishlamaydi | To'g'ri shakl |
| --- | --- | --- |
| `WHERE date(created_at) = ?` | Ustun funksiya ichida | Oraliq: `>= ? AND < ?` |
| `WHERE lower(email) = ?` | Funksiya | Ifoda indeksi: `ON t (lower(email))` |
| `WHERE amount::text LIKE '1%'` | Tur konversiyasi | Raqamli taqqoslash |
| `WHERE name LIKE '%abc%'` | Boshida wildcard | Trigram indeks (`pg_trgm`) yoki FTS |
| `WHERE status != 'CLOSED'` | Selektivlik past | Partial indeks |
| `WHERE col + 0 = ?` | Ustun ifodada | Shartni teskari yozish |
| `WHERE id IN (juda katta ro'yxat)` | Planner rejani o'zgartiradi | `= ANY(?)` massiv yoki vaqtinchalik jadval |
| `ORDER BY` indeks tartibiga mos emas | Sort kerak | Indeksni tartibga moslash |
| `WHERE a = ? OR b = ?` | Ikki indeksni birlashtirish qiyin | `UNION ALL` yoki ikki so'rov |
| Tur mos kelmasligi (`uuid` va `text`) | Implicit cast | Turlarni moslash |
| `WHERE nullable_col = ?` NULL bilan | `= NULL` hech narsa topmaydi | `IS NULL` |
| Timezone konversiyasi ustunda | Funksiya | Parametrni konvertatsiya qilish |

```sql
-- Review da bu farqni ko'rsatish: ikkisi bir xil natija, boshqa reja.
-- Yomon: har qator uchun date() hisoblanadi.
EXPLAIN (ANALYZE, BUFFERS)
SELECT count(*) FROM orders WHERE date(created_at) = '2026-10-01';
-- Seq Scan on orders (cost=... rows=...) actual time=1250ms

-- Yaxshi: indeks oralig'i.
EXPLAIN (ANALYZE, BUFFERS)
SELECT count(*) FROM orders
 WHERE created_at >= '2026-10-01' AND created_at < '2026-10-02';
-- Index Only Scan using orders_created_at_idx ... actual time=3ms
```

## 24.2 Yangi indeks qo'shilganda review savollari

```sql
-- Diffda yangi indeks. Review da yetti savol.
CREATE INDEX orders_customer_status_idx ON orders (customer_id, status);
```

1. Ustunlar tartibi to'g'rimi. Tenglik shartidagi ustunlar oldinda, oraliq shartidagi keyin. `WHERE customer_id = ? AND created_at > ?` uchun `(customer_id, created_at)`, teskarisi emas.
2. Bu indeks mavjud indeksning prefiksi emasmi. `(customer_id)` indeksi bo'lsa, `(customer_id, status)` uni o'z ichiga oladi - eskisini olib tashlash kerak.
3. Selektivlik qanday. `status` ustunida 3 qiymat bo'lsa va 95% `CLOSED` bo'lsa, planner bu indeksni ishlatmaydi. Partial indeks kerak.
4. Yozuv narxi hisobga olinganmi. Har indeks `INSERT`/`UPDATE` ni sekinlashtiradi va joy egallaydi.
5. `CONCURRENTLY` ishlatilganmi. Katta jadvalda `CREATE INDEX` yozuvni bloklaydi.
6. Hajmi qancha bo'ladi. 40 mln qatorli jadvalda indeks gigabaytlarga chiqadi.
7. Qaysi so'rov buni ishlatadi va reja tasdiqlanganmi.

```sql
-- Partial indeks: kichik va samarali.
CREATE INDEX CONCURRENTLY orders_open_idx ON orders (customer_id, created_at DESC)
    WHERE status IN ('NEW', 'PAID');
-- 40 mln qatorli jadvalda ochiq buyurtmalar 50 ming bo'lsa, indeks
-- 1000 baravar kichik va keshda to'liq turadi.

-- Covering indeks: Index Only Scan uchun (jadvalga tegmaydi).
CREATE INDEX CONCURRENTLY orders_lookup_idx ON orders (number) INCLUDE (status, total);

-- Mavjud indekslarni va ularning ishlatilishini ko'rish: review dalili.
SELECT indexrelname, idx_scan, idx_tup_read,
       pg_size_pretty(pg_relation_size(indexrelid)) AS hajm
  FROM pg_stat_user_indexes
 WHERE relname = 'orders'
 ORDER BY idx_scan;
-- idx_scan = 0 bo'lgan indekslar - o'lik yuk, olib tashlanishi kerak.

-- Dublikat va bir-birini qoplaydigan indekslarni topish.
SELECT a.indexrelid::regclass AS ortiqcha, b.indexrelid::regclass AS qoplaydi
  FROM pg_index a JOIN pg_index b
    ON a.indrelid = b.indrelid AND a.indexrelid <> b.indexrelid
   AND array_to_string(a.indkey, ' ') LIKE array_to_string(b.indkey, ' ') || '%'
 WHERE NOT a.indisprimary;
```

## 24.3 So'rov rejasini o'qish: review uchun minimal bilim

| Rejada ko'rilgan | Ma'nosi | Qachon muammo |
| --- | --- | --- |
| `Seq Scan` | Butun jadval o'qiladi | Katta jadvalda filtr bilan |
| `Index Scan` | Indeks + jadval | Normal |
| `Index Only Scan` | Faqat indeks | Eng yaxshi |
| `Bitmap Heap Scan` | Ko'p qator, indeks orqali | Odatda normal |
| `Nested Loop` | Har qator uchun ichki so'rov | Tashqi qatorlar ko'p bo'lsa |
| `Hash Join` | Hash jadval quriladi | `work_mem` yetmasa diskka tushadi |
| `Merge Join` | Ikki tartiblangan oqim | Normal |
| `Sort` + `Disk` | Saralash diskka tushgan | `work_mem` oshirish yoki indeks |
| `rows=1000` vs `actual rows=500000` | Statistika xato | `ANALYZE` kerak yoki shart murakkab |
| `Filter: ... Rows Removed by Filter: 2000000` | Ortiqcha qator o'qilgan | Indeks yo'q |
| `Buffers: read=50000` | Diskdan o'qish | Kesh yetmaydi |

```sql
-- Review da so'rash kerak bo'lgan to'liq shakl: BUFFERS va ANALYZE bilan.
EXPLAIN (ANALYZE, BUFFERS, VERBOSE, SETTINGS)
SELECT ...;
-- SETTINGS - standart bo'lmagan planner sozlamalarini ko'rsatadi.
-- Review izohi: "EXPLAIN (ANALYZE, BUFFERS) natijasini qo'shsangiz,
-- rejani birga ko'ramiz" - bu eng foydali so'rov.
```

## 24.4 JOIN va agregat so'rovlari

```sql
-- Naqsh: JOIN natijasida qatorlar ko'payib, SUM noto'g'ri bo'lishi.
SELECT o.id, sum(l.amount) AS total, sum(p.amount) AS paid
  FROM orders o
  JOIN order_line l ON l.order_id = o.id        -- 3 qator
  JOIN payment p ON p.order_id = o.id           -- 2 qator
 GROUP BY o.id;
-- Natija: 6 qator (3 x 2), total 2 baravar, paid 3 baravar katta!
-- Bu eng ko'p uchraydigan SQL xatosi va test bilan tutilmasligi mumkin
-- (bitta to'lov va bitta qator bo'lsa, natija to'g'ri chiqadi).

-- To'g'ri: alohida agregatlar yoki lateral.
SELECT o.id,
       (SELECT sum(amount) FROM order_line WHERE order_id = o.id) AS total,
       (SELECT sum(amount) FROM payment    WHERE order_id = o.id) AS paid
  FROM orders o;
-- Yoki LATERAL bilan (ko'p ustun kerak bo'lsa):
SELECT o.id, l.total, p.paid
  FROM orders o
  LEFT JOIN LATERAL (SELECT sum(amount) AS total FROM order_line WHERE order_id = o.id) l ON true
  LEFT JOIN LATERAL (SELECT sum(amount) AS paid  FROM payment    WHERE order_id = o.id) p ON true;
```

```sql
-- Naqsh: LEFT JOIN WHERE bilan INNER JOIN ga aylanadi.
SELECT o.* FROM orders o
  LEFT JOIN payment p ON p.order_id = o.id
 WHERE p.status = 'OK';          -- to'lovsiz buyurtmalar tushib qoladi!
-- To'g'ri: shart JOIN ichida.
 LEFT JOIN payment p ON p.order_id = o.id AND p.status = 'OK';

-- Naqsh: NOT IN va NULL.
SELECT * FROM orders WHERE customer_id NOT IN (SELECT id FROM blocked_customer);
-- Agar blocked_customer.id da bitta NULL bo'lsa - natija BO'SH bo'ladi.
-- To'g'ri: NOT EXISTS (NULL ga chidamli va odatda tezroq).
SELECT * FROM orders o WHERE NOT EXISTS (
    SELECT 1 FROM blocked_customer b WHERE b.id = o.customer_id);
```

## 24.5 Dinamik SQL review

```java
// Naqsh: shartlar satr qo'shish bilan quriladi.
StringBuilder sql = new StringBuilder("SELECT * FROM orders WHERE 1=1");
if (status != null) sql.append(" AND status = '").append(status).append("'");   // injection
if (from != null)   sql.append(" AND created_at >= '").append(from).append("'");
if (sortBy != null) sql.append(" ORDER BY ").append(sortBy);                   // injection

// To'g'ri: parametrlar bilan, tartiblash whitelist orqali ([29-bob](29-injection-review-sql-va-boshqalar.md)).
var sql = new StringBuilder("SELECT id, number, total FROM orders WHERE 1=1");
var params = new MapSqlParameterSource();
if (status != null) { sql.append(" AND status = :status"); params.addValue("status", status.name()); }
if (from != null)   { sql.append(" AND created_at >= :from"); params.addValue("from", from); }
sql.append(" ORDER BY ").append(SortColumn.of(sortBy).sql());    // enum: xavfsiz
sql.append(" LIMIT :limit");                                     // chegara majburiy
params.addValue("limit", Math.min(size, 100));

// Yoki JPA Criteria / jOOQ / QueryDSL - tipli qurish.
// Review tavsiyasi: uchdan ko'p ixtiyoriy shart bo'lsa, satr qurish
// o'rniga tipli qurilma ishlatish - injection xavfi strukturaviy
// ravishda yo'qoladi.
```

## 24.6 Katta jadvallar bilan ishlash

```sql
-- Naqsh: COUNT(*) katta jadvalda har sahifada.
SELECT count(*) FROM orders WHERE status = 'CLOSED';   -- 38 mln qator sanaladi
-- Review izohi: Spring Data `Page` har so'rovda COUNT bajaradi. Bu
-- 38 mln qatorli jadvalda 2-4 sekund. Yechimlar:
--   1) `Slice` ishlatish (COUNT yo'q, faqat "keyingi sahifa bormi");
--   2) taxminiy son: pg_class.reltuples;
--   3) alohida keshlangan hisoblagich.
SELECT reltuples::bigint AS taxminiy FROM pg_class WHERE relname = 'orders';

-- Naqsh: DELETE katta hajmda - uzoq qulf va WAL to'lishi.
DELETE FROM audit_log WHERE created_at < now() - interval '1 year';   -- 50 mln qator
-- To'g'ri: bo'laklab.
DO $$
DECLARE deleted int;
BEGIN
  LOOP
    DELETE FROM audit_log WHERE id IN (
        SELECT id FROM audit_log
         WHERE created_at < now() - interval '1 year'
         LIMIT 10000);
    GET DIAGNOSTICS deleted = ROW_COUNT;
    EXIT WHEN deleted = 0;
    COMMIT;                      -- har bo'lak alohida tranzaksiyada
    PERFORM pg_sleep(0.1);       -- replikatsiyaga nafas berish
  END LOOP;
END $$;
-- Eng yaxshi yechim: partitsiyalash va DROP PARTITION (bir zumda).
```

## 24.7 JSONB review

```sql
-- JSONB qulay, lekin review da uch savol bor.
-- 1) Nega JSONB va nega oddiy ustun emas?
--    Agar maydon har doim bor va u bo'yicha filtrlanadi - ustun bo'lishi kerak.
-- 2) Indeks bormi?
CREATE INDEX orders_meta_gin ON orders USING gin (metadata jsonb_path_ops);
-- Yoki aniq yo'l uchun ifoda indeksi (kichikroq va tezroq):
CREATE INDEX orders_channel_idx ON orders ((metadata->>'channel'));
-- 3) Sxema qanday nazorat qilinadi?
ALTER TABLE orders ADD CONSTRAINT metadata_shape CHECK (
    jsonb_typeof(metadata) = 'object'
    AND metadata ? 'channel'                     -- majburiy kalit
    AND metadata->>'channel' IN ('WEB', 'APP', 'POS')
);
-- JSONB da sxema bo'lmasa, u "nima bo'lsa shu" maydoniga aylanadi va
-- bir yildan keyin undagi ma'lumotni hech kim ishonchli o'qiy olmaydi.
```

## 24.8 Review paytida so'rovni o'lchash

```bash
# Review da dalil to'plash: eng qimmat so'rovlar va yangi so'rovning rejasi.
# 1) Prodda eng ko'p vaqt oladigan so'rovlar (pg_stat_statements kerak).
psql -c "SELECT calls,
                round(mean_exec_time::numeric, 1) AS avg_ms,
                round(total_exec_time::numeric/1000, 1) AS total_s,
                rows/greatest(calls,1) AS rows_per_call,
                left(query, 90) AS sorov
           FROM pg_stat_statements
          ORDER BY total_exec_time DESC LIMIT 15;"

# 2) Indekssiz skanerlar ko'p bo'lgan jadvallar.
psql -c "SELECT relname, seq_scan, seq_tup_read, idx_scan,
                seq_tup_read / greatest(seq_scan, 1) AS avg_rows_per_scan
           FROM pg_stat_user_tables
          WHERE seq_scan > 100
          ORDER BY seq_tup_read DESC LIMIT 10;"

# 3) PR dagi yangi so'rovning rejasini staging da olish.
psql -c "EXPLAIN (ANALYZE, BUFFERS) <yangi so'rov>"

# 4) Ilova yuborayotgan haqiqiy SQL ni ko'rish (lokal).
#    logging.level.org.hibernate.SQL=debug yoki
psql -c "ALTER SYSTEM SET log_min_duration_statement = '200ms';" -c "SELECT pg_reload_conf();"
```

## 24.9 Review checklisti: SQL va indekslar

| Savol | Nega |
| --- | --- |
| Filtr ustuni funksiya ichida emasmi | Indeks ishlamaydi |
| Yangi `WHERE`/`ORDER BY` ustuni indekslanganmi | Seq scan |
| Indeks ustunlari tartibi to'g'rimi | Prefiks qoidasi |
| Indeks mavjudining dublikati emasmi | Ortiqcha yozuv narxi |
| Katta jadvalda `CONCURRENTLY` ishlatilganmi | Yozuv bloklanishi |
| `LIMIT` majburiymi | Chegarasiz natija |
| Pagination tartibida yagona kalit bormi | Takrorlanish |
| Ko'p `JOIN` da agregat ko'paymaydimi | Noto'g'ri `SUM` |
| `LEFT JOIN` sharti `ON` dami | Jim `INNER JOIN` |
| `NOT IN` da NULL xavfi bormi | Bo'sh natija |
| Dinamik SQL parametrlar bilanmi | Injection |
| Katta `DELETE`/`UPDATE` bo'laklanganmi | Qulf va WAL |
| JSONB da indeks va sxema nazorati bormi | O'qilmaydigan ma'lumot |
| `COUNT(*)` har sahifada bajarilmaydimi | Sekin pagination |

## 24.10 Amalda qo'llash

- [ ] `pg_stat_statements` ni yoqib, eng qimmat 15 so'rovni oling va ularning har biri kodda qayerdan kelayotganini aniqlang.
- [ ] `pg_stat_user_indexes` dan `idx_scan = 0` bo'lgan indekslarni toping va olib tashlashni rejalashtiring.
- [ ] Bir-birini qoplaydigan indekslarni aniqlaydigan so'rovni ishga tushirib, ortiqchalarini belgilang.
- [ ] Filtrda funksiya ishlatilgan so'rovlarni (`date(...)`, `lower(...)`) toping va oraliq yoki ifoda indeksiga o'tkazing.
- [ ] Ko'p `JOIN` va `SUM` ishlatadigan hisobotlarni tekshirib, qatorlar ko'payishi natijani buzmasligini test bilan tasdiqlang.
- [ ] Dinamik SQL quruvchi joylarni toping va tartiblash ustunlarini enum whitelist ga o'tkazing.
- [ ] `Page` ishlatadigan katta jadval so'rovlarini `Slice` yoki keyset pagination ga o'tkazing.
- [ ] Yangi indeks qo'shadigan PR lar uchun `EXPLAIN (ANALYZE, BUFFERS)` natijasini majburiy talab qilib qo'ying.
- [ ] JSONB ustunlari uchun `CHECK` constraint va indeks borligini tekshiring.

---

[&larr; 23. JPA va Hibernate review](23-jpa-va-hibernate-review.md) · [Mundarija](README.md) · [25. Migratsiya review: qulf, backfill, orqaga moslik &rarr;](25-migratsiya-review-qulf-backfill-orqaga.md)
