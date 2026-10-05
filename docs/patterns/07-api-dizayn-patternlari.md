<!-- doc: patterns | chapter: 7 | part:  -->

[Barcha hujjatlar](../../README.md) / [Dizayn patternlar](README.md)

# 7. API dizayn patternlari (API Design Patterns)

<details>
<summary>Bu bo'limdagi 34 bo'lim</summary>

- [7.1 Resurs-yo'naltirilgan REST (Resource-oriented REST)](#71-resurs-yonaltirilgan-rest-resource-oriented-rest)
- [7.2 Richardson yetuklik modeli (Richardson Maturity Model)](#72-richardson-yetuklik-modeli-richardson-maturity-model)
- [7.3 HATEOAS - gipermedia bilan boshqariladigan holat (HATEOAS, Hypermedia as the Engine of Application State)](#73-hateoas---gipermedia-bilan-boshqariladigan-holat-hateoas-hypermedia-as-the-engine-of-application-state)
- [7.4 URI dizayn konvensiyalari (URI Design Conventions)](#74-uri-dizayn-konvensiyalari-uri-design-conventions)
- [7.5 API versiyalash (API Versioning)](#75-api-versiyalash-api-versioning)
- [7.6 Offset pagination (Offset Pagination)](#76-offset-pagination-offset-pagination)
- [7.7 Keyset / kursor pagination (Keyset / Cursor Pagination)](#77-keyset--kursor-pagination-keyset--cursor-pagination)
- [7.8 Filtrlash, tartiblash va maydon tanlash (Filtering, Sorting, Field Selection)](#78-filtrlash-tartiblash-va-maydon-tanlash-filtering-sorting-field-selection)
- [7.9 Idempotentlik kaliti (Idempotency Key)](#79-idempotentlik-kaliti-idempotency-key)
- [7.10 Problem Details - standart xato formati (Problem Details, RFC 9457)](#710-problem-details---standart-xato-formati-problem-details-rfc-9457)
- [7.11 Shartli so'rovlar va ETag (Conditional Requests / ETag)](#711-shartli-sorovlar-va-etag-conditional-requests--etag)
- [7.12 HTTP keshlash sarlavhalari (HTTP Caching Headers)](#712-http-keshlash-sarlavhalari-http-caching-headers)
- [7.13 So'rov tezligini cheklash (Rate Limiting)](#713-sorov-tezligini-cheklash-rate-limiting)
- [7.14 Bulk / Batch endpoint'lar (Bulk / Batch Endpoints)](#714-bulk--batch-endpointlar-bulk--batch-endpoints)
- [7.15 Asinxron so'rov-javob (Asynchronous Request-Reply)](#715-asinxron-sorov-javob-asynchronous-request-reply)
- [7.16 Uzoq polling (Long Polling)](#716-uzoq-polling-long-polling)
- [7.17 Webhook'lar (Webhooks)](#717-webhooklar-webhooks)
- [7.18 API Gateway (API Gateway)](#718-api-gateway-api-gateway)
- [7.19 Frontend uchun backend (Backend for Frontend, BFF)](#719-frontend-uchun-backend-backend-for-frontend-bff)
- [7.20 API kompozitsiyasi / Aggregator (API Composition / Aggregator)](#720-api-kompozitsiyasi--aggregator-api-composition--aggregator)
- [7.21 Bag'rikeng o'quvchi (Tolerant Reader)](#721-bagrikeng-oquvchi-tolerant-reader)
- [7.22 Consumer tomonidan boshqarilgan kontraktlar (Consumer-Driven Contracts)](#722-consumer-tomonidan-boshqarilgan-kontraktlar-consumer-driven-contracts)
- [7.23 Kengaytir/Qisqartir (Expand/Contract - Parallel Change)](#723-kengaytirqisqartir-expandcontract---parallel-change)
- [7.24 Konvert javob va yalang'och javob (Envelope vs Bare Response)](#724-konvert-javob-va-yalangoch-javob-envelope-vs-bare-response)
- [7.25 Xato javobini loyihalash (Error Response Design)](#725-xato-javobini-loyihalash-error-response-design)
- [7.26 GraphQL (GraphQL with Spring for GraphQL)](#726-graphql-graphql-with-spring-for-graphql)
- [7.27 gRPC (gRPC with Spring)](#727-grpc-grpc-with-spring)
- [7.28 OpenAPI: kontrakt-birinchi yoki kod-birinchi (Contract-First vs Code-First OpenAPI)](#728-openapi-kontrakt-birinchi-yoki-kod-birinchi-contract-first-vs-code-first-openapi)
- [7.29 Deklarativ HTTP client'lar (Declarative HTTP Interfaces / @HttpExchange)](#729-deklarativ-http-clientlar-declarative-http-interfaces--httpexchange)
- [7.30 Deprecation va Sunset header'lari (Deprecation / Sunset Headers)](#730-deprecation-va-sunset-headerlari-deprecation--sunset-headers)
- [7.31 Hypermedia boshqaruvlari va RPC uslubi (Hypermedia Controls vs RPC-style)](#731-hypermedia-boshqaruvlari-va-rpc-uslubi-hypermedia-controls-vs-rpc-style)
- [7.32 Chegarada API Key va token autentifikatsiyasi (API Key / Token Auth at the Edge)](#732-chegarada-api-key-va-token-autentifikatsiyasi-api-key--token-auth-at-the-edge)
- [7.33 Veb-servis brokeri (Web Service Broker)](#733-veb-servis-brokeri-web-service-broker)
- [7.34 Amalda qo'llash](#734-amalda-qollash)

</details>



API dizayn patternlari - bu tizimning tashqi dunyo bilan shartnomasini (contract) shakllantiruvchi qarorlar to'plami. Ichki arxitekturani keyinchalik qayta yozish mumkin, lekin bir marta chiqarilgan va iste'molchilar tomonidan ishlatilayotgan API'ni o'zgartirish deyarli har doim buzuvchi (breaking) o'zgarish bo'ladi va migratsiya xarajatlarini iste'molchilar zimmasiga yuklaydi. Shuning uchun arxitektor uchun resurs modeli, versiyalash strategiyasi, pagination yondashuvi, xato formati va idempotentlik kafolatlari - bu kech emas, balki eng boshida qabul qilinishi kerak bo'lgan qarorlardir. Quyidagi patternlar HTTP protokolining o'zidagi mexanizmlarga (status kodlar, header'lar, caching semantikasi) tayanadi va Spring ekotizimida bevosita qo'llab-quvvatlanadi.

## 7.1 Resurs-yo'naltirilgan REST (Resource-oriented REST)

**Tavsif:** API'ni protsedura (RPC-uslub) chaqiruvlari emas, balki URI bilan identifikatsiya qilinadigan resurslar to'plami sifatida modellashtirish. Harakat turi HTTP metodi bilan ifodalanadi (GET - o'qish, POST - yaratish, PUT/PATCH - o'zgartirish, DELETE - o'chirish), resurs esa ot shaklida URI'da turadi. Bu yondashuv protokolning kesh, idempotentlik va xavfsizlik (safe method) semantikasini bepul olib keladi, chunki oraliq proxy va CDN'lar HTTP metodlarining ma'nosini allaqachon tushunadi.

**Spring'da qayerda uchraydi:** `@RestController` bilan birga `@GetMapping`, `@PostMapping`, `@PutMapping`, `@PatchMapping`, `@DeleteMapping`; `@RequestMapping(path = "/orders", produces = MediaType.APPLICATION_JSON_VALUE)` resurs ildizini belgilash uchun. `@PathVariable` resurs identifikatorini, `ResponseEntity<T>` esa status kod va header'larni aniq boshqarish uchun ishlatiladi. Reaktiv stackda xuddi shu annotatsiyalar WebFlux'da, yoki funksional `RouterFunctions.route()` DSL'i bilan. Spring Data REST (`@RepositoryRestResource`) repository'lardan avtomatik resurs-yo'naltirilgan API generatsiya qiladi.

**Qo'llanish keyslari:**
- Ko'p turdagi klientlar (web SPA, mobil, partner integratsiyalari) iste'mol qiladigan ommaviy platforma API'si.
- CDN yoki reverse proxy darajasida GET javoblarini keshlash zarur bo'lgan katalog/kontent xizmatlari.
- CRUD ustunlik qiladigan admin va backoffice API'lari, bu yerda resurs modeli domen entity'lariga tabiiy mos keladi.
- API Gateway ortida turgan mikroservislar, chunki gateway'da marshrutlash va rate limiting metod+yo'l bo'yicha sozlanadi.
- Spring Data REST yoki shunga o'xshash generatorlar bilan tezkor prototip qurish.

**Ehtiyot bo'ling:** Har bir domen amalini resursga majburan siqib tiqish anti-pattern: "to'lovni qaytarish" yoki "buyurtmani bekor qilish" kabi tranzaksion amallar uchun alohida sub-resurs (`POST /orders/{id}/cancellations`) yoki ochiq RPC endpoint tabiiyroq bo'ladi. Shuningdek, DB jadvallarini bir-biriga aynan moslashtirish (`@Entity` to'g'ridan-to'g'ri JSON'ga) API'ni schema o'zgarishlariga qattiq bog'laydi - DTO qatlamini saqlang.

```java
// Resurs va holat: fe'l URL da emas, HTTP metodida
@RestController
@RequestMapping("/orders")
class OrderApi {
    @GetMapping("/{id}")    OrderDto get(@PathVariable long id) { /* ... */ }
    @PostMapping            ResponseEntity<Void> create(@RequestBody CreateOrder cmd) { /* ... */ }
    @PatchMapping("/{id}")  OrderDto patch(@PathVariable long id, @RequestBody JsonNode p) { /* ... */ }
    @DeleteMapping("/{id}") ResponseEntity<Void> delete(@PathVariable long id) { /* ... */ }
}
// Yomon: POST /createOrder, GET /getOrderById?id=1
```

## 7.2 Richardson yetuklik modeli (Richardson Maturity Model)

**Tavsif:** Leonard Richardson taklif qilgan, REST API'ning HTTP protokolidan qanchalik to'liq foydalanayotganini o'lchaydigan to'rt darajali shkala. Level 0 - bitta endpoint ustidan XML/JSON "botqoq" (SOAP-uslub tunnel), Level 1 - alohida resurslar paydo bo'ladi, Level 2 - HTTP metodlari va status kodlar to'g'ri semantikada ishlatiladi, Level 3 - javoblar o'z ichida keyingi mumkin bo'lgan harakatlar havolalarini (HATEOAS) olib yuradi. Model maqsad emas, balki diagnostika vositasi: u API'ning qaysi joyida protokol imkoniyatlari behuda qolganini ko'rsatadi.

**Spring'da qayerda uchraydi:** Level 2 - standart `@RestController` + `ResponseEntity` + to'g'ri status kodlar (`HttpStatus.CREATED`, `Location` header). Level 3 - Spring HATEOAS moduli (`spring-boot-starter-hateoas`), `EntityModel`, `CollectionModel`, `WebMvcLinkBuilder`. Spring Data REST sukut bo'yicha Level 3'ga yaqin javoblarni HAL formatida qaytaradi. `@ResponseStatus` va `ResponseStatusException` orqali status kodlarni domen xatolariga bog'lash Level 2 gigiyenasining bir qismi.

**Qo'llanish keyslari:**
- Mavjud legacy API'ni audit qilib, texnik qarz (tech debt) darajasini jamoaga tushuntirish.
- API design review'da umumiy lug'at sifatida: "bu Level 1'da qolgan, metodlar ishlatilmayapti".
- Yangi xizmat uchun maqsad darajani ongli tanlash (ko'pchilik uchun Level 2 yetarli).
- SOAP yoki bitta `/api/execute` endpointidan HTTP-native API'ga migratsiya rejasini bosqichlarga bo'lish.

**Ehtiyot bo'ling:** Level 3'ga intilish o'z-o'zidan qiymat emas - agar klientlar havolalarni kuzatmasa (follow qilmasa), HATEOAS faqat javob hajmini oshiradi. Modelni "ball to'plash" o'yiniga aylantirmang; asosiy xato Level 2 gigiyenasini (to'g'ri status kodlar, idempotent PUT) chetlab o'tib, darhol link'lar qo'shishdir.

```text
0-daraja: bitta URL, bitta metod (RPC over HTTP)
  POST /api  {"method":"getOrder","id":1}

1-daraja: resurslar paydo bo'ldi
  POST /orders/1

2-daraja: HTTP metod va status kodlari to'g'ri ishlatiladi
  GET /orders/1      -> 200
  DELETE /orders/1   -> 204
  POST /orders       -> 201 + Location

3-daraja: javobda keyingi harakatlar havolasi (HATEOAS)
  GET /orders/1 -> {"id":1,"_links":{"cancel":{"href":"/orders/1/cancel"}}}
```

## 7.3 HATEOAS - gipermedia bilan boshqariladigan holat (HATEOAS, Hypermedia as the Engine of Application State)

**Tavsif:** Javob ichida nafaqat ma'lumot, balki shu holatda bajarilishi mumkin bo'lgan keyingi harakatlarning havolalari ham qaytariladi. Klient URI'larni o'zida hardcode qilmasdan, link relation nomlari (`self`, `next`, `cancel`) bo'yicha harakat qiladi, server esa URI strukturasini va mavjud harakatlar to'plamini runtime'da o'zgartirishi mumkin. Masalan, `PAID` holatidagi buyurtmada `refund` havolasi bo'ladi, `DRAFT` holatida esa yo'q - ya'ni biznes qoidalari javobda deklarativ ko'rinadi.

**Spring'da qayerda uchraydi:** Spring HATEOAS: `EntityModel<T>`, `CollectionModel<T>`, `PagedModel<T>`, `Link`, `LinkRelation`, `WebMvcLinkBuilder.linkTo(methodOn(...))`, `RepresentationModelAssembler` va `RepresentationModelAssemblerSupport`. Media type'lar: HAL (`application/hal+json`, sukut bo'yicha), HAL-FORMS, Collection+JSON, UBER - `@EnableHypermediaSupport(type = HypermediaType.HAL_FORMS)` bilan tanlanadi. Affordance API (`.andAffordance(afford(methodOn(...)))`) HAL-FORMS'da bajarilishi mumkin bo'lgan metod va maydonlarni tasvirlaydi. Klient tomonida `Traverson` yoki `HalExplorer`.

**Qo'llanish keyslari:**
- Ish jarayoni (workflow) holatiga qarab ruxsat etilgan harakatlar o'zgaradigan API'lar: to'lov, buyurtma, hujjat tasdiqlash.
- Generik UI: frontend serverdan kelgan `_links`/HAL-FORMS asosida tugmalarni dinamik ko'rsatadi.
- Pagination havolalarini (`next`, `prev`, `first`, `last`) standart tarzda berish - eng ko'p qo'llanadigan amaliy holat.
- Spring Data REST asosidagi ichki admin API'lari, bu yerda discoverability qo'lda yozishni qisqartiradi.
- Partner API'lari, bu yerda URI strukturasini kelajakda o'zgartirish erkinligini saqlash muhim.

**Ehtiyot bo'ling:** Ko'pchilik klient jamoalari amalda URI'ni hardcode qiladi va `_links`'ni e'tiborsiz qoldiradi - natijada siz ikki tomonlama shartnomani saqlashga majbur bo'lasiz. Katta kolleksiyalarda har bir element uchun link generatsiyasi (`linkTo(methodOn(...))` reflection ishlatadi) sezilarli CPU va javob hajmi qo'shadi, shuning uchun uni o'lchab ko'ring.

```java
@GetMapping("/accounts/{id}")
EntityModel<AccountDto> get(@PathVariable long id) {
    Account a = service.load(id);
    EntityModel<AccountDto> model = EntityModel.of(AccountDto.of(a));
    model.add(linkTo(methodOn(getClass()).get(id)).withSelfRel());
    // Harakat faqat ruxsat etilgan holatda ko'rinadi
    if (a.canWithdraw()) {
        model.add(linkTo(methodOn(getClass()).withdraw(id, null)).withRel("withdraw"));
    }
    return model;
}
```

## 7.4 URI dizayn konvensiyalari (URI Design Conventions)

**Tavsif:** URI'larni bashorat qilinadigan va barqaror qiladigan qoidalar to'plami: resurs kolleksiyalari ko'plikda va ot shaklida (`/orders`), ierarxiya sub-resurs sifatida (`/orders/{orderId}/items/{itemId}`), ko'p so'zli segmentlar uchun kebab-case, versiya yoki format URI'da aralashtirilmasligi, so'rov parametrlari faqat filtr/sort/pagination uchun. Maqsad - URI'ni dokumentatsiyasiz ham o'qiladigan qilish va marshrutlash qoidalarini (gateway, rate limit, log grouping) oddiy saqlash.

**Spring'da qayerda uchraydi:** `@RequestMapping` sinf darajasida umumiy prefiksni, `spring.mvc.servlet.path` yoki `server.servlet.context-path` esa global prefiksni belgilaydi. `PathPattern` sintaksisi (Spring Framework 5.3+ dan MVC'da sukut bo'yicha): `{id}`, `{*path}`, `{id:[0-9]+}` regex cheklovlari. `PathMatchConfigurer` orqali `setUseTrailingSlashMatch` (Spring 6'da deprecated/o'chirilgan - oxirgi slash endi alohida yo'l hisoblanadi), `addPathPrefix(prefix, predicate)` esa paket yoki annotatsiya bo'yicha prefiks qo'shadi. `UriComponentsBuilder` va `@PathVariable Map<String,String>` URI qurish va o'qish uchun.

**Qo'llanish keyslari:**
- Ko'p jamoali monorepo yoki mikroservis platformasida umumiy API style guide'ni majburlash.
- API Gateway'da yo'l prefiksi bo'yicha marshrutlash va per-route rate limiting sozlash.
- Observability: yo'l shabloni (`/orders/{id}`) bo'yicha metrikalarni guruhlash, aks holda har bir ID alohida metrika kardinalligini oshiradi.
- SDK va kod generatsiyasi: bashorat qilinadigan URI'lar OpenAPI'dan klient generatsiyasini soddalashtiradi.
- Legacy API'ni konsolidatsiya qilishda yangi konvensiyaga o'tish uchun `addPathPrefix` bilan bosqichma-bosqich migratsiya.

**Ehtiyot bo'ling:** Chuqur ierarxiya (`/a/{id}/b/{id}/c/{id}/d`) qattiq bog'lanish hosil qiladi - ikki daraja odatda kifoya, qolganini filtr parametriga chiqaring. Spring 6'da trailing slash mosligi olib tashlangani uchun eski klientlar `/orders/` bilan 404 olishi mumkin; migratsiyada bunga aniq redirect yoki gateway qoidasi yozing.

```text
Konvensiya: ko'plik, kichik harf, chiziqcha, ichma-ich kolleksiya
  GET    /customers/42/orders              # 42-mijozning buyurtmalari
  GET    /orders/1001/line-items           # kebab-case, ko'plik
  POST   /orders/1001/cancellation         # harakat resurs sifatida

Qochish kerak:
  /getOrders, /orders_list, /Orders, /order/1001/LineItems

Ichma-ich 2 darajadan oshmasin: /a/1/b/2/c/3 o'qilmaydi
```

## 7.5 API versiyalash (API Versioning)

**Tavsif:** Shartnomani buzuvchi o'zgarishlarni mavjud iste'molchilarni sindirmasdan chiqarish mexanizmi. To'rtta asosiy variant: URI yo'lida (`/v2/orders`) - eng ko'rinadigan va keshlashga qulay; maxsus header'da (`X-API-Version: 2`) - URI toza qoladi, lekin kesh kaliti va debug qiyinlashadi; media type orqali content negotiation (`Accept: application/vnd.acme.order.v2+json`) - eng "to'g'ri" HTTP yondashuvi, ammo klientlar uchun noqulay; query parametrida (`?version=2`) - eng oson, lekin keshda va gateway'da chalkashlik keltiradi. Tanlov texnik emas, ko'proq tashkiliy: kim, qancha vaqt, nechta versiyani saqlaydi.

**Spring'da qayerda uchraydi:** Spring Framework 7 / Spring Boot 4'da versiyalash birinchi darajali qo'llab-quvvatlanadi: `@RequestMapping(version = "1.1")` (va `@GetMapping(version = ...)`), `ApiVersionConfigurer` orqali `useRequestHeader("X-API-Version")`, `usePathSegment(n)`, `useQueryParam("version")`, `useMediaTypeParameter(...)` konfiguratsiyasi, qo'llab-quvvatlanadigan versiyalarni ro'yxatdan o'tkazish va `ApiVersionDeprecationHandler`; mos kelmagan versiya `NotAcceptableApiVersionException` beradi. Klient tomonida `RestClient`/`WebClient`'da `apiVersion(...)`. Spring 6.x va undan oldin: `produces = "application/vnd.acme.v2+json"` bilan content negotiation, yoki `RequestMappingHandlerMapping`/`RequestCondition` sub-klassini qo'lda yozish. Deprecation'ni e'lon qilish uchun `Deprecation` va `Sunset` HTTP header'lari.

**Qo'llanish keyslari:**
- Partner yoki ommaviy API'da breaking o'zgarish: eski versiyani sunset sanasi bilan saqlab, yangisini parallel chiqarish.
- Mobil ilovalar: foydalanuvchilar eski versiyada qolib ketadi, shuning uchun bir necha API versiyasi uzoq yashashi kerak.
- Bitta controller ichida ikki versiya metodini saqlash (Spring 7 `version` atributi bilan) va umumiy service qatlamini qayta ishlatish.
- B2B integratsiyalarda shartnoma majburiyatlari: har bir versiya uchun SLA va qo'llab-quvvatlash muddati.
- Ichki mikroservislar o'rtasida header-based versiyalash, gateway esa tashqi klientlar uchun yo'l-based versiyani mapping qiladi.

```java
@RestController
@RequestMapping("/orders")
class OrderController {
    @GetMapping(path = "/{id}", version = "1.0")
    OrderV1 getV1(@PathVariable String id) { ... }

    @GetMapping(path = "/{id}", version = "1.1+")   // 1.1 va yuqorisi
    OrderV2 getV2(@PathVariable String id) { ... }
}
```

**Ehtiyot bo'ling:** Versiyalarni ko'paytirish eng qimmat yo'l - har bir aktiv versiya test, monitoring va bug-fix xarajati. Avval qo'shimcha (additive) o'zgarishlar va tolerant reader printsipi bilan versiyasiz yashashga harakat qiling; versiya ochganda sunset sanasini va o'chirish rejasini birgalikda e'lon qiling, aks holda "v1 abadiy" muammosiga tushasiz.

## 7.6 Offset pagination (Offset Pagination)

**Tavsif:** Natijalarni `offset`/`limit` (yoki `page`/`size`) orqali bo'lib berish: server `LIMIT n OFFSET m` bajaradi va odatda umumiy sonni ham qaytaradi. Afzalligi - ixtiyoriy sahifaga sakrash (`?page=57`), umumiy sahifa sonini ko'rsatish va klient tomonida oddiy implementatsiya. Kamchiligi - DB katta offset'da ham barcha oldingi qatorlarni skanerlab tashlab yuborishga majbur, shuningdek ma'lumot o'zgarganda elementlar sahifalar orasida takrorlanishi yoki yo'qolishi mumkin.

**Spring'da qayerda uchraydi:** Spring Data: `Pageable`, `PageRequest.of(page, size, Sort.by(...))`, qaytarish turlari `Page<T>` (umumiy son uchun qo'shimcha `count` query bajaradi) va `Slice<T>` (faqat "keyingisi bormi" ni biladi, count query yo'q). Controller'da `@PageableDefault(size = 20)` va `PageableHandlerMethodArgumentResolver` so'rov parametrlarini avtomatik bind qiladi (`?page=0&size=20&sort=createdAt,desc`); `spring.data.web.pageable.max-page-size` bilan yuqori chegara qo'yiladi. Spring HATEOAS `PagedModel` + `PagedResourcesAssembler` HAL javobida `page` metadata va navigatsiya havolalarini qo'shadi.

**Qo'llanish keyslari:**
- Admin/backoffice jadvallar: foydalanuvchi sahifa raqamlarini ko'radi va ixtiyoriy sahifaga o'tadi.
- Kichik yoki o'rta hajmli, nisbatan statik ma'lumot to'plamlari (ma'lumotnoma jadvallari, konfiguratsiya ro'yxatlari).
- Qidiruv natijalari, bu yerda "N natija topildi" ko'rsatish mahsulot talabi.
- Hisobot eksportlari uchun bosqichma-bosqich o'qish, agar hajm cheklangan bo'lsa.
- Prototip va ichki vositalar, bu yerda `Page<T>` bilan tezkor ishga tushirish muhim.

**Ehtiyot bo'ling:** Chuqur pagination (yuz minglab offset) DB'ni jiddiy sekinlashtiradi, `Page<T>`'ning `count(*)` query'si esa katta jadvalda alohida og'ir operatsiya - bunday holatda `Slice<T>` yoki keyset pagination'ga o'ting. `size` parametriga yuqori chegara qo'ymaslik - bu klassik DoS vektori.

```java
// Offset pagination: oddiy, lekin chuqur sahifada sekin
@GetMapping("/orders")
Page<OrderDto> list(@PageableDefault(size = 20, sort = "createdAt") Pageable pageable) {
    return repo.findAll(pageable).map(OrderDto::of);
}
// OFFSET 100000 LIMIT 20 - baza 100020 qatorni o'qib 20 tasini qaytaradi.
// Ikkinchi muammo: yangi yozuv qo'shilsa sahifalar siljiydi va yozuv ikki
// marta yoki umuman ko'rinmaydi. Katta jadval uchun keyset ishlatilsin.
```

## 7.7 Keyset / kursor pagination (Keyset / Cursor Pagination)

**Tavsif:** Offset o'rniga oxirgi ko'rilgan element qiymati (keyset) yoki uni kodlagan opaque cursor ishlatiladi: `WHERE (created_at, id) < (:lastCreatedAt, :lastId) ORDER BY created_at DESC, id DESC LIMIT n`. Natijada so'rov indeks bo'yicha to'g'ridan-to'g'ri kerakli joyga tushadi va ishlash vaqti sahifa chuqurligiga bog'liq bo'lmaydi; bir vaqtda yangi yozuvlar qo'shilsa ham elementlar takrorlanmaydi yoki o'tkazib yuborilmaydi. Shart - tartiblash kaliti aniq (deterministik) va unikal bo'lishi, shuning uchun odatda oxiriga `id` qo'shiladi.

**Spring'da qayerda uchraydi:** Spring Data 3.1+ (Spring Boot 3.1+) `Window<T>` va `ScrollPosition` API'si: repository metodi `Window<Order> findFirst20ByStatusOrderByCreatedAtDesc(Status s, ScrollPosition position)` shaklida, `ScrollPosition.keyset()`, `ScrollPosition.offset()`, `ScrollPosition.of(keys, Direction.FORWARD)`; `window.hasNext()` va `window.positionAt(index)` keyingi cursor'ni beradi. `Limit.of(n)` qaytarilayotgan natija sonini cheklaydi. Shuningdek `Slice<T>` oddiyroq variant sifatida, Querydsl/`Specification` esa qo'lda keyset predikatini qurish uchun. Cursor'ni tashqariga berishda uni Base64 bilan opaque qilish amaliyoti keng tarqalgan.

**Qo'llanish keyslari:**
- Cheksiz scroll (infinite scroll) feed'lari: lenta, bildirishnomalar, chat tarixi.
- Katta hajmli audit log yoki event stream'ni ketma-ket o'qish (ETL, data sync).
- Webhook yoki integratsiya iste'molchilari uchun "oxirgi ko'rilgan joydan davom etish" semantikasi.
- Yuqori yozuv tezligiga ega jadvallar, bu yerda offset pagination dublikat/yo'qotish beradi.
- Mobil API'lar, bu yerda umumiy sahifa soni kerak emas, lekin barqaror ishlash muhim.

**Ehtiyot bo'ling:** Keyset bilan ixtiyoriy sahifaga sakrash va umumiy sahifa sonini ko'rsatish mumkin emas - agar UI shuni talab qilsa, pattern mos emas. Cursor'ni shaffof (ochiq) qilib bersangiz, klientlar uni qo'lda qurishga urinadi va ichki tartiblash kalitini o'zgartirish imkoniyatini yo'qotasiz; tartiblash maydoni nullable bo'lsa, keyset predikati noto'g'ri natija berishi mumkin.

```java
// Keyset pagination: kursor oxirgi ko'rilgan qiymat
public interface OrderRepository extends Repository<Order, Long> {
    @Query("""
           SELECT o FROM Order o
           WHERE (o.createdAt, o.id) < (:afterAt, :afterId)
           ORDER BY o.createdAt DESC, o.id DESC
           """)
    List<Order> pageAfter(Instant afterAt, long afterId, Limit limit);
}
// Indeks (created_at DESC, id DESC) bo'lsa, 1-sahifa ham 10000-sahifa ham
// bir xil tezlikda ishlaydi. Kursor base64 qilib mijozga berilsin.
```

## 7.8 Filtrlash, tartiblash va maydon tanlash (Filtering, Sorting, Field Selection)

**Tavsif:** Kolleksiya resurslariga so'rov parametrlari orqali shart (`?status=PAID&createdAfter=...`), tartib (`?sort=createdAt,desc`) va qaytariladigan maydonlar to'plamini (`?fields=id,total,status` - partial response) uzatish imkonini beradi. Bu klientga kerakli ma'lumotni bitta so'rovda olishga yo'l ochadi va over-fetching'ni kamaytiradi; sparse fieldsets JSON:API spetsifikatsiyasida ham standartlashtirilgan. Server tomonida har bir ruxsat etilgan filtr/sort maydoni ongli ravishda whitelist qilinishi kerak.

**Spring'da qayerda uchraydi:** `@RequestParam` va DTO'ga bind qilish (`@ModelAttribute` yoki Spring 6.1+ `@ModelAttribute`-siz constructor binding); Spring Data JPA `Specification<T>` + `JpaSpecificationExecutor`, Querydsl `Predicate` va `QuerydslPredicateExecutor` (`@QuerydslPredicate(root = Order.class)` controller argumenti sifatida); `Sort` va `Sort.TypedSort` tartib uchun; `Example`/`QueryByExampleExecutor` oddiy holatlar uchun. Maydon tanlash uchun: Spring Data projection interfeyslari va `@Query` DTO projection, Jackson `@JsonView` + `@JsonView` controller'da, `MappingJacksonValue` bilan `SimpleBeanPropertyFilter`/`@JsonFilter` dinamik filtrlash. GraphQL muqobil sifatida - Spring for GraphQL.

**Qo'llanish keyslari:**
- Admin jadvallar: ustun bo'yicha tartiblash va bir nechta filtrni birlashtirish.
- Mobil klientlar uchun yengil javoblar: ro'yxat ko'rinishida faqat 4-5 maydon qaytarish.
- Hisobot va analitika ekranlari, bu yerda sana oralig'i va status bo'yicha filtr asosiy funksional.
- Partner API'larda "so'rovni toraytirish" imkoniyati, server yukini kamaytirish uchun.
- Bir xil resursning list va detail ko'rinishlarini bitta endpoint bilan `@JsonView` orqali boshqarish.

**Ehtiyot bo'ling:** Filtr va sort maydonlarini whitelist qilmasdan to'g'ridan-to'g'ri entity property'siga bog'lash ma'lumot oshkor qilish (masalan, `?sort=passwordHash`) va indekssiz maydon bo'yicha og'ir skan xavfini tug'diradi - `QuerydslBinderCustomizer` yoki aniq DTO bilan cheklang. Juda moslashuvchan filtr tili (ixtiyoriy `AND/OR` ifodalar) tezda o'z-o'zidan query tiliga aylanadi va keshlashni deyarli imkonsiz qiladi; bunday talab ko'p bo'lsa GraphQL'ni ko'rib chiqing.

```java
// Oq ro'yxat: faqat ruxsat etilgan maydon bo'yicha saralash va filtr
private static final Set<String> SORTABLE = Set.of("createdAt", "total", "status");

@GetMapping("/orders")
List<OrderDto> list(@RequestParam(required = false) OrderStatus status,
                    @RequestParam(defaultValue = "createdAt") String sort,
                    @RequestParam(defaultValue = "20") @Max(100) int limit) {
    if (!SORTABLE.contains(sort)) throw new InvalidSortException(sort);
    return service.search(status, sort, limit);
}
// Foydalanuvchi bergan ustun nomini to'g'ridan-to'g'ri SQL ga qo'ymang
```

## 7.9 Idempotentlik kaliti (Idempotency Key)

**Tavsif:** Tabiatan idempotent bo'lmagan `POST` operatsiyalarini xavfsiz qayta urinishga (retry) yaroqli qilish mexanizmi: klient so'rov bilan birga unikal kalit (odatda UUID) `Idempotency-Key` header'ida yuboradi, server esa bu kalitni saqlab, takroriy so'rovda operatsiyani qayta bajarmasdan avvalgi javobni qaytaradi. Bu tarmoq timeout'lari, gateway retry'lari va at-least-once message delivery sharoitida ikki marta to'lov yoki ikki marta buyurtma muammosini oldini oladi. To'liq implementatsiya kalit bilan birga so'rov tanasining hash'ini ham saqlaydi va bir xil kalit bilan boshqa payload kelsa `422`/`409` qaytaradi.

**Spring'da qayerda uchraydi:** Standart Spring annotatsiyasi yo'q - pattern qo'lda quriladi: `HandlerInterceptor` yoki `OncePerRequestFilter` kalitni ushlab, saqlangan javobni qaytaradi; holat uchun `JdbcTemplate`/JPA jadvali unikal constraint bilan yoki `RedisTemplate`/`StringRedisTemplate` TTL bilan (`setIfAbsent` - `SET NX`). Tranzaksiya bilan birlashtirish uchun `@Transactional` va DB'dagi unikal indeks eng ishonchli variant. Spring Integration'da `IdempotentReceiverInterceptor` va `MetadataStore` (`RedisMetadataStore`, `JdbcMetadataStore`) xabar oqimlari uchun shu patternning tayyor shakli; Spring Modulith event publication registry esa event yetkazishda takrorlanishni boshqaradi. Klient tomonida `RestClient`/`WebClient` interceptor'i kalitni avtomatik qo'shadi.

**Qo'llanish keyslari:**
- To'lov va pul o'tkazmalarini yaratish: bir xil kalit bilan ikki so'rov bitta tranzaksiya hosil qiladi.
- Buyurtma joylash (checkout), bu yerda foydalanuvchi tugmani ikki marta bosishi mumkin.
- Kafka yoki SQS iste'molchilari: at-least-once yetkazishda xabarni ikki marta ishlashni oldini olish.
- Tashqi provayder webhook'larini qabul qilish - provayder retry qiladi, siz esa bir marta bajarishingiz kerak.
- API Gateway yoki service mesh avtomatik retry yoqilgan har qanday yozuv (write) endpointi.

**Ehtiyot bo'ling:** Kalitni faqat keshda (TTL bilan) saqlash va biznes tranzaksiyasini alohida bajarish race condition qoldiradi - kalit yozilishi va asosiy operatsiya bir atomik chegarada (bitta DB tranzaksiyasi yoki unikal constraint) bo'lishi kerak. Kalitni server generatsiya qilishi patternni buzadi: kalit klient tomonidan, retry'lar orasida o'zgarmas bo'lishi shart; TTL ni juda qisqa qo'yish esa kech kelgan retry'ni dublikatga aylantiradi.

```java
// Idempotentlik kaliti: takroriy so'rov ikkinchi marta bajarilmaydi
@PostMapping("/payments")
ResponseEntity<Receipt> pay(@RequestHeader("Idempotency-Key") @NotBlank String key,
                            @RequestBody PaymentRequest req) {
    return store.find(key)
            .map(ResponseEntity::ok)                       // avvalgi natija
            .orElseGet(() -> {
                Receipt r = service.charge(req);
                store.save(key, r, Duration.ofHours(24));  // TTL bilan
                return ResponseEntity.status(201).body(r);
            });
}
// Kalitni unique indeks bilan qo'riqlang: parallel ikki so'rov ham tutilsin
```

## 7.10 Problem Details - standart xato formati (Problem Details, RFC 9457)

**Tavsif:** HTTP xatolari uchun mashina o'qiy oladigan yagona JSON formati: `type` (xato turini aniqlovchi URI), `title`, `status`, `detail`, `instance`, hamda ixtiyoriy kengaytma maydonlari. Media type - `application/problem+json`. Bu har bir xizmat o'z xato sxemasini ixtiro qilishini to'xtatadi va klientlarga xatolarni `type` bo'yicha programmatik ishlashga imkon beradi (RFC 9457 oldingi RFC 7807'ni almashtirdi va `errors` kabi bir nechta muammoni ko'rsatish yondashuvini aniqlashtirdi).

**Spring'da qayerda uchraydi:** Spring Framework 6+: `ProblemDetail` sinfi, `ErrorResponse`/`ErrorResponseException` interfeysi, `ResponseEntityExceptionHandler` built-in Spring exception'larni `ProblemDetail`'ga aylantiradi; `spring.mvc.problemdetails.enabled=true` (WebFlux uchun `spring.webflux.problemdetails.enabled=true`) global yoqadi. Maxsus xatolar uchun `@ControllerAdvice`/`@RestControllerAdvice` + `@ExceptionHandler` metodidan `ProblemDetail` qaytarish, `setProperty("traceId", ...)` bilan kengaytma maydonlari qo'shish. Validatsiya xatolari `MethodArgumentNotValidException` dan kelib, `MessageSource` orqali lokalizatsiya qilinadi. Spring Security 6'da `AuthenticationEntryPoint`/`AccessDeniedHandler` ni shu formatga moslash kerak bo'ladi.

**Qo'llanish keyslari:**
- Platforma darajasida yagona xato shartnomasi: barcha mikroservislar bir xil struktura qaytaradi.
- Validatsiya xatolarini maydon-maydon qaytarish (`errors` kengaytmasi) frontend form'lari uchun.
- `traceId`/`correlationId` ni xato javobiga qo'shib, support murojaatini log bilan bog'lash.
- Partner API'da xato kodlarini `type` URI sifatida dokumentatsiyalash, klient esa shu bo'yicha retry/ko'rsatma logikasini qurish.
- Gateway darajasidagi xatolarni (rate limit, auth) ham upstream xizmatlar formatiga moslash.

**Ehtiyot bo'ling:** `detail` maydoniga stack trace, SQL matni yoki ichki identifikatorlarni tushirish - ma'lumot oshkor qilish xavfi; foydalanuvchiga mo'ljallangan matn va ichki diagnostika aniq ajratilishi kerak. Shuningdek, 4xx va 5xx larni farqsiz `500 ProblemDetail` ga aylantirish klientning retry qarorini buzadi - status kodni domen xatosiga to'g'ri mapping qiling.

```java
@RestControllerAdvice
class ApiExceptionHandler {

    @ExceptionHandler(InsufficientFundsException.class)
    ProblemDetail onInsufficientFunds(InsufficientFundsException e) {
        ProblemDetail p = ProblemDetail.forStatus(HttpStatus.CONFLICT);
        p.setType(URI.create("https://errors.example.com/insufficient-funds"));
        p.setTitle("Hisobda mablag' yetarli emas");
        p.setProperty("accountId", e.accountId());   // mashina o'qiydigan tafsilot
        return p;                                    // application/problem+json
    }
}
// Stack trace va ichki xabar tashqariga chiqmasligi kerak
```

## 7.11 Shartli so'rovlar va ETag (Conditional Requests / ETag)

**Tavsif:** Resurs versiyasini `ETag` (kontent hash yoki versiya) yoki `Last-Modified` header'i bilan belgilash va klientga shartli so'rov yuborish imkonini berish. `If-None-Match` bilan GET o'zgarmagan bo'lsa `304 Not Modified` qaytariladi - tarmoq trafigi va serializatsiya tejaladi; `If-Match` bilan PUT/PATCH/DELETE yuborilsa va ETag mos kelmasa `412 Precondition Failed` qaytariladi - bu HTTP darajasidagi optimistik locking bo'lib, "oxirgi yozgan g'olib" (lost update) muammosini hal qiladi.

**Spring'da qayerda uchraydi:** `ShallowEtagHeaderFilter` javob tanasidan MD5 asosida ETag hisoblaydi (trafikni tejaydi, lekin ishlov berishni emas). Aniq boshqarish uchun `ResponseEntity.ok().eTag("\"v3\"").lastModified(instant).body(...)` va `ServletWebRequest.checkNotModified(etag)` / `WebRequest.checkNotModified(lastModified)` - true qaytarsa controller darhol `304` bilan tugaydi. `@RequestHeader("If-Match")` qiymatini JPA `@Version` (optimistic locking) maydoni bilan solishtirish amaliy yondashuv; mos kelmasa `OptimisticLockingFailureException` dan `412` ga mapping qilinadi. Statik resurslar uchun `WebContentGenerator`/`ResourceHttpRequestHandler` va `spring.web.resources.cache.cachecontrol.*` sozlamalari, `CacheControl` builder'i bilan birga.

**Qo'llanish keyslari:**
- Tez-tez o'qiladigan, kam o'zgaradigan resurslar (konfiguratsiya, katalog, profil) uchun trafikni kamaytirish.
- Hamkorlikdagi tahrirlash: ikki foydalanuvchi bir hujjatni o'zgartirganda `If-Match` bilan konfliktni aniqlash.
- Mobil klientlar: cheklangan tarmoqda `304` javoblar bilan batareya va trafik tejash.
- CDN va reverse proxy bilan validatsiyaga asoslangan keshlash (`Cache-Control: no-cache` + ETag).
- REST API ustida optimistik locking: JPA `@Version` qiymatini ETag sifatida tashqariga chiqarish.

**Ehtiyot bo'ling:** `ShallowEtagHeaderFilter` javobni to'liq buferlab hash hisoblaydi - ya'ni server ishini tejamaydi va katta javoblarda xotira hamda streaming (SSE, file download) bilan muammo tug'diradi; uni streaming endpointlarda yoqmang. ETag'ni serializatsiya tartibiga bog'liq hash'dan olish (Jackson maydon tartibi, timestamp formati o'zgarishi) soxta cache miss'ga olib keladi - barqaror versiya raqamidan foydalanish ishonchliroq.

```java
@GetMapping("/orders/{id}")
ResponseEntity<OrderDto> get(@PathVariable long id) {
    Order order = service.load(id);
    // Versiya ustunidan ETag: bir xil versiya -> bir xil teg
    return ResponseEntity.ok()
            .eTag("\"" + order.version() + "\"")
            .body(OrderDto.of(order));
}

@PutMapping("/orders/{id}")
ResponseEntity<Void> update(@PathVariable long id,
                            @RequestHeader("If-Match") String ifMatch,
                            @RequestBody UpdateOrder cmd) {
    // Optimistik lock: boshqa kishi o'zgartirgan bo'lsa 412 qaytadi
    service.update(id, cmd, Long.parseLong(ifMatch.replace("\"", "")));
    return ResponseEntity.noContent().build();
}
```

## 7.12 HTTP keshlash sarlavhalari (HTTP Caching Headers)

**Tavsif:** Server javobga `Cache-Control`, `ETag`, `Last-Modified` sarlavhalarini qo'shib, client va oraliq proxy'larga javobni qancha vaqt va qanday shartlar bilan saqlash mumkinligini aytadi. Keyingi so'rovda client `If-None-Match` yoki `If-Modified-Since` yuboradi va server o'zgarish bo'lmasa `304 Not Modified` qaytaradi - body umuman uzatilmaydi. Bu network trafigini, latency'ni va backend yuklamasini bir vaqtda kamaytiradi. Shartli so'rovlar yozish operatsiyalarida optimistic concurrency uchun ham ishlatiladi (`If-Match` bilan `412 Precondition Failed`).

**Spring'da qayerda uchraydi:** `org.springframework.http.CacheControl` (`CacheControl.maxAge(Duration)`, `.noStore()`, `.cachePublic()`) va `ResponseEntity.ok().cacheControl(...).eTag("\"v3\"").body(...)`. Shartli so'rovni qo'lda tekshirish uchun `ServletWebRequest#checkNotModified(String etag)` yoki `checkNotModified(long lastModified)`. Butun ilova uchun `ShallowEtagHeaderFilter` (`OncePerRequestFilter` vorisi) MD5 asosida ETag generatsiya qiladi; static resurslar uchun `WebMvcConfigurer#addResourceHandlers` bilan `ResourceHandlerRegistration#setCacheControl` va `ResourceChainRegistration#addResolver(new VersionResourceResolver())`. Spring Security'ning default `CacheControlHeadersWriter` barcha javobga `no-cache, no-store` qo'yadi - keshlash kerak bo'lsa `http.headers(h -> h.cacheControl(HeadersConfigurer.CacheControlConfig::disable))` orqali o'chiriladi. JPA `@Version` maydoni ETag qiymati uchun tabiiy manba.

**Qo'llanish keyslari:**
- Mahsulot katalogi yoki referens ma'lumotlar (davlatlar, valyutalar) uchun `Cache-Control: public, max-age=3600` qo'yib CDN'da keshlash.
- Mobil ilova uchun og'ir JSON ro'yxatga ETag berib, o'zgarmaganda `304` bilan mobil trafikni tejash.
- `PUT /orders/{id}` da `If-Match` talab qilib, bir vaqtda ikki operator tahririda lost update'ni oldini olish.
- SPA'ning hashlangan JS/CSS bundle'lariga `max-age=31536000, immutable`, `index.html` ga esa `no-cache` berish.
- Token, hisob balansi yoki shaxsiy ma'lumot qaytaruvchi endpoint'larga `Cache-Control: no-store` majburlash.

**Ehtiyot bo'ling:** Shaxsiy (per-user) javobga `public` qo'yish eng xavfli xato - shared proxy yoki CDN bir foydalanuvchi ma'lumotini boshqasiga beradi; bunday holatda `private` yoki `no-store` va `Vary: Authorization` ishlating. `ShallowEtagHeaderFilter` butun javob body'sini xotirada buferlab hash hisoblaydi, shuning uchun streaming, katta fayl yoki yuqori RPS endpoint'larda u foyda emas, zarar keltiradi.

```java
// O'zgarmas resurs: uzoq kesh. O'zgaruvchan: qisqa yoki tekshiruv bilan.
@GetMapping("/currencies")
ResponseEntity<List<Currency>> currencies() {
    return ResponseEntity.ok()
            .cacheControl(CacheControl.maxAge(Duration.ofHours(12)).cachePublic())
            .body(service.all());
}

@GetMapping("/accounts/{id}/balance")
ResponseEntity<Balance> balance(@PathVariable long id) {
    return ResponseEntity.ok()
            .cacheControl(CacheControl.noStore())    // shaxsiy va tez o'zgaradi
            .body(service.balance(id));
}
```

## 7.13 So'rov tezligini cheklash (Rate Limiting)

**Tavsif:** Rate limiting ma'lum vaqt oynasida bitta client (API key, foydalanuvchi, IP, tenant) bajara oladigan so'rov sonini cheklaydi va limit oshganda `429 Too Many Requests` qaytaradi. Eng ko'p ishlatiladigan algoritm - token bucket: bucket'da sanab turilgan token'lar bo'ladi, har so'rov bitta token oladi, token'lar belgilangan tezlikda to'ldiriladi, bu esa qisqa burst'larga yo'l berib o'rtacha tezlikni ushlab turadi. Maqsad - resursni adolatli bo'lish, abuse va noyob quota'li tashqi API'larni himoya qilish.

**Spring'da qayerda uchraydi:** Bucket4j (`com.bucket4j:bucket4j-core`) - `Bucket`, `Bandwidth.builder().capacity(100).refillGreedy(100, Duration.ofMinutes(1))`, `bucket.tryConsumeAndReturnRemaining(1)` → `ConsumptionProbe` orqali `X-Rate-Limit-Remaining` va `Retry-After` hisoblash. Distributed holatda `bucket4j-redis` (Lettuce/Jedis `LettuceBasedProxyManager`) yoki `bucket4j-hazelcast` bilan bucket state'i node'lar orasida bo'lishiladi; `bucket4j-spring-boot-starter` (community) `application.yml` da deklarativ konfiguratsiya beradi. Amalga oshirish nuqtasi odatda `HandlerInterceptor`/`OncePerRequestFilter` yoki Spring Security filter chain. Resilience4j'ning `RateLimiter` va `@RateLimiter` annotatsiyasi ko'proq outbound chaqiruvlarni bo'g'ish uchun qulay. Spring Cloud Gateway'da `RequestRateLimiter` GatewayFilter + `RedisRateLimiter` va `KeyResolver` bean'i gateway darajasida ishlaydi.

**Qo'llanish keyslari:**
- Public API'da tarif rejasiga qarab har API key uchun soatiga 1 000 / 10 000 so'rov quota'si.
- Login va parolni tiklash endpoint'larida IP bo'yicha credential stuffing hujumini bo'g'ish.
- SMS yoki email yuborish endpoint'ini foydalanuvchi bo'yicha cheklab xarajatni ushlab turish.
- Multi-tenant SaaS'da bitta "noisy" tenant butun cluster'ni egallab olishini oldini olish.
- Resilience4j RateLimiter bilan tashqi to'lov provayderining shartnomadagi TPS limitidan oshmaslik.

**Ehtiyot bo'ling:** In-memory bucket bir nechta instance'da limitni instance soniga ko'paytirib yuboradi - horizontal scale qilinadigan servisda Redis/Hazelcast backing majburiy. Kalit tanlashda ehtiyot bo'ling: faqat IP bo'yicha cheklash NAT yoki korporativ proxy ortidagi minglab foydalanuvchini bitta sifatida ko'radi, shuning uchun autentifikatsiyadan keyin tenant/user kaliti afzal; `429` bilan albatta `Retry-After` qaytaring, aks holda client'lar darhol qayta urinib yuklamani kuchaytiradi.

```java
// Rate limit: chegara va qolgan miqdor header'da e'lon qilinadi
@Component
class RateLimitFilter extends OncePerRequestFilter {
    private final RateLimiterRegistry registry;

    @Override
    protected void doFilterInternal(HttpServletRequest req, HttpServletResponse res,
                                    FilterChain chain) throws IOException, ServletException {
        RateLimiter limiter = registry.rateLimiter(apiKeyOf(req));
        if (!limiter.acquirePermission()) {
            res.setStatus(429);
            res.setHeader("Retry-After", "60");
            return;
        }
        chain.doFilter(req, res);
    }
}
```

## 7.14 Bulk / Batch endpoint'lar (Bulk / Batch Endpoints)

**Tavsif:** Bitta element uchun N marta HTTP chaqiruv qilish o'rniga, client bir so'rovda ko'p elementni yuboradi yoki so'raydi va server ularni to'plam sifatida qayta ishlaydi. Bu network round-trip, TLS handshake va per-request overhead'ni keskin kamaytiradi, DB tomonida esa batch insert/update imkonini beradi. Muhim dizayn qarori - qismiy muvaffaqiyat semantikasi: butun batch bitta tranzaksiyada "hammasi yoki hech nima" bo'ladimi, yoki har element uchun alohida natija qaytaruvchi `207 Multi-Status` uslubidami.

**Spring'da qayerda uchraydi:** Controller'da `@PostMapping("/orders/bulk")` + `@RequestBody @Valid List<CreateOrderRequest>` yoki wrapper DTO (`BulkRequest<T>` ichida `List<T> items`) va `@Validated` bilan `@Size(max = 500)` cheklovi. Javob uchun odatda `ResponseEntity<BulkResponse>` - har element bo'yicha `index`, `status`, `error`. Persist qatlamida `JdbcTemplate#batchUpdate(String, BatchPreparedStatementSetter)`, `JdbcClient` (Spring Framework 6.1+), `NamedParameterJdbcTemplate#batchUpdate`, yoki JPA'da `spring.jpa.properties.hibernate.jdbc.batch_size`, `order_inserts`, `order_updates` sozlamalari va `EntityManager#flush()`/`clear()` bilan chunking. `SimpleJpaRepository#saveAll` o'zi batch'ni yoqmaydi - yuqoridagi Hibernate property'lar kerak. Element darajasidagi tranzaksiya izolyatsiyasi uchun `TransactionTemplate` yoki `@Transactional(propagation = Propagation.REQUIRES_NEW)` ichki servis metodida. Juda katta hajm uchun Spring Batch (`Job`, `Step`, `ItemWriter`) yoki async job pattern'iga o'tiladi.

**Qo'llanish keyslari:**
- CRM'ga CSV'dan 10 000 kontakt import qilishda chunk'lab bulk create chaqirish.
- IoT qurilmalaridan kelgan o'lchov paketlarini bitta `POST /measurements:batch` bilan qabul qilish.
- Mobil ilova offline'da yiqqan o'zgarishlarni sinxronlashda bitta batch so'rov yuborishi.
- `GET /users?ids=1,2,3,...` bilan N+1 mijoz chaqiruvini bitta lookup'ga aylantirish.
- Ombor tizimida narxlarni kunlik yangilashda bulk update endpoint'i.

**Ehtiyot bo'ling:** Batch hajmini cheklamasa, bitta so'rov butun heap'ni yeb qo'yadi yoki timeout'ga uchraydi - `@Size` validatsiyasi va `server.tomcat.max-http-form-post-size`/`spring.codec.max-in-memory-size` kabi chegaralar majburiy. Qismiy muvaffaqiyatni `200 OK` ichida yashirmang: client qaysi element yiqilganini aniq bilishi kerak, aks holda retry butun batch'ni takrorlab duplicate yaratadi - shu sababli idempotency key bilan birga qo'llash tavsiya etiladi.

```java
// Batch endpoint: har element uchun alohida natija qaytariladi
public record BatchResult<T>(int index, boolean ok, T value, ProblemDetail error) {}

@PostMapping("/orders/batch")
ResponseEntity<List<BatchResult<OrderDto>>> batch(@RequestBody @Size(max = 100)
                                                  List<CreateOrder> commands) {
    List<BatchResult<OrderDto>> results = new ArrayList<>();
    for (int i = 0; i < commands.size(); i++) {
        try { results.add(new BatchResult<>(i, true, service.create(commands.get(i)), null)); }
        catch (ApiException e) { results.add(new BatchResult<>(i, false, null, e.toProblem())); }
    }
    return ResponseEntity.status(207).body(results);   // 207 Multi-Status
}
```

## 7.15 Asinxron so'rov-javob (Asynchronous Request-Reply)

**Tavsif:** Uzoq davom etadigan ishni HTTP so'rovi ichida kutib turish o'rniga, server ishni navbatga qo'yib darhol `202 Accepted` va `Location: /jobs/{id}` sarlavhasini qaytaradi. Client keyin shu status resursini polling qilib `PENDING → RUNNING → SUCCEEDED/FAILED` holatini kuzatadi va tugagach natija resursiga (`303 See Other` yoki javobdagi `resultUrl`) o'tadi. Bu pattern HTTP timeout'lari, load balancer cheklovlari va thread'larni uzoq ushlab turish muammosini hal qiladi.

**Spring'da qayerda uchraydi:** Controller `ResponseEntity.accepted().location(uri).body(jobDto)` qaytaradi; ish `@Async` metod + `ThreadPoolTaskExecutor` (yoki Java 21+ virtual thread'lar uchun `SimpleAsyncTaskExecutor` `setVirtualThreads(true)` bilan), aniqrog'i esa durable navbat - `@RabbitListener`, `@KafkaListener` yoki `JmsTemplate` - orqali bajariladi. Job holati DB'da entity sifatida saqlanadi (`JobEntity` + `JobRepository`), status endpoint `@GetMapping("/jobs/{id}")`. Tranzaksiya bilan bog'lash uchun `@TransactionalEventListener(phase = AFTER_COMMIT)` yoki transactional outbox. Spring Batch ishlatilsa `JobLauncher` (`TaskExecutorJobLauncher`) + `JobExplorer`/`JobOperator` holatni beradi; Spring Modulith'da `@ApplicationModuleListener` ishonchli async yetkazib berishni ta'minlaydi.

**Qo'llanish keyslari:**
- Katta hisobotni (PDF/Excel) generatsiya qilib S3'ga yuklash va natija link'ini qaytarish.
- Video yoki rasmni transcode qilish, thumbnail yaratish pipeline'i.
- Million qatorli CSV import yoki migratsiya job'ini ishga tushirish.
- Tashqi KYC/skoring provayderidan javob daqiqalar davomida kelganda.
- ML modeli bilan batch inference yoki katta analitik query'ni bajarish.

**Ehtiyot bo'ling:** Job'ni in-memory executor'da saqlash eng keng tarqalgan xato - pod restart bo'lsa ish ham, holat ham yo'qoladi; durable store va navbat ishlating. Status endpoint'ga `Cache-Control: no-store` qo'ying, polling intervalini `Retry-After` bilan boshqaring, job'ga TTL va retry chegarasi bering, hamda `POST` ni idempotency key bilan himoya qilmasangiz client retry'si bir xil ishni ikki marta tushiradi.

```java
// Asinxron so'rov-javob: 202 + holatni kuzatish havolasi
@PostMapping("/reports")
ResponseEntity<Void> request(@RequestBody ReportRequest req) {
    String jobId = jobs.submit(req);
    return ResponseEntity.accepted()
            .location(URI.create("/reports/jobs/" + jobId))
            .build();
}

@GetMapping("/reports/jobs/{id}")
ResponseEntity<?> status(@PathVariable String id) {
    JobStatus s = jobs.status(id);
    return s.done()
            ? ResponseEntity.status(303).location(s.resultUri()).build()
            : ResponseEntity.ok(s);
}
```

## 7.16 Uzoq polling (Long Polling)

**Tavsif:** Client so'rov yuboradi, server esa yangi ma'lumot paydo bo'lmaguncha (yoki timeout tugamaguncha) javobni ochiq ushlab turadi, so'ng javob qaytaradi va client darhol yangi so'rov ochadi. Bu oddiy short polling'ning behuda bo'sh javoblarini yo'q qiladi va WebSocket'ga o'tmasdan deyarli real-time yetkazib berish beradi. Asosiy shart - server thread'ni block qilmaslik, ya'ni so'rov async ravishda "to'xtatilishi" kerak.

**Spring'da qayerda uchraydi:** Spring MVC'da controller `DeferredResult<T>` yoki `CompletableFuture<T>` qaytaradi - Servlet 3.1 async orqali container thread bo'shatiladi; `DeferredResult#setResult`, `setErrorResult`, `onTimeout(Runnable)` va `spring.mvc.async.request-timeout` sozlamasi. Server→client oqimi kerak bo'lsa `SseEmitter` yoki `ResponseBodyEmitter` (`text/event-stream`) ko'pincha long polling'dan afzal. WebFlux'da `Mono<T>`/`Flux<ServerSentEvent<T>>` va `Sinks.Many` (`Sinks.many().multicast().onBackpressureBuffer()`) bilan tabiiy non-blocking yechim chiqadi; `Mono#timeout(Duration)` chegara qo'yadi. Ko'p instance'da event'ni barcha kutayotgan so'rovlarga tarqatish uchun Redis Pub/Sub (`ReactiveStringRedisTemplate#listenTo`) yoki Kafka ishlatiladi.

**Qo'llanish keyslari:**
- Async job tugashini kutish: polling o'rniga `GET /jobs/{id}/wait` long polling bilan.
- Chat yoki notification feed'i, WebSocket'ni proxy blokirovka qilgan korporativ muhitda.
- Konfiguratsiya/feature flag o'zgarishini kuzatish (Consul/etcd uslubidagi watch endpoint).
- Navbatdagi vazifani olish uchun worker'ning "take job" chaqiruvi.
- To'lov statusining provayder webhook'idan keyin yangilanishini frontend'ga tezda yetkazish.

**Ehtiyot bo'ling:** Blocking Servlet stack'da `DeferredResult` qo'llanmasa va thread'da `Thread.sleep`/`Future.get` bilan kutilsa, thread pool tez to'yinadi va butun servis javob bermay qoladi. Timeout qiymatini load balancer/ingress idle timeout'idan kichik qiling, aks holda client `504` oladi; yo'qolgan event'larga qarshi har javobda cursor yoki `lastEventId` qaytaring, bir yo'nalishli push uchun esa SSE/WebSocket aniq yaxshiroq tanlov.

```java
// Long polling: server o'zgarish bo'lguncha javobni ushlab turadi
@GetMapping("/orders/{id}/status")
public DeferredResult<OrderStatus> awaitChange(@PathVariable long id,
                                               @RequestParam OrderStatus current) {
    DeferredResult<OrderStatus> result = new DeferredResult<>(25_000L, current);
    // Timeout'da joriy holat qaytadi: mijoz qayta so'raydi
    watchers.register(id, current, result);
    result.onCompletion(() -> watchers.remove(id, result));
    return result;
}
// SSE bor joyda long polling kerak emas: u ko'proq resurs yeydi
```

## 7.17 Webhook'lar (Webhooks)

**Tavsif:** Webhook - "teskari API": client polling qilish o'rniga, hodisa yuz berganda server client'ning ro'yxatdan o'tgan HTTPS URL'iga `POST` yuboradi. Bu kechikishni minimumga tushiradi va behuda so'rovlarni yo'q qiladi, lekin yetkazib berish ishonchliligi, autentifikatsiya va qabul qiluvchi tomondagi idempotentlik mas'uliyatini keltirib chiqaradi. Ishlab chiqarishga yaroqli webhook har doim HMAC imzo, retry + exponential backoff, dead-letter va `at-least-once` semantikasini o'z ichiga oladi.

**Spring'da qayerda uchraydi:** Chiqaruvchi tomonda hodisalar `ApplicationEventPublisher` + `@TransactionalEventListener(phase = AFTER_COMMIT)` bilan ushlanadi, outbox jadvaliga yoziladi va `RestClient` (Spring Framework 6.1+) yoki `WebClient` bilan yuboriladi; retry uchun Spring Retry (`@Retryable`, `RetryTemplate`, `ExponentialBackOffPolicy`) yoki Resilience4j `Retry`, navbat uchun Rabbit'ning `x-dead-letter-exchange`/delayed exchange yoki Kafka `DefaultErrorHandler` + `DeadLetterPublishingRecoverer`. Imzo `javax.crypto.Mac` (`HmacSHA256`) bilan hisoblanadi va `X-Signature` sarlavhasida yuboriladi. Qabul qiluvchi tomonda imzoni raw body ustida tekshirish uchun `ContentCachingRequestWrapper` yoki `@RequestBody byte[]`/`String` ishlatiladi, `MessageDigest.isEqual` bilan constant-time comparison qilinadi; endpoint Spring Security'da `permitAll()` lekin CSRF'dan `ignoringRequestMatchers` orqali chiqariladi.

**Qo'llanish keyslari:**
- Stripe/PayPal uslubidagi `payment.succeeded` hodisasini qabul qilib buyurtmani tasdiqlash.
- SaaS platformasida mijoz tizimiga `invoice.created`, `user.deleted` hodisalarini push qilish.
- GitHub/GitLab webhook'i bilan CI pipeline yoki deploy'ni ishga tushirish.
- Yetkazib berish servisidan parcel status o'zgarishini real vaqtda olish.
- Ichki tizimlar o'rtasida event-driven integratsiya, broker o'rnatish imkoni bo'lmaganda.

**Ehtiyot bo'ling:** Webhook `at-least-once` - bir xil hodisa bir necha marta keladi, shuning uchun qabul qiluvchi `eventId` ni unique constraint bilan saqlab idempotent bo'lishi shart; imzoni Jackson deserializatsiya qilgan obyektdan qayta serializatsiya qilib hisoblash imzoni buzadi, faqat raw body ustida tekshiring. Yuborishni HTTP so'rov thread'ida sinxron qilmang va imzo tekshirilmagan webhook endpoint'ini hech qachon ishonchli deb qabul qilmang - bu to'g'ridan-to'g'ri SSRF/spoofing yo'li.

```java
// Webhook yuborish: imzo, retry va takrorlanishga tayyorlik
@Service
public class WebhookSender {

    public void send(Subscription sub, DomainEvent event) {
        String body = json.write(event);
        String signature = hmacSha256(sub.secret(), body);   // qabul qiluvchi tekshiradi
        rest.post().uri(sub.url())
                .header("X-Signature", signature)
                .header("X-Event-Id", event.id())            // idempotentlik uchun
                .body(body)
                .retrieve().toBodilessEntity();
    }
}
// Yetkazib berilmasa exponential backoff bilan qayta urinish va DLQ kerak
```

## 7.18 API Gateway (API Gateway)

**Tavsif:** API Gateway - barcha tashqi so'rovlar o'tadigan yakka kirish nuqtasi; u routing, TLS termination, autentifikatsiya, rate limiting, logging, retry va circuit breaking kabi cross-cutting vazifalarni servislardan tashqariga chiqaradi. Natijada har bir microservice biznes logikaga e'tibor qaratadi, client esa ichki topologiyani bilmaydi va servislarni erkin bo'laklashga yo'l ochiladi. Shuningdek protokol tarjimasi (HTTP → gRPC) va versiyalash/kanareyka routing uchun qulay nuqta.

**Spring'da qayerda uchraydi:** Spring Cloud Gateway - reaktiv `spring-cloud-starter-gateway` (Netty + WebFlux) yoki Servlet varianti `spring-cloud-starter-gateway-mvc`. Marshrutlar `application.yml` da yoki `RouteLocatorBuilder` bilan Java DSL'da tuziladi; `Predicate`'lar: `Path`, `Host`, `Method`, `Header`, `Weight`; `GatewayFilter`'lar: `RewritePath`, `StripPrefix`, `CircuitBreaker` (Resilience4j bilan), `RequestRateLimiter`, `Retry`, `TokenRelay`. Global kesishuvlar uchun `GlobalFilter` + `Ordered` interfeysi. Service discovery `spring-cloud-starter-netflix-eureka-client` yoki Kubernetes discovery bilan `lb://ORDER-SERVICE` sxemasida; xavfsizlik `spring-boot-starter-oauth2-resource-server` (JWT validatsiya) yoki `oauth2-client` + `TokenRelayGatewayFilterFactory`. Alternativ sifatida platforma darajasida Kubernetes Gateway API / Envoy ishlatiladi.

**Qo'llanish keyslari:**
- Mobil va web client'lar uchun 20+ microservice oldiga yagona `api.example.com` domeni.
- JWT ni gateway'da bir marta validatsiya qilib, ichkariga faqat ishonchli claim'larni uzatish.
- Monolitdan microservice'ga strangler fig migratsiyasida trafikni yo'l bo'yicha bo'lish.
- Kanareyka deploy: `Weight` predicate bilan trafikning 5%ini yangi versiyaga yuborish.
- Legacy SOAP yoki gRPC backend'ni tashqariga REST sifatida ko'rsatish.

**Ehtiyot bo'ling:** Gateway'ga biznes logika, ma'lumot transformatsiyasi va orkestratsiyani yiqib qo'ysangiz, u yangi distributed monolit va yakka failure point'ga aylanadi - logika servislarda yoki alohida BFF'da qolishi kerak. Reaktiv Gateway'da blocking kod yozish (JDBC, `RestTemplate`, `block()`) event loop thread'ini to'sib butun gateway throughput'ini yo'q qiladi.

```yaml
spring:
  cloud:
    gateway:
      routes:
        - id: orders
          uri: lb://orders-service
          predicates:
            - Path=/api/orders/**
          filters:
            - StripPrefix=1
            - name: RequestRateLimiter
              args:
                redis-rate-limiter.replenishRate: 100
                redis-rate-limiter.burstCapacity: 200
            - name: CircuitBreaker
              args: { name: ordersCb, fallbackUri: 'forward:/fallback/orders' }
```

## 7.19 Frontend uchun backend (Backend for Frontend, BFF)

**Tavsif:** BFF - har bir client turi (iOS, Android, web SPA, smart TV, partner portal) uchun alohida, o'ziga xos backend qatlami; u ichki servislarni chaqirib, aynan shu UI ehtiyojiga moslashtirilgan javob shaklini beradi. Bu "bitta universal API hammani qoniqtirmaydi" muammosini hal qiladi: mobil kam maydonli va kam so'rovli javob xohlaydi, web esa boshqa kesim. Har bir frontend jamoasi o'z BFF'siga egalik qilgani uchun reliz tezligi oshadi va umumiy API'da kelishuv muzokaralari kamayadi.

**Spring'da qayerda uchraydi:** BFF oddiy Spring Boot ilovasi: `@RestController` + `RestClient`/`WebClient` bilan downstream chaqiruvlar, `Mono.zip`/`CompletableFuture.allOf` yoki virtual thread'lar bilan parallel aggregatsiya, DTO'lar `record` sifatida. Juda ko'p o'zgaruvchan talab bo'lsa `spring-boot-starter-graphql` (`@QueryMapping`, `@SchemaMapping`, `BatchMapping` va `DataLoader`) BFF rolini bajaradi. Xavfsizlikda "BFF pattern" alohida ma'noga ega: SPA'da token'ni brauzerda saqlash o'rniga `spring-boot-starter-oauth2-client` bilan server-side session + `HttpOnly` cookie ishlatiladi, token esa BFF'da qoladi va `ServerOAuth2AuthorizedClientExchangeFilterFunction` orqali downstream'ga relay qilinadi; Spring Cloud Gateway `TokenRelay` filtri bilan ham shu sxema quriladi. `spring-session-data-redis` bir nechta instance uchun session'ni bo'lishadi.

**Qo'llanish keyslari:**
- Mobil ilovaning bosh ekranini bitta chaqiruvda to'ldirish uchun maxsus "home feed" endpoint'i.
- SPA uchun OAuth2 token'larni brauzerdan olib tashlab, cookie-based sessiyaga o'tish.
- Partner/B2B portali uchun ichki modelning faqat ruxsat etilgan qismini ko'rsatish.
- Smart TV yoki kiosk kabi kuchsiz client uchun og'ir hisob-kitoblarni serverga ko'chirish.
- Legacy va yangi servislarni bitta UI uchun vaqtincha birlashtirish.

**Ehtiyot bo'ling:** Har bir client uchun BFF ko'paygan sari bir xil kod nusxalanadi - umumiy mantiqni kutubxona yoki downstream domain servisiga chiqaring, aks holda 5 ta BFF'da 5 xil biznes qoida paydo bo'ladi. BFF faqat moslashtirish qatlami: u DB'ga to'g'ridan-to'g'ri yozishni yoki domain qoidalarini o'z ichiga olsa, domain mas'uliyati tarqalib ketadi.

```java
// BFF: bitta mijoz turi uchun moslashtirilgan API
@RestController
@RequestMapping("/bff/mobile")
class MobileHomeController {
    private final OrderClient orders;
    private final PromoClient promos;

    @GetMapping("/home")
    MobileHome home(@AuthenticationPrincipal Jwt jwt) {
        // Mobil ekran uchun kerakli minimal to'plam: 1 chaqiruv, kichik payload
        return new MobileHome(
                orders.lastThree(jwt.getSubject()),
                promos.activeBanner());
    }
}
```

## 7.20 API kompozitsiyasi / Aggregator (API Composition / Aggregator)

**Tavsif:** Bitta client so'rovini qondirish uchun bir nechta servisdan ma'lumot olib, ularni xotirada birlashtirib yagona javob qaytarish patterni. Microservice'larda har bir servis o'z DB'siga ega bo'lgani uchun `JOIN` imkoni yo'q - kompozitsiya shu bo'shliqni to'ldiradi. Samaradorlik uchun chaqiruvlar imkon qadar parallel bajariladi, har biriga timeout va fallback beriladi, zaruriy bo'lmagan servis yiqilsa javob qisman (degraded) qaytariladi.

**Spring'da qayerda uchraydi:** `WebClient` + `Mono.zip(...)` yoki `Flux.merge`, blocking stack'da esa Java 21+ virtual thread'lar (`spring.threads.virtual.enabled=true`) bilan `RestClient` chaqiruvlarini `StructuredTaskScope`/`ExecutorService` orqali parallel bajarish; `@Async` + `CompletableFuture.allOf(...).thenApply(...)` klassik varianti. Chidamlilik uchun `spring-cloud-starter-circuitbreaker-resilience4j` va `@CircuitBreaker(fallbackMethod = "...")`, `@TimeLimiter`, `@Bulkhead`. GraphQL'da `spring-boot-starter-graphql`ning `@BatchMapping` va `DataLoader`'i N+1 chaqiruvni partiyaga aylantiradi. Og'ir read model kerak bo'lsa CQRS tomon siljib, `@KafkaListener` bilan read-model'ni oldindan yiqish (materialized view) kompozitsiyani umuman olib tashlaydi.

**Qo'llanish keyslari:**
- Buyurtma sahifasi: order, payment, shipping va customer servislaridan bitta javob yig'ish.
- E-commerce mahsulot kartochkasi: katalog + narx + ombor qoldig'i + sharhlar reytingi.
- Dashboard'da bir necha domain metrikasini bitta `GET /overview` bilan ko'rsatish.
- Mobil "my account" ekrani uchun profil, obunalar va bonuslarni birlashtirish.
- Bank ilovasida hisoblar va oxirgi tranzaksiyalarni parallel olib ko'rsatish.

**Ehtiyot bo'ling:** Ketma-ket (sequential) chaqiruvlar latency'ni qo'shib yuboradi va eng sekin downstream butun javobni ushlaydi - parallel bajaring, har chaqiruvga alohida timeout qo'ying va kritik bo'lmaganlar uchun fallback bering. Kompozitsiyani katta ro'yxatlar ustida (`per-item` chaqiruv) qilish N+1 ga olib keladi; bunday hollarda bulk endpoint, `DataLoader` yoki materialized read model kerak.

```java
// API composition: bir nechta servisdan parallel yig'ish
@GetMapping("/customers/{id}/overview")
CustomerOverview overview(@PathVariable long id) throws InterruptedException {
    try (var scope = new StructuredTaskScope.ShutdownOnFailure()) {
        var profile = scope.fork(() -> profiles.get(id));
        var orders  = scope.fork(() -> orderClient.recent(id));
        var balance = scope.fork(() -> billing.balance(id));
        scope.join().throwIfFailed();        // bittasi yiqilsa hammasi bekor
        return new CustomerOverview(profile.get(), orders.get(), balance.get());
    }
}
```

## 7.21 Bag'rikeng o'quvchi (Tolerant Reader)

**Tavsif:** Client javobni qat'iy to'liq moslik talab qilmasdan o'qiydi: faqat o'ziga kerakli maydonlarni oladi, notanish yangi maydonlarni e'tiborsiz qoldiradi va tartib yoki qo'shimcha elementlarga bog'lanmaydi. Bu Postel qonunining integratsiyadagi ko'rinishi va API evolyutsiyasining asosiy sharti: provayder additive o'zgarish kiritganda hech bir consumer buzilmaydi. Pattern consumer tomonda minimal DTO va himoyalangan deserializatsiya bilan amalga oshiriladi.

**Spring'da qayerda uchraydi:** Jackson'da `@JsonIgnoreProperties(ignoreUnknown = true)` yoki global `ObjectMapper.configure(DeserializationFeature.FAIL_ON_UNKNOWN_PROPERTIES, false)` (Spring Boot'da bu default o'chirilgan; `Jackson2ObjectMapperBuilderCustomizer` yoki `spring.jackson.deserialization.fail-on-unknown-properties=false` bilan boshqariladi). Yangi enum qiymati kelganda yiqilmaslik uchun `@JsonEnumDefaultValue` + `READ_UNKNOWN_ENUM_VALUES_USING_DEFAULT_VALUE`. Faqat kerakli maydonlarni olish uchun `record`-DTO yoki `JsonPath`/`JsonNode` bilan selektiv o'qish; `RestClient`/`WebClient` javobini `bodyTo(MyMinimalDto.class)` ga map qilish. HATEOAS link'larini qattiq URL yozish o'rniga `Traverson` yoki `LinkDiscoverer` bilan topish ham shu falsafaga kiradi. Provayder tomonda esa `@JsonInclude(Include.NON_NULL)` va maydonni o'chirmaslik qoidasi mos keladi.

**Qo'llanish keyslari:**
- Tashqi to'lov yoki logistika provayderining tez-tez yangi maydon qo'shadigan API'sini iste'mol qilish.
- Microservice'lar orasida consumer'larni downstream release'iga bog'lanmagan holda saqlash.
- Kafka'dagi JSON event'larni schema biroz o'zgarganda ham uzilmasdan o'qish.
- Partner integratsiyasida faqat 5 ta maydon kerak bo'lgan 100 maydonli javobni o'qish.
- Legacy tizim versiyalari turlicha javob qaytarganda bitta client bilan ishlash.

**Ehtiyot bo'ling:** Bag'rikenglik "jim yutish" degani emas - majburiy maydon yo'qolganini ham e'tiborsiz qoldirsangiz, xato ma'lumot bilan ishlab noto'g'ri biznes natija chiqaradi; kerakli maydonlarni `@NotNull`/validatsiya bilan tekshiring va kutilmagan holatni log qiling. Shuningdek bu pattern breaking o'zgarishlardan himoya qilmaydi: maydon turi yoki semantikasi o'zgarsa, faqat versiyalash va contract test yordam beradi.

```java
// Tolerant reader: faqat kerakli maydonni o'qiydi, qolganiga e'tibor bermaydi
@Bean
ObjectMapper tolerantMapper() {
    return JsonMapper.builder()
            // Yangi maydon qo'shilsa integratsiya buzilmaydi
            .disable(DeserializationFeature.FAIL_ON_UNKNOWN_PROPERTIES)
            .disable(DeserializationFeature.FAIL_ON_NULL_FOR_PRIMITIVES)
            .build();
}

// Faqat kerakli maydonlar e'lon qilinadi
public record PspCallback(String reference, String status) { }
```

## 7.22 Consumer tomonidan boshqarilgan kontraktlar (Consumer-Driven Contracts)

**Tavsif:** Consumer'lar provayderdan nimani kutayotganini bajarilishi mumkin bo'lgan kontrakt sifatida yozib beradi; provayder CI'da shu kontraktlarning barchasini tekshiradi va birortasi buzilsa build yiqiladi. Bu microservice'larda to'liq end-to-end integration muhitini ko'tarmasdan breaking change'ni erta aniqlash imkonini beradi. Qo'shimcha foyda: provayder qaysi maydon haqiqatda ishlatilayotganini biladi va ishlatilmaganini xotirjam olib tashlaydi.

**Spring'da qayerda uchraydi:** Spring Cloud Contract - kontraktlar Groovy DSL, YAML yoki Kotlin DSL'da yoziladi, `spring-cloud-contract-maven-plugin`/`gradle` plugin'i provayder tomonida avtomatik test generatsiya qiladi (`RestAssured`/`MockMvc` asosida, base class `@AutoConfigureMessageVerifier`, `@AutoConfigureRestDocs` bilan birga ishlaydi) va consumer uchun stub JAR chiqaradi; consumer testida `@AutoConfigureStubRunner(ids = "com.example:order-service:+:stubs", stubsMode = StubRunnerProperties.StubsMode.LOCAL)` bilan WireMock stub'i ko'tariladi. Messaging kontraktlari uchun `spring-cloud-contract-verifier` + Kafka/Rabbit binder'lari. Alternativ va industriyada keng tarqalgan yo'l - Pact JVM (`au.com.dius.pact.provider:junit5`, `@PactTestFor`, `@Provider`, `@PactBroker`) Pact Broker bilan `can-i-deploy` tekshiruvi. OpenAPI tomonida `springdoc-openapi-starter-webmvc-ui` spec chiqaradi va buzilishni `openapi-diff` kabi vositalar aniqlaydi.

**Qo'llanish keyslari:**
- 10+ microservice'li platformada API breaking change'ni merge'dan oldin ushlash.
- Consumer jamoasi provayder stub'i bilan parallel ishlab chiqishni boshlashi (shift-left).
- Mobil app va backend o'rtasida JSON shaklini kontrakt bilan muzlatish.
- Kafka event schema'sining consumer'lar uchun mos qolishini CI'da tekshirish.
- Pact Broker'ning `can-i-deploy` bilan deploy'ni avtomatik gate qilish.

**Ehtiyot bo'ling:** Kontraktlarni to'liq funksional testga aylantirmang - ular shakl va asosiy semantikani tekshiradi, biznes logikani emas; haddan ziyod qattiq kontrakt (har maydon aniq qiymat bilan) provayderni mayda o'zgarishda ham qamoqqa oladi, shuning uchun matcher'lar (`$(consumer(...), producer(regex(...)))`) ishlatiladi. Kontrakt mas'uliyati va stub versiyalash jarayoni belgilanmagan jamoalarda bu infrastruktura tez eskirib, "yashil lekin yolg'on" testlarga aylanadi.

```java
// Consumer-driven contract: iste'molchi kutgan narsa testga aylanadi
@Pact(consumer = "orders-service", provider = "psp")
public RequestResponsePact chargePact(PactDslWithProvider builder) {
    return builder
            .given("hisobda mablag' bor")
            .uponReceiving("to'lov so'rovi")
                .path("/charge").method("POST")
            .willRespondWith()
                .status(201)
                .body(new PactDslJsonBody()
                        .stringType("reference")
                        .stringValue("status", "CAPTURED"))
            .toPact();
}
// Provayder shu kontraktni o'z CI'da tekshiradi: buzilsa uning build'i yiqiladi
```

## 7.23 Kengaytir/Qisqartir (Expand/Contract - Parallel Change)

**Tavsif:** Breaking change'ni uch bosqichga bo'lib, iste'molchilarni sindirmasdan API yoki sxemani evolyutsiya qilish usuli. Birinchi bosqichda yangi shakl qo'shiladi (expand) va eski bilan yonma-yon yashaydi, ikkinchi bosqichda barcha client'lar yangisiga ko'chiriladi (migrate), uchinchi bosqichda eskisi olib tashlanadi (contract). Bu pattern deploy'ni release'dan ajratib, nol downtime bilan rolling update qilishga imkon beradi. Asosiy shart - oraliq davrda ikkala shakl ham bir vaqtda to'g'ri ishlashi.

**Spring'da qayerda uchraydi:** Payload darajasida Jackson'ning `@JsonAlias` (eski va yangi field nomi bir vaqtda o'qiladi), `@JsonProperty`, `@JsonIgnoreProperties(ignoreUnknown = true)` va `@JsonGetter` bilan eski field'ni hisoblab chiqarish; DTO'da eski getter'ga `@Deprecated` qo'yiladi. Endpoint darajasida `@RequestMapping(produces = "application/vnd.shop.order.v2+json")` yoki alohida `/v2/...` controller'lar, `@RequestMapping(headers = "X-Api-Version=2")` ishlatiladi. Baza darajasida Flyway/Liquibase bilan additive migration (avval nullable yangi column, keyin backfill, keyin eski column drop) - Spring Boot'da `spring.flyway.*` konfiguratsiyasi. Yangi yo'lni bosqichma-bosqich yoqish uchun `@ConditionalOnProperty`, Spring Cloud Config yoki Togglz/Unleash kabi feature flag kutubxonalari qo'llanadi.

**Qo'llanish keyslari:**
- Mobil ilova client'lari bir necha oy davomida eski field nomini yuborishda davom etadigan REST API'da field nomini o'zgartirish.
- Monolitdan ajratilgan mikroservisga trafikni ko'chirishda eski va yangi endpoint'ni parallel ushlab turish.
- Baza column'ini `VARCHAR`dan normalizatsiya qilingan jadvalga ko'chirishda ikki yoqlama yozish (dual write) davri.
- Kafka event sxemasiga yangi majburiy maydon qo'shish: avval optional qilib chiqariladi, consumer'lar yangilanadi, keyin majburiyga aylantiriladi.
- gRPC proto fayliga yangi `optional` field qo'shib, eski field'ni `reserved` qilishdan oldin migratsiya oynasi berish.

**Ehtiyot bo'ling:** Eng ko'p uchraydigan xato - "contract" bosqichini hech qachon bajarmaslik: kod ikki shaklni abadiy ushlab turadi va texnik qarz to'planadi, shuning uchun har bir expand'ga deadline va iste'molchi telemetriyasi (eski field qancha so'raldi) bog'lanishi kerak. Dual write davrida ikki manba o'rtasida divergensiya paydo bo'lishi mumkin, shuning uchun reconciliation job va monitoring majburiy.

```java
// Expand/Contract: uch reliz, hech qachon ikkisini birga qilmang
// 1) EXPAND: yangi maydon qo'shiladi, eskisi ham to'ldiriladi
public record CustomerDto(
        @Deprecated String name,      // eski mijozlar uchun
        String firstName,             // yangi
        String lastName) {
    static CustomerDto of(Customer c) {
        return new CustomerDto(c.firstName() + " " + c.lastName(),
                               c.firstName(), c.lastName());
    }
}
// 2) MIGRATE: mijozlar yangi maydonga o'tadi (metrika bilan kuzatiladi)
// 3) CONTRACT: `name` olib tashlanadi
```

## 7.24 Konvert javob va yalang'och javob (Envelope vs Bare Response)

**Tavsif:** Javob tanasini metadata uchun o'rovchi obyektga (`{"data": ..., "meta": ..., "errors": ...}`) joylashtirish yoki resursning o'zini to'g'ridan-to'g'ri qaytarish o'rtasidagi tanlov. Konvert pagination, trace ID, warning va qisman xatolarni bir joyda uzatishga qulay, ammo har bir client'ni ortiqcha unwrap qilishga majbur qiladi va HTTP semantikasini (status kod, header) takrorlashga undaydi. Yalang'och javob HTTP'ni o'z protokoli sifatida ishlatadi: metadata header'larga va `Link`ga, xato esa `ProblemDetail`ga chiqadi. Qoida - bitta API ichida ikkisini aralashtirmaslik.

**Spring'da qayerda uchraydi:** Yalang'och javob `@RestController` + `ResponseEntity<T>`ning tabiiy natijasi; metadata `ResponseEntity.ok().header(...)` yoki `HttpHeaders` orqali beriladi. Konvertni markazlashtirish uchun `ResponseBodyAdvice<Object>` interfeysini amalga oshirgan `@RestControllerAdvice` yoki `MappingJacksonValue` ishlatiladi; Jackson tomonida `@JsonView` va `@JsonUnwrapped` yordam beradi. Pagination uchun Spring Data'ning `Page<T>` to'g'ridan-to'g'ri serialize qilinishi noturg'un hisoblanadi - Spring Data 3.3+ da shu maqsadda barqaror `org.springframework.data.web.PagedModel` DTO'si bor (`spring.data.web.pageable.serialization-mode` / `@EnableSpringDataWebSupport(pageSerializationMode = VIA_DTO)`), HATEOAS'da esa `PagedModel`/`CollectionModel`. Streaming javoblarda `ResponseBodyEmitter`, `SseEmitter` va `Flux<T>` konvertni amalda imkonsiz qiladi.

**Qo'llanish keyslari:**
- Ko'p tenantli public API'da har bir javobga `requestId` va rate-limit qoldig'ini qo'shish (konvert yoki header tanlovi).
- Ro'yxat endpoint'larida sahifalash metadata'sini (`totalElements`, `nextCursor`) qaytarish.
- BFF (Backend-for-Frontend) qatlamida bir nechta downstream natijasini partial failure bilan birlashtirish - bu yerda konvert oqlanadi.
- CDN yoki proxy keshlanadigan oddiy `GET /orders/{id}` uchun yalang'och JSON - `ETag` va `Cache-Control` header'lari bilan.
- SSE/stream endpoint'larida har bir element yalang'och chiqadi, umumiy konvert esa qo'llanilmaydi.

**Ehtiyot bo'ling:** Konvert ichida o'z "statusCode" yoki "success" maydonini saqlab, HTTP 200 bilan xato qaytarish anti-pattern: monitoring, retry va proxy'lar buzuladi. `ResponseBodyAdvice` bilan hamma javobni global o'rash `ProblemDetail`, `byte[]`, `Resource` va actuator endpoint'larini ham ushlab qolib sindirishi mumkin - albatta `supports()` va `MediaType` bo'yicha filtrlang.

```java
// Yalang'och javob: resurs o'zi, metadata header'da
@GetMapping("/orders/{id}")
OrderDto bare(@PathVariable long id) { return service.view(id); }

// Konvert: sahifalash yoki ogohlantirish kerak bo'lganda
public record Envelope<T>(T data, PageInfo page, List<String> warnings) {}

@GetMapping("/orders")
Envelope<List<OrderDto>> list(Pageable p) {
    Page<Order> page = repo.findAll(p);
    return new Envelope<>(page.map(OrderDto::of).getContent(),
                          PageInfo.of(page), List.of());
}
// Bitta API da ikkisini aralashtirmang: mijoz har javobni ikki xil o'qiydi
```

## 7.25 Xato javobini loyihalash (Error Response Design)

**Tavsif:** Barcha xatolarni bitta mashina o'qiy oladigan, barqaror formatga keltirish patterni: bir xil media type, bir xil maydonlar, stabil xato kodi va tashxis uchun korrelyatsiya ID'si. Maqsad - client'ning `instanceof`-ga o'xshash matn parsing qilishiga yo'l qo'ymaslik va stack trace kabi ichki ma'lumotni tashqariga chiqarmaslik. Hozirgi standart - RFC 9457 (ilgari RFC 7807) `application/problem+json`: `type`, `title`, `status`, `detail`, `instance` va ixtiyoriy kengaytmalar.

**Spring'da qayerda uchraydi:** Spring Framework 6.0 dan `org.springframework.http.ProblemDetail`, `ErrorResponse` va `ErrorResponseException` mavjud; built-in Spring MVC/WebFlux istisnolari uchun problem detail'ni yoqish `spring.mvc.problemdetails.enabled=true` (WebFlux'da `spring.webflux.problemdetails.enabled=true`). Markazlashgan handling `@RestControllerAdvice` + `@ExceptionHandler` yoki `ResponseEntityExceptionHandler`dan meros olish bilan qilinadi; validatsiya xatolari `MethodArgumentNotValidException`, `HandlerMethodValidationException` (6.1+) va `ConstraintViolationException`dan keladi. Spring Boot'ning eski "whitelabel" JSON formati `DefaultErrorAttributes`/`BasicErrorController` orqali ishlaydi va `server.error.include-stacktrace=never` bo'lishi kerak. Trace ID'ni qo'shish uchun Micrometer Tracing'ning `Tracer.currentSpan()` qiymati `ProblemDetail#setProperty` bilan beriladi.

```java
@RestControllerAdvice
class ApiErrors extends ResponseEntityExceptionHandler {
  @ExceptionHandler(InsufficientFundsException.class)
  ProblemDetail handle(InsufficientFundsException ex) {
    var pd = ProblemDetail.forStatusAndDetail(HttpStatus.CONFLICT, ex.getMessage());
    pd.setType(URI.create("https://api.shop.uz/errors/insufficient-funds"));
    pd.setTitle("Hisobda mablag' yetarli emas");
    pd.setProperty("errorCode", "WALLET_1007");
    return pd;
  }
}
```

**Qo'llanish keyslari:**
- Public REST API'da to'lov rad etilishi sabablarini stabil `errorCode` bilan qaytarish, toki client lokalizatsiyani o'zi qilsin.
- Bean Validation xatolarini maydon-maydon ro'yxati (`errors[].field`, `errors[].code`) bilan forma to'ldirish UI'siga uzatish.
- Idempotent operatsiyada konflikt (409) va optimistik lock (`OptimisticLockingFailureException`) holatlarini ajratib ko'rsatish.
- Har bir 5xx javobga `traceId` qo'shib, support ticket'dan log/trace'ga to'g'ridan-to'g'ri o'tish.
- Gateway va servis xatolari bir xil `problem+json` ko'rinishida chiqishi uchun Spring Cloud Gateway'da ham bir xil format qo'llash.

**Ehtiyot bo'ling:** `detail` maydoniga exception message'ni ko'r-ko'rona joylash SQL fragmenti, fayl yo'li yoki PII chiqib ketishiga olib keladi - foydalanuvchiga mo'ljallangan matnni alohida yozing. Ikkinchi tuzoq - `type` URI'sini keyinchalik o'zgartirish: u client uchun kontraktning bir qismi, shuning uchun versiyalanmaydigan barqaror identifikator sifatida qarang.

## 7.26 GraphQL (GraphQL with Spring for GraphQL)

**Tavsif:** Client'ga kerakli maydonlarni o'zi so'rash imkonini beradigan, kuchli tiplangan sxema asosidagi so'rov tili va runtime. Bir request bilan bir necha resursni grafik bo'ylab olish over-fetching va under-fetching muammosini kamaytiradi, endpoint ko'payishini to'xtatadi. Buning evaziga keshlash, rate-limiting va avtorizatsiya HTTP darajasidan sxema darajasiga ko'chadi va N+1 muammosi birinchi darajali xavf bo'lib qoladi.

**Spring'da qayerda uchraydi:** `spring-boot-starter-graphql` (Spring for GraphQL 1.x, ichida `graphql-java`) sxema fayllarini `src/main/resources/graphql/*.graphqls`dan o'qiydi va `/graphql` endpoint'ini ochadi. Handler'lar annotatsiya bilan yoziladi: `@QueryMapping`, `@MutationMapping`, `@SubscriptionMapping`, `@SchemaMapping`, `@Argument`, `@ContextValue`, `@ProjectedPayload`. N+1 ni yechish uchun `@BatchMapping` yoki `BatchLoaderRegistry`/`DataLoader`. Konfiguratsiya `RuntimeWiringConfigurer` va `GraphQlSourceBuilderCustomizer` orqali, instrumentation `graphql-java`ning `MaxQueryDepthInstrumentation`/`MaxQueryComplexityInstrumentation` bilan. Test uchun `GraphQlTester`/`HttpGraphQlTester`, client uchun `HttpGraphQlClient`; GraphiQL `spring.graphql.graphiql.enabled=true` bilan yoqiladi. Spring Security bilan integratsiya metod darajasida `@PreAuthorize` qo'yilgan `@SchemaMapping` metodlari orqali ishlaydi. Spring Data'da `@GraphQlRepository` va `QuerydslDataFetcher`/`QueryByExampleDataFetcher` avtomatik fetcher yasaydi.

**Qo'llanish keyslari:**
- Bir nechta platforma (iOS, Android, web) turlicha maydon to'plamini so'raydigan mahsulot katalogi.
- BFF qatlami: bir nechta mikroservis ma'lumotini bitta grafikka birlashtirib mobil client'ga berish.
- Admin paneli uchun murakkab filtrlash va nested relation'larni REST endpoint'lar ko'paytirmasdan ochish.
- Real-time notification'lar uchun WebSocket ustida `@SubscriptionMapping` bilan subscription.
- Federatsiyalangan grafikda (Apollo Federation) bitta subgraph'ni Spring Boot'da amalga oshirish.

**Ehtiyot bo'ling:** Ochiq internetda query depth/complexity limiti, `DataLoader` bilan batching va persisted queries bo'lmasa, bitta chuqur so'rov bazani o'ldiradigan DoS vektoriga aylanadi. GraphQL'ni "REST o'rnini bosuvchi" deb hamma joyda ishlatish xato: fayl yuklash/yuklab olish, CDN keshlanadigan oddiy resurslar va servis-servis ichki chaqiruvlari uchun REST yoki gRPC qulayroq.

```graphql
type Order {
  id: ID!
  total: String!
  lineItems: [LineItem!]!      # N+1 xavfi: DataLoader shart
}

type Query {
  order(id: ID!): Order
}
```

## 7.27 gRPC (gRPC with Spring)

**Tavsif:** Protocol Buffers sxemasi va HTTP/2 ustida ishlaydigan, kod generatsiyasiga asoslangan yuqori unumli RPC framework'i. Binary serialization, multiplexing, ikki tomonlama streaming va qat'iy kontrakt uni servis-servis aloqasi uchun JSON/REST'dan tezroq va xavfsizroq qiladi. Narxi - brauzerdan to'g'ridan-to'g'ri chaqirishning qiyinligi (gRPC-Web/proxy kerak), debug qilishning noqulayligi va proto fayllarini boshqarish zarurati.

**Spring'da qayerda uchraydi:** Rasmiy `Spring gRPC` loyihasi (`spring-grpc`, Spring Boot bilan autoconfiguration beradi) server tomonida `@GrpcService` bilan belgilangan bean'larni ro'yxatga oladi, `grpc.server.port` kabi property'larni o'qiydi; client tomonida `GrpcChannelFactory` orqali nomlangan channel'lardan stub yasaladi va `grpc.client.channels.*` konfiguratsiya qilinadi. Proto'dan Java kodi `protobuf-maven-plugin` (yoki Gradle protobuf plugin) bilan generatsiya qilinadi. Uzun vaqt keng tarqalgan community alternativa - `net.devh:grpc-spring-boot-starter` (`@GrpcService`, `@GrpcClient`). Observability uchun `grpc-java`ning interceptor'lari Micrometer bilan ulanadi, Spring Security `GlobalServerInterceptor`/`AuthenticationProcessInterceptor` uslubidagi interceptor orqali qo'shiladi. Protobuf'ni HTTP ustida uzatish kerak bo'lsa Spring Framework'ning `ProtobufHttpMessageConverter` va `ProtobufJsonFormatHttpMessageConverter` sinflari bor.

**Qo'llanish keyslari:**
- Ichki mikroservislar o'rtasida past latency talab qiladigan sinxron chaqiruvlar (masalan, narx hisoblash servisi).
- Katta hajmli ma'lumotni server-side streaming bilan uzatish (log, telemetriya, feed).
- Polyglot muhit: Java servisi Go yoki Python client'lari bilan bitta `.proto` kontrakt orqali ishlashi.
- Mobil client uchun trafikni qisqartirish (binary payload) - gRPC yoki gRPC-Web gateway bilan.
- Service mesh ichida mTLS va deadline/retry siyosatlarini protokol darajasida qo'llash.

**Ehtiyot bo'ling:** Proto evolyutsiyasi qoidalarini buzish (field raqamini qayta ishlatish, `reserved` qo'ymaslik, `required` semantikasini o'zgartirish) jimgina data corruption keltiradi - buf yoki protolock kabi breaking-change linter'ini CI'ga qo'ying. Public, uchinchi tomon integratsiyalari uchun gRPC'ni yagona yo'l qilib qo'ymang: ko'p client firewall, proxy va brauzer cheklovlari sabab REST/`problem+json` fasad'ini talab qiladi.

```proto
service Payments {
  rpc Charge (ChargeRequest) returns (ChargeReply);
}

message ChargeRequest {
  string account_id = 1;
  string amount = 2;           // pul uchun string: float ishlatilmaydi
  string currency = 3;
}
// Maydon raqamlari qayta ishlatilmaydi: olib tashlanganini `reserved` qiling
```

## 7.28 OpenAPI: kontrakt-birinchi yoki kod-birinchi (Contract-First vs Code-First OpenAPI)

**Tavsif:** API spetsifikatsiyasi haqiqat manbai bo'lishi (contract-first: avval YAML yoziladi, kod undan generatsiya qilinadi) yoki kod haqiqat manbai bo'lishi (code-first: controller'lardan runtime'da spetsifikatsiya chiqariladi) o'rtasidagi arxitektura tanlovi. Contract-first parallel ishlashni (frontend mock'ni darhol oladi), review'ni va breaking-change tekshiruvini kuchaytiradi; code-first esa boshlashga tez va kod bilan spetsifikatsiya o'rtasidagi drift'ni kamaytiradi. Yirik tashkilotlarda odatda tashqi API'lar contract-first, ichki API'lar code-first bo'ladi.

**Spring'da qayerda uchraydi:** Code-first'da `springdoc-openapi-starter-webmvc-ui` (Spring Boot 3.x uchun 2.x versiya) controller'larni skanerlab `/v3/api-docs` va Swagger UI beradi; boyitish `@Operation`, `@ApiResponse`, `@Schema`, `@Parameter` va `OpenAPI`/`GroupedOpenApi` bean'lari bilan qilinadi (eski `springfox` endi qo'llanmaydi). Contract-first'da `openapi-generator-maven-plugin`ning `spring` generatori interfeys va DTO'larni yasaydi (`interfaceOnly=true`, `delegatePattern=true`, `useSpringBoot3=true`), controller shu interfeysni implement qiladi. Test-driven dokumentatsiya yo'li - Spring REST Docs (`MockMvcRestDocumentation.document(...)`, `restdocs-api-spec` bilan OpenAPI chiqarish). Iste'molchi bilan kontraktni tekshirish uchun Spring Cloud Contract (`@AutoConfigureStubRunner`, generated test'lar) ishlatiladi.

**Qo'llanish keyslari:**
- Tashqi hamkorlar uchun public API: YAML'ni git'da review qilish va SDK'larni bir necha tilda generatsiya qilish.
- Frontend jamoasi backend tayyor bo'lishini kutmasdan Prism/WireMock mock'i bilan ishlashi.
- CI'da `openapi-diff` yoki buf-ga o'xshash tekshiruv bilan breaking change'ni merge'dan oldin bloklash.
- Ichki CRUD servislarda springdoc bilan tez dokumentatsiya va Swagger UI orqali qo'lda sinov.
- Mavjud legacy API'ni dokumentlashtirish: springdoc bilan spetsifikatsiya olib, keyin uni contract-first bazasiga aylantirish.

**Ehtiyot bo'ling:** Code-first'da spetsifikatsiya "tasodifiy kontrakt"ga aylanadi - DTO'ni refactor qilish jimgina public API'ni o'zgartirib qo'yadi, shuning uchun generated spec'ni artefakt sifatida saqlab, diff'ini CI'da tekshirish kerak. Contract-first'da generated kodni qo'lda tahrirlash yoki generator'ni build'dan chiqarib tashlash patternni butunlay yo'q qiladi; Swagger UI'ni prod'da autentifikatsiyasiz ochiq qoldirish esa alohida xavf.

```java
// Kod-birinchi: annotatsiyadan spetsifikatsiya chiqadi
@Operation(summary = "Buyurtma yaratish")
@ApiResponse(responseCode = "201", description = "Yaratildi")
@ApiResponse(responseCode = "409", description = "Takroriy idempotentlik kaliti")
@PostMapping("/orders")
ResponseEntity<OrderDto> create(@Valid @RequestBody CreateOrder cmd) { /* ... */ }

// Kontrakt-birinchi: openapi.yaml dan interfeys generatsiya qilinadi
// (openapi-generator-maven-plugin, generatorName=spring, interfaceOnly=true)
// Har ikki holatda CI da spetsifikatsiya va kod mosligi tekshirilsin.
```

## 7.29 Deklarativ HTTP client'lar (Declarative HTTP Interfaces / @HttpExchange)

**Tavsif:** Tashqi HTTP API'ni Java interfeysi sifatida e'lon qilib, so'rov yasash, serialize/deserialize va xato ishlovini framework generatsiya qilgan proxy'ga topshirish patterni. Chaqiruv kodi tip-xavfsiz va test qilishga oson bo'ladi, URL va header tafsilotlari bir joyda markazlashadi. Bu Feign uslubidagi yondashuvning Spring Framework yadrosiga ko'chgan ko'rinishi.

**Spring'da qayerda uchraydi:** Spring Framework 6.0 dan `@HttpExchange` va uning qisqartmalari `@GetExchange`, `@PostExchange`, `@PutExchange`, `@DeleteExchange`; parametrlar `@PathVariable`, `@RequestParam`, `@RequestBody`, `@RequestHeader` bilan belgilanadi. Proxy `HttpServiceProxyFactory.builderFor(adapter)` bilan yasaladi, adapter esa `RestClientAdapter.create(restClient)`, `WebClientAdapter.create(webClient)` yoki `RestTemplateAdapter`. Spring Framework 7 / Spring Boot 4 avlodida registratsiyani soddalashtirgan `@ImportHttpServices` va `AbstractHttpServiceRegistrar` mexanizmi qo'shildi. Alternativa - Spring Cloud OpenFeign'ning `@FeignClient`i (u ham `@HttpExchange`ni tushunadi). Resilience `WebClient`/`RestClient` filtri, Resilience4j (`@CircuitBreaker`, `@Retry`) va `ClientHttpRequestInterceptor` bilan qo'shiladi; test uchun `MockRestServiceServer` yoki WireMock.

```java
@HttpExchange("/customers")
public interface CustomerClient {
  @GetExchange("/{id}")
  Customer byId(@PathVariable String id);

  @PostExchange
  ResponseEntity<Customer> create(@RequestBody CustomerRequest req);
}
// RestClient rc = RestClient.create("https://crm.internal");
// var factory = HttpServiceProxyFactory.builderFor(RestClientAdapter.create(rc)).build();
// CustomerClient client = factory.createClient(CustomerClient.class);
```

**Qo'llanish keyslari:**
- Ichki mikroservis API'si uchun umumiy kutubxonada client interfeysini e'lon qilib, iste'molchilarga tarqatish.
- To'lov provayderi yoki SMS gateway kabi tashqi SaaS API'sini bitta interfeysga yopish.
- OpenAPI'dan generatsiya qilingan DTO'lar bilan birga qo'lda yozilgan ixcham client interfeysi.
- Blocking (`RestClient`) va reactive (`WebClient`) implementatsiyani bir xil interfeys ostida almashtirish.
- OAuth2 client credentials token'ini `ServletOAuth2AuthorizedClientExchangeFilterFunction` orqali avtomatik qo'shish.

**Ehtiyot bo'ling:** Default holatda 4xx/5xx `RestClientResponseException`/`WebClientResponseException` ko'rinishida chiqadi - timeout, retry va circuit breaker siyosatini ataylab sozlamasa, bitta sekin downstream butun thread pool'ni egallashi mumkin. Interfeysni juda "aqlli" qilib, unga business logika yoki mapping aralashtirish test qilishni qiyinlashtiradi; proxy faqat transport chegarasi bo'lib qolishi kerak.

## 7.30 Deprecation va Sunset header'lari (Deprecation / Sunset Headers)

**Tavsif:** API'ning eskirganini va o'chirilish sanasini javob header'lari orqali mashina o'qiy oladigan shaklda e'lon qilish patterni. `Deprecation` (RFC 9745) qachondan eskirganini, `Sunset` (RFC 8594) qachon ishlashdan to'xtashini, `Link` esa `rel="deprecation"`/`rel="successor-version"` bilan hujjat va almashtiruvchini ko'rsatadi. Bu changelog e'loniga tayanmasdan, client'larga va monitoring tizimlariga migratsiya oynasi haqida signal beradi.

**Spring'da qayerda uchraydi:** Spring'da maxsus abstraksiya yo'q - pattern o'z annotatsiyasi (masalan `@ApiDeprecated(sunset = "...")`) va `HandlerInterceptor` yoki `ResponseBodyAdvice` kombinatsiyasi bilan amalga oshiriladi; handler metodidagi annotatsiyani `HandlerMethod#getMethodAnnotation` orqali o'qib, `HttpServletResponse#setHeader` bilan header qo'shiladi. Global qoidalar uchun `OncePerRequestFilter`, WebFlux'da `WebFilter` ishlatiladi. Edge darajasida Spring Cloud Gateway'ning `AddResponseHeader` filtri butun route uchun header qo'shadi. Eski endpoint'dan qancha foydalanilayotganini bilish uchun Micrometer `Counter`ini client ID va endpoint tag'lari bilan oshirish, so'ngra Prometheus/Grafana'da alert qo'yish qo'llanadi; OpenAPI tomonida `@Operation(deprecated = true)` yoki Java'ning `@Deprecated`si spetsifikatsiyada `deprecated: true` beradi.

**Qo'llanish keyslari:**
- `/v1/orders`ni o'chirishdan oldin olti oylik sunset oynasini e'lon qilish va qolgan client'larni aniqlash.
- Field darajasidagi deprecation'ni `Warning`/custom header bilan bildirib, Expand/Contract bosqichini kuzatish.
- Partner integratsiyalarida qaysi tenant hali eski endpoint'ga urayotganini metrika bilan aniqlab, maqsadli xabar yuborish.
- Sunset sanasi kelganda eski endpoint'ni avval `410 Gone` qilib, keyin butunlay olib tashlash.
- Internal platform API'larida deprecation header'ini CI smoke-test'lari ushlab, iste'molchi jamoalarga build'da ogohlantirish berishi.

**Ehtiyot bo'ling:** Header'larni qo'yib, lekin haqiqiy foydalanish telemetriyasini yig'maslik eng keng tarqalgan xato - o'chirish paytida kim sinishini bilmay qolasiz. Sunset sanasini o'tkazib yuborish yoki uni bir necha marta surish header'ga ishonchni yo'q qiladi; `Sunset` qiymati esa albatta HTTP-date formatida bo'lishi kerak, ISO-8601 emas.

```java
// Eskirishni e'lon qilish: mijoz oldindan xabardor bo'ladi
@GetMapping("/v1/orders/{id}")
ResponseEntity<OrderDto> getV1(@PathVariable long id) {
    return ResponseEntity.ok()
            .header("Deprecation", "Sat, 01 Mar 2026 00:00:00 GMT")
            .header("Sunset", "Mon, 01 Jun 2026 00:00:00 GMT")
            .header("Link", "</v2/orders/" + id + ">; rel=\"successor-version\"")
            .body(service.view(id));
}
// Header yetarli emas: eskirgan endpoint foydalanuvchilari metrika bilan
// kuzatilsin va Sunset sanasidan oldin bevosita xabardor qilinsin.
```

## 7.31 Hypermedia boshqaruvlari va RPC uslubi (Hypermedia Controls vs RPC-style)

**Tavsif:** Javobga keyingi mumkin bo'lgan harakatlarning link va forma tavsiflarini kiritib (HATEOAS), client'ni URL'larni qo'lda yasashdan va holat mashinasini takrorlashdan xalos qilish yondashuvi; qarshi qutbda RPC uslubi - `POST /orders/{id}/cancel` kabi fe'l-endpoint'lar va client ichida qattiq kodlangan yo'llar. Hypermedia server tomonda evolyutsiya erkinligi va discoverability beradi, RPC esa soddaligi va kod generatsiyasiga qulayligi bilan ustun. Amalda ko'p tizim o'rtacha yo'lni tanlaydi: resurs-markazli URL'lar + ba'zi fe'l-endpoint'lar, linklar faqat workflow'li joylarda.

**Spring'da qayerda uchraydi:** Spring HATEOAS (`spring-boot-starter-hateoas`) `RepresentationModel`, `EntityModel<T>`, `CollectionModel<T>`, `PagedModel<T>` va `Link` abstraksiyalarini beradi; linklar `WebMvcLinkBuilder.linkTo(methodOn(OrderController.class).one(id)).withSelfRel()` bilan tip-xavfsiz yasaladi, mapping esa `RepresentationModelAssembler`/`RepresentationModelAssemblerSupport` ichida markazlashadi. Media type `@EnableHypermediaSupport(type = {HAL, HAL_FORMS})` bilan tanlanadi (`application/hal+json`, HAL-FORMS, Collection+JSON, UBER, ALPS). Shartli harakatlar `Affordances` API'si (`afford(methodOn(...))`) bilan ifodalanadi; `@ConditionalOnBean` emas, balki business shart asosida link qo'shiladi. Spring Data REST butun repository'ni HAL ko'rinishida avtomatik ochadi, client tomonida `Traverson` yoki `HalExplorer`/HAL Browser ishlatiladi. RPC uslubi esa oddiy `@PostMapping("/orders/{id}/cancel")` controller'lari ko'rinishida qoladi.

**Qo'llanish keyslari:**
- Buyurtma holat mashinasi: faqat ruxsat etilgan o'tishlar (`cancel`, `ship`, `refund`) link sifatida qaytariladi va UI tugmalarni shunga qarab ko'rsatadi.
- Admin/BO interfeysini generatsiya qilish: HAL-FORMS tavsiflari asosida forma avtomatik quriladi.
- Spring Data REST bilan ichki ma'lumot katalogini tez ochish va havolalar orqali kezish.
- API bazasi URL'lari o'zgarganda client'larni yangilamasdan yo'naltirish (faqat entry point qattiq kodlangan).
- Sahifalashda `next`/`prev` linklarini `PagedModel` bilan berish - client cursor logikasini yozmaydi.

**Ehtiyot bo'ling:** To'liq HATEOAS'ning foydasi faqat client haqiqatan linklarga tayanganda paydo bo'ladi; aksariyat mobil va SPA client'lar URL'ni qattiq kodlaydi, natijada javob hajmi va murakkabligi ortib, hech kim ishlatmaydigan metadata qoladi. Shuningdek `linkTo(methodOn(...))` har bir element uchun proxy yasaydi - katta ro'yxatlarda bu sezilarli CPU xarajati, assembler'ni o'lchab ko'rish kerak.

```text
RPC uslubi: mijoz qoidani biladi
  POST /orders/1/cancel        # mijoz "qachon mumkin" ni o'zi hisoblaydi

Gipermedia: qoida serverda qoladi
  GET /orders/1
  {
    "id": 1, "status": "NEW",
    "_links": { "cancel": { "href": "/orders/1/cancel", "method": "POST" } }
  }

Mijoz faqat _links.cancel bor-yo'qligini tekshiradi.
Narxi: javob kattaroq va mijoz kutubxonasi gipermediani tushunishi kerak.
```

## 7.32 Chegarada API Key va token autentifikatsiyasi (API Key / Token Auth at the Edge)

**Tavsif:** Chaqiruvchini identifikatsiya qilish va vakolatlarni tekshirishni tizimning eng tashqi chegarasida (gateway yoki resource server filter zanjirida) bir marta bajarish, ichki qatlamlarga esa allaqachon tasdiqlangan principal'ni uzatish patterni. API Key odatda mijoz ilovasini identifikatsiya qiladi va rate-limiting/billing uchun ishlatiladi, JWT yoki opaque access token esa foydalanuvchi va scope'larni ifodalaydi. Asosiy qoida - chegarada tekshirish ichki avtorizatsiyani almashtirmaydi, faqat uning oldiga qo'yiladi (batafsil: xavfsizlik bo'limiga qarang).

**Spring'da qayerda uchraydi:** Spring Security'da resource server `SecurityFilterChain` bean'i ichida `http.oauth2ResourceServer(o -> o.jwt(...))` yoki opaque token uchun `o.opaqueToken(...)` bilan yoqiladi; JWT'ni `NimbusJwtDecoder` (`spring.security.oauth2.resourceserver.jwt.issuer-uri`/`jwk-set-uri`) tekshiradi, scope'dan authority'ga o'girish `JwtAuthenticationConverter`/`JwtGrantedAuthoritiesConverter` bilan sozlanadi, zanjirdagi filter - `BearerTokenAuthenticationFilter`. API Key uchun built-in filter yo'q: `AuthenticationConverter` + `AuthenticationFilter` juftligi yoki custom `OncePerRequestFilter` yozilib, `PreAuthenticatedAuthenticationToken`/`AbstractPreAuthenticatedProcessingFilter` ishlatiladi va kalit hash ko'rinishida saqlanadi. Edge'da Spring Cloud Gateway `TokenRelay` filtri, `RequestRateLimiterGatewayFilterFactory` (Redis bilan) va route darajasidagi filtrlardan foydalanadi; servis ichida `@PreAuthorize`, `@AuthenticationPrincipal Jwt` va `SecurityContextHolder` qoladi. Mashina-mashina chaqiruvlarida token olish `OAuth2AuthorizedClientManager` orqali.

**Qo'llanish keyslari:**
- Public API'da har bir hamkorga alohida API Key berib, kvota va billing'ni kalit bo'yicha hisoblash.
- Mobil/SPA client'lar uchun OIDC provayderidan olingan JWT'ni gateway'da validatsiya qilib, downstream'ga uzatish.
- Mashina-mashina (service account) chaqiruvlarida client credentials grant va scope asosidagi cheklov.
- Webhook qabul qilishda HMAC imzo yoki API Key bilan jo'natuvchini tekshirish.
- Gateway'da rate-limiting kalitini (API Key yoki `sub` claim) aniqlab, abuse'ni ichki servislarga yetib bormasdan to'xtatish.

**Ehtiyot bo'ling:** API Key'ni autentifikatsiya emas, balki avtorizatsiya vositasi deb qarash xato - u URL'da, log'da va mobil ilova binary'sida oson oshkor bo'ladi, shuning uchun uni hech qachon query parametrida uzatmang va rotation imkoniyatini oldindan rejalashtiring. "Gateway tekshirdi" degan ishonch bilan ichki servislarni ochiq qoldirish (confused deputy / zero-trust buzilishi) eng xavfli holat: ichki chaqiruvlar ham mTLS yoki token bilan himoyalanishi va token `aud`/`iss` claim'lari albatta tekshirilishi kerak.

```java
@Bean
SecurityFilterChain api(HttpSecurity http) throws Exception {
    return http
        .securityMatcher("/api/**")
        .csrf(AbstractHttpConfigurer::disable)        // stateless API uchun
        .sessionManagement(s -> s.sessionCreationPolicy(SessionCreationPolicy.STATELESS))
        .authorizeHttpRequests(a -> a
            .requestMatchers("/api/public/**").permitAll()
            .anyRequest().authenticated())
        .oauth2ResourceServer(o -> o.jwt(Customizer.withDefaults()))
        .build();
}
// API kalitini query parametrda uzatmang: u log va Referer orqali oqib ketadi
```

## 7.33 Veb-servis brokeri (Web Service Broker)

**Tavsif:** Veb-servis brokeri bir yoki bir nechta ichki (domain) servisni tashqi dunyoga yagona, qo'pol donali (coarse-grained) veb-servis interfeysi orqali ochib beradi va shu bilan tashqi iste'molchini ichki komponentlar tuzilishidan ajratadi. Broker tashqi so'rovni qabul qiladi, uni ichki chaqiruvlarga (REST, gRPC, JMS, lokal bean metodlari) tarjima qiladi, natijalarni bitta javobga yig'adi va protokol hamda format o'girishni o'z ichiga oladi. Bu Facade va Adapter g'oyalarining integratsiya chegarasidagi ko'rinishi: domain modeli o'zgarsa ham tashqi kontrakt barqaror qoladi. Shuningdek broker markazlashgan nuqta sifatida autentifikatsiya, audit, throttling va xatolarni normallashtirish uchun qulay joy beradi.

**Spring'da qayerda uchraydi:** Spring Framework 6.x / Spring Boot 3.x da broker odatda alohida modul - `@RestController` yoki `@GraphQlController` (Spring for GraphQL) qatlami bo'lib, ichkariga `RestClient` (6.1+), `WebClient` yoki deklarativ HTTP interfeyslar (`@HttpExchange` + `HttpServiceProxyFactory`) orqali murojaat qiladi; bir nechta chaqiruvni parallel yig'ishda `CompletableFuture`, Reactor `Mono.zip`/`Flux` yoki Java 21+ `StructuredTaskScope` ishlatiladi. SOAP tomonda Spring Web Services (`spring-ws-core`) `@Endpoint` va `@PayloadRoot` bilan, hamda `WebServiceTemplate` ichki SOAP servislarni chaqirish uchun broker rolini bajaradi; JAX-WS integratsiyasi uchun `SimpleJaxWsServiceExporter` va `JaxWsPortProxyFactoryBean` mavjud. Format va kontrakt o'girish MapStruct yoki qo'lda yozilgan mapper'larda, kontraktni esa `springdoc-openapi` bilan hujjatlashtirish amalda standart; API gateway darajasida (Spring Cloud Gateway) brokerning yupqa varianti route va filter'lar bilan quriladi, lekin biznes agregatsiyasi bo'lsa, uni gateway'ga emas, alohida Spring Boot servisga qo'yish to'g'ri bo'ladi.

**Qo'llanish keyslari:**
- Legacy SOAP yoki mainframe servislarni tashqi mobil ilovalar uchun bitta REST/JSON kontraktiga o'rab berish.
- B2B hamkorlarga barqaror ommaviy API berish, ichki mikroservislar esa mustaqil refaktor qilinishi va bo'linishi kerak bo'lganda.
- Bir ekran uchun uch-to'rt xil domain servisidan ma'lumot yig'ib, bitta javob qaytarish (Backend-for-Frontend ko'rinishidagi broker).
- Tashqi provayder (to'lov, SMS, KYC) almashtirilishi mumkin bo'lganda, uni broker ortiga yashirib, iste'molchi kodi o'zgarmasligini ta'minlash.
- Autentifikatsiya, rate limiting, audit log va PII maskalashni yagona chegara nuqtasida markazlashtirish.

**Ehtiyot bo'ling:** Broker oson "distributed god object"ga aylanadi - biznes mantig'i unda to'planib, har bir domain o'zgarishi brokerni ham o'zgartirishni talab qiladi, shuning uchun uni orkestratsiya va tarjima bilan cheklang. Yana bir tuzoq - sinxron ketma-ket chaqiruvlar latency'ni qo'shib yuboradi va bitta sekin ichki servis butun brokerni bloklaydi: timeout, Resilience4j circuit breaker va parallel chaqiruvlarni albatta qo'ying, agar tashqi kontrakt ichki servis bilan amalda bir xil bo'lsa esa, bu qatlam faqat ortiqcha hop bo'ladi va uni umuman qo'ymaslik kerak.

```java
// Web service broker: tashqi tizim tafsiloti bitta sinfda qoladi
@Component
public class PspBroker {
    private final RestClient client;

    public Receipt charge(Payment p) {
        try {
            return client.post().uri("/v3/charge")
                    .body(toPspRequest(p))            // tashqi format bu yerda tug'iladi
                    .retrieve()
                    .body(PspResponse.class)
                    .toDomain();                      // va bu yerda o'ladi
        } catch (RestClientResponseException e) {
            throw PspErrorTranslator.translate(e);    // tashqi xato -> domen xatosi
        }
    }
}
```

## 7.34 Amalda qo'llash

- [ ] Har bir public endpoint uchun versiyalash strategiyasini yozib qo'ying va bitta loyihada bir nechta strategiya aralashmaganini tasdiqlang.
- [ ] Xato javoblarini tekshiring: hammasi bir xil formatdami, `stack trace` yoki ichki xabar tashqariga chiqmayaptimi.
- [ ] Sahifalashda `OFFSET` ishlatadigan endpointlarni toping va katta jadvallar uchun keyset pagination ga o'tkazish rejasini tuzing.
- [ ] Pul o'tkazish yoki buyurtma yaratish kabi takrorlanmasligi kerak bo'lgan endpointlarda idempotentlik kaliti borligini tasdiqlang.
- [ ] OpenAPI spetsifikatsiyasi kodga mos kelayotganini CI da tekshiradigan qadam qo'shing.
- [ ] Breaking change ro'yxatini tuzing: olib tashlangan maydon, majburiy bo'lgan parametr, o'zgargan tur va enum qiymati.
- [ ] Har bir endpoint uchun rate limit va maksimal payload hajmi belgilanganini tekshiring.
- [ ] Filtrlash va saralash parametrlarini ro'yxatga olib, har biri indekslangan ustunga tushayotganini tasdiqlang.

---

[&larr; 6. Web va taqdimot qatlami patternlari](06-web-va-taqdimot-qatlami-patternlari.md) · [Mundarija](README.md) · [8. Biznes logika va Service qatlam patternlari &rarr;](08-biznes-logika-va-service-qatlam-patternlari.md)
