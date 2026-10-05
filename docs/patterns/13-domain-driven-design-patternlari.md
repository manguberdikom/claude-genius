<!-- doc: patterns | chapter: 13 | part:  -->

[Barcha hujjatlar](../../README.md) / [Dizayn patternlar](README.md)

> Holat: AI yozgan, inson tekshirmagan.

# 13. Domain-Driven Design patternlari (DDD Patterns)

<details>
<summary>Bu bo'limdagi 36 bo'lim</summary>

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
- [13.36 Amalda qo'llash](#1336-amalda-qollash)

</details>



Domain-Driven Design patternlari - bu kodni emas, balki biznes domenini va jamoalar o'rtasidagi chegaralarni modellashtirish haqidagi patternlar to'plami. Ular ikki qatlamga bo'linadi: strategik patternlar (Bounded Context, Context Map, Subdomain turlari, integratsiya munosabatlari) tizimni qanday bo'laklarga ajratish va bu bo'laklar o'zaro qanday gaplashishini belgilaydi; taktik patternlar (Aggregate, Entity, Value Object, Repository va boshqalar) esa bitta kontekst ichidagi model tuzilishini belgilaydi. Arxitektor uchun strategik qism ayniqsa muhim, chunki monolitni mikroservislarga ajratish, jamoa mas'uliyat chegaralarini belgilash va legacy tizimlar bilan integratsiya qarorlari aynan shu patternlar tilida qabul qilinadi. Spring ekotizimida bu patternlar Spring Modulith, jMolecules, Spring Cloud Contract va OpenAPI kabi vositalar yordamida kod darajasida majburlanadigan (enforceable) qoidalarga aylanadi.

## 13.1 Umumiy til (Ubiquitous Language)

**Tavsif:** Biznes ekspertlari, dasturchilar va testerlar bitta domen haqida bir xil atamalar bilan gapirishini ta'minlaydigan pattern. Muammo shundaki, biznes "buyurtma bekor qilindi" deydi, kod esa `OrderEntity.setStatus(4)` deb yozadi - natijada har bir muloqotda tarjima yuz beradi va tarjima paytida ma'no yo'qoladi. Yechim: domen atamalarini to'g'ridan-to'g'ri kod identifikatorlariga aylantirish - sinf, metod, event va API maydon nomlari biznes lug'ati bilan bir xil bo'ladi. Umumiy til har bir Bounded Context ichida alohida va o'ziga xos bo'ladi, global emas.

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

**Tavsif:** Domen modelining ma'noga ega bo'lgan aniq chegarasini belgilaydi: shu chegara ichida har bir atama bitta aniq ma'noga ega, chegaradan tashqarida esa boshqa model boshlanadi. Bu katta tizimda bitta yagona model qurish imkonsizligi muammosini hal qiladi - model o'sgani sari ichki qarama-qarshiliklar paydo bo'ladi. Amalda kontekst o'z modeli, o'z ma'lumotlar bazasi sxemasi va o'z jamoasiga ega bo'ladi; tashqi dunyo bilan faqat aniq belgilangan API yoki eventlar orqali gaplashadi. Mikroservis chegaralarini aniqlashda asosiy mezon aynan shu pattern.

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

**Ehtiyot bo'ling:** Kontekstni texnik qatlam (controller/service/repository) bo'yicha emas, biznes qobiliyati bo'yicha ajratish kerak - aks holda "distributed monolith" chiqadi. Juda mayda kontekstlar esa har bir use-case uchun 5-6 ta tarmoq chaqiruviga olib keladi; chegarani ma'lumot bir joyda o'zgarishi (tranzaksiya yaxlitligi) talab qiladigan joyda chizing.

## 13.3 Kontekst xaritasi (Context Map)

**Tavsif:** Tizimdagi barcha Bounded Context'larni va ular orasidagi munosabat turlarini (Shared Kernel, Customer-Supplier, Conformist, ACL, Open Host Service va h.k.) ko'rsatadigan xarita. Muammo: jamoalar o'z kontekstini biladi, lekin kim kimga qaram, kim upstream, kim downstream ekani hech qayerda yozilmagan - natijada har bir o'zgarish kutilmagan buzilishlarga olib keladi. Xarita texnik integratsiya emas, balki jamoalar o'rtasidagi siyosiy va tashkiliy munosabatni ham ko'rsatadi. Bu arxitektorning asosiy qaror qabul qilish artifacti.

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

**Tavsif:** Ikki yoki undan ko'p Bounded Context ataylab modelning kichik bir qismini - kod, sxema yoki umumiy value object'larni - birgalikda egallaydi va birgalikda boshqaradi. Bu takrorlanishni kamaytiradi, lekin juda qattiq bog'liqlik yaratadi: yadroni bir tomonlama o'zgartirish mumkin emas, har qanday o'zgarish barcha egalar bilan kelishiladi. Shuning uchun yadro iloji boricha kichik va barqaror bo'lishi kerak - odatda faqat o'zgarmas value object'lar va umumiy identifikatorlar.

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

**Tavsif:** Ikki kontekst o'rtasidagi upstream/downstream munosabati, bunda upstream (ta'minotchi) downstream (mijoz) ehtiyojlarini hisobga olishga majbur. Mijoz o'z talablarini aytadi, ta'minotchi ularni backlog'ga qo'shadi va o'zgarishlarni oldindan kelishib buzmasdan chiqaradi. Bu munosabatni ishlashiga olib keladigan asosiy mexanizm - avtomatlashtirilgan kontrakt testlari, ular upstream'ning CI'sida ishlab, mijozni buzadigan o'zgarishni darhol ushlaydi.

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

