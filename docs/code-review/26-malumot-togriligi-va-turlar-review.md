<!-- doc: code-review | chapter: 26 | part: V. PostgreSQL va ma'lumot qatlami review -->

[Barcha hujjatlar](../../README.md) / [Kod review](README.md)

> Holat: AI yozgan, inson tekshirmagan.

# 26. Ma'lumot to'g'riligi va turlar review (Data Correctness)

<details>
<summary>Bu bobdagi 10 bo'lim</summary>

- [26.1 Constraint - yagona ishonchli himoya](#261-constraint---yagona-ishonchli-himoya)
- [26.2 Pul: tur, aniqlik, valyuta](#262-pul-tur-aniqlik-valyuta)
- [26.3 Vaqt: zona, tur, tartib](#263-vaqt-zona-tur-tartib)
- [26.4 Enum: baza va kod sinxronizatsiyasi](#264-enum-baza-va-kod-sinxronizatsiyasi)
- [26.5 NULL semantikasi](#265-null-semantikasi)
- [26.6 Tashqi kalitlar va o'chirish qoidalari](#266-tashqi-kalitlar-va-ochirish-qoidalari)
- [26.7 Yumshoq o'chirish (soft delete)](#267-yumshoq-ochirish-soft-delete)
- [26.8 Ma'lumot migratsiyasidagi to'g'rilik](#268-malumot-migratsiyasidagi-togrilik)
- [26.9 Review checklisti: ma'lumot to'g'riligi](#269-review-checklisti-malumot-togriligi)
- [26.10 Amalda qo'llash](#2610-amalda-qollash)

</details>


Bu bob ma'lumotning o'zi haqida: qaysi qiymat bazaga tushishi mumkin va qaysi biri mumkin emas. Kod xatosini tuzatish arzon, buzilgan ma'lumotni tuzatish qimmat va ba'zan imkonsiz. Shu sababli review da yangi ustun yoki yangi yozuv yo'li paydo bo'lganda, birinchi savol himoya haqida bo'ladi.

## 26.1 Constraint - yagona ishonchli himoya

Ilova kodidagi tekshiruv ikki instansda, migratsiyada, qo'lda `UPDATE` da va eski kod versiyasida ishlamaydi. Faqat ma'lumotlar bazasidagi constraint har doim ishlaydi.

```sql
-- Review da talab qilinadigan minimal himoya to'plami.
CREATE TABLE payment (
    id              uuid        PRIMARY KEY,
    order_id        uuid        NOT NULL REFERENCES orders(id),
    idempotency_key text        NOT NULL,
    amount          numeric(19,4) NOT NULL,
    currency        char(3)     NOT NULL,
    status          text        NOT NULL,
    created_at      timestamptz NOT NULL DEFAULT now(),
    captured_at     timestamptz,

    -- Pul manfiy bo'lmaydi va nol ham bo'lmaydi.
    CONSTRAINT payment_amount_positive CHECK (amount > 0),
    -- Valyuta kodi shakli.
    CONSTRAINT payment_currency_shape CHECK (currency ~ '^[A-Z]{3}$'),
    -- Status faqat ma'lum qiymatlardan.
    CONSTRAINT payment_status_valid
        CHECK (status IN ('PENDING', 'CAPTURED', 'DECLINED', 'REFUNDED')),
    -- Mantiqiy bog'liqlik: captured_at faqat CAPTURED holatida bo'ladi.
    CONSTRAINT payment_captured_consistency
        CHECK ((status = 'CAPTURED') = (captured_at IS NOT NULL)),
    -- Vaqt tartibi.
    CONSTRAINT payment_time_order CHECK (captured_at IS NULL OR captured_at >= created_at)
);

-- Idempotentlik: faqat unique indeks ishonchli (10.9).
CREATE UNIQUE INDEX payment_idem_uniq ON payment (idempotency_key);

-- Biznes qoidasi: bitta buyurtmaga bitta aktiv to'lov.
CREATE UNIQUE INDEX payment_one_active_per_order ON payment (order_id)
    WHERE status IN ('PENDING', 'CAPTURED');
```

Oxirgi indeks - review da kam uchraydigan, lekin juda kuchli vosita: partial unique indeks biznes qoidasini bazada majburlaydi va poyga holatlarini butunlay yo'q qiladi.

## 26.2 Pul: tur, aniqlik, valyuta

| Qaror | To'g'ri | Xato |
| --- | --- | --- |
| Java turi | `BigDecimal` + valyuta (`Money`) | `double`, `float` |
| PostgreSQL turi | `numeric(19,4)` yoki butun son (tiyin) | `float8`, `money` |
| Yaxlitlash | Aniq `RoundingMode`, biznes bilan kelishilgan | Standartga tashlab qo'yish |
| Valyuta | Alohida ustun, har summa bilan | Taxmin qilish |
| Taqqoslash | `compareTo` | `equals` |
| Yig'indi | SQL `sum(numeric)` yoki `Money::plus` | `double` yig'indisi |

```sql
-- PostgreSQL `money` turi ishlatilmaydi: u lokalga bog'liq va aniqligi
-- sozlamalardan keladi. numeric aniq va portativ.
amount numeric(19,4) NOT NULL          -- to'g'ri
amount money NOT NULL                  -- review da rad etiladi
amount double precision NOT NULL       -- blocker: aniqlik yo'qoladi

-- Valyuta aralashuvini bazada taqiqlash: agregatlarda ham xavfsiz.
CREATE TABLE invoice_line (
    invoice_id uuid NOT NULL,
    amount     numeric(19,4) NOT NULL,
    currency   char(3) NOT NULL
);
-- Invoys ichidagi hamma qator bir valyutada bo'lishi kerak:
-- trigger yoki denormalizatsiya (invoice.currency + FK) bilan majburlanadi.
```

## 26.3 Vaqt: zona, tur, tartib

```sql
-- timestamp va timestamptz: diffda bir harf farq, xulqda katta farq.
created_at timestamp                   -- zonasiz: "2026-10-04 12:00" - qaysi zonada?
created_at timestamptz                 -- UTC nuqta, zona bilan to'g'ri ishlaydi

-- Review qoidasi: hodisa vaqti har doim timestamptz.
-- Kalendar sanasi (tug'ilgan kun, bayram) esa date - zonasiz to'g'ri.
birth_date date                        -- to'g'ri: zona ma'nosiz
holiday_on date                        -- to'g'ri

-- Vaqt manbasi: ilova yoki baza?
created_at timestamptz NOT NULL DEFAULT now()
-- now() tranzaksiya boshlanish vaqtini beradi (clock_timestamp() - haqiqiy).
-- Review savoli: ikki serverning vaqti farq qilsa, tartib buziladimi?
-- Agar tartib muhim bo'lsa, ketma-ketlik (sequence) yoki bazadagi vaqt
-- ishlatiladi, ilova vaqti emas.
```

## 26.4 Enum: baza va kod sinxronizatsiyasi

| Variant | Foydasi | Narxi |
| --- | --- | --- |
| `text` + `CHECK IN (...)` | Qiymat qo'shish oson (`ALTER CONSTRAINT`) | Constraint ni yangilash kerak |
| PostgreSQL `enum` turi | Tipli, kichik saqlanadi | Qiymat olib tashlash qiyin, `ALTER TYPE` cheklovlari |
| Ma'lumotnoma jadval + FK | Metadata qo'shish mumkin | JOIN kerak |
| Hech qanday himoya | - | Bazaga har qanday satr tushadi |

```sql
-- Eng amaliy variant: text + CHECK. Yangi qiymat qo'shish:
ALTER TABLE orders DROP CONSTRAINT orders_status_valid;
ALTER TABLE orders ADD CONSTRAINT orders_status_valid
    CHECK (status IN ('NEW','PAID','SHIPPED','DELIVERED','CANCELLED','REFUNDED'))
    NOT VALID;                                       -- bir zumda
ALTER TABLE orders VALIDATE CONSTRAINT orders_status_valid;   -- bloklamaydi

-- Review diqqati: deploy tartibi. Yangi status kodda ishlatilishidan
-- OLDIN constraint yangilanishi kerak, aks holda yangi kod yozganda
-- constraint xatosi chiqadi (25.3 jadvaliga qarang).
```

```java
// Kod va baza o'rtasidagi mosligni test bilan qulflash.
@Test
void databaseConstraintCoversAllEnumValues() {
    // Bazadagi CHECK dan qiymatlarni o'qib, enum bilan solishtirish.
    String check = jdbc.queryForObject("""
        SELECT pg_get_constraintdef(oid) FROM pg_constraint
         WHERE conname = 'orders_status_valid'
        """, String.class);
    for (OrderStatus s : OrderStatus.values()) {
        assertThat(check)
            .as("baza constraint i %s qiymatini qabul qilishi kerak", s)
            .contains("'" + s.name() + "'");
    }
}
// Bu test enum ga yangi qiymat qo'shilib, migratsiya yozilmaganini tutadi -
// aks holda bu xato faqat prodda chiqadi.
```

## 26.5 NULL semantikasi

```sql
-- NULL ning ma'nosi yozilishi kerak: "bilinmaydi", "qo'llanmaydi" yoki "hali yo'q".
-- Review savoli: bu ustun nega nullable?

-- Xavfli naqsh: nullable boolean - uch holatli mantiq.
is_verified boolean                    -- true, false, NULL - NULL nima?
is_verified boolean NOT NULL DEFAULT false   -- aniq

-- NULL va unique: PostgreSQL da NULL lar bir-biriga teng emas.
CREATE UNIQUE INDEX ON customer (email);
-- Ikki qator email = NULL bilan - ikkisi ham o'tadi (dublikat emas).
-- Agar faqat bitta NULL bo'lishi kerak bo'lsa (PG 15+):
CREATE UNIQUE INDEX ON customer (email) NULLS NOT DISTINCT;

-- NULL va taqqoslash: eng ko'p uchraydigan mantiq xatosi.
SELECT * FROM orders WHERE cancelled_at <> '2026-01-01';
-- cancelled_at IS NULL bo'lgan qatorlar natijaga TUSHMAYDI.
-- To'g'ri: WHERE (cancelled_at IS NULL OR cancelled_at <> '2026-01-01')
-- yoki: WHERE cancelled_at IS DISTINCT FROM '2026-01-01'

-- NULL va agregat:
SELECT avg(risk_score) FROM orders;    -- NULL lar hisobga olinmaydi
-- Agar NULL ni 0 deb hisoblash kerak bo'lsa - coalesce aniq yozilishi kerak.
```

## 26.6 Tashqi kalitlar va o'chirish qoidalari

```sql
-- FK qoidasi ongli tanlanishi kerak, standartga tashlab qo'yilmasligi.
order_id uuid NOT NULL REFERENCES orders(id) ON DELETE CASCADE
-- CASCADE: buyurtma o'chirilsa, to'lovlar ham o'chadi. Buxgalteriya uchun xato.
order_id uuid NOT NULL REFERENCES orders(id) ON DELETE RESTRICT
-- RESTRICT: to'lovi bor buyurtmani o'chirib bo'lmaydi. Odatda to'g'ri.

-- Diqqat: FK ustunida indeks AVTOMATIK yaratilmaydi (PostgreSQL da).
-- Ota jadvaldan o'chirish yoki yangilash har bola jadvalda skan qiladi.
CREATE INDEX ON payment (order_id);   -- FK uchun indeks majburiy

-- FK ni mavjud katta jadvalga qo'shish: ikki qadamli xavfsiz yo'l (25.1).
ALTER TABLE payment ADD CONSTRAINT payment_order_fk
    FOREIGN KEY (order_id) REFERENCES orders(id) NOT VALID;    -- bir zumda
ALTER TABLE payment VALIDATE CONSTRAINT payment_order_fk;      -- bloklamaydi
```

```bash
# Indekssiz FK larni topish: review ning tez g'alabasi.
psql -c "
SELECT c.conrelid::regclass AS jadval, a.attname AS ustun
  FROM pg_constraint c
  JOIN pg_attribute a ON a.attrelid = c.conrelid AND a.attnum = c.conkey[1]
 WHERE c.contype = 'f'
   AND NOT EXISTS (
       SELECT 1 FROM pg_index i
        WHERE i.indrelid = c.conrelid AND i.indkey[0] = c.conkey[1])
 ORDER BY 1;"
```

## 26.7 Yumshoq o'chirish (soft delete)

`deleted_at timestamptz` ustuni qo'shilgan diff review da uch savol tug'diradi. Mexanikasi, SQL va narxi [arxitektor hujjatidagi yumshoq o'chirish va uning yashirin narxi](../architect/25-sxema-dizayni-malumot-turlari-va-cheklovlar.md#259-yumshoq-ochirish-soft-delete-va-uning-yashirin-narxi) mavzusida, bu yerda faqat review savollari.

1. **Hamma so'rov `deleted_at IS NULL` shartini hisobga oladimi?** Bitta so'rovda esdan chiqsa, o'chirilgan ma'lumot foydalanuvchiga ko'rinadi. Himoya ko'rinish (view) yoki RLS, `@SQLRestriction` (eski kodda `@Where`, u Hibernate 7.0 da olib tashlangan) emas: sababi [Hibernate xulqini o'zgartiradigan nozik annotatsiyalar](23-jpa-va-hibernate-review.md#238-hibernate-xulqini-ozgartiradigan-nozik-annotatsiyalar) mavzusida.
2. **Unique constraint qanday ishlaydi?** O'chirilgan va yangi qator bir xil email bilan turishi kerakmi? Kerak bo'lsa, unikallik faqat aktiv qatorlar orasida, `WHERE deleted_at IS NULL` li partial unique indeks bilan ta'minlanadi.
3. **Ma'lumotni haqiqatan o'chirish talabi (GDPR) bormi?** Yumshoq o'chirish "o'chirish huquqi" ni bajarmaydi: anonimlashtirish yoki haqiqiy o'chirish kerak bo'lishi mumkin, bu [secret, maxfiy ma'lumot va kriptografiya review](32-secret-maxfiy-malumot-va-kriptografiya.md) mavzusida.

## 26.8 Ma'lumot migratsiyasidagi to'g'rilik

```sql
-- Review da ma'lumot ko'chirish uchun uchta talab.
-- 1) Qancha qator ta'sirlanadi - oldin sanash.
SELECT count(*) FROM customer WHERE phone IS NOT NULL AND phone_e164 IS NULL;

-- 2) Namuna bilan tekshirish - ko'chirish qoidasi to'g'rimi.
SELECT phone, normalize_phone(phone) AS natija
  FROM customer WHERE phone IS NOT NULL
 ORDER BY random() LIMIT 20;
-- Review izohi: shu 20 qatorni PR ga qo'shing - qoida to'g'ri ishlashini
-- ko'rsatish uchun eng arzon dalil.

-- 3) Ko'chirib bo'lmaydigan qatorlar bilan nima qilinadi?
SELECT count(*) FROM customer
 WHERE phone IS NOT NULL AND normalize_phone(phone) IS NULL;
-- Javob "jim tashlab yuboriladi" bo'lsa - bu blocker. Bu qatorlar
-- hisobotga yozilishi va qo'lda ko'rilishi kerak.
```

## 26.9 Review checklisti: ma'lumot to'g'riligi

| Savol | Nega |
| --- | --- |
| Yangi ustun uchun `NOT NULL` va `DEFAULT` to'g'rimi | Noma'lum holat |
| `CHECK` constraint lar bormi | Kod tekshiruvi yetarli emas |
| Yagonalik unique indeks bilan majburlanganmi | Poyga |
| Biznes qoidasi partial unique bilan ifodalanishi mumkinmi | Eng kuchli himoya |
| Pul `numeric` va valyuta bilanmi | Aniqlik va aralashuv |
| Vaqt `timestamptz` mi | Zona xatolari |
| Enum qiymatlari baza va kodda mosmi | Deploy xatosi |
| NULL ning ma'nosi aniqmi | Uch holatli mantiq |
| FK qoidasi (`CASCADE`/`RESTRICT`) ongli tanlanganmi | Ma'lumot yo'qolishi |
| FK ustunida indeks bormi | Sekin o'chirish |
| Soft delete hamma so'rovda hisobga olinadimi | Ma'lumot oqishi |
| Ma'lumot ko'chirish namuna bilan tekshirilganmi | Jim buzilish |
| Ko'chirilmaydigan qatorlar hisobotga tushadimi | Jim yo'qotish |

## 26.10 Amalda qo'llash

- [ ] Eng muhim beshta jadval uchun invariantlar ro'yxatini yozib, ularning qanchasi DB constraint bilan himoyalanganini aniqlang.
- [ ] Idempotentlik va yagonalik talab qiladigan barcha joylarda unique indeks borligini tasdiqlang.
- [ ] Pul ustunlarini `numeric` ga va `double precision`/`money` dan o'tkazish rejasini tuzing.
- [ ] `timestamp` (zonasiz) ustunlarni toping va `timestamptz` ga migratsiya rejasini yozing.
- [ ] Enum va DB constraint mosligini tekshiradigan testni qo'shing.
- [ ] Indekssiz FK larni topadigan so'rovni ishga tushirib, kerakli indekslarni qo'shing.
- [ ] Nullable ustunlar uchun NULL ning ma'nosini `GLOSSARY.md` yoki jadval izohida (`COMMENT ON COLUMN`) yozib qo'ying.
- [ ] Soft delete ishlatiladigan jadvallar uchun aktiv qatorlar view ini yoki RLS ni joriy qiling.
- [ ] Ma'lumot ko'chiradigan PR lar uchun "20 qator namuna + ko'chirilmaydiganlar soni" talabini kiriting.

---

[&larr; 25. Migratsiya review: qulf, backfill, orqaga moslik](25-migratsiya-review-qulf-backfill-orqaga.md) · [Mundarija](README.md) · [27. Izolyatsiya, poyga holatlari va xabar yetkazish &rarr;](27-izolyatsiya-poyga-holatlari-va-xabar.md)
