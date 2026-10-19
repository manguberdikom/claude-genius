# oqim va lambda

Minimal shakl (clean-code 24.4, 24.6):

```java
public List<OrderId> readyToShip(List<Order> orders) {
    return orders.stream()
            .filter(Order::isReadyToShip)
            .map(Order::id)
            .toList();
}

public Money totalOf(OrderId id) {
    return repository.findById(id)
            .map(Order::total)
            .orElseThrow(() -> new OrderNotFoundException(id));
}
```

Allaqachon bor, yozmang:
- o'z funksional interfeysi o'rniga `Function`, `Predicate`, `Supplier`, primitivda `IntUnaryOperator` (clean-code 24.3)
- `isPresent()` va `get()` o'rniga `map(...).orElse(...)` / `orElseThrow` (clean-code 24.6)
- `filter(Optional::isPresent).map(Optional::get)` o'rniga `flatMap(Optional::stream)` (clean-code 24.6)
- `forEach(x -> list.add(...))` o'rniga `map(...).toList()` (clean-code 24.4)

Tuzoqlar:
- `orElse(load(id))` qiymat bo'lsa ham bazani chaqiradi; qimmat zaxira `orElseGet(() -> load(id))` bilan (clean-code 24.6)
- ikki argumentli `toMap` dublikat kalitda `IllegalStateException` tashlaydi; merge funksiyasini oshkor bering yoki `groupingBy` (clean-code 23.3)
- `forEach` ichida maydon, tashqi ro'yxat yoki `save` o'zgartirish jim poyga va N so'rov beradi; oqim natija qaytarsin, yozish paket amalida (clean-code 24.4)
