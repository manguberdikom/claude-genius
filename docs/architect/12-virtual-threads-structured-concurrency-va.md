<!-- doc: architect | chapter: 12 | part: II. Java chuqur bilim -->

[Barcha hujjatlar](../../README.md) / [Arxitektor miyasi](README.md)

# 12. Virtual threads, structured concurrency va scoped values (Modern Concurrency)

<details>
<summary>Bu bobdagi 11 bo'lim</summary>

- [12.1 Virtual thread nima: carrier thread, mount va unmount mexanikasi](#121-virtual-thread-nima-carrier-thread-mount-va-unmount-mexanikasi)
- [12.2 Platform thread bilan taqqoslash: xotira, soni, yaratish narxi](#122-platform-thread-bilan-taqqoslash-xotira-soni-yaratish-narxi)
- [12.3 Qaysi yuk uchun foyda beradi va qaysi uchun bermaydi](#123-qaysi-yuk-uchun-foyda-beradi-va-qaysi-uchun-bermaydi)
- [12.4 Pinning muammosi va undan qochish](#124-pinning-muammosi-va-undan-qochish)
- [12.5 Spring Boot da virtual thread ni yoqish](#125-spring-boot-da-virtual-thread-ni-yoqish)
- [12.6 Connection pool virtual thread bilan: nega pool hali ham chegara](#126-connection-pool-virtual-thread-bilan-nega-pool-hali-ham-chegara)
- [12.7 Structured concurrency: vazifalar daraxti, bekor qilish va xato tarqalishi](#127-structured-concurrency-vazifalar-daraxti-bekor-qilish-va-xato-tarqalishi)
- [12.8 Scoped values va `ThreadLocal` o'rniga ishlatish](#128-scoped-values-va-threadlocal-orniga-ishlatish)
- [12.9 Kuzatuvchanlik: thread dump va metrikalar o'zgarishi](#129-kuzatuvchanlik-thread-dump-va-metrikalar-ozgarishi)
- [12.10 Reactive dasturlashga nisbatan tanlov: qachon qaysi biri](#1210-reactive-dasturlashga-nisbatan-tanlov-qachon-qaysi-biri)
- [12.11 Amalda qo'llash](#1211-amalda-qollash)

</details>



Virtual thread Java dunyosida bir necha o'n yillik "thread qimmat, shuning uchun uni pool qil" qoidasini bekor qildi. Java 21 da bu imkoniyat barqaror (stable) bo'ldi, Java 24 da eng og'riqli cheklovi olib tashlandi, Java 25 da esa uning atrofidagi ikki yordamchi mexanizm yetildi: scoped values final bo'ldi, structured concurrency hali preview holatida qoldi. Arxitektor uchun bu yerdagi savol "yoqamanmi yoki yo'q" emas, balki "qaysi yuk profilida nima o'zgaradi va qaysi chegara endi bo'g'iz bo'lib qoladi" degan savol. Pastdagi bo'limlar aynan shu mexanikani va undan chiqadigan qarorlarni yig'adi.

## 12.1 Virtual thread nima: carrier thread, mount va unmount mexanikasi

Virtual thread bu JVM boshqaradigan `Thread` obyekti, uning ortida doimiy OS thread turmaydi. Uni ishga tushirish uchun JVM carrier thread kerak qiladi: bu oddiy platform thread, default holda `ForkJoinPool` ichidagi ishchi thread. Virtual thread carrier ustiga **mount** qilinadi, ya'ni uning stack frame'lari carrier thread'ning haqiqiy stack'iga ko'chiriladi va kod shu yerda bajariladi.

Qiziqarli joyi bloklanish paytida boshlanadi. Agar virtual thread blocking I/O ga kirsa (socket read, `Thread.sleep`, `BlockingQueue.take`), JDK ichidagi qayta yozilgan kutubxona kodi OS darajasida bloklanmaydi. U continuation'ni **unmount** qiladi: stack frame'lar carrier stack'dan heap'ga ko'chiriladi (freeze), carrier bo'shaydi va darhol boshqa virtual thread'ni oladi. I/O tayyor bo'lganda scheduler continuation'ni yana biror carrier ustiga qaytaradi (thaw) va kod xuddi hech narsa bo'lmagandek davom etadi.

```java
// Carrier thread nomini ko'rsatish: unmount dan keyin carrier o'zgarishi mumkin
Thread.ofVirtual().start(() -> {
    // Thread.currentThread() har doim virtual thread'ni qaytaradi, carrier'ni emas
    System.out.println(Thread.currentThread()); // VirtualThread[#21]/runnable@ForkJoinPool-1-worker-3
    try {
        Thread.sleep(Duration.ofMillis(50)); // bu yerda unmount sodir bo'ladi
    } catch (InterruptedException e) {
        Thread.currentThread().interrupt();
        return;
    }
    // Qaytganda carrier worker-3 emas, worker-7 bo'lishi mumkin
    System.out.println(Thread.currentThread());
}).join();
```

Scheduler parallelizmi default holda `Runtime.availableProcessors()` ga teng. Ya'ni 8 yadroli mashinada bir vaqtda ko'pi bilan 8 ta virtual thread haqiqatan CPU da ishlaydi, qolgan yuz minglari heap'da continuation ko'rinishida kutib turadi. Buni `jdk.virtualThreadScheduler.parallelism` va `jdk.virtualThreadScheduler.maxPoolSize` system property'lari bilan o'zgartirish mumkin, lekin bu deyarli hech qachon to'g'ri qaror emas: agar parallelizm kamlik qilsa, muammo CPU yukida yoki pinning'da.

## 12.2 Platform thread bilan taqqoslash: xotira, soni, yaratish narxi

Platform thread bir OS thread'ga 1:1 bog'langan. Linux x64 da uning stack'i uchun default `-Xss` 1 MB virtual manzil fazosi band qilinadi, haqiqiy RSS odatda 50-200 KB atrofida bo'ladi, ustiga yadro strukturalari uchun taxminan 8-16 KB qo'shiladi. Shuning uchun amalda 4-8 GB li konteynerda 5000-10000 platform thread chegara, undan yuqorisi scheduler va GC root skanerlashga bosim beradi.

| Xususiyat | Platform thread | Virtual thread |
|---|---|---|
| Stack joylashuvi | OS stack, 1 MB reserve | Heap'dagi stack chunk, boshida taxminan 200-800 bayt |
| Yaratish narxi | taxminan 50-200 mikrosekund | taxminan 1 mikrosekund |
| Amaliy soni | 5-10 ming | 1-5 million |
| Kontekst almashish | OS scheduler, taxminan 1-10 mikrosekund | JVM continuation, taxminan 100-300 nanosekund |
| Scheduling | OS yadrosi, preemptive | JVM, kooperativ (I/O va monitor nuqtalarida) |
| Pool qilish | Majburiy (qimmat resurs) | Zararli anti-pattern |
| `ThreadLocal` | Cheklangan soni, keshlash arzon | Million nusxa, keshlash xotirani yeydi |
| Nom va prioritet | Mavjud va ta'sir qiladi | Nom bo'sh, prioritet e'tiborga olinmaydi |

Eng muhim xulosa: virtual thread arzon bo'lgani uchun uni resurs sifatida ko'rishdan voz kechamiz. `Executors.newVirtualThreadPerTaskExecutor()` har bir vazifaga yangi thread beradi va bu to'g'ri ishlatish usuli. Virtual thread'ni fixed pool'ga solish barcha foydani yo'q qiladi, chunki parallellik yana pool kattaligi bilan cheklanadi.

```java
// 100 000 ta to'lov tekshiruvini bir vaqtda yuborish
try (var executor = Executors.newVirtualThreadPerTaskExecutor()) {
    List<Future<Natija>> natijalar = tolovlar.stream()
        .map(t -> executor.submit(() -> antifraudKlient.tekshir(t))) // har biri alohida virtual thread
        .toList();
    // close() barcha vazifa tugashini kutadi, try-with-resources shuni kafolatlaydi
    for (var f : natijalar) {
        qayta_ishla(f.get());
    }
}
```

## 12.3 Qaysi yuk uchun foyda beradi va qaysi uchun bermaydi

Virtual thread faqat bitta narsani arzonlashtiradi: kutishni. Agar servis vaqtining katta qismini tashqi chaqiruv javobini kutishga sarflasa, foyda katta. Buyurtma yaratish oqimini olaylik: narx servisiga 40 ms, ombor qoldig'iga 30 ms, antifraud'ga 60 ms, keyin bazaga 10 ms. Jami 140 ms, undan 130 ms sof kutish. 200 thread'li Tomcat pool bilan nazariy throughput taxminan 200 / 0.14 = 1400 so'rov/sekund. Virtual thread bilan chegara endi thread sonida emas, pastdagi haqiqiy resursda: baza connection, tashqi servisning rate limit'i, CPU.

CPU bilan band yuk uchun hech qanday foyda yo'q. Hisobot generatsiyasi, JSON ni katta hajmda serializatsiya qilish, shifrlash, in-memory saralash: bularning hammasi carrier thread'ni egallab turadi va unmount sodir bo'lmaydi. 8 yadroda 8 ta carrier bor, 10000 virtual thread CPU ishini bajarsa, ularning hammasi navbatda turadi va latency portlaydi. Bunday yuk uchun yadro soniga teng o'lchamli alohida platform thread pool to'g'ri yechim bo'lib qoladi.

Yana bir nozik holat: virtual thread scheduler preemptive emas. Uzun CPU tsikli ichida (masalan `while` ichida matematik hisob) unmount nuqtasi yo'q, shuning uchun bitta "yovuz" vazifa carrier'ni daqiqalab ushlab turishi mumkin. Bu holat `Thread.yield()` bilan yumshatiladi, lekin to'g'ri javob bunday yukni virtual thread'ga bermaslik.

## 12.4 Pinning muammosi va undan qochish

Pinning bu virtual thread'ning unmount qilolmay carrier'ni egallab qolishi. Blokirovka davomida carrier band bo'ladi va boshqa hech qanday virtual thread uni ishlatolmaydi. Agar carrier soni 8 bo'lsa va 8 ta virtual thread pinned holda bloklansa, butun ilova to'xtaydi.

Java 21-23 da pinning'ning asosiy manbasi `synchronized` blok edi: object monitor ichida bloklanish unmount'ni taqiqlaydi. Java 24 da bu tuzatildi, endi `synchronized` ichida bloklangan virtual thread ham normal unmount qiladi. Java 25 (LTS) shu xatti-harakatni meros qilib oladi. Shuning uchun bugungi pinning sabablari qisqargan: native frame (JNI chaqiruvi yoki `Object.wait` dan tashqari native blokirovka) va class initializer ichidagi kutish.

| Tuzoq | Nega sodir bo'ladi | Yechim |
|---|---|---|
| `synchronized` ichida I/O (Java 21-23) | Monitor unmount'ni taqiqlaydi | `ReentrantLock` ga o'tish yoki Java 24+ ga ko'tarilish |
| Eski JDBC yoki native driver | JNI frame'da bloklanish pinning beradi | Toza Java driver (PostgreSQL JDBC) ishlatish |
| Virtual thread'ni fixed pool'da ishlatish | Parallellik pool bilan cheklanadi | `newVirtualThreadPerTaskExecutor` |
| `ThreadLocal` keshi million thread'da | Har virtual thread o'z nusxasini oladi | `ScopedValue` yoki parametr orqali uzatish |
| Cheksiz virtual thread yaratish | Baza yoki tashqi API ni bosib tashlaydi | `Semaphore` bilan concurrency cheklash |
| CPU yukini virtual thread'ga berish | Carrier egallanib qoladi, latency o'sadi | Alohida platform thread pool |
| `ThreadPoolExecutor` metrikalariga tayanish | Pool yo'q, metrika bo'sh ko'rinadi | In-flight counter va semaphore metrikasi |
| Katta stack chuqurligi million thread'da | Heap'dagi stack chunk o'sadi | Rekursiyani cheklash, chuqurlikni nazorat qilish |

```java
// synchronized o'rniga ReentrantLock: ikkisi ham mutual exclusion beradi,
// lekin lock virtual thread'ga unmount qilish imkonini qoldiradi
public class OmborQoldigi {
    private final ReentrantLock lock = new ReentrantLock();
    private int qoldiq;

    public void kamaytir(int miqdor) {
        lock.lock();
        try {
            // Bu yerda tashqi chaqiruv bo'lsa ham carrier bloklanmaydi
            auditKlient.yoz(miqdor);
            qoldiq -= miqdor;
        } finally {
            lock.unlock();
        }
    }
}
```

Java 21-23 da pinning'ni topish uchun `-Djdk.tracePinnedThreads=full` flag'i ishlatilardi. Bu flag Java 24 da olib tashlandi, uning o'rniga `jdk.VirtualThreadPinned` JFR event'i qoldi. Arxitektor uchun amaliy qoida: pinning diagnostikasini JFR ga bog'lash, flag'ga emas, chunki flag JDK versiyasiga qarab yo'qoladi.

## 12.5 Spring Boot da virtual thread ni yoqish

Spring Boot 3.2 dan boshlab bitta property butun ilovani virtual thread'ga o'tkazadi. Shart: Java 21 yoki undan yuqori.

```properties
# Java 21+ talab qiladi, Spring Boot 3.2 dan mavjud
spring.threads.virtual.enabled=true

# Virtual thread bilan Tomcat thread pool chegarasi ma'nosini yo'qotadi,
# lekin so'rovlar sonini baribir cheklash kerak
server.tomcat.max-connections=10000
server.tomcat.accept-count=200

# Baza pool'i endi asosiy chegara, uni ongli qo'yish kerak
spring.datasource.hikari.maximum-pool-size=20
spring.datasource.hikari.connection-timeout=2000
```

Bu flag bir nechta joyni bir vaqtda o'zgartiradi: Tomcat (yoki Jetty) har so'rovni virtual thread'da bajaradi, `@Async` uchun ishlatiladigan `AsyncTaskExecutor` virtual thread'ga asoslangan bo'ladi, `@Scheduled` vazifalari uchun scheduler ham virtual thread ishlatadi. Spring MVC blocking modelda qolib, lekin thread chegarasidan xoli bo'ladi.

Nimalar o'zgarmaydi: `@Transactional` bemalol ishlaydi, chunki Spring tranzaksiya kontekstini `ThreadLocal` da saqlaydi va har virtual thread o'zining `ThreadLocal` nusxasiga ega. Security context ham xuddi shunday. Muammo faqat shunda chiqadi, agar kodda "thread kam bo'ladi" deb qurilgan `ThreadLocal` keshlar bo'lsa: masalan har thread uchun `SimpleDateFormat` yoki og'ir `ObjectMapper` nusxasi. 100 ta thread'da bu 100 nusxa, 200000 virtual thread'da bu xotira portlashi.

## 12.6 Connection pool virtual thread bilan: nega pool hali ham chegara

Virtual thread baza bilan ishlashni o'zgartirmaydi. PostgreSQL har ulanish uchun alohida backend jarayon ochadi va u taxminan 5-15 MB xotira oladi. `max_connections` default 100, odatda 200-300 gacha ko'tariladi, undan yuqorisi context switch va lock contention tufayli unumdorlikni pasaytiradi. Ya'ni ilova 100000 virtual thread ko'tarsa ham, baza 20 ta ulanishdan oshig'ini qabul qilmaydi.

Natijada arxitektura shakli o'zgaradi: oldin thread pool ham navbat, ham chegara vazifasini bajarardi. Endi navbat yo'qoladi va 50000 thread bir vaqtda Hikari dan ulanish so'raydi. Hikari `connection-timeout` ichida ulanish bermasa, `SQLTransientConnectionException` otadi va bu xatolar to'lqini ko'rinishida chiqadi. Shuning uchun cheklashni ongli ravishda oldinga, kirish darajasiga ko'chirish kerak.

```java
// Baza bilan ishlovchi qismga kirish nuqtasini cheklash
@Component
public class HisobotServisi {
    // Hikari pool 20 bo'lsa, semaphore 20 dan oshmasligi kerak
    private final Semaphore bazaKvotasi = new Semaphore(20);

    public Hisobot tayyorla(UUID buyurtmaId) throws InterruptedException {
        // 500 ms kutib ulanish olinmasa, tez fail qilamiz
        if (!bazaKvotasi.tryAcquire(500, TimeUnit.MILLISECONDS)) {
            throw new YukOshdiException("baza kvotasi band");
        }
        try {
            return jdbcClient.sql("SELECT ...").param(buyurtmaId).query(Hisobot.class).single();
        } finally {
            bazaKvotasi.release();
        }
    }
}
```

Pool o'lchamini tanlash qoidasi ham o'zgarmadi: CPU yadro soniga bog'lab, taxminan `yadro * 2` dan boshlab, keyin kuzatuv bilan sozlash. 8 yadroli bazada 16-30 ulanish ko'p holatda eng yaxshi throughput beradi. Agar mikroservislar soni ko'p bo'lsa, umumiy ulanish byudjetini hisoblash kerak: 10 instans * 20 pool = 200 ulanish, bu `max_connections` ga yaqin. Bunday holatda PgBouncer transaction pooling rejimida kiritiladi.

## 12.7 Structured concurrency: vazifalar daraxti, bekor qilish va xato tarqalishi

Oddiy `ExecutorService` bilan parallel chaqiruvlarda uch muammo doim takrorlanadi: biri xato berganda qolganlar behuda ishlashda davom etadi, timeout'ni har biri uchun alohida boshqarish kerak, va stack trace'da ota vazifa ko'rinmaydi. Structured concurrency shu uchtasini tilga olib kiradi: parallel vazifalar ota vazifaning leksik blokida tug'iladi va o'sha blokdan tashqariga chiqmaydi.

Java 25 da bu API beshinchi preview holatida, ya'ni `--enable-preview` kerak va imzolar hali o'zgarishi mumkin. Java 21-23 dagi shakl (`new StructuredTaskScope<>()`, `ShutdownOnFailure`, `throwIfFailed`) Java 25 da `StructuredTaskScope.open(...)` va `Joiner` ko'rinishiga almashtirildi. Arxitektor uchun xulosa: mexanikani o'zlashtirish arziydi, lekin production kodni preview API ga bog'lashdan oldin migratsiya narxini hisoblash kerak.

```java
// Java 25, preview: buyurtma sahifasi uchun uch chaqiruvni parallel bajarish
Buyurtma sahifa(UUID id) throws Exception {
    try (var scope = StructuredTaskScope.open(
            StructuredTaskScope.Joiner.<Object>awaitAllSuccessfulOrThrow(),
            cfg -> cfg.withTimeout(Duration.ofMillis(800)))) {

        var narx = scope.fork(() -> narxServisi.hisobla(id));
        var qoldiq = scope.fork(() -> omborServisi.qoldiq(id));
        var mijoz = scope.fork(() -> mijozServisi.profil(id));

        // join() biri xato bersa qolganlarini bekor qiladi va xatoni otadi
        scope.join();
        return new Buyurtma(narx.get(), qoldiq.get(), mijoz.get());
    }
}
```

Bekor qilish `Thread.interrupt` orqali ishlaydi, shuning uchun vazifa ichidagi kod interrupt'ni to'g'ri qayta uzatishi shart. Agar kod `InterruptedException` ni yutib yuborsa, bekor qilish ishlamaydi va timeout kafolati yo'qoladi. Bu eng ko'p uchraydigan integratsiya xatosi.

## 12.8 Scoped values va `ThreadLocal` o'rniga ishlatish

`ThreadLocal` ikki muammo keltiradi. Birinchisi: uning qiymati thread yashash davomida qoladi, shuning uchun uni tozalashni eslab qolish kerak va pool'da `remove()` qilinmasa ma'lumot oqib ketadi. Ikkinchisi: inheritable variant yaratilganda qiymat har bir child thread'ga nusxalanadi va million virtual thread'da bu xotirada sezilarli bo'ladi.

`ScopedValue` Java 25 da final bo'ldi. U immutable va uning amal qilish doirasi leksik blok bilan belgilanadi: blok tugashi bilan bog'lanish o'z-o'zidan yo'qoladi, tozalash kerak emas. Child virtual thread'lar qiymatni nusxalamaydi, ota'ning bog'lanishiga murojaat qiladi.

```java
// Request kontekstini ThreadLocal o'rniga ScopedValue da uzatish
public final class Kontekst {
    public static final ScopedValue<SorovId> SOROV = ScopedValue.newInstance();
}

// Filter yoki interceptor ichida
ScopedValue.where(Kontekst.SOROV, new SorovId(traceId)).run(() -> {
    // Bu blok ichidagi butun chaqiruv zanjiri qiymatni ko'radi
    tolovServisi.bajar(buyurtma);
});

// Chuqurlikdagi kod
String traceId = Kontekst.SOROV.isBound()
    ? Kontekst.SOROV.get().qiymat()
    : "yoq"; // bog'lanmagan holatni doim hisobga olish kerak
```

Amalda Spring ilovasida darhol hamma `ThreadLocal` ni almashtirishga urinmaslik kerak. Spring'ning o'z infratuzilmasi (tranzaksiya, security, MDC) `ThreadLocal` ga tayanadi va u virtual thread bilan to'g'ri ishlaydi. `ScopedValue` ni o'z kodingizdagi kontekst uzatish uchun va structured concurrency bilan birga ishlatish eng ko'p foyda beradi.

## 12.9 Kuzatuvchanlik: thread dump va metrikalar o'zgarishi

Klassik `jstack` virtual thread'larni ko'rsatmaydi, chunki u faqat OS thread'larni biladi. Siz carrier thread'lar ro'yxatini ko'rasiz va ularning stack'i ichida nima bo'layotgani tushunarsiz bo'ladi. To'g'ri vosita yangi formatdagi thread dump.

```bash
# Virtual thread'larni ham qamrab oladigan dump (JSON yoki matn)
jcmd <pid> Thread.dump_to_file -format=json /tmp/dump.json

# Pinning va virtual thread hodisalarini JFR bilan yozib olish
jcmd <pid> JFR.start name=vt settings=profile duration=120s filename=/tmp/vt.jfr
# Keyin quyidagi event'larni ko'rish:
#   jdk.VirtualThreadPinned, jdk.VirtualThreadStart,
#   jdk.VirtualThreadEnd, jdk.VirtualThreadSubmitFailed
jfr summary /tmp/vt.jfr
```

Metrikalar tomonida eng katta o'zgarish: `executor.pool.size`, `executor.queued`, `tomcat.threads.busy` kabi ko'rsatkichlar ma'nosini yo'qotadi. Oldin "pool to'ldi" signali yuk oshganini bildirardi, endi bunday signal yo'q va ilova jim turib latency'ni o'stiradi. Shuning uchun kuzatuvni boshqa joylarga ko'chirish kerak: in-flight so'rov soni (`Gauge` sifatida), semaphore'dagi kutish vaqti, Hikari `hikaricp.connections.pending` va `hikaricp.connections.acquire` taqsimoti. Bu uchtasi birgalikda haqiqiy bo'g'izni ko'rsatadi.

Tracing bilan ishlashda bitta nozik joy bor: Micrometer `Observation` konteksti `ThreadLocal` orqali tarqaladi va `executor.submit` chegarasida avtomatik ko'chmaydi. Context propagation kutubxonasi orqali executor'ni o'rash kerak, aks holda trace virtual thread chegarasida uzilib qoladi.

## 12.10 Reactive dasturlashga nisbatan tanlov: qachon qaysi biri

Reactive (WebFlux, Reactor, R2DBC) ikki narsani beradi: thread tejash va backpressure. Virtual thread birinchisini beradi, ikkinchisini bermaydi. Shuning uchun tanlov "qaysi biri tezroq" emas, "sizga backpressure kerakmi" degan savolga keladi.

| Holat | Oddiy yondashuv | Arxitektor yondashuvi |
|---|---|---|
| I/O ko'p REST servis | Tomcat `max-threads` ni 400 ga ko'tarish | Virtual thread yoqib, chegarani baza pool'iga ko'chirish |
| Mavjud WebFlux kodi | Virtual thread uchun hammasini blocking ga qaytarish | WebFlux ni qoldirish, yangi modullarni blocking yozish |
| Oqim (stream) ishlovi | Hamma elementga bitta virtual thread | Reactive yoki `Flow` bilan backpressure saqlash |
| CPU og'ir hisobot | Virtual thread executor'ga tashlash | Yadro soniga teng platform pool, alohida ajratish |
| Tashqi API rate limit | Retry va kutish bilan urinish | `Semaphore` bilan concurrency cheklash, fail fast |
| Parallel chaqiruvlar | `CompletableFuture.allOf` va qo'lda bekor qilish | Structured concurrency, timeout va bekor qilish tilda |
| Kontekst uzatish | `InheritableThreadLocal` | `ScopedValue`, leksik doira bilan |
| Yuk oshganini bilish | `tomcat.threads.busy` ni kuzatish | In-flight gauge va pool kutish vaqti |
| Pinning diagnostikasi | Log'larga tayanish | JFR `jdk.VirtualThreadPinned` event'i |
| Migratsiya rejasi | Bitta deploy'da hammasini o'tkazish | Bitta servisda yoqib, latency taqsimotini solishtirish |

Amaliy qoida: agar ilova HTTP so'rov qabul qilib, bir nechta servis va bazaga murojaat qilib, javob qaytarsa, virtual thread yetarli va kod ancha sodda bo'ladi. Agar ilova uzluksiz oqimni (event stream, SSE, WebSocket, Kafka'dan katta hajm) qayta ishlasa va ishlab chiqaruvchi iste'molchidan tez bo'lsa, backpressure kerak va reactive model o'z o'rnini saqlaydi. Ikkisini bitta ilovada aralashtirish mumkin, lekin chegarani aniq qo'yish kerak: blocking qism va reactive qism bir-birining thread'ida ishlamasin.

Migratsiyada arxitektor tekshiradigan narsa: yoqishdan oldin va keyin latency'ning p99 qiymati, Hikari pending ulanishlar soni, va yuk testida xatolar turi. Agar p50 yaxshilanib p99 yomonlashsa, bu deyarli har doim pastdagi resursning (baza yoki tashqi servis) bo'g'izga aylanganini bildiradi, virtual thread aybdor emas. Testlash qo'llanmasidagi performance test bo'limi shu solishtirishni qanday o'tkazishni ko'rsatadi.

## 12.11 Amalda qo'llash

- [ ] JDK versiyasini aniqlang: Java 21 da virtual thread barqaror, lekin `synchronized` pinning'dan qochish uchun Java 24 yoki 25 ga ko'tarilishni rejaga qo'ying.
- [ ] Bitta I/O ga bog'liq servisda `spring.threads.virtual.enabled=true` ni yoqib, p50 va p99 latency'ni yoqishdan oldingi qiymat bilan solishtiring.
- [ ] Kod bazasini `synchronized` bloklari ichida tashqi chaqiruv yoki I/O bor joylarga tekshirib, ularni `ReentrantLock` ga o'tkazing.
- [ ] Har bir `ThreadLocal` ishlatilishini ko'rib chiqing: og'ir obyekt keshi bo'lsa, uni umumiy thread-safe nusxaga yoki `ScopedValue` ga almashtiring.
- [ ] Bazaga kiradigan oqimlarga `Semaphore` qo'yib, uning o'lchamini Hikari `maximum-pool-size` dan oshmaydigan qilib belgilang.
- [ ] Dashboard'dagi `tomcat.threads.busy` panelini in-flight so'rov gauge'i va `hikaricp.connections.pending` bilan almashtiring.
- [ ] JFR profilini yuk testi davomida yozib, `jdk.VirtualThreadPinned` event'lari borligini tekshiring va sababini toping.
- [ ] CPU bilan band vazifalarni (hisobot, shifrlash, katta serializatsiya) yadro soniga teng alohida platform thread pool'ga ajratib chiqaring.

---

[&larr; 11. Concurrency: thread, lock, atomic, happens-before](11-concurrency-thread-lock-atomic-happens.md) · [Mundarija](README.md) · [13. Zamonaviy Java tili va API dizayni &rarr;](13-zamonaviy-java-tili-va-api-dizayni.md)
