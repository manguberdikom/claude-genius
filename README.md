# Java, Spring va PostgreSQL bo'yicha to'rtta qo'llanma

O'zbek tilidagi to'rtta bir-birini to'ldiruvchi hujjat. Har biri alohida sohani
qamraydi va mavzular takrorlanmaydi: pattern katalogi patternlar hujjatida,
testlash texnikasi testlash qo'llanmasida, ichki mexanika arxitektor hujjatida,
statik tahlil esa SonarQube hujjatida turadi.

| Hujjat | Hajm | Mazmun |
|---|---|---|
| [java-spring-design-patterns.md](java-spring-design-patterns.md) | 30 bo'lim, 1007 pattern | GoF, Spring, DDD, microservices, EIP, resilience, cloud-native va boshqa pattern kataloglari |
| [java-spring-testing-handbook.md](java-spring-testing-handbook.md) | 18 bob | Test piramidasi, unit va integratsion test, Testcontainers, contract testing, E2E, CI/CD test pipeline |
| [java-spring-architect-mindset.md](java-spring-architect-mindset.md) | 39 bob, 482 bo'lim | Fikrlash va qaror, JVM ichki tuzilishi, Spring mexanikasi, PostgreSQL chuqur bilim, operatsion haqiqat |
| [java-spring-sonarqube.md](java-spring-sonarqube.md) | 43 bob, 557 bo'lim | SonarQube mexanikasi, quality gate, coverage, xato katalogi, server va tashkilot, ma'lumotnoma |

## Qayerdan boshlash

- **Kod yozyapsiz va Sonar shikoyat qilyapti** - SonarQube hujjatidagi xato katalogi
- **Dizayn qaroriga pattern tanlayapsiz** - patternlar hujjatidagi mavzuga mos bo'lim
- **Test strategiyasi tuzyapsiz** - testlash qo'llanmasining birinchi boblari
- **Ichkarida nima sodir bo'layotganini bilmoqchisiz** - arxitektor hujjatidagi tegishli qism
- **O'zingizni baholamoqchisiz** - arxitektor hujjatining oxirgi bobi

Har bir hujjat mundarija bilan boshlanadi va har bob `Amalda qo'llash` ro'yxati
bilan tugaydi.

## Reja tuzuvchi skill: `/reja`

`.claude/skills/reja/` — kod yozishdan oldin bitta hujjat (`REJA.md`) tayyorlaydigan
Claude Code skill'i. U to'rtta qo'llanmani bitta ish oqimiga bog'laydi: arxitektura
qarorini, pattern tanlovini, test strategiyasini va quality gate talablarini bitta
rejaga yig'adi.

Ishlash tartibi — yettita bosqich, har biri o'z artefakti bilan:

| Bosqich | Nima qiladi | Reference |
|---|---|---|
| 1. Manba yig'ish | `pom.xml`, `application.yml`, Sonar/CI config, `CLAUDE.md` va memory fayllari, berilgan PDF / HTML / DOCX / rasm / URL | `references/manbalar.md` |
| 2. Kod analizi | tuzilish, kirish nuqtalari, qatlam yo'nalishi, ma'lumot yo'li, issiq nuqtalar, test haqiqati | `references/kod-analizi.md` |
| 3. Arxitektura | NFR budjeti, napkin math, chegaralar, ADR, risk ro'yxati | `references/arxitektura.md` |
| 4. Pattern tayinlash | `fayl:qator` -> pattern -> sabab -> narx -> qo'llanma bo'limi | `references/pattern-tanlash.md` |
| 5. Test va sifat | test matritsasi (daraja, joy, ma'lumot, oracle) va gate talablari | `references/test-sifat.md` |
| 6. Rejani yozish | prompt dizayn qoidalari va `REJA.md` shabloni | `references/prompt-dizayn.md`, `references/shablon.md` |
| 7. Tekshirish | 12 bandli yakuniy checklist | `SKILL.md` |

Asosiy qoidalari: manbaga bog'lanmagan da'vo yozilmaydi (`fayl:qator`, config
kaliti yoki PDF sahifasi), variant emas — qaror beriladi, har qadam loyihani
yashil qoldiradi, har pattern uchun narxi va qo'llanma bo'limi ko'rsatiladi.
Prompt dizayn bo'yicha PDF/HTML berilsa, uning texnikalari skill'ning bazaviy
qoidalaridan ustun turadi.

## Til va uslub

O'zbek lotin yozuvi. Texnik atamalar inglizcha qoldirilgan: bean, proxy, thread,
cache, latency, quality gate, coverage.
