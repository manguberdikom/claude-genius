<!-- doc: testing | chapter: 13 | part:  -->

[Java Spring loyihasida testlash](../../README.md) / [Testlash qo'llanmasi](README.md)

# 13. Nofunksional testlar: performance, resilience, xavfsizlik (Non-Functional Testing)

<details>
<summary>Bu bobdagi 16 bo'lim</summary>

- [13.1 Nofunksional talablarni o'lchanadigan qilib yozish](#131-nofunksional-talablarni-olchanadigan-qilib-yozish)
- [13.2 Performance test turlari](#132-performance-test-turlari)
- [13.3 Vositalar: Gatling, k6, JMeter, Locust](#133-vositalar-gatling-k6-jmeter-locust)
- [13.4 Amaliy senariy: Gatling va k6](#134-amaliy-senariy-gatling-va-k6)
- [13.5 To'g'ri o'lchash metodikasi](#135-togri-olchash-metodikasi)
- [13.6 Yuklama ostida nimani kuzatish](#136-yuklama-ostida-nimani-kuzatish)
- [13.7 Profiling va diagnostika](#137-profiling-va-diagnostika)
- [13.8 Virtual thread va reactive stack'ni yuklama ostida taqqoslash](#138-virtual-thread-va-reactive-stackni-yuklama-ostida-taqqoslash)
- [13.9 Resilience va chaos testing](#139-resilience-va-chaos-testing)
- [13.10 Xavfsizlik testlash turlari](#1310-xavfsizlik-testlash-turlari)
- [13.11 Penetration test va bug bounty](#1311-penetration-test-va-bug-bounty)
- [13.12 OWASP Top 10'ni test bilan qoplash](#1312-owasp-top-10ni-test-bilan-qoplash)
- [13.13 Accessibility (a11y) va yuridik talablar](#1313-accessibility-a11y-va-yuridik-talablar)
- [13.14 Nofunksional testni jarayonga kiritish](#1314-nofunksional-testni-jarayonga-kiritish)
- [13.15 Anti-patternlar](#1315-anti-patternlar)
- [13.16 Arxitektor nazorat ro'yxati](#1316-arxitektor-nazorat-royxati)

</details>


Funksional testlar "nima ishlaydi" degan savolga javob beradi, nofunksional testlar esa "qanday sharoitda va qancha vaqt ishlaydi" degan savolga. Arxitektor uchun aynan ikkinchi savol qimmatroq: tizim to'g'ri javob qaytarsa ham, 2 sekundda qaytarsa yoki ma'lumotlar bazasi pool'i tugab qolsa, biznes uchun bu nosozlik. Bu bobda performance, resilience va xavfsizlik testlarini o'lchanadigan talablardan boshlab, CI'dagi darvozalargacha va ishlab chiqarishdagi kuzatuvgacha bog'laymiz. Maqsad — alohida "yuklama tekshiruvi" marosimi emas, balki muhandislik jarayonining doimiy qismi.

## 13.1 Nofunksional talablarni o'lchanadigan qilib yozish

"Tizim tez ishlashi kerak" — bu talab emas, orzu. Uni test qilib bo'lmaydi, demak u hech qachon buzilmaydi va hech qachon bajarilmaydi. O'lchanadigan talab to'rt elementdan iborat: metrika, chegara, yuklama konteksti va xato darajasi. Masalan: "`POST /api/orders` uchun p95 < 300 ms va p99 < 800 ms, 500 RPS doimiy yuklamada, 5xx ulushi < 0,1%, 30 daqiqa davomida". Bunday yozuvni Gatling assertion'iga yoki k6 threshold'iga to'g'ridan-to'g'ri ko'chirish mumkin — bu asosiy mezon: talabni kodga aylantirib bo'lmasa, talab tugallanmagan.

Bu yerda SLI, SLO va error budget tushunchalari yordam beradi. SLI — o'lchanadigan signal (muvaffaqiyatli so'rovlar ulushi, p95 kechikish). SLO — SLI uchun maqsadli qiymat ma'lum oyna ichida (masalan, 30 kunda availability 99,9%). Error budget — SLO'dan qolgan "ruxsat etilgan nosozlik" (99,9% uchun oyda ~43 daqiqa). Arxitektor uchun error budget boshqaruv vositasi: budget tugayotgan bo'lsa, yangi funksiya emas, ishonchlilik ishlari birinchi o'ringa chiqadi. Performance testlardagi chegaralar SLO'dan kelib chiqishi kerak, aks holda CI'da "qizil" bo'lgan test biznes uchun hech narsani anglatmaydi.

## 13.2 Performance test turlari

Ko'pchilik jamoa "load test" deganda bitta narsani tushunadi, aslida esa turlari har xil savolga javob beradi va har xil muhit talab qiladi. Chalkashlik qimmatga tushadi: soak test o'rniga 5 daqiqalik load test o'tkazib, memory leak'ni sezmay qolish odatiy hol.

| Tur | Nimani aniqlaydi | Yuklama shakli | Qachon |
|---|---|---|---|
| Load (yuklama) | Kutilgan yuklamada SLO bajariladimi | Maqsadli RPS, 15-60 daqiqa | Nightly, release oldidan |
| Stress | SLO buzila boshlagan nuqta va xatolar xarakteri | Maqsadning 1,5-3 baravari | Har sprintda yoki arxitektura o'zgarsa |
| Spike | To'satdan o'sishga reaksiya, autoscaling va queue xatti-harakati | Sekundlar ichida 10x sakrash | Marketing kampaniyasi, Black Friday oldidan |
| Soak / endurance | Memory leak, connection leak, log to'planishi, GC degradatsiyasi | O'rtacha yuklama, 4-24 soat | Har hafta yoki katta release oldidan |
| Scalability | Resurs qo'shilsa throughput chiziqli o'sadimi | Bir xil yuklama, replica soni o'zgaradi | Capacity rejalashtirishda |
| Capacity | Bitta instance qancha RPS "ko'taradi" | Bosqichma-bosqich oshirish | Sizing va budget hisobida |
| Breakpoint | Tizim qayerda sinadi va qanday sinadi | Chegarasiz o'sish | Yangi komponent kiritilganda |

Amaliy tartib: avval capacity (bitta instance qancha), keyin load (SLO), keyin soak (barqarorlik), undan keyin spike va breakpoint. Stress va breakpoint natijasi ko'pincha eng qimmatli: ular timeout, bulkhead va circuit breaker sozlamalarining to'g'ri yoki noto'g'riligini ko'rsatadi.

## 13.3 Vositalar: Gatling, k6, JMeter, Locust

| Mezon | Gatling | k6 | JMeter | Locust |
|---|---|---|---|---|
| Senariy tili | Java/Kotlin/Scala DSL | JavaScript (ES6) | XML + GUI | Python |
| Yozish qulayligi (Java jamoa) | Juda yuqori, IDE va refactoring | Yuqori, lekin JS bilim kerak | O'rtacha, GUI'da katta senariy og'ir | O'rtacha |
| Version control'ga mosligi | Yaxshi (oddiy kod) | Yaxshi | Yomon (katta XML diff) | Yaxshi |
| CI integratsiyasi | Maven/Gradle plugin, exit code | CLI, Docker, exit code | CLI (non-GUI), plugin | CLI |
| Resurs sarfi (1 injector) | Past (Netty, async) | Juda past (Go runtime) | Yuqori (thread-per-user) | O'rtacha (gevent) |
| Taqsimlangan yuklama | Enterprise yoki qo'lda | Oson (bir nechta instance, Kubernetes operator) | Master/worker, murakkab | Master/worker, oson |
| Hisobot | HTML report, assertion natijasi | Summary, Prometheus remote write, JSON | HTML dashboard | Web UI, CSV |
| Protokollar | HTTP, WebSocket, JMS, gRPC | HTTP, WebSocket, gRPC | Juda ko'p (JDBC, JMS, LDAP) | HTTP asosan |

Tavsiya: Java/Spring jamoasi uchun **Gatling** birinchi tanlov — senariy bir xil tilda yoziladi, domain kodini (DTO, test fixture, signature generator) qayta ishlatish mumkin va Maven/Gradle orqali CI'ga tabiiy tushadi. **k6** platforma/SRE jamoasi senariylarni ilova repozitoriyasidan ajratib, Kubernetes'da ko'p injector bilan ishlatmoqchi bo'lsa yaxshi. **JMeter**ni faqat eski senariylar merosi yoki HTTP'dan tashqari ekzotik protokol kerak bo'lsa saqlang. **Locust** jamoa allaqachon Python bilan ishlayotgan joyda o'rinli.

## 13.4 Amaliy senariy: Gatling va k6

Gatling Java DSL'da foydalanuvchi profili, ramp-up, think time va assertion'lar bir faylda yoziladi. Assertion'lar muhim: ular test tugashida exit code'ni belgilaydi, ya'ni CI darvozasini.

```java
import io.gatling.javaapi.core.*;
import io.gatling.javaapi.http.*;
import static io.gatling.javaapi.core.CoreDsl.*;
import static io.gatling.javaapi.http.HttpDsl.*;

public class OrderApiSimulation extends Simulation {
  HttpProtocolBuilder httpProtocol = http
      .baseUrl(System.getProperty("targetUrl", "http://localhost:8080"))
      .acceptHeader("application/json");

  ScenarioBuilder checkout = scenario("Browse and checkout")
      .exec(http("GET products").get("/api/products?page=0")
          .check(status().is(200)))
      .pause(1, 3)
      .exec(http("POST orders").post("/api/orders").asJson()
          .body(StringBody("{\"sku\":\"SKU-1\",\"qty\":1}"))
          .check(status().is(201)));
  {
    setUp(checkout.injectOpen(
            rampUsersPerSec(20).to(500).during(180),
            constantUsersPerSec(500).during(900)))
        .protocols(httpProtocol)
        .assertions(
            global().responseTime().percentile3().lt(300),
            global().failedRequests().percent().lt(0.1));
  }
}
```

`injectOpen` — open workload model: foydalanuvchilar server sekinlashsa ham belgilangan tezlikda keladi. Bu ishlab chiqarishga yaqinroq va coordinated omission'dan himoya qiladi. `percentile3()` Gatling'ning standart sozlamasida p95, `percentile4()` — p99.

k6'da xuddi shu g'oya `ramping-arrival-rate` executor va `thresholds` orqali ifodalanadi:

```javascript
import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  scenarios: {
    checkout: {
      executor: 'ramping-arrival-rate',
      startRate: 20, timeUnit: '1s',
      preAllocatedVUs: 300, maxVUs: 1500,
      stages: [
        { target: 500, duration: '3m' },
        { target: 500, duration: '15m' },
      ],
    },
  },
  thresholds: {
    http_req_failed: ['rate<0.001'],
    'http_req_duration{name:orders}': ['p(95)<300', 'p(99)<800'],
  },
};

export default function () {
  const res = http.post(`${__ENV.TARGET_URL}/api/orders`,
    JSON.stringify({ sku: 'SKU-1', qty: 1 }),
    { headers: { 'Content-Type': 'application/json' }, tags: { name: 'orders' } });
  check(res, { created: (r) => r.status === 201 });
  sleep(Math.random() * 2 + 1);
}
```

CI'da bu testni darvoza sifatida ishlatish: threshold buzilsa k6 nolga teng bo'lmagan exit code qaytaradi, Gatling assertion buzilsa Maven/Gradle task fail bo'ladi. Shuning uchun alohida "natijani tahlil qiluvchi" skript yozish shart emas.

```yaml
name: nightly-performance
on:
  schedule: [{ cron: '0 2 * * *' }]
  workflow_dispatch:
jobs:
  load-test:
    runs-on: [self-hosted, perf-dedicated]
    steps:
      - uses: actions/checkout@v4
      - name: Warm-up (JIT va cache)
        run: ./scripts/warmup.sh "$TARGET_URL"
      - name: k6 load test
        run: |
          docker run --rm -i -e TARGET_URL \
            -e K6_PROMETHEUS_RW_SERVER_URL \
            grafana/k6:latest run \
            --out experimental-prometheus-rw - < perf/orders.js
        env:
          TARGET_URL: https://staging.internal
          K6_PROMETHEUS_RW_SERVER_URL: http://prom.internal/api/v1/write
      - name: Natijani saqlash
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: perf-summary
          path: perf/summary.json
```

Muhim detal: yuklama generatori alohida, band bo'lmagan runner'da ishlashi kerak. Umumiy GitHub-hosted runner'da o'lchangan p99 shovqindan boshqa narsa emas.

## 13.5 To'g'ri o'lchash metodikasi

Noto'g'ri o'lchov noto'g'ri qarorga olib keladi, shuning uchun metodika vositadan muhimroq. Birinchi qoida — **warm-up**. JVM C2 kompilyatori qaynoq kodni optimizatsiya qilishi uchun minglab chaqiruv kerak; shuningdek connection pool to'ladi, Hibernate metadata va cache isiydi. Shu sababli birinchi 1-3 daqiqa natijasini hisobdan chiqaring (Gatling'da alohida warm-up senariysi, k6'da `--no-summary` bilan oldindan yuritish yoki natijani time range bo'yicha kesish).

Ikkinchi qoida — **o'rtacha qiymatni unutish**. O'rtacha 120 ms bo'lgan tizimda p99 4 sekund bo'lishi mumkin va aynan shu 1% foydalanuvchi shikoyat qiladi. p50/p95/p99 va maksimum birga ko'riladi; persentillarni bir nechta injector natijasida "o'rtalashtirish" matematik jihatdan xato — HdrHistogram kabi birlashtiriladigan histogram ishlating yoki serverdagi Micrometer histogramiga tayaning.

Uchinchi qoida — **coordinated omission**. Closed model'da (fiksirlangan VU soni, har biri javobni kutadi) server sekinlashsa, yuklama ham o'z-o'zidan kamayadi va sekin so'rovlar o'lchovga tushmaydi — natija haqiqatdan chiroyliroq ko'rinadi. Yechim: arrival-rate / open model (`injectOpen`, `ramping-arrival-rate`) va so'rov yuborilishi kerak bo'lgan vaqtdan boshlab o'lchash.

To'rtinchi qoida — **bitta o'zgaruvchi**. Har bir testda faqat bitta narsa o'zgarsin: yoki yuklama, yoki pool hajmi, yoki JVM flag. Ikkitasini birga o'zgartirsangiz, natijani talqin qila olmaysiz. GC ta'siri shu yerda ko'rinadi: G1 bilan ZGC'ni taqqoslayotganda heap hajmi va yuklama bir xil bo'lishi shart.

Beshinchi qoida — **ishlab chiqarishga o'xshash muhit va ma'lumot hajmi**. 10 000 qatorli jadvalda index'siz query 2 ms, 50 million qatorda 4 sekund. CPU limiti, replica soni, tarmoq topologiyasi, TLS, ingress va feature flag'lar ham prod'dagiday bo'lishi kerak. Farqlar bo'lsa, ularni test hisobotida ochiq yozing.

## 13.6 Yuklama ostida nimani kuzatish

Load test natijasi faqat ikkita grafikdan iborat bo'lmasligi kerak. Yuklama paytida kamida to'rt qatlam metrikasi yoziladi va bir vaqt o'qida ko'riladi.

Ilova qatlami (Micrometer): `http.server.requests` (count, persentil, status bo'yicha), `resilience4j.circuitbreaker.state`, `executor.queued` va `executor.active` (`@Async`/task executor), biznes metrikalari (`orders.created`). JVM qatlami: `jvm.memory.used`, `jvm.gc.pause` (maksimal pauza va chastota), `jvm.threads.live`, virtual thread ishlatilsa — pinning hodisalari. Ma'lumotlar bazasi: `hikaricp.connections.active`, `hikaricp.connections.pending` (nolga teng bo'lmagan `pending` — pool tanqisligining birinchi belgisi), `hikaricp.connections.acquire` vaqti, PostgreSQL tomonida `pg_stat_statements`, lock kutishlari, `idle in transaction` sessiyalari. Tashqi servislar: `http.client.requests` yoki Feign/WebClient timer'lari, timeout va retry soni.

Spring Boot'da bu qatlamlarni ochish uchun Actuator va Prometheus registry yetarli, lekin histogram va SLO chegaralarini ataylab yoqish kerak:

```yaml
management:
  endpoints:
    web:
      exposure:
        include: health,info,metrics,prometheus
  prometheus:
    metrics:
      export:
        enabled: true
  metrics:
    tags:
      application: ${spring.application.name}
      env: ${ENVIRONMENT:staging}
    distribution:
      percentiles-histogram:
        http.server.requests: true
        http.client.requests: true
      slo:
        http.server.requests: 100ms,300ms,800ms
      maximum-expected-value:
        http.server.requests: 10s
```

`percentiles-histogram: true` server tomonida to'liq histogram beradi — shunda persentillarni Prometheus'da (`histogram_quantile`) to'g'ri hisoblash va bir nechta instance bo'yicha birlashtirish mumkin.

## 13.7 Profiling va diagnostika

Load test "muammo bor" deydi, profiling "muammo qayerda" deydi. Ikkisini aralashtirmang: avval yuklama ostida SLO buzilishini takrorlang, keyin shu holatda profil oling.

JFR — birinchi vosita, chunki overhead'i past (odatda bir necha foiz) va ishlab chiqarishda ham yoqish mumkin. Uni to'g'ridan-to'g'ri ishga tushirishda yoki `jcmd` orqali ulanishda ishlatasiz. async-profiler CPU va wall-clock flame graph uchun kuchliroq: `wall` rejimi bloklangan thread'larni ko'rsatadi, bu I/O bound Spring ilovalarida aynan kerak bo'ladigan narsa.

```bash
java -XX:StartFlightRecording=settings=profile,duration=20m,filename=/tmp/load.jfr -jar app.jar
jcmd <pid> JFR.start name=load settings=profile maxsize=512m
jcmd <pid> JFR.dump name=load filename=/tmp/load.jfr
jcmd <pid> Thread.print > /tmp/threads.txt
jcmd <pid> GC.heap_info
jcmd <pid> GC.heap_dump /tmp/heap.hprof
./asprof -e cpu -d 60 -f /tmp/cpu.html <pid>
./asprof -e wall -t -d 60 -f /tmp/wall.html <pid>
./asprof -e alloc -d 60 -f /tmp/alloc.html <pid>
```

JFR faylini JDK Mission Control'da ochib allocation, lock contention, GC pauzalari, socket I/O va exception "issiq nuqtalarini" ko'rish mumkin. Heap dump'ni Eclipse MAT yoki JMC bilan tahlil qilib dominator tree orqali leak egasini topasiz — soak testdan keyin heap doimiy o'sgan bo'lsa, shu yo'ldan borasiz.

Qachon nima: throughput kutilganidan past yoki kechikish o'sayotgan bo'lsa — load test; CPU to'liq band bo'lsa yoki sababini tushunmasangiz — CPU profiling; thread'lar band, CPU bo'sh bo'lsa — wall-clock profiling va thread dump; xotira o'sayotgan bo'lsa — alloc profiling va heap dump; "ba'zida sekin" bo'lsa — GC log va JFR.

## 13.8 Virtual thread va reactive stack'ni yuklama ostida taqqoslash

Java 21'dan virtual thread (`spring.threads.virtual.enabled=true`, Spring Boot 3.2+) blocking kodni saqlab turib yuqori konkurensiyaga erishish imkonini berdi; reactive stack (WebFlux) esa boshqa programmatik model taklif qiladi. Taqqoslashda xato qilish juda oson.

O'lchash kerak bo'lgan narsalar: bir xil SLO ostida maksimal throughput; p99 (o'rtacha emas); CPU va xotira birligiga to'g'ri keladigan RPS; thread/stack xotirasi; ulanish pool'ining to'yinish nuqtasi; downstream sekinlashganda tizim xatti-harakati (bu eng muhimi). Virtual thread downstream sekinlashganda ko'p "arzon" thread yaratadi, lekin ma'lumotlar bazasi pool'i hali ham 20 ta ulanish bilan cheklangan — ya'ni bottleneck ko'chadi, yo'qolmaydi. Reactive stack'da esa backpressure to'g'ri sozlanmagan bo'lsa queue cheksiz o'sadi.

Odatiy xatolar: (1) virtual thread testida `synchronized` bloklar sababli pinning — Java 21-23'da bu carrier thread'ni band qiladi; JDK 24'dan (JEP 491) `synchronized` endi pinning qilmaydi, lekin native/JNI chaqiruv va `Object.wait` hali ham muammo bo'lishi mumkin. Pinning'ni JFR'dagi `jdk.VirtualThreadPinned` hodisasi bilan tekshiring, taxmin qilmang. (2) Reactive zanjirning o'rtasida blocking JDBC chaqiruvi — event loop thread bloklanadi va butun tizim qulaydi; `BlockHound` bilan test muhitida aniqlash mumkin. (3) Thread pool o'lchamlarini bir xil qoldirib taqqoslash. (4) Faqat "salom dunyo" endpoint'ida o'lchash — real senariyda ma'lumotlar bazasi va tashqi servis bo'lishi shart. Arxitektorning xulosasi ko'pincha shunday bo'ladi: ikkala stack ham yetarli, tanlov jamoaning tajribasi, debug qulayligi va kutubxona ekosistemasiga bog'liq — raqamlar farqi esa bottleneck ma'lumotlar bazasida bo'lganda deyarli ko'rinmaydi.

## 13.9 Resilience va chaos testing

Resilience testi — nosozlikni kutish emas, ataylab kiritish. Minimal to'plam: konteynerni o'chirish (pod kill), tashqi servisga tarmoq kechikishi qo'shish, paket yo'qotish, ulanishni to'satdan uzish, ma'lumotlar bazasini qayta ishga tushirish, DNS javobini sekinlashtirish, disk to'lib qolishi. Har bir eksperiment uchun gipoteza yozilishi kerak: "payment-gateway 3 sekundga sekinlashsa, `POST /orders` 1 sekundda timeout bo'ladi, circuit breaker ochiladi va mijoz 503 emas, 'keyinroq tasdiqlanadi' javobini oladi".

Tarmoq nosozligini determinantlashtirib simulyatsiya qilish uchun Toxiproxy qulay: proxy'ni test ichida boshqarib, latency yoki bandwidth toxic'ini yoqib-o'chirish mumkin.

```java
ToxiproxyClient client = new ToxiproxyClient(toxiproxy.getHost(),
    toxiproxy.getControlPort());
Proxy payments = client.createProxy("payments", "0.0.0.0:8666",
    "payment-gw:8080");

payments.toxics().latency("lag", ToxicDirection.DOWNSTREAM, 3_000)
    .setJitter(500);
try {
  OrderResult result = orderService.place(new OrderRequest("SKU-1", 1));
  assertThat(result.status()).isEqualTo(Status.PENDING_CONFIRMATION);
  assertThat(circuitBreaker.getState())
      .isIn(State.OPEN, State.HALF_OPEN);
  assertThat(meterRegistry.get("http.client.requests")
      .tag("outcome", "CLIENT_ERROR").timer().count()).isPositive();
} finally {
  payments.toxics().get("lag").remove();
}
```

Ilova ichidagi nosozliklar uchun Chaos Monkey for Spring Boot (codecentric) ishlatiladi: `chaos.monkey.enabled=true`, watcher'lar (`watcher.service`, `watcher.repository`, `watcher.controller`) va assault'lar (`assaults.latencyActive`, `assaults.exceptionsActive`, `assaults.killApplicationActive`, `assaults.memoryActive`). Uni faqat staging yoki alohida chaos profilida yoqing va Actuator endpoint'i orqali ish vaqtida boshqaring.

Nimani tasdiqlash kerak: timeout'lar barcha qatlamda mavjud va downstream timeout upstream'dan kichik; retry faqat idempotent operatsiyalarda va jitter bilan; circuit breaker ochiladi va yopiladi; graceful degradation ishlaydi (cache'dan eski ma'lumot, qisqartirilgan javob); health check nosozlikni to'g'ri aks ettiradi; alert ishga tushadi va dashboard'da sabab ko'rinadi. Game day — jamoa bilan rejalashtirilgan mashq: staging yoki cheklangan prod segmentida nosozlik kiritiladi, on-call muhandis runbook bo'yicha harakat qiladi, natijada runbook va alert'lardagi bo'shliqlar topiladi.

## 13.10 Xavfsizlik testlash turlari

Xavfsizlik — bitta skaner emas, bir necha xil qarash. Har birining o'z o'rni va CI'dagi o'z bosqichi bor.

**SAST** (statik tahlil) — kodni ishga tushirmasdan zaif naqshlarni izlaydi: SonarQube security rules, Semgrep, SpotBugs + find-sec-bugs, CodeQL. PR'da ishlaydi, faqat o'zgargan kodga nisbatan qat'iy (incremental), aks holda eski "qarz" PR'ni to'sib qo'yadi.

**SCA / dependency scanning** — kutubxonalardagi ma'lum CVE'lar: OWASP Dependency-Check, Snyk, Trivy, GitHub Dependabot. Bu eng yuqori ROI'li tekshiruv, chunki OWASP Top 10'dagi "vulnerable components" punkti aynan shu. PR'da (yangi dependency kiritilishi) va kunlik jadval bo'yicha (yangi CVE eski kod uchun ham chiqadi) ishlatiladi.

**Secret scanning** — kalit va parollarni commit'ga tushishini oldini oladi: gitleaks, trufflehog, GitHub secret scanning va push protection. Pre-commit hook plus CI — ikkalasi kerak, chunki hook'ni o'tkazib yuborish oson.

**Container image scanning** — Trivy yoki Grype bilan base image va OS paketlari; **IaC scanning** — Trivy config, Checkov yoki tfsec bilan Terraform, Helm va Kubernetes manifestlari (ochiq security group, privileged container, `hostNetwork`).

**DAST** — ishlayotgan ilovaga tashqaridan hujum: OWASP ZAP baseline yoki full scan, autentifikatsiya bilan API scan (OpenAPI spetsifikatsiyasidan). Staging deploy'dan keyin ishlaydi, nightly rejimda.

```yaml
jobs:
  sca-and-secrets:
    steps:
      - uses: actions/checkout@v4
      - name: OWASP Dependency-Check
        run: ./gradlew dependencyCheckAnalyze --info
      - name: Trivy filesystem va IaC
        uses: aquasecurity/trivy-action@master
        with:
          scan-type: fs
          severity: HIGH,CRITICAL
          exit-code: '1'
          ignore-unfixed: 'true'
      - name: gitleaks
        uses: gitleaks/gitleaks-action@v2
  dast:
    needs: deploy-staging
    steps:
      - name: OWASP ZAP baseline
        uses: zaproxy/action-baseline@v0.12.0
        with:
          target: https://staging.internal
          rules_file_name: .zap/rules.tsv
          allow_issue_writing: false
```

Qoida: har bir skaner uchun suppression fayli (`dependency-check-suppressions.xml`, `.trivyignore`, `.zap/rules.tsv`) versiya nazoratida bo'lishi va har bir istisno sabab va muddat bilan izohlanishi kerak. Muddatsiz istisno — abadiy zaiflik.

## 13.11 Penetration test va bug bounty

Avtomatik skanerlar ma'lum naqshlarni topadi; penetration test biznes mantig'idagi zaifliklarni topadi. "Boshqa foydalanuvchi buyurtmasini `orderId`ni o'zgartirib ko'rish", "chegirma kuponini ikki marta ishlatish", "rol tekshiruvi faqat frontend'da" — bunday narsalarni ZAP topmaydi.

Kim o'tkazadi: tashqi mustaqil jamoa (ichki jamoa o'z tizimini "ko'r nuqta" bilan ko'radi). Qanchalik tez-tez: yiliga kamida bir marta, shuningdek arxitektura yoki autentifikatsiya modeli sezilarli o'zgarganda, yangi tashqi integratsiya yoki yangi to'lov oqimi qo'shilganda. Compliance (PCI DSS, ISO 27001) talablari ham chastotani belgilaydi. Scope va qoidalarni (rate limit, ma'lumot bilan ishlash, test akkauntlari) oldindan yozib qo'yish shart.

Natijani boshqarish: har bir topilma odatdagi backlog ishiga aylanadi, severity bo'yicha SLA belgilanadi (masalan, critical — 7 kun, high — 30 kun), va eng muhimi — har bir topilma uchun **regression test** yoziladi. Agar IDOR topilgan bo'lsa, `@WebMvcTest` yoki integratsiya testida boshqa foydalanuvchi resursiga 403 qaytishini tekshiradigan test paydo bo'lishi kerak. Shunday qilib pentest natijasi hujjat emas, doimiy himoyaga aylanadi. Bug bounty esa doimiy, tashqi, natijaga to'lanadigan kanal: u pentest o'rnini bosmaydi, balki "uzoq dum"dagi zaifliklarni topadi va faqat ichki jarayon yetilgan (triage, SLA, aloqa) jamoalarda ma'noga ega.

## 13.12 OWASP Top 10'ni test bilan qoplash

Quyidagi jadval OWASP Top 10 (2021 nashri) punktlarini qanday testlar bilan qoplash mumkinligini ko'rsatadi. Ro'yxat vaqti-vaqti bilan qayta ko'rib chiqiladi, shuning uchun jamoa qaysi nashrga tayanayotganini hujjatda qat'iy belgilab qo'ying.

| Punkt | Avtomatik test | Qo'lda / pentest | Izoh |
|---|---|---|---|
| A01 Broken Access Control | Qisman: har rol uchun endpoint testlari, IDOR regression testlari | Ha, asosiy | Biznes mantig'i avtomatlashtirilmaydi |
| A02 Cryptographic Failures | Qisman: TLS konfiguratsiyasi (testssl.sh), SAST (zaif algoritmlar) | Ha | Kalit boshqaruvi — audit masalasi |
| A03 Injection | Ko'p qismi: SAST, ZAP active scan, parametrlashtirilgan query testlari | Qisman | NoSQL va template injection e'tibor talab qiladi |
| A04 Insecure Design | Yo'q | Ha (threat modeling) | Testdan oldin dizayn sharhi |
| A05 Security Misconfiguration | Ha: IaC scanning, ZAP header tekshiruvi, Actuator ochiqligi testi | Qisman | Prod konfiguratsiyasini ham tekshirish |
| A06 Vulnerable Components | Ha, to'liq: Dependency-Check, Trivy, Dependabot | Yo'q | Eng oson avtomatlashtiriladigan punkt |
| A07 Auth Failures | Ko'p qismi: token muddati, brute force / rate limit, session testlari | Qisman | MFA bypass — qo'lda |
| A08 Integrity Failures | Ha: imzo tekshiruvi, SBOM, artefakt provenance, deserialization SAST | Qisman | Supply chain nazorati |
| A09 Logging & Monitoring Failures | Qisman: alert testlari, chaos eksperimentlari, log assertion | Ha (game day) | "Hujumni ko'ramizmi?" savoli |
| A10 SSRF | Qisman: allowlist unit testlari, ZAP qoidalari | Ha | Cloud metadata endpoint'i alohida tekshiriladi |

Xulosa: A06 va A05 deyarli to'liq avtomatlashtiriladi, A01, A04 va A09 esa inson tahlilini talab qiladi. Shuning uchun "skaner yashil" degani "xavfsiz" degani emas.

## 13.13 Accessibility (a11y) va yuridik talablar

Agar mahsulotda veb interfeys bo'lsa, accessibility nofunksional talab va ko'p yurisdiksiyalarda yuridik majburiyat. Yevropa Ittifoqida European Accessibility Act, AQShda ADA va davlat sektori uchun Section 508, Yevropa davlat xaridlarida EN 301 549 standarti amal qiladi. Texnik mezon — WCAG (2.1 yoki 2.2) va uning darajalari: A (minimal), AA (amalda standart talab, odatda shartnomalarda shu ko'rsatiladi), AAA (tanlangan kriteriyalar uchun).

Avtomatik tekshiruv: `axe-core` (E2E testlarga `@axe-core/playwright` yoki `@axe-core/cli` orqali qo'shiladi) va Lighthouse / Lighthouse CI. Ular kontrast, `alt` matn yo'qligi, ARIA noto'g'ri ishlatilishi, label'siz forma maydonlari, sarlavha ierarxiyasi kabi narsalarni topadi. Ammo real qoplama cheklangan — avtomatik vositalar WCAG kriteriyalarining taxminan uchdan bir qismini aniqlaydi. Qolgani qo'lda tekshiriladi: faqat klaviatura bilan butun oqimni o'tish (Tab tartibi, focus ko'rinishi, modal'dan chiqish), screen reader (NVDA, VoiceOver) bilan sinash, 200% zoom va matnni kattalashtirishda layout buzilmasligi, rangga bog'liq bo'lmagan ma'no uzatish, xato xabarlarining e'lon qilinishi. Jarayon uchun amaliy yechim: axe tekshiruvini E2E suite'ga qo'shib, yangi "critical" buzilishlarni PR'da to'xtatish, mavjud qarzni alohida backlog'da bosqichma-bosqich yopish va har chorakda qo'lda audit o'tkazish.

## 13.14 Nofunksional testni jarayonga kiritish

Nofunksional testlarning eng ko'p uchraydigan muvaffaqiyatsizlik sababi — noto'g'ri bosqichda ishlatish. Hamma narsani har PR'da ishlatsangiz, pipeline sekinlashadi va o'chirib qo'yiladi; hech narsani ishlatmasangiz, release oldida panika bo'ladi.

| Bosqich | Nima ishlaydi | Vaqt budjeti | Darvozami |
|---|---|---|---|
| Har PR'da | SAST (incremental), SCA, secret scanning, axe critical, 1-2 daqiqalik "smoke performance" (bitta endpoint, past RPS, regression chegarasi) | < 10 daqiqa | Ha, blokirovka |
| Nightly | To'liq load test, ZAP baseline, image va IaC scanning, Lighthouse | 1-2 soat | Ha, lekin merge'ni emas, release'ni bloklaydi |
| Har hafta | Soak (4-12 soat), stress, breakpoint | Tunda / dam olish kuni | Hisobot + trend |
| Release oldidan | Load + spike prod'ga o'xshash muhitda, chaos eksperimentlari, SBOM va litsenziya tekshiruvi | 0,5-1 kun | Ha, release checklist |
| Prod'da | Canary (metrika bo'yicha avtomatik rollback), synthetic monitoring, SLO va error budget kuzatuvi, doimiy JFR | Doimiy | Avtomatik rollback |

Kim ko'radi va qanday qaror qabul qiladi: PR darajasidagi natijani muallif va reviewer ko'radi — qizil bo'lsa, merge bo'lmaydi. Nightly va haftalik natijalar uchun aniq egasi bo'lishi kerak (performance uchun servis jamoasi tech lead'i, xavfsizlik uchun security champion) — "hamma ko'radi" degani "hech kim ko'rmaydi". Trend muhim: bitta test natijasi emas, p95 va p99'ning haftalar bo'yicha o'zgarishi. Qaror mezonlari oldindan yozilgan bo'lsin: SLO buzilishi — release to'xtatiladi; 10% regressiya — tergov ishi ochiladi; critical CVE — belgilangan SLA ichida tuzatiladi; error budget tugadi — yangi funksiyalar to'xtaydi.

## 13.15 Anti-patternlar

**Performance testni release oldidan bir marta o'tkazish.** Natija: muammo topilganda arxitekturani o'zgartirishga vaqt yo'q, shuning uchun "keyingi release'ga" ko'chiriladi. Yechim — har PR'da kichik regression testi, nightly'da to'liq test, trend kuzatuvi.

**Laptop'da o'lchash.** Mahalliy mashinada ma'lumotlar bazasi, ilova va yuklama generatori bir CPU'ni bo'lishadi, tarmoq kechikishi nolga teng, dataset kichik.

**O'rtacha javob vaqtiga qarash.** O'rtacha hech kimning tajribasini aks ettirmaydi. Persentil va maksimum ko'riladi, persentillar o'rtalashtirilmaydi.

**Bir foydalanuvchi bilan "test qilish".** Postman'da bitta so'rov 80 ms qaytargani konkurensiya, pool tanqisligi, lock contention va GC haqida hech narsa aytmaydi.

**Closed model bilan tinch o'lchash** va coordinated omission'ni e'tiborsiz qoldirish — natija sun'iy ravishda chiroyli chiqadi.

**Xavfsizlik skanini "warning" sifatida qoldirish.** Darvoza bo'lmagan skaner natijasi bir-ikki sprintdan keyin minglab ogohlantirishga aylanadi va hech kim o'qimaydi. Yechim: yangi topilmalar bloklaydi, eski qarz muddatli istisno bilan rasmiylashtiriladi.

**Chaos eksperimentini gipotezasiz o'tkazish.** "Pod'ni o'chirdik, hech narsa bo'lmadi" — bu natija emas. Gipoteza, o'lchov va kutilgan xatti-harakat oldindan yozilishi kerak.

**Nofunksional talabni hujjatda qoldirib, kodga ko'chirmaslik.** Agar SLO assertion yoki threshold sifatida mavjud bo'lmasa, u real emas.

## 13.16 Arxitektor nazorat ro'yxati

- [ ] Har bir muhim endpoint uchun o'lchanadigan SLO yozilgan (metrika, persentil chegarasi, RPS, xato ulushi) va u Gatling assertion yoki k6 threshold sifatida kodda mavjud.
- [ ] Yuklama turlari ajratilgan va rejalashtirilgan: load va smoke-performance CI'da, soak va stress jadval bo'yicha, spike muhim voqealar oldidan.
- [ ] O'lchash metodikasi hujjatlashtirilgan: warm-up, open/arrival-rate model, persentillar, prod'ga o'xshash muhit va dataset, bir vaqtda bitta o'zgaruvchi.
- [ ] Yuklama paytida ilova (Micrometer/Actuator), JVM, ma'lumotlar bazasi pool'i va tashqi servis metrikalari Prometheus'ga yoziladi va bitta dashboard'da ko'riladi.
- [ ] Resilience eksperimentlari gipoteza bilan avtomatlashtirilgan (Toxiproxy, Chaos Monkey for Spring Boot) va timeout, retry, circuit breaker, graceful degradation tasdiqlangan; choraklik game day o'tkaziladi.
- [ ] Xavfsizlik to'plami to'liq va to'g'ri bosqichda: SAST va SCA PR'da, secret scanning pre-commit va CI'da, image/IaC scanning build'da, DAST nightly; barcha istisnolar sabab va muddat bilan versiya nazoratida.
- [ ] Pentest yiliga kamida bir marta, har bir topilma uchun severity SLA va regression test mavjud.
- [ ] Natijalar uchun aniq egasi va qaror qoidalari belgilangan (regressiya foizi, error budget holati, CVE SLA), prod'da canary va synthetic monitoring ishlaydi.

---

[&larr; 12. End-to-end va UI testlar](12-end-to-end-va-ui-testlar.md) · [Mundarija](README.md) · [14. Arxitektura testlari va kod sifati darvozalari &rarr;](14-arxitektura-testlari-va-kod-sifati.md)
