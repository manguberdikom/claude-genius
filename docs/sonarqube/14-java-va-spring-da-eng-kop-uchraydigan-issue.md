<!-- doc: sonarqube | chapter: 14 | part: IV. Sonar o'tadigan kod -->

[SonarQube](../../README.md) / [SonarQube](README.md)

# 14. Java va Spring da eng ko'p uchraydigan issue va ularning yechimi (Common Java and Spring Issues)

<details>
<summary>Bu bobdagi 13 bo'lim</summary>

- [14.1 Maydon orqali bog'liqlik kiritish (`@Autowired` field injection) va konstruktor bilan almashtirish](#141-maydon-orqali-bogliqlik-kiritish-autowired-field-injection-va-konstruktor-bilan-almashtirish)
- [14.2 Katta controller metodi va uni servisga bo'lish](#142-katta-controller-metodi-va-uni-servisga-bolish)
- [14.3 Tekshirilmagan foydalanuvchi kiritmasi va validatsiya](#143-tekshirilmagan-foydalanuvchi-kiritmasi-va-validatsiya)
- [14.4 Qo'lda yozilgan SQL konkatenatsiyasi va parametrlangan so'rov](#144-qolda-yozilgan-sql-konkatenatsiyasi-va-parametrlangan-sorov)
- [14.5 `@Transactional` ni noto'g'ri joyga qo'yish bilan bog'liq ogohlantirishlar](#145-transactional-ni-notogri-joyga-qoyish-bilan-bogliq-ogohlantirishlar)
- [14.6 Sana va vaqt bilan ishlash: eskirgan API va `java.time`](#146-sana-va-vaqt-bilan-ishlash-eskirgan-api-va-javatime)
- [14.7 To'plamlarni qaytarish: modifikatsiya qilinadigan ichki to'plamni chiqarib yuborish](#147-toplamlarni-qaytarish-modifikatsiya-qilinadigan-ichki-toplamni-chiqarib-yuborish)
- [14.8 Strim va sikl ichida og'ir operatsiya](#148-strim-va-sikl-ichida-ogir-operatsiya)
- [14.9 Thread va `ExecutorService` bilan bog'liq ogohlantirishlar](#149-thread-va-executorservice-bilan-bogliq-ogohlantirishlar)
- [14.10 Eskirgan (deprecated) API ishlatish va migratsiya](#1410-eskirgan-deprecated-api-ishlatish-va-migratsiya)
- [14.11 Test kodidagi tez-tez uchraydigan issue lar](#1411-test-kodidagi-tez-tez-uchraydigan-issue-lar)
- [14.12 Issue larni toifa bo'yicha tartiblash va birinchi nimani tuzatish](#1412-issue-larni-toifa-boyicha-tartiblash-va-birinchi-nimani-tuzatish)
- [14.13 Amalda qo'llash](#1413-amalda-qollash)

</details>


Har bir Java loyihada Sonar topadigan issue larning aksariyati o'n chog'li naqshdan iborat. Ular yangi emas va qiyin ham emas, lekin takrorlanadi, chunki ularni kod yozish paytida ko'rmaslik oson. Quyida har bir naqsh uchun Sonar nimani o'lchaydi, nega shikoyat qiladi va qanday kod bilan u shikoyat qilmaydi ko'rsatilgan. Qoida kalitlari faqat ishonch komil bo'lgan joyda yozilgan, qolgan joyda qoidaning mazmuni tasvirlangan.

## 14.1 Maydon orqali bog'liqlik kiritish (`@Autowired` field injection) va konstruktor bilan almashtirish

Sonar `@Autowired` qo'yilgan maydonni maintainability issue sifatida belgilaydi. Spring uchun mos qoida kaliti `java:S6813`. Sababi texnik: maydon reflection orqali to'ldiriladi, demak obyekt konstruktor tugaganda hali to'liq emas. Shuning uchun maydon `final` bo'la olmaydi va klassni Spring context dan tashqarida test qilish uchun reflection yoki `@InjectMocks` kerak bo'ladi. Konstruktor injection da bog'liqlik majburiy bo'ladi va kompilyator uni tekshiradi. Yana bir foyda: konstruktor parametrlari soni o'sib ketsa, klass juda ko'p ish qilayotgani ko'rinadi. Bitta konstruktor bo'lsa Spring 4.3 dan beri `@Autowired` yozish shart emas.

```java
// Yomon: Sonar maydon orqali injection ni belgilaydi, maydon final bo'lmaydi
@Service
public class PaymentService {
    @Autowired private PaymentGateway gateway;
    @Autowired private OrderRepository orders;
    @Autowired private AuditLogger audit;
}

// Yaxshi: final maydon, bitta konstruktor, @Autowired shart emas
@Service
public class PaymentService {
    private final PaymentGateway gateway;
    private final OrderRepository orders;
    private final AuditLogger audit;

    public PaymentService(PaymentGateway gateway,
                          OrderRepository orders,
                          AuditLogger audit) {
        this.gateway = gateway;
        this.orders = orders;
        this.audit = audit;
    }
}
```

## 14.2 Katta controller metodi va uni servisga bo'lish

Controller ichida validatsiya, biznes qoida, baza bilan ishlash va javob yig'ish bir joyda bo'lsa, Sonar bir vaqtda bir necha qoidani ishga tushiradi. Eng muhimi cognitive complexity, kaliti `java:S3776`, standart chegara metod uchun 15. Yana `java:S138` metod qatorlari soni uchun va `java:S107` parametrlar soni uchun ishlaydi. Cognitive complexity har bir `if`, `for`, `catch` va ichki joylashuv uchun ball qo'shadi, shuning uchun ichma-ich shartlar jarimani tez oshiradi. Yechim kodni qisqartirish emas, balki mas'uliyatni ko'chirish. Controller HTTP ni biznesga tarjima qiladi va boshqa hech narsa qilmaydi. Shunda coverage ham osonlashadi: biznes qoidani servis testida yopasiz, controller uchun `@WebMvcTest` yetadi.

```java
// Yomon: controller ichida hamma narsa, cognitive complexity chegaradan oshadi
@PostMapping("/orders")
public ResponseEntity<?> create(@RequestBody Map<String, Object> body) {
    if (body.get("items") == null) return ResponseEntity.badRequest().build();
    List<?> items = (List<?>) body.get("items");
    if (items.isEmpty()) return ResponseEntity.badRequest().build();
    BigDecimal total = BigDecimal.ZERO;
    for (Object raw : items) {
        Map<?, ?> item = (Map<?, ?>) raw;
        Integer qty = (Integer) item.get("qty");
        if (qty == null || qty <= 0) return ResponseEntity.badRequest().build();
        Stock stock = stockRepo.findBySku((String) item.get("sku"));
        if (stock == null || stock.getQty() < qty) {
            return ResponseEntity.status(409).build();
        }
        total = total.add(stock.getPrice().multiply(BigDecimal.valueOf(qty)));
    }
    return ResponseEntity.ok(orderRepo.save(new Order(total)));
}

// Yaxshi: controller faqat tarjima qiladi
@PostMapping("/orders")
public ResponseEntity<OrderResponse> create(@Valid @RequestBody CreateOrderRequest req) {
    OrderResponse created = orderService.place(req);   // biznes qoida servisda
    return ResponseEntity.status(HttpStatus.CREATED).body(created);
}
```

## 14.3 Tekshirilmagan foydalanuvchi kiritmasi va validatsiya

Sonar tashqaridan kelgan ma'lumotni "tainted" deb kuzatadi va u xavfli joyga (SQL, fayl yo'li, komanda, HTML) tekshirilmagan holda yetib borsa vulnerability ochadi. Shu sababli validatsiyani chegarada bajarish Sonar uchun ham tushunarli bo'ladi. Tipli DTO ishlatsangiz, Bean Validation annotatsiyalari qoidani hujjatlashtiradi. `@Valid` yozilmagan `@RequestBody` keng tarqalgan xato: annotatsiyalar bor, lekin hech qachon ishlamaydi. Enum yoki whitelist orqali qabul qilish esa taint zanjirini butunlay uzadi, chunki qiymat endi foydalanuvchidan emas, sizning ro'yxatingizdan keladi.

```java
// Yomon: tekshiruv yo'q, sort maydoni to'g'ridan-to'g'ri so'rovga ketadi
@GetMapping("/reports")
public List<Report> list(@RequestParam String sort, @RequestParam String from) {
    return reportRepo.findAllSorted(sort, LocalDate.parse(from));
}

// Yaxshi: tipli DTO, Bean Validation va whitelist enum
public record ReportQuery(
        @NotNull SortField sort,
        @NotNull @PastOrPresent LocalDate from,
        @Min(1) @Max(200) int size) { }

public enum SortField {
    CREATED_AT("created_at"), TOTAL("total");           // ruxsat etilgan ustunlar
    private final String column;
    SortField(String column) { this.column = column; }
    public String column() { return column; }
}

@GetMapping("/reports")
public List<Report> list(@Valid ReportQuery query) {     // @Valid bo'lmasa tekshiruv ishlamaydi
    return reportService.find(query);
}
```

## 14.4 Qo'lda yozilgan SQL konkatenatsiyasi va parametrlangan so'rov

SQL ni satr qo'shish bilan yig'ish Sonar da ikki xil belgilanadi. Formatlangan so'rov security hotspot sifatida chiqadi, kaliti `java:S2077`. Agar taint tahlili foydalanuvchi qiymatining so'rovga yetib borishini isbotlasa, bu vulnerability darajasiga ko'tariladi. Yechim oddiy: qiymatlar har doim parametr orqali uzatiladi. Muhim nuqta: parametr faqat qiymat uchun ishlaydi, ustun nomi uchun ishlamaydi. Shuning uchun tartiblash ustunini enum orqali whitelist qilish kerak.

```java
// Yomon: konkatenatsiya, Sonar security hotspot yoki vulnerability ochadi
public List<Order> search(String customer, String sort) {
    String sql = "SELECT * FROM orders WHERE customer_name = '" + customer
               + "' ORDER BY " + sort;
    return jdbc.query(sql, new OrderRowMapper());
}

// Yaxshi: qiymat parametr orqali, ustun nomi whitelist orqali
private static final String BASE =
        "SELECT * FROM orders WHERE customer_name = :customer ORDER BY ";

public List<Order> search(String customer, SortField sort) {
    String sql = BASE + sort.column();                  // enum, foydalanuvchi satri emas
    return jdbc.query(sql, Map.of("customer", customer), new OrderRowMapper());
}

// Yoki butunlay Spring Data orqali, SQL qo'lda yozilmaydi
public interface OrderRepository extends JpaRepository<Order, Long> {
    List<Order> findByCustomerName(String customerName, Sort sort);
}
```

## 14.5 `@Transactional` ni noto'g'ri joyga qo'yish bilan bog'liq ogohlantirishlar

`@Transactional` proxy orqali ishlaydi, shuning uchun u faqat tashqaridan kelgan chaqiruvda kuchga kiradi. Sonar shu sababli bir necha ogohlantirish beradi. Bir xil klass ichidagi `this` orqali chaqiruvda annotatsiya butunlay e'tiborsiz qoladi va bu eng og'riqli xato. `private` yoki `final` metodga qo'yilgan annotatsiya ham ishlamaydi, chunki proxy uni override qila olmaydi. Sonar yana bir klass ichida mos kelmaydigan `@Transactional` sozlamalari bilan chaqiruvni belgilaydi, bu qoidaning kaliti `java:S2229`. Amaliy qoida: tranzaksiya chegarasi servisning ommaviy metodi bo'ladi. Controller ga `@Transactional` qo'yish HTTP javob yozilishini tranzaksiya ichiga tortadi.

```java
// Yomon: self-invocation, annotatsiya ishlamaydi; private metodda ham ishlamaydi
@Service
public class StockService {
    public void reserveAll(List<Line> lines) {
        for (Line line : lines) reserve(line);   // this orqali, proxy chetlab o'tiladi
    }

    @Transactional
    private void reserve(Line line) {            // private, proxy override qilmaydi
        stockRepo.decrease(line.sku(), line.qty());
    }
}

// Yaxshi: tranzaksiya chegarasi ommaviy servis metodida, bitta aniq joyda
@Service
public class StockService {
    @Transactional
    public void reserveAll(List<Line> lines) {   // tashqaridan chaqiriladi, proxy ishlaydi
        for (Line line : lines) {
            stockRepo.decrease(line.sku(), line.qty());
        }
    }

    @Transactional(readOnly = true)              // o'qish uchun alohida chegara
    public StockView view(String sku) {
        return stockRepo.findView(sku);
    }
}
```

## 14.6 Sana va vaqt bilan ishlash: eskirgan API va `java.time`

`java.util.Date`, `Calendar` va `SimpleDateFormat` bilan ishlagan kodda Sonar bir necha issue ochadi. Eskirgan konstruktorlar va metodlar uchun `java:S1874` ishlaydi. `SimpleDateFormat` ni `static` maydon sifatida saqlash esa thread safety muammosi, chunki u mutable va bir vaqtda ikki thread dan ishlatilsa noto'g'ri natija beradi. `java.time` paketi bu ikki muammoni ham yopadi: tiplar immutable va `DateTimeFormatter` thread safe. Yana bir jihat: `LocalDateTime` vaqt mintaqasini saqlamaydi, shuning uchun to'lov va audit vaqti uchun `Instant` tanlang.

```java
// Yomon: eskirgan API, thread safe bo'lmagan static formatter
public class InvoiceDates {
    private static final SimpleDateFormat FMT = new SimpleDateFormat("yyyy-MM-dd");

    public Date dueDate(Date issued) {
        Calendar c = Calendar.getInstance();
        c.setTime(issued);
        c.add(Calendar.DAY_OF_MONTH, 30);   // mutable obyektni o'zgartiradi
        return c.getTime();
    }
}

// Yaxshi: java.time, immutable tiplar, thread safe formatter
public final class InvoiceDates {
    private static final DateTimeFormatter FMT = DateTimeFormatter.ISO_LOCAL_DATE;
    private final Clock clock;                // test uchun vaqtni almashtirish mumkin

    public InvoiceDates(Clock clock) { this.clock = clock; }

    public LocalDate dueDate(LocalDate issued) {
        return issued.plusDays(30);           // yangi obyekt qaytaradi
    }

    public Instant paidAt() { return clock.instant(); }
}
```

## 14.7 To'plamlarni qaytarish: modifikatsiya qilinadigan ichki to'plamni chiqarib yuborish

Ichki `List` yoki `Map` ni to'g'ridan-to'g'ri qaytarish Sonar da aniq qoida bilan belgilanadi, kaliti `java:S2384`. Chaqiruvchi qaytgan havola orqali obyektning ichki holatini o'zgartira oladi, demak klass o'z invariantini himoya qilmaydi. Buyurtma qatorlari uchun bu real xato: tashqi kod `add` chaqirsa, summa qayta hisoblanmaydi. `null` qaytarish ham alohida issue, kaliti `java:S1168`, chunki har bir chaqiruvchini tekshirishga majbur qiladi. To'g'ri javob: bo'sh to'plam qaytarish va faqat o'qiladigan ko'rinish berish. Konstruktorda kelgan to'plamni ham ko'chirib olish kerak.

```java
// Yomon: ichki to'plam tashqariga chiqadi, null qaytarish ham issue
public class Order {
    private final List<Line> lines = new ArrayList<>();
    private BigDecimal total = BigDecimal.ZERO;

    public List<Line> getLines() { return lines; }        // tashqi kod add qila oladi
    public List<Discount> getDiscounts() { return null; } // chaqiruvchi tekshirishga majbur
}

// Yaxshi: faqat o'qiladigan ko'rinish, bo'sh to'plam, nazorat qilinadigan qo'shish
public class Order {
    private final List<Line> lines = new ArrayList<>();
    private final List<Discount> discounts = new ArrayList<>();
    private BigDecimal total = BigDecimal.ZERO;

    public List<Line> getLines() { return List.copyOf(lines); }
    public List<Discount> getDiscounts() { return List.copyOf(discounts); }

    public void addLine(Line line) {
        lines.add(line);
        total = total.add(line.amount());                 // invariant saqlanadi
    }
}
```

## 14.8 Strim va sikl ichida og'ir operatsiya

Sikl ichida baza so'rovi yoki tashqi chaqiruv turishi Sonar da bitta qoida bilan emas, bir necha signal bilan ko'rinadi. Satrni `+` bilan sikl ichida yig'ish uchun aniq qoida bor, kaliti `java:S1643`. Strim ichida `peek` orqali yon ta'sir qilish uchun ham qoida bor, kaliti `java:S3864`. N+1 so'rov esa ko'pincha statik tahlilga ko'rinmaydi, shuning uchun uni review va test bilan tutish kerak. Amaliy qoida ikkita. Birinchi: sikldan oldin bir marta so'rab `Map` ga yig'ib qo'yish. Ikkinchi: strimni baza bilan muloqot uchun ishlatmaslik.

```java
// Yomon: sikl ichida so'rov va satr konkatenatsiyasi
public String report(List<String> skus) {
    String out = "";
    for (String sku : skus) {
        Stock stock = stockRepo.findBySku(sku);   // har iteratsiyada bitta so'rov
        out += sku + ":" + stock.getQty() + "\n"; // har iteratsiyada yangi String
    }
    return out;
}

// Yaxshi: bitta so'rov, StringBuilder yoki joining
public String report(List<String> skus) {
    Map<String, Integer> qtyBySku = stockRepo.findAllBySkuIn(skus).stream()
            .collect(Collectors.toMap(Stock::getSku, Stock::getQty));

    return skus.stream()
            .map(sku -> sku + ":" + qtyBySku.getOrDefault(sku, 0))
            .collect(Collectors.joining("\n", "", "\n"));
}
```

## 14.9 Thread va `ExecutorService` bilan bog'liq ogohlantirishlar

Bu sohada Sonar ning eng qat'iy qoidalari bor, chunki xato natijasi kutilmagan bo'ladi. `Thread.run()` ni to'g'ridan-to'g'ri chaqirish yangi thread ochmaydi va buning uchun alohida qoida bor, kaliti `java:S1217`. `InterruptedException` ni yutib yuborish ham bug sifatida belgilanadi, kaliti `java:S2142`: interrupt signali yo'qoladi va thread to'xtamaydi. Yopilmagan `ExecutorService` esa thread leak beradi, ayniqsa har so'rovda yangi pool yaratilsa. Java 21 dan `ExecutorService` `AutoCloseable` ni amalga oshiradi, shuning uchun try-with-resources ishlaydi. Undan oldingi versiyada `shutdown` ni `finally` blokida chaqirish kerak.

```java
// Yomon: run() yangi thread ochmaydi, pool yopilmaydi, interrupt yutiladi
public void notifyAll(List<String> emails) {
    ExecutorService pool = Executors.newFixedThreadPool(8);  // hech qachon yopilmaydi
    for (String email : emails) {
        new Thread(() -> mailer.send(email)).run();           // oddiy metod chaqiruvi
    }
    try {
        pool.awaitTermination(5, TimeUnit.SECONDS);
    } catch (InterruptedException e) {
        // signal yutilib ketdi
    }
}

// Yaxshi: pool spring bean, interrupt qayta tiklanadi
public void notifyAll(List<String> emails) {
    List<CompletableFuture<Void>> tasks = emails.stream()
            .map(email -> CompletableFuture.runAsync(() -> mailer.send(email), pool))
            .toList();
    try {
        CompletableFuture.allOf(tasks.toArray(CompletableFuture[]::new))
                .get(5, TimeUnit.SECONDS);
    } catch (InterruptedException e) {
        Thread.currentThread().interrupt();                   // signal tiklanadi
        throw new NotificationException("to'xtatildi", e);
    } catch (ExecutionException | TimeoutException e) {
        throw new NotificationException("yuborilmadi", e);
    }
}
```

## 14.10 Eskirgan (deprecated) API ishlatish va migratsiya

Eskirgan API chaqirilganda Sonar `java:S1874` ni ochadi. Bu ogohlantirishni e'tiborsiz qoldirishning narxi keyinroq to'lanadi: `forRemoval = true` belgisi bilan kelgan API keyingi major versiyada yo'qoladi va yangilash to'xtab qoladi. Spring Boot 3.x ga o'tishda bu aniq ko'rindi: `WebSecurityConfigurerAdapter` Spring Security 6 da olib tashlandi va uning o'rniga `SecurityFilterChain` bean i keldi. Shuning uchun deprecated issue larni texnik qarz emas, balki muddat belgilangan vazifa deb ko'rish kerak. O'zingiz API eskirtirsangiz, `@Deprecated(since, forRemoval)` va Javadoc dagi `@deprecated` izohida almashtiruvchini aniq ko'rsating. Shunda chaqiruvchi nimaga o'tishini qidirib yurmaydi.

```java
// Yomon: eskirgan metodni chaqirish, almashtiruvchi ko'rsatilmagan
@Deprecated
public BigDecimal calc(Order o) { return o.getTotal(); }

public void send(Order o) {
    BigDecimal sum = calc(o);          // java:S1874, qachon yo'qolishi noma'lum
    gateway.charge(sum);
}

// Yaxshi: muddat va almashtiruvchi aniq, chaqiruv yangi API ga o'tgan
/**
 * @deprecated 2.4 dan beri. {@link #amountToCharge(Order)} dan foydalaning.
 */
@Deprecated(since = "2.4", forRemoval = true)
public BigDecimal calc(Order o) { return amountToCharge(o); }

public Money amountToCharge(Order o) {
    return Money.of(o.total(), o.currency());
}

public void send(Order o) {
    gateway.charge(amountToCharge(o));  // yangi API, issue yo'q
}
```

## 14.11 Test kodidagi tez-tez uchraydigan issue lar

Sonar test kodini ham tahlil qiladi, lekin boshqa qoidalar to'plami bilan. Assertion siz test uchun qoida bor, kaliti `java:S2699`: metod `@Test` bilan belgilangan, lekin hech narsa tekshirmaydi. Bunday test coverage ni oshiradi va hech qanday xatoni tutmaydi, bu esa 100% coverage raqamining eng ko'p uchraydigan aldovi. Test metodlari bo'lmagan test klass uchun `java:S2187` ishlaydi. Testda `Thread.sleep` ishlatish uchun `java:S2925` ishlaydi, chunki bu flaky test manbai. O'chirilgan testlar ham alohida belgilanadi, chunki ular yashirin ravishda abadiy o'chib qoladi. Mok emas, natijani tekshirish odatini saqlang. Test infratuzilmasi haqida batafsil ma'lumot [testlash qo'llanmasida](../testing/README.md).

```java
// Yomon: assertion yo'q, sleep bor, faqat mok tekshirilgan
@Test
void placeOrder() {
    orderService.place(new CreateOrderRequest("SKU-1", 2));   // hech narsa tekshirilmadi
}

@Test
void asyncNotify() throws Exception {
    notifier.notifyAll(List.of("a@b.uz"));
    Thread.sleep(2000);                                       // java:S2925, flaky
    verify(mailer).send("a@b.uz");                            // natija tekshirilmaydi
}
// Yaxshi: natija tekshirilgan, kutish deterministik
@Test
void placeOrderReservesStockAndReturnsId() {
    OrderResponse res = orderService.place(new CreateOrderRequest("SKU-1", 2));

    assertThat(res.id()).isPositive();
    assertThat(stockRepo.findBySku("SKU-1").getQty()).isEqualTo(8);
}

@Test
void asyncNotifySendsOnce() {
    notifier.notifyAll(List.of("a@b.uz"));

    await().atMost(Duration.ofSeconds(2))                     // shart bo'yicha kutish
           .untilAsserted(() -> verify(mailer).send("a@b.uz"));
}
```

## 14.12 Issue larni toifa bo'yicha tartiblash va birinchi nimani tuzatish

Mingta issue bilan ishlashning birinchi qadami ro'yxatni tartiblash. Eski Sonar taksonomiyasida issue lar Bug, Vulnerability, Code Smell va Security Hotspot ga bo'linadi. Yangi liniyada esa software quality (Security, Reliability, Maintainability) va severity (Blocker, High, Medium, Low, Info) ishlatiladi. Qaysi ko'rinish chiqishi versiya va sozlamaga qarab farq qiladi, lekin tartiblash mantiqi bir xil qoladi. Birinchi navbat har doim xavfsizlik va ishonchlilik: ma'lumot oqib ketishi yoki noto'g'ri hisob natijasi bevosita zarar keltiradi. Ikkinchi navbat yangi kod dagi issue lar, chunki quality gate aynan shuni tekshiradi. Uchinchi navbat eski koddagi maintainability, u faqat tegilgan fayllarda tuzatiladi.

| Mezon | Oddiy yondashuv | Arxitektor yondashuvi |
|---|---|---|
| Boshlash nuqtasi | Ro'yxatni tepadan pastga tuzatish | Security va Reliability ni birinchi navbatga qo'yish |
| Eski kod | Hammasini bir sprintda tozalashga urinish | Clean as You Code: faqat tegilgan kodni tozalash |
| Field injection | `@Autowired` qoldirib qoidani o'chirish | Konstruktor injection ni loyiha standarti qilish |
| Katta metod | Metodni ikkiga bo'lib chegaradan o'tish | Mas'uliyatni servisga ko'chirish va test bilan yopish |
| SQL issue | `NOSONAR` yoki false positive deb yopish | Parametr va whitelist enum bilan taint zanjirini uzish |
| `@Transactional` | Annotatsiyani ko'proq joyga qo'yish | Tranzaksiya chegarasini bitta qatlamda belgilash |
| Coverage | Raqamni assertion siz test bilan ko'tarish | Assertion sifatini va mutation natijasini kuzatish |
| Deprecated API | Ogohlantirishni e'tiborsiz qoldirish | Muddat belgilangan migratsiya vazifasi ochish |
| Qoidani o'chirish | Shovqin ko'rinsa profildan olib tashlash | Sababni yozib, quality profile ni versiyalab o'zgartirish |

| Tuzoq | Nima bo'ladi | Yechim |
|---|---|---|
| `@Transactional` self-invocation | Tranzaksiya umuman ochilmaydi | Chegarani tashqi ommaviy metodga ko'chirish |
| `private` metodda `@Transactional` | Proxy e'tiborsiz qoldiradi | Metodni ommaviy qilish yoki alohida bean ga chiqarish |
| Ichki `List` ni qaytarish | Tashqi kod invariantni buzadi | `List.copyOf` yoki immutable ko'rinish qaytarish |
| `null` to'plam qaytarish | Har bir chaqiruvchida tekshiruv | Bo'sh to'plam qaytarish |
| Sikl ichida repository chaqiruvi | N+1 so'rov, sekin javob | `findAllBy...In` bilan bitta so'rov va `Map` |
| Yutilgan `InterruptedException` | Thread to'xtamaydi, shutdown osiladi | `Thread.currentThread().interrupt()` chaqirish |
| Yopilmagan `ExecutorService` | Thread leak va xotira o'sishi | Pool ni bean qilish yoki try-with-resources |
| `static SimpleDateFormat` | Parallel ishlatganda noto'g'ri sana | `DateTimeFormatter` va `java.time` |
| Assertion siz test | Coverage yuqori, xato tutilmaydi | Natijani tekshiradigan assertion qo'shish |
| `@RequestBody` da `@Valid` yo'q | Validatsiya annotatsiyalari ishlamaydi | `@Valid` qo'shish va 400 javobni test qilish |

## 14.13 Amalda qo'llash

- [ ] Loyihada `@Autowired` qo'yilgan maydonlarni grep bilan toping va hammasini konstruktor injection ga o'tkazing, maydonlarni `final` qiling.
- [ ] Cognitive complexity chegarasidan oshgan metodlar ro'yxatini Sonar dan oling va eng yuqori uchtasini servis metodlariga bo'ling.
- [ ] Barcha `@RequestBody` va `@ModelAttribute` parametrlarini tekshirib, `@Valid` yo'qlarini qo'shing va noto'g'ri kiritma uchun 400 javobni test bilan yoping.
- [ ] Satr konkatenatsiyasi bilan yig'ilgan SQL larni parametrlangan so'rovga o'tkazing, tartiblash ustunlarini enum whitelist bilan cheklang.
- [ ] `@Transactional` annotatsiyalarini audit qiling: `private`, `final` va self-invocation holatlarini topib chegarani ommaviy servis metodiga ko'chiring.
- [ ] `java.util.Date`, `Calendar` va `SimpleDateFormat` ishlatgan joylarni `java.time` ga ko'chiring, vaqt olishni `Clock` bean i orqali qiling.
- [ ] Getter lar ichida ichki to'plam qaytaradigan joylarni `List.copyOf` ga almashtiring va `null` qaytaradiganlarni bo'sh to'plamga o'zgartiring.
- [ ] Test paketida assertion siz testlarni va `Thread.sleep` ishlatgan testlarni toping, birinchisiga assertion qo'shing, ikkinchisini shart bo'yicha kutishga o'tkazing.

---

[&larr; 13. Sonar o'tadigan kod yozish qoidalari](13-sonar-otadigan-kod-yozish-qoidalari.md) · [Mundarija](README.md) · [15. Cognitive complexity va takrorlanishni kamaytirish &rarr;](15-cognitive-complexity-va-takrorlanishni.md)
