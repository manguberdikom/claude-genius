<!-- doc: code-review | chapter: 20 | part: IV. Spring kodini review qilish -->

[Barcha hujjatlar](../../README.md) / [Kod review](README.md)

> Holat: AI yozgan, inson tekshirmagan.

# 20. Web qatlami review: DTO, validatsiya, xato javobi (The Web Layer)

<details>
<summary>Bu bobdagi 12 bo'lim</summary>

- [20.1 Tashqi shakl va ichki model chegarasi](#201-tashqi-shakl-va-ichki-model-chegarasi)
- [20.2 Validatsiya: qayerda va qanchalik](#202-validatsiya-qayerda-va-qanchalik)
- [20.3 Xato javobi: ichki detallar chiqmasligi](#203-xato-javobi-ichki-detallar-chiqmasligi)
- [20.4 HTTP semantikasi](#204-http-semantikasi)
- [20.5 Pagination va chegarasiz ro'yxatlar](#205-pagination-va-chegarasiz-royxatlar)
- [20.6 Serializatsiya tuzoqlari](#206-serializatsiya-tuzoqlari)
- [20.7 Fayl yuklash](#207-fayl-yuklash)
- [20.8 So'rov chegaralari va rate limit](#208-sorov-chegaralari-va-rate-limit)
- [20.9 Idempotentlik va qayta yuborish](#209-idempotentlik-va-qayta-yuborish)
- [20.10 CORS, header va kesh sozlamalari](#2010-cors-header-va-kesh-sozlamalari)
- [20.11 Review checklisti: web qatlami](#2011-review-checklisti-web-qatlami)
- [20.12 Amalda qo'llash](#2012-amalda-qollash)

</details>


Web qatlami - tizimning tashqi yuzasi. Bu yerdagi xato ikki tomonga qaraydi: tashqariga (mijoz sinadi, ma'lumot oqib chiqadi) va ichkariga (tekshirilmagan ma'lumot domenga kiradi). Review ning asosiy savoli: ishonilmaydigan kirish qayerda ishonchli ma'lumotga aylanadi, va javobda nima chiqib ketadi.

## 20.1 Tashqi shakl va ichki model chegarasi

```java
// Naqsh: entity to'g'ridan-to'g'ri qabul qilinadi va qaytariladi.
@PostMapping("/orders")
public Order create(@RequestBody Order order) {        // entity kirishda!
    return orders.save(order);                         // entity chiqishda!
}
```

Review izohi uchta aniq xavfni sanaydi:

1. Mass assignment: mijoz `{"id": 999, "status": "PAID", "total": 0}` yuborishi mumkin. Jackson barcha maydonlarni to'ldiradi, shu bilan mijoz o'z buyurtmasini to'langan deb belgilaydi.
2. Ichki maydonlar tashqariga chiqadi: `internalNote`, `costPrice`, `fraudScore`, boshqa foydalanuvchi ma'lumoti.
3. Jadval sxemasi API shartnomasiga aylanadi: ustun nomini o'zgartirish mijozni sindiradi.

```java
// To'g'ri: aniq kirish va chiqish shakllari, faqat ruxsat etilgan maydonlar.
public record CreateOrderRequest(
        @NotNull @Valid CustomerRef customer,
        @NotEmpty @Size(max = 100) @Valid List<LineRequest> lines,
        @Size(max = 500) String comment) { }

public record OrderResponse(
        UUID id, String number, String status,
        BigDecimal total, String currency,
        OffsetDateTime createdAt) {                    // ichki maydonlar yo'q
    static OrderResponse from(Order o) { ... }
}

@PostMapping("/orders")
public ResponseEntity<OrderResponse> create(@Valid @RequestBody CreateOrderRequest req) {
    Order order = orders.place(req.toCommand(currentUser()));
    return ResponseEntity.created(URI.create("/orders/" + order.id()))
                         .body(OrderResponse.from(order));
}
```

Qo'shimcha review diqqati: `customerId` so'rov tanasidan olinmasligi kerak - u autentifikatsiya kontekstidan olinadi. Aks holda foydalanuvchi boshqa mijoz nomidan buyurtma yaratadi ([30-bob](30-autentifikatsiya-va-avtorizatsiya-review.md)).

## 20.2 Validatsiya: qayerda va qanchalik

```java
// Review talabi: @Valid chegarada, va ichki obyektlarga ham tarqalgan.
public record LineRequest(
        @NotNull UUID productId,
        @Min(1) @Max(1000) int quantity) { }

public record CreateOrderRequest(
        @NotEmpty @Valid List<LineRequest> lines) { }   // @Valid ichkariga tarqaydi
// @Valid bo'lmasa: ichki obyektlarning annotatsiyalari tekshirilmaydi -
// bu eng ko'p o'tkazib yuboriladigan joy.

// Validatsiyaning uch darajasi va ularning joyi:
// 1) Shakl (format, uzunlik, diapazon) - DTO annotatsiyalari.
// 2) Domen qoidasi (status o'tishi, limit) - domen obyekti ichida.
// 3) Ma'lumot to'g'riligi (mavjudlik, yagonalik) - DB constraint + so'rov.
```

| Tekshiriladigan narsa | Qayerda | Nega |
| --- | --- | --- |
| Majburiy maydon, uzunlik, diapazon | DTO annotatsiyasi | Erta rad etish, aniq xato javobi |
| Format (email, telefon) | Value object konstruktori | Bir joyda, domenga kirmaydi |
| Biznes qoidasi | Domen metodi | Invariant himoyasi |
| Mavjudlik (`productId` bor) | Servis + FK | Poyga va yagona haqiqat |
| Yagonalik | DB unique indeks | Faqat u ishonchli (15.2) |
| Avtorizatsiya | Servis yoki metod security | Kirish huquqi |

```java
// Diqqat: @Validated va @Valid farqi - review da tez-tez chalkashtiriladi.
@RestController
@Validated                          // metod parametrlarini tekshirish uchun (@PathVariable, @RequestParam)
public class OrderController {
    @GetMapping("/orders")
    public List<OrderResponse> list(
            @RequestParam @Min(0) int page,                   // @Validated kerak
            @RequestParam @Max(100) int size) { ... }

    @PostMapping("/orders")
    public OrderResponse create(@Valid @RequestBody CreateOrderRequest req) { ... }
}                                   // @RequestBody uchun @Valid yetadi
```

## 20.3 Xato javobi: ichki detallar chiqmasligi

```java
// Naqsh: istisno xabari to'g'ridan-to'g'ri mijozga.
@ExceptionHandler(Exception.class)
public ResponseEntity<String> onError(Exception e) {
    return ResponseEntity.status(500).body(e.getMessage());   // ichki detallar!
}
// Oqibati: SQL so'rov matni, jadval nomlari, fayl yo'llari, kutubxona
// versiyalari mijozga ko'rinadi. Bu razvedka uchun tayyor ma'lumot.

// To'g'ri: standart shakl, ichki detal yo'q, korrelyatsiya ID bor.
@RestControllerAdvice
public class ApiExceptionHandler {

    @ExceptionHandler(MethodArgumentNotValidException.class)
    ProblemDetail onValidation(MethodArgumentNotValidException e) {
        ProblemDetail pd = ProblemDetail.forStatus(BAD_REQUEST);
        pd.setTitle("Validatsiya xatosi");
        pd.setProperty("errors", e.getFieldErrors().stream()
            .map(f -> Map.of("field", f.getField(), "message", f.getDefaultMessage()))
            .toList());
        return pd;
    }

    @ExceptionHandler(OrderNotFound.class)
    ProblemDetail onNotFound(OrderNotFound e) {
        ProblemDetail pd = ProblemDetail.forStatus(NOT_FOUND);
        pd.setTitle("Buyurtma topilmadi");
        return pd;                               // ID ni qaytarmaymiz: enumeratsiya
    }

    @ExceptionHandler(Exception.class)
    ProblemDetail onUnexpected(Exception e) {
        String traceId = MDC.get("traceId");
        log.error("kutilmagan xato traceId={}", traceId, e);   // detallar logda
        ProblemDetail pd = ProblemDetail.forStatus(INTERNAL_SERVER_ERROR);
        pd.setTitle("Ichki xatolik");
        pd.setProperty("traceId", traceId);      // support uchun yetarli
        return pd;
    }
}
```

```properties
# Standart Spring xato javobidan ichki detallarni olib tashlash.
# Boot 3.x kalitlari; Boot 4 da spring.web.error.include-* (pastga qarang).
server.error.include-message=never
server.error.include-stacktrace=never
server.error.include-binding-errors=never
server.error.include-exception=false
```

Bu to'rt qiymat Boot standarti bilan bir xil, ularni ochiq yozish standartni kimdir profil orqali o'zgartirmasligini hujjatlaydi. Boot 4 da kalitlar `spring.web.error.include-*` ga ko'chgan: [Boot 4.1.0 metadata](https://github.com/spring-projects/spring-boot/blob/v4.1.0/module/spring-boot-web-server/src/main/resources/META-INF/additional-spring-configuration-metadata.json) da `server.error.include-*` uchun `level=error` (4.0.0 dan) va `replacement` yangi kalit. Ya'ni Boot 4 da eski kalit umuman ulanmaydi: standartdan farqli qiymat (masalan dev profilida `include-message=always`) jim e'tiborsiz qoladi, review da kalit nomi Boot versiyasiga solishtiriladi.

## 20.4 HTTP semantikasi

| Belgi | Review savoli |
| --- | --- |
| `GET` holatni o'zgartiradi | Keshlanadi, prefetch qilinadi, retry qilinadi - xavfli |
| `POST` o'rniga `GET` bilan parametrlar | Maxfiy ma'lumot URL da va loglarda qoladi |
| `PUT` idempotent emas | Qayta yuborish dublikat yaratadi |
| `DELETE` ikki marta 404 beradi | Idempotentlik buzilgan - 204 bo'lishi kerak |
| Hamma xato 200 bilan `{"error": ...}` | Mijoz retry mantiqini qura olmaydi |
| 500 biznes rad etishi uchun | Monitoring shovqinga to'ladi |
| Yangi 4xx kod | Mijoz uni biladimi, hujjatlashtirilganmi |
| `Location` header yo'q `201` da | Mijoz yangi resurs manzilini bilmaydi |

```java
// Status kodlarining to'g'ri taqsimoti: review da shu jadval bo'yicha tekshiriladi.
// 400 - shakl xatosi (validatsiya)
// 401 - autentifikatsiya yo'q yoki yaroqsiz
// 403 - autentifikatsiya bor, huquq yo'q
// 404 - resurs yo'q (yoki ko'rish huquqi yo'q - enumeratsiyani oldini olish)
// 409 - konflikt (optimistik qulf, idempotentlik kaliti qayta ishlatilgan)
// 410 - resurs o'chirilgan (versiyalashda foydali)
// 422 - shakl to'g'ri, biznes qoidasi rad etdi
// 429 - rate limit
// 503 + Retry-After - vaqtincha ishlamaydi (circuit breaker ochiq)
```

## 20.5 Pagination va chegarasiz ro'yxatlar

```java
// Naqsh: chegarasiz ro'yxat.
@GetMapping("/orders")
public List<OrderResponse> all() { return orders.findAll()...; }   // 4 mln qator

// To'g'ri: majburiy chegara, maksimal qiymat, barqaror tartib.
@GetMapping("/orders")
public PageResponse<OrderResponse> list(
        @RequestParam(defaultValue = "0") @Min(0) int page,
        @RequestParam(defaultValue = "20") @Min(1) @Max(100) int size,
        @RequestParam(required = false) String cursor) {
    ...
}
```

Review da pagination uchun uch savol:

1. Maksimal `size` cheklanganmi. Cheklanmasa, `size=1000000` bilan ilovani yiqitish mumkin.
2. Tartib barqarormi. `ORDER BY created_at` da bir xil vaqtli qatorlar bo'lsa, sahifalar orasida qatorlar takrorlanadi yoki yo'qoladi. To'g'risi: `ORDER BY created_at DESC, id DESC` - yagona kalit bilan tugash.
3. Offset yoki kursor. Katta offset (`OFFSET 100000`) PostgreSQL da sekin: baza barcha oldingi qatorlarni o'qib tashlab yuboradi. Chuqur pagination uchun kursor (keyset) kerak.

```sql
-- Offset pagination: 100 000-sahifada sekin.
SELECT id, number FROM orders ORDER BY created_at DESC, id DESC
 LIMIT 20 OFFSET 100000;                  -- 100 020 qator o'qiladi

-- Keyset pagination: har doim tez, indeksdan foydalanadi.
SELECT id, number FROM orders
 WHERE (created_at, id) < (:lastCreatedAt, :lastId)   -- kursor
 ORDER BY created_at DESC, id DESC
 LIMIT 20;                                -- 20 qator o'qiladi
-- Indeks: CREATE INDEX ON orders (created_at DESC, id DESC);
```

## 20.6 Serializatsiya tuzoqlari

```java
// Tuzoq 1: lazy proxy serializatsiyasi.
// Entity qaytarilganda Jackson lazy kolleksiyaga tegadi va N+1 so'rov
// yuzaga keladi (yoki OSIV o'chirilgan bo'lsa istisno). Javob yozilayotganda
// xato chiqsa, HTTP status allaqachon 200 yuborilgan bo'ladi.

// Tuzoq 2: null va yo'q maydon farqi.
@JsonInclude(JsonInclude.Include.NON_NULL)    // null maydonlar chiqmaydi
public record OrderResponse(UUID id, String comment) { }
// Review savoli: mijoz "maydon yo'q" va "maydon null" ni ajrata oladimi?
// PATCH semantikasida bu farq muhim (JsonNullable yoki Optional kerak).

// Tuzoq 3: sana formati.
// Standart holatda Spring Boot `Instant` ni ISO-8601 satr sifatida yozadi,
// lekin WRITE_DATES_AS_TIMESTAMPS yoqilgan bo'lsa - raqam sifatida.
// Review da javob namunasini ko'rish kerak, kodga ishonmaslik.

// Tuzoq 4: BigDecimal serializatsiyasi.
// 1000.00 -> 1000.0 yoki 1000 bo'lib chiqishi mumkin, bu mijozda
// formatlash muammosi beradi. Pul uchun satr sifatida yuborish xavfsizroq.
@JsonSerialize(using = ToStringSerializer.class)
BigDecimal total;

// Tuzoq 5: polimorfik serializatsiya.
// @JsonTypeInfo bilan tur nomi JSON ga yoziladi - bu ichki klass nomlarini
// oshkor qiladi va deserializatsiyada xavf tug'diradi ([31-bob](31-kirish-va-chiqish-xavfsizligi-ssrf.md)).
```

## 20.7 Fayl yuklash

```java
// Review checklisti fayl yuklash uchun - har bir band alohida xavf.
@PostMapping(value = "/documents", consumes = MULTIPART_FORM_DATA_VALUE)
public DocumentResponse upload(@RequestPart("file") MultipartFile file) {
    // 1) Hajm chegarasi: konfiguratsiyada (quyida) va bu yerda ham.
    if (file.getSize() > MAX_SIZE) throw new FileTooLarge(MAX_SIZE);

    // 2) Tur tekshiruvi: Content-Type ga ishonmaslik - u mijozdan keladi.
    //    Haqiqiy turni baytlardan aniqlash (magic bytes).
    MediaType actual = fileTypeDetector.detect(file.getInputStream());
    if (!ALLOWED.contains(actual)) throw new UnsupportedFileType(actual);

    // 3) Nomni ishlatmaslik: path traversal va XSS manbasi.
    String storedName = UUID.randomUUID() + extensionFor(actual);   // o'z nomimiz

    // 4) Saqlash joyi: web root ichida emas, bajarilmaydigan joyda.
    storage.put(storedName, file.getInputStream());

    // 5) Antivirus yoki sandbox: ishonilmaydigan fayl uchun.
    return new DocumentResponse(storedName);
}
```

```properties
# Hajm chegaralari: ikki darajada.
spring.servlet.multipart.max-file-size=10MB
spring.servlet.multipart.max-request-size=12MB
server.tomcat.max-swallow-size=2MB        # rad etilgan so'rovni tez uzish
server.tomcat.max-http-form-post-size=2MB
```

## 20.8 So'rov chegaralari va rate limit

| Chegara | Nega kerak |
| --- | --- |
| So'rov tanasi hajmi | Xotira va parsing xarajati |
| Ro'yxat elementlari soni (`@Size(max=...)`) | 1 mln elementli massiv so'rovi |
| Ichma-ich JSON chuqurligi | Parser ni yiqitish |
| Rate limit (foydalanuvchi va IP bo'yicha) | Zo'ravonlik va tasodifiy retry bo'roni |
| So'rov timeout i | Sekin mijozlar thread ushlashi |
| Bir foydalanuvchiga parallel so'rov chegarasi | Resurs monopoliyasi |

```java
// Chuqur ichma-ich JSON va katta massivlardan himoya: Jackson chegaralari.
@Bean
Jackson2ObjectMapperBuilderCustomizer limits() {
    return builder -> builder.postConfigurer(mapper ->
        mapper.getFactory().setStreamReadConstraints(
            StreamReadConstraints.builder()
                .maxNestingDepth(50)
                .maxStringLength(1_000_000)
                .maxNumberLength(1_000)
                .build()));
}
```

## 20.9 Idempotentlik va qayta yuborish

Web qatlamida idempotentlik ikki joyda kerak: mijoz retry qilganda va foydalanuvchi ikki marta bosganda. Mexanizm 10.9 da ko'rsatilgan; bu yerda review savollari:

- Qaysi endpointlar idempotentlik kalitini talab qiladi (barcha pul va tashqi ta'sirli operatsiyalar).
- Kalit qayerdan keladi (mijoz yuboradi, server yaratmaydi).
- Takroriy so'rovga qanday javob qaytadi (bir xil natija, 409 emas, agar tana bir xil bo'lsa).
- Kalit qancha saqlanadi va kim tozalaydi.

Mavzuning to'liq yozuvi [idempotency](../patterns/07-api-dizayn-patternlari.md#79-idempotentlik-kaliti-idempotency-key) bo'limida; bu yerda faqat shu bo'limning nuqtai nazari.

## 20.10 CORS, header va kesh sozlamalari

```java
// Naqsh: hamma narsaga ruxsat.
@CrossOrigin(origins = "*")                   // credentials bilan birga - xavfli
// Review izohi: `*` va `allowCredentials=true` birga ishlamaydi (brauzer
// rad etadi), lekin `*` ning o'zi ham ichki API uchun ortiqcha ochiqlik.

// To'g'ri: aniq ro'yxat, konfiguratsiyadan.
@Bean
CorsConfigurationSource corsConfigurationSource(@Value("${app.cors.origins}") List<String> origins) {
    CorsConfiguration c = new CorsConfiguration();
    c.setAllowedOrigins(origins);                       // aniq domenlar
    c.setAllowedMethods(List.of("GET", "POST", "PUT", "DELETE"));
    c.setAllowedHeaders(List.of("Authorization", "Content-Type", "Idempotency-Key"));
    c.setAllowCredentials(true);
    c.setMaxAge(Duration.ofMinutes(30));
    UrlBasedCorsConfigurationSource src = new UrlBasedCorsConfigurationSource();
    src.registerCorsConfiguration("/api/**", c);
    return src;
}
```

Keshlash header lari uchun review savoli: maxfiy ma'lumot qaytaradigan javobda `Cache-Control: no-store` bormi. Aks holda javob brauzer keshida yoki proksi keshida qoladi.

## 20.11 Review checklisti: web qatlami

| Savol | Nega |
| --- | --- |
| Entity kirish yoki chiqishda ishlatilmaydimi | Mass assignment, ma'lumot oqishi |
| `@Valid` bormi va ichki obyektlarga tarqaladimi | Tekshirilmagan ma'lumot |
| Foydalanuvchi identifikatori so'rovdan olinmaydimi | Boshqa nomidan harakat |
| Xato javobida ichki detal yo'qmi | Razvedka ma'lumoti |
| Status kodlari semantikaga mosmi | Mijoz mantiqi va monitoring |
| Ro'yxatlarda majburiy va maksimal `size` bormi | Resurs tugashi |
| Tartib barqarormi (yagona kalit bilan) | Pagination takrorlanishi |
| Pul va sana formati aniqmi | Mijoz tomonda xato |
| Fayl yuklashda tur, hajm, nom tekshirilganmi | Xavfsizlik |
| Yozuv operatsiyalarida idempotentlik bormi | Dublikat |
| CORS ro'yxati aniqmi | Ortiqcha ochiqlik |
| Maxfiy javoblarda `no-store` bormi | Kesh oqishi |

## 20.12 Amalda qo'llash

- [ ] Barcha controller metodlarini skanerlab, JPA entity kirish yoki chiqish turi sifatida ishlatilgan joylarni toping.
- [ ] `@RequestBody` parametrlarida `@Valid` yo'q joylarni va ichki obyektlarda `@Valid` tarqalmagan joylarni aniqlang.
- [ ] `server.error.include-*` (Boot 4 da `spring.web.error.include-*`) sozlamalarini `never` qilib qo'ying va xato javoblarini `ProblemDetail` ga o'tkazing.
- [ ] Ro'yxat qaytaradigan endpointlarni sanab, `size` uchun maksimal chegara va barqaror tartib borligini tekshiring.
- [ ] Chuqur pagination ishlatiladigan joylarni keyset pagination ga o'tkazishni rejalashtiring.
- [ ] Pul maydonlarining JSON dagi ko'rinishini real javob namunasida tekshirib, satr sifatida yuborishni ko'rib chiqing.
- [ ] Fayl yuklash endpointlarida magic bytes bo'yicha tur tekshiruvi va o'z nomi bilan saqlash borligini tasdiqlang.
- [ ] Jackson `StreamReadConstraints` chegaralarini sozlang.
- [ ] `@CrossOrigin(origins = "*")` ishlatilgan joylarni aniq domen ro'yxatiga o'tkazing.
- [ ] Maxfiy ma'lumot qaytaradigan endpointlarda `Cache-Control: no-store` header ini qo'shing.

---

[&larr; 19. Tranzaksiya chegarasi review](19-tranzaksiya-chegarasi-review.md) · [Mundarija](README.md) · [21. Konfiguratsiya, profil va feature flag review &rarr;](21-konfiguratsiya-profil-va-feature-flag-review.md)
