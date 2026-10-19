<!-- doc: patterns | chapter: 29 | part:  -->

[Barcha hujjatlar](../../README.md) / [Dizayn patternlar](README.md)

> Holat: tekshirilgan (2026-10-19). Manbalar bob oxirida.

# 29. Kubernetes va cloud-native patternlar (Kubernetes & Cloud-Native Patterns)

<details>
<summary>Bu bobdagi 27 bo'lim</summary>

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
- [29.23 Pod uzilish byudjeti (Pod Disruption Budget)](#2923-pod-uzilish-byudjeti-pod-disruption-budget)
- [29.24 Pod prioriteti va preemption (Pod Priority & Preemption)](#2924-pod-prioriteti-va-preemption-pod-priority--preemption)
- [29.25 Klasterni bo'lishish: multitenancy va federatsiya (Multitenancy and Federation)](#2925-klasterni-bolishish-multitenancy-va-federatsiya-multitenancy-and-federation)
- [29.26 Scheduler siyosati va joylashtirishga aralashuv (Scheduler Policy and Placement Intervention)](#2926-scheduler-siyosati-va-joylashtirishga-aralashuv-scheduler-policy-and-placement-intervention)
- [29.27 Amalda qo'llash](#2927-amalda-qollash)

</details>



Kubernetes va cloud-native patternlar - bu ilovaning ichki sinflar darajasidagi dizayni emas, balki uning konteyner orkestratori bilan qanday "muloqot qilishi" haqidagi patternlar to'plami. Ular Bilgin Ibryam va Roland Huss'ning "Kubernetes Patterns" ishida tizimlashtirilgan va aslida deklarativ infratuzilma bilan ishlashning umumiy tilini beradi: ilova o'z talablarini oldindan e'lon qiladi, platforma esa joylashtirish, qayta ishga tushirish va masshtablashni o'z zimmasiga oladi. Arxitektor uchun bu muhim, chunki Spring Boot ilovasining kodi mukammal bo'lsa ham, noto'g'ri e'lon qilingan resurs limitlari, probe'lar yoki graceful shutdown sozlamalari butun relizni beqaror qiladi. Shuning uchun bu bo'limdagi patternlarni "YAML detallari" deb emas, ilova arxitekturasining tashqi kontrakti deb qarash kerak.

Bitta shart hammasidan oldin turadi: konteyner patternlari ilovaning ichki sifatini almashtirmaydi. Image ichiga tartibsiz kod solinsa, u yo'qolmaydi, faqat masshtabda tarqaladi va endi bir sinf ichida emas, o'nlab pod bo'ylab qidirishga to'g'ri keladi. Shuning uchun toza kod, domen chegaralari va mikroservisga ajratish qoidalari bu bobdagi patternlardan OLDIN qo'llaniladi: orkestrator noto'g'ri qo'yilgan modul chegarasini tuzatmaydi, uni ko'paytiradi.

## 29.1 Oldindan aytib beriladigan talablar (Predictable Demands)

**Tavsif:** Har bir konteyner o'zi talab qiladigan CPU, xotira, disk va platforma imkoniyatlarini aniq e'lon qilishi kerak, aks holda scheduler to'g'ri node tanlay olmaydi va cluster beqaror bo'ladi. Pattern `resources.requests` (kafolatlangan minimum, scheduling uchun asos) va `resources.limits` (yuqori chegara, uni oshsa CPU throttling yoki OOMKill) orqali amalga oshiriladi. Shuningdek ilova o'zining runtime bog'liqliklarini - ConfigMap, Secret, PersistentVolumeClaim, maxsus node imkoniyatlarini - deklarativ ravishda ko'rsatadi. Natijada platforma ilovaning "ishtahasi"ni biladi va QoS klassi (Guaranteed, Burstable, BestEffort) aniq bo'ladi.

**Spring'da qayerda uchraydi:** Bu birinchi navbatda infratuzilma darajasidagi pattern, lekin JVM uchun hayotiy muhim: Java 17-25 konteynerni taniydi (`UseContainerSupport` sukut bo'yicha yoqilgan) va `MaxRAMPercentage` orqali heap'ni konteyner limitidan foizda hisoblaydi - shuning uchun `limits.memory` ni e'lon qilmaslik JVM'ga butun node xotirasini ko'rsatadi. Spring Boot 3.x/4.x'da `bootBuildImage` (Gradle) yoki `spring-boot-maven-plugin`'ning `build-image` goal'i Paketo buildpack'lar bilan image yasaydi, Paketo'ning Memory Calculator esa heap, metaspace, thread stack va direct memory'ni konteyner limiti va `BPL_JVM_THREAD_COUNT` asosida avtomatik taqsimlaydi. Haqiqiy talabni o'lchash uchun `spring-boot-starter-actuator` va Micrometer'ning `jvm.memory.used`, `jvm.threads.live`, `process.cpu.usage` metrikalaridan foydalaniladi; CDS/AOT (`spring-boot-starter-parent` AOT plugin'i) yoki GraalVM native image esa talabni sezilarli kamaytiradi.

**Qo'llanish keyslari:**
- Spring Boot REST servisi uchun `requests.memory` ni haqiqiy RSS asosida o'lchab, `limits.memory` ni OOMKill'siz ishlaydigan darajada belgilash.
- Batch yoki reporting ilovasiga katta `limits.cpu` berib, scheduler'ni `requests` bilan ortiqcha bloklamaslik.
- Latency sezgir to'lov servisini Guaranteed QoS'ga chiqarish uchun `requests` va `limits` ni teng qilib qo'yish.
- Kafka consumer ilovasida thread pool o'lchamini konteynerga berilgan CPU soniga moslab, `BPL_JVM_THREAD_COUNT` ni to'g'rilash.
- Native image'ga o'tgan servis uchun xotira `requests` ni bir necha barobar kamaytirib, node zichligini oshirish.

**Runtime bog'liqlikning ikki xil narxi.** E'lon qilingan bog'liqliklar bir xil og'irlikda emas va ularning yo'qligi ikki xil nosozlik beradi. Node bera olmaydigan volume turi yoki mavjud bo'lmagan node imkoniyati pod ni UMUMAN joylashtirmaydi: hech bir node tanlanmaydi va pod `Pending` da qoladi. Yo'q ConfigMap yoki Secret esa boshqacha ishlaydi: scheduler pod ni muvaffaqiyatli joylashtiradi, kubelet konteynerni ishga tushira olmaydi. Diagnostikada farq shu yerda: birinchi holatda scheduler nima deganiga, ikkinchisida pod hodisalari va konteyner holatiga qaraladi.

Yana bir e'lon qilinadigan talab - tarmoq porti. `hostPort` bilan so'ralgan port node da band qilinadi va shu paytdan boshlab bitta node ga shu pod ning faqat bitta nusxasi sig'adi, ya'ni replica soni node sonidan oshmaydi. Legacy ilova `hostPort` ni talab qilsa, masshtab chegarasi manifest yozilayotgan paytda hisoblanadi, aks holda u keyinchalik HPA ning tushunarsiz maksimumi bo'lib chiqadi.

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

**`postStart` hook ning uch xossasi.** Faqat protsess signallari bilan hayot siklini boshqarish yetarli emas, shuning uchun Kubernetes `postStart` va `preStop` hook'larini beradi. `postStart` ni to'g'ri ishlatish uchun uchta xossasini birga bilish kerak va ular bir qarashda bir-biriga zid ko'rinadi:

- **Asinxron.** `postStart` konteyner yaratilgandan keyin asosiy konteyner protsessi bilan **parallel** bajariladi, ya'ni asosiy protsess tugashini kutmaydi va asosiy protsess ham uni kutmaydi.
- **Bloklovchi.** Shunga qaramay chaqiruvning o'zi bloklovchi: `postStart` handler tugamaguncha konteyner holati `Waiting` da qoladi, bu esa Pod ni `Pending` holatida ushlab turadi. Shu xossadan ataylab foydalanish mumkin - asosiy protsessga initsializatsiya uchun vaqt berib, konteynerning "ishga tushgan" holatini kechiktirish.
- **Nol bo'lmagan chiqish kodi asosiy protsessni o'ldiradi.** `postStart` hook xatoni nol bo'lmagan chiqish kodi bilan qaytarsa, Kubernetes asosiy konteyner protsessini o'ldiradi. Shuning uchun uni Pod oldindan belgilangan shartlarni bajarmasa konteynerni ishga tushirmaslik uchun darvoza sifatida ishlatish mumkin.
- **Kamida bir marta bajariladi.** Hook ning semantikasi at-least-once: u bir martadan ko'p chaqirilishi mumkin, demak dublikat bajarilishni ilovaning o'zi ko'tarishi kerak va handler idempotent yoziladi. Muvaffaqiyatsiz `httpGet` handler uchun esa platforma qayta urinmaydi, ya'ni "urinib ko'radi, keyin tuzatadi" deb hisoblash xato.

Handler turlari Health Probe (29.3 dagi probe'lar bilan bir xil mexanizm): `exec` - konteyner ichida buyruq, `httpGet` - Pod konteyneri ochgan portga HTTP GET. Kitobning ogohlantirishi aniq: `postStart` da kritik mantiq bajarmang, chunki uning bajarilishiga kafolat yo'q. Spring da bu xossalar odatda kerak ham emas: tartibni init container bilan, kutishni `ApplicationRunner`/`SmartLifecycle` bilan, tayyorlikni esa `/actuator/health/readiness` bilan ifodalash aniqroq va kuzatiladigan bo'ladi.

**`preStop` nimani kafolatlamaydi.** `preStop` konteyner o'chirilishidan oldin bajariladi va chaqiruvi bloklovchi, lekin undan konteyner umrini boshqarish vositasi sifatida foydalanish xato: handler ni ushlab turish ham, undan xato qaytarish ham konteynerning o'chirilishini TO'XTATMAYDI. U `SIGTERM` ga qulay alternativa, boshqa hech narsa emas - signalni o'zi ushlay olmaydigan ilova uchun to'xtatish buyrug'ini chaqirish yo'li. Shu sababli Spring Boot ilovasida graceful shutdown mantiqi `preStop` ga emas, `SIGTERM` da yopiladigan `ApplicationContext` ga biriktiriladi; `preStop` esa faqat Endpoint propagatsiyasini kutish uchun qoladi.

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

**Node ning haqiqiy sig'imi - Allocatable, node hajmi emas.** Scheduler pod ni joylashtirishdan oldin pod `requests` yig'indisini node ning umumiy hajmiga emas, **Allocatable** qiymatiga solishtiradi. Faqat Kubernetes ga ajratilgan node uchun formula shu:

```text
Allocatable [ilova pod'lari uchun sig'im] =
    Node Capacity   [node dagi mavjud sig'im]
  - Kube-Reserved   [Kubernetes demonlari: kubelet, container runtime]
  - System-Reserved [OS demonlari: sshd, udev]
```

Buning ikki amaliy natijasi bor. Birinchisi: OS va Kubernetes demonlari uchun zaxira ajratilmasa, pod'lar node ning to'liq hajmigacha joylashtirilishi mumkin va shu paytdan boshlab pod'lar bilan tizim demonlari resurs uchun kurasha boshlaydi - node da resource starvation paydo bo'ladi. Ikkinchisi: JVM pod hajmini hisoblash ham shu qiymatga tayanadi, chunki `-XX:MaxRAMPercentage` konteyner limitidan foiz oladi, limitlar yig'indisi esa node Allocatable iga sig'ishi kerak; "node 16 GB, demak 16 GB bo'lishaman" hisobi `Pending` pod bilan tugaydi. Uchinchi holat: node da Kubernetes boshqarmaydigan konteynerlar ishlayotgan bo'lsa, ularning iste'moli node sig'imi hisobida aks etmaydi. Kitob bu cheklovning chetlab o'tish yo'lini beradi - hech narsa qilmaydigan, lekin hisobga olinmagan konteynerlarning CPU va xotira iste'moliga teng `requests` ga ega placeholder pod ishga tushirish; u faqat o'sha iste'molni egallab turish va scheduler ga node ning to'g'riroq resurs modelini berish uchun yaratiladi.

**Label va annotation ikki xil maqsad uchun.** Joylashtirish va selector mexanizmlarining hammasi label ustida ishlaydi, shuning uchun har pod ta'rifi scheduling uchun ishlatiladigan noyob label kombinatsiyasiga ega bo'lishi kerak: selector shu kombinatsiya bo'yicha pod to'plamini aniq ajratadi. Label ni oldindan ko'p yozish esa qarz: keyinchalik yangi label qo'shish oson, lekin OLIB TASHLASH xavfli, chunki label ni kim ishlatayotganini - qaysi Service, qaysi selector, qaysi so'rov - ishonchli aniqlashning yo'li yo'q. Annotation boshqa ish uchun: u qidirilmaydigan mashina metadatasi, masalan build raqami, git branch nomi, image hash yoki mas'ul jamoa. Ajratish qoidasi oddiy: selector yoki so'rov tegishi mumkin bo'lgan narsa label bo'ladi, faqat o'qish uchun yozilgan narsa annotation bo'lib qoladi.

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

**Job turini ish bo'lagining narxiga qarab tanlash.** `completions` va `parallelism` ni sozlashdan oldin ish bo'laklari qanday ekanini aytib olish kerak, chunki uch xil shakl bor va ularning narxi boshqa.

- **Fixed completion count.** Bo'lak soni oldindan ma'lum va bitta bo'lak alohida pod ga arziydigan darajada katta bo'lsa, `completions` aniq son bilan beriladi va har bo'lak o'z pod ida bajariladi.
- **Work queue.** Bo'laklar mayda bo'lsa, har biriga pod ochish samarasiz: `completions` berilmaydi, pod lar navbat orqali o'zaro kelishadi va navbat bo'shligini birinchi topgan pod butun Job ni tugatgan hisoblanadi.
- **Cheksiz oqim.** Ish hech qachon tugamasa, bu umuman Job emas: doimiy ishlaydigan iste'molchi Deployment yoki ReplicaSet bilan yoziladi.

Granularlik ham ongli qaror: har bo'lakka alohida Job ochish faqat o'sha bo'lak mustaqil kuzatilishi va alohida skale bo'lishi kerak bo'lganda o'zini oqlaydi, aks holda bitta Job ochilib, bo'lak boshqaruvi ilova ichidagi batch framework ga (Spring Batch partitioning) qoldiriladi.

Oxirgi tafsilot `parallelism` haqida: uni baland qo'yish parallellikni KAFOLATLAMAYDI. Amalda bir vaqtda ishlaydigan pod soni platforma throttling i, namespace quota si va qolgan `completions` soni bilan cheklanadi, shuning uchun "20 qo'ydim, demak 20 ishlaydi" hisobi ko'pincha chiqmaydi. Teskari chegara esa foydali: `parallelism: 0` Job ni o'chirmasdan pauza qiladi.

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

**DaemonSet scheduler ga muhtoj emas.** DaemonSet pod i boshqa pod lardan boshqa yo'l bilan tug'iladi: u darhol `nodeName` to'ldirilgan holda yaratiladi, ya'ni scheduler qarorini kutmaydi. Uchta amaliy natijasi bor. Birinchisi: bunday pod scheduler ning o'zi ishga tushishidan oldin ham ishlay oladi, shu sababli mexanizm Kubernetes ning o'z komponentlarini yuritishga yaraydi. Ikkinchisi: u node ning `unschedulable` bayrog'ini HISOBGA OLMAYDI, demak `kubectl cordon` qilingan node da DaemonSet pod i qolaveradi - "node yopilgan, lekin agent hali ishlayapti" ko'rinishi nosozlik emas, kutilgan xulq. Uchinchisi: joylashuvni cheklash kerak bo'lsa u scheduler qoidalari bilan emas, DaemonSet ning o'z node selector i bilan beriladi.

**Agentga yetishning to'rt yo'li.** Iste'molchi node dagi agentga qanday murojaat qilishi alohida qaror va variantlarning narxi teng emas.

| Yo'l | Nima beradi | Narxi |
|---|---|---|
| oddiy Service | trafik tasodifiy node dagi agentga balanslanadi | qaysi node ga tushgani oldindan ma'lum emas |
| headless Service DNS | hamma agent pod ining IP si A yozuvi bilan qaytadi | tanlash mijoz ishi, balanslash yo'q |
| `hostPort` plus node IP | aynan shu node dagi agentga yetiladi | node da port band bo'ladi, joylashuv cheklanadi |
| push | agent o'zi yuboradi, iste'molchi umuman yetmaydi | yo'nalishni agent belgilaydi, so'rov mumkin emas |

Node-local collector ga yozadigan Spring ilovasida amalda uchinchi yo'l ishlatiladi: Downward API `status.hostIP` ni env ga beradi va ilova shu manzildagi portga yuboradi.

**Rad etilgan alternativa: static pod.** Har node da bitta protsess yuritishning ikkinchi yo'li bor - kubelet lokal katalogdan o'qiydigan static pod. U ishlaydi, lekin platformadan tashqarida qoladi: API server uni resurs sifatida ko'rmaydi, demak hech bir controller uni boshqarmaydi, health check va qayta joylashtirish yo'q, kubelet esa faqat crash dan keyin qayta ishga tushiradi. DaemonSet bir xil natijani beradi, lekin API server, RBAC, reliz va kuzatuv mexanizmlariga ulangan holda - shuning uchun static pod faqat kubelet ning o'zini ko'taradigan bootstrap komponentlari uchun qoladi.

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

**Qamrovni tanlash: butun servis yoki uning bir qismi.** Ikki ko'rinish orasidagi tanlov texnologiyadan emas, singleton QAMROVIdan boshlanadi. Butun servis bir vaqtda bitta nusxada ishlashi kerak bo'lsa, ilovadan tashqaridagi yo'l to'g'ri: `replicas: 1` li StatefulSet izchillikni mavjudlikdan ustun qo'yadi va "ko'pi bilan bitta" kafolatini beradi, narxi esa mavjudlikning pasayishi va qo'shimcha murakkablik. Servisning faqat BIR QISMI yakka bo'lishi kerak bo'lsa - HTTP endpoint lar erkin skale bo'lsin, lekin polling yoki rejalashtiruvchi komponent bitta ishlasin - ilova ichidagi lock to'g'ri tanlov, chunki tashqi lock butun servisni skale bo'lmaydigan qilib qo'yadi. Shu sababli polling komponentini "yakka bo'lishi kerak" degan sabab bilan alohida deploy ga chiqarish ko'pincha keraksiz: lock qamrovini kichraytirish arzonroq va kamroq harakatlanuvchi qismi bor.

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

**Rad etilgan ikki chetlab o'tish yo'li.** Taqsimlangan stateful ilovani StatefulSet siz ko'tarishning ikki ko'rinadigan yo'li bor va ikkisi ham ishlamaydi. Birinchisi: hamma instans bitta umumiy storage ga ulanadi va ilova o'zi ichidan har instansga alohida papka ajratadi. Bu bitta nosozlik nuqtasi yaratadi - storage yoki uni ushlab turgan komponent yiqilsa hamma instans birga to'xtaydi - va skale paytida ikki instans bir papkaga yozib ma'lumotni buzishi mumkin. Ikkinchisi: har instans uchun qo'lda alohida ReplicaSet, PVC va Service yozish. U texnik jihatdan ishlaydi, lekin instans soni o'zgarganda hammasini qo'lda qayta yozishga to'g'ri keladi va ilovani bitta abstraksiya bilan boshqarish imkoniyati yo'qoladi. StatefulSet aynan shu ikki muammoni yopadi.

**Manifest yozishda yiqiladigan shartlar.** `serviceName` bilan boshqaruvchi (governing) Service ga havola MAJBURIY va o'sha Service StatefulSet dan OLDIN yaratilishi kerak: barqaror DNS nomlari shu Service ostida tug'iladi. `volumeClaimTemplates` esa majburiy emas - diski yo'q, lekin barqaror identifikatsiya va tartibli ishga tushish kerak bo'lgan ilova uchun StatefulSet PVC siz ham ma'noli. Klaster a'zolarini dinamik topish kerak bo'lsa headless Service ning SRV yozuvi so'raladi: u boshqaruvchi Service ostidagi hamma ishlayotgan pod ni qaytaradi, A yozuvi esa faqat manzillar ro'yxatini beradi.

**Kvorumni saqlab yangilash va tartibni tezlashtirish.** StatefulSet ning o'z yangilash strategiyasi bor va u Deployment dagidan boshqa. `updateStrategy.rollingUpdate.partition` indeksi partition dan kichik pod larni yangilanmaydigan qiladi: ular o'chirilsa ham eski versiyada qayta yaratiladi, shuning uchun kvorumni ushlab turib bosqichma-bosqich yangilash yoki sinov uchun bitta a'zoni eski versiyada qoldirish mumkin bo'ladi. Teskari holat ham bor: tartib umuman muhim bo'lmasa, `podManagementPolicy: Parallel` pod larni ketma-ket emas, birga ko'taradi va katta klasterda operatsiyani sezilarli tezlashtiradi.

**Ehtiyot bo'ling:** Ishlab chiqarishda ma'lumotlar bazasini Kubernetes'da o'zi qo'lda boshqarish (operator'siz, backup va failover strategiyasisiz) jiddiy xavf - ko'p holatda managed DB yoki yetuk operator afzal. StatefulSet'ni oddiy stateless Spring servisi uchun "ehtiyot shart" ishlatish esa deploy'ni sekinlashtiradi va masshtablashni qiyinlashtiradi, foyda bermaydi. "Ko'pi bilan bitta" kafolatini esa ko'pincha platforma emas, ODAM buzadi: yetib bo'lmaydigan node obyektini API server dan o'chirish yoki `kubectl delete pod --grace-period=0 --force` qilish eski pod hali tirik bo'lgan holatda yangi nusxaga yo'l ochadi - bu ikki amal faqat node ning haqiqatan o'lgani tasdiqlangandan keyin bajariladi.

## 29.11 Servis topish (Service Discovery (Kubernetes view))

**Tavsif:** Pod'lar vaqtinchalik va ularning IP manzillari doimiy o'zgaradi, shuning uchun mijoz manzilni qattiq yozib qo'yolmaydi. Kubernetes bu muammoni `Service` abstraksiyasi bilan hal qiladi: ClusterIP va barqaror DNS nomi (`<service>.<namespace>.svc.cluster.local`) ortida Endpoint/EndpointSlice ro'yxati dinamik yangilanadi va kube-proxy trafikni sog'lom pod'larga taqsimlaydi. Tashqi trafik uchun `Ingress` yoki Gateway API, cluster ichidagi peer discovery uchun esa headless Service ishlatiladi. Natijada mijoz uchun discovery oddiy DNS so'roviga aylanadi.

**Spring'da qayerda uchraydi:** Eng oddiy va eng mustahkam yondashuv - hech qanday discovery client'siz, to'g'ridan-to'g'ri Service DNS nomiga murojaat: Spring Framework 6.x'dagi `RestClient` yoki `WebClient` bilan `http://order-service:8080/...`, yoki HTTP interface (`@HttpExchange` va `HttpServiceProxyFactory`). Kerak bo'lganda Spring Cloud Kubernetes'ning `spring-cloud-kubernetes-client-discovery` (yoki fabric8 varianti) moduli Spring Cloud'ning `DiscoveryClient`/`ReactiveDiscoveryClient` abstraksiyasini Kubernetes API ustiga quradi, `spring.cloud.kubernetes.discovery.enabled` bilan boshqariladi va Spring Cloud LoadBalancer (`@LoadBalanced WebClient.Builder`) bilan birga ishlaydi; `spring-cloud-kubernetes-discovery-server` esa discovery'ni alohida HTTP servis sifatida chiqaradi. Spring Cloud Gateway (Spring Boot 3.x) `lb://` sxemasi bilan discovery'ga tayangan routing qiladi, service mesh ishlatilsa esa discovery va retry butunlay sidecar'ga o'tadi.

**Qo'llanish keyslari:**
- Mikroservislar orasidagi chaqiruvlarni Service DNS nomi orqali `RestClient` bilan amalga oshirish.
- Spring Cloud Gateway'da marshrutlarni Kubernetes Service'lariga `lb://` orqali bog'lash.
- Headless Service bilan Hazelcast yoki Kafka Streams peer'larini topish.
- Eureka'dan Kubernetes-nativ discovery'ga ko'chishda `DiscoveryClient` abstraksiyasini saqlab, implementatsiyani almashtirish.
- Blue-Green relizda Service selector'ini o'zgartirib, trafikni yangi versiyaga bir qadamda yo'naltirish.

**Klaster tashqarisidagi bog'liqlikka ichki nom berish.** Selector li Service da Kubernetes mos va tayyor pod'lar ro'yxatini Endpoints resursida o'zi yuritadi. Lekin selector ni **yozmaslik** va Endpoints ni **qo'lda yaratish** mumkin - shunda Service nomi klaster tashqarisidagi IP va portga ishora qiladi. Shu uslubda uchta variant bor:

- **Selector siz Service va qo'lda Endpoints.** Service `type: ClusterIP` bilan, lekin `selector` siz yoziladi; keyin **Service bilan bir xil nomli** Endpoints resursi yaratilib, unda maqsad IP va portlar sanaladi. Iste'molchi uchun hech narsa o'zgarmaydi: u xuddi oddiy Service dek, muhit o'zgaruvchisi yoki DNS orqali ishlatadi, faqat endpoint ro'yxatini odam yuritadi. Endpoints pod IP larini ushlashi mumkin, lekin boshqa Service larning virtual IP larini ushlay olmaydi.
- **`ExternalName`.** `selector` yo'q, `type: ExternalName` va `externalName: my.database.example.com`. Bu variant proxy va IP orqali o'tmaydi: u faqat DNS CNAME yozuvi bilan tashqi endpoint uchun taxallus yaratadi.
- **Keyinchalik ichkariga ko'chirish.** Asosiy foyda shu: Service resursini o'chirmasdan unga selector qo'shish yoki olib tashlash mumkin, resursni o'chirish esa Service IP sining o'zgarishiga olib kelar edi. Natijada iste'molchi birinchi kuni ishora qilgan Service nomi va IP sida qolaveradi, provider ning implementatsiyasi esa on-premise dan Kubernetes ga ko'chadi - **ilova konfiguratsiyasi o'zgarmaydi**.

```yaml
# Klaster tashqarisidagi PostgreSQL ga ichki nom: ilova `jdbc:postgresql://orders-db:5432/orders` yozadi
apiVersion: v1
kind: Service
metadata:
  name: orders-db
spec:
  type: ClusterIP          # selector YO'Q: endpoint ro'yxatini o'zimiz yuritamiz
  ports:
    - protocol: TCP
      port: 5432
---
apiVersion: v1
kind: Endpoints
metadata:
  name: orders-db          # nomi Service nomi bilan AYNAN bir xil bo'lishi shart
subsets:
  - addresses:
      - ip: 10.20.30.40
      - ip: 10.20.30.41
    ports:
      - port: 5432
# Baza keyin klasterga ko'chsa: shu Service ga `selector` qo'shiladi va
# Endpoints o'chiriladi. Service nomi, IP si va ilova konfiguratsiyasi tegilmaydi.
```

**Klaster tashqarisidan topish: NodePort, LoadBalancer va headless.** Yuqoridagi mexanizmlarning hammasi klaster ichidan ko'rinadigan virtual IP ustida ishlaydi, tashqi ilovaga esa pod bergan endpointga yetish kerak. Korpusda tashqi yo'l uchun Ingress va Gateway API qisqa tilga olingan; Service darajasida esa uch variant bor va ularning farqi aniq.

| Tur | Nima qiladi | Narxi |
|---|---|---|
| `ClusterIP` | faqat klaster ichida ko'rinadi (standart) | tashqi mijoz ulanmaydi |
| `NodePort` | hamma node da bitta port ochiladi va trafik backend podlarga taqsimlanadi | firewall qoidalari, sog'lom node ni tanlash mijoz ishi, source NAT |
| `LoadBalancer` | `NodePort` ustiga provayderning load balancer ini qo'shadi | faqat Kubernetes ni qo'llaydigan provayderda, konfiguratsiya nazorati kam |
| `clusterIP: None` (headless) | alohida IP so'ralmaydi, DNS to'g'ridan-to'g'ri podlarni beradi | load balancing yo'q, mijoz o'zi tanlaydi |

`NodePort` ning tafsilotlari qarorga ta'sir qiladi. Portni `nodePort: 30036` bilan o'zingiz tanlashingiz yoki Kubernetes diapazonidan bo'sh portni tanlashiga qo'yishingiz mumkin (Richardson ning misolida diapazon 30000-32767). Har node da port ochilgani uchun tashqi mijozlarga ruxsat berish uchun qo'shimcha firewall qoidalari kerak bo'lishi mumkin. Mijoz klasterdagi istalgan node ga ulanishi mumkin, lekin node ishlamay qolsa boshqa sog'lom node ga o'tish mijoz ilovasining mas'uliyatida qoladi - shu sababli node lar oldiga sog'lom node ni tanlaydigan va failover qiladigan load balancer qo'yish yaxshi fikr; `NodePort` ni ataylab tanlashning asosiy sababi ham shu, o'z load balancer ingizni (masalan AWS ELB ni) to'liq nazorat qilish imkoni. Ulanish node port orqali kelganda trafik tasodifiy tanlangan podga, ehtimol boshqa node dagi podga yo'naltiriladi; bu qo'shimcha hop dan `externalTrafficPolicy: Local` bilan qochish mumkin, lekin shunda Kubernetes boshqa node dagi podlarga ulanishga ruxsat bermaydi, ya'ni har node da pod borligini (DaemonSet bilan) ta'minlash yoki mijoz qaysi node da sog'lom pod borligini bilishi kerak. Yana bir tafsilot manba manzili haqida: `NodePort` da mijoz manzili source NAT qilinadi, ya'ni pod ko'rgan manba IP mijozning emas, paket o'tgan node ning ichki manzili bo'ladi; `externalTrafficPolicy: Local` bu muammoni ham yechadi, chunki trafik faqat shu node dagi podga boradi. `LoadBalancer` da manba manzilini saqlash provayderga bog'liq: ba'zilari saqlaydi, ba'zilari uni load balancer manzili bilan almashtiradi, shuning uchun o'z provayderingizning amalga oshirishini tekshirish kerak.

Ingress ni tanlashning sababi ham shu jadvaldan chiqadi: `LoadBalancer` har Service ga alohida tashqi IP va alohida provayder load balancer ini talab qiladi, demak servis soni o'sganda infratuzilma xarajati ham u bilan birga o'sadi. Ingress bitta tashqi load balancer va bitta IP ni ko'p Service uchun qayta ishlatadi, lekin u L7 da ishlagani uchun faqat hamma servis bir xil protokolda (amalda HTTP da) bo'lganda ma'noli; HTTP bo'lmagan trafik uchun `NodePort` yoki `LoadBalancer` qoladi.

**Service abstraksiyasining to'rt cheklovi.** Service nomi oddiy ko'rinadi, lekin uning ortidagi mexanizm to'rt joyda kutilgandan boshqacha ishlaydi va ularning hammasi diagnostika paytida chiqadi.

- **Virtual IP tarmoq interfeysi emas.** Service ning ClusterIP si hech qanday tarmoq interfeysiga mos kelmaydi: kube-proxy iptables ga faqat e'lon qilingan protokol (TCP yoki UDP) uchun qoida yozadi, ICMP uchun yozmaydi. Natijada Service IP siga `ping` ishlamaydi, lekin shu IP ning portiga TCP ulanish ishlaydi - "ping o'tmadi, demak servis yiqilgan" degan xulosa soxta.
- **Balanslash transport darajasida.** Kubernetes Service L4 da balanslaydi va HTTP cookie bo'yicha sessiya yopishqoqligini QILOLMAYDI; yagona vositasi `sessionAffinity: ClientIP`. Cookie darajasidagi yopishqoqlik kerak bo'lsa, u Ingress controller, gateway yoki service mesh zimmasiga o'tadi.
- **Muhit o'zgaruvchisi orqali topish vaqtga bog'liq.** Service ni muhit o'zgaruvchisi sifatida olish ishlaydi, lekin env ishlab turgan pod ga kiritilmaydi: Service pod dan OLDIN yaratilgan bo'lishi yoki pod qayta ishga tushirilishi kerak. DNS yo'lida bu cheklov yo'q, shuning uchun Spring ilovasida manzil env emas, DNS nomi bilan beriladi.
- **`clusterIP` ni qo'lda tanlash istisno.** `spec.clusterIP` ga aniq qiymat yozish tavsiya qilinmaydi va faqat ikki holatda ma'noli: IP si qattiq yozilgan legacy ilova bor, yoki shu IP ga qadalgan mavjud DNS yozuvini qayta ishlatish kerak.

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

**Qo'lda masshtablashning ikki uslubi.** Avtomatik masshtablash har doim kerak emas: avtoskalerlar yo'q bo'lganda, yoki sekin o'zgaradigan yuklamada optimal konfiguratsiyani bosqichma-bosqich topish uchun odam o'zi buyruq beradi. Qo'lda yondashuvning avtoskalerda yo'q bir afzalligi bor - u faqat reaktiv emas, **oldindan** harakat qilish imkonini beradi: mavsumni va kutilayotgan yuklamani bilsangiz, yuklama oshgandan keyin reaksiya qilishni kutmasdan, replica sonini avvaldan oshirib qo'yasiz. Ikki uslubini ajratish kerak:

- **Imperativ masshtablash.** `kubectl scale deployment random-generator --replicas=4` - ReplicaSet kerakli replica sonini kuzatganligi uchun o'zgarish bitta buyruq bilan bo'ladi: kontroller yetishmaganini yaratadi, ortiqchasini o'chiradi. Shoshilinch holatda eng tez yo'l.
- **Deklarativ masshtablash.** `replicas` qiymati manifest ichida o'zgartiriladi va `kubectl apply -f deployment.yaml` bilan qo'llanadi. `kubectl scale` ning kamchiligi shu: u konfiguratsiyani klaster tashqarisida saqlamaydi, shuning uchun ReplicaSet asl ta'rifidan qayta yaratilsa, replica soni oldingi qiymatiga qaytadi. Aynan shu **configuration drift** ni oldini olish va o'zgarishni orqaga ko'chirish protsessini joriy qilish uchun deklarativ yo'l afzal.

Masshtablash bir nechta pod'ni boshqaradigan resurslarga (ReplicaSet, Deployment, StatefulSet) qo'llanadi. Ikki istisnoni bilish kerak: `volumeClaimTemplates` bo'lgan StatefulSet ni kichraytirish asimmetrik - o'sishda PVC yaratiladi, lekin kichrayishda o'chirilmaydi, saqlanishni yo'qotmaslik uchun; Job esa `replicas` emas, `parallelism` maydoni bilan masshtablanadi (semantik natija bir xil). Asimmetriyaning sababi StatefulSet ning qamrovida: u PersistentVolume ni umuman boshqarmaydi, faqat PVC yaratadi, shuning uchun kichraytirish ma'lumotni ataylab joyida qoldiradi va diskni bo'shatish alohida, qo'lda bajariladigan qadam bo'lib qoladi - PVC ni o'zingiz o'chirasiz.

**Masshtablash zinapoyasi: to'rt bosqich shu tartibda.** Uchta avtoskaler mexanizmini bilish yetarli emas - ularni qaysi tartibda yoqish ham qaror va tartib teskari bo'lsa har bosqich oldingisining xatosini kuchaytiradi.

1. **Ilovaning o'zi.** Avval ilova unga berilgan konteyner resursini to'g'ri ishlatishiga ishonch hosil qilinadi: heap limitdan foizda hisoblanganmi, thread va connection pool o'lchami CPU soniga mosmi, startup qancha davom etadi.
2. **VPA.** Keyin `requests` va `limits` haqiqiy iste'molga keltiriladi; recommender rejimi buni qiymatni o'zgartirmasdan ham ko'rsatadi.
3. **HPA.** Shundan keyin gorizontal masshtablash yoqiladi, chunki HPA to'g'ri qo'yilgan `requests` ustida ishlaydi.
4. **Cluster Autoscaler.** Oxirida klaster darajasi: node qo'shish va olib tashlash.

Birinchi ikki bosqich vertikal: ular uzilish beradi, lekin kamida bir marta bajarilishi shart. Keyingi ikkisi gorizontal va regressiya xavfi kamroq. HPA ning ikki sharti majburiy va aynan shu ikkisi "HPA nega hech narsa qilmaydi" savolining eng ko'p uchraydigan javobi: Deployment da CPU uchun `resources.requests` e'lon qilingan bo'lishi va klasterda metrics server yoqilgan bo'lishi kerak.

VPA ning narxi alohida aytiladi: resursni o'zgartirish uchun pod o'chirilib yangidan yaratiladi, demak qisqa yoki kutilmagan servis uzilishi bo'ladi. Ikkinchi yon ta'siri ham bor - resursi yetmagan konteynerga ko'proq resurs berish pod ni joylashtirilmaydigan qilib qo'yishi va yukni qolgan instanslarga surib yuborishi mumkin. Shu zinapoyani oxirigacha olib borishning natijasi faqat chidamlilik emas: to'g'ri sozlangan tizim og'ir yuklamada sinmaydi, balki pod va node sonini oshirib kuchliroq bo'ladi, va Ibryam va Huss buni antifragillik deb ataydi.

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

**Build va deploy ni bitta tizim bilishining foydasi.** Image ni klaster ichida qurishning asosiy argumenti qulaylik emas, zanjirning yopilishi: build ham, deploy ham bitta tizimga ma'lum bo'lganda bazaviy image dagi zaiflik tuzatilgan paytda unga tayangan hamma ilova image i qayta qurilib, ilovalarning o'zi avtomatik qayta joylashtirilishi mumkin bo'ladi. Tashqi CI bilan bu zanjir qo'lda ulanadi va amalda birinchi bo'g'inda uziladi: image qayta quriladi, lekin uni ishlatayotgan deploy lar eski digest da qolib ketadi.

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

**ConfigMap va Secret cheksiz emas.** Konfiguratsiyani resursga chiqarish qulay bo'lgani uchun unga katta narsalar ham solinadi, lekin kanalning o'lchami bor. Secret hajmi etcd tufayli 1 MB bilan cheklangan, binar ma'lumot esa Base64 da saqlanadi va shu kodlash hisobiga amalda undan sezilarli kamroq joy qoladi. Bundan tashqari haqiqiy klasterlar namespace boshiga ConfigMap SONIGA ham quota qo'yadi, ya'ni "har sozlama uchun bitta ConfigMap" strategiyasi ma'lum nuqtada to'xtaydi. Shuning uchun katta konfiguratsiya - sertifikat to'plami, ML modeli, uzun statik ma'lumot fayli - ConfigMap ga emas, image ga yoki object storage ga tushadi, qarorni qabul qilishdan oldin esa haqiqiy hajm o'lchanadi.

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

**Profil fayllarini image ga solishning narxi.** Spring loyihalarida eng ko'p uchraydigan shakl - hamma muhit uchun `application-<profil>.yaml` fayllarini bitta image ichiga solib, qaysi biri ishlatilishini bitta muhit o'zgaruvchisi (`SPRING_PROFILES_ACTIVE`) bilan tanlash. U ishlaydi, lekin konfiguratsiyani ilovaga qattiq bog'laydi: dev va prod sozlamalari bitta image da yonma-yon turadi va ikkisidan birining o'zgarishi butun image ni qayta qurishni talab qiladi. Buni [o'zgarmas konfiguratsiya](#2916-ozgarmas-konfiguratsiya-immutable-configuration) bilan adashtirmaslik kerak: o'sha patternda bitta reliz artefaktiga BITTA muhitning konfiguratsiyasi qadaladi va o'zgarish yangi reliz orqali keladi, bu yerda esa hamma muhit bitta artefaktda yashaydi va har kichik o'zgarish hammasiga teng tegadi.

**Qiymat qayerdan kelganini kuzatish.** Env o'zgaruvchisini bir vaqtda bir necha darajada qo'yish mumkin: image ning o'z `ENV` i, Deployment dagi `env`, ConfigMap yoki Secret dan `valueFrom`, butun resursdan `envFrom`. Har daraja o'zidan oldingisining ustidan yozadi, shuning uchun markaziy ta'rif joyi belgilanmasa "bu qiymat qayerdan keldi" savoliga javob topish deyarli imkonsiz bo'ladi va konfiguratsiya xatosi debug qilinmaydigan toifaga o'tadi. Amaliy qoida ikkita: har servis uchun env manbalarining ro'yxati va ustuvorlik tartibi bitta joyda yozib qo'yiladi, va bitta konteynerda `envFrom` bilan alohida `env` qiymatlari aralashtirilmaydi.

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

**Shablonga o'tish chegarasi.** Shablonlash bepul emas, shuning uchun unga bitta shart bajarilganda o'tiladi: katta konfiguratsiyaning faqat kichik qismi muhitga bog'liq bo'lsa. Teskari yo'l - to'liq konfiguratsiyani har muhit ConfigMap iga nusxalash - boshida ishlaydi va hech qanday asbob talab qilmaydi, lekin nusxalar vaqt o'tishi bilan muqarrar bir-biridan uzoqlashadi: biriga tuzatish kiritiladi, boshqasiga unutiladi va farq faqat incident paytida chiqadi. Teskari chegara ham bor: o'zgaruvchi qismning ulushi katta bo'lsa shablon ham yordam bermaydi, chunki unda muhitlar haqiqatan boshqa va ularni alohida boshqarish to'g'ri qaror.

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

**Controller ni kuzatish narxi.** Controller yozish qarorining ko'pincha hisobga olinmaydigan tomoni - uni debug qilish qiyinligi. Hodisalar oqimi to'g'ri chiziqda bormaydi: watch uziladi, informer resync qiladi, bitta o'zgarish bir necha reconcile chaqiruviga aylanadi. Hammasini to'xtatib holatni bir joyda ko'rish uchun breakpoint qo'yish ham ishlamaydi, chunki to'xtatilgan reconcile paytida klaster o'zgarishda davom etadi va qaytganingizda holat boshqa bo'ladi. Shuning uchun kuzatuvchanlik controller ga keyin qo'shiladigan narsa emas, uning birinchi versiyasiga yoziladi: har reconcile uchun resurs nomi bilan log, qayta urinish va xato soni uchun metrika, muhim qarorlar uchun esa Kubernetes event.

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

**CRD ning ikki turi.** Operator yozishdan oldin CRD ni nima uchun kiritayotganingizni ayting, chunki ikki xil toifa bor va ularni aralashtirish resurs modelini chalkashtiradi.

- **Installation CRD** - ilovani Kubernetes platformasiga o'rnatish va boshqarish uchun. Namunasi Prometheus ning CRD lari: ular Prometheus ning o'zini o'rnatish va yuritish uchun ishlatiladi.
- **Application CRD** - ilovaga xos domen tushunchasini ifodalash uchun. Bu tur ilovaning Kubernetes bilan chuqur integratsiyasini beradi, ya'ni Kubernetes mexanizmini domen xulqi bilan birlashtiradi. Namunasi `ServiceMonitor`: Prometheus operatori uni muayyan Kubernetes Service larni scrape ro'yxatiga qo'shish uchun ishlatadi va server konfiguratsiyasini shunga moslashtiradi.

Bitta operator ikki turga ham ta'sir qilishi mumkin (Prometheus operatori shunday qiladi) va ikki toifa orasidagi chegara xira. Shuningdek "Operator - CRD ishlatadigan Controller" ta'rifi ham qat'iy emas: orasidagi variantlardan biri - CRD o'rniga ConfigMap ni domen konfiguratsiyasi sifatida ishlatadigan controller. Bu yondashuv standart Kubernetes resurslari yetmaganda, lekin CRD yaratish imkoni bo'lmaganda ma'noli: CRD ro'yxatga olish uchun cluster-admin huquqi kerak, ba'zi klaster sozlamalarida esa bu huquq umuman berilmaydi. ConfigMap bilan ham Observe-Analyze-Act halqasi saqlanadi, lekin bir nechta narsa yo'qoladi: CRD lar uchun bo'ladigan `kubectl get` darajasidagi asbob qo'llovi, API Server darajasidagi validatsiya, API versiyalash, `status:` maydonini o'zingiz xohlagancha modellashtirish imkoniyati va CRD turi bo'yicha alohida sozlanadigan nozik RBAC modeli - ConfigMap larda esa bitta namespace dagi barcha ConfigMap lar bir xil ruxsatni bo'lishadi.

**Qo'llanish keyslari:**
- Ichki Kafka yoki PostgreSQL klasterini CRD orqali deklarativ yaratish, backup va failover'ni avtomatlashtirish.
- Platforma jamoasi uchun `kind: Microservice` abstraksiyasi - bitta resurs Deployment, Service, Ingress va HPA'ni generatsiya qiladi.
- Tenant onboarding: `kind: Tenant` yaratilganda namespace, DB schema, quota va credential'larni avtomatik tayyorlash.
- ML model deploy'ini `kind: ModelServing` resursi orqali versiyalab, canary rollout bilan boshqarish.
- Sertifikat va credential rotatsiyasini domen qoidalariga mos ravishda o'zi bajaradigan operator.

**Operator va CRD ni tanlash mezonlari.** Bu bo'limning oxiridagi ogohlantirish qarorni bir tomondan yopadi: Helm yoki Kustomize yetadigan joyda operator yozilmaydi. Lekin qaror ikki tomonlik va ikkinchi tomoni ham yozilishi kerak. CRD va operator yo'liga kamida bitta shart bajarilganda o'tiladi: `kubectl` va mavjud Kubernetes asboblariga chuqur integratsiya kerak; loyiha greenfield va eski API ni saqlash majburiyati yo'q; resurs yo'li, API guruhi, versiyalash va namespace tushunchalaridan haqiqatan foyda olasiz; yoki watch, autentifikatsiya, RBAC va selector qo'llovi tayyor bo'lgan client kutubxonasi kerak.

Teskari tomoni ikki pog'onali. Oddiy Controller standart resurslar (ConfigMap, Secret, Deployment) bilan yetarli bo'lsa, CRD ro'yxatga olinmaydi: CRD cluster-admin huquqini talab qiladi, ConfigMap yo'li esa xavfsizlik va validatsiya tomonida cheklangan bo'lsa ham shu huquqsiz ishlaydi. Uchinchi variant esa ko'pincha umuman ko'rilmaydi: use case deklarativ bo'lmasa yoki ma'lumot Kubernetes resurs modeliga sig'masa, Kubernetes API sini cho'zish o'rniga mustaqil API yozib uni Service yoki Ingress orqali chiqarish to'g'riroq bo'ladi.

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

**Pod ichidagi konteynerlar nimani bo'lishadi.** Pod atomik bo'lgani uchun uning ichidagi konteynerlar IP manzilni, host nomini va PORT DIAPAZONINI birga ishlatadi. Shundan oddiy, lekin amalda tez-tez yiqitadigan talab chiqadi: bitta pod ga qo'shilayotgan konteynerlarning portlari oldindan kelishib olinadi, aks holda ikkinchisi birinchisi egallagan portga bog'lanishga urinib ishga tushmaydi. Spring Boot ilovasi yonida metrika exporter, proxy yoki log sidecar turganda `server.port` va `management.server.port` qiymatlari shu kelishuvning qismi bo'ladi.

**Rad etilgan alternativa: controller siz yaratilgan pod.** Pod ni to'g'ridan-to'g'ri, hech bir controller ostida bo'lmagan holda yaratish mumkin, lekin bu deploy birligi emas: node yiqilsa bunday pod qayta ishga tushmaydi va mavjud pod boshqa node ga HECH QACHON ko'chirilmaydi - Kubernetes pod ni ko'chirmaydi, uni faqat controller qayta yaratadi. Shu sababli bir martalik ish uchun ham yalang pod emas, `Job` yoziladi: evict bo'lgan Job pod i yangi sog'lom node da qayta ishlaydi.

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

**`LimitRange` bilan nisbatni cheklash.** `LimitRange` namespace da standart va chegara qiymatlarni beradi, lekin uning kamroq ishlatiladigan qismi amalda muhimroq: `requests` bilan `limits` orasidagi nisbatni cheklash (LimitRequestRatio). Nisbat katta bo'lsa node da `limits` yig'indisi `requests` yig'indisidan ancha oshadi va node overcommit holatiga tushadi: hamma konteyner bir vaqtda so'raganidan ko'proq olishga urinsa, ishlash hammada pasayadi va sababi bitta ilovada ko'rinmaydi. Nisbatni cheklash shu holatning ehtimolini kamaytiradi.

**Klaster sig'imini jadval bilan hisoblash.** Sig'im rejasi pod `requests` va `limits` qiymatlarini instans soniga ko'paytirib yoziladigan jadvaldan boshlanadi: har ilova uchun bitta qator, oxirida yig'indi va uni [node Allocatable qiymati](#294-avtomatlashtirilgan-joylashtirish-automated-placement) bilan taqqoslash. QoS ni muhit bo'yicha taqsimlash ham shu jadvalning qismi: prod da asosan Guaranteed va bir oz Burstable, nonprod da esa Best-Effort va Burstable ma'noli taqsimot bo'ladi. Shundan keyin bitta signal aniq o'qiladi - prod da pod resurs tanqisligi tufayli o'ldirilsa, bu sozlama xatosi emas, klaster sig'imini oshirish kerakligining belgisi.

**Ehtiyot bo'ling:** `limits`ni belgilamaslik ham, `requests`ni real iste'moldan ancha yuqori qo'yish ham zarar: birinchisida bitta ilova node'ni yiqitadi, ikkinchisida klasterning yarmi bo'sh turgan holda to'la hisoblanadi. CPU limitini juda past qo'yish Spring Boot ilovasini startup paytida throttling'ga uchratib, liveness probe'ning noto'g'ri restart tsikliga olib keladi; memory limitida esa heap'ni limitga teng qilib qo'ymang - JVM'ning non-heap qismi ham o'sha limit ichida hisoblanadi.

## 29.23 Pod uzilish byudjeti (Pod Disruption Budget)

**Tavsif:** Ibryam va Huss PodDisruptionBudget'ni Singleton Service'ning to'ldiruvchi va qarama-qarshi tomoni deb ta'riflaydi: Singleton Service bir vaqtda ISHLAYDIGAN nusxalarning maksimumini cheklasa, PDB bir vaqtda O'CHIRILGAN nusxalarning maksimumini cheklaydi. Byudjet faqat ixtiyoriy (voluntary) eviction'ga tegishli, ya'ni kechiktirilishi mumkin bo'lgan uzilishga: `kubectl drain`, node'ni yangilash, cluster scale-down. Node'ning o'zi nosoz bo'lib qolishi ixtiyorsiz uzilish va PDB uni to'sa olmaydi. Resursda yoki `.spec.minAvailable` (kamida shuncha pod tirik qolsin), yoki `.spec.maxUnavailable` beriladi, ikkisi birga berilmaydi; qiymat son yoki foiz bo'lishi mumkin. PDB odatda faqat controller boshqaradigan pod'larga (Deployment, StatefulSet) ishlaydi, nazoratsiz "yalang'och" pod'lar uchun qo'shimcha cheklovlar bor. Asosiy qo'llanish joyi - kvorumga tayangan ilovalar va hech qachon ma'lum foizdan pastga tushmasligi kerak bo'lgan kritik trafik.

**Spring'da qayerda uchraydi:** PDB manifest darajasida yashaydi, lekin uning hisobi Spring Boot ilovasining readiness signaliga bog'liq: byudjet "available" deb faqat `Ready` holatdagi pod'ni sanaydi, demak `/actuator/health/readiness` nohalol `UP` bersa, PDB node drain'ga noto'g'ri ruxsat beradi. Teskarisi ham xavfli: readiness guruhiga tashqi bog'liqlik qo'shilib pod uzoq vaqt `Ready` bo'lmasa, drain cheksiz bloklanadi va cluster yangilanmaydi. Shuning uchun `management.endpoint.health.group.readiness.include` tarkibini ataylab tanlash kerak. Kvorumli ilovalarda (Hazelcast yoki Infinispan embedded cluster, `spring-integration-jdbc` lock registry'siga tayangan leader, ShedLock bilan himoyalangan `@Scheduled`) o'z `HealthIndicator`'i kvorum yo'qolganini readiness'ga chiqaradi. PDB `server.shutdown=graceful` va `terminationGracePeriodSeconds` bilan birga ishlaydi: byudjet qancha pod ketishi mumkinligini, graceful shutdown esa ketayotgan pod so'rovlarni yo'qotmasligini ta'minlaydi.

```java
@Component("replicaQuorum")
class ReplicaQuorumHealthIndicator implements HealthIndicator {

    private final ClusterMembership membership;

    ReplicaQuorumHealthIndicator(ClusterMembership membership) {
        this.membership = membership;
    }

    @Override
    public Health health() {
        int live = membership.liveMemberCount();
        // PDB faqat Ready pod'ni available sanaydi: kvorum yo'qolsa
        // readiness DOWN bo'lib, keyingi ixtiyoriy eviction to'siladi
        return live >= 2
                ? Health.up().withDetail("live", live).build()
                : Health.down().withDetail("live", live).build();
    }
}
```

**Qo'llanish keyslari:**
- Uch replica'li to'lov servisiga `minAvailable: 2` qo'yib, node yangilash paytida xizmatni uzmaslik.
- Kvorumga tayangan embedded cache cluster'ini (Hazelcast) drain vaqtida bir vaqtda ikki a'zodan ayrilishdan saqlash.
- Ko'p replica'li read-only API uchun `maxUnavailable: 20%` berib, yangilashni tez, lekin xavfsiz qilish.
- Leader'ga tayangan `@Scheduled` worker'da leader va standby bir vaqtda ketmasligini kafolatlash.
- Kafka consumer group'da bir vaqtda ko'p consumer ketib, rebalans bo'roni ko'tarilishini oldini olish.

**Ehtiyot bo'ling:** Byudjetni ilovaning haqiqiy replica sonidan baland qo'yish (masalan ikki replica'ga `minAvailable: 2`) node drain'ni butunlay to'xtatadi va platforma yangilanmay qoladi; bu PDB bilan eng ko'p uchraydigan operatsion tuzoq. Ibryam va Huss yana bir muhim cheklovni eslatadi: yuqori prioritetli pod joy izlab preemption qilganda PDB kafolatlanmaydi, shuning uchun PDB'ni kvorumning yagona himoyasi deb hisoblamang.

## 29.24 Pod prioriteti va preemption (Pod Priority & Preemption)

**Tavsif:** `PriorityClass` - namespace'ga bog'lanmagan resurs, u butun son qiymat (`value`) orqali pod'larning bir-biriga nisbatan muhimligini belgilaydi; pod unga `priorityClassName` bilan ulanadi. Priority admission controller yangi pod'ga shu qiymatni yozadi, scheduler esa kutayotgan pod'lar navbatini eng baland prioritetdan boshlab tartiblaydi. Eng muhim qismi preemption: agar hech bir node'da joy bo'lmasa, scheduler past prioritetli pod'larni node'dan chiqarib, baland prioritetlisiga joy ochadi. Ibryam va Huss ta'kidlashicha, prioritet va QoS klassi ortogonal mexanizmlar: kubelet node barqarorligini saqlash uchun avval QoS'ni, keyin `PriorityClass`'ni ko'radi, scheduler esa preemption nishonini tanlashda QoS'ni butunlay e'tiborsiz qoldiradi va faqat eng past prioritetli to'plamni izlaydi.

**Spring'da qayerda uchraydi:** Spring'da bu patternga mas'ul annotatsiya yo'q, lekin ilova "ko'chirilishga tayyor" bo'lishi kerak. Preemption oddiy graceful termination bilan boshlanadi, ya'ni pod `SIGTERM` oladi: shuning uchun `server.shutdown=graceful` va `spring.lifecycle.timeout-per-shutdown-phase` to'g'ri sozlangan past prioritetli ilova zarar ko'rmaydi. Uzoq ishlaydigan batch va reporting ilovalarini past prioritetga qo'yib, ular `SmartLifecycle.stop()` yoki `@PreDestroy` ichida progress checkpoint'ini saqlashi ma'qul; Spring Batch'da buning tayyor shakli `JobRepository` va restart imkoniyati. Latency sezgir web servislarni esa baland prioritetga qo'yish va `requests` bilan `limits`ni teng berib Guaranteed QoS'ga chiqarish birga ishlaydi. Micrometer'ning `jvm.memory.used` va `process.uptime` metrikalari pod kutilmaganda ko'chirilganini keyin tahlil qilishga yordam beradi.

```java
@Component
class CheckpointingWorker implements SmartLifecycle {

    private final CheckpointStore store;
    private volatile boolean running;
    private volatile long processedOffset;

    CheckpointingWorker(CheckpointStore store) { this.store = store; }

    @Override public void start() { running = true; }

    @Override
    public void stop() {
        running = false;
        // past prioritetli pod istalgan payt preemption bilan ketadi:
        // SIGTERM oynasida progressni saqlab qolamiz
        store.save(processedOffset);
    }

    @Override public boolean isRunning() { return running; }
}
```

**Qo'llanish keyslari:**
- Kritik to'lov API'siga baland `PriorityClass` berib, trafik cho'qqisida u albatta joylashishini ta'minlash.
- Kechqurun ishlaydigan ETL job'larini past prioritetga qo'yib, kunduzgi yuklamaga xalal bermaslik.
- Spot node pool'da ishlaydigan checkpoint qiladigan batch worker'larini eng past prioritetga chiqarish.
- Platforma komponentlarini (log collector, metrika agenti) ilova pod'laridan baland prioritetda ushlab turish.
- `ResourceQuota`'ni `PriorityClass` bo'yicha cheklab, jamoalar o'zboshimchalik bilan baland prioritet olishini to'sish.

**Ehtiyot bo'ling:** Ibryam va Huss prioritetdan ehtiyotkorlik bilan foydalanishni so'raydi: qiymatlarni foydalanuvchi o'zi yozgani uchun mexanizm "o'yinga" ochiq - xabardor bo'lmagan yoki niyati buzuq foydalanuvchi eng baland prioritetli pod yaratib qolganlarini chiqarib tashlashi mumkin, shu sababli `ResourceQuota` `PriorityClass`'ni qo'llashga kengaytirilgan va katta raqamlar tizim pod'lari uchun zaxiralangan. Ikkinchi xavf - preemption vaqtida [Pod uzilish byudjeti](#2923-pod-uzilish-byudjeti-pod-disruption-budget) kafolatlanmaydi, bu esa kvorumga tayangan past prioritetli cluster'ni buzishi mumkin.

## 29.25 Klasterni bo'lishish: multitenancy va federatsiya (Multitenancy and Federation)

**Tavsif:** Samaradorlik nuqtasidan eng to'g'ri javob oddiy ko'rinadi: barcha hisoblash resurslarini bitta Kubernetes klasterida yig'ib, tashkilotdagi hamma yuklamani shu yerda ishlatish - ishlatilmayotgan resurs kimga kerak bo'lsa shunga qayta taqsimlanadi, utilizatsiya oshadi, xarajat tushadi. Muammo shunda: Kubernetes turli maqsadlar uchun turli mikroservislarni boshqarishda yaxshi, lekin platformaning **multitenant** darajasi cheklangan. Tashkilotdagi har bir bo'lim turli resurslar ustidan turli darajada nazorat xohlaydi, bu nazorat vositalari esa Kubernetes ga qurib qo'yilmagan - bu Kubernetes qamrovini cheklangan ushlash nuqtasidan asosli qaror. Natijada tashkilotlar ikki yo'ldan birini tanlaydi.

- **Kubernetes ustidagi platforma.** Red Hat ning OpenShift i kabi yechimlar yirik tashkilotlarni hisobga olib qurilgan boy kirish nazorati va boshqa imkoniyatlarni beradi, multitenancy tushunchasini ancha osonlashtiradi. Narxi faqat litsenziya emas: ular ishlashi uchun ba'zan vendor bergan abstraksiyalar bilan ishlashga to'g'ri keladi, ya'ni developer lar nafaqat Kubernetes ni, o'sha vendor platformasini ham bilishi kerak bo'ladi.
- **Federatsiya.** Bir nechta alohida klaster saqlanadi, ustiga esa kerak bo'lganda hammasiga birdan o'zgarish kiritish imkonini beradigan dasturiy qatlam qo'yiladi. Ko'p holda odamlar bitta klaster bilan to'g'ridan-to'g'ri ishlaydi va tanish Kubernetes tajribasini oladi; ba'zi holatda esa ilovani bir nechta klaster bo'ylab tarqatish kerak bo'ladi, masalan klasterlar turli geografiyada bo'lsa va butun bir klaster yo'qolishiga chidash kerak bo'lsa.

Federatsiyaning o'z narxi bor va u aynan birinchi maqsadga - resurslarni bir joyga yig'ishga - qarshi ishlaydi. A klasteri to'liq band, B klasterida esa ko'p bo'sh sig'im bo'lsa, A da ko'proq yuklama ishlatish faqat unga ko'proq resurs berilsa mumkin, ya'ni B dagi bo'sh node ni A ga ko'chirish kerak bo'ladi; buning qanchalik oson bo'lishi federatsiya dasturiga bog'liq, lekin oson bo'lmasligi kutiladi. Sababi qat'iy: bitta node yoki bir klasterning, yoki boshqasining qismi bo'ladi, ikkisi uchun birga pod ishlata olmaydi. Buning teskari tomoni ham bor: bir nechta klaster klasterning o'zini yangilashni osonlashtiradi - mikroservisni yangilangan klasterga ko'chirish ko'pincha klasterni joyida yangilashdan oson va xavfsizroq.

**Spring'da qayerda uchraydi:** Bu qaror Spring ilovasining kodiga tegmaydi, lekin konfiguratsiyasiga tegadi. Ilova klaster nomiga, namespace nomiga yoki vendor abstraksiyasiga qattiq bog'lanmasligi kerak: ko'p klasterli muhitda ishlashi mumkin bo'lgan Spring Boot ilovasi klaster identifikatorini Downward API orqali `env` ga olib, uni Micrometer tag i qilib qo'yadi (`MeterRegistryCustomizer`) va log hamda trace ga chiqaradi - shunda metrika qaysi klasterdan kelgani ko'rinadi. Konfiguratsiya klaster ichidagi ConfigMap/Secret dan kelsa, federatsiyada u har klasterda takrorlanadi; shuning uchun ko'p klasterli ssenariyda konfiguratsiyani klaster tashqarisidagi manbaga (Spring Cloud Config Server, Vault) chiqarish va klasterga xos qismini faqat `spring.config.import` bilan ustiga qo'shish barqarorroq. Klasterlar orasida ulanish kerak bo'lsa, servis nomi `*.svc.cluster.local` bilan hal bo'lmaydi: tashqi DNS yoki service mesh ning multicluster rejimi talab qilinadi.

**Qo'llanish keyslari:**
- Bir nechta bo'lim bitta klasterni bo'lishishi kerak bo'lganda, nazorat talablari Kubernetes ning o'z RBAC va quota mexanizmidan oshsa, OpenShift kabi platformani baholash.
- Ikki geografiyada klaster saqlab, kritik ilovani ikkisiga tarqatish va butun klaster yo'qolishiga chidash.
- Klaster versiyasini yangilashda ilovani yangi klasterga ko'chirish yo'lini joyida yangilash bilan taqqoslash.
- Utilizatsiya hisobini federatsiya narxi bilan birga chiqarish: bo'sh node ni klasterlar orasida ko'chirish qanchalik qiyin ekanini oldindan o'lchash.
- Kichik tashkilotda bitta klasterni bo'lishib, bu masalaga umuman kirmaslik - bu ham haqli javob.

**Ehtiyot bo'ling:** Bu masshtab muammosi, hamma uchun emas: bitta klasterni bo'lishishdan xursand bo'lgan tashkilot bu savollarga hech qachon kelmaydi. Shu sababli multitenancy yoki federatsiyani "to'g'ri arxitektura" deb oldindan qurish tipik ortiqcha injinerlik: u bitta klasterning quota, RBAC va NetworkPolicy imkoniyatlari haqiqatan yetmaganida boshlanadi. Ikkinchi ehtiyot - Kubernetes federatsiyasi qanday ko'rinishi kerakligi haqida bir necha xil qarash va ularni boshqaradigan bir necha xil asboblar zanjiri bor, ya'ni bu yerda bitta standart yechim yo'q; tanlovni o'z talablaringiz ro'yxati bilan tekshiring.

## 29.26 Scheduler siyosati va joylashtirishga aralashuv (Scheduler Policy and Placement Intervention)

**Tavsif:** [Avtomatlashtirilgan joylashtirish](#294-avtomatlashtirilgan-joylashtirish-automated-placement) mexanizmlarni beradi, bu bo'lim esa ulardan qaysi birini QANCHA ishlatish kerakligini beradi. Scheduler siyosati ikki bosqichdan iborat: predicate lar mos kelmaydigan node larni filtrlaydi, priority lar esa qolganlarini vazn bilan tartiblaydi va eng baland bahoni olgan node tanlanadi. Siyosatning o'zini va o'z scheduler ini faqat klaster administratori belgilaydi; oddiy foydalanuvchi pod ta'rifida mavjud scheduler ga havola qila oladi, undan ko'p emas. Ikkinchi yarmi qaror tartibi: joylashtirishga aralashuv vositalari bir xil og'irlikda emas, shuning uchun ular eng oddiydan eng murakkabga qarab tanlanadi va MINIMAL aralash qoidasi amal qiladi. Uchinchi jihati vaqt: scheduler joylashtirgandan keyin qarorini qayta ko'rmaydi, demak klaster o'zgarganda eski joylashuvlarni tuzatish alohida ish bo'lib qoladi.

**Spring'da qayerda uchraydi:** Bu qarorlarga mas'ul Spring sinfi yo'q, lekin natijasi Spring ilovasining xulqida ko'rinadi va diagnostikada aynan shu savol beriladi: "bu pod nega shu node ga tushdi". Joylashuvni ilovaning o'zidan ko'rish uchun Downward API `spec.nodeName` va `metadata.labels['topology.kubernetes.io/zone']` qiymatlarini env ga beradi, Micrometer'ning `MeterRegistryCustomizer` i esa ularni umumiy tag qilib qo'yadi - shunda bitta node dagi pod larning latency i boshqalardan farq qilgani metrikadan ko'rinadi. Aralashuvning Spring tomonidagi narxi ham bor: qattiq joylashuv cheklovlari pod ni `Pending` da ushlab turganda HPA scale-out ga ulgurmaydi va `readinessProbe` vaqtida tayyor bo'lmaydi, shuning uchun cheklovlarni `spring.lifecycle.timeout-per-shutdown-phase` va probe sozlamalari bilan birga baholash kerak.

```yaml
# Aralashuvning eng yengil pog'onalari: node sinfi label bilan, maxsus pool toleration bilan
spec:
  nodeSelector:
    node-class: memory-optimized    # eng oddiy va eng tushunarli cheklov
  tolerations:
    - key: workload                 # taint opt-in: node sukut bo'yicha yopiq
      operator: Equal
      value: batch
      effect: NoSchedule            # NoExecute bo'lsa ishlayotgan pod ham chiqariladi
  # schedulerName: custom-scheduler # oxirgi pog'ona: faqat administrator beradi
```

**Qo'llanish keyslari:**
- Spot node pool ini `taints` bilan yopib, unga faqat chidamli batch ilovalarini `tolerations` orqali kiritish.
- Pod `Pending` da qolganda sababni predicate (joy yo'q, label mos emas) va priority (bor, lekin boshqa node yaxshiroq baholangan) darajalarida ajratib tekshirish.
- Klaster o'sgandan keyin joylashuvni descheduler bilan qayta tekislab, node fragmentatsiyasini kamaytirish.
- Yangi node pool qo'shilganda label ni hamma pod ga tarqatish o'rniga taint va toleration bilan faqat kerakli pod larni yo'naltirish.
- `nodeName` yozilgan legacy manifestlarni topib, ularni `nodeSelector` yoki node affinity ga ko'chirish.

**Aralashuv zinapoyasi.** Vositalar quyidagi tartibda, eng oddiydan eng murakkabga qarab ko'riladi va talab qondirilgan joyda to'xtaladi:

1. **`nodeName`** - pod ni aniq node ga qattiq bog'lash. Bu Kubernetes dan oldingi davrga qaytarish: joylashtirishni butunlay o'chiradi, node yiqilsa pod ko'chmaydi. Qilmang.
2. **`nodeSelector`** - node label i bo'yicha oddiy tanlov. Ko'p holat shu bilan tugaydi.
3. **Default scheduler siyosatini o'zgartirish** - klaster darajasidagi qaror, administrator ishi.
4. **Pod affinity va antiaffinity** - pod larni bir-biriga nisbatan joylashtirish.
5. **Node affinity** - label ifodalari bilan yumshoq va qattiq talablar.
6. **Taint va toleration** - node ni himoyalash va unga ruxsat berish.
7. **O'z scheduler i** - `spec.schedulerName` yoki scheduler extender. Eng murakkab va eng qimmat pog'ona.

**Taint va toleration teskari yo'naltirilgan.** Affinity bilan taint ni adashtirish keng tarqalgan xato, chunki ular bir xil natijaga qarama-qarshi tomondan keladi. Affinity - pod ning node tanlashi va u opt-out ishlaydi: ifodaga mos kelmagan hamma node chiqarib tashlanadi. Taint - node ning pod ni qabul qilmasligi va u opt-in ishlaydi: node sukut bo'yicha yopiq, faqat mos toleration ga ega pod kiradi. Taint ning uch effekti bor va ularning kuchi teng emas: `NoSchedule` qattiq to'siq, `PreferNoSchedule` yumshoq (imkon bo'lsa boshqa node tanlanadi), `NoExecute` esa allaqachon ishlab turgan pod ni ham node dan chiqaradi - `NoExecute` ni bilmaslik kutilmagan evict larning tez-tez uchraydigan sababi. Mexanizmning kam aytiladigan afzalligi shu tomondan chiqadi: klasterga yangi label li node qo'shilganda label ni HAMMA pod ga tarqatish kerak emas, faqat o'sha node ga tushishi kerak bo'lgan pod larga toleration qo'shiladi.

**Joylashuv statik, uni descheduler tuzatadi.** Scheduler pod ni joylashtirgandan keyin qarorini qayta ko'rmaydi: node qo'shilsa, label o'zgarsa yoki yuklama boshqa shaklga kirsa ham eski joylashuvlar o'z joyida qoladi va vaqt o'tishi bilan resurs fragmentatsiyasi yig'iladi. Buni descheduler hal qiladi: u doimiy ishlaydigan komponent emas, Job sifatida administrator xohlagan paytda ishga tushiriladi va siyosatga mos kelmaydigan pod larni evict qiladi, keyin ularni oddiy scheduler qaytadan joylashtiradi. Descheduler nimani evict QILMASLIGINI bilish ham qarorning qismi: kritik pod lar, controller boshqarmaydigan pod lar, DaemonSet pod lari, lokal diski bor pod lar va [uzilish byudjetini](#2923-pod-uzilish-byudjeti-pod-disruption-budget) buzadigan evict lar ro'yxatdan chiqariladi. Evict tartibi esa QoS ga rioya qiladi, ya'ni kubelet ning node bosimidagi tartibi bilan bir xil: avval Best-Effort, keyin Burstable, oxirida Guaranteed.

**Osilib qolgan resurs.** Scheduler ni haddan tashqari cheklash yoki node bilan konteyner o'lchamini nomutanosib tanlash node da "osilib qolgan" (stranded) resurs qoldiradi: masalan node da bir necha gigabayt xotira bo'sh turadi, lekin CPU qolmagani uchun unga hech narsa joylashmaydi. Hisobda node to'liq ko'rinadi, amalda esa uning bir qismi ishlatilmaydi va bu [sig'im hisobining](#2922-resurs-sorovlari-va-limitlari-resource-requests--limits) teskari tomoni. Ikki yo'li bor: resurs talablarini maydaroq qilib node ga zichroq joylashtirish, yoki yig'ilgan fragmentatsiyani descheduler bilan vaqti-vaqti bilan tozalash.

**Ehtiyot bo'ling:** Aralashuv zinapoyasining har pog'onasi keyingi operatsiyani qimmatlashtiradi: `nodeName` va qattiq affinity yozilgan manifest node almashtirishni, klaster yangilashni va autoscaling ni to'sadi, chunki pod ning boradigan joyi qolmaydi. Ikkinchi tuzoq descheduler da: uni siyosatini o'qimasdan muntazam jadvalga qo'yish pod larni foydasiz aylantirib, kesh isishi va ulanish pool larini doimiy sindirib turadi - avval bir marta qo'lda ishlatib, nimani evict qilganini ko'rib chiqish kerak. Uchinchisi diagnostika tomonida: "pod joylashmadi" degan xabarni predicate va priority bosqichlariga ajratmasdan tekshirish vaqtni behuda sarflaydi, chunki ikki bosqichning yechimi boshqa.

## 29.27 Amalda qo'llash

- [ ] Har bir pod uchun `requests` va `limits` qiymatlarini o'lchangan p95 CPU va maksimal RSS ga asoslab qayta hisoblang.
- [ ] Readiness, liveness va startup probe'lari uchta alohida maqsadga xizmat qilayotganini tasdiqlang.
- [ ] Graceful shutdown va `terminationGracePeriodSeconds` qiymatlari ilovaning eng uzun so'rovidan katta ekanini tekshiring.
- [ ] ConfigMap va Secret dan keladigan qiymatlarni ro'yxatga olib, o'zgarganda restart kerakligini yozib qo'ying.
- [ ] HPA sozlamalarini tekshiring: metrika to'g'ri tanlanganmi, minimal nusxa soni nol emasmi.
- [ ] Pod disruption budget borligini va reliz paytida xizmat uzilmasligini tasdiqlang.
- [ ] Init container va sidecar larni sanab chiqib, har birining nega kerakligini yozib qo'ying.
- [ ] Stateless talabini tekshirish uchun bitta podni ataylab o'chirib ko'ring va natijani hujjatlashtiring.
- [ ] Node larda `kube-reserved` va `system-reserved` berilganini va `requests` yig'indisi Allocatable ga sig'ishini tekshiring.
- [ ] Klaster tashqarisidagi har bir bog'liqlik (baza, legacy servis) uchun ichki Service nomi borligini tasdiqlang, ilovada tashqi host nomi qattiq yozilmaganini tekshiring.
- [ ] `kubectl scale` bilan qo'lda qilingan o'zgarishlar git dagi manifestga qaytarilganini tekshirib, configuration drift ro'yxatini yopib qo'ying.

## Manbalar

- [Kubernetes, Deployment](https://raw.githubusercontent.com/kubernetes/website/e91eff3b59c0bf813193202a4f193d37beb7efd7/content/en/docs/concepts/workloads/controllers/deployment.md) - rolling update, `maxSurge` va `maxUnavailable`
- [Kubernetes, Pod Lifecycle](https://raw.githubusercontent.com/kubernetes/website/e91eff3b59c0bf813193202a4f193d37beb7efd7/content/en/docs/concepts/workloads/pods/pod-lifecycle.md) - probe turlari va to'xtatish tartibi
- Bilgin Ibryam, Roland Huss, *Kubernetes Patterns: Reusable Elements for Designing Cloud-Native Applications*, 1-nashr, O'Reilly, 2019, 10-bob (84-85-betlar) - PodDisruptionBudget faqat ixtiyoriy eviction'ni cheklaydi, `minAvailable` va `maxUnavailable` birga berilmaydi
- Bilgin Ibryam, Roland Huss, *Kubernetes Patterns: Reusable Elements for Designing Cloud-Native Applications*, 1-nashr, O'Reilly, 2019, 2-bob (20-22-betlar) - `PriorityClass`, preemption va QoS bilan ortogonalligi, `ResourceQuota` ning `PriorityClass` ni qo'llashi, prioritetning "o'yinga" ochiqligi
- Bilgin Ibryam, Roland Huss, *Kubernetes Patterns: Reusable Elements for Designing Cloud-Native Applications*, 1-nashr, O'Reilly, 2019, 6-bob (48-bet) - Allocatable formulasi (node capacity minus kube-reserved minus system-reserved), zaxira berilmasa pod va tizim demonlarining resurs uchun kurashi, Kubernetes bilmagan konteynerlar uchun placeholder pod (29.4)
- Bilgin Ibryam, Roland Huss, *Kubernetes Patterns: Reusable Elements for Designing Cloud-Native Applications*, 1-nashr, O'Reilly, 2019, 5-bob (43-44-betlar) - `postStart` hook: asosiy protsess bilan asinxron, lekin bloklovchi (Pod `Pending` da qoladi), nol bo'lmagan chiqish kodi asosiy protsessni o'ldirishi, `exec` va `httpGet` handler turlari, bajarilishiga kafolat yo'qligi (29.3)
- Bilgin Ibryam, Roland Huss, *Kubernetes Patterns: Reusable Elements for Designing Cloud-Native Applications*, 1-nashr, O'Reilly, 2019, 12-bob (104-106-betlar) - selector siz Service va qo'lda yaratilgan Endpoints, `ExternalName` bilan DNS CNAME taxallusi, Service ni o'chirmasdan selector qo'shib provider ni klasterga ko'chirish (29.11)
- Bilgin Ibryam, Roland Huss, *Kubernetes Patterns: Reusable Elements for Designing Cloud-Native Applications*, 1-nashr, O'Reilly, 2019, 24-bob (204-205-betlar) - qo'lda masshtablashning imperativ (`kubectl scale`) va deklarativ (`kubectl apply`) uslublari, configuration drift, oldindan masshtablash imkoniyati, StatefulSet PVC asimmetriyasi va Job ning `parallelism` maydoni (29.13)
- Bilgin Ibryam, Roland Huss, *Kubernetes Patterns: Reusable Elements for Designing Cloud-Native Applications*, 1-nashr, O'Reilly, 2019, 23-bob (192-193-betlar) - Installation CRD va Application CRD farqi (Prometheus va `ServiceMonitor` misollari), CRD o'rniga ConfigMap bilan Observe-Analyze-Act va bu almashtirishda yo'qoladigan narsalar (29.20)
- Bilgin Ibryam, Roland Huss, *Kubernetes Patterns: Reusable Elements for Designing Cloud-Native Applications*, 1-nashr, O'Reilly, 2019, 12-bob (107-110-betlar) - klaster tashqarisidan Service topish: `NodePort` (port tanlash, firewall qoidalari, node ni tanlash mijoz ishi, `externalTrafficPolicy: Local` bilan qo'shimcha hop va source NAT dan qochish va uning narxi), `LoadBalancer` (provayder LB si sog'lom node ni tanlashi, manba manzilining provayderga bog'liqligi) va `clusterIP: None` headless Service (29.11)
- Chris Richardson, *Microservices Patterns: With examples in Java*, Manning, 2019, 12-bob, 405-407-betlar - API gateway ni klaster tashqarisiga ochish: `ClusterIP` faqat ichki, `NodePort` (30000-32767 diapazoni, o'z load balancer ini to'liq nazorat qilish imkoni) va `LoadBalancer` (avtomatik cloud LB, konfiguratsiya nazorati kam) (29.11)
- Bilgin Ibryam, Roland Huss, *Kubernetes Patterns: Reusable Elements for Designing Cloud-Native Applications*, 1-nashr, O'Reilly, 2019, 1-bob (2, 7, 8 va 9-betlar) - konteyner patternlari kod sifatini almashtirmasligi, Pod ichidagi konteynerlarning IP, nom va port diapazonini bo'lishishi, scheduling uchun noyob label kombinatsiyasi va label ni olib tashlashning xavfi, label (qidirish va tanlash) bilan annotation (qidirilmaydigan mashina metadatasi) ajratmasi (29 kirishi, 29.4, 29.21)
- Bilgin Ibryam, Roland Huss, *Kubernetes Patterns: Reusable Elements for Designing Cloud-Native Applications*, 1-nashr, O'Reilly, 2019, 2-bob (17 va 22-betlar) - `hostPort` node da portni band qilib replica sonini node soniga bog'lashi, runtime bog'liqlikning ikki nosozlik rejimi (volume turi pod ni joylashtirmaydi, yo'q ConfigMap joylashtiradi lekin ishga tushirmaydi), `LimitRange` ning `requests`/`limits` nisbatini cheklashi va overcommit, klaster sig'imini jadval bilan hisoblash hamda QoS ni muhit bo'yicha taqsimlash (29.1, 29.22)
- Bilgin Ibryam, Roland Huss, *Kubernetes Patterns: Reusable Elements for Designing Cloud-Native Applications*, 1-nashr, O'Reilly, 2019, 5-bob (43 va 44-betlar) - `postStart` ning at-least-once semantikasi va muvaffaqiyatsiz `httpGet` uchun qayta urinish yo'qligi, `preStop` ni ushlab turish yoki undan xato qaytarish konteyner o'chirilishini to'xtatmasligi (29.3)
- Bilgin Ibryam, Roland Huss, *Kubernetes Patterns: Reusable Elements for Designing Cloud-Native Applications*, 1-nashr, O'Reilly, 2019, 6-bob (49, 54-58-betlar) - scheduler siyosatining ikki bosqichi (predicate filtrlaydi, priority tartiblaydi) va uni faqat administrator belgilashi, taint/toleration ning affinity ga nisbatan teskari yo'nalishi va uch effekti (`NoSchedule`, `PreferNoSchedule`, `NoExecute`), yangi label li node da label ni hamma pod ga tarqatmaslik afzalligi, joylashuvning statikligi va descheduler ning Job sifatida ishlatilishi hamda evict istisnolari va QoS tartibi, osilib qolgan (stranded) resurs, joylashtirishga aralashuv zinapoyasi `nodeName` dan o'z scheduler iga (29.26)
- Bilgin Ibryam, Roland Huss, *Kubernetes Patterns: Reusable Elements for Designing Cloud-Native Applications*, 1-nashr, O'Reilly, 2019, 7-bob (64-67-betlar) - controller siz yaratilgan pod node yiqilganda qayta ishga tushmasligi va pod ning hech qachon ko'chirilmasligi, `parallelism` ning parallellikni kafolatlamasligi va `parallelism: 0` bilan pauza, Job ning uch turi (fixed completion count, work queue, cheksiz oqim uchun ReplicaSet) va bo'lak granularligi qarori (29.5, 29.21)
- Bilgin Ibryam, Roland Huss, *Kubernetes Patterns: Reusable Elements for Designing Cloud-Native Applications*, 1-nashr, O'Reilly, 2019, 10-bob (81 va 85-betlar) - qat'iy singleton uchun StatefulSet izchillikni mavjudlikdan ustun qo'yishi va "ko'pi bilan bitta" kafolati, servisning faqat bir qismi yakka bo'lishi kerak bo'lganda ilova ichidagi lock ni tanlash (29.8)
- Bilgin Ibryam, Roland Huss, *Kubernetes Patterns: Reusable Elements for Designing Cloud-Native Applications*, 1-nashr, O'Reilly, 2019, 11-bob (88, 93, 95 va 96-betlar) - rad etilgan ikki alternativa (umumiy storage ni ilova ichidan papkaga bo'lish va har instans uchun qo'lda ReplicaSet plus PVC plus Service), `serviceName` ning majburiyligi va boshqaruvchi Service ning oldin yaratilishi, headless Service ning SRV yozuvi, `updateStrategy.rollingUpdate.partition` va `podManagementPolicy: Parallel`, kafolatni operator amallari (node obyektini o'chirish, `--grace-period=0 --force`) buzishi (29.10)
- Bilgin Ibryam, Roland Huss, *Kubernetes Patterns: Reusable Elements for Designing Cloud-Native Applications*, 1-nashr, O'Reilly, 2019, 12-bob (103, 104 va 111-betlar) - muhit o'zgaruvchisi orqali topishning vaqt bog'liqligi, virtual IP ning tarmoq interfeysiga mos kelmasligi va ICMP uchun iptables qoidasi yozilmasligi, L4 balanslash va `sessionAffinity: ClientIP` dan boshqa yopishqoqlik yo'qligi, `spec.clusterIP` ni qo'lda tanlashning ikki istisnosi, Ingress ni bitta tashqi IP ni qayta ishlatish uchun tanlash va uning L7 sharti (29.11)
- Bilgin Ibryam, Roland Huss, *Kubernetes Patterns: Reusable Elements for Designing Cloud-Native Applications*, 1-nashr, O'Reilly, 2019, 18-bob (148 va 149-betlar) - profil fayllarini image ga solib bitta env bilan tanlashning narxi (konfiguratsiya ilovaga bog'lanadi, har o'zgarish image ni qayta qurishni talab qiladi) va env ni ko'p darajada qo'yish qiymat manbasini kuzatishni yo'qotishi (29.17)
- Bilgin Ibryam, Roland Huss, *Kubernetes Patterns: Reusable Elements for Designing Cloud-Native Applications*, 1-nashr, O'Reilly, 2019, 19-bob (156-bet) - Secret hajmining etcd tufayli 1 MB bilan cheklanishi, Base64 kodlashning amaldagi joyni kamaytirishi va klasterlarning namespace boshiga ConfigMap soniga quota qo'yishi (29.15)
- Bilgin Ibryam, Roland Huss, *Kubernetes Patterns: Reusable Elements for Designing Cloud-Native Applications*, 1-nashr, O'Reilly, 2019, 21-bob (170-bet) - shablonga o'tish sharti: faqat katta konfiguratsiyaning kichik qismi muhitga bog'liq bo'lganda; to'liq nusxalash vaqt o'tishi bilan uzoqlashishga olib kelishi (29.18)
- Bilgin Ibryam, Roland Huss, *Kubernetes Patterns: Reusable Elements for Designing Cloud-Native Applications*, 1-nashr, O'Reilly, 2019, 22-bob (186-bet) - controller ni asinxron tabiati tufayli debug qilish qiyinligi va breakpoint ning ishlamasligi, shundan kuzatuvchanlikni controller ga dastlabki versiyadan yozish talabi (29.19)
- Bilgin Ibryam, Roland Huss, *Kubernetes Patterns: Reusable Elements for Designing Cloud-Native Applications*, 1-nashr, O'Reilly, 2019, 23-bob (201-bet) - operator va CRD ni tanlashning to'rt sharti (asboblarga chuqur integratsiya, greenfield, resurs yo'li va versiyalashdan foyda, tayyor client qo'llovi) hamda rad etish yo'llari: standart resurs bilan Controller, va deklarativ bo'lmagan use case uchun mustaqil API (29.20)
- Bilgin Ibryam, Roland Huss, *Kubernetes Patterns: Reusable Elements for Designing Cloud-Native Applications*, 1-nashr, O'Reilly, 2019, 24-bob (206 va 218-219-betlar) - HPA ning ikki sharti (CPU uchun `resources.requests` va metrics server), masshtablashning to'rt bosqichi shu tartibda (ilova, VPA, HPA, Cluster Autoscaler) va birinchi ikkisining uzilish berishi, VPA uchun pod ning qayta yaratilishi va joylashtirilmaydigan holatga tushish xavfi, antifragillik tushunchasi (29.13)
- Bilgin Ibryam, Roland Huss, *Kubernetes Patterns: Reusable Elements for Designing Cloud-Native Applications*, 1-nashr, O'Reilly, 2019, 25-bob (222-bet) - image ni klaster ichida qurishning asosiy foydasi: build va deploy ni bitta tizim bilganda bazaviy image dagi zaiflik tuzatilganda hamma ilova image i qayta qurilib avtomatik qayta joylashtirilishi (29.14)
- Bilgin Ibryam, Roland Huss, *Kubernetes Patterns: Reusable Elements for Designing Cloud-Native Applications*, 1-nashr, O'Reilly, 2019, 11-bob (91-bet) - StatefulSet PersistentVolume ni boshqarmasligi, skale kamayganda pod o'chib PVC va PV ning ataylab qolishi va diskni bo'shatish uchun PVC ni qo'lda o'chirish qadami (29.13)
- ESLATMA: `k8s-patterns` ning 1-nashri 2019-yilda chiqqan va undagi `apiVersion` qiymatlarining ko'pi hozirgi Kubernetes da yo'q, shuning uchun bu bobga kitobdan faqat tamoyil va mexanizm olingan, `apiVersion` ko'chirilmagan. Kitob VPA resurs o'zgarishi uchun pod ni qayta yaratish kerakligini 2019-yil holatiga ko'ra aytadi; mexanizmning keyingi versiyalardagi holati korpusda tekshirilmagan
- ESLATMA: 29.26 dagi Spring tomoni (Downward API bilan `nodeName` va zone ni Micrometer tag qilish, qattiq joylashuv cheklovlarining HPA va probe bilan o'zaro ta'siri) hamda 29.4, 29.17 va 29.22 dagi Spring kalitlari shu korpusning amaliy qo'shimchasi, Ibryam va Huss Spring nomidan gapirmaydi
- Sam Newman, *Building Microservices: Designing Fine-Grained Systems*, 2-nashr, O'Reilly, 2021, 8-bob, "Multitenancy and Federation" bo'limi - bitta klasterni ko'p bo'lim bilan bo'lishish cheklovi, OpenShift kabi platforma va federatsiya yo'llari, federatsiyada node ni klasterlar orasida ko'chirish qiyinligi. Bu nashrning qo'limizdagi elektron nusxasida barqaror bet raqami yo'q, shuning uchun faqat bob va bo'lim nomi ko'rsatilgan (29.25)

---

[&larr; 28. Taqsimlangan ma'lumot, replikatsiya va konsistentlik patternlari](28-taqsimlangan-malumot-replikatsiya-va.md) · [Mundarija](README.md) · [30. Spring AI va LLM integratsiya patternlari &rarr;](30-spring-ai-va-llm-integratsiya-patternlari.md)
