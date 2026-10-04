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

1007 patternning hammasida kod misoli yo'q. Pattern qo'shilsa yoki
tahrirlansa, 5-15 qatorlik `java` bloki qo'shiladi: Spring'dagi tayyor
variantini yoki patternning eng kichik shaklini ko'rsatadigan misol.
Hozirgi holat `tools/check_docs.py` chiqishida ko'rinadi.

## Memory

Bu proyektning memoryasi `memory/claude-genius/` papkasida, barcha proyektlarga
tegishli bilim `memory/umumiy/` da. Ish boshida o'sha ikki `MEMORY.md` indeksi
o'qiladi, kerakli topic fayl indeksga qarab o'qiladi.

Memoryga yozish yoki uni tozalash kerak bo'lganda `memory-protocol.md` o'qiladi:
darvoza, marshrut jadvali va saqlash ketma-ketligi o'sha faylda. Ombor qoidasi
`memory/README.md` da. Bu yerda ular takrorlanmaydi.
