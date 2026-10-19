# web qatlami

Minimal shakl (clean-code 27.1, 27.2; code-review 20.2):

```java
record CreateOrderRequest(@NotEmpty @Valid List<LineRequest> lines) { }

@RestController
@RequestMapping("/api/orders")
class OrderController {
    private final OrderService orders;
    OrderController(OrderService orders) { this.orders = orders; }

    @GetMapping("/{id}") // topilmasa service OrderNotFound tashlaydi
    OrderResponse get(@PathVariable Long id) { return orders.find(id); }

    @PostMapping // ResponseEntity faqat dinamik Location uchun
    ResponseEntity<OrderResponse> create(@Valid @RequestBody CreateOrderRequest request) {
        OrderResponse order = orders.place(request);
        return ResponseEntity.created(URI.create("/api/orders/" + order.id())).body(order);
    }
}
```

Allaqachon bor, yozmang:
- Spring web istisnolari (`ResponseStatusException` ham) uchun handler o'rniga `spring.mvc.problemdetails.enabled=true`; usiz eski `/error` JSON (architect 17.8, patterns 7.10, 7.25)
- Domen istisnosi uchun `@RestControllerAdvice` + `@ExceptionHandler`, `ProblemDetail` qaytaradi (patterns 7.10, code-review 20.3)
- Qo'lda `page`/`size` o'rniga `Pageable` va `spring.data.web.pageable.max-page-size` (clean-code 27.5)

Tuzoqlar:
- Entity kirish yoki javob bo'lsa mass assignment va maydon oqishi; alohida record DTO (code-review 20.1)
- Controller repository olmaydi, DTO mapping service ichida: aks holda `LazyInitializationException` (architect 17.7, code-review 6.6)
- `ResponseEntity.of(Optional)` (patterns 24.5) 404 ni tanasiz beradi, advice shaklidan farqli (clean-code 27.2)
- Ichki DTO ro'yxatida `@Valid` bo'lmasa ichi tekshirilmaydi (code-review 20.2, clean-code 27.4)
