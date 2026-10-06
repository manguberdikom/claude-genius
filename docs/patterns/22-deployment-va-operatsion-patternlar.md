<!-- doc: patterns | chapter: 22 | part:  -->

[Barcha hujjatlar](../../README.md) / [Dizayn patternlar](README.md)

> Holat: AI yozgan, inson tekshirmagan.

# 22. Deployment va operatsion patternlar (Deployment & Operations Patterns)

<details>
<summary>Bu bobdagi 38 bo'lim</summary>

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
- [22.38 Amalda qo'llash](#2238-amalda-qollash)

</details>



Deployment va operatsion patternlar - bu kod yozilib bo'lgandan keyin boshlanadigan, lekin arxitektura qarorlariga eng kuchli ta'sir qiladigan qatlam: ilova qanday paketlanadi, konfiguratsiya qayerdan keladi, yangi versiya ishlab chiqarish muhitiga qanday chiqadi va noto'g'ri ketganda qanday orqaga qaytariladi. Spring Boot ilovasini "ishlaydigan" qilish oson, ammo uni kuniga o'n marta, tushkunliksiz (zero-downtime) va xavfsiz tarzda relizga chiqarish mumkin bo'ladigan qilib loyihalash - bu allaqachon arxitektorning vazifasi. Bu kategoriyadagi patternlar deploy jarayonini kod bilan bir qatorda versiyalanadigan, takrorlanadigan va qaytarib olinadigan muhandislik artefaktiga aylantiradi. Shu bilan birga ular arxitekturaga qattiq talablar qo'yadi: statelessness, backward-compatible ma'lumotlar bazasi migratsiyalari, kuzatuvchanlik (observability) va konfiguratsiyaning artefaktdan to'liq ajratilishi.

## 22.1 O'n ikki faktorli ilova (Twelve-Factor App)

**Tavsif:** Heroku tomonidan shakllantirilgan va bugun cloud-native standartga aylangan 12 ta tamoyil to'plami: bitta kod bazasi, aniq deklarativ bog'liqliklar, muhitdan keladigan konfiguratsiya, backing service'larni almashtiriladigan resurs sifatida ko'rish, build/release/run bosqichlarining qat'iy ajratilishi, stateless process'lar, port binding, gorizontal masshtablash, tez ishga tushish va graceful shutdown, dev/prod paritet, log'larni event stream sifatida stdout'ga yozish va admin vazifalarini bir martalik process sifatida bajarish. Muammosi - an'anaviy "application server'ga WAR tashlash" modeli konteyner va orkestratorlarda qayta-qayta buziladi; 12-faktor shu modelni almashtiradi. Natijada ilova o'zini qayerda ishlayotganini bilmaydigan, almashtiriladigan birlikka aylanadi.

**Spring'da qayerda uchraydi:** Spring Boot 3.x/4.x bu tamoyillarni deyarli standart holatda beradi: embedded Tomcat/Netty orqali port binding, `application.yml` + `Environment` + `@ConfigurationProperties` orqali tashqi konfiguratsiya, Maven/Gradle `spring-boot-starter-*` orqali deklarativ bog'liqliklar. `spring-boot-starter-actuator` build/release ajratilishini `/actuator/info` (git/build ma'lumotlari `BuildProperties`, `GitProperties`) va Kubernetes probe'lari (`management.endpoint.health.probes.enabled=true`, `/actuator/health/liveness`, `/actuator/health/readiness`) bilan qo'llab-quvvatlaydi. Graceful shutdown uchun `server.shutdown=graceful` va `spring.lifecycle.timeout-per-shutdown-phase`; stateless process uchun session'ni Redis'ga chiqarish - `spring-session-data-redis`; log'lar Logback'ning `ConsoleAppender` orqali stdout'ga; admin process'lar `ApplicationRunner`/`CommandLineRunner` yoki Spring Batch job'lari sifatida. Dev/prod paritetini Testcontainers (`spring-boot-testcontainers`, `@ServiceConnection`) ta'minlaydi, build/run ajratilishini esa `spring-boot-maven-plugin:build-image` (Cloud Native Buildpacks).

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

**Spring'da qayerda uchraydi:** Kubernetes `Deployment`ning standart `strategy.type: RollingUpdate` (`maxSurge`, `maxUnavailable`) strategiyasi; uning to'g'ri ishlashi butunlay Spring Boot'ning probe'lariga bog'liq - `management.endpoint.health.probes.enabled=true` bilan `/actuator/health/liveness` va `/actuator/health/readiness`, Spring Boot `AvailabilityChangeEvent`/`ReadinessState` orqali ichki holatni e'lon qiladi. In-flight so'rovlar yo'qolmasligi uchun `server.shutdown=graceful` + `spring.lifecycle.timeout-per-shutdown-phase: 30s` va `preStop` hook; foydalanuvchi sessiyasi pod'dan tashqarida - `spring-session-data-redis`. Sxema o'zgarishi Flyway bilan expand/contract tartibida chiqariladi, Kafka consumer'lar uchun esa yangi va eski deserializer mosligi (Avro/Protobuf schema evolution, `spring-kafka`) tekshiriladi.

**Qo'llanish keyslari:**
- Kuniga bir necha marta chiqadigan oddiy microservice relizlari uchun standart strategiya.
- Yuqori replica soni bilan ishlaydigan stateless REST API'ni tushkunliksiz yangilash.
- Faqat konfiguratsiya (ConfigMap) o'zgarganda pod'larni bosqichma-bosqich qayta ishga tushirish.
- Resurs cheklangan muhitda blue-green'ning ikki barobar xarajatidan qochish.
- Avtomatik `kubectl rollout undo` bilan tez qaytarish siyosatini o'rnatish.

**Ehtiyot bo'ling:** Readiness probe'ni liveness bilan bir xil qilib qo'yish yoki probe'ni warm-up tugashidan oldin "yashil" qilish - reliz paytida 5xx xatolarining asosiy sababi. Orqaga mos bo'lmagan DB migratsiyasi yoki API shartnomasi bilan rolling update ishlamaydi: reliz oynasida ikki versiya bir vaqtda jonli, shuning uchun har bir o'zgarish N va N-1 versiyalar bilan mos bo'lishi kerak.

## 22.9 Qayta yaratish usuli bilan joylashtirish (Recreate Deployment)

**Tavsif:** Eng sodda strategiya: barcha eski instance'lar to'xtatiladi, keyin yangi versiya ishga tushiriladi. Natijada qisqa, ongli ravishda qabul qilingan tushkunlik (downtime) oynasi paydo bo'ladi, lekin hech qachon ikki versiya bir vaqtda ishlamaydi. Bu orqaga mos bo'lmagan ma'lumotlar bazasi migratsiyalari, yagona-faol (singleton) komponentlar va eski litsenziya cheklovlari bo'lgan holatlarda eng xavfsiz va eng tushunarli yo'l.

**Spring'da qayerda uchraydi:** Kubernetes'da `strategy.type: Recreate` (yoki `replicas: 1` bilan StatefulSet) ko'rinishida; Spring tomonida bu strategiya ko'pincha Flyway/Liquibase migratsiyasini `initContainer` yoki alohida Job sifatida bir marta bajarishga bog'lanadi (`spring.flyway.enabled=false` ilovada, migratsiya alohida qadamda). Yagona-faol komponentlar: Quartz'ni klaster rejimisiz ishlatuvchi `spring-boot-starter-quartz` scheduler'lari, `@Scheduled` job'lar, Spring Batch `JobLauncher`, `@KafkaListener` bilan bitta partition'ga bog'langan consumer'lar. Tushkunlik oynasini qisqartirish uchun tez ishga tushish muhim - Spring Boot 3.x AOT, GraalVM native image yoki lazy initialization (`spring.main.lazy-initialization=true`) yordam beradi.

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

**Ehtiyot bo'ling:** Destruktiv migratsiyalar (ustun o'chirish, `NOT NULL` qo'shish, tur o'zgartirish) rollback'ni imkonsiz qiladi - avval expand, keyin contract bosqichini alohida release'larda bajaring. Ikkinchi tuzoq: rollback hech qachon sinalmagan bo'lsa, u inqiroz paytida ishlamaydi; uni release checklist'ida muntazam mashq qilish kerak.

## 22.15 Sidecar konteyner (Sidecar Container)

**Tavsif:** Asosiy ilova konteyneriga yordamchi funksiyani alohida konteyner sifatida biriktirib, uni bitta Pod ichida yonma-yon ishlatish patterni. Ikki konteyner network namespace'ni (localhost) va kerak bo'lsa volume'ni birga ishlatadi, lekin mustaqil ravishda build qilinadi, versiyalanadi va yangilanadi. Bu cross-cutting vazifalarni (log yig'ish, proxy, konfiguratsiya sinxronizatsiyasi, metrika eksporti) ilova kodidan ajratib olishga imkon beradi. Natijada polyglot tizimda bir xil infratuzilma imkoniyatlari barcha tillarga bir xil tarzda beriladi.

