<!-- doc: patterns | chapter: 29 | part:  -->

[Barcha hujjatlar](../../README.md) / [Dizayn patternlar](README.md)

> Holat: AI yozgan, inson tekshirmagan.

# 29. Kubernetes va cloud-native patternlar (Kubernetes & Cloud-Native Patterns)

<details>
<summary>Bu bobdagi 23 bo'lim</summary>

- [29.1 Oldindan aytib beriladigan talablar (Predictable Demands)](#291-oldindan-aytib-beriladigan-talablar-predictable-demands)
- [29.2 Deklarativ joylashtirish (Declarative Deployment)](#292-deklarativ-joylashtirish-declarative-deployment)
- [29.3 Boshqariladigan hayot sikli (Managed Lifecycle)](#293-boshqariladigan-hayot-sikli-managed-lifecycle)
- [29.4 Avtomatlashtirilgan joylashtirish (Automated Placement)](#294-avtomatlashtirilgan-joylashtirish-automated-placement)
- [29.5 Batch ishi (Batch Job)](#295-batch-ishi-batch-job)
- [29.6 Davriy ish (Periodic Job)](#296-davriy-ish-periodic-job)
- [29.7 Demon servis (Daemon Service)](#297-demon-servis-daemon-service)
- [29.8 Yakka servis (Singleton Service)](#298-yakka-servis-singleton-service)
- [29.9 Stateless servis (Stateless Service)](#299-stateless-servis-stateless-service)
- [29.10 Stateful servis (Stateful Service)](#2910-stateful-servis-stateful-service)
- [29.11 Servis topish (Service Discovery (Kubernetes view))](#2911-servis-topish-service-discovery-kubernetes-view)
- [29.12 O'z-o'zini anglash (Self Awareness)](#2912-oz-ozini-anglash-self-awareness)
- [29.13 Elastik masshtablash (Elastic Scale)](#2913-elastik-masshtablash-elastic-scale)
- [29.14 Image quruvchi (Image Builder)](#2914-image-quruvchi-image-builder)
- [29.15 Konfiguratsiya resursi (Configuration Resource)](#2915-konfiguratsiya-resursi-configuration-resource)
- [29.16 O'zgarmas konfiguratsiya (Immutable Configuration)](#2916-ozgarmas-konfiguratsiya-immutable-configuration)
- [29.17 Muhit o'zgaruvchilari orqali konfiguratsiya (EnvVar Configuration)](#2917-muhit-ozgaruvchilari-orqali-konfiguratsiya-envvar-configuration)
- [29.18 Konfiguratsiya shabloni (Configuration Template)](#2918-konfiguratsiya-shabloni-configuration-template)
- [29.19 Boshqaruvchi halqa (Controller (Kubernetes))](#2919-boshqaruvchi-halqa-controller-kubernetes)
- [29.20 Operator (Operator)](#2920-operator-operator)
- [29.21 Pod - deploy birligi sifatida (Pod as Deployment Unit)](#2921-pod---deploy-birligi-sifatida-pod-as-deployment-unit)
- [29.22 Resurs so'rovlari va limitlari (Resource Requests & Limits)](#2922-resurs-sorovlari-va-limitlari-resource-requests--limits)
- [29.23 Amalda qo'llash](#2923-amalda-qollash)

</details>



Kubernetes va cloud-native patternlar - bu ilovaning ichki sinflar darajasidagi dizayni emas, balki uning konteyner orkestratori bilan qanday "muloqot qilishi" haqidagi patternlar to'plami. Ular Bilgin Ibryam va Roland Huss'ning "Kubernetes Patterns" ishida tizimlashtirilgan va aslida deklarativ infratuzilma bilan ishlashning umumiy tilini beradi: ilova o'z talablarini oldindan e'lon qiladi, platforma esa joylashtirish, qayta ishga tushirish va masshtablashni o'z zimmasiga oladi. Arxitektor uchun bu muhim, chunki Spring Boot ilovasining kodi mukammal bo'lsa ham, noto'g'ri e'lon qilingan resurs limitlari, probe'lar yoki graceful shutdown sozlamalari butun relizni beqaror qiladi. Shuning uchun bu bo'limdagi patternlarni "YAML detallari" deb emas, ilova arxitekturasining tashqi kontrakti deb qarash kerak.

## 29.1 Oldindan aytib beriladigan talablar (Predictable Demands)

**Tavsif:** Har bir konteyner o'zi talab qiladigan CPU, xotira, disk va platforma imkoniyatlarini aniq e'lon qilishi kerak, aks holda scheduler to'g'ri node tanlay olmaydi va cluster beqaror bo'ladi. Pattern `resources.requests` (kafolatlangan minimum, scheduling uchun asos) va `resources.limits` (yuqori chegara, uni oshsa CPU throttling yoki OOMKill) orqali amalga oshiriladi. Shuningdek ilova o'zining runtime bog'liqliklarini - ConfigMap, Secret, PersistentVolumeClaim, maxsus node imkoniyatlarini - deklarativ ravishda ko'rsatadi. Natijada platforma ilovaning "ishtahasi"ni biladi va QoS klassi (Guaranteed, Burstable, BestEffort) aniq bo'ladi.

**Spring'da qayerda uchraydi:** Bu birinchi navbatda infratuzilma darajasidagi pattern, lekin JVM uchun hayotiy muhim: Java 17-25 konteynerni taniydi (`UseContainerSupport` sukut bo'yicha yoqilgan) va `MaxRAMPercentage` orqali heap'ni konteyner limitidan foizda hisoblaydi - shuning uchun `limits.memory` ni e'lon qilmaslik JVM'ga butun node xotirasini ko'rsatadi. Spring Boot 3.x/4.x'da `bootBuildImage` (Gradle) yoki `spring-boot-maven-plugin`'ning `build-image` goal'i Paketo buildpack'lar bilan image yasaydi, Paketo'ning Memory Calculator esa heap, metaspace, thread stack va direct memory'ni konteyner limiti va `BPL_JVM_THREAD_COUNT` asosida avtomatik taqsimlaydi. Haqiqiy talabni o'lchash uchun `spring-boot-starter-actuator` va Micrometer'ning `jvm.memory.used`, `jvm.threads.live`, `process.cpu.usage` metrikalaridan foydalaniladi; CDS/AOT (`spring-boot-starter-parent` AOT plugin'i) yoki GraalVM native image esa talabni sezilarli kamaytiradi.

**Qo'llanish keyslari:**
- Spring Boot REST servisi uchun `requests.memory` ni haqiqiy RSS asosida o'lchab, `limits.memory` ni OOMKill'siz ishlaydigan darajada belgilash.
- Batch yoki reporting ilovasiga katta `limits.cpu` berib, scheduler'ni `requests` bilan ortiqcha bloklamaslik.
- Latency sezgir to'lov servisini Guaranteed QoS'ga chiqarish uchun `requests` va `limits` ni teng qilib qo'yish.
- Kafka consumer ilovasida thread pool o'lchamini konteynerga berilgan CPU soniga moslab, `BPL_JVM_THREAD_COUNT` ni to'g'rilash.
- Native image'ga o'tgan servis uchun xotira `requests` ni bir necha barobar kamaytirib, node zichligini oshirish.

**Ehtiyot bo'ling:** Eng ko'p uchraydigan xato - `limits.memory` ni heap hajmiga teng qilib qo'yish: metaspace, thread stack, code cache va native buffer'lar hisobga olinmaydi va pod kutilmaganda OOMKill bo'ladi. CPU `limits` ni haddan tashqari past belgilash esa JVM startup va GC'ni throttling qilib, readiness probe'ni muddatidan oldin yiqitadi.

## 29.2 Deklarativ joylashtirish (Declarative Deployment)

**Tavsif:** Reliz jarayonini qo'lda skriptlar bilan boshqarish o'rniga, kerakli yakuniy holat (image versiyasi, replica soni, update strategiyasi) deklarativ tarzda e'lon qilinadi va controller uni bosqichma-bosqich amalga oshiradi. Kubernetes'da bu `Deployment` resursi va uning `RollingUpdate` (`maxSurge`, `maxUnavailable`) yoki `Recreate` strategiyasi; Blue-Green va Canary esa qo'shimcha Service/label manipulyatsiyasi yoki Argo Rollouts kabi vositalar bilan quriladi. Pattern'ning asosiy sharti - ilovaning readiness signalini halol berishi, aks holda rolling update buzilgan versiyani trafikga chiqaradi. Rollback ham deklarativ: avvalgi ReplicaSet'ga qaytish.

**Spring'da qayerda uchraydi:** Spring Boot 3.x/4.x Actuator Kubernetes probe'larini nativ qo'llaydi: `management.endpoint.health.probes.enabled=true` bilan `/actuator/health/liveness` va `/actuator/health/readiness` guruhlari paydo bo'ladi (Kubernetes muhitida avtomatik aniqlanadi). Ilova kodi `ApplicationAvailability` interfeysi orqali holatni o'qiydi, `AvailabilityChangeEvent.publish(context, ReadinessState.REFUSING_TRAFFIC)` yoki `LivenessState.BROKEN` orqali uni o'zgartiradi. Konfiguratsiya tomonda Helm chart yoki Kustomize overlay'lar ishlatiladi, Spring Cloud Kubernetes'ning `spring-cloud-kubernetes-config` moduli esa ConfigMap/Secret'ni Environment'ga ulaydi - shuning uchun konfiguratsiya o'zgarishi ham deklarativ reliz qismiga aylanadi. Canary'da Spring Cloud Gateway yoki service mesh trafikni versiyalar orasida taqsimlaydi.

**Qo'llanish keyslari:**
- Monolit Spring Boot ilovasining yangi versiyasini `maxUnavailable: 0` bilan nol downtime chiqarish.
- Schema migratsiyasi (Flyway) bilan kelayotgan relizni `Recreate` strategiyasi orqali ikki versiyani bir vaqtda ishlatmaslik.
- Yangi tavsiya algoritmini 5% trafikda canary sifatida sinab ko'rish.
- GitOps (Argo CD, Flux) orqali Deployment manifestini Git'dan avtomatik sinxronlash.
- Muammoli relizni `kubectl rollout undo` bilan avvalgi ReplicaSet'ga qaytarish.

**Ehtiyot bo'ling:** Readiness probe sifatida to'liq `/actuator/health` ni ishlatish xavfli: tashqi bog'liqlik (masalan, tashqi API) pasayganda sog'lom pod'lar trafikdan chiqarilib, kaskad uzilish yuzaga keladi. Shuningdek orqaga mos kelmaydigan DB migratsiyasi bilan rolling update birga ishlamaydi - bu holda expand/contract migratsiyasi majburiy.

## 29.3 Boshqariladigan hayot sikli (Managed Lifecycle)

**Tavsif:** Konteyner platformadan keladigan hayot sikli signallarini - `SIGTERM`, `SIGKILL`, `postStart` va `preStop` hook'larini - to'g'ri tinglashi va ularga mos javob berishi kerak. Kubernetes pod'ni o'chirganda avval Endpoint'dan olib tashlaydi, keyin `preStop` ni bajaradi, so'ng `SIGTERM` yuboradi va `terminationGracePeriodSeconds` tugagach `SIGKILL` qiladi. Ilova bu oynada yangi so'rovlarni qabul qilmasligi, lekin ishlayotganlarini tugatishi va resurslarni (connection pool, consumer, lock) toza yopishi lozim. Bu pattern'ga init container'lar bilan startup tartibini boshqarish ham kiradi.

**Spring'da qayerda uchraydi:** Spring Boot 3.x/4.x'da `server.shutdown=graceful` va `spring.lifecycle.timeout-per-shutdown-phase=30s` graceful shutdown'ni yoqadi: web server yangi ulanishni qabul qilishni to'xtatadi, mavjud so'rovlar tugaydi. Spring Framework 6.x darajasida `@PreDestroy`, `DisposableBean`, `SmartLifecycle` (`getPhase()` bilan to'xtatish tartibi) va `ContextClosedEvent` listener'lari ishlatiladi; `spring-kafka`'dagi `MessageListenerContainer` va `spring-rabbit` container'lari ham `SmartLifecycle` orqali to'xtaydi. Spring Boot `ApplicationContext`'ga shutdown hook'ni avtomatik registratsiya qiladi, shuning uchun `SIGTERM` to'g'ridan-to'g'ri `close()` ga olib keladi. Actuator'ning `shutdown` endpoint'i esa odatda Kubernetes muhitida kerak emas va o'chirilgan holda qoldirilishi afzal.

```java
@Component
class ConsumerLifecycle implements SmartLifecycle {
    private volatile boolean running;
    @Override public void start() { running = true; }
    @Override public void stop() { running = false; /* drain in-flight work */ }
    @Override public boolean isRunning() { return running; }
    @Override public int getPhase() { return Integer.MAX_VALUE; } // eng birinchi to'xtaydi
}
```

**Qo'llanish keyslari:**
- Rolling update vaqtida ishlayotgan HTTP so'rovlarni yo'qotmaslik uchun graceful shutdown yoqish.
- Kafka consumer'ning offset'ini commit qilib, rebalans bo'ronini kamaytirish.
- `preStop` da bir necha sekundlik kutish qo'yib, Endpoint propagatsiyasi kechikishini qoplash.
- Init container orqali Flyway migratsiyasini ilova pod'laridan oldin bajarish.
- Uzoq davom etadigan batch ishini SIGTERM'da nazorat ostida to'xtatib, keyin davom ettirish mumkin holatga keltirish.

**Ehtiyot bo'ling:** `terminationGracePeriodSeconds` ni Spring'ning shutdown timeout'idan kichik qoldirish eng jimjit xatolardan biri - pod `SIGKILL` oladi va graceful shutdown mantiqi hech qachon tugamaydi. Shuningdek `@PreDestroy` ichida bloklovchi tashqi chaqiruvlar qilish o'chirish vaqtini cho'zadi va deploy'ni sekinlashtiradi.

## 29.4 Avtomatlashtirilgan joylashtirish (Automated Placement)

**Tavsif:** Pod'lar qaysi node'ga tushishini inson emas, scheduler hal qiladi: u resurs `requests`, node sig'imi, affinity/anti-affinity qoidalari, taint/toleration va topologiya cheklovlariga qarab qaror chiqaradi. `nodeSelector` va `nodeAffinity` qaysi node sinfi mosligini, `podAntiAffinity` bir xil ilovaning replica'larini ajratishni, `topologySpreadConstraints` esa zonalar bo'ylab teng tarqalishni ta'minlaydi. `taints`/`tolerations` maxsus node pool'larni (GPU, spot instance) himoyalaydi. Pattern maqsadi - yuqori mavjudlik va resurslardan samarali foydalanishni deklarativ qoidalar bilan birlashtirish.

**Spring'da qayerda uchraydi:** Bu to'liq infratuzilma darajasidagi pattern, Spring'da hech qanday annotatsiya yoki sinf unga mas'ul emas - Spring ilovasi faqat "joylashtirishga qulay" bo'lishi kerak: stateless, tez startup qiladigan, node'ga bog'lanmagan. Spring Boot ilovasi bu qarorlarning natijasini bilib ishlashi mumkin: `env` orqali `spec.nodeName`, `metadata.labels['topology.kubernetes.io/zone']` yoki `status.hostIP` ni Downward API bilan olib, ularni Micrometer'ning `MeterRegistryCustomizer` yordamida umumiy tag sifatida qo'shish, yoki `spring.application.name` bilan birga trace attribute'ga chiqarish amaliyoti keng tarqalgan. Zonaga yaqin trafik kerak bo'lsa, Spring Cloud LoadBalancer'ning zone-aware tanlovi (`spring.cloud.loadbalancer.zone` property'si) yoki service mesh'ning locality routing'i ishlatiladi.

**Qo'llanish keyslari:**
- To'lov servisining 3 replica'sini `podAntiAffinity` bilan uchta turli node'ga tarqatish.
- `topologySpreadConstraints` orqali replica'larni ikki availability zone o'rtasida teng bo'lish.
- GPU talab qiladigan Spring AI inference servisini faqat GPU node pool'ga `tolerations` bilan yo'naltirish.
- Spot node'larda faqat qayta ishga tushirishga chidamli batch ilovalarini ishlatish.
- Yuqori xotira talab qiladigan in-memory cache servisini memory-optimized node pool'ga biriktirish.

**Ehtiyot bo'ling:** Haddan tashqari qattiq qoidalar (`requiredDuringSchedulingIgnoredDuringExecution` ni hamma joyda ishlatish) pod'ning `Pending` holatda muzlab qolishiga olib keladi, ayniqsa kichik cluster'larda. Anti-affinity'ni PodDisruptionBudget bilan muvofiqlashtirmaslik esa node drain vaqtida servisning butunlay yo'qolishiga sabab bo'lishi mumkin.

## 29.5 Batch ishi (Batch Job)

**Tavsif:** Ba'zi ishlar doimiy servis emas, balki boshlanadi, vazifani bajaradi va tugaydi - bunday workload uchun Deployment emas, `Job` resursi mos keladi. `Job` konteyner muvaffaqiyatli tugashini (exit code 0) kuzatadi, `completions` va `parallelism` bilan nechta pod ishlashini, `backoffLimit` bilan qayta urinish sonini belgilaydi. `Indexed` completion mode esa har bir pod'ga o'z indeksini berib, ma'lumotni bo'laklab qayta ishlashga imkon beradi. Asosiy shart - ish idempotent bo'lishi, chunki pod qayta ishga tushishi mumkin.

**Spring'da qayerda uchraydi:** Spring Batch 5.x (Spring Boot 3.x/4.x bilan) bu pattern'ning tabiiy sherigi: `@EnableBatchProcessing` yoki `DefaultBatchConfiguration`, `Job` va `Step` bean'lari, `JobRepository`, `JobLauncher`, hamda `ItemReader`/`ItemProcessor`/`ItemWriter` zanjiri. Spring Boot `JobLauncherApplicationRunner` orqali startup'da job'ni ishga tushiradi; `spring.batch.job.name` bilan qaysi job ishlashi tanlanadi, `spring.batch.job.enabled=false` esa avtomatik ishga tushirishni o'chiradi. Konteyner to'g'ri exit code qaytarishi uchun `SpringApplication.exit(context, new JobExecutionExitCodeGenerator(...))` yoki `ExitCodeGenerator` ishlatiladi - aks holda `Job` muvaffaqiyatsiz step'ni ham "bajarildi" deb hisoblaydi. Spring Cloud Task (`@EnableTask`) qisqa muddatli ishlarni kuzatadi, Spring Batch'ning remote partitioning'i esa Kubernetes'da har bir partition uchun alohida pod yaratishi mumkin.

```java
public static void main(String[] args) {
    var ctx = SpringApplication.run(BatchApp.class, args);
    int code = SpringApplication.exit(ctx, new JobExecutionExitCodeGenerator());
    System.exit(code); // Job pattern uchun exit code hayotiy muhim
}
```

**Qo'llanish keyslari:**
- Kunlik hisob-kitob (billing) faylini qayta ishlab, natijani ma'lumotlar bazasiga yozish.
- Legacy tizimdan bir martalik ma'lumot migratsiyasini `Job` sifatida bajarish.
- Katta CSV import'ini `Indexed` Job va Spring Batch partitioning bilan parallel ishlatish.
- Hisobot generatsiyasini alohida pod'da bajarib, asosiy servis resurslarini bo'shatish.
- ML model uchun feature'larni oldindan hisoblab, object storage'ga yozish.

**Ehtiyot bo'ling:** `JobRepository` ni to'g'ri sozlamasdan Job'ni qayta ishga tushirish dublikat ma'lumotga olib keladi - idempotentlik va Spring Batch'ning restart semantikasi (bir xil `JobParameters` bir marta bajariladi) aniq o'ylangan bo'lishi kerak. Tugagan Job'larni tozalashni unutmang: `ttlSecondsAfterFinished` bo'lmasa, cluster ming-minglab tugagan pod bilan to'lib ketadi.

## 29.6 Davriy ish (Periodic Job)

**Tavsif:** Vaqt bo'yicha takrorlanadigan ishlar uchun `CronJob` resursi ishlatiladi: u cron ifodasi bo'yicha belgilangan vaqtda `Job` yaratadi. `concurrencyPolicy` (`Allow`, `Forbid`, `Replace`) avvalgi ish tugamagan holatda nima qilishni, `startingDeadlineSeconds` esa kechikkan ishni hali ham ishga tushirish kerakligini belgilaydi. `successfulJobsHistoryLimit` va `failedJobsHistoryLimit` tarixni cheklaydi. Pattern'ning qiymati - rejalashtirishni ilovadan platformaga ko'chirish, shu bilan ilovaning o'zi oddiy bir martalik protsessga aylanadi.

**Spring'da qayerda uchraydi:** Ikki alternativ yondashuv bor. Birinchisi - rejalashtirishni Kubernetes `CronJob`'ga berib, Spring Boot ilovasini bir martalik protsess sifatida (Spring Batch yoki `ApplicationRunner`/`CommandLineRunner` bilan) yozish; bu holda `spring.main.web-application-type=none` qo'yiladi. Ikkinchisi - rejalashtirishni ilova ichida qoldirish: `@EnableScheduling` va `@Scheduled(cron = "...", zone = "...")`, `ThreadPoolTaskScheduler`, Spring Framework 6.x'dan `@Scheduled` ustida `scheduler` atributi va virtual thread'lar (`spring.threads.virtual.enabled=true`, Java 21+). Lekin bir nechta replica bo'lsa, `@Scheduled` har bir pod'da ishlaydi - shuning uchun ShedLock (`@SchedulerLock`), Quartz'ning JDBC JobStore clustering rejimi (`spring-boot-starter-quartz`, `spring.quartz.job-store-type=jdbc`) yoki Spring Integration'ning `LockRegistry` si kerak bo'ladi.

**Qo'llanish keyslari:**
- Har kuni ertalab 03:00 da kechagi tranzaksiyalarni jamlab reconciliation hisobotini yasash.
- Har 15 daqiqada tashqi hamkor API'sidan narx ro'yxatini tortib olish.
- Haftalik eski audit log'larni arxivga ko'chirish va bazani tozalash.
- Har soatda materialized view yoki cache'ni qayta hisoblash.
- Oylik invoyslarni generatsiya qilib, email navbatiga qo'yish.

**Ehtiyot bo'ling:** `concurrencyPolicy: Allow` (sukut qiymat) sekin ishlayotgan job'larning bir-biriga minib ketishiga olib keladi - moliyaviy jarayonlarda bu dublikat yozuv degani, shuning uchun `Forbid` yoki ilova darajasidagi lock majburiy. Bir nechta replica'li Deployment ichida oddiy `@Scheduled` ni distributed lock'siz ishlatish esa ishni har bir pod'da takrorlaydi.

## 29.7 Demon servis (Daemon Service)

**Tavsif:** Ba'zi komponentlar har bir node'da aynan bitta nusxada ishlashi kerak - log yig'ish, metrika eksport qilish, tarmoq yoki storage agentlari shunday. Kubernetes'da bu `DaemonSet` orqali amalga oshiriladi: har bir (yoki selector'ga mos) node'ga bitta pod joylashtiriladi va yangi node qo'shilganda avtomatik yana bitta yaratiladi. Bunday pod'lar odatda node'ning fayl tizimiga yoki tarmog'iga kengaytirilgan huquq bilan kiradi va `hostNetwork`, `hostPath` kabi imkoniyatlardan foydalanadi. Bu infratuzilma workload'i bo'lib, foydalanuvchi trafigini qabul qilmaydi.

**Spring'da qayerda uchraydi:** Biznes Spring Boot ilovasi deyarli hech qachon DaemonSet sifatida ishlatilmaydi - bu pattern asosan Fluent Bit, OpenTelemetry Collector (agent rejimi), Prometheus Node Exporter, CSI va CNI agentlari uchun. Spring ilovasi esa bu agentlardan iste'molchi sifatida foydalanadi: Micrometer'ning `micrometer-registry-otlp` yoki `micrometer-registry-prometheus` moduli bilan metrikani chiqaradi, Micrometer Tracing (`micrometer-tracing-bridge-otel`) va OTLP exporter orqali trace yuboradi. Node-local collector'ga yo'naltirish uchun Downward API bilan `status.hostIP` ni env o'zgaruvchiga olib, `management.otlp.tracing.endpoint` yoki `management.otlp.metrics.export.url` da ishlatiladi; log'lar esa Logback'ning STDOUT appender'iga (odatda JSON encoder bilan) yoziladi va DaemonSet agenti ularni fayl tizimidan yig'ib oladi.

**Qo'llanish keyslari:**
- Spring Boot ilovasining STDOUT JSON log'larini har node'dagi Fluent Bit agenti orqali markaziy log tizimiga uzatish.
- OTLP trace'larni node-local OpenTelemetry Collector'ga yuborib, tarmoq kechikishini kamaytirish.
- Node darajasidagi CPU va disk metrikalarini Node Exporter bilan yig'ib, ilova metrikalari bilan bir dashboard'da ko'rish.
- Barcha node'larda xavfsizlik agentini (runtime threat detection) ishlatish.
- CSI driver agenti orqali Spring ilovasiga PersistentVolume mount qilish imkonini berish.

**Ehtiyot bo'ling:** DaemonSet pod'lari har bir node'dan resurs "o'g'irlaydi" - ularning `requests` ini hisobga olmaslik ilova pod'lari uchun joy qolmasligiga olib keladi. Shuningdek biznes servisini "har node'da bittadan bo'lsin" degan niyatda DaemonSet'ga qo'yish masshtablashni node soniga bog'lab qo'yadi va HPA bilan boshqarishni yo'qotadi.

## 29.8 Yakka servis (Singleton Service)

**Tavsif:** Ba'zi ishlar butun cluster bo'ylab aynan bir martada bajarilishi kerak: rejalashtiruvchi, message poller, yoki tashqi tizim bilan yakka ulanishni boshqaruvchi komponent. Pattern'ning ikki ko'rinishi bor: out-of-application lock (ilovadan tashqaridagi koordinatsiya - StatefulSet'da `replicas: 1`, bu holda Kubernetes bitta nusxani kafolatlaydi, lekin mavjudlik pasayadi) va in-application lock (bir nechta replica ishlaydi, lekin faqat biri leader bo'lib ishni bajaradi). Ikkinchisi yuqori mavjudlikni saqlaydi, chunki leader yiqilsa boshqasi uning o'rnini egallaydi. Tanlov leader election mexanizmining ishonchliligiga bog'liq.

**Spring'da qayerda uchraydi:** In-application variant uchun Spring Integration'ning leader election abstraksiyasi ishlatiladi: `org.springframework.integration.leader.Candidate`, `LeaderInitiator` va `OnGrantedEvent`/`OnRevokedEvent` hodisalari, `spring-integration-zookeeper` yoki Hazelcast asosidagi implementatsiyalar. Oddiyroq yechim - `LockRegistry` interfeysi va uning `JdbcLockRegistry` (`spring-integration-jdbc`), `RedisLockRegistry` (`spring-integration-redis`) implementatsiyalari. Rejalashtirilgan ishlar uchun eng ko'p tarqalgan amaliyot - ShedLock kutubxonasi (`@SchedulerLock`, `LockProvider` sifatida JDBC yoki Redis) yoki Quartz'ning clustered JDBC JobStore'i, u bir vaqtda faqat bitta node'da trigger'ni ishga tushiradi. Spring Cloud Kubernetes'da ConfigMap asosidagi leader election moduli ham mavjud, lekin ko'p loyihalarda ShedLock yoki Quartz amalda ishonchliroq tanlov bo'lib qolgan.

```java
@Scheduled(cron = "0 */5 * * * *")
@SchedulerLock(name = "outboxPublisher", lockAtMostFor = "4m", lockAtLeastFor = "30s")
void publishOutbox() { outboxService.publishPending(); } // faqat bitta pod bajaradi
```

**Qo'llanish keyslari:**
- Outbox jadvalidan xabar yuboruvchi publisher'ni ko'p replica'li ilovada faqat bitta pod'da ishlatish.
- Tashqi SFTP serverdan fayl tortib olishni bir vaqtda bitta nusxada bajarish.
- Kunlik reconciliation job'ini dublikatsiz ishga tushirish.
- Legacy tizim bilan yakka long-lived ulanishni (masalan, bitta JMS consumer) ushlab turish.
- Cache'ni qayta qurish (cache warm-up) vazifasini bir pod'ga yuklab, bazani ortiqcha yuklamaslik.

**Ehtiyot bo'ling:** Faqat `replicas: 1` ga tayanish xavfli: node drain yoki rolling update vaqtida qisqa muddat ikkita pod birga yashashi mumkin, shuning uchun haqiqiy "aynan bir marta" kafolati ilova darajasidagi lock yoki idempotentlik bilan ta'minlanadi. Lock timeout'ini ishning haqiqiy davomiyligidan kichik qo'yish esa ikki pod'ning bir vaqtda ishlashiga yo'l ochadi.

## 29.9 Stateless servis (Stateless Service)

**Tavsif:** Stateless servis o'zida hech qanday muhim holat saqlamaydi: har bir so'rovni mustaqil qayta ishlaydi, holatni tashqi store'ga (DB, Redis, object storage) yozadi. Shu sababli uning nusxalari bir-biriga aynan o'xshash, almashtirilishi mumkin va erkin masshtablanadi - Kubernetes'da bu `Deployment` + `ReplicaSet` va `HorizontalPodAutoscaler` kombinatsiyasi. Pod har qanday paytda o'ldirilishi yoki boshqa node'da qayta tug'ilishi mumkin, bu esa relizni, autoscaling'ni va node almashtirishni osonlashtiradi. Bu cloud-native ilovaning asosiy (default) shakli.

**Spring'da qayerda uchraydi:** Spring Boot web ilovalari sukut bo'yicha deyarli stateless, lekin HTTP session ishlatilsa holat paydo bo'ladi - buni Spring Session (`spring-session-data-redis` va `@EnableRedisHttpSession`, yoki `spring-session-jdbc`) orqali tashqariga chiqarish kerak. Autentifikatsiyada Spring Security 6.x bilan JWT yoki opaque token (`oauth2ResourceServer()`) ishlatilsa, server tomonda sessiya saqlanmaydi (`SessionCreationPolicy.STATELESS`). Lokal holatdan qutulish uchun: fayllarni local disk o'rniga S3/object storage'ga yozish, local cache o'rniga `spring-boot-starter-data-redis` bilan `@Cacheable` ni markaziy cache'ga ulash, `@Scheduled` ishlarini lock bilan himoyalash. Vaqtinchalik fayllar uchun `emptyDir` volume yetarli. Tez masshtablash uchun startup vaqtini qisqartirish muhim: Spring Boot 3.x AOT, CDS yoki GraalVM native image.

**Qo'llanish keyslari:**
- Public REST API gateway'ini HPA bilan CPU yoki so'rov soniga qarab avtomatik masshtablash.
- Mahsulot katalogi servisini bir nechta zonada ko'p replica bilan ishlatib, node yo'qolishiga chidamli qilish.
- Session'ni Redis'ga chiqarib, sticky session va load balancer affinity'dan voz kechish.
- Fayl yuklash servisida yuklangan faylni darhol object storage'ga uzatib, pod diskini bo'shatish.
- Spot node'larda ishlaydigan read-only query servisini arzon resurslarda ishlatish.

**Ehtiyot bo'ling:** "Stateless" deb e'lon qilingan servisda yashirin holat tez-tez qoladi: local in-memory cache (Caffeine) nomuvofiqlikka, local fayl yozuvi esa pod o'lganda ma'lumot yo'qolishiga olib keladi. HPA ni sozlashdan oldin startup vaqtini va `requests` ni to'g'rilash kerak, aks holda scale-out trafik cho'qqisiga ulgurmaydi.

## 29.10 Stateful servis (Stateful Service)

**Tavsif:** Ba'zi komponentlar o'z identifikatsiyasi, barqaror tarmoq nomi va o'ziga tegishli doimiy diski bilan yashashi kerak - ma'lumotlar bazalari, message broker'lar, cluster'li cache'lar shunday. Kubernetes'da buning uchun `StatefulSet` bor: har bir pod barqaror tartibli nom (`app-0`, `app-1`), headless Service orqali barqaror DNS yozuvi va `volumeClaimTemplates` orqali o'ziga tegishli PersistentVolumeClaim oladi. Pod'lar tartib bilan ishga tushadi va teskari tartibda to'xtaydi, qayta tug'ilganda esa o'sha indeks va o'sha disk bilan qaytadi. Bu peer discovery va ma'lumot joylashuvini talab qiladigan tizimlar uchun zarur.

**Spring'da qayerda uchraydi:** Spring ilovasi odatda stateful emas, u StatefulSet ichida ishlaydigan tizimlarga mijoz bo'ladi: `spring-boot-starter-data-jpa` PostgreSQL'ga, `spring-kafka` Kafka cluster'iga, `spring-boot-starter-data-redis` Redis'ga, `spring-data-mongodb` MongoDB replica set'iga ulanadi - bu holda ulanish satrida headless Service orqali berilgan barqaror DNS nomlari ishlatiladi. Spring ilovasining o'zi stateful bo'lgan holatlar ham bor: Kafka Streams (`spring-kafka`'ning `StreamsBuilderFactoryBean`, `@EnableKafkaStreams`) local state store va RocksDB uchun doimiy disk talab qiladi - `state.dir` ni PVC'ga yo'naltirish rebalans vaqtida qayta tiklanishni keskin tezlashtiradi. Hazelcast yoki Infinispan embedded cluster'li Spring ilovasi ham barqaror peer identifikatsiyasidan foyda ko'radi.

**Qo'llanish keyslari:**
- Kafka Streams asosidagi Spring Boot ilovasining RocksDB state store'ini PVC'da saqlab, restart'dan keyin tez tiklanish.
- PostgreSQL yoki Kafka cluster'ini cluster ichida StatefulSet bilan ishlatib, Spring ilovasini unga headless DNS orqali ulash.
- Elasticsearch/OpenSearch node'larini barqaror disk va identifikatsiya bilan ko'tarish.
- Hazelcast embedded cluster'li Spring ilovasida peer discovery'ni barqaror pod nomlari orqali qurish.
- Zookeeper quorum'ini `replicas: 3` bilan tartibli ishga tushirish.

**Ehtiyot bo'ling:** Ishlab chiqarishda ma'lumotlar bazasini Kubernetes'da o'zi qo'lda boshqarish (operator'siz, backup va failover strategiyasisiz) jiddiy xavf - ko'p holatda managed DB yoki yetuk operator afzal. StatefulSet'ni oddiy stateless Spring servisi uchun "ehtiyot shart" ishlatish esa deploy'ni sekinlashtiradi va masshtablashni qiyinlashtiradi, foyda bermaydi.

## 29.11 Servis topish (Service Discovery (Kubernetes view))

**Tavsif:** Pod'lar vaqtinchalik va ularning IP manzillari doimiy o'zgaradi, shuning uchun mijoz manzilni qattiq yozib qo'yolmaydi. Kubernetes bu muammoni `Service` abstraksiyasi bilan hal qiladi: ClusterIP va barqaror DNS nomi (`<service>.<namespace>.svc.cluster.local`) ortida Endpoint/EndpointSlice ro'yxati dinamik yangilanadi va kube-proxy trafikni sog'lom pod'larga taqsimlaydi. Tashqi trafik uchun `Ingress` yoki Gateway API, cluster ichidagi peer discovery uchun esa headless Service ishlatiladi. Natijada mijoz uchun discovery oddiy DNS so'roviga aylanadi.

**Spring'da qayerda uchraydi:** Eng oddiy va eng mustahkam yondashuv - hech qanday discovery client'siz, to'g'ridan-to'g'ri Service DNS nomiga murojaat: Spring Framework 6.x'dagi `RestClient` yoki `WebClient` bilan `http://order-service:8080/...`, yoki HTTP interface (`@HttpExchange` va `HttpServiceProxyFactory`). Kerak bo'lganda Spring Cloud Kubernetes'ning `spring-cloud-kubernetes-client-discovery` (yoki fabric8 varianti) moduli Spring Cloud'ning `DiscoveryClient`/`ReactiveDiscoveryClient` abstraksiyasini Kubernetes API ustiga quradi, `spring.cloud.kubernetes.discovery.enabled` bilan boshqariladi va Spring Cloud LoadBalancer (`@LoadBalanced WebClient.Builder`) bilan birga ishlaydi; `spring-cloud-kubernetes-discovery-server` esa discovery'ni alohida HTTP servis sifatida chiqaradi. Spring Cloud Gateway (Spring Boot 3.x) `lb://` sxemasi bilan discovery'ga tayangan routing qiladi, service mesh ishlatilsa esa discovery va retry butunlay sidecar'ga o'tadi.

**Qo'llanish keyslari:**
- Mikroservislar orasidagi chaqiruvlarni Service DNS nomi orqali `RestClient` bilan amalga oshirish.
- Spring Cloud Gateway'da marshrutlarni Kubernetes Service'lariga `lb://` orqali bog'lash.
- Headless Service bilan Hazelcast yoki Kafka Streams peer'larini topish.
- Eureka'dan Kubernetes-nativ discovery'ga ko'chishda `DiscoveryClient` abstraksiyasini saqlab, implementatsiyani almashtirish.
- Blue-Green relizda Service selector'ini o'zgartirib, trafikni yangi versiyaga bir qadamda yo'naltirish.

**Ehtiyot bo'ling:** Spring Cloud Kubernetes discovery client Kubernetes API'ga RBAC huquqi talab qiladi va qo'shimcha murakkablik qo'shadi - ko'p loyihalarda oddiy DNS yetarli bo'lgani uchun uni "shunchaki bo'lsin" deb qo'shish ortiqcha. Yana bir tuzoq - JVM'ning DNS cache'i va connection pool'ning eski IP'ni ushlab qolishi: `networkaddress.cache.ttl` va HTTP client'ning keep-alive sozlamalarini tekshirmasa, pod almashganda vaqtinchalik xatolar paydo bo'ladi.

## 29.12 O'z-o'zini anglash (Self Awareness)

**Tavsif:** Container ichidagi ilova ko'pincha o'zi haqidagi ma'lumotni - pod nomi, namespace, node nomi, pod IP, unga ajratilgan CPU/memory limitlari - bilishi kerak, lekin bu ma'lumot faqat Kubernetes API'da yashaydi. Self Awareness pattern bu ma'lumotni Downward API orqali container'ga env variable yoki mount qilingan fayl ko'rinishida yetkazadi, ilova esa Kubernetes API'ga umuman murojaat qilmasdan o'qiydi. Natijada ilova RBAC token va API client talab qilmaydi, lekin o'z identitetini biladi. Bu log'larni boyitish, tracing, leader election va shard'larga bo'lish uchun asos bo'ladi.

**Spring'da qayerda uchraydi:** Downward API bergan `POD_NAME`, `POD_NAMESPACE`, `NODE_NAME` kabi env variable'lar oddiy `Environment`/`@Value` yoki `@ConfigurationProperties` bilan o'qiladi; `resourceFieldRef` orqali berilgan CPU/memory limitlari ham xuddi shunday keladi. `downwardAPI` volume sifatida mount qilingan label va annotation fayllarini Spring Boot 2.4+ dagi `spring.config.import=optional:configtree:/etc/podinfo/` bilan to'g'ridan-to'g'ri property source'ga aylantirish mumkin. Spring Cloud Kubernetes'da `org.springframework.cloud.kubernetes.commons.PodUtils` joriy pod'ni aniqlaydi, `spring.cloud.kubernetes.client.namespace` esa namespace'ni beradi. Micrometer `MeterRegistryCustomizer` bilan `commonTags("pod", podName, "namespace", ns)` qo'shilsa, barcha metrikalar pod bo'yicha ajratiladi; Logback MDC yoki `logging.pattern.level` ichida ham shu qiymatlar ishlatiladi.

```java
@Bean
MeterRegistryCustomizer<MeterRegistry> podTags(
        @Value("${POD_NAME:unknown}") String pod,
        @Value("${POD_NAMESPACE:default}") String ns) {
    return registry -> registry.config().commonTags("pod", pod, "namespace", ns);
}
```

**Qo'llanish keyslari:**
- Prometheus metrikalariga `pod` va `namespace` tag'larini qo'shib, muammoli instansni aniqlash.
- Strukturali log'larga pod nomi va node nomini MDC orqali yozib, markazlashgan log tizimida filtrlash.
- Batch ishni shard'larga bo'lishda StatefulSet pod ordinalidan (`myapp-3`) partition raqamini olish.
- Ajratilgan memory limitidan kelib chiqib cache hajmini yoki thread pool o'lchamini runtime'da sozlash.
- Distributed tracing span'lariga infratuzilma atributlarini (`k8s.pod.name`) qo'shish.

**Ehtiyot bo'ling:** Downward API faqat o'z pod'i haqidagi statik ma'lumotni beradi - pod yaratilgandan keyin o'zgargan label'lar env variable'da yangilanmaydi (faqat volume faylida yangilanadi), shuning uchun dinamik qiymatlarni env orqali kutmang. Pod nomini biznes identifikator yoki idempotentlik kaliti sifatida ishlatish xato: pod har restartda yangi nom oladi.

## 29.13 Elastik masshtablash (Elastic Scale)

**Tavsif:** Yuklama kun bo'yi va mavsum bo'yi o'zgaradi, statik replica soni esa yoki pul yondiradi, yoki peak'da sinadi. Elastic Scale pattern masshtablashni gorizontal (HPA - replica sonini metrika asosida o'zgartirish), vertikal (VPA - request/limit'ni moslash) va klaster darajasida (Cluster Autoscaler - node qo'shish) avtomatlashtiradi. Ilova esa bunga tayyor bo'lishi kerak: tez ishga tushishi, stateless bo'lishi va SIGTERM'ni to'g'ri qabul qilishi shart.

**Spring'da qayerda uchraydi:** HPA'ning o'zi Kubernetes infratuzilma komponenti - Spring'da sinfi yo'q; Spring ilovasi unga metrika va to'g'ri lifecycle berib tayanadi. Micrometer `micrometer-registry-prometheus` va Actuator'ning `/actuator/prometheus` endpoint'i custom metrikalarni chiqaradi, ularni Prometheus Adapter yoki KEDA (`ScaledObject`) HPA uchun manbaga aylantiradi - masalan Kafka consumer lag yoki `queue.depth` gauge. Scale-in paytida ma'lumot yo'qolmasligi uchun Spring Boot'da `server.shutdown=graceful` va `spring.lifecycle.timeout-per-shutdown-phase=30s` yoqiladi, Actuator'ning `management.endpoint.health.probes.enabled=true` bilan `/actuator/health/readiness` va `/actuator/health/liveness` probe'lari ulanadi, `ApplicationAvailability` va `AvailabilityChangeEvent` bilan readiness kodda boshqariladi. Startup vaqtini qisqartirish uchun Spring Boot 3.x'da AOT + GraalVM native image, CDS (Boot 3.3+, `-XX:SharedArchiveFile`) va CRaC checkpoint (`-Dspring.context.checkpoint=onRefresh`) ishlatiladi; `spring.main.lazy-initialization=true` ham yordam beradi.

**Qo'llanish keyslari:**
- Black Friday peak'ida HTTP RPS yoki p99 latency bo'yicha order-service replica'larini 4 dan 40 ga oshirish.
- Kafka consumer lag asosida KEDA bilan worker'larni skale qilish va tun bo'yi nolga tushirish (scale-to-zero).
- Batch/ETL job'lar uchun kechasi Cluster Autoscaler orqali qo'shimcha node'larni avtomatik olish.
- VPA'ning recommender rejimidan foydalanib Spring Boot servislarining real memory request'ini kalibrlash.
- Native image yoki CRaC bilan cold start'ni sekundlardan millisekundlarga tushirib, agressiv HPA'ni mumkin qilish.

**Ehtiyot bo'ling:** Stateful yoki in-memory session/cache'ga tayangan ilovani gorizontal skale qilish ma'lumot yo'qotishga olib keladi - avval holatni Redis yoki DB'ga chiqaring. HPA va VPA'ni bir xil resurs (ayniqsa CPU) bo'yicha birga ishlatish ikki kontrollerning kurashiga va tebranishga (thrashing) sabab bo'ladi; `stabilizationWindowSeconds` va PodDisruptionBudget'ni albatta sozlang.

## 29.14 Image quruvchi (Image Builder)

**Tavsif:** Container image'ni qurish an'anaviy ravishda CI serverida, Docker daemon va root huquqi bilan bajariladi - bu xavfsizlik va portativlik muammosi. Image Builder pattern image qurishni klaster ichidagi oddiy workload'ga aylantiradi: daemonsiz, root'siz builder'lar (Kaniko, Buildah) yoki deklarativ Cloud Native Buildpacks Dockerfile'ni ham keraksiz qiladi. Natijada build jarayoni bir xil klasterda, bir xil RBAC va resource limitlari ostida, takrorlanadigan (reproducible) tarzda kechadi.

**Spring'da qayerda uchraydi:** Spring Boot 3.x Maven/Gradle plugin'ida `spring-boot:build-image` / `bootBuildImage` task'i Cloud Native Buildpacks (Paketo) yordamida Dockerfile'siz OCI image quradi; `BP_JVM_VERSION`, `BP_NATIVE_IMAGE=true`, `BP_JVM_CDS_ENABLED` kabi env'lar bilan boshqariladi va `publish=true` bilan to'g'ridan-to'g'ri registry'ga push qiladi. Alternativa - Google `jib-maven-plugin`/`jib-gradle-plugin`, u ham daemonsiz layered image yasaydi. Dockerfile yozilsa, Spring Boot'ning layered jar mexanizmi (`spring-boot-jarmode-tools` Boot 3.3+, undan oldin `spring-boot-jarmode-layertools`) `dependencies`, `spring-boot-loader`, `snapshot-dependencies`, `application` qatlamlariga ajratib, cache'ni samarali qiladi. Klaster ichida build uchun Tekton, Argo Workflows yoki Kaniko pod'lari ishlatiladi; Spring Boot ilovasining o'zida esa Testcontainers va `spring-boot-testcontainers` moduli build'ni real infra bilan tekshiradi.

**Qo'llanish keyslari:**
- Dockerfile'ni butunlay yo'q qilib, yuzlab microservice uchun bir xil Paketo buildpack bilan standart image yasash.
- GraalVM native image'ni `BP_NATIVE_IMAGE=true` bilan qurib, cold start va memory iste'molini kamaytirish.
- Layered jar bilan faqat `application` qatlamini yangilab, CI'da push vaqtini va registry trafigini qisqartirish.
- Kaniko pod'lari orqali daemonsiz, root'siz build qilib, PCI/ISO talablariga mos CI yaratish.
- Base image CVE chiqqanda ilovani qayta kompilyatsiya qilmasdan buildpack `rebase` bilan yangilash.

**Ehtiyot bo'ling:** Klaster ichidagi builder pod'lari registry credential'lariga ega bo'ladi - bu Secret'ni cheklangan namespace va ServiceAccount bilan izolyatsiya qiling, aks holda build infrastrukturasi supply-chain hujum nuqtasiga aylanadi. Buildpack'lar qulay, lekin ular tanlagan JVM, memory calculator va base OS sizning talablaringizga mos kelmasligi mumkin - production'da image tarkibini aniq pinlab va skanerlab turing.

## 29.15 Konfiguratsiya resursi (Configuration Resource)

**Tavsif:** Konfiguratsiyani image ichiga qotirib qo'yish bir image'ni bir necha muhitda ishlatish imkonini yo'qotadi. Configuration Resource pattern konfiguratsiyani Kubernetes'ning birinchi darajali obyektlariga - ConfigMap (oddiy sozlamalar) va Secret (maxfiy ma'lumot) - chiqaradi, ularni esa pod'ga env variable yoki mount qilingan volume orqali uzatadi. Shunday qilib bir xil image dev, staging va prod'da turlicha sozlanadi, konfiguratsiya o'zgarishi esa Git va RBAC nazorati ostida kechadi.

**Spring'da qayerda uchraydi:** Eng oddiy va eng ishonchli yo'l - Secret/ConfigMap'ni volume sifatida mount qilib, Spring Boot 2.4+ `spring.config.import=optional:configtree:/etc/config/` orqali har bir faylni property'ga aylantirish (`ConfigTreePropertySource`). Spring Cloud Kubernetes'da `spring-cloud-starter-kubernetes-client-config` (yoki Fabric8 varianti) ilovaga Kubernetes API'dan to'g'ridan-to'g'ri ConfigMap/Secret o'qish imkonini beradi - `spring.config.import=kubernetes:`, ichida `ConfigMapPropertySource` va `SecretsPropertySource` ishlatiladi; `spring.cloud.kubernetes.reload.enabled=true` bilan o'zgarishda context refresh yoki restart bajariladi. Bu holda pod'ning ServiceAccount'iga ConfigMap/Secret uchun RBAC `get`/`list`/`watch` huquqi kerak. Property'lar `@ConfigurationProperties` sinflariga bog'lanadi; `@RefreshScope` (Spring Cloud Context) bean'larni qayta yaratadi. Haqiqiy maxfiy ma'lumot uchun Secret yetarli emas (u faqat base64) - Spring Cloud Vault yoki External Secrets Operator bilan birlashtiriladi.

**Qo'llanish keyslari:**
- Bitta `order-service` image'ini dev/stage/prod'da turli DB URL va feature flag'lar bilan ishga tushirish.
- DB parol va API kalitlarini Secret'dan `configtree` orqali o'qib, env variable'larda ochiq qoldirmaslik.
- Feature toggle'ni ConfigMap'da o'zgartirib, `/actuator/refresh` yoki Spring Cloud Kubernetes reload bilan deploy'siz qo'llash.
- Logging darajasini (`logging.level.*`) ConfigMap orqali incident paytida vaqtincha `DEBUG`ga o'tkazish.
- GitOps (Argo CD / Flux) bilan konfiguratsiyani Git'da versiyalab, audit va rollback olish.

**Ehtiyot bo'ling:** Secret'ni env variable qilib bersangiz, u `/proc`, crash dump va `kubectl describe pod` chiqishida oson ko'rinadi - volume mount'ni afzal ko'ring va etcd shifrlashni yoqing. `reload` rejimini o'ylamasdan yoqish xavfli: `restart_context` yoki `refresh` bean'larni yarmida qayta yaratib, trafik ostida kutilmagan holatga olib kelishi mumkin, bundan tashqari har bir pod API serverga watch ochadi.

## 29.16 O'zgarmas konfiguratsiya (Immutable Configuration)

**Tavsif:** Konfiguratsiya runtime'da jimgina o'zgarsa, ishlab turgan tizim endi Git'dagi haqiqatga mos kelmaydi va muammoni takrorlash imkonsiz bo'ladi. Immutable Configuration pattern konfiguratsiyani deploy artefaktining o'zgarmas qismiga aylantiradi: u image ichiga yoki alohida "config image"ga joylanadi va faqat yangi deploy orqali almashtiriladi. Natijada har bir versiya o'ziga xos, aniq, takrorlanadigan konfiguratsiyaga ega bo'ladi va rollback konfiguratsiyani ham qaytaradi.

**Spring'da qayerda uchraydi:** Spring Boot'da profile'ga bog'langan `application-prod.yaml` fayllarini jar yoki image ichiga qo'shish - eng tabiiy amalga oshirish; `spring.config.activate.on-profile` va `spring.profiles.active` bilan boshqariladi, `spring.config.import` bilan `classpath:` manbalari qo'shiladi. Alohida config artefaktini init container (yoki Kubernetes 1.29+ native sidecar) orqali `emptyDir`ga ko'chirib, asosiy container'da `spring.config.additional-location=file:/config/` yoki `configtree:` bilan o'qish mumkin. Kubernetes tomonida ConfigMap/Secret'ga `immutable: true` maydoni (1.21+) qo'yiladi - bunda o'zgartirish uchun yangi nomli ConfigMap yaratib, Deployment'ni yangilash shart, bu esa rollout'ni avtomatik qiladi (Kustomize `configMapGenerator` hash suffix bilan shuni beradi). `spring.cloud.kubernetes.reload.enabled` bu patternga qarama-qarshi, shuning uchun o'chirilgan holda qoldiriladi.

**Qo'llanish keyslari:**
- Regulyator talab qiladigan muhitda har bir release'ning konfiguratsiyasini image digest bilan birga audit qilish.
- Kustomize `configMapGenerator` hash'i orqali konfiguratsiya o'zgarganda avtomatik, nazoratli rolling update olish.
- Rollback paytida kod bilan birga eski konfiguratsiyaning ham qaytishiga kafolat berish.
- `immutable: true` ConfigMap'lar bilan API server va kubelet yukini kamaytirish (watch'lar yo'qoladi).
- Bir xil binar artefaktni turli region uchun alohida config image bilan paketlab tarqatish.

**Ehtiyot bo'ling:** Maxfiy ma'lumotni hech qachon image ichiga qotirmang - image registry'dan chiqib ketsa, parol ham chiqadi; secret'lar har doim tashqi manbada (Secret, Vault, External Secrets) qolishi kerak. Immutable konfiguratsiya har kichik o'zgarish uchun to'liq rollout talab qiladi, shuning uchun tez-tez o'zgaradigan feature flag'lar uchun bu pattern noto'g'ri - ularni Configuration Resource yoki maxsus flag servisida saqlang.

## 29.17 Muhit o'zgaruvchilari orqali konfiguratsiya (EnvVar Configuration)

**Tavsif:** Env variable - konfiguratsiyani container'ga yetkazishning eng universal va eng kam bog'liqlikka ega usuli: u 12-Factor App tamoyiliga mos, har qanday til va runtime'da ishlaydi, hech qanday fayl yoki kutubxona talab qilmaydi. Kubernetes'da u `env`, ConfigMap/Secret'dan `valueFrom`, yoki butun resursni `envFrom` orqali beriladi. Ammo bu kanal tekis (nested struktura yo'q), faqat satr qiymatlarini qabul qiladi va pod ishga tushgandan keyin o'zgarmaydi.

**Spring'da qayerda uchraydi:** Spring Boot `Environment` ichidagi `SystemEnvironmentPropertySource` env variable'larni eng yuqori prioritetlardan birida o'qiydi va "relaxed binding" qiladi: `SPRING_DATASOURCE_URL` → `spring.datasource.url`, `APP_RETRY_MAXATTEMPTS` → `app.retry.max-attempts`. `@ConfigurationProperties` sinflari shu qiymatlarga avtomatik bog'lanadi, `@Value("${...}")` esa nuqtali nom bilan ishlaydi. `SPRING_APPLICATION_JSON` yoki `SPRING_APPLICATION_JSON`ga o'xshash `SPRING_CONFIG_IMPORT` bilan butun konfiguratsiya blokini uzatish mumkin. Massiv indekslari `MYAPP_HOSTS_0_NAME` ko'rinishida beriladi. JVM sozlamalari uchun `JAVA_TOOL_OPTIONS` va `JDK_JAVA_OPTIONS` env'lari ishlatiladi (Paketo buildpack memory calculator ham shu orqali ishlaydi), `SPRING_PROFILES_ACTIVE` esa profile'ni tanlaydi.

**Qo'llanish keyslari:**
- `SPRING_PROFILES_ACTIVE=prod` bilan bir image'ni muhitga qarab turlicha sozlash.
- `SPRING_DATASOURCE_URL` va `SPRING_DATASOURCE_USERNAME`ni ConfigMap'dan `envFrom` orqali butun blok sifatida ulash.
- `JAVA_TOOL_OPTIONS=-XX:MaxRAMPercentage=75` bilan JVM heap'ini container limitiga moslash.
- Downward API `fieldRef` qiymatlarini env sifatida berib, ilovaga pod identitetini uzatish.
- Sidecar yoki init container bilan umumiy `envFrom` ishlatib, bir necha container'da bir xil endpoint'larni e'lon qilish.

**Ehtiyot bo'ling:** Env variable pod umri davomida o'zgarmaydi - ConfigMap yangilansa ham qiymat eski qoladi, shuning uchun dinamik konfiguratsiya uchun yaramaydi. Parol va token'larni env orqali berish tavsiya etilmaydi: ular log'larda, `kubectl describe`da, crash dump va child process'larda oqib ketadi; bunday hollarda volume mount + `configtree:` ishlatish xavfsizroq.

## 29.18 Konfiguratsiya shabloni (Configuration Template)

**Tavsif:** Katta va takrorlanuvchi konfiguratsiya fayllari (masalan JVM sozlamalari, nginx yoki Logback konfiguratsiyasi) muhitlar bo'yicha faqat bir necha qiymat bilan farq qiladi - hammasini qo'lda nusxalash xatolar manbai. Configuration Template pattern yagona shablon saqlaydi va uni deploy yoki startup vaqtida muhitga xos qiymatlar bilan to'ldiradi. To'ldirish klasterdan tashqarida (Helm, Kustomize) yoki klaster ichida init container tomonidan (gomplate, envsubst) bajariladi.

**Spring'da qayerda uchraydi:** Spring'ning o'zi property darajasida shablonlashni qo'llab-quvvatlaydi: `application.yaml` ichida `${...}` placeholder'lar `PropertySourcesPlaceholderConfigurer` orqali yechiladi, `spring.config.activate.on-profile` va `application-{profile}.yaml` fayllari esa muhit bo'yicha ustma-ust (overlay) qo'yiladi. Logback uchun `logback-spring.xml` ichida `<springProperty>` va `<springProfile>` teglari aynan shablonlash vositasi. Kubernetes manifestlari darajasida Helm `values.yaml` + Go template yoki Kustomize overlay/patch ishlatiladi - bu Spring tashqarisidagi, infratuzilma darajasidagi mexanizm. Murakkab holatlarda init container shablonni render qilib `emptyDir`ga yozadi, ilova esa `spring.config.additional-location=file:/config/` bilan o'qiydi. Markazlashgan alternativa - Spring Cloud Config Server, u Git'dagi shablonlardan ilova nomi va profile bo'yicha konfiguratsiya yig'ib beradi.

**Qo'llanish keyslari:**
- Helm chart bilan 30 ta microservice uchun bitta Deployment shablonidan foydalanib, faqat `values.yaml`ni almashtirish.
- `logback-spring.xml` ichida `<springProfile name="prod">` bilan prod'da JSON, dev'da konsol log formatini berish.
- Kustomize overlay'lari orqali dev/stage/prod uchun replica soni va resurs limitlarini farqlash.
- Init container'da gomplate bilan uzun legacy `.properties` faylini ConfigMap qiymatlaridan render qilish.
- Multi-tenant SaaS'da har bir tenant namespace'i uchun bir shablondan konfiguratsiya generatsiya qilish.

**Ehtiyot bo'ling:** Shablonlashni haddan oshirish ("template of templates", chuqur Helm `if/range` mantiqi) manifestlarni o'qilmas qiladi va render natijasi faqat deploy paytida ma'lum bo'lgani uchun xatoni erta topish imkonini yo'qotadi - `helm template`/`kustomize build` natijasini CI'da albatta validate qiling. Shablonga maxfiy qiymatni default sifatida yozib qo'ymang: u Git'da va render qilingan ConfigMap'da ochiq qoladi.

## 29.19 Boshqaruvchi halqa (Controller (Kubernetes))

**Tavsif:** Kubernetes'ning yuragi - reconciliation loop: controller kerakli holatni (spec) va joriy holatni (status) doimiy kuzatib, ularni bir-biriga yaqinlashtiradi. Controller pattern shu g'oyani sizning o'z resurslaringizga ham kengaytiradi: watch/informer orqali o'zgarishlarni eshitib, har bir hodisada "hozirgi holatni kerakli holatga keltir" deb butun holatni qayta hisoblash (level-triggered, edge-triggered emas). Bu yondashuv idempotent, o'z-o'zini tuzatuvchi va qayta urinishga (retry) tabiiy chidamli tizim beradi.

**Spring'da qayerda uchraydi:** Spring Framework'da controller halqasi uchun maxsus abstraksiya yo'q (`@Controller` butunlay boshqa narsa - web MVC), shuning uchun Kubernetes client kutubxonalari ishlatiladi: Fabric8 `io.fabric8.kubernetes.client.KubernetesClient` va uning `SharedIndexInformer`/`ResourceEventHandler` mexanizmi, yoki rasmiy `io.kubernetes:client-java` va uning `extended` moduli (`SharedInformerFactory`, `ControllerBuilder`, `io.kubernetes.client.extended.controller.reconciler.Reconciler`, `Result`). Spring Boot ilovasida bu `ApplicationRunner`/`SmartLifecycle` bean sifatida ishga tushiriladi, informer ishlashi `HealthIndicator` bilan readiness'ga bog'lanadi, xatolar `@Retryable` yoki exponential backoff bilan qayta urinadi. Bir vaqtda bitta instans ishlashi uchun Kubernetes lease asosidagi leader election (`LeaderElector` fabric8'da) yoki Spring Integration `LockRegistryLeaderInitiator` ishlatiladi; Spring Cloud Kubernetes ham watch'ga asoslangan discovery va config reload'ni xuddi shu pattern bilan amalga oshiradi.

**Qo'llanish keyslari:**
- Namespace'da ma'lum annotation'ga ega har bir ConfigMap paydo bo'lganda ichki cache'ni yoki routing jadvalini yangilash.
- Pod label'lari o'zgarganda tashqi load balancer yoki DNS yozuvlarini sinxronlash.
- Secret rotatsiyasini kuzatib, ilova connection pool'ini yangi credential bilan qayta ochish.
- Istalgan nosozlikda (pod o'chirilsa, ConfigMap qo'lda o'zgartirilsa) tizimni kerakli holatga o'zi qaytarish.
- Platforma jamoasi uchun "har bir yangi namespace'ga standart NetworkPolicy va ResourceQuota qo'y" avtomatizatsiyasi.

**Ehtiyot bo'ling:** Reconcile funksiyasi albatta idempotent bo'lishi shart va hodisalar ketma-ketligiga tayanmasligi kerak - watch uzilib, informer resync qilganda bir xil hodisa bir necha marta yoki umuman kelmasligi normal holat. API serverni `list` bilan bombardimon qilish (informer cache'ni ishlatmaslik) yoki xatoda backoff'siz qayta urinish katta klasterda butun control plane'ni cho'ktirishi mumkin.

## 29.20 Operator (Operator)

**Tavsif:** Operator - Controller pattern'ning Custom Resource Definition (CRD) bilan kuchaytirilgani: domenga xos operatsion bilim (backup, failover, versiya yangilash, shard qo'shish) kod ichiga yoziladi va `kubectl` bilan boshqariladigan yangi resurs turi sifatida e'lon qilinadi. Foydalanuvchi `kind: PostgresCluster` kabi deklarativ obyekt yozadi, Operator esa uni real holatga aylantiradi va doimiy kuzatadi. Shunday qilib stateful va murakkab tizimlarni ham Kubernetes'ning deklarativ modeliga kiritish mumkin bo'ladi.

**Spring'da qayerda uchraydi:** Java'da de-fakto standart - Java Operator SDK (`io.javaoperatorsdk:operator-framework`), u Fabric8 client ustida `Reconciler<P extends HasMetadata>` interfeysi, `reconcile(...)`/`cleanup(...)` metodlari va `UpdateControl`/`DeleteControl` natijalari bilan ishlaydi; CRD POJO'lari Fabric8'ning `CustomResource` sinfi va `@Group`, `@Version` annotatsiyalari bilan yoziladi. Spring Boot integratsiyasi uchun Java Operator SDK'ning Spring Boot starter'i mavjud: `Reconciler` bean'lari avtomatik ro'yxatga olinadi, `Operator` lifecycle Spring context'ga bog'lanadi, Actuator health va Micrometer metrikalari odatdagidek ishlaydi. Ichki holatni Spring bean'lari (`RestClient`, `JdbcClient`, `TaskScheduler`) bilan boshqarish qulay; finalizer'lar `cleanup` metodida, status yangilash esa `UpdateControl.patchStatus(...)` orqali bajariladi.

```java
@Component
public class CacheReconciler implements Reconciler<CacheCluster> {
    @Override
    public UpdateControl<CacheCluster> reconcile(CacheCluster res, Context<CacheCluster> ctx) {
        ensureStatefulSet(res);                 // idempotent: create-or-patch
        res.getStatus().setReadyReplicas(readyReplicas(res));
        return UpdateControl.patchStatus(res).rescheduleAfter(Duration.ofMinutes(1));
    }
}
```

**Qo'llanish keyslari:**
- Ichki Kafka yoki PostgreSQL klasterini CRD orqali deklarativ yaratish, backup va failover'ni avtomatlashtirish.
- Platforma jamoasi uchun `kind: Microservice` abstraksiyasi - bitta resurs Deployment, Service, Ingress va HPA'ni generatsiya qiladi.
- Tenant onboarding: `kind: Tenant` yaratilganda namespace, DB schema, quota va credential'larni avtomatik tayyorlash.
- ML model deploy'ini `kind: ModelServing` resursi orqali versiyalab, canary rollout bilan boshqarish.
- Sertifikat va credential rotatsiyasini domen qoidalariga mos ravishda o'zi bajaradigan operator.

**Ehtiyot bo'ling:** Operator yozish - jiddiy qaror: u klaster darajasida keng RBAC huquqlariga ega bo'ladi va undagi xato butun platformani buzishi mumkin, shuning uchun huquqlarni minimallashtiring va reconcile'ni og'ir yon ta'sirlardan (idempotent bo'lmagan tashqi chaqiruvlardan) toza tuting. Oddiy deploy ishini Helm yoki Kustomize hal qiladigan joyda operator qurish keraksiz murakkablik; mavjud yetuk operator (Strimzi, CloudNativePG) bo'lsa, o'zingiznikini yozmang.

## 29.21 Pod - deploy birligi sifatida (Pod as Deployment Unit)

**Tavsif:** Kubernetes'da eng kichik joylashtirish (scheduling) birligi container emas, balki pod: bir necha container umumiy network namespace, IP, volume va umr davrini bo'lishadi. Bu asosiy container bilan birga yordamchi container'larni (sidecar, init, adapter, ambassador) atomik birlikda deploy qilish imkonini beradi. Pod atomikdir - u butunligicha bir node'ga joylashadi, butunligicha ko'chadi va butunligicha o'ladi, shuning uchun unga faqat chindan birga yashashi kerak bo'lgan jarayonlarni qo'shish lozim.

**Spring'da qayerda uchraydi:** Bu toza infratuzilma darajasidagi pattern - Spring'da uni ifodalovchi sinf yo'q, lekin Spring Boot ilovasi pod shartlariga moslashadi. Service mesh (Istio/Linkerd) sidecar proxy'si mTLS, retry va circuit breaking'ni o'z ustiga olganda, ilovadan Resilience4j'ning bir qismini olib tashlash mumkin; aksincha, `localhost`ga murojaat qiladigan ambassador container (masalan Cloud SQL Auth Proxy) `spring.datasource.url=jdbc:postgresql://localhost:5432/...` bilan ishlatiladi. Init container migratsiyani (Flyway/Liquibase'ni `flyway migrate` yoki alohida `--spring.flyway.enabled` bilan ishga tushirgan holda) asosiy container'dan oldin bajaradi - bu bir necha replica'da migratsiya poygasini oldini oladi. Pod ichidagi `emptyDir` volume Spring Boot'ning `logging.file.name` yoki `spring.config.additional-location` yo'llari uchun umumiy maydon bo'ladi; `server.shutdown=graceful` va `preStop` hook esa sidecar bilan birga to'g'ri tartibda to'xtashni ta'minlaydi. Kubernetes 1.29+ dagi native sidecar (initContainer + `restartPolicy: Always`) proxy ilovadan oldin tayyor bo'lishini kafolatlaydi.

**Qo'llanish keyslari:**
- Spring Boot ilovasi yonida Istio Envoy sidecar'i bilan mTLS va trafik boshqaruvini kodga tegmasdan olish.
- Init container'da Flyway migratsiyasini bajarib, keyin N replica ilovani xavfsiz ishga tushirish.
- Fluent Bit sidecar'i bilan `emptyDir`ga yozilgan log fayllarini markazlashgan tizimga yuborish.
- Cloud SQL yoki Vault Agent ambassador container'i orqali credential va ulanishni `localhost`da taqdim etish.
- Legacy ilovaga adapter sidecar qo'shib, uning metrikalarini Prometheus formatiga o'girish.

**Ehtiyot bo'ling:** Pod'ga mustaqil skale qilinishi kerak bo'lgan komponentlarni qo'shish katta xato - ularni alohida Deployment qiling, chunki pod ichidagi container'lar faqat birgalikda skale bo'ladi. Sidecar'lar pod'ning resurs so'rovini va ishga tushish vaqtini sezilarli oshiradi; sidecar asosiy container'dan keyin tayyor bo'lsa, Spring Boot ilovasining dastlabki so'rovlari muvaffaqiyatsiz bo'ladi, shuning uchun native sidecar yoki readiness ketma-ketligini aniq sozlang.

## 29.22 Resurs so'rovlari va limitlari (Resource Requests & Limits)

**Tavsif:** Scheduler pod'ni qayerga joylashtirishni va kubelet uni qanchalik cheklashni faqat e'lon qilingan `requests` va `limits` asosida biladi. `requests` - kafolatlangan minimum va joylashtirish asosi, `limits` - qattiq yuqori chegara: CPU'da throttling, memory'da OOMKill. Ular pod'ning QoS klassini belgilaydi (Guaranteed, Burstable, BestEffort), bu esa node resurs tanqisligida kimni birinchi o'ldirishni aniqlaydi. To'g'ri sozlangan limitlar "shovqinli qo'shni" muammosini yo'qotadi va narxni nazorat qilish imkonini beradi.

**Spring'da qayerda uchraydi:** JVM container limitlarini o'zi hisobga oladi: `-XX:+UseContainerSupport` (JDK 10+ dan beri yoqilgan), `-XX:MaxRAMPercentage` bilan heap cgroup memory limitidan foiz sifatida olinadi, `Runtime.availableProcessors()` esa CPU quota/shares'ga qarab qaytaradi - bu ForkJoinPool, Netty event loop, Tomcat va Reactor Netty thread pool o'lchamlariga bevosita ta'sir qiladi. Paketo buildpack bilan qurilgan Spring Boot image'da Java Memory Calculator `JAVA_TOOL_OPTIONS` ichiga `-Xmx`, `-XX:MaxMetaspaceSize`, `-XX:ReservedCodeCacheSize` va thread stack hisobini avtomatik qo'yadi, shuning uchun memory limitini o'zgartirsangiz hisob ham o'zgaradi. `server.tomcat.threads.max`, HikariCP `spring.datasource.hikari.maximum-pool-size` va Spring Boot 3.2+ dagi `spring.threads.virtual.enabled=true` CPU limiti bilan muvofiqlashtirilishi kerak; haqiqiy iste'molni Micrometer JVM metrikalari (`jvm.memory.used`, `jvm.threads.live`) va `/actuator/metrics` bilan kuzatiladi.

**Qo'llanish keyslari:**
- Prod'da to'lov servisiga `requests == limits` berib Guaranteed QoS va barqaror latency olish.
- `-XX:MaxRAMPercentage=70` bilan heap'dan tashqari (metaspace, thread stack, native buffer) joy qoldirib OOMKill'dan qutulish.
- Dev namespace'ida past `requests` bilan node'larni zich to'ldirib, infra xarajatini kamaytirish.
- VPA recommender yoki Prometheus tarixiga qarab haddan oshirilgan `requests`ni qisqartirib, klaster sig'imini bo'shatish.
- `LimitRange` va `ResourceQuota` bilan jamoalar o'rtasida klaster resurslarini adolatli taqsimlash.

**Ehtiyot bo'ling:** `limits`ni belgilamaslik ham, `requests`ni real iste'moldan ancha yuqori qo'yish ham zarar: birinchisida bitta ilova node'ni yiqitadi, ikkinchisida klasterning yarmi bo'sh turgan holda to'la hisoblanadi. CPU limitini juda past qo'yish Spring Boot ilovasini startup paytida throttling'ga uchratib, liveness probe'ning noto'g'ri restart tsikliga olib keladi; memory limitida esa heap'ni limitga teng qilib qo'ymang - JVM'ning non-heap qismi ham o'sha limit ichida hisoblanadi.

## 29.23 Amalda qo'llash

- [ ] Har bir pod uchun `requests` va `limits` qiymatlarini o'lchangan p95 CPU va maksimal RSS ga asoslab qayta hisoblang.
- [ ] Readiness, liveness va startup probe'lari uchta alohida maqsadga xizmat qilayotganini tasdiqlang.
- [ ] Graceful shutdown va `terminationGracePeriodSeconds` qiymatlari ilovaning eng uzun so'rovidan katta ekanini tekshiring.
- [ ] ConfigMap va Secret dan keladigan qiymatlarni ro'yxatga olib, o'zgarganda restart kerakligini yozib qo'ying.
- [ ] HPA sozlamalarini tekshiring: metrika to'g'ri tanlanganmi, minimal nusxa soni nol emasmi.
- [ ] Pod disruption budget borligini va reliz paytida xizmat uzilmasligini tasdiqlang.
- [ ] Init container va sidecar larni sanab chiqib, har birining nega kerakligini yozib qo'ying.
- [ ] Stateless talabini tekshirish uchun bitta podni ataylab o'chirib ko'ring va natijani hujjatlashtiring.

---

[&larr; 28. Taqsimlangan ma'lumot, replikatsiya va konsistentlik patternlari](28-taqsimlangan-malumot-replikatsiya-va.md) · [Mundarija](README.md) · [30. Spring AI va LLM integratsiya patternlari &rarr;](30-spring-ai-va-llm-integratsiya-patternlari.md)
