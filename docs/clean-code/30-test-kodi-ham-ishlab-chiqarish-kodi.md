<!-- doc: clean-code | chapter: 30 | part: IX. Test kodining tozaligi -->

[Barcha hujjatlar](../../README.md) / [Toza kod qoidalari](README.md)

> Holat: tekshirilgan (2026-10-19). Manbalar bob oxirida.

# 30. Test kodi ham ishlab chiqarish kodi (Test Code Is Production Code)

<details>
<summary>Bu bobdagi 11 bo'lim</summary>

- [30.1 Toza test nega kod bazasini saqlab qoladi](#301-toza-test-nega-kod-bazasini-saqlab-qoladi)
- [30.2 DRY va DAMP muvozanati testda](#302-dry-va-damp-muvozanati-testda)
- [30.3 Test ma'lumot quruvchilari: builder va object mother](#303-test-malumot-quruvchilari-builder-va-object-mother)
- [30.4 Testda mantiq bo'lmasligi](#304-testda-mantiq-bolmasligi)
- [30.5 Bir tushuncha, bir test](#305-bir-tushuncha-bir-test)
- [30.6 Assertion o'qilishi va xato xabari](#306-assertion-oqilishi-va-xato-xabari)
- [30.7 Test dublyorlarini nomlash va chegaralash](#307-test-dublyorlarini-nomlash-va-chegaralash)
- [30.8 Testlar orasidagi bog'liqlik va tartib](#308-testlar-orasidagi-bogliqlik-va-tartib)
- [30.9 Test hidlari katalogi](#309-test-hidlari-katalogi)
- [30.10 Test kirish qiymatini tanlash](#3010-test-kirish-qiymatini-tanlash)
- [30.11 Amalda qo'llash](#3011-amalda-qollash)

</details>


Test strategiyasi, piramida, FIRST printsiplari, AAA tuzilishi va test nomlash [testlash qo'llanmasidagi](../testing/README.md) test piramidasi bo'limida berilgan; Sonar ning test kodiga tegishli qoidalari [SonarQube hujjatidagi](../sonarqube/README.md) test kodidagi Sonar qoidalari bo'limida. Bu bobda faqat bitta mavzu: test kodining **o'qilishi va saqlanishi**.

## 30.1 Toza test nega kod bazasini saqlab qoladi

Test kodi iflos bo'lsa, u o'zgarishga qarshilik qiladi: har bir refaktoring o'nlab testni buzadi va jamoa refaktoringdan voz kechadi. Natijada ishlab chiqarish kodi ham eskiradi. Shu sababli test kodining tozaligi ishlab chiqarish kodining tozaligidan kam ahamiyatli emas.

Teskari tomoni ham bor: ishonchli test to'plami refaktoringni **bepul** qiladi. Bu hujjatdagi deyarli har bir refaktoring harakati (35-37 boblar) xavfsizlik to'rini talab qiladi, va u to'r - testlar.

"Kam ahamiyatli emas" iborasi hamma o'lchovga tegmaydi va buni aniq aytish kerak, aks holda qoida ortiqcha ishga olib keladi. Standart ikkiga bo'linadi: test kodi sodda, qisqa va ifodali bo'lishi **shart**, lekin ishlab chiqarish kodi kabi **samarali** bo'lishi shart emas, chunki test muhiti xotira va protsessor cheklovida ishlamaydi. Ajratuvchi shart shu: **tozalik** o'lchovi ikkala kodda bir xil, **samaradorlik** o'lchovi bir xil emas.

Amalda bu shunday ko'rinadi: testda satrni oddiy konkatenatsiya bilan qurish, har bir testda ma'lumotni noldan yasash yoki ortiqcha nusxa olish haqli, chunki o'qilishni oshiradi va narxi sezilmaydi; ishlab chiqarish kodida esa shu tanlovlar o'lchanadi. Chegara ham bor: yon ta'sir bitta testdan chiqib to'plam darajasiga o'tsa, qoida teskarisiga aylanadi - sekin test to'plami tez qaytish halqasini buzadi (39.7), shuning uchun samaradorlikdan voz kechish bitta test ichida haqli, butun to'plam darajasida esa emas.

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

**Yordamchi metod nomi assert qilishini ko'rsatadi.** Test kodidagi yordamchi metodlar ikki turga bo'linadi va ularni nomdan ajratish kerak: biri o'zi tasdiqlash bajaradi, ikkinchisi oddiy, "testdan bexabar" yordamchi (fixture quradi, ma'lumot qo'shadi). Boswell va Foucher ning konvensiyasi: tasdiqlash bajaradigan metodga `assert` yoki `check` prefiksi qo'yiladi (`checkScoresBeforeAfter`), oddiy yordamchi esa oddiy nom oladi (`addScoredDoc`). Shunda testni o'qiyotgan odam qaysi qator muvaffaqiyatsizlikka olib kelishi mumkinligini nomdan ko'radi va yiqilish sababini qidirish tezlashadi.

Test metodining o'z nomi uchun qoida boshqa: u **tekshirilayotgan sinf, funksiya va holat** haqida ma'lumot beradi. `Test1`, `Test2` kabi nomlar taqiqlanadi; nom uzun chiqishi muammo emas, chunki uni hech kim chaqirmaydi va aksariyat freymvork xato hisobotida aynan shu nomni chiqaradi, ya'ni nom izoh vazifasini o'taydi.

```java
// Tasdiqlash bajaradi: nomi shuni aytadi
private void assertScoresAfterFiltering(String input, String expected) {
    assertThat(sorter.sortAndFilter(parse(input)))
            .extracting(ScoredDoc::score)
            .containsExactlyElementsOf(parse(expected));
}

// Testdan bexabar oddiy yordamchi: oddiy nom
private ScoredDoc scoredDoc(String url, double score) {
    return new ScoredDoc(url, score);
}
```

ESLATMA: `assert` yoki `check` prefiksi tanlovi jamoa kelishuviga qoladi, muhimi bitta prefiks butun kod bazasida ishlatilishi (2.11).

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

## 30.10 Test kirish qiymatini tanlash

Test ma'lumoti qanday qurilishi [test data builder](#303-test-malumot-quruvchilari-builder-va-object-mother)
bo'limida ko'rildi; bu bo'lim boshqa savolga javob beradi: builder ga qanday
QIYMAT berish kerak. Mezon ikkita va ular bir-biriga qarshi ishlaydi: qiymatlar
kodni to'liq tekshirsin, va ayni paytda o'qishga sodda bo'lsin. Boswell va
Foucher qoidani shunday beradi: kodni to'liq ishlatadigan eng sodda qiymatlar
to'plamini tanlash kerak (Boswell/Foucher, *The Art of Readable Code*, 1-nashr,
O'Reilly, 2011, 14-bob (156-bet)).

Ikki tomonga ham xato bo'ladi. `"1, 2, 3"` kirishi sodda, lekin manfiy qiymatni
filtrlash xatti-harakatini umuman tekshirmaydi. `"123014, -1082342, 823423,
234205, -235235"` esa keraksiz murakkab va ayni paytda kodni to'liq ham
tekshirmaydi. Kitob o'z misolidagi `-99998.7` qiymatini tanqid qiladi: u shunchaki
"biror manfiy son" degani edi, demak `-1` yetadi; agar "juda katta manfiy son"
nazarda tutilgan bo'lsa, `-1e100` kabi aniq qiymat yozilishi kerak. Natijada
`"-5, 1, 4, -99998.7, 3"` kirishi `"1, 2, -1, 3"` ga qisqaradi va samarasini
yo'qotmaydi (shu yerda, 156-157-bet).

```java
// yomon: qiymatlar shovqinli, nega aynan shular ekani ko'rinmaydi
@Test
void filtersNegativeScores() {
    List<Integer> result = ranking.sortAndFilter(
            List.of(-5, 1, 4, -99998, 3));
    assertThat(result).containsExactly(4, 3, 1);
}

// yaxshi: eng sodda qiymatlar, lekin manfiy filtri ham tekshiriladi
@Test
void filtersNegativeScores() {
    List<Integer> result = ranking.sortAndFilter(List.of(1, 2, -1, 3));
    assertThat(result).containsExactly(3, 2, 1);
}
```

Ikkita qo'shimcha qoida shundan chiqadi. Birinchi: bitta xatti-harakatni
tekshirish uchun bitta namuna yetadi - manfiy qiymat filtrlanishini ko'rsatish
uchun ro'yxatda bitta manfiy son bo'lishi kifoya. Ikkinchi: katta va "vahshiy"
kirish bilan sinash foydali (bufer chegarasi va kutilmagan xatolarni ochadi),
lekin u testda qo'lda yozilmaydi - katta kirish programma yo'li bilan quriladi,
chunki qo'lda yozilgan uzun ro'yxat o'qilmaydi va stress test sifatida ham
to'liq ishlamaydi (shu yerda, 157-bet).

```java
// yaxshi: katta kirish qo'lda yozilmaydi, generatsiya qilinadi
@Test
void handlesLargeInput() {
    List<Integer> scores = IntStream.rangeClosed(1, 100_000).boxed().toList();
    assertThat(ranking.sortAndFilter(scores)).hasSize(100_000);
}
```

Qiymat tanlash chegaraviy holat bilan birga ishlaydi: eng sodda qiymat to'plami
odatiy yo'lni qamraydi, chegara (bo'sh ro'yxat, bitta element, maksimal qiymat)
esa alohida test bo'ladi, chunki ularni bitta testga tiqish
[bir tushuncha, bir test](#305-bir-tushuncha-bir-test) qoidasini buzadi.

## 30.11 Amalda qo'llash

- [ ] Test ma'lumoti qurish takrorlanishini topib, har bir agregat uchun test data builder yozing.
- [ ] Testlardagi `if`, sikl va hisobni topib, parametrlangan testga aylantiring.
- [ ] `assertTrue`/`assertNotNull` assertion larini AssertJ ning aniq assertion lariga o'tkazing.
- [ ] Uchinchi tomon turlarining mock larini topib, o'z wrapper interfeysingizni mock qiling.
- [ ] Statik holat va test tartibiga bog'liqlikni yo'qotib, testlarni tasodifiy tartibda ishga tushirib tekshiring.
- [ ] `Thread.sleep` ishlatilgan testlarni Awaitility yoki qotirilgan `Clock` ga o'tkazing.
- [ ] `@Disabled` testlarni ro'yxatlab, har biriga sabab va ticket qo'shing yoki o'chiring.
- [ ] 30.9 jadvalidagi hidlar bo'yicha test kodini bir marta to'liq ko'rib chiqib, ro'yxat tuzing.
- [ ] Testlardagi uzun va "shovqinli" kirish qiymatlarini (`-99998.7`, `123014`) eng sodda ekvivalentiga almashtirib, assertion o'zgarmasligini tekshiring.
- [ ] Qo'lda yozilgan uzun kirish ro'yxatlarini generatsiya qiluvchi kodga o'tkazing.

## Manbalar

- Dustin Boswell, Trevor Foucher, *The Art of Readable Code*, 1-nashr, O'Reilly, 2011 (copyright 2012), 14-bob (158-159-betlar) - test yordamchisi nomida uning o'zi assert qilishini ko'rsatish (`assert` yoki `check` prefiksi, `checkScoresBeforeAfter` va `addScoredDoc` farqi), test metodi nomining sinf, funksiya va holatni aytishi hamda uzun nomning izoh vazifasini o'tashi
- Robert C. Martin, *Clean Code*, 9-bob ("Keeping Tests Clean") - test kodi ishlab chiqarish kodi bilan bir xil standartda
- Robert C. Martin, *Clean Code*, 9-bob ("One Assert per Test", "Single Concept per Test") - bir testda bir tushuncha, assert soni minimallashtiriladi
- Robert C. Martin, *Clean Code*, 9-bob ("F.I.R.S.T.") - tez, mustaqil, qaytariladigan, o'zini tasdiqlaydigan, o'z vaqtida
- Robert C. Martin, *Clean Code*, 17-bob, T1-T9 - test evristikalari
- Dustin Boswell, Trevor Foucher, *The Art of Readable Code*, 1-nashr, O'Reilly, 2011 (copyright 2012), 14-bob (156-157-betlar) - kodni to'liq ishlatadigan eng sodda kirish to'plami mezoni, `-99998.7` ni `-1` ga qisqartirish, bitta manfiy qiymat yetishi, va katta "smasher" kirishni qo'lda yozmasdan programma yo'li bilan qurish
- Robert C. Martin, *Clean Code*, 9-bob ("Dual Standard") (127-130-betlar) - ikki standart: test kodi sodda, qisqa va ifodali bo'lishi shart, lekin ishlab chiqarish kodi kabi samarali bo'lishi shart emas, chunki test muhiti resurs cheklovida ishlamaydi
- ESLATMA: tozalik o'lchovi bir xil, samaradorlik o'lchovi bir xil emas degan ajratuvchi shart korpus qarori: kitob ikki standartni sanaydi, korpusning o'zi esa test kodini ishlab chiqarish kodi bilan bir xil standartda deb yozadi; shart ikkisini o'lchov bo'yicha ajratadi. Qoidaning to'plam darajasidagi chegarasi ham korpus qo'shimchasi

---

[&larr; 29. Log kodining tozaligi](29-log-kodining-tozaligi.md) · [Mundarija](README.md) · [31. TDD intizomi va kod dizayniga ta'siri &rarr;](31-tdd-intizomi-va-kod-dizayniga-tasiri.md)
