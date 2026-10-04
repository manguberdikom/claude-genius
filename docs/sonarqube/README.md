# SonarQube: qanday ishlaydi va qanday kod bilan test undan o'tadi

Bu hujjat SonarQube ning ichki ishlashini va undan o'tadigan kod bilan testni
yozish yo'lini bir joyga yig'adi. Tayanch stek: Java, Spring va PostgreSQL.

Ogohlantirish: "har doim 100% o'tadigan" universal retsept yo'q. Quality gate
shartlari har loyihada boshqacha sozlanadi, va 100% coverage sifatni kafolatlamaydi.
Hujjat ikkalasini ham ko'rsatadi: shartni qanday qondirish, va qayerda bu raqam aldashi.

**Bu hujjat to'rtlikning bir qismi.** Mavzular takrorlanmaydi; qolgan uchtasi: [Dizayn patternlar katalogi](../patterns/README.md), [Testlash qo'llanmasi](../testing/README.md), [Arxitektor miyyasi](../architect/README.md).

**Versiya bazasi:** Java 21 LTS (pol: 17, Java 25 eslatmalari bilan), Spring Boot 3.2-3.5 (4.0 eslatmalari bilan), PostgreSQL 16+ (15-18 havolalari bilan), JUnit 5, SonarQube 2025.x LTA (9.9 LTA merosiy eslatmalari bilan).

## Mundarija

### I. SonarQube qanday ishlaydi

