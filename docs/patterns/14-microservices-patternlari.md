<!-- doc: patterns | chapter: 14 | part:  -->

[Barcha hujjatlar](../../README.md) / [Dizayn patternlar](README.md)

> Holat: tekshirilgan (2026-10-19). Manbalar bob oxirida.

# 14. Microservices patternlari (Microservices Patterns)

<details>
<summary>Bu bobdagi 48 bo'lim</summary>

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
- [14.40 Saga da izolyatsiya yo'q: anomaliyalar va qarshi choralar](#1440-saga-da-izolyatsiya-yoq-anomaliyalar-va-qarshi-choralar)
- [14.41 Tilga xos paketlash formati (Language-specific Packaging Format)](#1441-tilga-xos-paketlash-formati-language-specific-packaging-format)
- [14.42 Saga ning sakkiz varianti: uch o'lchamli tanlov (Transactional Saga Patterns)](#1442-saga-ning-sakkiz-varianti-uch-olchamli-tanlov-transactional-saga-patterns)
- [14.43 Oqim holatini kontraktda uzatish: stamp coupling (Stamp Coupling for Workflow Management)](#1443-oqim-holatini-kontraktda-uzatish-stamp-coupling-stamp-coupling-for-workflow-management)
- [14.44 Granularlik chegaralarining o'lchanadigan qoidalari](#1444-granularlik-chegaralarining-olchanadigan-qoidalari)
- [14.45 Saga amaliyoti: qadam tartibi va orkestrator egaligi](#1445-saga-amaliyoti-qadam-tartibi-va-orkestrator-egaligi)
- [14.46 Saga nimani hal qiladi va nima qilmaydi](#1446-saga-nimani-hal-qiladi-va-nima-qilmaydi)
- [14.47 Bir nechta jamoa bitta servisga muhtoj bo'lganda](#1447-bir-nechta-jamoa-bitta-servisga-muhtoj-bolganda)
- [14.48 Amalda qo'llash](#1448-amalda-qollash)

</details>



Mikroservis patternlari - bu bitta deployment birligiga sig'maydigan tizimni mustaqil ishlab chiqiladigan, mustaqil deploy qilinadigan va mustaqil masshtablanadigan servislarga bo'lish hamda ularni bir-biri bilan ishonchli bog'lash bo'yicha takrorlanuvchi yechimlar to'plami. Monolitda bitta `@Transactional` metod va bitta ma'lumotlar bazasi hal qilgan muammolar (atomarlik, join'lar, refactoring) tarqatilgan tizimda tamomila boshqa narxga ega bo'ladi - shuning uchun arxitektor uchun bu patternlar "moda" emas, balki tanlov narxini ongli boshqarish vositasi. Bu bo'limdagi patternlar uch guruhga bo'linadi: dekompozitsiya (qanday bo'lish kerak), ma'lumotlar izchilligi (saga, outbox, event'lar) va so'rovlarni birlashtirish (API composition). Spring ekotizimida bu patternlarning deyarli har biri uchun tayyor modul bor - Spring Boot 3.x/4.x, Spring Cloud, Spring Modulith, Spring for Apache Kafka - lekin pattern tanlashdagi xatoni hech qanday kutubxona tuzatib bermaydi.

## 14.1 Monolitik arxitektura va mikroservis arxitekturasi qarori (Monolithic Architecture vs Microservice Architecture (decision))

**Tavsif:** Bu pattern emas, balki boshlang'ich arxitektura qarori: tizim bitta deployment birligi bo'lib qoladimi yoki mustaqil deploy qilinadigan servislarga bo'linadimi. Monolit oddiy: bitta build, bitta tranzaksiya, bitta ma'lumotlar bazasi, refactoring kompilyator yordamida amalga oshadi; lekin jamoa va kod bazasi o'sgach, release'lar bir-birini bloklay boshlaydi va modullar orasidagi chegaralar yemiriladi. Mikroservislar mustaqil release, texnologiya tanlash erkinligi va alohida masshtablash beradi, biroq tarmoq, eventual consistency, tarqatilgan tracing va infratuzilma narxini qo'shadi. Amaliy javob ko'pincha "modular monolit" dan boshlash va chegaralar barqarorlashgach ajratishdir.

Qarorni aniqlashtiradigan vosita - masshtab kubining uch o'qi. X o'qi: ilovaning bir xil nusxalarini ko'paytirib yuk balansi orqasiga qo'yish. Z o'qi: so'rovni uning atributi bo'yicha bo'lib (mijoz identifikatori, tenant, geografiya) har bo'lakni o'z nusxasiga yuborish. Ikkisi ham hajm muammosini hal qiladi va ikkisi ham arzon, lekin ikkisi ham murakkablik muammosini hal qilmaydi: kod bazasi, build va release hamon bitta, har nusxa butun ilovani olib yuradi va har o'zgarish butun ilovani qayta deploy qilishni talab qiladi. Faqat Y o'qi, ya'ni funksional dekompozitsiya, murakkablikka javob beradi: ilova vazifasi bo'yicha mustaqil servislarga bo'linadi. Shuning uchun "yuk ko'tarmayapti" degan muammo odatda mikroservisga o'tish sababi emas (X va Z o'qi arzonroq); mikroservisga o'tish sababi "jamoalar bir-birini bloklayapti va kod bazasini hech kim tushunmaydi" bo'ladi. Ma'lumot darajasidagi X va Z o'qi [partitioning va replikatsiya](../architect/26-partitioning-replikatsiya-va-katta-hajm.md#261-jadval-qachon-katta-hisoblanadi-qaror-uchun-raqamlar) mavzusiga tegishli.

**Spring'da qayerda uchraydi:** Monolit tomoni - bitta Spring Boot 3.x ilovasi, `spring-boot-starter-web`, Spring Data JPA va `@Transactional`. Modular monolit uchun Spring Modulith: `@ApplicationModule`, `ApplicationModules.of(App.class).verify()` testda modul chegaralarini buzilishidan saqlaydi, `@ApplicationModuleListener` modullar orasini event bilan bo'shashtiradi, `spring-modulith-starter-jpa` va `spring-modulith-docs` hujjat/diagramma chiqaradi. Mikroservis tomoni - ko'p Spring Boot ilovasi, Spring Cloud Gateway, Spring Cloud Config, Spring Cloud OpenFeign yoki `RestClient`, Micrometer Tracing va `spring-boot-starter-actuator`. `spring.threads.virtual.enabled=true` (Java 21+) I/O ga bog'liq servislarda thread narxini sezilarli kamaytiradi.

**Qo'llanish keyslari:**
- Startap MVP: bitta Spring Boot monolit, lekin Spring Modulith bilan modul chegaralari testdan o'tkaziladi.
- 50+ injener va kuniga bir necha release kerak bo'lgan to'lov platformasi mikroservislarga ajratiladi.
- Hisobot va ML inference qismi asosiy ilovadan bir necha barobar ko'proq CPU talab qilsa, faqat shu qism alohida servis qilinadi.
- Legacy monolitni butunlay yozmasdan, eng tez o'zgaradigan domen (masalan, narxlash) birinchi mikroservis sifatida ajratiladi.
- Regulyator talabi bilan kartalar ma'lumoti alohida compliance zonasida ishlashi kerak bo'lgan tizim.

**Qarordan oldingi uch savol.** Newman tashkilot bilan ishlaganda har doim bir xil uch savolni beradi va ko'p holda shu uch savolning o'zi kompaniyani qaytadan o'ylashga majbur qiladi: (1) **nimaga erishmoqchisiz** - javob biznes maqsadiga bog'langan natijalar to'plami bo'lishi va tizimning oxirgi foydalanuvchisiga keltiradigan foydasi bilan tushuntirilishi kerak; (2) **mikroservisga muqobil yo'llarni ko'rdingizmi** - bir xil foydaning ko'pini ancha oson va "zerikarli" usul bilan olish mumkin, ko'rmagan bo'lsangiz nega ko'rmaganingizni ayting; (3) **o'tish ishlayotganini qanday bilasiz** - yo'nalish to'g'riligini qanday o'lchaysiz. Uchinchi savolga javobi bo'lmagan migratsiya qorong'ida qo'l bilan izlashdan farq qilmaydi.

**Mijoz o'rnatadigan dasturda mikroservis tanlanmaydi.** Agar dastur paketlanib mijozga yuborilsa va mijoz uni o'zi ishlatsa, mikroservis odatda yomon tanlov: migratsiya murakkablikning katta qismini operatsion sohaga suradi, operatsion soha esa bu yerda mijozning qo'lida. Monolitni mijoz tanish mexanizm bilan oladi ("Windows 2016 Server kerak" kabi aniq platforma, tanish o'rnatuvchi paket), bir jarayon o'rniga 10-20 jarayon yoki Kubernetes klasteri talab qilish esa mijozda yo'q ko'nikma va platformani talab qiladi. Mijozda Kubernetes bo'lsa ham, u sizdagi Kubernetes emas - o'rnatmalar orasidagi farq katta.

**Xarajatni kamaytirish maqsad bo'lsa mikroservis yomon tanlov.** Newman buni alohida ajratib aytadi: qisqa muddatda xarajat deyarli har doim oshadi, chunki ko'proq jarayon, ko'proq mashina, ko'proq tarmoq, ko'proq saqlash va ko'proq litsenziyalanadigan yordamchi dastur ishlatiladi; bundan tashqari jamoaga kiritilgan har qanday o'zgarish qisqa muddatda tezlikni pasaytiradi, ya'ni yoki yangi funksiya sekinlashadi yoki shu narxni yopish uchun odam qo'shiladi. IT ni daromad manbasi emas, xarajat markazi deb ko'radigan tashkilotda bu mentalitet arxitekturadan foyda olishga doimiy tormoz bo'ladi. Mikroservis pul topishga yordam berishi mumkin - ko'proq mijozga yetib borish yoki funksiyalarni parallel ishlab chiqish orqali; pulni tejashga esa yo'q.

**Ehtiyot bo'ling:** Domen chegaralari hali aniq bo'lmaganda mikroservislarga bo'lish eng qimmat xato - har bir refactoring API versiyalash, migratsiya va koordinatsiyaga aylanadi ("distributed monolith"). Jamoa CI/CD, observability va on-call madaniyatiga tayyor bo'lmasa, mikroservislar tezlikni oshirmaydi, balki kamaytiradi.

```text
Qaror jadvali (har qatorga loyihadan javob yoziladi):

  Jamoa soni          1-2 -> monolit         5+ -> ajratish mumkin
  Reliz chastotasi    haftada 1 -> monolit   kuniga ko'p -> ajratish
  Chegara aniqligi    noma'lum -> monolit    barqaror -> ajratish
  Operatsion yetuklik CI yo'q -> monolit     kuzatuvchanlik bor -> ajratish
  Masshtab talabi     bir xil -> monolit     qismlarga har xil -> ajratish

Modular monolit ko'pincha to'g'ri birinchi qadam: chegara kodda qo'yiladi
(Spring Modulith `verify()`), tarmoq esa keyin qo'shiladi.
Microservice hisobi: har servis uchun CI, deploy, monitoring va on-call.
```

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

**Nomzodni topishning uchta signali:** imkoniyat xaritasi tayyor bo'lmasa, Carnell domen suhbatining o'zidan chiqadigan uchta signalni beradi (Carnell, 2-bob, 39-bet):

- **Otlarni sanash.** Muammoni ovoz chiqarib tasvirlab, qaytarilib keladigan otlarni yozib boring. Takrorlangan ot ko'pincha o'zak biznes domenini va servis nomzodini ko'rsatadi: `contract`, `license`, `asset`.
- **Fe'llarga qarash.** Fe'l harakat chegarasini ochadi. "Bu tranzaksiya ma'lumotni A dan ham, B dan ham oladi" degan gap eshitilsa, bitta emas, bir nechta servis ishtirok etadi va ikkisi orasidagi o'zaro ta'sir keyinchalik servis interfeysiga aylanadi.
- **Ma'lumot yaxlitligi (data cohesion).** Suhbat davomida o'qilayotgan yoki yangilanayotgan ma'lumot birdan butunlay boshqa narsaga aylansa, bu yangi servis nomzodi: har bir servis o'z ma'lumotiga to'liq egalik qiladi.

Uchinchi signal jadvallarning GURUHINI (bitta mantiqiy entity) ko'rsatadi, jadvalning o'zini chegara qilib olishni emas. Ikkisini ajratadigan shart shu bobdagi [service granularligi bo'yicha qaror](#1439-service-granularligi-boyicha-qaror-service-granularity-decision) bo'limida yozilgan.

**Dekompozitsiyadan keyingi qadam - servis API larini aniqlash.** Richardson da servislar ro'yxati oxirgi natija emas: undan keyin har bir servisning operatsiyalari va hodisalari belgilanadi. Avval har bir tizim operatsiyasi bitta servisga biriktiriladi va bu biriktirish har doim ravshan bo'lmaydi. Kitobdagi misol: `noteUpdatedLocation()` kuryer joylashuvini yangilaydi - nomiga ko'ra Courier servisiga tegishli, lekin joylashuv Delivery servisiga kerak, shuning uchun operatsiya ma'lumot KERAK bo'lgan servisga biriktiriladi. Boshqa holatlarda teskari qoida ishlaydi: operatsiyani bajarish uchun kerakli ma'lumotga EGA servis tanlanadi. Keyin har bir operatsiya uchun "bu servis yolg'iz bajara oladimi" savoli beriladi; bajara olmasa, hamkorlik uchun qanday servislararo operatsiya va hodisa kerakligi aniqlanadi. Shunday paydo bo'ladigan ikkinchi toifa operatsiyalar faqat boshqa servislar tomonidan chaqiriladi va tashqi klientga ko'rinmaydi.

```yaml
services:
  - name: order-management     # buyurtma qabul qilish va kuzatish
  - name: payment-processing   # to'lov yig'ish va qaytarish
  - name: inventory            # zaxira hisobi
  - name: shipping             # yetkazib berish

# Texnik bo'linishdan farqi: `order-api`, `order-worker`, `order-db-service`
# imkoniyat emas, bitta imkoniyatning qatlamlari.
# Tekshiruv: har servis nomi biznes rahbariga tushunarli bo'lishi kerak.
```

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

```yaml
contexts:
  sales:    {aggregates: [Order, Quote],     ubiquitous: "buyurtma, taklif"}
  billing:  {aggregates: [Invoice, Payment], ubiquitous: "hisob-faktura"}
  shipping: {aggregates: [Shipment, Parcel], ubiquitous: "jo'natma"}

# Bir xil so'z ikki kontekstda boshqa narsani bildiradi: sales dagi
# "Customer" va billing dagi "Customer" bitta jadval bo'lishi shart emas.
# Shuning uchun chegara DDD kontekst chegarasi bilan mos tushadi.
```

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

```java
// Self-contained service: tashqi sinxron chaqiruvga tayanmaydi
@Service
public class ShippingService {
    private final RateCache localRates;        // nusxa lokal saqlanadi

    public ShippingQuote quote(Parcel p) {
        // Tashqi servisni so'rov vaqtida chaqirmaydi: ma'lumot oldindan
        // hodisa orqali kelib, lokal nusxada turadi
        return localRates.quote(p);
    }

    @KafkaListener(topics = "pricing.rates.updated")
    void onRatesUpdated(RatesUpdated e) { localRates.replace(e.rates()); }
}
// Natija: Pricing yiqilsa Shipping ishlashda davom etadi.
// Narxi: ma'lumot nusxalanadi va qisqa vaqt eskirgan bo'ladi.
```

## 14.5 Har bir jamoaga bitta servis (Service per Team)

**Tavsif:** Servis chegarasi jamoa chegarasiga mos qilinadi: bitta jamoa servisni to'liq egalik qiladi - kod, ma'lumotlar bazasi, deploy, on-call va SLA. Bu Conway qonunini ongli boshqarish usuli: koordinatsiya narxi eng qimmat resurs bo'lgani uchun, servislar jamoalar mustaqil release qila oladigan tarzda chizilaadi. Bitta jamoa bir nechta servisga egalik qilishi mumkin, lekin bitta servisga ikki jamoa egalik qilmasligi kerak.

**Spring'da qayerda uchraydi:** Har bir jamoa alohida repozitoriya va alohida Spring Boot 3.x/4.x ilovasini yuritadi; umumiy standart `spring-boot-starter-parent` yoki ichki "platform BOM" va kompaniya ichidagi custom starter (`*-spring-boot-starter` + `@AutoConfiguration`, `META-INF/spring/org.springframework.boot.autoconfigure.AutoConfiguration.imports`) orqali tarqatiladi. Jamoalararo API shartnomasi Spring Cloud Contract (`Contract.make { ... }`, `@AutoConfigureStubRunner`) va OpenAPI bilan mustahkamlanadi. Servis egaligi metadata'si `spring-boot-starter-actuator` ning `/actuator/info` va `build-info`/`git-info` orqali ko'rsatiladi; integratsiya testlari Testcontainers va `@ServiceConnection` bilan jamoa ichida mustaqil ishlaydi.

**Qo'llanish keyslari:**
- Payments jamoasi payment-service va payment-webhook-service'ni to'liq o'zi deploy qiladi.
- Platform jamoasi umumiy auth starter'ini yozadi, lekin biznes servislarga tegmaydi.
- Yangi jamoa qo'shilganda unga aniq bounded context va alohida servis beriladi.
- On-call rotatsiyasi servis bo'yicha tuziladi - alert to'g'ridan-to'g'ri egasiga boradi.
- Release train'dan voz kechib, har bir jamoa kuniga mustaqil deploy qila boshlaydi.

**Kuchli va jamoaviy egalik.** "Egalik" so'zi ikki xil rejimni yashiradi va ikkisining avtonomiyaga ta'siri boshqa.

- **Kuchli egalik (strong ownership).** Servis bitta jamoaga tegishli va unga qanday o'zgarish kiritilishini shu jamoa hal qiladi. Tashqi jamoa o'zgarish kerak bo'lsa egadan so'raydi yoki PR yuboradi, PR qanday shartlarda qabul qilinishini esa yana ega jamoa belgilaydi. Bitta jamoa bir nechta servisga ega bo'lishi mumkin. Kuchli egalik faqat kod o'zgarishi bilan cheklanmaydi: jamoa kod standarti, idiomalar, qachon deploy qilish, qanday texnologiya ishlatish va deploy platformasi haqida ham o'zi qaror qabul qiladi. Bu pattern aynan avtonomiyani maksimallashtirish uchun mavjud.
- **Jamoaviy egalik (collective ownership).** Istalgan jamoa istalgan servisni o'zgartiradi. Jamoalar bir-birining yo'lini to'smasligi uchun ehtiyotkor koordinatsiya kerak bo'ladi, ya'ni avtonomiya aynan koordinatsiya hisobiga pasayadi.

Kuchli egalik lokal xilma-xillikka ruxsat beradi, lekin ruxsat cheksiz emas: faqat jamoa ichida ta'sir qiladigan tanlov (masalan Java ni funksional uslubda yozish) erkin, boshqalarga ta'sir qiladigan tanlov esa muvofiqlashtirishni talab qiladi - hamma REST-over-HTTP ishlatganda bitta jamoaning gRPC endpoint chiqarishi iste'molchilarga muammo keltiradi. Qoida: qarorning radiusi jamoa chegarasidan chiqsa, qaror ham jamoa chegarasidan chiqadi.

**Teskari Conway qonuni.** Odatda tashkilot tuzilishi tizim dizaynini shakllantiradi deyiladi; Newman teskari yo'nalishni ham kuzatgan, lekin uni dalil sifatida emas, anekdot sifatida beradi (teskari ta'sirga Conway qonunining o'zi darajasidagi dalil topilmagan). Misoli: bir vaqtlar kichik veb-sayti bo'lgan yirik bosma nashr kompaniyasida sayt uch qismdan (kirish, yadro, chiqish) tuzilgan va bu bo'linish o'sha paytdagi tasodifiy texnik qarordan chiqqan edi; yillar o'tib IT tarafda aynan shu uch qismga mos uch kanal va alohida jamoalar paydo bo'lgani ma'lum bo'ldi - tashkiliy tuzilma dizayndan OLDIN mavjud emas, uning atrofida o'sgan edi. Natijasi amaliy: dizayn eskirganda uni o'zgartirish uchun tashkiliy tuzilmani ham o'zgartirish kerak bo'ladi va bu yillar oladi.

**Ehtiyot bo'ling:** Reorganizatsiyada jamoalar o'zgaradi, servis chegarasi esa oson o'zgarmaydi - shuning uchun jamoa strukturasini domen chegarasiga moslashtirish, teskarisi emas, to'g'ri yo'l. Teskari Conway kuzatuvi bunga zid emas, uni shartlaydi: tashkilot allaqachon eski dizayn atrofida o'sgan bo'lsa, yangi chegaralarga o'tish tashkiliy o'zgarishni ham talab qiladi, ya'ni "jamoani domenga moslash" bir martalik emas, migratsiyaning bir qismi. "Hamma hamma joyni o'zgartira oladi" degan madaniyatda bu pattern faqat qog'ozda qoladi va egasiz servislar paydo bo'ladi.

```yaml
teams:
  checkout:  {services: [order-management],   oncall: true, repo: orders}
  payments:  {services: [payment-processing], oncall: true, repo: payments}
  logistics: {services: [shipping, inventory], oncall: true, repo: logistics}

# Qoida: bitta servisning egasi bitta jamoa. Ikki jamoa bitta servisga
# yozsa, reliz muvofiqlashtirish kerak bo'ladi va mustaqillik yo'qoladi.
# Teskari holat ham yomon: bitta jamoa 15 servis - operatsion yuk ortadi.
```

## 14.6 Strangler Fig (Strangler Fig)

**Tavsif:** Legacy monolitni bir zarbada qayta yozmasdan, uning atrofida yangi servislar o'stirib, funksiyalarni asta-sekin "bo'g'ib" ko'chirish strategiyasi. Oldiga proxy/gateway qo'yiladi: ko'chirilgan marshrutlar yangi servisga, qolganlari monolitga yo'naltiriladi; har bir qadamda rollback imkoniyati saqlanadi. Ma'lumotlar vaqtincha ikki tomonda sinxronlanadi (event yoki CDC bilan), monolitdagi kod oxirida o'chiriladi. Asosiy qiymati - risk kichik bo'laklarga bo'linadi va biznes ishlab turadi.

**Spring'da qayerda uchraydi:** Fasad sifatida Spring Cloud Gateway (reaktiv `spring-cloud-starter-gateway-server-webflux` yoki servlet `spring-cloud-starter-gateway-server-webmvc`), `RouteLocatorBuilder` bilan `Predicates.path("/orders/**")` → yangi servis, qolgani monolitga; `RewritePath`, `CircuitBreaker` va `Retry` filtrlari migratsiyani xavfsizlashtiradi. Trafikni bosqichma-bosqich o'tkazish uchun `Weight` predicate yoki feature flag (Togglz/Unleash) ishlatiladi; monolit ichida esa `@RestController` metodini yangi servisga `RestClient`/`@FeignClient` orqali delegatsiya qiladigan adapter yoziladi. Ma'lumot sinxronizatsiyasi Debezium CDC yoki Transactional Outbox + Kafka bilan bajariladi. Monolitni avval Spring Modulith bilan modullashtirish ajratishni ancha osonlashtiradi.

**Qo'llanish keyslari:**
- 15 yillik Java EE monolitidan autentifikatsiya qismi birinchi bo'lib yangi Spring Boot servisiga ko'chiriladi.
- E-commerce'da faqat `/search` marshruti yangi servisga o'tkaziladi va natija A/B solishtiriladi.
- Hisobot va eksport funksiyalari monolitdan ajratilib, DB replikasidan o'qiydigan servisga olinadi.
- Mijozlar kabineti yangi frontend + BFF orqali ishlaydi, admin panel monolitda qoladi.
- Mintaqa bo'yicha migratsiya: avval bitta davlat trafigi yangi servisga yo'naltiriladi.

**Ehtiyot bo'ling:** Eng katta xato - migratsiyani oxirigacha yetkazmaslik: proxy, ikki ma'lumot manbasi va sinxronizatsiya kodi yillarga qolib, murakkablik ikki barobar bo'ladi. Har bir qadamga aniq "monolitdagi kod o'chirildi" mezonini va muddatni yozib qo'ying.

```yaml
spring:
  cloud:
    gateway:
      routes:
        - id: orders-new            # yangi servis, hozircha kichik ulush
          uri: lb://orders-service
          predicates:
            - Path=/api/orders/**
            - Weight=orders, 10     # 10% trafik
        - id: orders-legacy
          uri: http://legacy-erp:8080
          predicates:
            - Path=/api/orders/**
            - Weight=orders, 90     # 90% eski tizimda

# Har qadamda: ulush oshiriladi, metrika solishtiriladi, orqaga qaytish
# yo'li ochiq qoladi (Weight ni qaytarish bitta konfiguratsiya o'zgarishi).
```

## 14.7 Har bir servisga alohida ma'lumotlar bazasi (Database per Service (microservice view))

**Tavsif:** Har bir servis o'z ma'lumotlarini xususiy bazada (yoki kamida xususiy sxemada) saqlaydi va boshqa servislar unga faqat API/event orqali kiradi. Bu loose coupling'ni ta'minlaydi: sxemani o'zgartirish boshqa jamoalarni buzmaydi va har bir servis o'ziga mos ma'lumot modelini (RDBMS, document, graph) tanlashi mumkin. Narxi - cross-service join va distributed tranzaksiya yo'q, ularning o'rniga API composition, CQRS va saga keladi.

**Spring'da qayerda uchraydi:** Har bir Spring Boot servisi o'z `spring.datasource.url` va o'z Flyway/Liquibase migratsiyalariga ega (`spring-boot-starter-data-jpa` + `flyway-core`, `db/migration` har bir servisda alohida). Polyglot persistence uchun `spring-boot-starter-data-mongodb`, `spring-boot-starter-data-redis`, `spring-boot-starter-data-elasticsearch`. Testlarda Testcontainers va `@ServiceConnection` har bir servis bazasini izolyatsiya qiladi. Agar bitta DB instansi ichida sxema bo'yicha ajratilsa - `spring.jpa.properties.hibernate.default_schema` va alohida DB foydalanuvchisi/grant'lar ishlatiladi.

**Qo'llanish keyslari:**
- Order Service PostgreSQL'da, Catalog Service Elasticsearch'da ishlaydi.
- Session va rate-limit ma'lumotlari uchun alohida Redis instansi faqat gateway servisiga tegishli bo'ladi.
- Payment Service bazasiga PCI talablari bo'yicha alohida tarmoq va kalit boshqaruvi qo'llanadi.
- Analitika uchun har bir servis o'z event'larini chiqaradi, DWH esa ularni yig'adi - hech kim boshqa servis jadvalini o'qimaydi.
- Monolitdan ajratishda avval sxema ajratiladi (grant olib tashlanadi), keyin alohida instansga ko'chiriladi.

**"Bazani bo'lishmang" qoidasi bir servisning nusxalariga tegishli emas.** Qoida bir nechta TURLI servisning bitta bazaga yozishini taqiqlaydi, chunki o'sha holatda ma'lumotni o'qish va o'zgartirish mantiqi servislar orasiga tarqalib ketadi. Bitta mantiqiy servisning bir nechta nusxasi uchun esa teskarisi talab qilinadi: `order-service` ning qaysi nusxasiga borsangiz ham bir xil buyurtmani ko'rishingiz kerak, demak nusxalar o'rtasida umumiy holat SHART. Bu qoidani buzmaydi, chunki holatga kirish va uni o'zgartirish mantiqi hamon bitta mantiqiy servis ichida qoladi. Shuning uchun "har bir nusxaga alohida baza" degan talqin xato; fizik darajada o'sha bitta baza ko'p mashinada joylashishi va o'qish uchun read replica'larga bo'linishi mumkin.

**Ehtiyot bo'ling:** "Shared database" ga qaytish eng keng tarqalgan regress - hisobot uchun bo'lsa ham boshqa servis jadvaliga to'g'ridan-to'g'ri SELECT qilish chegarani yo'q qiladi. Shuningdek, cross-service `@Transactional` ishlamaydi: XA/2PC ni tiklashga urinmasdan, saga yoki outbox patternini loyihalashtiring.

```sql
-- Har servis o'z sxemasi va o'z roli bilan
CREATE SCHEMA orders   AUTHORIZATION orders_app;
CREATE SCHEMA payments AUTHORIZATION payments_app;

-- Boshqa sxemaga kirish bekor qilinadi: chegara bazada majburlanadi
REVOKE ALL ON SCHEMA payments FROM orders_app;
REVOKE ALL ON ALL TABLES IN SCHEMA payments FROM orders_app;

-- O'tish davri uchun aniq va cheklangan huquq beriladi
GRANT USAGE ON SCHEMA payments TO orders_app;
GRANT SELECT ON payments.payment_summary TO orders_app;
-- Shundan keyin "vaqtincha boshqa jadvalni o'qib turamiz" qarori
-- kod review da emas, bazada to'siladi.
```

## 14.8 Saga (xoreografiya) (Saga (choreography))

**Tavsif:** Bir nechta servisni qamragan biznes tranzaksiya lokal tranzaksiyalar ketma-ketligi sifatida bajariladi va har bir qadam natijasini event ko'rinishida e'lon qiladi; keyingi servis shu eventga reaksiya qilib o'z qadamini bajaradi. Markazlashgan koordinator yo'q - mantiq ishtirokchilar orasida tarqalgan. Xato bo'lsa, kompensatsion event'lar (masalan, `OrderRejected`, `InventoryReleased`) teskari yo'nalishda effektni bekor qiladi. Oddiy, 2-4 qadamli oqimlar uchun eng yengil yechim.

**Spring'da qayerda uchraydi:** Event transporti - Spring for Apache Kafka (`KafkaTemplate`, `@KafkaListener`, xatolar uchun `DefaultErrorHandler` + `DeadLetterPublishingRecoverer`) yoki Spring AMQP (`RabbitTemplate`, `@RabbitListener`). Spring Cloud Stream bilan bu `Consumer<OrderCreated>` / `Supplier<...>` bean'lari ko'rinishida yoziladi, `spring.cloud.stream.bindings.*` konfiguratsiyasi bilan. Event'larni atomar chiqarish uchun Transactional Outbox: Spring Modulith `@Externalized` + `spring-modulith-events-kafka`, yoki `@TransactionalEventListener(phase = AFTER_COMMIT)`. Idempotentlik uchun processed-message jadvali va `@Transactional` ichida unique constraint.

**Qo'llanish keyslari:**
- Buyurtma: `OrderCreated` → Inventory reserve → `StockReserved` → Payment charge → `PaymentCompleted` → `OrderConfirmed`.
- To'lov muvaffaqiyatsiz bo'lsa `PaymentFailed` eventi zaxirani avtomatik bo'shatadi.
- Foydalanuvchi ro'yxatdan o'tishi: profil yaratish → welcome email → bonus hisoblash.
- Kontent yuklash: fayl saqlash → transcoding → katalogda e'lon qilish.
- Obunani bekor qilish: billing to'xtatish → kirish huquqini olib tashlash → arxivlash.

**Xoreografiyali saga holatini correlation ID bilan kuzatish.** Xoreografiyada biznes jarayonining aniq ko'rinishi yo'qolishi bir muammo; ikkinchisi - saga hozir qaysi holatda ekanini biladigan joy yo'qligi, bu esa kerak bo'lganda kompensatsiya ulashning imkonini yo'q qiladi. Yechim: saga uchun unikal identifikator yaratib, uni shu saga chiqaradigan BARCHA hodisalarga qo'yish (correlation ID), keyin hodisalarni yig'ib har bir buyurtma qaysi holatda ekanini ko'rsatadigan proyeksiya quradigan alohida servis yozish. O'sha servis holat ko'rinishini berish bilan birga, ishtirokchilar o'zi hal qila olmagan muammolarni dasturiy ravishda tuzatishi ham mumkin. Spring'da correlation ID Micrometer Tracing ning `traceId` idan alohida, biznes identifikatori sifatida hodisa payload'ida va Kafka header'ida uzatiladi, holat proyeksiyasini esa `@KafkaListener` + read model jadvali quradi.

**Ehtiyot bo'ling:** Qadamlar soni oshgani sayin oqim hech bir kodda ko'rinmay qoladi - debug va "hozir saga qayerda?" savoliga javob berish qiyinlashadi, shuning uchun 4-5 qadamdan ko'pida orkestratsiyaga o'ting. Xoreografiya va orkestratsiya tanlovning faqat bir o'lchami: aloqa va izchillik bilan birga olinganda sakkizta nomlangan birikma chiqadi, ularning jadvali va qaror qoidasi [14.42](#1442-saga-ning-sakkiz-varianti-uch-olchamli-tanlov-transactional-saga-patterns) da. Tsiklik bog'liqlik (A eventi B'ni, B eventi yana A'ni uyg'otishi) va kompensatsiya qilib bo'lmaydigan qadamlar (yuborilgan email) ni oldindan hisobga oling.

```java
// Xoreografiya: markaz yo'q, har servis hodisaga javob beradi
@Component
class StockReservationSaga {
    @KafkaListener(topics = "orders.placed")
    void on(OrderPlaced e) {
        try {
            inventory.reserve(e.orderId(), e.items());
            kafka.send("stock.reserved", new StockReserved(e.orderId()));
        } catch (OutOfStockException ex) {
            kafka.send("stock.rejected", new StockRejected(e.orderId(), ex.sku()));
        }
    }
}

@Component
class OrderCancellation {
    @KafkaListener(topics = "stock.rejected")
    void on(StockRejected e) { orders.cancel(e.orderId(), "zaxira yo'q"); }
}
// Afzalligi: servislar bir-birini bilmaydi. Narxi: butun oqimni hech kim
// ko'rmaydi, nosozlikni kuzatish uchun trace shart.
```

## 14.9 Saga (orkestratsiya) (Saga (orchestration))

**Tavsif:** Tarqatilgan tranzaksiyani markaziy orchestrator (saga manager) boshqaradi: u ishtirokchilarga buyruq (command) yuboradi, javoblarni kutadi, holatni saqlaydi va xato bo'lsa kompensatsion buyruqlarni teskari tartibda ishga tushiradi. Oqim bitta joyda - state machine ko'rinishida - tasvirlanadi, shuning uchun murakkab shartlar, timeout'lar va retry'lar ancha boshqariladigan bo'ladi. Narxi - orchestrator qo'shimcha komponent va u biznes mantiqni o'ziga tortib ketishi mumkin.

**Spring'da qayerda uchraydi:** Orchestrator holatini saqlash uchun Spring Data JPA entity (`SagaInstance`, `@Version` bilan) va Spring Statemachine (`spring-statemachine-core`, `@EnableStateMachineFactory`, `StateMachinePersister`) ishlatiladi. Timeout va qayta urinish uchun `@Scheduled`, ShedLock yoki Quartz (`spring-boot-starter-quartz`); buyruqlar Kafka/RabbitMQ orqali boriladi. Tayyor yechimlar: Axon Framework (`@Saga`, `@SagaEventHandler`, `@StartSaga`/`@EndSaga` va `axon-spring-boot-starter`), Camunda 8 / Zeebe va Temporal (ikkisida ham Spring Boot starter bor), Eventuate Tram Saga. Resilience4j (`spring-cloud-starter-circuitbreaker-resilience4j`, `@Retry`, `@CircuitBreaker`) ishtirokchi chaqiruvlarini himoyalaydi.

**Qo'llanish keyslari:**
- Sayohat bron qilish: parvoz + mehmonxona + avtomobil, bittasi muvaffaqiyatsiz bo'lsa hammasi bekor qilinadi.
- Kredit arizasi: skoring → hujjat tekshiruvi → qo'lda tasdiqlash → shartnoma yaratish, har qadamda timeout bor.
- Mijoz onboarding: KYC → hisob ochish → karta buyurtmasi → yetkazib berish kuzatuvi.
- Katta buyurtmani bo'lib yuborish va qaytarishlarni (refund) kompensatsiya bilan boshqarish.
- Bulutli resurs provisioning: VM → tarmoq → DNS → monitoring, xatoda teskari tozalash.

**Saga va process manager: bitta narsami?** Korpusdagi [jarayon menejeri](15-enterprise-integration-patterns-i-xabarlar.md#1535-jarayon-menejeri-process-manager) bo'limi process manager ni "taqsimlangan tranzaksiyalarda orchestration-based saga sifatida tanilgan" deb beradi, Khononov esa ikkisini ataylab ajratadi. Zid emas, ikki xil darajadagi gap va ajratuvchi shart modellashtirish darajasida. **Topologiya darajasida** ikkisi bir xil: markaziy stateful komponent qadamlarni boshqaradi, holatni saqlaydi va kompensatsiyani ishga tushiradi - EIP ning ta'rifi shu haqda. **Modellashtirish darajasida** Khononovning uch mezoni ikkisini ajratadi: (1) saga hodisani buyruqqa ODDIY moslaydi, ya'ni ichida if-else yo'q; shart paydo bo'lsa u endi saga emas, process manager; (2) saga ma'lum hodisa kuzatilganda yashirin paydo bo'ladi (`CampaignActivated` kelsa saga bor), process manager esa bitta manba hodisaga bog'lanmaydi va aniq identifikator bilan ochiq yaratiladi; (3) process manager bir butun biznes jarayoni (xizmat safarini bron qilish: marshrutni hisoblash, xodimdan tasdiq, boshqa marshrut tanlansa rahbardan tasdiq, mehmonxona bo'lmasa chiptani bekor qilish) va holat saqlashi majburiy. Amaliy foydasi: agar sizning "saga" ingizda shartli tarmoqlanish bor va u foydalanuvchi so'rovidan ochiq yaratilsa, uni saga deb emas, process manager deb loyihalashtiring; shunda shart va tarmoqlanishni state machine bilan modellashtirish tabiiy bo'ladi.

**Ehtiyot bo'ling:** Orchestrator "god service" ga aylanib, ishtirokchilar anemik CRUD'ga tushib qolmasligi uchun unda faqat koordinatsiya mantiqi qolsin. Saga ACID emas: oraliq holatlar tashqariga ko'rinadi, shuning uchun `PENDING`/`CONFIRMED` statuslarini UI va API shartnomasida ochiq modellashtirish shart. Orkestratsiya o'zi ham bitta pattern emas: aloqa sinxronmi yoki asinxron, izchillik atomarmi yoki yakuniy - bu ikki savol natijasini keskin o'zgartiradi ([14.42](#1442-saga-ning-sakkiz-varianti-uch-olchamli-tanlov-transactional-saga-patterns)).

```java
// Orkestratsiya: qadamlar va kompensatsiya bitta joyda ko'rinadi
@Component
public class CheckoutSaga {
    private final SagaStateRepository state;      // holat saqlanishi SHART

    public void start(OrderId id) {
        state.save(SagaState.started(id));
        commands.send(new ReserveStock(id));
    }

    @KafkaListener(topics = "stock.reserved")
    void onStockReserved(StockReserved e) {
        state.advance(e.orderId(), Step.STOCK_RESERVED);
        commands.send(new CapturePayment(e.orderId()));
    }

    @KafkaListener(topics = "payment.failed")
    void onPaymentFailed(PaymentFailed e) {
        commands.send(new ReleaseStock(e.orderId()));     // kompensatsiya
        state.fail(e.orderId(), e.reason());
    }
}
// Orkestrator holati bazada saqlanadi: u yiqilsa saga davom etishi kerak
```

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

Mavjudlik ko'paytmaga aylanishidan qutulish uchun uchta yo'l bor va har birining narxi bor; tanlov shu uchtasi orasida qilinadi. Birinchi: kerakli ma'lumotni chaqiruvchi tomonga replikatsiya qilib, chaqiruvni butunlay yo'q qilish - katta hajmda yoki tez o'zgaradigan ma'lumotda samarasiz, chunki replikatsiya trafigi va eskirgan ma'lumot muammosi chaqiruvdan qimmatroq bo'lib qoladi ([Materiallashtirilgan ko'rinish](10-malumotlarni-boshqarish-va-taqsimlash.md#1018-materiallashtirilgan-korinish-materialized-view)). Ikkinchi: so'rovni to'liq ishlashdan oldin javob qaytarish - servis "qabul qildim" deb javob beradi va ishni keyin tugatadi; narxi mijozga ko'chadi, u endi natijani polling qilishi yoki xabarnoma olishi kerak ([Asinxron so'rov-javob](07-api-dizayn-patternlari.md#715-asinxron-sorov-javob-asynchronous-request-reply)). Uchinchi: servisni umuman faqat asinxron API bilan ta'riflash, ya'ni sinxron shartnoma bermaslik; ichki servislar orasida bu ishlaydi, ommaviy API da esa ko'pincha mumkin emas, chunki mijozlar sinxron chaqiruv kutadi.

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

```java
// Domen hodisasi: servislar orasidagi shartnoma, ichki model emas
public record OrderPlaced(
        long orderId,
        String customerId,
        String total,            // pul satr sifatida: float emas
        String currency,
        List<Item> items,
        Instant placedAt,
        String eventId) {        // idempotentlik uchun
    public record Item(String sku, int quantity) {}
}
// Qoidalar:
//  - nom o'tgan zamonda: OrderPlaced, OrderCancelled
//  - ichki entity emas, alohida versiyalangan sxema
//  - faqat iste'molchiga kerakli maydonlar (butun agregat emas)
//  - eventId va placedAt har doim bor
```

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

Mavzuning to'liq yozuvi shu hujjatdagi [tranzaksion Outbox](10-malumotlarni-boshqarish-va-taqsimlash.md#1014-tranzaksion-outbox-transactional-outbox) bo'limida; bu yerda faqat pattern katalogi nuqtai nazari.

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

```json
{
  "name": "orders-outbox",
  "config": {
    "connector.class": "io.debezium.connector.postgresql.PostgresConnector",
    "plugin.name": "pgoutput",
    "slot.name": "orders_outbox_slot",
    "table.include.list": "orders.outbox",
    "transforms": "outbox",
    "transforms.outbox.type": "io.debezium.transforms.outbox.EventRouter",
    "transforms.outbox.route.by.field": "aggregate_type"
  }
}
// Afzalligi: polling yo'q, kechikish millisekund.
// Narxi: wal_level = logical kerak va slot iste'mol qilinmasa WAL o'sadi.
```

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

```java
// Polling publisher: outbox jadvalini davriy o'qib yuboradi
@Scheduled(fixedDelay = 500)
@SchedulerLock(name = "outbox-publisher", lockAtMostFor = "PT1M")
public void publish() {
    List<OutboxMessage> batch = outbox.lockNextBatch(100);   // FOR UPDATE SKIP LOCKED
    for (OutboxMessage m : batch) {
        kafka.send(m.topic(), m.key(), m.payload());
        outbox.markSent(m.id());
    }
}
// SKIP LOCKED: bir nechta nusxa parallel ishlaydi va bir xil xabarni olmaydi.
// Debezium'dan sodda (qo'shimcha infratuzilma yo'q), lekin kechikish
// polling davriga teng va bazaga doimiy yuk tushadi.
```

## 14.15 Masofaviy protsedura chaqirig'i (Remote Procedure Invocation)

**Tavsif:** Servislar bir-biri bilan sinxron request/response stilida, masofaviy metod chaqirig'iga o'xshash protokol orqali gaplashadi - REST, gRPC, GraphQL yoki Thrift. Client so'rov yuboradi va javob kelguncha kutadi, shuning uchun model oddiy va debug qilish oson, lekin callee ishlamayotganda caller ham to'xtaydi (temporal coupling). Katta tizimlarda bu pattern Circuit Breaker, timeout va retry bilan birga qo'llanilishi shart. Odatda o'qish (query) operatsiyalari va darhol javob kerak bo'lgan hollarda tanlanadi.

**Spring'da qayerda uchraydi:** Server tomonda `@RestController`, `@GetMapping`/`@PostMapping`, Spring Boot 3.x'da `RestClient` va deklarativ `@HttpExchange` interfeyslari (`HttpServiceProxyFactory`), reaktiv stack'da `WebClient`; eski loyihalarda `RestTemplate` (maintenance mode) va OpenFeign (`spring-cloud-openfeign`, `@FeignClient`). gRPC uchun `grpc-spring-boot-starter` yoki Spring Boot 4 / Spring Framework 7 gRPC qo'llab-quvvatlashi, GraphQL uchun `spring-boot-starter-graphql` (`@QueryMapping`, `@SchemaMapping`). Java 21+ virtual thread'lar (`spring.threads.virtual.enabled=true`) blocking RPC'ni arzonlashtiradi.

**Qo'llanish keyslari:**
- API Gateway'dan `order-service`'ga mijoz buyurtmasi detallarini olish uchun REST GET chaqirig'i.
- Yuqori throughput'li internal servislar orasida gRPC + protobuf bilan past latency'li aggregatsiya.
- Mobil klient uchun bitta GraphQL endpoint orqali bir necha backend servis ma'lumotini birlashtirish.
- Autentifikatsiya servisidan token validation (introspection) uchun sinxron so'rov.
- To'lov provayderining sinxron authorize API'siga murojaat qilib darhol natija ko'rsatish.

**Besh ta'sirga ega uchta kechikish.** Boshqa servis ma'lumotini chaqiruv bilan o'qish Ford va boshqalarda uch qismdan iborat kechikish beradi (Hard Parts, 10-bob, 285-bet): **tarmoq kechikishi** so'rov va javobning yo'lda o'tgan vaqti, odatda 30-300 ms; **xavfsizlik kechikishi** maqsad endpoint qo'shimcha avtorizatsiya talab qilganda qo'shiladi va endpointning qattiqligiga qarab 20-400 ms oralig'ida; **ma'lumot kechikishi** esa javobni yasash uchun qo'shimcha baza chaqirig'i kerak bo'lganda (SQL join o'rniga alohida so'rov) 10-50 ms qo'shadi. Eng yomon holatda uchtasi birga faqat tavsifni olish uchun bir soniyaga yetadi. Narxning ikkinchi qismi bog'lanish: chaqiruvchi chaqirilganning mavjudligiga tayanadi, ya'ni ikkisi semantik va statik bog'lanadi va birga masshtablanishga majbur bo'ladi.

**Temporal coupling ikki servis orasida emas, ikki nusxa orasida.** Sinxron bloklovchi chaqiruvda javob odatda kelgan tarmoq ulanishining o'zi bilan qaytariladi. Demak chaqirilgan servis javob yuborishga tayyor bo'lganda chaqiruvchining AYNAN O'SHA nusxasi o'lgan bo'lsa, javob yo'qoladi - bog'lanish `order-processor` va `loyalty` orasida emas, ularning ikki konkret nusxasi orasida. Asinxron request-response ga o'tganda shu nuqtani hisobga olish kerak: javobni upstream servisning istalgan nusxasi qayta ishlay olishi shart, aks holda asinxronlik faqat nomda qoladi.

**Chaqiruv uslublarini ikki o'lchamda tasniflash.** Richardson IPC texnologiyasini tanlashdan OLDIN o'zaro ta'sir uslubini tanlashni aytadi va uni ikki o'lchamga joylaydi (Microservices Patterns, 3-bob, 67-68-betlar): birinchi o'lcham bir-bir yoki bir-ko'p (so'rovni bitta servis ishlaydimi yoki bir nechtasi), ikkinchisi sinxron yoki asinxron (klient javobni tez kutadi va bloklanadi, yoki bloklanmaydi).

| | bir-bir | bir-ko'p |
|---|---|---|
| Sinxron | request/response | - |
| Asinxron | async request/response, one-way notification | publish/subscribe, publish/async responses |

Muhim nuqta: sinxron request/response uslubi IPC texnologiyasiga deyarli ortogonal. Servis boshqa servis bilan request/response uslubida REST bilan ham, xabar brokeri bilan ham gaplashishi mumkin va broker ishlatilgani klient javobni kutib bloklanmasligini bildirmaydi, ya'ni broker o'zi bo'sh bog'lanish bermaydi. Har servis amalda bu uslublarning birikmasini ishlatadi.

**Ehtiyot bo'ling:** Sinxron chaqiriqlar zanjiri (A→B→C→D) availability'ni ko'paytma qilib kamaytiradi va latency'ni jamlaydi - har bir hop'da timeout, bulkhead va circuit breaker (Resilience4j) bo'lishi kerak. Yozuv operatsiyalarida retry'ni idempotency key'siz qilmang va distributed transaction o'rniga RPC zanjirini ishlatmang - bunday holatda Saga yoki Messaging to'g'ri tanlov.

```java
// RPC: sodda, lekin chaqiruvchi chaqirilganning mavjudligiga bog'lanadi
@Bean
RestClient inventoryClient(RestClient.Builder b, ServiceProperties p) {
    return b.baseUrl(p.inventoryUrl())
            // Boot 4.x: HttpClientSettings + ClientHttpRequestFactoryBuilder
            .requestFactory(ClientHttpRequestFactoryBuilder.detect().build(
                    HttpClientSettings.defaults()
                            .withConnectTimeout(Duration.ofSeconds(1))
                            .withReadTimeout(Duration.ofSeconds(3))))
            .build();
}
// Har sinxron chaqiruv uchun uchtasi shart: timeout, retry siyosati
// (faqat idempotent operatsiyaga) va circuit breaker.
// Zanjir uzunligi mavjudlikni kamaytiradi: 5 x 99.9% = 99.5%.
```

## 14.16 Xabar almashish (Messaging)

**Tavsif:** Servislar bir-biriga to'g'ridan-to'g'ri murojaat qilmasdan, message broker orqali asinxron xabar (event yoki command) almashadi. Producer xabarni yuborib ishini davom etadi, consumer o'z tezligida qayta ishlaydi - bu temporal coupling'ni yo'q qiladi, consumer vaqtincha o'chsa ham xabarlar queue'da saqlanadi. Buffering, back-pressure va bir xabarni ko'p consumer'ga tarqatish (pub/sub) imkonini beradi. Narxi - eventual consistency, duplicate'lar va distributed debugging murakkabligi.

**Spring'da qayerda uchraydi:** `spring-kafka` (`@KafkaListener`, `KafkaTemplate`, `DefaultErrorHandler`, `DeadLetterPublishingRecoverer`), `spring-boot-starter-amqp` (`@RabbitListener`, `RabbitTemplate`), `spring-jms` (`@JmsListener`), Spring Cloud Stream binder'lari (`spring-cloud-stream-binder-kafka`, `Function<T, R>` bean'lari va `StreamBridge`), Spring Integration va Spring Pulsar (`@PulsarListener`). Cloud native variantlar: Spring Cloud AWS SQS (`@SqsListener`), Spring Cloud GCP Pub/Sub. Observability uchun Micrometer Tracing xabar header'lariga trace context'ni avtomatik propagate qiladi.

**Qo'llanish keyslari:**
- `OrderPlaced` event'ini inventory, billing va notification servislari mustaqil tinglashi.
- Og'ir hisobot generatsiyasini queue'ga topshirib HTTP so'rovni darhol `202 Accepted` bilan yopish.
- Saga orkestratsiyasida qadamlar orasida command/reply xabarlari almashish.
- CQRS'da read model'ni event stream'dan asinxron yangilash.
- Peak trafik paytida tashqi provayder rate limit'ini queue bilan tekislash (load leveling).

**Sekin tekshiruvni kritik yo'ldan chiqarish.** Buyurtma oqimida `order-processor` to'lovni, to'lov servisi firibgarlik tekshiruvini, u esa mijoz servisini sinxron chaqirsa, to'rt servisdan yoki ular orasidagi tarmoqdan birortasidagi muammo butun amalni yiqitadi. Bundan tashqari uzun zanjir resurs uchun kurash yaratadi: `order-processor` to'lovdan javob kutib ulanishni ochiq ushlab turadi, to'lov servisi firibgarlik tekshiruvidan javob kutib o'zining ulanishini ushlab turadi va shu davom etadi, natijada bo'sh ulanish tugashi yoki tarmoq tirbandligi ehtimoli oshadi. Yechim oqimni qayta chizishdan boshlanadi: firibgarlik tekshiruvini asosiy xarid oqimidan chiqarib fonda yuritish, u muammo topsa mijoz yozuvini belgilash va to'lov jarayonining boshida shu belgini tekshirish. Natijada ish qismi parallel bajariladi, zanjir qisqaradi va kritik operatsiya uchun bitta bog'liqlik kamayadi.

**Ehtiyot bo'ling:** Broker at-least-once yetkazadi, shuning uchun consumer idempotent bo'lishi va retry + DLQ strategiyasi aniq belgilanishi kerak; `@KafkaListener`'da cheksiz retry poison message bilan partition'ni butunlay to'xtatib qo'yadi. Xabar sxemasini (schema) versiyalamasdan o'zgartirish barcha consumer'larni buzadi - Avro/Protobuf + Schema Registry yoki tolerant reader yondashuvini qo'llang.

```java
// Xabar: jo'natuvchi javobni kutmaydi, qabul qiluvchi yiqilsa xabar yo'qolmaydi
@Bean
NewTopic ordersPlaced() {
    return TopicBuilder.name("orders.placed")
            .partitions(12)                       // parallellik chegarasi
            .replicas(3)
            .config(TopicConfig.MIN_IN_SYNC_REPLICAS_CONFIG, "2")
            .config(TopicConfig.RETENTION_MS_CONFIG, "604800000")   // 7 kun
            .build();
}
// Producer tomonida: acks=all, enable.idempotence=true
// Consumer tomonida: idempotentlik (14.18) va DLQ shart
```

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

```java
// Domain-specific protocol: umumiy RPC o'rniga soha standarti
@Component
public class Iso20022PaymentAdapter {

    public PaymentReceipt send(Payment p) {
        // Protokol tafsiloti (maydon kodlari, formatlar) faqat shu sinfda
        Pain001Document doc = Pain001Builder.from(p)
                .debtor(p.from()).creditor(p.to())
                .amount(p.amount()).build();
        return translate(gateway.submit(doc.marshal()));
    }
}
// Afzalligi: soha standarti, integratsiya kelishuvi qisqa.
// Narxi: protokol og'ir va o'zgartirish sekin, shuning uchun u
// bitta adapter ichida qolishi kerak.
```

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

Alohida `processed_message` jadvali o'rniga [event store](10-malumotlarni-boshqarish-va-taqsimlash.md#1024-event-sourcing-ombori-event-sourcing-store)ning o'zini idempotentlik ombori sifatida ishlatish mumkin: kelgan xabarning identifikatorini shu xabar natijasida chiqadigan event ichiga yozib qo'yish va keyin shu identifikator bo'yicha tekshirish. Bu alohida jadvaldan qutqaradi, lekin bitta tuzog'i bor va u jim ishlaydi: xabarni ishlash hech qanday event chiqarmasa (agregat holati o'zgarmasa, biznes qoidasi bo'yicha hech narsa qilinmasa), xabar ishlangani haqida hech qanday yozuv ham qolmaydi. Xabar qayta yetkazilganda esa u "yangi" bo'lib ko'rinadi va ikkinchi marta ishlanadi - bu holatda birinchi urinishdan keyin holat o'zgargan bo'lsa, ikkinchisi boshqa natija beradi. Yechim: har holatda, hatto hech narsa o'zgarmaganda ham, soxta (pseudo) event yozish va iste'molchilarni uni e'tiborsiz qoldirishga majburlash. Shu majburiyat esa patternning yashirin narxi: endi har iste'molchi bu event turini bilishi va o'tkazib yuborishi kerak, aks holda oqimga ma'nosiz event chiqadi.

```java
// Idempotent iste'molchi: bir xil xabar ikki marta kelsa bir marta ishlanadi
@KafkaListener(topics = "orders.placed")
@Transactional
public void on(OrderPlaced e) {
    // Inbox: event_id unique, ikkinchi marta INSERT o'tmaydi
    int inserted = db.sql(
            "INSERT INTO inbox(event_id, consumer) VALUES (:id, 'warehouse') "
          + "ON CONFLICT (event_id) DO NOTHING")
            .param("id", e.eventId())
            .update();
    if (inserted == 0) return;                  // allaqachon ishlangan
    warehouse.reserve(e.orderId(), e.items());
}
// Inbox yozuvi va biznes o'zgarishi bitta tranzaksiyada bo'lishi shart,
// aks holda ikkisi orasida yiqilish takroriy ishlovga olib keladi.
```

Mavzuning to'liq yozuvi [idempotency](07-api-dizayn-patternlari.md#79-idempotentlik-kaliti-idempotency-key) bo'limida; bu yerda faqat shu bo'limning nuqtai nazari.

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

```java
// Klient tomonda aniqlash: klient reyestrdan ro'yxatni oladi va o'zi tanlaydi
@Bean
@LoadBalanced                         // Spring Cloud LoadBalancer
RestClient.Builder loadBalancedBuilder() { return RestClient.builder(); }

@Service
class InventoryClient {
    private final RestClient client;
    InventoryClient(@LoadBalanced RestClient.Builder b) {
        this.client = b.baseUrl("http://inventory-service").build();   // logik nom
    }
}
// Afzalligi: qo'shimcha tarmoq o'tishi yo'q, klient aqlli balanslash qiladi.
// Narxi: har til uchun kutubxona kerak va u ilova bilan birga yangilanadi.
```

## 14.20 Server tomonda aniqlash (Server-Side Discovery)

**Tavsif:** Client faqat barqaror manzilga (router, load balancer yoki gateway) so'rov yuboradi; registry'ni so'rash va instansiya tanlash mas'uliyati shu infratuzilma komponentiga tegishli. Client hech qanday discovery kodi saqlamaydi, shuning uchun polyglot muhit uchun ideal va discovery logikasi markazlashgan holda yangilanadi. Kamchiligi - qo'shimcha network hop va LB'ning o'zi high-availability talab qiladigan kritik komponentga aylanishi. Kubernetes'dagi `Service` + kube-proxy/DNS, AWS ALB yoki Istio sidecar - bu pattern'ning eng keng tarqalgan ko'rinishlari.

**Spring'da qayerda uchraydi:** Spring Cloud Gateway (reaktiv `spring-cloud-starter-gateway-server-webflux` yoki servlet `spring-cloud-starter-gateway-server-webmvc`) `lb://order-service` URI bilan discovery'ni server tomonda bajaradi; `DiscoveryClientRouteDefinitionLocator` registry'dan route'larni avtomatik yaratadi. Kubernetes'da Spring Boot ilovasi oddiygina `http://order-service:8080` ga `RestClient` bilan murojaat qiladi va DNS/kube-proxy load balancing qiladi - kodda hech qanday discovery bean kerak emas; `spring-cloud-kubernetes` ConfigMap/Secret va discovery integratsiyasini qo'shadi. Istio/Linkerd bilan esa barcha chiqish trafigi Envoy sidecar orqali o'tadi, ilova faqat logical hostname biladi.

**Qo'llanish keyslari:**
- Kubernetes'da Java, Go va Node servislari bir-birini `Service` DNS nomi orqali chaqirishi.
- Spring Cloud Gateway orqali tashqi trafikni `lb://` route'lar bilan ichki servislarga taqsimlash.
- mTLS, retry va circuit breaking siyosatini Istio DestinationRule'da markazlashgan boshqarish.
- AWS ECS/ALB target group orqali avtoskaling qilinadigan servis instansiyalariga trafik yuborish.
- Legacy .NET klientlari Spring servislariga hech qanday SDK o'rnatmasdan ulanishi.

**Ehtiyot bo'ling:** Qo'shimcha hop latency va single point of failure xavfini keltiradi - LB/gateway'ni albatta bir nechta replika va health-check bilan ishlating. Gateway'ga biznes logikani (validatsiya, transformatsiya, orkestratsiya) yuklash klassik anti-pattern: u yangi monolitga aylanadi; gateway faqat routing, auth va cross-cutting masalalar bilan shug'ullansin.

**Markaziy DNS va load balancer nega yetmaydi:** an'anaviy modelda klient umumiy DNS nomiga uradi, LB marshrut jadvalidan fizik manzilni topadi va statik serverlar guruhiga uzatadi. Carnell bu modelning bulut uchun to'rtta kamchiligini sanaydi (Carnell, 4-bob, 99-bet):

- **Yagona nosozlik nuqtasi.** LB ni HA qilsa ham, u butun infratuzilmaning markaziy bo'g'izi bo'lib qoladi: u o'chsa, unga tayangan hamma ilova o'chadi.
- **Gorizontal masshtab cheklangan.** Tijorat LB lari odatda hot-swap zaxira modelida ishlaydi: yukni bitta server ko'taradi, ikkinchisi faqat fail-over uchun turadi; litsenziya ham o'zgaruvchan emas, qat'iy sig'imga sozlangan.
- **Statik boshqariladi.** An'anaviy LB tez ro'yxatga olish va chiqarish uchun loyihalanmagan: marshrutlar markaziy bazada turadi va yangi marshrut ko'pincha vendor API si orqali qo'shiladi.
- **Murakkab.** LB proxy bo'lgani uchun klient so'rovini fizik servisga moslash qoidalari qo'lda yozilib deploy qilinadi, ya'ni yangi nusxa startupda o'zini ro'yxatga olmaydi.

Bu LB ni rad etish emas. LB SSL termination ni markazlashtirish va port xavfsizligini boshqarish uchun o'z o'rnida qoladi: u orqasidagi hamma serverning kirish (ingress) va chiqish (egress) portlarini qulflaydi, bu esa PCI kabi sertifikatsiya talablarida kerak bo'ladi.

```yaml
apiVersion: v1
kind: Service
metadata:
  name: inventory-service
spec:
  selector:
    app: inventory
  ports:
    - port: 80
      targetPort: 8080

# Klient shunchaki http://inventory-service ga murojaat qiladi.
# Service DNS va kube-proxy balanslashni o'zi bajaradi: ilovada
# kutubxona kerak emas, lekin balanslash siyosati platformada qoladi.
```

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

```yaml
eureka:
  client:
    service-url:
      defaultZone: http://eureka-1:8761/eureka/,http://eureka-2:8761/eureka/
    registry-fetch-interval-seconds: 10
  instance:
    prefer-ip-address: true
    lease-renewal-interval-in-seconds: 10     # heartbeat
    lease-expiration-duration-in-seconds: 30  # shundan keyin o'lik hisoblanadi

# Kubernetes'da bu rolni etcd va Service DNS bajaradi, shuning uchun
# alohida Eureka ko'pincha keraksiz qatlam bo'ladi.
```

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

**Warm-up kechikishi: yangi nusxa darhol ko'rinmaydi:** Eureka nusxani registratsiyadan keyin darhol emas, 30 soniya ichidagi uchta ketma-ket muvaffaqiyatli health check dan keyin mijozlarga ochadi (Carnell, 4-bob, 110-bet). Shuning uchun servis ko'tarilgan zahoti uni chaqirsangiz, servisning o'zi ishlab turgan bo'lsa ham "servis topilmadi" degan 404 olasiz. Bu ayniqsa hamma narsa birga ko'tariladigan lokal va `docker compose` muhitida seziladi; productionda registry allaqachon ishlab turadi va eski nusxalar so'rovni qabul qilib turgani uchun kechikish ko'rinmaydi. Amalda: smoke check va integratsiya testi registratsiya oynasini kutsin, deploy skripti esa "nusxa ko'tarildi" degan signalni emas, registry da ko'rindi degan signalni kutsin.

ESLATMA: uch heartbeat va 30 soniya - kitobdagi Eureka ning standart sozlamasi. Consul, Spring Cloud Kubernetes yoki Kubernetes `Endpoints` propagatsiyasi uchun oyna boshqa, lekin "ro'yxatga olish bilan ko'rinish bir vaqtda emas" qoidasi o'zgarmaydi.

```java
// Self registration: nusxa o'zini ro'yxatga oladi va heartbeat yuboradi
@SpringBootApplication
@EnableDiscoveryClient            // startup'da register, shutdown'da deregister
public class InventoryApplication { }

// Graceful shutdown bo'lmasa, o'lik nusxa reyestrda qolib, unga trafik
// ketishda davom etadi:
//   server.shutdown=graceful
//   spring.lifecycle.timeout-per-shutdown-phase=30s
// Shart: deregister shutdown boshida, so'rovlarni tugatishdan oldin bo'lsin.
```

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

```yaml
apiVersion: v1
kind: Pod
spec:
  containers:
    - name: app
      readinessProbe:               # ro'yxatga kirish sharti
        httpGet: {path: /actuator/health/readiness, port: 8080}
        periodSeconds: 5
        failureThreshold: 3

# Afzalligi: ilovada registratsiya kodi yo'q, shuning uchun til va
# framework ahamiyatsiz. Ro'yxat haqiqati readiness probe'ga tayanadi:
# probe noto'g'ri yozilsa, trafik tayyor bo'lmagan nusxaga ketadi.
```

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

**Veb sayt uchun standart tanlov sahifa asosidagi dekompozitsiya.** Newman UI dekompozitsiyasini ikki texnikaga ajratadi: widget asosidagi (bir ekranga mustaqil bo'laklarni ulash) va sahifa asosidagi (frontend mustaqil veb sahifalarga bo'linadi). Interfeys veb sayt bo'lsa, uning standart tanlovi sahifa asosidagi dekompozitsiya: `/albums/` so'rovlari to'g'ridan-to'g'ri Albums servisiga, `/artists/` esa Artists servisiga yo'naltiriladi, har biri o'z sahifasini to'liq render qiladi va ularni umumiy navigatsiya bog'laydi. Servisga egalik qilgan jamoa UI ni uchidan uchiga ko'radi, shuning uchun o'z o'zgarishi foydalanuvchiga qanday ta'sir qilishini tushunadi. Texnik jihati ham sodda: brauzerda hech qanday maxsus JavaScript ham, muammoli iFrame ham kerak emas - foydalanuvchi havolani bosadi va yangi sahifa so'raladi; qurilma turiga moslashish esa progressive enhancement bilan hal qilinadi. Newman shu yerda tez-tez uchraydigan xatoni aytadi: SPA texnologiyasiga shoshilish natijasida veb sayt sifatida yaxshi ishlaydigan tajriba zo'rlab single-page application ga joylashtiriladi. Sahifa asosidagi bo'linishni widget bilan birga ishlatish mumkin: sahifa ichida widgetlar bo'lishi mumkin.

**Ehtiyot bo'ling:** Bir sekin fragment butun sahifani ushlab turmasligi uchun har bir fragment chaqirig'iga qat'iy timeout, circuit breaker va bo'sh/keshlangan fallback bering. Umumiy CSS, dizayn tokenlari va versiyalanishini boshqarmasa, sahifa vizual jihatdan tarqalib ketadi va kompozitsiya qatlami yangi muvofiqlashtirish bo'yni (coupling point) bo'lib qoladi.

```html
<div class="cart">
  <!--#include virtual="/cart-service/fragment" -->
</div>

<!-- Nginx SSI yoki shlyuzda yig'ish. Qoidalar:
     - fragment timeout bilan so'raladi va yiqilsa fallback ko'rsatiladi
     - CSS nom maydoni ajratilgan (prefiks)
     - fragment HTML qaytaradi, JSON emas: brauzerda yig'ish kerak emas
     Afzalligi: birinchi renderlash tez va SEO ishlaydi.
     Narxi: shlyuz yangi tor joy bo'ladi va keshlash murakkablashadi. -->
```

## 14.26 Klient tomonda UI kompozitsiyasi (Client-Side UI Composition)

**Tavsif:** Sahifa brauzerda yig'iladi: shell ilova turli jamoalar deploy qilgan frontend modullarni (fragment, web component yoki remote bundle) runtime'da yuklaydi va har biri o'z backend servisi bilan to'g'ridan-to'g'ri gaplashadi. Bu jamoalarga to'liq mustaqil deploy va texnologiya tanlash erkinligini beradi, shuningdek sahifa bir qismi ishlamasa ham qolgani ishlashini (graceful degradation) ta'minlaydi. Odatda Module Federation, custom elements yoki single-spa bilan quriladi. Narxi - bundle hajmi, shared dependency boshqaruvi va birinchi yuklanish tezligi.

**Spring'da qayerda uchraydi:** Spring Boot bu yerda asosan backend tomonini ta'minlaydi: har bir micro frontend o'z Spring Boot servisiga `@RestController`/GraphQL orqali murojaat qiladi, CORS `@CrossOrigin` yoki `CorsConfigurationSource` bilan sozlanadi, static asset'lar `src/main/resources/static` dan yoki CDN'dan beriladi. Edge'da Spring Cloud Gateway path-based routing (`/billing/**` → billing frontend + API) bilan bir origin ko'rinishini yaratadi, bu CORS va cookie muammolarini kamaytiradi. BFF (Backend for Frontend) pattern'i har bir micro frontend uchun alohida Spring Boot modul sifatida quriladi; autentifikatsiya shell'da OAuth2 (`spring-boot-starter-oauth2-client` bilan BFF rejimida, token brauzerga chiqarilmaydi) orqali hal qilinadi.

**Qo'llanish keyslari:**
- Katta SaaS konsolida "Billing", "Users" va "Analytics" modullarini alohida jamoalar mustaqil deploy qilishi.
- Webpack/Vite Module Federation bilan remote modullarni runtime'da yuklab, har birini o'z CI/CD'si bilan chiqarish.
- Legacy Angular portaliga yangi React widget'ini web component sifatida qo'shish.
- Dashboard'da har bir widget o'z servisidan ma'lumot olishi va biri ishlamasa qolgani ishlashi.
- Mobil va web klientlar uchun alohida BFF qurib, har biriga mos payload shakllantirish.

**Widget larni iFrame bilan ulamang.** iFrame tarixda ko'p ishlatilgan, lekin bo'laklarni bitta sahifaga ulash uchun undan qochish kerak: o'lcham masalalari va sahifa bo'laklari orasida aloqa qurishning qiyinligi. O'rniga widget server tomonda shablon bilan qo'yiladi yoki mijoz tomonda brauzerga dinamik kiritiladi. Ikki holatda ham widget sahifaning boshqa qismlari bilan bir xil brauzer sahifasida ishlaydi, shuning uchun ular bir-biriga xalaqit bermasligini ta'minlash kerak; widgetlar orasidagi aloqa uchun esa brauzerning o'z hodisa mexanizmi ishlatiladi (masalan chart widget `Album Selected` custom event chiqaradi, tavsiya va tafsilot widgetlari unga obuna bo'ladi) - bu servislar orasidagi hodisaga asoslangan aloqaning sahifa ichidagi ko'rinishi.

**Sahifa og'irligi uchun avtomatik ogohlantirish.** Widget asosidagi SPA da bitta widget bog'liqligining kichik o'zgarishi juda ko'p yangi tranzitiv bog'liqlik olib kirib sahifa hajmini keskin oshirishi mumkin: natijada bir sahifaga React freymvorkining bir nechta versiyasi va ularning bog'liqliklari tushadi. Shuning uchun sahifa og'irligi muhim bo'lgan interfeysda hajm belgilangan chegaradan oshganda ogohlantiradigan avtomatik tekshiruv qo'yiladi. Alohida bundle qilish ishi bir martalik narx, sahifa hajmi esa doimiy nazorat talab qiladi.

**Kesishgan imkoniyat widget ga ham, sahifaga ham sig'maydi.** Mikro frontend modelining Newman hal qila olmagan deb ataydigan muammosi: servis imkoniyati ba'zan widget yoki sahifaga tabiiy joylashmaydi. Tavsiyalarni sahifadagi qutida ko'rsatish oson, lekin qidiruvda yozish paytida tavsiyalarni avtomatik yangilash kerak bo'lsa, u bir nechta bo'lakni kesib o'tadi. Qoida: o'zaro ta'sir qancha ko'p kesishsa, model shuncha kam mos keladi va yechim oddiy API chaqiruviga qaytadi.

**Ehtiyot bo'ling:** Shared dependency (React, dizayn tizimi) versiyalarini muvofiqlashtirmasa bundle hajmi va runtime konflikt muammolari paydo bo'ladi, SEO va first-contentful-paint esa server-side kompozitsiyadan yomonroq bo'lishi mumkin. Autentifikatsiya tokenini brauzer `localStorage`'ida saqlash XSS xavfini oshiradi - BFF + `HttpOnly` cookie yondashuvi afzal; shuningdek cross-module global state'ni iloji boricha kamaytiring, aks holda mustaqillik illyuziyaga aylanadi.

```javascript
// Klient tomonda UI kompozitsiyasi: brauzer bo'laklarni o'zi yig'adi
async function renderHome() {
  const [orders, promos] = await Promise.allSettled([
    fetch('/api/orders/recent').then(r => r.json()),
    fetch('/api/promos/active').then(r => r.json()),
  ]);
  // allSettled: bitta bo'lak yiqilsa sahifa yiqilmaydi
  if (orders.status === 'fulfilled') mountOrders(orders.value);
  if (promos.status === 'fulfilled') mountPromos(promos.value);
}
// Narxi: chaqiruv soni ko'payadi va birinchi renderlash sekinlashadi.
// BFF yoki API composition bilan bu kamayadi.
```

## 14.27 API Gateway (API Gateway)

**Tavsif:** Barcha tashqi client'lar uchun yagona kirish nuqtasini yaratadi va so'rovlarni orqadagi microservice'larga routing qiladi. Gateway qatlamida cross-cutting vazifalar - autentifikatsiya, rate limiting, TLS termination, so'rov/javob transformatsiyasi, circuit breaking - bir joyda markazlashadi. Natijada client'lar o'nlab host'ni bilishi va har biri bilan alohida shartnoma tuzishi shart emas. Shu bilan birga gateway tizimning yagona kirish nuqtasi bo'lgani uchun uning o'zi ham yuqori darajada available bo'lishi talab qilinadi.

**Spring'da qayerda uchraydi:** `spring-cloud-starter-gateway-server-webflux` (Spring Cloud Gateway) - reactive, Spring WebFlux va Netty ustida ishlaydi; `RouteLocator`/`RouteLocatorBuilder` bean'i yoki `application.yml` ichidagi `spring.cloud.gateway.server.webflux.routes` orqali route e'lon qilinadi. Predicate'lar (`Path`, `Host`, `Method`, `Header`) va filter'lar (`StripPrefix`, `RewritePath`, `CircuitBreaker`, `RequestRateLimiter`, `Retry`) GatewayFilterFactory sifatida keladi; o'z filter'ingiz uchun `GlobalFilter` yoki `AbstractGatewayFilterFactory` implement qilinadi. Spring Boot 3.x/4.x da `spring-cloud-gateway-server-webmvc` varianti blocking (Servlet) stack uchun ham mavjud. `RequestRateLimiter` odatda `RedisRateLimiter` bilan, xavfsizlik esa `spring-boot-starter-oauth2-resource-server` va `spring-security` ReactiveSecurityFilterChain bilan birga quriladi. Service discovery bilan integratsiya `lb://service-name` URI va `DiscoveryClientRouteDefinitionLocator` orqali amalga oshadi.

**Qo'llanish keyslari:**
- Mobil va web client'lar uchun yagona public HTTPS endpoint ochish va orqadagi 40 ta service'ni yashirish.
- JWT tekshiruvini gateway'da bajarib, downstream service'larga ishonchli header (`X-User-Id`) uzatish.
- Public API uchun Redis asosidagi rate limiting bilan bir client'ni sekundiga N so'rovga cheklash.
- Legacy monolitdan microservice'ga bosqichma-bosqich o'tishda trafikni path bo'yicha yangi service'ga yo'naltirish (strangler).
- Canary release'da header yoki weight predicate bilan trafikning 5%'ini yangi versiyaga berish.

**Gateway umumiy qolishi kerak: agregatsiya ham, protokolni qayta yozish ham unda emas.** Newman gateway va mesh dagi umumiy xulq servisning aniq xulqidan mustaqil bo'lishi shartini qo'yadi va uch xil noto'g'ri ishlatishni sanaydi. **Agregatsiya:** boshi zararsiz ko'rinadi (ikki chaqiruvni birlashtirib bitta payload qaytarish), keyin o'sha oqimga yana bir downstream chaqiruv qo'shiladi, keyin shartli mantiq kerak bo'ladi va oxirida asosiy biznes jarayoni bu ishga mos bo'lmagan uchinchi tomon vositasining ichiga yozilgan bo'lib chiqadi. Agregatsiya va filtrlash kerak bo'lsa GraphQL yoki BFF ni oling; agregatsiya mohiyatan biznes jarayoni bo'lsa uni aniq modellashtirilgan saga qiladi. **Protokolni qayta yozish:** "har qanday SOAP API ni REST ga aylantiramiz" degan da'vo noto'g'ri, chunki REST butun arxitektura yondashuvi va proxy qatlamida amalga oshmaydi; protokol tarjimasi oraliq qatlamga emas, servisning o'ziga tegishli. **Ichki chaqiruvlar:** gateway ni barcha servislararo (east-west) chaqiruv uchun vositachi qilish kamida bitta qo'shimcha tarmoq hop qo'shadi va bu masala uchun service mesh ancha mos.

Ikkisining ildizi bitta: "pipe lar sodda, endpointlar aqlli" qoidasi buziladi. Aqlni kodda ushlash mustaqil deploy qilish imkonini saqlaydi, oraliq qatlamga ko'chirilgan mantiq esa qattiq nazorat ostida bo'ladi - jamoalarga markaziy gateway ni o'zi o'zgartirishga ruxsat berilmaydi, demak har o'zgarish gateway jamoasiga tiket bo'lib boradi va yetkazish sekinlashadi. Mahsulot DSL ida ishlash buni kuchaytiradi: Java o'rniga vendor ning JSON konfiguratsiyasida marshrut qoidalari yoziladi, keyin o'sha agregatsiya naqshi aslida alohida servisga arzigulik domen funksiyasi ekani ma'lum bo'lganda uni ko'chirish qiyin bo'ladi, chunki mantiqni qaytadan yozish kerak. Eng yomon holatda agregatsiya qiladigan gateway o'ziga alohida jamoa talab qiladi va bitta funksiyani chiqarish uchun frontend jamoasi, gateway jamoasi va servis jamoasi ketma-ket o'zgarish kiritishi kerak bo'ladi. Newman ning yon sharti: API kalitlarini boshqarish, autentifikatsiya va marshrutlash kabi umumiy vazifalar uchun tayyor gateway mahsulotini olish to'g'ri, filtrlash va agregatsiyani esa undan tashqarida qoldirish kerak.

**Ehtiyot bo'ling:** Gateway'ga business logika yuklash eng keng tarqalgan xato - u tezda yangi monolitga va har bir jamoa uchun deployment bottleneck'ga aylanadi. Shuningdek Spring Cloud Gateway reactive bo'lgani uchun filter ichida blocking JDBC yoki `RestTemplate` chaqirmang, aks holda Netty event loop thread'lari band bo'lib butun gateway qotib qoladi.

**Gateway ning o'zi SPOF bo'lib qolmasin:** gateway hamma trafik o'tadigan bo'g'iz, shuning uchun Carnell uchta ekspluatatsiya qoidasini qo'yadi (Carnell, 6-bob, 156-bet):

- **Gateway nusxalarini LB orqasiga qo'ying.** Bir nechta gateway nusxasining oldiga load balancer qo'yish to'g'ri dizayn va gateway ni masshtablanadigan qiladi; lekin LB ni har bir servis nusxasining oldiga qo'yish bo'g'iz yasaydi.
- **Gateway kodi stateless bo'lsin.** Xotirada hech qanday ma'lumot saqlanmaydi: aks holda uni hamma nusxaga replikatsiya qilish kerak bo'ladi va masshtab cheklanadi.
- **Gateway kodi yengil bo'lsin.** Filter ichidagi murakkab mantiq va bir nechta baza chaqirig'i keyinchalik topilishi qiyin performance muammosining manbasiga aylanadi.

**Filter zanjiri va tartibi:** Carnell filterlarni uch turga ajratadi (Carnell, 6-bob, 170-bet): **pre** - maqsadga yuborishdan oldin ishlaydi, xabar shaklini bir xillashtiradi (muhim HTTP header lar joyidami) va darvozabon sifatida autentifikatsiya va avtorizatsiyani tekshiradi; **route** - chaqiruvdan oldin aralashib, marshrutni dinamik o'zgartiradi, masalan trafikning kichik qismini servisning yangi versiyasiga yuboradi; **post** - javob klientga qaytayotganda ishlaydi, javobni loglaydi, xatoni ishlaydi yoki maxfiy ma'lumot chiqib ketmayotganini tekshiradi. Har bir filter o'z turi ichidagi tartib raqamini e'lon qiladi (Carnell, 6-bob, 174-bet), ya'ni "qaysi filter avval ishlaydi" savoli taxminga qoldirilmaydi.

Spring Cloud Gateway da bu uch tur alohida sinf emas: `GlobalFilter` yoki `AbstractGatewayFilterFactory` ichida `chain.filter(exchange)` dan OLDINGI kod pre, qaytgan `Mono` ga ulangan `.then(Mono.fromRunnable(...))` esa post vazifasini bajaradi; marshrutni o'zgartirish `exchange.getAttributes().put(GATEWAY_REQUEST_URL_ATTR, ...)` bilan route filter o'rnini bosadi, tartib esa `Ordered` yoki `OrderedGatewayFilter` bilan beriladi. Global filter hamma marshrutga, `GatewayFilterFactory` esa faqat o'zi yozilgan marshrutga tegadi. ESLATMA: kitobda bu Netflix Zuul ning `ZuulFilter` sinfi va uning `filterType()`, `filterOrder()`, `shouldFilter()`, `run()` metodlari bilan ko'rsatilgan; Zuul endi maintenance rejimida, shuning uchun qoida bu yerda Spring Cloud Gateway nomlari bilan yozilgan.

**Timeout ni gateway dan servisga qarab moslash:** gateway ning timeouti orqadagi servisning javob vaqtidan kichik bo'lsa, servis ishlab tursa ham klient 500 oladi. Carnell ning stackida ikki qiymat bir-birining ustida turadi: circuit breaker standart bir soniyadan keyin uzadi, uning tashqarisidagi klient kutubxonasi esa besh soniyadan keyin uzadi, shuning uchun besh soniyadan uzun chaqiruv uchun IKKALASI ham ko'tarilishi kerak (Carnell, 6-bob, 169-bet). Spring Cloud Gateway da bu global `spring.cloud.gateway.server.webflux.httpclient.connect-timeout` va `.response-timeout`, marshrut darajasida `metadata.response-timeout`, hamda `CircuitBreaker` filtri ishlatilsa Resilience4j `TimeLimiter` ning `timeoutDuration` qiymati. Qiymatlarni yakka emas, zanjir sifatida sozlash qoidasi [timeout budjeti](17-resilience-va-cloud-dizayn-patternlari.md#1741-timeout-budjeti--deadline-propagatsiyasi-timeouts-budget--deadline-propagation) bo'limida.

```yaml
spring:
  cloud:
    gateway:
      default-filters:
        - name: RequestSize
          args: {maxSize: 1MB}
      routes:
        - id: orders
          uri: lb://orders-service
          predicates: [Path=/api/orders/**]
          filters:
            - StripPrefix=1
            - name: CircuitBreaker
              args: {name: ordersCb, fallbackUri: 'forward:/fallback/orders'}

# Gateway chegarada: autentifikatsiya, rate limit, so'rov hajmi va
# marshrutlash. Biznes logika gateway'ga kirmasligi kerak: aks holda u
# yashirin monolitga aylanadi va barcha jamoa unga bog'lanadi.
```

## 14.28 Frontend uchun Backend (Backend for Frontend)

**Tavsif:** Yagona umumiy API o'rniga har bir client turi - iOS, Android, web SPA, hamkor API - uchun alohida backend qatlami quriladi. Har bir BFF faqat o'z client'iga kerakli ma'lumotni downstream service'lardan yig'adi, keraksiz field'larni tashlab, aynan o'sha UI ekranlariga mos shaklda qaytaradi. Bu mobil client'da over-fetching va chatty network chaqiruvlarini kamaytiradi hamda UI jamoasiga o'z backend'ini mustaqil deploy qilish imkonini beradi. Amalda BFF - bu bitta client'ga tegishli, o'sha client jamoasi egalik qiladigan ixtisoslashgan aggregator.

**Spring'da qayerda uchraydi:** Har bir BFF odatda alohida Spring Boot 3.x ilovasi: `@RestController` + `WebClient` (reactive) yoki `RestClient` (Spring Framework 6.1+ dan, blocking) orqali downstream'ga parallel chaqiruvlar. Reactive BFF'da `Mono.zip(...)`/`Flux.zip(...)` bilan bir nechta service javobi birlashtiriladi; blocking stack'da Java 21+ virtual thread (`spring.threads.virtual.enabled=true`) yoki structured concurrency bilan parallel yig'ish qilinadi. Deklarativ client uchun `@HttpExchange` + `HttpServiceProxyFactory` (Spring interface clients) yoki Spring Cloud OpenFeign ishlatiladi. Sessiya va token almashinuvi uchun `spring-boot-starter-oauth2-client` bilan "token-mediating BFF" namunasi keng qo'llanadi: browser'da faqat HttpOnly cookie, access token esa BFF'da saqlanadi (`OAuth2AuthorizedClientManager`). GraphQL variantida `spring-boot-starter-graphql` va `@SchemaMapping`/`@BatchMapping` ishlatiladi.

**Qo'llanish keyslari:**
- Mobil ilova uchun bitta "home screen" endpoint'i yasash: 5 ta service javobini bitta ixcham JSON'ga yig'ish.
- SPA uchun token-mediating BFF: access token'ni browser'ga chiqarmaslik, faqat secure cookie bilan ishlash.
- Smart TV yoki kiosk kabi kam imkoniyatli client'ga yengillashtirilgan, oldindan formatlangan response berish.
- Hamkorlar (partner) uchun public API'ni ichki model'dan ajratilgan alohida shartnoma bilan taqdim etish.
- Web va mobil UI'ni turli tezlikda rivojlantirish: har bir BFF mustaqil release cycle'da bo'ladi.

**Qancha BFF kerak: bitta tajriba, bitta BFF.** Bir xil tajribani turli platformada yetkazishda ikki model uchraydi. Newman afzal ko'rgani va amalda ko'proq ko'rgani qat'iy model: har mijoz turiga alohida BFF (REA da iOS va Android ilovalari o'xshash funksiyani qoplasa ham har biri o'z BFF iga ega edi). Varianti - bir xil TURDAGI interfeys uchun bitta BFF ni bo'lishish: SoundCloud ning Listener ilovasi Android va iOS da bitta BFF ishlatadi. Ikkinchi modelning xavfi oshkor: bitta BFF ga qancha ko'p mijoz turi tushsa, u bir nechta mas'uliyatni o'z ichiga olib shishish ehtimoli shuncha yuqori; muhim sharti esa mijozlar bir SINF interfeysga tegishli bo'lishi, ya'ni SoundCloud ning boshqa native ilovalari boshqa BFF ishlatadi. Ajratuvchi mezon tashkiliy: Android va iOS ilovasiga hamda BFF ga bitta jamoa egalik qilsa umumiy BFF maqbul, jamoalar ayri bo'lsa qat'iy model tavsiya qilinadi (Conway qonuni). Stewart Gleadow ning qisqa qoidasi: "bitta tajriba, bitta BFF" - tajribalar o'xshash bo'lsa bitta BFF ni oqlash oson, keskin ajralsa alohida BFF to'g'ri. SoundCloud injenerlari o'zlari ham bitta mobil jamoa amalda Android va iOS mutaxassislariga bo'linib, har biri ko'proq bitta ilovada ishlagani uchun qarorni qayta ko'rib chiqishi mumkinligini aytgan. BFF lar orasidagi takrorlanishni darhol birlashtirishga shoshilmaslik kerak; umumiy kodni ajratish vaqti kelganda ikki yo'l bor - umumiy kutubxona (arzon, lekin bog'lanish manbai) yoki yangi servis (ajratilgan narsa domen funksiyasi bo'lsa to'g'ri), va "uchinchi marta ishlatilganda abstraksiya yasash" qoidasi servis darajasida ham ishlaydi.

**BFF qachon o'zini oqlaydi.** Faqat veb interfeysi bo'lgan ilovada BFF server tomonda sezilarli agregatsiya kerak bo'lgandagina ma'noga ega, chunki desktop veb odatda quvvatli qurilma va yaxshi ulanishda ishlaydi, ya'ni bir nechta downstream chaqiruvni brauzer o'zi ko'taradi; aks holda yuqoridagi UI kompozitsiya texnikalari yetadi. Server tomonda UI ning katta qismi shablon bilan yasalsa, BFF shu ish uchun tabiiy joy va keshlash ham osonlashadi: BFF oldiga reverse proxy qo'yib agregatsiya natijasini keshlash mumkin. Mobil interfeys yoki uchinchi tomon uchun maxsus funksiya kerak bo'lishi bilan esa har mijoz uchun BFF ni boshidan ko'rib chiqish kerak; qo'shimcha servis deploy qilish narxi yuqori bo'lsa qayta o'ylash mumkin, lekin UI quruvchi odamlar va downstream servislar orasida masofa katta bo'lsa BFF yanada kuchli tanlovga aylanadi.

**Tashqi tomonga alohida BFF buzuvchi o'zgarish ta'sirini cheklaydi.** Royalti ma'lumotini oladigan hamkor yoki set-top box kabi tashqi iste'molchilar foydalanuvchi interfeysi emas, lekin bir xil pattern ishlaydi. Ularning qiymati shundaki, tashqi tomonlar o'z chaqiruvlarini o'zgartirish imkoniga (yoki xohishiga) deyarli ega emas: markaziy API da ularning kichik qismi uchun eski versiyalarni ushlab turishga majbur bo'lasiz. Har tomonga alohida BFF berilsa bu muammo sezilarli kamayadi: bitta tomon uchun API ni mos kelmaydigan tarzda o'zgartirish qolgan tomonlarga tegmaydi.

**Foydalanuvchi turi bo'yicha alohida gateway.** Mijoz turi bo'yicha ajratishning yonida ikkinchi o'q bor: foydalanuvchi turi. Richards va Ford ning risk storming misolida tibbiy tashxis tizimining hamma chaqiruvlari (o'z-o'ziga xizmat, administrator va hamshira) bitta API gateway orqali o'tgani, har chaqiruvda xavfsizlik tekshiruvi bo'lishiga qaramay, yuqori xavf deb baholangan: administrator yoki o'z-o'ziga xizmat interfeysidan kelgan so'rov tibbiy yozuvlar almashish interfeysiga yetib borishi mumkin. Yechim - har foydalanuvchi turi uchun alohida gateway, shunda noto'g'ri turdagi so'rov nozik servisga hech qachon yetmaydi. BFF dan farqi: BFF payload shaklini mijoz turiga moslaydi, bu ajratish esa hujum yuzasini foydalanuvchi turiga qarab kesadi.

**Ehtiyot bo'ling:** Client turlari ko'paygani sayin BFF'lar soni ortib, ularda bir xil logika takrorlanadi - umumiy qoidalarni downstream service'ga yoki shared kutubxonaga chiqarmasa, maintenance narxi keskin oshadi. BFF'ni "hamma uchun bitta" qilib qo'ysangiz, u oddiy API Gateway'ga aylanadi va BFF pattern'ining asosiy foydasi yo'qoladi.

```java
// BFF: bitta mijoz turi uchun moslashtirilgan API
@RestController
@RequestMapping("/bff/mobile")
class MobileHomeController {
    private final OrderClient orders;
    private final PromoClient promos;

    @GetMapping("/home")
    MobileHome home(@AuthenticationPrincipal Jwt jwt) {
        // Mobil ekran uchun minimal to'plam: 1 chaqiruv, kichik payload
        return new MobileHome(orders.lastThree(jwt.getSubject()),
                              promos.activeBanner());
    }
}
// Har mijoz turi uchun o'z BFF si: mobil, veb va hamkor API si
// bir-birining ehtiyoji uchun murosaga kelmaydi. Narxi: yana bir
// deploy birligi va takrorlanish xavfi.
```

## 14.29 Microservice Shassi (Microservice Chassis)

**Tavsif:** Har bir microservice'ga kerak bo'ladigan infratuzilma imkoniyatlari - configuration, logging, metrics, health check, tracing, security, exception handling - qayta-qayta yozilmasligi uchun yagona asos (chassis) sifatida tayyorlanadi. Jamoa yangi service boshlaganda bu chassis'ni olib, faqat business logikani yozadi. Natijada cross-cutting masalalar bir joyda standartlashadi va butun landscape bo'ylab bir xil ishlaydi. Chassis odatda kutubxona (starter) yoki template ko'rinishida yetkaziladi.

**Spring'da qayerda uchraydi:** Spring Boot'ning o'zi de-facto chassis: auto-configuration, `spring-boot-starter-actuator` (health, metrics, `/actuator/prometheus`), Micrometer + Micrometer Tracing (OpenTelemetry/Brave bridge), `spring-boot-starter-validation`, Spring Cloud Config/Consul client, Resilience4j. Tashkilot darajasida o'z chassis'ingiz custom starter sifatida qilinadi: `spring.factories` o'rniga Boot 3.x da `META-INF/spring/org.springframework.boot.autoconfigure.AutoConfiguration.imports` fayliga `@AutoConfiguration` sinflari yoziladi, `@ConditionalOnMissingBean`/`@ConditionalOnProperty` bilan override imkoniyati qoldiriladi, `@ConfigurationProperties` bilan sozlamalar e'lon qilinadi. Umumiy xato formati `@ControllerAdvice` + `ProblemDetail` (RFC 9457, 7807 ni almashtirgan) orqali, correlation ID `ObservationRegistry` yoki MDC filter orqali markazlashtiriladi.

**Qo'llanish keyslari:**
- Barcha service'larda bir xil `ProblemDetail` xato formati va error code taksonomiyasini majburlash.
- Kompaniya standartidagi observability (tracing, metrics, structured JSON logging) ni bitta starter bilan yoqish.
- Ichki service-to-service autentifikatsiya (mTLS yoki OAuth2 client credentials) ni avtomatik sozlash.
- Umumiy Kafka producer/consumer sozlamalari, retry va DLT (dead-letter topic) siyosatini bir joyda belgilash.
- Yangi service'ni bir kun ichida production-ready holatda ko'tarish (health probe, graceful shutdown, readiness).

**Ehtiyot bo'ling:** Chassis'ga business logika yoki domain model kirib qolsa, u shared library coupling'ga aylanadi va har bir versiya yangilanishi butun landscape'ni bir vaqtda deploy qilishga majbur qiladi. Versiyalashni jiddiy oling: chassis'ning major versiyasi uzun muddat qo'llab-quvvatlanishi va service'lar o'z tezligida migratsiya qilishi mumkin bo'lsin.

```java
// Chassis: har servisda takrorlanadigan infratuzilma bitta starter'da
@AutoConfiguration
public class ChassisAutoConfiguration {

    @Bean @ConditionalOnMissingBean
    CorrelationIdFilter correlationIdFilter() { return new CorrelationIdFilter(); }

    @Bean @ConditionalOnMissingBean
    ProblemDetailExceptionHandler problemDetailHandler() {
        return new ProblemDetailExceptionHandler();
    }

    @Bean @ConditionalOnMissingBean
    HealthIndicator chassisHealth() { return new ChassisHealthIndicator(); }
}
// Natija: yangi servis kuzatuvchanlik, xato formati va health bilan tug'iladi.
// Xavf: chassis o'sib ketsa shared library bog'liqligiga aylanadi (14.36),
// shuning uchun unga biznes logika kirmasligi kerak.
```

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

**Strategiyani kech tanlash tasodifiy murakkablik yasaydi:** Carnell bir moliya kompaniyasidagi holatni keltiradi: ilova sozlamalari qo'lda boshqarilgan property fayllarda, source control dan tashqarida yashagan; 120 ilova, to'rt muhit va har ilovaga bir necha node ko'paytmasi natijasida ko'chirish kerak bo'lgan sozlama fayllari soni 12 000 ga chiqqan (Carnell, 3-bob, 66-bet). Boshida strategiya kichik ilovalar guruhi uchun o'ylangan, keyin ilovalar soni besh yil ichida portlagan, qayta ishlash uchun esa vaqt ham, pul ham ajratilmagan. Ikki oylik konsolidatsiyadan keyin hammasi 20 ta versiyalangan faylga tushgan.

Bundan ikkita amaliy qoida chiqadi. Birinchisi: konfiguratsiyani tashqariga chiqarish qarorining o'zi yetarli emas, uni qanday saqlash va versiyalash ham birinchi servisdan oldin hal qilinadi - tashqi konfiguratsiya bu yangi tashqi bog'liqlik va u boshqarilishi kerak. Ikkinchisi: fayl soni ilova soniga emas, muhit va node soniga ko'paytirilib o'sadi, shuning uchun "nechta fayl bo'ladi" savoliga javob ko'paytma shaklida hisoblanadi.

```yaml
spring:
  config:
    import:
      - optional:configserver:http://config-server:8888
      - optional:file:/etc/app/application.yml

# Kubernetes'da ConfigMap va Secret:
#   envFrom:
#     - configMapRef: {name: orders-config}
#     - secretRef: {name: orders-secrets}

# Qoidalar:
#  - bir xil image barcha muhitda ishlaydi
#  - sir image ichida yoki git da bo'lmaydi
#  - majburiy kalit yo'q bo'lsa startup yiqiladi (@Validated + @NotBlank)
```

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

**Initializr ni to'rt yo'ldan chaqirish:** Spring Initializr - bitta veb sahifa emas, bir vaqtda brauzer ilovasi va REST API (Walls, 1-bob, 7-bet). Shu sababli shablonni odam ham, skript ham bir xil manbadan oladi:

- **Veb:** `start.spring.io` da build tizimi, til, Boot versiyasi, group va artifact ID tanlanadi, bog'liqlik qidiruv maydonidan qo'shiladi va `Explore` tugmasi generatsiya qilinadigan loyihani yuklamasdan ko'rsatadi (Walls, A-ilova, 469-471-betlar).
- **`curl`:** `curl https://start.spring.io/starter.zip -o demo.zip` eng sodda shakl; parametrlar `-d dependencies=web,data-jpa`, `-d type=gradle-project`, `-d baseDir=my-dir` ko'rinishida beriladi, `starter.tgz` esa to'g'ridan-to'g'ri `tar -xzvf -` ga quvur qilinadi. Parametrlar va standart qiymatlar ro'yxatini `curl https://start.spring.io` ning o'zi qaytaradi (Walls, A-ilova, 472-475-betlar).
- **Boot CLI:** `spring init` xuddi shu API ni buyruq qatoridan chaqiradi.
- **IDE:** Spring Tool Suite, IntelliJ IDEA va NetBeans da yangi loyiha ustasi shu API ga uradi; ustadagi `Base Url` maydoni esa kompaniya ichidagi o'z Initializr nusxasiga yo'naltirish uchun (Walls, 1-bob, 11-bet).

Natija har qanday yo'lda bir xil Maven yoki Gradle tuzilmasi: kod `src/main/java`, test `src/test/java`, Java bo'lmagan resurslar `src/main/resources` ichida (Walls, 1-bob, 11-bet). Shablon uchun muhimi shu: generatsiya skript qilinadigani uchun "yangi servis" qadamini CI ga yoki o'z scaffolding asbobingizga ulash mumkin, qo'lda tugma bosish shart emas.

```text
my-service/
  pom.xml                   # chassis starter, qadalgan versiyalar
  Dockerfile                # layered jar, non-root user
  .github/workflows/ci.yml  # build, test, Sonar, image push
  src/main/resources/application.yml
  src/main/java/.../Application.java
  src/test/java/.../ArchitectureTest.java   # ArchUnit qoidalari
  README.md                 # on-call, runbook havolasi, SLO

Shablon kodni ko'chirmaydi, balki yangi servisni mavjud standartga
moslaydi: CI, kuzatuvchanlik, xavfsizlik va test darvozalari tayyor.
```

## 14.32 Sidecar (Sidecar)

**Tavsif:** Yordamchi funksionallik asosiy ilova process'iga emas, balki u bilan bir xil deployment unit'da (Kubernetes'da bir pod'da) yonma-yon ishlaydigan alohida container'ga joylashtiriladi. Sidecar asosiy ilova bilan localhost va umumiy volume orqali gaplashadi, shuning uchun til va framework'dan mustaqil bo'ladi. Shu yo'l bilan log yig'ish, proxy, secret yangilash yoki config sync kabi vazifalar ilova kodiga tegmasdan qo'shiladi. Ayni paytda sidecar asosiy container bilan bir xil hayot tsiklini va resurs cheklovini bo'lishadi.

**Spring'da qayerda uchraydi:** Spring Boot ilovasi sidecar'ni bilmasligi mumkin, lekin integratsiya nuqtalari bor: strukturali log'ni stdout'ga chiqarish (Boot 3.4+ dagi `logging.structured.format.console=ecs|logstash|gelf`) va Fluent Bit/Vector sidecar'i uni yig'ishi; metrics'ni `/actuator/prometheus` orqali berish; `OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4318` bilan OpenTelemetry Collector sidecar'iga eksport qilish (`micrometer-tracing-bridge-otel` + `opentelemetry-exporter-otlp`). Graceful shutdown muhim: `server.shutdown=graceful` va `spring.lifecycle.timeout-per-shutdown-phase`. Polyglot holatda Spring Cloud Netflix'ning `spring-cloud-netflix-sidecar` moduli non-JVM service'ni Eureka'ga ro'yxatdan o'tkazish uchun ishlatilgan (hozir legacy). Kubernetes 1.29+ da sidecar'lar `initContainers` ichida `restartPolicy: Always` bilan e'lon qilinadi.

**Qo'llanish keyslari:**
- Fluent Bit sidecar'i bilan log'ni ilova kodiga tegmasdan markazlashtirilgan tizimga yuborish.
- OpenTelemetry Collector sidecar'ini qo'yib, tracing eksport sozlamalarini barcha service'larda bir xil qilish.
- Vault Agent Injector sidecar'i bilan secret'larni fayl ko'rinishida yangilab berish.
- Legacy non-Java service'ga TLS va retry'ni proxy sidecar orqali qo'shish.
- Database'ga ulanish uchun Cloud SQL Auth Proxy sidecar'ini ishlatish va ilovada oddiy localhost JDBC URL qoldirish.

**Sidecar faqat operatsion bog'lanish uchun.** Sidecar va service mesh ning maqsadi operatsion bog'lanishni bir joyga yig'ish: logging, monitoring, service discovery, autentifikatsiya va avtorizatsiya, circuit breaker - infratuzilmaning domen mas'uliyati yo'q qismlari. Ford va boshqalarning qat'iy qoidasi: `Address` yoki `Customer` kabi umumiy DOMEN sinflarini sidecar ga qo'ymang. Ikki servisga bir xil sinf ta'rifi kerak bo'lsa, uni sidecar ga qo'yish "ikkisini bir vaqtda o'zgartirishga majburlash" degani, ya'ni mikroservisda aynan qochiladigan bog'lanish; bu masala sinf ulashish bilan emas, kontrakt bilan hal qilinadi. Chegara chizig'i har doim keskin emas: texnik utility (masalan 17 jamoadan 5 tasi ishlatadigan JSON dan XML ga o'girgich) uchun javob trade-off tahliliga qoladi va ikki mezonga qarab beriladi - yetarlicha jamoa ishlatadimi va sidecar hajmi oshishi maqbulmi. Sidecar arxitekturaning eng katta qismiga aylanmasligi kerak. Egalik modeli ham aniqlanadi: sidecar jamoalar o'rtasida bo'linadi yoki markazlashgan infratuzilma jamoasi uni yuritadi; Ford va boshqalarning misolida alohida infratuzilma jamoasi sidecar ni servisga ulangandan keyin avtomatik tekshiradigan fitness funksiyali deploy pipeline'i bilan birga boshqaradi.

**Ehtiyot bo'ling:** Sidecar asosiy container bilan CPU va memory'ni bo'lishadi - resource request/limit'ni to'g'ri bermasangiz, log agent ilovangizni OOMKill'ga olib keladi. Startup va shutdown tartibini ham hisobga oling: proxy sidecar ilovadan oldin tayyor bo'lishi va undan keyin to'xtashi kerak, aks holda deploy paytida qisqa muddatli xatolar paydo bo'ladi.

```yaml
apiVersion: v1
kind: Pod
spec:
  containers:
    - name: app
      image: orders:1.4.2
    - name: log-shipper              # sidecar
      image: fluent-bit:3.0
      volumeMounts:
        - {name: logs, mountPath: /var/log/app}
  volumes:
    - name: logs
      emptyDir: {}

# Afzalligi: ilova tiliga bog'liq emas va alohida yangilanadi.
# Narxi: har pod uchun qo'shimcha xotira va CPU, hamda ishga tushish
# tartibi (sidecar app dan oldin tayyor bo'lishi kerak).
```

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

```yaml
spec:
  containers:
    - name: app
      env:
        - name: PSP_URL
          value: "http://localhost:9000"   # ambassador'ga murojaat qiladi
    - name: ambassador
      image: envoy:1.31
      # Timeout, retry, circuit breaker, mTLS va kuzatuvchanlik
      # shu yerda, ilova kodida emas.

# Afzalligi: resilience siyosati bir joyda va barcha til uchun bir xil.
# Narxi: nosozlikni tashxislashda yana bir qatlam paydo bo'ladi.
```

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

Mesh ning kam aytiladigan, lekin reliz ishonchliligiga eng ko'p ta'sir qiladigan foydasi trafikni boshqarishdan keladi: u deploy ni relizdan ajratadi. Mesh bo'lmagan holatda servisning yangi versiyasini productionga qo'yish uni darhol trafik qabul qiladigan qilib qo'yadi, demak deploy va reliz bitta hodisa. Mesh bo'lsa, yangi versiyani productionga joylab, unga hali trafik yubormasdan sinab ko'rish va faqat shundan keyin trafikni yo'naltirish mumkin bo'ladi (avval nol foiz, keyin bir necha foiz, keyin hammasi). Bu reliz qarorini texnik deploy qarorining ustidan ko'taradi va orqaga qaytarishni trafik yo'nalishini o'zgartirish darajasiga tushiradi. Shu imkoniyat mesh'ga xos emas, lekin mesh uni ilova kodiga tegmasdan beradi; shu g'oyaning boshqa shakllari [Yashirin ishga tushirish](22-deployment-va-operatsion-patternlar.md#2211-yashirin-ishga-tushirish-dark-launch) bo'limida.

```yaml
apiVersion: networking.istio.io/v1
kind: VirtualService
metadata:
  name: inventory
spec:
  hosts: [inventory-service]
  http:
    - timeout: 3s
      retries:
        attempts: 2
        perTryTimeout: 1s
        retryOn: connect-failure,refused-stream   # 5xx ga retry qilmaydi
      route:
        - destination: {host: inventory-service, subset: v1}
          weight: 90
        - destination: {host: inventory-service, subset: v2}
          weight: 10

# Mesh ilova kodini o'zgartirmasdan mTLS, retry va canary beradi.
# Narxi: har pod uchun proxy, yangi nosozlik rejimlari va operatsion
# bilim. Servis soni kichik bo'lsa, mesh foydadan ko'p murakkablik qo'shadi.
```

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

**Kodni nusxalash qachon maqbul.** Umumiy kodni har servis repozitoriyasiga nusxalash (code replication) "hech narsa ulashmaydigan arxitektura" davrida mashhur bo'lgan va amalda tez yiqilgan: nusxadagi nuqsonni yoki muhim o'zgarishni hamma servisda tuzatish juda qiyin va ko'p vaqt oladi. Shunga qaramay u haqli texnika bo'lib qoladi - lekin faqat juda statik, bir martalik koda uchun. Ford va boshqalarning misoli: servisning kirish nuqtasini belgilaydigan `@ServiceEntrypoint` markeri, ya'ni ichida hech qanday funksiya yo'q, nuqsoni yo'q va kelajakda ham paydo bo'lishi kutilmaydigan annotatsiya. Qoida: bu yo'ldan borishdan oldin boshqa usullarni (kutubxona, servis, sidecar) ko'rib chiqing, chunki nusxalash bounded context ni saqlaydi, lekin kod o'zgarishi kerak bo'lganda o'zgartirishni qiyinlashtiradi.

**Kutubxona yoki servis: tanlov ikki mezonda.** Umumiy funksiyani kutubxona qilish va servis qilish orasidagi tanlovni Ford va boshqalar ikki mezonga bog'laydi. **Kutubxona** bir xil texnologiya stekida va umumiy kod kam yoki o'rtacha o'zgaradigan holatda to'g'ri: compile vaqtidagi bog'lanish runtime da hech narsa buzmaydi. **Umumiy servis** polyglot muhitda (bir nechta til va platforma) va umumiy funksiya tez-tez o'zgaradigan holatda to'g'ri: kodni takrorlamaydi va bounded context ni saqlaydi. Servisning narxi ochiq va faqat kechikish emas: endpointni versiyalash kutubxona versiyalashdan ko'ra sub'ektivroq va qiyinroq, chaqiruv kechikish qo'shadi, bog'liqlik tufayli fault tolerance, mavjudlik, masshtab va throughput pasayadi, eng muhimi o'zgarish RUNTIME da ta'sir qiladi - umumiy servisga chiqarilgan nuqson darhol hamma iste'molchiga tegadi, kutubxonada esa yangi versiyani olish qarori iste'molchida qoladi.

**Ehtiyot bo'ling:** "Kod takrorlanmasin" degan niyat bilan domain model'ni ulashish - microservice'da DRY prinsipi coupling'dan muhimroq emas; biroz dublikat kod mustaqil deploy'dan arzonroq turadi. Agar shared kutubxona qolsa, uning backward-compatible versiyalash siyosatini va bir necha major versiyani parallel qo'llab-quvvatlash majburiyatini oldindan belgilang.

```java
// Anti-pattern: umumiy kutubxona servislarni bog'laydi
// company-common 4.2.0:
public class Order { }                 // domen sinfi umumiy kutubxonada
public class OrderStatusMapper { }     // biznes qoida umumiy kutubxonada

// Natijasi: `Order` ga maydon qo'shish uchun barcha servisni yangilash
// va birga deploy qilish kerak. Bu taqsimlangan monolit.

// Qoida: umumiy kutubxonada faqat domen bilan bog'liq bo'lmagan
// infratuzilma qolishi mumkin (correlation ID filtri, log formati).
// Domen sinfi, DTO va biznes qoida umumiy bo'lmaydi: har servis o'z
// nusxasini saqlaydi, hatto maydonlar bir xil bo'lsa ham.
```

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

```sql
-- Taqsimlangan monolitni o'lchash: sinxron chaqiruv zanjiri uzunligi
SELECT trace_id, count(*) AS client_spans
FROM spans
WHERE kind = 'client' AND start_time > now() - interval '1 hour'
GROUP BY trace_id
ORDER BY client_spans DESC
LIMIT 20;

-- Boshqa belgilar:
--  - bitta funksiyani chiqarish uchun 3 servisni birga deploy qilish
--  - servislar bitta bazani bo'lishadi
--  - bitta servis yiqilsa barcha so'rov yiqiladi
-- Davolash: zanjirni asinxron hodisaga aylantirish, lokal nusxa (14.4)
-- yoki servislarni qayta birlashtirish.
```

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

```java
// Nano-service: chegara juda mayda qo'yilgan
@RestController
class TaxRateController {                      // butun servis bitta endpoint
    @GetMapping("/rate") BigDecimal rate() { return new BigDecimal("0.12"); }
}
// Belgilari:
//  - servisda bitta-ikkita endpoint va o'z ma'lumotlari yo'q
//  - har o'zgarish ikki-uch servisga birga tegadi
//  - chaqiruv zanjiri uzun va latency tarmoqdan kelib chiqadi
//
// Narxi: deploy, monitoring, on-call va tarmoq yuki funksiyadan katta.
// Davolash: nano-service'ni egasi bo'lgan servisga qaytarib qo'shish.
```

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

Qarordan oldin tekshiriladigan beshta to'siq bor va ularning har biri dekompozitsiyani imkonsiz yoki juda qimmat qilib qo'yishi mumkin. Birinchi: tarmoq kechikishi - juda mayda bo'linishda bitta so'rov o'nlab servis chaqiruviga aylanadi va kechikish yig'iladi. Ikkinchi: sinxron IPC mavjudlikni tushiradi, chunki zanjirdagi har servisning mavjudligi ko'paytmaga kiradi; buni hal qilish uchun aloqani asinxron qilish kerak va bu o'z navbatida yangi murakkablik. Uchinchi: servislararo ma'lumot izchilligini saqlash tranzaksiya o'rniga [saga](#149-saga-orkestratsiya-saga-orchestration)ni talab qiladi. To'rtinchi va eng ko'p e'tibordan chetda qolgani: ma'lumotning global izchil ko'rinishini olish imkonsiz bo'ladi - agar biznes talabi aynan shunday ko'rinishni so'rasa (bitta so'rovda hamma narsani izchil holatda ko'rish), o'sha ma'lumot bitta servisda qolishi shart. Beshinchisi esa kodda yotadi: god sinflar, ya'ni butun ilova bo'ylab ishlatiladigan va hamma narsani biladigan yirik sinflar, dekompozitsiyani to'sadi va ularni avval bo'lish kerak. Shuning uchun ajratish rejasi diagrammadan emas, shu beshtasini tekshirishdan boshlanadi.

**Yirik servis belgilari:** Carnell granularlikni uchta belgiga qarab tekshiradi (Carnell, 2-bob, 42-bet). **Mas'uliyat ko'pligi:** servisdagi biznes oqimi chalkash va bir-biriga bog'lanmagan juda xilma-xil qoidalarni majburlaydi. **Jadval ko'pligi:** servis o'zi boshqargan ma'lumot uchun yozuv manbasi, shuning uchun bir nechta jadvalga yozish yoki o'z bazasidan tashqaridagi jadvalga murojaat qilish belgi hisoblanadi; Carnell ning mezoni - bitta servis uchtadan beshtagacha jadvalga egalik qilsin, undan ko'pi mas'uliyat ortib ketganini ko'rsatadi. **Test soni:** kichik to'plamdan yuzlab unit va integratsiya testiga o'sgan servis bo'linish arafasida. Teskari tomonda mayda servis belgilari bor: har biri bitta jadval bilan ishlaydigan o'nlab servis, bitta so'rovni bajarish uchun bir-birini doimiy chaqirib turadigan servislar va faqat CRUD dan iborat servis. Shuning uchun **avval servislar bir-biri bilan qanday gaplashishini chizing**: qo'pol interfeysdan maydaga refaktoring qilish teskarisidan arzonroq.

**Jadval bo'yicha bo'lish qachon dalil, qachon xato:** yuqoridagi ogohlantirish jadval asosidagi bo'linishni distributed monolit yo'li deb ataydi, Carnell esa ma'lumot yaxlitligini dekompozitsiya signali qilib beradi va mavjud monolitni soddalashtirilgan data model asosida bo'lakka ajratadi (Carnell, 2-bob, 39-41-betlar). Ikkisi ikki xil narsa haqida va ikkita shart bilan ajraladi. **Bosqich:** Carnell ning keysi mavjud, jadvallari allaqachon qattiq bog'langan monolit; u yerda biznes intervyusidan chiqqan otlar fizik jadvallarga qaytib mos tushadi, ya'ni jadval ro'yxati chegarani YARATMAYDI, intervyudan chiqqan chegarani TASDIQLAYDI. Yangi tizimda esa tasdiqlanadigan jadval yo'q, shuning uchun chegara faqat biznes imkoniyatidan chiqadi. **Donadorlik:** yaxlitlik signali bir-biriga bog'liq jadvallar guruhini (bitta mantiqiy entity, Carnell mezonida uchtadan beshtagacha jadval) bitta egaga beradi; Carnell ning o'zi har biri bitta jadval bilan ishlaydigan servislarni mayda servis belgisi deb sanaydi. Demak zid pozitsiya bitta: jadval ro'yxatini yagona manba qilib olib, har jadvalga bitta servis yozish - bu ikki manbaning ikkisi ham xato deb ataydigan yo'l va u [taqsimlangan monolit](#1437-taqsimlangan-monolit-distributed-monolith---antipattern) bilan tugaydi. Signalning o'zi [biznes imkoniyati bo'yicha dekompozitsiya](#142-biznes-imkoniyati-boyicha-dekompozitsiya-decompose-by-business-capability) bo'limida yozilgan.

```text
Granularlik qarori uchun uch mezon (har biriga raqam bilan javob):

  1. Birga o'zgaradimi?   git tarixidan: ikki modul bir xil commit'da
     necha marta o'zgargan. Yuqori son -> bitta servis.
  2. Birga masshtablanadimi?  metrikadan: RPS va CPU profili bir xilmi.
     Har xil bo'lsa -> ajratish foydali.
  3. Birga yiqiladimi?    bittasi o'chsa ikkinchisi ishlay oladimi.
     Yo'q bo'lsa, ajratish mavjudlikni oshirmaydi, kamaytiradi.

Shubha bo'lsa kattaroq servis tanlanadi: ajratish keyin ham mumkin,
birlashtirish esa ancha qimmat.
```

## 14.40 Saga da izolyatsiya yo'q: anomaliyalar va qarshi choralar

**Tavsif:** Saga tranzaksiya modeli ACID emas, **ACD**: atomarlik, izchillik va chidamlilik bor, izolyatsiya esa yo'q. Bu nazariy nuqta emas, saga yozgan odam hal qilishi kerak bo'lgan masala, chunki izolyatsiyaning yo'qligi uchta anomaliyaga olib keladi.

| Anomaliya | Nima bo'ladi |
|---|---|
| Yo'qolgan yangilanish (lost update) | Bir saga ikkinchi saga qilgan o'zgarishni o'qimasdan uning ustiga yozadi |
| Iflos o'qish (dirty read) | Tranzaksiya yoki saga hali tugamagan saga ning yangilanishini o'qiydi |
| Takrorlanmaydigan o'qish (fuzzy read) | Saganing ikki qadami bir xil ma'lumotni o'qib turli natija oladi |

Birinchi ikkitasi eng ko'p uchraydi va eng qiyin. Kitobdagi misollar aniq. Yo'qolgan yangilanish: `Create Order Saga` ning birinchi qadami buyurtma yaratadi; u ishlayotganda `Cancel Order Saga` buyurtmani bekor qiladi; `Create Order Saga` ning oxirgi qadami buyurtmani tasdiqlaydi, ya'ni bekor qilishni ustiga yozadi va mijoz bekor qilgan buyurtma jo'natiladi. Iflos o'qish: bekor qilish sagasi mijozning kredit limitini bo'shatadi, shu oraliqda `Create Order Saga` kreditni band qiladi, keyin bekor qilish sagasi kompensatsiya bilan kreditni qaytarib kamaytiradi; natijada mijoz kredit limitidan oshgan buyurtma bera oladi.

**Qarshi choralar.** Kitob 1998 yildagi "Semantic ACID properties in multidatabases" maqolasidan oltita qarshi chorani keltiradi. Ularning bir qismi izolyatsiyani ilova darajasida tiklaydi, bir qismi esa izolyatsiya yo'qligining **biznes xavfini** kamaytiradi:

| Qarshi chora | Nima qiladi |
|---|---|
| Semantic lock | Ilova darajasidagi qulf: yozuv `*_PENDING` kabi holatga qo'yiladi va boshqa tranzaksiyalar shunga qarab ish qiladi |
| Commutative updates | Yangilash amallari istalgan tartibda bajarilsa ham bir xil natija bersin |
| Pessimistic view | Saga qadamlarini qayta tartiblab, biznes xavfini kamaytirish |
| Reread value | Ustiga yozishdan oldin ma'lumotni qayta o'qib, o'zgarmaganini tekshirish |
| Version file | Yozuvdagi yangilanishlarni qayd qilib, keyin ularni qayta tartiblash imkonini berish |
| By value | Har so'rovning biznes xavfiga qarab konkurentlik mexanizmini dinamik tanlash |

Eng ko'p ishlatiladigani semantic lock va u yuqoridagi `*_PENDING` holati bilan aynan bir narsa: `APPROVAL_PENDING` holati "bu yozuv hozir saga tomonidan o'zgartirilayapti" degan signal beradi.

**Spring'da qayerda uchraydi:** Semantic lock odatda entity dagi holat maydoni va `@Version` bilan optimistik qulf birgaligida yoziladi; reread value `@Version` yoki `WHERE` sharti bilan shartli `UPDATE` ga aylanadi (`UPDATE ... WHERE status = 'PENDING'` va `rowsAffected` ni tekshirish). Commutative updates ko'pincha `balance = balance + ?` shaklidagi nisbiy yangilanish bilan beriladi, mutlaq qiymat o'rniga. Pessimistic view esa saga qadamlarining tartibini o'zgartirish, ya'ni kodda emas, dizaynda hal qilinadi.

**Ehtiyot bo'ling:** Saga ni "distributed tranzaksiya o'rnini bosadi" deb o'ylash eng qimmat xato. U atomarlikni beradi, izolyatsiyani bermaydi; shuning uchun har bir saga uchun "qaysi anomaliya mumkin va qaysi qarshi chora qo'yildi" savoliga javob yozilishi kerak. Javobsiz saga ishlaydi, lekin yuklama ostida yuqoridagi ikki misoldagi holatga tushadi.

## 14.41 Tilga xos paketlash formati (Language-specific Packaging Format)

**Tavsif:** Servis production'ga o'z tilining tabiiy paket formatida chiqariladi: Java uchun executable JAR yoki WAR, Node.js uchun kod va modullar papkasi, Go uchun OS ga xos ikkilik fayl. Mashinaga avval runtime o'rnatiladi (JDK, WAR bo'lsa Tomcat ham), keyin paket ko'chiriladi va ishga tushiriladi; har bir nusxa alohida JVM process bo'ladi yoki eski application server'da bitta JVM ichidagi bir nechta servisdan biri. Richardson bu patternni ataylab deploy variantlarining birinchisi sifatida beradi: uning kamchiliklari qolgan uchtasini (VM, container, serverless) nega kerak qilganini ko'rsatadi (Chris Richardson, *Microservices Patterns: With examples in Java*, Manning, 2019, 12-bob, 386-390-betlar). Foydasi ikkita: deploy tez va resurs tejamkor, chunki OS hamda ba'zan JVM ham bo'lishiladi. Narxi to'rtta: technology stack kapsulalanmaydi, ya'ni operations har servisning runtime versiyasini bilishi shart; process iste'mol qiladigan resursni chegaralash imkoni yo'q; bitta mashinadagi nusxalar o'zaro izolyatsiyalanmaydi; nusxani qaysi mashinaga joylashni avtomatik hal qilib bo'lmaydi. Shu sababli kitob bu yo'lni faqat samaradorlik boshqa hamma narsadan ustun bo'lgan holatda tavsiya qiladi.

**Spring'da qayerda uchraydi:** Spring Boot'ning standart chiqishi aynan shu pattern: Gradle'da `bootJar`, Maven'da `spring-boot-maven-plugin` ning `repackage` goal'i executable JAR yasaydi va u `java -jar` bilan ishga tushadi. Boot 3 da tashqi Tomcat shart emas, lekin `spring-boot-starter-tomcat` ni `providedRuntime` qilib `bootWar` ham mumkin. Kamchilikni yumshatadigan sozlamalar: `-XX:MaxRAMPercentage` bilan heap'ni mashina xotirasiga nisbatda berish, `server.shutdown=graceful` va `spring.lifecycle.timeout-per-shutdown-phase` bilan to'g'ri to'xtash, `management.endpoint.health.group.readiness.include` bilan alohida readiness guruhi. Ishga tushishni tezlashtirish uchun CDS arxivi (`-XX:ArchiveClassesAtExit`, keyin `-XX:SharedArchiveFile`) yoki `nativeCompile` bilan GraalVM native image. Kitob Spring Boot 2 davrida yozilgani uchun undagi WAR va tashqi web container misoli bugun kam uchraydi, lekin patternning mohiyati o'zgarmagan.

**Qo'llanish keyslari:**
- Bitta VM da ishlaydigan ikki-uchta servisli kichik tizim: container orchestration narxi hali oqlanmagan.
- Kuniga bir marta ishlaydigan ichki batch yoki admin servisini `systemd` unit sifatida qo'yish.
- On-premise yetkazib berish: mijozga JAR fayl va `application.yml` beriladi, qolganini u o'zi boshqaradi.
- Container image qurish taqiqlangan muhitda legacy ilovani Spring Boot ga ko'chirishning birinchi bosqichi.
- Mahalliy va test muhitida `java -jar` bilan tez tekshirish, production esa konteynerda ketadi.

**Ehtiyot bo'ling:** Bitta Tomcat ichiga bir nechta servisni joylash eng xavfli shakl: izolyatsiya umuman yo'q, bitta servisning `OutOfMemoryError` i hammasini o'ldiradi va classloader konflikti kutilmagan joyda chiqadi. Resurs chegarasi yo'qligi "shovqinli qo'shni" muammosini keltiradi, shuning uchun hech bo'lmasa `systemd` darajasida `MemoryMax` va `CPUQuota` qo'yiladi. Operations har servisning JDK versiyasini qo'lda kuzatishi ham xato manbai, shuning uchun bu patterndan [har bir service instance alohida host, VM yoki konteynerda](22-deployment-va-operatsion-patternlar.md#2223-har-bir-service-instance-alohida-host--vm--konteynerda-service-instance-per-host--vm--container) va [servis deploy platformasi](22-deployment-va-operatsion-patternlar.md#2225-servis-deploy-platformasi-service-deployment-platform---kubernetes-paas) ga o'tish yo'li oldindan rejalashtiriladi.

```bash
# Tilga xos paket: Spring Boot executable JAR
./gradlew bootJar                  # build/libs/orders-1.4.2.jar

# Runtime mashinada faqat JDK bor: paket ko'chiriladi va ishga tushadi
java -XX:MaxRAMPercentage=70 -jar orders-1.4.2.jar --server.port=8081

# Patternning asosiy kamchiligi shu buyruqda ko'rinadi: process
# resursini OS darajasida hech narsa chegaralamaydi. Konteynerda bu
# cgroup orqali o'zi chiqadi, bu yerda esa qo'lda qo'yiladi:
systemd-run --unit=orders --property=MemoryMax=2G --property=CPUQuota=150% \
    java -XX:MaxRAMPercentage=70 -jar orders-1.4.2.jar
```

## 14.42 Saga ning sakkiz varianti: uch o'lchamli tanlov (Transactional Saga Patterns)

**Tavsif:** 14.8 va 14.9 saga ning ikki ko'rinishini beradi - xoreografiya va orkestratsiya. Bu haqiqatning bir uchdan biri: `Software Architecture: The Hard Parts` saga ni uch mustaqil o'lcham kesishmasi deb ko'rsatadi va natijada sakkizta nomlangan birikma chiqadi. O'lchamlar: **aloqa** (sinxron yoki asinxron), **izchillik** (atomar yoki yakuniy), **koordinatsiya** (orkestratsiya yoki xoreografiya). Nomlar yonidagi uch harfli ko'rsatkich o'sha uch qiymatni alifbo tartibida qaytaradi, masalan `sao` = synchronous, atomic, orchestrated. Nomlar o'zi qiziq, lekin ularni yodlash shart emas: qiymat uch harfda va reytinglarda.

| Pattern | Aloqa | Izchillik | Koordinatsiya | Bog'lanish | Murakkablik | Javob berish | Masshtab |
|---|---|---|---|---|---|---|---|
| Epic Saga (sao) | sinxron | atomar | orkestratsiya | juda yuqori | past | past | juda past |
| Phone Tag Saga (sac) | sinxron | atomar | xoreografiya | yuqori | yuqori | past | past |
| Fairy Tale Saga (seo) | sinxron | yakuniy | orkestratsiya | yuqori | juda past | o'rta | yuqori |
| Time Travel Saga (sec) | sinxron | yakuniy | xoreografiya | o'rta | past | o'rta | yuqori |
| Fantasy Fiction Saga (aao) | asinxron | atomar | orkestratsiya | yuqori | yuqori | past | past |
| Horror Story (aac) | asinxron | atomar | xoreografiya | o'rta | juda yuqori | past | o'rta |
| Parallel Saga (aeo) | asinxron | yakuniy | orkestratsiya | past | past | yuqori | yuqori |
| Anthology Saga (aec) | asinxron | yakuniy | xoreografiya | juda past | yuqori | yuqori | juda yuqori |

Har birining bir qatorli mazmuni:

- **Epic Saga (sao)** - "an'anaviy" saga: mediator barcha qadamlarni kuzatadi va xatoda kompensatsion yangilanish yuboradi. Monolit xulqini takrorlagani uchun eng tanish, ammo ro'yxatdagi eng ko'p bog'langan variant; mediator timing bottleneck yaratadi.
- **Phone Tag Saga (sac)** - mediator yo'q, lekin atomarlik talab qilinadi: birinchi chaqirilgan servis koordinatsiya nuqtasiga (**front controller**) aylanadi va har bir servis kompensatsiyani zanjir bo'ylab orqaga qaytarish mantiqini o'zida yuritadi. Happy path tezroq, xato yo'li ancha sekin.
- **Fairy Tale Saga (seo)** - mediator bor, atomarlik yo'q: har servis o'z tranzaksiyasiga egalik qiladi, mediator faqat so'rov, javob va xatoni boshqaradi. Mikroservislarda eng keng tarqalgan va eng muvozanatli variant.
- **Time Travel Saga (sec)** - mediator ham, umumiy tranzaksiya ham yo'q: har servis so'rovni qabul qiladi, bajaradi va keyingisiga uzatadi. Chain of Responsibility yoki Pipes and Filters shakli; "fire and forget" oqimlar (ma'lumot yuklash, bulk amallar) uchun juda yaxshi, murakkab oqim uchun yaroqsiz.
- **Fantasy Fiction Saga (aao)** - asinxron va atomar, mediator bilan: mediator barcha pending tranzaksiyalarning holatini ushlab turishi kerak, bir oqim ikkinchisining tugamagan natijasiga tayansa murakkablik portlaydi. Deyarli har doim `Parallel Saga (aeo)` yaxshiroq tanlov.
- **Horror Story (aac)** - **eng yomon birikma**: eng qattiq talab (atomarlik) eng bo'sh ikki mexanizm (asinxronlik va xoreografiya) bilan birga. Mediator yo'q, shuning uchun har servis bir necha pending tranzaksiyaning undo ma'lumotini o'zi saqlaydi va xato bo'lganda kutilmagan tartibda bekor qiladi. Murakkablik reytingi "juda yuqori" - ro'yxatda eng yuqorisi.
- **Parallel Saga (aeo)** - `Epic Saga (sao)` ning ikki cheklovi bo'shatilgani: mediator saqlanadi, aloqa asinxron, izchillik yakuniy. Murakkab oqimga mediator, yuqori masshtabga asinxronlik ishlaydi; trade-off lari eng jozibali to'plamlardan biri.
- **Anthology Saga (aec)** - `Epic Saga (sao)` ning to'liq teskarisi va **eng kam bog'langan** variant: navbatlar orqali asinxron xabar, mediator yo'q, izchillik yakuniy. Masshtab va javob berish eng yuqori, lekin murakkablik ham yuqori - faqat oddiy, asosan chiziqli oqimlar uchun.

**Qaror qoidasi.** Birinchi o'lchamni izchillik hal qiladi: atomarlik majburiy bo'lsa to'rtta variant qoladi va to'rttasi ham qimmat, `Horror Story (aac)` esa butunlay chiqarib tashlanadi. Yakuniy izchillikka ruxsat bo'lsa, ikkinchi savol oqim murakkabligi: murakkab oqim va ko'p xato shartlari bo'lsa orkestratsiya (`Fairy Tale Saga (seo)` yoki `Parallel Saga (aeo)`), oddiy va chiziqli oqimda xoreografiya (`Time Travel Saga (sec)` yoki `Anthology Saga (aec)`). Uchinchi savol - throughput: yuqori bo'lsa asinxron variantni ol. Kitobning qoidasi qisqa: implementatsiya semantik bog'lanishni yaxshilay olmaydi, faqat yomonlashtiradi - oqim mohiyatan murakkab bo'lsa mediatorni olib tashlash murakkablikni yo'qotmaydi, uni servislarga tarqatadi.

**State Owner and Coupling.** Oqim holatining egasi ham shu qarorning bir qismi: orkestratsiyada u mediatorda, xoreografiyada esa front controller da. Mediatorni olib tashlash holat egasini yo'qotadi va servislar orasidagi aloqa hajmini oshiradi. Bu almashtirish ba'zan to'g'ri: masshtab kerak va xato shartlari kam uchraydigan oqimda xoreografiyaning masshtabi xato boshqaruvi murakkabligiga arziydi, lekin oqim murakkabligi oshgani sayin orkestratorning foydasi proporsional ortadi. Uchinchi yechim ham bor - holatni kontrakt ichida uzatish, ya'ni stamp coupling (14.43).

**Spring'da qayerda uchraydi:** Uch o'lcham Spring da uch texnologiya tanloviga aylanadi. Aloqa: sinxron tomoni `RestClient` yoki `@HttpExchange` + `HttpServiceProxyFactory`; asinxron tomoni Spring for Apache Kafka (`KafkaTemplate`, `@KafkaListener`), Spring AMQP yoki Spring Cloud Stream `Supplier`/`Consumer` bean'lari. Izchillik: atomar tomoni ilova darajasidagi kompensatsiya, yakuniy tomoni Transactional Outbox (Spring Modulith `@Externalized`, `spring-modulith-events-kafka`) va `@TransactionalEventListener(phase = AFTER_COMMIT)`. Koordinatsiya: orkestrator - `@Service` ichidagi holat mashinasi yoki Spring Statemachine; xoreografiya - faqat listener'lar va kompensatsion event'lar.

**Ehtiyot bo'ling:** Ikki eng ko'p uchraydigan xato ro'yxatdan ko'rinadi. Birinchisi - `Epic Saga (sao)` ni "standart" deb olish: u tanish bo'lgani uchun tanlanadi, lekin bog'lanish va masshtab bo'yicha eng yomon qatorni egallaydi. Ikkinchisi - sekin ishlayotgan `Epic Saga (sao)` ni tezlashtirish uchun aloqani asinxron qilish va mediatorni olib tashlash, atomarlikni esa saqlab qolish: natija aynan `Horror Story (aac)`. Asinxronlik alohida olinganda tezlikni oshiradi, lekin izchillik va koordinatsiya o'lchamlari bilan chalkashganda oshirmaydi; shuning uchun uch o'lchamdan birini o'zgartirishdan oldin qolgan ikkisi qanday javob berishini yozib ko'rish kerak.

```text
Saga variantini tanlash tartibi (har qatorga loyihadan javob yoziladi):

  1. Atomarlik majburiymi?  ha -> sao yoki sac; aac ni YOZMA
                            yo'q -> 2 ga o't
  2. Oqim murakkabligi?     4+ qadam yoki ko'p xato sharti -> seo / aeo
                            2-3 qadam, chiziqli            -> sec / aec
  3. Throughput chegarami? ha -> asinxron (aeo / aec)
                            yo'q -> sinxron (seo / sec), debug osonroq
  4. Xoreografiyada holat egasi kerakmi?
                            ha -> front controller yoki stamp coupling (14.43)
```

## 14.43 Oqim holatini kontraktda uzatish: stamp coupling (Stamp Coupling for Workflow Management)

**Tavsif:** Stamp coupling - servislar orasida katta ma'lumot tuzilmasi uzatilib, har servis uning faqat kichik qismi bilan ishlashi; kontrakt dizayni nuqtasidan uning uch yuzi (soha standarti hujjati, ortiqcha e'lon qilingan kontraktning mo'rtligi, bandwidth narxi) [7.37 Shtamp bog'liqligi](07-api-dizayn-patternlari.md#737-shtamp-bogliqligi-stamp-coupling) bo'limida yozilgan. Bu bo'lim bitta yuzini oladi: uni **ataylab**, taqsimlangan oqimni mediatorsiz boshqarish uchun ishlatish. Savol shunday tug'iladi: murakkab oqimga odatda mediator qo'yiladi, lekin masshtab kabi boshqa kuchlar arxitektorni bir vaqtda xoreografiyali va murakkab yechimga haydasa nima qilish kerak? Javob - oqim holatini kontrakt ichida olib yurish: kontraktga domen ma'lumoti bilan birga oqim holati (qaysi qadam bajarildi, tranzaksiya holati, xato xabarlari) qo'shiladi. Har servis kontraktni qabul qiladi, o'z qismini va oqim holatini yangilaydi va keyingisiga uzatadi; oxirgi qabul qiluvchi butun natijani - muvaffaqiyat yoki xato, holat va xato matni - bitta kontraktdan o'qiydi. Atomar izchillik kerak bo'lsa, servislar kontraktni avval o'tgan servislarga qayta e'lon qiladi.

Bu yechim 14.42 dagi `Phone Tag Saga (sac)` va `Anthology Saga (aec)` variantlarida front controller yoki holat egasi o'rnini bosadi va 14.8 dagi "oqim hech bir kodda ko'rinmaydi" muammosini qisman yumshatadi: holat hech bo'lmasa xabarning o'zida turadi.

| Afzalligi | Narxi |
|---|---|
| Xoreografiyali yechim ichida murakkab oqim mumkin bo'ladi | Hamkorlar orasida nominal darajadan yuqori, ba'zan sun'iy bog'lanish |
| Domen servisi holat egasiga qo'shimcha so'rov yubormaydi | Kontrakt oqim holatini sig'dirish uchun kattalashadi |
| Mediatorga ehtiyoj qolmaydi | Yuqori masshtabda bandwidth muammosi chiqadi |
| Oqim davomida har servis qo'shimcha kontekst oladi | "Oqim hozir qayerda" degan so'rovni bitta joydan bermaydi |

**Spring'da qayerda uchraydi:** Oqim holati Kafka xabari payload'idagi alohida nomlangan bo'lim sifatida yoziladi va domen maydonlari bilan aralashtirilmaydi; `@KafkaListener` o'z kalitini yangilab, `KafkaTemplate` bilan keyingi topic'ga uzatadi. Spring Cloud Stream da bu `Function<Message<ShipmentContract>, Message<ShipmentContract>>` bean'i shaklini oladi, holatning kichik qismi esa `Message` header'lariga (`MessageBuilder.setHeader(...)`) chiqarilishi mumkin. Kontraktning versiyalanishi muhim bo'ladi, chunki oqim holati sxemasi domen sxemasidan tezroq o'zgaradi: Avro yoki Protobuf sxema reyestri, yoki eng kamida `schemaVersion` maydoni kerak. Kontrakt hajmini kuzatish uchun payload baytini Micrometer `DistributionSummary` ga yozib, RPS bilan ko'paytmasini dashboard'da ushlab turish kifoya.

```java
// Oqim holati domen maydonlaridan ajratilgan: `workflow` bo'limi ATAYLAB bor
public record ShipmentContract(
        String orderId,
        List<Item> items,                       // domen ma'lumoti
        int schemaVersion,
        Map<String, StepStatus> workflow        // oqim holati: kalit - qadam nomi
) {}

public record StepStatus(String state, Instant at, String error) {}

@Component
class PackagingStep {
    private final KafkaTemplate<String, ShipmentContract> kafka;
    PackagingStep(KafkaTemplate<String, ShipmentContract> kafka) { this.kafka = kafka; }

    @KafkaListener(topics = "shipment.reserved")
    void on(ShipmentContract in) {
        Map<String, StepStatus> wf = new LinkedHashMap<>(in.workflow());
        try {
            packer.pack(in.orderId(), in.items());
            wf.put("packaging", new StepStatus("DONE", Instant.now(), null));
            kafka.send("shipment.packed", in.orderId(), withWorkflow(in, wf));
        } catch (PackagingException e) {
            wf.put("packaging", new StepStatus("FAILED", Instant.now(), e.getMessage()));
            kafka.send("shipment.failed", in.orderId(), withWorkflow(in, wf));
        }
    }

    private ShipmentContract withWorkflow(ShipmentContract c, Map<String, StepStatus> wf) {
        return new ShipmentContract(c.orderId(), c.items(), c.schemaVersion(), Map.copyOf(wf));
    }
}
```

**Qo'llanish keyslari:**
- Xoreografiyali yuk tashish oqimida har servis `workflow` bo'limining o'z kalitini yangilab, oxirgi iste'molchi butun natijani bitta kontraktdan o'qishi.
- `Anthology Saga (aec)` da mediator kiritmasdan oqimni bir pog'ona murakkablashtirish.
- Xato matnini oqim davomida olib yurib, oxirida bitta joyda hisobot qilish.
- Bir nechta boyituvchi servis ketma-ket bitta hodisa payload'ini to'ldirishi.

**Ehtiyot bo'ling:** Bu qisman yechim: kitob uni holat egasining o'rnini to'liq bosmaydi deb aniq aytadi - foydalanuvchiga "oqim hozir qayerda" degan so'rovni beradigan bitta joy baribir yo'q, shuning uchun monitoring va qo'lda tuzatish uchun trace yoki alohida read model kerak bo'ladi. Ikkinchi chegara - masshtab: kontrakt hajmi va RPS ko'paytmasini oldindan hisoblab ko'rmasa, yechim bandwidth cheklovida sinadi. Va eng muhimi: semantik bog'lanish qayergadir joylashishi shart, stamp coupling uni kontraktga ko'chiradi, yo'q qilmaydi - shuning uchun oqim murakkabligi oshib ketsa to'g'ri javob mediatorga qaytish bo'ladi (14.42).

## 14.44 Granularlik chegaralarining o'lchanadigan qoidalari

**Tavsif:** Oltita disintegrator va to'rtta integrator sababining ro'yxati [mikroservislar](12-arxitektura-uslublari.md#1212-mikroservislar-microservices) bo'limida berilgan, bu yerda esa shu sabablarni qarorga aylantiradigan o'lchanadigan chegaralar yozilgan. Ford va boshqalar har bir sabab uchun "qachon yetarli" savoliga raqam yoki aniq sinov beradi, chunki jamoalar aynan shu nuqtada tortishadi.

- **Kohesiya yolg'iz o'zi bo'lish uchun sabab emas.** SMS, email va qog'oz xat yuboradigan Notification servisi uchta bir maqsadli servisga bo'linishi mumkin ko'rinadi, lekin uning kohesiyasi allaqachon kuchli: uchtasi ham bitta ishni, mijozni xabardor qilishni bajaradi. "Bir maqsadli" iborasi sub'ektiv, kohesiyani o'lchaydigan LCOM kabi metrikalar esa servis darajasida ishonchsiz, shuning uchun bo'lishni oqlash uchun ikkinchi disintegrator (volatility, scale, fault tolerance, security) ko'rsatilishi kerak. Teskari misol: profil, sozlamalar va sayt sharhlarini birga boshqaradigan Customer servisining kohesiyasi zaif, chunki uchtasi "mijoz" degan ancha keng doiraga tegishli, u esa bo'linishga yaxshi nomzod.
- **Qoldiq nom sinovi.** Bo'lishdan oldin qoldiq funksiyaga yaxshi nom topilishini tekshiring. `Notification -> Email + Other Notification`, `Email + Non-Email` va `Email + SMS-Letter` variantlarining uchtasida ham qoldiq nomi yomon, ya'ni qoldiqning kohesiyasi zaif; yagona mazmunli natija `Email + SMS + Letter`. Sinovning ikkinchi savoli: yangi kanal (ijtimoiy tarmoq) qo'shilsa u qaysi servisga tushadi.
- **Extensibility faqat rejalashtirilgan kengayishda.** To'lov servisi uchun yangi to'lov turlari (bonus ball, do'kon krediti, ApplePay) kelishi deyarli aniq, shuning uchun to'lov turi bo'yicha bo'lish oqlanadi: yangi tur qo'shish faqat bitta servisni ishlab chiqish, test qilish va deploy qilish bo'lib qoladi. Bildirishnoma kanallari esa SMS, email va xatdan tashqariga kengayishi shubhali. Qoida: kengayish oldindan ma'lum yoki domen uchun odatiy bo'lmasa, naqsh tasdiqlanmaguncha bu drayverni ishlatmang.
- **Sinxron bog'liq bo'laklarni ajratish fault tolerance BERMAYDI.** A servis B va C ni, B servis C ni, E servis C ni chaqiradigan tarmoqda C yiqilsa qolgan hammasi ishlamaydi: tranzitiv bog'liqlik butun foydadan voz kechtiradi. Fault tolerance disintegrator ro'yxatida bor, lekin ajratilgan bo'laklar bir-biri bilan sinxron gaplashishi kerak bo'lsa, biznes so'rovi darajasida hech narsa yaxshilanmaydi va ularni birga qoldirish to'g'ri bo'ladi.
- **Besh hop, har biri 300 ms, jami 1500 ms.** Bitta mijoz so'roviga javob berish uchun beshta servisni ketma-ket chaqirish kerak bo'lsa va har bir chaqiruvda tarmoq va xavfsizlik kechikishi 300 ms bo'lsa, so'rov faqat kechikish hisobiga 1500 ms qo'shib oladi. Nisbat qoidasi: so'rovlarning 30 foizi servislararo oqimni talab qilsa va 70 foizi atomar (bitta servis bilan tugaydigan) bo'lsa, servislarni alohida qoldirish maqbul; nisbat teskari bo'lsa birlashtirishni ko'rib chiqing. Ikkinchi mezon kritiklik: o'ta tez javob talab qiladigan so'rov o'sha 30 foiz ichida bo'lsa, qolgan 70 foiz atomar bo'lishiga qaramay birlashtirish to'g'ri. Foydalanuvchi natijani kutmayotgan backend ishida esa erkinlik ko'proq.
- **Ulashilgan domen kodi ~40 foizdan oshsa birlashtiring.** Mijoz bilan bog'liq funksiyalar (profil, sozlama, sharh) uchun umumiy kod jamlangan kodbazaning 40 foizidan ko'pini egallasa, ajratish kodning deyarli yarmini faqat shu uchta servis ishlatadigan umumiy kutubxonaga chiqaradi: bu holda ularni umumiy kod bilan birga bitta servisda qoldirish ma'qul. Yana ikki shart kuchaytiradi: umumiy kod tez-tez o'zgarsa (har o'zgarish muvofiqlashtirilgan reliz talab qiladi) va nuqsonni versiyalab bo'lmasa (biznes qoidasi hammaga bir vaqtda qo'llanishi shart). Infratuzilma kodi (logging, audit, autentifikatsiya, avtorizatsiya, monitoring) bu hisobga kirmaydi: u birlashtirish sababi emas.
- **Ikki servis bir-birining jadvaliga muhtoj bo'lsa birlashtiring.** Funksiya-jadval xaritasini tuzing: qalin chiziq yozuv, ya'ni egalik; punktir chiziq faqat o'qish. Agar bo'lishdan keyin B servisining har bir operatsiyasi C egalik qiladigan jadvalni, C ning har bir operatsiyasi esa B egalik qiladigan jadvalni talab qilsa, bounded context ularga to'g'ridan-to'g'ri so'rov berishga ruxsat bermaydi (B ustunni o'chirsa C buziladi), demak ikkisi orasida doimiy ikki tomonlama chaqiruv paydo bo'ladi. Bu integrator eng kam trade-off beradi: ularni birlashtirish to'g'ri javob.

**Spring'da qayerda uchraydi:** 30/70 nisbati taxmindan emas, o'lchovdan olinadi: Micrometer Tracing va Zipkin/Tempo service graph'i qaysi so'rov bir servis bilan tugaganini va qaysi biri zanjirga kirganini ko'rsatadi, `http.server.requests` timer'i esa o'sha zanjirning kechikish ulushini beradi. Ulashilgan domen kodi ulushini `jdeps`, ArchUnit yoki jQAssistant bilan modul bo'yicha hisoblash mumkin; umumiy kod tezligi uchun git tarixidagi o'zgarish chastotasi ishlatiladi. Funksiya-jadval xaritasini Hibernate metamodelidan yoki Flyway migratsiyalaridan chiqarib, Spring Modulith `ApplicationModules.of(App.class).verify()` bilan chegara buzilishini CI'da to'xtatish mumkin.

**Ehtiyot bo'ling:** Bu chegaralar qattiq qoida emas, trade-off tarozisi: faqat disintegrator ro'yxatiga qarab, integrator sabablarini hisobga olmaslik kitobda eng keng tarqalgan xato deb ko'rsatilgan. Raqamlarni kontekstsiz ko'chirmang: 300 ms Ford va boshqalarning misolidagi qiymat, sizdagi tarmoq va xavfsizlik kechikishi o'lchanishi kerak.

```text
Granularlik qarori uchun hisob varaqasi:

  hop soni x (tarmoq + xavfsizlik kechikishi) = qo'shilgan kechikish
     misolda: 5 x 300 ms = 1500 ms

  oqimli 30% / atomar 70%                    -> ajratib qoldirish mumkin
  nisbat teskari (oqimli 70% / atomar 30%)   -> birlashtirish
  o'sha 30% ichida kritik tez so'rov bor     -> birlashtirish
  ulashilgan DOMEN kodi ulushi 40% dan oshsa -> birlashtirish
  umumiy kod tez o'zgaradi yoki nuqsoni versiyalanmaydi -> birlashtirish
  ikki servis bir-birining jadvaliga muhtoj  -> birlashtirish

  qoldiqqa yaxshi nom yo'q                   -> bo'lmaslik
  ikkinchi disintegrator ko'rsatilmagan      -> bo'lmaslik
  kengayish rejalashtirilmagan               -> kutish
```

## 14.45 Saga amaliyoti: qadam tartibi va orkestrator egaligi

**Tavsif:** Saga ning ikki topologiyasi [14.8](#148-saga-xoreografiya-saga-choreography) va [14.9](#149-saga-orkestratsiya-saga-orchestration) da, sakkiz varianti esa [14.42](#1442-saga-ning-sakkiz-varianti-uch-olchamli-tanlov-transactional-saga-patterns) da berilgan. Bu bo'lim ularni amalda yozishda qabul qilinadigan qarorlarni to'playdi.

- **Qadamlarni qayta tartiblab rollback ni kamaytirish.** Kompensatsiyani yozishdan oldin qadamlar tartibini ko'rib chiqing. Buyurtma oqimida bonus ballni buyurtma yaratilganda emas, jo'natilganda berish qadamni oxirga suradi va paketlash muvaffaqiyatsiz bo'lsa uni orqaga qaytarish kerak bo'lmaydi. Ikki yo'nalishli qoida: yiqilish ehtimoli yuqori qadamni oldinga tortib oqimni erta to'xtatish (keyingi kompensatsiyalar umuman ishga tushmaydi), kompensatsiyasi qiyin qadamni esa orqaga surish. Kompensatsiya yozmaslik - kompensatsiyani to'g'ri yozishdan arzon.
- **Orkestratsiyani BPM vositasida emas, kodda yozing.** BPM vositalarining asosiy da'vosi - dasturchi bo'lmagan odam biznes oqimini o'zi chizadi - amalda deyarli bajarilmaydi: asbobni oxirida dasturchilar ishlatadi, oqim GUI'da o'zgaradi, versiya nazoratiga tushmaydi yoki qiyin tushadi va test qilish hisobga olinmagan. Vizual ko'rinish kerak bo'lsa uni koddan hosil qilish, kod qanday ishlashini vizual chizmadan chiqarishdan ancha oson. Dasturchilarga qaratilgan zamonaviy vositalar (Camunda, Zeebe, Temporal) bu tanqidning bir qismini yopadi, lekin tanlov hamon "oqim kodda yoziladi" tomonida.
- **Har oqimga alohida orkestrator, global ESB emas.** Mantiq markazlashishi mumkin bo'lgan joyda markazlashadi, shuning uchun buyurtma berish, qaytarish va tovar qabuli uchun uchta alohida orkestrator servis bo'ladi: Order Processor, Returns, Goods Receiving. Umumiy Warehouse servisi uchtasiga ham xizmat qiladi va shu sababli o'z mantiqini o'zida saqlab qoladi. Butun tashkilot uchun bitta global orkestrator (enterprise service bus) esa kerakli bo'shashishni yo'q qiladigan bog'lanish nuqtasi. Orkestratorning o'zida boshqaradigan oqimdan tashqari domen xatti-harakati bo'lmasligi kerak.
- **Bitta jamoa ichida orkestratsiya, jamoalar o'rtasida xoreografiya.** Butun saga bitta jamoa egaligida bo'lsa orkestratsiyaning qattiqroq bog'lanishi jamoa chegarasi ichida boshqariladi va qulay. Bir nechta jamoa ishtirok etsa xoreografiya afzal: mas'uliyat jamoalarga taqsimlanadi va bo'shroq bog'langan arxitektura ularni mustaqil ishlashga qo'yadi. Ikki uslubni aralashtirish ham mumkin: xoreografiyali umumiy oqim ichida bitta servisning chegarasida (paketlash va jo'natish) orkestratsiya qilingan ichki oqim bo'lishi normal, sharti - saga da nima bo'lganini tushunadigan yo'l qolishi.
- **Saga reyestrini kodda belgilang.** Saga tayyor kutubxona emas, loyihalanadi; shuning uchun qaysi servis qaysi sagada ishtirok etishini kodda e'lon qiling. Ford va boshqalarning usuli: saga nomlarini bitta `enum` ga yig'ib (`NEW_TICKET`, `CANCEL_TICKET`, ...), har servisning kirish sinfiga `@Saga(Transaction.NEW_TICKET)` annotatsiyasini qo'yish va kodbazani aylanib o'tadigan oddiy CLI bilan "`NEW_TICKET` sagasida qaysi servislar bor" savoliga javob olish. Bu test skopini va o'zgarish ta'sirini aniqlaydi.

**Spring'da qayerda uchraydi:** Orkestrator har oqim uchun alohida Spring Boot komponenti bo'ladi va holatini `SagaInstance` entity'sida `@Version` bilan saqlaydi; vizual ko'rinishni koddan chiqarish uchun state machine ta'rifini Spring Statemachine `StateMachineFactory` dan yoki Spring Modulith `Documenter` dan generatsiya qilish mumkin. Xoreografiyali oqimda holatni kuzatish [14.8](#148-saga-xoreografiya-saga-choreography) da. Saga reyestri uchun o'z `@Saga` annotatsiyangiz va `@Retention(RUNTIME)` yetarli, skaner sifatida Spring'ning `ClassPathScanningCandidateComponentProvider` sinfi ishlatiladi.

**Ehtiyot bo'ling:** Qadam tartibini o'zgartirish biznes semantikasini ham o'zgartiradi: bonus ballni jo'natilgandan keyin berish mijozga boshqacha ko'rinadi, shuning uchun tartib qarori texnik emas, mahsulot qarori. Bir nechta oqimga bitta orkestrator berish BPM vositasini olib tashlagandan keyin ham global ESB ni qaytarib keltiradi.

## 14.46 Saga nimani hal qiladi va nima qilmaydi

**Tavsif:** Saga ning chegarasi odatda loyihaning o'rtasida, birinchi texnik nosozlikda topiladi. To'rtta qoida bu chegarani oldindan aniq qilib qo'yadi.

- **Saga biznes xatosini hal qiladi, texnik xatoni emas.** Mijozning mablag'i yetmasligi - biznes xatosi va saga aynan shuni boshqarishi kerak; to'lov gateway'ining timeout'i yoki `500 Internal Server Error` esa texnik nosozlik va u alohida hal qilinadi. Saga asosiy qoida sifatida ishtirokchilarni ishonchli deb qabul qiladi: u ishonchli komponentlarning ishini muvofiqlashtiradi, ishonchsizligini tuzatmaydi. Demak har bir ishtirokchi chaqirig'i atrofida timeout, retry va circuit breaker bo'lishi shart, aks holda saga texnik xatoni biznes kompensatsiyasiga aylantirib yuboradi.
- **Undo odatda do dan qimmat.** Kompensatsiyani ikki yo'l bilan yozish mumkin: har so'rovni pending holatda ushlab turib, mediator umumiy muvaffaqiyatni bildirgach tasdiqlash (koordinatsiya trafigi ko'p, asinxron so'rovlar va pending holatga bog'langan yangi so'rovlar bilan murakkablashadi), yoki har operatsiya uchun `do` va `undo` juftligini qurish. Ikkinchi yo'lda koordinatsiya kamayadi, lekin `undo` amallari `do` dan sezilarli murakkabroq chiqadi va dizayn, implementatsiya hamda debug mehnatini ikki baravardan ko'proq oshiradi. Shuning uchun sagani kamdan-kam ishlatish tavsiya qilinadi: servislar orasida bir nechta tranzaksiya kerak bo'lishi normal, ular arxitekturaning asosiy belgisiga aylansa chegaralar xato qo'yilgan.
- **Muhim bo'lmagan qadamda kompensatsiya o'rniga holat belgisi.** So'rovnoma yuborish kabi ikkinchi darajali qadam yiqilsa, butun sagani orqaga qaytarish o'rniga saga holatini `NO_SURVEY` ga o'tkazib, foydalanuvchiga muvaffaqiyat qaytarish to'g'ri bo'ladi; orkestrator fonda qayta urinib ko'radi, hal qila olmasa ishni administratorga yuboradi. Natijada foydalanuvchi biznes jarayonining qolgan qismi bilan keraksiz bog'lanmaydi va boshqa ishini davom etadi. Narxi oshkor: ma'lumot manbalari tuzatilguncha bir-biri bilan mos emas.
- **Holatli saga ni buyruqlar bilan birga bajarmang.** Kompensatsiya uchun qanday amallar bajarilganini bilish kerak bo'lsa, saga holat saqlaydi va uni hodisa manbali agregat qilib yozish mumkin: qabul qilingan hodisalar va chiqarilgan buyruqlarning to'liq tarixi saqlanadi. Lekin buyruqni bajarish mantiqi saganing ichidan chiqarilishi kerak: saga `CommandIssued` hodisasini yozadi, uni esa outbox relay asinxron bajaradi. Holat o'tishini buyruq bajarilishidan ajratish buyruqning jarayon istalgan nuqtada qulasa ham ishonchli bajarilishini kafolatlaydi.

**Spring'da qayerda uchraydi:** Ishtirokchi chaqiruvlarini Resilience4j (`@CircuitBreaker`, `@Retry`, `@TimeLimiter`) himoyalaydi va texnik nosozlik kompensatsiyaga aylanmasligi uchun saga faqat biznes javobiga (masalan `InsufficientFunds`) reaksiya qiladi. Holat belgisi oddiy `enum` maydon (`NO_SURVEY`) bo'lib, fon urinishlari `@Scheduled` + ShedLock yoki Quartz bilan yuritiladi. `CommandIssued` hodisasini outbox orqali chiqarish uchun Spring Modulith `@Externalized` va `spring-modulith-events-jpa`/`-kafka` (`EventPublicationRegistry`) yoki `@TransactionalEventListener(phase = AFTER_COMMIT)` ishlatiladi; outbox patternining o'zi [14.12](#1412-tranzaksion-outbox-transactional-outbox-microservice-view) da.

**Ehtiyot bo'ling:** Texnik nosozlikni biznes kompensatsiyasi bilan hal qilish eng qimmat xato: to'lov gateway'i timeout bergani to'lov o'tmaganini bildirmaydi, shuning uchun zaxirani bo'shatish mijozdan pul olingan holatda ham sodir bo'lishi mumkin. Holat belgisi bilan tugash esa faqat ikkinchi darajali qadam uchun: asosiy qadamni `NO_*` holatiga qoldirish yakuniy izchillikni nomuvofiqlikka aylantiradi.

## 14.47 Bir nechta jamoa bitta servisga muhtoj bo'lganda

**Tavsif:** [14.5](#145-har-bir-jamoaga-bitta-servis-service-per-team) bitta servisga bitta jamoa egalik qilishini talab qiladi. Amalda bu qoida buziladi va buzilish aniq belgilar beradi; bu bo'lim belgilarni va chiqish yo'llarini beradi.

- **Jamoaviy egalikning o'lcham chegarasi.** Jamoaviy egalik (hamma hamma joyni o'zgartiradi) bir joyda o'tirgan, taxminan 20 gacha dasturchidan iborat jamoada ishlaydi, chunki "yaxshi o'zgarish qanday bo'ladi" degan umumiy tushuncha shu o'lchamda saqlanadi. Tez o'sishda yoki 100 dan ortiq dasturchida kuchli egalik (har jamoa o'z servisini boshqaradi) amalda yagona ishlaydigan model. Buzilish ko'rinishi aniq: 30-40 dan 100 dan ortiq dasturchiga o'sgan va hech qanday egalik belgilanmagan kompaniyada arxitektura "kolander" (elak) ga aylangan - kim xohlasa yangi teshik ochadi, ya'ni ma'lumotni ochib qo'yadi yoki to'g'ridan-to'g'ri chaqiruv qo'shadi; natija taqsimlangan monolit va uni yechish monolitni yechishdan ancha qimmat.
- **Ko'p kiruvchi pull request ulashilgan servis belgisi.** Servis egasi jamoaga boshqa jamoalardan pull request oqimi kelsa, bu PR larni tez ishlash bilan hal bo'lmaydi: bu servis amalda bir nechta jamoa tomonidan bo'lishib ishlatilayotganining belgisi. Birinchi savol - PR lar jiddiy qabul qilinayaptimi, ikkinchisi - egalik o'zgarishi kerak emasmi. Manba bitta jamoa bo'lsa javob oson: servis eng ko'p o'zgartirgan jamoaga o'tadi.
- **Umumiy skelet va har variantga alohida instance.** Manba bir nechta jamoa bo'lsa (har mamlakat jamoasi markaziy servisga o'z mantig'ini kiritishi kerak), markaziy jamoa servisni faqat umumiy xulqdan iborat framework ko'rinishida beradi va har jamoa o'z instansini o'z plaginlari bilan ishga tushiradi. Umumiy funksiya takrorlanmaydi, lekin narxi bor: umumiy kodni hamma variantda bir vaqtda yangilab bo'lmaydi (bu keng qamrovli lockstep reliz talab qiladi), yangi versiyani har jamoa o'zi olib deploy qiladi. Ichki framework shishib ketishi yoki jamoalarni cheklab qo'yishi mumkin va bu birinchi kuni ko'rinmaydi, shuning uchun boshqa variantlar tugamaguncha bu yo'lga shoshilmang.
- **Kutubxona orqali tashqi hissa.** Variant: har jamoa o'z mantiqini kutubxona qilib beradi va markaziy servis ularni bitta build'ga paketlaydi. Qo'shimcha servis ishlatilmaydi, lekin jamoa o'z kodi qachon production'ga chiqishini hal qilmaydi (deploy ni markaziy jamoa rejalashtiradi) va kutubxonadagi nuqson production muammosini markaziy jamoaga qaytaradi, ya'ni nosozlikni tekshirish murakkablashadi. Bu yo'l servisni bir nechta variantda ishga tushirishni oqlab bo'lmaganda va jamoaviy egalikdan chiqish kerak bo'lganda ko'rib chiqiladi.

**Spring'da qayerda uchraydi:** Umumiy skelet amalda [service template](#1431-service-shabloni-service-template) va [chassis](#1429-microservice-shassi-microservice-chassis) bilan bir xil mexanizm: umumiy xulq `*-spring-boot-starter` va `@AutoConfiguration` sifatida chiqariladi, mamlakatga xos mantiq esa `@ConditionalOnMissingBean` yoki `ObjectProvider` bilan ulanadigan plugin nuqtasi bo'ladi. Kutubxona orqali hissa qo'shish holatida har kutubxona o'z modulida, markaziy servis esa ularni `spring.factories` o'rnidagi `AutoConfiguration.imports` bilan yig'adi; nuqsonni manbaga qaytarish uchun har plugin o'z `@Timed`/`@Counted` metrikasi va alohida logger nomi bilan ajratiladi. Egalik ma'lumoti `/actuator/info` va `build-info` da ko'rsatiladi.

**Ehtiyot bo'ling:** Uchala yo'l ham egalikni to'g'rilashning o'rnini bosmaydi: Newman o'zi avval servis mas'uliyatini bo'lish yoki egalikni ko'chirish yo'lini izlashni va faqat ular tugagandan keyin framework yoki kutubxona modeliga o'tishni aytadi. Plugin modeliga o'tish qarori qaytarilishi qiyin, chunki ichki framework atrofida bir yilda yangi bog'liqliklar o'sadi.

## 14.48 Amalda qo'llash

- [ ] Servislar xaritasini chizib, har bir sinxron chaqiruv zanjirini va uning umumiy timeout budjetini yozib qo'ying.
- [ ] Ikki yoki undan ko'p servis bitta bazaga ulanadigan joylarni toping - bu taqsimlangan monolit belgisi.
- [ ] Har bir servis uchun o'z ma'lumotlari, o'z relizi va o'z jamoasi borligini tekshiring; uchtasi yo'q bo'lsa, u servis emas.
- [ ] Service discovery va konfiguratsiya manbasini hujjatlashtiring; qattiq yozilgan host nomlarini qidirib ro'yxat qiling.
- [ ] API gateway da autentifikatsiya, rate limit va so'rov hajmi chegarasi borligini tasdiqlang.
- [ ] Har bir servisning readiness va liveness probe'i alohida va to'g'ri ma'no berayotganini tekshiring.
- [ ] Servislar o'rtasida umumiy kutubxona (`shared`, `common`) borligini tekshirib, undagi har bir sinfni egasi bor servisga ko'chirish rejasini yozing.
- [ ] Strangler fig bilan ajratilayotgan funksiyalar uchun o'tish mezoni va orqaga qaytish yo'lini yozib qo'ying.
- [ ] Har bir saga uchun uchta anomaliyadan qaysi biri mumkinligini yozib chiqing va har biriga qarshi chora tanlang (semantic lock, reread value, commutative update).
- [ ] Har bir saga uchun uchta o'lchamni (aloqa, izchillik, koordinatsiya) yozib chiqib, qaysi nomlangan variantga tushganini aniqlang; `Horror Story (aac)` ga tushsa dizaynni qaytadan ko'rib chiqing.
- [ ] Xoreografiyali oqimlarda oqim holatining egasi kim ekanini yozib qo'ying: front controller, kontrakt ichidagi holat, yoki hech kim.
- [ ] Servislararo kontraktlarni ko'rib chiqib, iste'molchi ishlatmaydigan maydonlar ro'yxatini chiqaring va payload hajmini RPS ga ko'paytirib bandwidth hisobini yozing.
- [ ] Saga o'zgartiradigan entity larda holat maydoni va `@Version` borligini tekshirib, shartli `UPDATE` ning `rowsAffected` natijasi nazorat qilinishiga ishonch hosil qiling.

## Manbalar

- Chris Richardson, *Microservices Patterns*, 2-bob - biznes imkoniyati va subdomen bo'yicha dekompozitsiya, Service per Team
- Chris Richardson, *Microservices Patterns*, 4-bob - saga bilan tranzaksiyalarni boshqarish (koreografiya va orkestratsiya)
- Chris Richardson, *Microservices Patterns*, 11-bob - ishlab chiqarishga tayyor servis: chassis, Externalized Configuration
- Chris Richardson, *Microservices Patterns*, 13-bob - mikroservisga refaktoring va Strangler Fig
- Robert C. Martin, *Clean Architecture*, 27-bob - servis granularligi: katta va kichik servis
- John Carnell, *Spring Microservices in Action*, 4-bob - servis topish
- Chris Richardson, *Microservices Patterns*, 4.3 - saga modelining ACD ekani, izolyatsiya yo'qligidan kelib chiqadigan uchta anomaliya (lost update, dirty read, fuzzy read) va oltita qarshi chora (semantic lock, commutative updates, pessimistic view, reread value, version file, by value)
- Chris Richardson, *Microservices Patterns*, 3-bob - xabar almashish, outbox va idempotent iste'molchi
- Chris Richardson, *Microservices Patterns*, 7-bob - API composition va CQRS bilan so'rovlarni birlashtirish
- Chris Richardson, *Microservices Patterns*, 13-bob - Strangler Fig va monolitni bosqichma-bosqich ajratish
- Chris Richardson, *Microservices Patterns: With examples in Java*, Manning, 2019, 12-bob, 386-390-betlar - tilga xos paketlash formati patterni, uning ikki foydasi (tez deploy, resurs tejamkorligi) va to'rt kamchiligi (technology stack kapsulalanmasligi, resurs chegarasi yo'qligi, izolyatsiya yo'qligi, joylashtirishni avtomatlashtirishning qiyinligi)
- John Carnell, *Spring Microservices in Action*, 2-bob (39-43-betlar) - dekompozitsiya signallari (ot, fe'l, ma'lumot yaxlitligi), data modelni mavjud monolit uchun boshlang'ich xarita qilish va granularlik belgilari (uchtadan beshtagacha jadval, test soni, mas'uliyat ko'pligi)
- John Carnell, *Spring Microservices in Action*, 3-bob (66-67-betlar) - konfiguratsiya strategiyasini erta belgilash: 12 000 sozlama faylining 20 taga konsolidatsiyasi
- John Carnell, *Spring Microservices in Action*, 4-bob (99, 110-betlar) - markaziy DNS va load balancer modelining to'rt kamchiligi, Eureka ning uch heartbeat va 30 soniyalik warm-up kechikishi
- John Carnell, *Spring Microservices in Action*, 6-bob (156, 169, 170, 174-betlar) - gateway oldiga load balancer qo'yish, gateway kodining stateless va yengil bo'lishi, pre/route/post filter turlari va filter tartibi, gateway va servis timeout larining mosligi
- Craig Walls, *Spring in Action* 6th, 1-bob va A-ilova (7, 11, 469-475-betlar) - Spring Initializr ni veb, `curl`, Boot CLI va IDE orqali chaqirish, API parametrlari va hosil bo'ladigan loyiha tuzilmasi
- Neal Ford, Mark Richards, Pramod Sadalage, Zhamak Dehghani, *Software Architecture: The Hard Parts*, 1-nashr, O'Reilly, 2021 (copyright 2022), 12-bob (323-350-betlar) - saga ning uch o'lchami (aloqa, izchillik, koordinatsiya) va sakkiz nomlangan birikmasi, har biri uchun bog'lanish, murakkablik, javob berish va masshtab reytinglari; `Epic Saga(sao)` eng ko'p bog'langan, `Horror Story(aac)` eng murakkab, `Anthology Saga(aec)` eng kam bog'langan (14.42)
- Neal Ford, Mark Richards, Pramod Sadalage, Zhamak Dehghani, *Software Architecture: The Hard Parts*, 1-nashr, O'Reilly, 2021 (copyright 2022), 11-bob (313-316-betlar) - oqim holati egasi orkestratorda yoki front controller da; mediatorni olib tashlash servislararo aloqani oshirishi, oqim murakkabligi oshgani sayin orkestratorning foydasi ortishi, xoreografiyada holatni kontrakt ichida uzatish qisman yechim bo'lishi (14.42, 14.43)
- Neal Ford, Mark Richards, Pramod Sadalage, Zhamak Dehghani, *Software Architecture: The Hard Parts*, 1-nashr, O'Reilly, 2021 (copyright 2022), 13-bob (378-379-betlar) - oqim holatini kontrakt ichida uzatib xoreografiyali yechimda murakkab oqimni boshqarish, atomarlik kerak bo'lsa kontraktni avval o'tgan servislarga qayta e'lon qilish, trade-off jadvali (sun'iy yuqori bog'lanish va yuqori masshtabda bandwidth muammosi) (14.43)
- Sam Newman, *Monolith to Microservices*, O'Reilly, 2019, 2-bob (35, 44) - mikroservisga o'tishdan oldingi uch savol va mijoz o'rnatib boshqaradigan dasturda mikroservisning yomon tanlov bo'lishi (14.1)
- Sam Newman, *Building Microservices: Designing Fine-Grained Systems*, 2-nashr, O'Reilly, 2021, 15-bob, "Strong Versus Collective Ownership" va "Conway's Law in Reverse" bo'limlari - kuchli va jamoaviy egalik farqi hamda ularning avtonomiyaga ta'siri, tizim dizayni tashkilotni shakllantirishi (dalil anekdot darajasida). Bu nashrning qo'limizdagi elektron nusxasida barqaror bet raqami yo'q, shuning uchun faqat bob va bo'lim nomi ko'rsatilgan (14.5)
- Chris Richardson, *Microservices Patterns: With examples in Java*, Manning, 2019, 2-bob, 61-62-betlar - dekompozitsiyadan keyingi qadam: tizim operatsiyalarini servislarga biriktirish (ma'lumot kerak bo'lgan yoki ma'lumotga ega servisga) va hamkorlik uchun servislararo operatsiya hamda hodisalarni aniqlash (14.2)
- Neal Ford, Mark Richards, Pramod Sadalage, Zhamak Dehghani, *Software Architecture: The Hard Parts*, 1-nashr, O'Reilly, 2021 (copyright 2022), 7-bob (189-206-betlar) - granularlik qarorining o'lchanadigan chegaralari: kuchli kohesiyali servisni funksiya bo'yicha bo'lmaslik va LCOM ning sub'ektivligi, qoldiq nom sinovi, extensibility faqat rejalashtirilgan kengayishda, tranzitiv sinxron bog'liqlik fault tolerance ni yo'q qilishi, besh hop x 300 ms = 1500 ms va 30/70 nisbati hamda kritik so'rov mezoni, ulashilgan domen kodining ~40 foiz chegarasi, funksiya-jadval xaritasi bo'yicha birlashtirish (14.44)
- Neal Ford, Mark Richards, Pramod Sadalage, Zhamak Dehghani, *Software Architecture: The Hard Parts*, 1-nashr, O'Reilly, 2021 (copyright 2022), 8-bob (220-222, 233-235, 239-241-betlar) - kodni nusxalash faqat statik bir martalik kod uchun (`@ServiceEntrypoint` markeri), kutubxona va umumiy servis orasidagi tanlov (bir xil stek va kam o'zgarish, yoki polyglot va tez o'zgarish) hamda servisning runtime xavfi, sidecar va service mesh faqat operatsion bog'lanish uchun va domen sinflari sidecar ga qo'yilmasligi (14.32, 14.36)
- Neal Ford, Mark Richards, Pramod Sadalage, Zhamak Dehghani, *Software Architecture: The Hard Parts*, 1-nashr, O'Reilly, 2021 (copyright 2022), 10-bob (284-286-betlar) - servislararo o'qish kechikishining uch qismi: tarmoq 30-300 ms, xavfsizlik 20-400 ms, qo'shimcha baza chaqirig'i 10-50 ms, jami bir soniyagacha; semantik va statik bog'lanish (14.15)
- Neal Ford, Mark Richards, Pramod Sadalage, Zhamak Dehghani, *Software Architecture: The Hard Parts*, 1-nashr, O'Reilly, 2021 (copyright 2022), 11-bob (300-302-betlar) - mikroservislarda har workflow uchun alohida orkestrator, global ESB bog'lanish nuqtasi bo'lishi va orkestratorda oqimdan tashqari domen xatti-harakati bo'lmasligi (14.45)
- Neal Ford, Mark Richards, Pramod Sadalage, Zhamak Dehghani, *Software Architecture: The Hard Parts*, 1-nashr, O'Reilly, 2021 (copyright 2022), 12-bob (351, 354-357-betlar) - muhim bo'lmagan qadam yiqilganda kompensatsiya o'rniga saga holatini o'zgartirish (`NO_SURVEY`) va orkestratorning fonda tuzatishi, saga larni `enum` va `@Saga` annotatsiyasi bilan reyestrga olish hamda kod skaner CLI (14.45, 14.46)
- Sam Newman, *Monolith to Microservices*, O'Reilly, 2019, 4-bob (198, 201-205-betlar) - qadamlarni qayta tartiblab rollback ni kamaytirish, BPM vositalaridan qochib orkestratsiyani kodda yozish, turli oqimlarga turli orkestrator servis, xoreografiyali saga holatini correlation ID bilan proyeksiya qilish, jamoa egaligi mezoni (bitta jamoa - orkestratsiya, bir nechta jamoa - xoreografiya) va uslublarni aralashtirish (14.8, 14.45)
- Sam Newman, *Monolith to Microservices*, O'Reilly, 2019, 5-bob (209-210-betlar) - jamoaviy egalik taxminan 20 gacha bir joyda o'tirgan dasturchida ishlashi, 100 dan ortiq dasturchida kuchli egalik, egalik belgilanmaganda "kolander arxitekturasi" va taqsimlangan monolit (14.47)
- Sam Newman, *Building Microservices: Designing Fine-Grained Systems*, 2-nashr, O'Reilly, 2021, 1-bob, "Cost" bo'limi - xarajatni kamaytirish asosiy maqsad bo'lsa mikroservis yomon tanlov, foyda ko'proq mijoz va parallel ishlab chiqishdan keladi. Bu nashrda barqaror bet raqami yo'q, shuning uchun faqat bob va bo'lim nomi ko'rsatilgan (14.1)
- Sam Newman, *Building Microservices: Designing Fine-Grained Systems*, 2-nashr, O'Reilly, 2021, 4-bob, "Pattern: Synchronous Blocking" bo'limi - temporal coupling ikki servis emas, ikki konkret nusxa orasida bo'lishi va javob kutilayotgan nusxa o'lsa javobning yo'qolishi; sekin tekshiruvni (firibgarlik) kritik yo'ldan chiqarib fonda yuritish. Bu nashrda barqaror bet raqami yo'q, shuning uchun faqat bob va bo'lim nomi ko'rsatilgan (14.15, 14.16)
- Sam Newman, *Building Microservices: Designing Fine-Grained Systems*, 2-nashr, O'Reilly, 2021, 5-bob, "Service Meshes and API Gateways" va 14-bob, "Multiple Concerns" bo'limlari - gateway da agregatsiya, protokolni qayta yozish va ichki (east-west) chaqiruvlardan qochish, "dumb pipes, smart endpoints" qoidasi, mahsulot DSL ida ishlash va mantiqni keyin ko'chirishning qiyinligi, gateway jamoasi tiket navbatiga aylanishi. Bu nashrda barqaror bet raqami yo'q, shuning uchun faqat bob va bo'lim nomi ko'rsatilgan (14.27)
- Sam Newman, *Building Microservices: Designing Fine-Grained Systems*, 2-nashr, O'Reilly, 2021, 6-bob, "Saga Failure Modes" bo'limi - saga biznes xatosini (mablag' yetmasligi) hal qiladi, texnik xatoni (payment gateway timeout, 500) emas va ishtirokchilarni ishonchli deb faraz qiladi. Bu nashrda barqaror bet raqami yo'q, shuning uchun faqat bob va bo'lim nomi ko'rsatilgan (14.46)
- Sam Newman, *Building Microservices: Designing Fine-Grained Systems*, 2-nashr, O'Reilly, 2021, 8-bob, "The Database" bo'limi - "bazani bo'lishmang" qoidasi bir mantiqiy servisning bir nechta nusxasiga tegishli emas, holatni boshqaradigan mantiq bitta servis ichida qoladi. Bu nashrda barqaror bet raqami yo'q, shuning uchun faqat bob va bo'lim nomi ko'rsatilgan (14.7)
- Sam Newman, *Building Microservices: Designing Fine-Grained Systems*, 2-nashr, O'Reilly, 2021, 14-bob, "Pattern: Page-Based Decomposition", "Pattern: Widget-Based Decomposition", "Pattern: Micro Frontends", "How Many BFFs?", "Reuse and BFFs" va "BFFs for Desktop Web and Beyond" bo'limlari - veb sayt uchun sahifa asosidagi dekompozitsiya standart tanlov, iFrame dan qochish va widgetlar orasida custom event, sahifa og'irligi uchun avtomatik ogohlantirish, kesishgan imkoniyat widget ga sig'masligi, "one experience, one BFF" qoidasi va jamoa egaligi mezoni, faqat veb UI uchun BFF ning sharti, tashqi tomonga alohida BFF. Bu nashrda barqaror bet raqami yo'q, shuning uchun faqat bob va bo'lim nomlari ko'rsatilgan (14.25, 14.26, 14.28)
- Sam Newman, *Building Microservices: Designing Fine-Grained Systems*, 2-nashr, O'Reilly, 2021, 15-bob, "Pluggable, Modular Microservices" bo'limi (`Changing ownership`, `Run multiple variations`, `External contribution through libraries`) - ko'p kiruvchi pull request ulashilgan servis belgisi, egalikni ko'chirish, umumiy skelet framework va har variantga alohida instance (lockstep reliz narxi), kutubxona orqali tashqi hissa. Bu nashrda barqaror bet raqami yo'q, shuning uchun faqat bob va bo'lim nomi ko'rsatilgan (14.47)
- Vlad Khononov, *Learning Domain-Driven Design*, O'Reilly, 2021, 9-bob (149-152-betlar) - holatli sagani hodisa manbali agregat qilib `CommandIssued` hodisasini outbox relay orqali asinxron bajarish, hamda saga va process manager farqi (hodisadan buyruqqa oddiy moslash va yashirin yaralish, if-else bo'lsa process manager, ochiq yaratiladigan ko'p qadamli jarayon) (14.9, 14.46)
- Mark Richards, Neal Ford, *Fundamentals of Software Architecture*, O'Reilly, 2020, 17-bob, "Transactions and Sagas" bo'limi - kompensatsiya freymvorkining ikki ko'rinishi (pending holat yoki do/undo juftligi), `undo` ning `do` dan murakkabroq bo'lishi va dizayn, implementatsiya hamda debug mehnatini ikki baravardan oshirishi, sagani kamdan-kam ishlatish tavsiyasi (14.46)
- Mark Richards, Neal Ford, *Fundamentals of Software Architecture*, O'Reilly, 2020, 20-bob, "Security" bo'limi - foydalanuvchi turi (administrator, o'z-o'ziga xizmat, hamshira) uchun alohida API gateway, shunda noto'g'ri turdagi so'rov nozik servisga (tibbiy yozuvlar interfeysiga) yetmaydi (14.28)
- Chris Richardson, *Microservices Patterns: With examples in Java*, Manning, 2019, 3-bob, 67-68-betlar - o'zaro ta'sir uslublarining ikki o'lchamli tasnifi (bir-bir yoki bir-ko'p, sinxron yoki asinxron) va beshta uslub; request/response ning IPC texnologiyasiga ortogonalligi, broker orqali ham bloklanishi mumkinligi (14.15)
- ESLATMA: Carnell ning nusxasi 1-nashr (2017) va misollarda Netflix Zuul, Ribbon hamda Eureka ishlatilgan. Bu bobdagi qoidalar mohiyati o'zgarmagan holda Spring Cloud Gateway, Spring Cloud LoadBalancer va zamonaviy discovery nomlari bilan yozilgan; kitobning asl komponenti tegishli joyda ESLATMA bilan ko'rsatilgan
- Chris Richardson, *Microservices Patterns: With Examples in Java*, Manning, 2019, 1-bob (11-bet) - masshtab kubining uch o'qi: X o'qi klonlash va yuk balansi, Z o'qi so'rovni atributi bo'yicha bo'lish (ikkisi hajm muammosini hal qilib murakkablik muammosini hal qilmasligi), faqat Y o'qi (funksional dekompozitsiya) murakkablikni kamaytirishi (14.1)
- Chris Richardson, *Microservices Patterns: With Examples in Java*, Manning, 2019, 2-bob (57-59-betlar, 2.2.5-bo'lim "Obstacles to decomposing an application into services") - dekompozitsiyaning besh to'sig'i: tarmoq kechikishi, sinxron IPC mavjudlikni tushirishi, servislararo ma'lumot izchilligi, ma'lumotning izchil ko'rinishini olish (izchil ko'rinish kerak bo'lsa ma'lumot bitta servisda qolishi sharti) va god sinflar (14.39)
- Chris Richardson, *Microservices Patterns: With Examples in Java*, Manning, 2019, 3-bob (105-bet) - sinxron so'rovni sinxron chaqiruvsiz bajarishning uch yo'li va narxi: ma'lumotni replikatsiya qilish (katta hajmda samarasiz), so'rovni to'liq ishlashdan oldin javob qaytarish (mijozni murakkablashtiradi, polling yoki xabarnoma kerak), servisni faqat asinxron API bilan ta'riflash (ommaviy API da ko'pincha mumkin emas) (14.10)
- Chris Richardson, *Microservices Patterns: With Examples in Java*, Manning, 2019, 6-bob (198-bet) - event store ni idempotentlik ombori sifatida ishlatgandagi bo'sh natija tuzog'i: xabarni ishlash hech qanday event chiqarmasa xabar ishlangani haqida yozuv qolmasligi va qayta yetkazilganda noto'g'ri xulq paydo bo'lishi, yechim esa har holatda soxta (pseudo) event yozish va iste'molchilarni uni e'tiborsiz qoldirishga majburlash (14.18)
- Chris Richardson, *Microservices Patterns: With Examples in Java*, Manning, 2019, 12-bob (427-bet) - service mesh ning kam aytiladigan foydasi deploy ni relizdan ajratishi: servisni productionga joylab sinab, faqat shundan keyin unga haqiqiy trafikni yo'naltirish mumkin bo'lishi va bu yangi versiya chiqarishning ishonchliligini oshirishi (14.34)
- ESLATMA: Richardson ning kitobidan faqat pattern darajasidagi qoidalar olingan; uning vendor freymvorkiga xos tafsiloti (Eventuate Tram, Eventuate Local) korpus qamrovidan tashqarida qoldirilgan

---

[&larr; 13. Domain-Driven Design patternlari](13-domain-driven-design-patternlari.md) · [Mundarija](README.md) · [15. Enterprise Integration Patterns I: xabarlar, kanallar, marshrutlash &rarr;](15-enterprise-integration-patterns-i-xabarlar.md)
