# test: mock

Minimal shakl (testing 6.4, 5.8, 5.15):

```java
@ExtendWith(MockitoExtension.class)
class OrderServiceTest {
    @Mock LoyaltyClient loyalty;
    private final InMemoryOrderRepository orders = new InMemoryOrderRepository();
    private final Clock clock = Clock.fixed(Instant.parse("2026-03-01T10:00:00Z"), ZoneOffset.UTC);

    @Test
    void vipGetsDiscount() {
        var service = new OrderService(orders, new TierDiscountPolicy(loyalty), clock);
        var customer = new CustomerId("c-1");
        when(loyalty.tierOf(customer)).thenReturn(CustomerTier.VIP);

        var order = service.place(customer, List.of(line("SKU-1", 2, "100.00")));

        assertThat(orders.findByNumber(order.number())).get()
                .extracting(Order::total).isEqualTo(Money.of("85.00", "UZS"));
    }
}
```

Allaqachon bor, yozmang:
- qo'lda mock yaratish o'rniga `MockitoExtension` + `@Mock`, `@Captor` (testing 5.7)
- argumentni ushlovchi stub o'rniga `ArgumentCaptor` yoki `argThat(...)` (testing 5.7)
- vaqtni mock qilish o'rniga konstruktorga `Clock.fixed(...)` (testing 6.4)
- kontekstda bean almashtirish: `@MockitoBean` (Boot 3.4+; `@MockBean` 3.4 da deprecated, 4 da yo'q) (patterns 23.13)

Tuzoqlar:
- `@InjectMocks` yoki reflection maydon nomi o'zgarsa `null` beradi; mock'lar `new` bilan konstruktorga (testing 6.2)
- `any()` stub noto'g'ri argumentni ham qabul qiladi; aniq argumentda `STRICT_STUBS` `PotentialStubbingProblem` beradi (testing 5.7)
- mijoz xatosi haqiqiy turda: `RestClient` uchun `RestClientException`, domenga o'giruvchi port uchun domen xatosi; o'ylab topilgan `IllegalStateException` shartnomani buzadi (patterns 24.30, testing 9.4, 5.15)
- har sinfda boshqa `@MockitoBean` to'plami yangi kontekst ko'taradi; mock'lar bitta bazaviy sinfda (testing 7.8)
