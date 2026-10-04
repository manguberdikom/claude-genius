---
name: sonarqube-fix
description: Fix a SonarQube finding or pass a quality gate in a Java/Spring/PostgreSQL project - bug, vulnerability, code smell, security hotspot, cognitive complexity, duplication, coverage and branch coverage, JaCoCo wiring, exclusions, false positives, mutation testing, PR decoration, taint analysis, server setup and troubleshooting. Use when Sonar reports an issue or rule key (java:Sxxxx), a quality gate fails, coverage is below threshold, the user asks how to reach 100%, how to suppress or exclude something, or why the scanner produced no results.
---

# SonarQube: issue tuzatish va gate'dan o'tish

43 bob, 557 bo'lim. To'liq hujjat: `docs/sonarqube/README.md`.
Atamalar: `docs/sonarqube/43-tezkor-malumotnoma-parametrlar-buyruqlar.md#4314-glossariy`.

## Qoida

Sonar issue'si - bug hisoboti, uni yopish usuli emas. Tartib:

1. **Qoidani o'qing**, kalitidan boshlab (`java:S2259`). Qoida nimani
   taqiqlayotganini tushunmasdan tuzatmang.
2. **Haqiqiy xatomi yoki false positive**mi - ajratib oling
   (`docs/sonarqube/24-false-positive-suppression-va-oz-qoidangiz.md`).
3. **Kodni tuzatib** yopish birinchi variant. `@SuppressWarnings` va
   exclusion - oxirgi chora, har biri izoh va sabab bilan.
4. Coverage yetmasa, **test yozing**, exclusion qo'shmang. Halol va
   nohalol exclusion farqi: 12-bob.

100% coverage sifatni kafolatlamaydi - mutation testing buni ko'rsatadi
(`docs/sonarqube/20-mutation-testing-100-coverage-qachon-yolgon.md`).

## Vazifa - bob jadvali

| Vazifa | Bob fayli |
|---|---|
| Tahlil qanday ishlaydi, scanner nima yuboradi | `docs/sonarqube/01-sonarqube-arxitekturasi-va-tahlil-oqimi.md`, `docs/sonarqube/02-scanner-nimani-yigadi-va-qanday-yuboradi.md` |
| Issue turi, qoida, profil, severity ma'nosi | `docs/sonarqube/03-issue-turlari-bug-vulnerability-code-smell.md`, `docs/sonarqube/04-rule-quality-profile-va-severity.md` |
| Rating, texnik qarz, murakkablik, takrorlanish metrikalari | `docs/sonarqube/05-metrikalar-rating-texnik-qarz-murakkablik.md` |
| Quality gate shartlari va nega ERROR bo'ldi | `docs/sonarqube/06-quality-gate-mexanikasi-va-shartlari.md`, `docs/sonarqube/08-100-ga-sozlangan-gate-har-bir-shart-nimani.md` |
| New code, clean as you code, referens branch | `docs/sonarqube/07-yangi-kod-new-code-va-clean-as-you-code.md` |
| JaCoCo mexanikasi, Maven/Gradle ulash, agent sozlash | `docs/sonarqube/09-coverage-qanday-olchanadi-jacoco-mexanikasi.md`, `docs/sonarqube/10-jacoco-va-sonarqube-ulanishi-maven-va.md` |
| Qamralmaydigan kod (konfiguratsiya, DTO, exception) uchun test | `docs/sonarqube/11-qamralmay-qoladigan-kod-va-unga-test-yozish.md` |
| Exclusion: nimani chiqarish halol | `docs/sonarqube/12-exclusion-nimani-chiqarish-halol-nimani.md` |
| Sonar o'tadigan kod yozish qoidalari | `docs/sonarqube/13-sonar-otadigan-kod-yozish-qoidalari.md` |
| Java/Spring da eng ko'p uchraydigan issue va yechimi | `docs/sonarqube/14-java-va-spring-da-eng-kop-uchraydigan-issue.md` |
| Cognitive complexity va takrorlanishni kamaytirish | `docs/sonarqube/15-cognitive-complexity-va-takrorlanishni.md` |
| Security hotspot va vulnerability tekshirish | `docs/sonarqube/16-security-hotspot-va-vulnerability.md` |
| Sonar talablarini qondiradigan test, branch qamrovi | `docs/sonarqube/17-sonar-talablarini-qondiradigan-test-yozish.md`, `docs/sonarqube/18-branch-va-shart-qamrovini-toliq-yopish.md` |
| Test kodining o'zidagi Sonar qoidalari | `docs/sonarqube/19-testning-ozidagi-sonar-qoidalari-va-test.md` |
| CI/CD ga ulash, PR decoration, blokirovka | `docs/sonarqube/21-ci-cd-ga-ulash-pr-decoration-va-blokirovka.md` |
| Lokal tekshirish, IDE, sonar-scanner | `docs/sonarqube/22-lokal-tekshirish-ide-sonar-scanner-va-tez.md` |
| Legacy loyihani 100% ga olib chiqish rejasi | `docs/sonarqube/23-legacy-loyihani-100-ga-olib-chiqish-rejasi.md` |
| **Xato katalogi** - qoida kalitidan yechimga | 25-30 boblar (quyida) |
| Server o'rnatish, yangilash, huquqlar, Web API | 32-36 boblar |
| Taint analysis, ko'p tilli loyiha, bog'liqlik zaifliklari | `docs/sonarqube/37-taint-analysis-mexanikasi-source-sink.md`, `docs/sonarqube/38-kop-tilli-loyiha-sql-xml-yaml-docker.md`, `docs/sonarqube/39-bogliqlik-zaifliklari-va-litsenziya.md` |
| Lombok, record, generatsiya qilingan kod | `docs/sonarqube/41-lombok-record-va-generatsiya-qilingan-kod.md` |
| Tahlil ishlamadi, natija yo'q, 0 fayl indekslandi | `docs/sonarqube/42-diagnostika-tahlil-ishlamaganda-nima-qilish.md` |

## Xato katalogi

Issue toifasiga qarab:

| Toifa | Fayl |
|---|---|
| Reliability (bug): NPE, resurs oqishi, noto'g'ri solishtirish | `docs/sonarqube/25-xato-katalogi-reliability-bug-toifasi.md` |
| Security: injection, crypto, sirlar, hotspot | `docs/sonarqube/26-xato-katalogi-security-vulnerability-va.md` |
| Maintainability: tuzilish va murakkablik | `docs/sonarqube/27-xato-katalogi-maintainability-tuzilish-va.md` |
| Maintainability: nomlash, o'lik kod, uslub | `docs/sonarqube/28-xato-katalogi-maintainability-nomlash-olik.md` |
| Spring, JPA va PostgreSQL ga xos xatolar | `docs/sonarqube/29-xato-katalogi-spring-jpa-va-postgresql-ga.md` |
| Test kodidagi xatolar | `docs/sonarqube/30-xato-katalogi-test-kodidagi-xatolar.md` |
| Oldini olish checklisti | `docs/sonarqube/31-xatolarga-tushmaslik-uchun-yakuniy.md` |
