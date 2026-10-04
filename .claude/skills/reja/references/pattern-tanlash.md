# 4-bosqich: pattern tayinlash

Bu bosqich rejaning yuragi: **"shu joyda shu patternni ishlatasan"**. Natija —
jadval, unda har qator bitta aniq joyga bitta pattern bog'laydi va sababini
ko'rsatadi.

Pattern — maqsad emas, lug'at. Qoida: **muammo kodda allaqachon bo'lsa**, pattern
nomlanadi; dizaynni chiroyli ko'rsatish uchun emas.

## 4.1 To'rt savol darvozasi

Har pattern nomidan oldin to'rtta savolga javob bo'lishi shart. Bitta "yo'q" —
pattern rejaga kirmaydi.

1. **Muammo bormi va qayerda?** `fayl:qator` ko'rsatiladi. Kelajakda bo'lishi
   mumkin bo'lgan muammo — asos emas.
2. **Uchinchi marta uchradimi?** Ikki o'xshash joy — tasodif, uch — shakl.
   Istisno: xavfsizlik va ma'lumot yo'qolishi muammosi birinchi martadan hal
   qilinadi.
3. **Framework buni allaqachon bermaydimi?** Spring/JDK beradigan narsani qo'lda
   yozish — ortiqcha kod (4.4 ro'yxatiga qarang).
4. **Indirection narxi oqlanadimi?** Yangi interfeys + ikki sinf + bitta
   konfiguratsiya = o'qish uchun uch fayl. Agar `switch` ikki tarmoqli bo'lsa va
   o'smasa, `switch` qoladi.

Javoblar rejada ko'rinmaydi, lekin "Nega" ustuni shu javoblardan tug'iladi.

## 4.2 Qo'llanmadan qidirish tartibi

```bash
# 1. Alifbo indeksidan bo'lim raqamini topish
grep -n "^- \[Strategy" java-spring-design-patterns.md
# -> 3.9 (GoF), 8.21 (Spring registry), 24.11 (lambda bilan)

# 2. Bo'limni o'qish (Tavsif / Spring'da qayerda / Keyslar / Ehtiyot bo'ling)
grep -n "^### 8\.21 " java-spring-design-patterns.md
sed -n '<topilgan qator>,+40p' java-spring-design-patterns.md

# 3. Anti-pattern tomonini tekshirish (25-bo'lim ro'yxati)
grep -n "^### 25\." java-spring-design-patterns.md | head -80
```

Bir nomning bir nechta varianti bo'lsa (Strategy: 3.9 / 8.21 / 24.11),
**loyihaning idiomiga mos variant** tanlanadi: Spring loyihasida ko'pincha
`Map<String, Handler>` registri (8.21) yoki lambda (24.11), uchta yangi sinf emas.

## 4.3 Simptomdan patternga xarita

Raqamlar — `java-spring-design-patterns.md` bo'limlari.

### Obyekt yaratish va konfiguratsiya

| Kodda ko'rinadi | Pattern | § |
|---|---|---|
| `new Konkret()` o'nlab joyda, test qilib bo'lmaydi | Factory Method / Abstract Factory | 1.7 / 1.8 |
| Konstruktorda 6+ parametr, yarmi optional | Builder (Spring'da ko'pincha `record` + `@Builder`) | 1.10 |
| Singleton bean ichida prototype kerak | `ObjectProvider` / `@Lookup` | 1.15 / 5.5 |
| `getBean()` kod ichida chaqirilgan | Service Locator **o'rniga** konstruktor injection | 1.16 |
| Bir xil turdan bir nechta implementatsiya, tanlov noaniq | `@Primary` / `@Qualifier` | 5.8 |
| Konfiguratsiya qiymatlari `@Value` bilan sochilgan | `@ConfigurationProperties` | 5.22 |
| Bean faqat ma'lum shartda kerak | `@Conditional` / auto-configuration | 5.24 |

### Bog'liqlik va qatlamlar

| Kodda ko'rinadi | Pattern | § |
|---|---|---|
| Tashqi API/SDK shakli bizning interfeysga mos emas | Adapter | 2.1 |
| Tashqi modelning "iflosligi" domenga kirib kelgan | Anti-Corruption Layer | 13.7 |
| Domen paketi JPA/Kafka/web ga import qiladi | Ports & Adapters (Hexagonal) | 12.2 |
| Chaqiruvchi 5 ta servisni ketma-ket chaqiradi | Facade | 2.5 |
| Xulqni runtime da o'ramga qo'shish kerak (log, metrika, retry) | Decorator | 2.4 |
| Kesh/lazy/kirish nazorati obyekt atrofida | Proxy | 2.7 |
| Daraxt tuzilishi: yakka va guruh bir xil ishlatiladi | Composite | 2.3 |

### Service qatlam va biznes logika

| Kodda ko'rinadi | Pattern | § |
|---|---|---|
| Bitta metodda `if (type == ...)` ning uchta nusxasi | Strategy (+ `Map<String,Bean>` registri) | 3.9 / 8.21 |
| Strategiya bitta metodli va holatsiz | Lambda/funksional interfeys bilan Strategy | 24.11 |
| Obyekt holatiga qarab butunlay boshqa xulq | State | 3.8 |
| Operatsiyalar navbat, log, undo talab qiladi | Command / Use Case Handler | 3.2 / 8.15 |
| Controller 15 ta servisni biladi | Command Bus / Mediator | 8.16 / 3.5 |
| Algoritm bir xil, qadamlar farq qiladi | Template Method | 3.10 |
| So'rov ketma-ket tekshiruvlardan o'tishi kerak | Chain of Responsibility | 3.1 |
| Filtr/shart shartlari kodda takrorlanadi | Specification | 3.13 / 9.35 / 13.22 |
| `null` tekshiruvi hamma joyda | Null Object | 3.12 / 5.40 |
| Entity faqat getter/setter, logika service'da | Value Object + Aggregate (anemik modelni tuzatish) | 13.14 / 13.15 |
| Service DB ga ketma-ket buyruq yozadi, domen yo'q | Transaction Script (ongli tanlov bo'lsa) | 8.1 |
| Entity va DTO o'girish qo'lda, xato ko'p | Mapper (MapStruct) | 8.14 |
| Validatsiya qoidalari sochilgan | Validator abstraksiyasi | 5.29 |

