<!-- doc: architect | chapter: 11 | part: II. Java chuqur bilim -->

[Barcha hujjatlar](../../README.md) / [Arxitektor miyasi](README.md)

> Holat: tekshirilmoqda. Da'volar hali manbaga solishtirilmoqda.

# 11. Concurrency: thread, lock, atomic, happens-before (Java Concurrency)

<details>
<summary>Bu bobdagi 23 bo'lim</summary>

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
- [11.12 Thread safety darajasini hujjatlash va ortiqcha sinxronlashdan qochish](#1112-thread-safety-darajasini-hujjatlash-va-ortiqcha-sinxronlashdan-qochish)
- [11.13 Xavfsiz nashr (safe publication) va obyektning qochib ketishi](#1113-xavfsiz-nashr-safe-publication-va-obyektning-qochib-ketishi)
- [11.14 Bekor qilish, interrupt siyosati va thread starvation deadlock](#1114-bekor-qilish-interrupt-siyosati-va-thread-starvation-deadlock)
- [11.15 Qulf raqobatini kamaytirish: qamrov, bo'lish, striping va issiq maydon](#1115-qulf-raqobatini-kamaytirish-qamrov-bolish-striping-va-issiq-maydon)
- [11.16 Qo'shma amal, intrinsic lock va reentrancy mexanikasi](#1116-qoshma-amal-intrinsic-lock-va-reentrancy-mexanikasi)
- [11.17 Thread ga qamash: ad-hoc, stack va `ThreadLocal` qamashi](#1117-thread-ga-qamash-ad-hoc-stack-va-threadlocal-qamashi)
- [11.18 Condition queue mexanikasi: shart predikati, yo'qolgan signal va kirish-chiqish protokoli](#1118-condition-queue-mexanikasi-shart-predikati-yoqolgan-signal-va-kirish-chiqish-protokoli)
- [11.19 `AbstractQueuedSynchronizer`: acquire va release protokoli](#1119-abstractqueuedsynchronizer-acquire-va-release-protokoli)
- [11.20 Qayta tartiblash, piggybacking va initsializatsiya xavfsizligi](#1120-qayta-tartiblash-piggybacking-va-initsializatsiya-xavfsizligi)
- [11.21 ABA muammosi va atomic field updater](#1121-aba-muammosi-va-atomic-field-updater)
- [11.22 Sinxronlashning o'lchangan narxi: kontekst almashinuvi va memory barrier](#1122-sinxronlashning-olchangan-narxi-kontekst-almashinuvi-va-memory-barrier)
- [11.23 Amalda qo'llash](#1123-amalda-qollash)

</details>



Konkurentlik kodni tezlashtirmaydi, u kodni qimmatlashtiradi. To'lov servisi sekundiga 2000 so'rovni ko'tarishi uchun ko'p oqimli bo'lishi shart, lekin har bir umumiy o'zgaruvchi, har bir singleton bean maydoni va har bir lock shu narxga qo'shimcha qator qo'shadi. Arxitektor uchun asosiy savol "qanday parallellashtiraman" emas, "qaysi holat umumiy va uni kim qanday tartibda ko'radi" degan savol. Bu bobda JVM ichida nima sodir bo'lishini, Java Memory Model qanday kafolat berishini va Spring konteynerida bu kafolatlar qanday buzilishini ko'rib chiqamiz.

## 11.1 Parallellik va konkurentlik farqi, qaysi muammoni hal qilamiz

Konkurentlik bir nechta ishni bir vaqtda boshqarish haqida, parallellik esa ularni bir vaqtda bajarish haqida. Buyurtma servisi 200 ta so'rovni navbatga olib, bittadan ishlasa, bu konkurent lekin parallel emas. Shu farq muhim, chunki ikki holatda butunlay boshqa muammo hal qilinadi: konkurentlik resursni kutish vaqtini to'ldiradi, parallellik CPU vaqtini qisqartiradi.

Amalda arxitektor ikki qonunga tayanadi. Birinchisi Little qonuni: kerakli bir vaqtdagi ish soni throughput ni latency ga ko'paytirganga teng. Hisobot servisi 500 RPS ni 200 ms latency bilan ushlasa, tizimda doim taxminan 100 ta faol so'rov yashaydi, demak thread pool va DB connection pool shuni ko'tarishi kerak. Ikkinchisi Amdahl qonuni: agar ishning 5 foizi ketma-ket bo'lsa, 32 yadroda maksimal tezlanish taxminan 14 barobar, 64 yadroda esa faqat 15 barobar. Ya'ni bitta global lock ostidagi 5 foizlik kod butun gorizontal o'sishni o'ldiradi.

Shu sababli birinchi qaror doim arxitektura darajasida bo'ladi: umumiy holatni yo'q qilish, bo'lib tashlash yoki tashqi tizimga (PostgreSQL, Redis) ko'chirish. Lock qo'yish uchinchi variant, eng oxirgi variant.

Amdahl qonunining to'liq yozuvi va ketma-ket ulush jadvali [napkin math bobida](08-ishlash-va-resurs-hissi-napkin-math.md#811-amdahl-qonuni-ketma-ket-ulush-masshtablanishning-chegarasi).

Ikkinchi qaror kodni joylashtirishga tegishli: konkurentlik bilan ishlaydigan kod biznes mantiqidan ajratiladi. Thread yaratish, pool sozlash, qulf olish va bekor qilishni kuzatish alohida sinflarda yashaydi, biznes qoidasi esa bitta threadda bajarilayotgandek yoziladi. Sababi ikki tomonlama: aralash kod ikki xil o'zgarish sababiga ega bo'ladi (biznes qoidasi va konkurentlik strategiyasi), va konkurentlik xatosini test bilan ushlash uchun konkurentlik qismini alohida sinash kerak bo'ladi. Amalda bu Spring da `@Async`, `ExecutorService` bean i va `TaskExecutor` sozlamasini infratuzilma qatlamida ushlash, domen servisini esa ulardan xabarsiz qoldirish shaklini oladi.

Uchinchi qaror atamada. "Bu kod thread-safe mi" savoliga javob berishdan oldin gap qaysi bajarilish konteksti haqida ketayotganini aniqlash kerak, aks holda suhbat bir-biriga tegmaydigan ikki narsa haqida boradi. Fowler bu atamalar uchun standart lug'at yo'qligini ochiq aytadi va o'zi ishlatadiganlarini sanab beradi (Fowler, *Patterns of Enterprise Application Architecture*, Addison-Wesley, 2003, 5-bob, 65-66-betlar):

| Kontekst | Fowler ning ta'rifi | Spring va PostgreSQL tomonda |
|---|---|---|
| So'rov (request) | Tashqaridan kelgan bitta chaqiruv; ishlov asosan serverda, klient javobni kutadi deb hisoblanadi | bitta HTTP chaqiruv, `DispatcherServlet` dan controller gacha |
| Sessiya (session) | Klient va server orasidagi uzoq muloqot; odatda foydalanuvchi bitta izchil mantiqiy ketma-ketlik deb ko'radigan bir nechta so'rov | `HttpSession`, va server o'zi klient bo'lgan joyda baza sessiyasi |
| Jarayon (process) | Odatda og'ir kontekst, ichki ma'lumoti uchun ko'p izolyatsiya beradi | JVM processi; PostgreSQL tomonda har ulanish uchun alohida backend |
| Thread | Yengilroq faol agent, bitta jarayonda bir nechtasi ishlaydi | `ExecutorService`, request-per-thread model |
| Tranzaksiya | Klient bitta so'rov kabi ko'rishni xohlagan bir nechta so'rovni birlashtiradi; tizim tranzaksiyasi va biznes tranzaksiyasi deb ikkiga bo'linadi | `@Transactional` va uning tashqarisidagi biznes oqimi |

Fowler ikki nozik joyni ta'kidlaydi. Birinchi: klient ketma-ket ikki so'rov yuborib, ikkinchisi birinchisiga xalaqit berishi mumkin (buyurtma berish, keyin uni bekor qilish), va klient ko'zida bu ikki so'rov aniq bog'liq bo'lsa ham, protokolga qarab server uchun bu bog'liqlik ko'rinmasligi mumkin (65-bet). Ikkinchi: server ham so'rov, ham sessiyani ikki tomondan ko'radi, ya'ni klientga nisbatan server va boshqa tizimlarga nisbatan klient sifatida, shuning uchun bir vaqtda bir nechta sessiya bo'ladi: klientdan kelgan HTTP sessiyasi va bazalar bilan baza sessiyalari (66-bet).

Asosiy qiyinchilik esa kontekstlarning bir-biriga tushmasligida. Nazariy jihatdan har sessiya butun umri davomida bitta jarayon bilan eksklyuziv bog'langan bo'lardi va jarayonlar o'zaro izolyatsiyalangani uchun bu konkurentlik konfliktlarini kamaytirardi, lekin Fowler bunday ishlashga ruxsat beradigan server asbobini bilmasligini aytadi; yaqin variant har so'rov uchun yangi jarayon ochish (erta Perl veb tizimlarining usuli), undan hozir voz kechilgan, chunki jarayon ochish ko'p resurs band qiladi; shunga qaramay bitta jarayon bir vaqtda faqat bitta so'rovni ishlashi keng tarqalgan va bu ko'p konkurentlik bosh og'rig'ini yo'q qiladi (66-bet). PostgreSQL ning [process modeli](21-postgresql-arxitekturasi-process-model-wal.md#211-protsess-modeli-postmaster-backend-protsess-fon-ishchilari) aynan shu oxirgi holat, ilovaning request-per-thread modeli esa emas: shuning uchun ilova tomonida umumiy holat muammosi bor, baza backendi ichida esa yo'q.

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

`AtomicInteger`, `AtomicLong` va `AtomicReference` lock ishlatmaydi, ular CPU ning compare-and-swap buyrug'iga tayanadi: eski qiymatni o'qish, yangi qiymatni hisoblash, atomar almashtirish, muvaffaqiyatsiz bo'lsa qaytadan urinish. Raqobat past bo'lganda bu lock dan arzonroq, chunki kontekst almashtirish va monitor olish yo'q (necha barobar ekani protsessor va yuklamaga bog'liq, o'lchanmagan taxmin bermaymiz). Raqobat yuqori bo'lganda esa teskari effekt: har bir muvaffaqiyatsiz urinish cache line ni boshqa yadrodan tortib oladi, CPU bo'sh aylanadi.

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

Ikki tuzog'i bor va javadoc ikkisini ham aniq ta'riflaydi.

Birinchisi `size()`, `isEmpty()` va `containsValue()`: javadoc ularni "aggregate status" metodlari deb ataydi va aytadi-ki, ular faqat map boshqa thread larda o'zgarmayotgan holatda foydali. Aks holda natija o'tkinchi holatni ko'rsatadi: **monitoring va taxmin uchun yetarli, programma boshqaruvi uchun yo'q**. Shuning uchun biznes qarorini `size()` ga qurmaslik kerak; element soni rostdan kerak bo'lsa, `mappingCount()` ishlatiladi (u `long` qaytaradi va `int` ga sig'maydigan hollarda to'g'ri javob beradi), lekin uning ham aniqlik kafolati o'zgarmaydi.

Shu yerda iterator ning xulqi ham aytib o'tilgan: iterator, spliterator va enumeration jadvalning yaratilish paytidagi yoki undan keyingi biror nuqtadagi holatini ko'rsatadi, `ConcurrentModificationException` tashlamaydi, lekin **bir vaqtda faqat bitta thread** ishlatishi uchun mo'ljallangan.

Ikkinchisi `computeIfAbsent` va uning sharti kodga to'g'ridan-to'g'ri qoida bo'ladi. Metod chaqiruvi atomar bajariladi, funksiya kalit yo'q bo'lsa aynan bir marta chaqiriladi, va **hisoblash davomida boshqa thread larning shu map ga yozish urinishlari bloklanishi mumkin**, shuning uchun javadoc hisoblashni "qisqa va sodda" qilishni talab qiladi: uzoq IO yoki tashqi chaqiruv bu yerga tushmaydi. Alohida qattiq shart ham bor: mapping funksiyasi hisoblash davomida shu map ni **o'zgartirmasligi kerak**, va rekursiv yangilash aniqlansa metod `IllegalStateException` tashlaydi. Funksiya istisno tashlasa, mapping o'rnatilmagan holda qoladi.

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

## 11.12 Thread safety darajasini hujjatlash va ortiqcha sinxronlashdan qochish

Sinf thread safe ekani kodda ko'rinmaydi: `synchronized` kalit so'zi implementatsiya detali, chaqiruvchi esa shartnomani biladigan bo'lishi kerak. Shu sababli har bir ko'p threadda ishlatiladigan sinf uchun daraja hujjatda yoziladi. Amalda ishlatiladigan beshta daraja bor.

| Daraja | Ma'nosi | Namuna |
|---|---|---|
| O'zgarmas (immutable) | holat o'zgarmaydi, sinxronlash kerak emas | `String`, `Instant`, `Money` |
| So'zsiz thread safe | ichida yetarli sinxronlash bor | `ConcurrentHashMap`, `AtomicLong` |
| Shartli thread safe | ba'zi ketma-ketliklar tashqi sinxronlashni talab qiladi | `Collections.synchronizedMap` iteratsiyasi |
| Thread safe emas | chaqiruvchi o'zi sinxronlaydi | `ArrayList`, `HashMap` |
| Thread-hostile | tashqi sinxronlash bilan ham xavfli | global holatni o'zgartiradigan statik metod |

"Shartli thread safe" darajasi eng ko'p xato keltiradi, chunki u qanday qulfdan foydalanish kerakligini ham aytishi kerak. Javadoc da bu bitta gap bo'ladi: "iteratsiya paytida obyektning o'zida sinxronlanadi".

Ikkinchi qoida sinxronlashning ichida nima qilinishiga tegishli: sinxronlangan blok ichida boshqaruvni begona kodga bermaslik. Begona kod - siz nazorat qilmaydigan metod: override qilinishi mumkin bo'lgan metod, listener, lambda yoki argument sifatida kelgan funksiya. U nima qilishini bilmaysiz: qulfni ushlab turib boshqa qulf so'rashi (deadlock) yoki shu obyektni qaytib o'zgartirishi mumkin.

```java
// yomon: qulf ichida listener chaqirilyapti - u nima qilishi noma'lum
public void add(Order order) {
    synchronized (lock) {
        orders.add(order);
        for (OrderListener l : listeners) {
            l.onAdded(order);          // deadlock yoki qayta kirish
        }
    }
}

// yaxshi: qulf faqat holatni o'zgartiradi, chaqiruv tashqarida
public void add(Order order) {
    List<OrderListener> snapshot;
    synchronized (lock) {
        orders.add(order);
        snapshot = List.copyOf(listeners);
    }
    snapshot.forEach(l -> l.onAdded(order));
}
```

Uchinchi qoida: `wait` va `notify` ni yangi kodda yozmaslik. Ular to'g'ri ishlatilishi qiyin (qulf ichida tekshirish sikli, `notifyAll` tanlovi, soxta uyg'onish) va yuqori darajadagi vositalar shu ishni qiladi: `CountDownLatch`, `Semaphore`, `CyclicBarrier`, `BlockingQueue`, `CompletableFuture` va [`ExecutorService`](#118-executorservice-thread-pool-turlari-va-navbat-tanlash). To'rtinchi qoida esa to'g'rilikka tegishli: dastur to'g'riligi thread rejalashtiruvchisining tartibiga tayanmasligi kerak. `Thread.yield()` va prioritet bilan tuzatilgan xato tuzatilmagan hisoblanadi, chunki u boshqa platformada yoki boshqa yuk ostida qaytadi; bunday joyda haqiqiy sabab odatda ishlab turgan thread sonining noto'g'riligi yoki yo'qolgan shart tekshiruvi bo'ladi.

## 11.13 Xavfsiz nashr (safe publication) va obyektning qochib ketishi

Obyektni boshqa threadga ko'rinadigan qilish nashr (publication) deyiladi. Muammo shu: obyektga havola ko'rinishi uning **maydonlari** ham ko'rinishini kafolatlamaydi. Havolani oddiy maydonga yozib qo'yish bilan nashr qilingan obyektni boshqa thread yarim qurilgan holatda ko'rishi mumkin: havola bor, maydonlar esa hali default qiymatda.

```java
// yomon: xavfsiz bo'lmagan nashr - boshqa thread yarim qurilgan obyektni ko'radi
public Config config;                     // oddiy maydon

void init() {
    config = new Config(loadAll());       // havola ko'rinadi, maydonlar kafolatlanmaydi
}
```

To'g'ri nashr yo'llari chekli va ularning hammasi happens-before bog'lanishini yaratadi: statik ishga tushirgichda yozish, `volatile` yoki `AtomicReference` ga yozish, `final` maydonda to'g'ri qurilgan obyektni saqlash, yoki qulf bilan himoyalangan maydonga qulf ostida yozish. Eng arzon va eng ishonchli yo'l esa obyektni [o'zgarmas qilish](../clean-code/16-ozgarmaslik-va-holat-boshqaruvi-kod.md#161-final-maydon-final-sinf-va-haqiqiy-ozgarmaslik): `final` maydonlardan iborat o'zgarmas obyektni har qanday yo'l bilan nashr qilish xavfsiz.

Teskari tomoni qochib ketish (escape): obyekt o'zi tayyor bo'lmagan holda tashqariga chiqib ketadi. Eng ko'p uchraydigan ikki shakli - konstruktorda `this` ni ro'yxatga berish ([`this` ning konstruktordan qochib ketishi](../clean-code/14-obyekt-va-malumot-tuzilmasi-inkapsulyatsiya.md#1410-this-ning-konstruktordan-qochib-ketishi)) va ichki holatni o'zgartirib bo'ladigan ko'rinishda qaytarish (`getItems()` ichki `List` ni qaytaradi). Ikkinchisi ko'p threadda shunchaki xato emas, sinxronlash siyosatini butunlay buzadi: qulf ichida himoyalangan ma'lumot qulfdan tashqarida o'zgartiriladigan bo'lib qoladi.

Shu sababli sinxronlash siyosati har bir o'zgaradigan holat uchun yozib qo'yiladi: qaysi maydon qaysi qulf bilan himoyalangan. JCiP shu uchun `@GuardedBy("lock")` annotatsiyasini taklif qiladi va u hujjat sifatida ishlaydi, statik tahlil esa uni tekshirishi mumkin.

## 11.14 Bekor qilish, interrupt siyosati va thread starvation deadlock

Java da threadni majburan to'xtatish yo'li yo'q: `Thread.stop` ishlatilmaydi, chunki u obyektni buzilgan holatda qoldiradi. Buning o'rniga hamkorlik mexanizmi bor: interrupt - bu **so'rov**, uni qabul qiluvchi kod tekshirishi va hurmat qilishi kerak. Shu sababli har bir uzoq ishlaydigan vazifa uchun bekor qilish siyosati yoziladi: bekor qilish qanday so'raladi, kim so'raydi, vazifa qanday javob beradi va qancha vaqt ichida.

Eng ko'p uchraydigan xato interruptni yo'qotish: `InterruptedException` ushlanadi, log yoziladi va ish davom etadi. Natijada bekor qilish ishlamaydi va shutdown muddatsiz kutadi. Qoida: ya istisnoni yuqoriga uzatish, yoki holatni tiklash.

```java
// yaxshi: o'z thread ida emas, shuning uchun holat tiklanadi va sikl to'xtaydi
while (!Thread.currentThread().isInterrupted()) {
    try {
        Task task = queue.poll(1, TimeUnit.SECONDS);
        if (task != null) {
            task.run();
        }
    } catch (InterruptedException e) {
        Thread.currentThread().interrupt();   // holatni yo'qotmaslik
        break;
    }
}
```

Navbatga asoslangan ishchilarni to'xtatishning ikkinchi usuli - poison pill: navbatga maxsus "tugadi" belgisi qo'yiladi va ishchi uni ko'rgach chiqadi. U faqat ishlab chiqaruvchi va iste'molchi soni ma'lum bo'lganda ishlaydi, cheksiz navbat bilan esa umuman ishlamaydi.

`ExecutorService` to'xtatishning ikki shakli bor va farqi muhim: `shutdown()` yangi vazifa qabul qilmaydi, lekin navbatdagini bajaradi; `shutdownNow()` navbatni bo'shatadi, bajarilayotganlarga interrupt yuboradi va bajarilmagan vazifalar ro'yxatini qaytaradi - shu ro'yxat tashlab yuborilmasligi kerak, aks holda ish jim yo'qoladi.

Oxirgi tuzoq thread starvation deadlock: bitta pool dagi vazifa shu pool ga qo'yilgan boshqa vazifaning natijasini kutadi. Bitta threadli pool da bu darhol muzlaydi, kattaroq pool da esa yuk oshganda muzlaydi, ya'ni test da chiqmaydi. Qoida: bir-biriga tayanadigan vazifalar bir pool da bo'lmaydi; `CompletableFuture` zanjirlarida ham har bosqich uchun pool ni oshkor berish shu sababdan kerak.

## 11.15 Qulf raqobatini kamaytirish: qamrov, bo'lish, striping va issiq maydon

Qulf to'g'rilik vositasi, lekin u bir vaqtda bitta threadni o'tkazadi, ya'ni masshtablanishning chegarasi. Qulf raqobati (contention) o'lchanadi: JFR da `jdk.JavaMonitorEnter` hodisasi va thread dump da bir xil monitorda `BLOCKED` turgan threadlar shuni ko'rsatadi. Tuzatish yo'llari tartib bilan, arzondan qimmatga.

| Yo'l | Nima qilinadi | Qachon |
|---|---|---|
| Qamrovni qisqartirish | qulf ichidan I/O, hisob va log chiqariladi | har doim birinchi |
| Qulfni bo'lish (splitting) | mustaqil holat uchun alohida qulf | bitta qulf bir necha mustaqil maydonni himoyalayotganda |
| Striping | holat N bo'lakka bo'linib, har biriga o'z qulfi | bitta katta to'plam ustida raqobat bo'lsa |
| Qulfni olib tashlash | o'zgarmas obyekt, thread-local, atomic | holat haqiqatda umumiy bo'lmasa |

```java
// yomon: bitta qulf ikki mustaqil holatni himoyalaydi, ikkisi bir-birini kutadi
public synchronized void addOrder(Order o) { orders.add(o); }
public synchronized void addUser(User u) { users.add(u); }

// yaxshi: qulf bo'lindi, ikki oqim bir-birini kutmaydi
private final Object ordersLock = new Object();
private final Object usersLock = new Object();
```

Issiq maydon (hot field) alohida holat: hamma operatsiya bitta hisoblagichni o'zgartiradi, shuning uchun qulfni qanday bo'lsang ham raqobat o'sha maydonda qoladi. Yechim hisoblagichni ham bo'lish: `LongAdder` aynan shu uchun bor, u ichida bir nechta yacheyka saqlaydi va yig'indini faqat o'qishda hisoblaydi. `AtomicLong` o'rniga `LongAdder` ni tanlash mezoni oddiy: yozish ko'p va o'qish kam bo'lsa `LongAdder`, har yozishdan keyin aniq qiymat kerak bo'lsa `AtomicLong`.

Oxirgi ogohlantirish: qulfni almashtirishdan oldin o'lchash kerak. Raqobat yo'q qulf deyarli bepul (JVM uni biased yoki thin lock sifatida bajaradi), shuning uchun "sinxronlash sekin" degan taxmin bilan qilingan refaktoring odatda faqat xato kiritadi. Tartib: o'lchash, qamrovni qisqartirish, qayta o'lchash, keyin tuzilmani o'zgartirish.

## 11.16 Qo'shma amal, intrinsic lock va reentrancy mexanikasi

Konkurentlikdagi xatolarning aksariyati bitta sinfga tushadi: qo'shma amal (compound action). JCiP uni ikki shaklga ajratadi va shu ajratish diagnostikada ishlatiladi. Birinchisi check-then-act: holat tekshiriladi, keyin tekshiruv natijasiga qarab ish qilinadi, lekin tekshiruv bilan ish orasida holat o'zgargan bo'lishi mumkin. Ikkinchisi read-modify-write: yangi qiymat avvalgi qiymatdan hisoblanadi, demak hisoblash davomida hech kim o'sha qiymatni o'zgartirmasligi kerak. Kitob ikkisini birgalikda qo'shma amal deb ataydi va qoidani bitta gapda beradi: thread safety uchun check-then-act va read-modify-write ketma-ketliklari doim atomar bajarilishi shart.

Nega bu ajratish amaliy: ikki shakl ikki xil yechim talab qiladi. Read-modify-write bitta o'zgaruvchiga tegsa, uni `AtomicLong` yoki `LongAdder` ga almashtirish yetarli. Check-then-act esa odatda bir nechta maydonni yoki tashqi tizimni qamraydi, shuning uchun atomic sinf yordam bermaydi: u yerda qulf, `ConcurrentMap.putIfAbsent` kabi tayyor atomar amal, yoki DB darajasidagi shartli `UPDATE` kerak bo'ladi.

```java
@Service
public class CouponService {
    private final Map<String, Coupon> issued = new ConcurrentHashMap<>();

    // yomon: check-then-act, ikki thread bir kuponni ikki marta beradi
    public Coupon issueBroken(String code) {
        if (!issued.containsKey(code)) {        // tekshiruv
            issued.put(code, new Coupon(code)); // amal, oraliqda holat o'zgargan
        }
        return issued.get(code);
    }

    // yaxshi: tekshiruv va amal bitta atomar chaqiruvda
    public Coupon issue(String code) {
        return issued.computeIfAbsent(code, Coupon::new);
    }
}
```

Qulfning o'zi qanday ishlaydi. Har bir Java obyekti sinxronlash uchun qulf bo'lib xizmat qilishi mumkin va bu ichki qulflar intrinsic lock yoki monitor lock deb ataladi. `synchronized` metod butun metod tanasini qamragan blokning qisqartmasi, qulf esa metod chaqirilgan obyekt; statik `synchronized` metod `Class` obyektini qulf sifatida oladi. Qulf avtomatik olinadi va blokdan chiqishda, hatto istisno uchib ketganda ham avtomatik bo'shaydi. Intrinsic lock mutex sifatida ishlaydi: bir vaqtda ko'pi bilan bitta thread uni egallaydi.

Reentrancy shu mexanizmdagi ikkinchi muhim tafsilot: intrinsic lock reentrant, ya'ni thread o'zi ushlab turgan qulfni qayta so'rasa, so'rov muvaffaqiyatli bo'ladi. Kitob buni aniq ifodalaydi: qulf chaqiruv boshiga emas, thread boshiga beriladi. JVM har bir qulf uchun egasi (owning thread) va olish hisoblagichini (acquisition count) saqlaydi: hisoblagich nolga tushganda qulf bo'shaydi. Bu shart emas, zarurat: reentrancy bo'lmaganda `synchronized` metodni override qilib super versiyasini chaqirgan subclass o'zini deadlock ga olib keladi, chunki ikki metod ham bir xil obyekt qulfini so'raydi. Amalda bundan kelib chiqadigan xulosa: reentrancy qulflashni inkapsulyatsiya qilish imkonini beradi, lekin u qulf ichida begona kod chaqirishni xavfsiz qilmaydi (buni [11.10](#1110-deadlock-livelock-va-ochlik-starvation-sabab-va-oldini-olish) va patterns 4.34 ko'rsatadi).

Manba: Brian Goetz va boshqalar, *Java Concurrency in Practice*, Addison-Wesley, 2006, 2.2.3-bo'lim (15-bet), 2.3.1-bo'lim (17-bet) va 2.3.2-bo'lim (18-bet).

## 11.17 Thread ga qamash: ad-hoc, stack va `ThreadLocal` qamashi

Umumiy o'zgaradigan ma'lumotga kirish sinxronlashni talab qiladi, demak eng arzon yechim umuman bo'lishmaslik. Ma'lumotga faqat bitta threaddan kirilsa, sinxronlash kerak emas. JCiP bu usulni thread confinement deb ataydi va uch darajaga ajratadi, mustahkamligi bo'yicha pastdan yuqoriga.

Ad-hoc qamash (ad-hoc thread confinement): qamashni ta'minlash to'liq implementatsiya vijdonida qoladi, tilda hech qanday tayanch yo'q. Kitob uni mo'rt (fragile) deb ataydi va imkon bo'lsa kuchliroq shaklga o'tishni tavsiya qiladi. Shu darajaning bitta foydali xususiy holati bor: `volatile` o'zgaruvchi ustida read-modify-write bajarish xavfsiz, agar unga **faqat bitta thread yozsa**. Bu holda o'zgartirish bitta threadga qamalgani uchun poyga yo'q, `volatile` esa qolgan threadlarga eng yangi qiymatni ko'rsatadi. Hisoblagichni bitta writer thread yuritadigan metrika yig'uvchilarda shu naqsh uchraydi.

Stack qamashi (stack confinement): obyektga faqat lokal o'zgaruvchi orqali yetib borish mumkin. Lokal o'zgaruvchilar tabiatan ishlayotgan threadga qamalgan, chunki ular shu threadning stack ida yashaydi va boshqa thread uchun ochiq emas. Primitiv tipli lokal o'zgaruvchi uchun qamashni buzish umuman mumkin emas: primitivga havola olishning yo'li yo'q, demak tilning semantikasi kafolat beradi. Havola tipli lokal o'zgaruvchi uchun esa bitta shart qoladi: obyektni metoddan chiqarib yubormaslik.

`ThreadLocal` qamashi: eng oshkor shakl, qiymat thread bilan bog'lanadi. Spring da bu naqsh hamma joyda: `SecurityContextHolder`, `TransactionSynchronizationManager`, `RequestContextHolder` va `MDC` shu mexanizmga tayanadi.

```java
// stack qamashi: TreeSet metoddan chiqmaydi, shuning uchun sinxronlash kerak emas
public int pairUp(Collection<Animal> candidates) {
    SortedSet<Animal> sorted = new TreeSet<>(BY_SPECIES);  // lokal, qamalgan
    sorted.addAll(candidates);
    int pairs = 0;
    Animal pending = null;
    for (Animal a : sorted) {
        if (pending == null) { pending = a; } else { pairs++; pending = null; }
    }
    return pairs;                      // sorted tashqariga chiqmaydi
}
```

Kitobning muhim ogohlantirishi: tilda o'zgaruvchi qulf bilan himoyalanganini majburlash mexanizmi bo'lmagani kabi, obyektni threadga qamashni majburlash mexanizmi ham yo'q. Qamash dizayn elementi va uni implementatsiya ta'minlaydi. Server ilovalarida eng ko'p uchraydigan amaliy misol JDBC `Connection`: spetsifikatsiya `Connection` ning thread-safe bo'lishini talab qilmaydi, lekin pool bitta ulanishni so'rov davomida bitta threadga beradi va qaytarilmaguncha boshqasiga bermaydi, ya'ni ulanish so'rov davomida shu threadga bilvosita qamalgan bo'ladi.

Pool da `ThreadLocal` ni tozalamaslik ma'lumotni keyingi so'rovga oqizadi; `ThreadLocal` ning virtual thread davridagi o'rnini [architect 12.8](12-virtual-threads-structured-concurrency-va.md#128-scoped-values-va-threadlocal-orniga-ishlatish) `ScopedValue` bilan solishtiradi, pattern yozuvi esa patterns 4.15 da.

Manba: Brian Goetz va boshqalar, *Java Concurrency in Practice*, Addison-Wesley, 2006, 3.3-bo'lim (28-bet), 3.3.1-bo'lim (28-29-bet) va 3.3.2-bo'lim (29-bet).

## 11.18 Condition queue mexanikasi: shart predikati, yo'qolgan signal va kirish-chiqish protokoli

`wait` va `notify` atrofidagi chalkashlikning asosiy sababi JCiP ga ko'ra bitta: shart predikati (condition predicate) tushunchasi API da moddiy ko'rinishga ega emas. U til spetsifikatsiyasida ham, Javadoc da ham bevosita tilga olinmaydi, lekin usiz shartli kutish ishlamaydi. Shart predikati operatsiyani holatga bog'liq qiladigan dastlabki shart: chegaralangan buffer uchun `take` ning predikati "buffer bo'sh emas", `put` ning predikati "buffer to'la emas".

Mexanikaning yuragida uch tomonli bog'liqlik turadi: qulf, `wait` metodi va shart predikati. Predikat holat o'zgaruvchilaridan tuziladi, holat o'zgaruvchilari qulf bilan himoyalangan, demak predikatni tekshirishdan oldin o'sha qulf ushlab turilishi kerak. Bundan tashqari qulf obyekti va condition queue obyekti (ya'ni `wait` va `notify` chaqirilayotgan obyekt) bir xil obyekt bo'lishi shart. `wait` qulfni bo'shatadi, threadni bloklaydi, uyg'ongandan keyin esa qaytishdan oldin qulfni qayta oladi. Muhim tafsilot: `wait` dan uyg'ongan thread qulfni qayta olishda hech qanday ustunlikka ega emas, u boshqa har qanday thread bilan teng raqobatlashadi.

Shundan ikkinchi qoida chiqadi: `wait` qaytgani kutilgan predikat rost bo'lganini bildirmaydi. Sababi uchta. Bitta intrinsic condition queue bir nechta predikat bilan ishlatilishi mumkin, demak `notifyAll` sizni uyg'otgani sizning predikatingiz uchun emas (kitobning tashbehi: toster va kofe qaynatgich bitta qo'ng'iroqni bo'lishadi, qo'ng'iroq jiringlasa qaysi qurilma signal berganini borib ko'rish kerak). `wait` spurious, ya'ni hech kim `notify` chaqirmagan holda ham qaytishi mumkin. Va nihoyat, siz uyg'onganingiz bilan qulfni qayta olganingiz orasida boshqa thread holatni qaytarib buzgan bo'lishi mumkin. Shuning uchun `wait` doim tsikl ichida chaqiriladi va predikat har iteratsiyada qayta tekshiriladi.

```java
public final class BoundedBuffer<E> {
    private final Object lock = new Object();
    private final Deque<E> items = new ArrayDeque<>();
    private final int capacity;

    public BoundedBuffer(int capacity) { this.capacity = capacity; }

    public void put(E item) throws InterruptedException {
        synchronized (lock) {
            while (items.size() == capacity) {   // kirish protokoli: predikat
                lock.wait();                     // while, if emas
            }
            items.addLast(item);
            lock.notifyAll();                    // chiqish protokoli: xabar berish
        }
    }

    public E take() throws InterruptedException {
        synchronized (lock) {
            while (items.isEmpty()) {
                lock.wait();
            }
            E item = items.pollFirst();
            lock.notifyAll();
            return item;
        }
    }
}
```

Kitob bu intizomni kirish va chiqish protokoli (entry and exit protocol) sifatida rasmiylashtiradi: holatga bog'liq har bir operatsiya va boshqa operatsiya bog'liq bo'lgan holatni o'zgartiradigan har bir operatsiya uchun protokol belgilanadi va hujjatlashtiriladi. Kirish protokoli operatsiyaning shart predikati. Chiqish protokoli esa operatsiya o'zgartirgan holat o'zgaruvchilarini ko'rib chiqib, ular boshqa biror predikatni rost qilib qo'ymadimi degan savolga javob berish va qilib qo'ygan bo'lsa tegishli condition queue da xabar berish. `AbstractQueuedSynchronizer` aynan shu chiqish protokoli g'oyasini ekspluatatsiya qiladi: sinxronizator metodlari o'zlari xabar bermaydi, balki amal kutayotgan threadlarni bo'shatgan bo'lishi mumkinligini ko'rsatuvchi qiymat qaytaradi, shu bilan "xabar berishni esdan chiqarish" qiyinlashadi.

Amalda esa yuqori darajadagi vosita tanlanadi: `BlockingQueue`, `Semaphore`, `CountDownLatch` yoki `Condition`. Pattern nuqtasidan bu Guarded Suspension yozuvi, patterns 4.12 da.

Manba: Brian Goetz va boshqalar, *Java Concurrency in Practice*, Addison-Wesley, 2006, 14.2.1-bo'lim (183-bet), 14.2.2-bo'lim (184-bet) va 14.2.8-bo'lim (187-188-bet).

## 11.19 `AbstractQueuedSynchronizer`: acquire va release protokoli

`java.util.concurrent` dagi holatga bog'liq sinflarning ko'pi bitta asos ustida qurilgan: `AbstractQueuedSynchronizer` (AQS). Kitob ochiq aytadi: ko'p dasturchi AQS ni bevosita hech qachon ishlatmaydi, lekin standart sinxronizatorlar qanday qurilganini ko'rish ularning xulqini tushunishga yordam beradi. Arxitektor uchun bu amaliy foyda beradi, chunki thread dump da `ReentrantLock`, `Semaphore` va `CountDownLatch` ni kutayotgan threadlar bir xil `AbstractQueuedSynchronizer$ConditionObject` yoki `LockSupport.park` kadrida ko'rinadi.

AQS ikki asosiy amal atrofida qurilgan: acquire va release. Acquire holatga bog'liq amal va u doim bloklashi mumkin. Uning ma'nosi sinxronizatorga qarab o'zgaradi: qulf yoki ruxsat olish, `CountDownLatch` uchun "latch terminal holatga yetguncha kut", `FutureTask` uchun "vazifa tugaguncha kut". Release bloklamaydi: u faqat acquire da turgan threadlarga o'tish imkonini berishi mumkin. Acquire ikki qismdan iborat: avval sinxronizator joriy holat o'tishga ruxsat beradimi degan qarorni qabul qiladi, keyin esa sinxronizator holatini yangilashi mumkin.

Holatni AQS o'zi yuritadi: u bitta `int` sinxronlash holatini saqlaydi va unga `getState`, `setState` va `compareAndSetState` protected metodlari orqali tegiladi. Shu bitta butun son turli ma'no oladi va bu AQS ning asosiy nayrangi: `ReentrantLock` unda qulf egasi qulfni necha marta olganini, `Semaphore` qolgan ruxsatlar sonini, `FutureTask` esa vazifa holatini (hali boshlanmagan, ishlayotgan, tugagan, bekor qilingan) saqlaydi. Sinxronizator qo'shimcha holat o'zgaruvchilarini o'zi ham yuritishi mumkin: masalan `ReentrantLock` joriy qulf egasini alohida saqlaydi, shu bilan reentrant va raqobatli so'rovni ajratadi.

Acquire eksklyuziv (`ReentrantLock`) yoki noeksklyuziv (`Semaphore`, `CountDownLatch`) bo'lishi mumkin. AQS kutayotgan threadlarni FIFO navbatga qo'yish kabi tafsilotlarni o'z ustiga oladi, sinxronizator esa faqat o'tish mezonini belgilaydi.

AQS ustida qurishning kitob ko'rsatgan asosiy foydasi implementatsiya hajmini qisqartirish emas, bloklanish nuqtalarini birga tushirish. Agar sinxronizatorni boshqa sinxronizator ustida qursangiz, raqobat nuqtalari qo'shiladi: semaforni qulf ustida yozsangiz, ruxsat olish ikki joyda bloklanishi mumkin, avval semafor holatini himoyalagan qulfda, keyin ruxsat yo'q bo'lsa yana bir marta. AQS bilan qurilgan sinxronizatorda bloklanish nuqtasi bitta, bu kontekst almashinuvi narxini kamaytiradi va throughput ni oshiradi.

JDK da AQS ustida qurilganlar ro'yxati qisqa va foydali: `ReentrantLock`, `Semaphore`, `CountDownLatch`, `FutureTask` va `ReentrantReadWriteLock`. Amaliy xulosa: o'z sinxronizatoringizni yozish kerak bo'lsa, avval shu beshtadan biri yoki ularning kompozitsiyasi yetmasligini isbotlang; yetmasa, AQS ni `wait`/`notify` dan afzal ko'ring, chunki chiqish protokoli uning API sida majburlangan.

Manba: Brian Goetz va boshqalar, *Java Concurrency in Practice*, Addison-Wesley, 2006, 14.4-bo'lim (189-190-bet), 14.5-bo'lim (190-191-bet) va 14.6-bo'lim (192-194-bet).

## 11.20 Qayta tartiblash, piggybacking va initsializatsiya xavfsizligi

Dasturchilar ko'pincha ketma-ket izchillikni (sequential consistency) taxmin qiladi: amallar dasturda yozilgan tartibda bajariladi va har bir o'qish o'sha o'zgaruvchiga oxirgi yozilgan qiymatni ko'radi. JCiP buni ochiq rad etadi: hech bir zamonaviy ko'p protsessorli tizim ketma-ket izchillikni bermaydi va Java Memory Model ham bermaydi. Kechikish yoki tartibsiz bajarilishning barcha sabablari kitobda bitta nom ostida yig'iladi: qayta tartiblash (reordering). Kitobning ko'rsatkich misoli ikki thread ikki maydonni yozib ikkitasini o'qiydi va natija `(0, 0)` bo'lishi mumkin, ya'ni ikki thread ham boshqasining yozuvini ko'rmaydi: amallar orasida ma'lumot bog'liqligi yo'q, shuning uchun ularni tartibsiz bajarish mumkin.

happens-before qoidalarining o'zi va `volatile` bilan `final` maydon kafolatlari [architect 9.9](09-jvm-ichki-tuzilishi-class-loading-memory.md#99-java-memory-model-happens-before-volatile-final-maydon-kafolatlari) da yozilgan, bu yerda esa ulardan kelib chiqadigan ikki amaliy natija ko'rib chiqiladi.

Birinchisi piggybacking: mavjud sinxronlashga "osilib" qo'shimcha ma'lumotni arzonroq uzatish. JDK dagi kanonik misol `FutureTask`. U AQS ning butun son holatida vazifa holatini saqlaydi, lekin natijaning o'zini alohida maydonda yuritadi. Natijani yozgan thread bilan uni o'qigan thread orasida happens-before bo'lishi kerak. Buni natija havolasini `volatile` qilish bilan yechish mumkin edi, lekin `FutureTask` arzonroq yo'ldan boradi: natija `releaseShared` chaqiruvidan **oldin** yoziladi va `acquireShared` chaqiruvidan **keyin** o'qiladi. `tryReleaseShared` volatile o'zgaruvchiga yozadi, `tryAcquireShared` esa uni o'qiydi, demak dastur tartibi qoidasi volatile qoidasi bilan birlashib kerakli happens-before ni beradi. Amaliy xulosa ikki tomonli: tayyor sinxronizator ichidagi bunday nozik bog'lanishlar sizning kodingizda ham ishlaydi (masalan `BlockingQueue` orqali uzatilgan obyekt xavfsiz nashr qilinadi), lekin o'z kodida piggybacking ga tayanish mo'rt, chunki u ichki implementatsiya tafsilotiga bog'lanadi.

Ikkinchisi initsializatsiya xavfsizligi (initialization safety). `final` maydonlar konstruktor tugaganda "muzlatiladi" va `final` maydonlar orqali yetib boriladigan qiymatlar shu muzlatilgan holatdan kam bo'lmagan darajada yangi ko'rinadi; shu maydonlarni initsializatsiya qiladigan yozuvlar konstruktordan keyingi amallar bilan qayta tartiblanmaydi. Natijada juda kuchli kafolat chiqadi: faqat `final` maydonlardan iborat va holatini konstruktordan keyin o'zgartirmaydigan obyekt **xavfsiz bo'lmagan nashr bilan ham** xavfsiz ko'rinadi, hatto ichida thread-safe bo'lmagan `HashMap` saqlasa ham.

```java
// initsializatsiya xavfsizligi: final maydon, konstruktordan keyin o'zgarmaydi
public final class RateTable {
    private final Map<String, BigDecimal> rates;      // final SHART

    public RateTable(Map<String, BigDecimal> source) {
        this.rates = Map.copyOf(source);              // konstruktorda to'liq quriladi
    }

    public BigDecimal rateOf(String code) { return rates.get(code); }
}
```

Kafolatning chegaralari aniq va ularni buzish oson. `final` ni olib tashlash, konstruktordan boshqa metodda tarkibni o'zgartirish, qo'shimcha `final` bo'lmagan maydon qo'shish yoki konstruktor davomida obyektni tashqariga chiqarib yuborish (escape) kafolatni bekor qiladi. `final` bo'lmagan maydonlar orqali yetib boriladigan yoki qurilishdan keyin o'zgaradigan qiymatlar uchun ko'rinuvchanlikni sinxronlash bilan ta'minlash kerak. Shuning uchun [11.13](#1113-xavfsiz-nashr-safe-publication-va-obyektning-qochib-ketishi) dagi xavfsiz nashr yo'llari o'zgaradigan obyektlar uchun hamon majburiy qoladi.

Manba: Brian Goetz va boshqalar, *Java Concurrency in Practice*, Addison-Wesley, 2006, 16.1.1-16.1.2-bo'lim (207-208-bet), 16.1.4-bo'lim (210-211-bet) va 16.3-bo'lim (214-215-bet).

## 11.21 ABA muammosi va atomic field updater

CAS ning semantikasi aniq bitta savol beradi: "V ning qiymati hamon A mi?" va shunday bo'lsa yangilashni davom ettiradi. Ko'pchilik holatda bu yetarli. Lekin ba'zi algoritmlar uchun kerakli savol boshqa: "V ni oxirgi marta A deb ko'rganimdan beri u o'zgardimi?" Agar V ni A dan B ga, keyin yana A ga qaytarish algoritm uchun qayta urinishni talab qiladigan o'zgarish bo'lsa, oddiy CAS buni sezmaydi. JCiP buni ABA muammosi (ABA problem) deb ataydi.

Muhim nuans: kitob bu anomaliyani asosan node larni qayta ishlatadigan, ya'ni xotirani o'zi boshqaradigan algoritmlarga (va garbage collection bo'lmagan muhitlarga) tegishli deb belgilaydi. Bunday holatda ro'yxat boshi avval ko'rilgan node ga hamon ishora qilayotgani ro'yxat tarkibi o'zgarmaganini bildirmaydi. Java da link node larni GC boshqarganda muammo odatda o'zi yo'qoladi. Agar yo'qolmasa, yechim oddiy: havolaning o'zini yangilash o'rniga juftlikni yangilash kerak, havola va versiya belgisi. JDK da bu `AtomicStampedReference` (havola plus `int` stamp) va `AtomicMarkableReference` (havola plus `boolean` belgi).

```java
// ABA ga qarshi: havola plus versiya belgisi bir vaqtda almashtiriladi
private final AtomicStampedReference<Node> top =
        new AtomicStampedReference<>(null, 0);

public boolean replaceTop(Node expected, Node next) {
    int[] stampHolder = new int[1];
    Node current = top.get(stampHolder);              // havola va stamp birga o'qiladi
    if (current != expected) {
        return false;
    }
    return top.compareAndSet(current, next, stampHolder[0], stampHolder[0] + 1);
}
```

Shu bobning ikkinchi mavzusi atomic field updater. `AtomicIntegerFieldUpdater`, `AtomicLongFieldUpdater` va `AtomicReferenceFieldUpdater` mavjud `volatile` maydon ustidagi refleksiyaga asoslangan "ko'rinish" beradi, shu bilan oddiy `volatile` maydonga CAS qo'llash mumkin bo'ladi. Ularda konstruktor yo'q, `newUpdater` fabrika metodiga sinf va maydon nomi beriladi. Updater muayyan nusxaga bog'lanmaydi: bitta updater maqsadli sinfning har qanday nusxasidagi maydonni yangilashi mumkin.

Ikki tafsilot muhim. Birinchisi: updater ning atomarlik kafolati oddiy atomic sinflarga nisbatan **kuchsizroq**, chunki asosdagi maydon bevosita yozilmasligini kafolatlash mumkin emas; `compareAndSet` va arifmetik metodlar atomarlikni faqat shu updater ni ishlatadigan boshqa threadlarga nisbatan kafolatlaydi. Ikkinchisi: kitob uni nega umuman ishlatishini aytadi va sabab faqat unumdorlik. `ConcurrentLinkedQueue` har bir `Node` ni `AtomicReference` bilan ifodalash o'rniga oddiy `volatile` maydon va `AtomicReferenceFieldUpdater` ni ishlatadi, chunki tez-tez ajratiladigan va qisqa umr ko'radigan navbat node lari uchun har bitta node ga `AtomicReference` yaratmaslik qo'yish amalining narxini sezilarli kamaytiradi.

Kitobning xulosasi to'g'ridan-to'g'ri amaliy qoida beradi: deyarli barcha holatlarda oddiy atomic o'zgaruvchilar yetarli ishlaydi va field updater faqat sanoqli holatda kerak bo'ladi (qo'shimcha holat: mavjud sinfning serializatsiya shaklini saqlab atomar yangilash kerak bo'lganda). Zamonaviy kodda bu rolni `VarHandle` egallaydi: u refleksiyasiz, tiplangan va JIT uchun qulayroq, shuning uchun yangi kodda `AtomicReferenceFieldUpdater` emas, `VarHandle` tanlanadi.

Manba: Brian Goetz va boshqalar, *Java Concurrency in Practice*, Addison-Wesley, 2006, 15.4.3-bo'lim (205-206-bet) va 15.4.4-bo'lim (206-bet).

## 11.22 Sinxronlashning o'lchangan narxi: kontekst almashinuvi va memory barrier

Thread qo'shadigan narxni baholashda ikki manba ajratiladi: rejalashtirish (scheduling) va xotira sinxronlashi. Ikkisining tartibini bilish refaktoring qarorini o'zgartiradi, shuning uchun JCiP bergan raqamlar foydali, lekin ular 2006 yilda o'lchangan va shuni oshkor aytish kerak.

Kontekst almashinuvi. Agar ishga tayyor threadlar soni CPU sonidan ko'p bo'lsa, OS bir threadni to'xtatib boshqasini qo'yadi va bu joriy threadning bajarilish kontekstini saqlab, yangisini tiklashni talab qiladi. Kitobning qoidasi: kontekst almashinuvining haqiqiy narxi platformaga qarab o'zgaradi, lekin yaxshi taxmin sifatida u 5000 dan 10000 gacha protsessor taktiga, ya'ni ko'pchilik zamonaviy protsessorda bir necha mikrosekundga teng (143-bet). Lekin asosiy narx takt soni emas: yangi thread kirganda unga kerak bo'lgan ma'lumot lokal protsessor cache ida bo'lmaydi, demak almashinuv cache miss toshqinini keltiradi va thread ishga tushgandan keyin birinchi vaqtda sekinroq ishlaydi. Rejalashtiruvchi har bir threadga minimal vaqt kvantini berishining sababi ham shu: almashinuv narxini uzunroq uzluksiz bajarilish ustiga amortizatsiya qilish.

Shundan amaliy xulosa chiqadi: ko'p bloklanadigan dastur (bloklovchi I/O, raqobatli qulfni kutish, condition o'zgaruvchisini kutish) CPU-bound dasturdan ko'proq kontekst almashinuviga uchraydi, chunki threadlar o'z kvantini to'liq ishlatib bo'lmaydi. O'lchash vositalari ham kitobda aytilgan va hamon haqiqiy: Unix da `vmstat`, Windows da `perfmon` almashinuv sonini va kernel da o'tgan vaqt ulushini ko'rsatadi; kernel ulushi 10 foizdan oshsa, bu og'ir rejalashtirish faolligini bildiradi va sababi odatda I/O yoki qulf raqobati bo'ladi.

Xotira sinxronlashi. `synchronized` va `volatile` beradigan ko'rinuvchanlik kafolati memory barrier deb ataladigan maxsus instruksiyalarni talab qilishi mumkin: ular cache ni tozalaydi yoki yaroqsiz qiladi, apparat yozuv buferlarini bo'shatadi va bajarilish konveyerini to'xtatadi. Kitob bilvosita narxni ham ko'rsatadi va u ko'pincha e'tibordan qoladi: barrier kompilyator optimizatsiyalarini to'sadi, chunki ko'p amal memory barrier bilan qayta tartiblanmaydi.

Eng muhim ajratish esa raqobatli va raqobatsiz sinxronlash orasida. `synchronized` mexanizmi raqobatsiz holat uchun optimallashtirilgan (`volatile` esa doim raqobatsiz) va kitob yozilgan paytda raqobatsiz "fast-path" sinxronlashning narxi ko'pchilik tizimda 20 dan 250 gacha protsessor takti edi (143-bet). Bu nol emas, lekin kitobning xulosasi aniq: kerakli raqobatsiz sinxronlashning umumiy ilova unumdorligiga ta'siri kamdan-kam sezilarli bo'ladi, alternativa esa xavfsizlikni qurbon qilishni talab qiladi.

Shuning uchun "sinxronlash sekin" taxmini bilan qilinadigan refaktoring deyarli doim noto'g'ri qaror va ketma-ketlik [11.15](#1115-qulf-raqobatini-kamaytirish-qamrov-bolish-striping-va-issiq-maydon) da berilgan tartibda qoladi: o'lchash, qamrovni qisqartirish, qayta o'lchash. Buning yana bir ko'rinishi kitobdagi "hech qanday ta'sir bermaydigan sinxronlash" misoli: `synchronized (new Object())` bloki hech narsa himoyalamaydi, chunki qulfni boshqa hech kim ko'rmaydi, va JIT uni butunlay olib tashlashi mumkin (lock elision).

Manba: Brian Goetz va boshqalar, *Java Concurrency in Practice*, Addison-Wesley, 2006, 11.3-bo'lim (142-bet), 11.3.1-bo'lim (142-143-bet) va 11.3.2-bo'lim (143-144-bet).

## 11.23 Amalda qo'llash

- [ ] Hamma singleton bean larni ko'rib chiq va o'zgaruvchi maydon topilgan har bir joyni stateless qil yoki immutable obyektga almashtir; `SimpleDateFormat` va `Random` maydonlarini alohida qidir.
- [ ] `Executors.newFixedThreadPool` va `newCachedThreadPool` chaqiruvlarini loyihada qidirib, ularni chekli `queue-capacity` va ongli rad etish siyosatiga ega `ThreadPoolExecutor` ga ko'chir.
- [ ] Har bir pool ga ma'noli `thread-name-prefix` qo'y va `graceful shutdown` uchun `await-termination-period` ni 30 soniyaga sozla.
- [ ] Thread pool kattaligini Little qonuni bilan hisobla, natijani Hikari `maximum-pool-size` bilan solishtir va nisbat teskari bo'lmasligini tasdiqla.
- [ ] `@Async` va `@Transactional` birga ishlatilgan joylarni topib, entity uzatish o'rniga ID uzatishga o'tkaz; `SecurityContextHolder` ga tayangan asinxron kodni alohida belgila.
- [ ] Bir nechta instansiyada ishlaydigan har qanday `synchronized` blokni aniqla va uni PostgreSQL advisory lock yoki `SELECT ... FOR UPDATE` ga ko'chir, `lock_timeout` ni albatta qo'y.
- [ ] Yuklama testi paytida 2 sekund oraliq bilan uchta thread dump olib, `BLOCKED` threadlar sonini va lock egalarini qaydnomaga yozib qo'y.
- [ ] Pool metrikalarini (active, queue size, rejected, completed) Micrometer orqali chiqarib, navbat uzunligi va rad etish soniga alert qo'y.
- [ ] Ko'p threadda ishlatiladigan har bir sinf uchun thread safety darajasini Javadoc da bir gap bilan yozib qo'ying.
- [ ] `synchronized` bloklari ichidan listener, lambda va override qilinadigan metod chaqiruvlarini chiqarib tashlang.
- [ ] `wait`/`notify` ishlatadigan joylarni toping va ularni yuqori darajadagi konkurentlik vositasiga o'tkazing.
- [ ] O'zgaradigan umumiy holatning har bir maydoni uchun qaysi qulf himoyalaganini yozib qo'ying (`@GuardedBy`).
- [ ] Uzoq ishlaydigan har bir vazifa uchun bekor qilish siyosatini yozing va `InterruptedException` yo'qotilgan joylarni tuzating.
- [ ] Bir-biriga tayanadigan vazifalar bitta pool da bajarilmayotganini tekshiring.
- [ ] JFR yoki thread dump bilan qulf raqobatini o'lchab, eng band monitorni aniqlang va qamrovni qisqartirishdan boshlang.

## Manbalar

- Joshua Bloch, *Effective Java* 3rd, Item 78 - umumiy o'zgaradigan holatga kirishni sinxronlash
- Joshua Bloch, *Effective Java* 3rd, Item 79 - ortiqcha sinxronlashdan qochish, qulf ichida begona kod chaqirmaslik
- Joshua Bloch, *Effective Java* 3rd, Item 80, 81 - thread o'rniga executor va vazifa, `wait`/`notify` o'rniga konkurentlik vositalari
- Joshua Bloch, *Effective Java* 3rd, Item 82 - thread safety darajasini hujjatlash
- Joshua Bloch, *Effective Java* 3rd, Item 84 - thread rejalashtiruvchisiga tayanmaslik
- Brian Goetz, *Java Concurrency in Practice*, 2-bob - thread safety ta'rifi va atomarlik
- Brian Goetz, *Java Concurrency in Practice*, 4-bob - obyektlarni kompozitsiya qilish va sinxronlash siyosatini hujjatlash
- Brian Goetz, *Java Concurrency in Practice*, 3-bob - xavfsiz nashr, obyektning qochib ketishi, `@GuardedBy`
- Brian Goetz, *Java Concurrency in Practice*, 7-bob - bekor qilish va interrupt siyosati, poison pill, `shutdownNow` semantikasi
- Brian Goetz, *Java Concurrency in Practice*, 8-bob - thread starvation deadlock va to'yinish (saturation) siyosati
- Brian Goetz, *Java Concurrency in Practice*, 10-bob - qulf tartibi va deadlock
- Brian Goetz, *Java Concurrency in Practice*, 16-bob - Java xotira modeli va happens-before
- Brian Goetz va boshqalar, *Java Concurrency in Practice*, Addison-Wesley, 2006, 2.2.3, 2.3.1 va 2.3.2-bo'lim (15, 17 va 18-bet) - qo'shma amal (check-then-act plus read-modify-write), intrinsic lock va monitor lock, reentrancy ning thread boshiga berilishi, olish hisoblagichi va egasi
- Brian Goetz va boshqalar, *Java Concurrency in Practice*, Addison-Wesley, 2006, 3.3-bo'lim (28-30-bet) - thread ga qamashning uch darajasi: ad-hoc, stack va `ThreadLocal`; bitta thread yozadigan `volatile` ustida read-modify-write; JDBC `Connection` ning so'rov davomida bilvosita qamalishi
- Brian Goetz va boshqalar, *Java Concurrency in Practice*, Addison-Wesley, 2006, 14.2-bo'lim (183-188-bet) - shart predikati, qulf bilan condition queue obyektining bir xil bo'lishi sharti, erta uyg'onish va spurious wakeup, `wait` ni tsiklda chaqirish, kirish va chiqish protokoli
- Brian Goetz va boshqalar, *Java Concurrency in Practice*, Addison-Wesley, 2006, 14.4-14.6-bo'lim (189-194-bet) - AQS ning acquire va release protokoli, bitta `int` sinxronlash holati, bloklanish nuqtasini birga tushirish, AQS ustida qurilgan JDK sinxronizatorlari
- Brian Goetz va boshqalar, *Java Concurrency in Practice*, Addison-Wesley, 2006, 16.1.1-16.1.2, 16.1.4 va 16.3-bo'lim (207-211 va 214-215-bet) - ketma-ket izchillikning yo'qligi, qayta tartiblash, `FutureTask` dagi piggybacking, `final` maydonlarning muzlatilishi va initsializatsiya xavfsizligining chegaralari
- Brian Goetz va boshqalar, *Java Concurrency in Practice*, Addison-Wesley, 2006, 15.4.3-15.4.4-bo'lim (205-206-bet) - atomic field updater ning refleksiyaga asoslangan ko'rinishi va kuchsizroq kafolati, `ConcurrentLinkedQueue` da uning unumdorlik sababi, ABA muammosi va havola plus belgi juftligi bilan yechimi
- Brian Goetz va boshqalar, *Java Concurrency in Practice*, Addison-Wesley, 2006, 11.3-bo'lim (142-144-bet) - kontekst almashinuvi 5000-10000 takt (143-bet), cache miss toshqini va vaqt kvanti, memory barrier ning to'g'ri va bilvosita narxi, raqobatsiz fast-path sinxronlash 20-250 takt (143-bet); raqamlar 2006 yilgi o'lchov
- Robert C. Martin, *Clean Code*, 13-bob va A ilovasi - konkurentlik kodini ajratish, sinxronlangan bo'limni kichik ushlash, bajarilish modellari
- [OpenJDK 25, `java.util.concurrent` package javadoc](https://raw.githubusercontent.com/openjdk/jdk/jdk-25%2B36/src/java.base/share/classes/java/util/concurrent/package-info.java) - "Memory Consistency Properties": happens-before munosabati va uni yaratadigan konstruksiyalar (`synchronized`, `volatile`, `Thread.start()`, `Thread.join()`)
- [OpenJDK 25, `ConcurrentHashMap.java`](https://raw.githubusercontent.com/openjdk/jdk/jdk-25%2B36/src/java.base/share/classes/java/util/concurrent/ConcurrentHashMap.java) - `size`, `isEmpty`, `containsValue` ning aggregate status ekani (monitoring uchun, programma boshqaruvi uchun emas), `mappingCount()`, iteratorning weakly consistent xulqi, `computeIfAbsent` ning atomarligi, boshqa thread larni bloklashi, map ni o'zgartirish taqiqi va `IllegalStateException`
- Martin Fowler, *Patterns of Enterprise Application Architecture*, Addison-Wesley, 2003, 5-bob (65-66-betlar) - bajarilish kontekstlari uchun standart lug'at yo'qligi va Fowler ning ta'riflari (so'rov, sessiya, jarayon, thread, tranzaksiya); klientning ketma-ket ikki so'rovi orasidagi bog'liqlik serverga ko'rinmasligi; serverning so'rov va sessiyani ikki tomondan ko'rishi va bir vaqtda bir nechta sessiya bo'lishi; sessiyani butun umri uchun bitta jarayonga bog'laydigan asbob yo'qligi va bitta jarayonning bir vaqtda bitta so'rovni ishlashi

---

[&larr; 10. Garbage collection va xotira sozlash](10-garbage-collection-va-xotira-sozlash.md) · [Mundarija](README.md) · [12. Virtual threads, structured concurrency va scoped values &rarr;](12-virtual-threads-structured-concurrency-va.md)