**Tavsif:** Downstream kontekst upstream modeliga hech qanday tarjimasiz, to'liq bo'ysunadi - uning DTO'lari, atamalari va hatto xato kodlarini o'ziga oladi. Bu upstream'ga ta'sir o'tkazish imkoni bo'lmaganda (tashqi vendor, yirik platforma, hukumat API'si) ongli ravishda tanlanadigan strategiya: tarjima qilish narxidan voz kechib, upstream model bilan yashashga kelishiladi. Afzalligi - tez va arzon integratsiya; narxi - upstream modelining nomukammalligi va o'zgarishlari to'g'ridan-to'g'ri ichki kodga kirib keladi.

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

**Tavsif:** Downstream kontekst bilan upstream o'rtasiga qo'yiladigan tarjima qatlami: tashqi modelni ichki domen modeliga va teskarisiga o'giradi, shu bilan tashqi tizimning "yomon" yoki o'zgaruvchan modeli ichki toza modelni ifloslantirmasligini ta'minlaydi. ACL adapter, facade va translator'lar to'plamidan iborat bo'lib, domen uchun faqat o'z tilida ifodalangan port interfeysini ko'rsatadi. Legacy tizimlar va strangler-fig migratsiyalarida bu asosiy himoya mexanizmi.

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

**Tavsif:** Upstream kontekst o'z imkoniyatlarini bir nechta iste'molchi uchun mo'ljallangan, barqaror va yaxshi hujjatlashtirilgan protokol orqali taqdim etadi. Har bir yangi mijoz uchun maxsus integratsiya yozish o'rniga, bitta umumiy "host" API quriladi va u ichki modeldan ataylab ajratiladi. OHS odatda Published Language bilan birga keladi: interfeys ochiq, undagi ma'lumot formati esa e'lon qilingan va versiyalangan tilda.

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

**Tavsif:** Kontekstlar o'rtasida ma'lumot almashish uchun ishlatiladigan, rasmiy ravishda e'lon qilingan, versiyalangan va hech bir kontekstning ichki modeliga tegishli bo'lmagan umumiy format. Muammo: agar har bir juftlik o'z formatida gaplashsa, N ta kontekst uchun N² ta tarjima kerak bo'ladi; Published Language esa yagona neytral oraliq tilni beradi. U sxema (schema) ko'rinishida kodlanadi va sxema evolyutsiyasi qoidalari bilan boshqariladi.

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

**Tavsif:** Ikki kontekst ataylab hech qanday integratsiyaga ega bo'lmaydi - ehtiyoj kichik, integratsiya narxi esa yuqori bo'lgani uchun har biri o'z yechimini mustaqil quradi. Bu "hech narsa qilmaslik" emas, balki ongli arxitektura qarori: bog'liqlikni butunlay yo'q qilish orqali jamoalar maksimal mustaqillikka erishadi. Takrorlanish (duplication) bu holatda narx emas, balki to'lanadigan ongli to'lov hisoblanadi.

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

**Tavsif:** Ikki kontekst va ularning jamoalari shunday chambarchas bog'liq bo'ladi, birining muvaffaqiyatsizligi ikkinchisini ham muvaffaqiyatsiz qiladi - shuning uchun ular rejalashtirish, integratsiya va chiqarishni (release) birgalikda muvofiqlashtiradi. Bu yerda upstream/downstream ierarxiyasi yo'q: interfeys o'zgarishi ikki tomonning kelishuvi bilan bo'ladi va ikkisi bir vaqtda deploy qilinadi. Bu eng qimmat munosabat turi, shuning uchun uzoq muddat saqlanmasligi, vaqtincha holat bo'lishi kerak.

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

**Tavsif:** Domenni uch turga ajratish: Core - kompaniyaga raqobat ustunligi beradigan, eng murakkab va eng qimmatli qism; Supporting - biznes uchun zarur, lekin raqobat ustunligi bermaydigan o'ziga xos qism; Generic - barcha kompaniyalarda bir xil bo'lgan qism (autentifikatsiya, hisob-kitob, bildirishnoma, hujjat saqlash). Bu klassifikatsiya investitsiya qarorini belgilaydi: eng kuchli injenerlar va eng puxta DDD modellashtirish Core'ga, Supporting'ga oddiy CRUD yetarli, Generic esa sotib olinadi yoki tayyor yechim bilan yopiladi. Arxitektor uchun bu "qayerga kuch sarflash kerak" degan savolning asosiy javobi.

**Spring'da qayerda uchraydi:** Core subdomen aggregate'lar, domen eventlari va boy modellashtirish bilan yoziladi (jMolecules `@AggregateRoot`, Spring Modulith `@ApplicationModule`, `ApplicationEventPublisher`, `@DomainEvents` Spring Data'da). Supporting subdomenlar uchun tez yechimlar: Spring Data REST (`@RepositoryRestResource`), Spring Boot `JdbcClient` bilan oddiy CRUD, Spring Batch bilan ommaviy ishlov. Generic subdomenlar odatda tashqi mahsulot bilan yopiladi: autentifikatsiya - Keycloak yoki Spring Authorization Server, to'lov - Stripe SDK, email/SMS - `spring-boot-starter-mail` yoki provayder API'si, qidiruv - Elasticsearch/OpenSearch (`spring-data-elasticsearch`), fayl saqlash - S3. Bu holatda Generic tizimlar bilan aloqa ACL yoki Conformist orqali quriladi.

**Qo'llanish keyslari:**
- Logistika kompaniyasida marshrut optimizatsiyasini Core deb belgilab, unga eng tajribali jamoani biriktirish.
- Autentifikatsiyani o'zi yozish o'rniga Keycloak/Spring Authorization Server bilan yopish.
- Supporting modullarni Spring Data REST bilan tez yetkazib, Core'ga ko'proq vaqt qoldirish.
- Mikroservis chegaralarini subdomen turiga qarab belgilash: Core alohida servis, Generic esa tashqi SaaS.
- Texnik qarz (tech debt) prioritetlashda Core'dagi qarzni Generic'dagidan yuqori qo'yish.

**Ehtiyot bo'ling:** Eng keng tarqalgan xato - Generic subdomenni (o'z autentifikatsiya yoki bildirishnoma tizimini) o'zi yozib, Core'ni esa shoshma-shosharlik bilan anemik CRUD sifatida qoldirish. Shuni ham yodda tuting: klassifikatsiya statik emas - bugun Generic bo'lgan narsa biznes modeli o'zgarishi bilan Core'ga aylanishi mumkin, shuning uchun uni yiliga qayta ko'rib chiqish kerak.

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

**Tavsif:** Entity - bu o'z identifikatori (identity) orqali ajratiladigan domain obyekti: uning atributlari vaqt o'tishi bilan o'zgarsa ham, u bir xil obyekt bo'lib qoladi. Tenglik `equals`/`hashCode` ichida faqat identifikator asosida aniqlanadi, hech qachon barcha maydonlar bo'yicha emas. Entity o'z holatini himoya qiladi: setter'lar o'rniga domain ma'nosiga ega metodlar (`confirm()`, `cancel()`) invariantlarni tekshirib holatni o'zgartiradi. Shu sababli biznes qoidalari service'lar emas, aynan entity ichida yashaydi.

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

**Tavsif:** Value Object identifikatorga ega bo'lmagan, to'liq o'z qiymatlari bilan aniqlanadigan immutable domain tushunchasi: `Money`, `Address`, `EmailAddress`, `DateRange`. Ikki Value Object barcha maydonlari teng bo'lsa teng hisoblanadi, shuning uchun ularni erkin ulashish, cache qilish va thread'lar orasida uzatish xavfsiz. Ular primitive obsession'ni yo'q qiladi: `BigDecimal amount` + `String currency` juftligi o'rniga valyuta mosligini o'zi tekshiradigan `Money` paydo bo'ladi. Validatsiya konstruktorda bir marta bajarilgach, keyin noto'g'ri qiymat umuman mavjud bo'lolmaydi.

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

**Tavsif:** Aggregate - bir-biri bilan chambarchas bog'liq entity va Value Object'larning yagona tranzaksion va konsistentlik chegarasi; tashqi dunyo unga faqat Aggregate Root orqali murojaat qiladi. Root invariantlarni himoya qiladi: ichki obyektlarga havola tashqariga chiqmaydi, ichki o'zgarishlar faqat root metodlari orqali bo'ladi. Aggregate'lar o'zaro to'g'ridan-to'g'ri obyekt havolasi emas, balki ID orqali bog'lanadi, shu bilan ular mustaqil yuklanadi va mustaqil saqlanadi. Qoida sifatida bitta tranzaksiyada faqat bitta aggregate o'zgartiriladi, qolganlari esa domain event'lar bilan eventual consistency rejimida yangilanadi.

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

**Tavsif:** DDD'dagi Repository - aggregate root'lar uchun xotiradagi kolleksiya illyuziyasini beradigan, domain tilida yozilgan abstraksiya; u SQL, jadval yoki ORM haqida hech narsa oshkor qilmaydi. Interfeys domain qatlamida (`OrderRepository`), implementatsiya esa infrastructure qatlamida yashaydi - bu Dependency Inversion'ning amaliy ko'rinishi. Metod nomlari domain niyatini aks ettiradi (`findOverdueInvoices()`), CRUD jargonini emas. Har bir aggregate uchun bitta repository bo'ladi, ichki entity'lar uchun alohida repository yaratilmaydi.

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

**Tavsif:** Factory murakkab aggregate yoki Value Object'ni yaratish mantig'ini ichkariga yashiradi, shunda mijoz kod obyektni to'liq va invariantlari bajarilgan holatda oladi. Konstruktor juda ko'p parametrli yoki yaratish bir necha qoidaga bog'liq bo'lganda factory ishlatiladi: u domain tilida nomlangan metodlar beradi (`Order.placeFor(customer, cart)`). Factory obyekt yaratadi, lekin uni saqlamaydi - persistence repository'ning ishi. Reconstruction (bazadan tiklash) odatda ORM yoki alohida mapper vazifasi, factory esa yangi obyekt tug'ilishi uchun.

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

**Tavsif:** Domain Service - tabiiy ravishda biror entity yoki Value Object'ga tegishli bo'lmagan, bir nechta aggregate yoki murakkab domain qoidasini qamrab oladigan stateless domain operatsiyasi. U domain tilida nomlanadi (`PricingService`, `TransferService`, `RiskScoring`) va faqat domain turlari bilan ishlaydi: HTTP, tranzaksiya yoki DTO'lar haqida bilmaydi. Holat saqlamaydi, shuning uchun thread-safe va oson test qilinadi. Domain Service'ni Application Service bilan aralashtirmaslik kerak: birinchisi *nima* qoida, ikkinchisi *qanday* orkestratsiya.

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

**Tavsif:** Application Service - use case'ning kirish nuqtasi: u aggregate'ni repository'dan oladi, domain metodini chaqiradi, natijani saqlaydi va tranzaksiya, xavfsizlik, event publish kabi texnik masalalarni boshqaradi. Unda biznes qoidasi bo'lmaydi - faqat orkestratsiya: "load → do → save". U tashqi dunyo (controller, message listener, scheduler) bilan domain orasidagi yupqa qatlam bo'lib, DTO ↔ domain konversiyasini chegarada bajaradi. Shu tufayli bitta use case'ni HTTP, gRPC va Kafka'dan bir xil chaqirish mumkin bo'ladi.

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

**Tavsif:** Domain Event - domain'da yuz bergan va boshqa qismlar uchun ahamiyatli bo'lgan faktning immutable yozuvi: `OrderPlaced`, `PaymentFailed`, `InvoiceOverdue`. U o'tgan zamonda nomlanadi, o'zgarmas Value Object sifatida vaqt va kerakli identifikatorlarni olib yuradi, hech qanday xatti-harakat buyurmaydi. Event'lar aggregate'lar va modullar orasidagi bog'lanishni yumshatadi: chiqaruvchi tomon kim tinglayotganini bilmaydi. Natijada cross-aggregate yangilanishlar eventual consistency, audit va integratsiya oson amalga oshadi.

**Spring'da qayerda uchraydi:** Spring Framework 6.x ning `ApplicationEventPublisher#publishEvent(Object)` (POJO event yetarli, `ApplicationEvent` dan meros shart emas), `@EventListener`, `@TransactionalEventListener` va `@Async` bilan asinxron ishlash. Spring Data'da `org.springframework.data.domain.AbstractAggregateRoot#registerEvent()` yoki `@DomainEvents` + `@AfterDomainEventPublication` metodlari `save()` vaqtida event'larni avtomatik publish qiladi. Spring Modulith 1.x `@ApplicationModuleListener` (transactional + async), event publication registry (`EventPublicationRegistry`) va ishonchli qayta urinish/incomplete publication'larni ko'rish imkonini beradi; tashqi tizimga chiqarish uchun Kafka/RabbitMQ `externalized events` (`@Externalized`) ishlatiladi.

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

**Tavsif:** Module (Evans'da "Package") - bir-biriga bog'liq domain tushunchalarini yuqori kohezion, past bog'langan birlikka guruhlash usuli; chegaralar texnik qatlamlar bo'yicha emas, biznes qobiliyatlari bo'yicha chiziladi. Har bir modul tashqariga minimal API (command, event, read DTO) ochadi, qolgani `package-private` bo'lib yashiringan holatda qoladi. Bu monolit ichida ham bounded context'larni aniq ushlab turishga va keyinchalik kerak bo'lsa alohida xizmatga ajratishga imkon beradi. Modul chegarasi - refaktoringning asosiy birligi: ichini o'zgartirish tashqi mijozlarga ta'sir qilmaydi.

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

**Tavsif:** Specification - "obyekt shu shartga javob beradimi?" degan biznes predikatini birinchi darajali domain obyektiga aylantiradi. U uch xil ishlatiladi: validatsiya (mavjud obyektni tekshirish), tanlash (kolleksiya yoki bazadan filtrlash) va yaratish talabini ifodalash. Specification'lar `and`, `or`, `not` bilan birlashtirilib, murakkab qoidalarni kichik, nomlangan va alohida test qilinadigan bo'laklardan yig'ish mumkin. Shu bilan `if` lar daraxti o'rniga domain lug'atida o'qiladigan kod paydo bo'ladi.

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

**Tavsif:** Policy - o'zgarib turadigan biznes qoidasini (chegirma, jarima, marshrutlash, retry, autentifikatsiya talabi) alohida, almashtiriladigan obyektga ajratish; bu Strategy pattern'ning domain darajasidagi ko'rinishi. Qoidalar mijoz, mamlakat, tarif yoki vaqtga qarab farq qilganda, `if/else` daraxti o'rniga bir interfeys va bir nechta nomlangan implementatsiya paydo bo'ladi. Event-driven kontekstda Policy "shu hodisa yuz bersa, shu reaksiya bo'ladi" qoidasi sifatida ham qo'llanadi (Event Storming'dagi "policy" stikerlari). Yangi qoida qo'shish mavjud kodni o'zgartirmaydi - Open/Closed printsipi amalda.

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

**Tavsif:** Invariant - agregat ichida har qanday tranzaksiya tugaganda doimo rost bo'lishi shart bo'lgan biznes qoidasi ("buyurtma qatorlari summasi jami summaga teng", "hisob qoldig'i limitdan past tushmaydi"). Invariantlar aggregate root'ning konsistentlik chegarasini belgilaydi: root o'z ichidagi barcha o'zgarishlarni nazorat qiladi va har bir public metod oxirida qoidani tekshiradi. Shu sababli agregat hajmi invariantlar to'plamidan kelib chiqadi, ma'lumotlar bazasi jadvallari tuzilishidan emas. Invariant buzilganda obyekt yaratilmaydi yoki amal bajarilmaydi - noto'g'ri holat hech qachon xotirada paydo bo'lmasligi kerak.

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

**Tavsif:** Qoida shu: bitta tranzaksiyada faqat bitta agregat o'zgartiriladi, qolgan agregatlar esa domen hodisalari orqali keyinroq sinxronlanadi. Boshqa agregatlarga obyekt havolasi emas, identifikator (`CustomerId`) bilan murojaat qilinadi, shu bilan tranzaksiya chegarasi va lock maydoni kichik bo'ladi. Natijada sistema bir muddat "nomuvofiq" ko'rinadi, lekin bu oyna biznes nuqtai nazaridan maqbul bo'lsa, scalability va mavjudlik sezilarli yaxshilanadi. Kompensatsiya (sagas, retry, dead-letter) bu yondashuvning ajralmas qismi.

**Spring'da qayerda uchraydi:** `ApplicationEventPublisher` + `@TransactionalEventListener(phase = TransactionPhase.AFTER_COMMIT)` eng oddiy ichki variant. Ishonchli yetkazib berish uchun Spring Modulith: `@ApplicationModuleListener` (`@Async` + `@Transactional(propagation = REQUIRES_NEW)` + `AFTER_COMMIT` kombinatsiyasi) va Event Publication Registry (`event_publication` jadvali, `spring-modulith-events-jpa`/`-jdbc`, broker ko'prigi uchun `spring-modulith-events-kafka`/`-amqp`) - ya'ni transactional outbox pattern tayyor holda. Kattaroq miqyosda `spring-kafka` (`KafkaTemplate`, `@KafkaListener`), `spring-rabbit` yoki `spring-cloud-stream`, idempotentlik uchun `@Transactional` ichida ishlov berilgan message ID jadvali.

**Qo'llanish keyslari:**
- `OrderPlaced` hodisasidan keyin inventar agregati alohida tranzaksiyada zaxirani kamaytiradi.
- Foydalanuvchi profili o'zgarganda, uning nomi buyurtmalar read model'ida bir necha yuz millisekunddan keyin yangilanadi.
- To'lov tasdiqlangach, `Order` statusi `PAID`ga o'tadi - to'lov va buyurtma agregatlari alohida saqlanadi.
- Loyalty ball hisoblash kechiktirilgan listener'da bajariladi, chunki u buyurtmani qabul qilishni to'xtatmasligi kerak.
- Bir nechta microservice o'rtasida saga: buyurtma bekor qilinganda zaxira va to'lov kompensatsiya hodisalari bilan qaytariladi.

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

**Tavsif:** Operatsiyalarni ikki turga ajratamiz: holatni o'zgartiruvchi `command`lar va hech narsani o'zgartirmaydigan, faqat natija qaytaruvchi `query`lar (funksiyalar). Murakkab hisob-kitoblarni yon ta'sirsiz funksiyalarga, afzal holda value object'lar ustiga ko'chirsak, ularni erkin chaqirish, kombinatsiyalash, keshlash va test qilish mumkin bo'ladi. Command'lar esa iloji boricha sodda bo'lib, natijani funksiyalardan olib, faqat yakuniy holatni o'rnatadi. Bu "supple design"ning asosiy vositalaridan biri va invariantlar haqida fikrlashni ancha osonlashtiradi.

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

**Tavsif:** Sinf, metod va parametr nomlari implementatsiyani emas, maqsadni - ya'ni domen ekspertlari tilidagi niyatni - aytib turishi kerak. `order.setStatus(3)` o'rniga `order.confirm()`, `repo.findByFlagTrue()` o'rniga `repo.findActiveSubscriptions()` yoziladi. Shunda kodni o'qigan injener metod ichiga kirmasdan uning nima qilishini tushunadi va Ubiquitous Language kodda saqlanadi. Bu pattern test nomlari, exception nomlari va hodisa nomlariga ham taalluqli.

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

**Tavsif:** Agar amal argument sifatida qabul qilgan va natija sifatida qaytargan tur bir xil bo'lsa, amal shu tur ustida "yopiq" deyiladi: `Money.add(Money) -> Money`, `Specification.and(Specification) -> Specification`. Bunday amallar yangi tushuncha kiritmaydi, shuning uchun interfeys soddalashadi va amallarni cheksiz zanjirlash hamda kombinatsiyalash mumkin bo'ladi. Bu matematikadagi yarim guruh/monoid g'oyasining domen modelidagi ko'rinishi va u ko'pincha value object'lar ustida tabiiy chiqadi. Yopiqlikni qisman ham qo'llash mumkin - masalan, argument boshqa tur, natija esa o'sha turda bo'lsa (`Money.multiply(BigDecimal) -> Money`).

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

**Tavsif:** Har bir qo'shimcha bog'liqlik sinfni tushunish uchun kerakli "aqliy yuk"ni oshiradi; shuning uchun eng muhim va murakkab mantiqni iloji boricha kam bog'liqlikka ega, hatto umuman mustaqil sinflarga ajratish tavsiya etiladi. Ideal holda bunday sinf faqat til va standart kutubxona turlariga tayanadi, framework yoki ma'lumotlar bazasi haqida hech narsa bilmaydi. Natijada u mustaqil o'qiladi, oson test qilinadi va boshqa kontekstlarda qayta ishlatiladi. Bu Dependency Inversion bilan birga ishlaydi: infratuzilma domenga qaraydi, teskarisi emas.

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

**Tavsif:** Supple Design - Evans kitobining 10-bobidagi umumlashtiruvchi maqsad: model shunday yozilsinki, undan foydalanuvchi injener o'zgartirish kiritishdan qo'rqmasin va yangi talablar modelga "qulf"ga kalit kabi joylashsin. U alohida pattern emas, balki bir nechta texnikaning yig'indisi: Intention-Revealing Interfaces, Side-Effect-Free Functions, Assertions, Conceptual Contours, Standalone Classes, Closure of Operations va Declarative Style of Design. Asosiy mezoni - refactoring qilish qo'rqinchli emas, balki arzon bo'lishi; bu esa chuqur modelni izlash (deep model) jarayonining mevasi.

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

**Tavsif:** Anemik model - domen obyektlari faqat maydon, getter va setter'dan iborat bo'lib, barcha biznes mantiq "service" sinflariga ko'chib ketgan holat (atamani Martin Fowler 2003-yilda ommalashtirgan). Bunda obyektga yo'naltirilgan dizaynning asosiy foydasi - ma'lumot va xatti-harakatni birga saqlash - yo'qoladi: invariantlar tarqalib ketadi, bir xil qoida bir necha servisda takrorlanadi va noto'g'ri holatni yaratish oson bo'ladi. Natijada model emas, oddiy ma'lumot tashuvchi (data holder) qoladi va murakkablik o'sgan sari servis sinflari procedural "god class"larga aylanadi. Shuni ta'kidlash kerak: oddiy CRUD ilovada bu ongli, maqbul tanlov bo'lishi mumkin - anti-pattern bo'lishi faqat murakkab domenda yuzaga keladi.

**Spring'da qayerda uchraydi:** Tipik ko'rinishi: `@Entity` sinf Lombok `@Data`/`@Setter` bilan to'liq ochiq, yonida `@Service` sinf `OrderService.updateOrder(OrderDto)` metodida barcha `if`lar bilan. Davolash yo'llari: entity'da public setter'larni olib tashlash va niyatli metodlar qoldirish, `@Embeddable` value object'lar, JPA uchun `protected` no-arg konstruktor + factory metodlar, agregat ichidagi kolleksiyalarni `Collections.unmodifiableList` bilan qaytarish, hodisalar uchun `AbstractAggregateRoot`. Spring Modulith va jMolecules (`@AggregateRoot`, `@ValueObject`) rollarni aniq qilib, mantiqni to'g'ri joyga qo'yishga undaydi; `@Transactional` esa domen emas, application qatlamida turadi.

**Qo'llanish keyslari:**
- Legacy `OrderService` ichidagi status o'tish mantiqini `Order.confirm()`/`Order.cancel()` metodlariga ko'chirish.
- `@Data` annotatsiyasini olib tashlab, entity'ga faqat kerakli mutator metodlarni qoldirish.
- Pul va manzil maydonlarini `Money`/`Address` `@Embeddable` value object'lariga yig'ish.
- Takrorlangan validatsiyani uchta servisdan bitta agregat metodiga birlashtirish.
- CRUD-ga yaqin supporting modulni ataylab anemik qoldirib, core domain'ni boyitishga kuch yo'naltirish.

**Ehtiyot bo'ling:** Teskari chetga chiqmang: agregatga repository, HTTP client yoki tashqi servis in'ektsiya qilib, uni "boy" qilishga urinish bog'liqliklarni domenga tortadi - bunday mantiq application servisga yoki domain service'ga tegishli. Shuningdek DTO va API modellari ataylab anemik bo'ladi; anemiklik muammosi faqat domen modeliga tegishli.

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

**Tavsif:** Event Storming - Alberto Brandolini taklif qilgan ustaxona (workshop) texnikasi: domen ekspertlari va injenerlar katta devorga vaqt bo'yicha tartiblangan domen hodisalarini yopishqoq qog'ozlarda joylab, biznes jarayonini birgalikda kashf qiladi. Odatda uch darajada o'tkaziladi: Big Picture (butun biznes manzarasi), Process Level (bitta jarayonni chuqurlashtirish) va Design Level (agregatlar, command'lar, policy'lar aniqlanadigan daraja). Rang konvensiyasi keng tarqalgan: to'q sariq - domen hodisasi, ko'k - command, sariq - agregat, siyohrang - policy/qoida, pushti - tashqi sistema, yashil - read model, qizil - "hot spot" (nizo yoki noaniqlik). Natija sifatida Ubiquitous Language, bounded context chegaralari va agregat nomzodlari qo'lga kiritiladi.

**Spring'da qayerda uchraydi:** Bu kod pattern'i emas, lekin natijasi Spring loyihasiga bevosita ko'chadi: to'q sariq hodisalar - `OrderPlaced` kabi domen hodisa sinflari (`ApplicationEventPublisher`, `@DomainEvents`, `@ApplicationModuleListener`); ko'k command'lar - application servis metodlari yoki `@PostMapping` endpoint'lari; sariq agregatlar - `@Entity` aggregate root'lar va ularning repository'lari; siyohrang policy'lar - `@TransactionalEventListener`/`@KafkaListener` handler'lari; yashil read model'lar - CQRS projection jadvallari va `@Query` proyeksiyalari. Bounded context chegaralari Spring Modulith modullariga (`@ApplicationModule`, `package-info.java`) yoki alohida servislarga aylanadi, `Documenter` esa bu strukturani diagramma qilib beradi.

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
  2. Buyruqlar (ko'k): hodisani keltirib chiqaradi
       PlaceOrder, ReserveStock, CapturePayment
  3. Aktorlar (sariq): kim chaqiradi
       Mijoz, Ombor xodimi, To'lov provayderi
  4. Siyosatlar (siyohrang): "har qachon X bo'lsa, Y qilinadi"
       OrderPlaced -> ReserveStock
  5. Agregatlar (och sariq): buyruqni qabul qiladi va invariantni saqlaydi
       Order, Reservation, Payment
  6. Chegaralar: hodisalar zich guruhlangan joyda bounded context chizig'i

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

**Tavsif:** Klassik DDD tizimni to'rt qatlamga ajratadi: User Interface/Presentation, Application, Domain va Infrastructure; bog'liqliklar faqat yuqoridan pastga yo'naladi, domen esa hech kimga bog'lanmaydi. Application qatlami use-case'ni orkestratsiya qiladi (tranzaksiya, xavfsizlik, DTO mapping), biznes qoidalari domenda turadi, infrastruktura esa domen e'lon qilgan port'larni (repository interfeyslari) implement qiladi - ya'ni Dependency Inversion. Zamonaviy variantlari Hexagonal (Ports & Adapters), Onion va Clean Architecture bo'lib, maqsad bir xil: domen yadrosini framework va texnologiyadan ajratish.

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

**Tavsif:** Money - bu miqdor (amount) va valyuta (currency) juftligini bitta o'zgarmas Value Object sifatida birlashtiradigan maxsus pattern, chunki pulni oddiy `double` yoki yalang'och `BigDecimal` bilan ifodalash moliyaviy domenda eng ko'p uchraydigan xatolik manbai. `double` ikkilik suzuvchi nuqta tufayli yaxlitlash xatolarini keltiradi, yalang'och `BigDecimal` esa valyuta ma'lumotini yo'qotadi va USD bilan UZS'ni beg'araz qo'shib yuborish imkonini beradi. Money sinfi arifmetik amallarni (`add`, `subtract`, `multiply`, `allocate`) o'zida saqlaydi, har bir amalda valyuta mosligini tekshiradi va yaxlitlash qoidasini (`RoundingMode`, scale) markazlashtiradi. Shuningdek u taqsimlash muammosini hal qiladi: 100.00 ni 3 ga bo'lganda tiyinlar yo'qolmasligi uchun qoldiqni determinativ tarzda ulushlar orasida tarqatadi.

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

## 13.36 Amalda qo'llash

- [ ] Domen tilidagi atamalarni ro'yxat qiling va kodda boshqa nom bilan atalganlarini toping.
- [ ] Har bir agregat uchun invariantni bir gapda yozing va u qayerda majburlanayotganini ko'rsating.
- [ ] Agregat chegarasidan tashqariga chiqadigan tranzaksiyalarni toping - bitta tranzaksiya bitta agregatni o'zgartirishi kerak.
- [ ] Qiymat obyekti bo'lishi kerak bo'lgan primitivlarni toping (pul, email, telefon, ID) va ularni `record` ga o'tkazish rejasini tuzing.
- [ ] Bounded context chegaralarini chizib, kontekstlar o'rtasidagi har bir integratsiya uchun anti-corruption layer kerakligini qaror qiling.
- [ ] Domen hodisalarini sanab chiqing va har birining nomi o'tgan zamonda ekanini tasdiqlang.
- [ ] Repository interfeyslari domen paketida, implementatsiyasi infratuzilmada turganini tekshiring.
- [ ] Domen paketida `jakarta.persistence`, Jackson va Spring web importlarini qidirib, topilganlarini ro'yxat qiling.

---

[&larr; 12. Arxitektura uslublari](12-arxitektura-uslublari.md) · [Mundarija](README.md) · [14. Microservices patternlari &rarr;](14-microservices-patternlari.md)
