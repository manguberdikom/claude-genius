<!-- doc: architect | chapter: 11 | part: II. Java chuqur bilim -->

[Barcha hujjatlar](../../README.md) / [Arxitektor miyyasi](README.md)

# 11. Concurrency: thread, lock, atomic, happens-before (Java Concurrency)

<details>
<summary>Bu bobdagi 12 bo'lim</summary>

- [11.1 Parallellik va konkurentlik farqi, qaysi muammoni hal qilamiz](#111-parallellik-va-konkurentlik-farqi-qaysi-muammoni-hal-qilamiz)
- [11.2 Thread holatlari, kontekst almashinuvi va uning narxi](#112-thread-holatlari-kontekst-almashinuvi-va-uning-narxi)
- [11.3 Umumiy holat (shared state) muammosi: poyga sharti va ko'rinuvchanlik](#113-umumiy-holat-shared-state-muammosi-poyga-sharti-va-korinuvchanlik)
- [11.4 `synchronized`, `ReentrantLock`, `ReadWriteLock` va `StampedLock` farqi](#114-synchronized-reentrantlock-readwritelock-va-stampedlock-farqi)
- [11.5 Atomic sinflar va CAS: qachon lock dan tezroq](#115-atomic-sinflar-va-cas-qachon-lock-dan-tezroq)
- [11.6 `volatile` nimani kafolatlaydi va nimani kafolatlamaydi](#116-volatile-nimani-kafolatlaydi-va-nimani-kafolatlamaydi)
- [11.7 Thread-safe to'plamlar: `ConcurrentHashMap`, `CopyOnWriteArrayList` va ularning narxi](#117-thread-safe-toplamlar-concurrenthashmap-copyonwritearraylist-va-ularning-narxi)
- [11.8 `ExecutorService`, thread pool turlari va navbat tanlash](#118-executorservice-thread-pool-turlari-va-navbat-tanlash)
- [11.9 `CompletableFuture` bilan asinxron oqim qurish va xato tarqalishi](#119-completablefuture-bilan-asinxron-oqim-qurish-va-xato-tarqalishi)
- [11.10 Deadlock, livelock va ochlik (starvation): sabab va oldini olish](#1110-deadlock-livelock-va-ochlik-starvation-sabab-va-oldini-olish)
- [11.11 Konkurentlik xatolarini topish: thread dump o'qish](#1111-konkurentlik-xatolarini-topish-thread-dump-oqish)
- [11.12 Amalda qo'llash](#1112-amalda-qollash)

</details>



Konkurentlik kodni tezlashtirmaydi, u kodni qimmatlashtiradi. To'lov servisi sekundiga 2000 so'rovni ko'tarishi uchun ko'p oqimli bo'lishi shart, lekin har bir umumiy o'zgaruvchi, har bir singleton bean maydoni va har bir lock shu narxga qo'shimcha qator qo'shadi. Arxitektor uchun asosiy savol "qanday parallellashtiraman" emas, "qaysi holat umumiy va uni kim qanday tartibda ko'radi" degan savol. Bu bobda JVM ichida nima sodir bo'lishini, Java Memory Model qanday kafolat berishini va Spring konteynerida bu kafolatlar qanday buzilishini ko'rib chiqamiz.

## 11.1 Parallellik va konkurentlik farqi, qaysi muammoni hal qilamiz

Konkurentlik bir nechta ishni bir vaqtda boshqarish haqida, parallellik esa ularni bir vaqtda bajarish haqida. Buyurtma servisi 200 ta so'rovni navbatga olib, bittadan ishlasa, bu konkurent lekin parallel emas. Shu farq muhim, chunki ikki holatda butunlay boshqa muammo hal qilinadi: konkurentlik resursni kutish vaqtini to'ldiradi, parallellik CPU vaqtini qisqartiradi.

Amalda arxitektor ikki qonunga tayanadi. Birinchisi Little qonuni: kerakli bir vaqtdagi ish soni throughput ni latency ga ko'paytirganga teng. Hisobot servisi 500 RPS ni 200 ms latency bilan ushlasa, tizimda doim taxminan 100 ta faol so'rov yashaydi, demak thread pool va DB connection pool shuni ko'tarishi kerak. Ikkinchisi Amdahl qonuni: agar ishning 5 foizi ketma-ket bo'lsa, 32 yadroda maksimal tezlanish taxminan 14 barobar, 64 yadroda esa faqat 15 barobar. Ya'ni bitta global lock ostidagi 5 foizlik kod butun gorizontal o'sishni o'ldiradi.

Shu sababli birinchi qaror doim arxitektura darajasida bo'ladi: umumiy holatni yo'q qilish, bo'lib tashlash yoki tashqi tizimga (PostgreSQL, Redis) ko'chirish. Lock qo'yish uchinchi variant, eng oxirgi variant.

## 11.2 Thread holatlari, kontekst almashinuvi va uning narxi

Java threadining holatlari oltita: NEW, RUNNABLE, BLOCKED, WAITING, TIMED_WAITING, TERMINATED. Bu yerda bitta tuzoq bor: RUNNABLE holati thread CPU da ishlayotganini bildirmaydi. Socket dan o'qiyotgan thread ham RUNNABLE ko'rinadi, chunki JVM OS darajasidagi IO kutishini ajratmaydi. BLOCKED faqat monitor kutishini, WAITING esa `Object.wait`, `LockSupport.park` yoki `Future.get` ni bildiradi.

Platform thread OS threadiga bir-bir mos keladi. Uning stack hajmi 64-bitli HotSpot da odatda 1 MB (`-Xss` bilan sozlanadi), bu heapdan tashqari xotira. 2000 ta thread taxminan 2 GB virtual manzil maydonini oladi, shuning uchun 200 dan ortiq platform thread ishlatish deyarli har doim dizayn xatosi. Kontekst almashinuvi o'zi arzon ko'rinadi (taxminan 1-5 mikrosekund), lekin asl narx L1 va L2 cache ning sovishi: threadning ish to'plami cache dan chiqib ketadi va qayta yuklanadi.

Java 21 dan virtual thread (JEP 444) bu hisobni o'zgartirdi. Virtual thread stacki heapda yashaydi, blokirovka bo'lganda carrier thread dan yechiladi, shuning uchun 100 000 ta virtual thread normal holat. Lekin virtual thread IO uchun, CPU uchun emas: hisob-kitob og'ir bo'lsa, carrier pool (default o'lchami yadro soniga teng) baribir to'yinadi. Spring Boot 3.2 dan `spring.threads.virtual.enabled=true` bilan web va `@Async` ijrochilari virtual threadga o'tadi.

## 11.3 Umumiy holat (shared state) muammosi: poyga sharti va ko'rinuvchanlik

Konkurentlik xatolarining ikki turi bor va ular bir-biriga o'xshamaydi. Poyga sharti (race condition) atomarlik yo'qligidan kelib chiqadi: `balance = balance - amount` uch amaldan iborat, o'rtada boshqa thread kirib ketadi. Ko'rinuvchanlik (visibility) muammosi esa boshqa: bir thread yozgan qiymatni ikkinchi thread hech qachon ko'rmasligi mumkin, chunki qiymat CPU store buffer ida qolgan yoki JIT uni registrga ko'tarib (hoisting) tsikldan chiqarib tashlagan.

Java Memory Model bu yerda happens-before munosabati bilan ishlaydi. Amalda kerakli to'rt qoida: monitor dan chiqish keyingi kirishdan oldin sodir bo'ladi; `volatile` ga yozish keyingi o'qishdan oldin sodir bo'ladi; `Thread.start()` chaqirilishi yangi thread ichidagi hamma ishdan oldin; `Thread.join()` tugashi o'sha thread ishidan keyin. Agar ikki amal orasida happens-before bo'lmasa, JVM ularni istalgan tartibda ko'rsatishga haqli.

Spring da bu eng ko'p singleton bean da yonadi. Default scope singleton, demak bean maydonlari butun ilova bo'ylab umumiy.

```java
@Service
public class OrderTotalService {
    // XATO: singleton bean dagi o'zgaruvchi holat
    private BigDecimal lastTotal = BigDecimal.ZERO;
    // XATO: SimpleDateFormat thread-safe emas
    private final SimpleDateFormat fmt = new SimpleDateFormat("yyyy-MM-dd");

    public String render(Order order) {
        lastTotal = order.total();          // poyga sharti
        return fmt.format(order.createdAt()); // ichki holat buziladi
    }
}

@Service
public class OrderTotalServiceFixed {
    // TO'G'RI: holat metod ichida, formatter immutable
    private static final DateTimeFormatter FMT =
            DateTimeFormatter.ofPattern("yyyy-MM-dd");

    public String render(Order order) {
        BigDecimal total = order.total();   // lokal, stackda
        return FMT.format(order.createdAt());
    }
}
```

Qoida oddiy: singleton bean stateless bo'lsin yoki uning holati faqat immutable obyekt bo'lsin. `SimpleDateFormat`, `Random`, `StringBuilder` va har qanday Hibernate entity bean maydoni sifatida saqlanmaydi.

## 11.4 `synchronized`, `ReentrantLock`, `ReadWriteLock` va `StampedLock` farqi

`synchronized` eng arzon va eng ishonchli variant. HotSpot uni bosqichma-bosqich kuchaytiradi: avval thin lock (CAS bilan object header ga yozish), raqobat paydo bo'lsa inflate qilib monitor obyektiga o'tadi. Raqobatsiz holatda narxi taxminan 20 nanosekund, raqobat bo'lsa yuzlab nanosekundga chiqadi. Kamchiligi: timeout yo'q, uzilishga javob bermaydi, bitta shart o'zgaruvchisi bilan cheklangan.

`ReentrantLock` shu kamchiliklarni yopadi: `tryLock(200, MILLISECONDS)`, `lockInterruptibly()`, bir nechta `Condition`, va `fair=true` rejimi. Fair rejim navbatni kafolatlaydi, lekin throughput ni bir necha barobar tushiradi, shuning uchun uni faqat ochlik real muammo bo'lganda yoqadilar.

`ReentrantReadWriteLock` o'qish ko'p, yozish kam bo'lgan holatga mo'ljallangan. Lekin o'qish lockining o'zi umumiy counter ni CAS bilan yangilaydi, demak 16 yadroda o'qish ham cache line uchun kurashadi. Amalda u faqat kritik bo'lim uzun bo'lganda (mikrosekundlar, nanosekundlar emas) foyda beradi.

`StampedLock` optimistik o'qishni qo'shadi: `tryOptimisticRead` hech narsa yozmaydi, keyin `validate` yozuvchi kirganini tekshiradi. U reentrant emas, `Condition` bermaydi va noto'g'ri ishlatilsa ma'lumot yarim o'qilgan holatda qoladi.

| Mexanizm | Qachon | Narx | Asosiy xavf |
|---|---|---|---|
| `synchronized` | qisqa kritik bo'lim, oddiy holat | eng past, raqobatsiz ~20 ns | timeout yo'q, JDK 23 gacha virtual thread ni pin qiladi |
| `ReentrantLock` | timeout, interrupt, bir nechta Condition kerak | `synchronized` ga yaqin | `unlock` ni `finally` da yozish esdan chiqadi |
| `ReentrantReadWriteLock` | o'qish/yozish nisbati 10:1 dan yuqori, bo'lim uzun | o'qish ham CAS qiladi | yozuvchi ochligi, fair rejim sekin |
| `StampedLock` | juda qisqa o'qish, cache snapshot | optimistik o'qish deyarli 0 | reentrant emas, `validate` tekshirilmasa buzuq ma'lumot |

```java
@Component
public class StockCache {
    private final StampedLock lock = new StampedLock();
    private int warehouseQty;   // ombor qoldig'i snapshot

    public int read() {
        long stamp = lock.tryOptimisticRead();   // lock olmaydi
        int qty = warehouseQty;
        if (!lock.validate(stamp)) {             // yozuvchi kirdimi?
            stamp = lock.readLock();             // pessimistik rejimga tushamiz
            try { qty = warehouseQty; }
            finally { lock.unlockRead(stamp); }
        }
        return qty;
    }

    public void refresh(int qty) {
        long stamp = lock.writeLock();
        try { this.warehouseQty = qty; }
        finally { lock.unlockWrite(stamp); }     // finally bo'lmasa lock abadiy qoladi
    }
}
```

Muhim eslatma: JDK 21-23 da `synchronized` ichida blokirovka bo'lgan virtual thread carrier threadni pin qiladi, JDK 24 da (JEP 491) bu tuzatildi. Agar virtual threadga o'tayotgan bo'lsangiz va JDK 21 da qolsangiz, kutish bo'lgan joyda `ReentrantLock` ishlatish kerak.

## 11.5 Atomic sinflar va CAS: qachon lock dan tezroq

`AtomicInteger`, `AtomicLong` va `AtomicReference` lock ishlatmaydi, ular CPU ning compare-and-swap buyrug'iga tayanadi: eski qiymatni o'qish, yangi qiymatni hisoblash, atomar almashtirish, muvaffaqiyatsiz bo'lsa qaytadan urinish. Raqobat past bo'lganda bu lock dan 2-5 barobar tez. Raqobat yuqori bo'lganda esa teskari effekt: har bir muvaffaqiyatsiz urinish cache line ni boshqa yadrodan tortib oladi, CPU bo'sh aylanadi.

Shu sababli yuqori raqobatli hisoblagich uchun `LongAdder` ishlatiladi. U qiymatni bir nechta cell ga bo'lib tashlaydi, har bir thread o'z cell iga yozadi, `sum()` esa hammasini qo'shadi. 16 yadroda `LongAdder` `AtomicLong` dan taxminan 5-10 barobar tez bo'lishi mumkin, lekin `sum()` aniq snapshot bermaydi.

```java
@Component
public class PaymentMetrics {
    // ko'p yozish, kam o'qish: LongAdder
    private final LongAdder approved = new LongAdder();
    // murakkab holatni atomar almashtirish: AtomicReference + CAS tsikli
    private final AtomicReference<Limits> limits =
            new AtomicReference<>(new Limits(0, BigDecimal.ZERO));

    public void onApproved(BigDecimal amount) {
        approved.increment();
        Limits prev, next;
        do {
            prev = limits.get();
            next = new Limits(prev.count() + 1, prev.sum().add(amount));
        } while (!limits.compareAndSet(prev, next)); // urinish qayta boshlanadi
    }

    public long approvedCount() { return approved.sum(); }
}

// Limits immutable record bo'lishi SHART, aks holda CAS ma'nosiz
record Limits(long count, BigDecimal sum) {}
```

CAS tsiklining shartlari ikkita: almashtiriladigan obyekt immutable bo'lishi va qayta hisoblash yon ta'sirsiz bo'lishi kerak. Agar tsikl ichida DB ga yozsangiz yoki log chiqarsangiz, retry paytida u ikki marta bajariladi.

## 11.6 `volatile` nimani kafolatlaydi va nimani kafolatlamaydi

`volatile` ikki narsani beradi. Birinchisi ko'rinuvchanlik: yozish darhol boshqa threadlarga ko'rinadi, o'qish esa cache dan emas, aktual qiymatdan bo'ladi. Ikkinchisi tartib: `volatile` yozishdan oldingi barcha yozishlar o'sha `volatile` ni o'qigan thread uchun ko'rinadi, bu happens-before chegarasi.

`volatile` bermaydigan narsa esa atomarlik. `volatile int counter; counter++` hamon buzuq, chunki bu o'qish, qo'shish va yozishdan iborat. Shuningdek `volatile` massiv elementlariga ta'sir qilmaydi: `volatile int[] a` da havola volatile, `a[0]` esa yo'q.

Amalda `volatile` uchun ikki to'g'ri holat bor. Birinchisi to'xtatish flagi: background job `volatile boolean running` ni tekshiradi. Buning yo'qligida JIT tsikldan tashqariga ko'tarib tashlaydi va thread hech qachon to'xtamaydi. Ikkinchisi bir marta yoziladigan konfiguratsiya havolasi: feature flag snapshoti yoki qayta yuklanadigan narx jadvali, bunda immutable obyekt butunlay almashtiriladi.

Spring da `@Value` bilan to'ldirilgan maydonlar konstruktor tugaganidan keyin set qilinadi. Agar bean o'z konstruktorida thread ochib yuborsa, o'sha thread yarim initsializatsiya qilingan beanni ko'rishi mumkin. Shuning uchun thread ochish `@PostConstruct` da yoki `SmartLifecycle` da bo'lishi kerak, konstruktorda emas.

## 11.7 Thread-safe to'plamlar: `ConcurrentHashMap`, `CopyOnWriteArrayList` va ularning narxi

`Collections.synchronizedMap` butun map ni bitta monitorga o'raydi, shuning uchun u 4 yadrodan keyin o'smaydi. `ConcurrentHashMap` esa bucket darajasida ishlaydi: bo'sh bucket ga qo'yish CAS bilan, to'lgan bucket ga qo'yish o'sha bucket ning birinchi nodesi ustida `synchronized` bilan. Natijada o'qish deyarli lock siz, yozish esa faqat bir xil bucket ga tushganda raqobatlashadi.

Ikki tuzog'i bor. Birinchisi `size()` va `isEmpty()`: ular bir nechta counter cell ni qo'shadi va aniq snapshot bermaydi, shuning uchun biznes qarorini `size()` ga qurmaslik kerak. Ikkinchisi `computeIfAbsent`: mapping funksiyasi bucket lock ostida bajariladi, demak uning ichida shu map ga yozish yoki uzoq IO qilish deadlock va stall sababi bo'ladi.

```java
@Component
public class RateLimitRegistry {
    private final ConcurrentHashMap<String, LongAdder> hits = new ConcurrentHashMap<>();

    public void hit(String merchantId) {
        // TO'G'RI: mapping funksiyasi arzon va yon ta'sirsiz
        hits.computeIfAbsent(merchantId, k -> new LongAdder()).increment();
    }

    public void wrong(String merchantId) {
        hits.computeIfAbsent(merchantId, k -> {
            // XATO: lock ostida IO va shu map ga qayta murojaat
            Quota q = quotaClient.load(k);        // tashqi HTTP chaqiruv
            hits.put(k + ":meta", new LongAdder()); // rekursiv yozish
            return new LongAdder();
        });
    }
}
```

`CopyOnWriteArrayList` har bir yozishda butun massivni nusxalaydi. 10 000 elementli ro'yxatga bitta qo'shish taxminan 10 000 havolani ko'chiradi, ya'ni O(n). U faqat listener ro'yxati yoki konfiguratsiya ro'yxati kabi "yozish kuniga bir necha marta, o'qish sekundiga minglab" holatida to'g'ri. Buyurtma elementlarini unga yiqqan kod yuklama ostida GC ni bo'g'adi.

## 11.8 `ExecutorService`, thread pool turlari va navbat tanlash

`Executors.newFixedThreadPool` va `newCachedThreadPool` ikkisi ham production uchun xavfli. Birinchisi cheksiz `LinkedBlockingQueue` ishlatadi, demak yuklama oshganda navbat heap ni to'ldiradi va ilova `OutOfMemoryError` bilan yiqiladi, backpressure esa hech qachon ishlamaydi. Ikkinchisi cheksiz thread yaratadi.

To'g'ri yo'l `ThreadPoolExecutor` ni qo'lda sozlash. Asosiy mexanika: avval `corePoolSize` gacha thread yaratiladi, keyin navbat to'ldiriladi, navbat to'lgandan keyingina `maximumPoolSize` gacha yangi thread ochiladi. Shuning uchun cheksiz navbat bilan `maximumPoolSize` hech qachon ishlamaydi. Navbat sig'imi chekli bo'lishi va rad etish siyosati ongli tanlanishi kerak: `CallerRunsPolicy` chaqiruvchini sekinlashtirib backpressure beradi, `AbortPolicy` esa so'rovni tez rad etadi.

Pool kattaligi uchun boshlang'ich formula: CPU og'ir ish uchun yadro soni yoki yadro soni plus bitta; IO og'ir ish uchun yadro soni ni (1 plus kutish vaqti bo'linadi hisob vaqti) ga ko'paytirish. 8 yadroli mashinada so'rov 180 ms kutsa va 20 ms hisoblasa, taxminan 80 thread chiqadi. Lekin bu raqamni DB connection pool cheklaydi: 80 thread 20 ta connection uchun navbatda turadi, shuning uchun pool kattaligi DB pool dan ancha oshmasligi kerak.

```yaml
spring:
  task:
    execution:
      pool:
        core-size: 16
        max-size: 32
        queue-capacity: 500        # cheksiz QOLDIRILMASIN
        keep-alive: 60s
      thread-name-prefix: payment-async-   # thread dump uchun hayotiy muhim
      shutdown:
        await-termination: true
        await-termination-period: 30s   # graceful shutdown
  datasource:
    hikari:
      maximum-pool-size: 20
      connection-timeout: 3000
```

`@Async` ishlatganda yana ikki narsa esda tursin. Birinchisi, `@Async` proxy orqali ishlaydi, demak bir xil bean ichidagi chaqiruv asinxron bo'lmaydi. Ikkinchisi, `@Transactional` tranzaksiyasi yangi threadga ko'chmaydi, chunki tranzaksiya `ThreadLocal` da yashaydi. Shu sababli asinxron metodga entity emas, ID uzatiladi va u o'z tranzaksiyasini ochadi. Xuddi shu holat `SecurityContextHolder` va `RequestContextHolder` uchun ham amal qiladi.

## 11.9 `CompletableFuture` bilan asinxron oqim qurish va xato tarqalishi

`CompletableFuture` ikki narsani beradi: bir nechta mustaqil chaqiruvni parallel qilish va natijalarni kompozitsiya qilish. Asosiy tuzoq ijrochida: `supplyAsync` ni Executor siz chaqirsangiz, u `ForkJoinPool.commonPool()` ga tushadi, uning parallelligi yadro soni minus bitta (bitta yadroli konteynerda u faqat caller thread da ishlaydi). Bu pool butun JVM uchun umumiy, blokirovka qiladigan HTTP chaqiruv uni to'liq to'xtatadi.

Xato tarqalishi ham o'ziga xos. Zanjirdagi istisno `CompletionException` ichiga o'raladi, `join()` uni unchecked qilib otadi, `get()` esa `ExecutionException` qiladi. `exceptionally` xatoni qiymatga aylantiradi, `handle` ikkisini ham ko'radi, `whenComplete` esa natijani o'zgartirmaydi va xatoni yutmaydi. `allOf` birinchi xatoda ham hamma future tugashini kutadi, lekin natijasi `Void`, shuning uchun qiymatlarni alohida olish kerak.

```java
public OrderView load(long orderId, Executor ioPool) {
    var order = CompletableFuture.supplyAsync(() -> orderRepo.find(orderId), ioPool);
    var stock = CompletableFuture.supplyAsync(() -> stockClient.check(orderId), ioPool)
            .orTimeout(800, TimeUnit.MILLISECONDS)     // har bir shoxga timeout
            .exceptionally(ex -> Stock.unknown());      // degradatsiya, oqim o'lmaydi

    return order.thenCombine(stock, OrderView::of)
            .handle((view, ex) -> {
                if (ex != null) {
                    // ex ALBATTA CompletionException ichida keladi
                    log.warn("order view xatosi", ex.getCause());
                    return OrderView.partial(orderId);
                }
                return view;
            })
            .join();   // join unchecked otadi, get esa checked
}
```

Arxitektorning qarori shu yerda: qaysi shox majburiy va qaysi shox degradatsiyaga ruxsat beradi. Ombor qoldig'i noma'lum bo'lsa sahifa ko'rsatiladi, to'lov holati noma'lum bo'lsa esa ko'rsatilmaydi. Bu qaror kodda `exceptionally` bor yoki yo'qligi bilan ifodalanadi.

## 11.10 Deadlock, livelock va ochlik (starvation): sabab va oldini olish

Deadlock to'rt shart bir vaqtda bajarilganda yuzaga keladi: o'zaro istisno, lockni ushlab turib ikkinchisini kutish, lockni tortib olish imkonsizligi, va aylana kutish. Amalda eng ko'p uchraydigani aylana: bitta thread hisob A ni keyin B ni lock qiladi, ikkinchisi teskari tartibda. Yechim eng oddiy shartni buzish: lock olish tartibini global qilib belgilash, masalan hisob ID si bo'yicha o'sish tartibida.

Livelock da threadlar bloklanmaydi, lekin ish ham bitmaydi: ikkisi ham CAS da muvaffaqiyatsiz bo'lib qaytadan urinadi yoki ikkisi ham `tryLock` dan voz kechib qayta boshlaydi. Retry ga tasodifiy kechikish (jitter) qo'shish buni yechadi. Ochlik esa doim bir xil thread navbatga tushmasligi: `ReadWriteLock` da o'quvchilar uzluksiz kelsa, yozuvchi yillab kutadi.

| Tuzoq | Nima bo'ladi | Yechim |
|---|---|---|
| Ikki hisob o'rtasida teskari lock tartibi | aylana deadlock, thread dump da "Found one Java-level deadlock" | lockni ID bo'yicha tartiblab olish yoki bitta DB tranzaksiyasiga ko'chirish |
| `synchronized` ichida DB yoki HTTP chaqiruvi | lock timeout siz ushlanadi, pool to'yinadi | IO ni kritik bo'limdan tashqariga chiqarish |
| Lock ni bir nechta instansiyada ishlatish | horizontal scale da kafolat yo'qoladi | PostgreSQL advisory lock yoki `SELECT ... FOR UPDATE` |
| Cheksiz navbatli pool | OOM, backpressure yo'q | `queue-capacity` cheklash plus `CallerRunsPolicy` |
| `@Transactional` metodni `@Async` qilish | tranzaksiya ko'chmaydi, lazy maydon `LazyInitializationException` | entity emas, ID uzatish va yangi tranzaksiya ochish |
| `ThreadLocal` ni pool da tozalamaslik | ma'lumot boshqa so'rovga oqadi, memory leak | `finally` da `remove()`, filtrda tozalash |
| DB pool thread pool dan kichik | threadlar connection kutib WAITING da qotadi | pool nisbatini birgalikda sozlash |
| Uzun tranzaksiya ichida lock | PostgreSQL da qulf navbati, `lock_timeout` yo'q | tranzaksiyani qisqartirish, `lock_timeout` qo'yish |

```sql
-- Bir nechta instansiya uchun JVM lock ishlamaydi, advisory lock ishlaydi
-- Tranzaksiya tugashi bilan avtomatik bo'shaydi
BEGIN;
SET LOCAL lock_timeout = '2s';            -- abadiy kutishni taqiqlaymiz
SELECT pg_advisory_xact_lock(hashtext('payout-batch-2026-10'));
UPDATE payout SET status = 'SENT' WHERE batch_id = 42 AND status = 'NEW';
COMMIT;

-- Deadlock oldini olish: qatorlarni DOIM bir xil tartibda qulflash
BEGIN;
SELECT id, balance FROM account
 WHERE id IN (1001, 1002)
 ORDER BY id                               -- tartib global va barqaror
   FOR UPDATE;
COMMIT;
```

## 11.11 Konkurentlik xatolarini topish: thread dump o'qish

Konkurentlik xatosi debugger da takrorlanmaydi, shuning uchun asosiy quroling thread dump. `jcmd <pid> Thread.print` bir zumda hamma threadning stackini beradi, JDK 21 dan `Thread.dump_to_file -format=json` virtual threadlarni ham ko'rsatadi. Qoida: bitta dump hech narsa aytmaydi, 2-3 sekund oraliq bilan uchta dump olish kerak va bir xil joyda qotgan threadlarni solishtirish kerak.

```bash
# PID ni topish va uchta dump olish
PID=$(jcmd -l | grep payment-service | awk '{print $1}')
for i in 1 2 3; do jcmd $PID Thread.print > /tmp/dump-$i.txt; sleep 2; done

# Holatlar bo'yicha sanash: BLOCKED ko'p bo'lsa lock raqobati bor
grep -c 'java.lang.Thread.State: BLOCKED' /tmp/dump-2.txt
grep -A2 'waiting to lock' /tmp/dump-2.txt | head -40

# JVM deadlockni o'zi topadi va dump oxirida yozadi
grep -A30 'Found one Java-level deadlock' /tmp/dump-2.txt

# Virtual threadlar uchun (JDK 21+)
jcmd $PID Thread.dump_to_file -format=json /tmp/vthreads.json
```

Dump da uch naqshni qidirasiz. Birinchisi `BLOCKED` plus `waiting to lock <0x000000071ab...>` plus boshqa threadda `locked <0x000000071ab...>`: shu ikki satr lock egasini ko'rsatadi. Ikkinchisi ko'p threadning `HikariPool.getConnection` da `TIMED_WAITING` turishi: bu lock muammosi emas, DB pool yetishmasligi. Uchinchisi bitta thread uzoq vaqt bir xil stackda `RUNNABLE` turishi: cheksiz tsikl yoki CPU og'ir ish.

Shu sababli `thread-name-prefix` ni har bir pool uchun ma'noli qo'yish kerak. `pool-3-thread-7` dump da hech narsa aytmaydi, `payment-async-7` esa darhol qaysi pool to'yinganini ko'rsatadi.

| Savol | Oddiy yondashuv | Arxitektor yondashuvi |
|---|---|---|
| Umumiy holat kerakmi | bean ga maydon qo'shiladi | holat stateless qilinadi yoki PostgreSQL ga ko'chiriladi |
| Tezlik kerak bo'lsa | `synchronized` qo'yiladi | kritik bo'lim o'lchanadi, CAS yoki immutable snapshot tanlanadi |
| Pool kattaligi | `newFixedThreadPool(50)` | Little qonuni bilan hisoblanadi va DB pool bilan moslanadi |
| Navbat | default cheksiz navbat | chekli `queue-capacity` plus ongli rad etish siyosati |
| Asinxron chaqiruv | `@Async` qo'yiladi va kutiladi | tranzaksiya va security context chegarasi aniq belgilanadi |
| Xato | `exceptionally` yozilmaydi | har bir shox uchun timeout va degradatsiya qarori bor |
| Lock ko'lami | JVM lock yetarli deb hisoblanadi | bir nechta instansiya uchun advisory lock yoki `FOR UPDATE` |
| Tekshirish | lokalda bir marta ishlatib ko'riladi | yuklama ostida thread dump olinadi, pool metrikasi kuzatiladi |
| Hisoblagich | `AtomicLong` | raqobat yuqori bo'lsa `LongAdder`, aniqlik kerak bo'lsa DB |
| Kuzatuv | log qo'yiladi | pool ning active, queued va rejected metrikalari dashboardda |

Konkurentlikni testlash alohida mavzu, [testlash qo'llanmasidagi](../testing/README.md) asinxron va konkurentlik testlari bo'limi unga bag'ishlangan. Bu yerda muhimi shuki, bitta ham konkurentlik qarori o'lchovsiz qabul qilinmaydi: har bir lock ortida raqobat metrikasi, har bir pool ortida navbat uzunligi grafigi turishi kerak.

## 11.12 Amalda qo'llash

- [ ] Hamma singleton bean larni ko'rib chiq va o'zgaruvchi maydon topilgan har bir joyni stateless qil yoki immutable obyektga almashtir; `SimpleDateFormat` va `Random` maydonlarini alohida qidir.
- [ ] `Executors.newFixedThreadPool` va `newCachedThreadPool` chaqiruvlarini loyihada qidirib, ularni chekli `queue-capacity` va ongli rad etish siyosatiga ega `ThreadPoolExecutor` ga ko'chir.
- [ ] Har bir pool ga ma'noli `thread-name-prefix` qo'y va `graceful shutdown` uchun `await-termination-period` ni 30 soniyaga sozla.
- [ ] Thread pool kattaligini Little qonuni bilan hisobla, natijani Hikari `maximum-pool-size` bilan solishtir va nisbat teskari bo'lmasligini tasdiqla.
- [ ] `@Async` va `@Transactional` birga ishlatilgan joylarni topib, entity uzatish o'rniga ID uzatishga o'tkaz; `SecurityContextHolder` ga tayangan asinxron kodni alohida belgila.
- [ ] Bir nechta instansiyada ishlaydigan har qanday `synchronized` blokni aniqla va uni PostgreSQL advisory lock yoki `SELECT ... FOR UPDATE` ga ko'chir, `lock_timeout` ni albatta qo'y.
- [ ] Yuklama testi paytida 2 sekund oraliq bilan uchta thread dump olib, `BLOCKED` threadlar sonini va lock egalarini qaydnomaga yozib qo'y.
- [ ] Pool metrikalarini (active, queue size, rejected, completed) Micrometer orqali chiqarib, navbat uzunligi va rad etish soniga alert qo'y.

---

[&larr; 10. Garbage collection va xotira sozlash](10-garbage-collection-va-xotira-sozlash.md) · [Mundarija](README.md) · [12. Virtual threads, structured concurrency va scoped values &rarr;](12-virtual-threads-structured-concurrency-va.md)
