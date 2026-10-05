<!-- doc: code-review | chapter: 16 | part: III. Java kodini chuqur tahlil -->

[Barcha hujjatlar](../../README.md) / [Kod review](README.md)

> Holat: AI yozgan, inson tekshirmagan.

# 16. Resurs, xotira va GC bosimi review (Resources and Memory)

<details>
<summary>Bu bobdagi 10 bo'lim</summary>

- [16.1 Chegarasiz to'plam - eng ko'p uchraydigan OOM sababi](#161-chegarasiz-toplam---eng-kop-uchraydigan-oom-sababi)
- [16.2 Hajmni diffdan baholash](#162-hajmni-diffdan-baholash)
- [16.3 Resursni yopish](#163-resursni-yopish)
- [16.4 Kesh - boshqarilmagan xotira](#164-kesh---boshqarilmagan-xotira)
- [16.5 Allokatsiya bosimi: GC ni ko'p ishlashga majburlash](#165-allokatsiya-bosimi-gc-ni-kop-ishlashga-majburlash)
- [16.6 Katta javob va serializatsiya](#166-katta-javob-va-serializatsiya)
- [16.7 Xotira oqishining tipik manbalari Spring da](#167-xotira-oqishining-tipik-manbalari-spring-da)
- [16.8 Connection pool: eng tez tugaydigan resurs](#168-connection-pool-eng-tez-tugaydigan-resurs)
- [16.9 Review paytida xotirani o'lchash](#169-review-paytida-xotirani-olchash)
- [16.10 Amalda qo'llash](#1610-amalda-qollash)

</details>


Xotira muammolari diffda deyarli ko'rinmaydi: bitta qator kod 2 million obyekt yaratishi mumkin. Shu sababli bu bobning asosiy savoli hajm haqida: shu kod eng katta real kirishda nechta obyekt yaratadi va nechtasini bir vaqtda ushlab turadi. JVM xotira hududlari va GC mexanikasi [Arxitektor miyasi](../architect/README.md) da; bu yerda diffdan hajmni baholash.

## 16.1 Chegarasiz to'plam - eng ko'p uchraydigan OOM sababi

```java
// Naqsh: butun jadvalni xotiraga yuklash. Diffda bir qator, prodda OOM.
List<Order> all = orders.findAll();                       // 4 mln qator
Map<String, Order> byNumber = all.stream()
    .collect(toMap(Order::number, identity()));           // yana 4 mln yozuv

// Review izohi: `orders` jadvalida hozir 4.2 mln qator (DB da tekshirdim).
// Har bir Order taxminan 400 bayt + kolleksiyalar bilan ko'proq, ya'ni
// kamida 1.7 GB. Pod limiti 1 GB - bu kod birinchi ishga tushishda OOM.

// Yechim 1: so'rovda filtrlash va chegaralash.
List<Order> recent = orders.findTop500ByStatusOrderByCreatedAtDesc(OPEN);

// Yechim 2: bo'laklab ishlash (katta hajm uchun).
int page = 0;
Slice<Order> slice;
do {
    slice = orders.findByStatus(OPEN, PageRequest.of(page++, 1_000));
    process(slice.getContent());
    em.clear();                      // birinchi daraja keshni bo'shatish
} while (slice.hasNext());
// Diqqat: Page emas, Slice - Page har safar COUNT(*) so'rovini bajaradi.

// Yechim 3: kursor bilan oqim (eng tejamli, 5.7 da ko'rsatilgan).
```

## 16.2 Hajmni diffdan baholash

Reviewer bir nechta oddiy raqamni yodda tutsa, hajmni tez chamalay oladi.

| Narsa | Taxminiy hajm |
| --- | --- |
| Obyekt sarlavhasi | 12-16 bayt |
| `Long` o'rami | ~16 bayt (primitiv 8) |
| `String` (n belgi, lotin) | ~40 + n bayt |
| `ArrayList` elementi | 4-8 bayt havola + obyekt |
| `HashMap` yozuvi | ~32-48 bayt + kalit va qiymat |
| JPA entity (10 maydon) | 200-500 bayt |
| JSON matn (entity) | 2-5 baravar entity dan katta |

```bash
# Review paytida haqiqiy hajmni tekshirish: taxmin qilmaslik.
psql -c "SELECT relname,
                to_char(n_live_tup, '999G999G999') AS qatorlar,
                pg_size_pretty(pg_total_relation_size(relid)) AS hajm
           FROM pg_stat_user_tables
          ORDER BY n_live_tup DESC LIMIT 10;"

# Pod xotira limiti va hozirgi heap sozlamasi.
kubectl get deploy order-service -o jsonpath='{.spec.template.spec.containers[0].resources}'
# JVM konteynerda limitning qanchasini oladi (standart 25%):
java -XX:+PrintFlagsFinal -version | grep -E 'MaxRAMPercentage|MaxHeapSize'
```

Review izohining kuchi aynan shu raqamlarda: "jadval katta bo'lishi mumkin" degan gap bahs tug'diradi, "jadvalda 4.2 mln qator, pod limiti 1 GB" degan gap qarorni hal qiladi.

## 16.3 Resursni yopish

```java
// Naqsh 1: Stream yopilmaydi (5.7 da ko'rilgan).
// Naqsh 2: javax/jakarta resurslari.
InputStream in = s3.getObject(key);           // yopilmasa - ulanish pool i tugaydi
// try-with-resources majburiy:
try (InputStream in = s3.getObject(key)) { ... }

// Naqsh 3: javadagi ichki resurs e'tibordan chetda.
Files.lines(path).forEach(this::process);     // fayl deskriptori yopilmaydi
try (Stream<String> lines = Files.lines(path, UTF_8)) { lines.forEach(this::process); }

// Naqsh 4: HttpClient javob tanasi o'qilmaydi yoki yopilmaydi.
// Spring RestClient/WebClient o'zi boshqaradi, lekin quyi darajada:
try (Response r = okHttp.newCall(req).execute()) { ... }   // yopilmasa pool oqadi

// Naqsh 5: ExecutorService yopilmaydi (15.7).
// Naqsh 6: temporary fayl o'chirilmaydi.
Path tmp = Files.createTempFile("report", ".pdf");
try { ... } finally { Files.deleteIfExists(tmp); }   // disk to'lishi oldini oladi
```

## 16.4 Kesh - boshqarilmagan xotira

Kesh xotira muammolarining ikkinchi eng katta manbasi, chunki u ongli ravishda ma'lumotni ushlab turadi.

```java
// Naqsh: chegarasiz kesh.
private final Map<String, Report> cache = new HashMap<>();   // o'sishi cheksiz

// To'g'ri: hajm, TTL, metrika va yaxlitlash siyosati.
@Bean
Cache<ReportKey, Report> reportCache(MeterRegistry registry) {
    Cache<ReportKey, Report> cache = Caffeine.newBuilder()
        .maximumWeight(50 * 1024 * 1024)                 // 50 MB chegarasi
        .weigher((ReportKey k, Report v) -> v.sizeInBytes())
        .expireAfterWrite(Duration.ofMinutes(15))
        .recordStats()
        .build();
    CaffeineCacheMetrics.monitor(registry, cache, "report");   // hit rate ko'rinadi
    return cache;
}
```

Kesh uchun review savollari: hajmi cheklanganmi, qachon eskiradi, invalidatsiya qanday ishlaydi, hit rate o'lchanadimi, va eng muhimi - keshlangan ma'lumot foydalanuvchiga bog'liqmi. Oxirgi savol xavfsizlik bilan bog'liq: kalitda `tenantId` yoki `userId` bo'lmasa, bir foydalanuvchi boshqasining ma'lumotini oladi.

```java
// Xavfsizlik xatosi keshda: kalit foydalanuvchini hisobga olmaydi.
@Cacheable(value = "orders", key = "#page")                  // xato!
public List<OrderDto> myOrders(int page) {
    return orders.findByCustomer(currentUser().id(), page);  // natija har kimga boshqa
}
// To'g'ri: kalitda foydalanuvchi bor.
@Cacheable(value = "orders", key = "#root.target.currentUser().id() + ':' + #page")
```

## 16.5 Allokatsiya bosimi: GC ni ko'p ishlashga majburlash

Xotira yetarli bo'lsa ham, ko'p obyekt yaratish latency ga ta'sir qiladi: young GC tez-tez ishlaydi, p99 o'sadi.

| Naqsh | Nima bo'ladi |
| --- | --- |
| Siklda yangi `StringBuilder`, `SimpleDateFormat`, `ObjectMapper` | Har iteratsiyada ortiqcha obyekt |
| Siklda satr konkatenatsiyasi | O(n^2) allokatsiya |
| Autoboxing siklda (`Map<Integer,...>` kalitlar) | Har operatsiyada `Integer` o'rami |
| Katta `byte[]` ni to'liq xotiraga o'qish | Humongous allokatsiya (G1 da alohida muammo) |
| Logda `String.format` yoki konkatenatsiya | Log o'chirilgan bo'lsa ham hisob bajariladi |
| Ortiqcha DTO zanjiri | Har qatlamda yangi obyekt |

```java
// Log allokatsiyasi: eng ko'p e'tibordan chetda qoladigan joy.
log.debug("buyurtma qayta ishlandi: " + order.toString() + " " + total);   // har doim
log.debug("buyurtma qayta ishlandi: {} {}", order.id(), total);            // lazy
// Birinchi variantda DEBUG o'chirilgan bo'lsa ham satr quriladi.
// Katta kolleksiya uchun esa:
if (log.isTraceEnabled()) log.trace("qatorlar: {}", expensiveDump(rows));
```

## 16.6 Katta javob va serializatsiya

```java
// Naqsh: butun natija xotirada JSON ga aylanadi.
@GetMapping("/export")
public List<OrderDto> export() {                    // 500k qator -> ~300 MB JSON
    return orders.findAll().stream().map(OrderDto::from).toList();
}

// Yechim: oqimli javob, xotirada bir vaqtda bir qator.
@GetMapping(value = "/export", produces = "text/csv")
public void export(HttpServletResponse response) throws IOException {
    response.setHeader("Content-Disposition", "attachment; filename=orders.csv");
    try (PrintWriter out = response.getWriter();
         Stream<Order> rows = orders.streamAll()) {       // kursor
        out.println("id;number;total");
        rows.forEach(o -> {
            out.printf("%s;%s;%s%n", o.id(), o.number(), o.total());
            em.detach(o);                                 // keshni o'stirmaslik
        });
    }
}
// Review qo'shimcha savollari: timeout (nginx/ingress), mijoz uzilsa nima
// bo'ladi, va bu endpoint uchun rate limit bormi.
```

## 16.7 Xotira oqishining tipik manbalari Spring da

| Manba | Belgisi |
| --- | --- |
| `static` kolleksiyaga qo'shish | `static List.add` hech qachon tozalanmaydi |
| Listener ro'yxatdan chiqarilmaydi | `addListener` bor, `removeListener` yo'q |
| `ThreadLocal` tozalanmaydi | `remove()` yo'q (15.9) |
| Chegarasiz kesh | `HashMap` kesh sifatida |
| Class loader oqishi | Hot reload, ko'p deploy |
| Hibernate birinchi daraja keshi | Katta sikl ichida `clear()` yo'q |
| Ulanish/kursor yopilmaydi | `Stream`, `ResultSet` |
| Katta sessiya ma'lumoti | `HttpSession` ga katta obyektlar |
| Metrika teglarida cheksiz qiymat | `tag("userId", id)` - kardinallik portlashi |

Oxirgi band alohida e'tiborga loyiq: Micrometer teglarida foydalanuvchi ID si yoki URL yo'li bo'lsa, metrikalar soni cheksiz o'sadi va Prometheus ham, ilova xotirasi ham to'ladi.

```java
// Kardinallik portlashi: har foydalanuvchi uchun alohida metrika.
meter.counter("orders.created", "userId", userId.toString()).increment();   // xato
// To'g'ri: teglar cheklangan to'plamdan.
meter.counter("orders.created", "tier", customer.tier().name()).increment();
```

## 16.8 Connection pool: eng tez tugaydigan resurs

Xotiradan oldin tugaydigan resurs - DB ulanishlari. Review da har bir uzoq operatsiya uchun "bu ulanishni qancha ushlab turadi" savoli beriladi.

```java
// Naqsh: tranzaksiya ichida tashqi chaqiruv - ulanish 30 sekund band.
@Transactional
public void confirm(OrderId id) {
    Order o = orders.findById(id).orElseThrow();
    smsGateway.send(o.phone(), "tasdiqlandi");     // tashqi, sekin
    o.markConfirmed();
}
// 20 ta ulanishli pool da 20 parallel so'rov butun ilovani to'xtatadi:
// yangi so'rovlar connection-timeout gacha kutadi va 500 oladi.

// Yechim: tranzaksiyani qisqartirish, tashqi chaqiruvni tashqariga olish.
public void confirm(OrderId id) {
    Order o = orderTx.markConfirmed(id);           // qisqa tranzaksiya
    outbox.enqueueSms(o.phone(), "tasdiqlandi");   // yoki outbox ichida
}
```

```properties
# Pool sozlamalarini review da tekshirish uchun minimal to'plam.
spring.datasource.hikari.maximum-pool-size=20
spring.datasource.hikari.connection-timeout=2000        # tez xato
spring.datasource.hikari.max-lifetime=1200000
spring.datasource.hikari.leak-detection-threshold=10000 # ushlab qolingan ulanish logi
spring.jpa.properties.hibernate.jdbc.batch_size=50
# PostgreSQL tomonda ham chegara bor: max_connections va har ulanish uchun
# ~5-10 MB. Ko'p pod x katta pool = DB da ulanish tugashi (PgBouncer kerak).
```

## 16.9 Review paytida xotirani o'lchash

```bash
# Yuqori xavfli PR ni lokalda ishga tushirib, haqiqiy raqamni olish.
# 1) Heap holati va obyekt taqsimoti.
jcmd <pid> GC.heap_info
jcmd <pid> GC.class_histogram | head -25          # eng ko'p obyektlar

# 2) GC bosimi: qancha vaqt GC da ketgan.
jcmd <pid> VM.native_memory summary 2>/dev/null | head -20
java -Xlog:gc*:file=/tmp/gc.log -jar app.jar      # keyin gc.log tahlili

# 3) Oqish borligini tekshirish: ikki snapshot farqi.
jcmd <pid> GC.class_histogram > /tmp/h1.txt
# yuk berish
jcmd <pid> GC.class_histogram > /tmp/h2.txt
diff <(awk '{print $2, $4}' /tmp/h1.txt) <(awk '{print $2, $4}' /tmp/h2.txt) | head

# 4) Konteynerda limit va haqiqiy ishlatish.
kubectl top pod -l app=order-service
```

## 16.10 Amalda qo'llash

- [ ] `findAll()` chaqiruvlarini loyihada toping va har biri uchun jadval hajmini `pg_stat_user_tables` dan tekshiring.
- [ ] Chegarasiz kesh sifatida ishlatilgan `HashMap` va `ConcurrentHashMap` larni toping va Caffeine ga (hajm + TTL + metrika bilan) o'tkazing.
- [ ] Kesh kalitlarida foydalanuvchi yoki tenant identifikatori borligini tekshiring - yo'q bo'lsa, bu xavfsizlik xatosi.
- [ ] Barcha `Stream` qaytaradigan repository metodlarini toping va ularning `try-with-resources` ichida ishlatilganini tasdiqlang.
- [ ] Log chaqiruvlarida konkatenatsiya ishlatilgan joylarni platsholder ga o'tkazing.
- [ ] Micrometer teglarida yuqori kardinallikdagi qiymatlarni (ID, URL, email) toping va olib tashlang.
- [ ] `@Transactional` metodlar ichida tashqi chaqiruvlarni grep bilan aniqlab, har biri uchun tranzaksiyani qisqartirish rejasini yozing.
- [ ] `leak-detection-threshold` ni yoqib, ushlab qolingan ulanishlar haqidagi loglarni bir hafta kuzatib boring.
- [ ] Eksport va hisobot endpointlarini oqimli javobga o'tkazing va ularga rate limit qo'ying.

---

[&larr; 15. Holat, mutability va concurrency review](15-holat-mutability-va-concurrency-review.md) · [Mundarija](README.md) · [17. Zamonaviy Java review: record, sealed, pattern matching, virtual thread &rarr;](17-zamonaviy-java-review-record-sealed-pattern.md)
