<!-- doc: architect | chapter: 33 | part: VI. Amaliyot va o'sish -->

[Barcha hujjatlar](../../README.md) / [Arxitektor miyasi](README.md)

# 33. Sxema migratsiyasi va to'xtashsiz reliz (Schema Migration and Zero-Downtime Release)

<details>
<summary>Bu bobdagi 13 bo'lim</summary>

- [33.1 Migratsiya vositalari: Flyway va Liquibase, versiyalash va nomlash tartibi](#331-migratsiya-vositalari-flyway-va-liquibase-versiyalash-va-nomlash-tartibi)
- [33.2 Migratsiya qoidalari: oldinga faqat yangi fayl, qo'lda o'zgartirmaslik](#332-migratsiya-qoidalari-oldinga-faqat-yangi-fayl-qolda-ozgartirmaslik)
- [33.3 Kengaytirish va qisqartirish (expand and contract) usuli bosqichma-bosqich](#333-kengaytirish-va-qisqartirish-expand-and-contract-usuli-bosqichma-bosqich)
- [33.4 Ustun qo'shish, nomini o'zgartirish va o'chirishning xavfsiz ketma-ketligi](#334-ustun-qoshish-nomini-ozgartirish-va-ochirishning-xavfsiz-ketma-ketligi)
- [33.5 Qaysi DDL jadvalni bloklaydi: `ALTER TABLE` turlarining lock darajasi](#335-qaysi-ddl-jadvalni-bloklaydi-alter-table-turlarining-lock-darajasi)
- [33.6 Katta jadvalga ustun qo'shish va standart qiymat masalasi](#336-katta-jadvalga-ustun-qoshish-va-standart-qiymat-masalasi)
- [33.7 `NOT NULL` va `CHECK` cheklovini to'xtashsiz qo'shish (`NOT VALID` va `VALIDATE`)](#337-not-null-va-check-cheklovini-toxtashsiz-qoshish-not-valid-va-validate)
- [33.8 Indeksni ishlab chiqarishda qo'shish: `CONCURRENTLY` va u uzilganda nima bo'ladi](#338-indeksni-ishlab-chiqarishda-qoshish-concurrently-va-u-uzilganda-nima-boladi)
- [33.9 Ma'lumotni ko'chirish (backfill): bo'laklab, yuk nazorati bilan](#339-malumotni-kochirish-backfill-bolaklab-yuk-nazorati-bilan)
- [33.10 Kod va sxema relizini bir-biriga moslashtirish: eski kod yangi sxemada ishlasin](#3310-kod-va-sxema-relizini-bir-biriga-moslashtirish-eski-kod-yangi-sxemada-ishlasin)
- [33.11 Orqaga qaytish (rollback) rejasi: sxemani qaytarish nega qiyin](#3311-orqaga-qaytish-rollback-rejasi-sxemani-qaytarish-nega-qiyin)
- [33.12 Migratsiyani sinash: ishlab chiqarish hajmidagi nusxada vaqtini o'lchash](#3312-migratsiyani-sinash-ishlab-chiqarish-hajmidagi-nusxada-vaqtini-olchash)
- [33.13 Amalda qo'llash](#3313-amalda-qollash)

</details>



Sxema relizning eng qaytarib bo'lmaydigan qismi. Kodni oldingi image'ga qaytarish bir daqiqa oladi, o'chirilgan ustunni qaytarish esa backup'dan tiklashni talab qiladi. Shuning uchun arxitektor sxema o'zgarishini bir necha relizga cho'zilgan bosqichli operatsiya deb ko'radi. Bu bobda shu operatsiyaning mexanikasi bor: qaysi DDL qanday lock oladi, qaysi o'zgarish jadvalni qayta yozadi, va kod bilan sxemani qanday tartibda chiqarish kerak.

## 33.1 Migratsiya vositalari: Flyway va Liquibase, versiyalash va nomlash tartibi

Flyway va Liquibase bir masalani hal qiladi: sxemaning qaysi o'zgarishi allaqachon qo'llanganini bazaning o'zida saqlash. Flyway buni `flyway_schema_history` jadvalida qiladi: versiya, tavsif, skript nomi va checksum. Liquibase `DATABASECHANGELOG` va `DATABASECHANGELOGLOCK` jadvallarini ishlatadi, har changeset `id` va `author` juftligi bilan aniqlanadi.

Tanlov mexanikaga bog'liq. Bitta PostgreSQL bilan ishlaydigan to'lov servisi uchun Flyway yetarli, chunki SQL baribir Postgres'ga xos bo'ladi. Bir nechta DBMS'ni qo'llaydigan mahsulotda Liquibase abstraksiyasi va changeset ichidagi rollback bloki foyda beradi.

Versiyani vaqt belgisi bilan bering, shunda ikki developer bir vaqtda migratsiya yozsa, raqam to'qnashmaydi.

```bash
  # Flyway: versiya = UTC vaqt belgisi, tavsif = qisqa va fe'lsiz
db/migration/V20260112_1430__order_add_delivery_slot_column.sql
db/migration/V20260112_1655__order_backfill_delivery_slot.sql
db/migration/V20260113_0910__order_delivery_slot_set_not_null.sql
db/migration/V20260120_1100__order_drop_legacy_delivery_time.sql

  # Repeatable: har marta checksum o'zgarsa qayta ishlaydi (view, funksiya)
db/migration/R__view_warehouse_stock_summary.sql
```

Bitta fayl bitta mantiqiy o'zgarish bo'lsin. Ustun qo'shish va backfill alohida fayl, chunki ularning lock profili butunlay boshqa.

## 33.2 Migratsiya qoidalari: oldinga faqat yangi fayl, qo'lda o'zgartirmaslik

Qoida bitta va qattiq: `main` branch'ga tushgan migratsiya fayli o'zgarmas. Flyway har faylning checksum'ini saqlaydi va o'zgargan faylni ko'rib ishga tushishdan bosh tortadi. Bu himoya: aks holda ikki muhitning sxemasi jimgina ajralib ketadi.

Shuning uchun xatoni tuzatish yo'li bitta: yangi fayl yozish. `V...1430__add_column.sql` da tip xato bo'lsa, uni tahrirlamaymiz, `V...1700__fix_column_type.sql` qo'shamiz.

```yaml
spring:
  flyway:
    enabled: true
    locations: classpath:db/migration
    # checksum tekshiruvini O'CHIRMA, bu xatolikni erta ushlaydi
    validate-on-migrate: true
    # tartibdan tashqari migratsiyaga ruxsat bermaymiz
    out-of-order: false
    # mavjud bazaga birinchi ulanishda baseline faqat bir marta
    baseline-on-migrate: false
    # har migratsiya o'z tranzaksiyasida, biri yiqilsa keyingisi ishlamaydi
    group: false
  jpa:
    hibernate:
      # production'da MUTLAQO none, Hibernate sxemaga tegmasin
      ddl-auto: none
```

`spring.jpa.hibernate.ddl-auto` qiymati production'da `none` bo'lishi shart. `update` qiymati Hibernate'ga sxemani o'zgartirish huquqini beradi, u esa index va cheklovlarni o'zicha qo'shadi, migratsiya tarixiga esa hech narsa yozmaydi.

Qo'lda `psql` ochib production'da `ALTER TABLE` yozish ham xuddi shunday buzilish. Shoshilinch tuzatishni ham avval migratsiya fayli sifatida commit qiling.

## 33.3 Kengaytirish va qisqartirish (expand and contract) usuli bosqichma-bosqich

To'xtashsiz relizning asosiy g'oyasi: hech qachon kod va sxemani bir vaqtda mos kelmaydigan holatga keltirmaslik. Rolling deployment paytida bir necha daqiqa davomida eski va yangi kod bir xil bazaga yozadi. Demak sxema shu ikki versiyaning ikkisiga ham mos bo'lishi kerak.

Bosqichlar ketma-ketligi quyidagicha. Birinchi bosqich (expand): sxemaga yangi struktura qo'shiladi, eskisi joyida qoladi. Yangi ustun `NULL` qabul qiladi, yangi jadval bo'sh. Eski kod buni sezmaydi.

Keyin kod chiqadi va ikki joyga yozadi, eski joydan o'qiydi. Uchinchi bosqichda backfill eski ma'lumotni ko'chiradi. To'rtinchida kod yangi joydan o'qiydi, eskisiga hali yozadi. Beshinchida eski joyga yozish to'xtaydi. Oltinchida (contract) eski ustun o'chiriladi.

Har bosqich alohida deploy va har biri orqaga qaytishga ochiq. To'lov servisidagi `amount` ustunini `numeric(19,4)` ga o'tkazish shu yo'l bilan ikki hafta davom etadi, lekin bironta so'rov yo'qolmaydi. Alternativa bitta tungi `ALTER TABLE`, u 50 million qatorli jadvalda bir soat lock ushlaydi.

## 33.4 Ustun qo'shish, nomini o'zgartirish va o'chirishning xavfsiz ketma-ketligi

Ustun qo'shish eng oson holat: `NULL` ruxsatli ustun qo'shiladi, keyin kod uni to'ldira boshlaydi. Ustun nomini o'zgartirish esa eng xavfli, chunki `ALTER TABLE ... RENAME COLUMN` bir zumda ishlaydi, lekin eski kod shu sekundda `column does not exist` xatosini oladi.

Shuning uchun rename hech qachon rename sifatida bajarilmaydi. U "yangi ustun qo'shish, ko'chirish, eskisini o'chirish" ga aylantiriladi.

```sql
-- 1-bosqich: yangi ustun, NULL ruxsatli, default yo'q
ALTER TABLE orders ADD COLUMN delivery_slot_id bigint;

-- 2-bosqich: yangi kod ikki ustunga ham yozadi (dual write)

-- 3-bosqich: backfill bo'laklab (pastdagi bo'limga qarang)

-- 4-bosqich: cheklovni NOT VALID bilan qo'shamiz, keyin tasdiqlaymiz
ALTER TABLE orders
  ADD CONSTRAINT orders_delivery_slot_fk
  FOREIGN KEY (delivery_slot_id) REFERENCES delivery_slots (id) NOT VALID;
ALTER TABLE orders VALIDATE CONSTRAINT orders_delivery_slot_fk;

-- 5-bosqich: kod faqat yangi ustundan o'qiydi va unga yozadi

-- 6-bosqich: eski ustunni o'chirish, oldingi relizdan 1-2 hafta keyin
ALTER TABLE orders DROP COLUMN legacy_delivery_time;
```

`DROP COLUMN` PostgreSQL'da metadata operatsiyasi: ustun `pg_attribute` da `attisdropped` bilan belgilanadi, ma'lumot esa joyida qoladi. Ya'ni u tez, lekin diskni darhol bo'shatmaydi.


## 33.5 Qaysi DDL jadvalni bloklaydi: `ALTER TABLE` turlarining lock darajasi

PostgreSQL'da deyarli har qanday `ALTER TABLE` `ACCESS EXCLUSIVE` lock oladi. Bu lock hamma narsani bloklaydi, hatto `SELECT` ni ham. Muhim nuqta shunda: lock qancha ushlanadi, va uni olish uchun qancha kutiladi.

Eng ko'p uchraydigan halokat shu: `ALTER TABLE` uzoq ishlaydigan `SELECT` ortida navbatga tushadi. PostgreSQL navbatda adolatni saqlaydi, shuning uchun `ALTER TABLE` dan keyin kelgan oddiy `SELECT` lar ham navbatda to'planadi. Natijada 20 millisekundlik DDL butun jadvalni 3 daqiqa o'chirib qo'yadi.

| DDL operatsiyasi | Lock darajasi | Jadvalni qayta yozadimi |
| --- | --- | --- |
| `ADD COLUMN` (default yo'q yoki constant default) | ACCESS EXCLUSIVE, juda qisqa | Yo'q |
| `ADD COLUMN` volatile default bilan | ACCESS EXCLUSIVE, uzoq | Ha, to'liq |
| `DROP COLUMN` | ACCESS EXCLUSIVE, qisqa | Yo'q |
| `ALTER COLUMN TYPE int` dan `bigint` ga | ACCESS EXCLUSIVE, uzoq | Ha, to'liq |
| `SET NOT NULL` (valid CHECK bor) | ACCESS EXCLUSIVE, qisqa | Yo'q |
| `ADD CONSTRAINT ... NOT VALID` | ACCESS EXCLUSIVE, qisqa | Yo'q |
| `VALIDATE CONSTRAINT` | SHARE UPDATE EXCLUSIVE | Yo'q, lekin to'liq skan |
| `CREATE INDEX` | SHARE (yozish bloklanadi) | Yo'q |
| `CREATE INDEX CONCURRENTLY` | SHARE UPDATE EXCLUSIVE | Yo'q, ikki marta skan |

Himoya mexanizmi `lock_timeout`: kutish cho'zilsa migratsiya xato bilan to'xtaydi va boshqa so'rovlarni bo'g'maydi.

```sql
-- Har migratsiya faylining boshida: lockni 3 sekunddan ko'p kutmaymiz
SET lock_timeout = '3s';
-- DDL o'zi ham cheklangan bo'lsin
SET statement_timeout = '30s';

ALTER TABLE orders ADD COLUMN delivery_slot_id bigint;

-- Agar lock_timeout ishga tushsa: 55P03 lock_not_available xatosi.
-- Deploy pipeline shu xatoni ko'rib migratsiyani 1 daqiqadan keyin
-- qayta urinishi kerak, 5 martagacha.
```

## 33.6 Katta jadvalga ustun qo'shish va standart qiymat masalasi

PostgreSQL 11 dan boshlab constant default bilan ustun qo'shish jadvalni qayta yozmaydi. Default qiymat `pg_attribute.attmissingval` da saqlanadi va o'qishda qatorga "yopishtiriladi". Ya'ni `ADD COLUMN status text DEFAULT 'NEW' NOT NULL` 80 million qatorli `orders` jadvalida ham taxminan 20 millisekundda tugaydi.

Lekin default volatile funksiya bo'lsa, qoida buziladi. `DEFAULT gen_random_uuid()` yoki `DEFAULT clock_timestamp()` har qatorga boshqa qiymat beradi, demak PostgreSQL har qatorni yangidan yozishga majbur. 80 million qatorli jadvalda bu disk hajmining ikki baravariga va taxminan 20-40 daqiqa `ACCESS EXCLUSIVE` lock'ga olib keladi.

```sql
-- XAVFLI: volatile default jadvalni to'liq qayta yozadi
ALTER TABLE payments ADD COLUMN idempotency_key uuid DEFAULT gen_random_uuid();

-- XAVFSIZ: default yo'q, keyin backfill, keyin default
ALTER TABLE payments ADD COLUMN idempotency_key uuid;
-- backfill bo'laklab bajariladi
ALTER TABLE payments ALTER COLUMN idempotency_key SET DEFAULT gen_random_uuid();

-- XAVFSIZ: constant default, PG 11+ da metadata operatsiyasi
ALTER TABLE orders ADD COLUMN channel text NOT NULL DEFAULT 'WEB';
```

`now()` stable, `clock_timestamp()` volatile. Shuning uchun `DEFAULT now()` bilan ustun qo'shish qayta yozishga olib kelmaydi. Ishonchsiz bo'lsangiz production hajmidagi nusxada `\timing` bilan o'lchang.

## 33.7 `NOT NULL` va `CHECK` cheklovini to'xtashsiz qo'shish (`NOT VALID` va `VALIDATE`)

Cheklovni qo'shishda ikki xarajat bor: lock olish va mavjud ma'lumotni tekshirish. `NOT VALID` bu ikkisini ajratadi. `ADD CONSTRAINT ... NOT VALID` faqat katalogga yozadi, mavjud qatorlarni tekshirmaydi, lekin yangi va o'zgargan qatorlarga darhol amal qila boshlaydi. Keyin `VALIDATE CONSTRAINT` mavjud ma'lumotni tekshiradi va u `SHARE UPDATE EXCLUSIVE` lock oladi, ya'ni o'qish ham yozish ham davom etadi.

`SET NOT NULL` uchun PostgreSQL 12 dan boshlab nozik yo'l bor. Agar jadvalda `col IS NOT NULL` ni isbotlaydigan valid `CHECK` cheklovi bo'lsa, planner to'liq skanni o'tkazib yuboradi.

```sql
-- 1-qadam: tekshirmaydigan CHECK, qisqa lock
ALTER TABLE orders
  ADD CONSTRAINT orders_delivery_slot_not_null
  CHECK (delivery_slot_id IS NOT NULL) NOT VALID;

-- 2-qadam: tasdiqlash, o'qish va yozish bloklanmaydi
ALTER TABLE orders VALIDATE CONSTRAINT orders_delivery_slot_not_null;

-- 3-qadam: PG 12+ valid CHECK borligini ko'rib skan qilmaydi
ALTER TABLE orders ALTER COLUMN delivery_slot_id SET NOT NULL;

-- 4-qadam: endi CHECK keraksiz, uni olib tashlaymiz
ALTER TABLE orders DROP CONSTRAINT orders_delivery_slot_not_null;
```

`VALIDATE CONSTRAINT` 80 million qatorli jadvalda sequential scan qiladi, bu taxminan 2-5 daqiqa oladi. Uni yuk kam vaqtda ishga tushiring, lekin tungi oyna shart emas, chunki hech kim bloklanmaydi.

## 33.8 Indeksni ishlab chiqarishda qo'shish: `CONCURRENTLY` va u uzilganda nima bo'ladi

Oddiy `CREATE INDEX` `SHARE` lock oladi: o'qish davom etadi, yozish to'xtaydi. 50 million qatorli `payments` jadvalida bu 5-15 daqiqa yozishsiz qolish degani. `CONCURRENTLY` yozishga xalaqit bermaydi, lekin jadvalni ikki marta skanlaydi va taxminan ikki baravar uzoq ishlaydi.

Ikki muhim shart. Birinchisi: `CONCURRENTLY` tranzaksiya ichida ishlamaydi. Flyway'da bunday faylga maxsus belgi kerak.

```sql
-- flyway migratsiyasida tranzaksiyani o'chirish uchun fayl nomiga
-- Flyway'ning transactional=false sozlamasi yoki alohida callback kerak.
-- Liquibase'da changeset'ga runInTransaction="false" qo'yiladi.

CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_payments_merchant_created
  ON payments (merchant_id, created_at DESC);

-- Uzilgandan keyin tekshirish: invalid indeks qolganini topish
SELECT c.relname, i.indisvalid
FROM pg_index i
JOIN pg_class c ON c.oid = i.indexrelid
WHERE NOT i.indisvalid;

-- Invalid indeksni tozalash, u ham CONCURRENTLY bo'lsin
DROP INDEX CONCURRENTLY IF EXISTS idx_payments_merchant_created;
```

Ikkinchi shart: `CONCURRENTLY` uzilib qolsa, PostgreSQL `indisvalid = false` holatidagi indeksni qoldiradi. Bu indeks so'rovlarda ishlatilmaydi, lekin `INSERT` va `UPDATE` da yangilanadi, ya'ni faqat sekinlashtiradi va joy egallaydi. Shuning uchun har migratsiya ishga tushgandan keyin invalid indekslarni tekshiradigan avtomatik nazorat bo'lishi kerak.

Yana bir tuzoq: `CONCURRENTLY` boshlanish paytidagi ochiq tranzaksiyalarni kutadi. Bitta 40 daqiqalik hisobot so'rovi indeks yaratishni shu muddatga ushlab turadi, shuning uchun avval `pg_stat_activity` ni ko'rib chiqing.

## 33.9 Ma'lumotni ko'chirish (backfill): bo'laklab, yuk nazorati bilan

Bitta `UPDATE orders SET delivery_slot_id = ...` 80 million qatorda ulkan tranzaksiya ochadi, WAL hajmini o'nlab gigabaytga oshiradi, replika lag'ini cho'zadi va autovacuum'ni dead tuple ostida ko'madi. Bundan tashqari, u yiqilsa butun ish nolga qaytadi.

To'g'ri yo'l: primary key diapazoni bo'yicha bo'laklash, har bo'lak alohida tranzaksiya, bo'laklar orasida pauza va replika lag'ini kuzatish.

```sql
-- Bitta bo'lak: 5000 qator, o'z tranzaksiyasida
UPDATE orders o
SET delivery_slot_id = ds.id
FROM delivery_slots ds
WHERE o.legacy_delivery_time = ds.slot_time
  AND o.delivery_slot_id IS NULL
  AND o.id >= :from_id AND o.id < :from_id + 5000;

-- Qolgan ishni o'lchash, progress ko'rinib turishi uchun
SELECT count(*) FROM orders
WHERE delivery_slot_id IS NULL AND id < :max_id;

-- Replika lag'ini bo'laklar orasida tekshirish
SELECT application_name,
       pg_wal_lsn_diff(sent_lsn, replay_lsn) AS lag_bytes
FROM pg_stat_replication;
```

Backfill'ni dastur ichida boshqarish qulay, chunki shunda lag bo'yicha tormozlash mantiqi joylashadi.

```java
// Backfill runner: har bo'lak alohida tranzaksiyada, REQUIRES_NEW bilan
@Service
public class DeliverySlotBackfill {

    private static final int BATCH = 5000;
    private static final long MAX_LAG_BYTES = 32L * 1024 * 1024; // 32 MB

    private final BackfillBatchExecutor executor; // @Transactional(REQUIRES_NEW)
    private final ReplicationLagProbe lagProbe;

    public void run(long maxId) throws InterruptedException {
        for (long from = 0; from < maxId; from += BATCH) {
            int updated = executor.updateRange(from, from + BATCH);
            // lag oshib ketsa to'xtab turamiz, replikani bo'g'maymiz
            while (lagProbe.lagBytes() > MAX_LAG_BYTES) {
                Thread.sleep(2_000);
            }
            if (updated > 0) {
                Thread.sleep(50); // autovacuum nafas olsin
            }
        }
    }
}
```

Bo'lak kattaligini tajriba bilan tanlang. 5000 qator odatda 50-200 millisekund oladi, bu qabul qilinadigan muddat. 100000 qatorli bo'lak esa lock navbatini yaratadi va deadlock ehtimolini oshiradi.

## 33.10 Kod va sxema relizini bir-biriga moslashtirish: eski kod yangi sxemada ishlasin

Kubernetes rolling update paytida eski va yangi pod'lar bir necha daqiqa yonma-yon ishlaydi. Shundan kelib chiqadigan qoida: har bir migratsiya oldingi reliz kodi bilan mos bo'lishi shart. Buni "N-1 moslik" deb atash mumkin.

Shundan kelib chiqib yangi ustun `NULL` ruxsatli bo'lishi kerak, chunki eski kod uni to'ldirmaydi. Oraliq relizda Hibernate entity ikki ustunni ham bilsin.

Flyway Spring Boot startup'ida ishlaydi va advisory lock orqali bir vaqtda faqat bitta pod migratsiya qilishini kafolatlaydi. Lekin bu pod startup vaqtini migratsiya vaqtiga bog'laydi: 4 daqiqalik `VALIDATE CONSTRAINT` liveness probe'ni ishga tushiradi.

```yaml
  # Migratsiya alohida Job, deploy'dan oldin ishlaydi
apiVersion: batch/v1
kind: Job
metadata:
  name: payment-service-migrate
  annotations:
    "helm.sh/hook": pre-upgrade
    "helm.sh/hook-weight": "-5"
spec:
  backoffLimit: 3            # lock_timeout xatosida qayta urinadi
  activeDeadlineSeconds: 900 # 15 daqiqadan oshsa to'xtatamiz
  template:
    spec:
      restartPolicy: Never
      containers:
        - name: migrate
          image: registry.local/payment-service:1.42.0
          args: ["--spring.main.web-application-type=none",
                 "--spring.flyway.enabled=true"]
```

Application pod'larida esa `spring.flyway.enabled=false` bo'ladi: pod faqat sxema tayyor holatda ko'tariladi.

## 33.11 Orqaga qaytish (rollback) rejasi: sxemani qaytarish nega qiyin

Sxema rollback'i kod rollback'iga o'xshamaydi. `DROP COLUMN` ni qaytarish mumkin emas, chunki ma'lumot yo'q. `ALTER COLUMN TYPE` ni qaytarish yana bir to'liq qayta yozish. Backfill'ni qaytarish uchun esa qaysi qator o'zgargani haqida yozuv kerak.

Shuning uchun amaliy strategiya rollback'ni emas, oldinga tuzatishni (forward fix) rejalashtirishdir. Expand va contract usuli bu strategiyaning asosi: eski struktura joyida turganda rollback oddiygina eski image'ni qaytarishga aylanadi.

```yaml
  # Liquibase: rollback blokini changeset ichida e'lon qilish
databaseChangeLog:
  - changeSet:
      id: 20260112-1430-order-add-delivery-slot
      author: payments-team
      changes:
        - addColumn:
            tableName: orders
            columns:
              - column:
                  name: delivery_slot_id
                  type: bigint
      rollback:
        - dropColumn:
            tableName: orders
            columnName: delivery_slot_id
  - changeSet:
      id: 20260120-1100-order-drop-legacy-column
      author: payments-team
      comment: "Qaytarib bo'lmaydi, oldin backup tekshirilsin"
      changes:
        - dropColumn:
            tableName: orders
            columnName: legacy_delivery_time
      rollback:
        - empty: {}
```

Qaytarib bo'lmaydigan migratsiyalarni alohida belgilang va faqat yangi kod ishlab turgani tasdiqlangandan keyin chiqaring, odatda 1-2 hafta keyin. `DROP COLUMN` o'rniga ustunni `legacy_delivery_time_unused` deb nomlash ham ishlaydi: bir hafta xato chiqmasa, demak u rostdan ishlatilmaydi.

## 33.12 Migratsiyani sinash: ishlab chiqarish hajmidagi nusxada vaqtini o'lchash

Migratsiyaning to'g'riligi kichik bazada tekshiriladi, bu [testlash qo'llanmasidagi](../testing/README.md) Testcontainers mavzusi. Vaqtini esa faqat production hajmidagi nusxada o'lchash mumkin. 1000 qatorli jadvaldagi `ALTER TABLE` 5 millisekundda, 80 million qatorlisida 40 daqiqada tugaydi, va bu farq butun reliz rejasini o'zgartiradi.

Snapshot'dan nusxa ko'taring, unga production yukining 20-30 foizini bering, keyin migratsiyani `\timing` bilan ishga tushiring. Shu paytda `pg_locks` ni kuzatib, qanday so'rovlar bloklanganini ko'ring.

| Mavzu | Oddiy yondashuv | Arxitektor yondashuvi |
| --- | --- | --- |
| Ustun nomini o'zgartirish | `RENAME COLUMN`, bitta reliz | Yangi ustun, dual write, backfill, eskisini o'chirish |
| Yangi ustunga default | `ADD COLUMN ... DEFAULT gen_random_uuid()` | Default'siz qo'shish, backfill, keyin default |
| `NOT NULL` qo'shish | `SET NOT NULL` to'g'ridan to'g'ri | `CHECK ... NOT VALID`, `VALIDATE`, keyin `SET NOT NULL` |
| Indeks qo'shish | `CREATE INDEX` tungi oynada | `CONCURRENTLY`, invalid indeks nazorati bilan |
| Ma'lumot ko'chirish | Bitta `UPDATE` butun jadvalga | 5000 qatorli bo'laklar, replika lag bo'yicha tormoz |
| Migratsiya qachon ishlaydi | App startup'ida, har pod'da | Alohida `pre-upgrade` Job, app'da Flyway o'chirilgan |
| Lock kutish | Cheksiz kutadi | `lock_timeout = 3s` va pipeline'da qayta urinish |
| Rollback | "Kerak bo'lsa `DROP` qilamiz" | Expand va contract, rollback = eski image |

| Tuzoq | Nega sodir bo'ladi | Yechim |
| --- | --- | --- |
| 20 ms DDL jadvalni 3 daqiqa o'chirdi | `ACCESS EXCLUSIVE` uzoq `SELECT` ortida navbatga tushdi | `lock_timeout = 3s` va retry |
| `ADD COLUMN` 40 daqiqa ketdi | Volatile default to'liq qayta yozishni chaqirdi | Default'siz qo'shib, keyin backfill |
| Indeks so'rovda ishlatilmaydi | `CONCURRENTLY` uzilib `indisvalid = false` qoldirdi | `DROP INDEX CONCURRENTLY` va qayta yaratish |
| Replika 8 daqiqa orqada qoldi | Bitta ulkan `UPDATE` WAL'ni to'ldirdi | Bo'laklash va `pg_stat_replication` nazorati |
| Deploy paytida `column does not exist` | Sxema eski kod bilan mos emas | N-1 moslik qoidasi, expand bosqichi |
| Pod migratsiya paytida restart bo'ldi | Startup migratsiya liveness probe'dan uzoq ketdi | Migratsiyani alohida Job'ga chiqarish |
| Flyway ishga tushmadi, checksum xatosi | Qo'llangan migratsiya fayli tahrirlangan | Faylni qaytarish, tuzatishni yangi faylda berish |
| `DROP COLUMN` dan keyin disk bo'shamadi | Ma'lumot qatorlarda qoladi | `VACUUM FULL` yoki jadvalni asta qayta yozish |

## 33.13 Amalda qo'llash

- [ ] Loyihadagi hamma migratsiya fayllarini ko'rib chiqing va `spring.jpa.hibernate.ddl-auto` production profilida `none` ekanini tasdiqlang.
- [ ] Har migratsiya faylining boshiga `SET lock_timeout = '3s'` qo'shing va deploy pipeline'ga `55P03` xatosida 5 martagacha qayta urinish mantiqini kiriting.
- [ ] Migratsiyani application startup'idan ajratib, alohida `pre-upgrade` Job'ga chiqaring, app pod'larida Flyway'ni o'chiring.
- [ ] Eng katta uchta jadvalning qator sonini va hajmini yozib oling, keyingi migratsiya rejasi shu raqamlarga tayansin.
- [ ] Production snapshot'idan nusxa ko'tarib, keyingi rejalashtirilgan `ALTER TABLE` va `CREATE INDEX CONCURRENTLY` vaqtini o'lchang.
- [ ] Invalid indekslarni (`pg_index.indisvalid = false`) topadigan so'rovni monitoring'ga alert sifatida qo'shing.
- [ ] Backfill uchun bo'laklab ishlaydigan runner yozing, unda bo'lak kattaligi va replika lag chegarasi sozlanadigan bo'lsin.
- [ ] Qaytarib bo'lmaydigan migratsiyalar ro'yxatini tuzing va har biri uchun "oldingi relizdan necha kun keyin chiqadi" muddatini belgilang.

---

[&larr; 32. Tarmoq, timeout va integratsiya haqiqati](32-tarmoq-timeout-va-integratsiya-haqiqati.md) · [Mundarija](README.md) · [34. Legacy kod va bosqichma-bosqich refaktoring &rarr;](34-legacy-kod-va-bosqichma-bosqich-refaktoring.md)
