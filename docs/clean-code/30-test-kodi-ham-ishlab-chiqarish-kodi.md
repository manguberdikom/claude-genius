<!-- doc: clean-code | chapter: 30 | part: IX. Test kodining tozaligi -->

[Barcha hujjatlar](../../README.md) / [Toza kod qoidalari](README.md)

> Holat: AI yozgan, inson tekshirmagan.

# 30. Test kodi ham ishlab chiqarish kodi (Test Code Is Production Code)

<details>
<summary>Bu bobdagi 10 bo'lim</summary>

- [30.1 Toza test nega kod bazasini saqlab qoladi](#301-toza-test-nega-kod-bazasini-saqlab-qoladi)
- [30.2 DRY va DAMP muvozanati testda](#302-dry-va-damp-muvozanati-testda)
- [30.3 Test ma'lumot quruvchilari: builder va object mother](#303-test-malumot-quruvchilari-builder-va-object-mother)
- [30.4 Testda mantiq bo'lmasligi](#304-testda-mantiq-bolmasligi)
- [30.5 Bir tushuncha, bir test](#305-bir-tushuncha-bir-test)
- [30.6 Assertion o'qilishi va xato xabari](#306-assertion-oqilishi-va-xato-xabari)
- [30.7 Test dublyorlarini nomlash va chegaralash](#307-test-dublyorlarini-nomlash-va-chegaralash)
- [30.8 Testlar orasidagi bog'liqlik va tartib](#308-testlar-orasidagi-bogliqlik-va-tartib)
- [30.9 Test hidlari katalogi](#309-test-hidlari-katalogi)
- [30.10 Amalda qo'llash](#3010-amalda-qollash)

</details>


Test strategiyasi, piramida, FIRST printsiplari, AAA tuzilishi va test nomlash [testlash qo'llanmasidagi](../testing/README.md) test piramidasi bo'limida berilgan; Sonar ning test kodiga tegishli qoidalari [SonarQube hujjatidagi](../sonarqube/README.md) test kodidagi Sonar qoidalari bo'limida. Bu bobda faqat bitta mavzu: test kodining **o'qilishi va saqlanishi**.

## 30.1 Toza test nega kod bazasini saqlab qoladi

Test kodi iflos bo'lsa, u o'zgarishga qarshilik qiladi: har bir refaktoring o'nlab testni buzadi va jamoa refaktoringdan voz kechadi. Natijada ishlab chiqarish kodi ham eskiradi. Shu sababli test kodining tozaligi ishlab chiqarish kodining tozaligidan kam ahamiyatli emas.

Teskari tomoni ham bor: ishonchli test to'plami refaktoringni **bepul** qiladi. Bu hujjatdagi deyarli har bir refaktoring harakati (35-37 boblar) xavfsizlik to'rini talab qiladi, va u to'r - testlar.

## 30.2 DRY va DAMP muvozanati testda

Ishlab chiqarish kodida DRY (takrorlanmaslik) ustun; test kodida esa DAMP (Descriptive And Meaningful Phrases) ko'pincha ustun turadi. Sababi: test o'qilganda u **o'z-o'zidan tushunarli** bo'lishi kerak, boshqa fayllarga qarashga majbur qilmasligi lozim.

```java
// yomon: haqiqiy qiymatlar umumiy setup da yashirin - test nima tekshirayotgani ko'rinmaydi
@BeforeEach
void setUp() {
    order = TestData.defaultOrder();      // ichida nima bor?
}

@Test
void rejectsRefundExceedingPayment() {
    assertThatThrownBy(() -> service.refund(order, TestData.bigAmount()));
}

// yaxshi: muhim qiymatlar testda ko'rinadi, qolgani builder standartida
@Test
void rejectsRefundExceedingPayment() {
    Order order = anOrder().withSettledAmount(Money.of("100.00", UZS)).build();

    assertThatThrownBy(() -> service.refund(order, Money.of("150.00", UZS)))
            .isInstanceOf(RefundExceedsPaymentException.class);
}
```

Qoida: testga **ta'sir qiladigan** qiymatlar testda ko'rinadi; ahamiyatsiz qiymatlar builder standartida qoladi.

## 30.3 Test ma'lumot quruvchilari: builder va object mother

Test ma'lumotini qurish takrorlanishi eng katta test qarzi manbai. Ikki pattern ishlaydi va ularni birga ishlatish mumkin.

**Test data builder** - standart qiymatlar bilan to'ldirilgan builder, testda faqat muhim maydon o'zgartiriladi. **Object mother** - nomlangan tipik holatlar fabrikasi (`aSettledPayment()`, `anExpiredOrder()`). Builder'ning to'liq shakli, nested builder va Lombok `@Builder` bilan farqi testing hujjatidagi [Test Data Builder pattern](../testing/10-test-malumotlarini-boshqarish.md#103-test-data-builder-pattern) mavzusida.

```java
// Test data builder: standart qiymatlar + nuqtali o'zgartirish
public final class OrderBuilder {

    private OrderId id = OrderId.of("ORD-1");
    private OrderStatus status = OrderStatus.CONFIRMED;
    private Money settledAmount = Money.of("100.00", UZS);
    private Instant createdAt = Instant.parse("2026-01-01T00:00:00Z");

    public static OrderBuilder anOrder() { return new OrderBuilder(); }

    public OrderBuilder withStatus(OrderStatus status) { this.status = status; return this; }
    public OrderBuilder withSettledAmount(Money amount) { this.settledAmount = amount; return this; }

    public Order build() { return new Order(id, status, settledAmount, createdAt); }
}

// Object mother: tipik holatlar nomlangan
public final class Orders {
    public static Order settled() { return anOrder().withStatus(SETTLED).build(); }
    public static Order expired() { return anOrder().withCreatedAt(LONG_AGO).build(); }
}
```

## 30.4 Testda mantiq bo'lmasligi

Testda `if`, sikl yoki hisob bo'lsa, test o'zi xato bo'lishi mumkin va uni hech narsa tekshirmaydi. Bundan tashqari, shartli test ba'zi yo'llarni umuman sinamaydi va bu coverage hisobotida ko'rinmaydi.

```java
// yomon: testda shart - qaysi shox bajarilgani ko'rinmaydi
@Test
void calculatesTax() {
    for (Region region : Region.values()) {
        Money tax = policy.taxFor(region, net);
        if (region == Region.FREE_ZONE) {
            assertThat(tax).isEqualTo(Money.ZERO);
        } else {
            assertThat(tax).isGreaterThan(Money.ZERO);
        }
    }
}

// yaxshi: parametrlangan test, har bir holat alohida va kutilgan qiymat oshkor
@ParameterizedTest
@CsvSource({
        "TASHKENT,   100.00, 12.00",
        "FREE_ZONE,  100.00,  0.00",
        "SAMARKAND,  100.00, 12.00"
})
void calculatesTax(Region region, String net, String expectedTax) {
    assertThat(policy.taxFor(region, Money.of(net, UZS)))
            .isEqualTo(Money.of(expectedTax, UZS));
}
```

## 30.5 Bir tushuncha, bir test

"Bir testda bir assert" qoidasi juda qattiq; to'g'ri qoida - **bir testda bir tushuncha**. Bitta natijaning bir nechta jihati tekshirilsa, bir necha assert normal; ikki mustaqil xatti-harakat tekshirilsa, ikki test kerak.

```java
// yaxshi: bir tushuncha (yaratilgan refund holati), bir necha assert
@Test
void createsRefundInPendingState() {
    Refund refund = refunds.create(command, key);

    assertThat(refund.status()).isEqualTo(PENDING);
    assertThat(refund.amount()).isEqualTo(Money.of("50.00", UZS));
    assertThat(refund.requestedAt()).isEqualTo(FIXED_NOW);
}

// yaxshi: AssertJ bilan bitta assert, xato xabari to'liq
assertThat(refund)
        .extracting(Refund::status, Refund::amount)
        .containsExactly(PENDING, Money.of("50.00", UZS));
```

## 30.6 Assertion o'qilishi va xato xabari

Test yiqilganda uning xabari **sababni** aytishi kerak, aks holda diagnostika vaqti ketadi. AssertJ ning aniq assertion lari umumiylaridan ancha yaxshi xabar beradi.

```java
// yomon: "expected true but was false" - nima xato ekani ko'rinmaydi
assertTrue(refund.amount().equals(expected));
assertTrue(orders.size() == 3);

// yaxshi: xabar farqni ko'rsatadi
assertThat(refund.amount()).isEqualTo(expected);
assertThat(orders).hasSize(3);

// yaxshi: domen tilida, kontekst bilan
assertThat(orders)
        .as("tasdiqlangan buyurtmalar %s mijoz uchun", customerId)
        .extracting(Order::status)
        .containsOnly(CONFIRMED);
```

## 30.7 Test dublyorlarini nomlash va chegaralash

Test dublyorlari (mock, stub, fake) [testlash qo'llanmasida](../testing/README.md) batafsil. Bu yerda tozalik qoidasi: mock soni testning dizayn signali. Bir testda beshta mock bo'lsa, tekshirilayotgan sinfning bog'liqliklari juda ko'p (26.1).

Ikkinchi qoida: **o'zingiz yozmagan** turlarni mock qilmaslik. Uchinchi tomon kutubxonasining mock i uning haqiqiy xatti-harakatini takrorlamaydi va test yolg'on ishonch beradi; o'rniga wrapper yozib, uni mock qilish kerak (18.3).

```java
// yomon: tashqi kutubxona turi mock qilingan - haqiqiy xatti-harakat boshqa
@Mock RestTemplate restTemplate;

// yaxshi: o'z interfeysimiz mock qilinadi; integratsiya alohida testlanadi
@Mock PaymentGateway gateway;
```

## 30.8 Testlar orasidagi bog'liqlik va tartib

Testlar bir-biridan mustaqil bo'lishi kerak: har qanday tartibda, alohida yoki parallel ishga tushirilganda bir xil natija berishi lozim. Bog'liqlik odatda umumiy o'zgaradigan holatdan keladi: statik maydon (16.9), umumiy baza yozuvi, fayl tizimi.

```java
// yomon: statik holat testlar orasida oqib ketadi
static List<Order> created = new ArrayList<>();

// yomon: test tartibiga bog'liq
@Test @Order(1) void createsOrder() { ... }
@Test @Order(2) void findsCreatedOrder() { ... }     // birinchisiga bog'liq

// yaxshi: har bir test o'z ma'lumotini yaratadi va tozalaydi
@Test
void findsCreatedOrder() {
    Order saved = repository.save(anOrder().build());

    assertThat(repository.findById(saved.id())).contains(saved);
}
```

## 30.9 Test hidlari katalogi

Test kodidagi hidlar alohida katalogga ega va ularning har biri aniq muammoni bildiradi.

| Hid | Belgisi | Yechim |
|---|---|---|
| Qotib qolgan test (fragile) | mantiq o'zgarmasa ham yiqiladi | ichki tuzilish emas, xatti-harakat tekshirish |
| Sekin test | bir test sekundlar oladi | mock yoki slice test ([testlash qo'llanmasi](../testing/README.md)) |
| Shartli test | ichida `if`/sikl | parametrlangan test (30.4) |
| Assertsiz test | faqat chaqiradi | assertion qo'shish yoki o'chirish |
| Yashirin bog'liqlik | tartibga bog'liq | izolyatsiya (30.8) |
| Ko'p mock | 4+ mock | sinf bog'liqliklarini kamaytirish |
| Noaniq nom | `test1`, `testOrder` | xatti-harakat nomi (3.12) |
| Takrorlangan setup | har testda 20 qator | builder (30.3) |
| Erkin assert | `assertNotNull` bilan tugaydi | aniq kutilgan qiymat |
| `Thread.sleep` | vaqtga bog'liq | Awaitility yoki `Clock` (22.3) |
| Izohga olingan test | `// @Test` | o'chirish yoki tuzatish |
| `@Disabled` sababsiz | sababsiz o'chirilgan | sabab va ticket yozish |

## 30.10 Amalda qo'llash

- [ ] Test ma'lumoti qurish takrorlanishini topib, har bir agregat uchun test data builder yozing.
- [ ] Testlardagi `if`, sikl va hisobni topib, parametrlangan testga aylantiring.
- [ ] `assertTrue`/`assertNotNull` assertion larini AssertJ ning aniq assertion lariga o'tkazing.
- [ ] Uchinchi tomon turlarining mock larini topib, o'z wrapper interfeysingizni mock qiling.
- [ ] Statik holat va test tartibiga bog'liqlikni yo'qotib, testlarni tasodifiy tartibda ishga tushirib tekshiring.
- [ ] `Thread.sleep` ishlatilgan testlarni Awaitility yoki qotirilgan `Clock` ga o'tkazing.
- [ ] `@Disabled` testlarni ro'yxatlab, har biriga sabab va ticket qo'shing yoki o'chiring.
- [ ] 30.9 jadvalidagi hidlar bo'yicha test kodini bir marta to'liq ko'rib chiqib, ro'yxat tuzing.

---

[&larr; 29. Log kodining tozaligi](29-log-kodining-tozaligi.md) · [Mundarija](README.md) · [31. TDD intizomi va kod dizayniga ta'siri &rarr;](31-tdd-intizomi-va-kod-dizayniga-tasiri.md)
