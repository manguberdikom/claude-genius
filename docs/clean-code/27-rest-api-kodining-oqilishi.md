<!-- doc: clean-code | chapter: 27 | part: VIII. Spring va ma'lumot qatlamida toza kod -->

[Barcha hujjatlar](../../README.md) / [Toza kod qoidalari](README.md)

# 27. REST API kodining o'qilishi (Readable REST Code)

<details>
<summary>Bu bobdagi 9 bo'lim</summary>

- [27.1 Controller metodi imzosi va qaytish turi](#271-controller-metodi-imzosi-va-qaytish-turi)
- [27.2 HTTP holat kodini bitta joyda qaror qilish](#272-http-holat-kodini-bitta-joyda-qaror-qilish)
- [27.3 Xato javobi formati: `ProblemDetail` va `@ExceptionHandler`](#273-xato-javobi-formati-problemdetail-va-exceptionhandler)
- [27.4 Validatsiya: `@Valid`, guruhlar, maxsus validator](#274-validatsiya-valid-guruhlar-maxsus-validator)
- [27.5 Sahifalash, saralash va filtr parametrlari](#275-sahifalash-saralash-va-filtr-parametrlari)
- [27.6 Seriyalash sozlamalari: Jackson, `null`, sana formati](#276-seriyalash-sozlamalari-jackson-null-sana-formati)
- [27.7 Idempotentlik va `Idempotency-Key` kodda](#277-idempotentlik-va-idempotency-key-kodda)
- [27.8 API versiyasi kodda qanday ko'rinadi](#278-api-versiyasi-kodda-qanday-korinadi)
- [27.9 Amalda qo'llash](#279-amalda-qollash)

</details>


API dizayn patternlari [patternlar hujjatidagi](../patterns/README.md) API dizayn patternlari bo'limida, REST so'rov yo'li [arxitektor hujjatidagi](../architect/README.md) Spring MVC va WebFlux bo'limida. Bu bobda controller **kodining** tozaligi: imzo, holat kodi, xato javobi, validatsiya, seriyalash sozlamalari va idempotentlik.

## 27.1 Controller metodi imzosi va qaytish turi

Controller imzosi API shartnomasini ko'rsatishi kerak. `ResponseEntity<?>` va `Map<String, Object>` ikkisi ham shartnomani yashiradi: o'quvchi javob shaklini kod ichidan izlaydi.

```java
// yomon: shartnoma ko'rinmaydi
@PostMapping("/orders")
ResponseEntity<?> create(@RequestBody Map<String, Object> body) { ... }

// yaxshi: kirish va chiqish turlari oshkor, holat kodi annotatsiyada
@PostMapping("/orders")
@ResponseStatus(HttpStatus.CREATED)
OrderResponse create(@Valid @RequestBody CreateOrderRequest request) { ... }

// ResponseEntity faqat sarlavha yoki holat kodi dinamik bo'lganda
@PostMapping("/orders")
ResponseEntity<OrderResponse> create(@Valid @RequestBody CreateOrderRequest request) {
    Order order = orders.place(request.toCommand());
    return ResponseEntity.created(locationOf(order)).body(OrderResponse.from(order));
}
```

## 27.2 HTTP holat kodini bitta joyda qaror qilish

Holat kodi mantiqi controller lar bo'ylab tarqalsa, bir xil xato turli endpointlarda turli kod bilan qaytadi. Yechim: holat kodini **istisno turiga** bog'lash va bitta joyda belgilash.

| Holat | Kod |
|---|---|
| Yaratildi | 201 + `Location` |
| Muvaffaqiyatli, javob yo'q | 204 |
| Validatsiya xatosi | 400 |
| Autentifikatsiya yo'q | 401 |
| Ruxsat yo'q | 403 |
| Topilmadi | 404 |
| Konflikt (idempotentlik, versiya) | 409 |
| Biznes qoidasi buzildi | 422 |
| Juda ko'p so'rov | 429 |
| Ichki xato | 500 |
| Tashqi tizim javob bermadi | 502 / 504 |

## 27.3 Xato javobi formati: `ProblemDetail` va `@ExceptionHandler`

Hammasini tutuvchi exception handler [patternlar hujjatida](../patterns/README.md) anti-pattern (25.41). To'g'ri shakl: har bir istisno turiga aniq ishlov, bitta `@RestControllerAdvice` da, RFC 9457 (`ProblemDetail`) formatida.

```java
@RestControllerAdvice
class ApiExceptionHandler {

    private static final Logger log = LoggerFactory.getLogger(ApiExceptionHandler.class);

    @ExceptionHandler(OrderNotFoundException.class)
    ProblemDetail handleNotFound(OrderNotFoundException e) {
        // 404 - log kerak emas: bu normal holat
        return problem(HttpStatus.NOT_FOUND, e.code(), e.getMessage());
    }

    @ExceptionHandler(DomainRuleViolationException.class)
    ProblemDetail handleRule(DomainRuleViolationException e) {
        // 422 - biznes qoidasi; WARN yetarli
        log.warn("biznes qoidasi buzildi: {}", e.code());
        return problem(HttpStatus.UNPROCESSABLE_ENTITY, e.code(), e.getMessage());
    }

    @ExceptionHandler(GatewayUnavailableException.class)
    ProblemDetail handleGateway(GatewayUnavailableException e) {
        log.error("tashqi gateway javob bermadi", e);        // 19.7: log bir joyda
        return problem(HttpStatus.BAD_GATEWAY, e.code(), "To'lov tizimi vaqtincha ishlamayapti");
    }

    private ProblemDetail problem(HttpStatus status, String code, String detail) {
        ProblemDetail problem = ProblemDetail.forStatusAndDetail(status, detail);
        problem.setProperty("code", code);                   // barqaror kod (19.11)
        problem.setProperty("traceId", MDC.get("traceId"));  // diagnostika uchun
        return problem;
    }
}
```

Muhim qoida: xato javobida ichki sinf nomi, stack trace yoki SQL bo'lmasligi kerak (19.10).

## 27.4 Validatsiya: `@Valid`, guruhlar, maxsus validator

Validatsiya chegarada bo'ladi (5.11) va Bean Validation uning standart vositasi. Uch qoida: xabarlar kalitlar orqali lokalizatsiya qilinadi, guruhlar faqat haqiqatan kerak bo'lganda ishlatiladi, va murakkab qoidalar maxsus validator ga chiqadi.

```java
record CreateOrderRequest(
        @NotNull CustomerId customerId,
        @NotEmpty @Size(max = 100) List<@Valid OrderLineRequest> lines,
        @Pattern(regexp = "[A-Z]{3}") String currency) {

    OrderCommand toCommand() { ... }
}

// Maydonlar orasidagi qoida: maxsus validator (bitta maydonga bog'lanmaydi)
@Documented
@Constraint(validatedBy = DateRangeValidator.class)
@Target(ElementType.TYPE)
@Retention(RetentionPolicy.RUNTIME)
public @interface ValidDateRange {
    String message() default "{shop.validation.date-range}";
    Class<?>[] groups() default { };
    Class<? extends Payload>[] payload() default { };
}
```

Validatsiya xatolarini bir xil formatda qaytarish kerak: maydon nomi, kod, xabar.

```java
@ExceptionHandler(MethodArgumentNotValidException.class)
ProblemDetail handleValidation(MethodArgumentNotValidException e) {
    ProblemDetail problem = ProblemDetail.forStatus(HttpStatus.BAD_REQUEST);
    problem.setProperty("errors", e.getFieldErrors().stream()
            .map(f -> Map.of("field", f.getField(), "message", f.getDefaultMessage()))
            .toList());
    return problem;
}
```

## 27.5 Sahifalash, saralash va filtr parametrlari

Sahifalanmagan ro'yxat endpointi har doim kelajakdagi incident: ma'lumot o'sadi va javob vaqti bilan birga xotira ham oshadi. Qoida: ro'yxat qaytaradigan har bir endpoint sahifalangan bo'ladi va maksimal hajm cheklanadi.

```java
@GetMapping("/orders")
Page<OrderSummary> search(
        @Valid OrderCriteria criteria,
        @PageableDefault(size = 20, sort = "createdAt", direction = Sort.Direction.DESC)
        Pageable pageable) {
    return orders.search(criteria, pageable);
}
```

```yaml
spring:
  data:
    web:
      pageable:
        max-page-size: 100        # klient 10000 so'rasa ham 100 bilan cheklanadi
        default-page-size: 20
        one-indexed-parameters: false
```

Saralash maydonlarini oq ro'yxat bilan cheklash kerak: tashqi `sort` parametri to'g'ridan-to'g'ri SQL ga tushsa, indekssiz ustun bo'yicha saralash bazani yuklaydi.

## 27.6 Seriyalash sozlamalari: Jackson, `null`, sana formati

Jackson sozlamalari bir joyda, oshkor bo'lishi kerak; aks holda javob shakli standart qiymatlarga bog'lanib qoladi va versiya yangilanganda o'zgaradi.

```yaml
spring:
  jackson:
    default-property-inclusion: non_null    # null maydonlar javobda yo'q
    serialization:
      write-dates-as-timestamps: false      # ISO-8601 (22.9)
      fail-on-empty-beans: true
    deserialization:
      fail-on-unknown-properties: true      # klient xatosi jim o'tmaydi
      fail-on-null-for-primitives: true
    time-zone: UTC
```

Qo'shimcha qoidalar: JPA entitetini API da qaytarmaslik ([patternlar hujjatidagi](../patterns/README.md) API da JPA entitetlarini fosh qilish anti-patterni), `@JsonIgnore` bilan sezgir maydonlarni yopish, va DTO maydonlari nomini API shartnomasida barqaror ushlash.

## 27.7 Idempotentlik va `Idempotency-Key` kodda

Yaratish amallari (`POST`) takrorlanishi mumkin: klient timeout dan keyin qayta yuboradi. Idempotentlik kaliti shu takrorlanishni xavfsiz qiladi va u kodda ko'rinadigan bo'lishi kerak.

```java
@PostMapping("/refunds")
RefundResponse refund(
        @RequestHeader("Idempotency-Key") @NotBlank String idempotencyKey,
        @Valid @RequestBody RefundRequest request) {
    return RefundResponse.from(refunds.create(request.toCommand(), IdempotencyKey.of(idempotencyKey)));
}
```

Kalit server tomonda **generatsiya qilinmaydi** (20.8): u klientdan keladi, bazada unikal cheklov bilan saqlanadi (3.13 dagi `uq_payment_idempotency_key`), va takroriy so'rov oldingi natijani qaytaradi.

## 27.8 API versiyasi kodda qanday ko'rinadi

Versiyalash strategiyasi API dizayn masalasi, lekin kod tuzilishi unga mos bo'lishi kerak: ikki versiya bir controller da yashamasligi kerak.

```java
// yomon: ikki versiya bir sinfda, shartlar bilan
@GetMapping("/orders")
Object list(@RequestParam(defaultValue = "1") int version) {
    if (version == 2) return v2Response();
    return v1Response();
}

// yaxshi: har bir versiya o'z controlleri va DTO lari bilan
@RestController @RequestMapping("/api/v1/orders")
class OrderV1Controller { ... }

@RestController @RequestMapping("/api/v2/orders")
class OrderV2Controller { ... }
// Ikkisi ham bir xil service ni chaqiradi: mantiq takrorlanmaydi
```

## 27.9 Amalda qo'llash

- [ ] `ResponseEntity<?>` va `Map<String, Object>` qaytaradigan controller metodlarini aniq DTO turlariga o'tkazing.
- [ ] Holat kodi mantiqini controller lardan `@RestControllerAdvice` ga ko'chirib, 27.2 jadvaliga moslang.
- [ ] Xato javoblarini `ProblemDetail` formatiga keltirib, barqaror `code` va `traceId` qo'shing.
- [ ] Hammasini tutuvchi `@ExceptionHandler(Exception.class)` ni aniq turlarga bo'ling.
- [ ] Barcha ro'yxat endpointlarini sahifalangan qilib, `max-page-size` ni sozlang.
- [ ] Saralash maydonlarini oq ro'yxat bilan cheklab, indekssiz ustunlarni chiqarib tashlang.
- [ ] Jackson sozlamalarini `application.yml` da oshkor yozib, sana formatini ISO-8601 ga qotiring.
- [ ] Yaratish endpointlariga `Idempotency-Key` sarlavhasini va bazada unikal cheklovni qo'shing.

---

[&larr; 26. Spring kodining tozaligi](26-spring-kodining-tozaligi.md) · [Mundarija](README.md) · [28. JPA va SQL kodining tozaligi &rarr;](28-jpa-va-sql-kodining-tozaligi.md)
