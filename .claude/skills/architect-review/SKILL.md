---
name: architect-review
description: Review a design or diagnose runtime behaviour in a Java/Spring system - module boundaries, coupling and cohesion, complexity, failure modes, napkin-math capacity estimates, JVM internals and GC, concurrency and virtual threads, profiling, Spring container/Boot/MVC/WebFlux/Data/transaction/Security mechanics, caching, Kafka, observability, container deployment, timeouts, schema migration, legacy refactoring, incidents and ADRs. Use when asked whether a design is right, where to put a boundary, why something is slow or leaking, how many threads or how much heap to give, what happens inside Spring, or to write an ADR or post-mortem.
---

# Arxitektor ko'rigi

39 bob, 482 bo'lim. To'liq hujjat: `docs/architect/README.md`.

## Qoida

Har bob ikki narsani beradi: **ichkarida nima sodir bo'ladi** va **shu
bilimdan qanday qaror chiqadi**. Ko'rik berganda ikkinchisini tashlab
ketmang - mexanikani aytib, qarorni aytmaslik yarim javob.

Qaror tavsiya qilganda:
1. Muammoni va kontekstni aniqlang (`docs/architect/02-...`).
2. Ikkita-uchta variantni taqqoslang, har birining narxi bilan.
3. Raqam bilan tekshiring - napkin math (`docs/architect/08-...`).
   "Tezroq bo'ladi" o'lchovsiz gap.
4. Nosozlik rejimini ayting: bu nima buzilganda qanday o'ladi
   (`docs/architect/07-...`).
5. Qaror muhim bo'lsa, ADR yozing (`docs/architect/03-...`).

## Mavzu - bob jadvali

### I. Fikrlash va qarorlar
| Mavzu | Fayl |
|---|---|
| Fikrlash modeli, trade-off, sifat atributlari | `docs/architect/01-arxitektorning-fikrlash-modeli.md` |
| Muammoni tushunish, to'g'ri savol | `docs/architect/02-muammoni-tushunish-va-togri-savol-berish.md` |
| ADR yozish, shablon, yomon ADR belgilari | `docs/architect/03-qaror-qabul-qilish-va-uni-hujjatlashtirish.md` |
| Nomlash, aniqlik, kognitiv yuk | `docs/architect/04-kod-muloqot-vositasi-nomlash-aniqlik.md` |
| Abstraksiya, bog'liqlik, koheziya, chegara | `docs/architect/05-abstraksiya-hissi-bogliqlik-va-chegaralar.md` |
| Murakkablikni boshqarish | `docs/architect/06-murakkablikni-boshqarish.md` |
| Nosozlik rejimlari, blast radius, degradatsiya | `docs/architect/07-nosozlik-haqida-fikrlash.md` |
| Napkin math, Little qonuni, sig'im hisobi | `docs/architect/08-ishlash-va-resurs-hissi-napkin-math.md` |

### II. Java
| Mavzu | Fayl |
|---|---|
| Class loading, memory model, JIT | `docs/architect/09-jvm-ichki-tuzilishi-class-loading-memory.md` |
| GC tanlash va xotira sozlash | `docs/architect/10-garbage-collection-va-xotira-sozlash.md` |
| Thread, lock, atomic, happens-before | `docs/architect/11-concurrency-thread-lock-atomic-happens.md` |
| Virtual threads, structured concurrency | `docs/architect/12-virtual-threads-structured-concurrency-va.md` |
| `record`, `sealed`, API dizayni | `docs/architect/13-zamonaviy-java-tili-va-api-dizayni.md` |
| JFR, async-profiler, heap dump o'qish | `docs/architect/14-jvm-profiling-va-diagnostika-jfr-async.md` |

### III. Spring
| Mavzu | Fayl |
|---|---|
| IoC konteyner, bean lifecycle, AOP proxy | `docs/architect/15-spring-core-mexanikasi-ioc-konteyner-bean.md` |
| Auto-configuration, starter, Actuator | `docs/architect/16-spring-boot-mexanikasi-auto-configuration.md` |
| MVC vs WebFlux, so'rov yo'li, thread modeli | `docs/architect/17-spring-mvc-va-webflux-sorov-yoli-thread.md` |
| JPA/Hibernate: N+1, flush, dirty checking | `docs/architect/18-spring-data-jpa-va-hibernate-chuqur.md` |
| Tranzaksiya chegaralari, propagation, `readOnly` | `docs/architect/19-spring-tranzaksiyalari-va-ularning.md` |
| Filter chain, OAuth2, JWT | `docs/architect/20-spring-security-filter-chain-oauth2-jwt.md` |

### IV. PostgreSQL
Bu qism uchun `postgres-tuning` skilliga qarang (21-27 boblar).

### V-VI. Operatsion haqiqat va o'sish
| Mavzu | Fayl |
|---|---|
| Kesh invalidatsiyasi, stampede, Redis haqiqati | `docs/architect/28-keshlash-amaliyoti-invalidatsiya-stampede.md` |
| Kafka: partition, lag, rebalance, idempotentlik | `docs/architect/29-kafka-operatsion-haqiqati-partition-lag.md` |
| Log, metrika, trace va ularning narxi | `docs/architect/30-kuzatuvchanlik-amaliyoti-log-metrika-trace.md` |
| Konteyner, cgroup, JVM limitlari, probe | `docs/architect/31-deployment-haqiqati-konteyner-cgroup-jvm-va.md` |
| Timeout budjeti, retry, tarmoq haqiqati | `docs/architect/32-tarmoq-timeout-va-integratsiya-haqiqati.md` |
| Sxema migratsiyasi, to'xtashsiz reliz, expand/contract | `docs/architect/33-sxema-migratsiyasi-va-toxtashsiz-reliz.md` |
| Legacy kod, bosqichma-bosqich refaktoring | `docs/architect/34-legacy-kod-va-bosqichma-bosqich-refaktoring.md` |
| Incident, on-call, post-mortem shabloni | `docs/architect/35-incident-on-call-va-post-mortem.md` |
| Code review va texnik yetakchilik | `docs/architect/36-code-review-va-jamoada-texnik-yetakchilik.md` |
| Xarajat, SLO, biznes bilan muloqot | `docs/architect/37-xarajat-slo-va-biznes-bilan-muloqot.md` |
| Texnologiya tanlash, doimiy o'rganish | `docs/architect/38-doimiy-organish-va-texnologiya-tanlash.md` |
| Birinchi 90 kun, o'z-o'zini baholash | `docs/architect/39-birinchi-90-kun-va-oz-ozini-baholash.md` |

Pattern tanlash kerak bo'lsa: `design-patterns` skilli.
Test strategiyasi: `spring-testing` skilli.

## Asboblar

Bob jadvali mavzuni topadi, bu asboblar esa ish oldidan faktni beradi:

```bash
python3 tools/rules_for.py <fayl>...        # tegilayotgan faylga qaysi boblar
python3 tools/schema_from_entities.py <src> # baza tuzilishi, ulanmasdan
tools/doc.sh find -f "<so'rov>"             # matn ichidan qidirish
```

`docker up/run/build` va bazaga ulanish `tools/guard.py` tomonidan
to'siladi: sxemani entity sinflari, sababni esa chiqish aytadi.
