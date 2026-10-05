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

`docs/` - yagona haqiqat manbasi. `dist/` generatsiya natijasi, git ga
kirmaydi va qo'lda tahrir qilinmaydi.

### Bob fayli shakli

```markdown
<!-- doc: patterns | chapter: 7 | part:  -->

[Hujjat nomi](../../README.md) / [Dizayn patternlar](README.md)

# 7. Bob sarlavhasi (English Title)

<details>
<summary>Bu bo'limdagi 33 bo'lim</summary>
...
</details>

Bob matni.

---

[&larr; Oldingi](06-...md) · [Mundarija](README.md) · [Keyingi &rarr;](08-...md)
```

Metadata izohi, breadcrumb, H1 va navigatsiya footer majburiy.
`tools/check_docs.py` metadata izohini, footer oxirida turishini va yopish
bo'limi borligini tekshiradi; breadcrumb va H1 hozircha qo'lda kuzatiladi.

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

Loyiha qoidasi: har bob `Amalda qo'llash` yoki `Arxitektor nazorat ro'yxati`
bilan tugaydi. `tools/check_docs.py` buni tekshiradi.

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

Hozircha kod misoli qo'shilmaydi: foydalanuvchi buni xarajat sababli
keyinga qoldirgan. Pattern qo'shilsa yoki tahrirlansa ham kod bloki
qo'shilmaydi, ish foydalanuvchi alohida so'raganda boshlanadi.

Ish qayta boshlanganda har pattern uchun 5-15 qatorlik blok yoziladi:
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

## Yangi bob qo'shish

1. `docs/<hujjat>/NN-slug.md` yarating, yuqoridagi shaklga rioya qiling.
2. `docs/<hujjat>/README.md` mundarijasiga qo'shing.
3. `docs/manifest.json` ga yozuv qo'shing (`num`, `title`, `file`, `part`,
   `sections`).
4. Qo'shni boblarning navigatsiya footer'ini yangilang.
5. Bobni marshrutga qo'shing: tegishli `.claude/skills/<skill>/SKILL.md`
   jadvaliga va kerak bo'lsa `tools/rules_for.py` dagi `SIGNALS` ga. Buni
   hech bir tekshiruv ushlamaydi: `doc.sh find` bobni indeks orqali baribir
   topadi, lekin skill jadvalida yo'q bob skill ishga tushganda
   ko'rsatilmaydi.
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
harf, em-dash, kod fence juftligi, manifest mosligi, bob strukturasi,
bob-yopish konvensiyasi, skilllardagi havolalar. Xatosiz o'tishi shart.

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