### Ma'lumotlarga kirish

| Kodda ko'rinadi | Pattern | § |
|---|---|---|
| Loop ichida repository chaqiruvi, sekin ro'yxat | N+1 yechimlari (fetch join, `@EntityGraph`, batch) | 9.27 |
| Entity to'liq yuklanadi, kerak 3 maydon | DTO proyeksiyasi | 9.22 |
| `OFFSET 50000` sekin | Keyset / cursor pagination | 7.7 |
| Ko'p qator kiritiladi, har biri alohida `INSERT` | Bulk / batch insert | 10.20 |
| Ikki foydalanuvchi bir qatorni ustiga yozadi | Optimistik lock (`@Version`) | 9.23 |
| Qat'iy navbat kerak, konflikt ko'p | Pessimistik lock | 9.24 |
| Dinamik filtr uchun qo'lda SQL yig'ilgan | Specification (Spring Data) | 9.35 |
| Yozuv o'chirilmasligi kerak | Soft Delete + Audit Trail | 10.1 / 10.2 |
| Og'ir hisobot so'rovi har safar hisoblanadi | Materialized View | 10.18 |
| Sxema o'zgaradi, lekin to'xtash mumkin emas | Expand/Contract | 10.5 / 7.23 |
| Lazy load view da ochiladi (`open-in-view`) | Open Session in View — **tuzatiladi**, ishlatilmaydi | 9.28 / 25.32 |

### Integratsiya, xabarlar, hodisalar

