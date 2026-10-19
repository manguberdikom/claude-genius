# servis qatlami

Minimal shakl (patterns 8.4, patterns 8.24):

```java
@Service
class OrderService {
    private final OrderRepository orders;

    OrderService(OrderRepository orders) {
        this.orders = orders;
    }

    @Transactional
    public void cancel(long id, String reason) {
        orders.findById(id).orElseThrow().cancel(reason);
    }
}
```

Allaqachon bor, yozmang:
- Metod boshida qo'lda rol tekshiruvi o'rniga `@PreAuthorize("hasRole('MANAGER')")` (patterns 8.4)
- Argumentlarni `if` bilan tekshirish o'rniga sinfga `@Validated` va parametrga `jakarta.validation` annotatsiyasi (patterns 8.4)
- Har metodda qo'lda metrika yoki log o'rniga `@Observed` yoki `ObservationRegistry` (patterns 8.4)

Tuzoqlar:
- Biznes qoidasi (status tekshiruvi, setter) servisda yozilsa model anemik bo'lib qoida takrorlanadi; qoidani entity metodiga oling, servis faqat yuklab chaqirsin (patterns 8.23, patterns 8.5)
- Repository metodini shunchaki qayta chaqiruvchi pass-through servis qiymat qo'shmaydi; use-case bo'lmasa qatlam ochmang (patterns 8.4)
- Bir servis boshqa aggregate ni to'g'ridan-to'g'ri o'zgartirsa yoki servislar tsiklik bog'lansa chegara noto'g'ri; boshqa aggregate faqat o'z servisi yoki hodisa orqali (patterns 8.24)
