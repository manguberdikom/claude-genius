<!-- doc: architect | chapter: 31 | part: V. Atrof ekotizim: operatsion haqiqat -->

[Barcha hujjatlar](../../README.md) / [Arxitektor miyasi](README.md)

> Holat: tekshirilgan (2026-10-19). Manbalar bob oxirida.

# 31. Deployment haqiqati: konteyner, cgroup, JVM va probe (Deployment Reality)

<details>
<summary>Bu bobdagi 14 bo'lim</summary>

- [31.1 Konteyner nima va nima emas](#311-konteyner-nima-va-nima-emas)
- [31.2 JVM konteyner limitlarini qanday ko'radi](#312-jvm-konteyner-limitlarini-qanday-koradi)
- [31.3 Xotira limiti: heap, metaspace, thread stack va native xotira yig'indisi](#313-xotira-limiti-heap-metaspace-thread-stack-va-native-xotira-yigindisi)
- [31.4 CPU limiti va throttling: nega latency kutilmaganda oshadi](#314-cpu-limiti-va-throttling-nega-latency-kutilmaganda-oshadi)
- [31.5 Image qurish: qatlamlarni to'g'ri tartiblash, hajmni kamaytirish, bazaviy image tanlash](#315-image-qurish-qatlamlarni-togri-tartiblash-hajmni-kamaytirish-bazaviy-image-tanlash)
- [31.6 Liveness, readiness va startup probe farqi va noto'g'ri sozlashning oqibati](#316-liveness-readiness-va-startup-probe-farqi-va-notogri-sozlashning-oqibati)
- [31.7 Ishga tushish va to'xtash: SIGTERM, graceful shutdown, terminationGracePeriodSeconds](#317-ishga-tushish-va-toxtash-sigterm-graceful-shutdown-terminationgraceperiodseconds)
- [31.8 Rolling update, maxSurge va maxUnavailable ta'siri](#318-rolling-update-maxsurge-va-maxunavailable-tasiri)
- [31.9 Resurs so'rovi (request) va limiti: qanday hisoblanadi](#319-resurs-sorovi-request-va-limiti-qanday-hisoblanadi)
- [31.10 Konfiguratsiya va maxfiy ma'lumotlarni konteynerga berish](#3110-konfiguratsiya-va-maxfiy-malumotlarni-konteynerga-berish)
- [31.11 Gorizontal masshtablash: holatsizlik sharti va sessiya muammosi](#3111-gorizontal-masshtablash-holatsizlik-sharti-va-sessiya-muammosi)
- [31.12 Ishga tushish vaqti va avtomatik masshtablashning bog'liqligi](#3112-ishga-tushish-vaqti-va-avtomatik-masshtablashning-bogliqligi)
- [31.13 JVM ning o'zi qanday to'xtaydi: daemon thread, shutdown hook va `halt`](#3113-jvm-ning-ozi-qanday-toxtaydi-daemon-thread-shutdown-hook-va-halt)
- [31.14 Amalda qo'llash](#3114-amalda-qollash)

</details>



Lokalda ishlagan servis production'da boshqacha yashaydi. U cgroup bilan chegaralangan, orkestrator tomonidan har qanday paytda o'ldirilishi mumkin, va uning sog'ligi haqida qaror HTTP probe orqali chiqariladi. Arxitektor uchun deployment YAML fayl to'ldirish emas, balki JVM, kernel va orkestrator o'rtasidagi shartnomani tushunishdir. Bu bobda to'lov servisi va buyurtma servisi misolida shu shartnomaning har bir bandi ochiladi.

## 31.1 Konteyner nima va nima emas

Konteyner virtual mashina emas. U bitta Linux kernel ustida ishlaydigan oddiy process, atrofi ikki mexanizm bilan o'ralgan. Birinchisi namespace: process o'zining PID jadvalini, mount daraxtini, tarmoq interfeysini va hostname'ini ko'radi. Ikkinchisi cgroup: process guruhiga xotira, CPU, I/O va PID soni bo'yicha limit qo'yiladi.

Shundan kelib chiqadigan amaliy xulosalar bor. Konteyner ichidagi kernel versiyasi host kernel versiyasi bilan bir xil. Konteyner ichidagi `uname -r` host yadrosini ko'rsatadi, va ba'zi `/proc` fayllari hali ham hostning global qiymatini beradi. Konteyner "yengil" bo'lishining sababi ham shu: alohida kernel yuklanmaydi, boot jarayoni yo'q, faqat process ishga tushadi.

Image esa o'qish uchun mo'ljallangan qatlamlar to'plami. Har bir `RUN`, `COPY` yoki `ADD` yangi qatlam yaratadi, qatlamlar content hash bilan identifikatsiya qilinadi. Konteyner ishga tushganda ustiga bitta yoziladigan qatlam qo'shiladi, va u konteyner o'chganda yo'qoladi. Shu sababli konteyner ichidagi fayl tizimiga yozilgan hisobot fayli pod restart bo'lganda yo'qoladi.

```bash
# cgroup v2 da limitlarni konteyner ichidan o'qish
cat /sys/fs/cgroup/memory.max        # bayt yoki "max" (limit yo'q)
cat /sys/fs/cgroup/memory.current    # hozirgi real foydalanish
cat /sys/fs/cgroup/cpu.max           # "quota period", masalan "200000 100000"
cat /sys/fs/cgroup/pids.max          # thread va process soni chegarasi

# cgroup v1 da yo'llar boshqacha bo'ladi
cat /sys/fs/cgroup/memory/memory.limit_in_bytes
cat /sys/fs/cgroup/cpu/cpu.cfs_quota_us
```

Bu to'rt faylni bilish kerak, chunki JVM ham aynan shularni o'qiydi. Agar diagnostika paytida JVM noto'g'ri heap tanlagan bo'lsa, birinchi qadam shu qiymatlarni ko'rish.

## 31.2 JVM konteyner limitlarini qanday ko'radi

Java 10 dan boshlab JVM cgroup limitlarini o'zi aniqlaydi, bu `-XX:+UseContainerSupport` flagi bilan boshqariladi va u sukut bo'yicha yoqilgan. JVM ikki narsani cgroup'dan oladi: mavjud xotira va mavjud CPU soni. Ikkinchisi ko'pincha e'tibordan chetda qoladi, lekin ta'siri kattaroq.

Xotira uchun `-Xmx` emas, `-XX:MaxRAMPercentage` ishlatilsin. Sababi oddiy: `-Xmx` qattiq raqam, limit o'zgarganda u o'zgarmaydi. Foiz esa limitga moslashadi, demak bitta image bir xil sozlama bilan 512Mi va 2Gi podlarda ishlaydi. Amalda 60 dan 75 foizgacha oraliq tanlanadi, qolgan qismi JVM'ning heap'dan tashqari ehtiyojlariga ketadi.

```bash
# Kichik pod uchun (limit 1Gi): heap taxminan 640Mi
JAVA_TOOL_OPTIONS="-XX:MaxRAMPercentage=62.5 -XX:InitialRAMPercentage=62.5"

# Katta pod uchun (limit 4Gi): heap taxminan 3Gi, overhead nisbatan kichik
JAVA_TOOL_OPTIONS="-XX:MaxRAMPercentage=75 -XX:InitialRAMPercentage=75"

# JVM nimani ko'rganini tekshirish
java -XX:+PrintFlagsFinal -version | grep -E 'MaxHeapSize|ActiveProcessor'
java -Xlog:gc+init -version | head -20
```

`InitialRAMPercentage` ni `MaxRAMPercentage` ga teng qilish heap'ning asta o'sishini yo'q qiladi. Bu startup paytida GC ishini kamaytiradi va birinchi so'rovlar latency'sini pasaytiradi. Konteynerda xotira allaqachon ajratilgan, uni tejashdan foyda yo'q.

CPU tomonida JVM `cpu.max` dagi quota va period nisbatini olib, uni butun songa yaxlitlaydi. Agar limit 500m bo'lsa, JVM bitta processor ko'radi. Bu bitta son juda ko'p narsani belgilaydi: GC thread soni, JIT compiler thread soni, `ForkJoinPool.commonPool()` kattaligi, Netty event loop soni va Tomcat acceptor xatti harakati. Bitta yadroda G1 sukut bo'yicha serial rejimga yaqin ishlaydi, va GC pauzalari sezilarli uzayadi.

Shu sababli CPU limitini 1 dan past qo'yish JVM servis uchun deyarli har doim xato. Minimal amaliy qiymat 1000m, normal web servis uchun 2000m dan boshlanadi. Agar yadro sonini qo'lda boshqarish kerak bo'lsa, `-XX:ActiveProcessorCount` bor, lekin u limitdan kattaroq qilib qo'yilsa throttling kuchayadi.

## 31.3 Xotira limiti: heap, metaspace, thread stack va native xotira yig'indisi

Container OOM kill heap to'lganida emas, processning jami RSS limitdan oshganida sodir bo'ladi. Shuning uchun `-Xmx` ni limitga teng qilish eng tez yo'l bilan 137 exit code'ga olib keladi. Jami xotirani komponentlar yig'indisi sifatida hisoblash kerak.

Tarkibiy qismlar quyidagilar. Heap: `-Xmx` yoki `MaxRAMPercentage` bilan belgilanadi. Metaspace: Spring ilovasi uchun odatda 100Mi dan 250Mi, proxy sinflari va bytecode generatsiyasi ko'p bo'lsa yuqori. Code cache: JIT kompilyatsiya natijasi, taxminan 100Mi dan 240Mi. Thread stack: har bir platform thread uchun `-Xss` qiymati, sukut bo'yicha 1Mi, 200 thread 200Mi beradi. GC metadata va card table: heap hajmining taxminan 5 foizi. Direct buffer: Netty, WebClient va fayl I/O uchun ajratiladi, uning chegarasi `-XX:MaxDirectMemorySize` bilan qo'yiladi. Metrika va JDBC driver bufferlari ham shu yerga qo'shiladi.

```bash
# Native Memory Tracking bilan haqiqiy taqsimotni ko'rish
# 1-qadam: JVM ni shu flag bilan ishga tushirish
-XX:NativeMemoryTracking=summary

# 2-qadam: ishlayotgan podda hisobot olish
kubectl exec -it payment-7f9c-xkm2 -- jcmd 1 VM.native_memory summary scale=MB

# Chiqishdagi muhim qatorlar: Java Heap, Class (metaspace),
# Thread, Code, GC, Compiler, Internal, Other

# RSS bilan taqqoslash: NMT yig'indisi RSS dan kichik bo'lishi normal
kubectl exec -it payment-7f9c-xkm2 -- cat /proc/1/status | grep VmRSS
```

Amaliy formula: limit = heap + 250Mi (metaspace va code cache) + thread soni × 1Mi + 150Mi (GC va boshqa native) + 100Mi zahira. 1Gi limitli pod uchun bu taxminan 450Mi heap qoldiradi, agar thread soni 150 atrofida bo'lsa.

Thread sonining ikkinchi, operatsion tomoni ham bor va u xotira hisobidan tashqarida. *Software Engineering at Google* Borg da 2011 yilda topilgan izolyatsiya nosozligini keltiradi: jarayon identifikatori (PID) maydonining tugashi (sukut bo'yicha 32 000 PID) izolyatsiya nosozligiga aylangan, va bitta replika yarata oladigan jarayon hamda thread larning umumiy soniga chegara kiritishga to'g'ri kelgan. Birinchi qadam aynan shu bo'lgan: bitta konteyner ishlata oladigan PID soniga vaqtinchalik yuqori chegara, shunda bitta thread sizdirayotgan ish butun mashinani yaroqsiz qilib qo'ya olmaydi. Shundan keyin thread va jarayon PID maydonlari ajratilgan, chunki thread larga berilgan PID lar uchun 32 000 kafolatiga kam odam tayangan edi.

Kubernetes da bu `pids` cgroup chegarasi: kubelet dagi `podPidsLimit` har pod uchun maksimal jarayon va thread sonini belgilaydi. Qoida ikki qatorda: har pod uchun PID chegarasi qo'yiladi, va chegara JVM ning kutilgan maksimal thread sonidan (Tomcat, Hikari, async executor, Kafka consumer, scheduler va GC thread lari yig'indisi) sezilarli, lekin cheksiz bo'lmagan zaxira bilan yuqori turadi. Chegarasiz qolgan pod da thread sizdirgan xato o'z pod ini emas, butun node ni ishdan chiqaradi, chunki PID maydoni node darajasida bo'lishiladi. Diagnostikada esa `ThreadMXBean` dan olingan `jvm.threads.live` metrikasi va `cat /sys/fs/cgroup/pids.current` birga o'qiladi: birinchisi JVM thread larini, ikkinchisi jarayon va native thread larni ham ko'rsatadi.

Thread soni bu yerda yashirin xavf. Tomcat `server.tomcat.threads.max` sukut bo'yicha 200, har biri Hikari connection kutishi mumkin. Agar yana async executor, Kafka consumer va scheduler thread'lari qo'shilsa, 400 thread oson yig'iladi. Bu 400Mi faqat stack uchun. Virtual thread'lar bu muammoni kamaytiradi, chunki ularning stack'i heap'da yashaydi va o'sib boradi, lekin carrier thread soni yadro soniga bog'liq qoladi.

## 31.4 CPU limiti va throttling: nega latency kutilmaganda oshadi

Linux CFS quota mexanizmi 100 millisekundli period bilan ishlaydi. Limit 500m bo'lsa, process har 100ms ichida 50ms CPU vaqti sarflashi mumkin. Agar u kvotani 30ms da tugatsa, qolgan 70ms davomida butunlay to'xtatiladi. Bu to'xtash GC ishlayotgan paytga tushsa, bitta so'rov latency'si yuzlab millisekundga ko'tariladi.

Shuning uchun throttling o'rtacha CPU foydalanish pastligida ham sodir bo'ladi. Dashboard'da CPU 20 foizda ko'rinadi, lekin p99 latency 800ms. Sababi: burst kerak bo'lgan qisqa lahzalarda kvota tugaydi. Buni faqat throttling metrikasi ko'rsatadi.

```bash
# Throttling faktini aniqlash
cat /sys/fs/cgroup/cpu.stat
# nr_periods        : jami period soni
# nr_throttled      : qancha periodda to'xtatilgan
# throttled_usecs   : jami to'xtab turilgan mikrosekund

# nr_throttled / nr_periods nisbati 0.05 dan oshsa muammo bor
# throttled_usecs o'sish tezligini Prometheus da kuzatish:
#   container_cpu_cfs_throttled_seconds_total
```

Arxitektor qarori shunday bo'ladi. Latency sezgir servislar uchun CPU limitini request'dan sezilarli yuqori qo'yish yoki umuman qo'ymaslik. Limit yo'q bo'lsa pod Burstable QoS da qoladi va bo'sh CPU'dan foydalanadi, lekin nodega qo'shni podlar uchun xavf tug'diradi. Shu sababli ko'p tashkilot oraliq yechim tanlaydi: request 1000m, limit 2000m. Batch va hisobot generatsiya qiladigan servislarda esa limit qat'iy bo'lishi to'g'ri, chunki ular latency emas throughput bilan o'lchanadi.

Startup paytidagi throttling alohida muammo. JIT hali kodni kompilyatsiya qilmagan, Spring context quriladi, va bu bosqich CPU'ga juda och. Agar limit past bo'lsa startup 40 sekunddan 3 minutga cho'ziladi. Yechim: startup probe'ga keng muhlat berish, yoki JDK 24 dan boshlab mavjud AOT cache mexanizmini qo'llash.

## 31.5 Image qurish: qatlamlarni to'g'ri tartiblash, hajmni kamaytirish, bazaviy image tanlash

Fat jar'ni bitta `COPY` bilan image'ga qo'yish eng keng tarqalgan xato. Kodning bitta qatori o'zgarsa 60Mi qatlam butunlay qaytadan yuklanadi. Spring Boot buni hal qilish uchun layered jar formatini beradi: dependency, spring-boot-loader, snapshot dependency va application qatlamlari ajratilgan.

```bash
# 1-bosqich: layered jar ni ochish (Spring Boot 3.3+ sintaksisi)
# FROM eclipse-temurin:21-jre-alpine AS builder
# WORKDIR /app
# COPY target/payment-service.jar app.jar
# RUN java -Djarmode=tools -jar app.jar extract --layers --destination extracted

# 2-bosqich: qatlamlarni o'zgarish tezligi bo'yicha tartiblash
# FROM eclipse-temurin:21-jre-alpine
# WORKDIR /app
# COPY --from=builder /app/extracted/dependencies/ ./
# COPY --from=builder /app/extracted/spring-boot-loader/ ./
# COPY --from=builder /app/extracted/snapshot-dependencies/ ./
# COPY --from=builder /app/extracted/application/ ./
# USER 1000:1000
# ENTRYPOINT ["java", "-XX:MaxRAMPercentage=70", "org.springframework.boot.loader.launch.JarLauncher"]
```

Tartib qoidasi bitta: kam o'zgaradigan narsa pastda, tez o'zgaradigan narsa yuqorida. Dependency qatlami haftalarda bir marta o'zgaradi, application qatlami har commit'da. Shunda har deploy'da registry'ga 2Mi dan 5Mi gacha yuklanadi, 60Mi emas.

Bazaviy image tanlashda uch variant bor. JRE asosidagi Alpine image taxminan 180Mi beradi, lekin musl libc ba'zi native kutubxonalar bilan muammo tug'diradi. Debian asosidagi slim image kattaroq, taxminan 250Mi, lekin glibc bilan ishlaydi. Distroless image eng kichik hujum yuzasini beradi, lekin ichida shell yo'q, demak `kubectl exec` bilan debug qilish imkonsiz. Oxirgi variantda ephemeral debug container mexanizmidan foydalanish kerak.

`jlink` bilan maxsus runtime qurish image hajmini 100Mi gacha tushiradi. Lekin Spring ilovada modul grafi to'liq aniq bo'lmaydi, shuning uchun bu usul murakkab. Odatda foyda arzimas, chunki qatlam cache bilan tarmoq trafigi allaqachon kichik.

## 31.6 Liveness, readiness va startup probe farqi va noto'g'ri sozlashning oqibati

Uch probe uch xil savolga javob beradi. Startup probe: "ishga tushish tugadimi". Readiness probe: "trafikni qabul qila olamanmi". Liveness probe: "meni o'ldirib qayta ishga tushirish kerakmi". Ularni aralashtirib yuborish production'da eng og'riqli incident'larni keltiradi.

Eng xavfli xato: liveness probe'ni ma'lumotlar bazasiga bog'lash. Baza 30 sekundga javob bermay qolsa, barcha podlar liveness'dan o'tmaydi, kubelet hammasini o'ldiradi, va baza tiklanganda butun cluster bo'sh bo'lib qoladi. Liveness faqat process ichki holatini tekshirishi kerak: event loop tirikmi, deadlock yo'qmi. Tashqi bog'liqliklar faqat readiness'ga kiradi.

```yaml
# Spring Boot actuator bilan to'g'ri sozlangan probe'lar
startupProbe:
  httpGet: { path: /actuator/health/readiness, port: 8080 }
  periodSeconds: 5
  failureThreshold: 30          # 150 sekundgacha startup ga ruxsat
readinessProbe:
  httpGet: { path: /actuator/health/readiness, port: 8080 }
  periodSeconds: 5
  timeoutSeconds: 3
  failureThreshold: 3            # 15 sekunddan keyin trafikdan chiqadi
livenessProbe:
  httpGet: { path: /actuator/health/liveness, port: 8080 }
  periodSeconds: 10
  timeoutSeconds: 3
  failureThreshold: 3            # faqat jiddiy holatda restart
```

Startup probe ning ikkita xulqi ko'pincha e'tibordan qoladi. Birinchi: startup probe e'lon qilingan bo'lsa, Kubernetes u muvaffaqiyatli tugamaguncha liveness va readiness probe larini **umuman bajarmaydi**. Shuning uchun sekin ko'tariladigan JVM ilovasi uchun to'g'ri yo'l liveness ning `initialDelaySeconds` ini cho'zish emas, startup probe qo'yish. Ikkinchi: startup probe yiqilsa, kubelet konteynerni o'ldiradi, ya'ni `failureThreshold` × `periodSeconds` ko'tarilish uchun real kerak bo'lgan vaqtdan katta bo'lishi shart.

Spring tomonida bu `management.endpoint.health.probes.enabled=true` bilan yoqiladi, Kubernetes aniqlangan muhitda avtomatik ham ishlaydi. Baza health indicator readiness guruhiga qo'shiladi, liveness guruhi esa bo'sh qoldiriladi.

```properties
# Probe guruhlarini aniq boshqarish
management.endpoint.health.probes.enabled=true
management.endpoint.health.group.readiness.include=readinessState,db,redis
management.endpoint.health.group.liveness.include=livenessState
management.endpoint.health.show-details=when-authorized

# Graceful shutdown va uning muhlati
server.shutdown=graceful
spring.lifecycle.timeout-per-shutdown-phase=25s

# Hikari pool: thread sonidan emas, baza sig'imidan kelib chiqib
spring.datasource.hikari.maximum-pool-size=15
spring.datasource.hikari.connection-timeout=3000
```

Startup probe mavjud bo'lsa, liveness probe faqat startup tugagandan keyin ishlaydi. Shuning uchun `initialDelaySeconds` ni liveness'da katta qilish shart emas. Startup probe yo'q bo'lsa va startup 90 sekund davom etsa, liveness podni cheksiz restart qiladi va deployment hech qachon tugamaydi.

| Tuzoq | Nima sodir bo'ladi | Yechim |
| --- | --- | --- |
| Liveness baza holatini tekshiradi | Baza uzilsa butun cluster restart bo'ladi | Bazani faqat readiness guruhiga qo'shish |
| `-Xmx` limitga teng qo'yilgan | Native xotira hisobga olinmaydi, exit 137 | `MaxRAMPercentage=70` va NMT bilan tekshirish |
| CPU limit 500m | GC bitta threadda, p99 latency uch barobar | Limitni 1000m dan yuqori qilish |
| Startup probe yo'q | Sekin startup liveness tomonidan uzilib ketadi | `failureThreshold` 30 bilan startup probe |
| `preStop` hook yo'q | Load balancer hali yuborayotganda port yopiladi | 5 sekundli `preStop sleep` qo'shish |
| `terminationGracePeriodSeconds` 30, shutdown 60s | SIGKILL tranzaksiyani yarmida uzadi | Grace period'ni shutdown timeout'dan katta qilish |
| Readiness o'z servisining `/health` ini chaqiradi | Cheklangan thread pool o'zini o'zi bloklaydi | Probe'ni yengil va bog'liqliksiz qilish |
| Fat jar bitta qatlamda | Har deploy'da 60Mi registry trafigi | Layered jar va to'rt qatlamli `COPY` |

## 31.7 Ishga tushish va to'xtash: SIGTERM, graceful shutdown, terminationGracePeriodSeconds

Pod o'chirilganda kubelet konteynerga `SIGTERM` yuboradi va `terminationGracePeriodSeconds` kutadi, sukut bo'yicha 30 sekund. Muhlat tugasa `SIGKILL` keladi va uni ushlab qolish mumkin emas. Shu 30 sekund ichida ilova ishni toza tugatishi kerak.

Tartib aniq va uni bilish `preStop` ni to'g'ri yozish uchun kerak. Kubelet avval `preStop` hook ni ishga tushiradi, **keyin** konteyner ichidagi 1-process ga TERM yuboradi. Ikki shart bor: `terminationGracePeriodSeconds` 0 ga qo'yilgan bo'lsa, `preStop` umuman ishlamaydi; hook muhlat tugaganda hali ishlayotgan bo'lsa, kubelet faqat bir martalik 2 sekund qo'shimcha so'raydi, undan ortiq emas. Demak hook ga kerakli vaqt grace period ichiga sig'ishi kerak, aks holda uni cheklash foydasiz.

Ko'p konteynerli pod da yana bir nozik joy bor: sidecar container e'lon qilinmagan bo'lsa, konteynerlar TERM ni turli vaqtda va **ixtiyoriy tartibda** oladi. Ya'ni ilova o'z yonidagi proxy yoki agent dan oldin o'lishiga kafolat yo'q. To'xtash tartibi muhim bo'lsa, uni `preStop` bilan sinxronlash yoki sidecar container ga o'tish kerak.

Muhim nuance bor: endpoint'ni Service'dan olib tashlash va SIGTERM yuborish parallel sodir bo'ladi. Ya'ni SIGTERM kelganda load balancer hali bir necha so'rov yuborishi mumkin. Shu sababli `preStop` hook'da qisqa kutish qo'yiladi. Bu vaqtda ilova hali so'rovlarga javob beradi, lekin endpoint ro'yxatdan chiqib bo'lgan.

```yaml
spec:
  terminationGracePeriodSeconds: 45     # shutdown timeout dan katta
  containers:
    - name: payment
      lifecycle:
        preStop:
          exec:
            command: ["sh", "-c", "sleep 5"]   # LB propagatsiyasi uchun
      resources:
        requests: { cpu: "1000m", memory: "1Gi" }
        limits:   { cpu: "2000m", memory: "1Gi" }
      env:
        - name: JAVA_TOOL_OPTIONS
          value: "-XX:MaxRAMPercentage=65 -XX:InitialRAMPercentage=65
                  -XX:+ExitOnOutOfMemoryError -Xlog:gc*:file=/dev/stdout"
```

`server.shutdown=graceful` yoqilganda Spring Boot yangi so'rovlarni qabul qilmaydi, lekin ishlayotganlarini `spring.lifecycle.timeout-per-shutdown-phase` ichida tugatadi. Bu muhlat `terminationGracePeriodSeconds` dan kichik bo'lishi shart, aks holda SIGKILL o'rtada keladi. Kafka consumer va scheduler uchun shu bosqichda `@PreDestroy` yoki `SmartLifecycle` orqali toza to'xtash yozilishi kerak.

```java
// Uzoq davom etadigan hisobot generatsiyasini toza to'xtatish
@Component
class ReportWorker implements SmartLifecycle {

    private volatile boolean running = false;

    @Override public void start() { running = true; }

    @Override public void stop() {
        running = false;              // yangi batch olinmaydi
        // ishlayotgan batch o'zi tugaydi, flag tekshiriladi
    }

    @Override public boolean isRunning() { return running; }

    // Kechroq to'xtasin: raqam katta bo'lsa keyinroq to'xtatiladi
    @Override public int getPhase() { return Integer.MAX_VALUE - 100; }
}
```

Uzoq tranzaksiyalar alohida qaror talab qiladi. 10 minutlik hisobot generatsiyasi graceful shutdown'ga sig'maydi. Bunday ish web pod ichida emas, alohida Job yoki ishga qaytarilishi mumkin bo'lgan queue consumer sifatida bajarilishi kerak. Idempotentlik shu yerda majburiy shart bo'ladi.

## 31.8 Rolling update, maxSurge va maxUnavailable ta'siri

RollingUpdate strategiyasi ikki parametr bilan boshqariladi. `maxSurge` desired replica sonidan qancha ortiq pod yaratilishi mumkinligini belgilaydi. `maxUnavailable` qancha pod bir vaqtda yetishmasligi mumkinligini belgilaydi. Sukut qiymatlar 25 foiz va 25 foiz.

Arxitektor uchun bu sig'im masalasi. 4 replika ishlayotgan to'lov servisida `maxUnavailable: 25%` bitta podni olib tashlaydi, qolgan uchtasi har biri avvalgidan to'rtdan uch nisbatida ko'proq, ya'ni taxminan 33 foiz ko'proq trafik ko'taradi (bu o'lchov emas, 4 dan 3 ga bo'lishning arifmetikasi). Agar har bir pod allaqachon 80 foiz yuklangan bo'lsa, deploy paytida servis qulab tushadi. Shuning uchun yuqori yuklamali servislarda `maxUnavailable: 0` va `maxSurge: 1` tanlanadi. Bu deploy'ni sekinlashtiradi, lekin sig'im kamaymaydi.

`maxUnavailable: 0` qo'ysa cluster'da qo'shimcha resurs bo'lishi shart. Aks holda yangi pod `Pending` holatida qotib qoladi va deploy to'xtaydi. Shuning uchun bu qarorni node sig'imi bilan birga ko'rib chiqish kerak.

Yana bir qattiq shart: ikkisi bir vaqtda 0 bo'lmaydi. `maxUnavailable` 0 bo'lsa `maxSurge` 0 bo'la olmaydi va teskarisi, aks holda rollout qimirlay olmaydi. Foizdan sonning hisoblanishi ham ikki xil: `maxUnavailable` pastga, `maxSurge` yuqoriga yumaloqlanadi. 4 replika va 25 foiz da bu `maxUnavailable = 1` va `maxSurge = 1` beradi.

Deploy qotib qolganini qanday bilish ham sozlamada turadi. `progressDeadlineSeconds` default **600 sekund**: shu vaqt ichida rollout qimirlamasa, Deployment da `Progressing` sharti `False` va `reason: ProgressDeadlineExceeded` bilan belgilanadi, controller esa urinishni davom ettiradi. Ya'ni yomon image yoki yiqilayotgan readiness probe bilan deploy 10 daqiqa jim turadi va shundan keyin xato ko'rinadi. CI dagi deploy qadamiga shu chegaradan kichik timeout qo'yilsa, muammo tezroq ko'rinadi. Qiymat `minReadySeconds` dan katta bo'lishi shart.

Yana bir nozik joy: rolling update faqat probe'lar to'g'ri bo'lsa ishlaydi. Readiness probe `true` qaytarsa, lekin ilova hali JIT'ni qizdirmagan bo'lsa, yangi pod birinchi minutda sekin javob beradi. Bu "deploy paytida latency spike" deb nomlanadi. Yechim: readiness'dan oldin kichik warmup qilish, yoki `minReadySeconds` qo'yib podning trafikka kirishini kechiktirish.

Baza sxemasi migratsiyasi rolling update bilan to'qnashadi. Deploy paytida eski va yangi versiya bir vaqtda ishlaydi, demak sxema ikkalasiga ham mos bo'lishi shart. Ustun o'chirish uch deploy'ga bo'linadi: avval kod ustunni ishlatmay qo'yadi, keyin ustun nullable bo'ladi, oxirida o'chiriladi.

## 31.9 Resurs so'rovi (request) va limiti: qanday hisoblanadi

Request scheduler uchun, limit kernel uchun. Scheduler podni nodega joylashtirishda faqat request'ga qaraydi. Kernel esa limit'ni majburlaydi. Bu ikkisi QoS sinfini belgilaydi: teng bo'lsa Guaranteed, request kichik bo'lsa Burstable, ikkisi ham yo'q bo'lsa BestEffort. Node xotira bosimida BestEffort birinchi, Burstable keyin evict qilinadi.

Xotira uchun qoida: request va limit teng bo'lsin. Sababi JVM xotirani qaytarib bermaydi, demak "kerak bo'lganda ko'proq olish" degan model ishlamaydi. Teng qiymat Guaranteed QoS beradi va evict xavfini kamaytiradi. CPU uchun esa request va limit farqli bo'lishi odatda to'g'ri, chunki JVM startup va GC burst'lari qisqa.

Raqamni qanday topish kerak. Birinchi qadam: load test ostida bir hafta ishlatib, p95 CPU va maksimal RSS o'lchanadi. Request = p95 CPU × 1.2. Limit = request × 2. Xotira limiti = kuzatilgan maksimal RSS × 1.25. Keyin NMT hisoboti bilan taqsimot tekshiriladi va heap foizi moslashtiriladi.

| Vaziyat | Oddiy yondashuv | Arxitektor yondashuvi |
| --- | --- | --- |
| Heap sozlash | `-Xmx512m` qattiq yoziladi | `MaxRAMPercentage` bilan limitga bog'lanadi |
| Xotira limiti | Heap bilan bir xil qo'yiladi | Heap plus metaspace, stack, native va zahira |
| CPU limiti | 500m qo'yib "tejash" | 1000m dan yuqori, throttling metrikasi kuzatiladi |
| Probe'lar | Bitta `/health` uch probe uchun | Liveness ichki, readiness tashqi, startup alohida |
| Shutdown | SIGTERM ushlanmaydi, 30s kutiladi | Graceful shutdown plus `preStop` plus grace period |
| Image | Fat jar bitta `COPY` bilan | Layered jar, to'rt qatlam, non-root user |
| Deploy strategiyasi | Sukut 25 foiz qoldiriladi | Sig'im hisobidan `maxUnavailable` tanlanadi |
| Sxema migratsiyasi | Kod bilan birga bitta deploy | Orqaga mos uch bosqichli ketma ketlik |
| Sessiya | Sticky session sozlanadi | Holat tashqi store'ga chiqariladi |
| Masshtablash | HPA 70 foiz CPU bilan yoqiladi | Startup vaqti o'lchanib, metrika va zahira moslashtiriladi |

## 31.10 Konfiguratsiya va maxfiy ma'lumotlarni konteynerga berish

Image ichiga parol yozish mumkin emas, bu qoida muhokama qilinmaydi. Image har qanday registry'ga tushadi va qatlamlari o'qiladi. Konfiguratsiya tashqaridan keladi, ikki yo'l bilan: environment variable yoki mount qilingan fayl.

Environment variable oddiy, lekin kamchiliklari bor. U process boshlanganda o'qiladi, demak sekret aylanganda pod restart kerak. Yana u `/proc/1/environ` da ko'rinadi va crash dump'ga tushishi mumkin. Fayl sifatida mount qilingan Secret esa kubelet tomonidan yangilanadi, va Spring `configtree` mexanizmi uni fayl tizimidan o'qiydi.

```properties
# Secret volume /etc/secrets ga mount qilingan bo'lsa
spring.config.import=optional:configtree:/etc/secrets/
# Fayl nomi property nomiga aylanadi:
#   /etc/secrets/spring.datasource.password  ->  spring.datasource.password

# ConfigMap dan profil va yaml ni olish
spring.config.additional-location=optional:file:/etc/config/

# Sekret log ga tushmasligi uchun
management.endpoint.env.show-values=never
management.endpoint.configprops.show-values=never
```

Qaror darajasida: baza paroli, API kaliti va signing key Secret'da, timeout, pool kattaligi va feature flag ConfigMap'da. Vault yoki cloud secret manager ishlatilsa, pod init container bilan sekretni fayl tizimiga yozadi yoki sidecar orqali oladi. Har holda ilova kodi faqat property o'qiydi, qaysi manbadan kelganini bilmasligi kerak.

## 31.11 Gorizontal masshtablash: holatsizlik sharti va sessiya muammosi

Gorizontal masshtablash faqat bir shart bilan ishlaydi: pod ichida muhim holat saqlanmasligi. Buzilish uch joyda sodir bo'ladi. Birinchisi HTTP sessiya: foydalanuvchi savati pod xotirasida saqlansa, pod o'chganda savat yo'qoladi. Ikkinchisi lokal cache: har podda boshqa qiymat bo'ladi va foydalanuvchi har so'rovda boshqa javob oladi. Uchinchisi fayl tizimi: yuklangan hujjat bitta podda qoladi.

Sticky session bu muammoni yashiradi, lekin hal qilmaydi. Pod o'chganda unga bog'langan foydalanuvchilar hammasi holatini yo'qotadi. Rolling update esa barcha podlarni almashtiradi, demak har deploy'da barcha sessiya uziladi. To'g'ri yechim holatni tashqariga chiqarish: sessiya Redis'da, fayl object storage'da, cache esa ikki qatlamli bo'lib lokal qatlam qisqa TTL bilan ishlaydi.

Scheduler ham e'tibor talab qiladi. `@Scheduled` metod har podda ishlaydi, demak 4 replikada hisobot 4 marta generatsiya qilinadi. Yechim variantlari: bazada lock olish, ShedLock turidagi mexanizm, yoki ishni alohida CronJob'ga chiqarish. Oxirgi variant eng toza, chunki u web pod hayot siklidan ajralgan.

```sql
-- Bazadagi lock bilan bitta pod ishlashini kafolatlash
-- Advisory lock tranzaksiya oxirida o'zi bo'shaydi
SELECT pg_try_advisory_xact_lock(hashtext('daily_settlement_report'));

-- Agar true qaytsa, shu pod ishni bajaradi; false bo'lsa chiqib ketadi.
-- Bu usul alohida jadval va tozalash mantiqini talab qilmaydi.

-- Buyurtma holatini yangilashda ham bir xil qoida ishlaydi:
-- ikki pod bitta qatorni o'zgartirmasligi uchun optimistik versiya
UPDATE orders
   SET status = 'SHIPPED', version = version + 1
 WHERE id = $1 AND version = $2;
-- 0 qator yangilangan bo'lsa, boshqa pod allaqachon o'zgartirgan
```

## 31.12 Ishga tushish vaqti va avtomatik masshtablashning bog'liqligi

HPA yuklamaga javoban yangi pod yaratadi, lekin pod trafikka kirishi uchun startup tugashi kerak. Agar Spring ilovasi 60 sekundda ishga tushsa, HPA'ning reaksiyasi amalda bir daqiqa kechikadi. Trafik spike 30 sekund davom etsa, yangi pod spike tugaganda tayyor bo'ladi. Bu masshtablashni foydasiz qiladi.

Shu sababli startup vaqti arxitektura ko'rsatkichi. Uni qisqartirishning amaliy yo'llari bor. Birinchisi lazy initialization'dan voz kechish va kerakli bean'larni kamaytirish: `spring.main.lazy-initialization=true` startup'ni tezlashtiradi, lekin birinchi so'rov latency'sini oshiradi, shuning uchun u faqat dev uchun. Ikkinchisi auto configuration sonini kamaytirish, chunki har bir starter classpath skanerlash qo'shadi. Uchinchisi Class Data Sharing arxivi: Spring Boot 3.3 dan boshlab buning uchun qulay mexanizm bor va startup sezilarli tezlashadi; aniq ulushni bu yerda bermaymiz, chunki u bean soni va classpath hajmiga bog'liq va `-verbose:class` hamda startup vaqtini o'lchab solishtirish bilan aniqlanadi. To'rtinchisi JDK 24 dan paydo bo'lgan AOT cache. Beshinchisi GraalVM native image, u startup'ni 100 millisekundga tushiradi, lekin reflection konfiguratsiyasi va build vaqti narxi bilan keladi.

```yaml
# HPA: startup vaqti hisobga olingan sozlama
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
spec:
  minReplicas: 4                 # spike uchun zahira sig'im
  maxReplicas: 20
  metrics:
    - type: Resource
      resource:
        name: cpu
        target: { type: Utilization, averageUtilization: 60 }
  behavior:
    scaleUp:
      stabilizationWindowSeconds: 0      # tez ko'tarilish
      policies:
        - type: Percent
          value: 100
          periodSeconds: 30
    scaleDown:
      stabilizationWindowSeconds: 300    # sekin tushish, flapping bo'lmasin
```

Agar startup'ni tezlashtirish imkoni bo'lmasa, qaror boshqa tomondan keladi: `minReplicas` ni oshirib doimiy zahira sig'im ushlab turish. Bu pul turadi, lekin ishonchli. Target utilization'ni 60 foizga tushirish ham shu maqsadga xizmat qiladi, chunki podlar spike'ni o'zi ko'tarishga joy qoldiradi. Bu yerda ehtiyotkorlik patternlari kerak bo'lsa, dizayn [patternlar hujjatidagi](../patterns/README.md) resilience bo'limiga qaralsin.

## 31.13 JVM ning o'zi qanday to'xtaydi: daemon thread, shutdown hook va `halt`

[Graceful shutdown](#317-ishga-tushish-va-toxtash-sigterm-graceful-shutdown-terminationgraceperiodseconds) bo'limi orkestrator bilan ilova o'rtasidagi shartnomani yozadi. Uning ostida yana bir qatlam bor: SIGTERM ni Spring ushlagandan keyin ham JVM processi o'z qoidalari bo'yicha o'ladi, va bu qoidalar `terminationGracePeriodSeconds` ga bo'ysunmaydi. Shu qatlamni bilmaslik ikki aniq nosozlik beradi: pod grace period ni to'liq kutib o'tirib keyin SIGKILL olish, va `finally` blokidagi tozalash kodi hech qachon ishlamasligi.

Spetsifikatsiya chiqish yo'llarini sanab beradi (*The Java Language Specification, Java SE 25*, 12.8, 461-462-betlar): dastur barcha **daemon bo'lmagan** threadlari tugaganda chiqadi, yoki thread `System.exit` / `Runtime.exit` chaqirganda, yoki JVM realizatsiyasi OS signalini to'xtash so'rovi deb tan olganda; uch holatda ham shu sababli ishga tushgan shutdown hook lar tugashi kutiladi. `Runtime.halt` esa alohida: unda hook lar **umuman ishga tushmaydi**. JCiP shu ikki guruhni tartibli (orderly) va to'satdan (abrupt) to'xtash deb ajratadi, `SIGKILL` bilan process o'ldirishni ikkinchi guruhga qo'yadi (Goetz, 7.4, 102-bet).

Daemon va daemon bo'lmagan thread faqat bitta narsada farq qiladi: ular tugaganda nima bo'ladi. Platform thread uchun yangi thread o'zini yaratgan threadning daemon statusini meros qilib oladi, demak `main` dan yaratilgan hamma platform thread sukut bo'yicha daemon emas. Virtual thread da bu meros qoidasi amal qilmaydi, va farqi executor misolidan keyin yoziladi. JVM thread tugaganini ko'rib qolgan threadlarni sanaydi va faqat daemon lar qolsa tartibli to'xtashni boshlaydi (Goetz, 7.4.2, 103-bet). Chiqish paytidagi qoida qat'iy: hali tugamagan har qanday thread, daemon bo'ladimi yo'qmi, boshqa Java kodini bajarmaydi, uning joriy metodi na normal na abrupt tugaydi, **hech bir `finally` bandi ishlamaydi** va uncaught exception handler ham chaqirilmaydi (JLS 12.8, 462-bet). Shuning uchun fayl yopish, offset commit yoki vaqtinchalik katalogni tozalash daemon threadning `finally` bandiga ishonib topshirilmaydi.

Amaliy oqibat executor da ko'rinadi. Pool thread lari sukut bo'yicha daemon emas, va thread executor birinchi vazifada aynan daemon bo'lmagan thread yaratadi, shuning uchun `shutdown()` chaqirilmasa ilova hech qachon tugamaydi (Boyarsky/Selikoff, *OCP Java SE 17 Study Guide*, 13-bob, 731-bet). Konteynerda bu "SIGTERM dan keyin pod 30 sekund osilib turdi" shaklida namoyon bo'ladi.

**Yuqoridagi uch qoida platform thread uchun, virtual thread uchun emas.** Virtual thread har doim daemon, va `setDaemon` uni daemon bo'lmagan qilib o'zgartira olmaydi; uning priority si ham qotib qolgan `NORM_PRIORITY` va `setPriority` ta'sir qilmaydi (JEP 444, "Virtual Threads", "Scheduling and virtual threads" hamda "Thread API" bo'limlari). Demak virtual thread ichida meros qilish qoidasi ham ishlamaydi: `main` dan yaratilgan virtual thread yaratuvchidan daemon bo'lmaslikni meros qilib olmaydi, va JVM uni chiqish shartini hisoblashda umuman sanamaydi. Amaliy oqibati yuqoridagining teskarisi: `Executors.newVirtualThreadPerTaskExecutor()` yoki `Thread.ofVirtual().start(...)` bilan ishga tushgan ish JVM ni bir lahza ham tirik ushlab turmaydi. Pod osilib qolmaydi, buning o'rniga yarmida qolgan ish jim yo'qoladi: `main` qaytsa yoki oxirgi platform thread tugasa, hali bajarilayotgan virtual thread lar yuqoridagi JLS 12.8 qoidasi bo'yicha to'xtatiladi va ularning `finally` bandi ishlamaydi.

Shuning uchun virtual thread da ish kuzatuvchisi `setDaemon` emas, chegaradan chiqishni kutadigan konstruksiya bo'ladi: `ExecutorService` ni `try`-with-resources ichida yopish (`close()` o'zi `awaitTermination` ni kutadi), yoki `StructuredTaskScope` bilan ishni leksik chegara ichida ushlab turish. Spring tomonida `spring.threads.virtual.enabled=true` bo'lsa, ish `ApplicationContext` ning shutdown hook i ichida tugaydi, demak kafolatni hook beradi, thread turi emas.

```java
// Virtual thread daemon, shuning uchun JVM uni kutmaydi: chegarani o'zimiz ushlaymiz
void reconcileAll(List<PaymentId> ids) throws InterruptedException {
    // close() = shutdown + awaitTermination: hamma vazifa tugamaguncha qaytmaydi
    try (ExecutorService pool = Executors.newVirtualThreadPerTaskExecutor()) {
        ids.forEach(id -> pool.submit(() -> reconcile(id)));
    }
    // Bu yerga yetib kelish hamma reconcile tugaganining yagona kafolati.
    // try bloki bo'lmasa `main` qaytib ketadi va yarim ish jim yo'qoladi.
}
```

```java
// Spring boshqarmaydigan har bir executor uchun to'xtatish egasi bo'lishi kerak
@Component
class SettlementExecutor implements AutoCloseable {

    private final ExecutorService pool = Executors.newFixedThreadPool(
            4, Thread.ofPlatform().name("settlement-", 0).factory());

    public Future<?> submit(Runnable task) { return pool.submit(task); }

    @PreDestroy
    @Override
    public void close() throws InterruptedException {
        pool.shutdown();                                  // yangi vazifa qabul qilinmaydi
        if (!pool.awaitTermination(20, TimeUnit.SECONDS)) { // grace period ichida
            pool.shutdownNow();                           // qolganlariga interrupt
        }
    }
}
```

Shutdown hook lar bu tozalashning oxirgi chorasi, va ularning xulqi hisobga olinmasa ular muammo manbasiga aylanadi. JVM hook larni **qanday tartibda** ishga tushirishini kafolatlamaydi, hammasi bir vaqtda ishlaydi, va ilova threadlari shutdown jarayoni bilan parallel ishlashda davom etadi. Shundan to'rt talab chiqadi (Goetz, 7.4.1, 102-bet): hook thread-safe bo'lishi va umumiy ma'lumotga sinxronlash bilan murojaat qilishi kerak; boshqa servis allaqachon to'xtagan deb yoki JVM nima sababdan to'xtayotgani haqida taxmin qilib bo'lmaydi, shuning uchun u o'ta himoyalangan yoziladi; u imkon qadar tez chiqishi kerak, chunki uning mavjudligi JVM tugashini kechiktiradi; va u ilova yoki boshqa hook to'xtatishi mumkin bo'lgan servisga tayanmasligi kerak. Oxirgi talabning yechimi kitobda aniq: har servis uchun alohida hook o'rniga **bitta** hook yoziladi va u to'xtatish amallarini ketma-ket chaqiradi, shunda ular bitta threadda tartib bilan bajariladi va amallar orasidagi poyga ham, deadlock ham yo'qoladi.

| Holat | Hook ishlaydimi | `finally` ishlaydimi |
|---|---|---|
| Oxirgi daemon bo'lmagan thread tugadi | ha | ha, o'sha threadda |
| Oxirgi platform thread tugadi, virtual thread hali ishlayapti | ha | yo'q, virtual thread larda |
| `System.exit` / `Runtime.exit` | ha | yo'q, qolgan threadlarda |
| SIGTERM (JVM tanigan signal) | ha | yo'q, qolgan threadlarda |
| `Runtime.halt` | yo'q | yo'q |
| `SIGKILL`, OOM killer, node o'chishi | yo'q | yo'q |

Yana ikki chegara. Birinchi: hook yoki finalizer tugamasa tartibli to'xtash osilib qoladi va JVM ni to'satdan to'xtatishga to'g'ri keladi, ya'ni cheksiz kutadigan hook grace period ni o'zi yeb qo'yadi. Ikkinchi: hook lar ishlayotganda kimdir `Runtime.halt` chaqirsa, hali tugamagan hook ham boshqa Java kodini bajarmaydi (JLS 12.8, 462-bet). Shuning uchun `-XX:+ExitOnOutOfMemoryError` kabi flaglar, va `halt` chaqiradigan har qanday kutubxona, tozalash kodini o'tkazib yuborishi hisobga olinishi kerak: tashqi tizimdagi holat (Kafka offset, taqsimlangan lock, yarim yozilgan fayl) faqat shu tozalashga tayanmasligi, balki ishga tushishda tiklanadigan shaklda bo'lishi kerak.

Spring ilovasida odatiy taqsimot shunday: `ApplicationContext` ning o'z shutdown hook i `@PreDestroy` va `SmartLifecycle.stop` ni chaqiradi, demak o'z hook ingizni `Runtime.addShutdownHook` bilan qo'shish faqat konteyner boshqarmaydigan resurs uchun kerak bo'ladi. Vazifani bekor qilish va interrupt siyosatining o'zi [bekor qilish bo'limida](11-concurrency-thread-lock-atomic-happens.md#1114-bekor-qilish-interrupt-siyosati-va-thread-starvation-deadlock).

Manba: *The Java Language Specification, Java SE 25 Edition* (Gosling, Joy, Steele, Bracha, Buckley, Smith, Bierman), 12.8 (461-462-betlar); Brian Goetz va boshqalar, *Java Concurrency in Practice*, Addison-Wesley, 2006, 7.4-7.4.2-bo'lim (102-103-bet); Boyarsky/Selikoff, *OCP Java SE 17 Study Guide*, 13-bob (725-726 va 731-betlar); JEP 444, "Virtual Threads" (virtual threadning doimiy daemon statusi va o'zgarmas priority si).

## 31.14 Amalda qo'llash

- [ ] Har bir servis uchun `kubectl exec` bilan `cpu.stat` o'qib `nr_throttled / nr_periods` nisbatini hisoblang, 0.05 dan oshganlarga CPU limitini oshiring.
- [ ] Barcha deployment'larda `-Xmx` ni `-XX:MaxRAMPercentage` ga o'zgartiring va NMT hisoboti bilan xotira taqsimotini tasdiqlang.
- [ ] Liveness probe'dan baza va tashqi servis tekshiruvlarini olib tashlab, ularni faqat readiness guruhiga qoldiring.
- [ ] Sekin ishga tushadigan servislarga `failureThreshold: 30` bilan startup probe qo'shing va startup vaqtini metrika sifatida yozib boring.
- [ ] `server.shutdown=graceful`, `preStop sleep 5` va `terminationGracePeriodSeconds` uchligini bitta koherent qiymat to'plami sifatida sozlang.
- [ ] Fat jar deploy'larini layered jar'ga o'tkazing va registry'ga yuklanadigan qatlam hajmini deploy oldidan va keyin o'lchang.
- [ ] Yuqori yuklamali servislarda `maxUnavailable: 0` va `maxSurge: 1` ga o'tib, cluster'da yetarli zahira sig'im borligini tekshiring.
- [ ] `@Scheduled` metodlar ro'yxatini chiqarib, har biri uchun lock yoki CronJob yechimini tanlang va replikani 2 ga ko'tarib tekshirib ko'ring.

## Manbalar

- Craig Walls, *Spring in Action* 6th, 18-bob - Spring ilovasini deploy qilish
- John Carnell, *Spring Microservices in Action*, 10-bob - konteyner va bulutga deploy
- [Kubernetes, Pod Lifecycle](https://raw.githubusercontent.com/kubernetes/website/e91eff3b59c0bf813193202a4f193d37beb7efd7/content/en/docs/concepts/workloads/pods/pod-lifecycle.md) - `preStop` ning TERM dan oldin ishlashi, `terminationGracePeriodSeconds` default 30 va 2 sekundlik bir martalik uzaytirish, sidecar siz konteynerlarning ixtiyoriy tartibda TERM olishi, startup probe ning liveness va readiness ni to'sishi
- [Kubernetes, Deployment](https://raw.githubusercontent.com/kubernetes/website/e91eff3b59c0bf813193202a4f193d37beb7efd7/content/en/docs/concepts/workloads/controllers/deployment.md) - `maxSurge` va `maxUnavailable` defaultlari, yumaloqlash yo'nalishi, ikkisi bir vaqtda 0 bo'lmasligi, `progressDeadlineSeconds` default 600 va `ProgressDeadlineExceeded`
- Brian Goetz va boshqalar, *Java Concurrency in Practice*, Addison-Wesley, 2006, 7.4-7.4.2-bo'lim (102-103-bet) - tartibli va to'satdan to'xtash farqi; shutdown hook larning tartibsiz va bir vaqtda ishlashi, thread-safe va tez bo'lish talabi, boshqa servis holati haqida taxmin qilmaslik, hamma servis uchun bitta hook; to'satdan to'xtashda hook larning ishlamasligi; daemon statusining meros bo'lishi va JVM halt qilganda daemon threadlarning tashlab ketilishi
- *The Java Language Specification, Java SE 25 Edition* (Gosling, Joy, Steele, Bracha, Buckley, Smith, Bierman), 12.8 (461-462-betlar) - dastur chiqishining besh yo'li; `Runtime.halt` da shutdown hook ishga tushmasligi; chiqish paytida tugamagan threadning boshqa Java kodini bajarmasligi, `finally` va uncaught exception handler ishlamasligi; hook lar ishlayotganda `halt` chaqirilsa hook ning ham to'xtashi
- Boyarsky/Selikoff, *OCP Java SE 17 Study Guide*, 13-bob (725-726 va 731-betlar) - system thread va user-defined thread farqi, daemon thread JVM ni ushlab turmasligi; thread executor birinchi vazifada daemon bo'lmagan thread yaratishi va `shutdown()` chaqirilmasa ilovaning tugamasligi
- [JEP 444: Virtual Threads](https://openjdk.org/jeps/444) - virtual thread har doim daemon bo'lishi va `setDaemon` uni daemon bo'lmagan qilib o'zgartira olmasligi; priority ning `NORM_PRIORITY` da qotib qolishi va `setPriority` ning ta'sir qilmasligi. Shu ikki xossa 31.13 dagi daemon statusini meros qilish qoidasini platform thread bilan cheklaydi
- Titus Winters, Tom Manshreck, Hyrum Wright (tahr.), *Software Engineering at Google*, O'Reilly, 2020, 25-bob ("Containers and Implicit Dependencies" va PID maydoni misoli) - 2011 yilda Borg da PID maydonining tugashi izolyatsiya nosozligiga aylanishi, bitta konteyner yarata oladigan jarayon va thread soniga umumiy chegara kiritish (thread sizdirgan ish butun mashinani yaroqsiz qilmasligi uchun) va keyin thread hamda jarayon PID maydonlarini ajratish
- ESLATMA: 31.3 dagi `podPidsLimit` tavsiyasi, zaxira hisobi va `jvm.threads.live` bilan `pids.current` ni birga o'qish shu korpusning qo'shimchasi


---

[&larr; 30. Kuzatuvchanlik amaliyoti: log, metrika, trace va ularning narxi](30-kuzatuvchanlik-amaliyoti-log-metrika-trace.md) · [Mundarija](README.md) · [32. Tarmoq, timeout va integratsiya haqiqati &rarr;](32-tarmoq-timeout-va-integratsiya-haqiqati.md)