- **1.** [SonarQube arxitekturasi va tahlil oqimi (Architecture and Analysis Flow)](01-sonarqube-arxitekturasi-va-tahlil-oqimi.md) - 11 bo'lim
- **2.** [Scanner nimani yig'adi va qanday yuboradi (What the Scanner Collects)](02-scanner-nimani-yigadi-va-qanday-yuboradi.md) - 11 bo'lim
- **3.** [Issue turlari: bug, vulnerability, code smell, security hotspot (Issue Types)](03-issue-turlari-bug-vulnerability-code-smell.md) - 11 bo'lim
- **4.** [Rule, quality profile va severity (Rules, Profiles and Severity)](04-rule-quality-profile-va-severity.md) - 11 bo'lim
- **5.** [Metrikalar: rating, texnik qarz, murakkablik, takrorlanish (Metrics and Ratings)](05-metrikalar-rating-texnik-qarz-murakkablik.md) - 11 bo'lim

### II. Quality gate

- **6.** [Quality gate mexanikasi va shartlari (Quality Gate Mechanics)](06-quality-gate-mexanikasi-va-shartlari.md) - 11 bo'lim
- **7.** [Yangi kod (new code) va "clean as you code" tamoyili (New Code and Clean as You Code)](07-yangi-kod-new-code-va-clean-as-you-code.md) - 11 bo'lim
- **8.** [100% ga sozlangan gate: har bir shart nimani talab qiladi (A Gate Set to 100 Percent)](08-100-ga-sozlangan-gate-har-bir-shart-nimani.md) - 12 bo'lim

### III. Qamrov (coverage)

- **9.** [Coverage qanday o'lchanadi: JaCoCo mexanikasi (How Coverage Is Measured)](09-coverage-qanday-olchanadi-jacoco-mexanikasi.md) - 11 bo'lim
- **10.** [JaCoCo va SonarQube ulanishi: Maven va Gradle sozlash (Wiring JaCoCo to SonarQube)](10-jacoco-va-sonarqube-ulanishi-maven-va.md) - 12 bo'lim
- **11.** [Qamralmay qoladigan kod va unga test yozish (Code That Stays Uncovered)](11-qamralmay-qoladigan-kod-va-unga-test-yozish.md) - 15 bo'lim
- **12.** [Exclusion: nimani chiqarish halol, nimani chiqarish aldov (Exclusions, Honest and Dishonest)](12-exclusion-nimani-chiqarish-halol-nimani.md) - 12 bo'lim

### IV. Sonar o'tadigan kod

- **13.** [Sonar o'tadigan kod yozish qoidalari (Writing Code That Passes)](13-sonar-otadigan-kod-yozish-qoidalari.md) - 12 bo'lim
- **14.** [Java va Spring da eng ko'p uchraydigan issue va ularning yechimi (Common Java and Spring Issues)](14-java-va-spring-da-eng-kop-uchraydigan-issue.md) - 13 bo'lim
- **15.** [Cognitive complexity va takrorlanishni kamaytirish (Cognitive Complexity and Duplication)](15-cognitive-complexity-va-takrorlanishni.md) - 12 bo'lim
- **16.** [Security hotspot va vulnerability: tekshirish va tuzatish (Security Hotspots and Vulnerabilities)](16-security-hotspot-va-vulnerability.md) - 12 bo'lim

### V. Sonar o'tadigan test

- **17.** [Sonar talablarini qondiradigan test yozish (Writing Tests That Satisfy Sonar)](17-sonar-talablarini-qondiradigan-test-yozish.md) - 12 bo'lim
- **18.** [Branch va shart qamrovini to'liq yopish usullari (Covering Every Branch)](18-branch-va-shart-qamrovini-toliq-yopish.md) - 15 bo'lim
- **19.** [Testning o'zidagi Sonar qoidalari va test sifati (Sonar Rules on Test Code)](19-testning-ozidagi-sonar-qoidalari-va-test.md) - 12 bo'lim
- **20.** [Mutation testing: 100% coverage qachon yolg'on (Mutation Testing)](20-mutation-testing-100-coverage-qachon-yolgon.md) - 12 bo'lim

### VI. Amaliyot va jarayon

- **21.** [CI/CD ga ulash, PR decoration va blokirovka (CI/CD Integration)](21-ci-cd-ga-ulash-pr-decoration-va-blokirovka.md) - 12 bo'lim
- **22.** [Lokal tekshirish: IDE, sonar-scanner va tez qaytish (Local Feedback Loop)](22-lokal-tekshirish-ide-sonar-scanner-va-tez.md) - 11 bo'lim
- **23.** [Legacy loyihani 100% ga olib chiqish rejasi (Bringing a Legacy Project to 100)](23-legacy-loyihani-100-ga-olib-chiqish-rejasi.md) - 13 bo'lim
- **24.** [False positive, suppression va o'z qoidangiz (False Positives and Custom Rules)](24-false-positive-suppression-va-oz-qoidangiz.md) - 12 bo'lim

### VII. Xato katalogi: qanday kod qanday xato hisoblanadi

- **25.** [Xato katalogi: reliability (bug) toifasi (Catalog: Reliability)](25-xato-katalogi-reliability-bug-toifasi.md) - 19 bo'lim
- **26.** [Xato katalogi: security (vulnerability va hotspot) (Catalog: Security)](26-xato-katalogi-security-vulnerability-va.md) - 17 bo'lim
- **27.** [Xato katalogi: maintainability, tuzilish va murakkablik (Catalog: Maintainability, Structure)](27-xato-katalogi-maintainability-tuzilish-va.md) - 17 bo'lim
- **28.** [Xato katalogi: maintainability, nomlash, o'lik kod va uslub (Catalog: Maintainability, Naming)](28-xato-katalogi-maintainability-nomlash-olik.md) - 17 bo'lim
- **29.** [Xato katalogi: Spring, JPA va PostgreSQL ga xos xatolar (Catalog: Spring, JPA and PostgreSQL)](29-xato-katalogi-spring-jpa-va-postgresql-ga.md) - 17 bo'lim
- **30.** [Xato katalogi: test kodidagi xatolar (Catalog: Test Code)](30-xato-katalogi-test-kodidagi-xatolar.md) - 15 bo'lim
- **31.** [Xatolarga tushmaslik uchun yakuniy tavsiyalar (Preventive Checklist)](31-xatolarga-tushmaslik-uchun-yakuniy.md) - 12 bo'lim

### VIII. Server va tashkilot

- **32.** [SonarQube nashrlari va ularning farqi (Editions)](32-sonarqube-nashrlari-va-ularning-farqi.md) - 12 bo'lim
- **33.** [Serverni o'rnatish, sozlash va resurs rejalashtirish (Installing and Sizing the Server)](33-serverni-ornatish-sozlash-va-resurs.md) - 12 bo'lim
- **34.** [Yangilash, LTA migratsiyasi, zaxira va housekeeping (Upgrades, Backup and Housekeeping)](34-yangilash-lta-migratsiyasi-zaxira-va.md) - 12 bo'lim
- **35.** [Foydalanuvchi, guruh, huquqlar, token va SSO (Users, Permissions and Tokens)](35-foydalanuvchi-guruh-huquqlar-token-va-sso.md) - 12 bo'lim

### IX. Kengaytirish va integratsiya

- **36.** [Web API va avtomatlashtirish (Web API and Automation)](36-web-api-va-avtomatlashtirish.md) - 12 bo'lim
- **37.** [Taint analysis mexanikasi: source, sink, sanitizer (Taint Analysis Mechanics)](37-taint-analysis-mexanikasi-source-sink.md) - 13 bo'lim
- **38.** [Ko'p tilli loyiha: SQL, XML, YAML, Docker, Kubernetes, frontend (Multi-language Projects)](38-kop-tilli-loyiha-sql-xml-yaml-docker.md) - 13 bo'lim
- **39.** [Bog'liqlik zaifliklari va litsenziya tekshiruvi (Dependency Risk and Licences)](39-bogliqlik-zaifliklari-va-litsenziya.md) - 13 bo'lim
- **40.** [Sonar va boshqa vositalar: qachon qaysi biri (Sonar and Other Tools)](40-sonar-va-boshqa-vositalar-qachon-qaysi-biri.md) - 12 bo'lim

### X. Amaliy ma'lumotnoma

- **41.** [Lombok, record va generatsiya qilingan kod (Lombok, Records and Generated Code)](41-lombok-record-va-generatsiya-qilingan-kod.md) - 13 bo'lim
- **42.** [Diagnostika: tahlil ishlamaganda nima qilish (Troubleshooting)](42-diagnostika-tahlil-ishlamaganda-nima-qilish.md) - 17 bo'lim
- **43.** [Tezkor ma'lumotnoma: parametrlar, buyruqlar, glossariy (Quick Reference and Glossary)](43-tezkor-malumotnoma-parametrlar-buyruqlar.md) - 15 bo'lim

---

[&larr; Barcha hujjatlar](../../README.md)
