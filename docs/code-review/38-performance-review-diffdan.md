<!-- doc: code-review | chapter: 38 | part: VIII. Kesishgan sifat -->

[Kod review](../../README.md) / [Kod review](README.md)

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


Reviewer yuk sinovini o'tkaza olmaydi, lekin ikki narsani qila oladi: operatsiyalar sonini sanash va hajmni chamalash. Performance xatolarining katta qismi aynan shu ikki o'lchovda ko'rinadi - kod N marta ko'p ish qiladi yoki N marta ko'p ma'lumot tashiydi. Ishlash mexanikasi va napkin math [Arxitektor miyyasi](../architect/README.md) da; bu yerda diffdan baholash.

## 38.1 Asosiy usul: operatsiyalarni sanash

Har bir yangi kod yo'li uchun uch savol: nechta DB so'rovi, nechta tarmoq chaqiruvi, nechta obyekt yaratiladi. Javob "ma'lumot hajmiga bog'liq" bo'lsa, bu muammo belgisi.

| Operatsiya | Taxminiy narx | 1000 marta bajarilganda |
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
// Review diqqati: `findAllById` ham chegarasiz bo'lmasligi kerak -
// 100 000 ID bilan `IN` so'rovi PostgreSQL da rejani buzadi. Bo'laklash
// kerak: Lists.partition(ids, 1000).
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
// - refresh: eski qiymat qaytariladi, fonda yangilanadi (foydalanuvchi kutmaydi);
// - expire: qiymat o'chadi, keyingi so'rov kutadi.
// Review tavsiyasi: tashqi servisga bog'liq keshda ikkisi birga.
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
echo "$D" | grep -nE '^\+.*FetchType\.EAGER|^\+.*@(ManyToOne|OneToOne)\s*$'

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
// murakkablik - foyda kuniga bir sekunddan kam, narx esa doimiy.

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

# 2) So'rovlar sonini taqqoslash (eng tez signal).
#    hibernate.generate_statistics=true bilan loglardan:
grep -c 'select ' app.log

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

```java
// Byudjetni test bilan qulflash: so'rovlar soni (23.2) va javob hajmi.
@Test
void orderListStaysWithinBudget() {
    seedOrders(500);
    Statistics stats = statistics(); stats.clear();

    MvcTestResult result = mvc.get().uri("/api/orders?size=20").exchange();

    assertThat(stats.getPrepareStatementCount()).as("DB so'rovlari").isLessThanOrEqualTo(3);
    assertThat(result.getResponse().getContentAsByteArray().length / 1024)
        .as("javob hajmi (KB)").isLessThanOrEqualTo(50);
}
```

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

---

[&larr; 37. API moslik va breaking change review](37-api-moslik-va-breaking-change-review.md) · [Mundarija](README.md) · [39. Observability review &rarr;](39-observability-review.md)
