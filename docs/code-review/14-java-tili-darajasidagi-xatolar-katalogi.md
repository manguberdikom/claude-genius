<!-- doc: code-review | chapter: 14 | part: III. Java kodini chuqur tahlil -->

[Kod review](../../README.md) / [Kod review](README.md)

# 14. Java tili darajasidagi xatolar katalogi (Language-Level Defects)

<details>
<summary>Bu bobdagi 11 bo'lim</summary>

- [14.1 null: chegarada to'xtatish](#141-null-chegarada-toxtatish)
- [14.2 equals, hashCode va compareTo](#142-equals-hashcode-va-compareto)
- [14.3 Sonlar: butun bo'lish, overflow, pul](#143-sonlar-butun-bolish-overflow-pul)
- [14.4 Satr, kodlash va formatlash](#144-satr-kodlash-va-formatlash)
- [14.5 Vaqt va zona](#145-vaqt-va-zona)
- [14.6 Kolleksiyalar](#146-kolleksiyalar)
- [14.7 Stream xatolari](#147-stream-xatolari)
- [14.8 switch, enum va sealed](#148-switch-enum-va-sealed)
- [14.9 Istisnolar: tur va kontekst](#149-istisnolar-tur-va-kontekst)
- [14.10 Review da tez tekshirish uchun grep to'plami](#1410-review-da-tez-tekshirish-uchun-grep-toplami)
- [14.11 Amalda qo'llash](#1411-amalda-qollash)

</details>


Bu bob review ning eng tez ishlatiladigan qismi: Java ning o'zi beradigan tuzoqlar. Ularning ko'pini statik tahlil topadi, lekin reviewer ularni oldin ko'rishi va oqibatini aytishi kerak ([5-bob](05-mashina-va-odam-sonarqube-dan-oldin-topish.md)). Har bo'limda naqsh, nima bo'lishi va review javobi bor.

## 14.1 null: chegarada to'xtatish

Null bilan ishlashning yagona ishonchli strategiyasi - null ni tizim chegarasida to'xtatish va ichkarida null yo'qligini kafolatlash.

```java
// Naqsh 1: tashqi ma'lumot ichkariga null olib kiradi.
public OrderResponse create(@RequestBody OrderRequest req) {   // @Valid yo'q
    // req.customerId() null bo'lishi mumkin: JSON da maydon yo'q edi.
    Order order = orders.place(req.customerId(), req.lines());
    ...
}
// Review javobi: @Valid va @NotNull bilan chegarada to'xtatish; aks holda
// null domenga kiradi va NPE uch qatlam pastda, boshqa stack trace bilan
// chiqadi - diagnostika qiyin.

// Naqsh 2: Optional noto'g'ri ishlatilishi.
Optional<Customer> c = customers.findById(id);
if (c.isPresent()) { use(c.get()); }               // ishlaydi, lekin ortiqcha
customers.findById(id).ifPresent(this::use);       // niyat aniqroq

String name = customers.findById(id).get().name(); // NoSuchElementException
String name = customers.findById(id)
                       .map(Customer::name)
                       .orElseThrow(() -> new CustomerNotFound(id));   // to'g'ri

// Naqsh 3: Optional ni noto'g'ri joyda ishlatish.
public record Customer(String name, Optional<Email> email) { }   // yomon: maydon
public record Customer(String name, @Nullable Email email) {     // yaxshi
    public Optional<Email> email() { return Optional.ofNullable(email); }
}
// Sabab: Optional serializatsiya, JPA va equals bilan yaxshi ishlamaydi;
// u qaytish turi uchun mo'ljallangan.

// Naqsh 4: null bilan boolean mantiq.
Boolean active = settings.get("active");      // null bo'lishi mumkin
if (active) { ... }                           // NPE: avtounboxing
if (Boolean.TRUE.equals(active)) { ... }      // xavfsiz
```

## 14.2 equals, hashCode va compareTo

Bu uchlikdagi xatolar jim ishlaydi: kod kompilyatsiya bo'ladi, testlar o'tadi, va xato faqat `HashMap` yoki `TreeSet` ishlatilganda chiqadi.

| Xato | Oqibati |
| --- | --- |
| `equals` bor, `hashCode` yo'q | `HashSet` da dublikat, `HashMap` da yozuv topilmaydi |
| `hashCode` da mutable maydon | Obyekt o'zgargach `Map` dan yo'qoladi |
| `equals` da `getClass()` o'rniga `instanceof` meros bilan | Nosimmetrik tenglik |
| `compareTo` va `equals` mos emas | `TreeSet` va `HashSet` turlicha xulq |
| `equals` da `BigDecimal` to'g'ridan-to'g'ri | `10.0` va `10.00` teng emas |
| JPA entity da generated ID bilan `equals` | Saqlashdan keyin `hashCode` o'zgaradi |
| Array `equals` | Havola taqqoslanadi, `Arrays.equals` kerak |

```java
// compareTo va equals mos kelmasligi: TreeSet elementni "bor" deb hisoblaydi.
public record Version(int major, int minor, String qualifier) implements Comparable<Version> {
    @Override public int compareTo(Version o) {
        return Comparator.comparingInt(Version::major)
                         .thenComparingInt(Version::minor)
                         .compare(this, o);         // qualifier hisobga olinmaydi
    }
}
// record equals qualifier ni hisobga oladi, compareTo esa yo'q.
// TreeSet<Version> da 1.0-alpha va 1.0-beta bir xil element sanaladi,
// HashSet da ikki xil. Review izohi: compareTo ga qualifier qo'shish yoki
// Comparator ni alohida berish, record ichida emas.
```

## 14.3 Sonlar: butun bo'lish, overflow, pul

```java
// Xato 1: butun sonlar bo'linishi - natija 0.
int percent = count / total * 100;              // count < total bo'lsa 0
double percent = (double) count / total * 100;  // to'g'ri
// Review izohi: bu formula hisobotda 0% ko'rsatadi. Nol bilan bo'lish
// xavfi ham bor: total = 0 bo'lsa ArithmeticException (int) yoki
// Infinity (double) - ikkisi ham tekshirilmagan.

// Xato 2: int overflow jim aylanadi.
int totalBytes = fileCount * bytesPerFile;      // 100_000 * 50_000 manfiy bo'ladi
long totalBytes = (long) fileCount * bytesPerFile;
// Yoki aniq tekshiruv bilan: Math.multiplyExact tashlaydi, jim aylanmaydi.
long totalBytes = Math.multiplyExact((long) fileCount, bytesPerFile);

// Xato 3: pul double da.
double total = 0.1 + 0.2;                        // 0.30000000000000004
BigDecimal total = new BigDecimal("0.1").add(new BigDecimal("0.2"));   // 0.3
// Diqqat: BigDecimal.valueOf(0.1) ham xavfli - double dan o'tadi.
// new BigDecimal("0.1") - satr orqali, aniq.

// Xato 4: BigDecimal da scale va yakkalash e'lon qilinmagan.
BigDecimal vat = total.multiply(new BigDecimal("0.12"));   // scale o'sadi
BigDecimal vat = total.multiply(new BigDecimal("0.12"))
                      .setScale(2, RoundingMode.HALF_UP);  // qoida aniq
// Review savoli: yakkalash qoidasi biznes bilan kelishilganmi? Soliq
// hisobida HALF_UP va HALF_EVEN farqi yiliga sezilarli summa beradi.

// Xato 5: BigDecimal taqqoslashda equals.
if (price.equals(BigDecimal.ZERO)) { }           // 0.00 uchun false
if (price.compareTo(BigDecimal.ZERO) == 0) { }   // to'g'ri
```

## 14.4 Satr, kodlash va formatlash

```java
// Xato 1: kodlash ko'rsatilmagan - platformaga bog'liq natija.
byte[] bytes = text.getBytes();                       // JVM standart kodlashi
byte[] bytes = text.getBytes(StandardCharsets.UTF_8); // aniq
new String(bytes);                                    // yana platformaga bog'liq
new String(bytes, StandardCharsets.UTF_8);

// Xato 2: Locale ko'rsatilmagan - turk tilidagi "i" muammosi.
if (code.toUpperCase().equals("TITLE")) { }                 // tr_TR da buziladi
if (code.toUpperCase(Locale.ROOT).equals("TITLE")) { }      // barqaror

// Xato 3: formatlash Locale siz - o'nlik ajratgich o'zgaradi.
String s = String.format("%.2f", amount);                   // "1,50" yoki "1.50"
String s = String.format(Locale.ROOT, "%.2f", amount);      // har doim "1.50"

// Xato 4: siklda satr qo'shish.
String csv = "";
for (Row r : rows) { csv += r.id() + ";"; }      // O(n^2), 100k qatorda muammo
StringBuilder sb = new StringBuilder();          // yoki Collectors.joining()

// Xato 5: satr taqqoslash == bilan.
if (status == "ACTIVE") { }                      // intern ga bog'liq, xavfli
if ("ACTIVE".equals(status)) { }                 // null-xavfsiz tartib
```

## 14.5 Vaqt va zona

Vaqt bilan ishlash eng ko'p yashirin xato beradigan soha, chunki xatolar faqat ma'lum sharoitda (yozgi vaqt o'tishi, oyning oxiri, boshqa zonadagi foydalanuvchi) ko'rinadi.

```java
// Xato 1: zonasiz vaqt saqlash.
@Column private LocalDateTime createdAt;        // qaysi zonada?
@Column private Instant createdAt;              // UTC nuqta, aniq
// PostgreSQL da: timestamptz (timestamp with time zone) ishlatish kerak,
// timestamp emas. Ikkisi diffda bir xil ko'rinadi, lekin xulqi boshqa.

// Xato 2: hozirgi vaqtni to'g'ridan-to'g'ri olish - test qilinmaydi.
public boolean isExpired() { return expiresAt.isBefore(Instant.now()); }
// Review javobi: Clock ni inyeksiya qilish.
public boolean isExpired(Clock clock) { return expiresAt.isBefore(clock.instant()); }
// Testda: Clock.fixed(Instant.parse("2026-10-04T12:00:00Z"), ZoneOffset.UTC)

// Xato 3: kun hisobi vaqt bilan.
long days = Duration.between(from, to).toDays();          // 23:30 -> 00:30 = 0 kun
long days = ChronoUnit.DAYS.between(fromDate, toDate);    // kalendar kunlari

// Xato 4: kun boshini hisoblash zona bilan.
Instant dayStart = date.atStartOfDay().toInstant(ZoneOffset.UTC);  // noto'g'ri zona
Instant dayStart = date.atStartOfDay(ZoneId.of("Asia/Tashkent")).toInstant();

// Xato 5: yozgi vaqtda mavjud bo'lmagan vaqt.
// Ba'zi zonalarda 02:30 mavjud emas (soat oldinga suriladi).
// ZonedDateTime bu holatni o'zi tuzatadi, LocalDateTime esa jim o'tadi.

// Xato 6: tashqi API ga zonasiz vaqt yuborish.
public record Response(LocalDateTime createdAt) { }     // mijoz zonani bilmaydi
public record Response(OffsetDateTime createdAt) { }    // ofset bilan
```

## 14.6 Kolleksiyalar

```java
// Xato 1: o'zgarmas kolleksiyani o'zgartirishga urinish.
List<String> list = List.of("a", "b");
list.add("c");                                   // UnsupportedOperationException
List<String> list = new ArrayList<>(List.of("a", "b"));   // o'zgartirsa bo'ladi

// Xato 2: Arrays.asList yarim o'zgarmas.
List<String> l = Arrays.asList("a", "b");
l.set(0, "c");                                   // ishlaydi
l.add("c");                                      // istisno - kutilmagan

// Xato 3: null bilan Map.of va List.of.
Map.of("k", maybeNull);                          // NullPointerException
// HashMap null ni qabul qiladi, Map.of yo'q - almashtirishda jim buziladi.

// Xato 4: iteratsiya paytida o'zgartirish.
for (Order o : orders) {
    if (o.isExpired()) orders.remove(o);         // ConcurrentModificationException
}
orders.removeIf(Order::isExpired);               // to'g'ri

// Xato 5: tartib kafolati haqida taxmin.
Map<String, Integer> counts = new HashMap<>();   // tartib yo'q
// Agar javobda tartib muhim bo'lsa - LinkedHashMap yoki TreeMap.
// Review izohi: API javobida HashMap ishlatilgan, mijoz tartibni
// barqaror deb o'ylashi mumkin - JVM versiyasi o'zgarganda tartib o'zgaradi.

// Xato 6: Set ga mutable obyekt qo'yish.
Set<Order> set = new HashSet<>();
set.add(order);
order.setStatus(PAID);                           // hashCode o'zgardi
set.contains(order);                             // false - obyekt "yo'qoldi"
```

## 14.7 Stream xatolari

```java
// Xato 1: oqimda yon ta'sir.
List<Order> result = new ArrayList<>();
orders.parallelStream().forEach(result::add);    // thread-safe emas, buziladi
List<Order> result = orders.parallelStream().toList();   // to'g'ri

// Xato 2: Optional va oqim aralashuvi - jim yo'qotish.
orders.stream().map(this::findCustomer)          // Optional<Customer>
      .filter(Optional::isPresent).map(Optional::get)   // eski uslub
      .toList();
orders.stream().map(this::findCustomer).flatMap(Optional::stream).toList();
// Review savoli: topilmagan mijozlar jim tashlab ketilyapti. Bu niyatmi
// yoki xato? Agar har buyurtmaga mijoz bo'lishi kerak bo'lsa, bu yerda
// istisno tashlanishi kerak.

// Xato 3: toMap da dublikat kalit.
Map<String, Order> byNumber = orders.stream()
    .collect(toMap(Order::number, identity()));   // dublikat bo'lsa IllegalState
// Review: raqamlar yagona ekani kafolatlanganmi? Agar yo'q bo'lsa, merge
// funksiyasi berilishi kerak: toMap(k, v, (a, b) -> b)

// Xato 4: parallelStream bloklaydigan operatsiya bilan.
orders.parallelStream().forEach(o -> httpClient.send(o));  // common pool bloklanadi
// Butun ilovadagi boshqa parallel oqimlar ham sekinlashadi.

// Xato 5: oqimni ikki marta ishlatish.
Stream<Order> s = orders.stream();
long n = s.count();
List<Order> l = s.toList();                      // IllegalStateException

// Xato 6: peek bilan mantiq.
orders.stream().peek(o -> o.setChecked(true)).toList();   // peek kafolatsiz
// peek faqat diagnostika uchun; optimizatsiya uni o'tkazib yuborishi mumkin.
```

## 14.8 switch, enum va sealed

```java
// Xato 1: enum ordinal saqlash.
@Enumerated(EnumType.ORDINAL)                    // 0, 1, 2 saqlanadi
private OrderStatus status;
// Enum da yangi qiymat o'rtaga qo'shilsa, mavjud qatorlar ma'nosi o'zgaradi.
@Enumerated(EnumType.STRING)                     // "PAID" saqlanadi - barqaror
private OrderStatus status;

// Xato 2: enum valueOf tashqi ma'lumot bilan.
OrderStatus s = OrderStatus.valueOf(request.status());   // IllegalArgumentException
// Review: noma'lum qiymat 500 beradi, 400 bermaydi. Xavfsiz o'qish:
Optional<OrderStatus> parsed = Arrays.stream(OrderStatus.values())
    .filter(v -> v.name().equalsIgnoreCase(request.status())).findFirst();

// Xato 3: default bilan yangi qiymatni jim o'tkazish (12.1).
// Yechim: sealed bilan kompilyator tekshiradi.
public sealed interface PaymentResult {
    record Approved(String authCode) implements PaymentResult { }
    record Declined(DeclineReason reason) implements PaymentResult { }
    record Pending(Instant retryAt) implements PaymentResult { }
}
// Pattern matching switch: yangi holat qo'shilsa, kompilyator xato beradi.
String message = switch (result) {
    case Approved a -> "tasdiqlandi: " + a.authCode();
    case Declined d -> "rad etildi: " + d.reason().message();
    case Pending p  -> "kutilmoqda: " + p.retryAt();
    // default yo'q - va bo'lmasligi kerak: to'liqlik kompilyatorda.
};

// Xato 4: enum da mutable holat.
public enum Config {
    INSTANCE;
    private Map<String, String> values = new HashMap<>();   // umumiy mutable holat
}
```

## 14.9 Istisnolar: tur va kontekst

```java
// Xato 1: kontekst yo'qoladi.
catch (SQLException e) {
    throw new ServiceException("xatolik");       // original sabab yo'qoldi
}
catch (SQLException e) {
    throw new ServiceException("buyurtma saqlanmadi: id=" + id, e);   // sabab bor
}

// Xato 2: istisno turi ma'no bermaydi.
throw new RuntimeException("mijoz topilmadi");   // chaqiruvchi ajrata olmaydi
throw new CustomerNotFound(customerId);          // tur bo'yicha ishlash mumkin

// Xato 3: istisno bilan boshqaruv oqimi.
try { return Integer.parseInt(s); }
catch (NumberFormatException e) { return 0; }    // jim 0 - xato yashiringan
// Review savoli: noto'g'ri kirish 0 ga aylanishi biznesga to'g'rimi?
// Pul miqdori bo'lsa, bu jim ma'lumot buzilishi.

// Xato 4: checked istisnoni o'rash va ma'nosini yo'qotish.
catch (IOException e) { throw new RuntimeException(e); }   // ma'no yo'q
catch (IOException e) { throw new ReportGenerationFailed(reportId, e); }

// Xato 5: InterruptedException yutilishi.
catch (InterruptedException e) { }               // thread to'xtatish signali yo'qoldi
catch (InterruptedException e) {
    Thread.currentThread().interrupt();          // signalni qaytarish
    throw new OperationCancelled(e);
}

// Xato 6: finally ichida return yoki istisno.
try { return compute(); }
finally { cleanup(); }                           // cleanup istisno tashlasa,
                                                 // asosiy istisno yo'qoladi
```

## 14.10 Review da tez tekshirish uchun grep to'plami

```bash
# Tilga tegishli xatolarning tez skanerlanishi: PR dagi o'zgargan fayllarda.
FILES=$(git diff --name-only origin/main...HEAD -- '*.java')
[ -z "$FILES" ] && exit 0

echo "=== pul double da ==="
grep -nE '(double|float)\s+\w*(amount|price|total|sum|fee|balance)' $FILES

echo "=== kodlash va Locale ko'rsatilmagan ==="
grep -nE 'getBytes\(\)|new String\([^,)]*\)|toUpperCase\(\)|toLowerCase\(\)|String\.format\("' $FILES

echo "=== zonasiz vaqt va test qilinmaydigan now() ==="
grep -nE 'LocalDateTime\.now\(\)|new Date\(\)|Instant\.now\(\)|System\.currentTimeMillis' $FILES

echo "=== Optional noto'g'ri ishlatilishi ==="
grep -nE '\.get\(\)|isPresent\(\)|Optional<[A-Za-z]+>\s+\w+;' $FILES

echo "=== enum ORDINAL va valueOf ==="
grep -nE 'EnumType\.ORDINAL|\.valueOf\(' $FILES

echo "=== BigDecimal equals va scale ==="
grep -nE 'BigDecimal.*\.equals\(|BigDecimal\.valueOf\([0-9]+\.[0-9]' $FILES

echo "=== jim yutilgan istisno ==="
grep -nA2 -E 'catch\s*\(' $FILES | grep -B1 -E '^\S+[-:]\s*\}' 

echo "=== satr konkatenatsiyasi sikl ichida ==="
grep -nE '\+=\s*"' $FILES
```

Bu skriptni CI da ogohlantirish sifatida ishlatish mumkin, lekin bloklamaslik kerak: har bir naqshning qonuniy holatlari bor. Maqsad - reviewer diqqatini yo'naltirish.

## 14.11 Amalda qo'llash

- [ ] `scripts/review-java-scan.sh` skriptini qo'shing va uni PR da o'zgargan fayllarga ishlatishni review oqimiga kiriting.
- [ ] Loyihadagi pul maydonlarini tekshirib, `double`/`float` ishlatilgan joylarni `BigDecimal` yoki `Money` ga o'tkazish tiketini ochingg.
- [ ] `setScale` va `RoundingMode` ko'rsatilmagan pul hisoblarini toping va yakkalash qoidasini biznes bilan kelishib yozib qo'ying.
- [ ] `@Enumerated(EnumType.ORDINAL)` ishlatilgan joylarni toping - har biri kelajakdagi ma'lumot buzilishi.
- [ ] `Instant.now()` va `LocalDateTime.now()` to'g'ridan-to'g'ri ishlatilgan domen kodini `Clock` inyeksiyasiga o'tkazing.
- [ ] `LocalDateTime` saqlanadigan ustunlarni aniqlab, PostgreSQL da `timestamptz` ga o'tish rejasini tuzing.
- [ ] `toMap` ishlatilgan joylarda kalit yagonaligi kafolatlanganini tekshiring va merge funksiyasini qo'shing.
- [ ] `catch (InterruptedException)` bloklarida `Thread.currentThread().interrupt()` borligini tekshiring.

---

[&larr; 13. Domen modeli review: invariant, agregat, chegara](13-domen-modeli-review-invariant-agregat.md) · [Mundarija](README.md) · [15. Holat, mutability va concurrency review &rarr;](15-holat-mutability-va-concurrency-review.md)
