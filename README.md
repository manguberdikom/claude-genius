# Java, Spring va PostgreSQL bo'yicha beshta qo'llanma

O'zbek tilidagi beshta bir-birini to'ldiruvchi hujjat. Har biri alohida sohani
qamraydi va mavzular takrorlanmaydi: pattern katalogi patternlar hujjatida,
testlash texnikasi testlash qo'llanmasida, ichki mexanika arxitektor hujjatida,
statik tahlil SonarQube hujjatida, kod review esa review hujjatida turadi.

| Hujjat | Hajm | Mazmun |
|---|---|---|
| [java-spring-design-patterns.md](java-spring-design-patterns.md) | 30 bo'lim, 1007 pattern | GoF, Spring, DDD, microservices, EIP, resilience, cloud-native va boshqa pattern kataloglari |
| [java-spring-testing-handbook.md](java-spring-testing-handbook.md) | 18 bob | Test piramidasi, unit va integratsion test, Testcontainers, contract testing, E2E, CI/CD test pipeline |
| [java-spring-architect-mindset.md](java-spring-architect-mindset.md) | 39 bob, 482 bo'lim | Fikrlash va qaror, JVM ichki tuzilishi, Spring mexanikasi, PostgreSQL chuqur bilim, operatsion haqiqat |
| [java-spring-sonarqube.md](java-spring-sonarqube.md) | 43 bob, 557 bo'lim | SonarQube mexanikasi, quality gate, coverage, xato katalogi, server va tashkilot, ma'lumotnoma |
| [java-spring-code-review.md](java-spring-code-review.md) | 44 bob, 445 bo'lim | Diffni o'qish, arxitektura va pattern review, Java/Spring/PostgreSQL tahlili, xavfsizlik, test to'liqligi, jarayon va metrikalar |

## Memory protokoli

Qo'llanmalardan tashqari bitta ish hujjati bor:
[memory-protocol.md](memory-protocol.md). U Claude sessiyalari orasida bilim
qanday saqlanishini belgilaydi: qaysi bilim qaysi joyga boradi, qanday tartibda
o'qiladi va yoziladi, nima umuman saqlanmaydi. Memory haqida gap boradigan
boshqa fayllar qoidani nusxalamaydi, shu faylga havola qiladi.

Filtrdan o'tgan bilimning o'zi [memory/](memory/) papkasida, proyekt bo'yicha
yig'iladi: `memory/umumiy/` barcha proyektlarga tegishli bilim, `memory/<proyekt-slug>/`
esa bitta proyektga tegishli bilim. Boshqa proyektda ishlayotgan sessiya o'sha
proyekt papkasidan kerakligini o'qiydi. Ombor qoidasi [memory/README.md](memory/README.md) da.

## Reja tuzuvchi skill: `/reja`

`.claude/skills/reja/` - kod yozishdan oldin bitta hujjat (`REJA.md`) tayyorlaydigan
Claude Code skill'i. U beshta qo'llanmani bitta ish oqimiga bog'laydi: arxitektura
qarorini, pattern tanlovini, test strategiyasini, quality gate talablarini va
review nuqtai nazarini bitta rejaga yig'adi.

Yettita bosqich, har biri o'z artefakti bilan:

| Bosqich | Nima qiladi | Reference |
|---|---|---|
| 1. Manba yig'ish | `pom.xml`, `application.yml`, Sonar va CI config, `CLAUDE.md`, `memory/` indekslari, berilgan PDF, HTML, DOCX, rasm yoki URL | `references/manbalar.md` |
| 2. Kod analizi | tuzilish, kirish nuqtalari, qatlam yo'nalishi, ma'lumot yo'li, issiq nuqtalar, test haqiqati | `references/kod-analizi.md` |
| 3. Arxitektura | NFR budjeti, napkin math, chegaralar, ADR, risk ro'yxati | `references/arxitektura.md` |
| 4. Pattern tayinlash | `fayl:qator` -> pattern -> sabab -> narx -> qo'llanmadagi mavzu | `references/pattern-tanlash.md` |
| 5. Test va sifat | test matritsasi (daraja, joy, ma'lumot, oracle) va gate talablari | `references/test-sifat.md` |
| 6. Rejani yozish | prompt dizayn qoidalari va `REJA.md` shabloni | `references/prompt-dizayn.md`, `references/shablon.md` |
| 7. Tekshirish | 13 bandli yakuniy checklist | `SKILL.md` |

Asosiy qoidalari: manbaga bog'lanmagan da'vo yozilmaydi (`fayl:qator`, config
kaliti yoki PDF sahifasi), variant emas - qaror beriladi, har qadam loyihani
yashil qoldiradi, har pattern uchun narxi va qo'llanmadagi mavzu nomi
ko'rsatiladi. Prompt dizayn bo'yicha PDF yoki HTML berilsa, uning texnikalari
skill'ning bazaviy qoidalaridan ustun turadi.

## Qayerdan boshlash

- **Kod yozyapsiz va Sonar shikoyat qilyapti** - SonarQube hujjatidagi xato katalogi
- **Dizayn qaroriga pattern tanlayapsiz** - patternlar hujjatidagi mavzuga mos bo'lim
- **Test strategiyasi tuzyapsiz** - testlash qo'llanmasining birinchi boblari
- **Ichkarida nima sodir bo'layotganini bilmoqchisiz** - arxitektor hujjatidagi tegishli qism
- **Oldingizda PR turibdi va nimaga qarashni bilmoqchisiz** - review hujjatining 3, 4 va 44-boblari
- **O'zingizni baholamoqchisiz** - arxitektor hujjatining oxirgi bobi, review hujjatining 44-bobi
- **Ish boshlashdan oldin reja kerak** - `/reja` skill'i, u beshtasini birga ishlatadi

Har bir hujjat mundarija bilan boshlanadi va har bob `Amalda qo'llash` ro'yxati
bilan tugaydi.

## Hujjatlar qanday bog'langan

Review hujjati qolgan to'rttasining bilimini review stoliga olib chiqadi: qaysi
mexanika diffda qanday belgi qoldiradi va shu belgini ko'rgan reviewer nima
deyishi kerak. Mexanikaning o'zi kerak bo'lganda tegishli hujjatga havola
qilinadi, takrorlanmaydi.

```
patterns  --->  "bu yerda Strategy kerakmi, yoki switch yetadi?"      ---> review
testing   --->  "test holatlari to'liqmi, assertion nimani tekshiradi?" ---> review
architect --->  "bu migratsiya qanday qulf oladi, N+1 qayerdan keldi?"  ---> review
sonarqube --->  "Sonar nimani topadi, odam nimani topishi kerak?"       ---> review
```

## Til va uslub

O'zbek lotin yozuvi. Texnik atamalar inglizcha qoldirilgan: bean, proxy, thread,
cache, latency, quality gate, coverage, review, blocker, diff.
