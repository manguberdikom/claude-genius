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
<summary>Bu bobdagi 33 bo'lim</summary>
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
- [sonar-java, S109](https://raw.githubusercontent.com/SonarSource/sonar-java/8.44.0.48651/sonar-java-plugin/src/main/resources/org/sonar/l10n/java/rules/java/S109.json) - `scope: Main`
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
- **Bo'lim ichida bitta tushuncha bitta nom bilan.** Bo'limda
  "consistency" bir joyda "izchillik", boshqa joyda "konsistensiya"
  bo'lmaydi: o'quvchi ularni ikki narsa deb o'ylaydi. Sarlavhadagi
  `(English Name)` bundan mustasno.
- Imlo shakli bitta: `ssenariy`, `inyeksiya`, `obyekt`. Boshqa
  variantlarni `tools/known_errors.tsv` nasrda (`nasr` qamrovi: kod,
  sarlavha va havola chiqarib tashlanadi) ushlaydi. Sarlavhadagi eski
  shakl anchor bilan bog'langan, u alohida commitda mundarija va
  indeks bilan birga o'zgartiriladi.

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
formatida (`Havolalar` bo'limi).

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

- **Bo'lim 1-2 gap nasr bilan boshlanadi**: nima xato yoki nima
  ko'rsatilyapti va nega. Faqat koddan iborat bo'lim tushuntirishni kod
  izohiga yashiradi va telefonda o'qilmaydi.
- **Identifikatorlar inglizcha, izohlar o'zbekcha.** Sinf, metod va
  o'zgaruvchi nomi inglizcha (`OrderService`, `calculateTotal`), izoh
  va test `@DisplayName` matni o'zbekcha. `TolovService` kabi aralash
  nom clean-code nomlash qoidalariga zid namuna bo'ladi.

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

Mavzuning to'liq yozuvi bitta uy bo'limda (`docs/OWNERS.tsv`), boshqa hujjat o'z nuqtai nazarini yozadi va uyga mavzu nomi bilan havola beradi. Havola matni bob raqami emas, mavzu nomi.

- Bob ichida: `](#anchor)`.
- Bir hujjatning boshqa bobiga: `](NN-slug.md#anchor)`.
- Boshqa hujjatning bobiga: `](../<hujjat>/NN-slug.md#anchor)`.
  `](../<hujjat>/README.md)` faqat butun hujjat nazarda tutilganda
  ("patternlar hujjati"), aniq mavzu uchun emas.
- Havola yonida yalang bo'lim raqami (`(25.22)`, `13.5 da`) yozilmaydi:
  raqam renumberda jim eskiradi va qaysi hujjatniki ekani noaniq.
- Uy-bobdan tashqaridagi mavzu bo'limi (`docs/OWNERS.tsv`) uy bo'limga
  havola beradi; shunda `check_docs` ogohlantirmaydi.
- Anchor GitHub qoidasiga ko'ra hisoblanadi: kichik harf, `'` olib
  tashlanadi, `\w`, `-` va bo'shliqdan boshqa belgi olib tashlanadi,
  bo'shliq `-` ga aylanadi.

Havolani qo'lda hisoblamang: `tools/doc.sh path <hujjat> <raqam>` tayyor
anchor beradi, `python3 tools/check_docs.py` esa har havolani tekshiradi.
Bob tanasidagi `](../<hujjat>/README.md)` havolalari soni
`README_LINK_BASE` dan oshsa `check_docs` xato beradi (ratchet): eski
havolalar bob tekshiruvi paytida aniq anchorga aylantiriladi va chegara
pasaytiriladi.

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
7. **Manba tag yoki commit SHA ga qadaladi.** `main`, `master` va
   `trunk` dagi fayl o'zgaradi yoki ko'chadi, versiya da'vosi esa aniq
   versiyaga tegishli. Masalan
   `raw.githubusercontent.com/spring-projects/spring-boot/v4.0.0/...`,
   Maven Central dagi pom va sources jar ham birlamchi manba.

Da'vo turi bo'yicha kim tekshiradi. Uch qatlam bor: mashina har
commitda yuradi, agent faqat mashina hal qilmagan da'voni oladi, odam
esa mashina ham, agent ham ishonchli hal qila olmaydigan da'voni ko'radi.

| Da'vo turi | Kim | Qanday |
|---|---|---|
| Havola, anchor, bo'lim soni, bob shakli | mashina | `tools/check_docs.py` |
| `java:S` kaliti mavjudligi, turi va darajasi | mashina | `tools/check_docs.py` va `tools/sonar_rules.tsv` |
| Avval tuzatilgan xatoning qaytishi | mashina | `tools/known_errors.tsv` |
| Sozlama kaliti, annotatsiya, FQN, Maven koordinata, API mavjudligi | agent (mashina tekshiruvi tayyor bo'lguncha) | tagga qadalgan manba kodi yoki Maven Central |
| Versiya da'vosi ("7.0 da keldi") va default qiymat | agent | tagdagi manba kodi, changelog |
| Empirik taqqoslash ("2-4 barobar tez", "15 foiz yo'qotish", "G1 ga nisbatan") | agent, keyin odam | manba yoki `o'lchanmagan taxmin`; `python3 tools/claims_report.py --empirik` |
| Xulq da'vosi (`readOnly` nima qiladi, `ScopedValue` merosi), dialektga bog'liq default | odam | manbani o'qib, kerak bo'lsa sinab ko'rib |
| Sonar kaliti matndagi ma'noga mosmi | odam | qoida tavsifini o'qib |
| Maslahat to'g'ri va o'quvchiga tushunarlimi | odam | tasodifiy bo'lim namunasi, bobga 20 daqiqa |

Navbatni har qatlam o'z holati bo'yicha oladi:

```bash
python3 tools/review_queue.py --holat ai-draft         # agent: hali tekshirilmagan bob
python3 tools/review_queue.py --holat tekshirilmoqda   # odam: imzo kutayotgan bob
```

Haftalik maqsad: 15-20 bob agent tekshiruvidan o'tadi (`tekshirilmoqda`),
5 bob odam imzosini oladi (`tekshirilgan`). O'lchov `docs/review.tsv`
dagi holat soni va README dagi holat qatori.

`tools/check_docs.py` `docs/review.tsv` ni qat'iy tekshiradi: holat
`ai-draft` bo'lmasa `sana` va `tekshiruvchi` bo'sh emas, `manbalar`
bobdagi `## Manbalar` ro'yxati soniga teng, `tekshirilgan` bobda kamida
bitta manba bor. `tekshirilgan` qatorini oxirgi o'zgartirgan commit
Claude nomidan bo'lsa yoki `Co-Authored-By: Claude` qatori bo'lsa xato
(git tarixi bo'lmasa bu tekshiruv o'tkaziladi, sayoz klonda
ogohlantirish beradi). `## Manbalar` dagi `main`, `master` yoki `trunk`
havolasi ogohlantirish oladi.

Holat o'zgargandan keyin qator ham, bob fayllari ham yangilanadi:

```bash
python3 tools/review_status.py --yoz     # bob va README lardagi holat qatori
python3 tools/review_queue.py --yoz      # navbat
python3 tools/check_docs.py              # hammasi mos ekanini tekshiradi
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

## Ish tartibi

Bu qoidalar hamma ishga tegishli, ham korpusga, ham asboblarga.

1. **Sof asbob soni o'smaydi.** Yangi asbob faqat mavjudini almashtirsa
   yoki uning subbuyrug'i bo'lsa qo'shiladi. Avval savol: bu mavjud
   asbobning subbuyrug'i bo'la oladimi?
2. **Branch, PR va yashil CI.** `main` ga to'g'ridan-to'g'ri push yo'q.
   Push dan keyin CI natijasi kutiladi, qizil holda keyingi ishga
   o'tilmaydi.
3. **A/B tugaguncha muzlatish.** `manguberdi` skilli, `budget.py`,
   `guruh.py` va `check_code.py` dagi zanjir shartiga faqat xato
   tuzatish kiradi.
4. **Mustaqil tekshiruv.** 200 satrdan katta asbob o'zgarishi `review`
   aktyoridan o'tadi. Tashqi chiqishni o'qiydigan asbob (test logi,
   build chiqishi, Java manbasi) sintetik emas, haqiqiy fixture bilan
   sinaladi.
5. **Commit bitta asbob yoki qaror.** Kod, uning testi va hujjati bitta
   commitda, `docs/` mazmuni alohida commitda.
6. **Korpus ulushi.** Har ish kunida vaqtning kamida yarmi korpus
   tekshiruviga beriladi ("Tekshiruv tartibi" bo'limi).

### Windows saboqlari

Asosiy foydalanuvchi Windows da, Claude Code ning Git Bash ida ishlaydi.
Quyidagilar bir necha marta qaytgan, asbob o'zgarsa ular tekshiriladi:

- **Yo'l ajratgich.** `os.path` Windows da `\` beradi. Kalit, indeks va
  havola uchun yo'l `/` ga keltiriladi, solishtirishda ikkala tomon bir
  xil shaklda bo'ladi.
- **BOM siz UTF-8.** PowerShell 5.1 fayl va pipe ga BOM yozadi, stdin esa
  ANSI kod sahifasida o'qiladi. JSON va stdin `utf-8-sig` bilan
  o'qiladi, `settings.json` BOM siz yoziladi.
- **SIGPIPE yo'q.** `| head` yopgan quvurga yozish Windows da signal
  emas, `OSError` (EINVAL) traceback beradi. Chiqish yozadigan asbob uni
  ushlaydi.
- **8.3 qisqa nom va realpath.** Temp papka `RUNNER~1` kabi qisqa nom
  bilan keladi, git esa uzun nom beradi. Yo'l solishtirish yoki kalit
  qilishdan oldin ikkala tomon `os.path.realpath` dan o'tadi. Linux da
  shu holat symlink bilan sinaladi.
- **Linux CI yashilligi yetmaydi.** `tools (windows-latest)` ham yashil
  bo'lishi kerak. Agent sessiyasi Windows ni ko'rmaydi, shuning uchun
  yo'l, kodirovka yoki jarayon bilan ishlaydigan o'zgarishda Windows
  natijasi kutiladi.
