<!-- doc: patterns | chapter: 14 | part:  -->

[Java Spring arxitektori bilishi kerak bo'lgan barcha dizayn patternlar](../../README.md) / [Dizayn patternlar](README.md)

# 14. Microservices patternlari (Microservices Patterns)

<details>
<summary>Bu bo'limdagi 39 bo'lim</summary>

- [14.1 Monolitik arxitektura va mikroservis arxitekturasi qarori (Monolithic Architecture vs Microservice Architecture (decision))](#141-monolitik-arxitektura-va-mikroservis-arxitekturasi-qarori-monolithic-architecture-vs-microservice-architecture-decision)
- [14.2 Biznes imkoniyati bo'yicha dekompozitsiya (Decompose by Business Capability)](#142-biznes-imkoniyati-boyicha-dekompozitsiya-decompose-by-business-capability)
- [14.3 Subdomen bo'yicha dekompozitsiya (Decompose by Subdomain)](#143-subdomen-boyicha-dekompozitsiya-decompose-by-subdomain)
- [14.4 O'zi-yetarli servis (Self-Contained Service)](#144-ozi-yetarli-servis-self-contained-service)
- [14.5 Har bir jamoaga bitta servis (Service per Team)](#145-har-bir-jamoaga-bitta-servis-service-per-team)
- [14.6 Strangler Fig (Strangler Fig)](#146-strangler-fig-strangler-fig)
- [14.7 Har bir servisga alohida ma'lumotlar bazasi (Database per Service (microservice view))](#147-har-bir-servisga-alohida-malumotlar-bazasi-database-per-service-microservice-view)
- [14.8 Saga (xoreografiya) (Saga (choreography))](#148-saga-xoreografiya-saga-choreography)
- [14.9 Saga (orkestratsiya) (Saga (orchestration))](#149-saga-orkestratsiya-saga-orchestration)
- [14.10 API kompozitsiyasi (API Composition)](#1410-api-kompozitsiyasi-api-composition)
- [14.11 Domen hodisasi (Domain Event (microservice view))](#1411-domen-hodisasi-domain-event-microservice-view)
- [14.12 Tranzaksion Outbox (Transactional Outbox (microservice view))](#1412-tranzaksion-outbox-transactional-outbox-microservice-view)
- [14.13 Tranzaksiya logini kuzatish (Transaction Log Tailing)](#1413-tranzaksiya-logini-kuzatish-transaction-log-tailing)
- [14.14 Polling Publisher (Polling Publisher)](#1414-polling-publisher-polling-publisher)
- [14.15 Masofaviy protsedura chaqirig'i (Remote Procedure Invocation)](#1415-masofaviy-protsedura-chaqirigi-remote-procedure-invocation)
- [14.16 Xabar almashish (Messaging)](#1416-xabar-almashish-messaging)
- [14.17 Domenga xos protokol (Domain-Specific Protocol)](#1417-domenga-xos-protokol-domain-specific-protocol)
- [14.18 Idempotent iste'molchi (Idempotent Consumer)](#1418-idempotent-istemolchi-idempotent-consumer)
- [14.19 Klient tomonda aniqlash (Client-Side Discovery)](#1419-klient-tomonda-aniqlash-client-side-discovery)
- [14.20 Server tomonda aniqlash (Server-Side Discovery)](#1420-server-tomonda-aniqlash-server-side-discovery)
- [14.21 Servis reyestri (Service Registry)](#1421-servis-reyestri-service-registry)
- [14.22 O'z-o'zini ro'yxatga olish (Self Registration)](#1422-oz-ozini-royxatga-olish-self-registration)
- [14.23 Uchinchi tomon orqali ro'yxatga olish (3rd Party Registration)](#1423-uchinchi-tomon-orqali-royxatga-olish-3rd-party-registration)
- [14.24 Access token (Access Token)](#1424-access-token-access-token)
- [14.25 Server tomonda sahifa fragmentini kompozitsiya qilish (Server-Side Page Fragment Composition)](#1425-server-tomonda-sahifa-fragmentini-kompozitsiya-qilish-server-side-page-fragment-composition)
- [14.26 Klient tomonda UI kompozitsiyasi (Client-Side UI Composition)](#1426-klient-tomonda-ui-kompozitsiyasi-client-side-ui-composition)
- [14.27 API Gateway (API Gateway)](#1427-api-gateway-api-gateway)
- [14.28 Frontend uchun Backend (Backend for Frontend)](#1428-frontend-uchun-backend-backend-for-frontend)
- [14.29 Microservice Shassi (Microservice Chassis)](#1429-microservice-shassi-microservice-chassis)
- [14.30 Tashqariga chiqarilgan konfiguratsiya (Externalized Configuration)](#1430-tashqariga-chiqarilgan-konfiguratsiya-externalized-configuration)
- [14.31 Service Shabloni (Service Template)](#1431-service-shabloni-service-template)
- [14.32 Sidecar (Sidecar)](#1432-sidecar-sidecar)
- [14.33 Ambassador (Ambassador)](#1433-ambassador-ambassador)
- [14.34 Service Mesh (Service Mesh)](#1434-service-mesh-service-mesh)
- [14.35 Aggregator, Proxy, Chained va Branch microservice patternlari (Aggregator / Proxy / Chained / Branch Microservice Patterns)](#1435-aggregator-proxy-chained-va-branch-microservice-patternlari-aggregator--proxy--chained--branch-microservice-patterns)
- [14.36 Shared Library bog'liqligi (Shared Library Coupling) - antipattern](#1436-shared-library-bogliqligi-shared-library-coupling---antipattern)
- [14.37 Taqsimlangan monolit (Distributed Monolith) - antipattern](#1437-taqsimlangan-monolit-distributed-monolith---antipattern)
- [14.38 Nano-service'lar (Nano-services) - antipattern](#1438-nano-servicelar-nano-services---antipattern)
- [14.39 Service granularligi bo'yicha qaror (Service Granularity Decision)](#1439-service-granularligi-boyicha-qaror-service-granularity-decision)

</details>



Mikroservis patternlari - bu bitta deployment birligiga sig'maydigan tizimni mustaqil ishlab chiqiladigan, mustaqil deploy qilinadigan va mustaqil masshtablanadigan servislarga bo'lish hamda ularni bir-biri bilan ishonchli bog'lash bo'yicha takrorlanuvchi yechimlar to'plami. Monolitda bitta `@Transactional` metod va bitta ma'lumotlar bazasi hal qilgan muammolar (atomarlik, join'lar, refactoring) tarqatilgan tizimda tamomila boshqa narxga ega bo'ladi - shuning uchun arxitektor uchun bu patternlar "moda" emas, balki tanlov narxini ongli boshqarish vositasi. Bu bo'limdagi patternlar uch guruhga bo'linadi: dekompozitsiya (qanday bo'lish kerak), ma'lumotlar izchilligi (saga, outbox, event'lar) va so'rovlarni birlashtirish (API composition). Spring ekotizimida bu patternlarning deyarli har biri uchun tayyor modul bor - Spring Boot 3.x/4.x, Spring Cloud, Spring Modulith, Spring for Apache Kafka - lekin pattern tanlashdagi xatoni hech qanday kutubxona tuzatib bermaydi.

## 14.1 Monolitik arxitektura va mikroservis arxitekturasi qarori (Monolithic Architecture vs Microservice Architecture (decision))

**Tavsif:** Bu pattern emas, balki boshlang'ich arxitektura qarori: tizim bitta deployment birligi bo'lib qoladimi yoki mustaqil deploy qilinadigan servislarga bo'linadimi. Monolit oddiy: bitta build, bitta tranzaksiya, bitta ma'lumotlar bazasi, refactoring kompilyator yordamida amalga oshadi; lekin jamoa va kod bazasi o'sgach, release'lar bir-birini bloklay boshlaydi va modullar orasidagi chegaralar yemiriladi. Mikroservislar mustaqil release, texnologiya tanlash erkinligi va alohida masshtablash beradi, biroq tarmoq, eventual consistency, tarqatilgan tracing va infratuzilma narxini qo'shadi. Amaliy javob ko'pincha "modular monolit" dan boshlash va chegaralar barqarorlashgach ajratishdir.

**Spring'da qayerda uchraydi:** Monolit tomoni - bitta Spring Boot 3.x ilovasi, `spring-boot-starter-web`, Spring Data JPA va `@Transactional`. Modular monolit uchun Spring Modulith: `@ApplicationModule`, `ApplicationModules.of(App.class).verify()` testda modul chegaralarini buzilishidan saqlaydi, `@ApplicationModuleListener` modullar orasini event bilan bo'shashtiradi, `spring-modulith-starter-jpa` va `spring-modulith-docs` hujjat/diagramma chiqaradi. Mikroservis tomoni - ko'p Spring Boot ilovasi, Spring Cloud Gateway, Spring Cloud Config, Spring Cloud OpenFeign yoki `RestClient`, Micrometer Tracing va `spring-boot-starter-actuator`. `spring.threads.virtual.enabled=true` (Java 21+) I/O ga bog'liq servislarda thread narxini sezilarli kamaytiradi.

**Qo'llanish keyslari:**
- Startap MVP: bitta Spring Boot monolit, lekin Spring Modulith bilan modul chegaralari testdan o'tkaziladi.
- 50+ injener va kuniga bir necha release kerak bo'lgan to'lov platformasi mikroservislarga ajratiladi.
- Hisobot va ML inference qismi asosiy ilovadan 10 barobar ko'proq CPU talab qilsa, faqat shu qism alohida servis qilinadi.
- Legacy monolitni butunlay yozmasdan, eng tez o'zgaradigan domen (masalan, narxlash) birinchi mikroservis sifatida ajratiladi.
- Regulyator talabi bilan kartalar ma'lumoti alohida compliance zonasida ishlashi kerak bo'lgan tizim.

**Ehtiyot bo'ling:** Domen chegaralari hali aniq bo'lmaganda mikroservislarga bo'lish eng qimmat xato - har bir refactoring API versiyalash, migratsiya va koordinatsiyaga aylanadi ("distributed monolith"). Jamoa CI/CD, observability va on-call madaniyatiga tayyor bo'lmasa, mikroservislar tezlikni oshirmaydi, balki kamaytiradi.

## 14.2 Biznes imkoniyati bo'yicha dekompozitsiya (Decompose by Business Capability)

**Tavsif:** Servislar texnik qatlamlar (UI, service, DAO) emas, balki biznes nima qila oladigani - "imkoniyat" bo'yicha ajratiladi: Order Management, Inventory, Payment, Shipping, Pricing. Har bir imkoniyat o'z ma'lumotlari, qoidalari va API'siga ega bo'ladi va odatda biznesdagi muayyan bo'linmaga mos tushadi. Natijada o'zgarish bitta biznes talabidan bitta servisga tushadi, ya'ni "bitta feature - bitta deploy" prinsipi ishlaydi. Manba sifatida kompaniyaning biznes-imkoniyatlar xaritasi (capability map) ishlatiladi.

**Spring'da qayerda uchraydi:** Har bir imkoniyat - alohida Spring Boot 3.x ilovasi yoki Spring Modulith moduli (`package order`, `@ApplicationModule(allowedDependencies = "shared")`). Maven/Gradle multi-module loyihada `order-service`, `inventory-service`, `payment-service` modullari; umumiy DTO'lar uchun alohida `*-api` moduli. Servislararo shartnomalar Spring Cloud Contract (`spring-cloud-starter-contract-verifier`) yoki OpenAPI (`springdoc-openapi-starter-webmvc-ui`) bilan qotiriladi. Chaqiruvlar uchun `@HttpExchange` + `HttpServiceProxyFactory` (Spring Framework 6.1+) yoki `@FeignClient`.

**Qo'llanish keyslari:**
- E-commerce platformasi Catalog, Cart, Order, Payment, Shipping imkoniyatlariga bo'linadi.
- Bankda Account, Card Issuing, Credit Scoring, Statement alohida servislar bo'ladi.
- Logistika tizimida Fleet Management va Route Planning har xil tezlikda o'zgarganligi uchun ajratiladi.
- Marketplace'da Seller Onboarding alohida servis - unga faqat compliance jamoasi tegadi.
- Sug'urta tizimida Policy Administration va Claims Processing mustaqil release tsikliga ega bo'ladi.

**Ehtiyot bo'ling:** Imkoniyatlar ro'yxatini tashkiliy struktura bo'yicha emas, balki haqiqiy biznes funksiyasi bo'yicha tuzing - aks holda kompaniya reorganizatsiya qilinganda arxitektura yaroqsiz bo'lib qoladi. Juda mayda imkoniyatlar (masalan, "EmailSender service") mustaqil biznes qiymatiga ega bo'lmagani uchun faqat operatsion yukni oshiradi.

## 14.3 Subdomen bo'yicha dekompozitsiya (Decompose by Subdomain)

**Tavsif:** DDD yondashuvi: domen subdomenlarga (core, supporting, generic) bo'linadi va har bir bounded context bitta servisga aylanadi. Chegara modeldagi til (ubiquitous language) o'zgargan joyda o'tadi - masalan, "Order" so'zi Sales contextida mijoz buyurtmasi, Warehouse contextida esa yig'ish topshirig'i. Bu dekompozitsiya biznes imkoniyatiga yaqin, lekin model izchilligiga, aggregate'lar va context map'ga tayanadi. Natijada har bir servis o'z ichida yaxlit va tashqariga minimal til orqali bog'lanadi.

**Spring'da qayerda uchraydi:** Aggregate'lar Spring Data JPA entity'lari (`@Entity`, `@Version` optimistic locking uchun) yoki Spring Data MongoDB `@Document` sifatida modellashtiriladi; repository interfeysi `CrudRepository`/`JpaRepository` aggregate root uchun bittadan bo'ladi. Spring Modulith `@ApplicationModule` va `ApplicationModules.verify()` bounded context chegarasini kompilyatsiya/test darajasida himoya qiladi; `@ApplicationModuleTest` faqat bitta contextni ko'taradi. Context'lar orasida tarjima (ACL) uchun alohida `*Adapter`/`*Translator` `@Component` sinflari va Spring Cloud Stream `@Bean Function<...>` converterlari ishlatiladi. Event storming natijasi `@DomainEvents` (Spring Data `AbstractAggregateRoot`) yoki `ApplicationEventPublisher` ga tushadi.

**Qo'llanish keyslari:**
- Sug'urta tizimida Underwriting, Policy, Claims uchta bounded context sifatida ajratiladi.
- Telekomda Billing va Charging bir xil "subscriber" so'zini boshqa ma'noda ishlatgani uchun alohida servis bo'ladi.
- Sog'liq tizimida Patient Records (core) va Notification (generic) subdomenlari turlicha investitsiya oladi.
- HR platformasida Recruiting va Payroll alohida model va alohida ma'lumotlar bazasiga ega.
- Logistikada "Shipment" tushunchasi Sales va Customs contextlarida farq qilgani uchun tarjima qatlami qo'yiladi.

**Ehtiyot bo'ling:** Umumiy "canonical data model" yaratishga urinish bounded context g'oyasini buzadi va barcha servislarni bitta sxemaga bog'lab qo'yadi. Shuningdek, generic subdomenlarni (auth, notification, file storage) o'zingiz yozishdan oldin tayyor yechimni ko'rib chiqing - core domenga vaqt yetmay qoladi.

## 14.4 O'zi-yetarli servis (Self-Contained Service)

**Tavsif:** Servis sinxron so'rovni boshqa servislarga murojaat qilmasdan bajara olishi kerak: kerakli tashqi ma'lumotning replikasini oldindan event orqali olib, lokal saqlaydi. Masalan, Order Service mijoz kredit limitini Customer Service'dan so'ramasdan, o'zida saqlangan limit nusxasidan foydalanib buyurtmani qabul qiladi. Bu availability'ni oshiradi (bog'liq servis o'chsa ham ishlaydi) va latency zanjirini qisqartiradi, lekin ma'lumot eventual consistent bo'ladi. Amalda bu CQRS read model'ning servis ichidagi ko'rinishi.

**Spring'da qayerda uchraydi:** Replikatsiya uchun Spring for Apache Kafka (`@KafkaListener`, `KafkaTemplate`) yoki Spring Cloud Stream (`spring-cloud-stream-binder-kafka`, `Consumer<Message<...>>` bean'i) bilan hodisalar iste'mol qilinadi va lokal jadvalga yoziladi (Spring Data JPA yoki Redis orqali `spring-boot-starter-data-redis`). Idempotentlik uchun `@KafkaListener` ichida processed-id jadvali yoki `ConsumerRecord` offset/key'i ishlatiladi. Lokal cache variantida `@Cacheable` va Caffeine (`spring-boot-starter-cache`), lekin TTL va invalidatsiya event bilan boshqariladi. Kafka Streams integratsiyasi uchun `spring-kafka` ning `StreamsBuilderFactoryBean` va `@EnableKafkaStreams`.

**Qo'llanish keyslari:**
- Order Service mijoz statusi va kredit limitini lokal replikada saqlab, Customer Service o'chganda ham buyurtma qabul qiladi.
- Narxlash servisi valyuta kurslarini event orqali oladi va har bir hisob-kitobda tashqi API chaqirmaydi.
- Shipping Service mahsulot o'lchamlari nusxasini saqlab, Catalog'ga bog'liqlikni yo'qotadi.
- Fraud detection servisi mijoz profilining denormalizatsiyalangan nusxasida millisekundlarda qaror qabul qiladi.
- Mobil BFF servisi feature-flag va konfiguratsiya nusxasini lokal ushlab turadi.

**Ehtiyot bo'ling:** Replika eskirgan bo'lishi mumkin - pul yoki huquqiy oqibatli qarorlar (masalan, oxirgi qoldiqni yechish) uchun eskirish oynasi qabul qilinadimi, buni biznes bilan aniq kelishib oling. Har bir servisga hamma narsani replikatsiya qilish esa ma'lumotlar egaligini xiralashtiradi va storage/izchillik narxini portlatadi.

## 14.5 Har bir jamoaga bitta servis (Service per Team)

**Tavsif:** Servis chegarasi jamoa chegarasiga mos qilinadi: bitta jamoa servisni to'liq egalik qiladi - kod, ma'lumotlar bazasi, deploy, on-call va SLA. Bu Conway qonunini ongli boshqarish usuli: koordinatsiya narxi eng qimmat resurs bo'lgani uchun, servislar jamoalar mustaqil release qila oladigan tarzda chizilaadi. Bitta jamoa bir nechta servisga egalik qilishi mumkin, lekin bitta servisga ikki jamoa egalik qilmasligi kerak.

**Spring'da qayerda uchraydi:** Har bir jamoa alohida repozitoriya va alohida Spring Boot 3.x/4.x ilovasini yuritadi; umumiy standart `spring-boot-starter-parent` yoki ichki "platform BOM" va kompaniya ichidagi custom starter (`*-spring-boot-starter` + `@AutoConfiguration`, `META-INF/spring/org.springframework.boot.autoconfigure.AutoConfiguration.imports`) orqali tarqatiladi. Jamoalararo API shartnomasi Spring Cloud Contract (`Contract.make { ... }`, `@AutoConfigureStubRunner`) va OpenAPI bilan mustahkamlanadi. Servis egaligi metadata'si `spring-boot-starter-actuator` ning `/actuator/info` va `build-info`/`git-info` orqali ko'rsatiladi; integratsiya testlari Testcontainers va `@ServiceConnection` bilan jamoa ichida mustaqil ishlaydi.

**Qo'llanish keyslari:**
- Payments jamoasi payment-service va payment-webhook-service'ni to'liq o'zi deploy qiladi.
- Platform jamoasi umumiy auth starter'ini yozadi, lekin biznes servislarga tegmaydi.
- Yangi jamoa qo'shilganda unga aniq bounded context va alohida servis beriladi.
- On-call rotatsiyasi servis bo'yicha tuziladi - alert to'g'ridan-to'g'ri egasiga boradi.
- Release train'dan voz kechib, har bir jamoa kuniga mustaqil deploy qila boshlaydi.

**Ehtiyot bo'ling:** Reorganizatsiyada jamoalar o'zgaradi, servis chegarasi esa oson o'zgarmaydi - shuning uchun jamoa strukturasini domen chegarasiga moslashtirish, teskarisi emas, to'g'ri yo'l. "Hamma hamma joyni o'zgartira oladi" degan madaniyatda bu pattern faqat qog'ozda qoladi va egasiz servislar paydo bo'ladi.

## 14.6 Strangler Fig (Strangler Fig)

**Tavsif:** Legacy monolitni bir zarbada qayta yozmasdan, uning atrofida yangi servislar o'stirib, funksiyalarni asta-sekin "bo'g'ib" ko'chirish strategiyasi. Oldiga proxy/gateway qo'yiladi: ko'chirilgan marshrutlar yangi servisga, qolganlari monolitga yo'naltiriladi; har bir qadamda rollback imkoniyati saqlanadi. Ma'lumotlar vaqtincha ikki tomonda sinxronlanadi (event yoki CDC bilan), monolitdagi kod oxirida o'chiriladi. Asosiy qiymati - risk kichik bo'laklarga bo'linadi va biznes ishlab turadi.

**Spring'da qayerda uchraydi:** Fasad sifatida Spring Cloud Gateway (`spring-cloud-starter-gateway` yoki Boot 3.x+ uchun `spring-cloud-starter-gateway-mvc`), `RouteLocatorBuilder` bilan `Predicates.path("/orders/**")` → yangi servis, qolgani monolitga; `RewritePath`, `CircuitBreaker` va `Retry` filtrlari migratsiyani xavfsizlashtiradi. Trafikni bosqichma-bosqich o'tkazish uchun `Weight` predicate yoki feature flag (Togglz/Unleash) ishlatiladi; monolit ichida esa `@RestController` metodini yangi servisga `RestClient`/`@FeignClient` orqali delegatsiya qiladigan adapter yoziladi. Ma'lumot sinxronizatsiyasi Debezium CDC yoki Transactional Outbox + Kafka bilan bajariladi. Monolitni avval Spring Modulith bilan modullashtirish ajratishni ancha osonlashtiradi.

**Qo'llanish keyslari:**
- 15 yillik Java EE monolitidan autentifikatsiya qismi birinchi bo'lib yangi Spring Boot servisiga ko'chiriladi.
- E-commerce'da faqat `/search` marshruti yangi servisga o'tkaziladi va natija A/B solishtiriladi.
- Hisobot va eksport funksiyalari monolitdan ajratilib, DB replikasidan o'qiydigan servisga olinadi.
- Mijozlar kabineti yangi frontend + BFF orqali ishlaydi, admin panel monolitda qoladi.
- Mintaqa bo'yicha migratsiya: avval bitta davlat trafigi yangi servisga yo'naltiriladi.

**Ehtiyot bo'ling:** Eng katta xato - migratsiyani oxirigacha yetkazmaslik: proxy, ikki ma'lumot manbasi va sinxronizatsiya kodi yillarga qolib, murakkablik ikki barobar bo'ladi. Har bir qadamga aniq "monolitdagi kod o'chirildi" mezonini va muddatni yozib qo'ying.

## 14.7 Har bir servisga alohida ma'lumotlar bazasi (Database per Service (microservice view))

**Tavsif:** Har bir servis o'z ma'lumotlarini xususiy bazada (yoki kamida xususiy sxemada) saqlaydi va boshqa servislar unga faqat API/event orqali kiradi. Bu loose coupling'ni ta'minlaydi: sxemani o'zgartirish boshqa jamoalarni buzmaydi va har bir servis o'ziga mos ma'lumot modelini (RDBMS, document, graph) tanlashi mumkin. Narxi - cross-service join va distributed tranzaksiya yo'q, ularning o'rniga API composition, CQRS va saga keladi.

**Spring'da qayerda uchraydi:** Har bir Spring Boot servisi o'z `spring.datasource.url` va o'z Flyway/Liquibase migratsiyalariga ega (`spring-boot-starter-data-jpa` + `flyway-core`, `db/migration` har bir servisda alohida). Polyglot persistence uchun `spring-boot-starter-data-mongodb`, `spring-boot-starter-data-redis`, `spring-boot-starter-data-elasticsearch`. Testlarda Testcontainers va `@ServiceConnection` har bir servis bazasini izolyatsiya qiladi. Agar bitta DB instansi ichida sxema bo'yicha ajratilsa - `spring.jpa.properties.hibernate.default_schema` va alohida DB foydalanuvchisi/grant'lar ishlatiladi.

**Qo'llanish keyslari:**
- Order Service PostgreSQL'da, Catalog Service Elasticsearch'da ishlaydi.
- Session va rate-limit ma'lumotlari uchun alohida Redis instansi faqat gateway servisiga tegishli bo'ladi.
- Payment Service bazasiga PCI talablari bo'yicha alohida tarmoq va kalit boshqaruvi qo'llanadi.
- Analitika uchun har bir servis o'z event'larini chiqaradi, DWH esa ularni yig'adi - hech kim boshqa servis jadvalini o'qimaydi.
- Monolitdan ajratishda avval sxema ajratiladi (grant olib tashlanadi), keyin alohida instansga ko'chiriladi.

**Ehtiyot bo'ling:** "Shared database" ga qaytish eng keng tarqalgan regress - hisobot uchun bo'lsa ham boshqa servis jadvaliga to'g'ridan-to'g'ri SELECT qilish chegarani yo'q qiladi. Shuningdek, cross-service `@Transactional` ishlamaydi: XA/2PC ni tiklashga urinmasdan, saga yoki outbox patternini loyihalashtiring.

## 14.8 Saga (xoreografiya) (Saga (choreography))

**Tavsif:** Bir nechta servisni qamragan biznes tranzaksiya lokal tranzaksiyalar ketma-ketligi sifatida bajariladi va har bir qadam natijasini event ko'rinishida e'lon qiladi; keyingi servis shu eventga reaksiya qilib o'z qadamini bajaradi. Markazlashgan koordinator yo'q - mantiq ishtirokchilar orasida tarqalgan. Xato bo'lsa, kompensatsion event'lar (masalan, `OrderRejected`, `InventoryReleased`) teskari yo'nalishda effektni bekor qiladi. Oddiy, 2-4 qadamli oqimlar uchun eng yengil yechim.

**Spring'da qayerda uchraydi:** Event transporti - Spring for Apache Kafka (`KafkaTemplate`, `@KafkaListener`, xatolar uchun `DefaultErrorHandler` + `DeadLetterPublishingRecoverer`) yoki Spring AMQP (`RabbitTemplate`, `@RabbitListener`). Spring Cloud Stream bilan bu `Consumer<OrderCreated>` / `Supplier<...>` bean'lari ko'rinishida yoziladi, `spring.cloud.stream.bindings.*` konfiguratsiyasi bilan. Event'larni atomar chiqarish uchun Transactional Outbox: Spring Modulith `@Externalized` + `spring-modulith-events-kafka`, yoki `@TransactionalEventListener(phase = AFTER_COMMIT)`. Idempotentlik uchun processed-message jadvali va `@Transactional` ichida unique constraint.

**Qo'llanish keyslari:**
- Buyurtma: `OrderCreated` → Inventory reserve → `StockReserved` → Payment charge → `PaymentCompleted` → `OrderConfirmed`.
- To'lov muvaffaqiyatsiz bo'lsa `PaymentFailed` eventi zaxirani avtomatik bo'shatadi.
- Foydalanuvchi ro'yxatdan o'tishi: profil yaratish → welcome email → bonus hisoblash.
- Kontent yuklash: fayl saqlash → transcoding → katalogda e'lon qilish.
- Obunani bekor qilish: billing to'xtatish → kirish huquqini olib tashlash → arxivlash.

**Ehtiyot bo'ling:** Qadamlar soni oshgani sayin oqim hech bir kodda ko'rinmay qoladi - debug va "hozir saga qayerda?" savoliga javob berish qiyinlashadi, shuning uchun 4-5 qadamdan ko'pida orkestratsiyaga o'ting. Tsiklik bog'liqlik (A eventi B'ni, B eventi yana A'ni uyg'otishi) va kompensatsiya qilib bo'lmaydigan qadamlar (yuborilgan email) ni oldindan hisobga oling.

## 14.9 Saga (orkestratsiya) (Saga (orchestration))

**Tavsif:** Tarqatilgan tranzaksiyani markaziy orchestrator (saga manager) boshqaradi: u ishtirokchilarga buyruq (command) yuboradi, javoblarni kutadi, holatni saqlaydi va xato bo'lsa kompensatsion buyruqlarni teskari tartibda ishga tushiradi. Oqim bitta joyda - state machine ko'rinishida - tasvirlanadi, shuning uchun murakkab shartlar, timeout'lar va retry'lar ancha boshqariladigan bo'ladi. Narxi - orchestrator qo'shimcha komponent va u biznes mantiqni o'ziga tortib ketishi mumkin.

**Spring'da qayerda uchraydi:** Orchestrator holatini saqlash uchun Spring Data JPA entity (`SagaInstance`, `@Version` bilan) va Spring Statemachine (`spring-statemachine-core`, `@EnableStateMachineFactory`, `StateMachinePersister`) ishlatiladi. Timeout va qayta urinish uchun `@Scheduled`, ShedLock yoki Quartz (`spring-boot-starter-quartz`); buyruqlar Kafka/RabbitMQ orqali boriladi. Tayyor yechimlar: Axon Framework (`@Saga`, `@SagaEventHandler`, `@StartSaga`/`@EndSaga` va `axon-spring-boot-starter`), Camunda 8 / Zeebe va Temporal (ikkisida ham Spring Boot starter bor), Eventuate Tram Saga. Resilience4j (`spring-cloud-starter-circuitbreaker-resilience4j`, `@Retry`, `@CircuitBreaker`) ishtirokchi chaqiruvlarini himoyalaydi.

**Qo'llanish keyslari:**
- Sayohat bron qilish: parvoz + mehmonxona + avtomobil, bittasi muvaffaqiyatsiz bo'lsa hammasi bekor qilinadi.
- Kredit arizasi: skoring → hujjat tekshiruvi → qo'lda tasdiqlash → shartnoma yaratish, har qadamda timeout bor.
- Mijoz onboarding: KYC → hisob ochish → karta buyurtmasi → yetkazib berish kuzatuvi.
- Katta buyurtmani bo'lib yuborish va qaytarishlarni (refund) kompensatsiya bilan boshqarish.
- Bulutli resurs provisioning: VM → tarmoq → DNS → monitoring, xatoda teskari tozalash.

**Ehtiyot bo'ling:** Orchestrator "god service" ga aylanib, ishtirokchilar anemik CRUD'ga tushib qolmasligi uchun unda faqat koordinatsiya mantiqi qolsin. Saga ACID emas: oraliq holatlar tashqariga ko'rinadi, shuning uchun `PENDING`/`CONFIRMED` statuslarini UI va API shartnomasida ochiq modellashtirish shart.

## 14.10 API kompozitsiyasi (API Composition)

**Tavsif:** Bir nechta servisdagi ma'lumotni talab qiladigan so'rovga javob berish uchun composer (API gateway, BFF yoki alohida servis) bir necha servisni chaqirib, natijani xotirada birlashtiradi. Bu cross-service join'ning eng oddiy almashtiruvchisi: qo'shimcha ma'lumot bazasi yoki replikatsiya kerak emas. Kamchiligi - latency chaqiruvlar yig'indisiga teng, availability ko'paytmaga aylanadi va katta hajmli join'lar (filtr/sort/pagination) samarasiz bo'ladi; bunday holatda CQRS read model afzal.

**Spring'da qayerda uchraydi:** Composer odatda Spring Boot BFF: `WebClient` bilan parallel chaqiruvlar (`Mono.zip`, `Flux.flatMap`) yoki `RestClient` + virtual thread'lar (`spring.threads.virtual.enabled=true`, Java 21+) bilan `CompletableFuture.allOf`. Deklarativ klientlar: `@HttpExchange` interfeysi + `HttpServiceProxyFactory`, yoki Spring Cloud OpenFeign `@FeignClient`. Spring for GraphQL (`spring-boot-starter-graphql`) `@SchemaMapping` va `@BatchMapping` (DataLoader) bilan N+1 ni yo'q qilib kompozitsiyani sxema darajasida beradi. Barqarorlik uchun Resilience4j `@CircuitBreaker`/`@TimeLimiter` va `spring-cloud-gateway` ning fallback marshrutlari; kuzatuv uchun Micrometer Tracing.

```java
public Mono<OrderView> load(String id) {
    return Mono.zip(
        orders.get().uri("/orders/{id}", id).retrieve().body(Order.class),
        customers.get().uri("/customers/{id}", id).retrieve().body(Customer.class),
        shipping.get().uri("/shipments?order={id}", id).retrieve().body(Shipment.class)
    ).map(t -> new OrderView(t.getT1(), t.getT2(), t.getT3()));
}
```

**Qo'llanish keyslari:**
- Buyurtma detali sahifasi: order + customer + payment + shipment bitta javobda birlashtiriladi.
- Mobil ilova uchun BFF bir ekranga kerakli 5 ta chaqiruvni bitta endpoint'ga yig'adi.
- Admin panelda mijoz kartasi uchun profil, obunalar va to'lov tarixi jamlanadi.
- GraphQL gateway `@BatchMapping` bilan ro'yxatdagi har bir element uchun N+1 chaqiruvni oldini oladi.
- Dashboard'da bir necha servis `/actuator/health` natijasi jamlanib ko'rsatiladi.

**Ehtiyot bo'ling:** Katta ro'yxatlarni xotirada join qilib keyin filtrlash va sahifalash - yashirin performance bombasi; bunday keyslarda CQRS read model yoki qidiruv indeksi kerak. Har bir qo'shilgan chaqiruv umumiy availability'ni pasaytiradi, shuning uchun timeout, circuit breaker va partial response (ba'zi bo'lagi bo'sh) strategiyasini oldindan belgilang.

## 14.11 Domen hodisasi (Domain Event (microservice view))

**Tavsif:** Servis o'z agregatida muhim o'zgarish bo'lganda bu faktni o'tgan zamonda nomlangan hodisa sifatida e'lon qiladi: `OrderPlaced`, `PaymentCaptured`, `CustomerDeactivated`. Boshqa servislar bu hodisalarga mustaqil ravishda reaksiya qiladi - natijada sinxron bog'liqlik asinxron bog'lanishga aylanadi va yangi iste'molchi qo'shish uchun ishlab chiqaruvchi servis o'zgarmaydi. Mikroservis kontekstida domen hodisasi saga, CQRS, self-contained service va audit'ning umumiy quruvchi bloki. Hodisa sxemasi - bu public API, shuning uchun u versiyalanadi va ehtiyotkorlik bilan evolyutsiya qiladi.

**Spring'da qayerda uchraydi:** Ichkarida `ApplicationEventPublisher.publishEvent(...)`, `@EventListener`, `@TransactionalEventListener(phase = AFTER_COMMIT)`; Spring Data JPA'da `AbstractAggregateRoot.registerEvent(...)` va `@DomainEvents`/`@AfterDomainEventPublication` repository save paytida hodisalarni chiqaradi. Spring Modulith `@ApplicationModuleListener` (bu `@Async` + `@TransactionalEventListener` + `@Transactional` kombinatsiyasi) va `@Externalized` bilan hodisani Kafka/AMQP'ga chiqaradi (`spring-modulith-events-kafka`, `spring-modulith-events-amqp`). Tashqariga chiqarish uchun `KafkaTemplate`, Spring Cloud Stream, sxema boshqaruvi uchun Avro/Protobuf + Schema Registry; CloudEvents formati ham keng ishlatiladi.

**Qo'llanish keyslari:**
- `OrderPlaced` hodisasi inventarizatsiya, email va analitikani bir vaqtda uyg'otadi.
- `CustomerAddressChanged` hodisasini Shipping va Billing servislari o'z replikalarini yangilash uchun oladi.
- Audit servisi barcha domen hodisalarini o'zgarmas log sifatida saqlaydi.
- `PriceChanged` hodisasi cache invalidatsiyasini keltirib chiqaradi.
- `SubscriptionExpired` hodisasi kirish huquqini olib tashlash oqimini boshlaydi.

**Ehtiyot bo'ling:** Hodisaga butun entity'ni (barcha maydonlari bilan) solib yuborish iste'molchilarni ichki modelingizga bog'lab qo'yadi - faqat ma'noli, barqaror maydonlarni chiqaring va sxemani faqat qo'shimcha (backward compatible) o'zgartiring. Hodisani `@Transactional` ichida to'g'ridan-to'g'ri broker'ga yuborish atomar emas: rollback bo'lsa ham hodisa ketgan bo'lishi mumkin - outbox ishlatiladi.

## 14.12 Tranzaksion Outbox (Transactional Outbox (microservice view))

**Tavsif:** Ma'lumot o'zgarishi va hodisa e'loni atomar bo'lishi uchun hodisa broker'ga emas, xuddi shu ma'lumotlar bazasidagi `outbox` jadvaliga bitta lokal tranzaksiyada yoziladi. Keyin alohida publisher (polling yoki log tailing) outbox yozuvlarini o'qib broker'ga yuboradi va yuborilgan deb belgilaydi. Shu bilan "DB commit bo'ldi, event ketmadi" yoki teskari holat yo'qoladi; kafolat at-least-once bo'ladi, shuning uchun iste'molchi idempotent bo'lishi shart. Bu dual-write muammosining standart yechimi.

**Spring'da qayerda uchraydi:** Eng tez yo'l - Spring Modulith: `spring-modulith-starter-jpa` (yoki `-jdbc`, `-mongodb`) event publication registry jadvalini yaratadi, `@ApplicationModuleListener` hodisani tranzaksiya bilan birga qaydga oladi va muvaffaqiyatsizlarini qayta yuborishga imkon beradi; `@Externalized("order-events::#{#this.id}")` + `spring-modulith-events-kafka` esa tashqi broker'ga chiqaradi. Qo'lda amalga oshirishda: `@Entity OutboxMessage`, `@Transactional` ichida `outboxRepository.save(...)`, keyin `@Scheduled` publisher + ShedLock (bir nechta instansda ikki marta yubormaslik uchun) va `KafkaTemplate`. Debezium Outbox Event Router bilan bu log tailing variantiga o'tadi.

```java
@Transactional
public void place(Order order) {
    orderRepository.save(order);
    events.publishEvent(new OrderPlaced(order.getId(), order.getTotal()));
}

@Externalized("order-events::#{#this.orderId}")
record OrderPlaced(String orderId, BigDecimal total) {}
```

**Qo'llanish keyslari:**
- To'lov servisi tranzaksiya yozuvini saqlab, `PaymentCaptured` hodisasini kafolatli chiqaradi.
- Buyurtma yaratish va `OrderCreated` eventini atomar e'lon qilish (saga boshlanishi).
- Monolitdan mikroservisga migratsiyada legacy DB o'zgarishlarini event'ga aylantirish.
- Kafka vaqtincha ishlamaganda hodisalar DB'da to'planib, keyin avtomatik yuboriladi.
- Audit va analitika oqimining hech bir hodisani yo'qotmasligini ta'minlash.

**Ehtiyot bo'ling:** Outbox jadvalini tozalashni (archival/partition) oldindan rejalashtirmaslik DB o'sishi va vacuum muammolariga olib keladi. At-least-once sababli dublikatlar bo'ladi: iste'molchida dedup kaliti (message id) va idempotent handler bo'lmasa, ikki marta to'lov yoki ikki marta email yuborilishi real risk.

## 14.13 Tranzaksiya logini kuzatish (Transaction Log Tailing)

**Tavsif:** Hodisalarni ilova kodidan emas, ma'lumotlar bazasining tranzaksiya logidan (PostgreSQL WAL, MySQL binlog, MongoDB oplog) o'qib chiqarish usuli - CDC (Change Data Capture). Tailer log'ni ketma-ket o'qiydi, har bir commit qilingan o'zgarishni hodisaga aylantirib broker'ga yuboradi; polling yo'q, latency past va ilovaga qo'shimcha yuk tushmaydi. Ko'pincha outbox bilan birga ishlatiladi: faqat `outbox` jadvalidagi insert'lar kuzatiladi va shu bilan hodisa sxemasi ichki jadval strukturasidan ajratiladi. Eng ko'p ishlatiladigan vosita - Debezium.

**Spring'da qayerda uchraydi:** Debezium Kafka Connect rejimida alohida ishlaydi (`debezium-connector-postgresql`, `io.debezium.transforms.outbox.EventRouter` SMT), Spring Boot ilovasi esa hodisalarni oddiy `@KafkaListener`/Spring Cloud Stream bilan iste'mol qiladi. Embedded rejimda `debezium-api` + `debezium-embedded` ishlatilib, `DebeziumEngine.create(...)` bean'i Spring konteynerida ko'tariladi (`SmartLifecycle` yoki `ApplicationRunner` orqali boshqariladi). Spring Modulith'ning `@Externalized` mexanizmi bilan outbox yozuvi yaratiladi, Debezium esa uni log'dan o'qib tarqatadi. Lokal ishlab chiqish va testda `spring-boot-docker-compose` yoki Testcontainers (`PostgreSQLContainer` logical replication yoqilgan holda, `KafkaContainer`, `DebeziumContainer`).

**Qo'llanish keyslari:**
- Legacy monolit bazasidagi o'zgarishlarni kodga tegmasdan event oqimiga aylantirish (Strangler Fig bilan birga).
- Outbox jadvalini polling'siz, past latency bilan broker'ga ko'chirish.
- Operatsion DB'dan analitik ombor (DWH/lakehouse) ga real-time replikatsiya.
- Qidiruv indeksi (Elasticsearch) yoki cache'ni DB o'zgarishiga qarab avtomatik yangilash.
- Mikroservislar o'rtasida read model (CQRS) ni DB o'zgarishidan qurish.

**Ehtiyot bo'ling:** CDC ni to'g'ridan-to'g'ri biznes jadvallariga ulash iste'molchilarni ichki sxemaga bog'laydi - har bir migratsiya tashqi kontraktni buzadi, shuning uchun outbox jadvali orqali o'tkazish afzal. Replication slot'ni kuzatmaslik (iste'molchi to'xtab qolsa WAL o'sib disk to'ladi), schema evolution va snapshot rejimining ishlab chiqarishdagi yuki - ekspluatatsiyadagi asosiy tuzoqlar.

## 14.14 Polling Publisher (Polling Publisher)

**Tavsif:** Transactional Outbox jadvaliga yozilgan xabarlarni alohida background process davriy ravishda `SELECT ... WHERE published = false` qilib o'qib, message broker'ga publish qiladi va keyin yozuvni `published = true` deb belgilaydi yoki o'chiradi. Bu Change Data Capture (Debezium, transaction log tailing) talab qilmaydigan eng oddiy outbox relay usuli - faqat SQL va scheduler kerak. Afzalligi - infratuzilma minimal; kamchiligi - polling interval tufayli latency paydo bo'ladi va DB'ga doimiy yuk tushadi. Yuqori throughput'da `FOR UPDATE SKIP LOCKED` va batch o'qish bilan optimallashtiriladi.

**Spring'da qayerda uchraydi:** `@Scheduled(fixedDelay = 500)` metod + `JdbcTemplate`/Spring Data JPA repository, ko'p instansiyada parallel ishlashi uchun `@Lock(LockModeType.PESSIMISTIC_WRITE)` yoki native query'da `FOR UPDATE SKIP LOCKED` (PostgreSQL 9.5+, MySQL 8). Publish uchun `KafkaTemplate`, `RabbitTemplate` yoki `StreamBridge` (Spring Cloud Stream). Cluster'da bitta instansiya ishlashi uchun ShedLock (`net.javacrumbs.shedlock`, `@SchedulerLock`) yoki Quartz clustered scheduler ishlatiladi; alternativ sifatida Spring Integration `JdbcPollingChannelAdapter` va `PollerMetadata`.

**Qo'llanish keyslari:**
- To'lov servisi `payment_outbox` jadvalidan `PaymentCaptured` event'larini har 200 ms'da Kafka'ga uzatadi.
- Debezium/Kafka Connect o'rnatish imkoni yo'q on-premise muhitda outbox relay'ni oddiy Spring Boot job bilan qurish.
- Legacy monolitdan strangler migratsiya davrida domain event'larni asta-sekin broker'ga chiqarish.
- Email/SMS notification queue'sini DB jadvalidan o'qib provider API'ga yuborish (retry va attempt counter bilan).
- Multi-tenant SaaS'da har bir tenant schema'sidagi outbox'ni bitta leader instansiya tomonidan skanerlash.

**Ehtiyot bo'ling:** Polling interval'ni juda kichik qilsangiz DB CPU va WAL yuki oshadi, juda katta qilsangiz end-to-end latency sekinlashadi; ko'p instansiyada `SKIP LOCKED` yoki distributed lock bo'lmasa bir xabar bir necha marta publish bo'ladi. Publish bo'lgandan keyin status update fail bo'lishi mumkin, shuning uchun consumer tomonida Idempotent Consumer majburiy - bu pattern at-least-once kafolat beradi, exactly-once emas.

## 14.15 Masofaviy protsedura chaqirig'i (Remote Procedure Invocation)

**Tavsif:** Servislar bir-biri bilan sinxron request/response stilida, masofaviy metod chaqirig'iga o'xshash protokol orqali gaplashadi - REST, gRPC, GraphQL yoki Thrift. Client so'rov yuboradi va javob kelguncha kutadi, shuning uchun model oddiy va debug qilish oson, lekin callee ishlamayotganda caller ham to'xtaydi (temporal coupling). Katta tizimlarda bu pattern Circuit Breaker, timeout va retry bilan birga qo'llanilishi shart. Odatda o'qish (query) operatsiyalari va darhol javob kerak bo'lgan hollarda tanlanadi.

**Spring'da qayerda uchraydi:** Server tomonda `@RestController`, `@GetMapping`/`@PostMapping`, Spring Boot 3.x'da `RestClient` va deklarativ `@HttpExchange` interfeyslari (`HttpServiceProxyFactory`), reaktiv stack'da `WebClient`; eski loyihalarda `RestTemplate` (maintenance mode) va OpenFeign (`spring-cloud-openfeign`, `@FeignClient`). gRPC uchun `grpc-spring-boot-starter` yoki Spring Boot 4 / Spring Framework 7 gRPC qo'llab-quvvatlashi, GraphQL uchun `spring-boot-starter-graphql` (`@QueryMapping`, `@SchemaMapping`). Java 21+ virtual thread'lar (`spring.threads.virtual.enabled=true`) blocking RPC'ni arzonlashtiradi.

**Qo'llanish keyslari:**
- API Gateway'dan `order-service`'ga mijoz buyurtmasi detallarini olish uchun REST GET chaqirig'i.
- Yuqori throughput'li internal servislar orasida gRPC + protobuf bilan past latency'li aggregatsiya.
- Mobil klient uchun bitta GraphQL endpoint orqali bir necha backend servis ma'lumotini birlashtirish.
- Autentifikatsiya servisidan token validation (introspection) uchun sinxron so'rov.
- To'lov provayderining sinxron authorize API'siga murojaat qilib darhol natija ko'rsatish.

**Ehtiyot bo'ling:** Sinxron chaqiriqlar zanjiri (A→B→C→D) availability'ni ko'paytma qilib kamaytiradi va latency'ni jamlaydi - har bir hop'da timeout, bulkhead va circuit breaker (Resilience4j) bo'lishi kerak. Yozuv operatsiyalarida retry'ni idempotency key'siz qilmang va distributed transaction o'rniga RPC zanjirini ishlatmang - bunday holatda Saga yoki Messaging to'g'ri tanlov.

## 14.16 Xabar almashish (Messaging)

**Tavsif:** Servislar bir-biriga to'g'ridan-to'g'ri murojaat qilmasdan, message broker orqali asinxron xabar (event yoki command) almashadi. Producer xabarni yuborib ishini davom etadi, consumer o'z tezligida qayta ishlaydi - bu temporal coupling'ni yo'q qiladi, consumer vaqtincha o'chsa ham xabarlar queue'da saqlanadi. Buffering, back-pressure va bir xabarni ko'p consumer'ga tarqatish (pub/sub) imkonini beradi. Narxi - eventual consistency, duplicate'lar va distributed debugging murakkabligi.

**Spring'da qayerda uchraydi:** `spring-kafka` (`@KafkaListener`, `KafkaTemplate`, `DefaultErrorHandler`, `DeadLetterPublishingRecoverer`), `spring-boot-starter-amqp` (`@RabbitListener`, `RabbitTemplate`), `spring-jms` (`@JmsListener`), Spring Cloud Stream binder'lari (`spring-cloud-stream-binder-kafka`, `Function<T, R>` bean'lari va `StreamBridge`), Spring Integration va Spring Pulsar (`@PulsarListener`). Cloud native variantlar: Spring Cloud AWS SQS (`@SqsListener`), Spring Cloud GCP Pub/Sub. Observability uchun Micrometer Tracing xabar header'lariga trace context'ni avtomatik propagate qiladi.

**Qo'llanish keyslari:**
- `OrderPlaced` event'ini inventory, billing va notification servislari mustaqil tinglashi.
- Og'ir hisobot generatsiyasini queue'ga topshirib HTTP so'rovni darhol `202 Accepted` bilan yopish.
- Saga orkestratsiyasida qadamlar orasida command/reply xabarlari almashish.
- CQRS'da read model'ni event stream'dan asinxron yangilash.
- Peak trafik paytida tashqi provayder rate limit'ini queue bilan tekislash (load leveling).

**Ehtiyot bo'ling:** Broker at-least-once yetkazadi, shuning uchun consumer idempotent bo'lishi va retry + DLQ strategiyasi aniq belgilanishi kerak; `@KafkaListener`'da cheksiz retry poison message bilan partition'ni butunlay to'xtatib qo'yadi. Xabar sxemasini (schema) versiyalamasdan o'zgartirish barcha consumer'larni buzadi - Avro/Protobuf + Schema Registry yoki tolerant reader yondashuvini qo'llang.

## 14.17 Domenga xos protokol (Domain-Specific Protocol)

**Tavsif:** Umumiy RPC yoki messaging o'rniga servis o'z domeniga xos, ko'pincha standartlashgan protokolni ishlatadi - SMTP, SIP, RTSP, MQTT, FIX, HL7/FHIR, AMQP yoki custom binary protokol. Bu protokollar o'z sohasida ishlab chiqilgani uchun domen semantikasi, performance xarakteristikasi va ekosistemasi (tool, sertifikatsiya, interop) tayyor bo'ladi. Integratsiya qiymati tashqi dunyo talablari bilan belgilanadi: hamkor tizim faqat FIX tushunsa, REST taklif qilish variant emas. Arxitektorning vazifasi - bu protokolni servis chegarasida adapter orqali ichki modelga tarjima qilish.

**Spring'da qayerda uchraydi:** Spring Integration adapter'lari: `spring-integration-mail` (SMTP/IMAP), `spring-integration-mqtt` (Eclipse Paho), `spring-integration-ftp`/`sftp`, `spring-integration-ip` (TCP/UDP, `TcpInboundGateway`), `spring-integration-file`, `spring-integration-xmpp`, `spring-integration-stomp`. Shuningdek `spring-boot-starter-mail` (`JavaMailSender`), WebSocket/STOMP uchun `@EnableWebSocketMessageBroker` va `@MessageMapping`, RSocket uchun `spring-boot-starter-rsocket` (`@MessageMapping`, `RSocketRequester`). Sohaga xos kutubxonalar: HAPI FHIR, QuickFIX/J, Eclipse Milo (OPC UA) - ularni `@Configuration` ichida bean qilib Spring lifecycle'ga bog'lanadi.

**Qo'llanish keyslari:**
- IoT platformasida minglab qurilma MQTT orqali telemetriya yuborishi, Paho inbound adapter bilan qabul qilish.
- Tibbiy integratsiyada laboratoriya tizimidan HL7 v2 / FHIR xabarlarini qabul qilib ichki event'ga aylantirish.
- Broker-dealer tizimida birja bilan FIX session orqali order routing.
- Email ingestion servisi IMAP'dan support xatlarini o'qib ticket yaratishi.
- Real-time dashboard uchun RSocket yoki STOMP over WebSocket bilan server→client streaming.

**Ehtiyot bo'ling:** Domen protokolini tizim ichkarisiga "sizdirib" yuborish eng katta xato - protokol modeli (FIX tag'lari, HL7 segmentlari) faqat adapter qatlamida qolishi, domen esa toza bo'lishi kerak. Bunday protokollar ko'pincha stateful session, maxsus TLS va vendor'ga xos quirk'lar talab qiladi, shuning uchun autoscaling va blue-green deploy rejasini oldindan sinab ko'ring.

## 14.18 Idempotent iste'molchi (Idempotent Consumer)

**Tavsif:** At-least-once yetkazib beruvchi broker bir xabarni takroriy yuborishi mumkin, shuning uchun consumer bir xabarni bir necha marta qayta ishlaganda ham natija bir martalik bilan bir xil bo'lishini ta'minlaydi. Amalga oshirishning asosiy usuli - har bir xabarning unique `messageId`'sini `processed_message` jadvaliga biznes o'zgarishi bilan bitta local transaction ichida yozish; takror kelganda unique constraint violation bo'lib xabar e'tiborsiz qoldiriladi. Alternativ - operatsiyani tabiiy idempotent qilish (`UPSERT`, absolute qiymat qo'yish, state machine'da faqat oldinga o'tish). Bu pattern deyarli har bir event-driven tizimda majburiy.

**Spring'da qayerda uchraydi:** `@KafkaListener`/`@RabbitListener` metod boshida dedup tekshiruvi + `@Transactional` bilan bitta DB transaction; Kafka'da `ConsumerRecord` kaliti `topic-partition-offset` yoki `@Header(KafkaHeaders.RECEIVED_KEY)`, RabbitMQ'da `MessageProperties.getMessageId()`. Spring Integration'da to'g'ridan-to'g'ri `IdempotentReceiverInterceptor` + `MetadataStoreSelector` (`JdbcMetadataStore`, `RedisMetadataStore`) mavjud. Dedup store uchun Redis `SETNX`/`opsForValue().setIfAbsent(...)` (`StringRedisTemplate`) yoki JPA entity'da `@Id` sifatida `messageId` ishlatiladi; Kafka Streams'da `exactly_once_v2` processing guarantee qo'shimcha himoya beradi.

**Qo'llanish keyslari:**
- To'lov hisobga olish servisi `PaymentCaptured` event'ini ikki marta olganda balansni ikki marta oshirmasligi.
- Rebalance yoki consumer crash'dan keyin qayta o'qilgan Kafka offset'lardagi xabarlarni xavfsiz qayta ishlash.
- Saga reply xabarlarini qayta ishlashda qadam holatini `state machine` orqali faqat oldinga surish.
- Webhook endpoint'da provider (Stripe/PayPal) retry qilgan bir hodisani bir marta hisobga olish.
- Email yuborish consumer'ida duplikat xabarga ikkinchi email jo'natmaslik.

**Ehtiyot bo'ling:** Dedup yozuvini biznes o'zgarishidan alohida transaction'da yozish pattern'ni buzadi - ikkisi bir atomar birlikda bo'lishi shart, aks holda crash oynasida duplikat yoki yo'qotish yuz beradi. Dedup jadvali cheksiz o'smasligi uchun TTL/retention (masalan 7 kun) qo'ying, lekin retention broker'ning maksimal retry/replay oynasidan uzunroq bo'lsin.

## 14.19 Klient tomonda aniqlash (Client-Side Discovery)

**Tavsif:** Client (yoki uning ichidagi kutubxona) Service Registry'dan maqsadli servisning mavjud instansiyalari ro'yxatini oladi va o'zi load balancing qarorini qabul qiladi - qaysi instansiyaga so'rov yuborishni tanlaydi. Bu qo'shimcha network hop'ni yo'q qiladi va client'ga aqlli strategiya (zone affinity, least-requests, weighted) berish imkonini yaratadi. Kamchiligi - har bir til/stack uchun discovery client logikasi kerak va client registry'ga bog'lanadi. Service mesh davrida bu mantiq ko'pincha sidecar proxy'ga ko'chiriladi.

**Spring'da qayerda uchraydi:** `spring-cloud-commons` ning `DiscoveryClient` abstraktsiyasi va `spring-cloud-loadbalancer` (`@LoadBalanced RestTemplate`/`WebClient.Builder`, `LoadBalancerClient`, `ReactorServiceInstanceLoadBalancer`); Spring Boot 3.x'da `RestClient.Builder` ham `@LoadBalanced` bo'lishi mumkin. Registry implementatsiyalari: `spring-cloud-starter-netflix-eureka-client`, `spring-cloud-starter-consul-discovery`, `spring-cloud-starter-zookeeper-discovery`, `spring-cloud-kubernetes-client-discovery`. OpenFeign `@FeignClient(name = "order-service")` da logical nom avtomatik Spring Cloud LoadBalancer orqali hal qilinadi. Netflix Ribbon endi mavjud emas - zamonaviy loyihada Spring Cloud LoadBalancer ishlatiladi.

**Qo'llanish keyslari:**
- Eureka'ga ro'yxatdan o'tgan `inventory-service` instansiyalari orasida `@LoadBalanced WebClient` bilan round-robin so'rov yuborish.
- Bir xil zone'dagi instansiyalarni afzal ko'rish (zone affinity) bilan cross-AZ trafik xarajatini kamaytirish.
- Canary release'da instance metadata'siga qarab trafikning kichik qismini yangi versiyaga yo'naltirish.
- Hammasi Java/Spring bo'lgan ichki platformada hech qanday markaziy LB'ga tayanmasdan servis-servis chaqiriqlar.
- Consul'dagi health-check natijasiga qarab sog'lom instansiyalarnigina tanlash.

**Ehtiyot bo'ling:** Client'dagi instansiya ro'yxati cache'lanadi, shuning uchun scale-in yoki crash'dan keyin bir muddat "o'lik" instansiyaga so'rov ketadi - refresh interval'ni va retry (`spring-retry` + `LoadBalancedRetryPolicy`) sozlamasini birgalikda tuzatish kerak. Polyglot muhitda har bir tilda discovery client saqlash qimmat; bunda Server-Side Discovery yoki service mesh (Istio/Linkerd) ko'proq mos keladi.

## 14.20 Server tomonda aniqlash (Server-Side Discovery)

**Tavsif:** Client faqat barqaror manzilga (router, load balancer yoki gateway) so'rov yuboradi; registry'ni so'rash va instansiya tanlash mas'uliyati shu infratuzilma komponentiga tegishli. Client hech qanday discovery kodi saqlamaydi, shuning uchun polyglot muhit uchun ideal va discovery logikasi markazlashgan holda yangilanadi. Kamchiligi - qo'shimcha network hop va LB'ning o'zi high-availability talab qiladigan kritik komponentga aylanishi. Kubernetes'dagi `Service` + kube-proxy/DNS, AWS ALB yoki Istio sidecar - bu pattern'ning eng keng tarqalgan ko'rinishlari.

**Spring'da qayerda uchraydi:** Spring Cloud Gateway (`spring-cloud-starter-gateway`, Boot 3.x'da reactive yoki `gateway-server-webmvc`) `lb://order-service` URI bilan discovery'ni server tomonda bajaradi; `DiscoveryClientRouteDefinitionLocator` registry'dan route'larni avtomatik yaratadi. Kubernetes'da Spring Boot ilovasi oddiygina `http://order-service:8080` ga `RestClient` bilan murojaat qiladi va DNS/kube-proxy load balancing qiladi - kodda hech qanday discovery bean kerak emas; `spring-cloud-kubernetes` ConfigMap/Secret va discovery integratsiyasini qo'shadi. Istio/Linkerd bilan esa barcha chiqish trafigi Envoy sidecar orqali o'tadi, ilova faqat logical hostname biladi.

**Qo'llanish keyslari:**
- Kubernetes'da Java, Go va Node servislari bir-birini `Service` DNS nomi orqali chaqirishi.
- Spring Cloud Gateway orqali tashqi trafikni `lb://` route'lar bilan ichki servislarga taqsimlash.
- mTLS, retry va circuit breaking siyosatini Istio DestinationRule'da markazlashgan boshqarish.
- AWS ECS/ALB target group orqali avtoskaling qilinadigan servis instansiyalariga trafik yuborish.
- Legacy .NET klientlari Spring servislariga hech qanday SDK o'rnatmasdan ulanishi.

**Ehtiyot bo'ling:** Qo'shimcha hop latency va single point of failure xavfini keltiradi - LB/gateway'ni albatta bir nechta replika va health-check bilan ishlating. Gateway'ga biznes logikani (validatsiya, transformatsiya, orkestratsiya) yuklash klassik anti-pattern: u yangi monolitga aylanadi; gateway faqat routing, auth va cross-cutting masalalar bilan shug'ullansin.

## 14.21 Servis reyestri (Service Registry)

**Tavsif:** Service Registry - barcha servis instansiyalari va ularning tarmoq manzillarining markaziy, doimiy yangilanadigan ma'lumotlar bazasi. U registration API (instansiya o'zini yozadi/yangilaydi) va query API (client yoki router instansiyalarni so'raydi) ni taqdim etadi, shuningdek health check orqali javob bermayotgan yozuvlarni chiqarib tashlaydi. Dinamik muhitda (autoscaling, container, ephemeral IP) qattiq kodlangan manzillar ishlamaganda bu pattern asos bo'ladi. Registry o'zi yuqori darajada available bo'lishi kerak, chunki u butun tizimning control plane'i.

**Spring'da qayerda uchraydi:** Netflix Eureka server - `spring-cloud-netflix-eureka-server` va `@EnableEurekaServer` (peer-to-peer replikatsiya bilan HA). Alternativlar: HashiCorp Consul (`spring-cloud-starter-consul-discovery`), Apache ZooKeeper (`spring-cloud-starter-zookeeper-discovery`), etcd va Kubernetes'ning o'zining `Service`/`EndpointSlice` obyektlari (`spring-cloud-kubernetes-client-discovery` ularni `DiscoveryClient` sifatida ko'rsatadi). Spring Cloud tomonda hammasi `DiscoveryClient`/`ReactiveDiscoveryClient` interfeysi ortida abstraktlanadi, shuning uchun registry'ni almashtirish ko'p hollarda dependency va konfiguratsiya o'zgarishi bilan cheklanadi.

**Qo'llanish keyslari:**
- On-premise Spring Cloud platformasida Eureka cluster'ni control plane sifatida ishlatish.
- Consul'da servis instansiyalari bilan birga KV-store'dan dinamik konfiguratsiya olish.
- Hybrid muhitda VM'dagi legacy servislarni Consul'ga yozib, Kubernetes'dagi yangi servislarga ko'rinadigan qilish.
- Instance metadata (version, zone, canary bayrog'i) orqali aqlli routing qarorlari qabul qilish.
- Blue-green deploy'da yangi rang instansiyalarini registry'ga qo'shib, keyin eskisini chiqarib tashlash.

**Ehtiyot bo'ling:** Registry - tizim uchun single point of failure; uni bir nechta node bilan HA qilib, client tomonda oxirgi ma'lum ro'yxatni cache qilib ishlashga (fail-static) tayyor bo'lish kerak. Kubernetes'da ishlayotgan bo'lsangiz, platformaning o'z discovery'si ustiga Eureka qo'shish ko'pincha ortiqcha murakkablik - faqat real sabab bo'lganda (hybrid, VM'lar, cross-cluster) qo'shing.

## 14.22 O'z-o'zini ro'yxatga olish (Self Registration)

**Tavsif:** Servis instansiyasi ishga tushganda registry'ning registration API'siga o'zini yozadi, davriy heartbeat yuborib "tirik" ekanini bildiradi va to'g'ri o'chishda (graceful shutdown) o'zini de-register qiladi. Bu eng oddiy yondashuv, chunki hech qanday qo'shimcha infratuzilma komponenti kerak emas va instansiya o'zi haqida boy metadata (versiya, zone, capability) berishi mumkin. Kamchiligi - registration kodi ilovaga kiradi, demak har bir til/framework uchun client kutubxona kerak va ilova registry bilan bog'lanib qoladi.

**Spring'da qayerda uchraydi:** `spring-cloud-starter-netflix-eureka-client` classpath'da bo'lsa ilova avtomatik registratsiya qiladi (`eureka.client.service-url.defaultZone`, `eureka.instance.*`, lease renewal interval); Consul uchun `spring-cloud-starter-consul-discovery` `spring.cloud.consul.discovery.*` va health-check sifatida Actuator `/actuator/health` endpoint'ini ishlatadi. Boshqaruv `@EnableDiscoveryClient` (zamonaviy versiyalarda ko'pincha ixtiyoriy) va `spring.cloud.discovery.enabled` orqali; graceful shutdown uchun `server.shutdown=graceful` va `spring.lifecycle.timeout-per-shutdown-phase` bilan birga `ServiceRegistry.deregister(...)` lifecycle hook ishlaydi. Metadata `eureka.instance.metadata-map.version=2.3.1` ko'rinishida beriladi.

**Qo'llanish keyslari:**
- Spring Boot servislari Eureka'ga ishga tushishi bilan o'zini yozib, 30 soniyalik heartbeat yuborishi.
- Instance metadata'ga build versiyasini qo'yib, canary routing qoidalarini shunga asoslash.
- Autoscaling guruhida yangi pod/VM ko'tarilganda qo'lda hech narsa qilmasdan trafikka qo'shilishi.
- Graceful shutdown'da de-register qilib, keyin in-flight so'rovlarni tugatish (zero-downtime deploy).
- Consul health-check sifatida Actuator readiness probe'ni ulab, DB uzilganda instansiyani trafikdan chiqarish.

**Ehtiyot bo'ling:** Heartbeat interval va lease expiration sozlamalari noto'g'ri bo'lsa, o'lgan instansiya registry'da uzoq "tirik" turadi yoki tirik instansiya noto'g'ri chiqarib tashlanadi - Eureka'ning self-preservation rejimi ham bu xatti-harakatni o'zgartiradi, uni production'da bilib turing. Graceful shutdown'da de-register bo'lmasa klientlar o'chgan instansiyaga so'rov yuboraveradi; shuningdek registration kodi ilovaga kirishi polyglot muhitda 3rd Party Registration'ni afzal qiladi.

## 14.23 Uchinchi tomon orqali ro'yxatga olish (3rd Party Registration)

**Tavsif:** Instansiyalarni registry'ga yozish va chiqarish mas'uliyati ilovadan tashqaridagi alohida komponentga - registrar yoki deployment platformasiga beriladi. Registrar deployment muhitini (container runtime, orchestrator API) kuzatadi va yangi instansiya paydo bo'lganda registry'ga yozadi, yo'qolganda o'chiradi. Ilova kodi discovery haqida hech narsa bilmaydi, bu polyglot tizimlar va legacy ilovalar uchun katta afzallik. Narxi - yana bir infratuzilma komponenti va uning o'zi HA bo'lishi talabi.

**Spring'da qayerda uchraydi:** Kubernetes bu pattern'ning eng keng tarqalgan ko'rinishi: kubelet va endpoint controller Pod'ni `Service`/`EndpointSlice`'ga avtomatik qo'shadi, ilovada hech qanday registratsiya kodi bo'lmaydi - Spring Boot faqat `/actuator/health/readiness` va `/actuator/health/liveness` probe'larini ochadi (`management.endpoint.health.probes.enabled=true`, Kubernetes aniqlansa avtomatik yoqiladi). Boshqa muhitlarda Registrator/Consul agent, AWS ECS service discovery yoki Nomad shu ishni qiladi. Spring tomonda `spring-cloud-kubernetes` registratsiya o'rniga faqat discovery va konfiguratsiya tomonini ta'minlaydi; Istio'da sidecar injection ham shu modelga kiradi.

**Qo'llanish keyslari:**
- Kubernetes Deployment'dagi Spring Boot pod'larining readiness probe'ga qarab Service endpoint'lariga avtomatik qo'shilishi.
- Java, Python va Node servislari bir xil registratsiya mexanizmidan foydalanishi (hech biriga SDK kerak emas).
- Legacy WAR ilovasini kodini o'zgartirmasdan Consul registrator orqali discovery'ga kiritish.
- ECS task'lari AWS Cloud Map'ga platforma tomonidan yozilishi.
- Platform jamoasi registratsiya siyosatini (TTL, health-check turi) markazdan yangilay olishi.

**Ehtiyot bo'ling:** Registrar ishdan chiqsa registry haqiqatdan uzoqlashadi (stale yoki yo'q yozuvlar) - uni monitoring va alerting bilan qoplang. Ilovaning health endpoint'i sayoz bo'lsa (masalan DB uzilganida ham `UP` qaytarsa) platforma buzuq instansiyaga trafik yuboraveradi, shuning uchun readiness probe'ni haqiqiy dependency'larga asoslang va liveness'ni og'ir tekshiruvlar bilan yuklab yubormang.

## 14.24 Access token (Access Token)

**Tavsif:** API Gateway yoki edge servis foydalanuvchini bir marta autentifikatsiya qiladi va keyingi servis-servis chaqiriqlarida foydalanuvchi shaxsi hamda huquqlarini o'zi ichida tasdiqlangan holda tashuvchi token (odatda JWT) uzatiladi. Har bir downstream servis token imzosini va claim'larini mustaqil tekshiradi, shuning uchun markaziy session store'ga har safar murojaat qilish shart emas. Bu shaxsni tizim bo'ylab ishonchli propagate qilish va "confused deputy" muammosidan qochish imkonini beradi. Token qisqa muddatli bo'lishi, audience va scope bilan cheklanishi kerak.

**Spring'da qayerda uchraydi:** `spring-boot-starter-oauth2-resource-server` (`JwtDecoder`, `NimbusJwtDecoder`, `JwtAuthenticationConverter`, `@PreAuthorize("hasAuthority('SCOPE_orders.write')")`, `http.oauth2ResourceServer(o -> o.jwt(...))`), token olish va propagate qilish uchun `spring-boot-starter-oauth2-client` + `OAuth2AuthorizedClientManager` va Spring Boot 3.x'da `ServletOAuth2AuthorizedClientExchangeFilterFunction` (WebClient) yoki `RestClient` interceptor'i. Authorization server sifatida Spring Authorization Server (`spring-boot-starter-oauth2-authorization-server`) yoki Keycloak. Reaktiv stack'da `ReactiveJwtDecoder`, Gateway'da `TokenRelay` filtri. Mikroservislar orasida mTLS bilan birgalikda ishlatilsa eng kuchli natija beradi.

```java
@Bean
SecurityFilterChain api(HttpSecurity http) throws Exception {
    return http
        .authorizeHttpRequests(a -> a
            .requestMatchers("/api/orders/**").hasAuthority("SCOPE_orders.write")
            .anyRequest().authenticated())
        .oauth2ResourceServer(o -> o.jwt(Customizer.withDefaults()))
        .build();
}
```

**Qo'llanish keyslari:**
- Gateway OAuth2 code flow'ni bajarib, downstream servislarga JWT'ni `Authorization: Bearer` header'ida relay qilishi.
- `order-service` chaqirgan `payment-service`'da ham foydalanuvchi `sub` va `scope`'ini tekshirish (end-to-end authorization).
- Machine-to-machine integratsiyada client-credentials grant bilan servis tokeni olish.
- Multi-tenant SaaS'da tenant identifikatorini JWT custom claim sifatida tashish.
- Audit log'larda har bir operatsiya uchun haqiqiy foydalanuvchi shaxsini qayd etish.

**Ehtiyot bo'ling:** JWT'ni faqat imzo emas, `iss`, `aud`, `exp` va kerakli scope'larni ham tekshiring, va tashqi klient tokenini hech qachon ichki ishonch chegarasida tekshirmasdan qabul qilmang. Uzoq muddatli JWT'ni revoke qilish amalda mumkin emas - qisqa TTL + refresh token ishlating, token ichiga ko'p shaxsiy ma'lumot joylashtirmang (u faqat base64, shifrlangan emas) va tokenni log'larga yozmang.

## 14.25 Server tomonda sahifa fragmentini kompozitsiya qilish (Server-Side Page Fragment Composition)

**Tavsif:** Bir sahifa bir nechta jamoaga tegishli fragmentlardan iborat bo'ladi va ularni serverda yig'uvchi qatlam (frontend server, gateway yoki edge) birlashtirib, brauzerga yakuniy HTML yuboradi. Har bir jamoa o'z fragmentini mustaqil deploy qiladi, lekin foydalanuvchi bitta, SEO-ga do'st va tez first-paint beradigan sahifani oladi. Bu micro frontend yondashuvining server tomonidagi varianti - ESI, SSI yoki shablon-darajasidagi include bilan amalga oshiriladi. Asosiy savollar: fragment timeout'i, fallback va umumiy layout/dizayn tizimining egasi kim.

**Spring'da qayerda uchraydi:** Thymeleaf fragment'lari (`th:insert`, `th:replace`, `th:fragment`) va Thymeleaf Layout Dialect bilan server-side kompozitsiya; `spring-boot-starter-thymeleaf`. Haqiqiy micro frontend uchun Spring Boot'da Thymeleaf dialekti sifatida ishlaydigan Zalando Tailor/Tailor-x, `io.github.openfeign`/`RestClient` bilan fragment HTML'ini olib `Unstructured` qo'shish, yoki `spring-cloud-gateway` `ModifyResponseBody` filtri. Reaktiv stack'da `WebFlux` + `spring-webflux` Thymeleaf reactive rendering `IReactiveDataDriverContextVariable` orqali fragment'larni streaming qiladi. Alternativ: Nginx/Varnish ESI yoki Apache SSI edge'da, Spring servislari esa faqat fragment chiqaradi.

**Qo'llanish keyslari:**
- E-commerce mahsulot sahifasida narx, sharhlar va tavsiyalar fragment'larini turli jamoalar servisidan yig'ish.
- SEO muhim bo'lgan marketplace sahifalarini SPA'ga o'tmasdan server'da to'liq render qilish.
- Monolitdan ko'chishda sahifaning bir bo'lagini yangi servisga berib, qolganini legacy'da qoldirish.
- Admin portalda modullarni (billing, users, reports) mustaqil deploy qiladigan jamoalarga ajratish.
- Past quvvatli qurilmalar uchun JavaScript bundle'ni kamaytirib, HTML'ni serverda yig'ish.

**Ehtiyot bo'ling:** Bir sekin fragment butun sahifani ushlab turmasligi uchun har bir fragment chaqirig'iga qat'iy timeout, circuit breaker va bo'sh/keshlangan fallback bering. Umumiy CSS, dizayn tokenlari va versiyalanishini boshqarmasa, sahifa vizual jihatdan tarqalib ketadi va kompozitsiya qatlami yangi muvofiqlashtirish bo'yni (coupling point) bo'lib qoladi.

## 14.26 Klient tomonda UI kompozitsiyasi (Client-Side UI Composition)

**Tavsif:** Sahifa brauzerda yig'iladi: shell ilova turli jamoalar deploy qilgan frontend modullarni (fragment, web component yoki remote bundle) runtime'da yuklaydi va har biri o'z backend servisi bilan to'g'ridan-to'g'ri gaplashadi. Bu jamoalarga to'liq mustaqil deploy va texnologiya tanlash erkinligini beradi, shuningdek sahifa bir qismi ishlamasa ham qolgani ishlashini (graceful degradation) ta'minlaydi. Odatda Module Federation, custom elements yoki single-spa bilan quriladi. Narxi - bundle hajmi, shared dependency boshqaruvi va birinchi yuklanish tezligi.

**Spring'da qayerda uchraydi:** Spring Boot bu yerda asosan backend tomonini ta'minlaydi: har bir micro frontend o'z Spring Boot servisiga `@RestController`/GraphQL orqali murojaat qiladi, CORS `@CrossOrigin` yoki `CorsConfigurationSource` bilan sozlanadi, static asset'lar `src/main/resources/static` dan yoki CDN'dan beriladi. Edge'da Spring Cloud Gateway path-based routing (`/billing/**` → billing frontend + API) bilan bir origin ko'rinishini yaratadi, bu CORS va cookie muammolarini kamaytiradi. BFF (Backend for Frontend) pattern'i har bir micro frontend uchun alohida Spring Boot modul sifatida quriladi; autentifikatsiya shell'da OAuth2 (`spring-boot-starter-oauth2-client` bilan BFF rejimida, token brauzerga chiqarilmaydi) orqali hal qilinadi.

**Qo'llanish keyslari:**
- Katta SaaS konsolida "Billing", "Users" va "Analytics" modullarini alohida jamoalar mustaqil deploy qilishi.
- Webpack/Vite Module Federation bilan remote modullarni runtime'da yuklab, har birini o'z CI/CD'si bilan chiqarish.
- Legacy Angular portaliga yangi React widget'ini web component sifatida qo'shish.
- Dashboard'da har bir widget o'z servisidan ma'lumot olishi va biri ishlamasa qolgani ishlashi.
- Mobil va web klientlar uchun alohida BFF qurib, har biriga mos payload shakllantirish.

**Ehtiyot bo'ling:** Shared dependency (React, dizayn tizimi) versiyalarini muvofiqlashtirmasa bundle hajmi va runtime konflikt muammolari paydo bo'ladi, SEO va first-contentful-paint esa server-side kompozitsiyadan yomonroq bo'lishi mumkin. Autentifikatsiya tokenini brauzer `localStorage`'ida saqlash XSS xavfini oshiradi - BFF + `HttpOnly` cookie yondashuvi afzal; shuningdek cross-module global state'ni iloji boricha kamaytiring, aks holda mustaqillik illyuziyaga aylanadi.

## 14.27 API Gateway (API Gateway)

**Tavsif:** Barcha tashqi client'lar uchun yagona kirish nuqtasini yaratadi va so'rovlarni orqadagi microservice'larga routing qiladi. Gateway qatlamida cross-cutting vazifalar - autentifikatsiya, rate limiting, TLS termination, so'rov/javob transformatsiyasi, circuit breaking - bir joyda markazlashadi. Natijada client'lar o'nlab host'ni bilishi va har biri bilan alohida shartnoma tuzishi shart emas. Shu bilan birga gateway tizimning yagona kirish nuqtasi bo'lgani uchun uning o'zi ham yuqori darajada available bo'lishi talab qilinadi.

**Spring'da qayerda uchraydi:** `spring-cloud-starter-gateway` (Spring Cloud Gateway) - reactive, Spring WebFlux va Netty ustida ishlaydi; `RouteLocator`/`RouteLocatorBuilder` bean'i yoki `application.yml` ichidagi `spring.cloud.gateway.routes` orqali route e'lon qilinadi. Predicate'lar (`Path`, `Host`, `Method`, `Header`) va filter'lar (`StripPrefix`, `RewritePath`, `CircuitBreaker`, `RequestRateLimiter`, `Retry`) GatewayFilterFactory sifatida keladi; o'z filter'ingiz uchun `GlobalFilter` yoki `AbstractGatewayFilterFactory` implement qilinadi. Spring Boot 3.x/4.x da `spring-cloud-gateway-server-webmvc` varianti blocking (Servlet) stack uchun ham mavjud. `RequestRateLimiter` odatda `RedisRateLimiter` bilan, xavfsizlik esa `spring-boot-starter-oauth2-resource-server` va `spring-security` ReactiveSecurityFilterChain bilan birga quriladi. Service discovery bilan integratsiya `lb://service-name` URI va `DiscoveryClientRouteDefinitionLocator` orqali amalga oshadi.

**Qo'llanish keyslari:**
- Mobil va web client'lar uchun yagona public HTTPS endpoint ochish va orqadagi 40 ta service'ni yashirish.
- JWT tekshiruvini gateway'da bajarib, downstream service'larga ishonchli header (`X-User-Id`) uzatish.
- Public API uchun Redis asosidagi rate limiting bilan bir client'ni sekundiga N so'rovga cheklash.
- Legacy monolitdan microservice'ga bosqichma-bosqich o'tishda trafikni path bo'yicha yangi service'ga yo'naltirish (strangler).
- Canary release'da header yoki weight predicate bilan trafikning 5%'ini yangi versiyaga berish.

**Ehtiyot bo'ling:** Gateway'ga business logika yuklash eng keng tarqalgan xato - u tezda yangi monolitga va har bir jamoa uchun deployment bottleneck'ga aylanadi. Shuningdek Spring Cloud Gateway reactive bo'lgani uchun filter ichida blocking JDBC yoki `RestTemplate` chaqirmang, aks holda Netty event loop thread'lari band bo'lib butun gateway qotib qoladi.

## 14.28 Frontend uchun Backend (Backend for Frontend)

**Tavsif:** Yagona umumiy API o'rniga har bir client turi - iOS, Android, web SPA, hamkor API - uchun alohida backend qatlami quriladi. Har bir BFF faqat o'z client'iga kerakli ma'lumotni downstream service'lardan yig'adi, keraksiz field'larni tashlab, aynan o'sha UI ekranlariga mos shaklda qaytaradi. Bu mobil client'da over-fetching va chatty network chaqiruvlarini kamaytiradi hamda UI jamoasiga o'z backend'ini mustaqil deploy qilish imkonini beradi. Amalda BFF - bu bitta client'ga tegishli, o'sha client jamoasi egalik qiladigan ixtisoslashgan aggregator.

**Spring'da qayerda uchraydi:** Har bir BFF odatda alohida Spring Boot 3.x ilovasi: `@RestController` + `WebClient` (reactive) yoki `RestClient` (Spring Framework 6.1+ dan, blocking) orqali downstream'ga parallel chaqiruvlar. Reactive BFF'da `Mono.zip(...)`/`Flux.zip(...)` bilan bir nechta service javobi birlashtiriladi; blocking stack'da Java 21+ virtual thread (`spring.threads.virtual.enabled=true`) yoki structured concurrency bilan parallel yig'ish qilinadi. Deklarativ client uchun `@HttpExchange` + `HttpServiceProxyFactory` (Spring interface clients) yoki Spring Cloud OpenFeign ishlatiladi. Sessiya va token almashinuvi uchun `spring-boot-starter-oauth2-client` bilan "token-mediating BFF" namunasi keng qo'llanadi: browser'da faqat HttpOnly cookie, access token esa BFF'da saqlanadi (`OAuth2AuthorizedClientManager`). GraphQL variantida `spring-boot-starter-graphql` va `@SchemaMapping`/`@BatchMapping` ishlatiladi.

**Qo'llanish keyslari:**
- Mobil ilova uchun bitta "home screen" endpoint'i yasash: 5 ta service javobini bitta ixcham JSON'ga yig'ish.
- SPA uchun token-mediating BFF: access token'ni browser'ga chiqarmaslik, faqat secure cookie bilan ishlash.
- Smart TV yoki kiosk kabi kam imkoniyatli client'ga yengillashtirilgan, oldindan formatlangan response berish.
- Hamkorlar (partner) uchun public API'ni ichki model'dan ajratilgan alohida shartnoma bilan taqdim etish.
- Web va mobil UI'ni turli tezlikda rivojlantirish: har bir BFF mustaqil release cycle'da bo'ladi.

**Ehtiyot bo'ling:** Client turlari ko'paygani sayin BFF'lar soni ortib, ularda bir xil logika takrorlanadi - umumiy qoidalarni downstream service'ga yoki shared kutubxonaga chiqarmasa, maintenance narxi keskin oshadi. BFF'ni "hamma uchun bitta" qilib qo'ysangiz, u oddiy API Gateway'ga aylanadi va BFF pattern'ining asosiy foydasi yo'qoladi.

## 14.29 Microservice Shassi (Microservice Chassis)

**Tavsif:** Har bir microservice'ga kerak bo'ladigan infratuzilma imkoniyatlari - configuration, logging, metrics, health check, tracing, security, exception handling - qayta-qayta yozilmasligi uchun yagona asos (chassis) sifatida tayyorlanadi. Jamoa yangi service boshlaganda bu chassis'ni olib, faqat business logikani yozadi. Natijada cross-cutting masalalar bir joyda standartlashadi va butun landscape bo'ylab bir xil ishlaydi. Chassis odatda kutubxona (starter) yoki template ko'rinishida yetkaziladi.

**Spring'da qayerda uchraydi:** Spring Boot'ning o'zi de-facto chassis: auto-configuration, `spring-boot-starter-actuator` (health, metrics, `/actuator/prometheus`), Micrometer + Micrometer Tracing (OpenTelemetry/Brave bridge), `spring-boot-starter-validation`, Spring Cloud Config/Consul client, Resilience4j. Tashkilot darajasida o'z chassis'ingiz custom starter sifatida qilinadi: `spring.factories` o'rniga Boot 3.x da `META-INF/spring/org.springframework.boot.autoconfigure.AutoConfiguration.imports` fayliga `@AutoConfiguration` sinflari yoziladi, `@ConditionalOnMissingBean`/`@ConditionalOnProperty` bilan override imkoniyati qoldiriladi, `@ConfigurationProperties` bilan sozlamalar e'lon qilinadi. Umumiy xato formati `@ControllerAdvice` + `ProblemDetail` (RFC 7807) orqali, correlation ID `ObservationRegistry` yoki MDC filter orqali markazlashtiriladi.

**Qo'llanish keyslari:**
- Barcha service'larda bir xil `ProblemDetail` xato formati va error code taksonomiyasini majburlash.
- Kompaniya standartidagi observability (tracing, metrics, structured JSON logging) ni bitta starter bilan yoqish.
- Ichki service-to-service autentifikatsiya (mTLS yoki OAuth2 client credentials) ni avtomatik sozlash.
- Umumiy Kafka producer/consumer sozlamalari, retry va DLT (dead-letter topic) siyosatini bir joyda belgilash.
- Yangi service'ni bir kun ichida production-ready holatda ko'tarish (health probe, graceful shutdown, readiness).

**Ehtiyot bo'ling:** Chassis'ga business logika yoki domain model kirib qolsa, u shared library coupling'ga aylanadi va har bir versiya yangilanishi butun landscape'ni bir vaqtda deploy qilishga majbur qiladi. Versiyalashni jiddiy oling: chassis'ning major versiyasi uzun muddat qo'llab-quvvatlanishi va service'lar o'z tezligida migratsiya qilishi mumkin bo'lsin.

## 14.30 Tashqariga chiqarilgan konfiguratsiya (Externalized Configuration)

**Tavsif:** Konfiguratsiya qiymatlari (DB URL, credential, feature flag, timeout) artifact ichiga qotirilmaydi, balki tashqi manbadan - environment variable, config server, secret store yoki ConfigMap'dan - ish vaqtida o'qiladi. Shu sababli bir xil image dev, staging va prod muhitlarida o'zgartirilmasdan ishlatiladi. Bu 12-factor app tamoyili bo'lib, secret'larni kod repository'dan chiqarib tashlash va rebuild'siz sozlamani o'zgartirish imkonini beradi.

**Spring'da qayerda uchraydi:** Spring'ning `Environment` va `PropertySource` abstraksiyasi, `@ConfigurationProperties` (type-safe binding, `@Validated` bilan), profile-specific `application-{profile}.yml`, `spring.config.import` (Boot 2.4+ dan) va `OS environment` relaxed binding. Markazlashtirilgan variantda `spring-cloud-config-server` (Git, Vault yoki JDBC backend) va client tomonda `spring-cloud-starter-config` + `spring.config.import=configserver:`; dinamik yangilash `@RefreshScope` va `/actuator/refresh` yoki Spring Cloud Bus (`spring-cloud-bus-kafka`) orqali. Alternativalar: `spring-cloud-starter-kubernetes-client-config` (ConfigMap/Secret), `spring-cloud-starter-vault-config`, Consul KV. Boot 3.x/4.x da Kubernetes'da ko'pincha Config Server o'rniga ConfigMap + env var yetarli bo'ladi.

**Qo'llanish keyslari:**
- Bitta Docker image'ni dev/staging/prod'da faqat environment variable almashtirib ishlatish.
- DB parol va API kalitlarni Vault yoki Kubernetes Secret'da saqlab, kod repo'ga umuman kiritmaslik.
- Feature flag va rate limit chegaralarini deploy qilmasdan, `@RefreshScope` bilan jonli o'zgartirish.
- Barcha service'lar uchun umumiy sozlamalarni Git repo'dagi `application.yml` da markazlashtirish va audit qilish.
- Incident vaqtida downstream timeout va retry qiymatlarini tezda kamaytirib tizimni barqarorlashtirish.

**Ehtiyot bo'ling:** Config server yagona nosozlik nuqtasiga aylanmasligi uchun client'da fail-fast va retry sozlanishi, startup paytdagi config'ni esa keshlab qo'yish kerak. `@RefreshScope` hamma narsani qayta yoqmaydi - connection pool, Kafka listener yoki `@Value` qotirilgan primitive'lar jonli yangilanmasligi mumkin, shuning uchun muhim o'zgarishlarda rolling restart'ga tayanganingiz xavfsizroq.

## 14.31 Service Shabloni (Service Template)

**Tavsif:** Chassis kutubxona bo'lsa, service template - to'liq ishga tushadigan skeleton loyiha: build fayli, CI/CD pipeline, Dockerfile, test strukturasi, lint qoidalari, observability sozlamalari va namunaviy endpoint bilan. Jamoa yangi service yaratganda template'ni generatsiya qiladi va bir necha daqiqada deploy qiladigan holatga keladi. Bu "golden path" boshdanoq to'g'ri qarorlarni standart qilib beradi va har bir jamoaning noldan boshlashini oldini oladi.

**Spring'da qayerda uchraydi:** Boshlang'ich nuqta - Spring Initializr (`start.spring.io`), uni tashkilot ichida o'zingiz host qilishingiz mumkin (`initializr-generator`, `initializr-web` modullari). Kengaytirilgan scaffolding uchun Backstage Software Templates, Cookiecutter, Yeoman, `mvn archetype:generate` (Maven archetype) yoki Gradle init plugin'i ishlatiladi; generatsiya qilingan loyiha odatda sizning chassis starter'ingizga (`com.company:company-service-starter`) bog'lanadi va Spring Boot BOM'ni `spring-boot-dependencies` / `spring-cloud-dependencies` orqali import qiladi. Template ichida `spring-boot-maven-plugin` (yoki `bootBuildImage` bilan Paketo buildpack), Testcontainers (`spring-boot-testcontainers`, `@ServiceConnection`), Spring Cloud Contract yoki Pact, Flyway/Liquibase migratsiyalari va `.github/workflows` pipeline'i bo'ladi.

**Qo'llanish keyslari:**
- Yangi jamoa yangi service'ni bir soat ichida CI/CD'siz qo'shimcha ishsiz production'ga chiqarishi.
- Barcha service'larda bir xil test piramidasi (unit + Testcontainers integration + contract test) ni standart qilish.
- Flyway migratsiya tartibi, Dockerfile va buildpack konfiguratsiyasini kompaniya bo'ylab birlashtirish.
- Backstage katalogi uchun `catalog-info.yaml` va ownership metadata'sini avtomatik yaratish.
- Security baseline (dependency scan, SBOM generatsiya, non-root container) ni har bir yangi service'ga meros qilib berish.

**Ehtiyot bo'ling:** Template bir marta generatsiya qilinadi, shuning uchun unda jiddiy kamchilik bo'lsa, u o'nlab repo'ga tarqab ketadi va keyin orqaga qaytarish qiyin - tez-tez o'zgaradigan qismlarni template'da emas, versiyalanadigan chassis starter'da ushlab turing. Shuningdek template "majburiy qolip" bo'lmasin: boshqa stack'ga haqiqatan ehtiyoj bo'lgan holatlar uchun chetga chiqish yo'li qoldirilsin.

## 14.32 Sidecar (Sidecar)

**Tavsif:** Yordamchi funksionallik asosiy ilova process'iga emas, balki u bilan bir xil deployment unit'da (Kubernetes'da bir pod'da) yonma-yon ishlaydigan alohida container'ga joylashtiriladi. Sidecar asosiy ilova bilan localhost va umumiy volume orqali gaplashadi, shuning uchun til va framework'dan mustaqil bo'ladi. Shu yo'l bilan log yig'ish, proxy, secret yangilash yoki config sync kabi vazifalar ilova kodiga tegmasdan qo'shiladi. Ayni paytda sidecar asosiy container bilan bir xil hayot tsiklini va resurs cheklovini bo'lishadi.

**Spring'da qayerda uchraydi:** Spring Boot ilovasi sidecar'ni bilmasligi mumkin, lekin integratsiya nuqtalari bor: strukturali log'ni stdout'ga chiqarish (Boot 3.4+ dagi `logging.structured.format.console=ecs|logstash|gelf`) va Fluent Bit/Vector sidecar'i uni yig'ishi; metrics'ni `/actuator/prometheus` orqali berish; `OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4318` bilan OpenTelemetry Collector sidecar'iga eksport qilish (`micrometer-tracing-bridge-otel` + `opentelemetry-exporter-otlp`). Graceful shutdown muhim: `server.shutdown=graceful` va `spring.lifecycle.timeout-per-shutdown-phase`. Polyglot holatda Spring Cloud Netflix'ning `spring-cloud-netflix-sidecar` moduli non-JVM service'ni Eureka'ga ro'yxatdan o'tkazish uchun ishlatilgan (hozir legacy). Kubernetes 1.29+ da sidecar'lar `initContainers` ichida `restartPolicy: Always` bilan e'lon qilinadi.

**Qo'llanish keyslari:**
- Fluent Bit sidecar'i bilan log'ni ilova kodiga tegmasdan markazlashtirilgan tizimga yuborish.
- OpenTelemetry Collector sidecar'ini qo'yib, tracing eksport sozlamalarini barcha service'larda bir xil qilish.
- Vault Agent Injector sidecar'i bilan secret'larni fayl ko'rinishida yangilab berish.
- Legacy non-Java service'ga TLS va retry'ni proxy sidecar orqali qo'shish.
- Database'ga ulanish uchun Cloud SQL Auth Proxy sidecar'ini ishlatish va ilovada oddiy localhost JDBC URL qoldirish.

**Ehtiyot bo'ling:** Sidecar asosiy container bilan CPU va memory'ni bo'lishadi - resource request/limit'ni to'g'ri bermasangiz, log agent ilovangizni OOMKill'ga olib keladi. Startup va shutdown tartibini ham hisobga oling: proxy sidecar ilovadan oldin tayyor bo'lishi va undan keyin to'xtashi kerak, aks holda deploy paytida qisqa muddatli xatolar paydo bo'ladi.

## 14.33 Ambassador (Ambassador)

**Tavsif:** Sidecar'ning ixtisoslashgan ko'rinishi: ilovaning tashqi dunyoga chiqadigan (outbound) chaqiruvlari local proxy orqali o'tadi va retry, timeout, circuit breaking, TLS, service discovery, authentication kabi tarmoq murakkabligi shu proxy'ga topshiriladi. Ilova esa oddiygina `http://localhost:port` ga murojaat qiladi va remote endpoint haqida hech narsa bilmaydi. Bu, ayniqsa, polyglot muhitda yoki legacy client'ga zamonaviy tarmoq siyosatlarini qo'shishda qulay.

**Spring'da qayerda uchraydi:** Spring tomonda bu "proxy'ga ishonib topshirish" degani: `WebClient`/`RestClient` base URL'ini `http://localhost:15001` yoki `http://localhost:8080` (local proxy) qilib qo'yish va resilience logikasini proxy'ga berish. Amaliy misollar: Envoy yoki HAProxy ambassador container'i, AWS App Mesh/Istio sidecar, Cloud SQL Auth Proxy, Redis yoki Kafka uchun local proxy. Agar resilience'ni ilova ichida qoldirsangiz, u holda Spring Cloud Circuit Breaker (`spring-cloud-starter-circuitbreaker-resilience4j`), `@CircuitBreaker`/`@Retry`/`@RateLimiter` annotatsiyalari va `spring-cloud-loadbalancer` ishlatiladi - ambassador aynan shu mas'uliyatni kod tashqarisiga ko'chiradi. Spring Cloud Gateway esa ichkariga kirish uchun (ingress), ambassador chiqish uchun (egress) ishlaydi.

**Qo'llanish keyslari:**
- Legacy Java 8 ilovasiga mTLS va zamonaviy retry siyosatini kod o'zgartirmasdan qo'shish.
- Managed database'ga xavfsiz, IAM asosidagi ulanishni local proxy orqali ta'minlash.
- Tashqi to'lov provayderiga chiqishda outbound rate limiting va audit log'ni markazlashtirish.
- Chaos testing: proxy darajasida latency yoki xato inject qilib service'ning chidamliligini sinash.
- Bir nechta tilda yozilgan service'larda bir xil egress siyosatini majburlash.

**Ehtiyot bo'ling:** Resilience logikasini ham proxy'da, ham ilovada takrorlasangiz, retry'lar ko'payib (retry amplification) downstream'ni yuklab qo'yadi - har bir mas'uliyat faqat bitta qatlamda bo'lsin. Yana bir tuzoq: proxy orqali o'tgan trafikda real client IP va error semantikasi o'zgarib, debug va observability chalkashadi, shuning uchun tracing header'lari uzatilishiga ishonch hosil qiling.

## 14.34 Service Mesh (Service Mesh)

**Tavsif:** Ambassador/sidecar yondashuvining platforma darajasidagi, markazlashtirilgan boshqaruvga ega shakli: har bir pod'ga data plane proxy qo'yiladi va ularning hammasi control plane orqali bir joydan sozlanadi. Mesh mTLS, service discovery, L7 routing, traffic splitting, retry, outlier detection, authorization policy va yagona telemetriyani ilova kodidan tashqarida ta'minlaydi. Natijada minglab service bo'ylab tarmoq siyosati deklarativ va auditga yaroqli bo'ladi. To'lovi - qo'shimcha infratuzilma murakkabligi va latency.

**Spring'da qayerda uchraydi:** Mesh (Istio, Linkerd, Consul Connect, AWS App Mesh) Spring ilovasidan deyarli mustaqil ishlaydi, lekin Spring tomonida bir nechta amaliy nuqta bor: client-side load balancing va circuit breaker'ni o'chirib, mesh'ga topshirish (`spring-cloud-loadbalancer`/Resilience4j'ni ikkilantirmaslik); `/actuator/health/liveness` va `/actuator/health/readiness` probe'larini to'g'ri ochish (`management.endpoint.health.probes.enabled=true`); tracing header'larini (W3C `traceparent`, B3) uzatish uchun Micrometer Tracing propagation'ni yoqish, aks holda mesh span'lari uzilib qoladi. Ko'p holatda mesh bilan Eureka/Config Server o'rniga Kubernetes Service DNS va ConfigMap ishlatiladi, ya'ni Spring Cloud Netflix stack'i soddalashadi.

**Qo'llanish keyslari:**
- Butun cluster bo'ylab service-to-service mTLS'ni ilova kodiga tegmasdan majburlash (zero trust).
- Canary va blue-green deploy'da trafikni 95/5 nisbatda deklarativ taqsimlash.
- Polyglot landscape'da (Java, Go, Python) bir xil retry/timeout siyosatini qo'llash.
- Har bir service juftligi orasidagi L7 metrics va service graph'ni avtomatik olish.
- Namespace'lar orasidagi ruxsatlarni authorization policy bilan cheklash (PCI zonasini izolyatsiya qilish).

**Ehtiyot bo'ling:** Mesh'ni kichik landscape'ga (masalan 5-10 service) kiritish ko'pincha foydadan ko'proq operatsion yuk keltiradi - control plane, sertifikat rotatsiyasi va upgrade'lar alohida jamoa ishini talab qiladi. Retry'ni mesh'da ham, Resilience4j'da ham yoqib qo'yish klassik xato: natijada bitta so'rov downstream'da o'nlab chaqiruvga aylanadi.

## 14.35 Aggregator, Proxy, Chained va Branch microservice patternlari (Aggregator / Proxy / Chained / Branch Microservice Patterns)

**Tavsif:** Bu - bir nechta service'dan javob yig'ishning to'rtta tipik kompozitsiya shakli. Aggregator bir nechta service'ni (ideal holda parallel) chaqirib natijalarni birlashtiradi; Proxy hech qanday birlashtirmasdan faqat yo'naltiradi va formatni moslashtiradi; Chained ketma-ket chaqiruvlar zanjirini qurib, har bir qadam oldingisining natijasiga tayanadi; Branch esa shartga qarab bir yoki bir nechta mustaqil tarmoqni (shu jumladan ichma-ich zanjirlarni) tanlab chaqiradi. To'g'ri shaklni tanlash javob latency'si va coupling darajasini bevosita belgilaydi.

**Spring'da qayerda uchraydi:** Aggregator - `WebClient` + `Mono.zip`/`Flux.merge` (reactive) yoki `RestClient` bilan Java 21+ virtual thread'da `ExecutorService.invokeAll`, hamda `StructuredTaskScope` (JEP 505, Java 25 da standart) orqali parallel chaqiruv. Proxy - Spring Cloud Gateway route'i yoki `@HttpExchange` interface client'i bilan oddiy forwarding. Chained - bir controller ichida `flatMap` zanjiri (`a().flatMap(this::b).flatMap(this::c)`), bu sinxron blocking zanjir bo'lsa latency qo'shiladi. Branch - `switch`/strategy bean'lari (`Map<String, PricingStrategy>` injection) yoki Spring Integration `RouterSpec`/`@Router` bilan. Har uchala holatda Resilience4j `@TimeLimiter`/`@CircuitBreaker` va `ObservationRegistry` bilan tracing qo'shiladi.

```java
Mono<Dashboard> load(String id) {
    return Mono.zip(
            orders.get(id).onErrorReturn(Orders.empty()),
            profile.get(id),
            loyalty.get(id).onErrorReturn(Loyalty.none()))
        .map(t -> new Dashboard(t.getT2(), t.getT1(), t.getT3()))
        .timeout(Duration.ofMillis(800));
}
```

**Qo'llanish keyslari:**
- Mijoz dashboard'ini order, profile va loyalty service'laridan parallel yig'ish (aggregator).
- Legacy SOAP service'ni REST fasadga o'rab, client'larni o'zgartirmasdan migratsiya qilish (proxy).
- Buyurtma yaratish oqimida inventory tekshiruvi natijasiga qarab pricing chaqirish (chained).
- Mijoz segmentiga qarab turli narx yoki chegirma service'ini tanlash (branch).
- Hisobot uchun bir nechta bo'lim service'idan ma'lumot olib birlashtirgan read-only endpoint.

**Ehtiyot bo'ling:** Chained zanjir uzayganda latency va nosozlik ehtimoli ko'payadi (har bir qadam 99.9% available bo'lsa ham, 5 qadam 99.5% ga tushadi) - zanjirni event-driven yoki parallel aggregator ko'rinishiga aylantirishni ko'rib chiqing. Aggregator'da timeout va fallback bo'lmasa, eng sekin downstream butun javobni ushlab turadi; har bir chaqiruvga alohida timeout va qisman (partial) javob strategiyasi qo'ying.

## 14.36 Shared Library bog'liqligi (Shared Library Coupling) - antipattern

**Tavsif:** Bu antipattern'da service'lar o'rtasida domain model, DTO, entity yoki business qoidalar umumiy kutubxona orqali bo'lishiladi va har bir o'zgarish barcha iste'molchilarni bir vaqtda yangilashga majbur qiladi. Natijada mustaqil deploy qilish imkoniyati - microservice'larning asosiy foydasi - yo'qoladi: bitta field qo'shish uchun o'nlab repo'da versiya ko'tarish va koordinatsiyalangan release kerak bo'ladi. Umumiy kutubxonaning o'zi yomon emas, muammo uning *domain* va *shartnoma* bilan bog'liq qismlarida.

**Spring'da qayerda uchraydi:** Tipik ko'rinishi - `company-common-domain` yoki `company-shared-entities` moduli ichida JPA `@Entity` sinflari va DTO'lar bo'lib, uni 15 ta service'ga Maven dependency qilib qo'shish. Shuningdek `spring-boot-dependencies` BOM'ini shared kutubxona majburan qotirib qo'yishi, Spring Boot versiyasini mustaqil ko'tarishni bloklaydi. To'g'ri yondashuv: shartnomani kod emas, schema bilan ulashish - OpenAPI spec'dan client generatsiya (`openapi-generator-maven-plugin`), Avro/Protobuf schema registry, Spring Cloud Contract (`spring-cloud-starter-contract-verifier`) yoki Pact; umumiy kutubxonada esa faqat barqaror texnik utilitalar (logging format, tracing filter, `ProblemDetail` handler) qoldirilib, ular `@AutoConfiguration` starter sifatida versiyalanadi.

**Qo'llanish keyslari:**
- Tashxis: bitta DTO o'zgarishi uchun 10 ta repo'da versiya ko'tarish zarurati sezilgan holat.
- Shared entity kutubxonasini har bir service'ning o'z local model'iga ajratib chiqish (migratsiya rejasi).
- Domain class'lar o'rniga OpenAPI/Avro schema asosida generatsiya qilingan client'ga o'tish.
- Shared kutubxonani faqat texnik chassis starter'iga qisqartirish va domain qismini o'chirish.
- Contract test (Spring Cloud Contract/Pact) joriy qilib, umumiy kod o'rniga shartnomani tekshirish.

**Ehtiyot bo'ling:** "Kod takrorlanmasin" degan niyat bilan domain model'ni ulashish - microservice'da DRY prinsipi coupling'dan muhimroq emas; biroz dublikat kod mustaqil deploy'dan arzonroq turadi. Agar shared kutubxona qolsa, uning backward-compatible versiyalash siyosatini va bir necha major versiyani parallel qo'llab-quvvatlash majburiyatini oldindan belgilang.

## 14.37 Taqsimlangan monolit (Distributed Monolith) - antipattern

**Tavsif:** Tizim tashqi ko'rinishda microservice'lardan iborat, lekin service'lar shunchalik qattiq bog'langan ki, ularni mustaqil deploy qilish, test qilish yoki scale qilish mumkin emas. Belgilari: har bir release'da barcha service'ni birga chiqarish, sinxron chaqiruvlarning uzun zanjirlari, umumiy database schema, shared domain kutubxona va bitta service to'xtasa butun tizimning ishdan chiqishi. Natija - monolitning barcha coupling muammolari ustiga taqsimlangan tizimning tarmoq, latency va debug murakkabligi qo'shiladi. Bu ko'pincha monolitni domain chegaralarini tahlil qilmasdan, texnik qatlamlar bo'yicha bo'lish natijasida paydo bo'ladi.

**Spring'da qayerda uchraydi:** Amalda bu ko'rinadi: bir nechta Spring Boot ilovasi bitta `DataSource` va bitta schema'ga ulangan (`spring.datasource.url` bir xil), shared `@Entity` kutubxonasi, `@FeignClient` yoki `RestClient` bilan 4-5 qadamli sinxron chaqiruv zanjiri, va service'lararo distributed transaction urinishlari (JTA/XA). Davolash yo'llari Spring ekosistemasida mavjud: domain chegaralarini `spring-modulith` bilan monolit ichida aniqlab, keyin ajratish (`ApplicationModuleTest`, `@ApplicationModuleListener`); sinxron zanjirni Kafka/RabbitMQ event'lariga o'tkazish (`spring-kafka`, `@KafkaListener`, transactional outbox); har bir service'ga o'z schema'si va o'z Flyway migratsiyalari; shartnomani Spring Cloud Contract bilan qotirish.

**Qo'llanish keyslari:**
- Tashxis: oxirgi 10 release'ning hammasi "hamma service'ni birga chiqarish" bo'lgan holatni aniqlash.
- Umumiy database'ni service'lar bo'yicha schema'ga ajratish va cross-schema join'larni yo'q qilish.
- Sinxron chaqiruv zanjirini event-driven oqimga (outbox + Kafka) aylantirish.
- Spring Modulith bilan modulli monolitga qaytib, chegaralarni aniqlagandan keyin qayta ajratish.
- Release coupling metrikasini (bir service'ni yakka deploy qilish mumkinmi?) KPI sifatida kuzatish.

**Ehtiyot bo'ling:** Eng xatarli xato - muammoni "yana ko'proq microservice qilib" hal qilishga urinish; chegaralar noto'g'ri bo'lsa, bo'lish faqat coupling nuqtalarini ko'paytiradi. Ko'p holatda to'g'ri yo'l - avval modulli monolit (Spring Modulith) bilan chegaralarni to'g'rilash, keyin haqiqatan mustaqil bo'lgan qismlarni ajratish.

## 14.38 Nano-service'lar (Nano-services) - antipattern

**Tavsif:** Service'lar shunchalik mayda bo'linadi ki, har biri bir-ikki funksiyadan iborat bo'lib, o'z-o'zidan hech qanday mustaqil business qiymat bermaydi. Bitta oddiy use case bajarilishi uchun o'nlab service chaqirilishi kerak bo'ladi, shu sababli latency, operatsion yuk (deployment, monitoring, on-call, CI pipeline) va kognitiv murakkablik service'lar sonidan kelib chiqib o'sadi. Infratuzilma overhead'i (container, sidecar, observability, release) har bir service uchun deyarli bir xil bo'lgani uchun juda mayda service'larda bu overhead foydali ishdan ko'p bo'ladi.

**Spring'da qayerda uchraydi:** Belgisi - har biri 1-2 `@RestController` metodidan iborat o'nlab Spring Boot ilovasi, har birining o'z repo'si, Dockerfile'i va pipeline'i; `@FeignClient` chaqiruvlari grafigi dasturchi uchun kuzatib bo'lmas holga keladi. To'g'ri yechimlar: bir nechta mayda service'ni bitta bounded context ichidagi Spring Boot ilovasiga birlashtirish va ichida `spring-modulith` modullari sifatida ajratib ushlab turish; haqiqatan juda mayda, kamdan-kam ishlaydigan vazifalar uchun esa alohida service o'rniga serverless funksiya ishlatish (`spring-cloud-function`, `spring-cloud-function-adapter-aws`, GraalVM native image bilan `spring-boot-starter-parent` + `native` profile). Mustaqil scale talab qilinmaydigan kod - bu alohida service uchun sabab emas.

**Qo'llanish keyslari:**
- Tashxis: bitta checkout oqimida 12 ta ichki HTTP chaqiruv borligini tracing'da aniqlash.
- Bir nechta "mayda" service'ni bitta bounded context service'iga birlashtirish (Spring Modulith moduli sifatida).
- Kamdan-kam ishlaydigan konvertor yoki notifikator vazifalarini serverless funksiyaga ko'chirish.
- On-call yukini kamaytirish uchun egasiz, bir endpoint'li service'larni konsolidatsiya qilish.
- Yangi service ochish uchun aniq mezon (granularity checklist) ni joriy qilish.

**Ehtiyot bo'ling:** "Single Responsibility Principle" ni service darajasiga mexanik ko'chirish - asosiy sabab: SRP sinf uchun, service chegarasi esa bounded context va mustaqil o'zgarish sababi uchun. Konsolidatsiya qilayotganda ham ortiqcha narigi tomonga o'tib ketmang: biznes jihatdan turli tezlikda o'zgaradigan va turlicha scale talab qiladigan qismlarni zo'rlab bitta service'ga tiqish distributed monolit yoki bottleneck'ga olib keladi.

## 14.39 Service granularligi bo'yicha qaror (Service Granularity Decision)

**Tavsif:** Service chegarasini qancha mayda yoki yirik olish - microservice arxitekturasining eng qimmat va eng qaytarib bo'lmas qarori. Qarorni "qancha qatorlik kod" bilan emas, aniq kuchlar (granularity drivers) bilan o'lchash kerak: o'zgarish sabablari (bounded context), mustaqil scale ehtiyoji, fault isolation, turli xavfsizlik/compliance talablari, jamoa egaligi va release tezligi. Ularga qarshi kuchlar ham bor: data bog'liqligi, transaction integrity va service'lararo chaqiruvlar soni. Amalda yirikdan boshlab (modulli monolit yoki yirik service) kerakli joydan bo'lish - teskarisidan arzonroq va xatolarga chidamliroq.

**Spring'da qayerda uchraydi:** Spring Modulith (`spring-modulith-starter-core`) aynan shu qaror uchun qurilgan: `@ApplicationModule` bilan modul chegarasi e'lon qilinadi, `ApplicationModules.of(App.class).verify()` test'i chegara buzilishini CI'da ushlaydi, `spring-modulith-docs` (`Documenter`) modul diagrammasini generatsiya qiladi, `@ApplicationModuleListener` esa modullararo aloqani event'ga o'tkazadi - keyinchalik o'sha event'ni Kafka'ga chiqarish arzon bo'ladi. Shuningdek `spring-modulith-events-jpa`/`-jdbc` transactional outbox (`EventPublicationRegistry`) beradi, bu ajratishdan keyin ham ishlaydi. Bog'liqlik tahlili uchun ArchUnit, jQAssistant yoki `jdeps`; chaqiruv grafini o'lchash uchun Micrometer Tracing + Zipkin/Tempo service graph'i foydali.

**Qo'llanish keyslari:**
- Monolitni ajratishdan oldin Spring Modulith bilan chegaralarni tasdiqlab, keyin faqat tasdiqlangan modulni ajratish.
- Black Friday'da faqat catalog va pricing'ni mustaqil scale qilish zarurati bo'lgani uchun ularni ajratish.
- PCI DSS skopini kichraytirish uchun to'lov qismini alohida, qattiq izolyatsiyalangan service'ga chiqarish.
- Ikki jamoa bir modul ustida doimiy konflikt qilayotgani uchun chegarani jamoa egaligiga moslab bo'lish.
- Tracing ma'lumotiga tayanib, o'ta chatty bo'lgan ikki service'ni qayta birlashtirish (merge) qarorini qabul qilish.

**Ehtiyot bo'ling:** Chegarani texnik qatlam (controller-service-repository) yoki ma'lumotlar jadvali bo'yicha emas, business capability bo'yicha torting - jadval asosidagi bo'linish deyarli har doim distributed monolitga olib keladi. Qarorni bir martalik va abadiy deb qaramang: granularlikni vaqti-vaqti bilan release coupling, latency va incident ma'lumotlari asosida qayta ko'rib chiqing, va ajratishdan avval ma'lumot egaligi (data ownership) masalasini hal qilmasdan boshlamang.

---

[&larr; 13. Domain-Driven Design patternlari](13-domain-driven-design-patternlari.md) · [Mundarija](README.md) · [15. Enterprise Integration Patterns I: xabarlar, kanallar, marshrutlash &rarr;](15-enterprise-integration-patterns-i-xabarlar.md)
