# Java, Spring va PostgreSQL bo'yicha oltita qo'llanma

O'zbek tilidagi oltita bir-birini to'ldiruvchi hujjat: 223 bob, 3293 bo'lim,
2300 dan ortiq kod misoli. Mavzular takrorlanmaydi. Har bir hujjat bir
savolga javob beradi, qolganlariga mavzu nomi bilan havola qiladi.

| Hujjat | Hajm | Qanday savolga javob beradi |
|---|---|---|
| [Dizayn patternlar](docs/patterns/README.md) | 30 bo'lim, 1007 yozuv (996 noyob pattern) | Bu muammoga qaysi pattern to'g'ri keladi |
| [Testlash qo'llanmasi](docs/testing/README.md) | 18 bob, 239 bo'lim | Buni qanday test qilaman |
| [Arxitektor miyyasi](docs/architect/README.md) | 39 bob, 482 bo'lim | Ichkarida nima sodir bo'ladi va qanday qaror chiqaraman |
| [SonarQube](docs/sonarqube/README.md) | 43 bob, 557 bo'lim | Statik tahlil nimadan shikoyat qilyapti va qanday tuzataman |
| [Toza kod qoidalari](docs/clean-code/README.md) | 49 bob, 533 bo'lim | Klaviatura ostidagi shu qator toza yoki yo'q |
| [Kod review](docs/code-review/README.md) | 44 bob, 445 bo'lim | Diffda nimani ko'raman, nimani so'rayman, nimani to'xtataman |

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

`.claude/skills/` ichida to'qqizta skill bor: sakkiztasi qo'llanmaga marshrut,
`manguberdi` esa orkestrator. Repoda Claude Code ishga tushsa, sakkiztasi
avtomatik ko'rinadi va kerakli bobni o'zi topib o'qiydi, `manguberdi` esa
sessiyada bir marta `/manguberdi` bilan chaqiriladi. U `.claude/agents/`
dagi olti aktyorni yurgizadi.

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
| `manguberdi` | katta ish: aktyor tanlab reja, kod, test va review ni ketma-ket yurgizadi, oxirida memoryga yozadi |

Hooklar `.claude/settings.json` da turadi va repoda o'zi ishlaydi: har
so'rovga mos bo'lim taklif qilinadi (`suggest_sections.py`); katta bobni
butun o'qish, konteyner, bazaga ulanish va PowerShell to'siladi
(`guard.py`); Java fayl yozilganda mexanik qoidalar tekshiriladi va
`rules_for.py` chaqirilgani talab qilinadi (`check_code.py`); zanjir
aktyorlari (`rejalashtiruvchi`, `arxitektor`, `test-muhandis`, `review`)
bir vazifada ko'pi bilan ikki martadan chaqiriladi, `qidiruv` va `tahlil`
sanalmaydi (`budget.py`); token sarfi `.claude/usage/` ga yoziladi
(`usage.py`).

Sakkizta marshrut skilli faqat shu repo ichida ishlaydi: ulardagi `docs/` va
`tools/` yo'llari joriy papkaga nisbatan hal qilinadi va boshqa proyektda
topilmaydi, shuning uchun ularni boshqa joyga ko'chirmang. Boshqa Java
proyektda `manguberdi` ishlatiladi. U olti aktyor va hooklar bilan birga
[global o'rnatish](install/README.md#b-yoli-global-ornatish) yo'li bilan
o'rnatiladi va o'rnatuvchi (hozircha PowerShell skripti) yo'llarni klonga
mutlaq bog'laydi, shuning uchun klon o'chirilmaydi va ko'chirilmaydi. Bu
yo'l `~/.claude/` dagi avvalgi skill, agent va sozlamalarni zaxiraga olib
o'chiradi, shuning uchun avval `-Apply` siz yurgiziladi.

## Memory

`memory/` papkasida git ichida saqlanadigan memory ombori. Proyekt memoryasi
`memory/claude-genius/`, barcha proyektlarga tegishli bilim `memory/umumiy/`
da. Qoidalar: [memory-protocol.md](memory-protocol.md) va
[memory/README.md](memory/README.md).

## Tez qidirish

Korpus katta (~2.1M token), shuning uchun bob fayli butunligicha emas,
bo'lim darajasida o'qiladi:

```bash
tools/doc.sh find "circuit breaker"   # bo'limni topish
tools/doc.sh show patterns 17.2       # faqat o'sha bo'limni chiqarish
tools/doc.sh toc                      # hujjatlar va boblar
```

Qidiruv inglizcha atama bo'yicha ham ishlaydi: 1380 ta inglizcha nom bo'lim
raqamiga bog'langan. Indeks `index/` da turadi va bob o'zgarganda o'zini
yangilaydi. Qoidalar: [CLAUDE.md](CLAUDE.md).

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

Fayl hajmi, har bir havola va anchor, kirill harflar, em-dash, kod fence
juftligi, manifest mosligi, bob strukturasi, bob-yopish konvensiyasi va
skilllardagi havolalar tekshiriladi. CI buni `main` ga har push va har PR
da ishlatadi. Alohida `tools` ishi asbob sinovlarini, `eval_skill.py`,
`eval_find.py` va `cost_report.py` ni yurgizadi.

## Til va uslub

O'zbek lotin yozuvi. Texnik atamalar inglizcha qoldirilgan: bean, proxy,
thread, cache, latency, quality gate, coverage. Em-dash ishlatilmaydi.
To'liq qoidalar: [CONTRIBUTING.md](CONTRIBUTING.md).

## Litsenziya

Matn (.md fayllar): [CC BY 4.0](LICENSE). Kod misollari va .md bo'lmagan
barcha fayllar (`tools/`, `install/`, `.claude/settings.json`):
[MIT](LICENSE-CODE).
