<!-- doc: code-review | chapter: 15 | part: III. Java kodini chuqur tahlil -->

[Kod review](../../README.md) / [Kod review](README.md)

# 15. Holat, mutability va concurrency review (State and Concurrency)

<details>
<summary>Bu bobdagi 12 bo'lim</summary>

- [15.1 Umumiy holatni topish: review ning birinchi qadami](#151-umumiy-holatni-topish-review-ning-birinchi-qadami)
- [15.2 Tekshir-keyin-yoz: eng ko'p uchraydigan poyga](#152-tekshir-keyin-yoz-eng-kop-uchraydigan-poyga)
- [15.3 Yo'qolgan yangilanish (lost update)](#153-yoqolgan-yangilanish-lost-update)
- [15.4 Qulf tartibi va deadlock](#154-qulf-tartibi-va-deadlock)
- [15.5 Bir JVM dagi qulf ko'p instansda ishlamaydi](#155-bir-jvm-dagi-qulf-kop-instansda-ishlamaydi)
- [15.6 Atomiklik illuziyasi](#156-atomiklik-illuziyasi)
- [15.7 Thread pool va navbat review](#157-thread-pool-va-navbat-review)
- [15.8 @Async va xatoning yo'qolishi](#158-async-va-xatoning-yoqolishi)
- [15.9 ThreadLocal va kontekst oqishi](#159-threadlocal-va-kontekst-oqishi)
- [15.10 Virtual thread va pinning](#1510-virtual-thread-va-pinning)
- [15.11 Concurrency uchun review checklisti](#1511-concurrency-uchun-review-checklisti)
- [15.12 Amalda qo'llash](#1512-amalda-qollash)

</details>


Concurrency xatolari review ning eng qiymatli topilmalari, chunki ularni boshqa hech bir filtr ishonchli tutmaydi: test ularni 99 marta o'tkazadi va 100-marta yiqiladi, statik tahlil faqat eng oddiy naqshlarni ko'radi, prod monitoringi esa ularni "tushunarsiz incident" sifatida ko'rsatadi. Reviewer ning qo'lida bitta ishonchli usul bor: har bir umumiy holat uchun "ikki thread bu yerda bir vaqtda bo'lsa nima bo'ladi" savolini berish.

## 15.1 Umumiy holatni topish: review ning birinchi qadami

Spring ilovasida umumiy holat uchta joyda bo'ladi, va reviewer uchalasini ham biladi.

| Qayerda | Belgisi | Nega xavfli |
| --- | --- | --- |
| Singleton bean maydonlari | `private` maydon, `final` emas | Har so'rov shu maydonni ko'radi |
| `static` maydonlar | `static Map`, `static int` | Butun JVM bo'ylab umumiy |
| Tashqi holat | Baza qatori, kesh, fayl | Ko'p instans bo'ylab umumiy |

```java
// Eng ko'p uchraydigan xato: singleton bean ichida so'rov holati.
@Service
public class InvoiceService {
    private BigDecimal runningTotal = BigDecimal.ZERO;    // umumiy maydon!
    private Order current;                                // umumiy maydon!

    public Invoice generate(Order order) {
        this.current = order;                   // ikkinchi so'rov buni almashtiradi
        this.runningTotal = BigDecimal.ZERO;
        for (OrderLine line : order.lines()) {
            this.runningTotal = this.runningTotal.add(line.amount());
        }
        return new Invoice(current.id(), runningTotal);   // boshqa buyurtmaning summasi!
    }
}
// Review izohi (blocker): Spring bean standart holatda singleton. Bu
// maydonlar barcha so'rovlar uchun umumiy. Ikki parallel so'rovda biri
// ikkinchisining summasini oladi - ya'ni mijozga boshqa odamning invoysi
// ko'rsatiladi. Yuk kichik bo'lganda bu deyarli hech qachon ko'rinmaydi,
// shu sababli testda ham chiqmaydi.
// Yechim: holat metodning lokal o'zgaruvchisi bo'lishi kerak.

// To'g'ri: holatsiz bean, hamma narsa lokal.
@Service
public class InvoiceService {
    public Invoice generate(Order order) {
        BigDecimal total = order.lines().stream()
            .map(OrderLine::amount)
            .reduce(Money.ZERO, Money::plus);
        return new Invoice(order.id(), total);
    }
}
```

Review qoidasi: singleton bean ichidagi har bir `final` bo'lmagan maydon savol tug'diradi. Agar u konfiguratsiya yoki kesh bo'lsa - thread-safe bo'lishi kerak. Agar u so'rov holati bo'lsa - xato.

## 15.2 Tekshir-keyin-yoz: eng ko'p uchraydigan poyga

Bu naqsh shunchalik tabiiy ko'rinadi, kod review da osongina o'tadi. Uning belgisi: `if (!exists)` keyin `create`, yoki `if (balance >= amount)` keyin `withdraw`.

```java
// Naqsh: ikki parallel so'rov ikkisi ham "yo'q" deb ko'radi.
@Transactional
public Customer register(String email) {
    if (customers.existsByEmail(email)) {           // T1 va T2: false
        throw new EmailAlreadyUsed(email);
    }
    return customers.save(new Customer(email));     // ikki qator yaratiladi
}
// Review izohi: READ COMMITTED da (PostgreSQL standarti) ikki tranzaksiya
// bir-birining yozilmagan qatorini ko'rmaydi, shuning uchun ikkisi ham
// o'tadi. Test bitta thread da o'tadi, prodda ikki dublikat paydo bo'ladi.

// Yechim 1 (eng ishonchli): unique constraint, xatoni ushlash.
@Transactional
public Customer register(String email) {
    try {
        Customer c = customers.saveAndFlush(new Customer(email));   // flush shart
        return c;
    } catch (DataIntegrityViolationException e) {
        throw new EmailAlreadyUsed(email);          // poyga g'olibi aniq
    }
}
```

```sql
-- Himoya bazada: normalizatsiya bilan birga.
CREATE UNIQUE INDEX customer_email_uniq ON customer (lower(email));
-- lower() bilan: "Ali@x.com" va "ali@x.com" bir xil hisoblanadi.
-- Review savoli: email normalizatsiyasi Java va SQL da bir xilmi?
```

```java
// Yechim 2: qulf bilan (hisob qoldig'i kabi hollarda).
@Transactional
public void withdraw(AccountId id, Money amount) {
    // SELECT ... FOR UPDATE: ikkinchi tranzaksiya kutadi.
    Account acc = accounts.lockById(id).orElseThrow();
    if (acc.balance().isLessThan(amount)) throw new InsufficientFunds();
    acc.debit(amount);
}

// Yechim 3: atomik UPDATE (eng tez, qulf olmaydi).
@Modifying
@Query("""
    update Account a set a.balance = a.balance - :amount
     where a.id = :id and a.balance >= :amount
    """)
int debitIfEnough(@Param("id") UUID id, @Param("amount") BigDecimal amount);
// Qaytgan qiymat 0 bo'lsa - mablag' yetmagan. Bitta atomik operatsiya,
// hech qanday poyga yo'q. Review da shu shakl afzal ko'riladi.
```

## 15.3 Yo'qolgan yangilanish (lost update)

Belgi: obyekt o'qiladi, o'zgartiriladi va saqlanadi, versiya nazorati yo'q. Ikki parallel so'rovda ikkinchisi birinchisining o'zgarishini bosib ketadi.

```java
// Naqsh: ikki admin bir vaqtda mahsulot narxini o'zgartiradi.
Product p = products.findById(id).orElseThrow();
p.setPrice(newPrice);                    // ikkinchi saqlash birinchisini o'chiradi
products.save(p);

// Yechim: optimistik qulf - konflikt aniqlanadi.
@Entity
public class Product {
    @Version private long version;        // Hibernate avtomatik boshqaradi
}
// Ikkinchi saqlash OptimisticLockingFailureException beradi.

// Review savoli: bu istisno qanday ishlanadi? Foydalanuvchiga 409 bilan
// "ma'lumot o'zgargan, qayta yuklang" deyilishi kerak, 500 emas.
@ExceptionHandler(OptimisticLockingFailureException.class)
ResponseEntity<ProblemDetail> onConflict(OptimisticLockingFailureException e) {
    ProblemDetail pd = ProblemDetail.forStatus(CONFLICT);
    pd.setDetail("Yozuv boshqa foydalanuvchi tomonidan o'zgartirildi");
    return ResponseEntity.of(pd).build();
}
```

Review da `@Version` ning yo'qligi har doim savol: bu entity ni ikki foydalanuvchi bir vaqtda o'zgartirishi mumkinmi. Admin paneldan boshqariladigan har qanday ma'lumot uchun javob "ha".

## 15.4 Qulf tartibi va deadlock

Deadlock diffda ko'rinmaydi, chunki u ikki turli kod yo'lining o'zaro ta'siridan paydo bo'ladi. Reviewer uni faqat "bu kod boshqa qanday qulflar bilan uchrashadi" savolini berib topadi.

```java
// Yo'l A: avval hisob, keyin buyurtma.
@Transactional
public void settle(AccountId acc, OrderId ord) {
    accounts.lockById(acc);
    orders.lockById(ord);
}
// Yo'l B (boshqa faylda): avval buyurtma, keyin hisob.
@Transactional
public void cancel(OrderId ord, AccountId acc) {
    orders.lockById(ord);
    accounts.lockById(acc);
}
// Ikki tranzaksiya bir vaqtda ishga tushsa - deadlock. PostgreSQL bittasini
// o'ldiradi (deadlock detected), foydalanuvchi 500 oladi.

// Review javobi: qulf tartibini loyiha bo'ylab bitta qilib belgilash.
// Masalan: har doim identifikator bo'yicha o'sish tartibida qulflash.
List<UUID> ids = Stream.of(accId, ordId).sorted().toList();   // barqaror tartib
ids.forEach(this::lockById);
```

```sql
-- Deadlock larni topish: prodda sodir bo'lgach loglardan.
-- postgresql.conf: log_lock_waits = on, deadlock_timeout = 1s
-- Hozirgi qulf kutishlarini ko'rish:
SELECT blocked.pid AS blocked_pid, blocked.query AS blocked_query,
       blocking.pid AS blocking_pid, blocking.query AS blocking_query
  FROM pg_stat_activity blocked
  JOIN pg_stat_activity blocking ON blocking.pid = ANY(pg_blocking_pids(blocked.pid))
 WHERE blocked.wait_event_type = 'Lock';
```

## 15.5 Bir JVM dagi qulf ko'p instansda ishlamaydi

`synchronized` va `ReentrantLock` faqat bitta JVM ichida ishlaydi. Kubernetes da uch pod bo'lsa, uch mustaqil qulf bo'ladi va himoya yo'q.

```java
// Naqsh: bitta instans uchun yozilgan himoya.
@Scheduled(cron = "0 0 2 * * *")
public synchronized void nightlyBilling() {       // uch podda uch marta ishlaydi
    invoices.generateForAll();
}

// Yechim 1: ma'lumotlar bazasidagi advisory lock (qo'shimcha tizim kerak emas).
@Scheduled(cron = "0 0 2 * * *")
public void nightlyBilling() {
    // pg_try_advisory_lock darhol qaytadi: false bo'lsa boshqa pod ishlayapti.
    Boolean acquired = jdbc.queryForObject(
        "SELECT pg_try_advisory_lock(?)", Boolean.class, BILLING_LOCK_ID);
    if (!Boolean.TRUE.equals(acquired)) {
        log.info("tungi billing boshqa instansda ishlayapti, o'tkazib yuborildi");
        return;
    }
    try { invoices.generateForAll(); }
    finally {
        jdbc.update("SELECT pg_advisory_unlock(?)", BILLING_LOCK_ID);
    }
}
// Diqqat: advisory lock sessiyaga bog'langan. Pool dan olingan ulanish
// qaytarilsa, lock ham qoladi - shuning uchun finally shart, va ulanish
// uzilganda PostgreSQL uni o'zi bo'shatadi.

// Yechim 2: ShedLock yoki Quartz klasterli rejimi (tayyor mexanizm).
@Scheduled(cron = "0 0 2 * * *")
@SchedulerLock(name = "nightlyBilling", lockAtMostFor = "30m", lockAtLeastFor = "1m")
public void nightlyBilling() { invoices.generateForAll(); }
```

Review savoli har bir `@Scheduled` uchun: bu ish ikki instansda bir vaqtda ishga tushsa nima bo'ladi. Javob "ikki marta hisob-faktura" yoki "ikki marta SMS" bo'lsa, qulf majburiy.

## 15.6 Atomiklik illuziyasi

Thread-safe kolleksiya uning ustidagi operatsiyalar ketma-ketligini atomik qilmaydi.

```java
// Naqsh: ConcurrentHashMap, lekin operatsiya atomik emas.
if (!cache.containsKey(key)) {          // T1 va T2: ikkisi ham "yo'q"
    cache.put(key, expensiveLoad(key)); // ikki marta yuklanadi
}
// To'g'ri: atomik birlashtirilgan operatsiya.
cache.computeIfAbsent(key, this::expensiveLoad);   // bir marta yuklanadi

// Naqsh: hisoblagich.
private volatile int counter;
counter++;                              // o'qish-qo'shish-yozish: atomik emas
// volatile ko'rinishni kafolatlaydi, atomiklikni emas.
private final AtomicInteger counter = new AtomicInteger();
counter.incrementAndGet();              // atomik
// Yoki yuqori yukda: LongAdder (kamroq raqobat).
private final LongAdder counter = new LongAdder();

// Naqsh: ikki maydonni birga o'zgartirish.
private volatile Instant from;
private volatile Instant to;
// Har biri alohida volatile, lekin juftlik nomuvofiq ko'rinishi mumkin:
// boshqa thread yangi from va eski to ni ko'radi.
// Yechim: ikkisini bitta immutable obyektga joylash.
private volatile DateRange range;       // bitta atomik almashtirish
```

## 15.7 Thread pool va navbat review

```java
// Naqsh 1: har chaqiruvda yangi pool - thread portlashi.
public void processAll(List<Order> orders) {
    ExecutorService ex = Executors.newFixedThreadPool(10);   // har chaqiruvda 10 thread
    orders.forEach(o -> ex.submit(() -> process(o)));
    // shutdown() yo'q: threadlar abadiy qoladi, OOM gacha o'sadi
}

// Naqsh 2: cheksiz navbat - orqaga bosim yo'q.
new ThreadPoolExecutor(4, 4, 0L, MILLISECONDS, new LinkedBlockingQueue<>());
// Navbat cheksiz: yuk oshganda xotira to'ladi va kechikish cheksiz o'sadi.
// Tez xato berish yaxshiroq.

// To'g'ri: bean sifatida, chegaralangan navbat, aniq rad etish siyosati.
@Bean(destroyMethod = "shutdown")
ThreadPoolTaskExecutor orderExecutor(MeterRegistry registry) {
    ThreadPoolTaskExecutor ex = new ThreadPoolTaskExecutor();
    ex.setCorePoolSize(8);
    ex.setMaxPoolSize(16);
    ex.setQueueCapacity(500);                 // chegara bor
    ex.setThreadNamePrefix("order-");         // thread dump da o'qiladi
    // Navbat to'lsa: chaqiruvchi o'zi bajaradi - tabiiy orqaga bosim.
    ex.setRejectedExecutionHandler(new ThreadPoolExecutor.CallerRunsPolicy());
    ex.setWaitForTasksToCompleteOnShutdown(true);
    ex.setAwaitTerminationSeconds(30);        // graceful shutdown
    ex.initialize();
    // Metrikaga ulash: navbat uzunligi va aktiv threadlar ko'rinadi.
    ExecutorServiceMetrics.monitor(registry, ex.getThreadPoolExecutor(), "order");
    return ex;
}
```

Review savollari pool uchun: hajmi nimaga asoslangan (CPU yoki I/O), navbat chegarasi bormi, rad etish siyosati nima, shutdown qanday, va navbat uzunligi o'lchanadimi.

## 15.8 @Async va xatoning yo'qolishi

```java
// Naqsh: @Async void - xato hech qayerga bormaydi.
@Async
public void sendReceipt(OrderId id) {
    mailer.send(id);                    // istisno jim yutiladi
}

// Yechim 1: CompletableFuture qaytarish va xatoni ishlash.
@Async("orderExecutor")
public CompletableFuture<Void> sendReceipt(OrderId id) {
    return CompletableFuture.runAsync(() -> mailer.send(id));
}

// Yechim 2: global ishlovchi (void metodlar uchun yagona yo'l).
@Configuration
@EnableAsync
class AsyncConfig implements AsyncConfigurer {
    @Override public Executor getAsyncExecutor() { return orderExecutor; }
    @Override public AsyncUncaughtExceptionHandler getAsyncUncaughtExceptionHandler() {
        return (ex, method, params) -> {
            log.error("async xato: {} args={}", method.getName(), params, ex);
            meter.counter("async.failed", "method", method.getName()).increment();
        };
    }
}
```

Qo'shimcha review savoli: `@Async` metod `@Transactional` bilan birga ishlatilganmi. Async thread da yangi tranzaksiya boshlanadi, chaqiruvchining tranzaksiyasi uzatilmaydi; va agar async ishi commit dan oldin ishga tushsa, u hali saqlanmagan ma'lumotni o'qishga urinadi.

## 15.9 ThreadLocal va kontekst oqishi

```java
// ThreadLocal pool dagi thread da qoladi: keyingi so'rov eski qiymatni ko'radi.
public class TenantContext {
    private static final ThreadLocal<TenantId> CURRENT = new ThreadLocal<>();
    public static void set(TenantId id) { CURRENT.set(id); }
    public static TenantId get() { return CURRENT.get(); }
    public static void clear() { CURRENT.remove(); }        // majburiy!
}
// Filter da tozalash finally ichida bo'lishi shart:
try { TenantContext.set(tenantFrom(request)); chain.doFilter(req, res); }
finally { TenantContext.clear(); }
// Aks holda: A tenant so'rovidan keyin B tenant so'rovi A ning ma'lumotini
// ko'radi - bu xavfsizlik incidenti, nafaqat xato.
```

Virtual threadlar bilan bu muammo shakli o'zgaradi: har vazifa uchun yangi thread bo'lgani uchun oqish kamroq, lekin `ScopedValue` afzal ko'riladi. Review da `MDC` (log konteksti) ham xuddi shu tekshiruvni talab qiladi: async chegarasida u ko'chiriladimi.

## 15.10 Virtual thread va pinning

Java 21 dan keyin `spring.threads.virtual.enabled=true` bitta qator bilan xulqni tubdan o'zgartiradi. Review da uch narsa tekshiriladi.

```java
// 1) Pool kattaligi endi throughput ni cheklamaydi - lekin DB pool cheklaydi.
//    10 000 virtual thread 20 ta DB ulanishini kutadi: navbat DB da paydo bo'ladi.
//    Review savoli: Hikari pool va timeout qiymatlari qayta ko'rildimi?

// 2) synchronized bloki ichida uzoq bloklanish carrier thread ni band qiladi
//    (pinning). ReentrantLock esa virtual thread ni to'g'ri "parklaydi".
// Yomon:
public synchronized Token refresh() { return http.fetchToken(); }   // pinning
// Yaxshi:
private final ReentrantLock lock = new ReentrantLock();
public Token refresh() {
    lock.lock();
    try { return http.fetchToken(); } finally { lock.unlock(); }
}

// 3) ThreadLocal keshlari endi foyda bermaydi: har vazifa yangi thread.
//    Pool ga tayangan kesh (ThreadLocal<SimpleDateFormat>) ma'nosiz bo'ladi.
```

## 15.11 Concurrency uchun review checklisti

| Savol | Nimaga qaraladi |
| --- | --- |
| Bean ichida `final` bo'lmagan maydon bormi | Singleton da so'rov holati |
| `static` mutable holat bormi | Butun JVM bo'ylab umumiy |
| Tekshir-keyin-yoz naqshi bormi | Unique constraint yoki atomik UPDATE kerak |
| Entity da `@Version` bormi | Parallel tahrirlash mumkinmi |
| Bir necha qulf olinadimi, tartibi barqarormi | Deadlock xavfi |
| `@Scheduled` ikki instansda ishlaydimi | Taqsimlangan qulf kerak |
| Pool chegaralanganmi, navbat cheklanganmi | Orqaga bosim va OOM |
| `@Async` xatosi qayerga boradi | Jim nosozlik |
| `ThreadLocal` tozalanadimi | Ma'lumot aralashuvi |
| Virtual thread yoqilgan bo'lsa, `synchronized` uzoq bloklaydimi | Pinning |
| Kolleksiya operatsiyalari atomikmi | `computeIfAbsent` va boshqalar |
| Timeout har bir bloklanadigan chaqiruvda bormi | Thread to'planishi |

## 15.12 Amalda qo'llash

- [ ] Barcha `@Service`, `@Component` bean larini skanerlab, `final` bo'lmagan maydonlari borlarini ro'yxatga oling va har birini tekshiring.
- [ ] Tekshir-keyin-yoz naqshlarini toping (`existsBy` yoki `findBy` keyin `save`) va ularga unique constraint yoki atomik `UPDATE` qo'shing.
- [ ] Admin paneldan tahrirlanadigan entity larga `@Version` qo'shing va `OptimisticLockingFailureException` uchun 409 javob handleri yozing.
- [ ] Barcha `@Scheduled` metodlarni sanab, ularning har birida taqsimlangan qulf borligini tekshiring (advisory lock yoki ShedLock).
- [ ] Barcha `ExecutorService` va `TaskExecutor` konfiguratsiyalarini ko'rib, navbat chegarasi va rad etish siyosati borligini tasdiqlang.
- [ ] `ExecutorServiceMetrics` orqali pool metrikalarini Prometheus ga ulang va navbat uzunligi uchun alert qo'ying.
- [ ] `@Async` void metodlarni toping va `AsyncUncaughtExceptionHandler` sozlanganini tekshiring.
- [ ] `ThreadLocal` ishlatilgan joylarda `remove()` ning `finally` ichida chaqirilganini tasdiqlang.
- [ ] Virtual thread yoqilgan bo'lsa, uzoq bloklanadigan `synchronized` bloklarini `ReentrantLock` ga o'tkazing.

---

[&larr; 14. Java tili darajasidagi xatolar katalogi](14-java-tili-darajasidagi-xatolar-katalogi.md) · [Mundarija](README.md) · [16. Resurs, xotira va GC bosimi review &rarr;](16-resurs-xotira-va-gc-bosimi-review.md)
