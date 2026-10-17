<!-- doc: patterns | chapter: 13 | part:  -->

[Barcha hujjatlar](../../README.md) / [Dizayn patternlar](README.md)

> Holat: tekshirilmoqda. Da'volar hali manbaga solishtirilmoqda.

# 13. Domain-Driven Design patternlari (DDD Patterns)

<details>
<summary>Bu bobdagi 63 bo'lim</summary>

- [13.1 Umumiy til (Ubiquitous Language)](#131-umumiy-til-ubiquitous-language)
- [13.2 Chegaralangan kontekst (Bounded Context)](#132-chegaralangan-kontekst-bounded-context)
- [13.3 Kontekst xaritasi (Context Map)](#133-kontekst-xaritasi-context-map)
- [13.4 Umumiy yadro (Shared Kernel)](#134-umumiy-yadro-shared-kernel)
- [13.5 Mijoz-ta'minotchi (Customer-Supplier)](#135-mijoz-taminotchi-customer-supplier)
- [13.6 Konformist (Conformist)](#136-konformist-conformist)
- [13.7 Buzilishdan himoya qatlami (Anti-Corruption Layer)](#137-buzilishdan-himoya-qatlami-anti-corruption-layer)
- [13.8 Ochiq xizmat interfeysi (Open Host Service)](#138-ochiq-xizmat-interfeysi-open-host-service)
- [13.9 E'lon qilingan til (Published Language)](#139-elon-qilingan-til-published-language)
- [13.10 Ajralgan yo'llar (Separate Ways)](#1310-ajralgan-yollar-separate-ways)
- [13.11 Hamkorlik (Partnership)](#1311-hamkorlik-partnership)
- [13.12 Core / Supporting / Generic subdomenlar (Core / Supporting / Generic Subdomains)](#1312-core--supporting--generic-subdomenlar-core--supporting--generic-subdomains)
- [13.13 Entity (Entity)](#1313-entity-entity)
- [13.14 Qiymat obyekti (Value Object)](#1314-qiymat-obyekti-value-object)
- [13.15 Agregat va Agregat ildizi (Aggregate & Aggregate Root)](#1315-agregat-va-agregat-ildizi-aggregate--aggregate-root)
- [13.16 Repozitoriy (Repository - DDD view)](#1316-repozitoriy-repository---ddd-view)
- [13.17 Fabrika (Factory - DDD view)](#1317-fabrika-factory---ddd-view)
- [13.18 Domen servisi (Domain Service)](#1318-domen-servisi-domain-service)
- [13.19 Ilova servisi (Application Service - DDD view)](#1319-ilova-servisi-application-service---ddd-view)
- [13.20 Domen hodisasi (Domain Event)](#1320-domen-hodisasi-domain-event)
- [13.21 Modul (Module - DDD view)](#1321-modul-module---ddd-view)
- [13.22 Spetsifikatsiya (Specification - DDD view)](#1322-spetsifikatsiya-specification---ddd-view)
- [13.23 Siyosat (Policy)](#1323-siyosat-policy)
- [13.24 Invariantlar (Invariants)](#1324-invariantlar-invariants)
- [13.25 Agregatlar orasida yakuniy izchillik (Eventual Consistency Between Aggregates)](#1325-agregatlar-orasida-yakuniy-izchillik-eventual-consistency-between-aggregates)
- [13.26 Yon ta'sirsiz funksiyalar (Side-Effect-Free Functions)](#1326-yon-tasirsiz-funksiyalar-side-effect-free-functions)
- [13.27 Niyatni ochib beruvchi interfeyslar (Intention-Revealing Interfaces)](#1327-niyatni-ochib-beruvchi-interfeyslar-intention-revealing-interfaces)
- [13.28 Amallarning yopiqligi (Closure of Operations)](#1328-amallarning-yopiqligi-closure-of-operations)
- [13.29 Mustaqil sinflar (Standalone Classes)](#1329-mustaqil-sinflar-standalone-classes)
- [13.30 Egiluvchan dizayn (Supple Design)](#1330-egiluvchan-dizayn-supple-design)
- [13.31 Anemik domen modeli (anti) (Anemic Domain Model (anti))](#1331-anemik-domen-modeli-anti-anemic-domain-model-anti)
- [13.32 Event Storming (texnika) (Event Storming (technique))](#1332-event-storming-texnika-event-storming-technique)
- [13.33 Spring Data bilan domen hodisalari (Domain Events with Spring Data: AbstractAggregateRoot, @DomainEvents)](#1333-spring-data-bilan-domen-hodisalari-domain-events-with-spring-data-abstractaggregateroot-domainevents)
- [13.34 DDD qatlamli arxitekturasi (DDD Layered Architecture)](#1334-ddd-qatlamli-arxitekturasi-ddd-layered-architecture)
- [13.35 Pul (Money (Value Object specialization))](#1335-pul-money-value-object-specialization)
- [13.36 Modelga asoslangan dizayn (Model-Driven Design)](#1336-modelga-asoslangan-dizayn-model-driven-design)
- [13.37 Qo'li ishda bo'lgan modelchilar (Hands-On Modelers)](#1337-qoli-ishda-bolgan-modelchilar-hands-on-modelers)
- [13.38 Smart UI (anti-pattern) (Smart UI Anti-Pattern)](#1338-smart-ui-anti-pattern-smart-ui-anti-pattern)
- [13.39 Uzluksiz integratsiya (Continuous Integration - model darajasida)](#1339-uzluksiz-integratsiya-continuous-integration---model-darajasida)
- [13.40 Assertions (Assertions)](#1340-assertions-assertions)
- [13.41 Tushuncha konturlari (Conceptual Contours)](#1341-tushuncha-konturlari-conceptual-contours)
- [13.42 Deklarativ dizayn (Declarative Design)](#1342-deklarativ-dizayn-declarative-design)
- [13.43 Chuqur tushunchaga qarab refactoring (Refactoring Toward Deeper Insight)](#1343-chuqur-tushunchaga-qarab-refactoring-refactoring-toward-deeper-insight)
- [13.44 Breakthrough (Breakthrough)](#1344-breakthrough-breakthrough)
- [13.45 Distillation (Distillation)](#1345-distillation-distillation)
- [13.46 Domen qarashlari bayonoti (Domain Vision Statement)](#1346-domen-qarashlari-bayonoti-domain-vision-statement)
- [13.47 Yoritilgan yadro (Highlighted Core)](#1347-yoritilgan-yadro-highlighted-core)
- [13.48 Kogeziyali mexanizmlar (Cohesive Mechanisms)](#1348-kogeziyali-mexanizmlar-cohesive-mechanisms)
- [13.49 Ajratilgan yadro (Segregated Core)](#1349-ajratilgan-yadro-segregated-core)
- [13.50 Abstrakt yadro (Abstract Core)](#1350-abstrakt-yadro-abstract-core)
- [13.51 Katta masshtabli struktura (Large-Scale Structure)](#1351-katta-masshtabli-struktura-large-scale-structure)
- [13.52 Rivojlanuvchi tartib (Evolving Order)](#1352-rivojlanuvchi-tartib-evolving-order)
- [13.53 Tizim metaforasi (System Metaphor)](#1353-tizim-metaforasi-system-metaphor)
- [13.54 Mas'uliyat qatlamlari (Responsibility Layers)](#1354-masuliyat-qatlamlari-responsibility-layers)
- [13.55 Bilim darajasi (Knowledge Level)](#1355-bilim-darajasi-knowledge-level)
- [13.56 Ulanadigan komponent frameworki (Pluggable Component Framework)](#1356-ulanadigan-komponent-frameworki-pluggable-component-framework)
- [13.57 Hodisa manbali domen modeli (Event-Sourced Domain Model)](#1357-hodisa-manbali-domen-modeli-event-sourced-domain-model)
- [13.58 Model tarjimasi (Model Translation)](#1358-model-tarjimasi-model-translation)
- [13.59 Biznes logika shaklini tanlash evristikasi (Business Logic Implementation Patterns Heuristic)](#1359-biznes-logika-shaklini-tanlash-evristikasi-business-logic-implementation-patterns-heuristic)
- [13.60 Dizayn qarorlari evolyutsiyasi (Evolving Design Decisions)](#1360-dizayn-qarorlari-evolyutsiyasi-evolving-design-decisions)
- [13.61 Analiz patternlarini qo'llash (Applying Analysis Patterns)](#1361-analiz-patternlarini-qollash-applying-analysis-patterns)
- [13.62 Strategiyani birga yig'ish (Bringing the Strategy Together)](#1362-strategiyani-birga-yigish-bringing-the-strategy-together)
- [13.63 Amalda qo'llash](#1363-amalda-qollash)

</details>



Domain-Driven Design patternlari - bu kodni emas, balki biznes domenini va jamoalar o'rtasidagi chegaralarni modellashtirish haqidagi patternlar to'plami. Ular ikki qatlamga bo'linadi: strategik qism (Bounded Context, Context Map, subdomen turlari, integratsiya munosabatlari) tizimni qanday bo'laklarga ajratish va bu bo'laklar o'zaro qanday gaplashishini belgilaydi; taktik qism (Aggregate, Entity, Value Object, Repository va boshqalar) esa bitta kontekst ichidagi model tuzilishini belgilaydi. Atamalarning kelib chiqishi bir xil emas: "strategic design" Evans kitobining IV qismi nomi, "tactical design" esa Evans kitobida umuman uchramaydi - u Khononov kitobining II qismi nomi. Shuning uchun "taktik DDD" nomini Evans ga tiqishtirish xato. Arxitektor uchun strategik qism ayniqsa muhim, chunki monolitni mikroservislarga ajratish, jamoa mas'uliyat chegaralarini belgilash va legacy tizimlar bilan integratsiya qarorlari aynan shu patternlar tilida qabul qilinadi. Spring ekotizimida bu patternlar Spring Modulith, jMolecules, Spring Cloud Contract va OpenAPI kabi vositalar yordamida kod darajasida majburlanadigan (enforceable) qoidalarga aylanadi.

## 13.1 Umumiy til (Ubiquitous Language)

**Tavsif:** Biznes ekspertlari, dasturchilar va testerlar bitta domen haqida bir xil atamalar bilan gapirishini ta'minlaydigan pattern. Muammo shundaki, biznes "buyurtma bekor qilindi" deydi, kod esa `OrderEntity.setStatus(4)` deb yozadi - natijada har bir muloqotda tarjima yuz beradi va tarjima paytida ma'no yo'qoladi. Yechim: domen atamalarini to'g'ridan-to'g'ri kod identifikatorlariga aylantirish - sinf, metod, event va API maydon nomlari biznes lug'ati bilan bir xil bo'ladi. Umumiy til har bir Bounded Context ichida alohida va o'ziga xos bo'ladi, global emas: Evans bu patternni 2-bobda (UBIQUITOUS LANGUAGE) beradi, Khononov esa uni 3-bobda bounded context chegarasi bilan aniq bog'laydi.

**Spring'da qayerda uchraydi:** Domen sinflari nomlanishida: `@Entity class Shipment`, `shipment.dispatch()` (`setStatus()` emas), Java 17+ `record Money(BigDecimal amount, Currency currency)` va `sealed interface OrderState permits Draft, Confirmed, Cancelled`. jMolecules kutubxonasi (`org.jmolecules:jmolecules-ddd`) `@AggregateRoot`, `@ValueObject`, `@Repository`, `@DomainEvent` annotatsiyalarini beradi - ular modeldagi rolni kodda aniq ifodalaydi. ArchUnit (`com.tngtech.archunit`) yoki `jmolecules-archunit` bilan nomlash va qatlam qoidalarini test sifatida majburlash mumkin; Spring Modulith `Documenter` esa shu nomlarni avtomatik hujjatga chiqaradi. Event nomlari `ApplicationEventPublisher.publishEvent(new OrderConfirmed(...))` ko'rinishida o'tgan zamon fe'li bilan yoziladi.

**Qo'llanish keyslari:**
- Sug'urta domenida `Policy`, `Endorsement`, `Claim` atamalarini DTO, REST path va Kafka topic nomlarida bir xil saqlash.
- Legacy bazadagi `TBL_ORD_HDR` jadvalini `@Table(name = "TBL_ORD_HDR") class Order` orqali domen tiliga mapping qilish.
- Event-driven tizimda `payment.captured` kabi topic nomlarini biznes glossariy bilan moslashtirish.
- Yangi dasturchini onboarding qilishda kod bazasining o'zi glossariy vazifasini bajarishi.
- ArchUnit testi bilan `*Manager`, `*Helper`, `*Util` kabi ma'nosiz nomlarni domen paketlarida taqiqlash.

**Ehtiyot bo'ling:** Umumiy tilni butun kompaniya uchun yagona "korporativ kanonik model"ga aylantirishga urinish eng keng tarqalgan xato - har bir kontekstda `Customer` so'zi boshqa ma'noni bildiradi va bu normal. Shuningdek, atamalarni bir marta kelishib, keyin biznes o'zgarganda kodni refactor qilmaslik tilni tezda o'lik hujjatga aylantiradi.

```java
// Domen tilidagi atama kodda ham shu nom bilan turadi
public class Policy {                      // "shartnoma" emas, sug'urta tilida "polis"
    private PolicyNumber number;
    private Premium premium;               // "narx" emas, "mukofot puli"

    public void endorse(Endorsement e) { } // "update" emas, "o'zgartirish kiritish"
    public void lapse() { }                // "deactivate" emas, "muddati o'tish"
}
// Yomon: OrderManager.processData(), DataService.handle()
// Lug'at jamoada kelishiladi va kod review da tekshiriladi: yangi atama
// paydo bo'lsa, u lug'atga qo'shiladi, sinonim ishlatilmaydi.
```

## 13.2 Chegaralangan kontekst (Bounded Context)

**Tavsif:** Domen modelining ma'noga ega bo'lgan aniq chegarasini belgilaydi: shu chegara ichida har bir atama bitta aniq ma'noga ega, chegaradan tashqarida esa boshqa model boshlanadi. Bu katta tizimda bitta yagona model qurish imkonsizligi muammosini hal qiladi - model o'sgani sari ichki qarama-qarshiliklar paydo bo'ladi. Amalda kontekst o'z modeli, o'z ma'lumotlar bazasi sxemasi va o'z jamoasiga ega bo'ladi; tashqi dunyo bilan faqat aniq belgilangan API yoki eventlar orqali gaplashadi. Pattern Evans kitobining 14-bobida (BOUNDED CONTEXT) beriladi. Mikroservis chegarasi bilan aralashtirmang: Khononov 14-bobda munosabat nosimmetrik ekanini ko'rsatadi - har bir mikroservis bounded context, lekin har bir bounded context mikroservis emas; bounded context eng keng maqbul chegara ("eng katta maqbul monolit") ni, agregat esa eng tor chegarani belgilaydi. Servis chegarasi uchun Khononov muvozanatli evristika sifatida subdomen chegarasini tavsiya qiladi (13.12).

**Spring'da qayerda uchraydi:** Spring Modulith (`org.springframework.modulith`) bu patternni modulit ichida majburlaydi: har bir top-level paket modul bo'ladi, `@ApplicationModule(allowedDependencies = {...})` bilan ruxsat etilgan bog'liqliklar e'lon qilinadi, `package-info.java` esa modul metadatasini saqlaydi. `ApplicationModules.of(App.class).verify()` testi chegara buzilishini build vaqtida yiqitadi. Kattaroq ajratishda Maven/Gradle multi-module loyiha, har bir kontekstga alohida Flyway/Liquibase migratsiya papkasi va alohida PostgreSQL schema ishlatiladi. To'liq ajratilganda har bir kontekst mustaqil Spring Boot 3.x/4.x ilovasi bo'ladi.

```java
@ApplicationModule(allowedDependencies = { "shared" })
package com.acme.billing;

// test:
@Test void verifyModules() {
    ApplicationModules.of(ShopApplication.class).verify();
}
```

**Qo'llanish keyslari:**
- Monolitni ajratishdan oldin Spring Modulith bilan mantiqiy chegaralarni o'rnatib, keyin modulni servisga chiqarish.
- E-commerce'da `Catalog`, `Ordering`, `Shipping`, `Billing` kontekstlarini alohida jamoalarga biriktirish.
- Bitta `Product` tushunchasini katalogda (rasm, tavsif) va omborda (SKU, qoldiq) alohida modellashtirish.
- Har bir kontekst uchun alohida DB schema va alohida `DataSource` bean'i bilan tranzaksiya chegarasini aniq ushlash.
- Jamoa o'sganda (Team Topologies) kontekst chegarasini jamoa chegarasi bilan moslashtirish.

**Ehtiyot bo'ling:** Kontekstni texnik qatlam (controller/service/repository) bo'yicha emas, biznes qobiliyati bo'yicha ajratish kerak - aks holda "distributed monolith" chiqadi. Juda mayda kontekstlar esa bitta use-case uchun ko'p tarmoq chaqiruvini keltiradi va Khononov 14-bobda buni "taqsimlangan big ball of mud" deb ataydi; chegarani ma'lumot bir joyda o'zgarishi (tranzaksiya yaxlitligi) talab qiladigan joyda chizing.

## 13.3 Kontekst xaritasi (Context Map)

**Tavsif:** Tizimdagi barcha Bounded Context'larni va ular orasidagi munosabat turlarini (Shared Kernel, Customer-Supplier, Conformist, ACL, Open Host Service va h.k.) ko'rsatadigan xarita. Muammo: jamoalar o'z kontekstini biladi, lekin kim kimga qaram, kim upstream, kim downstream ekani hech qayerda yozilmagan - natijada har bir o'zgarish kutilmagan buzilishlarga olib keladi. Xarita texnik integratsiya emas, balki jamoalar o'rtasidagi siyosiy va tashkiliy munosabatni ham ko'rsatadi. Evans bu patternni 14-bobda (CONTEXT MAP) beradi va munosabat turlarini shu bobda ketma-ket sanab chiqadi; Khononov 4-bobda bir xil ro'yxatni kooperatsiya, mijoz-ta'minotchi va ajralgan yo'llar deb uch guruhga ajratadi.

**Spring'da qayerda uchraydi:** Spring Modulith `Documenter` sinfi (`new Documenter(modules).writeModulesAsPlantUml().writeIndividualModulesAsPlantUml().writeModuleCanvases()`) modullar va ularning bog'liqliklarini PlantUML/C4 diagrammalari va "module canvas" ko'rinishida avtomatik generatsiya qiladi - xarita kod bilan sinxron qoladi. Servislar darajasida Spring Cloud Contract'dagi contract fayllari kim kimning iste'molchisi ekanini ko'rsatadi; Micrometer Tracing (`io.micrometer:micrometer-tracing-bridge-otel`) + Zipkin/Tempo esa real chaqiruv grafini chiqaradi. Structurizr DSL yoki C4-PlantUML bilan qo'lda yozilgan xarita `/docs` papkasida ADR'lar yonida saqlanadi.

**Qo'llanish keyslari:**
- Monolitdan mikroservislarga migratsiya rejasini tuzishda qaysi modulni birinchi chiqarishni aniqlash.
- Yangi integratsiya talabi kelganda ACL kerakmi yoki OHS yetarlimi degan qarorni hujjatlashtirish.
- Legacy ERP bilan bog'liq barcha downstream kontekstlarni topib, risk tahlili qilish.
- Spring Modulith canvas'ini CI'da generatsiya qilib, PR'da arxitektura o'zgarishini ko'rinadigan qilish.
- Jamoalar reorganizatsiyasida Conway qonunini hisobga olib mas'uliyatni qayta taqsimlash.

**Ehtiyot bo'ling:** Xaritani bir marta chizib, devorga osib qo'yish foydasiz - u real holatni emas, orzuni ko'rsatib qoladi; generatsiya qilinadigan qismni CI'ga ulang. Shuningdek, xaritada faqat "strelkalar" ko'rsatib, munosabat turini (kim boshqaradi, kim moslashadi) yozmaslik uning asosiy qiymatini yo'qotadi.

```text
Kontekstlar va ular orasidagi munosabat turi:

  Checkout ──(Customer-Supplier)──> Pricing
  Checkout ──(Anti-Corruption Layer)──> Legacy ERP
  Billing  ──(Shared Kernel: Money, TaxId)──> Checkout
  Analytics ──(Published Language: Avro sxema)──> hammasi
  Marketing ──(Separate Ways)──  (integratsiya yo'q)

Har strelka uchun uch savolga javob yozilishi kerak:
  1) kim shartnomani belgilaydi
  2) o'zgarish qanday e'lon qilinadi
  3) buzilsa kim tuzatadi
Xarita kodda emas, hujjatda yashaydi va har chorakda qayta ko'riladi.
```

## 13.4 Umumiy yadro (Shared Kernel)

**Tavsif:** Ikki yoki undan ko'p Bounded Context ataylab modelning kichik bir qismini - kod, sxema yoki umumiy value object'larni - birgalikda egallaydi va birgalikda boshqaradi. Bu takrorlanishni kamaytiradi, lekin juda qattiq bog'liqlik yaratadi: yadroni bir tomonlama o'zgartirish mumkin emas, har qanday o'zgarish barcha egalar bilan kelishiladi. Shuning uchun yadro iloji boricha kichik va barqaror bo'lishi kerak - odatda faqat o'zgarmas value object'lar va umumiy identifikatorlar. Pattern Evans 14-bobida (SHARED KERNEL) va Khononov 4-bobida (kooperatsiya guruhi) bayon qilinadi.

**Spring'da qayerda uchraydi:** Alohida Maven/Gradle modul (`:shared-kernel`) sifatida chiqariladi va faqat Java `record`/`enum`lardan iborat bo'ladi: `record Money(BigDecimal amount, Currency currency)`, `record CustomerId(UUID value)`. Spring Modulith'da bu `@ApplicationModule(type = Type.OPEN)` yoki `shared` deb nomlangan va barcha modullarga `allowedDependencies` ro'yxatida ruxsat berilgan modul bo'ladi. Framework bog'liqligi bo'lmasligi uchun yadro faqat `jmolecules-ddd` va standart kutubxonaga tayanadi - unda `@Service`, `@Transactional` yoki JPA annotatsiyalari bo'lmasligi tavsiya etiladi. Versiyalash semantik (SemVer) bo'lib, artifact ichki Nexus/Artifactory repozitoriysi orqali tarqatiladi.

**Qo'llanish keyslari:**
- `Money`, `Quantity`, `DateRange` kabi universal value object'larni bir marta yozib, barcha kontekstlarda qayta ishlatish.
- Bir xil `TenantId`/`CustomerId` tipini multi-tenant tizimning barcha modullarida bir xil validatsiya bilan ta'minlash.
- Yaqin ishlaydigan ikki jamoa (masalan Ordering va Invoicing) uchun umumiy soliq hisoblash qoidalarini birgalikda saqlash.
- Umumiy event envelope formati (CloudEvents metadata) uchun kichik umumiy kutubxona.
- Mikroservislarda umumiy xato kodlari va `ProblemDetail` (RFC 9457) tuzilmasini standartlashtirish.

**Ehtiyot bo'ling:** Shared Kernel vaqt o'tib "common-utils" axlatxonasiga aylanib, DTO, mapper, HTTP client va hatto entity'larni o'z ichiga oladi - bu barcha kontekstlarni bir vaqtda deploy qilishga majbur qiladi. Agar jamoalar yadroni birgalikda boshqarishga tayyor bo'lmasa, Shared Kernel o'rniga Published Language yoki ACL tanlang.

```java
// Shared kernel: ikki kontekst ataylab bo'lishadigan kichik yadro
// shared-kernel moduli: faqat o'zgarmas qiymat obyektlari
public record Money(BigDecimal amount, Currency currency) { }
public record TaxId(String value) { }

// Qoidalar:
//  - yadro kichik qoladi va sekin o'zgaradi
//  - o'zgarish ikki jamoa kelishuvi bilan bo'ladi
//  - yadroga entity, repository yoki servis kirmaydi
// Yadro o'sib ketsa, u taqsimlangan monolitning sababiga aylanadi.
```

## 13.5 Mijoz-ta'minotchi (Customer-Supplier)

**Tavsif:** Evans kitobida bu patternning to'liq nomi CUSTOMER/SUPPLIER DEVELOPMENT TEAMS (14-bob), Khononov esa uni Customer-Supplier deb qisqartiradi (4-bob). Ikki kontekst o'rtasidagi upstream/downstream munosabati, bunda upstream (ta'minotchi) downstream (mijoz) ehtiyojlarini hisobga olishga majbur. Mijoz o'z talablarini aytadi, ta'minotchi ularni backlog'ga qo'shadi va o'zgarishlarni oldindan kelishib buzmasdan chiqaradi. Bu munosabatni ishlashiga olib keladigan asosiy mexanizm - avtomatlashtirilgan kontrakt testlari, ular upstream'ning CI'sida ishlab, mijozni buzadigan o'zgarishni darhol ushlaydi.

**Spring'da qayerda uchraydi:** Spring Cloud Contract (`spring-cloud-starter-contract-verifier` producer tomonda, `spring-cloud-starter-contract-stub-runner` consumer tomonda) aynan shu pattern uchun yaratilgan: kontrakt Groovy DSL yoki YAML'da yoziladi, producer build'ida avtomatik test generatsiya qilinadi, consumer esa `@AutoConfigureStubRunner(ids = "com.acme:billing:+:stubs:8090")` bilan real stub'ga qarshi test yozadi. Alternativa - Pact JVM `pact-jvm-provider-spring`. API versiyalash uchun Spring Framework 7 / Spring Boot 4'dagi `@RequestMapping(version = "1.1")` va `ApiVersionConfigurer` ishlatiladi; event kontraktlari uchun Avro + Confluent Schema Registry bilan backward-compatible evolyutsiya.

**Qo'llanish keyslari:**
- Ordering jamoasi Shipping API'dan yangi maydon so'rab, uni rejalashtirilgan sprintda olish.
- CI'da consumer-driven contract testlari bilan upstream deploy'ini buzilishdan oldin to'xtatish.
- Stub Runner yordamida downstream integratsiya testlarini upstream servisni ko'tarmasdan ishlatish.
- Kafka event sxemasini `BACKWARD` compatibility rejimida evolyutsiya qilib, iste'molchilarni buzmaslik.
- SLA va deprecation siyosatini (masalan eski API 2 kvartal yashaydi) kontraktga bog'lab rasmiylashtirish.

**Ehtiyot bo'ling:** Agar upstream jamoa boshqa budjet yoki boshqa prioritetga ega bo'lsa, "mijoz-ta'minotchi" faqat qog'ozda qoladi va amalda Conformist'ga aylanadi - bu holatni oldindan tan olish yaxshiroq. Kontrakt testlarini consumer o'zi yozmasa va ular upstream CI'sida ishlamasa, pattern hech qanday himoya bermaydi.

```java
// Customer-Supplier: yuqori oqim (supplier) quyi oqim talabini hisobga oladi
// Pricing (supplier) chiqargan shartnoma, Checkout (customer) uchun test bo'ladi
@Pact(consumer = "checkout", provider = "pricing")
RequestResponsePact priceQuote(PactDslWithProvider b) {
    return b.given("mahsulot mavjud")
            .uponReceiving("narx so'rovi")
            .path("/quote").method("POST")
            .willRespondWith().status(200)
            .body(new PactDslJsonBody().stringType("total"))
            .toPact();
}
// Shartnoma buzilsa supplier'ning CI si yiqiladi: munosabat shunday
// majburlanadi, yaxshi niyat bilan emas.
```

## 13.6 Konformist (Conformist)

**Tavsif:** Downstream kontekst upstream modeliga hech qanday tarjimasiz, to'liq bo'ysunadi - uning DTO'lari, atamalari va hatto xato kodlarini o'ziga oladi. Bu upstream'ga ta'sir o'tkazish imkoni bo'lmaganda (tashqi vendor, yirik platforma, hukumat API'si) ongli ravishda tanlanadigan strategiya: tarjima qilish narxidan voz kechib, upstream model bilan yashashga kelishiladi. Afzalligi - tez va arzon integratsiya; narxi - upstream modelining nomukammalligi va o'zgarishlari to'g'ridan-to'g'ri ichki kodga kirib keladi. Evans 14-bob (CONFORMIST), Khononov 4-bob.

**Spring'da qayerda uchraydi:** OpenAPI generator (`org.openapitools:openapi-generator-maven-plugin`) yoki `wsdl2java` bilan generatsiya qilingan client sinflari va DTO'lari to'g'ridan-to'g'ri biznes kodida ishlatiladi. Spring Framework 6.1+ `RestClient`, deklarativ HTTP interfeyslar (`@HttpExchange` + `HttpServiceProxyFactory`, Spring Boot 4'da `@ImportHttpServices`) yoki Spring Cloud OpenFeign bilan upstream shakli o'zgartirilmasdan iste'mol qilinadi. Odatiy misollar: Stripe/Twilio SDK model sinflari, Spring Security OAuth2'dagi `OidcUserInfo` claim nomlari, Keycloak admin client DTO'lari.

**Qo'llanish keyslari:**
- To'lov provayderining (Stripe, PayPal) rasmiy SDK modelini o'zgartirmasdan ishlatish.
- Hukumat yoki bank API'sining qat'iy XSD sxemasiga to'liq moslashish.
- MVP yoki PoC bosqichida integratsiyani tez yetkazish uchun ACL yozishni keyinga qoldirish.
- Ichki platforma jamoasi chiqargan standart `platform-events` sxemasiga barcha product jamoalarining bo'ysunishi.
- Faqat o'qish (read-only) integratsiyalarda, ma'lumot biznes qaroriga ta'sir qilmaganda.

**Ehtiyot bo'ling:** Conformist'ni core domain'da ishlatish eng xavfli xato - tashqi vendorning modeli sizning eng qimmatli biznes logikangizni shakllantirib qo'yadi va keyinchalik vendor almashtirish deyarli imkonsiz bo'ladi. Generatsiya qilingan DTO'lar aggregate ichiga kirib ketsa, bu amalda ACL'ni butunlay yo'q qiladi.

```java
// Conformist: quyi oqim yuqori oqim modelini o'zgartirmasdan qabul qiladi
// Tashqi tizim modeli to'g'ridan-to'g'ri ishlatiladi (tarjima yo'q)
@Service
public class TaxReportService {
    private final SoapTaxClient client;

    public void submit(long orderId) {
        // Soliq organining o'z sxemasi: biz uni o'zgartira olmaymiz
        TaxDeclarationType decl = new TaxDeclarationType();
        decl.setInn(taxId);
        client.submit(decl);
    }
}
// Qachon to'g'ri: tashqi model barqaror va bizning domenimizga yaqin.
// Qachon xato: tashqi model domenga sizib kirsa, u butun kodni buzadi -
// o'sha holatda Anti-Corruption Layer kerak.
```

## 13.7 Buzilishdan himoya qatlami (Anti-Corruption Layer)

**Tavsif:** Downstream kontekst bilan upstream o'rtasiga qo'yiladigan tarjima qatlami: tashqi modelni ichki domen modeliga va teskarisiga o'giradi, shu bilan tashqi tizimning "yomon" yoki o'zgaruvchan modeli ichki toza modelni ifloslantirmasligini ta'minlaydi. ACL adapter, facade va translator'lar to'plamidan iborat bo'lib, domen uchun faqat o'z tilida ifodalangan port interfeysini ko'rsatadi. Legacy tizimlar va strangler-fig migratsiyalarida bu asosiy himoya mexanizmi. Evans kitobida pattern nomi bitta so'z bilan yoziladi: ANTICORRUPTION LAYER (14-bob); Khononov 4-bobda uni downstream tomonning model tarjimasi deb beradi.

**Spring'da qayerda uchraydi:** Hexagonal arxitekturada domen paketda port interfeysi (`interface CreditScoreProvider`), infrastructure paketda esa `@Component class BureauCreditScoreAdapter implements CreditScoreProvider` bo'ladi; adapter ichida `RestClient`/`JdbcClient`/`JmsTemplate` va MapStruct (`@Mapper`) yoki qo'lda yozilgan translator ishlatiladi. Spring Retry (`@Retryable`) va Resilience4j (`spring-cloud-starter-circuitbreaker-resilience4j`) ACL ichida joylashtiriladi, shunda tashqi nosozlik domen qatlamiga chiqmaydi. Spring Integration `Transformer`/`MessageChannel` yoki Spring Cloud Stream `Function<ExternalEvent, DomainEvent>` bean'i event oqimi uchun ACL rolini bajaradi; ArchUnit testi domen paketidan tashqi DTO paketiga bog'liqlikni taqiqlaydi.

```java
@Component
class BureauCreditScoreAdapter implements CreditScoreProvider {
    private final RestClient client;
    @Override
    public CreditScore scoreFor(CustomerId id) {
        BureauResponse r = client.get()
            .uri("/v2/score/{ssn}", lookup(id))
            .retrieve().body(BureauResponse.class);
        return CreditScore.of(r.grade(), r.points()); // tarjima
    }
}
```

**Qo'llanish keyslari:**
- Legacy SOAP/COBOL tizimini strangler-fig bilan almashtirishda ichki modelni izolyatsiya qilish.
- Uchta turli CRM provayderini bitta `CustomerDirectory` port orqali almashtirib ishlatish.
- Tashqi API'ning `status: "4"` kabi ma'nosiz qiymatlarini ichki `OrderState` enum'ga o'girish.
- Kafka'dan keladigan tashqi sxemadagi eventni ichki domen eventiga transformatsiya qilish.
- Monolit bazasiga read-only view orqali kirib, yangi servisning modelini undan ajratish.

**Ehtiyot bo'ling:** ACL "anemik mapper"ga aylanib, tashqi maydonlarni bir-bir ichki DTO'ga ko'chirsa, u faqat qo'shimcha kod bo'lib qoladi - tarjima semantik bo'lishi, ya'ni ma'noni o'zgartirishi kerak. Har bir integratsiya uchun ACL yozish ham ortiqcha: barqaror ichki Published Language bilan ishlaganda Conformist arzonroq.

## 13.8 Ochiq xizmat interfeysi (Open Host Service)

**Tavsif:** Upstream kontekst o'z imkoniyatlarini bir nechta iste'molchi uchun mo'ljallangan, barqaror va yaxshi hujjatlashtirilgan protokol orqali taqdim etadi. Har bir yangi mijoz uchun maxsus integratsiya yozish o'rniga, bitta umumiy "host" API quriladi va u ichki modeldan ataylab ajratiladi. OHS odatda Published Language bilan birga keladi: interfeys ochiq, undagi ma'lumot formati esa e'lon qilingan va versiyalangan tilda - Evans 14-bobda ikki patternni ketma-ket beradi va OPEN HOST SERVICE dan PUBLISHED LANGUAGE ga o'tishni alohida transformatsiya sifatida ko'rsatadi. Khononov 4-bobda bu patternni upstream tomonning modeldan ajratilgan ommaviy interfeysi deb ta'riflaydi.

**Spring'da qayerda uchraydi:** `@RestController` + `ResponseEntity` yoki `@HttpExchange` server tomoni bilan REST API; springdoc-openapi (`springdoc-openapi-starter-webmvc-ui`) bilan OpenAPI 3.1 hujjati avtomatik chiqariladi. Spring Framework 7 / Spring Boot 4'da API versiyalash birinchi darajali: `@RequestMapping(version = "2")` va `WebMvcConfigurer#configureApiVersioning`. Spring for GraphQL (`spring-boot-starter-graphql`, `@QueryMapping`/`@SchemaMapping`) ko'p xil iste'molchiga moslashuvchan OHS beradi; gRPC uchun Spring Boot 4'dagi `spring-boot-starter-grpc` yoki `grpc-spring-boot-starter`. Xatolar `ProblemDetail`/`@ExceptionHandler` bilan standartlashtiriladi, kirish nazorati Spring Security OAuth2 Resource Server (`@PreAuthorize`, scope'lar) orqali qo'yiladi.

**Qo'llanish keyslari:**
- Ichki platforma jamoasi `Identity` servisini o'nlab product jamoasiga bitta REST + OpenAPI API orqali berishi.
- Hamkor (B2B) integratsiyalari uchun ochiq, versiyalangan va rate-limited public API chiqarish.
- Mobil, web va BFF'lar bir xil ma'lumotni turlicha shaklda so'rashi uchun GraphQL schema taqdim etish.
- Analytics jamoalari uchun domen eventlarini Kafka'da ommaviy "ochiq" topic sifatida e'lon qilish.
- Legacy monolitning tanlangan qobiliyatlarini yangi servislarga OHS orqali ochib, to'g'ridan-to'g'ri DB kirishini to'xtatish.

**Ehtiyot bo'ling:** Ichki JPA entity'lari yoki ichki enum'larni to'g'ridan-to'g'ri OHS orqali chiqarish eng keng tarqalgan xato - bu tashqi mijozlarni ichki refactoring'ga bog'lab qo'yadi, shuning uchun alohida API model (DTO) shart. Har bir iste'molchi so'roviga yangi endpoint qo'shish OHS'ni "umumiy" bo'lishdan to'xtatadi va uni n ta maxsus integratsiyaga aylantiradi.

```java
// Open Host Service: tashqi iste'molchilar uchun maxsus, barqaror API
@RestController
@RequestMapping("/public/v1")              // ichki API dan alohida
class PublicOrderApi {

    @GetMapping("/orders/{id}")
    PublicOrderDto get(@PathVariable long id) {
        // Ichki modelni tashqariga chiqarmaydi: alohida DTO va alohida versiya
        return PublicOrderDto.of(service.load(id));
    }
}
// Ichki refaktoring tashqi shartnomani buzmasligi kerak, shuning uchun
// ichki va ommaviy API bir xil sinflarni bo'lishmaydi.
```

## 13.9 E'lon qilingan til (Published Language)

**Tavsif:** Kontekstlar o'rtasida ma'lumot almashish uchun ishlatiladigan, rasmiy ravishda e'lon qilingan, versiyalangan va hech bir kontekstning ichki modeliga tegishli bo'lmagan umumiy format. Muammo: agar har bir juftlik o'z formatida gaplashsa, N ta kontekst uchun N² ta tarjima kerak bo'ladi; Published Language esa yagona neytral oraliq tilni beradi. U sxema (schema) ko'rinishida kodlanadi va sxema evolyutsiyasi qoidalari bilan boshqariladi. Evans 14-bob (PUBLISHED LANGUAGE).

**Spring'da qayerda uchraydi:** REST uchun OpenAPI 3.1 spetsifikatsiyasi `src/main/resources/openapi.yaml` sifatida saqlanib, `openapi-generator-maven-plugin` bilan ikki tomonga ham kod generatsiya qilinadi (spec-first). Event'lar uchun Apache Avro yoki Protobuf sxemasi Confluent Schema Registry'da ro'yxatga olinadi; Spring Kafka `KafkaAvroSerializer`/`KafkaAvroDeserializer` bilan, yoki Spring Cloud Schema Registry (`spring-cloud-schema-registry-client`) bilan ishlatiladi. CloudEvents (`io.cloudevents:cloudevents-spring`) event envelope standartini beradi; Spring Modulith esa `spring-modulith-events-api` va JSON serializatsiya orqali tashqariga chiqadigan "externalized events"ni (`@Externalized`) alohida e'lon qilingan shaklga ajratadi.

**Qo'llanish keyslari:**
- O'nlab servis iste'mol qiladigan `customer.created` eventini Avro sxemasi bilan rasmiylashtirish.
- Spec-first ishlab chiqishda OpenAPI faylini kontrakt sifatida alohida git repozitoriyda versiyalash.
- Moliya sohasida ISO 20022 yoki FHIR kabi tarmoq standartini Published Language sifatida qabul qilish.
- Schema Registry'da `BACKWARD`/`FULL` compatibility qoidasini CI'da majburlab, buzuvchi o'zgarishni bloklash.
- Spring Modulith'da ichki domen eventini `@Externalized` bilan tashqi barqaror formatga mapping qilish.

**Ehtiyot bo'ling:** Published Language'ni "yagona korporativ kanonik model"ga aylantirmang - u barcha kontekstlarning birlashmasi bo'lib ketsa, hech kimga mos kelmaydigan va doimo o'zgaradigan gigant sxema chiqadi; faqat almashish uchun zarur maydonlarni kiritgan. Sxema versiyalash siyosati va deprecation jarayoni bo'lmasa, e'lon qilingan til birinchi buzuvchi o'zgarishda ishdan chiqadi.

```json
# Published language: hamma kelishgan, versiyalangan sxema
# orders.placed.v1.avsc
{
  "type": "record",
  "name": "OrderPlaced",
  "namespace": "com.example.orders.v1",
  "fields": [
    {"name": "orderId", "type": "long"},
    {"name": "total", "type": "string"},
    {"name": "currency", "type": "string"},
    {"name": "placedAt", "type": {"type": "long", "logicalType": "timestamp-millis"}},
    {"name": "channel", "type": ["null", "string"], "default": null}
  ]
}
# Schema registry moslik rejimi BACKWARD bo'lsin: yangi maydon default
# bilan qo'shiladi, mavjud maydon olib tashlanmaydi.
```

## 13.10 Ajralgan yo'llar (Separate Ways)

**Tavsif:** Ikki kontekst ataylab hech qanday integratsiyaga ega bo'lmaydi - ehtiyoj kichik, integratsiya narxi esa yuqori bo'lgani uchun har biri o'z yechimini mustaqil quradi. Bu "hech narsa qilmaslik" emas, balki ongli arxitektura qarori: bog'liqlikni butunlay yo'q qilish orqali jamoalar maksimal mustaqillikka erishadi. Takrorlanish (duplication) bu holatda narx emas, balki to'lanadigan ongli to'lov hisoblanadi. Evans 14-bob (SEPARATE WAYS); Khononov 4-bobda integratsiyaning yo'qligini alohida munosabat turi sifatida sanaydi.

**Spring'da qayerda uchraydi:** Amalda bu alohida Spring Boot ilovalari, alohida DB va umumiy kutubxonaning yo'qligi bilan ifodalanadi - ya'ni `shared-kernel` artifact'iga bog'liqlik bo'lmaydi. Spring Modulith'da bu ikki modulning bir-birini `allowedDependencies` ro'yxatida umuman ko'rsatmasligi va `ApplicationModules.verify()` testi bilan bu mustaqillikni himoya qilish demakdir; ArchUnit `noClasses().that().resideInAPackage("..hr..").should().dependOnClassesThat().resideInAPackage("..crm..")` qoidasi bilan ham majburlanadi. Zarur bo'lsa ma'lumot almashish faqat offline (CSV eksport, kechalik batch - Spring Batch) yoki qo'lda amalga oshiriladi.

**Qo'llanish keyslari:**
- Ichki HR ilovasi va mijozlarga qaragan e-commerce platformasi orasida integratsiya qurmaslik.
- Marketing jamoasining landing-page CMS'ini asosiy tizimdan butunlay ajratish.
- Bir martalik, yiliga bir necha bor kerak bo'ladigan hisobotni CSV eksport bilan hal qilish.
- Qisqa muddatli kampaniya mikroservisini asosiy domen bilan bog'lamasdan yozib, keyin o'chirib tashlash.
- Qo'shib olingan (M&A) kompaniyaning tizimini birlashtirmasdan parallel ishlatish qarori.

**Ehtiyot bo'ling:** Separate Ways'ni "biz keyin integratsiya qilamiz" degan kechiktirish sifatida ishlatish xato - vaqt o'tib ikki joyda bir-biriga mos kelmaydigan ma'lumot (masalan ikki xil mijoz ro'yxati) paydo bo'ladi va reconciliation narxi integratsiyadan qimmatroq bo'lib chiqadi. Agar ma'lumot ikki kontekstda ham biznes qaroriga ta'sir qilsa, bu pattern mos emas.

```java
// Separate Ways: integratsiya qilmaslik ham qaror
// Marketing kampaniyalari Checkout bilan integratsiya qilinmaydi:
// ikki tizim bir xil mijoz ro'yxatini mustaqil saqlaydi.
//
// Qachon to'g'ri:
//  - integratsiya narxi foydadan katta
//  - ikki kontekst mustaqil rivojlanadi va bir-biriga tayanmaydi
//  - takrorlangan ma'lumot kichik va eskirsa zarar yo'q
//
// Qarorni ADR sifatida yozib qo'ying: aks holda keyingi jamoa
// "unutilgan integratsiya" deb o'ylab, keraksiz bog'liqlik qo'shadi.
```

## 13.11 Hamkorlik (Partnership)

**Tavsif:** Partnership Evans kitobidagi pattern emas - uning 14-bobidagi munosabat ro'yxatida bu nom yo'q. Atama Khononov kitobining 4-bobidan keladi va u yerda Shared Kernel bilan birga "kooperatsiya" guruhiga kiradi. Ikki kontekst va ularning jamoalari shunday chambarchas bog'liq bo'ladi, birining muvaffaqiyatsizligi ikkinchisini ham muvaffaqiyatsiz qiladi - shuning uchun ular rejalashtirish, integratsiya va chiqarishni (release) birgalikda muvofiqlashtiradi. Bu yerda upstream/downstream ierarxiyasi yo'q: interfeys o'zgarishi ikki tomonning kelishuvi bilan bo'ladi va ikkisi bir vaqtda deploy qilinadi. Bu eng qimmat munosabat turi, shuning uchun uzoq muddat saqlanmasligi, vaqtincha holat bo'lishi kerak.

**Spring'da qayerda uchraydi:** Amalda bitta monorepo yoki bitta Maven aggregator loyihada ikki modul, umumiy CI pipeline va birgalikda chiqariladigan versiyalar bilan ifodalanadi. Spring Cloud Contract ikki tomonlama ishlatiladi - har bir jamoa ikkinchisi uchun ham producer, ham consumer kontraktlarini saqlaydi va ikkala CI'da testlar ishlaydi. Spring Modulith'da bu ikki modulning o'zaro `allowedDependencies` orqali ochiq bog'lanishi yoki umumiy integratsiya testi (`@ApplicationModuleTest` bilan `Scenario` API, `scenario.publish(...).andWaitForEventOfType(...)`) bo'lib, eventlar oqimini uchidan-uchiga tekshiradi. Deploy muvofiqligi uchun ikki servisning versiyalari bitta Helm chart yoki bitta release train bilan chiqariladi.

**Qo'llanish keyslari:**
- Yangi domen uchun `Ordering` va `Payment` kontekstlarini bir vaqtda noldan qurayotgan ikki jamoa.
- Katta migratsiya davrida legacy modul va uning yangi almashtiruvchisi parallel ishlayotgan bosqich.
- Bitta product jamoasi ichidagi ikki modul: chegara bor, lekin release sikli bir xil.
- Spring Modulith `Scenario` API bilan ikki modul o'rtasidagi event oqimini birgalikda test qilish.
- Regulyator talab qilgan xususiyatni ikki servisda bir vaqtda, bir deploy bilan yetkazish.

**Ehtiyot bo'ling:** Partnership'ni doimiy holatga aylantirish mikroservislarning asosiy afzalligi - mustaqil deploy'ni yo'q qiladi; agar munosabat yillar davomida Partnership bo'lib qolsa, bu ikki kontekstni bitta kontekstga birlashtirish kerakligining alomati. Bu pattern faqat jamoalar haqiqatan ham bir xil prioritet va umumiy menejment ostida bo'lganda ishlaydi.

```java
// Partnership: ikki jamoa birga muvaffaqiyatga erishadi yoki birga yiqiladi
// Shartnoma o'zgarishi ikki tomondan ham kelishiladi va birga chiqariladi.
//
// Amalda nima qilinadi:
//  - umumiy integratsiya testlari ikki repoda ham ishlaydi
//  - reliz oynasi birga rejalashtiriladi
//  - buzuvchi o'zgarish uchun umumiy expand/contract rejasi
//
// Bu eng qimmat munosabat: u faqat chegara noto'g'ri qo'yilgan joyda
// kerak bo'ladi. Partnership ko'payib ketsa, chegaralarni qayta ko'ring.
```

## 13.12 Core / Supporting / Generic subdomenlar (Core / Supporting / Generic Subdomains)

**Tavsif:** Uch turli taksonomiya Evans kitobining emas: Evans 15-bobda faqat CORE DOMAIN va GENERIC SUBDOMAINS patternlarini beradi, "supporting subdomain" nomi unda yo'q. To'liq uchlik Khononov kitobining 1-bobidan keladi. Domenni uch turga ajratish: Core - kompaniyaga raqobat ustunligi beradigan, eng murakkab va eng qimmatli qism; Supporting - biznes uchun zarur, lekin raqobat ustunligi bermaydigan, mantiqi oddiy qism; Generic - barcha kompaniyalarda bir xil bo'lgan, murakkab lekin raqobat ustunligi bermaydigan qism (autentifikatsiya, hisob-kitob, bildirishnoma, hujjat saqlash). Bu klassifikatsiya investitsiya qarorini belgilaydi: eng kuchli injenerlar va eng puxta DDD modellashtirish Core'ga, Supporting'ga oddiy CRUD yetarli, Generic esa sotib olinadi yoki tayyor yechim bilan yopiladi. Arxitektor uchun bu "qayerga kuch sarflash kerak" degan savolning asosiy javobi. Khononov 1-bobda uch turni murakkablik va raqobat ustunligi bo'yicha solishtiradi: supporting subdomen mantiqi sodda (asosan ETL va shaklga to'ldirish), generic subdomen esa murakkab bo'lishi mumkin, lekin ikkisi ham ustunlik bermaydi. Mikroservis chegarasi uchun Khononov 14-bobda va Richardson 2-bobda (`Decompose by subdomain` patterni) aynan subdomen chegarasi tavsiya qilinadi.

**Spring'da qayerda uchraydi:** Core subdomen aggregate'lar, domen eventlari va boy modellashtirish bilan yoziladi (jMolecules `@AggregateRoot`, Spring Modulith `@ApplicationModule`, `ApplicationEventPublisher`, `@DomainEvents` Spring Data'da). Supporting subdomenlar uchun tez yechimlar: Spring Data REST (`@RepositoryRestResource`), Spring Boot `JdbcClient` bilan oddiy CRUD, Spring Batch bilan ommaviy ishlov. Generic subdomenlar odatda tashqi mahsulot bilan yopiladi: autentifikatsiya - Keycloak yoki Spring Authorization Server, to'lov - Stripe SDK, email/SMS - `spring-boot-starter-mail` yoki provayder API'si, qidiruv - Elasticsearch/OpenSearch (`spring-data-elasticsearch`), fayl saqlash - S3. Bu holatda Generic tizimlar bilan aloqa ACL yoki Conformist orqali quriladi.

**Qo'llanish keyslari:**
- Logistika kompaniyasida marshrut optimizatsiyasini Core deb belgilab, unga eng tajribali jamoani biriktirish.
- Autentifikatsiyani o'zi yozish o'rniga Keycloak/Spring Authorization Server bilan yopish.
- Supporting modullarni Spring Data REST bilan tez yetkazib, Core'ga ko'proq vaqt qoldirish.
- Mikroservis chegaralarini subdomen turiga qarab belgilash: Core alohida servis, Generic esa tashqi SaaS.
- Texnik qarz (tech debt) prioritetlashda Core'dagi qarzni Generic'dagidan yuqori qo'yish.

**Ehtiyot bo'ling:** Eng keng tarqalgan xato - Generic subdomenni (o'z autentifikatsiya yoki bildirishnoma tizimini) o'zi yozib, Core'ni esa shoshma-shosharlik bilan anemik CRUD sifatida qoldirish. Shuni ham yodda tuting: klassifikatsiya statik emas - Khononov 11-bobda subdomen turining o'zgarishini alohida ko'rib chiqadi va olti yo'nalishni sanaydi (core <-> generic, supporting <-> generic, supporting <-> core), shuning uchun klassifikatsiya biznes modeli o'zgarganda qayta ko'riladi.

```text
Subdomen turini aniqlash qarorni belgilaydi:

  Core (raqobat ustunligi)      -> eng yaxshi muhandislar, o'z kodi, chuqur model
    narx hisoblash, fraud baholash
  Supporting (kerak, lekin oddiy) -> sodda yechim, CRUD yetarli
    buyurtma tarixini ko'rsatish, bildirishnoma shabloni
  Generic (hamma uchun bir xil) -> sotib olinadi yoki tayyor yechim
    autentifikatsiya, pochta yuborish, PDF generatsiya

Xato: Generic subdomenga Core darajasida kuch sarflash. Tekshiruv savoli:
"bu kodni raqobatchi ham xuddi shunday yozadimi?" Javob "ha" bo'lsa, u Core emas.
```

## 13.13 Entity (Entity)

**Tavsif:** Entity - bu o'z identifikatori (identity) orqali ajratiladigan domain obyekti: uning atributlari vaqt o'tishi bilan o'zgarsa ham, u bir xil obyekt bo'lib qoladi. Tenglik `equals`/`hashCode` ichida faqat identifikator asosida aniqlanadi, hech qachon barcha maydonlar bo'yicha emas. Entity o'z holatini himoya qiladi: setter'lar o'rniga domain ma'nosiga ega metodlar (`confirm()`, `cancel()`) invariantlarni tekshirib holatni o'zgartiradi. Shu sababli biznes qoidalari service'lar emas, aynan entity ichida yashaydi. Evans bu patternni 5-bobda ENTITIES (AKA REFERENCE OBJECTS) nomi bilan beradi; Khononov 6-bobda entity ni agregatning qurilish bloki sifatida ko'rsatadi va uni mustaqil pattern sifatida alohida ishlatishdan ogohlantiradi.

**Spring'da qayerda uchraydi:** Spring Data JPA'da entity `jakarta.persistence.@Entity` va `@Id`/`@GeneratedValue` bilan belgilanadi; Spring Data MongoDB'da `org.springframework.data.annotation.@Id` va `@Document` ishlatiladi. `org.springframework.data.domain.Persistable` interfeysi yangi/mavjud obyektni ajratishga yordam beradi, `@Version` esa optimistic locking beradi. Audit maydonlari uchun `@CreatedDate`, `@LastModifiedBy` va `@EnableJpaAuditing` mavjud. Java 17+ da identifikatorni `record OrderId(UUID value)` ko'rinishida typed ID qilib JPA `@EmbeddedId` yoki `AttributeConverter` bilan map qilish keng tarqalgan.

**Qo'llanish keyslari:**
- `Order` entity'si statusini `confirm()` metodi orqali faqat `DRAFT` holatidan o'tkazib, noto'g'ri o'tishlarni bloklaydi.
- `Customer` entity'si email o'zgarganda ham bir xil `customerId` bilan saqlanadi va tarixiy buyurtmalari bog'langan qoladi.
- Bank `Account` entity'si `withdraw()` ichida balans manfiy bo'lmasligi invariantini tekshiradi.
- `Subscription` entity'si `renew()` chaqirilganda tugash sanasini o'zi hisoblaydi, controller emas.
- `@Version` bilan bir vaqtda ikki foydalanuvchi bitta `Invoice`ni tahrirlaganda optimistic lock xatosi beriladi.

**Ehtiyot bo'ling:** Lombok `@Data` yoki `@EqualsAndHashCode` ni entity'ga qo'yish barcha maydonlar bo'yicha tenglik va lazy collection'larni yuklab yuboradigan `toString`/`hashCode` muammolarini keltiradi - faqat ID bo'yicha qo'lda yozing. Shuningdek, entity'ni ochiq setter'lar bilan anemic data holder'ga aylantirsangiz, DDD foydasi yo'qoladi va mantiq service'larga tarqaladi.

```java
// Entity: identifikatori bo'yicha tenglik, holati o'zgaradi
@Entity
public class Customer {
    @Id private Long id;
    private String email;

    @Override
    public boolean equals(Object o) {
        if (!(o instanceof Customer other)) return false;
        // ID bo'yicha, lekin ID null bo'lsa faqat o'zi bilan teng
        return id != null && id.equals(other.id);
    }

    @Override
    public int hashCode() { return 31; }    // barqaror: ID keyin paydo bo'ladi
}
// Maydonlar bo'yicha equals yozish entity uchun xato: holat o'zgaradi,
// identifikator esa o'zgarmaydi.
```

## 13.14 Qiymat obyekti (Value Object)

**Tavsif:** Value Object identifikatorga ega bo'lmagan, to'liq o'z qiymatlari bilan aniqlanadigan immutable domain tushunchasi: `Money`, `Address`, `EmailAddress`, `DateRange`. Ikki Value Object barcha maydonlari teng bo'lsa teng hisoblanadi, shuning uchun ularni erkin ulashish, cache qilish va thread'lar orasida uzatish xavfsiz. Ular primitive obsession'ni yo'q qiladi: `BigDecimal amount` + `String currency` juftligi o'rniga valyuta mosligini o'zi tekshiradigan `Money` paydo bo'ladi. Validatsiya konstruktorda bir marta bajarilgach, keyin noto'g'ri qiymat umuman mavjud bo'lolmaydi. Pattern ikki kitobda ham bor: Evans 5-bob (VALUE OBJECTS) va Fowler, *Patterns of Enterprise Application Architecture*, 18-bob (Value Object).

**Spring'da qayerda uchraydi:** Java 17+ `record` Value Object uchun tabiiy vosita - `equals`/`hashCode`/immutability avtomatik. JPA'da `jakarta.persistence.@Embeddable` + `@Embedded` yoki `@AttributeOverride`, murakkab holatlarda `jakarta.persistence.AttributeConverter` ishlatiladi (Hibernate 6.x record'larni `@Embeddable` sifatida qo'llab-quvvatlaydi). Spring MVC'da `org.springframework.core.convert.converter.Converter` yoki `Formatter` ni `WebMvcConfigurer#addFormatters` orqali ro'yxatga olib, HTTP parametrini to'g'ridan-to'g'ri Value Object'ga aylantirish mumkin; JSON uchun Jackson `@JsonCreator`/`@JsonValue`.

**Qo'llanish keyslari:**
- `Money` turi `add()` chaqirilganda valyutalar farq qilsa `IllegalArgumentException` tashlab, valyuta aralashuvini bloklaydi.
- `EmailAddress` record konstruktorida regex validatsiyasi - tizimda noto'g'ri email obyekti hech qachon yaratilmaydi.
- `DateRange` ichida `overlaps()` metodi bron (booking) kesishishini aniqlaydi.
- `Address` ni `@Embeddable` qilib `Customer` jadvalining ustunlariga yoyish, alohida jadval yaratmasdan.
- `PhoneNumber` yoki `Iban` typed ID'lari metod signaturalarida `String` almashinishi xatolarini compile vaqtida to'xtatadi.

**Ehtiyot bo'ling:** Value Object'ni mutable qilib (setter'lar bilan) yozish eng keng tarqalgan xato - bir obyekt ikki joyda ulashilsa, kutilmagan o'zgarishlar tarqaladi; o'zgartirish uchun doim yangi nusxa (`withAmount()`) qaytaring. Juda mayda tushunchalarni ham majburan o'rab chiqish (masalan har bir `boolean` uchun alohida tur) kodni ortiqcha shishiradi.

```java
// Value object: qiymati bo'yicha tenglik, o'zgarmas
public record Money(BigDecimal amount, Currency currency) implements Comparable<Money> {

    public Money {
        Objects.requireNonNull(currency);
        amount = amount.setScale(currency.getDefaultFractionDigits(), RoundingMode.HALF_UP);
    }

    public Money plus(Money other) {
        requireSameCurrency(other);
        return new Money(amount.add(other.amount), currency);   // yangi nusxa
    }

    @Override public int compareTo(Money o) { requireSameCurrency(o); return amount.compareTo(o.amount); }
    private void requireSameCurrency(Money o) {
        if (!currency.equals(o.currency)) throw new CurrencyMismatchException(currency, o.currency);
    }
}
// `record` equals, hashCode va toString ni beradi: qiymat semantikasi tekin
```

## 13.15 Agregat va Agregat ildizi (Aggregate & Aggregate Root)

**Tavsif:** Aggregate - bir-biri bilan chambarchas bog'liq entity va Value Object'larning yagona tranzaksion va konsistentlik chegarasi; tashqi dunyo unga faqat Aggregate Root orqali murojaat qiladi (Evans, 6-bob, AGGREGATES). Root invariantlarni himoya qiladi: ichki obyektlarga havola tashqariga chiqmaydi, ichki o'zgarishlar faqat root metodlari orqali bo'ladi. Agregatlar o'zaro ID bilan bog'lanishi va bitta tranzaksiyada bitta agregat o'zgarishi - bu ikki qoida Evans dan keyin qat'iylashgan va manbasi boshqa: Richardson *Microservices Patterns* 5-bobida (5.2.3 `Aggregate rules`) uchta qoidani raqamlab beradi - (1) tashqaridan faqat agregat ildiziga havola, (2) agregatlar o'zaro birlamchi kalit (ID) bilan bog'lanadi, (3) bitta tranzaksiya bitta agregatni yaratadi yoki o'zgartiradi. Khononov 6-bobda ham "bir tranzaksiyaga bitta agregat nusxasi" qoidasini shu shaklda beradi. Evans ning o'zi 6-bobda bundan yumshoqroq yozadi: agregat ichidagi obyektlar boshqa agregat ildizlariga havola ushlashi mumkin, chegara faqat agregat ichiga tashqi havolani taqiqlaydi.

**Spring'da qayerda uchraydi:** Spring Data'da har bir aggregate root uchun bitta `CrudRepository`/`JpaRepository` yaratiladi, va `@OneToMany(cascade = CascadeType.ALL, orphanRemoval = true)` ichki a'zolar hayotiy siklini root'ga bog'laydi. Spring Data JDBC aynan aggregate g'oyasi ustiga qurilgan: u repository'ni faqat root uchun beradi, ichki obyektlarni root bilan birga saqlaydi va o'chiradi, cross-aggregate bog'lanish uchun `org.springframework.data.jdbc.core.mapping.AggregateReference` turini taklif qiladi. `org.springframework.data.domain.AbstractAggregateRoot` esa `registerEvent()` bilan domain event'lar to'plashga yordam beradi, `@Transactional` chegarasi odatda application service'da bitta aggregate'ni qamrab oladi.

**Qo'llanish keyslari:**
- `Order` root va uning `OrderLine` lari bitta aggregate: `order.addLine()` umumiy summa limitini tekshiradi.
- `Cart` aggregate'i ichidagi pozitsiyalar soni va chegirma qoidalarini root ichida saqlab, tashqi service'ga chiqarmaslik.
- `Order` dan `Customer` ga `customerId` (`AggregateReference`) orqali murojaat - ikkisi alohida yuklanadi va alohida saqlanadi.
- Omborda `Shipment` tasdiqlanganda `Order` statusini darhol emas, `ShipmentDispatched` event'i orqali yangilash.
- Spring Data JDBC'da `BlogPost` root bilan `Comment` larini bitta `save()` chaqirig'ida sinxron saqlash.

**Ehtiyot bo'ling:** Katta aggregate (masalan `Customer` ichiga barcha buyurtmalarni solish) lock kurashini, lazy-loading muammolarini va sekin tranzaksiyalarni keltiradi - chegarani invariantlar talab qilgan minimal hajmda saqlang. Bitta tranzaksiyada bir nechta aggregate'ni o'zgartirish deadlock va qattiq bog'lanishga olib keladi.

```java
// Agregat: tashqariga faqat ildiz ko'rinadi, invariant ildizda
@Entity
public class Order {                        // agregat ildizi
    @Id private Long id;
    private OrderStatus status;

    @OneToMany(mappedBy = "order", cascade = ALL, orphanRemoval = true)
    private final List<OrderLine> lines = new ArrayList<>();

    public void addLine(ProductId p, int qty, Money price) {
        if (status != OrderStatus.DRAFT) throw new OrderNotEditableException(id);
        if (lines.size() >= 100) throw new TooManyLinesException(id);   // invariant
        lines.add(new OrderLine(this, p, qty, price));
    }

    public List<OrderLine> lines() { return List.copyOf(lines); }  // tashqariga nusxa
}
// OrderLine uchun repository yo'q va u tashqaridan o'zgartirilmaydi
```

## 13.16 Repozitoriy (Repository - DDD view)

**Tavsif:** DDD'dagi Repository - aggregate root'lar uchun xotiradagi kolleksiya illyuziyasini beradigan, domain tilida yozilgan abstraksiya; u SQL, jadval yoki ORM haqida hech narsa oshkor qilmaydi. Interfeys domain qatlamida (`OrderRepository`), implementatsiya esa infrastructure qatlamida yashaydi - bu Dependency Inversion'ning amaliy ko'rinishi. Metod nomlari domain niyatini aks ettiradi (`findOverdueInvoices()`), CRUD jargonini emas. Har bir aggregate uchun bitta repository bo'ladi, ichki entity'lar uchun alohida repository yaratilmaydi. Repository ikki kitobda ham mustaqil pattern sifatida bor: Evans 6-bob (REPOSITORIES) va Fowler PoEAA 13-bob (Repository, Edward Hieatt va Rob Mee yozgan). Shu bilan bog'liq Unit of Work esa DDD patterni emas - u faqat PoEAA 11-bobida (Object-Relational Behavioral Patterns) turadi; Evans kitobida bu nom uchramaydi, shuning uchun uni "DDD patterni" deb atash xato.

**Spring'da qayerda uchraydi:** `org.springframework.data.repository.Repository` va uning avlodlari (`CrudRepository`, `JpaRepository`, `PagingAndSortingRepository`), `@Repository` annotatsiyasi va `PersistenceExceptionTranslationPostProcessor` orqali exception translation. Derived query'lar (`findByCustomerIdAndStatus`), `@Query`, `@Modifying`, Specification/`QueryByExampleExecutor` va murakkab holatlar uchun custom fragment interfeys + `...Impl` sinfi mavjud. Spring Data JDBC yoki `JdbcClient` (Spring Framework 6.1+) toza DDD repository yozish uchun JPA'dan ko'ra ko'proq nazorat beradi; `ListCrudRepository` (Spring Data 3.x) `List` qaytaradi.

**Qo'llanish keyslari:**
- `OrderRepository#findById(OrderId)` va `save(Order)` bilan application service'da persistence detallarini butunlay yashirish.
- Domain qatlamida `interface InvoiceRepository` e'lon qilib, test'larda in-memory `Map` asosidagi fake implementatsiya ishlatish.
- `findByStatusAndDueDateBefore(...)` kabi derived query bilan muddati o'tgan hisob-fakturalarni topish.
- Hisobot uchun murakkab o'qish talabini repository'ga emas, alohida read-model/projection query'ga yo'naltirish.
- Custom fragment (`OrderRepositoryCustom` + `OrderRepositoryImpl`) ichida `JdbcClient` bilan optimallashtirilgan batch yangilash.

**Ehtiyot bo'ling:** Generic `JpaRepository<Order, Long>` ni to'g'ridan-to'g'ri controller'larga ochib yuborish aggregate chegarasini buzadi va har qanday maydonni tashqaridan o'zgartirishga yo'l beradi - domain uchun toraytirilgan interfeys e'lon qiling. Repository'ni hisobot va UI uchun o'nlab `findByXyzOrderByAbc` metodlari bilan to'ldirish uni query-service'ga aylantiradi; bunda CQRS read-model to'g'ri yechim.

```java
// DDD nuqtai nazaridan repository - kolleksiya, DAO emas
public interface Orders {                   // domen paketida, domen tilida
    Optional<Order> byId(OrderId id);
    List<Order> awaitingPayment();          // domen savoli, SQL emas
    void add(Order order);
}

@Repository
class JpaOrders implements Orders {         // infratuzilmada
    private final OrderJpaRepository jpa;
    @Override public List<Order> awaitingPayment() {
        return jpa.findByStatus(OrderStatus.AWAITING_PAYMENT);
    }
}
// Har agregat ildizi uchun bitta repository: OrderLine uchun yo'q
```

## 13.17 Fabrika (Factory - DDD view)

**Tavsif:** Factory murakkab aggregate yoki Value Object'ni yaratish mantig'ini ichkariga yashiradi, shunda mijoz kod obyektni to'liq va invariantlari bajarilgan holatda oladi. Konstruktor juda ko'p parametrli yoki yaratish bir necha qoidaga bog'liq bo'lganda factory ishlatiladi: u domain tilida nomlangan metodlar beradi (`Order.placeFor(customer, cart)`). Factory obyekt yaratadi, lekin uni saqlamaydi - persistence repository'ning ishi. Reconstruction (bazadan tiklash) odatda ORM yoki alohida mapper vazifasi, factory esa yangi obyekt tug'ilishi uchun. Evans bu patternni 6-bobda (FACTORIES) agregat hayotiy sikli bilan birga beradi.

**Spring'da qayerda uchraydi:** Domain ichida bu oddiy `static` factory metod yoki alohida POJO factory sinfi bo'ladi - Spring annotatsiyasi shart emas. Framework darajasida esa `org.springframework.beans.factory.FactoryBean<T>`, `@Bean` metodlari va `ObjectProvider<T>`/`ObjectFactory<T>` (lazy yoki prototype bean olish uchun) mavjud. Agar factory infrastructure'ga bog'liq bo'lsa (masalan `IdGenerator`, `Clock`), uni `@Component` qilib constructor injection bilan `java.time.Clock` va `OrderIdGenerator` ni kiritish mumkin; `@Scope("prototype")` bilan birga `ObjectProvider#getObject(args)` runtime argumentlarni uzatadi.

**Qo'llanish keyslari:**
- `Order.placeFor(customerId, cartItems, clock)` static factory'si buyurtma raqamini generatsiya qilib, bo'sh savat holatini rad etadi.
- `Money.ofMinorUnits(1999, "USD")` kabi nomlangan factory'lar bilan noto'g'ri masshtabni oldini olish.
- `SubscriptionFactory` `@Component` sifatida narx-reja katalogi va `Clock` ga tayanib yangi obraz yaratadi.
- Test'larda object mother / builder factory bilan to'g'ri holatdagi aggregate'ni bir qatorda yasash.
- `FactoryBean` bilan uchinchi tomon SDK klientini (masalan payment gateway) murakkab sozlash bilan bean qilib chiqarish.

**Ehtiyot bo'ling:** Har bir entity uchun avtomatik `XxxFactory` yasash ortiqcha abstraksiya - konstruktor yetarli bo'lsa factory qo'shmang. Factory ichiga repository'ni kiritib, u yerda `save()` chaqirish mas'uliyatlarni aralashtiradi va tranzaksiya chegarasini noaniq qiladi.

```java
// Factory: murakkab agregatni to'g'ri holatda yaratadi
public final class OrderFactory {

    public static Order fromCart(Cart cart, PricingPolicy pricing) {
        if (cart.isEmpty()) throw new EmptyCartException(cart.id());
        Order order = new Order(OrderId.next(), cart.customerId());
        for (CartItem item : cart.items()) {
            // Narx yaratish paytida qotiriladi: keyin o'zgarsa buyurtma o'zgarmaydi
            order.addLine(item.productId(), item.quantity(), pricing.priceOf(item));
        }
        return order;                       // invariant bajarilgan holatda qaytadi
    }
}
// Konstruktor murakkab qoidani ifodalay olmasa, fabrika kerak
```

## 13.18 Domen servisi (Domain Service)

**Tavsif:** Domain Service - tabiiy ravishda biror entity yoki Value Object'ga tegishli bo'lmagan, bir nechta aggregate yoki murakkab domain qoidasini qamrab oladigan stateless domain operatsiyasi. U domain tilida nomlanadi (`PricingService`, `TransferService`, `RiskScoring`) va faqat domain turlari bilan ishlaydi: HTTP, tranzaksiya yoki DTO'lar haqida bilmaydi. Holat saqlamaydi, shuning uchun thread-safe va oson test qilinadi. Domain Service'ni Application Service bilan aralashtirmaslik kerak: birinchisi *nima* qoida, ikkinchisi *qanday* orkestratsiya. Evans bu patternni 5-bobda SERVICES nomi bilan beradi va servisni qatlam bo'yicha (domen, ilova, infratuzilma) ajratadi; Khononov 6-bobda domen servisi ham "bir tranzaksiyaga bitta agregat" qoidasidan chetlab o'tish yo'li emasligini alohida ta'kidlaydi.

**Spring'da qayerda uchraydi:** Toza DDD'da domain service domain qatlamidagi oddiy interfeys/sinf bo'lib, `@Service` annotatsiyasi majburiy emas (framework'dan mustaqil qolishi uchun); amalda ko'pchilik loyihalar uni `@Service` yoki `@Component` qilib constructor injection bilan ro'yxatga oladi. Strategiya variantlari uchun bir interfeysning bir nechta implementatsiyasi `@Qualifier` yoki `List<DiscountRule>` injection bilan tanlanadi. `@Transactional` ni bu yerga qo'ymaslik, balki undan yuqoridagi application service'da ushlab turish tavsiya etiladi; infrastructure'ga ehtiyoj bo'lsa, domain'da port interfeysi (`ExchangeRateProvider`) e'lon qilinib, adapter `@Component` sifatida implement qilinadi.

**Qo'llanish keyslari:**
- `FundsTransferService` ikki `Account` aggregate'i orasidagi o'tkazma qoidalarini (limit, valyuta) bajaradi.
- `PricingService` mahsulot, mijoz segmenti va aksiya qoidalarini birlashtirib yakuniy narxni hisoblaydi.
- `CreditRiskScoringService` bir nechta domain signaldan skor chiqaradi va `RiskLevel` Value Object qaytaradi.
- `SeatAllocationService` parvoz va yo'lovchi afzalliklarini solishtirib o'rin biriktiradi.
- `TaxCalculator` domain service'i mamlakat qoidalarini `List<TaxRule>` injection orqali qo'llaydi.

**Ehtiyot bo'ling:** Entity'dagi mantiqni `XxxService` larga ko'chirish anemic domain model'ga olib keladi - qoida bitta aggregate ichida bajarilsa, uni entity metodi qilib qoldiring. Domain service'ga repository, `RestClient` yoki `@Transactional` ni to'g'ridan-to'g'ri bog'lash domain'ni infrastructure'ga qul qiladi.

```java
// Domain service: bir nechta agregatga tegadigan, lekin birortasiga
// tegishli bo'lmagan qoida
public class TransferService {              // domen paketida, Spring'siz

    public TransferReceipt transfer(Account from, Account to, Money amount) {
        from.withdraw(amount);              // qoida agregatlarda
        to.deposit(amount);
        return new TransferReceipt(from.id(), to.id(), amount, Instant.now());
    }
}
// Farqi ilova servisidan: domen servisi tranzaksiya, xabar yoki
// repository bilan ishlamaydi. U faqat domen qoidasini ifodalaydi.
```

## 13.19 Ilova servisi (Application Service - DDD view)

**Tavsif:** Application Service - use case'ning kirish nuqtasi: u aggregate'ni repository'dan oladi, domain metodini chaqiradi, natijani saqlaydi va tranzaksiya, xavfsizlik, event publish kabi texnik masalalarni boshqaradi. Unda biznes qoidasi bo'lmaydi - faqat orkestratsiya: "load → do → save". U tashqi dunyo (controller, message listener, scheduler) bilan domain orasidagi yupqa qatlam bo'lib, DTO ↔ domain konversiyasini chegarada bajaradi. Shu tufayli bitta use case'ni HTTP, gRPC va Kafka'dan bir xil chaqirish mumkin bo'ladi. Bu qatlam Evans 4-bobidagi Application Layer ga to'g'ri keladi (vazifasi: ishni belgilash va domen obyektlarini yo'naltirish, biznes qoidasini o'zida saqlamaslik); Fowler PoEAA 9-bobidagi Service Layer patterni ham shu rolni tasvirlaydi.

**Spring'da qayerda uchraydi:** `@Service` sinflari `@Transactional` (odatda shu qatlamda), `@PreAuthorize`/`@Secured` (Spring Security 6.x method security), `ApplicationEventPublisher` yoki `@TransactionalEventListener` bilan ishlaydi. `@RestController` faqat validatsiya (`@Valid`) va mapping qilib application service'ni chaqiradi; `@TransactionalEventListener(phase = AFTER_COMMIT)` commit'dan keyingi yon ta'sirlar uchun. Spring Modulith 1.x da application service modul API'si sifatida ochiladi va `ApplicationModuleListener` modullararo aloqani boshqaradi; o'qish uchun `@Transactional(readOnly = true)` qo'llanadi.

```java
@Service
@RequiredArgsConstructor
class PlaceOrderService {
    private final OrderRepository orders;
    private final ApplicationEventPublisher events;

    @Transactional
    public OrderId handle(PlaceOrderCommand cmd) {
        Order order = Order.placeFor(cmd.customerId(), cmd.items());
        orders.save(order);
        order.domainEvents().forEach(events::publishEvent);
        return order.id();
    }
}
```

**Qo'llanish keyslari:**
- `PlaceOrderService#handle(PlaceOrderCommand)` bitta tranzaksiyada buyurtmani yaratib, event chiqaradi.
- `CancelSubscriptionService` da `@PreAuthorize("hasRole('SUPPORT')")` bilan huquqni use case darajasida tekshirish.
- Kafka `@KafkaListener` va `@RestController` ning ikkisi ham bir xil application service'ni chaqirishi.
- `@Transactional(readOnly = true)` bilan query use case'lari uchun read-model'dan DTO qaytarish.
- `@TransactionalEventListener(phase = AFTER_COMMIT)` orqali commit'dan keyin email yuborish topshirig'ini qo'yish.

**Ehtiyot bo'ling:** Application service'ga `if` lar bilan narx hisoblash yoki status o'tishlarini yozib qo'yish - klassik anemic model tuzog'i; bu mantiqni aggregate yoki domain service'ga qaytaring. Shuningdek, bitta `@Transactional` metod ichida bir nechta aggregate'ni o'zgartirib, uzoq davom etuvchi tranzaksiya va deadlock yaratmang.

## 13.20 Domen hodisasi (Domain Event)

**Tavsif:** Domain Event Evans ning 2004-yildagi kitobidagi pattern emas - uning pattern ro'yxatida bu nom yo'q va u keyinroq qo'shilgan. Bu yerdagi bayon Richardson *Microservices Patterns* 5-bobiga (5.3 `Publishing domain events`) va Khononov 6-bobidagi domen hodisasi qurilish blokiga tayanadi. Domain Event - domain'da yuz bergan va boshqa qismlar uchun ahamiyatli bo'lgan faktning immutable yozuvi: `OrderPlaced`, `PaymentFailed`, `InvoiceOverdue`. U o'tgan zamonda nomlanadi, o'zgarmas Value Object sifatida vaqt va kerakli identifikatorlarni olib yuradi, hech qanday xatti-harakat buyurmaydi. Event'lar aggregate'lar va modullar orasidagi bog'lanishni yumshatadi: chiqaruvchi tomon kim tinglayotganini bilmaydi. Natijada cross-aggregate yangilanishlar eventual consistency, audit va integratsiya oson amalga oshadi.

**Spring'da qayerda uchraydi:** `ApplicationEventPublisher#publishEvent(Object)` (POJO event yetarli, `ApplicationEvent` dan meros shart emas: bu overload Spring Framework 4.2 dan beri bor), `@EventListener`, `@TransactionalEventListener` va `@Async` bilan asinxron ishlash. Spring Data'da `org.springframework.data.domain.AbstractAggregateRoot#registerEvent()` yoki `@DomainEvents` + `@AfterDomainEventPublication` metodlari `save()` vaqtida event'larni avtomatik publish qiladi. Spring Modulith 1.x `@ApplicationModuleListener` (transactional + async), event publication registry (`EventPublicationRegistry`) va ishonchli qayta urinish/incomplete publication'larni ko'rish imkonini beradi; tashqi tizimga chiqarish uchun Kafka/RabbitMQ `externalized events` (`@Externalized`) ishlatiladi.

```java
@Entity
class Order extends AbstractAggregateRoot<Order> {
    void confirm() {
        this.status = CONFIRMED;
        registerEvent(new OrderConfirmed(this.id, Instant.now()));
    }
}
```

**Qo'llanish keyslari:**
- `OrderConfirmed` event'i omborda zaxirani band qilish jarayonini ishga tushiradi.
- `@TransactionalEventListener(phase = AFTER_COMMIT)` bilan faqat muvaffaqiyatli commit'dan keyin bildirishnoma yuborish.
- Spring Modulith event registry orqali ishlamay qolgan listener'ni qayta urinishga qo'yish.
- `CustomerRegistered` event'ini Kafka'ga externalize qilib CRM tizimiga integratsiya.
- Event'lar oqimidan audit log va analytics read-model'ini qurish.

**Ehtiyot bo'ling:** Event ichida butun JPA entity'ni (yoki lazy proxy'ni) uzatish detached/lazy xatolari va buzilgan chegaralarga olib keladi - faqat ID va zarur primitiv/Value Object maydonlarini soling. Oddiy `@EventListener` tranzaksiya ichida sinxron ishlaydi, shuning uchun u yerdagi xato asosiy tranzaksiyani rollback qilishi mumkin; yon ta'sirlar uchun `AFTER_COMMIT` yoki modulith registry'dan foydalaning.

## 13.21 Modul (Module - DDD view)

**Tavsif:** Module (Evans'da "Package") - bir-biriga bog'liq domain tushunchalarini yuqori kohezion, past bog'langan birlikka guruhlash usuli; chegaralar texnik qatlamlar bo'yicha emas, biznes qobiliyatlari bo'yicha chiziladi. Har bir modul tashqariga minimal API (command, event, read DTO) ochadi, qolgani `package-private` bo'lib yashiringan holatda qoladi. Bu monolit ichida ham bounded context'larni aniq ushlab turishga va keyinchalik kerak bo'lsa alohida xizmatga ajratishga imkon beradi. Modul chegarasi - refaktoringning asosiy birligi: ichini o'zgartirish tashqi mijozlarga ta'sir qilmaydi. Evans bu patternni 5-bobda MODULES (AKA PACKAGES) nomi bilan beradi.

**Spring'da qayerda uchraydi:** Eng oddiy shakli - `com.shop.order`, `com.shop.billing` kabi package-per-feature tuzilma va `package-private` `@Service`/`@Repository` bean'lar (Spring constructor injection package-private sinflar bilan ham ishlaydi). Spring Modulith 1.x buni rasmiylashtiradi: `@ApplicationModule` (`allowedDependencies` bilan), `ApplicationModules.of(App.class).verify()` testi arxitektura buzilishini build vaqtida tutadi, `Documenter` esa C4/PlantUML diagrammalari va modul kanvasini generatsiya qiladi. Qo'shimcha nazorat uchun ArchUnit qoidalari, Java 17+ `module-info.java` (JPMS) yoki Gradle/Maven multi-module tuzilma ishlatiladi; modullararo aloqa to'g'ridan-to'g'ri bean injection o'rniga event'lar bilan qurilishi afzal.

**Qo'llanish keyslari:**
- `order`, `inventory`, `billing` package'lari har biri `@ApplicationModule` sifatida belgilanib, ruxsat etilgan bog'liqliklar ro'yxati cheklanadi.
- `ApplicationModules.verify()` testi `billing` ning `order` ning internal sinfiga murojaatini CI'da sindiradi.
- `Documenter` bilan modullar diagrammasi va modul kanvasini avtomatik yangilab turish.
- Modullararo integratsiyani `@ApplicationModuleListener` event'lari bilan qilib, keyinchalik `billing` ni alohida servisga chiqarish.
- Maven multi-module loyihada `domain` moduli `spring-web` ga compile bog'liqlik olmasligini majburlash.

**Ehtiyot bo'ling:** `controller`/`service`/`repository` bo'yicha qatlamli package'lash har bir feature'ni uch joyga sochadi va hamma narsa `public` bo'lishini talab qiladi - feature bo'yicha bo'ling. Shuningdek modullarni faqat nomda e'lon qilib, avtomatlashtirilgan tekshiruv (Modulith `verify()` yoki ArchUnit) qo'ymasangiz, chegaralar bir necha sprint ichida yemiriladi.

```text
com.example.sales                 // modul = bounded context ichidagi bo'lak
  Order.java                      // public: agregat ildizi
  OrderLine.java                  // package-private: tashqariga chiqmaydi
  Orders.java                     // public: repository shartnomasi
  internal/
    OrderPricingRules.java        // ichki tafsilot

Modul nomi domen tilida bo'ladi: `sales`, `billing`, `shipping`.
`util`, `common`, `helper` nomlari modul emas, chiqindi qutisi.
Spring Modulith `verify()` bilan chegarani majburlash mumkin.
```

## 13.22 Spetsifikatsiya (Specification - DDD view)

**Tavsif:** Specification - "obyekt shu shartga javob beradimi?" degan biznes predikatini birinchi darajali domain obyektiga aylantiradi. Evans 9-bobda (SPECIFICATION) uning uchta qo'llanishini sanaydi: validatsiya (mavjud obyekt talabga javob beradimi), tanlash (kolleksiya yoki bazadan filtrlash) va buyurtmaga yaratish (building-to-order). Specification'lar `and`, `or`, `not` bilan birlashtirilib, murakkab qoidalarni kichik, nomlangan va alohida test qilinadigan bo'laklardan yig'ish mumkin. Shu bilan `if` lar daraxti o'rniga domain lug'atida o'qiladigan kod paydo bo'ladi.

**Spring'da qayerda uchraydi:** Spring Data JPA'da `org.springframework.data.jpa.domain.Specification<T>` interfeysi va `JpaSpecificationExecutor<T>` (`findAll(Specification, Pageable)`), kompozitsiya uchun `Specification.where(...).and(...).or(...)` hamda `Specification.allOf`/`anyOf` (Spring Data 3.x) mavjud; ichida Criteria API (`jakarta.persistence.criteria.Root`, `CriteriaBuilder`) ishlatiladi. Muqobil variantlar: Query by Example (`QueryByExampleExecutor`, `Example.of(...)`), Querydsl `BooleanExpression` + `QuerydslPredicateExecutor`, shuningdek Spring Security'da `o.s.security.authorization.AuthorizationManager` predikatlari o'xshash g'oyani qo'llaydi. Xotira ichidagi domain tekshiruvi uchun oddiy `Predicate<T>` yoki `interface Spec<T> { boolean isSatisfiedBy(T t); }` yetarli.

**Qo'llanish keyslari:**
- `CustomerSpecs.active().and(CustomerSpecs.inCountry("UZ"))` bilan dinamik qidiruv filtri qurish.
- Admin panelidagi bo'sh bo'lishi mumkin bo'lgan filtrlar uchun `Specification.where(null)` dan boshlab shartlarni qo'shib borish.
- `OverdueInvoiceSpec` ni ham bazadan tanlashda, ham bitta hisob-fakturani tekshirishda qayta ishlatish.
- Chegirma huquqini `EligibleForDiscountSpec` sifatida ifodalab, uni unit test bilan alohida qamrab olish.
- Querydsl `BooleanExpression` lar kutubxonasini qurib, type-safe reporting query'lari yozish.

**Ehtiyot bo'ling:** Criteria API asosidagi juda ko'p qatlamli specification'lar o'qilishi qiyin va kutilmagan JOIN'lar hamda N+1 muammosini keltirib chiqaradi - murakkab o'qish uchun aniq `@Query` yoki alohida read-model ko'pincha sodda yechim. Spring Data `Specification` ni domain qatlamiga tarqatish domain'ni JPA'ga bog'lab qo'yadi; domain ichida framework'siz o'z predikat abstraksiyangizni saqlang.

```java
// DDD da Specification domen qoidasini ifodalaydi, nafaqat so'rov shartini
public interface Specification<T> {
    boolean isSatisfiedBy(T candidate);

    default Specification<T> and(Specification<T> other) {
        return c -> this.isSatisfiedBy(c) && other.isSatisfiedBy(c);
    }
}

public final class EligibleForRefund implements Specification<Order> {
    @Override public boolean isSatisfiedBy(Order o) {
        return o.status() == OrderStatus.DELIVERED
                && Duration.between(o.deliveredAt(), Instant.now()).toDays() <= 14;
    }
}
// Bir xil qoida ikki joyda ishlaydi: xotiradagi obyektni tekshirish va
// so'rov sharti sifatida (Spring Data Specification ga aylantirilib).
```

## 13.23 Siyosat (Policy)

**Tavsif:** Policy - o'zgarib turadigan biznes qoidasini (chegirma, jarima, marshrutlash, retry, autentifikatsiya talabi) alohida, almashtiriladigan obyektga ajratish. Evans bu patternni 12-bobda aynan shu juft nom bilan beradi: STRATEGY AKA POLICY - ya'ni GoF Strategy patternining domen modelidagi ko'rinishi. Qoidalar mijoz, mamlakat, tarif yoki vaqtga qarab farq qilganda, `if/else` daraxti o'rniga bir interfeys va bir nechta nomlangan implementatsiya paydo bo'ladi. Event-driven kontekstda Policy "shu hodisa yuz bersa, shu reaksiya bo'ladi" qoidasi sifatida ham qo'llanadi: Khononov 12-bobda EventStorming ning 6-qadami aynan "Policies" bo'lib, policy stikerlari hodisani buyruqqa bog'laydi. Yangi qoida qo'shish mavjud kodni o'zgartirmaydi - Open/Closed printsipi amalda.

**Spring'da qayerda uchraydi:** Domain'da `interface DiscountPolicy { Money apply(Order order); }` va bir nechta `@Component` implementatsiya; tanlash `@Qualifier`, `List<DiscountPolicy>`/`Map<String, DiscountPolicy>` injection yoki `@ConditionalOnProperty`/`@Profile` orqali bo'ladi. Konfiguratsiya bilan boshqarish uchun `@ConfigurationProperties` va `spring-boot-configuration-processor`; hodisaga reaksiya qiluvchi policy'lar `@EventListener`/`@ApplicationModuleListener` ichida yashaydi. Infrastructure darajasidagi policy misollari: Spring Retry `RetryPolicy`/`BackOffPolicy` va `@Retryable`, Spring Security'da `AuthorizationManager` hamda `PasswordEncoder` strategiyalari, Resilience4j `CircuitBreakerConfig`, `@Cacheable` uchun `RedisCacheConfiguration` TTL siyosatlari.

**Qo'llanish keyslari:**
- `DiscountPolicy` implementatsiyalarini mijoz segmenti bo'yicha `Map<Segment, DiscountPolicy>` dan tanlash.
- Mamlakatga qarab `TaxPolicy` ni `@Qualifier("uzTaxPolicy")` bilan ulash va yangi mamlakatni yangi bean bilan qo'shish.
- `LateFeePolicy` ni `@ConfigurationProperties` orqali sozlab, kodga tegmasdan foizni o'zgartirish.
- `@Retryable(retryFor = TransientException.class, backoff = @Backoff(delay = 200, multiplier = 2))` bilan tashqi API chaqiruvi siyosati.
- `InvoiceOverdue` event'iga javob beruvchi `SuspendAccountPolicy` listener'i hisobni vaqtincha to'xtatadi.

**Ehtiyot bo'ling:** Faqat bitta implementatsiyasi bo'lgan va o'zgarishi kutilmayotgan qoidani Policy interfeysiga o'rash - bu keraksiz abstraksiya; variativlik real paydo bo'lganda ajratishni boshlang. Policy'larni infrastructure annotatsiyalariga (`@Retryable`, `@Cacheable`) bog'lab yuborish domain qoidasini framework'ga qamab qo'yadi va test qilishni qiyinlashtiradi.

```java
// Policy: almashtirilishi mumkin bo'lgan qaror qoidasi
public interface LateFeePolicy {
    Money feeFor(Invoice invoice, LocalDate today);
}

public final class FlatLateFeePolicy implements LateFeePolicy {
    private final Money flat;
    @Override public Money feeFor(Invoice i, LocalDate today) {
        return i.isOverdue(today) ? flat : Money.zero(i.currency());
    }
}

public final class DailyLateFeePolicy implements LateFeePolicy {
    @Override public Money feeFor(Invoice i, LocalDate today) {
        long days = i.daysOverdue(today);
        return i.total().percent(new BigDecimal("0.1")).times(days);
    }
}
// Qoida o'zgarsa yangi Policy qo'shiladi: Invoice kodi o'zgarmaydi
```

## 13.24 Invariantlar (Invariants)

**Tavsif:** Invariant - agregat ichida har qanday tranzaksiya tugaganda doimo rost bo'lishi shart bo'lgan biznes qoidasi ("buyurtma qatorlari summasi jami summaga teng", "hisob qoldig'i limitdan past tushmaydi"). Invariantlar aggregate root'ning konsistentlik chegarasini belgilaydi: root o'z ichidagi barcha o'zgarishlarni nazorat qiladi va har bir public metod oxirida qoidani tekshiradi. Shu sababli agregat hajmi invariantlar to'plamidan kelib chiqadi, ma'lumotlar bazasi jadvallari tuzilishidan emas. Invariant buzilganda obyekt yaratilmaydi yoki amal bajarilmaydi - noto'g'ri holat hech qachon xotirada paydo bo'lmasligi kerak. Evans 6-bobda (AGGREGATES) bu chegarani aniq ajratadi: agregat ichidagi invariantlar har bir tranzaksiya tugashida majburlanadi, agregatlar orasidagi qoidalar esa kelishilgan vaqt ichida hal qilinishi mumkin - ya'ni darhol emas.

**Spring'da qayerda uchraydi:** Eng ishonchli joy - konstruktor va factory metodlar: Java `record` compact constructor, `Objects.requireNonNull`, `org.springframework.util.Assert.isTrue/state` yoki o'z `IllegalArgumentException`/domen exception'laringiz. Deklarativ qism uchun Jakarta Bean Validation (`jakarta.validation.constraints.*`, `@Valid`, `@Validated`) - Spring Boot `spring-boot-starter-validation` orqali `LocalValidatorFactoryBean` va `MethodValidationPostProcessor` bean'larini beradi; Spring Framework 6.1+ controller va bean metodlari uchun built-in method validation'ni qo'llaydi. JPA tomonida Hibernate `BeanValidationEventListener` `@PrePersist`/`@PreUpdate` vaqtida constraint'larni avtomatik tekshiradi (`jakarta.persistence.validation.mode`), konkurent invariantlar uchun esa `@Version` (optimistic locking) yoki `@Lock(LockModeType.PESSIMISTIC_WRITE)` ishlatiladi.

**Qo'llanish keyslari:**
- `Order.addLine(...)` metodi qator qo'shgandan keyin jami summa va maksimal pozitsiya limitini tekshiradi.
- `Email`, `Iban`, `Money` kabi value object'lar konstruktorda formatni tekshiradi va noto'g'ri qiymat bilan yaratilmaydi.
- `BankAccount.withdraw(amount)` qoldiq overdraft limitidan oshmasligini kafolatlaydi.
- Bron qilish agregatida `@Version` bilan bir vaqtda ikki foydalanuvchi bitta joyni band qilishining oldi olinadi.
- `Subscription.changePlan(...)` faqat `ACTIVE` statusda ruxsat etilishini state machine tekshiruvi orqali ta'minlaydi.

**Ehtiyot bo'ling:** Invariantni faqat controller yoki DTO darajasidagi `@Valid` bilan himoya qilish xato - domen obyektini boshqa kod yo'li (importer, message listener, test) chetlab o'tadi, shuning uchun qoida agregat ichida ham turishi shart. Bir nechta agregatni qamrab oluvchi "global invariant" talab qilsangiz, bu agregat chegarasi noto'g'ri tortilganini yoki qoida eventual consistency'ga o'tishi kerakligini bildiradi.

```java
// Invariant: har doim rost bo'lishi kerak bo'lgan shart
public class Order {
    private final List<OrderLine> lines = new ArrayList<>();
    private Money total;

    // Invariant 1: total har doim qatorlar yig'indisiga teng
    // Invariant 2: DRAFT bo'lmagan buyurtma o'zgartirilmaydi
    // Invariant 3: qator soni 100 dan oshmaydi
    public void addLine(OrderLine line) {
        requireDraft();                               // 2
        if (lines.size() >= 100) throw new TooManyLinesException(id);  // 3
        lines.add(line);
        this.total = recalculateTotal();              // 1
    }
}
// Invariant agregat chegarasida tekshiriladi: shuning uchun agregat
// chegarasi "nimani bir vaqtda izchil saqlash kerak" savolidan chiqadi.
```

## 13.25 Agregatlar orasida yakuniy izchillik (Eventual Consistency Between Aggregates)

**Tavsif:** Qoida shu: bitta tranzaksiyada faqat bitta agregat o'zgartiriladi, qolgan agregatlar esa domen hodisalari orqali keyinroq sinxronlanadi. Manba: Richardson 5-bob, `Aggregate rules` ning 3-qoidasi, va Khononov 6-bobidagi "bir tranzaksiyaga bitta agregat nusxasi" talabi; Khononov 6-bobda bir nechta agregatni bitta tranzaksiyada commit qilish ehtiyoji chegara noto'g'ri tortilganining signali deb beriladi. Boshqa agregatlarga obyekt havolasi emas, identifikator (`CustomerId`) bilan murojaat qilinadi, shu bilan tranzaksiya chegarasi va lock maydoni kichik bo'ladi. Natijada sistema bir muddat "nomuvofiq" ko'rinadi, lekin bu oyna biznes nuqtai nazaridan maqbul bo'lsa, scalability va mavjudlik sezilarli yaxshilanadi. Kompensatsiya (sagas, retry, dead-letter) bu yondashuvning ajralmas qismi.

**Spring'da qayerda uchraydi:** `ApplicationEventPublisher` + `@TransactionalEventListener(phase = TransactionPhase.AFTER_COMMIT)` eng oddiy ichki variant. Ishonchli yetkazib berish uchun Spring Modulith: `@ApplicationModuleListener` (`@Async` + `@Transactional(propagation = REQUIRES_NEW)` + `AFTER_COMMIT` kombinatsiyasi) va Event Publication Registry (`event_publication` jadvali, `spring-modulith-events-jpa`/`-jdbc`, broker ko'prigi uchun `spring-modulith-events-kafka`/`-amqp`) - ya'ni transactional outbox pattern tayyor holda. Kattaroq miqyosda `spring-kafka` (`KafkaTemplate`, `@KafkaListener`), `spring-rabbit` yoki `spring-cloud-stream`, idempotentlik uchun `@Transactional` ichida ishlov berilgan message ID jadvali.

**Qo'llanish keyslari:**
- `OrderPlaced` hodisasidan keyin inventar agregati alohida tranzaksiyada zaxirani kamaytiradi.
- Foydalanuvchi profili o'zgarganda, uning nomi buyurtmalar read model'ida darhol emas, hodisa yetib borgandan keyin yangilanadi.
- To'lov tasdiqlangach, `Order` statusi `PAID`ga o'tadi - to'lov va buyurtma agregatlari alohida saqlanadi.
- Loyalty ball hisoblash kechiktirilgan listener'da bajariladi, chunki u buyurtmani qabul qilishni to'xtatmasligi kerak.
- Bir nechta microservice o'rtasida saga: buyurtma bekor qilinganda zaxira va to'lov kompensatsiya hodisalari bilan qaytariladi. Saga ning to'liq tavsifi bu bobda emas: Richardson 4-bob va Khononov 9-bob, korpusda esa 14-bob (microservices patternlari).

**Ehtiyot bo'ling:** Pul, zaxira yoki huquqiy jihatdan qat'iy qoidalar uchun "yakuniy" izchillik yaroqsiz bo'lishi mumkin - biznes bilan ruxsat etilgan nomuvofiqlik oynasini aniq kelishib oling. Oddiy `@EventListener` (`AFTER_COMMIT`siz yoki registry'siz) yetkazib berishni kafolatlamaydi: application qulasa hodisa yo'qoladi, shuning uchun outbox yoki Modulith registry'siz production'da tayanmang.

```java
// Bitta tranzaksiya - bitta agregat. Qolgani hodisa orqali.
@Transactional
public void place(PlaceOrder cmd) {
    Order order = Order.from(cmd);
    orders.add(order);                            // faqat Order agregati
    events.publish(new OrderPlaced(order.id(), order.items()));
}

@Component
class StockReservation {
    @TransactionalEventListener(phase = AFTER_COMMIT)
    void on(OrderPlaced e) {
        inventory.reserve(e.items());             // alohida tranzaksiya
    }
}
// Natija: qisqa vaqt ichida buyurtma bor, zaxira hali band emas.
// Bu holat biznes uchun qabul qilinishi aniq yozilgan bo'lishi kerak,
// va band qilish muvaffaqiyatsiz bo'lsa kompensatsiya rejasi bo'lsin.
```

## 13.26 Yon ta'sirsiz funksiyalar (Side-Effect-Free Functions)

**Tavsif:** Operatsiyalarni ikki turga ajratamiz: holatni o'zgartiruvchi `command`lar va hech narsani o'zgartirmaydigan, faqat natija qaytaruvchi `query`lar (funksiyalar). Murakkab hisob-kitoblarni yon ta'sirsiz funksiyalarga, afzal holda value object'lar ustiga ko'chirsak, ularni erkin chaqirish, kombinatsiyalash, keshlash va test qilish mumkin bo'ladi. Command'lar esa iloji boricha sodda bo'lib, natijani funksiyalardan olib, faqat yakuniy holatni o'rnatadi. Bu Evans ning 10-bobidagi Supple Design to'plamiga kiradi (SIDE-EFFECT-FREE FUNCTIONS) va invariantlar haqida fikrlashni ancha osonlashtiradi.

**Spring'da qayerda uchraydi:** Immutable value object'lar uchun Java `record` va `final` sinflar; `java.time` (`LocalDate.plusDays`, `Period.between`), `BigDecimal` va JSR-354 `MonetaryAmount` (Moneta) - hammasi yangi obyekt qaytaradi. Spring Data JPA'da `Specification<T>` va Querydsl `Predicate` - toza, kombinatsiyalanadigan funksiyalar; `@Transactional(readOnly = true)` esa query yo'lini aniq ajratadi. Keshlash uchun `@Cacheable` faqat yon ta'sirsiz metodlarda xavfsiz; `java.util.stream` va `Collectors` bilan hisob-kitoblarni deklarativ yozish ham shu uslubga mos.

**Qo'llanish keyslari:**
- `Money.add(...)`, `Money.multiply(...)` yangi `Money` qaytaradi, mavjud obyektni o'zgartirmaydi.
- `PricingPolicy.priceFor(cart)` chegirma va soliqni hisoblaydi, lekin savatni o'zgartirmaydi.
- `Itinerary.combine(other)` ikki marshrutni birlashtirib, uchinchi marshrut qaytaradi.
- `@Cacheable` bilan valyuta kursi konvertatsiyasi funksiyasini keshlash.
- `Specification` metodlari (`byStatus`, `createdAfter`) `and`/`or` bilan qo'shilib, qayta ishlatiladigan filtrlar beradi.

**Ehtiyot bo'ling:** "Getter ichida lazy yuklash yoki audit yozish" kabi yashirin yon ta'sirlar funksiya shartnomasini buzadi va keshlashni xavfli qiladi. Har bir hisob uchun yangi obyekt yaratish hot path'da ortiqcha allocation bersa, profiling natijasiga tayanib optimallashtiring - lekin immutable'likni sababsiz tashlab yubormang.

```java
// Yon ta'sirsiz funksiya: hisoblaydi, lekin holatni o'zgartirmaydi
public record Cart(List<CartItem> items) {

    public Money subtotal() {                     // so'rov: yon ta'siri yo'q
        return items.stream().map(CartItem::lineTotal)
                .reduce(Money.zero("UZS"), Money::plus);
    }

    public Cart withItem(CartItem item) {         // o'zgartirish: yangi nusxa
        List<CartItem> next = new ArrayList<>(items);
        next.add(item);
        return new Cart(List.copyOf(next));
    }
}
// Qoida: holatni o'zgartiradigan metod qiymat qaytarmaydi, qiymat
// qaytaradigan metod holatni o'zgartirmaydi (command-query separation).
```

## 13.27 Niyatni ochib beruvchi interfeyslar (Intention-Revealing Interfaces)

**Tavsif:** Sinf, metod va parametr nomlari implementatsiyani emas, maqsadni - ya'ni domen ekspertlari tilidagi niyatni - aytib turishi kerak. `order.setStatus(3)` o'rniga `order.confirm()`, `repo.findByFlagTrue()` o'rniga `repo.findActiveSubscriptions()` yoziladi. Shunda kodni o'qigan injener metod ichiga kirmasdan uning nima qilishini tushunadi va Ubiquitous Language kodda saqlanadi. Bu pattern Evans ning 10-bobida INTENTION REVEALING INTERFACES nomi bilan beriladi va test nomlari, exception nomlari hamda hodisa nomlariga ham taalluqli.

**Spring'da qayerda uchraydi:** Spring Data derived query metodlari (`findByCustomerIdAndStatus`) yoki `@Query` bilan nomlangan maxsus metodlar; `@NamedQuery` va `@Query(name = ...)`. Domen rollarini aniq ko'rsatish uchun jMolecules annotatsiyalari (`org.jmolecules.ddd.annotation.AggregateRoot`, `@ValueObject`, `@Repository`, `@Factory`, `@Service`) - ular kodni o'qishni ham, ArchUnit/Spring Modulith tekshiruvlarini ham osonlashtiradi. Application servis metodlari nomlari (`placeOrder`, `cancelReservation`) va hodisa sinflari (`OrderPlaced`, `PaymentFailed`) - Spring Modulith `@ApplicationModuleListener` bilan shu nomlar bo'ylab hujjatlashtiriladi (`spring-modulith-docs` Documenter).

**Qo'llanish keyslari:**
- `AccountService.closeAccount(accountId, reason)` - `update(account)` kabi umumiy metod o'rniga.
- `Invoice.markAsOverdue()` metodi `setState("OVERDUE")` ni almashtiradi.
- `InsufficientFundsException` nomi `IllegalStateException`dan ko'ra ko'proq ma'lumot beradi.
- REST qatlamida `POST /orders/{id}/cancellation` kabi niyatga asoslangan endpoint'lar.
- `@KafkaListener` handler nomi `onPaymentCaptured` bo'lib, hodisa nomi bilan bir xil atamada bo'ladi.

**Ehtiyot bo'ling:** Faqat getter/setter'ni qayta nomlash bilan cheklanib qolsangiz, anemik model o'zgarmaydi - niyat bilan birga xatti-harakat ham domen obyektiga ko'chishi kerak. Nomlar domen ekspertlari atamasidan uzoqlashsa (injener o'ylab topgan "chiroyli" nom) pattern teskari ishlaydi: tilni ekspertlar bilan tasdiqlang.

```java
// Niyat nomdan ko'rinadi, implementatsiyadan emas
// Yomon: nima qilayotgani noma'lum
order.setStatus(OrderStatus.CANCELLED);
order.setCancelReason(reason);
order.setCancelledAt(Instant.now());

// Yaxshi: bitta niyat, bitta chaqiruv, qoida ichda
order.cancel(reason);

public class Order {
    public void cancel(CancelReason reason) {
        if (status != OrderStatus.NEW) throw new OrderNotCancellableException(status);
        this.status = OrderStatus.CANCELLED;
        this.cancelReason = reason;
        this.cancelledAt = clock.instant();
    }
}
// Setter'lar to'plami chaqiruvchini qoidani bilishga majbur qiladi
```

## 13.28 Amallarning yopiqligi (Closure of Operations)

**Tavsif:** Agar amal argument sifatida qabul qilgan va natija sifatida qaytargan tur bir xil bo'lsa, amal shu tur ustida "yopiq" deyiladi: `Money.add(Money) -> Money`, `Specification.and(Specification) -> Specification`. Bunday amallar yangi tushuncha kiritmaydi, shuning uchun interfeys soddalashadi va amallarni cheksiz zanjirlash hamda kombinatsiyalash mumkin bo'ladi. Evans 10-bobda bu patternni CLOSURE OF OPERATIONS nomi bilan beradi va u ko'pincha value object'lar ustida tabiiy chiqadi. Yopiqlikni qisman ham qo'llash mumkin - masalan, argument boshqa tur, natija esa o'sha turda bo'lsa (`Money.multiply(BigDecimal) -> Money`).

**Spring'da qayerda uchraydi:** Spring Data JPA `Specification` (`where`, `and`, `or`, `not`) va Querydsl `BooleanExpression` - klassik yopiq amallar. `java.util.function.Function.andThen/compose`, `Predicate.and/or`, `Comparator.thenComparing`; `java.time` turlari (`Duration.plus`, `LocalDate.plusMonths`); `MonetaryAmount` (Moneta) arifmetikasi. Spring Security'da `AuthorizationManager` kombinatsiyalari, Spring Integration/`Flux`da operatorlar zanjiri ham shu uslubda tuzilgan.

**Qo'llanish keyslari:**
- `DateRange.intersect(other)` va `DateRange.union(other)` - natija ham `DateRange`.
- `Money` arifmetikasi: narx + yetkazib berish + soliq, hammasi `Money` turida.
- Qayta ishlatiladigan `Specification` bloklaridan dinamik filtr yig'ish (admin qidiruv ekrani).
- `DiscountPolicy.andThen(otherPolicy)` orqali chegirma qoidalarini kompozitsiya qilish.
- `Quantity.plus/minus` bilan ombor hisob-kitoblarini o'lchov birligi xavfsiz holda bajarish.

**Ehtiyot bo'ling:** Yopiqlikni sun'iy ravishda majburlash xato - turlar haqiqatan bir xil ma'noda bo'lmasa (`Money` + `Percentage`), bu modelni chalg'itadi. Shuningdek yopiq amallar immutable'likka tayanadi: ichki holatni o'zgartirib, `this` qaytarsangiz, zanjirlash kutilmagan natija beradi.

```java
// Closure of operations: amal o'z turi ichida qoladi
public record Money(BigDecimal amount, Currency currency) {
    public Money plus(Money other)  { return new Money(amount.add(other.amount), currency); }
    public Money minus(Money other) { return new Money(amount.subtract(other.amount), currency); }
    public Money times(int n)       { return new Money(amount.multiply(valueOf(n)), currency); }
}

// Natija har doim Money: shuning uchun zanjir tabiiy o'qiladi
Money total = price.times(qty).plus(shipping).minus(discount);
// Agar `plus` BigDecimal qaytarsa, chaqiruvchi har qadamda turni
// qayta o'rashga majbur bo'ladi va valyuta tekshiruvi yo'qoladi.
```

## 13.29 Mustaqil sinflar (Standalone Classes)

**Tavsif:** Har bir qo'shimcha bog'liqlik sinfni tushunish uchun kerakli "aqliy yuk"ni oshiradi; shuning uchun eng muhim va murakkab mantiqni iloji boricha kam bog'liqlikka ega, hatto umuman mustaqil sinflarga ajratish tavsiya etiladi. Ideal holda bunday sinf faqat til va standart kutubxona turlariga tayanadi, framework yoki ma'lumotlar bazasi haqida hech narsa bilmaydi. Natijada u mustaqil o'qiladi, oson test qilinadi va boshqa kontekstlarda qayta ishlatiladi. Evans 10-bobda bu patternni STANDALONE CLASSES nomi bilan beradi va asosiy o'lchov sifatida sinfni tushunish uchun kerakli bog'liqliklar sonini oladi. Amalda u Dependency Inversion bilan birga ishlaydi: infratuzilma domenga qaraydi, teskarisi emas.

**Spring'da qayerda uchraydi:** Domen sinflarini `spring-context`siz alohida Maven/Gradle modulda saqlash va `@Service`/`@Autowired`ni application qatlamiga qoldirish; konstruktor injection (`final` maydonlar) framework annotatsiyalariga ehtiyojni kamaytiradi. Arxitektura qoidalarini mashinada tekshirish uchun ArchUnit (`noClasses().that().resideInAPackage("..domain..").should().dependOnClassesThat().resideInAPackage("org.springframework..")`) va Spring Modulith `ApplicationModules.of(...).verify()`; JPMS `module-info.java` ham chegarani qattiq qiladi. jMolecules + `jmolecules-spring`/`jmolecules-bytebuddy` esa toza domen sinflarini build vaqtida Spring Data'ga moslashtirishga imkon beradi.

**Qo'llanish keyslari:**
- Tarif hisoblash engine'ini `@Component`siz, faqat POJO sifatida yozib, millionlab parametr kombinatsiyasini unit test qilish.
- Soliq qoidalari modulini alohida jar qilib, batch job va REST servisda bir xil ishlatish.
- Value object'larni (`Money`, `Iban`, `Quantity`) hech qanday JPA annotatsiyasisiz saqlab, mapping'ni `AttributeConverter`ga chiqarish.
- ArchUnit testi bilan domen paketidan `jakarta.persistence`ga bog'liqlikni taqiqlash.
- Reja hisoblash algoritmini alohida sinfga ajratib, uni fuzz/property-based test bilan tekshirish.

**Ehtiyot bo'ling:** "Nol bog'liqlik" dogma emas: JPA'ni domenga umuman kirtmaslik uchun qo'shimcha mapping qatlami yozish kichik loyihada ortiqcha xarajat bo'lib chiqadi - narx/foyda nisbatini o'lchang. Shuningdek sinfni ajratish uchun uni anemik qilib qo'ymang: mustaqillik mantiqni olib tashlash hisobiga erishilmasligi kerak.

```java
// Standalone class: bog'liqliksiz, shuning uchun o'qilishi va testi oson
public final class Percent {                  // hech narsa import qilmaydi
    private final BigDecimal value;

    private Percent(BigDecimal value) {
        if (value.signum() < 0) throw new IllegalArgumentException("manfiy foiz");
        this.value = value;
    }

    public static Percent of(String v) { return new Percent(new BigDecimal(v)); }
    public BigDecimal applyTo(BigDecimal base) {
        return base.multiply(value).divide(new BigDecimal("100"), 2, RoundingMode.HALF_UP);
    }
}
// Bu sinfni tushunish uchun boshqa hech narsani o'qish kerak emas:
// kognitiv yuk minimal. Domen yadrosi shunday sinflardan qurilishi kerak.
```

## 13.30 Egiluvchan dizayn (Supple Design)

**Tavsif:** Supple Design - Evans kitobining 10-bobidagi umumlashtiruvchi maqsad: model shunday yozilsinki, undan foydalanuvchi injener o'zgartirish kiritishdan qo'rqmasin va yangi talablar modelga "qulf"ga kalit kabi joylashsin. U alohida pattern emas, balki bir nechta texnikaning yig'indisi; Evans 10-bobda ularni shu tartibda beradi: INTENTION REVEALING INTERFACES, SIDE-EFFECT-FREE FUNCTIONS, ASSERTIONS, CONCEPTUAL CONTOURS, STANDALONE CLASSES, CLOSURE OF OPERATIONS va Declarative Design. Bu ro'yxatning har bir elementi uchun bu bobda alohida bo'lim bor. Asosiy mezoni - refactoring qilish qo'rqinchli emas, balki arzon bo'lishi; bu esa chuqur modelni izlash (deep model) jarayonining mevasi.

**Spring'da qayerda uchraydi:** Spring ekotizimida bu asosan loyiha strukturasi va disiplina sifatida namoyon bo'ladi: moduliy paketlar + Spring Modulith `ApplicationModules.verify()` va `Documenter`, ArchUnit qoidalari, konstruktor injection, `record`-asosidagi immutable value object'lar. Deklarativ uslub uchun Spring'ning o'z misollari: Spring Data `Specification`/derived query'lar, Spring Security DSL (`HttpSecurity` lambda konfiguratsiyasi), Spring Integration DSL - ularni domen tilidagi o'z DSL'laringiz uchun namuna qilib olish mumkin. Assertions uchun `Assert`, Bean Validation va test tomonida AssertJ (`spring-boot-starter-test` ichida) ishlatiladi.

**Qo'llanish keyslari:**
- Chegirma qoidalari uchun kichik domen DSL yozib, yangi aksiyani bir necha qator kod bilan qo'shish.
- Buyurtma holati o'tishlarini aniq nomlangan metodlar va assertion'lar bilan modellash, `if`lar to'dasi o'rniga.
- Modulith verification testini CI'ga qo'yib, moduldan modulga ruxsatsiz bog'liqlikni erta ushlash.
- Murakkab tarif mantiqini standalone, yon ta'sirsiz sinflarga ajratib, uni ishonchli refactor qilish.
- Domen hodisalari nomlarini ekspert tiliga moslab, yangi integratsiyani hodisalarga ulash orqali qo'shish.

**Ehtiyot bo'ling:** Supple design barcha kodga emas, eng murakkab va eng tez o'zgaruvchan core domain'ga yo'naltirilishi kerak - CRUD-ga yaqin supporting subdomain'ni shu darajada mukammallashtirish resurs isrofi. Shuningdek "chiroyli DSL" sifatida yozilgan, lekin ekspertlar atamasidan uzoq abstraksiyalar modelni egiluvchan emas, aksincha qotib qolgan qiladi.

```java
// Supple design: model o'zgarishga qarshilik qilmaydi
public final class DateRange {
    private final LocalDate from, to;

    public boolean overlaps(DateRange other) { /* ... */ return false; }
    public DateRange intersect(DateRange other) { /* ... */ return this; }
    public boolean contains(LocalDate day) { /* ... */ return false; }
}

// Shu uch amal bilan yangi talablar kod yozmasdan ifodalanadi:
//   tariflar kesishmasligi, chegirma davri, hisobot oynasi
// Belgilari: niyatni ochib beruvchi nomlar, yon ta'sirsiz funksiyalar,
// yopiq amallar, mustaqil sinflar va aniq invariantlar. Shundan keyin
// yangi talab "qanday qo'shaman" emas, "qaysi amallar bilan ifodalanadi"
// savoliga aylanadi.
```

## 13.31 Anemik domen modeli (anti) (Anemic Domain Model (anti))

**Tavsif:** Anemik model - domen obyektlari faqat maydon, getter va setter'dan iborat bo'lib, barcha biznes mantiq "service" sinflariga ko'chib ketgan holat. Bunda obyektga yo'naltirilgan dizaynning asosiy foydasi - ma'lumot va xatti-harakatni birga saqlash - yo'qoladi: invariantlar tarqalib ketadi, bir xil qoida bir necha servisda takrorlanadi va noto'g'ri holatni yaratish oson bo'ladi. Natijada model emas, oddiy ma'lumot tashuvchi (data holder) qoladi va murakkablik o'sgan sari servis sinflari procedural "god class"larga aylanadi. Shuni ta'kidlash kerak: oddiy CRUD ilovada bu ongli, maqbul tanlov bo'lishi mumkin - anti-pattern bo'lishi faqat murakkab domenda yuzaga keladi. Khononov 5-bobda atamaning o'ziga e'tiroz bildiradi: Active Record patterni ham "anemik domen modeli antipatterni" deb ataladi, lekin bu shunchaki asbob va oddiy mantiq uchun to'g'ri tanlov bo'lishi mumkin; "anemik" va "antipattern" so'zlarining salbiy ohangi qarorni buzadi.

**Spring'da qayerda uchraydi:** Tipik ko'rinishi: `@Entity` sinf Lombok `@Data`/`@Setter` bilan to'liq ochiq, yonida `@Service` sinf `OrderService.updateOrder(OrderDto)` metodida barcha `if`lar bilan. Davolash yo'llari: entity'da public setter'larni olib tashlash va niyatli metodlar qoldirish, `@Embeddable` value object'lar, JPA uchun `protected` no-arg konstruktor + factory metodlar, agregat ichidagi kolleksiyalarni `Collections.unmodifiableList` bilan qaytarish, hodisalar uchun `AbstractAggregateRoot`. Spring Modulith va jMolecules (`@AggregateRoot`, `@ValueObject`) rollarni aniq qilib, mantiqni to'g'ri joyga qo'yishga undaydi; `@Transactional` esa domen emas, application qatlamida turadi.

**Qo'llanish keyslari:**
- Legacy `OrderService` ichidagi status o'tish mantiqini `Order.confirm()`/`Order.cancel()` metodlariga ko'chirish.
- `@Data` annotatsiyasini olib tashlab, entity'ga faqat kerakli mutator metodlarni qoldirish.
- Pul va manzil maydonlarini `Money`/`Address` `@Embeddable` value object'lariga yig'ish.
- Takrorlangan validatsiyani uchta servisdan bitta agregat metodiga birlashtirish.
- CRUD-ga yaqin supporting modulni ataylab anemik qoldirib, core domain'ni boyitishga kuch yo'naltirish.

**Ehtiyot bo'ling:** Teskari chetga chiqmang: agregatga repository, HTTP client yoki tashqi servis inyeksiya qilib, uni "boy" qilishga urinish bog'liqliklarni domenga tortadi - bunday mantiq application servisga yoki domain service'ga tegishli. Shuningdek DTO va API modellari ataylab anemik bo'ladi; anemiklik muammosi faqat domen modeliga tegishli.

```java
// Anemik: qoida servisda, obyekt faqat ma'lumot tashiydi
class Order { private OrderStatus status; /* getter + setter */ }

class OrderService {
    void cancel(Order o) {
        if (o.getStatus() != OrderStatus.NEW) throw new IllegalStateException();
        o.setStatus(OrderStatus.CANCELLED);     // qoida tashqarida
    }
    void refund(Order o) {
        if (o.getStatus() != OrderStatus.NEW) throw new IllegalStateException();  // takror
    }
}
// Belgisi: domen sinflarida faqat getter va setter, barcha `if` servisda,
// va bir xil tekshiruv bir necha joyda takrorlanadi.
// Davolash: qoidani ma'lumot yoniga ko'chirish (13.15 va 13.24).
```

## 13.32 Event Storming (texnika) (Event Storming (technique))

**Tavsif:** Event Storming - Alberto Brandolini taklif qilgan ustaxona (workshop) texnikasi: domen ekspertlari va injenerlar katta devorga vaqt bo'yicha tartiblangan domen hodisalarini yopishqoq qog'ozlarda joylab, biznes jarayonini birgalikda kashf qiladi. Khononov 12-bobda jarayon o'nta qadam sifatida beriladi (tartibsiz izlanish, vaqt chizig'i, og'riq nuqtalari, burilish hodisalari, buyruqlar, siyosatlar, read model'lar, tashqi tizimlar, agregatlar, bounded context'lar) va amalda ikki bosqichda o'tkaziladi: avval 1-4 qadamlar bilan butun biznes manzarasi, keyin har bir biznes jarayoni uchun to'liq sessiya. Rang konvensiyasi shu bobda yozilgan: to'q sariq - domen hodisasi, och ko'k - buyruq, kichik sariq - aktor, katta sariq - agregat, binafsha - siyosat (hodisani buyruqqa bog'laydi), yashil - read model, pushti - tashqi tizim, burilgan (romb) pushti - og'riq nuqtasi. Natija sifatida Ubiquitous Language, bounded context chegaralari va agregat nomzodlari qo'lga kiritiladi; Khononov ning ta'kidi shu - asosiy qiymat chiqqan diagrammada emas, muhokamada.

**Spring'da qayerda uchraydi:** Bu kod pattern'i emas, lekin natijasi Spring loyihasiga bevosita ko'chadi: to'q sariq hodisalar - `OrderPlaced` kabi domen hodisa sinflari (`ApplicationEventPublisher`, `@DomainEvents`, `@ApplicationModuleListener`); och ko'k command'lar - application servis metodlari yoki `@PostMapping` endpoint'lari; katta sariq agregatlar - `@Entity` aggregate root'lar va ularning repository'lari; binafsha policy'lar - `@TransactionalEventListener`/`@KafkaListener` handler'lari; yashil read model'lar - CQRS projection jadvallari va `@Query` proyeksiyalari. Bounded context chegaralari Spring Modulith modullariga (`@ApplicationModule`, `package-info.java`) yoki alohida servislarga aylanadi, `Documenter` esa bu strukturani diagramma qilib beradi.

**Qo'llanish keyslari:**
- Yangi mahsulot domenini noldan o'rganish va birinchi bounded context xaritasini chizish.
- Legacy monolitni bo'lishdan oldin modul chegaralarini hodisalar oqimi bo'yicha aniqlash.
- Jamoalar o'rtasida integratsiya shartnomalarini (qanday hodisa kimga kerak) kelishish.
- Murakkab jarayonning "hot spot"larini ochib, biznes bilan noaniq qoidalarni hal qilish.
- Onboarding: yangi senior injenerga tizim mantiqini bir kunda ko'rsatish.

**Ehtiyot bo'ling:** Ustaxonada haqiqiy domen ekspertlari qatnashmasa, natija injenerlarning taxminlari to'plamiga aylanadi - texnikaning qiymati aynan birgalikdagi muhokamada. Shuningdek Big Picture natijasini to'g'ridan-to'g'ri jadval yoki sinf diagrammasiga ko'chirmang: bu kashf qilish vositasi, dizayn esa Design Level va keyingi modellashtirishda yetiladi.

```text
Event storming: hodisalar devorga yopishtiriladi, keyin guruhlanadi

  1. Domen hodisalari (to'q sariq): o'tgan zamonda
       OrderPlaced, StockReserved, PaymentCaptured, OrderShipped
  2. Og'riq nuqtalari (burilgan romb, pushti): jarayondagi muammo joyi
  3. Buyruqlar (och ko'k): hodisani keltirib chiqaradi
       PlaceOrder, ReserveStock, CapturePayment
  4. Aktorlar (kichik sariq): buyruqni kim chaqiradi
       Mijoz, Ombor xodimi, To'lov provayderi
  5. Siyosatlar (binafsha): "har qachon X bo'lsa, Y qilinadi"
       OrderPlaced -> ReserveStock
  6. Read model'lar (yashil) va tashqi tizimlar (pushti)
  7. Agregatlar (katta sariq): buyruqni qabul qiladi va invariantni saqlaydi
       Order, Reservation, Payment
  8. Chegaralar: hodisalar zich guruhlangan joyda bounded context chizig'i

Natija: hodisa ro'yxati, agregat ro'yxati va kontekst xaritasining
birinchi qoralamasi. Bu kod emas, lekin keyingi butun dizayn shundan chiqadi.
```

## 13.33 Spring Data bilan domen hodisalari (Domain Events with Spring Data: AbstractAggregateRoot, @DomainEvents)

**Tavsif:** Agregat o'zida ro'y bergan muhim o'zgarishlarni hodisa sifatida ro'yxatga oladi, hodisalar esa agregat saqlanganda avtomatik publish qilinadi - shunday qilib domen kodi `ApplicationEventPublisher`ga bog'lanmaydi. Spring Data buni `@DomainEvents` (publish qilinadigan kolleksiyani qaytaruvchi metod) va `@AfterDomainEventPublication` (ro'yxatni tozalovchi metod) annotatsiyalari bilan qo'llaydi; tayyor baza sinfi - `org.springframework.data.domain.AbstractAggregateRoot<A>` va uning `registerEvent(...)` metodi. Repository proxy `save`/`delete` chaqirig'ida bu metodlarni topib, hodisalarni `ApplicationEventPublisher` orqali yuboradi.

**Spring'da qayerda uchraydi:** `AbstractAggregateRoot` Spring Data Commons'da (`spring-data-commons`) joylashgan va JPA, MongoDB, JDBC modullarida ishlaydi; mexanizmni `EventPublishingRepositoryProxyPostProcessor` ta'minlaydi. Hodisa iste'molchilari - `@EventListener` yoki `@TransactionalEventListener(phase = AFTER_COMMIT)`; Spring Modulith'da `@ApplicationModuleListener` + Event Publication Registry ishonchli yetkazib berishni qo'shadi. Agregat JPA entity bo'lsa, hodisalar ro'yxati `@Transient` maydonda turadi.

```java
@Entity
class Order extends AbstractAggregateRoot<Order> {
    @Id @GeneratedValue private Long id;
    private OrderStatus status = OrderStatus.NEW;

    void confirm() {
        if (status != OrderStatus.NEW) throw new IllegalStateException("already handled");
        this.status = OrderStatus.CONFIRMED;
        registerEvent(new OrderConfirmed(id));   // save() paytida publish bo'ladi
    }
}
```

**Qo'llanish keyslari:**
- `OrderConfirmed` hodisasi bilan hisob-faktura modulini ishga tushirish.
- `CustomerRenamed` hodisasidan keyin read model/projection'ni yangilash.
- Audit log yozuvlarini agregat metodlariga aralashtirmasdan, listener'da yig'ish.
- Spring Modulith registry orqali hodisani Kafka'ga outbox bilan uzatish.
- Email yoki push xabarni faqat tranzaksiya commit bo'lgandan keyin yuborish.

**Ehtiyot bo'ling:** Hodisalar `save()` chaqirig'i ichida, ya'ni tranzaksiya hali commit bo'lmasdan publish qilinadi - tashqi ta'sirlar uchun albatta `AFTER_COMMIT` fazasini ishlatmasa, rollback bo'lgan ishni "sodir bo'lgan" deb e'lon qilib qo'yasiz. Shuningdek dirty checking bilan o'zgargan, lekin `save()` chaqirilmagan entity hodisalarini yubormaydi (JPQL bulk `update`/`delete` ham chetlab o'tadi), `@AfterDomainEventPublication` ro'yxatni tozalamasa esa hodisa takror publish bo'lishi mumkin.

## 13.34 DDD qatlamli arxitekturasi (DDD Layered Architecture)

**Tavsif:** Evans 4-bobda (LAYERED ARCHITECTURE) to'rt qatlamni sanaydi: User Interface, Application, Domain va Infrastructure; bog'liqliklar yuqoridan pastga yo'naladi va asosiy maqsad domen qatlamini ajratish. Bog'liqlik yo'nalishini teskari qilish (infratuzilma domen e'lon qilgan interfeysni bajaradi) Evans ning o'z sxemasi emas, Dependency Inversion bilan kelgan keyingi qadam: Khononov 8-bobda bu Ports & Adapters nomi bilan va DIP bo'limi ostida beriladi. Application qatlami use-case'ni orkestratsiya qiladi (tranzaksiya, xavfsizlik, DTO mapping), biznes qoidalari domenda turadi, infrastruktura esa domen e'lon qilgan port'larni (repository interfeyslari) implement qiladi - ya'ni Dependency Inversion. Zamonaviy variantlari Hexagonal (Ports & Adapters), Onion va Clean Architecture bo'lib, maqsad bir xil: domen yadrosini framework va texnologiyadan ajratish.

**Spring'da qayerda uchraydi:** Amalda `web`/`api` (`@RestController`, `@ControllerAdvice`), `application` (`@Service`, `@Transactional`, use-case sinflari), `domain` (entity, value object, repository interfeys, domain service) va `infrastructure` (`@Repository` implementatsiyalari, Spring Data interfeyslari, `RestClient`/`WebClient` adapterlari, `@KafkaListener`) paketlari yoki Gradle/Maven modullari sifatida tuziladi. Qoidalarni majburlash uchun ArchUnit `layeredArchitecture()` qoidalari, Spring Modulith `ApplicationModules.verify()` va `@ApplicationModule(allowedDependencies = ...)`, jMolecules `jmolecules-architecture-layered` (`@DomainLayer`, `@ApplicationLayer`, `@InfrastructureLayer`) ishlatiladi. Spring Boot 3.x/4.x'da konstruktor injection va `@Configuration` sinflarini infrastruktura qatlamiga yig'ish domen tozaligini saqlashga yordam beradi.

**Qo'llanish keyslari:**
- Repository interfeysini `domain` paketida saqlab, Spring Data implementatsiyasini `infrastructure`da qoldirish.
- `@Transactional`ni faqat application servislarda qo'llab, controller va domenni tranzaksiyadan xoli qilish.
- ArchUnit testi bilan `domain` paketidan `jakarta.servlet` yoki `org.springframework.web`ga bog'liqlikni taqiqlash.
- To'lov provayderi uchun port interfeysi va ikki adapter (real + sandbox stub) yozish.
- Monolitni modullarga ajratishda har bir modul ichida bir xil qatlam strukturasini takrorlash.

**Ehtiyot bo'ling:** Qatlamlarni "texnik" ajratish (hamma controller bitta paketda, hamma service boshqasida) modullikni bermaydi - avval bounded context/modul bo'yicha, keyin qatlam bo'yicha bo'lish ancha barqaror. Kichik CRUD servisda to'liq port/adapter mapping qatlamlari ortiqcha ko'p kod keltirib chiqaradi: qatlam sonini domen murakkabligiga moslab tanlang.

```text
com.example.sales
  domain/            Order, Money, Orders (interfeys)   -- hech narsaga bog'liq emas
  application/       PlaceOrderUseCase                  -- domain ga bog'liq
  infrastructure/    JpaOrders, PspPaymentAdapter       -- application portlarini bajaradi
  presentation/      OrderController                    -- application ni chaqiradi

ArchUnit bilan majburlash:
  noClasses().that().resideInAPackage("..domain..")
    .should().dependOnClassesThat()
    .resideInAnyPackage("..application..", "..infrastructure..", "..presentation..")

Klassik qatlamli arxitekturadan farqi: domen pastda emas, markazda.
Repository interfeysi domenda, implementatsiyasi infratuzilmada turadi,
shuning uchun bog'liqlik yo'nalishi teskari (dependency inversion).
```

## 13.35 Pul (Money (Value Object specialization))

**Tavsif:** Money - bu miqdor (amount) va valyuta (currency) juftligini bitta o'zgarmas Value Object sifatida birlashtiradigan maxsus pattern, chunki pulni oddiy `double` yoki yalang'och `BigDecimal` bilan ifodalash moliyaviy domenda eng ko'p uchraydigan xatolik manbai. `double` ikkilik suzuvchi nuqta tufayli yaxlitlash xatolarini keltiradi, yalang'och `BigDecimal` esa valyuta ma'lumotini yo'qotadi va USD bilan UZS'ni beg'araz qo'shib yuborish imkonini beradi. Money sinfi arifmetik amallarni (`add`, `subtract`, `multiply`, `allocate`) o'zida saqlaydi, har bir amalda valyuta mosligini tekshiradi va yaxlitlash qoidasini (`RoundingMode`, scale) markazlashtiradi. Shuningdek u taqsimlash muammosini hal qiladi: 100.00 ni 3 ga bo'lganda tiyinlar yo'qolmasligi uchun qoldiqni determinativ tarzda ulushlar orasida tarqatadi. Money mustaqil pattern sifatida Evans kitobida emas, Fowler PoEAA 18-bobida (Base Patterns, Money) turadi; aynan shu yerda valyutani miqdor bilan birga saqlash talabi, yaxlitlashda tiyin yo'qolishi muammosi va `allocate` amali tavsiflanadi.

**Spring'da qayerda uchraydi:** Spring Framework'da tayyor `Money` sinfi YO'Q - bu domen darajasidagi pattern va uni o'zingiz yozasiz yoki standart kutubxonalardan olasiz: JSR-354 `javax.money.MonetaryAmount` / `javax.money.CurrencyUnit` interfeyslari va uning Moneta referens implementatsiyasi (`org.javamoney.moneta.Money`, `org.javamoney.moneta.FastMoney`), yoki Joda-Money (`org.joda.money.Money`, `org.joda.money.CurrencyUnit`). JDK darajasida asos - `java.math.BigDecimal`, `java.math.RoundingMode` va `java.util.Currency`; Java 17+ `record` esa o'zgarmas Money'ni yozishning eng qisqa yo'li. Spring Data JPA'da Money odatda `@Embeddable` Value Object sifatida ikki ustunga (`amount` `DECIMAL(19,4)` va `currency` `CHAR(3)`) map qilinadi, yoki `jakarta.persistence.AttributeConverter` bilan bitta ustunga yoziladi; MongoDB'da esa Spring Data'ning `Converter<Money, Document>` juftligi `MongoCustomConversions` orqali ro'yxatga olinadi. JSON chegarasida Jackson uchun `@JsonSerialize`/`@JsonDeserialize` yoki Moneta'ning `jackson-datatype-money` moduli ishlatiladi, formatlash uchun esa Spring'ning `MessageSource` + `java.text.NumberFormat.getCurrencyInstance(Locale)` yoki `javax.money.format.MonetaryAmountFormat` xizmat qiladi. Spring MVC/WebFlux'da string'dan Money'ga konvertatsiya `org.springframework.core.convert.converter.Converter` yoki `Formatter` ni `WebMvcConfigurer#addFormatters` da registratsiya qilish bilan amalga oshiriladi, validatsiya uchun `@DecimalMin`, `@Digits` va custom `ConstraintValidator` qo'llanadi.

```java
public record Money(BigDecimal amount, Currency currency) {
    public Money {
        amount = amount.setScale(currency.getDefaultFractionDigits(), RoundingMode.HALF_EVEN);
    }
    public Money add(Money other) {
        if (!currency.equals(other.currency))
            throw new IllegalArgumentException("Valyutalar mos emas");
        return new Money(amount.add(other.amount), currency);
    }
}
```

**Qo'llanish keyslari:**
- E-commerce savatchasida mahsulot narxi, chegirma va yetkazib berish narxini qo'shib, umumiy summani tiyin aniqligida hisoblash.
- Bank yoki to'lov tizimida hisobdan hisobga o'tkazmani bajarishda valyuta mosligini kompilyatsiya yoki domen darajasida majburlash.
- Invoice summasini bir nechta pozitsiya yoki bo'lim o'rtasida `allocate` bilan qoldiqsiz taqsimlash (masalan, 100.00 USD → 33.34 / 33.33 / 33.33).
- Ko'p valyutali SaaS tariflarida narxni foydalanuvchi locale'iga qarab `MonetaryAmountFormat` orqali to'g'ri belgi va ajratgich bilan ko'rsatish.
- Soliq, komissiya yoki foiz hisoblashda yaxlitlash qoidasini (`HALF_EVEN` vs `HALF_UP`) bitta joyda belgilab, butun tizimda bir xil natijaga erishish.

**Ehtiyot bo'ling:** Money'ni hech qachon `double`/`float` ustiga qurmang va `BigDecimal` ni `equals` bilan taqqoslashda ehtiyot bo'ling - `2.0` va `2.00` `equals` bo'yicha teng emas, shuning uchun konstruktorda scale'ni normallashtirib qo'ying va `compareTo` dan foydalanish qoidasini belgilang. Valyuta konvertatsiyasini Money ichiga qurmang: kurs vaqtga bog'liq tashqi ma'lumot, uni alohida `ExchangeRateService`/domen servisiga chiqaring, aks holda Value Object o'zgaruvchan infratuzilmaga bog'lanib qoladi va test qilinmas holga keladi.

## 13.36 Modelga asoslangan dizayn (Model-Driven Design)

**Tavsif:** Evans ba'zi jarayonlarda uchraydigan ikki model holatini rad etadi: bir tomondan "analiz modeli" (domenni tushunish uchun, implementatsiya tashvishlarisiz), ikkinchi tomondan undan ajralgan dizayn. Model-Driven Design shu ikkiligini olib tashlaydi: bitta model ham domenni tushuntiradi, ham kodda ishlaydi. Evans ning asosiy da'vosi shundaki, dizayn (yoki uning markaziy qismi) modelga mos kelmasa, model qiymatsiz va dasturning to'g'riligi shubhali bo'ladi; model va dizayn orasidagi murakkab mapping esa amalda saqlab turilmaydi, chunki dizayn o'zgargan sari u eskiradi. Buning oqibati Evans aytgan "o'limga olib boruvchi bo'linish": analiz paytidagi tushuncha dizaynga o'tmaydi, dizayn paytidagi tushuncha analizga qaytmaydi. Shuning uchun modelni kodning o'zida ifodalash kerak: paket, sinf va metod nomlari modeldagi tushunchalar bilan bir xil bo'ladi va modelni o'zgartirish kodni o'zgartirish demakdir.

**Spring'da qayerda uchraydi:** Amalda bu domen paketini framework detallaridan tozalashda ko'rinadi: `com.example.sales.domain` ichida `jakarta.persistence`, Jackson va Spring web importlari yo'q, mapping esa `infrastructure` paketidagi adapterda bo'ladi. jMolecules annotatsiyalari (`@AggregateRoot`, `@ValueObject`, `@DomainService`) modeldagi rolni kodda nomlaydi, `jmolecules-archunit` esa buzilishni test sifatida ushlaydi. [Modulli monolit va Spring Modulith](12-arxitektura-uslublari.md#126-modulli-monolit-modular-monolith--spring-modulith) yondashuvi modelni modul chegaralari bilan birga saqlaydi.

**Qo'llanish keyslari:**
- UML diagrammada qolib ketgan "analiz modeli"ni tashlab, uning tushunchalarini domen sinflariga ko'chirish.
- `OrderDto` va `Order` o'rtasidagi qo'lda yozilgan mapping kodini adapterga yig'ib, domenni DTO shaklidan ozod qilish.
- Baza sxemasidan avtomatik generatsiya qilingan entity'lar ustiga domen modeli qurish va ularni faqat persistence adapteri ichida qoldirish.
- Yangi talab kelganda avval modelni (nomlar va munosabatlar) o'zgartirib, keyin kodni unga moslashtirish tartibini joriy qilish.
- ArchUnit testi bilan domen paketidan infratuzilma paketiga bog'liqlikni taqiqlash.

**Ehtiyot bo'ling:** "Model" so'zini baza sxemasi yoki ORM entity'lari bilan tenglashtirish eng tez-tez uchraydigan xato: jadval tuzilishi domen tushunchasi emas. Teskari chetga chiqish ham bor - modelni toza saqlash uchun ikki parallel sinf iyerarxiyasi (domen va persistence) yozib, ular orasida qo'lda mapping ushlab turish: bu Evans ogohlantirgan "murakkab mapping" ning aynan o'zi va kichik domenda o'zini oqlamaydi.

```java
// Model kodda ko'rinadi: nom, rol va munosabat modeldan olingan
package com.example.shipping.domain;   // framework importlari yo'q

public final class Cargo {                       // Aggregate root
    private final TrackingId trackingId;
    private RouteSpecification routeSpecification;
    private Itinerary itinerary;

    public void assignToRoute(Itinerary candidate) {
        if (!routeSpecification.isSatisfiedBy(candidate)) {
            throw new IllegalArgumentException("itinerary route spetsifikatsiyasiga mos emas");
        }
        this.itinerary = candidate;
    }
}
// Modeldagi "itinerary route spetsifikatsiyasini qanoatlantiradi" qoidasi
// kodda aynan shu nomlar bilan turadi, izohda emas.
```

## 13.37 Qo'li ishda bo'lgan modelchilar (Hands-On Modelers)

**Tavsif:** Evans 3-bobda ishlab chiqarish (manufacturing) metaforasini tanqid qiladi: "malakali injener loyihalaydi, kam malakali ishchi yig'adi" taqsimoti dasturda ishlamaydi, chunki dasturlashning hammasi dizayn. Modelchi implementatsiyadan uzilganda u implementatsiya cheklovlarini his qilishni yo'qotadi va modeli amaliy bo'lmaydi; kod yozuvchilar esa model uchun javobgarlikni sezmaganda model dasturga aloqasiz qoladi. Evans buni o'z tajribasi bilan ko'rsatadi: model yaxshi edi, lekin modelning niyati topshiriq paytida yo'qoldi va texnologik platformadagi samarasizlik haqidagi fikr unga oylar o'tib yetib keldi. Xulosa qat'iy: dasturchilar modelchi, kimga yoqsa yoqmasa; shuning uchun loyihani dasturchilar yaxshi modellashtiradigan tarzda tashkil qilish kerak. Bu rollarni butunlay yo'q qilishni talab qilmaydi, faqat modellashtirish va implementatsiyani ikki odamga bo'lishni taqiqlaydi.

**Spring'da qayerda uchraydi:** Tashkiliy pattern bo'lgani uchun u kodda bilvosita ko'rinadi: model qoidalarini hujjat emas, test himoya qiladi. ArchUnit va `ApplicationModules.verify()` testlarini modelni loyihalagan odamlar yozadi va ular CI'da ishlaydi; Spring Modulith `Documenter` modul diagrammasini kodning o'zidan yasaydi, shuning uchun diagramma eskirmaydi. Arxitektura qarori ADR faylida kod repozitoriysida yashaydi, alohida wiki'da emas.

**Qo'llanish keyslari:**
- "Arxitektor" rolidagi odamni haftada bir kun shu modul kodida ishlashga qaytarish.
- Domen modeli bo'yicha qarorni ADR sifatida repozitoriyga yozib, pull request orqali muhokama qilish.
- Modul chegarasi qoidasini wiki sahifasi emas, `ApplicationModules.verify()` testi bilan ifodalash.
- Yangi dasturchini onboarding qilishda model diagrammasini kod generatsiyasidan olish, qo'lda chizilgan rasmdan emas.
- Event storming natijasini o'sha kuni kod skeletiga (paket va sinf nomlariga) o'tkazish.

**Ehtiyot bo'ling:** Teskari xato ham bor: hamma bir xil ishni qilsin deb rol ixtisoslashuvini butunlay yo'q qilish. Evans aytganidek, har bir Agile jarayonda rollar bor va tabiiy ixtisoslashuv paydo bo'ladi; muammo faqat modellashtirish va implementatsiyani ajratishda. Shuningdek "modelchi kod yozsin" shiorini tajribali dizaynerni faqat ticket yopishga o'tkazish uchun bahona qilmang: bilim uzatish uchun unga juftlikda ishlash va review vaqti kerak.

```java
// Model qoidasi hujjatda emas, testda yashaydi va uni modelchining o'zi yozadi
@AnalyzeClasses(packages = "com.example.sales")
class DomainModelRulesTest {

    @ArchTest
    static final ArchRule domen_infratuzilmaga_bogliq_bolmasin =
        noClasses().that().resideInAPackage("..domain..")
            .should().dependOnClassesThat()
            .resideInAnyPackage("..infrastructure..", "jakarta.persistence..", "org.springframework.web..");

    @Test
    void modul_chegaralari_buzilmagan() {
        ApplicationModules.of(SalesApplication.class).verify();
    }
}
```

## 13.38 Smart UI (anti-pattern) (Smart UI Anti-Pattern)

**Tavsif:** Smart UI - butun biznes mantiqni foydalanuvchi interfeysiga joylash, ilovani kichik mustaqil ekranlarga bo'lish va relyatsion bazani umumiy ma'lumot ombori sifatida ishlatish. Evans buni 4-bobda ataylab qatlamli arxitekturaning inkori sifatida beradi va "anti-pattern" nomini yarim hazil deb aytadi: oddiy, ma'lumot kiritish va ko'rsatishdan iborat, biznes qoidasi kam bo'lgan loyihada va obyekt modellashtirishda tajribasiz jamoada bu ongli va to'g'ri tanlov. Afzalliklari aniq: tezkor natija, past o'rganish egri chizig'i, ilovalar bir-biridan ajralgani uchun reja aniq, relyatsion baza va vizual asboblar yaxshi ishlaydi. Narxi ham aniq: integratsiya faqat baza orqali bo'ladi, mantiq takrorlanadi, abstraksiya yo'qligi tufayli murakkablik o'sishi bilan tizim refactoring qilinmas holga keladi. Eng muhim xulosa: bu DDD bilan birga yashamaydigan, o'zaro inkor etuvchi yo'l; shuni bilib tanlash kerak.

**Spring'da qayerda uchraydi:** Tipik ko'rinishi: `@Controller` yoki `@RestController` ichida `JdbcTemplate` bilan to'g'ridan-to'g'ri SQL va `if` zanjirlari; Spring Data REST yoki `@RepositoryRestResource` bilan entity'ni to'g'ridan-to'g'ri HTTP ga chiqarish; Thymeleaf shablonida narx hisoblash. Oddiy admin panel, ichki hisobot va bir martalik migratsiya asboblarida bu maqbul. Murakkab domenda esa belgisi shu: bitta biznes qoidasini o'zgartirish uchun bir nechta controller va shablonni tahrirlash kerak bo'ladi.

**Qo'llanish keyslari:**
- Ichki CRUD admin ekranlari uchun ataylab Smart UI tanlab, kuchni core domain'ga yo'naltirish.
- Bir martalik ma'lumot ko'chirish asbobini qatlamsiz, controller ichida yozib tashlash.
- Prototip yoki demo ilovani tez chiqarib, foydalanuvchi talabini aniqlash.
- Supporting subdomain uchun Smart UI qoldirib, uni keyin alohida xizmatga ajratish rejasini yozish.
- Legacy Smart UI modulida biznes qoidasi takrorlanishini sanab, ko'chirish ustuvorligini belgilash.

**Ehtiyot bo'ling:** Eng qimmat xato - Smart UI'ni tanlov emas, standart deb qabul qilish va keyin uning ustiga DDD patternlarini yopishtirishga urinish: natijada ikki yondashuvning narxi qo'shiladi, foydasi esa qo'shilmaydi. Shuningdek "biznes qoidasi kam" bahosini loyiha boshida bir marta qilib qo'yib, qoidalar o'sganda yondashuvni qayta ko'rib chiqmaslik ham tuzoq: Evans ta'kidlaydiki, ambitsiyali loyihalar ham oddiy funksiyalardan boshlanadi, lekin ularning birinchi qadamlari ham model asosida va domen qatlami ajratilgan holda bo'ladi.

```java
// Smart UI: qoida controller ichida, bazaga to'g'ridan-to'g'ri
@RestController
class InvoiceController {
    private final JdbcTemplate jdbc;

    InvoiceController(JdbcTemplate jdbc) { this.jdbc = jdbc; }

    @PostMapping("/invoices/{id}/discount")
    void applyDiscount(@PathVariable long id, @RequestParam int percent) {
        if (percent > 30) throw new IllegalArgumentException("chegirma 30 foizdan oshmaydi");
        jdbc.update("update invoice set discount_percent = ? where id = ?", percent, id);
    }
}
// Oddiy admin ekranida bu maqbul. Murakkab domenda belgisi shu:
// "chegirma 30 foizdan oshmaydi" qoidasi yana uchta controller'da takrorlanadi.
```

## 13.39 Uzluksiz integratsiya (Continuous Integration - model darajasida)

**Tavsif:** Evans 14-bobda bu nomni qurilish quvuri ma'nosida emas, model butunligi ma'nosida ishlatadi: bitta bounded context ustida bir necha odam ishlaganda model parchalanishga moyil bo'ladi va uch-to'rt kishilik jamoada ham bu muammo boshlanadi. Dasturchilar boshqa birov modellagan obyektning niyatini tushunmay o'zgartiradi, yoki tushuncha allaqachon modelda borligini bilmay uni taxminiy tarzda takrorlaydi, yoki bor kodni buzishdan qo'rqib ataylab dublikat yozadi. Evans uzluksiz integratsiyani ikki darajada ko'radi: tushunchalar integratsiyasi (umumiy tilni tinimsiz muhokamada sinash) va implementatsiya integratsiyasi (takrorlanadigan merge va build, avtomatik testlar, integratsiya qilinmagan o'zgarishning yashash muddatiga kichik yuqori chegara). Oxirgi muhim shart: bu faqat bitta bounded context ichida zarur, qo'shni kontekstlar bilan munosabat boshqa tezlikda hal qilinadi.

**Spring'da qayerda uchraydi:** Implementatsiya tomoni odatdagi quvurda: Maven yoki Gradle build, `./gradlew test` va modul chegarasi testlari. Model tomoni uchun aynan shu testlar muhim: `ApplicationModules.verify()`, [arxitektura testlari](23-testing-patternlari.md#2321-arxitektura-testlari-architecture-tests---archunit-spring-modulith-verify) va nomlash qoidalari takroriy yoki chetga chiqqan tushunchani erta ko'rsatadi. Integratsiya qilinmagan o'zgarish muddatini qisqartirish uchun [trunk-based development](22-deployment-va-operatsion-patternlar.md#2231-trunk-based-development-va-reliz-poyezdlari-trunk-based-development--release-trains) ishlatiladi.

**Qo'llanish keyslari:**
- Bitta bounded context ustida ishlaydigan jamoada uzun feature branch'larni taqiqlab, kunlik merge joriy qilish.
- Umumiy til lug'atini review'da tekshirish punkti sifatida ishlatib, yangi atama paydo bo'lganda muhokama qilish.
- Takroriy tushunchani (`CustomerInfo` va `ClientData` kabi) ArchUnit nomlash qoidasi bilan ushlash.
- Agregat invariantlarini testda qoldirib, boshqa dasturchi uni buzganda build yiqilishini ta'minlash.
- Kontekstlar orasidagi kontrakt testini alohida, sekinroq tezlikda ishlatish.

**Ehtiyot bo'ling:** Nomdan kelib chiqib buni faqat DevOps masalasi deb tushunish - eng keng tarqalgan chalkashlik: yashil build modelning butunligini kafolatlamaydi, agar jamoa umumiy tilni muhokama qilmasa. Teskari tomondan, kontekstlar orasida ham uzluksiz integratsiyani majburlashga urinish qimmat: Evans buni ataylab bitta kontekst bilan cheklaydi va chegaradagi muvofiqlashtirish uchun shared kernel, customer-supplier yoki anti-corruption layer ishlatiladi.

```yaml
# Model butunligini tekshiradigan quvur: oddiy testdan tashqari
# modul chegarasi va nomlash qoidalari ham build'ni yiqitadi
name: ci
on: [push, pull_request]
jobs:
  verify:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-java@v4
        with: { distribution: temurin, java-version: '21' }
      - run: ./gradlew test                      # domen invariantlari
      - run: ./gradlew archTest modulithVerify   # model parchalanishi
```

## 13.40 Assertions (Assertions)

**Tavsif:** Evans 10-bobda Supple Design tarkibida beradi: yon ta'sirsiz funksiyalarni ajratgandan keyin ham entity'da yon ta'sir chiqaradigan buyruqlar qoladi va ulardan foydalanuvchi oqibatni bilishi kerak. Buyruq boshqa buyruqni chaqirganda bu muammo kuchayadi - yuqori darajadagi buyruqni ishlatuvchi har bir ichki buyruq oqibatini tushunishi kerak bo'ladi va enkapsulyatsiya foydasi yo'qoladi; bitta interfeysni implementatsiya qilgan ikki subclass turli yon ta'sirga ega bo'lishi esa abstraksiyani buzadi. Yechim "design by contract" maktabidan olingan: amal uchun keyingi shart (post-condition), uning amal qilishi uchun kerakli oldingi shart (precondition) va har qanday amal oxirida obyekt holati haqidagi sinf invarianti e'lon qilinadi; invariant butun agregat uchun ham e'lon qilinishi mumkin. Evans ta'kidlaydi: bu da'volar protsedura emas, holat haqida, shuning uchun ularni tahlil qilish va testga aylantirish oson. Agar til assertion'ni to'g'ridan-to'g'ri ifodalay olmasa, ular avtomatik unit test sifatida yoziladi.

**Spring'da qayerda uchraydi:** Oldingi shartlar uchun `Objects.requireNonNull`, `org.springframework.util.Assert` (`Assert.state`, `Assert.isTrue`) va Bean Validation (`@NotNull`, `@Positive`) ishlatiladi; keyingi shart va invariant esa odatda testda tekshiriladi, chunki Java `assert` kalit so'zi ishga tushirishda o'chirilgan bo'ladi. Testda AssertJ (`spring-boot-starter-test` ichida) holatni tekshirish uchun qulay. Shartnomani Javadoc'da qanday yozish [shartnoma yozish qoidasi](../clean-code/10-javadoc-va-api-hujjati.md#104-shartnoma-yozish-oldin-shart-keyin-shart-invariant) da batafsil.

**Qo'llanish keyslari:**
- Agregat invariantini bitta gapda yozib, uni `validate()` metodida har o'zgarishdan keyin tekshirish.
- Buyruq metodining keyingi shartini test nomida ifodalash: `tasdiqlangandan keyin status CONFIRMED va hodisa chiqadi`.
- Konstruktorda oldingi shartlarni tekshirib, noto'g'ri holatdagi obyektning yaratilishiga yo'l qo'ymaslik.
- Interfeysni implementatsiya qiluvchi barcha sinflar uchun umumiy shartnoma testi yozish.
- Pul va miqdor hisoblashda "umumiy summa o'zgarmaydi" invariantini testga aylantirish.

**Ehtiyot bo'ling:** Java `assert` operatoriga tayanmang: u `-ea` flagisiz ishlamaydi, shuning uchun ishlab chiqarishda invariant himoyasiz qoladi. Shuningdek assertion'ni istisno bilan aralashtirib yubormang: oldingi shart buzilishi programmist xatosi (`IllegalArgumentException`, `IllegalStateException`), biznes qoidasi buzilishi esa domen istisnosi bo'lishi kerak. Evans ogohlantirganidek, o'zaro qarama-qarshi bo'lmagan har qanday da'vo to'plami nazariy jihatdan ishlaydi, lekin odamlar predikatni boshida kompilyatsiya qilmaydi: shuning uchun odamga tushunarli, modelga mos da'volar izlanadi.

```java
public final class Shipment {
    private final List<Parcel> parcels = new ArrayList<>();
    private ShipmentStatus status = ShipmentStatus.DRAFT;

    // oldingi shart: status DRAFT; keyingi shart: parcels soni bittaga oshadi
    public void addParcel(Parcel parcel) {
        Assert.state(status == ShipmentStatus.DRAFT, "faqat DRAFT holatda parcel qo'shiladi");
        parcels.add(Objects.requireNonNull(parcel, "parcel null bo'lmaydi"));
        checkInvariant();
    }

    // agregat invarianti: jo'natmaning umumiy vazni ruxsat etilgan chegarada
    private void checkInvariant() {
        Weight total = parcels.stream().map(Parcel::weight).reduce(Weight.ZERO, Weight::plus);
        if (total.exceeds(Weight.ofKilograms(30))) {
            throw new ShipmentOverweightException(total);
        }
    }
}
```
## 13.41 Tushuncha konturlari (Conceptual Contours)

**Tavsif:** Evans 10-bobda donadorlik (granularity) savoliga javob beradi: funksionallikni moslashuvchan kombinatsiya uchun juda mayda bo'laklashish ham, murakkablikni yashirish uchun juda yirik to'da qilish ham, hamma sinfni bir xil kattalikda ushlash ham ishlamaydigan soddalashtirishlar. Monolit konstruksiyaga yopilgan model elementi funksiyani takrorlaydi va ma'nosi tushunarsiz bo'ladi; teskarisiga, haddan ortiq bo'laklash klient kodini mayda bo'laklarni qanday yig'ishni bilishga majbur qiladi va tushunchani butunlay yo'qotadi. Evans buni yorqin qiyoslash bilan beradi: uranium atomining yarmi uranium emas. Yechim domenning ichidagi mantiqiy izchillikka tayanadi: har qaror paytida "bu hozirgi modeldagi munosabatlarga asoslangan qulaylikmi, yoki domenning asl konturini takrorlaydimi" deb so'rash kerak. Ketma-ket refactoring paytida o'zgarish va barqarorlik o'qlari kuzatiladi va shu o'qlar ostidagi konturlar topiladi. Agar domende "qo'shish" amali butun ma'noga ega bo'lsa, u bitta metod bo'ladi va ikki qadamga bo'linmaydi; bu Ward Cunningham ning WHOLE VALUE patterniga ishora. Mos kelishning belgisi: keyingi refactoringlar mahalliy bo'lib qoladi.

**Spring'da qayerda uchraydi:** Donadorlik qarori paket va modul darajasida ko'rinadi: Spring Modulith modullari va [feature bo'yicha paketlash](12-arxitektura-uslublari.md#1228-feature-boyicha-vs-qatlam-boyicha-paketlash-package-by-feature-vs-package-by-layer) qaysi chegaralar tabiiy ekanini ochadi. Value object darajasida esa `record` ichida butun amal (`Money::plus`, `DateRange::intersect`) qoldiriladi, klient kodga bo'lak qadamlar chiqarilmaydi. Konturga mos kelmaslikning belgisi: bitta talab bir necha modulni birdan o'zgartirishga majbur qiladi, bu Modulith verify testida bog'liqlik shaklida ko'rinadi.

**Qo'llanish keyslari:**
- `addAmount()` va `addCurrencyCheck()` kabi ikki qadamni bitta `plus()` amaliga yig'ish.
- Chegirma hisoblashni mayda `calculateStep1..3` metodlaridan domen ma'nosiga ega `applyPromotion()` ga ko'chirish.
- Refactoring tarixini ko'rib, har doim birga o'zgaradigan sinflarni bitta modulga yig'ish.
- Ekspert uchun ahamiyatsiz detalni (pigment tarkibi kabi) bitta butun qiymatga yopib, modelni soddalashtirish.
- Bir talab tufayli uchta modul o'zgarganda buni model noto'g'riligining signali deb ko'rish va modelni chuqurlashtirish.

**Ehtiyot bo'ling:** Konturni kitobdan yoki "cookbook" qoidasidan izlash foydasiz: Evans aytganidek, oshxona retsepti ishlamaydi va javob faqat domenga intuitsiya bilan topiladi. Shuningdek konturlarni oldindan, refactoringdan oldin topishga urinish ham xato: ular odatda ketma-ket refactoring natijasida chiqadi va texnik refactoring o'zi ularni bermaydi.

```java
// Konturga mos: domenda ma'no bor amal bitta metod
public record Money(BigDecimal amount, Currency currency) {
    public Money plus(Money other) {
        if (!currency.equals(other.currency)) throw new CurrencyMismatchException();
        return new Money(amount.add(other.amount), currency);
    }
}
// Konturdan chetda: klient uchta qadamni to'g'ri tartibda chaqirishi shart
// total.checkCurrency(other); total.addRaw(other); total.normalizeScale();
```

## 13.42 Deklarativ dizayn (Declarative Design)

**Tavsif:** Evans 10-bobda deklarativ dizaynni Supple Design ning mantiqiy davomi sifatida beradi: qo'lda yozilgan kodda assertion'lar hech qachon haqiqiy kafolat bermaydi, chunki ataylab yoki tasodifan e'lon qilinmagan yon ta'sir qo'shilishi mumkin. Deklarativ dizayn esa programmaning bir qismini bajariladigan spetsifikatsiya shaklida yozish demakdir: xususiyatlarning aniq tavsifi dasturni boshqaradi va bu reflection yoki kompilyatsiya paytidagi kod generatsiyasi orqali amalga oshadi. Evans buni model-driven design ning "muqaddas kosasi" deb ataydi, lekin amaliy tuzoqlarni ham sanaydi: deklaratsiya tili kerak bo'lgan hamma narsani ifodalay olmaydi, framework esa avtomatlashtirilgan qismdan tashqariga chiqishni qiyinlashtiradi; kod generatsiyasi generatsiya qilingan kodni qo'lda yozilgan kod bilan qo'shib tashlaganda qayta generatsiya buzg'unchi bo'ladi. Natija kutilmagan bo'ladi: dasturchilar framework cheklovida qolib, model va ilovani soddalashtirib tashlaydi. Eng katta foyda tor qamrovli framework bir aniq zerikarli va xatoga moyil jihatni (masalan persistence va object-relational mapping) avtomatlashtirganda ko'rinadi.

**Spring'da qayerda uchraydi:** Spring ekotizimi deklarativ dizaynning tor qamrovli variantiga to'la: Spring Data derived query metodlari va `Specification`, Bean Validation annotatsiyalari, Spring Security `HttpSecurity` lambda DSL, Spring Integration DSL. Domen tomonida deklarativ uslub spetsifikatsiyalarni kombinatsiya qilishda ko'rinadi: `and`, `or`, `not` bilan biznes qoidasini o'qiladigan ifoda sifatida yozish mumkin. Qoidalar dvigateli (rule engine) ham shu yo'nalishda, lekin Evans ta'kidlaganidek, boshqaruv predikatlari qo'shilgach u haqiqiy deklarativlikni yo'qotadi.

**Qo'llanish keyslari:**
- Mijoz tanlash shartlarini `Specification` kombinatsiyasi sifatida yozib, yangi shartni bitta qator bilan qo'shish.
- Validatsiya qoidalarini annotatsiya va custom `ConstraintValidator` bilan deklarativ ifodalash.
- Xavfsizlik qoidalarini imperativ `if` lar o'rniga `HttpSecurity` DSL'da yig'ish.
- Chegirma siyosatlarini nomlangan spetsifikatsiyalar katalogiga aylantirib, marketing tilida o'qiladigan qilish.
- Kod generatsiyasini faqat alohida papkaga chiqarib, qo'lda yozilgan kod bilan aralashtirmaslik.

**Ehtiyot bo'ling:** Evans sanagan ikki tuzoq bugun ham aktual: ifodalash kuchi yetmagan DSL va buzg'unchi kod generatsiyasi. Shuning uchun deklarativ qatlam har doim imperativ chetlab o'tish yo'liga ega bo'lishi kerak (masalan `Specification` yonida qo'lda yozilgan query). Shuningdek "chiroyli DSL" ni ekspert tilidan uzoq atamalar bilan qurish deklarativ dizayn maqsadini yo'q qiladi: deklaratsiya umumiy til gaplariga o'xshamasa, u shunchaki yana bir framework.

```java
// Deklarativ: qoida kombinatsiya qilinadigan spetsifikatsiya sifatida
public final class CustomerSpecs {
    public static Specification<Customer> active() {
        return (root, q, cb) -> cb.isTrue(root.get("active"));
    }
    public static Specification<Customer> inCountry(String code) {
        return (root, q, cb) -> cb.equal(root.get("address").get("countryCode"), code);
    }
}

// Biznes qoidasi o'qiladigan ifoda bo'ladi, imperativ filtr emas
List<Customer> targets = customers.findAll(active().and(CustomerSpecs.inCountry("UZ")));
```

## 13.43 Chuqur tushunchaga qarab refactoring (Refactoring Toward Deeper Insight)

**Tavsif:** Bu Evans kitobining III qismi nomi va u texnik refactoringdan farq qiladi: maqsad kodni chiroyli qilish emas, modelni domen haqidagi yangi tushuncha bilan chuqurlashtirish. Evans uch narsa birga kelishini ta'kidlaydi: domen asosidagi refactoring, chuqur model va egiluvchan dizayn. Sabab ikki tomonlama: chuqur model ifodali dizaynni imkonli qiladi, ifodali va egiluvchan dizayn esa dasturchiga tajriba o'tkazish va natijani ko'rish imkonini berib, modelni kashf qilishga ozuqa beradi. Kod refactoring qilish qiyin bo'lsa, modellashtirish jarayoni ham to'xtaydi. Evans jarayonning tartibini ham ko'rsatadi: avval yashirin tushunchalarni aniq qilish (9-bob), keyin dizaynni egiluvchan qilish (10-bob), zarur bo'lsa tahlil patternlari va dizayn patternlaridan tushuncha olish. Muhim ogohlantirish: bu yo'l faqat texnik ko'rsatkichlarga (metodlar uzunligi, takrorlanish) tayanib bormaydi, u bilim yig'ish va ekspert bilan muloqotdan boshlanadi.

**Spring'da qayerda uchraydi:** Amalda bu domen paketidagi nomlarni o'zgartirish va mas'uliyatni ko'chirishdan iborat bo'ladi va xavfsizligi testlarga bog'liq: agregat invariantlari uchun unit test, modul chegarasi uchun `ApplicationModules.verify()`. IDE refactoring vositalari nomni bir zumda almashtiradi, lekin yangi nom umumiy tildan olinishi kerak, aks holda refactoring faqat kosmetik bo'ladi. Katta model o'zgarishini bosqichlarga bo'lish uchun yangi va eski modelni vaqtincha birga ushlab turish mumkin: domen qatlamida yangi model, adapterda esa eski shaklga mapping.

**Qo'llanish keyslari:**
- Ekspert bilan suhbatda yangi atama chiqqanda shu atamani modelga kiritib, eski nomlarni almashtirish.
- `OrderService` ichidagi takroriy `if` ni yangi value object (`DeliveryWindow`) ga aylantirish.
- Testni avval yangi model tilida yozib, keyin kodni unga moslashtirish.
- Har refactoringdan keyin qaysi tushuncha aniq bo'lganini ADR da bir gap bilan qoldirish.
- Modeldagi tushunchani topish uchun domen hujjatini yoki sohaning standart terminologiyasini o'qish.

**Ehtiyot bo'ling:** Chuqur modelni rejada "uchinchi sprintda" belgilab qo'yish ishlamaydi: tushuncha ketma-ket kichik yaxshilanishlar natijasida keladi. Teskarisiga, "katta refactoring" nomi ostida modelni butunlay qayta yozishga kirishish ham xavfli, agar yangi model ekspert tilidan emas, dasturchining estetikasidan tug'ilgan bo'lsa. Core domain'dan tashqarida esa bu kuchni sarflash o'zini oqlamaydi.

```java
// Oldin: qoida nomi yo'q, shart servisda tarqalgan
if (order.getRequestedDate().isAfter(LocalDate.now().plusDays(2))
        && order.getRequestedDate().getDayOfWeek() != DayOfWeek.SUNDAY) { /* ... */ }

// Keyin: ekspert tilidan olingan tushuncha modelga chiqdi
public record DeliveryWindow(LocalDate earliest, LocalDate latest) {
    public boolean accepts(LocalDate requested) {
        return !requested.isBefore(earliest) && !requested.isAfter(latest);
    }
}
// Nom o'zgardi, mas'uliyat ko'chdi: bu kosmetik emas, model refactoringi.
```

## 13.44 Breakthrough (Breakthrough)

**Tavsif:** Evans 8-bobni butunlay bitta hikoyaga bag'ishlaydi: ketma-ket refactoringlardan keyin loyihada modelning sakrashi (breakthrough) yuz berdi va qattiq kodning katta bo'lagi chuqurroq modelning sodda ifodasiga almashdi. Evans ikki muhim xususiyatini ko'rsatadi. Birinchisi, bu rejalashtirilmaydi: imkoniyat ko'pincha qo'rqinchli ko'rinadi, chunki oddiy refactoringdan ko'ra ham imkoniyati, ham xavfi katta, vaqti esa noqulay bo'lishi mumkin. Ikkinchisi, u bo'sh joydan chiqmaydi: Evans "Focus on Basics" deb maslahat beradi - sakrashni ko'zlab falaj bo'lmaslik kerak, aksincha bilim yig'ish va mustahkam umumiy tilni o'stirish, yashirin tushunchalarni aniq qilish, dizaynni egiluvchan qilish va modelni distillash kerak; bular oldindan aytib bo'ladigan va aniqlikni oshiradigan vositalar va sakrash odatda shulardan keyin keladi. Hikoyadagi qaror ham ibratli: jamoa menejerga aniq savollarga aniq javob berdi (qancha vaqt ketadi, muammoni bu o'zgarishsiz hal qilish mumkinmi, keyingi relizda yurish mumkinmi, bu to'g'ri ishmi) va natijada uch haftalik ish bilan model butun ilovaning birlashtiruvchi mavzusiga aylandi, marketing ham shu til bilan gapira boshladi.

**Spring'da qayerda uchraydi:** Texnik tomoni oddiy, tashkiliy tomoni qiyin: sakrash paytida domen qatlami qayta yoziladi, lekin tashqi kontrakt (REST API, Kafka topic sxemasi) saqlanishi kerak. Shuning uchun yangi model adapter orqasida yopiladi, eski API esa bir muddat ikkinchi model ustida ishlatiladi. Qarorni ADR shaklida yozish, tashqi kontraktni kontrakt testlari bilan muhofaza qilish va o'zgarishni funksiya kaliti ostida chiqarish amalda eng ishonchli yo'l.

**Qo'llanish keyslari:**
- Takroriy va tushunarsiz talab o'zgarishlari ketma-ket kelganda buni model mos kelmayotganining signali deb ko'rish.
- Sakrash qarorini menejerga narx, xavf va alternativa bilan bir sahifada taqdim qilish.
- Yangi modelni tashqi API ni o'zgartirmasdan, adapter orqasida chiqarish.
- Yangi model atamalarini darhol umumiy tilga kiritib, marketing va support bilan ham shu tilda gaplashish.
- Sakrashni ko'zlamasdan, haftada bir kichik model yaxshilanishini kiritishni odat qilish.

**Ehtiyot bo'ling:** Har bir katta refactoringni "breakthrough" deb atash atamani qadrsizlantiradi: Evans da bu domen haqidagi yangi tushunchadan tug'iladi, texnik stack yoki framework almashtirishdan emas. Ikkinchi xato - sakrashni kutib, oddiy yaxshilanishlardan tiyilish: Evans buni aniq taqiqlaydi. Uchinchisi - sakrashni tashqi kontraktni birgalikda buzadigan tarzda chiqarish: bu domen foydasini integratsiya xarajati bilan yo'qotadi.

```java
// Oldin: foiz va yaxlitlash mantiqi har hisoblashda takrorlanadi
BigDecimal lenderShare = amount.multiply(BigDecimal.valueOf(lenderPercent))
        .divide(BigDecimal.valueOf(100), 2, RoundingMode.HALF_UP);   // qoldiq yo'qoladi

// Keyin: domen tushunchasi modelga chiqdi va yaxlitlash bir joyda
public record SharePie(Map<LenderId, Share> shares) {
    public Map<LenderId, Money> allocate(Money total) { /* qoldiqsiz taqsimlash */ return Map.of(); }
}
// Sakrashning belgisi: yangi tushuncha paydo bo'lgach, kutilmagan
// talab o'zgarishlari to'xtadi va bitta nom butun ilovaning mavzusi bo'ldi.
```
## 13.45 Distillation (Distillation)

**Tavsif:** Distillation - Evans kitobining 15-bobi va u yagona pattern emas, balki modelni butun holda tozalash printsipi: aralashmadan eng qimmatli mohiyatni ajratib olish. Qatlamli arxitektura biznes tushunchalarini texnik mantiqdan ajratadi, lekin katta tizimda ajratilgan domen qatlamining o'zi ham boshqarilmas darajada murakkab bo'lib qolishi mumkin. Evans distillashning beshta aniq foydasini sanaydi: jamoaning hamma a'zosi tizimning umumiy dizaynini va qismlar qanday birlashishini tushunadi; boshqarilishi mumkin o'lchamdagi core model aniqlanib, umumiy tilga kiradi; refactoring yo'naltiriladi; ish modelning eng qimmatli joyiga qaratiladi; outsourcing, tayyor komponent sotib olish va vazifa taqsimlash qarorlari asoslanadi. 15-bobdagi patternlar shu maqsadga olib boruvchi yo'l xaritasi bo'lib, core domain ni aniqlashdan boshlanadi va uni model qolgan qismidan ajratishning turli texnikalari bilan davom etadi.

**Spring'da qayerda uchraydi:** Distillash natijasi kod strukturasida ko'rinadi: core subdomain alohida Gradle moduli yoki Spring Modulith moduli bo'ladi, generic qismlar esa kutubxona yoki tashqi xizmatga chiqariladi. `ApplicationModules` verify testi distillash chegaralarini qotirib qo'yadi, `Documenter` esa modul xaritasini chiqarib, qaysi qism yadro ekanini ko'rsatadi. Amalda eng ko'p uchraydigan qadam - autentifikatsiya, xabar yuborish va hisobot kabi generic qismlarni core moduldan chiqarish.

**Qo'llanish keyslari:**
- Monolitning paket daraxtini ko'rib, core subdomain paketini alohida modulga ajratish.
- Generic funksiyalarni (email yuborish, PDF yasash) tashqi xizmat yoki kutubxonaga chiqarish.
- Qaysi modulga eng tajribali dasturchilar qo'yilishini distillash natijasiga qarab qaror qilish.
- Outsourcing qilinadigan qismni aniqlash uchun core va generic chegarasini oldin chizish.
- Refactoring ustuvorligini belgilashda core domain'dagi kodga birinchi navbatda tegish.

**Ehtiyot bo'ling:** Distillashni "hamma narsani mukammal paketlarga ajratish" deb tushunish resursni yoyib tashlaydi: maqsad core ni ko'rinadigan qilish, qolgan massani esa vaqtincha o'z joyida qoldirish mumkin. Ikkinchi tuzoq - core domain ni texnik mezon bilan belgilash (eng ko'p kod, eng ko'p trafik): mezon raqobat ustunligi, texnik hajm emas.

```text
# Distillash natijasi paket daraxtida ko'rinadi
com.example.pricing            <- CORE: raqobat ustunligi shu yerda
    domain/                    PriceCalculation, PromotionPolicy, SharePie
com.example.catalog            <- SUPPORTING: oddiy CRUD, soddaroq pattern
com.example.notification       <- GENERIC: tayyor xizmat orqasidagi adapter
com.example.shared.graph       <- COHESIVE MECHANISM: graf traversal formalizmi
```

## 13.46 Domen qarashlari bayonoti (Domain Vision Statement)

**Tavsif:** Loyiha boshida model hali mavjud emas, lekin yo'nalishni belgilash zarurati allaqachon bor; keyinchalik esa tizimning qiymatini modelni chuqur o'rganmasdan tushuntirish kerak bo'ladi. Qiyinchilik yana shundaki, modelning kritik jihatlari bir necha bounded context'ga tarqalgan bo'lishi mumkin va bu alohida modellar ta'rifi bo'yicha umumiy fokusni ko'rsatadigan tarzda tuzilmaydi. Evans 15-bobda yechimni oddiy qilib beradi: core domain va u keltiradigan qiymat ("value proposition") haqida bir sahifalik qisqa tavsif yoziladi. Shu modelni boshqalardan ajratmaydigan jihatlar tashlab yuboriladi, model turli manfaatlarga qanday xizmat qilishi va ularni qanday muvozanatlashtirishi ko'rsatiladi, matn tor saqlanadi. Bayonot erta yoziladi va yangi tushuncha paydo bo'lgan sari qayta ko'rib chiqiladi. Evans misolida aviachipta tizimi uchun yo'lovchi ustuvorligi va bron strategiyasini muvozanatlash modelga tegishli, UI ning qulayligi, XML orqali integratsiya va logo keshlash esa muhim bo'lsa ham bayonotga kirmaydi.

**Spring'da qayerda uchraydi:** Bu kod artefakti emas, lekin kod repozitoriysida yashashi kerak: core modul `README.md` sida yoki `package-info.java` Javadoc'ida. Spring Modulith `Documenter` modul tavsiflarini shu matndan oladi, shuning uchun bayonot hujjatga avtomatik chiqadi va eskirmaydi. Menejment uchun yozilgan va keyin unutilgan alohida slayddan farqi aynan shunda: u kod bilan bir joyda turadi va review paytida ko'riladi.

**Qo'llanish keyslari:**
- Yangi loyihada birinchi sprintda bir sahifalik bayonot yozib, uni core modul README'siga qo'yish.
- Mikroservis chegarasi haqidagi bahsni bayonotga qaytib, "bu qism qiymatga xizmat qiladimi" savoli bilan hal qilish.
- Yangi dasturchi onboarding'ini shu bayonotni o'qishdan boshlash.
- Har chorakda bayonotni qayta ko'rib, modeldagi yangi tushunchalarni qo'shish.
- Tayyor mahsulot sotib olish yoki o'zi yozish qarorini bayonotdagi ustunlik ta'rifiga qarab qabul qilish.

**Ehtiyot bo'ling:** Bayonotga texnik qarorlarni (UI, protokol, kesh) kiritish uni oddiy loyiha tavsifiga aylantiradi va ajratish kuchini yo'qotadi. Ikkinchi xato - uni bir marta yozib arxivga qo'yish: Evans aniq aytadi, bu hujjat ishlab chiqishning barcha fazalarida resurs taqsimlash va modellashtirish qarorlarini yo'naltirish uchun ishlatiladi.

```text
# core modul README.md dan parcha: bayonot modelni ajratadigan narsani yozadi

Narx belgilash modeli tarif, aksiya va shartnoma chegirmalarini bitta
tushunchada (SharePie) ifodalaydi va sotuv, moliya va marketing
manfaatlarini muvozanatlashtiradi. Model bir xil chegirma qoidasini
ikki joyda saqlashga yo'l qo'ymaydi.

Bayonotga KIRMAYDI: admin UI shakli, hisobot eksport formati,
narx keshining TTL qiymati.
```

## 13.47 Yoritilgan yadro (Highlighted Core)

**Tavsif:** Domen qarashlari bayonoti core modelni umumiy so'zlar bilan belgilaydi, lekin aniq elementlarni aniqlashni har bir odamning talqiniga qoldiradi. Evans 15-bobda muammoni aniq qo'yadi: core domain ni ko'rish uchun har bir dasturchi katta modelni doimiy ravishda miyasida filtrlashi kerak bo'ladi, bu diqqat talab qiladi va natija dasturchidan dasturchiga, hatto kundan kunga bir xil bo'lmaydi. Kodning strukturasini o'zgartirish ideal yo'l, lekin ko'pincha qisqa muddatda amalga oshmaydi va aynan shu ko'rinishni talab qiladi. Shuning uchun yengilroq ikki texnika beriladi. Birinchisi distillash hujjati: core domain ni tushuntiruvchi alohida, minimal matn - eng muhim tushunchalar ro'yxati, ularning kritik munosabatlarini ko'rsatuvchi diagrammalar yoki asosiy o'zaro ta'sirlarning abstrakt bayoni. Bu to'liq dizayn hujjati emas, balki kirish nuqtasi: o'quvchini kodning kerakli joyiga yo'naltiradi. Ikkinchisi - core elementlarini modelning o'zida belgilash, ya'ni kodda yoki diagrammada ularni ajratib ko'rsatish.

**Spring'da qayerda uchraydi:** Belgilash uchun jMolecules `@AggregateRoot` va `@ValueObject` annotatsiyalari, paket darajasida `package-info.java` izohi va Spring Modulith modul metadatasi ishlatiladi. Distillash hujjati uchun esa `Documenter` yasagan C4 va PlantUML diagrammalari qulay, chunki ular koddan olinadi. ArchUnit testi bilan core paketga faqat ruxsat etilgan bog'liqlik kirishini majburlash mumkin: bu belgini hujjatdan qoidaga aylantiradi.

**Qo'llanish keyslari:**
- Core modul uchun bir sahifalik distillash hujjati yozib, uni repozitoriyda saqlash.
- `package-info.java` da modulning core ekanini va asosiy agregatlarni sanab o'tish.
- Modulith `Documenter` ni build'ga qo'shib, diagrammani har relizda qayta yasash.
- Core paketdagi sinflarni jMolecules annotatsiyalari bilan belgilab, rolni kodda ko'rinadigan qilish.
- Review'da "bu o'zgarish core modelga tegadimi" savolini belgilangan paketlar ro'yxatiga qarab hal qilish.

**Ehtiyot bo'ling:** Distillash hujjatini to'liq dizayn hujjatiga o'stirish uning maqsadini yo'q qiladi: u minimal kirish nuqtasi bo'lishi kerak, aks holda o'qilmaydi va eskiradi. Shuningdek faqat annotatsiya yopishtirib, strukturani o'zgartirmaslik ham vaqtincha chora: Evans ta'kidlaydiki, kodning muhim strukturaviy o'zgarishi core ni aniqlashning ideal yo'li va yengil texnikalar uni almashtirmaydi, faqat qo'llab-quvvatlaydi.

```java
// Core ni kodda belgilash: paket izohi va rol annotatsiyalari
/**
 * CORE DOMAIN: narx belgilash. Asosiy agregatlar: PriceList, SharePie.
 * Bu paketga faqat domain-shared va JDK bog'liqliklari kiradi.
 */
package com.example.pricing.domain;

@AggregateRoot
public final class PriceList { /* ... */ }

@ValueObject
public record Share(Percentage percentage) { }
```

## 13.48 Kogeziyali mexanizmlar (Cohesive Mechanisms)

**Tavsif:** Mexanizmni enkapsulyatsiya qilish obyektga yo'naltirilgan dizaynning odatiy printsipi: murakkab algoritmni niyatni ochib beruvchi nomli metod ichiga yashirib, "nima" ni "qanday" dan ajratish. Evans 15-bobda shu texnikaning tabiiy chegarasini ko'rsatadi: hisoblashlar shunday murakkablashadiki, dizaynni shishiradi va tushunchaviy "nima" mexanistik "qanday" ichida cho'kib ketadi; muammoni ifodalovchi metodlar algoritm metodlari to'dasi ichida ko'rinmas bo'ladi. Evans buni odatda modeldagi muammoning simptomi deb hisoblaydi va birinchi navbatda hisoblashni soddalashtiradigan model izlashni maslahat beradi. Lekin ba'zan mexanizmning bir qismi o'zi tushunchaviy jihatdan izchil bo'lib chiqadi: shunda u alohida yengil frameworkga ajratiladi va imkoniyatlari niyatni ochib beruvchi interfeys orqali ochiladi. Evans ayniqsa formalizmlarga va yaxshi hujjatlashtirilgan algoritm sinflariga e'tibor berishni aytadi: o'z misolida tashkilot ierarxiyasidagi savollar graf traversali ekani aniqlanib, graf frameworki generic subdomain sifatida yozilgan. Mas'uliyat taqsimoti aniq: ifodali model qoidani yoki muammoni shakllantiradi, kogeziyali mexanizm esa uni hal qiladi.

**Spring'da qayerda uchraydi:** Amalda bu alohida Gradle moduli yoki paket bo'ladi: `com.example.shared.graph`, `com.example.shared.scheduling`, va u domen tushunchalariga bog'liq bo'lmaydi. Spring tomonida mexanizm odatdagi bean sifatida inyeksiya qilinadi, lekin interfeysi domen tilida bo'ladi. Tayyor formalizm bo'lsa, kutubxona olinadi: optimallashtirish uchun OR-Tools, grafik uchun JGraphT, qoidalar uchun rule engine. Spring Modulith'da bu modul `shared` sifatida belgilanadi va unga barcha modullar bog'lanishi mumkin.

**Qo'llanish keyslari:**
- Yetkazib berish marshrutini optimallashtirishni alohida mexanizm moduliga chiqarish.
- Tashkilot ierarxiyasidagi "kim tasdiqlashga haqli" savolini graf traversal frameworkiga topshirish.
- Murakkab sana va ish vaqti hisoblashini alohida kalendar mexanizmiga ajratish.
- Soliq jadvali bo'yicha interpolyatsiyani matematik mexanizmga chiqarib, domen faqat qoidani aytishini ta'minlash.
- Mexanizmni tayyor kutubxona bilan almashtirish mumkinligini interfeys orqali saqlab qolish.

**Ehtiyot bo'ling:** Evans aniq ogohlantiradi: bu "hamma narsani hisoblaydigan kalkulyator" emas. Mexanizm tor, bitta hisoblashga yo'naltirilgan bo'lishi va ifodali domen modelini o'z ichiga tortmasligi kerak, aks holda yana bir util paket paydo bo'ladi. Shuningdek mexanizmni ajratishdan oldin modelni soddalashtirish imkonini tekshirmaslik ham xato: murakkab mexanizm ko'pincha noto'g'ri modelning belgisi.

```java
// Domen qoidani aytadi, mexanizm uni hal qiladi
public interface ApprovalGraph {                   // mexanizm interfeysi, domen tilida
    Optional<EmployeeId> firstApproverWithLimit(EmployeeId requester, Money amount);
}

public final class PurchaseRequest {               // core domain
    public EmployeeId routeForApproval(ApprovalGraph graph) {
        return graph.firstApproverWithLimit(requester, amount)
                .orElseThrow(() -> new NoApproverFoundException(amount));
    }
}
// Mexanizm ichida graf traversali turadi: u domen tushunchalarini bilmaydi.
```

## 13.49 Ajratilgan yadro (Segregated Core)

**Tavsif:** Modeldagi elementlar ko'pincha qisman core ga, qisman yordamchi rolga xizmat qiladi va core elementlari generic elementlar bilan qattiq bog'lanib qoladi. Evans 15-bobda natijani aniq ta'riflaydi: core ning tushunchaviy kogeziyasi kuchsiz yoki ko'rinmas bo'ladi, bu chalkashlik core ni bo'g'adi va dizayner eng muhim munosabatlarni ko'rmagani uchun dizayn kuchsiz chiqadi. Generic subdomain'larni ajratish chalkashlikning bir qismini olib tashlaydi, lekin bu og'ir ish va core eski qoldiq bilan chalkashgan holda qoladi. Shuning uchun teskari yo'ldan boriladi: core tushunchalari yordamchilardan (shu jumladan noaniq ta'riflanganlardan) ajratiladi, core ning kogeziyasi kuchaytiriladi va uning qolgan kodga bog'liqligi kamaytiriladi. Evans refactoring qadamlarini sanaydi: core subdomain ni aniqlash (distillash hujjatidan foydalanib), bog'liq sinflarni ularni birlashtiruvchi tushuncha nomi bilan yangi paketga ko'chirish, tushunchaning ifodasi bo'lmagan ma'lumot va funksionallikni ajratib boshqa paketlarga chiqarish, keyin qolgan core ning munosabatlarini soddalashtirish. Narxi ham aytilgan: core dan tashqaridagi qattiq bog'langan sinflar bilan aloqa ba'zan chigalroq ko'rinadi, lekin core ni aniqlashtirishning foydasi bundan ustun.

**Spring'da qayerda uchraydi:** Bu toza paket va modul refactoringi: core sinflarni `com.example.pricing.domain` ga yig'ish, qolganini `pricing.support` yoki boshqa modulga chiqarish. Spring tomonida eng ko'p uchraydigan ish - core sinflardan `jakarta.persistence` va Jackson annotatsiyalarini olib tashlab, ularni adapter DTO ga ko'chirish. `ApplicationModules.verify()` va ArchUnit paket qoidalari ajratishni qotirib qo'yadi, aks holda bir necha reliz ichida bog'liqlik qaytib keladi.

**Qo'llanish keyslari:**
- Distillash hujjatidan core sinflar ro'yxatini olib, ularni yangi paketga ko'chirish.
- Core entity'dan audit, hisobot va eksport maydonlarini alohida sinflarga chiqarish.
- Ko'chirishdan keyin ArchUnit qoidasi bilan core paketga yangi bog'liqlik kirishini taqiqlash.
- Qoldiq massani vaqtincha o'z joyida qoldirib, keyin generic subdomain'larga ajratish.
- Core paketdagi sinflar sonini kuzatib, o'sish sababini har relizda tekshirish.

**Ehtiyot bo'ling:** Ajratishni bir urinishda mukammal qilishga harakat qilmang: Evans qadamlarda ataylab "mukammal bo'lishga ko'p vaqt sarflamang" deb yozadi, chunki maqsad core ni tozalash, qoldiqni ideal joylashtirish emas. Ikkinchi tuzoq - ajratishni faqat paket nomini o'zgartirish deb tushunish: bog'liqlik yo'nalishi o'zgarmasa, core hali ham chalkash qoladi.

```java
// Ajratishdan oldin: core tushunchasi hisobot va audit bilan chalkashgan
class PriceList {
    List<PriceLine> lines;
    String lastExportedCsvPath;        // hisobot detali
    String changedByUserAgent;         // audit detali
}

// Ajratishdan keyin: core faqat narx qoidasini biladi
// com.example.pricing.domain
public final class PriceList { private final List<PriceLine> lines; /* ... */ }
// com.example.pricing.support
record PriceListExport(PriceListId id, String csvPath) { }
record PriceListAudit(PriceListId id, String userAgent, Instant at) { }
```

## 13.50 Abstrakt yadro (Abstract Core)

**Tavsif:** Hatto core domain modeli ham shuncha detalga ega bo'ladiki, umumiy manzarani uzatish qiyinlashadi. Odatdagi javob - katta modelni tushunarli kichik subdomen'larga bo'lish, lekin Evans 15-bobda bu reduktiv paketlashning chegarasini ko'rsatadi: alohida paketlar subdomen'lar orasidagi o'zaro ta'sirni yashirishi yoki hatto chigallashtirishi mumkin. Alohida paketlardagi subdomen'lar o'rtasida ko'p o'zaro ta'sir bo'lsa, ikki yoqimsiz variant qoladi: paketlar orasida juda ko'p havola yasash (bu bo'lishning qiymatini yo'qotadi) yoki o'zaro ta'sirni bilvosita qilish (bu modelni kamroq ifodali va tushunarsiz qiladi). Evans vertikal emas, gorizontal kesishni taklif qiladi: polimorfizm bizga tur nusxalaridagi detal farqlarini e'tiborsiz qoldirish kuchini beradi, shuning uchun agar paketlar orasidagi o'zaro ta'sirning ko'pini polimorf interfeyslar darajasida ifodalash mumkin bo'lsa, shu turlarni alohida core paketga chiqarish ma'noli bo'ladi. Shart qat'iy: bu texnik hiyla emas, polimorf interfeyslar domendagi fundamental tushunchalarga mos kelishi kerak. Natijada ixtisoslashgan detal sinflari o'z subdomen paketlarida qoladi va core paketga bog'lanadi, teskarisiga emas.

**Spring'da qayerda uchraydi:** Java'da bu `api` yoki `spi` paketidagi interfeyslar va Java 17+ `sealed interface` bilan ifodalanadi: abstrakt core ruxsat etilgan variantlarni sanab, kompilyatorga ham ma'lum qiladi. Spring Modulith'da bu modulning `NamedInterface` qismi bo'ladi: boshqa modullar faqat shu paketga bog'lanishi mumkin, ichki implementatsiya paketiga esa yo'q. Implementatsiyalar oddiy bean sifatida ro'yxatdan o'tadi va kerak bo'lsa `List<T>` inyeksiyasi orqali yig'iladi.

**Qo'llanish keyslari:**
- To'lov usullari (karta, bank o'tkazmasi, nasiya) uchun abstrakt `PaymentMethod` iyerarxiyasini core paketga chiqarish.
- Sug'urta mahsulot turlarini `sealed interface` bilan ifodalab, variantlarni kompilyatsiya paytida qotirish.
- Modul API paketini ajratib, boshqa modullar faqat shu paketga bog'lanishini Modulith bilan majburlash.
- Subdomen paketlari orasidagi ko'p havolani abstrakt core interfeyslariga almashtirish.
- Yangi variant qo'shilganda faqat bitta subdomen paketini o'zgartirish bilan cheklanish.

**Ehtiyot bo'ling:** Evans aniq aytadi: paketlar orasida tez-tez murojaat qilinadigan sinflarni shunchaki alohida paketga ko'chirish ma'nosiz tartibsizlik beradi. Abstrakt core ni ajratish mexanik emas, u asosiy tushunchalarni va ularning rolini chuqur bilishni va ko'pincha qayta loyihalashni talab qiladi. Shuningdek interfeys sonini oshirib, har bir sinf uchun interfeys yasash ham abstrakt core emas: faqat domendagi fundamental tushunchalar ajratiladi.

```java
// Abstrakt core: fundamental tushunchalar va ular orasidagi o'zaro ta'sir
// com.example.insurance.core
public sealed interface Coverage permits LifeCoverage, PropertyCoverage, MotorCoverage {
    Money premiumFor(RiskProfile profile);
    boolean covers(ClaimType type);
}

// Ixtisoslashgan detal o'z paketida qoladi va core ga bog'lanadi
// com.example.insurance.motor
public record MotorCoverage(VehicleClass vehicleClass, Money deductible) implements Coverage {
    @Override public Money premiumFor(RiskProfile profile) { /* ... */ return Money.ZERO; }
    @Override public boolean covers(ClaimType type) { return type == ClaimType.COLLISION; }
}
```
## 13.51 Katta masshtabli struktura (Large-Scale Structure)

**Tavsif:** Bounded context'ning qat'iy ajratilishi buzilish va chalkashlikni to'xtatadi, lekin tizimni butun holda ko'rishni osonlashtirmaydi; distillash yordam beradi, lekin yordamchi elementlarning core bilan va bir-biri bilan munosabatini tushunish zarurati qoladi. Evans 16-bobda muammoni shunday qo'yadi: katta loyihada odamlar turli qismlarda mustaqil ishlaydi va hech qanday muvofiqlashtirish yoki qoida bo'lmasa, bir xil muammoga turli uslub va turli yechimlar paydo bo'ladi; bitta qism haqidagi bilim boshqasiga o'tmaydi va loyiha oxirida bir-biriga yordam bera olmaydigan modul mutaxassislari qoladi. Katta masshtabli struktura - tizimni yirik chiziqlarda muhokama qilish va tushunish imkonini beradigan til: yuqori darajadagi tushunchalar va qoidalar to'plami butun tizim uchun dizayn naqshini belgilaydi. Evans muhim kuzatuvni ham aytadi: ko'p struktura UML'da ifodalanmaydi va bunga hojat ham yo'q - ular modelni shakllantiradi va tushuntiradi, lekin modelning o'zida ko'rinmaydi, dizayn haqida qo'shimcha muloqot qatlamini beradi. Struktura bitta bounded context ichida ham qolishi mumkin, lekin odatda bir nechtasini qamraydi. Shart ham bor: jamoa kichik va model juda murakkab bo'lmasa, yaxshi nomlangan modullar, bir oz distillash va norasmiy muvofiqlashtirish yetarli bo'ladi.

**Spring'da qayerda uchraydi:** Spring ekotizimida struktura modul nomlari va ular orasidagi ruxsat etilgan bog'liqlik yo'nalishi sifatida ifodalanadi: Spring Modulith modul grafikasi, ArchUnit `layeredArchitecture()` va `slices()` qoidalari. Muhimi shundaki, struktura hujjatda emas, testda yashaydi: shunda u eskirmaydi va buzilish build paytida ko'rinadi. Struktura nomlari paket nomlariga kirgani yaxshi, aks holda yangi dasturchi uni ko'rmaydi.

**Qo'llanish keyslari:**
- Katta monolitda modul nomlarini bitta tushuncha tizimiga keltirib, struktura tilini yaratish.
- Ruxsat etilgan bog'liqlik yo'nalishini ArchUnit testi bilan ifodalash.
- Yangi modul qo'shilganda uning strukturadagi o'rnini oldin aytib, keyin kod yozish.
- Review'da "bu sinf strukturada qaysi qismga tegishli" savolini standart tekshiruv punkti qilish.
- Kichik jamoada struktura kiritmaslik qarorini ADR da ataylab yozib qoldirish.

**Ehtiyot bo'ling:** Evans ta'kidlaydi: mos kelmagan struktura ishlab chiqishga qattiq to'sqinlik qiladi va katta masshtabli struktura umuman majburiy emas. Shuning uchun strukturani "to'g'ri arxitektura" deb loyiha boshida qotirib qo'yish xavfli; u model bilan birga rivojlanishi kerak. Ikkinchi xato - strukturani faqat texnik qatlamlar (controller, service, repository) deb tushunish: bu domen haqida hech narsa aytmaydi.

```java
// Struktura hujjatda emas, testda yashaydi
@ArchTest
static final ArchRule struktura_yonalishi = layeredArchitecture().consideringOnlyDependenciesInLayers()
        .layer("Operations").definedBy("com.example.shipping.operations..")
        .layer("Capability").definedBy("com.example.shipping.capability..")
        .whereLayer("Operations").mayNotBeAccessedByAnyLayer()
        .whereLayer("Capability").mayOnlyBeAccessedByLayers("Operations");
// Qoida buzilsa build yiqiladi: struktura tili jamoada saqlanadi.
```

## 13.52 Rivojlanuvchi tartib (Evolving Order)

**Tavsif:** Evans 16-bobni aynan shu pattern bilan boshlaydi, chunki u qolgan struktura patternlariga shart qo'yadi. Tartibsiz dizaynning narxini ko'rgan jamoalar ishlab chiqishni cheklaydigan arxitekturalar joriy qiladi. Ba'zi texnik arxitekturalar haqiqiy texnik muammoni (tarmoq, persistence) hal qiladi, lekin arxitektura ilova va domen modeli hududiga kirganda o'zi muammo tug'diradi: dasturchilarga muammoga mos model qurishga xalaqit beradi, eng ambitsiyali variantlari esa ularni dasturlash tilining tanish kuchidan ham mahrum qiladi. Texnik yoki domen yo'nalishli bo'lishidan qat'i nazar, arxitekturalar ko'p oldindan qabul qilingan dizayn qarorini qotirib qo'yadi va talablar o'zgargan, tushuncha chuqurlashgan sari bu qisqich bo'lib qoladi. Evans ikki chetni ham rad etadi: nazoratsiz erkinlik hech kim butun holda tushunmaydigan tizim beradi, qattiq arxitektura esa ilovani struktura ostida soddalashtirishga yoki strukturani buzib tashlashga olib keladi. Muammo qoidalarning borligida emas, balki ularning qattiqligi va manbasida. Shuning uchun struktura ilova bilan birga rivojlanishi, hatto butunlay boshqa turga o'tishi kerak va u detalli dizayn qarorlarini haddan ortiq cheklamasligi lozim.

**Spring'da qayerda uchraydi:** Amalda bu struktura qoidalarini kod bilan birga o'zgartirish imkonini saqlashda ko'rinadi: ArchUnit va Modulith qoidalari pull request ichida kod bilan birga tahrirlanadi, alohida me'morchilik qo'mitasidan o'tmaydi. Shuningdek paket strukturasini erta qotirib qo'ymaslik foydali: boshida kengroq modul olinadi, keyin bilim yig'ilgan sari bo'linadi. Fitness funksiya sifatida yozilgan arxitektura testi strukturaning o'zgarishini ko'rinadigan va muhokama qilinadigan qiladi.

**Qo'llanish keyslari:**
- Yangi loyihada bitta kengroq modul bilan boshlab, chegaralarni keyin aniqlashtirish.
- Arxitektura qoidasini o'zgartirish uchun alohida jarayon emas, oddiy pull request ishlatish.
- Struktura turini almashtirish qarorini ADR da sabab bilan yozib qoldirish.
- Struktura qoidasi ishni to'sayotganini sezganda uni muhokamaga qo'yish, chetlab o'tmaslik.
- Har chorakda arxitektura testlarini ko'rib, eskirgan qoidalarni olib tashlash.

**Ehtiyot bo'ling:** Evans aniq aytadi: katta masshtabli strukturani tanlash model ni butun holda boshqarish foydasini alohida qismlarning ideal tuzilishidan ustun qo'yish demakdir, shuning uchun murosaga tayyor bo'lish kerak. Lekin bu murosa haddan oshmasligi uchun haddan ortiq cheklovchi strukturalardan voz kechiladi. Ikkinchi tuzoq - strukturani "evolyutsiya qiladi" deb nomlab, amalda hech qachon o'zgartirmaslik: qoida kodda va testda bo'lmasa, uni o'zgartirish ham ko'rinmaydi.

```java
// Struktura qoidasi kod bilan bir repozitoriyda yashaydi va PR da o'zgaradi
@ArchTest
static final ArchRule modul_mustaqilligi = slices()
        .matching("com.example.(*)..")
        .should().beFreeOfCycles();
// Boshida kengroq modul: com.example.sales
// Bilim yig'ilgach bo'linadi: com.example.sales.pricing, com.example.sales.quoting
// Qoida ham shu PR da o'zgaradi, alohida qo'mitada emas.
```

## 13.53 Tizim metaforasi (System Metaphor)

**Tavsif:** Metaforik fikrlash dasturlashda, ayniqsa modellashtirished, hamma joyda uchraydi, lekin Extreme Programming'dagi "metaphor" amaliyoti undan aniq ma'noda foydalanadi: butun tizimni tartibga soluvchi metafora. Evans 16-bobda firewall misolini beradi: bino yonmasligi uchun qurilgan devor kabi dasturiy "devor" mahalliy tarmoqni tashqi tarmoq xavflaridan himoya qiladi; shu metafora tarmoq arxitekturalariga ta'sir qildi va butun mahsulot kategoriyasini shakllantirdi, yangi odamlar ham uni darhol tushunadi. Lekin Evans metaforaning ikkinchi yuzini ham ko'rsatadi: bu noaniq analogiya va u haddan ortiq tanlovchi bo'lmagan, kerakli almashinuvga ham to'sqinlik qiladigan va devor ichidagi tahdiddan himoya qilmaydigan to'siqlarning paydo bo'lishiga olib keldi. Struktura sifatida tizim metaforasi bo'sh va oson tushuniladigan bo'lgani uchun turli modellar unga taqribiy mos kelishi mumkin, shuning uchun u bir necha bounded context'da ishlatilib, ular orasidagi ishni muvofiqlashtirishga yordam beradi. Evans ogohlantirishni ham aniq beradi: metafora XP ning asosiy amaliyotlaridan biri bo'lgani uchun mashhur bo'ldi, lekin kam loyiha haqiqatan foydali metafora topdi va uni zarar keltiradigan domenlarga ham tiqishtirishga urindilar.

**Spring'da qayerda uchraydi:** Metafora kodda nomlar orqali ko'rinadi: `Pipeline`, `Stage`, `Ledger`, `Warehouse`, `Dispatcher`. Spring Integration va Spring Batch o'zi quvur (pipeline) metaforasiga qurilgan, shuning uchun ularni ishlatgan loyihada metafora tabiiy chiqadi. Muhim shart: metafora nomlari umumiy tilga mos kelishi kerak; ekspert "ledger" deb gapirmasa, bu nom faqat dasturchilar uchun ichki hazil bo'lib qoladi.

**Qo'llanish keyslari:**
- To'lov hisob-kitobini "ledger" metaforasida modellashtirib, barcha o'tkazmalarni yozuv sifatida ko'rish.
- Ma'lumot oqimini quvur va bosqichlar metaforasida ifodalab, modul nomlarini shunga moslash.
- Yangi dasturchiga tizimni bir gapli metafora bilan tushuntirib, keyin detalga kirish.
- Metaforani marketing va support bilan ham tekshirib, u tashqi muloqotda ishlashini ko'rish.
- Metafora noto'g'ri assotsiatsiya berayotganini sezganda undan voz kechish.

**Ehtiyot bo'ling:** Evans ning ogohlantirishi asosiy: ishonchli metafora dizaynga analogiyaning muammoga keraksiz jihatlarini olib kirish xavfini tug'diradi, yoki analogiya o'zi jozibali bo'lsa ham mos kelmasligi mumkin. Shuning uchun metafora majburiy emas; topilmasa, uni o'ylab topishga vaqt sarflamaslik kerak. Ikkinchi xato - metaforani umumiy til o'rniga qo'yish: metafora taqribiy, umumiy til esa aniq bo'lishi kerak.

```java
// Ledger metaforasi: har o'zgarish o'zgarmas yozuv bo'ladi
public record LedgerEntry(AccountId account, Money amount, EntryType type, Instant at) { }

public final class Ledger {
    private final List<LedgerEntry> entries = new ArrayList<>();

    public void post(LedgerEntry entry) { entries.add(entry); }   // yozuv o'chirilmaydi

    public Money balanceOf(AccountId account) {
        return entries.stream().filter(e -> e.account().equals(account))
                .map(LedgerEntry::amount).reduce(Money.ZERO, Money::plus);
    }
}
// Metafora nomlarni boshqaradi: "post", "entry", "balance" ekspert tilidan.
```

## 13.54 Mas'uliyat qatlamlari (Responsibility Layers)

**Tavsif:** Evans 16-bobda mas'uliyatga asoslangan dizaynni katta masshtabga ko'taradi: har bir obyektga qo'lda tor mas'uliyat berilsa, yo'l-yo'riq ham, bir xillik ham bo'lmaydi va domenning katta bo'laklarini birga boshqarish imkoni yo'qoladi. Ko'p domenda tabiiy qatlamlanish bor: ba'zi tushuncha va faoliyat boshqa elementlar fonida kechadi va bu elementlar mustaqil ravishda, boshqa tezlikda va boshqa sabablarga ko'ra o'zgaradi. Evans bu tabiiy stratifikatsiyadan foydalanishni taklif qiladi: modeldagi tushunchaviy bog'liqliklarga va domenning turli qismlarining o'zgarish tezligi va manbasiga qarab tabiiy qatlamlar aniqlanadi va ular keng abstrakt mas'uliyatlar sifatida nomlanadi; bu mas'uliyatlar tizimning yuqori darajadagi maqsadi va dizayni haqida hikoya qilishi kerak. Keyin model refactoring qilinadi: har bir domen obyekti, agregat va modulning mas'uliyati aniq bitta qatlamga sig'adi. Evans mos keladigan qatlamlash variantini ham aytadi: RELAXED LAYERED SYSTEM, ya'ni qatlam faqat o'zidan bevosita pastdagi emas, har qanday pastdagi qatlamga murojaat qilishi mumkin. Kema yuklari misolida jamoa ikki qatlamni ajratadi: "Operations" (Cargo, Route Specification, Itinerary - kunlik faoliyat) va uning asosi bo'lgan "Capability" (Transit Leg - kompaniya tayanadigan resurslar); Customer ning qaysi qatlamga tushishi esa biznes niyatiga bog'liq.

**Spring'da qayerda uchraydi:** Bu domen qatlami ichidagi struktura, texnik qatlamlardan (web, service, repository) butunlay boshqa narsa. Spring tomonida u paket nomlari va modul bog'liqligi sifatida ifodalanadi: `com.example.shipping.operations` va `com.example.shipping.capability`, va yo'nalish ArchUnit `layeredArchitecture()` qoidasi bilan majburlanadi. Spring Modulith modul grafikasi qatlamlar orasidagi bog'liqlikni ko'rsatadi, `Documenter` esa uni diagrammaga chiqaradi.

**Qo'llanish keyslari:**
- Logistika tizimida kunlik operatsiyalarni va resurs imkoniyatlarini ikki qatlamga ajratish.
- Bank tizimida hisob operatsiyalari va mahsulot shartlari qatlamlarini ajratib, o'zgarish tezligini hisobga olish.
- Har bir agregatning qaysi qatlamga tegishli ekanini paket joylashuvi bilan belgilash.
- Qatlam nomlarini umumiy tilga kiritib, muhokamada ishlatish.
- Qatlam chegarasini buzgan bog'liqlikni arxitektura testi bilan ushlash.

**Ehtiyot bo'ling:** Evans ad hoc qatlamlashni tanqid qiladi: bog'liqliklarni chizib, pastga tushirish bilan yasalgan qatlamlar bog'liqlikni kuzatishni osonlashtiradi, lekin model haqida tushuncha bermaydi va modellashtirish qarorlarini yo'naltirmaydi. Shuning uchun qatlam nomi texnik emas, domen mas'uliyati bo'lishi kerak. Ikkinchi tuzoq - qatlam sonini ko'paytirish: har bir qatlam domenda haqiqiy, mustaqil o'zgarish tezligiga mos kelishi shart.

```text
# Mas'uliyat qatlamlari: nomlar domen mas'uliyatidan, texnik qatlamdan emas
Operations   Cargo, RouteSpecification, Itinerary     <- kunlik faoliyat, tez o'zgaradi
Capability   TransitLeg, VesselSchedule, Customer     <- tayanch resurslar, sekin o'zgaradi

# Yo'nalish: Operations -> Capability. Teskarisi taqiqlanadi.
# Relaxed layered: Operations bir necha pastdagi qatlamga murojaat qilishi mumkin.
```

## 13.55 Bilim darajasi (Knowledge Level)

**Tavsif:** Evans 16-bobda bu patternni Martin Fowler ning *Analysis Patterns* kitobidan oladi va ta'rifni ham shu manbadan keltiradi: bir guruh obyekt boshqa guruh obyekt qanday xatti-harakat qilishi kerakligini tavsiflaydi. Pattern modelning bir qismini foydalanuvchi qo'lida plastik qilish kerak bo'lganda, lekin uni kengroq qoidalar to'plami bilan cheklash lozim bo'lganda ishlatiladi: entity'lar orasidagi rol va munosabatlar o'rnatish paytida yoki hatto ishlash vaqtida o'zgarishi kerak bo'lgan konfiguratsiyalanadigan xatti-harakat talablariga javob beradi. Evans muammoni "accountability" modeli misolida ko'rsatadi: tashkilotlar odam, kichik tashkilot, ular o'ynaydigan rol va munosabatlardan tashkil topgan, lekin bu rol va munosabatlarni boshqaruvchi qoidalar har tashkilotda juda farq qiladi - bir kompaniyada "Director" boshqaradigan "department" "Vice President" ga hisobot beradi, boshqasida nomlar ham, ierarxiya ham boshqa. Taxminlarga qurilgan odatiy ilovada foydalanuvchilar maydonlarni boshqacha ishlatishni boshlaydi, ilovaning xatti-harakati esa semantika o'zgargani uchun xato ishlaydi; keyin ular chetlab o'tish yo'llarini o'ylab topadi va tizimni o'zgartirish yoki almashtirish paytida funksiyalarning haqiqiy ma'nosi boshqa ekani ma'lum bo'ladi. Evans buni REFLECTION patternining domen qatlamiga qo'llanishi deb ham ta'riflaydi.

**Spring'da qayerda uchraydi:** Java'da bu ikki darajali model sifatida yoziladi: `TicketType` (bilim darajasi: qoidalar, ruxsat etilgan o'tishlar, limitlar) va `Ticket` (operatsion daraja: aniq nusxa). JPA bilan ikkalasi ham entity bo'ladi, bilim darajasi odatda kam o'zgargani uchun keshlanadi (Spring Cache yoki Hibernate second-level cache). Konfiguratsiyani Java kodida emas, bazada saqlash qarori aynan shu pattern: shuning uchun `@ConfigurationProperties` bilan farqini bilish kerak, chunki bilim darajasi ishlash vaqtida foydalanuvchi tomonidan o'zgartiriladi.

**Qo'llanish keyslari:**
- SaaS tizimida har bir tenant uchun ticket turlari, holat o'tishlari va limitlarni bazada saqlash.
- Sug'urta mahsulot shartlarini bilim darajasida saqlab, polislarni operatsion darajada yuritish.
- Tashkilot ierarxiyasi qoidalarini (kim kimga hisobot beradi) konfiguratsiyalanadigan qilish.
- Tasdiqlash yo'nalishini (approval workflow) bilim darajasidagi qoidalar bilan belgilash.
- Yangi mahsulot turini kod relizisiz, bilim darajasiga yozuv qo'shish bilan chiqarish.

**Ehtiyot bo'ling:** Evans bilvosita murakkablikni aniq tan oladi: bu pattern tushunarsizlikning bir qismini qaytarib olib keladi va bilim darajasi o'zgarganda allaqachon mavjud operatsion daraja obyektlari bilan nima qilish kerakligi masalasi tug'iladi - ba'zan ularni migratsiya qilish mumkin, ba'zan yo'q. Shuning uchun uni faqat haqiqatan konfiguratsiyalanadigan xatti-harakat talab qilinganda ishlatish kerak, "balki kelajakda kerak bo'lar" degan taxmin bilan emas: aks holda oddiy `enum` bilan hal bo'ladigan narsa ikki darajali metamodelga aylanadi.

```java
// Bilim darajasi: qoidalarni tavsiflaydi va foydalanuvchi tomonidan o'zgaradi
@Entity
public class TicketType {
    @Id private TicketTypeId id;
    private Duration slaResponseTime;
    @ElementCollection private Set<TicketStatus> allowedStatuses;

    public boolean allows(TicketStatus next) { return allowedStatuses.contains(next); }
}

// Operatsion daraja: aniq nusxa, qoidani bilim darajasidan so'raydi
@Entity
public class Ticket {
    @ManyToOne private TicketType type;
    private TicketStatus status;

    public void moveTo(TicketStatus next) {
        if (!type.allows(next)) throw new IllegalTicketTransitionException(status, next);
        this.status = next;
    }
}
```

## 13.56 Ulanadigan komponent frameworki (Pluggable Component Framework)

**Tavsif:** Evans 16-bobda bu patternni eng talabchan deb ataydi: imkoniyat faqat chuqur va distillangan, yetilgan modelda paydo bo'ladi va odatda bitta domende bir necha ilova allaqachon yozilganidan keyin keladi. Muammo shunday: turli, mustaqil loyihalashtirilgan, lekin bir xil abstraksiyalarga asoslangan ilovalar o'zaro ishlashi kerak bo'lganda ko'p bounded context orasidagi tarjima integratsiyani cheklaydi, shared kernel esa yaqin ishlamaydigan jamoalar uchun amalga oshmaydi; takrorlanish va parchalanish ishlab chiqish va o'rnatish narxini oshiradi. Yechim: interfeyslar va o'zaro ta'sirlarning abstrakt yadrosi distillanadi va shu interfeyslarning turli implementatsiyalarini erkin almashtirish imkonini beradigan framework yasaladi; har qanday ilova shu komponentlardan faqat abstrakt yadro interfeyslari orqali foydalanishi sharti bilan ishlaydi. Odatda barcha komponentlar ulanadigan markaziy hub bo'ladi. Evans texnik frameworkning ikkinchi darajali masala ekanini ta'kidlaydi: asosiy pattern - mas'uliyatlarning tushunchaviy tashkil etilishi va u bitta Java programmasi ichida ham qo'llanadi. Kamchiliklar ham aniq: patternni qo'llash juda qiyin, interfeyslar aniqligini va abstrakt yadroning chuqurligini talab qiladi; ilovalarning imkoniyatlari cheklanadi, chunki domenga boshqacha yondashuv kerak bo'lsa, protokolni barcha komponentlar uchun o'zgartirmasdan buni qilish mumkin emas va chuqur tushunchaga qarab refactoring amalda to'xtaydi.

**Spring'da qayerda uchraydi:** Spring konteynerining o'zi hub rolini bajaradi: interfeys bo'yicha `List<T>` yoki `Map<String, T>` inyeksiyasi barcha implementatsiyalarni yig'adi, `@ConditionalOnMissingBean` va `spring.factories`/`AutoConfiguration.imports` esa almashtirish mexanizmini beradi. JDK tomonida `ServiceLoader` va JPMS `provides ... with` xuddi shu rolni o'ynaydi. Plugin'larni alohida Gradle moduliga chiqarib, faqat abstrakt yadro modulga bog'lash eng toza shakl.

**Qo'llanish keyslari:**
- To'lov provayderlari uchun bitta `PaymentGateway` interfeysi va har provayder uchun alohida modul.
- Soliq hisoblashni mamlakat bo'yicha pluginlarga ajratib, yangi mamlakatni modul qo'shish bilan yoqish.
- Hisobot formatlarini (PDF, XLSX, CSV) bitta interfeys orqasida pluginlashtirish.
- Bir nechta ilova uchun umumiy domen abstraksiyalarini alohida kutubxonaga chiqarish.
- Yangi plugin qo'shilganda abstrakt yadro o'zgarmasligini kontrakt testi bilan tekshirish.

**Ehtiyot bo'ling:** Evans ning ogohlantirishi to'g'ridan-to'g'ri: bu loyihada qo'llanadigan birinchi katta masshtabli struktura bo'lmasligi kerak, ikkinchisi ham emas. Eng muvaffaqiyatli misollar bir nechta ixtisoslashgan ilova to'liq ishlab chiqilganidan keyin paydo bo'lgan. Asosiy to'siq - foydali framework loyihalash uchun kerak bo'ladigan tushunish darajasi. Shuning uchun uni yetilmagan modelda qo'llash modelni muzlatib qo'yadi va keyingi chuqurlashtirishni imkonsiz qiladi.

```java
// Abstrakt yadro interfeysi: barcha pluginlar faqat shu orqali ko'rinadi
public interface TaxRule {
    CountryCode country();
    Money taxFor(Invoice invoice);
}

// Hub: Spring konteyner barcha implementatsiyalarni yig'adi
@Service
public class TaxCalculator {
    private final Map<CountryCode, TaxRule> rules;

    public TaxCalculator(List<TaxRule> discovered) {
        this.rules = discovered.stream().collect(toMap(TaxRule::country, identity()));
    }

    public Money calculate(Invoice invoice) {
        TaxRule rule = rules.get(invoice.countryCode());
        if (rule == null) throw new UnsupportedCountryException(invoice.countryCode());
        return rule.taxFor(invoice);
    }
}
```
## 13.57 Hodisa manbali domen modeli (Event-Sourced Domain Model)

**Tavsif:** Khononov 7-bobda domen modelining variantini beradi: oddiy domen modeli agregat holatini saqlaydi va tanlangan domen hodisalarini chiqaradi, hodisa manbali domen modeli esa agregat hayot tsiklini modellashtirish uchun faqat domen hodisalaridan foydalanadi - agregat holatidagi har bir o'zgarish hodisa sifatida ifodalanishi shart. Har amal bir xil skript bo'yicha kechadi: agregatning hodisalari yuklanadi, ular holat ko'rinishiga proyeksiya qilinadi (biznes qarorini qabul qilish uchun), agregat buyruq bajaradi va natijada yangi hodisalar chiqadi, keyin yangi hodisalar event store ga commit qilinadi. Shunda haqiqat manbai hodisalar oqimi bo'ladi, holat esa undan hosil qilinadi. Khononov buni tanlash uchun aniq mezon beradi: subdomen pul yoki moliyaviy tranzaksiyalarni kuzatsa, izchil audit log berishga majbur bo'lsa, yoki biznes tizim xatti-harakatining chuqur tahlilini talab qilsa, shu pattern tanlanadi. Narxi ham bor: Khononov ta'kidlaydiki, bu pattern CQRS ni talab qiladi, aks holda tizim so'rov imkoniyatlarida juda cheklangan bo'lib qoladi va faqat ID bo'yicha bitta nusxani olishga qodir bo'ladi. Event sourcing mexanikasining to'liq yozuvi [hodisalarni saqlash](12-arxitektura-uslublari.md#1211-hodisalarni-saqlash-event-sourcing) da, o'qish modelini ajratish esa [buyruq va so'rovlar mas'uliyatini ajratish](12-arxitektura-uslublari.md#1210-buyruq-va-sorovlar-masuliyatini-ajratish-cqrs---command-query-responsibility-segregation) da.

**Spring'da qayerda uchraydi:** Spring'da tayyor event store yo'q, shuning uchun ikki yo'l bor: Axon Framework yoki shunga o'xshash kutubxona, yoki JPA/JDBC ustida o'zi yozilgan hodisa jadvali (`aggregate_id`, `version`, `event_type`, `payload`) va optimistik qulf uchun `version` ustuni. Snapshot (ma'lum versiyadagi holatni saqlash) uzun oqimlarda yuklashni tezlashtiradi. O'qish modeli alohida jadval yoki proyeksiya bo'ladi va uni hodisa tinglovchisi yangilaydi.

**Qo'llanish keyslari:**
- To'lov va hisob-kitob subdomen'ida har o'zgarishni hodisa sifatida saqlab, audit logni bepul olish.
- Ticket hayot tsiklini hodisalar bilan modellashtirib, holat o'tishlarining sababini saqlash.
- Qoidalar o'zgarganda o'tgan hodisalarni qayta proyeksiya qilib, yangi hisobot olish.
- Muayyan vaqtdagi holatni tiklab, bahsli operatsiyani tekshirish.
- Uzun oqimlar uchun snapshot joriy qilib, yuklash vaqtini qisqartirish.

**Ehtiyot bo'ling:** Hodisa sxemasi o'zgarishi eng og'ir masala: hodisalar o'zgarmas va abadiy, shuning uchun versiyalash va upcasting strategiyasini boshida belgilash kerak. Khononov ning mezonini chetlab o'tib, barcha subdomen'larga shu patternni qo'llash esa oddiy CRUD ni ham qimmat qiladi: supporting subdomain uchun [faol yozuv](09-malumotlarga-kirish-va-orm-patternlari.md#95-faol-yozuv-active-record) yetarli. Shuningdek hodisalardan shaxsiy ma'lumotni o'chirish talabi (GDPR) oddiy `delete` bilan hal bo'lmaydi va alohida loyihalashtirishni talab qiladi.

```java
// Hodisa manbali agregat: holat hodisalardan proyeksiya qilinadi
public final class Ticket {
    private final List<DomainEvent> newEvents = new ArrayList<>();
    private TicketState state = new TicketState();

    public Ticket(List<DomainEvent> history) { history.forEach(this::apply); }

    public void requestEscalation(EscalationReason reason) {
        if (state.escalated() || state.remainingTimePercentage() > 0) return;
        record(new TicketEscalated(state.id(), reason));
    }

    private void record(DomainEvent event) { newEvents.add(event); apply(event); }
    private void apply(DomainEvent event) { state = state.with(event); }
    public List<DomainEvent> newEvents() { return List.copyOf(newEvents); }
}
// Khononov misoli C# da; bu yerda g'oya Java ga o'tkazilgan:
// `dynamic` dispatch o'rniga `TicketState.with(event)` ishlatilgan.
```

## 13.58 Model tarjimasi (Model Translation)

**Tavsif:** Khononov 9-bobda anti-corruption layer va open-host service ning umumiy mexanikasini alohida ko'rib chiqadi, chunki tarjima mantiqi ikkisida ham bir xil: faqat yo'nalish farq qiladi - downstream kontekst upstream modelni o'ziga moslashtiradi (ACL), upstream kontekst esa o'z iste'molchilarini implementatsiya modelidagi o'zgarishlardan integratsiyaga xos published language bilan himoyalaydi (OHS). Tarjima mantiqi holatsiz yoki holatli bo'ladi. Holatsiz tarjima so'rov kelganda yoki chiqarilganda joyida bajariladi va proxy shaklida yoziladi: sinxron muloqotda transformatsiya kontekstning o'z kodida yoki API gateway kabi tashqi komponentda, asinxron muloqotda esa manba kontekstdan xabarlarga obuna bo'lgan message proxy orqali. Khononov asinxron tarjimaning muhim rolini ta'kidlaydi: domen hodisalarini aynan o'zi e'lon qilish keng tarqalgan xato, chunki u kontekstning implementatsiya modelini tashqariga ochadi; tarjima esa ichki (private) va integratsiyaga mo'ljallangan (public) hodisalarni ajratish imkonini beradi. Holatli tarjima manba ma'lumotini agregatlash yoki bir necha manbadan ma'lumotni bitta modelga birlashtirish kerak bo'lganda talab qiladi va o'z saqlash joyiga ega bo'ladi; API gateway bilan bunday tarjimani qilish mumkin emas. Khononov bir necha downstream kontekst foydalanadigan umumiy ACL ni alohida "interchange context" deb nomlaydi.

**Spring'da qayerda uchraydi:** Sinxron holatsiz tarjima uchun adapter sinfi va `RestClient`/`WebClient`, yoki Spring Cloud Gateway orqali tashqi tarjima. Asinxron holatsiz tarjima uchun Kafka Streams yoki Spring Integration `Transformer` bilan ichki hodisani public hodisaga aylantirish. Holatli tarjima uchun o'z jadvali va Kafka Streams state store yoki oddiy JPA jadval; batch yig'ish uchun Spring Batch yoki vaqt oynasi bilan agregatsiya.

**Qo'llanish keyslari:**
- Legacy SOAP xizmatini adapter orqali domen modeliga tarjima qilib, domenni XML shaklidan ozod qilish.
- Ichki domen hodisalarini public integratsiya hodisalariga aylantiruvchi message proxy yozish.
- Bir nechta iste'molchi uchun umumiy ACL ni alohida xizmat (interchange context) qilib chiqarish.
- API gateway'da published language ning bir necha versiyasini parallel saqlash.
- Mayda hodisalarni vaqt oynasida yig'ib, bitta birlashtirilgan hodisa chiqarish.

**Ehtiyot bo'ling:** Tarjima qatlamiga biznes mantiq kirib ketishi eng tez-tez uchraydigan muammo: adapter faqat shaklni o'zgartirishi kerak, qoida domen ichida qolishi lozim. Holatli tarjimani esa yengil deb o'ylamang: u o'z bazasi, idempotentlik va qayta tiklash mantiqini talab qiladi, ya'ni amalda alohida xizmat bo'ladi. Shuningdek API gateway'ga tarjimani chiqarish qulay bo'lsa ham, u bilan agregatsiya qilinmaydi va murakkab tarjimani gateway konfiguratsiyasiga siqishga urinish kuzatib bo'lmaydigan tizim beradi.

```java
// ACL adapteri: faqat shaklni tarjima qiladi, qoida domenda qoladi
@Component
class LegacyCustomerAdapter implements CustomerDirectory {
    private final RestClient legacy;

    LegacyCustomerAdapter(RestClient legacy) { this.legacy = legacy; }

    @Override
    public Customer findById(CustomerId id) {
        LegacyCustomerRecord raw = legacy.get()
                .uri("/CUST_GET?ID={id}", id.value())
                .retrieve().body(LegacyCustomerRecord.class);
        return new Customer(                       // domen modeliga tarjima
                new CustomerId(raw.custNo()),
                new PersonName(raw.fName(), raw.lName()),
                new Address(raw.addr1(), raw.city(), raw.cntry()));
    }
}
```

## 13.59 Biznes logika shaklini tanlash evristikasi (Business Logic Implementation Patterns Heuristic)

**Tavsif:** Khononov 10-bobda to'rt xil biznes logika shakli orasidan tanlash uchun aniq evristika beradi va uni qarorlar daraxti sifatida ko'rsatadi. Savollar tartibi muhim: subdomen pul yoki moliyaviy tranzaksiyalarni kuzatadimi, izchil audit log berishi shartmi yoki biznes uning xatti-harakatining chuqur tahlilini talab qiladimi - shunda hodisa manbali domen modeli; aks holda biznes logikasi murakkabmi - shunda domen modeli; aks holda ma'lumot strukturalari murakkabmi - shunda active record; aks holda transaction script. Murakkab va oddiy mantiq farqi uchun ham evristika bor: murakkab mantiq chigal biznes qoidalari, invariantlar va algoritmlarni o'z ichiga oladi, oddiy yondashuv esa asosan kirishni validatsiya qilish atrofida aylanadi; yana bir mezon - umumiy tilning o'zi asosan CRUD amallarini tasvirlaydimi yoki murakkabroq biznes jarayon va qoidalarni. Arxitektura patterni esa shundan keyin o'zi kelib chiqadi: hodisa manbali domen modeli CQRS ni talab qiladi, domen modeli ports and adapters ni talab qiladi (aks holda qatlamli arxitekturada agregat va value object'ni persistence'dan bexabar qilish qiyin), active record qatlamli arxitektura va qo'shimcha application qatlami bilan yaxshi yuradi, transaction script esa minimal uch qatlam bilan. Test strategiyasi ham shu zanjirga ulanadi: domen modeli uchun test piramidasi, active record uchun test olmosi, transaction script uchun teskari piramida. Khononov oxirida ogohlantiradi: bular qoida emas, evristika, va ularning foydali tomoni yana bitta - tanlangan pattern subdomen turi haqidagi taxminni tekshiradi, chunki core deb o'ylangan subdomen uchun active record yetarli bo'lsa, taxminni qayta ko'rish kerak.

**Spring'da qayerda uchraydi:** Har bir shaklning korpusdagi uy-bo'limi bor: [tranzaksiya skripti](08-biznes-logika-va-service-qatlam-patternlari.md#81-tranzaksiya-skripti-transaction-script), [faol yozuv](09-malumotlarga-kirish-va-orm-patternlari.md#95-faol-yozuv-active-record), [domen modeli](08-biznes-logika-va-service-qatlam-patternlari.md#82-domen-modeli-domain-model) va [hodisalarni saqlash](12-arxitektura-uslublari.md#1211-hodisalarni-saqlash-event-sourcing). Arxitektura tomonida [olti burchakli arxitektura](12-arxitektura-uslublari.md#122-olti-burchakli-arxitektura-hexagonal-architecture--ports--adapters) va qatlamli arxitektura, test tomonida esa [test piramidasi variantlari](../testing/02-test-piramidasi-va-test-turlari-xaritasi.md#22-zamonaviy-variantlar-testing-trophy-honeycomb-test-diamond) bu tanlovga mos keladi.

**Qo'llanish keyslari:**
- Yangi modul boshlashda avval subdomen turini aniqlab, keyin patternni daraxt bo'yicha tanlash.
- Audit talabi paydo bo'lganda domen modelidan hodisa manbali modelga o'tish qarorini asoslash.
- Core deb hisoblangan modul uchun transaction script yetarli chiqsa, subdomen bahosini qayta ko'rish.
- Test strategiyasini tanlangan pattern bilan birga belgilab, test turlari nisbatini rejalashtirish.
- CQRS ni hodisa manbali model bo'lmagan modulda ham bir necha o'qish modeli kerak bo'lsa qo'llash.

**Ehtiyot bo'ling:** Khononov o'zi aytganidek, bu daraxt uning oddiy asbobni afzal ko'rish moyilligiga asoslangan va har qoidaning istisnosi bor: hodisa manbali modelda katta tajribaga ega jamoa uchun uni hamma joyda ishlatish oddiyroq bo'lishi mumkin. Shuning uchun daraxtni tanqidiy fikrlash o'rniga qo'yish xato. Ikkinchi tuzoq - bitta tizimda bitta shaklni hamma modulga majburlash: tanlov subdomen darajasida qilinadi.

```text
# Khononov ning taktik qarorlar daraxti (10-bob), qisqartirilgan shaklda

pul / audit / chuqur tahlil kerakmi? -> ha  -> Event-Sourced Domain Model + CQRS
                                     -> yo'q
  biznes logikasi murakkabmi?        -> ha  -> Domain Model + Ports & Adapters
                                     -> yo'q                (test: piramida)
    ma'lumot strukturasi murakkabmi? -> ha  -> Active Record + Layered + service qatlami
                                     -> yo'q                (test: olmos)
                                             Transaction Script + minimal Layered
                                                            (test: teskari piramida)
```

## 13.60 Dizayn qarorlari evolyutsiyasi (Evolving Design Decisions)

**Tavsif:** Khononov 11-bobda DDD qarorlari bir marta qabul qilinmasligini ko'rsatadi va o'zgarishning to'rtta eng ko'p uchraydigan vektorini sanaydi: biznes domeni, tashkiliy struktura, domen bilimi va o'sish. Birinchi vektor subdomen turlarining almashuvida ko'rinadi va Khononov oltita o'tishni misol bilan beradi: core dan generic ga (raqobatchi shu funksiyani tayyor xizmat sifatida chiqarsa, ustunlik tovarga aylanadi), generic dan core ga (tayyor yechim o'rniga o'z tizimini qurish qaroriga misol Amazon ning infratuzilmasi va keyinchalik AWS), supporting dan generic ga, supporting dan core ga (belgisi - supporting subdomen mantiqining murakkablashishi; agar bu foydaga ta'sir qilmasa, u shunchaki tasodifiy murakkablik), core dan supporting ga va generic dan supporting ga. Ikkinchi vektor jamoa joylashuvi va muloqot darajasi o'zgarganda integratsiya patternini o'zgartiradi: partnership dan customer-supplier ga, customer-supplier dan separate ways ga, hamda o'sayotgan jamoalar tufayli keng bounded context'ning bo'linishi. Uchinchi vektor bo'yicha evristika shunday: domen mantiqi noaniq va tez o'zgarganda bounded context'lar kengroq chegaralar bilan loyihalashtiriladi, keyin bilim yig'ilgan va o'zgarishlar barqarorlashgan sari ular torroq kontekstlarga yoki mikroservislarga bo'linadi. To'rtinchi vektor o'sish: funksiyani dizayn qarorlarini qayta ko'rmasdan kengaytirish [katta loy to'pi](12-arxitektura-uslublari.md#1223-katta-loy-topi-big-ball-of-mud---anti-pattern) ga olib keladi, shuning uchun boshqaruv printsipi - eskirgan dizayn qarorlari tufayli paydo bo'lgan tasodifiy murakkablikni aniqlab, olib tashlash.

**Spring'da qayerda uchraydi:** Kengroq moduldan torroq modullarga o'tish Spring Modulith'da paket bo'lish va `ApplicationModules.verify()` qoidalarini yangilash sifatida ko'rinadi. Generic subdomen tashqi xizmatga chiqarilganda uning o'rnida anti-corruption layer adapteri qoladi; core ga aylangan subdomen esa aksincha, o'z moduliga ajratiladi va domen modeli bilan boyitiladi. Integratsiya patterni o'zgarishi amalda shared kernel moduliga bog'liqlikni olib tashlash va kontrakt testlariga o'tish bilan ifodalanadi.

**Qo'llanish keyslari:**
- Raqobatchi tayyor xizmat chiqarganda o'z yechimini generic subdomen deb qayta baholash va adapterga o'tish.
- Yangi jamoa qo'shilganda keng bounded context'ni ikki kontekstga bo'lib, egalikni ajratish.
- Jamoalar o'rtasidagi muloqot buzilganda partnership dan customer-supplier ga rasmiy o'tish.
- Supporting modul mantiqi murakkablashganda uning foydaga ta'sirini tekshirib, turini qayta aniqlash.
- Domen bilimi yetarli bo'lmaganida kengroq kontekstdan boshlab, keyin bo'lishni rejalashtirish.

**Ehtiyot bo'ling:** Khononov ta'kidlaydi: bounded context chegaralarini refactoring qilish qimmat va ko'p holatda samarasiz chegaralar shunchaki e'tiborsiz qolib, texnik qarz yig'adi; shuning uchun erta bo'linishdan qochish arzonroq, chunki mantiqiy chegaralarni refactoring qilish fizik chegaralarni refactoring qilishdan ancha arzon. Shuningdek domen bilimining yo'qolishi ham real xavf: hujjat eskiradi, odamlar ketadi, va Khononov bilimni tiklash uchun event storming workshopini tavsiya qiladi.

```text
# Subdomen turi o'zgarsa, pattern va integratsiya ham o'zgaradi

core -> generic      o'z yechimi tashqi xizmatga, o'rnida anti-corruption layer qoladi
generic -> core      tayyor xizmat o'rniga o'z moduli, domen modeli bilan boyitiladi
supporting -> core   mantiq murakkablashdi va foydaga ta'sir qiladi: pattern kuchayadi
partnership -> customer-supplier    jamoa boshqa joyga ko'chdi, muloqot pasaydi
customer-supplier -> separate ways  integratsiya narxi takrorlashdan qimmat bo'ldi
keng bounded context -> ikki kontekst   yangi jamoa qo'shildi, egalik ajratildi
```
## 13.61 Analiz patternlarini qo'llash (Applying Analysis Patterns)

**Tavsif:** Evans 11-bobda boshqa loyihada sinalgan tayyor modelni o'z domeniga olib kirishni ko'rib chiqadi va Martin Fowler ning *Analysis Patterns* kitobidagi ta'rifga tayanadi: analiz patterni biznes modellashtirishda takrorlanadigan qurilishni ifodalovchi tushunchalar guruhi. U texnologiya yechimi emas va qutidan chiqqanicha ishlamaydi: boshlang'ich nuqta, undan keyin refactoring va tajriba davom etadi. Evans misolida dasturchilar hisob-kitob bobidan Account, Entry va Transaction tushunchalarini oladi; domen eksperti bilan muhokamada Transaction mos kelmasligi ma'lum bo'ladi, chunki to'lov hisoblangan foizdan kech kelishi mumkin. Transaction tashlanadi, Account va Entry qoladi, muhokamadan esa yangi atama "accrual" umumiy tilga kiradi. Evans bitta qat'iy qoida qo'yadi: taniqli patterndan atama olinsa, tashqi shakl qancha o'zgarsa ham atama ortidagi asosiy tushuncha buzilmasin; ma'no o'zgargan bo'lsa, nom ham o'zgartiriladi. Sababi ikkita: pattern o'zida keyingi og'riqdan qutqaradigan tushunchani saqlaydi va keng tanilgan atama [umumiy til](#131-umumiy-til-ubiquitous-language) ni boyitadi.

**Spring'da qayerda uchraydi:** Tayyor model loyihaga ko'pincha kod bilan keladi: ikki yozuvli hisob kutubxonasi, tayyor sxema yoki ochiq kodli domen moduli. Atama domen paketiga faqat ma'nosi bilan birga ko'chadi; tashqi kutubxonaning turlari domenga kirib kelmasligi uchun [buzilishdan himoya qatlami](#137-buzilishdan-himoya-qatlami-anti-corruption-layer) ishlatiladi, almashtirish esa [chuqur tushunchaga qarab refactoring](#1343-chuqur-tushunchaga-qarab-refactoring-refactoring-toward-deeper-insight) sikli bilan boriladi.

**Qo'llanish keyslari:**
- Hisob-kitob yoki ombor kabi yaxshi o'rganilgan domenda modelni noldan o'ylash o'rniga tayyor modeldan boshlash.
- Tayyor modelni domen eksperti bilan muhokama qilib, mos kelmaydigan tushunchani olib tashlash.
- Muhokamada chiqqan yangi atamani umumiy tilga va sinf nomiga kiritish.

**Ehtiyot bo'ling:** Tayyor modelni ko'r-ko'rona olish eng keng tarqalgan xato: Evans uni qutidan chiqqan yechim emas deb ataydi, u faqat izlanishga yo'naltiruvchi ko'rsatma beradi. Teskari xato - atamani olib, ma'nosini o'zgartirib qo'yish: shunda kod kitobda tasvirlangan tushunchani anglatmaydi. Tayyor model izlash ishni boshlashni to'sib qo'ysa, bu [tahlil falaji](25-anti-patternlar.md#2577-tahlil-falaji-analysis-paralysis) ga aylanadi.

```java
// Kitobdagi atama saqlanadi, mos kelmagan tushuncha (Transaction) olinmaydi
public sealed interface Entry permits Accrual, Payment { Money amount(); }

record Accrual(Money amount, LocalDate date) implements Entry { }  // yangi atama
record Payment(Money amount, LocalDate date) implements Entry { }

record Account(AccountId id, List<Entry> entries) {
    Money balance() {   // balans yozuvlardan chiqadi, Transaction juftligi kerak emas
        return entries.stream().map(Entry::amount).reduce(Money.ZERO, Money::plus);
    }
}
```

## 13.62 Strategiyani birga yig'ish (Bringing the Strategy Together)

**Tavsif:** Evans 17-bobda strategik patternlarni alohida emas, birga qo'llash tartibini beradi. Uch asosiy printsip - kontekst, [distillation](#1345-distillation-distillation) va [katta masshtabli struktura](#1351-katta-masshtabli-struktura-large-scale-structure) - bir-birining o'rnini bosmaydi, to'ldiradi: struktura bitta bounded context ichida ham yashashi mumkin, [kontekst xaritasi](#133-kontekst-xaritasi-context-map) ni butun loyiha bo'ylab tashkil qilishi ham mumkin. Legacy tizim tanlangan strukturaga mos tuzilmagan bo'lsa, struktura tashlanmaydi: legacy ning struktura ichidagi haqiqiy o'rni tan olinadi va uning xizmatlari faqat bir necha qatlamga tegishli ekani legacy rolini qisqa tasvirlaydi. Ish baholashdan boshlanadi, Evans buni "assessment first" deb qo'yadi: avval mavjud holat haqida aniq javob olinadi, keyin nima eng shoshilinch ekani ko'rinadi. Strategiyani kim belgilashi ham patternning qismi: yuqoridan beriladigan arxitektura kam ishlaydi, ishlaydigan ikki uslub bor - struktura ilova jamoasida [rivojlanuvchi tartib](#1352-rivojlanuvchi-tartib-evolving-order) bilan o'sishi, yoki ilovaga yo'naltirilgan arxitektura jamoasi ilova jamoalari bilan teng hamkor bo'lishi. Qaror samarali bo'lishi uchun Evans shartlar qo'yadi: butun jamoaga yetib borishi, feedbackni singdirishi, evolyutsiyaga ruxsat berishi, eng kuchli dasturchilarni ilova jamoalaridan tortib ketmasligi, minimalizm bilan yozilishi.

**Spring'da qayerda uchraydi:** Baholash natijasi kod repozitoriysida yashaydi: kontekst xaritasi va [domen qarashlari bayonoti](#1346-domen-qarashlari-bayonoti-domain-vision-statement) core modul `README.md` sida, struktura qoidasi esa ArchUnit yoki Spring Modulith testida. Shunda struktura hujjat emas, bajariladigan qoida bo'ladi va uni o'zgartirish pull request ichida ko'rinadi.

**Qo'llanish keyslari:**
- Yangi loyihada strategik dizaynni oltita baholash savoliga javob yozishdan boshlash.
- Struktura bitta kontekst ichida qolishi yoki kontekst xaritasini tashkil qilishi haqidagi qarorni ADR da yozib qo'yish.
- Legacy tizimni strukturadagi aniq qatlamga joylab, uning rolini bir gapda tasvirlash.

**Ehtiyot bo'ling:** Evans eng katta xavf sifatida ortiqcha qurilgan strukturani ko'rsatadi: deyarli har qanday qoida kimningdir yo'lini to'sadi, shuning uchun dizayn aniqligini oshirmagan qoida olib tashlanadi. Ikkinchi tuzoq - eng kuchli dasturchilarni arxitektura jamoasiga yig'ib, ilovani zaif jamoa qo'lida qoldirish. Uchinchisi - strategiyani bir marta yozib qotirib qo'yish: u feedback bilan o'zgarmasa, jamoa uni chetlab o'tadi.

```text
# Evans ning "assessment first" savollari (17-bob), strategiyani boshlash tartibi

1. Kontekst xaritasini chizish: u izchil chiqadimi yoki noaniq joylar bormi?
2. Loyihadagi tilga qarash: umumiy til bormi, u ishni yengillatishga yetarlimi?
3. Nima muhimini tushunish: core domain aniqlanganmi, qarashlar bayonoti bormi?
4. Texnologiya model asosidagi dizaynga yordam beradimi yoki qarshi turadimi?
5. Jamoada kerakli texnik ko'nikma bormi?
6. Dasturchilar domenni bilishadimi, ular domenga qiziqadimi?
```

## 13.63 Amalda qo'llash

- [ ] Domen tilidagi atamalarni ro'yxat qiling va kodda boshqa nom bilan atalganlarini toping.
- [ ] Har bir agregat uchun invariantni bir gapda yozing va u qayerda majburlanayotganini ko'rsating.
- [ ] Agregat chegarasidan tashqariga chiqadigan tranzaksiyalarni toping - bitta tranzaksiya bitta agregatni o'zgartirishi kerak.
- [ ] Qiymat obyekti bo'lishi kerak bo'lgan primitivlarni toping (pul, email, telefon, ID) va ularni `record` ga o'tkazish rejasini tuzing.
- [ ] Bounded context chegaralarini chizib, kontekstlar o'rtasidagi har bir integratsiya uchun anti-corruption layer kerakligini qaror qiling.
- [ ] Domen hodisalarini sanab chiqing va har birining nomi o'tgan zamonda ekanini tasdiqlang.
- [ ] Repository interfeyslari domen paketida, implementatsiyasi infratuzilmada turganini tekshiring.
- [ ] Domen paketida `jakarta.persistence`, Jackson va Spring web importlarini qidirib, topilganlarini ro'yxat qiling.

## Manbalar

- Eric Evans, *Domain-Driven Design: Tackling Complexity in the Heart of Software*, Addison-Wesley, 2004, 2-bob (UBIQUITOUS LANGUAGE) - 13.1 dagi umumiy til patterni va uning nomi
- Eric Evans, *Domain-Driven Design*, Addison-Wesley, 2004, 3-bob (MODEL-DRIVEN DESIGN, HANDS-ON MODELERS) - 13.36 va 13.37; shu bobda analiz modeli va dizaynning ajralishi "o'limga olib boruvchi bo'linish" deb ataladi va "dasturchilar modelchi" xulosasi beriladi
- Eric Evans, *Domain-Driven Design*, Addison-Wesley, 2004, 4-bob (SMART UI ANTI-PATTERN) - 13.38; Evans "anti-pattern" nomini yarim hazil deb aytadi va patternni oddiy loyiha uchun o'zaro inkor etuvchi, lekin to'g'ri tanlov deb beradi
- Eric Evans, *Domain-Driven Design*, Addison-Wesley, 2004, 10-bob (ASSERTIONS, CONCEPTUAL CONTOURS, Declarative Design) - 13.40, 13.41 va 13.42; Assertions "design by contract" maktabiga va [Meyer 1988] ga ishora qiladi, Conceptual Contours esa Ward Cunningham ning WHOLE VALUE patterniga
- Eric Evans, *Domain-Driven Design*, Addison-Wesley, 2004, III qism nomi "Refactoring Toward Deeper Insight" va 8-bob (Breakthrough) - 13.43 va 13.44; shu bobda sakrash rejalashtirilmasligi va "Focus on Basics" maslahati beriladi
- Eric Evans, *Domain-Driven Design*, Addison-Wesley, 2004, 14-bob (CONTINUOUS INTEGRATION) - 13.39; Evans uni model butunligi ma'nosida beradi, ikki darajani (tushuncha va implementatsiya) ajratadi va faqat bitta bounded context ichida zarur deb cheklaydi
- Eric Evans, *Domain-Driven Design*, Addison-Wesley, 2004, 15-bob (DOMAIN VISION STATEMENT, HIGHLIGHTED CORE, COHESIVE MECHANISMS, SEGREGATED CORE, ABSTRACT CORE) - 13.45, 13.46, 13.47, 13.48, 13.49 va 13.50; shu bobda distillashning beshta foydasi va Segregated Core ning to'rt qadami sanaladi
- Eric Evans, *Domain-Driven Design*, Addison-Wesley, 2004, 16-bob (EVOLVING ORDER, SYSTEM METAPHOR, RESPONSIBILITY LAYERS, KNOWLEDGE LEVEL, PLUGGABLE COMPONENT FRAMEWORK) - 13.51, 13.52, 13.53, 13.54, 13.55 va 13.56; Responsibility Layers uchun RELAXED LAYERED SYSTEM varianti ko'rsatiladi, Knowledge Level esa Martin Fowler ning *Analysis Patterns* kitobidan olinadi
- Eric Evans, *Domain-Driven Design*, Addison-Wesley, 2004, 11-bob (APPLYING ANALYSIS PATTERNS) - 13.61; analiz patterni ta'rifi Martin Fowler ning *Analysis Patterns* kitobidan keltiriladi, Evans uni qutidan chiqqan yechim emas deb belgilaydi va Account, Entry, Transaction hamda Posting Rule misollarini shu bobda beradi; atamani olib ma'nosini saqlash qoidasi ham shu bobning xulosasi
- Eric Evans, *Domain-Driven Design*, Addison-Wesley, 2004, 17-bob (Assessment First, Who Sets the Strategy) - 13.62; uch strategik printsipning bir-birini to'ldirishi, legacy ning struktura ichidagi o'rni, oltita baholash savoli va strategik qaror uchun qo'yilgan shartlar shu bobda
- Vlad Khononov, *Learning Domain-Driven Design*, O'Reilly, 2021, 7-bob (108-112) - hodisa manbali domen modeli, agregat amalining to'rt qadamli skripti va bu patternning CQRS ni talab qilishi (13.57)
- Vlad Khononov, *Learning Domain-Driven Design*, O'Reilly, 2021, 9-bob (137-143) - model tarjimasi: holatsiz va holatli tarjima, proxy va message proxy, private va public hodisalar farqi, interchange context atamasi (13.58)
- Vlad Khononov, *Learning Domain-Driven Design*, O'Reilly, 2021, 10-bob (160-167) - biznes logika shaklini tanlash evristikasi, arxitektura patterni va test strategiyasi zanjiri, taktik qarorlar daraxti (13.59)
- Vlad Khononov, *Learning Domain-Driven Design*, O'Reilly, 2021, 11-bob (169-182) - o'zgarishning to'rt vektori, subdomen turlarining oltita o'tishi, partnership dan customer-supplier va customer-supplier dan separate ways ga o'tish, keng chegaradan boshlash evristikasi (13.60)
- Eric Evans, *Domain-Driven Design*, Addison-Wesley, 2004, 4-bob (LAYERED ARCHITECTURE) - 13.34 dagi to'rt qatlam nomi (User Interface, Application, Domain, Infrastructure) va 13.19 dagi ilova qatlamining roli
- Eric Evans, *Domain-Driven Design*, Addison-Wesley, 2004, 5-bob (ENTITIES AKA REFERENCE OBJECTS, VALUE OBJECTS, SERVICES, MODULES AKA PACKAGES) - 13.13, 13.14, 13.18 va 13.21 dagi pattern nomlari
- Eric Evans, *Domain-Driven Design*, Addison-Wesley, 2004, 6-bob (AGGREGATES, FACTORIES, REPOSITORIES) - 13.15, 13.16, 13.17 va 13.24; shu bobda invariant har bir tranzaksiya tugashida majburlanadi va agregat ichidagi obyektning boshqa agregat ildiziga havola ushlashi taqiqlanmaydi
- Eric Evans, *Domain-Driven Design*, Addison-Wesley, 2004, 9-bob (SPECIFICATION) - 13.22 dagi uchta qo'llanish: validatsiya, tanlash va buyurtmaga yaratish (building-to-order)
- Eric Evans, *Domain-Driven Design*, Addison-Wesley, 2004, 10-bob (INTENTION REVEALING INTERFACES, SIDE-EFFECT-FREE FUNCTIONS, ASSERTIONS, CONCEPTUAL CONTOURS, STANDALONE CLASSES, CLOSURE OF OPERATIONS, Declarative Design) - 13.26, 13.27, 13.28, 13.29 va 13.30 dagi Supple Design tarkibi
- Eric Evans, *Domain-Driven Design*, Addison-Wesley, 2004, 12-bob (STRATEGY AKA POLICY) - 13.23 dagi Policy nomi va uning Strategy bilan bog'liqligi
- Eric Evans, *Domain-Driven Design*, Addison-Wesley, 2004, 14-bob (BOUNDED CONTEXT, CONTEXT MAP, SHARED KERNEL, CUSTOMER/SUPPLIER DEVELOPMENT TEAMS, CONFORMIST, ANTICORRUPTION LAYER, SEPARATE WAYS, OPEN HOST SERVICE, PUBLISHED LANGUAGE) - 13.2-13.10 dagi strategik pattern nomlari; shu ro'yxatda Partnership va Domain Event yo'q
- Eric Evans, *Domain-Driven Design*, Addison-Wesley, 2004, 15-bob (CORE DOMAIN, GENERIC SUBDOMAINS) - 13.12; Evans da faqat shu ikki nom bor, "supporting subdomain" nomi yo'q
- Eric Evans, *Domain-Driven Design*, Addison-Wesley, 2004, IV qism nomi "Strategic Design" - kirishdagi "strategik" atamasining Evans dagi manbasi; "tactical design" iborasi esa kitob matnida uchramaydi
- Vlad Khononov, *Learning Domain-Driven Design*, O'Reilly, 2021, 1-bob (4-13) - core, generic va supporting subdomen turlari, ularning murakkablik va raqobat ustunligi bo'yicha solishtirilishi (13.12)
- Vlad Khononov, *Learning Domain-Driven Design*, O'Reilly, 2021, 3-bob (35-41) - bounded context va subdomen farqi, umumiy tilning kontekst ichida aniqlanishi (13.1, 13.2)
- Vlad Khononov, *Learning Domain-Driven Design*, O'Reilly, 2021, 4-bob (49-59) - Partnership, Shared Kernel, Customer-Supplier, Conformist, Anticorruption Layer, Open-Host Service, Separate Ways va Context Map (13.3-13.11); Partnership nomining manbasi aynan shu bob
- Vlad Khononov, *Learning Domain-Driven Design*, O'Reilly, 2021, 5-bob (69-72) - Active Record va "anemik domen modeli antipatterni" atamasiga e'tiroz (13.31)
- Vlad Khononov, *Learning Domain-Driven Design*, O'Reilly, 2021, 6-bob (75-96, xususan 87) - domen modeli qurilish bloklari va "bir tranzaksiyaga bitta agregat nusxasi" qoidasi (13.15, 13.25); domen servisi bu qoidadan chetlab o'tish yo'li emas (13.18)
- Vlad Khononov, *Learning Domain-Driven Design*, O'Reilly, 2021, 8-bob (117-134) - Layered Architecture, Ports & Adapters va Dependency Inversion Principle (13.34)
- Vlad Khononov, *Learning Domain-Driven Design*, O'Reilly, 2021, 12-bob (185-195) - EventStorming: o'nta qadam, stiker rang konvensiyasi va texnikaning Alberto Brandolini ga tegishliligi (13.23, 13.32)
- Vlad Khononov, *Learning Domain-Driven Design*, O'Reilly, 2021, 14-bob (225-229) - mikroservis va bounded context munosabati nosimmetrik: har bir mikroservis bounded context, har bir bounded context mikroservis emas; servis chegarasi uchun subdomen muvozanatli evristika (13.2, 13.12)
- Vlad Khononov, *Learning Domain-Driven Design*, O'Reilly, 2021, II qism nomi "Tactical Design" - kirishdagi "taktik" atamasining manbasi
- Chris Richardson, *Microservices Patterns*, Manning, 2019, 2-bob (53-56) - `Decompose by subdomain` patterni: servisni subdomen chegarasiga moslash (13.12)
- Chris Richardson, *Microservices Patterns*, Manning, 2019, 5-bob (156-158, `Aggregate rules`) - uchta qoida: tashqaridan faqat agregat ildiziga havola, agregatlar orasida birlamchi kalit bilan havola, bitta tranzaksiya bitta agregatni yaratadi yoki o'zgartiradi (13.15, 13.25)
- Chris Richardson, *Microservices Patterns*, Manning, 2019, 5-bob (152-160) - agregat chegarasi, agregat yirikligi va biznes mantiqini agregatlar bilan loyihalash (13.15)
- Chris Richardson, *Microservices Patterns*, Manning, 2019, 5-bob (160-182, `Publishing domain events`) - domen hodisasi nima, uni aniqlash, boyitish va chiqarish (13.20)
- Chris Richardson, *Microservices Patterns*, Manning, 2019, 4-bob (110-145) - saga va kompensatsiya tranzaksiyalari (13.25 dagi havola)
- Martin Fowler, *Patterns of Enterprise Application Architecture*, Addison-Wesley, 2003, 9-bob (109-141) - Transaction Script, Domain Model, Table Module va Service Layer aynan shu kitobda (13.19)
- Martin Fowler, *Patterns of Enterprise Application Architecture*, Addison-Wesley, 2003, 11-bob (183-213) - Unit of Work, Identity Map va Lazy Load: bu uchtasi faqat shu kitobda, Evans da yo'q (13.16)
- Martin Fowler, *Patterns of Enterprise Application Architecture*, Addison-Wesley, 2003, 13-bob (322-327) - Repository (Edward Hieatt va Rob Mee): Repository ning ikkinchi manbasi, Evans 6-bobi bilan birga (13.16)
- Martin Fowler, *Patterns of Enterprise Application Architecture*, Addison-Wesley, 2003, 18-bob (486-495) - Value Object va Money: valyutani miqdor bilan birga saqlash, yaxlitlashda tiyin yo'qolishi va `allocate` amali (13.14, 13.35)
- Robert C. Martin, *Clean Architecture*, Prentice Hall, 2017, 20-bob (Business Rules: Entities, Use Cases) - 13.19 va 13.34 dagi entity va use case mas'uliyatlarining ajratilishi
- ESLATMA: Evans kitobi uchun bet raqami yozilmadi. Repodagi nusxa 2003-yil aprel "Final Manuscript" bo'lib, uning betlari 2004-yilda chop etilgan nashr betlari bilan mos kelmaydi; shuning uchun iqtibos bob raqami va pattern nomi bilan beriladi
- ESLATMA: har bo'limdagi "Spring'da qayerda uchraydi" qismi va butun 13.33 (`AbstractAggregateRoot`, `@DomainEvents`) framework tafsiloti - yuqoridagi kitoblardan olingan emas
- ESLATMA: 13.63 dagi tekshiruv ro'yxati shu korpusning amaliy tavsiyasi, kitobdan olingan emas
- ESLATMA: 13.15 va 13.24 dagi kod misollaridagi aniq sonlar (masalan 100 qator chegarasi) namuna qiymatlar - kitoblarda agregat hajmi uchun bunday son yo'q
- ESLATMA: 13.61 dagi kod misoli Evans ning hisob-kitob modelidan (Account, Entry, Accrual) chiqarilgan Java shakli, kitobdagi diagramma yoki kodning ko'chirmasi emas
- ESLATMA: 13.57 dagi kod misoli Khononov kitobidagi C# misolining g'oyasi Java ga o'tkazilgan shakli, aynan ko'chirma emas
- ESLATMA: 13.36-13.56 dagi "Spring'da qayerda uchraydi" qismlari (Spring Modulith, jMolecules, ArchUnit, Spring Cloud Gateway, Axon) framework tafsiloti va Evans kitobidan olingan emas

---

[&larr; 12. Arxitektura uslublari](12-arxitektura-uslublari.md) · [Mundarija](README.md) · [14. Microservices patternlari &rarr;](14-microservices-patternlari.md)
