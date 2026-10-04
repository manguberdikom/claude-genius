<!-- doc: code-review | chapter: 35 | part: VII. Test review -->

[Kod review](../../README.md) / [Kod review](README.md)

# 35. Test sifati review: assertion, izolyatsiya, beqarorlik (Test Quality)

<details>
<summary>Bu bobdagi 10 bo'lim</summary>

- [35.1 Assertion sifati](#351-assertion-sifati)
- [35.2 Mock ni haddan ortiq ishlatish](#352-mock-ni-haddan-ortiq-ishlatish)
- [35.3 Beqaror (flaky) testlar](#353-beqaror-flaky-testlar)
- [35.4 Test izolyatsiyasi](#354-test-izolyatsiyasi)
- [35.5 Test nomlari va diagnostika](#355-test-nomlari-va-diagnostika)
- [35.6 Test ma'lumotini qurish](#356-test-malumotini-qurish)
- [35.7 Testlardagi anti-naqshlar](#357-testlardagi-anti-naqshlar)
- [35.8 Test ijro vaqti](#358-test-ijro-vaqti)
- [35.9 Review checklisti: test sifati](#359-review-checklisti-test-sifati)
- [35.10 Amalda qo'llash](#3510-amalda-qollash)

</details>


To'liqlikdan keyingi savol - testning o'zi ishonchlimi. Yomon test ikki xil zarar keltiradi: o'tib ketadigan xatoni yashiradi (yolg'on ishonch) yoki sababsiz yiqiladi (beqarorlik) va jamoa testlarga ishonishni to'xtatadi. Ikkinchisi birinchisidan ham xavfli, chunki u butun test to'plamini qadrsizlantiradi.

## 35.1 Assertion sifati

```java
// Daraja 1: hech narsa tekshirmaydi (eng ko'p uchraydi).
@Test void createsOrder() {
    Order o = service.place(cmd);
    assertThat(o).isNotNull();                   // har qanday o'zgarishda o'tadi
}

// Daraja 2: mock chaqirilganini tekshiradi (implementatsiyaga bog'liq).
@Test void createsOrder() {
    service.place(cmd);
    verify(repository).save(any());              // nima saqlandi - ma'lum emas
}

// Daraja 3: natijani tekshiradi (yaxshi).
@Test void placedOrderHasCalculatedTotal() {
    Order o = service.place(cmdWithLines(line(2, Money.of(50_000))));
    assertThat(o.total()).isEqualByComparingTo(Money.of(100_000));
    assertThat(o.status()).isEqualTo(NEW);
}

// Daraja 4: natija va yon ta'sirni tekshiradi (eng yaxshi).
@Test void placedOrderIsPersistedWithEventPublished() {
    Order o = service.place(cmdWithLines(line(2, Money.of(50_000))));

    Order stored = orders.findById(o.id()).orElseThrow();   // haqiqatan saqlandi
    assertThat(stored.total()).isEqualByComparingTo(Money.of(100_000));
    assertThat(stored.status()).isEqualTo(NEW);
    assertThat(publishedEvents()).containsExactly(new OrderPlaced(o.id(), o.total()));
}
```

Review mezoni: testni o'qib, "qanday o'zgarish bu testni yiqitadi" degan savolga javob berish. Javob "faqat NPE" bo'lsa, test qiymatsiz.

```bash
# Kuchsiz assertion larni topish: review ning tez qadami.
grep -rn --include='*Test.java' -E \
  'assertThat\([^)]*\)\.isNotNull\(\);|assertNotNull\(|assertTrue\(true\)|assertThat\([^)]*\)\.isNotEmpty\(\);$' \
  src/test/java | head -20

# Assertion siz testlarni topish (faqat chaqiruvdan iborat).
for f in $(grep -rl --include='*Test.java' '@Test' src/test/java); do
  tests=$(grep -c '@Test' "$f")
  asserts=$(grep -cE 'assert|verify|expect|should' "$f")
  [ "$asserts" -lt "$tests" ] && echo "$f: $tests test, $asserts assertion"
done
```

## 35.2 Mock ni haddan ortiq ishlatish

```java
// Naqsh: hamma narsa mock, test faqat o'z mocklarini tekshiradi.
@Test
void calculatesInvoice() {
    when(taxService.vatFor(any())).thenReturn(Money.of(12_000));
    when(discountService.discountFor(any())).thenReturn(Money.of(5_000));
    when(repository.save(any())).thenAnswer(i -> i.getArgument(0));

    Invoice inv = service.create(order);

    verify(taxService).vatFor(order);
    verify(discountService).discountFor(order);
    verify(repository).save(any());
}
// Bu test nimani tekshiradi? Faqat chaqiruvlar ketma-ketligini. Agar
// `create` ichidagi arifmetika xato bo'lsa (vat ni ayirish o'rniga
// qo'shish), test o'tadi. Review izohi: natija qiymati tekshirilishi kerak.

// Yaxshiroq: haqiqiy hisob mantiqini sinash, faqat chegarani mock qilish.
@Test
void invoiceTotalIncludesVatMinusDiscount() {
    // Haqiqiy kalkulyatorlar - ular sof funksiya, mock kerak emas.
    InvoiceService service = new InvoiceService(new VatCalculator(), new DiscountCalculator());

    Invoice inv = service.create(orderWithTotal(Money.of(100_000), GOLD));

    assertThat(inv.net()).isEqualByComparingTo(Money.of(100_000));
    assertThat(inv.vat()).isEqualByComparingTo(Money.of(12_000));
    assertThat(inv.discount()).isEqualByComparingTo(Money.of(15_000));
    assertThat(inv.total()).isEqualByComparingTo(Money.of(97_000));   // 100000+12000-15000
}
```

Review qoidasi: mock faqat chegarada (tashqi servis, tarmoq, vaqt, tasodif) ishlatiladi. Domen obyektlari va sof hisob mantiqi mock qilinmaydi - ular tez va determinantli.

## 35.3 Beqaror (flaky) testlar

Beqaror test - o'zgarmagan kodda ba'zan o'tadigan, ba'zan yiqiladigan test. Ularning sabablari cheklangan ro'yxatda va review da aniqlash mumkin.

| Sabab | Belgisi diffda | Yechim |
| --- | --- | --- |
| Haqiqiy vaqt | `LocalDate.now()`, `Instant.now()` | `Clock` inyeksiyasi |
| Uyqu bilan kutish | `Thread.sleep(100)` | Awaitility yoki sinxron signal |
| Tartibga tayanish | `assertThat(list).containsExactly(...)` tartibsiz manbadan | `containsExactlyInAnyOrder` |
| Umumiy holat | `static` maydon, umumiy baza | Har test uchun izolyatsiya |
| Test tartibi | Bir test ikkinchisiga tayanadi | `@DirtiesContext` yoki tozalash |
| Tasodifiy ma'lumot | `Random` seed siz | Belgilangan seed |
| Parallel ijro | Bir xil resursga tegish | Alohida ma'lumot yoki `@Isolated` |
| Tarmoq | Haqiqiy tashqi servis | Mock server (WireMock) |
| Vaqt zonasi | Server zonasiga tayanish | Aniq zona |
| Portga bog'lanish | Qattiq port | Tasodifiy port |

```java
// Eng ko'p uchraydigan beqarorlik: sleep bilan kutish.
@Test
void sendsNotificationAsync() throws Exception {
    service.place(cmd);
    Thread.sleep(500);                           // ba'zan yetmaydi, har doim sekin
    verify(mailer).send(any());
}

// To'g'ri: shartni kutish, belgilangan vaqt oynasida.
@Test
void sendsNotificationAsync() {
    service.place(cmd);
    await().atMost(Duration.ofSeconds(5))
           .pollInterval(Duration.ofMillis(50))
           .untilAsserted(() -> verify(mailer).send(any()));
}
// Foydasi: tez holatda darhol o'tadi, sekin holatda 5 sekund kutadi,
// va yiqilganda aniq xabar beradi.

// Vaqt: Clock bilan to'liq nazorat.
@Test
void subscriptionExpiresAfterOneYear() {
    Clock clock = Clock.fixed(Instant.parse("2026-10-04T00:00:00Z"), ZoneOffset.UTC);
    Subscription s = new Subscription(period(2025, 10, 4, 2026, 10, 3), price);
    assertThat(s.isExpired(clock)).isTrue();
    // Hech qachon o'zgarmaydi: bugungi sanaga bog'liq emas.
}
```

## 35.4 Test izolyatsiyasi

```java
// Naqsh: testlar umumiy bazani ishlatadi va bir-biriga ta'sir qiladi.
@SpringBootTest
class OrderServiceTest {
    @Test void test1() { service.place(cmd); assertThat(orders.count()).isEqualTo(1); }
    @Test void test2() { service.place(cmd); assertThat(orders.count()).isEqualTo(1); }
    // Ikkinchi test birinchisidan keyin yiqiladi: count = 2.
}

// Yechim 1: @Transactional - har test oxirida rollback (eng tez).
@SpringBootTest
@Transactional
class OrderServiceTest { }
// Diqqat: bu yondashuv tranzaksiya xulqini yashiradi - commit bo'lmagani
// uchun `AFTER_COMMIT` listener lar ishlamaydi va poyga testlari mumkin
// emas. Shu sababli tranzaksiya mantiqini sinaydigan testlar uchun
// boshqa usul kerak.

// Yechim 2: har test oldidan tozalash (aniq va ishonchli).
@BeforeEach
void cleanDatabase() {
    jdbc.execute("TRUNCATE orders, order_line, payment CASCADE");
}

// Yechim 3: har test o'z ma'lumotini yaratadi (unique kalitlar bilan).
private String uniqueEmail() { return "test-" + UUID.randomUUID() + "@example.com"; }
// Bu usul parallel ijroga ham imkon beradi - eng masshtablanadigan yo'l.
```

## 35.5 Test nomlari va diagnostika

```java
// Nomi hech narsa aytmaydi: yiqilganda nima buzilganini bilmaymiz.
@Test void test1() { }
@Test void orderTest() { }
@Test void shouldWork() { }

// Nomi xulqni aytadi: CI loglarida o'qiladi.
@Test void cancellingShippedOrderIsRejected() { }
@Test void totalIncludesVatForDomesticCustomers() { }
@Test void duplicateIdempotencyKeyReturnsOriginalResponse() { }

// Assertion xabari: yiqilganda kontekst beradi.
assertThat(order.total())
    .as("buyurtma %s uchun jami summa (2 qator x 50000)", order.number())
    .isEqualByComparingTo(Money.of(100_000));
// Yiqilganda: "buyurtma ORD-123 uchun jami summa (2 qator x 50000)
// expected: 100000 but was: 50000" - sabab darhol ko'rinadi.
```

## 35.6 Test ma'lumotini qurish

```java
// Naqsh: har testda uzun qurilish kodi - test maqsadi ko'rinmaydi.
@Test void test() {
    Customer c = new Customer();
    c.setName("Ali"); c.setEmail("ali@x.com"); c.setTier(GOLD);
    c.setRegisteredAt(LocalDate.of(2020, 1, 1)); c.setPhone("+998901234567");
    Order o = new Order();
    o.setCustomer(c); o.setStatus(NEW); o.setCreatedAt(Instant.now());
    // ... 15 qator; asl maqsad: GOLD mijoz uchun chegirma
}

// To'g'ri: test ma'lumoti quruvchisi, faqat muhim qism ko'rinadi.
@Test void goldCustomerGetsFifteenPercent() {
    Order order = anOrder()
        .forCustomer(aCustomer().withTier(GOLD))     // qolgani standart
        .withLine(2, Money.of(50_000))
        .build();

    assertThat(calculator.discountFor(order)).isEqualByComparingTo(Money.of(15_000));
}
// Review foydasi: testni o'qiyotgan odam darhol ko'radi - GOLD va summa
// muhim, qolgani ahamiyatsiz. Builder esa yangi majburiy maydon
// qo'shilganda bitta joyda tuzatiladi.
```

## 35.7 Testlardagi anti-naqshlar

| Anti-naqsh | Nega yomon |
| --- | --- |
| Testdagi mantiq (`if`, sikl) | Test o'zi xato bo'lishi mumkin |
| Kutilgan qiymatni hisoblash | Kod bilan bir xil xatoni takrorlaydi |
| Bitta testda ko'p stsenariy | Yiqilganda joy noaniq |
| Tasodifiy ma'lumot (seed siz) | Takrorlanmaydigan yiqilish |
| `@Disabled` izohsiz | Abadiy o'chirilgan test |
| `try/catch` bilan istisnoni yutish | Test har doim o'tadi |
| Prod bazasiga ulanish | Xavfli va beqaror |
| Juda ko'p `@SpringBootTest` | Sekin pipeline |
| Testni tuzatish uchun kodni o'zgartirish | Niyat buziladi |
| Assertion dan keyin kod | Yetib bo'lmaydigan tekshiruvlar |

```java
// Kutilgan qiymatni hisoblash: eng nozik anti-naqsh.
@Test void calculatesVat() {
    BigDecimal expected = total.multiply(new BigDecimal("0.12"));   // kod bilan bir xil
    assertThat(calculator.vat(total)).isEqualByComparingTo(expected);
}
// Agar stavka noto'g'ri bo'lsa (0.12 o'rniga 0.15 bo'lishi kerak bo'lsa),
// test ham xato stavka bilan hisoblaydi va o'tadi.
// To'g'ri: kutilgan qiymat qo'lda yozilgan konstanta.
assertThat(calculator.vat(Money.of(100_000))).isEqualByComparingTo(Money.of(12_000));

// try/catch bilan yutish: test hech narsa tekshirmaydi.
@Test void test() {
    try { service.doSomething(); }
    catch (Exception e) { /* ignore */ }         // istisno bo'lsa ham o'tadi
}
```

## 35.8 Test ijro vaqti

Sekin test to'plami - jarayon muammosi: jamoa testlarni lokalda ishga tushirishni to'xtatadi va xatolar CI ga ko'chadi.

```bash
# Eng sekin testlarni topish: review va optimizatsiya uchun.
./mvnw test
# Surefire hisobotlaridan vaqtni chiqarish:
for f in target/surefire-reports/*.xml; do
  awk -F'"' '/<testsuite /{print $(NF-1)" "$2}' "$f" 2>/dev/null
done | sort -rn | head -15

# Spring kontekst necha marta qurilgan (eng katta sekinlik manbasi).
grep -rc 'Starting .*Test' target/surefire-reports/*.txt 2>/dev/null | head

# Review izohi: har xil @MockBean kombinatsiyasi YANGI kontekst yaratadi.
# 20 xil kombinatsiya = 20 kontekst = 20 x ishga tushish vaqti.
# Yechim: @MockBean larni umumiy bazaviy klassga yig'ish.
```

| Test turi | Maqbul vaqt | Chegara |
| --- | --- | --- |
| Unit (domen) | < 10 ms | 50 ms |
| Spring slice (`@WebMvcTest`) | < 1 s | 3 s |
| Integratsion (Testcontainers) | < 5 s | 15 s |
| Butun unit to'plami | < 1 daqiqa | 3 daqiqa |
| Butun CI pipeline | < 10 daqiqa | 20 daqiqa |

## 35.9 Review checklisti: test sifati

| Savol | Nega |
| --- | --- |
| Assertion qiymatni tekshiradimi | Yolg'on ishonch |
| `isNotNull` yolg'iz ishlatilmaydimi | Hech narsa tekshirilmaydi |
| Mock faqat chegarada ishlatilganmi | Implementatsiya testi |
| `Thread.sleep` bormi | Beqarorlik va sekinlik |
| Vaqt `Clock` orqalimi | Sana bilan bog'liq yiqilish |
| Testlar bir-biridan mustaqilmi | Tartibga bog'liqlik |
| Test nomi xulqni aytadimi | Diagnostika |
| Kutilgan qiymat qo'lda yozilganmi | Bir xil xatoni takrorlash |
| Testda mantiq (`if`, sikl) yo'qmi | Test xatosi |
| `@Disabled` sabab va tiket bilanmi | O'lik test |
| Test ma'lumoti builder bilanmi | O'qiluvchanlik va yangilash |
| Ijro vaqti chegaradami | Lokalda ishlatilmaslik |

## 35.10 Amalda qo'llash

- [ ] Kuchsiz assertion larni (`isNotNull` yolg'iz, `assertNotNull`) topib, ularni qiymat tekshiruviga aylantiring.
- [ ] `Thread.sleep` ishlatilgan testlarni Awaitility ga o'tkazing.
- [ ] Domen kodida `Instant.now()` va `LocalDate.now()` ni `Clock` inyeksiyasiga o'tkazib, testlarni `Clock.fixed` ga asoslang.
- [ ] Faqat `verify(...)` bilan tugaydigan testlarni toping va natija tekshiruvini qo'shing.
- [ ] Test izolyatsiyasi strategiyasini kelishib oling (tranzaksion rollback, truncate yoki unique ma'lumot) va `REVIEW.md` ga yozing.
- [ ] Test ma'lumoti uchun builder yoki fabrika klasslarini kiritib, uzun qurilish kodini olib tashlang.
- [ ] `@Disabled` testlarni sanab, har biriga tiket va sabab qo'shing yoki o'chirib tashlang.
- [ ] Eng sekin 15 testni aniqlab, Spring kontekst kombinatsiyalarini kamaytirishni rejalashtiring.
- [ ] Beqaror testlarni aniqlash uchun CI da testlarni kuniga bir marta 3 takror ishga tushirib, natijani kuzatib boring.

---

[&larr; 34. Test to'liqligini review qilish](34-test-toliqligini-review-qilish.md) · [Mundarija](README.md) · [36. Test turi va integratsion test review &rarr;](36-test-turi-va-integratsion-test-review.md)