**Spring'da qayerda uchraydi:** Spring Boot ilovasi Pod'da Envoy (Istio `istio-proxy`) yoki Linkerd proxy bilan birga ishlaganda, ilova faqat `http://localhost:...` ga murojaat qiladi va mTLS, retry, circuit breaking sidecar'da bajariladi - bu holda `spring-cloud-starter-circuitbreaker-resilience4j`'ni dublikat qilmaslik kerak. Log sidecar'lari (Fluent Bit, Vector) uchun Spring Boot'da `logging.file.name` bilan shared `emptyDir` volume'ga yoziladi yoki Logback'ning `LogstashEncoder`'i (net.logstash.logback) bilan JSON format beriladi. Konfiguratsiya uchun Vault Agent Injector sidecar fayl yozadi, Spring esa `spring.config.import=file:/vault/secrets/application.yaml` yoki `spring-cloud-vault` bilan o'qiydi. Kubernetes 1.29+ da `initContainers` ichida `restartPolicy: Always` bilan rasmiy "native sidecar" mavjud.

**Qo'llanish keyslari:**
- Istio sidecar orqali Spring Boot servislari o'rtasida kodga tegmasdan mTLS yoqish.
- Fluent Bit sidecar bilan ilova loglarini markazlashgan Elasticsearch/Loki'ga uzatish.
- Vault Agent sidecar bilan DB parolini muntazam rotatsiya qilib fayl orqali berish.
- JMX/metrikalarni Prometheus formatiga o'giruvchi exporter sidecar (legacy ilovalar uchun).
- Config file'ni Git repodan muntazam pull qiluvchi `git-sync` sidecar.

