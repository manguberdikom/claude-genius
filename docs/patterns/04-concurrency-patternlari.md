<!-- doc: patterns | chapter: 4 | part:  -->

[Barcha hujjatlar](../../README.md) / [Dizayn patternlar](README.md)

> Holat: tekshirilgan (2026-10-19). Manbalar bob oxirida.

# 4. Concurrency patternlari (Concurrency Patterns)

<details>
<summary>Bu bobdagi 36 bo'lim</summary>

- [4.1 Oqimlar hovuzi / Bajaruvchi (Thread Pool / Executor)](#41-oqimlar-hovuzi--bajaruvchi-thread-pool--executor)
- [4.2 Ishlab chiqaruvchi-Iste'molchi (Producer-Consumer)](#42-ishlab-chiqaruvchi-istemolchi-producer-consumer)
- [4.3 Kelasi natija / Vada (Future / Promise / CompletableFuture)](#43-kelasi-natija--vada-future--promise--completablefuture)
- [4.4 Faol obyekt (Active Object)](#44-faol-obyekt-active-object)
- [4.5 Monitor obyekti (Monitor Object)](#45-monitor-obyekti-monitor-object)
- [4.6 Reaktor (Reactor)](#46-reaktor-reactor)
- [4.7 Proaktor (Proactor)](#47-proaktor-proactor)
- [4.8 Yarim-sinxron/Yarim-asinxron (Half-Sync/Half-Async)](#48-yarim-sinxronyarim-asinxron-half-synchalf-async)
- [4.9 Yetakchi/Izdoshlar (Leader/Followers)](#49-yetakchiizdoshlar-leaderfollowers)
- [4.10 O'qish-yozish lock'i (Read-Write Lock)](#410-oqish-yozish-locki-read-write-lock)
- [4.11 Ikki marta tekshirilgan lock (Double-Checked Locking)](#411-ikki-marta-tekshirilgan-lock-double-checked-locking)
- [4.12 Shart bilan to'xtatish (Guarded Suspension)](#412-shart-bilan-toxtatish-guarded-suspension)
- [4.13 Rad etib qaytish (Balking)](#413-rad-etib-qaytish-balking)
- [4.14 Rejalashtiruvchi (Scheduler)](#414-rejalashtiruvchi-scheduler)
- [4.15 Thread'ga xos saqlash (Thread-Specific Storage)](#415-threadga-xos-saqlash-thread-specific-storage)
- [4.16 O'zgarmas obyekt (Immutable Object)](#416-ozgarmas-obyekt-immutable-object)
- [4.17 Barrier va sanoqli kutish (Barrier / CountDownLatch / Phaser)](#417-barrier-va-sanoqli-kutish-barrier--countdownlatch--phaser)
- [4.18 Fork-Join va ishni o'g'irlash (Fork-Join / Work Stealing)](#418-fork-join-va-ishni-ogirlash-fork-join--work-stealing)
- [4.19 Actor modeli (Actor Model)](#419-actor-modeli-actor-model)
- [4.20 Lock'larni bo'lish (Lock Striping)](#420-locklarni-bolish-lock-striping)
- [4.21 Compare-And-Swap va lock-free algoritmlar (Compare-And-Swap / Lock-Free)](#421-compare-and-swap-va-lock-free-algoritmlar-compare-and-swap--lock-free)
- [4.22 So'rovga bitta thread va event loop (Thread-per-request vs Event Loop)](#422-sorovga-bitta-thread-va-event-loop-thread-per-request-vs-event-loop)
- [4.23 Virtual thread'lar (Virtual Threads)](#423-virtual-threadlar-virtual-threads)
- [4.24 Strukturaviy concurrency (Structured Concurrency)](#424-strukturaviy-concurrency-structured-concurrency)
- [4.25 Qamrovli qiymatlar (Scoped Values)](#425-qamrovli-qiymatlar-scoped-values)
- [4.26 Asinxron metod chaqiruvi (Asynchronous Method Invocation)](#426-asinxron-metod-chaqiruvi-asynchronous-method-invocation)
- [4.27 Semaphore va concurrency chegarasi (Semaphore / Concurrency Limit)](#427-semaphore-va-concurrency-chegarasi-semaphore--concurrency-limit)
- [4.28 Nusxaga qamash (Instance Confinement)](#428-nusxaga-qamash-instance-confinement)
- [4.29 Thread xavfsizligini delegatsiya qilish (Delegating Thread Safety)](#429-thread-xavfsizligini-delegatsiya-qilish-delegating-thread-safety)
- [4.30 Mijoz tomonida qulflash va kompozitsiya o'rami (Client-Side Locking / Composition)](#430-mijoz-tomonida-qulflash-va-kompozitsiya-orami-client-side-locking--composition)
- [4.31 Natija keshi (Memoizer / Result Cache)](#431-natija-keshi-memoizer--result-cache)
- [4.32 Ketma-ket thread qamashi va ownership uzatish (Serial Thread Confinement)](#432-ketma-ket-thread-qamashi-va-ownership-uzatish-serial-thread-confinement)
- [4.33 Zahar tabletka (Poison Pill)](#433-zahar-tabletka-poison-pill)
- [4.34 Ochiq chaqiruv (Open Call)](#434-ochiq-chaqiruv-open-call)
- [4.35 Treiber steki: bloklanmaydigan stek (Treiber Stack / Non-blocking Stack)](#435-treiber-steki-bloklanmaydigan-stek-treiber-stack--non-blocking-stack)
- [4.36 Amalda qo'llash](#436-amalda-qollash)

</details>



Concurrency patternlari ko'p oqimli (multi-threaded) va asinxron tizimlarda ishni oqimlar o'rtasida taqsimlash, umumiy holatni (shared state) xavfsiz himoyalash va kutish/bloklanishni boshqarishning takrorlanuvchi yechimlarini beradi. Java va Spring ekosistemasi bu patternlarning ko'pini tilning o'zida (`java.util.concurrent`, virtual threadlar) yoki framework darajasida (`TaskExecutor`, `@Async`, WebFlux, Netty event loop) allaqachon amalga oshirgan - arxitektorning vazifasi ularni noldan yozish emas, balki to'g'ri qatlamda to'g'risini tanlash. Noto'g'ri tanlov odatda kompilyatsiya xatosi bilan emas, yuklama ostida thread pool tugashi, deadlock, latency dumining (tail latency) o'sishi yoki ma'lumot buzilishi bilan namoyon bo'ladi. Shuning uchun bu bo'lim arxitektor uchun eng "qimmat" bo'limlardan biri: bu yerdagi qarorlar tizimning throughput, barqarorlik va diagnostika qulayligini uzoq muddatga belgilaydi.

## 4.1 Oqimlar hovuzi / Bajaruvchi (Thread Pool / Executor)

**Tavsif:** Har bir vazifa uchun yangi thread yaratish qimmat va cheklovsiz - bu pattern oldindan tayyorlangan oqimlar to'plamini saqlab, vazifalarni navbat orqali ularga topshiradi. Vazifani yuborish (submit) bajarilishdan ajratiladi, shu bilan thread yaratish narxi amortizatsiya qilinadi va parallellik darajasi yuqoridan cheklanadi. Hovuz o'lchami, navbat turi va to'lib qolgandagi rad etish siyosati (rejection policy) tizimning yuklama ostidagi xatti-harakatini belgilaydi.

**Spring'da qayerda uchraydi:** Java tomonida `java.util.concurrent.ExecutorService`, `ThreadPoolExecutor`, `Executors`, `ForkJoinPool.commonPool()` va Java 21+ dagi `Executors.newVirtualThreadPerTaskExecutor()`. Spring Framework 6.x/7.x `org.springframework.core.task.TaskExecutor` abstraksiyasini, `ThreadPoolTaskExecutor`, `SimpleAsyncTaskExecutor` (virtual threadlarni `setVirtualThreads(true)` bilan qo'llaydi) va `ConcurrentTaskExecutor` implementatsiyalarini beradi; `@EnableAsync` + `@Async` proxy orqali metod chaqiruvini shu executorga uzatadi. Spring Boot 3.x/4.x `spring.task.execution.pool.core-size`, `max-size`, `queue-capacity` propertylari bilan `applicationTaskExecutor` beanini avtomatik sozlaydi, `spring.threads.virtual.enabled=true` esa web konteyner va task executorlarni virtual threadlarga o'tkazadi.

**Qo'llanish keyslari:**
- REST controller'da yuborilgan email yoki audit yozuvini `@Async` bilan fon oqimida bajarish.
- Katta hisobotni bir nechta bo'lakka bo'lib `ExecutorService.invokeAll()` orqali parallel hisoblash.
- Tashqi API'ga ko'p sonli mustaqil chaqiruvlarni cheklangan parallellik bilan yuborish.
- Tomcat/Jetty uchun `server.tomcat.threads.max` orqali request bajaruvchi hovuzini kapasitetga moslash.
- Spring Batch'da `TaskExecutorPartitionHandler` bilan partition'larni parallel ishga tushirish.

**Ehtiyot bo'ling:** Cheksiz `LinkedBlockingQueue` bilan `max-size` hech qachon ishlamaydi - navbat o'sib OOM'ga olib keladi va backpressure yo'qoladi; `CallerRunsPolicy` yoki chegaralangan navbat tanlang. Platform threadli hovuzda bloklanuvchi I/O'ni ko'paytirish thread starvation beradi: bunday ishni virtual threadlarga yoki alohida ajratilgan (bulkhead) hovuzga chiqarish kerak.

```java
@Bean
ThreadPoolTaskExecutor reportExecutor() {
    ThreadPoolTaskExecutor ex = new ThreadPoolTaskExecutor();
    ex.setCorePoolSize(8);
    ex.setMaxPoolSize(8);              // core = max: pool "pulsatsiya" qilmaydi
    ex.setQueueCapacity(200);          // chegarasiz navbat = xotira tugashi
    ex.setThreadNamePrefix("report-"); // thread dump o'qilishi uchun
    ex.setRejectedExecutionHandler(new ThreadPoolExecutor.AbortPolicy());
    ex.setTaskDecorator(new ContextPropagatingTaskDecorator()); // MDC va trace
    return ex;
}
```

## 4.2 Ishlab chiqaruvchi-Iste'molchi (Producer-Consumer)

**Tavsif:** Ishni yaratuvchi va uni qayta ishlovchi komponentlar o'rtasiga navbat qo'yiladi, shu bilan ular bir-biridan vaqt va tezlik jihatidan ajratiladi. Chegaralangan navbat tabiiy backpressure beradi: navbat to'lsa producer sekinlashadi yoki rad etiladi. Iste'molchilar sonini o'zgartirib, qayta ishlash quvvatini yuklamaga moslash mumkin.

**Spring'da qayerda uchraydi:** Java'da `BlockingQueue` ierarxiyasi - `ArrayBlockingQueue`, `LinkedBlockingQueue`, `SynchronousQueue`, `LinkedTransferQueue`, `DelayQueue`; yuqori throughput uchun LMAX Disruptor. Spring Integration'da `QueueChannel`, `PriorityChannel` va `PollerMetadata` bilan sozlanadigan polling consumer; Spring Kafka'da `@KafkaListener` + `ConcurrentMessageListenerContainer` (`concurrency` parametri), Spring AMQP'da `SimpleMessageListenerContainer`/`DirectMessageListenerContainer`. Reaktiv tomonda Project Reactor'ning `Sinks.many()` va `Flux.onBackpressureBuffer()` xuddi shu rolni bajaradi.

**Qo'llanish keyslari:**
- Fayl yuklash endpointi yuklangan faylni navbatga qo'yadi, alohida worker'lar uni parse qiladi.
- Kafka topic'dan kelgan buyurtmalarni `concurrency=6` bilan parallel iste'mol qilish.
- Log/metrik hodisalarini navbatga yozib, batch holida tashqi tizimga yuborish.
- Elektron pochta yoki push notification yuborishni navbat orqali rate'ga moslash.
- ETL oqimida o'qish, transformatsiya va yozish bosqichlarini mustaqil tezlikda ishlatish.

**Ehtiyot bo'ling:** Navbat ichidagi elementlar JVM o'chganda yo'qoladi - "ishonchli" yetkazib berish kerak bo'lsa in-memory queue emas, broker yoki transactional outbox ishlatilsin. Poison message yoki sekin consumer navbatni to'ldirib butun pipeline'ni to'xtatishi mumkin, shuning uchun dead-letter va timeout majburiy.

```java
// Producer-Consumer: chegaralangan navbat backpressure beradi
private final BlockingQueue<Job> queue = new ArrayBlockingQueue<>(1_000);

void produce(Job job) throws InterruptedException {
    if (!queue.offer(job, 200, TimeUnit.MILLISECONDS)) {
        throw new QueueFullException();   // kutib qolmaydi, tez xato
    }
}

void consume() throws InterruptedException {
    while (!Thread.currentThread().isInterrupted()) {
        Job job = queue.take();           // bo'sh bo'lsa kutadi
        process(job);
    }
}
```

## 4.3 Kelasi natija / Vada (Future / Promise / CompletableFuture)

**Tavsif:** Asinxron hisoblashning natijasini hozir mavjud bo'lmagan, lekin keyin tayyor bo'ladigan obyekt sifatida ifodalaydi. `Future` faqat natijani kutish (pull) imkonini beradi, `CompletableFuture` esa callback va kompozitsiya (`thenApply`, `thenCompose`, `allOf`) orqali chaqiruvchini bloklamasdan quvur qurishga ruxsat beradi. Bu bir nechta mustaqil chaqiruvni parallel bajarib, umumiy latency'ni eng sekin chaqiruv darajasiga tushiradi.

**Spring'da qayerda uchraydi:** `java.util.concurrent.Future`, `CompletableFuture`, `CompletionStage`. Spring 6.x'da `@Async` metodi `void`, `Future` yoki `CompletableFuture` qaytaradi - eski `ListenableFuture` va `AsyncResult` olib tashlangan/deprecated, o'rniga `CompletableFuture.completedFuture(...)` ishlatiladi. Spring MVC'da `Callable`, `DeferredResult` va `CompletableFuture` controller qaytaruv turi sifatida qo'llanadi; `WebClient` `Mono`/`Flux` qaytaradi va `toFuture()` bilan `CompletableFuture`'ga o'tadi; Reactor'ning `Mono` - promise'ning lazy va cancel qilinadigan muqobili. Java 21+ `StructuredTaskScope` (preview) bir nechta subtask'ni bitta scope ichida boshqarishni beradi.

```java
CompletableFuture<User> u = CompletableFuture.supplyAsync(() -> userClient.find(id), executor);
CompletableFuture<List<Order>> o = CompletableFuture.supplyAsync(() -> orderClient.byUser(id), executor);
return u.thenCombine(o, UserProfile::new)
        .orTimeout(2, TimeUnit.SECONDS)
        .exceptionally(ex -> UserProfile.fallback(id));
```

**Qo'llanish keyslari:**
- Bir sahifa uchun uch xil mikroservisdan ma'lumotni parallel olib, `allOf` bilan birlashtirish.
- Sekin tashqi chaqiruvga `orTimeout` va `exceptionally` bilan fallback qo'shish.
- `DeferredResult` orqali long-polling endpoint qurish, servlet threadini bo'shatib.
- Cache miss bo'lganda qiymatni asinxron yuklab, `thenAccept` bilan cache'ga yozish.
- Fon vazifasining tugashini `@Async` natijasi orqali kuzatish va xatosini log qilish.

**Ehtiyot bo'ling:** `get()` yoki `join()` chaqirish asinxronlikni yo'q qiladi va ayni o'sha hovuzda chaqirilsa deadlock keltirib chiqaradi; `ForkJoinPool.commonPool()` ni bloklanuvchi I/O bilan band qilmang, o'z executoringizni bering. Istisnolar yutilib ketmasligi uchun har bir zanjirning oxirida `exceptionally`/`whenComplete` bo'lishi shart.

## 4.4 Faol obyekt (Active Object)

**Tavsif:** Metod chaqiruvini uning bajarilishidan ajratadi: client oddiy metod chaqiradi, lekin chaqiruv so'rov obyektiga aylanib navbatga tushadi va obyektning o'ziga tegishli bitta scheduler oqimida ketma-ket bajariladi. Natijada obyektning ichki holati faqat bitta oqim tomonidan o'zgartiriladi va lock'lar shart bo'lmaydi. Client natijani `Future` orqali oladi, shu bilan interfeys sinxron ko'rinishini saqlaydi.

**Spring'da qayerda uchraydi:** Eng toza Java ko'rinishi - bitta oqimli `Executors.newSingleThreadExecutor()` ustida qurilgan fasad, `submit()` natijasini `Future` qilib qaytaradigan. Spring'da `@Async` + `AsyncAnnotationBeanPostProcessor` tomonidan yaratilgan proxy aynan shu ajratishni amalga oshiradi (lekin ketma-ketlikni kafolatlash uchun bitta oqimli executor berish kerak). Spring Integration'ning `@MessagingGateway` interfeysi POSA'dagi proxy + so'rov navbati rolini bajaradi; aktor modelidagi muqobillar - Akka/Apache Pekko `typed.ActorRef` yoki Vert.x verticle'lari. Reaktiv dunyoda `Flux` ni bitta `Schedulers.single()` ga `publishOn` qilish ham xuddi shu seriyalashtirishni beradi.

**Qo'llanish keyslari:**
- Thread-safe bo'lmagan tashqi SDK klientini bitta oqim ortiga yashirish.
- Qurilma yoki serial port bilan ishlashda buyruqlarni ketma-ket navbatlash.
- In-memory order book yoki o'yin sessiyasi holatini lock'siz, bitta oqimda boshqarish.
- Narx jadvali kabi tez-tez yangilanadigan aggregatni seriyalashtirib yangilash.
- Audit yoki hodisa jurnalini bitta writer orqali tartibda yozish.

**Ehtiyot bo'ling:** Bitta oqim bo'g'iz (bottleneck) bo'lib qoladi - og'ir CPU ishi yoki bloklanuvchi chaqiruv butun navbatni to'xtatadi. Navbat chegarasiz bo'lsa yuklama ostida xotira o'sadi va latency ko'rinmas tarzda oshib ketadi.

```java
// Active Object: chaqiruv navbatga tushadi, o'z thread'ida bajariladi
@Component
public class LedgerActor {
    private final ExecutorService worker = Executors.newSingleThreadExecutor();
    private BigDecimal balance = BigDecimal.ZERO;   // lock kerak emas: bitta thread

    public CompletableFuture<BigDecimal> credit(BigDecimal amount) {
        return CompletableFuture.supplyAsync(() -> balance = balance.add(amount), worker);
    }

    @PreDestroy
    void shutdown() { worker.shutdown(); }
}
```

## 4.5 Monitor obyekti (Monitor Object)

**Tavsif:** Obyektning umumiy holatiga kirishni bitta mutex bilan seriyalashtiradi va shart bajarilmaganda oqimni shu monitor ichida kutishga qo'yadi. Ya'ni "o'zaro istisno" (mutual exclusion) va "shartli kutish" (condition wait) bir obyektda jamlanadi: bir vaqtda faqat bitta metod ishlaydi, kutayotgan oqim lock'ni bo'shatib turadi. Bu Java'ga tilning o'ziga singdirilgan eng asosiy sinxronlash patterni.

**Spring'da qayerda uchraydi:** Java'da `synchronized` metod/blok, `Object.wait()/notifyAll()` va aniqroq muqobil - `java.util.concurrent.locks.ReentrantLock` + `Condition.await()/signalAll()`. Spring'ning o'zida `DefaultSingletonBeanRegistry` singleton registrini, `ConcurrentWebSocketSessionDecorator` esa session yozishni monitor orqali himoyalaydi; `@Scope("singleton")` beanlar bo'lsa, mutable maydonlari bo'lsa, shu patternni yoki `ConcurrentHashMap`/`Atomic*` ni talab qiladi. Spring Integration va Spring AMQP container'lari lifecycle (`start()/stop()`) ni `lifecycleMonitor` obyekti ustida synchronized qiladi.

**Qo'llanish keyslari:**
- Singleton bean ichidagi mutable counter yoki konfiguratsiya snapshotini himoyalash.
- Chegaralangan bufferni `Condition` bilan "bo'sh emas"/"to'la emas" shartlari ustida qurish.
- Komponent `start()`/`stop()` hayot tsiklini ikki marta ishga tushishdan saqlash.
- Faylga yoki WebSocket session'ga yozishni bitta yozuvchiga seriyalashtirish.
- Lazy ravishda yuklanadigan og'ir resursni bir marta initsializatsiya qilish.

**Ehtiyot bo'ling:** `synchronized` blok ichida tashqi tarmoq chaqiruvi yoki boshqa lock olish deadlock va uzun lock contention manbai - kritik bo'limni minimal ushlang va lock'larni doim bir xil tartibda oling. Virtual threadlarda `synchronized` Java 24+ da endi carrier threadni pinlamaydi (JEP 491), lekin eski JDK'larda pinlaydi - bunday hollarda `ReentrantLock` xavfsizroq.

```java
// Monitor Object: holat va uni qo'riqlovchi lock bitta obyektda
public class BoundedCounter {
    private final Object lock = new Object();   // ichki, tashqariga chiqmaydi
    private int value;

    public void increment() {
        synchronized (lock) { value++; }        // ichida I/O yo'q
    }

    public int get() {
        synchronized (lock) { return value; }
    }
}
```

## 4.6 Reaktor (Reactor)

**Tavsif:** Bitta (yoki bir nechta) oqim ko'plab I/O manbalarini event demultiplexer orqali kuzatadi va tayyor bo'lgan hodisani mos handler'ga sinxron uzatadi. Ulanish soniga emas, hodisa soniga proporsional resurs ishlatilgani uchun o'n minglab bir vaqtli ulanishni kam thread bilan boshqarish mumkin. Handler'lar hech qachon bloklanmasligi - patternning asosiy shartidir.

**Spring'da qayerda uchraydi:** Java NIO'dagi `Selector`, `SelectionKey`, `SocketChannel` - klassik reaktor mexanizmi. Netty'dagi `EventLoopGroup`/`NioEventLoop` va `ChannelPipeline` shu patternning sanoat standarti; Spring WebFlux standart holda Reactor Netty ustida ishlaydi va `HttpHandler`/`WebFilter` zanjirini event loop oqimlarida bajaradi. Project Reactor (`Mono`, `Flux`, `Schedulers`) hodisalarni kompozitsiya qilish qatlamini beradi; `WebClient`, Spring Data R2DBC va Spring Data Reactive Redis ham shu modelga tayanadi. Undertow (XNIO) va Tomcat'ning NIO connector'i ham reaktor yondashuvidan foydalanadi.

**Qo'llanish keyslari:**
- Minglab SSE yoki WebSocket ulanishini kam thread bilan ushlab turadigan gateway.
- Spring Cloud Gateway orqali yuqori throughputli reverse proxy qurish.
- Ko'p sonli sekin downstream chaqiruvi bo'lgan API aggregator.
- Chat yoki real-time notification servisi.
- IoT qurilmalaridan kelgan uzluksiz telemetriya oqimini qabul qilish.

**Ehtiyot bo'ling:** Event loop oqimida bitta `Thread.sleep()`, JDBC chaqiruvi yoki `block()` butun serverni to'xtatadi - bloklanuvchi ishni `Schedulers.boundedElastic()` ga chiqarish shart. Agar domeningizda blocking kutubxonalar ko'p bo'lsa, WebFlux emas, virtual threadli MVC oddiyroq va diagnostikasi osonroq yechim bo'lishi mumkin.

```java
// Reactor: bitta event loop ko'p ulanishni navbat bilan multipleksirlaydi
@Bean
NettyReactiveWebServerFactory serverFactory() {
    NettyReactiveWebServerFactory f = new NettyReactiveWebServerFactory();
    // event loop thread'lari soni = yadro soni; blocking ish bu yerda bo'lmasligi kerak
    f.addServerCustomizers(server -> server.runOn(LoopResources.create("http", 1,
            Runtime.getRuntime().availableProcessors(), true)));
    return f;
}
// Event loop ichida JDBC yoki Thread.sleep chaqirilsa butun server to'xtaydi
```

## 4.7 Proaktor (Proactor)

**Tavsif:** Reaktordan farqli ravishda operatsiyaning tayyorligi haqida emas, tugallanganligi haqida xabar beradi: dastur asinxron o'qish/yozishni boshlab yuboradi, OS uni bajaradi va natija bilan completion handler'ni chaqiradi. Shu bilan I/O'ni kutish to'liq operatsion tizimga o'tadi va foydalanuvchi kodida kutish nuqtasi qolmaydi. Juda yuqori throughputli I/O uchun samarali, lekin boshqaruv oqimi callback'larga bo'linib ketadi.

**Spring'da qayerda uchraydi:** Java'da NIO.2 API - `AsynchronousSocketChannel`, `AsynchronousServerSocketChannel`, `AsynchronousFileChannel`, `AsynchronousChannelGroup` va `CompletionHandler<V, A>` interfeysi. OS darajasida Windows IOCP va Linux'dagi `io_uring` shu modelga mos; Netty'ning `IoUringEventLoopGroup` (netty-incubator-transport-io_uring) shunga yaqin. Spring Framework'ning o'zi proaktorni bevosita ochib bermaydi - Spring tomonida u Reactor/Netty qatlami ortida yashiringan bo'ladi, ya'ni arxitektor uni ko'proq transport tanlashda va mahalliy kutubxonalarni baholashda hisobga oladi.

**Qo'llanish keyslari:**
- Katta fayllarni `AsynchronousFileChannel` bilan bloklanmasdan o'qib/yozish.
- Juda yuqori ulanish zichligi bo'lgan TCP proxy yoki protokol server yozish.
- Linux'da `io_uring` transportini sinab, tarmoq I/O'dagi syscall yukini kamaytirish.
- Media yoki backup servisida parallel ko'p streamli yozish.
- Mavjud callback'li native kutubxonani `CompletionHandler` orqali JVM'ga integratsiya qilish.

**Ehtiyot bo'ling:** Platformaga bog'liqlik yuqori - bir OS'da tezlik beradigan yechim boshqasida emulyatsiya orqali sekinlashadi, shuning uchun o'lchovsiz tanlamang. Callback zanjirlari xato va timeout boshqaruvini qiyinlashtiradi; aksariyat Spring loyihasi uchun `CompletableFuture`/Reactor abstraksiyasi ostida qolish to'g'ri qaror.

```java
// Proactor: amal tugaganda callback chaqiriladi (haqiqiy asinxron I/O)
AsynchronousFileChannel ch = AsynchronousFileChannel.open(path, READ);
ByteBuffer buf = ByteBuffer.allocate(8192);

ch.read(buf, 0, buf, new CompletionHandler<Integer, ByteBuffer>() {
    @Override public void completed(Integer read, ByteBuffer b) {
        b.flip();                     // OS o'qishni tugatgandan keyin chaqiriladi
        handle(b);
    }
    @Override public void failed(Throwable t, ByteBuffer b) { log.error("o'qish xatosi", t); }
});
```

## 4.8 Yarim-sinxron/Yarim-asinxron (Half-Sync/Half-Async)

**Tavsif:** Tizimni ikki qatlamga bo'ladi: asinxron qatlam hodisalarni tez qabul qiladi va navbatga qo'yadi, sinxron qatlamdagi worker oqimlar esa ularni tushunarli, bloklanishi mumkin bo'lgan kod bilan qayta ishlaydi. Ikki qatlam o'rtasidagi navbat ularni ajratib, asinxron qismning tezligini yo'qotmasdan biznes mantiqni oddiy yozishga imkon beradi. Bu amaliyotdagi eng ko'p uchraydigan murosali pattern.

**Spring'da qayerda uchraydi:** Servlet konteynerlari aynan shunday ishlaydi: Tomcat'ning NIO acceptor/poller oqimlari ulanishni asinxron qabul qiladi, so'ngra so'rovni `http-nio-*-exec-*` worker hovuziga topshiradi. Spring MVC'da `Callable`, `DeferredResult` va `WebAsyncTask` so'rovni servlet threadidan ajratib, `AsyncTaskExecutor` ga uzatadi (Servlet 3.1+ async). Spring WebFlux'da chegara `publishOn(Schedulers.boundedElastic())` yoki `Mono.fromCallable(...).subscribeOn(...)` orqali qo'yiladi - masalan reaktiv controller ichidan blocking JPA chaqirilganda. Spring Kafka/AMQP container'lari ham xabarni asinxron oladi, qayta ishlashni listener hovuziga beradi.

**Qo'llanish keyslari:**
- WebFlux endpointidan eski blocking JDBC repository'ni `boundedElastic` orqali chaqirish.
- `WebAsyncTask` bilan uzoq hisobotni timeout va fallback bilan fon oqimida bajarish.
- Netty asosidagi gatewayda autentifikatsiyani tez, biznes mantiqni worker hovuzida bajarish.
- Message listener'da qabul qilishni tez tasdiqlab, og'ir ishni ichki navbatga uzatish.
- Legacy SOAP klientini reaktiv pipeline ichiga ajratilgan scheduler bilan integratsiya qilish.

**Ehtiyot bo'ling:** Ikki qatlam orasidagi navbat chegarasiz bo'lsa, asinxron qatlam sinxron qatlamdan tezroq ishlab xotirani to'ldiradi - chegara va rad etish siyosati majburiy. Shuningdek kontekst (SecurityContext, MDC, `@Transactional` transaksiyasi) chegaradan avtomatik o'tmaydi: `DelegatingSecurityContextAsyncTaskExecutor` yoki Micrometer `ContextPropagation` bilan ko'chirish kerak.

```java
// Half-Sync/Half-Async: asinxron qabul, sinxron ishlov - o'rtada navbat
@RestController
class UploadController {
    private final BlockingQueue<UploadTask> queue;   // chegaralangan

    @PostMapping("/uploads")
    ResponseEntity<Void> accept(@RequestBody UploadTask task) {
        if (!queue.offer(task)) return ResponseEntity.status(503).build();
        return ResponseEntity.accepted().build();    // tez javob, ish keyinroq
    }
}
// Worker pool navbatdan olib sinxron (blocking) ishlaydi
```

## 4.9 Yetakchi/Izdoshlar (Leader/Followers)

**Tavsif:** Hovuzdagi oqimlardan faqat bittasi "yetakchi" bo'lib hodisa manbasini kuzatadi; hodisa kelganda u darhol yangi yetakchini tanlab, o'zi qayta ishlashga o'tadi. Shu bilan hodisani bir oqimdan boshqasiga uzatish (handoff) va navbat ustidagi kontekst almashinuvi yo'qoladi, ya'ni latency va lock contention kamayadi. Bu Half-Sync/Half-Async'ning yuqori samarali, lekin murakkabroq alternativasi.

**Spring'da qayerda uchraydi:** Thread darajasida bu pattern asosan konteyner va transport ichida qoladi: Tomcat NIO/APR connector'larining acceptor-poller mexanizmi va Netty event loop'larining `SingleThreadEventExecutor` navbati shu g'oyaga yaqin, `ServerSocketChannel.accept()` ni navbatma-navbat chaqiradigan qo'lda yozilgan serverlar ham shunga kiradi. Taqsimlangan tizimda esa ayni nom boshqa, lekin tushunarli ma'noda ishlatiladi: Spring Integration'ning `LockRegistryLeaderInitiator`, `Candidate`/`DefaultCandidate` va `OnGrantedEvent`/`OnRevokedEvent` hodisalari, Spring Cloud Zookeeper/Kubernetes leader election starterlari - bu yerda "yetakchi" bitta instansiya bo'ladi. Arxitektor bu ikki qo'llanishni aralashtirmasligi kerak.

**Qo'llanish keyslari:**
- Yuqori frekansli, qisqa so'rovlarni ishlovchi maxsus TCP serverida handoff narxini yo'qotish.
- Netty asosidagi protokol serverida ulanishni bitta event loop'ga biriktirib, lock'siz ishlash.
- Klaster ichida faqat bitta instansiyada `@Scheduled` ishni bajarish (leader election).
- Spring Integration'da faqat yetakchi instansiya `inbound-channel-adapter`ni ishga tushirishi.
- Kafka consumer group'da partition egasini aniqlash kabi "bitta egasi" semantikasi.

**Ehtiyot bo'ling:** Thread-darajali Leader/Followers'ni qo'lda yozish deyarli hech qachon o'zini oqlamaydi - Netty yoki konteyner implementatsiyasidan foydalaning. Taqsimlangan leader election'da esa split-brain va fencing muammosi bor: yetakchilik yo'qolganda ishni darhol to'xtatish va token/fence bilan tekshirish logikasi bo'lmasa, ikki instansiya bir vaqtda "yetakchi" deb o'ylaydi.

```java
// Leader/Followers: bir vaqtda bitta nusxa yetakchi bo'ladi
@Scheduled(fixedDelay = 60_000)
@SchedulerLock(name = "nightly-settlement", lockAtMostFor = "PT10M")
public void settle() {
    // ShedLock: ko'p nusxada ishlaydigan ilovada faqat bittasi bajaradi
    settlementService.runOnce();
}
```

## 4.10 O'qish-yozish lock'i (Read-Write Lock)

**Tavsif:** Umumiy resursga bir vaqtda ko'p o'quvchiga ruxsat beradi, lekin yozuvchini yakka (exclusive) qo'yib, o'qish bilan birga kelmasligini kafolatlaydi. O'qish yozishdan ancha ko'p bo'lgan ssenariylarda oddiy mutexga nisbatan sezilarli parallellik beradi. Lock'ning adolatlilik (fairness) siyosati o'quvchilar yozuvchini "ochdan o'ldirmasligi" uchun muhim.

**Spring'da qayerda uchraydi:** Java'da `ReentrantReadWriteLock` (`readLock()`/`writeLock()`, `tryLock`, fair rejim) va optimistik o'qishni qo'llovchi, lekin reentrant bo'lmagan `StampedLock` (`tryOptimisticRead`/`validate`). Ko'p holatda lock'siz muqobil afzal: `ConcurrentHashMap`, `CopyOnWriteArrayList`, `AtomicReference` bilan immutable snapshotni almashtirish. Spring kodbazasida `ConcurrentReferenceHashMap` va `ReloadableResourceBundleMessageSource` kabi cache'li komponentlar shu yondashuvlarni ishlatadi; Spring Integration'ning `LockRegistry` esa taqsimlangan lock uchun shunga o'xshash abstraksiyani (masalan `RedisLockRegistry`, `JdbcLockRegistry`) beradi.

**Qo'llanish keyslari:**
- Kamdan-kam yangilanadigan, tez-tez o'qiladigan konfiguratsiya yoki feature-flag snapshotini himoyalash.
- In-memory reference data (valyuta kurslari, tariflar) ni fon yangilanishi bilan birga xizmat qilish.
- Katta ichki indeks yoki routing jadvalini qayta qurish davomida o'qishni to'xtatmaslik.
- Rate limiter yoki metrik agregatorining o'qish/reset bosqichlarini ajratish.
- Fayl yoki hujjat keshini ko'p o'quvchi va bitta yangilovchi bilan boshqarish.

**Ehtiyot bo'ling:** Lock olish va bo'shatish narxi oddiy `synchronized` dan yuqori - agar kritik bo'lim juda qisqa yoki yozish ulushi katta bo'lsa, read-write lock faqat sekinlashtiradi. `StampedLock` reentrant emas va `Condition` bermaydi; o'qish ichida yozish lock'iga "ko'tarilish" (upgrade) `ReentrantReadWriteLock` da deadlock keltiradi. Imkon bo'lsa umuman lock'siz immutable snapshot almashtirishni afzal ko'ring.

```java
// Read-Write lock: ko'p o'quvchi parallel, yozuvchi yakka
private final ReadWriteLock lock = new ReentrantReadWriteLock();
private volatile RateTable table = RateTable.empty();

public BigDecimal rate(String pair) {
    lock.readLock().lock();
    try { return table.get(pair); } finally { lock.readLock().unlock(); }
}

public void reload(RateTable fresh) {
    lock.writeLock().lock();
    try { this.table = fresh; } finally { lock.writeLock().unlock(); }
}
// Agar faqat almashtirish bo'lsa, volatile referens yetadi va lock kerak emas
```

## 4.11 Ikki marta tekshirilgan lock (Double-Checked Locking)

**Tavsif:** Lazy initsializatsiyada har safar lock olishning narxidan qutulish uchun maydon avval lock'siz tekshiriladi, faqat `null` bo'lsa lock olinadi va lock ichida qayta tekshiriladi. Java'da bu faqat maydon `volatile` bo'lganda to'g'ri ishlaydi, aks holda yarim qurilgan obyektni ko'rish mumkin (Java 5 dan keyingi memory model bilan `volatile` yetarli).

Baholashda halol bo'lish kerak: *Java Concurrency in Practice* bu idiomani **anti-pattern** deb ataydi va listingini "Don't do this" sarlavhasi bilan beradi. Kitobning dalili ikki qismdan iborat. Birinchi, nega u buziladi: DCL ning asosidagi taxmin "sinxronizatsiyasiz o'qishda bo'ladigan eng yomon narsa eskirgan qiymatni (bu holda `null`) ko'rish", holbuki haqiqiy eng yomon holat ancha og'ir, ya'ni havolaning **yangi** qiymatini, lekin obyekt holatining **eskirgan** qiymatlarini ko'rish, demak obyekt yaroqsiz holatda ko'rinishi mumkin. Ikkinchi, nega u endi kerak emas: idiomani tug'dirgan sabablar (sekin raqobatsiz sinxronizatsiya, sekin JVM startup) endi kuchda emas, shuning uchun u optimizatsiya sifatida ham ta'sirsiz; lazy initialization holder idiomasi xuddi shu foydani beradi va tushunish osonroq.

Shuning uchun bu bo'limdagi kod "to'g'ri yozilgan DCL" namunasi sifatida o'qilishi kerak, tavsiya sifatida emas: yangi kodda holder idiomasi yoki `AtomicReference.updateAndGet` tanlanadi.

**Spring'da qayerda uchraydi:** Spring Framework ichida `DefaultSingletonBeanRegistry.getSingleton(...)` singleton cache'ni avval lock'siz `singletonObjects.get(name)` bilan tekshiradi va faqat topilmasa lock ichida yaratadi, ya'ni klassik ikki marta tekshirish. Ikki tafsilot muhim: `singletonObjects` `ConcurrentHashMap`, demak birinchi tekshiruv rostdan lock'siz va ko'rinuvchanlik map ning o'zi tomonidan kafolatlanadi; qurish esa Spring 6 dan boshlab `synchronized` emas, `ReentrantLock` (`singletonLock`) bilan o'raladi, bu virtual thread da pinning ni oldini oladi (architect 12.4). `AbstractBeanFactory` va `ConcurrentReferenceHashMap` ham shunga yaqin yondashadi. Ilova kodida ko'pincha kerak bo'lmaydi, chunki `@Lazy`, `ObjectProvider<T>`, `@Configuration` bean metodlari va `Suppliers.memoize` uslubidagi yordamchilar xuddi shu natijani beradi; eng xavfsiz Java idiomasi - initialization-on-demand holder yoki `AtomicReference.updateAndGet`.

```java
private volatile Config config;

public Config get() {
    Config c = this.config;                 // 1-tekshiruv, lock'siz
    if (c == null) {
        synchronized (this) {
            c = this.config;                // 2-tekshiruv, lock ichida
            if (c == null) {
                c = loadConfig();
                this.config = c;            // volatile yozuv
            }
        }
    }
    return c;
}
```

**Qo'llanish keyslari:**
- Og'ir va ixtiyoriy resursni (ML modeli, katta parser) faqat birinchi so'rovda yuklash.
- Juda tez-tez chaqiriladigan getter'da lock contention'ni yo'qotish.
- Tashqi tizimga ulanishni (client, channel) talab bo'lganda bir marta qurish.
- Framework ichidagi cache'da "yo'q bo'lsa yarat" semantikasini tezlashtirish.
- Legacy singleton'larni thread-safe holatga keltirish.

**Ehtiyot bo'ling:** `volatile` ni tushirib qoldirish - bu patternning eng mashhur va eng jim xatosi: test muhitida hech qachon ko'rinmaydi, prodda esa buzilgan obyekt beradi. Yangi kodda avval `@Lazy`/holder idiomasini ko'rib chiqing; shuningdek lock ichida tashqi chaqiruv qilish startup paytida barcha so'rovlarni to'xtatib qo'yishi mumkin.

## 4.12 Shart bilan to'xtatish (Guarded Suspension)

**Tavsif:** Agar obyekt operatsiyani bajarish uchun kerakli holatda bo'lmasa, chaqiruvchini xato qaytarmasdan shart bajarilgunicha kutishga qo'yadi. Kutish lock'ni bo'shatib turadi va holat o'zgarganda signal orqali qayta tiklanadi. Kutish doim timeout bilan chegaralangan bo'lishi amaliy talab.

**Spring'da qayerda uchraydi:** Java'da `Object.wait()/notifyAll()`, `Condition.await(timeout, unit)/signalAll()`, va tayyor yuqori darajali vositalar: `BlockingQueue.take()/poll(timeout)`, `CountDownLatch.await()`, `Semaphore.acquire()`, `CyclicBarrier`, `Phaser`, `CompletableFuture.get(timeout)`. Spring tomonida `QueueChannel.receive(timeout)`, `DeferredResult` (natija kelmaguncha so'rovni "to'xtatib" turadi), `SimpleMessageListenerContainer` ning `shutdownTimeout` bilan to'xtashi, `ThreadPoolTaskExecutor.setWaitForTasksToCompleteOnShutdown(true)` va `SmartLifecycle` ning bosqichli start/stop kutishi shu patternga tayanadi; testlarda `Awaitility` yoki `CountDownLatch` bilan bir xil g'oya qo'llanadi.

**Qo'llanish keyslari:**
- Connection pool'dan bo'sh ulanish chiqishini `Semaphore` yoki pool timeout bilan kutish.
- Graceful shutdown'da bajarilayotgan vazifalar tugashini cheklangan vaqt kutish.
- Ilova start bo'lganda kerakli cache yoki schema migratsiyasi tayyor bo'lishini kutish.
- `DeferredResult` bilan hodisa kelgunicha HTTP so'rovni ochiq ushlab turish.
- Integratsion testda asinxron natija yozilishini latch orqali kutish.

**Ehtiyot bo'ling:** Timeout'siz kutish - ishlab chiqarishdagi to'liq osilib qolishning (hang) eng oson yo'li; har bir `await`/`take` uchun chegara va ortga qaytish rejasi bo'lsin. `wait()` ni doim `while (!condition)` tsikli ichida ishlating, chunki spurious wakeup bor; `notify()` o'rniga `notifyAll()` ni afzal ko'ring, aks holda noto'g'ri oqim uyg'otiladi.

```java
// Guarded Suspension: shart bajarilmaguncha kutish
private final Lock lock = new ReentrantLock();
private final Condition notEmpty = lock.newCondition();
private final Deque<Task> tasks = new ArrayDeque<>();

public Task take(Duration timeout) throws InterruptedException {
    lock.lock();
    try {
        long nanos = timeout.toNanos();
        while (tasks.isEmpty()) {                 // while, if emas: spurious wakeup
            if (nanos <= 0) throw new TimeoutException();
            nanos = notEmpty.awaitNanos(nanos);
        }
        return tasks.pollFirst();
    } finally { lock.unlock(); }
}
```

## 4.13 Rad etib qaytish (Balking)

**Tavsif:** Obyekt operatsiya uchun mos holatda bo'lmasa, kutmaydi ham, xato tashlamaydi ham - shunchaki hech narsa qilmasdan darhol qaytadi. Bu idempotent yoki "qayta urinish keyin ham bo'ladi" tabiatli ishlar uchun eng oddiy himoya: ikkinchi chaqiruv jim tashlab ketiladi. Guarded Suspension bilan tanlov: kutish arzonmi yoki o'tkazib yuborish xavfsizmi.

**Spring'da qayerda uchraydi:** Java'da `AtomicBoolean.compareAndSet(false, true)`, `ReentrantLock.tryLock()`, `Lock.tryLock(0, unit)` va `ConcurrentHashMap.putIfAbsent(...)` - klassik balking vositalari. Spring'da `SmartLifecycle.isRunning()` tekshiruvi `start()` ni ikki marta bajarmaslik uchun ishlatiladi; `@Scheduled` metodlarida takroriy ishni oldini olish uchun ShedLock (`@SchedulerLock`) yoki Spring Integration'ning `LockRegistry.obtain(key).tryLock()` qo'llanadi. `MessageListener` larda `IdempotentReceiverInterceptor` (Spring Integration) takroriy xabarni jim tashlab ketadi; Resilience4j'ning Bulkhead va CircuitBreaker ham "hozir qabul qilmayman" semantikasida shunga yaqin.

**Qo'llanish keyslari:**
- Klasterda `@Scheduled` ishni faqat lock'ni olgan instansiya bajarishi, qolganlari jim o'tishi.
- Allaqachon ishga tushgan cache warm-up yoki reindex jarayonini ikkinchi marta boshlamaslik.
- Takroriy webhook yoki Kafka xabarini idempotent kalit bo'yicha tashlab ketish.
- Foydalanuvchi "Saqlash" tugmasini ikki marta bosganda ikkinchi so'rovni e'tiborsiz qoldirish.
- Lifecycle komponentini qayta `stop()` qilishda hech narsa qilmaslik.

**Ehtiyot bo'ling:** Jim tashlab ketish kuzatuvchanlikni yo'qotadi - har bir balk hodisasini metrik yoki debug log bilan belgilab qo'ying, aks holda "ish bajarilmagani" sezilmaydi. Muhim biznes operatsiyasini balking bilan o'tkazib yuborish ma'lumot yo'qolishiga olib keladi: bunday joyda navbat, retry yoki aniq xato qaytarish to'g'riroq.

```java
// Balking: holat mos kelmasa, kutmasdan darhol qaytadi
private final AtomicBoolean running = new AtomicBoolean(false);

public void startReindex() {
    if (!running.compareAndSet(false, true)) {
        return;                       // allaqachon ketyapti: jimgina chiqadi
    }
    try {
        reindexAll();
    } finally {
        running.set(false);
    }
}
```

## 4.14 Rejalashtiruvchi (Scheduler)

**Tavsif:** Vazifalarning qachon va qanday tartibda bajarilishini markazlashtirilgan komponent hal qiladi: kechikish, davriylik, cron ifodasi yoki prioritet bo'yicha. Vazifa mantiqi vaqt mantiqidan ajratilgani uchun ishni sinab ko'rish va qayta sozlash osonlashadi. Bitta ilova ichida rejalashtirish va klaster bo'ylab rejalashtirish butunlay boshqa murakkablik darajalari ekanini ajratish kerak.

**Spring'da qayerda uchraydi:** Java'da `ScheduledExecutorService`, `Executors.newScheduledThreadPool(...)`, `DelayQueue`. Spring 6.x'da `@EnableScheduling` + `@Scheduled(cron = "...", fixedDelay = ..., fixedRate = ...)`, `TaskScheduler` abstraksiyasi, `ThreadPoolTaskScheduler`, Spring 6.1 dan virtual threadlarga mos `SimpleAsyncTaskScheduler`, `CronTrigger`, `PeriodicTrigger` va `@Scheduled(scheduler = "...")`; Spring Boot 3.x/4.x `spring.task.scheduling.pool.size` va `spring.task.scheduling.simple.*` propertylarini beradi. Og'irroq talablar uchun Quartz (`spring-boot-starter-quartz`, `JobDetail`, `Trigger`, JDBC JobStore), klasterda takrorlanmaslik uchun ShedLock, Spring Batch ishlarini boshqarish uchun `JobLauncher` + `@Scheduled` kombinatsiyasi ishlatiladi.

**Qo'llanish keyslari:**
- Har kuni ertalab hisobot generatsiyasi va uni email bilan tarqatish.
- Muddati o'tgan session, token yoki temp fayllarni davriy tozalash.
- Transactional outbox jadvalini har bir necha sekundda skanerlab, xabarlarni yuborish.
- Tashqi tizim bilan har 15 daqiqada inkremental sinxronizatsiya.
- Retry navbatidagi muvaffaqiyatsiz operatsiyalarni eksponensial kechikish bilan qayta urinish.

**Ehtiyot bo'ling:** Standart `ThreadPoolTaskScheduler` o'lchami 1 ga teng - bitta uzun vazifa boshqa barcha `@Scheduled` ishlarni kechiktiradi; pool o'lchamini oshiring va har bir vazifaga timeout qo'ying. `fixedRate` vazifa o'z intervalidan uzoq ishlasa navbat yig'iladi (odatda `fixedDelay` xavfsizroq), klasterda esa har bir instansiya ishni mustaqil bajaradi - leader election yoki ShedLock bo'lmasa, ish N marta takrorlanadi. Quartz JDBC JobStore da `Trigger` bean i ilova startini to'xtatishi mumkin: Spring Boot har `Trigger` bean ni `SchedulerFactoryBean` ga beradi, u esa ro'yxatga olishdan oldin `scheduler.getTrigger(key)` ni chaqiradi. Bazaviy qatori bor, lekin detal qatori (`cron_triggers` va boshqalar) yo'qolgan triggerda bu o'qish `NoRecordFoundException` bilan `afterPropertiesSet()` ichida yiqiladi va `overwrite-existing-jobs` tuzatishga ulgurmaydi. Start oldidan qatorni tozalaydigan himoya yetarli emas: xato yo'lining o'zi qoladi. Ilova usiz ham ishlay oladigan job ning triggeri bean qilinmaydi, startdan keyin (`ApplicationRunner`) bitta tranzaksiyada `unscheduleJob` + `scheduleJob` bilan ro'yxatga olinadi va xato log ga yoziladi. `unscheduleJob` qatorni o'qimay o'chiradi, shuning uchun buzilgan qatorni ham tozalaydi; `rescheduleJob` va `scheduleJob(job, triggers, true)` esa uni avval o'qiydi yoki detalni `UPDATE` qiladi va tuzatmaydi.

```java
// Scheduler: ishni qachon bajarish qarori alohida joyda
@Configuration
@EnableScheduling
class SchedulingConfig implements SchedulingConfigurer {
    @Override
    public void configureTasks(ScheduledTaskRegistrar registrar) {
        // default bitta thread: sekin job qolganini kechiktiradi
        ThreadPoolTaskScheduler s = new ThreadPoolTaskScheduler();
        s.setPoolSize(4);
        s.setThreadNamePrefix("sched-");
        s.setAwaitTerminationSeconds(30);
        s.setWaitForTasksToCompleteOnShutdown(true);
        s.initialize();
        registrar.setTaskScheduler(s);
    }
}
```

## 4.15 Thread'ga xos saqlash (Thread-Specific Storage)

**Tavsif:** Har bir thread o'ziga tegishli alohida qiymat nusxasiga ega bo'ladi, shu sababli umumiy o'zgaruvchini lock bilan himoyalash kerak emas. Kontekst (joriy foydalanuvchi, so'rov identifikatori, tranzaksiya) metod signaturalariga parametr qo'shmasdan chaqiruv stack'i bo'ylab "yashirin" tarzda uzatiladi. Amalda bu `ThreadLocal` orqali ro'yobga chiqadi: kalit - thread, qiymat - shu thread'ning xususiy holati. Kamchiligi shunda - kontekst thread bilan bog'langani uchun boshqa thread'ga avtomatik o'tmaydi va tozalanmasa leak beradi.

**Spring'da qayerda uchraydi:** `java.lang.ThreadLocal` va `InheritableThreadLocal`; SLF4J/Logback `MDC` (`MDC.put("traceId", ...)`, `%X{traceId}` pattern bilan). Spring Framework 6.x/7.x'da bu pattern hamma joyda: `RequestContextHolder`, `LocaleContextHolder`, `TransactionSynchronizationManager`, `SecurityContextHolder` (`MODE_THREADLOCAL` - standart), Spring AOP'da `ThreadLocalTargetSource`. Thread pool'ga kontekstni ko'chirish uchun `TaskDecorator` (`ThreadPoolTaskExecutor.setTaskDecorator`) va `DelegatingSecurityContextAsyncTaskExecutor` ishlatiladi; Micrometer `ContextRegistry` / `ContextSnapshot` (`context-propagation` kutubxonasi) esa imperativ `ThreadLocal` bilan Reactor `Context` o'rtasida ko'prik bo'ladi.

**Qo'llanish keyslari:**
- Barcha log satrlariga `traceId`/`correlationId` qo'shish uchun filter'da MDC'ni to'ldirish.
- Multi-tenant ilovada joriy tenant identifikatorini `AbstractRoutingDataSource` uchun saqlash.
- `SecurityContextHolder` orqali service qatlamida joriy foydalanuvchiga parametrsiz murojaat qilish.
- Auditing uchun `AuditorAware` implementatsiyasida joriy operatorni olish.
- Og'ir va thread-safe bo'lmagan obyektlarni (`SimpleDateFormat`, `Jackson ObjectWriter` ba'zi konfiguratsiyalari) thread bo'yicha keshlash.

**Ehtiyot bo'ling:** Thread pool'da `remove()` chaqirilmasa qiymat keyingi so'rovga "sizib o'tadi" - bu xavfsizlik incident'i darajasidagi xato, shuning uchun har doim `finally` blokida tozalang. Reactive (WebFlux) va `@Async` kodda kontekst o'z-o'zidan ko'chmaydi, virtual thread'larda esa millionlab `ThreadLocal` nusxasi xotirani yeb qo'yadi - yangi kodda `ScopedValue` yoki Reactor `Context` afzal.

```java
// Thread-specific storage: kontekst thread'ga bog'langan, tozalash majburiy
public final class TenantContext {
    private static final ThreadLocal<TenantId> CURRENT = new ThreadLocal<>();

    public static void set(TenantId id) { CURRENT.set(id); }
    public static TenantId get() { return CURRENT.get(); }
    public static void clear() { CURRENT.remove(); }   // finally da chaqirilmasa oqadi
}

// Virtual thread va reactive kodda ScopedValue yoki Reactor Context afzal
```

## 4.16 O'zgarmas obyekt (Immutable Object)

**Tavsif:** Obyekt yaratilgandan so'ng uning holati umuman o'zgarmaydi, shuning uchun uni istalgan sondagi thread bir vaqtda hech qanday sinxronizatsiyasiz o'qiy oladi. Holatni o'zgartirish o'rniga yangi nusxa qaytariladi (copy-on-write semantikasi). Bu concurrency'dagi eng arzon va eng ishonchli yechim: race condition texnik jihatdan imkonsiz bo'lib qoladi. Shart - barcha maydonlar `final`, mutable kolleksiyalar va massivlar konstruktorda hamda getter'da himoyalab nusxalanadi.

**Spring'da qayerda uchraydi:** Java 17+ `record` - DTO, event va value object uchun standart vosita; `java.time` turlari (`Instant`, `LocalDate`, `Duration`), `String`, `List.of`/`Map.of`, `Collections.unmodifiableList`. Spring'da: `@ConfigurationProperties` konstruktor binding (`@ConstructorBinding` bilan `record`), Spring Messaging'dagi `MessageHeaders` va `GenericMessage`, `HttpHeaders.readOnlyHttpHeaders(...)`, WebFlux functional endpoint'laridagi `ServerRequest`, `ResponseEntity` va `RequestEntity`, `MethodParameter`-ga o'xshash infratuzilma metadata obyektlari. Lombok `@Value` va Guava `ImmutableList` ham ko'p ishlatiladi.

**Qo'llanish keyslari:**
- REST API request/response DTO'larini `record` sifatida e'lon qilish va ularni bemalol thread'lar o'rtasida uzatish.
- Domain event'larni (`ApplicationEvent`, Kafka payload) o'zgarmas qilib, consumer tomonda tasodifiy mutatsiyani oldini olish.
- `@ConfigurationProperties` konfiguratsiyasini immutable qilib, runtime'da sozlamalar o'zgarishini taqiqlash.
- Pul, koordinata, interval kabi value object'larni `equals`/`hashCode` bilan to'g'ri modellashtirish va cache kaliti sifatida ishlatish.
- Hisoblash natijalari jadvalini `Map.copyOf` bilan immutable snapshot qilib e'lon qilish.

**Ehtiyot bo'ling:** `record` faqat sayoz (shallow) immutability beradi - ichidagi `List` yoki massiv mutable bo'lsa, himoya buziladi, shuning uchun konstruktorda `List.copyOf` qiling. JPA entity'larni immutable qilish amalda qiyin (proxy va dirty checking talab qiladi), shuning uchun entity emas, DTO/projection darajasida qo'llang.

```java
// Immutable: yaratilgandan keyin o'zgarmaydi, shuning uchun thread-safe
public record Money(BigDecimal amount, Currency currency) {
    public Money {
        Objects.requireNonNull(amount);
        amount = amount.setScale(currency.getDefaultFractionDigits(), RoundingMode.HALF_UP);
    }
    public Money plus(Money other) {      // yangi nusxa qaytaradi
        if (!currency.equals(other.currency)) throw new CurrencyMismatchException();
        return new Money(amount.add(other.amount), currency);
    }
}
```

## 4.17 Barrier va sanoqli kutish (Barrier / CountDownLatch / Phaser)

**Tavsif:** Bir nechta thread ma'lum nuqtaga yetib kelishini kutib, shundan keyingina davom etishni ta'minlaydigan koordinatsiya pattern'i. `CountDownLatch` bir martalik hisoblagich - N ta vazifa tugaganini kutish uchun; `CyclicBarrier` qayta ishlatiladigan to'siq - bir xil thread'lar har raundda uchrashib turadi; `Phaser` esa dinamik ravishda ro'yxatdan o'tadigan va chiqib ketadigan ishtirokchilar bilan ko'p fazali kutishni qo'llab-quvvatlaydi. Maqsad - "hammasi tayyor bo'lgandan keyin" semantikasini busy-wait qilmasdan ifodalash.

**Spring'da qayerda uchraydi:** `java.util.concurrent.CountDownLatch`, `CyclicBarrier`, `Phaser`, shuningdek `CompletableFuture.allOf(...)` va `ExecutorService.invokeAll(...)` - ko'p hollarda latch'ning yuqori darajadagi muqobili. Spring ekotizimida: integration test'larda `@KafkaListener`/`@RabbitListener` xabarni qabul qilganini `CountDownLatch` bilan kutish (Spring for Apache Kafka'ning o'z test utility'lari ham shu uslubda), `ApplicationReadyEvent`/`ContextRefreshedEvent` bilan start koordinatsiyasi, Spring Batch'da `TaskExecutorPartitionHandler` barcha partition step'lari tugashini kutishi, `DefaultLifecycleProcessor`'ning shutdown fazasida `CountDownLatch` ishlatishi. Test tomonida Awaitility ko'pincha latch o'rnini bosadi.

**Qo'llanish keyslari:**
- Asinxron listener xabar qabul qilganini integration test'da deterministik kutish.
- Ilova start bo'lishidan oldin bir nechta cache yoki reference data yuklanishini kutish.
- Bir so'rov uchun parallel ishga tushirilgan 5 ta tashqi chaqiruv natijasini yig'ish (ko'pincha `CompletableFuture.allOf` bilan).
- Load test'da N ta thread'ni bir vaqtning o'zida "start" qilib, haqiqiy raqobatni modellashtirish.
- Ko'p fazali ETL'da har bir faza oxirida barcha worker'larni `Phaser` bilan sinxronlash.

**Ehtiyot bo'ling:** Latch'ni timeout'siz `await()` qilish ilovani butunlay muzlatib qo'yadi - har doim `await(timeout, unit)` ishlatib natijani tekshiring. Biznes-logikada bunday quyi darajali primitivlarni qo'lda yozish o'rniga `CompletableFuture`, Reactor yoki structured concurrency'ni afzal ko'ring; `CyclicBarrier` virtual thread'lar bilan ishlashda thread sonini chegaralab qo'yishi mumkin.

```java
// CountDownLatch: hamma tayyor bo'lguncha kutish
int workers = 4;
CountDownLatch ready = new CountDownLatch(workers);
CountDownLatch start = new CountDownLatch(1);

for (int i = 0; i < workers; i++) {
    executor.submit(() -> {
        ready.countDown();
        start.await();        // hamma bir vaqtda boshlaydi (yuk testi uchun)
        doWork();
        return null;
    });
}
ready.await();               // hamma tayyor
start.countDown();           // start berildi
```

## 4.18 Fork-Join va ishni o'g'irlash (Fork-Join / Work Stealing)

**Tavsif:** Katta vazifani rekursiv ravishda mayda bo'laklarga bo'lib (fork), ularni parallel bajarib, natijalarni birlashtirish (join) usuli. Har bir worker thread o'zining deque'siga ega; o'z navbati bo'shab qolgan thread boshqa thread'ning navbati oxiridan vazifa "o'g'irlaydi" (work stealing), natijada yuk o'z-o'zidan tenglashadi va thread'lar bekor turmaydi. Bu divide-and-conquer tipidagi CPU-bound hisoblar uchun eng samarali model.

**Spring'da qayerda uchraydi:** `java.util.concurrent.ForkJoinPool`, `RecursiveTask`/`RecursiveAction`, `ForkJoinPool.commonPool()`, `Executors.newWorkStealingPool()`; `parallelStream()` va parametrsiz `CompletableFuture.supplyAsync(...)` standart holda `commonPool`'da ishlaydi.

`commonPool` ning hajmi aynan nechta ekani konteynerda muhim bo'lib qoladi: JDK manbasida u `Math.max(1, availableProcessors() - 1)`, ya'ni yadro sonidan **bittaga kam** (chaqiruvchi thread ham ishga qo'shilgani uchun). Konteynerga ikki yadro berilgan bo'lsa parallelism 1 ga tushadi va `parallelStream()` amalda ketma-ket ishlaydi; bir yadroda ham 1 qoladi. Shuning uchun konteynerdagi CPU limiti `parallelStream()` ning foydasini jim ravishda yo'q qilishi mumkin va bu `-XX:ActiveProcessorCount` yoki cgroup limiti bilan bog'liq (architect 31.2). Qiymatni `java.util.concurrent.ForkJoinPool.common.parallelism` system property si bilan ham berish mumkin. Java 21+ virtual thread scheduler'i ham ichida `ForkJoinPool`'ga asoslangan. Spring Framework'da `org.springframework.scheduling.concurrent.ForkJoinPoolFactoryBean` orqali `ForkJoinPool`'ni bean sifatida e'lon qilish mumkin, so'ng uni `@Async` yoki `TaskExecutor` sifatida (`ConcurrentTaskExecutor` bilan o'rab) ishlatish mumkin.

**Qo'llanish keyslari:**
- Katta hisobot uchun millionlab satrni xotirada parallel agregatlash.
- Rasm/video yoki hujjat qismlarini rekursiv bo'lib parallel qayta ishlash.
- Daraxt shaklidagi strukturani (BOM, tashkilot ierarxiyasi) parallel kesib o'tish.
- Katta matritsa ko'paytirish yoki Monte-Carlo simulyatsiyasi kabi sof CPU hisoblari.
- Mustaqil validatsiya qoidalari to'plamini bir so'rov ichida parallel bajarish.

**Ehtiyot bo'ling:** `commonPool` butun JVM uchun umumiy va sig'imi `CPU-1` ga teng - unda blocking I/O bajarish (JDBC, HTTP) butun ilovani, hatto boshqa parallel stream'larni ham to'xtatib qo'yadi; I/O uchun alohida pool yoki virtual thread ishlatilsin. Agar blocking muqarrar bo'lsa, `ForkJoinPool.ManagedBlocker` qo'llang va bo'lish chuqurligini ortiqcha mayda qilmang, aks holda koordinatsiya narxi foydadan oshadi.

Chegarani (threshold) tanlashda xato qilish kerak bo'lsa, yuqoriga qarab xato qilish afzal: kichik chegarada vazifa yaratish, navbatga qo'yish va o'g'irlash ishning o'zidan ko'p vaqt oladi, katta chegarada esa eng yomon holat parallellikning yetarli ishlatilmasligi bo'ladi. `ForkJoinTask` hujjati mo'ljal beradi: bitta vazifa taxminan 100 dan 10 000 gacha hisob qadamini bajarishi kerak - yuqoridagi `THRESHOLD = 10_000` shu oraliqning yuqori chekkasi. Ikkinchi cheklov `compute()` ichida qulf ishlatmaslik: bo'lib-hal qilish strategiyasi tashqi sinxronlashga mos emas, chunki vazifalar bir-birining tugashini kutadi va qulf bu kutishni deadlock ga aylantiradi. Vazifalar orasida muvofiqlashtirish zarur bo'lsa, `Phaser` kabi fork-join bilan birga ishlashga mo'ljallangan vosita ishlatiladi, `synchronized` yoki semafor emas.

```java
// Fork-Join: ishni bo'lib, natijani yig'ish. Faqat CPU ishi uchun.
class SumTask extends RecursiveTask<Long> {
    private static final int THRESHOLD = 10_000;
    private final long[] data; private final int from, to;

    SumTask(long[] data, int from, int to) { this.data = data; this.from = from; this.to = to; }

    @Override protected Long compute() {
        if (to - from <= THRESHOLD) {
            long s = 0; for (int i = from; i < to; i++) s += data[i]; return s;
        }
        int mid = (from + to) >>> 1;
        SumTask left = new SumTask(data, from, mid);
        left.fork();
        return new SumTask(data, mid, to).compute() + left.join();
    }
}
```

## 4.19 Actor modeli (Actor Model)

**Tavsif:** Umumiy o'zgaruvchan holat butunlay yo'q qilinadi: har bir actor o'z xususiy holatiga ega va faqat asinxron xabarlar orqali muloqot qiladi. Actor o'zining mailbox'idagi xabarlarni ketma-ket, bittalab qayta ishlaganligi uchun uning ichida lock ham, race condition ham bo'lmaydi. Supervision ierarxiyasi xatolarni lokalizatsiya qiladi - "let it crash" tamoyili bilan actor qayta ishga tushiriladi. Natijada concurrency lock emas, balki xabar almashinuvi va joylashuv shaffofligi (location transparency) orqali boshqariladi.

**Spring'da qayerda uchraydi:** Spring Framework'ning o'zida actor runtime'i yo'q, shuning uchun u tashqi kutubxonalar bilan birga ishlatiladi: Apache Pekko (`org.apache.pekko`, Akka'ning Apache-litsenziyali davomchisi), Akka Typed (`ActorSystem`, `Behaviors.receive`) yoki Vert.x verticle'lari. Spring'da actor'ga eng yaqin amaliy yondashuv - bitta kalit (partition/aggregate id) uchun faqat bitta thread ishlashini kafolatlash: `@KafkaListener(concurrency = "N")` bilan partition-per-consumer modeli, Spring Integration'da single-threaded `QueueChannel` + `PollerMetadata` yoki `BlockingQueue`'ga asoslangan event loop bean'lari. `ActorSystem`'ni `@Bean` sifatida e'lon qilib, uning lifecycle'ini Spring konteyneriga bog'lash odatiy amaliyot.

**Qo'llanish keyslari:**
- Trading yoki bank hisobi bo'yicha buyruqlarni aggregate-per-actor tarzida ketma-ket qayta ishlash.
- IoT'da har bir qurilma uchun alohida holatli sessiya (device twin) yuritish.
- O'yin serverida har bir o'yin xonasi holatini lock'siz boshqarish.
- Workflow/saga orkestratsiyasida uzoq yashovchi, holatli jarayonlarni modellashtirish.
- Chat yoki hamkorlikdagi tahrirlash sessiyalarini bitta "egasi" bo'lgan actor ichida tutish.

**Ehtiyot bo'ling:** Actor modeli typesafe emas (xabar - odatda `Object`) va debug qilish qiyin: stack trace yo'qoladi, xabar yo'qolishi mumkin, mailbox cheklanmagan bo'lsa OutOfMemoryError beradi. Shuning uchun uni butun ilovaga tarqatmang - faqat haqiqatan holatli, yuqori raqobatli domen qismlarida qo'llang; oddiy CRUD servis uchun bu ortiqcha murakkablik.

```java
// Actor: holat yakka egada, aloqa faqat xabar orqali
@Component
public class SeatBookingActor {
    private final BlockingQueue<BookRequest> inbox = new LinkedBlockingQueue<>(10_000);
    private final Set<Integer> taken = new HashSet<>();   // lock yo'q: bitta thread

    @PostConstruct
    void start() {
        Thread.ofVirtual().name("seat-actor").start(() -> {
            while (true) {
                BookRequest r = inbox.take();
                r.result().complete(taken.add(r.seat()));
            }
        });
    }
}
```

## 4.20 Lock'larni bo'lish (Lock Striping)

**Tavsif:** Butun struktura uchun bitta global lock olish o'rniga, lock'lar massivi yaratiladi va kalitning hash qiymatiga qarab faqat bitta "stripe" bloklanadi. Shunda turli kalitlar bilan ishlayotgan thread'lar bir-birini kutmaydi va throughput lock sonining o'sishi bilan chiziqli yaqinlashadi. Bu - granularity'ni oshirish orqali contention'ni kamaytiruvchi klassik kelishuv: xotira biroz ko'p sarflanadi, lekin kutish keskin kamayadi.

**Spring'da qayerda uchraydi:** `ConcurrentHashMap` (Java 7'da segment'lar, Java 8+ da bin darajasidagi node lock va CAS), `LongAdder`/`DoubleAdder` (hisoblagichni cell'lar bo'yicha bo'lish), Guava `Striped.lock(n)` / `Striped.semaphore(n)`, Caffeine cache'ning ichki yuklash mexanizmi. Spring ekotizimida: Spring Integration'ning `LockRegistry` abstraksiyasi - `DefaultLockRegistry` aynan hash mask bo'yicha lock massivini ishlatadi, `JdbcLockRegistry` va `RedisLockRegistry` esa shu interfeysning taqsimlangan variantlari. `@Cacheable(sync = true)` ham kalit bo'yicha lokal lock'lar bilan bir kalitga faqat bitta yuklashni kafolatlaydi.

**Qo'llanish keyslari:**
- Account yoki order id bo'yicha kritik bo'limni global lock'siz himoyalash.
- Yuqori yuklamali hisoblagichlar va metrikalarni `LongAdder` bilan yig'ish.
- Cache stampede'ni kalit bo'yicha lock orqali oldini olish (`@Cacheable(sync = true)`).
- Faylga yoki tashqi resursga kalit bo'yicha ketma-ket yozishni ta'minlash.
- Bir instansiya ichida idempotentlikni kalit bo'yicha lock bilan kafolatlash.

**Ehtiyot bo'ling:** Stripe soni kam bo'lsa turli kalitlar bitta lock'ga tushib "soxta" contention paydo bo'ladi, ko'p bo'lsa xotira va cache miss ortadi - odatda CPU sonidan bir necha baravar ko'p qilib tanlanadi. Eng muhimi: lokal lock striping bir nechta instansiyada ishlamaydi, klaster uchun `JdbcLockRegistry`/`RedisLockRegistry` yoki ShedLock kabi taqsimlangan yechim kerak.

```java
// Lock striping: bitta katta lock o'rniga kalit bo'yicha ko'p kichik lock
private final Object[] stripes = IntStream.range(0, 64)
        .mapToObj(i -> new Object()).toArray();

private Object stripeFor(String key) {
    return stripes[Math.floorMod(key.hashCode(), stripes.length)];
}

public void update(String key, Consumer<String> body) {
    synchronized (stripeFor(key)) {     // turli kalitlar bir-birini kutmaydi
        body.accept(key);
    }
}
// ConcurrentHashMap ichida xuddi shu g'oya ishlatiladi
```

## 4.21 Compare-And-Swap va lock-free algoritmlar (Compare-And-Swap / Lock-Free)

**Tavsif:** Lock olish o'rniga protsessorning atomar CAS instruksiyasiga tayanadi: "qiymat hali ham kutganimdek bo'lsa, yangisiga almashtir, aks holda qaytadan urin". Muvaffaqiyatsiz urinish retry bilan davom etadi, shuning uchun hech bir thread boshqasini bloklamaydi - kontekst almashinuvi va deadlock yo'qoladi. Past contention'da bu lock'dan sezilarli tez, yuqori contention'da esa retry'lar soni ortib samaradorlik tushib ketishi mumkin.

**Spring'da qayerda uchraydi:** `java.util.concurrent.atomic` paketi - `AtomicInteger`, `AtomicLong`, `AtomicReference` (`compareAndSet`, `updateAndGet`, `accumulateAndGet`), `AtomicStampedReference` (ABA muammosiga qarshi), `LongAdder`; quyi darajada `java.lang.invoke.VarHandle` (`compareAndExchange`) - `sun.misc.Unsafe`ning qo'llab-quvvatlanadigan o'rnini bosuvchisi. Lock-free kolleksiyalar: `ConcurrentLinkedQueue`, `ConcurrentLinkedDeque`, `ConcurrentSkipListMap`. Spring ichida ham keng ishlatiladi: Reactor'ning `Operators`/`Subscription` request accounting mexanizmi `AtomicLongFieldUpdater` bilan qurilgan, Micrometer `Counter` implementatsiyalari `DoubleAdder`ga tayanadi, Spring'ning ko'p infratuzilma cache'lari `ConcurrentHashMap` + atomic'lardan iborat.

**Qo'llanish keyslari:**
- Har bir so'rovda inkrement bo'luvchi metrikalar va statistik hisoblagichlar.
- Sozlama yoki feature flag snapshot'ini `AtomicReference` bilan atomar almashtirish (hot reload).
- Bir martalik initsializatsiyani `compareAndSet` bilan kafolatlash (idempotent start/stop).
- Circuit breaker holati kabi kichik holat mashinasini lock'siz boshqarish.
- Yuqori throughput'li queue va ring buffer (LMAX Disruptor uslubi) implementatsiyalari.

**Ehtiyot bo'ling:** CAS retry loop'i yuqori raqobatda CPU'ni behuda yoqadi va "livelock"ka olib kelishi mumkin; bir nechta o'zgaruvchini atomar o'zgartirish kerak bo'lsa CAS yetarli emas - immutable holatni bitta `AtomicReference`da almashtirish yoki lock ishlatish to'g'ri. Qo'lda lock-free struktura yozishdan saqlaning: memory model (`volatile`, happens-before) nozikliklari sabab JDK'dagi tayyor struktura deyarli har doim yaxshiroq.

```java
// CAS: lock'siz atomik o'zgartirish
private final AtomicReference<RateTable> table = new AtomicReference<>(RateTable.empty());

public void merge(RateTable delta) {
    table.updateAndGet(current -> current.mergedWith(delta));  // ichida CAS tsikli
}

private final AtomicLong processed = new AtomicLong();
public void onRecord() { processed.incrementAndGet(); }
// Nizo yuqori bo'lsa CAS tsikli ko'p aylanadi: LongAdder afzal
```

## 4.22 So'rovga bitta thread va event loop (Thread-per-request vs Event Loop)

**Tavsif:** Ikki qarama-qarshi server modeli. Thread-per-request'da har bir so'rov o'z thread'ini egallab turadi: kod oddiy, blocking chaqiruvlar tabiiy, lekin har bir thread stack uchun xotira yeydi va parallel so'rov soni pool hajmi bilan chegaralanadi. Event loop'da kichik sondagi thread (odatda CPU soniga teng) non-blocking I/O hodisalarini navbat bilan qayta ishlaydi: 10 ming ulanishni arzon ushlab turadi, biroq loop thread'ida bloklanish butun serverni to'xtatadi va kod callback/reactive uslubga o'tadi.

**Spring'da qayerda uchraydi:** Thread-per-request: Spring MVC + Tomcat/Jetty/Undertow (`server.tomcat.threads.max`), Servlet async'ni qo'llab-quvvatlash - `Callable`, `DeferredResult`, `StreamingResponseBody`, `spring.mvc.async.request-timeout`. Event loop: Spring WebFlux + Reactor Netty (`LoopResources`, `reactor.netty.ioWorkerCount`), bloklanadigan kodni ko'chirish uchun `Schedulers.boundedElastic()`, `WebClient`, `R2DBC`. Noto'g'ri bloklanishni aniqlash uchun BlockHound ishlatiladi. Spring Boot 3.2+ da `spring.threads.virtual.enabled=true` uchinchi yo'lni beradi: kod thread-per-request ko'rinishida qoladi, lekin thread'lar virtual bo'ladi.

**Qo'llanish keyslari:**
- Klassik CRUD + JDBC monolit uchun Spring MVC (thread-per-request) tanlash.
- Ko'p sonli uzoq yashovchi SSE/WebSocket ulanishlari uchun WebFlux event loop'i.
- Asosiy ishi downstream servislarni chaqirish bo'lgan API gateway'da non-blocking model.
- Streaming (katta fayl yoki log oqimi) javoblarini backpressure bilan uzatish.
- Mavjud blocking stack'da thread sonini oshirmasdan scalability olish uchun virtual thread'larni yoqish.
- Sekin tashqi chaqiruvni MVC'da `DeferredResult` bilan thread'ni band qilmasdan kutish.

**Ehtiyot bo'ling:** WebFlux'da event loop thread'ida JDBC, `Thread.sleep` yoki sinxron `RestTemplate` chaqirish eng ko'p uchraydigan halokatli xato - butun server kechikishi oshadi; bunday kodni albatta `boundedElastic`ga chiqaring. Shunchaki "tezroq bo'lsin" degan sabab bilan reactive stack'ga o'tmang: domen blocking bo'lsa, virtual thread'lar bir xil natijani ancha arzon murakkablikda beradi.

```yaml
# Thread-per-request: har so'rov o'z thread'ida, blocking ruxsat
spring:
  threads:
    virtual:
      enabled: true          # Boot 3.2+: so'rovlar virtual thread'da
  datasource:
    hikari:
      maximum-pool-size: 20  # virtual thread ko'p, DB ulanishi kam - chegara shu yerda
```

## 4.23 Virtual thread'lar (Virtual Threads)

**Tavsif:** JVM tomonidan boshqariladigan juda yengil thread'lar: ular platform thread'larga ko'p-ga-oz (M:N) nisbatda mount qilinadi va blocking operatsiya paytida (socket, lock, `sleep`) carrier thread'ni bo'shatib, stack'ni heap'ga park qiladi. Natijada bir JVM'da millionlab thread yaratish mumkin bo'ladi va "blocking kod - qimmat" degan asosiy cheklov yo'qoladi. Bu thread-per-request modelining oddiyligini event loop'ning scalability'si bilan birlashtiradi; API o'zgarmaydi - `Thread` o'sha-o'sha.

**Spring'da qayerda uchraydi:** Java 21'da yakuniy holatga keldi (JEP 444): `Thread.ofVirtual().start(...)`, `Executors.newVirtualThreadPerTaskExecutor()`. Spring Framework 6.1+ da `org.springframework.core.task.VirtualThreadTaskExecutor` va `SimpleAsyncTaskExecutor.setVirtualThreads(true)`. Spring Boot 3.2+ da bitta sozlama - `spring.threads.virtual.enabled=true` - Tomcat/Jetty request executor'ini, `@Async` uchun `applicationTaskExecutor`ni, `@Scheduled` uchun `taskScheduler`ni va Kafka/RabbitMQ listener container'larini virtual thread'larga o'tkazadi. JDK 24 (JEP 491) `synchronized` bloklardagi pinning muammosini hal qildi.

**Qo'llanish keyslari:**
- Ko'p sonli sekin REST yoki gRPC chaqiruvlarini bajaruvchi "fan-out" API'larda throughput'ni oshirish.
- Minglab parallel so'rovni kichik thread pool cheklovisiz qabul qilish.
- Reactive stack'ga ko'chmasdan I/O-bound batch yoki import jarayonlarini parallellashtirish.
- Har bir ulanish uchun bitta thread talab qiladigan legacy integratsiya kodini zamonaviylashtirish.
- Test va yuklama generatorlarida minglab mijoz sessiyasini soddagina modellashtirish.

**Ehtiyot bo'ling:** Virtual thread'larni pool qilmang - ular arzon, ularni cheklash kerak bo'lsa `Semaphore` ishlatilsin; `ThreadLocal`ga og'ir obyekt saqlash esa endi million nusxaga ko'payib xotirani yeb qo'yadi. Shuni ham yodda tuting: CPU-bound ish uchun hech qanday foyda bermaydi, JDBC pool (HikariCP) va downstream rate limit baribir haqiqiy bottleneck bo'lib qoladi, JDK 21-23 da `synchronized` ichidagi blocking carrier'ni pin qilib qo'yadi.

```java
// Virtual thread: arzon, blocking I/O uchun mo'ljallangan
try (var scope = Executors.newVirtualThreadPerTaskExecutor()) {
    List<Future<Quote>> futures = suppliers.stream()
            .map(s -> scope.submit(() -> s.fetchQuote(request)))   // har biri bloklanadi
            .toList();
    for (Future<Quote> f : futures) collect(f.get());
}

// Virtual thread bilan `synchronized` o'rniga ReentrantLock ishlating,
// va pool yasamang: thread o'zi arzon, chegara resursda bo'lishi kerak.
```

## 4.24 Strukturaviy concurrency (Structured Concurrency)

**Tavsif:** Parallel vazifalarning hayot davrini kod blokining leksik chegarasiga bog'laydi: blokdan chiqishdan oldin barcha bola vazifalar albatta tugaydi, bekor qilinadi yoki xatosi tashlanadi. Shu bilan "orphan" thread'lar, yo'qolgan exception'lar va qo'lda cancellation tarqatish muammosi bartaraf bo'ladi - xatolik va bekor qilish ierarxiya bo'ylab avtomatik tarqaladi. Mohiyatan bu `try`-with-resources'ning concurrency uchun analogi va virtual thread'lar bilan birga ishlatish uchun mo'ljallangan.

**Spring'da qayerda uchraydi:** `java.util.concurrent.StructuredTaskScope` - Java 21-24 da preview sifatida `ShutdownOnFailure`/`ShutdownOnSuccess` subclass'lari bilan, Java 25 (JEP 505) da esa API `StructuredTaskScope.open(Joiner.allSuccessfulOrThrow())` ko'rinishiga o'zgargan va hamon preview (`--enable-preview` kerak). Spring Framework'da buning uchun maxsus abstraksiya yo'q, shuning uchun u service metodi ichida to'g'ridan-to'g'ri ishlatiladi; klassik muqobillari - `CompletableFuture.allOf(...)`, `ExecutorService.invokeAll(...)` va Reactor'ning `Mono.zip(...)`, ular hozirgacha production uchun xavfsizroq tanlov.

```java
try (var scope = new StructuredTaskScope.ShutdownOnFailure()) { // Java 21-24 preview
    var user   = scope.fork(() -> userClient.find(id));
    var orders = scope.fork(() -> orderClient.findByUser(id));
    scope.join().throwIfFailed();
    return new Dashboard(user.get(), orders.get());
}
```

**Qo'llanish keyslari:**
- Bir so'rov uchun bir nechta downstream servisni parallel chaqirib, birortasi yiqilsa qolganini darhol bekor qilish.
- "Eng tez javob bergani g'olib" strategiyasi bilan ikki provayderga bir vaqtda murojaat qilish.
- Vaqt chegarasi (deadline) butun fan-out guruhiga yaxlit qo'llanishini kafolatlash.
- Batch ishida bola vazifalar ota vazifa to'xtaganda hech qachon "yetim" qolib ketmasligini ta'minlash.
- Murakkab aggregation logikasini o'qiladigan, blok ko'rinishidagi kodda ifodalash.

**Ehtiyot bo'ling:** API hali preview - relizlar o'rtasida o'zgaradi (Java 21 va Java 25 sintaksisi boshqa), shuning uchun uni ommaviy kutubxona yoki uzoq yashovchi production kodda ishlatishdan oldin yangilanish narxini hisobga oling. `scope`ni metoddan tashqariga chiqarmang yoki bean maydonida saqlamang - bu pattern'ning butun ma'nosini yo'q qiladi.

## 4.25 Qamrovli qiymatlar (Scoped Values)

**Tavsif:** `ThreadLocal`ning zamonaviy, o'zgarmas va qamrovga bog'langan o'rnini bosuvchisi: qiymat faqat ma'lum kod blokining bajarilish davrida ko'rinadi va blok tugashi bilan avtomatik "yo'qoladi". Qiymat o'zgartirilmaydi - faqat `where(...)` bilan yangi qamrov ochiladi, shuning uchun `remove()` qilishni unutish natijasidagi leak va kontekst "sizib o'tishi" imkonsiz. Structured concurrency bilan birga ishlaganda qiymat bola vazifalarga avtomatik, nusxa ko'chirmasdan meros bo'lib o'tadi - bu virtual thread'lar uchun juda muhim.

**Spring'da qayerda uchraydi:** `java.lang.ScopedValue` - Java 20'da incubator, 21-24 da preview, Java 25 (JEP 506) da yakuniy holatga keldi: `ScopedValue.newInstance()`, `ScopedValue.where(KEY, value)` bilan `Carrier` olinadi, undan `run(Runnable)` yoki `call(CallableOp)`, keyin `KEY.get()`, `KEY.isBound()`. `run` faqat checked istisno tashlamaydigan blok uchun; `CallableOp<T, X extends Throwable>` esa natija qaytaradi va checked istisnoni o'tkazib yuboradi. Spring Framework hozircha ichki kontekst holderlarini (`RequestContextHolder`, `SecurityContextHolder`, `TransactionSynchronizationManager`) `ThreadLocal` asosida yuritadi, shuning uchun amalda `ScopedValue` o'z ilova kodingizdagi kontekst uzatish uchun qo'llaniladi - masalan `OncePerRequestFilter` ichida qamrov ochib, pastdagi barcha chaqiruvlarga tenant yoki trace ma'lumotini uzatish.

```java
static final ScopedValue<String> TENANT = ScopedValue.newInstance();

// Filter ichida. run(Runnable) bu yerda kompilyatsiya bo'lmaydi:
// doFilter checked IOException va ServletException tashlaydi,
// Runnable.run() esa hech qanday checked istisnoni e'lon qilmaydi.
try {
    ScopedValue.where(TENANT, resolveTenant(request)).call(() -> {
        chain.doFilter(request, response);
        return null;                      // CallableOp natija qaytaradi
    });
}
catch (IOException | ServletException | RuntimeException | Error e) {
    throw e;                              // aniq qayta tashlash
}
catch (Exception e) {
    throw new IllegalStateException(e);   // yetib bo'lmaydigan shox
}

// chuqur qatlamda:
String tenant = TENANT.orElse("default");
```

**Qo'llanish keyslari:**
- Virtual thread'lar yoqilgan ilovada tenant yoki `traceId`ni `ThreadLocal` leak xavfisiz uzatish.
- So'rov qamrovidagi deadline yoki request metadata'sini chuqur qatlamlarga olib borish.
- Structured concurrency bloki ichidagi barcha bola vazifalarga kontekstni avtomatik meros qilish.
- Faqat ma'lum bir blok davomida amal qiladigan audit yoki feature-flag kontekstini belgilash.
- Immutable kontekst talab qilinadigan kutubxona API'larida `ThreadLocal`ni almashtirish.

**Ehtiyot bo'ling:** Qiymat qamrov ichida o'zgartirilmaydi - "o'zgaruvchi holat" kerak bo'lsa bu pattern to'g'ri kelmaydi, immutable snapshotni qayta bind qilish kerak. Java 25'dan past versiyalarda `--enable-preview` talab qilinadi va `KEY.get()` bog'lanmagan qamrovda `NoSuchElementException` tashlaydi, shuning uchun `orElse`/`isBound` ishlatish xavfsizroq. `call` ning `X` turi lambda tashlagan istisnolardan chiqariladi: ikki xil checked istisno bo'lsa `X` ularning umumiy ota sinfiga, ya'ni `Exception` ga keng tortiladi va chaqiruvchi `throws IOException, ServletException` deb e'lon qilgan bo'lsa ham kod kompilyatsiya bo'lmaydi. Shuning uchun yuqoridagi misolda aniq qayta tashlash (precise rethrow) bor. Bitta checked istisno bo'lganda bunday o'ram kerak emas.

## 4.26 Asinxron metod chaqiruvi (Asynchronous Method Invocation)

**Tavsif:** Chaqiruvchi metod natijasini kutib turmaydi: chaqiruv darhol qaytadi, haqiqiy ish esa boshqa thread'da bajariladi va natija kelajakda `Future`/`CompletableFuture` orqali olinadi. Bu latency'ni foydalanuvchi ko'zidan yashiradi va fon ishlarini so'rov oqimidan ajratadi. Spring'da bu pattern deklarativ: metod ustiga annotatsiya qo'yiladi, proxy esa chaqiruvni `TaskExecutor`ga topshiradi, shuning uchun biznes-kod thread boshqarishdan xabardor bo'lmaydi.

**Spring'da qayerda uchraydi:** `@EnableAsync` + `@Async` (Spring Framework 6.x/7.x), ortida `AsyncAnnotationBeanPostProcessor` va `AsyncExecutionInterceptor` turadi. Executor'ni `AsyncConfigurer.getAsyncExecutor()` bilan yoki `@Async("myExecutor")` qiymati bilan belgilanadi; Spring Boot 3.x `applicationTaskExecutor` (`ThreadPoolTaskExecutor`) ni avtomatik yaratadi va `spring.task.execution.pool.*` orqali sozlanadi. `void` qaytaruvchi metodlardagi exception'lar `AsyncUncaughtExceptionHandler`ga boradi, qolganlari `CompletableFuture` ichida qoladi. Kontekst uzatish uchun `TaskDecorator` va `DelegatingSecurityContextAsyncTaskExecutor`, event'lar uchun `ApplicationEventMulticaster`ga executor berish (`@EventListener` + `@Async`), rejalashtirish uchun esa `@Scheduled` ishlatiladi.

**Qo'llanish keyslari:**
- Ro'yxatdan o'tgandan keyin tasdiqlash email yoki push xabarini fonda yuborish.
- Audit log va analytics event'larini so'rov javobini kechiktirmasdan yozish.
- Hisobot yoki PDF generatsiyasini fonda ishga tushirib, foydalanuvchiga job id qaytarish.
- Bir nechta tashqi API'ni `CompletableFuture` qaytaruvchi `@Async` metodlar bilan parallel chaqirish.
- Cache'ni oldindan isitish (warm-up) yoki indeksni fonda qayta qurish.

**Ehtiyot bo'ling:** `@Async` proxy orqali ishlaydi - xuddi shu bean ichidan o'zini chaqirsangiz (self-invocation) annotatsiya butunlay e'tiborsiz qoladi va metod sinxron bajariladi; shuningdek `private`/`final` metodlarda ishlamaydi. `@Async` yangi thread'da `@Transactional` tranzaksiyani meros qilmaydi (`ThreadLocal`dagi tranzaksiya ko'chmaydi) va standart `SimpleAsyncTaskExecutor` chegarasiz thread yaratadi - har doim queue va pool chegarasi aniq belgilangan `ThreadPoolTaskExecutor` ko'rsating.

```java
// Asinxron metod chaqiruvi: natija keyinroq keladi
@Service
public class StatementService {

    @Async("reportExecutor")                  // aniq executor: default'ga tayanmang
    public CompletableFuture<Path> build(long accountId) {
        Path file = render(accountId);
        return CompletableFuture.completedFuture(file);
    }
}
// @Async proxy orqali ishlaydi: o'z sinfi ichidan chaqirilsa ishlamaydi,
// va `void` qaytarsa xato jimgina yo'qoladi.
```

## 4.27 Semaphore va concurrency chegarasi (Semaphore / Concurrency Limit)

**Tavsif:** Bir vaqtning o'zida resursdan foydalanayotgan bajaruvchilar sonini ruxsatnomalar (permit) soni bilan chegaralaydi: permit bo'lmasa, thread kutadi yoki darhol rad etiladi. Bu bulkhead vazifasini bajaradi - bitta sekin downstream butun ilovaning barcha thread'larini yutib ketishiga yo'l qo'ymaydi va yukni bashorat qilinadigan darajada ushlab turadi. Rate limiting'dan farqi shunda: bu yerda "vaqt birligidagi so'rov soni" emas, balki "bir paytda ishlayotgan ish soni" chegaralanadi.

**Spring'da qayerda uchraydi:** `java.util.concurrent.Semaphore` (`tryAcquire(timeout, unit)`); Spring'da `SimpleAsyncTaskExecutor.setConcurrencyLimit(...)` va `ConcurrencyThrottleSupport`, AOP uchun `org.springframework.aop.interceptor.ConcurrencyThrottleInterceptor`. Resilience4j - `@Bulkhead` (SemaphoreBulkhead) va `@RateLimiter`, Spring Boot 3.x bilan `resilience4j-spring-boot3` orqali. Reactor'da `flatMap(mapper, concurrency)` va `limitRate(...)`. Infratuzilma darajasida: HikariCP `maximumPoolSize` aslida DB uchun semaphore, Tomcat `server.tomcat.threads.max` va `max-connections`, Spring Cloud Gateway'da `RequestRateLimiter` filter'i, Kafka'da `max.poll.records` va listener `concurrency`. Virtual thread'lar davrida chegaralash uchun asosiy vosita aynan `Semaphore`.

**Qo'llanish keyslari:**
- Sekin yoki qimmat tashqi API'ga bir vaqtda ketadigan chaqiruvlar sonini 10 ta bilan chegaralash.
- Virtual thread'lar yoqilgan ilovada DB pool'ini toshirib yubormaslik uchun bulkhead qo'yish.
- Og'ir hisobot generatsiyasini bir paytda faqat N ta bajarilishiga ruxsat berish.
- Fayl yuklash yoki rasm konvertatsiyasi kabi xotira talab qiluvchi ishlarni cheklash.
- Downstream partnyorning kontraktdagi concurrency limitiga rioya qilish.

**Ehtiyot bo'ling:** `acquire()`ni timeout'siz chaqirish sekin downstream'da butun ilovani muzlatib qo'yadi - `tryAcquire(timeout, unit)` bilan tez fail qilish va fallback berish to'g'ri; `release()` har doim `finally` blokida bo'lsin, aks holda permit'lar asta-sekin "yo'qolib", tizim butunlay to'xtaydi. Lokal semaphore faqat bitta instansiyada amal qiladi: 10 ta pod'da chegara avtomatik 10 barobar oshadi, shuning uchun global limit uchun taqsimlangan rate limiter (masalan Redis asosidagi) kerak.

```java
// Semaphore: tashqi tizimga bir vaqtda necha chaqiruv ketishini cheklash
private final Semaphore permits = new Semaphore(10);

public Quote fetch(QuoteRequest r) throws InterruptedException {
    if (!permits.tryAcquire(100, TimeUnit.MILLISECONDS)) {
        throw new OverloadedException();      // navbatda kutmaydi
    }
    try {
        return pspClient.quote(r);
    } finally {
        permits.release();                    // finally shart
    }
}
```

## 4.28 Nusxaga qamash (Instance Confinement)

**Tavsif:** Thread-safe bo'lmagan obyektni thread-safe sinf ichiga to'liq berkitadi va unga kirishning barcha yo'llarini sinfning o'z metodlariga va o'z qulfiga bo'ysundiradi. G'oya oddiy: inkapsulyatsiya qamashni qo'llab-quvvatlaydi, chunki berkitilgan obyektga tegadigan kod yo'llari ma'lum va sanoqli bo'lib qoladi, demak ularni tahlil qilish butun dastur bo'ylab tarqalgan havolalarni tahlil qilishdan ancha oson. Qamash va qulflash intizomi birga ishlatilsa, ichida thread-safe bo'lmagan `HashSet` yoki `ArrayList` saqlagan sinf ham thread-safe bo'ladi. Shart bitta: qamalgan obyekt mo'ljallangan qamrovidan chiqib ketmasligi kerak, obyektlar esa o'zlari qochib ketmaydi, ularni dasturchi nashr qilib yuboradi.

**Spring'da qayerda uchraydi:** Bu `@Service` va `@Component` singleton beanlarda holat saqlashning asosiy to'g'ri shakli: ichki to'plam `private final`, hamma metod bitta `private final Object lock` yoki `ReentrantLock` ostida ishlaydi, getter esa ichki to'plamni emas, `List.copyOf(...)` nusxasini qaytaradi. JDK ichida `Collections.synchronizedList`, `synchronizedMap` va `synchronizedSet` o'ramlari aynan shu patternga quriladi: asosdagi to'plam o'ramga qamalgan va hamma metod o'ramning monitorini oladi. Spring Framework da `ConcurrentReferenceHashMap` segment holatini shu uslubda berkitadi, `AbstractApplicationContext` esa `applicationListeners` to'plamini qamab, kirishni o'z metodlariga tor qiladi.

**Qo'llanish keyslari:**
- Singleton bean ichida ishlatiladigan `HashMap` yoki `ArrayList` ni qulf ostida berkitib thread-safe API chiqarish.
- Uchinchi tomon kutubxonasining thread-safe bo'lmagan klientini o'z adapteringiz ichiga qamab ishlatish.
- `SimpleDateFormat` yoki shunga o'xshash mutable yordamchini sinf ichida qulf ostida yoki thread ga qamab ishlatish.
- Hisoblagichlar va jamlanmalardan iborat ichki statistika holatini bitta qulf ostida yig'ish.
- Legacy sinfni o'zgartirmasdan uning ustiga thread-safe fasad qurish.

**Ehtiyot bo'ling:** Patternni buzadigan narsa bitta: qamalgan havolaning chiqib ketishi. Ichki to'plamni to'g'ridan-to'g'ri qaytarish, uni listener yoki callback ga berish, `Iterator` chiqarish yoki konstruktorda `this` ni ro'yxatga yozib qo'yish qamashni bekor qiladi va sinxronlash siyosati jim buziladi (architect 11.13). Qulf ichidan begona kod chaqirmang: `forEach` ga tashqaridan kelgan lambda berish qulfni sizga tanish bo'lmagan kodga uzatadi.

```java
@Service
public class PersonRegistry {
    private final Set<Person> people = new HashSet<>();   // thread-safe EMAS
    private final Object lock = new Object();             // qamalgan holatning qulfi

    public void add(Person p) {
        synchronized (lock) { people.add(p); }
    }

    public boolean contains(Person p) {
        synchronized (lock) { return people.contains(p); }
    }

    public Set<Person> snapshot() {
        synchronized (lock) { return Set.copyOf(people); } // nusxa, "live" ko'rinish emas
    }
}
```

**Kitob asosi:** Brian Goetz va boshqalar, *Java Concurrency in Practice*, Addison-Wesley, 2006, 4.2-bo'lim (39-40-bet).

## 4.29 Thread xavfsizligini delegatsiya qilish (Delegating Thread Safety)

**Tavsif:** Sinf o'zi qulf ishlatmaydi, balki holatini allaqachon thread-safe bo'lgan komponentga topshiradi va o'zining thread safety ini shu komponentdan "meros" qilib oladi. Bu eng arzon yo'l, chunki hech qanday sinxronlash kodi yozilmaydi: `ConcurrentHashMap` yoki `AtomicLong` o'z ichidagi kafolatni beradi, o'rab turuvchi sinf esa faqat API ni shakllantiradi. Lekin delegatsiya shartli ishlaydi va shart aniq: delegatsiya faqat holat o'zgaruvchilari **mustaqil** bo'lganda, ya'ni ular orasida birgalikdagi invariant bo'lmaganda to'g'ri bo'ladi. Ikki mustaqil thread-safe maydon ustida ishlaydigan sinf thread-safe; ikki maydon bir-biriga bog'liq shart bilan bog'langan bo'lsa (masalan `lower <= upper`), ikkisi ham `AtomicInteger` bo'lsa ham sinf thread-safe emas, chunki ikkisini birga atomar o'zgartirish mumkin emas.

**Spring'da qayerda uchraydi:** Micrometer `MeterRegistry` implementatsiyalari hisoblagichlarni `ConcurrentHashMap` va atomic sinflarga delegatsiya qiladi. Spring ning ichki cache larining ko'pi (`ConcurrentReferenceHashMap`, `AnnotationUtils` cache lari, `DefaultSingletonBeanRegistry.singletonObjects`) xuddi shu uslubda: sinfning o'zida `synchronized` yo'q, kafolat map dan keladi. `ConcurrentMapCacheManager` esa `Cache` abstraksiyasini `ConcurrentHashMap` ga delegatsiya qiladi. Ilova kodida bu `@Service` ichidagi `ConcurrentHashMap` yoki `LongAdder` maydonlari shaklida uchraydi.

**Qo'llanish keyslari:**
- Mustaqil hisoblagichlar va o'lchovlarni `LongAdder` yoki `AtomicLong` maydonlarga topshirish.
- Kalit bo'yicha mustaqil yozuvlarni saqlovchi registr yoki ro'yxatni `ConcurrentHashMap` ga topshirish.
- Faqat almashtiriladigan (o'zgartirilmaydigan) konfiguratsiya snapshotini `AtomicReference` ga topshirish.
- Ishlab chiqaruvchi va iste'molchi orasidagi buferni `BlockingQueue` ga topshirish.
- Immutable qiymat obyektlarini saqlaydigan `CopyOnWriteArrayList` ustida listener ro'yxatini qurish.

**Ehtiyot bo'ling:** Eng ko'p uchraydigan xato invariantni sezmaslik. Agar ikki maydon birgalikda shart saqlasa, delegatsiya yetarli emas va qulf kerak bo'ladi; `AtomicInteger` lar sonini oshirish yordam bermaydi. Ikkinchi tuzoq asosdagi holatni nashr qilib yuborish: `ConcurrentHashMap` ni yoki uning `values()` ko'rinishini to'g'ridan-to'g'ri qaytarsangiz, chaqiruvchi sizning invariantingizni buzadigan o'zgarish kirita oladi; `Collections.unmodifiableMap` esa faqat o'ramni himoyalaydi, ichidagi mutable obyektlarni emas. Uchinchisi: bir nechta delegatga ketma-ket chaqiruv atomar emas, ya'ni `map.get` keyin `map.put` qo'shma amal bo'lib qoladi (architect 11.16).

```java
@Service
public class VehicleTracker {
    // delegat: kalitlar mustaqil, Point immutable, invariant yo'q
    private final ConcurrentMap<String, Point> locations = new ConcurrentHashMap<>();

    public void setLocation(String id, int x, int y) {
        if (locations.replace(id, new Point(x, y)) == null) {
            throw new IllegalArgumentException("noma'lum vosita: " + id);
        }
    }

    public Map<String, Point> snapshot() {
        return Map.copyOf(locations);      // ichki map chiqib ketmaydi
    }
}

record Point(int x, int y) {}              // immutable bo'lishi SHART
```

**Kitob asosi:** Brian Goetz va boshqalar, *Java Concurrency in Practice*, Addison-Wesley, 2006, 4.3-bo'lim, jumladan 4.3.2 (mustaqil holat o'zgaruvchilari) va 4.3.4 (asosdagi holatni nashr qilish), 41-47-bet.

## 4.30 Mijoz tomonida qulflash va kompozitsiya o'rami (Client-Side Locking / Composition)

**Tavsif:** Mavjud thread-safe sinfga yangi atomar amal qo'shish kerak bo'lganda to'rt yo'l bor va ularning narxi bir xil emas. Eng xavfsizi amalni sinfning o'ziga qo'shish, chunki sinxronlash siyosatini amalga oshiruvchi butun kod bitta faylda qoladi. Ikkinchisi sinfni extend qilish: `Vector` ni extend qilib `putIfAbsent` qo'shish ishlaydi, lekin kitob buni mo'rt deb ataydi, chunki sinxronlash siyosati endi alohida saqlanadigan bir nechta faylga tarqaladi; asosdagi sinf holatini himoyalash uchun boshqa qulfga o'tsa, subclass jim va sezdirmasdan buziladi. Uchinchisi mijoz tomonida qulflash: yordamchi sinfga kod yoziladi, lekin **mijoz obyektning o'z qulfini** oladi. To'rtinchisi va eng mustahkami kompozitsiya: o'z qulfi bilan o'ram yoziladi va asosdagi to'plam shu o'ramga qamaladi.

Mijoz tomonidagi qulflashning asosiy tuzog'i aynan shu yerda: yordamchi sinfda `synchronized` metod yozish **noto'g'ri qulfni** oladi (yordamchining o'zini), demak hech narsa himoyalanmaydi. To'g'ri shakl ro'yxatning o'zi ustida `synchronized` blok ochish, ya'ni `Collections.synchronizedList` o'rami ishlatadigan qulfni olish. Bu ishlaydi, lekin sinfning sinxronlash siyosatiga tashqaridan bog'lanish degani, shuning uchun kitob kompozitsiyani afzal ko'radi.

**Spring'da qayerda uchraydi:** `Collections.synchronizedXxx` o'ramlari qaytargan obyektlar o'zlarining monitorini qulf sifatida ishlatadi, shuning uchun ular ustida qo'shma amal bajarish uchun mijoz tomonida qulflash yoki kompozitsiya kerak bo'ladi. Amalda zamonaviy Java da bu patternlarning ko'pi kerak emas, chunki `ConcurrentMap` tayyor atomar amallar beradi: `putIfAbsent`, `replace`, `remove(k, v)`, `compute`, `computeIfAbsent` va `merge`. Spring Framework da kompozitsiya shaklini `ConcurrentWebSocketSessionDecorator` ko'rsatadi: u asosdagi `WebSocketSession` ni o'rab, yozishni o'z qulfi va buferi ostida seriyalashtiradi.

**Qo'llanish keyslari:**
- Thread-safe to'plamga "yo'q bo'lsa qo'sh" turidagi atomar amal qo'shish.
- `Collections.synchronizedList` ustida ikki amaldan iborat tekshiruv plus o'zgartirishni atomar qilish.
- Manba kodini o'zgartirish imkoni bo'lmagan uchinchi tomon thread-safe sinfiga amal qo'shish.
- Iteratsiya va o'zgartirishni bitta atomar oynada ushlash.
- Asosdagi to'plamni butunlay berkitib, faqat kerakli amallarni chiqaradigan tor API berish.

**Ehtiyot bo'ling:** Yordamchi sinfda `synchronized` metod yozish eng mashhur xato: u yordamchining qulfini oladi, ro'yxatning qulfini emas, va test da hech qachon ko'rinmaydi. Extend qilish yo'lini tanlasangiz, asosdagi sinfning sinxronlash siyosati spetsifikatsiyada qotirilganini tekshiring (`Vector` da qotirilgan, ko'p sinfda yo'q). Kompozitsiya bitta qo'shimcha qulf qatlami qo'shadi, ya'ni ikki marta qulflash narxi bor, lekin odatda bu narx mustahkamlikka arzonli to'lov.

```java
// yomon: yordamchining o'z qulfini oladi, ro'yxat qulfini EMAS
public class BadListHelper<E> {
    public final List<E> list = Collections.synchronizedList(new ArrayList<>());
    public synchronized boolean putIfAbsent(E x) {        // noto'g'ri qulf
        boolean absent = !list.contains(x);
        if (absent) { list.add(x); }
        return absent;
    }
}

// yaxshi: kompozitsiya, o'ram o'z qulfi bilan asosdagi ro'yxatni qamaydi
public class SafeList<E> {
    private final List<E> list;                           // qamalgan
    private final Object lock = new Object();

    public SafeList(List<E> list) { this.list = list; }

    public boolean putIfAbsent(E x) {
        synchronized (lock) {
            boolean absent = !list.contains(x);
            if (absent) { list.add(x); }
            return absent;
        }
    }
}
```

**Kitob asosi:** Brian Goetz va boshqalar, *Java Concurrency in Practice*, Addison-Wesley, 2006, 4.4-bo'lim (47-bet) va 4.4.1-bo'lim (47-49-bet).

## 4.31 Natija keshi (Memoizer / Result Cache)

**Tavsif:** Qimmat hisoblash natijasini kalit bo'yicha keshlaydi, lekin bitta qo'shimcha talab bilan: bir xil kalit uchun hisoblash **bir marta** bajarilishi kerak, hatto bir necha thread bir vaqtda so'rasa ham. Sodda yechimlar ketma-ket buziladi. Butun metodni `synchronized` qilish keshni ketma-ketlashtiradi, ya'ni keshning butun maqsadi yo'qoladi. `HashMap` ni `ConcurrentHashMap` ga almashtirish parallellikni tiklaydi, lekin ikki thread bir vaqtda "yo'q" deb ko'rib bir xil qiymatni ikki marta hisoblaydi. Yechim kitobning asosiy nayrangi: map da **qiymat emas, `Future` saqlanadi**. Birinchi kelgan thread `FutureTask` ni `putIfAbsent` bilan atomar joylaydi va hisoblashni boshlaydi; keyingilar mavjud `Future` ni topib `get()` da kutadi, demak hisoblash takrorlanmaydi. `putIfAbsent` ning atomarligi zarur, chunki `get` keyin `put` qo'shma amali bu oynani yopmaydi.

**Spring'da qayerda uchraydi:** Bu idioma `ConcurrentHashMap.computeIfAbsent` sifatida tilga kirib keldi: mapper atomar bajariladi va bir xil kalit uchun bir marta chaqiriladi. Caffeine ning `LoadingCache` i aynan shu semantikani beradi va uni "cache stampede" dan himoya sifatida reklama qiladi; Spring Cache abstraksiyasi (`@Cacheable`) esa o'zi bu kafolatni bermaydi, shuning uchun Caffeine da `sync = true` yoki provayder darajasidagi loader ishlatiladi. Spring ichida `AnnotationUtils` va `ReflectionUtils` cache lari, `ConcurrentReferenceHashMap` ustida qurilgan metadata cache lari shu naqshga tayanadi.

**Qo'llanish keyslari:**
- Qimmat parsing yoki kompilyatsiya natijasini (regex, template, sxema) kalit bo'yicha bir marta hisoblash.
- Tashqi tizimdan kelgan ma'lumotni keshlab, bir vaqtda kelgan bir xil so'rovlar uchun bitta chaqiruv qilish.
- Reflection yoki annotatsiya metadatasini sinf bo'yicha bir marta yig'ish.
- Og'ir klient yoki ulanish obyektini kalit bo'yicha bir marta qurish.
- Cache stampede ni oldini olish: issiq kalit muddati tugaganda yuzlab thread bir xil hisoblashni boshlamasligi.

**Ehtiyot bo'ling:** `Future` ni keshlash kitobning o'zi ogohlantirgan yangi muammoni keltiradi: kesh ifloslanishi (cache pollution). Hisoblash bekor qilinsa yoki xato bilan tugasa, keyingi urinishlar ham shu bekor qilish yoki xatoni ko'radi, chunki map da buzilgan `Future` qolgan. Shuning uchun bekor qilishni (va qayta urinish ma'noli bo'lsa `RuntimeException` ni) sezib `Future` ni map dan olib tashlash kerak. Kitob yana ikki narsani oshkor qoldiradi va ularni o'zingiz hal qilasiz: muddati o'tishi (expiration) va siqib chiqarish (eviction). Shu sababli amalda o'z `Memoizer` ini yozish o'rniga Caffeine olinadi. Oxirgi tuzoq: `computeIfAbsent` ichida uzoq I/O qilish map segmentini bloklaydi va shu map ga qayta kirish (rekursiv `computeIfAbsent`) deadlock beradi.

```java
@Service
public class SchemaCache {
    private final ConcurrentMap<String, Future<Schema>> cache = new ConcurrentHashMap<>();

    public Schema get(String name) throws InterruptedException {
        while (true) {
            Future<Schema> f = cache.get(name);
            if (f == null) {
                FutureTask<Schema> task = new FutureTask<>(() -> compile(name));
                f = cache.putIfAbsent(name, task);     // atomar: faqat bittasi o'tadi
                if (f == null) { f = task; task.run(); }
            }
            try {
                return f.get();
            } catch (CancellationException e) {
                cache.remove(name, f);                 // kesh ifloslanishini tozalash
            } catch (ExecutionException e) {
                cache.remove(name, f);
                throw new IllegalStateException(e.getCause());
            }
        }
    }

    private Schema compile(String name) { /* qimmat ish */ return new Schema(name); }
}
```

**Kitob asosi:** Brian Goetz va boshqalar, *Java Concurrency in Practice*, Addison-Wesley, 2006, 5.6-bo'lim (64-69-bet), `Memoizer` ning yakuniy implementatsiyasi 69-bet.

## 4.32 Ketma-ket thread qamashi va ownership uzatish (Serial Thread Confinement)

**Tavsif:** Mutable obyektni sinxronlashsiz xavfsiz ishlatishning yana bir yo'li: obyekt bir vaqtda faqat bitta threadga tegishli bo'ladi, lekin bu egalik (ownership) bir threaddan ikkinchisiga **uzatiladi**. Uzatish uchun uch shart bajariladi: obyekt xavfsiz nashr qilinadi, uni faqat bitta boshqa thread oladi, va uzatgan thread undan keyin obyektga qaytib tegmaydi. Xavfsiz nashr obyekt holatining yangi egaga ko'rinishini ta'minlaydi, uzatganning qaytib tegmasligi esa obyektni endi yangi threadga qamalgan qiladi. Natijada yangi ega obyektni erkin o'zgartirishi mumkin, chunki unga eksklyuziv kirish bor. `java.util.concurrent` dagi bloklovchi navbatlar bu uzatishni osonlashtiradi: ularning ichida obyektni ishlab chiqaruvchi threaddan iste'molchi threadga xavfsiz nashr qilish uchun yetarli sinxronlash bor.

**Spring'da qayerda uchraydi:** `BlockingQueue` orqali qurilgan har qanday ishlab chiqaruvchi-iste'molchi oqimi (4.2) shu patternga tayanadi: navbatga qo'yilgan DTO yoki buferni iste'molchi erkin o'zgartiradi. Spring Integration ning `QueueChannel` i va Spring AMQP, Spring Kafka listener container lari xabarni ichki navbat orqali ishchi threadga uzatganda xuddi shu kafolatga tayanadi. Obyekt pool lari ham shu patternni ekspluatatsiya qiladi: HikariCP `Connection` ni so'ragan threadga "qarzga" beradi va qaytarilmaguncha boshqasiga bermaydi, shuning uchun `Connection` so'rov davomida shu threadga qamalgan bo'ladi (architect 11.17).

**Qo'llanish keyslari:**
- Og'ir mutable bufer yoki yig'ma obyektni `BlockingQueue` orqali ishchi threadga topshirish.
- Fayl yoki hisobot bo'lagini tayyorlab, uni yozuvchi threadga uzatish.
- Obyekt pool i (ulanish, bufer, parser) orqali resursni vaqtincha bitta threadga berish.
- Bir bosqichli konveyerda (pipeline) har bosqich o'z navbatidan obyekt olib, o'zgartirib, keyingisiga uzatish.
- `ConcurrentMap.remove` yoki `AtomicReference.compareAndSet` bilan obyektni aniq bitta oluvchiga topshirish.

**Ehtiyot bo'ling:** Patternning yagona, lekin jim buziladigan sharti uzatgandan keyin tegmaslik. Ishlab chiqaruvchi navbatga qo'ygan obyektga log yozish uchun yoki "oxirgi yuborilgan" maydonida saqlab qo'yish uchun qaytib tegsa, pattern buziladi va natija poyga bo'ladi. Shuning uchun navbatga qo'yilgan obyektga mahalliy havolani darhol yo'qotish amaliy intizom. Pool bilan ishlaganda ikkinchi shart: obyektni qaytargandan keyin ishlatish (`Connection` ni `close` dan keyin ishlatish) xuddi shu buzilishning klassik ko'rinishi. Agar uzatishni navbat o'rniga boshqa mexanizm bilan qursangiz, obyektni **aniq bitta** thread olishini ta'minlash sizning zimmangizda qoladi.

```java
// ishlab chiqaruvchi: obyekt navbatga qo'yilgandan keyin unga TEGILMAYDI
public void produce(Path file) throws InterruptedException {
    ReportChunk chunk = new ReportChunk(file);   // mutable, hozir bizga tegishli
    chunk.fill();
    queue.put(chunk);                            // egalik uzatildi
    // chunk ga bu yerdan keyin TEGMAYMIZ: havolani ham saqlamaymiz
}

// iste'molchi: endi eksklyuziv ega, sinxronlashsiz o'zgartiradi
public void consume() throws InterruptedException {
    while (!Thread.currentThread().isInterrupted()) {
        ReportChunk chunk = queue.take();        // xavfsiz nashr qilingan
        chunk.compress();                        // qulf kerak emas
        write(chunk);
    }
}
```

**Kitob asosi:** Brian Goetz va boshqalar, *Java Concurrency in Practice*, Addison-Wesley, 2006, 5.3.2-bo'lim (57-58-bet).

## 4.33 Zahar tabletka (Poison Pill)

**Tavsif:** Ishlab chiqaruvchi-iste'molchi servisini to'xtatishning navbat orqali ishlaydigan usuli: navbatga tanib olinadigan maxsus obyekt qo'yiladi va uning ma'nosi "buni olgan bo'lsang, to'xta". FIFO navbat bilan birga bu muhim kafolat beradi: zahar tabletkadan **oldin** yuborilgan barcha ish tabletkadan oldin olinadi, demak iste'molchi to'xtashdan avval navbatdagi ishini oxiriga yetkazadi. Shu sababli poison pill `shutdownNow()` dan farq qiladi: `shutdownNow` navbatni bo'shatadi va bajarilayotganlarni uzadi, poison pill esa toza, ishni yo'qotmaydigan to'xtashni beradi. Protokolning qat'iy sharti: ishlab chiqaruvchi tabletkani navbatga qo'ygandan keyin boshqa hech qanday ish yubormaydi.

**Spring'da qayerda uchraydi:** Java da bu `BlockingQueue` ustidagi qo'l bilan yoziladigan protokol, tayyor API emas. Spring tomonida xuddi shu g'oya boshqa nomlar ostida uchraydi: Spring Batch da `ItemReader` ning `null` qaytarishi "ma'lumot tugadi" signali, Reactor da `onComplete` terminal signali, Spring Integration da esa `QueueChannel` ustida yozilgan to'xtatish xabari. Kafka va xabar brokerlari kontekstida "poison message" butunlay boshqa narsani bildiradi (qayta ishlab bo'lmaydigan, DLT ga ketadigan xabar) va ikkisini aralashtirmaslik kerak; brokerlar nuqtasidan bu patterns 16.35 da.

**Qo'llanish keyslari:**
- `BlockingQueue` ustida qurilgan indekslash yoki fayl crawler servisini ishni yo'qotmasdan to'xtatish.
- Ishlab chiqaruvchi tugaganini iste'molchiga bildirish, navbat bo'shashini kutish o'rniga.
- Graceful shutdown da navbatdagi barcha ishni bajarib keyin chiqish.
- Bir martalik batch oqimida oxirgi element belgisini oshkor qilish.
- Testda ishchi tsiklini aniq va deterministik to'xtatish.

**Ehtiyot bo'ling:** Kitobning cheklovi aniq: poison pill faqat ishlab chiqaruvchi va iste'molchi soni **ma'lum** bo'lganda ishlaydi. N iste'molchi bo'lsa N ta tabletka qo'yish kerak, chunki har biri bittasini iste'mol qiladi; M ishlab chiqaruvchi bo'lsa, har biri tugaganini sanab, oxirgisi tabletka qo'yishi kerak. Soni noma'lum bo'lsa pattern ishlamaydi. Ikkinchi cheklov: navbat chegarasiz bo'lsa yoki to'lib qolgan bo'lsa, `put` ning o'zi bloklanadi, shuning uchun tabletkani qo'yish ham kafolatlanmaydi. Uchinchisi: tabletka sifatida ishlatilgan obyekt haqiqiy ma'lumot bilan tasodifan teng bo'lmasligi kerak, shuning uchun identifikatsiya `equals` emas, havola tengligi (`==`) bilan qilinadi. Interrupt siyosati nuqtasidan bu architect 11.14 da.

```java
public class IndexingService {
    private static final Path POISON = Path.of("");          // tanib olinadigan belgi
    private final BlockingQueue<Path> queue = new LinkedBlockingQueue<>(1000);

    // ishlab chiqaruvchi tugaganda bitta tabletka qo'yadi va boshqa ish yubormaydi
    public void finishProducing() throws InterruptedException {
        queue.put(POISON);
    }

    // iste'molchi: havola tengligi bilan tekshiradi, equals bilan emas
    public void consume() throws InterruptedException {
        while (true) {
            Path file = queue.take();
            if (file == POISON) {
                return;                                      // navbatdagi ish tugagan
            }
            index(file);
        }
    }

    private void index(Path file) { /* ... */ }
}
```

**Kitob asosi:** Brian Goetz va boshqalar, *Java Concurrency in Practice*, Addison-Wesley, 2006, 7.2.3-bo'lim (97-98-bet).

## 4.34 Ochiq chaqiruv (Open Call)

**Tavsif:** Hech qanday qulf ushlanmagan holda metod chaqirish ochiq chaqiruv deb ataladi va faqat ochiq chaqiruvlarga tayanadigan sinflar ancha yaxshi xulqli va kompozitsiyaga qulay bo'ladi. Dalil dizayn darajasida: metod chaqiruvi abstraksiya to'sig'i, uning maqsadi narigi tomonda nima bo'layotganidan sizni himoyalash. Lekin aynan shuning uchun qulf ushlab turib begona (alien) metodni chaqirish tahlil qilib bo'lmaydigan va shuning uchun xavfli ish: narigi tomonda yana qulf olinishi mumkin va u sizga ko'rinmaydi. Kitob o'xshatishni aniq beradi: deadlock dan qochish uchun ochiq chaqiruvdan foydalanish thread safety uchun inkapsulyatsiyadan foydalanishga o'xshaydi. Inkapsulyatsiyasiz ham thread-safe dastur yozish mumkin, lekin tahlili ancha qiyin; xuddi shunday, faqat ochiq chaqiruvlarga tayanadigan dasturning liveness tahlili ancha oson, chunki bir nechta qulf oladigan kod yo'llarini aniqlash va ularda qulf tartibini bir xil ushlash osonlashadi.

**Spring'da qayerda uchraydi:** Eng ko'p uchraydigan buzilish listener va event ni qulf ostida chaqirish: `synchronized` blok ichida `ApplicationEventPublisher.publishEvent` qilish yoki callback ro'yxatini qulf ostida aylantirish. Spring ning o'zi bu tuzoqdan qochish uchun `CopyOnWriteArrayList` da listener larni saqlab, snapshot ustida qulfsiz iteratsiya qiladi. Xuddi shu qoida `@Transactional` ga ham tegishli: tranzaksiya ichida tashqi HTTP chaqiruvi qilish DB qulflarini tarmoq timeout i davomida ushlab turadi va bu architect 11.10 va architect 19 dagi klassik tuzoq. `@EventListener` ni `@Async` qilish yoki `TransactionSynchronization.afterCommit` ga ko'chirish amalda shu patternning qo'llanishi.

**Qo'llanish keyslari:**
- Listener, callback yoki `publishEvent` chaqiruvini qulf qamrovidan tashqariga chiqarish.
- Qulf ostida holat snapshot ini olib, qulfni bo'shatib, keyin snapshot ustida ishlash.
- Tranzaksiya yoki qulf ichidan tashqi HTTP va broker chaqiruvlarini `afterCommit` ga ko'chirish.
- Bir-biriga murojaat qiladigan ikki komponent orasidagi deadlock ni qulfni chiqarish bilan yechish.
- Override qilinadigan (`protected`, `public`) metodni qulf ostida chaqirmaslik, chunki subclass nima qilishini bilmaysiz.

**Ehtiyot bo'ling:** Qulfni chiqarish bepul emas: amal endi atomar bo'lmaydi. Qulf ichida holatni o'qib, qulfdan chiqib, keyin ish qilsangiz, oraliqda holat o'zgargan bo'lishi mumkin, demak yo kodni shu o'zgarishga chidamli (idempotent yoki versiya tekshiradigan) qilish, yo o'zgarish sodir bo'lganini sezib qayta urinish kerak. Shuning uchun refaktoring mexanik emas: avval amalning qaysi qismi rostdan atomar bo'lishi kerakligini aniqlash kerak. Ikkinchi ogohlantirish: ochiq chaqiruv deadlock ni imkonsiz qilmaydi, u faqat tahlilni mumkin qiladi; bir nechta qulf oladigan yo'llar qolsa, qulf tartibini global belgilash hamon kerak (architect 11.10).

```java
@Service
public class OrderBook {
    private final Object lock = new Object();
    private final List<Order> orders = new ArrayList<>();
    private final ApplicationEventPublisher events;

    public OrderBook(ApplicationEventPublisher events) { this.events = events; }

    public void add(Order order) {
        List<Order> snapshot;
        synchronized (lock) {           // qulf qamrovi faqat holat o'zgarishi
            orders.add(order);
            snapshot = List.copyOf(orders);
        }
        // ochiq chaqiruv: qulf bo'shatilgan, listener nima qilsa ham deadlock yo'q
        events.publishEvent(new OrderAdded(order, snapshot));
    }
}
```

**Kitob asosi:** Brian Goetz va boshqalar, *Java Concurrency in Practice*, Addison-Wesley, 2006, 10.1.4-bo'lim (131-132-bet).

## 4.35 Treiber steki: bloklanmaydigan stek (Treiber Stack / Non-blocking Stack)

**Tavsif:** Bloklanmaydigan bog'langan tuzilma qurishning kanonik namunasi va uning kaliti bitta g'oyada: atomar o'zgarish qamrovini **bitta o'zgaruvchiga** cheklash, shu bilan birga ma'lumot izchilligini saqlash. Stek buning uchun eng oson tuzilma, chunki har bir element faqat bitta boshqa elementga ishora qiladi va har bir elementga faqat bitta havola ishora qiladi. Shuning uchun butun stekning holati bitta `AtomicReference<Node> top` da ifodalanadi. `push` yangi node tayyorlaydi, uning `next` maydonini joriy `top` ga qaratadi va CAS bilan uni cho'qqiga o'rnatishga urinadi: cho'qqi o'zgarmagan bo'lsa CAS muvaffaqiyatli, o'zgargan bo'lsa CAS yiqiladi va `push` joriy holatga qarab node ni yangilab qaytadan urinadi. Ikki holatda ham stek CAS dan keyin izchil holatda qoladi.

Kitob shu misoldan barcha bloklanmaydigan algoritmlarning umumiy xususiyatini chiqaradi: ishning bir qismi **spekulyativ** bajariladi va qayta bajarilishi mumkin. Thread yangi node ni qurganda `next` havolasi o'rnatish paytigacha to'g'ri qolishiga umid qiladi, lekin raqobat bo'lsa qayta urinishga tayyor turadi. Thread safety esa `compareAndSet` ning o'zidan keladi: CAS, qulf kabi, atomarlikni ham, ko'rinuvchanlikni ham beradi. Holatni o'zgartirish `compareAndSet` bilan bajariladi va u volatile yozuvning xotira effektiga ega; holatni o'qish esa o'sha `AtomicReference` ning `get` i bilan bo'ladi va u volatile o'qishning effektiga ega. Shuning uchun bir thread kiritgan o'zgarish stekka qaragan har qanday boshqa threadga xavfsiz nashr qilinadi.

**Spring'da qayerda uchraydi:** O'z qo'lingiz bilan yozish kerak bo'lmaydi: JDK da `ConcurrentLinkedQueue` va `ConcurrentLinkedDeque` shu uslubda qurilgan, `ConcurrentSkipListMap` esa murakkabroq variantini beradi. Spring va Reactor ichida bu daraja ko'rinmaydi, lekin Reactor ning `Operators` dagi request accounting va Micrometer ning `DoubleAdder` ga tayangan hisoblagichlari xuddi shu CAS plus retry naqshiga quriladi. Umumiy CAS yozuvi 4.21 da.

**Qo'llanish keyslari:**
- Juda yuqori throughput li va qisqa kritik bo'limli LIFO bufer yoki free-list.
- Qulf raqobati o'lchangan va bloklanmaydigan tuzilmaga o'tish asoslangan issiq yo'l.
- Kontekst almashinuvi narxini yo'qotish kerak bo'lgan past latency li yo'l.
- Obyekt pool i ichidagi bo'sh elementlar steki.
- JDK dagi bloklanmaydigan to'plamlarning xulqini tushunish va thread dump da ularni o'qish.

**Ehtiyot bo'ling:** Kitobning birinchi gapi ogohlantirish: bloklanmaydigan algoritmlar qulfga asoslangan ekvivalentlaridan sezilarli murakkabroq. Qo'lda yozish deyarli har doim xato qaror, chunki memory model nozikliklari (`volatile`, happens-before) va ABA ehtimoli (architect 11.21) oson sezilmaydi; JDK dagi tayyor tuzilma deyarli har doim yaxshiroq. Ikkinchisi: stek oson, lekin navbat allaqachon qiyin, chunki bosh va dum ikkita havolani atomar yangilashni talab qiladi va bu bitta CAS ga sig'maydi. Uchinchisi: yuqori raqobatda retry tsikli CPU ni behuda yoqadi, demak bloklanmaydigan degani tezroq degani emas.

```java
// Treiber steki: butun holat bitta AtomicReference da
public class ConcurrentStack<E> {
    private final AtomicReference<Node<E>> top = new AtomicReference<>();

    public void push(E item) {
        Node<E> newHead = new Node<>(item);
        Node<E> oldHead;
        do {
            oldHead = top.get();
            newHead.next = oldHead;          // spekulyativ ish, qayta bajarilishi mumkin
        } while (!top.compareAndSet(oldHead, newHead));
    }

    public E pop() {
        Node<E> oldHead;
        Node<E> newHead;
        do {
            oldHead = top.get();
            if (oldHead == null) { return null; }
            newHead = oldHead.next;
        } while (!top.compareAndSet(oldHead, newHead));
        return oldHead.item;
    }

    private static final class Node<E> {
        final E item;
        Node<E> next;
        Node(E item) { this.item = item; }
    }
}
```

**Kitob asosi:** Brian Goetz va boshqalar, *Java Concurrency in Practice*, Addison-Wesley, 2006, 15.4.1-bo'lim (201-203-bet); Listing 15.6 Treiber (1986) algoritmiga havola qiladi, 203-bet.

## 4.36 Amalda qo'llash

- [ ] Loyihadagi har bir `ExecutorService` va `TaskExecutor` ni ro'yxatga olib, pool kattaligi, navbat hajmi va rejection siyosatini yozib qo'ying.
- [ ] Chegarasiz navbat (`LinkedBlockingQueue` parametrsiz) ishlatadigan pool'larni toping - ular xotira tugashiga olib keladi.
- [ ] `synchronized` bloklarni sanab chiqing va har biri ichida I/O yoki tashqi chaqiruv yo'qligini tasdiqlang.
- [ ] `ThreadLocal` ishlatadigan har bir joyni tekshirib, `finally` da tozalanayotganini va virtual thread bilan mos kelishini tasdiqlang.
- [ ] `CompletableFuture` chaqiruvlarida aniq Executor berilganini tekshiring; default `ForkJoinPool.commonPool()` blocking ish uchun mos emas.
- [ ] Virtual thread'ga o'tish nomzodlarini belgilang va ularda `synchronized` o'rniga `ReentrantLock` ishlatilganini tekshiring.
- [ ] Tashqi chaqiruvlar uchun `Semaphore` yoki bulkhead chegarasi borligini tekshiring; chegarasiz parallellik tashqi tizimni yiqitadi.
- [ ] O'zgarmas bo'lishi mumkin bo'lgan domen obyektlarini toping va ularni `record` yoki `final` maydonlarga o'tkazish rejasini tuzing.

## Manbalar

- [JEP 506: Scoped Values](https://openjdk.org/jeps/506) - `ScopedValue` Java 25 da yakuniy holat
- [openjdk/jdk, `java/lang/ScopedValue.java` (jdk-25-ga)](https://raw.githubusercontent.com/openjdk/jdk/jdk-25-ga/src/java.base/share/classes/java/lang/ScopedValue.java) - `Carrier.run(Runnable)`, `Carrier.call(CallableOp)` va `CallableOp<T, X extends Throwable>`
- [JLS 18.4, Resolution](https://docs.oracle.com/javase/specs/jls/se25/html/jls-18.html#jls-18.4) - lambda tashlagan istisnolardan `X` ning chiqarilishi
- Brian Goetz, *Java Concurrency in Practice*, 5-bob - qurilish bloklari: bloklovchi navbat, sinxronizatorlar, `Memoizer`
- Brian Goetz, *Java Concurrency in Practice*, 6-bob - vazifani bajarish va Producer-Consumer
- Brian Goetz, *Java Concurrency in Practice*, 8-bob - thread pool ni qo'llash va to'yinish siyosati
- Brian Goetz, *Java Concurrency in Practice*, 14-bob - shart navbatlari va Guarded Suspension
- Brian Goetz, *Java Concurrency in Practice*, 15-bob - atomik o'zgaruvchilar va bloklamaydigan algoritmlar
- Brian Goetz va boshqalar, *Java Concurrency in Practice*, Addison-Wesley, 2006, 4.2-bo'lim (39-40-bet) - nusxaga qamash (instance confinement), inkapsulyatsiyaning qamashni qo'llab-quvvatlashi va qamalgan obyektning qamrovidan chiqib ketmasligi sharti
- Brian Goetz va boshqalar, *Java Concurrency in Practice*, Addison-Wesley, 2006, 4.3-bo'lim (41-47-bet) - thread xavfsizligini delegatsiya qilish, mustaqil holat o'zgaruvchilari sharti va asosdagi holatni nashr qilish xavfi
- Brian Goetz va boshqalar, *Java Concurrency in Practice*, Addison-Wesley, 2006, 4.4 va 4.4.1-bo'lim (47-49-bet) - mavjud thread-safe sinfga amal qo'shishning to'rt yo'li, extend qilishning mo'rtligi, mijoz tomonida qulflashda noto'g'ri qulf tuzog'i va kompozitsiya o'rami
- Brian Goetz va boshqalar, *Java Concurrency in Practice*, Addison-Wesley, 2006, 5.6-bo'lim (64-69-bet) - natija keshi: qiymat emas `Future` ni keshlash, `putIfAbsent` ning atomarligi, kesh ifloslanishi va `Memoizer` ning yakuniy implementatsiyasi (69-bet)
- Brian Goetz va boshqalar, *Java Concurrency in Practice*, Addison-Wesley, 2006, 5.3.2-bo'lim (57-58-bet) - ketma-ket thread qamashi, egalikni uzatish uchun uch shart va obyekt pool ining shu patternga tayanishi
- Brian Goetz va boshqalar, *Java Concurrency in Practice*, Addison-Wesley, 2006, 7.2.3-bo'lim (97-98-bet) - zahar tabletka, FIFO navbatdagi ishni yo'qotmaslik kafolati va ishlab chiqaruvchi plus iste'molchi soni ma'lum bo'lishi cheklovi
- Brian Goetz va boshqalar, *Java Concurrency in Practice*, Addison-Wesley, 2006, 10.1.4-bo'lim (131-132-bet) - ochiq chaqiruv, qulf ushlab begona metod chaqirishning tahlil qilinmasligi va liveness tahlilini osonlashtirish dalili
- Brian Goetz va boshqalar, *Java Concurrency in Practice*, Addison-Wesley, 2006, 15.4.1-bo'lim (201-203-bet) - bloklanmaydigan stek, atomar o'zgarishni bitta o'zgaruvchiga cheklash, spekulyativ ish va `compareAndSet` ning atomarlik plus ko'rinuvchanlik effekti; Listing 15.6 Treiber (1986) ga havola qiladi (203-bet)
- Craig Walls, *Spring in Action* 6th, 11-bob - Reactor va reaktiv oqim
- Brian Goetz va boshqalar, *Java Concurrency in Practice*, 16.2.4 - double-checked locking ni anti-pattern deb belgilash, haqiqiy xavf (havolaning yangi, obyekt holatining eskirgan qiymati) va idiomaning endi keraksizligi
- [OpenJDK 25, `ForkJoinPool.java`](https://raw.githubusercontent.com/openjdk/jdk/jdk-25%2B36/src/java.base/share/classes/java/util/concurrent/ForkJoinPool.java) - `commonPool` parallelizmi `Math.max(1, availableProcessors() - 1)` va `ForkJoinPool.common.parallelism` property si
- [OpenJDK 25, `java.util.concurrent` package javadoc](https://raw.githubusercontent.com/openjdk/jdk/jdk-25%2B36/src/java.base/share/classes/java/util/concurrent/package-info.java) - happens-before munosabati va paket tarkibi
- [OpenJDK 25, `ConcurrentHashMap.java`](https://raw.githubusercontent.com/openjdk/jdk/jdk-25%2B36/src/java.base/share/classes/java/util/concurrent/ConcurrentHashMap.java) - lock striping, `computeIfAbsent` ning atomarligi va aggregate status metodlari
- [spring-framework, `DefaultSingletonBeanRegistry.java`](https://raw.githubusercontent.com/spring-projects/spring-framework/v7.0.0/spring-beans/src/main/java/org/springframework/beans/factory/support/DefaultSingletonBeanRegistry.java) - singleton cache da `ConcurrentHashMap` va `ReentrantLock` (`singletonLock`) bilan ikki marta tekshirish
- [OpenJDK 25, `ScopedValue.java`](https://raw.githubusercontent.com/openjdk/jdk/jdk-25%2B36/src/java.base/share/classes/java/lang/ScopedValue.java) - `where`/`run`/`call` API si, `StructuredTaskScope` bilan meros va kam sonda ishlatish tavsiyasi
- Herbert Schildt, *Java The Complete Reference*, 29-bob (1004-bet) - ketma-ket chegarani yuqoriga qarab tanlash, `ForkJoinTask` hujjatidagi 100 dan 10 000 gacha hisob qadami mo'ljali va `compute()` ichida `synchronized` yoki semafor ishlatmaslik (`Phaser` istisno)
- ESLATMA: kitobda yo'q, korpus qo'shgan qism - bo'limdagi `THRESHOLD = 10_000` qiymatini shu mo'ljalning yuqori chekkasi deb bog'lash

---

[&larr; 3. Xulq-atvor patternlari](03-xulq-atvor-patternlari.md) · [Mundarija](README.md) · [5. Spring Core ichidagi patternlar xaritasi &rarr;](05-spring-core-ichidagi-patternlar-xaritasi.md)
