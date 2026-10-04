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

## Memory protokoli

Qo'llanmalardan tashqari bitta ish hujjati bor:
[memory-protocol.md](memory-protocol.md). U Claude sessiyalari orasida bilim
qanday saqlanishini belgilaydi: qaysi bilim qaysi joyga boradi, qanday tartibda
o'qiladi va yoziladi, nima umuman saqlanmaydi. Memory haqida gap boradigan
boshqa fayllar qoidani nusxalamaydi, shu faylga havola qiladi.

## Qayerdan boshlash

- **Kod yozyapsiz va Sonar shikoyat qilyapti** - SonarQube hujjatidagi xato katalogi
- **Dizayn qaroriga pattern tanlayapsiz** - patternlar hujjatidagi mavzuga mos bo'lim
- **Test strategiyasi tuzyapsiz** - testlash qo'llanmasining birinchi boblari
- **Ichkarida nima sodir bo'layotganini bilmoqchisiz** - arxitektor hujjatidagi tegishli qism
- **O'zingizni baholamoqchisiz** - arxitektor hujjatining oxirgi bobi

Har bir hujjat mundarija bilan boshlanadi va har bob `Amalda qo'llash` ro'yxati
bilan tugaydi.

## Til va uslub

O'zbek lotin yozuvi. Texnik atamalar inglizcha qoldirilgan: bean, proxy, thread,
cache, latency, quality gate, coverage.