**Ehtiyot bo'ling:** Har bir sidecar Pod'ning CPU/memory sarfini va startup vaqtini oshiradi - yuzlab replica'da bu jiddiy xarajat, shuningdek sidecar ilovadan oldin tayyor bo'lmasa, startup'da connection refused xatolari paydo bo'ladi (native sidecar yoki `holdApplicationUntilProxyStarts` bilan hal qilinadi). Sidecar'ni mikroservisga aylantirib, unga biznes logikasi joylashtirish anti-pattern.

## 22.16 Ambassador konteyner (Ambassador Container)

**Tavsif:** Tashqi servisga chiqish murakkabligini alohida konteynerga chiqarib, ilova faqat `localhost` orqali oddiy ulanish qiladigan sidecar turi. Ambassador service discovery, TLS termination, connection pooling, sharding, retry va rate limiting kabi vazifalarni o'z ichiga oladi. Ilova uchun tashqi dunyo bitta statik local endpoint'ga aylanadi, bu esa test va lokal ishlab chiqishni osonlashtiradi. Sidecar'dan farqi: ambassador aynan chiquvchi (egress) trafikka proxy bo'lib xizmat qiladi.

**Spring'da qayerda uchraydi:** Cloud SQL Auth Proxy yoki AWS RDS Proxy ambassador sifatida ishlaganda Spring Boot'ning `spring.datasource.url` qiymati `jdbc:postgresql://localhost:5432/db` bo'lib qoladi va IAM autentifikatsiyasi proxy'da bajariladi. Istio'da egress uchun `ServiceEntry` + `DestinationRule` bilan sidecar ambassador rolini bajaradi, Spring'dagi `RestClient`/`WebClient` esa oddiy HTTP yuboradi. Redis cluster yoki Memcached uchun Twemproxy/Envoy local port beradi, `spring-boot-starter-data-redis` esa `spring.data.redis.host=localhost` bilan ishlaydi. Shuningdek Kafka uchun local proxy (masalan Envoy'ning Kafka filter'i) ishlatilganda `spring.kafka.bootstrap-servers=localhost:9092` qoladi.

