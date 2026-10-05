<!-- doc: architect | chapter: 14 | part: II. Java chuqur bilim -->

[Barcha hujjatlar](../../README.md) / [Arxitektor miyasi](README.md)

# 14. JVM profiling va diagnostika: JFR, async-profiler, heap dump (JVM Profiling and Diagnostics)

<details>
<summary>Bu bobdagi 12 bo'lim</summary>

- [14.1 Diagnostika tartibi: avval o'lchov, keyin faraz, keyin tuzatish](#141-diagnostika-tartibi-avval-olchov-keyin-faraz-keyin-tuzatish)
- [14.2 Thread dump olish va o'qish: `jstack`, bloklangan thread, lock egasi](#142-thread-dump-olish-va-oqish-jstack-bloklangan-thread-lock-egasi)
- [14.3 Heap dump olish (`jmap`, `-XX:+HeapDumpOnOutOfMemoryError`) va tahlil qilish](#143-heap-dump-olish-jmap--xxheapdumponoutofmemoryerror-va-tahlil-qilish)
- [14.4 Java Flight Recorder: yozuvni boshlash, sozlash profili, qancha ortiqcha yuk beradi](#144-java-flight-recorder-yozuvni-boshlash-sozlash-profili-qancha-ortiqcha-yuk-beradi)
- [14.5 JFR da nimaga qarash: allokatsiya, GC, lock contention, I/O kutish](#145-jfr-da-nimaga-qarash-allokatsiya-gc-lock-contention-io-kutish)
- [14.6 async-profiler va flame graph o'qish: CPU, allokatsiya, wall-clock rejimi](#146-async-profiler-va-flame-graph-oqish-cpu-allokatsiya-wall-clock-rejimi)
- [14.7 `jcmd` buyruqlari: eng foydali to'plam](#147-jcmd-buyruqlari-eng-foydali-toplam)
- [14.8 Mikro o'lchov tuzoqlari va JMH nega kerak](#148-mikro-olchov-tuzoqlari-va-jmh-nega-kerak)
- [14.9 Ishlab chiqarish muhitida profiling: xavfsizlik va ortiqcha yuk masalasi](#149-ishlab-chiqarish-muhitida-profiling-xavfsizlik-va-ortiqcha-yuk-masalasi)
- [14.10 Spring Boot Actuator orqali diagnostika endpointlari](#1410-spring-boot-actuator-orqali-diagnostika-endpointlari)
- [14.11 Tez-tez uchraydigan diagnoz: sekin so'rov, thread pool to'lishi, xotira sizishi](#1411-tez-tez-uchraydigan-diagnoz-sekin-sorov-thread-pool-tolishi-xotira-sizishi)
- [14.12 Amalda qo'llash](#1412-amalda-qollash)

</details>



Ishlab chiqarishda sekinlashgan to'lov servisi haqida xabar kelganda arxitektorning birinchi ishi kodga qarash emas. Birinchi ish JVM dan dalil olish: thread qayerda turgan, xotira qayerda yig'ilgan, vaqt qayerda yo'qolgan. JFR, async-profiler, thread dump va heap dump bu dalilni bir necha daqiqada beradi, lekin faqat ularni qanday o'qishni bilgan odamga. Bu bob shu asboblarning mexanikasi va ulardan qaror chiqarish tartibi haqida.

## 14.1 Diagnostika tartibi: avval o'lchov, keyin faraz, keyin tuzatish

Eng qimmat xato tartibni buzish: faraz qilib, darhol kodni o'zgartirish. Bunda siz tasodifan yaxshilangan yoki tasodifan yomonlashgan tizimni olasiz, lekin sabab haqida hech narsa bilmaysiz. To'g'ri tartib to'rt qadam: belgini raqamga aylantirish, resursni aniqlash, farazni tekshirish, keyin bitta o'zgarish kiritish.

Belgini raqamga aylantirish degani "sekin" so'zini "p99 latency 180 ms dan 2.4 s ga chiqdi, p50 esa 60 ms da qoldi" deb yozish. p50 o'zgarmagani muhim dalil: bu bir qism so'rov navbatda kutayotganini bildiradi. Navbat esa yoki thread pool, yoki connection pool, yoki GC pauza, yoki tashqi I/O.

Keyin resursni ajratish kerak. CPU to'lgan bo'lsa profiling kerak. CPU bo'sh, lekin latency baland bo'lsa, bu kutish, ya'ni wall-clock profiling yoki thread dump kerak. Xotira o'sib borsa heap dump kerak. Bitta asbob hamma holatga yaramaydi, shuning uchun resursni noto'g'ri aniqlash bir soatni yo'qotadi.

## 14.2 Thread dump olish va o'qish: `jstack`, bloklangan thread, lock egasi

Thread dump JVM ning bir lahzadagi fotosurati. U arzon: safepoint da olinadi va odatda bir necha o'n millisekund davom etadi. Shuning uchun latency muammosida birinchi olinadigan dalil aynan shu.

```bash
# PID ni topish (JVM processlar ro'yxati)
jcmd -l

# Thread dump: jstack yoki jcmd, natija bir xil
jstack -l 4211 > /var/tmp/td-1.txt
jcmd 4211 Thread.print -l > /var/tmp/td-2.txt

# 10 sekund oraliq bilan 3 ta dump olish (bitta surat yetarli emas)
for i in 1 2 3; do
  jcmd 4211 Thread.print -l > "/var/tmp/td-$i.txt"
  sleep 10
done

# Holatlar bo'yicha sanash: nechta thread RUNNABLE, nechta BLOCKED
grep -o 'java.lang.Thread.State: [A-Z_]*' /var/tmp/td-1.txt | sort | uniq -c

# JDK 21+ virtual thread larni ham ko'rsatadi, JSON formatda
jcmd 4211 Thread.dump_to_file -format=json /var/tmp/vthreads.json
```

Bitta dump hech narsa isbotlamaydi. Uch dumpda bir xil thread bir xil qatorda turgan bo'lsa, u qotib qolgan. O'qishda uch narsaga qaraladi: thread holati, stack ning yuqori qatori va lock satrlari. `BLOCKED (on object monitor)` qatoridan keyin `- waiting to lock <0x000000071a2b3c48>` bo'ladi, shu bir xil manzilni boshqa thread da `- locked <0x000000071a2b3c48>` deb topsangiz, lock egasini topdingiz. Egasining stack i muammoni ko'rsatadi, kutuvchilarning stack i esa faqat oqibatni ko'rsatadi.

`WAITING (parking)` holati odatda muammo emas, bu bo'sh pool thread i. Lekin socket o'qish yoki Hibernate so'rovini bajarish metodida turgan `RUNNABLE` thread lar aslida tashqi javobni kutmoqda. Agar 200 ta Tomcat thread idan 190 tasi shunday holatda bo'lsa, diagnoz tayyor: pastki servis yoki baza sekinlashgan, siz esa navbatni ko'rayapsiz.

## 14.3 Heap dump olish (`jmap`, `-XX:+HeapDumpOnOutOfMemoryError`) va tahlil qilish

Heap dump xotira ichidagi barcha obyekt va ularning havolalari. Hajmi live heap ga teng, olinishi esa to'liq STW pauza. 8 GB heap uchun dump fayli taxminan 6-8 GB bo'ladi va JVM taxminan 10-30 sekundga muzlaydi.

```bash
# Faqat tirik obyektlar (dumpdan oldin full GC bo'ladi, pauza uzunroq)
jmap -dump:live,format=b,file=/var/tmp/heap.hprof 4211

# jcmd orqali ham mumkin, xatti-harakati bir xil
jcmd 4211 GC.heap_dump -all=false /var/tmp/heap.hprof

# Dumpsiz tez ko'rish: sinflar bo'yicha gistogramma
jmap -histo:live 4211 | head -30

# Heap bo'limlari va to'lish darajasi
jcmd 4211 GC.heap_info
```

Ishlab chiqarish uchun to'g'ri yondashuv qo'lda dump olish emas, balki avtomatini yoqish:

```properties
# OutOfMemoryError paytida bir marta avtomatik dump
-XX:+HeapDumpOnOutOfMemoryError
-XX:HeapDumpPath=/var/dumps
# OOM dan keyin yarim tirik qolmasin, darhol o'lsin va orkestrator qayta ko'tarsin
-XX:+ExitOnOutOfMemoryError
# GC loglari: sabab tahlilida dumpdan kam bo'lmagan qiymatga ega
-Xlog:gc*,safepoint:file=/var/log/app/gc.log:time,uptime,level:filecount=10,filesize=50M
```

`HeapDumpPath` ko'rsatilgan katalogda heap hajmidan kamida ikki baravar bo'sh joy bo'lishi shart, aks holda dump yarim yozilib buziladi. Konteynerda bu katalog volume bo'lishi kerak, chunki pod o'chganda ephemeral disk ham o'chadi.

Tahlilni Eclipse MAT bilan qilish qulay. Dominator tree da eng katta ildizni topib, uning retained size iga qarasangiz, "agar shu obyekt o'lsa qancha xotira bo'shaydi" degan javobni olasiz. Shallow size emas, aynan retained size qaror uchun muhim. Javob odatda uchta naqshdan biri: cheksiz o'sadigan static map, yopilmagan resurs, yoki kesh da qolgan Hibernate entity grafi.

## 14.4 Java Flight Recorder: yozuvni boshlash, sozlash profili, qancha ortiqcha yuk beradi

JFR JVM ichiga qurilgan hodisa yozuvchisi. U sample emas, balki strukturaviy hodisalar oqimini yozadi: GC fazalari, allokatsiya namunalari, monitor kutishlari, socket va fayl operatsiyalari, class loading, exception. JDK 11 dan boshlab u ochiq va litsenziyasiz, shuning uchun har bir ishlab chiqarish JVM ida yoqilgan bo'lishi kerak.

```bash
# Start paytida: 200 MB aylanma bufer, process to'xtaganda ham diskka yozilsin
java -XX:StartFlightRecording=name=app,settings=default,maxsize=200m,maxage=4h,\
dumponexit=true,filename=/var/dumps/app.jfr -jar payments.jar

# Ishlayotgan JVM da yozuvni boshlash
jcmd 4211 JFR.start name=incident settings=profile maxsize=500m maxage=30m

# Holatini ko'rish
jcmd 4211 JFR.check

# Hozirgi buferni faylga tushirish (yozuv davom etadi)
jcmd 4211 JFR.dump name=incident filename=/var/dumps/incident-1.jfr

# To'xtatish
jcmd 4211 JFR.stop name=incident
```

Ikki standart profil bor. `default` profili taxminan 1 foizdan kam ortiqcha yuk beradi va doimiy yoqilgan holda ishlashga mo'ljallangan. `profile` profili taxminan 2 foiz atrofida yuk beradi, sample oralig'i qisqaroq va allokatsiya hodisalari batafsilroq. Tartib oddiy: `default` har doim yoniq, incident paytida `profile` ni 5-15 daqiqaga qo'shib yoqasiz.

`maxage=4h` bilan aylanma bufer saqlanadi. Bu "muammo bo'lganda yozuvni boshlash" muammosini yechadi: muammo sodir bo'lganda avvalgi to'rt soat allaqachon yozilgan. Stack chuqurligi default da chegaralangan, chuqur Spring proxy zanjirlarida yuqori qatorlar kesilib qolsa `-XX:FlightRecorderOptions=stackdepth=128` ni oshiring. Aniq stack uchun yana `-XX:+UnlockDiagnosticVMOptions -XX:+DebugNonSafepoints` qo'shiladi, u inline qilingan metodlarning noto'g'ri atributlanishini kamaytiradi.

## 14.5 JFR da nimaga qarash: allokatsiya, GC, lock contention, I/O kutish

Fayl ochilgandan keyin tartibsiz qarash vaqtni yo'qotadi. To'rt savolga ketma-ket javob izlang: vaqt CPU da ketdimi, GC da ketdimi, lock da ketdimi, yoki I/O kutishda ketdimi.

```bash
# Umumiy xulosa: qaysi hodisa necha marta yozilgan
jfr summary /var/dumps/incident-1.jfr

# Allokatsiya manbasi: eng ko'p bayt ishlab chiqargan joy
jfr print --events jdk.ObjectAllocationSample /var/dumps/incident-1.jfr | head -60

# GC pauzalari va ularning fazalari
jfr print --events jdk.GCPhasePause /var/dumps/incident-1.jfr | grep duration | head -20

# Lock contention: kim qancha kutdi va qaysi sinf monitorida
jfr print --events jdk.JavaMonitorEnter /var/dumps/incident-1.jfr | head -40

# Tarmoq kutishi: sekin pastki servis shu yerda ko'rinadi
jfr print --events jdk.SocketRead /var/dumps/incident-1.jfr | head -40

# JDK 21+ da tayyor ko'rinishlar, fayl ochmasdan
jcmd 4211 JFR.view hot-methods
```

GC bo'limida mutlaq pauza emas, pauzalarning yig'indisi muhim. 50 ms pauza sekundda yigirma marta takrorlansa, bu ishlash vaqtining katta qismini yeydi. Allokatsiya tezligi sekundiga bir necha gigabayt bo'lsa, GC ni sozlash emas, allokatsiyani kamaytirish kerak. Hisobot servisida bu odatda million qatorni ro'yxatga yig'ishdan kelib chiqadi.

Lock contention bo'limida `jdk.JavaMonitorEnter` hodisasining `monitorClass` maydoni muhim. Agar u servis sinfingiz bo'lsa, `synchronized` metod aybdor. Agar u logging yoki connection pool sinfi bo'lsa, pool o'lchami yoki log appender sozlamasiga qaraysiz. `jdk.ThreadPark` ko'pligi esa `ReentrantLock` yoki pool navbatida kutishni ko'rsatadi.

## 14.6 async-profiler va flame graph o'qish: CPU, allokatsiya, wall-clock rejimi

JFR hodisalarni yozadi, async-profiler esa stack larni juda tez sample qiladi va safepoint bias dan aziyat chekmaydi. Shuning uchun "CPU aniq qaysi metodda yonayapti" savoliga eng aniq javobni o'sha beradi.

```bash
# CPU profili, 30 sekund, natija interaktiv flame graph
./asprof -e cpu -d 30 -f /var/tmp/cpu.html 4211

# Allokatsiya profili: bayt bo'yicha, qaysi joy heap ni to'ldiradi
./asprof -e alloc -d 60 -f /var/tmp/alloc.html 4211

# Wall-clock: kutish ham ko'rinadi, latency muammosi uchun shu kerak
./asprof -e wall -t -d 30 -f /var/tmp/wall.html 4211

# Lock contention
./asprof -e lock -d 60 -f /var/tmp/lock.html 4211

# Konteynerda perf ruxsati bo'lmasa, taymerga o'tish
./asprof -e ctimer -d 30 -f /var/tmp/cpu.html 4211
```

Rejimni to'g'ri tanlash hamma narsani hal qiladi. `cpu` rejimi faqat CPU da ishlagan vaqtni ko'radi, shuning uchun baza javobini kutayotgan so'rov u yerda deyarli ko'rinmaydi. `wall` rejimi hamma holatdagi thread ni sample qiladi, shuning uchun sekin so'rov tahlilida aynan u kerak. Buni aralashtirib yuborish eng ko'p uchraydigan xato: CPU profilida hech narsa topilmagani "muammo yo'q" degani emas, "muammo CPU da emas" degani.

Flame graph ni o'qish qoidasi: gorizontal kenglik vaqt ulushi, vertikal chuqurlik chaqiruv zanjiri. Chapdan o'ngga tartib alifbo bo'yicha, ya'ni u vaqt oqimi emas. Qaraladigan narsa keng va yassi cho'qqilar, chunki ularning ichida chaqiruv kam va ish aynan o'sha metodda bajarilmoqda. Spring ilovalarida grafikning pastki yarmi odatda filter va proxy qatlamlari.

## 14.7 `jcmd` buyruqlari: eng foydali to'plam

`jcmd` bitta kirish nuqtasi va eski alohida utilitalarni almashtiradi. Incident paytida quyidagi to'plam yetarli.

```bash
jcmd -l                                 # JVM lar ro'yxati va PID
jcmd 4211 VM.version                    # aniq JDK versiyasi va build
jcmd 4211 VM.flags -all                 # haqiqiy ergonomika qiymatlari
jcmd 4211 VM.command_line               # ishga tushirish satri
jcmd 4211 Thread.print -l               # thread dump, lock lar bilan
jcmd 4211 GC.heap_info                  # heap bo'limlari holati
jcmd 4211 GC.class_histogram             # sinflar bo'yicha xotira
jcmd 4211 JFR.start settings=profile     # yozuvni boshlash
jcmd 4211 JFR.dump name=1 filename=/var/tmp/a.jfr
jcmd 4211 Compiler.codecache             # code cache to'lganini tekshirish
jcmd 4211 VM.native_memory summary       # NMT yoqilgan bo'lsa, heapdan tashqari xotira
```

`VM.native_memory` uchun JVM `-XX:NativeMemoryTracking=summary` bilan ishga tushgan bo'lishi kerak va u taxminan 5-10 foiz xotira qo'shadi. Lekin konteyner RSS heap dan ancha katta bo'lgan holatda faqat shu buyruq javob beradi: metaspace, code cache, thread stack, yoki direct byte buffer. `VM.flags -all` ni alohida ta'kidlash kerak: konteynerda JVM heap va GC thread sonini o'zi tanlaydi, siz kutgan qiymat bilan haqiqiy qiymat ko'pincha mos kelmaydi.

## 14.8 Mikro o'lchov tuzoqlari va JMH nega kerak

`System.nanoTime()` bilan halqa ichida metodni o'lchash deyarli har doim yolg'on raqam beradi. JIT birinchi minglab chaqiruvdan keyin kodni qayta kompilyatsiya qiladi, natijani ishlatmasangiz butunlay o'chirib tashlaydi, doimiy argumentni esa kompilyatsiya vaqtida hisoblab qo'yadi. Shuning uchun "optimizatsiyam 50 barobar tezlashdi" degan o'lchov odatda o'lchov xatosi.

```java
@BenchmarkMode(Mode.AverageTime)
@OutputTimeUnit(TimeUnit.MICROSECONDS)
@Warmup(iterations = 5, time = 2)        // JIT qizishi uchun
@Measurement(iterations = 10, time = 2)
@Fork(value = 3)                         // har fork alohida JVM
@State(Scope.Benchmark)
public class OrderTotalBenchmark {

    private List<OrderLine> lines;

    @Setup
    public void setUp() {
        lines = generateLines(500);       // real o'lchamga yaqin ma'lumot
    }

    @Benchmark
    public BigDecimal streamSum() {
        return lines.stream().map(OrderLine::amount)
                .reduce(BigDecimal.ZERO, BigDecimal::add);
    }

    @Benchmark
    public void loopSum(Blackhole bh) {   // natija o'chib ketmasin
        BigDecimal total = BigDecimal.ZERO;
        for (OrderLine l : lines) { total = total.add(l.amount()); }
        bh.consume(total);                // dead code elimination to'xtaydi
    }
}
```

JMH shu uch tuzoqni hal qiladi: alohida fork, majburiy warmup va `Blackhole` orqali dead code eliminationni to'xtatish. `-prof gc` bilan ishga tushirsangiz operatsiyaga nechchi bayt allokatsiya qilinganini ham ko'rasiz, bu ko'pincha nanosekunddan muhimroq dalil.

Lekin arxitektor uchun asosiy xulosa boshqa. Mikro benchmark faqat algoritm darajasidagi savolga javob beradi. Servis darajasidagi latency ni u hech qachon izohlamaydi, chunki u yerda pool, tarmoq va GC ta'siri hal qiladi. Shuning uchun mikro o'lchovni tanlov uchun ishlatasiz, qarorni esa JFR va yuk testi tasdiqlaydi.

## 14.9 Ishlab chiqarish muhitida profiling: xavfsizlik va ortiqcha yuk masalasi

Ishlab chiqarishda profiling qilish kerak, chunki stage muhit real trafik va real ma'lumot hajmini takrorlamaydi. Masala qancha yuk va qancha risk qabul qilishda.

Yuk tomoni hisoblanadigan: JFR `default` taxminan 1 foizdan kam, JFR `profile` taxminan 2 foiz, async-profiler CPU rejimi taxminan 1-3 foiz, thread dump bir necha o'n millisekund pauza, heap dump esa o'n sekundlab to'liq pauza. Ro'yxatda faqat heap dump xavfli, uni trafikdan chiqarilgan instansiyada olish kerak.

Xavfsizlik tomoni ko'pincha e'tiborsiz qoladi. Heap dump ichida ochiq matnda karta raqami, token, parol va mijoz ma'lumotlari bo'ladi. Shuning uchun dump maxfiy ma'lumot sifatida ko'riladi: shifrlangan joyda saqlanadi, kirish huquqi cheklangan, saqlash muddati bor va u hech qachon tiketga biriktirilmaydi.

Operatsion jihat: diagnostika asboblari image ichida bo'lishi kerak. Faqat runtime qolgan image da `jcmd` yo'q, incident paytida esa uni o'rnatib bo'lmaydi. Shuning uchun `jcmd`, `jfr` va async-profiler ni image ga qo'shish arxitektura qarori.

| Tuzoq | Nima sodir bo'ladi | Yechim |
|---|---|---|
| Faqat bitta thread dump olish | Bir lahza foto, sabab ko'rinmaydi | 10 s oraliq bilan 3-5 dump olish |
| CPU profili bilan sekin so'rovni izlash | Kutish ko'rinmaydi, profil bo'sh chiqadi | `wall` rejimi yoki JFR socket hodisalari |
| Ishlab chiqarishda heap dump olish | O'n sekundlab STW, health check yiqiladi | Instansiyani trafikdan chiqarib dump olish |
| `HeapDumpPath` da joy yetmasligi | Dump buzilgan, tahlil imkonsiz | Heap dan 2 barobar katta volume ajratish |
| Incident boshlanganda JFR yoqish | Muammo boshlanishi yozilmagan | `maxage` bilan aylanma bufer doimiy yoniq |
| Heap dumpni tiketga biriktirish | Maxfiy ma'lumot tarqaladi | Shifrlangan ombor, muddatli saqlash |
| `jstack -F` majburan ishlatish | Process qotishi mumkin | Avval oddiy `jcmd`, keyin JFR dalili |
| Mikro benchmarkka ishonib arxitektura o'zgartirish | JIT artefakti haqiqat deb qabul qilinadi | JMH plus servis darajasida yuk testi |
| Actuator heap dump endpointini ochiq qoldirish | Istalgan odam butun xotirani yuklab oladi | Alohida port, auth, endpointni o'chirish |

## 14.10 Spring Boot Actuator orqali diagnostika endpointlari

Actuator JVM asboblarini almashtirmaydi, lekin eng tez birinchi qarashni beradi. Muhim shart: diagnostika endpointlari biznes trafik portida turmasligi kerak.

```yaml
management:
  server:
    port: 9091                 # diagnostika alohida portda, tashqi LB ga chiqmaydi
  endpoints:
    web:
      exposure:
        include: health,info,metrics,prometheus,threaddump,loggers
  endpoint:
    heapdump:
      enabled: false           # kerak bo'lganda qo'lda yoqiladi
    health:
      show-details: when-authorized
  metrics:
    tags:
      application: payments
```

Eng foydali metrikalar: `hikaricp.connections.pending` nolda turmasa connection pool tor, `executor.queued` va `executor.active` async pool to'lishini ko'rsatadi, `jvm.gc.pause` va `jvm.memory.used` GC bosimini beradi. `/actuator/loggers` orqali qayta deploy qilmasdan bitta paketga DEBUG yoqish incident paytida juda qimmatli.

`/actuator/threaddump` va `/actuator/heapdump` faqat himoyalangan holda bo'lishi kerak. Heap dump endpointini odatda o'chirib qo'yish va zarurat tug'ilganda `jcmd` bilan ishlash xavfsizroq.

## 14.11 Tez-tez uchraydigan diagnoz: sekin so'rov, thread pool to'lishi, xotira sizishi

Sekin so'rovda zanjir bo'ylab yurish kerak. Thread dump da ko'p thread baza drayveri ichida turgan bo'lsa, muammo JVM da emas. Shu paytda bazaga qarash kerak:

```sql
-- Hozir ishlayotgan va kutayotgan so'rovlar, eng uzunidan boshlab
SELECT pid, now() - query_start AS runtime, state, wait_event_type, wait_event,
       left(query, 120) AS q
FROM pg_stat_activity
WHERE state <> 'idle' AND backend_type = 'client backend'
ORDER BY query_start;
```

Agar `pg_stat_activity` da uzun so'rov yo'q, lekin ilovada so'rov sekin ko'rinsa, vaqt connection kutishida ketmoqda. Bu pool o'lchami yoki tranzaksiya uzunligi muammosi, so'rov muammosi emas.

Thread pool to'lishining belgisi: `executor.queued` o'sib boradi, CPU past, latency esa chiziqli ortadi. Yechim pool ni ko'paytirish emas, balki pastki servisga timeout qo'yish va navbatga chegara berish. Timeout siz pool bir kun ichida albatta to'ladi.

Xotira sizishida uch dalil kerak: `jvm.memory.used` ning full GC dan keyingi pastki chizig'i o'sib borishi, `GC.class_histogram` da bitta sinf sonining monoton o'sishi, va heap dump dominator tree da shu obyektni ushlab turgan ildiz. Uchtasi ham bir xil narsani ko'rsatsa, diagnoz ishonchli.

| Savol | Oddiy yondashuv | Arxitektor yondashuvi |
|---|---|---|
| Ilova sekinlashdi | Kodga qarab taxmin qilish | p50 va p99 ni ajratib, resursni aniqlash |
| Qaysi asbob | Hamma joyda CPU profili | Kutish uchun wall-clock, CPU uchun cpu rejimi |
| JFR qachon yoqiladi | Muammo chiqqanda | `maxage` bufer bilan doimiy yoniq |
| Thread dump | Bitta dump olib o'qish | 3-5 dump, lock egasini topish |
| Heap dump | Ishlab chiqarishda darhol olish | Instansiyani trafikdan chiqarib olish |
| OOM ga tayyorlik | Logdagi xatoni o'qish | `HeapDumpOnOutOfMemoryError` plus volume plus `ExitOnOutOfMemoryError` |
| Optimizatsiya o'lchovi | `nanoTime` bilan halqa | JMH, fork, warmup, `-prof gc` |
| Pool to'lishi | Pool o'lchamini oshirish | Timeout, navbat chegarasi, Little qonuni hisobi |
| Dump maxfiyligi | Tiketga biriktirish | Shifrlangan ombor, cheklangan kirish |
| Diagnostika kirishi | Actuator biznes portida | Alohida management port va auth |
| Xulosa | Tuzatib unutish | Belgi, o'lchov, sabab, tuzatish yozuvi |

## 14.12 Amalda qo'llash

- [ ] Barcha ishlab chiqarish JVM lariga `-XX:StartFlightRecording` ni `settings=default`, `maxage=4h`, `dumponexit=true` bilan qo'shing va yozuv faylini doimiy volume ga chiqaring.
- [ ] `-XX:+HeapDumpOnOutOfMemoryError`, `-XX:HeapDumpPath` va `-XX:+ExitOnOutOfMemoryError` ni qo'shing, `HeapDumpPath` volume ida heap dan 2 barobar bo'sh joy borligini tekshirib ko'ring.
- [ ] GC va safepoint loglarini `-Xlog:gc*,safepoint` bilan fayl rotatsiyasi ostida yoqing va 7 kundan kam bo'lmagan muddatga saqlang.
- [ ] Konteyner image ichida `jcmd`, `jfr` va async-profiler mavjudligini tekshiring, yo'q bo'lsa image ga qo'shing.
- [ ] Incident uchun bitta runbook yozing: uch thread dump, JFR `profile` 10 daqiqa, keyin kerak bo'lsa izolyatsiyalangan instansiyada heap dump.
- [ ] Actuator ni `management.server.port` orqali alohida portga chiqaring, `heapdump` endpointini o'chiring va health detallarini faqat autentifikatsiyadan keyin ko'rsatadigan qilib qo'ying.
- [ ] `hikaricp.connections.pending`, `executor.queued` va `jvm.gc.pause` uchun alert qo'ying, chunki bu uchtasi latency muammosini belgidan oldin ko'rsatadi.
- [ ] Eng qimmat ikkita hot path uchun JMH benchmark yozing va uning natijasini servis darajasidagi yuk testi bilan taqqoslab tekshirib ko'ring.

---

[&larr; 13. Zamonaviy Java tili va API dizayni](13-zamonaviy-java-tili-va-api-dizayni.md) · [Mundarija](README.md) · [15. Spring Core mexanikasi: IoC konteyner, bean lifecycle, AOP proxy &rarr;](15-spring-core-mexanikasi-ioc-konteyner-bean.md)
