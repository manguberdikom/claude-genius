<!-- doc: patterns | chapter: 25 | part:  -->

[Barcha hujjatlar](../../README.md) / [Dizayn patternlar](README.md)

> Holat: AI yozgan, inson tekshirmagan.

# 25. Anti-patternlar (Anti-Patterns)

<details>
<summary>Bu bobdagi 84 bo'lim</summary>

- [25.1 Xudo obyekt (God Object)](#251-xudo-obyekt-god-object)
- [25.2 Spagetti kod (Spaghetti Code)](#252-spagetti-kod-spaghetti-code)
- [25.3 Lava oqimi (Lava Flow)](#253-lava-oqimi-lava-flow)
- [25.4 Oltin bolg'a (Golden Hammer)](#254-oltin-bolga-golden-hammer)
- [25.5 Qayiq langari (Boat Anchor)](#255-qayiq-langari-boat-anchor)
- [25.6 O'lik kod (Dead Code)](#256-olik-kod-dead-code)
- [25.7 Nusxa-ko'chirma dasturlash (Copy-Paste Programming)](#257-nusxa-kochirma-dasturlash-copy-paste-programming)
- [25.8 Sehrli sonlar va satrlar (Magic Numbers / Strings)](#258-sehrli-sonlar-va-satrlar-magic-numbers--strings)
- [25.9 Qattiq kodlash (Hard-Coding)](#259-qattiq-kodlash-hard-coding)
- [25.10 Vaqtidan oldin optimizatsiya (Premature Optimization)](#2510-vaqtidan-oldin-optimizatsiya-premature-optimization)
- [25.11 Kargo kulti dasturlash (Cargo Cult Programming)](#2511-kargo-kulti-dasturlash-cargo-cult-programming)
- [25.12 Yo-Yo muammosi (Yo-Yo Problem)](#2512-yo-yo-muammosi-yo-yo-problem)
- [25.13 Arvoh obyekt (Poltergeist)](#2513-arvoh-obyekt-poltergeist)
- [25.14 Istisnolarni yutib yuborish (Exception Swallowing)](#2514-istisnolarni-yutib-yuborish-exception-swallowing)
- [25.15 Oqib Chiquvchi Abstraksiya (Leaky Abstraction)](#2515-oqib-chiquvchi-abstraksiya-leaky-abstraction)
- [25.16 Interfeys Shishishi (Interface Bloat)](#2516-interfeys-shishishi-interface-bloat)
- [25.17 Ketma-ket Bog'liqlik (Sequential Coupling)](#2517-ketma-ket-bogliqlik-sequential-coupling)
- [25.18 Siklik Bog'liqlik (Circular Dependency)](#2518-siklik-bogliqlik-circular-dependency)
- [25.19 Primitivlarga Berilish (Primitive Obsession)](#2519-primitivlarga-berilish-primitive-obsession)
- [25.20 Begona Ma'lumotga Havas (Feature Envy)](#2520-begona-malumotga-havas-feature-envy)
- [25.21 Sochma Jarrohlik (Shotgun Surgery)](#2521-sochma-jarrohlik-shotgun-surgery)
- [25.22 Uzun Parametrlar Ro'yxati (Long Parameter List)](#2522-uzun-parametrlar-royxati-long-parameter-list)
- [25.23 G'ildirakni Qaytadan O'ylab Topish (Reinventing the Wheel)](#2523-gildirakni-qaytadan-oylab-topish-reinventing-the-wheel)
- [25.24 Ichki Platforma Effekti (Inner-Platform Effect)](#2524-ichki-platforma-effekti-inner-platform-effect)
- [25.25 Spekulyativ Umumiylik / Ortiqcha Injinerlik (Speculative Generality / Over-engineering)](#2525-spekulyativ-umumiylik--ortiqcha-injinerlik-speculative-generality--over-engineering)
- [25.26 Singleton'dan Suiiste'mol / Statik Yopishqoqlik (Singleton abuse / Static Cling)](#2526-singletondan-suiistemol--statik-yopishqoqlik-singleton-abuse--static-cling)
- [25.27 Satr Bilan Tiplash (Stringly Typed)](#2527-satr-bilan-tiplash-stringly-typed)
- [25.28 Mantiqiy Qiymat Ko'rligi (Boolean Blindness)](#2528-mantiqiy-qiymat-korligi-boolean-blindness)
- [25.29 Maydonga Injeksiya (Field Injection)](#2529-maydonga-injeksiya-field-injection)
- [25.30 O'z-o'ziga Chaqiruv Proxy'ni Buzishi (Self-invocation breaking @Transactional / @Cacheable)](#2530-oz-oziga-chaqiruv-proxyni-buzishi-self-invocation-breaking-transactional--cacheable)
- [25.31 Public Bo'lmagan Metodda @Transactional (@Transactional on Non-Public Methods)](#2531-public-bolmagan-metodda-transactional-transactional-on-non-public-methods)
- [25.32 View Ichida Ochiq Sessiya (Open Session in View - anti-pattern)](#2532-view-ichida-ochiq-sessiya-open-session-in-view---anti-pattern)
- [25.33 API'da JPA Entity'larini Fosh Qilish (Exposing JPA Entities in API)](#2533-apida-jpa-entitylarini-fosh-qilish-exposing-jpa-entities-in-api)
- [25.34 Semiz Controller (Fat Controller)](#2534-semiz-controller-fat-controller)
- [25.35 Anemik Domen Modeli (Anemic Domain Model - anti-pattern)](#2535-anemik-domen-modeli-anemic-domain-model---anti-pattern)
- [25.36 ApplicationContext.getBean() Service Locator Sifatida (ApplicationContext.getBean() as Service Locator)](#2536-applicationcontextgetbean-service-locator-sifatida-applicationcontextgetbean-as-service-locator)
- [25.37 Aylanali Bean Bog'liqliklari (Circular Bean Dependencies)](#2537-aylanali-bean-bogliqliklari-circular-bean-dependencies)
- [25.38 Juda Keng Component Scanning (Over-broad Component Scanning)](#2538-juda-keng-component-scanning-over-broad-component-scanning)
- [25.39 Profile Tarqoqligi (Profile Sprawl)](#2539-profile-tarqoqligi-profile-sprawl)
- [25.40 Hamma Narsa Uchun @SpringBootTest (@SpringBootTest for Everything)](#2540-hamma-narsa-uchun-springboottest-springboottest-for-everything)
- [25.41 Hammasini Tutuvchi Exception Handler (Catch-all Exception Handler)](#2541-hammasini-tutuvchi-exception-handler-catch-all-exception-handler)
- [25.42 Reactive Pipeline Ichida Bloklash (Blocking in Reactive Pipeline)](#2542-reactive-pipeline-ichida-bloklash-blocking-in-reactive-pipeline)
- [25.43 N+1 so'rovlar (N+1 Queries)](#2543-n1-sorovlar-n1-queries)
- [25.44 Yo'q @Version (Missing @Version)](#2544-yoq-version-missing-version)
- [25.45 Production DB testlari uchun H2 (H2 for Production-DB Tests)](#2545-production-db-testlari-uchun-h2-h2-for-production-db-tests)
- [25.46 Cheklanmagan connection pool / noto'g'ri pool o'lchami (Unbounded Connection Pool / Wrong Pool Size)](#2546-cheklanmagan-connection-pool--notogri-pool-olchami-unbounded-connection-pool--wrong-pool-size)
- [25.47 Sezgir ma'lumotni log'ga yozish (Logging Sensitive Data)](#2547-sezgir-malumotni-logga-yozish-logging-sensitive-data)
- [25.48 Singleton bean ichida mutable state (Mutable State in Singleton Beans)](#2548-singleton-bean-ichida-mutable-state-mutable-state-in-singleton-beans)
- [25.49 Executor sozlanmagan @Async (@Async Without Executor Configuration)](#2549-executor-sozlanmagan-async-async-without-executor-configuration)
- [25.50 rollbackFor'siz checked exception (Checked Exception Without rollbackFor)](#2550-rollbackforsiz-checked-exception-checked-exception-without-rollbackfor)
- [25.51 Remote chaqiruvni qamrab olgan tranzaksiya (Transaction Spanning Remote Calls)](#2551-remote-chaqiruvni-qamrab-olgan-tranzaksiya-transaction-spanning-remote-calls)
- [25.52 Tranzaksiyadan tashqarida LazyInitializationException (LazyInitializationException Outside Transaction)](#2552-tranzaksiyadan-tashqarida-lazyinitializationexception-lazyinitializationexception-outside-transaction)
- [25.53 Property tarqoqligi (Property Sprawl)](#2553-property-tarqoqligi-property-sprawl)
- [25.54 Katta loy to'p (Big Ball of Mud)](#2554-katta-loy-top-big-ball-of-mud)
- [25.55 Taqsimlangan monolit (Distributed Monolith)](#2555-taqsimlangan-monolit-distributed-monolith)
- [25.56 Umumiy ma'lumotlar bazasi (Shared Database)](#2556-umumiy-malumotlar-bazasi-shared-database)
- [25.57 Suhbatkash I/O (Chatty I/O)](#2557-suhbatkash-io-chatty-io)
- [25.58 Nano-servislar (Nano-services)](#2558-nano-servislar-nano-services)
- [25.59 Entitet-servislar (Entity Services)](#2559-entitet-servislar-entity-services)
- [25.60 Sinxron chaqiruv zanjirlari (Synchronous call chains)](#2560-sinxron-chaqiruv-zanjirlari-synchronous-call-chains)
- [25.61 Qayta urinish bo'roni (Retry Storm (anti-pattern))](#2561-qayta-urinish-boroni-retry-storm-anti-pattern)
- [25.62 Band ma'lumotlar bazasi (Busy Database)](#2562-band-malumotlar-bazasi-busy-database)
- [25.63 Noto'g'ri obyekt yaratish (Improper Instantiation)](#2563-notogri-obyekt-yaratish-improper-instantiation)
- [25.64 Monolit saqlash qatlami (Monolithic Persistence)](#2564-monolit-saqlash-qatlami-monolithic-persistence)
- [25.65 Cache'ning yo'qligi (No Caching)](#2565-cachening-yoqligi-no-caching)
- [25.66 Shovqinli qo'shni (Noisy Neighbor)](#2566-shovqinli-qoshni-noisy-neighbor)
- [25.67 Bloklovchi sinxron I/O (Synchronous I/O)](#2567-bloklovchi-sinxron-io-synchronous-io)
- [25.68 Keraksiz ma'lumot olish (Extraneous Fetching)](#2568-keraksiz-malumot-olish-extraneous-fetching)
- [25.69 Ikki tomonlama yozish (Dual Writes)](#2569-ikki-tomonlama-yozish-dual-writes)
- [25.70 Servislar o'rtasida ikki fazali commit (Two-Phase Commit across services)](#2570-servislar-ortasida-ikki-fazali-commit-two-phase-commit-across-services)
- [25.71 Taminotchi qulfi (Vendor Lock-in)](#2571-taminotchi-qulfi-vendor-lock-in)
- [25.72 Rezyume uchun dasturlash (Resume-Driven Development)](#2572-rezyume-uchun-dasturlash-resume-driven-development)
- [25.73 Arxitektura astronavti (Architecture Astronaut)](#2573-arxitektura-astronavti-architecture-astronaut)
- [25.74 Tasodifiy murakkablik (Accidental Complexity)](#2574-tasodifiy-murakkablik-accidental-complexity)
- [25.75 Hodisa spagettisi (Event Spaghetti)](#2575-hodisa-spagettisi-event-spaghetti)
- [25.76 Oltin qoplama (Gold Plating)](#2576-oltin-qoplama-gold-plating)
- [25.77 Tahlil falaji (Analysis Paralysis)](#2577-tahlil-falaji-analysis-paralysis)
- [25.78 Mayda-chuyda bahs (Bikeshedding)](#2578-mayda-chuyda-bahs-bikeshedding)
- [25.79 Komissiya bilan loyihalash (Design by Committee)](#2579-komissiya-bilan-loyihalash-design-by-committee)
- [25.80 "Bu yerda o'ylab topilmagan" (Not Invented Here)](#2580-bu-yerda-oylab-topilmagan-not-invented-here)
- [25.81 Mo'ri tizim (Stovepipe System)](#2581-mori-tizim-stovepipe-system)
- [25.82 Katta portlash bilan qayta yozish (Big-Bang Rewrite)](#2582-katta-portlash-bilan-qayta-yozish-big-bang-rewrite)
- [25.83 Rejalashtirishdan o'lim (Death by Planning)](#2583-rejalashtirishdan-olim-death-by-planning)
- [25.84 Amalda qo'llash](#2584-amalda-qollash)

</details>



Anti-patternlar - bu birinchi qarashda muammoni hal qilayotgandek ko'rinadigan, lekin amalda texnik qarzni oshiradigan, tizimni qo'llab-quvvatlashni va rivojlantirishni qimmatlashtiradigan takrorlanuvchi yechimlar. Dizayn patternlar "nimani qilish kerak"ni ko'rsatsa, anti-patternlar "nimadan qochish kerak"ni va eng muhimi - buzilish alomatlarini qanday tanib olishni o'rgatadi. Arxitektor uchun bu bilim ikki tomonlama muhim: birinchidan, u code review va arxitektura reviewda muammoni nomlash uchun umumiy lug'at beradi; ikkinchidan, legacy tizimlarni modernizatsiya qilishda qaysi joyni birinchi bo'lib refactoring qilish kerakligini prioritetlashtirishga yordam beradi. Spring ekosistemasida anti-patternlarning aksariyati freymvorkning qulayligidan kelib chiqadi - annotatsiya qo'yish oson, shuning uchun ularni o'ylamasdan qo'yish ham oson.

## 25.1 Xudo obyekt (God Object)

**Tavsif:** God Object - tizimdagi juda ko'p mas'uliyatni o'ziga yig'ib olgan, minglab qatorlik va o'nlab bog'liqlikka ega sinf. U Single Responsibility Principle'ni buzadi: har qanday talab o'zgarishi aynan shu sinfga tegadi, natijada merge conflictlar ko'payadi va unit test yozish amalda imkonsiz bo'lib qoladi. Bunday sinf tizimning arxitektura "bo'g'zi"ga aylanadi - uni bilmagan dasturchi hech narsa o'zgartira olmaydi. Sabab odatda bosqichma-bosqich o'sish: har safar "shu yerga ham qo'shib qo'yaman" degan qaror.

**Spring'da qayerda uchraydi:** Eng ko'p uchraydigan ko'rinish - 3000+ qatorlik `@Service` sinfi, unga 15-20 ta constructor parametri orqali `@Autowired` qilingan repository va boshqa service'lar; yoki `@RestController` ichida 40 ta `@GetMapping`/`@PostMapping` metodi. Yana bir ko'rinish - `ApplicationContext` yoki `BeanFactory`ni to'g'ridan-to'g'ri inject qilib, `getBean()` bilan hamma narsani qo'lda olish (service locator ko'rinishidagi God Object). Aniqlash uchun Spring loyihalarida ArchUnit (`classes().should().haveOnlyFinalFields()` kabi qoidalar bilan birga o'z metrikalaringiz), SonarQube, PMD'ning `ExcessiveClassLength` va `TooManyFields` qoidalari, Checkstyle'ning `FileLength` moduli ishlatiladi. Spring Modulith (`spring-modulith-core`) modul chegaralarini `@ApplicationModule` bilan belgilab, bitta paketga hamma narsa to'planishini test darajasida man qiladi.

**Qo'llanish keyslari:**
- Monolit ERP tizimidagi `OrderService` buyurtma, to'lov, omborxona va hisobot logikasini bir vaqtda o'z ichiga oladi.
- Legacy loyihada `UtilService` yoki `CommonHelper` nomli sinf butun tizimning aralash logikasini saqlaydi.
- `@Entity` sinf 80 ta ustun va 20 ta `@OneToMany` bog'lanishga ega bo'lib, DTO, validatsiya va business logikani ham o'z ichiga oladi.
- Konfiguratsiya darajasida: bitta `@Configuration` sinfida 50 dan ortiq `@Bean` metodi, hammasi turli domenlarga tegishli.
- Microservice'ga ko'chirish paytida: bitta service'ning 90% kodi bir sinfda bo'lsa, chegaralarni ajratish uchun avval shu sinfni bo'lish kerak bo'ladi.

**Ehtiyot bo'ling:** God Object'ni bir yo'la bo'lib tashlash ko'pincha regressiyaga olib keladi - avval xarakteristika testlari (characterization tests) yozib, so'ng Facade ortida bosqichma-bosqich metodlarni ko'chirish kerak. Shuningdek, sinfni mexanik ravishda kichik bo'laklarga bo'lish o'zi yechim emas: agar bo'laklar bir-biriga siklik bog'liq bo'lsa, siz God Object'ni distributed God Object'ga aylantirgan bo'lasiz.

## 25.2 Spagetti kod (Spaghetti Code)

**Tavsif:** Spaghetti Code - boshqaruv oqimi chigallashgan, aniq qatlamlari va modul chegaralari bo'lmagan kod. Uning asosiy belgisi: biror o'zgarishning qayerga ta'sir qilishini o'qib bilish mumkin emas, faqat debugger bilan kuzatish kerak. Bu holat chuqur ichma-ich `if/else`, ko'p nuqtada o'zgaradigan umumiy mutable holat va qatlamlar o'rtasidagi teskari bog'liqliklar natijasida yuzaga keladi. Oqibati - har bir bugfix yangi bug tug'diradi.

**Spring'da qayerda uchraydi:** Klassik ko'rinish - `@Controller` ichida business logika, tranzaksiya boshqaruvi va SQL chaqiruvlari aralash; yoki `@Service` sinfi `HttpServletRequest`ni parametr sifatida qabul qiladi (web qatlami domenga oqib kirgan). Spring'ga xos ko'rinishlar: annotatsiya ichidagi murakkab SpEL ifodalari (`@PreAuthorize`, `@Value`, `@Cacheable(condition = ...)`), bir-biriga bog'langan `@Conditional`/`@ConditionalOnProperty` zanjirlari, `@Order` bilan boshqarilayotgan noaniq filter va interceptor ketma-ketligi. Davolash vositalari: ArchUnit bilan qatlam qoidalari (`layeredArchitecture()`), Spring Modulith bilan modul chegaralari va `@ApplicationModuleTest`, `spring-boot-actuator`ning `/actuator/mappings` va `/actuator/beans` endpointlari bilan real bog'liqlik grafigini ko'rish.

**Qo'llanish keyslari:**
- 15 yillik to'lov tizimida `@Transactional` metod ichida 300 qatorlik `if (status == 1) ... else if (status == 2)` zanjiri.
- Web qatlamidan domen qatlamiga, domen qatlamidan yana web DTO'siga teskari bog'liqlik hosil bo'lgan monolit.
- Bir nechta `OncePerRequestFilter` va `HandlerInterceptor` bir-birining atributlariga tayanib ishlaydi, tartib `@Order` bilan tasodifiy belgilangan.
- Event-driven tizimda `ApplicationEventPublisher` orqali tarqalgan hodisalar zanjiri hech qayerda hujjatlashtirilmagan.
- Legacy XML konfiguratsiya va Java konfiguratsiya bir-birining bean'larini qayta ta'riflaydi.

**Ehtiyot bo'ling:** Spaghetti kodni "chiroyli" qilish uchun ko'p sonli abstraksiya qatlami qo'shish eng keng tarqalgan xato - bu muammoni yashiradi, yechmaydi. Avval boshqaruv oqimini test bilan qulflang, so'ng qatlam chegaralarini ArchUnit testi bilan majburiy qiling, shundan keyingina ichki tuzilmani o'zgartiring.

## 25.3 Lava oqimi (Lava Flow)

**Tavsif:** Lava Flow - bir paytdagi eksperiment yoki yarim bitgan migratsiyadan qolgan, hech kim nima uchun borligini bilmaydigan, lekin o'chirishga qo'rqadigan kod va konfiguratsiya qatlamlari. "Qotib qolgan lava" nomi shundan: kod loyihada muzlab qolgan, atrofidagi hamma narsa esa o'zgargan. U kod bazasining hajmini oshiradi, build vaqtini uzaytiradi va yangi dasturchini chalg'itadi. Asosiy sabab - migratsiyalarni oxirigacha yetkazmaslik va "ehtimol kerak bo'ladi" mentaliteti.

**Spring'da qayerda uchraydi:** `application.yml` ichida hech qanday `@ConfigurationProperties` yoki `@Value` tomonidan o'qilmaydigan o'nlab property; `@Profile("legacy")` yoki `@Profile("old-flow")` bilan belgilangan va hech bir muhitda yoqilmaydigan `@Configuration` sinflari; `spring.main.allow-bean-definition-overriding=true` bilan yashirilgan ikkilangan bean ta'riflari. Yana bir tipik holat - Spring Boot 2.x'dan 3.x'ga o'tishda qolib ketgan `javax.*` importlari uchun shim sinflar, yoki olib tashlangan `WebSecurityConfigurerAdapter` (Spring Security 6'da yo'q) o'rniga yozilgan ikkita parallel security konfiguratsiyasi. Flyway/Liquibase migratsiyalarida esa hech qachon ishlatilmagan jadval va ustunlar lava sifatida qoladi.

**Qo'llanish keyslari:**
- Spring Boot 3.x'ga ko'chirilgan loyihada eski `RestTemplate` konfiguratsiyasi va yangi `RestClient` konfiguratsiyasi bir vaqtda mavjud, biri ishlatilmaydi.
- Yarim bitgan Kafka migratsiyasi: `@KafkaListener` yozilgan, lekin topic hech qachon yaratilmagan.
- `application-staging.yml` ichida uch yil oldin o'chirilgan tashqi servis URL'lari.
- XML konfiguratsiyadan Java konfiguratsiyaga o'tish yakunlanmagan, `applicationContext.xml` hali `@ImportResource` bilan yuklanadi.
- Feature flag bilan o'chirilgan kod yo'li ikki yil davomida `false` holatida turadi va hech kim olib tashlamaydi.

**Ehtiyot bo'ling:** "Keyin kerak bo'ladi" degan sabab bilan saqlangan kod deyarli hech qachon kerak bo'lmaydi - Git tarixi sizning arxivingiz, kod bazasi emas. Lekin o'chirishdan oldin production telemetriyasi bilan tasdiqlang: Spring Boot Actuator metrikalari va log'lar orqali kod yo'li haqiqatan ishlatilmayotganini isbotlamasdan o'chirish xavfli.

## 25.4 Oltin bolg'a (Golden Hammer)

**Tavsif:** Golden Hammer - bitta tanish texnologiya yoki patternni barcha muammolarga qo'llash odati ("menda bolg'a bor, demak hammasi mix"). Bu anti-pattern texnik qarorlarni muammo talabidan emas, jamoaning mavjud ko'nikmasidan kelib chiqib qabul qilishdan tug'iladi. Natijada oddiy vazifa murakkab infratuzilma bilan hal qilinadi yoki noto'g'ri vosita ishlatiladi. Arxitektor uchun bu eng xavfli anti-pattern, chunki uning oqibati kod darajasida emas, platforma darajasida tuzatiladi.

**Spring'da qayerda uchraydi:** Spring ekosistemasida tipik misollar: barcha o'qish so'rovlari uchun ham JPA/Hibernate ishlatish (hisobotlar uchun `JdbcClient` yoki `JdbcTemplate` ancha samarali); har bir metodga `@Transactional` qo'yish; har bir integratsiya uchun Kafka ko'tarish; CRUD API uchun to'liq reactive stack (`spring-boot-starter-webflux`) tanlash, keyin esa ichida blokirovkalanadigan JDBC chaqirish. Yana bir ko'rinish - `@Cacheable`ni o'lchovsiz hamma joyga qo'yish yoki har bir domen hodisasi uchun Spring Integration / Spring Cloud Stream kanali yaratish. Java 21+ virtual threadlar (`spring.threads.virtual.enabled=true`) paydo bo'lgandan keyin ko'p holatda imperativ stack reactive'ga muqobil bo'ldi, bu esa "hammasi reactive" golden hammer'ini yanada asossiz qiladi.

**Qo'llanish keyslari:**
- Jamoa Hibernate'ni biladi, shuning uchun 50 jadvalli analitik hisobot ham `@Entity` grafigi orqali yuklanadi va N+1 muammo tug'iladi.
- Ikki service o'rtasidagi sinxron so'rov-javob uchun Kafka ishlatiladi, natijada correlation ID va timeout boshqaruvi qo'lda yoziladi.
- Monolitni bo'lish o'rniga har bir yangi funksiya uchun alohida microservice yaratiladi, chunki "biz microservice jamoasimiz".
- Oddiy mahalliy cache yetarli bo'lgan joyda Redis klasteri ko'tariladi va yangi nosozlik nuqtasi paydo bo'ladi.
- Har bir validatsiya uchun Spring AOP aspekti yoziladi, `jakarta.validation` annotatsiyalari yetarli bo'lsa ham.

**Ehtiyot bo'ling:** Golden Hammer'ga qarshi kurash "yangi texnologiya hammasini yechadi" degan teskari xatoga olib kelmasligi kerak - har bir yangi vosita operatsion yuk, monitoring va jamoa o'rganish xarajatini qo'shadi. Qarorni Architecture Decision Record (ADR) ko'rinishida muqobillari bilan birga yozib qo'yish bu anti-patternning eng arzon davosi.

## 25.5 Qayiq langari (Boat Anchor)

**Tavsif:** Boat Anchor - tizimda saqlanayotgan, lekin hech qanday foyda bermaydigan komponent, kutubxona yoki infratuzilma. Lava Flow'dan farqi shunda: Boat Anchor odatda ongli ravishda "kelajak uchun" sotib olingan yoki qo'shilgan, lekin hech qachon ishlatilmagan. U build vaqtini, artifact hajmini, xavfsizlik yuzasini (attack surface) va litsenziya xarajatlarini oshiradi. Microservice muhitida u to'g'ridan-to'g'ri pul yo'qotishga aylanadi.

**Spring'da qayerda uchraydi:** `pom.xml` yoki `build.gradle` ichida ishlatilmaydigan `spring-boot-starter-*` bog'liqliklari - masalan `spring-boot-starter-data-redis` qo'shilgan, lekin `RedisTemplate` hech qayerda inject qilinmagan; bu avtokonfiguratsiyani ishga tushiradi, ulanish urinishlari va ortiqcha bean'lar paydo bo'ladi. Aniqlash: `mvn dependency:analyze`, Gradle'ning `dependencyInsight` taski, Spring Boot Actuator'ning `/actuator/conditions` endpointi (qaysi avtokonfiguratsiya nega yoqilganini ko'rsatadi) va `/actuator/beans`. Native image (`spring-boot-starter-parent` + GraalVM AOT) ga o'tishda ishlatilmaydigan bog'liqliklar eng ko'p muammo tug'diradi, shuning uchun ularni oldin tozalash zarur.

**Qo'llanish keyslari:**
- "Keyin kerak bo'ladi" deb qo'shilgan Kafka klasteri ikki yil bo'sh turadi va infratuzilma hisobini oshiradi.
- Loyihada `spring-boot-starter-actuator` bor, lekin hech bir endpoint ochilmagan va metrikalar yig'ilmaydi.
- Eski SOAP integratsiyasi uchun olingan kutubxona qoladi va CVE skanerida har hafta ogohlantirish beradi.
- Monorepo'da hech kim deploy qilmaydigan modul CI'da har push'da build bo'lib, pipeline vaqtini yeydi.
- Litsenziyasi pullik APM agenti barcha pod'larga ulangan, lekin dashboard'ga hech kim kirmaydi.

**Ehtiyot bo'ling:** Boat Anchor'ni o'chirishdan oldin uning haqiqatan ishlatilmayotganini tekshiring - ba'zi bog'liqliklar runtime'da reflection yoki `META-INF/spring/...AutoConfiguration.imports` orqali yuklanadi va statik tahlil ularni "ishlatilmagan" deb ko'rsatadi. Shuningdek, transitiv bog'liqliklarni olib tashlashda `mvn dependency:tree` bilan kim uni talab qilayotganini aniqlang.

## 25.6 O'lik kod (Dead Code)

**Tavsif:** Dead Code - hech qachon bajarilmaydigan yoki natijasi ishlatilmaydigan kod: chaqirilmaydigan metodlar, hech qachon `true` bo'lmaydigan shartlar, ishlatilmaydigan maydonlar va endpointlar. U kompilyatsiyaga xalal bermaydi, lekin kod o'qish yukini, test qoplamasi statistikasini va refactoring narxini buzadi. Eng yomoni - o'lik kod review paytida "tirik" deb hisoblanib, unga asoslangan noto'g'ri qarorlar chiqariladi.

**Spring'da qayerda uchraydi:** Spring'da o'lik kodni aniqlash qiyinroq, chunki ko'p kod reflection orqali chaqiriladi: `@EventListener` metodlari, `@Scheduled` taskllari, `@KafkaListener`, `@JmsListener`, `@Bean` metodlari va `@RequestMapping` endpointlari statik tahlil uchun "chaqirilmagan" ko'rinadi. Shu sababli IDE inspeksiyasiga ishonib bo'lmaydi; buning o'rniga `/actuator/mappings` bilan real ro'yxatdan o'tgan endpointlarni, Micrometer'ning `http.server.requests` metrikasini (URI tag bilan) va API gateway log'larini birlashtirib, nol trafikli endpointlarni aniqlash kerak. Test qoplamasi uchun JaCoCo, kod hidlari uchun SonarQube'ning `java:S1144` (ishlatilmaydigan private metod) kabi qoidalari yordam beradi.

**Qo'llanish keyslari:**
- Mobil ilovaning eski versiyasi uchun qoldirilgan `/api/v1/...` endpointlari, yangi versiya `v2`ga o'tgan.
- `@Scheduled(cron = ...)` task metodi bor, lekin `@EnableScheduling` olib tashlangani uchun hech qachon ishlamaydi.
- `if (featureEnabled)` sharti konfiguratsiyada doimiy `false`, undan keyingi butun blok o'lik.
- `@Deprecated` service metodlari, barcha chaqiruvchilar yangi metodga o'tgan, lekin eskisi o'chirilmagan.
- Test kodidagi `@Disabled` testlar yillar davomida ishlamaydi, lekin loyihada "test bor" degan illuziya yaratadi.

**Ehtiyot bo'ling:** Public API yoki kutubxona kodida "o'lik" ko'rinadigan metod tashqi mijozlar tomonidan ishlatilayotgan bo'lishi mumkin - semantik versiyalash va deprecation siklini hurmat qiling. Reflection va Spring annotatsiyalari sababli o'chirish qarorini faqat production telemetriyasi bilan tasdiqlang.

## 25.7 Nusxa-ko'chirma dasturlash (Copy-Paste Programming)

**Tavsif:** Copy-Paste Programming - muammoni abstraksiya qilish o'rniga mavjud kod bo'lagini nusxalab, ozgina o'zgartirib ishlatish. Qisqa muddatda tez, uzoq muddatda qimmat: bitta bug yoki xavfsizlik teshigi o'nlab nusxada takrorlanadi va bir joyda tuzatilganda qolganlari eskiligida qoladi. Nusxalar vaqt o'tishi bilan sekin-asta bir-biridan farq qila boshlaydi (semantik drift), shuning uchun keyinchalik ularni birlashtirish ham xavfli bo'ladi. Bu microservice muhitida ayniqsa tez tarqaladi, chunki servislar o'rtasida "shared kod yo'q" qoidasi noto'g'ri tushuniladi.

**Spring'da qayerda uchraydi:** Har bir servisda takrorlanadigan `@ControllerAdvice` xato ishlovchilari, bir xil `SecurityFilterChain` konfiguratsiyasi, har bir modulda qayta yozilgan DTO-Entity mapping kodi, bir xil `RestClient`/`WebClient` bean sozlamalari (timeout, retry, interceptor). To'g'ri yechim - umumiy xatti-harakatni o'z starter'ingizga chiqarish: `@AutoConfiguration` sinfini yozib, uni `META-INF/spring/org.springframework.boot.autoconfigure.AutoConfiguration.imports` faylida ro'yxatdan o'tkazish (Spring Boot 3.x usuli; eski `spring.factories` endi ishlatilmaydi). Mapping uchun MapStruct, xato formati uchun Spring 6'ning `ProblemDetail` va `ResponseEntityExceptionHandler`, umumiy HTTP sozlamalari uchun `RestClientCustomizer` yoki `RestClient.Builder` bean'i ishlatiladi.

**Qo'llanish keyslari:**
- 12 ta microservice'ning har birida bir xil JWT tekshirish filteri nusxalangan, bittasida kalit aylanishi (key rotation) yangilanmagan.
- Bir xil pagination va sorting logikasi har bir controller'da qayta yozilgan.
- Audit log yozish kodi har bir service metodida takrorlanadi, AOP aspekti o'rniga.
- Integratsiya testlarining `@TestConfiguration` bloklari nusxalanib, Testcontainers sozlamalari har xil versiyada qoladi.
- Bir xil `application.yml` bloklari har bir servisda nusxalanadi, Spring Cloud Config yoki ConfigMap o'rniga.

**Ehtiyot bo'ling:** Teskari xato ham xavfli: tasodifiy o'xshash ikki kod bo'lagini majburan umumiy abstraksiyaga birlashtirish (noto'g'ri DRY) modullar o'rtasida keraksiz bog'liqlik yaratadi. Qoidani shunday qo'ying: bir xil business qoidasi takrorlansa - birlashtiring, shunchaki shakli o'xshash bo'lsa - qoldiring.

## 25.8 Sehrli sonlar va satrlar (Magic Numbers / Strings)

**Tavsif:** Magic Number/String - kodda izohsiz turgan, ma'nosi faqat muallifga ma'lum literal qiymat. Ular kodni o'qishni qiyinlashtiradi, bir qiymat bir necha joyda takrorlanganda esa noizchil o'zgarishga olib keladi. Eng xavfli ko'rinishi - biznes qoidasini ifodalovchi son (chegara, stavka, timeout) kodga yashiringanda: uni o'zgartirish uchun deploy kerak bo'ladi. Yechim - nomlangan konstanta, `enum` yoki tashqi konfiguratsiya.

**Spring'da qayerda uchraydi:** Spring'da sehrli satrlar annotatsiyalar ichida yashiringanda juda ko'p uchraydi: `@Qualifier("primaryDs")`, `@Cacheable("users")`, `@KafkaListener(topics = "order-created")`, `@Value("${...}")` kalitlari, `@PreAuthorize("hasRole('ADMIN')")` ichidagi rol nomlari, `@Profile("prod")`. Bularning hech biri kompilyatsiya vaqtida tekshirilmaydi - xato yozilsa, ilova ishga tushganda yoki undan ham keyin xato beradi. Davolash: `@ConfigurationProperties` (Spring Boot 3.x'da `record` bilan to'g'ridan-to'g'ri ishlaydi, `@ConstructorBinding` endi majburiy emas), konstanta sinflari, `CacheConfig` ichida cache nomlari uchun `public static final String`, rol nomlari uchun `enum` va `jakarta.validation` annotatsiyalari bilan chegaralarni ifodalash.

```java
@ConfigurationProperties("billing")
public record BillingProps(
        @DurationUnit(ChronoUnit.SECONDS) Duration gatewayTimeout,
        BigDecimal vatRate,
        int maxRetryAttempts) {}
// endi: props.vatRate() - kodda 0.12 literal yo'q, o'zgartirish deploy talab qilmaydi
```

**Qo'llanish keyslari:**
- To'lov servisida `if (amount > 1000000)` sharti - chegara qiymati biznes qoidasi, lekin kodda yashiringan.
- Cache nomi `@Cacheable("usr")` va `@CacheEvict("users")` shaklida har xil yozilgani uchun evict ishlamaydi.
- `Thread.sleep(3000)` yoki `setConnectTimeout(5000)` - birlik (sekund yoki millisekund) noma'lum.
- Status kodlari `status == 3` ko'rinishida saqlanadi, `enum OrderStatus` o'rniga.
- Kafka topic nomlari producer va consumer'da ikki joyda qo'lda yozilgan, biri typo bilan.

**Ehtiyot bo'ling:** Har bir literalni konstantaga chiqarish ham ortiqcha - `MAX_VALUE_ONE = 1` kabi konstantalar kodni faqat uzaytiradi. Faqat ma'no tashuvchi (biznes qoidasi, chegara, tashqi kontrakt nomi) qiymatlarni nomlang, loop indeksi yoki `0`/`1` kabi tabiiy qiymatlarni qoldiring.

## 25.9 Qattiq kodlash (Hard-Coding)

**Tavsif:** Hard-Coding - muhitga yoki kontekstga bog'liq qiymatni kodning o'ziga yozib qo'yish: URL, host, port, fayl yo'li, kredensial, muhit nomi. Bu ilovani bir muhitdan boshqasiga ko'chirishni imkonsiz qiladi va har bir o'zgarish uchun qayta build va deploy talab qiladi. Kredensiallar qattiq kodlanganda bu to'g'ridan-to'g'ri xavfsizlik hodisasiga aylanadi, chunki sir Git tarixiga abadiy tushadi. Magic String'dan farqi: bu yerda muammo nom emas, qiymatning tashqariga chiqarilmagani.

**Spring'da qayerda uchraydi:** `new RestTemplate()` yoki `RestClient.create("https://api.prod.example.com")` ko'rinishida kodda yozilgan host; `DataSource` bean'ida qattiq yozilgan JDBC URL, foydalanuvchi va parol; `@Value` default qiymatida yashiringan production endpoint. Spring buning uchun to'liq to'plam beradi: `application.yml` + `spring.profiles.active` bilan muhitga qarab ajratish, `@ConfigurationProperties`, `Environment` abstraksiyasi, tashqi konfiguratsiya uchun Spring Cloud Config Server, sirlar uchun `spring-cloud-starter-vault-config` yoki Kubernetes Secret'lari (`spring-cloud-kubernetes-config`), lokal rivojlanish uchun `spring-boot-docker-compose` va `spring-boot-testcontainers` modullari. Spring Boot'ning konfiguratsiya ustuvorligi (environment variable > command line > profile fayli > `application.yml`) aynan shu anti-patternni yechish uchun mavjud.

**Qo'llanish keyslari:**
- Integratsiya testida `jdbc:postgresql://localhost:5432/dev` yozilgan, CI muhitida test ishlamaydi.
- API kaliti `static final String API_KEY = "sk-..."` ko'rinishida kodda, repo public bo'lganda sir oshkor bo'ladi.
- Fayl yo'li `C:\\temp\\reports` yoki `/Users/dev/out` shaklida - Linux konteynerida ishlamaydi.
- `if ("prod".equals(env))` ko'rinishidagi muhit tekshiruvi `@Profile` yoki `@ConditionalOnProperty` o'rniga.
- Email jo'natuvchi manzil va SMTP host kodda, har bir mijoz uchun alohida build qilinadi.

**Ehtiyot bo'ling:** Hamma narsani konfiguratsiyaga chiqarish teskari muammo tug'diradi - yuzlab property hech kim tushunmaydigan "konfiguratsiya do'zaxi"ga aylanadi va noto'g'ri qiymat runtime'da ishdan chiqishga olib keladi. `@ConfigurationProperties` ustiga `jakarta.validation` annotatsiyalari va `@Validated` qo'yib, noto'g'ri konfiguratsiya ilovani ishga tushish paytida to'xtatishini ta'minlang.

## 25.10 Vaqtidan oldin optimizatsiya (Premature Optimization)

**Tavsif:** Premature Optimization - o'lchovga asoslanmagan, taxminiy "tezlik" uchun kodni murakkablashtirish. Uning narxi ikki tomonlama: kod o'qilishi va qo'llab-quvvatlanishi yomonlashadi, haqiqiy bottleneck esa boshqa joyda qoladi. Ko'pincha optimizatsiya ma'lumotlar hajmi va trafik profili ma'lum bo'lmaganda qilinadi, natijada noto'g'ri taxminga qurilgan arxitektura hosil bo'ladi. To'g'ri tartib: ishlaydigan kod → o'lchash → maqsadli optimizatsiya.

**Spring'da qayerda uchraydi:** Tipik ko'rinishlar: hamma joyga `@Cacheable` qo'yish (keyin cache invalidation muammosi paydo bo'ladi); har bir metodni `@Async` qilish va `TaskExecutor` sozlamalarini tushunmasdan thread pool ko'paytirish; Hibernate ikkinchi darajali cache'ni yoqib, keyin stale ma'lumot muammosiga tushish; faqat "tezroq bo'ladi" degan taxmin bilan reactive stack'ga o'tish. O'lchash vositalari Spring'da tayyor: `spring-boot-starter-actuator` + Micrometer (`http.server.requests`, `jdbc.connections`, `hikaricp.connections` metrikalari), Micrometer Tracing bilan distributed tracing, mikro-benchmark uchun JMH, `@Timed` va `ObservationRegistry` (Spring Framework 6 Observation API). Java 21+ virtual threadlar (`spring.threads.virtual.enabled=true`) ko'p holatda qo'lda thread pool sozlashni keraksiz qiladi.

**Qo'llanish keyslari:**
- Kuniga 100 so'rov keladigan endpoint uchun Redis cache va cache warming logikasi yozilgan.
- `StringBuilder` va bitwise optimizatsiyalar qilingan, haqiqiy bottleneck esa N+1 SQL so'rovi edi.
- Har bir repository metodi uchun qo'lda SQL yozilgan, chunki "JPA sekin" - profiling qilinmagan.
- Monolit erta bosqichda microservice'larga bo'lingan, go'yo "scale qilish kerak bo'ladi", natijada latency oshgan.
- Connection pool hajmi 200 ga ko'tarilgan, aslida ma'lumotlar bazasi 50 ulanishdan ko'pini ko'tarmaydi.

**Ehtiyot bo'ling:** Bu anti-pattern "optimizatsiya haqida hech o'ylamaslik" degan ruxsat emas - algoritm murakkabligi, N+1 so'rovlar va ma'lumotlar modeli kabi qarorlar keyinchalik juda qimmat tuzatiladi va ularni loyihaning boshida to'g'ri qilish kerak. Chegarani shunday qo'ying: arxitektura darajasidagi qarorlar oldindan o'ylanadi, mikro-optimizatsiyalar esa faqat profiler ko'rsatgandan keyin.

## 25.11 Kargo kulti dasturlash (Cargo Cult Programming)

**Tavsif:** Cargo Cult Programming - kodni yoki patternni nima uchun ishlashini tushunmasdan, "shunday yozish kerak" degan ishonch bilan takrorlash. Natijada tizimda ma'nosiz annotatsiyalar, keraksiz qatlamlar va nosamarali ritual kod paydo bo'ladi. Bu xato ko'pincha Stack Overflow javoblarini yoki eski blog postlarini ko'chirishdan, konferensiya ma'ruzasidagi yirik kompaniya yechimini kontekstsiz qabul qilishdan tug'iladi. Xavfi shundaki, kod ishlaydi - shu sababli hech kim uni so'roq qilmaydi.

**Spring'da qayerda uchraydi:** Juda ko'p: `@SpringBootApplication` ustiga yana `@ComponentScan` va `@EnableAutoConfiguration` qo'yish (ular allaqachon ichida); bitta constructor bo'lganda unga `@Autowired` yozish (Spring 4.3'dan beri keraksiz); har bir `@Transactional`ga `propagation = Propagation.REQUIRES_NEW` qo'yish; Spring Security 6'da olib tashlangan `WebSecurityConfigurerAdapter` uslubini `SecurityFilterChain` bean'i bilan birga saqlash; `@Service` qo'yilgan sinfni yana `@Bean` sifatida ta'riflash; har bir interfeys uchun faqat bitta implementatsiya bo'lsa ham `XxxServiceImpl` yaratish; DTO uchun Lombok `@Data` ishlatish, `record` yetarli bo'lsa ham. Yana bir keng tarqalgan ko'rinish - yirik kompaniyalarning microservice naqshini (service mesh, saga, CQRS) 5 kishilik jamoaga ko'chirish.

**Qo'llanish keyslari:**
- `@Transactional(readOnly = true)` har bir metodga qo'yilgan, shu bilan birga `@Modifying` so'rovlar jim ishlamay qoladi.
- `@EnableJpaRepositories` va `@EntityScan` qo'lda yozilgan, Spring Boot avtokonfiguratsiyasi allaqachon buni qiladi.
- Har bir service uchun interfeys + Impl yaratiladi, hech qachon ikkinchi implementatsiya bo'lmaydi.
- CQRS va Event Sourcing oddiy CRUD admin paneliga qo'llaniladi.
- `field injection` (`@Autowired private Foo foo;`) ishlatiladi, chunki "hamma shunday yozadi", natijada test yozish qiyinlashadi.

**Ehtiyot bo'ling:** Bu anti-patternni aniqlash uchun oddiy test bor: kod review'da "bu annotatsiya nima qiladi?" savoliga javob yo'q bo'lsa - bu kargo kult. Lekin teskari ekstremallikdan ham saqlaning: yaxshi o'rnashgan konvensiyalarni "o'zimcha qilaman" deb buzish jamoada yangi, hujjatlashtirilmagan murakkablik tug'diradi.

## 25.12 Yo-Yo muammosi (Yo-Yo Problem)

**Tavsif:** Yo-Yo Problem - kodni tushunish uchun o'quvchi meros zanjirining yuqori va pastki qatlamlari o'rtasida ko'p marta "yuqoriga-pastga" sakrashga majbur bo'lishi. Bu chuqur inheritance ierarxiyasi va template method'ning haddan ortiq ishlatilishidan kelib chiqadi: bitta so'rov oqimini kuzatish uchun 6-7 sinfni ochish kerak bo'ladi. Natijada kognitiv yuk oshadi, debugging sekinlashadi va abstract metodni o'zgartirish barcha avlodlarga kutilmagan ta'sir qiladi. Yechim - merosni kompozitsiya va delegatsiya bilan almashtirish.

**Spring'da qayerda uchraydi:** Spring'ning o'zida ham chuqur ierarxiyalar bor va ularni kengaytirganda bu muammo seziladi: `OncePerRequestFilter` → `GenericFilterBean`, `AbstractAuthenticationProcessingFilter` zanjiri, `AbstractApplicationContext` ierarxiyasi, Spring Data'dagi `Repository` → `CrudRepository` → `ListCrudRepository` → `JpaRepository` (Spring Data 3.x'da `ListCrudRepository` qo'shilgan). Loyiha kodida eng ko'p uchraydigan shakl - `AbstractBaseService<T, ID>` → `AbstractAuditableService<T>` → `AbstractCachedService<T>` → `OrderServiceImpl` ko'rinishidagi generik bazalar, yoki `BaseEntity` → `AuditableEntity` → `SoftDeletableEntity` zanjiri. Spring buning o'rniga `@MappedSuperclass`ni yupqa saqlash, audit uchun `@EnableJpaAuditing` + `AuditingEntityListener`, umumiy xatti-harakat uchun AOP va dekoratorlarni (`@Primary` bilan o'ralgan bean) taklif qiladi.

**Qo'llanish keyslari:**
- Legacy loyihada har bir controller `AbstractCrudController`dan meros oladi va `@Override` qilingan 12 ta hook metod bor.
- Generik `AbstractService<T>` bazasi barcha servislarni bir xil tranzaksiya modeliga majburlaydi.
- Testlar `AbstractIntegrationTest` → `AbstractDbTest` → `AbstractSecurityTest` zanjiridan meros oladi, qaysi `@Sql` qachon ishlashini bilish imkonsiz.
- Custom Spring Security filter yozilgan, lekin uning harakatini tushunish uchun uchta abstract bazani o'qish kerak.
- `@MappedSuperclass` zanjirida bir xil maydon turli darajada qayta ta'riflanadi va Hibernate kutilmagan DDL hosil qiladi.

**Ehtiyot bo'ling:** Merosni butunlay man qilish ham yechim emas - freymvork kengaytmalarida (filter, converter, listener) abstract baza sinflari to'g'ri vosita. Qoida: meros chuqurligi 2-3 darajadan oshsa yoki baza sinf faqat kodni "qayta ishlatish" uchun yaratilsa, kompozitsiyaga o'ting.

## 25.13 Arvoh obyekt (Poltergeist)

**Tavsif:** Poltergeist - qisqa umr ko'radigan, o'z holati va haqiqiy mas'uliyati bo'lmagan, faqat boshqa obyektga chaqiruvni uzatish uchun yaratilgan sinf. U arxitekturaga qatlam qo'shadi, lekin hech qanday qiymat bermaydi: chaqiruv zanjiri uzayadi, stack trace o'qilishi yomonlashadi va har bir yangi metod uchta joyda qo'shilishi kerak bo'ladi. Odatda "qatlamli arxitektura shunday bo'lishi kerak" degan noto'g'ri tushunchadan paydo bo'ladi.

**Spring'da qayerda uchraydi:** Eng keng tarqalgan ko'rinish - `@Service` sinf faqat `@Repository` metodini uzatadi: `findById(id)` → `repository.findById(id)`, hech qanday business logika yo'q; shu bilan birga controller → service → manager → helper → repository ko'rinishidagi to'rt qatlamli uzatish zanjiri. Nomlar bo'yicha hid: `XxxManager`, `XxxHelper`, `XxxCoordinator`, `XxxDelegate` - ularning hammasi bitta metodga ega. Spring'da bu ko'pincha keraksiz interfeys + `Impl` juftligi bilan birga keladi. Ba'zan esa teskari: `@Transactional` yoki `@Cacheable` proxy ishlashi uchun atayin alohida bean kerak bo'ladi (self-invocation proxy'ni chetlab o'tadi) - bu holat Poltergeist emas, texnik zarurat. Shuningdek `@Scope("prototype")` bilan har safar yaratiladigan, holati ishlatilmaydigan bean'lar ham shu anti-patternning ko'rinishi.

**Qo'llanish keyslari:**
- `UserFacade` sinfi faqat `UserService`ning bir metodini chaqiradi va boshqa hech narsa qilmaydi.
- `OrderHelper` har bir metodida `orderRepository`ga uzatadi, controller to'g'ridan-to'g'ri service'ni chaqira olardi.
- Har bir `@Entity` uchun avtomatik generatsiya qilingan `XxxManager` sinflari, hech qaysisida logika yo'q.
- Mapper sinfi faqat MapStruct mapper'ini o'rab turadi va qo'shimcha mantiq bermaydi.
- Legacy integratsiyada `Gateway` → `Adapter` → `Client` zanjiri, uchtasidan ikkitasi shunchaki uzatish.

**Ehtiyot bo'ling:** Barcha yupqa qatlamni Poltergeist deb olib tashlash xato bo'ladi - anti-corruption layer, port/adapter chegarasi va `@Transactional` proxy chegarasi ataylab yupqa bo'lishi mumkin. Qarorni shunday qabul qiling: agar qatlam kelajakdagi o'zgarishni izolyatsiya qilmasa va test yozishni osonlashtirmasa, u keraksiz.

## 25.14 Istisnolarni yutib yuborish (Exception Swallowing)

**Tavsif:** Exception Swallowing - istisnoni tutib olib, uni qayta tashlamaslik va yetarli ma'lumotni saqlab qolmaslik. Natijada xato jim yo'qoladi: tizim "muvaffaqiyatli" javob qaytaradi, lekin ma'lumot saqlanmagan yoki yarim saqlangan bo'ladi. Bu production'da aniqlash eng qiyin xato turi, chunki log ham, metrika ham hech narsa ko'rsatmaydi. Eng xavfli oqibati - buzilgan ma'lumotlar bazasi holati va hech kim payqamagan ma'lumot yo'qolishi.

**Spring'da qayerda uchraydi:** `catch (Exception e) { }` yoki faqat `log.error(e.getMessage())` (stack trace yo'q, `e` o'zi uzatilmagan) ko'rinishlari. Spring'ga xos eng muhim tuzoq - `@Transactional` metod ichida istisnoni tutib olish: Spring'ning default qoidasi bo'yicha faqat `RuntimeException` va `Error` rollback'ga olib keladi, checked exception esa olib kelmaydi; agar siz `RuntimeException`ni tutib, uni qayta tashlamasangiz, tranzaksiya commit bo'ladi. Agar tutib olish zarur bo'lsa, `TransactionAspectSupport.currentTransactionStatus().setRollbackOnly()` chaqirish yoki `@Transactional(rollbackFor = ...)` ni to'g'ri sozlash kerak. Yana bir joy - `@Async` metodlar: ulardan chiqqan istisno chaqiruvchiga yetib bormaydi, shuning uchun `AsyncUncaughtExceptionHandler` (`AsyncConfigurer` orqali) yoki `CompletableFuture` qaytarish kerak. Shuningdek `@ExceptionHandler` ichida istisnoni yutib, HTTP 200 qaytarish ham shu anti-pattern; Spring 6'da to'g'ri yo'l - `ProblemDetail` (RFC 9457) bilan `@RestControllerAdvice` va `ResponseEntityExceptionHandler`.

```java
@Transactional
public void process(Order o) {
    try {
        payments.charge(o);            // RuntimeException tashlashi mumkin
    } catch (PaymentException e) {
        log.error("charge failed id={}", o.getId(), e);          // stack trace saqlanadi
        TransactionAspectSupport.currentTransactionStatus().setRollbackOnly();
        throw new OrderProcessingException(o.getId(), e);        // sabab zanjiri uzilmaydi
    }
}
```

**Qo'llanish keyslari:**
- Batch job'da har bir element uchun `catch (Exception e) {}` - 10 ming yozuvdan 300 tasi jim yo'qoladi.
- `@Scheduled` task ichidagi yutib yuborilgan istisno sababli sinxronizatsiya oylar davomida ishlamaydi.
- `@Transactional` metodda tutilgan `RuntimeException` tufayli yarim bajarilgan tranzaksiya commit bo'ladi.
- `@KafkaListener` ichida xato yutiladi, xabar `acknowledge` bo'ladi va DLQ'ga tushmaydi.
- `InterruptedException` tutilib tashlab yuboriladi, `Thread.currentThread().interrupt()` chaqirilmaydi va shutdown muzlab qoladi.

**Ehtiyot bo'ling:** Teskari ekstremallik ham mavjud - har bir istisnoni yuqoriga uzatish natijasida controller darajasida tushunarsiz texnik xatolar foydalanuvchiga chiqadi; chegarani aniq belgilang va tashqi kontraktga faqat `ProblemDetail` ko'rinishidagi ma'noli xatoni qaytaring. Istisnoni tutish faqat uni ma'noli tarzda hal qilayotganingizda (retry, fallback, boshqa turga o'rash) o'rinli, "logga yozib davom etish" esa deyarli hamma holatda xato.

## 25.15 Oqib Chiquvchi Abstraksiya (Leaky Abstraction)

**Tavsif:** Abstraksiya o'zining ichki implementatsiya detallarini iste'molchiga "oqizib" chiqaradi, natijada klient kod abstraksiyaning ortidagi texnologiyani bilishga majbur bo'ladi. Masalan, repository interfeysi `List<T>` qaytaradi, lekin aslida lazy proxy bo'lib, transaction yopilgandan keyin ishlamaydi. Abstraksiya sodda ko'rinadi, ammo to'g'ri ishlatish uchun pastki qatlamni tushunish shart bo'ladi. Natijada qatlamlarni almashtirish imkoniyati yo'qoladi va xatolar kutilmagan joyda yuzaga chiqadi.

**Spring'da qayerda uchraydi:** Eng klassik misol - Hibernate'ning `LazyInitializationException`: `@OneToMany(fetch = FetchType.LAZY)` kolleksiyasini `@Transactional` metod tashqarisida, controller yoki Jackson serializatsiyasida o'qiganda yuzaga keladi. Spring Data JPA'ning `JpaRepository` interfeysi "shunchaki kolleksiya" ko'rinishini beradi, lekin `Page<T>`, `Slice<T>` va derived query nomlari JPQL semantikasiga bog'langan. `@Transactional` self-invocation muammosi ham oqib chiqadi: proxy-based AOP sababli bir sinf ichidagi metod chaqiruvi interceptor'dan o'tmaydi. `RestTemplate`/`RestClient` ustidagi o'ramlar `HttpClientErrorException` yoki `WebClientResponseException`ni to'g'ridan-to'g'ri yuqoriga chiqarib, HTTP detallarini domenga olib kiradi.

**Qo'llanish keyslari:**
- Entity'larni to'g'ridan-to'g'ri REST javobida qaytarganda `LazyInitializationException` olish - DTO va `@EntityGraph` bilan hal qilinadi.
- `@Transactional(readOnly = true)` ichida `findAll()` chaqirib, N+1 query muammosiga duch kelish.
- `CacheManager` abstraksiyasi ortidan Redis serializatsiya xatosi klientga `SerializationException` sifatida chiqishi.
- Feign/`RestClient` client interfeysi domen metodi ko'rinishida bo'lsa-da, timeout va 5xx xatolarini HTTP exception sifatida tarqatishi.
- `JdbcTemplate` ustidagi DAO qatlami `SQLException` vendor-specific kodlarini biznes qatlamiga o'tkazishi.

**Ehtiyot bo'ling:** Barcha oqishni yopishga urinish qalin, ortiqcha qatlamlarga olib keladi - Joel Spolsky aytganidek, hech bir abstraksiya 100% zich emas. To'g'ri yo'l: transaction chegarasini aniq belgilash, DTO proyeksiyalardan foydalanish va xatolarni qatlam chegarasida `DataAccessException` kabi umumiy ierarxiyaga tarjima qilish.

## 25.16 Interfeys Shishishi (Interface Bloat)

**Tavsif:** Bitta interfeys juda ko'p metodga ega bo'lib ketadi va implementatsiya qiluvchilar o'zlariga kerak bo'lmagan metodlarni ham amalga oshirishga majbur bo'ladi. Bu SOLID'ning Interface Segregation Principle (ISP) buzilishi hisoblanadi. Ko'pincha "universal servis" yoki "god interface" sifatida o'sadi: har bir yangi talab shu interfeysga yana bitta metod qo'shadi. Oqibatda mock yozish qiyinlashadi, implementatsiyalar `UnsupportedOperationException` bilan to'lib ketadi.

**Spring'da qayerda uchraydi:** Spring Data'ning `JpaRepository` o'zi 20+ metodni olib keladi (`findAll`, `deleteAllInBatch`, `flush`, `saveAllAndFlush`) - read-only aggregate uchun bu ortiqcha; buning yechimi `Repository<T, ID>` yoki `CrudRepository` o'rniga faqat kerakli metodlarni e'lon qiladigan o'z interfeysingiz. Spring Framework o'zi ISP'ga yaxshi misol: `BeanFactory`, `ApplicationEventPublisher`, `EnvironmentCapable`, `ResourceLoader` alohida interfeyslar bo'lib, `ApplicationContext` ularni kompozitsiya qiladi. Java 8+ `default` metodlari bu muammoni yumshatadi - `WebMvcConfigurer` va `HandlerInterceptor` barcha metodlarini `default` qilgani uchun implementatsiya faqat kerakligini override qiladi (eski `WebMvcConfigurerAdapter` Spring 5'dan deprecated). `@RepositoryDefinition` annotatsiyasi ham tor repository e'lon qilish imkonini beradi.

**Qo'llanish keyslari:**
- Read-only `ProductCatalogQuery` interfeysini `JpaRepository` o'rniga faqat `findBySku` va `findActive` metodlari bilan e'lon qilish.
- CQRS'da command va query interfeyslarini ajratish, bitta `OrderService`ga 30 metod to'plamaslik.
- `HandlerInterceptor`ni implement qilganda `default` metodlar hisobiga faqat `preHandle`ni yozish.
- Test uchun mock qilinadigan port interfeysini 2-3 metodga qisqartirib, Mockito stub'larini soddalashtirish.
- `PaymentGateway` interfeysini `Chargeable`, `Refundable`, `Tokenizable` kabi role interfeyslarga bo'lish.

**Ehtiyot bo'ling:** Teskari tomonga o'tib ketib, har bir metod uchun alohida interfeys yaratish (interface explosion) kod navigatsiyasini buzadi va bog'liqliklar sonini oshiradi. Interfeysni iste'molchi nuqtai nazaridan ajratish kerak - kim qanday rolni ishlatadi, shu role interface bo'ladi.

## 25.17 Ketma-ket Bog'liqlik (Sequential Coupling)

**Tavsif:** Obyekt metodlari faqat ma'lum tartibda chaqirilganda to'g'ri ishlaydi, lekin bu tartib API'da hech qanday tarzda majburlanmagan. Klient `init()` → `configure()` → `execute()` ketma-ketligini eslab qolishga majbur, aks holda `IllegalStateException` yoki jim buzilish yuz beradi. Bu "temporal coupling" deb ham ataladi va holatni (state) tashqariga oshkor qiladigan mutable obyektlarda ko'p uchraydi. Yechim - konstruktorda to'liq initsializatsiya, builder pattern yoki template method bilan tartibni kodning o'zida qulflash.

**Spring'da qayerda uchraydi:** Spring o'zi bu muammoni lifecycle callback'lari bilan boshqaradi: `InitializingBean.afterPropertiesSet()`, `@PostConstruct` (`jakarta.annotation.PostConstruct`), `SmartInitializingSingleton.afterSingletonsInstantiated()` va `DisposableBean.destroy()`. Mutable konteyner API'larida tartib muhim: `GenericApplicationContext`da `registerBean(...)` chaqiruvlari `refresh()`dan oldin bo'lishi shart, aks holda `IllegalStateException` otiladi. `RestTemplateBuilder` va `WebClient.Builder` immutable builder bo'lgani uchun xavfsiz, lekin xom `RestTemplate`ga `setInterceptors` chaqirish ishlatilgandan keyin ta'sir qilmaydi. `MockMvc` va `RestClient.Builder` zanjirlari ham `build()`dan keyin o'zgartirishni qabul qilmaydi. `@Transactional` metod ichida `EntityManager.flush()` tartibiga tayanadigan kod ham shu anti-patternning ko'rinishi.

**Qo'llanish keyslari:**
- `@PostConstruct` o'rniga konstruktor injection ishlatib, bean yaratilgan payti to'liq valid bo'lishini ta'minlash.
- Builder pattern bilan `OrderRequest.builder().customer(c).items(i).build()` - `build()` ichida invariantlarni tekshirish.
- Template Method yoki `TransactionTemplate.execute(...)` bilan "ochish-bajarish-yopish" tartibini framework ichida qulflash.
- `try-with-resources` va `AutoCloseable` orqali resurs yopilishini majburlash, qo'lda `close()` chaqirishga tayanmaslik.
- State machine (masalan Spring Statemachine yoki enum-based FSM) bilan ruxsat etilgan o'tishlarni aniq e'lon qilish.

**Ehtiyot bo'ling:** `@PostConstruct` ichida boshqa bean'lardan foydalanish xavfli - o'sha bean hali to'liq initsializatsiya qilinmagan bo'lishi mumkin; bunday holatda `ApplicationReadyEvent` yoki `SmartInitializingSingleton` ishlatish to'g'riroq. Tartibni faqat Javadoc bilan hujjatlashtirish yetarli emas, kompilyator yoki runtime tekshiruvi bilan majburlash kerak.

## 25.18 Siklik Bog'liqlik (Circular Dependency)

**Tavsif:** Ikki yoki undan ortiq komponent bir-biriga bog'liq bo'lib, yopiq halqa hosil qiladi: A → B → C → A. Bu dizayndagi noto'g'ri mas'uliyat taqsimotining belgisi - komponentlar mustaqil test qilinmaydi, alohida deploy qilinmaydi va o'zgarish halqa bo'ylab tarqaladi. Modul darajasida sikl Maven/Gradle build grafini ham buzadi. Yechim - umumiy qismni uchinchi komponentga ajratish, event-driven aloqaga o'tish yoki Dependency Inversion bilan yo'nalishni teskari qilish.

**Spring'da qayerda uchraydi:** Spring Boot 2.6'dan beri circular reference'lar **default holda o'chirilgan**: konteyner `BeanCurrentlyInCreationException` otadi va uni qayta yoqish uchun `spring.main.allow-circular-references=true` kerak (bu vaqtincha chora). Konstruktor injection siklni darhol fosh qiladi, setter yoki field injection esa uni yashiradi. `@Lazy` yoki `ObjectProvider<T>`/`ObjectFactory<T>` siklni texnik jihatdan "yechadi", lekin dizayn muammosini qoldiradi. Modul darajasida nazorat uchun ArchUnit (`SlicesRuleDefinition.slices().matching("..service.(*)..").should().beFreeOfCycles()`) yoki Spring Modulith'ning `ApplicationModules.verify()` ishlatiladi. Spring Modulith named interface va `@ApplicationModuleListener` orqali modullar o'rtasida event-based, bir yo'nalishli aloqani rag'batlantiradi.

**Qo'llanish keyslari:**
- `UserService` va `NotificationService` o'rtasidagi siklni `ApplicationEventPublisher` + `@TransactionalEventListener` bilan uzish.
- Umumiy logikani `UserValidator` kabi uchinchi, bog'liqliksiz komponentga chiqarish.
- Spring Modulith `ApplicationModules.of(App.class).verify()` testini CI'ga qo'shib, modul sikllarini bloklash.
- ArchUnit qoidasi bilan `controller → service → repository` yo'nalishini bir tomonlama qilib qulflash.
- Monolitdan microservice ajratishda sinxron ikki tomonlama REST chaqiruvlarni outbox + Kafka event'ga almashtirish.

**Ehtiyot bo'ling:** `@Lazy` yoki `spring.main.allow-circular-references=true` - bu diagnostika emas, muammoni ko'mish; proxy ichida haqiqiy obyekt birinchi chaqiruvda yaratiladi va startup xatolari runtime'ga ko'chadi. Sikl paydo bo'lganda avval "bu ikki sinf aslida bitta mas'uliyatmi yoki uchinchi abstraksiya kerakmi?" degan savolni bering.

## 25.19 Primitivlarga Berilish (Primitive Obsession)

**Tavsif:** Domen tushunchalari o'rniga hamma joyda `String`, `int`, `long`, `BigDecimal` kabi primitiv tiplar ishlatiladi. Natijada validatsiya logikasi butun kod bo'ylab takrorlanadi, kompilyator xato argument tartibini ushlay olmaydi va domen tili kodda ko'rinmaydi. `transfer(String from, String to, BigDecimal amount)` chaqiruvida `from` va `to`ni almashtirib qo'ysangiz, kompilyator jim turadi. Yechim - Value Object: `AccountId`, `Money`, `EmailAddress` kabi kichik, immutable, o'zini validatsiya qiladigan tiplar.

**Spring'da qayerda uchraydi:** Java 17+ `record` Value Object uchun ideal: `record Money(BigDecimal amount, Currency currency) {}` - compact konstruktorda invariant tekshiriladi. JPA'da bunday tiplar `@Embeddable` + `@Embedded` yoki `AttributeConverter<X, String>` (`@Converter(autoApply = true)`) bilan map qilinadi; Hibernate 6'da `@JavaType`/`@CompositeType` ham bor. Spring Data JDBC uchun `@WritingConverter`/`@ReadingConverter` va `@ConfigurationPropertiesBinding` qo'llangan `Converter<String, Money>` ishlatiladi. Web qatlamida `Converter<S, T>` yoki `Formatter<T>`ni `WebMvcConfigurer.addFormatters(FormatterRegistry)` orqali registratsiya qilib, `@PathVariable AccountId id` to'g'ridan-to'g'ri bind qilinadi. Validatsiya uchun Jakarta Bean Validation (`@Email`, `@Positive`) va custom `ConstraintValidator`, konfiguratsiya uchun `@ConfigurationProperties` bilan `Duration`, `DataSize` kabi tayyor tiplar mavjud.

```java
public record Money(BigDecimal amount, Currency currency) {
    public Money {
        Objects.requireNonNull(currency, "currency");
        if (amount.signum() < 0) throw new IllegalArgumentException("negative");
        amount = amount.setScale(currency.getDefaultFractionDigits(), RoundingMode.UNNECESSARY);
    }
    public Money plus(Money other) {
        if (!currency.equals(other.currency)) throw new IllegalArgumentException("mismatch");
        return new Money(amount.add(other.amount), currency);
    }
}
```

**Qo'llanish keyslari:**
- `BigDecimal` + `String currency` juftligi o'rniga `Money` record ishlatib, valyuta aralashuvini kompilyatsiya/runtime'da bloklash.
- `String userId` o'rniga `UserId` record - `AttributeConverter` bilan JPA ustuniga map qilinadi.
- `String email`ni `EmailAddress` ga aylantirib, regex validatsiyasini bitta joyda saqlash.
- `long millis` o'rniga `java.time.Duration` va `@ConfigurationProperties`da `30s` ko'rinishida yozish.
- `int` status kodlari o'rniga `enum OrderStatus` - `switch` ustida exhaustiveness tekshiruvi ishlaydi.

**Ehtiyot bo'ling:** Har bir maydonni o'rab chiqish ham mantiqsiz - faqat o'zining qoidalari, validatsiyasi yoki xatti-harakati bor tushunchalarni wrap qiling, aks holda boilerplate va serializatsiya murakkabligi o'sadi. Jackson uchun `@JsonValue`/`@JsonCreator` qo'shishni va `equals`/`hashCode` semantikasini (record buni bepul beradi) tekshirishni unutmang.

## 25.20 Begona Ma'lumotga Havas (Feature Envy)

**Tavsif:** Bitta sinfdagi metod o'z maydonlariga emas, boshqa sinfning ma'lumotlariga ko'proq qiziqadi: uning getter'larini ketma-ket chaqirib, hisob-kitobni o'zida bajaradi. Bu ma'lumot va xatti-harakat ajralib ketganining belgisi - klassik "anemic domain model" ko'rinishi. Natijada biznes qoidalari servis qatlamida tarqalib ketadi va bir xil hisob bir necha joyda takrorlanadi. Yechim - Move Method refaktoringi: logikani ma'lumot egasi bo'lgan sinfga ko'chirish (Tell, Don't Ask).

**Spring'da qayerda uchraydi:** Eng ko'p uchraydigan joy - `@Service` sinflari: `OrderService.calculateTotal(Order o)` metodi `o.getItems()`, `item.getPrice()`, `item.getQuantity()`, `o.getDiscount()`ni chaqirib yig'indi hisoblaydi, holbuki bu `Order.total()` metodi bo'lishi kerak. Lombok'ning `@Data`/`@Getter @Setter` barcha maydonlarni ochib, entity'larni passiv ma'lumot sumkasiga aylantirishi bilan bu anti-patternni rag'batlantiradi. Spring Data JPA entity'lari (`@Entity`) odatda biznes metodlarini o'zida saqlashi mumkin - agregat ildizi sifatida `AbstractAggregateRoot<T>`dan (Spring Data Commons) foydalanib `registerEvent(...)` bilan domen event'larini ham chiqarish mumkin. MapStruct (`@Mapper`) yoki qo'lda yozilgan DTO mapper'lar - bu joyda **qonuniy** feature envy: mapper'ning ishi aynan boshqa obyekt maydonlarini o'qish.

**Qo'llanish keyslari:**
- `OrderService.calculateTotal(order)`ni `order.total()` metodiga ko'chirib, narx qoidasini agregat ichida saqlash.
- `InvoiceValidator` ichidagi `invoice.getLines()` bo'yicha tsikllarni `Invoice.isBalanced()` metodiga olib kirish.
- `Money` arifmetikasini `BigDecimal` manipulyatsiyasi sifatida servisda emas, `Money.plus/minus` ichida saqlash.
- Status o'tishlarini `if (order.getStatus() == NEW) order.setStatus(PAID)` o'rniga `order.markPaid()` bilan ifodalash.
- Spring Modulith'da domen logikasini modul ichidagi agregatga to'plab, servisni faqat orkestratsiya va transaction chegarasi uchun qoldirish.

**Ehtiyot bo'ling:** Hamma narsani entity'ga ko'chirish entity'ni "god object"ga aylantiradi va JPA entity'siga infratuzilma bog'liqliklarini (repository, HTTP client) inyeksiya qilish vasvasasi paydo bo'ladi. Bir necha agregat ustida ishlaydigan koordinatsiya, transaction va tashqi integratsiya `@Service`da qolishi to'g'ri; mapper va serializatsiya kodida feature envy normal hol.

## 25.21 Sochma Jarrohlik (Shotgun Surgery)

**Tavsif:** Bitta mantiqiy o'zgarishni amalga oshirish uchun ko'p sonli fayl va modulda kichik tahrirlar qilish kerak bo'ladi. Bu past kohezioning (low cohesion) va tarqalib ketgan mas'uliyatning belgisi: bir tushuncha bir joyda emas, o'nlab joyda ifodalangan. Har bir bunday o'zgarish kamida bitta joyni o'tkazib yuborish riskini olib keladi. Yechim - bog'liq xatti-harakatlarni bitta modul yoki abstraksiyaga to'plash (Move/Inline refaktoringlari, cross-cutting logikani AOP'ga chiqarish).

**Spring'da qayerda uchraydi:** Yangi maydon qo'shish uchun entity, DTO, mapper, Liquibase/Flyway migratsiya, validatsiya, OpenAPI sxemasi va testlarni birga o'zgartirish - qisman muqarrar, lekin agar bitta maydon 15 faylga tegsa, bu signal. Cross-cutting logika uchun Spring tayyor markazlashtirish nuqtalarini beradi: `@Aspect` + `@Around` (Spring AOP), `@ControllerAdvice`/`@RestControllerAdvice` bilan `@ExceptionHandler` markazlashtirilgan xato ishlovi, `HandlerInterceptor` yoki `OncePerRequestFilter` bilan request-scoped logika, `@Transactional` va `@Cacheable` bilan deklarativ kesimlar. Konfiguratsiya tarqalishini `@ConfigurationProperties` bitta tipga yig'ish bilan to'xtatish mumkin; auto-configuration esa `AutoConfiguration.imports` fayli orqali bitta starter modulida saqlanadi. Spring Modulith modul chegaralarini majburlab, o'zgarish radiusini bitta paket ostiga cheklaydi.

**Qo'llanish keyslari:**
- Har bir controller'dagi `try/catch`ni olib tashlab, `@RestControllerAdvice` + `ProblemDetail` (RFC 9457) bilan bitta joyda xato formatini belgilash.
- 20 ta servisdagi takroriy audit logging kodini bitta `@Aspect`ga ko'chirish.
- Tarqalib ketgan `@Value("${...}")` chaqiruvlarini bitta `@ConfigurationProperties` record'ga yig'ish.
- Umumiy infratuzilma sozlamalarini ichki starter (`spring-boot-autoconfigure` uslubida) qilib, har bir servisda takrorlamaslik.
- Korrelyatsiya ID'sini har bir log chaqiruviga qo'lda qo'shish o'rniga Micrometer Tracing/MDC filtri bilan markazlashtirish.

**Ehtiyot bo'ling:** Markazlashtirishni haddan oshirsangiz, teskari muammo - Divergent Change (bitta sinf har xil sabablarga ko'ra tez-tez o'zgaradi) va yashirin "sehr" paydo bo'ladi; AOP debug qilish ancha qiyin. Qoidani belgilash uchun ArchUnit yoki Modulith verifikatsiyasini ishlatib, mas'uliyat chegaralarini kodda qulflang.

## 25.22 Uzun Parametrlar Ro'yxati (Long Parameter List)

**Tavsif:** Metod yoki konstruktor juda ko'p parametr qabul qiladi, ayniqsa bir xil tipdagi ketma-ket parametrlar. Bu chaqiruv joyini o'qib bo'lmaydigan qilib qo'yadi va bir xil tipli argumentlarni almashtirib qo'yish xavfini keltiradi - kompilyator bunday xatoni ushlamaydi. Ko'pincha bu yashirin tushunchaning mavjudligidan darak beradi: parametrlar aslida bitta obyektga tegishli. Yechim - Parameter Object, Builder pattern yoki Value Object'lar bilan tiplashtirish.

**Spring'da qayerda uchraydi:** Spring'da konstruktor injection standart bo'lgani uchun 10+ bog'liqlikka ega konstruktor paydo bo'lishi mumkin - bu DI muammosi emas, balki sinfning juda ko'p ishni bajarayotgani haqidagi eng aniq signal (Lombok `@RequiredArgsConstructor` bu signalni yashiradi). HTTP qatlamida uzun `@RequestParam` ro'yxati o'rniga Spring `@ModelAttribute` yoki `@ConstructorBinding` uslubidagi record DTO'ni qo'llab-quvvatlaydi; Spring Framework 6.1+ esa `@RequestParam`larni to'g'ridan-to'g'ri record'ga bind qiladigan metod argument'lari uchun qo'llab-quvvatlashga ega. Ko'p filtrli so'rovlar uchun Spring Data `Specification<T>`, `Example<T>`/`QueryByExampleExecutor` va `Pageable`/`Sort` obyektlari parametrlarni guruhlash uchun tabiiy yo'l. Builder uslubi Spring'ning o'zida keng: `WebClient.builder()`, `RestClient.builder()`, `UriComponentsBuilder`, `SpringApplicationBuilder`.

**Qo'llanish keyslari:**
- `searchOrders(String customer, String status, LocalDate from, LocalDate to, int page, int size)` → `searchOrders(OrderSearchCriteria criteria, Pageable pageable)`.
- 12 bog'liqlikli `@Service` konstruktorini ikki-uch tor servisga bo'lib, mas'uliyatni ajratish.
- Controller'da ko'p `@RequestParam` o'rniga `@ModelAttribute OrderFilter filter` record ishlatish.
- Test ma'lumotlari uchun Builder yoki Object Mother qo'llab, 15 argumentli konstruktordan voz kechish.
- `boolean`/`String` ketma-ketligini `enum` va Value Object'lar bilan almashtirib, almashtirib qo'yish xavfini yo'qotish.

**Ehtiyot bo'ling:** Parametrlarni shunchaki `Map<String, Object>` yoki umumiy "context" obyektiga tashlash muammoni yomonlashtiradi - tip xavfsizligi yo'qoladi va Stringly Typed anti-patternga o'tasiz. Parameter Object faqat parametrlar haqiqatan mantiqiy bir butun bo'lganda ma'noli; aks holda sinfni bo'lish to'g'riroq.

## 25.23 G'ildirakni Qaytadan O'ylab Topish (Reinventing the Wheel)

**Tavsif:** Standart kutubxona yoki framework allaqachon hal qilgan muammoni noldan, o'z qo'lda yozilgan yechimi bilan qayta hal qilish. Bunday kod sinovdan o'tmagan, edge-case'larni qamramagan, hujjatsiz va xavfsizlik auditidan o'tmagan bo'ladi. Ayniqsa xavfli sohalar: kriptografiya, parol hashing, sana-vaqt arifmetikasi, konkurensiya primitivlari, retry va connection pool mantig'i. Yechim - avval ekotizimni tekshirish, keyin yozish; va yozish kerak bo'lsa, farqni aniq hujjatlashtirish.

**Spring'da qayerda uchraydi:** Spring ekotizimi deyarli har bir infratuzilma masalasiga tayyor javob beradi: autentifikatsiya uchun Spring Security (`BCryptPasswordEncoder`, `Argon2PasswordEncoder`, `DelegatingPasswordEncoder`) - hech qachon o'z MD5/SHA hashini yozmang; retry va circuit breaker uchun Spring Retry (`@Retryable`, `RetryTemplate`) yoki Resilience4j (`@CircuitBreaker`, `@RateLimiter`); connection pool uchun HikariCP (Boot'ning default'i); scheduling uchun `@Scheduled`/`TaskScheduler` yoki Quartz; cache uchun `@Cacheable` + Caffeine/Redis; metrika va tracing uchun Micrometer va Micrometer Tracing (OpenTelemetry bridge); JSON uchun Jackson, validatsiya uchun Hibernate Validator; batch uchun Spring Batch. Umumiy yordamchi kod uchun `org.springframework.util.StringUtils`, `CollectionUtils`, `ObjectUtils`, `Assert`, `StreamUtils` va Java'ning o'zidagi `java.time`, `java.util.concurrent`, `HttpClient` mavjud.

**Qo'llanish keyslari:**
- O'z JWT parser'ini yozish o'rniga Spring Security OAuth2 Resource Server (`spring-boot-starter-oauth2-resource-server`) va `NimbusJwtDecoder`dan foydalanish.
- Qo'lda `while (retry < 3)` tsikli o'rniga `@Retryable(maxAttempts = 3, backoff = @Backoff(delay = 200, multiplier = 2))`.
- O'z DB migratsiya skript yugurtirgichi o'rniga Flyway yoki Liquibase integratsiyasini ishlatish.
- Qo'lda `ThreadPoolExecutor` sozlash o'rniga `@EnableAsync` + `ThreadPoolTaskExecutor` yoki Java 21 virtual thread'lar (`spring.threads.virtual.enabled=true`).
- O'z rate limiter'ini yozish o'rniga Resilience4j `RateLimiter` yoki Bucket4j'ni qo'llash.

**Ehtiyot bo'ling:** Teskari xato ham bor - har bir mayda ehtiyoj uchun yangi bog'liqlik qo'shish supply-chain riski, CVE yuzasi va transitive konflikt (`spring-boot-dependencies` BOM buni yumshatadi) keltiradi. Qaror mezoni: muammo sizning domeningizning raqobat ustunligimi (unda yozing) yoki standart infratuzilmami (unda kutubxona oling).

## 25.24 Ichki Platforma Effekti (Inner-Platform Effect)

**Tavsif:** Tizim shunchalik "moslashuvchan" qilib quriladi ki, u o'zining ichida yangi, lekin zaifroq programmalash platformasini qayta ixtiro qiladi. Odatda bu ma'lumotlar bazasidagi jadvallardan o'qiladigan "qoidalar dvigateli", XML/YAML'da yozilgan "DSL" yoki har qanday xatti-harakatni konfiguratsiya orqali o'zgartirish imkonini beradigan generic metamodel ko'rinishida bo'ladi. Natijada: debugger ishlamaydi, kompilyator yordam bermaydi, IDE refaktoring qilmaydi, test yozish qiyin va faqat bir-ikki odam tushunadigan "framework" paydo bo'ladi. Greenspun qoidasi aytganidek, bunday tizim oxir-oqibat to'liq, lekin yomon implementatsiya qilingan tilga aylanadi.

**Spring'da qayerda uchraydi:** Klassik ko'rinish - DB'dagi `rule` jadvalidan SpEL ifodalarini o'qib `SpelExpressionParser` bilan runtime'da bajarish, yoki `BeanDefinitionRegistryPostProcessor` orqali metadata asosida dinamik bean'lar generatsiya qilish. Yana bir ko'rinish - EAV (entity-attribute-value) sxemasi: `@Entity` ichida `Map<String, String> attributes` bo'lib, barcha domen maydonlari qator sifatida saqlanadi; natijada JPA query, indeks va tip xavfsizligi yo'qoladi. Agar qoidalar dvigateli haqiqatan kerak bo'lsa, tayyor yechimlar bor: Drools, Camunda/Flowable (BPMN), Spring Statemachine, Spring Cloud Function, yoki JSR-223 (`ScriptEngineManager`) orqali boshqarilgan skriptlash. Spring'ning o'z profiles (`@Profile`), `Environment`, `@ConditionalOnProperty` va feature flag kutubxonalari (Togglz, Unleash, FF4j) ko'p hollarda o'z konfiguratsiya tilini yozish ehtiyojini yo'q qiladi.

**Qo'llanish keyslari:**
- DB'dagi "qoida" jadvallari o'rniga Strategy pattern + `@Component` bean'lar va `Map<String, PricingStrategy>` injection ishlatish.
- Biznes qoidalari haqiqatan tez-tez o'zgarsa, o'z interpretatoringiz o'rniga Drools yoki Camunda DMN jadvallarini olish.
- Xatti-harakat variantlarini feature flag (`@ConditionalOnProperty`, Unleash) bilan boshqarib, dinamik kod generatsiyasidan voz kechish.
- Dinamik forma maydonlarini EAV o'rniga PostgreSQL `jsonb` ustuni + Hibernate 6 `@JdbcTypeCode(SqlTypes.JSON)` bilan saqlash.
- Multi-tenant sozlamalarni `@ConfigurationProperties` ierarxiyasi va Spring Cloud Config'ga yuklab, o'z "sozlama interpretatori"ni yozmaslik.

**Ehtiyot bo'ling:** Haqiqiy talab "biznes foydalanuvchisi qoidani o'zi o'zgartirsin" bo'lsa, buni tan olib sanoat standartidagi qoidalar dvigatelini oling - lekin shunda ham versiyalash, test va audit mexanizmlarini birinchi kundan qo'ying. Konfiguratsiya orqali boshqariladigan har bir yangi "hook" - bu kelajakdagi debug qilinmaydigan xato.

## 25.25 Spekulyativ Umumiylik / Ortiqcha Injinerlik (Speculative Generality / Over-engineering)

**Tavsif:** Hali mavjud bo'lmagan, faqat tasavvur qilinayotgan kelajak talablari uchun abstraksiya, interfeys va kengaytirish nuqtalari qurish. "Bir kun kelib boshqa DB'ga o'tamiz" yoki "ehtimol yana bitta provayder qo'shiladi" degan asosda qatlamlar, factory'lar va plugin mexanizmlari yaratiladi, lekin o'sha kun kelmaydi. Narxi real: har bir ortiqcha abstraksiya o'qish, debug va o'zgartirish xarajatini oshiradi, kod altitudini pasaytiradi. Yechim - YAGNI va "Rule of Three": uchinchi real holat paydo bo'lganda umumlashtirish.

**Spring'da qayerda uchraydi:** Eng ko'p uchraydigan ko'rinish - har bir `@Service` uchun bitta implementatsiyali interfeys yaratish (`UserService` + `UserServiceImpl`); Spring 5+ va CGLIB proxy bilan `@Transactional` interfeyssiz ham ishlaydi, shuning uchun bu interfeys faqat ko'rinish uchun qolgan (Mockito `mock(UserService.class)` konkret sinfni ham mock qila oladi). Boshqa misollar: bitta DB'da ishlaydigan loyihada o'z `Repository` abstraksiyasini Spring Data ustiga qo'yish; bitta REST kanal bor joyda to'liq hexagonal port/adapter to'plami; `AbstractBaseServiceImpl<T, ID, D>` kabi generic bazaviy sinflar; hech qachon ishlatilmaydigan `@Profile` va `@ConditionalOnProperty` shoxlari; bitta xabar turi uchun Spring Integration yoki Camel route'lari. Spring Boot'ning starter va auto-configuration mexanizmi aksariyat kengaytirish nuqtalarini allaqachon beradi - o'z plugin SPI'ngizni yozishdan oldin `ObjectProvider<List<T>>` yoki `@ConditionalOnMissingBean` yetarli emasligiga ishonch hosil qiling.

**Qo'llanish keyslari:**
- Bitta implementatsiyali `XServiceImpl` juftligini olib tashlab, konkret `@Service` sinfini qoldirish.
- Bir vaqtda faqat bitta provayder bor bo'lsa, Strategy interfeysini keyinroq, ikkinchi provayder kelganda kiritish.
- Generic `BaseEntity<ID>` ierarxiyasi o'rniga har bir agregatda kerakli maydonlarni aniq e'lon qilish.
- Ishlatilmayotgan `@Profile("legacy")` shoxlari va o'lik `@ConditionalOnProperty` sozlamalarini tozalash.
- Hexagonal arxitekturani butun monolitga emas, faqat chindan almashtirilishi mumkin bo'lgan integratsiya chegaralariga qo'llash.

**Ehtiyot bo'ling:** Teskari ekstremum ham xarajatli - keyinchalik qo'shish juda qimmat bo'ladigan chegaralarda (public API shartnomasi, DB sxemasi, xabar formati, xavfsizlik modeli) oldindan o'ylash o'zini oqlaydi. Mezon: o'zgarish narxi vaqt o'tishi bilan keskin oshadimi? Agar yo'q - kuting; agar ha - hozir qiling.

## 25.26 Singleton'dan Suiiste'mol / Statik Yopishqoqlik (Singleton abuse / Static Cling)

**Tavsif:** Global holat va statik metodlarga tayanish: `MyUtil.getInstance()`, statik mutable maydonlar, statik servis lokatori. Bu bog'liqliklarni yashiradi (konstruktorda ko'rinmaydi), test izolyatsiyasini buzadi (testlar bir-biriga holat orqali ta'sir qiladi), mock qilishni qiyinlashtiradi va konkurensiya xatolarini keltiradi. "Static cling" - kod statik chaqiruvga shunday mahkam yopishib qolgani sababli uni almashtirib bo'lmasligi. Yechim - Dependency Injection: bog'liqlikni konstruktor orqali oshkor qilish.

**Spring'da qayerda uchraydi:** Spring'ning bean'lari default `singleton` scope'da - bu GoF Singleton pattern'i emas, balki konteyner boshqaradigan, inyeksiya qilinadigan va test'da almashtiriladigan nusxa; shuning uchun o'z `getInstance()`ingiz kerak emas. Xavfli naqshlar: statik `ApplicationContextProvider implements ApplicationContextAware` orqali `context.getBean(...)` chaqirish (Service Locator anti-pattern), `SecurityContextHolder.getContext()`ni domen qatlamida to'g'ridan-to'g'ri ishlatish (`ThreadLocal`ga bog'lanish, virtual thread va reaktiv kontekstda muammoli - reaktivda `ReactiveSecurityContextHolder`), singleton bean ichida mutable instance maydon saqlash (thread-safety buzilishi; `@Scope("prototype")`, `@RequestScope` yoki stateless dizayn kerak). Statik vaqt uchun `LocalDate.now()` o'rniga `java.time.Clock` bean'ini inyeksiya qilish test qilishni osonlashtiradi (`Clock.fixed(...)`). Statik yordamchilar faqat toza funksiya bo'lsa maqbul: `StringUtils`, `Objects.requireNonNull`, `Assert.notNull`.

**Qo'llanish keyslari:**
- `ApplicationContextProvider.getBean(X.class)` statik yordamchisini konstruktor injection bilan almashtirish.
- `LocalDateTime.now()`ni `Clock` bean'iga ko'chirib, testda `Clock.fixed` bilan vaqtni qotirish.
- Legacy statik `CacheHolder`ni `@Cacheable` + `CacheManager` bean'iga o'tkazish.
- Singleton bean ichidagi mutable `List` maydonini olib tashlab, holatni metod parametriga yoki `@RequestScope` bean'ga ko'chirish.
- Statik `SecurityContextHolder` chaqiruvlarini servis chegarasida bir marta o'qib, pastga `AuthenticatedUser` parametri sifatida uzatish.

**Ehtiyot bo'ling:** `@Autowired` field injection ham yashirin bog'liqlik ko'rinishi - Spring rasmiy hujjatlari konstruktor injectionni tavsiya qiladi (immutable, majburiy bog'liqlik, testda `new` bilan yaratish mumkin). Singleton bean ichida har qanday mutable holat - bu potensial race condition; shared mutable state kerak bo'lsa, `ConcurrentHashMap`, `AtomicReference` yoki tashqi cache ishlatib, buni aniq hujjatlashtiring.

## 25.27 Satr Bilan Tiplash (Stringly Typed)

**Tavsif:** Tiplashtirilgan domen tushunchalari o'rniga hamma joyda `String` (yoki `Map<String, Object>`) ishlatiladi: status, rol, turi, kalit - barchasi erkin matn sifatida yuradi. Kompilyator "PAID" va "paid" o'rtasidagi farqni yoki xato yozilgan "PIAD"ni ushlamaydi; xato faqat runtime'da, ko'pincha productionda ko'rinadi. IDE autocomplete, refaktoring va `switch` exhaustiveness tekshiruvi ishlamaydi. Yechim - `enum`, sealed interface va Value Object'lar; serializatsiya chegarasida esa `String`ni darhol tipga aylantirish.

**Spring'da qayerda uchraydi:** Spring statik tiplashtirilgan alternativalarni keng beradi: web qatlamida `@PathVariable OrderStatus status` va `@RequestParam` `enum`ga avtomatik konvertatsiya qilinadi (`StringToEnumConverterFactory`), JPA'da `@Enumerated(EnumType.STRING)` (hech qachon `ORDINAL` emas), Jackson'da `@JsonValue`/`@JsonProperty` va `READ_UNKNOWN_ENUM_VALUES_AS_NULL`. Konfiguratsiya uchun `@Value("${...}")` satrlari o'rniga `@ConfigurationProperties` + record: `Duration`, `DataSize`, `Resource`, `enum` tiplari avtomatik bind qilinadi va `spring-boot-configuration-processor` metadata generatsiya qiladi. Cache nomlari, event turlari, header kalitlari uchun `String` literal o'rniga konstanta yoki `enum` ishlatish kerak; Spring'ning o'zi `HttpHeaders.CONTENT_TYPE`, `MediaType.APPLICATION_JSON`, `HttpStatus.NOT_FOUND` kabi tiplashtirilgan konstantalar beradi. Xavfli joy - SpEL ifodalari (`@PreAuthorize("hasRole('ADMIN')")`, `@Cacheable(key = "#id")`): bu satrlar kompilyatsiyada tekshirilmaydi, shuning uchun ularni integratsiya testlari bilan qoplash kerak.

**Qo'llanish keyslari:**
- `String status` maydonini `enum OrderStatus` ga o'tkazib, `@Enumerated(EnumType.STRING)` bilan saqlash.
- `Map<String, Object>` payload o'rniga record DTO + Jakarta Validation annotatsiyalari ishlatish.
- Cache nomlarini `@Cacheable("users")` satr literalidan `CacheNames.USERS` konstantasiga chiqarish.
- `@Value("${app.timeout}") String timeout` o'rniga `@ConfigurationProperties` record ichida `Duration timeout`.
- Rol nomlarini `enum Role` bilan e'lon qilib, `@PreAuthorize` SpEL satrlarini testda tekshirib chiqish.

**Ehtiyot bo'ling:** `enum`ni tashqi API shartnomasiga aylantirsangiz, yangi qiymat qo'shilishi eski klientlarni buzishi mumkin - kiruvchi ma'lumot uchun noma'lum qiymatni xushmuomala boshqarish (default yoki `null`) va chiquvchi uchun versiyalash strategiyasini o'ylang. DB'da `EnumType.ORDINAL` ishlatish esa `enum` tartibi o'zgarganda ma'lumotni jim buzadi.

## 25.28 Mantiqiy Qiymat Ko'rligi (Boolean Blindness)

**Tavsif:** `boolean` parametr yoki qaytaruvchi qiymat ma'noni yo'qotadi: `true`/`false` o'zi hech narsa aytmaydi va chaqiruv joyida `process(order, true, false, true)` ko'rinishidagi o'qib bo'lmaydigan kod paydo bo'ladi. Bir xil tipdagi flag'larni almashtirib qo'ysangiz, kompilyator jim turadi. Bundan tashqari, `boolean` faqat ikki holatni ifodalaydi - talab uchinchi holatni (masalan "noma'lum") qo'shsa, kod `Boolean` null bilan yoki qo'shimcha flag bilan buziladi. Yechim - `enum`, sealed interface, `Optional`, yoki flag'ni alohida nomlangan metodga ajratish.

**Spring'da qayerda uchraydi:** Java standart kutubxonasi va Spring bunga yaxshi misollar beradi: `Collectors.partitioningBy` o'rniga `groupingBy` + `enum`, `Boolean` o'rniga `java.time`ning `DayOfWeek` kabi aniq tiplari. Spring API'larida `boolean` flag'lar `enum`ga ko'chirilgan: `FetchType.LAZY/EAGER`, `Propagation.REQUIRED/REQUIRES_NEW`, `Isolation`, `MediaType`, `HttpStatus`, `RoundingMode`. Java 17+ sealed interface va pattern matching `switch` bilan natija turlarini `boolean` o'rniga aniq modellashtirish mumkin: `sealed interface PaymentResult permits Approved, Declined, Pending`. Metod darajasida flag o'rniga ikki metod to'g'riroq: `@Transactional(readOnly = true)` kabi framework flag'lari o'rinli, lekin domen metodida `save(order, true)` emas, `saveDraft(order)` va `publish(order)` bo'lishi kerak. Bean Validation'da `Boolean` uch holatli bo'lib qolmasligi uchun `@NotNull` majburlash, DTO'larda esa `Optional<Boolean>` o'rniga `enum` ishlatish tavsiya etiladi.

**Qo'llanish keyslari:**
- `sendEmail(user, true, false)` → `sendEmail(user, EmailFormat.HTML, Tracking.DISABLED)`.
- `boolean isActive` o'rniga `enum AccountState { ACTIVE, SUSPENDED, CLOSED }` - kelajakdagi holatlar uchun joy qoldiradi.
- `boolean` qaytaruvchi `validate()` o'rniga `ValidationResult` (sealed interface) qaytarib, xato sababini ham olib kelish.
- `Boolean` null-able flag o'rniga `enum ConsentStatus { GRANTED, DENIED, NOT_ASKED }` ishlatish.
- Repository'da `findByActive(boolean)` o'rniga `findByState(AccountState)` derived query'siga o'tish.

**Ehtiyot bo'ling:** Haqiqatan ikkilik, o'zgarmas tushunchalar uchun (`isEmpty()`, `hasNext()`, `@Transactional(readOnly = true)`) `boolean` eng sodda va to'g'ri tanlov - har bir flag'ni `enum`ga aylantirish ortiqcha shovqin. Mezon: flag chaqiruv joyida tushunarsiz bo'lsa, uchinchi holat ehtimoli bo'lsa yoki ikki va undan ortiq flag yonma-yon kelsa - tiplashtiring.

## 25.29 Maydonga Injeksiya (Field Injection)

**Tavsif:** Dependency'lar konstruktor orqali emas, balki bevosita maydonga `@Autowired` qo'yish bilan kiritiladi va Spring reflection yordamida private maydonni to'ldiradi. Bu kod yozishda qisqa ko'rinadi, lekin obyektning o'zi to'liq tuzilgan (fully constructed) bo'lishini kafolatlamaydi - bean yaratilgandan keyingina maydonlar to'ladi. Natijada sinf o'z dependency'larini yashiradi: tashqaridan qaraganda u hech narsaga bog'liq emasdek ko'rinadi. Shuningdek maydonni `final` qilib bo'lmaydi, ya'ni o'zgarmaslik (immutability) yo'qoladi.

**Spring'da qayerda uchraydi:** `@Autowired` annotatsiyasi maydon ustida, `AutowiredAnnotationBeanPostProcessor` orqali reflection bilan `Field.set()` chaqiriladi; `@Value`, `@Inject` (JSR-330), `@PersistenceContext` ham shu yo'l bilan ishlatiladi. Spring Framework 4.3'dan boshlab bitta konstruktorli bean uchun `@Autowired` shart emas, Spring Boot 3.x/4.x'da esa konstruktor inyeksiyasi rasmiy tavsiya; Lombok'ning `@RequiredArgsConstructor` bilan birgalikda `private final` maydonlar standart yondashuvga aylangan. IntelliJ IDEA va SonarQube (`java:S6813` qoidasi) maydonga inyeksiyani ogohlantirish sifatida belgilaydi.

**Qo'llanish keyslari:**
- Legacy XML-asosli loyihada ko'p dependency'li `@Service` sinflari konstruktorni "og'ir" qilmaslik uchun maydonga inyeksiya qilingan.
- Abstract base sinfda `protected @Autowired` maydon qo'yilib, barcha subclass'lar undan foydalanishi (konstruktor zanjirini yozmaslik uchun).
- `@Configuration` sinfida `@Value` bilan property'larni to'g'ridan-to'g'ri maydonga olish.
- Test sinfida `@Autowired` maydon - bu yerda `@SpringBootTest` kontekst o'zi to'ldirgani uchun odatda qabul qilinadi.
- Circular dependency'ni "yashirish" uchun maydonga o'tish - bu muammoni tuzatmaydi, faqat ko'rinmas qiladi.

**Ehtiyot bo'ling:** Maydonga inyeksiya qilingan sinfni oddiy `new` bilan unit test qilib bo'lmaydi - yoki reflection, yoki `ReflectionTestUtils`, yoki butun Spring kontekst kerak bo'ladi. Bundan tashqari u ko'p dependency'ni osonlik bilan "yopib" tashlaydi, shuning uchun 10 ta maydonli God Service paydo bo'lishini sezmasdan qolasiz; konstruktor inyeksiyasida bunday sinf parametr ro'yxati bilan o'zini darhol fosh qiladi.

## 25.30 O'z-o'ziga Chaqiruv Proxy'ni Buzishi (Self-invocation breaking @Transactional / @Cacheable)

**Tavsif:** Spring'ning AOP-asosidagi annotatsiyalari proxy orqali ishlaydi: tashqi chaqiruvchi proxy'ga murojaat qiladi, proxy esa interceptor zanjirini ishga tushirib, keyin haqiqiy obyektni chaqiradi. Agar bean o'z metodini `this.method()` orqali chaqirsa, chaqiruv proxy'dan o'tmaydi va annotatsiya butunlay e'tiborsiz qoladi. Shu sababli `@Transactional`, `@Cacheable`, `@Async`, `@Retryable`, `@PreAuthorize` indamay ishlamay qo'yadi - exception ham, warning ham bo'lmaydi. Bu Spring'dagi eng ko'p takrorlanadigan "jim xato".

**Spring'da qayerda uchraydi:** `JdkDynamicAopProxy` va CGLIB-asosidagi `ObjenesisCglibAopProxy`, `TransactionInterceptor`, `CacheInterceptor`, `AsyncAnnotationAdvisor` - barchasi proxy darajasida tutadi. Yechimlar: dependency'ni ikkita bean'ga ajratish; `@EnableAspectJAutoProxy(exposeProxy = true)` bilan `AopContext.currentProxy()`; `ObjectProvider<SelfType>` yoki `@Lazy` bilan o'ziga reference olish; yoki `@EnableTransactionManagement(mode = AdviceMode.ASPECTJ)` bilan compile/load-time weaving. Spring Framework 6.x'da bu semantika o'zgarmagan va `TransactionalProxyTests` hali ham shu xatti-harakatni tasdiqlaydi.

**Qo'llanish keyslari:**
- Service ichidagi public `importAll()` metodi har bir qator uchun `this.saveOne()` (`@Transactional(propagation = REQUIRES_NEW)`) ni chaqiradi - har biri alohida transaction bo'lishi kutilgan, lekin hammasi bitta transaction'da ketadi.
- `@Cacheable` qo'yilgan `findById()` o'sha sinf ichidan chaqirilganda cache hech qachon o'qilmaydi va DB har safar uriladi.
- Controller'ni emas, service'ni refactoring qilgandan so'ng `@Async` metodi sinxron ishlab, response vaqti sekinlashgani sezilmay qolishi.
- `@Retryable` qo'yilgan ichki metod self-invocation sababli retry qilmaydi va birinchi xatolikda yiqiladi.
- Metodni `private` yoki `final` qilish ham xuddi shu natijaga olib keladi - CGLIB uni override qila olmaydi.

**Ehtiyot bo'ling:** `AopContext.currentProxy()` ishlaydi, lekin kodni Spring'ga qattiq bog'laydi va testni qiyinlashtiradi - buning o'rniga mantiqni alohida bean'ga ko'chirish toza yechim. Integration testda `TransactionSynchronizationManager.isActualTransactionActive()` yoki log'da `TransactionInterceptor` DEBUG darajasini yoqib, transaction chindan ham boshlanganini tekshirib ko'ring.

## 25.31 Public Bo'lmagan Metodda @Transactional (@Transactional on Non-Public Methods)

**Tavsif:** Proxy-asosidagi transaction rejimida annotatsiya metodga uch sababdan tegmay qolishi mumkin. Birinchisi ko'rinish: Spring 6.0 dan beri class-based (CGLIB) proxy da `protected` va package-private metodlar ham tranzaksion bo'la oladi, lekin `private` va `final` metod hech qachon ishlamaydi, chunki CGLIB proxy target sinfning subclass'i va bu metodlarni override qila olmaydi. Ikkinchisi proxy turi: interface (JDK dynamic proxy) rejimida tranzaksion metod `public` bo'lishi va proxy qilinayotgan interface da e'lon qilinishi shart. Uchinchisi chaqiruv yo'li: ikki rejimda ham faqat proxy orqali kelgan tashqi chaqiruv ushlanadi, ya'ni `this` orqali self-invocation annotatsiyani chetlab o'tadi. Uchalasi ham kompilyatsiyada ham, startup'da ham ko'rinmaydi: ishlab chiquvchi transaction mavjud deb o'ylaydi, lekin har bir repository chaqiruvi o'zining auto-commit konteksida bajariladi va rollback ishlamaydi.

**Spring'da qayerda uchraydi:** `AbstractFallbackTransactionAttributeSource.computeTransactionAttribute()` `allowPublicMethodsOnly()` rost bo'lgan holatda public bo'lmagan metodni o'tkazib yuboradi. Bazaviy implementatsiya `false` qaytaradi, `AnnotationTransactionAttributeSource` esa uni `publicMethodsOnly` flagidan oladi, `@EnableTransactionManagement` (shu bilan Spring Boot ham) 6.0 dan beri bu bean'ni `new AnnotationTransactionAttributeSource(false)` bilan yasaydi. 5.3 gacha default public-only edi. Flagni orqaga qaytarish mumkin (`new AnnotationTransactionAttributeSource(true)` yoki `setPublicMethodsOnly(true)`), `private` va `final` uchun esa flagning ahamiyati yo'q: cheklov CGLIB ning o'zida. AspectJ weaving (`@EnableTransactionManagement(mode = AdviceMode.ASPECTJ)` bilan `spring-aspects` moduli va `AnnotationTransactionAspect`) `private` metodni va self-invocation ni ham qamraydi, lekin u yagona yo'l emas, eng qimmat yo'l. `@Cacheable` (`CacheInterceptor`) va `@Async` xuddi shu proxy mexanizmida ishlaydi, shuning uchun `private`, `final` va self-invocation cheklovi ularga ham tegishli.

**Qo'llanish keyslari:**
- Public `process()` metodi ichidan `private @Transactional void persist()` chaqirilgan va rollback kutilgan - aslida transaction hech qachon boshlanmaydi.
- Interface'i bor bean (JDK dynamic proxy): tranzaksion metod proxy qilinayotgan interface da e'lon qilinmagan, shuning uchun proxy uni ko'rmaydi va chaqiruv to'g'ridan to'g'ri target'ga tushadi.
- Kotlin da sinf va metod standart `final`: `kotlin("plugin.spring")` (allopen) ulanmasa, ochiq sinfdagi `final` metodga `@Transactional` qo'llanmaydi: chaqiruv proxy nusxasining o'zida bajariladi, u yerda injekt qilingan maydonlar `null`, natija tranzaksiyasiz ish yoki `NullPointerException`; `final` sinf esa startup da CGLIB xatosi bilan yiqiladi.
- 5.x dan 6.x ga ko'tarilish: ilgari jim e'tiborsiz qolgan `protected` yoki package-private `@Transactional` endi kuchga kirib, kutilmagan joyda yangi transaction chegarasi paydo bo'lishi.
- `TransactionAttributeSource` ni qo'lda bean qilib e'lon qilish: argumentsiz `new AnnotationTransactionAttributeSource()` da `publicMethodsOnly` `true` bo'ladi va `@EnableTransactionManagement` bergan default bosilib ketadi.

**Ehtiyot bo'ling:** SonarQube `java:S2230` ("Methods with Spring proxying annotations should be public") bu holatni aniqlaydi va CI'da yoqib qo'yishga arziydi, lekin qoida Spring versiyasiga bog'langan: o'z ta'rifiga ko'ra 5.x gacha har qanday public bo'lmagan metodni, 6.x da esa faqat `private` metodni belgilaydi. Shuning uchun topilmani loyihaning Spring versiyasi bilan birga o'qish kerak. Self-invocation ni bu qoida ko'rmaydi, u alohida qoida. Eng arzon yechim: transaction chegarasini interface dagi yoki sinfning ommaviy metodida aniq qilib qo'yish, self-invocation kerak bo'lsa metodni alohida bean'ga ko'chirish. AspectJ rejimiga o'tish `private` metodni ham qamraydi, lekin build murakkablashadi va weaving xatolari debug qilish qiyin, shuning uchun u oxirgi chora.

## 25.32 View Ichida Ochiq Sessiya (Open Session in View - anti-pattern)

**Tavsif:** Hibernate sessiyasi (yoki JPA `EntityManager`) HTTP so'rov tugaguniga qadar ochiq qoldiriladi, shunda view yoki serializer lazy collection'larni kerak bo'lganda yuklay oladi. Bu `LazyInitializationException`'ni "hal qiladi", lekin aslida uni yashiradi: DB chaqiruvlari service qatlamidan chiqib, rendering vaqtiga tarqaladi. Natijada N+1 so'rovlar nazoratdan chiqadi, DB connection har bir so'rov davomida ushlab turiladi va transaction chegaralari tushunarsiz bo'lib qoladi. Bugun bu Spring hamjamiyatida ochiq anti-pattern deb tan olingan.

**Spring'da qayerda uchraydi:** `OpenEntityManagerInViewInterceptor` va `OpenEntityManagerInViewFilter` (JPA), `OpenSessionInViewFilter` (Hibernate native). Spring Boot'da `spring.jpa.open-in-view` property'si standart holda `true` bo'lib, startup'da `JpaBaseConfiguration` WARN log yozadi: uni `false` qilib qo'yish deyarli har doim to'g'ri. O'rniga DTO projection (`interface`-based yoki `record`-based Spring Data projection), `JOIN FETCH` bilan JPQL, `@EntityGraph`, yoki `Hibernate.initialize()` service ichida ishlatiladi.

**Qo'llanish keyslari:**
- Thymeleaf/JSP template `${order.items}` ni iterate qilib, har bir satr uchun yangi SELECT yuborishi.
- Jackson `@RestController`'da entity'ni serializatsiya qilayotganda lazy `@OneToMany`'ni ochib, yuzlab so'rov generatsiya qilishi.
- Yuqori yuklamali endpoint'da connection pool (HikariCP) tugashi, chunki har bir so'rov connection'ni rendering tugaguniga qadar band qiladi.
- Legacy monolitni mikroservislarga ajratishda `open-in-view=false` qilingach, yashirin `LazyInitializationException`'lar to'planib chiqishi.
- APM (Micrometer/New Relic) trace'da DB vaqti controller'dan keyin ko'rinishi - muammoni topish qiyinlashishi.

**Ehtiyot bo'ling:** `open-in-view` ni `false` qilish mavjud loyihada ko'plab `LazyInitializationException`'ni yuzaga chiqaradi, shuning uchun uni integration testlar bilan birga, bosqichma-bosqich o'chirish kerak. Transaction `OpenEntityManagerInViewFilter` bilan uzaytirilmaydi - faqat sessiya ochiq qoladi, ya'ni view ichida qilingan o'zgarishlar kutilmagan `flush` yoki umuman commit bo'lmaslik bilan yakunlanishi mumkin.

## 25.33 API'da JPA Entity'larini Fosh Qilish (Exposing JPA Entities in API)

**Tavsif:** Persistence qatlamining entity sinflari to'g'ridan-to'g'ri REST controller'ning request/response tipi sifatida ishlatiladi. Bu boshida kod yozishni qisqartiradi, lekin DB sxemasi bilan public API kontraktini bir-biriga payvandlaydi: ustun nomini o'zgartirish API'ni buzadi. Bundan tashqari ichki maydonlar (`passwordHash`, `internalScore`, audit maydonlari) tasodifan tashqariga chiqadi va mass-assignment zaifligi paydo bo'ladi. Lazy aloqalar esa serializatsiya vaqtida kutilmagan so'rovlar va `LazyInitializationException` keltiradi.

**Spring'da qayerda uchraydi:** `@Entity` sinfini `@RestController` metodi qaytarishi yoki `@RequestBody` sifatida qabul qilishi; `JacksonAutoConfiguration` `ObjectMapper` bilan uni to'g'ridan-to'g'ri JSON'ga aylantiradi. Toza yechimlar: Java 17+ `record` DTO'lar, MapStruct yoki `@Mapper` bilan mapping, Spring Data'ning interface/class projection'lari (`List<OrderSummary> findBy...`), Jackson `@JsonView`/`@JsonIgnore` (palliativ chora), Spring Data REST ishlatilganda esa `@Projection` va `RepositoryDetectionStrategy` konfiguratsiyasi.

**Qo'llanish keyslari:**
- Ichki CRUD admin paneli uchun tez prototip - API kontrakti barqaror bo'lishi talab qilinmaganda.
- `PATCH /users` endpoint'i entity'ni to'g'ridan-to'g'ri bind qilib, foydalanuvchiga `role` maydonini o'zgartirish imkonini berishi (xavfsizlik incident'i).
- OpenAPI sxemasida Hibernate proxy maydonlari va `hibernateLazyInitializer` paydo bo'lishi.
- Ustun nomini `name` dan `full_name` ga o'zgartirish mobil klientlarni buzishi.
- Spring Data REST bilan repository avtomatik fosh bo'lib, barcha entity'lar hech qanday filtrsiz tashqariga chiqishi.

**Ehtiyot bo'ling:** `@JsonIgnore` bilan "yamoq" qo'yish vaqtinchalik yechim - yangi maydon qo'shilganda uni unutish osongina ma'lumot oqishiga olib keladi; shuning uchun DTO'ni aniq, explicit tarzda yozish xavfsizroq. DTO qatlami qo'shimcha kod degani, lekin uni avtomatik generatsiya (MapStruct) va API contract testlari bilan arzonlashtirish mumkin.

## 25.34 Semiz Controller (Fat Controller)

**Tavsif:** Biznes mantiq, validatsiya, transaction boshqaruvi, mapping va hatto DB so'rovlari controller sinfiga to'planib ketadi. Controller o'zining asosiy vazifasi - HTTP protokolini domen chaqiruviga aylantirish - dan tashqariga chiqadi va minglab qatorli monolit sinfga aylanadi. Natijada mantiqni qayta ishlatish imkonsiz bo'ladi: xuddi shu amalni message listener yoki scheduled job'dan chaqirish uchun kodni ko'chirib yozishga to'g'ri keladi. Test qilish ham HTTP qatlamini ko'tarishni talab qiladi.

**Spring'da qayerda uchraydi:** `@RestController`/`@Controller` sinflari ichida `@Transactional` metodlar, bevosita `JdbcTemplate` yoki `JpaRepository` chaqiruvlari, `if/else` bilan yozilgan biznes qoidalar. To'g'ri taqsimot: controller faqat `@Valid` bilan validatsiya, DTO mapping va status kodni boshqaradi; mantiq `@Service` yoki domen obyektlarida; so'rovlar `@Repository`'da; cross-cutting xatoliklar `@RestControllerAdvice`'da. Spring Framework 6.1+ `@HttpExchange`/`RestClient` bilan tashqi chaqiruvlarni ham controller'dan chiqarib tashlash osonlashgan.

**Qo'llanish keyslari:**
- 2000 qatorli `OrderController` ichida narx hisoblash, chegirma qoidalari va inventar tekshiruvi joylashgani.
- `@Transactional` controller metodida bo'lib, HTTP response yozilishi transaction ichiga tushib qolishi.
- Kafka listener'dan xuddi shu buyurtma mantig'i kerak bo'lganda controller'ni chaqirib bo'lmasligi.
- Unit test o'rniga faqat `MockMvc` testlari yozilib, test to'plami sekinlashishi.
- Bir nechta jamoa bitta controller faylida ishlab, har PR'da merge conflict chiqishi.

**Ehtiyot bo'ling:** Teskari tomonga o'tib ketmang - har bir controller metodi uchun bitta trivial "pass-through" service yaratish ham keraksiz qatlam (Lasagna code). Mantiq bor joyda service yoki domen obyektini ajratish kerak, shunchaki mapping bo'lsa controller ichida qoldirish to'g'ri.

## 25.35 Anemik Domen Modeli (Anemic Domain Model - anti-pattern)

**Tavsif:** Domen sinflari faqat maydonlar, getter va setter'lardan iborat bo'lib, hech qanday xatti-harakatga ega bo'lmaydi; barcha qoidalar esa service sinflariga ko'chadi. Bu obyektga yo'naltirilgan dizaynning asosini - ma'lumot va uning ustidagi mantiqni birga saqlashni - buzadi. Natijada invariantlar hech qachon obyekt darajasida kafolatlanmaydi: har bir service o'zi tekshiruvni takrorlashi kerak, biri esa unutib qo'yadi. Martin Fowler bu holatni klassik anti-pattern deb ta'riflagan, garchi amalda u Spring loyihalarida eng keng tarqalgan uslub bo'lsa ham.

**Spring'da qayerda uchraydi:** `@Entity` sinflari faqat `@Data` (Lombok) bilan yozilib, `OrderService` ichida `order.setStatus(SHIPPED)` kabi chaqiruvlar tarqalib ketishi. Boyroq model: entity ichida `ship()`, `cancel()` kabi metodlar; `@Embeddable` value object'lar (`Money`, `Address`); JPA 3.1/Hibernate 6 `AttributeConverter` bilan tipli maydonlar; Java 17+ `record` va `sealed` interface'lar bilan domen eventlari; `AbstractAggregateRoot.registerEvent()` (Spring Data) bilan domen eventlarini e'lon qilish va `@DomainEvents`/`@AfterDomainEventPublication` orqali tarqatish.

**Qo'llanish keyslari:**
- Status o'tishlari (`NEW → PAID → SHIPPED`) uchta turli service'da takrorlanib, biri noto'g'ri o'tishga yo'l qo'yishi.
- `setTotal()` public bo'lgani uchun har qanday kod jami summani invariantni buzgan holda o'zgartira olishi.
- Pul hisob-kitobi `double` bilan service ichida bajarilib, `Money` value object yo'qligi sababli yaxlitlash xatolari chiqishi.
- Oddiy CRUD mikroservis - bu yerda anemik model aslida yetarli va "boylashtirish" keraksiz murakkablik.
- Report/read-only model - projection DTO'lar tabiiy ravishda xatti-harakatsiz bo'ladi va bu normal.

**Ehtiyot bo'ling:** Anemik modelni har joyda "kasallik" deb hisoblamang: sodda CRUD va read-model uchun u to'g'ri tanlov, DDD'ni majburlash esa keraksiz murakkablik keltiradi. Boyitilgan entity'ga esa infrastruktura (repository, HTTP client) inyeksiya qilmang - domen obyekti faqat o'ziga berilgan argumentlar bilan ishlashi kerak, aks holda testlanmaydigan chalkashlik paydo bo'ladi.

## 25.36 ApplicationContext.getBean() Service Locator Sifatida (ApplicationContext.getBean() as Service Locator)

**Tavsif:** Bean'lar dependency injection orqali olinmay, kod ichida `applicationContext.getBean(Foo.class)` chaqiruvi bilan runtime'da izlanadi. Bu dependency inversion printsipini teskari aylantiradi: sinf o'z bog'liqliklarini o'zi "tortib oladi" va Spring konteyneriga qattiq bog'lanadi. Bog'liqliklar kompilyatsiya vaqtida ko'rinmaydi, shuning uchun yo'q bean faqat ishlash paytida `NoSuchBeanDefinitionException` bilan fosh bo'ladi. Testda esa butun kontekstni yoki mock `ApplicationContext`'ni qurishga majbur bo'lasiz.

**Spring'da qayerda uchraydi:** `ApplicationContextAware`, `BeanFactoryAware` interface'lari, statik holder sinflari (`SpringContextHolder`), `ServiceLocatorFactoryBean` (eski, 6.x'da hali bor lekin tavsiya etilmaydi). Zamonaviy alternativalar: `ObjectProvider<T>` (lazy va optional dependency uchun), `ObjectFactory<T>`, `List<Strategy>`/`Map<String, Strategy>` inyeksiyasi bilan strategiya tanlash, `@Lookup` metodi prototype bean uchun, va `Supplier<T>` bilan kechiktirilgan yaratish. Spring Framework 6.x AOT/native-image rejimida `getBean()` bilan dinamik izlash reflection metadata muammosiga ham olib keladi.

**Qo'llanish keyslari:**
- Framework yoki kutubxona kodi Spring'dan mustaqil bo'lishi kerak bo'lganda vaqtinchalik ko'prik sifatida.
- Legacy static utility sinfidan Spring bean'ga murojaat qilish (`SpringContextHolder.getBean(...)`) - ko'chirish davrida.
- Runtime'da nom bo'yicha strategiya tanlash - buning o'rniga `Map<String, PaymentHandler>` inyeksiyasi to'g'ri yechim.
- Singleton service'dan prototype bean'ni har safar yangisini olish - bu yerda `@Lookup` yoki `ObjectProvider` to'g'ri vositadir.
- Circular dependency'ni "aylanib o'tish" uchun `getBean()` ishlatish - bu dizayn muammosini yashiradi.

**Ehtiyot bo'ling:** Statik `ApplicationContext` holder'lar testlarda kontekst qoldiqlari (leak) va parallel test ishga tushirishda poyga holatiga olib keladi. Agar lazy yoki shartli dependency kerak bo'lsa, `ObjectProvider<T>` ni ishlating - u kontraktni konstruktor imzosida ko'rinadigan qiladi va AOT bilan ham mos keladi.

## 25.37 Aylanali Bean Bog'liqliklari (Circular Bean Dependencies)

**Tavsif:** A bean B'ga, B esa A'ga bog'liq bo'lib, konteyner ularni qaysi tartibda yaratishni aniqlay olmaydi. Spring buni ilgari uchinchi darajali cache va yarim tuzilgan obyektlarga reference berish bilan "hal qilardi", lekin bu nozik xatoliklar manbai. Aylana deyarli har doim mas'uliyatlar noto'g'ri taqsimlanganini bildiradi: ikkita sinf bir-birining ishini bajarmoqda yoki umumiy mantiq uchinchi sinfga ajratilmagan. Spring Boot 2.6'dan boshlab bu holat standart tarzda startup'da taqiqlangan.

**Spring'da qayerda uchraydi:** `BeanCurrentlyInCreationException` xatoligi; `spring.main.allow-circular-references` property'si (standart holda `false`, Spring Boot 2.6+ va 3.x/4.x'da); vaqtinchalik "yamoq" sifatida `@Lazy` qo'yish yoki setter/field inyeksiyaga o'tish. To'g'ri yechimlar: umumiy mantiqni uchinchi bean'ga ajratish, bog'liqlikni event'ga aylantirish (`ApplicationEventPublisher` va `@EventListener`), interface segregatsiyasi, yoki `ObjectProvider` bilan kechiktirish. Konstruktor inyeksiyasi aylanani darhol fosh qiladi - bu uning afzalligi, kamchiligi emas.

**Qo'llanish keyslari:**
- `UserService` ↔ `NotificationService` bir-birini chaqirib, startup'da `BeanCurrentlyInCreationException` berishi.
- Spring Boot 2.5'dan 3.x'ga migratsiya paytida ilgari jim ishlagan aylana startup'ni to'xtatishi.
- `@Configuration` sinflari bir-birining `@Bean` metodini chaqirib aylana yasashi.
- `@Lazy` bilan tuzatilgan aylanada proxy'ga birinchi murojaatda kutilmagan `NullPointerException` chiqishi.
- Self-reference (bean o'ziga bog'liq) - self-invocation muammosini hal qilish uchun ataylab ishlatiladigan kam hollardan biri.

**Ehtiyot bo'ling:** `spring.main.allow-circular-references=true` ni yoqish - texnik qarzni kechiktirish; u initsializatsiya tartibiga bog'liq, takrorlanishi qiyin xatolarni qoldiradi va AOT/native-image bilan muammo keltiradi. Aylanani `@Lazy` bilan berkitganda bean yarim tuzilgan holatda ishlatilishi mumkinligini unutmang - `@PostConstruct` ichida bunday dependency'ga murojaat qilish xavfli.

## 25.38 Juda Keng Component Scanning (Over-broad Component Scanning)

**Tavsif:** `@ComponentScan` juda yuqori paketdan (yoki umuman root paketdan) boshlanadi va natijada kerakmas sinflar ham bean sifatida ro'yxatga olinadi. Bu startup vaqtini uzaytiradi, xotira iste'molini oshiradi va eng muhimi - tasodifan uchinchi tomon kutubxonalaridagi yoki test-only sinflarni kontekstga tortib keladi. Modullar orasidagi chegaralar yemiriladi: bir modul boshqasining ichki bean'ini ko'radi va unga bog'lanib qoladi. Native-image va AOT rejimida esa skanerlanadigan sinf soni bevosita build vaqti va binar hajmiga ta'sir qiladi.

**Spring'da qayerda uchraydi:** `@SpringBootApplication` o'zi `@ComponentScan`ni o'z paketidan boshlab yoqadi - shu sababli main sinfni to'g'ri paketga qo'yish muhim; `@ComponentScan(basePackages = "com")` kabi yozuv jiddiy muammo. Nazoratli alternativalar: `@ComponentScan` uchun `includeFilters`/`excludeFilters` va `TypeExcludeFilter`; `@Import` bilan aniq konfiguratsiya; `@AutoConfiguration` va `META-INF/spring/org.springframework.boot.autoconfigure.AutoConfiguration.imports` (Spring Boot 3.x) kutubxona bean'lari uchun; `@Conditional`/`@ConditionalOnMissingBean` bilan shartli ro'yxatga olish. Spring Modulith esa paket chegaralarini test bilan majburlash imkonini beradi.

**Qo'llanish keyslari:**
- Monolit startup'i 60 sekundga yetishi - scan `com` paketidan boshlangani uchun minglab sinf tekshirilishi.
- Test uchun yozilgan `@Component` stub production kontekstiga tushib, haqiqiy bean'ni almashtirib qo'yishi.
- Shared kutubxona `@Component` bilan bean e'lon qilib, uni ishlatmaydigan servislar ham majburan ko'tarishi.
- Lambda/serverless deploy'da cold start vaqti scan hajmi sababli qabul qilinmas darajada o'sishi.
- `@ComponentScan` ikki marta turli konfiguratsiyada e'lon qilinib, bean'lar dublikat bo'lishi.

**Ehtiyot bo'ling:** Kutubxona yozayotgan bo'lsangiz hech qachon iste'molchining paketiga tayanib `@ComponentScan` qilmang - auto-configuration mexanizmidan foydalaning, aks holda iste'molchi sizning ichki sinflaringizga bog'lanib qoladi. `excludeFilters` bilan tozalash nozik: filter noto'g'ri yozilsa kerakli bean jim yo'qoladi va xato faqat runtime'da `NoSuchBeanDefinitionException` sifatida ko'rinadi.

## 25.39 Profile Tarqoqligi (Profile Sprawl)

**Tavsif:** `@Profile` annotatsiyasi konfiguratsiya farqlarini boshqarish uchun haddan tashqari ko'p ishlatilib, o'nlab profil va ularning kombinatsiyalari paydo bo'ladi (`dev`, `qa`, `staging`, `prod`, `prod-eu`, `no-kafka`, `mock-payments`). Natijada hech kim qaysi profil to'plamida qaysi bean aktiv bo'lishini aniq bilmaydi va production konfiguratsiyasi faqat deploy paytida tekshiriladi. Profil bo'yicha shartli bean'lar kod bazasiga tarqalib, muhitlar orasidagi xatti-harakat farqi kodning o'zida yashiringan bo'ladi. Testda esa bitta yetishmagan profil butunlay boshqa bean grafikasini beradi.

**Spring'da qayerda uchraydi:** `@Profile`, `spring.profiles.active`, `spring.profiles.group` (Spring Boot 2.4+), `application-{profile}.yml`, `@ActiveProfiles` testlarda. Spring Boot 2.4'dan `spring.profiles.include` o'rniga `spring.config.import` va profil guruhlari tavsiya etiladi; `spring.config.activate.on-profile` esa YAML hujjat ichida shartli blok yozishga imkon beradi. Toza alternativalar: oddiy `@ConfigurationProperties` qiymatlari bilan boshqarish, `@ConditionalOnProperty` orqali xususiyat (feature) flag'lari, tashqi konfiguratsiya (Spring Cloud Config, Kubernetes ConfigMap/Secret) va `Environment` abstraksiyasi.

**Qo'llanish keyslari:**
- `@Profile("!prod")` bilan yozilgan mock bean tasodifan production'da aktiv bo'lib qolishi (profil nomi o'zgargani uchun).
- To'rtta muhit × uchta xususiyat flag'i = o'n ikkita profil kombinatsiyasi, hech biri CI'da to'liq sinalmasligi.
- Test `@ActiveProfiles("test")` bilan ishlab, production'da boshqacha bean grafikasi tufayli xato chiqishi.
- `@Profile` bilan `DataSource` almashtirilib, migratsiya skriptlari noto'g'ri DB'ga tushishi.
- Profilni property flag'iga almashtirish (`@ConditionalOnProperty(name="payments.mock", havingValue="true")`) - bir o'lchovli va tushunarli yechim.

**Ehtiyot bo'ling:** Profil bean'ning bor-yo'qligini o'zgartiradi, property esa faqat qiymatini - shu sababli profil xatosi ancha og'irroq oqibatga olib keladi; muhit farqlarini iloji boricha qiymatlar bilan, bean grafigi bilan emas, ifodalang. Aktiv profil ro'yxatini startup'da log'ga chiqarib, deploy pipeline'ida uni tekshiradigan smoke test qo'shing.

## 25.40 Hamma Narsa Uchun @SpringBootTest (@SpringBootTest for Everything)

**Tavsif:** Har bir test, hatto oddiy mapper yoki validator uchun ham, butun Spring kontekstini ko'taradi. Natijada test to'plami daqiqalardan o'nlab daqiqalarga cho'ziladi, fikr-mulohaza halqasi (feedback loop) buziladi va ishlab chiquvchilar testni mahalliy ishlatishdan voz kechadi. Bundan tashqari bunday testlar "nimani sinayotgani" noaniq bo'ladi: xato chiqqanda u biznes mantiqda emas, konfiguratsiyada bo'lishi mumkin. Kontekst cache'i ham turli `@MockBean` kombinatsiyalari sababli parchalanib, har test sinfi yangi kontekst ko'taradi.

**Spring'da qayerda uchraydi:** `@SpringBootTest` o'rniga nishonlangan test slice'lar: `@WebMvcTest`, `@WebFluxTest`, `@DataJpaTest`, `@JdbcTest`, `@DataRedisTest`, `@JsonTest`, `@RestClientTest`. Spring Boot 3.4+ `@MockitoBean`/`@MockitoSpyBean` (eski `@MockBean` deprecated) va `@ServiceConnection` bilan Testcontainers integratsiyasi; `@TestConfiguration` va `TestPropertyValues` nozik sozlash uchun. Kontekst cache'i `TestContextManager` tomonidan kalit sifatida konfiguratsiya to'plamiga bog'lanadi - mock'lar kaliti o'zgarganda cache miss bo'ladi.

**Qo'llanish keyslari:**
- Pure funksiya yoki `MapStruct` mapper testi - oddiy JUnit 5 unit test yetarli, kontekst umuman kerak emas.
- Controller'ning HTTP mapping va validatsiyasini sinash - `@WebMvcTest` + `MockMvc` o'n baravar tez.
- Repository so'rovini tekshirish - `@DataJpaTest` + Testcontainers Postgres yoki `@ServiceConnection`.
- Har test sinfida boshqa `@MockitoBean` to'plami ishlatilib, kontekst cache 20 marta qayta ko'tarilishi.
- Haqiqiy end-to-end smoke test - bu yerda `@SpringBootTest(webEnvironment = RANDOM_PORT)` to'g'ri va zarur tanlov.

**Ehtiyot bo'ling:** `@DirtiesContext` ni ehtiyotsiz ishlatish kontekst cache'ini butunlay yo'q qiladi va test vaqtini keskin oshiradi - uni faqat chindan ham kontekstni buzadigan testda qo'llang. Test piramidasini teskari aylantirmang: integration testlar qiymatli, lekin ular sekin va mo'rt (flaky), shuning uchun mantiq tekshiruvining asosiy yuki unit testlarda bo'lishi kerak.

## 25.41 Hammasini Tutuvchi Exception Handler (Catch-all Exception Handler)

**Tavsif:** Bitta `@ExceptionHandler(Exception.class)` barcha xatoliklarni tutib, ularni bir xil javobga (ko'pincha `500` yoki hatto `200` + xato matni) aylantiradi. Bu client uchun ma'noli xato kodlarini yo'q qiladi: validatsiya xatosi, topilmagan resurs va haqiqiy ichki nosozlik bir-biridan farqlanmaydi. Bundan ham yomoni, handler stack trace'ni log'ga yozmasa, nosozliklar butunlay ko'rinmas bo'lib qoladi va monitoring (xato darajasi, alert'lar) ishlamaydi. Ba'zan `Error` va `InterruptedException` ham tutilib, JVM yoki thread holati buziladi.

**Spring'da qayerda uchraydi:** `@RestControllerAdvice` ichidagi `@ExceptionHandler(Exception.class)`. To'g'ri yondashuv: `ProblemDetail` va `ErrorResponse` (RFC 9457, Spring Framework 6.0+), `ResponseEntityExceptionHandler`'dan meros olib standart Spring xatolarini saqlab qolish, `@ResponseStatus` bilan domen exception'larini kodga bog'lash, `spring.mvc.problemdetails.enabled=true` (Spring Boot 3.x) va aniq tipli handler'lar (`MethodArgumentNotValidException`, `ConstraintViolationException`, `DataIntegrityViolationException`, `AccessDeniedException`). Xavfsizlik uchun esa `AuthenticationException`/`AccessDeniedException` Spring Security filter zanjirida, `ExceptionTranslationFilter`'da ishlanadi - controller advice ularni tutib qolmasligi kerak.

**Qo'llanish keyslari:**
- Validatsiya xatosi `400` emas `500` qaytarib, client retry qilib DB'ni yuklab tashlashi.
- `AccessDeniedException` tutilib `500` ga aylanishi va Spring Security'ning `403` mantig'i buzilishi.
- Stack trace log'ga yozilmagani uchun production incident'i bir necha kun aniqlanmasligi.
- Xato javobida ichki exception matni va SQL so'rovi fosh bo'lib, ma'lumot oqishi yuzaga kelishi.
- Haqiqiy fallback handler - eng pastki qatlamda, log yozib `ProblemDetail` bilan `500` qaytaruvchi yagona handler - bu to'g'ri va zarur.

**Ehtiyot bo'ling:** Fallback handler bo'lishi kerak, lekin u aniq tipli handler'lardan keyin ishlashi va har doim `log.error(ex)` bilan to'liq stack trace yozishi shart; `@Order` bilan advice tartibini aniq belgilang. Xato javobiga hech qachon exception matnini xom holda qo'ymang - `ProblemDetail`'ning `detail` maydoniga faqat tashqariga chiqarish xavfsiz bo'lgan, trace ID bilan birga beriladigan xabarni yozing.

## 25.42 Reactive Pipeline Ichida Bloklash (Blocking in Reactive Pipeline)

**Tavsif:** Reactive oqim ichida bloklovchi chaqiruv bajariladi: JDBC so'rovi, `RestTemplate`, `Thread.sleep()`, sinxron fayl o'qish yoki `block()`. Reactor'da operatorlar odatda kichik event-loop thread pool'da (`reactor-http-nio-*`) ishlaydi, shuning uchun bitta bloklovchi chaqiruv o'nlab minglab so'rovga xizmat qilayotgan thread'ni to'xtatadi. Natijada throughput qulab tushadi va yuklama ostida latency keskin o'sadi - reactive stack'dan olinadigan butun foyda yo'qoladi. Eng yomoni, bu past yuklamada sezilmaydi va faqat production'da fosh bo'ladi.

**Spring'da qayerda uchraydi:** Spring WebFlux (`@RestController` `Mono`/`Flux` qaytarganda), Reactor Netty event loop. Aniqlash va to'g'ri bajarish vositalari: BlockHound (`reactor-tools`, bloklovchi chaqiruvni exception bilan fosh qiladi), `Mono.fromCallable(...).subscribeOn(Schedulers.boundedElastic())` bloklovchi kod uchun, `Schedulers.parallel()` CPU ishi uchun, R2DBC (`spring-boot-starter-data-r2dbc`) JDBC o'rniga, `WebClient` `RestTemplate` o'rniga. Java 21+ virtual thread'lar (`spring.threads.virtual.enabled=true`) bilan Spring MVC ko'pincha WebFlux'ga alternativa sifatida yetarli bo'ladi.

**Qo'llanish keyslari:**
- WebFlux controller ichida `JpaRepository` chaqirilib, event loop thread'i bloklanishi va yuklamada servis muzlab qolishi.
- `Mono.block()` ni test uchun yozib, keyin production kodga tasodifan qoldirish.
- `Flux.map()` ichida sinxron `RestTemplate` chaqiruvi - `WebClient` bilan `flatMap` ga o'tish kerak.
- Legacy bloklovchi kutubxonani `boundedElastic()` scheduler'ga o'rab, qolgan pipeline'ni reactive saqlash.
- `MDC` yoki `ThreadLocal`'ga tayangan kod reactive oqimda ishlamay qolishi - `Context`/`ContextSnapshot` (Micrometer Context Propagation) kerak bo'lishi.

**Ehtiyot bo'ling:** `boundedElastic()` - qutqaruv emas, balki yamoq: uning thread limiti bor va barcha DB trafigini unga yuborish yashirin bottleneck yasaydi. Agar stack'ingizdagi asosiy I/O bloklovchi bo'lsa, WebFlux'ni majburlash o'rniga Java 21+ virtual thread'li Spring MVC'ni tanlash ko'pincha oddiyroq va tezroq yechim; BlockHound'ni esa test profilida doimiy yoqib qo'ying.

## 25.43 N+1 so'rovlar (N+1 Queries)

**Tavsif:** Bitta kolleksiyani yuklash uchun avval 1 ta so'rov (parent'lar ro'yxati), so'ngra har bir parent uchun alohida child so'rovi yuboriladi - jami N+1 ta SQL. Bu anti-pattern lazy association'larni loop ichida o'qiganda yoki DTO mapping paytida bexosdan yuzaga keladi. Natijada 100 ta yozuv uchun 101 ta round-trip bo'lib, latency va DB yuklamasi chiziqli o'sadi. Muammo kichik test datasida ko'rinmaydi, faqat production hajmida portlaydi.

**Spring'da qayerda uchraydi:** Spring Data JPA repository'lari + Hibernate 6.x da `@OneToMany(fetch = FetchType.LAZY)` kolleksiyasini servis loop ichida o'qiganda. Yechimlar: `@EntityGraph(attributePaths = "items")` repository metodida, JPQL `join fetch`, Hibernate `@BatchSize(size = 50)`, `hibernate.default_batch_fetch_size` property, yoki `@NamedEntityGraph`. Aniqlash uchun `spring.jpa.properties.hibernate.generate_statistics=true`, `datasource-proxy` yoki Hibernate 6 ning `SessionStatistics` hamda `spring-boot-starter-actuator` metrikalari ishlatiladi.

**Qo'llanish keyslari:**
- Order ro'yxatini qaytaradigan REST endpoint har bir order uchun `order.getItems()` chaqirib 1+N so'rov hosil qiladi.
- MapStruct mapper nested DTO to'ldirayotganda lazy proxy'ni ochib yuboradi va so'rovlar soni portlaydi.
- Jackson serializatsiyasi entity'ni to'g'ridan-to'g'ri qaytarganda getter'lar orqali barcha association'larni yuklaydi.
- Pagination bilan `join fetch` ishlatilganda Hibernate xotirada paginate qilib ogohlantirish beradi - `@EntityGraph` + `@BatchSize` kombinatsiyasi to'g'ri yechim.
- Audit yoki hisobot job'i millionlab satrni iteratsiya qilganda N+1 batch oynasini bir necha soatga uzaytiradi.

**Ehtiyot bo'ling:** Hammasini `FetchType.EAGER` qilib "tuzatish" yanada yomon - bu Cartesian product va keraksiz katta natijalarga olib keladi. Bir nechta `join fetch` bilan ikkita kolleksiyani birga olish `MultipleBagFetchException` beradi; bunda `Set` ishlatish yoki ikki bosqichli yuklash kerak.

Mavzuning to'liq yozuvi arxitektor hujjatidagi [N+1 so'rov muammosi](../architect/18-spring-data-jpa-va-hibernate-chuqur.md#184-n1-sorov-muammosi-topish-usuli-va-tort-xil-yechim) bo'limida; bu yerda faqat pattern katalogi nuqtai nazari.

## 25.44 Yo'q @Version (Missing @Version)

**Tavsif:** Entity'da optimistic locking maydoni bo'lmasa, bir vaqtda ikki transaction bir xil satrni o'qib, o'zgartirib, saqlaganda oxirgi yozuv birinchisini jimgina yo'q qiladi - klassik "lost update". Hech qanday xato tashlanmaydi, shuning uchun ma'lumot yo'qolishi faqat biznes shikoyati orqali bilinadi. `@Version` maydoni har `UPDATE` da `WHERE version = ?` shartini qo'shib, konfliktni aniq xatoga aylantiradi.

**Spring'da qayerda uchraydi:** JPA entity'da `@Version` bilan `int`/`long`/`short` yoki `java.time.Instant` maydoni. Konflikt yuz berganda Hibernate `StaleObjectStateException` tashlaydi, Spring uni `ObjectOptimisticLockingFailureException` ga tarjima qiladi. Spring Data JPA `save()` da `@Version == null` bo'lsa yangi entity deb hisoblaydi (`JpaEntityInformation` orqali). Retry uchun Spring Retry'ning `@Retryable(retryFor = OptimisticLockingFailureException.class)`, agar kuchli kafolat kerak bo'lsa `@Lock(LockModeType.PESSIMISTIC_WRITE)` ishlatiladi.

**Qo'llanish keyslari:**
- Hisob balansi yoki ombor qoldig'i ikki parallel buyurtma tomonidan bir vaqtda kamaytirilganda qoldiq noto'g'ri chiqadi.
- Admin paneldagi ikki operator bir mijoz profilini tahrirlab, biri ikkinchisining o'zgarishini bexabar o'chiradi.
- REST PUT bilan to'liq resurs almashtirilganda version `ETag`/`If-Match` header orqali client'ga uzatilsa, HTTP 409/412 to'g'ri qaytariladi.
- Kafka consumer bir xil aggregate'ga kelgan ikkita event'ni parallel partition'larda qayta ishlaganda state buziladi.
- Workflow status mashinasi (`NEW -> PAID -> SHIPPED`) version'siz orqaga qaytib qolishi mumkin.

**Ehtiyot bo'ling:** `@Version` ni mavjud jadvalga qo'shsangiz, eski satrlarda `NULL` qoladi - migratsiyada `DEFAULT 0` va `NOT NULL` bering, aks holda `save()` entity'ni yangi deb hisoblab `INSERT` qilishga urinadi. Shuningdek version faqat JPA orqali yozilganda ishlaydi; native `UPDATE` yoki bulk JPQL query version'ni o'zi oshirmaydi.

## 25.45 Production DB testlari uchun H2 (H2 for Production-DB Tests)

**Tavsif:** Testlar in-memory H2 da (yoki HSQLDB da) ishlatiladi, production esa PostgreSQL yoki Oracle da turadi. H2 ning SQL dialekti, tip tizimi, locking semantikasi va index xatti-harakati boshqa - shuning uchun testlar yashil bo'lsa ham production'da xato chiqadi. Bu yolg'on ishonch beradigan anti-pattern: migratsiyalar, JSON/array ustunlar, window funksiyalar va `ON CONFLICT` kabi narsalar hech qachon haqiqiy DB'da sinalmaydi.

**Spring'da qayerda uchraydi:** `@DataJpaTest` ning default `@AutoConfigureTestDatabase(replace = ANY)` xatti-harakati H2 ga almashtiradi. To'g'ri yondashuv - Testcontainers (Boot 3.5 / TC 1.x da `org.testcontainers:postgresql`, Boot 4 / TC 2.x da `org.testcontainers:testcontainers-postgresql`, qarang: [testlash hujjatidagi Testcontainers asoslari](../testing/08-testcontainers-bilan-real-infratuzilmada.md#82-testcontainers-asoslari-docker-api-ustida-hayot-aylanishi)) bilan `@Testcontainers` + `@Container PostgreSQLContainer<?>` (TC 2.x da generiksiz `org.testcontainers.postgresql.PostgreSQLContainer`) va Spring Boot 3.1+ dagi `@ServiceConnection` annotatsiyasi, yoki `spring-boot-testcontainers` moduli hamda `@DynamicPropertySource`. Shuningdek `@AutoConfigureTestDatabase(replace = NONE)` bilan real DB'ga ulanib, Flyway/Liquibase migratsiyalarini tekshirish mumkin.

**Qo'llanish keyslari:**
- PostgreSQL `jsonb` ustuni yoki `text[]` massiv mapping'i H2 da umuman ishlamaydi, Testcontainers'da esa real tekshiriladi.
- `SELECT ... FOR UPDATE SKIP LOCKED` asosidagi job queue semantikasi faqat haqiqiy PostgreSQL'da to'g'ri sinaladi.
- Flyway migratsiya skriptlari (`V12__add_partial_index.sql`) DB'ga xos sintaksis ishlatganda H2 da parse xatosi beradi yoki jimgina farq qiladi.
- Case-sensitivity va `ORDER BY` collation farqlari integration testlarda aniqlanadi.
- Unique constraint buzilishi `DataIntegrityViolationException` ga tarjimasi driver'ga bog'liq - real DB bilan tekshirish shart.

**Ehtiyot bo'ling:** Testcontainers har test klassida yangi container ko'tarsa, build sekinlashadi - container'ni `static` qilib reuse qiling yoki `testcontainers.reuse.enable=true` dan foydalaning. H2 ni butunlay tashlash shart emas: u juda tez unit-darajali repository smoke testlari uchun qolishi mumkin, lekin migratsiya va dialekt-ga bog'liq mantiq albatta real DB'da sinalsin.

## 25.46 Cheklanmagan connection pool / noto'g'ri pool o'lchami (Unbounded Connection Pool / Wrong Pool Size)

**Tavsif:** Pool o'lchami "katta bo'lsa tez bo'ladi" degan noto'g'ri taxmin bilan 200-500 ga qo'yiladi yoki umuman cheklanmaydi. Haqiqatda DB'ning parallel ishlov berish qobiliyati CPU va disk bilan chegaralangan; ortiqcha connection'lar kontekst almashinuvi, lock contention va DB tomonda `max_connections` tugashiga olib keladi. Teskari xato ham bor: pool juda kichik bo'lsa thread'lar `Connection is not available` timeout'i bilan yiqiladi.

**Spring'da qayerda uchraydi:** Spring Boot 3.x da default `com.zaxxer.hikari.HikariDataSource`. Asosiy property'lar: `spring.datasource.hikari.maximum-pool-size`, `minimum-idle`, `connection-timeout`, `max-lifetime`, `leak-detection-threshold`. Monitoring uchun Actuator `hikaricp.connections.*` Micrometer metrikalari va `/actuator/metrics` endpoint'i. Virtual thread'lar (`spring.threads.virtual.enabled=true`, Java 21+) yoqilganda pool yanada muhim bo'ladi, chunki minglab virtual thread cheklangan pool'ga bosim beradi.

**Qo'llanish keyslari:**
- 4 vCPU li PostgreSQL uchun `maximum-pool-size` ni 10-20 oralig'ida saqlash ko'pincha 200 dan tezroq ishlaydi.
- Kubernetes'da 20 replica x 50 connection = 1000 connection, DB `max_connections=200` ni oshirib yuboradi va deploy paytida cluster yiqiladi.
- `max-lifetime` ni DB yoki proxy (PgBouncer) idle timeout'idan qisqa qo'yish uzilgan connection xatolarini yo'qotadi.
- Uzoq ishlaydigan batch job uchun alohida `DataSource` va alohida kichik pool ajratish OLTP trafikni himoya qiladi.
- `leak-detection-threshold=20000` bilan yopilmagan `Connection` yoki unmanaged `EntityManager` leak'lari log'da aniqlanadi.

**Ehtiyot bo'ling:** Pool o'lchamini oshirish latency muammosini hal qilmaydi - u faqat navbatni DB'ga ko'chiradi; avval sekin so'rovlar va N+1 ni tuzating. PgBouncer kabi external pooler bilan birga ishlatganda transaction-pooling rejimida prepared statement va `SET` asosidagi xususiyatlar buzilishi mumkin.

## 25.47 Sezgir ma'lumotni log'ga yozish (Logging Sensitive Data)

**Tavsif:** Parol, token, karta raqami, shaxsiy ma'lumot (PII) yoki to'liq HTTP body log'ga tushadi va markazlashgan log tizimida uzoq muddat saqlanadi. Bu GDPR/PCI-DSS buzilishi hamda eng oson exploit qilinadigan ma'lumot oqimi, chunki log'larga ko'pincha butun jamoa va tashqi SaaS vendor kirish huquqiga ega. Ko'pincha `toString()` yoki debug log orqali bexosdan sodir bo'ladi.

**Spring'da qayerda uchraydi:** Xavf manbalari: Lombok `@Data`/`@ToString` entity'da, `log.debug("request={}", dto)`, `CommonsRequestLoggingFilter` ning `setIncludePayload(true)`, `spring.jpa.show-sql` bilan parametrlar, va `logging.level.org.springframework.web=DEBUG`. Himoya: Lombok `@ToString.Exclude` yoki `@ToString(onlyExplicitlyIncluded = true)`, Jackson `@JsonProperty(access = WRITE_ONLY)`, Logback `ch.qos.logback.core.rolling` + custom `MessageConverter`/`PatternLayout` maskalash, Spring Security'ning `HttpSessionEventPublisher` emas balki `AuthenticationException` xabarlarini yutish, va Micrometer Tracing'da `ObservationFilter` orqali tag'larni tozalash.

**Qo'llanish keyslari:**
- Login endpoint'ida `LoginRequest` DTO Lombok `@Data` tufayli parolni `toString()` bilan log'ga chiqaradi.
- `Authorization: Bearer ...` header'i request logging filter orqali to'liq log'ga tushadi va token qayta ishlatilishi mumkin.
- To'lov servisida karta raqami `IllegalArgumentException` xabari ichida stack trace bilan birga chiqadi.
- Webhook payload'ini xatolar uchun to'liq saqlash mijoz PII ma'lumotlarini log retention muddati davomida ushlab turadi.
- `show-sql` yoki Hibernate `TRACE` darajasi bind parametrlarni, demak shaxsiy ma'lumotlarni, log'ga chiqaradi.

**Ehtiyot bo'ling:** Maskalashni faqat log pattern darajasida qilish yetarli emas - regex PAN raqamini topmasa ham ma'lumot chiqib ketadi; manbada, DTO va entity darajasida excluding qiling. Shuningdek log'ni "vaqtincha DEBUG ga o'tkazib incident'ni tekshirish" eng ko'p uchraydigan sabab, shuning uchun production'da dinamik log level o'zgartirish huquqini cheklang.

## 25.48 Singleton bean ichida mutable state (Mutable State in Singleton Beans)

**Tavsif:** Spring'ning default bean scope'i singleton bo'lgani uchun bitta instance barcha request thread'lari tomonidan birgalikda ishlatiladi. Agar bean ichida instance maydoni (`private List<...> buffer`, `private String currentUser`) mutatsiya qilinsa, bu race condition, ma'lumot aralashib ketishi va bir foydalanuvchi ma'lumotining boshqasiga ko'rinishiga olib keladi. Bug kichik yuklamada hech qachon takrorlanmaydi, production'da esa tasodifiy va tushuntirib bo'lmas xatolar beradi.

**Spring'da qayerda uchraydi:** `@Service`, `@Component`, `@RestController`, `@Repository` - barchasi default singleton. Xavfli misollar: non-thread-safe `SimpleDateFormat` yoki `java.text.NumberFormat` ni field sifatida saqlash, `StringBuilder` buffer, yoki `HttpServletRequest` dan olingan qiymatni field'ga yozib qo'yish. To'g'ri yechimlar: stateless dizayn va lokal o'zgaruvchilar, immutable `DateTimeFormatter`/`ObjectMapper`, `ThreadLocal` o'rniga `RequestContextHolder`, `@Scope(value = "request", proxyMode = TARGET_CLASS)` yoki `ObjectProvider<T>` orqali per-request bean olish.

**Qo'llanish keyslari:**
- Controller'da `private String tenantId` ni request boshida o'rnatish ikki mijoz ma'lumotini almashtirib yuboradi.
- `SimpleDateFormat` field'i parallel chaqiruvlarda buzilgan sana yoki `NumberFormatException` beradi.
- Service ichidagi `private List<Error> errors` ro'yxati har request'da to'planib, xotira leak va noto'g'ri validatsiya natijasi beradi.
- Virtual thread'lar yoqilgandan keyin (Java 21+) parallelizm darajasi oshib, avval "ishlab turgan" kod yiqila boshlaydi.
- `@Cacheable` natijasi sifatida qaytarilgan mutable kolleksiya chaqiruvchilar tomonidan o'zgartirilsa, cache ichidagi obyekt buziladi.

**Ehtiyot bo'ling:** Muammoni `synchronized` bilan "tuzatish" throughput'ni butunlay yo'qotadi - bean'ni stateless qilish deyarli har doim to'g'ri yechim. `ThreadLocal` ishlatsangiz, `finally` blokida `remove()` qilishni unutmang: thread pool'da qoldiq qiymat keyingi request'ga oqib o'tadi, virtual thread'larda esa ThreadLocal foydasi ham kamayadi.

## 25.49 Executor sozlanmagan @Async (@Async Without Executor Configuration)

**Tavsif:** `@Async` ni executor ko'rsatmasdan ishlatish Spring'ni default executor'ga tayanishga majbur qiladi - bu qaysi thread'larda, qancha parallellik bilan va qanday navbat bilan ishlashini nazoratsiz qoldiradi. Natijada yoki cheksiz thread yaratiladi, yoki navbat cheksiz o'sib OOM beradi, yoki task'lar jimgina tashlanadi. Shuningdek default holatda `SecurityContext`, `MDC` va request-scoped kontekst asinxron thread'ga ko'chmaydi.

**Spring'da qayerda uchraydi:** `@EnableAsync` + `@Async("taskExecutor")`. Spring Boot 3.x da `spring.task.execution.*` property'lari (`pool.core-size`, `pool.max-size`, `pool.queue-capacity`, `shutdown.await-termination`) `ThreadPoolTaskExecutor` ni sozlaydi; Boot 3.2+ da `spring.threads.virtual.enabled=true` bo'lsa `SimpleAsyncTaskExecutor` virtual thread'lar bilan ishlaydi. Kontekst uzatish uchun `DelegatingSecurityContextAsyncTaskExecutor`, `TaskDecorator` (MDC uchun), xatolar uchun `AsyncUncaughtExceptionHandler` va `AsyncConfigurer` interfeysi mavjud.

**Qo'llanish keyslari:**
- Email/notification yuborishni fon thread'iga chiqarib, HTTP response latency'sini qisqartirish.
- Bir nechta tashqi API'ni parallel chaqirib `CompletableFuture.allOf()` bilan birlashtirish.
- Hisobot generatsiyasini alohida, chegaralangan executor'ga ajratib asosiy web pool'ni himoya qilish.
- `TaskDecorator` orqali `traceId` ni MDC'da saqlab, async log'larni distributed trace bilan bog'lash.
- Graceful shutdown'da `spring.task.execution.shutdown.await-termination=true` bilan yarim bajarilgan task'lar yo'qolishini oldini olish.

**Ehtiyot bo'ling:** `@Async` metodni bir xil bean ichidan chaqirsangiz proxy chetlab o'tiladi va metod sinxron ishlaydi; `void` qaytaradigan async metodda tashlangan exception esa `AsyncUncaughtExceptionHandler` bo'lmasa butunlay yo'qoladi. Bitta umumiy executor'dan hamma narsa uchun foydalanish esa bir sekin task'ning butun ilovani bloklashiga olib keladi.

## 25.50 rollbackFor'siz checked exception (Checked Exception Without rollbackFor)

**Tavsif:** Spring'ning deklarativ tranzaksiya menejeri default holatda faqat `RuntimeException` va `Error` da rollback qiladi; checked exception'da tranzaksiya commit bo'ladi. Shuning uchun `throws IOException` tashlagan metod yarim bajarilgan ma'lumotni DB'ga yozib yuborishi mumkin. Bu jimgina ma'lumot buzilishiga olib keladigan eng ko'p uchraydigan Spring tuzog'i.

**Spring'da qayerda uchraydi:** `@Transactional(rollbackFor = Exception.class)` yoki `noRollbackFor` atributi; past darajada `org.springframework.transaction.interceptor.DefaultTransactionAttribute#rollbackOn` shu qoidani belgilaydi. Imperativ variantda `TransactionTemplate` ichida `TransactionStatus#setRollbackOnly()` chaqirish mumkin. Spring Framework 6.x da `@Transactional` ni `jakarta.transaction.Transactional` bilan almashtirish ham mumkin, lekin uning `rollbackOn` semantikasi farq qiladi - shuni bilib ishlash kerak.

**Qo'llanish keyslari:**
- Fayl yuklash + DB yozuvi bir tranzaksiyada: `IOException` da yozuv commit bo'lib "orphan" record qoladi.
- Tashqi API'ga `JsonProcessingException` chiqqanda order status jimgina `PAID` holatida qolib ketadi.
- Biznes qoidasi uchun checked `InsufficientFundsException` yozilgan bo'lsa, balans kamaytirilgan holida commit bo'ladi.
- `rollbackFor = Exception.class` ni arxitektura standarti sifatida ArchUnit test bilan majburlash.
- Integration testda `assertThatThrownBy` dan keyin DB holatini tekshirib rollback haqiqatda bo'lganini tasdiqlash.

**Ehtiyot bo'ling:** Exception'ni `try/catch` bilan yutib yuborish rollback'ni butunlay bekor qiladi, agar `setRollbackOnly()` chaqirilmasa. Teskari tomondan, `rollbackFor = Exception.class` ni hamma joyga qo'yish validatsiya xatosi kabi "kutilgan" holatlarda ham keraksiz rollback keltirib chiqarishi mumkin - `noRollbackFor` bilan aniq istisnolarni belgilang.

## 25.51 Remote chaqiruvni qamrab olgan tranzaksiya (Transaction Spanning Remote Calls)

**Tavsif:** `@Transactional` metod ichida HTTP, gRPC yoki message broker chaqiruvi qilinadi va DB connection tashqi tizim javobini kutib turadi. Bu connection'ni ushlab turish vaqtini tashqi servis latency'siga bog'laydi, pool'ni tezda tugatadi va lock'lar uzoq saqlanib deadlock xavfini oshiradi. Bundan tashqari remote chaqiruv rollback qilinmaydi - tranzaksiya orqaga qaytsa ham tashqi side-effect qoladi, ya'ni ma'lumot izchilligi buziladi.

**Spring'da qayerda uchraydi:** `@Transactional` ichida `RestClient`/`WebClient`/`RestTemplate`, `KafkaTemplate.send()` yoki `JmsTemplate` chaqiruvi. To'g'ri pattern'lar: tranzaksiyadan keyin ishga tushadig`@TransactionalEventListener(phase = AFTER_COMMIT)`, Transactional Outbox (DB jadvaliga yozib, alohida poller yuboradi), `TransactionSynchronizationManager.registerSynchronization(...)`, Spring Modulith'ning `@ApplicationModuleListener` va event publication registry'si, hamda Spring Integration/Kafka'ning idempotent consumer yondashuvi.

**Qo'llanish keyslari:**
- Order saqlash va to'lov provayderiga chaqiruvni ajratib, to'lovni commit'dan keyin outbox orqali yuborish.
- Email yuborishni `AFTER_COMMIT` listener'ga ko'chirib, rollback bo'lsa xabar ketmasligini kafolatlash.
- Kafka event'ni outbox jadvaliga yozib, Debezium yoki poller orqali at-least-once yetkazish.
- Uzoq tashqi chaqiruvni butunlay saga/orkestratsiya bosqichiga ajratib, har bosqich o'z qisqa tranzaksiyasida ishlashi.
- Tashqi chaqiruv `connect-timeout`/`read-timeout` bilan cheklanishi, hatto to'g'ri joyda bo'lsa ham.

**Ehtiyot bo'ling:** `AFTER_COMMIT` listener'da tashlangan exception tranzaksiyani qaytarmaydi - bu yerda retry va xatolarni alohida boshqarish kerak. Outbox pattern at-least-once semantikasini keltiradi, shuning uchun consumer tomonda idempotentlik (deduplikatsiya kaliti) albatta bo'lishi shart.

## 25.52 Tranzaksiyadan tashqarida LazyInitializationException (LazyInitializationException Outside Transaction)

**Tavsif:** Lazy association tranzaksiya va `EntityManager` yopilganidan keyin o'qilsa, Hibernate proxy'ni initsializatsiya qila olmay `LazyInitializationException` tashlaydi. Bu ko'pincha controller yoki serializatsiya qatlamida, ya'ni servis metodidan chiqib ketilganidan keyin yuz beradi. Ildiz sababi - entity'larni web qatlamiga ochiq qoldirish va persistence context chegarasini noto'g'ri loyihalash.

**Spring'da qayerda uchraydi:** Spring Boot 3.x da `spring.jpa.open-in-view` default `true` bo'lib, `OpenEntityManagerInViewInterceptor` muammoni yashiradi, lekin uni N+1 va uzoq ushlab turilgan connection evaziga hal qiladi - shuning uchun ko'pincha `false` ga qo'yish tavsiya qilinadi. To'g'ri yechimlar: `@EntityGraph` bilan kerakli graph'ni oldindan yuklash, repository'dan to'g'ridan-to'g'ri projection/DTO qaytarish (Spring Data interface yoki class-based projection), `Hibernate.initialize(...)`, yoki `@Transactional(readOnly = true)` servis metodida mapping'ni yakunlash.

**Qo'llanish keyslari:**
- Entity'ni DTO'ga servis ichida, tranzaksiya ochiq holatda map qilib, controller'ga faqat DTO berish.
- `open-in-view=false` qilib, yashirin lazy yuklashlarni development vaqtida fail-fast aniqlash.
- Hisobot so'rovida `@EntityGraph(attributePaths = {"customer", "items"})` bilan bitta so'rovda kerakli graph'ni olish.
- Async yoki `@Scheduled` metodda detached entity bilan ishlashda avval `findById` va graph fetch qilish.
- Kafka listener'da olingan entity'ni boshqa thread'ga uzatmaslik - faqat ID yoki DTO uzatish.

**Ehtiyot bo'ling:** `spring.jpa.open-in-view=true` qoldirish "tuzatish" emas, muammoni yashirish: HTTP response yozilayotganda DB connection hali ham band bo'ladi. `FetchType.EAGER` ga o'tish esa muammoni Cartesian product va keraksiz yuklamaga almashtiradi.

## 25.53 Property tarqoqligi (Property Sprawl)

**Tavsif:** Konfiguratsiya yuzlab nomsiz `@Value("${...}")` injection'lari sifatida kod bo'ylab tarqalib ketadi: bir xil property bir nechta joyda, turli default qiymatlar bilan o'qiladi, nomlash konvensiyasi yo'q, validatsiya yo'q. Natijada noto'g'ri yoki yetishmayotgan konfiguratsiya faqat runtime'da, ko'pincha production'da aniqlanadi. Hech kim ilovaning haqiqiy konfiguratsiya sirtini (surface) bilmaydi.

**Spring'da qayerda uchraydi:** `@ConfigurationProperties(prefix = "app.billing")` + `@EnableConfigurationProperties` yoki `@ConfigurationPropertiesScan`, Java `record` yoki immutable klass bilan constructor binding. Validatsiya uchun `@Validated` + Jakarta Bean Validation (`@NotBlank`, `@Min`, `@DurationUnit`). Qo'shimcha: `spring-boot-configuration-processor` metadata generatsiyasi (IDE autocomplete), profile'lar va `spring.config.import`, Actuator `/actuator/configprops` va `/actuator/env` endpoint'lari, hamda `spring.config.activate.on-profile` bilan muhit-ga xos qiymatlar.

**Qo'llanish keyslari:**
- Barcha billing sozlamalarini bitta `BillingProperties` record'ga yig'ib, `@Validated` bilan ishga tushishda fail-fast qilish.
- `/actuator/configprops` orqali effektiv konfiguratsiyani auditlash va muhitlar o'rtasidagi farqni topish.
- `Duration` va `DataSize` tiplari bilan `30s`, `10MB` kabi qiymatlarni tipli o'qish.
- Sirlarni property'dan ajratib, Vault yoki Kubernetes Secret'dan `spring.config.import` bilan olish.
- Configuration metadata generatsiyasi bilan IDE'da autocomplete va hujjatlashtirishni ta'minlash.

**Ehtiyot bo'ling:** `@Value` ni butunlay taqiqlash shart emas, lekin bitta modul uchun bitta tipli properties klassi qoidasini ArchUnit yoki code review bilan qo'llab-quvvatlang. Mutable `@ConfigurationProperties` bean'ini runtime'da o'zgartirish xavfli - refresh kerak bo'lsa Spring Cloud Config'ning `@RefreshScope` ini ongli ravishda ishlatish lozim.

## 25.54 Katta loy to'p (Big Ball of Mud)

**Tavsif:** Tizimda aniq chegaralar, qatlamlar va modullar yo'q: har narsa har narsaga bog'langan, bog'liqliklar aylanali, package'lar tasodifiy. Bu "anti-pattern" - ya'ni arxitektura qarori emas, balki arxitektura yo'qligining natijasi. Har qanday o'zgarish kutilmagan joylarda buziladi, onboarding oylar oladi va refactoring deyarli imkonsiz bo'lib qoladi.

**Spring'da qayerda uchraydi:** Belgilari: `@Autowired` field injection bilan 15+ bog'liqlikka ega "God service", `util` package'da biznes mantiq, controller'dan to'g'ridan-to'g'ri repository chaqiruvi, entity'larning hamma qatlamda ishlatilishi, va aylanali bean bog'liqliklari (Spring Boot 2.6+ da `spring.main.allow-circular-references=false` default bo'lib, bu holda ishga tushish xato bilan to'xtaydi). Davolash vositalari: ArchUnit (`com.tngtech.archunit`) qoidalari, Spring Modulith (`@ApplicationModule`, `ApplicationModules.verify()`), constructor injection, Maven/Gradle multi-module ajratish va `spring-boot-starter` ichidagi package-by-feature tashkiloti.

**Qo'llanish keyslari:**
- ArchUnit testi bilan "controller repository'ga murojaat qilmaydi" va "domain Spring'ga bog'lanmaydi" qoidalarini CI'da majburlash.
- Spring Modulith `ApplicationModules.verify()` ni test sifatida qo'shib, modullar o'rtasidagi ruxsatsiz bog'liqlikni build'da to'xtatish.
- Monolitni package-by-feature ga qayta tashkil qilib, keyinroq modulni alohida deploy qilish imkonini yaratish.
- Legacy "God service" ni fasad ortida bo'lib-bo'lib, strangler pattern bilan asta almashtirish.
- `allow-circular-references=false` ni yoqib, aylanali bog'liqliklarni oshkor qilish va constructor injection'ga o'tish.

**Ehtiyot bo'ling:** Katta qayta yozish (big-bang rewrite) ko'pincha yangi loy to'pini yaratadi - chegaralarni avval test va ArchUnit qoidalari bilan mustahkamlang, keyin bosqichma-bosqich ajratish. Shuningdek har bir kichik ilovani modullashtirishga urinish ortiqcha ceremonial murakkablik keltirishi mumkin.

## 25.55 Taqsimlangan monolit (Distributed Monolith)

**Tavsif:** Tizim mikroservislarga bo'lingan, lekin ular sinxron chaqiruvlar zanjiri bilan qattiq bog'langan: bitta biznes amalini bajarish uchun 5-8 servis ketma-ket chaqiriladi va hammasi birga deploy qilinishi kerak. Natijada monolitning barcha bog'liqliklari saqlanadi, ustiga tarmoq latency'si, qisman nosozlik va distributed debugging murakkabligi qo'shiladi. Bu eng qimmat anti-pattern: foyda yo'q, narx ikki barobar.

**Spring'da qayerda uchraydi:** Belgilari: har bir service'da `RestClient`/`FeignClient` bilan sinxron zanjir, umumiy `shared-dto` kutubxonasi barcha servislarni bir versiyaga bog'laydi, va bitta release train. Diagnostika va davolash: Micrometer Tracing + OpenTelemetry bilan chaqiruv zanjirini o'lchash, Resilience4j (`@CircuitBreaker`, `@Bulkhead`, `@TimeLimiter`) bilan izolyatsiya, Spring for Apache Kafka / Spring Cloud Stream bilan asinxron event-driven integratsiya, Spring Cloud Contract bilan mustaqil deploy uchun consumer-driven kontraktlar, hamda Spring Modulith bilan avval modulli monolit qurish.

**Qo'llanish keyslari:**
- Trace'da bitta request 6 servisdan o'tayotganini ko'rib, chegaralarni biznes tranzaksiyasi bo'yicha qayta chizish.
- Sinxron "get customer details" zanjirini event bilan to'ldirilgan lokal read model'ga almashtirish.
- `shared-dto` kutubxonasini tashlab, har bir servisga o'z kontrakti va o'z mapping'ini berish.
- Spring Cloud Contract bilan servislarni mustaqil release qilish imkonini yaratish.
- Resilience4j timeout va circuit breaker bilan bir servisning sekinlashishi butun zanjirni yiqitmasligini ta'minlash.

**Ehtiyot bo'ling:** Hamma narsani asinxron qilish ham yechim emas - eventual consistency biznes talablariga mos kelmasa, foydalanuvchi uchun noto'g'ri natija beradi. Agar jamoa chegaralarni hali bilmasa, mikroservislarga bo'lishdan oldin modulli monolit (Spring Modulith) bilan chegaralarni sinab ko'rish arzonroq.

## 25.56 Umumiy ma'lumotlar bazasi (Shared Database)

**Tavsif:** Bir nechta servis yoki jamoa bitta DB sxemasiga to'g'ridan-to'g'ri yozadi va o'qiydi. Bu holda DB sxemasi yashirin, versiyalanmagan integratsiya kontraktiga aylanadi: bitta ustunni o'zgartirish boshqa servisni buzadi, hech kim migratsiyani mustaqil qila olmaydi va ma'lumot egaligi (ownership) yo'qoladi. Bundan tashqari lock contention va umumiy connection pool bir servisning nosozligini hammaga tarqatadi.

**Spring'da qayerda uchraydi:** Belgilari: ikki Spring Boot ilovasi bir xil `spring.datasource.url` ga ulanadi, ikkisi ham o'z Flyway/Liquibase migratsiyalarini bir sxemaga qo'llaydi (`flyway_schema_history` konflikti), entity'lar ikki repo'da dublikat. Davolash: har servis uchun alohida schema yoki DB, integratsiya API (`RestClient`, gRPC) yoki event'lar (Spring for Apache Kafka, Spring Cloud Stream) orqali, Transactional Outbox + Debezium bilan CDC, hamda o'qish uchun servis egasi tomonidan ta'minlangan read-only view yoki replika.

**Qo'llanish keyslari:**
- Reporting jamoasiga production jadvallariga emas, read-replica yoki data warehouse'ga kirish berish.
- Yozuvni faqat bitta "owner" servisga qoldirib, boshqalarga API yoki event orqali kirish berish.
- Flyway'ni har servis uchun alohida schema va alohida `flyway_schema_history` jadvaliga sozlash.
- Outbox + CDC bilan ma'lumotni iste'molchi servislarning o'z lokal store'iga ko'chirish.
- Legacy umumiy DB'dan chiqishda avval yozuvni, keyin o'qishni bosqichma-bosqich ajratish (strangler).

**Ehtiyot bo'ling:** Ma'lumotni duplikatsiya qilish eventual consistency keltiradi - iste'molchi tomonda idempotentlik va kechikishni biznes bilan muvofiqlashtirish kerak. Shuningdek "umumiy DB" ni darhol bo'lishga urinish migratsiya paytida ikki tomonlama yozish (dual write) muammosini keltiradi; CDC yoki outbox bilan bir yo'nalishli oqim xavfsizroq.

## 25.57 Suhbatkash I/O (Chatty I/O)

**Tavsif:** Chatty I/O - bitta mantiqiy operatsiyani bajarish uchun ko'p sonli mayda tarmoq yoki disk so'rovlari yuborilishi. Har bir so'rov o'z lotentligi, TLS handshake, serializatsiya va connection pool'dan slot olish narxiga ega, shuning uchun 500 ta mayda so'rov bitta batch so'rovdan o'nlab marta sekin ishlaydi. Ko'pincha u ORM'ning lazy loading xatti-harakati yoki "loop ichida servisni chaqirish" ko'rinishida yashiringan holda paydo bo'ladi. Yuk ortgach tizim CPU'dan emas, balki kutishdan bo'g'iladi.

**Spring'da qayerda uchraydi:** Eng klassik ko'rinishi - Spring Data JPA'da `@OneToMany` kolleksiyasini loop ichida o'qiganda yuzaga keladigan N+1 SELECT muammosi; `spring.jpa.show-sql` yoki Hibernate statistikasi (`hibernate.generate_statistics`) bilan oson aniqlanadi. Yechim sifatida `@EntityGraph`, JPQL `JOIN FETCH`, `@BatchSize` va `hibernate.default_batch_fetch_size` ishlatiladi. Yozish tomonida `JdbcTemplate.batchUpdate(...)` yoki `spring.jpa.properties.hibernate.jdbc.batch_size` + `order_inserts/order_updates` sozlamalari, HTTP tomonida esa `RestClient`/`WebClient` bilan element-element chaqirish o'rniga bulk endpoint yoki `Flux.buffer(...)` yondashuvi qo'llaniladi.

**Qo'llanish keyslari:**
- Buyurtma ro'yxatini ko'rsatuvchi endpoint har bir buyurtma uchun alohida `SELECT` qilib, 200 ta qo'shimcha query yuboradi.
- CSV import xizmati 100 000 qatorni bitta-bitta `save()` qilib, batch INSERT o'rniga 100 000 round-trip qiladi.
- Hisobot servisi har bir foydalanuvchi uchun profil mikroservisiga alohida REST chaqiruv yuboradi.
- Redis'dan har bir kalit uchun alohida `GET` o'rniga `MGET`/pipeline ishlatilmaydi.
- Kafka consumer har bir xabardan keyin alohida commit va alohida DB yozuvi bajaradi.

**Ehtiyot bo'ling:** Batching'ni haddan oshirib yuborish teskari muammo tug'diradi - juda katta `IN (...)` ro'yxatlari query plan'ni buzadi (Oracle'da 1000 element limiti), juda katta batch esa transaction'ni uzaytirib lock ushlab turadi. Shuningdek `JOIN FETCH` bilan bir nechta kolleksiyani birga olish Dekart ko'paytmasiga olib keladi, shuning uchun bir vaqtda faqat bitta kolleksiyani fetch qiling va `Pageable` bilan birga ishlatishda ehtiyot bo'ling.

## 25.58 Nano-servislar (Nano-services)

**Tavsif:** Nano-services - mikroservis g'oyasini absurd darajaga yetkazib, har bir funksiya yoki har bir entity uchun alohida deploy qilinadigan servis yaratish. Natijada biznes mantiqning foydali qismi juda kichik, lekin har bir servis o'zining tarmoq chaqiruvlari, serializatsiyasi, konfiguratsiyasi, monitoringi, CI/CD quvuri va JVM xotirasiga ega bo'ladi. Overhead foydali ishdan oshib ketadi va bitta biznes amaliyoti o'nlab servis orqali o'tadi. Bu "distributed monolith"ning eng qimmat ko'rinishi.

**Spring'da qayerda uchraydi:** Har bir Spring Boot 3.x ilovasi o'z Tomcat/Netty, actuator, `DataSource` va observability stack'ini ko'taradi - 30 ta nano-servis 30 marta shu narxni to'laydi. Belgisi: servislarda faqat bittadan `@RestController` va bittadan `JpaRepository` bo'lishi, va ularning barchasi `spring-cloud-openfeign` yoki `RestClient` orqali bir-birini ketma-ket chaqirishi. Alternativa - Spring Modulith (`@ApplicationModule`, `ApplicationModules.verify()`) bilan bitta deployment ichida mantiqiy modul chegaralarini majburlash, keyinchalik kerak bo'lsa modulni alohida servisga ajratish.

**Qo'llanish keyslari:**
- "email-validator-service", "phone-formatter-service" kabi utility'lar alohida deploy qilinib, har biri 2 ta metodga ega.
- Bitta `Order` jarayoni 12 ta nano-servisni ketma-ket chaqiradi va p99 lotentlik 2 sekundga chiqadi.
- 40 ta repozitoriy va 40 ta pipeline bitta kichik jamoa tomonidan qo'lda qo'llab-quvvatlanadi.
- Har bir nano-servis uchun alohida schema migration va Flyway konfiguratsiyasi saqlanadi.
- Bitta maydon qo'shish uchun 5 ta servisni bir vaqtda release qilish talab qilinadi.

**Ehtiyot bo'ling:** Servis chegarasi texnik qulaylik emas, balki biznes imkoniyati va mustaqil o'zgarish tezligi bilan belgilanadi - agar ikki servis har doim birga release qilinsa, ular bitta servis bo'lishi kerak. Nano-servislarni birlashtirishdan qo'rqmang: modullashtirilgan monolit mikroservislardan orqaga qadam emas, balki ko'p holatda to'g'ri boshlang'ich nuqta.

## 25.59 Entitet-servislar (Entity Services)

**Tavsif:** Entity Services - servislarni biznes imkoniyatlari emas, balki ma'lumotlar bazasi jadvallariga qarab bo'lish: `CustomerService`, `AddressService`, `InvoiceLineService`. Bunday servislar faqat CRUD taqdim etadi va hech qanday biznes qoidasini o'zida saqlamaydi, mantiq esa chaqiruvchi tomonga "oqib" ketadi. Har bir use-case bir nechta entity-servisni orkestratsiya qilishni, ya'ni tarqalgan tranzaksiyani talab qiladi. Bu Nano-services va Synchronous call chains bilan birga yuradi.

**Spring'da qayerda uchraydi:** Belgisi - `@RepositoryRestResource` yoki Spring Data REST bilan JPA entity'larini to'g'ridan-to'g'ri REST sifatida tashqariga chiqarish, va hech qanday domain qatlami bo'lmagan `@Service` sinflari (faqat `repository.save()` ni o'rab turadigan metodlar). To'g'ri yondashuv: DDD aggregate chegaralarini aniqlash, invariantlarni aggregate root ichida saqlash, tashqariga esa use-case darajasidagi endpoint (`POST /orders/{id}/confirm`) berish. Spring Modulith'da modulning tashqi API'si `@NamedInterface` va event'lar orqali, ichki entity'lar esa package-private qilib yopiladi.

**Qo'llanish keyslari:**
- `OrderService` buyurtmani tasdiqlash uchun `OrderLineService`, `StockService`, `PriceService`'ni ketma-ket chaqirib, qoidalarni o'zida takrorlaydi.
- Frontend 4 ta CRUD endpoint'ni to'g'ri tartibda chaqirishi kerak, aks holda ma'lumot nomuvofiq qoladi.
- Bir xil validatsiya qoidasi 3 ta turli chaqiruvchida copy-paste qilingan.
- Spring Data REST orqali ochilgan entity'ga tashqi client to'g'ridan-to'g'ri `PATCH` yuborib, biznes invariantini buzadi.
- Yangi biznes talabi hech bir servisga "tegishli" bo'lmaganligi uchun orkestratsiya qatlamiga joylashtiriladi.

**Ehtiyot bo'ling:** CRUD o'z-o'zidan anti-pattern emas - oddiy reference data (davlatlar, valyutalar) uchun entity-style servis mutlaqo o'rinli. Muammo faqat invariantlari va murakkab o'tish holatlari bo'lgan domenda paydo bo'ladi; bu yerda o'lchov - biznes qoidasi qaysi joyda yashaydi degan savolga javob berish mumkinmi yo'qmi.

## 25.60 Sinxron chaqiruv zanjirlari (Synchronous call chains)

**Tavsif:** Bir servis ikkinchisini, u uchinchisini kutib turadigan uzun sinxron zanjir yuzaga kelganda, umumiy lotentlik barcha bo'g'inlar lotentligining yig'indisiga, umumiy mavjudlik esa ularning ko'paytmasiga aylanadi. Har biri 99.9% uptime bergan 5 ta servis zanjirda 99.5% beradi, p99 lotentliklar esa qo'shilib tail latency portlashiga olib keladi. Bundan tashqari har bir bo'g'in chaqiruvchi tomonda thread yoki connection ushlab turadi, bu esa resurs tugashiga yo'l ochadi.

**Spring'da qayerda uchraydi:** `RestClient`, `RestTemplate` yoki `@FeignClient` orqali qurilgan servis-servis chaqiruvlari; Spring Cloud Gateway ortidagi 4-5 qatlamli zanjirlar. Himoya vositalari: Resilience4j'ning `TimeLimiter`, `CircuitBreaker`, `Bulkhead` (`spring-cloud-starter-circuitbreaker-resilience4j`), har bir client uchun aniq connect/read timeout (`ClientHttpRequestFactorySettings`, `HttpClient` sozlamalari), Micrometer Tracing + OpenTelemetry bilan zanjirni ko'rinadigan qilish. Arxitektura darajasidagi yechim - zanjirni Kafka/RabbitMQ orqali asinxron event'larga aylantirish yoki ma'lumotni oldinga ko'chirib (data locality, CQRS read model) chaqiruvni butunlay yo'q qilish.

**Qo'llanish keyslari:**
- API Gateway → BFF → order → pricing → tax zanjirida eng oxirgi servis sekinlashsa, butun zanjir timeout bo'ladi.
- Checkout endpoint'i 7 ta downstream servisni ketma-ket chaqirib, p99 3 sekundga chiqadi.
- Chaqiruvchida timeout belgilanmagani uchun downstream osilib qolganda Tomcat thread pool to'liq tugaydi.
- Kaskad fallback'lar bir-birini chaqirib, nosozlik paytida yukni yana oshiradi.
- Bir downstream'ning deploy'i butun zanjirning xato darajasini oshiradi.

**Ehtiyot bo'ling:** Parallelizatsiya (`CompletableFuture.allOf`, `Mono.zip`) lotentlikni kamaytiradi, lekin mavjudlik ko'paytmasi muammosini hal qilmaydi - bog'liqlik sonini kamaytirish kerak. Timeout'larni zanjir bo'ylab tanlashda tashqi timeout ichkisidan katta, lekin butun byudjetdan kichik bo'lishiga e'tibor bering, aks holda retry'lar bilan birga Retry Storm hosil bo'ladi.

## 25.61 Qayta urinish bo'roni (Retry Storm (anti-pattern))

**Tavsif:** Retry pattern to'g'ri qo'llanganda vaqtinchalik xatolarni yashiradi, ammo noto'g'ri sozlanganda nosozlikni kuchaytiradigan mexanizmga aylanadi. Downstream sekinlashganda har bir client 3 marta qayta urinadi, zanjirning har bir qatlami bu sonni ko'paytiradi (3×3×3 = 27 so'rov), natijada allaqachon qiynalgan servis yuki bir necha barobar oshadi. Jitter bo'lmaganda esa barcha client'lar bir vaqtda qayta uradi va to'lqinli yuk hosil bo'ladi. Bu metastabil nosozlik: sabab yo'qolgandan keyin ham tizim o'z-o'zini yuklab turadi.

**Spring'da qayerda uchraydi:** Spring Retry'da `@Retryable` va `RetryTemplate` standart holda `FixedBackOffPolicy` bilan ishlaydi - buni `ExponentialBackOffPolicy` yoki jitterli `ExponentialRandomBackOffPolicy` ga o'zgartirish kerak. Resilience4j'da `IntervalFunction.ofExponentialRandomBackoff(...)` va `Retry`ni albatta `CircuitBreaker` bilan birga (retry ichda, circuit breaker tashqarida) ishlatish lozim. Yashirin ko'paytirgichlar: `spring.cloud.loadbalancer.retry.enabled`, Feign'ning `Retryer`, Kafka consumer'da `DefaultErrorHandler` ning backoff'i, `RestClient` ustidagi o'z retry interceptor'lari - bularning barchasi bir vaqtda yoqilgan bo'lishi mumkin.

**Qo'llanish keyslari:**
- Downstream 503 qaytargan paytda zanjirning 3 qatlami retry qilib, yukni 27 barobarga oshiradi.
- `@Retryable` idempotent bo'lmagan `POST` chaqiruviga qo'yilgani uchun bir buyurtma 3 marta yaratiladi.
- Jitter yo'qligi sababli barcha pod'lar har 2 sekundda sinxron to'lqin yuboradi.
- Retry 4xx validatsiya xatolarida ham ishlaydi va hech qachon muvaffaqiyat keltirmaydi.
- Umumiy timeout byudjeti hisobga olinmagani uchun client allaqachon ketgan, server esa retry'larni bajarishda davom etadi.

**Ehtiyot bo'ling:** Retry'ni faqat bitta qatlamda (odatda eng chetkida yoki eng ichkisida, lekin ikkisida emas) qoldiring, faqat transient va idempotent operatsiyalar uchun yoqing va albatta retry budget yoki circuit breaker bilan cheklang. Zanjir bo'ylab umumiy deadline tarqatish (deadline propagation) bo'lmasa, retry har doim kuchaytirgich bo'lib qoladi.

## 25.62 Band ma'lumotlar bazasi (Busy Database)

**Tavsif:** Busy Database - hisoblash ishini keraksiz ravishda DB serveriga yuklash: murakkab biznes mantiqni stored procedure va trigger'larda saqlash, og'ir analitik query'larni OLTP bazada bajarish, yoki jadvalni navbat sifatida polling qilish. DB eng qimmat va eng qiyin gorizontal masshtablanadigan komponent bo'lgani uchun u butun tizimning bo'g'ziga aylanadi. Belgisi: ilova pod'lari bo'sh, DB CPU esa 95%da.

**Spring'da qayerda uchraydi:** `@Scheduled` metodlari bilan har sekundda jadvalni `SELECT ... FOR UPDATE SKIP LOCKED` qilib polling qilish; JPA'da ko'p ishlatiladigan `@Formula` va murakkab native query'lar; barcha hisobotlarni asosiy `DataSource` ustida ishlatish. Yechimlar: mantiqni Java tomoniga ko'chirish, o'qish uchun replika'ga yo'naltirish (`AbstractRoutingDataSource` yoki alohida `@Transactional(readOnly = true)` + ikkinchi `DataSource`), `@Cacheable` bilan takroriy o'qishlarni kamaytirish, navbat uchun Kafka/RabbitMQ ishlatish, HikariCP va Micrometer metrikalari (`hikaricp.connections.pending`, `spring.datasource.hikari.maximum-pool-size`) bilan bosimni kuzatish.

**Qo'llanish keyslari:**
- Kunlik hisobot query'si OLTP bazani bloklab, checkout lotentligini 10 barobar oshiradi.
- Biznes qoidalari PL/pgSQL funksiyalarida yashiringani uchun ularni test qilish va versiyalash imkonsiz.
- 50 ta pod har sekundda `job` jadvalini polling qilib, DB'ga sun'iy yuk hosil qiladi.
- Trigger'lar audit yozuvlarini sinxron yozadi va har bir INSERT ikki barobar sekinlashadi.
- `COUNT(*)` bilan pagination umumiy sonini har bir sahifa uchun qayta hisoblash.

**Ehtiyot bo'ling:** Teskari ekstremal ham xavfli - set-based operatsiyalarni (massiv UPDATE, agregatsiya, JOIN) ilovaga tortib kelish tarmoq va xotira jihatidan ancha qimmatga tushadi. Qoida: ma'lumot yonida bajarilishi tabiiy bo'lgan to'plam operatsiyalari DB'da qolsin, biznes qarorlari va workflow esa ilovada bo'lsin.

## 25.63 Noto'g'ri obyekt yaratish (Improper Instantiation)

**Tavsif:** Improper Instantiation - yaratilishi qimmat va thread-safe bo'lgan obyektlarni har bir so'rov yoki har bir iteratsiyada qaytadan yaratish. Bunday obyektlar o'z ichida connection pool, thread pool, kesh yoki kompilyatsiya qilingan metadata saqlaydi; ularni qayta yaratish CPU, xotira va socket resurslarini isrof qiladi hamda GC bosimini oshiradi. Eng og'ir holatda bu file descriptor yoki ephemeral port tugashiga olib keladi.

**Spring'da qayerda uchraydi:** Tipik xatolar: metod ichida `new RestTemplate()` yoki `WebClient.create()` chaqirish (o'rniga Spring Boot'ning `RestClient.Builder` / `RestTemplateBuilder` / `WebClient.Builder` bean'laridan foydalanish kerak), har safar `new ObjectMapper()` yaratish (Boot allaqachon sozlangan singleton `ObjectMapper` bean beradi), loop ichida `Pattern.compile(...)` yoki `DateTimeFormatter.ofPattern(...)` chaqirish, har bir xabar uchun yangi `KafkaProducer` yoki `EntityManagerFactory` ochish. To'g'ri yondashuv - bularni singleton `@Bean` qilib e'lon qilish yoki `static final` maydonga chiqarish.

```java
@Configuration
class HttpClients {
  @Bean
  RestClient paymentClient(RestClient.Builder builder) {
    return builder.baseUrl("https://payments.internal").build();
  }
}
```

**Qo'llanish keyslari:**
- Har bir HTTP so'rovda yangi `RestTemplate` yaratilib, connection pool qayta ishlatilmaydi va TIME_WAIT socket'lar to'planadi.
- `new ObjectMapper()` har bir serializatsiyada yaratilib, reflection keshi har safar bo'shatiladi.
- Validatsiya metodida regex har chaqiruvda qayta kompilyatsiya qilinadi.
- Har bir event uchun yangi Kafka producer ochilib, metadata fetch qilinadi.
- Test konfiguratsiyasida har bir test uchun yangi `EntityManagerFactory` ko'tarilib, suite 10 barobar sekinlashadi.

**Ehtiyot bo'ling:** Teskari xato ham bor - thread-safe bo'lmagan obyektni (masalan `SimpleDateFormat`, Hibernate `Session`, `StringBuilder`) singleton bean qilib ulashish ma'lumot buzilishiga olib keladi. Shuningdek singleton bean ichiga request-scoped holatni saqlamang; kerak bo'lsa `ObjectProvider` yoki `@Scope("prototype")` ishlatib, holatni aniq ajratib oling.

## 25.64 Monolit saqlash qatlami (Monolithic Persistence)

**Tavsif:** Monolithic Persistence - butunlay turli yuk profiliga ega bo'lgan ma'lumotlarni bitta ma'lumotlar omboriga tiqish: tranzaksion yozuvlar, audit log, sessiya, fayl metadata, analitika va navbat bitta schema'da yashaydi. Natijada bir xil turdagi yuk boshqasini buzadi (audit yozuvlari OLTP lock'larini ushlaydi), schema migration'lari butun tizimni to'xtatadi va hech bir modul mustaqil masshtablanmaydi. Bundan tashqari turli jadvallarga umumiy kirish huquqi modullar o'rtasidagi chegaralarni yemiradi.

**Spring'da qayerda uchraydi:** Bitta `DataSource` va bitta Flyway/Liquibase migration jildi ostida yuzlab jadval; turli modullarning `JpaRepository`'lari bir-birining entity'lariga `@ManyToOne` bilan bog'lanib ketishi. Ajratish vositalari: Spring Boot 3.x'da `@ConfigurationProperties` bilan bir nechta `DataSource` va `LocalContainerEntityManagerFactoryBean` e'lon qilish, modulga xos schema va `flyway.schemas` sozlamasi, Spring Modulith bilan modul chegarasini kompilyatsiya vaqtida tekshirish, issiq bo'lmagan ma'lumotni Redis/S3/time-series bazaga ko'chirish. Bir nechta `DataSource` bilan ishlaganda `@Primary` va `@Transactional("txManagerName")` ni aniq ko'rsatish talab qiladi.

**Qo'llanish keyslari:**
- Audit jadvali 2 TB'ga yetib, asosiy baza backup va vacuum jarayonlarini sekinlashtiradi.
- Bitta modul uchun indeks qo'shish migration'i butun ilovaning deploy'ini bloklaydi.
- Sessiya ma'lumotlari DB'da saqlanib, har so'rovda yozish yuki hosil qiladi (o'rniga Spring Session + Redis).
- Hisobot jadvallari va OLTP jadvallari bir xil connection pool uchun kurashadi.
- Modullar o'zaro jadvalga to'g'ridan-to'g'ri JOIN qilib, keyinchalik ajratishni imkonsiz qiladi.

**Ehtiyot bo'ling:** Ma'lumotlar bazasini bo'lish tranzaksion atomiklikni yo'qotadi va sizni darhol Dual Writes hamda eventual consistency muammolariga olib keladi - shuning uchun avval bitta baza ichida schema va modul chegaralarini o'rnatib, ajratishni faqat haqiqiy masshtab yoki release mustaqilligi talabi paydo bo'lganda bajaring.

## 25.65 Cache'ning yo'qligi (No Caching)

**Tavsif:** No Caching - bir xil, kam o'zgaruvchi ma'lumotni har bir so'rovda qayta hisoblash yoki qayta o'qish. Bu DB va downstream servislarga keraksiz yuk beradi, lotentlikni oshiradi va infratuzilma narxini ko'taradi. Odatda sabab arxitektura emas, balki e'tiborsizlik: hech kim o'qish/yozish nisbatini va ma'lumotning "eskirish" tolerantligini o'lchamagan. Kesh qo'shish ko'pincha eng arzon va eng katta ta'sirli optimizatsiya bo'ladi.

**Spring'da qayerda uchraydi:** Spring Framework 6.x kesh abstraksiyasi: `@EnableCaching`, `@Cacheable`, `@CachePut`, `@CacheEvict`, `CacheManager`. Lokal kesh uchun `CaffeineCacheManager` (`com.github.ben-manes.caffeine`), tarqalgan kesh uchun `RedisCacheManager` (`spring-boot-starter-data-redis`), `spring.cache.type` va `spring.cache.redis.time-to-live` sozlamalari. HTTP qatlamida `ShallowEtagHeaderFilter`, `ResponseEntity` bilan `Cache-Control`/`ETag` qo'yish; JPA darajasida Hibernate ikkinchi darajali keshi (`@Cache`, `hibernate.cache.use_second_level_cache`) va query cache. Keshni kuzatish uchun Micrometer `cache.gets`, `cache.puts` metrikalari mavjud (`CaffeineCacheMetrics`).

**Qo'llanish keyslari:**
- Valyuta kurslari yoki konfiguratsiya ma'lumotlari har so'rovda DB'dan o'qiladi.
- JWT tekshiruvi uchun har chaqiruvda tashqi JWKS endpoint'iga so'rov yuboriladi (o'rniga Nimbus/Spring Security keshi).
- Mahsulot katalogi sahifasi har marta 12 ta JOIN'li query bajaradi.
- Ruxsatlar (permissions) daraxti har bir avtorizatsiya tekshiruvida qayta yig'iladi.
- Statik referens ma'lumot mikroservisga tarmoq orqali har safar so'raladi.

**Ehtiyot bo'ling:** Kesh yangi muammolar sinfini olib keladi: stale data, invalidatsiya murakkabligi, cache stampede (bir vaqtda yuzlab thread bir xil kalitni qayta hisoblashi) va lokal kesh bilan pod'lar orasidagi nomuvofiqlik. Shu sababli TTL'ni aniq belgilang, `@CacheEvict` yo'llarini test bilan qoplang va shaxsiy (per-user) ma'lumotni umumiy kalit ostida keshlab qo'yishdan - bu xavfsizlik incidenti - ehtiyot bo'ling.

## 25.66 Shovqinli qo'shni (Noisy Neighbor)

**Tavsif:** Noisy Neighbor - umumiy resursni bo'lishib ishlatuvchi ko'plab iste'molchidan biri resursni nomutanosib egallab, qolganlarning ishlashini buzishi. Resurs sifatida CPU, connection pool, thread pool, kesh, disk IOPS yoki tarmoq band kengligi bo'lishi mumkin. Multi-tenant tizimlarda bitta tenant'ning og'ir hisoboti barcha mijozlar uchun lotentlikni oshiradi. Muammoning yomon tomoni - sabab aniq ko'rinmaydi, chunki buzilgan servis o'zi aybdor emas.

**Spring'da qayerda uchraydi:** Umumiy `ThreadPoolTaskExecutor`da og'ir va yengil `@Async` vazifalarni aralashtirish; bitta HikariCP pool'ini barcha modullar uchun ishlatish (`hikaricp.connections.pending` metrikasi o'sadi). Izolyatsiya vositalari: Resilience4j `Bulkhead` va `ThreadPoolBulkhead` (semaforli yoki alohida pool), `RateLimiter`, Bucket4j bilan tenant bo'yicha rate limiting, Spring Boot'da bir nechta nomli `TaskExecutor` bean'lari va `@Async("reportExecutor")`, og'ir vazifalarni alohida consumer group yoki alohida deployment'ga ajratish. Platform darajasida Kubernetes CPU/memory limit va `requests` to'g'ri qo'yilishi, Java 21+ uchun esa konteyner-aware heap sozlamalari muhim.

**Qo'llanish keyslari:**
- Bitta yirik mijozning bulk API chaqiruvlari barcha tenantlar uchun p99 lotentlikni oshiradi.
- Hisobot generatsiyasi umumiy `@Async` pool'ini to'ldirib, email yuborish vazifalari navbatda qoladi.
- Bitta modulning uzun query'lari connection pool'ni egallab, boshqa modullar timeout bo'ladi.
- Bitta Kafka partition'dagi og'ir xabarlar butun consumer group'ning lag'ini oshiradi.
- "Shovqinli" pod CPU limiti yo'qligi sababli node'dagi boshqa pod'larni throttling'ga olib keladi.

**Ehtiyot bo'ling:** Haddan ziyod izolyatsiya resurs isrofiga olib keladi - har bir tenant uchun alohida pool va alohida deployment narxi tez o'sadi. Avval metrikalar bilan haqiqiy shovqin manbasini aniqlang, so'ng eng arzon vositadan (rate limiting, alohida pool, navbat ustuvorligi) boshlang va faqat eng katta tenantlar uchun to'liq ajratilgan resursga o'ting.

## 25.67 Bloklovchi sinxron I/O (Synchronous I/O)

**Tavsif:** Synchronous I/O anti-pattern'i - bloklovchi I/O ni noto'g'ri joyda, ya'ni cheklangan va qimmat thread'larni uzoq kutishga majburlaydigan kontekstda bajarish. Bloklangan thread xotira (stack) egallaydi, lekin foydali ish qilmaydi; thread pool tugagach butun ilova javob bermay qoladi. Reaktiv muhitda esa bitta bloklangan event-loop thread minglab so'rovni to'xtatib qo'yadi. Asosiy belgisi: CPU past, lekin throughput shiftga urilgan.

**Spring'da qayerda uchraydi:** Eng xatarli ko'rinish - Spring WebFlux'da `Mono.block()`, bloklovchi JDBC yoki `RestTemplate` chaqiruvini Netty event-loop thread'ida bajarish; BlockHound bu holatni testda aniqlashga yordam beradi. To'g'ri yechimlar: reaktiv stack'da `Schedulers.boundedElastic()` ga ko'chirish yoki R2DBC'dan foydalanish; Spring MVC'da esa Java 21+ virtual thread'larni yoqish (`spring.threads.virtual.enabled=true`, Boot 3.2+), bu bloklovchi kodni saqlab turgan holda thread narxini keskin kamaytiradi. Uzoq ishlar uchun `@Async` + `ThreadPoolTaskExecutor`, yoki so'rov-javobdan ajratib Kafka orqali asinxron qilish. Har bir client uchun read/connect timeout majburiy.

**Qo'llanish keyslari:**
- WebFlux controller'ida `userClient.get().block()` chaqirilib, yuk ortganda butun ilova muzlab qoladi.
- 30 sekundlik tashqi to'lov chaqiruvi Tomcat'ning 200 ta thread'ini to'liq egallaydi.
- Fayl yuklash oqimi so'rov thread'ida sinxron tarzda S3'ga yoziladi.
- Scheduler vazifasi bitta thread'da bloklovchi ishni bajarib, keyingi ishga kechikadi.
- `CompletableFuture.get()` timeout'siz chaqirilib, thread cheksiz kutib qoladi.

**Ehtiyot bo'ling:** Asinxronlikni hamma joyda majburlash kodni keraksiz murakkablashtiradi - Java 21+ virtual thread'lar ko'p holatda reaktiv migratsiyani ortiqcha qiladi. Lekin virtual thread'lar `synchronized` bloklar va ba'zi native kutubxonalarda pinning'ga uchraydi, hamda thread sonining cheklanmasligi sababli downstream'ni himoya qilish uchun semafor yoki bulkhead qo'shishni talab qiladi.

## 25.68 Keraksiz ma'lumot olish (Extraneous Fetching)

**Tavsif:** Extraneous Fetching - kerak bo'lganidan ko'p ma'lumot o'qish: barcha ustunlarni (`SELECT *`), barcha qatorlarni yoki butun obyekt grafini olib, keyin ularning kichik qismini ishlatish. Bu DB I/O, tarmoq trafigi, serializatsiya vaqti va JVM heap'iga keraksiz bosim beradi, ba'zan esa `OutOfMemoryError` bilan tugaydi. Chatty I/O ning aksi: so'rovlar kam, lekin har biri haddan katta.

**Spring'da qayerda uchraydi:** JPA'da `FetchType.EAGER` bilan bog'langan kolleksiyalar; `findAll()` ni pagination'siz chaqirish; filtrlashni Java tomonida (`stream().filter(...)`) bajarish. Yechimlar: Spring Data'ning interface va DTO projection'lari, JPQL konstruktor ifodalari (`select new com.app.OrderView(o.id, o.total) from Order o`), `Pageable`/`Slice`/`ScrollPosition` bilan sahifalash, `@EntityGraph` bilan aniq fetch rejasi, katta natijalar uchun `Stream<T>` yoki `JdbcTemplate` bilan `setFetchSize`. HTTP qatlamida sparse fieldsets yoki GraphQL (`spring-boot-starter-graphql`) ortiqcha maydonlarni kesishga yordam beradi, lekin GraphQL'ning o'zi N+1 xavfini keltiradi (`DataLoader`/`BatchMapping` kerak).

**Qo'llanish keyslari:**
- Ro'yxat sahifasi uchun butun `Order` entity'si barcha `@Lob` maydonlari bilan o'qiladi.
- `findAll()` 2 million qatorni heap'ga tortib, pod OOM bilan qayta ishga tushadi.
- Hisobot uchun faqat `id` va `total` kerak bo'lsa ham to'liq obyekt grafi fetch qilinadi.
- Tashqi API'dan to'liq mijoz profili olinib, undan faqat email ishlatiladi.
- Qidiruv natijalari DB'da emas, Java'da filtrlanadi va 95% qator tashlab yuboriladi.

**Ehtiyot bo'ling:** Projection'larni haddan ziyod ko'paytirish maintenance yukini oshiradi, `@Transactional` tashqarisida lazy maydonga murojaat qilish esa `LazyInitializationException` beradi - `spring.jpa.open-in-view` ni yoqib bu muammoni "yashirish" esa yana Chatty I/O ga olib keladi (production'da uni o'chirish tavsiya etiladi). Shuningdek entity o'rniga projection o'qilganda ikkinchi darajali kesh va dirty checking ishlamaydi.

## 25.69 Ikki tomonlama yozish (Dual Writes)

**Tavsif:** Dual Writes - bitta biznes operatsiyasi doirasida ikki xil tizimga (masalan DB'ga va Kafka'ga, yoki DB'ga va keshga) alohida, atomik bo'lmagan ikki yozuv bajarish. Birinchi yozuv muvaffaqiyatli bo'lib, ikkinchisi xato bersa yoki process shu orada o'lsa, tizimlar bir-biriga mos kelmaydigan holatda qoladi: buyurtma bazada bor, lekin event yuborilmagan (yoki teskarisi). Bu nomuvofiqlik odatda darhol sezilmaydi va keyinchalik hal qilish juda qiyin bo'ladi.

**Spring'da qayerda uchraydi:** Tipik xato - `@Transactional` metod ichida `repository.save(order)` dan keyin darhol `kafkaTemplate.send(...)` chaqirish: JMS/Kafka va JDBC turli resurslar bo'lgani uchun ular bitta atomik commit emas. To'g'ri yechim - Transactional Outbox: event'ni bir xil tranzaksiyada outbox jadvaliga yozish va keyin alohida publisher yoki Debezium CDC bilan yuborish. Spring'da buni `@TransactionalEventListener(phase = AFTER_COMMIT)` (eng yaxshisi Spring Modulith'ning `@ApplicationModuleListener` va Event Publication Registry bilan, u yuborilmagan event'larni qayta urinish uchun saqlaydi) orqali amalga oshiriladi. Eslatma: `ChainedTransactionManager` best-effort bo'lgan va Spring Data'da deprecated qilingan - uni atomiklik vositasi deb hisoblamang.

```java
@Transactional
public void confirm(Order order) {
  order.confirm();
  repository.save(order);
  events.publishEvent(new OrderConfirmed(order.getId())); // outbox'ga yoziladi
}
```

**Qo'llanish keyslari:**
- Buyurtma bazada saqlanadi, lekin Kafka broker mavjud bo'lmagani uchun `OrderCreated` event yo'qoladi.
- Kesh yangilanadi, so'ng DB tranzaksiyasi rollback bo'ladi va kesh noto'g'ri ma'lumot ko'rsatadi.
- Elasticsearch indeksi DB bilan sinxron yozilib, nosozlikdan keyin abadiy farq qoladi.
- Fayl S3'ga yuklanadi, metadata yozuvi esa xato bilan tugaydi - yetim fayl paydo bo'ladi.
- To'lov provayderiga chaqiruv yuborilib, lokal yozuv saqlanmaydi va pul "ko'rinmas" bo'lib qoladi.

**Ehtiyot bo'ling:** Outbox ham mukammal emas: u at-least-once semantikani beradi, shuning uchun consumer tomonida idempotentlik (deduplikatsiya kaliti, `ON CONFLICT DO NOTHING`) majburiy. Outbox jadvalini tozalashni (retention) rejalashtirmasa, u Monolithic Persistence muammosiga aylanadi; shuningdek event tartibini faqat kalit bo'yicha (partition key) kafolatlash mumkinligini hisobga oling.

## 25.70 Servislar o'rtasida ikki fazali commit (Two-Phase Commit across services)

**Tavsif:** 2PC (XA) bir nechta resursni bitta atomik tranzaksiyaga birlashtirish uchun koordinator, prepare va commit fazalaridan foydalanadi. Mikroservislar o'rtasida qo'llanganda u barcha qatnashchilarni koordinator javobini kutishga majbur qiladi: lock'lar uzoq ushlanadi, lotentlik oshadi, mavjudlik eng kuchsiz qatnashchiga teng bo'ladi va koordinator prepare bilan commit orasida o'lsa, qatnashchilar "in-doubt" holatda qotib qoladi. Shu sababli u servislar chegarasida masshtablanmaydigan va nozik yechim hisoblanadi.

**Spring'da qayerda uchraydi:** Spring Framework 6.x'da `JtaTransactionManager` va Jakarta JTA orqali XA hali ham mavjud, ammo Spring Boot 3.x'da Atomikos uchun auto-configuration olib tashlangan, Narayana esa jamoa tomonidan qo'llab-quvvatlanadigan alohida starter (`narayana-spring-boot-starter`) orqali ishlatiladi - bu ekosistemaning yo'nalishini yaxshi ko'rsatadi. Kafka va ko'pchilik HTTP API'lar XA'ni umuman qo'llab-quvvatlamaydi. O'rniga Saga ishlatiladi: xoreografiya (Kafka event'lari + Transactional Outbox + idempotent consumer) yoki orkestratsiya (Camunda, Temporal, Axon Framework, Eventuate Tram, yoki `@StateMachine` bilan Spring Statemachine), har bir qadam uchun kompensatsion amal (`refund`, `releaseStock`) yoziladi.

**Qo'llanish keyslari:**
- Buyurtma, ombor va to'lov servislarini XA bilan bog'lashga urinish va ombor DB'sida uzoq lock'lar olish.
- Koordinator nosozligidan keyin in-doubt tranzaksiyalarni DBA qo'lda tozalashi.
- Saga bilan yozilgan checkout: to'lov muvaffaqiyatsiz bo'lsa, zaxiradagi tovar `releaseStock` bilan qaytariladi.
- Legacy JMS + JDBC integratsiyasi bitta JVM ichida, bitta vendor ostida XA ishlatadi (o'rinli holat).
- Pul o'tkazmasi bo'yicha ko'p qadamli jarayon Temporal workflow sifatida kompensatsiyalar bilan modellashtiriladi.

**Ehtiyot bo'ling:** Saga 2PC'ning "bepul" o'rnini bosuvchisi emas: u atomiklikni eventual consistency va kompensatsiyaga ayirboshlaydi, shuning uchun oraliq holatlar biznes tomonidan ko'rinadi (masalan "to'lov kutilmoqda") va buni UI hamda qoidalarda aniq modellashtirish kerak. Kompensatsion amallar har doim mumkin bo'lmaydi (yuborilgan email'ni qaytarib olmaysiz), shuning uchun avval chegaralarni qayta ko'rib chiqing - agar ikki qadam haqiqatan atomik bo'lishi shart bo'lsa, ehtimol ular bitta servis va bitta tranzaksiya ichida bo'lishi kerak.

## 25.71 Taminotchi qulfi (Vendor Lock-in)

**Tavsif:** Tizim muayyan bulut provayderi, ma'lumotlar bazasi yoki tijorat mahsulotining xususiy API'lariga shunchalik chuqur bog'lanib qoladiki, undan chiqish narxi amalda ko'chishni imkonsiz qiladi. Anti-pattern sifatida u texnik qaror emas, balki e'tiborsizlik natijasida yuzaga keladi: provayder SDK'si domen qatlamiga, hatto entity'largacha kirib boradi. Natijada narx oshganda yoki provayder xizmatni to'xtatganda muhandislik jamoasi hech qanday manevr maydoniga ega bo'lmaydi. To'g'ri yechim - bog'liqlikni ongli ravishda tanlash va uni adapter qatlami bilan chegaralash.

**Spring'da qayerda uchraydi:** Spring'ning o'zi abstraksiya qatlamlarini taklif qiladi - `JdbcTemplate`, `PlatformTransactionManager`, `JmsTemplate`, `CacheManager`, Spring Data'ning `Repository` interfeyslari - lekin ular chetlab o'tilganda qulf paydo bo'ladi: `io.awspring.cloud:spring-cloud-aws-starter` orqali `S3Client` va `SqsTemplate`'ni to'g'ridan-to'g'ri `@Service` sinflari ichida chaqirish, `@Query(nativeQuery = true)` bilan PostgreSQL yoki Oracle'ga xos SQL yozish, Hibernate'ning provayderga xos `Dialect` imkoniyatlariga tayanish. Spring Boot 3.x/4.x'dagi `@ConfigurationProperties` va `@Profile` bilan infratuzilma sozlamalarini ajratish, hexagonal uslubda port interfeysini e'lon qilib, provayder SDK'sini faqat `@Component` adapter ichida ushlab turish qulfni sezilarli kamaytiradi.

**Qo'llanish keyslari:**
- Bank integratsiyasida `WebClient` yoki `RestClient` o'rniga provayderning yopiq SDK'si butun kod bazasiga sochilib ketgan va ikkinchi provayder qo'shish 6 oy talab qiladi.
- Fayl saqlash logikasi to'g'ridan-to'g'ri AWS `S3Client`'ga bog'langani uchun on-premise MinIO'ga ko'chish uchun 200 dan ortiq sinf o'zgartirishga majbur bo'ladi.
- Hisobot so'rovlari Oracle analytic funksiyalarida yozilgani uchun jamoa PostgreSQL'ga ko'chishdan voz kechadi.
- Managed Kafka o'rniga provayderning xususiy message bus'i tanlanib, `@KafkaListener` emas, yopiq client ishlatilgani uchun lokal integratsiya testlari Testcontainers bilan yozilmaydi.
- Autentifikatsiya provayderning xususiy token formatiga bog'langan va standart `spring-boot-starter-oauth2-resource-server` konfiguratsiyasiga o'tish imkonsiz bo'ladi.

**Ehtiyot bo'ling:** Qulfdan qo'rqib hamma narsani abstraksiya qilish o'zi alohida anti-pattern - "eng past umumiy maxraj" abstraksiyasi provayderning eng kuchli imkoniyatlarini yo'q qiladi va Accidental Complexity keltiradi. Qulfni faqat haqiqatan chiqish ehtimoli bor va narxi yuqori bo'lgan nuqtalarda (ma'lumotlar bazasi, message broker, identity) chegaralang, qolgan joyda provayder imkoniyatlaridan to'liq foydalanish arzonroq tushadi.

## 25.72 Rezyume uchun dasturlash (Resume-Driven Development)

**Tavsif:** Texnologiya mahsulot ehtiyoji emas, balki muhandisning shaxsiy rezyumesini boyitish istagi asosida tanlanadi. Qarorlar "bu bizga nima beradi" emas, "bu moda va men buni o'rganmoqchiman" mantig'i bilan qabul qilinadi, natijada oddiy CRUD tizimi reactive stack, event sourcing, service mesh va GraphQL bilan qoplanadi. Anti-patternning xavfi shundaki, uni qo'zg'atgan muhandis ko'pincha 1-2 yildan keyin ketadi, texnik qarz esa jamoada qoladi. Bunday tanlovlar hech qachon ADR'da halol asoslanmaydi, chunki asl motiv yozib qo'yilmaydi.

**Spring'da qayerda uchraydi:** Eng tipik ko'rinishlari - ehtiyoj bo'lmasa ham `spring-boot-starter-web` o'rniga `spring-boot-starter-webflux` va `R2DBC` tanlash (holbuki Java 21+ virtual thread'lari va `spring.threads.virtual.enabled=true` bilan blocking MVC yetarli bo'ladi), uch endpoint uchun `spring-boot-starter-graphql` qo'shish, 50 ming so'rovli tizimga Spring Cloud Gateway, Eureka va `spring-cloud-config-server`dan to'liq microservice to'plami yoyish, yoki faqat "zamonaviy" bo'lish uchun GraalVM native image (`spring-boot-maven-plugin`'ning `native` profili) ga o'tib, reflection muammolari bilan oylar yo'qotish. Spring Framework 6.x/7.x'da `RestClient` kabi sodda vositalar mavjud bo'lsa ham, jamoa murakkabroq reactive `WebClient` zanjirlarini tanlaydi.

**Qo'llanish keyslari:**
- Bir jamoa oyiga 20 ming so'rov keladigan ichki admin paneli uchun WebFlux + R2DBC tanlab, debug va stack trace murakkabligi tufayli incident'larni tahlil qila olmay qoladi.
- Monolitda uchta modul borligida Kubernetes + Istio + 12 ta microservice arxitekturasiga o'tiladi va DevOps xarajati mahsulot daromadidan oshadi.
- Hisobot xizmati uchun Kafka Streams joriy qilinadi, holbuki kunlik batch `@Scheduled` job yetarli edi.
- Oddiy status tracking uchun to'liq event sourcing + CQRS qurilib, ma'lumotlarni o'qish uchun har safar projection qayta tiklanadi.
- Yangi loyihada Spring Boot 4.x'ning eksperimental imkoniyatlari production'da sinaladi va release muddati ikki barobar cho'ziladi.

**Ehtiyot bo'ling:** Yangi texnologiyani taqiqlash ham xato - jamoa o'sishini to'xtatadi va Not Invented Here'ga olib keladi; to'g'ri yo'l har bir yirik tanlov uchun ADR talab qilish va unda o'lchanadigan mezon (latency, xarajat, jamoa tajribasi) ko'rsatishdir. Tajriba qilish istagini production emas, ajratilgan spike yoki ichki vositalarga yo'naltiring.

## 25.73 Arxitektura astronavti (Architecture Astronaut)

**Tavsif:** Arxitektor real muammodan shunchalik uzoqlashib, shunchalik umumiy abstraksiyalar quradiki, ular hech qanday aniq talabni hal qilmaydi. Natija - "har qanday kelajakdagi ehtiyojni qoplaydigan" plugin tizimi, generic bazaviy sinflar iyerarxiyasi va o'z-o'zini tushuntirmaydigan metamodel. Kod o'qilishi qiyin, yangi a'zo onboarding'i haftalar davom etadi, oddiy maydon qo'shish uchun besh qatlamni o'zgartirish kerak bo'ladi. Bu anti-pattern ko'pincha "biz bunga tayyor bo'lishimiz kerak" degan asoslanmagan kelajak prognozidan tug'iladi.

**Spring'da qayerda uchraydi:** `AbstractGenericService<T, ID, D>` tipidagi uch-to'rt generic parametrli bazaviy sinflar, har bir domen uchun o'z `BeanFactoryPostProcessor` va `BeanDefinitionRegistryPostProcessor` yozish, Spring'ning ustiga o'z DI/lifecycle "frameworki"ni qurish, har bir mayda imkoniyat uchun alohida auto-configuration starter (`@AutoConfiguration`, `META-INF/spring/org.springframework.boot.autoconfigure.AutoConfiguration.imports`) chiqarish, yoki hamma joyda `ApplicationContext`'ni to'g'ridan-to'g'ri inject qilib dinamik bean izlash. Ko'pincha o'z `@Around` advice'lari `ProxyFactoryBean` bilan birga sochilib, Spring'ning o'z AOP va `@Transactional` semantikasi bilan ziddiyatga kiradi. Bunga qarshi vosita - ArchUnit yoki Spring Modulith'ning `ApplicationModules.verify()` bilan qatlamlarni oddiy va tekshiriladigan saqlash.

**Qo'llanish keyslari:**
- Jamoa barcha entity'lar uchun generic `BaseEntity`, `BaseService`, `BaseController` iyerarxiyasini qurib, har bir noodatiy use case uchun uni "aldab" o'tishga majbur bo'ladi.
- Oddiy to'lov integratsiyasi uchun ichki plugin SPI yozilib, amalda bitta implementatsiya chiqadi va u hech qachon almashtirilmaydi.
- Har bir modul o'z custom starter'iga ajratilib, 14 ta artefakt versiyasini sinxron ushlash alohida ish bo'lib qoladi.
- Konfiguratsiya tashqi DSL'ga chiqariladi va jamoa `@ConfigurationProperties` o'rniga o'z parser'ini qo'llab-quvvatlashga majbur bo'ladi.
- Domen modeli to'liq metadata-driven qilinadi: yangi maydon kodda emas, ma'lumotlar bazasidagi jadvalda e'lon qilinadi va IDE yordami, compile-time xavfsizlik yo'qoladi.

**Ehtiyot bo'ling:** Abstraksiyani uchinchi real takrorlanish paydo bo'lgandan keyin kiritish qoidasini (rule of three) qo'llang va har bir yangi qatlam uchun "bugun qaysi talabni hal qiladi" savoliga yozma javob talab qiling. Arxitektura diagrammasi kod bilan tekshirilmasa (ArchUnit, Spring Modulith `Documenter`), astronavt chizgan rasm ikki sprintdan keyin yolg'onga aylanadi.

## 25.74 Tasodifiy murakkablik (Accidental Complexity)

**Tavsif:** Muammoning o'ziga xos (essential) murakkabligi emas, balki tanlangan vositalar, ortiqcha qatlamlar va noto'g'ri qarorlar natijasida paydo bo'lgan qo'shimcha murakkablik. Uni aniqlash oson: bitta maydonni qo'shish uchun olti faylga tegish kerak bo'ladi, yoki bitta so'rov yo'li beshta mapper orqali o'tadi. Tasodifiy murakkablik asta-sekin to'planadi, chunki har bir alohida qadam mantiqiy ko'rinadi. Arxitektorning vazifasi - qaysi murakkablik domenga tegishli, qaysi biri bizning xatomiz ekanini ajratish.

**Spring'da qayerda uchraydi:** Entity → JPA projection → internal DTO → API DTO → response wrapper zanjiri va ularni bog'lovchi MapStruct mapper'lari; har bir sinfga tarqalgan `@Value("${...}")` o'rniga `@ConfigurationProperties` ishlatmaslik; `@Transactional` noto'g'ri joylarda (controller'da yoki `@Async` metod ichida) qo'yilib, `LazyInitializationException` va proxy muammolarini keltirib chiqarishi; CRUD xizmat uchun sakkiz Maven moduli; Spring Boot auto-configuration bergan standart xatti-harakatni qo'lda `@Bean` bilan qayta e'lon qilib, keyin `spring.autoconfigure.exclude` bilan jang qilish. `spring-boot-starter-*` to'plamlari va `spring-boot-dependencies` BOM aynan shu murakkablikni kamaytirish uchun mavjud, lekin ular chetlab o'tilsa, versiya boshqaruvi qo'lda qilinadi.

**Qo'llanish keyslari:**
- Bitta yangi maydon qo'shish uchun entity, ikki DTO, mapper, validator, Liquibase changelog va OpenAPI faylini qo'lda yangilash talab qiladi.
- Jamoa Spring Security'ning standart `SecurityFilterChain` konfiguratsiyasi ustiga o'z filter'lar zanjirini qo'shib, autentifikatsiya oqimini hech kim to'liq tushuntirib bera olmaydi.
- `application.yml` 1200 qatorga yetadi, chunki profil irsiyati noto'g'ri qurilgan va qiymatlar takrorlanadi.
- Har bir mikroservisda o'z qo'lda yozilgan exception → HTTP status mapping kodi bor, `@ControllerAdvice` va `ProblemDetail` esa ishlatilmaydi.
- Oddiy ichki chaqiruvlar HTTP orqali amalga oshiriladi, chunki modullar sun'iy ravishda alohida servislarga ajratilgan.

**Ehtiyot bo'ling:** Murakkablikni kesishni "hamma qatlamni olib tashlash" deb tushunmang - DTO va domen ajratilishi ko'pincha haqiqiy ehtiyoj, uni yo'q qilish esa API'ni ma'lumotlar bazasi sxemasiga bog'lab qo'yadi. O'lchov sifatida "bitta tipik o'zgarish uchun tegiladigan fayllar soni" metrikasini kuzatib, uni qisqartirishga harakat qiling.

## 25.75 Hodisa spagettisi (Event Spaghetti)

**Tavsif:** Tizim hodisalar orqali bog'langan, lekin hodisalar oqimi hech qayerda hujjatlashtirilmagan va kuzatilmaydi - bir hodisa ikkinchisini, u uchinchisini chaqiradi va yakuniy ta'sirni oldindan aytib bo'lmaydi. Debug qilish uchun muhandis loglar bo'ylab hodisalarni qo'lda bog'lashga majbur bo'ladi, cheksiz tsikllar esa production'da aniqlanadi. Bu ko'pincha "biz loosely coupled bo'lamiz" niyati bilan boshlanadi, ammo bog'liqlik yo'qolmaydi - faqat ko'rinmas bo'lib qoladi. Yechim - hodisalar chegaralarini modullar bilan moslashtirish va oqimni avtomatik hujjatlashtirish.

**Spring'da qayerda uchraydi:** `ApplicationEventPublisher.publishEvent()` va `@EventListener` metodlari butun kod bazasiga sochilib ketishi; `@TransactionalEventListener` fazasi (`AFTER_COMMIT` va `BEFORE_COMMIT`) noto'g'ri tanlanib, ma'lumotlar bazasiga yozuv yo'qolishi; `@Async` listener'larda xatolik yutilib ketishi, chunki `AsyncUncaughtExceptionHandler` sozlanmagan; Spring Cloud Stream yoki `@KafkaListener` zanjirlari bir topic'dan boshqasiga cheksiz ko'payishi. Spring Modulith (`spring-modulith-starter-core`, `@ApplicationModuleListener`, `spring-modulith-events-jpa` bilan Event Publication Registry) hodisalarni modul chegaralariga bog'lash, qayta urinish va `Documenter` orqali oqim diagrammasini generatsiya qilish imkonini beradi; Micrometer Tracing esa korrelyatsiya ID'si bilan zanjirni kuzatiladigan qiladi.

```java
@ApplicationModuleListener // = @Async + @Transactional + @TransactionalEventListener(AFTER_COMMIT)
void on(OrderCompleted event) {
    invoiceService.issue(event.orderId());
}
```

**Qo'llanish keyslari:**
- Buyurtma yopilganda yuborilgan hodisa oxir-oqibat yana buyurtmani yangilab, cheksiz tsikl hosil qiladi va production'da CPU 100% ga chiqadi.
- `@TransactionalEventListener(phase = BEFORE_COMMIT)` ichida tashqi API chaqirilib, transaction rollback bo'lganda mijozga noto'g'ri SMS ketadi.
- Hodisalarning 40 ta listener'i bor, lekin qaysi biri majburiy, qaysi biri ixtiyoriy ekani hujjatlashtirilmagan.
- `@Async` listener'da yuzaga kelgan `RuntimeException` hech qayerga yozilmaydi va ma'lumot jim-jitlikda yo'qoladi.
- Mikroservislar o'rtasida hodisa sxemasi versiyalanmagani uchun bitta maydon nomini o'zgartirish beshta consumer'ni buzadi.

**Ehtiyot bo'ling:** Hodisalarni "fire and forget" deb tushunmang - ishonchlilik kerak bo'lsa, transactional outbox yoki Spring Modulith'ning Event Publication Registry'sidan foydalaning, aks holda commit va publish o'rtasida ma'lumot yo'qoladi. Bir modul ichidagi oddiy chaqiruvni hodisaga aylantirish deyarli har doim zarar: hodisani faqat haqiqiy modul chegarasida ishlatish kerak.

## 25.76 Oltin qoplama (Gold Plating)

**Tavsif:** Jamoa talab qilinmagan, hech kim so'ramagan imkoniyatlarni "foydali bo'lar" degan umid bilan qo'shadi va mahsulot yetkazib berishni kechiktiradi. Har bir ortiqcha imkoniyat o'z test, hujjat, migratsiya va xavfsizlik yuzasini olib keladi, lekin biznes qiymati nolga teng. Anti-pattern xususan tajribali jamoalarda uchraydi: ular "to'g'ri" yechim qurishga intilib, kerakli minimal yechimdan ancha uzoqlashadi. Oqibatda qo'llab-quvvatlash xarajati hech qachon qaytmaydigan investitsiyaga aylanadi.

**Spring'da qayerda uchraydi:** Ichki xizmatga hech kim ishlatmaydigan multi-tenancy qatlamini (`AbstractRoutingDataSource` + tenant resolver) qo'shish; barcha `@Service` metodlarini `@Cacheable` bilan qoplab, keyin invalidatsiya muammolarini hal qilishga majbur bo'lish; `management.endpoints.web.exposure.include=*` bilan barcha Actuator endpoint'larini ochib qo'yish; ehtiyoj yo'q joyda `spring-boot-starter-batch`, Quartz cluster va to'liq audit log infratuzilmasini qurish; `@Validated` guruhlarining besh darajali kombinatsiyasini e'lon qilib, amalda ikkitasidan foydalanish. Spring Boot'ning `@ConditionalOnProperty` va feature flag'lari ko'pincha shunday ortiqcha imkoniyatlarni "o'chirilgan holatda" ushlab turish uchun ishlatiladi, ya'ni kod bazasi o'sadi, foyda esa yo'q.

**Qo'llanish keyslari:**
- Bitta mijoz uchun yozilgan xizmatga 50 ta tenant'ni qo'llab-quvvatlovchi routing qo'shiladi va u ikki yil ishlatilmaydi.
- Hisobot eksporti PDF, XLSX, CSV, XML va JSON formatlarida yozilib, foydalanuvchilar faqat XLSX'dan foydalanadi.
- Barcha endpoint'lar uchun universal filtrlash/saralash DSL yozilib, u SQL injection auditida muammo manbaiga aylanadi.
- Yangi xizmatda GraphQL ham, REST ham, gRPC ham chiqariladi va uchta kontraktni sinxron ushlash talab qiladi.
- Har bir metod uchun `@Cacheable` qo'yilgan tizimda stale ma'lumot hisob-kitob xatosiga olib keladi.

**Ehtiyot bo'ling:** Gold Plating bilan haqiqiy nonfunctional talabni (xavfsizlik, kuzatuvchanlik, migratsiya yo'li) aralashtirib yubormang - Actuator health/metrics yoki audit log ko'pincha zarur, ularni "ortiqcha" deb kesish boshqa muammo tug'diradi. Oddiy filtr: imkoniyatni so'ragan aniq stakeholder va o'lchanadigan natija bo'lmasa, uni backlog'da qoldiring.

## 25.77 Tahlil falaji (Analysis Paralysis)

**Tavsif:** Jamoa qaror qabul qilish uchun yetarli ma'lumot to'playdi, keyin yana to'playdi, va hech qachon harakatga o'tmaydi. Har bir variant uchun yangi savol topiladi, POC'lar bir-birini almashtiradi, muddat esa siljiydi. Asosiy sabab - noto'g'ri qarordan qo'rqish va qarorning qaytarib bo'lmasligi haqidagi noto'g'ri taxmin. Ko'pgina arxitektura qarorlari aslida qaytarilishi mumkin, va ularni tezda sinab ko'rish uzoq tahlildan arzonroq tushadi.

**Spring'da qayerda uchraydi:** "WebFlux yoki MVC", "R2DBC yoki JDBC", "Spring Cloud Gateway yoki Nginx", "Spring Modulith modulli monolit yoki microservice" tipidagi bahslar oylar davom etishi; `start.spring.io` bilan bir kunda prototip yig'ish mumkin bo'lsa ham, jamoa taqqoslash jadvallarini to'ldirishda qolishi; Spring Boot 3.x'dan 4.x'ga yoki `javax` → `jakarta` ko'chishini "to'liq o'rganib chiqqandan keyin" boshlash qarori bir yilga cho'zilishi. Amaliy qarshi vosita - Testcontainers va `@SpringBootTest` bilan ikki variantni bir hafta ichida real yuk ostida o'lchash, natijani ADR'ga yozib, qarorni yopish; `spring-boot-devtools` va `spring-boot-testcontainers` bu tsiklni yanada tezlashtiradi.

**Qo'llanish keyslari:**
- Ma'lumotlar bazasi tanlash bo'yicha qaror to'rt oy cho'ziladi va shu vaqt ichida biror funksional imkoniyat chiqmaydi.
- Jamoa uchta message broker'ni taqqoslab, hech birini joriy qilmaydi, mijoz esa integratsiyani kutib turadi.
- Har bir ADR qoralamasi yangi "nima bo'lsa" savoli bilan qaytariladi va hech qachon tasdiqlanmaydi.
- Monolitni ajratish rejasi diagramma darajasida qoladi, chunki "to'g'ri chegaralarni" aniqlashga kelishib bo'lmaydi.
- Performance optimizatsiyasi profiling o'rniga nazariy bahs bilan hal qilinmoqchi bo'ladi va bo'g'in joy noto'g'ri aniqlanadi.

**Ehtiyot bo'ling:** Falajning aksi - o'ylanmagan tezkor qarorlar, shuning uchun qaytarilishi qiyin qarorlarni (ma'lumotlar modeli, public API kontrakti, ma'lumotlar bazasi) alohida ajratib, ularga ko'proq vaqt bering. Har bir qaror uchun muddat (timebox) va "qaytarish narxi" bahosini belgilash eng samarali davodir.

## 25.78 Mayda-chuyda bahs (Bikeshedding)

**Tavsif:** Jamoa muhim va murakkab masalalarni chetlab o'tib, tushunarli, ammo ahamiyatsiz detallar ustida uzoq bahslashadi - chunki hamma o'z fikrini aytishi oson. Natijada code review va arxitektura uchrashuvlari nomlash, formatlash va uslub bahslariga aylanadi, haqiqiy riskli qarorlar esa muhokamasiz o'tib ketadi. Bu anti-pattern vaqtni emas, e'tiborni yo'q qiladi: eng qimmat resurs noto'g'ri joyga sarflanadi. Davosi - ahamiyatsiz masalalarni avtomatlashtirish yoki bir marta qaror qilib yopish.

**Spring'da qayerda uchraydi:** Paket nomlash (`com.x.service` yoki `com.x.application`), Lombok'ning `@Data`'si va Java 17+ `record` o'rtasidagi cheksiz bahslar, `Optional` qaytarish uslubi, `@Autowired` field injection va constructor injection haqidagi muhokama (bu masala aslida ahamiyatli - Spring 4.3'dan beri bitta konstruktor uchun `@Autowired` shart emas, shuning uchun uni kelishuv bilan bir marta yopish kerak). Avtomatlashtirish vositalari bahsni to'xtatadi: `spotless-maven-plugin` yoki Checkstyle/`google-java-format` formatlashni, `spring-javaformat` Spring uslubini, ArchUnit testlari paket qoidalarini majburiy qiladi, shu bilan uslub savollari review'dan butunlay chiqib ketadi.

**Qo'llanish keyslari:**
- Pull request'da 30 ta izoh nomlash va bo'sh qatorlar haqida, SQL N+1 muammosi esa e'tibordan chetda qoladi.
- Jamoa `ProductDto` yoki `ProductResponse` nomini tanlash uchun ikki uchrashuv o'tkazadi.
- Arxitektura kengashida Kafka retry strategiyasi o'rniga log formati muhokama qilinadi.
- Lombok'dan voz kechish bahsi sprint'ni to'sadi, holbuki `record` va `@ConfigurationProperties` birgalikda masalaning yarmini hal qilgan edi.
- Yangi mikroservis uchun REST yo'l nomlari (`/v1/orders` yoki `/orders/v1`) haftalik bahsga aylanadi, versiyalash strategiyasi esa umuman kelishilmaydi.

**Ehtiyot bo'ling:** Hamma uslub masalasini "bikeshedding" deb rad etmang - API kontrakti nomlari, hodisa sxemalari va public kutubxona nomlari uzoq muddatli ta'sirga ega va ularni jiddiy muhokama qilish o'rinli. Linter bilan avtomatlashtiriladigan narsani linter'ga bering, qolgan bahs uchun qaror egasi (DRI) belgilang.

## 25.79 Komissiya bilan loyihalash (Design by Committee)

**Tavsif:** Dizayn qarori ko'p sonli manfaatdor tomonlarning har biri o'z talabini kiritishi natijasida shakllanadi va yagona izchil tasavvurga ega bo'lmaydi. Har kimning fikri hisobga olinadi, hech kim "yo'q" deyishga vakolatli bo'lmaydi, natijada API yoki arxitektura kompromislar to'plamiga aylanadi. Bunday tizim barcha ssenariylarni qisman qoplaydi, lekin birortasini yaxshi bajarmaydi. Belgisi - bir xil ishni bajaradigan bir nechta parallel mexanizm bir vaqtda mavjud bo'lishi.

**Spring'da qayerda uchraydi:** Har bir jamoaning talabini qo'shgan OpenAPI kontrakti 300 ta ixtiyoriy maydonga ega bo'lishi va `@Validated` qoidalari bir-biriga zid kelishi; umumiy ichki "platform starter" har bir jamoaning iltimosi bilan o'sib, 40 ta `@ConditionalOnProperty` shartiga ega auto-configuration'ga aylanishi; Spring Security konfiguratsiyasida bir nechta `SecurityFilterChain` bean'lari turli jamoalar tomonidan qo'shilib, `@Order` qiymatlari ziddiyatga kirishi; umumiy `application.yml` har bir mahsulot egasi qo'shgan flag bilan to'lib ketishi. Spring Modulith yoki ArchUnit bilan modul egaligini (ownership) kodda majburiy qilish va har bir modulga aniq mas'ul belgilash kompromis dizaynga qarshi eng ishonchli himoya.

**Qo'llanish keyslari:**
- Umumiy API'da bir xil ma'lumotni qaytaruvchi uchta endpoint paydo bo'ladi, chunki har bir iste'molchi o'z formatini talab qilgan.
- Ichki platform starter'ga qo'shilgan har bir flag boshqa jamoani buzadi va versiya yangilash deyarli imkonsiz bo'ladi.
- Autentifikatsiya oqimi uchta xil variantni qo'llab-quvvatlaydi, chunki hech bir jamoa o'z yondashuvidan voz kechmaydi.
- Hodisa sxemasiga barcha jamoalarning maydonlari kiritilib, consumer'lar uchun kontrakt ma'nosiz bo'lib qoladi.
- Yagona hisobot modeli o'n bo'limning talabini birlashtirgani uchun hech bir bo'lim uni ishlatmaydi.

**Ehtiyot bo'ling:** Buning aksi - bir kishining yakka qarori bilan boshqa jamoalar ehtiyojini e'tiborsiz qoldirish, bu Stovepipe System va Not Invented Here'ga olib keladi. To'g'ri model: fikr yig'ish keng, qaror qabul qilish esa bitta mas'ul (arxitektor yoki modul egasi) qo'lida bo'lishi va rad etilgan variantlar ADR'da sababi bilan yozilishi.

## 25.80 "Bu yerda o'ylab topilmagan" (Not Invented Here)

**Tavsif:** Jamoa mavjud, sinovdan o'tgan va qo'llab-quvvatlanadigan yechimni ishlatish o'rniga uning o'z versiyasini yozadi, ko'pincha "bizning holatimiz o'ziga xos" degan asos bilan. O'z implementatsiyasi boshida soddaroq ko'rinadi, ammo keyin edge case'lar, xavfsizlik yamoqlari va hujjat yuki jamoa yelkasiga tushadi. Natijada muhandislar mahsulot o'rniga infratuzilma qo'llab-quvvatlashga vaqt sarflaydi. Anti-pattern xususan "framework yozishni yaxshi ko'radigan" jamoalarda kuchli.

**Spring'da qayerda uchraydi:** Resilience4j (`spring-cloud-starter-circuitbreaker-resilience4j`) o'rniga o'z circuit breaker'ini yozish; Spring Retry'ning `@Retryable`/`@Recover` mexanizmi bor joyda qo'lda retry tsikli qurish; `RestClient` (Spring Framework 6.1+), `WebClient` yoki `@HttpExchange` bilan interface client o'rniga `HttpURLConnection` ustiga o'z wrapper'ini yozish; Jackson o'rniga o'z JSON parser'i; Spring Security o'rniga o'z filter'ida JWT'ni qo'lda tekshirish; Flyway/Liquibase o'rniga o'z migratsiya skript yuritgichi; `@Scheduled` yoki Quartz o'rniga o'z thread pool scheduler'i; `CacheManager` abstraksiyasi o'rniga global `ConcurrentHashMap`. Bu komponentlarning har biri Spring Boot starter'lari orqali bir qatorlik bog'liqlik bilan keladi.

```java
@Retryable(retryFor = IOException.class, maxAttempts = 3,
           backoff = @Backoff(delay = 200, multiplier = 2))
public Rate fetch(String code) {
    return restClient.get().uri("/rates/{c}", code).retrieve().body(Rate.class);
}
```

**Qo'llanish keyslari:**
- Qo'lda yozilgan JWT tekshiruvi `exp` va `aud` da'volarini e'tiborsiz qoldiradi va xavfsizlik auditida kritik zaiflik sifatida topiladi.
- O'z yozilgan connection pool'i yuk ostida leak qiladi, HikariCP esa yillar davomida sinovdan o'tgan.
- Maxsus migratsiya mexanizmi parallel deploy'da bir xil skriptni ikki marta ishga tushiradi.
- O'z retry kodida jitter yo'qligi uchun barcha instance'lar bir vaqtda qayta urinib, downstream xizmatni yiqitadi.
- Ichki "mini-ORM" lazy loading va transaction semantikasini noto'g'ri bajarib, ma'lumot buzilishiga olib keladi.

**Ehtiyot bo'ling:** Teskari holat ham bor - har bir mayda ish uchun yangi bog'liqlik qo'shish supply chain riskini va `spring-boot-dependencies` BOM bilan versiya ziddiyatlarini keltiradi, shuning uchun kutubxona tanlashda qo'llab-quvvatlanish darajasi va litsenziyani baholang. O'z yechimini yozishni faqat haqiqatan differensiator bo'lgan domen logikasi uchun qoldiring.

## 25.81 Mo'ri tizim (Stovepipe System)

**Tavsif:** Tashkilotda har bir jamoa o'z vertikal, izolyatsiyalangan tizimini quradi - o'z autentifikatsiyasi, o'z log formati, o'z deploy quvuri va o'z ma'lumot modeli bilan. Tizimlar o'zaro integratsiya uchun loyihalanmagan, shuning uchun har bir bog'lanish nuqtasi nozik nuqta-nuqta adapter sifatida yozib chiqiladi. Oqibatda bir xil muammo tashkilotda o'n marta hal qilinadi, bilim esa jamoalar o'rtasida almashmaydi. Bu arxitektura emas, balki tashkiliy chegaralarning kodga ko'chgan aksidir.

**Spring'da qayerda uchraydi:** Har bir mikroservis `spring-boot-starter-parent` yoki umumiy BOM'dan foydalanmasdan o'z Spring Boot versiyasini tanlashi (bir xil tashkilotda 2.7, 3.2 va 4.0 birga yashashi), har biri o'z `SecurityFilterChain` va JWT validatsiya kodini nusxalashi, har biri o'z `@ControllerAdvice` exception formatini o'ylab topishi (`ProblemDetail` standarti o'rniga), log va metrik nomlari Micrometer konvensiyalariga mos kelmasligi tufayli umumiy dashboard qurib bo'lmasligi. Davosi - tashkilot darajasida umumiy `@AutoConfiguration` starter va BOM, Spring Boot Actuator/Micrometer uchun yagona konvensiya, hamda Spring Modulith bilan modul chegaralarini hujjatlashtirish.

**Qo'llanish keyslari:**
- Bir xil mijoz ma'lumoti to'rt xizmatda to'rt xil sxemada saqlanadi va hisobotlar bir-biriga mos kelmaydi.
- CVE chiqqanda jamoalar 12 ta repozitoriyda qo'lda versiya yangilashga majbur bo'ladi, chunki umumiy BOM yo'q.
- Har bir xizmat o'z correlation ID header nomini ishlatgani uchun distributed tracing uzilib qoladi.
- Yangi muhandis boshqa jamoaga o'tganda deyarli hech qanday bilimini ko'chira olmaydi.
- Umumiy mijoz autentifikatsiyasi har bir tizimda alohida amalga oshirilgani uchun parol siyosatini markazlashtirish imkonsiz bo'ladi.

**Ehtiyot bo'ling:** Standartlashtirishni haddan oshirish teskari xatoga - barcha jamoalarni bitta og'ir ichki platformaga majburlashga olib keladi, bu esa Design by Committee'ni tug'diradi. To'g'ri yo'l: majburiy minimum (xavfsizlik, kuzatuvchanlik, BOM versiyalari) va ixtiyoriy qolgan qism; umumiy starter'ni "taklif" sifatida sotish, majburlash emas.

## 25.82 Katta portlash bilan qayta yozish (Big-Bang Rewrite)

**Tavsif:** Jamoa mavjud legacy tizimni bosqichma-bosqich yangilash o'rniga, uni noldan to'liq qayta yozishga qaror qiladi va yangi tizimni faqat tayyor bo'lgandan keyin ishga tushirishni rejalashtiradi. Amalda yangi tizim eski tizimning yillar davomida to'plangan nozik xatti-harakatlarini takrorlay olmaydi, muddat esa ikki-uch barobar oshadi. Shu vaqt ichida eski tizimga ham o'zgarish kiritish kerak bo'ladi va jamoa ikki kod bazasini parallel ushlaydi. Ko'p loyihalar switchover kunigacha yetib ham kelmaydi.

**Spring'da qayerda uchraydi:** Spring 4/5 + XML konfiguratsiyali WAR monolitni bir yo'la Spring Boot 3.x/4.x mikroservislariga ko'chirish urinishi, bunda `javax.*` → `jakarta.*` ko'chishi, Spring Security'ning yangi lambda DSL'i (`SecurityFilterChain`) va `WebMvcConfigurer` o'zgarishlari bir vaqtda hal qilinishi kerak bo'ladi. Bosqichma-bosqich yondashuv ancha ishonchli: Strangler Fig naqshi bilan Spring Cloud Gateway yoki Nginx orqali trafikni modul-modul yangi xizmatga yo'naltirish, `@ConditionalOnProperty` va feature flag bilan ikki implementatsiyani parallel ushlash, migratsiyani OpenRewrite'ning `rewrite-spring` reseptlari va `spring-boot-properties-migrator` bilan avtomatlashtirish, avval modulli monolitga (Spring Modulith) o'tib keyin ajratish.

**Qo'llanish keyslari:**
- 18 oylik qayta yozish loyihasi bekor qilinadi, chunki eski tizimga kiritilgan yangi talablar yangi tizimga hech qachon yetib bormaydi.
- Yangi tizim ishga tushganda eski tizimning hisob-kitob chetga chiqishlari (rounding, legacy status kodlari) takrorlanmagani aniqlanadi va moliyaviy nomuvofiqlik yuzaga keladi.
- `javax` → `jakarta` ko'chishi uchinchi tomon kutubxonalari yangilanmagani sababli yarim yo'lda to'xtaydi.
- Switchover tunida rollback rejasi yo'qligi aniqlanadi, chunki ma'lumotlar sxemasi mos kelmaydi.
- Bir vaqtda ham texnologiya, ham domen modeli o'zgartirilgani uchun xatolik manbaini aniqlash imkonsiz bo'ladi.

**Ehtiyot bo'ling:** Ba'zi hollarda qayta yozish haqiqatan yagona yo'l (texnologiya qo'llab-quvvatlanishdan chiqqan, xavfsizlik yamog'i mavjud emas) - bunda ham modul-modul migratsiya va parallel run (shadow traffic) bilan natijalarni taqqoslash majburiy. Bir migratsiyada ikki o'zgarishni (framework yangilash + arxitektura o'zgartirish) birlashtirmang.

## 25.83 Rejalashtirishdan o'lim (Death by Planning)

**Tavsif:** Loyiha shunchalik batafsil va uzoq rejalashtiriladiki, rejaning o'zi mahsulotga aylanadi va haqiqiy kod yozishga vaqt qolmaydi. Jamoa diagrammalar, jadvallar, estimatelar va hujjatlar ishlab chiqaradi, ularning har biri birinchi real feedback'dan keyin eskiradi. Belgisi - sprint'larning ko'p qismi "tahlil" va "dizayn" vazifalaridan iborat bo'lishi, demo esa hech qachon ishlaydigan tizimni ko'rsatmasligi. Bu Analysis Paralysis'dan farq qiladi: bu yerda qaror qabul qilinadi, lekin u qog'ozda qoladi.

**Spring'da qayerda uchraydi:** 80 betlik texnik spetsifikatsiya va to'liq UML modeli tayyorlanadi, lekin `start.spring.io` orqali bir soatda yig'iladigan skeleton (`spring-boot-starter-web`, `spring-boot-starter-data-jpa`, Testcontainers) hech qachon yaratilmaydi. Spring Boot ekosistemasi aynan tez feedback uchun qurilgan: `spring-boot-devtools` bilan hot restart, `@SpringBootTest` va `@ServiceConnection`li Testcontainers bilan real ma'lumotlar bazasiga qarshi integratsiya testlari, `@DataJpaTest`/`@WebMvcTest` bilan qatlam testlari, Actuator'ning `/actuator/health` va Micrometer metrikalari bilan birinchi kundan kuzatuvchanlik. Rejadan oldin yupqa vertikal kesim (walking skeleton) chiqarish - bitta endpoint'dan ma'lumotlar bazasigacha - rejalashtirishdagi noto'g'ri taxminlarni darhol ochib beradi.

**Qo'llanish keyslari:**
- Uch oylik dizayn fazasidan keyin birinchi integratsiya urinishida tashqi API talab qilingan ma'lumotni bermasligi aniqlanadi.
- Gantt jadvalida 200 ta vazifa bor, lekin birinchi deployable artefakt beshinchi oyda paydo bo'ladi.
- Performance talablari hujjatda aniq yozilgan, ammo hech qanday o'lchov o'tkazilmagani uchun ular erishib bo'lmas ekani keyin bilinadi.
- Jamoa barcha entity'lar uchun to'liq ER-diagramma tuzadi, keyin birinchi real use case uni butunlay o'zgartiradi.
- Migratsiya rejasi batafsil yozilgan, ammo bitta jadvalni ham sinov muhitida ko'chirib ko'rilmagan.

**Ehtiyot bo'ling:** Buning aksi - rejasiz "shunchaki kod yozish" ham xavfli, ayniqsa qaytarib bo'lmaydigan qarorlar (ma'lumot modeli, public kontrakt, muvofiqlik talablari) uchun. Rejani qisqa va yangilanadigan ushlang (ADR + yupqa roadmap), har bir rejalashtirish fazasini ishlaydigan artefakt bilan tasdiqlang - hujjat kodni almashtirmaydi, faqat uning yo'nalishini belgilaydi.

## 25.84 Amalda qo'llash

- [ ] Bu bo'limdagi anti-patternlar ro'yxatini loyiha ustidan bir marta o'tkazib, topilgan har birini fayl va qator bilan yozib qo'ying.
- [ ] Topilgan anti-patternlarni ikki guruhga ajratib belgilang: hozir tuzatiladigan va ADR bilan qabul qilinadigan.
- [ ] Eng ko'p o'zgaradigan 5 faylni git tarixidan topib, ular ichida qaysi anti-pattern borligini tekshiring.
- [ ] Anemik domen modeli va God Object nomzodlarini sinf hajmi va metod soni bo'yicha o'lchab ro'yxat qiling.
- [ ] Aniqlangan anti-patternlarning har biri uchun avtomatik tekshiruv yozish mumkinmi degan savolga javob bering (ArchUnit yoki Sonar qoidasi).
- [ ] `catch (Exception e) {}` ko'rinishidagi yutilgan istisnolarni qidirib, hammasini ro'yxat qiling.
- [ ] Open Session in View, Shared Database va Distributed Monolith holatlarini alohida tekshirib, natijani hujjatlashtiring.
- [ ] Anti-pattern qarzini kamaytirish rejasini yozing: har chorakda qaysi biri yopiladi va buni qanday o'lchaysiz.

## Manbalar

- [Spring Framework, Declarative transaction annotations](https://docs.spring.io/spring-framework/reference/data-access/transaction/declarative/annotations.html) - 6.0 dan beri `protected` va package-visible metodlar class-based proxy da tranzaksion bo'ladi; interface proxy da metod `public` va proxy qilinayotgan interface da bo'lishi shart
- [Spring Framework, Proxying mechanisms](https://docs.spring.io/spring-framework/reference/core/aop/proxying.html) - CGLIB `final` va `private` metodni advise qila olmaydi
- [Spring Framework v6.2.0, Spring projects in Kotlin: Final by Default](https://github.com/spring-projects/spring-framework/blob/v6.2.0/framework-docs/modules/ROOT/pages/languages/kotlin/spring-projects-in.adoc#final-by-default) - Kotlin sinf va metodlari standart `final`, yechim `kotlin-spring` (allopen) plugini
- [sonar-java, S2230](https://raw.githubusercontent.com/SonarSource/sonar-java/8.44.0.48651/sonar-java-plugin/src/main/resources/org/sonar/l10n/java/rules/java/S2230.html) - qoida 5.x gacha har qanday public bo'lmagan metodni, 6.x da faqat `private` ni belgilaydi

---

[&larr; 24. Zamonaviy Java va funksional patternlar](24-zamonaviy-java-va-funksional-patternlar.md) · [Mundarija](README.md) · [26. Dizayn printsiplari: SOLID, GRASP va umumiy qoidalar &rarr;](26-dizayn-printsiplari-solid-grasp-va-umumiy.md)
