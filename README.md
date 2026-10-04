# Java, Spring va PostgreSQL bo'yicha oltita qo'llanma

O'zbek tilidagi oltita bir-birini to'ldiruvchi hujjat. Har biri alohida sohani
qamraydi va mavzular takrorlanmaydi: pattern katalogi patternlar hujjatida,
testlash texnikasi testlash qo'llanmasida, ichki mexanika arxitektor hujjatida,
statik tahlil SonarQube hujjatida, kod yozish qoidalari toza kod hujjatida, kod
review esa review hujjatida turadi.

| Hujjat | Hajm | Mazmun |
|---|---|---|
| [java-spring-design-patterns.md](java-spring-design-patterns.md) | 30 bo'lim, 1007 pattern | GoF, Spring, DDD, microservices, EIP, resilience, cloud-native va boshqa pattern kataloglari |
| [java-spring-testing-handbook.md](java-spring-testing-handbook.md) | 18 bob | Test piramidasi, unit va integratsion test, Testcontainers, contract testing, E2E, CI/CD test pipeline |
| [java-spring-architect-mindset.md](java-spring-architect-mindset.md) | 39 bob, 482 bo'lim | Fikrlash va qaror, JVM ichki tuzilishi, Spring mexanikasi, PostgreSQL chuqur bilim, operatsion haqiqat |
| [java-spring-sonarqube.md](java-spring-sonarqube.md) | 43 bob, 557 bo'lim | SonarQube mexanikasi, quality gate, coverage, xato katalogi, server va tashkilot, ma'lumotnoma |
| [java-spring-code-review.md](java-spring-code-review.md) | 44 bob, 445 bo'lim | Diffni o'qish, arxitektura va pattern review, Java/Spring/PostgreSQL tahlili, xavfsizlik, test to'liqligi, jarayon va metrikalar |
| [java-spring-clean-coder.md](java-spring-clean-coder.md) | 49 bob, 533 bo'lim | Nomlash, funksiya, izoh, formatlash, obyekt shartnomalari, xato bilan ishlash, Java/Spring/JPA kodi uslubi, test tozaligi, hid va refaktoring katalogi, professional intizom |

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

## Qayerdan boshlash

- **Kod yozyapsiz va Sonar shikoyat qilyapti** - SonarQube hujjatidagi xato katalogi
- **Dizayn qaroriga pattern tanlayapsiz** - patternlar hujjatidagi mavzuga mos bo'lim
- **Test strategiyasi tuzyapsiz** - testlash qo'llanmasining birinchi boblari
- **Ichkarida nima sodir bo'layotganini bilmoqchisiz** - arxitektor hujjatidagi tegishli qism
- **Nomni, funksiyani yoki izohni qanday yozishni hal qilyapsiz** - toza kod hujjatining tegishli bobi
- **Kod hidini topdingiz va refaktoring harakati kerak** - toza kod hujjatidagi hid va refaktoring kataloglari
- **Oldingizda PR turibdi va nimaga qarashni bilmoqchisiz** - review hujjatining 3, 4 va 44-boblari
- **O'zingizni baholamoqchisiz** - arxitektor hujjatining oxirgi bobi, review hujjatining 44-bobi, toza kod hujjatining 49-bobi

Har bir hujjat mundarija bilan boshlanadi va har bob `Amalda qo'llash` ro'yxati
bilan tugaydi.

## Hujjatlar qanday bog'langan

Toza kod hujjati kod **yozish** tomonida turadi: nomni, funksiyani, izohni va
xato yo'lini qanday yozish kerak. Review hujjati esa o'sha bilimni **o'qish**
tomoniga olib chiqadi: qaysi mexanika diffda qanday belgi qoldiradi va shu
belgini ko'rgan reviewer nima deyishi kerak. Mexanikaning o'zi kerak bo'lganda
tegishli hujjatga havola qilinadi, takrorlanmaydi.

```
patterns  --->  "bu yerda Strategy kerakmi, yoki switch yetadi?"        ---> review
testing   --->  "test holatlari to'liqmi, assertion nimani tekshiradi?" ---> review
architect --->  "bu migratsiya qanday qulf oladi, N+1 qayerdan keldi?"  ---> review
sonarqube --->  "Sonar nimani topadi, odam nimani topishi kerak?"       ---> review
clean     --->  "shu qator qanday yozilishi kerak edi?"                 ---> review
```

## Til va uslub

O'zbek lotin yozuvi. Texnik atamalar inglizcha qoldirilgan: bean, proxy, thread,
cache, latency, quality gate, coverage, review, blocker, diff.
