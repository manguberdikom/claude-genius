<!-- doc: patterns | chapter: 27 | part:  -->

[Barcha hujjatlar](../../README.md) / [Dizayn patternlar](README.md)

> Holat: tekshirilmoqda. Da'volar hali manbaga solishtirilmoqda.

# 27. Monolitdan microservice'ga migratsiya patternlari (Monolith to Microservices Migration Patterns)

<details>
<summary>Bu bobdagi 31 bo'lim</summary>

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
- [27.20 Statik reference data nusxasi, kutubxonasi va servisi (Duplicate Static Reference Data)](#2720-statik-reference-data-nusxasi-kutubxonasi-va-servisi-duplicate-static-reference-data)
- [27.21 Maxsus reference data sxemasi (Dedicated Reference Data Schema)](#2721-maxsus-reference-data-sxemasi-dedicated-reference-data-schema)
- [27.22 Migratsiyani bosqichma-bosqich joriy etish va qaytarish](#2722-migratsiyani-bosqichma-bosqich-joriy-etish-va-qaytarish)
- [27.23 Dekompozitsiya yondashuvini tanlash (Choosing a Decomposition Approach)](#2723-dekompozitsiya-yondashuvini-tanlash-choosing-a-decomposition-approach)
- [27.24 Taktik ayirish (Tactical Forking)](#2724-taktik-ayirish-tactical-forking)
- [27.25 Komponentlarni aniqlash va o'lchash (Identify and Size Components)](#2725-komponentlarni-aniqlash-va-olchash-identify-and-size-components)
- [27.26 Umumiy domen komponentlarini yig'ish (Gather Common Domain Components)](#2726-umumiy-domen-komponentlarini-yigish-gather-common-domain-components)
- [27.27 Komponentlarni tekislash (Flatten Components)](#2727-komponentlarni-tekislash-flatten-components)
- [27.28 Komponent bog'liqliklarini aniqlash (Determine Component Dependencies)](#2728-komponent-bogliqliklarini-aniqlash-determine-component-dependencies)
- [27.29 Komponent domenlarini yaratish (Create Component Domains)](#2729-komponent-domenlarini-yaratish-create-component-domains)
- [27.30 Domen servislarini yaratish (Create Domain Services)](#2730-domen-servislarini-yaratish-create-domain-services)
- [27.31 Amalda qo'llash](#2731-amalda-qollash)

</details>



Monolitdan microservice'ga o'tish - bu "katta portlash" (big bang) qayta yozish emas, balki ishlab turgan tizimni to'xtatmasdan, kichik-kichik qadamlar bilan funksionallikni va ma'lumotlarni ko'chirish jarayoni. Bu kategoriyadagi patternlar (asosan Sam Newman'ning "Monolith to Microservices" ishidan ma'lum) ikki qiyin masalani hal qiladi: chaqiruv oqimini (call flow) monolitdan yangi servisga xavfsiz yo'naltirish va umumiy ma'lumotlar bazasini (shared database) ajratish. Arxitektor uchun bu patternlar muhim, chunki migratsiyaning asosiy xavfi texnik emas - tashkiliy va ma'lumot izchilligi (data consistency) bilan bog'liq: har bir qadam orqaga qaytarilishi (reversible) va alohida release qilinishi kerak. Quyida har bir pattern Spring ekotizimidagi aniq amalga oshirish vositalari bilan beriladi.

## 27.1 Bo'g'uvchi Anjir Ilovasi (Strangler Fig Application)

**Tavsif:** Monolit oldiga proxy qo'yilib, trafik asta-sekin yangi servislarga yo'naltiriladi - monolit "bo'g'ilib", oxirida butunlay o'ladi. Boshida proxy barcha so'rovlarni monolitga uzatadi, keyin har bir ko'chirilgan endpoint uchun marshrut (route) yangi servisga almashtiriladi. Monolitning kodiga tegmasdan, HTTP yoki messaging darajasida ushlab olish (interception) amalga oshiriladi. Eng muhim xususiyati - har bir qadamni bir marshrut o'zgarishi bilan orqaga qaytarish mumkin.

**Spring'da qayerda uchraydi:** Spring Cloud Gateway (reactive `RouteLocator`, `RouteLocatorBuilder` yoki `spring.cloud.gateway.server.webflux.routes` konfiguratsiyasi) va Spring Boot 3.2+ dagi Spring Cloud Gateway Server MVC varianti asosiy vosita; `Path`, `Header`, `Weight` predicate'lari bilan trafikni bo'lish mumkin. Spring Framework 6.x ichida `ProxyExchange` (spring-cloud-gateway-mvc) yoki oddiy `RestClient`/`WebClient` asosidago `@RestController` fasad ham ishlaydi. Infratuzilma darajasida NGINX, Envoy, AWS ALB listener rule'lari shu vazifani bajaradi va Spring ilovasi faqat yangi endpoint'ni taqdim etadi. Progressiv o'tish uchun Spring Cloud Circuit Breaker (Resilience4j) va `Weight` predicate'i bilan canary qilinadi.

**Qo'llanish keyslari:**
- Legacy e-commerce monolitdan `/api/catalog/**` marshrutini yangi Catalog servisiga ko'chirish.
- Mobil BFF uchun eski SOAP monolit ustiga REST fasad qo'yib, endpoint'larni bitta-bitta almashtirish.
- To'lov moduli kabi yuqori yuklamali bo'limni alohida scale qilish uchun birinchi navbatda ajratish.
- Bir nechta mijoz (tenant) uchun yangi servisni faqat bitta tenant trafigida sinovdan o'tkazish.
- Mainframe yoki PHP legacy tizim oldiga Spring Cloud Gateway qo'yib, bosqichma-bosqich Java'ga o'tish.

**Ehtiyot bo'ling:** Agar monolit va yangi servis bir xil bazaga yozsa, strangler faqat illuziya beradi - ma'lumot bog'liqligi saqlanib qoladi, shuning uchun uni ma'lumotlar ajratish patternlari bilan birga qo'llash kerak. Proxy'ga biznes logika (ma'lumot transformatsiyasi, agregatsiya) joylashtirish eng tez-tez uchraydigan xato: gateway yangi "distributed monolith" markaziga aylanib qoladi.

## 27.2 UI Kompozitsiyasi (UI Composition)

**Tavsif:** Migratsiya chegarasi backend'da emas, foydalanuvchi interfeysida o'tkaziladi: ekranning bir qismi monolitdan, boshqa qismi yangi servisdan keladi va ular UI darajasida yig'iladi. Kompozitsiya sahifa bo'yicha (page-based), vidjet bo'yicha (widget/fragment) yoki micro-frontend ko'rinishida bo'ladi. Bu backend ma'lumotlar bazasiga tegmasdan, yangi funksionallikni foydalanuvchiga tez ko'rsatish imkonini beradi. Natijada jamoalar vertikal (UI + servis) tilimlarga egalik qiladi.

**Spring'da qayerda uchraydi:** Server-side kompozitsiya uchun Thymeleaf `th:insert`/`th:replace` fragmentlari va Spring MVC `ViewResolver`'lari, shuningdek Server-Side Includes (SSI) yoki Edge Side Includes (ESI) NGINX/Varnish darajasida ishlatiladi. Spring Boot 3.x da `spring-boot-starter-thymeleaf` bilan monolit layout saqlanib, yangi fragmentlar HTTP orqali `RestClient` bilan olinadi; Spring WebFlux'da `WebClient` va `Flux` bilan fragmentlar parallel yuklanadi. Micro-frontend yondashuvida kompozitsiya brauzerda (Webpack Module Federation, web components) bo'ladi va Spring tomoni faqat JSON/HTML fragment beradi - buni aniq ayting: pattern Spring'ning o'zida emas, UI qatlamida yashaydi. Spring Cloud Gateway marshrut bo'yicha statik SPA va yangi API'ni bitta origin ostida birlashtiradi (CORS muammosini yo'qotish uchun).

**Qo'llanish keyslari:**
- "Mening buyurtmalarim" sahifasidagi yetkazib berish holati vidjetini yangi Delivery servisidan olish.
- Legacy JSP admin panelida faqat "Hisobotlar" bo'limini yangi Angular/React SPA bilan almashtirish.
- Mobil ilovada bitta tab'ni yangi servis API'siga ulab, qolganini monolitda qoldirish.
- Marketing banner/tavsiya blokini alohida Recommendation servisidan render qilish.
- Bir nechta jamoa bitta portal'ni mustaqil deploy qilishi kerak bo'lganda.

**Ehtiyot bo'ling:** Vizual izchillik (dizayn tizimi, CSS, autentifikatsiya sessiyasi) buziladi - umumiy design system va SSO'ni oldin hal qilmasa, foydalanuvchi "chok"larni ko'radi. Ko'p fragmentni sinxron yuklash sahifa latency'sini oshiradi, shuning uchun timeout va fallback (bo'sh vidjet) majburiy.

## 27.3 Abstraksiya Orqali Tarmoqlanish (Branch by Abstraction)

**Tavsif:** Monolit ichidagi mavjud implementatsiya ustiga abstraksiya (interface) kiritiladi, so'ng shu interface'ning ikkinchi - yangi servisga chaqiruv qiladigan - implementatsiyasi yoziladi. Ikkala implementatsiya bir vaqtda kodda yashaydi va qaysi biri ishlashi feature flag bilan boshqariladi. Bu uzoq muddatli feature branch'larsiz, trunk'da ishlash imkonini beradi. Ishonch hosil bo'lgach, eski implementatsiya va flag o'chiriladi.

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

**Ehtiyot bo'ling:** Flag'larni o'z vaqtida tozalamaslik "flag debt"ga olib keladi - har bir flag kod yo'llarini eksponensial ko'paytiradi va test matritsasini buzadi. Abstraksiyani juda kech, kod allaqachon chalkash bo'lganda kiritish patternning ma'nosini yo'qotadi: avval ichki chegarani (seam) toza qilib ajratish kerak.

## 27.4 Parallel Ishga Tushirish (Parallel Run)

**Tavsif:** Eski va yangi implementatsiya bir vaqtda, bir xil kirish ma'lumotlari bilan chaqiriladi, lekin faqat bittasining natijasi foydalanuvchiga qaytariladi; natijalar esa solishtirilib, farqlar qayd etiladi. Bu yangi servisning funksional to'g'riligini va ishlash tezligini real trafikda, xavfsiz tekshirish usuli. Solishtirish faqat funksional tenglikni emas, javob vaqti va xatolik darajasi kabi nofunksional jihatlarni ham qamrashi kerak, chunki tarmoq chegarasidan o'tgan chaqiruv timeout va yo'qolgan so'rov keltiradi; verifikatsiyani so'rov doirasida emas, yon tarafda (masalan kunlik solishtirish hisoboti bilan) bajarish mumkin. Yetarli ishonch to'plangach, natija manbasi almashtiriladi. Buni canary release bilan aralashtirmang: canary'da foydalanuvchilarning bir qismi yangi yo'ldan o'tadi, parallel run'da esa har bir so'rov uchun ikkala implementatsiya ham chaqiriladi.

**Spring'da qayerda uchraydi:** Eski chaqiruv sinxron, yangisi `@Async` + `TaskExecutor` (Spring Boot 3.2+ da virtual thread'lar: `spring.threads.virtual.enabled=true`, Java 21+) bilan fon rejimida bajariladi; farqlar Micrometer `Counter`/`Timer` metrikalariga va strukturaviy log'ga yoziladi. `ApplicationEventPublisher` + `@TransactionalEventListener(phase = AFTER_COMMIT)` bilan solishtirishni asosiy tranzaksiyadan ajratish mumkin. Spring Cloud Gateway'da `Weight` predicate yoki maxsus `GlobalFilter` bilan "shadow traffic" nusxalash amalga oshiriladi; infratuzilma darajasida Envoy'ning request mirroring (`request_mirror_policies`) imkoniyati shu vazifani bajaradi. Natijalarni Spring Boot Actuator `/actuator/metrics` va Grafana dashboard orqali kuzatiladi.

**Qo'llanish keyslari:**
- Sug'urta mukofoti (premium) hisoblash algoritmini yangi servisda tekshirish - pul bilan bog'liq, xato qimmat.
- Soliq yoki chegirma hisoblash logikasini ko'chirishda tiyin darajasidagi farqlarni aniqlash.
- Kredit skoring modelini yangi servisga o'tkazishda eski qaror bilan moslikni o'lchash.
- Yangi Search servisining relevantligini eski natijalar bilan solishtirish.
- Ish haqi (payroll) hisob-kitobini yangi tizimda bir-ikki oy "quruq" rejimda yuritish.

**Ehtiyot bo'ling:** Nojo'ya ta'sirlar (side effects) ikki marta sodir bo'lishi mumkin: mijozga email ikki marta ketmasligi uchun past darajadagi amalni Spy bilan almashtirish mumkin - Spy chaqiruv bo'lganini qayd etadi, lekin amalni bajarmaydi. Spy'ni monolit ichida qo'yish vasvasasiga tushmang: shunda yangi servisga tarmoq chaqiruvi umuman ketmaydi va timeout, nosozlik va latency ta'siri ko'rinmay qoladi. Qoida teskari tarafga ham ishlaydi: Spy qancha ko'p funksionallikni almashtirsa, shuncha kam narsa haqiqatda tekshiriladi. Implementatsiya hech qachon arzon emas, shuning uchun bu pattern faqat yuqori riskli logikaga qo'llanadi va muddati oldindan belgilanadi.

## 27.5 Bezovchi Hamkor (Decorating Collaborator)

**Tavsif:** Monolitning kodini o'zgartirish imkoni bo'lmaganda, uning chaqiruvlari proxy orqali kuzatiladi va so'rov/javob asosida yangi servisda qo'shimcha xatti-harakat ishga tushiriladi. Proxy monolitning javobini o'zgartirmaydi - faqat "bezaydi": hodisa (event) chiqaradi yoki yangi servisga chaqiruv qiladi. Shu tariqa yangi funksionallik monolitga tegmasdan qo'shiladi. Strangler Fig'dan farqi aniq: chaqiruv to'silmaydi, monolitga odatdagidek yetib boradi va proxy faqat natijaga qarab ish qiladi. Ya'ni bu strangler'ning varianti emas, klassik Decorator g'oyasining migratsiyadagi qo'llanishi.

**Spring'da qayerda uchraydi:** Spring Cloud Gateway'da `GlobalFilter`/`GatewayFilterFactory` (yoki MVC variantida `HandlerFilterFunction`) javobni o'qib, Kafka'ga event yuboradi (`KafkaTemplate`, Spring for Apache Kafka 3.x). Monolit Spring ilovasi bo'lsa, `OncePerRequestFilter`, `HandlerInterceptor` yoki Spring AOP (`@Around` advice, `ProxyFactoryBean`) bilan bir xil natijaga erishiladi. Spring Integration'ning `WireTap` va `@ServiceActivator` komponentlari xabar oqimini nusxalab, yon kanalga uzatish uchun mo'ljallangan. Agar monolit umuman Java bo'lmasa, pattern infratuzilma (Envoy/NGINX `lua`, API Gateway) darajasida yashaydi va Spring servisi faqat iste'molchi (consumer) bo'ladi.

**Qo'llanish keyslari:**
- Buyurtma muvaffaqiyatli yaratilganda monolitga tegmasdan Loyalty servisida bonus ball berish.
- Ro'yxatdan o'tish javobini ushlab, yangi Notification servisi orqali "welcome" email yuborish (ruxsat berilgan hollarda).
- Legacy tizim javoblaridan analytics event'lar yaratib, yangi ma'lumot platformasiga uzatish.
- Mijoz profilini o'zgartirish chaqiruvidan keyin yangi CRM servisini sinxronlashtirish.
- Audit log'ni markaziy compliance servisiga yig'ish, monolit release'ini kutmasdan.

**Ehtiyot bo'ling:** Proxy'ga qancha ko'p "aql" qo'shilsa, u o'zi ham servisga aylanib boradi va strangler'dagi oddiy proxy'ning afzalligi yo'qoladi. Asosiy chegara esa ma'lumotda: pattern faqat kerakli ma'lumot kirish so'rovidan yoki monolit javobidan olinsa yaxshi ishlaydi. Ma'lumot yetmasa, proxy monolitga qayta murojaat qilishga majbur bo'ladi, bu qo'shimcha yuklama va aylanma bog'liqlik keltiradi; shunda monolitni o'zgartirib kerakli ma'lumotni javobga qo'shish yoki Change Data Capture kabi ko'proq aralashuvchi usul qoladi. Shuni aniq ayting: oddiy holatda bu pattern Change Data Capture'dan ko'ra nafisroq va kamroq bog'lanish beradi, ya'ni CDC ga o'tish ishonchlilikni oshirish uchun emas, boshqa chora qolmaganda qilinadi. Yon kanaldagi xatolar asosiy oqimni buzmasligi uchun chaqiruv asinxron va idempotent bo'lishi shart.

## 27.6 Ma'lumot O'zgarishini Ushlash (Change Data Capture)

**Tavsif:** Monolitning kodiga ham, chaqiruvlariga ham tegmasdan, uning ma'lumotlar bazasidagi o'zgarishlar (transaction log) o'qilib, yangi servislarga event sifatida uzatiladi. Uning o'rni aniq: ma'lumot o'zgarishiga munosabat bildirish kerak, lekin chaqiruvni tizim chegarasida strangler yoki decorator bilan ushlab olish imkoni yo'q va monolit kodini o'zgartirish ham mumkin emas. Amalga oshirishning uch yo'li sanaladi: baza trigger'lari, transaction log'ni o'qiydigan vositalar va davriy ishlaydigan batch delta copier. Trigger'lardan juda tejamkor foydalanish kerak, chunki ular ko'paygan sari tizim qanday ishlashini tushunish qiyinlashadi; transaction log varianti esa eng toza yechim, chunki vosita bazadan tashqarida, hatto log nusxasi ustida ishlaydi. CDC event'lari yangi servisning o'z ma'lumot nusxasini (read model) to'ldiradi yoki biznes jarayonini ishga tushiradi. Migratsiya nuqtai nazaridan bu monolitdan yangi dunyoga bir tomonlama ma'lumot "ko'prigi".

**Spring'da qayerda uchraydi:** Asosiy vosita - Debezium (PostgreSQL logical decoding, MySQL binlog, Oracle LogMiner) Kafka Connect orqali; Spring tomoni Spring for Apache Kafka 3.x `@KafkaListener` yoki Spring Cloud Stream Kafka binder bilan event'larni iste'mol qiladi. Debezium Engine'ni to'g'ridan-to'g'ri Spring Boot 3.x ilovasi ichida embedded rejimda ishga tushirish ham mumkin (`io.debezium:debezium-embedded`, `@Bean` sifatida `DebeziumEngine`). Buni aniq ayting: CDC Spring Framework'ning qismi emas - u ma'lumotlar bazasi va infratuzilma darajasidagi mexanizm, Spring ilovasi faqat consumer yoki engine host bo'ladi. Idempotentlik uchun qabul qilingan event'lar `@Transactional` ichida `processed_events` jadvaliga yoziladi.

**Qo'llanish keyslari:**
- Legacy monolit bazasidan Customer ma'lumotlarini yangi CRM servisiga real vaqtda ko'chirish.
- Ko'chirish davrida yangi servis bazasini monolit bilan sinxron saqlash (dual-write'dan qochish).
- Monolit jadvallaridan analytics/data lake'ga oqim (streaming ETL) qurish.
- Qidiruv indeksini (Elasticsearch) monolit bazasidagi o'zgarishlar bilan yangilash.
- Yangi servisga o'tishdan oldin tarixiy ma'lumotlarni snapshot + incremental tarzda yuklash.

**Ehtiyot bo'ling:** Ushlab oluvchi tizim monolitning datastore'iga bog'lanishi shart - bu patternning qochib bo'lmaydigan narxi: monolit DBA'si ustun nomini o'zgartirsa, servis sinadi. Shuning uchun Newman CDC qo'llanishini minimumda ushlashni maslahat beradi: trigger variantining o'z kamchiliklari bor, transaction log asosidagi to'laqonli vositalar esa yechimga sezilarli murakkablik qo'shadi. Shu korpusning amaliy tavsiyasi: uni vaqtinchalik ko'prik deb qarash va oxir-oqibat aniq event shartnomasiga (transactional outbox) o'tish. Event tartibi, schema evolution va "replay" paytidagi dublikatlar uchun idempotent consumer majburiy.

## 27.7 Ma'lumotlar Bazasi Ko'rinishi (Database View)

**Tavsif:** Monolit bazasining to'g'ridan-to'g'ri jadvallarini ochish o'rniga, iste'molchiga faqat kerakli ustunlarni ko'rsatuvchi read-only view beriladi. View bu yerda "ma'lumot shartnomasi" (contract) rolini bajaradi: ichki sxema o'zgarsa, view saqlanib qoladi va iste'molchi buzilmaydi. Bu to'liq servis ajratishga vaqt yo'q bo'lganda, integration database'ni qisman tartibga solish usuli. Cheklovi - view read-only va bitta ma'lumotlar bazasi ichida ishlaydi.

**Spring'da qayerda uchraydi:** Flyway yoki Liquibase migratsiyasi bilan `CREATE VIEW` (yoki materialized view) yaratiladi; Spring Data JPA tomonida `@Entity @Immutable` (Hibernate 6.x) yoki `@Subselect`, yaxshisi - Spring Data JDBC/`JdbcClient` (Spring Framework 6.1+) yoki projection interface bilan o'qiladi. Faqat o'qish uchun `@Transactional(readOnly = true)` va alohida `DataSource` (read-only user, cheklangan `GRANT SELECT`) sozlanadi; `spring.jpa.hibernate.ddl-auto=none` bo'lishi shart. Pattern asosan ma'lumotlar bazasi darajasida yashaydi - Spring faqat uni iste'mol qiladi va migratsiya skriptlari orqali boshqaradi.

**Qo'llanish keyslari:**
- Hisobot servisiga monolitning 40 ustunli `customers` jadvalidan faqat 6 ustunni ochish.
- Yangi servis vaqtincha monolit ma'lumotini o'qishi kerak bo'lganda, jadval nomlariga bog'lanmaslik uchun.
- Monolit jadvalini refaktoring qilishda (ustun nomini o'zgartirish) eski nomni view orqali saqlab qolish.
- Maxfiy maydonlarni (passport, karta raqami) berkitib, qolgan ma'lumotni hamkor servisga ko'rsatish.
- Bir nechta jadvalni denormalizatsiya qilib, read model sifatida materialized view berish.

**Ehtiyot bo'ling:** View yozishni qo'llab-quvvatlamaydi va iste'molchilar bir xil bazaga bog'lanib qolgani uchun mustaqil deploy, mustaqil scale va texnologiya tanlash erkinligi yo'q - bu faqat o'tish davri uchun vaqtinchalik yechim. Murakkab yoki materialized view'lar monolit bazasiga qo'shimcha yuklama beradi va yangilanish kechikishini (staleness) keltirib chiqaradi.

## 27.8 Ma'lumotlar Bazasini O'rovchi Servis (Database Wrapping Service)

**Tavsif:** Umumiy bazaga ko'p iste'molchi to'g'ridan-to'g'ri ulangan bo'lsa, ularning oldiga shu ma'lumot ustida yagona egalik qiladigan yupqa servis qo'yiladi va barcha murojaatlar faqat uning API'si orqali o'tadi. Bu "ma'lumot bazasi - integratsiya nuqtasi" muammosini servis chegarasiga aylantiradi, lekin jadvallarni hali ko'chirmaydi. Servis boshida monolit sxemasining ustiga yupqa CRUD qatlam bo'lishi mumkin, keyin ichida o'z modelini rivojlantiradi. Asosiy foyda - sxemani o'zgartirish erkinligini qaytarib olish.

**Spring'da qayerda uchraydi:** Yupqa Spring Boot 3.x servisi: `@RestController` + Spring Data JPA/JDBC repository'lar, `spring-boot-starter-validation` bilan kirish tekshiruvi va OpenAPI shartnomasi (springdoc-openapi 2.x). Iste'molchilar tomonida `@HttpExchange` interface client yoki `RestClient` ishlatiladi, shartnoma esa Spring Cloud Contract bilan verifikatsiya qilinadi. Baza darajasida eski iste'molchilarning to'g'ridan-to'g'ri ulanishini `REVOKE` bilan to'sish va faqat wrapper servisga `GRANT` berish kerak - bu qism Spring'da emas, DBA darajasida bajariladi. Kesh va yuklamani kamaytirish uchun `@Cacheable` (Spring Cache abstraction, Caffeine/Redis) qo'llanadi.

**Qo'llanish keyslari:**
- 7 ta ilova to'g'ridan-to'g'ri o'qiyotgan `product_catalog` jadvalini bitta Catalog servisi ortiga yashirish.
- Ko'p jamoa yozadigan "umumiy" `users` jadvalini yagona Identity servisiga topshirish.
- Batch/ETL job'larni bazadan uzib, servis API'siga o'tkazish.
- Monolit sxemasini refaktoring qilishdan oldin iste'molchilarni izolyatsiya qilish.
- Ma'lumotga kirishni markazlashtirib, audit va rate limiting qo'shish.

**Ehtiyot bo'ling:** Wrapper servis jadval strukturasini 1:1 ko'rsatsa, u "anemik CRUD proxy"ga aylanadi va hech qanday coupling kamaymaydi - API biznes operatsiyalari (`reserveStock`) tilida bo'lishi kerak, jadval tilida emas. Shuningdek u yangi yagona nosozlik nuqtasi (single point of failure) va qo'shimcha latency keltiradi, shuning uchun kesh, timeout va circuit breaker oldindan rejalashtiriladi.

## 27.9 Ma'lumotlar Bazasi Servis Interfeysi (Database-as-a-Service Interface)

**Tavsif:** Ba'zi iste'molchilarga (hisobot tizimlari, BI, analitika) baribir SQL kerak bo'ladi - ularga ichki baza emas, maxsus ko'chiriladigan, faqat o'qish uchun mo'ljallangan alohida "reporting database" beriladi. Servis o'z ichki bazasidan bu tashqi bazaga mapping engine orqali ma'lumot ko'chiradi va tashqi sxema aniq shartnoma bo'lib qoladi. Shu tariqa ichki model erkin o'zgaradi, tashqi sxema esa stabil qoladi. Bu CQRS'ning read model g'oyasini "SQL endpoint" shaklida beradi.

**Spring'da qayerda uchraydi:** Spring Boot 3.x da ikki `DataSource` (`@Primary` ichki, ikkinchisi `@Qualifier("reportingDataSource")`) va mapping engine sifatida `@Scheduled` job, Spring Batch 5.x step'lari yoki Debezium/Kafka Connect sink. Ikkala sxema Flyway/Liquibase bilan alohida boshqariladi (`spring.flyway.locations` bir nechta); yozish `JdbcClient`/`NamedParameterJdbcTemplate` yoki Spring Batch `JdbcBatchItemWriter` bilan bajariladi. Event asosida yangilash uchun `@TransactionalEventListener` + `@KafkaListener` birgalikda ishlatiladi. Tashqi baza va unga kirish huquqlari infratuzilma darajasida (alohida instance, read-only role, resurs kvotasi) ta'minlanadi - Spring buni faqat to'ldiradi.

**Qo'llanish keyslari:**
- Moliyaviy hisobot jamoasiga Orders servisining stabil, denormalizatsiyalangan read sxemasini berish.
- BI vositalari (Tableau, Power BI, Metabase) uchun SQL endpoint taqdim etish.
- Data warehouse'ga ETL uchun manba sifatida xizmat qilish, ichki sxemani ochmasdan.
- Og'ir analitik so'rovlarni asosiy OLTP bazadan ajratib, performance'ni himoyalash.
- Monolitdan ajratilgan servisdan keyin eski hisobot so'rovlarini ishlashda davom ettirish.

**Ehtiyot bo'ling:** Tashqi sxema ham xuddi API kabi versiyalanishi va buzilmaydigan (backward-compatible) o'zgartirilishi kerak - "shunchaki baza" deb qarash uni boshqarilmaydigan integration database'ga qaytaradi. Yangilanish kechikishi (eventual consistency) iste'molchiga aniq hujjatlashtirilmasa, hisobotlardagi nomuvofiqlik ishonchni yo'qotadi.

## 27.10 Agregatni Ochuvchi Monolit (Aggregate Exposing Monolith)

**Tavsif:** Yangi servisga monolitdagi ma'lumot kerak bo'lganda, u bazaga tegmasdan monolitning o'zi taqdim etgan API orqali agregat (DDD ma'nosidagi Aggregate - masalan Customer, Order) oladi. Monolit shu ma'lumot ustida egalik qilishda davom etadi, lekin endi uni aniq shartnoma bilan chiqaradi. Bu Database View'dan kuchliroq: monolit biznes qoidalari va invariantlarini saqlab qoladi, iste'molchi esa sxemaga bog'lanmaydi. Ko'pincha monolitni "haqiqiy servis"ga aylantirishning birinchi qadami.

**Spring'da qayerda uchraydi:** Monolit Spring ilovasi bo'lsa - yangi `@RestController` yoki `@RepositoryRestResource` (Spring Data REST) endpoint, DTO'lar `record` (Java 17+) sifatida, shartnoma springdoc-openapi 2.x bilan hujjatlashtiriladi; o'zgarishlar haqida xabar berish uchun qo'shimcha ravishda Kafka'ga event (`KafkaTemplate`) chiqariladi. Iste'molchi tomonida `RestClient`, `@HttpExchange` interface client yoki `WebClient` va Resilience4j `@CircuitBreaker`/`@Retry` ishlatiladi. Monolit ichida modul chegarasini saqlash uchun Spring Modulith 1.x (`@ApplicationModule`, `ApplicationModuleTest`, `@DomainEvent`) juda mos keladi - bu ko'pincha ajratishdan oldingi "ichki chegara" bosqichi. Shartnoma regressiyasini Spring Cloud Contract yoki Pact bilan tekshiriladi.

**Qo'llanish keyslari:**
- Yangi Loyalty servisi mijoz ma'lumotini monolitning `/api/customers/{id}` endpoint'idan olishi.
- Hisob-faktura servisi buyurtma agregatini monolitdan o'qib, o'z hujjatini yaratishi.
- Yangi mobil BFF monolitdagi mahsulot agregatiga API orqali murojaat qilishi.
- Monolitni Spring Modulith bilan modullarga bo'lib, kelajakdagi servis chegaralarini sinab ko'rish.
- Bir nechta yangi servis uchun monolitni "ma'lumot manbasi" sifatida rasmiylashtirish.

**Ehtiyot bo'ling:** Monolit sinxron chaqiruvlar manbasi bo'lib qolsa, yangi servislar uning mavjudligiga bog'liq bo'ladi - bu "distributed monolith"ning klassik ko'rinishi; shuning uchun kesh, timeout, circuit breaker va imkon bo'lsa event asosidagi replikatsiya zarur. Agregat chegarasini noto'g'ri tanlash (butun jadvalni "agregat" deb ko'rsatish) API'ni jadval proyeksiyasiga aylantiradi va keyinchalik ajratishni qiyinlashtiradi.

## 27.11 Ma'lumot Egaligini O'zgartirish (Change Data Ownership)

**Tavsif:** Funksionallik yangi servisga ko'chgandan keyin, ma'lumotning egaligi ham ko'chadi: jadvallar yangi servis bazasiga o'tadi va monolit endi ularga faqat servis API'si orqali murojaat qiladi. Bu migratsiyaning eng murakkab, lekin eng muhim qadami - ungacha ajratish faqat yarim bajarilgan hisoblanadi. Monolit endi yangi servisni haqiqat manbasi deb biladi va ma'lumotni o'qish yoki o'zgartirish uchun uning endpoint'iga murojaat qiladi. Agar monolitga faqat o'qish kerak bo'lsa, yangi servis bazasidan monolitga view proyeksiya qilish ham mumkin, lekin view'ning barcha cheklovlari saqlanadi va kitob monolitni o'zgartirib to'g'ridan-to'g'ri chaqiruvga o'tishni afzal ko'radi. Natijada foreign key va bitta ACID tranzaksiya o'rniga saga, event va eventual consistency keladi.

**Spring'da qayerda uchraydi:** Ko'chish davrida yozuvni bitta egada saqlab, ikkinchi nusxani replikatsiya bilan to'ldirish uchun Transactional Outbox + Debezium yoki Spring Modulith 1.x `@Externalized` event publication registry ishlatiladi; monolitdagi `@OneToMany` JPA assotsiatsiyalari oddiy ID maydoni va `RestClient` chaqiruviga aylantiriladi. Sxema o'zgarishi Flyway/Liquibase migratsiyalari bilan expand-contract uslubida bosqichma-bosqich bajariladi; birlashtirilgan (join) so'rovlar o'rniga API kompozitsiyasi yoki CQRS read model quriladi. Taqsimlangan jarayon izchilligi uchun saga orkestratsiyasi (Spring Statemachine, Camunda, Temporal Java SDK yoki qo'lda yozilgan `@KafkaListener` state machine) va idempotentlik jadvali kerak bo'ladi. Ma'lumotni ko'chirishning o'zi Spring Batch 5.x job'lari yoki CDC bilan amalga oshiriladi.

**Qo'llanish keyslari:**
- `orders` va `order_items` jadvallarini monolitdan Order servisining o'z bazasiga ko'chirish.
- Monolitdagi `invoices` ustidagi yozish huquqini Billing servisiga topshirib, monolitni read-only qilish.
- Monolit bilan servis o'rtasidagi foreign key'ni olib tashlab, ID + API chaqiruviga o'tish.
- Umumiy `users` jadvalini Identity servisiga ko'chirib, parol va sessiya egaligini bir joyga olish.
- Ikki fazali ko'chish: avval write, keyin read trafikini almashtirib, eski jadvalni arxivlash.

**Ehtiyot bo'ling:** Xavf ikki joyga yozishning o'zida emas, yozuvchilar sonida. Ikki sxemani ilova kodi orqali sinxron ushlash kitobda anti-pattern emas, balki bosqichli migratsiya usuli sifatida beriladi (27.12) - ammo u faqat har bir vaqt momentida yozuvni bitta tomon, yo monolit, yo servis bajarganda ishonchli. Monolit ham, servis ham bir vaqtda ikkala sxemaga yozsa, ikkisi ham sinxronlikni to'g'ri ta'minlashi shart bo'ladi va biri xato qilsa ma'lumot jim-jitlik bilan ajralib ketadi. Shuning uchun egalikni ko'chirishda avval yozuvni bitta joyga yig'ing, keyin ikkinchi nusxani replikatsiya (hodisa yoki CDC) bilan to'ldiring. Foreign key va `JOIN`larni yo'qotish hisobotlarni, validatsiyani va "hammasi yoki hech narsa" kafolatini buzadi - buni oldindan saga, compensating transaction va monitoring bilan rejalashtirmasa, migratsiya ishlab chiqarishda (production) ma'lumot nomuvofiqligi bilan tugaydi.

## 27.12 Ma'lumotlarni ilova darajasida sinxronlashtirish (Synchronize Data in Application)

**Tavsif:** Monolit va yangi microservice bir vaqtning o'zida bir xil ma'lumotga muhtoj bo'lganda, sinxronlashtirish mas'uliyati baza replikatsiyasiga emas, ilova kodining o'ziga yuklanadi - pattern nomidagi "in Application" shuni bildiradi. Kitobda u uch qadamga bo'linadi. (1) Bulk sinxronizatsiya: yangi bazaga bir martalik batch migratsiya qilinadi; eski tizim ishlab turgani uchun manba snapshot bo'ladi, shuning uchun import tugagach snapshot'dan keyingi o'zgarishlarni yetkazish uchun Change Data Capture ishga tushiriladi. (2) Yozuv ikkala bazaga, o'qish eski sxemadan: maqsad - ilova ikkala manbaga to'g'ri yozayotganini va yangi baza qabul qilinadigan chegarada ishlayotganini tasdiqlash; yangi baza yiqilsa ham ma'lumot eski bazadan olinadi. (3) Yozuv ikkala bazaga, o'qish yangi sxemadan: endi yangi baza haqiqat manbasi, lekin yozuv eski bazaga davom etgani uchun orqaga qaytish yo'li ochiq qoladi. Eski sxema faqat yangi tizimga ishonch to'liq hosil bo'lgach olib tashlanadi.

**Spring'da qayerda uchraydi:** Service qatlamida ikkita alohida `DataSource` va ikkita `JdbcTemplate`/`EntityManager` bean'i e'lon qilinadi (`@Primary` va `@Qualifier` bilan ajratiladi), `ChainedTransactionManager` o'rniga odatda birinchi bazaga `@Transactional` yozuv, ikkinchisiga `TransactionSynchronization` yoki `@TransactionalEventListener(phase = AFTER_COMMIT)` orqali yozuv bajariladi. Bulk backfill uchun Spring Batch (`JdbcPagingItemReader` + `JdbcBatchItemWriter`, chunk-oriented step, `JobRepository` orqali restart) juda mos keladi. O'qish/yozish marshrutini boshqarish uchun `AbstractRoutingDataSource` yoki feature flag kutubxonasi (Togglz, FF4j, Unleash) ishlatiladi; kod darajasidagi dual write'ga alternativa sifatida Debezium (CDC) infratuzilma darajasida qo'llanadi.

**Qo'llanish keyslari:**
- Monolit `orders` jadvalidan yangi Order Service'ning alohida PostgreSQL bazasiga uzilishsiz ko'chish.
- Legacy Oracle bazasidan PostgreSQL'ga bosqichma-bosqich migratsiya, ikki baza bir necha hafta parallel yashaydi.
- Yangi service'ni "shadow mode"da ishga tushirib, uning ma'lumotlari monolitdagi bilan mos kelishini tekshirish.
- On-premise bazadan cloud-managed bazaga (RDS/Cloud SQL) ko'chirishda ilova ishlab turgan holda sinxronlik ushlab turish.
- Yangi, boshqacha modellashtirilgan sxemaga (masalan, normalizatsiyadan denormalizatsiyaga) o'tishda ikki model parallel to'ldirilishi.

**Ehtiyot bo'ling:** Ikki joyga yozish atomik emas - ikkinchi yozuv muvaffaqiyatsiz bo'lsa bazalar ajralib ketadi, shuning uchun doimiy reconciliation job va drift metrikasi majburiy. Kitob patternning chegarasini aniq belgilaydi: u bitta ilova ikki sxemani sinxron ushlaganda (masalan kodni bo'lishdan oldin sxemani bo'lishda) yaxshi ishlaydi va aynan shu holatda tez almashtirish va rollback uchun katta foyda beradi. Monolit ham, microservice ham bir vaqtda ikkala sxemani sinxron ushlashi kerak bo'lsa, murakkablik keskin oshadi va biri xato qilsa muammo boshlanadi. Murakkablik faqat bitta shart bilan kamayadi: har bir vaqt momentida yozuvni yo monolit, yo servis bajaradi, ya'ni oddiy switchover. So'rov ikkalasiga ham tushishi mumkin bo'lsa (masalan canary), bu patterndan voz kechish kerak.

## 27.13 Tracer Write (Tracer Write)

**Tavsif:** Kitobda bu Synchronize Data in Application patternining varianti deb beriladi: ma'lumotning yangi service'dagi nusxasi "source of truth" sifatida bosqichma-bosqich, atribut-atribut yoki use-case-use-case tan olinadi va migratsiya davomida ikki haqiqat manbasining birga yashashiga chidaladi. Boshida yangi service faqat kichik bir qism maydonlar uchun haqiqat manbasi bo'ladi, qolganlari monolitda qoladi; vaqt o'tishi bilan "chiziq" (tracer) siljib boradi va nihoyat butun ma'lumot yangi service'ga o'tadi. Bu Big Bang migratsiyasini juda kichik, qaytarib olinadigan qadamlarga bo'lib tashlaydi.

**Spring'da qayerda uchraydi:** Monolitdagi domain sinfining getter'lari ichiga yoki repository fasad'iga qaror nuqtasi qo'yiladi: ma'lum maydon uchun yangi service'ga `RestClient`/`WebClient` (Spring Framework 6.1+ `RestClient`, Spring Boot 3.2+) yoki `@HttpExchange` interface client orqali so'rov yuboriladi, qolgani lokal JPA entity'dan o'qiladi. Migratsiya chizig'i feature flag (Togglz/Unleash) yoki `@ConfigurationProperties` orqali boshqariladi; har bir qadam uchun `Micrometer` counter'lari ("read-from-new", "read-from-old") qo'yilib Grafana'da kuzatiladi. Sinxronlik Debezium Kafka Connect yoki `@TransactionalEventListener` + `ApplicationEventPublisher` orqali ikki tomonlama saqlanadi.

**Qo'llanish keyslari:**
- Customer ma'lumotining avval faqat `marketingPreferences` qismini yangi Customer Service'ga o'tkazish, keyin `address`, keyin butun profil.
- Yirik `product` jadvalini Catalog Service'ga use-case bo'yicha ko'chirish: avval "product search", keyin "pricing", keyin "inventory".
- Yuz millionlab satrli jadvalni bir kecha ichida ko'chirish imkoni yo'q bo'lgan paytda migratsiyani oylarga cho'zish.
- Riskli core domain (masalan, billing) migratsiyasini har bir qadamda rollback qilish mumkin bo'lgan holda bajarish.
- Yangi service'ning ishlash sifatini real trafikda, kichik maydon ustida sinovdan o'tkazish.

**Ehtiyot bo'ling:** Kitob sinxronizatsiyaning uch variantini sanaydi: bitta manbaga yozib ikkinchisini fon jarayoni bilan to'ldirish, mijozning o'zi ikkala manbaga yozishi, yoki xohlagan manbaga yozish. Dastlabki ikkisi ishlaydi, uchinchisidan esa qochish kerak, chunki u ikki tomonlama sinxronizatsiya talab qiladi va bunga erishish juda qiyin. Qanday variant tanlansa ham, nomuvofiqlik oynasi qoladi, shuning uchun sinxronizatsiya haqiqatan ishlayotganini tekshiradigan reconciliation jarayoni majburiy - hatto u har bir bazaga qaratilgan bir juft SQL so'rov bo'lsa ham. Yangi manbani bir muddat iste'molchisiz ishlatib ko'rish ham oqilona qadam. "Tracer" holatida uzoq qolish eng katta xavf: vaqtinchalik murakkablik doimiyga aylanmasligi uchun har bir qadamga deadline va "eski kodni o'chirish" tiketi biriktirilsin.

## 27.14 Jadvalni bo'lish (Split Table)

**Tavsif:** Bitta jadval ikki yoki undan ko'p bounded context'ga tegishli ustunlarni saqlayotgan bo'lsa, jadval vertikal ravishda bo'linadi va har bir bo'lagi o'z service'i bazasiga ko'chiriladi. Masalan `item` jadvalidagi `sku`, `name` Catalog'ga, `stock_count` Warehouse'ga ketadi. Agar bo'linadigan ustunlar bitta tranzaksiyada o'zgarsa, bo'lishdan oldin ushbu tranzaksiya saga yoki eventual consistency bilan almashtirilishi kerak - shuning uchun bu pattern ko'pincha Saga patterniga olib keladi.

**Spring'da qayerda uchraydi:** Bu avvalo sxema darajasidagi o'zgarish: Flyway (`spring.flyway`) yoki Liquibase migratsiya skriptlari bilan yangi jadvallar yaratiladi va ma'lumot `INSERT ... SELECT` yoki Spring Batch job'i orqali ko'chiriladi. Kod tomonida bitta JPA `@Entity` ikkita entity'ga va bitta `JpaRepository` ikkita repository'ga ajratiladi; bitta `@Transactional` metod ichidagi yozuv Saga'ga (Axon Framework, Eventuate Tram yoki qo'lda yozilgan orchestrator + Outbox) aylantiriladi. Avvalgi birlashgan o'qishlarni saqlab qolish uchun vaqtincha database view yoki API-level composition (`RestClient` bilan ikki service'dan o'qib birlashtirish) ishlatiladi.

**Qo'llanish keyslari:**
- Legacy `customer` jadvalidagi login ma'lumotlarini Identity Service'ga, manzil va buyurtma tarixini Customer Service'ga ajratish.
- `item` jadvalidagi narx va ombor qoldig'ini Pricing va Inventory service'lariga bo'lish.
- Bitta keng `order` jadvalini Order (status, mijoz) va Payment (to'lov holati, tranzaksiya ID) bo'laklariga ajratish.
- God-table'ni (100+ ustun) bo'lib, har bir jamoaga o'z sxemasi ustida mustaqil DDL qilish imkonini berish.
- PII ustunlarini alohida, shifrlangan va audit qilinadigan sxemaga chiqarish (GDPR talabi).

**Ehtiyot bo'ling:** Bo'lishdan keyin avval bitta ACID tranzaksiya bo'lgan yozuv eventual consistent bo'ladi - biznes bu holatni (masalan, "ombor hali yangilanmagan") qabul qilishga tayyormi, buni mahsulot egasidan oldin so'rang. Jadvalni bo'lishdan oldin domainni to'g'ri modellashtirmaslik eng keng tarqalgan xato: noto'g'ri chiziq bo'yicha bo'lingan jadval service'lar orasida doimiy chatty integratsiya tug'diradi.

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

**Ehtiyot bo'ling:** Baza endi yaxlitlikni kafolatlamaydi - "o'lik" ID'lar (orphan) paydo bo'ladi, shuning uchun o'chirishni soft delete qilib, davriy consistency tekshiruvi va "nomalum element" uchun graceful degradation qo'shish kerak. Bitta SELECT o'rniga bir so'rov va unga ulangan servis chaqiruvi kelgani uchun operatsiyaning umumiy latency'si oshadi: kitob buni SKU'larni bitta so'rovda to'p-to'p (bulk) olish va kerakli ma'lumotni lokal keshlash bilan yumshatishni taklif qiladi, shuning uchun batch API va cache'ni loyihaning boshida rejalashtiring. Qaytarib bo'lmas xato esa boshqa joyda: o'chirishdan oldin "bu yozuv kimda ishlatiladi" deb so'rash yechim emas - uni to'g'ri bajarish uchun lock kerak bo'ladi va har bir yangi iste'molchi bilan teskari bog'liqlik ko'payadi.

## 27.16 Har bir bounded context uchun repository (Repository per Bounded Context)

**Tavsif:** Monolitda bitta katta repository/DAO qatlami butun bazani qamrab olgan bo'ladi. Bu patternda baza hali ham bitta, ammo data access kodi bounded context'lar bo'yicha alohida repository guruhlariga ajratiladi: har bir modul faqat o'z repository'lari orqali o'z jadvallariga murojaat qiladi. Mapping kodi kontekst kodi bilan bir joyda turgani uchun qaysi kod sxemaning qaysi qismidan foydalanayotgani ko'rinadi va kelgusi dekompozitsiyada qaysi jadvallar ko'chishi kerakligini tushunish osonlashadi. Lekin bu to'liq manzara emas: repository bo'linishi baza darajasidagi constraint'larni, masalan ikki jadval orasidagi tashqi kalit munosabatini ko'rsatmaydi - buni ko'rish uchun sxemani vizuallashtiradigan alohida vosita kerak bo'ladi.

**Spring'da qayerda uchraydi:** `@EnableJpaRepositories(basePackages = "com.shop.catalog.repo", entityManagerFactoryRef = ..., transactionManagerRef = ...)` orqali har bir context uchun alohida repository scan zonasi belgilanadi; Spring Modulith (1.x) `@ApplicationModule` va `ApplicationModules.verify()` testi bilan modullar orasidagi noqonuniy repository importlarini build vaqtida buzadi. ArchUnit qoidalari (`noClasses().that().resideInAPackage("..catalog..").should().accessClassesThat().resideInAPackage("..inventory.repo..")`) bilan chegara mustahkamlanadi. Paketlarni `package-private` repository interface'lari va public service fasadlari bilan yopish Spring'da tabiiy ishlaydi.

**Qo'llanish keyslari:**
- Monolitni bo'lishdan oldin kod bazasini context'lar bo'yicha "xaritalash" va aralash murojaatlarni topish.
- Katta `CommonDao`/`GenericRepository` sinfini modulga xos repository'larga sindirish.
- Spring Modulith bilan modular monolit qurib, keyin eng og'ir modulni service'ga chiqarish.
- Jamoalar orasida egalik chegaralarini aniqlash: qaysi jadvalga kim yozadi degan savolga javob berish.
- Monolit ichida har bir modul uchun alohida `DataSource`'ga o'tishga tayyorgarlik.

**Ehtiyot bo'ling:** Repository'lar ajratilgan bo'lsa-da, baza bitta bo'lgani uchun DDL hali ham umumiy va developer'lar "tezlik uchun" boshqa context jadvaliga JOIN qilish vasvasasiga tushadi - bu intizomni faqat avtomatik test (Modulith/ArchUnit) saqlab turadi. Bu pattern yakuniy maqsad emas, oraliq bosqich: unda haddan tashqari uzoq qolish "distributed monolith"ga emas, "yashirin bog'langan monolit"ga olib keladi.

## 27.17 Har bir bounded context uchun ma'lumotlar bazasi (Database per Bounded Context)

**Tavsif:** Repository'lar ajratilgandan keyingi qadam - har bir bounded context o'z sxemasini oladi, service'lar esa hali ham bitta deployment unit ichida qoladi. Bu "monolitni ajratishdan oldin bazani ajratish" strategiyasi: eng og'ir ish (ma'lumotni bo'lish, tashqi kalitlarni olib tashlash, JOIN'larni kodga ko'chirish) deployment o'zgarishidan ajratib bajariladi. Kitobdagi misolda uchta izolyatsiyalangan bounded context bitta servis sifatida deploy qilinadi, lekin har biri butunlay alohida bazaga ega bo'ladi - keyinchalik ularni microservice'ga ajratish kerak bo'lsa, bu ancha oson bo'lishi uchun. O'sha misolda ajratish hech qachon kerak bo'lmagan: tizim yillar davomida bir necha bazaga ega modular monolit holida qolgan. Shuning uchun patternning asosiy qiymati - tanlov erkinligini saqlash; Newman uni ayniqsa noldan qurilayotgan yangi tizimlar uchun tavsiya qiladi, chunki bunday tizimda domen chegaralari hali yetilmagan bo'ladi.

**Spring'da qayerda uchraydi:** Har bir context uchun alohida `DataSource`, `LocalContainerEntityManagerFactoryBean` va `JpaTransactionManager` bean'lari e'lon qilinadi (`@ConfigurationProperties("app.datasource.catalog")` + `DataSourceBuilder`), har biriga o'z Flyway instansiyasi (`spring.flyway.locations` yoki programmatik `Flyway.configure()`) biriktiriladi. Context'lar oshib ketadigan yozuvlar uchun XA/`ChainedTransactionManager`dan ko'ra Outbox + `@TransactionalEventListener` yoki Saga tanlanadi. Testlarda Testcontainers (`@ServiceConnection`, Spring Boot 3.1+) bilan har bir sxema uchun alohida konteyner ko'tarilib, chegaralar real tekshiriladi.

**Qo'llanish keyslari:**
- Monolitni saqlab turgan holda `catalog`, `inventory`, `billing` uchun uchta alohida PostgreSQL sxemasiga o'tish.
- Yuklamasi juda farq qiladigan modulni (masalan, reporting) alohida read-optimized bazaga chiqarish.
- Service'ga ajratish rejasidagi modul uchun baza chegarasini oldindan sinovdan o'tkazish.
- Har bir jamoaga o'z migratsiya skriptlari va DDL deploy jadvalini berish.
- Compliance talabi bo'lgan ma'lumotni (to'lov kartalari, PII) alohida, qattiq nazoratli bazaga ajratish.

**Ehtiyot bo'ling:** Bazani bo'lgandan so'ng cross-context JOIN'lar yo'qoladi va ba'zi hisobotlar sindirilishi mumkin - migratsiyadan oldin barcha hisobot va analitik so'rovlarni inventarizatsiya qilib, ularni replica, data warehouse yoki CQRS read model'ga ko'chirishni rejalashtiring. Distributed tranzaksiya (XA) bilan muammoni "yopish" vasvasasiga tushmang: bu ishlash tezligi va operatsion murakkablikni keskin oshiradi.

## 27.18 Monolit ma'lumotga kirish qatlami sifatida (Monolith as Data Access Layer)

**Tavsif:** Yangi service monolit bazasiga to'g'ridan-to'g'ri ulanish o'rniga monolitda yaratilgan API orqali ma'lumot oladi. Bu patternda monolit o'z ma'lumoti uchun "haqiqat manbai" va yagona yozuvchi bo'lib qoladi, yangi service esa uning mijozi bo'ladi. Ma'lumotni ko'chirish qiyin yoki hali vaqti kelmagan, lekin yangi funksionallikni alohida service sifatida yozish kerak bo'lgan hollarda ideal: baza sxemasi yashirin qoladi va keyinchalik ma'lumot ko'chirilganda API shartnomasi o'zgarmaydi.

**Spring'da qayerda uchraydi:** Monolitda yangi REST endpoint'lar `@RestController` + DTO (ko'pincha Java record) bilan ochiladi; shartnoma OpenAPI (springdoc-openapi 2.x) orqali hujjatlanadi va Spring Cloud Contract yoki Pact bilan consumer-driven test qilinadi. Yangi service tomonida `RestClient` yoki `@HttpExchange` interface client, Resilience4j `@CircuitBreaker` va `@Cacheable` ishlatiladi. O'qish yuklamasini kamaytirish uchun monolit `ETag`/`If-None-Match` (Spring'ning `ShallowEtagHeaderFilter`) yoki `Cache-Control` qo'yadi; katta hajmdagi o'qish uchun esa monolit o'zgarish event'larini Kafka'ga (`spring-kafka`) chiqaradi.

**Qo'llanish keyslari:**
- Yangi Recommendation Service monolitdagi mijoz profilini monolit API'si orqali o'qishi.
- Mobil ilova uchun yangi BFF service yozib, ma'lumotni hali monolitdan olish.
- Hali ko'chirilmagan legacy `customer` ma'lumotiga umumiy bazaga to'g'ridan-to'g'ri ulanmasdan murojaat qilish.
- Monolit bazasiga kirishni bitta nazorat nuqtasiga yig'ib, audit va rate limiting qo'shish.
- Vaqtinchalik qadam: API birinchi bo'lib yaratiladi, keyin uning orqasidagi ma'lumot sekin-asta yangi service'ga ko'chiriladi.

**Ehtiyot bo'ling:** Monolitga qattiq bog'lanish saqlanadi - monolit ishdan chiqsa yangi service ham ishlamaydi, shuning uchun circuit breaker, timeout va cache bilan graceful degradation shart. Agar yangi service shu ma'lumotni o'zgartirishi (yozishi) kerak bo'lsa, bu pattern yetarli emas: egalik masalasini hal qilib, ma'lumotni ko'chirish yoki yozuv API'sini aniq biznes operatsiyasi sifatida modellashtirish kerak.

## 27.19 Ko'p sxemali saqlash (Multischema Storage)

**Tavsif:** Monolit bazasidan ma'lumotni chiqarish vaqt oladi va bir qadamda bajarilmaydi, shuning uchun yangi service bir vaqtda ikki joydan ishlaydi: eski ma'lumotni hali monolit bazasidan o'qiydi, o'zining yangi ma'lumotini esa o'z sxemasida saqlaydi. Kitobdagi asosiy sabab aynan yangi ma'lumot: service'ga monolitda yo'q funksionallik qo'shilib, u yangi jadval talab qilsa, o'sha jadvalni monolit bazasiga qo'shish yomon holatni yanada yomonlashtiradi - u boshidan yangi sxemada tursin. Keyin monolitdagi ma'lumot jadval-jadval yangi sxemaga ko'chiriladi. Shu yerda tashqi kalit munosabati sxema chegarasidan o'tib ketadi va bu alohida hal qilinishi kerak (27.15).

**Spring'da qayerda uchraydi:** Service ichida ikkita `DataSource` + ikkita `EntityManagerFactory` konfiguratsiya qilinadi, yoki o'z sxemasi JPA bilan, legacy sxema esa faqat o'qish uchun `JdbcClient` (Spring Framework 6.1+) / `JdbcTemplate` bilan ishlanadi. `AbstractRoutingDataSource` so'rovni kontekstga qarab marshrutlaydi; polyglot holatda (PostgreSQL + MongoDB + Redis) Spring Data'ning alohida modullari (`spring-data-jpa`, `spring-data-mongodb`) bir ilovada `@EnableJpaRepositories(basePackages=...)` va `@EnableMongoRepositories(basePackages=...)` bilan paket bo'yicha ajratiladi. Birlashgan natija service qatlamidagi aggregator (facade) sinfida yig'iladi.

**Qo'llanish keyslari:**
- Yangi Invoice Service'ga hisob-fakturani ko'rib chiqish funksionalligi qo'shilib, ko'rib chiquvchilar jadvali o'z sxemasida saqlanishi, asosiy hisob-faktura ma'lumoti esa hali monolitda qolishi.
- Issiq (hot) ma'lumotni yangi PostgreSQL'da, arxiv ma'lumotni legacy Oracle'da qoldirish.
- Monolitdagi ma'lumotni jadval-jadval yangi sxemaga ko'chirish davomida ikki sxemadan parallel o'qish.
- Yangi Customer Service profil ma'lumotini o'z bazasida, hali ko'chirilmagan kredit tarixini esa monolit sxemasida o'qishi.
- Reglament tufayli ma'lum ma'lumot turi ma'lum bazada qolishi kerak bo'lgan holatlar.

**Ehtiyot bo'ling:** Ikki manbadan o'qish murakkablikni, latency'ni va xato ehtimolini oshiradi - bu holatga aniq tugash muddati (sunset date) qo'ymasa, "vaqtinchalik" arxitektura doimiy texnik qarzga aylanadi. Ikki sxema ustida bitta tranzaksiya kafolati yo'q, shuning uchun yozuvlarni bitta sxemaga cheklashga harakat qiling.

## 27.20 Statik reference data nusxasi, kutubxonasi va servisi (Duplicate Static Reference Data)

**Tavsif:** Davlat kodlari, kiyim o'lchamlari, valyuta ro'yxati kabi kam o'zgaradigan, ammo odatda muhim bo'lgan reference data bir necha service'ga kerak bo'ladi. "Shared Static Data" kitobda pattern nomi emas, shu muammoni ko'rsatuvchi misol sarlavhasi; uning ostida to'rtta alohida nomlangan pattern beriladi: Duplicate Static Reference Data (har service o'z sxemasida nusxa saqlaydi), Dedicated Reference Data Schema (27.21), Static Reference Data Library (ma'lumot kod yoki konfiguratsiya fayliga joylanib, kerak bo'lgan har service'ga kutubxona sifatida ulanadi) va Static Reference Data Service (ma'lumotni beradigan alohida kichik service). Nusxalash variantini tanlashda asosiy savol - ma'lumot qanday ishlatiladi: u faqat service ichida ishlatilsa, nusxalar orasidagi nomuvofiqlik muammo emas, chunki bounded context ta'rifi ham ma'lumotni chegara ichida yashirish haqida; ammo ma'lumot service'lar orasidagi muloqotning qismi bo'lsa, nusxalashdan tashvishlanish kerak. Kutubxona varianti kichik hajmli va deyarli o'zgarmas ma'lumot uchun eng mos. Service varianti esa ma'lumotning hayot tsiklini kod bilan boshqarish, o'zgarish hodisalarini chiqarish yoki test uchun qulay shartnoma berish kerak bo'lganda tanlanadi.

**Spring'da qayerda uchraydi:** Kod sifatida yondashuvda ma'lumot Java `enum`, `record`, yoki `src/main/resources` ichidagi JSON/YAML/CSV faylga joylanib `@ConfigurationProperties` bilan type-safe o'qiladi (`@ConstructorBinding` Spring Boot 3.x'da standart). Markaziy boshqaruv uchun Spring Cloud Config Server yoki Consul/Vault backend, hamda `@RefreshScope` va Spring Cloud Bus bilan runtime refresh ishlatiladi. Service variantida ma'lumot `@Cacheable` (Caffeine/Redis) bilan uzoq TTL'da keshlanadi; `MessageSource` va `ResourceBundle` lokalizatsiyalangan statik matnlar uchun mos keladi.

**Qo'llanish keyslari:**
- ISO 3166-1 davlat kodlarini (ro'yxatda 249 ta yozuv) `enum` sifatida kutubxonaga joylab, barcha service'larga ulash.
- Kiyim o'lchamlari kabi hajmi kichik va deyarli o'zgarmas ro'yxatlarni kutubxonada saqlash.
- Britaniya pochta indekslari fayli kabi yirik, davriy yangilanadigan ma'lumotni har service'ning o'z sxemasiga nusxalash.
- Ma'lumotni o'zgartirish uchun API kerak bo'lganda yoki o'zgarish hodisalarini chiqarish kerak bo'lganda alohida kichik service yaratish; servis yaratish narxi past muhitda bu variant Function-as-a-Service platformasiga ham yaxshi mos keladi.
- Xatolik kodlari va foydalanuvchiga ko'rinadigan matnlarni `MessageSource` bundle'lari orqali boshqarish.

**Ehtiyot bo'ling:** Kutubxona yondashuvining asosiy narxi - deployment coupling: ma'lumot o'zgarsa va hamma service darhol yangi qiymatni ko'rishi kerak bo'lsa, hammasini bir vaqtda qayta deploy qilish, ya'ni lockstep release talab qilinadi - bu esa microservice'ning mustaqil deploy qoidasiga qarshi. Kitobdagi yechim boshqa: o'zgarishdan oldin yetarli ogohlantirish beriladi va production'da kutubxonaning turli versiyalari birga yashashi qabul qilinadi; agar bu sizga to'g'ri kelmasa, service variantiga o'tish kerak. Newman o'z tanlovini aniq aytadi: davlat kodlari barcha service'larda doim bir xil bo'lishi shart bo'lmasa, u ma'lumotni umumiy kutubxonada saqlaydi; murakkabroq yoki kattaroq reference data uchun har service'ning lokal bazasiga moyil bo'ladi; ma'lumot service'lar orasida izchil bo'lishi shart bo'lsa, alohida service yaratadi. Umumiy jadvalni shared database'da shundayligicha qoldirish bu ro'yxatda variant emas: u Shared Database holatiga olib keladi, ya'ni nima ochiq va nima yashirin ekanini tanlash imkoniyatidan voz kechiladi.

## 27.21 Maxsus reference data sxemasi (Dedicated Reference Data Schema)

**Tavsif:** Reference data uchun bitta haqiqat manbasi kerak bo'lsa, u alohida sxemaga ko'chiriladi - odatda barcha statik reference data uchun ajratilgan sxemaga. Barcha service'lar undan o'qiydi. Bu shared database muammolarini yo'q qilmaydi: kitob ularni to'liq hisobga olishni talab qiladi, lekin ma'lumotning tabiati tufayli (kam o'zgaradi, tuzilishi sodda) coupling va o'zgarish tashvishi qisman yumshaydi va sxemani belgilangan interfeys deb qarash osonlashadi. Shart esa aniq: sxema o'zining versiyalangan birligi sifatida boshqariladi va uning tuzilishi iste'molchilar uchun servis interfeysi ekani hammaga tushuntiriladi. Variantning o'ziga xos foydasi shu: ma'lumot sxemada turgani uchun service'lar uni o'z lokal ma'lumoti bilan JOIN qilib so'rov bera oladi. Buning uchun ikkala sxema bitta baza dvigichida turishi kerak, bu esa mantiqiy va jismoniy tuzilish o'rtasidagi moslashtirishni qiyinlashtiradi va yagona nosozlik nuqtasi xavfini keltiradi.

**Spring'da qayerda uchraydi:** Bu infratuzilma/baza darajasidagi qaror; Spring tomonida har bir service'da ushbu sxemaga `read-only` baza useri bilan ikkinchi `DataSource` qo'shiladi va o'qish `@Transactional(readOnly = true)` + `JdbcClient`/JPA bilan bajariladi. Sxemaga DDL va DML faqat owner service'ning Flyway/Liquibase migratsiyalari orqali qo'llaniladi, boshqalarda `spring.flyway.enabled=false` qoldiriladi. O'zgarishlar haqida xabar berish uchun owner service Kafka'ga event chiqaradi va iste'molchilar `@CacheEvict` bilan lokal cache'ni tozalaydi; tez o'qish uchun Redis (`spring-boot-starter-data-redis`) yoki Caffeine ishlatiladi.

**Qo'llanish keyslari:**
- Butun mamlakat bo'yicha pochta indekslari va manzil katalogini yagona sxemada saqlash.
- Bank identifikatorlari (BIC/IBAN) va to'lov marshrutlash jadvallarini markaziy sxemada ushlab turish.
- Tibbiy klassifikatorlar (ICD-10) yoki mahsulot klassifikatori kabi yirik, standartlashtirilgan ma'lumotlar bazasi.
- Valyuta kurslari tarixini bitta egalik qiluvchi service yozib, boshqalar hisob-kitob uchun o'qishi.
- Soliq jurisdiktsiyalari jadvalini compliance jamoasi boshqarishi va barcha service'lar o'qishi.

**Ehtiyot bo'ling:** Kitobning ogohlantirishi bitta va qat'iy: sxema formatidagi har qanday o'zgarish bir necha service'ga sezilarli ta'sir qiladi va buzadigan o'zgarish kiritish og'riqli bo'ladi. Shuning uchun faqat qo'shimcha (additive) o'zgarish siyosatini va ustun o'chirishdan oldin deprecation davrini qabul qiling. Shu korpusning amaliy tavsiyasi: "faqat o'qish" intizomini texnik vositalar bilan (baza darajasidagi grant, alohida read-only user) majburlash - aks holda vaqt o'tishi bilan kimdir yozishni boshlaydi.

## 27.22 Migratsiyani bosqichma-bosqich joriy etish va qaytarish

**Tavsif:** Buni alohida pattern deb ko'rsatmang: "Incremental Rollout and Rollback" kitobda pattern nomi emas, bu bir necha nomlangan texnikaning birlashtirilgan amaliyoti. Newman strangler fig'ni tavsiflaganda marshrutni almashtirishni feature toggle bilan amalga oshirishni taklif qiladi va o'sha proxy nuqtasini yangi funksionallikni canary rollout yoki to'laqonli parallel run bilan bosqichma-bosqich joriy etish uchun qulay joy deb ataydi; "incremental rollout" u yerda arxitektura o'zgarishini boshqa ishlar bilan birga, kichik qadamlarda bajarish usuli deb tushuntiriladi, ya'ni "katta portlash" bilan qayta platformalashtirish kerak emas. Dark launching, parallel run va canary release esa progressive delivery deb nomlangan umumiy soyabon ostida birlashtiriladi. Newman ikkinchi kitobida buzadigan o'zgarishni bosqichga ajratish usulini "expand and contract" patterni deb nomlaydi: avval eski va yangi usul birga qo'llab-quvvatlanadi (expand), iste'molchilar yangisiga o'tgach eskisi olib tashlanadi (contract). Birlashgan qoida esa strangler fig'ning asosiy foydasidan kelib chiqadi: har bir qadam kichik bo'lishi va oson qaytarilishi kerak, shuning uchun har qadam uchun rollback rejasi oldindan yoziladi.

**Spring'da qayerda uchraydi:** Marshrutlash Spring Cloud Gateway (`spring-cloud-starter-gateway-server-webflux`) predicate/filter'lari yoki service mesh (Istio `VirtualService` weight) darajasida bajariladi; ilova ichida Togglz/Unleash/FF4j yoki `@ConditionalOnProperty` + `@Primary` bean almashtirish ishlatiladi. Parallel Run uchun eski va yangi implementatsiya bir interfeysga yozilib, farq `Micrometer` counter'i va struktura log'iga yoziladi; kuzatuv uchun Micrometer Tracing (Spring Boot 3.x) + OpenTelemetry va `/actuator/health`, `/actuator/prometheus` endpoint'lari ishlatiladi. Sxema migratsiyalari Flyway'da faqat additive, backward-compatible qadamlar sifatida yoziladi (avval ustun qo'shish, keyingi release'da eski ustunni o'chirish).

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
- Yangi Payment Service'ga trafikni kichik ulushdan boshlab bosqichma-bosqich o'tkazish va har bosqichda xatolik darajasi bilan latency'ni solishtirish.
- Parallel Run: eski va yangi narx hisoblash logikasini bir vaqtda ishlatib, natija farqini kuzatish.
- Expand va contract bilan API endpoint'ining buzadigan o'zgarishini bosqichga ajratish: eski va yangi shaklni birga chiqarish, iste'molchilar o'tgach eskisini olib tashlash.
- Feature flag bilan yangi service'ni faqat ichki xodimlar yoki bitta mijoz segmenti uchun yoqish.
- Xatolik darajasi oshganda flag'ni sekundlar ichida o'chirib, deploy'siz rollback qilish.

**Ehtiyot bo'ling:** Trafik marshrutini qaytarish oson, holatni qaytarish esa oson emas: ko'chirilgan funksionallik holatni saqlasa, uni yangi servisga va kerak bo'lsa orqaga qanday ko'chirish masalasi alohida o'ylanadi. Agar ma'lumot oldin ko'chirilib, keyin monolitga qaytilsa, yangi sxemada o'zgargan ma'lumot monolit bazasida ko'rinmaydi va holat yo'qoladi; shuning uchun orqaga qaytish yo'li ochiq bo'lishi kerak bo'lgan davrda ikki sxemani sinxron ushlash zarur (27.12). Feature flag'lar tozalanmasa kod bazasi tezda boshqarib bo'lmas holatga keladi: har bir migratsiya flag'iga yaroqlilik muddati va uni o'chirish tiketini biriktiring.

## 27.23 Dekompozitsiya yondashuvini tanlash (Choosing a Decomposition Approach)

**Tavsif:** Bu bo'limdan boshlab keladigan sakkizta yozuv *Software Architecture: The Hard Parts* ning dekompozitsiya patternlariga tayanadi va yuqoridagi Newman patternlaridan **boshqa yondashuv**: Newman patternlari chaqiruv oqimini va ma'lumotni xavfsiz yo'naltirish haqida (masalan, [bo'g'uvchi anjir ilovasi](#271-boguvchi-anjir-ilovasi-strangler-fig-application)), Hard Parts patternlari esa monolit kodining ichki tuzilishini oldindan o'lchab, bog'liqlikni aniqlab va komponentlarni domenga guruhlab, undan keyin servis ajratish haqida. Ikkisi raqobatchi emas: Hard Parts tartibi monolitni ajratishga tayyorlaydi, Newman patternlari esa o'sha ajratishni ishlab turgan tizimda bajaradi. Kitob dekompozitsiyani ikki yondashuvga ajratadi va tanlovni kodning holatiga bog'laydi: kod bazasida komponent chegaralari ko'rinsa komponentga asoslangan dekompozitsiya, kod chegarasiz [katta loy to'pi](25-anti-patternlar.md#2554-katta-loy-top-big-ball-of-mud) bo'lsa taktik ayirish. Birinchi savol esa bundan ham oldin turadi: bu kod umuman bo'linadimi. Javobni kitob coupling metrikalari bilan beradi: afferent (kiruvchi) va efferent (chiquvchi) coupling, ulardan chiqadigan abstractness va instability, va ikkisini birga baholaydigan "asosiy ketma-ketlikdan masofa". Komponentlarning ko'pi "foydasizlik zonasi" (juda abstrakt) yoki "og'riq zonasi" (abstraksiya yetishmaydigan, mo'rt kod) ga tushsa, ichki tuzilishni tuzatishga vaqt sarflash o'zini oqlamasligi mumkin.

**Spring'da qayerda uchraydi:** Metrikalarni o'lchash build ichida bajariladi: JDepend (Maven `jdepend-maven-plugin`) paket bo'yicha Ca, Ce, A, I va D qiymatlarini beradi, ArchUnit (`com.tngtech.archunit.library.metrics`) esa komponent bog'liqligi metrikalarini testdan hisoblaydi. Spring loyihasida komponent odatda `@SpringBootApplication` paketi ostidagi funksional paket (`com.shop.ticket.assign`) bo'ladi va Spring Modulith `ApplicationModules.of(...).verify()` shu chegaralarni testda qotiradi. Qarorning o'zi [ADR tuzilishi](../architect/03-qaror-qabul-qilish-va-uni-hujjatlashtirish.md#31-adr-architecture-decision-record-tuzilishi-kontekst-qaror-oqibat-holat) sifatida yoziladi: kitobdagi misolda ham tanlov ADR bilan hujjatlashtirilgan.

```java
/** Robert Martin metrikasi: asosiy ketma-ketlikdan masofa, D = |A + I - 1|. */
public static double distanceFromMainSequence(
        int abstractTypes, int concreteTypes, int efferent, int afferent) {
    double abstractness = (double) abstractTypes / (abstractTypes + concreteTypes);
    double instability = (double) efferent / (efferent + afferent);
    return Math.abs(abstractness + instability - 1);
}
```

**Qo'llanish keyslari:**
- Migratsiya boshlashdan oldin kod bazasining bo'linishga yaroqliligini baholash va natijani ADR ga yozish.
- Komponent chegarasi bor modullar bilan chegarasiz modullarni ajratib, ularga turli yondashuv tanlash.
- Texnik qarz baholashda qaysi paketlar og'riq zonasida turganini topib, refaktoring navbatini tuzish.
- Yangi kelgan jamoaga notanish monolitning ichki tuzilishini raqam bilan ko'rsatish.
- "Bir tishlam bir tishlam" (elephant migration) tartibsiz ajratishdan voz kechishni asoslash: kitob buni anti-pattern deb ataydi va natijasi taqsimlangan monolit bo'ladi.

**Ehtiyot bo'ling:** Bitta metrika qaror qilmaydi: instability nolga yaqin komponent ham barqaror (ko'pi abstrakt), ham qotib qolgan (ko'pi konkret) bo'lishi mumkin, shuning uchun A va I har doim birga o'qiladi. Yuqori barqarorlikning narxi ham bor: har komponent to'liq o'zicha bo'lsa, takrorlanish paydo bo'ladi. Va metrikalar faqat kodga qaraydi: jamoa tuzilishi, relizlar bog'liqligi va ma'lumotning holati bu raqamlarda ko'rinmaydi, ularni [monolit va mikroservis qarori](14-microservices-patternlari.md#141-monolitik-arxitektura-va-mikroservis-arxitekturasi-qarori-monolithic-architecture-vs-microservice-architecture-decision) bilan birga baholang.

## 27.24 Taktik ayirish (Tactical Forking)

**Tavsif:** Ichki tuzilishi yo'q monolitdan bo'lak ajratish qiyin, chunki ajratilayotgan bo'lak bilan birga bog'liqliklar zanjiri tortib keladi. Taktik ayirish yo'nalishni teskari qiladi: kerakli bo'lakni chiqarish o'rniga, keraksizini o'chirish. Monolitning butun kod bazasi har jamoaga to'liq nusxa qilib beriladi, keyin har jamoa o'z nusxasidan kerak bo'lmagan kodni o'chiradi. O'chirish osonroq, chunki kuchli bog'langan kodda bog'liqlikni yechish shart emas: funksionallik ajratilgandan keyin hech narsani buzmaydigan kodni o'chirish kompilyatsiya va test bilan tekshiriladi. Pattern nomini Fausto De La Torre bergan va nom o'zini oqlaydi: bu strategik emas, taktik yo'l. Natijada monolit yirik donali servislarga bo'linadi, lekin kodning sifati o'zgarmaydi, faqat hajmi kamayadi.

**Spring'da qayerda uchraydi:** Amalda bu repozitoriy va build darajasidagi ish: monolit repozitoriysi nusxalanadi, har nusxada `src/main/java` dagi keraksiz paketlar va ularga tegishli `@Configuration`, `@Entity`, Flyway migratsiyalari olib tashlanadi, `pom.xml` dan ishlatilmaydigan starter'lar chiqariladi. Spring Boot da keraksiz avtokonfiguratsiyani `spring.autoconfigure.exclude` yoki bog'liqlikni olib tashlash bilan yopiladi; qolgan kodni topish uchun `./mvnw dependency:analyze` va IDE ning "unused" tahlili ishlatiladi. Har nusxada `@SpringBootTest` kontekst yuklanishi o'chirishdan keyin ham ishlashi smoke test rolini o'ynaydi.

```bash
# Har jamoa monolitning to'liq nusxasini oladi
git clone --origin monolith https://git.example.com/shop/monolith.git ticket-service
git clone --origin monolith https://git.example.com/shop/monolith.git customer-service

# Keraksiz paketlar o'chiriladi va "hech narsa buzilmadi" build bilan tasdiqlanadi
cd ticket-service
rm -rf src/main/java/com/shop/reporting src/main/java/com/shop/billing
./mvnw -q verify
```

**Qo'llanish keyslari:**
- Tuzilishi yo'q legacy monolitni muhim bo'lgani uchun tez ikkiga bo'lish, keyin har bo'lakni alohida tozalash.
- Ikki jamoa bir kod bazasida bir-birini to'sib qo'yayotganda deployment bog'liqligini darhol uzish.
- Komponent chegarasi topilmagan, lekin biznes chegarasi aniq bo'lgan tizimni ajratish.
- Qolgan ishni rejalashtirish uchun avval nusxani chiqarib, keyin [komponentlarni aniqlash va o'lchash](#2725-komponentlarni-aniqlash-va-olchash-identify-and-size-components) ni yangi, kichikroq kod bazasida bajarish.
- Ajratish qanchalik real ekanini bir hafta ichida tekshirish: nusxada o'chirish qanchalik oson kechgani dalil bo'ladi.

**Ehtiyot bo'ling:** Natijadagi servislarda monolitdan qolgan, hech kim chaqirmaydigan ko'p kod qoladi va qo'shimcha ish qilinmasa, kod sifati monolitdagidan yaxshi bo'lmaydi: faqat kamroq bo'ladi. Umumiy kod ikki nusxada ketadi va nomlar tez farqlanib ketadi, shuning uchun umumiy bo'lakni keyinroq [umumiy domen komponentlarini yig'ish](#2726-umumiy-domen-komponentlarini-yigish-gather-common-domain-components) bilan qaytarib birlashtirish rejasi oldindan yozilsin. Nusxa olishdan oldin servis chegarasi belgilangan bo'lishi shart: nechta fork kerakligini bilish uchun chegara oldindan aytiladi, komponentga asoslangan yo'lda esa chegara guruhlashdan o'zi chiqadi.

## 27.25 Komponentlarni aniqlash va o'lchash (Identify and Size Components)

**Tavsif:** Quyidagi oltita pattern *Software Architecture: The Hard Parts* ning komponentga asoslangan dekompozitsiya ketma-ketligini tashkil qiladi ([dekompozitsiya yondashuvini tanlash](#2723-dekompozitsiya-yondashuvini-tanlash-choosing-a-decomposition-approach)) va ular Newman patternlaridan oldin, monolitni ajratishga tayyorlash bosqichida ketma-ket qo'llanadi. Servis sinflardan emas, komponentlardan yasaladi, shuning uchun monolit migratsiyasining birinchi qadami komponentlar ro'yxatini tuzish va ularning o'lchamini tenglashtirish. Kitob komponentni namespace yoki papka bilan belgilaydi va o'lcham mezoni sifatida sinf yoki qator sonini emas, komponent ichidagi **gaplar sonini** (statement, Java da nuqtali vergul bilan tugaydigan amal) taklif qiladi: sinf va metod dizayni har programmistda boshqacha, gaplar soni esa komponent qancha ish qilayotganiga yaqinroq ko'rsatma beradi. Mukammal metrika emas, lekin yaroqli indikator. Qoida: komponent o'lchamlari o'rtachadan bir-ikki standart og'ish ichida bo'lsin va har komponentga tegishli kod ulushi taxminan teng taqsimlansin. Juda katta komponent boshqalarga ko'proq bog'langan bo'lib chiqadi va servisga ajratish qiyinlashadi; juda kichigi yetarli ish qilmaydi.

**Spring'da qayerda uchraydi:** Komponent chegarasi Spring loyihasida paket bo'lib ko'rinadi (`com.shop.ticket.assign`), shuning uchun inventarni papka daraxtidan hisoblash mumkin. Avtomatlashtirish CI/CD ichida fitness function sifatida ishlaydi: yangi yoki yo'qolgan komponent haqida ogohlantirish, va o'rtachadan belgilangan standart og'ishdan oshgan komponent haqida ogohlantirish. Spring Modulith `ApplicationModules.of(ShopApplication.class)` bilan modullar ro'yxatini beradi va uni testda qotirish mumkin; ArchUnit `slices().matching("com.shop.(*).(*)")` bilan shu ro'yxatni qoida shaklida ushlab turadi. Hisoblashning o'zi oddiy Java yoki Gradle/Maven task bo'lishi kifoya.

```java
/** Komponent o'lchami: namespace ichidagi gaplar soni. */
public static Map<String, Long> statementsPerComponent(Path sourceRoot) throws IOException {
    try (Stream<Path> files = Files.walk(sourceRoot)) {
        return files.filter(path -> path.toString().endsWith(".java"))
                .collect(Collectors.groupingBy(
                        path -> sourceRoot.relativize(path).getParent().toString().replace('/', '.'),
                        Collectors.summingLong(ComponentSizer::countStatements)));
    }
}

private static long countStatements(Path file) {
    try {
        return Files.readAllLines(file).stream().filter(line -> line.strip().endsWith(";")).count();
    } catch (IOException e) {
        throw new UncheckedIOException(e);
    }
}
```

**Qo'llanish keyslari:**
- Migratsiya boshida komponent inventarini tuzib, uni build da qotirish va keyingi o'zgarishlarni ogohlantirish bilan ushlash.
- O'rtachadan uch standart og'ishdan oshgan komponentni topib, uni servisga ajratishdan oldin bo'lish.
- Juda kichik komponentlarni qo'shni komponentga qo'shib, servislar sonini oldindan kamaytirish.
- Monolitda kod ulushi bo'yicha eng katta paketni aniqlab, migratsiya navbatini shu ro'yxat bilan tuzish.
- Jamoa yangi paket qo'shganini relizda sezib, uni domen ro'yxatiga kiritish yoki rad etish.

**Ehtiyot bo'ling:** Gaplar soni murakkablikning o'rnini bosmaydi: bir xil o'lchamdagi ikki komponentning biri sodda CRUD, ikkinchisi chigal hisob-kitob bo'lishi mumkin, shuning uchun o'lchamni [cognitive complexity](../sonarqube/15-cognitive-complexity-va-takrorlanishni.md#151-cognitive-complexity-qanday-hisoblanadi-ortish-va-chuqurlik-jarimasi) bilan birga o'qing. Ro'yxatni bir marta tuzib qo'yish ham yetmaydi: migratsiya davom etar ekan monolit o'zgaradi, shuning uchun inventar tekshiruvi har relizda ishlashi kerak. Va o'lchamni tenglashtirish maqsad emas, vosita: domen chizig'i bo'yicha to'g'ri bo'lingan katta komponentni faqat raqam uchun bo'lish keyinchalik servislar orasida chatty integratsiya tug'diradi.

## 27.26 Umumiy domen komponentlarini yig'ish (Gather Common Domain Components)

**Tavsif:** Monolitda bir xil biznes mantiqi bir necha komponentda takrorlanib yotadi va ajratish paytida har bir nusxa alohida servisga aylanib ketish xavfi bor. Bu pattern shu takrorlanishni oldin bir komponentga yig'adi. Kitob umumiy **domen** funksionalligini umumiy **infratuzilma** funksionalligidan ajratadi: domen funksionalligi biznes jarayonining qismi (xabarnoma yuborish, ma'lumotni formatlash, validatsiya) va faqat ba'zi jarayonlarga umumiy; infratuzilma funksionalligi operatsion (log, metrika, xavfsizlik) va hamma jarayonga umumiy. Umumiylikni topish asosan qo'l ishi, lekin ikki ishorasi bor: bir sinfning turli namespace lardagi sinflar tomonidan ishlatilishi, va komponent nomining oxirgi tugunining takrorlanishi. Kitobdagi misol aniq: `ticket.audit`, `billing.audit` va `survey.audit` uchalasi ham audit jadvaliga qator yozadi, demak ular `shared.audit` ga yig'iladi. Natijada kod takrorlanishi ham, kelgusi servislar soni ham kamayadi.

**Spring'da qayerda uchraydi:** Yig'ilgan komponent Spring da oddiy `@Component` yoki `@Service` bean bo'ladi va uni ishlatuvchi modullar konstruktor orqali oladi. Umumiy kodni servis qilish shart emas: u compile vaqtida bog'lanadigan umumiy kutubxona (alohida Maven modul) bo'lishi ham mumkin, va tanlov [shared library bog'liqligi](14-microservices-patternlari.md#1436-shared-library-bogliqligi-shared-library-coupling---antipattern) bilan birga hal qilinadi. Ogohlantirishni avtomatlashtirish uchun paket nomining oxirgi tugunlari bo'yicha takrorni qidiradigan fitness function yoziladi va yolg'on ogohlantirishni kamaytirish uchun istisno ro'yxati (`.validate`, `.calculate` kabi) saqlanadi.

```java
// oldin: uchta komponentda bir xil audit yozuvi
//   com.shop.ticket.audit.TicketAuditWriter
//   com.shop.billing.audit.BillingAuditWriter
//   com.shop.survey.audit.SurveyAuditWriter
package com.shop.shared.audit;

@Component
public class AuditWriter {

    private final AuditEntryRepository repository;

    AuditWriter(AuditEntryRepository repository) {
        this.repository = repository;
    }

    public void record(String actor, String action, String subjectId) {
        repository.save(new AuditEntry(actor, action, subjectId, Instant.now()));
    }
}
```

**Qo'llanish keyslari:**
- Uch-to'rt modulda takrorlangan xabarnoma yuborish kodini bitta `shared.notification` komponentiga yig'ib, bitta Notification servisiga yo'l tayyorlash.
- Audit yozuvini yozadigan kodni yig'ib, keyin uni umumiy kutubxona yoki umumiy servis sifatida chiqarish qarorini bir joyda qabul qilish.
- Turli paketlardagi `SmtpConnection` kabi umumiy sinf foydalanuvchilarini sanab, yashiringan umumiy domen mantiqini topish.
- Paket nomining oxirgi tuguni takrorlanishini CI da ogohlantirishga aylantirib, yangi takrorlanishni paydo bo'lganda ushlash.
- Taktik ayirishdan keyin ikki nusxada qolgan umumiy kodni qaytarib birlashtirish.

**Ehtiyot bo'ling:** Umumiylik va domen chegarasini adashtirish oson: ikki joyda bir xil ko'rinadigan kod ikki boshqa biznes qoidasi bo'lsa, ularni yig'ish keyinchalik bitta komponentni ikki jamoa tortadigan holatga olib keladi. Nomning o'xshashligi dalil emas, faqat ishora: `.validate` yoki `.calculate` bilan tugaydigan paketlar bir-biriga aloqasiz bo'lishi mumkin. Va umumiy komponentni darhol servis qilib yubormang: umumiy servis har chaqiruvga latency va nosozlik nuqtasi qo'shadi, umumiy kutubxona esa reliz bog'liqligi qo'shadi, ikkisining narxini oldin solishtiring.

## 27.27 Komponentlarni tekislash (Flatten Components)

**Tavsif:** Komponent papka yoki namespace bilan belgilanadi, lekin namespace boshqa tugun bilan kengaytirilsa (masalan `survey` ustiga `survey.templates` qo'shilsa), eski namespace komponent bo'lishdan to'xtaydi va subdomain ga aylanadi. Kitob komponentni namespace ning **oxirgi tuguni** deb ta'riflaydi va shundan uchta atama chiqaradi: komponent (kod turgan oxirgi tugun), root namespace (boshqa tugun bilan kengaytirilgan tugun, ya'ni subdomain) va **orphaned class** (root namespace ichida qolib ketgan, hech qaysi komponentga tegishli bo'lmagan sinflar). Tekislash shu orphaned sinflarni joyiga ko'chirishdan iborat: ichki tugundagi kodni yuqoriga ko'tarish yoki root namespace dagi kodni pastdagi tugunlarga tushirish. Buning amaliy sababi oddiy: tekislanmagan tuzilishda "bu ikki komponent bir servisga tushadimi yoki ikkitaga" degan savolga javob yo'q.

**Spring'da qayerda uchraydi:** Tekislash sof refaktoring: paketlar ko'chiriladi, `@Entity`, `@Repository` va `@Configuration` sinflari yangi paketga o'tadi, `@ComponentScan` va `@EnableJpaRepositories(basePackages = ...)` qiymatlari yangilanadi. Spring Boot da avtoskanlash `@SpringBootApplication` paketidan boshlanadi, shuning uchun ko'chirish bean topilishini buzmaydi, lekin `basePackages` qo'lda yozilgan joylar buziladi: ularni grep bilan topish kerak. Qoidani ushlab turish uchun ArchUnit testi yoziladi: kengaytirilgan namespace larda sinf qolmasin.

```java
@AnalyzeClasses(packages = "com.shop")
class FlatComponentsTest {

    // Root namespace (boshqa tugun bilan kengaytirilgan paket) da kod turmasin
    @ArchTest
    static final ArchRule root_namespace_da_sinf_yoq = noClasses()
            .should().resideInAnyPackage("com.shop.survey", "com.shop.ticket")
            .because("bu paketlar subdomain, komponent esa faqat oxirgi tugun bo'ladi");
}
```

**Qo'llanish keyslari:**
- `survey` va `survey.templates` kabi ikki darajali tuzilishni bir komponentga yig'ib, servis chegarasi savolini yopish.
- Root namespace da qolgan "umumiy" yordamchi sinflarni topib, ularni o'z komponentiga yoki umumiy komponentga chiqarish.
- Komponent inventarini o'lchash oldidan tekislash: tekislanmagan tuzilishda o'lcham raqamlari chalkash chiqadi.
- Paket daraxti chuqurlashib ketgan modulda "qaysi tugun komponent" savolini bir marta hal qilish.
- Migratsiya davomida yangi orphaned sinf paydo bo'lishini relizda ushlash.

**Ehtiyot bo'ling:** Bu patternda subyektivlik ko'p: kodni yuqoriga ko'tarishmi yoki pastga tushirishmi degan savolga qoida javob bermaydi, qarorni domen aytadi, shuning uchun har tekislashni ADR yoki arxitektura story si bilan yozib qo'ying. Paket ko'chirish git tarixini o'qishni qiyinlashtiradi va boshqa jamoalardagi ochiq branch larni konfliktga olib keladi: tekislashni alohida, faqat ko'chirishdan iborat commit da bajaring va shu relizda boshqa o'zgarish qilmang. Va tekislash kodni yaxshilamaydi: u faqat chegarani ko'rinadigan qiladi, [xudo obyekt](25-anti-patternlar.md#251-xudo-obyekt-god-object) tekislangandan keyin ham xudo obyekt bo'lib qoladi.

## 27.28 Komponent bog'liqliklarini aniqlash (Determine Component Dependencies)

**Tavsif:** Migratsiya haqida eng ko'p beriladigan uch savolga (bo'lish real bo'ladimi, qancha ish bor, bu refaktoringmi yoki qayta yozishmi) javob komponentlar orasidagi bog'liqlik grafigidan chiqadi. Pattern shu grafikni tuzadi: har komponentning kiruvchi (afferent, CA) va chiquvchi (efferent, CE) bog'liqligi sanaladi, ikkisining yig'indisi jami coupling (CT) bo'ladi. Muhim nuqta: hisob **komponentlar orasidagi** bog'liqlik haqida, komponent ichidagi sinflar bir-biriga qanchalik chalkash bog'langani bu patternda ahamiyatsiz. Bog'liqlik komponent chegarasini kesib o'tgan sinf chaqiruvidan tug'iladi: `customer.survey` paketidagi sinf `shared.notification` paketidagi sinfning metodini chaqirsa, birinchisida efferent, ikkinchisida afferent bog'liqlik paydo bo'ladi. Grafik nafaqat realligini, balki refaktoring imkonini ham ko'rsatadi: CA si yuqori komponentni ikkiga bo'lsa (ko'pchilik ishlatadigan kichik bo'lak va qolgani), katta bo'lakning CA si keskin tushadi.

**Spring'da qayerda uchraydi:** Grafikni ArchUnit `slices()` qoidalari va `com.tngtech.archunit.library.metrics` paketi, Spring Modulith `ApplicationModules` hisoboti, JDepend yoki IDE ning paket bog'liqligi diagrammasi beradi. Spring loyihasida bog'liqlikning katta qismi konstruktor inyeksiyasida ko'rinadi, shuning uchun `@Service` sinflarining konstruktor parametrlari bo'yicha grafik tuzish ham ishlaydi. Chegarani qotirish uchun ArchUnit testi yoziladi: ruxsat etilmagan paketga chiquvchi bog'liqlik testni yiqitadi va bog'liqlik jim o'smaydi.

```java
@AnalyzeClasses(packages = "com.shop")
class ComponentDependencyTest {

    // Komponentlar grafigida halqa bo'lmasin: halqa ajratish tartibini buzadi
    @ArchTest
    static final ArchRule komponentlar_halqasiz = SlicesRuleDefinition.slices()
            .matching("com.shop.(*).(*)")
            .should().beFreeOfCycles();

    // Survey komponentining chiquvchi bog'liqligi ro'yxat bilan chegaralangan
    @ArchTest
    static final ArchRule survey_chiqishi_chegaralangan = classes()
            .that().resideInAPackage("com.shop.customer.survey")
            .should().onlyDependOnClassesThat()
            .resideInAnyPackage("com.shop.customer.survey", "com.shop.shared.notification", "java..");
}
```

**Qo'llanish keyslari:**
- Migratsiya hajmini boshqarma uchun qo'pol baholash: grafik zich bo'lsa javob "qayta yozish", siyrak bo'lsa "refaktoring".
- Birinchi ajratiladigan komponentni tanlash: CT si eng past komponent eng arzon birinchi qadam bo'ladi.
- CA si yuqori umumiy komponentni ikkiga bo'lib, qolgan qismining kiruvchi bog'liqligini tushirish.
- Kelgusi servis bog'liqligi grafigini oldindan ko'rish va unda halqa bormi deb tekshirish.
- Relizda bog'liqlik chegarasidan oshgan komponentni ushlab, jamoa bilan sababini muhokama qilish.

**Ehtiyot bo'ling:** Grafik statik: refleksiya, Spring ning `@Qualifier` bilan nomdan topiladigan bean lari, SpEL ifodalari va event listener lar orqali o'tadigan bog'liqlik unda ko'rinmaydi, shuning uchun [statik va dinamik bog'liqlik](../architect/05-abstraksiya-hissi-bogliqlik-va-chegaralar.md#54-bogliqlik-turlari-malumot-vaqt-joylashuv-sxema-boyicha-bogliqlik) ni birga baholang. Komponent ichidagi chalkashlikni bu pattern ko'rsatmaydi: ichi loy to'pi bo'lgan komponent grafikda toza ko'rinishi mumkin. Va bog'liqlik chegarasi uchun universal raqam yo'q: chegarani ilovaning umumiy coupling darajasi va komponentlar soniga qarab arxitektor o'zi tanlaydi, boshqa loyihadan ko'chirilgan son ma'no bermaydi.

## 27.29 Komponent domenlarini yaratish (Create Component Domains)

**Tavsif:** Har bir komponent alohida servis bo'lishi shart emas: amalda servis bilan komponent orasidagi munosabat bir-ga-ko'p, ya'ni bitta servis bir necha komponentni o'z ichiga oladi. Bu pattern bog'liq funksionallikni bajaradigan komponentlarni mantiqiy domenlarga guruhlaydi, chunki keyingi qadamda aynan shu guruhlar yirik donali domen servislariga aylanadi. Guruhlash fizik shaklda namespace orqali ko'rinadi: namespace tugunlari ierarxik bo'lgani uchun ular domen, subdomain va komponentni bir qatorda ifodalaydi (`shop.customer.billing.payment` da `customer` domen, `billing` subdomain, `payment` komponent). DDD keng tarqalishidan oldin yozilgan monolitlarda bu tuzilish yo'q, shuning uchun namespace larni refaktoring qilish kerak bo'ladi: `shop.billing.payment`, `shop.billing.history` va `shop.supportcontract` komponentlari `customer` domeniga tegishli bo'lsa, ularning namespace lari boshiga `customer` tuguni qo'shiladi.

**Spring'da qayerda uchraydi:** Refaktoring paketlarni ko'chirishdan iborat, keyin `@ComponentScan`, `@EnableJpaRepositories` va `@EntityScan` da qo'lda yozilgan `basePackages` qiymatlari yangilanadi. Guruhni qotirish uchun ArchUnit testi yoziladi: faqat tasdiqlangan domen paketlari mavjud bo'lsin, shunda jamoa jim yangi domen ochmaydi. Spring Modulith `@ApplicationModule` va `ApplicationModules.verify()` shu guruhlashni modul darajasida tekshiradi va `Documenter` bilan domen diagrammasini chiqaradi. Domen nomlarini mahsulot egasi bilan birga tanlash kitobda ham shunday ko'rsatilgan.

```java
@AnalyzeClasses(packages = "com.shop")
class DomainBoundaryTest {

    // Tasdiqlangan domenlar ro'yxati: yangi domen jim paydo bo'lmasin
    @ArchTest
    static final ArchRule faqat_tasdiqlangan_domenlar = classes()
            .should().resideInAnyPackage(
                    "com.shop.ticket..",
                    "com.shop.customer..",
                    "com.shop.reporting..",
                    "com.shop.admin..",
                    "com.shop.shared..");
}
```

**Qo'llanish keyslari:**
- Monolitdagi komponentlarni besh-olti domenga guruhlab, kelgusi servislar ro'yxatini shu guruhlardan olish.
- Nomi domenni aytmaydigan paketlarni (`shop.supportcontract`) domen tuguni ostiga ko'chirish.
- Login va notification kabi umumiy funksionallikni alohida `shared` domeniga yig'ish.
- Domen nomlarini mahsulot egasi bilan kelishib, keyin ularni build qoidasi bilan qotirish.
- Modular monolit sifatida to'xtash: domen chegarasi qotirilgan monolit o'zi ham yaroqli maqsad.

**Ehtiyot bo'ling:** Namespace ko'chirish arzon ko'rinadi, lekin u butun kod bazasiga tegadigan diff beradi: ochiq branch lar konfliktga uchraydi va review faktik o'zgarishni ko'rmaydi, shuning uchun ko'chirishni alohida commit va alohida relizda bajaring. Domen chizig'ini noto'g'ri tortish esa keyinchalik qimmat tushadi: bir domenga qo'yilgan ikki komponent bitta servisga tushib, ularni keyin ajratish kerak bo'lsa, ish qaytadan boshlanadi. Domen nomini texnik atama bilan (`service`, `manager`, `util`) belgilamang: domen biznes tilidan olinadi, aks holda guruhlash kodni emas, qatlamni takrorlaydi.

## 27.30 Domen servislarini yaratish (Create Domain Services)

**Tavsif:** Komponentlar o'lchangan, tekislangan va domenlarga guruhlangandan keyin har domen alohida deploy qilinadigan **domen servisi** ga chiqariladi va natijada service-based arxitektura paydo bo'ladi: foydalanuvchi interfeysi yirik donali domen servislariga masofadan murojaat qiladi, bazasi esa hozircha bitta qoladi. Bu mikroservislarga o'tishdan oldingi oraliq bosqich va kitob uni ataylab tavsiya qiladi: service-based arxitektura bazani bo'lishni talab qilmaydi, operatsion avtomatlashtirish va konteynerizatsiyani talab qilmaydi, har domen servisi monolitning o'sha deployment artefakti bilan chiqariladi, va o'tish texnik ish bo'lgani uchun tashkiliy tuzilishga tegmaydi. Shu bosqichda qaysi domen yana bo'linishi kerakligi va qaysi biri yirik qolishi mumkinligi ko'rinadi. Bitta qat'iy maslahat bor: hamma domen aniqlanib refaktoring qilinmaguncha bu patternni qo'llamang, aks holda chiqarilgan servis keyin yana o'zgartirilishi kerak bo'ladi.

**Spring'da qayerda uchraydi:** Har domen o'z Maven/Gradle moduliga va o'z `@SpringBootApplication` sinfiga chiqariladi; umumiy kod alohida kutubxona modulida qoladi. Baza umumiy bo'lgani uchun har servis bir xil `spring.datasource.url` ga ulanadi va sxema egaligi hozircha kelishuv darajasida ushlanadi; keyingi qadam [har bir bounded context uchun ma'lumotlar bazasi](#2717-har-bir-bounded-context-uchun-malumotlar-bazasi-database-per-bounded-context) bo'ladi. UI dan chaqiruv `RestClient` yoki `@HttpExchange` interfeys client orqali ketadi, oldiga Spring Cloud Gateway qo'yiladi. Flyway migratsiyalari bitta egaga qoldiriladi, aks holda ikki servis bir sxemani bir vaqtda o'zgartiradi.

```java
// Reporting domeni o'z deployment unit iga chiqdi
@SpringBootApplication
public class ReportingServiceApplication {

    public static void main(String[] args) {
        SpringApplication.run(ReportingServiceApplication.class, args);
    }
}

@AnalyzeClasses(packages = "com.shop")
class ReportingServiceBoundaryTest {

    // Domen servisi ichida faqat o'z domeni qolsin, aks holda u yangi monolitga aylanadi
    @ArchTest
    static final ArchRule faqat_reporting_domeni = classes()
            .should().resideInAPackage("com.shop.reporting..");
}
```

**Qo'llanish keyslari:**
- Hisobot domenini birinchi bo'lib chiqarish: u monolitni sekinlashtirayotgan bo'lsa, ajratish darhol foyda beradi.
- Service-based arxitekturada to'xtash: domen servislari yetarli bo'lsa, mikroservislarning narxini to'lash shart emas.
- Har domen servisini alohida kuzatib, qaysi biri [service granularligi qarori](14-microservices-patternlari.md#1439-service-granularligi-boyicha-qaror-service-granularity-decision) bo'yicha yana bo'linishi kerakligini aniqlash.
- Jamoalarni domen servislari bo'yicha taqsimlab, reliz bog'liqligini kamaytirish.
- Monolit deployment artefaktini saqlab qolib, faqat marshrutni o'zgartirish: UI chaqiruvi mahalliy metod o'rniga HTTP ga o'tadi.

**Ehtiyot bo'ling:** Domen servisining ichi nazoratsiz qolsa, u o'z navbatida kichik monolitga aylanadi: namespace qoidasini build da ushlab turish shuning uchun kerak. Mahalliy metod chaqiruvi tarmoq chaqiruviga aylangani uchun avval bitta tranzaksiyada bo'lgan ish endi bir necha servisga yoyiladi va timeout, retry hamda qisman nosozlik masalasi paydo bo'ladi: baza umumiy bo'lsa ham chaqiruv endi masofaviy. Bazani bo'lmaslik vaqtincha yengillik beradi, lekin umumiy sxema servislarni reliz darajasida bog'lab turadi: bu holat [monolit ma'lumotga kirish qatlami sifatida](#2718-monolit-malumotga-kirish-qatlami-sifatida-monolith-as-data-access-layer) patternidagi kamchilikni takrorlaydi, shuning uchun uni oraliq holat deb biling va muddat qo'ying.

## 27.31 Amalda qo'llash

- [ ] Monolitdagi modullarni o'zgarish zichligi va bog'liqlik soni bo'yicha jadvalga yozib, ajratish tartibini belgilang.
- [ ] Birinchi ajratiladigan modul uchun savolga javob yozing: uning ma'lumotlari boshqa modullar bilan JOIN qilinadimi.
- [ ] Strangler fig uchun marshrutlash nuqtasini belgilang va orqaga qaytish yo'lini yozib qo'ying.
- [ ] Branch by abstraction qo'llanadigan joylarda abstraksiya interfeysi va ikki implementatsiya mavjudligini tasdiqlang.
- [ ] Parallel run rejasini yozing: ikki yo'l natijasi qanday solishtiriladi va farq topilsa nima qilinadi.
- [ ] Ma'lumotlarni ajratish rejasini expand/contract bosqichlari bilan yozing; bitta relizda ikkisini qilmang.
- [ ] Har bir ajratilgan servis uchun chiqish mezonini yozing: qancha trafik o'tdi, qancha vaqt barqaror ishladi.
- [ ] Migratsiyani to'xtatish mezonini oldindan yozib qo'ying: qaysi belgilar ko'rilsa, ajratish to'xtatiladi.

## Manbalar

- Sam Newman, *Monolith to Microservices*, O'Reilly, 2019, 3-bob (79-82) - Strangler Fig Application: uch qadam, deploy va release tushunchalarini ajratish, har qadamning oson qaytarilishi va chuqur joylashgan funksionallikda ishlamasligi (27.1)
- Sam Newman, *Monolith to Microservices*, O'Reilly, 2019, 3-bob (86, 88) - marshrutni feature toggle bilan almashtirish, proxy nuqtasida canary rollout va parallel run, incremental rollout ning ma'nosi (27.22)
- Sam Newman, *Monolith to Microservices*, O'Reilly, 2019, 3-bob (98-104) - UI Composition: sahifa, vidjet va micro frontend kompozitsiyasi (27.2)
- Sam Newman, *Monolith to Microservices*, O'Reilly, 2019, 3-bob (104-112) - Branch by Abstraction: bir kod bazasida ikki implementatsiyaning birga yashashi, feature toggle bilan almashtirish va fallback mexanizmi (27.3)
- Sam Newman, *Monolith to Microservices*, O'Reilly, 2019, 3-bob (113-118) - Parallel Run: har so'rov uchun ikkala implementatsiyani chaqirish, nofunksional jihatlarni ham tekshirish, yon ta'sirni Spy bilan to'sish, GitHub Scientist; canary va dark launching dan farqi hamda progressive delivery (27.4, 27.22)
- Sam Newman, *Monolith to Microservices*, O'Reilly, 2019, 3-bob (118-120) - Decorating Collaborator: chaqiruv monolitga yetib boradi va proxy natijaga qarab ishlaydi; oddiy holatda Change Data Capture dan nafisroq va kamroq bog'langan, kerakli ma'lumot so'rov yoki javobda bo'lmasa esa ehtiyot bo'lish kerak (27.5)
- Sam Newman, *Monolith to Microservices*, O'Reilly, 2019, 3-bob (120-124) - Change Data Capture: baza trigger'i, transaction log poller va batch delta copier; patternning sweet spot i va qo'llanishni minimumda ushlash maslahati (27.6)
- Sam Newman, *Monolith to Microservices*, O'Reilly, 2019, 4-bob (125-127) - Shared Database: nima ochiq, nima yashirin ekanini tanlash imkoniyatidan voz kechish (27.18, 27.20)
- Sam Newman, *Monolith to Microservices*, O'Reilly, 2019, 4-bob (128-132) - Database View: view ma'lumot shartnomasi sifatida, read-only ekani, materialized view va staleness, manba bilan view bir baza dvigichida bo'lishi, view egaligi (27.7)
- Sam Newman, *Monolith to Microservices*, O'Reilly, 2019, 4-bob (132-134) - Database Wrapping Service: umumiy baza oldiga yupqa fasad qo'yib, baza bog'liqligini servis bog'liqligiga aylantirish (27.8)
- Sam Newman, *Monolith to Microservices*, O'Reilly, 2019, 4-bob (135-137) - Database-as-a-Service Interface: alohida read-only baza endpoint i, mapping engine va uning kechikishi, oddiy view dan farqi (27.9)
- Sam Newman, *Monolith to Microservices*, O'Reilly, 2019, 4-bob (138-141) - Aggregate Exposing Monolith: monolit agregat holati va holat o'tishlarini aniq interfeys orqali chiqaradi, bu keyingi servis chegarasini topish yo'li ham bo'ladi (27.10)
- Sam Newman, *Monolith to Microservices*, O'Reilly, 2019, 4-bob (141-143) - Change Data Ownership: ma'lumot yangi servisga ko'chadi va monolit uni haqiqat manbasi deb biladi; monolit faqat o'qisa view proyeksiyasi mumkin, lekin to'g'ridan-to'g'ri chaqiruv afzal (27.11)
- Sam Newman, *Monolith to Microservices*, O'Reilly, 2019, 4-bob (143-148) - Synchronize Data in Application: uch qadam (bulk sinxronizatsiya va CDC bilan yetib olish, yozuv ikkalasiga va o'qish eskidan, keyin o'qish yangidan) va patternning chegarasi: bitta ilova ikki sxemani ushlaganda ishlaydi, monolit bilan servis ikkisi ham yozsa juda murakkablashadi, canary da esa tavsiya etilmaydi (27.11, 27.12)
- Sam Newman, *Monolith to Microservices*, O'Reilly, 2019, 4-bob (149-158) - Tracer Write: haqiqat manbasini bosqichma-bosqich ko'chirish, sinxronizatsiyaning uch varianti va ikki tomonlama sinxronizatsiyadan qochish, reconciliation jarayonining majburiyligi, Square dagi Order misoli (27.13)
- Sam Newman, *Monolith to Microservices*, O'Reilly, 2019, 4-bob (162-163) - Repository per Bounded Context: data access kodini bounded context bo'yicha bo'lish; baza darajasidagi constraint larni ko'rish uchun sxemani vizuallashtiradigan alohida vosita kerakligi (27.16)
- Sam Newman, *Monolith to Microservices*, O'Reilly, 2019, 4-bob (163-165) - Database per Bounded Context: bitta deployment unit ichida alohida bazalar, yillar davomida shundayligicha qolgan modular monolit misoli, yangi tizimlar uchun tavsiya (27.17)
- Sam Newman, *Monolith to Microservices*, O'Reilly, 2019, 4-bob (166-167) - Monolith as Data Access Layer: monolitda API yaratib, unga murojaat qilish; holat o'tishlari monolitda qolganda mos, ma'lumot servisga tegishli bo'lsa bu patterndan o'tib ketish kerak (27.18)
- Sam Newman, *Monolith to Microservices*, O'Reilly, 2019, 4-bob (168-169) - Multischema Storage: yangi funksionallikning yangi ma'lumotini o'z sxemasiga qo'yish, eski ma'lumotni monolit bazasidan o'qishda davom etish va jadval-jadval ko'chirish (27.19)
- Sam Newman, *Monolith to Microservices*, O'Reilly, 2019, 4-bob (171-173) - Split Table: jadvalni bounded context chizig'i bo'yicha bo'lish, bitta ustunni bir necha kod o'zgartirsa egalikni tanlash, baza tranzaksiyasi himoyasining yo'qolishi (27.14)
- Sam Newman, *Monolith to Microservices*, O'Reilly, 2019, 4-bob (173-178) - Move Foreign-Key Relationship to Code: JOIN ni servis chaqiruviga aylantirish, latency ning oshishi va bulk lookup bilan kesh, o'chirishni nazokat bilan boshqarish, o'chirishdan oldin tekshirishning xatoligi, agregatni bo'lib tashlamaslik (27.15)
- Sam Newman, *Monolith to Microservices*, O'Reilly, 2019, 4-bob (178-180) - Example: Shared Static Data (bu bo'lim sarlavhasi, pattern nomi emas) va Pattern: duplicate static reference data: nusxalash qachon muammo emas va qachon xavfli (27.20)
- Neal Ford, Mark Richards, Pramod Sadalage, Zhamak Dehghani, *Software Architecture: The Hard Parts*, 1-nashr, O'Reilly, 2021 (copyright 2022), 4-bob (63-64-betlar) - dekompozitsiyaning ikki yondashuvi (komponentga asoslangan va taktik ayirish) va "elephant migration" anti-patterni; tanlov kodning ichki tuzilishiga bog'liqligi (27.23)
- Neal Ford, Mark Richards, Pramod Sadalage, Zhamak Dehghani, *Software Architecture: The Hard Parts*, 1-nashr, O'Reilly, 2021 (copyright 2022), 4-bob (65-70-betlar) - kod bazasi bo'linadimi degan savol, afferent va efferent coupling, abstractness va instability formulalari, asosiy ketma-ketlikdan masofa, foydasizlik va og'riq zonalari (27.23)
- Neal Ford, Mark Richards, Pramod Sadalage, Zhamak Dehghani, *Software Architecture: The Hard Parts*, 1-nashr, O'Reilly, 2021 (copyright 2022), 4-bob (71-72-betlar) - komponent ta'rifi (namespace va papka bilan belgilangan qurilish bloki), servis sinflardan emas komponentlardan yasalishi, service-based arxitektura oraliq bosqich sifatida (27.23, 27.30)
- Neal Ford, Mark Richards, Pramod Sadalage, Zhamak Dehghani, *Software Architecture: The Hard Parts*, 1-nashr, O'Reilly, 2021 (copyright 2022), 4-bob (73-78-betlar) - Tactical Forking: nomni Fausto De La Torre bergani, chiqarish o'rniga o'chirish, monolitni nusxalab har jamoaga berish, trade-off lari (qoldiq kod, kod sifati o'zgarmasligi, umumiy kodda nom farqlari) (27.24)
- Neal Ford, Mark Richards, Pramod Sadalage, Zhamak Dehghani, *Software Architecture: The Hard Parts*, 1-nashr, O'Reilly, 2021 (copyright 2022), 5-bob (81-83-betlar) - oltita komponentga asoslangan dekompozitsiya patterni ro'yxati va tartibi, har patternning uch qismi, arxitektura story si tushunchasi (27.23, 27.25-27.30)
- Neal Ford, Mark Richards, Pramod Sadalage, Zhamak Dehghani, *Software Architecture: The Hard Parts*, 1-nashr, O'Reilly, 2021 (copyright 2022), 5-bob (84-89-betlar) - Identify and Size Components: gaplar soni o'lcham mezoni sifatida, o'rtachadan bir-ikki standart og'ish qoidasi, komponent inventari va standart og'ish fitness function lari (27.25)
- Neal Ford, Mark Richards, Pramod Sadalage, Zhamak Dehghani, *Software Architecture: The Hard Parts*, 1-nashr, O'Reilly, 2021 (copyright 2022), 5-bob (94-97-betlar) - Gather Common Domain Components: umumiy domen va umumiy infratuzilma funksionalligi farqi, audit namespace lari misoli, umumiy servis yoki umumiy kutubxona tanlovi, namespace oxirgi tuguni va umumiy kod bo'yicha fitness function lar (27.26)
- Neal Ford, Mark Richards, Pramod Sadalage, Zhamak Dehghani, *Software Architecture: The Hard Parts*, 1-nashr, O'Reilly, 2021 (copyright 2022), 5-bob (101-107-betlar) - Flatten Components: komponent namespace ning oxirgi tuguni ekani, root namespace va orphaned class ta'riflari, tekislashning ikki yo'li va root namespace da kod bo'lmasligi fitness function i (27.27)
- Neal Ford, Mark Richards, Pramod Sadalage, Zhamak Dehghani, *Software Architecture: The Hard Parts*, 1-nashr, O'Reilly, 2021 (copyright 2022), 5-bob (111-117-betlar) - Determine Component Dependencies: migratsiya haqidagi uch savol, komponentlar orasidagi (sinflar orasidagi emas) bog'liqlik, CA, CE va CT, komponentni bo'lib afferent coupling ni tushirish, bog'liqlik chegarasi fitness function i (27.28)
- Neal Ford, Mark Richards, Pramod Sadalage, Zhamak Dehghani, *Software Architecture: The Hard Parts*, 1-nashr, O'Reilly, 2021 (copyright 2022), 5-bob (120-122-betlar) - Create Component Domains: servis va komponent orasidagi bir-ga-ko'p munosabat, domen, subdomain va komponentning namespace tugunlari bilan ifodalanishi, namespace refaktoringi va tasdiqlangan domenlar ro'yxatini ArchUnit bilan ushlash (27.29)
- Neal Ford, Mark Richards, Pramod Sadalage, Zhamak Dehghani, *Software Architecture: The Hard Parts*, 1-nashr, O'Reilly, 2021 (copyright 2022), 5-bob (126-129-betlar) - Create Domain Services: domen servisi ta'rifi, service-based arxitekturaning asosiy topologiyasi, hamma domen refaktoring qilinmaguncha patternni qo'llamaslik maslahati, domen ichida namespace birligi fitness function i (27.30)
- Sam Newman, *Monolith to Microservices*, O'Reilly, 2019, 4-bob (181) - Pattern: Dedicated reference data schema: alohida sxema, shared database muammolarining saqlanishi, sxemani versiyalangan servis interfeysi deb boshqarish, cross-schema JOIN uchun bir xil baza dvigichi sharti (27.21)
- Sam Newman, *Monolith to Microservices*, O'Reilly, 2019, 4-bob (182-186) - Pattern: Static reference data library va Pattern: Static reference data service: ISO 3166-1 da 249 davlat, kutubxona versiyalarining farqi va lockstep release xavfi, servis variantining narxi va muallifning yakuniy tanlovi (27.20)
- Sam Newman, *Building Microservices*, 2-nashr, O'Reilly, 2021, 5-bob - expand and contract: buzadigan o'zgarishni bosqichga ajratish, eski va yangi usulni birga qo'llab-quvvatlab, keyin eskisini olib tashlash (27.22). Bu nashrning qo'limizdagi elektron nusxasida barqaror bet raqami yo'q, shuning uchun faqat bob ko'rsatilgan
- ESLATMA: barcha bo'limlardagi Spring va Java vositalari (Spring Cloud Gateway, Spring Modulith, Togglz, Debezium, Flyway, Liquibase, Spring Batch, Resilience4j, Testcontainers va boshqalar) shu korpusning amaliy qo'shimchasi - yuqoridagi kitoblar Spring nomidan gapirmaydi
- ESLATMA: 27.6 dagi CDC ni oxir-oqibat transactional outbox shartnomasiga almashtirish tavsiyasi shu korpusning amaliy tavsiyasi, kitobdan olingan emas
- ESLATMA: 27.21 dagi read-only baza useri va grant bilan intizomni majburlash tavsiyasi shu korpusning amaliy tavsiyasi, kitobdan olingan emas
- ESLATMA: 27.20 va 27.22 sarlavhalari tuzatildi. Ilgari ularda kitobda bo'lmagan nomlar turgan edi: "Shared Static Data" aslida 4-bobdagi misol sarlavhasi (178-bet), "Incremental Rollout & Rollback of a Migration" esa kitobda umuman uchramaydi. Endi 27.20 sarlavhasida haqiqiy pattern nomi (Duplicate Static Reference Data) turadi, qolgan ikki nom bo'lim tanasida va alifbo indeksida ko'rsatilgan; 27.22 sarlavhasidan esa inglizcha nom olib tashlandi
- ESLATMA: 27.31 dagi nazorat ro'yxati shu korpusning amaliy ro'yxati, kitobdan olingan emas

---

[&larr; 26. Dizayn printsiplari: SOLID, GRASP va umumiy qoidalar](26-dizayn-printsiplari-solid-grasp-va-umumiy.md) · [Mundarija](README.md) · [28. Taqsimlangan ma'lumot, replikatsiya va konsistentlik patternlari &rarr;](28-taqsimlangan-malumot-replikatsiya-va.md)
