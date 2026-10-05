---
name: design-patterns
description: Pick and apply a design pattern for Java/Spring code - GoF, Spring container, DDD, microservices, EIP, resilience, caching, reactive, batch, cloud-native and anti-patterns. Use when a task involves object creation strategy, decoupling modules, swapping algorithms at runtime, adding behavior without subclassing, integration or messaging shape, retry/circuit-breaker/bulkhead choices, splitting a monolith, or when the user names a pattern (factory, strategy, observer, adapter, decorator, singleton, repository, saga, outbox, CQRS, sidecar, ...) or asks "qaysi pattern to'g'ri keladi" / "what pattern fits here".
---

# Dizayn patternlar

1007 pattern, 30 bob. To'liq katalog: `docs/patterns/README.md`.
Inglizcha nom bo'yicha qidirish: `tools/doc.sh find "<nom>"` (alifbo indeksi
shu buyruq ichida; `99-alifbo-boyicha-indeks.md` faylini o'qimang, u ~42k token).

## Qoida

Pattern - lug'at, maqsad emas. Patternni u hal qiladigan **muammo kodda
allaqachon bo'lsa** oling, dizayn jiddiy ko'rinsin uchun emas.

1. Muammoni bitta gapda ayting: "har bir yangi to'lov provayderi uchta
   `switch` ni tahrirlashga majbur qiladi".
2. Kontekstda bo'lim taklifi (`patterns 3.9` kabi) yoki `doc.sh find`
   natijasi bo'lsa, 3-qadamga o'ting. Bo'lmasa quyidagi jadvaldan bobni
   toping (fayl nomidagi NN bob raqami) va `tools/doc.sh outline patterns <bob>`
   bilan pattern nomlarini ko'ring.
3. Bobni butunligicha o'qimang (bob 17-66k token, bo'lim ~1k): keraklisini
   `tools/doc.sh show patterns <bob.bo'lim>` bilan oching. Har yozuvda
   `Tavsif`, `Spring'da qayerda uchraydi`, `Qo'llanish keyslari`,
   `Ehtiyot bo'ling` bor.
4. Qo'llashdan oldin anti-patternni tekshiring: `tools/doc.sh outline patterns 25`
   (83 anti-pattern), mosini `tools/doc.sh show patterns 25.N` bilan oching.
