# Loyiha ko'rsatmalari

## Til va uslub

- Javob va hujjatlar o'zbek lotin yozuvida. Kirill yoki rus tili bo'lmaydi.
- Texnik atamalar inglizcha qoladi: bean, proxy, thread, cache, latency,
  quality gate, coverage. To'liq ro'yxat `GLOSSARY.md` da.
- Javob birinchi qatorida natija turadi, keyin tafsilot. Em-dash ishlatilmaydi.

## Hujjat konvensiyasi

- Har bir hujjat mundarija bilan boshlanadi, havolalar GitHub anchor formatida.
- Har bob `Amalda qo'llash` yoki `Arxitektor nazorat ro'yxati` ro'yxati bilan
  tugaydi.
- Mavzu takrorlanmaydi: boshqa hujjatga bob raqami bilan emas, mavzu nomi bilan
  havola qilinadi.

## Struktura

Oltita hujjat, har biri `docs/<hujjat>/` papkasida, har bob alohida faylda:
`patterns` (30 bob, 1007 pattern), `testing` (18 bob), `architect` (39 bob),
`sonarqube` (43 bob), `clean-code` (49 bob), `code-review` (44 bob).

- `docs/<hujjat>/README.md` - mundarija va kirish.
- `docs/<hujjat>/NN-slug.md` - bitta bob. Shakli `CONTRIBUTING.md` da.
- `docs/manifest.json` - boblar ro'yxati. Bob qo'shilsa yoki o'chirilsa
  yangilanadi, aks holda tekshiruv xato beradi.
- `dist/` - `tools/build_single.py` natijasi. Git da yo'q, qo'lda tahrir
  qilinmaydi.
- `.claude/skills/` - sakkizta skill, `docs/` ga marshrutlash jadvallari.

`docs/` yagona haqiqat manbasi. Bitta fayllik variant kerak bo'lsa
`python3 tools/build_single.py` ishga tushiriladi.

## Qidirish va o'qish

Korpus 5.9 MB, ~2.1M token. Eng katta bob ~68k token, bitta bo'lim esa
o'rtacha ~700 token. Shuning uchun bob fayli butunligicha emas, bo'lim
darajasida o'qiladi. Hammasi `tools/doc.sh` orqali:

```bash
tools/doc.sh find "circuit breaker"       # sarlavha va inglizcha taxalluslar
tools/doc.sh find -f "pg_stat_statements" # matn ichidan ham, ~60 ms
tools/doc.sh show patterns 17.2           # faqat o'sha bo'limni chiqaradi
tools/doc.sh outline sonarqube 29         # bobdagi bo'limlar
tools/doc.sh path patterns 17.2           # fayl, satr oralig'i va anchor
```

Odatiy yo'l ikki qadam: `find` bo'lim raqamini beradi, `show` matnni beradi.
Hujjat kalitlari `doc.sh toc` da.

Buning ustiga `tools/suggest_sections.py` har bir so'rovda avtomatik
ishlaydi (`UserPromptSubmit` hook) va mos bo'lim raqamlarini kontekstga
qo'shadi. Ya'ni kerakli joy `find` chaqirilmasa ham ko'rsatiladi. Taklif
chiqqan bo'lsa, javob o'sha bo'limlarga tayanishi kerak: ularni `show`
bilan o'qing yoki nega mos emasligini ayting. Taklif chiqmasligi mavzu
yo'q degani emas, `find` bilan qidirib ko'ring.

Qoidalar:

- `cat`, `less` yoki chegarasiz `Read` bilan 1200 satrdan uzun bob fayli
  o'qilmaydi. Buni `tools/guard_bigdocs.py` PreToolUse hook sifatida to'sadi
  (`.claude/settings.json`), sinovlari `tools/test_guard.py` da.
- Havolani qo'lda yozmang: `doc.sh path` tayyor anchor beradi, u
  `check_docs.py` ishlatadigan slug bilan bir xil hisoblanadi.
- Indeks `index/` da, uni `tools/build_index.py` `docs/manifest.json` dan
  yasaydi. Bob fayli indeksdan yangiroq bo'lsa `doc.sh` o'zi qayta yasaydi,
  shuning uchun tahrirdan keyin qo'lda hech narsa qilish shart emas.
- Indeks grep qilinadi, o'qilmaydi. Uni ham kontekstga to'liq olmang.
- Qidiruv sifati o'lchanadi: `python3 tools/eval_find.py`. U bo'limni
  topish emas, nechanchi o'rinda chiqishini o'lchaydi. `find` mantig'i yoki
  indeks o'zgarsa, pasayish shu yerda ko'rinadi.
- Avtomatik taklifning chegaralari `python3 tools/test_suggest.py` da
  sinaladi: mavzuli so'rovga taklif chiqishi, mavzusiziga jim turishi
  shart. Chegara qiymatlari o'sha ro'yxatda sozlangan, ko'z bilan emas.

