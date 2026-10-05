<!-- doc: code-review | chapter: 25 | part: V. PostgreSQL va ma'lumot qatlami review -->

[Barcha hujjatlar](../../README.md) / [Kod review](README.md)

# 25. Migratsiya review: qulf, backfill, orqaga moslik (Reviewing Migrations)

<details>
<summary>Bu bobdagi 9 bo'lim</summary>

- [25.1 Birinchi savol: bu operatsiya qanday qulf oladi](#251-birinchi-savol-bu-operatsiya-qanday-qulf-oladi)
- [25.2 Qulf kutish navbati: yashirin kaskad](#252-qulf-kutish-navbati-yashirin-kaskad)
- [25.3 Orqaga moslik: deploy tartibi](#253-orqaga-moslik-deploy-tartibi)
- [25.4 Backfill review](#254-backfill-review)
- [25.5 Qaytarish rejasi](#255-qaytarish-rejasi)
- [25.6 Migratsiya fayllarining o'zi](#256-migratsiya-fayllarining-ozi)
- [25.7 Migratsiyani sinash](#257-migratsiyani-sinash)
- [25.8 Review checklisti: migratsiya](#258-review-checklisti-migratsiya)
- [25.9 Amalda qo'llash](#259-amalda-qollash)

</details>


Migratsiya - review ning eng yuqori xavfli qismi. Sababi oddiy: kodni qaytarish mumkin, ma'lumotni qaytarish ko'pincha mumkin emas. Bundan tashqari migratsiya diffda zararsiz ko'rinadi - bitta `ALTER TABLE` qatori. Shu qator 12 million qatorli jadvalda 8 daqiqa davomida barcha yozuvlarni bloklashi mumkin, ya'ni to'liq to'xtash. Shu sababli migratsiyaga tegadigan PR har doim eng chuqur review darajasini oladi.

## 25.1 Birinchi savol: bu operatsiya qanday qulf oladi

PostgreSQL da har bir DDL operatsiyasi qulf oladi, va qulf turi hamma narsani belgilaydi. `ACCESS EXCLUSIVE` qulfi jadvalga har qanday murojaatni - hatto `SELECT` ni ham - bloklaydi.

| Operatsiya | Qulf | Davomiyligi | Xavf |
| --- | --- | --- | --- |
| `ADD COLUMN` (standart qiymatsiz, nullable) | ACCESS EXCLUSIVE | Bir zumda (metadata) | Past |
| `ADD COLUMN ... DEFAULT <const>` (PG 11+) | ACCESS EXCLUSIVE | Bir zumda | Past |
| `ADD COLUMN ... DEFAULT <volatile>` | ACCESS EXCLUSIVE | Jadvalni qayta yozadi | Juda yuqori |
| `ADD COLUMN ... NOT NULL` qiymatsiz | ACCESS EXCLUSIVE | Xato beradi (mavjud qatorlar) | - |
| `DROP COLUMN` | ACCESS EXCLUSIVE | Bir zumda (mantiqiy) | O'rtacha (kod moslik) |
| `ALTER COLUMN TYPE` | ACCESS EXCLUSIVE | Jadvalni qayta yozadi | Juda yuqori |
| `ALTER COLUMN SET NOT NULL` | ACCESS EXCLUSIVE | To'liq skan | Yuqori |
| `ADD CONSTRAINT CHECK` | ACCESS EXCLUSIVE | To'liq skan | Yuqori |
| `ADD CONSTRAINT ... NOT VALID` | ACCESS EXCLUSIVE | Bir zumda | Past |
| `VALIDATE CONSTRAINT` | SHARE UPDATE EXCLUSIVE | To'liq skan, lekin yozuv o'tadi | Past |
| `ADD FOREIGN KEY` | Ikki jadvalda SHARE ROW EXCLUSIVE | Skan | Yuqori |
| `CREATE INDEX` | SHARE (yozuv bloklanadi) | Uzoq | Yuqori |
| `CREATE INDEX CONCURRENTLY` | SHARE UPDATE EXCLUSIVE | Uzoqroq, lekin yozuv o'tadi | Past |
| `DROP INDEX CONCURRENTLY` | SHARE UPDATE EXCLUSIVE | Tez | Past |
| `RENAME COLUMN` | ACCESS EXCLUSIVE | Bir zumda | Yuqori (kod moslik) |
| `TRUNCATE` | ACCESS EXCLUSIVE | Tez | Juda yuqori (ma'lumot) |

```sql
-- Review da to'xtatiladigan migratsiya: diffda bir qator.
ALTER TABLE orders ADD COLUMN risk_score numeric(5,2) NOT NULL DEFAULT random();
-- Uch muammo: (1) volatile default - 12 mln qator qayta yoziladi;
-- (2) ACCESS EXCLUSIVE qulfi shu vaqt davomida hamma so'rovni bloklaydi;
-- (3) jadval hajmi ikki baravar oshadi (eski versiyalar VACUUM gacha qoladi).

-- Xavfsiz ketma-ketlik: uch qadam, har biri tez.
-- 1-qadam (bu reliz): nullable ustun qo'shish - bir zumda.
ALTER TABLE orders ADD COLUMN risk_score numeric(5,2);

-- 2-qadam (alohida ish): bo'laklab to'ldirish, qulfsiz.
--   UPDATE orders SET risk_score = ... WHERE risk_score IS NULL AND id IN (...)
--   har 10 000 qator, alohida tranzaksiya.

-- 3-qadam (keyingi reliz): NOT NULL ni arzon qo'shish.
ALTER TABLE orders ADD CONSTRAINT risk_score_not_null
    CHECK (risk_score IS NOT NULL) NOT VALID;      -- bir zumda
ALTER TABLE orders VALIDATE CONSTRAINT risk_score_not_null;  -- yozuvni bloklamaydi
-- (PG 12+ da: constraint validatsiya qilingach SET NOT NULL arzon bo'ladi)
```

## 25.2 Qulf kutish navbati: yashirin kaskad

Eng ko'p e'tibordan chetda qoladigan mexanizm: `ACCESS EXCLUSIVE` qulfini kutayotgan DDL o'zidan keyingi barcha so'rovlarni ham bloklaydi, hatto ular `SELECT` bo'lsa ham.

```text
T1: uzoq SELECT ishlayapti (30 sekund, hisobot)        -> ACCESS SHARE qulfi
T2: ALTER TABLE ... kutadi (T1 tugashini)              -> ACCESS EXCLUSIVE so'raydi
T3: oddiy SELECT                                        -> T2 ortida navbatda qoladi!
T4..T200: barcha so'rovlar navbatda                     -> ilova to'xtaydi
```

Shu sababli migratsiya uchun `lock_timeout` majburiy: DDL qulfni darhol olmasa, voz kechadi va keyin qayta urinadi, navbat yaratmaydi.

```sql
-- Har bir xavfli migratsiyaning boshida: qulfni kutmaslik.
SET lock_timeout = '3s';
SET statement_timeout = '30s';
ALTER TABLE orders ADD COLUMN risk_score numeric(5,2);
-- Qulf 3 sekundda olinmasa: "canceling statement due to lock timeout"
-- Migratsiya yiqiladi, lekin ilova to'xtamaydi. Keyin qayta urinish mumkin.
```

```sql
-- Flyway da har migratsiya uchun sozlash (yoki alohida fayl boshida).
-- V42__add_risk_score.sql
SET lock_timeout = '3s';
ALTER TABLE orders ADD COLUMN risk_score numeric(5,2);
```

## 25.3 Orqaga moslik: deploy tartibi

Migratsiya va kod bir vaqtda ishga tushmaydi. Rolling deploy da eski va yangi kod bir necha daqiqa (yoki soat) birga ishlaydi. Shu sababli migratsiya har doim ikki tomonga mos bo'lishi kerak.

| O'zgarish | Eski kod bilan ishlaydimi | To'g'ri ketma-ketlik |
| --- | --- | --- |
| Nullable ustun qo'shish | Ha | Bitta reliz |
| `NOT NULL` ustun qo'shish | Yo'q (eski kod uni to'ldirmaydi) | Nullable qo'shish -> kod -> NOT NULL |
| Ustun olib tashlash | Yo'q (eski kod o'qiydi) | Kodni tozalash -> keyingi relizda DROP |
| Ustun nomini o'zgartirish | Yo'q | Yangi ustun -> ikkisiga yozish -> ko'chirish -> eskisini olib tashlash |
| Turni o'zgartirish | Ko'pincha yo'q | Yangi ustun bilan ko'chirish |
| Jadval nomini o'zgartirish | Yo'q | View bilan o'tish davri |
| Enum qiymati qo'shish | Ha (eski kod uni bilmaydi, lekin o'qiydi) | Avval DB, keyin kod |
| Enum qiymatini olib tashlash | Yo'q | Avval kod, keyin DB |
| Unique constraint qo'shish | Faqat ma'lumot toza bo'lsa | Dublikatlarni tozalash -> `CONCURRENTLY` indeks -> constraint |

```sql
-- Ustun nomini o'zgartirish: to'rt relizli naqsh ("expand and contract").
-- Review da bitta RENAME ko'rilsa, bu blocker.

-- RELIZ 1: yangi ustun qo'shish (nullable).
ALTER TABLE customer ADD COLUMN phone_e164 text;

-- RELIZ 1 kodi: ikkisiga ham yozadi, eskisidan o'qiydi.
--   customer.setPhone(p); customer.setPhoneE164(normalize(p));

-- RELIZ 2: eski ma'lumotni ko'chirish (bo'laklab, migratsiyadan tashqarida).
--   UPDATE customer SET phone_e164 = normalize(phone)
--    WHERE phone_e164 IS NULL AND id BETWEEN ? AND ?;

-- RELIZ 2 kodi: yangisidan o'qiydi, ikkisiga yozadi.

-- RELIZ 3 kodi: faqat yangisi bilan ishlaydi.

-- RELIZ 4: eski ustunni olib tashlash.
ALTER TABLE customer DROP COLUMN phone;
```

Review izohining shakli bunday holatda: "`RENAME COLUMN` rolling deploy da eski podlarni darhol sindiradi. Bizda 6 pod va deploy 4 daqiqa davom etadi - shu vaqt ichida barcha so'rovlar `column phone does not exist` beradi. Expand-and-contract ketma-ketligi kerak."

## 25.4 Backfill review

Katta jadvaldagi ma'lumotni to'ldirish - alohida xavf sinfi. Uni migratsiya fayliga qo'yish deyarli har doim xato.

```sql
-- Blocker: migratsiya ichida butun jadvalga UPDATE.
UPDATE orders SET risk_score = 0 WHERE risk_score IS NULL;   -- 12 mln qator
-- Oqibatlari: (1) bitta tranzaksiya, 12 mln qator qulflanadi;
-- (2) WAL hajmi gigabaytlarga chiqadi, replikatsiya lag o'sadi;
-- (3) migratsiya 20 daqiqa ishlaydi, deploy timeout iga tushadi;
-- (4) yarmida yiqilsa, hammasi qaytadi va qaytadan boshlanadi;
-- (5) jadval bo'rtadi (bloat) - har qator yangi versiya oladi.
```

```java
// To'g'ri: backfill alohida, boshqarilishi mumkin, kuzatiladigan ish.
@Component
public class RiskScoreBackfill {

    private static final int BATCH = 5_000;

    @Scheduled(fixedDelay = 1_000)
    public void run() {
        if (!enabled) return;
        // Idempotent: faqat to'ldirilmagan qatorlar, ID bo'yicha oldinga yurish.
        int updated = jdbc.update("""
            UPDATE orders SET risk_score = 0
             WHERE id IN (SELECT id FROM orders
                           WHERE risk_score IS NULL
                           ORDER BY id
                           LIMIT ?)
            """, BATCH);
        processed.addAndGet(updated);
        meter.gauge("backfill.remaining", remainingCount());
        if (updated == 0) { enabled = false; log.info("backfill tugadi"); }
    }
}
// Review talablari backfill uchun:
// 1) bo'lak hajmi va tezlik boshqariladi (to'xtatish imkoni bor);
// 2) idempotent - qayta ishga tushirish xavfsiz;
// 3) progress o'lchanadi va alert bor;
// 4) replikatsiya lag kuzatiladi va kerak bo'lsa sekinlashtiriladi;
// 5) yangi yozuvlar ham to'g'ri qiymat oladi (kod yoki DEFAULT).
```

## 25.5 Qaytarish rejasi

```sql
-- Review savoli har bir migratsiya uchun: qaytarish qanday?
-- Flyway da `undo` faqat tijorat versiyasida, shu sababli qaytarish
-- rejasi yozma bo'lishi kerak, kodda emas.
```

| Migratsiya turi | Qaytarish |
| --- | --- |
| Ustun qo'shish | `DROP COLUMN` - xavfsiz, lekin ma'lumot ketadi |
| Indeks qo'shish | `DROP INDEX CONCURRENTLY` - xavfsiz |
| Ustun olib tashlash | Qaytarilmaydi - ma'lumot yo'q |
| Turni o'zgartirish | Qaytarilmaydi - aniqlik yo'qolgan bo'lishi mumkin |
| Ma'lumot ko'chirish | Faqat eski ma'lumot saqlangan bo'lsa |
| `DROP TABLE` | Faqat backup dan |
| Constraint qo'shish | `DROP CONSTRAINT` - xavfsiz |

Review qoidasi: qaytarilmaydigan migratsiya (ustun yoki jadval o'chirish, tur o'zgartirish) alohida relizda va alohida tasdiq bilan boriladi. Bundan tashqari o'chirish oldidan kutish davri bo'lishi kerak: ustun kodda ishlatilmay qolgandan keyin kamida bir reliz kutiladi, shunda qaytarish imkoni saqlanadi.

```sql
-- Qaytarish imkonini saqlash: o'chirish o'rniga ko'chirish.
-- Jadvalni darhol o'chirish o'rniga:
ALTER TABLE legacy_orders RENAME TO legacy_orders_deprecated_20261004;
-- Bir oydan keyin, hech kim shikoyat qilmagach:
DROP TABLE legacy_orders_deprecated_20261004;
```

## 25.6 Migratsiya fayllarining o'zi

| Review savoli | Nega |
| --- | --- |
| Fayl nomi konvensiyaga mosmi | `V42__add_risk_score.sql` - raqam va tavsif |
| Mavjud migratsiya o'zgartirilmaganmi | Checksum buziladi, Flyway yiqiladi |
| Raqam konflikti bormi (ikki branch) | Ikki PR da `V42` - merge dan keyin xato |
| Migratsiya idempotentmi | `IF NOT EXISTS` kerak bo'lgan joylarda |
| Tranzaksiyada bajariladimi | PostgreSQL DDL tranzaksion, lekin `CONCURRENTLY` emas |
| `CONCURRENTLY` alohida faylda bormi | Tranzaksiya ichida ishlamaydi |
| Ma'lumot o'zgartirish bormi | Backfill alohida bo'lishi kerak |
| Sinalganmi va qancha vaqt oldi | Real hajmdagi nusxada |

```sql
-- CREATE INDEX CONCURRENTLY tranzaksiya ichida ishlamaydi.
-- Flyway da bu fayl uchun tranzaksiyani o'chirish kerak:
-- V43__add_orders_index.sql
-- flyway:executeInTransaction=false
CREATE INDEX CONCURRENTLY IF NOT EXISTS orders_open_idx
    ON orders (customer_id, created_at DESC)
    WHERE status IN ('NEW', 'PAID');
-- Diqqat: CONCURRENTLY yiqilsa, yaroqsiz (invalid) indeks qoladi va u
-- so'rovlarda ishlatilmaydi, lekin yozuvni sekinlashtiradi. Tekshirish:
--   SELECT indexrelid::regclass FROM pg_index WHERE NOT indisvalid;
```

```bash
# Migratsiya raqami konfliktini CI da tutish.
# Ikki branch bir xil versiya raqamini ishlatsa, merge dan keyin bilinadi.
ls src/main/resources/db/migration/V*.sql \
  | sed -E 's/.*\/V([0-9]+)__.*/\1/' | sort | uniq -d \
  | while read -r dup; do echo "XATO: V$dup takrorlangan"; exit 1; done

# Mavjud migratsiya o'zgartirilganini tutish (checksum buzilishi).
git diff --name-status origin/main...HEAD -- 'src/main/resources/db/migration/' \
  | awk '$1=="M" {print "XATO: mavjud migratsiya tahrirlangan: "$2}'
```

## 25.7 Migratsiyani sinash

```bash
# Review da talab qilinadigan dalil: migratsiya real hajmda sinalgan.
# 1) Prod nusxasida (yoki shunga yaqin hajmda) vaqtni o'lchash.
pg_dump --schema-only prod_db > schema.sql
psql -c "CREATE DATABASE migration_test;"
psql migration_test < schema.sql
# Ma'lumot hajmini generatsiya qilish (yoki anonimlashtirilgan nusxa).
psql migration_test -c "INSERT INTO orders SELECT ... FROM generate_series(1, 12000000);"

# 2) Migratsiyani o'lchash va qulfni kuzatish.
psql migration_test -c "\timing on" -f src/main/resources/db/migration/V42__add_risk_score.sql

# 3) Migratsiya ishlayotganda boshqa sessiyada yozuv o'tadimi - tekshirish.
#    1-terminal: migratsiya; 2-terminal:
psql migration_test -c "INSERT INTO orders (id, number) VALUES (gen_random_uuid(), 'test');"
#    Agar bu buyruq kutsa - migratsiya yozuvni bloklaydi.

# 4) Tozalash.
psql -c "DROP DATABASE migration_test;"
```

```java
// Testcontainers bilan avtomatik tekshiruv: migratsiyalar toza bazada
// va mavjud ma'lumot bilan ishlaydimi.
@Test
void migrationsRunOnSchemaWithExistingData() {
    try (PostgreSQLContainer<?> pg = new PostgreSQLContainer<>("postgres:16")) {
        pg.start();
        // 1) Avvalgi relizning sxemasiga ko'chish.
        Flyway.configure().dataSource(pg.getJdbcUrl(), pg.getUsername(), pg.getPassword())
              .target(MigrationVersion.fromVersion("41"))
              .load().migrate();
        // 2) Mavjud ma'lumotni qo'yish (eski kod yozadigan shakl).
        insertLegacyRows(pg, 10_000);
        // 3) Yangi migratsiyalarni qo'llash - xatosiz o'tishi kerak.
        MigrateResult r = Flyway.configure()
              .dataSource(pg.getJdbcUrl(), pg.getUsername(), pg.getPassword())
              .load().migrate();
        assertThat(r.success).isTrue();
        // 4) Ma'lumot buzilmaganini tekshirish.
        assertThat(countRows(pg, "orders")).isEqualTo(10_000);
    }
}
```

## 25.8 Review checklisti: migratsiya

| Savol | Nega |
| --- | --- |
| Qanday qulf oladi va qancha vaqt | To'liq to'xtash xavfi |
| `lock_timeout` qo'yilganmi | Navbat kaskadi |
| Jadval qayta yozilmaydimi | Uzoq qulf va hajm |
| Rolling deploy da eski kod ishlaydimi | Deploy paytida xatolar |
| Backfill alohida va bo'laklanganmi | WAL, lag, bloat |
| Yangi yozuvlar to'g'ri qiymat oladimi | Yarim to'ldirilgan ustun |
| Qaytarish rejasi yozilganmi | Reliz qaytarilmasligi |
| `CONCURRENTLY` alohida, tranzaksiyasiz faylmi | Xato |
| Versiya raqami konflikti yo'qmi | Merge dan keyin yiqilish |
| Mavjud migratsiya o'zgartirilmaganmi | Checksum |
| Real hajmda sinalganmi va vaqti o'lchanganmi | Taxminiy xavf |
| Ma'lumot yo'qotadigan operatsiya alohida relizdami | Qaytarib bo'lmaslik |
| FK va unique qo'shishda mavjud ma'lumot tozami | Migratsiya yiqilishi |

## 25.9 Amalda qo'llash

- [ ] Migratsiya fayllarini o'zgartiradigan PR lar uchun `CODEOWNERS` da majburiy reviewer belgilang.
- [ ] Qulf turlari jadvalini `REVIEW.md` ga qo'shing va har migratsiya PR ida shu jadval bo'yicha javob talab qiling.
- [ ] Barcha migratsiya fayllariga `SET lock_timeout` qo'yish konvensiyasini joriy qiling.
- [ ] Migratsiya versiya raqami konflikti va mavjud fayl o'zgarishini tutadigan CI tekshiruvini qo'shing.
- [ ] Yaroqsiz indekslarni (`NOT indisvalid`) kuzatadigan monitoring so'rovini qo'shing.
- [ ] Testcontainers bilan "avvalgi versiyaga ko'chish -> ma'lumot qo'yish -> yangi migratsiyalar" testini yozing.
- [ ] Eng katta beshta jadval hajmini `REVIEW.md` ga yozib qo'ying - reviewer qulf xavfini tez baholashi uchun.
- [ ] Ma'lumot yo'qotadigan migratsiyalar uchun "ko'chirib nomlash va bir oy kutish" konvensiyasini kelishib oling.
- [ ] Backfill lar uchun standart shablon (bo'lak, idempotentlik, progress metrikasi, to'xtatish kaliti) tayyorlang.

---

[&larr; 24. SQL, so'rov rejasi va indeks review](24-sql-sorov-rejasi-va-indeks-review.md) · [Mundarija](README.md) · [26. Ma'lumot to'g'riligi va turlar review &rarr;](26-malumot-togriligi-va-turlar-review.md)