5. Kodga tegishdan oldin `python3 tools/rules_for.py <tegiladigan fayllar>`
   chaqiring (yangi fayl bo'lsa ham). Aks holda `check_code.py` hook birinchi
   Java yozuvini qaytaradi.
6. Muammoni hal qiladigan **eng kichik** variantni qo'llang.

Spring loyihasida ko'p pattern allaqachon konteyner ichida bor: qo'lda
Singleton, Factory yoki Registry yozishdan oldin
`tools/doc.sh outline patterns 5` ga qarang (Spring core ichidagi patternlar
xaritasi).

## Muammo - bob jadvali

| Kodda ko'rayotgan muammo | Bob fayli (NN = bob raqami) |
|---|---|
| `new ConcreteThing()` har joyda, 6+ parametrli konstruktor, lazy yaratish, obyekt hovuzi | `docs/patterns/01-yaratuvchi-patternlar.md` |
| Tashqi API shakli mos emas, runtime'da xulq qo'shish, murakkab tizimga sodda eshik, kesh/lazy/huquq uchun o'ram | `docs/patterns/02-strukturaviy-patternlar.md` |
| `if/switch` almashinadigan algoritm tanlaydi, hodisaga reaksiya, lifecycle bosqichiga qarab xulq, undo/queue | `docs/patterns/03-xulq-atvor-patternlari.md` |
| Thread, lock, latch, producer-consumer, thread-local, double-checked locking | `docs/patterns/04-concurrency-patternlari.md` |
| Konteyner nima qilyapti: bean lifecycle, `@Lazy`, `FactoryBean`, `BeanPostProcessor`, AOP proxy, `ObjectProvider` | `docs/patterns/05-spring-core-ichidagi-patternlar-xaritasi.md` |
| Controller semirib ketdi, filter/interceptor, view, async so'rov, `@ControllerAdvice` | `docs/patterns/06-web-va-taqdimot-qatlami-patternlari.md` |
| REST shakli, versiyalash, sahifalash, xato formati (RFC 9457), HATEOAS, idempotentlik kaliti | `docs/patterns/07-api-dizayn-patternlari.md` |
| Service qatlam semizligi, use-case handler, mapper, tranzaksiya chegarasi, validatsiya | `docs/patterns/08-biznes-logika-va-service-qatlam-patternlari.md` |
| Repository vs DAO, Unit of Work, lazy load, N+1, ID generatsiyasi, Specification, connection pool | `docs/patterns/09-malumotlarga-kirish-va-orm-patternlari.md` |
| Outbox, inbox, CDC, kompensatsiya, TCC, 2PC/XA, multi-tenancy, sharding, read replica marshrutlash, taqsimlangan lock | `docs/patterns/10-malumotlarni-boshqarish-va-taqsimlash.md` |
| Cache-aside, write-through, invalidatsiya, stampede, taqsimlangan kesh | `docs/patterns/11-keshlash-patternlari.md` |
| Monolit/modular monolit/microservice/EDA/CQRS/hexagonal tanlovi | `docs/patterns/12-arxitektura-uslublari.md` |
| Aggregate, entity, value object, domain event, bounded context, anti-corruption layer | `docs/patterns/13-domain-driven-design-patternlari.md` |
| Bir nechta servisga tegadigan biznes oqimi va uni qaytarish (Saga: xoreografiya yoki orkestratsiya), service discovery, API gateway, sidecar, tashqi konfiguratsiya, strangler, BFF, servis granularligi | `docs/patterns/14-microservices-patternlari.md` |
| Xabar kanali, marshrutlash, splitter, aggregator, message bus | `docs/patterns/15-enterprise-integration-patterns-i-xabarlar.md` |
| Xabar transformatsiyasi, endpoint turlari, idempotent receiver, event patternlar | `docs/patterns/16-enterprise-integration-patterns-ii.md` |
| Retry, backoff, jitter, circuit breaker, bulkhead, timeout, fallback, rate limiter | `docs/patterns/17-resilience-va-cloud-dizayn-patternlari.md` |
| `SecurityFilterChain`, RBAC/ABAC, parol hash, CSRF, CSP/HSTS, sirlarni boshqarish | `docs/patterns/18-xavfsizlik-patternlari.md` |
| Reactive oqim, backpressure, SSE/NDJSON, blocking kodni ko'prikka olish | `docs/patterns/19-reactive-patternlar.md` |
| Spring Batch step, chunk, partitioning, scheduler, ETL | `docs/patterns/20-batch-va-scheduling-patternlari.md` |
| Correlation ID, structured log, metrika, trace, baggage, health check | `docs/patterns/21-observability-patternlari.md` |
| Blue-green, canary, rolling update, feature flag, health probe (liveness/readiness/startup), init va sidecar konteyner, graceful shutdown, image qurish, GraalVM native, 12-factor konfiguratsiya | `docs/patterns/22-deployment-va-operatsion-patternlar.md` |
| Test double turlari, AAA/GWT, test data builder, slice test, mutation testing | `docs/patterns/23-testing-patternlari.md` |
| `record`, `sealed`, pattern matching, `Optional`, funksional kompozitsiya, JPMS | `docs/patterns/24-zamonaviy-java-va-funksional-patternlar.md` |
| Bu dizayn yomonmi: anemik model, god class, open session in view, distributed monolith | `docs/patterns/25-anti-patternlar.md` |
| SOLID, GRASP, DRY/KISS/YAGNI, Law of Demeter | `docs/patterns/26-dizayn-printsiplari-solid-grasp-va-umumiy.md` |
| Monolitni bo'lish: strangler fig, branch by abstraction, parallel run | `docs/patterns/27-monolitdan-microservicega-migratsiya.md` |
| Replikatsiya, konsistentlik modellari, konflikt yechish, quorum | `docs/patterns/28-taqsimlangan-malumot-replikatsiya-va.md` |
| Kubernetes resurs modeli: pod, resurs limiti, HPA va elastic scale, ConfigMap/Secret, controller va operator, stateless/stateful servis | `docs/patterns/29-kubernetes-va-cloud-native-patternlar.md` |
| `ChatClient`, RAG, embedding, tool calling, advisor zanjiri, prompt shabloni | `docs/patterns/30-spring-ai-va-llm-integratsiya-patternlari.md` |

## Javob shakli

Pattern tavsiya qilganda har doim to'rttasini bering: **qaysi pattern**,
**nega aynan shu muammoga**, **Spring'da tayyor varianti bormi**, va
**qaysi tuzoqqa tushmaslik kerak**. Faqat nom aytib qo'yish yetarli emas.

## Asboblar

Asosiy o'qish yo'li shu buyruqlar, jadval faqat bob raqamini beradi. Indeks
inglizcha taxallusni ham biladi (`circuit breaker`, `saga`, `outbox`):

```bash
python3 tools/rules_for.py <fayl>...     # Java yozishdan OLDIN majburiy: boblar, punktlar, avvalgi xatolar
tools/doc.sh find "<pattern nomi>"       # bob.bo'lim raqamini beradi (masalan 3.9)
tools/doc.sh outline patterns <bob>      # bobdagi bo'limlar ro'yxati
tools/doc.sh show patterns <bob.bo'lim>  # faqat o'sha bo'lim (masalan 17.2)
```

`show` ga faqat bob raqami berilsa kichik bob butunligicha chiqadi, 1200
satrdan uzuni esa outline bo'lib qaytadi.
