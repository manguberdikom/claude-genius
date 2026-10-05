# Kod yozadigan arxitektorning miyasi: Java, Spring, PostgreSQL

Bu hujjat kod yozadigan arxitektorning bilimi va fikrlash tarzini yig'adi.
Tayanch stek: Java, Spring va PostgreSQL. Har bob ikki narsani beradi: ichkarida nima
sodir bo'lishining mexanikasi, va shu bilimdan qanday qaror chiqarish.


**Bu hujjat oltilikning bir qismi.** Har biri boshqa savolga javob beradi; qolgan beshtasi: [Dizayn patternlar katalogi](../patterns/README.md), [Testlash qo'llanmasi](../testing/README.md), [SonarQube hujjati](../sonarqube/README.md), [Toza kod qoidalari](../clean-code/README.md), [Kod review](../code-review/README.md).

**Versiya bazasi:** Java 21 LTS (pol: 17, Java 25 eslatmalari bilan), Spring Boot 3.2-3.5 (4.0 eslatmalari bilan), PostgreSQL 16+ (15-18 havolalari bilan), JUnit 5.

## Mundarija

### I. Fikrlash va qarorlar

- **1.** [Arxitektorning fikrlash modeli (The Architect's Mental Model)](01-arxitektorning-fikrlash-modeli.md) - 11 bo'lim
- **2.** [Muammoni tushunish va to'g'ri savol berish (Understanding the Problem)](02-muammoni-tushunish-va-togri-savol-berish.md) - 11 bo'lim
- **3.** [Qaror qabul qilish va uni hujjatlashtirish (Decisions and ADRs)](03-qaror-qabul-qilish-va-uni-hujjatlashtirish.md) - 11 bo'lim
- **4.** [Kod - muloqot vositasi: nomlash, aniqlik, kognitiv yuk (Code as Communication)](04-kod-muloqot-vositasi-nomlash-aniqlik.md) - 11 bo'lim
- **5.** [Abstraksiya hissi, bog'liqlik va chegaralar (Abstraction, Coupling and Boundaries)](05-abstraksiya-hissi-bogliqlik-va-chegaralar.md) - 11 bo'lim
- **6.** [Murakkablikni boshqarish (Managing Complexity)](06-murakkablikni-boshqarish.md) - 11 bo'lim
- **7.** [Nosozlik haqida fikrlash (Thinking About Failure)](07-nosozlik-haqida-fikrlash.md) - 11 bo'lim
- **8.** [Ishlash va resurs hissi: napkin math (Performance Intuition and Napkin Math)](08-ishlash-va-resurs-hissi-napkin-math.md) - 11 bo'lim

### II. Java chuqur bilim

- **9.** [JVM ichki tuzilishi: class loading, memory model, JIT (JVM Internals)](09-jvm-ichki-tuzilishi-class-loading-memory.md) - 12 bo'lim
- **10.** [Garbage collection va xotira sozlash (Garbage Collection and Memory Tuning)](10-garbage-collection-va-xotira-sozlash.md) - 12 bo'lim
- **11.** [Concurrency: thread, lock, atomic, happens-before (Java Concurrency)](11-concurrency-thread-lock-atomic-happens.md) - 12 bo'lim
- **12.** [Virtual threads, structured concurrency va scoped values (Modern Concurrency)](12-virtual-threads-structured-concurrency-va.md) - 11 bo'lim
- **13.** [Zamonaviy Java tili va API dizayni (Modern Java and API Design)](13-zamonaviy-java-tili-va-api-dizayni.md) - 12 bo'lim
- **14.** [JVM profiling va diagnostika: JFR, async-profiler, heap dump (JVM Profiling and Diagnostics)](14-jvm-profiling-va-diagnostika-jfr-async.md) - 12 bo'lim

### III. Spring chuqur bilim

- **15.** [Spring Core mexanikasi: IoC konteyner, bean lifecycle, AOP proxy (Spring Core Mechanics)](15-spring-core-mexanikasi-ioc-konteyner-bean.md) - 12 bo'lim
- **16.** [Spring Boot mexanikasi: auto-configuration, starter, Actuator (Spring Boot Mechanics)](16-spring-boot-mexanikasi-auto-configuration.md) - 12 bo'lim
- **17.** [Spring MVC va WebFlux: so'rov yo'li, thread modeli, REST dizayni (Spring MVC and WebFlux)](17-spring-mvc-va-webflux-sorov-yoli-thread.md) - 12 bo'lim
- **18.** [Spring Data JPA va Hibernate chuqur (Spring Data JPA and Hibernate)](18-spring-data-jpa-va-hibernate-chuqur.md) - 13 bo'lim
- **19.** [Spring tranzaksiyalari va ularning chegaralari (Spring Transactions)](19-spring-tranzaksiyalari-va-ularning.md) - 13 bo'lim
- **20.** [Spring Security: filter chain, OAuth2, JWT (Spring Security)](20-spring-security-filter-chain-oauth2-jwt.md) - 13 bo'lim

### IV. PostgreSQL chuqur bilim

- **21.** [PostgreSQL arxitekturasi: process model, WAL, checkpoint, vacuum (PostgreSQL Architecture)](21-postgresql-arxitekturasi-process-model-wal.md) - 12 bo'lim
- **22.** [MVCC, izolyatsiya darajalari, lock va deadlock (MVCC and Isolation)](22-mvcc-izolyatsiya-darajalari-lock-va-deadlock.md) - 12 bo'lim
- **23.** [Indekslar: B-tree, GIN, GiST, BRIN va tanlov (Indexes)](23-indekslar-b-tree-gin-gist-brin-va-tanlov.md) - 13 bo'lim
- **24.** [Planner, statistika va EXPLAIN ANALYZE o'qish (Planner and EXPLAIN ANALYZE)](24-planner-statistika-va-explain-analyze-oqish.md) - 13 bo'lim
- **25.** [Sxema dizayni, ma'lumot turlari va cheklovlar (Schema Design and Data Types)](25-sxema-dizayni-malumot-turlari-va-cheklovlar.md) - 13 bo'lim
- **26.** [Partitioning, replikatsiya va katta hajm (Partitioning, Replication and Scale)](26-partitioning-replikatsiya-va-katta-hajm.md) - 13 bo'lim
- **27.** [Sozlash, connection pool va monitoring (Configuration, Pooling and Monitoring)](27-sozlash-connection-pool-va-monitoring.md) - 13 bo'lim

### V. Atrof ekotizim: operatsion haqiqat

- **28.** [Keshlash amaliyoti: invalidatsiya, stampede, Redis haqiqati (Caching in Practice)](28-keshlash-amaliyoti-invalidatsiya-stampede.md) - 13 bo'lim
- **29.** [Kafka operatsion haqiqati: partition, lag, rebalance, idempotentlik (Kafka in Production)](29-kafka-operatsion-haqiqati-partition-lag.md) - 14 bo'lim
- **30.** [Kuzatuvchanlik amaliyoti: log, metrika, trace va ularning narxi (Observability in Practice)](30-kuzatuvchanlik-amaliyoti-log-metrika-trace.md) - 13 bo'lim
- **31.** [Deployment haqiqati: konteyner, cgroup, JVM va probe (Deployment Reality)](31-deployment-haqiqati-konteyner-cgroup-jvm-va.md) - 13 bo'lim
- **32.** [Tarmoq, timeout va integratsiya haqiqati (Network, Timeouts and Integration)](32-tarmoq-timeout-va-integratsiya-haqiqati.md) - 13 bo'lim

### VI. Amaliyot va o'sish

- **33.** [Sxema migratsiyasi va to'xtashsiz reliz (Schema Migration and Zero-Downtime Release)](33-sxema-migratsiyasi-va-toxtashsiz-reliz.md) - 13 bo'lim
- **34.** [Legacy kod va bosqichma-bosqich refaktoring (Legacy Code and Refactoring)](34-legacy-kod-va-bosqichma-bosqich-refaktoring.md) - 13 bo'lim
- **35.** [Incident, on-call va post-mortem (Incidents and Post-mortems)](35-incident-on-call-va-post-mortem.md) - 14 bo'lim
- **36.** [Code review va jamoada texnik yetakchilik (Code Review and Technical Leadership)](36-code-review-va-jamoada-texnik-yetakchilik.md) - 13 bo'lim
- **37.** [Xarajat, SLO va biznes bilan muloqot (Cost, SLO and Business Communication)](37-xarajat-slo-va-biznes-bilan-muloqot.md) - 13 bo'lim
- **38.** [Doimiy o'rganish va texnologiya tanlash (Continuous Learning and Technology Choice)](38-doimiy-organish-va-texnologiya-tanlash.md) - 13 bo'lim
- **39.** [Birinchi 90 kun va o'z-o'zini baholash (First 90 Days and Self-Assessment)](39-birinchi-90-kun-va-oz-ozini-baholash.md) - 14 bo'lim

---

[&larr; Barcha hujjatlar](../../README.md)
