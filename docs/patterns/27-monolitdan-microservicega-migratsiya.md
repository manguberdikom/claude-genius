<!-- doc: patterns | chapter: 27 | part:  -->

[Java Spring arxitektori bilishi kerak bo'lgan barcha dizayn patternlar](../../README.md) / [Dizayn patternlar](README.md)

# 27. Monolitdan microservice'ga migratsiya patternlari (Monolith to Microservices Migration Patterns)

<details>
<summary>Bu bo'limdagi 22 bo'lim</summary>

- [27.1 Bo'g'uvchi Anjir Ilovasi (Strangler Fig Application)](#271-boguvchi-anjir-ilovasi-strangler-fig-application)
- [27.2 UI Kompozitsiyasi (UI Composition)](#272-ui-kompozitsiyasi-ui-composition)
- [27.3 Abstraksiya Orqali Tarmoqlanish (Branch by Abstraction)](#273-abstraksiya-orqali-tarmoqlanish-branch-by-abstraction)
- [27.4 Parallel Ishga Tushirish (Parallel Run)](#274-parallel-ishga-tushirish-parallel-run)
- [27.5 Bezovchi Hamkor (Decorating Collaborator)](#275-bezovchi-hamkor-decorating-collaborator)
- [27.6 Ma'lumot O'zgarishini Ushlash (Change Data Capture)](#276-malumot-ozgarishini-ushlash-change-data-capture)
- [27.7 Ma'lumotlar Bazasi Ko'rinishi (Database View)](#277-malumotlar-bazasi-korinishi-database-view)
- [27.8 Ma'lumotlar Bazasini O'rovchi Servis (Database Wrapping Service)](#278-malumotlar-bazasini-orovchi-servis-database-wrapping-service)
- [27.9 Ma'lumotlar Bazasi Servis Interfeysi (Database-as-a-Service Interface)](#279-malumotlar-bazasi-servis-interfeysi-database-as-a-service-interface)
- [27.10 Agregatni Ochuvchi Monolit (Aggregate Exposing Monolith)](#2710-agregatni-ochuvchi-monolit-aggregate-exposing-monolith)
- [27.11 Ma'lumot Egaligini O'zgartirish (Change Data Ownership)](#2711-malumot-egaligini-ozgartirish-change-data-ownership)
- [27.12 Ma'lumotlarni ilova darajasida sinxronlashtirish (Synchronize Data in Application)](#2712-malumotlarni-ilova-darajasida-sinxronlashtirish-synchronize-data-in-application)
- [27.13 Tracer Write (Tracer Write)](#2713-tracer-write-tracer-write)
- [27.14 Jadvalni bo'lish (Split Table)](#2714-jadvalni-bolish-split-table)
- [27.15 Tashqi kalit munosabatini kodga ko'chirish (Move Foreign-Key Relationship to Code)](#2715-tashqi-kalit-munosabatini-kodga-kochirish-move-foreign-key-relationship-to-code)
- [27.16 Har bir bounded context uchun repository (Repository per Bounded Context)](#2716-har-bir-bounded-context-uchun-repository-repository-per-bounded-context)
- [27.17 Har bir bounded context uchun ma'lumotlar bazasi (Database per Bounded Context)](#2717-har-bir-bounded-context-uchun-malumotlar-bazasi-database-per-bounded-context)
- [27.18 Monolit ma'lumotga kirish qatlami sifatida (Monolith as Data Access Layer)](#2718-monolit-malumotga-kirish-qatlami-sifatida-monolith-as-data-access-layer)
- [27.19 Ko'p sxemali saqlash (Multischema Storage)](#2719-kop-sxemali-saqlash-multischema-storage)
- [27.20 Umumiy statik ma'lumot (Shared Static Data)](#2720-umumiy-statik-malumot-shared-static-data)
- [27.21 Maxsus reference data sxemasi (Dedicated Reference Data Schema)](#2721-maxsus-reference-data-sxemasi-dedicated-reference-data-schema)
- [27.22 Migratsiyani bosqichma-bosqich joriy etish va qaytarish (Incremental Rollout & Rollback of a Migration)](#2722-migratsiyani-bosqichma-bosqich-joriy-etish-va-qaytarish-incremental-rollout--rollback-of-a-migration)

</details>


Monolitdan microservice'ga o'tish — bu "katta portlash" (big bang) qayta yozish emas, balki ishlab turgan tizimni to'xtatmasdan, kichik-kichik qadamlar bilan funksionallikni va ma'lumotlarni ko'chirish jarayoni. Bu kategoriyadagi patternlar (asosan Sam Newman'ning "Monolith to Microservices" ishidan ma'lum) ikki qiyin masalani hal qiladi: chaqiruv oqimini (call flow) monolitdan yangi servisga xavfsiz yo'naltirish va umumiy ma'lumotlar bazasini (shared database) ajratish. Arxitektor uchun bu patternlar muhim, chunki migratsiyaning asosiy xavfi texnik emas — tashkiliy va ma'lumot izchilligi (data consistency) bilan bog'liq: har bir qadam orqaga qaytarilishi (reversible) va alohida release qilinishi kerak. Quyida har bir pattern Spring ekotizimidagi aniq amalga oshirish vositalari bilan beriladi.

## 27.1 Bo'g'uvchi Anjir Ilovasi (Strangler Fig Application)

**Tavsif:** Monolit oldiga proxy qo'yilib, trafik asta-sekin yangi servislarga yo'naltiriladi — monolit "bo'g'ilib", oxirida butunlay o'ladi. Boshida proxy barcha so'rovlarni monolitga uzatadi, keyin har bir ko'chirilgan endpoint uchun marshrut (route) yangi servisga almashtiriladi. Monolitning kodiga tegmasdan, HTTP yoki messaging darajasida ushlab olish (interception) amalga oshiriladi. Eng muhim xususiyati — har bir qadamni bir marshrut o'zgarishi bilan orqaga qaytarish mumkin.

**Spring'da qayerda uchraydi:** Spring Cloud Gateway (reactive `RouteLocator`, `RouteLocatorBuilder` yoki `spring.cloud.gateway.routes` konfiguratsiyasi) va Spring Boot 3.2+ dagi Spring Cloud Gateway Server MVC varianti asosiy vosita; `Path`, `Header`, `Weight` predicate'lari bilan trafikni bo'lish mumkin. Spring Framework 6.x ichida `ProxyExchange` (spring-cloud-gateway-mvc) yoki oddiy `RestClient`/`WebClient` asosidago `@RestController` fasad ham ishlaydi. Infratuzilma darajasida NGINX, Envoy, AWS ALB listener rule'lari shu vazifani bajaradi va Spring ilovasi faqat yangi endpoint'ni taqdim etadi. Progressiv o'tish uchun Spring Cloud Circuit Breaker (Resilience4j) va `Weight` predicate'i bilan canary qilinadi.

**Qo'llanish keyslari:**
- Legacy e-commerce monolitdan `/api/catalog/**` marshrutini yangi Catalog servisiga ko'chirish.
- Mobil BFF uchun eski SOAP monolit ustiga REST fasad qo'yib, endpoint'larni bitta-bitta almashtirish.
- To'lov moduli kabi yuqori yuklamali bo'limni alohida scale qilish uchun birinchi navbatda ajratish.
- Bir nechta mijoz (tenant) uchun yangi servisni faqat bitta tenant trafigida sinovdan o'tkazish.
- Mainframe yoki PHP legacy tizim oldiga Spring Cloud Gateway qo'yib, bosqichma-bosqich Java'ga o'tish.

**Ehtiyot bo'ling:** Agar monolit va yangi servis bir xil bazaga yozsa, strangler faqat illuziya beradi — ma'lumot bog'liqligi saqlanib qoladi, shuning uchun uni ma'lumotlar ajratish patternlari bilan birga qo'llash kerak. Proxy'ga biznes logika (ma'lumot transformatsiyasi, agregatsiya) joylashtirish eng tez-tez uchraydigan xato: gateway yangi "distributed monolith" markaziga aylanib qoladi.

## 27.2 UI Kompozitsiyasi (UI Composition)

**Tavsif:** Migratsiya chegarasi backend'da emas, foydalanuvchi interfeysida o'tkaziladi: ekranning bir qismi monolitdan, boshqa qismi yangi servisdan keladi va ular UI darajasida yig'iladi. Kompozitsiya sahifa bo'yicha (page-based), vidjet bo'yicha (widget/fragment) yoki micro-frontend ko'rinishida bo'ladi. Bu backend ma'lumotlar bazasiga tegmasdan, yangi funksionallikni foydalanuvchiga tez ko'rsatish imkonini beradi. Natijada jamoalar vertikal (UI + servis) tilimlarga egalik qiladi.

**Spring'da qayerda uchraydi:** Server-side kompozitsiya uchun Thymeleaf `th:insert`/`th:replace` fragmentlari va Spring MVC `ViewResolver`'lari, shuningdek Server-Side Includes (SSI) yoki Edge Side Includes (ESI) NGINX/Varnish darajasida ishlatiladi. Spring Boot 3.x da `spring-boot-starter-thymeleaf` bilan monolit layout saqlanib, yangi fragmentlar HTTP orqali `RestClient` bilan olinadi; Spring WebFlux'da `WebClient` va `Flux` bilan fragmentlar parallel yuklanadi. Micro-frontend yondashuvida kompozitsiya brauzerda (Webpack Module Federation, web components) bo'ladi va Spring tomoni faqat JSON/HTML fragment beradi — buni aniq ayting: pattern Spring'ning o'zida emas, UI qatlamida yashaydi. Spring Cloud Gateway marshrut bo'yicha statik SPA va yangi API'ni bitta origin ostida birlashtiradi (CORS muammosini yo'qotish uchun).

**Qo'llanish keyslari:**
- "Mening buyurtmalarim" sahifasidagi yetkazib berish holati vidjetini yangi Delivery servisidan olish.
- Legacy JSP admin panelida faqat "Hisobotlar" bo'limini yangi Angular/React SPA bilan almashtirish.
- Mobil ilovada bitta tab'ni yangi servis API'siga ulab, qolganini monolitda qoldirish.
- Marketing banner/tavsiya blokini alohida Recommendation servisidan render qilish.
- Bir nechta jamoa bitta portal'ni mustaqil deploy qilishi kerak bo'lganda.

**Ehtiyot bo'ling:** Vizual izchillik (dizayn tizimi, CSS, autentifikatsiya sessiyasi) buziladi — umumiy design system va SSO'ni oldin hal qilmasa, foydalanuvchi "chok"larni ko'radi. Ko'p fragmentni sinxron yuklash sahifa latency'sini oshiradi, shuning uchun timeout va fallback (bo'sh vidjet) majburiy.

## 27.3 Abstraksiya Orqali Tarmoqlanish (Branch by Abstraction)

**Tavsif:** Monolit ichidagi mavjud implementatsiya ustiga abstraksiya (interface) kiritiladi, so'ng shu interface'ning ikkinchi — yangi servisga chaqiruv qiladigan — implementatsiyasi yoziladi. Ikkala implementatsiya bir vaqtda kodda yashaydi va qaysi biri ishlashi feature flag bilan boshqariladi. Bu uzoq muddatli feature branch'larsiz, trunk'da ishlash imkonini beradi. Ishonch hosil bo'lgach, eski implementatsiya va flag o'chiriladi.

**Spring'da qayerda uchraydi:** Java interface + ikki `@Service` bean, tanlash `@ConditionalOnProperty`, `@Profile` yoki `@Qualifier` bilan; dinamik almashtirish uchun `ObjectProvider<T>`/`Map<String, PaymentGateway>` injection va runtime'da flag o'qish. Feature flag uchun Togglz, FF4J, Unleash yoki OpenFeature Spring Boot starter'lari; konfiguratsiyani qayta yuklash uchun Spring Cloud Config + `@RefreshScope`. Yangi implementatsiya tashqi servisga `RestClient` (Spring Framework 6.1+) yoki `@HttpExchange` interface client bilan murojaat qiladi va Resilience4j `@CircuitBreaker` bilan himoyalanadi.

```java
public interface InventoryPort { int available(String sku); }

@Service @ConditionalOnProperty(name="inventory.impl", havingValue="legacy", matchIfMissing=true)
class LegacyInventory implements InventoryPort { /* monolit JPA repository */ }
@Service @ConditionalOnProperty(name="inventory.impl", havingValue="remote")
class RemoteInventory implements InventoryPort {
    private final RestClient client;
    RemoteInventory(RestClient.Builder b) { this.client = b.baseUrl("http://inventory").build(); }
    public int available(String sku) {
        return client.get().uri("/stock/{sku}", sku).retrieve().body(Integer.class);
    }
}
```

**Qo'llanish keyslari:**
- Monolitdagi `PaymentService`ni yangi Payment microservice'ga bosqichma-bosqich o'tkazish.
- Email yuborish logikasini ichki SMTP kodidan yangi Notification servisiga ko'chirish.
- Narx hisoblash (pricing) algoritmini yangi servisda qayta yozib, flag bilan yoqish.
- Qidiruvni JPA `LIKE` so'rovlaridan alohida Search servisiga (Elasticsearch) o'tkazish.
- Katta refaktoring davomida trunk-based development'ni saqlab qolish.

**Ehtiyot bo'ling:** Flag'larni o'z vaqtida tozalamaslik "flag debt"ga olib keladi — har bir flag kod yo'llarini eksponensial ko'paytiradi va test matritsasini buzadi. Abstraksiyani juda kech, kod allaqachon chalkash bo'lganda kiritish patternning ma'nosini yo'qotadi: avval ichki chegarani (seam) toza qilib ajratish kerak.

## 27.4 Parallel Ishga Tushirish (Parallel Run)

**Tavsif:** Eski va yangi implementatsiya bir vaqtda, bir xil kirish ma'lumotlari bilan chaqiriladi, lekin faqat bittasining natijasi foydalanuvchiga qaytariladi; natijalar esa solishtirilib, farqlar qayd etiladi. Bu yangi servisning funksional to'g'riligini va ishlash tezligini real trafikda, xavfsiz tekshirish usuli. Odatda yangi (yorug'likdan tashqari) yo'l asinxron ishlatiladi, shunda latency'ga ta'sir qilmaydi. Yetarli ishonch to'plangach, natija manbasi almashtiriladi.

**Spring'da qayerda uchraydi:** Eski chaqiruv sinxron, yangisi `@Async` + `TaskExecutor` (Spring Boot 3.2+ da virtual thread'lar: `spring.threads.virtual.enabled=true`, Java 21+) bilan fon rejimida bajariladi; farqlar Micrometer `Counter`/`Timer` metrikalariga va strukturaviy log'ga yoziladi. `ApplicationEventPublisher` + `@TransactionalEventListener(phase = AFTER_COMMIT)` bilan solishtirishni asosiy tranzaksiyadan ajratish mumkin. Spring Cloud Gateway'da `Weight` predicate yoki maxsus `GlobalFilter` bilan "shadow traffic" nusxalash amalga oshiriladi; infratuzilma darajasida Envoy'ning request mirroring (`request_mirror_policies`) imkoniyati shu vazifani bajaradi. Natijalarni Spring Boot Actuator `/actuator/metrics` va Grafana dashboard orqali kuzatiladi.

**Qo'llanish keyslari:**
- Sug'urta mukofoti (premium) hisoblash algoritmini yangi servisda tekshirish — pul bilan bog'liq, xato qimmat.
- Soliq yoki chegirma hisoblash logikasini ko'chirishda tiyin darajasidagi farqlarni aniqlash.
- Kredit skoring modelini yangi servisga o'tkazishda eski qaror bilan moslikni o'lchash.
- Yangi Search servisining relevantligini eski natijalar bilan solishtirish.
- Ish haqi (payroll) hisob-kitobini yangi tizimda bir-ikki oy "quruq" rejimda yuritish.

**Ehtiyot bo'ling:** Nojo'ya ta'sirlar (side effects) ikki marta sodir bo'lishi mumkin — yangi yo'l email yubormasligi, to'lov qilmasligi yoki bazaga yozmasligi uchun uni albatta "dry-run"/idempotent qilib ajratish kerak. Shuningdek bu pattern yuklamani va infratuzilma xarajatini ikki baravar oshiradi, shuning uchun uni faqat yuqori riskli, aniq verifikatsiya talab qiladigan logikaga qo'llang va muddatini oldindan belgilang.

## 27.5 Bezovchi Hamkor (Decorating Collaborator)

**Tavsif:** Monolitning kodini o'zgartirish imkoni bo'lmaganda, uning chaqiruvlari proxy orqali kuzatiladi va so'rov/javob asosida yangi servisda qo'shimcha xatti-harakat ishga tushiriladi. Proxy monolitning javobini o'zgartirmaydi — faqat "bezaydi": hodisa (event) chiqaradi yoki yangi servisga chaqiruv qiladi. Shu tariqa yangi funksionallik monolitga tegmasdan qo'shiladi. Bu Strangler Fig'ning "yangi xatti-harakat qo'shish" varianti.

**Spring'da qayerda uchraydi:** Spring Cloud Gateway'da `GlobalFilter`/`GatewayFilterFactory` (yoki MVC variantida `HandlerFilterFunction`) javobni o'qib, Kafka'ga event yuboradi (`KafkaTemplate`, Spring for Apache Kafka 3.x). Monolit Spring ilovasi bo'lsa, `OncePerRequestFilter`, `HandlerInterceptor` yoki Spring AOP (`@Around` advice, `ProxyFactoryBean`) bilan bir xil natijaga erishiladi. Spring Integration'ning `WireTap` va `@ServiceActivator` komponentlari xabar oqimini nusxalab, yon kanalga uzatish uchun mo'ljallangan. Agar monolit umuman Java bo'lmasa, pattern infratuzilma (Envoy/NGINX `lua`, API Gateway) darajasida yashaydi va Spring servisi faqat iste'molchi (consumer) bo'ladi.

**Qo'llanish keyslari:**
- Buyurtma muvaffaqiyatli yaratilganda monolitga tegmasdan Loyalty servisida bonus ball berish.
- Ro'yxatdan o'tish javobini ushlab, yangi Notification servisi orqali "welcome" email yuborish (ruxsat berilgan hollarda).
- Legacy tizim javoblaridan analytics event'lar yaratib, yangi ma'lumot platformasiga uzatish.
- Mijoz profilini o'zgartirish chaqiruvidan keyin yangi CRM servisini sinxronlashtirish.
- Audit log'ni markaziy compliance servisiga yig'ish, monolit release'ini kutmasdan.

**Ehtiyot bo'ling:** Proxy monolit javobidan niyatni (intent) taxmin qiladi — HTTP 200 har doim biznes amal bajarilganini bildirmaydi, shuning uchun noto'g'ri trigger'lar paydo bo'lishi mumkin; murakkab shartlar kerak bo'lsa, Change Data Capture ishonchliroq. Yon kanaldagi xatolar asosiy oqimni buzmasligi uchun chaqiruv asinxron va idempotent bo'lishi shart.

## 27.6 Ma'lumot O'zgarishini Ushlash (Change Data Capture)

**Tavsif:** Monolitning kodiga ham, chaqiruvlariga ham tegmasdan, uning ma'lumotlar bazasidagi o'zgarishlar (transaction log) o'qilib, yangi servislarga event sifatida uzatiladi. Bu monolit "qo'lga tushmaydigan" bo'lganda — kodi yo'q, jamoa yo'q, release tsikli uzoq bo'lganda — ishlatiladigan oxirgi chora. CDC event'lari yangi servisning o'z ma'lumot nusxasini (read model) to'ldiradi yoki biznes jarayonini ishga tushiradi. Migratsiya nuqtai nazaridan bu monolitdan yangi dunyoga bir tomonlama ma'lumot "ko'prigi".

**Spring'da qayerda uchraydi:** Asosiy vosita — Debezium (PostgreSQL logical decoding, MySQL binlog, Oracle LogMiner) Kafka Connect orqali; Spring tomoni Spring for Apache Kafka 3.x `@KafkaListener` yoki Spring Cloud Stream Kafka binder bilan event'larni iste'mol qiladi. Debezium Engine'ni to'g'ridan-to'g'ri Spring Boot 3.x ilovasi ichida embedded rejimda ishga tushirish ham mumkin (`io.debezium:debezium-embedded`, `@Bean` sifatida `DebeziumEngine`). Buni aniq ayting: CDC Spring Framework'ning qismi emas — u ma'lumotlar bazasi va infratuzilma darajasidagi mexanizm, Spring ilovasi faqat consumer yoki engine host bo'ladi. Idempotentlik uchun qabul qilingan event'lar `@Transactional` ichida `processed_events` jadvaliga yoziladi.

**Qo'llanish keyslari:**
- Legacy monolit bazasidan Customer ma'lumotlarini yangi CRM servisiga real vaqtda ko'chirish.
- Ko'chirish davrida yangi servis bazasini monolit bilan sinxron saqlash (dual-write'dan qochish).
- Monolit jadvallaridan analytics/data lake'ga oqim (streaming ETL) qurish.
- Qidiruv indeksini (Elasticsearch) monolit bazasidagi o'zgarishlar bilan yangilash.
- Yangi servisga o'tishdan oldin tarixiy ma'lumotlarni snapshot + incremental tarzda yuklash.

**Ehtiyot bo'ling:** CDC yangi servisni monolitning jadval sxemasiga bog'laydi — bu eng kuchli coupling turlaridan biri, chunki monolit DBA'si ustun nomini o'zgartirsa, servis sinadi; shu sababli u vaqtinchalik ko'prik bo'lishi, oxir-oqibat aniq event shartnomasiga (Outbox) almashtirilishi kerak. Event tartibi, schema evolution va "replay" paytidagi dublikatlar uchun idempotent consumer majburiy.

## 27.7 Ma'lumotlar Bazasi Ko'rinishi (Database View)

**Tavsif:** Monolit bazasining to'g'ridan-to'g'ri jadvallarini ochish o'rniga, iste'molchiga faqat kerakli ustunlarni ko'rsatuvchi read-only view beriladi. View bu yerda "ma'lumot shartnomasi" (contract) rolini bajaradi: ichki sxema o'zgarsa, view saqlanib qoladi va iste'molchi buzilmaydi. Bu to'liq servis ajratishga vaqt yo'q bo'lganda, integration database'ni qisman tartibga solish usuli. Cheklovi — view read-only va bitta ma'lumotlar bazasi ichida ishlaydi.

**Spring'da qayerda uchraydi:** Flyway yoki Liquibase migratsiyasi bilan `CREATE VIEW` (yoki materialized view) yaratiladi; Spring Data JPA tomonida `@Entity @Immutable` (Hibernate 6.x) yoki `@Subselect`, yaxshisi — Spring Data JDBC/`JdbcClient` (Spring Framework 6.1+) yoki projection interface bilan o'qiladi. Faqat o'qish uchun `@Transactional(readOnly = true)` va alohida `DataSource` (read-only user, cheklangan `GRANT SELECT`) sozlanadi; `spring.jpa.hibernate.ddl-auto=none` bo'lishi shart. Pattern asosan ma'lumotlar bazasi darajasida yashaydi — Spring faqat uni iste'mol qiladi va migratsiya skriptlari orqali boshqaradi.

**Qo'llanish keyslari:**
- Hisobot servisiga monolitning 40 ustunli `customers` jadvalidan faqat 6 ustunni ochish.
- Yangi servis vaqtincha monolit ma'lumotini o'qishi kerak bo'lganda, jadval nomlariga bog'lanmaslik uchun.
- Monolit jadvalini refaktoring qilishda (ustun nomini o'zgartirish) eski nomni view orqali saqlab qolish.
- Maxfiy maydonlarni (passport, karta raqami) berkitib, qolgan ma'lumotni hamkor servisga ko'rsatish.
- Bir nechta jadvalni denormalizatsiya qilib, read model sifatida materialized view berish.

**Ehtiyot bo'ling:** View yozishni qo'llab-quvvatlamaydi va iste'molchilar bir xil bazaga bog'lanib qolgani uchun mustaqil deploy, mustaqil scale va texnologiya tanlash erkinligi yo'q — bu faqat o'tish davri uchun vaqtinchalik yechim. Murakkab yoki materialized view'lar monolit bazasiga qo'shimcha yuklama beradi va yangilanish kechikishini (staleness) keltirib chiqaradi.

## 27.8 Ma'lumotlar Bazasini O'rovchi Servis (Database Wrapping Service)

**Tavsif:** Umumiy bazaga ko'p iste'molchi to'g'ridan-to'g'ri ulangan bo'lsa, ularning oldiga shu ma'lumot ustida yagona egalik qiladigan yupqa servis qo'yiladi va barcha murojaatlar faqat uning API'si orqali o'tadi. Bu "ma'lumot bazasi — integratsiya nuqtasi" muammosini servis chegarasiga aylantiradi, lekin jadvallarni hali ko'chirmaydi. Servis boshida monolit sxemasining ustiga yupqa CRUD qatlam bo'lishi mumkin, keyin ichida o'z modelini rivojlantiradi. Asosiy foyda — sxemani o'zgartirish erkinligini qaytarib olish.

**Spring'da qayerda uchraydi:** Yupqa Spring Boot 3.x servisi: `@RestController` + Spring Data JPA/JDBC repository'lar, `spring-boot-starter-validation` bilan kirish tekshiruvi va OpenAPI shartnomasi (springdoc-openapi 2.x). Iste'molchilar tomonida `@HttpExchange` interface client yoki `RestClient` ishlatiladi, shartnoma esa Spring Cloud Contract bilan verifikatsiya qilinadi. Baza darajasida eski iste'molchilarning to'g'ridan-to'g'ri ulanishini `REVOKE` bilan to'sish va faqat wrapper servisga `GRANT` berish kerak — bu qism Spring'da emas, DBA darajasida bajariladi. Kesh va yuklamani kamaytirish uchun `@Cacheable` (Spring Cache abstraction, Caffeine/Redis) qo'llanadi.

**Qo'llanish keyslari:**
- 7 ta ilova to'g'ridan-to'g'ri o'qiyotgan `product_catalog` jadvalini bitta Catalog servisi ortiga yashirish.
- Ko'p jamoa yozadigan "umumiy" `users` jadvalini yagona Identity servisiga topshirish.
- Batch/ETL job'larni bazadan uzib, servis API'siga o'tkazish.
- Monolit sxemasini refaktoring qilishdan oldin iste'molchilarni izolyatsiya qilish.
- Ma'lumotga kirishni markazlashtirib, audit va rate limiting qo'shish.

**Ehtiyot bo'ling:** Wrapper servis jadval strukturasini 1:1 ko'rsatsa, u "anemik CRUD proxy"ga aylanadi va hech qanday coupling kamaymaydi — API biznes operatsiyalari (`reserveStock`) tilida bo'lishi kerak, jadval tilida emas. Shuningdek u yangi yagona nosozlik nuqtasi (single point of failure) va qo'shimcha latency keltiradi, shuning uchun kesh, timeout va circuit breaker oldindan rejalashtiriladi.

## 27.9 Ma'lumotlar Bazasi Servis Interfeysi (Database-as-a-Service Interface)

**Tavsif:** Ba'zi iste'molchilarga (hisobot tizimlari, BI, analitika) baribir SQL kerak bo'ladi — ularga ichki baza emas, maxsus ko'chiriladigan, faqat o'qish uchun mo'ljallangan alohida "reporting database" beriladi. Servis o'z ichki bazasidan bu tashqi bazaga mapping engine orqali ma'lumot ko'chiradi va tashqi sxema aniq shartnoma bo'lib qoladi. Shu tariqa ichki model erkin o'zgaradi, tashqi sxema esa stabil qoladi. Bu CQRS'ning read model g'oyasini "SQL endpoint" shaklida beradi.

**Spring'da qayerda uchraydi:** Spring Boot 3.x da ikki `DataSource` (`@Primary` ichki, ikkinchisi `@Qualifier("reportingDataSource")`) va mapping engine sifatida `@Scheduled` job, Spring Batch 5.x step'lari yoki Debezium/Kafka Connect sink. Ikkala sxema Flyway/Liquibase bilan alohida boshqariladi (`spring.flyway.locations` bir nechta); yozish `JdbcClient`/`NamedParameterJdbcTemplate` yoki Spring Batch `JdbcBatchItemWriter` bilan bajariladi. Event asosida yangilash uchun `@TransactionalEventListener` + `@KafkaListener` birgalikda ishlatiladi. Tashqi baza va unga kirish huquqlari infratuzilma darajasida (alohida instance, read-only role, resurs kvotasi) ta'minlanadi — Spring buni faqat to'ldiradi.

**Qo'llanish keyslari:**
- Moliyaviy hisobot jamoasiga Orders servisining stabil, denormalizatsiyalangan read sxemasini berish.
- BI vositalari (Tableau, Power BI, Metabase) uchun SQL endpoint taqdim etish.
- Data warehouse'ga ETL uchun manba sifatida xizmat qilish, ichki sxemani ochmasdan.
- Og'ir analitik so'rovlarni asosiy OLTP bazadan ajratib, performance'ni himoyalash.
- Monolitdan ajratilgan servisdan keyin eski hisobot so'rovlarini ishlashda davom ettirish.

**Ehtiyot bo'ling:** Tashqi sxema ham xuddi API kabi versiyalanishi va buzilmaydigan (backward-compatible) o'zgartirilishi kerak — "shunchaki baza" deb qarash uni boshqarilmaydigan integration database'ga qaytaradi. Yangilanish kechikishi (eventual consistency) iste'molchiga aniq hujjatlashtirilmasa, hisobotlardagi nomuvofiqlik ishonchni yo'qotadi.

## 27.10 Agregatni Ochuvchi Monolit (Aggregate Exposing Monolith)

**Tavsif:** Yangi servisga monolitdagi ma'lumot kerak bo'lganda, u bazaga tegmasdan monolitning o'zi taqdim etgan API orqali agregat (DDD ma'nosidagi Aggregate — masalan Customer, Order) oladi. Monolit shu ma'lumot ustida egalik qilishda davom etadi, lekin endi uni aniq shartnoma bilan chiqaradi. Bu Database View'dan kuchliroq: monolit biznes qoidalari va invariantlarini saqlab qoladi, iste'molchi esa sxemaga bog'lanmaydi. Ko'pincha monolitni "haqiqiy servis"ga aylantirishning birinchi qadami.

**Spring'da qayerda uchraydi:** Monolit Spring ilovasi bo'lsa — yangi `@RestController` yoki `@RepositoryRestResource` (Spring Data REST) endpoint, DTO'lar `record` (Java 17+) sifatida, shartnoma springdoc-openapi 2.x bilan hujjatlashtiriladi; o'zgarishlar haqida xabar berish uchun qo'shimcha ravishda Kafka'ga event (`KafkaTemplate`) chiqariladi. Iste'molchi tomonida `RestClient`, `@HttpExchange` interface client yoki `WebClient` va Resilience4j `@CircuitBreaker`/`@Retry` ishlatiladi. Monolit ichida modul chegarasini saqlash uchun Spring Modulith 1.x (`@ApplicationModule`, `ApplicationModuleTest`, `@DomainEvent`) juda mos keladi — bu ko'pincha ajratishdan oldingi "ichki chegara" bosqichi. Shartnoma regressiyasini Spring Cloud Contract yoki Pact bilan tekshiriladi.

**Qo'llanish keyslari:**
- Yangi Loyalty servisi mijoz ma'lumotini monolitning `/api/customers/{id}` endpoint'idan olishi.
- Hisob-faktura servisi buyurtma agregatini monolitdan o'qib, o'z hujjatini yaratishi.
- Yangi mobil BFF monolitdagi mahsulot agregatiga API orqali murojaat qilishi.
- Monolitni Spring Modulith bilan modullarga bo'lib, kelajakdagi servis chegaralarini sinab ko'rish.
- Bir nechta yangi servis uchun monolitni "ma'lumot manbasi" sifatida rasmiylashtirish.

**Ehtiyot bo'ling:** Monolit sinxron chaqiruvlar manbasi bo'lib qolsa, yangi servislar uning mavjudligiga bog'liq bo'ladi — bu "distributed monolith"ning klassik ko'rinishi; shuning uchun kesh, timeout, circuit breaker va imkon bo'lsa event asosidagi replikatsiya zarur. Agregat chegarasini noto'g'ri tanlash (butun jadvalni "agregat" deb ko'rsatish) API'ni jadval proyeksiyasiga aylantiradi va keyinchalik ajratishni qiyinlashtiradi.

## 27.11 Ma'lumot Egaligini O'zgartirish (Change Data Ownership)

**Tavsif:** Funksionallik yangi servisga ko'chgandan keyin, ma'lumotning egaligi ham ko'chadi: jadvallar yangi servis bazasiga o'tadi va monolit endi ularga faqat servis API'si orqali murojaat qiladi. Bu migratsiyaning eng murakkab, lekin eng muhim qadami — ungacha ajratish faqat yarim bajarilgan hisoblanadi. Jarayon odatda bosqichli bo'ladi: yangi servis yozishni oladi (write), monolit vaqtincha eski nusxani o'qiydi, keyin monolit o'qishni ham API'ga o'tkazadi va eski jadval o'chiriladi. Natijada foreign key va bitta ACID tranzaksiya o'rniga saga, event va eventual consistency keladi.

**Spring'da qayerda uchraydi:** Ko'chish davrida ikki yozuvdan (dual-write) qochish uchun Transactional Outbox + Debezium yoki Spring Modulith 1.x `@Externalized` event publication registry ishlatiladi; monolitdagi `@OneToMany` JPA assotsiatsiyalari oddiy ID maydoni va `RestClient` chaqiruviga aylantiriladi. Sxema o'zgarishi Flyway/Liquibase migratsiyalari bilan expand-contract uslubida bosqichma-bosqich bajariladi; birlashtirilgan (join) so'rovlar o'rniga API kompozitsiyasi yoki CQRS read model quriladi. Taqsimlangan jarayon izchilligi uchun saga orkestratsiyasi (Spring Statemachine, Camunda, Temporal Java SDK yoki qo'lda yozilgan `@KafkaListener` state machine) va idempotentlik jadvali kerak bo'ladi. Ma'lumotni ko'chirishning o'zi Spring Batch 5.x job'lari yoki CDC bilan amalga oshiriladi.

**Qo'llanish keyslari:**
- `orders` va `order_items` jadvallarini monolitdan Order servisining o'z bazasiga ko'chirish.
- Monolitdagi `invoices` ustidagi yozish huquqini Billing servisiga topshirib, monolitni read-only qilish.
- Monolit bilan servis o'rtasidagi foreign key'ni olib tashlab, ID + API chaqiruviga o'tish.
- Umumiy `users` jadvalini Identity servisiga ko'chirib, parol va sessiya egaligini bir joyga olish.
- Ikki fazali ko'chish: avval write, keyin read trafikini almashtirib, eski jadvalni arxivlash.

**Ehtiyot bo'ling:** Dual-write (monolit ham, servis ham bir vaqtda ikki joyga yozishi) — eng xavfli anti-pattern: tranzaksiyasiz ikki yozuv ma'lumotni jim-jitlik bilan buzadi, shuning uchun har doim bitta egali yozuv + Outbox/CDC replikatsiyasi tanlanadi. Foreign key va `JOIN`larni yo'qotish hisobotlarni, validatsiyani va "hammasi yoki hech narsa" kafolatini buzadi — buni oldindan saga, compensating transaction va monitoring bilan rejalashtirmasa, migratsiya ishlab chiqarishda (production) ma'lumot nomuvofiqligi bilan tugaydi.

## 27.12 Ma'lumotlarni ilova darajasida sinxronlashtirish (Synchronize Data in Application)

**Tavsif:** Monolit va yangi microservice bir vaqtning o'zida bir xil ma'lumotga muhtoj bo'lganda, ma'lumot ko'chirish uchun uch fazali yondashuv qo'llaniladi: avval yangi bazaga bir martalik bulk migratsiya (backfill) qilinadi, so'ngra ilova kodi ikki bazaga parallel yozishni boshlaydi (dual write), nihoyat o'qish manbasi bosqichma-bosqich yangi bazaga ko'chiriladi. Sinxronlashtirish mas'uliyati ma'lumotlar bazasi replikatsiyasi emas, balki ilova kodining o'zida bo'ladi — shuning uchun pattern nomi "in Application". Bu uzilishsiz (zero-downtime) migratsiya imkonini beradi va har qanday fazada orqaga qaytish (rollback) yo'lini ochiq qoldiradi.

**Spring'da qayerda uchraydi:** Service qatlamida ikkita alohida `DataSource` va ikkita `JdbcTemplate`/`EntityManager` bean'i e'lon qilinadi (`@Primary` va `@Qualifier` bilan ajratiladi), `ChainedTransactionManager` o'rniga odatda birinchi bazaga `@Transactional` yozuv, ikkinchisiga `TransactionSynchronization` yoki `@TransactionalEventListener(phase = AFTER_COMMIT)` orqali yozuv bajariladi. Bulk backfill uchun Spring Batch (`JdbcPagingItemReader` + `JdbcBatchItemWriter`, chunk-oriented step, `JobRepository` orqali restart) juda mos keladi. O'qish/yozish marshrutini boshqarish uchun `AbstractRoutingDataSource` yoki feature flag kutubxonasi (Togglz, FF4j, Unleash) ishlatiladi; kod darajasidagi dual write'ga alternativa sifatida Debezium (CDC) infratuzilma darajasida qo'llanadi.

**Qo'llanish keyslari:**
- Monolit `orders` jadvalidan yangi Order Service'ning alohida PostgreSQL bazasiga uzilishsiz ko'chish.
- Legacy Oracle bazasidan PostgreSQL'ga bosqichma-bosqich migratsiya, ikki baza bir necha hafta parallel yashaydi.
- Yangi service'ni "shadow mode"da ishga tushirib, uning ma'lumotlari monolitdagi bilan mos kelishini tekshirish.
- On-premise bazadan cloud-managed bazaga (RDS/Cloud SQL) ko'chirishda ilova ishlab turgan holda sinxronlik ushlab turish.
- Yangi, boshqacha modellashtirilgan sxemaga (masalan, normalizatsiyadan denormalizatsiyaga) o'tishda ikki model parallel to'ldirilishi.

**Ehtiyot bo'ling:** Dual write atomik emas — ikkinchi yozuv muvaffaqiyatsiz bo'lsa bazalar ajralib ketadi, shuning uchun doimiy reconciliation job va drift metrikasi majburiy. Agar o'qish ham yozish ham faqat bitta service'dan o'tmasa (monolitda boshqa modullar to'g'ridan-to'g'ri jadvalga yozsa), bu pattern buziladi — bunday holatda CDC asosidagi yondashuv xavfsizroq.

## 27.13 Tracer Write (Tracer Write)

**Tavsif:** Synchronize Data in Application'ning rivojlangan shakli: ma'lumotning yangi service'dagi nusxasi "source of truth" sifatida bosqichma-bosqich, atribut-atribut yoki use-case-use-case tan olinadi. Boshida yangi service faqat kichik bir qism maydonlar uchun haqiqat manbasi bo'ladi, qolganlari monolitda qoladi; vaqt o'tishi bilan "chiziq" (tracer) siljib boradi va nihoyat butun ma'lumot yangi service'ga o'tadi. Bu Big Bang migratsiyasini juda kichik, qaytarib olinadigan qadamlarga bo'lib tashlaydi.

**Spring'da qayerda uchraydi:** Monolitdagi domain sinfining getter'lari ichiga yoki repository fasad'iga qaror nuqtasi qo'yiladi: ma'lum maydon uchun yangi service'ga `RestClient`/`WebClient` (Spring Framework 6.1+ `RestClient`, Spring Boot 3.2+) yoki `@HttpExchange` interface client orqali so'rov yuboriladi, qolgani lokal JPA entity'dan o'qiladi. Migratsiya chizig'i feature flag (Togglz/Unleash) yoki `@ConfigurationProperties` orqali boshqariladi; har bir qadam uchun `Micrometer` counter'lari ("read-from-new", "read-from-old") qo'yilib Grafana'da kuzatiladi. Sinxronlik Debezium Kafka Connect yoki `@TransactionalEventListener` + `ApplicationEventPublisher` orqali ikki tomonlama saqlanadi.

**Qo'llanish keyslari:**
- Customer ma'lumotining avval faqat `marketingPreferences` qismini yangi Customer Service'ga o'tkazish, keyin `address`, keyin butun profil.
- Yirik `product` jadvalini Catalog Service'ga use-case bo'yicha ko'chirish: avval "product search", keyin "pricing", keyin "inventory".
- Yuz millionlab satrli jadvalni bir kecha ichida ko'chirish imkoni yo'q bo'lgan paytda migratsiyani oylarga cho'zish.
- Riskli core domain (masalan, billing) migratsiyasini har bir qadamda rollback qilish mumkin bo'lgan holda bajarish.
- Yangi service'ning ishlash sifatini real trafikda, kichik maydon ustida sinovdan o'tkazish.

**Ehtiyot bo'ling:** Migratsiya davrida ikki tomonlama sinxronlik (bidirectional sync) cheksiz loop va yozuv konfliktlarini keltirib chiqarishi mumkin — har bir maydon uchun aniq bitta yozuvchi (single writer) bo'lishini ta'minlang. "Tracer" holatida uzoq qolish eng katta xavf: vaqtinchalik murakkablik doimiyga aylanmasligi uchun har bir qadamga deadline va "eski kodni o'chirish" tiketi biriktirilsin.

## 27.14 Jadvalni bo'lish (Split Table)

**Tavsif:** Bitta jadval ikki yoki undan ko'p bounded context'ga tegishli ustunlarni saqlayotgan bo'lsa, jadval vertikal ravishda bo'linadi va har bir bo'lagi o'z service'i bazasiga ko'chiriladi. Masalan `item` jadvalidagi `sku`, `name` Catalog'ga, `stock_count` Warehouse'ga ketadi. Agar bo'linadigan ustunlar bitta tranzaksiyada o'zgarsa, bo'lishdan oldin ushbu tranzaksiya saga yoki eventual consistency bilan almashtirilishi kerak — shuning uchun bu pattern ko'pincha Saga patterniga olib keladi.

**Spring'da qayerda uchraydi:** Bu avvalo sxema darajasidagi o'zgarish: Flyway (`spring.flyway`) yoki Liquibase migratsiya skriptlari bilan yangi jadvallar yaratiladi va ma'lumot `INSERT ... SELECT` yoki Spring Batch job'i orqali ko'chiriladi. Kod tomonida bitta JPA `@Entity` ikkita entity'ga va bitta `JpaRepository` ikkita repository'ga ajratiladi; bitta `@Transactional` metod ichidagi yozuv Saga'ga (Axon Framework, Eventuate Tram yoki qo'lda yozilgan orchestrator + Outbox) aylantiriladi. Avvalgi birlashgan o'qishlarni saqlab qolish uchun vaqtincha database view yoki API-level composition (`RestClient` bilan ikki service'dan o'qib birlashtirish) ishlatiladi.

**Qo'llanish keyslari:**
- Legacy `customer` jadvalidagi login ma'lumotlarini Identity Service'ga, manzil va buyurtma tarixini Customer Service'ga ajratish.
- `item` jadvalidagi narx va ombor qoldig'ini Pricing va Inventory service'lariga bo'lish.
- Bitta keng `order` jadvalini Order (status, mijoz) va Payment (to'lov holati, tranzaksiya ID) bo'laklariga ajratish.
- God-table'ni (100+ ustun) bo'lib, har bir jamoaga o'z sxemasi ustida mustaqil DDL qilish imkonini berish.
- PII ustunlarini alohida, shifrlangan va audit qilinadigan sxemaga chiqarish (GDPR talabi).

**Ehtiyot bo'ling:** Bo'lishdan keyin avval bitta ACID tranzaksiya bo'lgan yozuv eventual consistent bo'ladi — biznes bu holatni (masalan, "ombor hali yangilanmagan") qabul qilishga tayyormi, buni mahsulot egasidan oldin so'rang. Jadvalni bo'lishdan oldin domainni to'g'ri modellashtirmaslik eng keng tarqalgan xato: noto'g'ri chiziq bo'yicha bo'lingan jadval service'lar orasida doimiy chatty integratsiya tug'diradi.

## 27.15 Tashqi kalit munosabatini kodga ko'chirish (Move Foreign-Key Relationship to Code)

**Tavsif:** Monolit bazasida ikki jadval o'rtasidagi `FOREIGN KEY` constraint ularni turli service'lar bazasiga ajratishga to'sqinlik qiladi. Bu patternda FK olib tashlanadi va JOIN'ning o'rniga service chaqiruvi qo'yiladi: egalik qiluvchi service faqat ID'ni saqlaydi, bog'liq ma'lumotni esa boshqa service'ning API'sidan oladi. Referensial yaxlitlikni ta'minlash bazadan ilova kodiga (va "orphan" yozuvlarni tozalovchi jarayonlarga) o'tadi.

**Spring'da qayerda uchraydi:** JPA'da `@ManyToOne @JoinColumn` bilan bog'langan assotsiatsiya oddiy skalyar maydonga (`private Long catalogItemId;` yoki `UUID`) almashtiriladi va DDL'dan FK Flyway migratsiyasi bilan olib tashlanadi. Ma'lumot olish uchun `RestClient` / `@HttpExchange` HTTP interface client yoki gRPC stub ishlatiladi; N+1 chaqiruvlardan qochish uchun batch endpoint (`GET /items?ids=...`) va `@Cacheable` (Caffeine yoki Redis, `spring-boot-starter-cache`) qo'llanadi. Chidamlilik uchun Resilience4j (`@CircuitBreaker`, `@Retry`, `@Bulkhead`) va `RestClient` timeout konfiguratsiyasi majburiy bo'ladi.

```java
@Entity
class OrderLine {
    @Id @GeneratedValue Long id;
    private UUID catalogItemId; // FK emas, faqat ID
    private int quantity;
}
```

**Qo'llanish keyslari:**
- `order_line.item_id` → `catalog_item.id` FK'sini olib tashlab, Order va Catalog service'larini ajratish.
- Hisobot jadvalidagi `user_id` FK'sini olib tashlab, foydalanuvchi nomini Identity Service'dan olish.
- Service'lar o'rtasida "soft reference" qilib, biri o'chganda ikkinchisi ishlab turishini ta'minlash.
- JOIN'li og'ir hisobot so'rovini CQRS read model yoki API composition bilan almashtirish.
- Turli jamoalar egalik qiladigan jadvallar o'rtasidagi deployment bog'liqligini uzish.

**Ehtiyot bo'ling:** Baza endi yaxlitlikni kafolatlamaydi — "o'lik" ID'lar (orphan) paydo bo'ladi, shuning uchun o'chirishni soft delete qilib, davriy consistency tekshiruvi va "nomalum element" uchun graceful degradation qo'shish kerak. Har bir satr uchun alohida HTTP chaqiruv qilish (N+1 over the network) bu patternning eng og'riqli antipatterni: batch API va cache'ni loyihaning boshida rejalashtiring.

## 27.16 Har bir bounded context uchun repository (Repository per Bounded Context)

**Tavsif:** Monolitda bitta katta repository/DAO qatlami butun bazani qamrab olgan bo'ladi. Bu patternda baza hali ham bitta, ammo data access kodi bounded context'lar bo'yicha alohida repository guruhlariga ajratiladi: har bir modul faqat o'z repository'lari orqali o'z jadvallariga murojaat qiladi. Bu monolit ichida "logical decomposition" bo'lib, service'larga ajratishdan oldingi eng arzon va eng xavfsiz qadam — bazani bo'lish keyingi bosqichda ancha osonlashadi.

**Spring'da qayerda uchraydi:** `@EnableJpaRepositories(basePackages = "com.shop.catalog.repo", entityManagerFactoryRef = ..., transactionManagerRef = ...)` orqali har bir context uchun alohida repository scan zonasi belgilanadi; Spring Modulith (1.x) `@ApplicationModule` va `ApplicationModules.verify()` testi bilan modullar orasidagi noqonuniy repository importlarini build vaqtida buzadi. ArchUnit qoidalari (`noClasses().that().resideInAPackage("..catalog..").should().accessClassesThat().resideInAPackage("..inventory.repo..")`) bilan chegara mustahkamlanadi. Paketlarni `package-private` repository interface'lari va public service fasadlari bilan yopish Spring'da tabiiy ishlaydi.

**Qo'llanish keyslari:**
- Monolitni bo'lishdan oldin kod bazasini context'lar bo'yicha "xaritalash" va aralash murojaatlarni topish.
- Katta `CommonDao`/`GenericRepository` sinfini modulga xos repository'larga sindirish.
- Spring Modulith bilan modular monolit qurib, keyin eng og'ir modulni service'ga chiqarish.
- Jamoalar orasida egalik chegaralarini aniqlash: qaysi jadvalga kim yozadi degan savolga javob berish.
- Monolit ichida har bir modul uchun alohida `DataSource`'ga o'tishga tayyorgarlik.

**Ehtiyot bo'ling:** Repository'lar ajratilgan bo'lsa-da, baza bitta bo'lgani uchun DDL hali ham umumiy va developer'lar "tezlik uchun" boshqa context jadvaliga JOIN qilish vasvasasiga tushadi — bu intizomni faqat avtomatik test (Modulith/ArchUnit) saqlab turadi. Bu pattern yakuniy maqsad emas, oraliq bosqich: unda haddan tashqari uzoq qolish "distributed monolith"ga emas, "yashirin bog'langan monolit"ga olib keladi.

## 27.17 Har bir bounded context uchun ma'lumotlar bazasi (Database per Bounded Context)

**Tavsif:** Repository'lar ajratilgandan keyingi keyingi qadam — har bir bounded context o'z sxemasi yoki o'z baza instansiyasini oladi, service'lar esa hali ham bitta deployment unit (monolit) ichida qoladi. Bu "monolitni ajratishdan oldin bazani ajratish" strategiyasi: eng og'ir va eng xavfli ish (ma'lumotni bo'lish, FK'larni olib tashlash, JOIN'larni kodga ko'chirish) deployment o'zgarishidan ajratib bajariladi. Natijada keyinchalik modulni service sifatida chiqarish deyarli mexanik ish bo'lib qoladi.

**Spring'da qayerda uchraydi:** Har bir context uchun alohida `DataSource`, `LocalContainerEntityManagerFactoryBean` va `JpaTransactionManager` bean'lari e'lon qilinadi (`@ConfigurationProperties("app.datasource.catalog")` + `DataSourceBuilder`), har biriga o'z Flyway instansiyasi (`spring.flyway.locations` yoki programmatik `Flyway.configure()`) biriktiriladi. Context'lar oshib ketadigan yozuvlar uchun XA/`ChainedTransactionManager`dan ko'ra Outbox + `@TransactionalEventListener` yoki Saga tanlanadi. Testlarda Testcontainers (`@ServiceConnection`, Spring Boot 3.1+) bilan har bir sxema uchun alohida konteyner ko'tarilib, chegaralar real tekshiriladi.

**Qo'llanish keyslari:**
- Monolitni saqlab turgan holda `catalog`, `inventory`, `billing` uchun uchta alohida PostgreSQL sxemasiga o'tish.
- Yuklamasi juda farq qiladigan modulni (masalan, reporting) alohida read-optimized bazaga chiqarish.
- Service'ga ajratish rejasidagi modul uchun baza chegarasini oldindan sinovdan o'tkazish.
- Har bir jamoaga o'z migratsiya skriptlari va DDL deploy jadvalini berish.
- Compliance talabi bo'lgan ma'lumotni (to'lov kartalari, PII) alohida, qattiq nazoratli bazaga ajratish.

**Ehtiyot bo'ling:** Bazani bo'lgandan so'ng cross-context JOIN'lar yo'qoladi va ba'zi hisobotlar sindirilishi mumkin — migratsiyadan oldin barcha hisobot va analitik so'rovlarni inventarizatsiya qilib, ularni replica, data warehouse yoki CQRS read model'ga ko'chirishni rejalashtiring. Distributed tranzaksiya (XA) bilan muammoni "yopish" vasvasasiga tushmang: bu ishlash tezligi va operatsion murakkablikni keskin oshiradi.

## 27.18 Monolit ma'lumotga kirish qatlami sifatida (Monolith as Data Access Layer)

**Tavsif:** Yangi service monolit bazasiga to'g'ridan-to'g'ri ulanish o'rniga monolitda yaratilgan API orqali ma'lumot oladi. Bu patternda monolit o'z ma'lumoti uchun "haqiqat manbai" va yagona yozuvchi bo'lib qoladi, yangi service esa uning mijozi bo'ladi. Ma'lumotni ko'chirish qiyin yoki hali vaqti kelmagan, lekin yangi funksionallikni alohida service sifatida yozish kerak bo'lgan hollarda ideal: baza sxemasi yashirin qoladi va keyinchalik ma'lumot ko'chirilganda API shartnomasi o'zgarmaydi.

**Spring'da qayerda uchraydi:** Monolitda yangi REST endpoint'lar `@RestController` + DTO (ko'pincha Java record) bilan ochiladi; shartnoma OpenAPI (springdoc-openapi 2.x) orqali hujjatlanadi va Spring Cloud Contract yoki Pact bilan consumer-driven test qilinadi. Yangi service tomonida `RestClient` yoki `@HttpExchange` interface client, Resilience4j `@CircuitBreaker` va `@Cacheable` ishlatiladi. O'qish yuklamasini kamaytirish uchun monolit `ETag`/`If-None-Match` (Spring'ning `ShallowEtagHeaderFilter`) yoki `Cache-Control` qo'yadi; katta hajmdagi o'qish uchun esa monolit o'zgarish event'larini Kafka'ga (`spring-kafka`) chiqaradi.

**Qo'llanish keyslari:**
- Yangi Recommendation Service monolitdagi mijoz profilini monolit API'si orqali o'qishi.
- Mobil ilova uchun yangi BFF service yozib, ma'lumotni hali monolitdan olish.
- Hali ko'chirilmagan legacy `customer` ma'lumotiga Shared Database antipatternidan qochib murojaat qilish.
- Monolit bazasiga kirishni bitta nazorat nuqtasiga yig'ib, audit va rate limiting qo'shish.
- Vaqtinchalik qadam: API birinchi bo'lib yaratiladi, keyin uning orqasidagi ma'lumot sekin-asta yangi service'ga ko'chiriladi.

**Ehtiyot bo'ling:** Monolitga qattiq bog'lanish saqlanadi — monolit ishdan chiqsa yangi service ham ishlamaydi, shuning uchun circuit breaker, timeout va cache bilan graceful degradation shart. Agar yangi service shu ma'lumotni o'zgartirishi (yozishi) kerak bo'lsa, bu pattern yetarli emas: egalik masalasini hal qilib, ma'lumotni ko'chirish yoki yozuv API'sini aniq biznes operatsiyasi sifatida modellashtirish kerak.

## 27.19 Ko'p sxemali saqlash (Multischema Storage)

**Tavsif:** Migratsiya davrida ma'lumotning bir qismi yangi service bazasida, bir qismi esa hali monolit bazasida bo'ladi va yangi service ikki manbadan ham o'qiydi. Bu Split Table va Tracer Write bilan birga yuzaga keladigan o'tkinchi holat: yangi service o'z sxemasida yangi ma'lumotni saqlaydi, qolgan maydonlar uchun esa monolit bazasiga yoki monolit API'siga murojaat qiladi. Maqsad — migratsiyani bir martalik katta operatsiya emas, bosqichli jarayonga aylantirish.

**Spring'da qayerda uchraydi:** Service ichida ikkita `DataSource` + ikkita `EntityManagerFactory` konfiguratsiya qilinadi, yoki o'z sxemasi JPA bilan, legacy sxema esa faqat o'qish uchun `JdbcClient` (Spring Framework 6.1+) / `JdbcTemplate` bilan ishlanadi. `AbstractRoutingDataSource` so'rovni kontekstga qarab marshrutlaydi; polyglot holatda (PostgreSQL + MongoDB + Redis) Spring Data'ning alohida modullari (`spring-data-jpa`, `spring-data-mongodb`) bir ilovada `@EnableJpaRepositories(basePackages=...)` va `@EnableMongoRepositories(basePackages=...)` bilan paket bo'yicha ajratiladi. Birlashgan natija service qatlamidagi aggregator (facade) sinfida yig'iladi.

**Qo'llanish keyslari:**
- Yangi Customer Service profil ma'lumotini o'z bazasida, kredit tarixini esa hali monolit sxemasida saqlashi.
- Issiq (hot) ma'lumotni yangi PostgreSQL'da, arxiv ma'lumotni legacy Oracle'da qoldirish.
- Polyglot persistence: tranzaksion ma'lumot RDBMS'da, qidiruv indeksi Elasticsearch'da, session Redis'da.
- Migratsiya oynasi davomida (bir necha hafta) yangi va eski sxema parallel o'qilishi.
- Reglament tufayli ma'lum ma'lumot turi ma'lum bazada qolishi kerak bo'lgan holatlar.

**Ehtiyot bo'ling:** Ikki manbadan o'qish murakkablikni, latency'ni va xato ehtimolini oshiradi — bu holatga aniq tugash muddati (sunset date) qo'ymasa, "vaqtinchalik" arxitektura doimiy texnik qarzga aylanadi. Ikki sxema ustida bitta tranzaksiya kafolati yo'q, shuning uchun yozuvlarni bitta sxemaga cheklashga harakat qiling.

## 27.20 Umumiy statik ma'lumot (Shared Static Data)

**Tavsif:** Davlat kodlari, valyuta ro'yxati, QQS stavkalari kabi kam o'zgaradigan reference data bir necha service'ga kerak bo'ladi. To'rtta asosiy variant mavjud: (1) har bir service'da ma'lumotning nusxasini saqlash, (2) umumiy jadvalni shared database'da qoldirish, (3) ma'lumotni kod/konfiguratsiya sifatida deploy qilish (static reference library), (4) alohida kichik service yaratish. Tanlov ma'lumotning o'zgarish chastotasi va consistency talabiga bog'liq: juda kam o'zgaradigan ma'lumot uchun kod yoki nusxa, tez o'zgaradigan uchun service.

**Spring'da qayerda uchraydi:** Kod sifatida yondashuvda ma'lumot Java `enum`, `record`, yoki `src/main/resources` ichidagi JSON/YAML/CSV faylga joylanib `@ConfigurationProperties` bilan type-safe o'qiladi (`@ConstructorBinding` Spring Boot 3.x'da standart). Markaziy boshqaruv uchun Spring Cloud Config Server yoki Consul/Vault backend, hamda `@RefreshScope` va Spring Cloud Bus bilan runtime refresh ishlatiladi. Service variantida ma'lumot `@Cacheable` (Caffeine/Redis) bilan uzoq TTL'da keshlanadi; `MessageSource` va `ResourceBundle` lokalizatsiyalangan statik matnlar uchun mos keladi.

**Qo'llanish keyslari:**
- ISO davlat va valyuta kodlarini shared library sifatida barcha service'larga qo'shish.
- QQS/soliq stavkalarini Config Server'da saqlab, `@RefreshScope` bilan deploy'siz yangilash.
- Mamlakat bo'yicha yetkazib berish zonalari ro'yxatini har bir service'da keshlangan nusxada saqlash.
- Xatolik kodlari va foydalanuvchiga ko'rinadigan matnlarni `MessageSource` bundle'lari orqali boshqarish.
- Mahsulot kategoriyalari ierarxiyasini kichik Reference Data Service orqali tarqatish.

**Ehtiyot bo'ling:** Shared library yondashuvi barcha service'lar uchun deployment coupling yaratadi — stavka o'zgarsa hamma service'ni qayta deploy qilish kerak bo'ladi, shuning uchun o'zgarish chastotasi oyda bir martadan ko'p bo'lsa konfiguratsiya yoki service variantini tanlang. Umumiy jadvalni shared database'da qoldirish eng oson yo'l, lekin u Shared Database antipatterniga eshik ochadi: faqat read-only va DDL'ga egalik bitta jamoada bo'lgan holda ruxsat bering.

## 27.21 Maxsus reference data sxemasi (Dedicated Reference Data Schema)

**Tavsif:** Reference data hajmi katta (yuz minglab satr) yoki unga tez-tez murojaat qilinadigan JOIN'lar zarur bo'lsa, uni alohida, faqat o'qish uchun mo'ljallangan sxemaga chiqarish mantiqiy bo'ladi. Barcha service'lar bu sxemadan o'qiydi, ammo unga yozish huquqi faqat bitta egaga (owner service yoki data-governance jamoasi) tegishli bo'ladi. Bu Shared Database antipatterni emas: chegara aniq — bitta yozuvchi, ko'p o'quvchi va o'zgarmas, versiyalangan sxema shartnomasi.

**Spring'da qayerda uchraydi:** Bu infratuzilma/baza darajasidagi qaror; Spring tomonida har bir service'da ushbu sxemaga `read-only` baza useri bilan ikkinchi `DataSource` qo'shiladi va o'qish `@Transactional(readOnly = true)` + `JdbcClient`/JPA bilan bajariladi. Sxemaga DDL va DML faqat owner service'ning Flyway/Liquibase migratsiyalari orqali qo'llaniladi, boshqalarda `spring.flyway.enabled=false` qoldiriladi. O'zgarishlar haqida xabar berish uchun owner service Kafka'ga event chiqaradi va iste'molchilar `@CacheEvict` bilan lokal cache'ni tozalaydi; tez o'qish uchun Redis (`spring-boot-starter-data-redis`) yoki Caffeine ishlatiladi.

**Qo'llanish keyslari:**
- Butun mamlakat bo'yicha pochta indekslari va manzil katalogini yagona read-only sxemada saqlash.
- Bank identifikatorlari (BIC/IBAN) va to'lov marshrutlash jadvallarini markaziy sxemada ushlab turish.
- Tibbiy klassifikatorlar (ICD-10) yoki mahsulot klassifikatori kabi yirik, standartlashtirilgan ma'lumotlar bazasi.
- Valyuta kurslari tarixini bitta egalik qiluvchi service yozib, boshqalar hisob-kitob uchun o'qishi.
- Soliq jurisdiktsiyalari jadvalini compliance jamoasi boshqarishi va barcha service'lar o'qishi.

**Ehtiyot bo'ling:** "Faqat o'qish" intizomini texnik vositalar bilan (baza darajasidagi grant, alohida read-only user) majburlang — aks holda vaqt o'tishi bilan kimdir yozishni boshlaydi va bu to'liq shared database'ga aylanadi. Sxema o'zgarishi barcha iste'molchilarga ta'sir qiladi, shuning uchun faqat qo'shimcha (additive) o'zgarish siyosatini va ustun o'chirishdan oldin deprecation davrini qabul qiling.

## 27.22 Migratsiyani bosqichma-bosqich joriy etish va qaytarish (Incremental Rollout & Rollback of a Migration)

**Tavsif:** Migratsiyaning har bir qadami kichik, kuzatiladigan va qaytarib olinadigan bo'lishi kerak: trafikning 1%, keyin 10%, keyin 100% yangi service'ga yo'naltiriladi va har bir bosqichda xatolik darajasi hamda latency taqqoslanadi. Bu Feature Toggle, Canary Release, Parallel Run (eski va yangi kodni bir vaqtda ishlatib natijalarni solishtirish) va Expand–Contract (sxemani avval kengaytirib, keyin qisqartirish) usullarini bir strategiyaga birlashtiradi. Asosiy qoida: har qanday qadam uchun oldindan yozilgan rollback rejasi bo'lishi shart.

**Spring'da qayerda uchraydi:** Marshrutlash Spring Cloud Gateway (`spring-cloud-starter-gateway`) predicate/filter'lari yoki service mesh (Istio `VirtualService` weight) darajasida bajariladi; ilova ichida Togglz/Unleash/FF4j yoki `@ConditionalOnProperty` + `@Primary` bean almashtirish ishlatiladi. Parallel Run uchun eski va yangi implementatsiya bir interfeysga yozilib, farq `Micrometer` counter'i va struktura log'iga yoziladi; kuzatuv uchun Micrometer Tracing (Spring Boot 3.x) + OpenTelemetry va `/actuator/health`, `/actuator/prometheus` endpoint'lari ishlatiladi. Sxema migratsiyalari Flyway'da faqat additive, backward-compatible qadamlar sifatida yoziladi (avval ustun qo'shish, keyingi release'da eski ustunni o'chirish).

```java
@Service
class ShippingFacade {
    @Value("${migration.useNewShippingService:false}") boolean useNew;
    ShippingQuote quote(Order o) {
        return useNew ? newClient.quote(o) : legacy.quote(o);
    }
}
```

**Qo'llanish keyslari:**
- Yangi Payment Service'ga trafikni 1% → 10% → 50% → 100% bosqichlarida o'tkazish.
- Parallel Run: eski va yangi narx hisoblash logikasini bir vaqtda ishlatib, natija farqini kuzatish.
- Expand–Contract bilan ustun nomini uzilishsiz o'zgartirish (yangi ustun qo'shish, dual write, eski ustunni o'chirish).
- Feature flag bilan yangi service'ni faqat ichki xodimlar yoki bitta mijoz segmenti uchun yoqish.
- Xatolik darajasi oshganda flag'ni sekundlar ichida o'chirib, deploy'siz rollback qilish.

**Ehtiyot bo'ling:** Ma'lumot migratsiyasi odatda qaytarib olinmaydi — rollback faqat kod va trafik marshruti uchun ishlaydi, shuning uchun har bir sxema qadami backward-compatible bo'lishi va yangi bazadagi o'zgarishlar eski bazaga qaytarilishi kafolatlanishi kerak. Feature flag'lar tozalanmasa kod bazasi tezda boshqarib bo'lmas holatga keladi: har bir migratsiya flag'iga yaroqlilik muddati va uni o'chirish tiketini biriktiring.

---

[&larr; 26. Dizayn printsiplari: SOLID, GRASP va umumiy qoidalar](26-dizayn-printsiplari-solid-grasp-va-umumiy.md) · [Mundarija](README.md) · [28. Taqsimlangan ma'lumot, replikatsiya va konsistentlik patternlari &rarr;](28-taqsimlangan-malumot-replikatsiya-va.md)