**Qo'llanish keyslari:**
- Cloud SQL Proxy bilan ilovaga DB parolini bermasdan IAM orqali ulanish.
- Legacy Spring ilovasini o'zgartirmasdan tashqi API'larga mTLS bilan chiqarish.
- Redis shardlarini ambassador ichida taqsimlab, client kodni oddiy saqlash.
- Tashqi provayder API'siga chiqishda markazlashgan rate limiting va retry qo'yish.
- Lokal development'da ambassador'ni mock serverga almashtirib integratsiya testlari o'tkazish.

**Ehtiyot bo'ling:** Ambassador qo'shimcha network hop keltiradi va o'zi single point of failure bo'lib qolishi mumkin - uning health check'i, timeout'i va resurs limitlari ilovaning timeout'laridan qisqaroq/muvofiq sozlanishi kerak. Ikki joyda (ilovada ham, ambassador'da ham) retry yoqilsa, retry storm va kutilmagan kechikish kuchayishi yuzaga keladi.

## 22.17 Adapter konteyner (Adapter Container)

**Tavsif:** Ilovaning nostandart chiqishini (log formati, metrika, health ma'lumoti) tashqi tizim kutgan yagona standart formatga o'giruvchi sidecar turi. Ambassador chiquvchi trafikni normallashtirsa, adapter ilovadan tashqariga ko'rinadigan interfeysni normallashtiradi. Bu heterogen (turli til va framework'dagi) servislarni bitta monitoring va logging platformasiga arzon narxda ulashga imkon beradi. Ilova kodi o'zgarmaydi - moslashtirish infratuzilma qatlamida bajariladi.

**Spring'da qayerda uchraydi:** Spring Boot 3.x'da Micrometer `PrometheusMeterRegistry` (`micrometer-registry-prometheus`) metrikani `/actuator/prometheus` orqali o'zi beradi, shuning uchun adapter asosan legacy yoki non-Spring komponentlar uchun kerak bo'ladi: `jmx_exporter` JMX'ni Prometheus formatiga, `statsd_exporter` StatsD'ni Prometheus'ga o'giradi (Spring tomonida alternativa - `micrometer-registry-statsd`). Log tomonida Fluent Bit/Vector adapter sifatida plain text Logback chiqishini JSON'ga parse qiladi; Spring'ning o'zida bu `logging.structured.format.console=ecs|logstash|gelf` (Spring Boot 3.4+) bilan ilova ichida ham bajarilishi mumkin. OpenTelemetry Collector esa `opentelemetry-spring-boot-starter` yuborgan ma'lumotni turli backend formatlariga moslashtiruvchi adapter rolini o'ynaydi.

**Qo'llanish keyslari:**
- Legacy JVM ilovasidan JMX metrikalarni `jmx_exporter` bilan Prometheus'ga chiqarish.
- Har xil til'dagi servislar loglarini bitta ECS/JSON schema'ga keltirish.
- OpenTelemetry Collector orqali trace'larni bir vaqtda Jaeger va Datadog'ga yuborish.
- Eski ilovaning `/status` HTML javobini standart health formatiga o'girib Kubernetes probe'ga berish.
- Vendor-specific audit loglarni markazlashgan SIEM kutgan formatga normallashtirish.

