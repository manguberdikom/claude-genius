# Toza kod yozuvchining qoidalari: Java, Spring, PostgreSQL

Bu hujjat toza kodning **qoidalar to'plami**. Arxitektura qarorlari, pattern katalogi va
test texnikasi boshqa hujjatlarda turadi; bu yerda faqat bitta savolga javob beriladi:
klaviatura ostida tug'ilayotgan shu qator toza yoki yo'q.

Hujjat oltilikning bir qismi, har biri boshqa savolga javob beradi:

- [Dizayn patternlar](../patterns/README.md) - pattern katalogi, SOLID va GRASP printsiplari, 83 ta anti-pattern.
- [Arxitektor miyasi](../architect/README.md) - qaror, abstraksiya, chegara, murakkablik, JVM va PostgreSQL mexanikasi.
- [Testlash qo'llanmasi](../testing/README.md) - test strategiyasi, piramida, Testcontainers, CI pipeline.
- [SonarQube](../sonarqube/README.md) - statik tahlil, quality gate, coverage, Sonar xato katalogi.
- [Kod review](../code-review/README.md) - diffni o'qish, review stolida nimani ko'rish va nimani to'xtatish.

Shu hujjatlar bir xil bilimga turli tomondan qaraydi: [review hujjati](../code-review/README.md) "diffda nimani
ko'rasiz" degan savolga javob beradi, bu hujjat esa "shu qatorni qanday yozasiz" degan
savolga.

Arxitektor va pattern hujjatlarida yoritilgan mavzular bu yerda qayta yozilmaydi, faqat
nomi bilan havola qilinadi: masalan nomni domen tilidan olish, kognitiv yuk, erta qaytish,
izohning "nega" qoidasi, SOLID, GRASP, DRY, KISS, YAGNI, Demeter qonuni, God Object va
qolgan anti-patternlar.

Bu yerda ularning **qolgan qismi** bor: nomlashning to'liq qoidalar to'plami, funksiya va
argument qoidalari, shart va sikl gigiyenasi, izohlarning to'liq katalogi, formatlash,
obyekt shartnomalari, xato bilan ishlash, Java va Spring kodining mayda qoidalari, test
kodining tozaligi, hid va refaktoring kataloglari, kod bazasi gigiyenasi va professional
intizom.

Har bob `Amalda qo'llash` tekshiruv ro'yxati bilan tugaydi. Oxirgi ikki bob tezkor
ma'lumotnoma va o'z-o'zini baholash uchun.


**Versiya bazasi:** Java 21 LTS (pol: 17, Java 25 eslatmalari bilan), Spring Boot 3.2-3.5 (4.0 eslatmalari bilan), PostgreSQL 16+ (15-18 havolalari bilan), JUnit 5.

## Mundarija

### I. Toza kodning asosi

- **1.** [Toza kod nima va nega qimmat (What Clean Code Is)](01-toza-kod-nima-va-nega-qimmat.md) - 10 bo'lim
- **2.** [Nomlash qoidalari: maqsadni ochib beruvchi nom (Naming: Intention-Revealing Names)](02-nomlash-qoidalari-maqsadni-ochib-beruvchi.md) - 16 bo'lim
- **3.** [Nom turlari bo'yicha aniq konvensiyalar (Naming Conventions by Kind)](03-nom-turlari-boyicha-aniq-konvensiyalar.md) - 16 bo'lim

### II. Funksiya va boshqaruv oqimi

- **4.** [Funksiya: kichiklik va bitta ish (Functions: Small and Doing One Thing)](04-funksiya-kichiklik-va-bitta-ish.md) - 11 bo'lim
- **5.** [Funksiya argumentlari (Function Arguments)](05-funksiya-argumentlari.md) - 12 bo'lim
- **6.** [Shart, mantiq va boshqaruv oqimi (Conditionals and Control Flow)](06-shart-mantiq-va-boshqaruv-oqimi.md) - 11 bo'lim
- **7.** [Sikl, iteratsiya va to'plam bilan ishlash (Loops and Iteration)](07-sikl-iteratsiya-va-toplam-bilan-ishlash.md) - 10 bo'lim

### III. Izoh va hujjat

- **8.** [Izoh qoidalari: yaxshi izohlar (Comments: The Good Ones)](08-izoh-qoidalari-yaxshi-izohlar.md) - 10 bo'lim
- **9.** [Yomon izohlar katalogi (Comments: The Bad Ones)](09-yomon-izohlar-katalogi.md) - 13 bo'lim
- **10.** [Javadoc va API hujjati (Javadoc and API Documentation)](10-javadoc-va-api-hujjati.md) - 11 bo'lim

### IV. Formatlash va kod uslubi

- **11.** [Vertikal formatlash (Vertical Formatting)](11-vertikal-formatlash.md) - 10 bo'lim
- **12.** [Gorizontal formatlash va kod uslubi (Horizontal Formatting and Style)](12-gorizontal-formatlash-va-kod-uslubi.md) - 11 bo'lim
- **13.** [Formatlashni avtomatlashtirish va diff gigiyenasi (Automated Formatting and Diff Hygiene)](13-formatlashni-avtomatlashtirish-va-diff.md) - 9 bo'lim

### V. Obyekt, ma'lumot va holat

- **14.** [Obyekt va ma'lumot tuzilmasi: inkapsulyatsiya (Objects vs Data Structures)](14-obyekt-va-malumot-tuzilmasi-inkapsulyatsiya.md) - 11 bo'lim
- **15.** [Tenglik, hash va obyekt shartnomalari (Equality, Hashing and Object Contracts)](15-tenglik-hash-va-obyekt-shartnomalari.md) - 11 bo'lim
- **16.** [O'zgarmaslik va holat boshqaruvi kod darajasida (Immutability in Code)](16-ozgarmaslik-va-holat-boshqaruvi-kod.md) - 10 bo'lim
- **17.** [Vorislik, kompozitsiya va polimorfizm mexanikasi (Inheritance Mechanics)](17-vorislik-kompozitsiya-va-polimorfizm.md) - 10 bo'lim

### VI. Xato bilan ishlash

- **18.** [Xato bilan ishlash qoidalari (Error Handling Rules)](18-xato-bilan-ishlash-qoidalari.md) - 11 bo'lim
- **19.** [Istisno mexanikasi va resurslar (Exception Mechanics and Resources)](19-istisno-mexanikasi-va-resurslar.md) - 12 bo'lim

### VII. Java tilining toza ishlatilishi

- **20.** [Primitiv, son va pul (Primitives, Numbers and Money)](20-primitiv-son-va-pul.md) - 9 bo'lim
- **21.** [Satr, matn va regex (Strings, Text and Regex)](21-satr-matn-va-regex.md) - 10 bo'lim
- **22.** [Sana, vaqt va mintaqa (Date, Time and Zone)](22-sana-vaqt-va-mintaqa.md) - 10 bo'lim
- **23.** [To'plamlar va generiklar gigiyenasi (Collections and Generics)](23-toplamlar-va-generiklar-gigiyenasi.md) - 12 bo'lim
- **24.** [Lambda, oqim va funksional uslub tozaligi (Lambdas and Streams)](24-lambda-oqim-va-funksional-uslub-tozaligi.md) - 10 bo'lim
- **25.** [Java kodidagi umumiy tuzoqlar (Common Java Pitfalls)](25-java-kodidagi-umumiy-tuzoqlar.md) - 11 bo'lim

### VIII. Spring va ma'lumot qatlamida toza kod

- **26.** [Spring kodining tozaligi (Clean Code in Spring)](26-spring-kodining-tozaligi.md) - 11 bo'lim
- **27.** [REST API kodining o'qilishi (Readable REST Code)](27-rest-api-kodining-oqilishi.md) - 9 bo'lim
- **28.** [JPA va SQL kodining tozaligi (Clean JPA and SQL)](28-jpa-va-sql-kodining-tozaligi.md) - 10 bo'lim
- **29.** [Log kodining tozaligi (Clean Logging Code)](29-log-kodining-tozaligi.md) - 10 bo'lim

### IX. Test kodining tozaligi

- **30.** [Test kodi ham ishlab chiqarish kodi (Test Code Is Production Code)](30-test-kodi-ham-ishlab-chiqarish-kodi.md) - 10 bo'lim
- **31.** [TDD intizomi va kod dizayniga ta'siri (TDD Discipline)](31-tdd-intizomi-va-kod-dizayniga-tasiri.md) - 8 bo'lim

### X. Hid katalogi va refaktoring harakatlari

- **32.** [Kod hidlari katalogi I: nom, funksiya, ma'lumot (Code Smells I)](32-kod-hidlari-katalogi-i-nom-funksiya-malumot.md) - 15 bo'lim
- **33.** [Kod hidlari katalogi II: sinf, ierarxiya, bog'liqlik (Code Smells II)](33-kod-hidlari-katalogi-ii-sinf-ierarxiya.md) - 17 bo'lim
- **34.** [Toza kod evristikalarining to'liq ro'yxati (Clean Code Heuristics)](34-toza-kod-evristikalarining-toliq-royxati.md) - 11 bo'lim
- **35.** [Refaktoring harakatlari katalogi I: funksiya va o'zgaruvchi (Refactoring Moves I)](35-refaktoring-harakatlari-katalogi-i-funksiya.md) - 21 bo'lim
- **36.** [Refaktoring harakatlari katalogi II: ma'lumot va inkapsulyatsiya (Refactoring Moves II)](36-refaktoring-harakatlari-katalogi-ii-malumot.md) - 16 bo'lim
- **37.** [Refaktoring harakatlari katalogi III: shart, API va ierarxiya (Refactoring Moves III)](37-refaktoring-harakatlari-katalogi-iii-shart.md) - 17 bo'lim
- **38.** [Refaktoringni xavfsiz bajarish (Safe Refactoring Mechanics)](38-refaktoringni-xavfsiz-bajarish.md) - 9 bo'lim

### XI. Kod bazasi va jarayon gigiyenasi

- **39.** [Bir qadamli build va mahalliy qaytish halqasi (One-Step Build)](39-bir-qadamli-build-va-mahalliy-qaytish.md) - 9 bo'lim
- **40.** [Versiya nazorati gigiyenasi (Version Control Hygiene)](40-versiya-nazorati-gigiyenasi.md) - 9 bo'lim
- **41.** [O'zgarishni kiritish jarayoni: kichik qadamlar (Working in Small Steps)](41-ozgarishni-kiritish-jarayoni-kichik-qadamlar.md) - 9 bo'lim
- **42.** [Statik tahlil va avtomatik qoidalar (Static Analysis and Automated Rules)](42-statik-tahlil-va-avtomatik-qoidalar.md) - 8 bo'lim

### XII. Professional intizom

- **43.** [Professional mas'uliyat (Professionalism)](43-professional-masuliyat.md) - 6 bo'lim
- **44.** ["Yo'q" va "ha" deyish: majburiyat tili (Saying No and Saying Yes)](44-yoq-va-ha-deyish-majburiyat-tili.md) - 6 bo'lim
- **45.** [Baholash, muddat va bosim (Estimation, Deadlines and Pressure)](45-baholash-muddat-va-bosim.md) - 8 bo'lim
- **46.** [Vaqt, diqqat va mashq (Time, Focus and Practice)](46-vaqt-diqqat-va-mashq.md) - 9 bo'lim
- **47.** [Birgalikda ishlash va o'rgatish (Collaboration and Mentoring)](47-birgalikda-ishlash-va-orgatish.md) - 6 bo'lim

### XIII. Ma'lumotnoma

- **48.** [Tezkor ma'lumotnoma: qoidalar va tekshiruv ro'yxatlari (Quick Reference)](48-tezkor-malumotnoma-qoidalar-va-tekshiruv.md) - 12 bo'lim
- **49.** [O'z-o'zini baholash: toza kod yetukligi (Self-Assessment)](49-oz-ozini-baholash-toza-kod-yetukligi.md) - 10 bo'lim

---

[&larr; Barcha hujjatlar](../../README.md)
