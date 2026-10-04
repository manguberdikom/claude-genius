# Java Spring arxitektori bilishi kerak bo'lgan barcha dizayn patternlar

Bu ma'lumotnoma Java va Spring ekotizimida ishlaydigan arxitektor bilishi kerak bo'lgan **1007 ta** dizayn pattern, arxitektura uslubi, integratsiya, resilience, xavfsizlik, testing va anti-patternni **30 ta bo'limda** qamrab oladi. Har bir pattern uchun to'rt qism berilgan:

- **Tavsif** — pattern qanday muammoni hal qiladi va qanday ishlaydi.
- **Spring'da qayerda uchraydi** — Spring Framework, Spring Boot va ekotizimdagi aniq sinflar, annotatsiyalar, kutubxonalar.
- **Qo'llanish keyslari** — real loyihalarda qayerda ishlatiladi.
- **Ehtiyot bo'ling** — tuzoqlar, noto'g'ri qo'llash holatlari va qachon ishlatmaslik kerak.

Barcha patternlarning inglizcha nomi bo'yicha [alifbo indeksi](99-alifbo-boyicha-indeks.md) alohida faylda.

**Bu hujjat to'rtlikning bir qismi.** Mavzular takrorlanmaydi; qolgan uchtasi: [Testlash qo'llanmasi](../testing/README.md), [Arxitektor miyyasi](../architect/README.md), [SonarQube hujjati](../sonarqube/README.md).

**Versiya bazasi:** Java 21 LTS (pol: 17, Java 25 eslatmalari bilan), Spring Boot 3.2-3.5 (4.0 eslatmalari bilan), PostgreSQL 16+ (15-18 havolalari bilan), JUnit 5.

## Mundarija

- **1.** [Yaratuvchi patternlar (Creational Patterns)](01-yaratuvchi-patternlar.md) - 17 bo'lim
- **2.** [Strukturaviy patternlar (Structural Patterns)](02-strukturaviy-patternlar.md) - 17 bo'lim
- **3.** [Xulq-atvor patternlari (Behavioral Patterns)](03-xulq-atvor-patternlari.md) - 23 bo'lim
- **4.** [Concurrency patternlari (Concurrency Patterns)](04-concurrency-patternlari.md) - 27 bo'lim
- **5.** [Spring Core ichidagi patternlar xaritasi (Patterns inside Spring Core)](05-spring-core-ichidagi-patternlar-xaritasi.md) - 41 bo'lim
- **6.** [Web va taqdimot qatlami patternlari (Web & Presentation Patterns)](06-web-va-taqdimot-qatlami-patternlari.md) - 34 bo'lim
- **7.** [API dizayn patternlari (API Design Patterns)](07-api-dizayn-patternlari.md) - 33 bo'lim
- **8.** [Biznes logika va Service qatlam patternlari (Business & Service Layer Patterns)](08-biznes-logika-va-service-qatlam-patternlari.md) - 26 bo'lim
- **9.** [Ma'lumotlarga kirish va ORM patternlari (Data Access & ORM Patterns)](09-malumotlarga-kirish-va-orm-patternlari.md) - 37 bo'lim
- **10.** [Ma'lumotlarni boshqarish va taqsimlash patternlari (Data Management & Distribution Patterns)](10-malumotlarni-boshqarish-va-taqsimlash.md) - 31 bo'lim
- **11.** [Keshlash patternlari (Caching Patterns)](11-keshlash-patternlari.md) - 22 bo'lim
- **12.** [Arxitektura uslublari (Architectural Styles)](12-arxitektura-uslublari.md) - 33 bo'lim
- **13.** [Domain-Driven Design patternlari (DDD Patterns)](13-domain-driven-design-patternlari.md) - 35 bo'lim
- **14.** [Microservices patternlari (Microservices Patterns)](14-microservices-patternlari.md) - 39 bo'lim
- **15.** [Enterprise Integration Patterns I: xabarlar, kanallar, marshrutlash (EIP I: Messaging Systems, Channels, Construction, Routing)](15-enterprise-integration-patterns-i-xabarlar.md) - 36 bo'lim
- **16.** [Enterprise Integration Patterns II: transformatsiya, endpointlar, boshqaruv, event patternlar (EIP II: Transformation, Endpoints, System Management, Event Patterns)](16-enterprise-integration-patterns-ii.md) - 44 bo'lim
- **17.** [Resilience va cloud dizayn patternlari (Resilience & Cloud Design Patterns)](17-resilience-va-cloud-dizayn-patternlari.md) - 42 bo'lim
- **18.** [Xavfsizlik patternlari (Security Patterns)](18-xavfsizlik-patternlari.md) - 48 bo'lim
- **19.** [Reactive patternlar (Reactive Patterns)](19-reactive-patternlar.md) - 25 bo'lim
- **20.** [Batch va scheduling patternlari (Batch & Scheduling Patterns)](20-batch-va-scheduling-patternlari.md) - 30 bo'lim
- **21.** [Observability patternlari (Observability Patterns)](21-observability-patternlari.md) - 25 bo'lim
- **22.** [Deployment va operatsion patternlar (Deployment & Operations Patterns)](22-deployment-va-operatsion-patternlar.md) - 37 bo'lim
- **23.** [Testing patternlari (Testing Patterns)](23-testing-patternlari.md) - 61 bo'lim
- **24.** [Zamonaviy Java va funksional patternlar (Modern Java & Functional Patterns)](24-zamonaviy-java-va-funksional-patternlar.md) - 40 bo'lim
- **25.** [Anti-patternlar (Anti-Patterns)](25-anti-patternlar.md) - 83 bo'lim
- **26.** [Dizayn printsiplari: SOLID, GRASP va umumiy qoidalar (Design Principles: SOLID, GRASP & General Rules)](26-dizayn-printsiplari-solid-grasp-va-umumiy.md) - 29 bo'lim
- **27.** [Monolitdan microservice'ga migratsiya patternlari (Monolith to Microservices Migration Patterns)](27-monolitdan-microservicega-migratsiya.md) - 22 bo'lim
- **28.** [Taqsimlangan ma'lumot, replikatsiya va konsistentlik patternlari (Distributed Data, Replication & Consistency Patterns)](28-taqsimlangan-malumot-replikatsiya-va.md) - 28 bo'lim
- **29.** [Kubernetes va cloud-native patternlar (Kubernetes & Cloud-Native Patterns)](29-kubernetes-va-cloud-native-patternlar.md) - 22 bo'lim
- **30.** [Spring AI va LLM integratsiya patternlari (Spring AI & LLM Integration Patterns)](30-spring-ai-va-llm-integratsiya-patternlari.md) - 20 bo'lim
- [Alifbo bo'yicha indeks](99-alifbo-boyicha-indeks.md)

---

[&larr; Barcha hujjatlar](../../README.md)
