# test: ma'lumot

Minimal shakl (testing 10.3):

```java
public final class CustomerTestBuilder {
    private String email = "alisher@example.com";
    private CustomerTier tier = CustomerTier.STANDARD;

    public static CustomerTestBuilder aCustomer() { return new CustomerTestBuilder(); }

    public CustomerTestBuilder vip() { tier = CustomerTier.VIP; return this; }

    public Customer build() { return new Customer(email, tier); }
}
// testda: Customer customer = aCustomer().vip().build();
```

Allaqachon bor, yozmang:
- Maxsus holat qatorlarini Java da insert qilish o'rniga `@Sql("/data/customers.sql")` (testing 10.7)
- Reference ma'lumotni har testda yuklash o'rniga `spring.flyway.locations` ga `classpath:db/testdata` va `R__` repeatable migration (testing 10.7)
- Ahamiyatsiz maydonlarni qo'lda to'ldirish o'rniga `Instancio.of(...).set(...).create()` va `@Seed` (testing 10.6)

Tuzoqlar:
- `isEqualTo(1L)` yoki `@Sql` dagi id ga tayanmang: saqlangan obyekt qaytargan id ni oling, test id larini seed dan uzoq bazadan boshlang (testing 10.14, 10.7)
- `RANDOM_PORT` bilan `@Transactional` test ishlamaydi, server boshqa thread da ma'lumotni ko'rmaydi; `TRUNCATE ... RESTART IDENTITY CASCADE` bilan aniq tozalang (testing 10.8)
- Builder default i `null` bo'lsa test o'tadi, production validatsiyasi buziladi; har maydonga valid default bering (testing 10.14, 10.3)
