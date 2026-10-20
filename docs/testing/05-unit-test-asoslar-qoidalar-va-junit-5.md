<!-- doc: testing | chapter: 5 | part:  -->

[Barcha hujjatlar](../../README.md) / [Testlash qo'llanmasi](README.md)

> Holat: tekshirilmoqda. Da'volar hali manbaga solishtirilmoqda.

# 5. Unit test: asoslar, qoidalar va JUnit 5 (Unit Testing - Foundations, Rules & JUnit 5)

<details>
<summary>Bu bobdagi 17 bo'lim</summary>

- [5.1 Unit test nima va nima emas](#51-unit-test-nima-va-nima-emas)
- [5.2 FIRST printsiplari](#52-first-printsiplari)
- [5.3 Arrange-Act-Assert va test nomlash](#53-arrange-act-assert-va-test-nomlash)
- [5.4 JUnit 5 asoslari: lifecycle va tuzilma](#54-junit-5-asoslari-lifecycle-va-tuzilma)
- [5.5 Parametrlashtirilgan testlar](#55-parametrlashtirilgan-testlar)
- [5.6 AssertJ bilan tasdiqlash](#56-assertj-bilan-tasdiqlash)
- [5.7 Mockito bilan test double'lar](#57-mockito-bilan-test-doublelar)
- [5.8 Over-mocking muammosi va fake'lar](#58-over-mocking-muammosi-va-fakelar)
- [5.9 Istisno, chegara holatlari va null-safety](#59-istisno-chegara-holatlari-va-null-safety)
- [5.10 Vaqt, tasodif va UUID'ni testlash](#510-vaqt-tasodif-va-uuidni-testlash)
- [5.11 Property-based testing: jqwik](#511-property-based-testing-jqwik)
- [5.12 Mutation testing bilan sifatni o'lchash (PIT)](#512-mutation-testing-bilan-sifatni-olchash-pit)
- [5.13 Unit test anti-patternlari](#513-unit-test-anti-patternlari)
- [5.14 Test case sonini kod tuzilishidan chiqarish: structured basis va data-flow](#514-test-case-sonini-kod-tuzilishidan-chiqarish-structured-basis-va-data-flow)
- [5.15 Test double intizomi: real implementatsiya va fake](#515-test-double-intizomi-real-implementatsiya-va-fake)
- [5.16 Interaction tekshiruvi va ortiqcha aniqlik](#516-interaction-tekshiruvi-va-ortiqcha-aniqlik)
- [5.17 Arxitektor nazorat ro'yxati](#517-arxitektor-nazorat-royxati)

</details>



Unit test - test strategiyasining eng arzon va eng tez fikr-mulohaza (feedback) manbasi: u sekundlar ichida ishlaydi, xatoni aniq joyda ko'rsatadi va refaktoringga ruxsat beradi. Ammo noto'g'ri yozilgan unit testlar teskari ta'sir qiladi: ular implementatsiyaga yopishib qoladi, har bir o'zgarishda yuzlab test qizil bo'ladi va jamoa oxirida testlarni o'chirib tashlaydi. Shu sababli arxitektor uchun muhim savol "qancha test bor?" emas, balki "test nimaga bog'langan?" bo'ladi. Quyidagi barcha misollar Java 17+ (Java 21/25 da ham o'zgarishsiz ishlaydi), JUnit 5 (Jupiter), AssertJ va Mockito 5.x uchun amal qiladi.

## 5.1 Unit test nima va nima emas

Eng keng tarqalgan xato - "unit" so'zini "sinf" deb tushunish. Agar har bir sinf uchun bitta test sinfi majburiy bo'lsa, test to'plami kod tuzilishining ko'zguga aylanadi: ikki sinfni bittaga qo'shsangiz, mantiq o'zgarmasa ham, testlar buziladi. To'g'ri yondashuv - unitni *xatti-harakat* (behaviour) deb olish: tashqi dunyo uchun ma'noga ega bo'lgan eng kichik qaror. `PriceCalculator` ichidagi `DiscountPolicy`, `RoundingRule` va `TaxTable` birgalikda bitta unit bo'lishi mumkin; ular public API emas, implementatsiya detali.

Shu nuqtada ikki uslub ajraladi. **Solitary** unit test sinovdan o'tayotgan obyektning barcha hamkorlarini (collaborator) test double bilan almashtiradi - izolyatsiya maksimal, lekin test ichki tuzilishni biladi. **Sociable** unit test esa faqat protsess chegarasidan tashqariga chiqadigan hamkorlarni (DB, HTTP, broker, tizim vaqti) almashtiradi, qolgan domen obyektlarini haqiqiy holda ishlatadi. Amalda arxitektura qoidasi oddiy: **sociable - standart, solitary - istisno**. Mock faqat I/O, nodeterminizm yoki sekinlik chegarasida paydo bo'ladi.

"Public API" bu yerda til visibility si emas. Google ning formulasi: public API deganda **jamoadan tashqariga** ochilgan API tushuniladi, Java da `public` deb belgilangan hamma narsa emas (sinf `public` bo'lishi mumkin, lekin faqat o'sha unit ichidagi boshqa paketlar uchun). Shundan uch amaliy qoida chiqadi: faqat bir-ikki sinfga xizmat qiladigan yordamchi sinf alohida unit emas va u egalari orqali testlanadi; egalariga murojaat qilmasdan istalgan kishi ishlata oladigan paket albatta unitdir va to'g'ridan-to'g'ri testlanadi; faqat egalari murojaat qiladigan, lekin ko'p kontekstda ishlatiladigan umumiy **support kutubxona** ham unit hisoblanadi va to'g'ridan-to'g'ri testlanadi. Oxirgi holatda testda takrorlanish paydo bo'ladi (kutubxona kodi o'z testi bilan ham, foydalanuvchilarining testi bilan ham qoplanadi) va bu takrorlanish foydali: foydalanuvchi va uning testi bir kun o'chirilsa, qamrovda jim bo'shliq paydo bo'lmaydi.

Unit test nima emas: u DB bilan gaplashmaydi, Spring kontekstini ko'tarmaydi, tarmoqqa chiqmaydi, fayl tizimiga tayanmaydi va boshqa testning natijasiga bog'liq bo'lmaydi. Qaysi sinflarni umuman Spring'siz testlash kerakligi [6-bobda](06-unit-test-spring-loyihasida-kontekstsiz.md) batafsil ko'rib chiqiladi.

## 5.2 FIRST printsiplari

**Fast.** Butun unit to'plam bir necha o'n sekundda tugashi kerak, aks holda uni hech kim lokal ishlatmaydi. Amaliy mezon: bitta test < 10 ms. Agar sekin bo'lsa - sababi deyarli har doim I/O yoki kontekst yuklanishi.

**Isolated.** Test o'z ma'lumotini o'zi tayyorlaydi va global holatni (static field, singleton cache, `System` property, `TimeZone` default) o'zgartirmaydi. Izolyatsiya buzilishining klassik belgisi - test yolg'iz ishlaganda yashil, to'plamda qizil.

**Repeatable.** Bir xil kirish → bir xil natija, mashinadan, soatdan va tartibdan qat'i nazar. `Instant.now()`, `Math.random()`, `UUID.randomUUID()`, `Locale.getDefault()` - barchasi repeatability dushmani.

**Self-validating.** Test o'zi "o'tdi/o'tmadi" deb javob beradi; log o'qish yoki konsolni ko'z bilan tekshirish talab qilinmaydi. `System.out.println` bilan "tekshirish" - test emas.

**Timely.** Test kodga yaqin vaqtda yoziladi (ideal holda - oldin). Keyinga qoldirilgan test API dizaynini yaxshilash imkonini yo'qotadi va "endi testlash qiyin" degan xulosaga olib keladi - bu dizayn muammosining signali.

## 5.3 Arrange-Act-Assert va test nomlash

Har bir test uchta ko'rinadigan bosqichdan iborat bo'lishi kerak: **Arrange** (holatni tayyorlash), **Act** (bitta chaqiruv), **Assert** (natijani tasdiqlash). BDD atamalarida bu Given-When-Then. Qoida: **bitta testda bitta xatti-harakat va bitta Act**. Agar testda ikkinchi `service.doSomething()` paydo bo'lsa, demak ikkita test kerak.

```java
class PriceCalculatorTest {
    private final PriceCalculator calculator = new PriceCalculator();

    @Test
    @DisplayName("Haqiqiy kupon yakuniy narxni 10% kamaytiradi")
    void appliesPercentageDiscountWhenCouponIsValid() {
        // Arrange
        Order order = new Order(List.of(new Item("book", money("100.00"), 2)));
        Coupon coupon = Coupon.percentage("SUMMER10", 10);

        // Act
        Money total = calculator.total(order, coupon);

        // Assert
        assertThat(total).isEqualTo(money("180.00"));
    }
}
```

Nomlash konvensiyalari, afzalliklari bilan:

1. `method_stateUnderTest_expectedBehaviour` - `pay_whenCardExpired_throwsPaymentDeclined`. Tuzilgan, lekin metod nomiga bog'langan: refaktoringdan keyin nom yolg'on gapiradi.
2. `should...When...` - `shouldThrowWhenCardExpired`. O'qiladi, ammo "should" har bir nomda takrorlanib shovqin hosil qiladi.
3. `given...When...Then...` - `givenExpiredCard_whenPaying_thenThrows`. BDD jamoalari uchun qulay, lekin nomlar uzayib ketadi.
4. **Xatti-harakat gapi** - `rejectsPaymentWhenCardExpired`, ustiga `@DisplayName` bilan to'liq o'zbekcha/inglizcha tavsif.

**Tavsiya: 4-variant.** Metod nomi emas, qarorning natijasi nomlanadi; `@DisplayName` esa hisobotda to'liq gap beradi. `@DisplayNameGeneration(DisplayNameGenerator.ReplaceUnderscores.class)` bilan pastki chiziqli nomlarni avtomatik gapga aylantirish ham mumkin.

**Nomdagi "and" ikkita xatti-harakat borligini aytadi.** Google ning qoidasi: test nomini yozayotganda `and` so'zi kerak bo'lsa, ehtimol test bir nechta xatti-harakatni tekshiryapti va ikkiga bo'linishi kerak. Ya'ni nom bitta Act qoidasining ([bu bo'limning boshi](#53-arrange-act-assert-va-test-nomlash)) mashinasiz tekshiruvi bo'lib ishlaydi. `rejectsPaymentWhenCardExpiredAndLogsAudit` ikkita test: biri rad etishni, ikkinchisi audit yozuvini tekshiradi. Nom yozish qiyin bo'lsa vaqtincha `should` bilan boshlash yordam beradi: sinf nomi bilan birga o'qilganda nom gapga aylanadi ("BankAccount should not allow withdrawals when balance is empty") va shu gapda `and` darhol ko'rinadi. Nom uzun chiqishi muammo emas, chunki uni hech kim chaqirmaydi: u xato hisobotida birinchi va ko'pincha yagona ko'rinadigan matn.

Shu bilan **test bajariladigan hujjat** bo'lib ishlaydi. Bir vaqtda bitta xatti-harakatni tekshiradigan aniq va qisqa test "kod shu holatda nima qiladi" savoliga javob beradi, hujjat esa javob bermaydi, chunki hujjatning kod bilan aloqasi tekshirilmaydi. Talab o'zgarib yangi kod mavjud testni buzsa, "hujjat" eskirgani darhol ko'rinadi. Bu faqat test toza va qisqa ushlangan holda ishlaydi: 40 qatorlik setup va `if` li test hujjat emas.

## 5.4 JUnit 5 asoslari: lifecycle va tuzilma

`@Test` - `void`, parametrsiz (yoki inyeksiya qilinadigan parametrlar bilan), `public` bo'lishi shart emas. Lifecycle: `@BeforeEach`/`@AfterEach` har bir testdan oldin/keyin, `@BeforeAll`/`@AfterAll` esa sinf darajasida bir marta ishlaydi va standart holatda `static` bo'lishi kerak. `@Nested` ichki sinflar bilan testlarni kontekst bo'yicha guruhlash - eng kuchli o'qiluvchanlik vositasi: tashqi `@BeforeEach` ichki sinflarda ham ishlaydi. `@Nested` ning uchta qattiq sharti bor: sinf **non-static inner** bo'lishi kerak (static nested sinf `@Nested` bo'la olmaydi), annotatsiyaning o'zi meros olinmaydi, va `@BeforeAll`/`@AfterAll` ni `@Nested` ichida ishlatish Java versiyasiga bog'liq: Java 16 dan boshlab ularni `static` deb e'lon qilish har ikki lifecycle rejimida ishlaydi, undan oldingi Java da esa faqat per-class lifecycle bilan.

```java
@DisplayName("CartService")
class CartServiceTest {
    private Cart cart;

    @BeforeEach
    void setUp() {
        cart = new Cart("user-1");
    }

    @Nested
    @DisplayName("savat bo'sh bo'lganda")
    class WhenEmpty {
        @Test
        void totalIsZero() {
            assertThat(cart.total()).isEqualTo(Money.ZERO);
        }

        @Test
        void checkoutIsRejected() {
            assertThatThrownBy(cart::checkout)
                    .isInstanceOf(EmptyCartException.class);
        }
    }
}
```

**Test instance lifecycle.** Standart holat - `PER_METHOD`: har bir test uchun test sinfining yangi nusxasi yaratiladi, shu sababli maydonlar testlar orasida oqib ketmaydi. `@TestInstance(TestInstance.Lifecycle.PER_CLASS)` bitta nusxani barcha testlarga beradi - `@BeforeAll` ni non-static qilish va qimmat setup'ni bir marta bajarish imkonini beradi, ammo holat izolyatsiyasini o'zingiz ta'minlashingiz kerak. Arxitektor qoidasi: `PER_CLASS` ni faqat o'zgarmas (immutable) setup uchun ruxsat ber.

**`@Disabled` xavfi.** O'chirilgan test - yashil CI'da yashiringan qizil test. U eskiradi, kompilyatsiya qilinadi, lekin hech narsani himoya qilmaydi. Qoida: `@Disabled` faqat sababi va issue havolasi bilan (`@Disabled("PAY-412: gateway sandbox o'chirilgan")`) va muddat bilan; sababsiz `@Disabled` CI'da fail bo'lishi kerak. Platforma/shart asosida o'tkazib yuborish uchun `@EnabledOnOs`, `@EnabledIfSystemProperty`, `@EnabledIfEnvironmentVariable` yoki `Assumptions.assumeTrue(...)` ishlatiladi - bu `@Disabled` dan ancha halolroq.

## 5.5 Parametrlashtirilgan testlar

Parametrlashtirish kerak bo'lgan vaziyat aniq: **bir xil xatti-harakat, faqat ma'lumot farq qiladi**. Agar har bir holat uchun turli assertion mantiqi kerak bo'lsa - bu alohida testlar, parametr emas. `junit-jupiter-params` artefakti talab qiladi.

```java
class IbanValidatorTest {
    private final IbanValidator validator = new IbanValidator();

    @ParameterizedTest(name = "[{index}] {0} haqiqiy")
    @ValueSource(strings = {"UZ8300010000000000000001", "DE89370400440532013000"})
    void acceptsValidIbans(String iban) {
        assertThat(validator.isValid(iban)).isTrue();
    }

    @ParameterizedTest
    @CsvSource({"UZ8, TOO_SHORT", "XX89370400, UNKNOWN_COUNTRY"})
    void rejectsWithReason(String iban, IbanError expected) {
        assertThat(validator.validate(iban).error()).isEqualTo(expected);
    }

    @ParameterizedTest
    @NullAndEmptySource
    @ValueSource(strings = {"   ", "\t"})
    void rejectsBlankInput(String iban) {
        assertThat(validator.isValid(iban)).isFalse();
    }
}
```

Manbalar xaritasi: `@ValueSource` - bitta primitiv/String parametr; `@CsvSource` va `@CsvFileSource` - bir necha ustun, `nullValues`/`delimiter` sozlamalari bilan; `@MethodSource("name")` - murakkab obyektlar uchun `static Stream<Arguments>` qaytaruvchi metod; `@EnumSource(value = OrderStatus.class, names = {"PENDING", "PAID"})` yoki `mode = EXCLUDE` - enum bo'ylab to'liq qamrov (yangi enum qiymati qo'shilganda test avtomatik o'sadi); `@ArgumentsSource(ExpiredCardsProvider.class)` - qayta ishlatiladigan `ArgumentsProvider` implementatsiyasi. `@NullSource`, `@EmptySource`, `@NullAndEmptySource` - null-safety uchun eng arzon qamrov.

## 5.6 AssertJ bilan tasdiqlash

JUnit'ning `assertEquals` uchta muammoga ega: argument tartibi (expected/actual) adashtiradi, kolleksiyalar va obyekt graflari uchun imkoniyat bermaydi, xato xabari esa "expected: 2 but was: 3" dan nariga o'tmaydi. AssertJ fluent API bilan IDE avtomatik to'ldirishi orqali kashf qilinadigan, aniq diagnostikali assertion beradi.

```java
// Yomon: tarqoq, xato xabari ma'nosiz
@Test
void badAssertions() {
    List<Order> orders = service.findPending();
    assertEquals(2, orders.size());
    assertEquals("A-1", orders.get(0).number());
    assertTrue(orders.get(0).total().compareTo(BigDecimal.TEN) > 0);
}

// Yaxshi: bitta oqim, to'liq diagnostika
@Test
void goodAssertions() {
    assertThat(service.findPending())
            .as("kutilayotgan buyurtmalar")
            .hasSize(2)
            .extracting(Order::number, Order::status)
            .containsExactly(tuple("A-1", PENDING), tuple("A-2", PENDING));

    assertThat(service.findPending()).first().satisfies(order -> {
        assertThat(order.total()).isGreaterThan(money("10.00"));
        assertThat(order.customer().email()).endsWith("@example.com");
    });
}
```

Kalit vositalar: `extracting` - kolleksiyadan maydonlarni ajratib, `containsExactly` (tartib muhim), `containsExactlyInAnyOrder` (tartib muhim emas) yoki `allSatisfy` bilan tekshirish; `satisfies` - bitta element uchun bir necha shartni guruhlash; `assertThatThrownBy` - istisnolar; `usingRecursiveComparison` - `equals` yozmasdan butun obyekt grafini solishtirish; `SoftAssertions` - barcha xatolarni bir yugurishda ko'rish.

```java
@Test
void mapsDtoIgnoringTechnicalFields() {
    OrderDto dto = mapper.toDto(order);

    assertThat(dto)
            .usingRecursiveComparison()
            .ignoringFields("createdAt", "version")
            .isEqualTo(expectedDto);
}
```

Domen tilida o'qiladigan testlar uchun custom assertion yozing - bu takrorlanuvchi tekshiruvlarni bir joyga yig'adi:

```java
public class OrderAssert extends AbstractAssert<OrderAssert, Order> {

    private OrderAssert(Order actual) {
        super(actual, OrderAssert.class);
    }

    public static OrderAssert assertThat(Order actual) {
        return new OrderAssert(actual);
    }

    public OrderAssert isPaid() {
        isNotNull();
        if (actual.status() != OrderStatus.PAID) {
            failWithMessage("<%s> uchun PAID kutilgan, aslida <%s>",
                    actual.number(), actual.status());
        }
        return this;
    }
}
```

## 5.7 Mockito bilan test double'lar

`@ExtendWith(MockitoExtension.class)` (`mockito-junit-jupiter` artefakti) `@Mock`, `@Spy`, `@Captor` va `@InjectMocks` maydonlarini to'ldiradi hamda har bir testdan keyin tekshiruvni ishga tushiradi. Mockito 5.x standart holatda `inline` mock maker ishlatadi - `final` sinf va metodlarni ham mock qiladi, `mockito-inline` alohida qo'shilishi shart emas.

```java
@ExtendWith(MockitoExtension.class)
class OrderServiceTest {

    @Mock private PaymentGateway gateway;
    @Mock private OrderRepository repository;
    @InjectMocks private OrderService service;
    @Captor private ArgumentCaptor<Payment> paymentCaptor;

    @Test
    void chargesGatewayWithOrderTotal() {
        Order order = pending("A-1", money("250.00"));
        when(repository.findByNumber("A-1")).thenReturn(Optional.of(order));
        when(gateway.charge(any(Payment.class)))
                .thenReturn(PaymentResult.approved("tx-9"));

        service.pay("A-1");

        verify(gateway).charge(paymentCaptor.capture());
        assertThat(paymentCaptor.getValue().amount()).isEqualTo(money("250.00"));
    }
}
```

`thenThrow(new GatewayTimeoutException())` bilan xato yo'llarini, `ArgumentCaptor` bilan uzatilgan argumentni, `ArgumentMatchers` (`any()`, `eq()`, `argThat(p -> ...)`) bilan moslashuvchan moslikni oling. Muhim qoida: bitta chaqiruvda matcher ishlatsangiz, qolgan barcha argumentlar ham matcher bo'lishi kerak (`eq("A-1")`).

**Strict stubbing.** `MockitoExtension` standart holatda `Strictness.STRICT_STUBS` rejimida ishlaydi: ishlatilmagan stub `UnnecessaryStubbingException`, mos kelmagan argument bilan chaqiruv esa `PotentialStubbingProblem` beradi. Bu o'lik stub'larni va noto'g'ri tushunchalarni darhol oshkor qiladi - uni `@MockitoSettings(strictness = Strictness.LENIENT)` bilan o'chirish kodni emas, muammoni yashirish demakdir.

**Nimani mock qilmaslik kerak:** value object va DTO (`Money`, `Address`, `OrderDto`) - ularni shunchaki yarating; JDK sinflari (`List`, `Map`, `Optional`, `String`, `LocalDate`) - haqiqiy nusxa doim arzonroq; sinovdan o'tayotgan sinfning o'zi (`@Spy` + partial mock - dizayn muammosining belgisi); sof funksiyalar va mapper'lar. `@Spy` faqat legacy kodni bosqichma-bosqich qamrab olishda vaqtinchalik vosita bo'lishi kerak.

## 5.8 Over-mocking muammosi va fake'lar

Haddan ziyod mock qilingan test o'zini testlaydi: `when(a.b()).thenReturn(c); when(c.d()).thenReturn(e);` zanjiri kodning *qanday yozilganini* yozib oladi, *nima qilishini* emas. Belgilari: testda 5+ `when`, mock mock qaytaradi, assertion'lar faqat `verify` dan iborat, nomi o'zgarmagan refaktoringda o'nlab test buziladi. Bunday test regressiyani tutmaydi, lekin refaktoringni to'xtatadi - eng yomon kombinatsiya.

Davosi - **fake** (haqiqiy, lekin soddalashtirilgan implementatsiya) va **stub** (oldindan belgilangan javob). Repository, cache, clock va event publisher uchun in-memory fake yozish bir marta qilinadigan 20 qatorlik ish, lekin o'nlab testni mock zanjirlaridan xalos qiladi:

```java
public class InMemoryOrderRepository implements OrderRepository {
    private final Map<String, Order> store = new ConcurrentHashMap<>();

    @Override
    public Optional<Order> findByNumber(String number) {
        return Optional.ofNullable(store.get(number));
    }

    @Override
    public Order save(Order order) {
        store.put(order.number(), order);
        return order;
    }
}

@Test
void paidOrderIsPersistedWithPaidStatus() {
    OrderRepository repository = new InMemoryOrderRepository();
    OrderService service = new OrderService(repository, new ApprovingGateway());
    repository.save(pending("A-1", money("250.00")));

    service.pay("A-1");

    assertThat(repository.findByNumber("A-1")).get().extracting(Order::status).isEqualTo(PAID);
}
```

Fake natijani (state) tekshiradi, mock esa o'zaro ta'sirni (interaction). Qoida: **holat tekshiruvi - birinchi tanlov; interaction tekshiruvi faqat natija ko'rinmaydigan joyda** (email yuborildimi, event chiqdimi, to'lov chaqirildimi).

## 5.9 Istisno, chegara holatlari va null-safety

Istisnoni `try/catch` + `fail()` bilan emas, `assertThatThrownBy` bilan tekshiring: tur, xabar va kontekst maydonlarining barchasini. Chegara holatlari esa buglarning asosiy uyasi: 0, 1, -1, `MIN_VALUE`/`MAX_VALUE`, bo'sh kolleksiya, bitta elementli kolleksiya, aniq teng qiymat (`isBefore` vs `isAfter` chegarasi), yakshanba/oy oxiri, scale va rounding (`BigDecimal.ZERO` va `0.00` `equals` bo'yicha teng emas - shu sababli `isEqualByComparingTo` yoki `Money` value object ishlating).

```java
@Test
void rejectsNegativeAmount() {
    assertThatThrownBy(() -> Money.of(new BigDecimal("-1.00"), "UZS"))
            .isInstanceOf(InvalidAmountException.class)
            .hasMessageContaining("manfiy")
            .hasFieldOrPropertyWithValue("currency", "UZS")
            .hasNoCause();

    assertThatNullPointerException()
            .isThrownBy(() -> Money.of(null, "UZS"));

    assertThatCode(() -> Money.of(BigDecimal.ZERO, "UZS"))
            .doesNotThrowAnyException();
}
```

Null-safety uchun eng samarali strategiya - null'ni API chegarasida taqiqlash (`Objects.requireNonNull`, `Optional` qaytarish, JSpecify/`@NonNull` annotatsiyalari) va shu shartnomani `@NullSource`/`@NullAndEmptySource` bilan testlash. Null'ni domen ichiga kiritmaslik - testlarni ikki barobar kamaytiradi.

## 5.10 Vaqt, tasodif va UUID'ni testlash

`Instant.now()` ni to'g'ridan-to'g'ri chaqirgan kodni determinizm bilan testlash mumkin emas. Yechim - vaqtni dependency qilish: `java.time.Clock` ni Spring bean sifatida e'lon qilib (`@Bean Clock clock() { return Clock.systemUTC(); }`) konstruktor orqali inyeksiya qiling, testda esa `Clock.fixed(...)` yoki `Clock.offset(...)` bering.

```java
// Yomon: test tizim soatiga bog'langan, chegarani tekshirib bo'lmaydi
public boolean isExpired(Subscription s) {
    return s.endsAt().isBefore(Instant.now());
}
```

```java
public class SubscriptionService {
    private final Clock clock;

    public SubscriptionService(Clock clock) {
        this.clock = clock;
    }

    public boolean isExpired(Subscription s) {
        return s.endsAt().isBefore(clock.instant());
    }
}

@Test
void isNotExpiredExactlyAtBoundary() {
    Instant now = Instant.parse("2026-01-01T00:00:00Z");
    var service = new SubscriptionService(Clock.fixed(now, ZoneOffset.UTC));

    assertThat(service.isExpired(new Subscription(now))).isFalse();
    assertThat(service.isExpired(new Subscription(now.minusMillis(1)))).isTrue();
}
```

Xuddi shu naqsh tasodif va identifikatorlar uchun: `UUID.randomUUID()` o'rniga `Supplier<UUID> idGenerator`, `Random` o'rniga `IntSupplier` yoki urug' (seed) bilan `new Random(42)`. Testda `() -> UUID.fromString("00000000-0000-0000-0000-000000000001")` beriladi va natija to'liq oldindan aytiladi. **`Thread.sleep` ishlatmang** - u testni sekin va flaky qiladi; asinxron natija uchun Awaitility yoki boshqariladigan executor (`new SyncTaskExecutor()`) ishlating. Flaky testlar bilan kurash [16-bobda](16-flaky-testlar-test-qarzi-va-test-kodini.md).

## 5.11 Property-based testing: jqwik

Misol asosidagi test siz o'ylagan holatlarni tekshiradi; property-based test esa *invariant* ni e'lon qiladi va yuzlab tasodifiy kirishni o'zi generatsiya qiladi, xato topilganda esa uni minimal misolga qisqartiradi (shrinking). jqwik JUnit 5 platformasining mustaqil test engine'i sifatida ishlaydi va mavjud Jupiter testlari bilan birga yashaydi.

```java
class MoneyProperties {

    @Property
    void additionIsCommutative(@ForAll("amounts") BigDecimal a,
                               @ForAll("amounts") BigDecimal b) {
        assertThat(Money.of(a, "UZS").plus(Money.of(b, "UZS")))
                .isEqualTo(Money.of(b, "UZS").plus(Money.of(a, "UZS")));
    }

    @Property
    void stringRoundTripKeepsValue(@ForAll("amounts") BigDecimal a) {
        Money money = Money.of(a, "UZS");
        assertThat(Money.parse(money.toString())).isEqualTo(money);
    }

    @Provide
    Arbitrary<BigDecimal> amounts() {
        return Arbitraries.bigDecimals()
                .between(BigDecimal.ZERO, new BigDecimal("1000000"))
                .ofScale(2);
    }
}
```

Qachon foydali: parser va serializer (round-trip xossasi), pul va soliq hisob-kitoblari (assotsiativlik, taqsimlanish, yig'indi saqlanishi), saralash va ketma-ketlik algoritmlari, domen invariantlari (buyurtma holati hech qachon `PAID` dan `PENDING` ga qaytmaydi), idempotentlik. Qachon foydasiz: CRUD oqimlari, oddiy delegatsiya, I/O bilan ishlovchi kod. Property-based test misol asosidagi testni almashtirmaydi - u o'zingiz o'ylamagan chegara holatlarini topish uchun qo'shimcha qatlam.

## 5.12 Mutation testing bilan sifatni o'lchash (PIT)

Line coverage testlarning *bajarilganini* ko'rsatadi, *tekshirganini* emas: assertion'siz test ham 100% qamrov beradi. Mutation testing bu bo'shliqni yopadi - PIT (pitest) bytecode'ga kichik "mutant"lar kiritadi (`>` ni `>=` ga almashtirish, return qiymatini o'zgartirish, shartni inkor qilish, metod chaqiruvini olib tashlash) va har bir mutant uchun testlarni ishga tushiradi. Agar mutant bilan ham testlar yashil bo'lsa - mutant *tirik qoldi*, ya'ni bu mantiqni hech bir assertion himoya qilmayapti. Asosiy ko'rsatkich - **mutation score** (o'ldirilgan mutantlar ulushi), ko'proq ishonchli variant esa test strength.

Amalda PIT'ni JUnit 5 bilan ishlatish uchun `pitest-maven` (yoki Gradle plugin) yoniga `pitest-junit5-plugin` kerak, va uni butun kod bazasiga emas, domen hamda hisob-kitob paketlariga yo'naltirish to'g'ri bo'ladi - mutation testing CPU talab qiladi. Arxitektor uchun qiymati: mutation score sun'iy coverage KPI'larini oshkor qiladi va "qaysi testlar haqiqatan ishlaydi" degan savolga javob beradi. Konfiguratsiya va incremental analiz SonarQube hujjatidagi [mutation testing](../sonarqube/20-mutation-testing-100-coverage-qachon-yolgon.md#205-pit-pitest-ni-maven-va-gradle-da-ishga-tushirish) mavzusida, CI darvozasidagi o'rni esa [arxitektura testlari va kod sifati](14-arxitektura-testlari-va-kod-sifati.md#147-mutation-testing-pit) bobida.

## 5.13 Unit test anti-patternlari

**Assertion yo'q test.** Faqat chaqiruv bor, natija tekshirilmaydi - u faqat `NullPointerException` ni tutadi. Coverage hisobotini bo'yaydi, regressiyani tutmaydi.

**Logikasi bor test.** `if`, `for`, `switch`, `try/catch` yoki hisob-kitob testning o'zida bo'lsa - testni ham testlash kerak bo'ladi. Buning o'rniga `@ParameterizedTest` va to'g'ridan-to'g'ri yozilgan kutilgan qiymatlar:

```java
// Yomon: assertion yo'q + testning o'zida mantiq
@Test
void processesOrders() {
    for (Order order : randomOrders()) {
        if (order.total().isPositive()) {
            service.process(order);
        }
    }
}

// Yaxshi: har bir holat alohida va determinnistik
@ParameterizedTest
@CsvSource({"250.00, PROCESSED", "0.00, REJECTED"})
void processesOrderByTotal(BigDecimal total, OrderStatus expected) {
    Order order = pending("A-1", Money.of(total, "UZS"));

    assertThat(service.process(order).status()).isEqualTo(expected);
}
```

**Tasodifiy ma'lumotga tayanish.** `Faker` yoki `random()` bilan generatsiya qilingan kirish testni nodeterministik qiladi: bugun yashil, ertaga qizil, ayblanuvchi topilmaydi. Test ma'lumotini aniq va o'qiladigan qilib bering (test data builder'lar [10-bobda](10-test-malumotlarini-boshqarish.md)).

**Testlar orasidagi tartib bog'liqligi.** `static` maydon yoki umumiy DB holati orqali bir test ikkinchisini "tayyorlaydi". JUnit test tartibini kafolatlamaydi; `@TestMethodOrder` bilan tartibni "tuzatish" - muammoni mustahkamlash. Har bir test o'z holatini o'zi quradi.

**Private metodni reflection bilan testlash.** Bu shartnoma emas, implementatsiya detalini qulflash. Agar private metod mustaqil testga arziydigan darajada murakkab bo'lsa - u alohida sinfga chiqarilishi kerak degan signal. `@VisibleForTesting` bilan ko'rinishni ochish ham xuddi shu muammoning yumshoq shakli.

**Haddan ziyod setup.** 40 qatorlik `@BeforeEach` barcha testlarga xizmat qiladi, lekin hech biri uchun aniq emas - testni o'qib, u nimani tekshirayotganini tushunib bo'lmaydi. Setup'ni test uchun ahamiyatli qismini testning o'zida qoldiring, qolganini builder'lar ortiga yashiring.

**Katta kirishni test matniga literal qilib yozish.** Bufer to'lishi yoki chegara xatosini ochish uchun katta kirish kerak bo'lsa, uni testga ko'chirib qo'yish ("smasher" test) ikki tomondan yomon: blok qo'rqinchli ko'rinadi va kodni haqiqatda zo'riqtirmaydi. Bunday kirish kodda dasturiy ravishda quriladi, masalan 100000 qiymatli ro'yxat sikl bilan. Qiymatlar esa iloji boricha sodda bo'lsin: `-99998.7` o'rniga `-1` yetadi, chunki maqsad "istalgan manfiy son" edi.

```java
@Test
void sortsLargeInputWithoutOverflow() {
    List<ScoredDoc> docs = IntStream.range(0, 100_000)
            .mapToObj(i -> new ScoredDoc("doc-" + i, 100_000 - i))
            .toList();

    List<ScoredDoc> sorted = sorter.sortAndFilter(docs);

    assertThat(sorted).hasSize(100_000);
    assertThat(sorted.get(0).score()).isEqualTo(100_000);
}
```

**Boshqalar:** `verify` dan iborat testlar (interaction'ga ortiqcha bog'lanish), `assertTrue(result != null)` kabi ma'nosiz assertion'lar, bir testda 10 ta mantiqiy tekshiruv, va `@Disabled` "vaqtincha" qoldirilgan testlar.

## 5.14 Test case sonini kod tuzilishidan chiqarish: structured basis va data-flow

Qancha test yozish kerakligini taxmin bilan emas, metodning o'z tuzilishidan hisoblash mumkin. McConnell ikkita bir-birini to'ldiradigan usul beradi va tartibni ham aytadi: avval structured basis, keyin undan qolgan bo'shliqni data-flow bilan yopish.

**Structured basis testing: minimal test case soni.** G'oyasi - har bir bayonot hech bo'lmaganda bir marta bajarilsin, lekin buni minimal to'plam bilan qilish. Hisoblash protsedurasi: metod bo'ylab to'g'ri yo'l uchun 1 dan boshlanadi; har bir `if`, `while`, `repeat`, `for`, `and` va `or` uchun 1 qo'shiladi; `case` ning har bir shoxi uchun 1, va agar `default` yo'q bo'lsa yana 1 qo'shiladi. Natija - **minimal** son: olti chiqsa, har qanday olti test yetadi degani emas, har bir kalit so'z uchun kamida bitta `true` va bitta `false` holat bo'lishi shart (McConnell, *Code Complete*, 2-nashr, Microsoft Press, 2004, 22.3 (506-508-bet)). Kitob shu protsedura murakkablikni o'lchash protsedurasi bilan bir xil ekanini ham aytadi, ya'ni [cyclomatic complexity va cognitive complexity farqi](../sonarqube/05-metrikalar-rating-texnik-qarz-murakkablik.md#54-cyclomatic-complexity-va-cognitive-complexity-farqi) bo'limidagi raqam shu yerda to'g'ridan-to'g'ri ishlatiladi: qaror nuqtalari soni + 1 minimal test case sonini beradi. Kitob code coverage va logic coverage yondashuvlarini shu bilan qiyoslaydi: ular ham barcha yo'llarni qoplaydi, lekin minimal to'plam g'oyasi yo'q, shuning uchun bir xil mantiq uchun kerakdan ko'p test chiqadi.

```java
// 1 (to'g'ri yo'l) + 1 (for) + 1 (birinchi if) + 1 (ikkinchi if) + 1 (&&) + 1 (uchinchi if) = 6
BigDecimal totalNetPay(List<Employee> employees) {
    BigDecimal total = BigDecimal.ZERO;
    for (Employee employee : employees) {                       // for
        BigDecimal pension = BigDecimal.ZERO;
        if (employee.pensionWithheld().compareTo(MAX_PENSION) < 0) {   // if
            pension = pensionOf(employee);
        }
        BigDecimal voluntary = BigDecimal.ZERO;
        if (employee.wantsVoluntary() && eligible(employee)) {  // if + &&
            voluntary = voluntaryOf(employee);
        }
        if (eligibleForIra(employee)) {                         // if
            voluntary = voluntary.add(iraOf(employee));
        }
        total = total.add(grossOf(employee).subtract(pension).subtract(voluntary));
    }
    return total;
}
```

Olti holat: hamma shart `true` bo'lgan nominal holat; bo'sh ro'yxat (`for` sharti darhol `false`); birinchi `if` `false`; ikkinchi `if` `&&` ning birinchi qismi tufayli `false`; ikkinchi `if` `&&` ning ikkinchi qismi tufayli `false`; uchinchi `if` `false`.

**Data-flow testing: defined-used yo'llari.** Ikkinchi usul boshqa o'qqa qaraydi - ma'lumotdan foydalanish xatoga control flow dan kam moyil emas. O'zgaruvchi uch holatda bo'ladi: **defined** (qiymat berilgan, hali ishlatilmagan), **used** (hisobda yoki argument sifatida ishlatilgan), **killed** (aniqlangandan keyin qaytib aniqlanmagan holatga o'tgan, masalan yopilgan resursga ishora). Kitob avval anomal ketma-ketliklarni testdan oldin qidirishni talab qiladi: defined-defined, defined-exited, defined-killed, entered-killed, entered-used, killed-killed, killed-used va used-defined. Keyin asosiy qoida keladi: barcha mumkin bo'lgan **defined-used** yo'llarini bajarish. Kitob ikki darajani ajratadi: "barcha definition" darajasi zaif, chunki har qatorni bajarishga urinsangiz uni bepul olasiz; kuchli daraja esa har bir "bir joyda aniqlash + boshqa joyda ishlatish" juftligini sinaydi (o'sha joy, 22.3 (509-512-bet)).

Ikkisining farqi eng oddiy misolda ko'rinadi: ikkita ketma-ket `if` bo'lsa, structured basis ikki test bilan qanoatlanadi (ikkisi ham `true`, ikkisi ham `false`), lekin `x` ni birinchi shoxda aniqlab ikkinchi shoxda ishlatish juftliklari qoplanmay qoladi, shuning uchun to'rt test kerak bo'ladi. Shu sababli kitobning tavsiyasi ketma-ket: structured basis bilan boshlanadi, keyin yetishmagan defined-used holatlari qo'shiladi.

**Qo'lda tekshirishni osonlashtiradigan ma'lumot tanlash.** Uchinchi, kichik lekin amalda ko'p vaqt tejaydigan qoida: nominal qiymatni "barmoq tushgan raqam" bilan emas, qo'lda hisoblash oson bo'ladigan ko'rinishda tanlang. Kitobning misoli: 90 783.82 kabi qiymatda kutilgan natijani qo'lda hisoblaganda xato qilish ehtimoli koddagi xatoni topish ehtimoli bilan teng bo'lib qoladi, 20 000 esa hisobni yengillashtiradi. Muhimi: xunuk raqam o'z ekvivalentlik sinfidagi boshqa raqamdan ko'proq xato ochmaydi (o'sha joy, 22.3 (516-bet)). Ekvivalentlik sinflari va chegara qiymatlari texnikasining o'zi [test dizayn texnikalari](04-testrovshik-qanday-ishlashi-kerak-qa-ish.md#43-test-dizayn-texnikalari) bo'limida.

**Uchinchi o'q: ierarxiya.** Yuqoridagi ikki usul bitta metodning tuzilishi bo'yicha hisoblaydi, lekin vorislik ishlatilgan kodda test case soni boshqa yo'nalishda ko'payadi. Fowler buni refactoring ning yon ta'siri sifatida ko'rsatadi: super sinf instansiyasida chaqirilgan amal endi voris sinf instansiyalarida ham chaqiriladi, shuning uchun har holat uchun alohida test kerak bo'ladi, va vorislik ishlatilgan kodda test qoplami yetishmasligi odatiy hol (Martin Fowler, *Refactoring: Improving the Design of Existing Code*, 1-nashr, Addison-Wesley, 1999, 13-bob, 319-bet). Amaliy hisob: structured basis bitta metod uchun N test bersa, uni K voris sinf meros qilib olsa, qoplam uchun N dan ko'proq, ya'ni har voris uchun o'zgargan shoxlar soni qo'shiladigan son kerak bo'ladi. JUnit 5 da shakli arzon: umumiy xulqni abstrakt test sinfiga yoki `@TestFactory` ga chiqarib, har voris uchun bir marta yurgizish. Shu yerda ham [variant va kombinatsiya](#514-test-case-sonini-kod-tuzilishidan-chiqarish-structured-basis-va-data-flow) qoidasi amal qiladi: har kombinatsiyani emas, o'zgargan xulqni sinash kerak.

## 5.15 Test double intizomi: real implementatsiya va fake

5.7 va 5.8 "nimani ishlatish" ni ko'rsatdi. Bu bo'lim tanlovni qaror apparatiga aylantiradi: real implementatsiyadan boshlanadi va fake ga tushadi; interaction tekshiruvi oxirgi variant va u 5.16 da.

- **Real implementatsiya uch shart bajarilsa tanlanadi:** tez, deterministik va bog'liqligi oddiy. Value object (`Money`, `Address`, `LocalDate`), kolleksiya va sof hisob-kitob sinflari uchun javob doim "real". Chegara holatda tartib bir yo'nalishda: **avval realini ishlat, sekinlashganda double ga o't**. "Sekin" ning mutlaq chegarasi yo'q: bitta test uchun qo'shilgan bir sekund besh test uchun maqbul, besh yuz test uchun emas.
- **Nondeterminizmning ikki asosiy manbasi** tashqi servis (tarmoq orqasidagi HTTP yoki broker, uning holatini test boshqarmaydi) va tizim soati. Ikkisi ham double bilan almashtiriladi, uchinchi yo'l esa hayot sikli testga tegishli hermetik nusxa ([Testcontainers asoslari](08-testcontainers-bilan-real-infratuzilmada.md#82-testcontainers-asoslari-docker-api-ustida-hayot-aylanishi)). Ko'p threadli real implementatsiya ham nondeterminizm xavfi, chunki chiqish thread tartibiga bog'lanib qolishi mumkin.
- **Bog'liqlik daraxtini testda qo'lda qurmang.** `new Foo(new A(new B(new C()), new D()), ..., new Z())` ko'rinishidagi setup konstruktor imzosi o'zgarganda butun test to'plamini sindiradi va aynan shu og'riq odamni `@Mock` ga haydaydi. To'g'ri yechim - production dagi obyekt qurish kodini ishlatish: factory metod yoki DI konteyner. Shunda qurish kodi double ni ham qabul qila oladigan darajada moslashuvchan bo'lishi kerak.
- **API egasi mock qilinmasligi kerak turni belgilaydi.** Error Prone ning `@DoNotMock` annotatsiyasi aynan shu uchun: "bu turni mock qilmang, yaxshiroq muqobili bor". Egasi uchun bu erkinlik masalasi: tur minglab testda mock qilingan bo'lsa, har mock API ning xatti-harakatini takrorlaydi va ularning ko'pi shartnomani buzadi (masalan hech qachon `null` qaytarmaydigan metod uchun `null` qaytaradi). Shunda implementatsiyani o'zgartirish avval minglab noto'g'ri testni tuzatishni talab qiladi.

```java
@DoNotMock("SimpleQuery.create() ishlatilsin, mock qilinmasin")
public interface Query {
    String queryValue();
}
```

- **Fake ni haqiqiy implementatsiyaning egasi yozadi.** Fake real xatti-harakatga mos bo'lishi kerak, ya'ni real o'zgarganda u ham yangilanadi: bu domen bilimi va doimiy qarashni talab qiladi, shuning uchun uni foydalanuvchi emas, egasi saqlaydi. Fake **ildiz API uchun** yoziladi: bazaning o'zi testda ishlatilmasa, fake bazaning API si uchun yoziladi, bazaga murojaat qiladigan har bir sinf uchun emas. Foydalanuvchisi bir-ikkita bo'lsa fake o'zini oqlamaydi; yuzlab bo'lsa, oqlaydi.
- **Fake yo'q bo'lsa avval egasidan so'rang.** Egasi fake tushunchasidan xabarsiz bo'lishi mumkin. Rad etilsa, API ga qilinadigan hamma chaqiruvni bitta sinf ichiga o'rab, shu sinfning fake ini yozish mumkin: amalda API ning faqat bir qismi kerak bo'ladi, shuning uchun bu butun API uchun fake yozishdan arzon.
- **Fake ning aniqligi (fidelity) API shartnomasiga qarab o'lchanadi, implementatsiyaga emas.** Bir xil kirishga real nima qaytarsa va holatni qanday o'zgartirsa, fake ham shuni qiladi: `save(id)` yangi ID da muvaffaqiyat, mavjud ID da xato bersa, fake ham shunday beradi. Kechikish, resurs sarfi va disk bilan ishlash aniqligi talab qilinmaydi (in-memory fake diskka yozmaydi va bu normal). Qo'llab-quvvatlanmagan yo'lda fake **tez yiqilishi** kerak: istisno tashlab, bu holatda o'zi mos emasligini aytadi. Latency va yuk testida fake ishlatilmaydi, chunki o'lchanayotgan narsa aynan fake da yo'q.
- **Fake ning o'z testi bor.** Testsiz fake boshida real xatti-harakatni beradi, keyin real rivojlanishi bilan jim ajralib ketadi. Yechim - **contract test**: testlar API ning public interfeysiga yoziladi va ham real implementatsiyada, ham fake da yurgiziladi. Real ustida yurgan nusxa sekinroq, lekin uni faqat fake egasi yurgizadi, shuning uchun bu narx foydalanuvchiga tushmaydi. JUnit 5 da bu `@TestFactory` yoki umumiy abstrakt test sinfi bilan yoziladi.

```java
abstract class OrderRepositoryContract {

    abstract OrderRepository repository();

    @Test
    void savingDuplicateNumberFails() {
        OrderRepository repo = repository();
        repo.save(pending("A-1", money("10.00")));

        assertThatThrownBy(() -> repo.save(pending("A-1", money("10.00"))))
                .isInstanceOf(DuplicateOrderException.class);
    }
}

class InMemoryOrderRepositoryTest extends OrderRepositoryContract {
    @Override OrderRepository repository() { return new InMemoryOrderRepository(); }
}

@DataJpaTest
class JpaOrderRepositoryTest extends OrderRepositoryContract {
    @Autowired private OrderRepository repository;
    @Override OrderRepository repository() { return repository; }
}
```

## 5.16 Interaction tekshiruvi va ortiqcha aniqlik

Oldingi bo'lim real implementatsiya va fake ni tanlash tartibini berdi. Interaction tekshiruvi esa shu tartibdagi oxirgi variant va u o'z qoidalariga ega.

- **Interaction tekshiruvi kattaroq zaxira test talab qiladi.** U faqat ikki holatda o'rinli: holatni tekshirishning yo'li yo'q (real ham, fake ham yo'q) yoki chaqiruv soni va tartibining o'zi talab (kesh bazaga murojaatni kamaytirishi kerak, shunda `verify(reader, atMostOnce()).select()` o'rinli). Ikki holatda ham interaction testi holat tekshiruvining o'rnini bosmaydi: unit testda `verify` bilan baza chaqiruvini tekshirgan bo'lsangiz, real bazada holatni tekshiradigan integratsion test qo'shiladi ([7-bob](07-integratsion-test-spring-boot-slice-testlari.md)).
- **Interaction tekshiruvi holat o'zgartiradigan funksiyalar uchun qilinadi.** `sendEmail()`, `saveRecord()`, `logAccess()` - tashqi dunyoda yon ta'siri bor, shuning uchun `verify` ma'noli. `getUser()`, `findResults()`, `readFile()` esa holatni o'zgartirmaydi: ularning qaytargan qiymati sinovdan o'tayotgan kod ishida ishlatiladi va natijada tekshiriladi, demak chaqiruvning o'zini tekshirish ortiqcha. Bir signal aniq: metod shu testda allaqachon `when(...)` bilan stub qilingan bo'lsa, uni yana `verify` qilish kerak emas.

**`verifyNoMoreInteractions`.** Google haddan tashqari aniq (over-specified) interaction tekshiruvidan ogohlantiradi: tekshiruv faqat shu xatti-harakatga tegishli funksiya va argumentlar bilan cheklanadi, qolgan argumentlar `any()` bilan ochiq qoldiriladi, har xatti-harakat esa o'z testiga ajratiladi. Aks holda test o'zi tekshirmayotgan xatti-harakat o'zgarganda sinadi.

Ajratuvchi shart - **"boshqa chaqiruv yo'q" shartnomaning bir qismimi yoki yo'qmi**:

- **Shartnoma bo'lsa o'rinli.** "To'lov bir martadan ko'p yuborilmaydi", "kesh urgan so'rov bazaga chiqmaydi" - bu yerda chaqiruv soni tekshirilayotgan xatti-harakatning o'zi. Shunda `verifyNoMoreInteractions` yoki aniqrog'i `verify(gateway, times(1))` va `verifyNoInteractions(repository)` testning maqsadi bo'ladi va nomi ham shuni aytadi (`doesNotChargeTwice`).
- **Umumiy himoya bo'lsa o'rinsiz.** Har testning oxiriga qo'yilgan `verifyNoMoreInteractions` implementatsiya tafsilotini qulflaydi: `gateway` ga yangi metrika chaqiruvi qo'shilsa, summa tekshirayotgan test ham qizil beradi.

Amaliy chegara: `verifyNoMoreInteractions` testning sarlavhasida nomlangan xatti-harakatning qismi bo'lmasa, uni yozmang. `STRICT_STUBS` allaqachon ishlatilmagan stub ni ushlaydi, ya'ni ortiqcha himoya qatlami kerak emas.

## 5.17 Arxitektor nazorat ro'yxati

- [ ] Unit test "unit"i sinf emas, xatti-harakat deb belgilangan; sociable uslub standart, solitary - faqat I/O chegarasida
- [ ] Butun unit to'plam lokal mashinada 60 sekunddan kam ishlaydi va hech bir test DB, tarmoq, fayl tizimi yoki Spring kontekstiga tegmaydi
- [ ] Barcha assertion'lar AssertJ orqali; takrorlanuvchi domen tekshiruvlari uchun custom assertion yoki `usingRecursiveComparison` ishlatiladi
- [ ] Mockito `STRICT_STUBS` rejimida; `LENIENT` va `@Spy` ishlatilishi istisno sifatida asoslanadi; value object, DTO va JDK sinflari mock qilinmaydi
- [ ] Repository, cache va event publisher uchun in-memory fake'lar mavjud va mock zanjirlari o'rniga ishlatiladi
- [ ] Vaqt `Clock` bean orqali, tasodif va UUID `Supplier` ortida inyeksiya qilinadi; kod bazasida `Thread.sleep` va `Instant.now()` to'g'ridan-to'g'ri chaqiruvi yo'q
- [ ] `@Disabled` testlar sabab va issue havolasi bilan; ularning soni CI'da kuzatiladi va nolga intiladi
- [ ] Domen va hisob-kitob paketlari uchun mutation score o'lchanadi (PIT) va coverage foizi yagona sifat mezoni sifatida ishlatilmaydi

## Manbalar

- Robert C. Martin, *Clean Code*, 9-bob ("F.I.R.S.T.") - tez, mustaqil, qaytariladigan, o'zini tasdiqlaydigan, o'z vaqtida
- Robert C. Martin, *Clean Code*, 9-bob ("Single Concept per Test") - bir testda bir tushuncha, assert soni minimallashtiriladi
- Robert C. Martin, *Clean Code*, 9-bob ("Keeping Tests Clean") - iflos test testsizlikdan yomonroq
- [JUnit 5.11, Writing Tests](https://raw.githubusercontent.com/junit-team/junit5/r5.11.0/documentation/src/docs/asciidoc/user-guide/writing-tests.adoc) - annotatsiyalar jadvali, test instance lifecycle, `@Nested` ning non-static sharti va `@BeforeAll` ning Java 16 dagi o'zgarishi, `@Timeout` ning sinf darajasida tarqalishi
- [Mockito, README](https://raw.githubusercontent.com/mockito/mockito/613ab039480c8dbf1fe0fe4c0c91022e81cd7b75/README.md) - Mockito 5 da default mock maker `mockito-inline` ga o'tgani va Java 11 talabi
- [AssertJ, README](https://raw.githubusercontent.com/assertj/assertj/fb834e1df5e12973b120b67eafb09938fdf14976/README.md) - fluent assertion modeli va modullar
- Titus Winters, Tom Manshreck, Hyrum Wright, *Software Engineering at Google*, O'Reilly, 2020, 13-bob ("How to Decide When to Use a Real Implementation", "@DoNotMock") - real implementatsiya tez, deterministik va oddiy bog'liqlikli bo'lsa tanlanishi, chegarada avval realdan boshlab sekinlashganda double ga o'tish, nondeterminizm manbalari, bog'liqlikni production factory yoki DI bilan qurish, `@DoNotMock` ning API egasi uchun ma'nosi. Bu nashrning nusxasida barqaror bet raqami yo'q, shuning uchun bob va bo'lim nomi ko'rsatilgan
- Titus Winters, Tom Manshreck, Hyrum Wright, *Software Engineering at Google*, O'Reilly, 2020, 13-bob ("When Should Fakes Be Written?", "The Fidelity of Fakes", "Fakes Should Be Tested", "What to Do If a Fake Is Not Available") - fake ni real implementatsiya egasi yozishi va ildiz API uchun yozilishi, aniqlikning API shartnomasiga qarab o'lchanishi, qo'llab-quvvatlanmagan yo'lda tez yiqilish, contract test ni real va fake ustida yurgizish. Bu nashrning nusxasida barqaror bet raqami yo'q, shuning uchun bob va bo'lim nomi ko'rsatilgan
- Titus Winters, Tom Manshreck, Hyrum Wright, *Software Engineering at Google*, O'Reilly, 2020, 13-bob ("When Is Interaction Testing Appropriate?", "Best Practices for Interaction Testing", "Avoid Overspecification") - interaction tekshiruvining ikki o'rinli holati va kattaroq qamrovli zaxira test zarurati, holat o'zgartiruvchi va o'zgartirmaydigan funksiya farqi, ortiqcha aniqlikdan qochish. Bu nashrning nusxasida barqaror bet raqami yo'q, shuning uchun bob va bo'lim nomi ko'rsatilgan
- Titus Winters, Tom Manshreck, Hyrum Wright, *Software Engineering at Google*, O'Reilly, 2020, 12-bob ("Test via Public APIs", "Name Tests After the Behavior Being Tested") - public API ning jamoadan tashqariga ochilgan API ma'nosi, yordamchi sinf va support kutubxona uchun uch qoida, test nomidagi "and" ikki xatti-harakat belgisi ekani. Bu nashrning nusxasida barqaror bet raqami yo'q, shuning uchun bob va bo'lim nomi ko'rsatilgan
- Titus Winters, Tom Manshreck, Hyrum Wright, *Software Engineering at Google*, O'Reilly, 2020, 11-bob ("Benefits of Testing Code") - bir vaqtda bitta xatti-harakatni tekshiradigan qisqa testning bajariladigan hujjat sifatida ishlashi va talab o'zgarganda eskirgani ko'rinishi. Bu nashrning nusxasida barqaror bet raqami yo'q, shuning uchun bob va bo'lim nomi ko'rsatilgan
- Dustin Boswell, Trevor Foucher, *The Art of Readable Code*, 1-nashr, O'Reilly, 2011 (copyright 2012), 14-bob (157-bet) - katta "smasher" kirishni test matniga literal qilib yozmaslik va uni kodda dasturiy ravishda qurish, test qiymatlarini eng sodda shaklga keltirish
- Steve McConnell, *Code Complete*, 2-nashr, Microsoft Press, 2004, 22.3 "Bag of Testing Tricks" (505-516-bet) - structured basis testing uchun minimal test case sonini hisoblash protsedurasi, data-flow testingdagi defined/used/killed holatlari va defined-used juftliklari, qo'lda hisoblashni osonlashtiradigan ma'lumot tanlash
- Martin Fowler, *Refactoring: Improving the Design of Existing Code*, 1-nashr, Addison-Wesley, 1999, 13-bob (319-bet) - vorislik ishlatilgan kodda test qoplami yetishmasligining odatiy bo'lishi: super sinf instansiyasida chaqirilgan amal voris sinf instansiyalarida ham chaqirilishi va har holat uchun alohida test kerak bo'lishi

---

[&larr; 4. Tester qanday ishlashi kerak: QA ish jarayoni](04-testrovshik-qanday-ishlashi-kerak-qa-ish.md) · [Mundarija](README.md) · [6. Unit test Spring loyihasida: kontekstsiz testlash &rarr;](06-unit-test-spring-loyihasida-kontekstsiz.md)
