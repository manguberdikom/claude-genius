# Hissa qo'shish qoidalari

Bu repozitoriy asosan oltita hujjatdan iborat korpus, `tools/` da uni
tekshiradigan va qidiradigan asboblar bor. Shuning uchun asosiy qoidalar
uslub va struktura haqida.

## Struktura

```text
docs/<hujjat>/README.md        hujjat mundarijasi va kirish
docs/<hujjat>/NN-slug.md       bitta bob
docs/manifest.json             boblar ro'yxati (tools/ shuni o'qiydi)
tools/build_single.py          docs/ -> dist/ monolit
tools/check_docs.py            tekshiruv (CI shuni ishlatadi)
.claude/skills/                Claude Code skilllari
```

`docs/` - `dist/` ning manbasi. `dist/` generatsiya natijasi, git ga
kirmaydi va qo'lda tahrir qilinmaydi.

Ildizdagi `DECISIONS.md` xulqni o'zgartirgan qarorlarni yozadi: nima
o'zgardi, nega, rad etilgan variantlar, xavf, qaysi tekshiruv o'tdi va
orqaga qaytarish yo'li. Hamma o'zgarish emas, faqat foydalanuvchi
muhitiga tegadigan, ma'lumot yo'qotishi mumkin bo'lgan yoki ruxsat
qarorini o'zgartiradigani. `check_docs.py` uni ham tekshiradi: em-dash
va kirill yo'q, asbob havolalari mavjud.

### Bob fayli shakli

```markdown
<!-- doc: patterns | chapter: 7 | part:  -->

[Barcha hujjatlar](../../README.md) / [Dizayn patternlar](README.md)

> Holat: AI yozgan, inson tekshirmagan.

# 7. Bob sarlavhasi (English Title)

<details>
<summary>Bu bo'limdagi 33 bo'lim</summary>
...
</details>

Bob matni.

---

[&larr; 6. Oldingi bob sarlavhasi](06-...md) · [Mundarija](README.md) · [8. Keyingi bob sarlavhasi &rarr;](08-...md)
```

Metadata izohi, breadcrumb, H1 va navigatsiya footer majburiy.
Breadcrumb ning birinchi havolasi ildiz README ga, ya'ni oltita hujjat
ro'yxatiga olib boradi, shuning uchun u har bobda `Barcha hujjatlar` deb
yoziladi. Footer havolasida qo'shni bobning raqami va to'liq o'zbekcha
sarlavhasi turadi.

Holat qatori (5-qator) **qo'lda yozilmaydi**: u `docs/review.tsv` dan
`python3 tools/review_status.py --yoz` bilan yasaladi.

`tools/check_docs.py` shaklni tekshiradi: metadata izohi manifest bilan
mos, breadcrumb 3-qatorda, holat qatori 5-qatorda va `review.tsv` ga
mos, H1 7-qatorda va manifest sarlavhasi bilan bir xil, bo'lim soni
manifest, README va `<summary>` bilan mos, footer oxirida turadi va
qo'shni boblarga ishora qiladi.

### Manbalar

Tekshirilgan bobda bob oxirida **raqamsiz** `## Manbalar` bo'limi
turadi. Joyi qat'iy: yopish bo'limidan (`Amalda qo'llash` yoki
`Arxitektor nazorat ro'yxati`) KEYIN, navigatsiya footeridan oldin.
Raqamsiz, chunki u bob bo'limi emas, apparat: manifest sanog'iga
kirmaydi va `doc.sh show` bilan ochilmaydi.

```markdown
## N.M Amalda qo'llash

- Yopish bo'limi.

## Manbalar

- [Spring Framework, Declarative transaction annotations](https://docs.spring.io/spring-framework/reference/data-access/transaction/declarative/annotations.html) - 6.0 dan beri protected va package-visible metodlar
- [PostgreSQL, Resource consumption](https://www.postgresql.org/docs/current/runtime-config-resource.html) - `work_mem` konteksti
- [sonar-java, S109](https://raw.githubusercontent.com/SonarSource/sonar-java/master/sonar-java-plugin/src/main/resources/org/sonar/l10n/java/rules/java/S109.json) - `scope: Main`
- Robert C. Martin, *Clean Code*, 17-bob
```

