# Java, Spring va PostgreSQL bo'yicha oltita qo'llanma

O'zbek tilidagi oltita bir-birini to'ldiruvchi hujjat: 224 bob, 3293 bo'lim,
2300 dan ortiq kod misoli. Har bir hujjat bir savolga javob beradi. Ba'zi
mavzular bir nechta hujjatda uchraydi, chunki ular har bir nuqtadan
boshqacha ko'rinadi: masalan N+1 so'rovi pattern, arxitektura, review va
Sonar tomonidan.
Mavzuning to'liq yozuvi bitta uy bo'limda (`docs/OWNERS.tsv`), boshqa hujjat o'z nuqtai nazarini yozadi va uyga mavzu nomi bilan havola beradi.

| Hujjat | Hajm | Qanday savolga javob beradi |
|---|---|---|
| [Dizayn patternlar](docs/patterns/README.md) | 31 bob, 1037 bo'lim | Bu muammoga qaysi pattern to'g'ri keladi |
| [Testlash qo'llanmasi](docs/testing/README.md) | 18 bob, 239 bo'lim | Buni qanday test qilaman |
| [Arxitektor miyasi](docs/architect/README.md) | 39 bob, 482 bo'lim | Ichkarida nima sodir bo'ladi va qanday qaror chiqaraman |
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

`.claude/skills/` ichida sakkizta skill bor: yettitasi qo'llanmaga marshrut,
`manguberdi` esa orkestrator. Repoda Claude Code ishga tushsa, yettitasi
avtomatik ko'rinadi va kerakli bobni o'zi topib o'qiydi, `manguberdi` esa
sessiyada bir marta `/manguberdi` bilan chaqiriladi. U `.claude/agents/`
dagi olti aktyorni yurgizadi.

| Skill | Qachon ishga tushadi |
|---|---|
| `design-patterns` | pattern tanlash, refaktoring, "bu yerga qaysi pattern to'g'ri keladi" |
| `spring-testing` | test yozish, Testcontainers, flaky test, test strategiyasi |
| `sonarqube-fix` | Sonar issue tuzatish, quality gate, coverage, exclusion |
| `architect-review` | dizayn ko'rigi, chegaralar, ADR, nosozlik tahlili |
| `postgres-tuning` | sekin so'rov, indeks, EXPLAIN, vacuum, connection pool |
| `clean-code` | nomlash, funksiya uzunligi, izoh, kod hidi, refaktoring |
| `code-review` | diffni o'qish, review izohi yozish, nimani to'xtatish |
| `manguberdi` | Java/Spring ishi, kichik vazifa ham: aktyor tanlab reja, kod, test va review ni ketma-ket yurgizadi, oxirida memoryga yozadi |

Hooklar `.claude/settings.json` da turadi va repoda o'zi ishlaydi: har
so'rovga mos bo'lim taklif qilinadi (`suggest_sections.py`); katta bobni
butun o'qish to'siladi, konteyner, bazaga ulanish va PowerShell esa
foydalanuvchi qaroriga qo'yiladi (`guard.py`); Java fayl yozilganda mexanik qoidalar tekshiriladi va
`rules_for.py` chaqirilgani talab qilinadi (`check_code.py`); zanjir
aktyorlari (`rejalashtiruvchi`, `dasturchi`, `test-muhandis`, `review`)
bir vazifada ko'pi bilan ikki martadan chaqiriladi, `qidiruv` va `tahlil`
sanalmaydi (`budget.py`); token sarfi `.claude/usage/` ga yoziladi
(`usage.py`).

Hooklar faqat ikki joyda ish qiladi: shu klonda va Java proyektida (ildizida
yoki birinchi darajali papkasida `pom.xml` yoki Gradle fayli bo'lgan repo).
Global o'rnatishda ular har proyektda yuradi, lekin boshqa joyda chiqishsiz
0 bilan chiqadi, ya'ni Python yoki JS proyektida hech narsa to'smaydi.
`GENIUS_HOOKS=off` hammasini o'chiradi. Tafsiloti
[install/README.md](install/README.md#hooklar-qaysi-proyektda-ishlaydi) da.

Yettita marshrut skilli faqat shu repo ichida ishlaydi: ulardagi `docs/` va
`tools/` yo'llari joriy papkaga nisbatan hal qilinadi va boshqa proyektda
topilmaydi, shuning uchun ularni boshqa joyga ko'chirmang. Boshqa Java
proyektda `manguberdi` ishlatiladi. U olti aktyor va hooklar bilan birga
[global o'rnatish](install/README.md#b-yoli-global-ornatish) yo'li bilan
o'rnatiladi va o'rnatuvchi (hozircha PowerShell skripti) yo'llarni klonga
mutlaq bog'laydi, shuning uchun klon o'chirilmaydi va ko'chirilmaydi. Bu
yo'l qo'shuvchi: faqat `manguberdi` birliklari almashadi, `~/.claude/`
dagi boshqa skill, agent va sozlamalarga tegilmaydi. To'liq tozalash
faqat `-Reset -ConfirmReset` bilan. Baribir avval `-Apply` siz
yurgiziladi: ro'yxat chiqadi, hech narsa o'zgarmaydi.

## Memory

`memory/` papkasida git ichida saqlanadigan memory ombori. Proyekt memoryasi
`memory/claude-genius/`, barcha proyektlarga tegishli bilim `memory/umumiy/`
da. Qoida bitta faylda: [memory/README.md](memory/README.md). Nima
yoziladi, nima yozilmaydi, qayerga, qanday format va qachon o'chiriladi.

## Tez qidirish

Korpus katta (~6.4 MB), shuning uchun bob fayli butunligicha emas,
bo'lim darajasida o'qiladi:

```bash
tools/doc.sh find "circuit breaker"   # bo'limni topish
tools/doc.sh show patterns 17.2       # faqat o'sha bo'limni chiqarish
tools/doc.sh toc                      # hujjatlar va boblar
```

Qidiruv inglizcha atama bo'yicha ham ishlaydi: 1300 dan ortiq inglizcha nom bo'lim
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

SPDX: `CC-BY-4.0 AND MIT`. Ikki litsenziya, qamrovi fayl turi bo'yicha:

| Nima | Litsenziya |
|---|---|
| Hujjat matni: `docs/` dagi boblar, ildizdagi va `install/` dagi `.md` hujjatlar | [CC BY 4.0](LICENSE) |
| `.md` ichidagi kod misollari (kod bloki, undagi izoh ham) | [MIT](LICENSE-CODE) |
| `.md` bo'lmagan barcha fayllar: `tools/`, `install/`, `.github/`, `.claude/settings.json` | [MIT](LICENSE-CODE) |
| Funksional `.md`: `.claude/skills/`, `.claude/agents/`, `memory/`, `CLAUDE.md` | [MIT](LICENSE-CODE) |

`LICENSE` va `LICENSE-CODE` litsenziyaning kanonik matnini saqlaydi,
qamrov faqat shu jadvalda. Bo'limni nusxalaganda nasr uchun CC BY
atributi (manba va litsenziya havolasi) yetadi, kod bloki esa MIT
bildirishnomasi bilan olinadi.
