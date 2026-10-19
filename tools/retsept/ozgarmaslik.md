# o'zgarmaslik

Minimal shakl (clean-code 16.1, 16.4):

```java
public record Order(OrderId id, OrderStatus status, List<OrderItem> items) {

    public Order {
        items = List.copyOf(items);
    }

    public Order confirmed() {
        if (status != DRAFT) throw new IllegalStateException("faqat DRAFT");
        return new Order(id, CONFIRMED, items);
    }
}
```

Allaqachon bor, yozmang:
- qo'lda final maydon, konstruktor, equals/hashCode o'rniga `record` (patterns 24.1)
- `new ArrayList<>(src)` yoki `unmodifiableList` o'rniga `List.copyOf` / `Set.copyOf` / `Map.copyOf` (clean-code 16.3)
- `collect(Collectors.toList())` o'rniga `stream().toList()` (clean-code 16.3)
- qo'lda konfiguratsiya sinfi o'rniga `@ConfigurationProperties` record, constructor binding (patterns 24.26)

Tuzoqlar:
- `Collections.unmodifiableList` faqat ko'rinish, manba o'zgarsa u ham o'zgaradi; chegarada `List.copyOf` oling (clean-code 16.3)
- `final` va record faqat havolani qotiradi, ichidagi `Date`, massiv yoki `ArrayList` o'zgaraveradi; `Instant`, record, `List.copyOf` ishlating (clean-code 16.2)
- JPA entity `@OneToMany` kolleksiyasini `List.copyOf` bilan almashtirish dirty checking va `orphanRemoval` ni buzadi; getterda `unmodifiableList` qaytaring (patterns 24.26)