Faqat **birlamchi** manba: `docs.spring.io`, `postgresql.org/docs`,
`openjdk.org/jeps`, `docs.oracle.com/javase`, JLS, sonar-java rule
metadata, kutubxonaning rasmiy hujjati (JUnit, Mockito, Testcontainers,
Hibernate), yoki kitob nomi va bob raqami. Blog, Stack Overflow va
qayta hikoya qilgan maqola manba emas.

Qoidalar:

- Tekshirilgan bobda kamida bitta manba bo'ladi.
- Har **versiya** va **raqam** da'vosi uchun alohida manba: "Spring 7.0
  da keldi" va "default 2.0" ikki alohida qator.
- Har qator manbadan keyin qisqa izoh beradi: manba nimani tasdiqlaydi.
- Havola bobning o'zidagi da'voga ishora qilishi kerak, umumiy sahifaga
  emas: imkon bo'lsa aniq bo'lim anchori bilan.

### Raqamlar

Manbasiz foiz, millisekund, bayt yoki "N barobar" yozilmaydi. Uch yo'l
bor va boshqasi yo'q:

1. Manba bilan: raqam yonida yoki yuqoridagi uch qator ichida havola.
2. Belgilangan taxmin: `o'lchanmagan taxmin` so'zi bilan.
3. Olib tashlash: raqam gapning mohiyatini o'zgartirmasa, u ortiqcha.

`python3 tools/claims_report.py` holatni hujjat va bob bo'yicha
sanaydi. U faqat hisobot: CI ni yiqitmaydi, chunki qaysi raqam
o'lchangan va qaysi biri taxmin ekanini odam biladi.

```bash
python3 tools/claims_report.py                   # hamma hujjat
python3 tools/claims_report.py --bob architect 27
python3 tools/claims_report.py --batafsil        # har da'voning qatori
```

## Til

- **O'zbek lotin yozuvi.** Kirill harf bo'lmasligi kerak; CI buni tekshiradi.
- **Texnik atamalar inglizcha qoladi.** Ro'yxat: [GLOSSARY.md](GLOSSARY.md).
  Tarjima qilinadigan va qilinmaydigan atamalar shu faylda belgilangan.
- Annotatsiya, sinf, metod va konfiguratsiya kaliti hech qachon tarjima
  qilinmaydi: `@Transactional`, `HikariCP`, `spring.datasource.url`.
- Yangi atama tarjima qilinsa, GLOSSARY.md ga qo'shiladi.

## Hujjat konvensiyalari

Har hujjatning o'z bob-yopish konvensiyasi bor; buzmang:

| Hujjat | Bob oxiri |
|---|---|
| `docs/patterns/` | `## N.M Amalda qo'llash` |
| `docs/testing/` | `## N.M Arxitektor nazorat ro'yxati` (`- [ ]` bandlar) |
| `docs/architect/` | `## N.M Amalda qo'llash` |
| `docs/sonarqube/` | `## N.M Amalda qo'llash` |
| `docs/clean-code/` | `## N.M Amalda qo'llash` |
| `docs/code-review/` | `## N.M Amalda qo'llash` |

Loyiha qoidasi: har bobning oxirgi `##` bo'limi `Amalda qo'llash` yoki
`Arxitektor nazorat ro'yxati` bo'ladi. `tools/check_docs.py` buni
tekshiradi: yopish bo'limi borligi yetmaydi, undan keyin boshqa `##`
bo'lim kelmaydi.

Bo'lim sarlavhasi doim raqamli H2 (`## N.M ...`) bo'ladi.
`tools/check_docs.py` yopish bo'limini shu shaklda qidiradi, indeks faqat
`## N.M` sarlavhani bo'lim deb oladi, `tools/code_gap.py` va
`tools/add_code.py` bo'lim chegarasini shu sarlavhadan topadi. H3 bo'lsa
`doc.sh show` va `find` uni ko'rmaydi.

