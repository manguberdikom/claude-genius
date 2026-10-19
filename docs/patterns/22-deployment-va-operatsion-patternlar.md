<!-- doc: patterns | chapter: 22 | part:  -->

[Barcha hujjatlar](../../README.md) / [Dizayn patternlar](README.md)

> Holat: tekshirilgan (2026-10-19). Manbalar bob oxirida.

# 22. Deployment va operatsion patternlar (Deployment & Operations Patterns)

<details>
<summary>Bu bobdagi 47 bo'lim</summary>

- [22.1 O'n ikki faktorli ilova (Twelve-Factor App)](#221-on-ikki-faktorli-ilova-twelve-factor-app)
- [22.2 Tashqi konfiguratsiya (Externalized Configuration)](#222-tashqi-konfiguratsiya-externalized-configuration)
- [22.3 O'zgarmas infratuzilma (Immutable Infrastructure)](#223-ozgarmas-infratuzilma-immutable-infrastructure)
- [22.4 Infratuzilma kod sifatida (Infrastructure as Code)](#224-infratuzilma-kod-sifatida-infrastructure-as-code)
- [22.5 GitOps (GitOps)](#225-gitops-gitops)
- [22.6 Ko'k-yashil joylashtirish (Blue-Green Deployment)](#226-kok-yashil-joylashtirish-blue-green-deployment)
- [22.7 Kanareyka relizi (Canary Release)](#227-kanareyka-relizi-canary-release)
- [22.8 Bosqichma-bosqich yangilash (Rolling Update)](#228-bosqichma-bosqich-yangilash-rolling-update)
- [22.9 Qayta yaratish usuli bilan joylashtirish (Recreate Deployment)](#229-qayta-yaratish-usuli-bilan-joylashtirish-recreate-deployment)
- [22.10 Funksiya kalitlari (Feature Toggle / Feature Flags)](#2210-funksiya-kalitlari-feature-toggle--feature-flags)
- [22.11 Yashirin ishga tushirish (Dark Launch)](#2211-yashirin-ishga-tushirish-dark-launch)
- [22.12 Soya trafik (Shadow Traffic)](#2212-soya-trafik-shadow-traffic)
- [22.13 A/B Testlash (A/B Testing)](#2213-ab-testlash-ab-testing)
- [22.14 Rollback strategiyasi (Rollback Strategy)](#2214-rollback-strategiyasi-rollback-strategy)
- [22.15 Sidecar konteyner (Sidecar Container)](#2215-sidecar-konteyner-sidecar-container)
- [22.16 Ambassador konteyner (Ambassador Container)](#2216-ambassador-konteyner-ambassador-container)
- [22.17 Adapter konteyner (Adapter Container)](#2217-adapter-konteyner-adapter-container)
- [22.18 Init konteyner (Init Container)](#2218-init-konteyner-init-container)
- [22.19 Health probe'lar (Health Probes: Liveness, Readiness, Startup)](#2219-health-probelar-health-probes-liveness-readiness-startup)
- [22.20 Nazorat ostida to'xtatish (Graceful Shutdown)](#2220-nazorat-ostida-toxtatish-graceful-shutdown)
- [22.21 Gorizontal / vertikal avtomatik masshtablash (Horizontal / Vertical Autoscaling)](#2221-gorizontal--vertikal-avtomatik-masshtablash-horizontal--vertical-autoscaling)
- [22.22 Bitta hostda bir nechta service instance (Multiple Service Instances per Host)](#2222-bitta-hostda-bir-nechta-service-instance-multiple-service-instances-per-host)
- [22.23 Har bir service instance alohida host / VM / konteynerda (Service Instance per Host / VM / Container)](#2223-har-bir-service-instance-alohida-host--vm--konteynerda-service-instance-per-host--vm--container)
- [22.24 Serverless deployment (Serverless Deployment)](#2224-serverless-deployment-serverless-deployment)
- [22.25 Servis deploy platformasi (Service Deployment Platform - Kubernetes, PaaS)](#2225-servis-deploy-platformasi-service-deployment-platform---kubernetes-paas)
- [22.26 Container image qurish (Container Image Build - Buildpacks, Jib, layered jar, multi-stage)](#2226-container-image-qurish-container-image-build---buildpacks-jib-layered-jar-multi-stage)
- [22.27 GraalVM Native Image (GraalVM Native Image)](#2227-graalvm-native-image-graalvm-native-image)
- [22.28 Sinflar arxivi va AOT cache (CDS / AppCDS / Project Leyden)](#2228-sinflar-arxivi-va-aot-cache-cds--appcds--project-leyden)
- [22.29 JVM'ning container ergonomikasi (JVM Container Ergonomics)](#2229-jvmning-container-ergonomikasi-jvm-container-ergonomics)
- [22.30 Nol to'xtalishli deploy (Zero-Downtime Deployment)](#2230-nol-toxtalishli-deploy-zero-downtime-deployment)
- [22.31 Trunk-based development va reliz poyezdlari (Trunk-Based Development & Release Trains)](#2231-trunk-based-development-va-reliz-poyezdlari-trunk-based-development--release-trains)
- [22.32 Semantik versiyalash va BOM bilan dependency boshqarish (Semantic Versioning & BOM Dependency Management)](#2232-semantik-versiyalash-va-bom-bilan-dependency-boshqarish-semantic-versioning--bom-dependency-management)
- [22.33 Runbook'lar (Runbooks)](#2233-runbooklar-runbooks)
- [22.34 Muhitlar o'zarosi mosligi (Environment Parity)](#2234-muhitlar-ozarosi-mosligi-environment-parity)
- [22.35 Secrets manager integratsiyasi (Secrets Manager Integration)](#2235-secrets-manager-integratsiyasi-secrets-manager-integration)
- [22.36 Hisoblash resurslarini konsolidatsiya qilish (Compute Resource Consolidation)](#2236-hisoblash-resurslarini-konsolidatsiya-qilish-compute-resource-consolidation)
- [22.37 Har bir servis nusxasi uchun alohida container (Service Instance per Container)](#2237-har-bir-servis-nusxasi-uchun-alohida-container-service-instance-per-container)
- [22.38 Replikatsiyalangan yuk-balanslangan servis (Replicated Load-Balanced Service)](#2238-replikatsiyalangan-yuk-balanslangan-servis-replicated-load-balanced-service)
- [22.39 Shardlangan servis (Sharded Service)](#2239-shardlangan-servis-sharded-service)
- [22.40 Ish navbati tizimi (Work Queue System)](#2240-ish-navbati-tizimi-work-queue-system)
- [22.41 Hodisaga asoslangan batch ishlov (Event-Driven Batch Processing)](#2241-hodisaga-asoslangan-batch-ishlov-event-driven-batch-processing)
- [22.42 Muvofiqlashtirilgan batch ishlov (Coordinated Batch Processing: Join, Reduce)](#2242-muvofiqlashtirilgan-batch-ishlov-coordinated-batch-processing-join-reduce)
- [22.43 Har mikroservisga bitta repozitoriya (One Repository per Microservice, Multirepo)](#2243-har-mikroservisga-bitta-repozitoriya-one-repository-per-microservice-multirepo)
- [22.44 Konteyner shartnomasi: parametr, API va hujjat (Container Contract: Parameters, API, Documentation)](#2244-konteyner-shartnomasi-parametr-api-va-hujjat-container-contract-parameters-api-documentation)
- [22.45 Avtomatik masshtablash qoidalarini qurish (Autoscaling Policy Design)](#2245-avtomatik-masshtablash-qoidalarini-qurish-autoscaling-policy-design)
- [22.46 Deploy infratuzilmasining xavfsizlik gigiyenasi (Patching and Rebuild Hygiene)](#2246-deploy-infratuzilmasining-xavfsizlik-gigiyenasi-patching-and-rebuild-hygiene)
- [22.47 Amalda qo'llash](#2247-amalda-qollash)

</details>



Deployment va operatsion patternlar - bu kod yozilib bo'lgandan keyin boshlanadigan, lekin arxitektura qarorlariga eng kuchli ta'sir qiladigan qatlam: ilova qanday paketlanadi, konfiguratsiya qayerdan keladi, yangi versiya ishlab chiqarish muhitiga qanday chiqadi va noto'g'ri ketganda qanday orqaga qaytariladi. Spring Boot ilovasini "ishlaydigan" qilish oson, ammo uni kuniga o'n marta, tushkunliksiz (zero-downtime) va xavfsiz tarzda relizga chiqarish mumkin bo'ladigan qilib loyihalash - bu allaqachon arxitektorning vazifasi. Bu kategoriyadagi patternlar deploy jarayonini kod bilan bir qatorda versiyalanadigan, takrorlanadigan va qaytarib olinadigan muhandislik artefaktiga aylantiradi. Shu bilan birga ular arxitekturaga qattiq talablar qo'yadi: statelessness, backward-compatible ma'lumotlar bazasi migratsiyalari, kuzatuvchanlik (observability) va konfiguratsiyaning artefaktdan to'liq ajratilishi.

## 22.1 O'n ikki faktorli ilova (Twelve-Factor App)

**Tavsif:** Heroku tomonidan shakllantirilgan va bugun cloud-native standartga aylangan 12 ta tamoyil to'plami: bitta kod bazasi, aniq deklarativ bog'liqliklar, muhitdan keladigan konfiguratsiya, backing service'larni almashtiriladigan resurs sifatida ko'rish, build/release/run bosqichlarining qat'iy ajratilishi, stateless process'lar, port binding, gorizontal masshtablash, tez ishga tushish va graceful shutdown, dev/prod paritet, log'larni event stream sifatida stdout'ga yozish va admin vazifalarini bir martalik process sifatida bajarish. Muammosi - an'anaviy "application server'ga WAR tashlash" modeli konteyner va orkestratorlarda qayta-qayta buziladi; 12-faktor shu modelni almashtiradi. Natijada ilova o'zini qayerda ishlayotganini bilmaydigan, almashtiriladigan birlikka aylanadi.

**Spring'da qayerda uchraydi:** Spring Boot 3.x/4.x bu tamoyillarni deyarli standart holatda beradi: embedded Tomcat/Netty orqali port binding, `Environment` + `@ConfigurationProperties` orqali tashqi konfiguratsiya (diqqat: repo ichidagi `application.yml` ning o'zi 12-faktorning III bandiga to'liq javob bermaydi - u konfiguratsiyani environment variable'da saqlashni talab qiladi va versiya nazoratiga tushmaydigan config faylini ham "zaifliklari bor" deb ataydi; shuning uchun muhitga xos qiymatlar `SPRING_DATASOURCE_URL` kabi o'zgaruvchilar yoki ConfigMap/Secret orqali kelsin, `application.yml` esa faqat defaultlarni ushlab tursin), Maven/Gradle `spring-boot-starter-*` orqali deklarativ bog'liqliklar. `spring-boot-starter-actuator` build/release ajratilishini `/actuator/info` (git/build ma'lumotlari `BuildProperties`, `GitProperties`) va Kubernetes probe'lari (`management.endpoint.health.probes.enabled=true`, `/actuator/health/liveness`, `/actuator/health/readiness`) bilan qo'llab-quvvatlaydi. Graceful shutdown uchun `server.shutdown=graceful` va `spring.lifecycle.timeout-per-shutdown-phase`; stateless process uchun session'ni Redis'ga chiqarish - `spring-session-data-redis`; log'lar Logback'ning `ConsoleAppender` orqali stdout'ga; admin process'lar `ApplicationRunner`/`CommandLineRunner` yoki Spring Batch job'lari sifatida. Dev/prod paritetini Testcontainers (`spring-boot-testcontainers`, `@ServiceConnection`) ta'minlaydi, build/run ajratilishini esa `spring-boot-maven-plugin:build-image` (Cloud Native Buildpacks).

**Qo'llanish keyslari:**
- Kubernetes'da ishlaydigan har qanday yangi Spring Boot microservice uchun bazaviy talablar ro'yxati sifatida.
- Monolitni konteynerlashtirishdan oldin "nimani tuzatish kerak" auditining chek-listi sifatida (local fayl yozish, in-memory session, hardcode qilingan URL'lar).
- Autoscaling (HPA) joriy qilishdan oldin pod'larning haqiqatan stateless ekanini tekshirishda.
- CI/CD quvuri bitta artefaktni barcha muhitlarga chiqarishi kerak bo'lgan reliz modelini asoslashda.
- Platform team uchun "golden path" service template'ini loyihalashda.

**Ehtiyot bo'ling:** 12-faktor stateless web service'lar uchun yozilgan - stateful tizimlar (Kafka Streams state store, Spring Batch partition'lari, legacy ETL) uchun uni so'zma-so'z qo'llash sun'iy murakkablik keltiradi. Eng ko'p buziladigan faktor - konfiguratsiya: profil ichiga yozilgan prod parollari yoki `application-prod.yml`ni jar ichida tashish allaqachon 12-faktorni buzadi.

## 22.2 Tashqi konfiguratsiya (Externalized Configuration)

**Tavsif:** [Microservices patternlari bobidagi tashqariga chiqarilgan konfiguratsiya yozuvi](14-microservices-patternlari.md#1430-tashqariga-chiqarilgan-konfiguratsiya-externalized-configuration) bu patternning to'liq yozuvi, bu yerda faqat deployment nuqtai nazari: bitta image o'zgartirilmasdan dev, staging va prod'ga chiqadi, konfiguratsiya esa muhit o'zgaruvchisi, mount qilingan ConfigMap/Secret fayli yoki Vault'dan keladi va asosiy qiyinlik ustuvorlik tartibi (precedence) hamda runtime'da qayta yuklash semantikasida.

**Spring'da qayerda uchraydi:** Kanonik yozuvdagidan tashqari Kubernetes Secret'ni fayl sifatida o'qiydigan `spring.config.import=configtree:/etc/secrets/`, API orqali o'qishdagi `ConfigMapPropertySource` va `SecretsPropertySource`, server tomonda `@EnableConfigServer`, relaxed binding'da `MY_APP_TIMEOUT` ning `my.app.timeout` ga tushishi va Spring Cloud AWS parameter store integratsiyasi.

**Qo'llanish keyslari:**
- Bitta Docker image'ni dev, staging va prod'ga bir xil digest bilan chiqarib, DB paroli va to'lov gateway kalitini Kubernetes Secret yoki Vault'dan olish.

**Xossa nomi administrator uchun interfeys.** Tashqariga chiqarilgan konfiguratsiyaning har bir kaliti ishlab chiqarishda tizimni yuritadigan odam uchun interfeys bo'lib qoladi, shuning uchun u kodning ichki tuzilishi emas, FUNKSIYA bo'yicha nomlanadi. `hostname` yoki `url2` kabi nom qiymatning tabiatini aytadi va nima uchun ishlatilayotganini aytmaydi; `authenticationServer` esa to'g'ridan-to'g'ri aytadi va incident paytida uni o'zgartirayotgan odam nima qilayotganini biladi. Bu clean-code dagi nomlash qoidalarining aynan o'zi, faqat identifikator emas, sozlama kaliti ustida qo'llanadi: `spring.datasource.url` kabi framework kalitlari tegilmaydi, lekin ilovaning o'z kalitlari (`app.partner.timeout` emas, `app.partner.priceFeedTimeout`) shu mezon bilan yoziladi.

**Ehtiyot bo'ling:** `@RefreshScope` bilan DataSource yoki `@Scheduled` holatini runtime'da almashtirish yarim-ishlaydigan holatga olib keladi, shubha bo'lsa pod qayta ishga tushiriladi, Config Server uzilishiga qarshi esa client'da `optional:` prefiksi yoki lokal fallback ongli tanlanadi.

## 22.3 O'zgarmas infratuzilma (Immutable Infrastructure)

**Tavsif:** Serverlar va konteynerlar ishga tushgandan keyin hech qachon o'zgartirilmaydi - har qanday yangilanish yangi image qurib, eski instance'ni butunlay almashtirish orqali amalga oshiriladi. Bu "configuration drift" muammosini (har bir server vaqt o'tib o'ziga xos, takrorlanmaydigan holatga kelishini) butunlay yo'q qiladi va orqaga qaytarishni oddiy "eski image digest'iga qaytish"ga aylantiradi. Deploy birligi - kod, JRE va OS kutubxonalari bilan birga muzlatilgan artefakt.

**Spring'da qayerda uchraydi:** Spring Boot'da artefakt - executable jar; undan OCI image qurish uchun `spring-boot-maven-plugin`ning `build-image` goal'i (Paketo/Cloud Native Buildpacks) yoki `jib-maven-plugin`. Layered jar (`spring-boot-jarmode-tools`, avvalgi `layertools`) image qatlamlarini bog'liqlik/ilova bo'yicha ajratib, qayta qurishni tezlashtiradi. Spring Boot 3.x/4.x AOT va GraalVM native image (`native-maven-plugin`, `-Pnative`) bilan yanada qattiqroq muzlatilgan, tez ishga tushadigan binary beradi - immutable modelga juda mos. Ishlash vaqtida mutatsiya qilmaslik uchun ilova lokal diskka yozmasligi, `java.io.tmpdir`dan tashqari holatni saqlamasligi va read-only root filesystem'da ishlashi loyihalanadi; Kubernetes'da image `sha256` digest bo'yicha pin qilinadi.

**Qo'llanish keyslari:**
- Har bir commit uchun o'zgarmas image qurib, uni dev→prod bo'ylab bir xil digest bilan ko'chirish.
- Xavfsizlik patch'ini SSH bilan emas, yangi base image qurib butun flot'ni almashtirish orqali yopish.
- Incident paytida orqaga qaytishni bir buyruqqa (`kubectl rollout undo`) keltirish.
- Compliance auditida "prod'da qanday aniq artefakt ishlayapti" savoliga digest bilan javob berish.
- Native image bilan sovuq ishga tushish vaqtini qisqartirib, serverless/scale-to-zero ssenariylarini qo'llab-quvvatlash.

**Ehtiyot bo'ling:** `latest` tegidan foydalanish immutable modelni butunlay buzadi - bir xil teg turli vaqtda turli image'ni bildiradi, shu bilan rollback ham ishonchsiz bo'ladi. Shuningdek, ishlash vaqtida pod ichiga `exec` bilan kirib fayl tuzatish yoki konfiguratsiyani qo'lda o'zgartirish - keyingi deploy'da "sirli regressiya" sifatida qaytadi.

**Phoenix server: serverni ataylab o'ldirib qayta tiklash:** o'zgarmaslik faqat qog'ozda qolmasligi uchun serverni muntazam buzib, machine image dan qayta yaratish kerak. Carnell bu amaliyotni Martin Fowler ning "Phoenix Server" nomi bilan beradi: eski server o'ldirilganda yangisi uning kulidan ko'tariladi, shu sababli server qancha uzoq ishlab turgan bo'lsa, drift ehtimoli shuncha katta (Carnell, 1-bob, 25-bet; 10-bob, 308-bet). Patternning ikki foydasi bor va ikkisi ham tekshiruv:

- **Drift ni ochadi va muhitdan quvib chiqaradi.** Doimiy buzib qayta ko'tarsangiz, konfiguratsiya farqi erta chiqadi. Bu izchillikni ta'minlashning eng kuchli yo'li va "stage da bitta kichik o'zgarish qildim, prod da qilishni esimdan chiqardim" turidagi incident manbasini yopadi.
- **Tiklanmaydigan holatni fosh qiladi.** Mikroservis stateless bo'lishi va serverning o'limi kichik uzilish bo'lishi kerak. Tasodifiy o'ldirib qayta ko'tarish servisda yoki infratuzilmada holat qolib ketgan va bog'liqlik yashiringan joylarni tez ko'rsatadi; bunday joylarni g'azablangan mijoz bilan telefonda gaplashayotganda emas, deploy pipeline ining o'zida topish arzonroq.

Carnell buni Netflix Chaos Monkey bilan tekshiradi: u muhitdagi server nusxalarini tasodifiy tanlab o'ldiradi, maqsad esa serverni yo'qotganda tiklanmaydigan servisni va yangi server eskisi kabi ishlamaydigan holatni topish (Carnell, 10-bob, 308-bet). Umumiy intizom shaklida bu [chaos engineering](17-resilience-va-cloud-dizayn-patternlari.md#1738-chaos-engineering-chaos-engineering) bo'limida yozilgan.

ESLATMA: kitob 2017 yilgi kontekstda virtual server image lari haqida gapiradi (CI da baked machine image, keyin yangi server deploy). Kubernetes da shu patternning amaliy shakli boshqa nomlar bilan keladi: pod ni qo'lda o'chirish o'rniga `kubectl rollout restart`, tasodifiy o'chirishni `PodDisruptionBudget` bilan chegaralash va chaos uchun Chaos Mesh yoki LitmusChaos.

## 22.4 Infratuzilma kod sifatida (Infrastructure as Code)

**Tavsif:** Serverlar, tarmoq, ma'lumotlar bazalari, Kubernetes resurslari va boshqa infratuzilma deklarativ, versiyalanadigan matn fayllari orqali tavsiflanadi va avtomatik tarzda qo'llanadi. Bu qo'lda konsol orqali qilingan, hujjatlanmagan o'zgarishlarni yo'q qiladi, muhitlarni bir xil shablon bilan qayta yaratish imkonini beradi va infratuzilma o'zgarishiga ham code review, PR va audit tarixini keltiradi. Odatda `plan`/`diff` bosqichi bilan niyat va haqiqiy holat o'rtasidagi farq avval ko'rsatiladi.

**Spring'da qayerda uchraydi:** Spring ilovasi uchun IaC asosan atrofdagi qatlamda yashaydi: Terraform/Pulumi/AWS CDK bilan RDS, Kafka, S3 va IAM; Helm chart yoki Kustomize overlay'lari bilan `Deployment`, `Service`, `HPA`, `ConfigMap`, `Secret`. Ilova tomonida IaC bilan juftlashadigan narsalar - ma'lumotlar bazasi sxemasini kod sifatida boshqaradigan Flyway (`spring.flyway.*`, `db/migration/V1__init.sql`) yoki Liquibase (`spring.liquibase.change-log`), hamda `spring.jpa.hibernate.ddl-auto=none` bilan avtomatik sxema o'zgarishini o'chirish. Lokal va test muhitida bir xil infratuzilmani deklarativ olish uchun Testcontainers va Spring Boot 3.1+ `@ServiceConnection`, `docker-compose.yaml` bilan esa `spring-boot-docker-compose` moduli.

**Qo'llanish keyslari:**
- Yangi mijoz yoki region uchun to'liq muhitni (DB, broker, service'lar) bir buyruq bilan yaratish.
- Prod va staging o'rtasidagi "nega faqat prod'da sinadi" farqlarini bir xil modul va turli `tfvars` bilan yo'q qilish.
- DB sxemasi o'zgarishini Flyway migratsiyasi sifatida kod bilan birga review qilish.
- Disaster recovery mashqida butun stack'ni boshqa regionda qayta tiklash.
- Xavfsizlik guruhlari va IAM siyosatlarini PR orqali o'zgartirib, audit izini saqlash.

**Ehtiyot bo'ling:** Eng xatarli nuqta - state fayli va qo'lda qilingan o'zgarishlar (drift): konsolda "tezda" tuzatilgan narsa keyingi `apply`da yo'qoladi yoki, undan yomoni, prod resursni o'chirib yuboradi. Ikkinchi tuzoq - maxfiy ma'lumotlarni IaC repository'siga ochiq yozish; ular Vault, SOPS yoki External Secrets orqali boshqarilishi kerak.

## 22.5 GitOps (GitOps)

**Tavsif:** Git repository ishlab chiqarish muhitining yagona haqiqat manbasi (single source of truth) bo'ladi, klasterdagi operator esa repozitoriydagi deklarativ holatni doimiy kuzatib, real holatni unga moslashtiradi (reconciliation loop). Deploy "push" emas, "pull" modeliga o'tadi: CI faqat image qurib teg/digest'ni repository'ga yozadi, qolganini operator bajaradi. Buning natijasi - har bir o'zgarish uchun commit, review va avtomatik drift tuzatish; rollback esa oddiy `git revert`.

**Spring'da qayerda uchraydi:** Spring Boot service'lari uchun Argo CD yoki Flux `Application`/`Kustomization` resurslari orqali Helm chart yoki Kustomize overlay'ini kuzatadi; CI quvuri `spring-boot-maven-plugin:build-image` bilan image qurib, uning digest'ini `values.yaml`ga commit qiladi. Muhitlar farqi overlay'lardagi `SPRING_PROFILES_ACTIVE` va ConfigMap'lar bilan ifodalanadi, maxfiy ma'lumotlar Sealed Secrets yoki External Secrets Operator orqali Vault'dan keladi (shunda Git'da shifrlangan ko'rinish turadi). Reliz sog'lig'ini Argo CD `/actuator/health/readiness` probe'lari va Micrometer/Prometheus metrikalari orqali baholaydi; progressiv deploy uchun Argo Rollouts yoki Flagger bilan birga ishlatiladi.

**Qo'llanish keyslari:**
- O'nlab microservice'ning prod holatini bitta "environment repo"da kuzatish va review qilish.
- Incident'dan keyin `git revert` bilan butun muhitni oldingi tasdiqlangan holatga qaytarish.
- Klasterga to'g'ridan-to'g'ri `kubectl apply` huquqlarini olib tashlab, barcha o'zgarishni PR orqali o'tkazish.
- Yangi klasterni (DR yoki yangi region) repozitoriydan "sync" qilib tiklash.
- Auditorga "kim, qachon, nimani prod'ga chiqardi" savoliga Git tarixi bilan javob berish.

**Ehtiyot bo'ling:** Git'ni haqiqat manbasi deb e'lon qilib, bir vaqtning o'zida qo'lda `kubectl edit` qilishga ruxsat berish - eng ko'p uchraydigan xato; operator o'zgarishni jimgina qaytaradi va jamoa "deploy ishlamayapti" deb o'ylaydi. Maxfiy ma'lumotlar strategiyasi (shifrlash yoki tashqi secrets manager) GitOps'ni joriy qilishdan oldin hal qilinishi shart.

## 22.6 Ko'k-yashil joylashtirish (Blue-Green Deployment)

**Tavsif:** Ishlab chiqarishda bir vaqtda ikki to'liq muhit saqlanadi: trafik qabul qilayotgan "blue" va yangi versiya o'rnatilgan, lekin hali trafik olmaydigan "green". Yangi versiya green'da tekshirilgandan so'ng trafik bir qadamda green'ga o'tkaziladi; muammo chiqsa, xuddi shunday tez blue'ga qaytariladi. Bu zero-downtime reliz va juda tez rollback beradi, lekin ikki barobar resurs va umumiy ma'lumotlar bazasi bilan ehtiyotkor ishlashni talab qiladi.

**Spring'da qayerda uchraydi:** Kubernetes'da ikki `Deployment` (`version: blue` / `version: green`) va `Service` selector'ini yoki Ingress/Gateway route'ini almashtirish bilan amalga oshiriladi; Argo Rollouts `blueGreen` strategiyasi `activeService`/`previewService` juftligini boshqaradi. Spring tomonida kalit nuqtalar: `spring-boot-starter-actuator` readiness probe'i (`/actuator/health/readiness`) green to'liq isishini (connection pool, cache warm-up) kafolatlaydi; `server.shutdown=graceful` eski instance'lar in-flight so'rovlarni tugatishiga imkon beradi. Umumiy DB uchun Flyway migratsiyalari ikki versiya bilan ham mos (expand/contract: avval ustun qo'shish, keyin eski ustunni olib tashlash) bo'lishi, `spring.jpa.hibernate.ddl-auto=none` bo'lishi va session Redis'da (`spring-session-data-redis`) saqlanishi loyihalanadi.

**Qo'llanish keyslari:**
- Katta funksional reliz oldidan yangi versiyani prod konfiguratsiyasi bilan smoke-test qilish.
- Reglament oynasi yo'q, SLA qattiq bo'lgan to'lov yoki bank API'sini tushkunliksiz yangilash.
- Kutubxona yoki Java versiyasini (masalan Java 17 → 21) butun service uchun almashtirishda xavfni kamaytirish.
- Reliz kechasi rollback vaqtini daqiqalardan sekundlarga tushirish talab qilinganda.
- Yangi infratuzilma (yangi klaster, yangi ingress) ga ko'chishda eski muhitni zaxira sifatida ushlab turish.

**Reliz strategiyasi va deploy strategiyasining farqi.** Deployment resursining o'z strategiyalari (rolling update, recreate) to'liq avtomatik: ularni yoqib qo'ygandan keyin platforma hech kimdan so'ramasdan oxirigacha olib boradi. Blue-Green va [kanareyka](#227-kanareyka-relizi-canary-release) boshqa toifada: ular platformaning ichiga qurilgan emas va ularning kalit qadami - trafikni yangi versiyaga o'tkazish tetigi - inson qaroriga yoki inson yozgan avtomatik mezonga tayanadi. Shundan amaliy natija chiqadi: bu ikki strategiya uchun "kim va nimaga qarab o'tkazadi" degan savol oldindan javoblanadi va javob reliz tartibida yoziladi, aks holda green muhit haftalar davomida trafiksiz turib, faqat xarajat bo'lib qoladi.

**Ehtiyot bo'ling:** Ma'lumotlar bazasi odatda umumiy bo'ladi - orqaga mos bo'lmagan migratsiya rollback'ni imkonsiz qiladi va blue-green'ning asosiy afzalligini yo'q qiladi. Bir qadamda 100% trafik ko'chishi tufayli bu pattern progressiv "oz-ozdan sinab ko'rish" bermaydi: faqat performans regressiyasi real yuk ostida ko'rinadigan holatlarda canary bilan birga ishlatish to'g'riroq.

## 22.7 Kanareyka relizi (Canary Release)

**Tavsif:** Yangi versiya avval trafikning kichik ulushiga (masalan 1-5%) beriladi, metrikalar (xato darajasi, kechikish, biznes KPI) kuzatiladi va faqat sog'lom bo'lsa ulush bosqichma-bosqich 100%ga oshiriladi. Shu bilan nosozlikning ta'sir radiusi (blast radius) keskin kichraytiriladi va qaror gipotezaga emas, o'lchovga asoslanadi. Ulush yo'naltirish darajasida (weight), foydalanuvchi segmenti yoki header bo'yicha belgilanishi mumkin.

**Spring'da qayerda uchraydi:** Infratuzilma darajasida Istio `VirtualService` weight'lari, Argo Rollouts yoki Flagger avtomatik analiz bilan; ilova darajasida Spring Cloud Gateway'ning `Weight` route predicate'i (`predicates: - Weight=group1, 8`) ikki backend o'rtasida trafikni bo'lishi mumkin, Spring Cloud LoadBalancer esa instance metadata bo'yicha filtr qiluvchi `ServiceInstanceListSupplier` bilan sozlanadi. Qaror uchun kerakli signallarni Micrometer (`spring-boot-starter-actuator`, `micrometer-registry-prometheus`) beradi: `http.server.requests` metrikasiga `version` yoki `deployment` tegini qo'shish uchun `MeterFilter`/`ObservationFilter` ishlatiladi, tracing uchun Micrometer Tracing + OpenTelemetry. Yangi versiya qulashida eski instance'larni himoya qilish uchun Resilience4j circuit breaker (`spring-cloud-starter-circuitbreaker-resilience4j`).

**Qo'llanish keyslari:**
- Yangi tavsiya algoritmini avval 2% foydalanuvchiga ochib, konversiyani eski versiya bilan solishtirish.
- JVM yoki GC sozlamalari o'zgarishini real yuk ostida kichik ulushda tekshirish.
- Yuqori trafikli API'da yangi caching qatlamini bosqichma-bosqich joriy qilish.
- Ichki xodimlar yoki beta mijozlarni header bo'yicha canary'ga yo'naltirish.
- Avtomatik rollback siyosatini (xato darajasi 1%dan oshsa - qaytar) o'rnatish.

**Ehtiyot bo'ling:** Canary'ni versiyaga xos metrikalarsiz joriy qilish ma'nosiz - ikki versiya metrikalari bitta grafikda aralashsa, regressiya statistik ko'rinmaydi. Shuningdek, juda kichik trafik ulushi statistik ahamiyatsiz bo'lib, sizni noto'g'ri xotirjamlikka olib keladi; sticky routing bo'lmasa, bir foydalanuvchi ikki versiya o'rtasida sakrab, mos kelmaydigan UX yoki schema xatolarini ko'radi.

## 22.8 Bosqichma-bosqich yangilash (Rolling Update)

**Tavsif:** Eski versiya instance'lari birin-ketin, kichik to'plamlar bilan yangi versiyaga almashtiriladi; har bir yangi pod sog'lom deb tan olinganidan keyingina keyingisi almashtiriladi. Bu zero-downtime relizning eng arzon va eng ko'p ishlatiladigan shakli, chunki qo'shimcha to'liq muhit talab qilmaydi. Narxi - reliz davomida ikki versiya bir vaqtda ishlaydi, demak API va DB sxemasi ikki tomonga mos bo'lishi shart.

**Spring'da qayerda uchraydi:** Kubernetes `Deployment`ning standart `strategy.type: RollingUpdate` strategiyasi; `maxSurge` va `maxUnavailable` ikkisining ham default qiymati 25% (`maxUnavailable` foizdan pastga, `maxSurge` yuqoriga yumaloqlanadi, ikkisi bir vaqtda 0 bo'la olmaydi), `revisionHistoryLimit` default 10, `progressDeadlineSeconds` default 600, `minReadySeconds` default 0. Oxirgisiga alohida e'tibor bering: Kubernetes "available" ni "ready bo'lgandan keyin `minReadySeconds` o'tgan" deb hisoblaydi, ya'ni 0 da pod ready bo'lishi bilanoq available sanaladi va keyingi pod almashtirilishi boshlanadi - warm-up ni hisobga olish uchun bu qiymatni ataylab qo'yish kerak. uning to'g'ri ishlashi butunlay Spring Boot'ning probe'lariga bog'liq - `management.endpoint.health.probes.enabled=true` bilan `/actuator/health/liveness` va `/actuator/health/readiness`, Spring Boot `AvailabilityChangeEvent`/`ReadinessState` orqali ichki holatni e'lon qiladi. In-flight so'rovlar yo'qolmasligi uchun `server.shutdown=graceful` (Spring Boot 3.4 dan default allaqachon `GRACEFUL`, 3.3 va undan oldin `IMMEDIATE` edi - ya'ni bu kalit eski versiyada zarur, yangisida ortiqcha) + `spring.lifecycle.timeout-per-shutdown-phase` (default 30s) va `preStop` hook; foydalanuvchi sessiyasi pod'dan tashqarida - `spring-session-data-redis`. Sxema o'zgarishi Flyway bilan expand/contract tartibida chiqariladi, Kafka consumer'lar uchun esa yangi va eski deserializer mosligi (Avro/Protobuf schema evolution, `spring-kafka`) tekshiriladi.

**Qo'llanish keyslari:**
- Kuniga bir necha marta chiqadigan oddiy microservice relizlari uchun standart strategiya.
- Yuqori replica soni bilan ishlaydigan stateless REST API'ni tushkunliksiz yangilash.
- Faqat konfiguratsiya (ConfigMap) o'zgarganda pod'larni bosqichma-bosqich qayta ishga tushirish.
- Resurs cheklangan muhitda blue-green'ning ikki barobar xarajatidan qochish.
- Avtomatik `kubectl rollout undo` bilan tez qaytarish siyosatini o'rnatish.

**Ehtiyot bo'ling:** Readiness probe'ni liveness bilan bir xil qilib qo'yish yoki probe'ni warm-up tugashidan oldin "yashil" qilish - reliz paytida 5xx xatolarining asosiy sababi. Orqaga mos bo'lmagan DB migratsiyasi yoki API shartnomasi bilan rolling update ishlamaydi: reliz oynasida ikki versiya bir vaqtda jonli, shuning uchun har bir o'zgarish N va N-1 versiyalar bilan mos bo'lishi kerak. Ikkinchi tez-tez uchraydigan xato - shutdown byudjetini qo'shmaslik: Kubernetes'ning `terminationGracePeriodSeconds` default qiymati 30s, Spring'ning `timeout-per-shutdown-phase` default qiymati ham 30s, `preStop` esa shu grace oynasi ICHIDA ishlaydi. Shu defaultlar bilan `preStop` ga sleep qo'shsangiz, drain tugamasdan SIGKILL keladi. Qoida: `terminationGracePeriodSeconds` > `preStop` davomiyligi + `timeout-per-shutdown-phase` + zaxira. Grace tugaganda `preStop` hali ishlayotgan bo'lsa kubelet faqat bir martalik 2 sekund qo'shadi, undan keyin SIGKILL.

## 22.9 Qayta yaratish usuli bilan joylashtirish (Recreate Deployment)

**Tavsif:** Eng sodda strategiya: barcha eski instance'lar to'xtatiladi, keyin yangi versiya ishga tushiriladi. Natijada qisqa, ongli ravishda qabul qilingan tushkunlik (downtime) oynasi paydo bo'ladi, buning o'rniga ikki versiya trafikni bir vaqtda qabul qilmaydi. "Hech qachon ikki versiya ishlamaydi" deb aytish aniq emas: Kubernetes yangi pod'larni eski pod'lar o'chirilishi tasdiqlanmaguncha yaratmaydi, lekin grace oynasi davomida eski pod `Terminating` holatda bo'lsa ham jarayon hali tirik - demak eksklyuziv resursga (singleton lock, migratsiya) tayangan ilovada o'chish faktini ilova ichida ham tekshirish kerak. Bu orqaga mos bo'lmagan ma'lumotlar bazasi migratsiyalari, yagona-faol (singleton) komponentlar va eski litsenziya cheklovlari bo'lgan holatlarda eng xavfsiz va eng tushunarli yo'l.

**Spring'da qayerda uchraydi:** Kubernetes'da `Deployment`ning `strategy.type: Recreate` ko'rinishida. StatefulSet'ni `replicas: 1` qilish Recreate EMAS - u `OrderedReady` yoki `RollingUpdate` bilan pod'ni o'rnini bosib yangilaydi; StatefulSet uchun haqiqiy `Recreate` strategiyasi alohida `StatefulSetRecreateStrategy` feature gate ostida turadi va faqat u yoqilganda barcha pod'lar yangilarini yaratishdan oldin o'chiriladi; Spring tomonida bu strategiya ko'pincha Flyway/Liquibase migratsiyasini `initContainer` yoki alohida Job sifatida bir marta bajarishga bog'lanadi (`spring.flyway.enabled=false` ilovada, migratsiya alohida qadamda). Yagona-faol komponentlar: Quartz'ni klaster rejimisiz ishlatuvchi `spring-boot-starter-quartz` scheduler'lari, `@Scheduled` job'lar, Spring Batch `JobLauncher`, `@KafkaListener` bilan bitta partition'ga bog'langan consumer'lar. Tushkunlik oynasini qisqartirish uchun tez ishga tushish muhim - Spring Boot 3.x AOT, GraalVM native image yoki lazy initialization (`spring.main.lazy-initialization=true`) yordam beradi.

**Qo'llanish keyslari:**
- Orqaga mos bo'lmagan DB sxemasi o'zgarishi (ustun turini o'zgartirish, jadvalni bo'lish) bilan chiqadigan reliz.
- Kechasi ishlaydigan ichki admin yoki hisobot ilovasini reglament oynasida yangilash.
- Bitta faol instance talab qiladigan Quartz scheduler yoki ETL koordinatori.
- Eski litsenziya yoki tashqi tizim bir vaqtda faqat bitta ulanishga ruxsat beradigan integratsiya.
- Dev/test muhitlarida eng sodda va eng arzon deploy usuli sifatida.

**Ehtiyot bo'ling:** Bu strategiyani "vaqtincha" deb mijozga qaraydigan yuqori SLA'li service'ga qo'llash sekin-asta normaga aylanadi va keyin undan chiqish qiyin bo'ladi. Tushkunlik oynasi ilovaning ishga tushish vaqti va migratsiya davomiyligiga teng - sekin start (katta context, eager cache warm-up) bu oynani bir necha daqiqaga cho'zishini oldindan o'lchab qo'ying.

## 22.10 Funksiya kalitlari (Feature Toggle / Feature Flags)

**Tavsif:** Yangi xatti-harakat kodga chiqariladi, lekin uni yoqish/o'chirish runtime'da, deploy'dan mustaqil tarzda boshqariladi. Shu bilan "deploy" va "release" ajratiladi: kod prod'da bo'lsa ham, funksiya o'chirilgan holatda turadi va kerakli vaqtda, kerakli segment uchun yoqiladi. Toggle'lar turi bo'yicha farqlanadi - reliz toggle'lari (qisqa muddatli), eksperiment (A/B), operatsion kill-switch va huquq (entitlement) toggle'lari; ularning yashash muddati va boshqaruvi ham turlicha bo'lishi kerak.

**Spring'da qayerda uchraydi:** Eng yengil variant - konfiguratsiyaga asoslangan `@ConditionalOnProperty` (bean darajasida, faqat ishga tushishda) yoki `@ConfigurationProperties` + `@RefreshScope` bilan dinamik qiymat. To'liq toggle boshqaruvi uchun Togglz: `togglz-spring-boot-starter`, `Feature` interfeysini implement qiladigan enum, `@EnabledByDefault`, `@Label`, `FeatureManager.isActive(...)`, `StateRepository` (masalan `JdbcStateRepository`) va `togglz-console` admin UI; Actuator uchun `/actuator/togglz` endpoint'i mavjud. Vendor-neutral yondashuv - OpenFeature Java SDK (`dev.openfeature:sdk`: `OpenFeatureAPI`, `Client`, `getBooleanValue(key, false)`, `EvaluationContext`) va uning provider'lari (flagd, Unleash, LaunchDarkly, GO Feature Flag); OpenFeature contrib'da Spring Boot starter ham bor. Muqobil - FF4j yoki Unleash'ning Spring client'i.

```java
public enum BillingFeature implements Feature {
    @Label("Yangi to'lov gateway'i")
    NEW_PAYMENT_GATEWAY;
    public boolean isActive() { return FeatureContext.getFeatureManager().isActive(this); }
}
// Servis ichida:
// if (BillingFeature.NEW_PAYMENT_GATEWAY.isActive()) { newGateway.charge(o); } else { legacy.charge(o); }
```

**Qo'llanish keyslari:**
- Yarim tugallangan funksiyani trunk-based development bilan har kuni prod'ga chiqarib, o'chirilgan holatda ushlab turish.
- Yangi to'lov provayderiga o'tishda kill-switch bilan bir sekundda eski yo'lga qaytish.
- Funksiyani avval ichki xodimlarga, keyin 10% mijozga, keyin barchaga ochish.
- A/B eksperimentda ikki UX variantini bir xil binary ichida sinash.
- Og'ir hisobot so'rovini incident paytida vaqtincha o'chirib, tizim yukini kamaytirish.

**Ehtiyot bo'ling:** Toggle'lar texnik qarz: olib tashlanmagan flag'lar kodda eksponensial kombinatsiyalar hosil qiladi va test qoplamasini buzadi - har bir reliz toggle'iga yaratilishida yashash muddati va o'chirish uchun mas'ul biriktirilsin. Shuningdek, flag'ni so'rov ichida bir marta hal qilib, keyin uzatish kerak: bitta so'rov oqimida bir nechta joyda qayta o'qilsa, qiymat o'rtada o'zgarib, mos kelmaydigan holat yuzaga keladi.

**Konfiguratsiya faylidan boshlang, keyin vositaga o'ting:** toggle
uchun to'liq boshqariladigan platforma (Newman LaunchDarkly va Split
ni nomlaydi) birinchi qadam emas. Newman ning tavsiyasi aniq: ancha
soddaroq narsa bilan, oddiy konfiguratsiya fayli bilan boshlash
mumkin, bu vositalarga esa toggle larni qanday ishlatishni
chuqurlashtirgandan keyin qarash kerak. Ya'ni tanlov ketma-ketligi
`@ConditionalOnProperty` va `application.yml` dan boshlanadi,
markaziy boshqaruvga ehtiyoj (audit, real vaqtda o'zgartirish, ko'p
muhit) paydo bo'lganda Togglz yoki OpenFeature ga o'tiladi.
Toggle ning ikkinchi qo'llanishi shu yerdan chiqadi: toggle qiymatini
so'rov qilayotgan foydalanuvchining xususiyatiga qarab boshqacha
qilish mumkin, masalan beta guruh funksiyani yoqilgan ko'radi,
qolganlar o'chirilgan ko'radi, va bu [kanareyka
rollout](#227-kanareyka-relizi-canary-release) ning
konfiguratsiya darajasidagi shakli.

## 22.11 Yashirin ishga tushirish (Dark Launch)

**Tavsif:** Yangi funksiya yoki yangi implementatsiya ishlab chiqarishda real trafik bilan ishlaydi, lekin natijasi foydalanuvchiga ko'rsatilmaydi - u faqat log, metrika yoki solishtirish uchun yoziladi. Maqsad - performans, xatolar va natija mosligini sun'iy yuk testlari emas, haqiqiy ma'lumotlar bilan tekshirish. Ko'pincha feature toggle bilan birga, "yoqilgan lekin ko'rinmas" rejimda qo'llanadi.

**Spring'da qayerda uchraydi:** Amalda yangi yo'l eski yo'l bilan parallel chaqiriladi: `@Async` (`ThreadPoolTaskExecutor`) yoki `ApplicationEventPublisher` + `@TransactionalEventListener(phase = AFTER_COMMIT)` orqali asosiy so'rov javobiga ta'sir qilmaydigan tarzda ishga tushiriladi, natijalar esa Micrometer `Counter`/`Timer` (`MeterRegistry`) va struktur log'lar bilan solishtiriladi. Yangi yo'lni izolyatsiya qilish uchun Resilience4j `@CircuitBreaker`, `@TimeLimiter` va `@Bulkhead` (`spring-cloud-starter-circuitbreaker-resilience4j`), yoqish/o'chirish uchun Togglz yoki OpenFeature client. Ikki implementatsiyani bitta interfeys ortida saqlash uchun oddiy Spring pattern: bir nechta `@Component` implementatsiya + `@Qualifier` yoki delegating bean, shu bilan toggle qiymatiga qarab yo'l tanlanadi.

**Qo'llanish keyslari:**
- Yangi search yoki ranking servisini real so'rovlar bilan ishlatib, natijalarini eski servis bilan solishtirish (diff rate o'lchash).
- Yangi narx hisoblash dvigatelini prod ma'lumotlarida sinab, farqlar 0.01%dan oshmasligini tasdiqlash.
- Yangi DB yoki read-replica'ga o'qish so'rovlarini parallel yuborib, kechikishni o'lchash.
- Og'ir yangi endpoint'ni real yuk ostida sinab, capacity planning uchun ma'lumot to'plash.
- Migratsiya oldidan yangi integratsiyaning rate limit va timeout xatti-harakatini o'rganish.

**Ehtiyot bo'ling:** Dark launch faqat yon ta'sirsiz (idempotent, read-only) yo'llar uchun xavfsiz - yangi kod e-mail yuborsa, to'lov yaratsa yoki jadvalga yozsa, foydalanuvchi "ko'rmasa" ham real zarar yetadi. Ikkinchi xavf - resurs: parallel chaqiruvlar CPU, connection pool va tashqi API kvotasini ikki barobar iste'mol qiladi, shuning uchun uni alohida thread pool va bulkhead bilan cheklang.

## 22.12 Soya trafik (Shadow Traffic)

**Tavsif:** Ishlab chiqarish so'rovlari nusxalanadi va yangi versiyaga (shadow) yuboriladi, ammo uning javobi tashlab yuboriladi - foydalanuvchi faqat asosiy (primary) versiyaning javobini oladi. Bu yangi versiyani nol foydalanuvchi xavfi bilan to'liq real trafik profili ostida sinashga imkon beradi: kechikish taqsimoti, xotira iste'moli, xato naqshlari va javob farqlari o'lchanadi. Dark launch'dan farqi - bu yerda nusxalash odatda tarmoq/proxy darajasida, butun so'rov oqimi uchun bajariladi.

**Spring'da qayerda uchraydi:** Asosiy mexanizm infratuzilmada: Istio `VirtualService`ning `mirror` va `mirrorPercentage` sozlamalari, Envoy `request_mirror_policies`, NGINX `mirror` direktivasi yoki GoReplay. Spring stack ichida nusxalashni Spring Cloud Gateway uchun maxsus `GlobalFilter`/`GatewayFilter` yozib, so'rov tanasini cache qilib (`ServerWebExchangeUtils.CACHED_REQUEST_BODY_ATTR`, `cacheRequestBody` filtri) `WebClient` bilan shadow endpoint'ga asinxron yuborish orqali amalga oshirish mumkin; MVC stack'da esa `OncePerRequestFilter` + `ContentCachingRequestWrapper` va `RestClient`/`WebClient` bilan. Shadow tomonda ilova alohida profil bilan ishga tushiriladi (`SPRING_PROFILES_ACTIVE=shadow`), yozish operatsiyalari o'chiriladi yoki alohida DB'ga yo'naltiriladi; solishtirish Micrometer metrikalari va `Observation` tag'lari bo'yicha qilinadi.

**Qo'llanish keyslari:**
- Monolitdan ajratilgan yangi microservice'ni real trafik bilan sinab, javoblarini monolit javoblari bilan solishtirish.
- Java yoki framework versiyasini (masalan Spring Boot 3 → 4) ko'tarishdan oldin GC va kechikish regressiyasini aniqlash.
- Yangi caching yoki query optimizatsiyasini prod so'rov naqshlari ostida tekshirish.
- Capacity planning uchun yangi versiyaning CPU/xotira profilini real yuk bilan o'lchash.
- Migratsiya oldidan yangi DB engine'ida real so'rovlarni ijro etib, sekin query'larni topish.

**Ehtiyot bo'ling:** Eng katta tuzoq - shadow versiyaning yon ta'sirlari: u bir xil ma'lumotlar bazasiga yozsa, Kafka'ga event chiqarsa yoki tashqi to'lov/SMS API'siga murojaat qilsa, "sinov" real dublikat operatsiyalarga aylanadi; shadow uchun yozishni butunlay to'sish yoki izolyatsiya qilingan backing service'lar talab qilinadi. Shuningdek, nusxalangan trafik PII'ni yangi muhitga ko'chiradi (GDPR/maxfiylik masalasi) va downstream xizmatlarga ikki barobar yuk beradi - `mirrorPercentage` bilan cheklash va asosiy so'rov yo'lida bloklanmaslikni (fire-and-forget) kafolatlash kerak.

## 22.13 A/B Testlash (A/B Testing)

**Tavsif:** Foydalanuvchilar trafigini ikki yoki undan ko'p variantga (A - nazorat, B - yangi variant) bo'lib, biznes metrikalar asosida qaysi variant yaxshiroq ishlayotganini statistik o'lchash patterni. Canary release'dan farqi shundaki, maqsad texnik barqarorlikni emas, balki mahsulot gipotezasini tekshirishdir. Foydalanuvchi segmentatsiyasi odatda barqaror hash (user ID, session ID) orqali amalga oshiriladi, shunda bitta foydalanuvchi har doim bitta variantda qoladi. Natijalar yetarli statistik ishonchga yetgach, g'olib variant 100% trafikka chiqariladi.

**Spring'da qayerda uchraydi:** Spring Cloud Gateway'da `RoutePredicateFactory` (masalan `WeightRoutePredicateFactory` - `weight=group1, 8` sintaksisi) yoki custom `GatewayFilter` orqali header/cookie asosida routing qilinadi. Feature flag kutubxonalari: Togglz (`spring-boot-starter-togglz`), FF4j, Unleash'ning Java SDK'si yoki OpenFeature Java SDK bilan `@Bean FeatureProvider`. Kubernetes muhitida Istio `VirtualService` weight'lari yoki Argo Rollouts `AnalysisTemplate` bilan birgalikda ishlatiladi. Metrikalarni yig'ish uchun Micrometer `MeterRegistry` bilan variant tag'ini (`Tags.of("variant", "B")`) `Counter`/`Timer`'ga qo'shish standart yondashuv.

**Qo'llanish keyslari:**
- E-commerce'da checkout oqimining ikki dizaynini solishtirib, konversiya foizini o'lchash.
- Yangi tavsiya (recommendation) algoritmini eski collaborative filtering bilan taqqoslash.
- Search ranking formulasining o'zgarishini click-through rate bo'yicha baholash.
- Narx siyosati yoki obuna paketlari ko'rinishining daromadga ta'sirini sinash.
- Push-notification matnining ikki variantini ochilish foizi bo'yicha tekshirish.

**Tajribani qayerga joylashtirish: ambassador yoki alohida servis.** Variantga yo'naltirish mantiqini ikki joyga qo'yish mumkin va tanlov tajribaning umriga bog'liq. Birinchi yo'l - klient yonidagi ambassador konteyner: yo'naltirish pod ichida bajariladi, hech qanday yangi deploy birligi paydo bo'lmaydi va tajriba tugaganda ambassador olib tashlanadi. Ikkinchi yo'l - klient oldidagi alohida servis: u markazlashgan va bir nechta iste'molchi uchun bir xil qaror beradi, lekin o'z saqlanishi, masshtablanishi va monitoringini talab qiladi. Ajratuvchi shart aniq: tajriba doimiy mexanizm bo'lsa (platformada har vaqt A/B oqimi bor) alohida servis o'zini oqlaydi, kamdan-kam o'tkazilsa ambassador arzonroq va tezroq olib tashlanadi.

**Ehtiyot bo'ling:** Statistik ahamiyatga yetmasdan xulosa chiqarish (peeking problem) va bir vaqtda juda ko'p test o'tkazish natijalarni buzadi; shuningdek foydalanuvchini variantga bog'lashda sticky assignment bo'lmasa, bitta sessiya ichida UI o'zgarib ketib, tajriba ham, ma'lumot ham ifloslanadi. A/B testing to'lov, hisob-kitob yoki huquqiy jihatdan muhim oqimlarda ehtiyotkorlik talab qiladi - ba'zi yurisdiksiyalarda narx diskriminatsiyasi sifatida qaralishi mumkin.

## 22.14 Rollback strategiyasi (Rollback Strategy)

**Tavsif:** Deploy muvaffaqiyatsiz bo'lganda tizimni oldingi ishlaydigan holatiga tez va aniqlangan tartibda qaytarish patterni. U faqat artifact (JAR, image) versiyasini qaytarish bilan cheklanmaydi: database migration, cache, message format va feature flag holati ham qaytarilishi yoki orqaga moslashuvchan (backward compatible) bo'lishi kerak. Eng amaliy yondashuv - "rollback" o'rniga "roll forward"ga tayyor turish va har bir o'zgarishni ortga qaytarib bo'ladigan qilib loyihalash. MTTR (mean time to recovery) ni qisqartirish uchun rollback avtomatlashtirilgan va mashq qilingan bo'lishi shart.

**Spring'da qayerda uchraydi:** Flyway'da `undo` migratsiyalari faqat Flyway Teams'da bor, shuning uchun Spring Boot loyihalarida ko'proq expand-contract usuli qo'llanadi: `spring.flyway.baseline-on-migrate`, `spring.flyway.out-of-order` sozlamalari va alohida "forward fix" migratsiyasi. Liquibase'da esa `<rollback>` bloki va `liquibase rollbackCount`/`rollbackToDate` komandalari mavjud (`spring.liquibase.*`). Artifact darajasida Kubernetes `kubectl rollout undo deployment/...`, Helm `helm rollback`, Argo Rollouts'ning `abort` mexanizmi ishlatiladi; Spring Boot Actuator'ning `/actuator/info` va `/actuator/health` endpointlari qaysi versiya ishlayotganini va qaytarish kerakligini aniqlashga xizmat qiladi (`spring.boot.build-info` orqali `build.version`).

**Qo'llanish keyslari:**
- Canary deploy'da error rate oshgach, Argo Rollouts analysis'i avtomatik `abort` qilib eski ReplicaSet'ga qaytishi.
- Yangi API versiyasi mijoz client'larini buzgach, Gateway orqali trafikni eski service versiyasiga yo'naltirish.
- Noto'g'ri feature flag yoqilgandan keyin kodni deploy qilmasdan flag'ni o'chirib "logical rollback" qilish.
- Liquibase changeset xato ishlaganda `rollbackCount 1` bilan schema o'zgarishini bekor qilish.
- Performance regressiya aniqlangach, oldingi image tag'iga Helm rollback qilish.

**Deployment rollback i nimani qamramaydi.** `kubectl rollout undo` va unga o'xshash mexanizmlar pod shablonini, ya'ni ReplicaSet darajasidagi holatni qaytaradi. Pod dan BOSHQA hech narsani - ConfigMap ni, Secret ni, bog'liq servisning versiyasini - Deployment yangilamaydi ham, qaytarmaydi ham. Shuning uchun reliz birligi bir necha resursdan iborat bo'lsa, ularning relizi va rollback i yuqori darajadagi mexanizm bilan boshqariladi: reliz skripti, Helm reliz versiyasi yoki GitOps da bitta commit. Amalda eng ko'p uchraydigan nosozlik shu chegarada tug'iladi - image qaytariladi, lekin yangi versiya bilan birga kelgan ConfigMap joyida qolib, eski kod yangi konfiguratsiya bilan ishga tushadi.

**Ehtiyot bo'ling:** Destruktiv migratsiyalar (ustun o'chirish, `NOT NULL` qo'shish, tur o'zgartirish) rollback'ni imkonsiz qiladi - avval expand, keyin contract bosqichini alohida release'larda bajaring. Ikkinchi tuzoq: rollback hech qachon sinalmagan bo'lsa, u inqiroz paytida ishlamaydi; uni release checklist'ida muntazam mashq qilish kerak. Uchinchisi Kubernetes tomonida: `kubectl rollout undo` faqat saqlangan revision'lar hisobidan ishlaydi, `revisionHistoryLimit` esa default 10 - uni "chiqindini kamaytiraman" deb 0 ga qo'ysangiz, Deployment butun tarixini tozalaydi va rollback umuman imkonsiz bo'ladi.

## 22.15 Sidecar konteyner (Sidecar Container)

**Tavsif:** Asosiy ilova konteyneriga yordamchi funksiyani alohida konteyner sifatida biriktirib, uni bitta Pod ichida yonma-yon ishlatish patterni. Ikki konteyner network namespace'ni (localhost) va kerak bo'lsa volume'ni birga ishlatadi, lekin mustaqil ravishda build qilinadi, versiyalanadi va yangilanadi. Bu cross-cutting vazifalarni (log yig'ish, proxy, konfiguratsiya sinxronizatsiyasi, metrika eksporti) ilova kodidan ajratib olishga imkon beradi. Natijada polyglot tizimda bir xil infratuzilma imkoniyatlari barcha tillarga bir xil tarzda beriladi. Pattern ikki manbada ham kanonik: Burns unga modullilik va qayta ishlatish tomonidan qaraydi va har konteynerning o'z API'sini e'lon qilishi, parametrlanishi va hujjatlashtirilishini talab qiladi (bu uch talab [22.44](#2244-konteyner-shartnomasi-parametr-api-va-hujjat-container-contract-parameters-api-documentation) da alohida yozilgan), Ibryam va Huss esa uni Pod ichidagi struktura patterni sifatida yozadi.

**Spring'da qayerda uchraydi:** Spring Boot ilovasi Pod'da Envoy (Istio `istio-proxy`) yoki Linkerd proxy bilan birga ishlaganda, ilova faqat `http://localhost:...` ga murojaat qiladi va mTLS, retry, circuit breaking sidecar'da bajariladi - bu holda `spring-cloud-starter-circuitbreaker-resilience4j`'ni dublikat qilmaslik kerak. Log sidecar'lari (Fluent Bit, Vector) uchun Spring Boot'da `logging.file.name` bilan shared `emptyDir` volume'ga yoziladi yoki Logback'ning `LogstashEncoder`'i (net.logstash.logback) bilan JSON format beriladi. Konfiguratsiya uchun Vault Agent Injector sidecar fayl yozadi, Spring esa `spring.config.import=file:/vault/secrets/application.yaml` yoki `spring-cloud-vault` bilan o'qiydi. Kubernetes 1.29+ da `initContainers` ichida `restartPolicy: Always` bilan rasmiy "native sidecar" mavjud.

**Qo'llanish keyslari:**
- Istio sidecar orqali Spring Boot servislari o'rtasida kodga tegmasdan mTLS yoqish.
- Fluent Bit sidecar bilan ilova loglarini markazlashgan Elasticsearch/Loki'ga uzatish.
- Vault Agent sidecar bilan DB parolini muntazam rotatsiya qilib fayl orqali berish.
- JMX/metrikalarni Prometheus formatiga o'giruvchi exporter sidecar (legacy ilovalar uchun).
- Config file'ni Git repodan muntazam pull qiluvchi `git-sync` sidecar.

**Ro'yxatdagi birinchi konteyner default hisoblanadi.** Pod ta'rifidagi `containers` ro'yxati tartibsiz emas: birinchisi asosiy konteyner deb olinadi va `kubectl exec`, `kubectl logs` kabi buyruqlar konteyner nomi berilmaganda shunga boradi. Shuning uchun sidecar ni ro'yxatning boshiga yozmaslik kerak - bu kichik qoida, lekin incident paytida seziladi: `kubectl logs` ilova logi o'rniga proxy logini chiqarsa, birinchi daqiqalar yo'qoladi.

**Keys: introspeksiyani kutubxona emas, sidecar bilan berish.** Sidecar ning qiymatini ko'rsatadigan aniq misol - ishlab turgan protsessning ichini ko'rsatadigan asbob (masalan `top` ga o'xshash introspeksiya endpoint i). Uni har til uchun alohida kutubxona qilib yozish va har ilovaga qo'shish qimmat: kutubxona versiyalari farq qiladi, tillarda imkoniyatlar bir xil bo'lmaydi va qo'shilishi har jamoaning ixtiyorida qoladi. PID namespace ni asosiy konteyner bilan bo'lishadigan sidecar bir xil natijani boshqa narx bilan beradi: orkestrator uni barcha ilovaga avtomatik qo'shadi, vositalar to'plami esa hamma joyda bir xil bo'ladi.

**Ehtiyot bo'ling:** Har bir sidecar Pod'ning CPU/memory sarfini va startup vaqtini oshiradi - yuzlab replica'da bu jiddiy xarajat, shuningdek sidecar ilovadan oldin tayyor bo'lmasa, startup'da connection refused xatolari paydo bo'ladi (native sidecar yoki `holdApplicationUntilProxyStarts` bilan hal qilinadi). Sidecar'ni mikroservisga aylantirib, unga biznes logikasi joylashtirish anti-pattern. Teskari chegara ham bor va u tanlov sharti sifatida yoziladi: kutubxona yo'li ilovaga ko'proq mos tushadi (til, build va konfiguratsiya bir xil), modul konteyner esa umumiyroq va qayta ishlatiladigan bo'ladi, shuning uchun o'z sidecar ini noldan yozish faqat ishlash talablari ekstremal bo'lganda to'g'ri - qolgan holatda mavjud modul konteyner yoki tayyor kutubxona olinadi.

## 22.16 Ambassador konteyner (Ambassador Container)

**Tavsif:** Tashqi servisga chiqish murakkabligini alohida konteynerga chiqarib, ilova faqat `localhost` orqali oddiy ulanish qiladigan sidecar turi. Ambassador service discovery, TLS termination, connection pooling, sharding, retry va rate limiting kabi vazifalarni o'z ichiga oladi. Ilova uchun tashqi dunyo bitta statik local endpoint'ga aylanadi, bu esa test va lokal ishlab chiqishni osonlashtiradi. Sidecar'dan farqi: ambassador aynan chiquvchi (egress) trafikka proxy bo'lib xizmat qiladi. Burns ambassador uchun uch asosiy qo'llanishni sanaydi: servisni shardlash, service brokering hamda tajriba o'tkazish yoki so'rovni bo'lish; Ibryam va Huss esa uni Pod ichidan tashqi dunyoga chiqadigan proxy sifatida beradi.

**Spring'da qayerda uchraydi:** Cloud SQL Auth Proxy yoki AWS RDS Proxy ambassador sifatida ishlaganda Spring Boot'ning `spring.datasource.url` qiymati `jdbc:postgresql://localhost:5432/db` bo'lib qoladi va IAM autentifikatsiyasi proxy'da bajariladi. Istio'da egress uchun `ServiceEntry` + `DestinationRule` bilan sidecar ambassador rolini bajaradi, Spring'dagi `RestClient`/`WebClient` esa oddiy HTTP yuboradi. Redis cluster yoki Memcached uchun Twemproxy/Envoy local port beradi, `spring-boot-starter-data-redis` esa `spring.data.redis.host=localhost` bilan ishlaydi. Shuningdek Kafka uchun local proxy (masalan Envoy'ning Kafka filter'i) ishlatilganda `spring.kafka.bootstrap-servers=localhost:9092` qoladi.

**Qo'llanish keyslari:**
- Cloud SQL Proxy bilan ilovaga DB parolini bermasdan IAM orqali ulanish.
- Legacy Spring ilovasini o'zgartirmasdan tashqi API'larga mTLS bilan chiqarish.
- Redis shardlarini ambassador ichida taqsimlab, client kodni oddiy saqlash.
- Tashqi provayder API'siga chiqishda markazlashgan rate limiting va retry qo'yish.
- Lokal development'da ambassador'ni mock serverga almashtirib integratsiya testlari o'tkazish.

**Ehtiyot bo'ling:** Ambassador qo'shimcha network hop keltiradi va o'zi single point of failure bo'lib qolishi mumkin - uning health check'i, timeout'i va resurs limitlari ilovaning timeout'laridan qisqaroq/muvofiq sozlanishi kerak. Ikki joyda (ilovada ham, ambassador'da ham) retry yoqilsa, retry storm va kutilmagan kechikish kuchayishi yuzaga keladi.

## 22.17 Adapter konteyner (Adapter Container)

**Tavsif:** Ilovaning nostandart chiqishini (log formati, metrika, health ma'lumoti) tashqi tizim kutgan yagona standart formatga o'giruvchi sidecar turi. Ambassador chiquvchi trafikni normallashtirsa, adapter ilovadan tashqariga ko'rinadigan interfeysni normallashtiradi. Bu heterogen (turli til va framework'dagi) servislarni bitta monitoring va logging platformasiga arzon narxda ulashga imkon beradi. Ilova kodi o'zgarmaydi - moslashtirish infratuzilma qatlamida bajariladi. Burns adapter uchun uch keysni ko'rsatadi: monitoring, logging va boy health monitor qo'shish; Ibryam va Huss esa uni heterogen tizimni yagona interfeysga keltirish patterni deb yozadi.

**Spring'da qayerda uchraydi:** Spring Boot 3.x'da Micrometer `PrometheusMeterRegistry` (`micrometer-registry-prometheus`) metrikani `/actuator/prometheus` orqali o'zi beradi, shuning uchun adapter asosan legacy yoki non-Spring komponentlar uchun kerak bo'ladi: `jmx_exporter` JMX'ni Prometheus formatiga, `statsd_exporter` StatsD'ni Prometheus'ga o'giradi (Spring tomonida alternativa - `micrometer-registry-statsd`). Log tomonida Fluent Bit/Vector adapter sifatida plain text Logback chiqishini JSON'ga parse qiladi; Spring'ning o'zida bu `logging.structured.format.console=ecs|logstash|gelf` (Spring Boot 3.4+) bilan ilova ichida ham bajarilishi mumkin. OpenTelemetry Collector esa `opentelemetry-spring-boot-starter` yuborgan ma'lumotni turli backend formatlariga moslashtiruvchi adapter rolini o'ynaydi.

**Qo'llanish keyslari:**
- Legacy JVM ilovasidan JMX metrikalarni `jmx_exporter` bilan Prometheus'ga chiqarish.
- Har xil til'dagi servislar loglarini bitta ECS/JSON schema'ga keltirish.
- OpenTelemetry Collector orqali trace'larni bir vaqtda Jaeger va Datadog'ga yuborish.
- Eski ilovaning `/status` HTML javobini standart health formatiga o'girib Kubernetes probe'ga berish.
- Vendor-specific audit loglarni markazlashgan SIEM kutgan formatga normallashtirish.

**Nega upstream image ga tegilmaydi.** Monitoring yoki log formatini to'g'rilashning ko'rinadigan yo'li bor: mavjud konteynerni (masalan MySQL ning rasmiy image ini) o'zgartirib, unga kerakli eksporterni qo'shib qo'yish. Bu yo'l bir marta ishlaydi va keyin qarz bo'lib qoladi: o'sha image ni endi o'zingiz saqlashga majbur bo'lasiz - har yangi versiyada o'zgarishni qayta qo'llash, xavfsizlik yangilanishlarini kuzatish va farqni hujjatlashtirish. Adapter konteyner shu narxni to'lamaydi: upstream image asl holida qoladi va yangilanishi oddiy tag almashtirishga aylanadi, moslashtirish esa alohida, o'zingizga tegishli konteynerda yashaydi.

**Ehtiyot bo'ling:** Spring Boot allaqachon Micrometer va structured logging beradigan joyda adapter qo'shish ortiqcha murakkablik va ikki marta transformatsiya (format yo'qotish) demakdir - avval ilovaning nativ imkoniyatlarini tekshiring. Adapter'da parse qoidalari log formati o'zgarganda jim buziladi, shuning uchun format shartnomasini test bilan qulflash kerak.

## 22.18 Init konteyner (Init Container)

**Tavsif:** Asosiy konteynerlar ishga tushishidan oldin to'liq bajarilib tugaydigan, bir martalik tayyorlov vazifalarini o'tkazuvchi konteyner. Kubernetes init konteynerlarni `.spec.initContainers` tartibida ketma-ket ishga tushiradi va oddiy init konteyner muvaffaqiyatli tugamaguncha keyingisi boshlanmaydi; xato bo'lsa Pod `restartPolicy`ga qarab qayta uriniladi. Bitta istisno bor: `restartPolicy: Always` qo'yilgan init konteyner (native sidecar) umuman tugamaydi - kubelet uning `started` holatini `true` qilgandan keyin ro'yxatdagi keyingi init konteynerni boshlaydi, ya'ni "tugadi" sharti faqat sidecar bo'lmagan init konteynerlarga tegishli. Shu sababli u dependency kutish, schema migration, fayl yuklab olish, ruxsatlarni to'g'rilash kabi ishlar uchun ideal. Natijada asosiy ilova image'i toza va yagona vazifaga mo'ljallangan bo'lib qoladi.

**Spring'da qayerda uchraydi:** Eng keng tarqalgan keys - Flyway yoki Liquibase migratsiyasini init konteynerda alohida ishga tushirib, ilova replica'larida esa `spring.flyway.enabled=false` (yoki `spring.liquibase.enabled=false`) qilib qo'yish; shunda bir nechta replica bir vaqtda migration qilishga urinmaydi. Migratsiyani Flyway/Liquibase CLI image'i yoki Spring Boot ilovasining o'zini maxsus profil bilan ishga tushirish orqali bajarish mumkin. Konfiguratsiya va sertifikatlarni oldindan tortib olish uchun Vault Agent init mode, `git-sync` yoki `busybox` skriptlari ishlatiladi, Spring esa `spring.config.import=file:/config/app.yaml` bilan o'qiydi. Kubernetes 1.29+ dan boshlab `restartPolicy: Always` bilan init konteyner "native sidecar" bo'lib ham ishlaydi.

**Qo'llanish keyslari:**
- Flyway migratsiyasini init konteynerda bir marta bajarib, 20 replica'da race'ni oldini olish.
- PostgreSQL yoki Kafka tayyor bo'lishini kutib turuvchi `wait-for-it` skripti.
- Vault'dan secret'larni `emptyDir` volume'ga tortib olib, ilovaga fayl sifatida berish.
- Shared volume'dagi fayllar egasi/ruxsatini (`chown`) ilova non-root user'i uchun to'g'rilash.
- Statik asset yoki ML modelini S3/GCS'dan yuklab olib, ilova startup'ini tezlashtirish.

**Initsializatsiyani init konteynerga chiqarishning uch sababi.** Tayyorlov ishini asosiy konteyner ichida ham bajarish mumkin, shuning uchun ajratishning sababi aytib qo'yilishi kerak. Uchta sabab bor: tayyorlovga ilova image ida bo'lmagan asbob yoki kutubxona kerak (`curl`, `git`, migratsiya CLI si); tayyorlovga ilova image iga ataylab berilmagan huquq kerak (fayl egasini o'zgartirish, tizim sozlamasiga tegish); yoki tashqi bog'liqlik tayyor bo'lmaguncha startup ni kechiktirish kerak. Birinchi ikkisining natijasi bitta - ilova image i kichik va huquqsiz qoladi, asbob va huquq esa faqat bir martalik konteynerda yashaydi.

**Tanlov zinapoyasi: bash skript, hook, init konteyner.** Startup va shutdown mantiqini joylashtirishning uch yo'li bor va ularning narxi bir xil emas. Eng arzoni - mantiqni konteyner buyrug'i ichidagi bash skriptga qo'yish: u hech qanday platforma imkoniyatini talab qilmaydi, lekin konteynerni skript bilan qattiq bog'laydi, qayta ishlatilmaydi va texnik xizmatni og'irlashtiradi - skript image ichida yashirin qoladi va uni manifestdan ko'rinmaydi. Keyingi pog'ona - lifecycle hook (`postStart`, `preStop`): mantiq manifestga chiqadi va ko'rinadigan bo'ladi, lekin platforma unga kafolat bermaydi. Eng kuchli pog'ona - init konteyner: u tartibni kafolatlaydi, alohida image va huquq bilan ishlaydi va boshqa pod larda qayta ishlatiladi. Kafolat ham, qayta ishlatish ham shu tartibda oshadi, shuning uchun mantiq o'sgan sari pastdan yuqoriga ko'chiriladi.

**Ehtiyot bo'ling:** Init konteyner har Pod restartida qaytadan ishlaydi, shuning uchun u idempotent va tez bo'lishi shart - uzoq migratsiya rolling update'ni sekinlashtiradi va `terminationGracePeriod`/probe sozlamalari bilan ziddiyat keltirishi mumkin. Migratsiyani init konteynerga ko'chirsangiz, backward compatible schema (expand-contract) qoidasiga qat'iy rioya qilish zarur, aks holda eski va yangi Pod'lar bir vaqtda ishlayotganda xato beradi.

## 22.19 Health probe'lar (Health Probes: Liveness, Readiness, Startup)

**Tavsif:** Orkestratorga ilovaning ishlayotgani (liveness), trafik qabul qilishga tayyorligi (readiness) va hali ishga tushayotgani (startup) haqida mashina o'qiy oladigan signal berish patterni. Uch probe'dan oldin bitta bepul tekshiruv turadi va u ko'pincha e'tibordan qoladi: process health check. Ibryam va Huss uni eng oddiy tekshiruv deb ataydi: kubelet konteyner jarayonini doimiy kuzatadi va jarayon ishlamay qolsa konteynerni qayta ishga tushiradi, ya'ni boshqa hech qanday probe yozmasdan ham ilova shu umumiy tekshiruv hisobiga bir oz chidamliroq bo'ladi. Shundan amaliy qoida chiqadi: agar ilova har qanday nosozlikni o'zi sezib, o'zini to'xtata olsa (fail fast), process health check yetarli; deadlock kabi "jarayon tirik, lekin ish bajarmaydi" holati esa faqat liveness probe bilan ochiladi, chunki bunday ilova process health check nuqtai nazaridan sog'lom ko'rinadi (Ibryam/Huss, 4-bob, 36-bet). Liveness muvaffaqiyatsiz bo'lsa konteyner restart qilinadi, readiness muvaffaqiyatsiz bo'lsa Pod Service endpoint'laridan chiqariladi (lekin restart bo'lmaydi), startup probe esa sekin ishga tushadigan ilovada liveness bilan birga readiness'ni ham bloklab turadi - startup probe muvaffaqiyatli bo'lmaguncha kubelet liveness va readiness probe'larning hech birini bajarmaydi. To'g'ri ajratilgan probe'lar rolling update, autoscaling va graceful shutdown'ning asosidir.

**Spring'da qayerda uchraydi:** Spring Boot Actuator `/actuator/health/liveness` va `/actuator/health/readiness` endpointlarini beradi; Kubernetes muhitida ular avtomatik yoqiladi yoki `management.endpoint.health.probes.enabled=true` bilan majburan yoqiladi. `ApplicationAvailability`, `LivenessState` va `ReadinessState` interfeyslari orqali holatni kodda o'qish, `AvailabilityChangeEvent.publish(context, ReadinessState.REFUSING_TRAFFIC)` bilan o'zgartirish mumkin. Custom tekshiruvlar `HealthIndicator`/`ReactiveHealthIndicator` implementatsiyasi bilan yoziladi, `management.endpoint.health.group.readiness.include=db,redis` orqali guruhlanadi. Probe endpoint'ini asosiy portdan ajratish uchun `management.server.port` ishlatiladi. Kubernetes tomonidagi default qiymatlarni yodda tuting: `initialDelaySeconds` 0, `periodSeconds` 10, `timeoutSeconds` 1 (minimal qiymat ham 1), `successThreshold` 1 (liveness va startup uchun u faqat 1 bo'lishi mumkin), `failureThreshold` 3. Shulardan eng xavflisi `timeoutSeconds: 1`: yuklama ostida yoki GC pauzasida `/actuator/health/liveness` bir sekundga sig'masa, uchta ketma-ket timeout konteynerni restart qiladi - ya'ni soxta restart'larning eng keng tarqalgan sababi aynan shu sozlanmagan default. Kubernetes 1.25+ da probe darajasida `terminationGracePeriodSeconds` ham bor (liveness va startup uchun; readiness probe'da u taqiqlangan).

**Qo'llanish keyslari:**
- Kubernetes `readinessProbe` uchun `/actuator/health/readiness` ni ko'rsatib, warm-up tugaguncha trafik yubormaslik.
- Deadlock'ka tushgan ilovani `livenessProbe` bilan aniqlab avtomatik restart qilish.
- JVM va Hibernate sekin ishga tushadigan katta monolitda `startupProbe` bilan `failureThreshold` ni oshirish.
- Kafka consumer lag kritik bo'lganda custom `HealthIndicator` bilan readiness'ni `DOWN` qilish.
- Load balancer uchun `management.server.port=8081` da alohida health porti ochish.

**Tekshiruv TASHQARIDAN bajariladi.** Sog'liq tekshiruvini ilovaning o'z ichidagi flag yoki watchdog bilan almashtirish mumkin emas va sababi mexanik: ba'zi nosozliklar ilovani shu nosozlik haqida xabar berishdan ham to'sadi. Thread pool to'lgan, heap tugagan yoki event loop bloklangan ilova o'zining ichki watchdog ini ham ishlata olmaydi va "hammasi joyida" degan oxirgi holatda muzlab qoladi. Shuning uchun qaror tashqarida qabul qilinadi: kubelet tashqaridan probe yuboradi va javob kelmasa yoki kechiksa, ilovaning fikrini so'ramasdan chora ko'radi. Amaliy natija - `/actuator/health/liveness` endpoint i haqiqiy tekshiruv bajarishi kerak, oldindan hisoblangan statik qiymatni qaytarmasligi.

**Restart sababni tuzatmasa, liveness probe foyda bermaydi.** Liveness probe ning yagona chorasi - konteynerni qayta ishga tushirish, shuning uchun uni yozishdan oldin bitta savolga javob beriladi: restart bu nosozlikni tuzatadimi. Deadlock, tugab qolgan ichki navbat yoki buzilgan ichki holat uchun javob "ha". Konfiguratsiya xatosi, yo'q bog'liqlik yoki kod xatosi uchun javob "yo'q" va bu holatda yiqiladigan liveness probe faqat zarar beradi: Kubernetes asosiy muammoni tuzatmasdan konteynerni qayta-qayta ko'taradi, log lar restart bilan yo'qoladi va haqiqiy sabab restart tsikli ortida ko'rinmas bo'lib qoladi. Shunday hollarda probe ni olib tashlab, pod ni yiqilgan holatda qoldirish diagnostikaga ko'proq yordam beradi.

**Ehtiyot bo'ling:** Liveness probe'ga tashqi bog'liqliklarni (DB, boshqa servis) qo'shish eng keng tarqalgan xato - DB qisqa vaqt ishlamasa, butun kluster restart tsikliga tushib ketadi; tashqi bog'liqliklar faqat readiness'ga tegishli. `initialDelaySeconds`/`timeoutSeconds` juda qisqa bo'lsa, yuklama paytida soxta restartlar boshlanadi, juda uzun bo'lsa nosoz Pod uzoq vaqt trafik oladi.

## 22.20 Nazorat ostida to'xtatish (Graceful Shutdown)

**Tavsif:** `SIGTERM` signalini olgandan keyin yangi so'rovlarni qabul qilishni to'xtatib, ishlayotgan so'rovlar va task'larni tugatib, resurslarni toza yopib chiqish patterni. Bu rolling update, scale-in va spot instance uzilishlarida 5xx xatolari va yarim bajarilgan tranzaksiyalarni oldini oladi. Kubernetes'da bu ketma-ketlik kafolatlanmaydi: kubelet Pod'ni graceful to'xtatishni boshlaganda control plane Pod'ni EndpointSlice'lardan olib tashlashni SHU PAYTNING O'ZIDA, ya'ni SIGTERM bilan parallel bajaradi - demak SIGTERM kelganda LB hali trafik yuborayotgan bo'lishi mumkin. Shuning uchun oynani `preStop` hook bilan ochish kerak: `preStop` SIGTERM'dan OLDIN ishlaydi, shu yerdagi qisqa kutish propagatsiyaga vaqt beradi. Shutdown byudjeti ham shu grace oynasiga sig'ishi shart: `terminationGracePeriodSeconds` (default 30s) > `preStop` + Spring'ning `timeout-per-shutdown-phase` (default 30s) + zaxira.

**Spring'da qayerda uchraydi:** Spring Boot'da `server.shutdown=graceful` va `spring.lifecycle.timeout-per-shutdown-phase=30s` asosiy sozlamalar; `SmartLifecycle` yoki `@PreDestroy` bilan o'z komponentlarini tartibli yopish mumkin. Kubernetes muhitida Actuator'ning readiness'i avtomatik `OUT_OF_SERVICE` ga o'tadi, qo'lda esa `AvailabilityChangeEvent.publish(ctx, ReadinessState.REFUSING_TRAFFIC)` ishlatiladi; `preStop` hook'da qisqa `sleep` qo'yish LB propagatsiyasini kutish uchun amaliy usul. Kafka uchun `spring-kafka`'ning `KafkaListenerEndpointRegistry.stop()`, scheduler uchun `ThreadPoolTaskExecutor`'da `setWaitForTasksToCompleteOnShutdown(true)` va `setAwaitTerminationSeconds(...)` ishlatiladi. Shuningdek `/actuator/shutdown` endpointi mavjud, lekin production'da odatda o'chirib qo'yiladi.

```java
@Component
class ConsumerLifecycle implements SmartLifecycle {
    private final KafkaListenerEndpointRegistry registry;
    ConsumerLifecycle(KafkaListenerEndpointRegistry registry) { this.registry = registry; }
    @Override public void start() { registry.start(); }
    @Override public void stop() { registry.stop(); }       // SIGTERM'da chaqiriladi
    @Override public boolean isRunning() { return registry.isRunning(); }
    @Override public int getPhase() { return Integer.MAX_VALUE; } // eng birinchi to'xtaydi
}
```

**Qo'llanish keyslari:**
- Rolling update paytida ishlayotgan HTTP so'rovlarni tugatib, 502/504 xatolarini nolga tushirish.
- Kafka consumer'ning offset'ini commit qilib, qayta ishlash dublikatini kamaytirish.
- Uzoq ishlaydigan batch task'ni checkpoint saqlab to'xtatish (`@Scheduled` + `TaskScheduler`).
- Spot/preemptible instance uzilishi ogohlantirilganda ulanishlarni toza yopish.
- HikariCP connection pool'ni yopib, DB'da osilib qolgan sessiyalarni oldini olish.

**Ehtiyot bo'ling:** Ikki default bir-biriga teng: Kubernetes `terminationGracePeriodSeconds` 30s va Spring `spring.lifecycle.timeout-per-shutdown-phase` 30s. Ikkisini ham o'zgartirmasdan `preStop` ga sleep qo'shsangiz byudjet allaqachon to'lgan bo'ladi va `SIGKILL` keladi: `terminationGracePeriodSeconds` ni ataylab oshiring. Grace tugaganda `preStop` hali ishlayotgan bo'lsa kubelet faqat bir martalik 2 sekund qo'shadi. Ikkinchi tuzoq: readiness'ni `DOWN` qilmasdan darhol drain boshlash, chunki load balancer bir necha soniya hali trafik yuborib turadi. Uchinchisi - native sidecar bilan ishlaganda tartibni unutish: kubelet sidecar konteynerlarni asosiy ilova konteyneri TO'LIQ to'xtaguncha o'chirmaydi, keyin ularni ro'yxatdagi teskari tartibda yopadi. Istio yoki Vault sidecar'i app drain tugaguncha tirik qolishi aynan shuning hisobiga ishlaydi, lekin sidecar'ning o'z to'xtash vaqti ham umumiy grace byudjetidan yeydi.

## 22.21 Gorizontal / vertikal avtomatik masshtablash (Horizontal / Vertical Autoscaling)

**Tavsif:** Yuklamaga qarab replica sonini oshirib-kamaytirish (gorizontal) yoki bitta instance'ning CPU/memory limitini o'zgartirish (vertikal) patterni. Gorizontal masshtablash stateless servislar uchun afzal, chunki u deyarli cheksiz va uzilishsiz bo'ladi; vertikal esa stateless bo'lmagan yoki thread-bound ilovalar uchun qo'llanadi, lekin odatda Pod restartini talab qiladi. Scaling qarori metrikaga asoslanadi: CPU, memory, so'rov soni, queue lag yoki custom biznes metrikasi. To'g'ri sozlangan autoscaling xarajatni kamaytiradi va yuklama cho'qqilarida SLO'ni saqlaydi.

**Spring'da qayerda uchraydi:** Spring Boot tomonidan Micrometer metrikalari (`/actuator/prometheus`) Kubernetes HPA'ga Prometheus Adapter yoki KEDA (`ScaledObject`) orqali uzatiladi - masalan `kafka_consumergroup_lag` yoki `http_server_requests_seconds_count` bo'yicha scale qilish. Vertikal tomonda Java 17+ konteyner-aware bo'lib, `-XX:MaxRAMPercentage=75` va `UseContainerSupport` bilan Pod memory limitiga moslashadi; Spring Boot 3.x uchun bu JVM flag'lari `JAVA_TOOL_OPTIONS` orqali beriladi. Masshtablash tezligi uchun startup vaqti muhim: Spring AOT (`spring-boot-maven-plugin` `process-aot`), GraalVM native image yoki CDS (`-XX:SharedArchiveFile`, Spring Boot 3.3+ `spring-boot-jarmode-tools`) qo'llaniladi. Thread model nuqtai nazaridan Java 21+ virtual thread'lar (`spring.threads.virtual.enabled=true`) bitta Pod'ning sig'imini oshiradi.

**Qo'llanish keyslari:**
- Kunlik trafik cho'qqisida HPA bilan Spring Boot API replica'sini 3 dan 30 ga ko'tarish.
- KEDA orqali Kafka consumer lag oshganda consumer Pod'larini avtomatik qo'shish.
- Kechasi trafik yo'qolganda replica'ni minimumgacha tushirib cloud xarajatini kamaytirish.
- VPA'ning recommendation rejimida JVM heap uchun to'g'ri memory request/limit topish.
- Native image yordamida scale-out kechikishini soniyalardan millisekundlarga tushirish.

**Ehtiyot bo'ling:** JVM ilovasida CPU-asosidagi HPA aldamchi: JIT warm-up va GC CPU'ni ko'tarib, soxta scale-out keltiradi - so'rov darajasidagi yoki lag metrikalari ishonchliroq, `stabilizationWindowSeconds` bilan flapping'ni bosish kerak. HPA va VPA'ni bitta resursda bir xil metrika (CPU/memory) bo'yicha birga ishlatmang, hamda masshtablanadigan servis DB connection pool'i (`spring.datasource.hikari.maximum-pool-size` × replica) DB limitidan oshib ketmasligini hisoblang.

## 22.22 Bitta hostda bir nechta service instance (Multiple Service Instances per Host)

**Tavsif:** Bir nechta servis instance'ini bitta host yoki VM ichida, alohida process yoki process guruhlari sifatida ishga tushirish patterni. Uning afzalligi - resurslardan yuqori foydalanish va kam deployment xarajati; kamchiligi - izolyatsiyaning zaifligi, chunki bitta instance CPU, memory yoki fayl deskriptorlarini "yeb" qo'yishi mumkin. Bu klassik model: bitta application server'da (yoki bitta OS'da) ko'p WAR/JAR joylashtirish. Hozirda u ko'proq legacy muhitlarda, on-premise serverlarda va development/test stendlarida uchraydi.

**Spring'da qayerda uchraydi:** An'anaviy ko'rinishi - bitta Tomcat yoki WildFly'da bir nechta WAR deploy qilish (`spring-boot-starter-web` + `spring-boot-starter-tomcat` `provided` scope, `SpringBootServletInitializer` extend qilingan holda). Zamonaviy ko'rinishi - bitta VM'da bir nechta executable JAR'ni turli portlarda (`server.port=0` tasodifiy port yoki `--server.port=8081`) systemd service sifatida ishga tushirish; Spring Boot bunga `spring-boot-maven-plugin`'ning fully executable JAR imkoniyati bilan yordam beradi. Instance'larni topish uchun Spring Cloud Consul/Eureka client (`spring-cloud-starter-netflix-eureka-client`) `eureka.instance.instance-id` ni `${spring.application.name}:${random.value}` ko'rinishida belgilaydi. Izolyatsiya uchun har bir process'ga `-XX:MaxRAMPercentage` emas, aniq `-Xmx` berish va `cgroups`/systemd `MemoryMax` qo'yish amaliyoti bor.

**Qo'llanish keyslari:**
- On-premise serverda bir nechta kichik ichki servisni bitta VM'da yuritish.
- CI muhitida bir xil servisning bir nechta versiyasini turli portlarda integratsiya testi uchun ko'tarish.
- Legacy Java EE serverida umumiy WAR'larni bitta JVM'da saqlab, litsenziya xarajatini kamaytirish.
- Development laptop'ida docker-compose'siz bir nechta Spring Boot modulini parallel ishga tushirish.
- Kam trafikli ko'p mijozli (multi-tenant) ichki vositalarni bitta hostda konsolidatsiya qilish.

**Ehtiyot bo'ling:** Resurs izolyatsiyasi yo'qligi "noisy neighbour" muammosini keltiradi: bitta instance'dagi memory leak yoki GC pauzasi hammasini ta'sirlaydi, bitta JVM'da ko'p WAR bo'lsa classloader leak va bitta restart hammasini yiqitadi. Port to'qnashuvi, log fayllari aralashishi va monitoring'da instance'larni ajratib bo'lmasligi ham tipik tuzoqlar - bugungi kunda konteyner-per-instance modelini afzal ko'ring.

## 22.23 Har bir service instance alohida host / VM / konteynerda (Service Instance per Host / VM / Container)

**Tavsif:** Har bir servis instance'ini o'zining izolyatsiyalangan ijro muhitida - alohida host, VM yoki (eng ko'p) konteynerda ishlatish patterni. Bu resurs limitlarini aniq belgilash, mustaqil deploy qilish, muammoli instance'ni boshqalarga ta'sir qilmasdan o'ldirish va texnologiya stack'ini erkin tanlash imkonini beradi. Immutable infrastructure g'oyasi bilan birga ishlaydi: instance o'zgartirilmaydi, balki yangi versiya bilan almashtiriladi. Konteyner variantida boot vaqti va overhead eng kichik, VM variantida izolyatsiya eng kuchli.

**Spring'da qayerda uchraydi:** Spring Boot'ning executable JAR + Cloud Native Buildpacks integratsiyasi aynan shu modelga mo'ljallangan: `mvn spring-boot:build-image` (yoki `gradle bootBuildImage`) OCI image yasaydi, `spring-boot-maven-plugin`'ning layered JAR (`layers.enabled`) esa Docker cache'ni optimallashtiradi. Image ichida JVM konteyner limitlarini hurmat qiladi (Java 17+ `UseContainerSupport`), Spring Boot 3.3+ da CDS va `spring-boot-jarmode-tools` bilan startup tezlashtiriladi, GraalVM native image uchun `spring-boot-starter-parent`'ning `native` profili ishlatiladi. Deploy tomonida Kubernetes `Deployment` + `Service`, yoki Spring Cloud Kubernetes (`spring-cloud-starter-kubernetes-client-all`) orqali discovery va `ConfigMap`/`Secret` bilan konfiguratsiya o'qilishi standart.

**Qo'llanish keyslari:**
- Har bir mikroservisni alohida Docker image sifatida build qilib Kubernetes'da `Deployment` bilan yuritish.
- Buildpacks bilan Dockerfile yozmasdan reproducible va xavfsiz base image olish.
- Resurs limitlarini servis-bo'yicha aniq belgilab, noisy neighbour muammosini yo'q qilish.
- Turli servislarni turli JDK versiyalarida (17, 21, 25) parallel ishlatish.
- Immutable image tag'lari bilan aniq va takrorlanadigan rollback qilish.

**Ehtiyot bo'ling:** Har bir instance'ga alohida JVM degani - o'z heap, metaspace va thread stack'i, shuning uchun ko'p mayda servis image'i memory'ni tez yeydi; `requests`/`limits` va `MaxRAMPercentage` ni birga hisoblash kerak. Shuningdek `latest` tag ishlatish immutable deployment tamoyilini buzadi va rollback'ni imkonsiz qiladi - doim aniq versiya yoki digest bilan deploy qiling.

**Konteyner izolyatsiyasining chegarasi:** `requests` va `limits`
resursni ajratadi, lekin bu VM yoki alohida jismoniy mashina
beradigan izolyatsiya darajasi emas. Newman buni ochiq aytadi:
konteyner resurs nuqtai nazaridan izolyatsiyalangan deb qarash
mumkin, lekin erta davrda bitta konteynerdagi jarayonning tashqariga
chiqib boshqa konteyner yoki asos mashina bilan muloqot qilishining
hujjatlashtirilgan yo'llari bo'lgan. Runtime va orkestrator
tomonidan katta ish qilingan, lekin qaror hamon sizda va mezon
oddiy: konteynerni **ishonchli** dasturni izolyatsiya qilishning
yaxshi vositasi deb qarang. Boshqalar yozgan kodni ishlatsangiz va
zararli tomon konteyner darajasidagi izolyatsiyani chetlab
o'tishidan tashvishlansangiz, hozirgi holatni o'zingiz chuqurroq
tekshirishingiz yoki kuchliroq izolyatsiyaga o'tishingiz kerak.
Newman o'rtadagi variantni ham nomlaydi: alohida yadro beradigan
Hyper-V konteynerlari va yengil VM shaklidagi Firecracker (AWS
Lambda da turli mijoz yuklamalarini to'liq ajratish uchun
ishlatiladi). Narxi ham aytilgan: bunday izolyatsiya ishga tushish
vaqtiga ta'sir qiladi va runtime narxini oddiy virtualizatsiyaga
yaqinlashtiradi. Amaliy qoida: o'z kodingiz va ishonchli base image
uchun oddiy konteyner, mijoz yuborgan kod yoki plugin uchun yengil
VM yoki alohida yadro.

## 22.24 Serverless deployment (Serverless Deployment)

**Tavsif:** Kodni serverlarni boshqarmasdan, provayder tomonidan talab bo'yicha ishga tushiriladigan funksiya yoki konteyner sifatida joylashtirish patterni. Scaling to'liq platformaga o'tadi, to'lov esa faqat haqiqiy ijro vaqti uchun amalga oshiriladi, nol trafikda xarajat ham nolga yaqin bo'ladi. Kamchiliklari - cold start, ijro vaqti va resurs limitlari, hamda cheklangan protokol/ulanish modeli (uzoq ulanishlar, connection pool'lar muammoli). JVM uchun eng muhim savol - ishga tushish tezligi va xotira izi.

**Spring'da qayerda uchraydi:** Spring Cloud Function (`spring-cloud-function-context`) biznes logikasini `java.util.function.Function`/`Supplier`/`Consumer` bean'lari sifatida yozish va bir xil kodni turli muhitlarda ishlatish imkonini beradi; AWS Lambda uchun `spring-cloud-function-adapter-aws` va `FunctionInvoker` handler ishlatiladi, Azure/GCP uchun ham mos adapterlar mavjud. Butun Spring Boot web ilovasini Lambda'da yuritish uchun AWS Serverless Java Container (`aws-serverless-java-container-springboot3`) qo'llanadi. Cold start'ni kamaytirish uchun GraalVM native image (`spring-boot-starter-parent` `native` profili + `org.graalvm.buildtools:native-maven-plugin`), AOT processing, yoki AWS Lambda SnapStart ishlatiladi. Konteyner-asosidagi serverless (AWS Fargate, Google Cloud Run, Azure Container Apps) uchun oddiy Spring Boot image yetarli va `server.shutdown=graceful` bilan scale-to-zero yumshoq o'tadi.

```java
@SpringBootApplication
public class OrderFunctionApp {
    public static void main(String[] args) { SpringApplication.run(OrderFunctionApp.class, args); }

    @Bean
    public Function<OrderRequest, OrderResponse> createOrder(OrderService service) {
        return req -> service.create(req);   // AWS: handler = ...FunctionInvoker
    }
}
```

**Qo'llanish keyslari:**
- S3'ga yuklangan faylni qayta ishlovchi event-driven Lambda funksiyasi.
- Kam va notekis chaqiriladigan webhook endpoint'ini Cloud Run'da scale-to-zero bilan yuritish.
- Kunlik report generatsiyasi yoki ETL job'ini scheduled funksiya sifatida bajarish.
- SQS/Pub-Sub xabarlarini Spring Cloud Function bilan qayta ishlash.
- Prototip yoki ichki vositani infratuzilma boshqarmasdan tez joylashtirish.

**Ehtiyot bo'ling:** JVM cold start va connection pool muammosi serverless'ning asosiy tuzog'i: har bir yangi instance DB'ga yangi ulanish ochadi va trafik cho'qqisida DB connection limitiga urilib qoladi - RDS Proxy/pgBouncer ishlating va `maximum-pool-size` ni 1-2 ga tushiring. Uzoq ishlaydigan, stateful yoki barqaror yuqori trafikli servislar uchun serverless odatda qimmatroq va cheklovli; bunday hollarda konteyner-per-instance modeli afzal.

## 22.25 Servis deploy platformasi (Service Deployment Platform - Kubernetes, PaaS)

**Tavsif:** Har bir servis o'zining deploy, scaling, restart va service discovery mantig'ini qayta yozmasligi uchun bu mas'uliyat umumiy platformaga (Kubernetes, Cloud Foundry, ECS, Nomad) ko'chiriladi. Ilova faqat container image va deklarativ konfiguratsiya beradi, qolganini platforma orkestratsiya qiladi: desired state'ni saqlash, o'lgan pod'ni qayta ko'tarish, trafikni load balancer orqali taqsimlash. Natijada infratuzilma kodi ilova kodidan ajraladi va o'nlab servis bir xil operatsion model bilan boshqariladi. Arxitektor uchun asosiy qaror - qancha mas'uliyat platformaga, qancha ilovaga qoladi.

**Spring'da qayerda uchraydi:** Spring Boot 3.x/4.x uchun standart yo'l - `spring-boot-starter-actuator` bilan `management.endpoint.health.probes.enabled=true` yoqib, Kubernetes `livenessProbe`/`readinessProbe` uchun `/actuator/health/liveness` va `/actuator/health/readiness` endpoint'laridan foydalanish (Boot Kubernetes muhitini avtomatik aniqlab, bu probe'larni o'zi yoqadi). Konfiguratsiya ConfigMap/Secret'dan `spring.config.import=configtree:/etc/config/` yoki environment variable orqali keladi; `spring-cloud-starter-kubernetes-client-config` va `...-discovery` esa ConfigMap-ni to'g'ridan-to'g'ri `Environment`'ga ulaydi va `DiscoveryClient`'ni Kubernetes Service API'siga map qiladi. Cloud Foundry uchun `spring-boot-starter-actuator` CF-specific `/cloudfoundryapplication` endpoint'ini beradi, `java-cfenv` esa `VCAP_SERVICES`'ni `DataSource` bean'iga bog'laydi.

**Qo'llanish keyslari:**
- 40-50 ta Spring Boot microservice'ni bitta Kubernetes cluster'da bir xil Helm chart template bilan deploy qilish.
- HPA (HorizontalPodAutoscaler) orqali `http_server_requests_seconds` metrikasi bo'yicha avtomatik scaling.
- Platform team Kubernetes operator yozib, `Kind: SpringService` CRD'si orqali product team'larga tayyor deploy abstraksiyasi berishi.
- Legacy monolitni Cloud Foundry'ga `cf push` bilan ko'tarib, keyin bo'laklarini Kubernetes'ga ko'chirish.
- Ko'p-tenant SaaS'da har bir tenant uchun alohida namespace va resource quota ajratish.

**Deploy variantini eng yengilidan boshlab baholash.** Qaysi platformaga chiqish qarori to'rt variantni sanab emas, ularni belgilangan TARTIBDA ko'rib hal qilinadi: avval serverless, keyin konteyner va orkestrator, keyin virtual mashina, oxirida tilga xos paket (JAR ni mashinaga qo'yib servis sifatida yuritish). Tartibning mantiqi shu: ro'yxat boshidagi variant operatsion mas'uliyatning ko'pini platformaga beradi, oxiridagisi esa hammasini o'zingizga qoldiradi. Qoida ham shundan chiqadi - talabni qondiradigan eng yengil variant tanlanadi va keyingisiga faqat oldingisi talabni qondirmaganda o'tiladi. Uzoq yashaydigan ulanish, bir sekunddan katta cold start ga chidamaslik yoki maxsus runtime talabi serverless dan konteynerga, mashinaga kirish yoki agent o'rnatish talabi esa konteynerdan virtual mashinaga o'tkazadigan sabablar bo'ladi.

**Ehtiyot bo'ling:** Kubernetes operatsion murakkablikni yo'qotmaydi, faqat uni boshqa joyga ko'chiradi - 3-4 servis uchun oddiy PaaS yoki hatto systemd + VM arzonroq va ishonchliroq. Platformaga juda chuqur bog'lanib qolish (CRD, service mesh annotation'lari, vendor-specific probe'lar) keyinchalik migratsiyani qimmatlashtiradi, shuning uchun ilova kodi platforma API'sini bilmasligi kerak.

**Bulut xizmat modellari: kim nimani boshqaradi:** platformani tanlashdan oldin qaysi darajada ishlayotganingizni aniqlash kerak, chunki "bulut" so'zi o'zi hech narsa aytmaydi. Carnell uchta modelni ovqatlanish bilan taqqoslab ajratadi (Carnell, 1-bob, 13-14-betlar):

- **On-premise:** ovqatni uyda o'zingiz tayyorlaysiz, o'z pechingiz va uydagi masalliq bilan. Hamma ish sizda.
- **IaaS (Infrastructure as a Service):** do'kondan yarim tayyor ovqat olasiz: do'konning oshpazi va pechi bilan tayyorlangan, lekin isitish, uyda yeyish va keyin idishni yuvish sizda. Ya'ni provayder asosiy infratuzilmani beradi, texnologiyani tanlash va yakuniy yechimni qurish esa sizning javobgarligingizda qoladi.
- **PaaS (Platform as a Service):** mas'uliyat baribir sizda, lekin asosiy ishni vendor oladi: idish va mebelni siz qo'yasiz, pech, masalliq va oshpazni restoran beradi.
- **SaaS (Software as a Service):** restoranga borasiz, hamma narsa tayyor. Siz xizmatning passiv iste'molchisisiz: texnologiya tanlashga ta'siringiz ham, infratuzilmani saqlash majburiyatingiz ham yo'q.

Modellarni ajratadigan haqiqiy o'q ikkita: infratuzilmani kim saqlaydi va ilovani qurish uchun qanday texnologiya tanlovi qoladi. Shu o'q bu bo'limdagi qarorni aniqlaydi. O'zingiz boshqaradigan Kubernetes - IaaS ustiga qurilgan o'z platformangiz: node, tarmoq, versiya yangilanishi va orkestratorning o'zi sizda, evaziga texnologiya tanlovi erkin. Boshqarilgan PaaS operatsion yukning katta qismini oladi, lekin ilova platformaning shakliga moslashadi. Shuning uchun "Kubernetes kerakmi" savoli avval "infratuzilma mas'uliyatining qancha qismini o'zimizda ushlab turishimiz kerak" savoliga aylantiriladi.

**Desired state boshqaruvining oldindan sharti:** platforma (Newman
Kubernetes, bulut provayderining autoscaling group i va Nomad ni
nomlaydi) desired state ni o'zi saqlaydi, lekin buning uchun u
instance ni o'zi ko'tara olishi kerak. Shundan birinchi shart
chiqadi: mikroservis instance ini **to'liq avtomatik** deploy
qilish imkoni bo'lishi shart, aks holda desired state haqida gap
ham yo'q. Ikkinchi shart vaqtga tegishli: yangi instance ko'tarilishi
uzoq bo'lsa, bittasi o'lganda bo'shliqni yopish uchun ortiqcha
sig'im ushlab turish kerak, chunki platforma almashtirishni
boshlaydi, lekin yuk shu vaqt ichida qayergadir tushishi kerak.
Uchinchi: desired state ni o'zingiz yozmang. Newman buni vaqtni
yaxshi sarflash deb hisoblamaydi va tushunchani birinchi darajali
qiladigan tayyor platformani olishni tavsiya qiladi; lekin
platformani kiritishni bir necha mikroservis ishlab turgandan keyin
qilish mantiqli, aks holda mikroservis asoslari bilan yangi
texnologiya bir vaqtda ustingizga tushadi. To'rtinchi, va bu amalda
eng ko'p vaqt yeydigan tuzoq: platforma o'lgan instance ni qayta
ko'taradi, shuning uchun ta'mir yoki klasterni o'chirish uchun
avval desired state qoidasini (minimal instance soni, autoscaling
group) to'xtatish kerak. Newman ning o'z keysi: dev klasterni
tungi vaqtga o'chirmoqchi bo'lganda, o'chirilgan har instance
o'rniga yangisi ko'tarilib turgan va bu o'n besh daqiqa davom
etgan.

**Hisoblash platformasi: tanlov qaytarilishi qiyin:** platformani
tanlash lock-in darajasi yuqori qaror va Winters/Manshreck/Wright
sababini Hyrum qonuniga bog'laydi. Jamoalar tanlangan tizimning
hamma xususiyatiga tayanadigan kod yozadi: VM asosidagi yechim
tanlansa, o'z VM obrazlarini sozlaydi; konteyner asosidagi yechim
tanlansa, klaster menejerining API siga to'g'ridan-to'g'ri
murojaat qiladi. Arxitektura instance ni pet kabi ko'rishga yo'l
qo'ysa, jamoalar shunday qiladi, va keyin cattle modeliga o'tish
qiyin bo'ladi. Kitobning misoli tanlovning qanchalik mayda
tafsiloti ham qotib qolishini ko'rsatadi: Borg jamoasi
foydalanuvchi buyrug'ini `bash -c` bilan yurgizar edi, keyin
masshtabda xotira tejash uchun yengilroq `ash` ga o'tdi; ba'zi
jamoalar esa `bash` ni o'z fayl tizimi qatlamida o'z kodiga
almashtirgan bo'lgani uchun ularning xotira iste'moli
o'zgarishdan keyin **oshdi** va o'zgarish qaytarildi. Ikkinchi
sabab: har qanday platforma tanlovi atrofida log, monitoring,
debug, alert, vizualizatsiya, konfiguratsiya tili va interfeys
vositalaridan katta ekotizim o'sadi; platformani o'zgartirsangiz
ularning hammasi qayta yozilishi kerak va o'rta yoki katta
tashkilotda shu vositalarni shunchaki sanab chiqishning o'zi ham
ish. Amaliy natija: ilova kodi platforma API sini bilmasligi
talabiga (yuqoridagi "Ehtiyot bo'ling") atrofdagi vositalar
ro'yxatini yuritish talabi qo'shiladi.

## 22.26 Container image qurish (Container Image Build - Buildpacks, Jib, layered jar, multi-stage)

**Tavsif:** Spring Boot fat jar'ni to'g'ridan-to'g'ri `COPY app.jar` qilib image'ga solish har bir build'da 60+ MB layer'ni qayta yaratadi va cache'ni buzadi. Pattern image'ni o'zgarish tezligi bo'yicha qatlamlarga ajratishni taklif qiladi: avval kam o'zgaruvchi dependency'lar, oxirida tez o'zgaruvchi ilova klasslari. Bu push/pull vaqtini va registry hajmini bir necha barobar kamaytiradi, shuningdek base image'ni markazlashgan holda yangilash va CVE'larni yopish imkonini beradi. Qurish usuli esa Dockerfile'ni qo'lda yozishdan Buildpacks/Jib kabi deklarativ vositalarga o'tadi.

**Spring'da qayerda uchraydi:** Spring Boot 3.x jar'i default holda layered bo'ladi - ichida `BOOT-INF/layers.idx` fayli bor va `java -Djarmode=tools extract --layers --launcher` (Boot 3.3+; undan avval `-Djarmode=layertools extract`) jar'ni `dependencies`, `spring-boot-loader`, `snapshot-dependencies`, `application` kataloglariga ajratadi - bu multi-stage Dockerfile uchun ideal. Cloud Native Buildpacks yo'li: Maven'da `mvn spring-boot:build-image`, Gradle'da `bootBuildImage` task'i Paketo buildpack'lari bilan Dockerfile'siz OCI image yasaydi va `BP_JVM_VERSION`, `BP_NATIVE_IMAGE` kabi env'lar bilan boshqariladi. Google Jib (`com.google.cloud.tools:jib-maven-plugin` / `jib-gradle-plugin`) Docker daemon'siz, reproducible va layer'lari avtomatik ajratilgan image'ni to'g'ridan-to'g'ri registry'ga push qiladi.

**Qo'llanish keyslari:**
- CI'da 50 servis uchun build vaqtini qisqartirish: faqat `application` layer qayta push bo'ladi.
- Jib bilan Docker daemon bo'lmagan Kubernetes-based CI runner'da image qurish.
- Paketo buildpack'larini markazlashgan holda yangilab, barcha servislar JDK patch'ini bitta rebuild bilan olishi.
- Distroless yoki `eclipse-temurin:*-jre-alpine` base image bilan attack surface va image hajmini kamaytirish.
- `bootBuildImage` + `BP_NATIVE_IMAGE=true` bilan native image'ni bitta buyruqda yasash.

**Ehtiyot bo'ling:** Buildpacks qulay, lekin base image va JVM sozlamalari ustidan nazoratni kamaytiradi hamda qurish paytida internet/registry'ga bog'liqlik qo'shadi - qat'iy supply-chain talabi bo'lgan joyda o'z Dockerfile'ingiz shaffofroq. Layered jar'ni to'g'ri ishlatish uchun Dockerfile'da layer'lar tartibi (dependencies oldin, application keyin) buzilmasligi kerak, aks holda cache'dan foyda yo'q.

## 22.27 GraalVM Native Image (GraalVM Native Image)

**Tavsif:** JVM bytecode'ni ahead-of-time kompilyatsiya qilib, ilovani o'z ichiga olgan mustaqil native binary yasaydi: startup 50-100 ms'ga tushadi, RSS bir necha barobar kamayadi, JIT warm-up yo'qoladi. Buning narxi - closed-world assumption: reflection, dynamic proxy, resource yuklash va serializatsiya build vaqtida ma'lum bo'lishi shart, shuning uchun ularni hint'lar bilan e'lon qilish kerak. Peak throughput odatda JIT'li HotSpot'dan pastroq bo'ladi, build vaqti esa daqiqalarga cho'ziladi.

**Spring'da qayerda uchraydi:** Spring Boot 3.x/4.x native'ni birinchi darajali qo'llab-quvvatlaydi: `spring-boot-maven-plugin`'ning `process-aot` goal'i va `org.graalvm.buildtools:native-maven-plugin` (`mvn -Pnative native:compile`) yoki Gradle'da `org.graalvm.buildtools.native` plugin'i. AOT engine bean definition'larni build vaqtida generatsiya qiladi, `RuntimeHintsRegistrar` + `@ImportRuntimeHints` orqali qo'lda hint qo'shiladi, `@RegisterReflectionForBinding` va `@Reflective`/`@ReflectiveScan` esa reflection metadata'sini deklarativ beradi. Testda `@EnabledInNativeImage`, JVM'da esa `spring.aot.enabled=true` bilan AOT yo'lini tekshirish mumkin; Java 17-25 va GraalVM/Liberica NIK bilan ishlaydi.

```java
class PaymentHints implements RuntimeHintsRegistrar {
    @Override
    public void registerHints(RuntimeHints hints, ClassLoader cl) {
        hints.resources().registerPattern("rules/*.json");
        hints.reflection().registerType(LegacyPayload.class,
                MemberCategory.INVOKE_DECLARED_CONSTRUCTORS,
                MemberCategory.ACCESS_DECLARED_FIELDS);
    }
}
```

**Qo'llanish keyslari:**
- Serverless/FaaS (AWS Lambda, Knative) funksiyalarida cold start'ni sekundlardan millisekundlarga tushirish.
- CLI vositalari va scheduled job'larda JVM ko'tarish narxini yo'qotish.
- Scale-to-zero qilinadigan, trafigi pulsatsiyali internal API'lar.
- Edge yoki resurs cheklangan muhitda memory footprint'ni qisqartirish.
- Juda ko'p replica'li servisda umumiy RAM xarajatini kamaytirish.

**Ehtiyot bo'ling:** Reflection'ga tayanadigan kutubxona (eski ORM, dynamic scripting, ba'zi mocking framework'lari) hint'siz runtime'da `ClassNotFoundException` beradi va bu xato faqat native binary'da chiqadi - demak CI'da albatta native test suite kerak. Uzoq ishlaydigan, yuqori throughput'li servis uchun native odatda noto'g'ri tanlov: CDS/AOT cache bilan JVM'da qolish arzonroq.

## 22.28 Sinflar arxivi va AOT cache (CDS / AppCDS / Project Leyden)

**Tavsif:** Startup vaqtining katta qismi klass yuklash, verifikatsiya va linking'ga ketadi. CDS (Class Data Sharing) bu ishni bir marta bajarib, natijani memory-mappable arxivga yozadi; AppCDS buni ilovaning o'z klasslariga ham yoyadi. Project Leyden esa keyingi qadam - AOT cache klass yuklashdan tashqari linking va metod profillarini ham saqlab, startup va warm-up'ni yanada tezlashtiradi. Native image'dan farqi: to'liq JVM dinamikasi, reflection va observability saqlanib qoladi, faqat tezlik oshadi.

**Spring'da qayerda uchraydi:** Spring Boot 3.3+ CDS'ni rasman qo'llab-quvvatlaydi: jar'ni `java -Djarmode=tools extract` bilan ochib, `java -XX:ArchiveClassesAtExit=app.jsa -Dspring.context.exit=onRefresh -jar app.jar` training run'ini bajarasiz (`spring.context.exit=onRefresh` context ko'tarilgach ilovani tark etadi), keyin `-XX:SharedArchiveFile=app.jsa` bilan ishga tushirasiz. JDK 19+ da `-XX:+AutoCreateSharedArchive` arxivni avtomatik yaratadi/yangilaydi. JDK 24'dagi JEP 483 (AOT Class Loading & Linking) va JDK 25'dagi JEP 514/515 `-XX:AOTMode=record|create|on`, `-XX:AOTCache=app.aot`, `-XX:AOTCacheOutput` bilan Leyden AOT cache'ni beradi; Spring Boot 3.5+ buni `spring-boot-maven-plugin` va Paketo buildpack (`BP_JVM_CDS_ENABLED`, AOT cache) darajasida avtomatlashtiradi. CRaC esa `-Dspring.context.checkpoint=onRefresh` va `org.crac.Resource` bilan boshqa, komplementar yo'l.

**Qo'llanish keyslari:**
- Rolling update'da pod'larning tezroq Ready bo'lishi va deploy oynasining qisqarishi.
- Native image'ga o'tish imkoni yo'q, lekin startup bir necha barobar tez bo'lishi talab qilinadigan katta monolit.
- Kubernetes'da CPU limit past bo'lgan pod'da startup timeout'ga tushib qolmaslik.
- CI'da integration test suite'ini ko'p marta JVM ko'tarib ishga tushirish vaqtini kamaytirish.
- Scheduled batch job'larda har safar warm-up to'lashdan qutulish.

**Ehtiyot bo'ling:** Arxiv JDK versiyasi, classpath va GC sozlamalariga bog'liq - ularning biri o'zgarsa arxiv jim-jitlik bilan ishlatilmay qolishi mumkin, shuning uchun `-Xlog:cds` bilan haqiqatan ishlayotganini tekshiring va arxivni image build'ning bir qismi qilib yasang. Training run'ni production trafigi bilan adashtirmang: u faqat context'ni ko'taradi, barcha kod yo'llarini qamrab olmaydi.

## 22.29 JVM'ning container ergonomikasi (JVM Container Ergonomics)

**Tavsif:** JVM default sozlamalarini xost mashina resurslariga qarab tanlaydi; container ichida esa cgroup limitlari haqiqat hisoblanadi. To'g'ri sozlanmasa JVM heap'ni juda katta oladi va `OOMKilled` bo'ladi, yoki haddan tashqari ko'p GC thread va ForkJoinPool parallelism yaratadi. Pattern - heap'ni absolyut MB emas, limitning foizi sifatida berish, CPU limitiga mos GC tanlash va JVM'ga ko'rinadigan processor sonini ongli boshqarish. Shuningdek heap'dan tashqari (metaspace, thread stack, direct buffer, code cache) xotirani ham hisobga olish kerak.

**Spring'da qayerda uchraydi:** JDK 17-25 da `-XX:+UseContainerSupport` default yoqilgan va cgroup v1/v2 limitlarini o'qiydi; amalda `-XX:MaxRAMPercentage=70 -XX:InitialRAMPercentage=70`, `-XX:ActiveProcessorCount=N` va kichik container uchun `-XX:+UseSerialGC` ishlatiladi. Spring Boot buildpack'lari (Paketo) `java-memory-calculator` yordamida `JAVA_TOOL_OPTIONS`'ni avtomatik hisoblaydi va `BPL_JVM_THREAD_COUNT`, `BPL_JVM_HEAD_ROOM` env'lari bilan tuziladi. Ilova tomonida `server.tomcat.threads.max`, `spring.task.execution.pool.*`, `spring.datasource.hikari.maximum-pool-size` qiymatlari ham `Runtime.availableProcessors()` va CPU limitiga mos bo'lishi kerak; Java 21+ virtual thread'lar (`spring.threads.virtual.enabled=true`) platform thread sonini kamaytiradi, lekin CPU limiti muammosini hal qilmaydi.

**Qo'llanish keyslari:**
- `OOMKilled` restart loop'ining sababini topish: `MaxRAMPercentage` + non-heap xotira hisobi.
- 0.5 vCPU limitli sidecar-tipidagi servisda G1 o'rniga SerialGC bilan latency va xotirani yaxshilash.
- Hikari pool va Tomcat thread'larini CPU quota'ga mos kichraytirib, context switch'ni kamaytirish.
- `ActiveProcessorCount` bilan parallel stream va ForkJoinPool'ning haddan ortiq thread yaratishini to'xtatish.
- Actuator `/actuator/metrics/jvm.memory.max` va `jvm.gc.pause` bilan sozlamalar ta'sirini o'lchash.

**Ehtiyot bo'ling:** CPU limit (quota) throttling keltiradi - JVM 8 core ko'rsa-da, cgroup 500m bersa, GC va startup kutilmaganda sekinlashadi; shuning uchun CPU request/limit nisbatiga ehtiyot bo'ling. Heap'ni limitning 90%'iga qo'yish xato: metaspace, thread stack va native buffer'lar uchun 20-25% headroom qoldirish kerak.

## 22.30 Nol to'xtalishli deploy (Zero-Downtime Deployment)

**Tavsif:** Yangi versiyani chiqarishda hech bir request yo'qolmasligi uchun eski va yangi instance'lar qisqa vaqt birga yashaydi, trafik esa faqat haqiqatan tayyor bo'lgan instance'ga yuboriladi. Buning uchun uch mexanizm kerak: aniq readiness signali, graceful shutdown (in-flight request'larni tugatish) va orqaga mos (backward-compatible) ma'lumotlar bazasi migratsiyasi. Shakllari - rolling update, blue/green va canary; ularning har biri rollback tezligi va infratuzilma narxi bo'yicha farq qiladi.

**Spring'da qayerda uchraydi:** `spring-boot-starter-actuator` `LivenessState` va `ReadinessState` ni `ApplicationAvailability` orqali beradi; `AvailabilityChangeEvent.publish(...)` bilan ilova o'zini vaqtincha `REFUSING_TRAFFIC` deb belgilashi mumkin. Graceful shutdown `server.shutdown=graceful` va `spring.lifecycle.timeout-per-shutdown-phase=30s` bilan yoqiladi (Tomcat, Jetty, Netty, Boot 3.x da Undertow ham: hammasida ishlaydi), Kubernetes tomonida `preStop` hook va `terminationGracePeriodSeconds` bu bilan muvofiqlashtiriladi. Schema migratsiyasi uchun Flyway (`spring-boot-starter-flyway` / `FlywayMigrationStrategy`) yoki Liquibase expand-and-contract uslubida ishlatiladi; canary/blue-green esa Argo Rollouts, Flagger yoki Spring Cloud Gateway'ning weighted routing'i bilan amalga oshiriladi.

```java
@Component
class DrainOnShutdown {
    @EventListener(ContextClosedEvent.class)
    void drain(ContextClosedEvent e) {
        AvailabilityChangeEvent.publish(e.getApplicationContext(),
                this, ReadinessState.REFUSING_TRAFFIC);
    }
}
```

**Qo'llanish keyslari:**
- Ish kuni o'rtasida deploy qilish: rolling update + readiness probe bilan 0 xato.
- Ustun qo'shish va o'chirishni ikki relizga bo'lish (expand/contract) orqali DB migratsiyasini xavfsizlashtirish.
- Yangi tartiblash algoritmini 5% trafikda canary qilib, metrikalar yaxshi bo'lsa 100%'ga ko'tarish.
- Kafka consumer'da shutdown paytida offset commit qilib, qayta ishlashni (duplicate) kamaytirish.
- Blue/green bilan bir buyruqda bir necha sekundda rollback qilish imkoniyati.

**Ehtiyot bo'ling:** Readiness probe'ni tashqi bog'liqliklarga (DB, boshqa servis) bog'lash eng keng tarqalgan xato - bitta DB sekinlashganda butun cluster bir vaqtda NotReady bo'lib, o'z-o'zini o'chiradi; liveness'ni esa yengil va deyarli hamisha muvaffaqiyatli qilish kerak. Shuningdek graceful shutdown bekor bo'ladi, agar `preStop` kutish vaqti Service endpoint'lari yangilanishidan qisqa bo'lsa.

## 22.31 Trunk-based development va reliz poyezdlari (Trunk-Based Development & Release Trains)

**Tavsif:** Barcha ishlab chiquvchilar qisqa umrli branch'lar bilan bitta asosiy branch'ga (trunk) kuniga bir necha marta merge qiladi; tugallanmagan funksionallik feature flag ortida yashirin qoladi. Bu merge do'zaxini va uzoq yashovchi release branch'larni yo'q qiladi, integration muammolarini erta ochadi. Release train esa qat'iy jadval bilan (masalan har hafta yoki har oy) "poyezd ketadi": o'z vaqtida tayyor bo'lmagan funksiya keyingi poyezdga qoladi, reliz sanasi esa siljimaydi. Ikkisi birgalikda "katta big-bang reliz" riskini ko'plab kichik, oson rollback qilinadigan relizlarga aylantiradi.

**Spring'da qayerda uchraydi:** Spring ekosistemasining o'zi release train modelida yashaydi - Spring Boot 3.x/4.x minor relizlari va Spring Cloud'ning `spring-cloud-dependencies` BOM'ining kalendar bo'yicha nomlangan versiyalari (`2023.0.x`, `2024.0.x`, `2025.0.x`) muayyan Boot versiyasiga biriktirilgan. Ilova darajasida feature flag'lar `@ConditionalOnProperty`, `@Profile`, `@ConfigurationProperties` + `@RefreshScope` (Spring Cloud Config) bilan, yoki OpenFeature SDK, Unleash, Togglz, FF4j kabi kutubxonalar orqali yoziladi. Trunk'ni yashil ushlab turish uchun `spring-boot-starter-test`, Testcontainers va `@SpringBootTest` slice test'lari CI'da har commit'da ishlaydi.

**Qo'llanish keyslari:**
- 30 kishilik jamoada release branch'lardan voz kechib, kuniga 10+ deploy qilish.
- Yarim tayyor yangi to'lov provayderini `payments.provider.new.enabled=false` flag ortida trunk'ga merge qilish.
- Platform jamoasining Spring Boot BOM yangilanishini butun tashkilot bo'ylab choraklik poyezd bilan tarqatishi.
- Mobil klient bilan bog'liq API o'zgarishini flag bilan yoqib, mobil reliz jadvaliga moslashtirish.
- Flag'ni kill switch sifatida ishlatib, incident vaqtida deploy qilmasdan funksiyani o'chirish.

**Ehtiyot bo'ling:** Feature flag'lar tozalanmasa texnik qarzga aylanadi - har bir flag kodda eksponensial ko'payadigan yo'llar yaratadi, shuning uchun flag'ga egalik va o'chirish muddati belgilanishi shart. Trunk-based ishlash kuchli avtomatlashtirilgan test va tez CI'siz ishlamaydi: yashil bo'lmagan trunk butun jamoani bloklaydi.

**Chiqarish qobiliyati va chiqarish chastotasi ikki boshqa narsa:**
Winters/Manshreck/Wright bu ikkisini ataylab ajratadi. Qiymatning
katta qismini **har kuni chiqara olish qobiliyati** beradi, hatto
siz har kuni chiqarmasangiz ham: bu qobiliyat hujjatlashtirilgan
uzluksiz deploy jarayonini, foydalanuvchi mamnunligi va mahsulot
sog'ligi bo'yicha real vaqtdagi metrikani, nima kiradi va nima
kirmaydi degan aniq siyosatni, production da sozlanadigan binarni,
konfiguratsiyani kod kabi versiya nazoratida ushlashni va dry-run
tekshiruvi, rollback hamda ishonchli patch kabi xavfsizlik
choralarini talab qiladi. Haqiqiy chiqarish chastotasi esa
foydalanuvchi ehtiyojiga qarab ataylab tanlanadi. Qo'shimcha
natija: muntazam va bashorat qilinadigan reliz poyezdi har bir
relizning narxini pasaytiradi, shuning uchun tashlab ketilgan
relizning narxi ham juda past bo'ladi va "bu funksiya uchun relizni
ushlab turamiz" degan bosim yo'qoladi.

**Change-neutral release:** A/B qilish uchun foydalanuvchi bazasi
yetmasa, kitobning tavsiyasi relizni o'zgarishsiz qilish, ya'ni
barcha yangi funksiyalarni flag ostiga qo'yish. Shunda tarqatish
paytida sinaladigan yagona narsa deploy ning barqarorligi bo'ladi.
Buning sababi aniq: yangilanishni surishning o'zi foydalanuvchi
metrikalarini statistik jihatdan sezilarli o'zgartirishi mumkin,
shuning uchun kanareyka yiqilish va barqarorlik haqida yaxshi
ma'lumot beradi, lekin "yangi versiya eskisidan yaxshiroqmi"
degan savolga javob bermaydi. Shu savolga javob kerak bo'lsa,
alohida A/B reliz kerak, ya'ni bir vaqtda yangi versiya va
placebo sifatida eski versiyani qayta chiqarish.

**Release train maqsad emas, o'tish bosqichi:** korpusdagi tavsif
release train ni big-bang relizni mayda relizlarga aylantirish
vositasi sifatida beradi. Newman uni bir qadam oldinga suradi:
release train foydali texnika, lekin uni to'g'ri release-on-demand
ga o'tishdagi **o'tish bosqichi** deb ko'rish kerak, oxirgi maqsad
emas. Sababi deployment coupling: Newman release train jarayoni
ostida hamma servisni, hatto o'zgarmaganlarini ham, birga
chiqaradigan tashkilotlarda ishlagan. Deploy xavf tug'diradi va
xavfni kamaytirish yo'llaridan biri faqat o'zgarishi kerak bo'lgan
narsani o'zgartirish; kichikroq reliz qamrovi xatoning sababini
topishni ham, tuzatishni ham osonlashtiradi (Newman,
*Monolith to Microservices*, 1-bob, 23-bet).

**Branch chegaralari: raqam bilan:** "qisqa umrli branch" ni
o'lchovsiz qoldirmaslik kerak. DORA va Puppet ning 2016 yilgi State
of DevOps tadqiqoti yuqori samaradorlik bilan bog'langan uch
ko'rsatkichni beradi: branch yoki fork ning trunk ga merge
qilinishigacha umri **bir kundan kam**, jami **uchtadan kam** faol
branch va trunk ga **kunlik** merge. Newman shu yerda GitFlow
haqida ham ogohlantiradi: branch ga og'ir yondashuv ochiq kod
dunyosida keng tarqalgan, chunki u ko'p sonli, vaqti kam,
"ishonilmagan" committer lardan keladigan ad hoc hissalar bilan
ishlaydi va ularni kichik "ishonilgan" guruh tekshiradi; yopiq
jamoada esa hamma a'zoda commit huquqi bor, demak ochiq kod uchun
ishlagan narsa kundalik ishda ishlamasligi mumkin. 2019 yilgi
hisobot ikki tomonga umumiy bo'lgan xulosani beradi: qisqa umrli
branch, kichik va o'qiladigan patch hamda o'zgarishlarning
avtomatik testi ikki holatda ham samaradorlikni oshiradi.

## 22.32 Semantik versiyalash va BOM bilan dependency boshqarish (Semantic Versioning & BOM Dependency Management)

**Tavsif:** Semantic Versioning (MAJOR.MINOR.PATCH) versiya raqamini mijoz uchun shartnomaga aylantiradi: MAJOR - buzuvchi o'zgarish, MINOR - orqaga mos yangi funksiya, PATCH - faqat tuzatish. BOM (Bill of Materials) esa o'nlab o'zaro bog'liq kutubxona versiyasini bitta joyda, sinab ko'rilgan to'plam sifatida qotiradi va transitive dependency konfliktlarini ("diamond dependency") oldini oladi. Ikkisi birga katta tashkilotda yangilanishni oldindan bashorat qilinadigan qiladi.

**Spring'da qayerda uchraydi:** Spring Boot `spring-boot-starter-parent` yoki `spring-boot-dependencies` BOM'i yuzlab kutubxona versiyasini boshqaradi; Spring Cloud uchun `spring-cloud-dependencies`, Spring Framework uchun `spring-framework-bom` bor. Gradle'da `implementation(platform("org.springframework.boot:spring-boot-dependencies:3.5.0"))` yoki `io.spring.dependency-management` plugin'i, Maven'da `dependencyManagement` bloki ishlatiladi; versiyani faqat `<spring-kafka.version>` kabi property'ni override qilish bilan o'zgartirish tavsiya etiladi. Ichki kutubxonalar uchun o'z `*-bom` modulini chiqarish, API mosligini `japicmp-maven-plugin` yoki Revapi bilan tekshirish, `maven-enforcer-plugin` (`requireUpperBoundDeps`, `banDuplicateClasses`) va Renovate/Dependabot bilan avtomatik yangilash amalda keng tarqalgan.

**Qo'llanish keyslari:**
- Umumiy `company-platform-bom` chiqarib, 60 servisda Jackson/Netty versiya konfliktini yo'qotish.
- Spring Boot 3.x dan 4.x ga o'tishni BOM versiyasini bitta joyda almashtirish bilan boshlash.
- Ichki `shared-dto` kutubxonasida MAJOR versiya ko'tarilsa, mijozlarga migratsiya oynasi berish.
- `japicmp` ni CI'da gate qilib, PATCH relizda API buzilishini bloklash.
- Renovate bilan PATCH yangilanishlarni avtomatik merge qilib, MINOR/MAJOR'ni qo'lda ko'rib chiqish.

**Ehtiyot bo'ling:** BOM'dan bitta kutubxona versiyasini sababsiz override qilish Spring Boot'ning sinab ko'rilgan kombinatsiyasini buzadi va topilishi qiyin `NoSuchMethodError` keltiradi - override qilsangiz, sababini va qaytarish shartini hujjatlashtiring. SemVer faqat e'lon qilingan va kuzatilgan holda ishlaydi: `0.x` da qolib ketish yoki MAJOR'ni ko'tarishdan qo'rqish mijozlarni yashirin buzuvchi o'zgarishlarga duchor qiladi.

**Release train: Spring Cloud versiyasi Boot versiyasiga ergashmaydi:** Spring Cloud o'nlab mustaqil subloyihadan iborat va ular alohida emas, birga, bitta BOM ostida "release train" sifatida chiqariladi. BOM o'sha chiqarishga kiradigan har bir subloyihaning tekshirilgan versiya raqamini va uchinchi tomon kutubxonalarni ushlaydi, shuning uchun siz subdependency larga versiya yozmaysiz va mos kelmaydigan kombinatsiyadan himoyalanasiz (Carnell, 3-bob, 71-72-betlar). Muhim nuqtasi esa shu: Spring Boot release train dan MUSTAQIL chiqariladi, ya'ni Spring Boot ning har bir versiyasi Spring Cloud ning har bir chiqarishi bilan mos kelmaydi va mosligini Spring Cloud ning o'z sahifasidagi jadvaldan tekshirish kerak. Amaliy qoida: `spring-cloud-dependencies` versiyasini Boot versiyasidan ayrim holda ko'tarmang, ikkisini bitta migratsiya qadamida, moslik jadvaliga qarab almashtiring va `spring-boot-dependencies` bilan `spring-cloud-dependencies` ni bir xil commit da yangilang.

ESLATMA: kitobdagi chiqarish nomlari London metro bekatlari bo'yicha harf tartibida berilgan (Angel, Brixton, Camden; kitob misoli `Camden.SR5`). Spring Cloud keyinchalik bu nomlashdan voz kechib kalendar-semantik versiyaga o'tdi, lekin release train mexanizmi va Boot bilan moslik jadvalini tekshirish talabi o'zgarmagan.

**Eskirish oynasi har kutubxona uchun alohida:** versiyalash
mexanizmidan keyin keladigan savol - eski versiyani qancha vaqt
qo'llab-quvvatlash. Ford va boshqalar global siyosatni soddaroq,
lekin kamroq samarali deb ataydi va sababini aytadi: kutubxonalar
turli tezlikda o'zgaradi. Kitobning misoli ikki chegarani ajratadi:
kam o'zgaradigan `Security.jar` uchun ikki yoki uch versiyani
ushlab turish asosli, haftada o'zgaradigan `Calculators.jar` uchun
esa shu chegara iste'molchini oyda yoki haftada bir marta
yangilashga majbur qiladi, demak o'n versiya oynasi ancha
mantiqli. Global siyosat (kitobning misolida to'rt orqaga versiya)
boshqarish oson, lekin tez o'zgaradigan kutubxona atrofida churn
keltiradi, ya'ni servislarni faqat moslik uchun doimiy qayta
testlash va qayta deploy qilish. Narxi ham aytilgan: har kutubxona
uchun alohida oynani kimdir yuritishi va kuzatishi kerak. Oxirgi
qoida esa har qanday strategiyani bekor qiladi - umumiy koddagi
jiddiy nuqson yoki buzuvchi o'zgarish barcha servisni darhol
oxirgi versiyaga o'tishga majburlaydi. Eskirishning jarayon
tomoni, ya'ni iste'molchini kim va qanday ko'chiradi,
[code-review 37.9](../code-review/37-api-moslik-va-breaking-change-review.md#379-eskirish-jarayoni-advisory-compulsory-va-qaytmaslik)
da.

## 22.33 Runbook'lar (Runbooks)

**Tavsif:** Runbook - ma'lum bir signal yoki incident uchun yozilgan aniq, bajariladigan qadamlar ro'yxati: qanday tasdiqlash, qanday diagnostika qilish, qanday yumshatish va qachon eskalatsiya qilish. Maqsad - "tizimni faqat bitta odam biladi" holatidan chiqish va tungi navbatchining qaror qabul qilish vaqtini qisqartirish. Yaxshi runbook har bir alert'ga bog'langan, nazariyadan emas, haqiqiy buyruq va dashboard havolalaridan iborat bo'ladi va har incidentdan keyin yangilanadi. Oxirgi maqsad - runbook qadamlarini avtomatlashtirib, odam aralashuvini kamaytirish.

**Spring'da qayerda uchraydi:** Spring Boot Actuator runbook'ning asosiy quroli: `/actuator/health` (component'lar bo'yicha detallar), `/actuator/loggers` bilan restart qilmasdan log darajasini `DEBUG`ga ko'tarish, `/actuator/threaddump` va `/actuator/heapdump` bilan diagnostika, `/actuator/env` va `/actuator/configprops` bilan amaldagi konfiguratsiyani tekshirish, `/actuator/metrics` va `/actuator/prometheus` bilan Micrometer metrikalarini olish. Operatsion harakatlarni `@Endpoint`/`@WriteOperation` bilan maxsus actuator endpoint sifatida kodlashtirish mumkin (masalan cache tozalash, scheduler'ni pauza qilish - `/actuator/quartz`, `/actuator/scheduledtasks`). Spring Boot Admin UI bu endpoint'larni jamoa uchun ko'rinadigan qiladi; `management.endpoints.web.exposure.include` va Spring Security bilan ularni qat'iy himoyalash kerak.

**Qo'llanish keyslari:**
- "Kafka consumer lag > 100k" alert'i uchun qadam-baqadam diagnostika va consumer'ni qayta balanslash yo'riqnomasi.
- Hikari pool to'lib qolganda `/actuator/metrics/hikaricp.connections.pending` ni tekshirish va sekin query'ni topish.
- Memory leak gumonida `/actuator/heapdump` olish va saqlash tartibi.
- Deploy'ni rollback qilish aniq buyruqlari va kimdan ruxsat olish kerakligi.
- Yangi navbatchini onboarding qilishda runbook'lar bo'yicha "game day" mashqi o'tkazish.

**Ehtiyot bo'ling:** Eskirgan runbook xavfli - noto'g'ri buyruq incident'ni chuqurlashtiradi, shuning uchun har ishlatilganda tekshirilib, postmortem'da yangilanishi kerak. Actuator'ning `heapdump`, `env`, `shutdown` kabi endpoint'larini himoyalanmagan holda ochish to'g'ridan-to'g'ri xavfsizlik teshigi hisoblanadi.

## 22.34 Muhitlar o'zarosi mosligi (Environment Parity)

**Tavsif:** Dev, test, staging va production muhitlari o'rtasidagi farq qancha katta bo'lsa, "mening mashinamda ishlaydi" turidagi xatolar shuncha ko'p bo'ladi. Pattern bir xil artifact (bitta container image) barcha muhitlarga ketishini, farq esa faqat tashqi konfiguratsiya va maxfiy ma'lumotlarda bo'lishini talab qiladi. Infratuzilma komponentlari ham imitatsiya qilinmaydi: dev'da H2 emas, production'dagi PostgreSQL'ning aynan o'sha versiyasi ishlatiladi. Bu 12-factor app'ning "dev/prod parity" tamoyilining amaliy ko'rinishi.

**Spring'da qayerda uchraydi:** Spring Boot 3.1+ dagi Testcontainers integratsiyasi bu patternning asosiy quroli: `spring-boot-testcontainers` moduli, `@ServiceConnection` annotatsiyasi (`PostgreSQLContainer`, `KafkaContainer`, `RedisContainer` uchun `DataSource`/bootstrap server'larni avtomatik ulaydi) va `@DynamicPropertySource`; lokal ishlab chiqish uchun `@TestConfiguration` + `SpringApplication.from(...).with(...)` bilan `TestcontainersApplication` ko'tariladi. `spring-boot-docker-compose` moduli esa `compose.yaml` ni ilova startida avtomatik ko'taradi va servislarni `Environment`'ga bog'laydi. Konfiguratsiya farqi `application-{profile}.yaml`, `spring.config.activate.on-profile`, `spring.config.import=configtree:/etc/secrets/` va environment variable'lar orqali tashqarida qoladi; Kubernetes tomonida Helm values yoki Kustomize overlay'lari bir xil image'ga turli konfiguratsiya beradi.

**Qo'llanish keyslari:**
- Integration test'larda H2 o'rniga Testcontainers PostgreSQL ishlatib, native SQL va migration xatolarini erta topish.
- Bitta image digest'ini staging'da tasdiqlab, aynan shuni production'ga promote qilish.
- Dev mashinasida `compose.yaml` bilan Kafka, Redis va Postgres'ni bir buyruqda ko'tarish.
- Staging'ni production ma'lumotlarining anonimlashtirilgan nusxasi bilan to'ldirish.
- Helm overlay'lari orqali replica soni va resource limitlaridan boshqa hech narsani farqlamaslik.

**Ehtiyot bo'ling:** "Har muhitga alohida build" anti-pattern: profil bo'yicha turlicha kompilyatsiya qilingan artifact staging'da sinalgan narsa production'ga bormasligini bildiradi. Shu bilan birga to'liq parity qimmat - trafik hajmi va ma'lumot ko'lamini aynan takrorlash ko'pincha imkonsiz, shuning uchun farqlarni ro'yxatga olib, ongli qabul qilish kerak.

## 22.35 Secrets manager integratsiyasi (Secrets Manager Integration)

**Tavsif:** Parol, API key va sertifikatlar kodda, git'da yoki oddiy konfiguratsiya faylida saqlanmaydi: ular markazlashgan secrets manager'da yashaydi va ilova start paytida yoki runtime'da autentifikatsiyadan so'ng oladi. Bu audit, rotatsiya va eng kam imtiyoz (least privilege) ni mumkin qiladi; eng kuchli shakli - dynamic secrets, ya'ni har bir instance uchun qisqa umrli, avtomatik rotatsiya qilinadigan credential. Ilova kodi secret'ning qayerdan kelganini bilmasligi va faqat `@ConfigurationProperties` orqali qiymatni ko'rishi kerak.

**Spring'da qayerda uchraydi:** Spring Cloud Vault (`spring-cloud-starter-vault-config`) secret'larni `Environment`'ga PropertySource sifatida qo'yadi, `spring.cloud.vault.database` esa PostgreSQL/MySQL uchun dynamic credential beradi va `VaultTemplate` to'g'ridan-to'g'ri API kirishini ta'minlaydi. AWS uchun `io.awspring.cloud:spring-cloud-aws-starter-secrets-manager` va `spring.config.import=aws-secretsmanager:/prod/app` sintaksisi, Azure uchun `spring-cloud-azure-starter-keyvault-secrets`, GCP uchun `spring-cloud-gcp-starter-secretmanager` (`${sm://my-secret}` placeholder'i) ishlatiladi. Kubernetes'da eng oddiy va mustahkam yo'l - External Secrets Operator Secret'ni volume qilib mount qiladi, Spring esa `spring.config.import=configtree:/etc/secrets/` bilan o'qiydi; rotatsiyadan keyin yangilanish uchun `@RefreshScope` + Spring Cloud Config `/actuator/refresh` yoki `ContextRefresher` qo'llaniladi.

**Qo'llanish keyslari:**
- DB parolini Vault dynamic secret bilan har soatda avtomatik rotatsiya qilish.
- Git'dan barcha hardcoded key'larni olib tashlab, CI'da secret-scanning gate qo'yish.
- Multi-cloud'da bitta `@ConfigurationProperties` interfeysi ortida turli secret backend'lardan foydalanish.
- TLS sertifikatlarini Key Vault'dan olib, muddati tugashidan avval avtomatik yangilash.
- Audit talabi uchun "kim qaysi secret'ni qachon o'qidi" jurnalini secrets manager'dan olish.

**Ehtiyot bo'ling:** Secrets manager yangi single point of failure yaratadi - u ishlamay qolsa pod'lar ko'tarilmaydi, shuning uchun cache, retry va mavjud ulanishlarni saqlab qolish strategiyasi kerak. Secret'ni `/actuator/env`, log, exception message yoki `toString()` orqali oshkor qilib yuborish juda keng uchraydigan xato: `management.endpoint.env.show-values` ni cheklang va secret'larni `String` emas, `char[]` yoki maxsus tipda ushlab, loglardan chiqarib tashlang.

## 22.36 Hisoblash resurslarini konsolidatsiya qilish (Compute Resource Consolidation)

**Tavsif:** Bu pattern bir nechta kichik va kam yuklangan servis yoki vazifani bitta hisoblash birligiga (bitta JVM process, bitta container yoki bitta node'ga) birlashtirib, infratuzilma xarajatlari va operatsion murakkablikni kamaytiradi. Har bir mikroservis uchun alohida JVM ko'tarish RAM, CPU va litsenziya nuqtai nazaridan qimmat bo'ladi - ayniqsa trafik past bo'lgan "oyiga bir marta ishlaydigan" modullar uchun. Konsolidatsiya qilinganda bir xil hayot sikliga, bir xil scaling profiliga va bir xil xavfsizlik darajasiga ega komponentlar guruhlanadi. Natijada resurs utilizatsiyasi oshadi, lekin izolyatsiya darajasi pasayadi, shuning uchun guruhlash mezonlari ehtiyotkorlik bilan tanlanishi kerak.

**Spring'da qayerda uchraydi:** Spring Boot 3.x/4.x'da bu asosan "modulli monolit" ko'rinishida amalga oshiriladi: bir nechta domen moduli bitta `@SpringBootApplication` ichida alohida Gradle/Maven modul sifatida yashaydi, chegaralar esa Spring Modulith (`@ApplicationModule`, `ApplicationModules.verify()`) yoki `@ComponentScan` filtrlari bilan ushlab turiladi. Bir xil JVM ichida bir nechta mustaqil kontekstni ko'tarish kerak bo'lsa `SpringApplicationBuilder` bilan `parent()`/`child()` kontekst ierarxiyasi ishlatiladi. Resurslarni bo'lishishni boshqarish uchun Spring Boot `spring.task.execution.pool.*` va `spring.task.scheduling.pool.*` konfiguratsiyalari, `@ConfigurationProperties`, hamda Virtual Threads (`spring.threads.virtual.enabled=true`, Java 21+) ishlatiladi - virtual thread'lar bir JVM'da ko'p sondagi bloklanuvchi vazifani arzon ushlab turishga imkon beradi. Profile'lar (`@Profile`, `spring.profiles.active`) orqali bitta artefaktdan turli rollarni (web, worker, scheduler) yoqish mumkin. Kuzatish darajasida Micrometer va Spring Boot Actuator (`/actuator/metrics`, `jvm.memory.used`, `executor.active`) resurslar haqiqatan samarali ishlatilayotganini ko'rsatadi. Konsolidatsiyaning infratuzilma qismi - Kubernetes `requests/limits`, bitta node'da bir nechta pod joylashtirish - Spring'dan tashqarida bo'ladi; Spring ilovasi unga `-XX:MaxRAMPercentage`, `spring.lifecycle.timeout-per-shutdown-phase` va graceful shutdown (`server.shutdown=graceful`) sozlamalari bilan moslashadi.

**Qo'llanish keyslari:**
- Kam trafikli admin paneli, reporting moduli va notification moduli bitta Spring Boot ilovasiga birlashtiriladi, chunki har biri alohida 512 MB RAM'ni behuda egallaydi.
- Startup bosqichidagi tim 8 ta mikroservis o'rniga Spring Modulith asosidagi bitta deploy birligi bilan boshlaydi va keyin kerakli modulni ajratadi.
- Oyda bir marta ishlaydigan bir nechta batch job bitta scheduler ilovasiga yig'iladi va `@Scheduled` hamda Spring Batch `Job`lar sifatida bir JVM'da yuritiladi.
- Ko'p-tenantli SaaS'da har bir mijoz uchun alohida ilova emas, bitta ilova ichida tenant-aware `DataSource` routing (`AbstractRoutingDataSource`) bilan xizmat ko'rsatiladi.
- Bulut xarajatini optimallashtirishda past utilizatsiyali servislar bitta node pool'ga konsolidatsiya qilinadi va Virtual Threads bilan I/O-og'ir yuklar bir JVM'da ushlab turiladi.

**Ehtiyot bo'ling:** Turli scaling profiliga, turli SLA'ga yoki turli xavfsizlik zonasiga tegishli komponentlarni birlashtirish eng keng tarqalgan xato - bitta modulning memory leak'i yoki `OutOfMemoryError`'i butun JVM'ni, demak barcha konsolidatsiya qilingan servislarni o'ldiradi va deploy'lar bir-biriga bog'lanib qoladi. Shuningdek har bir modul uchun alohida thread pool va `Resilience4j` bulkhead ajratmasangiz, bitta sekin tashqi chaqiruv umumiy pool'ni to'ldirib, qolgan modullarni ham to'xtatib qo'yadi.

## 22.37 Har bir servis nusxasi uchun alohida container (Service Instance per Container)

**Tavsif:** Bu pattern har bir servis nusxasini o'z container'i (masalan Docker image) ichida, o'z process va fayl tizimi namespace'ida ishga tushirishni belgilaydi - ya'ni bir container'da aynan bitta servis nusxasi bo'ladi. Shu orqali resurs izolyatsiyasi (CPU, memory limitlari), bog'liqliklarni paketlash (JDK versiyasi, native kutubxonalar) va immutable deployment ta'minlanadi: image bir marta build qilinadi va dev/stage/prod bo'ylab o'zgarmagan holda ko'chadi. Nusxani ko'paytirish image'dan yangi container ko'tarish bilan amalga oshadi, buzilgan nusxa esa tuzatilmaydi, balki almashtiriladi (cattle, not pets). Bu "Service Instance per VM" ga nisbatan tezroq start va zichroq joylashuv beradi, "Multiple Services per Host" ga nisbatan esa ancha kuchli izolyatsiya beradi.

**Spring'da qayerda uchraydi:** Spring Boot 3.x/4.x fat JAR'ini container'ga o'rashning ikki asosiy mexanizmi bor: Cloud Native Buildpacks orqali `./mvnw spring-boot:build-image` (yoki Gradle `bootBuildImage` task'i, `paketobuildpacks/builder-jammy-java-tiny` kabi builder bilan), va layered JAR + qo'lda yozilgan `Dockerfile` - `layertools` (`java -Djarmode=tools -jar app.jar extract --layers`) Docker layer cache'ini samarali qiladi. Image hajmi va start vaqtini keskin kamaytirish uchun GraalVM native image ishlatiladi: Spring Boot AOT (`spring-boot-starter-parent`'dagi `native` profil, `./mvnw -Pnative native:compile`, `@RegisterReflectionForBinding`, `RuntimeHintsRegistrar`), yoki CRaC/Project Leyden asosidagi checkpoint-restore. Container ichida to'g'ri ishlash uchun Spring Boot `server.shutdown=graceful` va `spring.lifecycle.timeout-per-shutdown-phase` bilan SIGTERM'ga javob beradi, Actuator esa `/actuator/health/liveness` va `/actuator/health/readiness` probe'larini beradi (`management.endpoint.health.probes.enabled=true`) - Kubernetes `livenessProbe`/`readinessProbe` aynan shularga ulanadi. Konfiguratsiya tashqaridan environment variable yoki `ConfigMap`/`Secret` orqali keladi (`SPRING_DATASOURCE_URL` kabi relaxed binding, Spring Cloud Kubernetes `spring-cloud-starter-kubernetes-client-config`). JVM container limitlarini `UseContainerSupport` va `-XX:MaxRAMPercentage=75` bilan hisobga oladi. Container orchestration va replica soni Spring'ning o'zida emas - Kubernetes `Deployment`/`HorizontalPodAutoscaler` yoki ECS task definition darajasida bo'ladi; Spring ilovasi unga stateless bo'lish, sessiyani tashqariga chiqarish (Spring Session Redis) va `/actuator` endpoint'lari bilan tayanadi.

**Qo'llanish keyslari:**
- Kubernetes'da har bir mikroservis `Deployment` sifatida ishlaydi, har bir pod ichida bitta Spring Boot container bo'ladi va HPA CPU bo'yicha replica sonini o'zgartiradi.
- CI pipeline'da `bootBuildImage` bilan bitta image build qilinadi va aynan o'sha digest dev, stage, prod'ga ketadi, farq faqat environment variable'larda bo'ladi.
- Serverless yoki scale-to-zero ssenariylarida GraalVM native image'li container 100 ms ichida ko'tarilib, sovuq start muammosini kamaytiradi.
- Bir xil kodbazaning turli versiyalari (v1 va v2 API) bir vaqtda alohida container sifatida ishlab, canary yoki blue-green release amalga oshiriladi.
- Lokal integratsiya testlarida Testcontainers (`@ServiceConnection`, `PostgreSQLContainer`) servis va bog'liqliklarini real container'larda ko'taradi.

**Ehtiyot bo'ling:** Container ichidagi JVM'ga memory limit haqida xabar bermaslik klassik tuzoq - `-XX:MaxRAMPercentage` yoki to'g'ri `requests/limits` sozlanmasa, pod `OOMKilled` bo'lib doimiy restart qiladi, heap esa limitdan katta bo'lib qoladi. Shuningdek container'ga state (yuklangan fayllar, lokal cache, H2 fayl bazasi) yozib qo'yish uni stateless bo'lmagan "pet"ga aylantiradi: har bir restart yoki rescheduling'da ma'lumot yo'qoladi, shuning uchun state tashqi store'ga (S3, Redis, DB) chiqarilishi va graceful shutdown bilan in-flight so'rovlar tugatilishi shart.

## 22.38 Replikatsiyalangan yuk-balanslangan servis (Replicated Load-Balanced Service)

**Tavsif:** Burns bu patternni eng oddiy taqsimlangan shakl deb ataydi: har bir server qolganlariga aynan o'xshash, har biri har qanday so'rovni qabul qila oladi, oldida esa load balancer turadi va trafikni round-robin yoki session stickiness bilan tarqatadi. Replikatsiyaning birinchi sababi masshtab emas, zaxira: Burns hisobiga ko'ra yuqori mavjudlik SLA'sini bitta nusxa bilan ushlab turish uchun reliz butun kunlik downtime byudjetiga sig'ishi kerak bo'ladi, shuning uchun eng kichik servis ham kamida ikki nusxada ishlatiladi. Patternning ikkinchi majburiy qismi - load balancer uchun halol readiness signali: konteyner tirik, lekin bazaga ulanmagan yoki ma'lumotni hali yuklab olmagan bo'lsa, u "tayyor" deb ko'rinmasligi kerak. Burns shuningdek ayni patternning sessiyani kuzatuvchi variantini beradi: so'rovni foydalanuvchi bo'yicha doimiy ravishda bitta nusxaga yo'naltirish (in-memory cache hit rate yoki uzoq davom etadigan muloqot uchun), bu odatda manba va manzil IP'sini xeshlash bilan amalga oshiriladi, NAT sababli tashqi IP'lar uchun esa cookie darajasidagi kuzatish afzal. Nusxa soni o'zgarganda yo'naltirish buzilishini kamaytirish uchun konsistent xeshlash ishlatiladi. Pattern tepasiga ikki chekka qatlam qo'shiladi: caching proxy (hit rate'ni oshirish uchun kam sonli, lekin katta nusxa) hamda rate limiting va SSL termination qiladigan reverse proxy.

**Spring'da qayerda uchraydi:** Kubernetes'da bu `Deployment` + `Service` juftligi, Spring tomonidan esa talab bitta - warm-up tugaguncha readiness bermaslik. Spring Boot Actuator'da buni `ApplicationAvailability` va `AvailabilityChangeEvent.publish(context, ReadinessState.REFUSING_TRAFFIC)` bilan boshqarish mumkin; probe mexanikasi [Health probe'lar](#2219-health-probelar-health-probes-liveness-readiness-startup) da. Sessiyani kuzatish kerak bo'lsa `spring-session-data-redis` bilan holatni tashqariga chiqarish sticky routing'dan afzal, chunki u nusxalarni almashtirishga to'sqinlik qilmaydi. Chekka qatlam uchun rate limiting Spring Cloud Gateway'ning `RequestRateLimiterGatewayFilterFactory` (`spring-cloud-starter-gateway-server-webflux` + Redis) bilan yoki Resilience4j `RateLimiter` bilan ilovaning o'zida yoziladi; limitga urilgan so'rovga Burns aytgandek `429` va qolgan chaqiruvlar sonini ko'rsatuvchi javob header'i qaytariladi. SSL termination odatda Ingress yoki `nginx` qatlamida bajariladi, shuning uchun Spring Boot'da `server.forward-headers-strategy=framework` qo'yib `X-Forwarded-*` header'larini hisobga olish kerak.

```java
@Component
class CatalogWarmUp {

    private final ApplicationContext context;
    private final CatalogLoader loader;

    CatalogWarmUp(ApplicationContext context, CatalogLoader loader) {
        this.context = context;
        this.loader = loader;
    }

    @EventListener(ApplicationReadyEvent.class)
    void warmUp() {
        // load balancer warm-up tugamaguncha bu nusxaga trafik yubormaydi
        AvailabilityChangeEvent.publish(context, ReadinessState.REFUSING_TRAFFIC);
        loader.loadAll();
        AvailabilityChangeEvent.publish(context, ReadinessState.ACCEPTING_TRAFFIC);
    }
}
```

**Qo'llanish keyslari:**
- Stateless REST API'ni kamida ikki nusxada ishlatib, reliz paytida uzilishsiz yangilash.
- Katta ma'lumot to'plamini startup'da yuklab oladigan servisda readiness'ni warm-up tugagach berish.
- Ko'p o'qiladigan sahifalar uchun ilova oldiga caching proxy qatlamini qo'yib, backend yuklamasini kamaytirish.
- Anonim trafikka past, autentifikatsiya qilingan foydalanuvchiga baland rate limit berib, tasodifiy DoS'dan himoyalanish.
- Chekka qatlamda SSL termination qilib, ichki qatlamlarga alohida sertifikat berish va ularni mustaqil yangilash.

**Ehtiyot bo'ling:** Burns caching qatlamini ilova yonidagi sidecar sifatida joylashtirishning kamchiligini aniq ko'rsatadi: cache ilova bilan birga masshtablanadi va har bir nusxa bir xil sahifani saqlaydi, natijada hit rate pasayadi; shuning uchun cache uchun kam sonli, lekin katta xotirali nusxa afzal. Sticky session'ga tayanish esa yashirin holat yaratadi - nusxa yo'qolganda foydalanuvchi sessiyasi ham yo'qoladi va deploy paytida trafik bir tekis tarqalmaydi, shuning uchun sessiyani tashqariga chiqarish birinchi tanlov bo'lishi kerak.

## 22.39 Shardlangan servis (Sharded Service)

**Tavsif:** Replikatsiyalangan servisda har bir nusxa har qanday so'rovga javob bera oladi, shardlangan servisda esa har bir nusxa (shard) so'rovlarning faqat bir qismiga javob beradi; oldida turgan root yoki shard router har so'rovni ko'rib, uni kerakli shard'ga yo'naltiradi. Burns asosiy sababni aniq aytadi: holat bitta mashinaga sig'maydi, shuning uchun shardlash servisni ma'lumot HAJMI bo'yicha masshtablash usuli. Eng ko'rsatuvchi misol - shardlangan cache: replikatsiyalangan cache'da har nusxa taxminan bir xil ma'lumotni saqlaydi va umumiy to'plamning kichik qismi sig'adi, shardlanganda esa har kalit faqat bitta cache'da yashaydi va xotira ancha samarali ishlatiladi. Yo'naltirish shardlash funksiyasi bilan bajariladi: `Shard = ShardingFunction(Req)`, odatda xesh va modulo. Funksiyadan ikki xususiyat talab qilinadi - determinizm (bir so'rov doim bir shard'ga tushsin) va bir tekislik (yuklama shardlar orasida teng bo'linsin). Burns kalit tanlashga alohida to'xtaladi: butun so'rov obyektini xesh qilish noto'g'ri, chunki javobga ta'sir qilmaydigan maydonlar (so'rov vaqti, mijoz IP'si) kalitni behuda maydalaydi; aksincha juda umumiy kalit javobi boshqa bo'lgan so'rovlarni bir shard'ga qo'shib, xato javob beradi. Shard soni o'zgarganda qayta yo'naltirishni kamaytirish uchun konsistent xeshlash ishlatiladi, hot shard paydo bo'lganda esa shard replikatsiyalanadi.

**Spring'da qayerda uchraydi:** Ma'lumot darajasidagi shardlashning to'liq yozuvi [Shardlash / Bo'laklash](10-malumotlarni-boshqarish-va-taqsimlash.md#109-shardlash--bolaklash-sharding--partitioning) da, bu yerda gap serving qatlamidagi shard router haqida. Spring Boot'da shard router rolini odatda ambassador konteyner (Twemproxy, Envoy) bajaradi va ilova `spring.data.redis.host=localhost` bilan ishlaydi; `spring-boot-starter-data-redis` Redis Cluster rejimida (`spring.data.redis.cluster.nodes`) Lettuce'ning o'zi slot hisobini qiladi. Ilova ichida shard tanlash kerak bo'lsa, shardlash funksiyasi oddiy `@Component` sifatida yozilib, `RestClient`/`WebClient` base URL'ini shard bo'yicha tanlaydi; `AbstractRoutingDataSource` esa bir nechta shard DataSource'ini bitta mantiqiy manbaga biriktiradi. Kalit tanlash xatosi Spring tomonida `@Cacheable(keyGenerator = ...)` darajasida ham takrorlanadi, shuning uchun cache kaliti va shard kaliti bir mantiqdan chiqishi kerak. Konsistent xeshlashning o'z yozuvi [Konsistent xeshlash](28-taqsimlangan-malumot-replikatsiya-va.md#286-konsistent-xeshlash-consistent-hashing) da, hot shard bilan kurash esa [Hot key ta'sirini yumshatish](11-keshlash-patternlari.md#1120-hot-key-tasirini-yumshatish-hot-key-mitigation) da.

```java
@Component
class CacheShardRouter {

    private final List<String> shards;

    CacheShardRouter(@Value("${app.cache.shards}") List<String> shards) {
        this.shards = shards;
    }

    String shardFor(String path, String countryCode) {
        // kalitga faqat javobga ta'sir qiladigan maydonlar kiradi:
        // IP va vaqtni butunligicha xesh qilish shard'ni behuda maydalaydi
        int hash = Objects.hash(countryCode, path);
        return shards.get(Math.floorMod(hash, shards.size()));
    }
}
```

**Qo'llanish keyslari:**
- Umumiy hajmi bitta node xotirasiga sig'maydigan render natijalarini shardlangan cache'da saqlash.
- Shard routerni ambassador sifatida joylashtirib, ilova kodini oddiy local ulanish bilan qoldirish.
- Shard kalitiga mamlakat kodini qo'shib, tilga bog'liq javoblarni to'g'ri ajratish.
- Har shard'ni alohida autoscaling qilib, hot shard'ni dinamik ravishda ko'paytirish.
- Ish navbatini shardlab, yangi worker versiyasini bosqichma-bosqich chiqarish va nosozlik qamrovini kamaytirish.

**Ehtiyot bo'ling:** Burns shardlangan cache'ning replikatsiyalanganidan farqli xavfini ta'kidlaydi: foydalanuvchi doim bir shard'ga tushgani uchun o'sha shard yiqilsa, u tiklanmaguncha bu foydalanuvchi uchun cache har safar miss beradi - demak backend sig'imi cache hit rate'ga qarab hisoblanishi kerak, aks holda shard yo'qolganda backend yuklamasi birdan ko'tariladi. Ikkinchi tuzoq - shard sonini `%` modulo bilan hisoblash: shard soni o'zgarishi bilan deyarli barcha kalitlar ko'chadi, shuning uchun o'sadigan tizimda konsistent xeshlash tanlanadi.

## 22.40 Ish navbati tizimi (Work Queue System)

**Tavsif:** Burns ish navbatini batch ishlovning eng oddiy shakli deb ataydi: bajarilishi kerak bo'lgan ish bo'laklari bor, har bir bo'lak qolganlaridan butunlay mustaqil va o'zaro ta'sirsiz ishlanadi, maqsad esa har bo'lakni belgilangan vaqt ichida tugatish, worker sonini shunga qarab ko'paytirib yoki kamaytirib. Patternning asosiy g'oyasi - navbat mantiqining deyarli hammasi bajarilayotgan ishdan mustaqil, shuning uchun u qayta ishlatiladigan konteynerlarga chiqariladi va ilovaga faqat ikki interfeys qoladi. Birinchisi - source container interface: ishlov kerak bo'lgan bo'laklar oqimini beradi va ambassador rolini o'ynaydi, chunki umumiy navbat menejerining so'rovini real manbaga (cloud storage'dagi fayl ro'yxati, Kafka yoki Redis navbati) proksilaydi. Burns bu interfeys uchun oddiy HTTP REST shartnomasini beradi: `GET /api/v1/items` butun ro'yxatni, `GET /api/v1/items/<item-name>` bitta bo'lak tafsilotini qaytaradi; API'da "bajarildi" deb belgilash yo'q, chunki qaysi bo'lak ishlangani hisobini navbat menejerining o'zi yuritadi. Ikkinchisi - worker container interface: u bir martalik chaqiruv, worker navbat menejeri bilan bir konteyner guruhida emas, alohida joylashtiriladi, shuning uchun chaqiruv masofaviy va xavfsizlik talablari qattiqroq. Burns yana versiyalash bo'yicha amaliy qoida beradi: API'ga `v1` ni darhol qo'yish arzon, keyin qo'shish qimmat.

**Spring'da qayerda uchraydi:** Xabarlar darajasidagi o'xshash yozuv [Raqobatlashuvchi Iste'molchilar](16-enterprise-integration-patterns-ii.md#1612-raqobatlashuvchi-istemolchilar-competing-consumers) da; bu yerda gap konteyner darajasidagi shartnoma haqida. Spring Boot'da source interface oddiy `@RestController` bo'ladi va `record` bilan kitobdagi `kind`/`apiVersion`/`items` javob shaklini aynan beradi. Worker tomonida Kubernetes `Job` ichida ishlaydigan Spring Boot ilovasi `ApplicationRunner` yoki Spring Batch `Job` sifatida yoziladi; `spring-cloud-task` esa qisqa yashovchi vazifa uchun `TaskRepository` bilan ijro tarixini yozib boradi. Navbat haqiqiy broker ustida qurilsa, `spring-kafka`'ning `@KafkaListener` `concurrency` parametri yoki `spring-rabbit`'ning `SimpleRabbitListenerContainerFactory.setConcurrentConsumers` worker sonini boshqaradi. Burns bergan dinamik masshtablash hisobi (ishlov vaqtini parallellikka bo'lib, uni yangi bo'laklarning kelish davridan kichik ushlab turish) Micrometer'ning `kafka.consumer.fetch.manager.records.lag` yoki o'z `Gauge`'ingiz orqali o'lchanadi va KEDA yoki HPA custom metrikasiga beriladi.

```java
@RestController
@RequestMapping("/api/v1/items")
class WorkQueueSourceController {

    private final ItemSource source;

    WorkQueueSourceController(ItemSource source) { this.source = source; }

    @GetMapping
    ItemList list() {
        // navbat menejeri qaysi bo'lak ishlanganini o'zi hisoblaydi:
        // bu API faqat mavjud bo'laklarni e'lon qiladi
        return new ItemList("ItemList", "v1", source.names());
    }

    @GetMapping("/{name}")
    Item detail(@PathVariable String name) { return source.detail(name); }
}

record ItemList(String kind, String apiVersion, List<String> items) {}
```

**Qo'llanish keyslari:**
- Object storage'ga tushgan rasm yoki videoni thumbnail qilish uchun bir martalik worker `Job`'larini navbatdan ishga tushirish.
- Manbani almashtirib (S3, NFS, Kafka) bir xil navbat menejerini qayta ishlatish.
- Worker sonini navbat lag'i bo'yicha KEDA bilan avtomatik masshtablash.
- Hisobot generatsiyasini navbatga qo'yib, foydalanuvchi so'rovini bloklamaslik.
- Bir vaqtda yaratiladigan `Job` sonini cheklab, cluster'ni burst yuklamadan saqlash.

**Ehtiyot bo'ling:** Burns parallellikni cheklashning narxini aniq ko'rsatadi: bir vaqtda yaratiladigan ish soni cheklansa resurs sarfi barqarorlashadi, lekin har bo'lakning tugash vaqti uzayadi; agar barqaror yuklama sig'imdan baland bo'lsa navbat hech qachon yetib olmaydi va kechikish cheksiz o'sadi. Shuning uchun ikki metrikani birga kuzatish kerak: yangi bo'laklarning o'rtacha kelish davri va bitta bo'lakning o'rtacha ishlov vaqti. Spring tomonida eng ko'p uchraydigan xato - worker'ni idempotent qilmaslik: `Job` qayta urinishida bo'lak ikkinchi marta ishlanadi.

## 22.41 Hodisaga asoslangan batch ishlov (Event-Driven Batch Processing)

**Tavsif:** Bitta ish navbati bitta kirishni bitta chiqishga o'girish uchun yaxshi, lekin ko'p batch ilovada bir kirishdan bir nechta chiqish yoki ketma-ket bir nechta amal kerak bo'ladi. Shunda navbatlar bir-biriga ulanadi: birining chiqishi ikkinchisining kirishi bo'ladi va yo'naltirilgan asiklik grafda hodisaga javob beradigan workflow hosil bo'ladi, hodisa esa oldingi qadamning tugashi. Burns navbatlarni ulashning besh nomlangan shaklini beradi. Copier bitta oqimni ikki yoki undan ko'p aynan oqimga ko'paytiradi (bir video bir nechta formatga render qilinadi). Filter oqimni mezon bo'yicha kichraytiradi, mos kelmagan bo'laklarni tashlab yuboradi (faqat marketing xabarlariga rozilik bergan foydalanuvchilar). Splitter hech narsani tashlamaydi, ikki xil kirishni mezon bo'yicha ikki alohida navbatga ajratadi (email va SMS xabarnomalari); Burns ta'kidlashicha, splitter'ni copier va ikki filter bilan ham qurish mumkin, lekin splitter ixchamroq shakl. Sharder splitter'ning umumiylashgan shakli: navbatni shardlash funksiyasi bilan teng bo'laklarga bo'ladi, bu ishonchlilik uchun (yangi worker versiyasini bir shard'ga chiqarib sinash) va yuklamani datacenter'lar bo'ylab tarqatish uchun ishlatiladi. Merger copier'ning teskarisi: bir nechta navbatni bitta navbatga qo'shadi (ko'p sondagi repozitoriydan kelgan commit'larni bitta build tizimiga berish).

**Spring'da qayerda uchraydi:** Bu shakllarning xabar darajasidagi yozuvlari EIP bo'limlarida: [Ajratuvchi](15-enterprise-integration-patterns-i-xabarlar.md#1529-ajratuvchi-splitter) va [Agregator](15-enterprise-integration-patterns-i-xabarlar.md#1530-agregator-aggregator). Spring Integration Java DSL ularni to'g'ridan-to'g'ri beradi: copier uchun `.publishSubscribeChannel(...)`, filter uchun `.filter(...)`, splitter uchun `.route(...)` yoki `.split()`, merger uchun bir nechta `IntegrationFlow`'ni bitta `MessageChannel`'ga ulash. Sharder esa `.route(...)` ichida shardlash funksiyasini ishlatish bilan yoziladi va Kafka'da `spring.kafka.producer.properties.partitioner.class` yoki `@SendTo` bilan partitsiya tanlashga tushadi. Spring Cloud Stream'da xuddi shu grafni `spring.cloud.stream.bindings.*.destination` va funksional kompozitsiya (`spring.cloud.function.definition=enrich|filterOptIn`) orqali e'lon qilish mumkin. Filter va splitter mezoni biznes qoidasi bo'lgani uchun ularni alohida bean sifatida yozib test bilan qulflash kerak.

```java
@Bean
IntegrationFlow shippingNotifications() {
    return IntegrationFlow.from("shippedOrders")
        // Copier: bir xil bo'lakni audit navbatiga ham ko'paytiramiz
        .publishSubscribeChannel(p -> p.subscribe(f -> f.channel("auditQueue")))
        // Filter: xabarnomaga rozilik bermaganlar oqimdan chiqadi
        .filter(Order.class, Order::notifyCustomer)
        // Splitter: qolganlari ikki alohida navbatga ajraladi
        .<Order, String>route(Order::channelPreference,
            m -> m.channelMapping("EMAIL", "emailQueue")
                  .channelMapping("SMS", "smsQueue"))
        .get();
}
```

**Qo'llanish keyslari:**
- Yuklangan videoni bir vaqtda bir nechta formatga render qilish uchun copier qo'yish.
- Yangi ro'yxatdan o'tgan foydalanuvchilardan faqat rozilik berganlariga xabar yuborish uchun filter.
- Yuborilgan buyurtmalarni email va SMS navbatlariga splitter bilan ajratish.
- Ish navbatini to'rt shard'ga bo'lib, yangi worker image'ini faqat bitta shard'da sinash.
- Ko'p repozitoriydan kelgan commit'larni merger bilan bitta build navbatiga keltirish.

**Ehtiyot bo'ling:** Burns bu tizimlarning asosiy xavfini aniq aytadi: navbatlar bir-biriga qanday ulanganini ko'rsatadigan umumiy chizma bo'lmasa, tizim qanday ishlayotganini tushunish qiyinlashadi - xuddi hodisaga asoslangan FaaS'dagi kabi. Shuning uchun graf hujjatlashtirilishi va kuzatuvchanlikka chiqarilishi kerak: Spring tomonida bu Micrometer Tracing bilan uchidan uchiga trace va har kanal uchun alohida metrika. Ikkinchi tuzoq - filter mezonini kodga yashirish: rozilik yoki segment qoidasi o'zgarganda jim ravishda boshqa oqim hosil bo'ladi.

## 22.42 Muvofiqlashtirilgan batch ishlov (Coordinated Batch Processing: Join, Reduce)

**Tavsif:** Oldingi pattern navbatlarni bo'lish va ko'paytirish haqida bo'lsa, bu pattern teskari tomon: parallel chiqishlarni qaytadan birlashtirib yig'ma natija chiqarish. Burns eng kanonik misol sifatida MapReduce'ning reduce qismini ko'rsatadi: map qadami ish navbatini shardlash, reduce qadami esa ko'p sonli chiqishni bitta yig'ma javobga keltiradigan muvofiqlashtirilgan ishlov. Join (yoki barrier synchronization) - thread'ga `join` qilishning batch analogi: ish parallel bajariladi, lekin barcha parallel bo'laklar tugamaguncha hech bir natija join'dan chiqmaydi. Burns merge bilan farqni ta'kidlaydi: merge ikki navbat chiqishini shunchaki bitta navbatga aralashtiradi va to'liqlikni kafolatlamaydi, join esa yig'ma statistika hisoblash mumkin bo'lishi uchun ma'lumot to'plamining to'liq ekanini kafolatlaydi. Narxi bor: join keyingi qadamni oldingi qadam butunlay tugashiga bog'laydi, bu parallellikni kamaytiradi va butun workflow kechikishini oshiradi. Reduce boshqacha ishlaydi: u hamma ma'lumot ishlanishini kutmaydi, parallel chiqishlarni optimistik ravishda bosqichma-bosqich birlashtiradi va har qadam chiqishlar sonini kamaytiradi; shakli kirishiga o'xshagani uchun reduce kerak bo'lgancha marta takrorlanadi. Shu sababli reduce map qadami hali davom etayotganda ham boshlanishi mumkin va butun hisob tezroq tugaydi.

**Spring'da qayerda uchraydi:** Spring Batch'da join'ning tabiiy shakli - qadam chegarasi: `JobBuilder.start(mapStep).next(reduceStep)` da `reduceStep` `mapStep` to'liq tugamaguncha boshlanmaydi, ya'ni qadam o'tishi barrier rolini o'ynaydi. Map qismi partitsiyalangan qadam bilan beriladi (`StepBuilder.partitioner(...)` va `TaskExecutor`), uning to'liq yozuvi [Partitsiyalash](20-batch-va-scheduling-patternlari.md#207-partitsiyalash-partitioning---local-remote) da. Reduce qismi `ItemProcessor` va `ItemWriter` zanjirida yoki `StepExecutionContext`'dan `JobExecutionContext`'ga promotion (`ExecutionContextPromotionListener`) orqali yig'iladi. Agar natijani to'liqlik kafolati bilan yig'ish xabar oqimida kerak bo'lsa, Spring Integration `AggregatorSpec`'ning `releaseStrategy` va `correlationStrategy` juftligi aynan join semantikasini beradi; `groupTimeout` esa to'liq to'plam kelmasa nima qilishni belgilaydi. Reaktiv kodda bu `Flux.reduce(...)` va `Mono.zip(...)`, imperativ kodda `Stream.reduce(...)` yoki `CompletableFuture.allOf(...)`.

```java
@Bean
Job wordCountJob(JobRepository repository, Step mapStep, Step reduceStep) {
    return new JobBuilder("wordCount", repository)
        .start(mapStep)      // map: partitsiyalar parallel sanaydi
        .next(reduceStep)    // join: mapStep tugamaguncha bu qadam boshlanmaydi
        .build();
}

@Bean
Step mapStep(JobRepository repository, Step countPagesStep,
             Partitioner pagePartitioner, TaskExecutor executor) {
    return new StepBuilder("mapStep", repository)
        .partitioner("countPagesStep", pagePartitioner)
        .step(countPagesStep)
        .taskExecutor(executor)
        .build();
}
```

**Qo'llanish keyslari:**
- Kunlik hisobotni partitsiyalangan qadamda hisoblab, yig'ma jadvalni keyingi qadamda yozish.
- Barcha bo'laklar tugaganini kafolatlab, keyin yig'ma summani va histogramni chiqarish.
- Hisob-kitob yopilishida to'liqlik kafolati talab qilinadigan solishtirish (reconciliation) job'i.
- Ko'p manbadan kelgan narx fayllarini parallel o'qib, yakuniy narx jadvalini bitta reduce bilan yasash.
- Oraliq natijalarni bosqichma-bosqich reduce qilib, xotirada butun to'plamni ushlab turmaslik.

**Ehtiyot bo'ling:** Join'ning narxi parallellikning yo'qolishi: butun to'plam oldingi qadamdan o'tmaguncha keyingi hisob boshlanmaydi, demak bitta sekin partitsiya butun job'ni ushlab turadi - shuning uchun partitsiya kalitini teng taqsimlanadigan qilib tanlash kerak. Ikkinchi tuzoq - to'liqlik kafolati kerak bo'lmagan joyda join ishlatish: agar yig'ma statistika emas, oddiy oqim kerak bo'lsa, merge yoki bosqichma-bosqich reduce arzonroq va tezroq. Reduce funksiyasi esa assotsiativ bo'lishi shart, aks holda bo'laklarni boshqa tartibda birlashtirish boshqa natija beradi.

## 22.43 Har mikroservisga bitta repozitoriya (One Repository per Microservice, Multirepo)

**Tavsif:** Har mikroservisning kodi o'z manba repozitoriysida turadi; shunda manba o'zgarishi va CI build o'rtasida bir-bir moslik bo'ladi: `User` repozitoriysidagi har o'zgarish faqat `User` build ini qo'zg'atadi va o'tsa deploy qilish mumkin bo'lgan yangi versiya chiqadi. Newman bu patternni monorepo bilan yonma-yon qo'yib, uchinchi, eng yomon variantni ham nomlaydi: bitta repozitoriya plus BITTA umumiy build. Shu uchinchi variantda bir servisdagi bir qatorlik o'zgarish hamma servisni qayta qurdiradi, qaysi artefaktni deploy qilish kerakligini aytib bo'lmaydi va natijada jamoalar hammasini birga deploy qilishga qaytadi; bitta build sinsa esa boshqa hech bir servisga o'zgarish kiritilmaydi (Newman, 7-bob, "Pattern: One Repository per Microservice (aka Multirepo)").

Tanlov kelishuvlari:

- **Multirepo foydasi.** Egalikni repozitoriya darajasida berish mumkin (kuchli egalik modeli uchun zarur), build xaritasi oddiy, va bir nechta repozitoriyada ishlashning og'irligi servis chegarasini himoya qiladi: chegarani qayta-qayta kesib o'tish kerak bo'layotgani chegara noto'g'ri joyda turganining signali.
- **Multirepo narxi.** Repozitoriyalar orasida atomar commit yo'q (hech bo'lmaganda Git da): `Inventory` API sini va uni ishlatadigan `Shipping` ni ikki commit bilan o'zgartirasiz. Newman buni muammo deb tan oladi, lekin uni amalda bosqichli commit bilan hal qiladi (avval API, keyin iste'molchi) va doimiy kesishuvchi o'zgarishni servis chegarasi xatosining ko'rsatkichi deb o'qiydi. Qayta ishlatish esa versiyalangan kutubxona orqali boradi va kutubxonaning yangi versiyasini chiqarish iste'molchi servislarni ham qayta deploy qilishni talab qiladi.
- **Monorepo foydasi va narxi.** Bir nechta servisga tegadigan o'zgarish bitta commit bo'ladi va mayda qayta ishlatish osonlashadi. Lekin atomar commit atomar rollout bermaydi: hammasini birga chiqarish istagi mustaqil deploy printsipini buzadi. Build xaritasi ham murakkablashadi: papkani build ga bog'lash oddiy boshlanish, keyin bir papka bir nechta build ni qo'zg'atadi, umumiy `common` papkasi esa hammasini; katta loyihada bu graf asosidagi build vositalariga (Bazel) olib boradi, va bunday tizimni joriy qilish jiddiy ish.

**Spring'da qayerda uchraydi:** Multirepo da har servis o'z Maven yoki Gradle build iga ega va umumiy narsalar (BOM, ota-pom, umumiy kutubxona) alohida repozitoriyadan versiyalangan artefakt sifatida keladi; shu yerda [22.32](#2232-semantik-versiyalash-va-bom-bilan-dependency-boshqarish-semantic-versioning--bom-dependency-management) dagi versiyalash qoidalari hal qiluvchi bo'ladi. Monorepo da esa Gradle multi-project (`settings.gradle` da `include`) yoki Maven ko'p modulli reaktor ishlatiladi va CI da o'zgargan modulni aniqlash kerak bo'ladi (Gradle build cache plus `--parallel`, yoki modul bo'yicha path filtri). Spring Boot ilovasining o'zi ikki modelda ham bir xil qoladi: farq build va reliz zanjirida, kodda emas. Test pipeline tomoni [testlash hujjatida](../testing/15-ci-cd-da-test-pipeline.md#1513-monorepo-va-multi-modul-loyihada-test-pipeline).

**Qo'llanish keyslari:**
- Har servisga alohida jamoa egalik qiladigan tashkilotda repozitoriya bo'yicha ruxsat va CODEOWNERS.
- Mustaqil deploy talab qilinadigan servislarda build vaqtini faqat o'zgargan servis bilan cheklash.
- Monorepo: kam sonli jamoa va tez-tez kesishuvchi o'zgarish bo'lgan erta bosqich.

**Ehtiyot bo'ling:** Bitta repozitoriya plus bitta umumiy build ni "oddiy boshlanish" deb tanlash eng qimmat yo'l: u lockstep relizni majburlaydi va keyin undan chiqish qiyin. Monorepo tanlansa, papkadan build ga xaritani boshida yozib qo'ying, aks holda `common` papkasiga tegish butun tizimni qayta qurishga aylanadi. Multirepo tanlansa, kesishuvchi o'zgarishlar sonini o'lchab turing: u o'sib borayotgan bo'lsa muammo build da emas, servis chegarasida.

**Monorepo chekkalarda ishlaydi, o'rtada og'riydi:** Newman tanlovni
tashkilot kattaligiga bog'laydi va natija chiziqli emas. Bir
chekkada juda katta, texnologiyaga yo'naltirilgan kompaniyalar
(Google, Microsoft, Facebook, Twitter, Uber) bor: ularda bu
patterndan eng ko'p foyda olish uchun katta resurs ajratish imkoni
mavjud. Ikkinchi chekkada kichik jamoalar bor: 10-20 dasturchi
bilan egalik chegaralarini boshqarish va build jarayonini sodda
ushlab turish monorepo da osonroq. Og'riq nuqtalari o'rtadagi
tashkilotlarda paydo bo'ladi: masshtabi yangi asbob va yangi ish
usullarini talab qiladigan muammolarga yetgan, lekin shu ishlarga
ajratadigan ortiqcha vaqti yo'q. Newman ning o'z tanlovi masshtabda
multirepo, chunki mayda qayta ishlatish va atomar commit ning
foydasi masshtabda chiqadigan muammolardan ustun kelmaydi.
Vaqt o'qidagi tuzoq alohida eslatiladi: kichik boshlangan va
monorepo yaxshi ishlagan tashkilotlar keyinchalik boshqa modelga
o'tishda qiynaladi, chunki monorepo tushunchasi odatga aylanib
qolgan; tashkilot o'sgan sari monorepo ning og'rig'i ham,
migratsiya narxi ham o'sadi va bu sunk cost tuzog'ini keltiradi,
ya'ni "shuncha sarfladik, yana bir oz sarflasak ishlaydi" degan
fikr. Oraliq variant ham bor va u korpusdagi jamoaviy egalik
modeliga mos keladi: monorepo ni bitta jamoa o'z servislari uchun
ishlatishi.

## 22.44 Konteyner shartnomasi: parametr, API va hujjat (Container Contract: Parameters, API, Documentation)

**Tavsif:** Qayta ishlatiladigan konteyner (ayniqsa [sidecar](#2215-sidecar-konteyner-sidecar-container), ambassador va adapter) uch narsa bilan modullashadi va bu uchtasi birga bitta shartnomani tashkil qiladi.

- **Parametrlangan konteyner.** Konteynerni programmadagi funksiya kabi ko'ring va uning parametrlarini sanang: har parametr umumiy konteynerni aniq holatga moslaydigan kirish. Burns ning misoli: SSL sidecar i amalda foydali bo'lishi uchun kamida ikki parametr kerak, sertifikat nomi va `localhost` dagi legacy ilova porti; bu parametrlarsiz bunday sidecar ni keng qo'llash qiyin. Parametrni berishning ikki yo'li bor, env var va komandalar satri, Burns env var ni afzal ko'radi; konteyner ichida esa oddiy shell skript env var larni o'qib konfiguratsiya faylini sozlaydi (Burns, 2-bob, 17-bet).
- **Konteyner API si.** Parametrlar bilan birga konteyner "funksiya" e'lon qilgan bo'ladi, lekin API faqat shu emas: konteyner BOSHQA servislarga qiladigan chaqiruvlar va o'zi beradigan HTTP yoki boshqa API lar ham shartnomaning qismi. Shartnoma iste'molchilarning keyingi versiyada ham ishlashi uchun kerak. Burns breaking change ni uch bosqichda ko'rsatadi: `UPDATE_FREQUENCY` nomini `UPDATE_PERIOD` ga o'zgartirish ochiq buzilish; sekundda son qabul qilgan parametrni `10m`, `5s` kabi matnga o'tkazish ham buzilish, chunki eski qiymat (`10`) yangi sxemada parse bo'lmaydi; eng nozigi esa birlikni jimgina o'zgartirish, ya'ni birliksiz qiymatni avval sekund, keyin millisekund deb o'qish: xato chiqmaydi, lekin konfiguratsiya tekshiruvi keskin tezlashib konfiguratsiya serveriga yuk ortadi, demak bu ham breaking change (Burns, 2-bob, 17-18-betlar).
- **Konteynerni hujjatlashtirish.** Modulli konteynerni hech kim ishlatolmasa, uning moslashuvchanligi behuda. Rasmiy vosita kam, shuning uchun hujjat Dockerfile ning o'zida yoziladi: `EXPOSE` portni e'lon qiladi (shart emas, lekin yozish yaxshi amaliyot) va yonida o'sha portda aynan nima tinglayotganini izoh bilan ko'rsatish kerak; `ENV` parametrlarga default qiymat berib, ularning ma'nosini izohlaydi; `LABEL` esa metadata beradi, masalan maintainer manzili, sahifa va image versiyasi, nomlar esa Label Schema loyihasining umumiy taksonomiyasidan olinadi (Burns, 2-bob, 18-19-betlar).

**Spring'da qayerda uchraydi:** Spring Boot ilovasida env var parametri avtomatik ishlaydi: `SPRING_DATASOURCE_URL` yoki `PROXY_PORT` relaxed binding orqali `spring.datasource.url` va `@ConfigurationProperties` ga tushadi, shuning uchun konteyner shartnomasi amalda `@ConfigurationProperties` sinfining maydonlari bo'ladi. Shu sabab birlik o'zgarishi Spring da ham xuddi shunday xavfli: `Duration` turi `30s` va `PT30S` ni tushunadi, lekin birliksiz `30` ni property ning `@DurationUnit` iga qarab o'qiydi, ya'ni `@DurationUnit` ni o'zgartirish breaking change. Image ni Buildpacks yoki Jib bilan qurganda ham ([22.26](#2226-container-image-qurish-container-image-build---buildpacks-jib-layered-jar-multi-stage)) `LABEL` va `EXPOSE` ni qo'lda bergan ma'qul.

**Qo'llanish keyslari:**
- Bir nechta jamoa ishlatadigan log yoki metrika sidecar ini sertifikat yo'li va port parametrlari bilan chiqarish.
- Konfiguratsiya sinxronizatsiyasi sidecar ida yangilanish davrini env var bilan berish va uning birligini shartnomada muhrlash.
- `LABEL` orqali image versiyasi va egasini yozib, reliz auditini avtomatlashtirish.

**Ehtiyot bo'ling:** Burns ning asosiy ogohlantirishi: konteyner API sidagi buzilish parametr nomini o'zgartirish kabi doim ko'rinadigan bo'lmaydi; birlik, default qiymat va parse qoidasi ham shartnomaning qismi. Shuning uchun sidecar ni versiyalab, o'zgarishni [22.32](#2232-semantik-versiyalash-va-bom-bilan-dependency-boshqarish-semantic-versioning--bom-dependency-management) dagi semantik versiyalash qoidalari bilan belgilang va eski qiymat shaklini hech bo'lmaganda bir reliz davomida qabul qilib turing.

```text
# Sidecar ning shartnomasi Dockerfile da ko'rinadi: port, parametr va metadata.
FROM eclipse-temurin:21-jre-alpine

# Config sinxronizatsiyasi sidecar i shu portda status beradi
EXPOSE 8081

# UPDATE_FREQUENCY: yangilanish davri. QIYMAT BIRLIGI SHARTNOMANING QISMI:
# birliksiz son millisekund deb o'qiladi, `10s` va `PT10S` ham qabul qilinadi.
# Birlikni yoki parse qoidasini o'zgartirish breaking change.
ENV UPDATE_FREQUENCY=30s

# CERT_PATH: SSL sertifikat fayli yo'li. Majburiy, default yo'q.
ENV CERT_PATH=""

LABEL "org.label-schema.vendor"="platform@musicorp.example"
LABEL "org.label-schema.version"="1.4.0"

ENTRYPOINT ["java", "-jar", "/app/config-sync.jar"]
```

```java
// Konteyner shartnomasining Spring tomoni: env var -> @ConfigurationProperties.
// UPDATE_FREQUENCY -> config.sync.update-frequency (relaxed binding).
@ConfigurationProperties(prefix = "config.sync")
@Validated
public record ConfigSyncProperties(

        // @DurationUnit birliksiz qiymat qanday o'qilishini belgilaydi.
        // Uni o'zgartirish - jimgina breaking change.
        @DurationUnit(ChronoUnit.MILLIS)
        @DefaultValue("30s")
        Duration updateFrequency,

        @NotBlank
        String certPath) {
}
```

## 22.45 Avtomatik masshtablash qoidalarini qurish (Autoscaling Policy Design)

**Tavsif:** [22.21](#2221-gorizontal--vertikal-avtomatik-masshtablash-horizontal--vertical-autoscaling)
masshtablash mexanizmini beradi (HPA, VPA, KEDA, metrika tanlovi).
Bu bo'lim qoidalarning o'zini qanday tartibda kiritish va qanday
sinash kerakligi haqida: Newman ning kuzatishi bo'yicha autoscaling
amalda yukka javob berishdan ko'ra ko'proq instance nosozligini
boshqarish uchun ishlatiladi, va ketma-ketlikni buzish qimmat
turadi.

- **Avval nosozlik, keyin yuk.** Autoscaling ni birinchi navbatda
  nosoz instance ni almashtirish uchun yoqib, shu vaqt ichida
  yuk ma'lumotini yig'ing. Bulut provayderining "bu guruhda kamida
  besh instance bo'lsin" qoidasi bittasi o'lganda yangisini
  avtomatik ko'taradi, bu esa yukdan mustaqil va kutilmagan xulq
  bermaydi. Yuk bo'yicha qo'shishga o'tgach, **pastga** tushirishda
  juda ehtiyot bo'lish kerak: ko'p holatda kerakdan ortiq quvvat
  ushlab turish yetishmovchilikdan ancha yaxshi. Operatsion tuzoq
  ham shu qoidadan chiqadi: ta'mir uchun instance larni o'chirishdan
  oldin minimal instance qoidasini vaqtincha to'xtatish kerak, aks
  holda ular qayta ko'tarilaveradi
  ([22.25](#2225-servis-deploy-platformasi-service-deployment-platform---kubernetes-paas)
  dagi desired state sharti).
- **Autoscaling qoidasini yuk testi bilan sinash.** Turli yuk
  shakllarini qayta yarata oladigan yuk testlari to'plami bu yerda
  deyarli majburiy: ular bilan masshtablash qoidalarini sinab
  ko'rasiz. Qoidani sinamasangiz, uni noto'g'ri yozganingizni faqat
  production da bilib olasiz va oqibati og'ir bo'ladi. Testdan
  chiqadigan ikkinchi raqam ham qimmat: qo'shilish vaqti. Yuk
  ortayotgani haqida ogohlantirish bir necha daqiqa oldin kelsa,
  yangi instance ko'tarilishi esa kamida o'n daqiqa olsa, oradagi
  bo'shliqni ortiqcha quvvat bilan yopish kerak (kitobdagi aniq
  misol shu ikki raqam bilan beriladi).
- **Bashorat va reaktiv masshtablashni aralashtirish.** Yuk
  tendensiyasi ma'lum bo'lsa, oldindan masshtablang: kitobning
  misolida tizimning cho'qqisi 9:00 dan 17:00 gacha bo'lsa, qo'shimcha
  instance lar 8:45 da ko'tariladi va 17:15 da o'chiriladi. Buning
  uchun yuk kundan kunga, haftadan haftaga qanday o'zgarishini
  ko'rsatadigan ma'lumot kerak, mavsumiy davri bor biznesda esa ancha
  uzoqqa boradigan tarix kerak. Kutilmagan cho'qqi uchun esa reaktiv
  qoida qo'shiladi. Newman ning misoli yangiliklar sayti: kunlik
  tendensiya aniq (ertalabdan tushgacha o'sadi, keyin pasayadi,
  dam olish kunlari pastroq), lekin katta yangilik kutilmagan va
  tez keladigan cho'qqi beradi.

```yaml
# Jadvalli (bashoratli) va reaktiv qoidani birga ishlatish.
# KEDA: cron scaler minimal darajani cho'qqidan oldin ko'taradi,
# Prometheus scaler kutilmagan cho'qqiga javob beradi.
apiVersion: keda.sh/v1alpha1
kind: ScaledObject
metadata:
  name: orders-api
spec:
  scaleTargetRef:
    name: orders-api
  minReplicaCount: 3                 # nosozlik uchun zaxira
  maxReplicaCount: 30
  cooldownPeriod: 600                # pastga tushishda shoshilmaslik
  advanced:
    horizontalPodAutoscalerConfig:
      behavior:
        scaleDown:
          stabilizationWindowSeconds: 600
  triggers:
    - type: cron                     # bashoratli: cho'qqidan oldin
      metadata:
        timezone: Asia/Tashkent
        start: "45 8 * * 1-5"
        end: "15 17 * * 1-5"
        desiredReplicas: "12"
    - type: prometheus               # reaktiv: kutilmagan cho'qqi
      metadata:
        serverAddress: http://prometheus:9090
        threshold: "50"
        query: sum(rate(http_server_requests_seconds_count{service="orders-api"}[2m]))
```

ESLATMA: yuqoridagi `ScaledObject` dagi aniq qiymatlar
(`minReplicaCount`, `maxReplicaCount`, `cooldownPeriod`,
`desiredReplicas`) korpusning misoli, kitobdan olingan raqam emas.
Kitobdan olingan raqamlar faqat ikkitasi: cho'qqi oralig'i (9:00 dan
17:00 gacha) va unga mos jadval (8:45 da ko'tarish, 17:15 da
tushirish). O'z qiymatlaringizni shu bo'limdagi ikkinchi qoidaga
ko'ra, yuk testi bilan toping.

**Ehtiyot bo'ling:** Jadvalli qoidani reaktiv qoida bilan birga
ishlatganda ikkisi bir xil obyektni qarama-qarshi yo'nalishga tortmasin:
cron qoidasi minimal darajani ko'taradi, so'rov metrikasi esa undan
yuqoriga chiqaradi, ya'ni ikkisi bir xil o'qda emas, biri pol, biri
javob bo'lishi kerak. Ikkinchi xavf: zaxira quvvatning narxi
ko'rinmas bo'lib qoladi, shuning uchun qo'shilish vaqti qisqargan
sari (AOT, CDS, native image -
[22.27](#2227-graalvm-native-image-graalvm-native-image),
[22.28](#2228-sinflar-arxivi-va-aot-cache-cds--appcds--project-leyden))
zaxira darajasini qayta ko'rib chiqish kerak.

## 22.46 Deploy infratuzilmasining xavfsizlik gigiyenasi (Patching and Rebuild Hygiene)

**Tavsif:** [22.3](#223-ozgarmas-infratuzilma-immutable-infrastructure)
o'zgarmas infratuzilmani deploy mexanizmi sifatida beradi; bu bo'lim
o'sha mexanizmning xavfsizlik tomoni, ya'ni nega almashtirish
muntazam bo'lishi kerak va izolyatsiya chegarasi qayerda tugaydi.

- **Ma'lum zaiflikni o'z vaqtida yoping.** Newman 2017 yildagi
  Equifax hodisasini aynan shu qoidaning ahamiyati uchun keltiradi:
  Apache Struts dagi ma'lum zaiflik orqali ruxsatsiz kirish
  olingan, 160 milliondan ortiq odamning ma'lumoti zarar ko'rgan
  va kompaniya 700 million dollarlik kelishuvni to'lagan. Zaiflik
  hodisadan oylar oldin aniqlangan va tuzatuvchi reliz chiqarilgan
  edi, lekin yangilanish qo'llanmagan. Zaiflik ilovaning o'z kodida
  emas, Java web framework ida bo'lgani alohida muhim: uchinchi
  tomon kodi ham patch doirasiga kiradi va masshtabda qaysi servis
  ma'lum zaiflikli kutubxonaga bog'langanini aniqlash juda qiyin,
  shuning uchun bog'liqlik skaneri (Snyk, GitHub code scanning)
  build ning o'ziga ulanadi va topilma build ni yiqitadi
  ([code-review 33.3](../code-review/33-bogliqlik-va-supply-chain-review.md#333-skanerlashni-ci-ga-qoyish)).
- **Patch bitta qatlam emas.** Kubernetes ostida bir nechta qatlam
  turadi va ularning hammasini o'zingiz yuritsangiz, patch
  mas'uliyati ham sizda: mashina, OS, konteyner runtime, klaster
  komponentlari, keyin ilova va uning bog'liqliklari. Boshqariladigan
  xizmat egalik doirasini keskin qisqartiradi, ya'ni patch
  qarzini kamaytirishning eng arzon yo'li ko'pincha arxitektura
  emas, xizmat modeli. Konteyner bu yerda alohida tuzoq beradi:
  biz konteyner nusxasini o'zgarmas deb qaraymiz, lekin konteyner
  ichida ilovadan tashqari operatsion tizim ham bor. Olti oy
  o'zgarmagan konteyner - olti oy qo'llanmagan OS patch i; bundan
  tashqari base image boshqa image ni meros qilib olishi mumkin,
  demak asos image larning ishonchli ekani alohida savol.
- **Serverlarni muntazam qayta qurish bilinmay kirgan hujumchini
  chiqaradi.** Hujum sodir bo'lgach eng muhim ish tizimni ruxsatsiz
  tomonning kirishi olib tashlangan holda qayta ko'tarish, va bu
  har doim oson emas: Newman ning keysida mashinaga rootkit
  o'rnatilgan, u `ls` va `ps` kabi asosiy buyruqlarni izni
  yashirish uchun o'zgartirgan, muammo esa faqat ishlab turgan
  programalarning xeshini rasmiy paketlar bilan solishtirganda
  ko'rinib qolgan, oqibatda server noldan qayta o'rnatilgan.
  Qoida shundan chiqadi: serverni butunlay o'chirib qayta qurish
  qobiliyati nafaqat ma'lum hujumdan keyin, balki **doimiy**
  hujumchining ta'sirini kamaytirishda ham kuchli. Tizimingizda
  zararli tomon borligini bilmasligingiz mumkin, lekin serverlarni
  muntazam qayta qurib va credential larni aylantirib turgan
  bo'lsangiz, u sezdirmasdan qila oladigan ishni keskin
  cheklaysiz. Qobiliyat ikki narsaga tayanadi: avtomatlashtirish
  sifati (har mikroservisni versiya nazoratidagi ma'lumotdan noldan
  deploy va sozlash) va ma'lumot uchun ishonchli tiklash jarayoni.
  Ishlayotganini tekshirishning eng oson yo'li uni ko'p marta
  qilish, ya'ni qayta qurish uchun har deploy da ishlatiladigan
  aynan bitta jarayonni ishlatish - shunda qayta qurish hodisa ham
  bo'lmaydi. Bitta istisno alohida aytilgan: konteyner platformasida
  siz pod larni tez-tez o'chirib qayta yaratasiz, lekin
  **platformaning o'zini** noldan qayta qura olasizmi degan savol
  ochiq qoladi; boshqariladigan Kubernetes da yangi klaster
  ko'tarish qiyin emas, o'zingiz o'rnatgan va yuritgan klasterda esa
  bu arzimas ish emas.

**Ehtiyot bo'ling:** Patch jarayonini `latest` teg bilan
almashtirmang: u yangilanishni avtomatik qiladi, lekin bir vaqtda
rollback ni ham ishonchsiz qiladi
([22.3](#223-ozgarmas-infratuzilma-immutable-infrastructure)).
Base image ni yangilashni alohida jadvalga qo'ying, aks holda ilova
bog'liqliklari yangilanib, OS qatlami qotib qoladi. Credential
aylantirishni qayta qurish jarayonining bir qismi qilish uchun esa
servis sirni qayta o'qiy olishi yoki rolling restart tayyor bo'lishi
kerak ([18.30](18-xavfsizlik-patternlari.md#1830-sirlarni-boshqarish-secrets-management---vault-config-server-encryption)).

## 22.47 Amalda qo'llash

- [ ] Konteyner image'ini tekshiring: qatlamlar ajratilganmi, JAR to'liq nusxalanmayaptimi, base image yangilanadimi.
- [ ] JVM ning cgroup limitlarini hurmat qilayotganini tasdiqlang va heap foizini yozib qo'ying.
- [ ] Konteyner xotira limitini formula bilan hisoblang: heap, metaspace, code cache, thread stack va native zahira.
- [ ] Readiness va liveness probe'lari alohida ekanini va readiness tashqi tizimga bog'lanmaganini tekshiring.
- [ ] Graceful shutdown yoqilganini va `preStop` kechikishi bilan mos kelishini tasdiqlang.
- [ ] Deploy strategiyasini hujjatlashtiring: rolling, blue-green yoki canary. Orqaga qaytish qadamlarini yozib qo'ying.
- [ ] Konfiguratsiya image ichiga qotib qolmaganini tekshiring; har bir muhit uchun qiymat tashqaridan kelishi kerak.
- [ ] Feature flag larni ro'yxatga olib, har biriga yaratilgan sana va o'chirish rejasini qo'shing.
- [ ] Repozitoriya modelini yozib qo'ying: bitta repozitoriya bitta build ga mos kelayaptimi; monorepo bo'lsa papkadan build ga xarita bormi.
- [ ] Qayta ishlatiladigan sidecar lar uchun shartnomani hujjatlashtiring: `EXPOSE`, `ENV` default va izohlari, `LABEL` metadata si; parametr nomi va BIRLIGI o'zgarishi breaking change deb belgilangan.
- [ ] Autoscaling ni avval nosoz instance ni almashtirish uchun yoqib, yuk bo'yicha qoidani ma'lumot yiqqandan keyin kiriting.
- [ ] Masshtablash qoidalarini turli yuk shakllarini yaratadigan yuk testi bilan sinang va qo'shilish vaqtini o'lchang.
- [ ] Ma'lum yuk tendensiyasi bo'lsa jadvalli qoidani kiritib, kutilmagan cho'qqi uchun reaktiv qoidani ustiga qo'ying.
- [ ] Ta'mir oldidan minimal instance va autoscaling qoidasini to'xtatishni runbook ga yozib qo'ying.
- [ ] Base image va OS qatlamini yangilash jadvalini belgilab, bog'liqlik skanerini build ga ulang.
- [ ] Butun servisni (va imkon bo'lsa klasterni) noldan qayta qurishni mashq qilib, vaqtini yozib qo'ying.
- [ ] Konteyner izolyatsiyasi yetarli emasligi mumkin bo'lgan yuklamalarni (boshqalar yozgan kod, plugin) ro'yxatga olib, ular uchun kuchliroq izolyatsiyani tanlang.

## Manbalar

- Sam Newman, *Building Microservices: Designing Fine-Grained Systems*,
  2-nashr, O'Reilly, 2021, 7-bob ("Be Careful About Branches",
  "Pattern: Monorepo", "Where to use this pattern", "Which Approach
  Would I Use?") - 22.31 dagi DORA 2016 State of DevOps chegaralari
  (branch umri bir kundan kam, jami uchtadan kam faol branch, trunk ga
  kunlik merge), GitFlow ning ochiq kod konteksti va 2019 hisobotining
  qisqa patch bo'yicha xulosasi; 22.43 dagi monorepo ning kichik
  (10-20 dasturchi) va juda katta tashkilotda ishlashi, o'rtadagi
  tashkilotdagi og'riq nuqtasi, atomar commit atomar rollout bermasligi
  va sunk cost tuzog'i. Bu nashrning nusxasida barqaror bet raqami
  yo'q, shuning uchun bob va bo'lim nomi ko'rsatilgan
- Sam Newman, *Building Microservices: Designing Fine-Grained Systems*,
  2-nashr, O'Reilly, 2021, 8-bob ("Desired State Management",
  "Prerequisites", "Feature Toggles", "Containers", "Not perfect",
  "Blurred Lines") - 22.25 dagi desired state ning oldindan shartlari
  (to'liq avtomatik deploy, sekin ko'tarilishda zaxira sig'im,
  platformani o'zi yozmaslik, bir necha mikroservisdan keyin kiritish)
  va autoscaling group ni o'chirmasdan klaster o'chirish keysi; 22.10
  dagi konfiguratsiya faylidan boshlash tavsiyasi va foydalanuvchi
  turiga qarab toggle; 22.23 dagi konteyner izolyatsiyasining VM
  darajasida emasligi, ishonchli dastur mezoni hamda Hyper-V va
  Firecracker ning ishga tushish vaqtiga ta'siri. Bu nashrning
  nusxasida barqaror bet raqami yo'q, shuning uchun bob va bo'lim
  nomi ko'rsatilgan
- Sam Newman, *Building Microservices: Designing Fine-Grained Systems*,
  2-nashr, O'Reilly, 2021, 11-bob ("Patching", "Rebuild") va 13-bob
  ("Autoscaling") - 22.46 dagi Equifax Apache Struts keysi (zaiflik
  oylar oldin tuzatilgan, 160 milliondan ortiq odam ma'lumoti, 700
  million dollarlik kelishuv), Kubernetes ostidagi qatlamlar va
  managed xizmatning egalik doirasini qisqartirishi, konteyner
  ichidagi OS patch i va base image ishonchi, rootkit `ls` va `ps`
  ni o'zgartirgani hamda paket xeshini solishtirish, serverlarni
  muntazam qayta qurish va credential aylantirishning doimiy
  hujumchiga ta'sirini cheklashi, platformaning o'zini qayta qurish
  savoli; 22.45 dagi autoscaling ni avval nosozlik uchun yoqish,
  pastga tushirishda ehtiyot, minimal instance qoidasi va ta'mir
  tuzog'i, yuk testi bilan qoidani sinash va qo'shilish vaqti
  bo'shlig'ini zaxira bilan yopish, 9:00-17:00 cho'qqisi uchun 8:45
  va 17:15 jadvali hamda yangiliklar sayti misolida bashorat plus
  reaktiv aralashmasi. Bu nashrning nusxasida barqaror bet raqami
  yo'q, shuning uchun bob va bo'lim nomi ko'rsatilgan
- Sam Newman, *Monolith to Microservices*, O'Reilly, 2019, 1-bob
  (23-bet) - 22.31 dagi release train ning release-on-demand ga
  o'tishdagi o'tish bosqichi ekani, o'zgarmagan servislarni ham
  birga chiqarishning deployment coupling ni saqlashi va kichik
  reliz qamrovining xavfni kamaytirishi
- Titus Winters, Tom Manshreck, Hyrum Wright, *Software Engineering at
  Google*, O'Reilly, 2020, 24-bob ("Striving for Agility: Setting Up a
  Release Train", "Shifting Left: Making Data-Driven Decisions
  Earlier", "Conclusion") va 25-bob ("Choosing a Compute Service") -
  22.31 dagi chiqarish qobiliyatini chastotadan ajratish (qobiliyatning
  o'zi qiymatning katta qismini berishi va u talab qiladigan jarayon,
  metrika, siyosat hamda rollback vositalari), tashlab ketilgan
  relizning narxi pastligi, change-neutral release va kanareyka
  nimaga javob bermasligi; 22.25 dagi hisoblash platformasining
  lock-in darajasi, Hyrum qonuni orqali pet va cattle farqi, `bash`
  dan `ash` ga o'tish keysi va atrofdagi vositalar ekotizimi. Bu
  nashrning qo'limizdagi nusxasida chop etilgan bet raqami yo'q,
  shuning uchun bob va bo'lim nomi ko'rsatilgan
- Neal Ford va boshqalar, *Software Architecture: The Hard Parts*,
  1-nashr, O'Reilly, 2021 (copyright 2022), 8-bob (226-227-betlar) -
  22.32 dagi eskirish oynasini har kutubxona uchun alohida belgilash,
  `Security.jar` uchun ikki-uch va `Calculators.jar` uchun o'n versiya
  misoli, global strategiyaning (to'rt orqaga versiya) churn
  keltirishi va jiddiy nuqsonning har qanday strategiyani bekor
  qilishi
- Chris Richardson, *Microservices Patterns*, 12-bob - mikroservisni deploy qilish: konteyner, orkestrator, serverless
- John Carnell, *Spring Microservices in Action*, 10-bob - servisni bulutga deploy qilish
- Kubernetes hujjati: Deployments. kubernetes/website, commit `2f85f2802e59eb2128543dbfbf114ad641db4be0`, `content/en/docs/concepts/workloads/controllers/deployment.md`. CC BY 4.0. https://github.com/kubernetes/website/blob/2f85f2802e59eb2128543dbfbf114ad641db4be0/content/en/docs/concepts/workloads/controllers/deployment.md
- Kubernetes hujjati: Pod Lifecycle (termination, preStop, grace period). kubernetes/website, commit `2f85f2802e59eb2128543dbfbf114ad641db4be0`, `content/en/docs/concepts/workloads/pods/pod-lifecycle.md`. CC BY 4.0. https://github.com/kubernetes/website/blob/2f85f2802e59eb2128543dbfbf114ad641db4be0/content/en/docs/concepts/workloads/pods/pod-lifecycle.md
- Kubernetes hujjati: Liveness, Readiness va Startup Probes. kubernetes/website, commit `2f85f2802e59eb2128543dbfbf114ad641db4be0`, `content/en/docs/concepts/workloads/pods/probes.md`. CC BY 4.0. https://github.com/kubernetes/website/blob/2f85f2802e59eb2128543dbfbf114ad641db4be0/content/en/docs/concepts/workloads/pods/probes.md
- Kubernetes hujjati: Sidecar Containers. kubernetes/website, commit `2f85f2802e59eb2128543dbfbf114ad641db4be0`, `content/en/docs/concepts/workloads/pods/sidecar-containers.md`. CC BY 4.0. https://github.com/kubernetes/website/blob/2f85f2802e59eb2128543dbfbf114ad641db4be0/content/en/docs/concepts/workloads/pods/sidecar-containers.md
- Kubernetes hujjati: StatefulSets (`StatefulSetRecreateStrategy` feature gate). kubernetes/website, commit `2f85f2802e59eb2128543dbfbf114ad641db4be0`, `content/en/docs/concepts/workloads/controllers/statefulset.md`. CC BY 4.0. https://github.com/kubernetes/website/blob/2f85f2802e59eb2128543dbfbf114ad641db4be0/content/en/docs/concepts/workloads/controllers/statefulset.md
- Kubernetes API default qiymatlari: `SetDefaults_Probe` va `SetDefaults_Deployment`. kubernetes/kubernetes, tag `v1.37.1`, `pkg/apis/core/v1/defaults.go`, `pkg/apis/apps/v1/defaults.go`, `staging/src/k8s.io/api/apps/v1/types.go`. Apache-2.0. https://github.com/kubernetes/kubernetes/blob/v1.37.1/pkg/apis/core/v1/defaults.go
- Spring Boot hujjati: Graceful Shutdown va Actuator Kubernetes probe'lari. spring-projects/spring-boot, tag `v4.1.1`. Apache-2.0. https://github.com/spring-projects/spring-boot/blob/v4.1.1/documentation/spring-boot-docs/src/docs/antora/modules/reference/pages/web/graceful-shutdown.adoc
- Spring Boot kodi: `LifecycleProperties` (`timeout-per-shutdown-phase` default 30s), `ServletWebServerApplicationContext` (`REFUSING_TRAFFIC`). spring-projects/spring-boot, tag `v4.1.1`. Apache-2.0. https://github.com/spring-projects/spring-boot/blob/v4.1.1/core/spring-boot/src/main/java/org/springframework/boot/context/properties/LifecycleProperties.java
- Spring Boot kodi: `ServerProperties.shutdown` default qiymati. spring-projects/spring-boot, tag `v3.4.13` (`GRACEFUL`) va tag `v3.3.13` (`IMMEDIATE`). Apache-2.0. https://github.com/spring-projects/spring-boot/blob/v3.4.13/spring-boot-project/spring-boot-autoconfigure/src/main/java/org/springframework/boot/autoconfigure/web/ServerProperties.java
- Spring Framework kodi: `SmartLifecycle` (to'xtatish teskari tartibda). spring-projects/spring-framework, tag `v6.2.19`. Apache-2.0. https://github.com/spring-projects/spring-framework/blob/v6.2.19/spring-context/src/main/java/org/springframework/context/SmartLifecycle.java
- Brendan Burns, *Designing Distributed Systems: Patterns and Paradigms for Scalable, Reliable Services*, 1-nashr, O'Reilly, 2018, 2-4-boblar (11-38-betlar) - sidecar, ambassador va adapter bir node ichidagi uch pattern sifatida
- Brendan Burns, *Designing Distributed Systems: Patterns and Paradigms for Scalable, Reliable Services*, 1-nashr, O'Reilly, 2018, 5-bob (45-57-betlar) - load balancer uchun readiness probe, sessiyani kuzatuvchi servis va konsistent xeshlash, caching qatlami, rate limiting va SSL termination
- Brendan Burns, *Designing Distributed Systems: Patterns and Paradigms for Scalable, Reliable Services*, 1-nashr, O'Reilly, 2018, 6-bob (59-71-betlar) - shardlash funksiyasi, kalit tanlash xatolari, shardlangan cache'ning hit rate xavfi va hot sharding
- Brendan Burns, *Designing Distributed Systems: Patterns and Paradigms for Scalable, Reliable Services*, 1-nashr, O'Reilly, 2018, 10-bob (109-119-betlar) - source va worker container interfeyslari, `GET /api/v1/items` shartnomasi, worker'ni dinamik masshtablash hisobi
- Brendan Burns, *Designing Distributed Systems: Patterns and Paradigms for Scalable, Reliable Services*, 1-nashr, O'Reilly, 2018, 11-bob (121-131-betlar) - copier, filter, splitter, sharder va merger shakllari
- Brendan Burns, *Designing Distributed Systems: Patterns and Paradigms for Scalable, Reliable Services*, 1-nashr, O'Reilly, 2018, 12-bob (133-141-betlar) - join (barrier synchronization) va reduce, hamda ularning parallellikka ta'siri
- Bilgin Ibryam, Roland Huss, *Kubernetes Patterns: Reusable Elements for Designing Cloud-Native Applications*, 1-nashr, O'Reilly, 2019, 14-17-boblar (125-142-betlar) - init container, sidecar, adapter va ambassador Structural Patterns qismi sifatida
- Bilgin Ibryam, Roland Huss, *Kubernetes Patterns: Reusable Elements for Designing Cloud-Native Applications*, 1-nashr, O'Reilly, 2019, 4-bob (35-40-betlar) - Health Probe: process health check, liveness va readiness ajratmasi
- Bilgin Ibryam, Roland Huss, *Kubernetes Patterns: Reusable Elements for Designing Cloud-Native Applications*, 1-nashr, O'Reilly, 2019, 4-bob (36-bet) - process health check eng oddiy tekshiruv ekani, jarayon tugasa kubelet ning qayta ishga tushirishi, ilova nosozlikni o'zi sezib o'chsa shu yetarli bo'lishi va deadlock uchun liveness probe zarurati
- Brendan Burns, *Designing Distributed Systems: Patterns and Paradigms for Scalable, Reliable Services*, 1-nashr, O'Reilly, 2018, 2-bob (17-19-betlar) - konteynerni funksiya kabi parametrlash va env var ni afzal ko'rish (SSL sidecar uchun sertifikat nomi va port); konteyner API siga parametrlar, boshqa servislarga chaqiruvlar va o'zi beradigan API lar kirishi; `UPDATE_FREQUENCY` nomi, qiymat formati va birligi o'zgarishining uchtasi ham breaking change ekani; Dockerfile da `EXPOSE` izoh bilan, `ENV` default va izoh bilan, `LABEL` va Label Schema nomlari
- Sam Newman, *Building Microservices: Designing Fine-Grained Systems*, 2-nashr, O'Reilly, 2021, 7-bob ("Pattern: One Repository per Microservice (aka Multirepo)", "Pattern: Monorepo") - bitta repozitoriya plus bitta umumiy build ning zarari va lockstep reliz; multirepo da manba va build ning bir-bir mosligi, repozitoriya bo'yicha egalik, atomar commit ning yo'qligi va kesishuvchi o'zgarishning chegara xatosi signali bo'lishi; monorepo da atomar commit atomar rollout bermasligi, papkadan build ga xarita va Bazel kabi graf asosidagi build. Bu nashrning nusxasida barqaror bet raqami yo'q, shuning uchun bob va bo'lim nomlari ko'rsatilgan
- *The Twelve-Factor App* (III. Config, IX. Disposability). heroku/12factor, commit `1385d2c80bac38c25647651f6f5ec769561828dc`, `content/en/config.md`, `content/en/disposability.md`. MIT. https://github.com/heroku/12factor/blob/1385d2c80bac38c25647651f6f5ec769561828dc/content/en/config.md
- John Carnell, *Spring Microservices in Action*, Manning, 2017, 1-bob (13-14, 25-betlar) - IaaS, PaaS va SaaS taksonomiyasi hamda kim nimani boshqaradi savoli; Phoenix server build va deploy patternlari ro'yxatida
- Bilgin Ibryam, Roland Huss, *Kubernetes Patterns: Reusable Elements for Designing Cloud-Native Applications*, 1-nashr, O'Reilly, 2019, 3-bob (31-32-betlar) - Deployment strategiyalari (rolling update, recreate) avtomatik, Blue-Green va Canary ning o'tish tetigi esa inson qaroriga tayanishi; Deployment pod dan boshqa bog'liqlikni (ConfigMap, Secret, boshqa servis) yangilamasligi va qaytarmasligi, ularning relizi yuqori darajadagi skript yoki GitOps bilan boshqarilishi (22.6, 22.14)
- Bilgin Ibryam, Roland Huss, *Kubernetes Patterns: Reusable Elements for Designing Cloud-Native Applications*, 1-nashr, O'Reilly, 2019, 4-bob (36-37-betlar) - sog'liq tekshiruvi ilovaning o'z ichidan emas tashqaridan bajarilishi (ba'zi nosozlik ilovani o'z watchdog i haqida xabar berishdan ham to'sadi) va restart sababni tuzatmasa yiqiladigan liveness probe dan foyda yo'qligi (22.19)
- Bilgin Ibryam, Roland Huss, *Kubernetes Patterns: Reusable Elements for Designing Cloud-Native Applications*, 1-nashr, O'Reilly, 2019, 5-bob (45-bet) - startup va shutdown mantiqini konteyner buyrug'i ichidagi bash skriptga qo'yishning narxi va tanlov zinapoyasi: bash skript, lifecycle hook, init konteyner (kafolat va qayta ishlatish shu tartibda oshadi) (22.18)
- Bilgin Ibryam, Roland Huss, *Kubernetes Patterns: Reusable Elements for Designing Cloud-Native Applications*, 1-nashr, O'Reilly, 2019, 14-bob (125-bet) - initsializatsiyani init konteynerga chiqarishning uch sababi: ilova image ida bo'lmagan asbob va kutubxona, ilova image iga berilmagan huquq, tashqi bog'liqlik bajarilmaguncha startup ni kechiktirish (22.18)
- Bilgin Ibryam, Roland Huss, *Kubernetes Patterns: Reusable Elements for Designing Cloud-Native Applications*, 1-nashr, O'Reilly, 2019, 15-bob (133-bet) - Pod dagi `containers` ro'yxatining birinchi elementi asosiy konteyner hisoblanishi va `kubectl exec` kabi buyruqlar uchun default bo'lishi (22.15)
- Brendan Burns, *Designing Distributed Systems: Patterns and Paradigms for Scalable, Reliable Services*, 1-nashr, O'Reilly, 2018, 2-bob (15-16-betlar) - introspeksiya asbobini har til uchun kutubxona qilish o'rniga PID namespace ni bo'lishadigan sidecar bilan berish va orkestratorning uni hamma ilovaga qo'shishi; kutubxona yo'li ilovaga ko'proq mos tushishi, modul konteynerning umumiyroq bo'lishi va o'z kodini yozish faqat ishlash talablari ekstremal bo'lganda to'g'ri ekani (22.15)
- Brendan Burns, *Designing Distributed Systems: Patterns and Paradigms for Scalable, Reliable Services*, 1-nashr, O'Reilly, 2018, 3-bob (27-bet) - tajribani (A/B) klient yonidagi ambassador bilan yoki klient oldidagi alohida servis bilan qurish, alohida servisning saqlash, masshtablash va monitoring narxi va shundan chiqadigan ajratuvchi shart (22.13)
- Brendan Burns, *Designing Distributed Systems: Patterns and Paradigms for Scalable, Reliable Services*, 1-nashr, O'Reilly, 2018, 4-bob (40-bet) - mavjud konteynerni (masalan MySQL ni) monitoring qo'shish uchun o'zgartirish uni o'zi saqlash majburiyatini keltirishi, adapter konteyner esa upstream image ni asl holida qoldirishi (22.17)
- Chris Richardson, *Microservices Patterns: With examples in Java*, Manning, 2019, 12-bob, 414-bet - deploy variantlarini eng yengilidan boshlab shu tartibda baholash (serverless, konteyner, virtual mashina, tilga xos paket) va talabni qondiradigan eng yengilini tanlash qoidasi (22.25)
- Michael T. Nygard, *Release It! Design and Deploy Production-Ready Software*, 1-nashr, Pragmatic Bookshelf, 2007, 14-bob (246-bet) - konfiguratsiya xossasi tizimning administrator uchun interfeysi ekani va nomni qiymatning tabiati emas funksiyasi bilan berish qoidasi (`hostname` emas, `authenticationServer`) (22.2)
- ESLATMA: `k8s-patterns` ning 1-nashri 2019-yilda chiqqan va undagi `apiVersion` qiymatlarining ko'pi hozirgi Kubernetes da yo'q, shuning uchun bu bobga kitobdan faqat tamoyil va mexanizm olingan, `apiVersion` ko'chirilmagan
- ESLATMA: 22.2 dagi Spring kalit misollari, 22.15 dagi `kubectl logs` diagnostikasi va 22.25 dagi serverless dan konteynerga o'tkazadigan aniq sabablar ro'yxati shu korpusning amaliy qo'shimchasi, kitoblardan olingan emas
- John Carnell, *Spring Microservices in Action*, Manning, 2017, 3-bob (71-72-betlar) - Spring Cloud release train va BOM, Spring Boot ning release train dan mustaqil chiqishi
- John Carnell, *Spring Microservices in Action*, Manning, 2017, 10-bob (308-bet) - Phoenix server patternining ikki foydasi (drift ni ochish, tiklanmaydigan holatni topish) va Chaos Monkey bilan tekshirish
- ESLATMA: Carnell ning nusxasi 1-nashr (2017) va misollari virtual server image hamda o'sha davr Spring Cloud chiqarish nomlari (Camden) bilan berilgan. Qoidalarning mohiyati saqlanib, zamonaviy nomlar bilan yozilgan; kitobning asl shakli tegishli joyda ESLATMA bilan ko'rsatilgan

---

[&larr; 21. Observability patternlari](21-observability-patternlari.md) · [Mundarija](README.md) · [23. Testing patternlari &rarr;](23-testing-patternlari.md)