**Ehtiyot bo'ling:** Spring Boot allaqachon Micrometer va structured logging beradigan joyda adapter qo'shish ortiqcha murakkablik va ikki marta transformatsiya (format yo'qotish) demakdir - avval ilovaning nativ imkoniyatlarini tekshiring. Adapter'da parse qoidalari log formati o'zgarganda jim buziladi, shuning uchun format shartnomasini test bilan qulflash kerak.

## 22.18 Init konteyner (Init Container)

**Tavsif:** Asosiy konteynerlar ishga tushishidan oldin to'liq bajarilib tugaydigan, bir martalik tayyorlov vazifalarini o'tkazuvchi konteyner. Kubernetes init konteynerlarni ketma-ket ishga tushiradi va har biri muvaffaqiyatli tugamaguncha keyingisi boshlanmaydi; xato bo'lsa Pod `restartPolicy`ga qarab qayta uriniladi. Shu sababli u dependency kutish, schema migration, fayl yuklab olish, ruxsatlarni to'g'rilash kabi ishlar uchun ideal. Natijada asosiy ilova image'i toza va yagona vazifaga mo'ljallangan bo'lib qoladi.

**Spring'da qayerda uchraydi:** Eng keng tarqalgan keys - Flyway yoki Liquibase migratsiyasini init konteynerda alohida ishga tushirib, ilova replica'larida esa `spring.flyway.enabled=false` (yoki `spring.liquibase.enabled=false`) qilib qo'yish; shunda bir nechta replica bir vaqtda migration qilishga urinmaydi. Migratsiyani Flyway/Liquibase CLI image'i yoki Spring Boot ilovasining o'zini maxsus profil bilan ishga tushirish orqali bajarish mumkin. Konfiguratsiya va sertifikatlarni oldindan tortib olish uchun Vault Agent init mode, `git-sync` yoki `busybox` skriptlari ishlatiladi, Spring esa `spring.config.import=file:/config/app.yaml` bilan o'qiydi. Kubernetes 1.29+ dan boshlab `restartPolicy: Always` bilan init konteyner "native sidecar" bo'lib ham ishlaydi.

**Qo'llanish keyslari:**
- Flyway migratsiyasini init konteynerda bir marta bajarib, 20 replica'da race'ni oldini olish.
- PostgreSQL yoki Kafka tayyor bo'lishini kutib turuvchi `wait-for-it` skripti.
- Vault'dan secret'larni `emptyDir` volume'ga tortib olib, ilovaga fayl sifatida berish.
- Shared volume'dagi fayllar egasi/ruxsatini (`chown`) ilova non-root user'i uchun to'g'rilash.
- Statik asset yoki ML modelini S3/GCS'dan yuklab olib, ilova startup'ini tezlashtirish.

**Ehtiyot bo'ling:** Init konteyner har Pod restartida qaytadan ishlaydi, shuning uchun u idempotent va tez bo'lishi shart - uzoq migratsiya rolling update'ni sekinlashtiradi va `terminationGracePeriod`/probe sozlamalari bilan ziddiyat keltirishi mumkin. Migratsiyani init konteynerga ko'chirsangiz, backward compatible schema (expand-contract) qoidasiga qat'iy rioya qilish zarur, aks holda eski va yangi Pod'lar bir vaqtda ishlayotganda xato beradi.

## 22.19 Health probe'lar (Health Probes: Liveness, Readiness, Startup)

**Tavsif:** Orkestratorga ilovaning ishlayotgani (liveness), trafik qabul qilishga tayyorligi (readiness) va hali ishga tushayotgani (startup) haqida mashina o'qiy oladigan signal berish patterni. Liveness muvaffaqiyatsiz bo'lsa konteyner restart qilinadi, readiness muvaffaqiyatsiz bo'lsa Pod Service endpoint'laridan chiqariladi (lekin restart bo'lmaydi), startup probe esa sekin ishga tushadigan ilovada liveness'ni vaqtincha bloklab turadi. To'g'ri ajratilgan probe'lar rolling update, autoscaling va graceful shutdown'ning asosidir.

**Spring'da qayerda uchraydi:** Spring Boot Actuator `/actuator/health/liveness` va `/actuator/health/readiness` endpointlarini beradi; Kubernetes muhitida ular avtomatik yoqiladi yoki `management.endpoint.health.probes.enabled=true` bilan majburan yoqiladi. `ApplicationAvailability`, `LivenessState` va `ReadinessState` interfeyslari orqali holatni kodda o'qish, `AvailabilityChangeEvent.publish(context, ReadinessState.REFUSING_TRAFFIC)` bilan o'zgartirish mumkin. Custom tekshiruvlar `HealthIndicator`/`ReactiveHealthIndicator` implementatsiyasi bilan yoziladi, `management.endpoint.health.group.readiness.include=db,redis` orqali guruhlanadi. Probe endpoint'ini asosiy portdan ajratish uchun `management.server.port` ishlatiladi.

**Qo'llanish keyslari:**
- Kubernetes `readinessProbe` uchun `/actuator/health/readiness` ni ko'rsatib, warm-up tugaguncha trafik yubormaslik.
- Deadlock'ka tushgan ilovani `livenessProbe` bilan aniqlab avtomatik restart qilish.
- JVM va Hibernate sekin ishga tushadigan katta monolitda `startupProbe` bilan `failureThreshold` ni oshirish.
- Kafka consumer lag kritik bo'lganda custom `HealthIndicator` bilan readiness'ni `DOWN` qilish.
- Load balancer uchun `management.server.port=8081` da alohida health porti ochish.

**Ehtiyot bo'ling:** Liveness probe'ga tashqi bog'liqliklarni (DB, boshqa servis) qo'shish eng keng tarqalgan xato - DB qisqa vaqt ishlamasa, butun kluster restart tsikliga tushib ketadi; tashqi bog'liqliklar faqat readiness'ga tegishli. `initialDelaySeconds`/`timeoutSeconds` juda qisqa bo'lsa, yuklama paytida soxta restartlar boshlanadi, juda uzun bo'lsa nosoz Pod uzoq vaqt trafik oladi.

## 22.20 Nazorat ostida to'xtatish (Graceful Shutdown)

**Tavsif:** `SIGTERM` signalini olgandan keyin yangi so'rovlarni qabul qilishni to'xtatib, ishlayotgan so'rovlar va task'larni tugatib, resurslarni toza yopib chiqish patterni. Bu rolling update, scale-in va spot instance uzilishlarida 5xx xatolari va yarim bajarilgan tranzaksiyalarni oldini oladi. To'g'ri ishlashi uchun ketma-ketlik muhim: avval readiness'ni `DOWN` qilish, load balancer endpoint'ni olib tashlashini kutish, keyin server'ni drain qilish. Shutdown muddati orkestratorning `terminationGracePeriodSeconds` qiymatidan qisqa bo'lishi shart.

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

**Ehtiyot bo'ling:** `terminationGracePeriodSeconds` Spring'ning shutdown timeout'idan kichik bo'lsa, Kubernetes `SIGKILL` yuborib, graceful shutdown ma'nosini yo'qotadi - bu qiymatlarni doim birga sozlang. Ikkinchi tuzoq: readiness'ni `DOWN` qilmasdan darhol drain boshlash, chunki load balancer bir necha soniya hali trafik yuborib turadi.

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

**Ehtiyot bo'ling:** Kubernetes operatsion murakkablikni yo'qotmaydi, faqat uni boshqa joyga ko'chiradi - 3-4 servis uchun oddiy PaaS yoki hatto systemd + VM arzonroq va ishonchliroq. Platformaga juda chuqur bog'lanib qolish (CRD, service mesh annotation'lari, vendor-specific probe'lar) keyinchalik migratsiyani qimmatlashtiradi, shuning uchun ilova kodi platforma API'sini bilmasligi kerak.

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
- Native image'ga o'tish imkoni yo'q, lekin startup 2-3 barobar tez bo'lishi kerak bo'lgan katta monolit.
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

## 22.38 Amalda qo'llash

- [ ] Konteyner image'ini tekshiring: qatlamlar ajratilganmi, JAR to'liq nusxalanmayaptimi, base image yangilanadimi.
- [ ] JVM ning cgroup limitlarini hurmat qilayotganini tasdiqlang va heap foizini yozib qo'ying.
- [ ] Konteyner xotira limitini formula bilan hisoblang: heap, metaspace, code cache, thread stack va native zahira.
- [ ] Readiness va liveness probe'lari alohida ekanini va readiness tashqi tizimga bog'lanmaganini tekshiring.
- [ ] Graceful shutdown yoqilganini va `preStop` kechikishi bilan mos kelishini tasdiqlang.
- [ ] Deploy strategiyasini hujjatlashtiring: rolling, blue-green yoki canary. Orqaga qaytish qadamlarini yozib qo'ying.
- [ ] Konfiguratsiya image ichiga qotib qolmaganini tekshiring; har bir muhit uchun qiymat tashqaridan kelishi kerak.
- [ ] Feature flag larni ro'yxatga olib, har biriga yaratilgan sana va o'chirish rejasini qo'shing.

---

[&larr; 21. Observability patternlari](21-observability-patternlari.md) · [Mundarija](README.md) · [23. Testing patternlari &rarr;](23-testing-patternlari.md)
