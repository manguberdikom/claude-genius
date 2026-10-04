<!-- doc: sonarqube | chapter: 30 | part: VII. Xato katalogi: qanday kod qanday xato hisoblanadi -->

[SonarQube](../../README.md) / [SonarQube](README.md)

# 30. Xato katalogi: test kodidagi xatolar (Catalog: Test Code)

<details>
<summary>Bu bobdagi 15 bo'lim</summary>

- [30.1 Assertion siz test metodi](#301-assertion-siz-test-metodi)
- [30.2 Istisnoni try-catch bilan tekshirish va assertThrows ga o'tish](#302-istisnoni-try-catch-bilan-tekshirish-va-assertthrows-ga-otish)
- [30.3 Juda keng qamrovli assertThrows bloki](#303-juda-keng-qamrovli-assertthrows-bloki)
- [30.4 @Disabled qoldirilgan test va sababsiz o'chirish](#304-disabled-qoldirilgan-test-va-sababsiz-ochirish)
- [30.5 Thread.sleep bilan kutish va uni almashtirish](#305-threadsleep-bilan-kutish-va-uni-almashtirish)
- [30.6 Testlar orasida umumiy o'zgaruvchan holat](#306-testlar-orasida-umumiy-ozgaruvchan-holat)
- [30.7 Test metodining ma'nosiz nomi](#307-test-metodining-manosiz-nomi)
- [30.8 Testda magic number va tushunarsiz ma'lumot](#308-testda-magic-number-va-tushunarsiz-malumot)
- [30.9 Takrorlangan tayyorlash kodi va uni yagona joyga chiqarish](#309-takrorlangan-tayyorlash-kodi-va-uni-yagona-joyga-chiqarish)
- [30.10 Bir testda juda ko'p assertion va aralash maqsad](#3010-bir-testda-juda-kop-assertion-va-aralash-maqsad)
- [30.11 Test klassida test metodi yo'qligi](#3011-test-klassida-test-metodi-yoqligi)
- [30.12 Faqat qamrov uchun yozilgan, natijani tekshirmaydigan test](#3012-faqat-qamrov-uchun-yozilgan-natijani-tekshirmaydigan-test)
- [30.13 Oddiy yondashuv va arxitektor yondashuvi](#3013-oddiy-yondashuv-va-arxitektor-yondashuvi)
- [30.14 Tuzoq va yechim](#3014-tuzoq-va-yechim)
- [30.15 Amalda qo'llash](#3015-amalda-qollash)

</details>



Sonar test kodini ham production kod kabi tahlil qiladi, lekin boshqa qoida to'plamini qo'llaydi. Asosiy savol "bu metod ishlaydimi" emas, balki "bu test haqiqatan biror narsani tekshiradimi". Quyidagi katalog test kodida eng ko'p uchraydigan shikoyatlarni, toifasini va tuzatilgan variantini yig'adi. Jiddiylik "taxminan", chunki u quality profile sozlamasiga qarab o'zgaradi.

| Kod holati | Sonar nima deydi | Toifa | Jiddiylik (taxminan) | Ta'siri |
| --- | --- | --- | --- | --- |
| Test metodi assertion chaqirmaydi | `java:S2699`: test assertion o'z ichiga olishi kerak | maintainability (code smell) | Blocker | Test qizil bo'lmaydi, coverage o'sadi |
| `try { ... fail(); } catch (Ex e) {}` | eskirgan usul, `assertThrows` tavsiya qilinadi | maintainability (code smell) | Major | Noto'g'ri joyda tashlangan istisno ham testni o'tkazadi |
| `assertThrows` lambdasida bir nechta chaqiruv | `java:S5778`: faqat bitta metod chaqirig'i kutiladi | maintainability (code smell) | Major | Qaysi chaqiruv istisno tashlaganini bilib bo'lmaydi |
| `@Disabled` izohsiz qoldirilgan | `java:S1607`: tuzatilishi yoki olib tashlanishi kerak | maintainability (code smell) | Major | Yashirin regressiya, sababi esda qolmaydi |
| `Thread.sleep(2000)` test ichida | `java:S2925`: testda `Thread.sleep` ishlatilmasin | reliability (bug) | Critical | Flaky test va sekin CI |
| `static` o'zgaruvchan maydonga yozish | `java:S2696`: instance metod static maydonga yozmasin | reliability (bug) | Major | Testlar bajarilish tartibiga bog'lanadi |
| `void test1()` kabi nomlar | `java:S100`: metod nomi konventsiyaga mos bo'lsin | maintainability (code smell) | Minor | Buzilgan test nimani anglatishini hisobot ko'rsatmaydi |
| Kutilgan natija `BigDecimal("1187.5")` | `java:S109`: magic number izohlanmagan | maintainability (code smell) | Minor | Qoida o'zgarganda raqam manbasi noma'lum |
| Har testda takrorlangan setup | duplicated blocks, duplication density o'sadi | maintainability (code smell) | Major | Gate ning duplication sharti buziladi |
| Bitta testda 20 dan ortiq assertion | `java:S5961`: testda juda ko'p assertion | maintainability (code smell) | Major | Birinchi xato qolganini yashiradi |
| `...Test` klassida test metodi yo'q | `java:S2187`: test klassi test o'z ichiga olishi kerak | maintainability (code smell) | Blocker | Fayl test deb o'qiladi, hech narsa bajarilmaydi |
| `assertThat(total)` oxirigacha yozilmagan | `java:S2970`: assertion tugallanmagan | reliability (bug) | Blocker | Shart tekshirilmaydi, test doim yashil |
| `assertTrue(true)` yoki `assertNotNull(new Order())` | `java:S2701` va o'xshash qoidalar | maintainability (code smell) | Major | Soxta tekshiruv, aslida assertion yo'q |
| Faqat metodni chaqiradigan coverage testi | `java:S2699`, coverage ko'rsatkichi buziladi | maintainability (code smell) | Blocker | Coverage raqami haqiqatdan uzoqlashadi |

## 30.1 Assertion siz test metodi

Eng ko'p uchraydigan shikoyat shu: test servisni chaqiradi, natijani o'zgaruvchiga yozadi va tugaydi.

```java
@Test
void calculateTotal() {
    Order order = new Order(List.of(new Item("SKU-1", 2, new BigDecimal("500"))));
    // natija olinadi, lekin tekshirilmaydi
    BigDecimal total = paymentCalculator.calculateTotal(order);
    System.out.println(total); // konsolga chiqarish assertion emas
}
```

Sonar `java:S2699` bo'yicha shikoyat qiladi: metodda `@Test` izohi bor, lekin tanilgan assertion kutubxonalaridan birortasi ham chaqirilmagan. `System.out.println` assertion deb hisoblanmaydi. Bunday test faqat istisno tashlanganda qizil bo'ladi. JaCoCo esa o'sha qatorlarni qoplangan deb belgilaydi: coverage o'sadi, ishonch o'smaydi.

```java
@Test
void calculateTotal_qqs_bilan_yakuniy_summani_qaytaradi() {
    Order order = new Order(List.of(new Item("SKU-1", 2, new BigDecimal("500"))));

    BigDecimal total = paymentCalculator.calculateTotal(order);

    // 1000 asosiy summa, 12 foiz QQS qo'shiladi
    assertThat(total).isEqualByComparingTo("1120.00");
}
```

Tavsiya: har bir `@Test` metodi kamida bitta aniq assertion bilan tugashi kerak. Bunday shikoyatlar sonini tahlildan keyin filtr bilan sanash mumkin.

```bash
# faqat test fayllaridagi issue larni qoida bo'yicha guruhlab ko'rish
curl -s -u "$SONAR_TOKEN:" \
  "http://sonar.internal:9000/api/issues/search?componentKeys=payment-service&scopes=TEST&ps=100" \
  | jq -r '.issues[].rule' | sort | uniq -c | sort -rn
```

## 30.2 Istisnoni try-catch bilan tekshirish va assertThrows ga o'tish

JUnit 4 davrida keng tarqalgan usul JUnit 5 da code smell bo'lib qoldi.

```java
@Test
void insufficientStock() {
    try {
        inventoryService.reserve("SKU-1", 100); // omborda 3 dona bor
        fail("istisno kutilgan edi");
    } catch (InsufficientStockException e) {
        // bo'sh blok, xabar ham tekshirilmaydi
    }
}
```

Sonar bu yerda ikki narsadan shikoyat qiladi: bo'sh `catch` bloki va usulning o'zi. JUnit 5 da `assertThrows` bor, shuning uchun `try` va `fail` kombinatsiyasi keraksiz murakkablik hisoblanadi. Amaliy xavf ham bor: agar `reserve` noto'g'ri SKU formati uchun shu istisnoni tashlasa, test baribir yashil bo'ladi.

```java
@Test
void reserve_qoldiq_yetmaganda_istisno_tashlaydi() {
    // omborda faqat 3 dona bor, 100 dona so'raladi
    InsufficientStockException ex = assertThrows(
            InsufficientStockException.class,
            () -> inventoryService.reserve("SKU-1", 100));

    assertThat(ex.getMessage()).contains("SKU-1").contains("3");
    assertThat(inventoryService.available("SKU-1")).isEqualTo(3); // holat o'zgarmadi
}
```

Tavsiya: istisnoni `assertThrows` bilan tuting va qaytgan obyektning xabarini ham tekshirib, testni aniq sababga bog'lang.

## 30.3 Juda keng qamrovli assertThrows bloki

`assertThrows` ga o'tish yetarli emas, lambda ichiga nima yozilgani ham muhim.

```java
@Test
void orderFlowFails() {
    assertThrows(IllegalStateException.class, () -> {
        Order order = orderService.create("CUST-7");     // bu ham tashlashi mumkin
        orderService.pay(order.getId(), new BigDecimal("1120"));
        orderService.ship(order.getId());                // asl maqsad shu
    });
}
```

`java:S5778` aytadi: istisno kutilayotgan blokda bitta chaqiruv qolishi kerak. Yuqoridagi testda uchta chaqiruvdan qaysi biri istisno tashlagani ma'lum emas. Agar `create` validatsiya qo'shib `IllegalStateException` tashlasa, test yashil qoladi, ammo `ship` mantiqini tekshirmaydi.

```java
@Test
void ship_tolanmagan_buyurtmada_istisno_tashlaydi() {
    Order order = orderService.create("CUST-7");   // tayyorlash qismi lambdadan tashqarida

    IllegalStateException ex = assertThrows(
            IllegalStateException.class,
            () -> orderService.ship(order.getId()));  // faqat tekshirilayotgan chaqiruv

    assertThat(ex.getMessage()).contains("NEW");
    assertThat(orderService.find(order.getId()).getStatus()).isEqualTo(OrderStatus.NEW);
}
```

Tavsiya: tayyorlash qadamlarini lambdadan tashqariga chiqarib, blokda bitta chaqiruv qoldiring.

## 30.4 @Disabled qoldirilgan test va sababsiz o'chirish

O'chirilgan test vaqtinchalik qaror bo'lib tug'iladi va doimiy qarz bo'lib qoladi.

```java
@Test
@Disabled   // sabab yo'q, qachondan beri o'chiq ekani ham ma'lum emas
void refund_qismiy_qaytarishni_hisoblaydi() {
    assertThat(paymentCalculator.refund(order, new BigDecimal("300")))
            .isEqualByComparingTo("336.00");
}
```

`java:S1607` o'chirilgan testni ko'rsatadi va uni tuzatishni yoki olib tashlashni talab qiladi. Sonar uchun bu code smell: bajarilmaydigan, lekin saqlanayotgan mantiq bor. Amalda yomoni boshqa: o'sha test qoplagan qatorlar coverage dan chiqadi va new code coverage pasayadi.

```yaml
# CI da o'chirilgan testlar sonini kuzatish, ular sezdirmay ko'paymasligi uchun
- name: Disabled testlarni sanash
  run: |
    COUNT=$(grep -rcE "@Disabled|@Ignore" src/test/java | awk -F: '{s+=$2} END {print s+0}')
    echo "O'chirilgan testlar: $COUNT"
    # kelishilgan chegaradan oshsa, build ni to'xtatamiz
    if [ "$COUNT" -gt 5 ]; then
      echo "Chegaradan oshdi, avval mavjudlarini tuzatish kerak" >&2
      exit 1
    fi
```

Tavsiya: `@Disabled` ga sabab va ticket raqamini yozing, sonini CI da chegaralang va eskilarini sprint rejasiga qo'shing.

## 30.5 Thread.sleep bilan kutish va uni almashtirish

Asinxron kodni tekshirishda birinchi xayolga kelgan yechim eng yomoni.

```java
@Test
void tolov_tasdiqlangandan_keyin_buyurtma_PAID_bolishi_kerak() throws Exception {
    paymentGateway.confirmAsync("PAY-42");
    Thread.sleep(2000); // webhook kelishini kutamiz
    assertThat(orderService.find("ORD-42").getStatus()).isEqualTo(OrderStatus.PAID);
}
```

`java:S2925` testda `Thread.sleep` ni reliability muammosi deb belgilaydi. Sabab oddiy: kutish vaqti hech qachon to'g'ri bo'lmaydi. Sekin CI agentida 2 sekund yetmaydi va test flaky bo'ladi, tez mashinada vaqt behuda ketadi. Yechim shartni davriy tekshiradigan kutish, masalan Awaitility.

```java
@Test
void tolov_tasdiqlangandan_keyin_buyurtma_PAID_bolishi_kerak() {
    paymentGateway.confirmAsync("PAY-42");

    // shart bajarilishi bilan davom etadi, kutish vaqti faqat yuqori chegara
    await().atMost(Duration.ofSeconds(5))
           .pollInterval(Duration.ofMillis(100))
           .untilAsserted(() -> assertThat(orderService.find("ORD-42").getStatus())
                   .isEqualTo(OrderStatus.PAID));
}
```

Tavsiya: belgilangan vaqt kutish o'rniga shartni poll qiladigan kutishni ishlatib, timeout ni himoya chegarasi qilib qoldiring.

## 30.6 Testlar orasida umumiy o'zgaruvchan holat

Bu xato Sonar hisobotida ikki xil qoida ostida chiqadi.

```java
class InventoryServiceTest {
    // barcha testlar shu bitta ro'yxatni bo'lishadi
    private static final Map<String, Integer> STOCK = new HashMap<>();

    @Test
    void reserve_qoldiqni_kamaytiradi() {
        STOCK.put("SKU-1", 10);            // static maydonga yozish
        inventoryService.reserve("SKU-1", 4);
        assertThat(STOCK.get("SKU-1")).isEqualTo(6);
    }

    @Test
    void release_qoldiqni_qaytaradi() {
        // avvalgi testdan qolgan qiymatga ishonadi
        inventoryService.release("SKU-1", 2);
        assertThat(STOCK.get("SKU-1")).isEqualTo(8);
    }
}
```

Sonar instance metoddan static o'zgaruvchan maydonga yozishni `java:S2696` bo'yicha belgilaydi. Muammoning mohiyati test izolyatsiyasi: ikkinchi test birinchisining natijasiga tayanadi. JUnit 5 metod tartibini kafolatlamaydi, parallel bajarishda esa ikki test o'sha `Map` ni bir vaqtda o'zgartiradi. Natija kutilmagan qizil yoki undan yomoni kutilmagan yashil.

```java
class InventoryServiceTest {
    private Map<String, Integer> stock;   // static emas, har test uchun yangi

    @BeforeEach
    void setUp() {
        stock = new HashMap<>(Map.of("SKU-1", 10));
        inventoryService = new InventoryService(new InMemoryStockRepository(stock));
    }

    @Test
    void reserve_qoldiqni_kamaytiradi() {
        inventoryService.reserve("SKU-1", 4);
        assertThat(stock.get("SKU-1")).isEqualTo(6);
    }
}
```

Tavsiya: holatni `@BeforeEach` da noldan tiklang va o'zgaruvchan `static` maydonlarni test klassidan olib tashlang.

## 30.7 Test metodining ma'nosiz nomi

Nom testning hisobotdagi yuzi: buzilganda siz birinchi shu satrni ko'rasiz.

```java
@Test void test1() { /* ... */ }
@Test void testCalculate() { /* ... */ }
@Test void TolovTest_2() { /* ... */ }   // konventsiyaga ham mos emas
```

Uchinchi nom `java:S100` ni buzadi, chunki Java metod nomi kichik harf bilan boshlanadi. Birinchi ikkitasi qoida kalitiga tushmasligi mumkin, lekin review darajasida xuddi shunday xato: `test1` buzilganda hisobot hech narsa aytmaydi. Yaxshi nom uchta narsani bildiradi: nima, qanday sharoitda va qanday natija.

```java
@Test
void calculateTotal_chegirma_kodi_amal_qilmasa_toliq_summani_qaytaradi() { /* ... */ }

@Test
void reserve_qoldiq_nolga_teng_bolganda_istisno_tashlaydi() { /* ... */ }

@DisplayName("Buyurtma PAID holatidan CANCELLED ga o'tmaydi")
@Test
void cancel_tolangan_buyurtmani_bekor_qilmaydi() { /* ... */ }
```

Tavsiya: nomni "metod_shart_natija" shaklida yozing, murakkab holatni `@DisplayName` bilan to'ldiring.

## 30.8 Testda magic number va tushunarsiz ma'lumot

To'lov hisoblashda raqamlar ko'p va ularning kelib chiqishi tez yo'qoladi.

```java
@Test
void calculateTotal_hammasini_hisoblaydi() {
    Order order = new Order("ORD-1", 3, new BigDecimal("450.00"));
    order.applyDiscount(new BigDecimal("0.15"));
    // bu raqam qanday chiqdi, hech kim bilmaydi
    assertThat(paymentCalculator.calculateTotal(order))
            .isEqualByComparingTo(new BigDecimal("1285.20"));
}
```

`java:S109` izohlanmagan sonli konstantalarni belgilaydi va ko'p profilda bu qoida test fayllariga ham qo'llanadi. Asl muammo kengroq: `1285.20` qayerdan chiqqanini test tushuntirmaydi. QQS stavkasi o'zgarganda yangi developer raqamni qayta hisoblashni bilmaydi va testni shunchaki yangi natijaga moslashtiradi. Shu paytda test regressiyani ushlash qobiliyatini yo'qotadi.

```java
private static final BigDecimal BIRLIK_NARXI = new BigDecimal("450.00");
private static final int MIQDOR = 3;
private static final BigDecimal CHEGIRMA = new BigDecimal("0.15"); // 15 foiz aksiya
private static final BigDecimal QQS = new BigDecimal("0.12");

@Test
void calculateTotal_chegirma_va_qqs_ni_ketma_ket_qollaydi() {
    Order order = new Order("ORD-1", MIQDOR, BIRLIK_NARXI);
    order.applyDiscount(CHEGIRMA);

    BigDecimal kutilgan = BIRLIK_NARXI.multiply(BigDecimal.valueOf(MIQDOR))
            .multiply(BigDecimal.ONE.subtract(CHEGIRMA))
            .multiply(BigDecimal.ONE.add(QQS))
            .setScale(2, RoundingMode.HALF_UP);

    assertThat(paymentCalculator.calculateTotal(order)).isEqualByComparingTo(kutilgan);
}
```

Ehtiyot bo'ling: kutilgan natijani formula bilan hisoblash tekshirilayotgan mantiqni takrorlash xavfini tug'diradi. Murakkab qoidalar uchun qiymatni konstanta qilib, izohda manbasini ko'rsatish afzal.

Tavsiya: har bir raqamga nom bering, izohda biznes manbasini ko'rsating va formulani testda takrorlamang.

## 30.9 Takrorlangan tayyorlash kodi va uni yagona joyga chiqarish

Duplication alohida ko'rsatkich va test kodi uni tez buzadi.

```java
@Test
void tolov_muvaffaqiyatli() {
    Customer c = new Customer("CUST-7", "Toshkent", Tier.GOLD);
    Order o = new Order("ORD-1", c);
    o.addItem(new Item("SKU-1", 2, new BigDecimal("500")));
    o.addItem(new Item("SKU-2", 1, new BigDecimal("250")));
    o.setStatus(OrderStatus.NEW);
    // ... shu olti qator yana sakkiz testda aynan takrorlanadi
}
```

Sonar bir xil tuzilgan bloklarni duplicated blocks deb belgilaydi va `Duplicated Lines (%)` ni oshiradi. Agar gate da new code uchun duplication chegarasi bo'lsa, faqat test fayllari sababli build qizil bo'ladi. `"CUST-7"` kabi literal uch marta uchrasa `java:S1192` ham qo'shiladi.

```java
// test uchun yagona manba, faqat kerakli maydon o'zgartiriladi
final class OrderMother {
    static Order goldMijozBuyurtmasi() {
        Customer c = new Customer("CUST-7", "Toshkent", Tier.GOLD);
        Order o = new Order("ORD-1", c);
        o.addItem(new Item("SKU-1", 2, new BigDecimal("500")));
        o.addItem(new Item("SKU-2", 1, new BigDecimal("250")));
        return o;
    }
}

@Test
void calculateTotal_gold_mijozga_chegirma_qollaydi() {
    Order order = OrderMother.goldMijozBuyurtmasi();
    assertThat(paymentCalculator.calculateTotal(order)).isEqualByComparingTo("1260.00");
}
```

Integratsion testlarda shu rolni umumiy fixture fayli bajaradi.

```sql
-- src/test/resources/fixtures/ombor.sql, barcha integratsion testlar uchun yagona boshlang'ich holat
TRUNCATE TABLE stock_movement, stock_balance RESTART IDENTITY CASCADE;

INSERT INTO stock_balance (sku, warehouse, quantity) VALUES
  ('SKU-1', 'TOSHKENT-1', 10),   -- yetarli qoldiq holati
  ('SKU-2', 'TOSHKENT-1', 0),    -- qoldiq tugagan holat
  ('SKU-3', 'SAMARQAND-1', 3);   -- chegaraga yaqin holat

INSERT INTO orders (id, customer_id, status, total) VALUES
  ('ORD-1', 'CUST-7', 'NEW', 1260.00);
```

Tavsiya: takrorlangan tayyorlashni builder yoki fixture fayliga chiqarib, testda faqat o'ziga xos farqni qoldiring.

## 30.10 Bir testda juda ko'p assertion va aralash maqsad

Bitta test butun jarayonni qamrasa, buzilganda sabab noaniq bo'ladi.

```java
@Test
void buyurtma_jarayoni() {
    Order o = orderService.create("CUST-7");
    assertThat(o.getStatus()).isEqualTo(OrderStatus.NEW);
    assertThat(o.getItems()).isEmpty();
    orderService.addItem(o.getId(), "SKU-1", 2);
    assertThat(o.getItems()).hasSize(1);
    assertThat(paymentCalculator.calculateTotal(o)).isEqualByComparingTo("1120.00");
    orderService.pay(o.getId(), new BigDecimal("1120.00"));
    assertThat(orderService.find(o.getId()).getStatus()).isEqualTo(OrderStatus.PAID);
    // ... yana o'n beshta assertion, jo'natish va hisobot ham shu yerda
}
```

`java:S5961` bitta test metodidagi assertion sonini cheklaydi, chegara profilda sozlanadi. Amaliy sabab diagnostika: oltinchi assertion yiqilsa, qolgan o'n beshtasi bajarilmaydi. Bunday testning nomini ham to'g'ri yozib bo'lmaydi, chunki u bir vaqtda to'rtta narsani tekshiradi.

```java
@Test
void pay_buyurtmani_PAID_holatiga_otkazadi() {
    Order order = OrderMother.goldMijozBuyurtmasi();   // tayyor holat

    orderService.pay(order.getId(), new BigDecimal("1260.00"));

    Order saqlangan = orderService.find(order.getId());
    // bir obyektga tegishli tekshiruvlar bitta guruhda, hammasi baholanadi
    assertAll(
        () -> assertThat(saqlangan.getStatus()).isEqualTo(OrderStatus.PAID),
        () -> assertThat(saqlangan.getPaidAmount()).isEqualByComparingTo("1260.00"),
        () -> assertThat(saqlangan.getPaidAt()).isNotNull());
}
```

Tavsiya: bitta testda bitta xatti-harakatni tekshiring va bog'liq tekshiruvlarni `assertAll` bilan birlashtiring.

## 30.11 Test klassida test metodi yo'qligi

Bu shikoyat ko'pincha refaktoringdan keyin qoladi.

```java
// nomi Test bilan tugaydi, lekin bitta @Test metodi yo'q
class PaymentCalculatorTest {

    static Order buyurtma(String id, BigDecimal narx) {
        return new Order(id, 1, narx);
    }

    @BeforeEach
    void setUp() { /* ... */ }
}
```

`java:S2187` aytadi: test klassi deb nomlangan tur kamida bitta test o'z ichiga olishi kerak. Sonar buni Blocker darajasida ko'rsatadi, chunki fayl test sifatida o'qiladi, lekin hech narsa bajarilmaydi. Odatiy sabab: testlar ko'chirilgan, yordamchi metodlar qolib ketgan. Yechim uni `...Fixtures` yoki `...Mother` deb qayta nomlash.

```properties
# sonar-project.properties, qaysi fayl production, qaysi biri test ekani aniq ajratiladi
sonar.sources=src/main/java
sonar.tests=src/test/java

# test deb hisoblanadigan fayllar
sonar.test.inclusions=**/*Test.java,**/*Tests.java,**/*IT.java

# yordamchi fixture lar test emas, ular alohida qoida to'plamiga tushmasin
sonar.test.exclusions=**/*Fixtures.java,**/*Mother.java,**/TestSupport.java

# JaCoCo hisobotining yo'li, aks holda coverage nol ko'rinadi
sonar.coverage.jacoco.xmlReportPaths=target/site/jacoco/jacoco.xml
```

Tavsiya: yordamchi klass nomida `Test` so'zini qoldirmang va `sonar.test.inclusions` ni aniq belgilang.

## 30.12 Faqat qamrov uchun yozilgan, natijani tekshirmaydigan test

Katalogdagi eng xavfli holat, chunki u metrikani yaxshilab ko'rsatadi.

```java
@Test
void barcha_getterlarni_chaqiramiz() {
    Order o = new Order("ORD-1", new Customer("CUST-7", "Toshkent", Tier.GOLD));
    o.getId(); o.getCustomer(); o.getStatus(); o.getTotal();   // natija tekshirilmaydi
    assertNotNull(o);                                          // doim rost
    assertTrue(true);                                          // soxta assertion
}
```

Sonar bir nechta qoida bilan javob beradi: `assertTrue(true)` uchun `java:S2701`, yangi obyektni `assertNotNull` bilan tekshirish esa ma'nosiz assertion deb belgilanadi. Metrik tomondan bu test coverage ni ko'taradi va gate ni yashil qiladi. Shuning uchun coverage raqamiga yakka o'zida ishonib bo'lmaydi: u qaysi qatorlar bajarilganini o'lchaydi, tekshirilganini emas. Mutation testing bunday testni ochib beradi, Sonar faqat qisman ushlaydi.

```xml
<!-- getter va DTO larni qamrovdan chiqarish, soxta test yozishga sabab qolmasin -->
<properties>
  <sonar.coverage.exclusions>
    **/dto/**,
    **/config/**,
    **/*Application.java
  </sonar.coverage.exclusions>
  <!-- generatsiya qilingan kod umuman tahlilga kirmaydi -->
  <sonar.exclusions>**/generated/**</sonar.exclusions>
</properties>
```

Tavsiya: qamrov uchun soxta test yozish o'rniga mantiqsiz fayllarni `sonar.coverage.exclusions` bilan chiqarib, qolgan kodni haqiqiy assertion bilan qoplang.

## 30.13 Oddiy yondashuv va arxitektor yondashuvi

| Holat | Oddiy yondashuv | Arxitektor yondashuvi |
| --- | --- | --- |
| Test assertion siz chiqdi | `assertNotNull` qo'shib issue ni yopish | Maqsadni aniqlab, natija haqida aniq assertion yozish |
| Istisno tekshiruvi | `try` va `fail` ni qoldirish | `assertThrows` ga o'tish va istisno xabarini tekshirish |
| `@Disabled` test | Issue ni won't fix deb belgilash | Sabab va ticket yozib, sonini CI da chegaralash |
| Asinxron natijani kutish | `Thread.sleep` vaqtini oshirish | Shartni poll qiladigan kutish, timeout faqat chegara |
| Testlar bir-biriga xalal beradi | Metod tartibini `@Order` bilan majburlash | Holatni `@BeforeEach` da tiklash, static maydonni olib tashlash |
| Takrorlangan setup | Duplication qoidasini o'chirish | Builder va object mother bilan yagona manbaga chiqarish |
| Juda ko'p assertion | Qoida chegarasini oshirish | Testni holatlarga bo'lib, bog'liq tekshiruvlarni `assertAll` ga yig'ish |
| Coverage yetmaydi | Getter chaqiradigan test yozish | Haqiqiy mantiqni qoplash, mantiqsiz fayllarni chiqarish |

## 30.14 Tuzoq va yechim

| Tuzoq | Nega xavfli | Yechim |
| --- | --- | --- |
| `sonar.exclusions` ga `src/test/**` qo'shish | Test kodi sifati umuman o'lchanmaydi va flaky testlar ko'payadi | `sonar.test.inclusions` bilan to'g'ri ajratish, tahlilni saqlash |
| Assertion kutubxonasini Sonar tanimasligi | Assertion bor, lekin `java:S2699` baribir chiqadi | Standart kutubxonadan foydalanish yoki custom metodni qoidaga tanitish |
| `assertThrows` da `Exception.class` ni kutish | Har qanday xato testni o'tkazadi, hatto `NullPointerException` ham | Eng aniq istisno turini ko'rsatish |
| Faqat line coverage ga qarash | Shart tarmoqlari tekshirilmay qoladi | Branch coverage ni ham gate ga kiritish |
| Mock ni haddan ko'p ishlatish | Test faqat o'z mock ini tekshiradi | Integratsion sathni Testcontainers bilan qoplash, [testlash qo'llanmasidagi](../testing/README.md) Testcontainers mavzusida |
| Flaky testni `@Disabled` bilan yopish | Muammo yashiriladi va unutiladi | Sababni topish va kutishni shartga bog'lash, [testlash qo'llanmasidagi](../testing/README.md) flaky testlar mavzusi |

## 30.15 Amalda qo'llash

- [ ] Sonar hisobotini `scopes=TEST` filtri bilan oching va eng ko'p uchraydigan uchta qoidani aniqlang.
- [ ] `java:S2699` va `java:S2970` issue larini birinchi navbatda yoping, ular doim yashil testni bildiradi.
- [ ] `grep -rE "@Disabled|@Ignore" src/test/java` natijasidagi har bir testga sabab va ticket yozing yoki olib tashlang.
- [ ] `grep -rn "Thread.sleep" src/test/java` natijasidagi har bir joyni shartga asoslangan kutishga almashtiring.
- [ ] `try` va `fail` kombinatsiyasini `assertThrows` ga o'tkazib, lambdada bitta chaqiruv qoldiring.
- [ ] Eng ko'p takrorlanadigan test ma'lumotini object mother yoki fixture fayliga chiqaring.
- [ ] `sonar.tests`, `sonar.test.inclusions` va `sonar.test.exclusions` qiymatlarini aniq yozib, yordamchi klasslarni test to'plamidan chiqaring.
- [ ] Bitta modulda mutation testing ni ishga tushirib, coverage bilan haqiqiy tekshiruv orasidagi farqni ko'rsating.

---

[&larr; 29. Xato katalogi: Spring, JPA va PostgreSQL ga xos xatolar](29-xato-katalogi-spring-jpa-va-postgresql-ga.md) · [Mundarija](README.md) · [31. Xatolarga tushmaslik uchun yakuniy tavsiyalar &rarr;](31-xatolarga-tushmaslik-uchun-yakuniy.md)