## Arzon yo'ldan borish

Javob ko'pincha kodning yoki chiqishning o'zida turadi. Qimmat yo'l
natijani yaxshilamasa, u shunchaki pul va vaqt.

| Kerak bo'lsa | Qimmat yo'l | Arzon yo'l |
|---|---|---|
| Baza tuzilishi | konteyner, ulanish, `\d+` | `python3 tools/schema_from_entities.py <src>` |
| Test nega yiqildi | qayta ishga tushirish | chiqishdagi birinchi xatoni o'qish |
| Qoida nima deydi | bobni to'liq o'qish | `tools/doc.sh show <hujjat> <raqam>` |
| Diff to'g'rimi | hammasini qurib ko'rish | `review` agenti, keyin maqsadli test |

`docker up/run/build/pull` va bazaga ulanish `tools/guard.py` tomonidan
to'siladi. Yo'l yopiq emas: haqiqatan kerak bo'lsa buyruq oldiga
`COST_OK=1` qo'yiladi va nega arzon yo'l yetmagani aytiladi. `docker ps`,
`docker logs` kabi tashxis buyruqlari arzon, ular to'silmaydi.

Og'ir o'qishni arzon modelga bering. `.claude/agents/` da uchta agent bor:

- `qidiruv` (haiku) - bir nechta bo'limni o'qib, qisqa parcha qaytaradi.
- `tahlil` (haiku) - asbobni yurgizib, uzun chiqishdan topilmani ajratadi.
- `review` (sonnet) - diffni qoidaga solishtiradi.

Qoida: **ko'p o'qib oz qaytaradigan ish** agentga boradi, chunki uzun
chiqish uning kontekstida qoladi. Qaror va yozish asosiy sessiyada
qoladi.

## Tekshiruv

Hujjat o'zgartirilgandan keyin:

```bash
python3 tools/check_docs.py
```

Tekshiradi: fayl hajmi, har bir havola va anchor, kirill harf, em-dash, kod
fence juftligi, manifest mosligi, bob strukturasi, bob-yopish konvensiyasi,
skilllardagi havolalar.
Xatosiz o'tishi shart. CI ham shuni ishlatadi.

## Qattiq qoidalar

1. **Fayl 900 KB dan oshmaydi.** GitHub 1 MB dan katta markdown ni render
   qilmaydi. Bob o'sib ketsa ikkiga bo'linadi.
2. **Havolani qo'lda hisoblamang** - `tools/check_docs.py` ishlatilsin.
3. **Bob fayl shakli buzilmaydi**: metadata izohi, breadcrumb, H1, kontent,
   navigatsiya footer.
4. **Mavzular takrorlanmaydi.** Bir mavzu ikki hujjatda yozilmaydi, havola
   qilinadi.

## Pattern yozuvi shakli

`docs/patterns/` dagi har yozuv to'rt qismdan iborat, tartibi o'zgarmaydi:
`**Tavsif:**`, `**Spring'da qayerda uchraydi:**`, `**Qo'llanish keyslari:**`,
`**Ehtiyot bo'ling:**`.

## Ma'lum bo'shliq

1007 patternning 498 tasida kod misoli bor, 509 tasida yo'q. 1-14
bo'limlar tugatilgan, 15-30 bo'limlar qolgan.

Pattern qo'shilsa yoki tahrirlansa, 5-15 qatorlik kod bloki qo'shiladi:
Spring'dagi tayyor variantini yoki patternning eng kichik shaklini
ko'rsatadigan misol. Til snippet'ga mos bo'lsin (`java`, `yaml`, `sql`,
`json`), `java` deb yozib qo'yilmasin.

Holatni ko'rish va ish qo'shish:

```bash
python3 tools/code_gap.py                 # hujjat bo'yicha qolgan son
python3 tools/code_gap.py patterns 17 -v  # bo'lim ro'yxati, Spring qatori bilan
python3 tools/add_code.py snippets.json   # bloklarni bo'lim oxiriga joylashtiradi
```

`add_code.py` kirishi: `{"patterns": {"17.2": "<kod>", ...}}`. Boshqa til
kerak bo'lsa qiymat `{"lang": "yaml", "code": "..."}` ko'rinishida beriladi.

## Memory

Bu proyektning memoryasi `memory/claude-genius/` papkasida, barcha proyektlarga
tegishli bilim `memory/umumiy/` da. Ish boshida o'sha ikki `MEMORY.md` indeksi
o'qiladi, kerakli topic fayl indeksga qarab o'qiladi.

Memoryga yozish yoki uni tozalash kerak bo'lganda `memory-protocol.md` o'qiladi:
darvoza, marshrut jadvali va saqlash ketma-ketligi o'sha faylda. Ombor qoidasi
`memory/README.md` da. Bu yerda ular takrorlanmaydi.