Har bir hujjat mundarija bilan boshlanadi, havolalar GitHub anchor
formatida. Mavzu takrorlanmaydi: bir mavzu ikki hujjatda yozilmaydi,
boshqa hujjatga bob raqami bilan emas, mavzu nomi bilan havola qilinadi.

Pattern yozuvi to'rt qismdan iborat va tartibi o'zgarmaydi:

```markdown
## N.M Uzbekcha nomi (English Name)

**Tavsif:** muammo va pattern qanday ishlaydi.

**Spring'da qayerda uchraydi:** aniq sinf, annotatsiya, kutubxona.

**Qo'llanish keyslari:**
- ...

**Ehtiyot bo'ling:** tuzoqlar va qachon ishlatmaslik kerak.
```

## Kod misollari

Korpusda hozir 2300 dan ortiq kod bloki bor (ochuvchi fence qatorlari
soni bo'yicha). Ya'ni kod misoli qo'shiladi va yangi bo'lim uchun u
kutiladi.

Har pattern uchun 5-15 qatorlik blok yoziladi:
Spring'dagi tayyor variant yoki patternning eng kichik shakli. Til belgisi
snippetga mos bo'ladi (`java`, `yaml`, `sql`, `json`), hammasiga `java` deb
yozib qo'yilmaydi.

```bash
python3 tools/code_gap.py                 # hujjat bo'yicha qolgan son
python3 tools/code_gap.py patterns 17 -v  # bo'lim ro'yxati, Spring qatori bilan
python3 tools/add_code.py snippets.json   # bloklarni bo'lim oxiriga joylashtiradi
```

`add_code.py` kirishi: `{"patterns": {"17.2": "<kod>", ...}}`. Boshqa til
kerak bo'lsa qiymat `{"lang": "yaml", "code": "..."}` ko'rinishida beriladi.
Hujjat kaliti noto'g'ri bo'lsa hech narsa yozilmaydi va asbob 2 bilan
chiqadi; kodi bor va topilmagan bo'lim alohida ogohlantirish oladi.

## Yozuv uslubi

- **Em-dash ishlatilmaydi.** Faqat oddiy tire (`-`). En-dash ham yo'q.
  CI buni tekshiradi.
- Kod bloklariga til belgisi qo'yiladi: ```java, ```sql, ```bash, ```yaml,
  ```properties, ```xml. Kod bo'lmagan chiqish, log, shablon va papka
  daraxti uchun ```text.
- Kod misoli iloji boricha ko'chirib ishlatish mumkin bo'lsin: import
  shart emas, lekin sinf va metod nomi real bo'lsin.

## Havolalar

- Bob ichida: `](#anchor)`.
- Bir hujjatning boshqa bobiga: `](NN-slug.md#anchor)`.
- Boshqa hujjatga: `](../<hujjat>/README.md)` yoki aniq bobga
  `](../<hujjat>/NN-slug.md#anchor)`.
- Anchor GitHub qoidasiga ko'ra hisoblanadi: kichik harf, `'` olib
  tashlanadi, `\w`, `-` va bo'shliqdan boshqa belgi olib tashlanadi,
  bo'shliq `-` ga aylanadi.

Havolani qo'lda hisoblamang - `python3 tools/check_docs.py` ishga tushiring.

## Tekshiruv tartibi

Korpus AI tomonidan yozilgan va `docs/review.tsv` har bobning holatini
aytib turadi: `ai-draft`, `tekshirilmoqda` yoki `tekshirilgan`.
Navbat `docs/review-queue.tsv` da: agentlar eng ko'p tayanadigan
boblar oldinda.

Qoidalar:

1. **Bobni yozgan sessiya uni tekshirmaydi.** O'z ishini tekshirgan
   sessiya o'z xatosini topa olmaydi: u xuddi shu bilimdan chiqqan.
2. **Mustaqil sessiya har texnik da'voni birlamchi manbaga
   solishtiradi** va URL ni bobning `## Manbalar` bo'limiga qo'yadi.
   "Tasdiqlandi" faqat manba OCHIB KO'RILGAN bo'lsa yoziladi;
   xotiradan tasdiqlash tekshiruv emas.
3. **Odam har 10 bobdan kamida 3 tasini tanlab o'qiydi.** Tanlash
   tasodifiy bo'ladi, eng oson bob emas.
4. **`tekshirilgan` holatini faqat ODAM qo'yadi.** Sessiya ko'pi bilan
   `tekshirilmoqda` ga o'tkazadi va topilmalarini hisobotda beradi.
5. **Yangi bob faqat tekshirilgan holatda qo'shiladi.** Yangi
   `ai-draft` bob qo'shilsa, qarz o'sadi.
6. **Tuzatilgan xato `tools/known_errors.tsv` ga naqsh bo'lib
   tushadi**, aks holda u keyingi tahrirda jim qaytib keladi.

Holat o'zgargandan keyin qator ham, bob fayllari ham yangilanadi:

```bash
python3 tools/review_status.py --yoz     # bob fayllaridagi holat qatori
python3 tools/review_queue.py --yoz      # navbat
python3 tools/check_docs.py              # ikkisi mos ekanini tekshiradi
```

## Yangi bob qo'shish

1. `docs/<hujjat>/NN-slug.md` yarating, yuqoridagi shaklga rioya qiling.
2. `docs/<hujjat>/README.md` mundarijasiga qo'shing.
3. `docs/manifest.json` ga yozuv qo'shing (`num`, `title`, `file`, `part`,
   `sections`).
