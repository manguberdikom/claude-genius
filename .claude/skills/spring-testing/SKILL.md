---
name: spring-testing
description: Write or fix tests in a Java/Spring project - unit tests, Spring Boot slice tests, Testcontainers, contract testing, test data, security/transaction/async/concurrency tests, E2E, performance and resilience tests, CI test pipeline, flaky-test triage. Use when adding or reviewing tests, choosing between @SpringBootTest and a slice, replacing H2 with a real PostgreSQL container, mocking an external service, a test is flaky or slow, or when the user asks about test strategy, test pyramid, coverage targets or JUnit 5 / Mockito / AssertJ / WireMock / PIT usage.
---

# Spring loyihasida testlash

18 bob, 239 bo'lim. To'liq qo'llanma: `docs/testing/README.md`.

## Qoida

Testning birligi - sinf emas, **xatti-harakat**. Standart uslub sociable;
solitary (hamma narsa mock) faqat I/O chegarasida.

Test yozishdan oldin uchta savolga javob bering:
1. Nimani tasdiqlamoqchimiz - xatti-harakatni yoki implementatsiyani?
2. Eng past darajada tekshirsa bo'ladimi? (unit > slice > to'liq kontekst)
3. Bu test nima buzilganda qizil bo'ladi? Javob "har qanday refaktoringda"
   bo'lsa, test yomon.

Har bob oxirida `Arxitektor nazorat ro'yxati` bor - tavsiya berishdan
oldin shuni o'qing.

## Vazifa - bob jadvali

| Vazifa | Bob fayli |
|---|---|
| Test strategiyasi hujjati, sifat darvozalari, arxitektorning roli | `docs/testing/01-sifat-strategiyasi-va-arxitektorning-roli.md` |
| Qaysi darajada test yozish, piramida vs trophy, test turlari xaritasi | `docs/testing/02-test-piramidasi-va-test-turlari-xaritasi.md` |
| Kim nima yozadi: dev, QA, automation muhandisi mas'uliyati | `docs/testing/03-kim-nima-yozadi-rollar-va-masuliyat.md` |
| QA ish jarayoni, test dizayni, riskka asoslangan ustuvorlik, bug hisoboti | `docs/testing/04-testrovshik-qanday-ishlashi-kerak-qa-ish.md` |
| JUnit 5, AssertJ, Mockito `STRICT_STUBS`, parametrlangan test, nomlash | `docs/testing/05-unit-test-asoslar-qoidalar-va-junit-5.md` |
| Spring'siz unit test, constructor injection, `Clock` va `Supplier` in'ektsiyasi | `docs/testing/06-unit-test-spring-loyihasida-kontekstsiz.md` |
| `@WebMvcTest`, `@DataJpaTest`, `@JsonTest`, `@RestClientTest`, kontekst keshi | `docs/testing/07-integratsion-test-spring-boot-slice-testlari.md` |
| Testcontainers, `@ServiceConnection`, reuse, PostgreSQL/Kafka/Redis konteyner | `docs/testing/08-testcontainers-bilan-real-infratuzilmada.md` |
| WireMock, MockWebServer, Pact/Spring Cloud Contract, consumer-driven kontrakt | `docs/testing/09-tashqi-servislarni-taqlid-qilish-va.md` |
| Test ma'lumotlari: builder, object mother, fixture, DB holatini tiklash | `docs/testing/10-test-malumotlarini-boshqarish.md` |
| `@WithMockUser`, tranzaksiya rollback tuzoqlari, `@Async`, konkurentlik testi | `docs/testing/11-xavfsizlik-tranzaksiya-asinxron-va.md` |
| E2E, Selenium/Playwright, page object, test muhiti | `docs/testing/12-end-to-end-va-ui-testlar.md` |
| JMeter/Gatling/k6, chaos, xavfsizlik skanerlash, yuk profilini tanlash | `docs/testing/13-nofunksional-testlar-performance-resilience.md` |
| ArchUnit, Spring Modulith verify, qoidani test qilib yozish | `docs/testing/14-arxitektura-testlari-va-kod-sifati.md` |
| CI pipeline bosqichlari, parallel ishga tushirish, test tanlash, artefaktlar | `docs/testing/15-ci-cd-da-test-pipeline.md` |
| Flaky test sabablari va tuzatish, test qarzi, `@Disabled` siyosati | `docs/testing/16-flaky-testlar-test-qarzi-va-test-kodini.md` |
| Coverage, mutation score, test yetukligi modeli, nimani o'lchash | `docs/testing/17-metrikalar-va-test-yetukligi-modeli.md` |
| Tayyor shablonlar: test strategiyasi, test reja, DoD, checklistlar | `docs/testing/18-shablonlar-checklistlar-va-malumotnoma.md` |

## Qattiq qoidalar

- H2 ni PostgreSQL o'rniga ishlatmang - dialekt farqi testni yolg'onchi
  qiladi. Testcontainers ishlating (8-bob).
- `Thread.sleep` test ichida yo'q. Awaitility yoki deterministik soat.
- `Instant.now()` va `UUID.randomUUID()` to'g'ridan-to'g'ri chaqirilmaydi -
  `Clock` va `Supplier` orqali in'ektsiya qilinadi (6-bob).
- Value object, DTO va JDK sinflari mock qilinmaydi.
- Coverage foizi yagona sifat mezoni emas; domen paketlari uchun mutation
  score o'lchanadi (17-bob).
- `@SpringBootTest` - oxirgi chora. Avval slice'ni ko'rib chiqing (7-bob).

Sonar coverage talablari va JaCoCo mexanikasi boshqa hujjatda:
`docs/sonarqube/README.md`.
