# Kod review: diffni o'qish, xatoni ko'rish, qarorni tekshirish

Bu hujjat kod review ni alohida muhandislik sohasi sifatida ko'radi. Savol bitta:
oldingizda diff turibdi, unda nimani ko'rasiz, nimani so'raysiz va nimani to'xtatasiz.
Tayanch stek: Java, Spring va PostgreSQL.

Hujjat oltilikning bir qismi va qolganlari bilan kesishmaydi:

- pattern katalogi - [Dizayn patternlar](../patterns/README.md)
- test yozish texnikasi - [Testlash qo'llanmasi](../testing/README.md)
- JVM, Spring va PostgreSQL ichki mexanikasi - [Arxitektor miyyasi](../architect/README.md)
- statik tahlil qoidalari va quality gate - [SonarQube](../sonarqube/README.md)
- toza kod qoidalari - [Toza kod qoidalari](../clean-code/README.md)

Bu yerda ularning bilimi review stoliga olib chiqiladi: qaysi mexanika diffda qanday
belgi qoldiradi, va shu belgini ko'rgan reviewer nima deyishi kerak. Mexanikaning
o'zi kerak bo'lsa, tegishli hujjatga mavzu nomi bilan havola qilinadi.

Hujjat kimga: kod yozadigan arxitektor, tech lead, review ga kuniga vaqt ajratadigan
senior va o'z PR ini review dan o'tkazishni o'rganmoqchi bo'lgan developer.

Har bob oxirida `Amalda qo'llash` ro'yxati bor: loyihada darhol bajariladigan bandlar.
Review izohlari uchun tayyor iboralar oxirgi bobda.


**Versiya bazasi:** Java 21 LTS (pol: 17, Java 25 eslatmalari bilan), Spring Boot 3.2-3.5 (4.0 eslatmalari bilan), PostgreSQL 16+ (15-18 havolalari bilan), JUnit 5.

## Mundarija

### I. Review ning mohiyati va iqtisodi

- **1.** [Review nima uchun bor va nimani haqiqatda beradi (Why Review Exists)](01-review-nima-uchun-bor-va-nimani-haqiqatda.md) - 11 bo'lim
- **2.** [Review iqtisodi: xato narxi, navbat va PR hajmi (The Economics of Review)](02-review-iqtisodi-xato-narxi-navbat-va-pr.md) - 11 bo'lim
- **3.** [Reviewer ning tahlil apparati: niyat, invariant, xavf yuzasi (The Reviewer's Analytical Apparatus)](03-reviewer-ning-tahlil-apparati-niyat.md) - 11 bo'lim
- **4.** [Diffni o'qish mexanikasi (Reading a Diff)](04-diffni-oqish-mexanikasi.md) - 11 bo'lim
- **5.** [Mashina va odam: SonarQube dan oldin topish (Beating the Tools)](05-mashina-va-odam-sonarqube-dan-oldin-topish.md) - 11 bo'lim

### II. Arxitektura, dizayn va clean code review

- **6.** [Arxitektura review: qatlam, chegara, bog'liqlik yo'nalishi (Architecture in a Diff)](06-arxitektura-review-qatlam-chegara-bogliqlik.md) - 11 bo'lim
- **7.** [Bog'liqlik, koheziya va abstraksiya review (Coupling, Cohesion, Abstraction)](07-bogliqlik-koheziya-va-abstraksiya-review.md) - 11 bo'lim
- **8.** [Clean code review: nomlash, kognitiv yuk, metod shakli (Clean Code at the Review Table)](08-clean-code-review-nomlash-kognitiv-yuk.md) - 11 bo'lim
- **9.** [SOLID va dizayn printsiplarini diffda tekshirish (Principles, Not Slogans)](09-solid-va-dizayn-printsiplarini-diffda.md) - 11 bo'lim
- **10.** [Dizayn pattern review I: yo'q patternni ko'rish (Missing Patterns)](10-dizayn-pattern-review-i-yoq-patternni-korish.md) - 12 bo'lim
- **11.** [Dizayn pattern review II: noto'g'ri va ortiqcha qo'llangan pattern (Misapplied and Over-Applied Patterns)](11-dizayn-pattern-review-ii-notogri-va.md) - 12 bo'lim
- **12.** [Code smell va anti-pattern katalogi diffda (Smells in a Diff)](12-code-smell-va-anti-pattern-katalogi-diffda.md) - 11 bo'lim
- **13.** [Domen modeli review: invariant, agregat, chegara (Reviewing the Domain Model)](13-domen-modeli-review-invariant-agregat.md) - 11 bo'lim

### III. Java kodini chuqur tahlil

- **14.** [Java tili darajasidagi xatolar katalogi (Language-Level Defects)](14-java-tili-darajasidagi-xatolar-katalogi.md) - 11 bo'lim
- **15.** [Holat, mutability va concurrency review (State and Concurrency)](15-holat-mutability-va-concurrency-review.md) - 12 bo'lim
- **16.** [Resurs, xotira va GC bosimi review (Resources and Memory)](16-resurs-xotira-va-gc-bosimi-review.md) - 10 bo'lim
- **17.** [Zamonaviy Java review: record, sealed, pattern matching, virtual thread (Modern Java)](17-zamonaviy-java-review-record-sealed-pattern.md) - 8 bo'lim

### IV. Spring kodini review qilish

- **18.** [Bean, kontekst va proxy mexanikasi review (Beans, Context and Proxies)](18-bean-kontekst-va-proxy-mexanikasi-review.md) - 10 bo'lim
- **19.** [Tranzaksiya chegarasi review (Transaction Boundaries)](19-tranzaksiya-chegarasi-review.md) - 11 bo'lim
- **20.** [Web qatlami review: DTO, validatsiya, xato javobi (The Web Layer)](20-web-qatlami-review-dto-validatsiya-xato.md) - 12 bo'lim
- **21.** [Konfiguratsiya, profil va feature flag review (Configuration)](21-konfiguratsiya-profil-va-feature-flag-review.md) - 10 bo'lim
- **22.** [Tashqi integratsiya review: timeout, retry, broker (Outbound Integration)](22-tashqi-integratsiya-review-timeout-retry.md) - 9 bo'lim

### V. PostgreSQL va ma'lumot qatlami review

- **23.** [JPA va Hibernate review (JPA and Hibernate)](23-jpa-va-hibernate-review.md) - 11 bo'lim
- **24.** [SQL, so'rov rejasi va indeks review (SQL, Plans and Indexes)](24-sql-sorov-rejasi-va-indeks-review.md) - 10 bo'lim
- **25.** [Migratsiya review: qulf, backfill, orqaga moslik (Reviewing Migrations)](25-migratsiya-review-qulf-backfill-orqaga.md) - 9 bo'lim
- **26.** [Ma'lumot to'g'riligi va turlar review (Data Correctness)](26-malumot-togriligi-va-turlar-review.md) - 10 bo'lim
- **27.** [Izolyatsiya, poyga holatlari va xabar yetkazish (Isolation, Races and Delivery)](27-izolyatsiya-poyga-holatlari-va-xabar.md) - 11 bo'lim

### VI. Xavfsizlik review

- **28.** [Xavfsizlik review metodikasi (How to Review for Security)](28-xavfsizlik-review-metodikasi.md) - 8 bo'lim
- **29.** [Injection review: SQL va boshqalar (Injection)](29-injection-review-sql-va-boshqalar.md) - 10 bo'lim
- **30.** [Autentifikatsiya va avtorizatsiya review (Authentication and Authorization)](30-autentifikatsiya-va-avtorizatsiya-review.md) - 10 bo'lim
- **31.** [Kirish va chiqish xavfsizligi: SSRF, deserializatsiya, fayllar (Input and Output Safety)](31-kirish-va-chiqish-xavfsizligi-ssrf.md) - 8 bo'lim
- **32.** [Secret, maxfiy ma'lumot va kriptografiya review (Secrets, PII and Crypto)](32-secret-maxfiy-malumot-va-kriptografiya.md) - 9 bo'lim
- **33.** [Bog'liqlik va supply chain review (Dependencies and Supply Chain)](33-bogliqlik-va-supply-chain-review.md) - 7 bo'lim

### VII. Test review

- **34.** [Test to'liqligini review qilish (Test Case Completeness)](34-test-toliqligini-review-qilish.md) - 11 bo'lim
- **35.** [Test sifati review: assertion, izolyatsiya, beqarorlik (Test Quality)](35-test-sifati-review-assertion-izolyatsiya.md) - 10 bo'lim
- **36.** [Test turi va integratsion test review (Test Types and Integration Tests)](36-test-turi-va-integratsion-test-review.md) - 9 bo'lim

### VIII. Kesishgan sifat

- **37.** [API moslik va breaking change review (API Compatibility)](37-api-moslik-va-breaking-change-review.md) - 9 bo'lim
- **38.** [Performance review diffdan (Performance from a Diff)](38-performance-review-diffdan.md) - 10 bo'lim
- **39.** [Observability review (Observability)](39-observability-review.md) - 9 bo'lim

### IX. Jarayon, madaniyat va o'lchov

- **40.** [Review jarayonini qurish (Building the Process)](40-review-jarayonini-qurish.md) - 12 bo'lim
- **41.** [Review madaniyati, til va kelishmovchilik (Culture, Language, Disagreement)](41-review-madaniyati-til-va-kelishmovchilik.md) - 15 bo'lim
- **42.** [Review metrikalari (Measuring Review)](42-review-metrikalari.md) - 8 bo'lim
- **43.** [AI yozgan kodni review qilish va AI bilan review qilish (Reviewing AI-Generated Code)](43-ai-yozgan-kodni-review-qilish-va-ai-bilan.md) - 9 bo'lim
- **44.** [Shablonlar, checklistlar va reviewer yetukligi (Templates and Maturity)](44-shablonlar-checklistlar-va-reviewer.md) - 9 bo'lim

---

[&larr; Barcha hujjatlar](../../README.md)
