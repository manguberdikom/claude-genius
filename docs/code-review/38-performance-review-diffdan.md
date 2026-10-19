<!-- doc: code-review | chapter: 38 | part: VIII. Kesishgan sifat -->

[Barcha hujjatlar](../../README.md) / [Kod review](README.md)

> Holat: tekshirilgan (2026-10-19). Manbalar bob oxirida.

# 38. Performance review diffdan (Performance from a Diff)

<details>
<summary>Bu bobdagi 10 bo'lim</summary>

- [38.1 Asosiy usul: operatsiyalarni sanash](#381-asosiy-usul-operatsiyalarni-sanash)
- [38.2 Siklda I/O: eng ko'p uchraydigan muammo](#382-siklda-io-eng-kop-uchraydigan-muammo)
- [38.3 Hajm: nima tashiladi](#383-hajm-nima-tashiladi)
- [38.4 Kesh: qachon foyda, qachon zarar](#384-kesh-qachon-foyda-qachon-zarar)
- [38.5 Performance regressiyasini diffdan ko'rish](#385-performance-regressiyasini-diffdan-korish)
- [38.6 O'lchovsiz optimallashtirishni rad etish](#386-olchovsiz-optimallashtirishni-rad-etish)
- [38.7 Review paytida o'lchash](#387-review-paytida-olchash)
- [38.8 Performance byudjeti](#388-performance-byudjeti)
- [38.9 Review checklisti: performance](#389-review-checklisti-performance)
- [38.10 Amalda qo'llash](#3810-amalda-qollash)

</details>


Reviewer yuk sinovini o'tkaza olmaydi, lekin ikki narsani qila oladi: operatsiyalar sonini sanash va hajmni chamalash. Performance xatolarining katta qismi aynan shu ikki o'lchovda ko'rinadi - kod N marta ko'p ish qiladi yoki N marta ko'p ma'lumot tashiydi. Ishlash mexanikasi va napkin math [Arxitektor miyasi](../architect/README.md) da; bu yerda diffdan baholash.

## 38.1 Asosiy usul: operatsiyalarni sanash

Har bir yangi kod yo'li uchun uch savol: nechta DB so'rovi, nechta tarmoq chaqiruvi, nechta obyekt yaratiladi. Javob "ma'lumot hajmiga bog'liq" bo'lsa, bu muammo belgisi.

Quyidagi jadvaldagi raqamlar o'lchanmagan taxmin: ular apparat, tarmoq,
baza sozlamasi va ma'lumot hajmiga qarab bir necha barobar farq qiladi.
Jadvalning maqsadi aniq qiymat berish emas, KATTALIK TARTIBINI eslatish:
xotira nanosekund, tarmoq millisekund, tashqi provayder yuz millisekund.
Review da raqam kerak bo'lsa, u o'z tizimingizdagi metrikadan olinadi.

| Operatsiya | Kattalik tartibi (o'lchanmagan taxmin) | 1000 marta bajarilganda |
| --- | --- | --- |
| Xotiradagi hisob | nanosekundlar | sezilmaydi |
| Log yozish (buferlangan) | mikrosekundlar | millisekundlar |
| Keshdan o'qish (lokal) | mikrosekundlar | millisekundlar |
| Redis chaqiruvi (bir xil DC) | 0.2-1 ms | 0.2-1 sekund |
| DB so'rovi (indeks bilan, bir xil DC) | 0.5-3 ms | 0.5-3 sekund |
| DB so'rovi (seq scan, katta jadval) | 100 ms - sekundlar | daqiqalar |
| HTTP chaqiruvi (ichki servis) | 5-50 ms | 5-50 sekund |
| HTTP chaqiruvi (tashqi provayder) | 50-500 ms | daqiqalar |
| Fayl yozish (disk) | 1-10 ms | sekundlar |
| JSON serializatsiya (1 KB) | mikrosekundlar | millisekundlar |

Shu jadvaldan review ning asosiy qoidasi chiqadi: siklda turgan har qanday I/O - diqqat markazida. Review izohida esa raqam ko'rsatiladi: "1000 qatorli hisobotda bu 1000 HTTP chaqiruv, provayderning p99 i 200 ms - ya'ni 3 daqiqa".

## 38.2 Siklda I/O: eng ko'p uchraydigan muammo

```java
// Naqsh: har element uchun so'rov.
List<OrderDto> enrich(List<Order> orders) {
    return orders.stream().map(o -> new OrderDto(
        o.id(),
        customers.findById(o.customerId()).orElseThrow().name(),   // N so'rov
        products.nameFor(o.firstProductId())                        // yana N
    )).toList();
}

// Yechim: ommaviy yuklash (batch loading) - 2 so'rov.
List<OrderDto> enrich(List<Order> orders) {
    Set<UUID> customerIds = orders.stream().map(Order::customerId).collect(toSet());
    Map<UUID, String> names = customers.findAllById(customerIds).stream()
        .collect(toMap(Customer::id, Customer::name));

    Set<UUID> productIds = orders.stream().map(Order::firstProductId).collect(toSet());
    Map<UUID, String> products = this.products.namesByIds(productIds);

    return orders.stream()
        .map(o -> new OrderDto(o.id(), names.get(o.customerId()),
                               products.get(o.firstProductId())))
        .toList();
}
// Review diqqati: `findAllById` ham chegarasiz bo'lmasligi kerak.
// Sabab rejada emas, protokolda: PostgreSQL ning bitta Bind xabari
// ko'pi bilan 65535 parametr ko'taradi, va pgjdbc bu chegaradan
// oshganda so'rov bazaga yetib bormasdan istisno beradi:
// "Tried to send an out-of-range integer as a 2-byte unsigned int
// value: 100000". Ya'ni bu sekinlik emas, ishlamaydigan kod.
// Bo'laklash kerak, lekin `ids` to'plam bo'lsa `Lists.partition`
// kompilyatsiya qilinmaydi: u `List` talab qiladi. To'plam uchun
// `Iterables.partition(ids, 1000)`.
```

## 38.3 Hajm: nima tashiladi

```java
// Naqsh 1: ortiqcha ustunlar.
SELECT * FROM orders WHERE ...               // 40 ustun, 3 tasi kerak
// 100 000 qator x 2 KB = 200 MB tarmoq va xotira. Projection bilan
// 100 000 x 100 bayt = 10 MB (23.7).

// Naqsh 2: ortiqcha qatorlar.
List<Order> all = orders.findByCustomer(id);     // 5000 buyurtma
return all.stream().filter(o -> o.isOpen()).limit(20).toList();   // 20 kerak
// Filtr va chegara so'rovda bo'lishi kerak.

// Naqsh 3: ortiqcha javob.
public record OrderResponse(Order order, Customer customer, List<Payment> payments,
                            List<Shipment> shipments, List<AuditEntry> audit) { }
// Mijoz ro'yxat ekranida faqat raqam va summani ko'rsatadi, lekin
// server har buyurtma uchun audit tarixini ham yuboradi.
// Review savoli: mijoz bu maydonlarning qaysilarini ishlatadi?

// Naqsh 4: ortiqcha serializatsiya.
String json = mapper.writeValueAsString(bigObject);   // satr sifatida xotirada
// Oqimli yozish: mapper.writeValue(outputStream, bigObject)
```

## 38.4 Kesh: qachon foyda, qachon zarar

```java
// Review savollari har bir yangi kesh uchun.
@Cacheable(value = "rates", key = "#currency")
public Rate rateFor(String currency) { return client.fetch(currency); }
```

1. Ma'lumot qanchalik tez eskiradi va eskirgan qiymat qabul qilinadimi. Valyuta kursi 10 daqiqa - ha; hisob qoldig'i - yo'q.
2. Hit rate qanday bo'ladi. Kalitlar soni ko'p va har biri bir marta so'ralsa, kesh faqat xotira yeydi.
3. Hajmi va TTL si bormi (16.4).
4. Kalitda foydalanuvchi yoki tenant bormi (xavfsizlik, 16.4).
5. Invalidatsiya qanday ishlaydi va ikki instansda mos keladimi.
6. Kesh to'ldirilishi momenti (cache stampede): TTL tugaganda 100 parallel so'rov bir vaqtda tashqi servisga ketadimi.

```java
// Cache stampede dan himoya: bitta so'rov to'ldiradi, qolganlar kutadi.
private final Cache<String, Rate> cache = Caffeine.newBuilder()
    .maximumSize(200)
    .refreshAfterWrite(Duration.ofMinutes(5))     // fonda yangilaydi
    .expireAfterWrite(Duration.ofMinutes(30))     // qattiq chegara
    .recordStats()
    .build(this::loadFromProvider);               // LoadingCache: bitta yuklash

// refreshAfterWrite va expireAfterWrite farqi:
// - refresh: qiymat muddati o'tgandan keyin kelgan so'rov yangilashni
//   BOSHLAYDI (`asyncReload` ni sinxron chaqiradi) va agar qaytgan
//   future allaqachon tugagan bo'lsa yangi qiymatni, aks holda eski
//   qiymatni qaytaradi. Ya'ni "foydalanuvchi hech qachon kutmaydi"
//   degani emas: yuklovchi sinxron ishlasa, o'sha bitta so'rov kutadi.
// - expire: qiymat o'chadi, keyingi so'rov albatta kutadi.
// Review tavsiyasi: tashqi servisga bog'liq keshda ikkisi birga.
// Uchinchi narsa esa ko'pincha e'tibordan chetda qoladi: refresh
// paytidagi istisnolar log ga yoziladi va yutiladi. Demak tashqi
// servis uzilsa, kesh eski qiymatni muddat tugaguncha jimgina
// berib turadi va buni faqat log yoki metrika ko'rsatadi.
```

## 38.5 Performance regressiyasini diffdan ko'rish

| Diffdagi belgi | Nimani bildiradi |
| --- | --- |
| Yangi `@OneToMany` EAGER | Yashirin qo'shimcha so'rovlar |
| Yangi `JOIN` | Qatorlar ko'payishi, reja o'zgarishi |
| `ORDER BY` yangi ustun bo'yicha | Indeks yo'q bo'lsa - sort |
| `DISTINCT` qo'shilgan | Ko'pincha noto'g'ri `JOIN` belgisi |
| Yangi `LEFT JOIN` ko'p qatorli jadvalga | Natija portlashi |
| Siklda `save()` | Batch yo'q |
| Yangi tashqi chaqiruv | Latency qo'shiladi |
| `findAll()` | Chegarasiz yuklash |
| Yangi regex murakkab naqsh bilan | CPU va ReDoS |
| Yangi serializatsiya qatlami | Ortiqcha nusxalash |
| `parallelStream()` | Common pool bloklash |
| Sinxron chaqiruv tranzaksiyada | Ulanish ushlanishi |
| Yangi log `INFO` darajada siklda | Disk va kechikish |

```bash
# Performance xavfini diffdan qidirish.
D=$(git diff origin/main...HEAD)

echo "=== siklda DB yoki HTTP chaqiruvi (qo'lda tekshirish kerak) ==="
git diff -U10 origin/main...HEAD -- '*.java' \
  | awk '/^\+.*(for|while|\.forEach|\.stream\(\).*map)/ {inloop=1; n=0}
         inloop && /^\+.*(repository\.|repo\.|client\.|jdbc\.|restClient|webClient|\.findBy|\.save\()/ {
           print "EHTIMOLIY N+1: " $0; inloop=0 }
         inloop && ++n > 12 { inloop=0 }'

echo "=== findAll va chegarasiz so'rovlar ==="
echo "$D" | grep -nE '^\+.*(findAll\(\)|\.toList\(\)\s*;\s*$)' | head

echo "=== yangi EAGER ==="
# `\s*$` talab qilinmaydi: `@ManyToOne(optional = false)` ham EAGER.
echo "$D" | grep -nE '^\+.*FetchType\.EAGER|^\+.*@(ManyToOne|OneToOne)\b'

echo "=== siklda log ==="
echo "$D" | grep -nE '^\+.*log\.(info|debug)' | head
```

## 38.6 O'lchovsiz optimallashtirishni rad etish

Review ning teskari vazifasi ham bor: asossiz optimallashtirishni to'xtatish. Murakkab optimallashtirish o'qish narxini oshiradi va ko'pincha hech narsa bermaydi.

```java
// PR da: "performance uchun" qo'lda kesh va murakkab mantiq qo'shilgan.
private final Map<String, BigDecimal> precomputed = new ConcurrentHashMap<>();
private final int[] lookupTable = buildLookupTable();           // 200 satr

// Review savollari:
// 1) Bu kod qancha marta chaqiriladi? (metrikada: kuniga 400 marta)
// 2) Hozirgi vaqti qancha? (p99 = 3 ms)
// 3) Yangi vaqti qancha? (o'lchanmagan)
// 4) Bu yo'l profilda ko'rindimi? (yo'q)
// Xulosa: kuniga 400 marta chaqiriladigan 3 ms lik kod uchun 200 satr
// murakkablik arzimaydi. Raqamni ehtiyot bilan o'qish kerak: 400 x 3 ms
// bu kuniga 1,2 sekund, va u ham yuqori chegara, chunki 3 ms p99 emas,
// o'rtacha emas. Ya'ni "jami vaqt" raqami aniq emas; aniq bo'lgani shu
// foyda foydalanuvchining birorta so'rovida ham sezilmasligi.

// Review izohi: "Optimallashtirishdan oldin o'lchov kerak. Agar bu yo'l
// haqiqatan muammo bo'lsa, profil natijasini (async-profiler yoki JFR)
// qo'shsangiz, birga ko'ramiz. Hozirgi metrikada bu endpoint p99 = 40 ms
// va uning 35 ms i DB so'roviga ketadi - optimallashtirish shu yerda
// qaytim beradi."
```

## 38.7 Review paytida o'lchash

```bash
# Yuqori xavfli PR uchun: lokalda o'lchash va dalil to'plash.
# 1) Endpoint ni yuk bilan sinash (oldin va keyin).
#    Base branch da:
git switch main && ./mvnw -q spring-boot:run &
hey -n 2000 -c 20 -H "Authorization: Bearer $TOKEN" http://localhost:8080/api/orders
#    PR branchda bir xil o'lchov:
git switch pr-1423 && ./mvnw -q spring-boot:run &
hey -n 2000 -c 20 -H "Authorization: Bearer $TOKEN" http://localhost:8080/api/orders
# Taqqoslash: p50, p95, p99 va so'rovlar/sekund.

# 2) So'rovlar sonini taqqoslash (eng tez signal). Bu yerda ikki xil
#    narsa aralashtiriladi: `hibernate.generate_statistics` SQL MATNINI
#    loglamaydi, u faqat sanoq qatorlarini chiqaradi. SQL matni uchun
#    `org.hibernate.SQL` logeri DEBUG bo'lishi kerak.
#    SQL matnini sanash uchun:
#      logging.level.org.hibernate.SQL=DEBUG
grep -c 'select ' app.log
#    Yoki statistikadan to'g'ridan-to'g'ri sanoqni olish (aniqroq,
#    chunki log formatiga bog'liq emas):
#      hibernate.generate_statistics=true
#      sessionFactory.getStatistics().getPrepareStatementCount()

# 3) Profil olish: CPU vaqti qayerga ketadi.
#    async-profiler (eng foydali vosita):
java -agentpath:/opt/async-profiler/libasyncProfiler.so=start,event=cpu,file=/tmp/cpu.html \
     -jar target/app.jar
# Yoki JFR:
java -XX:StartFlightRecording=duration=60s,filename=/tmp/rec.jfr -jar target/app.jar
jfr summary /tmp/rec.jfr
jfr print --events jdk.ExecutionSample /tmp/rec.jfr | head -50

# 4) Allokatsiya profili: GC bosimi manbasi.
java -agentpath:/opt/async-profiler/libasyncProfiler.so=start,event=alloc,file=/tmp/alloc.html \
     -jar target/app.jar
```

## 38.8 Performance byudjeti

Review ni did bahsidan chiqarish uchun endpointlar uchun byudjet belgilanadi va PR shu byudjetga nisbatan baholanadi.

```yaml
# performance-budget.yml - loyihada saqlanadi, review da havola qilinadi.
endpoints:
  - path: GET /api/orders
    p99_ms: 300
    max_db_queries: 3
    max_external_calls: 0
    max_response_kb: 50
  - path: POST /api/orders
    p99_ms: 500
    max_db_queries: 6
    max_external_calls: 1      # to'lov provayderi
    max_response_kb: 5
  - path: GET /api/reports/monthly
    p99_ms: 5000               # og'ir hisobot, ongli qabul qilingan
    max_db_queries: 2
    max_external_calls: 0
    async: true                # natija fayl sifatida beriladi
```

Bu testda bitta tuzoq bor va u testni foydasiz qiladi: Hibernate
statistikasi default holatda O'CHIQ, chunki u qo'shimcha CPU va xotira
talab qiladi. Yoqilmagan statistikada hisoblagich oshmaydi, ya'ni
`getPrepareStatementCount()` har doim 0 qaytaradi va byudjet testi
hech qachon yiqilmaydi. Shuning uchun test profilida statistikani
yoqish va hisoblagichning haqiqatan ishlayotganini tasdiqlash kerak.

```properties
# src/test/resources/application-test.properties
spring.jpa.properties.hibernate.generate_statistics=true
```

```java
// Byudjetni test bilan qulflash: so'rovlar soni (23.2) va javob hajmi.
@Test
void orderListStaysWithinBudget() {
    seedOrders(500);
    Statistics stats = statistics();
    // Himoya: statistika o'chiq bo'lsa test yashil yolg'on gapiradi.
    assertThat(stats.isStatisticsEnabled())
        .as("hibernate.generate_statistics test profilida yoqilgan")
        .isTrue();
    stats.clear();

    MvcTestResult result = mvc.get().uri("/api/orders?size=20").exchange();

    long queries = stats.getPrepareStatementCount();
    assertThat(queries).as("DB so'rovlari").isBetween(1L, 3L);
    assertThat(result.getResponse().getContentAsByteArray().length / 1024)
        .as("javob hajmi (KB)").isLessThanOrEqualTo(50);
}
```

Yuqori chegara bilan birga PASTKI chegara ham qo'yilgani bejiz emas:
`isBetween(1, 3)` so'rov umuman bajarilmagan holatni ham ushlaydi, ya'ni
endpoint keshdan javob bergan yoki test umuman boshqa yo'ldan ketgan
holatni. Faqat `isLessThanOrEqualTo(3)` yozilganda bu holat yashil
chiqadi.

## 38.9 Review checklisti: performance

| Savol | Nega |
| --- | --- |
| Siklda DB yoki HTTP chaqiruvi bormi | N+1 |
| So'rovlar soni ma'lumot hajmiga bog'liqmi | Masshtablanmaydi |
| Chegarasiz yuklash bormi | Xotira va kechikish |
| Faqat kerakli ustunlar o'qiladimi | Ortiqcha tashish |
| Yangi `JOIN` natijani ko'paytirmaydimi | Qatorlar portlashi |
| Yangi `ORDER BY` indeksli ustundami | Sort |
| Kesh TTL, hajm va kalit to'g'rimi | Eskirgan yoki oqadigan ma'lumot |
| Cache stampede himoyasi bormi | Tashqi servisga to'lqin |
| Tranzaksiya ichida tashqi chaqiruv bormi | Ulanish ushlanishi |
| Optimallashtirish o'lchov bilan asoslanganmi | Ortiqcha murakkablik |
| Byudjetga sig'adimi | Regressiya |
| Og'ir operatsiyalar async mi | Timeout va thread |

## 38.10 Amalda qo'llash

- [ ] Eng muhim 5-10 endpoint uchun performance byudjetini (p99, so'rovlar soni, javob hajmi) yozib, repoda saqlang.
- [ ] Byudjetni test bilan qulflang: so'rovlar soni va javob hajmi tekshiruvi.
- [ ] Diffda siklda I/O ni qidiradigan skriptni review oqimiga qo'shing.
- [ ] `findAll()` va chegarasiz so'rovlarni toping va ularga `LIMIT` yoki bo'laklash qo'shing.
- [ ] Barcha keshlar uchun hit rate metrikasini yoqib, foyda bermayotganlarini aniqlang.
- [ ] Tashqi servisga bog'liq keshlarda `refreshAfterWrite` + `expireAfterWrite` kombinatsiyasini qo'ying.
- [ ] Yuqori xavfli PR lar uchun `hey` yoki `k6` bilan oldin/keyin o'lchov qilish amaliyotini joriy qiling.
- [ ] Prodda async-profiler yoki JFR bilan muntazam profil olishni sozlab, optimallashtirish qarorlarini dalilga asoslang.

## Manbalar

- Hibernate ORM, *Statistics* va *Fetching* qo'llanmasi
  ([https://github.com/hibernate/hibernate-orm/blob/7.4.13/documentation/src/main/asciidoc/userguide/chapters/statistics/Statistics.adoc](https://github.com/hibernate/hibernate-orm/blob/7.4.13/documentation/src/main/asciidoc/userguide/chapters/statistics/Statistics.adoc),
  tag `7.4.13`, Apache-2.0) - 38.8 dagi statistikaning default o'chiqligi
  va 38.5 dagi `@ManyToOne` bilan `@OneToOne` ning spetsifikatsiya
  bo'yicha EAGER bo'lishi.
- Hibernate ORM, `SqlStatementLogger`
  ([https://github.com/hibernate/hibernate-orm/blob/7.4.13/hibernate-core/src/main/java/org/hibernate/engine/jdbc/spi/SqlStatementLogger.java](https://github.com/hibernate/hibernate-orm/blob/7.4.13/hibernate-core/src/main/java/org/hibernate/engine/jdbc/spi/SqlStatementLogger.java),
  tag `7.4.13`, Apache-2.0) - 38.7 dagi SQL matni `org.hibernate.SQL`
  logeri DEBUG bo'lganda chiqishi.
- pgjdbc, `PGStream` va `BatchedQuery`
  ([https://github.com/pgjdbc/pgjdbc/blob/REL42.7.14/pgjdbc/src/main/java/org/postgresql/core/PGStream.java](https://github.com/pgjdbc/pgjdbc/blob/REL42.7.14/pgjdbc/src/main/java/org/postgresql/core/PGStream.java),
  tag `REL42.7.14`, BSD-2-Clause) - 38.2 dagi bitta Bind xabaridagi
  65535 parametr chegarasi va undan oshganda chiqadigan istisno.
- Guava, `Lists` va `Iterables`
  ([https://github.com/google/guava/blob/v33.7.2/guava/src/com/google/common/collect/Iterables.java](https://github.com/google/guava/blob/v33.7.2/guava/src/com/google/common/collect/Iterables.java),
  tag `v33.7.2`, Apache-2.0) - 38.2 dagi `Lists.partition` ning `List`
  talab qilishi va to'plam uchun `Iterables.partition`.
- Caffeine, `Caffeine` javadoc i
  ([https://github.com/ben-manes/caffeine/blob/v3.3.1/caffeine/src/main/java/com/github/benmanes/caffeine/cache/Caffeine.java](https://github.com/ben-manes/caffeine/blob/v3.3.1/caffeine/src/main/java/com/github/benmanes/caffeine/cache/Caffeine.java),
  tag `v3.3.1`, Apache-2.0) - 38.4 dagi `refreshAfterWrite` ning sinxron
  `asyncReload` chaqiruvi va refresh istisnolarining yutilishi.
- Spring Framework, `MockMvcTester`
  ([https://github.com/spring-projects/spring-framework/blob/v7.0.9/spring-test/src/main/java/org/springframework/test/web/servlet/assertj/MockMvcTester.java](https://github.com/spring-projects/spring-framework/blob/v7.0.9/spring-test/src/main/java/org/springframework/test/web/servlet/assertj/MockMvcTester.java),
  tag `v7.0.9`, Apache-2.0) - 38.8 dagi `mvc.get().uri(...).exchange()`
  API si.
- async-profiler, *Profiler Options*
  ([https://github.com/async-profiler/async-profiler/blob/v4.5/docs/ProfilerOptions.md](https://github.com/async-profiler/async-profiler/blob/v4.5/docs/ProfilerOptions.md),
  tag `v4.5`, Apache-2.0) - 38.7 dagi `event=cpu` va `event=alloc`
  bilan agent chaqiruvi.
- OpenJDK, `jfr` vositasining `print` va `summary` buyruqlari
  ([https://github.com/openjdk/jdk/blob/jdk-28+20/src/jdk.jfr/share/classes/jdk/jfr/internal/tool/Print.java](https://github.com/openjdk/jdk/blob/jdk-28+20/src/jdk.jfr/share/classes/jdk/jfr/internal/tool/Print.java),
  tag `jdk-28+20`, GPLv2 + Classpath istisnosi) - 38.7 dagi
  `jfr print --events jdk.ExecutionSample` va `jfr summary`.

---

[&larr; 37. API moslik va breaking change review](37-api-moslik-va-breaking-change-review.md) · [Mundarija](README.md) · [39. Observability review &rarr;](39-observability-review.md)