4. Qo'shni boblarning navigatsiya footer'ini yangilang.
5. Bobni marshrutga qo'shing: tegishli `.claude/skills/<skill>/SKILL.md`
   jadvaliga va kerak bo'lsa `tools/rules_for.py` dagi `SIGNALS` ga. Skill
   jadvalida yo'q bobni `tools/check_docs.py` xato deb chiqaradi
   (`UNROUTED_OK` istisno), `SIGNALS` ni esa hech bir tekshiruv
   ushlamaydi.
6. Bob sonini yangilang: `README.md` jadvali, `CLAUDE.md` dagi `Struktura`
   qatori va skill boshidagi `N bob, M bo'lim` qatori.
7. `python3 tools/check_docs.py` - xatosiz o'tishi shart.

## Hajm chegarasi

Hech bir markdown fayl 900 KB dan oshmasligi kerak. GitHub 1 MB dan
katta markdown ni render qilmaydi - bu real chegara, kosmetik emas.
Bob o'sib ketsa, uni ikkiga bo'ling.

## Tekshiruv

```bash
python3 tools/check_docs.py      # hajm, havola, kirill, em-dash, manifest, struktura
python3 tools/build_single.py    # monolit qayta yig'ilishini sinash
```

`check_docs.py` tekshiradi: fayl hajmi, har bir havola va anchor, kirill
harf, em-dash, kod fence juftligi va til belgisi, manifest mosligi, bob
strukturasi, bob-yopish konvensiyasi, skilllardagi havolalar, har bob
kamida bitta skill jadvalida. Xatosiz o'tishi shart.

Ikkisi CI ning `check` ishida `main` ga har push va har PR da yuradi.
`tools` ishi esa asbob testlarini, `eval_skill.py`, `eval_find.py` va
`cost_report.py` ni yurgizadi, shuning uchun bob ko'chirilsa yoki bo'lim
nomi o'zgartirilsa ham qizil berishi mumkin.

Asbob (`tools/`) o'zgartirilsa uning `tools/test_<nom>.py` si, oxirida
`eval_skill.py`, `eval_find.py` va `cost_report.py` yurgiziladi. `eval_find`
pastki chegara bilan o'lchaydi: so'rovlar tasodifiy olinadi, 100% talab
qilsa har safar qizil berib e'tibordan qolardi.

`CLAUDE.md` matni hamda skill va agent frontmatter'idagi `description`
maydoni har navbatda kontekstga kiradi. `python3 tools/cost_report.py`
byudjetdan oshsa CI qizil beradi: yangi matn qo'shishdan oldin mavjudi
qisqartiriladi. Bitta `description` 900 baytdan, skill tanasi 500 satrdan
oshmaydi (`tools/test_skill.py`).
