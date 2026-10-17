<!-- doc: architect | chapter: 40 | part: VII. Kengaytirilgan mavzular -->

[Barcha hujjatlar](../../README.md) / [Arxitektor miyasi](README.md)

> Holat: tekshirilmoqda. Da'volar hali manbaga solishtirilmoqda.

# 40. Qidiruv: PostgreSQL FTS chegarasi va alohida dvigatelga o'tish (Search: Postgres FTS and Moving to a Dedicated Engine)

<details>
<summary>Bu bobdagi 11 bo'lim</summary>

- [40.1 Qachon PostgreSQL to'liq matn qidiruvi yetadi](#401-qachon-postgresql-toliq-matn-qidiruvi-yetadi)
- [40.2 `tsvector`, `tsquery` va indeks tanlovi](#402-tsvector-tsquery-va-indeks-tanlovi)
- [40.3 PostgreSQL FTS ning qattiq chegaralari](#403-postgresql-fts-ning-qattiq-chegaralari)
- [40.4 Relevantlik: `ts_rank` nimani hisoblaydi va nimani hisoblamaydi](#404-relevantlik-ts_rank-nimani-hisoblaydi-va-nimani-hisoblamaydi)
- [40.5 Til va morfologiya: dictionary, stemmer va o'zbek tili holati](#405-til-va-morfologiya-dictionary-stemmer-va-ozbek-tili-holati)
- [40.6 Alohida dvigatelga o'tish mezonlari](#406-alohida-dvigatelga-otish-mezonlari)
- [40.7 Indeksni to'ldirish: CDC, outbox va qayta indekslash](#407-indeksni-toldirish-cdc-outbox-va-qayta-indekslash)
- [40.8 Ikki manba muammosi: lag, izchillik va yo'qolgan yozuv](#408-ikki-manba-muammosi-lag-izchillik-va-yoqolgan-yozuv)
- [40.9 Qidiruv sifatini o'lchash](#409-qidiruv-sifatini-olchash)
- [40.10 Operatsion narx: shard, xotira va yangilash](#4010-operatsion-narx-shard-xotira-va-yangilash)
- [40.11 Amalda qo'llash](#4011-amalda-qollash)

</details>


Qidiruv arxitekturada aldamchi mavzu: `LIKE '%mato%'` bilan boshlanadi, keyin PostgreSQL ning to'liq matn qidiruviga o'tadi, keyin kimdir "Elasticsearch qo'yamiz" deydi va tizimga ikkinchi ma'lumot manbasi kiradi. Har bosqich o'z narxini oladi va ularning narxi bir xil emas. Bu bobda qaysi bosqichda turish kerakligini belgilaydigan mezonlar va o'tish qilinganda paydo bo'ladigan masalalar.

## 40.1 Qachon PostgreSQL to'liq matn qidiruvi yetadi

PostgreSQL ning FTS i to'laqonli qidiruv dvigateli emas, lekin ko'p loyihada u yetadi va uning eng katta afzalligi arxitekturada: ma'lumot bitta joyda qoladi, tranzaksiya bitta, izchillik masalasi yo'q.

Yetadigan holatlar aniq: qidiruv ikkilamchi funksiya (admin panelidagi qidiruv, qo'llanma ichidan topish), hujjat soni million atrofida, so'rov tilida oddiy so'z va ibora bor, relevantlik tartibi "to'g'ri bo'lsa yaxshi" darajasida, va qidiruv so'rovlari umumiy yukning kichik ulushi.

Yetmay qoladigan holatlar ham aniq va ular 40.6 da mezon bilan beriladi. Oraliq qaror esa odatda eng to'g'ri: FTS ni qoldirib, faqat muammoli qismni (masalan, avtoto'ldirish) alohida hal qilish.

```sql
-- Generatsiya qilingan ustun: tsvector ni qo'lda yangilash kerak emas
ALTER TABLE product ADD COLUMN search tsvector
    GENERATED ALWAYS AS (
        setweight(to_tsvector('simple', coalesce(name, '')), 'A') ||
        setweight(to_tsvector('simple', coalesce(description, '')), 'B')
    ) STORED;

CREATE INDEX product_search_idx ON product USING GIN (search);

SELECT id, name
FROM product
WHERE search @@ websearch_to_tsquery('simple', 'olma telefon')
ORDER BY ts_rank(search, websearch_to_tsquery('simple', 'olma telefon')) DESC
LIMIT 20;
```

## 40.2 `tsvector`, `tsquery` va indeks tanlovi

FTS ikki turga tayanadi: `tsvector` qayta ishlangan hujjat (leksemalar va ularning pozitsiyalari), `tsquery` esa qayta ishlangan so'rov. Ularni `@@` operatori solishtiradi. Hujjatni har so'rovda qayta hisoblash qimmat, shuning uchun u ustunda saqlanadi va indekslanadi.

So'rovni qurishning uch yo'li bor va tanlov foydalanuvchi kiritishiga bog'liq: `to_tsquery` qat'iy sintaksis talab qiladi va yaroqsiz kiritishda istisno beradi; `plainto_tsquery` hamma so'zni `AND` bilan bog'laydi; `websearch_to_tsquery` esa qidiruv tizimlari sintaksisini (qo'shtirnoq, `or`, `-`) tushunadi va yaroqsiz kiritishda yiqilmaydi. Tashqi foydalanuvchi kiritishi uchun oxirgisi standart tanlov.

Indeks tanlovi ikkita: GIN va GiST. GIN kattaroq va qurilishi sekinroq, lekin qidiruvda tezroq va aniq; GiST kichikroq va yozishda arzonroq, lekin u yo'qotishli (lossy) tuzilma, ya'ni natijalar qayta tekshiriladi. Statik yoki kam o'zgaradigan matn uchun GIN, tez-tez yangilanadigan katta jadval uchun GiST yoki GIN ning `fastupdate` rejimi ko'riladi. Indeks turlarining umumiy taqqoslanishi [indekslar bobida](23-indekslar-b-tree-gin-gist-brin-va-tanlov.md#236-gin-massiv-jsonb-va-toliq-matn-qidiruvi-uchun).

## 40.3 PostgreSQL FTS ning qattiq chegaralari

Bu chegaralar sozlama bilan o'zgarmaydi, ular implementatsiyaga qadalgan va qo'llanmada ro'yxat bo'lib berilgan. Ular katta hujjat bilan ishlaganda to'siq bo'ladi.

| Chegara | Qiymat |
|---|---|
| Bitta leksema uzunligi | 2 KB dan kam |
| Bitta leksema uchun pozitsiya soni | 256 dan ko'p emas |
| Pozitsiya qiymati | 1 dan 16383 gacha |
| `tsvector` ma'lumotining uzunligi | 1 MB dan kam |
| `tsquery` ma'lumotining uzunligi | 1 MB dan kam |
| `<N>` (FOLLOWED BY) operatoridagi masofa | 16384 dan ko'p emas |

Amaliy ma'nosi: uzun hujjat (kitob bobi, shartnoma matni) bitta `tsvector` ga sig'masligi mumkin va u bo'laklarga bo'linishi kerak. Pozitsiya chegarasi esa ibora bo'yicha qidiruvni uzun hujjatning oxirida ishonchsiz qiladi: 16383 dan keyingi so'zlarning pozitsiyasi saqlanmaydi, demak ibora mosligi u yerda topilmaydi.

## 40.4 Relevantlik: `ts_rank` nimani hisoblaydi va nimani hisoblamaydi

`ts_rank` so'z chastotasi va `setweight` bilan berilgan vaznga qarab ball beradi. Bu matn ichidagi moslikni o'lchaydi, boshqa hech narsani o'lchamaydi.

Hisoblamaydigan narsalar ro'yxati qidiruv sifati haqidagi kutilmani belgilaydi: hujjatning mashhurligi, bosilish statistikasi, yangilik, foydalanuvchining oldingi xatti-harakati, geografik yaqinlik, shaxsiylashtirish, imlo xatosiga toqat, sinonim (lug'at bilan qo'lda qo'shilmasa) va noto'g'ri klaviatura layoutida yozilgan so'rov. Qidiruv mahsulotning asosiy funksiyasi bo'lsa, shu ro'yxatning yarmi talab bo'ladi va uni `ts_rank` ustiga qurib bo'lmaydi.

Shu sababli qaror sifat talabi bilan o'lchanadi, hujjat soni bilan emas: 50 ming hujjatli, lekin relevantlik muhim bo'lgan tizim alohida dvigatelni talab qiladi, 5 million hujjatli admin qidiruvi esa FTS da qoladi.

## 40.5 Til va morfologiya: dictionary, stemmer va o'zbek tili holati

FTS matnni leksemaga aylantirishda lug'at (dictionary) zanjiridan o'tkazadi: parser so'zni ajratadi, stop word lar tashlanadi, qolganlari stemmer bilan o'zakka keltiriladi. Shu sababli natija tilga bog'liq: `english` konfiguratsiyasi `running` ni `run` ga keltiradi, `simple` esa hech narsa qilmaydi, faqat kichik harfga o'tkazadi.

O'zbek tili uchun PostgreSQL da tayyor konfiguratsiya yo'q. Amalda uch yo'l bor. Birinchisi `simple` bilan qolish: morfologiya yo'q, "kitoblarni" va "kitob" boshqa leksema bo'ladi. Ikkinchisi `unaccent` va sinonim lug'at bilan eng ko'p uchraydigan shakllarni qo'lda bog'lash: arzon, lekin qo'lda saqlanadi. Uchinchisi Snowball yoki Hunspell lug'atini ulash: PostgreSQL ikkisini ham qo'llaydi, lekin o'zbek tili uchun lug'at fayli tashqi manbadan olinadi va uning sifati alohida tekshiriladi.

Lotin va kirill yozuvi bir vaqtda ishlatiladigan loyihada yana bitta qaror bor: indekslashdan oldin matnni bitta yozuvga normallashtirish. Buni qidiruv vaqtida qilish mumkin emas, chunki indeks allaqachon qurilgan bo'ladi.

## 40.6 Alohida dvigatelga o'tish mezonlari

O'tish qarori "Elasticsearch zo'r" degan gapdan emas, mezondan chiqadi. Quyidagilardan kamida ikkitasi bajarilsa, o'tish asosli bo'ladi.

| Mezon | Nega FTS yetmaydi |
|---|---|
| Relevantlik mahsulot sifatining qismi | `ts_rank` faqat matn moslikni biladi (40.4) |
| Imlo xatosiga toqat va "shunga o'xshash" qidiruv kerak | fuzzy moslik FTS da yo'q, `pg_trgm` esa boshqa masala hal qiladi |
| Avtoto'ldirish, 100 ms dan kichik javob talabi | har bosishda GIN qidiruvi OLTP bazasiga tushadi |
| Faset (kategoriya bo'yicha sanoq) va agregatsiya | har faset uchun alohida `count` so'rovi kerak bo'ladi |
| Qidiruv yuki OLTP ga ta'sir qilyapti | qidiruv buffer cache ni to'ldiradi (26.13) |
| Hujjat `tsvector` chegaralariga sig'mayapti | 40.3 dagi 1 MB va pozitsiya chegarasi |
| Ko'p tilli morfologiya va sinonim boshqaruvi | lug'at zanjirini qo'lda saqlash qimmatlashadi |

Bitta mezon bajarilsa, odatda arzonroq yechim topiladi: faset uchun oldindan hisoblangan jadval, avtoto'ldirish uchun `pg_trgm` bilan alohida kichik indeks, OLTP ta'siri uchun standby ga yo'naltirish.

## 40.7 Indeksni to'ldirish: CDC, outbox va qayta indekslash

Alohida dvigatel qo'shilgandan keyin asosiy ish qidiruv emas, **sinxronizatsiya** bo'ladi. To'rt yo'l bor va ularning ishonchliligi farq qiladi.

| Yo'l | Qanday | Xavfi |
|---|---|---|
| Ikki tomonga yozish | kod bazaga ham, indeksga ham yozadi | tranzaksiya yo'q: biri o'tadi, biri yo'q |
| Tranzaksion outbox | o'zgarish bazaga bitta tranzaksiyada yoziladi, worker indeksga uzatadi | kechikish bor, lekin yozuv yo'qolmaydi |
| CDC (logical replication, Debezium) | WAL dan o'qiladi | sxema o'zgarishi va boshlang'ich yuklash alohida ish |
| Davriy to'liq qayta indekslash | belgilangan vaqtda hammasi qaytadan | oddiy, lekin kechikish katta va yuk cho'qqisi |

Ishlab chiqarishda odatda outbox yoki CDC tanlanadi, chunki ular yozuv yo'qolmasligini kafolatlaydi. Outbox ning to'liq yozuvi [patternlar hujjatida](../patterns/10-malumotlarni-boshqarish-va-taqsimlash.md#1014-tranzaksion-outbox-transactional-outbox).

Qayta indekslash imkoniyati esa arxitektura talabi bo'ladi, qulaylik emas: mapping o'zgarganda, analyzer sozlamasi o'zgarganda yoki indeks buzilganda uni noldan qurish kerak bo'ladi. Shu sababli indeks **hosila** ma'lumot deb qaraladi va uning yagona haqiqat manbasi baza bo'lib qoladi. Yangi indeksga alias bilan o'tish (eski indeks turgan holda yangisini qurib, keyin alias ni almashtirish) shu talabning amaliy shakli.

## 40.8 Ikki manba muammosi: lag, izchillik va yo'qolgan yozuv

Qidiruv indeksi qo'shilishi bilan tizimda ikki manba paydo bo'ladi va ular hech qachon bir vaqtda bir xil holatda bo'lmaydi. Buni yashirish emas, oshkor qilish kerak.

Uchta amaliy oqibat bor. Birinchisi: foydalanuvchi yaratgan yozuv qidiruvda darhol ko'rinmaydi. Yechim interfeysda: yangi yaratilgan yozuvni ro'yxatga qidiruvdan emas, bazadan qo'shib ko'rsatish, yoki "indekslanmoqda" holatini ko'rsatish. Ikkinchisi: o'chirilgan yozuv qidiruvda qolib ketishi mumkin, shuning uchun qidiruv natijasi bazadan qayta tekshiriladi va topilmaganlari tashlanadi. Uchinchisi: qidiruv natijasidagi maydonlar eskirgan bo'lishi mumkin, shu sababli ro'yxatda ko'rsatiladigan narx yoki qoldiq kabi maydonlar indeksdan emas, bazadan olinadi.

Oxirgi qoida eng ko'p buziladigani: indeksga hamma maydonni yozib, uni o'qish uchun asosiy manba qilish. Shunda indeks biznes ma'lumotining nusxasiga aylanadi va har bir sxema o'zgarishi ikki joyda bajariladi.

## 40.9 Qidiruv sifatini o'lchash

Qidiruvni "yaxshilash" o'lchovsiz ma'nosiz, chunki har o'zgarish bir so'rovni yaxshilab, boshqasini buzadi. Ikki xil o'lchov ishlatiladi va ikkisi ham kerak.

Oflayn o'lchov: belgilangan so'rovlar to'plami va ular uchun kutilgan natijalar (relevantlik belgilari) yozib qo'yiladi, keyin har o'zgarishdan keyin precision va recall hisoblanadi. Bu regressiyani ushlaydi va uni CI ga qo'yish mumkin.

Onlayn o'lchov: qidiruvdan keyin bosilgan natijaning o'rni (birinchi bosish pozitsiyasi), natijasiz so'rovlar ulushi, so'rovni qayta yozish ulushi va qidiruvdan keyin savatga qo'shish ulushi. Natijasiz so'rovlar ro'yxati eng arzon va eng foydali manba: u lug'at, sinonim va mahsulot nomlaridagi bo'shliqni to'g'ridan-to'g'ri ko'rsatadi.

## 40.10 Operatsion narx: shard, xotira va yangilash

Alohida dvigatel qo'shilishi bitta kutubxona qo'shish emas, yangi ishlab turuvchi tizim qo'shish. Uning narxi uchta joyda paydo bo'ladi.

Birinchisi xotira: qidiruv dvigatelining tezligi fayl tizimi keshiga tayanadi, ya'ni indeks hajmining sezilarli qismi RAM da bo'lishi kutiladi. Shu sababli "qidirilmaydigan maydonlarni indeksga yozmaslik" tavsiyasi tezlik tavsiyasi bo'lib qoladi: indeks kichik bo'lsa, u keshga sig'adi.

Ikkinchisi tuzilish qarorlari: shard soni indeks yaratilganda tanlanadi va keyin uni o'zgartirish qayta indekslashni talab qiladi; replika soni esa o'qish sig'imi va chidamlilikni belgilaydi. Bu qarorlar partitioning qarorlariga o'xshaydi: ularni keyinga qoldirish qimmat.

Uchinchisi yangilash va mos kelish: dvigatelning katta versiyalari orasida mapping va so'rov sintaksisi o'zgaradi, klaster yangilanishi esa alohida rejani talab qiladi. Shu sababli qidiruvni kod darajasida o'ramga olish kerak: so'rov qurish va natijani o'qish bitta adapter ichida qoladi ([chegara interfeysi](../clean-code/14-obyekt-va-malumot-tuzilmasi-inkapsulyatsiya.md#1411-chegara-interfeysini-tizim-boylab-uzatmaslik)), shunda dvigatel almashtirilsa, o'zgarish bitta joyga tegadi.

## 40.11 Amalda qo'llash

- [ ] Hozirgi qidiruvning so'rov hajmini va p95 vaqtini o'lchang, keyin uni umumiy OLTP yukining ulushi sifatida yozib qo'ying.
- [ ] 40.6 jadvalidagi yettita mezonni o'z tizimingizga qo'llab, nechtasi bajarilayotganini sanang: ikkitadan kam bo'lsa, FTS da qolish qarorini yozib qo'ying.
- [ ] Eng uzun hujjatning `tsvector` hajmini `pg_column_size` bilan tekshirib, 1 MB chegarasiga qancha qolganini bilib oling.
- [ ] Natijasiz qidiruv so'rovlarini bir hafta yozib, eng ko'p uchraydigan 50 tasini ko'rib chiqing: ular lug'at va sinonim ishini belgilaydi.
- [ ] Agar alohida dvigatel bor bo'lsa, indeksni noldan qayta qurish jarayonini sinab ko'ring va qancha vaqt olishini o'lchang.
- [ ] Qidiruv natijasida ko'rsatiladigan maydonlarni ko'rib chiqing: narx, qoldiq va holat kabi o'zgaradigan maydonlar bazadan olinayotganini ta'minlang.
- [ ] Oflayn o'lchov uchun 50 so'rovdan iborat to'plam tuzib, kutilgan natijalarni belgilab qo'ying va uni CI ga ulang.

## Manbalar

- [PostgreSQL 17, Full Text Search: Limitations (textsearch.sgml)](https://raw.githubusercontent.com/postgres/postgres/REL_17_STABLE/doc/src/sgml/textsearch.sgml) - leksema 2 KB, pozitsiya 16383, `tsvector` va `tsquery` 1 MB, FOLLOWED BY masofasi 16384
- [PostgreSQL 17, Full Text Search: Parsing and Dictionaries (textsearch.sgml)](https://raw.githubusercontent.com/postgres/postgres/REL_17_STABLE/doc/src/sgml/textsearch.sgml) - lug'at zanjiri, stop word, Snowball va Hunspell qo'llovi
- [PostgreSQL 17, Indexes: GIN va GiST (indices.sgml)](https://raw.githubusercontent.com/postgres/postgres/REL_17_STABLE/doc/src/sgml/indices.sgml) - GiST ning yo'qotishli ekani va qayta tekshirish
- [Elasticsearch 8.15, Tune for search speed](https://raw.githubusercontent.com/elastic/elasticsearch/v8.15.0/docs/reference/how-to/search-speed.asciidoc) - fayl tizimi keshiga xotira berish, kam maydon qidirish, ma'lumotni oldindan indekslash, identifikatorni `keyword` qilish
- [Elasticsearch 8.15, Mapping](https://raw.githubusercontent.com/elastic/elasticsearch/v8.15.0/docs/reference/mapping.asciidoc) - mapping o'zgarishi qayta indekslashni talab qilishi
- Martin Kleppmann, *Designing Data-Intensive Applications*, 11-bob - hosila ma'lumot va indeksni qayta qurish tushunchasi

---

[&larr; 39. Birinchi 90 kun va o'z-o'zini baholash](39-birinchi-90-kun-va-oz-ozini-baholash.md) · [Mundarija](README.md) · [41. Ko'p region: kechikish, ma'lumot rezidentligi va failover &rarr;](41-kop-region-kechikish-rezidentlik-failover.md)
