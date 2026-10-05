<!-- doc: architect | chapter: 10 | part: II. Java chuqur bilim -->

[Barcha hujjatlar](../../README.md) / [Arxitektor miyasi](README.md)

# 10. Garbage collection va xotira sozlash (Garbage Collection and Memory Tuning)

<details>
<summary>Bu bobdagi 12 bo'lim</summary>

- [10.1 GC nima uchun kerak va u qaysi muammoni hal qiladi](#101-gc-nima-uchun-kerak-va-u-qaysi-muammoni-hal-qiladi)
- [10.2 Avlodlar farazi (generational hypothesis) va young/old hudud](#102-avlodlar-farazi-generational-hypothesis-va-youngold-hudud)
- [10.3 G1GC ishlash tartibi: region, young collection, mixed collection](#103-g1gc-ishlash-tartibi-region-young-collection-mixed-collection)
- [10.4 ZGC va Shenandoah: past pauza evaziga nima to'lanadi](#104-zgc-va-shenandoah-past-pauza-evaziga-nima-tolanadi)
- [10.5 Serial va Parallel GC: kichik konteynerda qachon mantiqli](#105-serial-va-parallel-gc-kichik-konteynerda-qachon-mantiqli)
- [10.6 Qaysi GC ni tanlash: jadval bilan, yadro va xotira hajmiga qarab](#106-qaysi-gc-ni-tanlash-jadval-bilan-yadro-va-xotira-hajmiga-qarab)
- [10.7 Heap kattaligini tanlash va `-Xmx` ni konteyner limiti bilan bog'lash](#107-heap-kattaligini-tanlash-va--xmx-ni-konteyner-limiti-bilan-boglash)
- [10.8 GC log ni yoqish va o'qish: pauza vaqti, sabab, hudud hajmi](#108-gc-log-ni-yoqish-va-oqish-pauza-vaqti-sabab-hudud-hajmi)
- [10.9 Xotira sizishi (leak) belgilari va heap dump bilan tekshirish](#109-xotira-sizishi-leak-belgilari-va-heap-dump-bilan-tekshirish)
- [10.10 Off-heap xotira: direct buffer, Netty, metaspace o'sishi](#1010-off-heap-xotira-direct-buffer-netty-metaspace-osishi)
- [10.11 Allokatsiyani kamaytirish: ortiqcha obyekt yaratmaslik amaliyoti](#1011-allokatsiyani-kamaytirish-ortiqcha-obyekt-yaratmaslik-amaliyoti)
- [10.12 Amalda qo'llash](#1012-amalda-qollash)

</details>



Garbage collector JVM ning eng ko'p noto'g'ri sozlanadigan qismi. Ko'pchilik jamoa uni faqat `OutOfMemoryError` chiqqanda eslaydi, keyin `-Xmx` ni oshiradi va muammo yashiringanday bo'ladi. Arxitektor esa GC ni latency byudjetining bir qismi deb ko'radi: p99 200 ms bo'lsa, GC pauzasi uning qancha ulushini yeyishi oldindan hisoblangan bo'lishi shart.

## 10.1 GC nima uchun kerak va u qaysi muammoni hal qiladi

GC bitta vazifani bajaradi: endi hech kim murojaat qilmaydigan obyektlar xotirasini qaytarib oladi. Evaziga uch narsa to'lanadi: CPU, xotira va pauza.

Muhim nuqta: GC "axlatni" emas, "tirik obyektni" izlaydi. Kollektor GC root lardan (thread stack, static maydon, JNI reference) erishiladigan grafni kezadi, qolgani o'lik hisoblanadi. Shuning uchun GC xarajati o'lik obyektlar soniga emas, TIRIK obyektlar hajmiga bog'liq. Buyurtma servisida 500 ming vaqtinchalik DTO arzon tushadi, lekin 2 GB li cache har marking siklda qayta kezib chiqiladi.

Ikkinchi nuqta: allokatsiya arzon. Har thread o'z TLAB (Thread Local Allocation Buffer) sohasida pointer ni surish bilan obyekt yaratadi, taxminan 10 nanosekunddan kam. Qimmat narsa, obyektning tirik qolib old hududga ko'chishi.

## 10.2 Avlodlar farazi (generational hypothesis) va young/old hudud

Barcha zamonaviy kollektorlar bitta empirik kuzatuvga tayanadi: obyektlarning katta qismi juda yosh holida o'ladi. Hisobot metodidagi `StringBuilder`, JDBC qatorlari, Jackson node lari bir necha millisekund yashaydi. Tirik qolganlar uzoq yashaydi: Spring bean lari, connection pool, cache yozuvlari.

Shundan amaliy natija chiqadi: young hududni tez-tez va arzon yig'ish mumkin. Young collection faqat tirik obyektlarni ko'chiradi, ya'ni ish hajmi survival rate ga proporsional. Young hududda 1 GB dan faqat 30 MB tirik qolsa, pauza taxminan 10 ms bo'ladi.

Old hududni to'liq kezish qimmat, shuning uchun marking application bilan parallel bajariladi. Bu yerda card table va remembered set ishlaydi: old hududdagi obyekt young obyektga reference yozsa, write barrier card ni "dirty" deb belgilaydi. Shu sababli young collection butun old hududni emas, faqat dirty card larni skanerlaydi.

Xulosa: survival rate ni pasaytirish GC ni tezlashtiradi. Har request da 5 MB lik graf yasab uni cache ga tiqish o'sha obyektlarni old hududga promote qiladi va mixed collection ni og'irlashtiradi.

## 10.3 G1GC ishlash tartibi: region, young collection, mixed collection

G1 (Garbage First) JDK 9 dan beri standart kollektor va 4 GB dan 32 GB gacha heap uchun oqilona tanlov. U heap ni teng region larga bo'ladi, har biri 1 MB dan 32 MB gacha (taxminan heap / 2048, ikkining darajasiga yaxlitlanadi). Har bir region Eden, Survivor, Old yoki Humongous rolini o'ynaydi va rol sikldan siklga o'zgaradi. Shuning uchun G1 da `-Xmn` ni qattiq belgilash deyarli har doim xato: young hudud hajmi pauza maqsadiga qarab moslanadi.

G1 uch xil ish bajaradi. Young evacuation pause: Eden va Survivor region laridan tirik obyektlar ko'chiriladi, bu stop-the-world. Concurrent marking: heap band bo'lishi IHOP chegarasiga yetganda old hududni parallel markalash boshlanadi. Mixed collection: young region lar bilan birga eng ko'p axlat saqlagan old region lar ham evakuatsiya qilinadi. "Garbage first" nomi shundan.

```bash
# To'lov servisi: 8 vCPU, 8 GB konteyner, p99 maqsadi 150 ms
java -XX:+UseG1GC -XX:MaxRAMPercentage=70.0 \
  -XX:MaxGCPauseMillis=100 \
  -XX:+ParallelRefProcEnabled -XX:+AlwaysPreTouch \
  -XX:+HeapDumpOnOutOfMemoryError \
  -XX:HeapDumpPath=/var/log/app/heap.hprof \
  -jar payment-service.jar
```

`MaxGCPauseMillis` kafolat emas, maqsad. G1 uni ushlash uchun young hududni kichraytiradi, natijada collection lar tez-tez bo'ladi va throughput pasayadi. 50 ms dan past qiymat ko'p holda teskari natija beradi: pauza qisqarmaydi, GC CPU iste'moli oshadi. Amalda 100 dan 200 ms oralig'i sog'lom.

G1 ning eng xavfli holati: to-space exhausted. Evakuatsiya uchun bo'sh region qolmaganda G1 full GC ga tushadi va bu bir necha sekund davom etadi. Sabab odatda juda tez allokatsiya yoki humongous obyektlar. Region yarmidan katta array (16 MB region da 10 MB lik `byte[]`) humongous hisoblanadi va ketma-ket region larni band qiladi. Hisobot servisida butun CSV ni bitta `byte[]` ga yuklash shu muammoni tug'diradi.

## 10.4 ZGC va Shenandoah: past pauza evaziga nima to'lanadi

ZGC va Shenandoah bir maqsadni ko'zlaydi: pauzani heap hajmidan mustaqil qilish. Ikkisi ham evakuatsiyani application ishlab turganda bajaradi, buning uchun barrier ishlatiladi: ZGC da colored pointer va load barrier, Shenandoah da load reference barrier. Thread ko'chirilgan obyektga murojaat qilsa, barrier uni yangi manzilga yo'naltiradi.

ZGC da pauzalar bir necha yuz mikrosekund darajasida va 128 GB heap da ham shunday qoladi. JDK 21 da generational ZGC qo'shildi, JDK 23 dan boshlab u standart rejim. Eski ZGC yuqori allokatsiya tezligida heap ni to'ldirib qo'yardi.

Evaziga uch narsa to'lanadi. Throughput: barrier lar har reference o'qishga instruksiya qo'shadi, G1 ga nisbatan 5 dan 15 foizgacha yo'qotish odatiy. Xotira: concurrent evakuatsiya uchun zaxira joy kerak, heap ni to'liq to'ldirib ishlatish mumkin emas. Allocation stall: allokatsiya tezligi GC ning bo'shatish tezligidan oshsa thread lar to'xtaydi, bu "pauzasiz" GC da eng chalkash muammo.

```bash
# Past latency talab qilinadigan API gateway: 16 vCPU, 32 GB
java -XX:+UseZGC \
  -Xms20g -Xmx20g \
  -XX:SoftMaxHeapSize=16g \
  -XX:+UseLargePages \
  -Xlog:gc*,safepoint:file=/var/log/app/gc.log:time,uptime:filecount=5,filesize=50M \
  -jar gateway.jar

# Shenandoah faqat ba'zi distributiv JDK larda mavjud (masalan Red Hat build)
java -XX:+UseShenandoahGC -Xms8g -Xmx8g -jar order-service.jar
```

`SoftMaxHeapSize` ZGC ni shu chegarada ushlashga urinadi, lekin zarurat bo'lsa `-Xmx` gacha o'sishga ruxsat beradi, bu burst trafikda OOM dan saqlaydi.

## 10.5 Serial va Parallel GC: kichik konteynerda qachon mantiqli

Serial GC ni "eski" deb yozib qo'yish keng tarqalgan xato. 1 vCPU va 512 MB ajratilgan konteynerda u ko'pincha G1 dan yaxshi ishlaydi. Sabab: G1 ga concurrent marking thread lari, write barrier va remembered set kerak, bitta CPU da bular application dan vaqt tortadi. Serial GC da barrier minimal, 100 MB young hudud uchun pauza 20 dan 50 ms.

JVM ergonomikasi buni o'zi ham aniqlaydi: 2 dan kam CPU yoki taxminan 1792 MB dan kam xotira ko'rsa, Serial GC tanlanadi. Lekin bu qaror konteynerda xato chiqishi mumkin, shuning uchun kollektorni aniq yozib qo'yish to'g'ri.

Parallel GC boshqa holat uchun: pauza muhim emas, throughput muhim. Tungi batch, hisobot, ETL job. U bir xil CPU byudjetida G1 dan taxminan 10 dan 20 foizgacha ko'proq foydali ish bajaradi. 2 sekundlik pauza 4 soatlik job da hech kimni bezovta qilmaydi.

```bash
# Kichik sidecar yoki Spring Boot admin util: 1 vCPU, 512 MB
java -XX:+UseSerialGC -XX:MaxRAMPercentage=60.0 -jar config-sync.jar

# Tungi hisobot batch job: throughput muhim, pauza muhim emas
java -XX:+UseParallelGC \
  -XX:MaxRAMPercentage=75.0 \
  -XX:ActiveProcessorCount=4 \
  -jar monthly-report.jar
```

## 10.6 Qaysi GC ni tanlash: jadval bilan, yadro va xotira hajmiga qarab

Tanlov ikki o'qda yotadi: CPU soni va latency talabi. Jadval boshlang'ich nuqta beradi, keyin o'z yuklamangizda o'lchash kerak.

| Kollektor | CPU | Heap | Odatiy pauza | Throughput | Qachon mantiqli |
|---|---|---|---|---|---|
| Serial | 1 | 512 MB gacha | 20-50 ms | o'rtacha | sidecar, CLI util, kichik konteyner |
| Parallel | 2-8 | 1-8 GB | 100 ms - 2 s | eng yuqori | batch, ETL, tungi hisobot |
| G1 | 4+ | 4-32 GB | 50-200 ms | yuqori | oddiy REST servis, standart tanlov |
| Generational ZGC | 8+ | 8 GB - 1 TB | 1 ms dan kam | G1 dan 5-15% past | past p99 talab, katta cache |
| Shenandoah | 8+ | 4-64 GB | 1-10 ms | ZGC ga yaqin | past pauza, kichikroq heap |

Qoida: 4 GB dan kichik heap va 4 dan kam vCPU bo'lsa G1 ni majburlamang. 32 GB dan katta heap yoki qattiq p99 SLA bo'lsa generational ZGC ni sinang. Qolgan holatda G1 ni o'zgartirmaslik eng kam xatarli qaror.

| Savol | Oddiy yondashuv | Arxitektor yondashuvi |
|---|---|---|
| GC tanlash | default qoldiriladi yoki blog dan ko'chiriladi | CPU, heap va p99 byudjetiga qarab tanlanadi |
| `-Xmx` qiymati | konteyner limiti bilan teng yoziladi | limitdan off-heap zaxira ayirib hisoblanadi |
| OOM chiqqanda | `-Xmx` ikki baravar oshiriladi | heap dump olinadi, dominator tree o'rganiladi |
| GC log | yoqilmagan yoki faqat xatolikda ko'riladi | doim yoqilgan, rotatsiya bilan, dashboard da |
| Pauza maqsadi | `MaxGCPauseMillis=20` yoziladi | 100-200 ms qo'yiladi, keyin o'lchanadi |
| Katta ro'yxat qaytarish | butun natija `List` ga yuklanadi | stream va pagination bilan o'qiladi |
| Off-heap xotira | hisobga olinmaydi | metaspace va direct buffer limitlangan, NMT bor |
| Leak gumoni | restart qilib yuboriladi | ikki vaqt oralig'ida histogram taqqoslanadi |
| GC regressiyasi | prod da sezilmaydi | yuklama testida GC metrikasi solishtiriladi |

## 10.7 Heap kattaligini tanlash va `-Xmx` ni konteyner limiti bilan bog'lash

Eng ko'p uchraydigan incident: pod `OOMKilled` bo'ladi, lekin heap dump yo'q va GC log da OOM ko'rinmaydi. Sababi: JVM heap limitida qolgan, lekin jarayonning RSS si konteyner limitidan oshgan. Kernel uni o'ldirgan, JVM buni bilmaydi ham.

Java jarayonining xotirasi faqat heap emas. Unga metaspace, code cache, thread stack (har biri taxminan 1 MB), GC strukturalari, direct buffer va native qism qo'shiladi. Amaliy taxmin: heap dan tashqari 300 MB dan 700 MB gacha.

```bash
# XATO: 2 GB limitli konteynerda heap ham 2 GB
java -Xmx2g -jar order-service.jar     # OOMKilled bo'ladi

# TO'G'RI: foiz orqali, JVM cgroup limitini o'zi o'qiydi
java -XX:MaxRAMPercentage=70.0 \
  -XX:InitialRAMPercentage=70.0 \
  -XX:MaxMetaspaceSize=256m \
  -XX:MaxDirectMemorySize=256m \
  -XX:+ExitOnOutOfMemoryError \
  -jar order-service.jar

# Tekshirish: JVM qanday qiymat tanladi
java -XX:MaxRAMPercentage=70.0 -XX:+PrintFlagsFinal -version | grep -i maxheapsize
```

`MaxRAMPercentage` ning standart qiymati 25 foiz, bu katta konteynerda juda kam. 70 foiz yaxshi boshlang'ich: 4 GB limitda taxminan 2.8 GB heap. `Xms` ni `Xmx` ga tenglashtirish tavsiya etiladi, chunki heap ning asta o'sishi autoscaling metrikalarini chalkashtiradi.

Yana bir nuqta: 32 GB chegarasi. Shu hajmgacha JVM compressed oops ishlatadi, reference 4 bayt. Chegaradan oshsa reference 8 baytga aylanadi. 33 GB heap 31 GB dan kamroq foydali obyekt sig'dirishi mumkin, shuning uchun `-Xmx31g` dan `-Xmx33g` ga o'tish zarar keltiradi.

## 10.8 GC log ni yoqish va o'qish: pauza vaqti, sabab, hudud hajmi

GC log prod da doim yoqilgan bo'lishi kerak. Overhead i deyarli nol, qiymati yuqori: GC log bo'lmasa incident tahlili taxminga aylanadi. JDK 9 dan beri unified logging ishlatiladi, eski `-XX:+PrintGCDetails` o'rniga `-Xlog` keladi.

```bash
# Prod uchun minimal va yetarli konfiguratsiya
-Xlog:gc*:file=/var/log/app/gc.log:time,uptime,level,tags:filecount=10,filesize=20M

# Chuqur tahlil uchun (vaqtincha, debug paytida)
-Xlog:gc*,gc+heap=debug,gc+ergo=trace,safepoint:file=/var/log/app/gc-debug.log

# Log dagi muhim satrlar
# [12.345s] GC(7) Pause Young (Normal) (G1 Evacuation Pause) 1024M->312M(4096M) 18.472ms
# [88.004s] GC(41) To-space exhausted
# [88.330s] GC(41) Pause Full (G1 Compaction Pause) 3900M->1200M(4096M) 2341.7ms
```

Qavs ichidagi sabab eng muhim: `G1 Evacuation Pause` normal holat, `G1 Humongous Allocation` juda katta obyekt, `Metadata GC Threshold` metaspace to'lgani. `Pause Full` G1 da har doim muammo belgisi.

Keyin raqamlar: `1024M->312M(4096M)` GC dan oldin, keyin va umumiy heap. "Keyin" qiymati o'sib borib qaytmasa, bu leak. U `Xmx` ga yaqinlashib full GC lar ketma-ket kelsa, servis o'lim spiraliga tushgan.

Uchinchi metrika: GC chastotasi. Young collection har 300 ms da kelib 1 GB ni tozalasa, servis sekundiga taxminan 3 GB allokatsiya qiladi, bu juda baland. Micrometer orqali `jvm.gc.pause` va `jvm.gc.memory.allocated` ni chiqarib, GC CPU ulushini 10 foizdan past ushlash amaliy maqsad.

## 10.9 Xotira sizishi (leak) belgilari va heap dump bilan tekshirish

Leak ning uch belgisi bor. Full GC dan keyingi heap qoldig'i monoton o'sadi. GC chastotasi oshadi, lekin har sikl kamroq xotira qaytaradi. Servis bir necha kundan keyin sekinlashadi va restart dan keyin tiklanadi. Oxirgisi eng ko'p uchraydi, chunki restart "yechim" deb qabul qilinadi.

Dump olish paytida JVM to'liq to'xtaydi, 4 GB heap uchun 10 dan 30 sekund. Shuning uchun dump ni load balancer dan chiqarilgan instance da olish to'g'ri.

```bash
# Tirik obyektlar histogrammasi (dump dan arzonroq)
jcmd $(pgrep -f order-service) GC.class_histogram | head -25

# To'liq heap dump
jcmd $(pgrep -f order-service) GC.heap_dump /var/log/app/dump-1.hprof

# Heap holati va classloader statistikasi
jcmd $(pgrep -f order-service) GC.heap_info
jcmd $(pgrep -f order-service) VM.classloader_stats
```

Eng ishonchli usul: ikki heap dump, orasida 30 dan 60 minut, keyin Eclipse MAT da solishtirib dominator tree da o'sgan branch ni topish. Dominator tree "bu obyekt o'lsa qancha xotira bo'shaydi" degan savolga javob beradi, histogram esa bermaydi.

Spring ilovalarida leak manbalari aniq: TTL va maksimal hajm belgilanmagan Caffeine cache; `static Map` ga user context yozish; `ThreadLocal` ni pool thread da `remove` qilmaslik; katta tranzaksiyada minglab entity ni persistence context da ushlash. Oxirgisi leak emas, lekin bir xil natija beradi.

## 10.10 Off-heap xotira: direct buffer, Netty, metaspace o'sishi

Heap dump toza, GC log sog'lom, lekin RSS o'sib boradi. Bu deyarli har doim off-heap ni ko'rsatadi, va Native Memory Tracking yagona ishonchli diagnostika vositasi.

```bash
# Start da yoqish kerak, taxminan 5-10% overhead
java -XX:NativeMemoryTracking=summary -XX:+UseG1GC -jar gateway.jar

# Hozirgi holat, keyin baseline va o'sish farqi
jcmd $(pgrep -f gateway) VM.native_memory summary scale=MB
jcmd $(pgrep -f gateway) VM.native_memory baseline
jcmd $(pgrep -f gateway) VM.native_memory summary.diff scale=MB
```

Uch asosiy off-heap manba bor. Direct byte buffer: `ByteBuffer.allocateDirect` yaratgan xotira heap tashqarisida yotadi va faqat buffer obyekti GC bo'lganda bo'shaydi. `-XX:MaxDirectMemorySize` ni aniq qo'ying, aks holda u `-Xmx` ga teng olinadi va limit ikki baravar oshadi.

Netty (Spring WebFlux va Gateway ostida) o'z pooled direct allocator ini ishlatadi. U heap limitiga hisoblanmaydi va `io.netty.maxDirectMemory` bilan boshqariladi. Staging da `io.netty.leakDetection.level=paranoid` yoqib, release qilinmagan buffer ni aniqlash mumkin. Prod da bu rejim qimmat.

Metaspace class metadata ni saqlaydi va standart holda cheklanmagan. U o'sishining yagona sababi: yangi class lar yuklanishi. Servis ishlab turib metaspace o'sa, demak dinamik proxy yoki bytecode generatsiya classloader leak ga olib kelgan. `-XX:MaxMetaspaceSize=256m` leak ni to'xtatmaydi, lekin uni aniq xatolik bilan ko'rsatadi.

| Tuzoq | Nima bo'ladi | Yechim |
|---|---|---|
| `-Xmx` konteyner limitiga teng | pod `OOMKilled`, dump yo'q | `MaxRAMPercentage=70`, native uchun zaxira |
| `MaxGCPauseMillis=20` | GC CPU oshadi, pauza qisqarmaydi | 100-200 ms, keyin o'lchash |
| `-Xmx33g` | compressed oops yo'qoladi | 31 GB da qolish yoki ZGC ga o'tish |
| Butun jadvalni `List` ga yuklash | humongous allokatsiya, full GC | pagination yoki stream bilan o'qish |
| `MaxDirectMemorySize` yo'q | off-heap `Xmx` gacha o'sadi | aniq limit va NMT monitoring |
| Metaspace cheklanmagan | RSS sekin o'sadi, OOMKilled | `MaxMetaspaceSize` va classloader audit |
| GC log yoqilmagan | incident sababi topilmaydi | `-Xlog:gc*` rotatsiya bilan, doim yoniq |
| Cache da TTL yo'q | old hudud to'ladi | hajm va TTL majburiy, metrika bilan |
| `ThreadLocal` tozalanmagan | pool thread da leak | `finally` da `remove` |

## 10.11 Allokatsiyani kamaytirish: ortiqcha obyekt yaratmaslik amaliyoti

GC ni sozlashdan ko'ra allokatsiyani kamaytirish samaraliroq: yaratilmagan obyektni yig'ish kerak emas. Lekin mikro-optimizatsiya o'rniga allokatsiya tezligi eng baland joyni topish kerak, JFR buni aniq ko'rsatadi.

```bash
# JFR yozib olish, allokatsiya profili bilan
java -XX:StartFlightRecording=duration=120s,filename=/tmp/alloc.jfr,settings=profile \
  -jar order-service.jar

# Natijani tahlil qilish: eng ko'p allokatsiya qiladigan joylar
jfr print --events ObjectAllocationSample /tmp/alloc.jfr | head -40
```

Birinchi texnika: kolleksiyani oldindan o'lchamlash. `new ArrayList<>()` 10 element bilan boshlanadi va 10 ming element uchun taxminan 17 marta qayta allokatsiya qiladi. Ikkinchisi: SLF4J ning parametrli formatini ishlatish, aks holda `DEBUG` o'chiq bo'lsa ham string yasaladi.

```java
// Ombor qoldig'i: primitiv long, Long boxing yo'q
public long hisoblaQoldiq(List<Harakat> harakatlar) {
    long jami = 0;
    for (int i = 0; i < harakatlar.size(); i++) {
        jami += harakatlar.get(i).miqdor();
    }
    return jami;
}

// Parametrli format: DEBUG o'chiq bo'lsa string yasalmaydi
log.debug("Qoldiq: ombor={}, qoldiq={}", omborId, jami);
// XATO: log.debug("Qoldiq: " + omborId + " = " + jami);

// Katta natija stream bilan, butun ro'yxat heap ga tushmaydi
@Transactional(readOnly = true)
public void eksport(Writer writer) {
    try (Stream<Buyurtma> oqim = repo.topAllStream()) {
        oqim.forEach(b -> yoz(writer, b));   // har 500 da clear kerak
    }
}
```

Uchinchisi: autoboxing dan qutulish. `Map<Long, Long>` da million yozuvda har kalit va qiymat alohida `Long` obyekt. Primitiv kolleksiya kutubxonasi (Eclipse Collections, fastutil) heap ni 3 dan 5 baravargacha kamaytiradi.

To'rtinchisi: escape analysis ga ishonish. JIT metoddan chiqmaydigan kichik obyektni scalar replacement orqali umuman allokatsiya qilmasligi mumkin, shuning uchun kodni buzish kerak emas. Obyekt metoddan chiqsa yoki field ga yozilsa, bu optimizatsiya ishlamaydi.

Beshinchisi: obyekt pool dan ehtiyot bo'lish. Kichik obyektlar uchun pool deyarli har doim zarar: u obyektlarni sun'iy uzoq yashatadi, ular old hududga promote bo'ladi. Pool faqat qimmat resurs uchun o'rinli: connection, thread, katta direct buffer.

## 10.12 Amalda qo'llash

- [ ] Har bir servis uchun GC ni aniq belgilang: 4 vCPU dan kam bo'lsa Serial yoki Parallel, oddiy REST servisga `-XX:+UseG1GC`, qattiq p99 SLA uchun generational ZGC.
- [ ] `-Xmx` konteyner limitiga teng yozilgan joylarni `-XX:MaxRAMPercentage=70.0` ga o'tkazing va `InitialRAMPercentage` ni ham shu qiymatga qo'ying.
- [ ] Barcha prod profillarda `-Xlog:gc*:file=...:filecount=10,filesize=20M` ni yoqing, `-XX:+HeapDumpOnOutOfMemoryError` bilan `HeapDumpPath` ni persistent volume ga yo'naltiring.
- [ ] `jvm.gc.pause`, `jvm.gc.memory.allocated` va after-GC heap metrikalarini dashboard ga chiqarib, GC CPU ulushi 10 foizdan oshganda alert qo'ying.
- [ ] `MaxMetaspaceSize` va `MaxDirectMemorySize` ni har servisda aniq belgilang, reactive stack bo'lsa `io.netty.maxDirectMemory` ni ham sozlang.
- [ ] Eng katta trafikli servisda 120 sekundlik JFR profili oling va `ObjectAllocationSample` bo'yicha top 5 allokatsiya manbasiga ticket yarating.
- [ ] Butun jadvalni yoki faylni xotiraga yuklaydigan kodlarni pagination yoki stream ga o'tkazib humongous allokatsiyani yo'qoting.
- [ ] Yuklama testiga GC regressiya tekshiruvini qo'shing: release dan oldin va keyin p99 pauza va after-GC qoldiqni solishtirib, farq 20 foizdan oshsa to'xtating.

---

[&larr; 9. JVM ichki tuzilishi: class loading, memory model, JIT](09-jvm-ichki-tuzilishi-class-loading-memory.md) · [Mundarija](README.md) · [11. Concurrency: thread, lock, atomic, happens-before &rarr;](11-concurrency-thread-lock-atomic-happens.md)
