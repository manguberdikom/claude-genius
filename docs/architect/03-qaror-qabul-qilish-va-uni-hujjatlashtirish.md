<!-- doc: architect | chapter: 3 | part: I. Fikrlash va qarorlar -->

[Kod yozadigan arxitektorning miyyasi](../../README.md) / [Arxitektor miyyasi](README.md)

# 3. Qaror qabul qilish va uni hujjatlashtirish (Decisions and ADRs)

<details>
<summary>Bu bobdagi 11 bo'lim</summary>

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
- [3.11 Amalda qo'llash](#311-amalda-qollash)

</details>



Arxitektorning asosiy mahsuloti kod emas, qaror. Kod qaytarilishi mumkin, qaror esa jamoaning keyingi ikki yilini belgilaydi. Qaror yozilmasa, u yo'q: olti oydan keyin "nega bu yerda Kafka turibdi" degan savolga javob beradigan hujjat kerak. Bu bob qarorni qanday pishitish, qanday yozib qo'yish va keyin uning natijasini qanday kuzatish haqida.

## 3.1 ADR (Architecture Decision Record) tuzilishi: kontekst, qaror, oqibat, holat

ADR bitta qarorni tasvirlaydigan qisqa fayl. U loyiha hujjati emas, tarix yozuvi: bir marta yoziladi va keyin o'zgartirilmaydi, faqat holati almashadi. To'rtta majburiy qismi bor. Kontekst: qaror paytidagi haqiqat, raqamlar bilan. Qaror: bitta gap, "biz X ni tanlaymiz" shaklida. Oqibat: nimani qo'lga kiritdik va nimani yo'qotdik, ikkinchisi birinchisidan muhimroq. Holat: Taklif qilindi, Qabul qilindi, Rad etildi, Eskirdi yoki O'rnini bosdi.

Eng ko'p xato qilinadigan joy kontekst. "Tizim tez ishlashi kerak" kontekst emas. "Buyurtma qidiruvi p95 da 1.8 soniya, maqsad 300 ms, kunlik qidiruv soni taxminan 40 ming, baza hajmi 180 GB" kontekst. Kontekst o'qilganda qaror o'z-o'zidan kelib chiqishi kerak. Agar o'qiganingizda "unda nega boshqasini tanlamadilar" degan savol tug'ilsa, kontekst to'liq emas.

Oqibat bo'limi ADR ni boshqa hujjatdan ajratib turadi. Har bir qaror narx bilan keladi va bu narxni oldindan yozib qo'yish keyin "bizni hech kim ogohlantirmagan" deyishning oldini oladi. Qaytarish narxini ham shu yerga yozing: bir haftalik ish bo'ladimi yoki uch oylik migratsiya.

```markdown
# ADR-0042: <Qaror sarlavhasi, fe'l bilan>

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

Taqqoslashni jadvalga aylantirish muhokamani fikrdan mezonga ko'chiradi. Mezonlarni variantlarni ko'rib chiqishdan OLDIN yozing, aks holda mezonlar o'zingiz yoqtirgan variantga moslashib qoladi. Har bir mezonga og'irlik bering: yig'indisi 100 bo'lsin. Og'irlik haqidagi tortishuv eng foydalisi, chunki u yashirin ustuvorliklarni ochadi.

Ball bering, lekin ballga ishonib qolmang. Jadval qarorni chiqarmaydi, u qaror qayerda tug'ilishini ko'rsatadi. Agar bir variant 71, ikkinchisi 69 ball olsa, bu "tenglik" degani: unda ikkinchi darajali omil, masalan jamoaning tajribasi yoki qaytarish narxi hal qiladi. Agar farq 20 balldan oshsa, muhokamani yoping.

| Mezon | Og'irlik | PostgreSQL FTS | Alohida qidiruv tizimi |
|---|---|---|---|
| Qidiruv sifati (tilga mos, ranking) | 25 | 3 | 5 |
| p95 latency 300 ms ga sig'ishi | 20 | 4 | 5 |
| Operatsion murakkablik | 20 | 5 | 2 |
| Ma'lumot izchilligi | 15 | 5 | 2 |
| Jamoa tajribasi | 10 | 5 | 3 |
| 12 oylik umumiy narx | 10 | 5 | 3 |
| Og'irlangan yig'indi (100 dan) | | 85 | 72 |

## 3.3 Oxirgi mas'ul daqiqa (last responsible moment) tamoyili

Har bir qarorni iloji boricha kechiktirish kerak degan fikr noto'g'ri tushuniladi. Tamoyil "kechiktir" demaydi, "qaror qilmaslik qimmatga tusha boshlagan daqiqada qaror qil" deydi. Bu daqiqani topish uchun ikki narxni taqqoslaysiz: kutish narxi va erta qaror narxi. Kutish narxi bu to'siqdagi jamoa, vaqtincha yechim va ikki marta yoziladigan kod. Erta qaror narxi bu noto'g'ri tanlovni keyin yechib tashlash.

Amalda bu shunday ko'rinadi. Buyurtma servisida "qanday message broker" savolini birinchi sprintda hal qilish shart emas, agar siz hodisani chiqarishni interfeys orqasiga yashirgan bo'lsangiz va dizayn [patternlar hujjatidagi](../patterns/README.md) outbox pattern ni qo'llagan bo'lsangiz. Lekin "buyurtma identifikatori UUID bo'ladimi yoki bigint" savolini kechiktirish mumkin emas: u sxemaga, indeks hajmiga va tashqi integratsiyaga kirib ketadi, bir hafta o'tgach o'zgartirish migratsiya bo'ladi.

Qoida sifatida: ma'lumot sxemasi, identifikator turi, tranzaksiya chegaralari va autentifikatsiya modeli erta qaror qilinadi, chunki ularning qaytarish narxi vaqt bilan tez o'sadi. Cache qatlami, qidiruv tizimi, broker tanlovi va deployment topologiyasi esa kechiktirilishi mumkin, chunki ular interfeys orqasida turadi. ADR da "nega hozir" degan bir qatorni yozib qo'ying: bu qaror vaqtini ham hujjatlashtiradi.

## 3.4 Taxminlarni yozib qo'yish va keyin ularni tekshirish

Har bir qaror ostida tekshirilmagan taxminlar yotadi. "Kunlik buyurtma soni 50 mingdan oshmaydi", "hisobot kechikishi 5 daqiqa bo'lishi mumkin", "ombor qoldig'i faqat bitta mintaqada o'zgaradi". Bu taxminlar yozilmasa, ular haqiqatga aylanib qoladi va keyin hech kim ularni shubha ostiga olmaydi.

Har bir taxminga uch narsa biriktiring: qanday o'lchanadi, qachon tekshiriladi, buzilsa nima qilinadi. Uchinchisi eng qimmatli: "agar kunlik buyurtma 200 mingdan oshsa, partitsiyalashga o'tamiz" degan qator keyingi arxitektorga tayyor yo'l xaritasi beradi.

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

Spike bu vaqti chegaralangan tadqiqot: maqsadi mahsulot emas, javob. Spike ni boshlashdan oldin uch narsani yozing: qaysi savolga javob izlayapmiz, qancha vaqt beramiz, qanday natija javob hisoblanadi. Vaqt chegarasi bo'lmasa spike loyihaga aylanadi. Odatda ikki kundan besh kungacha yetadi.

Spike kodi tashlab yuboriladi va bu ataylab shunday. Agar spike kodi ishlab chiqarishga ketsa, u prototip emas, shoshilib yozilgan tizim. Prototip esa boshqa narsa: u ishlab chiqarish yo'liga kiradigan, lekin cheklangan qamrovdagi haqiqiy kod. Spike dan prototipga o'tish ham qaror va u ADR da aks etishi kerak.

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

Texnik kelishmovchilik normal holat va uni yo'q qilishga urinish eng yomon strategiya. Yo'q qilinishi kerak bo'lgan narsa boshqa: hal bo'lmagan kelishmovchilikning kodda ikki xil uslub sifatida qotib qolishi. Shuning uchun har bir qarorga egasi tayinlanadi. Ega ovoz yig'maydi, u fikrlarni eshitib qaror chiqaradi va natija uchun javob beradi.

Qoida oddiy: muhokama ochiq, qaror yopiq. Muhokama davrida har kim e'tirozini yozma shaklda, ADR ga izoh sifatida qo'yishi kerak. Yozma e'tiroz og'zakisidan foydaliroq, chunki u aniq bo'lishga majbur qiladi: "menga yoqmaydi" dan "bu yondashuvda hisobot so'rovi asosiy bazaga yuk beradi" ga o'tadi. Qaror chiqqandan keyin esa "rozi emasman, lekin bajaraman" qoidasi kuchga kiradi. Ya'ni e'tiroz yozib qoldiriladi, lekin hamma bir xil qarorni bajaradi va unga qarshi ishlamaydi.

Bu qoidaning ikkita sharti bor. Birinchisi: e'tiroz ADR da ko'rinadigan joyda qoladi, "Rad etilgan e'tirozlar" bo'limida. Ikkinchisi: qayta ko'rish sanasi belgilanadi. Agar e'tiroz egasi haq bo'lsa, oradan olti oy o'tib metrika buni ko'rsatadi va ADR qayta ochiladi. Shu ikki shart bo'lsa, jamoa qarorni osonroq qabul qiladi: fikr yo'q qilinmagan, navbatga qo'yilgan.

## 3.7 Qaror oqibatini kuzatish: metrika va qayta ko'rish sanasi

Kuzatilmagan qaror tekshirilmagan gipotezaga teng. ADR da kamida bitta metrika va bitta sana bo'lishi kerak. Metrika qarorning asosiy da'vosini o'lchasin: "qidiruv tezlashadi" degan qaror uchun qidiruv latency si o'lchanadi, umumiy CPU emas.

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

ADR kod bilan bir repoda, `docs/adr/` papkasida yashashi kerak. Sababi oddiy: alohida wiki da turgan hujjat kod o'zgarganda yangilanmaydi, pull request ichidagi fayl esa review ga tushadi. Nom shabloni `NNNN-qisqa-sarlavha.md`, raqam to'rt xonali va ketma-ket. Raqamni qayta ishlatmang, hatto ADR rad etilgan bo'lsa ham: raqam tarixning bir qismi.

Eskirgan ADR o'chirilmaydi va tahrirlanmaydi. Uning holati `Eskirdi` yoki `O'rnini bosdi: ADR-0057` ga o'zgaradi va shu bitta qator qo'shiladi. Mazmuni esa o'sha paytdagi haqiqat sifatida qoladi. Keyingi odam "nega avval boshqacha edi" savoliga javob topadi, bu esa bir xil xatoning takrorlanishini to'xtatadi.

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

Eng keng tarqalgan nosog'lom ADR bu keyin yozilgan oqlash hujjati. Uni tanib olish oson: unda bitta variant bor, salbiy oqibatlar bo'limi bo'sh yoki "jiddiy salbiy oqibat yo'q" deb yozilgan, va kontekstda birorta raqam yo'q. Bunday hujjat ma'lumot bermaydi, faqat qarorni muhokamadan himoya qiladi. Agar qaror chindan ham allaqachon qilingan bo'lsa, buni ochiq yozing: "Bu qaror 2025 yil dekabrda amalga oshirilgan, ADR retrospektiv yozilmoqda". Shu bir gap hujjatning ishonchini saqlaydi.

| Tuzoq | Nega xavfli | Yechim |
|---|---|---|
| Bitta variantli ADR | Muqobil ko'rib chiqilmaganini yashiradi | Kamida ikki rad etilgan variant va rad sababi |
| Salbiy oqibatsiz ADR | Narx yashiringan, keyin kutilmagan bo'lib chiqadi | "Salbiy" bo'limi bo'sh ADR review dan o'tmaydi |
| Raqamsiz kontekst | Qaror did asosida qilinganini bildiradi | Latency, hajm, QPS, muddat yoziladi |
| Eski ADR ni tahrirlash | Tarix yo'qoladi, sabab izi uziladi | Yangi ADR, eskisiga "O'rnini bosdi" |
| 20 betlik ADR | Hech kim o'qimaydi | Bir betga sig'sin, chuqur tahlil ilova havolasida |
| Sanasiz qayta ko'rish | Qaror hech qachon tekshirilmaydi | Majburiy maydon, CI tekshiradi |
| Egasi yo'q ADR | Javobgarlik tarqaladi | Bitta ism, jamoa nomi yetarli emas |
| Spike natijasiz qaror | Taxmin ma'lumot o'rniga qo'yiladi | EXPLAIN yoki yuklama testi natijasi ilova qilinadi |

## 3.10 To'liq misol: PostgreSQL da qolish yoki alohida qidiruv tizimi qo'shish qarori

Holat shunday. Buyurtma qidiruvi admin panelda ishlatiladi, kunlik taxminan 40 ming so'rov, `orders` jadvalida 42 million qator, jadval hajmi taxminan 180 GB. Hozirgi qidiruv `ILIKE '%...%'` bilan qurilgan va p95 da 1.8 soniya beradi. Maqsad 300 ms. Jamoa uch kishi, alohida infratuzilma injeneri yo'q. Spike S-07 natijasi: generated `tsvector` ustun va GIN indeks bilan p95 taxminan 90 ms, indeks hajmi taxminan 11 GB, yozish tezligi taxminan 7 foizga pasaydi.

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
1. Alohida qidiruv klasteri: eventual izchillik qo'shadi. 72/100 ball.
2. Faqat trigram (pg_trgm): opechatkaga chidamli, lekin ranking yo'q.

## Oqibatlar
- Ijobiy: yangi tizim yo'q, qidiruv tranzaksiya bilan izchil.
- Salbiy: morfologiya cheklangan, facet va fuzzy qidiruv zaif.
- Qaytarish narxi: taxminan 6 hafta (outbox bilan indeksga ko'chirish).

## Taxminlar
- T1: qidiruv hajmi 12 oyda 3 barobardan oshmaydi. O'lchov: QPS metrikasi.

## Kuzatiladigan metrika
- order.search.duration p95 < 300 ms, order.search.empty ulushi < 8%
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

Bu ADR nimani ko'rsatdi: tanlov "yaxshi texnologiya" bilan "yomon texnologiya" orasida emas edi. Tanlov jamoaning uch kishiligi, izchillik talabi va 90 ms spike natijasi orasida edi. Agar oradan bir yil o'tib facet qidiruv mahsulot talabiga aylansa, T2 taxmini buziladi, ADR-0042 "O'rnini bosdi" bo'ladi va yangi ADR alohida indeks hamda outbox orqali sinxronizatsiyani yozadi. Bu muvaffaqiyatsizlik emas, bu ADR ning maqsadga muvofiq ishlashi.

## 3.11 Amalda qo'llash

- [ ] `docs/adr/` papkasini va `template.md` shablonini repoga qo'shing, raqamlash skriptini ishga tushiring.
- [ ] Oxirgi 12 oyda qilingan eng katta uch qarorni retrospektiv ADR sifatida yozing va retrospektiv ekanini ochiq belgilang.
- [ ] Har bir ochiq ADR ga qaror egasining ismini va qayta ko'rish sanasini qo'ying, egasiz ADR ni merge qilmang.
- [ ] CI ga ikki tekshiruv qo'shing: `Holat` qatori majburiy, muddati o'tgan qayta ko'rish sanalari ro'yxati haftalik chiqsin.
- [ ] Keyingi arxitektura qarori uchun mezon jadvalini og'irliklar bilan variantlarni ko'rishdan OLDIN tuzing.
- [ ] Hozir muhokamada turgan bitta savolni spike ga aylantiring: savol, vaqt chegarasi va javob mezonini yozib qo'ying.
- [ ] Har bir qabul qilingan ADR uchun bitta Micrometer metrikasi va bitta alert chegarasini kod bilan birga joylashtiring.
- [ ] Jamoa bilan "rozi emasman, lekin bajaraman" qoidasini kelishib oling va rad etilgan e'tirozlarni ADR ichida saqlaydigan bo'lim qo'shing.

---

[&larr; 2. Muammoni tushunish va to'g'ri savol berish](02-muammoni-tushunish-va-togri-savol-berish.md) · [Mundarija](README.md) · [4. Kod - muloqot vositasi: nomlash, aniqlik, kognitiv yuk &rarr;](04-kod-muloqot-vositasi-nomlash-aniqlik.md)
