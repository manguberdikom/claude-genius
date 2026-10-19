<!-- doc: architect | chapter: 11 | part: II. Java chuqur bilim -->

[Barcha hujjatlar](../../README.md) / [Arxitektor miyasi](README.md)

> Holat: tekshirilgan (2026-10-19). Manbalar bob oxirida.

# 11. Concurrency: thread, lock, atomic, happens-before (Java Concurrency)

<details>
<summary>Bu bobdagi 26 bo'lim</summary>

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
- [11.23 Vazifani `Future` orqali bekor qilish: vaqt chegarasi, `shutdownNow` chegarasi va `newTaskFor`](#1123-vazifani-future-orqali-bekor-qilish-vaqt-chegarasi-shutdownnow-chegarasi-va-newtaskfor)
- [11.24 Deadlockdan tiklanish: `tryLock(timeout)`, qulfni qo'yib yuborish va qayta urinish](#1124-deadlockdan-tiklanish-trylocktimeout-qulfni-qoyib-yuborish-va-qayta-urinish)
- [11.25 Yashirin iteratsiya: `toString`, `hashCode` va `containsAll` ham kolleksiyani aylanadi](#1125-yashirin-iteratsiya-tostring-hashcode-va-containsall-ham-kolleksiyani-aylanadi)
- [11.26 Amalda qo'llash](#1126-amalda-qollash)

</details>



Konkurentlik kodni tezlashtirmaydi, u kodni qimmatlashtiradi. To'lov servisi sekundiga 2000 so'rovni ko'tarishi uchun ko'p oqimli bo'lishi shart, lekin har bir umumiy o'zgaruvchi, har bir singleton bean maydoni va har bir lock shu narxga qo'shimcha qator qo'shadi. Arxitektor uchun asosiy savol "qanday parallellashtiraman" emas, "qaysi holat umumiy va uni kim qanday tartibda ko'radi" degan savol. Bu bobda JVM ichida nima sodir bo'lishini, Java Memory Model qanday kafolat berishini va Spring konteynerida bu kafolatlar qanday buzilishini ko'rib chiqamiz.

## 11.1 Parallellik va konkurentlik farqi, qaysi muammoni hal qilamiz

Konkurentlik bir nechta ishni bir vaqtda boshqarish haqida, parallellik esa ularni bir vaqtda bajarish haqida. Buyurtma servisi 200 ta so'rovni navbatga olib, bittadan ishlasa, bu konkurent lekin parallel emas. Shu farq muhim, chunki ikki holatda butunlay boshqa muammo hal qilinadi: konkurentlik resursni kutish vaqtini to'ldiradi, parallellik CPU vaqtini qisqartiradi.

Konkurentlikka "kirish" degan qaror esa ko'pincha umuman yo'q: u allaqachon ichkarida. Kitobning kuzatuvi qisqa: har bir Java ilovasi thread ishlatadi. JVM ishga tushganda GC va finalization kabi uy ishlari uchun thread yaratadi, `main` metodi ham o'z threadida ishlaydi, `Timer`, servlet konteyneri, RMI va AWT yoki Swing esa so'ramasdan o'z threadlarini ochadi (Goetz, 1.1, 8-bet). Ya'ni bitta `new Thread` yozmagan kod ham bir nechta threadda chaqiriladi. Spring da shu ro'yxat uzun: har HTTP so'rovi uchun ajratilgan thread, `@Async` va `@Scheduled` ijrochilari, `@KafkaListener` konteyneri, `WebClient` ning event loopi. Bloch xuddi shu narsani talab shaklida yozadi: ishlatayotgan framework va kutubxonani chuqur bilish kerak, chunki ular siz hisobga olmagan threadlarni kiritishi mumkin (Bloch, Item 78, 315-bet). Amaliy xulosa: "bu kod ko'p threadda ishlaydimi" savoliga javob kod ichida emas, uni kim chaqirayotganida yotadi.

Konkurent ilovani tashkil qilish esa vazifa chegarasini tanlashdan boshlanadi, chunki keyingi hamma qaror shu chegaraga tayanadi. JCiP ning mezoni ikkita: vazifalar ideal holda mustaqil bo'ladi, ya'ni boshqa vazifaning holatiga, natijasiga yoki yon ta'siriga bog'liq bo'lmaydi, va har bir vazifa ilovaning ishlov sig'imining kichik ulushini egallaydi. Birinchisi parallellashtirishga yo'l beradi, ikkinchisi rejalashtirish va yuk balansini moslashtirishga joy qoldiradi. Server ilovasida bu chegara odatda o'zidan tayyor keladi: bitta klient so'rovi. Pochta serveriga yuborilgan xabarning natijasi bir vaqtda ishlanayotgan boshqa xabarlarga bog'liq emas va bitta xabarni ishlash umumiy sig'imning juda kichik foizini oladi (Goetz, 6.1, 72-bet). Ikki mezon buzilgan joyda muammo keyinroq, yuk ostida chiqadi: bir-biriga tayanadigan vazifalar ijro siyosatiga yashirin shart qo'yadi, juda yirik vazifa esa pool ni bitta ish bilan band qilib qo'yadi. Vazifa chegarasi va ijro siyosati birgalikda ilova yuk oshganda chiroyli degradatsiya qiladimi yoki butunlay yiqiladimi degan savolga javob beradi.

Amalda arxitektor ikki qonunga tayanadi. Birinchisi Little qonuni: kerakli bir vaqtdagi ish soni throughput ni latency ga ko'paytirganga teng. Hisobot servisi 500 RPS ni 200 ms latency bilan ushlasa, tizimda doim taxminan 100 ta faol so'rov yashaydi, demak thread pool va DB connection pool shuni ko'tarishi kerak. Ikkinchisi Amdahl qonuni: agar ishning 5 foizi ketma-ket bo'lsa, 32 yadroda maksimal tezlanish taxminan 14 barobar, 64 yadroda esa faqat 15 barobar. Ya'ni bitta global lock ostidagi 5 foizlik kod butun gorizontal o'sishni o'ldiradi.

Bu ikki qonun nimani o'lchashni aytadi, lekin qaysi kuchlar orasida tanlov qilinayotganini aytmaydi. Ularning katalogi `java.util.concurrent` ni yozgan Doug Lea dan keladi va to'rtta: xavfsizlik (concurrent type safety, ya'ni obyekt bir vaqtda ketayotgan boshqa amallardan qat'i nazar o'zi bilan izchil qolishi), tiriklik, unum va qayta ishlatiluvchanlik. Tiriklik bu yerda Kubernetes probe emas: har bir boshlangan harakat oxir-oqibat yoki oldinga ketadi, yoki yiqiladi degan xossa, va kalit so'z "oxir-oqibat", chunki vaqtincha to'xtash (qulfni kutish, tarmoq kirishini kutish, CPU yetmasligi) bilan doimiy to'xtash (deadlock, qaytarilmaydigan resurs nosozligi, yo'qolgan signal) ikki xil narsa. To'rt kuch bir-biriga qarshi turadi va shu qarshilik konkurent dizaynni qiyin qiladi: xavfsizlik "yomon narsa bo'lmasin" deydi, tiriklik esa "ish oldinga ketsin" deydi; qayta ishlatiladigan tizim ichki tuzilmasini ochishga moyil va shu bilan xavfsizlikni pasaytiradi; soddalikcha yozilgan xavfsiz tizim esa kafolatni qulfni ko'p ishlatish bilan oladi va unumni yo'qotadi (Evans va Verburg, 4.1.2-4.1.3, 79-80-betlar). Shu bobdagi har bir keyingi bo'lim aslida shu to'rtlik orasidagi bitta tanlov.

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

Prioritet shu rasmga uchinchi o'zgaruvchi qo'shadi, lekin u kafolat emas. Prioritet threadning boshqalariga nisbatan nisbiy ahamiyatini bildiradigan butun son, va mutlaq qiymat sifatida u ma'nosiz: yuqori prioritetli thread yolg'iz ishlayotgan bo'lsa pastdan tezroq ishlamaydi. Prioritet faqat qaysi threaddan qaysisiga o'tishni hal qilishda, ya'ni kontekst almashinuvi qoidasida ishlatiladi: thread boshqaruvni o'zi berganda (`yield`, `sleep` yoki blokirovka) ishga tayyorlar orasidan eng yuqori prioritetlisi CPU ni oladi, va past prioritetli thread yuqori prioritetlisi ishlashni xohlagan paytda preempt qilinadi. Teng prioritetli ikki thread holati esa OS ga qoladi: ba'zi tizimlar ularni round-robin bilan time-slice qiladi, boshqalarida esa teng prioritetli thread ixtiyoriy ravishda boshqaruvni bermasa qolganlari umuman ishlamaydi, va kitob bundan to'g'ridan-to'g'ri portativlik ogohlantirishini chiqaradi (Schildt, *Java The Complete Reference*, 12-nashr, 11-bob, 249-bet).

Deitel xuddi shu xulosani Java tomonidan takrorlaydi: har yangi thread o'zini yaratgan threadning prioritetini meros qiladi, va yuqori prioritet "ilova uchun muhimroq" degan norasmiy ma'noga ega bo'lsa ham, prioritet threadlarning bajarilish **tartibini kafolatlamaydi**; rejalashtirish platformaga bog'liq va ko'p threadli dasturning xulqi turli Java realizatsiyalarida farq qilishi mumkin (Deitel, *Java How to Program*, 10-nashr, 23.2.7, 962-963-betlar). Kitobning o'z tavsiyasi ham shundan chiqadi: `Thread` obyektini qo'lda yaratib boshqarish o'rniga `Executor` interfeysi ishlatiladi, prioritet esa sahna ortida OS bilan muloqot uchun qoladi va ko'pchilik dasturchi uni sozlamaydi. Qoida qisqa: prioritet to'g'rilik, tartib yoki adolat vositasi emas, va [rejalashtiruvchiga tayanmaslik qoidasi](#1112-thread-safety-darajasini-hujjatlash-va-ortiqcha-sinxronlashdan-qochish) aynan shu sababdan turadi. Bloch buni yana qattiqroq qo'yadi: prioritet Java ning eng kam ko'chma xususiyatlaridan biri, uni ishlab turgan programmaning javob berish sifatini sozlash uchun kamdan-kam ishlatish mumkin, lekin jiddiy tiriklik muammosini prioritet bilan hal qilishga urinish noto'g'ri yondashuv, chunki muammo bitta platformada yo'qolib boshqasida qaytadi (Bloch, Item 84, 337-bet).

Virtual thread bu rasmdagi bitta meros qoidasini ham buzadi. Platform thread uchun yangi thread o'zini yaratgan threadning daemon statusini meros qiladi, shuning uchun [JVM to'xtash semantikasida](31-deployment-haqiqati-konteyner-cgroup-jvm-va.md#3113-jvm-ning-ozi-qanday-toxtaydi-daemon-thread-shutdown-hook-va-halt) yozilgan "non-daemon thread JVM ni ushlab turadi" qoidasi ishlaydi. Virtual thread esa **doim** daemon: `setDaemon(boolean)` virtual threadga ta'sir qilmaydi va uni non-daemon qilib qo'ya olmaydi ([JEP 444](https://openjdk.org/jeps/444)). Shundan ikki amaliy natija: virtual threadda ketayotgan ish JVM to'xtashini kechiktirmaydi, shuning uchun tugashi kafolatlanishi kerak bo'lgan ish yoki non-daemon platform threadda, yoki shutdown hook bilan kutiladigan structured concurrency bloki ichida bajariladi; va "thread ni non-daemon qilib qo'yamiz, shunda yozib bo'lguncha JVM kutadi" shaklidagi eski yechim `spring.threads.virtual.enabled=true` yoqilgan ilovada jim ishlamay qoladi.

## 11.3 Umumiy holat (shared state) muammosi: poyga sharti va ko'rinuvchanlik

Konkurentlik xatolarining ikki turi bor va ular bir-biriga o'xshamaydi. Poyga sharti (race condition) atomarlik yo'qligidan kelib chiqadi: `balance = balance - amount` uch amaldan iborat, o'rtada boshqa thread kirib ketadi. Ko'rinuvchanlik (visibility) muammosi esa boshqa: bir thread yozgan qiymatni ikkinchi thread hech qachon ko'rmasligi mumkin, chunki qiymat CPU store buffer ida qolgan yoki JIT uni registrga ko'tarib (hoisting) tsikldan chiqarib tashlagan.

Java Memory Model bu yerda happens-before munosabati bilan ishlaydi. Amalda kerakli to'rt qoida: monitor dan chiqish keyingi kirishdan oldin sodir bo'ladi; `volatile` ga yozish keyingi o'qishdan oldin sodir bo'ladi; `Thread.start()` chaqirilishi yangi thread ichidagi hamma ishdan oldin; `Thread.join()` tugashi o'sha thread ishidan keyin. Agar ikki amal orasida happens-before bo'lmasa, JVM ularni istalgan tartibda ko'rsatishga haqli.

Poyganing chegarasini ham bilib turish kerak, aks holda diagnostika noto'g'ri yo'nalishga ketadi. Spetsifikatsiya shu chegarani aniq qo'yadi: massiv uzunligi, checked cast ning bajarilishi va virtual metod chaqiruvi ma'lumot poygasidan bevosita ta'sir ko'rmaydi (*The Java Language Specification, Java SE 25*, 17.4, 788-bet). Ya'ni poyga xulqni buzadi, qiymatni yo'qotadi va invariantni yemiradi, lekin JVM ning tur xavfsizligini buzmaydi: sinxronlanmagan `List` dan `ArrayIndexOutOfBoundsException` yoki `ClassCastException` chiqishi mumkin, chunki holat buzilgan, lekin tashqariga yolg'on turdagi obyekt chiqib ketmaydi va massiv chegarasidan tashqariga yozilmaydi. Buning amaliy qiymati diagnostikada: xotira buzilishini emas, buzilgan invariantni qidirish kerak.

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

`ReadWriteLock` ni tanlashdan oldin bitta narsani bilish kerak: u bitta xulq emas, beshta tanlovning birikmasi, va implementatsiyalar shu beshta bo'yicha farq qiladi. Qo'yib yuborish ustuvorligi: yozuvchi qulfni bo'shatganda navbatda ham o'quvchi, ham yozuvchi bo'lsa, qaysi biri oldin o'tadi. O'quvchi barging i: qulf o'quvchilarda, lekin yozuvchi navbatda bo'lsa, yangi kelgan o'quvchi darhol o'tadimi yoki yozuvchi ortida kutadimi (o'tsa konkurentlik oshadi, lekin yozuvchi och qolish xavfi paydo bo'ladi). Reentrancy: read va write qulflari qayta kirishga ruxsat beradimi. Pastga tushish: write qulfini ushlab turgan thread uni qo'yib yubormasdan read qulfini olishi mumkinmi. Va ko'tarilish: read qulfini write ga aylantirish mumkinmi. Oxirgisi ko'pchilik implementatsiyada ataylab yo'q, sababi esa aniq: oshkor ko'tarilish amali bo'lmasa u deadlock ga moyil, chunki ikki o'quvchi bir vaqtda ko'tarilishga urinsa, hech biri o'z read qulfini qo'yib yubormaydi va ikkisi ham kutib qoladi (Goetz, 13.5, 177-bet).

`ReentrantReadWriteLock` da javob qat'iy yozilgan: yozuvchidan o'quvchiga tushishga ruxsat bor, o'quvchidan yozuvchiga ko'tarilishga ruxsat yo'q va urinish deadlock bilan tugaydi (178-bet). Amalda eng ko'p yoziladigan xato shundan chiqadi: `readLock()` ni ushlab turib shart tekshiriladi, keyin shu blok ichida `writeLock()` so'raladi va thread o'zini o'zi qotirib qo'yadi. To'g'ri shakl ikkita: read qulfini ochiq `unlock` qilib, keyin write qulfini olib, shartni qayta tekshirish (oraliqda holat o'zgargan bo'lishi mumkin), yoki butun amalni boshidan write qulfi ostida bajarish. Shu tuzoq uchinchi sababni ham beradi: `ReadWriteLock` faqat kritik bo'lim uzun va o'qish ulushi yuqori bo'lgan joyda haqli, qolgan hamma joyda oddiy qulf yoki `ConcurrentHashMap` ham sodda, ham tez.

```java
// XATO: read ushlab turib write so'rash, shu threadning o'zi deadlock ga tushadi
lock.readLock().lock();
try {
    if (narxJadvali.isEmpty()) {
        lock.writeLock().lock();        // hech qachon qaytmaydi
    }
} finally { lock.readLock().unlock(); }

// TO'G'RI: read ni yopib, write ni olib, shartni QAYTA tekshirish
lock.readLock().lock();
boolean bosh;
try { bosh = narxJadvali.isEmpty(); }
finally { lock.readLock().unlock(); }

if (bosh) {
    lock.writeLock().lock();
    try {
        if (narxJadvali.isEmpty()) {    // oraliqda boshqa thread to'ldirgan bo'lishi mumkin
            narxJadvali.putAll(yukla());
        }
    } finally { lock.writeLock().unlock(); }
}
```

`StampedLock` optimistik o'qishni qo'shadi: `tryOptimisticRead` hech narsa yozmaydi, keyin `validate` yozuvchi kirganini tekshiradi. U reentrant emas, `Condition` bermaydi va noto'g'ri ishlatilsa ma'lumot yarim o'qilgan holatda qoladi.

| Mexanizm | Qachon | Narx | Asosiy xavf |
|---|---|---|---|
| `synchronized` | qisqa kritik bo'lim, oddiy holat | eng past, raqobatsiz ~20 ns | timeout yo'q, JDK 23 gacha virtual thread ni pin qiladi |
| `ReentrantLock` | timeout, interrupt, bir nechta Condition kerak | `synchronized` ga yaqin | `unlock` ni `finally` da yozish esdan chiqadi |
| `ReentrantReadWriteLock` | o'qish/yozish nisbati 10:1 dan yuqori, bo'lim uzun | o'qish ham CAS qiladi | yozuvchi ochligi, fair rejim sekin, read dan write ga ko'tarilish deadlock beradi |
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

Yana bir taqiq qulf obyektini **tanlashga** tegishli. JDK 8 dan boshlab Java da value-based sinf tushunchasi bor va API dagi bir qancha sinf shunday tasniflangan. Ularning qoidalari qatorida: sinf `final` bo'lishi va instansiya o'zgaruvchilari ham `final` bo'lishi shart; `equals` ikki instansiyani teng deb topsa, bittasini ikkinchisining o'rniga ishlatish mumkin; teng lekin alohida olingan ikki instansiya amalda bitta obyekt bo'lishi mumkin. Shundan aniq amaliy qoida chiqadi: value-based sinf instansiyasini sinxronlash uchun ishlatmaslik kerak (Schildt, *Java The Complete Reference*, 12-nashr, 13-bob, 345-bet). Ya'ni `Integer`, `Long`, `Boolean`, `Optional` va `java.time` sinflari ustida `synchronized` yozilmaydi: `synchronized (userId)` da `userId` `Long` bo'lsa, qulf obyekti autoboxing keshi tufayli butunlay boshqa kod bilan bo'lishilgan bo'lishi mumkin, yoki kesh oralig'idan tashqarida har chaqiruvda boshqa obyekt bo'lib qulf umuman ishlamasligi mumkin. To'g'ri shakl: qulf uchun maxsus `private final Object` yoki `ReentrantLock` maydoni, kalit bo'yicha qulflash kerak bo'lsa esa kalitdan qulf obyektiga `ConcurrentHashMap` bilan moslashtirish.

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

Shu yerda eng ko'p takrorlanadigan chalkashlik atomarlikni ko'rinuvchanlik bilan almashtirishdan kelib chiqadi. `long` va `double` dan boshqa o'zgaruvchini o'qish va yozish atomar, ya'ni yarim yozilgan qiymat o'qilmaydi, lekin atomarlik qiymat boshqa threadga ko'rinishini kafolatlamaydi; shuning uchun "ma'lumot atomar o'qiladi, sinxronlashni tashlab keting" shaklidagi maslahat xavfli xato (Bloch, Item 78, 311-bet). Ikkinchi yarmi ham shu joydan chiqadi: o'qish ham, yozish ham sinxronlanishi shart, faqat yozuvchi metodni sinxronlash yetarli emas, garchi ba'zi mashinalarda yoki ba'zi yuk ostida ishlayotganday ko'rinsa ham (Item 78, 314-bet). Kitob buni qoida shaklida ham beradi: sinxronlash o'zgaruvchiga murojaat qilinadigan HAR bir joyda kerak va hamma joyda bir xil qulf bilan (Goetz, 2.4, 19-bet).

Pastdagi apparat kafolatlari esa spetsifikatsiyada yozilgan va ularni bilish `volatile` ni qayerga qo'yishni belgilaydi.

| Amal | Atomarlik | Izoh |
|---|---|---|
| `int`, `boolean`, `char` va qisqa turlarga yozish va o'qish | atomar | ko'rinuvchanlik kafolatlanmaydi, bu alohida masala |
| `volatile` bo'lmagan `long` va `double` ga yozish | atomar emas | ikki 32-bitli yozuvga bo'linishi mumkin, boshqa thread bir yozuvning yuqori yarmini va boshqasining past yarmini ko'radi |
| `volatile long` va `volatile double` | atomar | shuning uchun umumiy 64-bitli o'zgaradigan maydon `volatile` qilinadi yoki qulf ostiga olinadi |
| Havolaga yozish va o'qish | doim atomar | 32-bitli yoki 64-bitli implementatsiyadan qat'i nazar |
| Qo'shni maydon yoki massiv elementlarini turli threadda yangilash | aralashmaydi | word tearing taqiqlangan: `byte[]` ning turli elementlarini sinxronlashsiz yangilash to'g'rilik jihatidan xavfsiz |

Jadvalning uchta qatori *The Java Language Specification, Java SE 25* ning 17.7 (802-bet) va 17.6 (801-bet) bandlariga tayanadi: spetsifikatsiya 64-bitli umumiy qiymatni `volatile` deb e'lon qilishni ochiq tavsiya qiladi, har bir maydon va massiv elementini esa alohida deb e'lon qiladi, ya'ni bir elementni yangilash boshqasining o'qilishiga yoki yangilanishiga ta'sir qilmasligi shart. Oxirgi qatorda ikkita tuzoq bor: word tearing yo'qligi faqat **to'g'rilik** haqida, ya'ni qiymat buzilmaydi, lekin bir threadning yozgani ikkinchisiga ko'rinishi baribir happens-before talab qiladi; va bir cache line ga tushgan qo'shni elementlarni turli yadroda yangilash [issiq maydon va false sharing](#1115-qulf-raqobatini-kamaytirish-qamrov-bolish-striping-va-issiq-maydon) masalasi bo'lib qoladi, ya'ni to'g'ri lekin sekin kod chiqadi.

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

Shunga qaramay framework ning o'zi to'g'ri va uning qiymati bitta ajratishda: Executor da ish birligi (`Runnable` yoki `Callable`, ya'ni vazifa) va uni bajarish mexanizmi ikki alohida narsa, shuning uchun bajarish siyosatini keyin, kodni qayta yozmasdan o'zgartirish mumkin (Bloch, Item 80, 324-bet). Amalda bu `new Thread(...)` yozilgan har bir joy keyinchalik sozlanmaydigan qarorni kodga muhrlab qo'yadi degani: pool o'lchami, navbat turi, rad etish siyosati, thread nomi va to'xtatish tartibi hammasi vazifa kodidan tashqarida yashashi kerak. Shu ajratishning ikkinchi mevasi fork-join: vazifalar `ForkJoinPool` da bajariladi va bo'sh qolgan thread band threaddan vazifa "o'g'irlaydi", parallel oqim esa shu pool ustida qurilgan, ya'ni fork-join ni qo'lda yozmasdan uning foydasini olish mumkin (Item 80, 324-bet). Narxi ham shundan kelib chiqadi: `parallelStream` umumiy `commonPool` ni ishlatadi, demak bitta joydagi bloklanadigan chaqiruv butun ilovadagi barcha parallel oqimni sekinlashtiradi.

To'g'ri yo'l `ThreadPoolExecutor` ni qo'lda sozlash. Asosiy mexanika: avval `corePoolSize` gacha thread yaratiladi, keyin navbat to'ldiriladi, navbat to'lgandan keyingina `maximumPoolSize` gacha yangi thread ochiladi. Shuning uchun cheksiz navbat bilan `maximumPoolSize` hech qachon ishlamaydi. Navbat sig'imi chekli bo'lishi va rad etish siyosati ongli tanlanishi kerak: `CallerRunsPolicy` chaqiruvchini sekinlashtirib backpressure beradi, `AbortPolicy` esa so'rovni tez rad etadi.

Shu mexanikaning eng ko'p e'tibordan qoladigan tuzog'i `corePoolSize` ni nolga qo'yishda. Odatda u "JVM chiqishini to'smasin" deb nolga qo'yiladi, lekin natija g'alati bo'ladi: navbat `SynchronousQueue` bo'lmasa, vazifa navbat TO'LGUNCHA umuman bajarilmaydi, chunki yangi thread faqat navbat to'lgandan keyin ochiladi. `ThreadPoolExecutor(0, 32, 60, SECONDS, new LinkedBlockingQueue<>(500))` konfiguratsiyasi shu sababli 500 vazifa yig'ilgunicha bitta ham thread ochmaydi. To'g'ri vosita Java 6 dan beri mavjud: `allowCoreThreadTimeOut` bilan pool ning hamma threadi, core threadlar ham, bo'sh turganda yo'qolishini so'rash mumkin, shuning uchun "thread qolib ketmasin" maqsadi uchun `corePoolSize` ni nolga tushirish kerak emas (Goetz, 8.3.1, 107-bet).

`ThreadPoolExecutor` kengaytirish uchun uchta hook ham beradi va kuzatuvchanlik uchun eng arzon joy aynan shu: `beforeExecute`, `afterExecute` va `terminated`. Har vazifaning vaqtini o'lchash, MDC ni to'ldirish yoki tozalash shu yerda qilinadi. Ikki chegara esa hujjatlanmagan holda surpriz beradi: `afterExecute` vazifa `Error` bilan tugaganda CHAQIRILMAYDI, demak metrikada jim yo'qotish paydo bo'ladi; `beforeExecute` dan `RuntimeException` uchib ketsa vazifa ham bajarilmaydi va `afterExecute` ham chaqirilmaydi (8.4, 111-bet). Shundan qoida: hook ichidagi kod o'z istisnosini o'zi yutishi kerak va vazifa sonini hook da emas, vazifaning o'zida sanash ishonchliroq.

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

Rejalashtirilgan va kechiktirilgan vazifa uchun esa `java.util.Timer` emas, `ScheduledExecutorService` yoki Spring ning `@Scheduled` i olinadi. `Timer` ham "bu vazifani 100 ms dan keyin bajar" va "har 10 ms da bajar" shaklidagi ishni boshqaradi, lekin kitob uni o'rnini bosuvchisi bor eskirgan vosita deb aytadi va ikki sababini beradi (Goetz, 6.2.5, 77-78-bet). Birinchi: `Timer` barcha vazifalar uchun **faqat bitta thread** yaratadi, demak bir vazifa uzoq ishlasa boshqalarining vaqt aniqligi buziladi; har 10 ms da ishlashi kerak bo'lgan vazifa yonida 40 ms ishlagan vazifa bo'lsa, rejalashtirish turiga qarab u yo uzun vazifa tugagach ketma-ket to'rt marta chaqiriladi, yo to'rt chaqiruvni butunlay o'tkazib yuboradi. Ikkinchi va og'irrog'i: `TimerTask` dan chiqqan tekshirilmaydigan istisno `Timer` threadini o'ldiradi, `Timer` esa threadni tiklamaydi va butun `Timer` bekor qilingan deb xato taxmin qiladi; shundan keyin rejalashtirilgan lekin bajarilmagan vazifalar hech qachon ishlamaydi va yangi vazifa qo'shib ham bo'lmaydi, chaqiruvchi esa `IllegalStateException` oladi. Kitobning xulosasi qat'iy: Java 5.0 va undan keyin `Timer` ishlatish uchun deyarli sabab yo'q. Bitta farqni esda tutish kerak: `Timer` mutlaq vaqt bo'yicha rejalashtirishni qo'llab-quvvatlaydi, ya'ni vazifa tizim soati o'zgarishiga sezgir bo'lishi mumkin, `ScheduledThreadPoolExecutor` esa faqat nisbiy vaqt bilan ishlaydi. Non-daemon `Timer` ni to'xtatmaslik esa dastur tugashini ushlab turadi, shuning uchun uni tugashda `cancel()` bilan to'xtatish kerak (Schildt, *Java The Complete Reference*, 12-nashr, 21-bob, 673-bet); bu [JVM to'xtash semantikasi](31-deployment-haqiqati-konteyner-cgroup-jvm-va.md#3113-jvm-ning-ozi-qanday-toxtaydi-daemon-thread-shutdown-hook-va-halt) bilan bir xil muammoning ko'rinishi.

`ScheduledExecutorService` ga o'tgandan keyin ham bitta tanlov qoladi va u xotira bilan to'g'ridan-to'g'ri bog'liq. `scheduleAtFixedRate` har davrda yangi vazifa yuboradi va oldingisi tugaganini kutmaydi, shuning uchun vazifa o'z davridan uzoq ishlasa navbat o'sib boradi va dastur oxir-oqibat yig'ilgan vazifalardan heap ga sig'may yiqiladi (Boyarsky/Selikoff, *OCP Java SE 17 Study Guide*, 13-bob, 738-bet). `scheduleWithFixedDelay` esa kechikishni oldingi vazifa tugaganidan keyin hisoblaydi, ya'ni navbat o'smaydi. Qoida: davriy vazifaning bajarilish vaqti davrdan qisqa ekani o'lchangan bo'lmasa, `fixedRate` emas, `fixedDelay` tanlanadi; Spring da bu `@Scheduled(fixedDelayString = ...)` va `@Scheduled(fixedRateString = ...)` orasidagi ayni shu tanlov.

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

`CompletableFuture` dan oldin JDK da shu maqsad uchun ikkinchi vosita bor va bir qancha holatda u soddaroq: `CompletionService`. U `Executor` va `BlockingQueue` funksiyasini birlashtiradi. Vazifa to'plamini `submit` bilan yuborib, natijalarni `take` va `poll` bilan **tayyor bo'lish tartibida** olasiz, `Future` lar ro'yxatini nol timeout bilan aylanib poll qilish kerak bo'lmaydi. `ExecutorCompletionService` ichida sodda: yuborilgan har vazifa `FutureTask` ning `done` metodini override qiladigan `QueueingFuture` ga o'raladi va u natijani navbatga qo'yadi, `take` va `poll` esa shu navbatga delegatsiya qiladi (Goetz, 6.3.5, 81-82-bet). Bir nechta `CompletionService` bitta `Executor` ni bo'lishishi mumkin, shuning uchun aniq bir hisob uchun xususiy `CompletionService` yasab umumiy pool ni saqlab qolish to'liq mantiqli: shunda `Future` bitta hisobning ushlagichi bo'lgani kabi `CompletionService` bir **to'plam** hisobning ushlagichi bo'ladi, va yuborilgan vazifa soni bilan olingan natija sonini solishtirib to'plam tugaganini bilib olasiz (6.3.6, 82-bet). `invokeAll` dan farqi aniq: `invokeAll` hammasi tugaguncha bloklanadi va `Future` larni yuborish tartibida qaytaradi, `CompletionService` esa har natijani kelgan zahoti berib, qism natijani darhol ishlatishga yo'l qoldiradi.

Parallellashtirishning chegarasini ham shu yerda ko'rib qo'yish kerak. Turli xil (heterogen) vazifalarni ishchilar orasida bo'lish idish yuvishga o'xshaydi: biri yuvadi, biri quritadi, lekin yana bir necha kishi kelsa ularni halaqit bermaydigan qilib joylash yo'li ko'rinmaydi. Kitob bunga ikki aniq raqam qo'shadi: A va B vazifalarini ikki ishchi orasida bo'lsangiz va A B dan o'n barobar uzoq ishlasa, umumiy jarayonni faqat 9 foizga tezlatgan bo'lasiz; ikki thread bilan erishilishi mumkin bo'lgan eng yaxshi natija esa ikki barobar (Goetz, 6.3.4, 80-81-bet). Shundan qoida chiqadi: ishni vazifalarga bo'lishning haqiqiy foydasi **ko'p sonli, mustaqil va bir turdagi** vazifa bo'lganda keladi. Fan-out shaklidagi oqimda bu [Amdahl qonuni](08-ishlash-va-resurs-hissi-napkin-math.md#811-amdahl-qonuni-ketma-ket-ulush-masshtablanishning-chegarasi) bilan bir xil gapni aytadi: `thenCombine` va `allOf` natijasining vaqtini eng sekin shox belgilaydi, shuning uchun qaror shoxlar sonini oshirish emas, eng sekin shoxni qisqartirish yoki unga timeout qo'yib degradatsiyaga ruxsat berish bo'ladi.

## 11.10 Deadlock, livelock va ochlik (starvation): sabab va oldini olish

Deadlock to'rt shart bir vaqtda bajarilganda yuzaga keladi: o'zaro istisno, lockni ushlab turib ikkinchisini kutish, lockni tortib olish imkonsizligi, va aylana kutish. Amalda eng ko'p uchraydigani aylana: bitta thread hisob A ni keyin B ni lock qiladi, ikkinchisi teskari tartibda. Yechim eng oddiy shartni buzish: lock olish tartibini global qilib belgilash, masalan hisob ID si bo'yicha o'sish tartibida.

Lock tartibini global belgilash alohida hodisa emas, umumiy qoidaning ko'rinishi. Fairbanks arxitekturaga yo'naltirilgan dizaynni shu bilan ta'riflaydi: siz duch kelgan muammoga lokal tuzatish emas, arxitektura darajasidagi, ya'ni universal qo'llanadigan yechim izlanadi (*Just Enough Software Architecture*, 2.7-bo'lim). Uning misollari shu bobning mavzusini qoplaydi: tizim qulf olishi kerak bo'lsa, deadlock dan qochish uchun tartib konvensiyasiga ergashiladi; garbage collection bo'lmasa, xotira sizishini oldini olish uchun xotirani bo'shatishning standarti qo'yiladi, masalan modul qamroviga qarab; kesh ishlatilsa, kesh izchilligini saqlash uchun kirish cheklanadi; buyurtma xabari yo'qolmasligi kerak bo'lsa, davomiylik kafolati bor message queue ishlatiladi. Fairbanks ikki tomonini ham aytadi: xotira sizishini topilgan paytda tuzatish ham yo'l, lekin u lokal yo'l. Amaliy belgi oddiy: qoida kod review da og'zaki aytilsa, u lokal tuzatish; qoida bitta joyda yozilgan va tekshiriladigan bo'lsa, u arxitektura yechimi.

Qulf tartibining eng ko'p o'tkazib yuboriladigan kod yo'li seriyalash. `writeObject` obyektning butun holatini o'qiydi, shuning uchun unga obyekt holatini to'liq o'qiydigan boshqa metodga qo'yilgan sinxronlashning o'zi qo'yiladi; lekin shu bilan `writeObject` qulf oladigan yana bitta yo'lga aylanadi va u qolgan faoliyat bilan bir xil qulf tartibiga rioya qilmasa, resurs tartibi deadlocki chiqadi (Bloch, Item 87, 351-bet). Amalda bu "o'zim chaqirmayman" deb o'ylangan joyda yonadi, chunki seriyalashni ko'pincha infratuzilma chaqiradi: sessiya replikatsiyasi va passivatsiyasi, taqsimlangan keshga yozish, obyektni navbatga Java seriyalash bilan qo'yish. Eng sodda yechim seriyalanadigan holatni qulf ostida bir marta immutable snapshotga ko'chirish va shu snapshotni yozish.

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
| `writeObject` ichida sinxronlash | seriyalash yo'li boshqa qulf tartibi bilan kesishadi, deadlock | holatni qulf ostida snapshotga olib, snapshotni seriyalash |

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

Eng kuchli shakl esa konkurentlikni butunlay infratuzilmaga ko'tarish. Fairbanks ning email ishlovchi tizimida `Filter` superklassi shu ishni qiladi: har bir filter o'z thread ida ishlaydi va kirishini inkremental ishlab chiqadi, superklass esa Template method patternini qo'yib, avlodlardan faqat `work()` metodini implement qilishni talab qiladi; shu bilan tizimdagi konkurentlikni boshqarish bir joyda standartlashtiriladi va soddalashtiriladi (*Just Enough Software Architecture*, 10.8-bo'lim). Ikkinchi yarmi connector da: filterlar bir-biri bilan faqat thread-safe `Pipe` orqali gaplashadi, shuning uchun yangi filter yozadigan odam thread haqida umuman o'ylamaydi va filter soni oshganda tashvish o'smaydi. Narxi ham bor va Fairbanks uni ochiq aytadi: ideal holda implementatsiya filterlarning batch emas, inkremental ishlashi cheklovini majburlashi kerak edi, lekin buni kodda majburlash yo'li ko'rinmaydi, xuddi shunday filterlar faqat pipe orqali gaplashishini ham; shuning uchun cheklovlar izoh shaklida yoziladi va `Filter` sinfi izoh uchun yaxshi joy bo'ladi. Java ning bitta superklass cheklovi ham eslatiladi: interfeys ishlatish mumkin, lekin u holda konkurentlikni hoisting qilish imkoni yo'qoladi.

```java
// Konkurentlik bir joyda hal qilinadi: har filter o'z thread ida.
public abstract class Filter implements Runnable {

    // DIQQAT: work() inkremental ishlashi shart, batch emas.
    // Bu cheklovni kompilyator tekshirmaydi, review tekshiradi.
    // DIQQAT: filter tashqariga faqat Pipe orqali yozadi.
    protected abstract void work() throws InterruptedException;

    @Override
    public final void run() {
        try {
            work();
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
    }
}

// Pipe thread-safe: filter yozuvchisi sinxronlash haqida o'ylamaydi.
public final class Pipe<T> {
    private final BlockingQueue<T> navbat = new LinkedBlockingQueue<>(1000);

    public void write(T element) throws InterruptedException {
        navbat.put(element);                 // to'lsa backpressure beradi
    }

    public T read() throws InterruptedException {
        return navbat.take();
    }
}
```

ESLATMA: yuqoridagi Java kodi shu korpusning tarjimasi. Fairbanks `Filter` da `System.exit(1)` bilan tugaydigan `catch` blokini beradi; korpus uning o'rniga interrupt holatini tiklashni tanladi, chunki JVM ni o'chirish Spring ilovasida qabul qilinmaydigan reaksiya. Sig'imi 1000 ga teng `LinkedBlockingQueue` ham korpusning tanlovi, kitobda sig'im berilmagan.

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

Hujjat nega kerakligining sababi esa shu talabning tarqalishida. Thread xavfsizligi yuqumli: framework ilova komponentini o'z threadida chaqiradi, komponent ilova holatiga tegadi, demak SHU holatga tegadigan har bir kod yo'li thread-safe bo'lishi shart, garchi o'sha yo'llarning ko'pi bitta threadda yozilgan va sinalgan bo'lsa ham (Goetz, 1.1, 8-9-betlar). Bitta `@Scheduled` metod qo'shilishi shu sababli uzoqdagi sinfning ham talabini o'zgartiradi, va kodda bu o'zgarish ko'rinmaydi: aynan shuning uchun daraja hujjatda yoziladi.

Lekin hujjatning o'zi eng kuchsiz vosita va bu tartib bilib ishlatiladi. Xavfsizlik mexanizmlari kuchi bo'yicha to'rt pog'onada turadi: birinchi va eng kuchlisi har bir quyi tizimning tashqi aloqasini imkon qadar cheklash, ya'ni ma'lumotni yashirish; ikkinchisi ichki tuzilmani imkon qadar determinatsiyalangan qilish, masalan quyi tizim ichidagi thread va obyektlarni oldindan bilinadigan qilib loyihalash; uchinchisi mijoz ilova rioya qilishi kerak bo'lgan siyosat belgilash (kuchli, lekin mijozning hamkorligiga tayanadi va buzilganda diagnostikasi qiyin); to'rtinchisi va eng kuchsizi talab qilinadigan xatti-harakatni hujjatlash, u ba'zan boshqa yo'l bo'lmaganda tanlanadi (Evans va Verburg, 4.1.3, 80-81-betlar). Shuning uchun "Javadoc da yozib qo'ydim" javobi faqat yuqoridagi uchtasi amalda imkonsiz bo'lganda qabul qilinadi.

"Shartli thread safe" darajasi eng ko'p xato keltiradi, chunki u qanday qulfdan foydalanish kerakligini ham aytishi kerak. Javadoc da bu bitta gap bo'ladi: "iteratsiya paytida obyektning o'zida sinxronlanadi".

Hujjatlash talabining chegarasi ham aniq. Qaytish turi obyektning thread xavfsizligini ko'rsatmasa, uni qaytaradigan statik fabrika shu xossani hujjatlashi shart, chunki chaqiruvchi faqat interfeys nomini ko'radi va `Collections.synchronizedMap` qaytargan `Map` bilan oddiy `HashMap` orasidagi farqni imzodan bilmaydi; `enum` turining o'zgarmasligini esa hujjatlash kerak emas, u tilning kafolati (Bloch, Item 82, 331-bet).

Hujjat jim bo'lgan holat alohida qoida talab qiladi, chunki u ko'p uchraydi: JDBC spetsifikatsiyasida "thread" va "concurrent" so'zlari umuman uchramaydi, servlet spetsifikatsiyasida esa juda kam, ya'ni `ServletContext`, `HttpSession` va `DataSource` uchun kafolat yozilmagan (Goetz, 4.5.1, 50-bet). Taxmin qilishdan boshqa yo'l yo'q, lekin taxminning sifatini oshirish mumkin: spetsifikatsiyani uni **ishlatuvchi** emas, **realizatsiya qiluvchi** (konteyner yoki baza vendori) nuqtai nazaridan o'qish kerak. Servlet doim konteyner boshqaradigan threadda chaqiriladi va konteyner o'zi bir nechta thread yaratganini biladi, demak bir nechta servletga xizmat ko'rsatadigan obyektlarga bir vaqtda murojaat qilinishini kutishi shart; bunday obyekt faqat bitta threadli kontekstda foydali bo'ladigan holatni tasavvur qilish mumkin emas, shuning uchun u thread-safe qilingan deb hisoblanadi. Qo'shimcha dalil ham bor: spetsifikatsiya va rasmiy qo'llanmalardagi misollarda bu obyektlarga murojaatda klient tomonida hech qanday sinxronlash ko'rsatilmaydi.

Lekin shu mulohazadan **teskari** xulosa ham chiqadi va u ko'pincha o'tkazib yuboriladi. `setAttribute` bilan `HttpSession` yoki `ServletContext` ga qo'yilgan obyektlar konteynerniki emas, ilovaniki, va spetsifikatsiya ularga bir vaqtda murojaatni muvofiqlashtirish uchun hech qanday mexanizm taklif qilmaydi. Shuning uchun ular o'zi thread-safe yoki amalda o'zgarmas (effectively immutable) bo'lishi kerak: konteyner `HttpSession` ni replikatsiya yoki passivatsiya uchun serializatsiya qilishi mumkin va sizning qulflash protokolingizni bilmaydi, demak tashqi qulf bilan himoyalash yetarli emas (4.5.1, 50-bet). Xuddi shu mulohaza `DataSource` va undan olingan `Connection` ni ajratadi: `DataSource.getConnection` qo'shimcha klient qulfini talab qilmaydi deb hisoblanadi, lekin `Connection` pool ga qaytarilmaguncha boshqa faoliyat bilan bo'lishishga mo'ljallanmagan, shuning uchun bir nechta threadga yoyilgan faoliyat `Connection` ga murojaatni o'zi sinxronlashi kerak. Bu holat Spring da kamdan-kam ko'rinadi, chunki `Connection` so'rov davomida threadga qamalgan bo'ladi, lekin `@Async` yoki `parallelStream` bilan chegara buzilsa qoida darhol kuchga kiradi.

Daraja tanlashning o'zi ham qaror, va u yozilayotgan sinfga tegishli. O'zgaradigan sinf yozayotganda ikki variant bor: sinxronlashni butunlay tashlab, uni mijozga qoldirish va buni hujjatda aytish, yoki sinxronlashni sinf ichida qilish; ikkinchisi faqat ichki sinxronlash bilan mijoz tomonidagidan sezilarli yuqori konkurentlik olinganda tanlanadi (Bloch, Item 79, 322-bet). Standart kutubxonaning o'zi ikki yo'lni ikki paketga ajratgan: `java.util` birinchi yo'lni tanlagan (`ArrayList`, `HashMap` thread-safe emas), `java.util.concurrent` ikkinchisini (`ConcurrentHashMap` ichida himoyalangan). Amalda domen sinfi uchun deyarli har doim birinchi yo'l to'g'ri: sinfni o'zgarmas yoki threadga qamalgan qilish, sinxronlashni esa o'rab turgan komponentga chiqarish.

Ichida sinxronlash tanlansa, qulf obyektining ko'rinishi alohida qaror bo'ladi. Qulfni oshkor (public) qilish, masalan `synchronized (this)` bilan, mijozga sinf metodlaridan atomar ketma-ketlik yasash imkonini beradi, lekin ikki narxi bor: u yuqori unumli ichki konkurentlik nazorati bilan (masalan `ConcurrentHashMap` dagi striping bilan) sig'ishmaydi, va mijoz qulfni uzoq ushlab turib xizmatni rad etish hujumini amalga oshirishi mumkin; yechim qulf uchun `private final Object` maydoni (Bloch, Item 82, 331-bet). Shuning uchun `synchronized` metod yozish aslida qulfni API ga chiqarish degani va bu qaror ongli bo'lishi kerak.

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

Lekin qulfga tegishdan oldin raqobat haqiqatan ham aybdor ekani tekshiriladi, chunki "CPU to'liq band emas" belgisining to'rtta sababi bor va faqat bittasi qulf. Birinchi: yuk yetarli emas, ya'ni mijoz tomoni yoki yuk generatori o'z sig'imida ishlayapti, tekshirish usuli yukni oshirib utilizatsiya, javob vaqti va xizmat vaqtining o'zgarishini kuzatish. Ikkinchi: I/O ga bog'liqlik, disk yoki tarmoq chegarasi. Uchinchi: tashqi servisga bog'liqlik, ya'ni bo'g'iz bazada yoki boshqa servisda, va buni profiler yoki baza administratsiya vositasi bilan "javob kutishda qancha vaqt ketdi" savoliga javob berib ajratiladi. To'rtinchi: qulf raqobati. Bundan tashqari nosimmetrik yuklanish (ba'zi CPU qizigan, ba'zisi bo'sh) alohida ma'no beradi: hisobning katta qismi kichik thread to'plamida ketayapti, demak birinchi vazifa qulfni emas, parallellikni oshirish (Goetz, 11.4.6, 149-bet). Shu bo'limning diagnostika uchun eng foydali tafsiloti ham shu yerda: kam raqobatli qulf [thread dumpda](#1111-konkurentlik-xatolarini-topish-thread-dump-oqish) kamdan-kam ko'rinadi, ko'p raqobatlisi esa deyarli har dumpda kamida bitta kutuvchi thread bilan chiqadi, shuning uchun profiler bo'lmasa ham bir necha tasodifiy dump "issiq" qulfni aytib beradi.

| Yo'l | Nima qilinadi | Qachon |
|---|---|---|
| Qamrovni qisqartirish | qulf ichidan I/O, hisob va log chiqariladi | har doim birinchi |
| Qulfni bo'lish (splitting) | mustaqil holat uchun alohida qulf | bitta qulf bir necha mustaqil maydonni himoyalayotganda |
| Striping | holat N bo'lakka bo'linib, har biriga o'z qulfi | bitta katta to'plam ustida raqobat bo'lsa |
| Qulfni olib tashlash | o'zgarmas obyekt, thread-local, atomic | holat haqiqatda umumiy bo'lmasa |
| Hand-over-hand qulflash | har node ga alohida qulf, keyingisini olib oldingisini qo'yib yuborish | bog'langan tuzilmani thread lar turli joyidan aylanganda |

```java
// yomon: bitta qulf ikki mustaqil holatni himoyalaydi, ikkisi bir-birini kutadi
public synchronized void addOrder(Order o) { orders.add(o); }
public synchronized void addUser(User u) { users.add(u); }

// yaxshi: qulf bo'lindi, ikki oqim bir-birini kutmaydi
private final Object ordersLock = new Object();
private final Object usersLock = new Object();
```

Jadvalning oxirgi qatori alohida izoh talab qiladi, chunki u `synchronized` bilan **bajarilmaydi**. Bog'langan ro'yxatda butun tuzilmaga bitta qulf qo'yish o'rniga har node ga alohida qulf beriladi, va tuzilmani aylanayotgan thread keyingi node ning qulfini OLGANDAN KEYIN oldingisini qo'yib yuboradi; shu bilan turli thread ro'yxatning turli qismida bir vaqtda ishlaydi. Bu usul hand-over-hand qulflash yoki lock coupling deb ataladi va u blok-strukturali emas, ya'ni qulf olish va qo'yib yuborish bitta leksik blokka sig'maydi (Goetz, 13.1.4, 174-bet). `synchronized` qulfni blok oxirida majburan bo'shatadi, shuning uchun bu naqsh faqat `ReentrantLock` bilan yoziladi va u [`ReentrantLock` ni haqli qiladigan](#114-synchronized-reentrantlock-readwritelock-va-stampedlock-farqi) to'rtinchi holat (qolgan uchtasi: vaqt chegarasi bilan olish, uzilishga javob beradigan olish va adolatli navbat). Narxi ham bor va u yozishdan oldin hisobga olinadi: qulf tartibi tuzilma bo'ylab bir tomonlama bo'lishi shart, aks holda ikki thread ro'yxatni ikki tomondan aylanganda klassik aylana deadlock chiqadi.

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

Qulf tanlashdagi eng nozik xato shu yerda yashiradi: bitta umumiy holatni ikki xil monitor himoya qilishi. `OCP Oracle Certified Professional Java SE 17 Developer Practice Tests` ning 8-bobidagi 36-savoli buni aniq ko'rsatadi. Sinfda `static int cookies` maydoni bor, uni instans `synchronized` metodi (`deposit`) va static `synchronized` metodi (`withdrawal`) o'zgartiradi; dastur kompilyatsiya qiladi va istisno tashlamaydi, lekin ikki metod turli obyektlarda sinxronlanadi, ya'ni instans metodi `bank` obyektida, static metodi esa `Bank.class` obyektida, shuning uchun ular bir-birini chiqarmaydi. Qo'shimcha sabab esa qo'shma amalda: `+=` va `-=` atomik emas, demak bir chaqiruv qiymatni o'zgartirayotganda ikkinchisi xuddi shu qiymat ustida ishlab turishi mumkin va o'zgarish yo'qoladi; natijada 25 ta qo'shish va 25 ta ayirishdan keyin chiqadigan son oldindan aytilmaydi (Appendix, 8-bobning javoblari, 36-savol). Ikki metod bir xil obyektda sinxronlangan bo'lsa, maydon konkurent o'zgartirishdan himoyalanadi va natija `0` chiqadi.

Shundan amaliy qoida chiqadi va u [11.12](#1112-thread-safety-darajasini-hujjatlash-va-ortiqcha-sinxronlashdan-qochish) bo'limidagi hujjatlash talabining asosi: umumiy holatning qulfi hujjatda nomlanishi va shu holatga tegadigan har bir metod aynan shu qulfni olishi kerak. Static maydonni instans metodi himoya qila olmaydi, va teskarisi ham shunday.

Shu qoidaning kuchliroq shakli ham bor va amalda eng ko'p buziladigani ayni shu. Har bir o'zgaradigan umumiy o'zgaruvchiga aynan bitta qulf biriktirish yetarli emas: sinfda bir nechta o'zgaruvchini qamragan invariant bo'lsa, shu invariantda qatnashadigan HAMMA o'zgaruvchi BIR XIL qulf bilan himoyalanishi kerak, chunki faqat shunda ularni bitta atomar amalda o'qish yoki yangilash va invariantni saqlab qolish mumkin (Goetz, 2.4, 20-bet). Ya'ni qulf chegarasi maydon bo'yicha emas, invariant bo'yicha chiziladi. Bu nega muhim: `AtomicReference` va `AtomicLong` lardan yig'ilgan "thread-safe" sinf har maydoni darajasida atomar bo'lsa ham invariant darajasida buzuq bo'lishi mumkin, chunki ikki atomar amal orasidagi oynada boshqa thread yarim yangilangan holatni ko'radi. Buning review dagi belgisi oddiy: bitta metod ketma-ket ikki yoki undan ko'p `set` chaqirsa va o'quvchi ularni birga o'qisa, invariant himoyalanmagan.

```java
// XATO: har maydon alohida atomar, invariant (kurs va uning vaqti birga) himoyalanmagan
@Component
public class RateCache {
    private final AtomicReference<BigDecimal> rate = new AtomicReference<>();
    private final AtomicReference<Instant> asOf = new AtomicReference<>();

    public void refresh(BigDecimal newRate, Instant newAsOf) {
        rate.set(newRate);          // ikki set orasidagi oynada o'quvchi
        asOf.set(newAsOf);          // yangi kursni eski vaqt bilan ko'radi
    }

    public Quote current() {
        return new Quote(rate.get(), asOf.get());
    }
}

// TO'G'RI: invariant bitta immutable qiymatga yig'ilib, bitta amalda almashadi
@Component
public class RateCacheFixed {
    private final AtomicReference<Quote> quote =
            new AtomicReference<>(Quote.EMPTY);

    public void refresh(BigDecimal newRate, Instant newAsOf) {
        quote.set(new Quote(newRate, newAsOf));   // bitta atomar almashtirish
    }

    public Quote current() {
        return quote.get();                        // yarim yangilangan holat ko'rinmaydi
    }
}

public record Quote(BigDecimal rate, Instant asOf) {
    public static final Quote EMPTY = new Quote(null, Instant.EPOCH);
}
```

Ikki yo'ldan birini tanlash qoidasi ham shundan chiqadi: invariantdagi o'zgaruvchilarni bitta qulf ostiga olish, yoki ularni bitta o'zgarmas obyektga yig'ib, o'sha obyekt havolasini atomar almashtirish. Ikkinchisi odatda arzonroq, chunki o'quvchi hech narsa qulflamaydi, va u [xavfsiz nashr](#1113-xavfsiz-nashr-safe-publication-va-obyektning-qochib-ketishi) qoidasiga ham tabiiy mos keladi.

Qulfning o'zi qanday ishlaydi. Har bir Java obyekti sinxronlash uchun qulf bo'lib xizmat qilishi mumkin va bu ichki qulflar intrinsic lock yoki monitor lock deb ataladi. `synchronized` metod butun metod tanasini qamragan blokning qisqartmasi, qulf esa metod chaqirilgan obyekt; statik `synchronized` metod `Class` obyektini qulf sifatida oladi. Qulf avtomatik olinadi va blokdan chiqishda, hatto istisno uchib ketganda ham avtomatik bo'shaydi. Intrinsic lock mutex sifatida ishlaydi: bir vaqtda ko'pi bilan bitta thread uni egallaydi.

Bu "avtomatik bo'shashi" qanday ta'minlanganini bilish bitta amaliy qoidani asoslaydi. Metod va blok uchun mexanizm ikki xil. `synchronized` METOD alohida instruksiya bilan emas, metodning `ACC_SYNCHRONIZED` flagi bilan belgilanadi: monitor metod chaqirilganda olinadi va metod normal yoki noodatiy, ya'ni istisno bilan tugaganidan qat'i nazar qo'yib yuboriladi (*The Java Virtual Machine Specification, Java SE 25* (Lindholm, Yellin, Bracha, Buckley, Smith), 2.11.10, 39-bet). `synchronized` BLOK esa `monitorenter` va `monitorexit` ga kompilyatsiya qilinadi, va kompilyator har `monitorenter` ga juft `monitorexit` bajarilishini kafolatlaydi: buning uchun u har qanday istisnoni tutadigan yashirin handler yaratadi, handler `monitorexit` ni bajarib istisnoni qayta tashlaydi (3.14, 70-71-bet). Shundan chiqadigan qoida: `synchronized` qulfni istisno yo'lida oqib ketkaza olmaydi, shuning uchun unda `finally` yozilmaydi, `ReentrantLock` da esa shu kafolatni kompilyator bermaydi va `finally { lock.unlock(); }` majburiy bo'ladi. Yashirin handler yana bir narsani tushuntiradi: bytecode da `synchronized` bloki bor metodda hech kim yozmagan istisno yo'li paydo bo'ladi, shuning uchun bytecode darajasida ishlaydigan vositalar (qamrov o'lchagich, statik tahlilchi) o'sha metodda sizning kodingizda ko'rinmaydigan shoxni ko'rsatishi mumkin.

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

Kitob yo'qolgan signalni (missed signal) alohida liveness nosozligi sifatida nomlaydi va ta'rifi aniq: thread allaqachon rost bo'lgan shartni kutishi kerak bo'lsa, lekin kutishdan oldin shart predikatini tekshirmasa, u sodir bo'lib bo'lgan hodisa haqida xabar kutib qoladi va bu kutish abadiy bo'lishi mumkin. Xabar yopishqoq emas: A thread condition queue da `notify` qilib, keyin B thread o'sha navbatda `wait` qilsa, B darhol uyg'onmaydi, uni uyg'otish uchun yana bitta xabar kerak bo'ladi. Yo'qolgan signal kod xatosining natijasi, va yuqoridagi shakl, ya'ni predikatni `wait` dan oldin ham, keyin ham tekshirish, bu muammoni butunlay yopadi (Goetz, 14.2.3, 185-bet).

Predikat `isOpen` kabi bitta bayroqdan murakkabroq bo'lishi kerak bo'lgan klassik holat ham bor: qayta yopiladigan darvoza. Darvoza tez ochilib yopilsa, ochilish paytida kutib turgan threadlarning hammasi o'tib ketolmaydi, chunki uyg'ongan thread qulfni qayta olgunicha darvoza yana yopilgan bo'lishi mumkin va u yopiq darvozani ko'rib qaytib kutadi. Yechim predikatni boyitish: har yopilishda `generation` hisoblagichi oshiriladi, kutuvchi esa kelganidagi generatsiyani eslab, "hozir ochiqmi YOKI men kelganimdan keyin bir marta ochilganmi" shartini tekshiradi (Goetz, 14.2.5, 186-187-betlar).

```java
public class ThreadGate {
    private boolean open;            // @GuardedBy("this")
    private int generation;          // @GuardedBy("this")

    public synchronized void open() {
        open = true;
        notifyAll();                 // hamma kutuvchi predikatini qayta tekshiradi
    }

    public synchronized void close() {
        open = false;
        ++generation;                // yopilish hodisasi raqamga aylanadi
    }

    public synchronized void await() throws InterruptedException {
        int arrival = generation;    // kelgan paytdagi generatsiya
        while (!open && arrival == generation) {
            wait();                  // ochilib yopilgan bo'lsa predikat rost bo'lib qoladi
        }
    }
}
```

Shu naqsh qayta o'zgarib turadigan har qanday holat uchun kerak bo'ladi: feature flag ning yoqilib o'chishi, circuit breaker ning ochilib yopilishi, konfiguratsiyaning qayta yuklanishi. Bayroqning joriy qiymatini kutish o'zgarish hodisasini o'tkazib yuboradi, generatsiya esa hodisani raqamga aylantirib, o'tkazib yuborishni imkonsiz qiladi. Xabar berish tomonida esa standart tanlov `notifyAll`: u konservativ va har holda to'g'ri, `notify` esa faqat kutish to'plamidagi hamma thread bir xil shartni kutsa va shart rost bo'lganda bir vaqtda faqat bitta thread foyda ko'rsa, optimallashtirish sifatida tanlanadi (Bloch, Item 81, 329-bet).

Condition queue obyektining **ko'rinishi** esa dizayn qarori. Qoida: condition queue ni u ishlatiladigan sinf ierarxiyasidan tashqarida ko'rinmas qilish. Aks holda chaqiruvchilar sizning kutish va xabar berish protokolingizni tushundik deb o'ylab, uni dizayningizga zid ishlatishi mumkin; yakka xabar berish (single notification) uchun kerak bo'lgan "hamma kutuvchilar bir xil" shartini esa condition queue siz nazorat qilmaydigan kodga ochiq bo'lsa majburlab bo'lmaydi, chunki begona kod sizning navbatingizda kutib qolsa protokol buziladi va signal o'g'irlanadi (hijacked signal) (14.2.7, 187-bet). Amaliy shakl yuqoridagi misolda: `this` o'rniga `private final Object lock`. Buning narxi bor va kitob uni aytadi: bunday sinf klient tomonda qulflashni (client-side locking) qo'llab-quvvatlamaydi.

Vorislik uchinchi tuzoq. Shartli yoki yakka xabar berish subklassga cheklov qo'yadi, shuning uchun holatga bog'liq sinf kutish va xabar berish protokollarini subklassga to'liq ochib hujjatlashi, yoki subklassni ularda qatnashishdan butunlay to'sishi kerak: `final` qilish yoki condition queue, qulf va holat o'zgaruvchilarini yashirish. Eng yomon variant holatni subklassga ochib protokolni hujjatlashtirmaslik, bu holat o'zgaruvchilarini ochib invariantni yozmaslik bilan teng. Kitobning misoli: `pop` ni bloklaydigan cheksiz stack yakka xabar berish shartlarini qanoatlantiradi, lekin subklass "ketma-ket ikki elementni pop qilish" metodini qo'shsa, endi ikki sinf kutuvchi paydo bo'ladi va yakka xabar berish buziladi; bazaviy sinf condition queue ni ochib protokolni hujjatlagan bo'lsagina subklass `push` ni override qilib `notifyAll` chaqirib zararni tuzata oladi (14.2.6, 187-bet).

Amalda esa yuqori darajadagi vosita tanlanadi: `BlockingQueue`, `Semaphore`, `CountDownLatch` yoki `Condition`. Pattern nuqtasidan bu Guarded Suspension yozuvi, patterns 4.12 da. Yuqoridagi uch tafsilot shu sababli asosan mavjud kodni o'qish va review uchun kerak: predikatsiz kutish, tashqariga ochiq condition queue va hujjatsiz protokol bilan vorislik, uchalasi ham nosozlikning odatiy manbasi.

Manba: Brian Goetz va boshqalar, *Java Concurrency in Practice*, Addison-Wesley, 2006, 14.2.1-bo'lim (183-bet), 14.2.2-bo'lim (184-bet), 14.2.3-bo'lim (185-bet), 14.2.6-14.2.7-bo'lim (187-bet) va 14.2.8-bo'lim (187-188-bet).

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

Uchinchi natija taqiq shaklida va u ko'pincha butunlay boshqa sababdan berilgan maslahat bilan aralashtiriladi. `Thread.sleep` va `Thread.yield` da **hech qanday sinxronlash semantikasi yo'q**: kompilyator bu chaqiruvlardan oldin registrda keshlangan yozuvlarni umumiy xotiraga chiqarishga majbur emas, chaqiruvdan keyin esa registrdagi qiymatlarni qayta o'qishga majbur emas (*The Java Language Specification, Java SE 25*, 17.3, 780-bet). Spetsifikatsiyaning o'z misoli qisqa va u korpusda ko'p uchraydigan shaklga tegadi:

```java
// BUZUQ: done volatile emas, shuning uchun sikl hech qachon tugamasligi mumkin
private boolean done;

void awaitDone() throws InterruptedException {
    while (!this.done) {
        Thread.sleep(1000);     // happens-before bermaydi
    }
}
```

Kompilyator `this.done` ni bir marta o'qib keshlangan qiymatni har iteratsiyada qayta ishlatishi mumkin, va boshqa thread qiymatni o'zgartirsa ham sikl tugamaydi. Buni [testda `Thread.sleep` ishlatmaslik](../sonarqube/30-xato-katalogi-test-kodidagi-xatolar.md#305-threadsleep-bilan-kutish-va-uni-almashtirish) maslahati bilan adashtirmaslik kerak: u beqarorlik va test tezligi haqida, bu esa **ko'rinuvchanlik** haqida va u testda emas, prodda buziladi, ko'pincha faqat `-server` rejimida yoki JIT kodni qayta kompilyatsiya qilgandan keyin. Tuzatish `sleep` ni olib tashlash emas: bayroq [`volatile`](#116-volatile-nimani-kafolatlaydi-va-nimani-kafolatlamaydi) qilinadi yoki `AtomicBoolean` ga o'tkaziladi, undan ham to'g'risi bunday kutish sikli o'rniga `CountDownLatch`, `BlockingQueue.poll(timeout)` yoki `Future.get(timeout)` olinadi. `Thread.yield` ham shu sababdan to'g'rilik vositasi bo'lolmaydi.

Manba: Brian Goetz va boshqalar, *Java Concurrency in Practice*, Addison-Wesley, 2006, 16.1.1-16.1.2-bo'lim (207-208-bet), 16.1.4-bo'lim (210-211-bet) va 16.3-bo'lim (214-215-bet); *The Java Language Specification, Java SE 25 Edition*, 17.3 (780-bet).

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

Shu hisobning eng ko'p uchraydigan amaliy ko'rinishi log yozishda chiqadi. Log operatsiyasining xizmat vaqti I/O oqimi sinflaridagi hisobni va I/O bloklanib qolgan vaqtni o'z ichiga oladi: OS bloklangan threadni I/O tugaguncha, ehtimol bir oz ko'proq, rejadan chiqaradi; I/O tugaganda boshqa threadlar faol bo'lib o'z kvantini tugatishga haqli bo'ladi va rejalashtirish navbatida sizdan oldin turganlar ham bo'lishi mumkin. Bir nechta thread bir vaqtda log yozsa natija bir xil: chiqish oqimi qulfi uchun raqobat paydo bo'ladi va thread qulfni kutib switch qilinadi. Ya'ni inline log yozish I/O va qulflashni birga keltiradi, bu esa kontekst almashinuvini va xizmat vaqtini oshiradi (Goetz, 11.6, 151-bet).

Uzun xizmat vaqtining ikkinchi natijasi muhimroq: u qulf raqobatini oshiradi. Qulf qancha uzoq ushlab turilsa, unga raqobat tushish ehtimoli shuncha yuqori; thread qulfni ushlab turib I/O ni kutsa, boshqa threadning shu qulfni so'rash ehtimoli oshadi, raqobatli qulf olish esa yana kontekst almashinuvi degani. Shuning uchun ko'proq kontekst almashinuviga undaydigan kod uslubi umumiy throughput ni tushiradi. I/O ni so'rov threadidan chiqarish o'rtacha xizmat vaqtini qisqartiradi: `log` chaqiruvchi threadlar chiqish oqimi qulfini yoki I/O ni kutmaydi, ular xabarni navbatga qo'yib ishiga qaytadi, va butun log I/O sini bitta threadga ko'chirish chiqish oqimi uchun raqobatni umuman yo'q qiladi (11.6, 151-bet).

Lekin kitob narxini ham yozadi va qaror uchun hal qiluvchisi shu: I/O ni boshqa threadga ko'chirish bir qancha dizayn savolini ochadi. Interrupt: log operatsiyasida bloklangan thread interrupt qilinsa nima bo'ladi. Xizmat kafolati: muvaffaqiyatli navbatga qo'yilgan xabar servis to'xtashidan oldin yozilishi kafolatlanadimi. To'yinish siyosati: ishlab chiqaruvchilar log threadi ko'tara oladiganidan tez yozsa nima bo'ladi. Servis hayot sikli: log threadi qanday to'xtatiladi va uning holati ishlab chiqaruvchilarga qanday aytiladi (11.6, 151-bet). Amalda bu to'rt savol kutubxona darajasida yopilgan: Logback ning `AsyncAppender` va Log4j2 ning asinxron logger i ularning har biriga sozlama beradi (`queueSize`, `discardingThreshold`, `neverBlock`), shuning uchun arxitektorning qarori "asinxron qilamizmi" emas, "navbat to'lganda xabarni tashlaymizmi yoki so'rovni sekinlashtiramizmi" degan shaklga keladi. Oxirgi savolning javobi esa [JVM to'xtash semantikasiga](31-deployment-haqiqati-konteyner-cgroup-jvm-va.md#3113-jvm-ning-ozi-qanday-toxtaydi-daemon-thread-shutdown-hook-va-halt) bog'lanadi: navbatda qolgan xabarlar faqat log threadi daemon bo'lmasa va to'xtatish tartibi unga vaqt bersa yoziladi.

Manba: Brian Goetz va boshqalar, *Java Concurrency in Practice*, Addison-Wesley, 2006, 11.3-bo'lim (142-bet), 11.3.1-bo'lim (142-143-bet), 11.3.2-bo'lim (143-144-bet) va 11.6-bo'lim (151-bet).

## 11.23 Vazifani `Future` orqali bekor qilish: vaqt chegarasi, `shutdownNow` chegarasi va `newTaskFor`

[Bekor qilish siyosati](#1114-bekor-qilish-interrupt-siyosati-va-thread-starvation-deadlock) kim bekor qilishni so'raydi va vazifa qanday javob berishini belgilaydi. Bu bo'lim mexanikaga tegishli: bekor qilish amalda qaysi chaqiruv bilan yuboriladi va to'xtatishdan keyin nima qolganini qanday bilib olinadi.

Vaqt budjeti bilan ishlaydigan vazifa uchun shakl bitta. Vazifa executor ga yuboriladi, natija `Future.get(timeout, unit)` bilan kutiladi, va `finally` da `future.cancel(true)` chaqiriladi. `finally` da shartsiz chaqirish xavfsiz, chunki allaqachon tugagan vazifani bekor qilish hech qanday ta'sir bermaydi (Goetz, 6.3.7, 83-bet). Qoida kitobda qisqa yozilgan: `Future.get` `InterruptedException` yoki `TimeoutException` bilan tugasa va natija endi kerak bo'lmasa, vazifa `Future.cancel` bilan bekor qilinadi (7.1.5, 92-bet).

```java
// Reklama bloki 300 ms ichida kelmasa, sahifa usiz chiqadi
Optional<Banner> fetchBanner(long userId) {
    Future<Banner> task = bannerExecutor.submit(() -> bannerClient.fetch(userId));
    try {
        return Optional.of(task.get(300, TimeUnit.MILLISECONDS));
    } catch (TimeoutException e) {
        return Optional.empty();                  // degradatsiya, xato emas
    } catch (ExecutionException e) {
        log.warn("banner servisi xato qaytardi", e.getCause());
        return Optional.empty();
    } catch (InterruptedException e) {
        Thread.currentThread().interrupt();       // holatni yo'qotmaslik
        return Optional.empty();
    } finally {
        task.cancel(true);                        // tugagan bo'lsa ta'siri yo'q
    }
}
```

`cancel(true)` ning qaytgan qiymati nimani bildirishini aniq bilish kerak: u faqat interrupt ni yetkazib berish imkoni bo'lganini aytadi, vazifa uni sezib ish to'xtatganini aytmaydi (7.1.5, 91-bet). Ikkinchi qoida undan ham muhim: pool threadini **o'zingiz interrupt qilmaysiz**. Interrupt yetib borgan paytda o'sha threadda qaysi vazifa ishlayotganini bilmaysiz, shuning uchun bekor qilish faqat vazifaning o'z `Future` i orqali yuboriladi. Standart `Executor` realizatsiyalari yaratgan threadlar vazifani interrupt bilan bekor qilishga ruxsat beradigan siyosatga ega, shuning uchun `mayInterruptIfRunning` ni `true` qo'yish aynan shu yo'lda xavfsiz (7.1.5, 91-bet).

To'xtatilgan pool dan keyin nima qolganini aniqlash alohida masala. `shutdownNow` faqat **yuborilgan lekin boshlanmagan** vazifalar ro'yxatini qaytaradi, boshlangan va tugamaganlarini bilishning umumiy yo'li yo'q: to'xtatish paytidagi vazifalar holatini bilish uchun vazifaning o'zi checkpoint yozib borishi kerak (7.2.5, 98-bet). Yana bir nozik joy: qaytarilgan `Runnable` lar yuborilgan obyektlarning o'zi bo'lishi shart emas, ular o'ralgan nusxa bo'lishi mumkin, demak ro'yxatni identity bo'yicha solishtirib bo'lmaydi. Kitobning yechimi tracking executor: `ExecutorService` ni o'rab, `execute` va `submit` ni asboblab, to'xtatishdan keyin bekor qilingan vazifalarni eslab qoladigan sinf. U faqat bitta shart bajarilganda ishlaydi: vazifa qaytganda threadning interrupted holatini saqlab qolishi kerak, va to'g'ri yozilgan vazifa buni baribir qiladi (7.2.5, 98-99-bet).

| Savol | Javob beradigan vosita |
|---|---|
| Vazifa boshlanmadi, kim qoldi | `shutdownNow()` qaytargan ro'yxat |
| Vazifa boshlandi lekin tugamadi | tracking executor yoki vazifaning o'z checkpoint i |
| Vazifa qayerga yetdi | faqat vazifaning o'zi yozgan progress holati |
| Interrupt yetkazildimi | `cancel(true)` ning qaytgan qiymati |
| Vazifa interrupt ni sezdimi | hech qaysi API, faqat vazifaning o'z logi |

Oxirgi vosita kam kerak bo'ladi, lekin boshqa yo'li yo'q holat uchun: interrupt ga javob bermaydigan blokirovka. Sinxron socket I/O da `InputStream.read` interrupt ni sezmaydi, uni to'xtatishning yo'li socket ni yopish. Buni bekor qilish shartnomasiga ulash uchun `ThreadPoolExecutor.newTaskFor` override qilinadi: u yuborilgan vazifa uchun `Future` yasovchi fabrika metodi, `RunnableFuture` qaytaradi, va o'z realizatsiyasida `Future.cancel` interrupt dan tashqari socket ni ham yopadi (Goetz, 6.3.2, 80-bet va 7.1.7, 92-93-bet). Zamonaviy kodda bundan oldin tekshiriladigan ikki arzon yo'l bor: HTTP klientga o'z `requestTimeout` ini berish va `InterruptibleChannel` ishlatish, chunki ularda interrupt kanalni yopib `ClosedByInterruptException` beradi.

Manba: Brian Goetz va boshqalar, *Java Concurrency in Practice*, Addison-Wesley, 2006, 6.3.2-bo'lim (80-bet), 6.3.7-bo'lim (82-83-bet), 7.1.5-7.1.7-bo'lim (91-93-bet) va 7.2.5-bo'lim (98-99-bet).

## 11.24 Deadlockdan tiklanish: `tryLock(timeout)`, qulfni qo'yib yuborish va qayta urinish

[Deadlock bo'limi](#1110-deadlock-livelock-va-ochlik-starvation-sabab-va-oldini-olish) to'rt shartni sanaydi va ularning eng amaliyini, aylana kutishni, qulf tartibi bilan buzadi. Lekin qulf tartibini butun dastur bo'yicha kafolatlash har doim imkonli emas: qulf metod chaqiruvlari ichida, kutubxona ichida yoki boshqa vendor kodida olinishi mumkin. Shuning uchun oldini olishdan tashqari **tiklanish** rejasi ham kerak.

Tiklanish vositasi vaqt chegarasi bilan qulf olish: `ReentrantLock.tryLock(timeout, unit)`. Intrinsic qulf qulfni olmaguncha abadiy kutadi, ochiq `Lock` esa muhlat tugagandan keyin `false` qaytaradi va boshqaruv sizga qaytadi. Muhlat kutilgan olish vaqtidan **ancha katta** qilib tanlanadi, shunda u normal sekinlikni emas, faqat kutilmagan holatni ushlaydi (Goetz, 10.2.1, 134-bet).

Muhlat tugaganda sabab noma'lum qoladi va bu ongli qabul qilinadigan narsa: deadlock bo'lishi mumkin, thread qulfni ushlab turib cheksiz siklga tushgan bo'lishi mumkin, yoki shunchaki kutilganidan ancha sekin ish bo'lishi mumkin. Shunga qaramay bitta imkoniyat paydo bo'ladi: urinish muvaffaqiyatsiz bo'lganini **yozib qoldirish**, nima qilmoqchi bo'lganingiz haqidagi foydali ma'lumotni log ga tushirish va hisobni butun processni o'ldirishdan ko'ra chiroyliroq qaytadan boshlash (10.2.1, 134-bet).

Tiklanish tartibi shundan chiqadi: muhlat tugasa log yoz, **olgan qulflarni qo'yib yubor**, biroz kutib qayta urin. Bu usul qulf izchil ishlatilmagan dasturda ham samarali, lekin uning qat'iy sharti bor: faqat ikki qulf **birga** olinganda ishlaydi. Qulflar metod chaqiruvlarining ichma-ich joylashuvi tufayli yig'ilgan bo'lsa, tashqi qulfni ushlab turganingizni bilsangiz ham uni shunchaki qo'yib yuborib bo'lmaydi (10.2.1, 134-bet).

```java
// Ikki hisob o'rtasida o'tkazma: qulflar birga olinadi, demak tiklanish mumkin
boolean transfer(Account from, Account to, BigDecimal amount, Duration budget)
        throws InterruptedException {
    long deadline = System.nanoTime() + budget.toNanos();
    while (System.nanoTime() < deadline) {
        if (from.lock().tryLock(200, TimeUnit.MILLISECONDS)) {
            try {
                if (to.lock().tryLock(200, TimeUnit.MILLISECONDS)) {
                    try {
                        from.debit(amount);
                        to.credit(amount);
                        return true;
                    } finally { to.lock().unlock(); }
                }
            } finally { from.lock().unlock(); }   // ikkinchisi olinmasa birinchisi qo'yiladi
        }
        log.warn("qulf olinmadi, qayta urinaman from={} to={}", from.id(), to.id());
        // jitter: ikki thread bir xil ritmda qaytmasin, aks holda livelock
        Thread.sleep(20 + ThreadLocalRandom.current().nextLong(80));
    }
    return false;                                 // chaqiruvchi degradatsiya qarorini qabul qiladi
}
```

Jitter tasodifiy emas: usulning o'z narxi bor va u [livelock](#1110-deadlock-livelock-va-ochlik-starvation-sabab-va-oldini-olish) va ochlik shaklida keladi. Clean Code shu usulni "lock va wait shartini buzish" deb nomlaydi va ikki xavfini ochiq sanaydi: ochlik, ya'ni bitta thread kerakli resurslar to'plamini hech qachon yig'a olmasligi, va livelock, ya'ni bir nechta thread bir vaqtda bitta resursni olib keyin qo'yib yuborib takrorlanishi. Birinchisi CPU ni past ishlatishga, ikkinchisi yuqori lekin foydasiz ishlatishga olib keladi. Kitobning hukmi esa amaliy: bu strategiya samarasiz ko'rinsa ham hech narsadan yaxshiroq, va boshqa hamma yo'l tugaganda deyarli har doim amalga oshirilishi mumkin (Martin, *Clean Code*, A ilovasi, 338-bet).

O'zaro istisno shartini buzish esa alohida ko'rib chiqiladi, chunki u arzonroq. Uch yo'li bor: bir vaqtda foydalanishga ruxsat beradigan resursni tanlash (masalan `AtomicInteger` bilan hisoblash), resurslar sonini raqobatdagi thread soniga yetkazish yoki oshirish, va hamma resurs bo'shligini tekshirib keyin olish. Kitobning o'zi chegarasini ham aytadi: ko'p resurs soni chekli va bir vaqtda foydalanishga ruxsat bermaydi, bundan tashqari ikkinchi resursning qaysi biri bo'lishi ko'pincha birinchisi bilan ishlash natijasidan kelib chiqadi, shuning uchun bu yo'l kamdan-kam qo'llanadi (Martin, *Clean Code*, A ilovasi, 337-bet). Shunga qaramay birinchi yo'l amalda juda ko'p ishlaydi: hisoblagich va bayroq uchun qulf o'rniga atomic sinf olinsa, deadlock sharti umuman tug'ilmaydi.

Qaysi yo'l qachon tanlanadi:

| Shart | Buzish yo'li | Amalda |
|---|---|---|
| Aylana kutish | global qulf tartibi | birinchi tanlov, [deadlock bo'limida](#1110-deadlock-livelock-va-ochlik-starvation-sabab-va-oldini-olish) |
| O'zaro istisno | atomic sinf, resurs sonini oshirish | hisoblagich va bayroqda arzon, umumiy holatda kam ishlaydi |
| Ushlab turib kutish | `tryLock(timeout)`, qo'yib yuborish, jitter bilan qayta urinish | tartibni kafolatlab bo'lmaganda; qulflar birga olinishi shart |
| Tortib olish imkonsizligi | egadan qo'yib yuborishni so'rash protokoli | so'rovlarni boshqarish murakkab, ilova kodida kam haqli |

Qulf va `tryLock` ning umumiy taqqoslovi [qulf mexanizmlari bo'limida](#114-synchronized-reentrantlock-readwritelock-va-stampedlock-farqi), hodisadan keyin deadlock ni thread dump dan topish esa [thread dump o'qish bo'limida](#1111-konkurentlik-xatolarini-topish-thread-dump-oqish).

Manba: Brian Goetz va boshqalar, *Java Concurrency in Practice*, Addison-Wesley, 2006, 10.2.1-bo'lim (134-bet); Robert C. Martin, *Clean Code*, Prentice Hall, 2009, A ilovasi (337-338-betlar).

## 11.25 Yashirin iteratsiya: `toString`, `hashCode` va `containsAll` ham kolleksiyani aylanadi

Sinxronlangan kolleksiyani iteratsiya davomida qulflash kerakligi ma'lum qoida. Amalda buziladigan joy boshqa: iteratsiya kodda ko'rinmaydi. JCiP buni yashirin iterator (hidden iterator) deb nomlaydi va eng ko'p uchraydigan ko'rinishini beradi: kolleksiyani satrga qo'shish. Kompilyator satr konkatenatsiyasini `StringBuilder.append(Object)` ga aylantiradi, u kolleksiyaning `toString` ini chaqiradi, standart kolleksiyalarning `toString` i esa kolleksiyani aylanib har elementning `toString` ini chaqiradi. Natijada log yoki debug xabari tayyorlanayotganda `ConcurrentModificationException` chiqadi (Goetz, 5.1.3, 53-bet).

Iteratsiya bilvosita chaqiriladigan joylar bundan ko'p. Kolleksiya boshqa kolleksiyaning elementi yoki kaliti bo'lsa, uning `hashCode` va `equals` metodlari chaqiriladi va ular ham aylanadi. `containsAll`, `removeAll` va `retainAll` metodlari, shuningdek kolleksiyani argument qilib oladigan konstruktorlar ham iteratsiya qiladi. Bu bilvosita ishlatishlarning har biri `ConcurrentModificationException` berishi mumkin (5.1.3, 54-bet).

```java
// yomon: log xabari himoyalanmagan holda iteratsiya qiladi
@GuardedBy("this") private final Set<Long> activeOrders = new HashSet<>();

public synchronized void add(long orderId) { activeOrders.add(orderId); }

public void dump() {
    log.debug("faol buyurtmalar: {}", activeOrders);  // toString -> iteratsiya, qulf yo'q
}
```

Kitobning asosiy xulosasi esa aniq bitta xatoni emas, butun xato sinfini yopadi: holat bilan uni himoyalaydigan sinxronlash orasidagi masofa qancha katta bo'lsa, kimdir shu holatga murojaat qilganda to'g'ri sinxronlashni ishlatishni unutishi shunchalik ehtimolli. Obyekt holatini inkapsulyatsiya qilish invariantni saqlashni osonlashtirgani kabi, obyektning **sinxronlashini** inkapsulyatsiya qilish sinxronlash siyosatini majburlashni osonlashtiradi (5.1.3, 53-bet). Yuqoridagi sinf `HashSet` ni `synchronizedSet` bilan o'rab olsa, bu xato turi umuman tug'ilmaydi.

```java
// yaxshi: sinxronlash kolleksiyaning o'zida, log yo'li xatarsiz
private final Set<Long> activeOrders = ConcurrentHashMap.newKeySet();

public void add(long orderId) { activeOrders.add(orderId); }

public void dump() {
    log.debug("faol buyurtmalar: {}", activeOrders);  // weakly consistent iterator
}
```

Zamonaviy tanlov tartibi shunday. Birinchi variant konkurent kolleksiya: uning iteratori weakly consistent, ya'ni `ConcurrentModificationException` otmaydi va iteratsiya davomida qulf ushlamaydi, buning evaziga u snapshot emas (batafsil [thread-safe to'plamlar bo'limida](#117-thread-safe-toplamlar-concurrenthashmap-copyonwritearraylist-va-ularning-narxi)). Ikkinchi variant nusxa olib nusxani aylanish: nusxa threadga qamalgani uchun xavfsiz, lekin nusxa olishning o'z narxi bor va u kolleksiya hajmiga, har element uchun qilinadigan ish hajmiga va iteratsiyaning boshqa amallarga nisbatan chastotasiga bog'liq (5.1.2, 53-bet). Uchinchi variant iteratsiya davomida qulflash: u eng oxirgi, chunki qulf ushlab turib `doSomething` chaqirish [begona kod](#1112-thread-safety-darajasini-hujjatlash-va-ortiqcha-sinxronlashdan-qochish) muammosi, va uzoq ushlangan qulf raqobatni oshirib masshtablanishni tushiradi.

Review paytida qidiriladigan naqsh ham qisqa: himoyalangan kolleksiya nomining log chaqiruvi, satr konkatenatsiyasi, `assert`, istisno xabari yoki `Objects.hash` argumenti ichida uchrashi. Ulardan hech biri qulf olmaydi.

Manba: Brian Goetz va boshqalar, *Java Concurrency in Practice*, Addison-Wesley, 2006, 5.1.2-bo'lim (53-bet) va 5.1.3-bo'lim (53-54-bet).

## 11.26 Amalda qo'llash

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

- Joshua Bloch, *Effective Java* 3rd, Item 78 (311, 314 va 315-betlar) - umumiy o'zgaradigan holatga kirishni sinxronlash; `long` va `double` dan boshqa o'zgaruvchini o'qish va yozish atomar bo'lsa ham ko'rinuvchanlik kafolatlanmasligi va "atomar ma'lumotda sinxronlashni tashla" maslahatining xatosi; faqat yozish metodini sinxronlash yetarli emasligi; framework va kutubxonaning hisobga olinmagan thread kiritishi
- Joshua Bloch, *Effective Java* 3rd, Item 79 (322-bet) - ortiqcha sinxronlashdan qochish, qulf ichida begona kod chaqirmaslik; o'zgaradigan sinfda sinxronlashni mijozga qoldirish yoki ichida qilish tanlovi va `java.util` bilan `java.util.concurrent` ning qarama-qarshi tanlovi
- Joshua Bloch, *Effective Java* 3rd, Item 80 va 81 (324 va 329-betlar) - thread o'rniga executor va vazifa, ish birligi bilan bajarish mexanizmining ajratilishi, `ForkJoinPool` dagi vazifa o'g'irlash va parallel oqimning shu pool ustida qurilishi; `wait`/`notify` o'rniga konkurentlik vositalari va `notifyAll` ning konservativ to'g'ri tanlov ekani, `notify` ni optimallashtirish sifatida tanlash sharti
- Joshua Bloch, *Effective Java* 3rd, Item 82 (331-bet) - thread safety darajasini hujjatlash; qaytish turi ko'rsatmaganda statik fabrikaning qaytargan obyekt xossasini hujjatlashi va `enum` uchun bunday talab yo'qligi; oshkor qulfning ikki narxi (ichki konkurentlik nazorati bilan sig'ishmasligi va xizmatni rad etish hujumi) hamda `private` qulf obyekti yechimi
- Joshua Bloch, *Effective Java* 3rd, Item 84 (337-bet) - thread rejalashtiruvchisiga tayanmaslik; prioritetning Java ning eng kam ko'chma xususiyatlaridan biri ekani va jiddiy tiriklik muammosini prioritet bilan hal qilishga urinishning noto'g'riligi
- Joshua Bloch, *Effective Java* 3rd, Item 87 (351-bet) - obyekt holatini to'liq o'qiydigan metodga qo'yilgan sinxronlash seriyalashga ham qo'yilishi va `writeObject` ning umumiy qulf tartibiga rioya qilishi, aks holda resurs tartibi deadlocki
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
- Brian Goetz va boshqalar, *Java Concurrency in Practice*, Addison-Wesley, 2006, 4.5.1-bo'lim (50-bet) - hujjat thread safety haqida jim bo'lganda spetsifikatsiyani realizatsiya qiluvchi nuqtai nazaridan o'qish; `ServletContext`, `HttpSession` va `DataSource` ning thread-safe deb hisoblanishi; `setAttribute` bilan qo'yilgan atributlar ilovaniki va o'zi thread-safe yoki amalda o'zgarmas bo'lishi sharti; `Connection` ning pool ga qaytarilmaguncha bo'lishilmasligi
- Brian Goetz va boshqalar, *Java Concurrency in Practice*, Addison-Wesley, 2006, 5.1.2-5.1.3-bo'lim (53-54-bet) - iteratsiya davomida qulflashning narxi va nusxa olish alternativasi; yashirin iterator: satr konkatenatsiyasining `toString` ni chaqirishi, `hashCode` / `equals` / `containsAll` / `removeAll` / `retainAll` va kolleksiya oluvchi konstruktorlarning iteratsiya qilishi; holat bilan sinxronlash orasidagi masofa qoidasi va sinxronlashni inkapsulyatsiya qilish
- Brian Goetz va boshqalar, *Java Concurrency in Practice*, Addison-Wesley, 2006, 6.1-bo'lim (72-bet) - vazifa chegarasini tanlash: mustaqillik va sig'imning kichik ulushi mezoni, server ilovasida bitta klient so'rovining tabiiy chegara bo'lishi, yuk ostida chiroyli degradatsiya talabi
- Brian Goetz va boshqalar, *Java Concurrency in Practice*, Addison-Wesley, 2006, 6.2.5-bo'lim (77-78-bet) - `Timer` ning `ScheduledThreadPoolExecutor` bilan almashtirilishi: bitta thread va vaqt aniqligining buzilishi (10 ms vazifa yonida 40 ms vazifa), `TimerTask` dagi tekshirilmaydigan istisnoning timer threadini o'ldirishi va `IllegalStateException`, mutlaq va nisbiy vaqt farqi
- Brian Goetz va boshqalar, *Java Concurrency in Practice*, Addison-Wesley, 2006, 6.3.2-bo'lim (80-bet), 6.3.4-6.3.7-bo'lim (80-83-bet) - `newTaskFor` ning `Future` yasovchi fabrika ekani; heterogen vazifalarni parallellashtirish chegarasi (o'n barobar farqda 9 foiz tezlanish, ikki threadda ko'pi bilan ikki barobar) va foyda ko'p sonli bir turdagi vazifadan kelishi; `CompletionService` ning `Executor` plus `BlockingQueue` ekani, `QueueingFuture` mexanikasi, umumiy `Executor` ustida xususiy `CompletionService`; vaqt budjeti bilan `Future.get(timeout)` va tugagan vazifani bekor qilishning ta'sirsizligi
- Brian Goetz va boshqalar, *Java Concurrency in Practice*, Addison-Wesley, 2006, 7.1.5-7.1.7-bo'lim (91-93-bet) - `cancel(true)` faqat interrupt yetkazilganini bildirishi, pool threadini bevosita interrupt qilmaslik va faqat `Future` orqali bekor qilish, standart `Executor` threadlarining interrupt siyosati; interrupt ga javob bermaydigan blokirovka va `newTaskFor` bilan nostandart bekor qilishni inkapsulyatsiya qilish
- Brian Goetz va boshqalar, *Java Concurrency in Practice*, Addison-Wesley, 2006, 7.2.5-bo'lim (98-99-bet) - `shutdownNow` faqat boshlanmagan vazifalarni qaytarishi, qaytarilgan `Runnable` larning o'ralgan nusxa bo'lishi mumkinligi, boshlangan va tugamagan vazifalarni bilishning umumiy yo'li yo'qligi, tracking executor va vazifaning interrupted holatini saqlash sharti
- Brian Goetz va boshqalar, *Java Concurrency in Practice*, Addison-Wesley, 2006, 10.2.1-bo'lim (134-bet) - vaqt chegarasi bilan qulf olish: muhlat kutilgan vaqtdan ancha katta bo'lishi, muvaffaqiyatsiz urinishning sababi noma'lum qolishi, log yozib hisobni chiroyliroq qaytadan boshlash, qulflarni qo'yib yuborib kutib qayta urinish va bu usul faqat qulflar birga olinganda ishlashi
- Brian Goetz va boshqalar, *Java Concurrency in Practice*, Addison-Wesley, 2006, 11.6-bo'lim (151-bet) - inline log yozishning I/O va chiqish oqimi qulfi orqali kontekst almashinuvini va xizmat vaqtini oshirishi, uzun xizmat vaqtining qulf raqobatini oshirishi, I/O ni alohida threadga ko'chirishning foydasi va to'rt dizayn savoli (interrupt, xizmat kafolati, to'yinish siyosati, servis hayot sikli)
- Brian Goetz va boshqalar, *Java Concurrency in Practice*, Addison-Wesley, 2006, 14.2.3-bo'lim (185-bet) va 14.2.6-14.2.7-bo'lim (187-bet) - yo'qolgan signalning ta'rifi va xabarning yopishqoq emasligi; condition queue ni sinf ierarxiyasidan tashqarida ko'rinmas qilish, uniform waiters shartini majburlab bo'lmasligi va o'g'irlangan signal; holatga bog'liq sinfning protokolni to'liq hujjatlashi yoki vorislikni to'sishi, ikki sinf kutuvchi paydo bo'lganda `notifyAll` bilan tuzatish
- *The Java Language Specification, Java SE 25 Edition* (Gosling, Joy, Steele, Bracha, Buckley, Smith, Bierman), 17.3 (780-bet) - `Thread.sleep` va `Thread.yield` da sinxronlash semantikasi yo'qligi: kompilyator registrdagi yozuvni chiqarishga va chaqiruvdan keyin qayta o'qishga majbur emasligi, `volatile` bo'lmagan bayroqni `sleep` siklida kutishning buzuqligi
- Robert C. Martin, *Clean Code*, Prentice Hall, 2009, A ilovasi (337-338-betlar) - deadlockning to'rt shartidan o'zaro istisnoni buzish (bir vaqtda foydalanishga ruxsat beradigan resurs, resurs sonini raqobatdagi thread soniga yetkazish, hammasi bo'shligini tekshirib olish) va uning chegarasi; lock va wait shartini buzish: hamma resursni qo'yib yuborib qaytadan boshlash, ochlik va livelock xavfi, va bu strategiyaning hech narsadan yaxshiroq ekani
- Herbert Schildt, *Java The Complete Reference*, 12-nashr, McGraw-Hill, 2022, 11-bob (249-bet), 13-bob (345-bet) va 21-bob (672-673-betlar) - thread prioriteti mutlaq qiymat sifatida ma'nosiz ekani, kontekst almashinuvining ikki qoidasi, teng prioritetli threadlar uchun portativlik ogohlantirishi; value-based sinflarning qoidalari va ular ustida sinxronlash qilmaslik; `Timer` va `TimerTask` ning ishlashi va non-daemon `Timer` ni `cancel()` qilmaslik dasturni osilib qoldirishi
- George Fairbanks, *Just Enough Software Architecture: A Risk-Driven Approach*, Marshall & Brainerd, 2010, 2.7 va 10.8-bo'limlar - arxitekturaga yo'naltirilgan dizayn lokal tuzatish emas, universal qo'llanadigan arxitektura yechimini izlashi va uning to'rt misoli (qulf olish tartibi konvensiyasi, modul qamroviga qarab xotirani bo'shatish standarti, kesh izchilligi uchun kirishni cheklash, davomiylik kafolati bor message queue); email ishlovchi tizimda `Filter` superklassi bilan konkurentlikni bir joyga ko'tarish (Template method, har filter o'z thread ida, inkremental ishlash) va thread-safe `Pipe` orqali aloqa; inkremental ishlash hamda faqat pipe orqali gaplashish cheklovlarini kodda majburlash qiyinligi va ularni izohda yozish; Java ning bitta superklass cheklovi va interfeys ishlatilganda konkurentlikni hoisting qilish imkonining yo'qolishi
- Jeanne Boyarsky, Scott Selikoff, *OCP Oracle Certified Professional Java SE 17 Developer Practice Tests*, Wiley, Appendix, 8-bobning javoblari, 36-savol - umumiy `static` maydonni instans `synchronized` metodi (`this` monitori) va static `synchronized` metodi (`Class` obyekti monitori) himoya qilsa, ikkisi bir-birini chiqarmasligi; `+=` va `-=` ning atomik emasligi va o'zgarishning yo'qolishi; natija oldindan aytilmasligi va ikki metod bir xil obyektda sinxronlanganda maydonning himoyalanishi
- Brian Goetz va boshqalar, *Java Concurrency in Practice*, Addison-Wesley, 2006, 1.1-bo'lim (8-9-betlar) - har bir Java ilovasining thread ishlatishi (JVM ning GC va finalization threadlari, `main`, `Timer`, servlet konteyneri, RMI, AWT va Swing); thread xavfsizligining yuqumliligi va talabning umumiy holatga tegadigan hamma kod yo'li bo'ylab tarqalishi
- Brian Goetz va boshqalar, *Java Concurrency in Practice*, Addison-Wesley, 2006, 2.4-bo'lim (19-20-betlar) - sinxronlash o'zgaruvchiga murojaat qilinadigan hamma joyda va bir xil qulf bilan kerakligi; har bir o'zgaradigan umumiy o'zgaruvchiga aynan bitta qulf biriktirish va uni hujjatda nomlash; bir nechta o'zgaruvchini qamragan har bir invariant uchun qatnashuvchi hamma o'zgaruvchining bitta qulf ostida bo'lishi va bitta atomar amalda o'qilishi yoki yangilanishi
- Brian Goetz va boshqalar, *Java Concurrency in Practice*, Addison-Wesley, 2006, 8.3.1-bo'lim (107-bet) - `corePoolSize` nolga qo'yilganda sig'imi bor navbatda vazifaning navbat to'lguncha bajarilmasligi va `allowCoreThreadTimeOut` ning Java 6 dan beri hamma pool threadini vaqt chegarasiga qo'yishi
- Brian Goetz va boshqalar, *Java Concurrency in Practice*, Addison-Wesley, 2006, 8.4-bo'lim (111-bet) - `beforeExecute`, `afterExecute` va `terminated` hooklarining vazifani bajaradigan threadda chaqirilishi, `Error` bilan tugagan vazifada `afterExecute` chaqirilmasligi, `beforeExecute` dagi `RuntimeException` ning vazifani ham, `afterExecute` ni ham to'xtatishi
- Brian Goetz va boshqalar, *Java Concurrency in Practice*, Addison-Wesley, 2006, 11.4.6-bo'lim (149-bet) - CPU to'liq band bo'lmasligining to'rt sababi (yuk yetarli emas, I/O ga bog'liq, tashqi servisga bog'liq, qulf raqobati), nosimmetrik yuklanishning kichik thread to'plamini bildirishi, kam raqobatli qulfning thread dumpda kamdan-kam va ko'p raqobatlisining deyarli har dumpda ko'rinishi
- Brian Goetz va boshqalar, *Java Concurrency in Practice*, Addison-Wesley, 2006, 13.1.4-bo'lim (174-bet) - blok-strukturali bo'lmagan qulflash: bog'langan tuzilmada har node ga alohida qulf va keyingi node qulfini olgandan keyin oldingisini qo'yib yuborish (hand-over-hand locking yoki lock coupling)
- Brian Goetz va boshqalar, *Java Concurrency in Practice*, Addison-Wesley, 2006, 13.5-bo'lim (177-178-betlar) - `ReadWriteLock` implementatsiyasining besh tanlovi (qo'yib yuborish ustuvorligi, o'quvchi barging i va yozuvchi ochligi, reentrancy, pastga tushish, yuqoriga ko'tarilish); oshkor ko'tarilish amali bo'lmaganda ko'tarilishning deadlock ga moyilligi va ikki o'quvchining bir vaqtda ko'tarilishi misoli; `ReentrantReadWriteLock` da pastga tushishga ruxsat borligi va ko'tarilish urinishining deadlock bilan tugashi
- Brian Goetz va boshqalar, *Java Concurrency in Practice*, Addison-Wesley, 2006, 14.2.5-bo'lim (186-187-betlar) - qayta yopiladigan `ThreadGate` ning `isOpen` dan murakkabroq shart predikati: har yopilishda `generation` hisoblagichining oshirilishi va kutuvchining "hozir ochiq yoki men kelganimdan keyin ochilgan" shartini tekshirishi
- *The Java Language Specification, Java SE 25 Edition* (Gosling, Joy, Steele, Bracha, Buckley, Smith, Bierman), 17.4 (788-bet), 17.6 (801-bet) va 17.7 (802-bet) - ma'lumot poygasining massiv uzunligi, checked cast va virtual metod chaqiruviga bevosita ta'sir qilmasligi; word tearing taqiqi va `byte[]` ning qo'shni elementlarini sinxronlashsiz yangilash xavfsizligi; `volatile` bo'lmagan `long` va `double` ga yozishning ikki 32-bitli yozuvga bo'linishi mumkinligi, `volatile long` va `volatile double` hamda havolalarning doim atomar bo'lishi va 64-bitli umumiy qiymatni `volatile` qilish tavsiyasi
- *The Java Virtual Machine Specification, Java SE 25 Edition* (Lindholm, Yellin, Bracha, Buckley, Smith), 2.11.10 (39-bet) va 3.14 (70-71-betlar) - `synchronized` metodning `ACC_SYNCHRONIZED` flagi bilan belgilanishi, monitorning metod chaqirilganda olinishi va normal hamda noodatiy tugashda qo'yib yuborilishi; `synchronized` blokning `monitorenter` va `monitorexit` ga kompilyatsiya qilinishi va juftlikni kafolatlash uchun har qanday istisnoni tutadigan yashirin handler yaratilishi
- Jeanne Boyarsky, Scott Selikoff, *OCP Java SE 17 Study Guide*, Wiley, 13-bob (738-bet) - `scheduleAtFixedRate` ning oldingi vazifa tugashini kutmasligi, vazifa davrdan uzoq ishlaganda navbatning o'sishi va xotira tugashi
- Benjamin Evans, Martijn Verburg, *The Well-Grounded Java Developer*, Manning, 4.1.2-4.1.3-bo'lim (79-81-betlar) - Doug Lea katalogiga ko'ra konkurent dizaynning to'rt kuchi (xavfsizlik, tiriklik, unum, qayta ishlatiluvchanlik), tiriklikning "oxir-oqibat oldinga ketadi yoki yiqiladi" ta'rifi va vaqtincha hamda doimiy to'xtash farqi; kuchlarning bir-biriga qarshi turishi; xavfsizlik mexanizmlarining kuch tartibi (tashqi aloqani cheklash, determinatsiyalangan ichki tuzilma, mijoz siyosati, hujjatlash) va eng kuchlisini tanlash talabi
- [JEP 444: Virtual Threads](https://openjdk.org/jeps/444) - virtual threadning doim daemon bo'lishi va `setDaemon(boolean)` ning unga ta'sir qilmasligi
- ESLATMA: `RateCache` va `RateCacheFixed` misollari hamda `ReadWriteLock` ko'tarilishining xato va to'g'ri shakli korpusning qo'shimchasi: kitoblar qoidani beradi, Spring konteksti (`@Component`, kurs keshi) va bu kod shakllari shu korpusda yozilgan. `ThreadGate` esa kitobning 14.9-listingi asosida qisqartirilgan: `@GuardedBy` annotatsiyasi izohga aylantirilgan va metod nomlari qisqartirilgan, mexanika o'zgarmagan
- Paul Deitel va Harvey Deitel, *Java How to Program*, 10-nashr, Pearson, 23.2.7-bo'lim (962-963-betlar) - prioritetning yaratuvchi threaddan meros bo'lishi, prioritet bajarilish tartibini kafolatlamasligi, timeslicing va round-robin, rejalashtirishning platformaga bog'liqligi, `Thread` ni qo'lda boshqarish o'rniga `Executor` tavsiyasi


---

[&larr; 10. Garbage collection va xotira sozlash](10-garbage-collection-va-xotira-sozlash.md) · [Mundarija](README.md) · [12. Virtual threads, structured concurrency va scoped values &rarr;](12-virtual-threads-structured-concurrency-va.md)
