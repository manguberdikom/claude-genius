# Loyiha ko'rsatmalari

## Til va uslub

- Javob va hujjatlar o'zbek lotin yozuvida. Kirill yoki rus tili bo'lmaydi.
- Texnik atamalar inglizcha qoladi: bean, proxy, thread, cache, latency,
  quality gate, coverage. To'liq ro'yxat `GLOSSARY.md` da.
- Javob birinchi qatorida natija turadi, keyin tafsilot. Em-dash va en-dash
  ishlatilmaydi.

## Struktura

Oltita hujjat `docs/<hujjat>/` da, bob `NN-slug.md` faylida, boblar
ro'yxati `docs/manifest.json`; kalitlar va bob sonlari `tools/doc.sh toc`
da. `dist/` hosila (`tools/build_single.py`), qo'lda tahrir qilinmaydi.

## Qidirish va o'qish

Bob ~200 KB gacha, bo'lim ~2 KB: bob butunligicha emas, bo'lim
darajasida o'qiladi.

```bash
tools/doc.sh find "circuit breaker"  # sarlavha va inglizcha taxalluslar
tools/doc.sh find -f "pg_stat_statements"  # matn ichidan ham
tools/doc.sh show patterns 17.2  # faqat o'sha bo'lim
tools/doc.sh outline sonarqube 29  # bobdagi bo'limlar
tools/doc.sh path patterns 17.2  # fayl, satr oralig'i, anchor
tools/doc.sh toc  # hujjat kalitlari
```

`tools/suggest_sections.py` har so'rovda kontekstga nomzod bo'lim
raqamlarini qo'shadi. Nomzod tartibi ishonchli emas: javob nomzodga emas,
`show` bilan o'qilgan matnga tayanadi, mos kelmasa shuni ayting. Nomzod
yo'qligi mavzu yo'q degani emas, `find` bilan qidiring.

- `guard.py` 16 KB dan katta bo'lakni o'qishni to'sadi. Havolani qo'lda
  yozmang, `doc.sh path` tayyor anchor beradi.
- Indeks `index/` hosila: `doc.sh` o'zi yangilaydi, u grep qilinadi,
  kontekstga olinmaydi.
- Bob holati `docs/review.tsv` da. `ai-draft` bob AI yozgan va inson
  tekshirmagan: unga tayangan javobda shu aytiladi. `doc.sh show` va
  `rules_for` holatni o'zi ko'rsatadi.

## Orkestrator

Java/Spring ishi uchun foydalanuvchi `/manguberdi` ni chaqiradi. Qoidalar,
aktyor modellari va asboblar katalogi `.claude/skills/manguberdi/` da.
Og'ir o'qish `qidiruv` va `tahlil` subagentida, asosiy sessiyada qaror,
marshrut va hujjat tahriri.

## Arzon yo'ldan borish

Javob ko'pincha kodda yoki chiqishda; natijani yaxshilamagan qimmat yo'l
faqat pul va vaqt.

| Kerak bo'lsa | Arzon yo'l |
|---|---|
| Baza tuzilishi | `python3 tools/schema_from_entities.py <src>` |
| O'zgarish testlari | `python3 tools/run_tests.py --diff --yurgiz` |
| Test nega yiqildi | chiqishdagi birinchi xatoni o'qish |
| Qoida nima deydi | `tools/doc.sh show <hujjat> <raqam>` |
| Diff to'g'rimi | `manguberdi` faol bo'lsa `review` aktyori, aks holda `code-review` skilli |

`guard.py` docker, bazaga ulanish, `flyway:clean` va PowerShell ni
so'raydi (`ask`, subagentda `deny`), katta bob, xom to'liq suite va
`.java` ga Bash bilan yozishni to'sadi
(`.claude/skills/manguberdi/references/taqiq.md`).

`tools/rules_for.py` Java yozishdan OLDIN majburiy (tegishli boblar,
tekshiruv punktlari, avvalgi xatolar), `check_code.py` hooki buni talab
qiladi.

## Hujjat yoki asbob o'zgarsa

`docs/` tahririda `CONTRIBUTING.md` amal qiladi: bob shakli, pattern yozuvi
va kod misoli tartibi, 900 KB chegara, havolalar. Mavzuning to'liq yozuvi bitta uy bo'limda (`docs/OWNERS.tsv`), boshqa hujjat o'z nuqtai nazarini yozadi va uyga mavzu nomi bilan havola beradi.
Keyin `python3 tools/check_docs.py` xatosiz o'tishi shart, CI ham
shuni ishlatadi. Asbob o'zgarsa uning `tools/test_<nom>.py` si, keyin
`eval_skill.py`, `eval_find.py` va `cost_report.py`.

## Memory

Ish boshida `memory/claude-genius/MEMORY.md` (shu proyekt) va
`memory/umumiy/MEMORY.md` (hamma proyekt) indekslari o'qiladi, topic
fayl indeksga qarab. Yozish va tozalash qoidasi `memory/README.md` da.
