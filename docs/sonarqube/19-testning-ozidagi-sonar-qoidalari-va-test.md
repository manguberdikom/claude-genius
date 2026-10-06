<!-- doc: sonarqube | chapter: 19 | part: V. Sonar o'tadigan test -->

[Barcha hujjatlar](../../README.md) / [SonarQube](README.md)

> Holat: AI yozgan, inson tekshirmagan.

# 19. Testning o'zidagi Sonar qoidalari va test sifati (Sonar Rules on Test Code)

<details>
<summary>Bu bobdagi 12 bo'lim</summary>

- [19.1 Sonar test kodini ham tahlil qiladi: qaysi qoidalar unga tegishli](#191-sonar-test-kodini-ham-tahlil-qiladi-qaysi-qoidalar-unga-tegishli)
- [19.2 Assertion siz test va u nega buzilgan hisoblanadi](#192-assertion-siz-test-va-u-nega-buzilgan-hisoblanadi)
- [19.3 O'chirilgan yoki e'tiborsiz qoldirilgan test (`@Disabled`) va uning hisobi](#193-ochirilgan-yoki-etiborsiz-qoldirilgan-test-disabled-va-uning-hisobi)
- [19.4 Testda `Thread.sleep` va vaqtga bog'liqlik](#194-testda-threadsleep-va-vaqtga-bogliqlik)
- [19.5 Testda umumiy holat va testlar tartibiga bog'liqlik](#195-testda-umumiy-holat-va-testlar-tartibiga-bogliqlik)
- [19.6 Juda ko'p mock va haddan tashqari bog'langan test](#196-juda-kop-mock-va-haddan-tashqari-boglangan-test)
- [19.7 Test metodining nomi va uning hujjat sifatidagi roli](#197-test-metodining-nomi-va-uning-hujjat-sifatidagi-roli)
- [19.8 Test kodidagi takrorlanish: fixture va yordamchi metodlar](#198-test-kodidagi-takrorlanish-fixture-va-yordamchi-metodlar)
- [19.9 Testdagi magic number va tushunarsiz ma'lumot](#199-testdagi-magic-number-va-tushunarsiz-malumot)
- [19.10 Test fayllarini Sonar uchun to'g'ri belgilash (`sonar.tests`)](#1910-test-fayllarini-sonar-uchun-togri-belgilash-sonartests)
- [19.11 Test sifatini o'lchash: qamrov emas, nimani tekshirayotgani](#1911-test-sifatini-olchash-qamrov-emas-nimani-tekshirayotgani)
- [19.12 Amalda qo'llash](#1912-amalda-qollash)

</details>



Ko'p jamoa Sonar faqat `src/main/java` ni ko'radi deb o'ylaydi. Bu xato: Sonar test fayllarini ham skanerlaydi, ularda ham issue ochadi va bu issue'lar quality gate'ga tushadi. Lekin test kodiga asosiy koddan boshqa qoidalar to'plami ishlaydi, chunki har bir qoidaning "scope" xossasi bor. Bu bobda aynan shu mexanika va undan kelib chiqadigan test yozish usuli ko'rilgan.

## 19.1 Sonar test kodini ham tahlil qiladi: qaysi qoidalar unga tegishli

Sonar'dagi har bir qoidada `scope` degan xossa bor va uning uchta qiymati bo'ladi: Main sources, Test sources, yoki ikkisi birga. Rules UI'da yon paneldagi "Scope" filtri shuni ko'rsatadi. Shuning uchun "nega bu qoida testda ishlamadi" degan savolga javob ko'pincha quality gate'da emas, qoidaning scope'ida bo'ladi.

Amalda uchta guruh ajraladi. Birinchi guruh faqat test kodida ishlaydi: assertion yo'qligi, o'chirilgan test, `Thread.sleep`, assertion argumentlari tartibi. Ikkinchi guruh faqat asosiy kodda ishlaydi: magic number, production kodda `assert` kalit so'zi. Uchinchi guruh ikkala joyda ham ishlaydi: cognitive complexity, takrorlangan string literal, ishlatilmagan o'zgaruvchi, bo'sh `catch` bloki.

Natijada test fayli Sonar hisobotida ikki marta ko'rinadi. Birinchi marta coverage manbasi sifatida: test ishga tushganda qaysi asosiy qatorlar bajarilganini JaCoCo yozadi. Ikkinchi marta tahlil obyekti sifatida: test faylining o'zidagi code smell'lar Maintainability o'lchoviga qo'shiladi. Ikkinchisini e'tibordan qoldirgan jamoa "coverage 85%, lekin gate qizil" holatiga tushadi.

| Tuzoq | Nega yuz beradi | Yechim |
| --- | --- | --- |
| Test papkasi `sonar.sources` ichida | `sonar.tests` ko'rsatilmagan | `sonar.tests=src/test/java` ni aniq yoz |
| Testdagi issue gate'ni buzadi | New Code'dagi issue manba turini ajratmaydi | Qoidani profil darajasida test uchun o'chir, faylni emas |
| Coverage 0% ko'rinadi | JaCoCo report yo'li noto'g'ri | `sonar.coverage.jacoco.xmlReportPaths` ni tekshir |
| Test fayli coverage'ni "suyultiradi" | Test papkasi sources deb belgilangan | Papkalarni to'g'ri ajrat |
| Testda hardcoded parol issue beradi | `java:S2068` (vulnerability) `scope` i `Main`, ya'ni test papkasi sources deb sanalganda ishga tushadi | Avval `sonar.tests` ni to'g'rila; kerak bo'lsa aniq qoida uchun `issue.ignore`, izoh bilan |
| Testdagi smell abadiy qoladi | Hech kim test faylini refaktor qilmaydi | Test kodini ham Definition of Done'ga kirit |

## 19.2 Assertion siz test va u nega buzilgan hisoblanadi

`java:S2699` qoidasi test metodida hech qanday assertion yo'qligini topadi va bu Bug kategoriyasiga tushadi, ya'ni Reliability o'lchovini buzadi. Sonar buni shunday izohlaydi: assertion siz test faqat "exception tashlanmadi" degan faktni tekshiradi, lekin natijani tekshirmaydi. Bunday test yashil bo'lib turadi va coverage beradi, holbuki mantiq buzilgan bo'lsa ham sezmaydi.

Eng xavfli ko'rinish shundaki, assertion bor ko'rinadi, lekin yarim. AssertJ'da `assertThat(x)` yozilib, keyin hech qanday tekshiruv metodi chaqirilmasa, bu to'liqsiz assertion bo'ladi va `java:S2970` shunga reaksiya qiladi. Shuningdek `assertThrows` ichiga bir nechta chaqiruv solinsa, qaysi biri exception tashlaganini bilmaymiz va `java:S5778` shuni belgilaydi.

```java
// Sonar shikoyat qiladi: java:S2699 (assertion yo'q)
@Test
void shouldCreateOrder() {
    orderService.create(new OrderRequest("SKU-1", 2));
}

// Sonar shikoyat qiladi: java:S2970 (assertion to'liq emas)
@Test
void shouldReturnTotal() {
    assertThat(orderService.total(order)); // tekshiruv metodi yo'q
}

// Sonar o'tadigan variant: natija aniq tekshirilgan
@Test
void shouldCreateOrderWithReservedStock() {
    Order created = orderService.create(new OrderRequest("SKU-1", 2));

    assertThat(created.status()).isEqualTo(OrderStatus.RESERVED);
    assertThat(created.lines()).hasSize(1);
    assertThat(stockRepository.findBySku("SKU-1").reserved()).isEqualTo(2);
}
```

Agar test chindan ham faqat "xatolik bo'lmasligini" tekshirsa, buni ham assertion bilan ayt. `assertThatCode(() -> service.run()).doesNotThrowAnyException()` yozilgan test Sonar uchun to'g'ri, chunki niyat kodda ko'rinadi. Bo'sh metod esa niyatni yashiradi va shuning uchun bug deb hisoblanadi.

Yana bir nozik joy: JUnit 4'dan 5'ga o'tishda `assertEquals(expected, actual)` argumentlari almashtirilib yuborilsa, `java:S3415` ishga tushadi. Bu faqat estetika emas. Argumentlar teskari bo'lsa, test yiqilganda xabar chalg'itadi va debug vaqti ikki barobar oshadi.

## 19.3 O'chirilgan yoki e'tiborsiz qoldirilgan test (`@Disabled`) va uning hisobi

`java:S1607` qoidasi o'chirilgan testni topadi: JUnit 4'da `@Ignore`, JUnit 5'da `@Disabled`. Sonar uning sababini emas, mavjudligini belgilaydi. Mantiq oddiy: o'chirilgan test na himoya beradi, na coverage beradi, lekin "test bor" degan tasavvur qoldiradi.

Bu yerda halol gap kerak. Qoidani qondirishning ikki yo'li bor va faqat bittasi to'g'ri. Noto'g'ri yo'l: `@Disabled` ni olib tashlab, test tanasini bo'shatib qo'yish. Shunda `java:S1607` ketadi, lekin `java:S2699` keladi. To'g'ri yo'l: testni tuzatish yoki uni butunlay o'chirib, o'rniga issue tracker'da vazifa qoldirish.

```java
// Sonar shikoyat qiladi: java:S1607, sabab ham yozilmagan
@Disabled
@Test
void shouldRefundPaymentWhenOrderCancelled() { ... }

// Agar vaqtincha o'chirish zarur bo'lsa: sabab va muddat aniq
@Disabled("PAY-412: sandbox gateway 5xx qaytaradi, 2026-11-01 da qayta yoqiladi")
@Test
void shouldRefundPaymentWhenOrderCancelled() { ... }

// Eng yaxshisi: o'chirish emas, shartli ishga tushirish
@Test
@EnabledIfEnvironmentVariable(named = "PAYMENT_SANDBOX", matches = "true")
void shouldRefundPaymentWhenOrderCancelled() {
    PaymentResult result = paymentService.refund(order.id());

    assertThat(result.status()).isEqualTo(RefundStatus.ACCEPTED);
}
```

`@EnabledIf...` yondashuvi Sonar uchun `@Disabled` dan yaxshiroq, chunki test butunlay o'lgan emas: sharti bajarilgan muhitda ishlaydi. Shuningdek JUnit 5'ga o'tgan loyihalarda `java:S5786` muhim: test klassi yoki metodi noto'g'ri ko'rinish darajasiga ega bo'lsa, JUnit uni jim o'tkazib yuboradi. Bu "o'chirilgan test" ning eng yomon turi, chunki hech kim buni bilmaydi.

## 19.4 Testda `Thread.sleep` va vaqtga bog'liqlik

`java:S2925` qoidasi test kodida `Thread.sleep` ishlatilishini topadi. Sonar uning sababi sifatida flaky bo'lish xavfini ko'rsatadi: kutish vaqti CI mashinasining yuklamasiga bog'liq, shuning uchun lokalda o'tgan test build serverda yiqiladi. Qoida test scope'ida ishlaydi, ya'ni asosiy kodda `Thread.sleep` boshqa qoidalar ostida ko'riladi.

Yechim kutishni shartga bog'lashdir. Awaitility kutuvni "qancha vaqt" dan "nima bo'lishini" ga aylantiradi va `java:S2925` ni tabiiy yo'l bilan yopadi, chunki `Thread.sleep` umuman qolmaydi.

```java
// Sonar shikoyat qiladi: java:S2925
@Test
void shouldPublishOrderEvent() throws InterruptedException {
    orderService.create(request);
    Thread.sleep(2000); // CI da 2 sekund yetmasligi mumkin
    assertThat(eventStore.count()).isEqualTo(1);
}

// Sonar o'tadigan variant: shartga asoslangan kutish
@Test
void shouldPublishOrderEventWithinTimeout() {
    orderService.create(request);

    await().atMost(Duration.ofSeconds(5))
           .untilAsserted(() -> assertThat(eventStore.findByOrderId(request.id()))
                   .hasSize(1));
}
```

Vaqtga bog'liqlikning ikkinchi ko'rinishi `LocalDate.now()` ni test ichida chaqirishdir. Sonar bunga alohida qoida bilan reaksiya qilmasligi mumkin, lekin natija bir xil: oyning oxirgi kunida yoki yil almashganda test yiqiladi. To'g'ri yechim asosiy kodga `Clock` ni inject qilish va testda `Clock.fixed(...)` berish. Bu Sonar nuqtai nazaridan ham foydali, chunki `Clock` ni parametr qilish asosiy koddagi statik chaqiruvni kamaytiradi va testning cognitive complexity'sini pasaytiradi.

## 19.5 Testda umumiy holat va testlar tartibiga bog'liqlik

Sonar'da "testlar bir-biriga bog'liq" degan to'g'ridan to'g'ri qoida yo'q, lekin uning belgilarini topadigan qoidalar bor. Eng aniqi `java:S2386`: o'zgartirilishi mumkin bo'lgan `public static` maydon. Test klassida `static List<Order> created = new ArrayList<>()` yozilsa, bu bir testdan ikkinchisiga holat olib o'tadi va aynan shu qoida ishga tushadi.

Mexanika shunday: JUnit 5 sinf uchun yangi nusxa yaratadi, lekin `static` maydon umumiy qoladi. Shuning uchun `static` holat tartibga bog'liqlik keltiradi, Sonar esa buni "o'zgaruvchan umumiy holat" sifatida belgilaydi. Qo'shimcha signal `@TestMethodOrder` bilan tartibni qotirishdir: bu Sonar qoidasi emas, lekin review'da to'xtatish kerak bo'lgan naqsh.

```java
// Muammoli: static holat testlar orasida oqib ketadi (java:S2386)
class StockServiceTest {
    static Map<String, Integer> stock = new HashMap<>();

    @Test void shouldReserve() { stock.put("SKU-1", 5); ... }
    @Test void shouldRelease() { assertThat(stock).containsKey("SKU-1"); }
}

// Tozalangan: holat har testda qaytadan quriladi
class StockServiceTest {
    private StockService service;
    private InMemoryStockRepository repository;

    @BeforeEach
    void setUp() {
        repository = new InMemoryStockRepository();
        service = new StockService(repository);
    }

    @Test
    void shouldReserveRequestedQuantity() {
        repository.save(new Stock("SKU-1", 5));

        service.reserve("SKU-1", 2);

        assertThat(repository.findBySku("SKU-1").available()).isEqualTo(3);
    }
}
```

Spring kontekstidagi varianti ham bor: `@MockitoBean` yoki `@MockitoSpyBean` orqali sozlangan stub kontekst keshida qoladi va keyingi test klassiga o'tadi. Sonar bunga qoida bermaydi, lekin `@DirtiesContext` ning ko'payishi loyihada muammo borligini bildiradi. Bu holatda arxitektura darajasidagi qarorni [testlash qo'llanmasidagi](../testing/README.md) test izolyatsiyasi mavzusidan oling.

## 19.6 Juda ko'p mock va haddan tashqari bog'langan test

Sonar'da "mock soni ko'p" degan qoida yo'q. Buni ochiq aytish kerak, chunki ko'p maqolada aks fikr uchraydi. Lekin ortiqcha mock bilvosita o'lchanadi va aynan shu bilvosita o'lchov gate'ni buzadi.

Birinchi o'lchov `java:S3776`, cognitive complexity. Qoida test metodlariga ham tegishli, chunki uning scope'i ikkala manbani qamraydi. Yettita mock sozlangan test metodida shartlar, lambda'lar va `when(...)` zanjirlari yig'ilib, standart 15 limitidan oshadi. Ikkinchi o'lchov `java:S1448`, klassda metodlar soni juda ko'p. Uchinchisi `java:S107`, yordamchi metodda parametr juda ko'p: odatda bu "test ma'lumotini qurish uchun hamma narsani uzatamiz" degan naqshning natijasi.

```java
// Sonar shikoyat qiladi: java:S3776 (test metodining complexity'si yuqori)
@Test
void shouldProcessPayment() {
    when(customerRepo.findById(1L)).thenReturn(Optional.of(customer));
    when(cardValidator.validate(any())).thenReturn(true);
    when(fraudClient.score(any())).thenReturn(12);
    when(limitService.check(any(), any())).thenReturn(ALLOWED);
    when(gateway.charge(any())).thenAnswer(inv -> {
        ChargeRequest r = inv.getArgument(0);
        return r.amount().compareTo(LIMIT) > 0 ? DECLINED : APPROVED;
    });
    ...
}
```

Yechim mock sonini kamaytirish uchun asosiy kodni bo'lishdir. Agar `PaymentService` beshta hamkorga bog'langan bo'lsa, test ham beshta mock talab qiladi. Fraud tekshiruvi va limit tekshiruvini bitta `PaymentPolicy` ortiga yashirsangiz, test ikki mock bilan ishlaydi va `java:S3776` o'zidan ketadi. Ya'ni Sonar'ning test metodidagi shikoyati ko'pincha asosiy koddagi dizayn muammosining signali bo'ladi.

Ikkinchi yechim: `thenAnswer` ichidagi mantiqni fake obyektga ko'chirish. Fake klass alohida fayl bo'ladi, uning complexity'si o'z metodlari orasida taqsimlanadi va test metodi uch qatorga tushadi.

## 19.7 Test metodining nomi va uning hujjat sifatidagi roli

`java:S100` metod nomlash konvensiyasini tekshiradi va uning standart regex'i pastki chiziqga ruxsat bermaydi. Shuning uchun `given_validCard_when_charge_then_approved` uslubini tanlagan jamoa yuzlab issue oladi. Bu yerda ikki qarorning biri kerak, va ikkisi ham to'g'ri bo'lishi mumkin.

Birinchi qaror: nomlash uslubini camelCase'ga keltirish, masalan `shouldApproveChargeWhenCardIsValid`. Ikkinchi qaror: quality profile'da `java:S100` qoidasining `format` parametrini o'zgartirish, pastki chiziqli nomga ruxsat berish. Muhimi shuki, bu qoidani butunlay o'chirib tashlamang: u asosiy kodda ham ishlaydi va u yerda kerak. Parametrni o'zgartirish faylni exclude qilishdan ancha yaxshi.

Uchinchi tegishli qoida `java:S3577`: test klassi nomlash konvensiyasiga mos kelmasa. Bu qoida bilan birga `java:S2187` ishlaydi: nomi `...Test` bo'lgan, lekin ichida test metodi yo'q klass. Ikkisi birgalikda "fayl bor, test yo'q" holatini yopadi.

Nom Sonar uchun shuning uchun muhim: nomi `test1` bo'lgan metod yiqilganda CI log'da hech narsa aytmaydi. Nom aytib beradigan test esa yiqilish sababini o'qishdan oldin ko'rsatadi va bu flaky testlarni saralashda vaqt tejaydi.

## 19.8 Test kodidagi takrorlanish: fixture va yordamchi metodlar

Sonar takrorlanishni ikki xil o'lchaydi. Birinchisi `Duplicated Lines` metrikasi, ikkinchisi qoidalar: `java:S1192` takrorlangan string literal va `java:S4144` bir xil tanaga ega metodlar. Diqqat qiling: `Duplicated Lines` metrikasi ko'p sozlamalarda test fayllarida hisoblanmaydi, lekin `java:S1192` va `java:S4144` issue sifatida testda ham chiqadi. Loyihangizda aynan qanday ishlayotganini Measures sahifasidan tekshirib ko'ring, chunki bu versiya va sozlamaga qarab farq qiladi.

```java
// Sonar shikoyat qiladi: java:S1192 ("SKU-1" uch martadan ko'p takrorlangan)
@Test void t1() { service.reserve("SKU-1", 1); }
@Test void t2() { service.reserve("SKU-1", 2); }
@Test void t3() { service.release("SKU-1"); }

// Tozalangan: konstanta va builder
private static final String SKU = "SKU-1";

private static Order orderWith(int quantity) {
    return Order.builder().sku(SKU).quantity(quantity).build();
}
```

`java:S5976` alohida eslatishga arziydi: bir xil shaklda, faqat ma'lumoti farq qiladigan bir nechta test uchun parameterized test taklif qiladi. Uchta deyarli bir xil `@Test` metodini bitta `@ParameterizedTest` ga aylantirish ham bu qoidani yopadi, ham `java:S4144` xavfini kamaytiradi. Lekin ehtiyot bo'ling: hamma takrorlanish yomon emas. Test kodida ozgina takrorlanish o'qilishini oshirsa, abstraksiyadan ko'ra foydali bo'ladi va bu holatda issue'ni "won't fix" bilan yopish asosli qaror.

## 19.9 Testdagi magic number va tushunarsiz ma'lumot

`java:S109`, magic number qoidasi, ko'p profilda faqat asosiy kodda ishlaydi. Shuning uchun testda `assertThat(total).isEqualTo(237.50)` yozsangiz, Sonar jim turadi. Bu Sonar'ning testda sifat talab qilmasligini bildirmaydi, faqat bu aniq qoida test scope'iga kirmaydi.

Lekin bilvosita ta'sir bor. Tushunarsiz raqamlar testni uzaytiradi, yordamchi metodlar ko'payadi va oxirida `java:S3776` yoki `java:S1448` ishga tushadi. Shuning uchun magic number'ni testda ham nomlang, lekin sababini to'g'ri aytib: bu Sonar talabi emas, bu yiqilgan testni o'qiy olish talabi.

```java
// Tushunarsiz: 237.50 qayerdan keldi
@Test
void shouldCalculateInvoiceTotal() {
    assertThat(invoiceService.total(invoice)).isEqualByComparingTo("237.50");
}

// Tushunarli: hisob kodda ko'rinadi
private static final BigDecimal UNIT_PRICE = new BigDecimal("95.00");
private static final BigDecimal VAT_RATE = new BigDecimal("0.25");

@Test
void shouldAddVatToLineTotalForTwoUnits() {
    BigDecimal expected = UNIT_PRICE.multiply(BigDecimal.valueOf(2))
            .multiply(BigDecimal.ONE.add(VAT_RATE));

    assertThat(invoiceService.total(invoiceWith(2, UNIT_PRICE)))
            .isEqualByComparingTo(expected);
}
```

Testda hardcoded ma'lumotning yana bir turi Sonar'ni chindan ham qo'zg'atadi: `java:S2068`, kodga yozilgan parol. Test resource'laridagi `spring.datasource.password=test` qatori security hotspot sifatida chiqadi. Buni fayl bo'yicha exclude qilmang, aniq qoida va aniq yo'l bo'yicha `issue.ignore` yozib, sababini izohda qoldiring.

Mavzuning to'liq yozuvi [magic number](../patterns/25-anti-patternlar.md#258-sehrli-sonlar-va-satrlar-magic-numbers--strings) bo'limida; son va pul qiymatlari toza kod hujjatidagi [primitiv, son va pul](../clean-code/20-primitiv-son-va-pul.md) bobida ham bor; bu yerda faqat Sonar qoidasi nuqtai nazari.

## 19.10 Test fayllarini Sonar uchun to'g'ri belgilash (`sonar.tests`)

Bu bo'lim butun bobning asosi. Agar Sonar test fayllarini asosiy manba deb bilsa, hamma hisob buziladi: coverage pasayadi, chunki test fayllari o'zlari qoplanmagan qator sifatida hisoblanadi, test scope'idagi qoidalar esa umuman ishga tushmaydi. Maven va Gradle plugin'lari standart papka tuzilmasini o'zi aniqlaydi, lekin ko'p modulli yoki nostandart loyihada buni qo'lda yozish kerak.

```properties
# Asosiy va test manbalarini aniq ajratish
sonar.sources=src/main/java
sonar.tests=src/test/java,src/integrationTest/java

# JaCoCo XML hisobotining yo'li (agregat modul bo'lsa hammasini sanab o't)
sonar.coverage.jacoco.xmlReportPaths=target/site/jacoco/jacoco.xml

# Test kodini kompilyatsiya natijasi: semantik tahlil uchun zarur
sonar.java.test.binaries=target/test-classes
sonar.java.test.libraries=target/test-libs/*.jar

# Qaysi fayllar test deb sanaladi (nostandart joylashuvda)
sonar.test.inclusions=**/*Test.java,**/*IT.java,**/*Tests.java
```

`sonar.java.test.binaries` ni tashlab ketish keng tarqalgan xato. Bu sozlama bo'lmasa, Sonar test fayllarini faqat sintaktik darajada ko'radi va assertion bilan bog'liq qoidalarning ko'pi ishlamaydi, chunki ular tiplarni bilishni talab qiladi. Tahlil log'ida bu haqda ogohlantirish chiqadi va uni o'qish kerak.

Keyingi qadam: testdagi ayrim qoidalarni maqsadli o'chirish. Butun faylni exclude qilish eng yomon variant, chunki u bilan birga foydali qoidalar ham ketadi.

```properties
# Faqat test resource'laridagi parol hotspot'ini jim qildirish
sonar.issue.ignore.multicriteria=e1,e2
sonar.issue.ignore.multicriteria.e1.ruleKey=java:S2068
sonar.issue.ignore.multicriteria.e1.resourceKey=**/src/test/resources/**

# Fake va test double klasslarida nomlash qoidasini yumshatish
sonar.issue.ignore.multicriteria.e2.ruleKey=java:S3577
sonar.issue.ignore.multicriteria.e2.resourceKey=**/testsupport/**

# Coverage hisobidan generatsiya qilingan kodni chiqarish
sonar.coverage.exclusions=**/config/**,**/*Application.java,**/dto/**
```

## 19.11 Test sifatini o'lchash: qamrov emas, nimani tekshirayotgani

Oxirgi va eng muhim fikr: Sonar coverage raqamini ko'rsatadi, lekin test nimani tekshirayotganini bilmaydi. `java:S2699` faqat assertion mavjudligini ko'radi, uning kuchini ko'rmaydi. Shuning uchun `assertThat(result).isNotNull()` bilan tugaydigan yuzta test 90% coverage va yashil gate beradi, holbuki biror mantiq buzilsa hech biri sezmaydi.

Bu yerda halol bo'lish kerak: Sonar bu bo'shliqni yopa olmaydi. U sintaksis va bajarilgan qatorlarni biladi, niyatni bilmaydi. Shuning uchun quality gate'ni test sifatining o'lchovi deb emas, test sifatining minimal poli deb qarash kerak. Haqiqiy o'lchov uchun mutation testing yoki review kerak, va buni [testlash qo'llanmasidagi](../testing/README.md) test sifati metrikalari mavzusidan qarang.

| Masala | Oddiy yondashuv | Arxitektor yondashuvi |
| --- | --- | --- |
| Test kodidagi issue | "Bu test, muhim emas" | Test kodi ham gate'ga kiradi, DoD'ga kirit |
| `@Disabled` test | Sababsiz qo'shib qo'yiladi | Ticket raqami, muddat, yoki shartli yoqish |
| Kutish | `Thread.sleep(2000)` | Awaitility va `untilAsserted` |
| Vaqt | `LocalDate.now()` testda | Inject qilingan `Clock.fixed(...)` |
| Ko'p mock bilan test | Mock'ni ko'paytiradi | Asosiy kodni bo'lib mock'ni kamaytiradi |
| Qoida xalaqit berganda | Faylni butunlay exclude qiladi | Qoida parametrini yoki aniq `issue.ignore` ni sozlaydi |
| Test nomi | `test1`, `testOrder` | Xatti harakat va kutilgan natija nomda |
| Takrorlanish | Copy paste yoki ortiqcha abstraksiya | Builder, parameterized test, o'qilishi muhim joyda takror qoldiradi |
| Coverage 90% | "Sifat yetarli" | Assertion kuchini review va mutation bilan tekshiradi |
| Test konfiguratsiyasi | Standart holatga tayanadi | `sonar.tests` va `test.binaries` ni aniq yozadi |

## 19.12 Amalda qo'llash

- [ ] `sonar-project.properties` yoki `pom.xml` da `sonar.sources`, `sonar.tests` va `sonar.java.test.binaries` ni aniq yozib, tahlil log'ida test manbalari soni to'g'ri ko'rsatilganini tekshir.
- [ ] Sonar UI'da Issues bo'limini `Scope: Test sources` bo'yicha filtrlab, test kodidagi joriy issue sonini yozib qo'y: bu sizning boshlang'ich nuqtangiz.
- [ ] `java:S2699` va `java:S2970` bo'yicha chiqqan hamma issue'ni ko'rib chiq va har birini yo assertion qo'shish bilan, yo testni o'chirish bilan yop.
- [ ] Kod bazasida `Thread.sleep` ni test papkalarida qidirib, har birini Awaitility'ning `untilAsserted` chaqiruviga aylantir.
- [ ] Hamma `@Disabled` annotatsiyasiga sabab matni va ticket raqamini qo'sh, uch oydan oshganini esa butunlay o'chir.
- [ ] Quality profile'da `java:S100` qoidasining `format` parametrini jamoangiz nomlash uslubiga moslashtir, qoidani o'chirmay.
- [ ] Test klasslarida `static` o'zgaruvchan maydonlarni qidirib, holatni `@BeforeEach` ga ko'chir va `java:S2386` issue'larini yop.
- [ ] Cognitive complexity'si limitdan oshgan test metodlarini ro'yxatga ol va har biri uchun qaror yoz: fake'ga ko'chirish, yoki asosiy kodni bo'lish.

---

[&larr; 18. Branch va shart qamrovini to'liq yopish usullari](18-branch-va-shart-qamrovini-toliq-yopish.md) · [Mundarija](README.md) · [20. Mutation testing: 100% coverage qachon yolg'on &rarr;](20-mutation-testing-100-coverage-qachon-yolgon.md)
