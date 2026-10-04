# Hissa qo'shish qoidalari

Bu repozitoriy - oltita hujjatdan iborat korpus, kod bazasi emas. Shuning
uchun asosiy qoidalar uslub va struktura haqida.

## Struktura

```
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

Metadata izohi, breadcrumb va navigatsiya footer majburiy -
`tools/check_docs.py` ularni tekshiradi.

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
| `docs/patterns/` | konvensiya yo'q (ma'lum bo'shliq, pastga qarang) |
| `docs/testing/` | `### N.M Arxitektor nazorat ro'yxati` (`- [ ]` bandlar) |
| `docs/architect/` | `### Amalda qo'llash` |
| `docs/sonarqube/` | `### Amalda qo'llash` |
| `docs/clean-code/` | `### Amalda qo'llash` |
| `docs/code-review/` | `### Amalda qo'llash` |

Loyiha qoidasi: har bob `Amalda qo'llash` yoki `Arxitektor nazorat ro'yxati`
bilan tugaydi. `docs/patterns/` ning 30 bo'limida bu ro'yxat yo'q; bob
tahrirlanganda qo'shiladi.

Pattern yozuvi to'rt qismdan iborat va tartibi o'zgarmaydi:

```markdown
### N.M Uzbekcha nomi (English Name)

**Tavsif:** muammo va pattern qanday ishlaydi.

**Spring'da qayerda uchraydi:** aniq sinf, annotatsiya, kutubxona.

**Qo'llanish keyslari:**
- ...

**Ehtiyot bo'ling:** tuzoqlar va qachon ishlatmaslik kerak.
```

## Yozuv uslubi

- **Em-dash ishlatilmaydi.** Faqat oddiy tire (`-`). En-dash ham yo'q.
  CI buni tekshiradi.
- Kod bloklariga til belgisi qo'yiladi: ```java, ```sql, ```bash, ```yaml,
  ```properties, ```xml.
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
5. `python3 tools/check_docs.py` - xatosiz o'tishi shart.

## Hajm chegarasi

Hech bir markdown fayl 900 KB dan oshmasligi kerak. GitHub 1 MB dan
katta markdown ni render qilmaydi - bu real chegara, kosmetik emas.
Bob o'sib ketsa, uni ikkiga bo'ling.

## Tekshiruv

```bash
python3 tools/check_docs.py      # hajm, havola, kirill, em-dash, manifest, struktura
python3 tools/build_single.py    # monolit qayta yig'ilishini sinash
```

Ikkisi ham CI da har push va PR da ishlaydi.