| Kodda ko'rinadi | Pattern | § |
|---|---|---|
| Tranzaksiya ichida Kafka/HTTP chaqiruvi | Transactional Outbox | 10.14 |
| Ikki tizimga ketma-ket yoziladi | Dual Write muammosi -> Outbox yoki Saga | 10.31 / 14.8 / 14.9 |
| Takroriy xabar ikki marta ishlanadi | Idempotent Consumer / Receiver + inbox jadvali | 14.18 / 16.16 / 10.15 |
| Xabar ishlanmay qoladi, yo'qoladi | Dead Letter Channel / retry topic | 15.11 / 16.35 |
| Consumer har xabarda source'dan ma'lumot so'raydi | Event-Carried State Transfer | 16.27 |
| Bir nechta servisga tegadigan biznes oqimi | Saga (xoreografiya yoki orkestratsiya) | 14.8 / 14.9 |
| Domen hodisasi service ichida qo'lda publish qilinadi | Domain Event (+ Spring Data `@DomainEvents`) | 13.20 / 8.26 / 13.33 |
| Klient ikki marta so'rov yuboradi (to'lov) | Idempotency Key | 7.9 |
| Mijoz uchun maxsus agregatsiya kerak | BFF / API Gateway | 7.19 / 14.27 |

### Chidamlilik va resurslar

| Kodda ko'rinadi | Pattern | § |
|---|---|---|
| Tashqi chaqiruvda timeout yo'q | Timeout -> Retry (jitter) -> Fallback | 17.1 / 19.10 |
| Tashqi servis uzilganda hamma thread band | Circuit Breaker + Bulkhead | 17.2 / 17.3 |
| Hamma mijoz bir xil resursni to'ldiradi | Rate Limiter / Throttling | 17.5 / 7.13 / 17.6 |
| Xato bo'lsa ham javob qaytishi kerak | Graceful Degradation | 17.37 |
| Retry retry ustiga qo'yilgan | Retry bo'roni — **anti-pattern**, budjet hisoblanadi | 17.42 |
| Noto'g'ri konfiguratsiya ishga tushgandan keyin bilinadi | Fail Fast | 17.8 |

### Keshlash

| Kodda ko'rinadi | Pattern | § |
|---|---|---|
| Bir xil og'ir so'rov qayta-qayta | Cache-Aside (`@Cacheable` + aniq invalidatsiya) | 11.1 |
| Kesh bo'shaganda bazaga bir vaqtda urish | Cache stampede himoyasi | 11.11 |

### Reliz va legacy

| Kodda ko'rinadi | Pattern | § |
|---|---|---|
| Yangi xulq xavfli, qaytarish kerak bo'lishi mumkin | Feature Toggle | 22.10 |
| Katta sinfni asta almashtirish kerak | Branch by Abstraction | 27.3 |
| Monolitdan qismni ajratish | Strangler Fig | 27.1 / 14.6 |
| Reliz paytida ikki versiya yonma-yon | Blue-Green / Canary | 22.6 / 22.7 |

### Xavfsizlik va kuzatuvchanlik

| Kodda ko'rinadi | Pattern | § |
|---|---|---|
| Token/ruxsat tekshiruvi har controllerda qo'lda | Access Token + filter chain | 14.24 / 18-bo'lim |
| Log'da so'rovni kuzatib bo'lmaydi | Correlation ID / Trace ID propagatsiyasi | 21.3 / 15.21 |
| Log matn sifatida yozilgan, qidirib bo'lmaydi | Structured Logging | 21.2 |
| Ilova tirik, lekin ishlamaydi | Health Check API + probe | 21.9 / 22.19 |
| Reliz paytida so'rovlar uziladi | Graceful Shutdown | 22.20 |
| Kim nimani o'zgartirganini bilish kerak | Audit Logging | 18.34 / 21.10 |

### Test tomoni (to'liq roʻyxat: 5-bosqich)

| Ehtiyoj | Pattern | § |
|---|---|---|
| Test ma'lumotini qurish takrorlanadi | Test Data Builder / Object Mother | 23.5 / 23.6 |
| Real DB/broker bilan test | Testcontainers + `@ServiceConnection` | 23.15 |
| Tashqi servis kontrakti buzilmasligi kerak | Contract Testing | 23.17 / 7.22 |
| Coverage bor, lekin xato o'tib ketadi | Mutation testing (PIT) | 23.10 |
| Test sekin, kontekst qayta ko'tariladi | Kontekst keshlash qoidalari | 23.12 |

## 4.4 Spring allaqachon beradi — qo'lda yozilmaydi

