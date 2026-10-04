# claude-genius

Java, Spring va PostgreSQL bo'yicha o'zbek tilidagi to'rtta hujjat korpusi.
Bu kod bazasi emas - kompilyatsiya, test yoki ishga tushirish yo'q.

## Struktura

- `docs/<hujjat>/` - har bob alohida fayl. **Yagona haqiqat manbasi.**
- `docs/manifest.json` - boblar ro'yxati. Bob qo'shilsa/o'chirilsa yangilanadi.
- `dist/` - `tools/build_single.py` natijasi. Git da yo'q, qo'lda tahrir qilinmaydi.
- `tools/` - `build_single.py` (monolit yig'ish), `check_docs.py` (tekshiruv).
- `.claude/skills/` - beshta skill, `docs/` ga marshrutlash jadvallari.

To'rtta hujjat: `patterns` (1007 pattern), `testing` (18 bob),
`architect` (39 bob), `sonarqube` (43 bob).

## Har o'zgarishdan keyin

```bash
python3 tools/check_docs.py
```

Hajm, havola, anchor, kirill, manifest va bob strukturasini tekshiradi.
Xatosiz o'tishi shart - CI ham shuni ishlatadi.

## Qattiq qoidalar

1. **Kirill yo'q.** O'zbek lotin yozuvi. CI buni tekshiradi.
2. **Fayl 900 KB dan oshmaydi.** GitHub 1 MB dan katta markdown ni render
   qilmaydi. Bob o'sib ketsa ikkiga bo'linadi.
3. **Texnik atamalar inglizcha qoladi.** Ro'yxat `GLOSSARY.md` da. Yangi
   atama tarjima qilinsa, lug'atga qo'shiladi.
4. **Havolani qo'lda hisoblamang** - `tools/check_docs.py` ishlatilsin.
5. **Bob fayl shakli buzilmaydi**: metadata izohi, breadcrumb, H1, kontent,
   navigatsiya footer. Batafsil: `CONTRIBUTING.md`.
6. **Mavzular takrorlanmaydi.** Pattern katalogi `patterns` da, testlash
   `testing` da, mexanika `architect` da, statik tahlil `sonarqube` da.
   Bir mavzu ikki hujjatda yozilmaydi - havola qilinadi.
7. **Bob-yopish konvensiyasi hujjatga bog'liq**: `architect` va `sonarqube`
   `### Amalda qo'llash` bilan, `testing` `### N.M Arxitektor nazorat
   ro'yxati` bilan tugaydi, `patterns` da konvensiya yo'q.

## Pattern yozuvi shakli

`docs/patterns/` dagi har yozuv to'rt qismdan iborat, tartibi o'zgarmaydi:
`**Tavsif:**`, `**Spring'da qayerda uchraydi:**`, `**Qo'llanish keyslari:**`,
`**Ehtiyot bo'ling:**`.

## Ma'lum bo'shliq

1007 patternning 146 tasida kod misoli bor, 861 tasida yo'q. Pattern
qo'shilsa yoki tahrirlansa, imkon bo'lsa qisqa `java` bloki qo'shiladi -
Spring'dagi tayyor variantini ko'rsatadigan 5-15 qatorlik misol.
