# Java, Spring va PostgreSQL bo'yicha oltita qo'llanma

O'zbek tilidagi oltita bir-birini to'ldiruvchi hujjat: 223 bob, 3270 bo'lim,
1955 kod misoli. Mavzular takrorlanmaydi. Har bir hujjat bir savolga javob
beradi, qolganlariga mavzu nomi bilan havola qiladi.

| Hujjat | Hajm | Qanday savolga javob beradi |
|---|---|---|
| [Dizayn patternlar](docs/patterns/README.md) | 30 bo'lim, 1007 pattern | Bu muammoga qaysi pattern to'g'ri keladi |
| [Testlash qo'llanmasi](docs/testing/README.md) | 18 bob, 239 bo'lim | Buni qanday test qilaman |
| [Arxitektor miyyasi](docs/architect/README.md) | 39 bob, 482 bo'lim | Ichkarida nima sodir bo'ladi va qanday qaror chiqaraman |
| [SonarQube](docs/sonarqube/README.md) | 43 bob, 557 bo'lim | Statik tahlil nimadan shikoyat qilyapti va qanday tuzataman |
| [Toza kod qoidalari](docs/clean-code/README.md) | 49 bob, 533 bo'lim | Klaviatura ostidagi shu qator toza yoki yo'q |
| [Kod review](docs/code-review/README.md) | 44 bob, 452 bo'lim | Diffda nimani ko'raman, nimani so'rayman, nimani to'xtataman |

Har bob alohida faylda. Bu ataylab: GitHub 1 MB dan katta markdown faylni
render qilmaydi, monolit variant brauzerda ochilmaydi.

## Qayerdan boshlash

- **Kod yozyapsiz va Sonar shikoyat qilyapti** - [xato katalogi](docs/sonarqube/README.md#vii-xato-katalogi-qanday-kod-qanday-xato-hisoblanadi)
- **Dizayn qaroriga pattern tanlayapsiz** - [patternlar mundarijasi](docs/patterns/README.md) yoki [alifbo indeksi](docs/patterns/99-alifbo-boyicha-indeks.md)
- **Test strategiyasi tuzyapsiz** - [testlash qo'llanmasining birinchi boblari](docs/testing/README.md)
- **PR ni review qilyapsiz** - [kod review hujjati](docs/code-review/README.md)
- **Shu qatorni qanday yozish kerakligini bilmoqchisiz** - [toza kod qoidalari](docs/clean-code/README.md)
- **Ichkarida nima sodir bo'layotganini bilmoqchisiz** - [arxitektor hujjati](docs/architect/README.md)
- **O'zingizni baholamoqchisiz** - [Birinchi 90 kun va o'z-o'zini baholash](docs/architect/39-birinchi-90-kun-va-oz-ozini-baholash.md)
- **Atama tushunarsiz** - [GLOSSARY.md](GLOSSARY.md)

## Claude Code bilan ishlatish

`.claude/skills/` ichida sakkizta skill bor. Repoda Claude Code ishga tushsa,
ular avtomatik ko'rinadi va kerakli bobni o'zi topib o'qiydi.

| Skill | Qachon ishga tushadi |
|---|---|
| `reja` | murakkab vazifa uchun bosqichli reja tuzish |
| `design-patterns` | pattern tanlash, refaktoring, "bu yerga qaysi pattern to'g'ri keladi" |
| `spring-testing` | test yozish, Testcontainers, flaky test, test strategiyasi |
| `sonarqube-fix` | Sonar issue tuzatish, quality gate, coverage, exclusion |
| `architect-review` | dizayn ko'rigi, chegaralar, ADR, nosozlik tahlili |
| `postgres-tuning` | sekin so'rov, indeks, EXPLAIN, vacuum, connection pool |
| `clean-code` | nomlash, funksiya uzunligi, izoh, kod hidi, refaktoring |
| `code-review` | diffni o'qish, review izohi yozish, nimani to'xtatish |

Boshqa loyihada ishlatish uchun shu repo'ni klon qilib,
`.claude/skills/*` ni o'z loyihangizning `.claude/skills/` ichiga
ko'chiring yoki `~/.claude/skills/` ga qo'ying. Skilllar `docs/` ga
havola qiladi, shuning uchun repo'ning o'zi ham qo'lda bo'lishi kerak.

## Memory

`memory/` papkasida git ichida saqlanadigan memory ombori. Proyekt memoryasi
`memory/claude-genius/`, barcha proyektlarga tegishli bilim `memory/umumiy/`
da. Qoidalar: [memory-protocol.md](memory-protocol.md) va
[memory/README.md](memory/README.md).

## Bitta fayllik variant

Offline o'qish, PDF yoki LLM kontekstiga uzatish uchun:

```bash
python3 tools/build_single.py              # oltitasi ham -> dist/
python3 tools/build_single.py patterns     # faqat bittasi
```

`dist/` git ga kirmaydi, u har safar `docs/` dan qayta yig'iladi.

## Tekshirish

```bash
python3 tools/check_docs.py
```

Fayl hajmi, har bir havola va anchor, kirill harflar, em-dash, manifest
mosligi, bob strukturasi va skilllardagi havolalar tekshiriladi. CI da har
push va PR da ishlaydi.

## Til va uslub

O'zbek lotin yozuvi. Texnik atamalar inglizcha qoldirilgan: bean, proxy,
thread, cache, latency, quality gate, coverage. Em-dash ishlatilmaydi.
To'liq qoidalar: [CONTRIBUTING.md](CONTRIBUTING.md).

## Litsenziya

Matn: [CC BY 4.0](LICENSE). Kod misollari va `tools/`: [MIT](LICENSE-CODE).
