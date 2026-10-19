# shart va sikl

Minimal shakl (sonarqube 15.5, clean-code 6.1, clean-code 6.6):

```java
Money shippingFee(Order order) {
    if (order.isFreeShipping()) {
        return Money.ZERO;
    }
    return switch (order.shipping()) {
        case STANDARD -> STANDARD_FEE;
        case EXPRESS -> EXPRESS_FEE;
        case FREIGHT -> FREIGHT_RATE_PER_KG.times(order.weightKg());
    };
}
```

Allaqachon bor, yozmang:
- `for-each` ichida `remove` o'rniga `orders.removeIf(Order::isExpired)` (clean-code 7.6)
- Erta chiqishli qidiruv sikli o'rniga `stream().filter(...).findFirst()` (clean-code 7.7)
- Ichma-ich `null` tekshiruvi o'rniga `Optional.map(...).orElse(...)` (clean-code 6.8)
- Strategiya tanlovchi `switch` o'rniga Spring kiritgan `List<Strategy>` dan `Map` (sonarqube 15.6)

Tuzoqlar:
- Enum ustidagi `switch` da `default` yangi a'zoni jimgina yutadi; uni yozmang, to'liqlikni kompilyator tekshirsin (clean-code 6.6)
- Ichma-ich `if` har qavatda S3776 balliga chuqurlik qo'shadi; tekshiruvni guard clause bilan boshga chiqaring (sonarqube 15.1, 15.5)
- Bir xil `switch` bir necha joyda takrorlansa, har shox enum a'zosining metodiga ko'chadi (clean-code 6.10)
