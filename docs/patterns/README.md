# Java Spring arxitektori bilishi kerak bo'lgan barcha dizayn patternlar

Bu ma'lumotnoma Java va Spring ekotizimida ishlaydigan arxitektor bilishi kerak bo'lgan dizayn pattern, arxitektura uslubi, integratsiya, resilience, xavfsizlik, testing va anti-patternni **30 ta bo'limda**, **1007 ta** yozuv (996 noyob pattern) bilan qamrab oladi. Har bir pattern uchun to'rt qism berilgan:

- **Tavsif** - pattern qanday muammoni hal qiladi va qanday ishlaydi.
- **Spring'da qayerda uchraydi** - Spring Framework, Spring Boot va ekotizimdagi aniq sinflar, annotatsiyalar, kutubxonalar.
- **Qo'llanish keyslari** - real loyihalarda qayerda ishlatiladi.
- **Ehtiyot bo'ling** - tuzoqlar, noto'g'ri qo'llash holatlari va qachon ishlatmaslik kerak.

Barcha patternlarning inglizcha nomi bo'yicha [alifbo indeksi](99-alifbo-boyicha-indeks.md) alohida faylda.


**Bu hujjat oltilikning bir qismi.** Mavzular takrorlanmaydi; qolgan beshtasi: [Testlash qo'llanmasi](../testing/README.md), [Arxitektor miyasi](../architect/README.md), [SonarQube hujjati](../sonarqube/README.md), [Toza kod qoidalari](../clean-code/README.md), [Kod review](../code-review/README.md).

**Versiya bazasi:** Java 21 LTS (pol: 17, Java 25 eslatmalari bilan), Spring Boot 3.2-3.5 (4.0 eslatmalari bilan), PostgreSQL 16+ (15-18 havolalari bilan), JUnit 5.

## Mundarija

- **1.** [Yaratuvchi patternlar (Creational Patterns)](01-yaratuvchi-patternlar.md) - 17 pattern
- **2.** [Strukturaviy patternlar (Structural Patterns)](02-strukturaviy-patternlar.md) - 17 pattern
- **3.** [Xulq-atvor patternlari (Behavioral Patterns)](03-xulq-atvor-patternlari.md) - 23 pattern
- **4.** [Concurrency patternlari (Concurrency Patterns)](04-concurrency-patternlari.md) - 27 pattern
- **5.** [Spring Core ichidagi patternlar xaritasi (Patterns inside Spring Core)](05-spring-core-ichidagi-patternlar-xaritasi.md) - 41 pattern
- **6.** [Web va taqdimot qatlami patternlari (Web & Presentation Patterns)](06-web-va-taqdimot-qatlami-patternlari.md) - 34 pattern
- **7.** [API dizayn patternlari (API Design Patterns)](07-api-dizayn-patternlari.md) - 33 pattern
- **8.** [Biznes logika va Service qatlam patternlari (Business & Service Layer Patterns)](08-biznes-logika-va-service-qatlam-patternlari.md) - 26 pattern
- **9.** [Ma'lumotlarga kirish va ORM patternlari (Data Access & ORM Patterns)](09-malumotlarga-kirish-va-orm-patternlari.md) - 37 pattern
- **10.** [Ma'lumotlarni boshqarish va taqsimlash patternlari (Data Management & Distribution Patterns)](10-malumotlarni-boshqarish-va-taqsimlash.md) - 31 pattern
- **11.** [Keshlash patternlari (Caching Patterns)](11-keshlash-patternlari.md) - 22 pattern
- **12.** [Arxitektura uslublari (Architectural Styles)](12-arxitektura-uslublari.md) - 33 pattern
- **13.** [Domain-Driven Design patternlari (DDD Patterns)](13-domain-driven-design-patternlari.md) - 35 pattern
- **14.** [Microservices patternlari (Microservices Patterns)](14-microservices-patternlari.md) - 39 pattern
- **15.** [Enterprise Integration Patterns I: xabarlar, kanallar, marshrutlash (EIP I: Messaging Systems, Channels, Construction, Routing)](15-enterprise-integration-patterns-i-xabarlar.md) - 36 pattern
- **16.** [Enterprise Integration Patterns II: transformatsiya, endpointlar, boshqaruv, event patternlar (EIP II: Transformation, Endpoints, System Management, Event Patterns)](16-enterprise-integration-patterns-ii.md) - 44 pattern
- **17.** [Resilience va cloud dizayn patternlari (Resilience & Cloud Design Patterns)](17-resilience-va-cloud-dizayn-patternlari.md) - 42 pattern
- **18.** [Xavfsizlik patternlari (Security Patterns)](18-xavfsizlik-patternlari.md) - 48 pattern
- **19.** [Reactive patternlar (Reactive Patterns)](19-reactive-patternlar.md) - 25 pattern
- **20.** [Batch va scheduling patternlari (Batch & Scheduling Patterns)](20-batch-va-scheduling-patternlari.md) - 30 pattern
- **21.** [Observability patternlari (Observability Patterns)](21-observability-patternlari.md) - 25 pattern
- **22.** [Deployment va operatsion patternlar (Deployment & Operations Patterns)](22-deployment-va-operatsion-patternlar.md) - 37 pattern
- **23.** [Testing patternlari (Testing Patterns)](23-testing-patternlari.md) - 61 pattern
- **24.** [Zamonaviy Java va funksional patternlar (Modern Java & Functional Patterns)](24-zamonaviy-java-va-funksional-patternlar.md) - 40 pattern
- **25.** [Anti-patternlar (Anti-Patterns)](25-anti-patternlar.md) - 83 pattern
- **26.** [Dizayn printsiplari: SOLID, GRASP va umumiy qoidalar (Design Principles: SOLID, GRASP & General Rules)](26-dizayn-printsiplari-solid-grasp-va-umumiy.md) - 29 pattern
- **27.** [Monolitdan microservice'ga migratsiya patternlari (Monolith to Microservices Migration Patterns)](27-monolitdan-microservicega-migratsiya.md) - 22 pattern
- **28.** [Taqsimlangan ma'lumot, replikatsiya va konsistentlik patternlari (Distributed Data, Replication & Consistency Patterns)](28-taqsimlangan-malumot-replikatsiya-va.md) - 28 pattern
- **29.** [Kubernetes va cloud-native patternlar (Kubernetes & Cloud-Native Patterns)](29-kubernetes-va-cloud-native-patternlar.md) - 22 pattern
- **30.** [Spring AI va LLM integratsiya patternlari (Spring AI & LLM Integration Patterns)](30-spring-ai-va-llm-integratsiya-patternlari.md) - 20 pattern
- [Alifbo bo'yicha indeks](99-alifbo-boyicha-indeks.md)

---

[&larr; Barcha hujjatlar](../../README.md)
