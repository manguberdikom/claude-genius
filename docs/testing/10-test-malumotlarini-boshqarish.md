<!-- doc: testing | chapter: 10 | part:  -->

[Barcha hujjatlar](../../README.md) / [Testlash qo'llanmasi](README.md)

> Holat: AI yozgan, inson tekshirmagan.

# 10. Test ma'lumotlarini boshqarish (Managing Test Data)

<details>
<summary>Bu bobdagi 15 bo'lim</summary>

- [10.1 Test ma'lumoti nega alohida mavzu](#101-test-malumoti-nega-alohida-mavzu)
- [10.2 Fixture strategiyalari](#102-fixture-strategiyalari)
- [10.3 Test Data Builder pattern](#103-test-data-builder-pattern)
- [10.4 Object Mother pattern](#104-object-mother-pattern)
- [10.5 Creation Method va test helper sinflarini tashkil qilish](#105-creation-method-va-test-helper-sinflarini-tashkil-qilish)
- [10.6 Tasodifiy va generatsiya qilingan ma'lumot](#106-tasodifiy-va-generatsiya-qilingan-malumot)
- [10.7 Ma'lumotlar bazasidagi holatni boshqarish](#107-malumotlar-bazasidagi-holatni-boshqarish)
- [10.8 Testlar orasida izolyatsiya](#108-testlar-orasida-izolyatsiya)
- [10.9 Tartibga bog'liqlik va uni aniqlash](#109-tartibga-bogliqlik-va-uni-aniqlash)
- [10.10 Katta hajmli va ishonchli ma'lumot](#1010-katta-hajmli-va-ishonchli-malumot)
- [10.11 Vaqtga bog'liq ma'lumot](#1011-vaqtga-bogliq-malumot)
- [10.12 Fayl, rasm va tashqi resurs ma'lumotlari](#1012-fayl-rasm-va-tashqi-resurs-malumotlari)
- [10.13 QA uchun test ma'lumoti](#1013-qa-uchun-test-malumoti)
- [10.14 Anti-patternlar](#1014-anti-patternlar)
- [10.15 Arxitektor nazorat ro'yxati](#1015-arxitektor-nazorat-royxati)

</details>



Test ma'lumoti - testning eng kam qadrlanadigan, ammo eng ko'p muammo keltiradigan qismi. Amalda test suite'ning o'qilishi, barqarorligi va ishlash tezligi ko'p hollarda business logic'dan emas, balki ma'lumotni tayyorlash usulidan kelib chiqadi. Bu bobda fixture strategiyalari, Test Data Builder va Object Mother patternlari, ma'lumotlar bazasi holatini boshqarish, izolyatsiya usullari va test ma'lumoti bilan ishlashdagi tipik anti-patternlar ko'rib chiqiladi. Maqsad - arxitektor sifatida loyihada test ma'lumoti bo'yicha bitta ongli, hujjatlashtirilgan qaror qabul qilish va uni butun komanda bo'ylab bir xil qo'llash.

## 10.1 Test ma'lumoti nega alohida mavzu

Odatda testda uch qism bo'ladi: arrange, act, assert. Katta tizimlarda `act` bir qator, `assert` ikki-uch qator, `arrange` esa qirq qator bo'lib ketadi. Shu qirq qator testning ma'nosini yashiradi: o'quvchi `new Customer(...)` konstruktorining 12 argumenti orasidan qaysi biri aynan shu test uchun muhim ekanini topa olmaydi. Bu "Obscure Test" muammosi - test hujjat sifatida ishlamay qoladi.

Ikkinchi ta'sir - beqarorlik. Umumiy ma'lumotga tayangan testlar bir-birining holatini buzadi: test A yaratilgan mijozni test B o'chiradi, natijada parallel yoki boshqa tartibda ishga tushirilganda suite qizil bo'ladi. Bu sabab ko'pincha "flaky test" deb nomlanadi, lekin aslida bu izolyatsiya xatosi - deterministik va tuzatiladigan.

Uchinchi ta'sir - tezlik. 500 ta integration testning har biri 300 ms ma'lumot tayyorlashga ketsa, bu 2.5 daqiqa faqat `arrange` uchun. Ma'lumotni qanday yaratish (SQL insert, repository, HTTP API orqali) va qachon tozalash - CI quvurining umumiy vaqtiga to'g'ridan-to'g'ri ta'sir qiladi.

To'rtinchisi - ishonchlilik. Ma'lumot hayotiy bo'lmasa (bo'sh string'lar, `null` maydonlar, `BigDecimal.ZERO` narxlar), test o'tadi, production'da esa validatsiya yoki hisob-kitob buziladi. Shuning uchun default qiymatlar "valid va mazmunli" bo'lishi kerak.

## 10.2 Fixture strategiyalari

Fixture - test boshlanishidagi tizim holati. Gerard Meszaros klassifikatsiyasi bo'yicha to'rtta asosiy yondashuv bor.

**Fresh Fixture** - har test o'zining ma'lumotini noldan yaratadi va o'zi tozalaydi. Eng izolyatsiyalangan, eng sekin.

**Shared Fixture** - bir marta yaratilgan ma'lumot to'plamini barcha testlar baham ko'radi (`@BeforeAll`, bir marta to'ldirilgan baza). Tez, lekin testlar o'zaro bog'lanadi.

**Prebuilt Fixture** - ma'lumot test ishga tushishidan oldin tashqaridan tayyorlanadi (migration, dump, seed skript). Shared Fixture'ning maxsus holati.

**Immutable Shared Fixture** - baham ko'rilgan, lekin hech bir test o'zgartirmaydigan reference ma'lumot: valyuta kodlari, soliq stavkalari, mamlakatlar ro'yxati. Amalda eng foydali kelishuv.

| Strategiya | Tezlik | Izolyatsiya | Asosiy xavf | Qachon |
|---|---|---|---|---|
| Fresh Fixture | Past | Juda yuqori | CI vaqti o'sadi | Standart tanlov; business holatga tegadigan testlar |
| Shared Fixture | Yuqori | Past | Test interdependence, tartibga bog'liqlik | Faqat read-only scenario'lar |
| Prebuilt Fixture | Yuqori | O'rtacha | Dump eskiradi, kim o'zgartirgani noma'lum | Reference/lookup jadvallar |
| Immutable Shared | Yuqori | Yuqori (o'zgarmasa) | Kimdir yozib yuborsa jim buziladi | Valyuta, soliq, konfiguratsiya kataloglari |

Tavsiya: **o'zgaradigan (mutable) business ma'lumot uchun Fresh Fixture, o'zgarmaydigan reference ma'lumot uchun Immutable Shared Fixture (Flyway migration orqali)**. Shared mutable fixture'ni loyiha konvensiyasi darajasida taqiqlash kerak - bu eng ko'p yashirin nosozlik manbasi.

## 10.3 Test Data Builder pattern

Builder'ning maqsadi: testda **faqat shu test uchun ahamiyatli maydonni** ko'rsatish, qolganiga valid default berish.

```java
public final class CustomerTestBuilder {
    private String name = "Alisher Qodirov";
    private String email = "alisher@example.com";
    private CustomerTier tier = CustomerTier.STANDARD;
    private boolean blocked = false;

    public static CustomerTestBuilder aCustomer() {
        return new CustomerTestBuilder();
    }

    public CustomerTestBuilder vip() {
        this.tier = CustomerTier.VIP;
        return this;
    }

    public CustomerTestBuilder blocked() {
        this.blocked = true;
        return this;
    }
    public CustomerTestBuilder withEmail(String email) {
        this.email = email;
        return this;
    }

    public Customer build() {
        return new Customer(name, email, tier, blocked);
    }
}
```

Buyurtma builder'i boshqa builder'ni qabul qiladi - bu "nested builder" yondashuvi, obyekt grafigini qurishni soddalashtiradi.

```java
public final class OrderTestBuilder {
    private Customer customer = aCustomer().build();
    private final List<OrderLine> lines = new ArrayList<>();
    private OrderStatus status = OrderStatus.NEW;

    public static OrderTestBuilder anOrder() {
        return new OrderTestBuilder();
    }

    public OrderTestBuilder for_(CustomerTestBuilder c) {
        this.customer = c.build();
        return this;
    }
    public OrderTestBuilder withLine(String sku, int qty, String price) {
        lines.add(new OrderLine(sku, qty, new BigDecimal(price)));
        return this;
    }
    public OrderTestBuilder paid() {
        this.status = OrderStatus.PAID;
        return this;
    }
    public Order build() {
        if (lines.isEmpty()) {
            withLine("SKU-1", 1, "100.00");
        }
        return new Order(customer, List.copyOf(lines), status);
    }
}
```

Testda o'qilishi shunday bo'ladi:

```java
@Test
void vipMijozgaChegirmaQollanadi() {
    Order order = anOrder()
            .for_(aCustomer().vip())
            .withLine("SKU-9", 2, "250.00")
            .build();

    Money total = discountService.applyDiscount(order);

    assertThat(total).isEqualTo(Money.of("450.00"));
}
```

`vip()` - testning yagona muhim fakti, qolgani default. Buyurtmaning manzili, telefon raqami, yaratilgan sanasi testda ko'rinmaydi, lekin ular valid.

**Lombok `@Builder` bilan farqi.** Lombok builder - production obyektini qurish uchun mexanik vosita: barcha maydonga setter'ga o'xshash method generatsiya qiladi, lekin default qiymat bermaydi (`@Builder.Default` yozmasa `null` va `0` qoladi) va domen tilidagi `vip()`, `blocked()`, `paid()` kabi semantik methodlarni yarata olmaydi. Natijada test yana 12 ta `.field(...)` chaqiruviga aylanadi. Qo'lda yozilgan test builder'ning qiymati aynan default'larda va semantik shortcut'larda. Amaliy kelishuv: production sinfida Lombok `@Builder` qolsin, test tarafda esa uni o'rab turuvchi test builder bo'lsin - test builder `build()` ichida Lombok builder'ni chaqiradi. Shunda domen modeli o'zgarganda faqat bitta joy tuzatiladi.

## 10.4 Object Mother pattern

Object Mother - nomlangan tipik obyektlarni qaytaradigan static factory. Builder "qanday qurish"ni, Object Mother "qaysi tipik holat"ni ifodalaydi.

```java
public final class Customers {
    private Customers() {}

    public static Customer standard() {
        return aCustomer().build();
    }

    public static Customer vipCustomer() {
        return aCustomer().vip().withEmail("vip@example.com").build();
    }

    public static Customer blockedCustomer() {
        return aCustomer().blocked().build();
    }
}
```

Ikkisi raqobatchi emas: Object Mother ichida Builder ishlatiladi, test esa odatda Mother'dan boshlab, kerak bo'lsa Builder bilan nozik o'zgartirish kiritadi (`Customers.vipBuilder().withEmail(...)`).

Qachon qaysi biri: domenda **chindan ham nomlangan, takrorlanuvchi tipik holatlar** bo'lsa (VIP mijoz, bloklangan hisob, muddati o'tgan hujjat) - Object Mother o'qishni yaxshilaydi. Variatsiya o'qi ko'p va har test o'ziga xos kombinatsiya talab qilsa - faqat Builder. Object Mother'ning xavfi - o'sib ketishi: 60 ta method'li `Customers` sinfi hech kimga tushunarli bo'lmaydi va har biri kimdir tomonidan "ozgina" o'zgartirilib, boshqa 10 ta testni buzadi. Chegara: har Mother sinfida 5-10 ta mazmunli holat, qolgani Builder orqali.

## 10.5 Creation Method va test helper sinflarini tashkil qilish

Creation Method - test sinfi ichidagi `private Order paidOrderWithTwoLines()` kabi lokal yordamchi. Faqat bitta test sinfida ishlatilsa - shu yerda qolsin. Ikkinchi sinf kerak bo'lganda `src/test/java` ichidagi umumiy paketga ko'chiriladi.

Tavsiya etiladigan joylashuv: test builder va Mother sinflari **production paketining o'zida**, lekin `src/test/java` ostida turadi (`com.example.order.OrderTestBuilder`). Shunda package-private konstruktorlarga kirish imkoni saqlanadi va IDE'da model yonida turadi. Umumiy infratuzilma (baza tozalash, Testcontainers konfiguratsiyasi, custom assertion'lar) `com.example.test.support` kabi alohida paketda bo'ladi.

Modullar orasida test util'larni ulash uchun Maven'da test-jar:

```xml
<plugin>
  <groupId>org.apache.maven.plugins</groupId>
  <artifactId>maven-jar-plugin</artifactId>
  <executions>
    <execution>
      <goals><goal>test-jar</goal></goals>
    </execution>
  </executions>
</plugin>
```

Iste'molchi modul `<type>test-jar</type>` va `<scope>test</scope>` bilan bog'lanadi. Gradle'da shu maqsadda `java-test-fixtures` plugin ishlatiladi: `src/testFixtures/java` papkasi va `testFixtures(project(":order"))` dependency. Gradle varianti afzal - fixture kodi test kodidan ajratiladi va kompilyatsiya chegarasi aniq bo'ladi. Arxitektura nazorati: test fixture moduli production modulga bog'lanadi, teskarisi hech qachon.

## 10.6 Tasodifiy va generatsiya qilingan ma'lumot

Uch vosita amalda keng ishlatiladi:

- **Datafaker** (JavaFaker'ning faol davom etuvchisi) - realistik ism, manzil, email, IBAN, telefon generatsiyasi. JavaFaker arxivlangan, yangi loyihada Datafaker olinadi.
- **Instancio** - butun obyekt grafigini typed API bilan to'ldiradi, `set()`, `generate()`, `ignore()` orqali nozik boshqariladi, JUnit 5 extension'i va `@Seed` annotatsiyasi bor.
- **EasyRandom** (eski `random-beans`) - reflection orqali bean'ni tasodifiy to'ldiradi; hozir sust rivojlanadi, yangi loyihada Instancio afzal.

Foydasi: ahamiyatsiz maydonlarni yozishdan xalos qiladi va "faqat shu bitta maydon muhim" g'oyasini kuchaytiradi - qolgani shovqin sifatida random bo'ladi.

Xavfi: takrorlanmaydigan test. Random ism uzunligi 51 belgi chiqib, `varchar(50)` ustunini buzsa, test haftada bir qizil bo'ladi va qayta ishga tushirilganda yashil - bu suite'ga ishonchni yo'q qiladi.

Qoida: **seed qat'iy belgilanadi va log'ga chiqariladi**. Instancio'da:

```java
@ExtendWith(InstancioExtension.class)
class OrderMappingTest {

    @Seed(1234L)
    @Test
    void mapsAllFields() {
        Order order = Instancio.of(Order.class)
                .set(field(Order::getStatus), OrderStatus.PAID)
                .generate(field(OrderLine::getQuantity), gen -> gen.ints().range(1, 5))
                .ignore(field(Order::getId))
                .create();

        OrderDto dto = mapper.toDto(order);

        assertThat(dto.status()).isEqualTo("PAID");
        assertThat(dto.lines()).hasSameSizeAs(order.getLines());
    }
}
```

`InstancioExtension` test yiqilganda ishlatilgan seed'ni xato xabariga qo'shadi - shu seed'ni `@Seed` bilan qotirib, nosozlikni aynan takrorlash mumkin. Datafaker'da esa `new Faker(new Locale("uz"), new Random(42L))` ko'rinishida seed beriladi. Assertion'ni hech qachon random qiymatga emas, balki invariantga (uzunlik, diapazon, mapping tengligi) qurish kerak.

## 10.7 Ma'lumotlar bazasidagi holatni boshqarish

To'rtta usul va ularning o'rni:

**`@Sql` skriptlari** - Spring Test'ning deklarativ mexanizmi. Oddiy, tez, SQL'ni aniq ko'rsatadi. Lekin domen o'zgarganda jim eskiradi va kompilyator tekshirmaydi.

```java
@SpringBootTest
@Sql("/data/customers.sql")
@Sql(scripts = "/data/cleanup.sql", executionPhase = AFTER_TEST_METHOD)
class CustomerQueryTest {

    @Autowired CustomerRepository repository;

    @Test
    void vipMijozlarniTopadi() {
        assertThat(repository.findByTier(CustomerTier.VIP)).hasSize(2);
    }
}
```

**Flyway test migratsiyalari** - reference ma'lumot uchun eng barqaror yo'l. `src/test/resources/db/testdata` papkasi qo'shimcha location sifatida qo'shiladi:

```yaml
spring:
  flyway:
    locations: classpath:db/migration,classpath:db/testdata
```

Shu yerga `R__reference_data.sql` kabi repeatable migration joylanadi - valyutalar, soliq stavkalari, rollar. Bu Immutable Shared Fixture'ning amaliy ko'rinishi.

**Repository orqali yozish** - domen validatsiyasi va mapping ishlaydi, refactoring'ga chidamli, lekin sekinroq va JPA cascade/flush nozikliklariga sezgir. Business holat uchun asosiy tanlov.

**To'g'ridan-to'g'ri SQL insert** (`JdbcClient`, `JdbcTestUtils`) - domen orqali yaratish imkonsiz yoki juda qimmat bo'lgan holatlar uchun: legacy ustunlar, buzilgan ma'lumot scenario'lari, 10 000 qatorli performance fixture.

```sql
-- src/test/resources/data/customers.sql
INSERT INTO customers (id, name, email, tier, blocked, created_at) VALUES
  (1001, 'Nodira Yusupova', 'nodira@example.com', 'VIP',      false, '2026-01-10T09:00:00'),
  (1002, 'Sardor Alimov',   'sardor@example.com', 'VIP',      false, '2026-01-11T09:00:00'),
  (1003, 'Kamola Rashidova','kamola@example.com', 'STANDARD', true,  '2026-01-12T09:00:00');
```

Qoida: **sxema har doim Flyway orqali**, business ma'lumot repository yoki builder orqali, reference ma'lumot test migration orqali, maxsus holatlar `@Sql` orqali.

## 10.8 Testlar orasida izolyatsiya

| Usul | Tezlik | Ishonchlilik | Asosiy tuzoq |
|---|---|---|---|
| `@Transactional` test (rollback) | Juda tez | O'rtacha | Haqiqiy commit tekshirilmaydi; `@Async`, yangi thread, `REQUIRES_NEW` va MVC server portidagi so'rov bu tranzaksiyani ko'rmaydi |
| `TRUNCATE`/`DELETE` har testdan keyin | Tez | Yuqori | FK tartibi, sequence qiymatlari saqlanib qolishi |
| Har test uchun alohida schema | O'rtacha | Juda yuqori | Flyway'ni har schema'ga qayta yugurtirish narxi |
| Alohida tenant/prefiks (logik ajratish) | Juda tez | Yuqori | Kod multi-tenancy'ni qo'llab-quvvatlashi shart |
| Konteynerni qayta yaratish | Juda sekin | Maksimal | CI vaqti bir necha barobar oshadi |

`@Transactional` testning eng ko'p uchraydigan tuzog'i: `@SpringBootTest(webEnvironment = RANDOM_PORT)` bilan birga ishlatish. Server so'rovni boshqa thread'da, boshqa tranzaksiyada bajaradi - test yozgan ma'lumotni ko'rmaydi, test esa server yozganini rollback qila olmaydi. Bu holatda tranzaksion rollback'dan voz kechib, aniq tozalash kerak.

Amaliy default: **TRUNCATE strategiyasi**, bir marta yoziladigan umumiy extension bilan.

```java
public class DatabaseCleaner {

    private static final List<String> TABLES =
            List.of("order_lines", "orders", "customers");

    private final JdbcClient jdbc;

    public DatabaseCleaner(JdbcClient jdbc) {
        this.jdbc = jdbc;
    }

    public void clean() {
        jdbc.sql("SET session_replication_role = 'replica'").update();
        TABLES.forEach(t -> jdbc.sql("TRUNCATE TABLE " + t + " RESTART IDENTITY CASCADE").update());
        jdbc.sql("SET session_replication_role = 'origin'").update();
    }
}
```

Bu metod `@AfterEach` yoki `TestExecutionListener` ichidan chaqiriladi. `RESTART IDENTITY` sequence'larni qaytaradi - shu bilan "ID 1 bo'ladi" degan yashirin taxminlar fosh bo'ladi (va shuning uchun ID'ga tayanmaslik kerak). Jadvallar ro'yxatini qo'lda emas, `information_schema.tables`'dan o'qib olish yanada barqaror.

Reference ma'lumot TRUNCATE ro'yxatiga **kirmasligi** kerak - aks holda har testdan keyin Flyway seed'ini qayta yuklashga majbur bo'lasiz.

## 10.9 Tartibga bog'liqlik va uni aniqlash

Test interdependence - test B faqat test A'dan keyin ishlaganda o'tishi. JUnit 5 sukut bo'yicha deterministik, lekin tasodifiy bo'lmagan tartibni ishlatadi; shu barqarorlik muammoni yashiradi.

Aniqlash uchun tartibni ataylab buzish kerak. `junit-platform.properties` faylida:

```properties
junit.jupiter.testmethod.order.default=org.junit.jupiter.api.MethodOrderer$Random
junit.jupiter.testclass.order.default=org.junit.jupiter.api.ClassOrderer$Random
junit.jupiter.execution.order.random.seed=424242
```

Seed log'ga chiqadi - qizil bo'lgan tartibni aynan takrorlash mumkin. Bir sinf uchun esa `@TestMethodOrder(MethodOrderer.Random.class)` yoziladi. Agar test chindan ham tartibga muhtoj bo'lsa (`@TestMethodOrder(OrderAnnotation.class)` + `@Order`), bu odatda scenario testi - uni bitta `@Test` ichida yoki `@TestFactory` bilan ifodalash to'g'riroq.

Ikkinchi diagnostika usuli - bitta testni yakka ishga tushirish: `mvn test -Dtest=OrderServiceTest#vipChegirma` yoki `gradle test --tests "...vipChegirma"`. Yakka holda yiqilsa - test boshqa testning qoldirgan ma'lumotiga tayangan. Yakka holda o'tib, suite'da yiqilsa - kimdir uning ma'lumotini buzadi. CI'da nightly job sifatida random order bilan to'liq suite'ni ishga tushirish - arzon va juda samarali nazorat.

## 10.10 Katta hajmli va ishonchli ma'lumot

Ba'zi testlar (performance, hisobot, migratsiya tekshiruvi) realistik hajm va taqsimot talab qiladi. Production dump'ini to'g'ridan-to'g'ri olib kelish - eng oson va eng xatarli yo'l.

Huquqiy tomon: GDPR shaxsiy ma'lumotni test muhitida ishlatishni "maqsadga muvofiqlik" va "minimallashtirish" talablari bilan cheklaydi; O'zbekiston "Shaxsga doir ma'lumotlar to'g'risida"gi qonuni esa fuqarolar ma'lumotini mamlakat hududidagi texnik vositalarda saqlashni va qayta ishlashga rozilikni talab qiladi. Developer laptopidagi production dump - bu ikkisining ham buzilishi.

Amaliy yondashuvlar:

- **Anonimlashtirish/maskalash** - dump chiqarilayotganda ism, telefon, PINFL, karta raqami deterministik hash yoki fake qiymatga almashtiriladi. Deterministik bo'lishi muhim: bir xil kirish bir xil chiqishni bersa, JOIN'lar va analitika ishlaydi.
- **Sintetik generatsiya** - Datafaker + taqsimot modeli bilan noldan yaratish. Huquqiy risk nol, lekin real "iflos" holatlarni (bo'sh maydonlar, eski formatlar) qamrab olmaydi.
- **Subset** - referensial butunlikni saqlab, 1-5% nusxa olish. Hajm kichik, FK butun, CI'da ko'tarish mumkin.

Tavsiya: subset + deterministik maskalash quvuri avtomatlashtiriladi va u faqat himoyalangan muhitda ishlaydi; natija artifact sifatida versiyalanadi, repository'ga emas, object storage'ga joylanadi.

## 10.11 Vaqtga bog'liq ma'lumot

"Bugun" ga bog'langan test - kechiktirilgan nosozlik. `LocalDate.now()` ishlatgan kod oyning 31-kunida, yil oxirida yoki kun o'zgarishida boshqacha natija beradi.

Yechim: vaqtni dependency sifatida `java.time.Clock` orqali kiritish.

```java
@Service
public class InvoiceService {

    private final Clock clock;

    public InvoiceService(Clock clock) {
        this.clock = clock;
    }

    public boolean isOverdue(Invoice invoice) {
        return invoice.dueDate().isBefore(LocalDate.now(clock));
    }
}

class InvoiceServiceTest {

    private final Clock fixed = Clock.fixed(
            Instant.parse("2026-03-31T23:59:00Z"), ZoneId.of("Asia/Tashkent"));

    @Test
    void oyOxiridaMuddatiOtgan() {
        InvoiceService service = new InvoiceService(fixed);
        Invoice invoice = anInvoice().dueDate(LocalDate.of(2026, 3, 30)).build();

        assertThat(service.isOverdue(invoice)).isTrue();
    }
}
```

Production konfiguratsiyasida `@Bean Clock clock() { return Clock.systemDefaultZone(); }`. Moliyaviy tizimlarda alohida tekshirilishi shart holatlar: oy/chorak/yil oxiri, kun oxiri (end of day) kesimi, timezone chegarasidan o'tish (Tashkent UTC+5, DST yo'q, lekin UTC'da saqlangan `Instant` mahalliy kunni siljitadi), kabisa yili 29-fevral. Fixture'da sanalarni `LocalDate.now().minusDays(5)` emas, aniq literal bilan berish kerak - shunda test bir yildan keyin ham xuddi shu narsani tekshiradi.

## 10.12 Fayl, rasm va tashqi resurs ma'lumotlari

Test fayllari `src/test/resources` ostida, mazmunli papkalarda turadi (`fixtures/xml`, `fixtures/json`, `fixtures/csv`). Ularni o'qishda absolute path emas, classpath resource ishlatiladi:

```java
class StatementParserTest {

    @Test
    void mt940FayliniOqiydi() throws Exception {
        ClassPathResource resource = new ClassPathResource("fixtures/mt940/sample.sta");
        String content;
        try (InputStream in = resource.getInputStream()) {
            content = new String(in.readAllBytes(), StandardCharsets.UTF_8);
        }

        Statement statement = parser.parse(content);

        assertThat(statement.transactions()).hasSize(3);
        assertThat(statement.closingBalance()).isEqualTo(new BigDecimal("1250.75"));
    }
}
```

Katta fayllarni (bir necha MB'dan oshadigan PDF, rasm, dump) repository'ga qo'ymaslik kerak - git tarixi shishadi va har clone sekinlashadi. Variantlar: hajmni qisqartirilgan namuna, generatsiya qilib yaratish (`new byte[5_000_000]` bilan sintetik fayl), yoki tashqi artifact repository'dan CI vaqtida yuklab olish. Rasm va PDF solishtirishda bayt-bayt tenglikni emas, mazmunni (o'lcham, sahifa soni, ajratilgan matn) tekshirish kerak - kutubxona versiyasi o'zgarishi baytni o'zgartiradi.

## 10.13 QA uchun test ma'lumoti

Manual va E2E testlar uchun test muhitida barqaror hisob va ma'lumot to'plamlari bo'lishi kerak: `qa-vip@example.com`, `qa-blocked@example.com`, bo'sh savatli hisob, to'lanmagan buyurtmasi bor hisob. Ular hujjatlashtiriladi va kodda emas, muhit seed'ida yashaydi.

Eng muhim talab - **tiklanish (reset) imkoni**. Test muhitida faqat test profilida yoqiladigan endpoint yoki CLI buyruq bo'lishi kerak:

```java
@RestController
@RequestMapping("/internal/test-data")
@Profile("qa")
class TestDataResetController {

    private final TestDataSeeder seeder;

    TestDataResetController(TestDataSeeder seeder) {
        this.seeder = seeder;
    }

    @PostMapping("/reset")
    ResponseEntity<Void> reset() {
        seeder.resetToBaseline();
        return ResponseEntity.noContent().build();
    }
}
```

`@Profile("qa")` bu endpoint production'da registratsiya qilinmasligini kafolatlaydi; qo'shimcha himoya sifatida uni authentication ortiga qo'yish va faqat ichki tarmoqdan ochish kerak.

Ma'lumotni bazada qo'lda SQL bilan tuzatish - zararli amaliyot: hech kim nima o'zgarganini bilmaydi, bir hafta o'tib QA muhiti hech bir kodga mos kelmaydigan holatga tushadi va "bizda ishlaydi" janriga olib keladi. Har qanday tuzatish seed skriptiga yozilib, reset orqali qayta qo'llanishi kerak.

## 10.14 Anti-patternlar

- **Umumiy yozuvga tayanish** - bir nechta test bitta mijoz yoki buyurtmani baham ko'rishi. Natija: tartibga bog'liqlik, parallel ishlashning imkonsizligi, sabablari tushunarsiz nosozliklar.
- **Hardcoded ID** - `assertThat(order.getId()).isEqualTo(1L)` yoki `@Sql`dagi `id = 1001`'ga tayanish. Sequence o'zgarsa yoki testlar tartibi almashsa darhol buziladi. Yaratilgan obyekt qaytargan ID'dan foydalanish kerak.
- **Production ma'lumotini to'g'ridan-to'g'ri ishlatish** - huquqiy risk va ma'lumot utkazishi.
- **Katta SQL dump fayllari** - repository'da yotgan 50 MB `testdata.sql`: sekin, o'qilmaydi, review qilinmaydi, sxema o'zgarganda jim eskiradi.
- **Har testda butun bazani tozalash va qayta migratsiya** - "xavfsiz" ko'rinadi, lekin suite vaqtini o'nlab barobar oshiradi va natijada komanda testlarni lokal ishga tushirishni to'xtatadi.
- **Default'lar o'rniga `null`/bo'sh qiymatlar** - builder `email = null` bersa, testlar o'tadi, production validatsiyasi buziladi.
- **Fixture'da business logikasi** - `if (customer.isVip()) total = ...` kabi hisob fixture ichida takrorlanishi: test o'zi tekshirayotgan logikani qayta yozib, nosozlikni yashiradi.

## 10.15 Arxitektor nazorat ro'yxati

- [ ] Loyihada fixture strategiyasi hujjatlashtirilgan: mutable business ma'lumot uchun Fresh Fixture, reference ma'lumot uchun Flyway test migration orqali Immutable Shared Fixture.
- [ ] Har bir asosiy aggregate uchun Test Data Builder mavjud va default qiymatlar valid; tipik holatlar Object Mother bilan nomlangan.
- [ ] Test fixture kodi `java-test-fixtures` yoki Maven test-jar orqali modullar orasida ulangan; fixture modul production'ga bog'liq, teskarisi yo'q.
- [ ] Izolyatsiya usuli bitta va aniq tanlangan (TRUNCATE yoki schema-per-test); `@Transactional` test `webEnvironment = RANDOM_PORT` bilan birga ishlatilmaydi.
- [ ] Random ma'lumot ishlatilsa, seed qat'iy belgilangan yoki xato xabariga chiqariladi; assertion'lar random qiymatga emas, invariantga qurilgan.
- [ ] CI'da random test order bilan ishlaydigan nightly job bor va tartibga bog'liq testlar aniqlanadi.
- [ ] Vaqtga bog'liq kod `Clock` bean orqali ishlaydi; oy/yil oxiri va kun oxiri holatlari uchun fixed Clock testlari mavjud.
- [ ] Production ma'lumoti test muhitiga faqat subset + deterministik maskalash quvuri orqali o'tadi; QA muhitida `@Profile`-himoyalangan reset mexanizmi bor va qo'lda SQL tuzatish taqiqlangan.

---

[&larr; 9. Tashqi servislarni taqlid qilish va contract testing](09-tashqi-servislarni-taqlid-qilish-va.md) · [Mundarija](README.md) · [11. Xavfsizlik, tranzaksiya, asinxron va konkurentlik testlari &rarr;](11-xavfsizlik-tranzaksiya-asinxron-va.md)