| Qo'lda yozilgan narsa | Spring'dagi o'rni |
|---|---|
| Singleton registri, statik `getInstance()` | singleton scope bean (§1.1) |
| Qo'lda proxy, qo'lda tranzaksiya boshqaruvi | `@Transactional` proxy (§5.17) |
| Qo'lda retry sikli | `@Retryable` / Resilience4j (§17.1) |
| Qo'lda kesh xaritasi | `@Cacheable` + CacheManager (§11.1) |
| Qo'lda event bus | `ApplicationEventPublisher` (§3.7, 13.20) |
| Qo'lda validatsiya `if` lari | Bean Validation + `Validator` (§5.29) |
| Qo'lda DTO o'girish | MapStruct (§8.14) |
| Qo'lda konfiguratsiya o'qish | `@ConfigurationProperties` (§5.22) |
| Qo'lda thread pool boshqaruvi | `TaskExecutor`, `@Async` (executor **sozlanadi**, §25.49) |

## 4.5 Anti-pattern darvozasi

Tanlangan har pattern 25-bo'limga solishtiriladi. Eng ko'p uchraydiganlari:

| Tanlov | Xavf | § |
|---|---|---|
| Singleton'ni o'zi yozish | yashirin global holat, test buziladi | 25.26 |
| Juda ko'p mas'uliyatli "Manager" sinf | God Object | 25.1 |
| Logikasiz entity + hamma logika service'da | Anemic Domain Model | 25.35 |
| Ikki tizimga to'g'ridan-to'g'ri yozish | Dual Writes | 25.69 |
| Servislar bitta bazani bo'lishishi | Shared Database | 25.56 |
| Har testga `@SpringBootTest` | sekin pipeline | 25.40 |
| `@Async` executor sozlanmagan | default pool, nazoratsiz | 25.49 |
| `@Transactional` private metodda | proxy ishlamaydi, tranzaksiya yo'q | 25.31 |
| Bitta implementatsiyali abstrakt fabrika | spekulyativ umumiylik / ortiqcha injinerlik | 25.25 |
| Singleton bean ichida mutable maydon | ko'p thread'da race condition | 25.48 |

## 4.6 Rejaga yoziladigan qator formati

| Joy | Hozir | Pattern | Nega | Narxi | § |
|---|---|---|---|---|---|
| `OrderService.java:142-198` | `if (type==CARD/CASH/CRYPTO)` uch joyda takrorlangan | Strategy, `Map<PaymentType, PaymentHandler>` registri | yangi to'lov turi faqat yangi bean qo'shadi, mavjud kod o'zgarmaydi | +1 interfeys, +3 sinf; stack trace bir qatlam uzayadi | 3.9, 8.21 |
| `OrderService.java:214` | tranzaksiya ichida `kafkaTemplate.send` | Transactional Outbox | broker yo'q bo'lsa tranzaksiya qaytmaydi, hodisa yo'qolmaydi | +1 jadval, +publisher, ~1 s kechikish | 10.14 |
| `PaymentClient.java:30` | timeout yo'q `RestTemplate` | Timeout + Retry(jitter) + Circuit Breaker | tashqi servis sekinlashganda thread pool to'lmaydi | +Resilience4j dependency, +konfiguratsiya | 17.1, 17.2 |

"Narxi" ustuni majburiy: narxi yozilmagan pattern — sotuv, qaror emas.

## 4.7 Patternlarni birga ishlatish

- **Yaxshi juftliklar:** Strategy + Factory (tanlash + yaratish); Outbox +
  Idempotent Consumer (ikki uchi); Circuit Breaker + Fallback; Repository +
  Specification; Feature Toggle + Branch by Abstraction.
- **Ziddiyatli juftliklar:** Decorator zanjiri + AOP proxy (xulq ikki joyda
  yashiriladi); Event Sourcing + anemik model; CQRS + bitta kichik CRUD modul
  (ortiqcha); Saga + qat'iy tranzaksiya talabi.
- **Bir sinfda ikkitadan ortiq pattern** — belgi, ko'rgazma emas: mas'uliyat
  bo'linmagan.

## Bosqich tugaganini qanday bilamiz

- Har qatorda `fayl:qator` bor
- Har pattern to'rt savoldan o'tgan va narxi yozilgan
- Har pattern 25-bo'lim bilan solishtirilgan
- Framework beradigan narsa qo'lda yozilmaydi
- Pattern soni o'zgarishlar soniga mos (bitta tuzatishga uch pattern — ortiqcha)
