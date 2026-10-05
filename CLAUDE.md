# Loyiha ko'rsatmalari

## Til va uslub

- Javob va hujjatlar o'zbek lotin yozuvida. Kirill yoki rus tili bo'lmaydi.
- Texnik atamalar inglizcha qoladi: bean, proxy, thread, cache, latency,
  quality gate, coverage. To'liq ro'yxat `GLOSSARY.md` da.
- Javob birinchi qatorida natija turadi, keyin tafsilot. Em-dash va en-dash
  ishlatilmaydi.

## Struktura

Oltita hujjat, har biri `docs/<hujjat>/` papkasida, har bob alohida faylda:
`patterns` (31 bob), `testing` (18 bob), `architect` (39 bob),
`sonarqube` (43 bob), `clean-code` (49 bob), `code-review` (44 bob).

- `docs/<hujjat>/README.md` - mundarija va kirish.
- `docs/<hujjat>/NN-slug.md` - bitta bob. Shakli `CONTRIBUTING.md` da.
- `docs/manifest.json` - boblar ro'yxati. Bob qo'shilsa yoki o'chirilsa
  yangilanadi, aks holda tekshiruv xato beradi.
- `dist/` - `tools/build_single.py` natijasi. Git da yo'q, qo'lda tahrir
  qilinmaydi.
- `.claude/skills/` - `docs/` ga marshrutlovchi skilllar va `manguberdi`
  orkestrator.

`docs/` - `dist/` ning manbasi. Bitta fayllik variant kerak bo'lsa
`python3 tools/build_single.py` ishga tushiriladi.

## Qidirish va o'qish

Korpus ~6.4 MB, eng katta bob ~200 KB, bitta bo'lim esa ~2 KB. Shuning
uchun bob butunligicha emas, bo'lim darajasida o'qiladi.

```bash
tools/doc.sh find "circuit breaker"   # sarlavha va inglizcha taxalluslar
tools/doc.sh find -f "pg_stat_statements"  # matn ichidan ham
tools/doc.sh show patterns 17.2       # faqat o'sha bo'lim
tools/doc.sh outline sonarqube 29     # bobdagi bo'limlar
tools/doc.sh path patterns 17.2       # fayl, satr oralig'i, anchor
tools/doc.sh toc                      # hujjat kalitlari
```

`tools/suggest_sections.py` har so'rovda avtomatik ishlaydi va mos bo'lim
raqamlarini kontekstga qo'shadi, ya'ni `find` chaqirilmasa ham kerakli
joy ko'rsatiladi. Taklif chiqqan bo'lsa javob unga tayanadi: `show` bilan
o'qing yoki nega mos emasligini ayting. Taklif yo'qligi mavzu yo'q degani
emas, `find` bilan qidiring.

- 16 KB dan katta bo'lakni o'qish `tools/guard.py` tomonidan
  to'siladi. Havolani qo'lda yozmang, `doc.sh path` tayyor anchor beradi.
- Indeks `index/` da, hosila. Bob yangiroq bo'lsa `doc.sh` o'zi qayta
  yasaydi. Indeks grep qilinadi, kontekstga olinmaydi.
- Bob holati `docs/review.tsv` da. `ai-draft` bob AI yozgan va inson
  tekshirmagan: unga tayangan javobda shu aytiladi. `doc.sh show` va
  `rules_for` holatni o'zi ko'rsatadi.

## Orkestrator

Java/Spring ishi uchun `/manguberdi` sessiyada bir marta chaqiriladi: u promptni
normallashtiradi, aktyor tanlaydi (`rejalashtiruvchi`, `dasturchi`,
`test-muhandis`, `review`), ularni ketma-ket yurgizadi va oxirida
memoryga yozadi. Qoidalar `.claude/skills/manguberdi/` da.

## Arzon yo'ldan borish

Javob ko'pincha kodning yoki chiqishning o'zida. Qimmat yo'l natijani
yaxshilamasa, u shunchaki pul va vaqt.

| Kerak bo'lsa | Arzon yo'l |
|---|---|
| Baza tuzilishi | `python3 tools/schema_from_entities.py <src>` |
| O'zgarish testlari | `python3 tools/run_tests.py --diff --yurgiz` |
| Test nega yiqildi | chiqishdagi birinchi xatoni o'qish |
| Qoida nima deydi | `tools/doc.sh show <hujjat> <raqam>` |
| Diff to'g'rimi | `review` agenti, keyin maqsadli test |

`docker up/run/build/pull/start` (compose bilan ham), bazaga ulanish va
PowerShell `guard.py` tomonidan foydalanuvchi qaroriga qo'yiladi (`ask`):
o'z-o'zidan yurgizilmaydi, nega arzon yo'l yetmagani aytib so'raladi.
`docker ps`, `docker logs`, `psql --version` so'ralmaydi. Katta bobni
butun o'qish va xom to'liq test suite esa to'siladi (`deny`).

Og'ir o'qish `qidiruv` va `tahlil` (haiku) da, diffni `review` (sonnet)
tekshiradi, kod va testni `dasturchi` va `test-muhandis` (sonnet) yozadi.
Uzun chiqish ularning kontekstida qoladi. Asosiy sessiyada qaror, marshrut
va hujjat tahriri.

Boshqa asboblar:

- `doc.sh rule java:S3776` - Sonar kalitini izohlagan bo'lim.
- `doc.sh checklist <hujjat> [bob]` - yozilgan tekshiruv punktlari.
- `parse_test_output.py` - test chiqishidan birinchi haqiqiy sababni oladi.
- `run_tests.py` - ta'sirlangan testlarni modul bilan yurgizadi;
  `--hammasi` partiyada bir marta, `--tashxis` suite nega sekin.
- `guruh.py` - parallel guruh uchun git worktree va birlashtirish.
- `rules_for.py` - tegilayotgan fayllarga qaysi boblar, tekshiruv
  punktlari va avvalgi xatolar tegishli. Java yozishdan OLDIN majburiy.
- `check_code.py` - Java fayl yozilgandan keyin `PostToolUse` hook
  sifatida mexanik qoidalarni tekshiradi va `rules_for` chaqirilganini
  talab qiladi. Faqat yolg'on ishga tushishi nol bo'lgan tekshiruvlar.
- `budget.py`, `handoff.py`, `usage.py` - aktyor budjeti, kontekst uzatish
  va token sarfi. Batafsil `manguberdi` skillida.

## Hujjat yoki asbob o'zgarsa

`docs/` tahririda `CONTRIBUTING.md` amal qiladi: bob shakli, pattern yozuvi
va kod misoli tartibi, 900 KB chegara, havolalar. Mavzu ikki hujjatda
yozilmaydi, boshqa hujjatga bob raqami bilan emas, mavzu nomi bilan havola
qilinadi. Keyin `python3 tools/check_docs.py` xatosiz o'tishi shart, CI ham
shuni ishlatadi. Asbob o'zgarsa uning `tools/test_<nom>.py` si, keyin
`eval_skill.py`, `eval_find.py` va `cost_report.py`.

## Memory

Bu proyektning memoryasi `memory/claude-genius/` papkasida, barcha proyektlarga
tegishli bilim `memory/umumiy/` da. Ish boshida o'sha ikki `MEMORY.md` indeksi
o'qiladi, kerakli topic fayl indeksga qarab o'qiladi.

Memoryga yozish yoki uni tozalash kerak bo'lganda `memory/README.md`
o'qiladi: darvoza, format va ketma-ketlik o'sha faylda. Bu yerda
takrorlanmaydi.
