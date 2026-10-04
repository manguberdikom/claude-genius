# 4-bosqich: pattern tayinlash

Bu bosqich rejaning yuragi: **"shu joyda shu patternni ishlatasan"**. Natija -
jadval, unda har qator bitta aniq joyga bitta pattern bog'laydi va sababini
ko'rsatadi.

Pattern - maqsad emas, lug'at. Qoida: **muammo kodda allaqachon bo'lsa**, pattern
nomlanadi; dizaynni chiroyli ko'rsatish uchun emas.

## 4.1 To'rt savol darvozasi

Har pattern nomidan oldin to'rtta savolga javob bo'lishi shart. Bitta "yo'q" -
pattern rejaga kirmaydi.

1. **Muammo bormi va qayerda?** `fayl:qator` ko'rsatiladi. Kelajakda bo'lishi
   mumkin bo'lgan muammo - asos emas.
2. **Uchinchi marta uchradimi?** Ikki o'xshash joy - tasodif, uch - shakl.
   Istisno: xavfsizlik va ma'lumot yo'qolishi muammosi birinchi martadan hal
   qilinadi.
3. **Framework buni allaqachon bermaydimi?** Spring/JDK beradigan narsani qo'lda
   yozish - ortiqcha kod (4.4 ro'yxatiga qarang).
4. **Indirection narxi oqlanadimi?** Yangi interfeys + ikki sinf + bitta
   konfiguratsiya = o'qish uchun uch fayl. Agar `switch` ikki tarmoqli bo'lsa va
   o'smasa, `switch` qoladi.

Javoblar rejada ko'rinmaydi, lekin "Nega" ustuni shu javoblardan tug'iladi.

## 4.2 Qo'llanmadan qidirish tartibi

```bash
# 1. Alifbo indeksidan pattern nomini va bo'limini topish
grep -n "^- \[Strategy" java-spring-design-patterns.md
# -> 3.9 (GoF), 8.21 (Spring registry), 24.11 (lambda bilan)

# 2. Bo'limni o'qish (Tavsif / Spring'da qayerda / Keyslar / Ehtiyot bo'ling)
grep -n "^### 8\.21 " java-spring-design-patterns.md
sed -n '<topilgan qator>,+40p' java-spring-design-patterns.md

# 3. Anti-pattern tomonini tekshirish: Anti-patternlar bo'limi ro'yxati
grep -n "^### " java-spring-design-patterns.md | sed -n '/Anti-pattern/,$p' | head -80
```

Bir nomning bir nechta varianti bo'lsa (`Strategy`, `Strategy Registry via
Map<String, Bean>`, `Strategy via Lambdas / Functional Interfaces`),
**loyihaning idiomiga mos variant** tanlanadi: Spring loyihasida ko'pincha
`Map<String, Handler>` registri yoki lambda, uchta yangi sinf emas.

## 4.3 Simptomdan patternga xarita

Uchinchi ustun - `java-spring-design-patterns.md` ning alifbo indeksidagi
qidiruv kaliti, ya'ni patternning inglizcha nomi.

### Obyekt yaratish va konfiguratsiya

| Kodda ko'rinadi | Pattern | Qo'llanmada qidirish |
|---|---|---|
| `new Konkret()` o'nlab joyda, test qilib bo'lmaydi | Factory Method / Abstract Factory | `Factory Method` / `Abstract Factory` |
| Konstruktorda 6+ parametr, yarmi optional | Builder (Spring'da ko'pincha `record` + `@Builder`) | `Builder, Step Builder, Lombok @Builder` |
| Singleton bean ichida prototype kerak | `ObjectProvider` / `@Lookup` | `Provider / Supplier Injection` / `@Lookup Method Injection` |
| `getBean()` kod ichida chaqirilgan | Service Locator **o'rniga** konstruktor injection | `Service Locator` |
| Bir xil turdan bir nechta implementatsiya, tanlov noaniq | `@Primary` / `@Qualifier` | `@Primary / @Qualifier Disambiguation` |
| Konfiguratsiya qiymatlari `@Value` bilan sochilgan | `@ConfigurationProperties` | `@ConfigurationProperties Binding` |
| Bean faqat ma'lum shartda kerak | `@Conditional` / auto-configuration | `@Conditional & Auto-configuration` |

### Bog'liqlik va qatlamlar

| Kodda ko'rinadi | Pattern | Qo'llanmada qidirish |
|---|---|---|
| Tashqi API/SDK shakli bizning interfeysga mos emas | Adapter | `Adapter` |
| Tashqi modelning "iflosligi" domenga kirib kelgan | Anti-Corruption Layer | `Anti-Corruption Layer` |
| Domen paketi JPA/Kafka/web ga import qiladi | Ports & Adapters (Hexagonal) | `Hexagonal Architecture / Ports & Adapters` |
| Chaqiruvchi 5 ta servisni ketma-ket chaqiradi | Facade | `Facade` |
| Xulqni runtime da o'ramga qo'shish kerak (log, metrika, retry) | Decorator | `Decorator` |
| Kesh/lazy/kirish nazorati obyekt atrofida | Proxy | `Proxy` |
| Daraxt tuzilishi: yakka va guruh bir xil ishlatiladi | Composite | `Composite` |

### Service qatlam va biznes logika

| Kodda ko'rinadi | Pattern | Qo'llanmada qidirish |
|---|---|---|
| Bitta metodda `if (type == ...)` ning uchta nusxasi | Strategy (+ `Map<String,Bean>` registri) | `Strategy` / `Strategy Registry via Map<String, Bean>` |
| Strategiya bitta metodli va holatsiz | Lambda/funksional interfeys bilan Strategy | `Strategy via Lambdas / Functional Interfaces` |
| Obyekt holatiga qarab butunlay boshqa xulq | State | `State` |
| Operatsiyalar navbat, log, undo talab qiladi | Command / Use Case Handler | `Command` / `Command / Use Case Handler` |
| Controller 15 ta servisni biladi | Command Bus / Mediator | `Command Bus / Mediator` / `Mediator` |
| Algoritm bir xil, qadamlar farq qiladi | Template Method | `Template Method` |
| So'rov ketma-ket tekshiruvlardan o'tishi kerak | Chain of Responsibility | `Chain of Responsibility` |
| Filtr/shart shartlari kodda takrorlanadi | Specification | `Specification` |
| `null` tekshiruvi hamma joyda | Null Object | `Null Object` / `Null Object Usage in Spring` |
| Entity faqat getter/setter, logika service'da | Value Object + Aggregate (anemik modelni tuzatish) | `Value Object` / `Aggregate & Aggregate Root` |
| Service DB ga ketma-ket buyruq yozadi, domen yo'q | Transaction Script (ongli tanlov bo'lsa) | `Transaction Script` |
| Entity va DTO o'girish qo'lda, xato ko'p | Mapper (MapStruct) | `Mapper` |
| Validatsiya qoidalari sochilgan | Validator abstraksiyasi | `Validator Abstraction` |

### Ma'lumotlarga kirish

| Kodda ko'rinadi | Pattern | Qo'llanmada qidirish |
|---|---|---|
| Loop ichida repository chaqiruvi, sekin ro'yxat | N+1 yechimlari (fetch join, `@EntityGraph`, batch) | `N+1 Problem Solutions` |
| Entity to'liq yuklanadi, kerak 3 maydon | DTO proyeksiyasi | `DTO Projection` |
| `OFFSET 50000` sekin | Keyset / cursor pagination | `Keyset / Cursor Pagination` |
| Ko'p qator kiritiladi, har biri alohida `INSERT` | Bulk / batch insert | `Bulk / Batch insert` |
| Ikki foydalanuvchi bir qatorni ustiga yozadi | Optimistik lock (`@Version`) | `Optimistic Offline Lock` |
| Qat'iy navbat kerak, konflikt ko'p | Pessimistik lock | `Pessimistic Offline Lock` |
| Dinamik filtr uchun qo'lda SQL yig'ilgan | Specification (Spring Data) | `Specification` |
| Yozuv o'chirilmasligi kerak | Soft Delete + Audit Trail | `Soft Delete` / `Audit Trail / Auditing` |
| Og'ir hisobot so'rovi har safar hisoblanadi | Materialized View | `Materialized View` |
| Sxema o'zgaradi, lekin to'xtash mumkin emas | Expand/Contract | `Expand/Contract schema migration` / `Expand/Contract` |
| Lazy load view da ochiladi (`open-in-view`) | Open Session in View - **tuzatiladi**, ishlatilmaydi | `Open Session in View` |

### Integratsiya, xabarlar, hodisalar

| Kodda ko'rinadi | Pattern | Qo'llanmada qidirish |
|---|---|---|
| Tranzaksiya ichida Kafka/HTTP chaqiruvi | Transactional Outbox | `Transactional Outbox` |
| Ikki tizimga ketma-ket yoziladi | Dual Write muammosi -> Outbox yoki Saga | `Dual Write Problem` / `Saga (xoreografiya)` / `Saga (orkestratsiya)` |
| Takroriy xabar ikki marta ishlanadi | Idempotent Consumer / Receiver + inbox jadvali | `Idempotent Consumer` / `Idempotent Receiver` / `Idempotent Receiver store` |
| Xabar ishlanmay qoladi, yo'qoladi | Dead Letter Channel / retry topic | `Dead Letter Channel` / `Retry topic va Dead Letter Topic` |
| Consumer har xabarda source'dan ma'lumot so'raydi | Event-Carried State Transfer | `Event-Carried State Transfer` |
| Bir nechta servisga tegadigan biznes oqimi | Saga (xoreografiya yoki orkestratsiya) | `Saga (xoreografiya)` / `Saga (orkestratsiya)` |
| Domen hodisasi service ichida qo'lda publish qilinadi | Domain Event (+ Spring Data `@DomainEvents`) | `Domain Event` / `Domain Event Publishing from Service` / `Domain Events with Spring Data: AbstractAggregateRoot, @DomainEvents` |
| Klient ikki marta so'rov yuboradi (to'lov) | Idempotency Key | `Idempotency Key` |
| Mijoz uchun maxsus agregatsiya kerak | BFF / API Gateway | `Backend for Frontend, BFF` / `API Gateway` |

### Chidamlilik va resurslar

| Kodda ko'rinadi | Pattern | Qo'llanmada qidirish |
|---|---|---|
| Tashqi chaqiruvda timeout yo'q | Timeout -> Retry (jitter) -> Fallback | `Retry` / `Retry / Timeout / Fallback` |
| Tashqi servis uzilganda hamma thread band | Circuit Breaker + Bulkhead | `Circuit Breaker` / `Bulkhead` |
| Hamma mijoz bir xil resursni to'ldiradi | Rate Limiter / Throttling | `Rate Limiter` / `Rate Limiting` / `Throttling` |
| Xato bo'lsa ham javob qaytishi kerak | Graceful Degradation | `Graceful Degradation` |
| Retry retry ustiga qo'yilgan | Retry bo'roni - **anti-pattern**, budjet hisoblanadi | `Retry Storm` |
| Noto'g'ri konfiguratsiya ishga tushgandan keyin bilinadi | Fail Fast | `Fail Fast` |

### Keshlash

| Kodda ko'rinadi | Pattern | Qo'llanmada qidirish |
|---|---|---|
| Bir xil og'ir so'rov qayta-qayta | Cache-Aside (`@Cacheable` + aniq invalidatsiya) | `Cache-Aside` |
| Kesh bo'shaganda bazaga bir vaqtda urish | Cache stampede himoyasi | `Cache Stampede / Thundering Herd Protection` |

### Reliz va legacy

| Kodda ko'rinadi | Pattern | Qo'llanmada qidirish |
|---|---|---|
| Yangi xulq xavfli, qaytarish kerak bo'lishi mumkin | Feature Toggle | `Feature Toggle / Feature Flags` |
| Katta sinfni asta almashtirish kerak | Branch by Abstraction | `Branch by Abstraction` |
| Monolitdan qismni ajratish | Strangler Fig | `Strangler Fig Application` / `Strangler Fig` |
| Reliz paytida ikki versiya yonma-yon | Blue-Green / Canary | `Blue-Green Deployment` / `Canary Release` |

### Xavfsizlik va kuzatuvchanlik

| Kodda ko'rinadi | Pattern | Qo'llanmada qidirish |
|---|---|---|
| Token/ruxsat tekshiruvi har controllerda qo'lda | Access Token + filter chain | `Access Token` / `Xavfsizlik patternlari` |
| Log'da so'rovni kuzatib bo'lmaydi | Correlation ID / Trace ID propagatsiyasi | `Correlation ID / Trace ID Propagation` / `Correlation Identifier` |
| Log matn sifatida yozilgan, qidirib bo'lmaydi | Structured Logging | `Structured Logging` |
| Ilova tirik, lekin ishlamaydi | Health Check API + probe | `Health Check API` / `Health Probes: Liveness, Readiness, Startup` |
| Reliz paytida so'rovlar uziladi | Graceful Shutdown | `Graceful Shutdown` |
| Kim nimani o'zgartirganini bilish kerak | Audit Logging | `Audit Logging` |

### Test tomoni (to'liq roʻyxat: 5-bosqich)

| Ehtiyoj | Pattern | Qo'llanmada qidirish |
|---|---|---|
| Test ma'lumotini qurish takrorlanadi | Test Data Builder / Object Mother | `Test Data Builder` / `Object Mother` |
| Real DB/broker bilan test | Testcontainers + `@ServiceConnection` | `Testcontainers & @ServiceConnection` |
| Tashqi servis kontrakti buzilmasligi kerak | Contract Testing | `Contract Testing` / `Consumer-Driven Contracts` |
| Coverage bor, lekin xato o'tib ketadi | Mutation testing (PIT) | `Mutation Testing` |
| Test sekin, kontekst qayta ko'tariladi | Kontekst keshlash qoidalari | `@SpringBootTest & context caching` |

## 4.4 Spring allaqachon beradi - qo'lda yozilmaydi

| Qo'lda yozilgan narsa | Spring'dagi o'rni |
|---|---|
| Singleton registri, statik `getInstance()` | singleton scope bean (`Singleton`) |
| Qo'lda proxy, qo'lda tranzaksiya boshqaruvi | `@Transactional` proxy (`@Transactional Proxy & TransactionTemplate`) |
| Qo'lda retry sikli | `@Retryable` / Resilience4j (`Retry`) |
| Qo'lda kesh xaritasi | `@Cacheable` + CacheManager (`Cache-Aside`) |
| Qo'lda event bus | `ApplicationEventPublisher` (`Observer` / `Domain Event`) |
| Qo'lda validatsiya `if` lari | Bean Validation + `Validator` (`Validator Abstraction`) |
| Qo'lda DTO o'girish | MapStruct (`Mapper`) |
| Qo'lda konfiguratsiya o'qish | `@ConfigurationProperties` (`@ConfigurationProperties Binding`) |
| Qo'lda thread pool boshqaruvi | `TaskExecutor`, `@Async` (executor **sozlanadi**, `@Async Without Executor Configuration`) |

## 4.5 Anti-pattern darvozasi

Tanlangan har pattern `Anti-patternlar` bo'limi bilan solishtiriladi. Eng ko'p
uchraydiganlari:

| Tanlov | Xavf | Qo'llanmada qidirish |
|---|---|---|
| Singleton'ni o'zi yozish | yashirin global holat, test buziladi | `Singleton abuse / Static Cling` |
| Juda ko'p mas'uliyatli "Manager" sinf | God Object | `God Object` |
| Logikasiz entity + hamma logika service'da | Anemic Domain Model | `Anemic Domain Model` |
| Ikki tizimga to'g'ridan-to'g'ri yozish | Dual Writes | `Dual Writes` |
| Servislar bitta bazani bo'lishishi | Shared Database | `Shared Database` |
| Har testga `@SpringBootTest` | sekin pipeline | `@SpringBootTest for Everything` |
| `@Async` executor sozlanmagan | default pool, nazoratsiz | `@Async Without Executor Configuration` |
| `@Transactional` private metodda | proxy ishlamaydi, tranzaksiya yo'q | `@Transactional on Non-Public Methods` |
| Bitta implementatsiyali abstrakt fabrika | spekulyativ umumiylik / ortiqcha injinerlik | `Speculative Generality / Over-engineering` |
| Singleton bean ichida mutable maydon | ko'p thread'da race condition | `Mutable State in Singleton Beans` |

## 4.6 Rejaga yoziladigan qator formati

| Joy | Hozir | Pattern | Nega | Narxi | Qo'llanmada qidirish |
|---|---|---|---|---|---|
| `OrderService.java:142-198` | `if (type==CARD/CASH/CRYPTO)` uch joyda takrorlangan | Strategy, `Map<PaymentType, PaymentHandler>` registri | yangi to'lov turi faqat yangi bean qo'shadi, mavjud kod o'zgarmaydi | +1 interfeys, +3 sinf; stack trace bir qatlam uzayadi | `Strategy` / `Strategy Registry via Map<String, Bean>` |
| `OrderService.java:214` | tranzaksiya ichida `kafkaTemplate.send` | Transactional Outbox | broker yo'q bo'lsa tranzaksiya qaytmaydi, hodisa yo'qolmaydi | +1 jadval, +publisher, ~1 s kechikish | `Transactional Outbox` |
| `PaymentClient.java:30` | timeout yo'q `RestTemplate` | Timeout + Retry(jitter) + Circuit Breaker | tashqi servis sekinlashganda thread pool to'lmaydi | +Resilience4j dependency, +konfiguratsiya | `Retry` / `Circuit Breaker` |

"Narxi" ustuni majburiy: narxi yozilmagan pattern - sotuv, qaror emas.

## 4.7 Patternlarni birga ishlatish

- **Yaxshi juftliklar:** Strategy + Factory (tanlash + yaratish); Outbox +
  Idempotent Consumer (ikki uchi); Circuit Breaker + Fallback; Repository +
  Specification; Feature Toggle + Branch by Abstraction.
- **Ziddiyatli juftliklar:** Decorator zanjiri + AOP proxy (xulq ikki joyda
  yashiriladi); Event Sourcing + anemik model; CQRS + bitta kichik CRUD modul
  (ortiqcha); Saga + qat'iy tranzaksiya talabi.
- **Bir sinfda ikkitadan ortiq pattern** - belgi, ko'rgazma emas: mas'uliyat
  bo'linmagan.

## 4.8 Review ko'zi bilan ikki tomonlama tekshirish

Pattern tayinlashda ikki xato bir xil darajada qimmat: kerakli pattern yo'qligi
va keraksiz pattern qo'yilishi. Review qo'llanmasi aynan shu ikkisini ajratadi,
shuning uchun jadval tugagandan keyin u ikki ko'z bilan o'qiladi.

| Savol | Qarash | Belgisi |
|---|---|---|
| Qaysi pattern yetishmaydi? | review: `Dizayn pattern review I: yo'q patternni ko'rish` | takrorlangan shart, ochiq-oydin kengayish nuqtasi, tashqi chaqiruvda himoya yo'qligi |
| Qaysi pattern ortiqcha? | review: `Dizayn pattern review II: noto'g'ri va ortiqcha qo'llangan pattern` | bitta implementatsiyali interfeys, bir necha qatlamli o'ram, nomida pattern bor-u muammosi yo'q sinf |

Ikki savolga javob bitta jumla bo'lib rejaning pattern jadvali ostiga yoziladi:
nima qo'shilmadi va nega qo'shilmadi. Qo'shilmagan pattern ham qaror, shuning
uchun u ko'rinadigan joyda qoladi.

## Bosqich tugaganini qanday bilamiz

- Har qatorda `fayl:qator` bor
- Har pattern to'rt savoldan o'tgan va narxi yozilgan
- Har pattern `Anti-patternlar` bo'limi bilan solishtirilgan
- Framework beradigan narsa qo'lda yozilmaydi
- Pattern soni o'zgarishlar soniga mos (bitta tuzatishga uch pattern - ortiqcha)
- Yetishmayotgan va ortiqcha pattern savoli yozib javoblangan (4.8)
