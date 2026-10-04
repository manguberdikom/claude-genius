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

Korpus ~2.1M token, eng katta bob ~68k, bitta bo'lim esa ~700. Shuning
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

- 1200 satrdan uzun faylni chegarasiz o'qish `tools/guard.py` tomonidan
  to'siladi. Havolani qo'lda yozmang, `doc.sh path` tayyor anchor beradi.
- Indeks `index/` da, hosila. Bob yangiroq bo'lsa `doc.sh` o'zi qayta
  yasaydi. Indeks grep qilinadi, kontekstga olinmaydi.
- O'lchov: `eval_find.py` (qidiruv o'rni), `test_suggest.py` (taklif
  chegaralari), `cost_report.py` (har navbatdagi kontekst).

## Arzon yo'ldan borish

Javob ko'pincha kodning yoki chiqishning o'zida. Qimmat yo'l natijani
yaxshilamasa, u shunchaki pul va vaqt.

| Kerak bo'lsa | Arzon yo'l |
|---|---|
| Baza tuzilishi | `python3 tools/schema_from_entities.py <src>` |
| Test nega yiqildi | chiqishdagi birinchi xatoni o'qish |
| Qoida nima deydi | `tools/doc.sh show <hujjat> <raqam>` |
| Diff to'g'rimi | `review` agenti, keyin maqsadli test |

`docker up/run/build/pull` va bazaga ulanish `tools/guard.py` tomonidan
to'siladi. Haqiqatan kerak bo'lsa buyruq oldiga `COST_OK=1` qo'yiladi va
sababi aytiladi. `docker ps`, `docker logs` to'silmaydi.

Og'ir o'qishni arzon modelga bering: `qidiruv` va `tahlil` (haiku) ko'p
o'qib oz qaytaradi, `review` (sonnet) diffni qoidaga solishtiradi. Uzun
chiqish ularning kontekstida qoladi. Qaror va yozish asosiy sessiyada.

Boshqa asboblar:

- `doc.sh rule java:S3776` - Sonar kalitini izohlagan bo'lim.
- `doc.sh checklist <hujjat> [bob]` - yozilgan tekshiruv punktlari.
- `parse_test_output.py` - test chiqishidan birinchi haqiqiy sababni oladi.
- `check_code.py` - Java fayl yozilgandan keyin `PostToolUse` hook sifatida
  mexanik qoidalarni tekshiradi va buzilganini bo'lim raqami bilan
  qaytaradi. Faqat yolg'on ishga tushishi nol bo'lgan tekshiruvlar.

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

1007 patternning 528 tasida kod misoli bor, 479 tasida yo'q. 1-15
bo'limlar tugatilgan, 16-30 bo'limlar qolgan.

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
