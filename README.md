# Java, Spring va PostgreSQL bo'yicha to'rtta qo'llanma

O'zbek tilidagi to'rtta bir-birini to'ldiruvchi hujjat: 2285 bo'lim, 130 bob,
1276 kod misoli. Mavzular takrorlanmaydi - pattern katalogi patternlar
hujjatida, testlash texnikasi testlash qo'llanmasida, ichki mexanika arxitektor
hujjatida, statik tahlil esa SonarQube hujjatida turadi.

| Hujjat | Hajm | Mazmun |
|---|---|---|
| [Dizayn patternlar](docs/patterns/README.md) | 30 bo'lim, 1007 pattern | GoF, Spring, DDD, microservices, EIP, resilience, cloud-native va boshqa pattern kataloglari |
| [Testlash qo'llanmasi](docs/testing/README.md) | 18 bob, 239 bo'lim | Test piramidasi, unit va integratsion test, Testcontainers, contract testing, E2E, CI/CD test pipeline |
| [Arxitektor miyyasi](docs/architect/README.md) | 39 bob, 482 bo'lim | Fikrlash va qaror, JVM ichki tuzilishi, Spring mexanikasi, PostgreSQL chuqur bilim, operatsion haqiqat |
| [SonarQube](docs/sonarqube/README.md) | 43 bob, 557 bo'lim | SonarQube mexanikasi, quality gate, coverage, xato katalogi, server va tashkilot, ma'lumotnoma |

Har bir hujjat alohida papkada, har bob alohida faylda. Bu ataylab: GitHub
1 MB dan katta markdown faylni render qilmaydi, monolit variant brauzerda
umuman ochilmaydi.

## Qayerdan boshlash

- **Kod yozyapsiz va Sonar shikoyat qilyapti** - [xato katalogi](docs/sonarqube/README.md#vii-xato-katalogi-qanday-kod-qanday-xato-hisoblanadi)
- **Dizayn qaroriga pattern tanlayapsiz** - [patternlar mundarijasi](docs/patterns/README.md) yoki [alifbo indeksi](docs/patterns/99-alifbo-boyicha-indeks.md)
- **Test strategiyasi tuzyapsiz** - [testlash qo'llanmasining birinchi boblari](docs/testing/README.md)
- **Ichkarida nima sodir bo'layotganini bilmoqchisiz** - [arxitektor hujjati](docs/architect/README.md)
- **O'zingizni baholamoqchisiz** - [Birinchi 90 kun va o'z-o'zini baholash](docs/architect/39-birinchi-90-kun-va-oz-ozini-baholash.md)
- **Atama tushunarsiz** - [GLOSSARY.md](GLOSSARY.md)

## Claude Code bilan ishlatish

`.claude/skills/` ichida beshta skill bor. Repoda Claude Code ishga tushsa,
ular avtomatik ko'rinadi va kerakli bobni o'zi topib o'qiydi:

| Skill | Qachon ishga tushadi |
|---|---|
| `design-patterns` | pattern tanlash, refaktoring, "bu yerga qaysi pattern to'g'ri keladi" |
| `spring-testing` | test yozish, Testcontainers, flaky test, test strategiyasi |
| `sonarqube-fix` | Sonar issue tuzatish, quality gate, coverage, exclusion |
| `architect-review` | dizayn ko'rigi, chegaralar, ADR, nosozlik tahlili |
| `postgres-tuning` | sekin so'rov, indeks, EXPLAIN, vacuum, connection pool |

Boshqa loyihada ishlatish uchun shu repo'ni klon qilib,
`.claude/skills/*` ni o'z loyihangizning `.claude/skills/` ichiga
ko'chiring yoki `~/.claude/skills/` ga qo'ying.

## Bitta fayllik variant

Offline o'qish, PDF yoki LLM kontekstiga uzatish uchun:

```bash
python3 tools/build_single.py              # to'rttasi ham -> dist/
python3 tools/build_single.py patterns     # faqat bittasi
```

`dist/` git ga kirmaydi - u har safar `docs/` dan qayta yig'iladi.

## Tekshirish

```bash
python3 tools/check_docs.py
```

Fayl hajmi, har bir havola va anchor, kirill harflar, manifest mosligi va bob
strukturasi tekshiriladi. CI da har push va PR da ishlaydi.

## Til va uslub

O'zbek lotin yozuvi. Texnik atamalar inglizcha qoldirilgan: bean, proxy, thread,
cache, latency, quality gate, coverage. To'liq qoidalar:
[CONTRIBUTING.md](CONTRIBUTING.md).

## Litsenziya

Matn: [CC BY 4.0](LICENSE). Kod misollari: [MIT](LICENSE-CODE).
