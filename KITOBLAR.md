# Manbalar ro'yxati: to'liq

Korpus 224 bob. Shundan 141 bob ortida kitob yo'q, 10 bob esa bor
kitoblar bilan yopilmaydi. Bu ro'yxat ikkisini ham qamraydi va yangi
boblar uchun kerak bo'ladiganini ham qo'shadi.

Tartib: avval bepul va qonuniy manbalar, keyin pullik kitoblar
foydasi bo'yicha. Ruxsatsiz nusxa ishlatilmaydi.

Hozirgi holat: 13 kitob bor (`docs/BOOKS.tsv`), 3 to'plam bepul hujjat
`books` repoga qo'yilgan (`docs/postgresql/`, `docs/owasp/`,
`docs/spring/`).

## 0. Bepul, qonuniy, bugun olinadi

Sessiya proksisi ko'p hostni to'sadi, `raw.githubusercontent.com` esa
ochiq. Shu sababli ikki ustun: men ola oladiganlari va siz brauzerda
olishingiz kerak bo'lganlari.

### 0.1 Men ola oladiganlar (GitHub da)

| Manba | Bob | Holat |
|---|---|---|
| PostgreSQL 17 qo'llanmasi (SGML) | architect 21-27, code-review 24-27 | olingan |
| OWASP Cheat Sheet Series | code-review 28-33, patterns 18 | olingan, 9 varaq |
| Spring Framework reference (AsciiDoc) | architect 15-20, clean-code 26-29 | olingan, 3 sahifa |
| Spring Boot reference | architect 16, clean-code 26 | olingan |
| Spring Security reference (tag 6.3.0) | architect 20 | olingan |
| Elasticsearch reference (tag v8.15.0) | architect 40 | olingan |
| Kubernetes website hujjati | architect 31, patterns 29 | olingan |
| sonar-java rule metadata | sonarqube 1-43 | `tools/sonar_rules.tsv` da bor |
| Hibernate ORM user guide (tag 6.6.0) | architect 18, code-review 23 | olingan |
| JUnit 5 (tag r5.11.0), Mockito, AssertJ, Testcontainers | testing 5-8 | olingan |
| Google Java Style Guide | clean-code 12, 13 | olingan |
| ArchUnit, PIT, jqwik | testing 14, 5.11, sonarqube 20 | olingan |
| Caffeine, Micrometer, SLF4J, SpotBugs | architect 28, 30, clean-code 29, 42 | olingan |
| async-profiler | architect 14 | olingan |
| Spring AI reference | patterns 30 | olingan |
| OpenJDK manba kodi (tagga qadalgan) | architect 9, 11, 12 | yo'li tekshirilgan, kerak bo'lganda olinadi |
| SLSA, GitHub Actions, Gradle, Checkstyle, Error Prone, k6 | code-review 33, testing 13, 15, clean-code 39, 42 | `raw` da yo'li boshqacha, olinmadi |
| Google *eng-practices* (review qo'llanmasi) | code-review 1, 4, 40, 41 | olinadi |
| *Pro Git* (Chacon, Straub) | clean-code 40, 41 | olinadi, to'liq kitob ochiq litsenziyada |
| OpenTelemetry spetsifikatsiyasi | architect 30.8, patterns 21.4 | olinadi |
| OpenAPI spetsifikatsiyasi | patterns 7.28, code-review 37 | olinadi |
| Project Reactor hujjati | patterns 19, architect 17 | olinadi |
| ArchUnit, PIT, jqwik hujjatlari | testing 14, sonarqube 20, testing 5.11 | olinadi |
| Micrometer va Logback hujjatlari | architect 30, clean-code 29 | olinadi |
| Maven, Gradle, GitHub Actions hujjatlari | clean-code 39, testing 15, sonarqube 21 | olinadi |
| SEI CERT Oracle Coding Standard for Java | code-review 28-33 | siz olasiz, hosti yopiq |
| RFC 9110, 9457, 6749, 7519 (HTTP, ProblemDetail, OAuth 2, JWT) | architect 17.6, 17.8, 20.6 | siz olasiz, hosti yopiq |

### 0.2 Siz olishingiz kerak (hosti proksida yopiq)

| Manba | Bob | Qayerdan |
|---|---|---|
| Egor Rogov, *PostgreSQL Internals* | architect 21-24, 27 | `postgrespro.com/community/books/internals` |
| JLS va JVMS (PDF) | architect 9, clean-code til boblari | `docs.oracle.com/javase/specs` |
| OpenJDK JEP lari | architect 12, 13 | `openjdk.org/jeps` |
| Google *SRE Book* va *SRE Workbook* | architect 35, 37, testing 17 | `sre.google/books` |
| *Kubernetes Patterns* (Ibryam, Huss) | patterns 29, 22 | Red Hat developers |
| *Observability Engineering* (Majors va boshq.) | architect 30, patterns 21 | Honeycomb |
| C4 model hujjati | yangi "arxitekturani hujjatlash" bobi | `c4model.com` |
| ISTQB Foundation sillabusi | testing 4 | `istqb.org` |
| DORA / *Accelerate* hisobotlari | testing 17, architect 37 | `dora.dev` |

## 1. Majburiy o'n bir: eng ko'p bob yopadigani

Pul cheklangan bo'lsa, shu tartibda olinadi.

| # | Kitob | Bob | Nega almashtirib bo'lmaydi |
|---|---|---|---|
| 1 | Gamma, Helm, Johnson, Vlissides, *Design Patterns* (GoF, 1994) | patterns 1, 2, 3; code-review 10, 11 | `patterns` hujjatining 1-3 boblari to'liq uning nomlariga tayanadi. Head First uni pedagogik qaytaradi, lekin uy manbasi emas |
| 2 | Martin Fowler, *Patterns of Enterprise Application Architecture* | patterns 8, 9, 10, 11 | Korpus uning nomlarini ishlatadi: Data Mapper, Unit of Work, Identity Field, Serialized LOB, Lazy Load, Offline Lock. Uy manbasi shu |
| 3 | Martin Fowler, *Refactoring* 2-nashr | clean-code 32, 33, 35, 36, 37, 38, architect 34, code-review 12 | Hid va refaktoring harakatlari katalogi: 8 bob to'g'ridan-to'g'ri shunga tayanadi |
| 4 | Winters, Manshreck, Wright, *Software Engineering at Google* | code-review 1, 2, 40, 41, 42, 44, testing 1, 3, 15, 16 | Review iqtisodi, jarayoni va madaniyati bo'yicha eng o'lchangan manba |
| 5 | Michael Nygard, *Release It!* 2-nashr | patterns 17, architect 7, 32 | Circuit Breaker, Bulkhead, Steady State, Handshaking nomlarining manbasi |
| 6 | Gregor Hohpe, Bobby Woolf, *Enterprise Integration Patterns* | patterns 15, 16 | Message Channel, Splitter, Aggregator, Dead Letter Channel manbasi |
| 7 | Gerard Meszaros, *xUnit Test Patterns* | patterns 23, testing 10, 16, 18, code-review 35 | Test Double taksonomiyasi, Object Mother, test hidlari |
| 8 | Vlad Mihalcea, *High-Performance Java Persistence* | architect 18, code-review 23, clean-code 28, patterns 9 | JPA va Hibernate xatti-harakatining o'lchangan tahlili |
| 9 | Steve McConnell, *Code Complete* 2-nashr | code-review 3, 4, 8, 12, clean-code 4, 5, 6, 11 | Konstruksiya bo'yicha eng ko'p empirik ma'lumotga tayangan kitob |
| 10 | Michael Feathers, *Working Effectively with Legacy Code* | architect 34, clean-code 38, testing 1 | Tikuv (seam) tushunchasi korpusda ishlatiladi, manbasi shu |
| 11 | Brendan Gregg, *Systems Performance* 2-nashr | architect 8, 14, 31, code-review 38 | USE metodikasi va o'lchov tartibi: performance boblarining asosi |

## 2. Soha bo'yicha to'liq ro'yxat

### 2.1 Arxitektura va dizayn

| Kitob | Bob |
|---|---|
| Ford, Richards, Sadalage, Dehghani, *Software Architecture: The Hard Parts* | architect 5, patterns 14, 27 |
| Richards, Ford, *Fundamentals of Software Architecture* | architect 1, 2, 6, 36, 39 |
| Ford, Parsons, Kua, *Building Evolutionary Architectures* | testing 14, architect 33 |
| John Ousterhout, *A Philosophy of Software Design* | architect 5, 6, clean-code 4 |
| George Fairbanks, *Just Enough Software Architecture* | architect 1, 3 |
| Simon Brown, *Software Architecture for Developers* | yangi: arxitekturani hujjatlash (C4) |
| Clements va boshq., *Documenting Software Architectures* | yangi: hujjatlash ko'rinishlari |
| Skelton, Pais, *Team Topologies* | architect 36, 39, patterns 14.5 |
| Brendan Burns, *Designing Distributed Systems* | patterns 29, 22 |

### 2.2 Domen va mikroservis

| Kitob | Bob |
|---|---|
| Eric Evans, *Domain-Driven Design* | patterns 13, code-review 13 |
| Vaughn Vernon, *Implementing Domain-Driven Design* | patterns 13 |
| Vlad Khononov, *Learning Domain-Driven Design* | patterns 13, architect 2 |
| Sam Newman, *Building Microservices* 2-nashr | patterns 12, 14 |
| Sam Newman, *Monolith to Microservices* | patterns 27 |

### 2.3 Java va JVM

| Kitob | Bob |
|---|---|
| Scott Oaks, *Java Performance* 2-nashr | architect 8, 9, 10, 14, 28 |
| Evans, Gough, Newland, *Optimizing Java* | architect 9, 10, 14 |
| Evans, Clark, Verburg, *The Well-Grounded Java Developer* 2-nashr | architect 12, 13, patterns 24 |
| Urma, Fusco, Mycroft, *Modern Java in Action* | clean-code 24, patterns 24 |
| Horstmann, *Core Java* 1 va 2 jild | clean-code 20-25 (Schildt ga muqobil, qat'iyroq) |

### 2.4 Spring va persistence

| Kitob | Bob |
|---|---|
| Carnell, Sanchez, *Spring Microservices in Action* **2-nashr** | patterns 14, 17, 21, architect 16 |
| Spilca, *Spring Security in Action* **2-nashr** | architect 20, patterns 18 |
| Thomas Vitale, *Cloud Native Spring in Action* | architect 16, 31, patterns 22, 29 |
| Catalin Tudose, *Java Persistence with Spring Data and Hibernate* | architect 18, clean-code 28 |
| Mark Heckler, *Spring Boot: Up and Running* | architect 16 |

### 2.5 Ma'lumot va SQL

| Kitob | Bob |
|---|---|
| Bill Karwin, *SQL Antipatterns, Volume 1* | code-review 24-27, patterns 25 |
| Markus Winand, *SQL Performance Explained* | architect 23, 24 |
| Alex Petrov, *Database Internals* | architect 21, 23, 26 |
| Dimitri Fontaine, *The Art of PostgreSQL* | architect 24, 25 |
| Hans-Jurgen Schonig, *Mastering PostgreSQL* | architect 21, 27 |
| Reis, Housley, *Fundamentals of Data Engineering* | architect 26.13, yangi: analitik quvur |

### 2.6 Testlash

| Kitob | Bob |
|---|---|
| Freeman, Pryce, *Growing Object-Oriented Software, Guided by Tests* | testing 1, 5, clean-code 31 |
| Vladimir Khorikov, *Unit Testing: Principles, Practices and Patterns* | testing 1, 5, 6, 10, code-review 34-36 |
| Mauricio Aniche, *Effective Software Testing* | testing 1, 4, 13, 34 |
| Posta va boshq., *Testing Java Microservices* | testing 9, 12, patterns 23 |

### 2.7 Xavfsizlik

| Kitob | Bob |
|---|---|
| Manico, Detlefsen, *Iron-Clad Java* | code-review 28-32, patterns 18 |
| Richer, Sanso, *OAuth 2 in Action* | architect 20, patterns 18.12-18.17 |
| Tanya Janca, *Alice and Bob Learn Application Security* | code-review 28, testing 13 |
| Michal Zalewski, *The Tangled Web* | code-review 31, patterns 18.23, 18.24 |
| Jean-Philippe Aumasson, *Serious Cryptography* | code-review 32 |

### 2.8 Operatsion va SRE

| Kitob | Bob |
|---|---|
| Campbell, Majors, *Database Reliability Engineering* | architect 27, 33, 35 |
| Rosenthal, Jones, *Chaos Engineering* | patterns 17.38, testing 13 |
| John Allspaw, *The Art of Capacity Planning* | architect 8, yangi: sig'im rejalashtirish |
| Burns va boshq., *Kubernetes Up and Running* | architect 31, patterns 29 |
| Brendan Gregg, *BPF Performance Tools* | architect 14 (chuqur, ixtiyoriy) |

### 2.9 Kasb va jarayon

| Kitob | Bob |
|---|---|
| Hunt, Thomas, *The Pragmatic Programmer* (20 yillik nashr) | clean-code 1, 39, 40, 41, 46 |
| Robert C. Martin, *The Clean Coder* | clean-code 43, 44, 45, 46, 47 |
| Kent Beck, *Tidy First?* | clean-code 38, 41 |
| Humble, Farley, *Continuous Delivery* | testing 15, clean-code 39, 40 |
| Forsgren, Humble, Kim, *Accelerate* | testing 17, architect 37 |
| Camille Fournier, *The Manager's Path* | architect 36, 39 |
| Will Larson, *An Elegant Puzzle* | architect 36, 37 |

### 2.10 Yangi boblar uchun

| Kitob | Yangi bob |
|---|---|
| Turnbull, Berryman, *Relevant Search* | qidiruv tizimi: PostgreSQL FTS dan qachon chiqish |
| Nishant Bhajaria, *Data Privacy* | ma'lumot maxfiyligi va o'chirish talabi |
| Simon Brown, *Software Architecture for Developers* | arxitekturani hujjatlash: C4 |
| Reis, Housley, *Fundamentals of Data Engineering* | analitik quvur va ombor |
| Kleppmann, *DDIA* (bor) + bulut provayder whitepaper lari | ko'p region va geo-taqsimlash |

### 2.11 Audit natijasida qo'shilgan: infratuzilma va vositalar

Ro'yxatning birinchi variantida shu sohalar ochiq qolgan edi va
ularning har biri korpusda alohida bob egallaydi.

| Kitob | Bob | Nega kerak |
|---|---|---|
| Shapira, Palino, Sivaram, Petty, *Kafka: The Definitive Guide* 2-nashr | architect 29, patterns 16 | Partition, consumer group, rebalance, idempotent producer va aniq bir marta semantikasining uy manbasi. Hozir architect 29 ortida faqat DDIA 11-bob turadi, u esa Kafka ga xos emas |
| Josh Long, *Reactive Spring* yoki Project Reactor hujjati | patterns 19, architect 17.4, 17.12 | Reaktiv operatorlar, orqaga bosim va `Schedulers` semantikasi |
| Cogoluegnes va boshq., *Spring Batch in Action* | patterns 20 | Chunk, restart, skip va listener mexanikasi. Hozir patterns 20 ortida faqat DDIA turadi |
| Josiah Carlson, *Redis in Action* | architect 28, patterns 11 | Kesh invalidatsiyasi, TTL, stampede va Redis ma'lumot tuzilmalari. Keshlash boblari ortida hozir kitob yo'q |
| Jeffrey Friedl, *Mastering Regular Expressions* | clean-code 21.6, 21.7, code-review 31 | Katastrofik backtracking ning yagona chuqur manbasi |
| Adam Shostack, *Threat Modeling: Designing for Security* | code-review 28, architect 7 | Xavfsizlik review metodikasi: xavf yuzasi va STRIDE |
| Indrasiri, Kuruppu, *gRPC: Up and Running* | patterns 7.27 | Stream turlari, deadline va xato modeli |
| Marc-Andre Giroux, *Production Ready GraphQL* | patterns 7.26 | N+1, murakkablik chegarasi va versiyalanmaydigan sxema |
| Nigel Poulton, *Docker Deep Dive* | architect 31, patterns 22 | Image qatlamlari, cgroup va konteyner chegaralari |
| Richardson, Amundsen, *RESTful Web APIs* | patterns 7, architect 17.6 | Resurs modeli va gipermedia qarori |

## 3. Nashrni yangilash kerak

`books` repoda ikki kitob eski nashrda va bu korpusga zarar qiladi:

| Bor nashr | Muammo | Kerak |
|---|---|---|
| Carnell, *Spring Microservices in Action* 1-nashr | Hystrix, Zuul, Eureka, Sleuth: hammasi EOL yoki almashtirilgan | 2-nashr: Resilience4j, Spring Cloud Gateway |
| Spilca, *Spring Security in Action* 1-nashr | Boot 2 davri, `WebSecurityConfigurerAdapter` olib tashlangan | 2-nashr: Boot 3 va lambda DSL |

## 4. Kitob yordam bermaydigan joy

| Bob | Sabab va yechim |
|---|---|
| sonarqube 1-43 | SonarQube bo'yicha jiddiy kitob yo'q. Faqat rasmiy hujjat va rule metadata |
| patterns 30 (Spring AI va LLM) | Mavzu juda yangi. Manba: Spring AI reference va model provayderi hujjati |
| testing 4 (QA jarayoni) | Jamoaga bog'liq. Manba: ISTQB sillabusi |
| architect 12 (virtual thread) | JCiP bu mavzudan oldin yozilgan. Manba: JEP 444, 453, 446 va OpenJDK manba kodi |

## 5. Qo'shilishi kerak bo'lgan yangi boblar

Mavzu bo'shliqlari qidiruv bilan tekshirildi. Quyidagilar korpusda
yo'q va ular bo'lim emas, alohida bob bo'lishga arziydi:

| Hujjat | Taklif qilingan bob | Manba |
|---|---|---|
| architect | Arxitekturani hujjatlash: C4, ko'rinishlar, diagramma qachon arziydi | Brown, Clements, c4model.com |
| architect | Ko'p region va geo-taqsimlash: kechikish, ma'lumot rezidentligi, failover | DDIA, provayder whitepaper lari |
| architect | Ma'lumot maxfiyligi: saqlash muddati, o'chirish talabi, audit izi | Bhajaria, OWASP |
| architect | Sig'im rejalashtirish: o'sish prognozi, yuk testi bilan tizza nuqtasini topish | Allspaw, Gregg |
| architect | Qidiruv tizimi: PostgreSQL FTS chegarasi va alohida dvigatelga o'tish | Relevant Search, Elasticsearch reference |
| testing | Test ma'lumot generatsiyasi va property-based testlash chuqur | Aniche, jqwik hujjati |
| code-review | Ma'lumot migratsiyasi va backfill review (hozir 25-bobda qisqa) | PoEAA, DDIA |

Yangi bob qo'shish tartibi `CONTRIBUTING.md` da: fayl, mundarija,
manifest, qo'shni footer, skill jadvali, bob soni, `check_docs`.
Bitta eslatma: hujjat "yangi bob faqat tekshirilgan holatda
qo'shiladi" deydi, `tekshirilgan` ni esa faqat odam qo'yadi. Shu
sababli yangi bob manba bilan yoziladi va `tekshirilmoqda` da
qoldiriladi, imzo sizda.
