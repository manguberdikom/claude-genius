# Kod yozadigan arxitektorning miyyasi: Java, Spring, PostgreSQL

Bu hujjat kod yozadigan arxitektorning bilimi va fikrlash tarzini yig'adi.
Tayanch stek: Java, Spring va PostgreSQL. Har bob ikki narsani beradi: ichkarida nima
sodir bo'lishining mexanikasi, va shu bilimdan qanday qaror chiqarish.

Hujjat beshlikning bir qismi. Dizayn patternlar katalogi `java-spring-design-patterns.md`
faylida, testlashning butun sohasi `java-spring-testing-handbook.md` faylida, statik
tahlil `java-spring-sonarqube.md` faylida, kod review esa `java-spring-code-review.md`
faylida. Bu yerda
ular takrorlanmaydi, kerak bo'lganda mavzu nomi bilan havola qilinadi.

## Mundarija


**[I. Fikrlash va qarorlar](#i-fikrlash-va-qarorlar)**

- [1. Arxitektorning fikrlash modeli (The Architect's Mental Model)](#1-arxitektorning-fikrlash-modeli-the-architects-mental-model)
  - [1.1 Arxitektor va senior developer o'rtasidagi haqiqiy farq](#11-arxitektor-va-senior-developer-ortasidagi-haqiqiy-farq)
  - [1.2 Kontekst birinchi: biznes maqsadi, jamoa kattaligi, muddat, byudjet](#12-kontekst-birinchi-biznes-maqsadi-jamoa-kattaligi-muddat-byudjet)
  - [1.3 Trade-off tili: bepul qaror yo'q, har birining narxi bor](#13-trade-off-tili-bepul-qaror-yoq-har-birining-narxi-bor)
  - [1.4 Sifat atributlari va ularni o'lchash](#14-sifat-atributlari-va-ularni-olchash)
  - [1.5 Qaytarib bo'ladigan va qaytarib bo'lmaydigan qarorlar](#15-qaytarib-boladigan-va-qaytarib-bolmaydigan-qarorlar)
  - [1.6 "Yetarlicha yaxshi" arxitektura, over-engineering va YAGNI chegarasi](#16-yetarlicha-yaxshi-arxitektura-over-engineering-va-yagni-chegarasi)
  - [1.7 Hozirgi talab va kelajak taxmini orasidagi muvozanat](#17-hozirgi-talab-va-kelajak-taxmini-orasidagi-muvozanat)
  - [1.8 Arxitektura qarori qanday eskiradi va uni qachon qayta ko'rish kerak](#18-arxitektura-qarori-qanday-eskiradi-va-uni-qachon-qayta-korish-kerak)
  - [1.9 Kod yozmaydigan arxitektor nega haqiqatdan uzoqlashadi](#19-kod-yozmaydigan-arxitektor-nega-haqiqatdan-uzoqlashadi)
  - [1.10 O'z fikrlashini tekshirish uchun savollar ro'yxati](#110-oz-fikrlashini-tekshirish-uchun-savollar-royxati)
  - [1.11 Amalda qo'llash](#111-amalda-qollash)
- [2. Muammoni tushunish va to'g'ri savol berish (Understanding the Problem)](#2-muammoni-tushunish-va-togri-savol-berish-understanding-the-problem)
  - [2.1 Talab ortidagi haqiqiy ehtiyojni topish](#21-talab-ortidagi-haqiqiy-ehtiyojni-topish)
  - [2.2 Funksional va nofunksional talablarni ajratish](#22-funksional-va-nofunksional-talablarni-ajratish)
  - [2.3 Noaniq talabni o'lchanadigan talabga aylantirish](#23-noaniq-talabni-olchanadigan-talabga-aylantirish)
  - [2.4 Domenni o'rganish: umumiy til va event storming](#24-domenni-organish-umumiy-til-va-event-storming)
  - [2.5 Chegaraviy holatlar va istisnolarni oldindan topish](#25-chegaraviy-holatlar-va-istisnolarni-oldindan-topish)
  - [2.6 Hajm va o'sish taxmini](#26-hajm-va-osish-taxmini)
  - [2.7 Kim foydalanadi: tashqi foydalanuvchi, ichki jamoa, boshqa servis](#27-kim-foydalanadi-tashqi-foydalanuvchi-ichki-jamoa-boshqa-servis)
  - [2.8 Muvaffaqiyat mezoni va uni qanday o'lchash](#28-muvaffaqiyat-mezoni-va-uni-qanday-olchash)
  - [2.9 Noto'g'ri tushunishning narxi](#29-notogri-tushunishning-narxi)
  - [2.10 Talabni rad etish va qamrovni qisqartirish san'ati](#210-talabni-rad-etish-va-qamrovni-qisqartirish-sanati)
  - [2.11 Amalda qo'llash](#211-amalda-qollash)
- [3. Qaror qabul qilish va uni hujjatlashtirish (Decisions and ADRs)](#3-qaror-qabul-qilish-va-uni-hujjatlashtirish-decisions-and-adrs)
  - [3.1 ADR (Architecture Decision Record) tuzilishi: kontekst, qaror, oqibat, holat](#31-adr-architecture-decision-record-tuzilishi-kontekst-qaror-oqibat-holat)
  - [3.2 Variantlarni taqqoslash: mezon jadvali va og'irlik berish](#32-variantlarni-taqqoslash-mezon-jadvali-va-ogirlik-berish)
  - [3.3 Oxirgi mas'ul daqiqa (last responsible moment) tamoyili](#33-oxirgi-masul-daqiqa-last-responsible-moment-tamoyili)
  - [3.4 Taxminlarni yozib qo'yish va keyin ularni tekshirish](#34-taxminlarni-yozib-qoyish-va-keyin-ularni-tekshirish)
  - [3.5 Spike va prototip: qarorni ma'lumot bilan quvvatlash](#35-spike-va-prototip-qarorni-malumot-bilan-quvvatlash)
  - [3.6 Jamoadagi kelishmovchilik va "rozi emasman, lekin bajaraman" qoidasi](#36-jamoadagi-kelishmovchilik-va-rozi-emasman-lekin-bajaraman-qoidasi)
  - [3.7 Qaror oqibatini kuzatish: metrika va qayta ko'rish sanasi](#37-qaror-oqibatini-kuzatish-metrika-va-qayta-korish-sanasi)
  - [3.8 ADR ni repoda saqlash, raqamlash va eskirganini belgilash](#38-adr-ni-repoda-saqlash-raqamlash-va-eskirganini-belgilash)
  - [3.9 Yomon ADR belgilari: allaqachon qilingan ishni oqlash uchun yozilgan hujjat](#39-yomon-adr-belgilari-allaqachon-qilingan-ishni-oqlash-uchun-yozilgan-hujjat)
  - [3.10 To'liq misol: PostgreSQL da qolish yoki alohida qidiruv tizimi qo'shish qarori](#310-toliq-misol-postgresql-da-qolish-yoki-alohida-qidiruv-tizimi-qoshish-qarori)
  - [3.11 Amalda qo'llash](#311-amalda-qollash)
- [4. Kod - muloqot vositasi: nomlash, aniqlik, kognitiv yuk (Code as Communication)](#4-kod---muloqot-vositasi-nomlash-aniqlik-kognitiv-yuk-code-as-communication)
  - [4.1 Kod yozishdan ko'ra o'qishga ko'p vaqt ketadi](#41-kod-yozishdan-kora-oqishga-kop-vaqt-ketadi)
  - [4.2 Nomlash: domen tilidan nom olish](#42-nomlash-domen-tilidan-nom-olish)
  - [4.3 Kognitiv yuk: bir metodni tushunish uchun nechta narsa](#43-kognitiv-yuk-bir-metodni-tushunish-uchun-nechta-narsa)
  - [4.4 Metod uzunligi, ichma-ich shartlar va erta qaytish](#44-metod-uzunligi-ichma-ich-shartlar-va-erta-qaytish)
  - [4.5 Izoh qachon kerak: "nima" emas, "nega"](#45-izoh-qachon-kerak-nima-emas-nega)
  - [4.6 Xato va istisnolar orqali muloqot](#46-xato-va-istisnolar-orqali-muloqot)
  - [4.7 Tur tizimidan foydalanish](#47-tur-tizimidan-foydalanish)
  - [4.8 Paket tuzilishi: xususiyat bo'yicha bo'lish](#48-paket-tuzilishi-xususiyat-boyicha-bolish)
  - [4.9 Kodda yashirin bilim](#49-kodda-yashirin-bilim)
  - [4.10 O'zini hujjatlaydigan API](#410-ozini-hujjatlaydigan-api)
  - [4.11 Amalda qo'llash](#411-amalda-qollash)
- [5. Abstraksiya hissi, bog'liqlik va chegaralar (Abstraction, Coupling and Boundaries)](#5-abstraksiya-hissi-bogliqlik-va-chegaralar-abstraction-coupling-and-boundaries)
  - [5.1 Abstraksiya nima uchun qo'yiladi: o'zgarishni bitta joyga to'plash](#51-abstraksiya-nima-uchun-qoyiladi-ozgarishni-bitta-joyga-toplash)
  - [5.2 Erta abstraksiya va takrorlanish: qaysi biri arzonroq](#52-erta-abstraksiya-va-takrorlanish-qaysi-biri-arzonroq)
  - [5.3 Noto'g'ri abstraksiya narxi va undan qaytish yo'li](#53-notogri-abstraksiya-narxi-va-undan-qaytish-yoli)
  - [5.4 Bog'liqlik turlari: ma'lumot, vaqt, joylashuv, sxema bo'yicha bog'liqlik](#54-bogliqlik-turlari-malumot-vaqt-joylashuv-sxema-boyicha-bogliqlik)
  - [5.5 Kohéziya: nima birga o'zgarsa, birga tursin](#55-kohéziya-nima-birga-ozgarsa-birga-tursin)
  - [5.6 Modul chegarasini qayerdan o'tkazish: o'zgarish tezligi va egalik bo'yicha](#56-modul-chegarasini-qayerdan-otkazish-ozgarish-tezligi-va-egalik-boyicha)
  - [5.7 Interfeys kimga tegishli: foydalanuvchi tomonda e'lon qilish](#57-interfeys-kimga-tegishli-foydalanuvchi-tomonda-elon-qilish)
  - [5.8 Bog'liqlik yo'nalishini boshqarish: ichki qatlam tashqarini bilmasin](#58-bogliqlik-yonalishini-boshqarish-ichki-qatlam-tashqarini-bilmasin)
  - [5.9 Sxema chegarasi: boshqa servisning jadvaliga tegmaslik qoidasi](#59-sxema-chegarasi-boshqa-servisning-jadvaliga-tegmaslik-qoidasi)
  - [5.10 Chegara noto'g'ri qo'yilganini bildiradigan belgilar](#510-chegara-notogri-qoyilganini-bildiradigan-belgilar)
  - [5.11 Amalda qo'llash](#511-amalda-qollash)
- [6. Murakkablikni boshqarish (Managing Complexity)](#6-murakkablikni-boshqarish-managing-complexity)
  - [6.1 Muhim murakkablik va tasodifiy murakkablik farqi](#61-muhim-murakkablik-va-tasodifiy-murakkablik-farqi)
  - [6.2 Murakkablik qayerda to'planadi: shart, holat, integratsiya nuqtalari](#62-murakkablik-qayerda-toplanadi-shart-holat-integratsiya-nuqtalari)
  - [6.3 Holat (state) ni kamaytirish: immutable obyekt va sof funksiya](#63-holat-state-ni-kamaytirish-immutable-obyekt-va-sof-funksiya)
  - [6.4 Konfiguratsiya murakkabligi: har bir flag kelajakdagi xato](#64-konfiguratsiya-murakkabligi-har-bir-flag-kelajakdagi-xato)
  - [6.5 Kodni o'chirish: eng kam baholangan arxitektura ishi](#65-kodni-ochirish-eng-kam-baholangan-arxitektura-ishi)
  - [6.6 Texnik qarz: ongli qarz va tasodifiy loyqalik](#66-texnik-qarz-ongli-qarz-va-tasodifiy-loyqalik)
  - [6.7 Murakkablikni o'lchash: o'zgarish vaqti, incident soni, yangi odam vaqti](#67-murakkablikni-olchash-ozgarish-vaqti-incident-soni-yangi-odam-vaqti)
  - [6.8 Servislar soni va operatsion murakkablik narxi](#68-servislar-soni-va-operatsion-murakkablik-narxi)
  - [6.9 Umumiylashtirish tuzog'i: uchta foydalanuvchiga mo'ljallangan platforma](#69-umumiylashtirish-tuzogi-uchta-foydalanuvchiga-moljallangan-platforma)
  - [6.10 Murakkablikni jamoaga tushuntirish va qarorni himoya qilish](#610-murakkablikni-jamoaga-tushuntirish-va-qarorni-himoya-qilish)
  - [6.11 Amalda qo'llash](#611-amalda-qollash)
- [7. Nosozlik haqida fikrlash (Thinking About Failure)](#7-nosozlik-haqida-fikrlash-thinking-about-failure)
  - [7.1 Hamma narsa buziladi: tarmoq, disk, protsess, boshqa servis](#71-hamma-narsa-buziladi-tarmoq-disk-protsess-boshqa-servis)
  - [7.2 Nosozlik turlari: to'liq to'xtash, sekinlashuv, qisman javob, yolg'on javob](#72-nosozlik-turlari-toliq-toxtash-sekinlashuv-qisman-javob-yolgon-javob)
  - [7.3 Sekin servis o'lgan servisdan xavfliroq: navbat to'lishi va orqaga bosim](#73-sekin-servis-olgan-servisdan-xavfliroq-navbat-tolishi-va-orqaga-bosim)
  - [7.4 Qayta urinish qachon zarar keltiradi: retry bo'roni va retry byudjeti](#74-qayta-urinish-qachon-zarar-keltiradi-retry-boroni-va-retry-byudjeti)
  - [7.5 Idempotentlik: bir xil so'rovni ikki marta bajarish xavfsiz bo'lsin](#75-idempotentlik-bir-xil-sorovni-ikki-marta-bajarish-xavfsiz-bolsin)
  - [7.6 Qisman nosozlikda nima qilish: degradatsiya rejasi va zaxira javob](#76-qisman-nosozlikda-nima-qilish-degradatsiya-rejasi-va-zaxira-javob)
  - [7.7 Ma'lumot yo'qolishi va buzilishi: qaysi biri ko'proq qo'rqinchli](#77-malumot-yoqolishi-va-buzilishi-qaysi-biri-koproq-qorqinchli)
  - [7.8 Nosozlik ta'sirini cheklash: bulkhead va alohida resurs hovuzlari](#78-nosozlik-tasirini-cheklash-bulkhead-va-alohida-resurs-hovuzlari)
  - [7.9 Tiklanish vaqti: RTO va RPO raqamlarini kelishib olish](#79-tiklanish-vaqti-rto-va-rpo-raqamlarini-kelishib-olish)
  - [7.10 Nosozlik ssenariylarini oldindan yozish: "nima bo'lsa, nima qilamiz" jadvali](#710-nosozlik-ssenariylarini-oldindan-yozish-nima-bolsa-nima-qilamiz-jadvali)
  - [7.11 Amalda qo'llash](#711-amalda-qollash)
- [8. Ishlash va resurs hissi: napkin math (Performance Intuition and Napkin Math)](#8-ishlash-va-resurs-hissi-napkin-math-performance-intuition-and-napkin-math)
  - [8.1 Har bir arxitektor yodda tutishi kerak bo'lgan kechikish raqamlari](#81-har-bir-arxitektor-yodda-tutishi-kerak-bolgan-kechikish-raqamlari)
  - [8.2 Oddiy hisob: kuniga N so'rov nechta RPS bo'ladi, cho'qqi koeffitsienti](#82-oddiy-hisob-kuniga-n-sorov-nechta-rps-boladi-choqqi-koeffitsienti)
  - [8.3 Little qonuni: parallellik, kechikish va throughput bog'liqligi](#83-little-qonuni-parallellik-kechikish-va-throughput-bogliqligi)
  - [8.4 Thread pool va connection pool kattaligini hisoblash](#84-thread-pool-va-connection-pool-kattaligini-hisoblash)
  - [8.5 Ma'lumot hajmini hisoblash: qator kattaligi, indeks hajmi, bir yillik o'sish](#85-malumot-hajmini-hisoblash-qator-kattaligi-indeks-hajmi-bir-yillik-osish)
  - [8.6 O'rtacha emas, p95 va p99 ga qarash sababi](#86-ortacha-emas-p95-va-p99-ga-qarash-sababi)
  - [8.7 Tarmoq safari soni: bitta so'rovda nechta tashqi chaqiruv bor](#87-tarmoq-safari-soni-bitta-sorovda-nechta-tashqi-chaqiruv-bor)
  - [8.8 Serializatsiya, JSON va ortiqcha ma'lumot tashishning narxi](#88-serializatsiya-json-va-ortiqcha-malumot-tashishning-narxi)
  - [8.9 Qachon kesh kerak emas: ma'lumotlar bazasi allaqachon yetarli](#89-qachon-kesh-kerak-emas-malumotlar-bazasi-allaqachon-yetarli)
  - [8.10 O'lchovsiz optimallashtirish: taxmin qilib emas, o'lchab tuzatish](#810-olchovsiz-optimallashtirish-taxmin-qilib-emas-olchab-tuzatish)
  - [8.11 Amalda qo'llash](#811-amalda-qollash)

**[II. Java chuqur bilim](#ii-java-chuqur-bilim)**

- [9. JVM ichki tuzilishi: class loading, memory model, JIT (JVM Internals)](#9-jvm-ichki-tuzilishi-class-loading-memory-model-jit-jvm-internals)
  - [9.1 JVM xotira hududlari: heap, metaspace, stack, code cache, direct buffer](#91-jvm-xotira-hududlari-heap-metaspace-stack-code-cache-direct-buffer)
  - [9.2 Class loading bosqichlari va class loader ierarxiyasi](#92-class-loading-bosqichlari-va-class-loader-ierarxiyasi)
  - [9.3 Spring Boot fat jar va uning class loading ga ta'siri](#93-spring-boot-fat-jar-va-uning-class-loading-ga-tasiri)
  - [9.4 Bytecode va interpretatsiya: ishga tushish paytidagi sekinlik](#94-bytecode-va-interpretatsiya-ishga-tushish-paytidagi-sekinlik)
  - [9.5 JIT: C1, C2, profil yig'ish, tiered compilation](#95-jit-c1-c2-profil-yigish-tiered-compilation)
  - [9.6 Inlining, escape analysis va boshqa optimizatsiyalar](#96-inlining-escape-analysis-va-boshqa-optimizatsiyalar)
  - [9.7 Deoptimizatsiya: nega kod birdan sekinlashadi](#97-deoptimizatsiya-nega-kod-birdan-sekinlashadi)
  - [9.8 Isinish (warmup) muammosi va u deployment ga qanday ta'sir qiladi](#98-isinish-warmup-muammosi-va-u-deployment-ga-qanday-tasir-qiladi)
  - [9.9 Java memory model: happens-before, volatile, final maydon kafolatlari](#99-java-memory-model-happens-before-volatile-final-maydon-kafolatlari)
  - [9.10 JVM ni kuzatish uchun asosiy flaglar va `-XX:+PrintFlagsFinal` dan foydalanish](#910-jvm-ni-kuzatish-uchun-asosiy-flaglar-va--xxprintflagsfinal-dan-foydalanish)
  - [9.11 AOT, CDS va GraalVM native image: qachon mantiqli](#911-aot-cds-va-graalvm-native-image-qachon-mantiqli)
  - [9.12 Amalda qo'llash](#912-amalda-qollash)
- [10. Garbage collection va xotira sozlash (Garbage Collection and Memory Tuning)](#10-garbage-collection-va-xotira-sozlash-garbage-collection-and-memory-tuning)
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
- [11. Concurrency: thread, lock, atomic, happens-before (Java Concurrency)](#11-concurrency-thread-lock-atomic-happens-before-java-concurrency)
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
  - [11.12 Amalda qo'llash](#1112-amalda-qollash)
- [12. Virtual threads, structured concurrency va scoped values (Modern Concurrency)](#12-virtual-threads-structured-concurrency-va-scoped-values-modern-concurrency)
  - [12.1 Virtual thread nima: carrier thread, mount va unmount mexanikasi](#121-virtual-thread-nima-carrier-thread-mount-va-unmount-mexanikasi)
  - [12.2 Platform thread bilan taqqoslash: xotira, soni, yaratish narxi](#122-platform-thread-bilan-taqqoslash-xotira-soni-yaratish-narxi)
  - [12.3 Qaysi yuk uchun foyda beradi va qaysi uchun bermaydi](#123-qaysi-yuk-uchun-foyda-beradi-va-qaysi-uchun-bermaydi)
  - [12.4 Pinning muammosi va undan qochish](#124-pinning-muammosi-va-undan-qochish)
  - [12.5 Spring Boot da virtual thread ni yoqish](#125-spring-boot-da-virtual-thread-ni-yoqish)
  - [12.6 Connection pool virtual thread bilan: nega pool hali ham chegara](#126-connection-pool-virtual-thread-bilan-nega-pool-hali-ham-chegara)
  - [12.7 Structured concurrency: vazifalar daraxti, bekor qilish va xato tarqalishi](#127-structured-concurrency-vazifalar-daraxti-bekor-qilish-va-xato-tarqalishi)
  - [12.8 Scoped values va `ThreadLocal` o'rniga ishlatish](#128-scoped-values-va-threadlocal-orniga-ishlatish)
  - [12.9 Kuzatuvchanlik: thread dump va metrikalar o'zgarishi](#129-kuzatuvchanlik-thread-dump-va-metrikalar-ozgarishi)
  - [12.10 Reactive dasturlashga nisbatan tanlov: qachon qaysi biri](#1210-reactive-dasturlashga-nisbatan-tanlov-qachon-qaysi-biri)
  - [12.11 Amalda qo'llash](#1211-amalda-qollash)
- [13. Zamonaviy Java tili va API dizayni (Modern Java and API Design)](#13-zamonaviy-java-tili-va-api-dizayni-modern-java-and-api-design)
  - [13.1 Record: qachon ishlatish, qachon oddiy sinf kerak](#131-record-qachon-ishlatish-qachon-oddiy-sinf-kerak)
  - [13.2 Sealed interface va pattern matching bilan to'liq qamrovli tanlov](#132-sealed-interface-va-pattern-matching-bilan-toliq-qamrovli-tanlov)
  - [13.3 `switch` ifodasi va deconstruction pattern](#133-switch-ifodasi-va-deconstruction-pattern)
  - [13.4 Text block, `var` va o'qilishi: foyda va chegara](#134-text-block-var-va-oqilishi-foyda-va-chegara)
  - [13.5 Optional ni to'g'ri ishlatish: qaytish qiymati, maydon emas](#135-optional-ni-togri-ishlatish-qaytish-qiymati-maydon-emas)
  - [13.6 Stream API: qachon foyda, qachon oddiy sikl tushunarliroq](#136-stream-api-qachon-foyda-qachon-oddiy-sikl-tushunarliroq)
  - [13.7 Istisnolar dizayni: tekshiriladigan va tekshirilmaydigan, o'z ierarxiyangiz](#137-istisnolar-dizayni-tekshiriladigan-va-tekshirilmaydigan-oz-ierarxiyangiz)
  - [13.8 Kutubxona API si dizayni: kirish nuqtasi kam, nom aniq, standart qiymat xavfsiz](#138-kutubxona-api-si-dizayni-kirish-nuqtasi-kam-nom-aniq-standart-qiymat-xavfsiz)
  - [13.9 Orqaga moslik: metod qo'shish, nomini o'zgartirish, deprecate qilish siyosati](#139-orqaga-moslik-metod-qoshish-nomini-ozgartirish-deprecate-qilish-siyosati)
  - [13.10 Null xavfsizligi: annotatsiyalar va chegaraviy tekshiruv](#1310-null-xavfsizligi-annotatsiyalar-va-chegaraviy-tekshiruv)
  - [13.11 Java versiyalari: LTS tanlash va yangilanish strategiyasi](#1311-java-versiyalari-lts-tanlash-va-yangilanish-strategiyasi)
  - [13.12 Amalda qo'llash](#1312-amalda-qollash)
- [14. JVM profiling va diagnostika: JFR, async-profiler, heap dump (JVM Profiling and Diagnostics)](#14-jvm-profiling-va-diagnostika-jfr-async-profiler-heap-dump-jvm-profiling-and-diagnostics)
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

**[III. Spring chuqur bilim](#iii-spring-chuqur-bilim)**

- [15. Spring Core mexanikasi: IoC konteyner, bean lifecycle, AOP proxy (Spring Core Mechanics)](#15-spring-core-mexanikasi-ioc-konteyner-bean-lifecycle-aop-proxy-spring-core-mechanics)
  - [15.1 `ApplicationContext` ishga tushish bosqichlari: bean definition, post-processor, instantiation](#151-applicationcontext-ishga-tushish-bosqichlari-bean-definition-post-processor-instantiation)
  - [15.2 `BeanFactoryPostProcessor` va `BeanPostProcessor` farqi va ularning tartibi](#152-beanfactorypostprocessor-va-beanpostprocessor-farqi-va-ularning-tartibi)
  - [15.3 Bean lifecycle: konstruktor, inject, `@PostConstruct`, `@PreDestroy`](#153-bean-lifecycle-konstruktor-inject-postconstruct-predestroy)
  - [15.4 Scope lar: singleton, prototype, request va ularning amaliy oqibati](#154-scope-lar-singleton-prototype-request-va-ularning-amaliy-oqibati)
  - [15.5 Bog'liqlikni kiritish usullari va nega konstruktor orqali kiritish afzal](#155-bogliqlikni-kiritish-usullari-va-nega-konstruktor-orqali-kiritish-afzal)
  - [15.6 Aylanma bog'liqlik: nega paydo bo'ladi, Spring Boot 3 da nega xato beradi](#156-aylanma-bogliqlik-nega-paydo-boladi-spring-boot-3-da-nega-xato-beradi)
  - [15.7 `@Lazy`, `@Primary`, `@Qualifier`, `@Conditional` qachon kerak](#157-lazy-primary-qualifier-conditional-qachon-kerak)
  - [15.8 AOP mexanikasi: JDK dinamik proxy va CGLIB farqi](#158-aop-mexanikasi-jdk-dinamik-proxy-va-cglib-farqi)
  - [15.9 Proxy tuzog'i: ichki metod chaqiruvida `@Transactional` va `@Cacheable` ishlamasligi](#159-proxy-tuzogi-ichki-metod-chaqiruvida-transactional-va-cacheable-ishlamasligi)
  - [15.10 `ApplicationEvent` va `@EventListener`: sinxron tabiati va tranzaksiya bilan bog'liqligi](#1510-applicationevent-va-eventlistener-sinxron-tabiati-va-tranzaksiya-bilan-bogliqligi)
  - [15.11 Ishga tushish vaqtini qisqartirish: ortiqcha bean va komponent skanerlash](#1511-ishga-tushish-vaqtini-qisqartirish-ortiqcha-bean-va-komponent-skanerlash)
  - [15.12 Amalda qo'llash](#1512-amalda-qollash)
- [16. Spring Boot mexanikasi: auto-configuration, starter, Actuator (Spring Boot Mechanics)](#16-spring-boot-mexanikasi-auto-configuration-starter-actuator-spring-boot-mechanics)
  - [16.1 Auto-configuration qanday ishlaydi: `AutoConfiguration.imports` va shartli annotatsiyalar](#161-auto-configuration-qanday-ishlaydi-autoconfigurationimports-va-shartli-annotatsiyalar)
  - [16.2 `@ConditionalOnClass`, `@ConditionalOnMissingBean` va tartib (`@AutoConfigureAfter`)](#162-conditionalonclass-conditionalonmissingbean-va-tartib-autoconfigureafter)
  - [16.3 Auto-configuration ni tekshirish: `--debug` va shartlar hisoboti](#163-auto-configuration-ni-tekshirish---debug-va-shartlar-hisoboti)
  - [16.4 Starter yozish: o'z jamoangiz uchun umumiy kutubxona qurish qoidalari](#164-starter-yozish-oz-jamoangiz-uchun-umumiy-kutubxona-qurish-qoidalari)
  - [16.5 Konfiguratsiya manbalari tartibi va ustunlik qoidasi](#165-konfiguratsiya-manbalari-tartibi-va-ustunlik-qoidasi)
  - [16.6 `@ConfigurationProperties` va validatsiya, `application.yaml` tuzilishi](#166-configurationproperties-va-validatsiya-applicationyaml-tuzilishi)
  - [16.7 Profil (profile) dan to'g'ri foydalanish va uning tuzoqlari](#167-profil-profile-dan-togri-foydalanish-va-uning-tuzoqlari)
  - [16.8 Actuator: health, metrics, env, httpexchanges va ularning xavfsizligi](#168-actuator-health-metrics-env-httpexchanges-va-ularning-xavfsizligi)
  - [16.9 Health indicator yozish va readiness va liveness farqi](#169-health-indicator-yozish-va-readiness-va-liveness-farqi)
  - [16.10 Ishga tushish vaqti: lazy initialization, AOT va native image ta'siri](#1610-ishga-tushish-vaqti-lazy-initialization-aot-va-native-image-tasiri)
  - [16.11 Spring Boot 3 ga o'tish: Jakarta nomlari va konfiguratsiya o'zgarishlari](#1611-spring-boot-3-ga-otish-jakarta-nomlari-va-konfiguratsiya-ozgarishlari)
  - [16.12 Amalda qo'llash](#1612-amalda-qollash)
- [17. Spring MVC va WebFlux: so'rov yo'li, thread modeli, REST dizayni (Spring MVC and WebFlux)](#17-spring-mvc-va-webflux-sorov-yoli-thread-modeli-rest-dizayni-spring-mvc-and-webflux)
  - [17.1 So'rovning to'liq yo'li: konteyner, filter, `DispatcherServlet`, handler, converter](#171-sorovning-toliq-yoli-konteyner-filter-dispatcherservlet-handler-converter)
  - [17.2 Thread modeli: har so'rovga bitta thread va uning chegarasi](#172-thread-modeli-har-sorovga-bitta-thread-va-uning-chegarasi)
  - [17.3 Tomcat sozlamalari: `max-threads`, `accept-count`, `connection-timeout` va ularning ma'nosi](#173-tomcat-sozlamalari-max-threads-accept-count-connection-timeout-va-ularning-manosi)
  - [17.4 WebFlux va event loop modeli: qachon haqiqatan foyda beradi](#174-webflux-va-event-loop-modeli-qachon-haqiqatan-foyda-beradi)
  - [17.5 Virtual thread bilan MVC: WebFlux ga ehtiyoj qanday kamayadi](#175-virtual-thread-bilan-mvc-webflux-ga-ehtiyoj-qanday-kamayadi)
  - [17.6 REST dizayni: resurs nomlari, HTTP metodlari, holat kodlari, versiyalash](#176-rest-dizayni-resurs-nomlari-http-metodlari-holat-kodlari-versiyalash)
  - [17.7 So'rov va javob modellari: DTO chegarasi va entity ni tashqariga chiqarmaslik](#177-sorov-va-javob-modellari-dto-chegarasi-va-entity-ni-tashqariga-chiqarmaslik)
  - [17.8 Validatsiya va xato javobi formati (`ProblemDetail`, RFC 7807)](#178-validatsiya-va-xato-javobi-formati-problemdetail-rfc-7807)
  - [17.9 Katta javoblar: sahifalash, oqim (streaming), siqish](#179-katta-javoblar-sahifalash-oqim-streaming-siqish)
  - [17.10 `RestClient` va `WebClient`: timeout, connection pool, qayta urinish sozlamalari](#1710-restclient-va-webclient-timeout-connection-pool-qayta-urinish-sozlamalari)
  - [17.11 Filter va interceptor: qayerda kontekst (trace id, foydalanuvchi) o'rnatiladi](#1711-filter-va-interceptor-qayerda-kontekst-trace-id-foydalanuvchi-ornatiladi)
  - [17.12 Amalda qo'llash](#1712-amalda-qollash)
- [18. Spring Data JPA va Hibernate chuqur (Spring Data JPA and Hibernate)](#18-spring-data-jpa-va-hibernate-chuqur-spring-data-jpa-and-hibernate)
  - [18.1 Persistence context: birinchi daraja kesh, dirty checking, flush tartibi](#181-persistence-context-birinchi-daraja-kesh-dirty-checking-flush-tartibi)
  - [18.2 Entity holatlari: transient, managed, detached, removed va ular orasidagi o'tish](#182-entity-holatlari-transient-managed-detached-removed-va-ular-orasidagi-otish)
  - [18.3 Lazy loading mexanikasi, proxy va `LazyInitializationException` sababi](#183-lazy-loading-mexanikasi-proxy-va-lazyinitializationexception-sababi)
  - [18.4 N+1 so'rov muammosi: topish usuli va to'rt xil yechim](#184-n1-sorov-muammosi-topish-usuli-va-tort-xil-yechim)
  - [18.5 Faqat kerakli ustunni olish: interfeys va record proyeksiyasi](#185-faqat-kerakli-ustunni-olish-interfeys-va-record-proyeksiyasi)
  - [18.6 `@OneToMany` to'plamlar: `List` va `Set` farqi, yangilashdagi tuzoqlar](#186-onetomany-toplamlar-list-va-set-farqi-yangilashdagi-tuzoqlar)
  - [18.7 Identifikator strategiyalari: `IDENTITY`, `SEQUENCE` va batch insert ga ta'siri](#187-identifikator-strategiyalari-identity-sequence-va-batch-insert-ga-tasiri)
  - [18.8 Optimistik va pessimistik lock: `@Version`, `PESSIMISTIC_WRITE` qachon](#188-optimistik-va-pessimistik-lock-version-pessimistic_write-qachon)
  - [18.9 Hibernate statistikasi va yozilgan SQL ni ko'rish sozlamalari](#189-hibernate-statistikasi-va-yozilgan-sql-ni-korish-sozlamalari)
  - [18.10 Spring Data metod nomlari, `@Query`, `Specification` va ularning chegarasi](#1810-spring-data-metod-nomlari-query-specification-va-ularning-chegarasi)
  - [18.11 Qachon JPA dan voz kechib `JdbcClient` yoki to'g'ridan-to'g'ri SQL yozish kerak](#1811-qachon-jpa-dan-voz-kechib-jdbcclient-yoki-togridan-togri-sql-yozish-kerak)
  - [18.12 Ikkinchi daraja kesh: foydasi va xavfi](#1812-ikkinchi-daraja-kesh-foydasi-va-xavfi)
  - [18.13 Amalda qo'llash](#1813-amalda-qollash)
- [19. Spring tranzaksiyalari va ularning chegaralari (Spring Transactions)](#19-spring-tranzaksiyalari-va-ularning-chegaralari-spring-transactions)
  - [19.1 `@Transactional` qanday ishlaydi: proxy, `TransactionInterceptor`, `PlatformTransactionManager`](#191-transactional-qanday-ishlaydi-proxy-transactioninterceptor-platformtransactionmanager)
  - [19.2 Propagation turlari: `REQUIRED`, `REQUIRES_NEW`, `NESTED` va amaliy farqi](#192-propagation-turlari-required-requires_new-nested-va-amaliy-farqi)
  - [19.3 Isolation darajasini Spring da belgilash va PostgreSQL dagi haqiqiy xatti-harakat](#193-isolation-darajasini-spring-da-belgilash-va-postgresql-dagi-haqiqiy-xatti-harakat)
  - [19.4 Rollback qoidasi: nega tekshiriladigan istisnoda rollback bo'lmaydi](#194-rollback-qoidasi-nega-tekshiriladigan-istisnoda-rollback-bolmaydi)
  - [19.5 `readOnly = true` nima beradi va nima bermaydi](#195-readonly--true-nima-beradi-va-nima-bermaydi)
  - [19.6 Ichki metod chaqiruvi tuzog'i va undan chiqish yo'llari](#196-ichki-metod-chaqiruvi-tuzogi-va-undan-chiqish-yollari)
  - [19.7 Tranzaksiya uzunligi: tashqi HTTP chaqiruvni tranzaksiya ichiga qo'ymaslik](#197-tranzaksiya-uzunligi-tashqi-http-chaqiruvni-tranzaksiya-ichiga-qoymaslik)
  - [19.8 `TransactionSynchronization` va `@TransactionalEventListener` bilan commit dan keyin ish](#198-transactionsynchronization-va-transactionaleventlistener-bilan-commit-dan-keyin-ish)
  - [19.9 Tranzaksiya va kesh, tranzaksiya va xabar yuborish nomuvofiqligi](#199-tranzaksiya-va-kesh-tranzaksiya-va-xabar-yuborish-nomuvofiqligi)
  - [19.10 Timeout, lock kutish vaqti va deadlock bilan uchrashish](#1910-timeout-lock-kutish-vaqti-va-deadlock-bilan-uchrashish)
  - [19.11 Dasturiy tranzaksiya: `TransactionTemplate` qachon aniqroq](#1911-dasturiy-tranzaksiya-transactiontemplate-qachon-aniqroq)
  - [19.12 Katta batch operatsiyalarda tranzaksiya chegarasini tanlash](#1912-katta-batch-operatsiyalarda-tranzaksiya-chegarasini-tanlash)
  - [19.13 Amalda qo'llash](#1913-amalda-qollash)
- [20. Spring Security: filter chain, OAuth2, JWT (Spring Security)](#20-spring-security-filter-chain-oauth2-jwt-spring-security)
  - [20.1 `SecurityFilterChain` tuzilishi va filtrlar tartibi](#201-securityfilterchain-tuzilishi-va-filtrlar-tartibi)
  - [20.2 Autentifikatsiya va avtorizatsiya: `Authentication`, `SecurityContext`, `GrantedAuthority`](#202-autentifikatsiya-va-avtorizatsiya-authentication-securitycontext-grantedauthority)
  - [20.3 Spring Security 6 konfiguratsiyasi: lambda uslubi va eski uslubdan farqi](#203-spring-security-6-konfiguratsiyasi-lambda-uslubi-va-eski-uslubdan-farqi)
  - [20.4 Sessiya va token: qachon qaysi biri mantiqli](#204-sessiya-va-token-qachon-qaysi-biri-mantiqli)
  - [20.5 OAuth2 rollari: resource server, client, authorization server](#205-oauth2-rollari-resource-server-client-authorization-server)
  - [20.6 JWT ni tekshirish: imzo, `iss`, `aud`, `exp`, kalit aylanishi (JWKS)](#206-jwt-ni-tekshirish-imzo-iss-aud-exp-kalit-aylanishi-jwks)
  - [20.7 Token muddati, yangilash (refresh) va bekor qilish muammosi](#207-token-muddati-yangilash-refresh-va-bekor-qilish-muammosi)
  - [20.8 Metod darajasidagi xavfsizlik: `@PreAuthorize` va uning proxy chegarasi](#208-metod-darajasidagi-xavfsizlik-preauthorize-va-uning-proxy-chegarasi)
  - [20.9 Ko'p ijarachi (multi-tenant) va qator darajasidagi kirish nazorati](#209-kop-ijarachi-multi-tenant-va-qator-darajasidagi-kirish-nazorati)
  - [20.10 CORS, CSRF va ular qachon kerak](#2010-cors-csrf-va-ular-qachon-kerak)
  - [20.11 Parol saqlash, maxfiy ma'lumot va audit izlari](#2011-parol-saqlash-maxfiy-malumot-va-audit-izlari)
  - [20.12 Keng tarqalgan xatolar: ochiq qolgan endpoint, tekshirilmagan token, ortiqcha huquq](#2012-keng-tarqalgan-xatolar-ochiq-qolgan-endpoint-tekshirilmagan-token-ortiqcha-huquq)
  - [20.13 Amalda qo'llash](#2013-amalda-qollash)

**[IV. PostgreSQL chuqur bilim](#iv-postgresql-chuqur-bilim)**

- [21. PostgreSQL arxitekturasi: process model, WAL, checkpoint, vacuum (PostgreSQL Architecture)](#21-postgresql-arxitekturasi-process-model-wal-checkpoint-vacuum-postgresql-architecture)
  - [21.1 Protsess modeli: postmaster, backend protsess, fon ishchilari](#211-protsess-modeli-postmaster-backend-protsess-fon-ishchilari)
  - [21.2 Har ulanishga bitta protsess: bundan kelib chiqadigan ulanish narxi](#212-har-ulanishga-bitta-protsess-bundan-kelib-chiqadigan-ulanish-narxi)
  - [21.3 Umumiy xotira: `shared_buffers` va operatsion tizim keshi bilan munosabati](#213-umumiy-xotira-shared_buffers-va-operatsion-tizim-keshi-bilan-munosabati)
  - [21.4 Sahifa (page) tuzilishi, tuple va `ctid`](#214-sahifa-page-tuzilishi-tuple-va-ctid)
  - [21.5 WAL: yozuv tartibi, `wal_level`, `synchronous_commit` va ma'lumot xavfsizligi](#215-wal-yozuv-tartibi-wal_level-synchronous_commit-va-malumot-xavfsizligi)
  - [21.6 Checkpoint: qachon boshlanadi, I/O cho'qqisi va `checkpoint_timeout` sozlash](#216-checkpoint-qachon-boshlanadi-io-choqqisi-va-checkpoint_timeout-sozlash)
  - [21.7 Vacuum nima qiladi: o'lik tuple, visibility map, index-only scan bilan bog'liqligi](#217-vacuum-nima-qiladi-olik-tuple-visibility-map-index-only-scan-bilan-bogliqligi)
  - [21.8 Autovacuum sozlamalari va u yetishmay qolganda nima bo'ladi](#218-autovacuum-sozlamalari-va-u-yetishmay-qolganda-nima-boladi)
  - [21.9 Transaction ID o'ralishi (wraparound) va freeze jarayoni](#219-transaction-id-oralishi-wraparound-va-freeze-jarayoni)
  - [21.10 Jadval va indeks shishishi (bloat): o'lchash va tuzatish](#2110-jadval-va-indeks-shishishi-bloat-olchash-va-tuzatish)
  - [21.11 `TOAST`: katta qiymatlar qanday saqlanadi](#2111-toast-katta-qiymatlar-qanday-saqlanadi)
  - [21.12 Amalda qo'llash](#2112-amalda-qollash)
- [22. MVCC, izolyatsiya darajalari, lock va deadlock (MVCC and Isolation)](#22-mvcc-izolyatsiya-darajalari-lock-va-deadlock-mvcc-and-isolation)
  - [22.1 MVCC mexanikasi: `xmin`, `xmax`, snapshot va ko'rinuvchanlik qoidasi](#221-mvcc-mexanikasi-xmin-xmax-snapshot-va-korinuvchanlik-qoidasi)
  - [22.2 PostgreSQL da Read Committed haqiqatda qanday ishlaydi](#222-postgresql-da-read-committed-haqiqatda-qanday-ishlaydi)
  - [22.3 Repeatable Read va serialization xatosi, qayta urinish zarurati](#223-repeatable-read-va-serialization-xatosi-qayta-urinish-zarurati)
  - [22.4 Serializable izolyatsiya: predikat lock va uning narxi](#224-serializable-izolyatsiya-predikat-lock-va-uning-narxi)
  - [22.5 Yo'qolgan yangilanish (lost update) va uni oldini olish usullari](#225-yoqolgan-yangilanish-lost-update-va-uni-oldini-olish-usullari)
  - [22.6 Qator darajasidagi lock: `FOR UPDATE`, `FOR NO KEY UPDATE`, `SKIP LOCKED`](#226-qator-darajasidagi-lock-for-update-for-no-key-update-skip-locked)
  - [22.7 Jadval darajasidagi lock turlari va DDL ning lock talabi](#227-jadval-darajasidagi-lock-turlari-va-ddl-ning-lock-talabi)
  - [22.8 Deadlock qanday yuzaga keladi, log da qanday ko'rinadi, qanday oldini olinadi](#228-deadlock-qanday-yuzaga-keladi-log-da-qanday-korinadi-qanday-oldini-olinadi)
  - [22.9 Uzoq ochiq tranzaksiya: vacuum ni to'xtatishi va bloat keltirishi](#229-uzoq-ochiq-tranzaksiya-vacuum-ni-toxtatishi-va-bloat-keltirishi)
  - [22.10 `pg_locks` va `pg_stat_activity` bilan bloklanishni topish](#2210-pg_locks-va-pg_stat_activity-bilan-bloklanishni-topish)
  - [22.11 Navbat jadvali qurish: `SKIP LOCKED` bilan ishonchli ishlov berish](#2211-navbat-jadvali-qurish-skip-locked-bilan-ishonchli-ishlov-berish)
  - [22.12 Amalda qo'llash](#2212-amalda-qollash)
- [23. Indekslar: B-tree, GIN, GiST, BRIN va tanlov (Indexes)](#23-indekslar-b-tree-gin-gist-brin-va-tanlov-indexes)
  - [23.1 B-tree tuzilishi va u qaysi so'rovlarga yordam beradi](#231-b-tree-tuzilishi-va-u-qaysi-sorovlarga-yordam-beradi)
  - [23.2 Ko'p ustunli indeks va ustunlar tartibining ahamiyati](#232-kop-ustunli-indeks-va-ustunlar-tartibining-ahamiyati)
  - [23.3 Qamrab oluvchi indeks (`INCLUDE`) va index-only scan sharti](#233-qamrab-oluvchi-indeks-include-va-index-only-scan-sharti)
  - [23.4 Qisman indeks (`WHERE` bilan) va uning amaliy foydasi](#234-qisman-indeks-where-bilan-va-uning-amaliy-foydasi)
  - [23.5 Ifoda bo'yicha indeks va funksiya bilan qidirish](#235-ifoda-boyicha-indeks-va-funksiya-bilan-qidirish)
  - [23.6 GIN: massiv, `jsonb` va to'liq matn qidiruvi uchun](#236-gin-massiv-jsonb-va-toliq-matn-qidiruvi-uchun)
  - [23.7 GiST, matn o'xshashligi va oraliq turlar](#237-gist-matn-oxshashligi-va-oraliq-turlar)
  - [23.8 BRIN: katta, tartibli jadvallar uchun arzon indeks](#238-brin-katta-tartibli-jadvallar-uchun-arzon-indeks)
  - [23.9 Indeks narxi: yozuv sekinlashuvi, disk, vacuum yuki](#239-indeks-narxi-yozuv-sekinlashuvi-disk-vacuum-yuki)
  - [23.10 Keraksiz indekslarni topish va o'chirish (`pg_stat_user_indexes`)](#2310-keraksiz-indekslarni-topish-va-ochirish-pg_stat_user_indexes)
  - [23.11 `CREATE INDEX CONCURRENTLY` va ishlab chiqarishda indeks qo'shish](#2311-create-index-concurrently-va-ishlab-chiqarishda-indeks-qoshish)
  - [23.12 Indeks shishishi va `REINDEX CONCURRENTLY`](#2312-indeks-shishishi-va-reindex-concurrently)
  - [23.13 Amalda qo'llash](#2313-amalda-qollash)
- [24. Planner, statistika va EXPLAIN ANALYZE o'qish (Planner and EXPLAIN ANALYZE)](#24-planner-statistika-va-explain-analyze-oqish-planner-and-explain-analyze)
  - [24.1 Planner nima qiladi: variantlar, narx modeli, tanlov](#241-planner-nima-qiladi-variantlar-narx-modeli-tanlov)
  - [24.2 Statistika qayerdan keladi: `ANALYZE`, `pg_statistic`, `default_statistics_target`](#242-statistika-qayerdan-keladi-analyze-pg_statistic-default_statistics_target)
  - [24.3 Narx parametrlari: `random_page_cost`, `seq_page_cost`, `effective_cache_size` ma'nosi](#243-narx-parametrlari-random_page_cost-seq_page_cost-effective_cache_size-manosi)
  - [24.4 Skan turlari: sequential, index, index-only, bitmap heap scan](#244-skan-turlari-sequential-index-index-only-bitmap-heap-scan)
  - [24.5 Join algoritmlari: nested loop, hash join, merge join va qachon qaysi biri tanlanadi](#245-join-algoritmlari-nested-loop-hash-join-merge-join-va-qachon-qaysi-biri-tanlanadi)
  - [24.6 `EXPLAIN (ANALYZE, BUFFERS)` chiqishini satrma-satr o'qish](#246-explain-analyze-buffers-chiqishini-satrma-satr-oqish)
  - [24.7 Taxmin qilingan va haqiqiy qator soni farqi: eng muhim signal](#247-taxmin-qilingan-va-haqiqiy-qator-soni-farqi-eng-muhim-signal)
  - [24.8 Ko'p ustunli statistika (`CREATE STATISTICS`) va bog'liq ustunlar muammosi](#248-kop-ustunli-statistika-create-statistics-va-bogliq-ustunlar-muammosi)
  - [24.9 Parametrlashtirilgan so'rov va generic plan muammosi (`plan_cache_mode`)](#249-parametrlashtirilgan-sorov-va-generic-plan-muammosi-plan_cache_mode)
  - [24.10 `pg_stat_statements` bilan eng qimmat so'rovlarni topish](#2410-pg_stat_statements-bilan-eng-qimmat-sorovlarni-topish)
  - [24.11 So'rovni qayta yozish: `EXISTS`, `LATERAL`, `DISTINCT ON`, CTE va materializatsiya](#2411-sorovni-qayta-yozish-exists-lateral-distinct-on-cte-va-materializatsiya)
  - [24.12 Sekin so'rovni tekshirish tartibi: aniq qadamlar ro'yxati](#2412-sekin-sorovni-tekshirish-tartibi-aniq-qadamlar-royxati)
  - [24.13 Amalda qo'llash](#2413-amalda-qollash)
- [25. Sxema dizayni, ma'lumot turlari va cheklovlar (Schema Design and Data Types)](#25-sxema-dizayni-malumot-turlari-va-cheklovlar-schema-design-and-data-types)
  - [25.1 Turni to'g'ri tanlash: `text`, `varchar`, `numeric`, `timestamptz`, `uuid`, `boolean`](#251-turni-togri-tanlash-text-varchar-numeric-timestamptz-uuid-boolean)
  - [25.2 Pul qiymatini saqlash: `numeric` va butun son yondashuvi](#252-pul-qiymatini-saqlash-numeric-va-butun-son-yondashuvi)
  - [25.3 Vaqtni saqlash: `timestamptz` va vaqt mintaqasi masalasi](#253-vaqtni-saqlash-timestamptz-va-vaqt-mintaqasi-masalasi)
  - [25.4 Birlamchi kalit tanlovi: `bigint` ketma-ketlik, UUIDv4 va UUIDv7 taqqoslashi](#254-birlamchi-kalit-tanlovi-bigint-ketma-ketlik-uuidv4-va-uuidv7-taqqoslashi)
  - [25.5 Cheklovlar ma'lumotlar bazasida bo'lishi kerakligi: `NOT NULL`, `CHECK`, `UNIQUE`, tashqi kalit](#255-cheklovlar-malumotlar-bazasida-bolishi-kerakligi-not-null-check-unique-tashqi-kalit)
  - [25.6 `jsonb` qachon to'g'ri tanlov va qachon dangasalik belgisi](#256-jsonb-qachon-togri-tanlov-va-qachon-dangasalik-belgisi)
  - [25.7 Massiv, `enum` va alohida lug'at jadvali orasidagi tanlov](#257-massiv-enum-va-alohida-lugat-jadvali-orasidagi-tanlov)
  - [25.8 Normalizatsiya va ataylab denormalizatsiya qilish qarori](#258-normalizatsiya-va-ataylab-denormalizatsiya-qilish-qarori)
  - [25.9 Yumshoq o'chirish (soft delete) va uning yashirin narxi](#259-yumshoq-ochirish-soft-delete-va-uning-yashirin-narxi)
  - [25.10 Audit ustunlari va o'zgarishlar tarixini saqlash usullari](#2510-audit-ustunlari-va-ozgarishlar-tarixini-saqlash-usullari)
  - [25.11 Ustun tartibi va qator kattaligi (padding) ta'siri](#2511-ustun-tartibi-va-qator-kattaligi-padding-tasiri)
  - [25.12 Nomlash qoidalari va sxema ichidagi tartib](#2512-nomlash-qoidalari-va-sxema-ichidagi-tartib)
  - [25.13 Amalda qo'llash](#2513-amalda-qollash)
- [26. Partitioning, replikatsiya va katta hajm (Partitioning, Replication and Scale)](#26-partitioning-replikatsiya-va-katta-hajm-partitioning-replication-and-scale)
  - [26.1 Jadval qachon katta hisoblanadi: qaror uchun raqamlar](#261-jadval-qachon-katta-hisoblanadi-qaror-uchun-raqamlar)
  - [26.2 Deklarativ partitioning: range, list, hash va kalit tanlash](#262-deklarativ-partitioning-range-list-hash-va-kalit-tanlash)
  - [26.3 Partition pruning qachon ishlaydi va qachon ishlamaydi](#263-partition-pruning-qachon-ishlaydi-va-qachon-ishlamaydi)
  - [26.4 Eski ma'lumotni o'chirish: `DETACH PARTITION` ning tezligi](#264-eski-malumotni-ochirish-detach-partition-ning-tezligi)
  - [26.5 Mavjud katta jadvalni to'xtashsiz partitsiyalashga o'tkazish](#265-mavjud-katta-jadvalni-toxtashsiz-partitsiyalashga-otkazish)
  - [26.6 Streaming replikatsiya: primary va standby, lag o'lchash](#266-streaming-replikatsiya-primary-va-standby-lag-olchash)
  - [26.7 Sinxron va asinxron replikatsiya tanlovi va uning narxi](#267-sinxron-va-asinxron-replikatsiya-tanlovi-va-uning-narxi)
  - [26.8 O'qishni standby ga yo'naltirish va replikatsiya lag dan kelib chiqadigan xatolar](#268-oqishni-standby-ga-yonaltirish-va-replikatsiya-lag-dan-kelib-chiqadigan-xatolar)
  - [26.9 Mantiqiy replikatsiya va CDC uchun asos](#269-mantiqiy-replikatsiya-va-cdc-uchun-asos)
  - [26.10 Failover va yuqori mavjudlik vositalari haqida qisqacha](#2610-failover-va-yuqori-mavjudlik-vositalari-haqida-qisqacha)
  - [26.11 Spring da o'qish va yozish uchun alohida DataSource sozlash](#2611-spring-da-oqish-va-yozish-uchun-alohida-datasource-sozlash)
  - [26.12 Sharding qachon zarur bo'ladi va nega eng oxirgi chora](#2612-sharding-qachon-zarur-boladi-va-nega-eng-oxirgi-chora)
  - [26.13 Amalda qo'llash](#2613-amalda-qollash)
- [27. Sozlash, connection pool va monitoring (Configuration, Pooling and Monitoring)](#27-sozlash-connection-pool-va-monitoring-configuration-pooling-and-monitoring)
  - [27.1 Asosiy `postgresql.conf` parametrlari va ularni server resursidan kelib chiqib hisoblash](#271-asosiy-postgresqlconf-parametrlari-va-ularni-server-resursidan-kelib-chiqib-hisoblash)
  - [27.2 `shared_buffers`, `work_mem`, `maintenance_work_mem`, `effective_cache_size` tanlash](#272-shared_buffers-work_mem-maintenance_work_mem-effective_cache_size-tanlash)
  - [27.3 `work_mem` tuzog'i: u har bir operatsiya uchun ajratiladi](#273-work_mem-tuzogi-u-har-bir-operatsiya-uchun-ajratiladi)
  - [27.4 `max_connections` nega katta bo'lmasligi kerak](#274-max_connections-nega-katta-bolmasligi-kerak)
  - [27.5 HikariCP sozlash: `maximum-pool-size`, `connection-timeout`, `max-lifetime`, `leak-detection-threshold`](#275-hikaricp-sozlash-maximum-pool-size-connection-timeout-max-lifetime-leak-detection-threshold)
  - [27.6 Pool kattaligini hisoblash formulasi va amaliy raqamlar](#276-pool-kattaligini-hisoblash-formulasi-va-amaliy-raqamlar)
  - [27.7 PgBouncer: transaction va session rejimi, prepared statement masalasi](#277-pgbouncer-transaction-va-session-rejimi-prepared-statement-masalasi)
  - [27.8 `statement_timeout`, `lock_timeout`, `idle_in_transaction_session_timeout` o'rnatish](#278-statement_timeout-lock_timeout-idle_in_transaction_session_timeout-ornatish)
  - [27.9 Monitoring uchun asosiy ko'rsatkichlar: `pg_stat_database`, `pg_stat_activity`, kesh hit nisbati](#279-monitoring-uchun-asosiy-korsatkichlar-pg_stat_database-pg_stat_activity-kesh-hit-nisbati)
  - [27.10 `pg_stat_statements` ni yoqish va undan muntazam foydalanish](#2710-pg_stat_statements-ni-yoqish-va-undan-muntazam-foydalanish)
  - [27.11 Sekin so'rov logi va `auto_explain` sozlash](#2711-sekin-sorov-logi-va-auto_explain-sozlash)
  - [27.12 Zaxira nusxa va tiklanish: `pg_basebackup`, PITR, tiklanishni sinab ko'rish majburiyati](#2712-zaxira-nusxa-va-tiklanish-pg_basebackup-pitr-tiklanishni-sinab-korish-majburiyati)
  - [27.13 Amalda qo'llash](#2713-amalda-qollash)

**[V. Atrof ekotizim: operatsion haqiqat](#v-atrof-ekotizim-operatsion-haqiqat)**

- [28. Keshlash amaliyoti: invalidatsiya, stampede, Redis haqiqati (Caching in Practice)](#28-keshlash-amaliyoti-invalidatsiya-stampede-redis-haqiqati-caching-in-practice)
  - [28.1 Kesh qo'yishdan oldin so'raladigan savollar](#281-kesh-qoyishdan-oldin-soraladigan-savollar)
  - [28.2 Hit nisbati qanchadan boshlab foyda beradi](#282-hit-nisbati-qanchadan-boshlab-foyda-beradi)
  - [28.3 Mahalliy kesh va taqsimlangan kesh tanlovi](#283-mahalliy-kesh-va-taqsimlangan-kesh-tanlovi)
  - [28.4 Spring Cache abstraksiyasi mexanikasi va proxy chegarasi](#284-spring-cache-abstraksiyasi-mexanikasi-va-proxy-chegarasi)
  - [28.5 Invalidatsiya: muddat, hodisa va versiya kaliti bo'yicha](#285-invalidatsiya-muddat-hodisa-va-versiya-kaliti-boyicha)
  - [28.6 Kesh stampede va undan himoya usullari](#286-kesh-stampede-va-undan-himoya-usullari)
  - [28.7 Eskirgan ma'lumotni ko'rsatish siyosati](#287-eskirgan-malumotni-korsatish-siyosati)
  - [28.8 Kesh va tranzaksiya nomuvofiqligi](#288-kesh-va-tranzaksiya-nomuvofiqligi)
  - [28.9 Redis operatsion haqiqati: xotira, eviction va bitta thread](#289-redis-operatsion-haqiqati-xotira-eviction-va-bitta-thread)
  - [28.10 Katta kalit, uzun ro'yxat va KEYS buyrug'i xavfi](#2810-katta-kalit-uzun-royxat-va-keys-buyrugi-xavfi)
  - [28.11 Serializatsiya tanlovi va kesh qiymati hajmi](#2811-serializatsiya-tanlovi-va-kesh-qiymati-hajmi)
  - [28.12 Kesh ishlamay qolganda tizim yiqilmasligi](#2812-kesh-ishlamay-qolganda-tizim-yiqilmasligi)
  - [28.13 Amalda qo'llash](#2813-amalda-qollash)
- [29. Kafka operatsion haqiqati: partition, lag, rebalance, idempotentlik (Kafka in Production)](#29-kafka-operatsion-haqiqati-partition-lag-rebalance-idempotentlik-kafka-in-production)
  - [29.1 Kafka modeli: topic, partition, offset, consumer group](#291-kafka-modeli-topic-partition-offset-consumer-group)
  - [29.2 Partition soni tanlash: parallellik chegarasi va keyin o'zgartirish qiyinligi](#292-partition-soni-tanlash-parallellik-chegarasi-va-keyin-ozgartirish-qiyinligi)
  - [29.3 Kalit tanlash va tartib kafolati: tartib faqat partition ichida](#293-kalit-tanlash-va-tartib-kafolati-tartib-faqat-partition-ichida)
  - [29.4 Producer sozlamalari: acks, enable.idempotence, linger.ms, batch.size](#294-producer-sozlamalari-acks-enableidempotence-lingerms-batchsize)
  - [29.5 Consumer sozlamalari: max.poll.records, max.poll.interval.ms va rebalance sababi](#295-consumer-sozlamalari-maxpollrecords-maxpollintervalms-va-rebalance-sababi)
  - [29.6 Offset commit strategiyasi va kamida bir marta yetkazish oqibati](#296-offset-commit-strategiyasi-va-kamida-bir-marta-yetkazish-oqibati)
  - [29.7 Idempotent iste'molchi qurish: PostgreSQL da ishlov berilgan xabar jadvali](#297-idempotent-istemolchi-qurish-postgresql-da-ishlov-berilgan-xabar-jadvali)
  - [29.8 Consumer lag ni o'lchash va ogohlantirish chegarasi qo'yish](#298-consumer-lag-ni-olchash-va-ogohlantirish-chegarasi-qoyish)
  - [29.9 Xato xabar bilan nima qilish: qayta urinish topic va dead letter topic](#299-xato-xabar-bilan-nima-qilish-qayta-urinish-topic-va-dead-letter-topic)
  - [29.10 Sxema o'zgarishi va orqaga moslik](#2910-sxema-ozgarishi-va-orqaga-moslik)
  - [29.11 Tranzaksiya va xabar yuborish nomuvofiqligi: nega ikki fazali commit emas](#2911-tranzaksiya-va-xabar-yuborish-nomuvofiqligi-nega-ikki-fazali-commit-emas)
  - [29.12 Spring Kafka da asosiy sozlamalar va xato ishlovchisi](#2912-spring-kafka-da-asosiy-sozlamalar-va-xato-ishlovchisi)
  - [29.13 Qaror jadvali: oddiy yondashuv va arxitektor yondashuvi](#2913-qaror-jadvali-oddiy-yondashuv-va-arxitektor-yondashuvi)
  - [29.14 Amalda qo'llash](#2914-amalda-qollash)
- [30. Kuzatuvchanlik amaliyoti: log, metrika, trace va ularning narxi (Observability in Practice)](#30-kuzatuvchanlik-amaliyoti-log-metrika-trace-va-ularning-narxi-observability-in-practice)
  - [30.1 Uchta manba: log, metrika, trace va har biri qaysi savolga javob beradi](#301-uchta-manba-log-metrika-trace-va-har-biri-qaysi-savolga-javob-beradi)
  - [30.2 Tuzilgan (strukturali) log: JSON format, maydon nomlari, trace id bog'lash](#302-tuzilgan-strukturali-log-json-format-maydon-nomlari-trace-id-boglash)
  - [30.3 Log darajalari siyosati va ishlab chiqarishda nimani yozmaslik kerak](#303-log-darajalari-siyosati-va-ishlab-chiqarishda-nimani-yozmaslik-kerak)
  - [30.4 Log hajmi va narxi: bitta so'rovga nechta qator yozilyapti](#304-log-hajmi-va-narxi-bitta-sorovga-nechta-qator-yozilyapti)
  - [30.5 Micrometer bilan metrika: counter, gauge, timer, distribution summary](#305-micrometer-bilan-metrika-counter-gauge-timer-distribution-summary)
  - [30.6 Kardinallik portlashi: metrika tegiga foydalanuvchi id qo'yish xatosi](#306-kardinallik-portlashi-metrika-tegiga-foydalanuvchi-id-qoyish-xatosi)
  - [30.7 Qaysi metrikalar majburiy: so'rov soni, xato ulushi, kechikish taqsimoti, resurs](#307-qaysi-metrikalar-majburiy-sorov-soni-xato-ulushi-kechikish-taqsimoti-resurs)
  - [30.8 OpenTelemetry: trace, span, kontekst tarqalishi va namuna olish (sampling)](#308-opentelemetry-trace-span-kontekst-tarqalishi-va-namuna-olish-sampling)
  - [30.9 Namuna olish darajasi tanlash va xatoli so'rovlarni to'liq saqlash](#309-namuna-olish-darajasi-tanlash-va-xatoli-sorovlarni-toliq-saqlash)
  - [30.10 Ogohlantirish (alert) dizayni: belgiga emas, foydalanuvchi ta'siriga qarab](#3010-ogohlantirish-alert-dizayni-belgiga-emas-foydalanuvchi-tasiriga-qarab)
  - [30.11 Dashboard qanday bo'lishi kerak: birinchi ekranda nima turadi](#3011-dashboard-qanday-bolishi-kerak-birinchi-ekranda-nima-turadi)
  - [30.12 Spring Boot Actuator va Micrometer sozlash amaliyoti](#3012-spring-boot-actuator-va-micrometer-sozlash-amaliyoti)
  - [30.13 Amalda qo'llash](#3013-amalda-qollash)
- [31. Deployment haqiqati: konteyner, cgroup, JVM va probe (Deployment Reality)](#31-deployment-haqiqati-konteyner-cgroup-jvm-va-probe-deployment-reality)
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
  - [31.13 Amalda qo'llash](#3113-amalda-qollash)
- [32. Tarmoq, timeout va integratsiya haqiqati (Network, Timeouts and Integration)](#32-tarmoq-timeout-va-integratsiya-haqiqati-network-timeouts-and-integration)
  - [32.1 Tarmoq ishonchsiz: ulanish uzilishi, paket yo'qolishi, yarim ochiq ulanish](#321-tarmoq-ishonchsiz-ulanish-uzilishi-paket-yoqolishi-yarim-ochiq-ulanish)
  - [32.2 Timeout turlari: ulanish, o'qish, yozish, umumiy so'rov, va ularning farqi](#322-timeout-turlari-ulanish-oqish-yozish-umumiy-sorov-va-ularning-farqi)
  - [32.3 Timeout qiymatini qanday tanlash: yuqori qatlam quyi qatlamdan uzunroq bo'lsin](#323-timeout-qiymatini-qanday-tanlash-yuqori-qatlam-quyi-qatlamdan-uzunroq-bolsin)
  - [32.4 Timeout byudjeti: zanjirdagi har bir chaqiruvga vaqt taqsimlash](#324-timeout-byudjeti-zanjirdagi-har-bir-chaqiruvga-vaqt-taqsimlash)
  - [32.5 Ulanish hovuzi (HTTP client va JDBC): kattalik, kutish navbati, keep-alive](#325-ulanish-hovuzi-http-client-va-jdbc-kattalik-kutish-navbati-keep-alive)
  - [32.6 DNS: TTL, keshlash va JVM dagi DNS kesh sozlamalari](#326-dns-ttl-keshlash-va-jvm-dagi-dns-kesh-sozlamalari)
  - [32.7 TLS: qo'l siqish narxi, sertifikat muddati, ichki CA, qayta ishlatish](#327-tls-qol-siqish-narxi-sertifikat-muddati-ichki-ca-qayta-ishlatish)
  - [32.8 Qayta urinish siyosati: faqat idempotent chaqiruvda, eksponensial kechikish va jitter](#328-qayta-urinish-siyosati-faqat-idempotent-chaqiruvda-eksponensial-kechikish-va-jitter)
  - [32.9 Orqaga bosim (backpressure) va navbat chuqurligini cheklash](#329-orqaga-bosim-backpressure-va-navbat-chuqurligini-cheklash)
  - [32.10 Tashqi servis bilan shartnoma: versiyalash, buzilmaydigan o'zgarish, ogohlantirish](#3210-tashqi-servis-bilan-shartnoma-versiyalash-buzilmaydigan-ozgarish-ogohlantirish)
  - [32.11 Yuk tarqatuvchi va proxy sozlamalari: idle timeout nomuvofiqligi tuzog'i](#3211-yuk-tarqatuvchi-va-proxy-sozlamalari-idle-timeout-nomuvofiqligi-tuzogi)
  - [32.12 Integratsiyani sinash: tashqi servis sekinlashganda nima bo'ladi](#3212-integratsiyani-sinash-tashqi-servis-sekinlashganda-nima-boladi)
  - [32.13 Amalda qo'llash](#3213-amalda-qollash)

**[VI. Amaliyot va o'sish](#vi-amaliyot-va-osish)**

- [33. Sxema migratsiyasi va to'xtashsiz reliz (Schema Migration and Zero-Downtime Release)](#33-sxema-migratsiyasi-va-toxtashsiz-reliz-schema-migration-and-zero-downtime-release)
  - [33.1 Migratsiya vositalari: Flyway va Liquibase, versiyalash va nomlash tartibi](#331-migratsiya-vositalari-flyway-va-liquibase-versiyalash-va-nomlash-tartibi)
  - [33.2 Migratsiya qoidalari: oldinga faqat yangi fayl, qo'lda o'zgartirmaslik](#332-migratsiya-qoidalari-oldinga-faqat-yangi-fayl-qolda-ozgartirmaslik)
  - [33.3 Kengaytirish va qisqartirish (expand and contract) usuli bosqichma-bosqich](#333-kengaytirish-va-qisqartirish-expand-and-contract-usuli-bosqichma-bosqich)
  - [33.4 Ustun qo'shish, nomini o'zgartirish va o'chirishning xavfsiz ketma-ketligi](#334-ustun-qoshish-nomini-ozgartirish-va-ochirishning-xavfsiz-ketma-ketligi)
  - [33.5 Qaysi DDL jadvalni bloklaydi: `ALTER TABLE` turlarining lock darajasi](#335-qaysi-ddl-jadvalni-bloklaydi-alter-table-turlarining-lock-darajasi)
  - [33.6 Katta jadvalga ustun qo'shish va standart qiymat masalasi](#336-katta-jadvalga-ustun-qoshish-va-standart-qiymat-masalasi)
  - [33.7 `NOT NULL` va `CHECK` cheklovini to'xtashsiz qo'shish (`NOT VALID` va `VALIDATE`)](#337-not-null-va-check-cheklovini-toxtashsiz-qoshish-not-valid-va-validate)
  - [33.8 Indeksni ishlab chiqarishda qo'shish: `CONCURRENTLY` va u uzilganda nima bo'ladi](#338-indeksni-ishlab-chiqarishda-qoshish-concurrently-va-u-uzilganda-nima-boladi)
  - [33.9 Ma'lumotni ko'chirish (backfill): bo'laklab, yuk nazorati bilan](#339-malumotni-kochirish-backfill-bolaklab-yuk-nazorati-bilan)
  - [33.10 Kod va sxema relizini bir-biriga moslashtirish: eski kod yangi sxemada ishlasin](#3310-kod-va-sxema-relizini-bir-biriga-moslashtirish-eski-kod-yangi-sxemada-ishlasin)
  - [33.11 Orqaga qaytish (rollback) rejasi: sxemani qaytarish nega qiyin](#3311-orqaga-qaytish-rollback-rejasi-sxemani-qaytarish-nega-qiyin)
  - [33.12 Migratsiyani sinash: ishlab chiqarish hajmidagi nusxada vaqtini o'lchash](#3312-migratsiyani-sinash-ishlab-chiqarish-hajmidagi-nusxada-vaqtini-olchash)
  - [33.13 Amalda qo'llash](#3313-amalda-qollash)
- [34. Legacy kod va bosqichma-bosqich refaktoring (Legacy Code and Refactoring)](#34-legacy-kod-va-bosqichma-bosqich-refaktoring-legacy-code-and-refactoring)
  - [34.1 Legacy kodga birinchi kun: o'qish, o'lchash, hech narsani o'zgartirmaslik](#341-legacy-kodga-birinchi-kun-oqish-olchash-hech-narsani-ozgartirmaslik)
  - [34.2 Tizimni tushunish usullari: kirish nuqtalari, ma'lumot oqimi, eng ko'p o'zgargan fayllar](#342-tizimni-tushunish-usullari-kirish-nuqtalari-malumot-oqimi-eng-kop-ozgargan-fayllar)
  - [34.3 Xavfsizlik to'ri qurish: xatti-harakatni qayd etuvchi test](#343-xavfsizlik-tori-qurish-xatti-harakatni-qayd-etuvchi-test)
  - [34.4 Chok (seam) topish: o'zgarishni kiritish mumkin bo'lgan nuqta](#344-chok-seam-topish-ozgarishni-kiritish-mumkin-bolgan-nuqta)
  - [34.5 Kichik qadamlar: har bir qadamdan keyin ishlaydigan tizim](#345-kichik-qadamlar-har-bir-qadamdan-keyin-ishlaydigan-tizim)
  - [34.6 Katta qayta yozish nega deyarli har doim muvaffaqiyatsiz bo'ladi](#346-katta-qayta-yozish-nega-deyarli-har-doim-muvaffaqiyatsiz-boladi)
  - [34.7 Bo'g'uvchi anjir (strangler) usuli bilan bosqichma-bosqich almashtirish](#347-boguvchi-anjir-strangler-usuli-bilan-bosqichma-bosqich-almashtirish)
  - [34.8 Ma'lumotlar bazasini ajratish: eng qiyin qism va uning tartibi](#348-malumotlar-bazasini-ajratish-eng-qiyin-qism-va-uning-tartibi)
  - [34.9 Refaktoringni biznes bilan kelishish: qiymat tilida tushuntirish](#349-refaktoringni-biznes-bilan-kelishish-qiymat-tilida-tushuntirish)
  - [34.10 O'lchov: refaktoring ishladimi yoki yo'qligini qanday bilish](#3410-olchov-refaktoring-ishladimi-yoki-yoqligini-qanday-bilish)
  - [34.11 Qachon tegmaslik kerak: ishlayotgan, o'zgarmaydigan kod](#3411-qachon-tegmaslik-kerak-ishlayotgan-ozgarmaydigan-kod)
  - [34.12 Bosqichma-bosqich reja namunasi: to'lov moduli misolida](#3412-bosqichma-bosqich-reja-namunasi-tolov-moduli-misolida)
  - [34.13 Amalda qo'llash](#3413-amalda-qollash)
- [35. Incident, on-call va post-mortem (Incidents and Post-mortems)](#35-incident-on-call-va-post-mortem-incidents-and-post-mortems)
  - [35.1 Incident darajalari va ularni belgilash mezoni](#351-incident-darajalari-va-ularni-belgilash-mezoni)
  - [35.2 Incident paytidagi rollar: boshqaruvchi, tekshiruvchi, aloqachi](#352-incident-paytidagi-rollar-boshqaruvchi-tekshiruvchi-aloqachi)
  - [35.3 Birinchi qadam: tiklash, sabab qidirish emas](#353-birinchi-qadam-tiklash-sabab-qidirish-emas)
  - [35.4 Tiklash usullari: orqaga qaytarish, flag o'chirish, trafikni yo'naltirish](#354-tiklash-usullari-orqaga-qaytarish-flag-ochirish-trafikni-yonaltirish)
  - [35.5 Diagnostika tartibi: nima o'zgardi, qachon boshlandi, nima umumiy](#355-diagnostika-tartibi-nima-ozgardi-qachon-boshlandi-nima-umumiy)
  - [35.6 Muloqot: kimga, qanchalik tez-tez, qanday til bilan](#356-muloqot-kimga-qanchalik-tez-tez-qanday-til-bilan)
  - [35.7 Incident jurnali va vaqt chizig'ini yozib borish](#357-incident-jurnali-va-vaqt-chizigini-yozib-borish)
  - [35.8 Ayblamaydigan post-mortem: tuzilishi va yozish qoidalari](#358-ayblamaydigan-post-mortem-tuzilishi-va-yozish-qoidalari)
  - [35.9 Besh marta "nega" va tizimli sabablarga yetish](#359-besh-marta-nega-va-tizimli-sabablarga-yetish)
  - [35.10 Harakat bandlari: egasi, muddati, tekshiruvi bo'lsin](#3510-harakat-bandlari-egasi-muddati-tekshiruvi-bolsin)
  - [35.11 On-call navbati: adolatli taqsimot, ogohlantirish charchoqini kamaytirish](#3511-on-call-navbati-adolatli-taqsimot-ogohlantirish-charchoqini-kamaytirish)
  - [35.12 Ogohlantirishlar sifati: har bir alert bajariladigan ish bo'lsin](#3512-ogohlantirishlar-sifati-har-bir-alert-bajariladigan-ish-bolsin)
  - [35.13 To'liq post-mortem namunasi: to'lov servisi uzilishi misolida](#3513-toliq-post-mortem-namunasi-tolov-servisi-uzilishi-misolida)
  - [35.14 Amalda qo'llash](#3514-amalda-qollash)
- [36. Code review va jamoada texnik yetakchilik (Code Review and Technical Leadership)](#36-code-review-va-jamoada-texnik-yetakchilik-code-review-and-technical-leadership)
  - [36.1 Code review nimani topishi kerak: xatti-harakat, chegara, nom, xavfsizlik](#361-code-review-nimani-topishi-kerak-xatti-harakat-chegara-nom-xavfsizlik)
  - [36.2 Nimani topmasligi kerak: formatlash, uslub, mashina tekshiradigan narsalar](#362-nimani-topmasligi-kerak-formatlash-uslub-mashina-tekshiradigan-narsalar)
  - [36.3 Izoh yozish uslubi: muammoni ko'rsat, qaror egasini qoldirib ket](#363-izoh-yozish-uslubi-muammoni-korsat-qaror-egasini-qoldirib-ket)
  - [36.4 Majburiy va ixtiyoriy izohlarni ajratish](#364-majburiy-va-ixtiyoriy-izohlarni-ajratish)
  - [36.5 Review hajmi: katta o'zgarishni bo'lish va navbat vaqtini qisqartirish](#365-review-hajmi-katta-ozgarishni-bolish-va-navbat-vaqtini-qisqartirish)
  - [36.6 Kelishmovchilikni hal qilish: dalil, prototip, uchinchi fikr](#366-kelishmovchilikni-hal-qilish-dalil-prototip-uchinchi-fikr)
  - [36.7 Yangi odamga review orqali o'rgatish](#367-yangi-odamga-review-orqali-orgatish)
  - [36.8 Arxitektura qarorlarini jamoaga tarqatish: hujjat, ichki suhbat, namuna kod](#368-arxitektura-qarorlarini-jamoaga-tarqatish-hujjat-ichki-suhbat-namuna-kod)
  - [36.9 Standart o'rnatish: linter, formatlash, ArchUnit qoidalari, shablon loyiha](#369-standart-ornatish-linter-formatlash-archunit-qoidalari-shablon-loyiha)
  - [36.10 Jamoaning bilim xaritasi va bitta odamga bog'liqlikni kamaytirish](#3610-jamoaning-bilim-xaritasi-va-bitta-odamga-bogliqlikni-kamaytirish)
  - [36.11 Texnik yetakchi va menejer roli farqi](#3611-texnik-yetakchi-va-menejer-roli-farqi)
  - [36.12 Vaqtni taqsimlash: kod, hujjat, suhbat, o'rganish](#3612-vaqtni-taqsimlash-kod-hujjat-suhbat-organish)
  - [36.13 Amalda qo'llash](#3613-amalda-qollash)
- [37. Xarajat, SLO va biznes bilan muloqot (Cost, SLO and Business Communication)](#37-xarajat-slo-va-biznes-bilan-muloqot-cost-slo-and-business-communication)
  - [37.1 Arxitektura qarorining pul tarafi: server, litsenziya, odam vaqti](#371-arxitektura-qarorining-pul-tarafi-server-litsenziya-odam-vaqti)
  - [37.2 Bulut xarajati qayerdan keladi: hisoblash, saqlash, tarmoq chiqishi, boshqariladigan xizmat](#372-bulut-xarajati-qayerdan-keladi-hisoblash-saqlash-tarmoq-chiqishi-boshqariladigan-xizmat)
  - [37.3 Bitta so'rovning narxi: oddiy hisob va uni kuzatish](#373-bitta-sorovning-narxi-oddiy-hisob-va-uni-kuzatish)
  - [37.4 Xarajatni kamaytirish yo'llari va ularning sifatga ta'siri](#374-xarajatni-kamaytirish-yollari-va-ularning-sifatga-tasiri)
  - [37.5 SLI, SLO va SLA farqi, ularni to'g'ri tanlash](#375-sli-slo-va-sla-farqi-ularni-togri-tanlash)
  - [37.6 Xato byudjeti (error budget) va u qanday qaror qabul qilishga yordam beradi](#376-xato-byudjeti-error-budget-va-u-qanday-qaror-qabul-qilishga-yordam-beradi)
  - [37.7 Mavjudlik raqamlari: 99.9 va 99.99 orasidagi amaliy farq va narxi](#377-mavjudlik-raqamlari-999-va-9999-orasidagi-amaliy-farq-va-narxi)
  - [37.8 Nofunksional talabni biznes tiliga o'girish](#378-nofunksional-talabni-biznes-tiliga-ogirish)
  - [37.9 Texnik qarzni biznesga tushuntirish: tezlik va xavf tilida](#379-texnik-qarzni-biznesga-tushuntirish-tezlik-va-xavf-tilida)
  - [37.10 Qaror uchun arzon o'lchov: kichik tajriba va bosqichma-bosqich yoyish](#3710-qaror-uchun-arzon-olchov-kichik-tajriba-va-bosqichma-bosqich-yoyish)
  - [37.11 Yetkazib berish muddati va sifat orasidagi muzokarani olib borish](#3711-yetkazib-berish-muddati-va-sifat-orasidagi-muzokarani-olib-borish)
  - [37.12 Hisobot: rahbarga nima ko'rsatiladi va qanday ko'rinishda](#3712-hisobot-rahbarga-nima-korsatiladi-va-qanday-korinishda)
  - [37.13 Amalda qo'llash](#3713-amalda-qollash)
- [38. Doimiy o'rganish va texnologiya tanlash (Continuous Learning and Technology Choice)](#38-doimiy-organish-va-texnologiya-tanlash-continuous-learning-and-technology-choice)
  - [38.1 Nimani chuqur o'rganish kerak va nimani yuzaki bilish yetarli](#381-nimani-chuqur-organish-kerak-va-nimani-yuzaki-bilish-yetarli)
  - [38.2 Uzoq yashaydigan bilim va tez eskiradigan bilim farqi](#382-uzoq-yashaydigan-bilim-va-tez-eskiradigan-bilim-farqi)
  - [38.3 Birlamchi manbalar: spetsifikatsiya, hujjat, manba kod, reliz eslatmasi](#383-birlamchi-manbalar-spetsifikatsiya-hujjat-manba-kod-reliz-eslatmasi)
  - [38.4 Yangi kutubxonani baholash mezonlari: qo'llab-quvvatlash, bog'liqlik, chiqish yo'li](#384-yangi-kutubxonani-baholash-mezonlari-qollab-quvvatlash-bogliqlik-chiqish-yoli)
  - [38.5 Bog'liqlik qo'shishning yashirin narxi va uni yangilash majburiyati](#385-bogliqlik-qoshishning-yashirin-narxi-va-uni-yangilash-majburiyati)
  - [38.6 Moda texnologiyani baholash: qaysi muammoni hal qiladi, sizda u bormi](#386-moda-texnologiyani-baholash-qaysi-muammoni-hal-qiladi-sizda-u-bormi)
  - [38.7 Qurish yoki sotib olish qarori va mezonlari](#387-qurish-yoki-sotib-olish-qarori-va-mezonlari)
  - [38.8 Tajriba uchun vaqt ajratish: spike, ichki loyiha, o'lchovli tajriba](#388-tajriba-uchun-vaqt-ajratish-spike-ichki-loyiha-olchovli-tajriba)
  - [38.9 Bilimni jamoaga tarqatish: hujjat, suhbat, namuna kod](#389-bilimni-jamoaga-tarqatish-hujjat-suhbat-namuna-kod)
  - [38.10 Xatolardan o'rganishni odat qilish va o'z qarorlarini qayta ko'rish](#3810-xatolardan-organishni-odat-qilish-va-oz-qarorlarini-qayta-korish)
  - [38.11 Java va Spring ekotizimini kuzatib borish usullari](#3811-java-va-spring-ekotizimini-kuzatib-borish-usullari)
  - [38.12 O'z o'rganish rejangizni tuzish: chorak uchun aniq maqsadlar](#3812-oz-organish-rejangizni-tuzish-chorak-uchun-aniq-maqsadlar)
  - [38.13 Amalda qo'llash](#3813-amalda-qollash)
- [39. Birinchi 90 kun va o'z-o'zini baholash (First 90 Days and Self-Assessment)](#39-birinchi-90-kun-va-oz-ozini-baholash-first-90-days-and-self-assessment)
  - [39.1 Yangi loyihada birinchi hafta: nimani o'qish, kimdan so'rash, nima yozmaslik](#391-yangi-loyihada-birinchi-hafta-nimani-oqish-kimdan-sorash-nima-yozmaslik)
  - [39.2 Birinchi oy: tizim xaritasini chizish va og'riqli nuqtalarni ro'yxatlash](#392-birinchi-oy-tizim-xaritasini-chizish-va-ogriqli-nuqtalarni-royxatlash)
  - [39.3 Ikkinchi oy: kichik, ko'rinadigan yaxshilanish bilan ishonch qozonish](#393-ikkinchi-oy-kichik-korinadigan-yaxshilanish-bilan-ishonch-qozonish)
  - [39.4 Uchinchi oy: o'rta muddatli reja taklif qilish va kelishib olish](#394-uchinchi-oy-orta-muddatli-reja-taklif-qilish-va-kelishib-olish)
  - [39.5 Mavjud qarorlarni hurmat qilish: "nega shunday qilingan" savolini birinchi berish](#395-mavjud-qarorlarni-hurmat-qilish-nega-shunday-qilingan-savolini-birinchi-berish)
  - [39.6 O'z bilimingizdagi bo'shliqni topish uchun o'z-o'zini tekshirish ro'yxati](#396-oz-bilimingizdagi-boshliqni-topish-uchun-oz-ozini-tekshirish-royxati)
  - [39.7 Yetuklik darajalari: qaysi mavzuda qay darajada turibsiz](#397-yetuklik-darajalari-qaysi-mavzuda-qay-darajada-turibsiz)
  - [39.8 Fikrlash va qarorlar bilimini o'zingizga qo'llash](#398-fikrlash-va-qarorlar-bilimini-ozingizga-qollash)
  - [39.9 Java va JVM: o'zingizni sinash savollari](#399-java-va-jvm-ozingizni-sinash-savollari)
  - [39.10 Spring: o'zingizni sinash savollari](#3910-spring-ozingizni-sinash-savollari)
  - [39.11 PostgreSQL: o'zingizni sinash savollari](#3911-postgresql-ozingizni-sinash-savollari)
  - [39.12 Operatsion tayyorlik: o'zingizni sinash savollari](#3912-operatsion-tayyorlik-ozingizni-sinash-savollari)
  - [39.13 Keyingi qadam: shu hujjatni va qolgan ikki hujjatni qanday ishlatish](#3913-keyingi-qadam-shu-hujjatni-va-qolgan-ikki-hujjatni-qanday-ishlatish)
  - [39.14 Amalda qo'llash](#3914-amalda-qollash)


# I. Fikrlash va qarorlar

## 1. Arxitektorning fikrlash modeli (The Architect's Mental Model)

Arxitektorning ishi diagramma chizish emas. Uning ishi noaniq biznes talabini o'lchanadigan texnik cheklovga aylantirish va har bir qarorning narxini oldindan aytib berish. Shu sababli arxitektorning fikrlash modeli kod yozish mahoratidan emas, kontekstni o'qish va trade-off ni raqamda ko'rsatish qobiliyatidan boshlanadi. Bu bobda shu model ichidan o'tamiz: kontekst, trade-off, sifat atributlari, qarorning qaytarilish darajasi va qarorning eskirishi.

### 1.1 Arxitektor va senior developer o'rtasidagi haqiqiy farq

Senior developer berilgan masalani eng yaxshi tarzda yechadi. Arxitektor masalaning o'zi to'g'ri qo'yilganini tekshiradi. Farq mahoratda emas, javobgarlik ufqida. Senior bitta servis va bitta sprint doirasida o'ylaydi, arxitektor esa uch yildan keyin shu servisni kim qo'llab-quvvatlaydi deb o'ylaydi.

Ikkinchi farq: senior "qanday qilib" degan savolga javob beradi, arxitektor "nega aynan shunday" degan savolga javob beradi. To'lov servisida senior idempotentlik kalitini `UNIQUE` indeks bilan amalga oshiradi. Arxitektor esa idempotentlik oynasi qancha vaqt saqlanishini, eski kalitlarni kim tozalashini va bu jadval bir yilda qancha o'sishini hisoblaydi.

Uchinchi farq: arxitektor o'z qarorini yozib qoldiradi. Yozilmagan qaror olti oydan keyin yo'qoladi. Shu sababli arxitektorning asosiy chiqishi kod emas, qaror yozuvi va o'lchov mezoni.

| Vaziyat | Oddiy yondashuv | Arxitektor yondashuvi |
| --- | --- | --- |
| Yangi talab keldi | Darhol texnik yechim tanlaydi | Avval biznes maqsadi va cheklovlarni so'raydi |
| Texnologiya tanlash | "Zamonaviy" va mashhur variantni oladi | Jamoa tajribasi va operatsion narxni hisoblaydi |
| Performance muammosi | Kodni optimallashtirishga kirishadi | Avval o'lchaydi, keyin eng qimmat qismni tanlaydi |
| Microservice bo'lish | Domen bo'ylab darhol ajratadi | Modulli monolit bilan boshlab, chegarani tekshiradi |
| Cache qo'shish | TTL ni 5 daqiqa qilib qo'yadi | Stale ma'lumot biznesga qancha turishini so'raydi |
| Kutubxona qo'shish | Tez yechim uchun qo'shadi | Yangilash, CVE va transitive bog'liqlikni ko'radi |
| Qaror yozuvi | Og'zaki aytib o'tadi | ADR yozadi, alternativani va narxini qayd qiladi |
| Kelajak talabi | "Keyin kerak bo'ladi" deb mavhum qoldiradi | Taxminni yozadi va qachon tekshirishni belgilaydi |
| Latency maqsadi | "Tez bo'lsin" deydi | p99 uchun aniq raqam va o'lchash usulini beradi |
| Xato holati | Happy path ni yopadi | Timeout, retry va degradatsiya rejimini aniqlaydi |

### 1.2 Kontekst birinchi: biznes maqsadi, jamoa kattaligi, muddat, byudjet

Bir xil talab ikki kompaniyada ikki xil arxitekturaga olib keladi. Sababi kontekst: biznes maqsadi, jamoa kattaligi va tajribasi, muddat, byudjet. Shu to'rttasini yozmagan arxitektor taxmin bilan ishlaydi.

Biznes maqsadi qaysi sifat atributi birinchi o'rinda turishini aytadi. To'lov servisida ma'lumot to'g'riligi latency dan ustun. Omborda qoldiq ko'rsatadigan katalog sahifasida esa latency to'g'rilikdan ustun, chunki bir soniya kechikish konversiyani yo'qotadi. Shu bitta jumla keyingi o'nta qarorni belgilaydi.

Jamoa kattaligi operatsion yukning chegarasini belgilaydi. Besh kishilik jamoa uchun o'n ikki microservice va Kafka klasteri xarajat, qobiliyat emas. Taxminan har bir mustaqil deploy qilinadigan servis haftada bir necha soat operatsion yuk qo'shadi. Shu yukni ko'taradigan odam yo'q bo'lsa, qaror noto'g'ri.

Muddat va byudjet qarorni kesadi. Uch oyda MVP kerak bo'lsa, PostgreSQL ichidagi `FOR UPDATE SKIP LOCKED` navbati broker o'rnini bosadi. Bu ongli vaqtinchalik yechim.

```sql
-- Oddiy navbat: PostgreSQL ichida, broker o'rnatmasdan.
-- SKIP LOCKED bir nechta worker bir-birini kutmasligini ta'minlaydi.
CREATE TABLE payment_outbox (
    id          bigserial PRIMARY KEY,
    aggregate_id uuid        NOT NULL,
    payload     jsonb       NOT NULL,
    status      text        NOT NULL DEFAULT 'NEW',
    attempts    int         NOT NULL DEFAULT 0,
    next_try_at timestamptz NOT NULL DEFAULT now()
);

-- Faqat ishlov berilmagan qatorlar uchun indeks: jadval o'sganda ham kichik qoladi.
CREATE INDEX payment_outbox_pending_idx
    ON payment_outbox (next_try_at)
    WHERE status = 'NEW';

-- Worker bir martada 100 qator oladi, boshqa worker ularni ko'rmaydi.
SELECT id, payload
  FROM payment_outbox
 WHERE status = 'NEW' AND next_try_at <= now()
 ORDER BY next_try_at
 LIMIT 100
 FOR UPDATE SKIP LOCKED;
```

Bu yondashuv taxminan sekundda bir necha mingta xabarga yetadi. Shundan keyin broker kerak bo'ladi. Qaror yozuvida aynan shu chegara ko'rsatilishi kerak.

### 1.3 Trade-off tili: bepul qaror yo'q, har birining narxi bor

Arxitektura qarorining birinchi qonuni oddiy: har bir foyda biror narsa hisobidan keladi. Cache latency ni pasaytiradi va ma'lumot yangiligini yo'qotadi. Replika o'qish yukini bo'ladi va replication lag keltiradi. Async ishlov berish javobni tezlashtiradi va xatoni ko'rinmas qiladi. Shu sababli arxitektor "yaxshiroq" degan so'z o'rniga "nima hisobidan" deb so'raydi.

Amaliy shakli bor: har bir qaror uchun bitta jumla yozish. "X ni oldik, chunki Y ni yaxshilaydi, buning narxi Z, va Z ni W bilan kuzatamiz." Bu jumla yozilmasa, qaror muhokama emas, didga aylanadi.

Misol: buyurtma servisida read replika qo'shish. Foyda: master dagi o'qish yuki taxminan 60 foizga kamayadi. Narx: foydalanuvchi buyurtma yaratgandan keyin uni ro'yxatda darhol ko'rmasligi mumkin. Lag odatda 10 dan 200 millisekundgacha, lekin yuk ostida sekundlarga chiqadi. Yechim: yozuvdan keyingi o'qish master ga yo'naltiriladi.

```java
// Tranzaksiya darajasida qaysi ma'lumotlar bazasiga borishni tanlash.
// readOnly = true bo'lgan tranzaksiya replika ga yo'naltiriladi.
@Service
public class OrderQueryService {

    private final OrderRepository orders;

    // Ro'yxat eskirishi mumkin: 200 ms lag biznes uchun qabul qilinadi.
    @Transactional(readOnly = true)
    public List<OrderView> recentOrders(long customerId) {
        return orders.findTop20ByCustomerIdOrderByCreatedAtDesc(customerId);
    }

    // Yangi yaratilgan buyurtmani ko'rsatish: lag qabul qilinmaydi.
    // readOnly berilmaydi, shuning uchun master ga boradi.
    @Transactional
    public OrderView justCreated(long orderId) {
        return orders.findById(orderId)
                     .map(OrderView::from)
                     .orElseThrow();
    }
}
```

Bu yerda muhimi marshrutlash mexanizmi emas, balki shu: qaysi so'rov eskirgan ma'lumotga toqat qiladi degan savolga biznes javob bergan.

### 1.4 Sifat atributlari va ularni o'lchash

Sifat atributi o'lchanmasa, u talab emas, istak. "Tizim tez bo'lsin" degan gap qaror chiqarmaydi. "Buyurtma yaratish p99 kechikishi 300 millisekunddan oshmasin, kunlik pik yukda, 95 foiz kunlarda" degan gap qaror chiqaradi. Shu sababli arxitektor har bir atributga stsenariy, raqam va o'lchash nuqtasini beradi.

Latency ni o'rtacha qiymat bilan o'lchash eng keng tarqalgan xato. O'rtacha 80 millisekund bo'lgan tizimda p99 ikki sekund bo'lishi mumkin. Foydalanuvchi o'rtachani sezmaydi, u o'z so'rovini sezadi. Shu sababli p95 va p99 o'lchanadi, mean esa faqat qo'shimcha sifatida.

Throughput va latency bir-biriga bog'liq. Pool to'lganda navbat paydo bo'ladi va latency keskin o'sadi. Agar bir so'rov bazani 50 millisekund egallasa, 20 ta ulanish bilan nazariy maksimum taxminan 400 so'rov/sekund bo'ladi.

```properties
# Pool kattaligini "kattaroq yaxshiroq" deb emas, hisob bilan qo'yamiz.
# PostgreSQL da har bir ulanish alohida backend process, xotira hisobi bor.
spring.datasource.hikari.maximum-pool-size=20
spring.datasource.hikari.minimum-idle=20
# Pool bo'sh bo'lmasa, 2 sekunddan ko'p kutmaymiz: tez xato yaxshi.
spring.datasource.hikari.connection-timeout=2000
# Ulanishni 20 daqiqada yangilaymiz, DNS va failover uchun.
spring.datasource.hikari.max-lifetime=1200000
# Ochiq qolgan ulanishni 10 sekundda log ga yozadi.
spring.datasource.hikari.leak-detection-threshold=10000

# Histogram va SLO chegaralari: p99 ni server tomonda o'lchaymiz.
management.metrics.distribution.percentiles-histogram.http.server.requests=true
management.metrics.distribution.slo.http.server.requests=200ms,300ms,500ms,1s
management.endpoints.web.exposure.include=health,metrics,prometheus
```

Availability ni foizda emas, yo'qotilgan daqiqada o'ylash foydali. 99.9 foiz oyda taxminan 43 daqiqa to'xtash degani. 99.99 foiz esa taxminan 4 daqiqa. Ikkinchisi odatda ikki baravar emas, besh baravar qimmat, chunki u avtomatik failover, ko'p zona va mashq qilingan runbook talab qiladi.

Maintainability ham o'lchanadi: o'zgarishdan prod gacha o'tgan vaqt, bitta oddiy o'zgarish uchun tegiladigan modul soni, yangi odam birinchi PR ni qancha kunda yuboradi. Bu raqamlar ko'rinmasa, "toza arxitektura" suhbati did bo'lib qoladi.

```bash
# Sifat atributini o'lchashni gapdan emas, skriptdan boshlang.
# 1) Bazadagi eng qimmat so'rovlarni toping (pg_stat_statements kerak).
psql -c "SELECT calls, round(mean_exec_time::numeric,2) AS avg_ms,
                round(total_exec_time::numeric/1000,1) AS total_s, query
           FROM pg_stat_statements
          ORDER BY total_exec_time DESC LIMIT 10;"

# 2) Konkret so'rovning rejasini real buferlar bilan ko'ring.
psql -c "EXPLAIN (ANALYZE, BUFFERS) SELECT * FROM orders
          WHERE customer_id = 42 ORDER BY created_at DESC LIMIT 20;"

# 3) Pool chegarasini yuk ostida tekshiring, taxminiy emas.
pgbench -c 40 -j 4 -T 60 -S orders_db

# 4) Servis tomonidagi p99 ni Prometheus formatidan o'qing.
curl -s localhost:8080/actuator/metrics/http.server.requests \
  | head -c 400
```

### 1.5 Qaytarib bo'ladigan va qaytarib bo'lmaydigan qarorlar

Qarorlarni muhimlik bo'yicha emas, qaytarilish narxi bo'yicha saralash kerak. Qaytarib bo'ladigan qaror uchun uzoq muhokama vaqtni behuda sarflaydi. Qaytarib bo'lmaydigan qaror uchun tez qaror esa yillarga cho'ziladigan qarz yaratadi.

Odatda arzon qaytariladigan qarorlar: ichki kutubxona tanlovi, cache TTL, log formati, bitta endpoint ning shakli. Qimmat qaytariladigan qarorlar: ma'lumot modeli va jadval bo'linishi, servis chegaralari, public API kontrakti, autentifikatsiya modeli, multi-tenancy strategiyasi. Eng qimmati odatda ma'lumotga tegishli bo'ladi, chunki ma'lumot migratsiya qilinadi, kod esa qayta yoziladi.

Qaytarilish narxini kamaytirishning amaliy usuli bor: qarorni interfeys ortiga yashirish. Agar to'lov provayderi tanlovi noaniq bo'lsa, domen kodi provayder SDK sini ko'rmasligi kerak.

```java
// Domen faqat shu portni biladi, provayder nomini bilmaydi.
// Shu sababli provayderni almashtirish adapter almashtirishga aylanadi.
public interface PaymentGateway {
    PaymentResult charge(ChargeCommand command);
    RefundResult refund(RefundCommand command);
}

// Idempotentlik kaliti domen qarori, provayder detali emas.
public record ChargeCommand(
        String idempotencyKey,
        long orderId,
        BigDecimal amount,
        String currency) { }

// Adapter qatlamida provayderning xato kodlari domen xatosiga ko'chiriladi.
@Component
class AcquirerPaymentGateway implements PaymentGateway {

    @Override
    public PaymentResult charge(ChargeCommand command) {
        // Timeout va retry siyosati shu yerda, domen ichida emas.
        // Tarmoq xatosi "noma'lum natija" deb qaytariladi, "xato" deb emas.
        return PaymentResult.unknownIfTimeout(command.idempotencyKey());
    }
    // refund ham shu adapter ichida, bir xil tamoyil bilan amalga oshiriladi.
}
```

Bu abstraksiya bepul emas, u qo'shimcha qatlam va model qo'shadi. Narxi oqlanadi, chunki aynan qaytarilishi qimmat joyni himoya qiladi. O'sha abstraksiyani har bir CRUD repository uchun qo'yish esa oqlanmaydi.

### 1.6 "Yetarlicha yaxshi" arxitektura, over-engineering va YAGNI chegarasi

Over-engineering mahoratning ortiqchasi emas, noto'g'ri yo'naltirilgan qo'rquv natijasi. Arxitektor noaniqlikni abstraksiya bilan yopishga urinadi va shu bilan noaniqlikni ko'paytiradi. Yetarlicha yaxshi arxitektura esa bugungi talabni bajaradi va ertangi o'zgarishni to'sib qo'ymaydi. Ikkinchi shart birinchisidan muhimroq.

YAGNI chegarasini belgilashning amaliy mezoni: keyin qo'shishning narxi hozir qo'shish narxidan qancha yuqori. Agar farq kichik bo'lsa, kutish kerak. Agar farq katta bo'lsa, hozir qilish kerak. Buyurtma jadvaliga `created_at` ustunini keyin qo'shish arzon. Monolit ichida tranzaksiya chegarasini keyin ajratish qimmat.

Shu mezon ikkita ro'yxat beradi. Hozir: ma'lumot modelining normal shakli, ID strategiyasi, audit maydonlari, migratsiya vositasi, korrelyatsiya ID. Keyin: ikkinchi baza, CQRS read modeli, event sourcing, o'z service mesh i.

| Tuzoq | Nega yuzaga keladi | Yechim |
| --- | --- | --- |
| Har bir servisga alohida baza "kelajak uchun" | Microservice qoidasini kontekstsiz qo'llash | Modulli monolit, schema bo'yicha ajratish, chegara test bilan tekshirilsin |
| Barcha narsaga interfeys va bitta implementatsiya | Testlash uchun kerak degan noto'g'ri odat | Interfeys faqat haqiqiy almashuv nuqtasida qoldirilsin |
| Event sourcing ni hisobot uchun tanlash | Audit talabini noto'g'ri o'qish | Audit jadvali yoki temporal ustunlar yetadi |
| Cache ni o'lchamasdan qo'shish | Latency muammosi taxmin qilingan | Avval so'rov rejasi va indeks tekshirilsin |
| Mavhum "konfiguratsiya dvigateli" | Kelajakdagi talab taxmin qilingan | Kodda qattiq yozilsin, uchinchi holatda umumlashtirilsin |
| Barcha chaqiruvni async qilish | Javob vaqtini yashirish istagi | Async faqat biznes toqat qiladigan joyda, outbox bilan |
| Pool va thread sonini katta qo'yish | "Ko'proq parallel tezroq" degan taxmin | Pool past yuk sinovidan kelib chiqib, backpressure bilan |
| Qaror yozuvining yo'qligi | Yozish vaqt oladi deb hisoblash | Bir sahifali ADR, kontekst, alternativa, narx |

### 1.7 Hozirgi talab va kelajak taxmini orasidagi muvozanat

Kelajakni inkor qilish ham xato. To'g'ri yondashuv kelajakni taxmin sifatida yozib qo'yish va unga tekshirish nuqtasi belgilash. Taxmin yozilganda u muhokama qilinadigan narsaga aylanadi. Yozilmaganda u kodda yashiringan farazga aylanadi.

Taxminni raqam bilan yozish kerak. "Buyurtmalar o'sadi" emas, balki "kunlik buyurtma hozir 20 ming, bir yilda 80 ming, bu sekundda taxminan 3 yozuv". Shu raqam bitta PostgreSQL instansi yetarli ekanini ko'rsatadi. O'n baravar oshsa, partitioning masalasi ochiladi.

Amaliy usul: bugungi kodni sodda qoldirib, kelajakni kengaytirish nuqtasi bilan ta'minlash. Jadvalni hozir bo'lmagan, lekin bo'linishga tayyor qilib loyihalash shunga misol.

```sql
-- Hozir bitta jadval yetadi, lekin kalit partition ga tayyor.
-- Birlamchi kalitga created_at kiritilgani keyingi migratsiyani arzonlashtiradi.
CREATE TABLE orders (
    id          bigserial,
    customer_id bigint      NOT NULL,
    status      text        NOT NULL,
    total       numeric(14,2) NOT NULL,
    created_at  timestamptz NOT NULL DEFAULT now(),
    PRIMARY KEY (id, created_at)
);

-- Eng ko'p ishlatiladigan so'rov uchun kompozit indeks.
CREATE INDEX orders_customer_recent_idx
    ON orders (customer_id, created_at DESC);

-- Kelajakda oylik partition ga o'tish: struktura allaqachon mos.
-- ALTER TABLE orders ... PARTITION BY RANGE (created_at) to'g'ridan-to'g'ri
-- ishlamaydi, shuning uchun yangi partitioned jadval va ma'lumot ko'chirish kerak.
-- Shuning uchun bu qaror "kelajakda qimmat" ro'yxatida turadi.
```

Ba'zi kelajak qarorlari uchun hozir to'liq yechim kerak emas, lekin yo'lni yopmaslik kerak. Arxitektorning ishi shu ikki holatni ajratish.

### 1.8 Arxitektura qarori qanday eskiradi va uni qachon qayta ko'rish kerak

Har bir qaror o'z farazlari ustida turadi. Faraz o'zgarganda qaror eskiradi, qaror yomon bo'lganidan emas. Shu sababli ADR da "bu qaror qaysi farazga tayanadi" degan qism eng qimmatlisi.

Eskirish sabablari: yuk hajmi, jamoa tarkibi, platforma imkoniyati yoki biznes modeli o'zgardi. Misol: Java 21 da virtual thread lar barqarorlashgandan keyin "blocking I/O uchun reactive ga o'tish" qarorining asosi zaiflashdi. Oldingi qaror noto'g'ri emas edi, uning farazi eskirdi.

Qayta ko'rishni tasodifga qoldirmaslik kerak. Har bir muhim qarorga trigger qo'yiladi: metrika chegarasi yoki sana. Chegara buzilsa, qaror qayta ko'riladi.

```yaml
# ADR ga ilova qilinadigan "qayta ko'rish sharti" fayli.
# Bu hujjat emas, kuzatuv uchun mashina o'qiydigan ro'yxat.
decision: ADR-014-single-postgres-for-orders
assumptions:
  - daily_orders_max: 80000          # bir yilga qilingan taxmin
  - write_tps_peak: 10               # pik yozuv tezligi
  - orders_table_rows_max: 30000000  # partitioning chegarasi
review_triggers:
  - metric: orders_table_rows
    threshold: 25000000
    action: "partitioning rejasini ADR sifatida ochish"
  - metric: db_write_tps_p99
    threshold: 25
    action: "yozuv yo'lini qayta o'lchash, batch imkoniyatini ko'rish"
  - metric: replica_lag_seconds_p99
    threshold: 2
    action: "o'qish marshrutlashni qayta ko'rish"
  - date: 2027-01-15
    action: "farazlarni real raqamlar bilan solishtirish"
owner: orders-team
status: accepted
```

Chegaralar kuzatuvga ulanmasa, bu fayl o'lik hujjat. Har bir trigger uchun dashboard paneli yoki alert bo'lishi kerak. Kuzatuv tomoni dizayn patternlar hujjatidagi observability bo'limida ko'rilgan.

### 1.9 Kod yozmaydigan arxitektor nega haqiqatdan uzoqlashadi

Diagrammada har bir strelka bir xil ko'rinadi. Kodda esa bitta strelka ikki qator, ikkinchisi ikki haftalik ish bo'ladi. Kod yozmaydigan arxitektor shu farqni ko'rmaydi, shuning uchun smetasi muntazam xato bo'ladi.

Ikkinchi sabab: ramkalarning haqiqiy xatti-harakati hujjatdan farq qiladi. `@Transactional` bitta sinf ichidagi chaqiruvda ishlamasligi, lazy collection ni tranzaksiyadan tashqarida o'qish `LazyInitializationException` berishi, `@Async` metodining self-invocation da proxy dan o'tmasligi hammasi shunday detallar. Bu detallar arxitektura qarorini o'zgartiradi, chunki ular jamoaning kunlik tezligiga ta'sir qiladi.

Uchinchi sabab: ishonch. Jamoa o'zi bilan bir kodga tegadigan odamning qaroriga boshqacha qaraydi.

```java
// Arxitektor uchun "kichik detal" emas, qaror darajasidagi tuzoq.
@Service
public class OrderService {

    // Shu metod ichidagi self-invocation proxy dan o'tmaydi,
    // shuning uchun ikkinchi metodning tranzaksiyasi YARATILMAYDI.
    public void importBatch(List<OrderRequest> requests) {
        for (OrderRequest r : requests) {
            saveOne(r);          // @Transactional e'tiborsiz qoladi
        }
    }

    @Transactional
    public void saveOne(OrderRequest r) {
        // ...
    }
}
```

Bu kod sintaktik to'g'ri va mantiqan buzuq. Amaliy chegara shunday: haftada bir necha soat real kod, odatda eng xavfli yo'lning prototipi yoki murakkab PR ni chuqur ko'rib chiqish. Feature yetkazish emas, mexanikaga tegib turish.

### 1.10 O'z fikrlashini tekshirish uchun savollar ro'yxati

Quyidagi savollarning maqsadi javob topish emas, yashirin farazni ochish. Agar savolga raqam bilan javob bera olmasang, qaror hali tayyor emas.

Birinchi guruh, kontekst haqida. Bu qaror qaysi biznes maqsadiga xizmat qiladi. Kim bu tizimni bir yildan keyin qo'llab-quvvatlaydi. Jamoada bu texnologiyani ishlab ko'rgan odam bormi. Muddat qisqarsa, qaysi qism birinchi tashlab yuboriladi.

Ikkinchi guruh, narx haqida. Bu qaror nimani yaxshilaydi va nimani yomonlashtiradi. Yomonlashgan narsani qanday o'lchayman. Agar bu qaror xato bo'lsa, qaytarish qancha turadi va necha hafta oladi. Bu qaror operatsion yukni qancha oshiradi.

Uchinchi guruh, haqiqat haqida. Bu raqamni o'lchadimmi yoki taxmin qildimmi. Eng yomon holatda nima bo'ladi va tizim qanday degradatsiya qiladi. Agar yuk o'n baravar oshsa, birinchi nima sinadi. Bu qarorning farazi qachon eskiradi va kim buni sezadi.

To'rtinchi guruh, soddalik haqida. Bu komponentni olib tashlasam, nima buziladi. Shu natijani ikki baravar kam harakat bilan olish mumkinmi. Yangi odam bu yechimni bir kunda tushunadimi. Bu abstraksiyaning uchta real ishlatilish holati bormi yoki bittasi bormi.

### 1.11 Amalda qo'llash

- [ ] Hozirgi loyihangizning uchta eng muhim arxitektura qarorini bir sahifali ADR qilib yozing, har birida kontekst, alternativa va narx bo'lsin.
- [ ] Eng muhim uchta foydalanuvchi yo'li uchun p99 latency maqsadini raqamda belgilang va `management.metrics.distribution.slo` orqali o'lchovga ulang.
- [ ] `pg_stat_statements` dan eng qimmat o'nta so'rovni oling va har biri uchun `EXPLAIN (ANALYZE, BUFFERS)` rejasini tekshiring.
- [ ] HikariCP pool kattaligini taxmin bilan emas, yuk sinovi natijasi bilan asoslang va `connection-timeout` ni 2 sekundgacha tushiring.
- [ ] Loyihadagi qarorlarni "arzon qaytariladigan" va "qimmat qaytariladigan" ikki ro'yxatga ajratib, ikkinchisiga ko'proq tekshiruv vaqti ajratganingizni tasdiqlang.
- [ ] Har bir muhim ADR ga review trigger qo'shing: metrika chegarasi yoki sana, va unga alert yoki dashboard paneli bog'lang.
- [ ] Faqat bitta implementatsiyasi bo'lgan interfeyslarni toping va haqiqiy almashuv nuqtasi bo'lmaganlarini olib tashlang.
- [ ] Haftada ikki soatni real kodga ajratib, eng xavfli yo'lning prototipini yoki eng murakkab PR ni o'zingiz ko'rib chiqing.

## 2. Muammoni tushunish va to'g'ri savol berish (Understanding the Problem)

Arxitektorning eng qimmat xatosi kod yozishda emas, talabni tushunishda sodir bo'ladi. Noto'g'ri tushunilgan talab asosida yozilgan toza, test bilan qoplangan, chiroyli kod ham yaroqsiz. Shuning uchun arxitektorning ishi klaviaturadan emas, savoldan boshlanadi. Bu bob savolni qanday berish, javobni qanday o'lchanadigan shaklga aylantirish va qachon talabni umuman rad etish kerakligi haqida.

### 2.1 Talab ortidagi haqiqiy ehtiyojni topish

Biznes odatda talabni yechim shaklida aytadi, ehtiyoj shaklida emas. "Bizga hisobot sahifasida Excel eksport tugmasi kerak" degan gap talab emas, bu allaqachon tanlangan yechim. Arxitektor shu yerda to'xtab, "nima uchun" ni so'raydi. Birinchi javob: "chunki moliya bo'limi raqamlarni ko'rishi kerak". Ikkinchi "nima uchun": "chunki ular har oy bank o'tkazmalarini tizimdagi to'lovlar bilan solishtiradi". Uchinchi "nima uchun": "chunki o'tgan yil 400 ming so'mlik farq topilgan va kim javobgar ekani aniqlanmagan".

Mana haqiqiy ehtiyoj: solishtirish (reconciliation) va audit izi. Excel tugmasi uni qondirmaydi, faqat qo'lda ishlashni osonlashtiradi. To'g'ri yechim boshqa: har kuni avtomatik solishtirish, farqlar uchun alohida jadval va to'lov holati o'zgarishining o'zgarmas tarixi. Excel esa ikkinchi darajali xususiyat bo'lib qoladi.

Qo'shimcha foydali savollar: "hozir buni qanday hal qilib turasiz", "agar biz hech narsa qilmasak nima bo'ladi", "oxirgi marta bu muammo qachon yuz bergan va qancha turdi". Oxirgi savol eng kuchlisi, chunki u talabning narxini oshkor qiladi. Agar javob "aslida hali yuz bermagan" bo'lsa, demak siz hali mavjud bo'lmagan muammoni hal qilmoqchisiz.

### 2.2 Funksional va nofunksional talablarni ajratish

Funksional talab tizim nima qilishini aytadi. Nofunksional talab buni qanday qilishini aytadi. Ikkinchisi arxitekturani birinchisidan ko'ra ko'proq belgilaydi. "Buyurtma yaratiladi" talabi uchun oddiy monolit ham, event-driven tizim ham yaroqli. Lekin "buyurtma yaratish 99 foiz hollarda 200 ms dan tez bo'lsin va ombor servisi o'chganda ham ishlashi kerak" talabi sizni sinxron chaqiruvdan voz kechishga majbur qiladi.

Amalda nofunksional talabni arxitektor o'zi qazib oladi. Buning uchun har bir funksional talabga olti o'lchov bo'yicha savol beriladi.

| O'lchov | Savol | To'lov servisi uchun misol javob |
|---|---|---|
| Tezlik | Qancha kutish mumkin | p99 < 300 ms, p999 < 1 s |
| Hajm | Kunda necha marta | 80 ming to'lov, peak soatda 12 ming |
| Ishonchlilik | Yo'qolsa nima bo'ladi | Hech bir to'lov yo'qolmasin, takror o'tkazma bo'lmasin |
| Ma'lumot yangiligi | Eski ma'lumot yaraydimi | Balans aniq, hisobot 15 daqiqa kechikishi mumkin |
| Xavfsizlik | Kim ko'rishi mumkin | Karta raqami log'ga tushmasin, PCI doirasi toraytirilsin |
| Narx | Oyiga qancha turadi | Infratuzilma 500 dollardan oshmasin |

"Hech bir to'lov yo'qolmasin" talabi texnik tilga tarjima qilinsa, ikki aniq qarorga olib keladi. Birinchisi: to'lov holati biznes tranzaksiyasi bilan bir atomik yozuvda saqlanadi. Ikkinchisi: tashqi tizimga xabar yuborish o'sha tranzaksiya ichida emas, keyin bajariladi. Bu dizayn patternlar hujjatidagi outbox pattern hududi. Arxitektor uni shu yerda nomlaydi, lekin tushuntirib o'tirmaydi.

### 2.3 Noaniq talabni o'lchanadigan talabga aylantirish

"Tez bo'lsin" talabi qabul qilinmaydi, chunki uni hech kim tekshira olmaydi. Uni o'lchanadigan shaklga aylantirish uchun to'rt narsa kerak: metrika, persentil, qiymat va o'lchash nuqtasi. "Buyurtma yaratish endpoint'i p99 latency'si 300 ms dan kam bo'lsin, server tomonda, 30 daqiqalik oynada, peak trafikda" degan gap allaqachon shartnoma.

Persentilni tanlash muhim. O'rtacha qiymat (mean) sekin so'rovlarni yashiradi: 1000 so'rovdan 990 tasi 50 ms, 10 tasi 5 s bo'lsa, o'rtacha 99 ms chiqadi va grafik sog'lom ko'rinadi, p99 esa 5 s ko'rsatadi. Agar bitta sahifa 20 ta so'rov qilsa, 300 ms lik p99 foydalanuvchining 18 foizi sekin sahifa ko'rishini bildiradi. Shuning uchun p999 ni ham belgilash kerak.

```yaml
# Spring Boot 3.x: SLO ni metrikaga aylantirish
management:
  endpoints:
    web:
      exposure:
        include: health,metrics,prometheus
  metrics:
    distribution:
      # histogram bo'lmasa persentilni Prometheus tomonda hisoblab bo'lmaydi
      percentiles-histogram:
        http.server.requests: true
      # SLO chegaralari: shu bucket'lar aniq sanaladi
      slo:
        http.server.requests: 100ms,300ms,1s
      # mijoz tomonda ko'rinadigan persentillar
      percentiles:
        http.server.requests: 0.95,0.99,0.999
```

Faqat HTTP latency'ni emas, biznes metrikasini ham o'lchash kerak. "To'lov tasdiqlanishi" bir nechta HTTP so'rovni qamrab oladigan biznes hodisasi.

```java
// To'lov oqimining uchidan uchiga vaqti: biznes SLO si
@Service
public class PaymentConfirmationService {

    private final Timer confirmationTimer;

    public PaymentConfirmationService(MeterRegistry registry) {
        this.confirmationTimer = Timer.builder("payment.confirmation.duration")
                .description("To'lov yaratilgandan tasdiqlangangacha")
                .publishPercentileHistogram()      // persentil uchun zarur
                .serviceLevelObjectives(Duration.ofSeconds(3))
                .register(registry);
    }

    public void onConfirmed(Payment payment) {
        // createdAt biznes hodisasi vaqti, so'rov boshi emas
        Duration elapsed = Duration.between(payment.getCreatedAt(), Instant.now());
        confirmationTimer.record(elapsed);
    }
}
```

O'lchash nuqtasi ham shartnomaning qismi. Server tomonda o'lchangan 200 ms mijoz brauzerida 900 ms bo'lishi mumkin, chunki orada TLS handshake, DNS va mobil tarmoq bor. Agar biznes "foydalanuvchi uchun tez" desa, server uchun budjet 300 ms emas, taxminan 120 ms bo'ladi.

```bash
# Tezlikni gapirmasdan oldin o'lchab ko'rish: eng arzon tekshiruv
curl -s -o /dev/null -w 'ulanish=%{time_connect}s tls=%{time_appconnect}s \
birinchi_bayt=%{time_starttransfer}s jami=%{time_total}s\n' \
  https://api.internal/orders/42

# Ma'lumotlar bazasi haqiqatan tor joy ekanini tekshirish
# 20 ta parallel ulanish, 60 sekund, faqat o'qish
pgbench -h db-host -U app -d orders -c 20 -j 4 -T 60 -S -P 10
```

### 2.4 Domenni o'rganish: umumiy til va event storming

Kod va suhbat bir xil so'zlardan foydalanmasa, har bir yig'ilish tarjimaga aylanadi. Biznes "yetkazib berish" deganda kod `ShipmentDto` ni, mijoz esa "qachon keladi" ni tushunadi. Umumiy til (ubiquitous language) shu uchlikni bitta so'zga bog'laydi va o'sha so'z klass nomiga aynan tushadi.

Eng ko'p uchraydigan belgi: bitta so'z ikki xil ma'noda ishlatiladi. "Buyurtma" savdo kontekstida savatcha va narx, ombor kontekstida yig'ish ro'yxati, moliyada esa hisob-faktura asosi. Uchalasi bitta `Order` klassiga siqilsa, o'sha klass 60 maydonga ega bo'ladi va hech kim uni o'zgartirishga jur'at etmaydi. To'g'ri qaror: uch kontekst, uch model, orada aniq tarjima.

```java
// Savdo konteksti: narx va mijoz muhim, ombor joylashuvi yo'q
public record SalesOrder(OrderId id, CustomerId customer,
                         List<OrderLine> lines, Money total) { }

// Ombor konteksti: joylashuv va miqdor muhim, narx yo'q
public record PickingList(OrderId id, WarehouseId warehouse,
                          List<PickTask> tasks, PickPriority priority) { }

// Tarjima faqat bitta joyda: anti-corruption layer
@Component
class SalesToWarehouseTranslator {
    PickingList toPickingList(SalesOrder order, WarehouseId wh) {
        // narx ombor modeliga o'tmaydi, shuning uchun bog'liqlik yo'qoladi
        var tasks = order.lines().stream()
                .map(l -> new PickTask(l.sku(), l.quantity()))
                .toList();
        return new PickingList(order.id(), wh, tasks, PickPriority.NORMAL);
    }
}
```

Event storming shu chegaralarni topishning eng tez usuli. Jarayon oddiy: devorga biznes hodisalarini o'tgan zamonda yozasiz ("to'lov tasdiqlandi", "tovar zahiraga olindi", "yetkazib berish bekor qilindi"), ularni vaqt bo'yicha tartiblaysiz, keyin har bir hodisadan oldin qaysi buyruq va qaysi qoida turganini aniqlaysiz. Ikki soatlik sessiya odatda 40 dan 80 ta hodisa beradi.

Natijada uch narsa ko'rinadi. Hodisalar zich to'planadigan joylar aggregate chegaralarini, oqim uziladigan joylar kontekst va kelajakdagi servis chegaralarini ko'rsatadi. Uchinchisi eng qimmati: hech kim javob bera olmaydigan savollar. "To'lov o'tgan, lekin tovar qolmagan bo'lsa nima qilamiz" savoliga javob yo'q bo'lsa, siz hali loyihani boshlashga tayyor emassiz.

### 2.5 Chegaraviy holatlar va istisnolarni oldindan topish

Baxtli oqim (happy path) kodning taxminan 20 foizini, chegaraviy holatlar qolganini egallaydi. Biznes faqat baxtli oqimni aytadi, qolganini arxitektor o'zi sanab chiqadi va har biriga qaror talab qiladi.

Ombor qoldig'i misolida sanoq shunday ko'rinadi. Noldan kam qoldiq bo'lishi mumkinmi. Ikki foydalanuvchi oxirgi bitta tovarni bir vaqtda olsa kim yutadi. Tovar zahiraga olingan, lekin to'lov 30 daqiqa kelmasa zahira qachon bo'shaydi. Buyurtma bekor qilingan, lekin tovar allaqachon yig'ilgan bo'lsa qoldiq qanday qaytadi. Inventarizatsiya natijasi tizim raqamidan farq qilsa qaysi biri haqiqat.

Bu savollarning har biri texnik qarorga aylanadi. "Noldan kam bo'lmasin" talabi baza darajasidagi cheklovga aylanadi, chunki faqat ilova kodidagi tekshiruv parallel so'rovlarda ishlamaydi.

```sql
-- Qoldiq manfiy bo'lmasligi: ilova kodiga ishonmaymiz
ALTER TABLE stock_item
  ADD CONSTRAINT stock_item_qty_non_negative
  CHECK (quantity_available >= 0);

-- Parallel kamaytirish: UPDATE o'zi qulflaydi, SELECT keyin UPDATE qilmaymiz
UPDATE stock_item
   SET quantity_available = quantity_available - 3
 WHERE sku = 'SKU-1042'
   AND quantity_available >= 3
RETURNING quantity_available;
-- 0 qator qaytsa, qoldiq yetmagan. Xatoga emas, biznes javobiga aylanadi.

-- Zahira muddati: osilib qolgan rezervlarni topish uchun indeks
CREATE INDEX stock_reservation_expiry_idx
    ON stock_reservation (expires_at)
 WHERE released_at IS NULL;
```

Ikkinchi yondashuv, ya'ni `SELECT` qilib, Java tomonda solishtirib, keyin `UPDATE` qilish, past izolyatsiya darajasida ikki parallel tranzaksiyada ikkisiga ham ruxsat beradi. PostgreSQL ning standart `READ COMMITTED` darajasi buni to'xtatmaydi. Bu mexanika tafsiloti, lekin talab tahlili bosqichida bilinishi kerak, chunki u talabni "oddiy tekshiruv" dan "atomik operatsiya" ga ko'taradi.

### 2.6 Hajm va o'sish taxmini

Har bir talab ortida raqam turadi va u raqam arxitekturani belgilaydi. Kunda 1000 ta buyurtma uchun bitta PostgreSQL instansi va oddiy jadval yetadi. Kunda 5 million buyurtma uchun partitioning, arxivlash va alohida o'qish nusxasi kerak. Bu ikki tizim bir xil kod bilan yozilmaydi.

Taxminni ikki raqam bilan yozish kerak: bugungi va uch yildan keyingi. Bir yil juda qisqa, unda hech qanday qaror o'zgarmaydi. Besh yil juda uzoq, biznes o'sha vaqtda boshqa ish qilayotgan bo'lishi mumkin.

```sql
-- Bugungi haqiqat: taxmin qilmasdan o'lchash
SELECT relname AS jadval,
       pg_size_pretty(pg_total_relation_size(c.oid)) AS jami_hajm,
       n_live_tup AS qatorlar
  FROM pg_class c
  JOIN pg_stat_user_tables s ON s.relid = c.oid
 WHERE c.relkind = 'r'
 ORDER BY pg_total_relation_size(c.oid) DESC
 LIMIT 10;

-- Bitta qator qancha joy oladi: o'sishni hisoblash uchun asos
SELECT pg_total_relation_size('payment') / NULLIF(count(*), 0) AS bayt_per_qator
  FROM payment;
```

Hisob oddiy. Bitta to'lov qatori indekslar bilan taxminan 400 bayt olsa va kunda 80 ming to'lov bo'lsa, bu kuniga 32 MB, yiliga taxminan 11 GB. Uch yilda 35 GB, o'sish uch barobar bo'lsa 70 GB. Bu bitta serverda muammosiz saqlanadi, ya'ni sharding haqida o'ylash shart emas. Lekin sana bo'yicha hisobot so'rovlari bo'lsa, oylik partitioning asoslanadi: eski partitionlar sovuq saqlashga ko'chadi va `VACUUM` ishi engillashadi.

Xotira hisobi ham shunday. 2000 ta sessiya, har biri 20 KB bo'lsa, bu 40 MB heap va muammo emas. Lekin har bir sessiyada 500 elementli savatcha cache'lansa, raqam taxminan 400 MB ga chiqadi va bu JVM uchun sezilarli.

### 2.7 Kim foydalanadi: tashqi foydalanuvchi, ichki jamoa, boshqa servis

Foydalanuvchi turi API dizaynini, xatolik strategiyasini va mustahkamlik darajasini butunlay o'zgartiradi. Bitta endpoint uchun uch xil iste'molchi uch xil talab qo'yadi.

Tashqi mobil ilova sekin tarmoqda ishlaydi, shuning uchun so'rov soni kam, javob kichik va retry ko'p bo'ladi. Bu idempotentlikni majburiy qiladi. Ichki admin paneli trafikni kam beradi, lekin og'ir filtrlar va eksport so'raydi, demak bu so'rovlar o'qish nusxasiga yo'naltiriladi. Boshqa servis sekundda minglab so'rov yuboradi va xatoni ko'rganda darhol qayta urinib tizimni yiqitadi, shuning uchun unga rate limit va aniq xato semantikasi kerak.

```java
// Idempotentlik: tashqi mijoz retry qilsa ikkinchi to'lov yaratilmasin
@PostMapping("/payments")
public ResponseEntity<PaymentResponse> create(
        @RequestHeader("Idempotency-Key") String key,
        @Valid @RequestBody CreatePaymentRequest request) {

    // Kalit bo'yicha unique index bazada: ikkinchi INSERT xato beradi
    var result = paymentService.createOrGet(key, request);

    // Takroriy so'rovga 201 emas, 200 qaytaramiz: mijoz farqni bilsin
    return result.created()
            ? ResponseEntity.status(HttpStatus.CREATED).body(result.payload())
            : ResponseEntity.ok(result.payload());
}
```

Iste'molchi turini bilish versiyalash qarorini ham belgilaydi. Ichki jamoa uchun API ni bugun o'zgartirib, ertaga ikki chaqiruvchini tuzatish mumkin. Tashqi mobil ilova uchun bu imkonsiz, chunki eski versiya telefonlarda yillab yashaydi va majburiy yangilanish mijozni yo'qotadi. Shuning uchun "kim foydalanadi" savoliga javob "tashqi mobil" bo'lsa, orqaga moslik qoidasi birinchi kundan kuchga kiradi.

### 2.8 Muvaffaqiyat mezoni va uni qanday o'lchash

Talab tugagan deb hisoblanishi uchun uch narsa aniq bo'lishi kerak: qaysi raqam o'zgaradi, qancha o'zgaradi va qachon tekshiriladi. "Hisobot tezlashsin" mezon emas. "Oylik moliya hisoboti hozir 14 daqiqa ishlaydi, maqsad 2 daqiqadan kam, 1 million qatorli ma'lumotda, ishga tushirilgandan keyin birinchi oy oxirida o'lchanadi" mezon.

Mezon faqat texnik bo'lmaydi. Biznes mezoni ko'pincha muhimroq. "Qo'lda solishtirish uchun ketadigan vaqt oyiga 16 soatdan 1 soatga tushsin" degan gap loyihaning qiymatini bevosita ko'rsatadi va u loyihani himoya qilish uchun eng yaxshi argument.

Har bir mezonga o'lchash usuli yozilishi kerak, aks holda u shiorga aylanadi. "Ma'lumot yo'qolmasin" mezoni uchun o'lchash usuli bu tunda ishlaydigan solishtirish jarayoni: u tashqi va ichki yozuvlarni sanab taqqoslaydi, farq nolga teng bo'lmasa ogohlantiradi. Shu o'lchov bo'lmasa, siz bilmaysiz, faqat ishonasiz.

Testlash qo'llanmasidagi performance test bo'limi shu mezonlarni avtomatik darvozaga aylantirish usulini beradi. Arxitektorning bu yerdagi ishi boshqa: mezonni shunday yozish, uni mashinani o'qiydigan shaklga aylantirish mumkin bo'lsin.

### 2.9 Noto'g'ri tushunishning narxi

Talabni noto'g'ri tushunish narxi chiziqli emas, ko'rsatkichli o'sadi. Savollar bosqichida tuzatish bir soat, dizaynda bir kun, ishlab chiqarishda esa oylar oladi, chunki o'sha paytga kelib ma'lumot noto'g'ri sxemada yotadi.

Eng qimmat uch xato turi bor. Yaroqsiz sxema: to'lov summasini `double` saqlash qarori arzon ko'rinadi, lekin million qatorda tiyin yo'qolganini topganda migratsiya haftalab davom etadi. Keraksiz servis: "kelajakda kerak bo'ladi" taxmini bilan ajratilgan servis har bir yangi xususiyatga ikki deploy va taqsimlangan tranzaksiya muammosini qo'shadi. Noto'g'ri chegara: agregat chegarasi xato qo'yilsa, har bir operatsiya bir necha agregatga tegadi va lock contention yuzaga keladi.

| Holat | Oddiy yondashuv | Arxitektor yondashuvi |
|---|---|---|
| Biznes yechim aytdi | Aytganini kodlaydi | Uch marta "nima uchun" so'rab, ehtiyojni topadi |
| "Tez bo'lsin" talabi | Keyinroq optimallashtiramiz deydi | p99 va o'lchash nuqtasini shartnomaga yozadi |
| Hajm noma'lum | Standart sozlama bilan ketadi | Bugungi va uch yillik raqamni hisoblaydi |
| Chegaraviy holat | Birinchi bug hisobotida bilib oladi | Oldindan 10 ta holatni sanab, har biriga qaror oladi |
| Domen so'zlari | Dto va Entity deb nomlaydi | Biznes so'zini klass nomiga aynan ko'chiradi |
| Yangi ehtiyoj paydo bo'ldi | Yangi servis ajratadi | Avval mavjud chegara ichida sinab ko'radi |
| Iste'molchi turi | Hamma uchun bitta API | Tashqi, ichki va servis uchun alohida shartnoma |
| Muvaffaqiyat | Vazifa yopilsa tugadi deydi | Raqam o'zgarganini o'lchab tasdiqlaydi |
| Qamrov o'sdi | Hammasini sig'dirishga urinadi | Kesib tashlaydi va nimadan voz kechganini yozadi |
| Qoldiq manfiy bo'lmasligi | Java tomonda if bilan tekshiradi | Baza cheklovi va atomik UPDATE bilan ta'minlaydi |

| Tuzoq | Nimaga olib keladi | Yechim |
|---|---|---|
| Pul uchun `double` | Tiyin yo'qoladi, hisobot farq qiladi | `BigDecimal` yoki `numeric(19,4)`, scale aniq belgilanadi |
| Vaqtni mahalliy zonada saqlash | Yozgi vaqt o'tishida qatorlar takrorlanadi | `timestamptz` va UTC, ko'rsatishda zona qo'llanadi |
| "Nima uchun" so'ralmagan | Keraksiz xususiyat yozildi | Talab bilan biznes natijasi orasida bog'liqlik talab qilinadi |
| O'rtacha latency ni mezon qilish | Sekin so'rovlar yashirinadi | p99 va p999, histogram yoqilgan holda |
| Hajm taxminsiz sxema | Bir yildan keyin majburiy migratsiya | Qator hajmi va yillik o'sish oldindan hisoblanadi |
| Bitta `Order` hamma kontekst uchun | 60 maydonli klass, hech kim o'zgartirmaydi | Kontekstga ko'ra alohida model va tarjima qatlami |
| Idempotentlik yo'q | Mijoz retry qilganda ikki marta to'lov | Idempotency kaliti va unique cheklov |
| Chegaraviy holat kechiktirildi | Ishlab chiqarishda ma'lumot buziladi | Talab bosqichida holatlar ro'yxati va qarorlar |

### 2.10 Talabni rad etish va qamrovni qisqartirish san'ati

Arxitektorning eng kuchli vositasi "yo'q" so'zi, lekin quruq rad etish ishonchni buzadi. To'g'ri shakl uch qismdan iborat: ehtiyojni tan olish, narxni ko'rsatish va arzonroq alternativa taklif qilish.

Misol. Biznes real vaqtda yangilanadigan omborlar dashboard'ini so'raydi. Rad etish shunday ko'rinadi: "Qoldiqni kuzatish kerakligini tushunaman. Real vaqtda yangilanish WebSocket infratuzilmasi, alohida o'qish modeli va taxminan uch hafta ish talab qiladi. Boshqa variant: 30 sekundda bir yangilanadigan sahifa, bu ikki kunlik ish. Agar 30 sekund yetmasa, qaysi qaror shuncha tez qabul qilinishi kerakligini aytsangiz, shu oqim uchun alohida real vaqt kanali qilamiz."

Bu javobda hurmat, raqam va tanlov bor. Biznes odatda ikkinchi variantni oladi, chunki haqiqiy ehtiyoj 30 sekundlik yangilanish bilan qoplanadi.

Qamrovni qisqartirishning foydali usuli: talabni "birinchi relizda kerak", "uchinchi oyda kerak" va "hech qachon kerak bo'lmasligi mumkin" guruhlariga ajratish. Oxirgi guruhga tushgan talablar yozilib qo'yiladi, lekin bajarilmaydi. Uch oydan keyin ularning aksariyati o'z-o'zidan yo'qoladi va bu eng arzon yechim.

Rad etilgan talabni yozib qo'yish majburiy. Qaror hujjatida (ADR) "nimadan voz kechdik va nima uchun" bo'limi bo'lsin. Oltinchi oyda kimdir "nega bu yo'q" deb so'raganda, javob repozitoriyda turadi.

Oxirgi qoida: talabni tushunishga ikki haftadan ko'p vaqt ketsa, talab juda katta va bo'laklarga ajratilishi kerak. Bo'linmaydigan talab odatda yaxshi tushunilmagan talab.

### 2.11 Amalda qo'llash

- [ ] Hozirgi backlog'dagi eng katta uch talabni oling va har biriga uch marta "nima uchun" savolini berib, javoblarni bir betga yozing.
- [ ] Har bir talab uchun olti o'lchov jadvalini (tezlik, hajm, ishonchlilik, ma'lumot yangiligi, xavfsizlik, narx) to'ldiring va bo'sh qolgan katakchalarni biznesdan so'rang.
- [ ] Eng muhim ikki endpoint uchun p99 va p999 qiymatini belgilab, `percentiles-histogram` va `slo` sozlamalarini yoqing, keyin bir hafta haqiqiy raqamni kuzatib SLO ni to'g'rilang.
- [ ] Eng katta uch jadvalning hozirgi hajmini va bitta qator o'rtacha bayt hajmini o'lchab, uch yillik o'sish prognozini yozib qo'ying.
- [ ] Bitta asosiy biznes oqimi uchun kamida 10 ta chegaraviy holatni sanab chiqing va har biriga qaror yozing, qarorsiz qolganini xavf ro'yxatiga kiritasiz.
- [ ] Ikki soatlik event storming sessiyasini o'tkazing va natijada paydo bo'lgan javobsiz savollarni alohida ro'yxatga oling.
- [ ] Kodingizdagi eng katta entity'ni oling va unda necha xil kontekst aralashganini aniqlang, kamida bitta kontekstni alohida modelga ajratish rejasini yozing.
- [ ] Rad etilgan yoki kechiktirilgan talablar uchun ADR shabloniga "nimadan voz kechdik" bo'limini qo'shib, oxirgi uch qarorni retrospektiv yozib chiqing.

## 3. Qaror qabul qilish va uni hujjatlashtirish (Decisions and ADRs)

Arxitektorning asosiy mahsuloti kod emas, qaror. Kod qaytarilishi mumkin, qaror esa jamoaning keyingi ikki yilini belgilaydi. Qaror yozilmasa, u yo'q: olti oydan keyin "nega bu yerda Kafka turibdi" degan savolga javob beradigan hujjat kerak. Bu bob qarorni qanday pishitish, qanday yozib qo'yish va keyin uning natijasini qanday kuzatish haqida.

### 3.1 ADR (Architecture Decision Record) tuzilishi: kontekst, qaror, oqibat, holat

ADR bitta qarorni tasvirlaydigan qisqa fayl. U loyiha hujjati emas, tarix yozuvi: bir marta yoziladi va keyin o'zgartirilmaydi, faqat holati almashadi. To'rtta majburiy qismi bor. Kontekst: qaror paytidagi haqiqat, raqamlar bilan. Qaror: bitta gap, "biz X ni tanlaymiz" shaklida. Oqibat: nimani qo'lga kiritdik va nimani yo'qotdik, ikkinchisi birinchisidan muhimroq. Holat: Taklif qilindi, Qabul qilindi, Rad etildi, Eskirdi yoki O'rnini bosdi.

Eng ko'p xato qilinadigan joy kontekst. "Tizim tez ishlashi kerak" kontekst emas. "Buyurtma qidiruvi p95 da 1.8 soniya, maqsad 300 ms, kunlik qidiruv soni taxminan 40 ming, baza hajmi 180 GB" kontekst. Kontekst o'qilganda qaror o'z-o'zidan kelib chiqishi kerak. Agar o'qiganingizda "unda nega boshqasini tanlamadilar" degan savol tug'ilsa, kontekst to'liq emas.

Oqibat bo'limi ADR ni boshqa hujjatdan ajratib turadi. Har bir qaror narx bilan keladi va bu narxni oldindan yozib qo'yish keyin "bizni hech kim ogohlantirmagan" deyishning oldini oladi. Qaytarish narxini ham shu yerga yozing: bir haftalik ish bo'ladimi yoki uch oylik migratsiya.

```markdown
# ADR-0042: <Qaror sarlavhasi, fe'l bilan>

- Holat: Taklif qilindi | Qabul qilindi | Rad etildi | Eskirdi | O'rnini bosdi
- Sana: 2026-03-11
- Qaror egasi: <ism>, ishtirokchilar: <jamoa>
- Qayta ko'rish sanasi: 2026-09-01
- Bog'liq ADR: ADR-0012 (o'rnini bosadi)

## Kontekst
Majburlovchi holat raqamlar bilan: latency, hajm, o'sish, muddat, cheklovlar.

## Qaror
Biz <X> ni tanlaymiz.

## Ko'rib chiqilgan variantlar
1. <Variant A>: rad etildi, sababi ...
2. <Variant B>: rad etildi, sababi ...

## Oqibatlar
- Ijobiy: ...
- Salbiy: ...
- Qaytarish narxi: <taxminan N kun / N oy>

## Taxminlar
- T1: <taxmin>. Tekshirish usuli: <o'lchov>. Muddat: <sana>.

## Kuzatiladigan metrika
- <metrika nomi>, hozirgi qiymat, maqsad qiymat, dashboard havolasi
```

| Masala | Oddiy yondashuv | Arxitektor yondashuvi |
|---|---|---|
| Qaror sababi | Chat xabarida qoladi | Repoda ADR fayli, kontekst raqamlari bilan |
| Variantlar | Bitta tanlangan variant aytiladi | Rad etilganlar va rad sababi yoziladi |
| Oqibat | Faqat foyda sanaladi | Narx, cheklov va qaytarish narxi yoziladi |
| Taxminlar | Boshda qoladi | Yozib qo'yiladi va tekshirish muddati beriladi |
| Qaror vaqti | Sprint boshida hammasi hal qilinadi | Oxirgi mas'ul daqiqaga qoldiriladi |
| Ma'lumot | "Men shunday o'ylayman" | Spike natijasi, EXPLAIN chiqishi, yuklama testi |
| Kelishmovchilik | Ovoz berish yoki eng baland ovoz | Yozma e'tiroz, qaror egasi, bajarish majburiyati |
| Natija | Deploy dan keyin unutiladi | Metrika va qayta ko'rish sanasi bilan kuzatiladi |
| Eskirgan qaror | Hujjat jimgina o'zgartiriladi | Yangi ADR yoziladi, eskisi "O'rnini bosdi" bo'ladi |

### 3.2 Variantlarni taqqoslash: mezon jadvali va og'irlik berish

Taqqoslashni jadvalga aylantirish muhokamani fikrdan mezonga ko'chiradi. Mezonlarni variantlarni ko'rib chiqishdan OLDIN yozing, aks holda mezonlar o'zingiz yoqtirgan variantga moslashib qoladi. Har bir mezonga og'irlik bering: yig'indisi 100 bo'lsin. Og'irlik haqidagi tortishuv eng foydalisi, chunki u yashirin ustuvorliklarni ochadi.

Ball bering, lekin ballga ishonib qolmang. Jadval qarorni chiqarmaydi, u qaror qayerda tug'ilishini ko'rsatadi. Agar bir variant 71, ikkinchisi 69 ball olsa, bu "tenglik" degani: unda ikkinchi darajali omil, masalan jamoaning tajribasi yoki qaytarish narxi hal qiladi. Agar farq 20 balldan oshsa, muhokamani yoping.

| Mezon | Og'irlik | PostgreSQL FTS | Alohida qidiruv tizimi |
|---|---|---|---|
| Qidiruv sifati (tilga mos, ranking) | 25 | 3 | 5 |
| p95 latency 300 ms ga sig'ishi | 20 | 4 | 5 |
| Operatsion murakkablik | 20 | 5 | 2 |
| Ma'lumot izchilligi | 15 | 5 | 2 |
| Jamoa tajribasi | 10 | 5 | 3 |
| 12 oylik umumiy narx | 10 | 5 | 3 |
| Og'irlangan yig'indi (100 dan) | | 85 | 72 |

### 3.3 Oxirgi mas'ul daqiqa (last responsible moment) tamoyili

Har bir qarorni iloji boricha kechiktirish kerak degan fikr noto'g'ri tushuniladi. Tamoyil "kechiktir" demaydi, "qaror qilmaslik qimmatga tusha boshlagan daqiqada qaror qil" deydi. Bu daqiqani topish uchun ikki narxni taqqoslaysiz: kutish narxi va erta qaror narxi. Kutish narxi bu to'siqdagi jamoa, vaqtincha yechim va ikki marta yoziladigan kod. Erta qaror narxi bu noto'g'ri tanlovni keyin yechib tashlash.

Amalda bu shunday ko'rinadi. Buyurtma servisida "qanday message broker" savolini birinchi sprintda hal qilish shart emas, agar siz hodisani chiqarishni interfeys orqasiga yashirgan bo'lsangiz va dizayn patternlar hujjatidagi outbox pattern ni qo'llagan bo'lsangiz. Lekin "buyurtma identifikatori UUID bo'ladimi yoki bigint" savolini kechiktirish mumkin emas: u sxemaga, indeks hajmiga va tashqi integratsiyaga kirib ketadi, bir hafta o'tgach o'zgartirish migratsiya bo'ladi.

Qoida sifatida: ma'lumot sxemasi, identifikator turi, tranzaksiya chegaralari va autentifikatsiya modeli erta qaror qilinadi, chunki ularning qaytarish narxi vaqt bilan tez o'sadi. Cache qatlami, qidiruv tizimi, broker tanlovi va deployment topologiyasi esa kechiktirilishi mumkin, chunki ular interfeys orqasida turadi. ADR da "nega hozir" degan bir qatorni yozib qo'ying: bu qaror vaqtini ham hujjatlashtiradi.

### 3.4 Taxminlarni yozib qo'yish va keyin ularni tekshirish

Har bir qaror ostida tekshirilmagan taxminlar yotadi. "Kunlik buyurtma soni 50 mingdan oshmaydi", "hisobot kechikishi 5 daqiqa bo'lishi mumkin", "ombor qoldig'i faqat bitta mintaqada o'zgaradi". Bu taxminlar yozilmasa, ular haqiqatga aylanib qoladi va keyin hech kim ularni shubha ostiga olmaydi.

Har bir taxminga uch narsa biriktiring: qanday o'lchanadi, qachon tekshiriladi, buzilsa nima qilinadi. Uchinchisi eng qimmatli: "agar kunlik buyurtma 200 mingdan oshsa, partitsiyalashga o'tamiz" degan qator keyingi arxitektorga tayyor yo'l xaritasi beradi.

Taxminni o'lchash ko'pincha bitta so'rov bilan hal bo'ladi. Ishlab chiqarish bazasida o'sish tezligini ko'rish uchun quyidagicha yozing, keyin natijani ADR ga nusxa qiling.

```sql
-- Taxmin T1: kunlik buyurtma soni 50 mingdan oshmaydi.
-- Oxirgi 90 kunning kunlik hajmi va o'sish trendi.
SELECT date_trunc('day', created_at)::date AS kun,
       count(*)                            AS buyurtma_soni,
       pg_size_pretty(sum(pg_column_size(o.*))) AS taxminiy_hajm
FROM orders o
WHERE created_at >= now() - interval '90 days'
GROUP BY 1
ORDER BY 1 DESC
LIMIT 10;

-- Jadval va indeks hajmi: qidiruv indeksi qancha joy egallaydi.
SELECT relname,
       pg_size_pretty(pg_relation_size(oid))       AS jadval,
       pg_size_pretty(pg_indexes_size(oid))        AS indekslar
FROM pg_class
WHERE relname IN ('orders', 'order_items')
  AND relkind = 'r';
```

Taxminni tekshirishni odamning esiga tayanib qoldirmang. Agar taxmin raqam bo'lsa, uni metrikaga aylantirib, chegara o'tilganda signal bering. Shunda taxmin o'z-o'zini tekshiradi.

### 3.5 Spike va prototip: qarorni ma'lumot bilan quvvatlash

Spike bu vaqti chegaralangan tadqiqot: maqsadi mahsulot emas, javob. Spike ni boshlashdan oldin uch narsani yozing: qaysi savolga javob izlayapmiz, qancha vaqt beramiz, qanday natija javob hisoblanadi. Vaqt chegarasi bo'lmasa spike loyihaga aylanadi. Odatda ikki kundan besh kungacha yetadi.

Spike kodi tashlab yuboriladi va bu ataylab shunday. Agar spike kodi ishlab chiqarishga ketsa, u prototip emas, shoshilib yozilgan tizim. Prototip esa boshqa narsa: u ishlab chiqarish yo'liga kiradigan, lekin cheklangan qamrovdagi haqiqiy kod. Spike dan prototipga o'tish ham qaror va u ADR da aks etishi kerak.

Qidiruv qarori uchun spike shunday ko'rinadi: haqiqiy ma'lumotning nusxasini oling, indeks quring, o'nta tipik so'rovni o'lchang. Sun'iy ma'lumotda o'lchash behuda, chunki PostgreSQL planner statistikaga qarab boshqa plan tanlaydi.

```sql
-- Spike S-07: PostgreSQL full text search 300 ms ga sig'adimi.
-- 1. Generated ustun va GIN indeks.
ALTER TABLE orders
  ADD COLUMN search_doc tsvector
  GENERATED ALWAYS AS (
    to_tsvector('simple',
      coalesce(customer_name, '') || ' ' ||
      coalesce(order_number, '') || ' ' ||
      coalesce(notes, ''))
  ) STORED;

CREATE INDEX CONCURRENTLY idx_orders_search
  ON orders USING gin (search_doc);

-- 2. Haqiqiy so'rovni o'lchash. Buffer va vaqt bilan.
EXPLAIN (ANALYZE, BUFFERS)
SELECT id, order_number, created_at,
       ts_rank(search_doc, q) AS reyting
FROM orders, websearch_to_tsquery('simple', 'alisher toshkent') q
WHERE search_doc @@ q
ORDER BY reyting DESC, created_at DESC
LIMIT 20;
```

Natijani o'qiyotganda ikki raqamga qarang: Execution Time va shared read bloklari soni. Agar plan Bitmap Index Scan ko'rsatsa va bloklar soni cache ga sig'sa, bu yondashuv ishlaydi. Agar Seq Scan qolsa yoki ORDER BY katta natija to'plamini saralashga majbur qilsa, raqam yuklama ostida yomonlashadi.

### 3.6 Jamoadagi kelishmovchilik va "rozi emasman, lekin bajaraman" qoidasi

Texnik kelishmovchilik normal holat va uni yo'q qilishga urinish eng yomon strategiya. Yo'q qilinishi kerak bo'lgan narsa boshqa: hal bo'lmagan kelishmovchilikning kodda ikki xil uslub sifatida qotib qolishi. Shuning uchun har bir qarorga egasi tayinlanadi. Ega ovoz yig'maydi, u fikrlarni eshitib qaror chiqaradi va natija uchun javob beradi.

Qoida oddiy: muhokama ochiq, qaror yopiq. Muhokama davrida har kim e'tirozini yozma shaklda, ADR ga izoh sifatida qo'yishi kerak. Yozma e'tiroz og'zakisidan foydaliroq, chunki u aniq bo'lishga majbur qiladi: "menga yoqmaydi" dan "bu yondashuvda hisobot so'rovi asosiy bazaga yuk beradi" ga o'tadi. Qaror chiqqandan keyin esa "rozi emasman, lekin bajaraman" qoidasi kuchga kiradi. Ya'ni e'tiroz yozib qoldiriladi, lekin hamma bir xil qarorni bajaradi va unga qarshi ishlamaydi.

Bu qoidaning ikkita sharti bor. Birinchisi: e'tiroz ADR da ko'rinadigan joyda qoladi, "Rad etilgan e'tirozlar" bo'limida. Ikkinchisi: qayta ko'rish sanasi belgilanadi. Agar e'tiroz egasi haq bo'lsa, oradan olti oy o'tib metrika buni ko'rsatadi va ADR qayta ochiladi. Shu ikki shart bo'lsa, jamoa qarorni osonroq qabul qiladi: fikr yo'q qilinmagan, navbatga qo'yilgan.

### 3.7 Qaror oqibatini kuzatish: metrika va qayta ko'rish sanasi

Kuzatilmagan qaror tekshirilmagan gipotezaga teng. ADR da kamida bitta metrika va bitta sana bo'lishi kerak. Metrika qarorning asosiy da'vosini o'lchasin: "qidiruv tezlashadi" degan qaror uchun qidiruv latency si o'lchanadi, umumiy CPU emas.

Metrikani kod yozilgan paytda joylashtiring, keyin emas. Micrometer bilan bu bir necha qatorlik ish va natijasi ADR ning haqiqiy nazoratchisi bo'ladi.

```java
@Service
public class OrderSearchService {
    private final Timer qidiruvVaqti;
    private final Counter boshNatija;
    private final OrderSearchRepository repository;

    public OrderSearchService(MeterRegistry registry, OrderSearchRepository repository) {
        this.repository = repository;
        // ADR-0042 metrikasi: p95 maqsad 300 ms.
        this.qidiruvVaqti = Timer.builder("order.search.duration")
                .description("Buyurtma qidiruvi davomiyligi")
                .publishPercentiles(0.5, 0.95, 0.99)
                .tag("engine", "postgres_fts")
                .register(registry);
        this.boshNatija = Counter.builder("order.search.empty")
                .register(registry);
    }

    public List<OrderView> search(String query, Pageable page) {
        return qidiruvVaqti.record(() -> {
            List<OrderView> natija = repository.search(query, page);
            if (natija.isEmpty()) {
                boshNatija.increment();  // sifat signali, tezlik emas
            }
            return natija;
        });
    }
}
```

Natijasiz qidiruvlar ulushi muhim, chunki tezlik yaxshilanib, sifat yomonlashishi mumkin. Qayta ko'rish sanasi kelganda uchta javobdan birini yozasiz: qaror o'zini oqladi, qaror qisman ishladi va tuzatish kerak, yoki qaror xato bo'ldi va yangi ADR yoziladi. Uchinchi javob eng qimmatli, lekin uni faqat sana va metrika bo'lgan jamoa chiqara oladi.

### 3.8 ADR ni repoda saqlash, raqamlash va eskirganini belgilash

ADR kod bilan bir repoda, `docs/adr/` papkasida yashashi kerak. Sababi oddiy: alohida wiki da turgan hujjat kod o'zgarganda yangilanmaydi, pull request ichidagi fayl esa review ga tushadi. Nom shabloni `NNNN-qisqa-sarlavha.md`, raqam to'rt xonali va ketma-ket. Raqamni qayta ishlatmang, hatto ADR rad etilgan bo'lsa ham: raqam tarixning bir qismi.

Eskirgan ADR o'chirilmaydi va tahrirlanmaydi. Uning holati `Eskirdi` yoki `O'rnini bosdi: ADR-0057` ga o'zgaradi va shu bitta qator qo'shiladi. Mazmuni esa o'sha paytdagi haqiqat sifatida qoladi. Keyingi odam "nega avval boshqacha edi" savoliga javob topadi, bu esa bir xil xatoning takrorlanishini to'xtatadi.

```bash
#!/usr/bin/env bash
# docs/adr/new.sh: keyingi ADR raqamini topib, shablondan fayl yaratadi.
set -euo pipefail

DIR="$(dirname "$0")"
LAST=$(ls "$DIR" | grep -E '^[0-9]{4}-' | sort | tail -n 1 | cut -c1-4)
NEXT=$(printf "%04d" $((10#${LAST:-0} + 1)))
SLUG=$(echo "$*" | tr '[:upper:] ' '[:lower:]-' | tr -cd 'a-z0-9-')

cp "$DIR/template.md" "$DIR/$NEXT-$SLUG.md"
sed -i "s/ADR-0000/ADR-$NEXT/; s/<SANA>/$(date +%F)/" "$DIR/$NEXT-$SLUG.md"
echo "Yaratildi: $DIR/$NEXT-$SLUG.md"
```

CI da ikkita oddiy tekshiruv katta foyda beradi: har bir ADR da `Holat` qatori borligi va qayta ko'rish sanasi o'tgan ADR lar ro'yxatini chiqarish.

```yaml
# .github/workflows/adr-check.yml dagi qadamlar
- name: ADR holat qatori bormi
  run: |
    for f in docs/adr/[0-9]*.md; do
      grep -q '^- Holat:' "$f" || { echo "Holat yo'q: $f"; exit 1; }
    done

- name: Qayta ko'rish sanasi o'tgan ADR lar
  run: |
    BUGUN=$(date +%F)
    grep -H '^- Qayta ko.rish sanasi:' docs/adr/[0-9]*.md \
      | awk -v t="$BUGUN" -F': ' '$2 != "" && $2 < t {print "Muddati o-tdi: " $0}'
```

### 3.9 Yomon ADR belgilari: allaqachon qilingan ishni oqlash uchun yozilgan hujjat

Eng keng tarqalgan nosog'lom ADR bu keyin yozilgan oqlash hujjati. Uni tanib olish oson: unda bitta variant bor, salbiy oqibatlar bo'limi bo'sh yoki "jiddiy salbiy oqibat yo'q" deb yozilgan, va kontekstda birorta raqam yo'q. Bunday hujjat ma'lumot bermaydi, faqat qarorni muhokamadan himoya qiladi. Agar qaror chindan ham allaqachon qilingan bo'lsa, buni ochiq yozing: "Bu qaror 2025 yil dekabrda amalga oshirilgan, ADR retrospektiv yozilmoqda". Shu bir gap hujjatning ishonchini saqlaydi.

| Tuzoq | Nega xavfli | Yechim |
|---|---|---|
| Bitta variantli ADR | Muqobil ko'rib chiqilmaganini yashiradi | Kamida ikki rad etilgan variant va rad sababi |
| Salbiy oqibatsiz ADR | Narx yashiringan, keyin kutilmagan bo'lib chiqadi | "Salbiy" bo'limi bo'sh ADR review dan o'tmaydi |
| Raqamsiz kontekst | Qaror did asosida qilinganini bildiradi | Latency, hajm, QPS, muddat yoziladi |
| Eski ADR ni tahrirlash | Tarix yo'qoladi, sabab izi uziladi | Yangi ADR, eskisiga "O'rnini bosdi" |
| 20 betlik ADR | Hech kim o'qimaydi | Bir betga sig'sin, chuqur tahlil ilova havolasida |
| Sanasiz qayta ko'rish | Qaror hech qachon tekshirilmaydi | Majburiy maydon, CI tekshiradi |
| Egasi yo'q ADR | Javobgarlik tarqaladi | Bitta ism, jamoa nomi yetarli emas |
| Spike natijasiz qaror | Taxmin ma'lumot o'rniga qo'yiladi | EXPLAIN yoki yuklama testi natijasi ilova qilinadi |

### 3.10 To'liq misol: PostgreSQL da qolish yoki alohida qidiruv tizimi qo'shish qarori

Holat shunday. Buyurtma qidiruvi admin panelda ishlatiladi, kunlik taxminan 40 ming so'rov, `orders` jadvalida 42 million qator, jadval hajmi taxminan 180 GB. Hozirgi qidiruv `ILIKE '%...%'` bilan qurilgan va p95 da 1.8 soniya beradi. Maqsad 300 ms. Jamoa uch kishi, alohida infratuzilma injeneri yo'q. Spike S-07 natijasi: generated `tsvector` ustun va GIN indeks bilan p95 taxminan 90 ms, indeks hajmi taxminan 11 GB, yozish tezligi taxminan 7 foizga pasaydi.

```markdown
# ADR-0042: Buyurtma qidiruvini PostgreSQL FTS da qoldirish

- Holat: Qabul qilindi
- Sana: 2026-03-11
- Qaror egasi: A. Qoraev. Ishtirokchilar: order-platform jamoasi
- Qayta ko'rish sanasi: 2026-09-01

## Kontekst
42 mln qator, 180 GB, kunlik 40 ming qidiruv. ILIKE bilan p95 = 1.8 s,
maqsad 300 ms. Jamoa 3 kishi. Spike S-07: GIN + tsvector da p95 = 90 ms.

## Qaror
Qidiruvni PostgreSQL full text search ustida qoldiramiz.

## Ko'rib chiqilgan variantlar
1. Alohida qidiruv klasteri: eventual izchillik qo'shadi. 72/100 ball.
2. Faqat trigram (pg_trgm): opechatkaga chidamli, lekin ranking yo'q.

## Oqibatlar
- Ijobiy: yangi tizim yo'q, qidiruv tranzaksiya bilan izchil.
- Salbiy: morfologiya cheklangan, facet va fuzzy qidiruv zaif.
- Qaytarish narxi: taxminan 6 hafta (outbox bilan indeksga ko'chirish).

## Taxminlar
- T1: qidiruv hajmi 12 oyda 3 barobardan oshmaydi. O'lchov: QPS metrikasi.

## Kuzatiladigan metrika
- order.search.duration p95 < 300 ms, order.search.empty ulushi < 8%
```

Qaror sozlash bilan to'liq bo'ladi. Qidiruv so'rovi analitik xarakterda, shuning uchun uni alohida connection pool va qisqa statement timeout ortiga qo'yish kerak, aks holda bitta og'ir so'rov asosiy buyurtma oqimini to'sib qo'yadi.

```properties
# Qidiruv uchun alohida pool: asosiy oqimdan ajratilgan.
spring.datasource.search.hikari.maximum-pool-size=8
spring.datasource.search.hikari.connection-timeout=2000
spring.datasource.search.hikari.pool-name=search-pool

# Qidiruv so'rovi 1 soniyadan oshsa uzilsin, foydalanuvchi kutmasin.
spring.datasource.search.hikari.data-source-properties.options=-c statement_timeout=1000

# Hibernate ni bu pool da faqat o'qish uchun ishlatamiz.
spring.jpa.properties.hibernate.jdbc.fetch_size=50
```

Bu ADR nimani ko'rsatdi: tanlov "yaxshi texnologiya" bilan "yomon texnologiya" orasida emas edi. Tanlov jamoaning uch kishiligi, izchillik talabi va 90 ms spike natijasi orasida edi. Agar oradan bir yil o'tib facet qidiruv mahsulot talabiga aylansa, T2 taxmini buziladi, ADR-0042 "O'rnini bosdi" bo'ladi va yangi ADR alohida indeks hamda outbox orqali sinxronizatsiyani yozadi. Bu muvaffaqiyatsizlik emas, bu ADR ning maqsadga muvofiq ishlashi.

### 3.11 Amalda qo'llash

- [ ] `docs/adr/` papkasini va `template.md` shablonini repoga qo'shing, raqamlash skriptini ishga tushiring.
- [ ] Oxirgi 12 oyda qilingan eng katta uch qarorni retrospektiv ADR sifatida yozing va retrospektiv ekanini ochiq belgilang.
- [ ] Har bir ochiq ADR ga qaror egasining ismini va qayta ko'rish sanasini qo'ying, egasiz ADR ni merge qilmang.
- [ ] CI ga ikki tekshiruv qo'shing: `Holat` qatori majburiy, muddati o'tgan qayta ko'rish sanalari ro'yxati haftalik chiqsin.
- [ ] Keyingi arxitektura qarori uchun mezon jadvalini og'irliklar bilan variantlarni ko'rishdan OLDIN tuzing.
- [ ] Hozir muhokamada turgan bitta savolni spike ga aylantiring: savol, vaqt chegarasi va javob mezonini yozib qo'ying.
- [ ] Har bir qabul qilingan ADR uchun bitta Micrometer metrikasi va bitta alert chegarasini kod bilan birga joylashtiring.
- [ ] Jamoa bilan "rozi emasman, lekin bajaraman" qoidasini kelishib oling va rad etilgan e'tirozlarni ADR ichida saqlaydigan bo'lim qo'shing.

## 4. Kod - muloqot vositasi: nomlash, aniqlik, kognitiv yuk (Code as Communication)

Kod ikki marta ishlatiladi: bir marta kompilyator uchun, qolgan yuz marta odam uchun. Kompilyator uchun ishlaydigan kod yozish past bar, chunki buni statik tahlil ham tekshiradi. Arxitektor uchun asosiy savol boshqa: ertaga bu metodga kelgan, domenni bilmaydigan odam uni to'g'ri o'zgartira oladimi. Shu bobda kod yozishni muloqot kanali sifatida ko'rib chiqamiz, va shu kanalning o'tkazuvchanligini oshiradigan aniq qarorlarni sanab o'tamiz.

### 4.1 Kod yozishdan ko'ra o'qishga ko'p vaqt ketadi

To'lov servisining hayot sikliga qarang. `PaymentAuthorizationService` bir hafta yozildi, keyin uch yil davomida o'qildi: incident vaqtida, audit vaqtida, yangi to'lov provayderi qo'shilganda, PCI tekshiruvida. Amaliyotda bitta metodni o'zgartirish uchun uni o'qiydigan odam o'zgartirishdan taxminan 5-10 barobar ko'p vaqt o'qishga sarflaydi. Bu nisbat qoida chiqaradi: yozishni qiyinlashtirib o'qishni osonlashtiradigan har qanday almashuv foydali.

Shundan kelib chiqadigan amaliy qoidalar qisqa. Birinchi, qisqa nom yozish vaqtini tejaydi, lekin o'qish vaqtini oshiradi, demak yutqazadi. Ikkinchi, "aqlli" bir qatorli ifoda yozuvchiga zavq beradi, o'quvchini sekinlashtiradi. Uchinchi, kodni tushunish uchun debugger ishga tushirish kerak bo'lsa, bu kod muloqotda muvaffaqiyatsiz bo'lgan.

```java
// yomon: nima qaytadi, qanday tartibda, nega filter shunday - hammasi yashirin
public List<Object[]> proc(Long id, int t) {
    return repo.find(id, t).stream()
        .filter(r -> r[3] != null && ((Integer) r[2]) > 0)
        .sorted((a, b) -> ((Date) b[1]).compareTo((Date) a[1]))
        .toList();
}

// yaxshi: tur, nom va tartib kodning o'zida aytilgan
public List<SettledPayment> findSettledPayments(OrderId orderId, Period period) {
    return paymentRepository.findByOrder(orderId, period).stream()
        .filter(Payment::isSettled)          // faqat bank tomonidan yopilganlar
        .sorted(comparing(Payment::settledAt).reversed())  // yangi birinchi
        .map(SettledPayment::from)
        .toList();
}
```

### 4.2 Nomlash: domen tilidan nom olish

Yaxshi nom domen mutaxassisi aytadigan so'z bo'ladi. Ombor bo'limi "qoldiq", "rezerv", "yo'lda" deb gapiradi, shuning uchun kodda `availableQuantity`, `reservedQuantity`, `inTransitQuantity` bo'lishi kerak, `qty1` va `qty2` emas. Agar domen eksperti bilan suhbatda ishlatilgan so'z kodda yo'q bo'lsa, demak tarjima qatlami bor, va har bir tarjima xato manbasi.

Qisqartma eng qimmat tejamkorlik. `calcAmt`, `pmtSts`, `ordHdr` kabi nomlar har o'qishda ongda qayta ochiladi. Faqat domenda rasman qabul qilingan qisqartmalar qoladi: `IBAN`, `VAT`, `SKU`, `TTL`. Qolgan hamma joyda to'liq so'z yoziladi, chunki IDE yozishni o'zi tugatadi.

`Manager`, `Helper`, `Util`, `Processor`, `Data`, `Info` qo'shimchalari alohida tuzoq. `OrderManager` nima qiladi degan savolga javob yo'q, shuning uchun unga hamma narsa to'planadi va u 2000 qatorga yetadi. Nom javobgarlikni cheklamasa, sinf ham cheklanmaydi. Yechim: nomni fe'ldan yoki aniq roldan chiqarish. `OrderManager` o'rniga `OrderPlacement`, `OrderCancellation`, `OrderPricing`. `PaymentHelper` o'rniga `PaymentRetryPolicy` va `CardNumberMasker`.

| Mavzu | Oddiy yondashuv | Arxitektor yondashuvi |
|---|---|---|
| Sinf nomi | `OrderManager` hamma narsani yig'adi | `OrderPlacement`, `OrderCancellation` alohida |
| Metod nomi | `process(order)` | `reserveStockFor(order)` |
| Mantiqiy flag | `boolean flag` | `boolean stockAlreadyReserved` |
| Pul miqdori | `BigDecimal amount` | `Money amount` (valyuta bilan) |
| Xato belgisi | `return null` | `Optional<Invoice>` yoki domen xatosi |
| Izoh | kod nima qilishini takrorlaydi | nega shunday qilinganini yozadi |
| Metod imzosi | `save(Long, int, String)` | `save(OrderId, Quantity, WarehouseCode)` |
| Paket | `service`, `dto`, `util` | `order`, `payment`, `inventory` |
| Istisno | `throw new RuntimeException("err")` | `InsufficientStockException(sku, requested, available)` |
| Magic number | `if (status == 3)` | `if (status == OrderStatus.SHIPPED)` |

### 4.3 Kognitiv yuk: bir metodni tushunish uchun nechta narsa

Odamning ishchi xotirasi bir vaqtda taxminan 4-7 ta mustaqil elementni ushlab turadi. Metodni o'qiyotgan odam shu sig'imdan foydalanadi: har bir mahalliy o'zgaruvchi, har bir shart, har bir nomsiz shart bitta slot egallaydi. Metodda 12 ta o'zgaruvchi va 5 ta shart bo'lsa, o'quvchi sig'imdan chiqadi va qog'ozga yozib o'qishga o'tadi.

Shuning uchun amaliy o'lchov bor: metodga kirgandan keyin oxirigacha yodda tutish kerak bo'lgan narsalar sonini sanash. To'rtta yoki beshtadan ko'p bo'lsa, metodni bo'lish kerak. Bu "metod 20 qatordan oshmasin" qoidasidan aniqroq, chunki 40 qatorli to'g'ri chiziqli metod 10 qatorli ichma-ich shartlardan osonroq.

Kognitiv yukni kamaytiradigan uchta kuchli harakat bor. Shartni nomli mantiqiy o'zgaruvchiga chiqarish, chunki nom bir slotga joylashadi, ifoda esa uchta slotni oladi. Mahalliy o'zgaruvchi hayot muddatini qisqartirish, ideal holda e'lon qilingan joyda ishlatish. Metod ichida abstraksiya darajasini bir xil ushlash, ya'ni bir metodda ham SQL, ham narx hisoblash, ham audit log bo'lmasligi.

```java
// yomon: o'quvchi 6 ta shartni bir vaqtda yodda tutishi kerak
if (order.getStatus() == 2 && order.getItems().size() > 0
        && order.getCustomer().getBalance().compareTo(order.getTotal()) >= 0
        && !order.getCustomer().isBlocked()
        && order.getCreatedAt().isAfter(LocalDateTime.now().minusDays(30))) {
    ship(order);
}

// yaxshi: har bir shart nomlangan, o'quvchi 3 ta tushunchani ushlaydi
boolean paymentCovered = customer.hasBalanceFor(order.total());
boolean customerAllowed = !customer.isBlocked();
boolean withinShippingWindow = order.createdWithin(Duration.ofDays(30));

if (order.isConfirmed() && paymentCovered && customerAllowed && withinShippingWindow) {
    ship(order);
}
```

### 4.4 Metod uzunligi, ichma-ich shartlar va erta qaytish

Ichma-ich shartlar chuqurligi o'qish narxini chiziqli emas, ko'rsatkichli oshiradi. Uchinchi darajadagi `if` ichida turgan o'quvchi yuqoridagi ikki shartni ham yodda tutadi. Amaliy chegara: bitta metodda ikki darajadan chuqur bormaslik, uchinchi daraja paydo bo'lsa, ichkarini alohida metodga chiqarish.

Erta qaytish shu muammoni eng arzon yechadi. Metod boshida barcha yaroqsiz holatlarni tekshirib qaytarilsa, qolgan tana faqat "to'g'ri yo'l" bo'lib qoladi. Bu "guard clause" uslubi, va uning foydasi psixologik: o'quvchi tekshirilgan shartni xotiradan o'chirib yuboradi, chunki u boshqa qaytib kelmaydi.

```java
// yomon: 4 daraja chuqurlik, to'g'ri yo'l eng ichkarida yashiringan
public void refund(RefundRequest request) {
    if (request != null) {
        Payment payment = repo.find(request.paymentId());
        if (payment != null) {
            if (payment.isSettled()) {
                if (request.amount().compareTo(payment.amount()) <= 0) {
                    gateway.refund(payment, request.amount());
                }
            }
        }
    }
}

// yaxshi: yaroqsiz holatlar boshida tugaydi, oxirida faqat biznes amali qoladi
public void refund(RefundRequest request) {
    Payment payment = paymentRepository.findById(request.paymentId())
            .orElseThrow(() -> new PaymentNotFoundException(request.paymentId()));

    if (!payment.isSettled()) {
        throw new PaymentNotSettledException(payment.id(), payment.status());
    }
    if (request.amount().greaterThan(payment.refundableAmount())) {
        throw new RefundExceedsPaymentException(payment.id(), request.amount());
    }
    gateway.refund(payment, request.amount());
}
```

### 4.5 Izoh qachon kerak: "nima" emas, "nega"

Kod nima qilishini o'zi aytadi, shuning uchun uni takrorlagan izoh shovqin. Bundan yomoni, bu izoh kod o'zgarganda yangilanmaydi va yolg'onga aylanadi. Qoida oddiy: izoh kodda ko'rinmaydigan ma'lumot bersa qoladi, aks holda o'chiriladi.

Kodda ko'rinmaydigan to'rt xil ma'lumot bor. Birinchi, nega aynan shu yechim tanlangan va qaysi muqobil rad etilgan. Ikkinchi, tashqi dunyoning cheklovi, masalan provayder API si kunda 100 ta so'rovga ruxsat beradi. Uchinchi, matematik yoki huquqiy formulaning manbasi, masalan soliq hisoblash qoidasining rasmiy havolasi. To'rtinchi, vaqtinchalik yechim va uni olib tashlash sharti.

```java
// yomon: kod nima qilishini takrorlaydi
// pool kattaligini 20 ga o'rnatadi
hikariConfig.setMaximumPoolSize(20);

// yaxshi: qarorning asosi va chegarasi yozilgan
// PostgreSQL da max_connections = 100, bizda 4 ta instance ishlaydi.
// 4 x 20 = 80, qolgan 20 ta replikatsiya va admin ulanishlari uchun zaxira.
// Instance soni oshsa, bu qiymatni qayta hisoblash kerak.
hikariConfig.setMaximumPoolSize(20);

// yaxshi: tashqi cheklov kodda ko'rinmaydi, shuning uchun yoziladi
// Bank gateway bir IBAN uchun soatda 3 ta tekshiruvga ruxsat beradi (shartnoma 4.2).
// Shundan ortig'i 429 qaytaradi va 24 soat blok bo'ladi.
@RateLimiter(name = "ibanValidation")
public ValidationResult validate(Iban iban) { ... }
```

### 4.6 Xato va istisnolar orqali muloqot

Istisno xabari eng ko'p o'qiladigan matn, chunki uni production incidentida yarim tunda o'qiydilar. `RuntimeException("error")` kabi xabar muloqotni butunlay to'xtatadi. Yaxshi istisno uchta savolga javob beradi: nima bo'lmadi, qaysi obyekt bilan, va kutilgan holat qanday edi.

Arxitektura darajasida muhim qaror: domen xatolarini texnik xatolardan ajratish. "Omborda qoldiq yetmaydi" biznes holati, u kutilgan va uni foydalanuvchiga ko'rsatish kerak. "Ulanish uzildi" texnik holat, u retry va alert talab qiladi. Ikkisi bir xil tipda bo'lsa, chaqiruvchi ularni ajrata olmaydi va `catch (Exception e)` yozadi.

Xato kodlari API chegarasida alohida qiymat beradi. Kod mashina uchun, xabar odam uchun. Kodi bor xato mijoz tomonida ishlov berishni barqaror qiladi, chunki xabar matnini o'zgartirish mijozni buzmaydi.

```java
// yomon: kontekst yo'q, tip yo'q, log da faqat stack trace qoladi
if (stock < qty) {
    throw new RuntimeException("not enough");
}

// yaxshi: kontekst, domen tipi va mashina o'qiydigan kod
public final class InsufficientStockException extends BusinessException {
    private final Sku sku;
    public InsufficientStockException(Sku sku, int requested, int available) {
        super("INVENTORY_INSUFFICIENT_STOCK",
              "SKU %s uchun %d dona so'raldi, omborda %d dona bor"
                  .formatted(sku.value(), requested, available));
        this.sku = sku;
    }
}
// chaqiruvchi tomonda ajratish aniq bo'ladi
try {
    reservation.reserve(sku, quantity);
} catch (InsufficientStockException e) {
    return OrderResult.rejected(e.errorCode(), e.getMessage()); // biznes holati
} catch (DataAccessResourceFailureException e) {
    throw new RetryableInfrastructureException(e);              // texnik holat
}
```

### 4.7 Tur tizimidan foydalanish

Tur tizimi hujjatning kompilyator tekshiradigan qismi. Java 17 dan keyin bu kanalning kengligi sezilarli oshdi. `record` ma'lumot tashuvchini bir qatorda e'lon qiladi va `equals`, `hashCode`, `toString` ni o'zi beradi. `sealed interface` esa holatlar to'liq ro'yxatini e'lon qiladi, va `switch` da yangi holat qo'shilganda kompilyator xato beradi.

Value object primitiv obsessiyasini davolaydi. `String warehouseCode` va `String sku` o'rin almashsa kompilyator jim turadi, `WarehouseCode` va `Sku` bo'lsa esa kompilyatsiya buziladi. Bu xatoni runtime dan compile time ga ko'chiradi, ya'ni eng arzon joyga.

`Optional` qaytuvchi qiymat uchun, maydon yoki parametr uchun emas. Repository metodida `Optional<Order>` chaqiruvchiga "yo'q bo'lishi normal" degan xabarni beradi. `null` qaytarish esa hech narsa demaydi, shuning uchun chaqiruvchi tekshirishni esdan chiqaradi.

```java
// yomon: holatlar ro'yxati hech qayerda e'lon qilinmagan, string bilan ishlanadi
public String handle(String paymentResult, String code) {
    if ("OK".equals(paymentResult)) return "confirmed";
    if ("DECLINED".equals(paymentResult)) return "rejected:" + code;
    return "unknown";
}

// yaxshi: holatlar to'liq, switch da yangi holat qo'shilsa kompilyator ogohlantiradi
public sealed interface PaymentResult {
    record Authorized(TransactionId id, Money amount) implements PaymentResult {}
    record Declined(DeclineReason reason) implements PaymentResult {}
    record PendingReview(Duration expectedWait) implements PaymentResult {}
}

OrderDecision decide(PaymentResult result) {
    return switch (result) {
        case PaymentResult.Authorized a -> OrderDecision.confirm(a.id());
        case PaymentResult.Declined d -> OrderDecision.reject(d.reason());
        case PaymentResult.PendingReview p -> OrderDecision.hold(p.expectedWait());
    };
}
```

### 4.8 Paket tuzilishi: xususiyat bo'yicha bo'lish

Qatlam bo'yicha bo'lish, ya'ni `controller`, `service`, `repository`, `dto`, birinchi qarashda tartibli ko'rinadi. Amalda u eng muhim ma'lumotni yashiradi: tizim nima qiladi. `service` paketini ochgan odam 40 ta sinf ko'radi va ularning qaysi biri birga ishlashini bilmaydi. Bundan tashqari bitta funksiyani o'zgartirish 4 ta paketni ochishni talab qiladi.

Xususiyat bo'yicha bo'lishda yuqori daraja domenni aytadi: `order`, `payment`, `inventory`, `invoicing`. Har bir paket ichida o'z controller va repository si turadi. Buning ikki amaliy foydasi bor. Birinchi, `package-private` ko'rinishi haqiqatan ishlaydi, chunki bir xususiyatning ichki sinflari tashqariga chiqmaydi. Ikkinchi, modulni ajratish paytida paketni ko'chirish yetarli bo'ladi.

```bash
# yomon: qatlam bo'yicha, "tizim nima qiladi" ko'rinmaydi
com/shop/controller/{OrderController,PaymentController,StockController}.java
com/shop/service/{OrderService,PaymentService,StockService,...37 ta}.java
com/shop/repository/...
com/shop/dto/...

# yaxshi: xususiyat bo'yicha, chegaralar ko'rinadi
com/shop/order/{OrderController,OrderPlacement,OrderRepository,Order}.java
com/shop/payment/{PaymentController,PaymentAuthorization,PaymentGateway}.java
com/shop/inventory/{StockReservation,StockLevel,InventoryRepository}.java
com/shop/shared/money/{Money,Currency}.java   # faqat haqiqiy umumiy narsalar
```

Bu qarorni gap bilan emas, test bilan ushlab turish kerak. ArchUnit qoidasi `payment` paketidan `order` ning ichki sinflariga ulanishni taqiqlaydi, va shu bilan chegara hujjatdan kodga ko'chadi. Batafsil qoidalarni testlash qo'llanmasidagi arxitektura testlari bo'limida ko'rish mumkin.

### 4.9 Kodda yashirin bilim

Eng qimmat xatolar kodda yozilmagan bilim atrofida tug'iladi. Magic number buning eng ko'rinadigan shakli. `if (daysLate > 15)` ni o'qigan odam 15 ning qaydan kelganini bilmaydi, shuning uchun uni o'zgartirishga qo'rqadi yoki noto'g'ri o'zgartiradi. Nomli konstanta bu bilimni kodga qaytaradi: `MAX_GRACE_PERIOD_DAYS`.

Ikkinchi shakl yashirin tartib. Agar `validate()` ni `calculate()` dan oldin chaqirish kerak bo'lsa, lekin buni faqat muallif bilsa, bu bilim yo'qoladi. To'g'ri yechim tartibni imkonsiz qilish, masalan `calculate()` ni faqat `ValidatedOrder` tipidan qabul qiladigan qilish. Uchinchi shakl kutilmagan yon ta'sir: nomi `get` bilan boshlanadigan metod cache ni yangilasa yoki audit log yozsa, chaqiruvchi buni kutmaydi.

| Tuzoq | Nega xavfli | Yechim |
|---|---|---|
| `if (status == 3)` | 3 ning ma'nosi faqat SQL da yozilgan | `enum OrderStatus` va `@Enumerated(STRING)` |
| `Thread.sleep(500)` kutish | nega 500 ms, qanday sharoitda yetadi | nomli timeout konstanta va kommentda asos |
| `getBalance()` ichida yozish | tranzaksiyada kutilmagan UPDATE | `get` faqat o'qiydi, yozish `recalculate...()` |
| Yashirin chaqiruv tartibi | yangi developer tartibni buzadi | tipni o'zgartirish, `ValidatedOrder` kabi |
| `BigDecimal` da valyuta yo'q | USD va UZS qo'shilib ketadi | `Money(amount, currency)` value object |
| `List<String>` parametrlar | nima uchun ekani nomsiz | `record StockFilter(Set<Sku> skus, ...)` |
| Bo'sh `catch` bloki | xato yo'qoladi, incident ko'rinmaydi | log yoki qayta throw, albatta kontekst bilan |
| Statik util holat ushlaydi | test lar bir-biriga ta'sir qiladi | bean qilish, holatni argumentga ko'chirish |

### 4.10 O'zini hujjatlaydigan API

Public API uchun to'rtta kanal bor, va ularni birga ishlatish kerak. Birinchi kanal nom: metod nomi natijani va yon ta'sirni aytadi. Ikkinchi kanal imzo: parametr turlari noto'g'ri chaqiruvni imkonsiz qiladi. Uchinchi kanal Javadoc: faqat kod aytolmaydigan narsani yozadi, ya'ni shartnomani, tranzaksiya talabini, idempotentlikni va tashlanadigan istisnolarni. To'rtinchi kanal test nomlari: ular bajariladigan hujjat, chunki eskirsa qizil bo'ladi.

```java
// yomon: nom, imzo va hujjat hech narsa aytmaydi
/** Hisob-faktura yaratadi. */
public Invoice create(Long id, boolean b, int t) { ... }

// yaxshi: imzo chaqiruvni cheklaydi, Javadoc shartnomani aytadi
/**
 * Yopilgan buyurtma uchun hisob-faktura chiqaradi.
 * Idempotent: bir buyurtma uchun qayta chaqirilsa, mavjud fakturani qaytaradi.
 * Mavjud tranzaksiya talab qiladi (REQUIRED), o'zi tranzaksiya ochmaydi.
 *
 * @throws OrderNotClosedException buyurtma hali yopilmagan bo'lsa
 */
public Invoice issueInvoice(OrderId orderId, VatPolicy vatPolicy) { ... }
```

Test nomlari shu hujjatning davomi. `testCreate1` nomi hech kimga yordam bermaydi, `issueInvoice_returnsExistingInvoice_whenCalledTwiceForSameOrder` esa shartnomani takrorlaydi va buzilganda aynan qaysi kelishuv buzilganini aytadi. Arxitektor uchun amaliy o'lchov shu: public metod uchun yozilgan test nomlarini ketma-ket o'qib chiqqanda, u metodning shartnomasi tiklanishi kerak.

### 4.11 Amalda qo'llash

- [ ] Eng ko'p o'zgaradigan 5 ta sinfni tanlab, nomlaridan `Manager`, `Helper`, `Util`, `Processor` qo'shimchalarini olib tashlang va javobgarlik bo'yicha bo'ling.
- [ ] Domen eksperti ishlatadigan 15 ta atamani ro'yxat qilib, kodda ularning qanday yozilganini tekshiring; farq bo'lsa kodni domenga moslang.
- [ ] Eng murakkab 3 ta metodda ichma-ich shartlarni erta qaytishga aylantirib, chuqurlikni ikki darajadan oshmasligiga keltiring.
- [ ] Pul, SKU, ombor kodi va buyurtma identifikatori uchun value object joriy qiling, `String` va `BigDecimal` ni public imzolardan chiqaring.
- [ ] Barcha `throw new RuntimeException(...)` chaqiruvlarini topib, ularni kontekst va xato kodi bor domen yoki infratuzilma istisnolariga ajratib bering.
- [ ] Bitta xususiyatni (masalan to'lov) qatlam paketlaridan `payment` paketiga ko'chirib, ichki sinflarni `package-private` qiling va chegarani ArchUnit qoidasi bilan mahkamlang.
- [ ] Kodni magic number uchun skanerlang (timeout, retry soni, limit, kun soni) va har birini nomli konstanta va asosni aytuvchi izoh bilan almashtiring.
- [ ] Public API ning 10 ta metodida Javadoc ni "nima" dan "shartnoma" ga qayta yozing: idempotentlik, tranzaksiya talabi, tashlanadigan istisnolar.

## 5. Abstraksiya hissi, bog'liqlik va chegaralar (Abstraction, Coupling and Boundaries)

Abstraksiya hissi deganda chiroyli ierarxiya qurish qobiliyati emas, o'zgarish qayerdan kelishini oldindan sezish tushuniladi. Arxitektor har bir interfeysni savol bilan qo'yadi: "ertaga nima o'zgaradi va o'zgarish qancha faylga tegadi?". Agar javob yo'q bo'lsa, abstraksiya hali kerak emas. Bu bobda abstraksiyaning iqtisodi, bog'liqlik mexanikasi va chegarani qayerdan o'tkazish qarori ko'rib chiqiladi.

### 5.1 Abstraksiya nima uchun qo'yiladi: o'zgarishni bitta joyga to'plash

Abstraksiyaning yagona haqiqiy vazifasi bor: o'zgarish radiusini qisqartirish. Agar QQS stavkasi o'zgarganda 14 ta faylni tahrirlash kerak bo'lsa, abstraksiya yo'q. Agar bitta sinfni tahrirlab, qolgan hamma joy avtomatik to'g'ri ishlaydigan bo'lsa, abstraksiya ishlayapti. Shu sababli abstraksiyani "qayta ishlatish uchun" emas, "o'zgarishni ushlab turish uchun" qo'yish kerak.

Amalda bu ikki xil narsani ajratishdan boshlanadi: siyosat (policy) va mexanika. To'lov summasini hisoblash siyosat, HTTP orqali provayderga murojaat qilish mexanika. Siyosat biznes talabi bilan o'zgaradi, mexanika texnologiya bilan o'zgaradi. Ikkisi bir sinfda yashasa, har bir biznes o'zgarishi texnik kodga tegib ketadi.

```java
// Siyosat bitta joyda: narx qanday hisoblanadi.
// Mexanika (provayder, retry, timeout) bu sinfga umuman kirmaydi.
public final class OrderPricing {

    private final TaxPolicy taxPolicy;      // stavka o'zgarsa faqat shu implementatsiya o'zgaradi
    private final DiscountPolicy discounts; // aksiya qoidalari alohida evolyutsiya qiladi

    public Money total(OrderDraft draft) {
        Money net = draft.lines().stream()
                .map(line -> line.unitPrice().multiply(line.quantity()))
                .reduce(Money.ZERO, Money::add);
        Money afterDiscount = discounts.apply(draft.customerTier(), net);
        return afterDiscount.add(taxPolicy.taxFor(draft.region(), afterDiscount));
    }
}
```

Diqqat qiling: bu yerda `OrderPricing` uchun interfeys yaratilmadi. Narx hisoblashning bitta to'g'ri usuli bor, demak unda almashtiriladigan nuqta yo'q. Almashtiriladigan nuqtalar `TaxPolicy` va `DiscountPolicy`, chunki aynan shu ikkisi mintaqa va aksiya bo'yicha turlanadi. Abstraksiyani turlanish bor joyga qo'yish kerak, turlanish yo'q joyga emas.

### 5.2 Erta abstraksiya va takrorlanish: qaysi biri arzonroq

Ikki xato bir xil og'ir emas. Takrorlangan kodni birlashtirish mexanik ish: IDE yordamida 20 daqiqada bajariladi va natijasi testlar bilan tekshiriladi. Noto'g'ri abstraksiyani yechish esa chaqiruvchilar zanjirini buzadi, chunki hamma allaqachon o'sha interfeysga suyangan. Shuning uchun amaliy qoida: shubha bo'lsa takrorlashni tanla.

Takrorlanishning o'zi ham bir xil emas. Tasodifiy o'xshashlik (incidental duplication) ikki joyda kod hozir o'xshash, lekin sabablari boshqa. Haqiqiy takrorlanish (real duplication) bitta biznes qoidasi ikki joyda yozilgan. Birinchisini birlashtirish zarar keltiradi, ikkinchisini birlashtirmaslik xatolikka olib keladi. Tekshirish usuli oddiy: "bu ikki joy kelasi chorakda bir xil sababdan o'zgaradimi?". Javob "yo'q" bo'lsa, qo'shmang.

Raqamli chegara ham foydali. Uchinchi marta bir xil mantiq paydo bo'lganda abstraksiya qo'yish ko'pchilik jamoada yaxshi ishlaydi. Ikkinchi marta hali ma'lumot yetarli emas, to'rtinchi marta esa kech bo'lib qoladi. Spring loyihalarida yana bitta signal bor: agar bir xil `@Transactional` + repository + mapping ketma-ketligi uch xil servisda takrorlansa, u yerda yashirin domen amali turgan bo'ladi.

| Holat | Oddiy yondashuv | Arxitektor yondashuvi |
| --- | --- | --- |
| Ikki joyda o'xshash kod ko'rindi | Darhol umumiy `BaseService` chiqariladi | O'zgarish sababi bir xilmi, shu tekshiriladi |
| Yangi provayder qo'shilishi mumkin | Har bir servisga interfeys yoziladi | Interfeys faqat ikkinchi haqiqiy provayder kelganda chiqariladi |
| Har bir entity uchun repository | Jenerik `CrudService<T>` qatlami | Faqat haqiqiy domen amallari e'lon qilinadi |
| DTO va entity bir xil ko'rinadi | Entity to'g'ridan to'g'ri API ga chiqariladi | API shartnomasi alohida turadi, ichki model erkin o'zgaradi |
| Ikki modulga umumiy kod kerak | `common` moduli yaratiladi va o'sadi | Faqat o'zgarmas tiplar (`Money`, `OrderId`) umumiylashtiriladi |
| Bitta metodda ikki xatti-harakat | `boolean` flag parametri qo'shiladi | Ikki alohida metod yoki ikki implementatsiya |
| Modullar o'rtasida ma'lumot kerak | Boshqa modul jadvaliga `join` qilinadi | Event yoki aniq API orqali olinadi |
| Interfeys o'zgarishi kerak | Interfeysga yangi metod qo'shiladi | Avval kim foydalanayotgani va kim egasi aniqlanadi |
| Chegara noqulaylik keltiryapti | Chegara olib tashlanadi | Chegara joyi noto'g'ri qo'yilgani tekshiriladi |

### 5.3 Noto'g'ri abstraksiya narxi va undan qaytish yo'li

Noto'g'ri abstraksiya o'zini bitta belgi bilan oshkor qiladi: yangi talab kelganda interfeysga parametr qo'shiladi. Keyin ikkinchi parametr, keyin `Map<String, Object> options`. Shu paytdan boshlab abstraksiya mantiqni yashirmaydi, balki chaqiruvchidan mantiqni bilishni talab qiladi. Chaqiruvchi `if` yozib qaysi parametrni berishni tanlay boshlaydi, demak qaror chegaradan tashqariga chiqib ketgan.

```java
// Noto'g'ri abstraksiya: bitta metod uch xil ishni bajarmoqchi.
public interface ReportService {
    // includeDraft, groupByWarehouse, currency - bular chaqiruvchining qarori bo'lib qoldi
    Report build(LocalDate from, LocalDate to,
                 boolean includeDraft, boolean groupByWarehouse, String currency);
}

// Qaytish yo'li: har bir haqiqiy foydalanish holati o'z nomini oladi.
public interface StockReports {
    WarehouseStockReport dailyStockByWarehouse(LocalDate day);
}

public interface SalesReports {
    SalesReport monthlySales(YearMonth month, Currency currency);
}
```

Qaytish ketma-ketligi quyidagicha ishlaydi. Birinchi qadam: abstraksiyani olib tashlamasdan, chaqiruvchilarni ikki guruhga bo'lib, har biriga yangi aniq metod beriladi. Ikkinchi qadam: eski metod `@Deprecated` qilinadi va chaqiruvchilar bittalab yangi metodga ko'chiriladi. Uchinchi qadam: eski metod o'chiriladi. Bu "inline qilib, keyin to'g'ri joyda qayta ajratish" usuli, va u katta refaktoringdan ko'ra xavfsiz, chunki har bir qadam alohida deploy qilinadi.

Narxni raqamda ko'rish uchun bitta o'lchov yetarli: noto'g'ri abstraksiyaga suyangan chaqiruvchilar soni. 3 ta chaqiruvchi bo'lsa bir kunlik ish. 30 ta chaqiruvchi va 4 ta jamoa bo'lsa bu chorak davomidagi migratsiya rejasiga aylanadi. Shuning uchun abstraksiyani jamoalar o'rtasidagi chegarada qo'yishdan oldin ikki marta o'ylash kerak.

### 5.4 Bog'liqlik turlari: ma'lumot, vaqt, joylashuv, sxema bo'yicha bog'liqlik

"Coupling" degan so'z juda umumiy. Qaror chiqarish uchun uni turlarga bo'lib ko'rish kerak, chunki har bir tur boshqa yechim talab qiladi.

Ma'lumot bo'yicha bog'liqlik: modul boshqa modulning ma'lumot shaklini biladi. Agar `OrderService` to'lov javobidagi 12 ta maydondan faqat 2 tasini ishlatsa ham, butun sinfga bog'lanib qoladi. Yechim: chegarada faqat kerakli maydonlardan iborat kichik tip e'lon qilish.

Vaqt bo'yicha bog'liqlik (temporal coupling): A modul ishlashi uchun B modul aynan shu paytda tirik bo'lishi shart. Buyurtma qabul qilish to'lov servisining sinxron javobiga bog'liq bo'lsa, to'lov servisi 2 sekundga sekinlashganda buyurtma oqimi ham to'xtaydi. Yechim: javobni kutish shart bo'lmagan joyda event yoki outbox orqali asinxron qilish, shart bo'lgan joyda esa timeout va fallback bilan aniq chegara qo'yish.

Joylashuv bo'yicha bog'liqlik: kod boshqa tomonning manzilini, port raqamini yoki topologiyasini biladi. Bu konfiguratsiya va service discovery darajasida hal qilinadi, kodda qattiq yozilmaydi.

Sxema bo'yicha bog'liqlik: eng og'iri. Ikki servis bitta jadvalni o'qiydi yoki yozadi. Bu holatda hech qanday kod refaktoringi yordam bermaydi, chunki bog'liqlik ma'lumotlar bazasi darajasida.

| Bog'liqlik turi | Qanday aniqlanadi | Qanday yumshatiladi | Qoldiq xavf |
| --- | --- | --- | --- |
| Ma'lumot | Chaqiruvchi 12 maydonli tipni import qiladi | Chegarada kichik, o'zingga tegishli tip | Mapping kodi ko'payadi |
| Vaqt | Sinxron zanjir 3 va undan ko'p servisdan o'tadi | Event, outbox, timeout va fallback | Yakuniy izchillik kechikishi |
| Joylashuv | URL va port kodda yozilgan | Config, discovery, abstraksiyalangan client | Konfiguratsiya xatosi |
| Sxema | Ikki servis bitta jadvalga yozadi | Egalik bitta servisga, qolganlarga API yoki view | Migratsiya murakkabligi |

### 5.5 Kohéziya: nima birga o'zgarsa, birga tursin

Kohéziya bog'liqlikning teskari tomoni emas, uning sherigi. Yuqori kohéziya degani bitta sababdan o'zgaradigan kod bitta joyda turadi. Spring loyihalarida eng keng tarqalgan xato texnik qatlamlar bo'yicha paketlash: `controller`, `service`, `repository`, `dto`. Bu ko'rinishda chiroyli, lekin har bir biznes o'zgarishi to'rt paketga tegadi, demak kohéziya past.

Alternativa: xususiyat bo'yicha paketlash. `order`, `payment`, `inventory`, `reporting`. Har birining ichida o'z controller, servis va repository turadi. Bunda "buyurtmani bekor qilish" talabi bitta paket ichida bajariladi. Qo'shimcha foyda: paket darajasida ko'rinishni cheklash mumkin bo'ladi, chunki sinflarning ko'pchiligi `public` bo'lishi shart emas.

```java
// com/shop/order/OrderCancellation.java
// Paket-private: modul tashqarisidan ko'rinmaydi, demak chegara kod bilan himoyalangan.
class OrderCancellation {

    private final OrderRepository orders;
    private final ApplicationEventPublisher events;

    @Transactional
    void cancel(OrderId id, CancelReason reason) {
        Order order = orders.findForUpdate(id)      // SELECT ... FOR UPDATE
                .orElseThrow(() -> new OrderNotFound(id));
        order.cancel(reason);                        // qoida entity ichida
        orders.save(order);
        // Tashqi modullar faqat shu event'ni ko'radi, Order ni ko'rmaydi.
        events.publishEvent(new OrderCancelled(id, order.customerId(), reason));
    }
}
```

Bu yerda muhim mexanika bor: `ApplicationEventPublisher` bilan chiqarilgan event `@TransactionalEventListener` orqali commit dan keyin ishlanishi mumkin. Shunda inventar moduli buyurtma tranzaksiyasini uzaytirmaydi. Agar event tashqi tizimga chiqishi kerak bo'lsa, u holda bazaga yozib, keyin yuboradigan yondashuv kerak bo'ladi, bu dizayn patternlar hujjatidagi outbox pattern.

### 5.6 Modul chegarasini qayerdan o'tkazish: o'zgarish tezligi va egalik bo'yicha

Chegarani domen diagrammasidan emas, ikki o'lchovdan chiqarish kerak: nima qanchalik tez o'zgaradi va kim javobgar. Bir xil tezlikda va bir xil jamoa qo'li bilan o'zgaradigan kod bitta modulda yashashi kerak. Haftada o'zgaradigan aksiya qoidalari va yilda bir o'zgaradigan buxgalteriya hisobi bir modulda bo'lmasligi lozim.

O'zgarish tezligini taxmin qilish shart emas, uni git tarixidan o'lchash mumkin. Bu arxitektor uchun eng arzon ma'lumot manbai.

```bash
# Oxirgi 6 oyda qaysi paketlar eng ko'p o'zgargan: chegara nomzodlari shu yerda.
git log --since="6 months ago" --name-only --pretty=format: \
  | grep '^src/main/java' \
  | awk -F/ '{print $4"/"$5"/"$6}' \
  | sort | uniq -c | sort -rn | head -20

# Birga o'zgaradigan fayllar juftligi: yuqori son yashirin kohéziyani ko'rsatadi.
git log --since="6 months ago" --name-only --pretty=format:%H \
  | awk 'NF==0{next} /^[0-9a-f]{40}$/{c=$0; next} {print c" "$0}' \
  | sort | head -5
```

Birinchi buyruq o'zgarish zichligini beradi. Ikkinchisi birga o'zgaradigan fayllarni ko'rsatadi, va agar ikki alohida modul fayllari doim birga o'zgarsa, chegara noto'g'ri joydan o'tgan. Egalik o'lchovi ham shu tarixdan chiqadi: bitta paketga 4 xil jamoa commit qilayotgan bo'lsa, u paket chegara emas, umumiy maydon.

### 5.7 Interfeys kimga tegishli: foydalanuvchi tomonda e'lon qilish

Klassik xato: interfeys implementatsiya bilan bir paketda turadi. Bunda interfeys "men nimani taklif qilaman" degan ma'noni beradi. To'g'ri yondashuv teskari: interfeysni muhtoj tomon e'lon qiladi va unda "menga nima kerak" yoziladi. Shunda interfeys ehtiyoj bilan o'zgaradi, provayder bilan emas.

Farq amalda sezilarli. Agar `PaymentGateway` interfeysi to'lov adapteri paketida tursa, unda provayderning hamma imkoniyati paydo bo'ladi: `authorize`, `capture`, `void`, `partialRefund`, `tokenize`. Buyurtma moduliga esa faqat ikkitasi kerak. Interfeysni buyurtma tomonida e'lon qilsangiz, u ikki metod bilan qoladi va provayder almashganda buyurtma moduli umuman o'zgarmaydi.

```java
// com/shop/order/spi/PaymentAuthorizer.java
// Buyurtma moduli nimaga muhtoj ekanini o'zi aytadi. 2 metod, boshqa hech narsa.
public interface PaymentAuthorizer {
    AuthorizationResult authorize(OrderId orderId, Money amount, PaymentMethodRef method);
    void release(AuthorizationId authorizationId);   // bekor qilinganda bloklangan summani bo'shatish
}

// com/shop/payment/acme/AcmeAuthorizerAdapter.java
// Adapter tashqi paketda turadi va buyurtma modulining interfeysiga moslashadi.
@Component
class AcmeAuthorizerAdapter implements PaymentAuthorizer {

    private final RestClient acme;   // timeout: connect 1s, read 3s

    @Override
    public AuthorizationResult authorize(OrderId id, Money amount, PaymentMethodRef m) {
        AcmeAuthResponse res = acme.post()
                .uri("/v2/authorizations")
                .body(AcmeAuthRequest.of(id, amount, m))
                .retrieve()
                .body(AcmeAuthResponse.class);
        return AuthorizationResult.from(res);   // tashqi tip chegaradan o'tmaydi
    }
}
```

Bu joylashuvning yana bir foydasi bor: bog'liqlik yo'nalishi avtomatik to'g'ri bo'lib qoladi. `payment.acme` paketi `order.spi` paketini biladi, teskarisi yo'q. Spring konteyner `PaymentAuthorizer` ni injeksiya qilganda implementatsiya qaysi paketda ekani ahamiyatsiz, chunki bog'lanish tip bo'yicha amalga oshadi.

### 5.8 Bog'liqlik yo'nalishini boshqarish: ichki qatlam tashqarini bilmasin

Qatlamlar haqida gapirishning foydali usuli: import yo'nalishi. Domen kodida `jakarta.persistence`, `org.springframework.web` yoki `com.fasterxml.jackson` importlari paydo bo'lsa, chegara allaqachon buzilgan. Bu holat sekin-asta keladi: avval `@JsonIgnore` entity ga qo'yiladi, keyin `@Column` nomi API shartnomasiga ta'sir qiladi, va oxirida API ni o'zgartirish uchun migratsiya yozish kerak bo'ladi.

Bu qoidani sharhda yozib qo'yish yetarli emas, uni avtomatik tekshirish kerak. ArchUnit shu uchun mavjud va u testlash qo'llanmasidagi arxitektura qoidalari bo'limida batafsil ko'rsatilgan. Bu yerda faqat qoida shakli muhim.

```java
@AnalyzeClasses(packages = "com.shop", importOptions = ImportOption.DoNotIncludeTests.class)
class BoundaryRulesTest {

    @ArchTest
    static final ArchRule domen_web_ni_bilmaydi = noClasses()
            .that().resideInAPackage("..domain..")
            .should().dependOnClassesThat()
            .resideInAnyPackage("..web..", "..api..", "org.springframework.web..");

    @ArchTest
    static final ArchRule modullar_bir_birining_ichiga_kirmaydi = slices()
            .matching("com.shop.(*)..")
            .should().notDependOnEachOther()
            .ignoreDependency(alwaysTrue(), resideInAPackage("com.shop.shared.."));
}
```

Yo'nalishni buzadigan eng ko'p uchraydigan sabab qulaylik. Developer hisobot uchun buyurtma entity sini to'g'ridan to'g'ri olmoqchi bo'ladi, chunki shunday qilish 5 daqiqa, API orqali olish 2 soat. Arxitektorning ishi shu tanlovni arzonlashtirish: hisobot uchun aniq o'qish interfeysi va kerakli ma'lumotni beradigan proyeksiya oldindan tayyor bo'lsa, qoidani buzish ehtiyoji qolmaydi.

### 5.9 Sxema chegarasi: boshqa servisning jadvaliga tegmaslik qoidasi

Kod chegarasini ArchUnit saqlaydi, lekin ma'lumotlar bazasi chegarasini hech kim saqlamaydi. Agar ikki servis bitta `orders` jadvalini o'qisa, ularni mustaqil deploy qilish imkoni yo'q: ustun nomini o'zgartirish ikkinchi servisni sindiradi. Shuning uchun har bir modul yoki servis o'z jadvallarining yagona egasi bo'lishi kerak.

PostgreSQL da buni sxema va rol darajasida majburiy qilish mumkin. Bu eng ishonchli usul, chunki u niyatga emas, ruxsatga asoslanadi.

```sql
-- Har bir modul o'z sxemasida yashaydi.
CREATE SCHEMA order_svc AUTHORIZATION order_app;
CREATE SCHEMA billing_svc AUTHORIZATION billing_app;

-- Billing order_svc jadvallarini ko'rmaydi: ruxsat berilmagan.
REVOKE ALL ON SCHEMA order_svc FROM billing_app;

-- Kerakli ma'lumot faqat aniq shartnoma orqali chiqadi: tor view.
CREATE VIEW order_svc.order_billing_v AS
SELECT id AS order_id, customer_id, total_amount, currency, placed_at
FROM order_svc.orders
WHERE status IN ('PLACED', 'SHIPPED');

GRANT USAGE ON SCHEMA order_svc TO billing_app;
GRANT SELECT ON order_svc.order_billing_v TO billing_app;

-- search_path ni rolga biriktirib, tasodifiy jadval nomlanishini oldini olish.
ALTER ROLE billing_app SET search_path = billing_svc, public;
```

View bu yerda shartnoma rolini o'ynaydi. Ichki jadval tuzilishi o'zgarsa, view saqlanadi va billing hech narsani sezmaydi. Bu to'liq yechim emas, chunki baza darajasidagi sinxron o'qish baribir vaqt bo'yicha bog'liqlik qoldiradi, lekin bu "hamma hamma joyga `join` qiladi" holatidan ancha yaxshi.

Migratsiyalar ham egalik qoidasiga bo'ysunadi. Har bir servis faqat o'z sxemasiga migratsiya qiladi, va bu konfiguratsiyada aniq yozilishi kerak.

```yaml
spring:
  flyway:
    enabled: true
    schemas: order_svc            # faqat o'z sxemasi
    default-schema: order_svc
    locations: classpath:db/migration/order
    baseline-on-migrate: false
  datasource:
    hikari:
      maximum-pool-size: 20       # 4 instance x 20 = 80, PostgreSQL max_connections 200 dan past
      connection-timeout: 3000    # ms
  jpa:
    properties:
      hibernate:
        default_schema: order_svc
```

Pool o'lchami ham chegara masalasi. Har bir servis o'z pooliga ega bo'lishi kerak, chunki umumiy pool bir servisning sekin so'rovini boshqasining muammosiga aylantiradi. 4 ta instance va har birida 20 ulanish 80 ulanishni beradi, va bu `max_connections` 200 bo'lgan serverda xavfsiz. Pool to'lib qolsa `connection-timeout` 3 sekundda xato qaytaradi, bu cheksiz kutishdan afzal.

### 5.10 Chegara noto'g'ri qo'yilganini bildiradigan belgilar

Chegara to'g'ri yoki noto'g'ri ekanini nazariyadan emas, kundalik ishlashdan bilib olish mumkin. Quyidagi belgilar aniq va o'lchanadigan.

Birinchi belgi: bitta talab uchun ikki yoki uch repozitoriyga o'zgartirish kiritiladi va ularni birgalikda deploy qilish kerak. Bu "taqsimlangan monolit" ning klassik ko'rinishi. Ikkinchi belgi: pull request lar doim ikki jamoaning reviewi ni kutadi. Uchinchi belgi: integratsiya testlarisiz hech narsani ishonch bilan o'zgartirib bo'lmaydi, chunki mantiq chegaralar bo'ylab tarqalgan.

To'rtinchi belgi texnik: bitta API chaqiruvi ichida 4 va undan ortiq sinxron tashqi murojaat bo'lsa. Har biri taxminan 50 ms bo'lsa ham, yakuniy p99 latency 500 ms dan oshadi va mavjudlik ko'paytmaga aylanadi. Beshinchi belgi: "shared" yoki "common" moduli loyihada eng tez o'sadigan modul bo'lsa. Bu modul chegara emas, chegaradan qochish joyi.

| Tuzoq | Nimaga olib keladi | Yechim |
| --- | --- | --- |
| Entity ni API javobi sifatida qaytarish | Ustun nomini o'zgartirish API ni sindiradi | Alohida javob tipi va mapping |
| `common` moduliga hamma narsa tushadi | Har bir o'zgarish hamma modulni qayta qurishga majbur qiladi | Faqat o'zgarmas tiplar qoldiriladi |
| Boshqa servis jadvaliga `join` | Mustaqil deploy imkoni yo'qoladi | Egalik + view yoki API |
| Interfeys implementatsiya paketida | Provayder o'zgarishi iste'molchiga tegadi | Interfeys iste'molchi tomonida |
| Sinxron zanjir 4 servisdan o'tadi | p99 latency va mavjudlik buziladi | Asinxron qadamlar, timeout, fallback |
| Lazy loading chegaradan o'tib ketadi | Boshqa qatlamda `LazyInitializationException` | Chegarada to'liq yuklangan proyeksiya |
| Har modul uchun alohida `CrudService<T>` | Domen amallari nomsiz qoladi | Aniq nomli biznes metodlari |

Oxirgi va eng ishonchli tekshiruv savoli shunday: yangi developer bitta modulni o'qib, uning vazifasini boshqa modulga qaramay tushuntirib bera oladimi? Agar "buni tushunish uchun to'lov servisini ham ko'rish kerak" degan javob kelsa, chegara hali to'g'ri joyda emas.

### 5.11 Amalda qo'llash

- [ ] Git tarixidan oxirgi 6 oylik o'zgarish zichligini paket bo'yicha hisoblab chiqing va eng ko'p o'zgaradigan 5 paketni chegara nomzodi sifatida belgilang.
- [ ] Loyihadagi har bir interfeysni ko'rib chiqing va implementatsiyasi bitta bo'lganlarini ro'yxatga oling, ularning qanchasi haqiqatan kerak ekanini qaror qiling.
- [ ] `boolean` yoki `Map<String, Object>` parametri bor public metodlarni toping va har birini aniq nomli alohida metodga ajratish rejasini yozing.
- [ ] Domen paketidan `jakarta.persistence`, `org.springframework.web` va Jackson importlarini qidirib, topilganlarini ro'yxatga oling.
- [ ] Bog'liqlik yo'nalishini tekshiradigan kamida 2 ta arxitektura qoidasini CI ga qo'shing va uni buzadigan mavjud holatlarni vaqtincha ro'yxat sifatida qayd qilib qo'ying.
- [ ] Ma'lumotlar bazasida har bir modul uchun alohida sxema va alohida rol yarating, keyin boshqa sxemalarga `SELECT` ruxsatini bekor qiling.
- [ ] Modullar o'rtasidagi har bir sinxron chaqiruvni ro'yxatga olib, har biri uchun timeout qiymatini yozib qo'ying va asinxron qilish mumkin bo'lganlarini belgilang.
- [ ] `common` yoki `shared` modulidagi sinflarni sanab chiqing va o'zgarmas tiplardan boshqa hammasini egasi bor modulga ko'chirish rejasini tuzing.

## 6. Murakkablikni boshqarish (Managing Complexity)

Arxitektorning asosiy ishi tezlik emas, murakkablikni boshqarish. Kod ishlayotgan holatda ham tizim o'lishi mumkin, chunki uni o'zgartirish narxi daromaddan oshib ketadi. Shu bobda murakkablik qayerdan kelib chiqadi, qanday o'lchanadi va uni kamaytiradigan qarorlar qanday himoya qilinadi degan savollarga javob beramiz. Misollar bitta tizimdan olinadi: to'lov servisi, buyurtma oqimi va ombor qoldig'i.

### 6.1 Muhim murakkablik va tasodifiy murakkablik farqi

Muhim murakkablik (essential) biznesning o'zidan keladi. Ombor qoldig'i rezervatsiya, bekor qilish, qaytarish va inventarizatsiya hisobiga o'zgaradi, va bu to'rt oqim bir-biri bilan kesishadi. Bu murakkablikni yo'qotib bo'lmaydi, uni faqat ko'chirish mumkin: kodga, ma'lumotlar modeliga yoki operator qo'llanmasiga.

Tasodifiy murakkablik (accidental) bizning qarorlarimizdan keladi. Uch qatlamli mapper, keraksiz event bus, har bir DTO uchun abstract factory, oltita profil, ikkita ORM. Buni o'lchash oson: biznes qoidasini bitta gap bilan aytib bo'ladimi, lekin uni kodda topish uchun beshta faylni ochish kerakmi. Agar shunday bo'lsa, qolgan to'rtta fayl tasodifiy murakkablik.

Amaliy test: yangi talab kelganda nechta joyga tegish kerak. "Rezerv 30 daqiqadan keyin bo'shasin" talabi bitta domen metodida bo'lsa, model to'g'ri. Agar bu scheduler, cache evict listener, DTO flag va frontend timerga tarqalgan bo'lsa, murakkablik tarqab ketgan.

```java
// Tasodifiy murakkablik: qoida uch joyga tarqalgan
if (order.getStatus() == Status.NEW && order.getPayment() != null
        && order.getPayment().getState().equals("AUTHORIZED")
        && !order.getItems().isEmpty()
        && order.getCreatedAt().isAfter(Instant.now().minus(Duration.ofMinutes(30)))) {
    reserve(order);
}

// Muhim murakkablik model ichida: qoida bitta nom oldi
if (order.readyForReservation(clock.instant())) {
    reserve(order);
}

// Order ichida, testlanadigan sof shart
boolean readyForReservation(Instant now) {
    return status == Status.NEW
        && payment.isAuthorized()
        && !items.isEmpty()
        && createdAt.isAfter(now.minus(RESERVATION_WINDOW));
}
```

### 6.2 Murakkablik qayerda to'planadi: shart, holat, integratsiya nuqtalari

Murakkablik tizimda bir tekis tarqalmaydi, u uchta joyga yig'iladi. Birinchi joy shartlar. Har bir `if` ikkita yo'l hosil qiladi, ketma-ket beshta mustaqil shart esa nazariy jihatdan 32 holat beradi. Amalda ularning yarmi hech qachon test qilinmaydi va aynan shu yarmidan incident chiqadi.

Ikkinchi joy holat. O'zgaradigan maydon vaqt o'qini kiritadi: javob endi "qaysi tartibda chaqirildi" degan savolga bog'liq. Spring kontekstida singleton bean ichidagi o'zgaradigan maydon eng qimmat xato, chunki u barcha request thread'lari bilan bo'linadi.

Uchinchi joy integratsiya nuqtalari. Har bir tashqi chaqiruv to'rtta yangi natija qo'shadi: muvaffaqiyat, biznes xatosi, timeout va noaniq holat. Noaniq holat eng qimmati, chunki to'lov provayderi timeout bergan paytda pul o'tgan yoki o'tmaganini bilmaymiz. Shu sababli to'lovda idempotency key va status so'rovi arxitekturaning bir qismi, qo'shimcha emas.

```java
// Integratsiya nuqtasi: uchta natija emas, to'rtta
PaymentOutcome charge(ChargeCommand cmd) {
    try {
        var res = client.charge(cmd.idempotencyKey(), cmd.amount());
        return res.approved() ? PaymentOutcome.approved(res.id())
                              : PaymentOutcome.declined(res.reason());
    } catch (PaymentDeclinedException e) {
        return PaymentOutcome.declined(e.getReason());   // biznes xatosi
    } catch (ResourceAccessException e) {
        // noaniq holat: pul o'tgan bo'lishi ham mumkin
        return PaymentOutcome.unknown(cmd.idempotencyKey());
    }
}
```

`unknown` holatini alohida nom bilan belgilash murakkablikni kamaytiradi. Aks holda u `catch (Exception e) { return false; }` ichida yashirinadi va bir yildan keyin ikki marta pul olish incidenti bo'lib qaytadi.

### 6.3 Holat (state) ni kamaytirish: immutable obyekt va sof funksiya

O'zgarmas obyekt bitta savolni butunlay o'chiradi: "bu qiymat qachon o'zgardi". Java 17 dan keyin `record` buni arzon qiladi, Java 21 da pattern matching bilan birga esa domen modelini o'qish osonlashadi. Qoida sodda: hisob-kitob sof funksiyada, o'zgarish esa faqat bitta joyda, aggregate ichida.

Sof funksiya testda mock talab qilmaydi. Narx hisoblashni `Clock` va narx jadvalini argument sifatida olgan funksiyaga aylantirsangiz, uning testi 1 ms da ishlaydi va Spring konteksti ko'tarilmaydi. Shu bilan test paketining ishlash vaqti o'nlab barobar qisqaradi, buning tafsiloti testlash qo'llanmasidagi unit test bo'limida.

```java
// Immutable buyruq va natija, sof hisob-kitob
public record PriceRequest(String sku, int qty, BigDecimal unitPrice,
                           BigDecimal discountRate) {
    public PriceRequest {
        if (qty <= 0) throw new IllegalArgumentException("qty musbat bo'lishi kerak");
    }
}

public record PriceResult(BigDecimal net, BigDecimal vat, BigDecimal total) {}

public final class Pricing {
    private static final BigDecimal VAT = new BigDecimal("0.12");

    // Sof funksiya: tashqi holat yo'q, natija faqat argumentlarga bog'liq
    public static PriceResult calculate(PriceRequest r) {
        var gross = r.unitPrice().multiply(BigDecimal.valueOf(r.qty()));
        var net = gross.subtract(gross.multiply(r.discountRate()))
                       .setScale(2, RoundingMode.HALF_UP);
        var vat = net.multiply(VAT).setScale(2, RoundingMode.HALF_UP);
        return new PriceResult(net, vat, net.add(vat));
    }
}
```

Kolleksiyalarni ham himoyalash kerak. `record` maydonidagi `List` havolasi hali ham o'zgaradi, shuning uchun konstruktorda `List.copyOf(items)` chaqiriladi. Hibernate 6.x bilan ishlaganda entity o'zgaruvchan bo'lib qoladi, lekin uning atrofida immutable projection va read model yarating. Bitta amaliy qoida: tranzaksiyadan tashqariga entity emas, record chiqsin, shunda lazy loading va detached holat muammosi tug'ilmaydi.

### 6.4 Konfiguratsiya murakkabligi: har bir flag kelajakdagi xato

Feature flag arzon ko'rinadi, chunki uni qo'shish bir qator. Narx esa kombinatsiyada. Oltita boolean flag 64 ta konfiguratsiya varianti beradi, va siz ulardan ikkitasini test qilasiz. Qolgan 62 tasi production'da "bizda shunday sozlanmagan edi" degan incident sifatida ochiladi.

Flag ikki turga bo'linadi. Release flag vaqtinchalik, uning muddati bor va u yopilgandan keyin o'chiriladi. Operatsion flag doimiy, masalan timeout qiymati yoki pool kattaligi. Release flag kodda qolib ketsa, u darhol texnik qarzga aylanadi. Shu sababli har bir release flag yaratilganda ikkita narsa yoziladi: egasi va o'lim sanasi.

```yaml
# Flag ro'yxati: har birida ega va o'lim sanasi bor
app:
  payments:
    # operatsion sozlama, doimiy qoladi
    connect-timeout: 2s
    read-timeout: 5s
    pool-max-connections: 50
  features:
    # release flag, 2026-11-15 da kod bilan birga o'chiriladi
    new-refund-flow:
      enabled: false
      owner: payments-team
      remove-after: 2026-11-15
```

```java
// Flag sonini cheklash uchun: tipli konfiguratsiya va validatsiya
@Validated
@ConfigurationProperties(prefix = "app.payments")
public record PaymentProperties(
        @NotNull Duration connectTimeout,
        @NotNull Duration readTimeout,
        @Min(5) @Max(200) int poolMaxConnections) {}
```

Tipli `@ConfigurationProperties` noto'g'ri qiymatni ishga tushish paytida ushlaydi, ya'ni soat 03:00 dagi incident o'rniga deploy paytidagi xato beradi. Spring Boot'ning `configprops` actuator endpoint'i joriy qiymatlarni ko'rsatadi, shuning uchun "qaysi qiymat ishlayapti" savoli bahsga aylanmaydi. Qoida: `@Value` bilan tarqalgan o'nlab satr o'rniga bitta tipli record yaxshi.

### 6.5 Kodni o'chirish: eng kam baholangan arxitektura ishi

Kod o'chirish murakkablikni kamaytiradigan eng ishonchli usul. U yangi abstraksiya qo'shishdan farqli ravishda hech qanday yangi xato kiritmaydi, agar o'chirilayotgan kod haqiqatan ishlatilmayotgan bo'lsa. Muammo faqat bitta: "ishlatilmayapti" degan gapni dalil bilan tasdiqlash kerak.

Dalil uchta manbadan olinadi. Birinchisi kod tahlili: statik qidiruv, reflection va SpEL ishlatilishini qo'lda tekshirish. Ikkinchisi runtime telemetriya: endpoint uchun request soni, bean uchun metrika, SQL uchun statistika. Uchinchisi ma'lumot: jadvalda yangi qator qo'shilganmi.

```sql
-- PostgreSQL 15-17: oxirgi statistika tiklanishidan beri tegilmagan indekslar
SELECT s.relname AS jadval, s.indexrelname AS indeks,
       s.idx_scan AS skanlar,
       pg_size_pretty(pg_relation_size(s.indexrelid)) AS hajm
FROM pg_stat_user_indexes s
JOIN pg_index i ON i.indexrelid = s.indexrelid
WHERE s.idx_scan = 0 AND NOT i.indisunique
ORDER BY pg_relation_size(s.indexrelid) DESC
LIMIT 20;

-- Jadval haqiqatan o'likmi: oxirgi yozuv vaqti va o'sish
SELECT relname, n_live_tup, n_tup_ins, n_tup_upd, last_autoanalyze
FROM pg_stat_user_tables
WHERE n_tup_ins = 0 AND n_tup_upd = 0
ORDER BY n_live_tup DESC;
```

Statistika `pg_stat_reset()` dan keyin yig'ilganini tekshiring, aks holda "0 skan" degan xulosa yolg'on bo'ladi. Kamida ikki hafta, mavsumiy hisobotlar bor bo'lsa bir oy kuzatish kerak, chunki chorak oxiridagi hisobot indeksni yiliga to'rt marta ishlatadi.

```bash
# O'chirishga nomzod: 12 oy davomida tegilmagan paketlar
git log --since="12 months ago" --name-only --pretty=format: \
  | grep -E '^src/main/java' | sort -u > /tmp/tegilgan.txt
find src/main/java -name '*.java' | sort > /tmp/hammasi.txt
comm -13 /tmp/tegilgan.txt /tmp/hammasi.txt | head -50

# O'chirishni bosqichli qilish: avval @Deprecated, keyin log, keyin olib tashlash
grep -rn "@Deprecated" src/main/java | wc -l
```

O'chirish bosqichli bo'ladi. Avval `@Deprecated` va WARN log qo'yiladi, ikki hafta kuzatiladi, log bo'sh bo'lsa kod olib tashlanadi. Ma'lumotlar bazasida ustun darhol `DROP` qilinmaydi, avval yozishni to'xtatish, keyin o'qishni to'xtatish, so'ng bir release kutib `DROP COLUMN` qilish kerak.

### 6.6 Texnik qarz: ongli qarz va tasodifiy loyqalik

Qarzning ikki turi bor va ular bilan muomala butunlay boshqacha. Ongli qarz qaror bilan olinadi: "Qora juma oldidan hisobotni to'g'ri modellashtirishga vaqt yo'q, vaqtinchalik SQL view bilan chiqaramiz, yanvarda qaytamiz". Bunda shart ma'lum, muddat ma'lum, egasi ma'lum.

Tasodifiy loyqalik hech qanday qaror bilan olinmagan. U shunchaki paydo bo'ladi: nomlash buzilgan, qatlam chegarasi yo'q, bitta servis ikki xil tranzaksiya modelini ishlatadi. Bu turdagi qarz foizi yuqori, chunki uning mavjudligini hech kim bilmaydi.

Arxitektor vazifasi loyqalikni ongli qarzga aylantirish. Bu ADR (arxitektura qaror yozuvi) orqali qilinadi: muammo, variantlar, tanlangan yo'l, narxi va qaytish sharti yoziladi. Qaytish sharti eng muhim qism, chunki u "bir kun kelib tozalaymiz" degan gapni o'lchanadigan narsaga aylantiradi. Masalan: "kunlik hisobot 90 sekunddan oshsa, yoki jadval 50 mln qatordan o'tsa, read model kiritiladi".

| Tuzoq | Nimaga olib keladi | Yechim |
|---|---|---|
| Flag kod bilan birga o'chirilmaydi | Har release'da kombinatsiya soni ikki barobar | Flag yaratilganda `remove-after` sanasi va CI tekshiruvi |
| "Umumiy" `util` paketi o'sib ketadi | Hamma hammaga bog'lanadi, modul chegarasi yo'qoladi | ArchUnit qoidasi: `util` faqat JDK ga bog'lansin |
| Singleton bean ichida o'zgaradigan maydon | Yuk ostida tasodifiy noto'g'ri natija | Holatni `record` ga, yoki `ThreadLocal` emas, argumentga ko'chirish |
| Entity DTO sifatida API dan chiqadi | Sxema o'zgarishi mijozni buzadi, lazy loading xatosi | Alohida projection record va `@Query` bilan to'g'ridan-to'g'ri map |
| Har bir servis o'zi retry qiladi | Timeout ostida chaqiruvlar ko'payib yuk oshadi | Retry faqat eng chetki qatlamda, idempotency key bilan |
| Konfiguratsiya 6 ta profil ichida takrorlanadi | Qaysi qiymat ishlayotgani noma'lum | Bitta asosiy fayl, profil faqat farqni override qiladi |
| Ko'p mayda servis bitta tranzaksiyani bo'ladi | Taqsimlangan nomuvofiqlik, qo'lda tuzatish | Tranzaksiya chegarasini bitta servisga qaytarish |
| Qarz hech qayerda yozilmagan | Har yangi odam uni qaytadan kashf qiladi | ADR va kodda `// QARZ: shart, muddat, ega` izohi |

### 6.7 Murakkablikni o'lchash: o'zgarish vaqti, incident soni, yangi odam vaqti

Murakkablikni "chiroyli emas" degan his bilan himoya qilib bo'lmaydi, raqam kerak. Uchta metrika amalda ishlaydi. Birinchisi o'zgarish vaqti: oddiy talab (masalan yangi to'lov usuli qo'shish) uchun idea'dan production'gacha necha kun ketadi. Ikkinchisi incident soni va ularning taqsimoti: qaysi modul oyiga nechta incident beradi. Uchinchisi yangi odam vaqti: yangi developer birinchi mustaqil PR'ini qancha vaqtda yuboradi.

Mo'ljal raqamlari: kichik o'zgarish uchun lead time 1-3 kun, deploy chastotasi kuniga kamida bir marta, change failure rate 15 foizdan past, yangi odamning birinchi PR'i 3-5 ish kuni. Agar yangi odam ikki haftada ham mustaqil PR yubora olmasa, bu tizim murakkabligining to'g'ridan-to'g'ri o'lchovi.

Kodga tegishli yordamchi signal: churn va bog'lanish. Oyiga 30 martadan ko'p o'zgaradigan va 40 ta boshqa klassga bog'langan fayl keyingi incident manbai. Bunday fayllarni git tarixidan topish oson, va u sub'ektiv bahsni ma'lumotga aylantiradi.

```bash
# Eng ko'p o'zgargan fayllar: murakkablik issiq nuqtalari
git log --since="6 months ago" --name-only --pretty=format: \
  | grep '\.java$' | sort | uniq -c | sort -rn | head -15

# Bitta fayl ustida nechta odam ishlagan: egasi noaniq modul belgisi
git log --since="6 months ago" --format='%an' -- \
  src/main/java/com/shop/order/OrderService.java | sort -u | wc -l
```

| Mavzu | Oddiy yondashuv | Arxitektor yondashuvi |
|---|---|---|
| Yangi talab | Mavjud servisga yana bitta `if` qo'shish | Shart domen metodiga nom bilan ko'chiriladi, holat soni hisoblanadi |
| Holat | Entity har joyda o'zgartiriladi | O'zgarish aggregate ichida, tashqariga immutable record chiqadi |
| Konfiguratsiya | Yangi ehtiyojga yangi flag | Flag egasi, o'lim sanasi va kombinatsiya narxi yoziladi |
| Abstraksiya | Kelajak uchun oldindan interfeys | Uchinchi real foydalanuvchi paydo bo'lganda chiqariladi |
| Eski kod | "Tegmaymiz, ishlayapti" | Telemetriya bilan o'likligi tasdiqlanadi va bosqichli o'chiriladi |
| Texnik qarz | Backlog'da nomsiz ticket | ADR: shart, narx, qaytish mezoni va muddat |
| Servis ajratish | Modul katta bo'ldi, ajratamiz | Avval modul chegarasi, ajratish faqat alohida masshtab yoki SLA uchun |
| O'lchov | "Kod chigal" degan his | Lead time, incident taqsimoti, yangi odam vaqti raqamda |
| Integratsiya | `try/catch (Exception e)` | Timeout, noaniq holat va idempotency alohida modellashtiriladi |
| Qaror | Eng yangi texnologiya tanlanadi | Operatsion narx va jamoa tajribasi hisobga olinadi |

### 6.8 Servislar soni va operatsion murakkablik narxi

Har bir yangi servis kod emas, operatsion birlik qo'shadi. Unga pipeline, sekretlar, monitoring, alert, on-call egasi, versiya yangilash jadvali va migratsiya mexanizmi kerak. Taxminiy hisob: bitta servisni "bor" holatda saqlash yiliga bir muhandisning 10-15 foiz vaqtini oladi, hech qanday yangi funksiya qo'shilmasa ham.

Ikkinchi narx chaqiruv zanjirida. Agar bitta tashqi so'rov ketma-ket beshta servisdan o'tsa va har biri 99.9 foiz mavjud bo'lsa, umumiy mavjudlik taxminan 99.5 foizga tushadi. Latency ham qo'shiladi: har bir hop tarmoq va serializatsiya uchun taxminan 1-5 ms, ichki retry bo'lsa ko'proq. Sinxron zanjirni qisqartirish eng arzon performance optimizatsiyasi.

Uchinchi narx ma'lumotda. Bitta tranzaksiya ikki servisga bo'linsa, siz ACID'dan voz kechib eventual consistency olasiz. Buning o'rnini outbox, kompensatsiya va reconciliation job to'ldiradi, ya'ni uchta yangi mexanizm (tafsiloti dizayn patternlar hujjatidagi outbox va saga bo'limlarida). Shu sababli servis chegarasi birinchi navbatda tranzaksiya chegarasiga qarab tanlanadi, kod hajmiga qarab emas.

Praktik yo'l: modular monolit bilan boshlash. Modul chegarasini kodda majburlash, ma'lumotlar bazasida sxema bilan ajratish, keyin faqat haqiqiy sabab bo'lganda ajratish. Haqiqiy sabab uchta: alohida masshtab profili, alohida ishonchlilik talabi, alohida release tezligi. "Jamoa alohida" ham sabab, lekin faqat jamoa 6-8 odamdan oshganda.

```java
// Modul chegarasini testda majburlash: kelajakdagi ajratishni arzon qiladi
@AnalyzeClasses(packages = "com.shop", importOptions = DoNotIncludeTests.class)
class ModuleRulesTest {

    // Ombor moduli to'lov modulining ichki klasslariga bog'lanmasin
    @ArchTest
    static final ArchRule chegara = noClasses()
            .that().resideInAPackage("..inventory..")
            .should().dependOnClassesThat()
            .resideInAPackage("..payment.internal..");

    // Domen qatlami Spring web'ga bog'lanmasin
    @ArchTest
    static final ArchRule domenMustaqil = noClasses()
            .that().resideInAPackage("..domain..")
            .should().dependOnClassesThat()
            .resideInAPackage("org.springframework.web..");
}
```

### 6.9 Umumiylashtirish tuzog'i: uchta foydalanuvchiga mo'ljallangan platforma

Eng qimmat murakkablik yaxshi niyatdan keladi. Jamoa ikkinchi mijoz uchun shunga o'xshash xususiyat so'raganini ko'radi va "keling, umumiy platforma qilamiz" deydi. Natijada ikki holatni qoplaydigan abstraksiya tug'iladi, lekin u uchinchi holatni qoplamaydi, chunki uchinchi holat hali ma'lum emas.

Qoida sodda: ikkita o'xshash joy takrorlanish emas. Uchinchi real holat paydo bo'lgandan keyin abstraksiya chiqarilsa, u haqiqiy o'zgaruvchanlik o'qini ko'radi. Undan oldin chiqarilgan abstraksiya tasodifiy o'q tanlaydi va keyin har yangi talab unga `if` qo'shib buziladi.

Ikkinchi belgi: parametr soni. Agar "umumiy" metod sakkizta argument, uchta enum va bitta `Map<String, Object>` olsa, u umumiy emas, u uchta alohida metodning ustiga tashlangan plash. Bunday holatda plashni yechib, uchta aniq nomli metod qoldirish kodni uzaytiradi, lekin murakkablikni kamaytiradi.

```java
// Erta umumiylashtirish: nima bo'layotgani o'qilmaydi
report.generate("ORDERS", Map.of("from", from, "to", to,
        "groupBy", "WAREHOUSE", "includeVat", true, "format", "XLSX"));

// Uchta aniq yo'l: har biri o'z testi va o'z SQL'i bilan
OrdersByWarehouseReport r1 = reports.ordersByWarehouse(from, to);
VatSummaryReport       r2 = reports.vatSummary(from, to);
StockSnapshotReport    r3 = reports.stockSnapshot(asOf);
```

Takrorlanishning o'zi ham narx, shuni inkor qilmaymiz. Farq shundaki, takrorlangan kodni birlashtirish keyinroq oson, noto'g'ri abstraksiyani yechish esa qiyin. Shu sababli tanlov nosimmetrik: shubha bo'lsa, takrorlanishni qoldiring.

### 6.10 Murakkablikni jamoaga tushuntirish va qarorni himoya qilish

Murakkablikni kamaytirish taklifi deyarli har doim "bu biznes qiymati bermaydi" degan e'tirozga uchraydi. Javob his bilan emas, narx bilan beriladi. "Bu modul oxirgi chorakda 7 ta incident berdi, har biri o'rtacha 4 soat ishni oldi, va unga tegadigan o'zgarish o'rtacha 9 kun ketadi" degan gap bahsni tugatadi.

Taklifni uchta ustunda bering. Birinchisi hozirgi narx raqamda. Ikkinchisi taklif va uning hajmi (masalan ikki hafta, bitta developer). Uchinchisi natija qanday o'lchanadi (lead time 9 kundan 3 kunga, incident oyiga 2 dan 0-1 ga). Agar uchinchi ustunni yozolmasangiz, taklif hali tayyor emas.

Bir vaqtda hamma narsani tozalashni so'ramang. Issiq nuqta ro'yxatidan eng qimmat bittasini tanlang va uni oqim ichida qiling: har bir funksional ishga 20 foiz tozalash qo'shing. Bu rejani buzmaydi va bir chorakda sezilarli natija beradi.

Teskari yo'nalishni ham unutmang. Ba'zan to'g'ri qaror murakkablikni ataylab qabul qilish: to'lovda idempotency, reconciliation va audit log kerak, chunki pul yo'qolishining narxi kodning chiroyliligidan baland. Arxitektorning mahorati murakkablikni yo'qotishda emas, uni qayerga qo'yishni tanlashda.

### 6.11 Amalda qo'llash

- [ ] Eng ko'p incident bergan uch modulni aniqlang va har biri uchun lead time hamda incident sonini raqamda yozib qo'ying.
- [ ] Git tarixidan oxirgi 6 oyda eng ko'p o'zgargan 15 faylni chiqarib, ularning bog'lanish sonini tekshiring va ikkitasini bo'lishni rejalashtiring.
- [ ] Barcha feature flag'larni ro'yxatga oling, har biriga ega va `remove-after` sanasi qo'shing, muddati o'tganlarini kod bilan birga o'chiring.
- [ ] Bitta muhim oqimdagi (masalan buyurtmani to'lash) tashqi chaqiruvlarni sanab chiqing va har biri uchun timeout, retry va noaniq holat qanday modellashtirilganini yozing.
- [ ] Bitta servisda `@Value` bilan tarqalgan sozlamalarni tipli `@ConfigurationProperties` record'ga yig'ib, validatsiya qo'shing.
- [ ] `pg_stat_user_indexes` va `pg_stat_user_tables` asosida o'lik indeks va jadvallar ro'yxatini tuzing, statistika yig'ilgan muddatni tekshirib, bosqichli o'chirish rejasini yozing.
- [ ] Modul chegaralari uchun kamida uchta ArchUnit qoidasi qo'shib, ularni CI darvozasiga ulang.
- [ ] Mavjud eng katta nomsiz texnik qarz uchun ADR yozing: shart, narx, qaytish mezoni va muddat.

## 7. Nosozlik haqida fikrlash (Thinking About Failure)

Nosozlik haqida fikrlash arxitektorni developerdan ajratadigan eng aniq chegara. Developer "bu kod ishlaydi" deb o'ylaydi, arxitektor "bu kod qachon va qanday ishlamaydi" deb so'raydi. Bu bob pattern katalogi emas: bu yerda nosozlikning mexanikasi, uning raqamlari va shu raqamlardan chiqadigan qarorlar bor. Har bir bo'limda siz jamoadan nimani so'rashingiz va qanday son kelishib olishingiz kerakligi ko'rsatilgan.

### 7.1 Hamma narsa buziladi: tarmoq, disk, protsess, boshqa servis

Taqsimlangan tizimda nosozlik hodisa emas, doimiy holat. Tarmoq paketi yo'qoladi, TCP ulanish NAT jadvalidan tushib qoladi, disk fsync'ni 400 ms kechiktiradi, JVM 3 sekundlik full GC ga ketadi, Kubernetes node'ni evict qiladi. Bu ro'yxatning har bir bandi oyda bir necha marta sodir bo'ladi, va ularning hech biri sizning kodingizdagi bug emas.

Arxitektor har bir tashqi chaqiruv uchun uchta savolga javob tayyorlaydi. Bu chaqiruv eng ko'p qancha kutadi. Kutish tugagach nima bo'ladi. Chaqiruv ikkinchi marta bajarilsa, biznes natija buziladimi.

Eng ko'p uchraydigan xato: timeout belgilanmagan chaqiruv. Spring'da `RestClient` yoki `WebClient` da timeout qo'yilmasa, OS darajasidagi TCP retransmission limitiga tayanadi, bu Linux'da taxminan 15 minutgacha cho'ziladi.

```yaml
spring:
  datasource:
    hikari:
      # pool'dan ulanish kutish: tez xato yaxshi, uzoq kutish yomon
      connection-timeout: 2000
      maximum-pool-size: 20
      max-lifetime: 1200000      # 20 daqiqa, PgBouncer/LB dan qisqa bo'lsin
      keepalive-time: 120000
      validation-timeout: 1000
      leak-detection-threshold: 20000
      data-source-properties:
        # JDBC socket darajasi: server o'lsa 5 sekundda bilamiz
        socketTimeout: 5
        connectTimeout: 2
        tcpKeepAlive: true
```

PostgreSQL tomonida ham chegara kerak. `statement_timeout` uzoq so'rovni uzadi, `lock_timeout` navbatda qotib qolishni to'xtatadi, `idle_in_transaction_session_timeout` ochiq tranzaksiyani tashlab ketgan protsessni tozalaydi. Hisobot servisi uchun `statement_timeout` ni 30 sekund, OLTP to'lov servisi uchun 3 sekund qilib ajratish normal qaror.

### 7.2 Nosozlik turlari: to'liq to'xtash, sekinlashuv, qisman javob, yolg'on javob

To'rt turdagi nosozlik bir xil emas, va ularni aniqlash qiyinligi ham bir xil emas. To'liq to'xtash eng oson tur: ulanish rad etiladi, xato darhol ko'rinadi, alert ishlaydi. Sekinlashuv qiyinroq: servis javob beradi, lekin p99 latency 80 ms dan 4 sekundga chiqadi.

Qisman javob yana qiyin. Katalog servisi 1000 ta mahsulotdan 940 tasini qaytaradi, qolgani uchun ichki timeout bo'ldi, lekin HTTP status 200 keladi. Sizning kodingiz buni muvaffaqiyat deb hisoblaydi.

Yolg'on javob eng xavfli tur. Cache'da eski narx turibdi, replica 40 sekund orqada qolgan, yoki xato tutilib `catch` ichida bo'sh ro'yxat qaytarilgan. Alert chiqmaydi, metrikada xato ko'rinmaydi, lekin biznes zarar ko'radi.

```java
// Yolg'on javob ishlab chiqaruvchi klassik anti-qaror
try {
    return warehouseClient.getStock(sku); // timeout bo'lsa?
} catch (Exception e) {
    log.warn("ombor javob bermadi", e);
    return 0; // "qoldiq nol" deb yozdik, aslida bilmaymiz
}
```

Nol qoldiq va "bilmayman" bir xil ma'no emas. Birinchisi mijozga "tugadi" deb ko'rsatadi, ikkinchisi "hozir aytolmaymiz" deb ko'rsatadi. Arxitektor qaytariladigan tipni shunday loyihalaydi: `Optional`, `Result` yoki alohida `UNKNOWN` holati bo'lsin, nol bilan aralashmasin.

| Nosozlik turi | Aniqlash vositasi | Tipik aniqlash vaqti | Biznes zarari |
|---|---|---|---|
| To'liq to'xtash | health check, 5xx hisoblagich | 10-30 sekund | katta, lekin ko'rinadi |
| Sekinlashuv | p99 latency, thread pool to'lishi | 1-5 daqiqa | kaskadga aylanadi |
| Qisman javob | natija hajmi metrikasi, element soni | soatlar | sekin va yashirin |
| Yolg'on javob | ma'lumot solishtirish, reconciliation | kunlar | eng qimmat |

### 7.3 Sekin servis o'lgan servisdan xavfliroq: navbat to'lishi va orqaga bosim

Buni raqam bilan ko'rsatish kerak, aks holda jamoa ishonmaydi. Little qonuni: bir vaqtda band bo'lgan ishlovchilar soni teng kelayotgan oqim ko'paytirilgan javob vaqtiga. Buyurtma servisi sekundda 200 so'rovni qabul qiladi va o'rtacha 50 ms ishlaydi. Demak bir vaqtda taxminan 10 thread band.

Endi downstream to'lov servisi sekinlashdi va javob vaqti 50 ms dan 2 sekundga chiqdi. Bir xil 200 rps da band thread soni 400 ga ko'tariladi. Tomcat'da `server.tomcat.threads.max` default 200. Demak 200 thread to'ladi, qolgan so'rovlar `accept-count` navbatiga tushadi, navbat ham to'lgach TCP ulanish rad etiladi.

Natija: to'lov servisi sekinlashgani uchun buyurtma servisi butunlay ishlamay qoldi, hatto to'lovga aloqasi yo'q "buyurtma tarixini ko'rish" endpoint'i ham o'ldi. O'lgan servis bunday zarar keltirmaydi, chunki undan kelgan xato darhol qaytadi va thread bo'shaydi.

```properties
# Navbat chuqurligini ataylab cheklash: tez rad etish, sekin o'lishdan yaxshi
server.tomcat.threads.max=200
server.tomcat.accept-count=50
server.tomcat.connection-timeout=5s
server.tomcat.max-connections=2000
# Async MVC uchun javob kutish chegarasi
spring.mvc.async.request-timeout=4s
# Graceful shutdown: navbatdagi so'rovni tugatib keyin o'chish
server.shutdown=graceful
spring.lifecycle.timeout-per-shutdown-phase=25s
```

Asosiy qoida: har bir chaqiruvning timeout'i chaqiruvchi tomonning SLO sidan kichik bo'lsin. Agar API o'z mijoziga 1 sekund ichida javob berishga majbur bo'lsa, ichki uchta chaqiruvning timeout yig'indisi 1 sekundan oshmasligi kerak. Ko'pincha bu 300 ms, 300 ms va 250 ms degan taqsimot bo'ladi.

Orqaga bosim (backpressure) kutishni navbatga yashirishni to'xtatadi. Kafka consumer'da `max.poll.records` ni kamaytirish, reactive oqimda bounded buffer, HTTP darajasida 429 qaytarish: bularning hammasi bitta fikrni amalga oshiradi. Tizim imkonidan ko'p ish qabul qilmasin.

### 7.4 Qayta urinish qachon zarar keltiradi: retry bo'roni va retry byudjeti

Retry foydali vosita, lekin u yuklamani ko'paytiradigan vosita. Uch marta urinish siyosati tizim allaqachon qiynalgan paytda yuklamani uch barobar oshiradi. Bu aynan eng yomon vaqtda sodir bo'ladi.

Ko'p qatlamli retry yana xavfliroq. Gateway 3 marta, buyurtma servisi 3 marta, JDBC qatlami 2 marta urinadi. Natijada bitta foydalanuvchi so'rovi bazaga 18 ta chaqiruvga aylanadi. Qoida: retry faqat bitta qatlamda bo'lsin.

Ikkinchi qoida: faqat retry qilish mumkin bo'lgan xatolar qaytarilsin. HTTP 503 va ulanish rad etilishi qaytariladi. HTTP 400 va validatsiya xatosi qaytarilmaydi. PostgreSQL'da `40001` (serialization failure) va `40P01` (deadlock detected) qaytariladi, `23505` (unique violation) qaytarilmaydi.

Uchinchi qoida: jitter majburiy. Jittersiz exponential backoff barcha mijozlarni bir xil daqiqada qayta urinishga majbur qiladi, va bu to'lqinni takrorlaydi. Tasodifiy tarqatish bilan birinchi urinish 100-200 ms, ikkinchisi 200-400 ms, uchinchisi 400-800 ms oralig'ida bo'ladi.

Retry byudjeti eng kuchli, lekin kamdan kam qo'llanadigan g'oya. Mohiyati: oxirgi 10 sekunddagi umumiy chaqiruvlardan ko'pi bilan 10 foizi retry bo'lishi mumkin. Byudjet tugasa retry butunlay o'chadi va xato darhol qaytariladi. Bu cheklov nosozlik paytida yuklama 3 barobar emas, 1.1 barobar oshishini kafolatlaydi. Resilience4j yoki shunga o'xshash kutubxona tanlanganda arxitektor shu byudjet imkoniyati bor-yo'qligini tekshiradi.

### 7.5 Idempotentlik: bir xil so'rovni ikki marta bajarish xavfsiz bo'lsin

Retry haqida gapirish idempotentlikni kelishib olmasdan ma'nosiz. Timeout bo'lganda siz ikkita holatni ajratib olmaysiz: so'rov umuman yetib bormadimi, yoki yetib borib bajarildi, faqat javob yo'qoldimi. Ikkinchi holatda qayta urinish ikkinchi to'lovni amalga oshiradi.

Yechim mijoz tomonidan beriladigan idempotency key va ma'lumotlar bazasidagi unique constraint. Muhim nuqta: constraint ilova kodida emas, bazada bo'lsin. Ilovadagi "avval tekshir, keyin yoz" mantig'i ikki instance parallel ishlaganda buziladi.

```sql
-- Idempotentlik kalitini bazada majburiy qilamiz
CREATE TABLE payment (
    id            bigserial PRIMARY KEY,
    order_id      bigint      NOT NULL,
    idem_key      text        NOT NULL,
    amount        numeric(18,2) NOT NULL,
    status        text        NOT NULL,
    response_body jsonb,
    created_at    timestamptz NOT NULL DEFAULT now()
);

-- Bitta kalit bitta to'lov: poyga (race) bo'lsa baza hal qiladi
CREATE UNIQUE INDEX ux_payment_idem ON payment (idem_key);

-- Takroriy urinishda yozmaymiz, lekin eski javobni topamiz
INSERT INTO payment (order_id, idem_key, amount, status)
VALUES (:orderId, :idemKey, :amount, 'PENDING')
ON CONFLICT (idem_key) DO NOTHING
RETURNING id;
```

`RETURNING` bo'sh qaytdi degani: bu kalit allaqachon bor. Shundan keyin kod yangi to'lov boshlamaydi, saqlangan javobni o'qib qaytaradi. Agar eski yozuv hali `PENDING` bo'lsa, mijozga 409 yoki "hozir ishlanmoqda" holati qaytariladi, lekin yangi debet qilinmaydi.

Idempotentlikning ikkinchi shakli natural kalitlar orqali keladi. Ombor qoldig'ini `stock = stock - 5` deb emas, hodisa identifikatori bilan yozib keyin yig'indini hisoblash qayta urinishga chidamli bo'ladi. Bu yerda outbox va hodisa jurnali kerak bo'ladi, dizayn patternlar hujjatidagi outbox pattern bo'limi mexanikani tushuntiradi.

Tashqi tizim o'zi idempotent bo'lmasa, uni siz idempotent qilasiz: har chaqiruvga `request_id` saqlab, javobni yozib, retry'ni o'sha saqlangan natija orqali boshqarasiz.

### 7.6 Qisman nosozlikda nima qilish: degradatsiya rejasi va zaxira javob

Degradatsiya texnik masala emas, biznes qaror. Arxitektorning ishi har bir funksiya uchun "bu yo'q bo'lsa nima ko'rsatamiz" javobini product egasidan yozma olish, va buni insidentdan oldin qilish.

Funksiyalarni uch guruhga bo'lish yetarli. Majburiy guruh ishlamasa, servis ishlamagan deb hisoblanadi: to'lovni qabul qilish, buyurtma yozish. Muhim guruh ishlamasa, xizmat davom etadi lekin sifat tushadi: tavsiyalar, yetkazib berish vaqti prognozi. Qo'shimcha guruh ishlamasa, foydalanuvchi sezmaydi ham: bonus ballar ko'rsatkichi, ko'rilgan mahsulotlar tarixi.

```java
// Degradatsiya: aniq uch holat, "nol" bilan aralashmaydi
public DeliveryEstimate estimate(Order order) {
    try {
        return deliveryClient.estimate(order); // 300 ms timeout
    } catch (TimeoutException | ServiceUnavailableException e) {
        metrics.counter("delivery.degraded").increment();
        // zaxira javob: shahar bo'yicha statik o'rtacha, aniqligi past
        return DeliveryEstimate.approximate(
                staticTable.averageDays(order.cityCode()),
                Confidence.LOW);
    }
}
```

Zaxira javobning uchta shartidan hech biri tushib qolmasligi kerak. Birinchi shart: zaxira javob o'z manbasiga bog'liq bo'lmasin, ya'ni u ham o'sha o'lgan servisdan kelmasin. Ikkinchi shart: zaxira javob ekanligi javob ichida ko'rinsin, `Confidence.LOW` yoki shunga o'xshash maydon bilan. Uchinchi shart: degradatsiya hisoblagichi alohida metrika bo'lsin, aks holda siz haftalab degradatsiyada ishlab, buni bilmasligingiz mumkin.

### 7.7 Ma'lumot yo'qolishi va buzilishi: qaysi biri ko'proq qo'rqinchli

Ma'lumot yo'qolishi ko'rinadi va o'lchanadi. Oxirgi 30 sekundlik tranzaksiyalar yo'qoldi, siz buni biladigan nuqtani topasiz, mijozlarga aytasiz, qayta yuklashni so'raysiz. Jarayon og'riqli, lekin chegarasi aniq.

Ma'lumot buzilishi ko'rinmaydi. Noto'g'ri migratsiya hisob qoldig'ini ikki barobar qildi, va bu uch hafta davomida hisobotlarga, to'lov hujjatlariga, soliq deklaratsiyasiga ko'chib ketdi. Backup'lar ham buzilgan ma'lumot bilan to'ldi. Shuning uchun arxitektor uchun buzilish har doim xavfliroq.

Buzilishga qarshi himoya to'rt qatlamdan iborat. Birinchi qatlam: bazadagi constraint'lar. `NOT NULL`, `CHECK (amount > 0)`, foreign key, unique index ilovaga bog'liq emas va deploy xatosidan omon qoladi. Ikkinchi qatlam: PostgreSQL data checksums. PostgreSQL 15-17 da bu `initdb` paytida yoqiladi, keyin `pg_checksums` yordamida to'xtatilgan klasterda o'zgartirish mumkin. Checksum yoqilmagan bo'lsa, diskdagi jimgina buzilish (silent corruption) sizga umuman xabar bermaydi.

Uchinchi qatlam: muntazam solishtirish. Kunda bir marta to'lov provayderi hisoboti bilan ichki jurnalni taqqoslash farqni bir kun ichida topadi. To'rtinchi qatlam: nuqtaga tiklanish imkoniyati, ya'ni PITR. Buzilish vaqti topilgach, shu nuqtaga qadar tiklash kerak bo'ladi.

```bash
# Bazaviy nusxa va WAL arxivi: PITR uchun asos
pg_basebackup -h db-primary -U replicator -D /backup/base \
  --wal-method=stream --checkpoint=fast --progress

# Tiklash nuqtasini belgilash (recovery sozlamalarida)
# restore_command = 'cp /backup/wal/%f %p'
# recovery_target_time = '2026-10-03 14:22:00+05'
# recovery_target_action = 'promote'

# Nusxaning haqiqatan tiklanishini har hafta tekshirish
pg_verifybackup /backup/base
```

Tekshirilmagan backup backup emas. Bu jumlani jamoa devoriga yozib qo'yish kerak. Har hafta avtomatik tiklash testi bo'lsin, va u faqat "fayl bor" emas, "baza ko'tarildi va kalit jadvallarda kutilgan qator soni bor" darajasida tekshirsin.

### 7.8 Nosozlik ta'sirini cheklash: bulkhead va alohida resurs hovuzlari

Kemadagi suv o'tkazmaydigan bo'limlar g'oyasi: bitta bo'lim suvga to'lsa, kema cho'kmaydi. Ilovada bu alohida resurs hovuzlari degani. Hisobot so'rovlari va to'lov so'rovlari bitta HikariCP pool'ini bo'lishmasin.

Amalda bu ikki `DataSource` bean degani. To'lov uchun 20 ulanish, hisobot uchun 5 ulanish. Hisobot og'ir so'rovlar bilan o'z 5 ta ulanishini band qilsa, to'lov hali ham 20 ulanishga ega. Bitta 25 lik umumiy pool'da hisobot hammasini yeb ketishi mumkin.

```java
@Bean
@Primary
@ConfigurationProperties("app.datasource.oltp")
public HikariDataSource oltpDataSource() {
    // to'lov va buyurtma: qisqa tranzaksiyalar, ko'p ulanish
    return DataSourceBuilder.create().type(HikariDataSource.class).build();
}

@Bean
@ConfigurationProperties("app.datasource.reporting")
public HikariDataSource reportingDataSource() {
    // hisobot: uzoq so'rovlar, kam ulanish, alohida pool
    return DataSourceBuilder.create().type(HikariDataSource.class).build();
}
```

Thread pool darajasida ham shu mantiq ishlaydi. Tashqi to'lov provayderiga chaqiruvlar alohida executor'da bo'lsa, provayder sekinlashganda umumiy web thread'lar band bo'lmaydi. Java 21+ dagi virtual thread'lar thread sonini arzonlashtiradi, lekin bulkhead zaruriyatini yo'qotmaydi: chegara endi thread sonida emas, pool ulanishlari va semaphore'larda bo'ladi.

Ajratish mezoni oddiy: so'rovning latency profili, biznes muhimligi va downstream bog'liqligi. Uchalasidan biri boshqalardan keskin farq qilsa, alohida hovuz oqlanadi.

### 7.9 Tiklanish vaqti: RTO va RPO raqamlarini kelishib olish

RTO: nosozlikdan keyin xizmat qancha vaqtda qayta ishlashi kerak. RPO: qancha ma'lumot yo'qolishiga ruxsat berilgan. Bu ikki raqam arxitekturani belgilaydi, aksi emas. Shuning uchun ular jamoa xohishi emas, biznes bilan yozma kelishuv bo'lishi kerak.

RPO nolga teng bo'lishi sinxron replikatsiyani talab qiladi. PostgreSQL'da bu `synchronous_commit = remote_apply` yoki `remote_write` va `synchronous_standby_names` sozlanishi. Buning narxi bor: har bir commit replica javobini kutadi, bu bir xil ma'lumot markazida taxminan 1-3 ms, boshqa regionda 30-80 ms qo'shadi. To'lov servisi uchun bu narx oqlanadi, hodisa jurnali uchun ko'pincha oqlanmaydi.

```sql
-- Replikatsiya orqada qolishini RPO raqami sifatida o'lchash
SELECT application_name,
       sync_state,
       write_lag,            -- WAL replicaga yozildi
       flush_lag,            -- diskka fsync qilindi
       replay_lag,           -- so'rovlar ko'radigan holat
       pg_wal_lsn_diff(pg_current_wal_lsn(), replay_lsn) AS bytes_behind
FROM pg_stat_replication;

-- Agar flush_lag > 2 sekund bo'lsa, RPO 2 sekunddan katta: alert kerak
```

RTO ni hisoblashda eng ko'p uchraydigan xato: faqat baza ko'tarilish vaqtini sanash. Haqiqiy RTO besh qismdan iborat: aniqlash, qaror, failover, ilovalarni qayta ulash, cache'ni isitish. Aniqlash 2 daqiqa, qaror 5 daqiqa, failover 1 daqiqa, qayta ulanish 2 daqiqa, cache isishi 10 daqiqa bo'lsa, RTO 20 daqiqa.

| Tizim qismi | RPO maqsadi | RTO maqsadi | Buni ta'minlaydigan qaror |
|---|---|---|---|
| To'lov tranzaksiyalari | 0 | 5 daqiqa | sinxron replica, avtomatik failover |
| Buyurtma holati | 10 sekund | 15 daqiqa | asinxron replica, WAL arxivi |
| Ombor qoldig'i | 1 daqiqa | 30 daqiqa | asinxron replica va qayta hisoblash |
| Hisobot omborxonasi | 24 soat | 8 soat | kunlik backup, qayta yuklash |
| Audit jurnali | 0 | 1 soat | append-only saqlash, ikki nusxa |

### 7.10 Nosozlik ssenariylarini oldindan yozish: "nima bo'lsa, nima qilamiz" jadvali

Insident paytida fikrlash sifati tushadi. Shuning uchun fikrlashni oldin bajarib, natijani jadvalga yozib qo'yish kerak. Bu jadval dizayn hujjatining majburiy qismi bo'lsin va har chorakda qayta ko'rilsin.

Jadvalda besh ustun bo'ladi: ssenariy, qanday bilib olamiz, avtomatik nima bo'ladi, odam nima qiladi, foydalanuvchi nimani ko'radi. Oxirgi ustun eng ko'p tashlab ketiladigan, lekin eng muhim ustun. Agar foydalanuvchi nimani ko'rishini yozib qo'yolmasangiz, degradatsiya rejasi hali tayyor emas.

| Tuzoq | Nega yuzaga keladi | Yechim |
|---|---|---|
| Timeout'siz tashqi chaqiruv | default qiymat OS darajasida, 15 minutgacha | har client uchun aniq timeout, SLO dan kichik |
| Ko'p qatlamli retry | har qatlam mustaqil 3 marta urinadi | retry bitta qatlamda, byudjet bilan cheklangan |
| Bo'sh ro'yxat qaytaradigan catch | xato yashiriladi, metrika toza ko'rinadi | alohida UNKNOWN holati va degradatsiya hisoblagichi |
| Umumiy connection pool | hisobot va OLTP bitta hovuzda | alohida DataSource, bulkhead |
| Takroriy to'lov | timeout'dan keyin retry, kalit yo'q | idem_key va unique index bazada |
| Tekshirilmagan backup | tiklash hech qachon sinalmagan | haftalik avtomatik tiklash testi |
| Replica lag nazoratsiz | RPO raqam sifatida o'lchanmagan | flush_lag alert, sinxron rejim kerakli joyda |
| Cache isishi hisobga olinmagan | RTO faqat baza vaqti deb o'lchangan | RTO ga isitish vaqti qo'shiladi |
| Checksum o'chirilgan baza | initdb default bilan ketilgan | data checksums yoqish, pg_verifybackup |

| Mavzu | Oddiy yondashuv | Arxitektor yondashuvi |
|---|---|---|
| Tashqi chaqiruv | "ishlaydi deb o'ylaymiz" | timeout, retry siyosati va zaxira javob oldindan yozilgan |
| Timeout qiymati | bitta umumiy 30 sekund | SLO dan kelib chiqib har chaqiruvga alohida budjet |
| Retry | har joyda 3 marta | bitta qatlamda, jitter bilan, byudjet cheklovida |
| Sekin downstream | "latency oshdi, kutamiz" | thread va pool to'lishini hisoblab, tez rad etishga o'tiladi |
| Xato tutish | log yozib bo'sh natija qaytarish | aniq UNKNOWN holati va degradatsiya metrikasi |
| Takroriy so'rov | "ikki marta kelmaydi" | idempotency key va bazadagi unique constraint |
| Resurs hovuzlari | bitta katta pool | latency profili bo'yicha ajratilgan hovuzlar |
| Backup | nusxa olinadi | nusxa olinadi va har hafta tiklanishi sinaladi |
| Tiklanish vaqti | "tez tiklaymiz" | RTO va RPO raqamlari biznes bilan yozma kelishilgan |
| Nosozlik rejasi | insident paytida o'ylanadi | ssenariy jadvali dizayn hujjatida tayyor |

Ssenariylarni izlash joyi aniq. Har bir tashqi bog'liqlik ikki ssenariy beradi: o'ldi va sekinlashdi. Har bir ma'lumot ombori uchta ssenariy beradi: o'qish, yozish, buzilish. Har bir navbat ikki ssenariy beradi: consumer orqada qoldi, xabar takrorlandi. O'rtacha servisda 15-25 ta ssenariy chiqadi.

Ssenariyni yozgandan keyin uni sinab ko'rish kerak. Bu yerda chaos testlari va nosozlikni ataylab kiritish ishga kiradi, testlash qo'llanmasidagi resilience testlari bo'limi texnikani ko'rsatadi. Arxitektor uchun muhimi: har bir yozilgan ssenariyning kamida bittasi haqiqatan tekshirilgan bo'lsin, aks holda jadval ishonch emas, qog'oz bo'lib qoladi.

### 7.11 Amalda qo'llash

- [ ] Servisdagi barcha tashqi chaqiruvlarni sanab, timeout qo'yilmaganlarini topib, har biriga SLO dan kelib chiqqan aniq qiymat belgilash.
- [ ] Little qonuni bilan hisoblab ko'rish: eng muhim downstream 10 barobar sekinlashsa, thread pool va connection pool qachon to'ladi va qancha so'rov rad etiladi.
- [ ] Retry siyosatini bitta qatlamga yig'ish, jitter qo'shish va retry byudjetini umumiy oqimning 10 foizi darajasida cheklash.
- [ ] To'lov va buyurtma yozuvlariga idempotency key maydoni va unique index qo'shib, takroriy so'rovni baza darajasida to'xtatish.
- [ ] Funksiyalarni majburiy, muhim va qo'shimcha guruhlarga ajratib, har bir muhim funksiya uchun zaxira javobni product egasi bilan yozma kelishib olish.
- [ ] Hisobot va OLTP uchun alohida DataSource bean'lari ajratib, pool o'lchamlarini mustaqil belgilash.
- [ ] `pg_stat_replication` dagi `flush_lag` bo'yicha alert yoqib, haqiqiy RPO ni o'lchangan raqam sifatida hujjatga yozish.
- [ ] Backup'dan tiklashni haftalik avtomatik test qilib, RTO ni besh qismi bilan (aniqlash, qaror, failover, qayta ulanish, cache isishi) o'lchash.
- [ ] Dizayn hujjatiga besh ustunli ssenariy jadvalini kiritib, kamida 15 ta ssenariy yozish va ulardan uchtasini haqiqatan sinab ko'rish.

## 8. Ishlash va resurs hissi: napkin math (Performance Intuition and Napkin Math)

Arxitektorni developerdan ajratadigan eng arzon ko'nikma: qog'oz burchagida hisoblash. Yuklamani, kechikishni va hajmni oldin hisoblab keyin kod yozish sprintni emas, yillarni tejaydi. Bu bobda to'lov servisi, buyurtma oqimi va ombor qoldig'i misolida aniq raqamlar bilan ishlaymiz. Maqsad formulani yodlash emas, kattalik tartibini (order of magnitude) sezish.

### 8.1 Har bir arxitektor yodda tutishi kerak bo'lgan kechikish raqamlari

Napkin math uchun aniq raqam kerak emas, kattalik tartibi kerak. Quyidagi jadval oddiy cloud muhiti uchun taxminiy qiymatlar, ularni yodlab oling.

| Operatsiya | Taxminiy kechikish | Nisbati (L1 = 1) |
|---|---|---|
| L1 cache o'qish | 1 ns | 1x |
| Main memory (RAM) tasodifiy o'qish | 80 ns | 80x |
| HashMap `get` (JVM, issiq kod) | 20-50 ns | ~30x |
| Bitta obyekt allokatsiyasi + keyingi young GC ulushi | 20-100 ns | ~50x |
| 1 KB JSON serializatsiya (Jackson) | 2-5 mcs | ~3 000x |
| NVMe SSD tasodifiy 4 KB o'qish | 100-200 mcs | ~150 000x |
| Bir xil AZ ichida tarmoq round-trip | 0.3-0.7 ms | ~500 000x |
| PostgreSQL oddiy indeks bo'yicha `SELECT` (issiq buffer) | 0.3-1 ms | ~700 000x |
| PostgreSQL `INSERT` + `COMMIT` (WAL fsync bilan) | 1-5 ms | ~3 000 000x |
| AZ'lar orasida round-trip (bir region) | 1-2 ms | ~1 500 000x |
| Region'lar orasi (masalan, Frankfurt va Virginia) | 80-100 ms | ~90 000 000x |
| Kafka'ga `acks=all` bilan yozish | 3-10 ms | ~6 000 000x |
| Tashqi HTTPS API chaqiruvi (TLS handshake bilan) | 50-300 ms | ~100 000 000x |

Xulosa: process ichidagi hisob deyarli bepul, tarmoq va disk qimmat. 10 000 marta `HashMap.get` bitta `SELECT` dan arzon, shuning uchun optimallashtirish tarmoq safarlari va fsync'lardan boshlanadi.

PostgreSQL'da `COMMIT` narxi asosan WAL'ni diskka yozishdir. `synchronous_commit = off` bilan commit 0.1 ms ga tushadi, lekin crash paytida oxirgi `wal_writer_delay` oraligidagi tranzaksiyalar yo'qoladi. Audit jurnali uchun bu yaramaydi, analitik event jadvali uchun to'g'ri savdo.

### 8.2 Oddiy hisob: kuniga N so'rov nechta RPS bo'ladi, cho'qqi koeffitsienti

Bir kunda 86 400 sekund bor. Napkin math uchun uni 100 000 deb olsa bo'ladi, xato 15 foizdan oshmaydi.

```java
// Buyurtma servisi uchun yuklama hisobi.
// Berilgan: kuniga 4 million buyurtma ko'rish so'rovi.
long kunlikSorov = 4_000_000L;
long sekundlar   = 86_400L;

double ortachaRps = (double) kunlikSorov / sekundlar;   // ~46 RPS

// Trafik sutka bo'ylab tekis emas. Amaliy koeffitsientlar:
//   B2B ichki sistema: cho'qqi = o'rtacha * 3 (ish kuni 8 soatga siqilgan)
//   ommaviy e-commerce: cho'qqi = o'rtacha * 5..8 (kechki soat 20:00-22:00)
//   aksiya yoki Black Friday: o'rtacha * 20..50
double cheqqiRps = ortachaRps * 6;                      // ~278 RPS

// Zaxira (headroom): hech qachon 100% sig'imga rejalashtirmang.
double rejaRps = cheqqiRps / 0.6;                       // ~463 RPS, 40% zaxira
```

4 million degan raqam katta ko'rinadi, lekin 46 RPS bitta Spring Boot instansiyasi uchun hech narsa emas. Arxitektor shu yerda "Kafka va sharding kerak" degan taklifni to'xtatadi. Teskari holat ham bor: kuniga 2 milliard event 23 000 RPS beradi, bu bitta PostgreSQL yozuv node'i uchun jiddiy chegara.

### 8.3 Little qonuni: parallellik, kechikish va throughput bog'liqligi

Little qonuni sig'im rejalashtirishning asosi: bir vaqtda bajarilayotgan ishlar soni (L) teng kelish tezligi (lambda) ko'paytiriladi ishning sistemada turish vaqti (W).

```java
// L = lambda * W
//   L      = bir vaqtda ishlayotgan so'rovlar soni (concurrency)
//   lambda = throughput, sekundiga so'rov (RPS)
//   W      = bitta so'rovning to'liq davomiyligi (sekund)
// Misol: to'lov servisi. Bitta so'rov o'rtacha 120 ms ishlaydi.
// Shundan: 15 ms bizning CPU, 25 ms PostgreSQL, 80 ms tashqi bank API.
double w = 0.120;          // sekund
double lambda = 400;       // kerakli RPS

double l = lambda * w;     // 48 ta so'rov bir vaqtda "havoda" turadi

// Teskari yo'nalish: 200 ta thread bor, har so'rov 120 ms.
// Nazariy maksimum throughput:
double maxRps = 200 / 0.120;   // ~1666 RPS, agar pastdagi resurs cheklamasa

// Agar tashqi bank API bir vaqtda faqat 50 ta ulanishga ruxsat bersa,
// haqiqiy chegara: 50 / 0.080 = 625 RPS. Thread sonini oshirish yordam bermaydi.
```

Amaliy xulosa: kechikish oshsa, o'sha throughput'ni saqlash uchun parallellik ham oshadi. Tashqi bank API 80 ms dan 400 ms ga sekinlashsa, 400 RPS uchun 48 emas, 160 ta so'rov bir vaqtda ushlanib turadi. Thread pool 100 ta bo'lsa, navbat o'sadi, timeout ishga tushadi va kaskad nosozlik boshlanadi. Bulkhead va timeout bo'yicha qarorlar aynan shu hisobdan kelib chiqadi.

### 8.4 Thread pool va connection pool kattaligini hisoblash

Ikki xil pool, ikki xil formula. CPU'ga bog'liq ishda thread soni yadro sonidan ko'p bo'lishi behuda, I/O kutadigan ishda esa thread soni kutish nisbatiga qarab oshadi.

```java
// 1) CPU-bound pool (masalan, hisobot aggregatsiyasi, PDF generatsiya)
int yadro = Runtime.getRuntime().availableProcessors();   // konteynerda: cpu limit
int cpuPool = yadro + 1;                                  // 8 yadro -> 9 thread

// 2) I/O-bound pool. Brian Goetz formulasi:
//    threads = yadro * targetUtilization * (1 + kutish / hisob)
// To'lov so'rovi: 15 ms CPU, 105 ms kutish (DB + bank API)
double kutish = 105, hisob = 15;
int ioPool = (int) (8 * 1.0 * (1 + kutish / hisob));      // 8 * 8 = 64 thread

// 3) Connection pool (HikariCP). Bu yerda formula BOSHQA.
// Faqat DB da o'tgan vaqtni oling: 25 ms DB, so'rovning qolgan 95 ms da
// ulanish band bo'lmasligi kerak (tranzaksiyani tashqi chaqiruv bilan bog'lamang).
// Little qonuni: L = 400 RPS * 0.025 s = 10 ta ulanish.
// Zaxira bilan: 10 / 0.7 = taxminan 15.
```

```properties
# To'lov servisi, 400 RPS, 25 ms DB vaqti, 4 instansiya.
spring.datasource.hikari.maximum-pool-size=15
spring.datasource.hikari.minimum-idle=15
# Pool bo'sh bo'lsa 2 sekunddan ko'p kutmaymiz: tez xato yaxshi.
spring.datasource.hikari.connection-timeout=2000
# Ulanishni 20 daqiqada yangilash: NAT va firewall timeout'idan oldin.
spring.datasource.hikari.max-lifetime=1200000
spring.datasource.hikari.leak-detection-threshold=10000
# Jami: 4 * 15 = 60 ulanish. PostgreSQL max_connections=200 ga sig'adi.
# Agar 4 ta servis har biri 50 so'rasa, 200 chegaradan oshadi: pgbouncer kerak.
```

Katta pool sekinlashtiradi. PostgreSQL'da har bir aktiv ulanish alohida backend process, 8 yadroli serverda 200 ta aktiv so'rov kontekst almashish va lock contention ustida vaqt yo'qotadi. 20 ta ulanish bilan umumiy throughput ko'pincha yuqori chiqadi.

### 8.5 Ma'lumot hajmini hisoblash: qator kattaligi, indeks hajmi, bir yillik o'sish

Qator kattaligini ustunlar yig'indisidan katta deb hisoblang. Har qatorda 23 baytlik tuple header, null bitmap va 8 bayt chegaraga tekislash bor, har sahifada (8 KB) item pointer uchun 4 bayt ketadi.

```sql
-- Buyurtma qatori: id bigint(8) + user_id bigint(8) + status smallint(2)
-- + amount numeric(12,2) ~ 10 + created_at timestamptz(8)
-- + idempotency_key uuid(16) = 52 bayt ma'lumot
-- + 23 bayt header + tekislash ~ 80 bayt/qator
-- Sahifaga: 8192 / (80 + 4) = taxminan 97 qator

-- Kuniga 200 000 buyurtma, bir yil:
--   200000 * 365 = 73 mln qator
--   73e6 * 80 bayt = 5.8 GB heap
--   fillfactor va o'lik qatorlar (bloat) uchun * 1.3 = taxminan 7.6 GB

-- Indekslar. B-tree yozuvi = kalit + 6 bayt TID + header, taxminan 16 bayt.
--   PK (bigint):              73e6 * 16  = 1.2 GB
--   (user_id, created_at):    73e6 * 32  = 2.3 GB
--   idempotency_key (uuid):   73e6 * 40  = 2.9 GB
-- Jami indeks 6.4 GB, jadvaldan bir xil kattalikda. Bu normal.

-- Haqiqatni tekshirish (taxmin emas, o'lchov):
SELECT pg_size_pretty(pg_relation_size('orders'))        AS heap,
       pg_size_pretty(pg_indexes_size('orders'))         AS indekslar,
       pg_size_pretty(pg_total_relation_size('orders'))  AS jami;
```

Hisob darhol qaror beradi: 14 GB jami hajm 64 GB RAM'li serverda to'liq cache'ga sig'adi, demak partitioning kerak emas. Kuniga 20 million qator kelsa bir yilda 1.4 TB chiqadi va oylik partitioning majburiy bo'ladi.

### 8.6 O'rtacha emas, p95 va p99 ga qarash sababi

O'rtacha kechikish haqiqatni yashiradi. Agar 95 foiz so'rov 10 ms da, 5 foizi 2000 ms da bajarilsa, o'rtacha 109 ms chiqadi va grafik "yaxshi" ko'rinadi. Lekin har yigirmanchi mijoz to'lov sahifasida ikki sekund kutadi.

```java
// Micrometer: faqat o'rtacha emas, taqsimot chop etilsin.
@Bean
MeterRegistryCustomizer<MeterRegistry> persentillar() {
    return registry -> registry.config().meterFilter(
        new MeterFilter() {
            @Override
            public DistributionStatisticConfig configure(
                    Meter.Id id, DistributionStatisticConfig config) {
                if (!id.getName().startsWith("payment.")) return config;
                return DistributionStatisticConfig.builder()
                        // p95/p99 ni server tomonda emas, histogram'dan hisoblash
                        .percentilesHistogram(true)
                        .serviceLevelObjectives(
                            Duration.ofMillis(50).toNanos(),
                            Duration.ofMillis(200).toNanos(),
                            Duration.ofMillis(1000).toNanos())
                        .build().merge(config);
            }
        });
}
```

Ikkinchi sabab fan-out. Bitta sahifa 20 ta servisga parallel murojaat qilsa va har birining p99 si 500 ms bo'lsa, kamida bittasi sekin chiqish ehtimoli 1 - 0.99^20 = taxminan 18 foiz. Servis darajasidagi p99 sahifa darajasida p82 ga aylanadi. Uchinchi sabab: "p99 < 300 ms" degan SLO tekshiriladi, "o'rtacha tez bo'lsin" degani esa yo'q.

Yana bir qoida: bir nechta instansiyaning p99 qiymatini o'rtachalashtirish matematik jihatdan xato. Persentil faqat xom histogram bucket'lar qo'shilgandan keyin hisoblanadi, Prometheus'da buni `histogram_quantile` qiladi.

### 8.7 Tarmoq safari soni: bitta so'rovda nechta tashqi chaqiruv bor

Kechikish manbasi ko'pincha bitta sekin so'rov emas, ketma-ket kelgan o'nlab tez so'rov. N+1 muammosi aynan shu: 50 buyurtma uchun 51 ta `SELECT`.

```java
// YOMON: ketma-ket safarlar. Kechikish qo'shiladi.
// 1 (buyurtma) + 50 (pozitsiyalar) + 1 (mijoz) + 1 (bank) = 53 safar
// 53 * 0.8 ms (DB) + 80 ms (bank) = taxminan 122 ms, bunda CPU deyarli bo'sh.

// YAXSHI: safarlar sonini kamaytirish va qolganini parallellashtirish.
var mijoz = CompletableFuture.supplyAsync(() -> mijozRepo.topish(id), pool);
var limit = CompletableFuture.supplyAsync(() -> limitClient.olish(id), pool);
// Pozitsiyalarni bitta so'rov bilan: @EntityGraph yoki join fetch
var buyurtma = buyurtmaRepo.topishPozitsiyalarBilan(buyurtmaId);
CompletableFuture.allOf(mijoz, limit).join();
// Yangi hisob: 1 + 1 + max(1 ta parallel safar) + 80 ms = taxminan 82 ms

// Java 21+ da strukturali variant (virtual thread'lar bilan):
try (var scope = new StructuredTaskScope.ShutdownOnFailure()) {
    var m = scope.fork(() -> mijozRepo.topish(id));
    var l = scope.fork(() -> limitClient.olish(id));
    scope.join().throwIfFailed();
}
```

Arxitektor har bir muhim endpoint uchun bitta raqamni biladi: safarlar soni. Uni taxmin qilish shart emas, trace bor. Jaeger yoki Zipkin'da span daraxtini ochib sanash yetarli, 8 dan ko'p ketma-ket span bo'lsa batching yoki parallellashtirish imkoni bor.

### 8.8 Serializatsiya, JSON va ortiqcha ma'lumot tashishning narxi

JSON arzon ko'rinadi, lekin hajm oshganda narx ikki joyda to'lanadi: CPU va tarmoq.

```java
// Hisobot endpoint'i: 50 000 qator, har biri 40 maydon.
// Taxminiy JSON hajmi: 50_000 * 40 * 25 bayt = 50 MB
// Jackson serializatsiya tezligi: taxminan 150-250 MB/s bitta yadroda
//   -> 50 MB / 200 MB/s = 250 ms faqat yozishga, CPU 100% band
// Mijoz tomonda parse: yana taxminan 300 ms
// 1 Gbit/s tarmoqda uzatish: 50 MB / 125 MB/s = 400 ms
// Jami taxminan 1 sekund, va 50 MB byte[] to'g'ridan-to'g'ri old gen'ga tushadi.

// Yechim 1: gzip. JSON 6-10 barobar siqiladi -> 50 MB dan 6 MB ga.
//   Qo'shimcha CPU: taxminan 30 ms. Bu juda foydali savdo.
// Yechim 2: faqat kerakli maydonlarni tanlash (projection).
//   40 maydondan 6 tasi kerak bo'lsa, hajm 50 MB dan 8 MB ga tushadi.
// Yechim 3: 50 000 qatorni umuman bitta javobda bermaslik.
//   Keyset pagination yoki fayl eksporti (CSV + S3 link).
```

Eng ko'p uchraydigan xato: entity'ni to'g'ridan-to'g'ri JSON qilib qaytarish, u ortiqcha maydonlarni va bog'lanishlarni tortib keladi. 100 qatorda sezilmaydi, 50 000 qatorda servisni yiqitadi: ro'yxat va hisobot endpoint'larida doim DTO yoki projection ishlatiladi.

### 8.9 Qachon kesh kerak emas: ma'lumotlar bazasi allaqachon yetarli

Kesh bepul emas: u invalidatsiya muammosini, nomuvofiqlik oynasini (stale window) va yangi nosozlik nuqtasini olib keladi. Shuning uchun kesh qo'shishdan oldin raqam bilan isbot kerak.

```sql
-- Oldin shuni tekshiring: ma'lumotlar bazasi allaqachon kesh.
-- shared_buffers + OS page cache = aslida sizning L2 keshingiz.
SELECT heap_blks_hit, heap_blks_read,
       round(100.0 * heap_blks_hit /
             nullif(heap_blks_hit + heap_blks_read, 0), 2) AS hit_foiz
FROM pg_statio_user_tables WHERE relname = 'ombor_qoldigi';
-- hit_foiz 99.5 bo'lsa, so'rov RAM'dan o'qiyapti: Redis 0.4 ms tarmoq
-- safarini qo'shadi, PostgreSQL esa 0.3 ms da javob beradi. Kesh ZARAR.

-- Keyin aniq raqamni ko'ring:
EXPLAIN (ANALYZE, BUFFERS)
SELECT qoldiq FROM ombor_qoldigi WHERE sku = 'A-1024' AND ombor_id = 7;
-- Execution Time: 0.21 ms, Buffers: shared hit=4
```

Kesh kerak bo'lmaydigan holatlar: so'rov 1 ms dan tez; ma'lumot tez o'zgaradi (ombor qoldig'i); o'qish soni past (kuniga 500 marta); nomuvofiqlik narxi yuqori (hisob balansi). Kesh foydali bo'ladigan holat: o'qish/yozish nisbati 100:1 dan yuqori, hisob qimmat, va bir necha sekundlik eskilik qabul qilinadi, masalan valyuta kursi yoki mahsulot katalogi.

| Vaziyat | Oddiy yondashuv | Arxitektor yondashuvi |
|---|---|---|
| Kuniga 4 mln so'rov keldi | "Kafka va sharding kerak" | 46 RPS, bitta instansiya yetadi, hisob qilib isbotlaydi |
| Sekin endpoint | Random joyga Redis qo'yadi | Trace ochadi, safarlar sonini sanaydi, N+1 ni tuzatadi |
| Thread pool sozlash | 200 qo'yadi, "ko'p yaxshi" deydi | Little qonuni bilan 64 chiqaradi, DB pool'ni alohida hisoblaydi |
| Connection pool | Har servisga 50, jami 300 | DB vaqtidan 15 chiqaradi, `max_connections` ga sig'dirib tekshiradi |
| Monitoring | O'rtacha latency grafigi | p95, p99 va histogram, fan-out ta'sirini hisoblaydi |
| Jadval o'sishi | "Keyinroq ko'ramiz" | qator kattaligi * kunlik oqim * 365, partitioning qarori bugun |
| Hisobot 50 000 qator | Entity ro'yxatini JSON qiladi | Projection + gzip, yoki CSV eksport, hajmni oldin hisoblaydi |
| Tashqi API sekinlashdi | Thread pool'ni oshiradi | Bulkhead va timeout, chegara API tomonda ekanini biladi |
| Optimallashtirish | Kodga qarab taxmin qiladi | profiler va `EXPLAIN ANALYZE` bilan o'lchab topadi |
| GC pauzasi | Heap'ni ikki barobar oshiradi | allokatsiya tezligini o'lchaydi, ortiqcha obyektni yo'qotadi |

### 8.10 O'lchovsiz optimallashtirish: taxmin qilib emas, o'lchab tuzatish

Napkin math qaysi joyni o'lchashni aytadi, lekin o'lchov o'rnini bosmaydi. Tartibi shunday: hisobla, o'lch, tuzat, yana o'lch.

```bash
# 1) Qaysi so'rov jami vaqtni yeyayotganini toping (taxmin emas, fakt).
psql -c "SELECT calls, round(mean_exec_time::numeric,2) AS ortacha_ms,
                round(total_exec_time::numeric/1000,1) AS jami_sek, query
         FROM pg_stat_statements ORDER BY total_exec_time DESC LIMIT 10;"
# Diqqat: 0.4 ms lekin 2 mln marta chaqirilgan so'rov,
# 900 ms lekin kuniga 3 marta ishlaganidan 600 barobar qimmat.

# 2) JVM tomonida: async-profiler bilan 30 sekundlik wall-clock profil.
./profiler.sh -d 30 -e wall -f /tmp/payment.html <pid>

# 3) Allokatsiya tezligi va GC. 300 MB/s dan yuqori bo'lsa, sabab izlang.
jcmd <pid> GC.heap_info
java -Xlog:gc*:file=/var/log/gc.log:time,uptime:filecount=5,filesize=20M ...

# 4) Yuklama testi. O'zgarishdan oldin va keyin bir xil skript bilan.
#    k6 yoki Gatling, p95/p99 ni solishtirish uchun.
```

Eng ko'p vaqt "bu yer sekin bo'lsa kerak" degan taxminga ketadi. Haqiqiy sabab ko'pincha boshqa joyda: ortiqcha log, `toString` ichidagi JSON, katta kolleksiyada dirty checking yoki `ThreadLocal` to'planishi. Shuning uchun har bir performance o'zgarishidan oldin bitta son yoziladi (p99 = 480 ms) va keyin qayta o'lchanadi. Son o'zgarmasa, o'zgarish bekor qilinadi.

| Tuzoq | Nega yuzaga keladi | Yechim |
|---|---|---|
| Connection pool DB sig'imidan katta | Har servis alohida sozlangan | Jami pool'ni `max_connections` ga sig'dirish, pgbouncer |
| Tranzaksiya ichida tashqi HTTP chaqiruv | `@Transactional` metodga client qo'shilgan | Chaqiruvni tranzaksiyadan tashqariga chiqarish, outbox |
| O'rtacha latency yashiradi | Dashboard faqat `mean` ko'rsatadi | Histogram va p95/p99, SLO ni persentilda yozish |
| Keraksiz kesh nomuvofiqlik keltirdi | Kesh profilaktika uchun qo'yilgan | `EXPLAIN ANALYZE` bilan isbot, 1 ms so'rovga kesh qo'ymaslik |
| N+1 faqat prod'da ko'rinadi | Test ma'lumoti 5 qator | Testda so'rov sonini tekshirish, statistikani o'lchash |
| Indeks jadvaldan katta | Har ustunga indeks qo'yilgan | Ishlatilmagan indekslarni `pg_stat_user_indexes` dan topib olib tashlash |
| Katta JSON old gen'ni to'ldiradi | Butun ro'yxat bir javobda | Pagination, streaming yoki fayl eksporti |
| Thread pool o'sishi yordam bermaydi | Chegara pastdagi resursda | Little qonuni bilan haqiqiy bottleneck'ni topish |

### 8.11 Amalda qo'llash

- [ ] Eng yuklamali 5 endpoint uchun kunlik so'rov sonini oling, RPS va cho'qqi koeffitsientini (o'rtacha * 6) hisoblab, hujjatga yozib qo'ying.
- [ ] Har bir servisning HikariCP `maximum-pool-size` qiymatini Little qonuni bilan qayta hisoblang, instansiya soniga ko'paytirib PostgreSQL `max_connections` bilan solishtiring.
- [ ] Asosiy 3 jadval uchun qator kattaligi, indeks hajmi va bir yillik o'sishni hisoblab, natijani `pg_total_relation_size` bilan tekshiring.
- [ ] Dashboard'dagi o'rtacha latency grafiklarini p95 va p99 ga almashtiring, muhim endpoint'lar uchun SLO qiymatini persentilda yozing.
- [ ] `pg_stat_statements` ni yoqib, `total_exec_time` bo'yicha top 10 so'rovni haftada bir ko'rib chiqishni jarayonga kiriting.
- [ ] Eng muhim 2 endpoint uchun trace ochib, ketma-ket tarmoq safarlari sonini sanang va 8 dan ko'p bo'lsa batching rejasini tuzing.
- [ ] 1 MB dan katta javob qaytaradigan endpoint'larni toping, gzip yoqilganini tekshirib, entity o'rniga projection ga o'tkazing.
- [ ] Mavjud har bir kesh uchun o'sha so'rovning `EXPLAIN (ANALYZE, BUFFERS)` natijasini yozib qo'ying, 1 ms dan tez bo'lsa keshni olib tashlashni taklif qiling.


# II. Java chuqur bilim

## 9. JVM ichki tuzilishi: class loading, memory model, JIT (JVM Internals)

Arxitektor JVM ni "qora quti" deb qarasa, ishlab chiqarishdagi har bir g'alati holat uchun tushuntirish topa olmaydi. Nega to'lov servisi deploy dan keyin birinchi 90 sekundda p99 ni 40 ms dan 900 ms ga ko'taradi, nega hisobot generatori heap da joy bor paytda ham `OutOfMemoryError` beradi, nega bitta `volatile` olib tashlansa ombor qoldig'i hisoblovi bir necha kundan keyin xato qiymat ko'rsatadi. Javob bitta joyda: JVM ichida xotira qanday bo'linadi, class qanday yuklanadi, kod qanday kompilyatsiya qilinadi va kompilyatsiya qachon bekor qilinadi. Quyida shu mexanika va undan chiqadigan qarorlar.

### 9.1 JVM xotira hududlari: heap, metaspace, stack, code cache, direct buffer

`-Xmx` konteynerning butun xotirasi emas. Process ning RSS i heap dan tashqari yana bir qancha hududni o'z ichiga oladi va ularning har biri alohida chegara bilan boshqariladi. Heap da obyektlar yashaydi. Metaspace da class metadata, method struktura, constant pool yashaydi va u native xotiradan olinadi. Har bir thread o'z stack ini oladi, 64-bit Linux da default taxminan 1 MB. Code cache da JIT chiqargan mashina kodi turadi, tiered compilation yoqilgan holatda default taxminan 240 MB rezerv qilinadi. Direct buffer esa Netty, NIO va ba'zi driver lar ishlatadigan heap dan tashqari bufer.

Amaliy hisob: 300 ta platform thread faqat stack uchun taxminan 300 MB oladi. Shuning uchun `-Xmx` ni qattiq raqam bilan emas, foiz bilan berish ishonchliroq.

```bash
# Konteynerda xotira chegaralarini foiz bilan berish
java -XX:MaxRAMPercentage=70 \
     -XX:InitialRAMPercentage=70 \
     -XX:MaxMetaspaceSize=256m \
     -XX:MaxDirectMemorySize=256m \
     -XX:ReservedCodeCacheSize=192m \
     -Xss512k \
     -XX:+AlwaysPreTouch \
     -XX:+HeapDumpOnOutOfMemoryError \
     -XX:HeapDumpPath=/var/dumps \
     -XX:+ExitOnOutOfMemoryError \
     -jar payment-service.jar

# Haqiqatda qancha native xotira ketganini ko'rish
java -XX:NativeMemoryTracking=summary -jar payment-service.jar
jcmd <pid> VM.native_memory summary
jcmd <pid> GC.heap_info
jcmd <pid> Compiler.codecache
```

`-XX:+AlwaysPreTouch` heap sahifalariga ishga tushishda bir marta tegib chiqadi. Start vaqti bir necha yuz millisekund uzayadi, lekin birinchi yuklamadagi sahifa xatolari tufayli paydo bo'ladigan latency sakrashi yo'qoladi. Uzoq yashaydigan servis uchun bu yaxshi savdo, qisqa batch job uchun yo'q.

| Tuzoq | Nima sodir bo'ladi | Yechim |
|---|---|---|
| `-Xmx` konteyner limitiga teng | Metaspace va stack qo'shilib OOMKilled | `MaxRAMPercentage=70`, qolganini native uchun qoldirish |
| Metaspace cheklanmagan | Dinamik proxy va class generatsiya sekin o'sadi, node ni yeydi | `MaxMetaspaceSize` qo'yib, `class+load` ni kuzatish |
| Direct buffer leak | Heap bo'sh, lekin process o'ladi | `MaxDirectMemorySize` va NMT bilan tekshirish |
| Code cache to'lib qoladi | "CodeCache is full" ogohlantirishi, JIT o'chadi, hamma kod sekinlashadi | `ReservedCodeCacheSize` oshirish |
| Thread pool juda katta | Faqat stack uchun yuzlab MB | `Xss` kamaytirish yoki pool qisqartirish |
| Heap dump sozlanmagan | OOM dan keyin tahlil uchun hech narsa yo'q | `HeapDumpOnOutOfMemoryError` + mount qilingan papka |
| `OmitStackTraceInFastThrow` default | Takrorlanuvchi exception stack trace siz keladi | diagnostika paytida `-XX:-OmitStackTraceInFastThrow` |
| CPU limiti noto'g'ri ko'rinadi | GC va JIT thread soni xato tanlanadi | `-XX:ActiveProcessorCount` bilan aniq berish |

### 9.2 Class loading bosqichlari va class loader ierarxiyasi

Class yuklash uch bosqichdan iborat. Loading da bytecode topiladi va `Class` obyekti yaratiladi. Linking uch qismga bo'linadi: verification bytecode ni xavfsizlik va tiplar bo'yicha tekshiradi, preparation static maydonlarga default qiymat beradi, resolution esa constant pool dagi havolalarni haqiqiy class va method ga bog'laydi. Initialization da `static` blok va `static` maydon initsializatorlari ishlaydi, aynan shu bosqich faqat bir marta va thread-safe bajariladi.

JDK 9 dan beri ierarxiya shunday: bootstrap loader platform modullarini yuklaydi, platform loader JDK ning qolgan qismini, application loader esa classpath ni. Eski `ext` mexanizmi yo'q. Qoida oddiy: bola loader avval otasidan so'raydi, faqat u topa olmasa o'zi qidiradi. Shu sabab `javax.sql.DataSource` ni classpath ga qo'shib qo'yishning ma'nosi yo'q, platform loader uni har doim birinchi topadi.

```bash
# Qaysi class qaysi manbadan yuklangani
java -Xlog:class+load=info:file=/tmp/classload.log -jar order-service.jar

# Faqat bitta class ni kuzatish
grep 'com.shop.order.OrderService' /tmp/classload.log

# Loader lar bo'yicha statistika va class unload
jcmd <pid> VM.classloader_stats
java -Xlog:class+unload=info -jar order-service.jar
```

Bundan ikkita amaliy xulosa chiqadi. Birinchisi, `class+load` logida bitta class ikkita turli jar dan ko'rinsa, bu dependency konflikti va uning oqibati runtime da `NoSuchMethodError` bo'ladi. Ikkinchisi, static blokda fayl yoki tarmoq chaqiruvi bo'lsa, bu class ga birinchi tegadigan thread qolgan thread larni initialization lock da kutishga majbur qiladi.

### 9.3 Spring Boot fat jar va uning class loading ga ta'siri

Spring Boot fat jar oddiy jar emas. Ichida `BOOT-INF/classes` va `BOOT-INF/lib/*.jar` turadi, ya'ni jar ichida jar. Standart `JarFile` bunday tuzilmani ocha olmaydi, shuning uchun Boot o'z launcher ini va o'z class loader ini ishlatadi. Boot 3.2 dan beri launcher sinflari `org.springframework.boot.loader.launch` paketida va ichki jar larga `nested:` protokoli bilan murojaat qilinadi.

Bu arxitekturaga uchta amaliy ta'sir qiladi. Birinchisi, ichki jar lar siqilmagan holda saqlanadi, shuning uchun fat jar hajmi odatdagidan katta ko'rinadi. Ikkinchisi, class topish yo'li bir pog'ona uzayadi, demak ishga tushish vaqti biroz oshadi. Uchinchisi va eng muhimi, CDS va AOT kabi optimizatsiyalar fat jar ichida yaxshi ishlamaydi, ularga yoyilgan tuzilma kerak.

```bash
# Fat jar ni qatlamlarga yoyish (Docker cache uchun va CDS uchun)
java -Djarmode=tools -jar payment-service.jar list-layers
java -Djarmode=tools -jar payment-service.jar extract --destination /app

# Yoyilgan holatda ishga tushirish: launcher o'rniga oddiy classpath
java -XX:+UseG1GC -jar /app/payment-service.jar

# Dependency konfliktini oldindan ko'rish
./mvnw dependency:tree -Dverbose -Dincludes=com.fasterxml.jackson.core
```

Dependency lar alohida Docker qatlamida bo'lsa, faqat ilova kodi o'zgargan deploy da registry ga 200 MB emas, taxminan 2 MB ketadi. Bu CI vaqtini ham, rollout tezligini ham yaxshilaydi.

### 9.4 Bytecode va interpretatsiya: ishga tushish paytidagi sekinlik

Java kompilyatori bytecode chiqaradi, mashina kodi emas. JVM ishga tushganda hamma method interpreter da bajariladi, ya'ni har bir bytecode instruksiya uchun JVM alohida ish qiladi. Interpreter da bajarilish kompilyatsiya qilingan koddan taxminan 10 dan 50 barobar sekin. Ishga tushish paytida nafaqat sizning kodingiz, balki Spring konteyner, Hibernate metamodel qurilishi, Jackson reflection tahlili ham interpreter da ketadi.

Shu sababli 2.5 sekundlik start vaqtining katta qismi haqiqiy ish emas, balki hali qizimagan kodning sekin bajarilishi. Arxitektura xulosasi: start vaqti muhim bo'lgan joyda avval ishlar sonini kamaytirish kerak, flaglarni emas. Keraksiz avtomatik konfiguratsiyani o'chirish, classpath scanning hududini toraytirish, keyin interpretatsiya narxini CDS yoki AOT bilan kamaytirish.

### 9.5 JIT: C1, C2, profil yig'ish, tiered compilation

HotSpot ikkita kompilyatorga ega. C1 tez kompilyatsiya qiladi, lekin optimizatsiyasi yuza. C2 sekin kompilyatsiya qiladi, lekin chiqargan kodi ancha tezroq. Tiered compilation ikkalasini birlashtiradi: method avval interpreter da ishlaydi, keyin C1 ga o'tadi va u yerda profil yig'adi, yetarlicha qizigandan keyin C2 ga uzatiladi.

Beshta daraja bor. 0 bu interpreter. 1 bu C1, profil yig'masdan, trivial method lar uchun. 2 va 3 bu C1 profil bilan. 4 bu C2. Default thresholdlar: `Tier3InvocationThreshold` taxminan 200, `Tier4InvocationThreshold` taxminan 5000.

```bash
# Qaysi method qaysi darajada kompilyatsiya qilinganini ko'rish
java -XX:+PrintCompilation -jar payment-service.jar | head -200

# Faqat C1: start tez, peak sekin (CLI va qisqa job uchun)
java -XX:TieredStopAtLevel=1 -jar report-cli.jar

# Kompilyator thread soni (kichik konteynerda muhim)
java -XX:CICompilerCount=2 -jar payment-service.jar

# Kompilyatsiya thresholdlarining haqiqiy qiymatlari
java -XX:+PrintFlagsFinal -version | grep -E 'Tier[34].*Threshold'
```

`-XX:TieredStopAtLevel=1` qaror nuqtasi sifatida qiziq. Hisobot generatori 20 sekund ishlab tugaydigan CLI bo'lsa, C2 ga qizishga vaqt yetmaydi va C1 da qolish umumiy vaqtni qisqartiradi. Doimiy ishlaydigan to'lov servisida esa bu flag peak throughput ni taxminan ikki barobar tushiradi, ya'ni zarar.

### 9.6 Inlining, escape analysis va boshqa optimizatsiyalar

C2 ning eng katta kuchi inlining da. Chaqirilgan method tanasi chaqiruv joyiga ko'chiriladi va shundan keyin boshqa hamma optimizatsiya ishlay oladi. `MaxInlineSize` default taxminan 35 bytecode, tez-tez chaqiriladigan method uchun `FreqInlineSize` taxminan 325. Shuning uchun uzun method inline bo'lmaydi va u bilan birga ichidagi butun optimizatsiya zanjiri uziladi. Kichik method lar yozish uslub masalasi emas, performance masalasi.

Escape analysis obyekt method chegarasidan chiqmasligini aniqlaydi. Chiqmasa, allokatsiya umuman bajarilmaydi, maydonlar registr yoki stack da saqlanadi. Shu bilan birga lock lar ham olib tashlanadi, agar obyekt faqat bitta thread ga ko'rinsa.

```java
// Bu Money obyekti method dan chiqmaydi, escape analysis uni yo'q qiladi
private long jamiTiyin(List<OrderLine> lines) {
    long jami = 0;
    for (OrderLine line : lines) {
        Money narx = line.narx();           // allokatsiya yo'qoladi
        jami += narx.tiyin() * line.soni();
    }
    return jami;
}

// Bu esa chiqadi: havola tashqariga qaytadi, allokatsiya qoladi
public Money jami(List<OrderLine> lines) {
    return Money.ofTiyin(jamiTiyin(lines));
}

// Megamorphic chaqiruv: 3 dan ortiq implementatsiya inline bo'lmaydi
public BigDecimal komissiya(PaymentMethod m, BigDecimal summa) {
    return m.komissiya(summa);  // 7 ta implementatsiya bor bo'lsa, virtual chaqiruv
}
```

Oxirgi misol muhim. Interface ning bitta yoki ikkita implementatsiyasi bo'lsa, JIT uni monomorphic yoki bimorphic deb hisoblab inline qiladi. To'lov usullari soni ettiga chiqsa, chaqiruv megamorphic bo'ladi va inline qilinmaydi. Issiq loop da strategiyani har safar tanlash o'rniga, qarorni bir marta loop dan tashqarida qabul qilish samaraliroq.

```bash
# Inlining qarorlarini ko'rish
java -XX:+UnlockDiagnosticVMOptions -XX:+PrintInlining \
     -XX:+PrintCompilation -jar payment-service.jar 2>&1 | grep 'too big'

# Escape analysis va allokatsiya yo'q qilish default yoqilgan, tekshirish
java -XX:+PrintFlagsFinal -version | grep -E 'DoEscapeAnalysis|EliminateAllocations|EliminateLocks'

# Inline chegaralarining haqiqiy qiymatlari
java -XX:+PrintFlagsFinal -version | grep -E 'MaxInlineSize|FreqInlineSize|MaxInlineLevel'
```

### 9.7 Deoptimizatsiya: nega kod birdan sekinlashadi

JIT optimistik taxminlar asosida kod chiqaradi. "Bu `if` hech qachon true bo'lmaydi", "bu interface ning faqat bitta implementatsiyasi bor", "bu havola null emas". Agar taxmin buzilsa, JVM uncommon trap ga tushadi va kompilyatsiya qilingan kodni bekor qiladi, bajarilish interpreter ga qaytadi. Keyin method qaytadan profil yig'adi va qayta kompilyatsiya qilinadi.

Hayotiy misol: to'lov servisi bir oy davomida faqat karta to'lovini ko'radi va JIT shunga moslashadi. Bank o'tkazmasi orqali to'lovlar kelganda o'sha issiq yo'l deoptimizatsiya bo'ladi va latency bir necha sekund ko'tariladi. Yana bir misol: ilgari yolg'iz bo'lgan interface ga ikkinchi implementatsiya qo'shilsa, class hierarchy ga asoslangan inline lar bekor qilinadi.

```bash
# Deoptimizatsiya hodisalarini log qilish
java -Xlog:deoptimization=info:file=/tmp/deopt.log:uptime,tags -jar payment-service.jar

# Eng ko'p takrorlanadigan sabablarni sanash
grep -o 'reason=[a-z_]*' /tmp/deopt.log | sort | uniq -c | sort -rn

```

Arxitektura xulosasi: exception ni oqim boshqarish uchun ishlatmaslik, issiq yo'ldan noyob holatlarni alohida method ga chiqarish. Bu JIT taxminini stabil qiladi. Monitoring uchun xulosa: latency ning sababsiz o'sishini tekshirganda GC va DB dan keyin uchinchi gipoteza deoptimizatsiya bo'lishi kerak.

### 9.8 Isinish (warmup) muammosi va u deployment ga qanday ta'sir qiladi

Yangi pod ko'tarilganda u darhol to'liq tezlikda ishlamaydi. Odatiy manzara: birinchi 5 sekundda context quriladi, keyingi taxminan 30 dan 90 sekundda JIT issiq yo'llarni C2 ga olib chiqadi, shu bilan birga Hibernate query plan cache va HikariCP connection lar to'ladi. Agar load balancer pod ni readiness dan keyin darhol to'liq trafik bilan to'ldirsa, o'sha oynada p99 bir necha barobar oshadi.

Eng arzon yechim bosqichma bosqich trafik berish.

| Masala | Oddiy yondashuv | Arxitektor yondashuvi |
|---|---|---|
| Xotira chegarasi | `-Xmx` ni konteyner limitiga teng qo'yish | `MaxRAMPercentage` + native hudud uchun zahira, NMT bilan tekshirish |
| Start sekinligi | "Java shunchaki sekin" deb qabul qilish | Bean sonini o'lchash, lazy init, keyin CDS yoki AOT |
| Deploy paytidagi latency | Darhol 100% trafik berish | Readiness dan keyin bosqichli trafik, canary, startupProbe |
| JIT sozlash | Internetdan topilgan flag to'plamini ko'chirish | `PrintFlagsFinal` bilan default ni ko'rib, bitta flag ni o'lchab o'zgartirish |
| Konkurensiya | Hamma umumiy maydonga `synchronized` | happens-before zanjirini loyihalash, immutable va `volatile` ni to'g'ri joyda |
| Native image | "Tezroq, demak har joyda ishlatamiz" | Faqat start va xotira muhim bo'lgan servisda, peak throughput ni o'lchagandan keyin |
| Class konflikti | Runtime xatosini kutish | `class+load` logi va dependency tree ni CI da tekshirish |
| Diagnostika | Muammo chiqqanda flag qo'shish | JFR va heap dump ni oldindan doimiy sozlab qo'yish |

```yaml
# Kubernetes: isinish uchun vaqt berish va trafikni asta ko'tarish
readinessProbe:
  httpGet: { path: /actuator/health/readiness, port: 8080 }
  periodSeconds: 5
  failureThreshold: 3
startupProbe:
  httpGet: { path: /actuator/health/liveness, port: 8080 }
  periodSeconds: 5
  failureThreshold: 30        # taxminan 150 sekund start uchun ruxsat
lifecycle:
  preStop:
    exec: { command: ["sleep", "10"] }   # in-flight so'rovlar tugashi uchun
resources:
  requests: { cpu: "1", memory: "1Gi" }
  limits:   { cpu: "2", memory: "2Gi" }
```

```properties
# Isinishni tezlashtiradigan sozlamalar
spring.datasource.hikari.minimum-idle=10
spring.datasource.hikari.maximum-pool-size=20
spring.datasource.hikari.connection-timeout=3000
spring.jpa.properties.hibernate.query.plan_cache_max_size=2048
spring.main.lazy-initialization=false
management.endpoint.health.probes.enabled=true
server.shutdown=graceful
spring.lifecycle.timeout-per-shutdown-phase=30s
```

Diqqat: `spring.main.lazy-initialization=true` start vaqtini qisqartiradi, lekin ishni birinchi so'rovga suradi. Muammoni hal qilmaydi, ko'rinmaydigan joyga ko'chiradi, shuning uchun uni faqat lokal development da yoqish mantiqli.

### 9.9 Java memory model: happens-before, volatile, final maydon kafolatlari

JMM kompilyator, JVM va protsessorga kodni qayta tartiblashga ruxsat beradi. Bitta thread ichida natija o'zgarmaydi, lekin ikki thread bir xil maydon bilan ishlaganda tartib kafolatlanmaydi. Kafolatni happens-before munosabati beradi. Asosiy manbalar: monitor ni bo'shatish va keyin shu monitor ni olish, `volatile` ga yozish va keyin shu maydonni o'qish, thread ni ishga tushirish va uning tugashini kutish, hamda `java.util.concurrent` dagi struktura lar.

```java
// Xato: flag ko'rinishi kafolatlanmagan, loop abadiy davom etishi mumkin
private boolean toxtatildi = false;          // volatile yo'q

// To'g'ri: volatile yozish va o'qish orasida happens-before bor
private volatile boolean toxtatildi = false;

public void toxtat() { toxtatildi = true; }

public void ishla() {
    while (!toxtatildi) {
        qoldiqniHisobla();
    }
}

// final maydon kafolati: konstruktor tugagach boshqa thread to'liq holatni ko'radi
public final class OmborQoldigi {
    private final long tiyin;
    private final Instant vaqt;

    public OmborQoldigi(long tiyin, Instant vaqt) {
        this.tiyin = tiyin;
        this.vaqt = vaqt;
        // DIQQAT: bu yerda this ni tashqariga bermaslik kerak, aks holda kafolat buziladi
    }
}
```

`final` maydon kafolati shartli: konstruktor ichida `this` havolasi tashqariga chiqmasligi shart. Listener ni konstruktor ichida registratsiya qilish aynan shu kafolatni buzadi. Amaliy qoida: umumiy mutable holatni imkon qadar yo'q qilish, qolganida happens-before zanjirini ongli loyihalash. Immutable record, `AtomicLong`, `ConcurrentHashMap` va `BlockingQueue` kafolatni o'zi beradi. `volatile` faqat ko'rinishni beradi, atomiklikni emas: `counter++` ustida u hech narsa hal qilmaydi.

### 9.10 JVM ni kuzatish uchun asosiy flaglar va `-XX:+PrintFlagsFinal` dan foydalanish

Flag haqida taxmin qilmaslik kerak. `-XX:+PrintFlagsFinal` har bir flagning haqiqiy qiymatini va uning manbasini ko'rsatadi. Qiymat yonidagi `{default}` va `{ergonomic}` belgisi muhim: `ergonomic` degani JVM konteyner va CPU ga qarab o'zi tanlagan.

```bash
# Ishlayotgan konfiguratsiyaning haqiqiy qiymatlari
java -XX:+PrintFlagsFinal -version | grep -E 'MaxHeapSize|InitialHeapSize|UseG1GC|UseZGC'

# Faqat default dan farq qiladiganlar
java -XX:+PrintFlagsFinal -version | grep -v 'default'

# Jonli process dan olish, qayta ishga tushirmasdan
jcmd <pid> VM.flags -all
jcmd <pid> VM.command_line

# Doimiy yoqib qo'yiladigan minimal to'plam
java -Xlog:gc*:file=/var/log/gc.log:uptime,level,tags:filecount=5,filesize=20m \
     -XX:+HeapDumpOnOutOfMemoryError -XX:HeapDumpPath=/var/dumps \
     -XX:StartFlightRecording:settings=profile,maxsize=256m,filename=/var/dumps/app.jfr \
     -XX:NativeMemoryTracking=summary \
     -jar payment-service.jar
```

GC log, heap dump va JFR ni muammo chiqqandan keyin yoqish kech. Narxi kichik: GC log amalda sezilmaydi, `NativeMemoryTracking=summary` taxminan 5 dan 10 foiz native xotira ustama beradi. Oldindan sozlab qo'yish incident vaqtida soatlarni tejaydi.

### 9.11 AOT, CDS va GraalVM native image: qachon mantiqli

Uchta variant bir muammoning uch yechimi va narxi butunlay boshqa. CDS class metadata ni arxivga oladi, keyingi start da verification va parsing takrorlanmaydi, start vaqti taxminan 20 dan 35 foizga qisqaradi, kod o'zgarmaydi. JDK 24 dan boshlangan AOT cache bundan ko'proq ish qiladi, link holatini ham saqlaydi. Native image butun ilovani oldindan mashina kodiga kompilyatsiya qiladi, start taxminan 50 ms ga tushadi va xotira sarfi bir necha barobar kamayadi, lekin reflection uchun metadata kerak va peak throughput odatda HotSpot dan past.

```bash
# CDS: training run, keyin arxiv bilan ishga tushirish (yoyilgan tuzilma kerak)
java -Djarmode=tools -jar payment-service.jar extract --destination /app
java -XX:ArchiveClassesAtExit=/app/app.jsa \
     -Dspring.context.exit=onRefresh -jar /app/payment-service.jar
java -XX:SharedArchiveFile=/app/app.jsa -jar /app/payment-service.jar

# AOT cache (JDK 24+): yozib olish va ishlatish
java -XX:AOTMode=record -XX:AOTConfiguration=app.aotconf -jar /app/payment-service.jar
java -XX:AOTMode=create -XX:AOTConfiguration=app.aotconf -XX:AOTCache=app.aot -jar /app/payment-service.jar
java -XX:AOTCache=app.aot -jar /app/payment-service.jar

# Spring AOT bilan native image
./mvnw -Pnative native:compile
./target/payment-service
```

Qaror mezoni oddiy. Uzoq ishlaydigan va yuqori throughput talab qiladigan to'lov servisi uchun CDS yoki AOT cache yetarli va xavfsiz tanlov. Scale-to-zero funksiya yoki kamdan kam ishlaydigan ichki yordamchi servis uchun native image mantiqli. Hibernate va keng reflection ishlatadigan monolitni native image ga ko'chirish odatda foydadan ko'p vaqt oladi.

### 9.12 Amalda qo'llash

- [ ] Har bir servis uchun `jcmd VM.native_memory summary` chiqarib, heap tashqarisidagi xotirani hisoblang va `MaxRAMPercentage` ni shunga qarab 65 dan 75 foizga qo'ying.
- [ ] GC log, `HeapDumpOnOutOfMemoryError` va JFR ni barcha production profilga doimiy yoqib, dump papkasini mount qiling.
- [ ] `-Xlog:class+load=info` bilan bitta start ni yozib, duplikat class va keraksiz jar larni aniqlang, dependency tree tekshiruvini CI ga qo'shing.
- [ ] Fat jar ni `-Djarmode=tools ... extract` bilan qatlamlarga bo'lib, Docker image ni dependency va kod qatlamlariga ajratib qurishga o'tkazing.
- [ ] Bitta servisda CDS arxivi tayyorlab, start vaqtini arxivsiz holat bilan taqqoslang va natijani o'lchov sifatida yozib qo'ying.
- [ ] `-Xlog:deoptimization=info` ni staging da yuklama testi vaqtida yoqib, eng ko'p takrorlanadigan deoptimizatsiya sabablarini ro'yxatga oling.
- [ ] Kubernetes manifestlariga `startupProbe`, graceful shutdown va bosqichli trafik berishni qo'shib, deploy paytidagi p99 sakrashini o'lchang.
- [ ] Umumiy mutable holat ishlatadigan har bir class ni ko'rib chiqib, uni immutable ga, `volatile` ga yoki `java.util.concurrent` strukturasiga o'tkazish bo'yicha qaror yozib qo'ying.

## 10. Garbage collection va xotira sozlash (Garbage Collection and Memory Tuning)

Garbage collector JVM ning eng ko'p noto'g'ri sozlanadigan qismi. Ko'pchilik jamoa uni faqat `OutOfMemoryError` chiqqanda eslaydi, keyin `-Xmx` ni oshiradi va muammo yashiringanday bo'ladi. Arxitektor esa GC ni latency byudjetining bir qismi deb ko'radi: p99 200 ms bo'lsa, GC pauzasi uning qancha ulushini yeyishi oldindan hisoblangan bo'lishi shart.

### 10.1 GC nima uchun kerak va u qaysi muammoni hal qiladi

GC bitta vazifani bajaradi: endi hech kim murojaat qilmaydigan obyektlar xotirasini qaytarib oladi. Evaziga uch narsa to'lanadi: CPU, xotira va pauza.

Muhim nuqta: GC "axlatni" emas, "tirik obyektni" izlaydi. Kollektor GC root lardan (thread stack, static maydon, JNI reference) erishiladigan grafni kezadi, qolgani o'lik hisoblanadi. Shuning uchun GC xarajati o'lik obyektlar soniga emas, TIRIK obyektlar hajmiga bog'liq. Buyurtma servisida 500 ming vaqtinchalik DTO arzon tushadi, lekin 2 GB li cache har marking siklda qayta kezib chiqiladi.

Ikkinchi nuqta: allokatsiya arzon. Har thread o'z TLAB (Thread Local Allocation Buffer) sohasida pointer ni surish bilan obyekt yaratadi, taxminan 10 nanosekunddan kam. Qimmat narsa, obyektning tirik qolib old hududga ko'chishi.

### 10.2 Avlodlar farazi (generational hypothesis) va young/old hudud

Barcha zamonaviy kollektorlar bitta empirik kuzatuvga tayanadi: obyektlarning katta qismi juda yosh holida o'ladi. Hisobot metodidagi `StringBuilder`, JDBC qatorlari, Jackson node lari bir necha millisekund yashaydi. Tirik qolganlar uzoq yashaydi: Spring bean lari, connection pool, cache yozuvlari.

Shundan amaliy natija chiqadi: young hududni tez-tez va arzon yig'ish mumkin. Young collection faqat tirik obyektlarni ko'chiradi, ya'ni ish hajmi survival rate ga proporsional. Young hududda 1 GB dan faqat 30 MB tirik qolsa, pauza taxminan 10 ms bo'ladi.

Old hududni to'liq kezish qimmat, shuning uchun marking application bilan parallel bajariladi. Bu yerda card table va remembered set ishlaydi: old hududdagi obyekt young obyektga reference yozsa, write barrier card ni "dirty" deb belgilaydi. Shu sababli young collection butun old hududni emas, faqat dirty card larni skanerlaydi.

Xulosa: survival rate ni pasaytirish GC ni tezlashtiradi. Har request da 5 MB lik graf yasab uni cache ga tiqish o'sha obyektlarni old hududga promote qiladi va mixed collection ni og'irlashtiradi.

### 10.3 G1GC ishlash tartibi: region, young collection, mixed collection

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

### 10.4 ZGC va Shenandoah: past pauza evaziga nima to'lanadi

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

### 10.5 Serial va Parallel GC: kichik konteynerda qachon mantiqli

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

### 10.6 Qaysi GC ni tanlash: jadval bilan, yadro va xotira hajmiga qarab

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

### 10.7 Heap kattaligini tanlash va `-Xmx` ni konteyner limiti bilan bog'lash

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

### 10.8 GC log ni yoqish va o'qish: pauza vaqti, sabab, hudud hajmi

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

### 10.9 Xotira sizishi (leak) belgilari va heap dump bilan tekshirish

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

### 10.10 Off-heap xotira: direct buffer, Netty, metaspace o'sishi

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

### 10.11 Allokatsiyani kamaytirish: ortiqcha obyekt yaratmaslik amaliyoti

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

### 10.12 Amalda qo'llash

- [ ] Har bir servis uchun GC ni aniq belgilang: 4 vCPU dan kam bo'lsa Serial yoki Parallel, oddiy REST servisga `-XX:+UseG1GC`, qattiq p99 SLA uchun generational ZGC.
- [ ] `-Xmx` konteyner limitiga teng yozilgan joylarni `-XX:MaxRAMPercentage=70.0` ga o'tkazing va `InitialRAMPercentage` ni ham shu qiymatga qo'ying.
- [ ] Barcha prod profillarda `-Xlog:gc*:file=...:filecount=10,filesize=20M` ni yoqing, `-XX:+HeapDumpOnOutOfMemoryError` bilan `HeapDumpPath` ni persistent volume ga yo'naltiring.
- [ ] `jvm.gc.pause`, `jvm.gc.memory.allocated` va after-GC heap metrikalarini dashboard ga chiqarib, GC CPU ulushi 10 foizdan oshganda alert qo'ying.
- [ ] `MaxMetaspaceSize` va `MaxDirectMemorySize` ni har servisda aniq belgilang, reactive stack bo'lsa `io.netty.maxDirectMemory` ni ham sozlang.
- [ ] Eng katta trafikli servisda 120 sekundlik JFR profili oling va `ObjectAllocationSample` bo'yicha top 5 allokatsiya manbasiga ticket yarating.
- [ ] Butun jadvalni yoki faylni xotiraga yuklaydigan kodlarni pagination yoki stream ga o'tkazib humongous allokatsiyani yo'qoting.
- [ ] Yuklama testiga GC regressiya tekshiruvini qo'shing: release dan oldin va keyin p99 pauza va after-GC qoldiqni solishtirib, farq 20 foizdan oshsa to'xtating.

## 11. Concurrency: thread, lock, atomic, happens-before (Java Concurrency)

Konkurentlik kodni tezlashtirmaydi, u kodni qimmatlashtiradi. To'lov servisi sekundiga 2000 so'rovni ko'tarishi uchun ko'p oqimli bo'lishi shart, lekin har bir umumiy o'zgaruvchi, har bir singleton bean maydoni va har bir lock shu narxga qo'shimcha qator qo'shadi. Arxitektor uchun asosiy savol "qanday parallellashtiraman" emas, "qaysi holat umumiy va uni kim qanday tartibda ko'radi" degan savol. Bu bobda JVM ichida nima sodir bo'lishini, Java Memory Model qanday kafolat berishini va Spring konteynerida bu kafolatlar qanday buzilishini ko'rib chiqamiz.

### 11.1 Parallellik va konkurentlik farqi, qaysi muammoni hal qilamiz

Konkurentlik bir nechta ishni bir vaqtda boshqarish haqida, parallellik esa ularni bir vaqtda bajarish haqida. Buyurtma servisi 200 ta so'rovni navbatga olib, bittadan ishlasa, bu konkurent lekin parallel emas. Shu farq muhim, chunki ikki holatda butunlay boshqa muammo hal qilinadi: konkurentlik resursni kutish vaqtini to'ldiradi, parallellik CPU vaqtini qisqartiradi.

Amalda arxitektor ikki qonunga tayanadi. Birinchisi Little qonuni: kerakli bir vaqtdagi ish soni throughput ni latency ga ko'paytirganga teng. Hisobot servisi 500 RPS ni 200 ms latency bilan ushlasa, tizimda doim taxminan 100 ta faol so'rov yashaydi, demak thread pool va DB connection pool shuni ko'tarishi kerak. Ikkinchisi Amdahl qonuni: agar ishning 5 foizi ketma-ket bo'lsa, 32 yadroda maksimal tezlanish taxminan 14 barobar, 64 yadroda esa faqat 15 barobar. Ya'ni bitta global lock ostidagi 5 foizlik kod butun gorizontal o'sishni o'ldiradi.

Shu sababli birinchi qaror doim arxitektura darajasida bo'ladi: umumiy holatni yo'q qilish, bo'lib tashlash yoki tashqi tizimga (PostgreSQL, Redis) ko'chirish. Lock qo'yish uchinchi variant, eng oxirgi variant.

### 11.2 Thread holatlari, kontekst almashinuvi va uning narxi

Java threadining holatlari oltita: NEW, RUNNABLE, BLOCKED, WAITING, TIMED_WAITING, TERMINATED. Bu yerda bitta tuzoq bor: RUNNABLE holati thread CPU da ishlayotganini bildirmaydi. Socket dan o'qiyotgan thread ham RUNNABLE ko'rinadi, chunki JVM OS darajasidagi IO kutishini ajratmaydi. BLOCKED faqat monitor kutishini, WAITING esa `Object.wait`, `LockSupport.park` yoki `Future.get` ni bildiradi.

Platform thread OS threadiga bir-bir mos keladi. Uning stack hajmi 64-bitli HotSpot da odatda 1 MB (`-Xss` bilan sozlanadi), bu heapdan tashqari xotira. 2000 ta thread taxminan 2 GB virtual manzil maydonini oladi, shuning uchun 200 dan ortiq platform thread ishlatish deyarli har doim dizayn xatosi. Kontekst almashinuvi o'zi arzon ko'rinadi (taxminan 1-5 mikrosekund), lekin asl narx L1 va L2 cache ning sovishi: threadning ish to'plami cache dan chiqib ketadi va qayta yuklanadi.

Java 21 dan virtual thread (JEP 444) bu hisobni o'zgartirdi. Virtual thread stacki heapda yashaydi, blokirovka bo'lganda carrier thread dan yechiladi, shuning uchun 100 000 ta virtual thread normal holat. Lekin virtual thread IO uchun, CPU uchun emas: hisob-kitob og'ir bo'lsa, carrier pool (default o'lchami yadro soniga teng) baribir to'yinadi. Spring Boot 3.2 dan `spring.threads.virtual.enabled=true` bilan web va `@Async` ijrochilari virtual threadga o'tadi.

### 11.3 Umumiy holat (shared state) muammosi: poyga sharti va ko'rinuvchanlik

Konkurentlik xatolarining ikki turi bor va ular bir-biriga o'xshamaydi. Poyga sharti (race condition) atomarlik yo'qligidan kelib chiqadi: `balance = balance - amount` uch amaldan iborat, o'rtada boshqa thread kirib ketadi. Ko'rinuvchanlik (visibility) muammosi esa boshqa: bir thread yozgan qiymatni ikkinchi thread hech qachon ko'rmasligi mumkin, chunki qiymat CPU store buffer ida qolgan yoki JIT uni registrga ko'tarib (hoisting) tsikldan chiqarib tashlagan.

Java Memory Model bu yerda happens-before munosabati bilan ishlaydi. Amalda kerakli to'rt qoida: monitor dan chiqish keyingi kirishdan oldin sodir bo'ladi; `volatile` ga yozish keyingi o'qishdan oldin sodir bo'ladi; `Thread.start()` chaqirilishi yangi thread ichidagi hamma ishdan oldin; `Thread.join()` tugashi o'sha thread ishidan keyin. Agar ikki amal orasida happens-before bo'lmasa, JVM ularni istalgan tartibda ko'rsatishga haqli.

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

### 11.4 `synchronized`, `ReentrantLock`, `ReadWriteLock` va `StampedLock` farqi

`synchronized` eng arzon va eng ishonchli variant. HotSpot uni bosqichma-bosqich kuchaytiradi: avval thin lock (CAS bilan object header ga yozish), raqobat paydo bo'lsa inflate qilib monitor obyektiga o'tadi. Raqobatsiz holatda narxi taxminan 20 nanosekund, raqobat bo'lsa yuzlab nanosekundga chiqadi. Kamchiligi: timeout yo'q, uzilishga javob bermaydi, bitta shart o'zgaruvchisi bilan cheklangan.

`ReentrantLock` shu kamchiliklarni yopadi: `tryLock(200, MILLISECONDS)`, `lockInterruptibly()`, bir nechta `Condition`, va `fair=true` rejimi. Fair rejim navbatni kafolatlaydi, lekin throughput ni bir necha barobar tushiradi, shuning uchun uni faqat ochlik real muammo bo'lganda yoqadilar.

`ReentrantReadWriteLock` o'qish ko'p, yozish kam bo'lgan holatga mo'ljallangan. Lekin o'qish lockining o'zi umumiy counter ni CAS bilan yangilaydi, demak 16 yadroda o'qish ham cache line uchun kurashadi. Amalda u faqat kritik bo'lim uzun bo'lganda (mikrosekundlar, nanosekundlar emas) foyda beradi.

`StampedLock` optimistik o'qishni qo'shadi: `tryOptimisticRead` hech narsa yozmaydi, keyin `validate` yozuvchi kirganini tekshiradi. U reentrant emas, `Condition` bermaydi va noto'g'ri ishlatilsa ma'lumot yarim o'qilgan holatda qoladi.

| Mexanizm | Qachon | Narx | Asosiy xavf |
|---|---|---|---|
| `synchronized` | qisqa kritik bo'lim, oddiy holat | eng past, raqobatsiz ~20 ns | timeout yo'q, JDK 23 gacha virtual thread ni pin qiladi |
| `ReentrantLock` | timeout, interrupt, bir nechta Condition kerak | `synchronized` ga yaqin | `unlock` ni `finally` da yozish esdan chiqadi |
| `ReentrantReadWriteLock` | o'qish/yozish nisbati 10:1 dan yuqori, bo'lim uzun | o'qish ham CAS qiladi | yozuvchi ochligi, fair rejim sekin |
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

### 11.5 Atomic sinflar va CAS: qachon lock dan tezroq

`AtomicInteger`, `AtomicLong` va `AtomicReference` lock ishlatmaydi, ular CPU ning compare-and-swap buyrug'iga tayanadi: eski qiymatni o'qish, yangi qiymatni hisoblash, atomar almashtirish, muvaffaqiyatsiz bo'lsa qaytadan urinish. Raqobat past bo'lganda bu lock dan 2-5 barobar tez. Raqobat yuqori bo'lganda esa teskari effekt: har bir muvaffaqiyatsiz urinish cache line ni boshqa yadrodan tortib oladi, CPU bo'sh aylanadi.

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

### 11.6 `volatile` nimani kafolatlaydi va nimani kafolatlamaydi

`volatile` ikki narsani beradi. Birinchisi ko'rinuvchanlik: yozish darhol boshqa threadlarga ko'rinadi, o'qish esa cache dan emas, aktual qiymatdan bo'ladi. Ikkinchisi tartib: `volatile` yozishdan oldingi barcha yozishlar o'sha `volatile` ni o'qigan thread uchun ko'rinadi, bu happens-before chegarasi.

`volatile` bermaydigan narsa esa atomarlik. `volatile int counter; counter++` hamon buzuq, chunki bu o'qish, qo'shish va yozishdan iborat. Shuningdek `volatile` massiv elementlariga ta'sir qilmaydi: `volatile int[] a` da havola volatile, `a[0]` esa yo'q.

Amalda `volatile` uchun ikki to'g'ri holat bor. Birinchisi to'xtatish flagi: background job `volatile boolean running` ni tekshiradi. Buning yo'qligida JIT tsikldan tashqariga ko'tarib tashlaydi va thread hech qachon to'xtamaydi. Ikkinchisi bir marta yoziladigan konfiguratsiya havolasi: feature flag snapshoti yoki qayta yuklanadigan narx jadvali, bunda immutable obyekt butunlay almashtiriladi.

Spring da `@Value` bilan to'ldirilgan maydonlar konstruktor tugaganidan keyin set qilinadi. Agar bean o'z konstruktorida thread ochib yuborsa, o'sha thread yarim initsializatsiya qilingan beanni ko'rishi mumkin. Shuning uchun thread ochish `@PostConstruct` da yoki `SmartLifecycle` da bo'lishi kerak, konstruktorda emas.

### 11.7 Thread-safe to'plamlar: `ConcurrentHashMap`, `CopyOnWriteArrayList` va ularning narxi

`Collections.synchronizedMap` butun map ni bitta monitorga o'raydi, shuning uchun u 4 yadrodan keyin o'smaydi. `ConcurrentHashMap` esa bucket darajasida ishlaydi: bo'sh bucket ga qo'yish CAS bilan, to'lgan bucket ga qo'yish o'sha bucket ning birinchi nodesi ustida `synchronized` bilan. Natijada o'qish deyarli lock siz, yozish esa faqat bir xil bucket ga tushganda raqobatlashadi.

Ikki tuzog'i bor. Birinchisi `size()` va `isEmpty()`: ular bir nechta counter cell ni qo'shadi va aniq snapshot bermaydi, shuning uchun biznes qarorini `size()` ga qurmaslik kerak. Ikkinchisi `computeIfAbsent`: mapping funksiyasi bucket lock ostida bajariladi, demak uning ichida shu map ga yozish yoki uzoq IO qilish deadlock va stall sababi bo'ladi.

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

### 11.8 `ExecutorService`, thread pool turlari va navbat tanlash

`Executors.newFixedThreadPool` va `newCachedThreadPool` ikkisi ham production uchun xavfli. Birinchisi cheksiz `LinkedBlockingQueue` ishlatadi, demak yuklama oshganda navbat heap ni to'ldiradi va ilova `OutOfMemoryError` bilan yiqiladi, backpressure esa hech qachon ishlamaydi. Ikkinchisi cheksiz thread yaratadi.

To'g'ri yo'l `ThreadPoolExecutor` ni qo'lda sozlash. Asosiy mexanika: avval `corePoolSize` gacha thread yaratiladi, keyin navbat to'ldiriladi, navbat to'lgandan keyingina `maximumPoolSize` gacha yangi thread ochiladi. Shuning uchun cheksiz navbat bilan `maximumPoolSize` hech qachon ishlamaydi. Navbat sig'imi chekli bo'lishi va rad etish siyosati ongli tanlanishi kerak: `CallerRunsPolicy` chaqiruvchini sekinlashtirib backpressure beradi, `AbortPolicy` esa so'rovni tez rad etadi.

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

### 11.9 `CompletableFuture` bilan asinxron oqim qurish va xato tarqalishi

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

### 11.10 Deadlock, livelock va ochlik (starvation): sabab va oldini olish

Deadlock to'rt shart bir vaqtda bajarilganda yuzaga keladi: o'zaro istisno, lockni ushlab turib ikkinchisini kutish, lockni tortib olish imkonsizligi, va aylana kutish. Amalda eng ko'p uchraydigani aylana: bitta thread hisob A ni keyin B ni lock qiladi, ikkinchisi teskari tartibda. Yechim eng oddiy shartni buzish: lock olish tartibini global qilib belgilash, masalan hisob ID si bo'yicha o'sish tartibida.

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

### 11.11 Konkurentlik xatolarini topish: thread dump o'qish

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

Konkurentlikni testlash alohida mavzu, testlash qo'llanmasidagi asinxron va konkurentlik testlari bo'limi unga bag'ishlangan. Bu yerda muhimi shuki, bitta ham konkurentlik qarori o'lchovsiz qabul qilinmaydi: har bir lock ortida raqobat metrikasi, har bir pool ortida navbat uzunligi grafigi turishi kerak.

### 11.12 Amalda qo'llash

- [ ] Hamma singleton bean larni ko'rib chiq va o'zgaruvchi maydon topilgan har bir joyni stateless qil yoki immutable obyektga almashtir; `SimpleDateFormat` va `Random` maydonlarini alohida qidir.
- [ ] `Executors.newFixedThreadPool` va `newCachedThreadPool` chaqiruvlarini loyihada qidirib, ularni chekli `queue-capacity` va ongli rad etish siyosatiga ega `ThreadPoolExecutor` ga ko'chir.
- [ ] Har bir pool ga ma'noli `thread-name-prefix` qo'y va `graceful shutdown` uchun `await-termination-period` ni 30 soniyaga sozla.
- [ ] Thread pool kattaligini Little qonuni bilan hisobla, natijani Hikari `maximum-pool-size` bilan solishtir va nisbat teskari bo'lmasligini tasdiqla.
- [ ] `@Async` va `@Transactional` birga ishlatilgan joylarni topib, entity uzatish o'rniga ID uzatishga o'tkaz; `SecurityContextHolder` ga tayangan asinxron kodni alohida belgila.
- [ ] Bir nechta instansiyada ishlaydigan har qanday `synchronized` blokni aniqla va uni PostgreSQL advisory lock yoki `SELECT ... FOR UPDATE` ga ko'chir, `lock_timeout` ni albatta qo'y.
- [ ] Yuklama testi paytida 2 sekund oraliq bilan uchta thread dump olib, `BLOCKED` threadlar sonini va lock egalarini qaydnomaga yozib qo'y.
- [ ] Pool metrikalarini (active, queue size, rejected, completed) Micrometer orqali chiqarib, navbat uzunligi va rad etish soniga alert qo'y.

## 12. Virtual threads, structured concurrency va scoped values (Modern Concurrency)

Virtual thread Java dunyosida bir necha o'n yillik "thread qimmat, shuning uchun uni pool qil" qoidasini bekor qildi. Java 21 da bu imkoniyat barqaror (stable) bo'ldi, Java 24 da eng og'riqli cheklovi olib tashlandi, Java 25 da esa uning atrofidagi ikki yordamchi mexanizm yetildi: scoped values final bo'ldi, structured concurrency hali preview holatida qoldi. Arxitektor uchun bu yerdagi savol "yoqamanmi yoki yo'q" emas, balki "qaysi yuk profilida nima o'zgaradi va qaysi chegara endi bo'g'iz bo'lib qoladi" degan savol. Pastdagi bo'limlar aynan shu mexanikani va undan chiqadigan qarorlarni yig'adi.

### 12.1 Virtual thread nima: carrier thread, mount va unmount mexanikasi

Virtual thread bu JVM boshqaradigan `Thread` obyekti, uning ortida doimiy OS thread turmaydi. Uni ishga tushirish uchun JVM carrier thread kerak qiladi: bu oddiy platform thread, default holda `ForkJoinPool` ichidagi ishchi thread. Virtual thread carrier ustiga **mount** qilinadi, ya'ni uning stack frame'lari carrier thread'ning haqiqiy stack'iga ko'chiriladi va kod shu yerda bajariladi.

Qiziqarli joyi bloklanish paytida boshlanadi. Agar virtual thread blocking I/O ga kirsa (socket read, `Thread.sleep`, `BlockingQueue.take`), JDK ichidagi qayta yozilgan kutubxona kodi OS darajasida bloklanmaydi. U continuation'ni **unmount** qiladi: stack frame'lar carrier stack'dan heap'ga ko'chiriladi (freeze), carrier bo'shaydi va darhol boshqa virtual thread'ni oladi. I/O tayyor bo'lganda scheduler continuation'ni yana biror carrier ustiga qaytaradi (thaw) va kod xuddi hech narsa bo'lmagandek davom etadi.

```java
// Carrier thread nomini ko'rsatish: unmount dan keyin carrier o'zgarishi mumkin
Thread.ofVirtual().start(() -> {
    // Thread.currentThread() har doim virtual thread'ni qaytaradi, carrier'ni emas
    System.out.println(Thread.currentThread()); // VirtualThread[#21]/runnable@ForkJoinPool-1-worker-3
    try {
        Thread.sleep(Duration.ofMillis(50)); // bu yerda unmount sodir bo'ladi
    } catch (InterruptedException e) {
        Thread.currentThread().interrupt();
        return;
    }
    // Qaytganda carrier worker-3 emas, worker-7 bo'lishi mumkin
    System.out.println(Thread.currentThread());
}).join();
```

Scheduler parallelizmi default holda `Runtime.availableProcessors()` ga teng. Ya'ni 8 yadroli mashinada bir vaqtda ko'pi bilan 8 ta virtual thread haqiqatan CPU da ishlaydi, qolgan yuz minglari heap'da continuation ko'rinishida kutib turadi. Buni `jdk.virtualThreadScheduler.parallelism` va `jdk.virtualThreadScheduler.maxPoolSize` system property'lari bilan o'zgartirish mumkin, lekin bu deyarli hech qachon to'g'ri qaror emas: agar parallelizm kamlik qilsa, muammo CPU yukida yoki pinning'da.

### 12.2 Platform thread bilan taqqoslash: xotira, soni, yaratish narxi

Platform thread bir OS thread'ga 1:1 bog'langan. Linux x64 da uning stack'i uchun default `-Xss` 1 MB virtual manzil fazosi band qilinadi, haqiqiy RSS odatda 50-200 KB atrofida bo'ladi, ustiga yadro strukturalari uchun taxminan 8-16 KB qo'shiladi. Shuning uchun amalda 4-8 GB li konteynerda 5000-10000 platform thread chegara, undan yuqorisi scheduler va GC root skanerlashga bosim beradi.

| Xususiyat | Platform thread | Virtual thread |
|---|---|---|
| Stack joylashuvi | OS stack, 1 MB reserve | Heap'dagi stack chunk, boshida taxminan 200-800 bayt |
| Yaratish narxi | taxminan 50-200 mikrosekund | taxminan 1 mikrosekund |
| Amaliy soni | 5-10 ming | 1-5 million |
| Kontekst almashish | OS scheduler, taxminan 1-10 mikrosekund | JVM continuation, taxminan 100-300 nanosekund |
| Scheduling | OS yadrosi, preemptive | JVM, kooperativ (I/O va monitor nuqtalarida) |
| Pool qilish | Majburiy (qimmat resurs) | Zararli anti-pattern |
| `ThreadLocal` | Cheklangan soni, keshlash arzon | Million nusxa, keshlash xotirani yeydi |
| Nom va prioritet | Mavjud va ta'sir qiladi | Nom bo'sh, prioritet e'tiborga olinmaydi |

Eng muhim xulosa: virtual thread arzon bo'lgani uchun uni resurs sifatida ko'rishdan voz kechamiz. `Executors.newVirtualThreadPerTaskExecutor()` har bir vazifaga yangi thread beradi va bu to'g'ri ishlatish usuli. Virtual thread'ni fixed pool'ga solish barcha foydani yo'q qiladi, chunki parallellik yana pool kattaligi bilan cheklanadi.

```java
// 100 000 ta to'lov tekshiruvini bir vaqtda yuborish
try (var executor = Executors.newVirtualThreadPerTaskExecutor()) {
    List<Future<Natija>> natijalar = tolovlar.stream()
        .map(t -> executor.submit(() -> antifraudKlient.tekshir(t))) // har biri alohida virtual thread
        .toList();
    // close() barcha vazifa tugashini kutadi, try-with-resources shuni kafolatlaydi
    for (var f : natijalar) {
        qayta_ishla(f.get());
    }
}
```

### 12.3 Qaysi yuk uchun foyda beradi va qaysi uchun bermaydi

Virtual thread faqat bitta narsani arzonlashtiradi: kutishni. Agar servis vaqtining katta qismini tashqi chaqiruv javobini kutishga sarflasa, foyda katta. Buyurtma yaratish oqimini olaylik: narx servisiga 40 ms, ombor qoldig'iga 30 ms, antifraud'ga 60 ms, keyin bazaga 10 ms. Jami 140 ms, undan 130 ms sof kutish. 200 thread'li Tomcat pool bilan nazariy throughput taxminan 200 / 0.14 = 1400 so'rov/sekund. Virtual thread bilan chegara endi thread sonida emas, pastdagi haqiqiy resursda: baza connection, tashqi servisning rate limit'i, CPU.

CPU bilan band yuk uchun hech qanday foyda yo'q. Hisobot generatsiyasi, JSON ni katta hajmda serializatsiya qilish, shifrlash, in-memory saralash: bularning hammasi carrier thread'ni egallab turadi va unmount sodir bo'lmaydi. 8 yadroda 8 ta carrier bor, 10000 virtual thread CPU ishini bajarsa, ularning hammasi navbatda turadi va latency portlaydi. Bunday yuk uchun yadro soniga teng o'lchamli alohida platform thread pool to'g'ri yechim bo'lib qoladi.

Yana bir nozik holat: virtual thread scheduler preemptive emas. Uzun CPU tsikli ichida (masalan `while` ichida matematik hisob) unmount nuqtasi yo'q, shuning uchun bitta "yovuz" vazifa carrier'ni daqiqalab ushlab turishi mumkin. Bu holat `Thread.yield()` bilan yumshatiladi, lekin to'g'ri javob bunday yukni virtual thread'ga bermaslik.

### 12.4 Pinning muammosi va undan qochish

Pinning bu virtual thread'ning unmount qilolmay carrier'ni egallab qolishi. Blokirovka davomida carrier band bo'ladi va boshqa hech qanday virtual thread uni ishlatolmaydi. Agar carrier soni 8 bo'lsa va 8 ta virtual thread pinned holda bloklansa, butun ilova to'xtaydi.

Java 21-23 da pinning'ning asosiy manbasi `synchronized` blok edi: object monitor ichida bloklanish unmount'ni taqiqlaydi. Java 24 da bu tuzatildi, endi `synchronized` ichida bloklangan virtual thread ham normal unmount qiladi. Java 25 (LTS) shu xatti-harakatni meros qilib oladi. Shuning uchun bugungi pinning sabablari qisqargan: native frame (JNI chaqiruvi yoki `Object.wait` dan tashqari native blokirovka) va class initializer ichidagi kutish.

| Tuzoq | Nega sodir bo'ladi | Yechim |
|---|---|---|
| `synchronized` ichida I/O (Java 21-23) | Monitor unmount'ni taqiqlaydi | `ReentrantLock` ga o'tish yoki Java 24+ ga ko'tarilish |
| Eski JDBC yoki native driver | JNI frame'da bloklanish pinning beradi | Toza Java driver (PostgreSQL JDBC) ishlatish |
| Virtual thread'ni fixed pool'da ishlatish | Parallellik pool bilan cheklanadi | `newVirtualThreadPerTaskExecutor` |
| `ThreadLocal` keshi million thread'da | Har virtual thread o'z nusxasini oladi | `ScopedValue` yoki parametr orqali uzatish |
| Cheksiz virtual thread yaratish | Baza yoki tashqi API ni bosib tashlaydi | `Semaphore` bilan concurrency cheklash |
| CPU yukini virtual thread'ga berish | Carrier egallanib qoladi, latency o'sadi | Alohida platform thread pool |
| `ThreadPoolExecutor` metrikalariga tayanish | Pool yo'q, metrika bo'sh ko'rinadi | In-flight counter va semaphore metrikasi |
| Katta stack chuqurligi million thread'da | Heap'dagi stack chunk o'sadi | Rekursiyani cheklash, chuqurlikni nazorat qilish |

```java
// synchronized o'rniga ReentrantLock: ikkisi ham mutual exclusion beradi,
// lekin lock virtual thread'ga unmount qilish imkonini qoldiradi
public class OmborQoldigi {
    private final ReentrantLock lock = new ReentrantLock();
    private int qoldiq;

    public void kamaytir(int miqdor) {
        lock.lock();
        try {
            // Bu yerda tashqi chaqiruv bo'lsa ham carrier bloklanmaydi
            auditKlient.yoz(miqdor);
            qoldiq -= miqdor;
        } finally {
            lock.unlock();
        }
    }
}
```

Java 21-23 da pinning'ni topish uchun `-Djdk.tracePinnedThreads=full` flag'i ishlatilardi. Bu flag Java 24 da olib tashlandi, uning o'rniga `jdk.VirtualThreadPinned` JFR event'i qoldi. Arxitektor uchun amaliy qoida: pinning diagnostikasini JFR ga bog'lash, flag'ga emas, chunki flag JDK versiyasiga qarab yo'qoladi.

### 12.5 Spring Boot da virtual thread ni yoqish

Spring Boot 3.2 dan boshlab bitta property butun ilovani virtual thread'ga o'tkazadi. Shart: Java 21 yoki undan yuqori.

```properties
# Java 21+ talab qiladi, Spring Boot 3.2 dan mavjud
spring.threads.virtual.enabled=true

# Virtual thread bilan Tomcat thread pool chegarasi ma'nosini yo'qotadi,
# lekin so'rovlar sonini baribir cheklash kerak
server.tomcat.max-connections=10000
server.tomcat.accept-count=200

# Baza pool'i endi asosiy chegara, uni ongli qo'yish kerak
spring.datasource.hikari.maximum-pool-size=20
spring.datasource.hikari.connection-timeout=2000
```

Bu flag bir nechta joyni bir vaqtda o'zgartiradi: Tomcat (yoki Jetty) har so'rovni virtual thread'da bajaradi, `@Async` uchun ishlatiladigan `AsyncTaskExecutor` virtual thread'ga asoslangan bo'ladi, `@Scheduled` vazifalari uchun scheduler ham virtual thread ishlatadi. Spring MVC blocking modelda qolib, lekin thread chegarasidan xoli bo'ladi.

Nimalar o'zgarmaydi: `@Transactional` bemalol ishlaydi, chunki Spring tranzaksiya kontekstini `ThreadLocal` da saqlaydi va har virtual thread o'zining `ThreadLocal` nusxasiga ega. Security context ham xuddi shunday. Muammo faqat shunda chiqadi, agar kodda "thread kam bo'ladi" deb qurilgan `ThreadLocal` keshlar bo'lsa: masalan har thread uchun `SimpleDateFormat` yoki og'ir `ObjectMapper` nusxasi. 100 ta thread'da bu 100 nusxa, 200000 virtual thread'da bu xotira portlashi.

### 12.6 Connection pool virtual thread bilan: nega pool hali ham chegara

Virtual thread baza bilan ishlashni o'zgartirmaydi. PostgreSQL har ulanish uchun alohida backend jarayon ochadi va u taxminan 5-15 MB xotira oladi. `max_connections` default 100, odatda 200-300 gacha ko'tariladi, undan yuqorisi context switch va lock contention tufayli unumdorlikni pasaytiradi. Ya'ni ilova 100000 virtual thread ko'tarsa ham, baza 20 ta ulanishdan oshig'ini qabul qilmaydi.

Natijada arxitektura shakli o'zgaradi: oldin thread pool ham navbat, ham chegara vazifasini bajarardi. Endi navbat yo'qoladi va 50000 thread bir vaqtda Hikari dan ulanish so'raydi. Hikari `connection-timeout` ichida ulanish bermasa, `SQLTransientConnectionException` otadi va bu xatolar to'lqini ko'rinishida chiqadi. Shuning uchun cheklashni ongli ravishda oldinga, kirish darajasiga ko'chirish kerak.

```java
// Baza bilan ishlovchi qismga kirish nuqtasini cheklash
@Component
public class HisobotServisi {
    // Hikari pool 20 bo'lsa, semaphore 20 dan oshmasligi kerak
    private final Semaphore bazaKvotasi = new Semaphore(20);

    public Hisobot tayyorla(UUID buyurtmaId) throws InterruptedException {
        // 500 ms kutib ulanish olinmasa, tez fail qilamiz
        if (!bazaKvotasi.tryAcquire(500, TimeUnit.MILLISECONDS)) {
            throw new YukOshdiException("baza kvotasi band");
        }
        try {
            return jdbcClient.sql("SELECT ...").param(buyurtmaId).query(Hisobot.class).single();
        } finally {
            bazaKvotasi.release();
        }
    }
}
```

Pool o'lchamini tanlash qoidasi ham o'zgarmadi: CPU yadro soniga bog'lab, taxminan `yadro * 2` dan boshlab, keyin kuzatuv bilan sozlash. 8 yadroli bazada 16-30 ulanish ko'p holatda eng yaxshi throughput beradi. Agar mikroservislar soni ko'p bo'lsa, umumiy ulanish byudjetini hisoblash kerak: 10 instans * 20 pool = 200 ulanish, bu `max_connections` ga yaqin. Bunday holatda PgBouncer transaction pooling rejimida kiritiladi.

### 12.7 Structured concurrency: vazifalar daraxti, bekor qilish va xato tarqalishi

Oddiy `ExecutorService` bilan parallel chaqiruvlarda uch muammo doim takrorlanadi: biri xato berganda qolganlar behuda ishlashda davom etadi, timeout'ni har biri uchun alohida boshqarish kerak, va stack trace'da ota vazifa ko'rinmaydi. Structured concurrency shu uchtasini tilga olib kiradi: parallel vazifalar ota vazifaning leksik blokida tug'iladi va o'sha blokdan tashqariga chiqmaydi.

Java 25 da bu API beshinchi preview holatida, ya'ni `--enable-preview` kerak va imzolar hali o'zgarishi mumkin. Java 21-23 dagi shakl (`new StructuredTaskScope<>()`, `ShutdownOnFailure`, `throwIfFailed`) Java 25 da `StructuredTaskScope.open(...)` va `Joiner` ko'rinishiga almashtirildi. Arxitektor uchun xulosa: mexanikani o'zlashtirish arziydi, lekin production kodni preview API ga bog'lashdan oldin migratsiya narxini hisoblash kerak.

```java
// Java 25, preview: buyurtma sahifasi uchun uch chaqiruvni parallel bajarish
Buyurtma sahifa(UUID id) throws Exception {
    try (var scope = StructuredTaskScope.open(
            StructuredTaskScope.Joiner.<Object>awaitAllSuccessfulOrThrow(),
            cfg -> cfg.withTimeout(Duration.ofMillis(800)))) {

        var narx = scope.fork(() -> narxServisi.hisobla(id));
        var qoldiq = scope.fork(() -> omborServisi.qoldiq(id));
        var mijoz = scope.fork(() -> mijozServisi.profil(id));

        // join() biri xato bersa qolganlarini bekor qiladi va xatoni otadi
        scope.join();
        return new Buyurtma(narx.get(), qoldiq.get(), mijoz.get());
    }
}
```

Bekor qilish `Thread.interrupt` orqali ishlaydi, shuning uchun vazifa ichidagi kod interrupt'ni to'g'ri qayta uzatishi shart. Agar kod `InterruptedException` ni yutib yuborsa, bekor qilish ishlamaydi va timeout kafolati yo'qoladi. Bu eng ko'p uchraydigan integratsiya xatosi.

### 12.8 Scoped values va `ThreadLocal` o'rniga ishlatish

`ThreadLocal` ikki muammo keltiradi. Birinchisi: uning qiymati thread yashash davomida qoladi, shuning uchun uni tozalashni eslab qolish kerak va pool'da `remove()` qilinmasa ma'lumot oqib ketadi. Ikkinchisi: inheritable variant yaratilganda qiymat har bir child thread'ga nusxalanadi va million virtual thread'da bu xotirada sezilarli bo'ladi.

`ScopedValue` Java 25 da final bo'ldi. U immutable va uning amal qilish doirasi leksik blok bilan belgilanadi: blok tugashi bilan bog'lanish o'z-o'zidan yo'qoladi, tozalash kerak emas. Child virtual thread'lar qiymatni nusxalamaydi, ota'ning bog'lanishiga murojaat qiladi.

```java
// Request kontekstini ThreadLocal o'rniga ScopedValue da uzatish
public final class Kontekst {
    public static final ScopedValue<SorovId> SOROV = ScopedValue.newInstance();
}

// Filter yoki interceptor ichida
ScopedValue.where(Kontekst.SOROV, new SorovId(traceId)).run(() -> {
    // Bu blok ichidagi butun chaqiruv zanjiri qiymatni ko'radi
    tolovServisi.bajar(buyurtma);
});

// Chuqurlikdagi kod
String traceId = Kontekst.SOROV.isBound()
    ? Kontekst.SOROV.get().qiymat()
    : "yoq"; // bog'lanmagan holatni doim hisobga olish kerak
```

Amalda Spring ilovasida darhol hamma `ThreadLocal` ni almashtirishga urinmaslik kerak. Spring'ning o'z infratuzilmasi (tranzaksiya, security, MDC) `ThreadLocal` ga tayanadi va u virtual thread bilan to'g'ri ishlaydi. `ScopedValue` ni o'z kodingizdagi kontekst uzatish uchun va structured concurrency bilan birga ishlatish eng ko'p foyda beradi.

### 12.9 Kuzatuvchanlik: thread dump va metrikalar o'zgarishi

Klassik `jstack` virtual thread'larni ko'rsatmaydi, chunki u faqat OS thread'larni biladi. Siz carrier thread'lar ro'yxatini ko'rasiz va ularning stack'i ichida nima bo'layotgani tushunarsiz bo'ladi. To'g'ri vosita yangi formatdagi thread dump.

```bash
# Virtual thread'larni ham qamrab oladigan dump (JSON yoki matn)
jcmd <pid> Thread.dump_to_file -format=json /tmp/dump.json

# Pinning va virtual thread hodisalarini JFR bilan yozib olish
jcmd <pid> JFR.start name=vt settings=profile duration=120s filename=/tmp/vt.jfr
# Keyin quyidagi event'larni ko'rish:
#   jdk.VirtualThreadPinned, jdk.VirtualThreadStart,
#   jdk.VirtualThreadEnd, jdk.VirtualThreadSubmitFailed
jfr summary /tmp/vt.jfr
```

Metrikalar tomonida eng katta o'zgarish: `executor.pool.size`, `executor.queued`, `tomcat.threads.busy` kabi ko'rsatkichlar ma'nosini yo'qotadi. Oldin "pool to'ldi" signali yuk oshganini bildirardi, endi bunday signal yo'q va ilova jim turib latency'ni o'stiradi. Shuning uchun kuzatuvni boshqa joylarga ko'chirish kerak: in-flight so'rov soni (`Gauge` sifatida), semaphore'dagi kutish vaqti, Hikari `hikaricp.connections.pending` va `hikaricp.connections.acquire` taqsimoti. Bu uchtasi birgalikda haqiqiy bo'g'izni ko'rsatadi.

Tracing bilan ishlashda bitta nozik joy bor: Micrometer `Observation` konteksti `ThreadLocal` orqali tarqaladi va `executor.submit` chegarasida avtomatik ko'chmaydi. Context propagation kutubxonasi orqali executor'ni o'rash kerak, aks holda trace virtual thread chegarasida uzilib qoladi.

### 12.10 Reactive dasturlashga nisbatan tanlov: qachon qaysi biri

Reactive (WebFlux, Reactor, R2DBC) ikki narsani beradi: thread tejash va backpressure. Virtual thread birinchisini beradi, ikkinchisini bermaydi. Shuning uchun tanlov "qaysi biri tezroq" emas, "sizga backpressure kerakmi" degan savolga keladi.

| Holat | Oddiy yondashuv | Arxitektor yondashuvi |
|---|---|---|
| I/O ko'p REST servis | Tomcat `max-threads` ni 400 ga ko'tarish | Virtual thread yoqib, chegarani baza pool'iga ko'chirish |
| Mavjud WebFlux kodi | Virtual thread uchun hammasini blocking ga qaytarish | WebFlux ni qoldirish, yangi modullarni blocking yozish |
| Oqim (stream) ishlovi | Hamma elementga bitta virtual thread | Reactive yoki `Flow` bilan backpressure saqlash |
| CPU og'ir hisobot | Virtual thread executor'ga tashlash | Yadro soniga teng platform pool, alohida ajratish |
| Tashqi API rate limit | Retry va kutish bilan urinish | `Semaphore` bilan concurrency cheklash, fail fast |
| Parallel chaqiruvlar | `CompletableFuture.allOf` va qo'lda bekor qilish | Structured concurrency, timeout va bekor qilish tilda |
| Kontekst uzatish | `InheritableThreadLocal` | `ScopedValue`, leksik doira bilan |
| Yuk oshganini bilish | `tomcat.threads.busy` ni kuzatish | In-flight gauge va pool kutish vaqti |
| Pinning diagnostikasi | Log'larga tayanish | JFR `jdk.VirtualThreadPinned` event'i |
| Migratsiya rejasi | Bitta deploy'da hammasini o'tkazish | Bitta servisda yoqib, latency taqsimotini solishtirish |

Amaliy qoida: agar ilova HTTP so'rov qabul qilib, bir nechta servis va bazaga murojaat qilib, javob qaytarsa, virtual thread yetarli va kod ancha sodda bo'ladi. Agar ilova uzluksiz oqimni (event stream, SSE, WebSocket, Kafka'dan katta hajm) qayta ishlasa va ishlab chiqaruvchi iste'molchidan tez bo'lsa, backpressure kerak va reactive model o'z o'rnini saqlaydi. Ikkisini bitta ilovada aralashtirish mumkin, lekin chegarani aniq qo'yish kerak: blocking qism va reactive qism bir-birining thread'ida ishlamasin.

Migratsiyada arxitektor tekshiradigan narsa: yoqishdan oldin va keyin latency'ning p99 qiymati, Hikari pending ulanishlar soni, va yuk testida xatolar turi. Agar p50 yaxshilanib p99 yomonlashsa, bu deyarli har doim pastdagi resursning (baza yoki tashqi servis) bo'g'izga aylanganini bildiradi, virtual thread aybdor emas. Testlash qo'llanmasidagi performance test bo'limi shu solishtirishni qanday o'tkazishni ko'rsatadi.

### 12.11 Amalda qo'llash

- [ ] JDK versiyasini aniqlang: Java 21 da virtual thread barqaror, lekin `synchronized` pinning'dan qochish uchun Java 24 yoki 25 ga ko'tarilishni rejaga qo'ying.
- [ ] Bitta I/O ga bog'liq servisda `spring.threads.virtual.enabled=true` ni yoqib, p50 va p99 latency'ni yoqishdan oldingi qiymat bilan solishtiring.
- [ ] Kod bazasini `synchronized` bloklari ichida tashqi chaqiruv yoki I/O bor joylarga tekshirib, ularni `ReentrantLock` ga o'tkazing.
- [ ] Har bir `ThreadLocal` ishlatilishini ko'rib chiqing: og'ir obyekt keshi bo'lsa, uni umumiy thread-safe nusxaga yoki `ScopedValue` ga almashtiring.
- [ ] Bazaga kiradigan oqimlarga `Semaphore` qo'yib, uning o'lchamini Hikari `maximum-pool-size` dan oshmaydigan qilib belgilang.
- [ ] Dashboard'dagi `tomcat.threads.busy` panelini in-flight so'rov gauge'i va `hikaricp.connections.pending` bilan almashtiring.
- [ ] JFR profilini yuk testi davomida yozib, `jdk.VirtualThreadPinned` event'lari borligini tekshiring va sababini toping.
- [ ] CPU bilan band vazifalarni (hisobot, shifrlash, katta serializatsiya) yadro soniga teng alohida platform thread pool'ga ajratib chiqaring.

## 13. Zamonaviy Java tili va API dizayni (Modern Java and API Design)

Java 17 dan 25 gacha til shunchalik o'zgardi ki, eski uslubda yozilgan kod endi texnik qarz bo'lib qoldi. Record, sealed interface va pattern matching birgalikda ma'lumot modelini kompilyator tekshiradigan shaklga keltiradi. Arxitektor uchun bu yerdagi savol "yangi sintaksis chiroylimi" emas, balki "qaysi xato kompilyatsiya vaqtida tutiladi va qaysi biri production da tutiladi". Bu bobda til imkoniyatlari va API dizayni qarorlari aynan shu mezon bilan ko'rib chiqiladi.

### 13.1 Record: qachon ishlatish, qachon oddiy sinf kerak

Record o'zgarmas ma'lumot tashuvchisi uchun mo'ljallangan. Kompilyator unga konstruktor, `equals`, `hashCode`, `toString` va komponent accessor larini o'zi yozadi. `equals` barcha komponentlar ustidan hisoblanadi, shuning uchun record ni `HashMap` kaliti qilib ishlatish xavfsiz. Record yashirin tarzda `final`, boshqa sinfdan meros olmaydi, maydonlari `final`.

Validatsiyani compact konstruktorda qilish kerak. Bu yagona joy, chunki record o'zgarmas, demak yaroqsiz holat hech qachon yuzaga kelmaydi.

```java
public record PaymentRequest(
        String orderId,
        BigDecimal amount,
        Currency currency,
        Instant requestedAt) {

    public PaymentRequest {
        // compact konstruktor: validatsiya shu yerda, boshqa joyda emas
        Objects.requireNonNull(orderId, "orderId null bo'lmaydi");
        Objects.requireNonNull(currency, "currency null bo'lmaydi");
        if (amount == null || amount.signum() <= 0) {
            throw new IllegalArgumentException("summa musbat bo'lishi kerak: " + amount);
        }
        // BigDecimal scale ni normallashtiramiz, aks holda equals yolg'on ishlaydi:
        // 10.0 va 10.00 BigDecimal da teng emas
        amount = amount.setScale(currency.getDefaultFractionDigits(), RoundingMode.UNNECESSARY);
    }

    public boolean isLargePayment() {
        return amount.compareTo(new BigDecimal("10000")) >= 0;
    }
}
```

Oddiy sinf quyidagi hollarda kerak. Birinchi, JPA entity: Hibernate argumentsiz konstruktor, o'zgaruvchan maydon va proxy uchun ochiq sinf talab qiladi, record bunga yaramaydi. Ikkinchi, identity semantikasi kerak bo'lsa: buyurtma entity si ID bo'yicha teng bo'lishi kerak, barcha maydonlari bo'yicha emas. Uchinchi, komponentlar soni oltitadan oshsa va ularning yarmi ixtiyoriy bo'lsa: bu yerda builder li oddiy sinf o'qilishi yaxshiroq. To'rtinchi, keyinchalik maydon qo'shilishi kutilayotgan ommaviy API da record komponentlari tartibi konstruktor imzosining bir qismi, shuning uchun har bir qo'shimcha binary moslikni buzadi.

Record DTO va read model uchun ideal. Spring Data JPA interface va sinf asosidagi projection larda record ni to'g'ridan to'g'ri qabul qiladi, JPQL da `select new` konstruktor ifodasi ham ishlaydi. Jackson record ni 2.12 dan beri komponent nomlari bo'yicha serialize va deserialize qiladi, qo'shimcha annotatsiya shart emas.

### 13.2 Sealed interface va pattern matching bilan to'liq qamrovli tanlov

Sealed ierarxiya kompilyatorga "bu turning variantlari aynan shular" deb aytadi. Natijada `switch` da `default` shoxi kerak emas, va yangi variant qo'shilganda uni unutgan har bir `switch` kompilyatsiya xatosi beradi. Bu to'lov natijasi, buyurtma holati, hisobot formati kabi yopiq to'plamlar uchun eng kuchli vositalardan biri.

```java
public sealed interface PaymentResult {

    record Captured(String providerRef, BigDecimal amount) implements PaymentResult {}
    record Pending(String providerRef, Duration retryAfter) implements PaymentResult {}
    record Declined(DeclineReason reason, String providerMessage) implements PaymentResult {}
    record ProviderUnavailable(Duration retryAfter) implements PaymentResult {}
}

// Yangi variant qo'shilsa, bu switch kompilyatsiya qilinmaydi: default yo'q
String auditLine(PaymentResult result) {
    return switch (result) {
        case Captured(var ref, var amount) ->
                "olindi ref=" + ref + " summa=" + amount;
        case Pending(var ref, var retryAfter) ->
                "kutilmoqda ref=" + ref + " qayta=" + retryAfter.toSeconds() + "s";
        case Declined(DeclineReason.INSUFFICIENT_FUNDS, var msg) ->
                "mablag' yetmadi: " + msg;
        case Declined(var reason, var msg) ->
                "rad etildi " + reason + ": " + msg;
        case ProviderUnavailable(var retryAfter) ->
                "provayder ishlamaydi, qayta=" + retryAfter.toSeconds() + "s";
    };
}
```

`permits` ro'yxatini yozmasa ham bo'ladi, agar barcha implementatsiya bir faylda yoki bir paketda bo'lsa. Nested record lar shu sababli ko'p qulay: butun ierarxiya bitta faylda ko'rinadi.

Muhim chegara: sealed ierarxiya sizning kodingizda bo'lishi kerak. Agar siz kutubxona chiqarayotgan bo'lsangiz, sealed interface mijozga yangi variant qo'shishga ruxsat bermaydi. Bu ataylab qilinadigan qaror. Agar genişlashtirish nuqtasi kerak bo'lsa, oddiy interface qoldiring va visitor o'rnini saqlang. Agar variantlar sizda to'liq nazoratda bo'lsa, sealed ni tanlang, chunki u har bir yangi holatni qamrab olishga majbur qiladi.

### 13.3 `switch` ifodasi va deconstruction pattern

`switch` endi ifoda, ya'ni qiymat qaytaradi. Bu uch narsani beradi. Birinchi, `->` shoxlari fall through qilmaydi, shuning uchun unutilgan `break` dan kelib chiqadigan xatolar yo'qoladi. Ikkinchi, har bir shox qiymat qaytarishi shart, demak kompilyator to'liqlikni tekshiradi. Uchinchi, record pattern bilan ma'lumotni darhol ochib olish mumkin, alohida cast va getter chaqiruvlari kerak emas.

`when` guard shart ni pattern ustiga qo'yadi. Guard tartibi muhim: aniqroq shart avval yozilishi kerak, aks holda kompilyator "pattern dominated" xatosini beradi.

```java
// Ombor qoldig'i bo'yicha qaror: pattern + guard, hech qanday if-else zinapoyasi yo'q
sealed interface StockEvent {
    record Reserved(String sku, int qty) implements StockEvent {}
    record Released(String sku, int qty) implements StockEvent {}
    record Recounted(String sku, int counted, int expected) implements StockEvent {}
}

int delta(StockEvent event) {
    return switch (event) {
        case null -> 0;                                  // pattern switch da null ni aniq yozish mumkin
        case Reserved(_, int qty) when qty > 1000 -> -qty; // katta rezerv, alohida audit
        case Reserved(_, int qty) -> -qty;
        case Released(_, int qty) -> qty;
        case Recounted(_, int counted, int expected) -> counted - expected;
    };
}
```

Ikki tuzoqni bilib turish kerak. Birinchi, `case null` yozilmasa pattern switch `NullPointerException` tashlaydi. Eski `switch` ham shunday qilardi, lekin endi `case null` ni ochiq yozish imkoni bor va u niyatni ko'rsatadi. Ikkinchi, sealed ierarxiya alohida kompilyatsiya qilingan modul da o'zgarsa, eski `switch` runtime da `MatchException` beradi. Shuning uchun sealed ierarxiya va uni ishlatuvchi kod bir deploy birligida bo'lishi afzal. Nomsiz pattern `_` Java 22 dan boshlab to'liq qo'llanadi va ishlatilmaydigan komponentni ko'rsatishga xizmat qiladi.

### 13.4 Text block, `var` va o'qilishi: foyda va chegara

Text block SQL va JSON ni kodda o'qiladigan qiladi. Kompilyator chap tomondagi umumiy bo'shliqni o'zi olib tashlaydi, chegarani yopuvchi `"""` ning joylashuvi belgilaydi. Satr oxiridagi `\` yangi qatorni bosadi, `\s` esa kerakli bo'shliqni saqlab qoladi.

```java
// Hisobot so'rovi: text block bilan SQL diff da o'qiladi va DBA bilan muhokama qilinadi
private static final String MONTHLY_REVENUE = """
        select date_trunc('month', p.captured_at) as month,
               p.currency,
               sum(p.amount)                      as total,
               count(*)                           as payments
        from payment p
        where p.status = 'CAPTURED'
          and p.captured_at >= ?
          and p.captured_at <  ?
        group by 1, 2
        order by 1 desc
        """;

// var: o'ng tomon turni aytib turganda foydali
var byCurrency = new HashMap<Currency, BigDecimal>();      // tur bir marta yozildi
var rows = jdbcTemplate.query(MONTHLY_REVENUE, mapper, from, to);

// var: bu yerda zarar, chunki o'qiyotgan odam turni bilmaydi
var result = service.process(request);                     // nima qaytadi, noma'lum
```

`var` qoidasi oddiy. O'ng tomonda konstruktor yoki fabrika chaqiruvi bo'lib, tur nomi ko'rinib turgan bo'lsa `var` ishlatiladi. Metod chaqiruvining natijasi bo'lsa va tur nomi ko'rinmasa, turni ochiq yozish kerak. `var` ommaviy API imzosida ishlatilmaydi, u faqat lokal o'zgaruvchi. Diamond operator bilan birga `var x = new ArrayList<>()` yozsangiz `ArrayList<Object>` chiqadi, bu deyarli har doim xato.

Text block ning chegarasi: u shablon mexanizmi emas. Ichida o'zgaruvchi almashtirish uchun `formatted` ishlating. Foydalanuvchi kiritgan qiymatni SQL text block ichiga string sifatida ulamang, bu SQL injection. Parametr placeholder ishlating.

### 13.5 Optional ni to'g'ri ishlatish: qaytish qiymati, maydon emas

`Optional` bitta masalani hal qilish uchun yaratilgan: metod qiymat qaytarmasligi mumkinligini imzoda bildirish. U maydon turi emas, konstruktor parametri emas, kolleksiya elementi emas. `Optional` `Serializable` ni implement qilmaydi, shuning uchun entity maydoni yoki cache ga yoziladigan DTO maydoni sifatida ishlatilmaydi.

```java
// To'g'ri: repository topilmaslikni imzoda bildiradi
Optional<Payment> findByProviderRef(String providerRef);

// To'g'ri: orElseThrow domen istisnosi bilan
Payment payment = payments.findByProviderRef(ref)
        .orElseThrow(() -> new PaymentNotFoundException(ref));

// To'g'ri: zanjir, hech qanday isPresent yo'q
String country = payments.findByProviderRef(ref)
        .map(Payment::payer)
        .flatMap(Payer::billingAddress)
        .map(Address::countryCode)
        .orElse("UZ");

// Xato: Optional maydon. Serializable emas, JPA uni map qilmaydi, xotira ortadi
// private Optional<String> note;

// Xato: get() tekshiruvsiz. NoSuchElementException stack trace si foydasiz
// Payment p = payments.findByProviderRef(ref).get();

// Xato: Optional parametr. Chaqiruvchi Optional.of qurishga majbur
// void notify(Optional<String> email) { ... }
```

Bo'sh kolleksiya qaytarish kerak bo'lganda `Optional<List<T>>` yozmang. Bo'sh `List` o'zi "yo'q" ni anglatadi. `orElse` va `orElseGet` farqi muhim: `orElse` argumentini har doim hisoblaydi, hatto qiymat bor bo'lsa ham. Agar standart qiymat hisoblanishi arzon bo'lmasa, `orElseGet` ishlating. Oqimda ishlaganda `stream().flatMap(Optional::stream)` bo'sh qiymatlarni toza filtrlaydi.

### 13.6 Stream API: qachon foyda, qachon oddiy sikl tushunarliroq

Stream deklarativ transformatsiya uchun yaxshi: filtrlash, map qilish, guruhlash, jamlash. U bitta ifodada niyatni ko'rsatadi va oraliq o'zgaruvchilarni yo'q qiladi. Lekin stream ning uchta aniq zaifligi bor: debug qilish qiyin, `break` ekvivalenti yo'q, va stack trace o'qilmas holga keladi.

```java
// Stream foydali: guruhlash va jamlash bir ifodada
Map<Currency, BigDecimal> totalByCurrency = payments.stream()
        .filter(p -> p.status() == CAPTURED)
        .collect(Collectors.groupingBy(
                Payment::currency,
                Collectors.reducing(BigDecimal.ZERO, Payment::amount, BigDecimal::add)));

// Sikl tushunarliroq: bir nechta o'zgaruvchi, erta chiqish va xatolar yig'ilishi
List<String> rejected = new ArrayList<>();
BigDecimal running = BigDecimal.ZERO;
for (Payment p : payments) {
    if (running.compareTo(dailyLimit) >= 0) {
        break;                                  // stream da bunga toza ekvivalent yo'q
    }
    try {
        running = running.add(provider.capture(p));   // checked exception stream ichida og'riq
    } catch (ProviderException e) {
        rejected.add(p.orderId());
    }
}
```

Qoida: agar lambda ichida `try/catch` paydo bo'lsa yoki tashqi o'zgaruvchi o'zgarishi kerak bo'lsa, sikl yozing. Agar transformatsiya toza bo'lsa, stream yozing.

`parallelStream` ni ehtiyotkorlik bilan ishlating. U umumiy `ForkJoinPool.commonPool` da ishlaydi va butun JVM uchun umumiy. Bloklanadigan I/O ni parallel stream ga bermang. Foyda odatda element soni o'n minglardan oshganda va amal sof CPU bo'lganda ko'rinadi. Virtual thread davrida I/O ni parallellashtirish uchun to'g'ri vosita executor, parallel stream emas. Java 24 da `Stream.gather` va `Gatherers` to'liq qo'shildi, u oynali va holatli transformatsiyalarni standart usulda yozish imkonini beradi.

### 13.7 Istisnolar dizayni: tekshiriladigan va tekshirilmaydigan, o'z ierarxiyangiz

Tekshiriladigan istisno chaqiruvchi haqiqatan ham tiklanish harakati qila oladigan holat uchun. Tekshirilmaydigan istisno programma xatosi yoki tiklanmaydigan infratuzilma nosozligi uchun. Spring ning o'zi bu tanlovni allaqachon qilgan: `DataAccessException` ierarxiyasi butunlay `RuntimeException` dan meros oladi, chunki SQL xatosidan chaqiruvchi deyarli hech narsa qila olmaydi.

```java
// Domen ierarxiyasi: bitta ildiz, barqaror xato kodi, kontekst maydonlari
public abstract class PaymentException extends RuntimeException {
    private final String code;          // API javobiga chiqadigan barqaror kod
    private final String orderId;

    protected PaymentException(String code, String orderId, String message, Throwable cause) {
        super(message, cause);
        this.code = code;
        this.orderId = orderId;
    }
    public String code() { return code; }
    public String orderId() { return orderId; }
}

public final class InsufficientFundsException extends PaymentException {
    public InsufficientFundsException(String orderId) {
        super("PAYMENT_INSUFFICIENT_FUNDS", orderId, "mablag' yetarli emas: " + orderId, null);
    }
}

// Qayta urinish mumkinligini tur bilan bildirish: resilience qatlami shu belgiga qaraydi
public interface Retryable { Duration retryAfter(); }
```

Uch amaliy qoida. Birinchi, xato kodini `enum` yoki konstanta sifatida saqlang va uni API kontraktining bir qismi deb bilib, hech qachon o'zgartirmang. Xato matni o'zgarishi mumkin, kod o'zgarmasligi kerak. Ikkinchi, `cause` ni hech qachon yo'qotmang: `throw new MyException(msg)` yozib asl istisnoni tashlab ketish eng ko'p uchraydigan diagnostika yo'qotishi. Uchinchi, boshqaruv oqimi uchun istisno ishlatmang. Agar holat kutilgan bo'lsa, sealed natija turi qaytaring, yuqoridagi `PaymentResult` kabi.

Yuqori chastotali kodda stack trace yig'ish qimmat. Kutilgan, soniyada minglab marta yuz beradigan holat uchun `super(message, cause, false, false)` konstruktori bilan suppression va writableStackTrace ni o'chirish mumkin. Bu optimizatsiyani faqat o'lchov ko'rsatganda qiling.

### 13.8 Kutubxona API si dizayni: kirish nuqtasi kam, nom aniq, standart qiymat xavfsiz

Ichki kutubxona chiqarayotganda eng muhim qaror nimani ommaviy qilish emas, nimani ommaviy qilmaslik. Har bir `public` tur kelajakdagi majburiyat. Bir kirish nuqtasi, bir nechta `sealed` yoki `final` qiymat turi, qolgani `package private`.

```java
// Bitta kirish nuqtasi, qolgan hammasi paket ichida yashiringan
public final class ReportExporter {

    public static Builder builder() { return new Builder(); }

    public static final class Builder {
        // Standart qiymatlar xavfsiz tomonga qaragan: kichik sahifa, qisqa timeout
        private int pageSize = 1_000;
        private Duration timeout = Duration.ofSeconds(30);
        private boolean includePii = false;        // standart: PII yo'q

        public Builder pageSize(int pageSize) {
            if (pageSize < 1 || pageSize > 50_000) {
                throw new IllegalArgumentException("pageSize 1..50000 oralig'ida");
            }
            this.pageSize = pageSize;
            return this;
        }
        public Builder timeout(Duration timeout) { this.timeout = timeout; return this; }
        public Builder includePii(boolean includePii) { this.includePii = includePii; return this; }
        public ReportExporter build() { return new ReportExporter(this); }
    }
}
```

Nom berishda uch qoida. Birinchi, `get` prefiksi faqat haqiqiy accessor uchun. Hisoblash qiladigan metod `calculateMonthlyTotal` deb nomlanadi, chunki chaqiruvchi uning qimmatligini bilishi kerak. Ikkinchi, bool parametr o'rniga `enum` bering. `export(true, false)` chaqiruvni o'qib bo'lmaydi, `export(Format.CSV, Pii.EXCLUDE)` o'qiladi. Uchinchi, vaqt birligini nomga yozmang, `Duration` qabul qiling. `timeoutMs` xato birlik berish xatosini ochiq qoldiradi.

Standart qiymat har doim xavfsiz tomonga qarashi kerak. PII standart holda o'chirilgan, retry standart holda o'chirilgan yoki chegaralangan, timeout standart holda cheksiz emas. Mijoz xavfli rejimni ongli ravishda yoqadi.

| Mezon | Oddiy yondashuv | Arxitektor yondashuvi |
|---|---|---|
| Ma'lumot modeli | Hamma joyda mutable POJO, setter bilan | Record, compact konstruktorda validatsiya, yaroqsiz holat mavjud emas |
| Variantlar to'plami | `String type` maydoni va `if-else` zinapoyasi | Sealed interface va to'liq qamrovli `switch` ifodasi |
| Yo'qlik | Null qaytarish va Javadoc da eslatma | `Optional` qaytish qiymati, maydon emas, parametr emas |
| Istisnolar | Hamma joyda `RuntimeException` yoki `Exception` | Bitta domen ildizi, barqaror xato kodi, `cause` saqlanadi |
| API sirti | Hamma sinf `public`, "kerak bo'lar" | Bir kirish nuqtasi, qolgani paket ichida |
| Standart qiymatlar | Cheksiz timeout, cheksiz sahifa | Chegaralangan va xavfsiz standart, xavfli rejim ongli yoqiladi |
| Null kontrakti | Hech qanday annotatsiya, har joyda tekshiruv | `@NullMarked` paket, chegarada tekshiruv, build da statik tahlil |
| Metod o'chirish | To'g'ridan to'g'ri o'chirish, minor versiyada | `@Deprecated(since, forRemoval)`, ikki relizlik oyna, `japicmp` darvozasi |
| Java versiyasi | "Ishlayapti, tegmaymiz" | LTS da turish, har oraliq relizni CI da sinash |
| Stream va sikl | Hamma narsa stream, lambda ichida `try/catch` | Toza transformatsiya stream, holatli va erta chiqadigan mantiq sikl |

### 13.9 Orqaga moslik: metod qo'shish, nomini o'zgartirish, deprecate qilish siyosati

Binary moslik va source moslik ikki xil narsa. Interface ga metod qo'shsangiz, source moslik buziladi, chunki implementatsiya qiluvchilar kompilyatsiya qilinmaydi. `default` metod qo'shsangiz ikkisi ham saqlanadi. Record ga komponent qo'shsangiz konstruktor imzosi o'zgaradi va eski kompilyatsiya qilingan mijoz `NoSuchMethodError` oladi.

Metod nomini "o'zgartirish" degan amal yo'q. Yangi nom bilan metod qo'shiladi, eskisi eski nomda qoladi va `@Deprecated(since = "...", forRemoval = true)` bilan belgilanadi. Eski metod yangisiga delegatsiya qiladi. Olib tashlash faqat major versiyada bo'ladi.

```bash
# Build da moslikni darvoza qilib qo'yish
# japicmp: oldingi reliz bilan binary farqni tekshiradi, buzilish bo'lsa build yiqiladi
mvn -q com.github.siom79.japicmp:japicmp-maven-plugin:cmp

# jdeprscan: kodingiz JDK ning deprecated API sidan foydalanayotganini ko'rsatadi
jdeprscan --release 25 --for-removal target/report-exporter-2.4.0.jar

# jdeps: tasodifiy ichki paket bog'liqligini topadi
jdeps --multi-release 25 -summary target/report-exporter-2.4.0.jar
```

Deprecate siyosatini yozib qo'ying va unga rioya qiling. Amaliy shakl: belgilangan metod kamida ikki minor reliz yoki taxminan oltita oy yashaydi. Javadoc da `@deprecated` tegi o'rnini aniq ko'rsatadi, ya'ni "`exportCsv(Pii)` ni ishlating". Metrika qo'ying: eski metod chaqirilganda counter oshadi, shunda olib tashlashdan oldin uni hali kim ishlatayotganini bilasiz.

| Tuzoq | Nima bo'ladi | Yechim |
|---|---|---|
| Record ga yangi komponent qo'shish | Eski mijozda `NoSuchMethodError` | Yangi record turi chiqarish yoki builder li sinfga o'tish |
| Interface ga abstrakt metod qo'shish | Mijoz implementatsiyasi kompilyatsiya qilinmaydi | `default` metod qo'shish yoki yangi interface ajratish |
| `Optional` ni entity maydoni qilish | JPA map qilmaydi, serializatsiya yiqiladi | Maydon nullable, accessor `Optional` qaytaradi |
| `parallelStream` ichida bloklanadigan I/O | `commonPool` to'lib qoladi, butun JVM sekinlashadi | Alohida executor yoki virtual thread ishlatish |
| Sealed ierarxiyani alohida modulda o'zgartirish | Runtime da `MatchException` | Ierarxiya va iste'molchini bir deploy birligida saqlash |
| Pattern `switch` da `case null` yo'q | Kutilmagan `NullPointerException` | `case null` ni ochiq yozish yoki chegarada tekshirish |
| `var new ArrayList<>()` | Tur `ArrayList<Object>` bo'lib ketadi | Generic parametrni ochiq yozish |
| `orElse` ichida qimmat chaqiruv | Qiymat bor bo'lsa ham hisoblanadi | `orElseGet` ishlatish |
| Istisno `cause` sini tashlab ketish | Asl sabab log da yo'q, diagnostika imkonsiz | `cause` ni har doim konstruktorga uzatish |
| Xato matniga qarab mijoz mantiq yozishi | Matn o'zgarsa integratsiya yiqiladi | Barqaror xato kodi, matn faqat odam uchun |

### 13.10 Null xavfsizligi: annotatsiyalar va chegaraviy tekshiruv

Java da null xavfsizligini til bermaydi, shuning uchun uni annotatsiya va build darvozasi bilan quramiz. JSpecify 1.0 bugungi standart tanlov. `@NullMarked` ni paket yoki modul darajasida qo'ysangiz, o'sha doiradagi barcha tur ishlatilishi standart holda non null deb qabul qilinadi. Shundan keyin faqat istisnolarni, ya'ni `@Nullable` ni belgilash kifoya. Spring Framework 7 va Spring Boot 4 o'z API sida JSpecify ga o'tdi, shuning uchun ekosistemaga mos tanlov shu.

```java
// package-info.java: butun paket uchun non null standart
@NullMarked
package com.shop.payment.api;

import org.jspecify.annotations.NullMarked;
```

```java
@NullMarked
public final class PaymentFacade {

    // Parametr va qaytish qiymati standart holda non null
    public PaymentResult pay(PaymentRequest request, @Nullable String idempotencyKey) {
        // Chegaraviy tekshiruv: tashqi dunyodan kelgan qiymat faqat shu yerda tekshiriladi
        Objects.requireNonNull(request, "request");
        String key = idempotencyKey != null ? idempotencyKey : UUID.randomUUID().toString();
        return engine.execute(request, key);   // ichkarida endi null tekshiruvi yo'q
    }
}
```

Arxitektura qoidasi: null tekshiruvi tizim chegarasida bo'ladi. Chegara deganda controller, message listener, tashqi klient adapter va ommaviy facade tushuniladi. Chegaradan o'tgandan keyin ichki qatlamlar non null deb ishonadi va takroriy tekshiruv yozmaydi. Bu minglab keraksiz `if (x != null)` ni yo'q qiladi.

Annotatsiya o'z o'zidan hech narsa tekshirmaydi. Build ga statik tahlil qo'shish kerak. Error Prone ustidagi NullAway annotatsiyalarni o'qiydi va qoida buzilishini kompilyatsiya xatosiga aylantiradi. IDE inspeksiyasi ham shu annotatsiyalarni tushunadi, lekin IDE CI emas. Qoidani CI da majburlash kerak, aks holda u tavsiya bo'lib qoladi.

### 13.11 Java versiyalari: LTS tanlash va yangilanish strategiyasi

Java olti oyda bir reliz chiqaradi va Java 21 dan boshlab LTS har ikki yilda keladi. Amaldagi LTS lar: 17 (2021), 21 (2023), 25 (2025). Production da LTS da turish to'g'ri qaror, chunki oraliq relizlar faqat oltita oy yamoq oladi. Lekin "LTS da turish" degani oraliq relizlarni ko'rmaslik degani emas.

Praktik strategiya ikki trekli. Production trek LTS da. Ikkinchi trek CI da: nightly build eng yangi JDK da ham kompilyatsiya qilib, testlarni o'tkazadi. Shunda keyingi LTS ga o'tish ikki yillik katta loyiha emas, balki bir necha kunlik ish bo'ladi.

```yaml
# CI: production LTS plus kelgusi relizni kuzatuvchi trek
strategy:
  fail-fast: false
  matrix:
    java: [ 21, 25, 26-ea ]   # 21 production, 25 maqsad, 26-ea ogohlantirish uchun
steps:
  - uses: actions/setup-java@v4
    with:
      distribution: temurin
      java-version: ${{ matrix.java }}
  - run: mvn -B verify
```

```properties
# Maven: bytecode maqsadi va manba sintaksisi alohida boshqariladi
maven.compiler.release=21
# Kutubxona chiqarayotganda eng past qo'llanadigan versiyaga release qiling,
# chunki --release eski API dan tashqariga chiqishni kompilyatsiyada bloklaydi
maven.compiler.parameters=true
```

Yangilanish paytida uchta narsa ko'p muammo beradi. Birinchi, bytecode manipulyatsiya qiladigan kutubxonalar: ByteBuddy, ASM asosidagi agentlar va eski mock kutubxonalari yangi class file versiyasini tanimasligi mumkin, shuning uchun ularni avval ko'taring. Ikkinchi, JDK ichki API siga kirish: yangi relizlarda u qattiqroq yopiladi va `--add-opens` flaglari tobora kamroq ishlaydi. Uchinchi, GC standartining o'zgarishi: heap va pauza o'lchovlarini yangilanishdan keyin qaytadan oling, chunki eski tuning parametrlari yangi kollektorda ma'noni o'zgartiradi.

Qaror mezoni oddiy. Agar Spring Boot 3.x da bo'lsangiz, Java 17 minimal, lekin Java 21 virtual thread uchun amalda majburiy. Spring Boot 4.x va Spring Framework 7.x ham Java 17 ni minimal baseline deb oladi, shunga qaramay yangi loyihani Java 25 da boshlash to'g'ri, chunki keyingi ikki yil davomida yangilanish talab qilinmaydi.

### 13.12 Amalda qo'llash

- [ ] Loyihadagi barcha DTO va read model sinflarini ko'rib chiqing, mutable POJO larni record ga o'tkazing va validatsiyani compact konstruktorga yig'ing.
- [ ] `String type` yoki `int status` maydoni bilan boshqarilayotgan eng katta `if-else` zinapoyasini toping va uni sealed interface plus `switch` ifodasiga aylantiring.
- [ ] Barcha `Optional` maydonlarini va `Optional` parametrlarini grep bilan topib olib tashlang, `Optional` ni faqat qaytish qiymati sifatida qoldiring.
- [ ] `.get()` va `orElse` ichidagi qimmat chaqiruvlarni audit qiling, birinchisini `orElseThrow` ga, ikkinchisini `orElseGet` ga o'zgartiring.
- [ ] Domen istisnolari uchun bitta ildiz sinf va barqaror xato kodlari `enum` ini joriy qiling, `cause` yo'qotilayotgan joylarni tuzatib chiqing.
- [ ] Ommaviy paketlarga `package-info.java` da `@NullMarked` qo'ying va NullAway ni build darvozasi qilib yoqing.
- [ ] Kutubxona modullariga `japicmp` ni ulang va binary moslik buzilishini build yiqilishiga aylantiring, deprecate oynasini yozib hujjatlashtiring.
- [ ] CI matritsasiga production LTS dan tashqari keyingi JDK ni qo'shing va nightly build da uni ham sinaydigan qilib qo'ying.

## 14. JVM profiling va diagnostika: JFR, async-profiler, heap dump (JVM Profiling and Diagnostics)

Ishlab chiqarishda sekinlashgan to'lov servisi haqida xabar kelganda arxitektorning birinchi ishi kodga qarash emas. Birinchi ish JVM dan dalil olish: thread qayerda turgan, xotira qayerda yig'ilgan, vaqt qayerda yo'qolgan. JFR, async-profiler, thread dump va heap dump bu dalilni bir necha daqiqada beradi, lekin faqat ularni qanday o'qishni bilgan odamga. Bu bob shu asboblarning mexanikasi va ulardan qaror chiqarish tartibi haqida.

### 14.1 Diagnostika tartibi: avval o'lchov, keyin faraz, keyin tuzatish

Eng qimmat xato tartibni buzish: faraz qilib, darhol kodni o'zgartirish. Bunda siz tasodifan yaxshilangan yoki tasodifan yomonlashgan tizimni olasiz, lekin sabab haqida hech narsa bilmaysiz. To'g'ri tartib to'rt qadam: belgini raqamga aylantirish, resursni aniqlash, farazni tekshirish, keyin bitta o'zgarish kiritish.

Belgini raqamga aylantirish degani "sekin" so'zini "p99 latency 180 ms dan 2.4 s ga chiqdi, p50 esa 60 ms da qoldi" deb yozish. p50 o'zgarmagani muhim dalil: bu bir qism so'rov navbatda kutayotganini bildiradi. Navbat esa yoki thread pool, yoki connection pool, yoki GC pauza, yoki tashqi I/O.

Keyin resursni ajratish kerak. CPU to'lgan bo'lsa profiling kerak. CPU bo'sh, lekin latency baland bo'lsa, bu kutish, ya'ni wall-clock profiling yoki thread dump kerak. Xotira o'sib borsa heap dump kerak. Bitta asbob hamma holatga yaramaydi, shuning uchun resursni noto'g'ri aniqlash bir soatni yo'qotadi.

### 14.2 Thread dump olish va o'qish: `jstack`, bloklangan thread, lock egasi

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

### 14.3 Heap dump olish (`jmap`, `-XX:+HeapDumpOnOutOfMemoryError`) va tahlil qilish

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

### 14.4 Java Flight Recorder: yozuvni boshlash, sozlash profili, qancha ortiqcha yuk beradi

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

### 14.5 JFR da nimaga qarash: allokatsiya, GC, lock contention, I/O kutish

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

### 14.6 async-profiler va flame graph o'qish: CPU, allokatsiya, wall-clock rejimi

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

### 14.7 `jcmd` buyruqlari: eng foydali to'plam

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

### 14.8 Mikro o'lchov tuzoqlari va JMH nega kerak

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

### 14.9 Ishlab chiqarish muhitida profiling: xavfsizlik va ortiqcha yuk masalasi

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

### 14.10 Spring Boot Actuator orqali diagnostika endpointlari

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

### 14.11 Tez-tez uchraydigan diagnoz: sekin so'rov, thread pool to'lishi, xotira sizishi

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

### 14.12 Amalda qo'llash

- [ ] Barcha ishlab chiqarish JVM lariga `-XX:StartFlightRecording` ni `settings=default`, `maxage=4h`, `dumponexit=true` bilan qo'shing va yozuv faylini doimiy volume ga chiqaring.
- [ ] `-XX:+HeapDumpOnOutOfMemoryError`, `-XX:HeapDumpPath` va `-XX:+ExitOnOutOfMemoryError` ni qo'shing, `HeapDumpPath` volume ida heap dan 2 barobar bo'sh joy borligini tekshirib ko'ring.
- [ ] GC va safepoint loglarini `-Xlog:gc*,safepoint` bilan fayl rotatsiyasi ostida yoqing va 7 kundan kam bo'lmagan muddatga saqlang.
- [ ] Konteyner image ichida `jcmd`, `jfr` va async-profiler mavjudligini tekshiring, yo'q bo'lsa image ga qo'shing.
- [ ] Incident uchun bitta runbook yozing: uch thread dump, JFR `profile` 10 daqiqa, keyin kerak bo'lsa izolyatsiyalangan instansiyada heap dump.
- [ ] Actuator ni `management.server.port` orqali alohida portga chiqaring, `heapdump` endpointini o'chiring va health detallarini faqat autentifikatsiyadan keyin ko'rsatadigan qilib qo'ying.
- [ ] `hikaricp.connections.pending`, `executor.queued` va `jvm.gc.pause` uchun alert qo'ying, chunki bu uchtasi latency muammosini belgidan oldin ko'rsatadi.
- [ ] Eng qimmat ikkita hot path uchun JMH benchmark yozing va uning natijasini servis darajasidagi yuk testi bilan taqqoslab tekshirib ko'ring.


# III. Spring chuqur bilim

## 15. Spring Core mexanikasi: IoC konteyner, bean lifecycle, AOP proxy (Spring Core Mechanics)

Spring konteyneri sehr emas, u aniq tartibda ishlaydigan mexanizm. Arxitektor uchun bu mexanizmni bilish zarurati amaliy: ishga tushish vaqti, aylanma bog'liqlik xatosi, `@Transactional` ning jim turib ishlamasligi va event larning tranzaksiya bilan noto'g'ri bog'lanishi hammasi shu mexanizmdan kelib chiqadi. Quyida konteyner ichida nima sodir bo'lishini bosqichma-bosqich ko'rib chiqamiz va har bosqichga bog'langan tuzoqlarni ajratamiz. Misollar to'lov servisi, buyurtma va ombor qoldig'i domenidan olingan.

### 15.1 `ApplicationContext` ishga tushish bosqichlari: bean definition, post-processor, instantiation

`AbstractApplicationContext.refresh()` ketma-ketligi Spring Framework 6.x da deterministik. Avval `obtainFreshBeanFactory()` bo'sh `DefaultListableBeanFactory` yaratadi. Keyin `invokeBeanFactoryPostProcessors()` chaqiriladi va aynan shu nuqtada `ConfigurationClassPostProcessor` komponent skanerlashni bajaradi, `@Configuration` sinflarini o'qiydi, `@Bean` metodlaridan bean definition lar yasaydi. Bu bosqichda hech bir business bean yaratilmagan, faqat metadata bor.

Keyin `registerBeanPostProcessors()` `BeanPostProcessor` larni topadi va ularni ro'yxatga oladi. Faqat shundan keyin `finishBeanFactoryInitialization()` barcha singleton larni haqiqatan instantiate qiladi. Oxirida `finishRefresh()` `ContextRefreshedEvent` ni yuboradi va `SmartLifecycle` bean larini ishga tushiradi.

```java
// Bean definition bosqichida qancha bean ro'yxatga olinganini ko'rish.
// Bu metadata, hali hech narsa yaratilmagan.
@Component
class DefinitionAudit implements BeanFactoryPostProcessor {

    @Override
    public void postProcessBeanFactory(ConfigurableListableBeanFactory bf) {
        // Bu yerda getBean() chaqirmaymiz: bean ni muddatidan oldin
        // yaratib, uni proxy lanmay qolishiga olib kelamiz.
        System.out.println("definition soni: " + bf.getBeanDefinitionCount());
        BeanDefinition bd = bf.getBeanDefinition("paymentService");
        System.out.println("scope: " + bd.getScope()
                + ", lazy: " + bd.isLazyInit());
    }
}
```

Amaliy xulosa: definition bosqichida bean ni `getBean()` bilan tortib olish eng tipik xato. Bean `BeanPostProcessor` lar ro'yxatga olinishidan oldin yaratiladi va na `@Transactional`, na `@Async` proxy ni oladi. Log dagi "is not eligible for getting processed by all BeanPostProcessors" ogohlantirishi aynan shuni bildiradi.

### 15.2 `BeanFactoryPostProcessor` va `BeanPostProcessor` farqi va ularning tartibi

Ikkisi nomi o'xshash, lekin ular butunlay boshqa bosqichda ishlaydi. `BeanFactoryPostProcessor` bean definition ni, ya'ni retseptni o'zgartiradi. `BeanPostProcessor` esa allaqachon yaratilgan obyektni, ya'ni tayyor taomni o'zgartiradi yoki uni proxy bilan o'raydi.

| Jihat | `BeanFactoryPostProcessor` | `BeanPostProcessor` |
|---|---|---|
| Nima bilan ishlaydi | `BeanDefinition` (metadata) | instance (obyekt) |
| Chaqirilish vaqti | singleton lar yaratilishidan oldin, bir marta | har bir bean yaratilganda |
| Tipik vazifa | property qiymatini almashtirish, definition qo'shish | AOP proxy o'rash, `@Autowired` ni bajarish |
| Platforma misoli | `ConfigurationClassPostProcessor`, `PropertySourcesPlaceholderConfigurer` | `AutowiredAnnotationBeanPostProcessor`, `AnnotationAwareAspectJAutoProxyCreator` |
| Tartib mexanizmi | `PriorityOrdered`, keyin `Ordered`, keyin qolganlar | xuddi shu uch guruh |
| Xato narxi | kontekst ko'tarilmaydi | bean proxy siz qoladi, xato jim o'tadi |

`BeanDefinitionRegistryPostProcessor` esa `BeanFactoryPostProcessor` ning kengaytmasi va u yangi definition qo'shish imkonini beradi. Spring uni birinchi chaqiradi, chunki definition qo'shish definition o'zgartirishdan oldin bo'lishi shart.

```java
// To'lov provayderlarini konfiguratsiyadan dinamik ro'yxatga olish.
// Har bir provayder uchun alohida bean definition yasaymiz.
class ProviderRegistrar implements BeanDefinitionRegistryPostProcessor {

    @Override
    public void postProcessBeanDefinitionRegistry(BeanDefinitionRegistry reg) {
        for (String code : List.of("uzcard", "humo", "visa")) {
            AbstractBeanDefinition bd = BeanDefinitionBuilder
                    .genericBeanDefinition(HttpPaymentGateway.class)
                    .addConstructorArgValue(code)
                    .setLazyInit(true)   // kerak bo'lmasa yaratilmaydi
                    .getBeanDefinition();
            reg.registerBeanDefinition("gateway_" + code, bd);
        }
    }
}
```

`BeanPostProcessor` yozganda bitta qoida bor: u imkon qadar kam dependency ga ega bo'lsin. Post-processor boshqa bean ga muhtoj bo'lsa, o'sha bean ham muddatidan oldin yaratiladi va proxy siz qoladi. Shu sababli kerakli bean ni `ObjectProvider` orqali kechiktirib olish to'g'ri usul.

### 15.3 Bean lifecycle: konstruktor, inject, `@PostConstruct`, `@PreDestroy`

Bitta singleton bean uchun tartib qat'iy: konstruktor ishlaydi, keyin field va setter inject qilinadi, keyin `Aware` interfeyslari chaqiriladi, keyin `BeanPostProcessor.postProcessBeforeInitialization()`, keyin `@PostConstruct`, keyin `InitializingBean.afterPropertiesSet()`, keyin `@Bean(initMethod)`, va oxirida `postProcessAfterInitialization()`. Proxy aynan oxirgi qadamda yasaladi.

```java
@Service
public class PaymentService {

    private final PaymentGateway gateway;
    private final MeterRegistry meters;
    private Counter failures;

    // 1-qadam: konstruktor. Dependency lar shu yerda yetib keladi.
    public PaymentService(PaymentGateway gateway, MeterRegistry meters) {
        this.gateway = gateway;
        this.meters = meters;
        // Bu yerda gateway ni ISHLATMAYMIZ: u hali proxy lanmagan
        // bo'lishi mumkin va tranzaksiya ishlamaydi.
    }

    // 2-qadam: barcha dependency tayyor, og'ir ish shu yerda.
    @PostConstruct
    void init() {
        this.failures = meters.counter("payment.failures");
    }

    // Faqat singleton uchun chaqiriladi va faqat graceful shutdown da.
    @PreDestroy
    void drain() {
        gateway.closeIdleConnections();
    }
}
```

Eng ko'p uchraydigan tuzoq: konstruktor ichida inject qilingan bean ning metodini chaqirish. O'sha payt proxy hali yo'q, demak `@Transactional` ishlamaydi. Og'ir initializatsiya va cache warm-up `@PostConstruct` yoki `ApplicationReadyEvent` ga tegishli.

`@PreDestroy` ishonchliligi cheklangan: u faqat kontekst normal yopilganda ishlaydi. `kill -9`, OOM killer yoki `terminationGracePeriodSeconds` tugaganda bajarilmaydi, shuning uchun unga majburiy business logika qo'yish xato. Kubernetes da `server.shutdown=graceful` va `spring.lifecycle.timeout-per-shutdown-phase=30s` kerak, pod grace period esa taxminan 45 sekund bo'lsin.

### 15.4 Scope lar: singleton, prototype, request va ularning amaliy oqibati

Default scope singleton va u konteyner darajasidagi yakka nusxa. Bu degani singleton bean da o'zgaradigan holat saqlash thread safety buzilishiga olib keladi. Prototype har `getBean()` da yangi obyekt beradi, lekin Spring uni kuzatmaydi va `@PreDestroy` ni chaqirmaydi. Shu sababli prototype ichida resurs ochish xotira sizishiga olib keladi.

Eng nozik joy: prototype yoki request scope bean ni singleton ga to'g'ridan to'g'ri inject qilish. Singleton bir marta yaratilganda bir marta inject oladi, demak prototype bir martagina olinadi va amalda singleton ga aylanadi.

```java
@Service
public class ReportService {

    // Noto'g'ri: prototype faqat bir marta olinadi.
    // @Autowired private ReportBuffer buffer;

    // To'g'ri: har chaqiruvda yangi nusxa.
    private final ObjectProvider<ReportBuffer> bufferProvider;

    ReportService(ObjectProvider<ReportBuffer> bufferProvider) {
        this.bufferProvider = bufferProvider;
    }

    public byte[] build(long orderId) {
        ReportBuffer buffer = bufferProvider.getObject();
        try {
            return buffer.render(orderId);
        } finally {
            buffer.close();   // prototype ni O'ZIMIZ yopamiz
        }
    }
}

// Request scope ni singleton ga inject qilish uchun proxy shart.
@Component
@RequestScope   // ichida proxyMode = TARGET_CLASS
class CurrentUserContext { }
```

Request scope da yana bir tuzoq bor: `@Async` yoki `CompletableFuture` ichida request scope bean ga murojaat qilish `BeanCreationException` beradi, chunki yangi thread da request yo'q. Kerakli qiymatni asinxron ishga uzatishdan oldin oddiy obyektga ko'chirib olish kerak.

### 15.5 Bog'liqlikni kiritish usullari va nega konstruktor orqali kiritish afzal

Uch usul bor: konstruktor, setter va field. Konstruktor orqali kiritish yagona to'g'ri default. Sababi mexanik, estetik emas.

Konstruktor `final` field ga ruxsat beradi, demak dependency o'zgarmaydi va thread safe publication kafolatlanadi. Obyekt hamisha to'liq holatda tug'iladi. Parametrlar sonining o'sishi dizayn muammosini ko'rsatadigan ochiq signal, field inject esa buni yashiradi. Va konstruktor aylanma bog'liqlikni yashirmay, darhol oshkor qiladi.

| Vazifa | Oddiy yondashuv | Arxitektor yondashuvi |
|---|---|---|
| Dependency kiritish | `@Autowired` field ga | konstruktor, `final` field |
| Dependency soni 8 ta bo'lsa | hammasini inject qilish | sinfni bo'lish, facade ajratish |
| Bir interfeys, ikki implementatsiya | `@Primary` bilan tezda yopish | `@Qualifier` yoki alohida tip bilan aniq ko'rsatish |
| Aylanma bog'liqlik | `allow-circular-references=true` | mas'uliyatni ajratish yoki event bilan uzish |
| Ishga tushish sekin | `lazy-initialization=true` yoqish | `/actuator/startup` bilan o'lchash, bean larni kamaytirish |
| Kesh ishlamayapti | `@Cacheable` ni ko'chirish | self-invocation ekanini tekshirish, chaqiruvni tashqariga olish |
| Event bilan ish | `@EventListener` da DB yozish | `@TransactionalEventListener(AFTER_COMMIT)` |
| Komponent skanerlash | ildiz paketdan hammasini | aniq paketlar va `@ConditionalOnProperty` |
| Prototype resursi | GC ga ishonish | `ObjectProvider` va qo'lda yopish |
| Shutdown | `@PreDestroy` ga tayanish | idempotent qayta ishlash, outbox orqali kafolat |

Setter inject faqat ixtiyoriy bog'liqlik uchun o'rinli. Field inject esa testda reflection talab qiladi va sinfni konteynerga mahkamlab qo'yadi.

### 15.6 Aylanma bog'liqlik: nega paydo bo'ladi, Spring Boot 3 da nega xato beradi

`OrderService` `PaymentService` ga, `PaymentService` esa `OrderService` ga muhtoj bo'lsa aylanma bog'liqlik paydo bo'ladi. Konstruktor orqali kiritishda Spring bu halqani uza olmaydi, chunki ikkisidan birini yaratish uchun ikkinchisi tayyor bo'lishi kerak. Field inject da Spring yarim yaratilgan obyektni "early reference" sifatida berib, halqani yashiradi va shu bilan muammoni ertaga suradi.

Spring Boot 2.6 dan boshlab `spring.main.allow-circular-references` default `false`, Spring Boot 3.x da ham shunday. Natijada kontekst `BeanCurrentlyInCreationException` bilan ko'tarilmaydi. Bu to'g'ri qaror: halqa doim mas'uliyat chegarasi noto'g'ri chizilganini ko'rsatadi.

```properties
# Bu flag ni yoqish muammoni yashiradi, yechmaydi.
# Faqat legacy kodni vaqtincha ishga tushirish uchun.
spring.main.allow-circular-references=false

# Ishga tushishni tezlashtirish, lekin xatolar runtime ga suriladi.
spring.main.lazy-initialization=false

# Spring Boot da default allaqachon true: hamma joyda CGLIB.
spring.aop.proxy-target-class=true

# Graceful shutdown: @PreDestroy ga real imkon beradi.
server.shutdown=graceful
spring.lifecycle.timeout-per-shutdown-phase=30s
```

Halqani uzishning uch yo'li bor: umumiy logikani uchinchi bean ga ajratish (narx hisobini `PricingCalculator` ga chiqarish), yo'nalishni event bilan teskari qilish (`PaymentService` `PaymentCompletedEvent` yuboradi), yoki kichik interfeys ajratib faqat kerakli shartnomani inject qilish. `@Lazy` bilan yopish ishlaydi lekin dizayn qarzini qoldiradi.

### 15.7 `@Lazy`, `@Primary`, `@Qualifier`, `@Conditional` qachon kerak

`@Lazy` bean ni birinchi murojaatga qadar yaratmaydi. U og'ir, kamdan kam ishlatiladigan bean uchun foydali, masalan yiliga bir marta ishlaydigan hisobot eksporteri. Lekin `@Lazy` xatoni ishga tushish vaqtidan birinchi so'rov vaqtiga suradi, ya'ni fail-fast ni yo'qotadi. Shuning uchun uni global yoqish emas, nuqtali qo'llash to'g'ri.

`@Primary` bir nechta nomzod bo'lganda default ni belgilaydi. `@Qualifier` esa chaqiruv joyida aniq tanlaydi. Qoida sodda: agar tanlov kontekstga bog'liq bo'lsa `@Qualifier`, agar haqiqatan bitta "asosiy" implementatsiya bo'lsa `@Primary`. Ikkisini aralashtirib ishlatish eng qiyin topiladigan konfiguratsiya xatolariga olib keladi.

```java
@Configuration
class GatewayConfig {

    // Asosiy provayder: boshqa joyda qualifier yozilmasa shu olinadi.
    @Bean
    @Primary
    PaymentGateway uzcardGateway(GatewayProperties props) {
        return new HttpPaymentGateway(props.uzcard());
    }

    // Faqat property yoqilgan bo'lsa yaratiladi: ortiqcha bean bo'lmaydi.
    @Bean
    @Qualifier("fallback")
    @ConditionalOnProperty(name = "payment.visa.enabled", havingValue = "true")
    PaymentGateway visaGateway(GatewayProperties props) {
        return new HttpPaymentGateway(props.visa());
    }

    // Test profilida haqiqiy HTTP ga chiqmaydigan stub.
    @Bean
    @ConditionalOnMissingBean(PaymentGateway.class)
    PaymentGateway noopGateway() {
        return new NoopPaymentGateway();
    }
}
```

`@Conditional` va uning Boot dagi shakllari (`@ConditionalOnProperty`, `@ConditionalOnMissingBean`, `@ConditionalOnClass`) definition bosqichida ishlaydi: shart bajarilmasa bean umuman ro'yxatga olinmaydi. Bu startup ni qisqartirishning eng arzon usuli. `@ConditionalOnMissingBean` tartibga sezgir, uni faqat auto-configuration ichida ishlatish kerak.

### 15.8 AOP mexanikasi: JDK dinamik proxy va CGLIB farqi

Spring AOP byte code ni o'zgartirmaydi, u proxy yasaydi. Ikki mexanizm bor. JDK dinamik proxy interfeys asosida ishlaydi va faqat interfeysda e'lon qilingan metodlarni ushlaydi. CGLIB esa sinfdan subclass yasaydi va metodlarni override qiladi.

| Jihat | JDK dinamik proxy | CGLIB |
|---|---|---|
| Talab | kamida bitta interfeys | nofinal sinf, nofinal metod |
| Nimani ushlaydi | interfeys metodlari | barcha public va protected metodlar |
| `final` sinf | muammo yo'q | proxy yasalmaydi, xato |
| `private` metod | ushlanmaydi | ushlanmaydi |
| Konstruktor | chaqirilmaydi | subclass konstruktori chaqiriladi |
| Tipga cast | faqat interfeysga | konkret sinfga ham |

Spring Boot da `spring.aop.proxy-target-class` default `true`, ya'ni CGLIB ishlatiladi hatto interfeys bo'lsa ham. Bu bilimsiz holda tuzoqqa aylanadi: agar kod `@Autowired` bilan interfeysni emas, konkret sinfni kutsa va boshqa joyda JDK proxy yasalgan bo'lsa, `BeanNotOfRequiredTypeException` chiqadi. Shuning uchun injection nuqtalarida interfeysga tayanish ishonchliroq.

Spring Framework 6.x da CGLIB qayta paketlangan holda ichida keladi. Lekin u `final` metodni override qila olmaydi, demak `@Transactional` qo'yilgan `final` metod jim tranzaksiyasiz ishlaydi. Kotlin da sinflar default `final` bo'lgani uchun bu muammo tez yuzaga keladi.

### 15.9 Proxy tuzog'i: ichki metod chaqiruvida `@Transactional` va `@Cacheable` ishlamasligi

Bu eng ko'p takrorlanadigan va eng jim o'tadigan xato. Proxy faqat tashqaridan kelgan chaqiruvni ushlaydi. Bir sinf ichida `this.method()` chaqirilsa, chaqiruv proxy dan o'tmaydi va annotatsiya butunlay e'tiborsiz qoladi. Kompilyator ogohlantirmaydi, test ham ko'pincha o'tadi.

```java
@Service
public class StockService {

    private final StockRepository repo;
    private final StockService self;   // o'ziga proxy orqali havola

    StockService(StockRepository repo, @Lazy StockService self) {
        this.repo = repo;
        this.self = self;
    }

    public void importBatch(List<StockRow> rows) {
        for (StockRow row : rows) {
            // NOTO'G'RI: this orqali, proxy chetlab o'tiladi,
            // REQUIRES_NEW ishlamaydi, hamma narsa bitta tranzaksiyada.
            // applyRow(row);

            // TO'G'RI: proxy orqali o'tadi, har qator alohida tranzaksiya.
            self.applyRow(row);
        }
    }

    @Transactional(propagation = Propagation.REQUIRES_NEW)
    public void applyRow(StockRow row) {
        repo.decrease(row.sku(), row.qty());
    }
}
```

Uch yechim bor va ularning narxi farq qiladi. Eng toza yechim mas'uliyatni ikki bean ga ajratish, chunki `importBatch` orkestratsiya, `applyRow` esa tranzaksional birlik va ular bir sinfda turishi majburiy emas. Ikkinchisi yuqoridagidek `@Lazy` self-injection, u ishlaydi lekin niyatni yashiradi. Uchinchisi `TransactionTemplate` ni to'g'ridan to'g'ri ishlatish, bu annotatsiyadan ko'ra ochiqroq va test qilish osonroq.

| Tuzoq | Nima sodir bo'ladi | Yechim |
|---|---|---|
| `this.method()` ichki chaqiruvi | annotatsiya e'tiborsiz, tranzaksiya yo'q | bean ni bo'lish yoki `TransactionTemplate` |
| `@Transactional` `private` metodda | proxy ushlamaydi, jim o'tadi | `public` qilish va tashqaridan chaqirish |
| `@Transactional` `final` metodda | CGLIB override qila olmaydi | `final` ni olib tashlash |
| `@PostConstruct` ichida `@Transactional` chaqiruvi | proxy hali tayyor emas | `ApplicationReadyEvent` da bajarish |
| `@Cacheable` o'sha sinf ichidan | kesh hamisha bo'sh, DB yuklanadi | chaqiruvni tashqi bean ga chiqarish |
| `@Async` metod `void` va exception | xato yo'qoladi | `CompletableFuture` qaytarish |
| Prototype singleton ichida | bir marta olinadi | `ObjectProvider` |
| Request scope `@Async` ichida | `BeanCreationException` | qiymatni oldin DTO ga ko'chirish |

### 15.10 `ApplicationEvent` va `@EventListener`: sinxron tabiati va tranzaksiya bilan bog'liqligi

`ApplicationEventPublisher.publishEvent()` default holda SINXRON. `SimpleApplicationEventMulticaster` listener larni chaqiruvchi thread da ketma-ket ishga tushiradi. Demak event yuborish "fire and forget" emas: listener sekin bo'lsa publisher kutadi, listener exception tashlasa publisher ham yiqiladi. Bu ko'pincha noto'g'ri tushuniladi va event lar yengil deb o'ylanadi.

Ikkinchi muhim nuqta tranzaksiya. Oddiy `@EventListener` hali ochiq tranzaksiya ichida ishlaydi. Agar listener email yuborsa yoki tashqi API ga chiqsa, keyin esa tranzaksiya rollback bo'lsa, email yuborilgan, lekin buyurtma yo'q. Bu klassik nomuvofiqlik.

```java
@Component
class PaymentNotifier {

    // Commit dan KEYIN ishlaydi: rollback bo'lsa umuman chaqirilmaydi.
    @TransactionalEventListener(phase = TransactionPhase.AFTER_COMMIT)
    public void onPaid(PaymentCompletedEvent e) {
        // Diqqat: bu yerdagi DB yozish yangi tranzaksiya talab qiladi.
        notifier.send(e.orderId());
    }

    // Asinxron: alohida thread, publisher kutmaydi.
    // Lekin xato publisher ga qaytmaydi, log qilish MAJBURIY.
    @Async
    @EventListener
    public void onAudit(PaymentCompletedEvent e) {
        auditLog.append(e);
    }
}
```

`AFTER_COMMIT` fazasida DB ga yozmoqchi bo'lsangiz, u avtomatik yangi tranzaksiyaga tushmaydi, shuning uchun `REQUIRES_NEW` ni aniq ko'rsatish kerak. Yuborish kafolati talab qilinsa, event emas, dizayn patternlar hujjatidagi outbox yondashuvi to'g'ri, chunki `AFTER_COMMIT` dan keyin JVM o'lsa xabar yo'qoladi.

### 15.11 Ishga tushish vaqtini qisqartirish: ortiqcha bean va komponent skanerlash

Oddiy monolitda 3000 dan 8000 gacha bean bo'lishi mumkin va ishga tushish 15 sekunddan 60 sekundgacha cho'ziladi. Kubernetes da bu readiness probe va rolling update tezligiga to'g'ridan to'g'ri ta'sir qiladi. Birinchi qadam taxmin qilmaslik, o'lchash.

```bash
# 1. Startup qadamlarini yozib olish uchun actuator endpoint.
#    Config: BufferingApplicationStartup bean sifatida ro'yxatga olinadi.
curl -s localhost:8080/actuator/startup | jq \
  '.timeline.events | sort_by(-.duration) | .[0:15]
   | map({name: .startupStep.name, ms: (.duration | ltrimstr("PT"))})'

# 2. Auto-configuration hisobotini ko'rish: nima yoqilgan, nima yo'q.
java -jar app.jar --debug 2>&1 | sed -n '/Positive matches/,/Exclusions/p'

# 3. AOT bosqichini oldindan bajarish (Spring Boot 3.x).
./mvnw -Pnative spring-boot:process-aot

# 4. CDS arxivi: Spring Boot 3.3+ da ishga tushishni taxminan
#    30-40 foizga qisqartiradi.
java -XX:ArchiveClassesAtExit=app.jsa -Dspring.context.exit=onRefresh -jar app.jar
java -XX:SharedArchiveFile=app.jsa -jar app.jar
```

Eng katta g'oliblar quyidagilar. Komponent skanerlash doirasini toraytirish, ya'ni `@SpringBootApplication(scanBasePackages = ...)` bilan aniq paketlarni ko'rsatish, chunki ildiz paketdan skanerlash kutubxona paketlariga ham kirib ketadi. Keraksiz auto-configuration larni `spring.autoconfigure.exclude` bilan o'chirish. Ishlatilmaydigan starter larni `pom.xml` dan olib tashlash, ayniqsa bir nechta template engine yoki ikkita HTTP client qolgan loyihalarda.

Connection pool ham ta'sir qiladi: HikariCP da `minimum-idle` ni `maximum-pool-size` ga teng qo'yish start paytida barcha connection ni ochadi. Odatiy web servis uchun pool 10 dan 20 gacha yetarli, undan kattasi PostgreSQL tomonda zarar keltiradi.

`spring.main.lazy-initialization=true` ishga tushishni taxminan ikki baravar tezlashtiradi, lekin konfiguratsiya xatolari birinchi so'rovga suriladi. Shuning uchun uni faqat lokal development profilida yoqish mantiqiy, production da esa fail-fast qimmatliroq. Spring Framework 6.2 dan boshlab sekin bean larni fonda initsializatsiya qilish imkoni bor va u asosan tashqi ulanish kutadigan bean lar uchun foyda beradi.

### 15.12 Amalda qo'llash

- [ ] `/actuator/startup` ni `BufferingApplicationStartup` bilan yoqib, eng sekin 15 ta qadamni yozib ol va ishga tushish vaqtini bazaviy raqam sifatida qayd qil.
- [ ] Kod bazasida `@Transactional` va `@Cacheable` qo'yilgan barcha metodlarni tekshirib, ichki `this.` chaqiruvi orqali chaqirilayotganlarini top va chaqiruvni tashqariga chiqar.
- [ ] `final` yoki `private` metodda turgan `@Transactional`, `@Async`, `@Cacheable` annotatsiyalarini grep bilan izla va ularni tuzat, chunki ular jim ishlamayapti.
- [ ] `spring.main.allow-circular-references` ni `false` holatida qoldirib kontekstni ko'tar, chiqqan halqalarni `@Lazy` bilan yopmay, mas'uliyatni ajratib yech.
- [ ] Tashqi effekt beradigan (email, SMS, tashqi API) barcha `@EventListener` larni ko'rib chiq va ularni `@TransactionalEventListener(AFTER_COMMIT)` ga o'tkaz.
- [ ] `--debug` bilan auto-configuration hisobotini olib, ishlatilmaydigan starter larni va auto-configuration larni `spring.autoconfigure.exclude` bilan o'chir.
- [ ] `scanBasePackages` ni aniq paketlar ro'yxatiga qisqartirib, bean definition sonining oldin va keyingi farqini o'lchab yoz.
- [ ] `server.shutdown=graceful` va `spring.lifecycle.timeout-per-shutdown-phase` ni sozlab, Kubernetes grace period ini undan kattaroq qilib qo'y.

## 16. Spring Boot mexanikasi: auto-configuration, starter, Actuator (Spring Boot Mechanics)

Spring Boot ko'pchilik uchun "sehr" bo'lib ko'rinadi, lekin ichida sehr yo'q. Bor-yo'g'i classpath da nima borligini o'qiydigan shartli konfiguratsiya mexanizmi va bean ni faqat foydalanuvchi o'zi bermagan holda yaratadigan qoida bor. Arxitektor uchun bu mexanikani bilish ikki narsani beradi: ishga tushmayotgan kontekstni daqiqalarda emas, sekundlarda tushuntirish, va o'z jamoasi uchun to'g'ri sozlanadigan umumiy kutubxona qurish. Quyida auto-configuration ning ichki ishlashi, konfiguratsiya ustunligi, Actuator ning xavfsiz qismi va startup vaqtini qisqartirish yo'llari ko'rib chiqiladi.

### 16.1 Auto-configuration qanday ishlaydi: `AutoConfiguration.imports` va shartli annotatsiyalar

`@SpringBootApplication` ichida `@EnableAutoConfiguration` bor, u esa `AutoConfigurationImportSelector` ni ishga soladi. Bu selector classpath dagi barcha jar lardan `META-INF/spring/org.springframework.boot.autoconfigure.AutoConfiguration.imports` faylini o'qiydi. Fayl oddiy matn: har qatorda bitta konfiguratsiya sinfining to'liq nomi. Spring Boot 2.7 gacha bu ro'yxat `META-INF/spring.factories` ichida edi, 3.x da faqat yangi format o'qiladi.

Keyingi qadam filtrlash. Boot ro'yxatdagi yuzlab sinfni darhol yuklamaydi, avval `spring-autoconfigure-metadata.properties` orqali `@ConditionalOnClass` shartlarini ASM bilan tekshiradi. Shu sababli `DataSourceAutoConfiguration` sizda JDBC driver bo'lmasa, umuman sinf sifatida yuklanmaydi. Bu startup ni sezilarli tezlashtiradi: tipik servisda ro'yxatdagi 150 dan ortiq nomzoddan odatda 25-40 tasi qoladi.

```properties
# to'lov servisi uchun o'z starter faylimiz
# src/main/resources/META-INF/spring/
#   org.springframework.boot.autoconfigure.AutoConfiguration.imports
com.acme.payment.autoconfigure.PaymentClientAutoConfiguration
com.acme.payment.autoconfigure.PaymentRetryAutoConfiguration
com.acme.payment.autoconfigure.PaymentMetricsAutoConfiguration
```

Muhim nuance: auto-configuration sinflari oddiy `@Configuration` dan keyin qayta ishlanadi. Ya'ni sizning ilovangizdagi `@Configuration` va `@Component` lar har doim birinchi ro'yxatga olinadi, auto-configuration esa oxirida "bo'sh joylarni to'ldiradi". Shuning uchun `@ConditionalOnMissingBean` ishlaydi: sizning bean ingiz allaqachon registratsiyada bo'ladi.

### 16.2 `@ConditionalOnClass`, `@ConditionalOnMissingBean` va tartib (`@AutoConfigureAfter`)

`@ConditionalOnClass` javobgarligi: "bu integratsiya umuman mumkinmi". `@ConditionalOnMissingBean` javobgarligi: "foydalanuvchi o'zi bermaganmi". `@ConditionalOnProperty` javobgarligi: "buni yoqishni xohlashdimi". Uchtasini aralashtirmaslik kerak. Masalan Kafka client classpath da bo'lsa ham, ombor qoldig'i eventlarini yuborish `acme.inventory.events.enabled=true` bo'lmaganda yoqilmasligi kerak.

Spring Boot 3.x da auto-configuration sinfi `@Configuration` emas, `@AutoConfiguration` bilan belgilanadi. Bu annotatsiya `proxyBeanMethods = false` ni o'zi o'rnatadi va tartibni to'g'ridan-to'g'ri atributlarda qabul qiladi: `@AutoConfiguration(after = DataSourceAutoConfiguration.class)`. Alohida `@AutoConfigureAfter` va `@AutoConfigureBefore` ham ishlaydi, lekin yangi kodda atributlar afzal.

```java
@AutoConfiguration(after = { DataSourceAutoConfiguration.class })
@ConditionalOnClass(name = "com.acme.payment.sdk.PaymentGateway")
@ConditionalOnProperty(prefix = "acme.payment", name = "enabled",
                       matchIfMissing = true)
@EnableConfigurationProperties(PaymentProperties.class)
public class PaymentClientAutoConfiguration {

    // foydalanuvchi o'z PaymentGateway ini bersa, biz chetga chiqamiz
    @Bean
    @ConditionalOnMissingBean
    PaymentGateway paymentGateway(PaymentProperties props,
                                  RestClient.Builder builder) {
        RestClient client = builder
                .baseUrl(props.baseUrl())
                .requestFactory(timeouts(props))   // connect 2s, read 5s
                .build();
        return new HttpPaymentGateway(client, props.merchantId());
    }
}
```

Tartib faqat auto-configuration lar orasidagi `@ConditionalOnMissingBean` natijasiga ta'sir qiladi. Agar `A` auto-config `B` ning bean iga qarab qaror qilsa, `A` majburan `B` dan keyin ishlashi kerak, aks holda shart tasodifiy natija beradi. Bu eng ko'p uchraydigan xato: tartib ko'rsatilmagan, lokal mashinada ishlaydi, CI da sinadi.

### 16.3 Auto-configuration ni tekshirish: `--debug` va shartlar hisoboti

`--debug` flagi bilan ishga tushirish `ConditionEvaluationReport` ni konsolga chiqaradi. U uch blokdan iborat: `Positive matches` (nima yoqildi va nima uchun), `Negative matches` (nima yoqilmadi va qaysi shart bajarilmadi), `Exclusions` va `Unconditional classes`. Bu hisobot "nega mening `DataSource` im yaratilmadi" savoliga to'g'ridan-to'g'ri javob beradi.

```bash
# shartlar hisobotini olish va kerakli qismni filtrlash
java -jar payment-service.jar --debug 2>&1 | tee startup.log
grep -A 5 "DataSourceAutoConfiguration" startup.log

# Actuator orqali ishlayotgan ilovada
curl -s localhost:8081/actuator/conditions \
  | jq '.contexts.application.negativeMatches
        | to_entries | map(select(.key | test("Payment")))'
```

Ishlab chiqarishda `--debug` ishlatish o'rinli emas, chunki u root logger ni DEBUG ga o'tkazmaydi lekin hisobot hajmi katta. Buning o'rniga `conditions` endpoint ni staging da yoqib qo'yish yetarli. Test darajasida esa auto-configuration ni to'liq kontekst ko'tarmasdan `ApplicationContextRunner` bilan tekshirish mumkin: u shartlarni real tarzda baholaydi va taxminan 20-50 ms da natija beradi.

```java
private final ApplicationContextRunner runner = new ApplicationContextRunner()
        .withConfiguration(AutoConfigurations.of(PaymentClientAutoConfiguration.class));

@Test
void foydalanuvchiBeani_ustunlikQiladi() {
    runner.withUserConfiguration(CustomGatewayConfig.class)
          .withPropertyValues("acme.payment.base-url=https://pay.local")
          .run(ctx -> assertThat(ctx).getBean(PaymentGateway.class)
                                     .isSameAs(ctx.getBean("myGateway")));
}

@Test
void ocharishMumkin() {
    runner.withPropertyValues("acme.payment.enabled=false")
          .run(ctx -> assertThat(ctx).doesNotHaveBean(PaymentGateway.class));
}
```

### 16.4 Starter yozish: o'z jamoangiz uchun umumiy kutubxona qurish qoidalari

Starter ikki artefaktdan iborat bo'lishi kerak: `acme-payment-spring-boot-autoconfigure` (kod va shartlar) va `acme-payment-spring-boot-starter` (faqat dependency ro'yxati, kodsiz). Nomlash qoidasi qat'iy: `spring-boot-starter-` prefiksi Spring jamoasiga tegishli, sizning starter `acme-payment-spring-boot-starter` ko'rinishida bo'lishi kerak. Bu shunchaki odob emas, Maven koordinatalarining kim tomonidan qo'llab-quvvatlanishini aytib turadi.

Starter ichida hech qachon `spring-boot-starter-web` yoki boshqa katta starter ni majburiy dependency qilib qo'ymang. Foydalanuvchi reactive stack da bo'lishi mumkin. Integratsiya kutubxonasini `optional` yoki `provided` qilib, mavjudligini `@ConditionalOnClass` bilan tekshirish to'g'ri yo'l. Shuningdek `@ComponentScan` ni starter ichida ishlatmang: u foydalanuvchi paketini skanerlashga urinadi va kutilmagan bean lar keltirib chiqaradi. Faqat aniq `@Bean` metodlari va `@Import`.

| Qaror | Oddiy yondashuv | Arxitektor yondashuvi |
|---|---|---|
| Starter tuzilishi | bitta jar, hammasi ichida | autoconfigure va starter alohida, dependency lar `optional` |
| Bean e'lon qilish | `@Component` va `@ComponentScan` | `@Bean` + `@ConditionalOnMissingBean`, skan yo'q |
| Yoqish/o'chirish | kod o'zgartirib o'chiriladi | `@ConditionalOnProperty` va `matchIfMissing` |
| Sozlash | statik `final` konstantalar | `@ConfigurationProperties` + metadata generator |
| Versiya boshqaruvi | har joyda qo'lda versiya | `spring-boot-dependencies` BOM + o'z BOM |
| Tartib | tasodifga tashlanadi | `@AutoConfiguration(after = ...)` aniq ko'rsatiladi |
| Tekshirish | qo'lda ilova ko'tarib sinaladi | `ApplicationContextRunner` bilan shart matritsasi |
| Monitoring | starter metrikasiz chiqadi | `MeterBinder` beriladi, prefiks `acme.payment.*` |
| Buzuvchi o'zgarish | xossa nomi jim o'zgaradi | eski nom deprecated metadata bilan 2 relizda saqlanadi |

### 16.5 Konfiguratsiya manbalari tartibi va ustunlik qoidasi

Spring Boot konfiguratsiyani `Environment` ichidagi tartiblangan `PropertySource` ro'yxatidan o'qiydi. Yuqoridagi manba pastdagini yopadi. Amalda eng ko'p kerak bo'ladigan tartib yuqoridan pastga: command line argumentlar, `SPRING_APPLICATION_JSON`, JVM system property lari (`-D`), OS environment o'zgaruvchilari, jar tashqarisidagi profil fayllari, jar tashqarisidagi `application.yaml`, jar ichidagi profil fayllari, jar ichidagi `application.yaml`, `@PropertySource`, va oxirida `SpringApplication.setDefaultProperties` bilan berilgan qiymatlar.

Bu tartibdan kelib chiqadigan amaliy qoida: Kubernetes da sirlarni environment o'zgaruvchisi sifatida bering, chunki u jar ichidagi har qanday qiymatni yopadi va image ni qayta qurishni talab qilmaydi. Relaxed binding tufayli `ACME_PAYMENT_BASE_URL` o'zgaruvchisi `acme.payment.base-url` xossasiga avtomatik tushadi.

```yaml
# application.yaml - bitta fayl, profil bo'limlari `---` bilan ajratiladi
acme:
  payment:
    base-url: https://pay.sandbox.acme.internal
    connect-timeout: 2s          # Duration tipi, 2s / 500ms / PT2S qabul qiladi
    read-timeout: 5s
    max-retries: 3
spring:
  config:
    # tashqi fayl va vault: topilmasa yiqilmasin
    import: "optional:file:/etc/acme/payment.yaml,optional:configtree:/run/secrets/"
---
spring:
  config:
    activate:
      on-profile: prod
acme:
  payment:
    base-url: https://pay.acme.com
    max-retries: 5
```

`spring.config.import` Boot 2.4 dan beri mavjud va `spring.config.location` ni ko'p holatda almashtiradi. `optional:` prefiksi fayl yo'q bo'lsa ishga tushishni to'xtatmaydi. `configtree:` esa Kubernetes Secret ni fayl sifatida mount qilganda har bir faylni xossaga aylantiradi, bu sirlarni yaml ga yozishdan xavfsizroq.

### 16.6 `@ConfigurationProperties` va validatsiya, `application.yaml` tuzilishi

`@Value` bitta-ikkita qiymat uchun yetarli, lekin to'rt-besh xossadan keyin `@ConfigurationProperties` ga o'tish kerak. Sababi: guruhlangan tipli obyekt, IDE da avtomatik to'ldirish, va eng muhimi ishga tushish paytida validatsiya. Boot 3.x da record bilan constructor binding standart holat: bir dona konstruktor bo'lsa `@ConstructorBinding` yozish shart emas, natijada immutable konfiguratsiya obyekti chiqadi.

```java
@ConfigurationProperties(prefix = "acme.payment")
@Validated
public record PaymentProperties(
        @NotBlank String merchantId,
        @NotNull URI baseUrl,
        @DefaultValue("2s") Duration connectTimeout,
        @DefaultValue("5s") Duration readTimeout,
        @Min(0) @Max(5) int maxRetries,
        @Valid Circuit circuit) {

    public record Circuit(
            @DefaultValue("50") @Min(1) @Max(100) int failureRatePercent,
            @DefaultValue("30s") Duration openStateDuration) {}
}
```

`@Validated` bo'lmasa `@NotBlank` hech narsa qilmaydi, bu juda keng tarqalgan jim xato. Validatsiya ishga tushishda bajariladi va noto'g'ri konfiguratsiya pod ni Readiness ga chiqarmaydi. Bu xohlangan xatti-harakat: noto'g'ri sozlangan to'lov servisi ishlamagani yaxshi, yarim ishlagandan ko'ra. `spring-boot-configuration-processor` ni `annotationProcessor` sifatida qo'shsangiz, `META-INF/spring-configuration-metadata.json` generatsiya bo'ladi va jamoa IDE da xossa nomlarini taklif sifatida ko'radi.

Yaml tuzilishi haqida: bitta ildiz prefiks (`acme`) ostida barcha o'z xossalaringizni saqlang, `spring.*` ichiga hech narsa qo'shmang. Bu konflikt ehtimolini nolga tushiradi va `configprops` endpoint da sizning sozlamalaringiz bir joyda ko'rinadi.

### 16.7 Profil (profile) dan to'g'ri foydalanish va uning tuzoqlari

Profil ikki xil narsa uchun ishlatiladi va faqat bittasi to'g'ri. To'g'ri ishlatish: muhitga bog'liq QIYMATLARNI almashtirish (URL, pool kattaligi, log darajasi). Noto'g'ri ishlatish: `@Profile` bilan bean larni almashtirib, muhitlar o'rtasida har xil kod yo'lini yaratish. Ikkinchi holatda prod da ishlaydigan kod hech qachon test qilinmagan bo'lib chiqadi.

`spring.profiles.active` ni `application.yaml` ichida yozish zararli odat, chunki u bilan dev profil jar ga kirib ketadi. Faqat tashqaridan bering: `SPRING_PROFILES_ACTIVE=prod`. `spring.profiles.group` bilan bir profil ostida bir nechtasini birlashtirish mumkin, masalan `prod` ichiga `prod-db` va `prod-cache` kiradi. Profilga xos faylda `spring.profiles.active` ni qayta e'lon qilish mumkin emas, Boot bunda xato bilan to'xtaydi.

| Tuzoq | Nega sodir bo'ladi | Yechim |
|---|---|---|
| `@Profile("!prod")` bilan mock to'lov gateway | prod yo'li hech qachon ishlatilmaydi | yondashuv xossaga o'tkaziladi, barcha muhitda bir kod |
| `application.yaml` da `spring.profiles.active: dev` | jar ichidagi standart dev bo'lib qoladi | faqat `SPRING_PROFILES_ACTIVE` orqali |
| Yaml ro'yxati profil bilan "birlashadi" deb o'ylash | ro'yxat merge bo'lmaydi, butunlay almashadi | to'liq ro'yxatni har profilda qayta yozish |
| `@ConfigurationProperties` validatsiyasi ishlamaydi | `@Validated` qo'yilmagan | sinfga `@Validated`, ichki obyektga `@Valid` |
| `@ConditionalOnMissingBean` tasodifiy ishlaydi | auto-config tartibi ko'rsatilmagan | `@AutoConfiguration(after = ...)` |
| Actuator barcha endpoint ni ochib yuboradi | `exposure.include: "*"` yozilgan | faqat kerakli ro'yxat, `management.server.port` alohida |
| Liveness probe DB ni tekshiradi | custom indicator liveness guruhida | DB faqat readiness guruhida bo'ladi |
| Lazy init prod da xatoni kechiktiradi | `spring.main.lazy-initialization=true` hammaga | lazy faqat lokal dev uchun |
| Boot 3 ga o'tishda xossa jim o'chadi | nomi o'zgargan, xato chiqmaydi | `spring-boot-properties-migrator` bir relizga qo'shiladi |

### 16.8 Actuator: health, metrics, env, httpexchanges va ularning xavfsizligi

Actuator ning standart holati konservativ: web orqali faqat `health` ochiq. Qolganini `management.endpoints.web.exposure.include` bilan ataylab ochish kerak. Bu ro'yxatga `*` yozish eng tez yo'l va eng xavfli qaror, chunki `env`, `configprops`, `heapdump` va `threaddump` birdan ochiladi. `heapdump` butun xotirani, ya'ni karta raqamlari va token larni diskka yozadi.

```yaml
management:
  server:
    port: 8081                 # asosiy trafikdan ajratilgan port
  endpoints:
    web:
      exposure:
        include: health,info,metrics,prometheus,loggers
  endpoint:
    health:
      show-details: when-authorized
      probes:
        enabled: true
      group:
        readiness:
          include: readinessState,db,paymentGateway
        liveness:
          include: livenessState
    env:
      show-values: never       # Boot 3.x: never | always | when-authorized
    configprops:
      show-values: never
  httpexchanges:
    recording:
      include: request-headers,response-headers,time-taken
```

`management.server.port` ni alohida qilish arxitektura darajasidagi qaror: shunda Ingress faqat 8080 ni tashqariga chiqaradi, 8081 esa cluster ichida qoladi. `httpexchanges` ishlashi uchun `HttpExchangeRepository` bean kerak, `InMemoryHttpExchangeRepository` standart holda taxminan oxirgi 100 ta so'rovni saqlaydi. Uni debug uchun yoqish mumkin, lekin `authorization` va `cookie` header larini hech qachon include ro'yxatiga qo'shmang.

Metrikalar tomonida `http.server.requests` timer eng qimmatli signal. Latency taqsimotini olish uchun `management.metrics.distribution.percentiles-histogram.http.server.requests=true` ni yoqish kerak, aks holda Prometheus da faqat o'rtacha qiymat bo'ladi. Histogram har bir tag kombinatsiyasi uchun taxminan 70 ta qo'shimcha seriya yaratadi, shuning uchun `uri` tag ida yuqori kardinallik (masalan buyurtma ID si yo'lda) bo'lmasligini tekshirish kerak.

### 16.9 Health indicator yozish va readiness va liveness farqi

Farq oddiy va qat'iy. Liveness: "bu process tirikmi, restart kerakmi". Readiness: "bu instance hozir trafik qabul qila oladimi". Shuning uchun tashqi bog'liqlik (PostgreSQL, to'lov gateway, Kafka) hech qachon liveness ga kirmasligi kerak. Agar kirsa, baza bir daqiqa sekinlashganda Kubernetes butun pod larni ketma-ket restart qiladi va vaziyat yomonlashadi.

Boot `probes.enabled: true` bilan `/actuator/health/liveness` va `/actuator/health/readiness` yo'llarini beradi. Bular `LivenessStateHealthIndicator` va `ReadinessStateHealthIndicator` ga asoslanadi, holatni esa `AvailabilityChangeEvent` orqali kod ichidan o'zgartirish mumkin. Masalan ombor qoldig'i cache i hali to'lmagan paytda instance ni readiness dan olib qo'yish mumkin.

```java
@Component("paymentGateway")   // bean nomi health kalitiga aylanadi
class PaymentGatewayHealthIndicator implements HealthIndicator {

    private final PaymentGateway gateway;

    @Override
    public Health health() {
        long start = System.nanoTime();
        try {
            gateway.ping();     // ichida read-timeout 1s bo'lishi shart
            long ms = (System.nanoTime() - start) / 1_000_000;
            return (ms < 500 ? Health.up() : Health.status("DEGRADED"))
                    .withDetail("latencyMs", ms)
                    .build();
        } catch (Exception e) {
            // xabar ichida URL va kalit bo'lmasin
            return Health.down().withDetail("reason", "gateway unreachable").build();
        }
    }
}
```

Health indicator ichida timeout bo'lmasa, health endpoint ning o'zi osilib qoladi va probe timeout ga tushadi. Qoida: har bir indicator 1 sekunddan tez javob berishi kerak, umumiy health javobi 2 sekunddan oshmasligi kerak. `management.endpoint.health.validate-group-membership` standart holda `true`, shuning uchun guruhda yo'q indicator nomini yozsangiz ishga tushishda xato chiqadi, bu foydali himoya.

### 16.10 Ishga tushish vaqti: lazy initialization, AOT va native image ta'siri

Tipik Spring Boot 3.x servis JVM da taxminan 2-5 sekundda ko'tariladi. Bu vaqtning katta qismi classpath skanerlash, annotatsiya metadata o'qish va bean yaratishga ketadi. `spring.main.lazy-initialization=true` bean larni birinchi murojaatga qoldiradi va startup ni taxminan 30-50 foizga qisqartiradi, lekin konfiguratsiya xatolari ishga tushishda emas, birinchi so'rovda chiqadi. Shu sababli bu flag lokal dev uchun, prod uchun emas.

AOT boshqa yondashuv: `spring-boot-maven-plugin` ning `process-aot` goal i build vaqtida bean definition larni Java kodiga aylantiradi va reflection ehtiyojini kamaytiradi. JVM da AOT ni `-Dspring.aot.enabled=true` bilan yoqish startup ni taxminan 20-30 foiz tezlashtiradi, lekin dinamik qarorlarni (profil bilan bean almashtirish, shartlarni runtime da hal qilish) build vaqtiga muzlatadi.

```bash
# 1) AOT bilan oddiy JVM jar: shartlar build vaqtida hisoblanadi
./mvnw -Pnative spring-boot:process-aot package
java -Dspring.aot.enabled=true -jar target/payment-service.jar

# 2) GraalVM native image: taxminan 50-120 ms startup, build 3-8 daqiqa
./mvnw -Pnative native:compile
./target/payment-service          # RSS taxminan 80-150 MB

# 3) CDS bilan o'rta yechim: kod o'zgarmaydi, startup taxminan 30% tez
java -XX:ArchiveClassesAtExit=app.jsa -Dspring.context.exit=onRefresh \
     -jar target/payment-service.jar
java -XX:SharedArchiveFile=app.jsa -jar target/payment-service.jar
```

Native image da reflection, dynamic proxy va resource yuklash build vaqtida ma'lum bo'lishi kerak. Spring buni ko'p holatda o'zi hal qiladi, qolganini `RuntimeHintsRegistrar` va `@ImportRuntimeHints` bilan qo'lda ko'rsatasiz. Arxitektorning qarori oddiy: agar servis kuniga bir marta deploy bo'lsa va uzoq ishlasa, JVM ni JIT bilan qoldirish tezroq ishlaydi (peak throughput JIT da yuqori). Agar scale-to-zero yoki tez avtoskaling kerak bo'lsa, native image yoki hech bo'lmasa CDS mantiqiy. Native ga o'tishdan oldin Testcontainers bilan native binary ustida integratsiya testlari o'tkazilishi shart, chunki klassik unit testlar native muammolarini ko'rmaydi.

### 16.11 Spring Boot 3 ga o'tish: Jakarta nomlari va konfiguratsiya o'zgarishlari

Eng katta o'zgarish kod darajasida: `javax.persistence`, `javax.servlet`, `javax.validation` paketlari `jakarta.*` ga ko'chdi. Bu Spring ning qarori emas, Java EE dan Jakarta EE ga o'tishning natijasi. Amalda bu import larni almashtirish va barcha uchinchi tomon kutubxonalarini jakarta ni qo'llab-quvvatlaydigan versiyaga ko'tarishni talab qiladi. Java baseline 17 ga ko'tarildi, Hibernate 6.x standart ORM bo'ldi.

Konfiguratsiya tomonida ko'p xossa nomi o'zgardi va eng xavfli jihati shu: eski nom jim e'tiborsiz qoldiriladi, xato chiqmaydi. Masalan `management.metrics.export.prometheus.*` endi `management.prometheus.metrics.export.*`, `spring.redis.*` endi `spring.data.redis.*`. Buni qo'lda topish mumkin emas, shuning uchun migratsiya davomida `spring-boot-properties-migrator` ni runtime dependency sifatida qo'shish kerak: u ishga tushishda eski nomlarni WARN bilan ro'yxatlaydi.

```properties
# faqat migratsiya davriga, keyin olib tashlanadi
# pom.xml: org.springframework.boot:spring-boot-properties-migrator (runtime)

# Boot 2.x -> 3.x nomlar misoli
# spring.redis.host                      -> spring.data.redis.host
# management.metrics.export.prometheus.enabled
#   -> management.prometheus.metrics.export.enabled
# spring.mvc.pathmatch.matching-strategy: endi PATH_PATTERN_PARSER standart
# trailing slash ("/orders/") avtomatik mos kelmaydi, aniq yozish kerak
```

Yana ikki nuqta e'tibor talab qiladi. Birinchisi: URL oxiridagi slash avtomatik moslashtirish olib tashlandi, ya'ni `/api/orders` va `/api/orders/` endi bir xil emas. Agar mijozlar eski formatda so'rov yuborsa, 404 oladi. Ikkinchisi: Hibernate 6 da identifikator generatsiyasi va ba'zi SQL generatsiya qoidalari o'zgardi, shu sababli migratsiyadan keyin yaratilgan SQL ni log orqali solishtirish kerak. Migratsiya tartibi amalda shunday bo'ladi: avval Boot 2.7 ga ko'tarilish, keyin dependency larni jakarta versiyalariga olib chiqish, so'ngra Boot 3.x, va har qadamda to'liq test to'plami. Shartnoma buzilmaganini tekshirish uchun testlash qo'llanmasidagi contract testing bo'limida tavsiflangan yondashuv qo'l keladi.

### 16.12 Amalda qo'llash

- [ ] Servisni `--debug` bilan bir marta ishga tushirib, `Negative matches` ro'yxatini ko'rib chiqing va kutilmagan tarzda o'chib qolgan auto-configuration borligini aniqlang.
- [ ] `management.endpoints.web.exposure.include` qiymatini tekshiring: `*` bo'lsa aniq ro'yxatga almashtiring va `management.server.port` ni 8081 ga ajratib, Ingress dan olib tashlang.
- [ ] `env` va `configprops` endpoint larida `show-values: never` o'rnatilganini tasdiqlang, `heapdump` va `threaddump` tashqariga ochiq emasligini tekshiring.
- [ ] Health guruhlarini qayta ko'rib chiqing: readiness ichida DB va tashqi gateway bo'lsin, liveness ichida faqat `livenessState` qolsin, har bir indicator ga 1 sekundlik timeout qo'shing.
- [ ] Barcha `@Value` guruhlarini bitta `@ConfigurationProperties` record ga birlashtirib, `@Validated` va `@Min`/`@NotBlank` cheklovlarini qo'shing, `spring-boot-configuration-processor` ni build ga ulang.
- [ ] `application.yaml` ichida `spring.profiles.active` yozilgan bo'lsa olib tashlang va uni faqat `SPRING_PROFILES_ACTIVE` orqali bering.
- [ ] Jamoaning umumiy kodini `acme-*-spring-boot-starter` va `acme-*-spring-boot-autoconfigure` juftligiga ajratib, `ApplicationContextRunner` bilan kamida uchta shart holatini (bean bor, bean yo'q, o'chirilgan) qamrab oling.
- [ ] Startup vaqtini o'lchang va 3 sekunddan oshsa avval CDS arxivi bilan sinab ko'ring, native image ga o'tish qarorini faqat scale-to-zero talabi bo'lganda qabul qiling.

## 17. Spring MVC va WebFlux: so'rov yo'li, thread modeli, REST dizayni (Spring MVC and WebFlux)

Web qatlami arxitektor uchun eng ko'p noto'g'ri tushunilgan joy, chunki u tashqaridan oddiy ko'rinadi: annotatsiya qo'yasan, JSON chiqadi. Haqiqatda bitta HTTP so'rov konteyner socket'idan boshlab, thread pool, filter zanjiri, `DispatcherServlet`, argument resolver, message converter va javob buferi orqali o'tadi. Shu yo'lning har bir bo'g'inida o'z limiti, o'z timeout'i va o'z xotira narxi bor. Quyida mexanikani, aniq sozlash raqamlarini va eng ko'p uchraydigan tuzoqlarni ko'rib chiqamiz.

### 17.1 So'rovning to'liq yo'li: konteyner, filter, `DispatcherServlet`, handler, converter

Tomcat'da `NioEndpoint` acceptor thread socket ulanishini qabul qiladi va uni poller'ga beradi. Poller ulanishda o'qishga tayyor ma'lumot paydo bo'lganda ishni worker thread pool'ga uzatadi. Shu nuqtadan boshlab so'rov bitta worker thread'ni egallab oladi. Keyin `FilterChain` ishga tushadi: Spring Boot'da bu odatda `CharacterEncodingFilter`, `FormContentFilter`, Micrometer'ning observation filtri, Spring Security filter zanjiri va sizning filtrlaringiz.

`DispatcherServlet` ichida tartib qat'iy: `HandlerMapping` URL va metodga qarab handler topadi (`RequestMappingHandlerMapping`), `HandlerAdapter` uni chaqiradi, argument resolver'lar `@RequestBody`, `@PathVariable`, `@RequestParam` qiymatlarini tayyorlaydi, qaytgan obyektni `HttpMessageConverter` serializatsiya qiladi. Xato chiqsa `HandlerExceptionResolver` zanjiri ishlaydi.

Muhim mexanika: `@RequestBody` uchun Jackson butun JSON'ni o'qiydi va obyekt daraxtini xotirada quradi. 5 MB JSON yuborilgan so'rov deserializatsiya paytida taxminan 15-40 MB heap talab qiladi, chunki string'lar, map'lar va boxing qo'shimcha xarajat beradi. Shuning uchun `spring.servlet.multipart.max-request-size` va body limitini ataylab qo'yish kerak, aks holda bitta mijoz 50 ta parallel so'rov bilan heap'ni to'ldiradi.

Javob tomonida ham tuzoq bor. Converter natijani to'g'ridan-to'g'ri response output stream'ga yozadi, lekin buferlash Tomcat darajasida (`server.tomcat.max-http-response-header-size` emas, balki socket buferi) sodir bo'ladi. Agar serializatsiya o'rtasida exception chiqsa, status kodi allaqachon 200 bo'lib ketgan bo'ladi va mijoz yarim JSON oladi. Bu `@Transactional` ichida lazy collection'ni serializatsiya qilishga urinishning klassik natijasi.

### 17.2 Thread modeli: har so'rovga bitta thread va uning chegarasi

Platform thread bilan servlet modeli oddiy: so'rov boshida thread beriladi, javob yozilgandan keyin qaytariladi. Blocking chaqiruv (JDBC, HTTP client, fayl) davomida thread kutadi va boshqa hech kimga xizmat qilmaydi. Shu sababli parallellik chegarasi thread pool kattaligiga teng.

Little qonuni bu yerda to'g'ridan-to'g'ri ishlaydi: kerakli thread soni taxminan RPS ni o'rtacha javob vaqtiga ko'paytirishga teng. To'lov servisi sekundda 300 so'rov qabul qilsa va o'rtacha 120 ms ishlasa, 300 × 0.12 = 36 thread yetadi. Lekin p99 latency 800 ms bo'lsa, burst paytida 240 thread kerak bo'lib qoladi. Arxitektor o'rtacha emas, tail latency bo'yicha hisoblaydi.

Ikkinchi chegara xotira. Har bir platform thread stack'i uchun default 1 MB virtual manzil ajratiladi (`-Xss`), amalda 80-200 KB tegiladi. 200 thread uchun bu taxminan 20-40 MB, bu muammo emas. Haqiqiy muammo thread'ga bog'langan obyektlar: har bir so'rovning DTO'lari, Hibernate persistence context, JDBC statement buferlari. 200 parallel so'rovda har biri 2 MB ishlatsa, 400 MB heap faqat ishlab turgan so'rovlar uchun ketadi.

Uchinchi chegara va eng xavflisi: thread pool'ning to'lib qolishi. Downstream servis sekinlashsa, barcha 200 thread shu chaqiruvda kutib turadi, keyin health endpoint ham javob bermaydi va orkestrator pod'ni o'chiradi. Shuning uchun har bir tashqi chaqiruvda timeout majburiy va bulkhead (alohida limit) kerak.

### 17.3 Tomcat sozlamalari: `max-threads`, `accept-count`, `connection-timeout` va ularning ma'nosi

Bu to'rt parametr aslida bitta navbat tizimini tasvirlaydi: OS accept queue, Tomcat ulanish limiti, worker pool, va keep-alive siyosati.

```yaml
server:
  tomcat:
    threads:
      max: 200            # bir vaqtda ishlaydigan worker thread chegarasi
      min-spare: 20       # bo'sh turadigan minimum, burst'da yaratish kechikmasligi uchun
    max-connections: 8192 # ochiq socket chegarasi, worker'dan ancha katta
    accept-count: 100     # OS backlog: ulanish kutadigan navbat uzunligi
    connection-timeout: 5s        # birinchi so'rov baytini kutish muddati
    keep-alive-timeout: 20s       # keyingi so'rovni kutish muddati
    max-keep-alive-requests: 100  # bitta ulanishdagi so'rov soni
  # so'rovni butunlay tashlab yuborish uchun emas, diagnostika uchun
  tomcat.mbeanregistry.enabled: true
```

`max-connections` (default 8192) va `threads.max` (default 200) orasidagi farq ataylab qo'yilgan: keep-alive ulanish ochiq turadi, lekin thread egallamaydi. 8192 ochiq ulanish va 200 worker bo'lsa, tizim 8000 ta bekor turgan ulanishni arzon ushlab turadi. `accept-count` (default 100) esa `max-connections` ham to'lganda OS backlog'ida kutadigan navbat. U to'lsa yangi ulanish darhol rad etiladi va mijoz "connection refused" oladi.

`connection-timeout` default qiymati 20 s va bu juda uzun. Mijoz TCP ulanishni ochib, so'rov yozmasa, 20 s davomida slot egallanadi. Ommaviy API uchun 5 s yetarli. `accept-count` ni kattalashtirish vasvasasiga tushmaslik kerak: uzun navbat latency'ni oshiradi, lekin throughput'ni oshirmaydi. To'lgan navbat o'rniga tez rad etish (fail fast) mijozga retry qilish imkonini beradi, uzoq kutish esa timeout'dan keyin ishni behuda qiladi.

`threads.max` ni 800 ga ko'tarish ham odatda xato. Agar bottleneck DB connection pool bo'lsa (masalan HikariCP 20 ta ulanish), 800 thread shunchaki 780 tasini pool navbatida kutishga majbur qiladi. Natijada latency oshadi, context switch ko'payadi va xato diagnostikasi qiyinlashadi. Qoida: worker thread soni DB pool'dan 4-10 barobar katta bo'lsin, undan ortiq emas.

### 17.4 WebFlux va event loop modeli: qachon haqiqatan foyda beradi

WebFlux Netty ustida ishlaydi va event loop thread soni CPU yadrosi soniga teng (default `max(4, yadro soni)`). Har bir so'rov thread egallamaydi, balki callback zanjiri sifatida ro'yxatga olinadi. Shuning uchun 20 000 ochiq ulanishni 8 thread bilan ushlab turish mumkin.

Foyda aniq uchta holatda keladi. Birinchisi: ko'p sonli uzoq yashaydigan ulanish (SSE, WebSocket, long polling). Ikkinchisi: servis asosan boshqa servislarga proxy bo'lsa va o'zi hisob-kitob qilmasa (API gateway, aggregator). Uchinchisi: oqim sifatida kelayotgan katta ma'lumotni backpressure bilan uzatish kerak bo'lsa.

Foyda kelmaydigan holat ham aniq: oddiy CRUD servis, JDBC bilan ishlaydi, sekundda 200 so'rov oladi. Bu yerda WebFlux faqat zarar keltiradi, chunki blocking JDBC chaqiruvi event loop thread'ini bloklaydi va butun servis to'xtaydi. `Mono.fromCallable(...).subscribeOn(Schedulers.boundedElastic())` bilan o'rab chiqish mumkin, lekin natija oddiy thread pool'ning qimmat va murakkab taqlidi bo'ladi.

Reactive stack'ning yashirin narxi: stack trace o'qilmas holga keladi, `ThreadLocal` ishlamaydi (kontekst `Context` orqali uzatiladi), debugger'da qadamlab yurish imkonsiz, va har bir yangi dasturchi uchun o'rganish vaqti haftalar bilan hisoblanadi. Arxitektor bu narxni faqat o'lchangan ehtiyoj bo'lganda to'laydi.

### 17.5 Virtual thread bilan MVC: WebFlux ga ehtiyoj qanday kamayadi

Java 21 dan boshlab virtual thread barqaror. Spring Boot'da bitta sozlama bilan yoqiladi va Tomcat worker'lari virtual thread executor'ga o'tadi.

```properties
# Java 21+ va Boot 3.2+ talab qiladi
spring.threads.virtual.enabled=true

# virtual thread yoqilganda bu limit ma'nosini yo'qotadi,
# shuning uchun chegarani boshqa joyda qo'yish kerak
server.tomcat.threads.max=200
# haqiqiy chegara endi shu: DB pool va downstream bulkhead
spring.datasource.hikari.maximum-pool-size=25
spring.datasource.hikari.connection-timeout=3000
```

Mexanika: virtual thread blocking I/O'da park bo'ladi va carrier (platform) thread'ni bo'shatadi. Shu sababli 10 000 parallel so'rovni 8 carrier thread bilan bajarish mumkin, kod esa oddiy blocking uslubda qoladi. Ya'ni WebFlux bergan scalability'ning katta qismi reactive kodsiz olinadi.

Lekin ikki muhim nuqta bor. Birinchisi: virtual thread I/O'ni arzonlashtiradi, CPU ishini emas. Hisobot generatsiyasi CPU'ga bog'liq bo'lsa, foyda nolga teng. Ikkinchisi: chegara yo'qoladi. Ilgari 200 thread tabiiy bulkhead bo'lgan, endi 10 000 virtual thread bir vaqtda DB pool'ga yopiriladi va `connection-timeout` xatolari yog'iladi. Shuning uchun virtual thread yoqilganda semaphore yoki rate limiter bilan aniq limit qo'yish majburiy bo'ladi.

Pinning masalasi: `synchronized` blok ichida blocking I/O bo'lsa, JDK 21-23 da virtual thread carrier'ga qotib qoladi. JDK 24 dan bu muammo asosan hal qilindi, lekin eski kutubxonalarda `ReentrantLock` ga o'tish hali ham to'g'ri qadam. `ThreadLocal` ishlaydi, lekin har bir virtual thread o'z nusxasini oladi, shuning uchun thread-local cache (masalan `SimpleDateFormat` pool) endi foydasiz va faqat xotira yeydi.

### 17.6 REST dizayni: resurs nomlari, HTTP metodlari, holat kodlari, versiyalash

Resurs nomi ko'plikda va ot bo'lsin: `/api/orders`, `/api/orders/{id}/payments`. Fe'l URL'da emas, HTTP metodida. Istisno: haqiqiy harakatlar uchun subresurs maqbul, masalan `POST /api/orders/{id}/cancellation`.

Status kodlarida eng ko'p xato qilinadigan joylar: 400 va 422 farqi (400 noto'g'ri formatlangan so'rov, 422 format to'g'ri lekin semantik xato), 404 va 403 farqi (resurs yo'qligini yashirish kerak bo'lsa 404), 409 (konflikt, masalan optimistic lock) va 412 (`If-Match` bajarilmadi). `POST` muvaffaqiyatli bo'lsa 201 va `Location` header qaytarilsin.

Idempotency muhim mexanika. `PUT` va `DELETE` tabiiy idempotent, `POST` emas. To'lov yaratishda mijoz `Idempotency-Key` header yuborsin, server esa shu kalitni unique index bilan saqlab, takroriy so'rovga avvalgi javobni qaytarsin. Bu retry va timeout bo'lganda ikki marta pul olishdan saqlaydi.

Versiyalash uchun amalda ishlaydigani URL prefiksi (`/api/v1/`, `/api/v2/`). Header orqali versiyalash nazariy toza, lekin cache, log va debug'da og'riq keltiradi. Qoida: yangi maydon qo'shish buzmaydigan o'zgarish, maydonni o'chirish yoki tipini o'zgartirish buzadi. Buzmaydigan o'zgarishlar uchun yangi versiya chiqarmang. Ikki versiyani bir vaqtda ushlash muddatini oldindan e'lon qiling, masalan 6 oy.

### 17.7 So'rov va javob modellari: DTO chegarasi va entity ni tashqariga chiqarmaslik

Entity'ni controller'dan qaytarish eng keng tarqalgan arxitektura xatosi. Sabablari mexanik: lazy proxy serializatsiya paytida `LazyInitializationException` beradi yoki yashirin SELECT yog'diradi, DB sxemasi o'zgarishi API contract'ini buzadi, va `password_hash` kabi maydon tasodifan tashqariga chiqadi.

```java
// Javob DTO: record yetarli, o'zgarmas va Jackson bilan ishlaydi
public record OrderResponse(
        Long id,
        String status,
        BigDecimal total,           // pul uchun hech qachon double ishlatilmaydi
        OffsetDateTime createdAt,
        List<OrderLineResponse> lines) {

    static OrderResponse from(Order order) {
        // lines allaqachon fetch qilingan bo'lishi shart,
        // shu yerda lazy yuklash bo'lsa N+1 kelib chiqadi
        return new OrderResponse(
                order.getId(),
                order.getStatus().name(),
                order.getTotal(),
                order.getCreatedAt(),
                order.getLines().stream().map(OrderLineResponse::from).toList());
    }
}
```

Mapping qayerda bo'lishi kerak? Service qatlamining chegarasida, tranzaksiya hali ochiq bo'lganda. Agar mapping controller'da bo'lsa, `@Transactional` yopilgandan keyin lazy maydonlarga tegish xatoga olib keladi. Ko'p maydonli DTO uchun MapStruct qulay, chunki u compile vaqtida kod generatsiya qiladi va reflection ishlatmaydi. Reflection'ga asoslangan mapper'lar har bir chaqiruvda taxminan 1-5 mikrosekund qo'shadi, bu 1000 obyektli javobda sezilarli bo'ladi.

Alohida so'rov DTO'si ham kerak. `OrderCreateRequest` ichida `id` va `createdAt` bo'lmasin, aks holda mijoz server boshqaradigan maydonni yuborishga harakat qiladi. Projection (interface yoki record based) read tomonida DTO'ni DB darajasida to'g'ridan-to'g'ri qurish imkonini beradi va keraksiz ustunlarni o'qishni oldini oladi.

### 17.8 Validatsiya va xato javobi formati (`ProblemDetail`, RFC 7807)

Spring Framework 6 dan `ProblemDetail` mavjud va RFC 7807 formatini beradi: `type`, `title`, `status`, `detail`, `instance`, plus qo'shimcha maydonlar. `Content-Type` esa `application/problem+json` bo'ladi.

```java
@RestControllerAdvice
class ApiExceptionHandler extends ResponseEntityExceptionHandler {

    // Bean Validation xatolarini maydon bo'yicha ro'yxatga aylantiramiz
    @Override
    protected ResponseEntity<Object> handleMethodArgumentNotValid(
            MethodArgumentNotValidException ex, HttpHeaders headers,
            HttpStatusCode status, WebRequest request) {

        ProblemDetail body = ProblemDetail.forStatus(HttpStatus.UNPROCESSABLE_ENTITY);
        body.setTitle("Validatsiya xatosi");
        body.setType(URI.create("https://api.example.com/problems/validation"));
        body.setProperty("errors", ex.getBindingResult().getFieldErrors().stream()
                .map(fe -> Map.of("field", fe.getField(), "message", fe.getDefaultMessage()))
                .toList());
        body.setProperty("traceId", MDC.get("traceId"));   // qo'llab-quvvatlash uchun
        return ResponseEntity.unprocessableEntity().body(body);
    }

    @ExceptionHandler(InsufficientBalanceException.class)
    ProblemDetail handleBalance(InsufficientBalanceException ex) {
        ProblemDetail pd = ProblemDetail.forStatusAndDetail(
                HttpStatus.CONFLICT, "Hisobdagi mablag' yetarli emas");
        pd.setProperty("accountId", ex.getAccountId());
        return pd;
    }
}
```

Mexanik detallar: `@Valid` `@RequestBody` ustida `MethodArgumentNotValidException` beradi, `@Validated` service metodida esa `ConstraintViolationException`. Ikkinchisi default holda 500 ga aylanadi, shuning uchun uni alohida ushlash kerak. `spring.mvc.problemdetails.enabled=true` qo'yilsa Spring o'zi standart xatolarni `ProblemDetail` ko'rinishida qaytaradi.

Muhim xavfsizlik qoidasi: `detail` ichiga exception message'ni to'g'ridan-to'g'ri yozmang. SQL xatosi, fayl yo'li yoki ichki sinf nomi tashqariga chiqadi. Mijozga barqaror `type` URI va inson o'qiydigan xabar bersin, texnik detal log'da `traceId` bilan qolsin.

### 17.9 Katta javoblar: sahifalash, oqim (streaming), siqish

Birinchi qoida: chegarasiz ro'yxat endpoint'i bo'lmasin. `GET /api/orders` default 20 element qaytarsin va `size` parametri uchun maksimum (masalan 200) qattiq qo'yilsin. `spring.data.web.pageable.max-page-size` shuni ta'minlaydi.

Offset pagination chuqur sahifalarda sekinlashadi, chunki PostgreSQL tashlab yuboriladigan qatorlarni ham o'qishga majbur. Keyset (cursor) pagination bu muammoni yo'q qiladi.

```sql
-- Yomon: 100 000 qatorni o'qib tashlaydi, taxminan 200-800 ms
SELECT id, created_at, total FROM orders
WHERE customer_id = $1
ORDER BY created_at DESC, id DESC
LIMIT 20 OFFSET 100000;

-- Yaxshi: index bo'yicha to'g'ridan-to'g'ri sakraydi, taxminan 1-3 ms
SELECT id, created_at, total FROM orders
WHERE customer_id = $1
  AND (created_at, id) < ($2, $3)   -- oxirgi ko'rilgan qator kursori
ORDER BY created_at DESC, id DESC
LIMIT 20;

-- Shu so'rov uchun kerak bo'ladigan index
CREATE INDEX idx_orders_cust_created ON orders (customer_id, created_at DESC, id DESC);
```

Hisobot eksporti uchun esa sahifalash ham to'g'ri emas. 2 million qatorli CSV'ni ro'yxatga yig'ib qaytarish OOM beradi. Yechim: `StreamingResponseBody` bilan qatorni o'qib darhol yozish, DB tomonida `fetchSize` qo'yish.

```java
@GetMapping(value = "/api/reports/orders.csv", produces = "text/csv")
ResponseEntity<StreamingResponseBody> export(@RequestParam LocalDate from) {
    StreamingResponseBody body = out -> {
        var writer = new BufferedWriter(new OutputStreamWriter(out, StandardCharsets.UTF_8));
        writer.write("id,created_at,total\n");
        // Stream tranzaksiya ichida ochiladi, fetchSize kursor bilan ishlashni majbur qiladi
        try (Stream<OrderRow> rows = reportService.streamOrders(from)) {
            rows.forEach(r -> writeRow(writer, r));
        }
        writer.flush();   // flush bo'lmasa oxirgi bufer yo'qoladi
    };
    return ResponseEntity.ok()
            .header("Content-Disposition", "attachment; filename=orders.csv")
            .body(body);
}
```

Siqish arzon va samarali: JSON odatda 5-10 barobar kichrayadi. Lekin kichik javoblar uchun siqish CPU'ni behuda yeydi, shuning uchun minimal hajm chegarasi bor.

```yaml
server:
  compression:
    enabled: true
    min-response-size: 2KB     # bundan kichik javob siqilmaydi
    mime-types: application/json,application/problem+json,text/csv,text/plain
  # streaming javobda async timeout ni oshirish kerak bo'ladi
spring:
  mvc:
    async:
      request-timeout: 300s
  jackson:
    default-property-inclusion: non_null   # null maydonlar javobni shishiradi
```

Streaming javobda ikki tuzoq bor. Birinchisi: javob boshlangandan keyin status kodini o'zgartirish imkonsiz, shuning uchun barcha validatsiya oqim boshlanishidan oldin bajarilsin. Ikkinchisi: tranzaksiya oqim butun davomida ochiq turadi va bu PostgreSQL'da uzun transaction, ya'ni vacuum kechikishi. Katta eksport uchun `readOnly` tranzaksiya va 5 daqiqadan oshmaydigan muddat maqbul.

### 17.10 `RestClient` va `WebClient`: timeout, connection pool, qayta urinish sozlamalari

`RestClient` (Spring Framework 6.1+) blocking, `RestTemplate` o'rnini oladi va virtual thread bilan mukammal ishlaydi. `WebClient` reactive, lekin MVC ilovasida ham ishlatiladi. Tanlov qoidasi: blocking stack'da `RestClient`, reactive stack'da `WebClient`.

Eng xavfli default: timeout yo'q. JDK'ning `HttpClient` da connect timeout o'rnatilmasa OS darajasiga tushadi, read timeout esa cheksiz bo'ladi. Bitta sekin downstream butun thread pool'ni yeyishi uchun shu yetarli.

```java
@Bean
RestClient paymentClient(RestClient.Builder builder) {
    var settings = ClientHttpRequestFactorySettings.defaults()
            .withConnectTimeout(Duration.ofSeconds(2))   // TCP + TLS uchun
            .withReadTimeout(Duration.ofSeconds(3));     // javob baytlarini kutish
    return builder
            .baseUrl("https://payments.internal")
            .requestFactory(ClientHttpRequestFactoryBuilder.jdk().build(settings))
            .defaultHeader("Accept", "application/json")
            .requestInterceptor((request, body, execution) -> {
                // trace id ni downstream'ga uzatamiz
                request.getHeaders().add("X-Trace-Id", MDC.get("traceId"));
                return execution.execute(request, body);
            })
            .build();
}
```

`WebClient` uchun reactor-netty connection pool muhim. Default `max-connections` taxminan `max(16, 2 × yadro soni)` ga teng, `pendingAcquireTimeout` esa 45 s. Bu 45 s juda uzun: so'rov pool navbatida yarim daqiqa kutib, keyin baribir xato beradi.

```java
@Bean
WebClient inventoryClient() {
    ConnectionProvider provider = ConnectionProvider.builder("inventory")
            .maxConnections(50)
            .pendingAcquireTimeout(Duration.ofSeconds(2))  // navbatda uzoq kutmaslik
            .pendingAcquireMaxCount(100)
            .maxIdleTime(Duration.ofSeconds(20))   // LB idle timeout'dan kichik bo'lsin
            .maxLifeTime(Duration.ofMinutes(5))    // DNS o'zgarishini ushlash uchun
            .evictInBackground(Duration.ofSeconds(30))
            .build();

    HttpClient httpClient = HttpClient.create(provider)
            .option(ChannelOption.CONNECT_TIMEOUT_MILLIS, 2000)
            .responseTimeout(Duration.ofSeconds(3));

    return WebClient.builder()
            .clientConnector(new ReactorClientHttpConnector(httpClient))
            .build();
}
```

Timeout budjeti hisoblanadi, taxmin qilinmaydi. Tashqi so'rovga 5 s ajratilgan bo'lsa va ichida ketma-ket ikki chaqiruv bor bo'lsa, har biriga 3 s berib bo'lmaydi. Retry ham budjetga kiradi: 3 s read timeout va 2 marta retry 9 s degani. Shuning uchun retry faqat idempotent chaqiruvda, exponential backoff va jitter bilan, umumiy deadline nazoratida qilinadi. `maxIdleTime` ni load balancer idle timeout'idan kichik qo'yish majburiy, aks holda yopilgan ulanishga yozishga urinib tasodifiy `connection reset` xatolari olinadi.

### 17.11 Filter va interceptor: qayerda kontekst (trace id, foydalanuvchi) o'rnatiladi

Farq mexanik: filter servlet darajasida ishlaydi va barcha so'rovlarni (static resurs, xato sahifasi, hatto handler topilmasa ham) ko'radi. `HandlerInterceptor` esa `DispatcherServlet` ichida, handler aniqlangandan keyin ishlaydi va `HandlerMethod` ga kirish imkoni bor.

Shuning uchun taqsimlash shunday: trace id, correlation id, request log, response header filter'da; handler haqida bilim talab qiladigan ish (ruxsat tekshirish annotatsiya bo'yicha, metrika endpoint nomi bilan) interceptor'da.

```java
@Component
@Order(Ordered.HIGHEST_PRECEDENCE + 10)   // Security filtridan oldin turishi mumkin
class TraceIdFilter extends OncePerRequestFilter {

    @Override
    protected void doFilterInternal(HttpServletRequest req, HttpServletResponse res,
                                    FilterChain chain) throws IOException, ServletException {
        String traceId = Optional.ofNullable(req.getHeader("X-Trace-Id"))
                .filter(s -> s.length() <= 64)      // tashqi qiymatni validatsiya qilamiz
                .orElseGet(() -> UUID.randomUUID().toString());
        MDC.put("traceId", traceId);
        res.setHeader("X-Trace-Id", traceId);
        try {
            chain.doFilter(req, res);
        } finally {
            MDC.clear();   // thread pool'da qaytariladi, tozalamasa kontekst oqib ketadi
        }
    }
}
```

`MDC.clear()` ni `finally` da yozmaslik eng ko'p uchraydigan xato. Platform thread pool'da thread qaytariladi va keyingi so'rov eski `traceId` bilan log yozadi. Virtual thread'da bu muammo kamayadi, chunki thread bir martalik, lekin `finally` baribir to'g'ri odat.

Ikkinchi tuzoq: `@Async` yoki `ExecutorService` ga o'tganda `MDC` va `SecurityContext` ko'chmaydi, chunki ular `ThreadLocal`. Spring'da `DelegatingSecurityContextExecutor` va `TaskDecorator` bu masalani hal qiladi. Micrometer ishlatilayotgan bo'lsa, `ObservationRegistry` kontekstni avtomatik uzatadi va qo'lda `MDC` boshqarish ehtiyoji kamayadi.

Uchinchi tuzoq: filter'da `request.getInputStream()` ni o'qish. Stream bir marta o'qiladi, keyin `@RequestBody` bo'sh qoladi. Body'ni log qilish kerak bo'lsa `ContentCachingRequestWrapper` ishlatiladi, lekin u butun body'ni xotirada saqlaydi, shuning uchun limit qo'yish shart.

| Mavzu | Oddiy yondashuv | Arxitektor yondashuvi |
|---|---|---|
| Thread pool o'lchami | `threads.max` ni 500 ga ko'tarish | Little qonuni bilan p99 bo'yicha hisoblash, DB pool'ga nisbatda 4-10x |
| Tashqi chaqiruv | default timeout bilan `RestTemplate` | connect 2 s, read 3 s, bulkhead va umumiy deadline budjeti |
| Javob modeli | entity'ni to'g'ridan-to'g'ri qaytarish | DTO/record, mapping tranzaksiya ichida, projection bilan ustun tanlash |
| Xato javobi | `Map.of("error", ex.getMessage())` | `ProblemDetail` + barqaror `type` URI + `traceId`, ichki detal log'da |
| Ro'yxat endpoint | chegarasiz `findAll()` | default 20, max 200, chuqur sahifa uchun keyset kursor |
| Katta eksport | `List` ga yig'ib JSON qaytarish | `StreamingResponseBody`, `fetchSize` bilan kursor, async timeout |
| Scalability muammosi | darhol WebFlux ga ko'chish | avval virtual thread va blocking kod, WebFlux faqat o'lchangan ehtiyojda |
| Versiyalash | har o'zgarishda `/v2` | buzmaydigan o'zgarishda versiya o'zgarmaydi, eskisi uchun muddat e'lon qilinadi |
| `POST` takrori | mijozga ishonish | `Idempotency-Key` va unique index bilan natijani saqlash |
| Trace id | controller'da log'ga yozish | filter'da `MDC`, javob header'ida va downstream header'ida uzatish |

| Tuzoq | Nima bo'ladi | Yechim |
|---|---|---|
| `MDC` tozalanmaydi | keyingi so'rov eski `traceId` bilan log yozadi | `finally` da `MDC.clear()`, yoki `TaskDecorator` |
| Serializatsiya paytida lazy fetch | yarim JSON va 200 status bilan xato | mapping'ni tranzaksiya ichida bajarish, fetch join |
| `accept-count` juda katta | latency oshadi, throughput oshmaydi | navbatni qisqa tutib tez rad etish, mijozga retry qoldirish |
| `maxIdleTime` > LB idle timeout | tasodifiy `connection reset` | pool idle vaqtini LB dan kichik qo'yish, `maxLifeTime` 5 min |
| Virtual thread + `synchronized` I/O | carrier thread pinning, throughput tushadi | `ReentrantLock` ga o'tish, JDK 24+ ga ko'tarilish |
| Filter'da body o'qish | `@RequestBody` bo'sh keladi | `ContentCachingRequestWrapper` va hajm limiti |
| Reactive'da blocking JDBC | event loop bloklanadi, butun servis to'xtaydi | blocking kodni MVC'da qoldirish yoki alohida scheduler |
| Retry budjetsiz | downstream'ga yuk ko'payadi, cascade failure | idempotent chaqiruvda, backoff + jitter, umumiy deadline |

### 17.12 Amalda qo'llash

- [ ] Har bir tashqi HTTP client uchun `connect` va `read` timeout qiymatini aniq yozib chiqing, default qolgan joy bo'lmasin.
- [ ] `threads.max` ni Little qonuni bo'yicha p99 latency asosida qayta hisoblang va DB pool o'lchami bilan nisbatini tekshiring.
- [ ] `server.tomcat.connection-timeout` ni 20 s dan 5 s ga tushirib, yuk testida rad etilgan ulanish sonini kuzatib ko'ring.
- [ ] Barcha ro'yxat endpoint'lariga default va maksimal `size` qo'ying, chuqur sahifa uchun bitta endpoint'ni keyset kursorga o'tkazing.
- [ ] Xato javoblarini `ProblemDetail` ga ko'chiring, `type` URI katalogini hujjatlashtiring va `traceId` maydonini qo'shing.
- [ ] Controller qaytaradigan tiplarni audit qiling: entity qaytaradigan joy qolmasin, test sifatida JSON sxemasini qotirib qo'yish yetarli.
- [ ] Java 21+ da `spring.threads.virtual.enabled=true` ni staging'da yoqib, DB pool timeout va bulkhead limitlarini qayta o'lchang.
- [ ] `MDC` va `SecurityContext` async chaqiruvlarda ko'chayotganini bitta integratsiya testi bilan qotirib qo'ying.

## 18. Spring Data JPA va Hibernate chuqur (Spring Data JPA and Hibernate)

Hibernate bilan ishlashdagi eng keng tarqalgan xato uni "ob'ektni jadvalga saqlaydigan kutubxona" deb tushunishdir. Aslida u tranzaksiya davomida yashaydigan holat mashinasi: o'zi ushlab turgan ob'ektlarni kuzatadi, o'zgarishlarni to'playdi va qat'iy belgilangan paytda SQL ga aylantiradi. Arxitektor uchun asosiy savol "qanday annotatsiya qo'yaman" emas, "bu kod oxirida PostgreSQL ga nechta va qanday so'rov ketadi" degan savol. Bob shu savol atrofida quriladi.

### 18.1 Persistence context: birinchi daraja kesh, dirty checking, flush tartibi

Persistence context bu `EntityManager` ichidagi identity map: kalit birlamchi kalit, qiymat managed entity. Bir tranzaksiyada bitta `id` bo'yicha ikki marta `findById` chaqirsangiz, ikkinchisi SQL yubormaydi. Bu keshni o'chirib ham, sozlab ham bo'lmaydi, u faqat session hayotiga bog'liq.

Dirty checking shu identity map ustida ishlaydi. Entity yuklanganda Hibernate uning maydonlarini alohida massivga nusxalab oladi. Flush da har bir managed entity ning joriy qiymatlari shu nusxaga maydon-maydon solishtiriladi. Demak dirty checking narxi persistence context dagi entity soniga proportsional va har flush da qaytariladi. 50 ming entity ni bitta tranzaksiyaga yuklab, ichida 1000 so'rov bajarsangiz, 50 million maydon taqqoslash olasiz.

Flush uch holatda bo'ladi: commit dan oldin, `flush()` ni qo'lda chaqirganda, va so'rovdan oldin, agar so'rov tegadigan jadvalga navbatda o'zgarish bor bo'lsa. Flush dagi SQL tartibi sizning kod tartibingizga emas, Hibernate ning action queue siga bog'liq: avval orphan removal, keyin insert, keyin update, keyin to'plam o'chirish va yangilash, eng oxirida entity delete.

```java
@Transactional
public void hisobniYopish(Long buyurtmaId) {
    Buyurtma b = buyurtmaRepo.findById(buyurtmaId).orElseThrow();
    b.setHolat(Holat.YOPILGAN);   // hali hech qanday UPDATE yo'q
    // save() shart emas: b managed, dirty checking o'zi topadi.
    // bu so'rov buyurtma jadvaliga tegadi, shuning uchun UPDATE
    // ANA SHU YERDA yuboriladi, commit da emas
    long ochiq = buyurtmaRepo.countByHolat(Holat.OCHIQ);
    log.info("qolgan ochiq buyurtma: {}", ochiq);
}
```

Shu tartib bitta klassik xatoni tug'diradi: unique constraint ostidagi qatorni o'chirib, o'rniga yangisini qo'shsangiz, avval INSERT ketadi va constraint buziladi. Yechim ikkisi orasida aniq `flush()` chaqirish yoki amalni bitta UPDATE ga aylantirish.

### 18.2 Entity holatlari: transient, managed, detached, removed va ular orasidagi o'tish

Transient: `new` qilingan, identifikatori yo'q. Managed: persistence context ichida, dirty checking ostida. Detached: ilgari managed bo'lgan, identifikatori bor, lekin o'zgarishlari kuzatilmaydi. Removed: `remove` chaqirilgan, flush da DELETE ketadi.

Eng ko'p xato detached bilan bo'ladi. Controller ga kelgan JSON dan `Tolov` yasalib `save()` chaqirilsa, Spring Data `isNew()` ni tekshiradi: identifikator bo'sh bo'lsa `persist`, aks holda `merge`. `merge` esa avval bazadan shu id ni SELECT qiladi, qiymatlarni managed nusxaga ko'chiradi va MANAGED NUSXANI qaytaradi. Siz uzatgan ob'ekt detached bo'lib qoladi.

```java
// XATO: natija tashlab yuborilgan, tolov hali ham detached
tolovRepo.save(detachedTolov);
detachedTolov.setHolat(Holat.TASDIQLANGAN); // hech qayerga yozilmaydi

// TO'G'RI: merge dan butunlay qochish, bitta SELECT va bitta UPDATE
Tolov managed = tolovRepo.findById(dto.id()).orElseThrow();
managed.applyFrom(dto);
```

`merge` ning yashirin narxi ham shu: har bir `save` uchun qo'shimcha SELECT. Mingta qatorni yangilovchi importda bu mingta keraksiz so'rov.

### 18.3 Lazy loading mexanikasi, proxy va `LazyInitializationException` sababi

Lazy bog'lanish proxy orqali ishlaydi. Hibernate bayt-kod darajasida entity sinfidan voris yasaydi, uning ichida faqat identifikator to'ldirilgan bo'ladi. Birinchi metod chaqirilganda proxy o'z session iga murojaat qilib SELECT yuboradi va o'zini to'ldiradi. To'plamlar uchun `PersistentBag` yoki `PersistentSet` xuddi shunday kechiktirilgan.

`LazyInitializationException` proxy o'z session ini topolmaganda tashlanadi: tranzaksiya yopilgan, lekin ob'ekt hali hayot va kimdir uning to'ldirilmagan qismini so'rayapti. Bu entity ni DTO ga aylantirmasdan controller ga qaytarganda yuz beradi.

Bu yerda `spring.jpa.open-in-view` haqida aniq pozitsiya kerak. Spring Boot da u sukut bo'yicha yoqilgan va session ni HTTP javob yozilib bo'lguncha ochiq ushlaydi. Xato "yo'qoladi", o'rniga ikki yomonroq narsa keladi: serializatsiya paytidagi kutilmagan SELECT lar va connection ning javob tugaguncha pool da band turishi. 10 connection li pool da bu throughput ni sezilarli pasaytiradi.

```yaml
spring:
  jpa:
    open-in-view: false   # session ni HTTP qatlamiga chiqarmaymiz
    properties:
      hibernate:
        # pagination ustida collection fetch ni jim kechirmaslik
        query.fail_on_pagination_over_collection_fetch: true
        default_batch_fetch_size: 50
        jdbc.batch_size: 50
        order_inserts: true
        order_updates: true
```

### 18.4 N+1 so'rov muammosi: topish usuli va to'rt xil yechim

N+1 ni ko'z bilan topish qiyin, kod toza ko'rinadi. Uni raqam bilan topish kerak: statistikani yoqib, bitta use case dagi so'rov sonini o'lchash. 20 buyurtmani mijozi bilan ko'rsatadigan endpoint 21 so'rov yuborsa, bu N+1.

```sql
-- bitta ro'yxat so'rovi
select b.id, b.mijoz_id, b.summa from buyurtma b where b.holat = 'OCHIQ';
-- keyin har qator uchun alohida so'rov, 20 marta
select m.id, m.nomi from mijoz m where m.id = 101;
select m.id, m.nomi from mijoz m where m.id = 102;
```

Birinchi yechim `join fetch`: bitta so'rovda hammasi. To'plam bilan ishlatganda dekart ko'paytmasi paydo bo'ladi, shuning uchun `Set` yoki `distinct` kerak. Muhimi: to'plam fetch bilan `Pageable` ni birga ishlatib bo'lmaydi, Hibernate hamma qatorni xotiraga olib, kesishni Java da bajaradi. Yuqoridagi `fail_on_pagination_over_collection_fetch` aynan shuni xatoga aylantiradi.

Ikkinchi yechim `@EntityGraph`: bir metod uchun deklarativ fetch rejasi. Uchinchi yechim `@BatchSize` yoki global `default_batch_fetch_size`: Hibernate N alohida so'rov o'rniga `where id in (?, ?, ...)` bilan guruhlaydi va 21 so'rov 2 ga tushadi. To'rtinchi va ko'pincha eng to'g'ri yechim: entity ni umuman yuklamaslik, faqat kerakli ustunlarni proyeksiya qilish.

```java
// 1) join fetch: to'plamsiz bog'lanish uchun eng sodda
@Query("select b from Buyurtma b join fetch b.mijoz where b.holat = :h")
List<Buyurtma> ochiqBuyurtmalar(@Param("h") Holat h);

// 2) entity graph: to'plam bo'lmasa pagination bilan ham xavfsiz
@EntityGraph(attributePaths = {"mijoz", "valyuta"})
Page<Buyurtma> findByHolat(Holat holat, Pageable pageable);

// 3) batch fetch: to'plamni guruhlab olish
@OneToMany(mappedBy = "buyurtma", fetch = FetchType.LAZY)
@BatchSize(size = 50)
private Set<BuyurtmaQatori> qatorlar;
```

Tanlash qoidasi: ro'yxat ekrani uchun proyeksiya, bitta ob'ektni tahrirlash uchun entity graph, oldindan bilinmaydigan navigatsiya uchun global batch fetch size.

| Tuzoq | Nega yuz beradi | Yechim |
| --- | --- | --- |
| `MultipleBagFetchException` | ikki `List` to'plam bir so'rovda fetch qilingan | to'plamlarni `Set` ga o'tkazish yoki birini batch fetch ga qoldirish |
| Noto'g'ri sahifa | collection fetch da limit xotirada qo'llanadi | sahifada faqat id larni olib, ikkinchi so'rovda fetch qilish |
| Takroriy qatorlar | `join fetch` dekart ko'paytmasi | `Set` ishlatish yoki `distinct` |
| `List` dan bitta element o'chirishda hamma qator qayta yozilishi | bag semantikasi | `Set` yoki `@OrderColumn` |
| `IDENTITY` da batch insert ishlamasligi | har insert dan keyin id o'qilishi shart | `SEQUENCE` ga o'tish |
| Importda har `save` da SELECT | detached ob'ekt uchun `merge` | yangi ob'ektlarda id ni bo'sh qoldirish |

### 18.5 Faqat kerakli ustunni olish: interfeys va record proyeksiyasi

Hisobot ekranida entity yuklash sof yo'qotish: 30 ustun, nusxa massiv va identity map yozuvini to'laysiz, ekranga 4 ustun chiqadi. Interfeys proyeksiyasi faqat getter lardan tashkil topadi va Hibernate kerakli ustunlarni tanlab oladi. Record proyeksiyasi esa DTO ni bevosita so'rov natijasi qiladi.

```java
public record BuyurtmaSatri(Long id, BigDecimal summa, String mijozNomi) {}

public interface BuyurtmaRepo extends JpaRepository<Buyurtma, Long> {

    @Query("""
           select new com.ombor.dto.BuyurtmaSatri(b.id, b.summa, b.mijoz.nomi)
           from Buyurtma b where b.holat = :h
           """)
    List<BuyurtmaSatri> satrlar(@Param("h") Holat h);

    // dinamik proyeksiya: bitta so'rov, turli shakldagi natija
    <T> List<T> findBySanaAfter(LocalDate sana, Class<T> turi);
}
```

```sql
-- natijadagi SQL aynan shunday, qo'shimcha so'rov qolmaydi
select b.id, b.summa, m.nomi
from buyurtma b join mijoz m on m.id = b.mijoz_id
where b.holat = 'OCHIQ';
```

Muhim chegara: proyeksiya faqat o'qish uchun. Natijani o'zgartirib saqlash kerak bo'lsa, entity kerak. Shuning uchun repository da ikki xil metod bo'ladi: ekran uchun proyeksiya, buyruq uchun entity.

### 18.6 `@OneToMany` to'plamlar: `List` va `Set` farqi, yangilashdagi tuzoqlar

`@OrderColumn` siz `List` bu bag: tartibsiz va takrorlanishga ruxsat beradigan to'plam. Hibernate bag dan bitta elementni o'chirishni ifodalay olmaydi, chunki qatorni aniqlovchi pozitsiya yo'q. Shu sababli butun bog'lanishni o'chirib, qolganini qayta kiritadi. 200 qatorli buyurtmadan bitta qatorni olsangiz, bazaga 1 DELETE va 199 INSERT ketadi.

```sql
-- List (bag) dan bitta qator o'chirilganda
delete from buyurtma_qatori where buyurtma_id = 42;
insert into buyurtma_qatori (buyurtma_id, mahsulot_kodi, soni) values (42, 'A-1', 3);
-- ... qolgan 198 qator qayta kiritiladi

-- Set da xuddi shu amal
delete from buyurtma_qatori where id = 7781;
```

`Set` da bu muammo yo'q, sharti `equals` va `hashCode` ni to'g'ri yozish. Ularni `id` ustiga qurish xato: yangi element hali id siz bo'lganda hashCode o'zgarib ketadi va `Set` buziladi. To'g'ri yo'l biznes kaliti yoki ilova tomonida yasalgan UUID.

Ikkinchi tuzoq: to'plamni to'liq almashtirish. `setQatorlar(yangiRoyxat)` Hibernate kuzatayotgan to'plam ob'ektini tashlab yuboradi va butun to'plam qayta yoziladi. To'g'ri usul ichini o'zgartirish, yaxshisi `addQator` va `removeQator` metodlari orqali ikki tomonni sinxron ushlash. `orphanRemoval = true` bo'lsa, to'plamdan chiqarilgan element bazadan ham o'chadi va buyurtma qatorlari uchun bu aynan kerakli xatti-harakat.

### 18.7 Identifikator strategiyalari: `IDENTITY`, `SEQUENCE` va batch insert ga ta'siri

`IDENTITY` PostgreSQL da identity ustunga tayanadi va qiymat faqat INSERT dan keyin ma'lum bo'ladi. Hibernate esa identity map ga qo'shish uchun identifikatorni darhol talab qiladi. Natijada `persist` chaqirilgan zahoti INSERT ketadi va batch yig'ish imkoniyati butunlay yo'qoladi. 10 ming qatorli import 10 ming round trip ga aylanadi, har biri taxminan 0.3 dan 1 ms bo'lsa, faqat tarmoqqa 3 dan 10 sekund ketadi.

`SEQUENCE` da Hibernate `nextval` ni oldindan so'rab, id ni INSERT dan oldin biladi. `allocationSize` bilan pooled optimizer ishlaydi: bitta `nextval` dan keyin 50 id ilova xotirasida tarqatiladi. Shart: baza sequence idagi `increment by` qiymati `allocationSize` ga teng bo'lishi kerak.

```java
@Id
@GeneratedValue(strategy = GenerationType.SEQUENCE, generator = "harakat_seq_gen")
@SequenceGenerator(name = "harakat_seq_gen",
                   sequenceName = "harakat_seq",
                   allocationSize = 50)   // sequence increment by 50 bo'lishi shart
private Long id;
```

Batch ishlashi uchun `jdbc.batch_size` dan tashqari `order_inserts` va `order_updates` ham kerak, aks holda turli entity turlari aralashganda batch uzilib ketadi. `@Version` ishlatilsa, versiyali qatorlarni batch qilish uchun `hibernate.batch_versioned_data` yoqiladi. Batch size uchun amaliy oraliq 50 dan 100 gacha, undan kattasida foyda yassilashadi.

### 18.8 Optimistik va pessimistik lock: `@Version`, `PESSIMISTIC_WRITE` qachon

`@Version` qo'shilganda Hibernate har UPDATE ga versiya shartini qo'shadi. UPDATE 0 qator o'zgartirsa, kimdir oldin ulgurgan va Hibernate `OptimisticLockException` tashlaydi, Spring uni `ObjectOptimisticLockingFailureException` ga o'raydi. Hech qanday lock olinmaydi, shuning uchun bu usul arzon va nizo kam bo'lgan joyda to'g'ri tanlov: foydalanuvchi tahrirlaydigan kartochka, profil, buyurtma sarlavhasi.

```sql
-- optimistik: versiya shart ichida, 0 qator qaytsa ilova xato tashlaydi
update buyurtma set holat = 'YOPILGAN', version = 8 where id = 42 and version = 7;

-- pessimistik: qator commit gacha band qilinadi
select qoldiq from ombor_qoldiq where mahsulot_kodi = 'A-1' for update;
```

Pessimistik lock boshqa hol uchun: qiymat o'qilgandan keyin darhol unga tayanib yoziladigan va retry qimmat joylar, ya'ni ombor qoldig'i va hisobdan pul yechish. `PESSIMISTIC_WRITE` PostgreSQL da `FOR UPDATE` ga aylanadi.

```java
@Lock(LockModeType.PESSIMISTIC_WRITE)
Optional<OmborQoldiq> findByMahsulotKodi(String kod);

// navbat shaklidagi ish: band qatorlarni butunlay chetlab o'tish
@Query(value = """
       select * from tolov_vazifa where holat = 'YANGI'
       order by id limit :n for update skip locked
       """, nativeQuery = true)
List<TolovVazifa> navbatdanOl(@Param("n") int n);
```

Pessimistik lock da ikki raqamni oldindan belgilash kerak: lock kutish vaqti va tranzaksiya uzunligi. PostgreSQL da `lock_timeout` ni tranzaksiya boshida taxminan 3 sekundga qo'yish xavfsiz amaliyot. Lock ushlab turgan tranzaksiya ichida tashqi HTTP chaqiruv qilish esa jiddiy xato: tashqi servis sekinlashsa, hamma qoldiq yangilash navbatga tizilib qoladi.

### 18.9 Hibernate statistikasi va yozilgan SQL ni ko'rish sozlamalari

`spring.jpa.show-sql=true` ni lokalda ham ishlatmaslik kerak: u System.out ga yozadi, parametrlarni ko'rsatmaydi va log tizimidan tashqarida qoladi. To'g'ri sozlama logger lar orqali.

```properties
logging.level.org.hibernate.SQL=DEBUG
# bog'langan parametrlar, Hibernate 6 da aynan shu logger
logging.level.org.hibernate.orm.jdbc.bind=TRACE
spring.jpa.properties.hibernate.generate_statistics=true
logging.level.org.hibernate.stat=DEBUG
# chegaradan sekin so'rovlarni alohida belgilash, ms
spring.jpa.properties.hibernate.session.events.log.LOG_QUERIES_SLOWER_THAN_MS=100
```

`generate_statistics` yoqilganda har session tugaganda qisqa hisobot chiqadi: nechta JDBC statement, nechta so'rov, nechta collection fetch, qancha vaqt. Shu raqam N+1 ni ob'ektiv aniqlaydi. Uni production da doimiy yoqmaslik kerak, lekin yuklama va integratsiya testlarida yoqish kerak. Eng foydali qoida: muhim use case uchun so'rov sonini test bilan qotirib qo'yish, ya'ni "buyurtma ro'yxati 3 so'rovdan oshmaydi". Buni qanday yozish testlash qo'llanmasidagi Spring slice testlari bo'limiga tegishli.

### 18.10 Spring Data metod nomlari, `@Query`, `Specification` va ularning chegarasi

Metod nomi bo'yicha so'rov sodda holat uchun ideal, lekin tez buziladi. `findByHolatAndSanaBetweenAndMijozShahriOrderBySummaDesc` kabi nom o'qilmaydi. Amaliy chegara ikki, ko'pi bilan uch shart. Undan keyin `@Query` ga o'tish kerak, chunki JPQL matni review qilinadi.

`Specification` dinamik filtr uchun: foydalanuvchi 8 filtrdan ixtiyoriy kombinatsiyani tanlasa, har biri uchun metod yozib bo'lmaydi. Narxi bor: Criteria kodi SQL dan uch barobar uzun va nima generatsiya bo'lishini ko'rish qiyin. Yana bir chegara: `Specification` va `Pageable` birga kelganda count so'rovi ham shu specification bilan quriladi, va unda fetch join xatoga olib keladi. Shuning uchun specification ichida natija turini tekshirib, count paytida fetch qo'shmaslik kerak.

Eng muhim chegara shu: JPQL ham, Criteria ham PostgreSQL ning kuchli qismini ifodalay olmaydi. Window funksiya, CTE, `distinct on`, `lateral`, `jsonb` operatorlari, to'liq matn qidirish va `insert ... on conflict` JPA modeliga sig'maydi. Bu yerda kurashish kerak emas.

| Masala | Oddiy yondashuv | Arxitektor yondashuvi |
| --- | --- | --- |
| Ro'yxat ekrani | entity yuklash, keyin DTO ga mapping | so'rovda record proyeksiyasi, entity yuklanmaydi |
| Lazy xato | `open-in-view` ni yoqib qo'yish | `open-in-view: false`, tranzaksiya ichida DTO yasash |
| N+1 | hamma bog'lanishni EAGER qilish | use case bo'yicha entity graph yoki batch fetch size |
| Ommaviy import | har qator uchun `save` | `SEQUENCE`, batch size 50, davriy `flush` va `clear` |
| Qoldiqni yechish | o'qib, hisoblab, keyin yozish | `for update` yoki bitta atomar UPDATE |
| Nizo boshqaruvi | lock umuman ishlatilmaydi | `@Version` sukut bo'yicha, `PESSIMISTIC_WRITE` faqat pul va qoldiqda |
| Hisobot | JPQL ni murakkablashtirish | `JdbcClient` va read-only tranzaksiya |
| Kesh | `@Cacheable` ni hamma joyga qo'yish | o'zgarmas ma'lumot uchun aniq region, TTL va invalidatsiya rejasi |
| Performans tekshiruvi | "sekin" degan hisga tayanish | statistikadan so'rov soni, `explain analyze` dan plan |
| Sahifalash | `offset` ni cheksiz o'stirish | katta offset da kalit bo'yicha keyset sahifalash |

### 18.11 Qachon JPA dan voz kechib `JdbcClient` yoki to'g'ridan-to'g'ri SQL yozish kerak

JPA ning kuchi domen ob'ektining hayot aylanishini boshqarishda: bitta buyurtmani yuklash, tahrirlash, saqlash. Kuchsiz joyi ommaviy o'qish va ommaviy yozish. Spring Framework 6.1 dan beri `JdbcClient` mavjud va shu bo'shliqni toza to'ldiradi: nomli parametrlar, record ga mapping.

```java
public List<KunlikTushum> kunlikTushum(LocalDate dan, LocalDate gacha) {
    // window funksiya JPQL da ifodalanmaydi, demak SQL bu yerda o'rinli
    return jdbc.sql("""
            select kun, summa, sum(summa) over (order by kun) as jamlanma
            from (select date(yaratilgan_at) kun, sum(summa) summa from tolov
                  where yaratilgan_at >= :dan and yaratilgan_at < :gacha
                  group by 1) t
            order by kun
            """)
        .param("dan", dan).param("gacha", gacha)
        .query(KunlikTushum.class).list();
}
```

Qaror mezoni sodda. Natija domen ob'ekti bo'lmasa va o'zgartirilmasa, JPA shart emas. So'rov aniq SQL konstruksiyasiga tayansa, JPA shart emas. Bir operatsiya 10 mingdan ortiq qatorga tegsa, `update ... from` yoki `insert ... on conflict` shaklidagi bitta SQL deyarli har doim entity sikldan tez. Shu paytda ikki narsa esda bo'lsin: bunday SQL persistence context ni bilmaydi, shuning uchun bir tranzaksiyada entity bilan aralashtirmaslik yaxshi, va u keshni ham chetlab o'tadi.

### 18.12 Ikkinchi daraja kesh: foydasi va xavfi

Ikkinchi daraja kesh session lar orasida yashaydi va `SessionFactory` ga tegishli. U birlamchi kalit bo'yicha entity yuklashni tezlashtiradi, yoqish uchun provider va entity da concurrency strategiyasi talab qiladi. Foydali joyi aniq: kam o'zgaradigan ma'lumot. Valyuta ro'yxati, soliq stavkasi, mahsulot kategoriyasi, mamlakat kodi. Bunday jadvallar yiliga bir necha marta o'zgaradi, ularni har so'rovda bazadan olish bekor.

Xavfi aniq. Query cache alohida mexanizm va jadvalning oxirgi o'zgarish vaqtiga tayanib bekor qilinadi, shu sababli tez o'zgaradigan jadvalda faqat xotira yeydi. Native SQL yoki JPQL `update` orqali qilingan ommaviy o'zgarish keshni bekor qilmaydi, natijada eskirgan ma'lumot qoladi. Ilova bir nechta nusxada ishlaganda mahalliy kesh nusxalari farq qiladi va foydalanuvchi so'rov qaysi nusxaga tushganiga qarab turli javob oladi.

Shuning uchun qoida: ikkinchi daraja keshni butun ilovaga yoqmaslik. Faqat sanab o'tilgan o'zgarmas entity larga, aniq TTL bilan, va o'zgarish faqat administrativ yo'l bilan bo'ladigan joyda. Qolgan holatda application darajasidagi kesh ko'proq nazorat beradi, chunki unda nima keshlangani va qachon tozalangani kodda ko'rinib turadi.

### 18.13 Amalda qo'llash

- [ ] `spring.jpa.open-in-view=false` qilib, chiqqan har bir `LazyInitializationException` ni service qatlamida proyeksiya yoki DTO bilan tuzatish.
- [ ] Eng band uchta endpoint uchun `generate_statistics` yoqib so'rov sonini o'lchash va har biriga yuqori chegarani test bilan qotirish.
- [ ] Ro'yxat va hisobot so'rovlarini record proyeksiyasiga o'tkazish, entity ni faqat yozish yo'lida qoldirish.
- [ ] `IDENTITY` ishlatayotgan entity larni topib, ommaviy yozuv bo'ladiganlarini `SEQUENCE` va `allocationSize = 50` ga ko'chirish, sequence `increment by` ni moslash.
- [ ] `jdbc.batch_size`, `order_inserts`, `order_updates` ni yoqib, import oqimida batch ishlayotganini PostgreSQL log i bo'yicha tasdiqlash.
- [ ] Pul va ombor qoldig'iga tegadigan metodlarda `@Version` yoki `PESSIMISTIC_WRITE` dan birini ongli tanlash va qarorni izoh bilan qoldirish.
- [ ] Lock ushlaydigan tranzaksiyalarda tashqi HTTP chaqiruvi yo'qligini tekshirish va `lock_timeout` ni taxminan 3 sekundga belgilash.
- [ ] Window funksiya yoki CTE talab qiladigan hisobotlarni `JdbcClient` ga chiqarib, read-only tranzaksiyada bajarish.

## 19. Spring tranzaksiyalari va ularning chegaralari (Spring Transactions)

Tranzaksiya arxitektorning qo'lidagi eng arzon va eng xavfli asbob. Arzon, chunki bitta annotatsiya yozasan. Xavfli, chunki o'sha annotatsiya connection'ni egallaydi, PostgreSQL da lock ushlaydi va snapshot muzlatadi, buning hammasi kodda ko'rinmaydi. Bu bobda `@Transactional` ning ichki mexanikasi, uning chegaralari va o'sha chegaralarni qanday joylashtirish kerakligi haqida gaplashamiz.

### 19.1 `@Transactional` qanday ishlaydi: proxy, `TransactionInterceptor`, `PlatformTransactionManager`

`@Transactional` tilning imkoniyati emas, Spring AOP ning natijasi. `@EnableTransactionManagement` (Spring Boot da `TransactionAutoConfiguration` orqali avtomatik) `BeanFactoryTransactionAttributeSourceAdvisor` ni ro'yxatga oladi. Bean yaratilayotganda `InfrastructureAdvisorAutoProxyCreator` sinfda yoki metodda tranzaksiya atributi borligini `AnnotationTransactionAttributeSource` yordamida aniqlaydi va bean o'rniga proxy qaytaradi. Interfeys bo'lsa JDK dynamic proxy, bo'lmasa CGLIB subclass.

Chaqiruv proxy ga kelganda `TransactionInterceptor` ishga tushadi. U `TransactionAttribute` ni o'qiydi, `PlatformTransactionManager` dan `getTransaction(definition)` so'raydi, maqsadli metodni chaqiradi, keyin `commit` yoki `rollback` qiladi. JPA uchun bu `JpaTransactionManager`, faqat `JdbcTemplate` uchun `DataSourceTransactionManager`. Ikkalasi ham `AbstractPlatformTransactionManager` dan keladi va connection yoki `EntityManager` ni `TransactionSynchronizationManager` ning thread-local resurs xaritasiga bog'laydi.

```java
// Spring Boot avtomatik beradi, lekin arxitektor nimani sozlashini bilishi kerak
@Configuration
@EnableTransactionManagement // Boot da default; AdviceMode.PROXY
public class TxConfig {

    @Bean
    public JpaTransactionManager transactionManager(EntityManagerFactory emf) {
        JpaTransactionManager tm = new JpaTransactionManager(emf);
        // default timeout: hech qanday @Transactional da timeout ko'rsatilmasa shu ishlaydi
        tm.setDefaultTimeout(5); // sekund
        // DataSourceTransactionManager da savepoint uchun kerak; JPA da ko'pincha qo'llanmaydi
        tm.setNestedTransactionAllowed(false);
        return tm;
    }

    @Bean
    public TransactionTemplate paymentTxTemplate(PlatformTransactionManager tm) {
        TransactionTemplate t = new TransactionTemplate(tm);
        t.setIsolationLevel(TransactionDefinition.ISOLATION_REPEATABLE_READ);
        t.setTimeout(3);
        return t;
    }
}
```

Shu mexanikadan ikki natija kelib chiqadi. Birinchi: tranzaksiya faqat proxy orqali o'tgan chaqiruvda boshlanadi. Ikkinchi: `EntityManager` thread ga bog'langan, demak boshqa thread ga o'tgan ish (masalan `CompletableFuture.supplyAsync`) tashqaridagi tranzaksiyani ko'rmaydi.

### 19.2 Propagation turlari: `REQUIRED`, `REQUIRES_NEW`, `NESTED` va amaliy farqi

`REQUIRED` default. Tranzaksiya bo'lsa unga qo'shiladi, bo'lmasa yangisini boshlaydi. "Qo'shiladi" so'zi aldaydi: ichki metodda `rollback` sodir bo'lsa, u o'z o'zini bekor qila olmaydi, faqat umumiy tranzaksiyani `rollback-only` deb belgilaydi. Tashqi metod istisnoni yutib yuborib commit qilmoqchi bo'lsa, Spring `UnexpectedRollbackException` tashlaydi. Bu eng ko'p uchraydigan "nega ma'lumot saqlanmadi" sababi.

`REQUIRES_NEW` tashqi tranzaksiyani to'xtatib (suspend qilib) butunlay yangi tranzaksiya oladi. Bu yangi connection degani: pool dan ikkinchi connection olinadi va ikkisi ham bir vaqtda band bo'ladi. Shuning uchun `REQUIRES_NEW` ni rekursiv yoki loop ichida ishlatish pool ni tugatadigan klassik xato. 20 ta connection li pool da 10 ta parallel so'rov bitta joyda `REQUIRES_NEW` qilsa, pool to'la bo'ladi va qolgan so'rovlar `HikariPool-1 - Connection is not available` bilan tushadi.

`NESTED` savepoint ishlatadi: ichki qism bekor bo'lsa faqat savepoint ga qaytadi, tashqi tranzaksiya davom etadi. Lekin bu `SavepointManager` ni talab qiladi. `DataSourceTransactionManager` da `nestedTransactionAllowed = true` bo'lsa ishlaydi, `JpaTransactionManager` da esa odatda `NestedTransactionNotSupportedException` olasan. Agar savepoint kerak bo'lsa, `JdbcTemplate` qatlamida yoki `EntityManager.unwrap(Session.class)` orqali aniq boshqarish amaliyroq.

```java
@Service
public class PaymentService {

    private final PaymentRepository payments;
    private final AuditLogService audit;

    @Transactional // REQUIRED: buyurtma va to'lov bitta atomar birlik
    public void charge(Long orderId, BigDecimal amount) {
        Payment p = payments.save(Payment.pending(orderId, amount));
        // Audit yozuvi to'lov bekor bo'lsa ham qolishi kerak: alohida tranzaksiya
        audit.record(orderId, "CHARGE_STARTED");
        gateway.authorize(p); // istisno chiqsa to'lov rollback, audit qoladi
    }
}

@Service
public class AuditLogService {
    // REQUIRES_NEW: pool dan ikkinchi connection oladi, buni hisobga ol
    @Transactional(propagation = Propagation.REQUIRES_NEW, timeout = 2)
    public void record(Long orderId, String event) {
        auditRepo.save(new AuditLog(orderId, event, Instant.now()));
    }
}
```

Amaliy qoida: `REQUIRES_NEW` ni faqat "bu yozuv asosiy ish bekor bo'lsa ham qolishi kerak" holatida ishlat. Audit, xatolar jurnali, retry hisoblagichi. Boshqa barcha holatda `REQUIRED` yetarli.

### 19.3 Isolation darajasini Spring da belgilash va PostgreSQL dagi haqiqiy xatti-harakat

`@Transactional(isolation = Isolation.REPEATABLE_READ)` yozganingda Spring `Connection.setTransactionIsolation` chaqiradi, keyin tranzaksiya oxirida eski qiymatni qaytaradi. PostgreSQL da to'rtta nomdan amalda uchtasi ishlaydi: `READ UNCOMMITTED` `READ COMMITTED` ga aylanadi, chunki PostgreSQL da dirty read umuman mavjud emas.

`READ COMMITTED` default va har bir statement o'z snapshot ini oladi. Ya'ni bitta tranzaksiya ichidagi ikkita `SELECT` boshqa natija berishi mumkin. `REPEATABLE READ` PostgreSQL da snapshot isolation sifatida amalga oshirilgan: tranzaksiya boshidagi snapshot oxirigacha saqlanadi va yozuv to'qnashuvida `40001 serialization_failure` keladi. `SERIALIZABLE` esa Serializable Snapshot Isolation ishlatadi va predicate darajasidagi anomaliyani ham tutadi, lekin ko'proq `40001` beradi.

Muhim nuqta: `40001` va `40P01` dasturchi kodida retry qilinadigan xatolar. Spring ularni `CannotAcquireLockException` yoki `ConcurrencyFailureException` ga aylantiradi. Retry esa tranzaksiya tashqarisida bo'lishi kerak, aks holda bekor qilingan tranzaksiyani qayta ishlatishga urinasan.

```sql
-- Ombor qoldig'ini tekshirish: REPEATABLE READ da bu ikki SELECT bir xil natija beradi
BEGIN ISOLATION LEVEL REPEATABLE READ;
SELECT quantity FROM stock WHERE sku = 'SKU-1001';
-- boshqa tranzaksiya shu qatorni o'zgartirib commit qildi
UPDATE stock SET quantity = quantity - 1 WHERE sku = 'SKU-1001';
-- ERROR: 40001 could not serialize access due to concurrent update
ROLLBACK;

-- READ COMMITTED da xuddi shu ishni atomar qilish yo'li: shartni SQL ga ko'chirish
UPDATE stock SET quantity = quantity - 1
 WHERE sku = 'SKU-1001' AND quantity >= 1;
-- 0 qator qaytsa qoldiq yetmagan; hech qanday race yo'q
```

Arxitektor qarori oddiy: kamayadigan resurs (ombor qoldig'i, balans, limit) uchun yuqori isolation emas, atomar `UPDATE ... WHERE` yoki `SELECT ... FOR UPDATE` ishlatiladi. `SERIALIZABLE` ni faqat murakkab invariant (masalan "bitta smenada ikki shifokor bo'lmasin") SQL ga sig'masa tanlaymiz va retry bilan birga tanlaymiz.

### 19.4 Rollback qoidasi: nega tekshiriladigan istisnoda rollback bo'lmaydi

Spring ning default qoidasi `RuleBasedTransactionAttribute` ichida: `RuntimeException` va `Error` da rollback, qolganida commit. Bu EJB dan kelgan tarixiy meros, mantiq esa shunday edi: checked exception biznes natijasining bir qismi, demak ma'lumot saqlanishi kerak. Amalda esa bu kutilmagan commit lar manbasi, chunki hech kim `IOException` dan keyin yarim yozilgan buyurtma qolishini xohlamaydi.

Yechim uchta. Birinchi: loyihada checked exception ni biznes qatlamida umuman ishlatmaslik va `RuntimeException` dan meros olgan domen istisnolarini qurish. Ikkinchi: `@Transactional(rollbackFor = Exception.class)` ni aniq yozish. Uchinchi: istisno tutilgan, lekin ish bekor bo'lishi kerak bo'lgan joyda `TransactionAspectSupport.currentTransactionStatus().setRollbackOnly()`.

```java
@Service
public class OrderService {

    // Checked istisnoda ham rollback kerak: aniq yozamiz
    @Transactional(rollbackFor = Exception.class, noRollbackFor = StockReservedException.class)
    public void place(OrderRequest req) throws InventoryUnavailableException {
        Order order = orderRepo.save(Order.from(req));
        try {
            inventory.reserve(order);
        } catch (PartialReservationException e) {
            // Yozuv qolsin, lekin tranzaksiya commit bo'lmasin degan holat:
            TransactionAspectSupport.currentTransactionStatus().setRollbackOnly();
            log.warn("Buyurtma {} qisman band qilindi, bekor qilinadi", order.getId());
        }
    }
}
```

Alohida tuzoq: ichki `REQUIRED` metod istisno tashlab, tashqi metod uni `catch` qilsa, tranzaksiya allaqachon `rollback-only`. Tashqi metod commit qilmoqchi bo'ladi va `UnexpectedRollbackException` oladi. Agar ichki qismning muvaffaqiyatsizligi kechirimli bo'lsa, u `REQUIRES_NEW` bo'lishi kerak, yoki umuman tranzaksiyadan tashqariga chiqarilishi kerak.

### 19.5 `readOnly = true` nima beradi va nima bermaydi

`readOnly = true` ning eng aniq samarasi Hibernate qatlamida: Spring `Session` ning flush mode ini `MANUAL` ga qo'yadi, natijada commit da avtomatik flush bo'lmaydi va dirty checking amalda bajarilmaydi. Katta `SELECT` lar uchun bu sezilarli yutuq: 10 000 entity o'qilgan hisobot metodida dirty check ga ketadigan vaqt va snapshot xotirasi yo'qoladi.

Nimani bermaydi: u ma'lumotni o'zgartirishdan himoya qilmaydi degan tushuncha noto'g'ri emas, lekin yarim to'g'ri. Native query yoki `JdbcTemplate` orqali `UPDATE` bajarish mumkin bo'lib qolishi mumkin, chunki JDBC connection ning `readOnly` flagi har doim DB tomoniga yetib bormaydi. Shuningdek `readOnly` o'zi bilan replika ga yo'naltirish qilmaydi. Yo'naltirishni o'zing qurasan: `AbstractRoutingDataSource` da `TransactionSynchronizationManager.isCurrentTransactionReadOnly()` ni o'qib key tanlaysan.

```java
// Read-only tranzaksiyani replika ga yo'naltirish: Spring o'zi qilmaydi
public class ReplicaRoutingDataSource extends AbstractRoutingDataSource {
    @Override
    protected Object determineCurrentLookupKey() {
        // readOnly = true bo'lsa replika, aks holda primary
        return TransactionSynchronizationManager.isCurrentTransactionReadOnly()
                ? "replica" : "primary";
    }
}
```

```properties
# Hisobot so'rovlari uchun DB tomonidan kafolat: faqat shu yerda haqiqiy himoya bor
spring.datasource.hikari.read-only=false
spring.jpa.open-in-view=false
# Har bir statement uchun qattiq chegara (PostgreSQL tomonida ishlaydi)
spring.datasource.hikari.connection-init-sql=SET statement_timeout = '5s'
spring.jpa.properties.hibernate.jdbc.batch_size=50
spring.jpa.properties.hibernate.order_inserts=true
```

Tekshirish usuli oddiy: metod ichida `SELECT current_setting('transaction_read_only')` bajar va natijani ko'r. Taxmin qilma, o'lchab ko'r.

### 19.6 Ichki metod chaqiruvi tuzog'i va undan chiqish yo'llari

Proxy faqat tashqaridan kelgan chaqiruvni ushlaydi. Shuning uchun `this.saveAudit()` ko'rinishidagi ichki chaqiruvda `@Transactional` butunlay e'tiborsiz qoladi. Xuddi shu sabab `@Async`, `@Cacheable` va `@Retryable` da ham ishlaydi. Eng yomoni, xato jim: hech qanday ogohlantirish chiqmaydi, faqat tranzaksiya yo'q.

To'rtta chiqish yo'li bor. Metodni boshqa bean ga ko'chirish eng toza yechim va men shuni tanlayman. `TransactionTemplate` orqali chegarani kodda ochish ikkinchi tanlov, u ayniqsa loop ichida yaxshi. O'ziga `@Lazy` bilan inject qilish (self-injection) ishlaydi, lekin kodni o'qiyotgan odamni chalg'itadi. `@EnableTransactionManagement(mode = AdviceMode.ASPECTJ)` proxy muammosini butunlay yo'q qiladi, lekin build ga weaving qo'shadi va kichik loyiha uchun bu juda qimmat.

```java
@Service
public class ReportService {

    private final TransactionTemplate txTemplate;

    public void rebuildDaily(LocalDate day) {
        // XATO bo'lardi: this.persistChunk(...) -> proxy chetlab o'tiladi, tranzaksiya yo'q
        for (List<Row> chunk : partition(load(day), 500)) {
            // TO'G'RI: chegara aniq va ko'rinadigan joyda
            txTemplate.executeWithoutResult(status -> persistChunk(chunk));
        }
    }

    // @Transactional bu yerda keraksiz: chegarani txTemplate boshqaradi
    private void persistChunk(List<Row> chunk) {
        jdbcTemplate.batchUpdate("INSERT INTO report_daily(...) VALUES (?,?,?)", toArgs(chunk));
    }
}
```

### 19.7 Tranzaksiya uzunligi: tashqi HTTP chaqiruvni tranzaksiya ichiga qo'ymaslik

Tranzaksiya ochilgan paytdan commit gacha bitta connection band, PostgreSQL da `xmin` ushlanib turadi va yozilgan qatorlar ustidagi row lock saqlanadi. Shuning uchun tranzaksiya uzunligi arxitektura ko'rsatkichi. OLTP yo'lida maqsad: 50 ms dan kam, 200 ms dan oshmasin. Ichida tashqi HTTP chaqiruv bo'lsa, bu raqam to'lov gateway ining javob vaqtiga bog'lanib qoladi, ya'ni taxminan 300 ms dan 10 sekundgacha.

Hisob oddiy. 20 ta connection li pool, har bir tranzaksiya 2 sekund turadi. Demak tizim sekundiga 10 ta tranzaksiyadan ko'p bajara olmaydi. Gateway sekinlashsa, pool to'ladi, keyin HTTP thread lar `Connection is not available` bilan tushadi, keyin health check ham yiqiladi. Bitta tashqi servis sekinlashuvi butun dasturni o'ldiradi. Bu bog'lanishni faqat chegarani to'g'ri qo'yish uzadi.

```java
@Service
public class CheckoutService {

    // Hech qanday @Transactional yo'q: bu orkestrator metod
    public void checkout(Long orderId) {
        // 1-qadam: qisqa tranzaksiya, holatni PENDING ga o'tkazamiz
        Payment p = txTemplate.execute(s -> payments.markPending(orderId));

        // 2-qadam: tranzaksiyadan TASHQARIDA, connection band emas
        GatewayResult result = gateway.authorize(p.getExternalId(), p.getAmount());

        // 3-qadam: yana qisqa tranzaksiya, natijani yozamiz
        txTemplate.executeWithoutResult(s -> payments.applyResult(orderId, result));
    }
}
```

Bu uch qadamli shakl "tranzaksiya ichida tashqi chaqiruv yo'q" qoidasini kodda ko'rsatadi. Ikkinchi qadam uzilib qolsa, yozuv `PENDING` holatda qoladi va reconciliation jarayoni uni gateway dan so'rab aniqlaydi. Bu yerda idempotency key va holat mashinasi kerak bo'ladi, buni dizayn patternlar hujjatidagi saga va idempotent receiver bo'limlari qoplaydi.

### 19.8 `TransactionSynchronization` va `@TransactionalEventListener` bilan commit dan keyin ish

Ko'p holatda ish commit dan keyin bajarilishi kerak: email yuborish, kesh tozalash, Kafka ga xabar qo'yish. Buni `@Transactional` metod ichida to'g'ridan to'g'ri qilsang, commit muvaffaqiyatsiz bo'lganda ham xabar ketgan bo'ladi. Spring ikki vosita beradi. Past daraja: `TransactionSynchronizationManager.registerSynchronization(new TransactionSynchronization() { ... })` va uning `afterCommit`, `afterCompletion` metodlari. Yuqori daraja: `ApplicationEventPublisher` bilan event chiqarish va `@TransactionalEventListener(phase = TransactionPhase.AFTER_COMMIT)`.

```java
@Service
public class ShipmentService {

    @Transactional
    public void confirm(Long orderId) {
        Shipment s = shipments.confirm(orderId);
        // Event tranzaksiya ichida chiqadi, listener commit dan keyin ishlaydi
        events.publishEvent(new ShipmentConfirmed(s.getId(), s.getTrackingNo()));
    }
}

@Component
public class ShipmentNotifier {

    @TransactionalEventListener(phase = TransactionPhase.AFTER_COMMIT)
    public void onConfirmed(ShipmentConfirmed e) {
        // Bu yerda yangi tranzaksiya YO'Q. DB ga yozish kerak bo'lsa aniq ochish shart.
        notifier.send(e.trackingNo());
    }

    @TransactionalEventListener(phase = TransactionPhase.AFTER_COMMIT)
    @Transactional(propagation = Propagation.REQUIRES_NEW)
    public void writeOutbox(ShipmentConfirmed e) {
        outbox.save(OutboxRecord.of(e)); // yangi tranzaksiya bilan yoziladi
    }
}
```

Ikki muhim detal. `AFTER_COMMIT` listener default holda yangi tranzaksiyada emas, shuning uchun u ichida DB ga yozish jim yo'qoladi; `REQUIRES_NEW` aniq kerak. Ikkinchi: `AFTER_COMMIT` listener istisno tashlasa, commit allaqachon bo'lgan, hech narsa qaytmaydi. Demak listener ichidagi ish o'z retry va o'z monitoringi bilan kelishi kerak.

### 19.9 Tranzaksiya va kesh, tranzaksiya va xabar yuborish nomuvofiqligi

Kesh va DB turli tizimlar, demak atomarlik yo'q. `@CacheEvict` default holda metod tugashi bilan ishlaydi, ya'ni commit dan oldin. Tranzaksiya keyin bekor bo'lsa, kesh allaqachon tozalangan va DB da eski ma'lumot. Teskari holda, kesh ga yangi qiymat yozilgan bo'lsa, DB rollback bo'lgandan keyin kesh butunlay yolg'on gapiradi. Spring da yechim `TransactionAwareCacheManagerProxy`: u yozuv va eviction ni commit gacha kutadi.

```java
@Bean
public CacheManager cacheManager(RedisConnectionFactory cf) {
    RedisCacheManager delegate = RedisCacheManager.builder(cf).build();
    // Kesh operatsiyalari faqat commit dan keyin qo'llanadi
    return new TransactionAwareCacheManagerProxy(delegate);
}
```

Xabar yuborishda ham xuddi shu nomuvofiqlik. Kafka ga `send` qilib keyin DB rollback bo'lsa, consumer mavjud bo'lmagan buyurtmani ko'radi. `AFTER_COMMIT` da yuborish bu muammoni kamaytiradi, lekin yo'q qilmaydi: commit bo'lgan, so'ng broker ga ulanish uzilgan bo'lsa xabar yo'qoladi. Yagona ishonchli yo'l xabarni DB ning o'zida, bitta tranzaksiyada jadvalga yozish va alohida jarayon bilan uzatish. Buning tafsilotlari dizayn patternlar hujjatidagi transactional outbox bo'limida. Bu bobning hissasi bitta: xabarni tranzaksiya ichida broker ga yuborish har doim xato, va bu xato yuk oshganda ko'rinadi.

### 19.10 Timeout, lock kutish vaqti va deadlock bilan uchrashish

Spring ning `@Transactional(timeout = 3)` qiymati DB tomonidan majburlanmaydi. Spring uni `ResourceHolderSupport` da deadline sifatida saqlaydi va JDBC statement larga `setQueryTimeout` qo'yish orqali qo'llaydi. Agar vaqt tranzaksiya ichidagi Java kodida ketayotgan bo'lsa yoki statement allaqachon ketgan bo'lsa, u darhol to'xtamaydi. Qattiq kafolat PostgreSQL tomonida.

Uchta parametr muhim. `statement_timeout` bitta statement ni uzadi, OLTP uchun 3 dan 10 sekund oralig'i oqilona. `lock_timeout` lock kutishni cheklaydi, 1 dan 3 sekund yaxshi boshlang'ich qiymat, u deadlock ni kutmasdan tez xato beradi. `idle_in_transaction_session_timeout` ochiq qolib ketgan tranzaksiyani o'ldiradi, 30 sekunddan 60 sekundgacha. Deadlock ni PostgreSQL `deadlock_timeout` (default 1 sekund) dan keyin aniqlaydi va qurbonlardan birini `40P01` bilan uzadi.

```sql
-- Hisobot va batch roli uchun alohida chegaralar
ALTER ROLE report_user SET statement_timeout = '60s';
ALTER ROLE app_user   SET statement_timeout = '5s';
ALTER ROLE app_user   SET lock_timeout = '2s';
ALTER ROLE app_user   SET idle_in_transaction_session_timeout = '30s';

-- Kim kimni kutayotganini ko'rish: deadlock tahlilining birinchi qadami
SELECT a.pid, a.state, a.wait_event_type, a.wait_event,
       now() - a.xact_start AS tx_age, left(a.query, 60) AS q
  FROM pg_stat_activity a
 WHERE a.datname = current_database() AND a.xact_start IS NOT NULL
 ORDER BY tx_age DESC LIMIT 10;
```

Deadlock ning amaliy sababi deyarli har doim bitta: lock lar turli tartibda olinadi. Buyurtma qatorlarini `id` bo'yicha tartiblab yangilash, ya'ni `ORDER BY id FOR UPDATE`, deadlock ning katta qismini yo'q qiladi. Navbat jadvallarida `FOR UPDATE SKIP LOCKED` ishlatish esa kutishning o'zini yo'q qiladi.

| Tuzoq | Nima bo'ladi | Yechim |
| --- | --- | --- |
| Ichki `this.method()` chaqiruvi | Tranzaksiya jim ochilmaydi | Alohida bean yoki `TransactionTemplate` |
| Tashqi HTTP tranzaksiya ichida | Pool tugaydi, kaskad nosozlik | Chegarani uch qadamga bo'lish |
| Checked istisno | Kutilmagan commit, yarim ma'lumot | `rollbackFor = Exception.class` |
| Ichki `REQUIRED` da istisno tutildi | `UnexpectedRollbackException` | Ichki qismni `REQUIRES_NEW` qilish |
| `REQUIRES_NEW` loop ichida | Har iteratsiyada yangi connection | Chegarani loop tashqarisiga chiqarish |
| Kesh commit dan oldin tozalanadi | Kesh va DB mos emas | `TransactionAwareCacheManagerProxy` |
| `AFTER_COMMIT` da DB ga yozish | Yozuv jim yo'qoladi | Listener ga `REQUIRES_NEW` qo'shish |
| `@Transactional` + yangi thread | Tranzaksiya kontekst ko'chmaydi | Chegarani thread ichida ochish |
| Bitta ulkan batch tranzaksiya | WAL o'sadi, lock uzoq ushlanadi | 500-1000 qatorli chunk lar |
| `timeout` faqat Spring da | Statement DB da davom etadi | `statement_timeout`, `lock_timeout` |

### 19.11 Dasturiy tranzaksiya: `TransactionTemplate` qachon aniqroq

`@Transactional` deklarativ va shuning uchun ko'rinmas. `TransactionTemplate` esa chegarani kodda ko'rsatadi. Uni to'rt holatda tanlaymiz. Birinchi: bitta metod ichida bir nechta mustaqil tranzaksiya kerak bo'lganda, masalan chunk lar bo'yicha yurganda. Ikkinchi: tranzaksiya chegarasi shartga bog'liq bo'lganda. Uchinchi: retry mantig'i tranzaksiyani to'liq qamrab olishi kerak bo'lganda. To'rtinchi: proxy muammosidan qochish kerak bo'lganda.

```java
@Service
public class StockAdjuster {

    private final TransactionTemplate tx;

    // Serialization xatosida retry: tranzaksiya har urinishda qaytadan ochiladi
    public void adjust(String sku, int delta) {
        for (int attempt = 1; attempt <= 3; attempt++) {
            try {
                tx.executeWithoutResult(s -> stockRepo.applyDelta(sku, delta));
                return;
            } catch (ConcurrencyFailureException e) { // 40001 yoki 40P01
                // Taxminan 50 ms dan boshlab eksponensial kutish
                sleepQuietly(50L * attempt);
            }
        }
        throw new StockAdjustmentFailedException(sku);
    }
}
```

E'tibor ber: `@Transactional` va `@Retryable` ni bitta metodga qo'yish ishlamaydi, chunki retry tranzaksiya ichida qoladi va bekor qilingan tranzaksiyani qayta ishlatadi. Tartib muhim: retry tashqarida, tranzaksiya ichkarida.

### 19.12 Katta batch operatsiyalarda tranzaksiya chegarasini tanlash

Million qatorlik hisobotni bitta tranzaksiyada yozish bir necha narsani buzadi. WAL o'sadi, autovacuum eski versiyalarni tozalay olmaydi, connection soatlab band bo'ladi, va xato chiqsa butun ish nolga qaytadi. To'g'ri shakl: chunk lar, har biri o'z tranzaksiyasida, va qayerga yetganini saqlab turadigan checkpoint. 500 dan 1000 qatorgacha chunk ko'pchilik holatda yaxshi muvozanat beradi.

JPA bilan batch yozishda `EntityManager` ni vaqti-vaqti bilan `flush()` va `clear()` qilish shart, aks holda persistence context o'sib xotirani yeydi. Agar entity hayotiy sikli kerak bo'lmasa, Hibernate ning `StatelessSession` i yoki to'g'ridan to'g'ri `JdbcTemplate.batchUpdate` ancha tezroq: taxminan 3 dan 10 barobargacha.

```java
@Service
public class InvoiceImporter {

    @PersistenceContext private EntityManager em;
    private final TransactionTemplate tx;

    public void importAll(Iterator<InvoiceRow> rows) {
        List<InvoiceRow> chunk = new ArrayList<>(500);
        while (rows.hasNext()) {
            chunk.add(rows.next());
            if (chunk.size() == 500) { flushChunk(List.copyOf(chunk)); chunk.clear(); }
        }
        if (!chunk.isEmpty()) flushChunk(chunk);
    }

    private void flushChunk(List<InvoiceRow> chunk) {
        tx.executeWithoutResult(s -> {
            for (InvoiceRow r : chunk) em.persist(Invoice.from(r));
            em.flush();  // SQL ni DB ga yuboramiz
            em.clear();  // persistence context ni bo'shatamiz, xotira o'smaydi
        });
    }
}
```

| Savol | Oddiy yondashuv | Arxitektor yondashuvi |
| --- | --- | --- |
| Chegara qayerda | Service ning har metodida `@Transactional` | Chegara biznes operatsiyasi bo'yicha, orkestrator tranzaksiyasiz |
| Tashqi chaqiruv | Tranzaksiya ichida qulay bo'lgani uchun | Tranzaksiyadan tashqarida, holat mashinasi bilan |
| Istisno siyosati | Default qoldiriladi | `rollbackFor` aniq, domen istisnolari runtime |
| Isolation | Muammo chiqsa `SERIALIZABLE` ga ko'tariladi | `READ COMMITTED` + atomar `UPDATE ... WHERE` |
| Timeout | `@Transactional(timeout = ...)` yetarli deb o'ylanadi | DB rolida `statement_timeout`, `lock_timeout` |
| Commit dan keyingi ish | Metod oxirida darhol bajariladi | `AFTER_COMMIT` listener yoki outbox jadvali |
| Kesh | `@CacheEvict` ga ishoniladi | Tranzaksiyaga bog'langan cache manager |
| Batch | Bitta katta tranzaksiya | 500-1000 qatorli chunk va checkpoint |
| Retry | `@Retryable` tranzaksiya ichida | Retry tashqarida, `40001` ga aniq ishlov |
| Nazorat | Xato chiqsa log qaraladi | Tranzaksiya davomiyligi metrikasi va uzoq tranzaksiya alerti |

Testlashda arxitektor uchta narsani tekshiradi: rollback haqiqatan sodir bo'ladimi, `AFTER_COMMIT` listener chaqiriladimi, va parallel ikki tranzaksiya kutilgan natija beradimi. Buning texnikasi testlash qo'llanmasidagi tranzaksiya testlari bo'limida.

### 19.13 Amalda qo'llash

- [ ] Loyihadagi barcha `@Transactional` metodlarni ro'yxatla va ichida tashqi HTTP yoki broker chaqiruvi borlarini ajratib, uch qadamli shaklga ko'chir.
- [ ] `rollbackFor = Exception.class` siyosatini kelishib ol yoki biznes istisnolarini `RuntimeException` dan meros qilib qayta qur.
- [ ] `app_user` va `report_user` rollariga alohida `statement_timeout`, `lock_timeout` va `idle_in_transaction_session_timeout` qiymatlarini qo'y.
- [ ] `pg_stat_activity` asosida 5 sekunddan uzoq ochiq tranzaksiyalar uchun alert yarat va bir hafta kuzat.
- [ ] `CacheManager` ni `TransactionAwareCacheManagerProxy` ga o'ra va kesh bilan DB nomuvofiqligini qayta tekshir.
- [ ] Broker ga tranzaksiya ichida yuborilayotgan har bir xabarni outbox jadvaliga ko'chirish rejasini tuz.
- [ ] Barcha batch va import joblarini 500-1000 qatorli chunk tranzaksiyalariga bo'lib, qayerga yetganini saqlaydigan checkpoint qo'sh.
- [ ] `40001` va `40P01` xatolari uchun tranzaksiyadan tashqaridagi retry ni `TransactionTemplate` bilan joylashtir va urinishlar sonini metrika sifatida chiqar.

## 20. Spring Security: filter chain, OAuth2, JWT (Spring Security)

Spring Security ko'pchilik uchun "sehrli qora quti" bo'lib qoladi: konfiguratsiya ishlaydi, lekin nega ishlaydi degan savolga javob yo'q. Aslida u oddiy servlet filter zanjiri ustiga qurilgan, va deyarli har bir xatolik shu zanjirdagi tartib, SecurityContext ning umri yoki token tekshiruvining to'liq bo'lmagani bilan izohlanadi. Bu bobda to'lov va buyurtma servislari misolida mexanikaga qaraymiz: so'rov qaysi filtrdan o'tadi, JWT qanday tekshiriladi, va arxitektor qayerda qaror qabul qiladi.

### 20.1 `SecurityFilterChain` tuzilishi va filtrlar tartibi

Spring Boot servlet konteynerga bitta `DelegatingFilterProxy` ni ro'yxatdan o'tkazadi, u `springSecurityFilterChain` nomli beanga, ya'ni `FilterChainProxy` ga delegat qiladi. `FilterChainProxy` ichida `SecurityFilterChain` beanlar ro'yxati bor. Har bir so'rov uchun u ro'yxatni yuqoridan pastga aylanib chiqadi va BIRINCHI mos kelgan zanjirni ishlatadi, qolganlarini umuman ko'rmaydi. Shuning uchun `@Order` va `securityMatcher` qiymatlari funksional emas, xavfsizlik qarori hisoblanadi.

Bitta zanjir ichidagi filtrlar tartibi qattiq belgilangan. Amalda muhim ketma-ketlik: `SecurityContextHolderFilter` (kontekstni o'qiydi), `HeaderWriterFilter`, `CorsFilter`, `CsrfFilter`, `LogoutFilter`, keyin autentifikatsiya filtrlari (`BearerTokenAuthenticationFilter`, `UsernamePasswordAuthenticationFilter`, `BasicAuthenticationFilter`), so'ng `AnonymousAuthenticationFilter`, `ExceptionTranslationFilter` va eng oxirida `AuthorizationFilter`. Ikki xulosa chiqadi. Birinchi: CORS preflight CSRF dan oldin ishlanadi, shuning uchun `OPTIONS` so'rovi token talab qilmaydi. Ikkinchi: avtorizatsiya qarori zanjirning OXIRIDA chiqadi, ya'ni undan oldin turgan filtrlar allaqachon ishlab bo'lgan va ular ichida qilingan I/O (masalan foydalanuvchini bazadan o'qish) hali ruxsat tekshirilmagan holda bajarilgan.

`ExceptionTranslationFilter` `AuthorizationFilter` dan oldin turadi, chunki u pastdan ko'tarilgan `AccessDeniedException` ni tutib 401 yoki 403 ga aylantiradi. Agar sizning `@RestControllerAdvice` ingiz 403 ni ushlamayotgan bo'lsa, sabab shu: exception controller ga yetib bormaydi, filtr darajasida hal bo'ladi.

```java
// Ikkita alohida zanjir: API uchun stateless, admin UI uchun sessiyali.
@Bean
@Order(1)
SecurityFilterChain apiChain(HttpSecurity http) throws Exception {
    return http
        .securityMatcher("/api/**")                 // faqat shu prefiks
        .csrf(csrf -> csrf.disable())               // stateless API, cookie ishlatilmaydi
        .sessionManagement(s -> s.sessionCreationPolicy(SessionCreationPolicy.STATELESS))
        .authorizeHttpRequests(a -> a
            .requestMatchers(HttpMethod.GET, "/api/payments/**").hasAuthority("SCOPE_payments.read")
            .requestMatchers(HttpMethod.POST, "/api/payments/**").hasAuthority("SCOPE_payments.write")
            .anyRequest().authenticated())          // oxirgi qoida har doim yopiq
        .oauth2ResourceServer(o -> o.jwt(Customizer.withDefaults()))
        .build();
}

@Bean
@Order(2)
SecurityFilterChain adminChain(HttpSecurity http) throws Exception {
    return http
        .authorizeHttpRequests(a -> a
            .requestMatchers("/login", "/css/**").permitAll()
            .anyRequest().hasRole("ADMIN"))
        .formLogin(Customizer.withDefaults())
        .build();
}
```

### 20.2 Autentifikatsiya va avtorizatsiya: `Authentication`, `SecurityContext`, `GrantedAuthority`

`Authentication` uchta narsani saqlaydi: `getPrincipal()` (kim), `getCredentials()` (nima bilan isbotlandi) va `getAuthorities()` (nimaga haqli). JWT resource server holatida principal `Jwt` obyekti bo'ladi, authority lar esa `scope` yoki `scp` claim idan `JwtGrantedAuthoritiesConverter` tomonidan `SCOPE_` prefiksi bilan yasaladi. Bu yerda birinchi tuzoq: `hasRole("ADMIN")` avtomatik `ROLE_ADMIN` authority ini qidiradi, `hasAuthority("ADMIN")` esa aynan `ADMIN` ni. JWT dagi rollar odatda `realm_access.roles` yoki `roles` claim ida keladi va `ROLE_` prefiksi yo'q, shuning uchun `hasRole` jim turib ishlamaydi.

`SecurityContextHolder` ichida `ThreadLocal` turadi. Demak kontekst so'rovni ishlayotgan thread ga bog'langan. `@Async` metod yoki qo'lda yaratilgan `ExecutorService` ichida kontekst bo'lmaydi, va `@PreAuthorize` u yerda "anonymous" ni ko'radi. Yechim: executor ni `DelegatingSecurityContextExecutorService` bilan o'rash, yoki `SecurityContextHolder.setStrategyName(MODE_INHERITABLETHREADLOCAL)` (lekin pool da qayta ishlatilgan thread da eski kontekst qolib ketishi mumkin, bu xavfli).

```java
// Keycloak uslubidagi rollarni ROLE_ prefiksi bilan authority ga aylantirish.
@Bean
JwtAuthenticationConverter jwtAuthenticationConverter() {
    JwtGrantedAuthoritiesConverter scopes = new JwtGrantedAuthoritiesConverter();
    scopes.setAuthorityPrefix("SCOPE_");
    scopes.setAuthoritiesClaimName("scope");

    JwtAuthenticationConverter converter = new JwtAuthenticationConverter();
    converter.setJwtGrantedAuthoritiesConverter(jwt -> {
        Collection<GrantedAuthority> all = new ArrayList<>(scopes.convert(jwt));
        Map<String, Object> realm = jwt.getClaimAsMap("realm_access");
        if (realm != null && realm.get("roles") instanceof Collection<?> roles) {
            roles.forEach(r -> all.add(new SimpleGrantedAuthority("ROLE_" + r)));
        }
        return all;
    });
    // principal nomi sub emas, preferred_username bo'lsin: audit log uchun qulay
    converter.setPrincipalClaimName("preferred_username");
    return converter;
}
```

### 20.3 Spring Security 6 konfiguratsiyasi: lambda uslubi va eski uslubdan farqi

Spring Security 6 da `WebSecurityConfigurerAdapter` butunlay olib tashlangan, konfiguratsiya faqat `SecurityFilterChain` bean orqali yoziladi. `antMatchers` va `mvcMatchers` o'rniga bitta `requestMatchers` qolgan. `authorizeRequests` o'rniga `authorizeHttpRequests`, u ichkarida `AuthorizationManager` ishlatadi va eski `FilterSecurityInterceptor` emas, `AuthorizationFilter` bilan ishlaydi. Zanjirni yozishda `and()` deprecated, 7.x da esa lambda bo'lmagan uslub umuman yo'q.

Eng ko'p yo'qotish keltiradigan o'zgarish ko'rinmaydigan joyda: `SecurityContextPersistenceFilter` o'rniga `SecurityContextHolderFilter` keldi. Eski filtr har so'rov oxirida kontekstni sessiyaga AVTOMATIK saqlar edi, yangisi saqlamaydi. Agar siz o'z filtringizda `SecurityContextHolder.getContext().setAuthentication(...)` qilib qo'ysangiz, Spring Security 6 da bu sessiyada qolmaydi va keyingi so'rov yana anonim bo'ladi. To'g'ri yo'li: `SecurityContextRepository` ga ochiq yozish.

```java
// Spring Security 6: kontekstni sessiyaga saqlash endi QO'LDA bo'ladi.
public class OtpVerificationFilter extends OncePerRequestFilter {

    private final SecurityContextRepository repository =
            new HttpSessionSecurityContextRepository();

    @Override
    protected void doFilterInternal(HttpServletRequest req, HttpServletResponse res,
                                    FilterChain chain) throws ServletException, IOException {
        Authentication auth = verifyOtp(req);          // ikkinchi faktor tekshirildi
        if (auth != null) {
            SecurityContext ctx = SecurityContextHolder.createEmptyContext();
            ctx.setAuthentication(auth);
            SecurityContextHolder.setContext(ctx);
            repository.saveContext(ctx, req, res);     // bu qator bo'lmasa kontekst yo'qoladi
        }
        chain.doFilter(req, res);
    }
}
```

### 20.4 Sessiya va token: qachon qaysi biri mantiqli

Sessiya serverda holat saqlaydi, demak logout va bekor qilish darhol ishlaydi, lekin horizontal skalalashda yopishqoq (sticky) sessiya yoki Spring Session orqali Redis/JDBC ga ko'chirish kerak bo'ladi. Token, xususan JWT, holatsiz: tekshirish uchun bazaga borish shart emas, lekin chiqarilgan tokenni muddatidan oldin to'xtatish deyarli imkonsiz. Qaror oddiy mezonga tayanadi: agar bir brauzer ichida ishlaydigan ichki admin paneli bo'lsa, sessiya arzonroq va xavfsizroq. Agar mobil ilova, SPA va servis orasidagi chaqiruvlar bo'lsa, token kerak.

Amalda eng barqaror kombinatsiya: brauzer uchun `HttpOnly`, `Secure`, `SameSite=Lax` cookie dagi sessiya yoki opaque token, servislar orasida esa JWT. Oraliq variant: BFF (backend for frontend) sessiyani ushlab turadi va downstream ga JWT uzatadi, shunda JavaScript tokenni hech qachon ko'rmaydi. Sessiya hajmi uchun raqam: bitta oddiy autentifikatsiyalangan sessiya taxminan 2 dan 10 KB gacha joy oladi, 50 ming parallel foydalanuvchi Redis da taxminan 100 dan 500 MB gacha degani.

### 20.5 OAuth2 rollari: resource server, client, authorization server

Uchta rol uchta mutlaqo boshqa starter va boshqa mas'uliyat. Resource server kiruvchi tokenni TEKSHIRADI va hech qachon chiqarmaydi: `spring-boot-starter-oauth2-resource-server`. Client foydalanuvchi nomidan token OLADI va downstream chaqiruvga qo'yadi: `spring-boot-starter-oauth2-client`, ichida `OAuth2AuthorizedClientManager`. Authorization server tokenni CHIQARADI: alohida `spring-authorization-server` proyekti, va uni o'z qo'lingiz bilan yozishga urinish deyarli har doim xato qaror.

Arxitektor eng ko'p xato qiladigan joy: buyurtma servisi ham API ni himoyalaydi, ham to'lov servisiga chaqiruv qiladi. Bu bitta ilovada resource server va client rollarining birgaligi. Ikkisi bir zanjirda yashashi mumkin, lekin token olish uchun `client_credentials` grant kerak, foydalanuvchi tokenini shunchaki uzatish (token passthrough) esa audience ni buzadi.

```yaml
# Buyurtma servisi: ham resource server (kiruvchi), ham client (chiquvchi).
spring:
  security:
    oauth2:
      resourceserver:
        jwt:
          issuer-uri: https://id.example.com/realms/orders
          # jwk-set-uri ni ko'rsatmasak, issuer metadata dan topiladi
          audiences: orders-api          # aud tekshiruvi YOQILADI
      client:
        registration:
          payments:
            provider: internal-idp
            client-id: orders-service
            client-secret: ${ORDERS_CLIENT_SECRET}
            authorization-grant-type: client_credentials
            scope: payments.write
        provider:
          internal-idp:
            token-uri: https://id.example.com/realms/orders/protocol/openid-connect/token
```

### 20.6 JWT ni tekshirish: imzo, `iss`, `aud`, `exp`, kalit aylanishi (JWKS)

`NimbusJwtDecoder` ishi ikki qadamdan iborat: avval imzoni tekshiradi, keyin `OAuth2TokenValidator` zanjirini ishlatadi. `JwtDecoders.fromIssuerLocation(...)` ishlatilganda standart validator `JwtTimestampValidator` (`exp` va `nbf`, standart clock skew taxminan 60 sekund) va `JwtIssuerValidator` dan iborat. Diqqat qiling: `aud` AVTOMATIK tekshirilmaydi. Agar siz uni qo'shmasangiz, bitta IdP dan olingan va boshqa servis uchun chiqarilgan token sizning API ga ham kiradi. Bu real audit topilmasi, nafaqat nazariya.

Kalit aylanishi (rotation) JWKS orqali ishlaydi. Decoder `jwk-set-uri` ni o'qiydi va natijani cache qiladi (Nimbus da standart TTL taxminan 5 daqiqa, oldindan yangilash bilan). Noma'lum `kid` kelganda JWKS qayta o'qiladi, lekin bu masofaviy HTTP chaqiruv: IdP javob bermasa, butun API 401 qaytara boshlaydi. Shuning uchun JWKS endpoint ga timeout (connect taxminan 2 sekund, read taxminan 3 sekund) va retry qo'yish kerak, hamda IdP ni mavjudlik nuqtai nazaridan kritik bog'liqlik deb hisoblash kerak.

```java
// aud va iss ni ochiq tekshirish, qo'shimcha claim bilan.
@Bean
JwtDecoder jwtDecoder(@Value("${idp.issuer}") String issuer) {
    NimbusJwtDecoder decoder = JwtDecoders.fromIssuerLocation(issuer);

    OAuth2TokenValidator<Jwt> audience = new JwtClaimValidator<List<String>>(
            JwtClaimNames.AUD,
            aud -> aud != null && aud.contains("payments-api"));

    // to'lov servisi faqat kuchli autentifikatsiyadan o'tgan tokenni qabul qiladi
    OAuth2TokenValidator<Jwt> acr = new JwtClaimValidator<String>(
            "acr", v -> "mfa".equals(v));

    decoder.setJwtValidator(new DelegatingOAuth2TokenValidator<>(
            JwtValidators.createDefaultWithIssuer(issuer), audience, acr));
    return decoder;
}
```

| Tuzoq | Nima sodir bo'ladi | Yechim |
|---|---|---|
| `aud` tekshirilmagan | Boshqa servis uchun chiqarilgan token qabul qilinadi | `audiences` property yoki `JwtClaimValidator` |
| `alg: none` yoki tokenni qo'lda parse qilish | Imzosiz token ishonchli deb qabul qilinadi | Faqat `JwtDecoder`, hech qachon qo'lda base64 decode emas |
| JWKS cache ga timeout yo'q | IdP sekinlashsa butun API bloklanadi | Connect/read timeout va circuit breaker |
| `exp` ga ortiqcha clock skew | Muddati o'tgan token yana ishlaydi | Skew ni taxminan 30 sekundda ushlab turish, NTP sozlash |
| Scope va rol aralashtirilgan | `hasRole` jim turib ishlamaydi | Authority prefikslarini bitta konvensiyaga keltirish |
| Har zanjirda alohida `JwtDecoder` | Validator qoidalari bo'linib ketadi | Bitta `JwtDecoder` bean, zanjirlarga inject qilish |
| Token ichida ko'p ma'lumot | Header 8 KB limitiga uriladi, proxy 431 qaytaradi | Faqat `sub`, `scope`, `tenant` kabi minimal claim lar |

### 20.7 Token muddati, yangilash (refresh) va bekor qilish muammosi

JWT ni bekor qilish mumkin emas, bu uning dizayni. Demak qaror savol qo'yilishi bilan boshlanadi: "foydalanuvchi huquqi olingandan keyin qancha vaqt eski huquq bilan ishlashi mumkin?" Javob access token TTL ini belgilaydi. Ichki servislar uchun taxminan 5 dan 15 daqiqa, to'lov yoki admin amallari uchun taxminan 2 dan 5 daqiqa oqilona. Refresh token uzoqroq yashaydi (taxminan 8 soatdan 30 kungacha) va u IdP tomonida saqlanadi, demak uni bekor qilish mumkin.

Darhol bekor qilish kerak bo'lsa uch yo'l bor. Birinchi: opaque token va `OpaqueTokenIntrospector` (RFC 7662), har so'rov IdP ga boradi, latency taxminan 5 dan 30 ms oshadi, lekin introspection natijasini 10 dan 30 sekundga cache qilish kelishuvni yumshatadi. Ikkinchi: `jti` bo'yicha denylist, Redis da token TTL muddatiga teng yashaydi, xotira kichik. Uchinchi: foydalanuvchi uchun `tokensValidAfter` vaqt belgisi, token `iat` undan oldin bo'lsa rad etiladi, bu "barcha qurilmalardan chiqish" funksiyasiga aynan to'g'ri keladi.

### 20.8 Metod darajasidagi xavfsizlik: `@PreAuthorize` va uning proxy chegarasi

`@EnableMethodSecurity` AOP proxy orqali ishlaydi. Shundan kelib chiqadigan chegaralar aniq. Birinchi: o'z-o'ziga chaqiruv (self-invocation) tekshiruvdan o'tmaydi, chunki chaqiruv proxy dan emas, `this` dan ketadi. Ikkinchi: `private` va `final` metod JDK dinamik proxy yoki CGLIB da ushlanmaydi. Uchinchi: faqat Spring bean ichidagi metodlar himoyalanadi, `new` bilan yaratilgan obyekt ustida annotatsiya hech narsa qilmaydi.

Tartib ham muhim. Metod xavfsizligi advice i tranzaksiya advice idan oldin ishlashi kerak, aks holda ruxsatsiz chaqiruv uchun ham tranzaksiya ochiladi. Standart tartibda shunday, lekin o'z `@Aspect` ingizga `@Order` qo'yganda buzilishi mumkin. `@PostAuthorize` esa alohida tuzoq: metod allaqachon bajarilgan, demak yon effekt sodir bo'lgan, faqat natija qaytarilmaydi. Yozish amallarida `@PostAuthorize` ishlatmaslik kerak.

```java
@Service
public class PaymentService {

    @PreAuthorize("hasAuthority('SCOPE_payments.write') and #cmd.amount <= 1000000")
    public PaymentId create(CreatePayment cmd) {
        return store(cmd);
    }

    // TUZOQ: bu chaqiruv proxy dan o'tmaydi, @PreAuthorize ishlamaydi
    public void createBatch(List<CreatePayment> cmds) {
        cmds.forEach(this::create);
    }

    // natijani filtrlash: faqat o'z filiali hisobotlari qoladi
    @PostFilter("filterObject.branchId == authentication.name")
    public List<Report> reports() { return allReports(); }
}
```

`@PostFilter` ro'yxatni xotirada filtrlaydi. 100 ming qatorni bazadan olib keyin 12 tasini qoldirish arxitektura xatosi. Filtrlash `WHERE` ga tushishi kerak.

### 20.9 Ko'p ijarachi (multi-tenant) va qator darajasidagi kirish nazorati

Bir nechta issuer bo'lsa, `JwtIssuerAuthenticationManagerResolver` har token uchun `iss` ga qarab mos `AuthenticationManager` ni tanlaydi va har biri o'z JWKS ini ishlatadi. Ro'yxat qattiq belgilangan bo'lishi shart, aks holda hujumchi o'z issuer ini ko'rsatib o'z tokenini yasaydi.

Qator darajasidagi nazorat uchun ikki yo'l bor. Birinchi: har `WHERE` ga `tenant_id` qo'shish, bu bitta esdan chiqqan query da sizib chiqishni beradi. Ikkinchi: PostgreSQL Row Level Security, tekshiruv bazada qoladi va ilova xatosiga bog'liq bo'lmaydi.

```sql
-- Ijarachi bo'yicha izolyatsiya bazada, ilovada emas.
ALTER TABLE payments ENABLE ROW LEVEL SECURITY;
ALTER TABLE payments FORCE ROW LEVEL SECURITY;  -- jadval egasiga ham tegsin

CREATE POLICY payments_tenant_isolation ON payments
  USING (tenant_id = current_setting('app.tenant_id', true)::uuid);

-- Har tranzaksiya boshida, pool dagi connection ga yopishib qolmasligi uchun LOCAL
SET LOCAL app.tenant_id = '9f1c...';
```

`SET LOCAL` tanlovi qasddan: u tranzaksiya oxirida avtomatik bekor bo'ladi. `SET` (LOCAL siz) ishlatilsa qiymat connection da qoladi va HikariCP uni keyingi foydalanuvchiga beradi, bu esa to'g'ridan to'g'ri ma'lumot sizishi. `current_setting('app.tenant_id', true)` dagi `true` sozlama yo'q bo'lsa `NULL` qaytaradi, `NULL = tenant_id` esa hech qanday qator bermaydi, ya'ni xato holatda tizim yopiq bo'ladi. Bu "fail closed" xatti-harakati, aynan shu kerak.

### 20.10 CORS, CSRF va ular qachon kerak

CSRF faqat brauzer so'rovga avtomatik credential (cookie yoki basic auth) qo'shadigan holatda kerak. `Authorization: Bearer` header ni brauzer o'zi qo'shmaydi, demak to'liq stateless JWT API da CSRF himoyasi ma'nosiz. Lekin tokenni cookie da saqlasangiz, CSRF yana kerak bo'ladi. Ko'pchilik `csrf().disable()` ni cookie sessiyali ilovada ham yozib qo'yadi, bu esa ochiq teshik.

CORS Spring Security da `CorsFilter` orqali ishlaydi va u CSRF dan oldin turadi. Ikki qoida esda tursin: `allowCredentials(true)` bilan `allowedOrigins("*")` birga ishlamaydi, `allowedOriginPatterns` kerak bo'ladi. Ikkinchisi: CORS brauzer himoyasi, server himoyasi emas, `curl` uni e'tiborsiz qoldiradi.

```java
@Bean
CorsConfigurationSource corsConfigurationSource() {
    CorsConfiguration cfg = new CorsConfiguration();
    cfg.setAllowedOriginPatterns(List.of("https://*.example.com"));  // * emas
    cfg.setAllowedMethods(List.of("GET", "POST", "PUT", "DELETE"));
    cfg.setAllowedHeaders(List.of("Authorization", "Content-Type"));
    cfg.setAllowCredentials(true);
    cfg.setMaxAge(1800L);   // preflight natijasi 30 daqiqa cache lanadi
    UrlBasedCorsConfigurationSource src = new UrlBasedCorsConfigurationSource();
    src.registerCorsConfiguration("/api/**", cfg);
    return src;
}
```

### 20.11 Parol saqlash, maxfiy ma'lumot va audit izlari

`DelegatingPasswordEncoder` (ya'ni `PasswordEncoderFactories.createDelegatingPasswordEncoder()`) hash ni `{bcrypt}$2a$10$...` ko'rinishida saqlaydi. Prefiks tufayli algoritmni migratsiyasiz almashtirish mumkin: yangi parollar `{argon2}` bilan yoziladi, eskilari hali `{bcrypt}` bilan tekshiriladi. BCrypt strength 10 taxminan 50 dan 100 ms gacha hisoblanadi, 12 esa taxminan 200 dan 400 ms. Bu login endpoint ning throughput ini to'g'ridan to'g'ri cheklaydi, demak brute force dan himoya bo'lib ham xizmat qiladi. BCrypt kiruvchi parolni 72 baytdan keyin kesib tashlaydi, uzun passphrase lar uchun Argon2 to'g'riroq tanlov.

Audit izi uchun `AuditorAware` ni `SecurityContextHolder` ga bog'lash eng qisqa yo'l. Lekin bu `@Async` va batch job larda bo'sh qaytadi, shuning uchun tizim foydalanuvchisi uchun zaxira qiymat kerak. Audit yozuvi hech qachon `Authentication#getCredentials()` ni, token ni yoki parolni saqlamasligi kerak. Log da token ko'rinib qolishi eng ko'p takrorlanadigan sizish kanali, odatda `DEBUG` darajadagi HTTP client logger orqali.

```java
@Bean
AuditorAware<String> auditorAware() {
    return () -> Optional.ofNullable(SecurityContextHolder.getContext().getAuthentication())
            .filter(Authentication::isAuthenticated)
            .map(Authentication::getName)
            .filter(name -> !"anonymousUser".equals(name))
            .or(() -> Optional.of("system"));   // batch job uchun zaxira
}
```

### 20.12 Keng tarqalgan xatolar: ochiq qolgan endpoint, tekshirilmagan token, ortiqcha huquq

Ochiq qolgan endpoint deyarli har doim `requestMatchers` tartibidan kelib chiqadi: birinchi mos kelgan qoida ishlaydi, shuning uchun `anyRequest().permitAll()` ni yuqoriga qo'yish keyingi qoidalarni o'ldiradi. Ikkinchi manba: `/actuator/**` uchun alohida zanjir yozilib, unda autentifikatsiya qo'yilmagani. `/actuator/env` va `/actuator/heapdump` maxfiy ma'lumot beradi, ularni ochiq qoldirish kritik xato. Uchinchi manba: `/api/v2/**` qo'shilgan, lekin konfiguratsiyada faqat `/api/v1/**` bor.

```bash
# Chiqishdan oldin minimal tekshiruv: tokensiz qancha endpoint javob beradi?
BASE=https://orders.example.com
for p in /api/payments /api/orders /actuator /actuator/env /actuator/heapdump \
         /api/v2/orders /swagger-ui/index.html /v3/api-docs; do
  code=$(curl -s -o /dev/null -w '%{http_code}' "$BASE$p")
  echo "$code $p"       # 401 yoki 403 kutiladi, 200 bo'lsa darhol tekshir
done
```

| Mezon | Oddiy yondashuv | Arxitektor yondashuvi |
|---|---|---|
| Zanjir soni | Bitta `SecurityFilterChain` hamma yo'l uchun | Yo'l bo'yicha ajratilgan zanjirlar, `securityMatcher` bilan |
| Standart qoida | `permitAll` dan boshlash, keyin yopish | `anyRequest().authenticated()` dan boshlash, keyin ochish |
| JWT tekshiruvi | `issuer-uri` yozib qo'yish bilan cheklanish | `iss`, `aud`, `exp`, `acr` ni ochiq validator bilan tekshirish |
| Authority | String rol nomlari kodga sochilgan | Konstanta va bitta prefiks konvensiyasi, scope va rol ajratilgan |
| Token umri | 24 soatlik access token, qulay bo'lgani uchun | 5 dan 15 daqiqa, refresh rotation va `jti` denylist |
| Bekor qilish | "JWT ni bekor qilib bo'lmaydi" deb qo'yib yuborish | `tokensValidAfter` yoki introspection, SLA raqami bilan |
| Ijarachi izolyatsiyasi | Har `WHERE` ga `tenant_id` qo'lda qo'shish | PostgreSQL RLS, `SET LOCAL` va fail closed xatti-harakat |
| CSRF | Hamma joyda `disable()` | Cookie sessiyali zanjirda yoqilgan, stateless zanjirda o'chirilgan |
| Metod xavfsizligi | `@PostFilter` bilan xotirada filtrlash | Filtrni `WHERE` ga tushirish, `@PreAuthorize` ni chegarada ishlatish |
| Nazorat | Konfiguratsiyani ko'z bilan o'qish | Avtomatlashtirilgan tekshiruv, testlash qo'llanmasidagi xavfsizlik testlari bo'limi |

Ortiqcha huquq eng sekin seziladigan xato. Odatda `SCOPE_orders.read` yetarli bo'lgan joyda `ROLE_ADMIN` talab qilinadi, chunki shunday yozish osonroq. Natijada har servis admin huquqi bilan ishlaydi va bitta buzilgan servis butun tizimni ochadi. Minimal scope ni yozib chiqish zerikarli ish, lekin uni qilmaslik narxi incident paytida bilinadi.

### 20.13 Amalda qo'llash

- [ ] Barcha `SecurityFilterChain` beanlarni ro'yxatga oling, `@Order` va `securityMatcher` qiymatlarini yozib, har bir yo'l qaysi zanjirga tushishini jadvalda tasdiqlang.
- [ ] Har bir zanjirda oxirgi qoida `anyRequest().authenticated()` yoki undan qattiqroq ekanini tekshiring, `permitAll` ni faqat aniq ro'yxat uchun qoldiring.
- [ ] `JwtDecoder` ga `aud` validatorini qo'shing yoki `spring.security.oauth2.resourceserver.jwt.audiences` ni to'ldiring, so'ng boshqa audience li token bilan 401 kelishini tasdiqlang.
- [ ] JWKS chaqiruviga connect taxminan 2 sekund va read taxminan 3 sekund timeout o'rnatib, IdP ni mavjudlik bog'liqligi sifatida monitoringga qo'shing.
- [ ] Access token TTL ini 15 daqiqadan oshmaydigan qilib kelishib oling va huquq olingandan keyin eski token qancha yashashini SLA sifatida hujjatlashtiring.
- [ ] `@Async` va batch kodda `DelegatingSecurityContextExecutorService` ishlatilayotganini tekshiring, aks holda `@PreAuthorize` va audit nomlari bo'sh qoladi.
- [ ] Ko'p ijarachi jadvallarda RLS ni yoqib, `SET LOCAL` ishlatilayotganini va sozlama yo'q holatda hech qanday qator qaytmasligini tekshiring.
- [ ] Chiqishdan oldin tokensiz `curl` skriptini CI ga qo'shib, `/actuator/env`, `/actuator/heapdump` va yangi versiya prefikslarini har deploy da sinab turing.


# IV. PostgreSQL chuqur bilim

## 21. PostgreSQL arxitekturasi: process model, WAL, checkpoint, vacuum (PostgreSQL Architecture)

PostgreSQL ko'pchilik Java dasturchisi uchun "JDBC orqasidagi qora quti" bo'lib qoladi, lekin production muammolarining katta qismi aynan shu qutining ichidagi mexanikadan kelib chiqadi: ulanish narxi, WAL yozuvi, checkpoint I/O cho'qqisi, vacuum qarzi. Bu bobda PostgreSQL 15-17 ichida nima sodir bo'lishini qarab chiqamiz va har bir mexanizmdan arxitektor qanday qaror chiqarishini ko'rsatamiz. Misollar bitta tizim ustida boradi: to'lov servisi, buyurtma jadvali, ombor qoldig'i va kunlik hisobot. Har bir bo'limda sozlash parametrining haqiqiy nomi va uni kuzatadigan katalog so'rovi bor.

### 21.1 Protsess modeli: postmaster, backend protsess, fon ishchilari

PostgreSQL thread modelida emas, protsess modelida ishlaydi. `postmaster` deb ataladigan asosiy protsess portni tinglaydi, umumiy xotirani yaratadi va har bir yangi ulanish uchun `fork()` qiladi. Natijada hosil bo'lgan backend protsess faqat o'sha bitta ulanishga xizmat qiladi va uzilganda o'ladi. Bu dizayn izolyatsiya beradi: bitta backend segfault bo'lsa, postmaster butun instansni qayta tiklaydi, lekin bitta buzilgan session boshqa sessionlarning stackini buzolmaydi.

Backendlardan tashqari doimiy fon ishchilari bor. `checkpointer` iflos sahifalarni diskka tushiradi, `background writer` buffer poolni oldindan bo'shatadi, `walwriter` WAL buferini fayl tizimiga oqizadi, `autovacuum launcher` ishchilarni ishga tushiradi, `archiver` WAL segmentlarini arxivga beradi, `logical replication launcher` esa logical slotlarni boshqaradi. PostgreSQL 15 dan boshlab statistika yig'uvchi alohida protsess emas, statistika umumiy xotirada saqlanadi, shuning uchun `pg_stat_*` ko'rinishlari arzonroq va restartda yo'qolmaydi.

```bash
# Instansdagi barcha protsesslarni ko'rish: kim backend, kim fon ishchisi
ps -o pid,etime,rss,cmd -u postgres | grep -E 'postgres:' | head -20

# Tipik natija (qisqartirilgan):
# postgres: checkpointer
# postgres: background writer
# postgres: walwriter
# postgres: autovacuum launcher
# postgres: logical replication launcher
# postgres: payments app 10.0.3.14(51322) idle in transaction
```

Arxitektor uchun muhim xulosa: `idle in transaction` holatidagi backend bu shunchaki bo'sh ulanish emas. U snapshot ushlab turadi va vacuum ishini to'sadi. Spring tomonida bu `@Transactional` metod ichida tashqi HTTP chaqiriq qilinganda yuzaga keladi.

### 21.2 Har ulanishga bitta protsess: bundan kelib chiqadigan ulanish narxi

`fork()` arzon emas. Yangi backend yaratilishi taxminan 1 dan 5 millisekundgacha oladi, uning ustiga ulanish autentifikatsiyasi, katalog keshini isitish va `search_path` o'rnatish qo'shiladi. Har bir bo'sh backend taxminan 2 dan 10 MB gacha xususiy xotira egallaydi, murakkab so'rovlardan keyin esa `work_mem` va katalog keshi hisobiga 50 MB dan oshishi mumkin. Shuning uchun `max_connections = 1000` qo'yish xatodir: PostgreSQL 1000 ta parallel backendda lock manager va snapshot hisob-kitoblari ustida o'zini yeb qo'yadi.

Amaliy qoida: haqiqiy parallel ishlayotgan backendlar soni CPU yadrosi sonidan 2-4 barobar ko'p bo'lmasin. 16 yadroli serverda 40-60 ta faol backend ko'pincha maksimal throughput beradi. Qolgan hamma narsa pool va PgBouncer vazifasi.

```properties
# Spring Boot 3.x: pool kattaligi PostgreSQL imkoniyatiga qarab tanlanadi
# 16 yadro, 4 ta instans => har instansga 10 ta ulanish, jami 40
spring.datasource.hikari.maximum-pool-size=10
spring.datasource.hikari.minimum-idle=10
# Pooldan ulanish kutish timeouti: tez fail qilish uchun qisqa
spring.datasource.hikari.connection-timeout=3000
# Backendni cheksiz band qilib turmaslik uchun
spring.datasource.hikari.max-lifetime=1800000
# Server tomonida himoya: tranzaksiya ichida qotib qolgan sessionni uzish
# postgresql.conf: idle_in_transaction_session_timeout = '30s'
# postgresql.conf: statement_timeout = '15s'
```

PgBouncer `transaction` rejimida 2000 ta application ulanishini 50 ta backendga siqadi. Buning narxi bor: session darajasidagi narsalar (`SET LOCAL` dan tashqari `SET`, advisory lock, prepared statement nomlari) ishonchsiz bo'ladi. Hibernate ishlatganda `prepareThreshold=0` yoki PgBouncer 1.21+ dagi prepared statement qo'llashini tekshirish kerak.

```sql
-- Ulanishlarning holati bo'yicha taqsimlanishi: pool muammosini shu ko'rsatadi
SELECT state, count(*), max(now() - state_change) AS eng_uzun
FROM pg_stat_activity
WHERE backend_type = 'client backend'
GROUP BY state ORDER BY 2 DESC;

-- Vacuum'ni to'sayotgan eng qadimgi tranzaksiya
SELECT pid, usename, application_name,
       now() - xact_start AS xact_davomiyligi, state, left(query, 60)
FROM pg_stat_activity
WHERE xact_start IS NOT NULL
ORDER BY xact_start LIMIT 5;
```

### 21.3 Umumiy xotira: `shared_buffers` va operatsion tizim keshi bilan munosabati

`shared_buffers` bu PostgreSQL ning o'z buffer pooli, 8 KB li sahifalardan iborat. Backend diskdan sahifa o'qiganda uni avval shu poolga joylaydi, o'zgartirsa sahifani "iflos" (dirty) deb belgilaydi. PostgreSQL ikki qatlamli keshga tayanadi: o'z pooli va operatsion tizim page cache. Shuning uchun `shared_buffers` ni RAM ning 80 foiziga qo'yish zarar keltiradi, chunki bir xil ma'lumot ikki joyda yotadi va OS ga joy qolmaydi.

Boshlang'ich nuqta: `shared_buffers` RAM ning taxminan 25 foizi, 64 GB li serverda 16 GB. `effective_cache_size` esa hech narsa ajratmaydi, u faqat plannerga "disk keshida shuncha joy bor" deb aytadi, uni RAM ning 50-75 foiziga qo'yish mumkin. `work_mem` har bir sort yoki hash node uchun ajratiladi, shuning uchun 100 ta backend va 4 ta sort node bo'lsa, real iste'mol `work_mem` ning 400 barobariga chiqishi mumkin.

```sql
-- pg_buffercache: kesh ichida qaysi jadvallar o'tiribdi
CREATE EXTENSION IF NOT EXISTS pg_buffercache;

SELECT c.relname,
       count(*) * 8192 / 1024 / 1024 AS kesh_mb,
       round(100.0 * count(*) FILTER (WHERE b.isdirty) / count(*), 1) AS iflos_foiz
FROM pg_buffercache b
JOIN pg_class c ON c.relfilenode = b.relfilenode
GROUP BY c.relname ORDER BY 2 DESC LIMIT 10;

-- Kesh hit ratio: 0.99 dan past bo'lsa shared_buffers yoki indeks muammosi
SELECT sum(heap_blks_hit) * 100.0 / nullif(sum(heap_blks_hit + heap_blks_read), 0)
         AS heap_hit_foiz
FROM pg_statio_user_tables;
```

16 GB dan katta `shared_buffers` da `huge_pages = try` qo'yish TLB bosimini kamaytiradi va taxminan 2-5 foiz CPU tejaydi. PostgreSQL 16 dan boshlab `pg_stat_io` ko'rinishi o'qish va yozishni kontekst bo'yicha ajratib beradi, bu checkpoint va vacuum I/O sini aralashtirmasdan o'lchash imkonini beradi.

### 21.4 Sahifa (page) tuzilishi, tuple va `ctid`

Heap fayl 8 KB li sahifalarga bo'lingan. Har sahifa boshida 24 baytli header, keyin sahifa oxiridan o'sib keladigan tuple ma'lumotlari va boshidan o'sib keladigan 4 baytli line pointer massivi joylashadi. Har bir tuple o'z headerida `xmin` (qaysi tranzaksiya yaratgan) va `xmax` (qaysi tranzaksiya o'chirgan) ni saqlaydi, header hajmi taxminan 23 bayt, hizalanish bilan 24 bayt.

`ctid` bu tuple ning fizik manzili: `(sahifa_raqami, sahifa_ichidagi_slot)`. UPDATE PostgreSQL da joyida o'zgartirish emas, balki yangi tuple yozish va eskisining `xmax` ini to'ldirishdir. Shuning uchun `ctid` barqaror identifikator emas va uni application darajasida saqlash xato.

```sql
-- ctid va tizim ustunlari: bitta buyurtma qatori qaysi sahifada yotadi
SELECT ctid, xmin, xmax, buyurtma_id, holat
FROM buyurtmalar WHERE buyurtma_id = 10045;

-- Sahifa ichini bayt darajasida ko'rish
CREATE EXTENSION IF NOT EXISTS pageinspect;
SELECT lp, lp_off, lp_len, t_xmin, t_xmax, t_ctid
FROM heap_page_items(get_raw_page('buyurtmalar', 0)) LIMIT 10;

-- Bitta satrga qancha sahifa va o'rtacha necha bayt to'g'ri keladi
SELECT relname, relpages, reltuples::bigint,
       pg_size_pretty(pg_relation_size(oid)) AS heap_hajm,
       round(pg_relation_size(oid)::numeric / nullif(reltuples, 0), 1) AS bayt_per_satr
FROM pg_class WHERE relname = 'buyurtmalar';
```

HOT (Heap Only Tuple) update yangi tuple ni shu sahifaning o'zida yaratadi va indeksni umuman yangilamaydi. Buning sharti ikkita: o'zgaruvchi ustunlarning birortasi indekslanmagan bo'lsin va sahifada bo'sh joy qolgan bo'lsin. Tez-tez yangilanadigan `ombor_qoldiq` jadvalida `ALTER TABLE ... SET (fillfactor = 80)` qo'yish va `oxirgi_ozgarish` ustunini indekslamaslik WAL hajmini sezilarli kamaytiradi.

### 21.5 WAL: yozuv tartibi, `wal_level`, `synchronous_commit` va ma'lumot xavfsizligi

WAL (Write Ahead Log) qoidasi oddiy: ma'lumot sahifasi diskka tushishidan oldin uning o'zgarishini tasvirlaydigan WAL yozuvi diskda bo'lishi shart. COMMIT paytida PostgreSQL ma'lumot fayllarini emas, faqat WAL ni `fsync` qiladi. Shuning uchun commit narxi jadval kattaligiga emas, disk `fsync` latensiyasiga bog'liq. NVMe diskda bu taxminan 0.05-0.2 ms, tarmoqli diskda 1-5 ms bo'lishi mumkin.

`wal_level` uch qiymat oladi. `minimal` eng kam yozadi, lekin replika ham, PITR ham bo'lmaydi. `replica` standart qiymat, streaming replication va arxivdan tiklash uchun yetarli. `logical` qo'shimcha ma'lumot yozadi va logical replication yoki CDC uchun kerak. Outbox naqshini Debezium bilan ishlatish rejasi bo'lsa, `logical` ni boshidan yoqib qo'yish kerak, chunki uni o'zgartirish restart talab qiladi.

```sql
-- WAL bilan bog'liq hamma sozlamani bir ko'rishda tekshirish
SELECT name, setting, unit, context
FROM pg_settings
WHERE name IN ('wal_level','synchronous_commit','full_page_writes','wal_compression',
               'wal_buffers','max_wal_size','min_wal_size','checkpoint_timeout',
               'checkpoint_completion_target','archive_mode')
ORDER BY name;

-- WAL generatsiya tezligi: ikki o'lchov orasidagi farqni oling
SELECT pg_current_wal_lsn() AS lsn, pg_walfile_name(pg_current_wal_lsn()) AS segment;

-- Replikatsiya kechikishi va slot ushlab turgan WAL hajmi
SELECT slot_name, active, pg_size_pretty(
         pg_wal_lsn_diff(pg_current_wal_lsn(), restart_lsn)) AS ushlangan_wal
FROM pg_replication_slots;
```

`synchronous_commit` ma'lumot xavfsizligining asosiy tugmasi. `on` (standart) commit ni mahalliy WAL diskka tushmaguncha kutadi. `off` kutmaydi, natijada commit 10-50 barobar tez bo'ladi, lekin crash paytida oxirgi `wal_writer_delay` ichidagi commitlar yo'qoladi; tranzaksiya atomikligi buzilmaydi, faqat tasdiqlangan commit yo'qolishi mumkin. `local` replikani kutmaydi, `remote_write` va `remote_apply` esa sinxron replikadan tasdiq kutadi.

Arxitektorning asosiy qarori shu yerda: xavfsizlik darajasi butun instans uchun bir xil bo'lishi shart emas. To'lov tranzaksiyasi `synchronous_commit = on` bilan ketadi, audit log yoki metrika yozuvi esa o'sha sessionda `SET LOCAL synchronous_commit = off` qilib tezlashtiriladi. `full_page_writes` ni o'chirish esa deyarli har doim xato, chunki u qisman yozilgan sahifadan himoya qiladi.

| Tuzoq | Nimaga olib keladi | Yechim |
|---|---|---|
| `@Transactional` ichida tashqi HTTP chaqiriq | `idle in transaction`, vacuum to'xtaydi, bloat o'sadi | Tranzaksiyani HTTP dan oldin yopish, `idle_in_transaction_session_timeout = 30s` |
| `max_connections = 500`, pool yo'q | Lock manager va snapshot CPU ni yeydi, latency sakraydi | PgBouncer transaction rejimi, backend soni yadro sonidan 2-4 barobar |
| Faol bo'lmagan replication slot qolgan | WAL to'planadi, `pg_wal` disk to'ladi, instans to'xtaydi | `pg_replication_slots` monitoringi, `max_slot_wal_keep_size` o'rnatish |
| `checkpoint_timeout = 5min`, katta yozuv | Har 5 daqiqada I/O cho'qqisi, p99 ikki barobar | `checkpoint_timeout = 15min`, `max_wal_size` kattalashtirish |
| Uzoq ishlaydigan hisobot tranzaksiyasi | Barcha jadvalda o'lik tuple tozalanmaydi | Hisobotni replikada bajarish, `hot_standby_feedback` ni o'ylab qo'yish |
| Tez-tez yangilanadigan ustun indekslangan | HOT update buziladi, indeks shishadi, WAL ko'payadi | Keraksiz indeksni olib tashlash, `fillfactor = 80` |
| Toast ustuniga `LIKE '%...%'` qidiruv | Har satr uchun dekompressiya, CPU yonadi | Alohida qidiruv ustuni yoki GIN indeksli `tsvector` |
| `autovacuum_vacuum_cost_delay` standart qoldirilgan | Katta jadvalda vacuum yetib ulgurmaydi | Jadval darajasida `cost_delay = 0`, `cost_limit = 1000` |

### 21.6 Checkpoint: qachon boshlanadi, I/O cho'qqisi va `checkpoint_timeout` sozlash

Checkpoint bu barcha iflos sahifalarni diskka tushirish va WAL da "shu nuqtadan tiklash boshlanadi" degan belgi qo'yish jarayoni. U uch holatda boshlanadi: `checkpoint_timeout` vaqti o'tganda (standart 5 daqiqa), `max_wal_size` chegarasiga yetilganda (standart 1 GB), yoki `CHECKPOINT` buyrug'i va to'g'ri to'xtatish paytida.

Ikki tur orasidagi farq muhim. Vaqt bo'yicha (`timed`) checkpoint rejali va yoyilgan, talab bo'yicha (`requested`) checkpoint esa yozuv hajmi bosganini bildiradi va odatda keskin I/O cho'qqisi yaratadi. Sog'lom instansda `requested` checkpointlar deyarli bo'lmasligi kerak.

```sql
-- PostgreSQL 17: checkpointer statistikasi alohida ko'rinishda
SELECT num_timed, num_requested,
       round(write_time / 1000.0) AS yozish_sek,
       round(sync_time / 1000.0) AS sync_sek, buffers_written
FROM pg_stat_checkpointer;

-- PostgreSQL 15 va 16 da shu ma'lumot pg_stat_bgwriter ichida
SELECT checkpoints_timed, checkpoints_req,
       checkpoint_write_time, checkpoint_sync_time, buffers_checkpoint
FROM pg_stat_bgwriter;

-- Oxirgi checkpoint qachon va qaysi LSN da bo'lgani
SELECT checkpoint_lsn, redo_lsn, checkpoint_time,
       pg_size_pretty(pg_wal_lsn_diff(pg_current_wal_lsn(), redo_lsn)) AS redo_dan_keyin
FROM pg_control_checkpoint();
```

Sozlash mantiqi: `checkpoint_timeout` ni 15 daqiqaga ko'tarish iflos sahifalarni ko'proq qayta ishlatish imkonini beradi, ya'ni bir xil sahifa 5 daqiqada uch marta emas, 15 daqiqada bir marta yoziladi. Narxi crash dan keyin tiklanish vaqtining uzayishi. `max_wal_size` ni shunday tanlash kerakki, `checkpoint_timeout` ichida generatsiya bo'ladigan WAL undan kichik bo'lsin. Yozuv og'ir to'lov tizimida `checkpoint_timeout = 15min`, `max_wal_size = 16GB`, `checkpoint_completion_target = 0.9` kombinatsiyasi ko'p holatda p99 latency ni tekislaydi. `wal_compression = lz4` esa checkpointdan keyingi full page image larni 2-4 barobar siqib, WAL hajmini kamaytiradi.

### 21.7 Vacuum nima qiladi: o'lik tuple, visibility map, index-only scan bilan bog'liqligi

MVCC tufayli DELETE va UPDATE hech narsani darhol o'chirmaydi, faqat tuple ni o'lik deb belgilaydi. VACUUM uch ish qiladi. Birinchi, hech bir snapshot ko'rmaydigan o'lik tuple larning joyini qayta ishlatish uchun bo'shatadi. Ikkinchi, indekslardan o'sha tuple larga bo'lgan ko'rsatkichlarni olib tashlaydi. Uchinchi, visibility map ni yangilaydi.

Visibility map har sahifa uchun ikki bit saqlaydi: `all-visible` va `all-frozen`. `all-visible` biti index-only scan uchun hayotiy ahamiyatga ega: agar sahifa to'liq ko'rinarli bo'lsa, planner heap ga murojaat qilmasdan faqat indeksdan javob beradi. Shuning uchun covering indeks qo'ygan odam `EXPLAIN` da `Heap Fetches: 900000` ko'rsa, muammo indeksda emas, vacuum qarzida.

```sql
-- O'lik tuple nisbati va oxirgi vacuum qachon bo'lgani
SELECT relname, n_live_tup, n_dead_tup,
       round(100.0 * n_dead_tup / nullif(n_live_tup + n_dead_tup, 0), 1) AS olik_foiz,
       last_autovacuum, autovacuum_count
FROM pg_stat_user_tables
WHERE n_dead_tup > 10000 ORDER BY olik_foiz DESC LIMIT 10;

-- Visibility map holati: index-only scan samarasi shunga bog'liq
CREATE EXTENSION IF NOT EXISTS pg_visibility;
SELECT * FROM pg_visibility_map_summary('buyurtmalar');

-- Ketayotgan vacuum qaysi fazada va qancha qilgani
SELECT pid, relid::regclass, phase, heap_blks_total, heap_blks_scanned,
       index_vacuum_count FROM pg_stat_progress_vacuum;
```

VACUUM tuple larni siqib, faylni kichraytirmaydi, faqat sahifa ichida joy bo'shatadi. Faylni qisqartirish uchun `VACUUM FULL` kerak, lekin u `ACCESS EXCLUSIVE` lock oladi va jadvalni butunlay bloklaydi.

### 21.8 Autovacuum sozlamalari va u yetishmay qolganda nima bo'ladi

Autovacuum launcher har `autovacuum_naptime` (standart 1 daqiqa) da bazalarni ko'rib chiqadi va ishchi ishga tushiradi. Jadval vacuum ga tushish sharti: o'lik tuple soni `autovacuum_vacuum_threshold` (50) plus `autovacuum_vacuum_scale_factor` (0.2) karra satr sonidan oshsa. Ya'ni 100 million satrli buyurtma jadvali 20 million o'lik tuple to'planmaguncha tozalanmaydi. Bu katta jadvallar uchun juda kech.

Ikkinchi muammo tezlik. `autovacuum_vacuum_cost_delay` standart qiymati 2 ms va `vacuum_cost_limit` 200, bu throughput ni taxminan sekundiga bir necha MB ga cheklaydi. Katta jadvalda bu vacuum ning yetib ulgurmasligiga olib keladi: o'lik tuple lar vacuum tozalaganidan tez to'planadi, jadval shishadi, so'rovlar sekinlashadi va bu o'z navbatida yana ko'proq lock yaratadi.

```sql
-- Katta va tez o'zgaradigan jadvalga individual autovacuum rejimi
ALTER TABLE buyurtmalar SET (
  autovacuum_vacuum_scale_factor = 0.02,   -- 20% emas, 2%
  autovacuum_vacuum_threshold = 5000,
  autovacuum_vacuum_cost_delay = 0,        -- throttling'ni olib tashlash
  autovacuum_vacuum_cost_limit = 2000,
  autovacuum_analyze_scale_factor = 0.01
);

-- Faqat INSERT bo'ladigan log jadvalida visibility map uchun (PG 13+)
ALTER TABLE tolov_audit SET (autovacuum_vacuum_insert_threshold = 50000);

-- Instans darajasi (postgresql.conf): 16 yadroli serverda
-- autovacuum_max_workers = 6
-- autovacuum_naptime = '15s'
-- maintenance_work_mem = '1GB'
-- log_autovacuum_min_duration = '1s'
```

Autovacuum ni butunlay o'chirish deyarli har doim halokatga olib keladi, chunki u nafaqat joy bo'shatadi, balki transaction ID freeze ishini ham bajaradi. `maintenance_work_mem` vacuum ning o'lik tuple identifikatorlari uchun ishlatadigan xotirasi; u kichik bo'lsa vacuum indekslarni bir necha marta aylanib o'tadi. PostgreSQL 17 da bu struktura samaraliroq bo'ldi va bir xil xotirada ko'proq TID saqlaydi.

### 21.9 Transaction ID o'ralishi (wraparound) va freeze jarayoni

Transaction ID 32 bitli, ya'ni taxminan 4 milliard qiymat, undan amalda 2 milliardi ishlatiladi. Tuple ning ko'rinishi `xmin` ni hozirgi XID bilan taqqoslash orqali aniqlanadi, shuning uchun XID hisoblagich aylanib ketsa, eski tuple "kelajakdan" ko'rinib qoladi. Buning oldini olish uchun yetarlicha qadimgi tuple lar `frozen` deb belgilanadi, ya'ni ular doim ko'rinarli hisoblanadi va XID taqqoslashga muhtoj emas.

`vacuum_freeze_min_age` (standart 50 million) qanchalik qadimgi tuple freeze bo'lishini, `autovacuum_freeze_max_age` (standart 200 million) esa autovacuum majburan aggressive vacuum boshlash chegarasini belgilaydi. Agar freeze orqada qolsa, PostgreSQL avval ogohlantirish log yozadi, keyin `vacuum_failsafe_age` (standart 1.6 milliard) da barcha throttling va indeks tozalashni tashlab, faqat freeze ga kirishadi. 2 milliardga yetilsa instans yozuvni rad etadi va faqat single user rejimda tiklanadi.

```sql
-- Baza darajasida wraparound'ga qancha qolgani
SELECT datname, age(datfrozenxid) AS xid_yoshi,
       round(100.0 * age(datfrozenxid) / 2000000000, 1) AS sarflangan_foiz
FROM pg_database ORDER BY 2 DESC;

-- Eng xavfli jadvallar: freeze orqada qolganlari
SELECT c.relname, age(c.relfrozenxid) AS xid_yoshi,
       pg_size_pretty(pg_total_relation_size(c.oid)) AS hajm
FROM pg_class c JOIN pg_namespace n ON n.oid = c.relnamespace
WHERE c.relkind IN ('r','m','t') AND n.nspname NOT LIKE 'pg\_%'
ORDER BY 2 DESC LIMIT 10;

-- Qo'lda tezkor freeze: oynadagi vaqtda, parallel bilan
VACUUM (FREEZE, VERBOSE, PARALLEL 4) buyurtmalar;
```

Monitoringda bitta alert yetarli: `age(datfrozenxid)` 500 million dan oshsa ogohlantirish, 1 milliarddan oshsa jiddiy hodisa. Yuqori yozuvli tizimda XID sarfi kuniga 50-100 million bo'lishi mumkin, demak zaxira vaqti haftalar bilan o'lchanadi, oylar bilan emas.

### 21.10 Jadval va indeks shishishi (bloat): o'lchash va tuzatish

Bloat bu jadval yoki indeks fayli ichidagi, ishlatilmayotgan lekin bo'shatilmagan joy. Manbasi uchta: vacuum qarzi, uzoq tranzaksiyalar va tez-tez UPDATE qilinadigan keng satrlar. Natijasi oddiy: bir xil ma'lumotni o'qish uchun ko'proq sahifa o'qiladi, kesh samarasi tushadi, sequential scan sekinlashadi.

Aniq o'lchov uchun `pgstattuple` ishlatiladi, lekin u butun jadvalni o'qiydi, shuning uchun katta jadvalda `pgstattuple_approx` yoki past yuklangan vaqtni tanlash kerak.

```sql
CREATE EXTENSION IF NOT EXISTS pgstattuple;

-- Jadval bloat: free_percent va dead_tuple_percent muhim
SELECT * FROM pgstattuple_approx('buyurtmalar');

-- Indeks bloat: avg_leaf_density 70% dan past bo'lsa reindex foydali
SELECT index_size, avg_leaf_density, leaf_fragmentation
FROM pgstatindex('buyurtmalar_mijoz_id_idx');

-- Hech ishlatilmaydigan indekslar: ularni o'chirish bloat va WAL ni kamaytiradi
SELECT relname, indexrelname, idx_scan,
       pg_size_pretty(pg_relation_size(indexrelid)) AS hajm
FROM pg_stat_user_indexes WHERE idx_scan = 0
ORDER BY pg_relation_size(indexrelid) DESC LIMIT 10;
```

Tuzatishda uch yo'l bor. `REINDEX INDEX CONCURRENTLY` indeksni yozuvni bloklamasdan qayta quradi va ko'pincha yetarli. `pg_repack` extension jadvalni ham online qayta zichlashtiradi, lekin oxirida qisqa vaqt exclusive lock oladi. `VACUUM FULL` eng samarali siqadi, lekin jadvalni to'liq bloklaydi va shuning uchun faqat rejali oynada qo'llanadi. Vaqt bo'yicha o'sadigan `tolov_audit` kabi jadvalda eng to'g'ri yechim umuman boshqacha: partitioning va eski partition ni `DROP TABLE` qilish, chunki u bloat masalasini butunlay yo'q qiladi.

### 21.11 `TOAST`: katta qiymatlar qanday saqlanadi

Tuple sahifadan katta bo'lishi mumkin emas, shuning uchun PostgreSQL satr hajmi taxminan 2 KB (`toast_tuple_target`, standart 2032 bayt) dan oshsa, katta ustunlarni siqadi va kerak bo'lsa alohida TOAST jadvaliga 2 KB ga yaqin chunk larga bo'lib chiqaradi. TOAST jadvali `pg_toast` sxemasida yashaydi va o'z indeksiga ega.

Har bir ustun uchun strategiya tanlanadi: `EXTENDED` (standart, siqadi va kerak bo'lsa chiqaradi), `EXTERNAL` (siqmaydi, lekin chiqaradi), `MAIN` (imkon qadar ichida qoldiradi), `PLAIN` (umuman TOAST qilmaydi). JSONB hisobot payload ida `substring` yoki prefiks qidiruv ko'p bo'lsa, `EXTERNAL` tezroq bo'ladi, chunki dekompressiya kerak emas. PostgreSQL 14 dan `default_toast_compression = lz4` mavjud va u `pglz` dan 2-4 barobar tez siqadi.

```sql
-- Jadvalning TOAST qismi qancha joy egallaydi
SELECT c.relname,
       pg_size_pretty(pg_relation_size(c.oid)) AS heap,
       pg_size_pretty(pg_relation_size(t.oid)) AS toast,
       pg_size_pretty(pg_indexes_size(c.oid)) AS indekslar
FROM pg_class c LEFT JOIN pg_class t ON t.oid = c.reltoastrelid
WHERE c.relname = 'hisobot_natija';

-- Ustun darajasida strategiya va siqish usuli
ALTER TABLE hisobot_natija ALTER COLUMN payload SET STORAGE EXTERNAL;
ALTER TABLE hisobot_natija ALTER COLUMN payload SET COMPRESSION lz4;

-- Qiymat TOAST bo'lganini tekshirish
SELECT pg_column_size(payload) AS saqlangan_bayt,
       octet_length(payload) AS haqiqiy_bayt
FROM hisobot_natija LIMIT 5;
```

TOAST ning yashirin narxi: `SELECT *` bilan 200 KB li JSONB ni har safar tortib olish tarmoq va CPU yeydi, hatto application unga qaramasa ham. Hibernate da bunday ustunni `@Basic(fetch = FetchType.LAZY)` yoki alohida entity ga ajratish kerak. Shuningdek TOAST jadvalining o'z vacuum i bor; uni `VACUUM (PROCESS_TOAST on)` boshqaradi va katta payload li jadvalda TOAST bloat asosiy jadvaldan kattaroq bo'lishi mumkin.

Quyidagi jadval butun bob bo'yicha ikki xil fikrlashni qiyoslaydi.

| Masala | Oddiy yondashuv | Arxitektor yondashuvi |
|---|---|---|
| Ulanish soni | `max_connections` ni 500 ga ko'tarish | Pool ni yadro soniga bog'lash, PgBouncer transaction rejimi, 40-60 faol backend |
| `shared_buffers` | RAM ning 75 foizi, "ko'proq yaxshi" | RAM ning 25 foizi plus `effective_cache_size`, `pg_buffercache` bilan tasdiqlash |
| Commit tezligi | Butun bazaga `synchronous_commit = off` | To'lov yo'lida `on`, audit yo'lida sessiya darajasida `off` |
| Checkpoint | Standart 5 daqiqa, tegmaslik | `checkpoint_timeout = 15min`, `max_wal_size` ni WAL tezligiga moslash, `requested` ni nolga tushirish |
| Vacuum | Kecha kerak bo'lganda `VACUUM FULL` | Jadval darajasida `scale_factor = 0.02`, `cost_delay = 0`, o'lik tuple monitoringi |
| Wraparound | Esga ham kelmaydi | `age(datfrozenxid)` ga alert, XID sarf tezligini o'lchash, freeze oynasi |
| Bloat | Hajm o'sganda indeks qo'shish | `pgstattuple` bilan o'lchash, `REINDEX CONCURRENTLY`, vaqt bo'yicha partitioning |
| Katta JSONB | Entity ga oddiy ustun qilib qo'yish | TOAST strategiyasi, `lz4`, lazy fetch, alohida jadval |
| UPDATE yuki | Hamma ustunga indeks qo'yish | HOT update ni saqlash, `fillfactor = 80`, keraksiz indeksni o'chirish |
| Hisobot so'rovi | Asosiy bazada uzoq tranzaksiya | Replikada bajarish, snapshot ushlab turmaslik, vacuum ni erkin qoldirish |

### 21.12 Amalda qo'llash

- [ ] `pg_stat_activity` dan `idle in transaction` sessionlarini sanab chiqing va `idle_in_transaction_session_timeout` ni 30 sekundga qo'ying.
- [ ] HikariCP `maximum-pool-size` ni barcha instanslar bo'yicha qo'shib, PostgreSQL yadro sonining 2-4 barobaridan oshmasligini tekshiring.
- [ ] `pg_stat_checkpointer` (yoki 16 va pastda `pg_stat_bgwriter`) dagi `num_requested` ni o'lchab, nolga yaqin bo'lmasa `checkpoint_timeout` va `max_wal_size` ni kattalashtiring.
- [ ] Eng katta uchta jadvalga individual `autovacuum_vacuum_scale_factor = 0.02` va `autovacuum_vacuum_cost_delay = 0` qo'yib, o'lik tuple nisbatini bir hafta kuzating.
- [ ] `age(datfrozenxid)` uchun monitoringga alert qo'shing: 500 million da ogohlantirish, 1 milliardda jiddiy hodisa.
- [ ] Index-only scan kutilgan so'rovlarda `EXPLAIN (ANALYZE, BUFFERS)` dagi `Heap Fetches` ni tekshirib, `pg_visibility_map_summary` bilan vacuum qarzini tasdiqlang.
- [ ] `pgstattuple_approx` bilan top 10 jadvalning bloat foizini o'lchab, 30 foizdan oshganlar uchun `pg_repack` yoki partitioning rejasini yozing.
- [ ] Katta JSONB yoki matn ustunlari uchun `pg_column_size` ni o'lchab, `lz4` siqish va lazy fetch ni joriy qiling.

## 22. MVCC, izolyatsiya darajalari, lock va deadlock (MVCC and Isolation)

Tranzaksiya izolyatsiyasi arxitektor uchun eng ko'p pul yo'qotadigan joy. Buyurtma ikki marta to'lanadi, ombor qoldig'i manfiy bo'ladi, hisobot jami summasi balansga to'g'ri kelmaydi. Bu xatolar testda ko'rinmaydi, chunki bitta sessiyada hamma narsa ishlaydi. Shu bob PostgreSQL ichida aniq nima sodir bo'layotganini va shu mexanikadan qanday qaror chiqarishni ko'rsatadi.

### 22.1 MVCC mexanikasi: `xmin`, `xmax`, snapshot va ko'rinuvchanlik qoidasi

PostgreSQL da `UPDATE` hech qachon qatorni joyida o'zgartirmaydi. U yangi versiya (tuple) yozadi va eskisini o'lgan deb belgilaydi. Har bir tuple da yashirin ustunlar bor: `xmin` ya'ni qaysi tranzaksiya bu versiyani yaratgan, `xmax` ya'ni qaysi tranzaksiya uni o'chirgan yoki yangilagan, `ctid` ya'ni jismoniy manzil.

Snapshot ichida uch narsa bor: pastki chegara, yuqori chegara va shu paytda ochiq tranzaksiyalar ro'yxati. Tuple ko'rinadi, agar `xmin` tranzaksiyasi commit qilgan va snapshot dan oldin tugagan bo'lsa, va `xmax` yo bo'sh, yo abort qilgan, yo snapshot dan keyin tugagan bo'lsa.

```sql
CREATE TABLE payment (id bigserial PRIMARY KEY, amount numeric, status text);
INSERT INTO payment (amount, status) VALUES (100, 'NEW');

SELECT ctid, xmin, xmax, status FROM payment;
--  (0,1) | 812 | 0 | NEW

UPDATE payment SET status = 'PAID' WHERE id = 1;

-- eski versiya diskda qoldi, yangi versiya yangi ctid oldi
SELECT ctid, xmin, xmax, status FROM payment;
--  (0,2) | 813 | 0 | PAID

-- o'lik versiyalar soni statistikada ko'rinadi
SELECT n_live_tup, n_dead_tup FROM pg_stat_user_tables
WHERE relname = 'payment';
```

Shundan ikki xulosa chiqadi. Birinchi: `UPDATE` narxi `INSERT` ga yaqin, chunki yangi tuple va unga tegishli hamma index yozuvi yangilanadi. Istisno HOT update: yangilangan ustunlar bironta ham index da bo'lmasa va sahifada joy bo'lsa, index tegilmaydi. Shuning uchun tez-tez yangilanadigan `last_seen_at` ga index qo'yish katta xato.

Ikkinchi: o'lik tuple lar o'zidan o'zi yo'qolmaydi, ularni `VACUUM` tozalaydi. Va `VACUUM` eng qadimgi ochiq snapshot dan keyingi hech narsani tozalay olmaydi.

### 22.2 PostgreSQL da Read Committed haqiqatda qanday ishlaydi

Read Committed default izolyatsiya. Ko'pchilik uni "commit qilingan ma'lumotni o'qiydi" deb biladi va shu bilan to'xtaydi. Mexanika boshqacha: har bir statement O'ZIGA yangi snapshot oladi. Bitta tranzaksiya ichidagi ikki `SELECT` turli natija qaytarishi normal holat.

Eng nozik joy `UPDATE` da. Kutilayotgan qatorni boshqa tranzaksiya o'zgartirib commit qilsa, PostgreSQL abort qilmaydi: u eng yangi versiyani oladi va `WHERE` shartini qayta tekshiradi. Buni EvalPlanQual deb ataladi.

```sql
-- SESSIYA A                          -- SESSIYA B
BEGIN;                                BEGIN;
UPDATE stock SET qty = qty - 1
  WHERE sku = 'SKU-1' AND qty > 0;
-- 1 qator, qator lock olindi
                                      UPDATE stock SET qty = qty - 1
                                        WHERE sku = 'SKU-1' AND qty > 0;
                                      -- B bloklangan, kutadi
COMMIT;
                                      -- B yangi versiyani oldi, WHERE qayta
                                      -- tekshirildi: qty hali > 0, UPDATE 1
                                      COMMIT;
```

Bu yerda `qty = qty - 1` ko'rinishi qutqardi, chunki yangi qiymatdan hisoblandi. Agar kod Java da hisoblangan tayyor qiymat yozsa, B ning yozuvi A ning ustidan bosadi va bitta birlik qoldiq yo'qoladi. Shu farq lost update ning asosi.

Yana bir tuzoq: yangi versiyada `WHERE` to'g'ri kelmasa, `UPDATE 0` qaytadi va hech qanday xato bo'lmaydi. Java kodi affected rows ni tekshirmasa, jim ravishda hech narsa yangilanmaydi.

```java
@Modifying
@Query("""
    update Stock s set s.qty = s.qty - :n
    where s.sku = :sku and s.qty >= :n
    """)
int reserve(String sku, int n);

// chaqiruvchi joy: affected rows majburiy tekshiriladi
int updated = stockRepository.reserve(sku, qty);
if (updated == 0) {
    throw new InsufficientStockException(sku);  // qoldiq yetmadi
}
```

### 22.3 Repeatable Read va serialization xatosi, qayta urinish zarurati

Repeatable Read da snapshot tranzaksiya boshida olinadi va oxirigacha o'zgarmaydi, hamma `SELECT` bir xil holatni ko'radi. Hisobot va ko'p bosqichli o'qish uchun ideal.

Yozishda narx paydo bo'ladi. Agar snapshot olgandan keyin boshqa kim o'zgartirgan qatorni yangilamoqchi bo'lsangiz, EvalPlanQual ishlamaydi va `40001` keladi: `could not serialize access due to concurrent update`. Tranzaksiya butunlay bekor bo'ladi.

Qoida: Repeatable Read yoki Serializable ishlatgan har bir yozuv yo'li qayta urinish mantiqiga ega bo'lishi shart. Retry tranzaksiyadan TASHQARIDA turishi kerak, chunki abort qilingan tranzaksiya ichida hech narsa qilib bo'lmaydi.

```java
@Service
public class SettlementRunner {
    private final SettlementService service;  // @Transactional shu ichida

    public void runWithRetry(long batchId) {
        int attempt = 0;
        while (true) {
            try {
                service.settle(batchId);     // har urinishda yangi tranzaksiya
                return;
            } catch (CannotSerializeTransactionException
                     | CannotAcquireLockException e) {
                if (++attempt >= 5) throw e;
                sleepQuiet(20L * (1L << (attempt - 1)));  // 20ms..320ms
            }
        }
    }
}
```

Spring da izolyatsiya `@Transactional(isolation = Isolation.REPEATABLE_READ)` bilan beriladi. Hibernate ning `@Version` optimistic locking ham aynan shunday retry talab qiladi.

### 22.4 Serializable izolyatsiya: predikat lock va uning narxi

Serializable PostgreSQL da Serializable Snapshot Isolation orqali amalga oshirilgan. U bloklamaydi va o'qishni sekinlashtirmaydi. U o'qish va yozish bog'liqliklarini kuzatadi, natija hech qanday ketma-ket bajarilishga to'g'ri kelmasa, tranzaksiyalardan birini `40001` bilan abort qiladi.

Kuzatish predikat lock orqali ketadi. `WHERE account_id = 7` bajarilsa, shu predikat eslab qolinadi, boshqa tranzaksiya unga tushadigan qator yozsa konflikt qayd etiladi. Predikat lock index darajasida bo'ladi, shuning uchun index borligi aniqlikka ta'sir qiladi: sequential scan da butun jadval kuzatiladi va yolg'on konflikt soni keskin oshadi.

```sql
-- write skew: mijozning jami balansi musbat qolishi kerak
-- SESSIYA A                                -- SESSIYA B
BEGIN ISOLATION LEVEL SERIALIZABLE;         BEGIN ISOLATION LEVEL SERIALIZABLE;
SELECT sum(balance) FROM account
  WHERE customer_id = 7;  -- 100
                                            SELECT sum(balance) FROM account
                                              WHERE customer_id = 7;  -- 100
UPDATE account SET balance = balance - 100
  WHERE id = 71;
                                            UPDATE account SET balance = balance - 100
                                              WHERE id = 72;
COMMIT;  -- muvaffaqiyat
                                            COMMIT;
-- ERROR: could not serialize access due to read/write dependencies
-- HINT: The transaction might succeed if retried.
```

Narxi uchta. Birinchi: SSI holati xotira talab qiladi, `max_pred_locks_per_transaction` default 64 va yetmasa lock sahifa yoki relation darajasiga ko'tariladi, aniqlik yo'qoladi. Ikkinchi: abort darajasi yuklama bilan o'sadi, hot qatorga ko'p yozuv tushsa 10 foizdan ortiq abort bo'lishi mumkin. Uchinchi: yashirin retry hisobiga latency oshadi.

Arxitektor qarori: Serializable ni butun ilovaga qo'ymang, faqat invariant haqiqatan global bo'lgan bir-ikki yo'lga qo'ying, masalan kredit limitini tekshirish. Qolgan joyda Read Committed plus aniq lock arzonroq va bashoratliroq.

### 22.5 Yo'qolgan yangilanish (lost update) va uni oldini olish usullari

Sxema bitta: ikki tranzaksiya bir qatorni o'qiydi, har biri Java da hisoblaydi, ikkisi ham yozadi, ikkinchisi birinchisini yo'q qiladi. Read Committed da bu hech qanday xato bermaydi.

To'rt yechim bor. Birinchi: hisoblashni SQL ichiga ko'chirish, `qty = qty - :n`, eng arzon. Ikkinchi: `@Version` optimistic locking. Uchinchi: `SELECT ... FOR UPDATE` pessimistic locking. To'rtinchi: izolyatsiyani ko'tarish plus retry.

```java
@Entity
public class Order {
    @Id private Long id;
    @Version private long version;   // Hibernate o'zi WHERE ga qo'shadi
    private BigDecimal total;
}

public interface StockRepository extends JpaRepository<Stock, Long> {
    @Lock(LockModeType.PESSIMISTIC_WRITE)   // SELECT ... FOR UPDATE
    Optional<Stock> findBySku(String sku);
}
```

Tanlov qoidasi: konflikt ehtimoli past bo'lsa optimistic, chunki kutish yo'q. Konflikt deyarli har safar bo'lsa, masalan bir xil ombor qatoriga yuzlab buyurtma, pessimistic kerak, aks holda retry bo'roni boshlanadi va throughput tushadi.

### 22.6 Qator darajasidagi lock: `FOR UPDATE`, `FOR NO KEY UPDATE`, `SKIP LOCKED`

`FOR UPDATE` eng kuchli qator lock i. U boshqa `FOR UPDATE`, `FOR SHARE`, `UPDATE` va `DELETE` ni bloklaydi. Nozik joyi: u shu qatorga foreign key qo'yadigan child insert ni ham bloklaydi.

`FOR NO KEY UPDATE` kuchsizroq. U key ustunlari o'zgarmasligini bildiradi, shuning uchun FK tekshiruvi bilan birga yashay oladi. Oddiy `UPDATE` o'zi default shu lock ni oladi. Parent qatorni non-key ustun uchun lock qilsangiz, shu variant child insert larni bekorga to'xtatmaydi.

```sql
-- interaktiv UI: kutish o'rniga darhol xato
SELECT * FROM invoice WHERE id = 42 FOR UPDATE NOWAIT;
-- ERROR: could not obtain lock on row ...  (SQLSTATE 55P03)

-- batch worker: band qatorlarni jimgina tashlab ketish
BEGIN;
SELECT id FROM invoice WHERE status = 'DRAFT'
ORDER BY id LIMIT 10 FOR UPDATE SKIP LOCKED;
COMMIT;
```

Advisory lock alohida mexanizm. `pg_advisory_xact_lock(key)` tranzaksiya oxirida o'zi bo'shaydi, `pg_advisory_lock(key)` sessiya oxirigacha turadi. Ikkinchisi connection pool bilan xavfli, chunki connection pool ga qaytganda lock qolib ketadi. Spring da faqat birinchi variantni ishlatish qoidasi bo'lsin.

### 22.7 Jadval darajasidagi lock turlari va DDL ning lock talabi

Jadval lock lari sakkiz turga bo'linadi, amalda uchtasi yetadi. `ACCESS SHARE` ni `SELECT` oladi. `ROW EXCLUSIVE` ni `INSERT`, `UPDATE`, `DELETE` oladi. `ACCESS EXCLUSIVE` ni `ALTER TABLE`, `DROP`, `TRUNCATE`, `VACUUM FULL`, `REINDEX` oladi va u hamma narsa bilan konflikt qiladi, hatto `SELECT` bilan.

Shundan produksiyadagi eng xavfli ketma-ketlik chiqadi. `ALTER TABLE` lock kutadi, u kutayotganda ortidan kelgan `SELECT` lar ham navbatga tushadi, chunki lock navbati FIFO. Natijada bitta uzun `SELECT` tufayli butun jadval bir necha daqiqa o'lik bo'ladi.

```sql
SET lock_timeout = '3s';          -- migratsiyada MAJBURIY
SET statement_timeout = '30s';

-- ustun qo'shish metadata-only, DEFAULT bilan ham jadval qayta yozilmaydi
ALTER TABLE orders ADD COLUMN channel text NOT NULL DEFAULT 'WEB';

-- NOT NULL cheklov ikki qadamda, uzun lock siz
ALTER TABLE orders ADD CONSTRAINT orders_ch_nn
  CHECK (channel IS NOT NULL) NOT VALID;
ALTER TABLE orders VALIDATE CONSTRAINT orders_ch_nn;

-- index: hech qachon oddiy CREATE INDEX emas
CREATE INDEX CONCURRENTLY idx_orders_channel ON orders (channel);
-- CONCURRENTLY tranzaksiya ichida ishlamaydi va xato bo'lsa INVALID
-- index qoldiradi, uni DROP INDEX CONCURRENTLY bilan tozalash kerak
```

`lock_timeout` ni migratsiyada majburiy qilish arxitektura qarori: 3 soniyada ololmasa migratsiya tushadi va keyin qayta urinadi, bu butun ilovaning o'lishidan yaxshi.

### 22.8 Deadlock qanday yuzaga keladi, log da qanday ko'rinadi, qanday oldini olinadi

Shart bitta: ikki tranzaksiya resurslarni teskari tartibda lock qiladi. PostgreSQL buni o'zi topadi: `deadlock_timeout` (default 1 soniya) o'tgach kutish grafigini tekshiradi, tsikl topsa biror tranzaksiyani `40P01` bilan o'ldiradi.

```
ERROR:  deadlock detected
DETAIL:  Process 2841 waits for ShareLock on transaction 9123; blocked by process 2902.
         Process 2902 waits for ShareLock on transaction 9124; blocked by process 2841.
         Process 2841: UPDATE account SET balance = balance - 50 WHERE id = 2;
         Process 2902: UPDATE account SET balance = balance - 50 WHERE id = 1;
CONTEXT:  while updating tuple (0,14) in relation "account"
```

Oldini olishning uch usuli. Birinchi va eng kuchli: har doim bir xil tartibda lock qilish. Ikkinchi: `IN (...)` ro'yxatiga tayanmaslik, chunki ichki tartib kafolatlanmaydi, `ORDER BY` plus `FOR UPDATE` ishlatish. Uchinchi: tranzaksiyani qisqa tutish.

```java
@Transactional
public void transfer(long fromId, long toId, BigDecimal amount) {
    // lock tartibi id bo'yicha, deadlock tuzilmaviy yo'q qilindi
    List<Long> ids = Stream.of(fromId, toId).sorted().toList();
    List<Account> locked = accountRepository.lockOrdered(ids);

    Account from = pick(locked, fromId);
    Account to   = pick(locked, toId);
    if (from.getBalance().compareTo(amount) < 0) throw new InsufficientFunds();
    from.debit(amount);
    to.credit(amount);
}
// lockOrdered ichidagi SQL:
// select * from account where id = any(:ids) order by id for update
```

### 22.9 Uzoq ochiq tranzaksiya: vacuum ni to'xtatishi va bloat keltirishi

Bu bobdagi eng qimmat tuzoq. `VACUUM` o'lik tuple ni faqat hech kim ko'rmasligi aniq bo'lsa tozalaydi, bu esa eng qadimgi ochiq snapshot bilan aniqlanadi. Bitta `idle in transaction` sessiya soatlab turib butun bazadagi tozalashni to'xtatadi.

Zanjir shunday: o'lik tuple soni o'sadi, jadval va index hajmi o'sadi, scan sekinlashadi, shared buffers o'lik sahifa saqlaydi, statistika eskiradi, so'rov rejasi buziladi. 2 GB jadval ikki kunda 20 GB bo'lishi real hodisa.

Eng ko'p uchraydigan sabab Java tomonida: `@Transactional` metod ichida HTTP chaqiruv turadi, tranzaksiya 50 ms emas, 8 soniya yashaydi. Ikkinchi sabab: `readOnly` hisobot tranzaksiyasi butun pagination tsiklini o'rab olgan.

```sql
-- global himoya, buzilgan kodni oshkor qiladi
ALTER SYSTEM SET idle_in_transaction_session_timeout = '60s';
ALTER SYSTEM SET statement_timeout = '30s';
ALTER SYSTEM SET log_lock_waits = on;
SELECT pg_reload_conf();

-- eng qadimgi xavfli sessiyalar
SELECT pid, state, now() - xact_start AS xact_age,
       now() - state_change AS idle_age, left(query, 50) AS q
FROM pg_stat_activity
WHERE xact_start IS NOT NULL AND now() - xact_start > interval '1 minute'
ORDER BY xact_start;
```

### 22.10 `pg_locks` va `pg_stat_activity` bilan bloklanishni topish

Hodisa paytida birinchi savol: kim kimni bloklayapti. Eng tez javob `pg_blocking_pids()` dan keladi.

```sql
SELECT w.pid AS kutayotgan, b.pid AS bloklovchi, b.state,
       now() - b.xact_start AS bloklovchi_yoshi,
       left(b.query, 40) AS bloklovchi_q
FROM pg_stat_activity w
JOIN pg_stat_activity b ON b.pid = ANY (pg_blocking_pids(w.pid))
WHERE w.wait_event_type = 'Lock'
ORDER BY bloklovchi_yoshi DESC;

-- kutilayotgan lock lar
SELECT locktype, relation::regclass, mode, pid
FROM pg_locks WHERE NOT granted ORDER BY pid;

SELECT pg_cancel_backend(2902);     -- avval so'rovni bekor qilish
SELECT pg_terminate_backend(2902);  -- oxirgi chora, sessiyani uzish
```

Monitoringda ikki metrikani alertga qo'ying: `wait_event_type = 'Lock'` bo'lgan sessiyalar soni va eng uzun ochiq tranzaksiya yoshi. `log_lock_waits = on` bilan 1 soniyadan uzun kutishlar log ga tushadi.

### 22.11 Navbat jadvali qurish: `SKIP LOCKED` bilan ishonchli ishlov berish

PostgreSQL navbat uchun yaxshi vosita, agar to'g'ri yozilsa. `FOR UPDATE SKIP LOCKED` bilan worker lar bir-birini kutmaydi va bir xil ishni ikki marta olmaydi.

```sql
CREATE TABLE outbox_job (
  id bigserial PRIMARY KEY, payload jsonb NOT NULL,
  status text NOT NULL DEFAULT 'READY', attempts int NOT NULL DEFAULT 0,
  run_after timestamptz NOT NULL DEFAULT now(), locked_at timestamptz
);
-- faqat ishlanishi kerak bo'lgan qatorlar index da
CREATE INDEX idx_outbox_ready ON outbox_job (run_after, id)
  WHERE status = 'READY';

-- tanlash va belgilash bitta atomik statement da
UPDATE outbox_job j
SET status = 'IN_PROGRESS', locked_at = now(), attempts = attempts + 1
FROM (
  SELECT id FROM outbox_job
  WHERE status = 'READY' AND run_after <= now()
  ORDER BY run_after, id LIMIT 20
  FOR UPDATE SKIP LOCKED
) AS picked
WHERE j.id = picked.id
RETURNING j.id, j.payload;
```

Uch qoida. Birinchi: partial index shart, aks holda navbat o'sgani sari olish so'rovi sekinlashadi. Ikkinchi: reaper kerak, chunki worker o'lsa status qaytmaydi, `locked_at` 5 daqiqadan oshganlarni `READY` ga qaytaradi. Uchinchi: ishlangan qatorni o'chirish yoki arxivga ko'chirish kerak, `DONE` holida qoldirsangiz jadval cheksiz o'sadi.

Hajm chegarasini bilib turing: bitta PostgreSQL navbat taxminan minutda 10 mingdan 50 minggacha ish uchun qulay, undan yuqorisida Kafka kerak. Lekin outbox uchun (dizayn patternlar hujjatidagi outbox pattern) shu jadval to'g'ri tanlov, chunki u biznes yozuvi bilan bir tranzaksiyada turadi.

| Tuzoq | Nima sodir bo'ladi | Yechim |
|---|---|---|
| Java da qiymatni hisoblab yozish | Lost update, qoldiq yo'qoladi | SQL ichida `qty = qty - :n` |
| Affected rows ni tekshirmaslik | `UPDATE 0` jim o'tadi | 0 holatida biznes exception |
| Repeatable Read ni retry siz ishlatish | `40001` foydalanuvchiga 500 bo'ladi | Tranzaksiyadan tashqarida retry |
| `@Transactional` ichida HTTP chaqiruv | Vacuum to'xtaydi, bloat o'sadi | I/O ni tranzaksiyadan chiqarish |
| `CREATE INDEX` CONCURRENTLY siz | Jadval yozishga yopiq | `CREATE INDEX CONCURRENTLY` |
| `ALTER TABLE` ni `lock_timeout` siz | Navbat yig'iladi, `SELECT` ham o'ladi | `SET lock_timeout = '3s'` |
| Lock larni turli tartibda olish | Deadlock, `40P01` | `ORDER BY id ... FOR UPDATE` |
| Sessiya advisory lock plus pool | Lock connection da qolib ketadi | Tranzaksiyaga bog'langan variant |
| Navbatda partial index yo'q | Olish so'rovi sekinlashadi | `WHERE status = 'READY'` index |

| Savol | Oddiy yondashuv | Arxitektor yondashuvi |
|---|---|---|
| Izolyatsiya tanlash | Hamma joyda default | Yo'l bo'yicha: hisobotga Repeatable Read, invariantga Serializable |
| Lost update | "Baza o'zi hal qiladi" | Atomik `UPDATE`, `@Version` yoki `FOR UPDATE` ni ongli tanlash |
| Serialization xatosi | Stack trace ni log ga tashlaydi | Idempotent retry, urinish soni o'lchanadi |
| Lock turi | Har joyda `FOR UPDATE` | Konflikt profiliga qarab `FOR NO KEY UPDATE` yoki `SKIP LOCKED` |
| DDL deploy | Migratsiyani ish vaqtida yuboradi | `lock_timeout`, `CONCURRENTLY`, ikki qadamli cheklov |
| Deadlock | Retry qo'shib unutadi | Lock tartibini tuzilmaviy majburlaydi, retry ikkinchi himoya |
| Uzun tranzaksiya | Sezmaydi | Timeout plus tranzaksiya yoshi alerti |
| Diagnostika | `pg_stat_activity` ni qo'lda ko'radi | `pg_blocking_pids` dashboard, `log_lock_waits = on` |
| Navbat | `SELECT` plus `UPDATE` ikki qadamda | Bitta atomik statement plus reaper |

### 22.12 Amalda qo'llash

- [ ] Hamma yozuv yo'llarini ro'yxatlab chiq va har biri lost update dan nima bilan himoyalanganini yoz. Himoyasiz yo'llarni darhol tuzat.
- [ ] Har bir shartli `UPDATE` ning affected rows ini tekshirishni majburiy qil va 0 holatida aniq biznes exception tashla.
- [ ] Repeatable Read yoki Serializable ishlatadigan yo'llarga tranzaksiyadan tashqarida 3-5 urinishli retry qo'y va urinish sonini metrika qilib chiqar.
- [ ] `@Transactional` metodlar ichidagi hamma tashqi HTTP, fayl va queue chaqiruvini audit qilib, tranzaksiyadan tashqariga ko'chir.
- [ ] Bazada `idle_in_transaction_session_timeout = 60s`, `statement_timeout = 30s`, `log_lock_waits = on` ni yoq va eng uzun ochiq tranzaksiya yoshiga alert qo'y.
- [ ] Migratsiya shabloniga `SET lock_timeout = '3s'` ni majburiy qator sifatida kirit va index yaratishni faqat `CONCURRENTLY` bilan ruxsat et.
- [ ] Pul yoki qoldiq o'zgartiradigan kodda lock lar `id` bo'yicha saralangan tartibda olinishini tekshir va buni test bilan qotir.
- [ ] Navbat jadvaliga partial index, `SKIP LOCKED` bilan atomik olish va qolib ketgan ishlar uchun reaper job qo'sh.

## 23. Indekslar: B-tree, GIN, GiST, BRIN va tanlov (Indexes)

Indeks so'rovni tezlashtiradigan sehr emas, balki ma'lumotning ikkinchi, tartiblangan nusxasi. Har bir indeks o'qishni tezlashtirgani uchun yozishdan, diskdan va vacuum vaqtidan to'lov oladi. Arxitektor uchun savol "indeks qo'shaylikmi" emas, balki "qaysi tur, qaysi ustunlar tartibida, qanday shart bilan va qaysi so'rovni qoplash uchun". Bu bobda PostgreSQL 15-17 dagi indeks turlarining ichki mexanikasi, ularning narxi va tanlov mezonlari ko'rib chiqiladi.

### 23.1 B-tree tuzilishi va u qaysi so'rovlarga yordam beradi

PostgreSQL ning standart indeksi B-tree, aniqrog'i B+tree ning Lehman-Yao variantidir. Daraxt 8 KB li sahifalardan iborat: yuqorida root, o'rtada internal sahifalar, pastda leaf sahifalar. Faqat leaf sahifalarda heap ga ko'rsatkichlar, ya'ni TID lar saqlanadi, va leaf qatlami ikki tomonlama bog'langan ro'yxat bo'lib, shu sababli oraliq bo'yicha skanlash bitta yo'nalishda ketma-ket boradi.

Chuqurlik juda sekin o'sadi. Taxminan 100 million qatorli `bigint` kalit uchun daraxt 4 qatlamdan oshmaydi va yuqori qatlamlar deyarli doim `shared_buffers` da yotadi.

B-tree quyidagilarga yordam beradi: `=`, `<`, `>`, `BETWEEN`, `IN`, `IS NULL`, `ORDER BY` uchun tayyor tartib, `MIN`/`MAX`, merge join, va unique constraint. U yordam bermaydigan holatlar: `LIKE '%mato%'` kabi prefiksi yo'q qidiruv, ustun ustida funksiya chaqirilgan shart, va jadvalning 10 foizidan ko'pini qaytaradigan so'rov. Oxirgi holatda planner ataylab seq scan ni tanlaydi, chunki random IO ketma-ket o'qishdan qimmatroq.

```sql
-- buyurtmalar jadvali: taxminan 80 mln qator
CREATE TABLE orders (
    id           bigserial PRIMARY KEY,
    customer_id  bigint      NOT NULL,
    status       text        NOT NULL,   -- NEW, PAID, SHIPPED, CANCELLED
    total_amount numeric(14,2) NOT NULL,
    created_at   timestamptz NOT NULL DEFAULT now()
);

-- status past kardinallikda: PG 13 dan boshlab deduplication
-- bir xil kalitlarni bitta posting list ga yig'adi va indeksni kichraytiradi
CREATE INDEX idx_orders_status ON orders (status);

EXPLAIN (ANALYZE, BUFFERS)
SELECT id, total_amount FROM orders WHERE created_at > now() - interval '1 day';
```

### 23.2 Ko'p ustunli indeks va ustunlar tartibining ahamiyati

Ko'p ustunli B-tree da tartib hal qiluvchi. Indeks `(a, b, c)` kalitlari leksikografik tartibda saqlanadi, shuning uchun u faqat chapdan boshlangan prefiks uchun samarali: `a`, keyin `a, b`, keyin `a, b, c`. Agar so'rovda `a` bo'yicha shart bo'lmasa, PostgreSQL indeksni butunlay skanlashi mumkin, lekin bu seq scan dan kam farq qiladi, chunki tanlab o'tish imkoniyati yo'qoladi.

Amaliy qoida: tenglik shartidagi ustunlar oldinda, oraliq yoki tartiblash ustuni oxirida. Mijoz kabinetidagi "oxirgi 20 buyurtma" so'rovi uchun `(customer_id, created_at DESC)` to'g'ri tartib. Teskari tartib `(created_at, customer_id)` da planner avval sana oralig'ini oladi, keyin har bir qatorni mijoz bo'yicha filtrlaydi, ya'ni ortiqcha minglab heap o'qish paydo bo'ladi.

Ikkinchi mezon: ustun soni. Har bir qo'shimcha ustun indeks qatorini kengaytiradi va leaf sahifaga sig'adigan kalit sonini kamaytiradi. To'rt va undan ko'p ustunli indeks ko'pincha foydasini oqlamaydi, chunki yozuv narxi hamma so'rovga tegadi, tezlik esa bittasiga.

```sql
-- noto'g'ri: created_at oldinda, customer_id filtrga tushadi
CREATE INDEX idx_bad ON orders (created_at DESC, customer_id);

-- to'g'ri: tenglik oldinda, tartiblash oxirida
CREATE INDEX idx_good ON orders (customer_id, created_at DESC);

-- bu so'rov idx_good bilan 20 ta leaf qatorini o'qib to'xtaydi,
-- idx_bad bilan esa butun kunlik oraliqni skanlaydi
SELECT id, status, total_amount
FROM orders
WHERE customer_id = 48213
ORDER BY created_at DESC
LIMIT 20;
```

### 23.3 Qamrab oluvchi indeks (`INCLUDE`) va index-only scan sharti

`INCLUDE` PostgreSQL 11 dan beri mavjud va indeksga qidiruv kaliti bo'lmagan ustunlarni qo'shadi. Bu ustunlar faqat leaf sahifalarda yotadi, daraxt tartibiga qatnashmaydi va `ORDER BY` uchun ishlatilmaydi. Maqsadi bitta: so'rov qaytaradigan hamma ustun indeksda bo'lsa, PostgreSQL heap ga bormasdan javob beradi, ya'ni index-only scan bajariladi.

Lekin index-only scan ning ikkinchi sharti bor va ko'pchilik shuni e'tiborsiz qoldiradi: visibility map da tegishli sahifa all-visible deb belgilangan bo'lishi kerak. Yangi yozilgan yoki yangilangan sahifalar uchun bu belgi yo'q, shuning uchun vacuum ishlamagan jadvalda index-only scan amalda heap fetch ga aylanadi. `EXPLAIN (ANALYZE, BUFFERS)` chiqishidagi `Heap Fetches: 0` yagona ishonchli dalil.

Unique indeksda `INCLUDE` ayniqsa foydali, chunki unikallik faqat kalit ustunlar bo'yicha tekshiriladi, qolgan ustunlar esa yuk sifatida boradi.

```sql
-- hisobot so'rovi faqat shu uch ustunni qaytaradi
CREATE INDEX idx_orders_cust_covering
    ON orders (customer_id, created_at DESC)
    INCLUDE (status, total_amount);

-- Heap Fetches: 0 bo'lsagina index-only scan haqiqatan ishlagan
EXPLAIN (ANALYZE, BUFFERS)
SELECT created_at, status, total_amount
FROM orders
WHERE customer_id = 48213
ORDER BY created_at DESC
LIMIT 50;

-- visibility map ni yangilash: aggressiv autovacuum yoki qo'lda
VACUUM (ANALYZE) orders;

-- unikallik faqat (tenant_id, email) bo'yicha, ism yuk sifatida
CREATE UNIQUE INDEX uq_users_email
    ON users (tenant_id, lower(email)) INCLUDE (full_name);
```

### 23.4 Qisman indeks (`WHERE` bilan) va uning amaliy foydasi

Qisman indeks jadvalning faqat bir qismini qamraydi. Eng kuchli qo'llanishi navbat jadvali: 80 million buyurtmaning faqat 20 mingtasi `NEW` holatida bo'lsa, `WHERE status = 'NEW'` sharti bilan qurilgan indeks taxminan 1 MB joy oladi, to'liq indeks esa 2 GB dan oshadi. Kichik indeks to'liq cache da yotadi va yozuv narxi ham deyarli nolga tushadi, chunki `PAID` holatiga o'tgan qator indeksdan chiqib ketadi.

Ikkinchi kuchli qo'llanishi shartli unikallik: "bitta foydalanuvchida faqat bitta aktiv karta bo'lsin" qoidasini `WHERE deleted_at IS NULL` sharti bilan unique indeks orqali ifodalash mumkin. Buni `CHECK` yoki application logikasi bilan ishonchli qilib bo'lmaydi.

Tuzoq shu yerda: planner qisman indeksni faqat so'rov sharti indeks shartidan kelib chiqishini isbotlay olsa ishlatadi. `status = 'NEW'` literal bilan ishlaydi, lekin JPA yuboradigan `status = $1` bind parameter bilan isbot tuzilmaydi va indeks e'tiborga olinmaydi. Shuning uchun qisman indeks shartini application so'rovida literal sifatida yozish yoki shartni `created_at > '2026-01-01'` kabi turg'un chegara bilan qurish kerak.

```sql
-- navbat: faqat qayta ishlanmagan buyurtmalar
CREATE INDEX idx_orders_queue
    ON orders (created_at)
    WHERE status = 'NEW';

-- shartli unikallik: o'chirilmagan kartalar orasida bitta primary
CREATE UNIQUE INDEX uq_card_primary
    ON payment_cards (customer_id)
    WHERE is_primary AND deleted_at IS NULL;

-- ombor qoldig'ining faqat muammoli qatorlari
CREATE INDEX idx_stock_negative
    ON stock_balance (warehouse_id, sku)
    WHERE quantity < 0;
```

### 23.5 Ifoda bo'yicha indeks va funksiya bilan qidirish

Ustun ustida funksiya chaqirilgan shart oddiy indeksni o'ldiradi, chunki indeksda `email` yotadi, so'rov esa `lower(email)` ni so'raydi. Yechim ifoda bo'yicha indeks: indeks kaliti sifatida ifodaning o'zi saqlanadi. Shart bitta, ifoda `IMMUTABLE` bo'lishi kerak, ya'ni bir xil kirish uchun doim bir xil natija bersin.

Shu sababli `date_trunc('day', created_at)` ni `timestamptz` ustida indekslash mumkin emas: natija session ning time zone sozlamasiga bog'liq, demak funksiya `STABLE`, `IMMUTABLE` emas. Bu holatda kundalik agregatsiya uchun oddiy `created_at` indeksini qurib, so'rovni yarim ochiq oraliqqa aylantirish to'g'ri yo'l.

Qo'shimcha foyda: ifoda bo'yicha indeks qurilganda `ANALYZE` shu ifoda uchun alohida statistika yig'adi. `jsonb` dan chiqarilgan `status` maydonining selektivligini planner shu statistikadan biladi, aks holda u qattiq kodlangan taxminni ishlatadi.

```sql
-- registratsiyada katta-kichik harf farqi bo'lmasin
CREATE UNIQUE INDEX uq_customer_email_ci
    ON customers (lower(email));
SELECT id FROM customers WHERE lower(email) = lower('Alisher@Mail.Uz');

-- jsonb payload ichidagi tashqi ID bo'yicha qidiruv
CREATE INDEX idx_payment_ext_id
    ON payments ((payload ->> 'external_id'));

-- date_trunc timestamptz ustida IMMUTABLE emas, shuning uchun
-- oraliq shartini ishlatamiz va oddiy indeks yetarli bo'ladi
CREATE INDEX idx_orders_created ON orders (created_at);
SELECT date_trunc('day', created_at) AS d, sum(total_amount)
FROM orders
WHERE created_at >= '2026-09-01' AND created_at < '2026-10-01'
GROUP BY 1;
```

### 23.6 GIN: massiv, `jsonb` va to'liq matn qidiruvi uchun

GIN teskari indeks: u qiymatni emas, qiymat ichidagi elementlarni kalit qilib oladi va har bir kalit uchun TID lar ro'yxatini saqlaydi. Shuning uchun u bitta ustunda ko'p elementli qiymat yotganda ishlaydi: massiv, `jsonb`, `tsvector`, va `pg_trgm` orqali trigrammalarga ajratilgan matn. Qo'llanadigan operatorlar `@>`, `?`, `?|`, `?&`, `&&` va to'liq matn uchun `@@`.

`jsonb` uchun ikki opclass bor. Standart `jsonb_ops` hamma kalit va qiymatni indekslaydi, shuning uchun `?` operatori ham ishlaydi, lekin hajmi katta. `jsonb_path_ops` faqat yo'l va qiymat hash ini saqlaydi, taxminan ikki barobar kichik va `@>` so'rovlarida tezroq, lekin kalit mavjudligini tekshiruvchi operatorlarni qo'llamaydi.

Hajm haqida ogohlik: `tsvector` ustidagi GIN jadval hajmining taxminan 20-40 foizini oladi va qurilishi B-tree dan bir necha barobar uzoq davom etadi, shuning uchun uni `maintenance_work_mem` ni kamida 1 GB qilib qo'ygan sessiyada qurish kerak.

Mexanikaning muhim qismi: GIN da `fastupdate` yoqilgan va yangi yozuvlar avval pending list ga tushadi. Ro'yxat `gin_pending_list_limit` (standart 4 MB) ga yetganda yoki vacuum vaqtida asosiy tuzilmaga ko'chiriladi. Natijada ommaviy `INSERT` dan keyingi birinchi qidiruv kutilmaganda sekin bo'ladi, chunki u pending list ni ketma-ket o'qiydi. Yuqori yozuv oqimida `fastupdate = off` qilish yoki pending limitni kamaytirish kerak bo'ladi.

```sql
CREATE EXTENSION IF NOT EXISTS pg_trgm;

-- to'lov payload i bo'yicha containment qidiruvi
CREATE INDEX idx_payments_payload
    ON payments USING gin (payload jsonb_path_ops);
SELECT id FROM payments WHERE payload @> '{"provider":"click"}';

-- mahsulot teglari massivi
CREATE INDEX idx_product_tags ON products USING gin (tags);
SELECT id FROM products WHERE tags && ARRAY['aksiya','yangi'];

-- ichki qidiruv: ILIKE '%...%' uchun yagona ishlaydigan variant
CREATE INDEX idx_products_name_trgm
    ON products USING gin (name gin_trgm_ops);
SELECT id, name FROM products WHERE name ILIKE '%simsiz quloqchin%';

-- yuqori yozuv oqimida pending list ni o'chirish
ALTER INDEX idx_payments_payload SET (fastupdate = off);
```

### 23.7 GiST, matn o'xshashligi va oraliq turlar

GiST umumlashgan qidiruv daraxti: har bir ichki tugun o'z farzandlarini qamrab oluvchi predikatni saqlaydi. Bu tuzilma lossy, ya'ni indeks faqat nomzod qatorlarni qaytaradi va yakuniy tekshiruv heap da bajariladi. Shuning uchun GiST tenglik qidiruvida B-tree dan sekin, lekin u B-tree ifodalay olmaydigan munosabatlarni ifodalaydi: kesishish, qamrash, masofa.

Arxitektor uchun eng qimmatli qo'llanishi exclusion constraint. "Bitta xonaga ustma-ust tushgan ikki bron bo'lmasin" yoki "bitta mahsulotning narx amal qilish davrlari kesishmasin" qoidasini `tstzrange` va `&&` operatori bilan baza darajasida majburlash mumkin. Skalyar ustunni (xona ID si) oraliq bilan bitta constraint ga qo'shish uchun `btree_gist` kengaytmasi kerak.

Ikkinchi qo'llanishi KNN tartiblash: `ORDER BY name <-> 'qidiruv matni' LIMIT 10` so'rovi GiST da indeks orqali bajariladi va "eng o'xshash 10 ta" javobini butun jadvalni saralamasdan beradi. GIN bunday tartiblashni qo'llamaydi, shuning uchun o'xshashlik reytingi kerak bo'lsa GiST tanlanadi.

```sql
CREATE EXTENSION IF NOT EXISTS btree_gist;

-- narx amal qilish davrlari kesishmasligi kafolati
ALTER TABLE price_periods
    ADD CONSTRAINT no_overlap_price
    EXCLUDE USING gist (product_id WITH =, valid_period WITH &&);

-- ombor bronlari uchun ham shu yondashuv
ALTER TABLE reservations
    ADD CONSTRAINT no_overlap_slot
    EXCLUDE USING gist (warehouse_id WITH =, period WITH &&)
    WHERE (status <> 'CANCELLED');

-- o'xshashlik bo'yicha tartiblash: GiST, GIN emas
CREATE INDEX idx_customers_name_gist
    ON customers USING gist (full_name gist_trgm_ops);
SELECT id, full_name
FROM customers
ORDER BY full_name <-> 'alisher navoiev'
LIMIT 10;
```

### 23.8 BRIN: katta, tartibli jadvallar uchun arzon indeks

BRIN qator emas, blok oraliqlarini indekslaydi. Har `pages_per_range` sahifa (standart 128, ya'ni 1 MB) uchun u shu oraliqdagi minimal va maksimal qiymatni saqlaydi. Natijada indeks hayratlanarli kichik: 300 GB li audit log jadvali uchun `created_at` ustida BRIN taxminan bir necha MB joy oladi, xuddi shu ustundagi B-tree esa 8 GB dan oshadi.

BRIN lossy indeks: u mos kelishi mumkin bo'lgan blok oraliqlarini qaytaradi, keyin har bir qator heap da qayta tekshiriladi. Shuning uchun u nuqtali qidiruv uchun emas, kunlik yoki oylik oraliq bo'yicha agregatsiya uchun mo'ljallangan.

Shart bitta va qattiq: jadvalning fizik tartibi ustun qiymati bilan korrelyatsiya qilishi kerak. Append-only log, `created_at` yoki `bigserial` ID buni tabiiy beradi. Korrelyatsiyani `pg_stats.correlation` dan tekshirish mumkin, qiymat 1 ga yaqin bo'lsa BRIN ishlaydi, 0 ga yaqin bo'lsa foydasiz. Ko'p `UPDATE` bo'ladigan jadvalda tartib buziladi va BRIN sekin asta o'z ma'nosini yo'qotadi.

PostgreSQL 14 dan `minmax_multi` opclass bor: u bitta oraliq uchun bir nechta chegara to'plamini saqlaydi, shuning uchun bir nechta chetlab ketgan qiymat butun oraliqni buzmaydi. `bloom` opclass esa korrelyatsiyasiz ustunda tenglik qidiruvi uchun ishlaydi. Yangi sahifalarni avtomatik umumlashtirish uchun `autosummarize = on` yoqiladi.

```sql
-- audit log: append-only, 300 GB, kunlik oraliq so'rovlari
CREATE TABLE audit_log (
    id         bigserial,
    entity     text        NOT NULL,
    payload    jsonb,
    created_at timestamptz NOT NULL DEFAULT now()
);

CREATE INDEX idx_audit_created_brin
    ON audit_log USING brin (created_at)
    WITH (pages_per_range = 64, autosummarize = on);

-- korrelyatsiya 1 ga yaqin bo'lsagina foyda bor
SELECT attname, correlation
FROM pg_stats
WHERE tablename = 'audit_log' AND attname = 'created_at';

-- oraliq so'rov: BRIN nomzod bloklarni beradi, heap recheck qiladi
EXPLAIN (ANALYZE, BUFFERS)
SELECT count(*) FROM audit_log
WHERE created_at >= '2026-10-01' AND created_at < '2026-10-02';
```

| Holat | Mos indeks turi | Sabab |
|---|---|---|
| ID yoki kod bo'yicha nuqtali qidiruv | B-tree | eng kichik latency, unikallikni ham beradi |
| Sana oralig'i va `ORDER BY ... LIMIT` | B-tree | tartib tayyor, saralash kerak emas |
| Jadvalning 1 foizi qiziq (navbat) | Qisman B-tree | indeks kichik, cache da, yozuv narxi past |
| `lower(email)`, `payload ->> 'id'` | Ifoda bo'yicha B-tree | so'rov ifodasi indeks kaliti bilan bir xil |
| `jsonb @>`, massiv `&&` | GIN | elementlar bo'yicha teskari ro'yxat |
| `ILIKE '%matn%'` | GIN + `gin_trgm_ops` | trigramma bo'yicha nomzodlar |
| To'liq matn qidiruvi `@@` | GIN + `tsvector` | leksemalar bo'yicha indeks |
| O'xshashlik reytingi `<->` | GiST + `gist_trgm_ops` | KNN tartiblashni qo'llaydi |
| Oraliqlar kesishmasligi | GiST exclusion | `&&` operatori faqat GiST da |
| 100 GB dan katta append-only log | BRIN | hajmi MB larda, oraliq so'rovga yetarli |
| Yuqori kardinallik va tez `UPDATE` | B-tree | BRIN korrelyatsiyani yo'qotadi |

### 23.9 Indeks narxi: yozuv sekinlashuvi, disk, vacuum yuki

Har bir `INSERT` jadvalga bitta, indekslarga esa har biriga bittadan yozuv qo'shadi. Bu yozuvlar WAL ga ham tushadi, va agar sahifa checkpoint dan keyin birinchi marta o'zgarsa, WAL ga butun sahifa tasviri yoziladi. Taxminan har bir qo'shimcha indeks insert-og'ir jadvalda 5 dan 15 foizgacha sekinlashuv beradi, sakkiz indeksli jadvalda yozuv latency si indekssiz holatga nisbatan ikki barobarga chiqishi normal.

Ikkinchi, ko'rinmas narx HOT update ni buzish. PostgreSQL yangilangan ustun hech bir indeksda qatnashmasa, yangi versiyani o'sha sahifada qoldiradi va indekslarga tegmaydi. Bu HOT update deyiladi. Agar siz tez-tez o'zgaradigan `last_seen_at` yoki `status` ustuniga indeks qo'ysangiz, har bir `UPDATE` hamma indeksga yangi yozuv qo'shadi, bloat tezlashadi, vacuum ko'proq ishlaydi.

Uchinchi narx vacuum ning o'zi. Vacuum har bir indeksni ko'rib chiqadi, demak uning davomiyligi indekslar soniga chiziqli bog'liq va ortiqcha indekslar wraparound xavfini yaqinlashtiradi.

| Jihat | Oddiy yondashuv | Arxitektor yondashuvi |
|---|---|---|
| Indeks qo'shish qarori | Sekin so'rov ko'rindi, indeks qo'shildi | `EXPLAIN (ANALYZE, BUFFERS)` o'qiladi, mavjud indeks kengaytiriladi |
| Ustunlar tartibi | Yozilish tartibida | Tenglik oldinda, oraliq va `ORDER BY` oxirida |
| Qamrov | Har bir so'rovga alohida indeks | Bitta `INCLUDE` li indeks bir nechta so'rovni qoplaydi |
| Hajm | Butun jadval indekslanadi | `WHERE` sharti bilan faqat kerakli qism |
| Katta log jadvali | `created_at` ustida B-tree | BRIN, korrelyatsiya o'lchangandan keyin |
| `jsonb` qidiruv | Har bir maydonga alohida indeks | Bitta GIN, kerak bo'lsa `jsonb_path_ops` |
| Ishlab chiqarishga chiqarish | Oddiy `CREATE INDEX`, jadval bloklanadi | `CONCURRENTLY`, `lock_timeout`, uzun tranzaksiyalar tekshiriladi |
| Eskirgan indeks | Hech kim tegmaydi | `pg_stat_user_indexes` choraklik ko'rikda, replikalar ham |
| Shishish | Sezilganda `REINDEX`, jadval bloklanadi | `pgstatindex` bilan o'lchash, `REINDEX CONCURRENTLY` |
| O'lchov | "Tez bo'ldi shekilli" | p95 latency va indeks hajmi dashboard da kuzatiladi |

### 23.10 Keraksiz indekslarni topish va o'chirish (`pg_stat_user_indexes`)

`pg_stat_user_indexes` har bir indeks bo'yicha `idx_scan` hisoblagichini beradi. Nol yoki juda kichik qiymat indeks ishlatilmayotganini bildiradi, lekin ikki shartni esdan chiqarmaslik kerak. Birinchisi: statistika `pg_stat_reset` yoki major upgrade dan beri yig'iladi, shuning uchun `pg_stat_database.stats_reset` sanasini ko'rib, kamida bir necha hafta, hisobot mavsumini qamrab oluvchi muddat kutish kerak. PostgreSQL 16 dan `last_idx_scan` ustuni bor va u qarorni ancha osonlashtiradi.

Ikkinchi shart ko'pincha xatolikka olib keladi: statistika har bir instansda alohida yig'iladi. Agar hisobot so'rovlari read replica ga yuborilsa, primary da `idx_scan = 0` bo'lgan indeks replika da faol ishlatilayotgan bo'lishi mumkin. Qarorni hamma instansdan yig'ilgan ma'lumot bilan qabul qilish kerak.

Unique yoki constraint ortidagi indeksni va foreign key ustunidagi indeksni skanlanmagani uchun o'chirmang: birinchisi qoidani majburlaydi, ikkinchisi ota jadvaldagi `DELETE` ni tezlashtiradi. PostgreSQL da MySQL dagi "invisible index" yo'q, shuning uchun xavfsiz tekshiruv usuli `hypopg` kengaytmasi yoki tranzaksiya ichida `DROP INDEX` qilib, planni ko'rib, `ROLLBACK` qilish.

```sql
-- ishlatilmayotgan va katta indekslar
SELECT s.relname AS tbl, s.indexrelname AS idx, s.idx_scan,
       pg_size_pretty(pg_relation_size(s.indexrelid)) AS size
FROM pg_stat_user_indexes s
JOIN pg_index i ON i.indexrelid = s.indexrelid
WHERE s.idx_scan < 50
  AND NOT i.indisunique
  AND NOT i.indisprimary
  AND pg_relation_size(s.indexrelid) > 50 * 1024 * 1024
ORDER BY pg_relation_size(s.indexrelid) DESC;

-- statistika qachondan yig'ilgan
SELECT datname, stats_reset FROM pg_stat_database WHERE datname = current_database();

-- takrorlangan indekslar: bir xil ustun to'plami
SELECT indrelid::regclass AS tbl, count(*), array_agg(indexrelid::regclass)
FROM pg_index
GROUP BY indrelid, indkey
HAVING count(*) > 1;
```

### 23.11 `CREATE INDEX CONCURRENTLY` va ishlab chiqarishda indeks qo'shish

Oddiy `CREATE INDEX` jadvalga `SHARE` lock oladi va butun qurilish davomida `INSERT`, `UPDATE`, `DELETE` ni to'xtatadi. 80 million qatorli jadvalda bu bir necha daqiqa to'liq to'xtash degani. `CONCURRENTLY` esa `SHARE UPDATE EXCLUSIVE` lock bilan ishlaydi, DML ni to'xtatmaydi, lekin jadvalni ikki marta skanlaydi va taxminan ikki barobar uzoq davom etadi.

Ikki muhim cheklov bor. Birinchisi: `CONCURRENTLY` tranzaksiya blokida bajarilmaydi. Flyway har bir migratsiyani tranzaksiyada ishlatadi, shuning uchun bunday migratsiyani Java migratsiyasi sifatida yozib, `canExecuteInTransaction()` dan `false` qaytarish kerak. Liquibase da `runInTransaction="false"` atributi bor. Ikkinchisi: qurilish o'zidan oldin boshlangan hamma tranzaksiya tugashini kutadi, shuning uchun soatlab ochiq turgan analitik tranzaksiya indeks qurilishini cheksiz kechiktiradi.

Xato bo'lsa `CONCURRENTLY` jadvalda yaroqsiz indeks qoldiradi. U so'rovlarda ishlatilmaydi, lekin yozuv narxini oladi va vacuum ni sekinlashtiradi, shuning uchun uni topib o'chirish shart. Partition qilingan jadvalda ota jadval ustida `CONCURRENTLY` qo'llanmaydi: har bir partitionda alohida quriladi, keyin ota jadvalda `ONLY` bilan indeks yaratilib, `ATTACH PARTITION` orqali bog'lanadi.

```sql
-- qurishdan oldin uzun tranzaksiyalarni tekshirish
SELECT pid, now() - xact_start AS xact_age, left(query, 50)
FROM pg_stat_activity
WHERE now() - xact_start > interval '5 min';

-- quruvchi sessiya uchun resurs va navbat sozlamalari
SET maintenance_work_mem = '2GB';
SET max_parallel_maintenance_workers = 4;
SET lock_timeout = '5s';

CREATE INDEX CONCURRENTLY idx_orders_cust_created
    ON orders (customer_id, created_at DESC);

-- yaroqsiz qolgan indekslarni topish va tozalash
SELECT indexrelid::regclass FROM pg_index WHERE NOT indisvalid;
DROP INDEX CONCURRENTLY IF EXISTS idx_orders_cust_created;
```

### 23.12 Indeks shishishi va `REINDEX CONCURRENTLY`

B-tree indeks o'chirilgan qatorlarni darhol bo'shatmaydi: leaf sahifadagi joy faqat vacuum indeks yozuvini olib tashlagandan keyin qayta ishlatiladi. Tasodifiy kalit bo'yicha yozuv, masalan UUID v4 primary key, sahifa bo'linishlarini ko'paytiradi va indeksni parchalaydi. Shu sababli yangi loyihalarda vaqt bo'yicha o'sadigan kalit, ya'ni UUID v7 yoki ULID, yoki `bigserial` tanlanadi.

Shishishni taxmin qilmasdan o'lchash kerak. `pgstattuple` kengaytmasidagi `pgstatindex` funksiyasi `avg_leaf_density` va `leaf_fragmentation` qiymatlarini beradi. Sog'lom B-tree da leaf zichligi taxminan 70-90 foiz, 40 foizdan past qiymat qayta qurish vaqti kelganini ko'rsatadi.

`REINDEX CONCURRENTLY` PostgreSQL 12 dan beri mavjud va indeksni DML ni to'xtatmasdan qayta quradi. Uchta narsani hisobga olish kerak. Birinchisi: vaqtincha ikkinchi nusxa quriladi, demak disk da indeks hajmidan ko'proq bo'sh joy kerak. Ikkinchisi: xato bo'lsa `_ccnew` qo'shimchali yaroqsiz indeks qoladi va uni tozalash lozim. Uchinchisi: exclusion constraint ortidagi indeksni `CONCURRENTLY` qayta qurib bo'lmaydi, u uchun xizmat oynasi kerak. Append-only jadvalda `fillfactor = 100` qo'yish indeksni zichlashtiradi, tez-tez yangilanadigan jadvalda esa standart 90 qoldiriladi.

```sql
CREATE EXTENSION IF NOT EXISTS pgstattuple;

-- shishishni o'lchash: zichlik 40 foizdan past bo'lsa qayta qurish kerak
SELECT avg_leaf_density, leaf_fragmentation, index_size
FROM pgstatindex('idx_orders_cust_created');

-- DML ni to'xtatmasdan qayta qurish
REINDEX INDEX CONCURRENTLY idx_orders_cust_created;

-- yarim qolgan nusxalarni topish
SELECT indexrelid::regclass FROM pg_index
WHERE NOT indisvalid AND indexrelid::regclass::text LIKE '%_ccnew%';
```

| Tuzoq | Nima bo'ladi | Yechim |
|---|---|---|
| `INCLUDE` qo'yildi, lekin vacuum yo'q | Index-only scan ishlamaydi, `Heap Fetches` katta | Autovacuum ni agressivlashtirish, `Heap Fetches: 0` ni tekshirish |
| Qisman indeks sharti bind parameter bilan | Planner isbot tuzmaydi, indeks tashlanadi | Shartni literal yozish yoki turg'un chegara qo'yish |
| Tez o'zgaradigan ustunga indeks | HOT update buziladi, bloat o'sadi | Indeksni olib tashlash yoki ustunni alohida jadvalga chiqarish |
| BRIN uncorrelated ustunda | Deyarli butun jadval qayta tekshiriladi | `pg_stats.correlation` ni o'lchash, B-tree ga o'tish |
| GIN ga ommaviy `INSERT` | Pending list o'sadi, birinchi qidiruv sekin | `fastupdate = off` yoki `gin_pending_list_limit` ni kamaytirish |
| `CONCURRENTLY` uzun tranzaksiya paytida | Qurilish soatlab kutadi yoki uziladi | `pg_stat_activity` tekshiruvi, keyin qayta urinish |
| Yaroqsiz indeks e'tibordan chetda | Yozuv sekin, vacuum og'ir, foyda yo'q | `pg_index.indisvalid` monitoringi, `DROP INDEX CONCURRENTLY` |
| `idx_scan = 0` deb primary da o'chirildi | Replika dagi hisobot sekinlashadi | Hamma instansdan statistika yig'ish |
| UUID v4 primary key | Sahifa bo'linishi, indeks parchalanishi | UUID v7 yoki `bigserial` ga o'tish |

### 23.13 Amalda qo'llash

- [ ] Eng og'ir 10 so'rovni `pg_stat_statements` dan oling va har biriga `EXPLAIN (ANALYZE, BUFFERS)` yozib, `Heap Fetches` va `Rows Removed by Filter` qiymatlarini qayd qiling.
- [ ] Mijoz kabinetidagi ro'yxat so'rovi uchun ustunlar tartibini tekshirib, tenglik ustunini oldinga, `ORDER BY` ustunini oxiriga qo'ygan bitta indeks qoldiring.
- [ ] Navbat yoki status jadvalidagi to'liq indeksni qisman indeksga aylantirib, hajm va yozuv latency sidagi farqni o'lchang.
- [ ] `jsonb` ustunidagi hamma alohida ifoda indekslarini ko'rib chiqib, ularni bitta GIN indeksi bilan almashtirish mumkinligini sinab ko'ring.
- [ ] 100 GB dan katta append-only jadvalda `pg_stats.correlation` ni o'lchab, mos bo'lsa BRIN ga o'tish rejasini tuzing.
- [ ] `pg_stat_user_indexes` so'rovini primary va hamma replikada bajarib, nomzod keraksiz indekslar ro'yxatini tuzing va choraklik ko'rikka qo'ying.
- [ ] Migratsiya quvurida `CREATE INDEX CONCURRENTLY` ni tranzaksiyadan tashqarida ishlatish imkonini sozlab, yaroqsiz indeksni tekshiruvchi qadamni qo'shing.
- [ ] Eng katta uchta indeks uchun `pgstatindex` bilan leaf zichligini o'lchab, 40 foizdan past bo'lsa `REINDEX CONCURRENTLY` ni xizmat oynasiga rejalashtiring.

## 24. Planner, statistika va EXPLAIN ANALYZE o'qish (Planner and EXPLAIN ANALYZE)

PostgreSQL planner so'rovni qanday bajarishni o'zi tanlaydi va bu tanlov statistikaga asoslangan taxminlar ustiga qurilgan. Arxitektor uchun muhim narsa index qo'shish emas, balki planner nimaga ishonib shu rejani tanlaganini o'qib tushunish. `EXPLAIN (ANALYZE, BUFFERS)` chiqishi aynan shu ishonchni va haqiqatni yonma-yon ko'rsatadigan yagona vosita. Bu bobda planner mexanikasi, narx modeli, skan va join turlari, hamda sekin so'rovni tartib bilan tekshirish usuli ko'rib chiqiladi.

### 24.1 Planner nima qiladi: variantlar, narx modeli, tanlov

Parser SQL matnini daraxtga aylantiradi, rewriter view va rule'larni ochadi, keyin planner ishga tushadi. Planner bir xil natijani beradigan ko'plab jismoniy rejalarni generatsiya qiladi: har bir jadval uchun skan usuli, har bir juftlik uchun join algoritmi, join tartibi, agregatsiya va sort joyi. Har bir variantga narx beriladi va eng arzoni tanlanadi.

Narx birligi sekund emas, shartli son. Bazasi `seq_page_cost = 1.0`, ya'ni ketma-ket o'qilgan bitta 8 kB sahifa narxi. Qolgan hamma parametr shunga nisbatan o'lchanadi. Narx ikki qismdan: `startup cost` (birinchi qator chiqishidan oldingi ish) va `total cost` (barcha qatorlar). `LIMIT` bo'lsa planner total narxning faqat bir ulushini hisoblaydi, shuning uchun `LIMIT 20` bilan va `LIMIT` siz rejalar butunlay boshqacha bo'lishi mumkin.

Join tartibi uchun jadval soni 8 dan oshsa (`geqo_threshold`), to'liq dinamik programmalash o'rniga genetik algoritm ishlaydi va reja barqaror bo'lmay qoladi. 12 ta jadvalli hisobot so'rovi har deploy'dan keyin boshqa reja olishi mumkin, bu esa "kecha ishlagan, bugun ishlamaydi" muammosining tipik manbasi. Arxitektor qarori: katta hisobotni bir nechta bosqichga bo'lish yoki oldindan hisoblangan jadvaldan o'qish.

### 24.2 Statistika qayerdan keladi: `ANALYZE`, `pg_statistic`, `default_statistics_target`

Planner qator sonini jadvalni o'qib bilmaydi, u `pg_statistic` dagi namunaviy statistikaga qaraydi. Uni `ANALYZE` yig'adi: jadvaldan `300 * statistics_target` ta qator tasodifiy olinadi, ya'ni standart 100 da 30000 qator. Shu namunadan har bir ustun uchun null ulushi, o'rtacha kenglik, eng tez uchraydigan qiymatlar ro'yxati va histogram chegaralari saqlanadi.

Autovacuum o'z ichida autoanalyze ishlatadi va standart shart: o'zgargan qator soni jadval hajmining 10 foizidan oshsa. 50 million qatorli `orders` jadvalida bu 5 million qator degani, demak statistika kunlar davomida eskirgan holda qoladi. Katta jadvalda chegarani qo'lda pasaytirish kerak.

```sql
-- Namuna hajmini oshirish: notekis taqsimlangan ustunlar uchun
ALTER TABLE orders ALTER COLUMN status SET STATISTICS 500;
ALTER TABLE orders ALTER COLUMN customer_id SET STATISTICS 1000;
ANALYZE orders;              -- o'zgarish faqat ANALYZE dan keyin kuchga kiradi

-- Katta jadvalda autoanalyze tezroq ishlashi uchun
ALTER TABLE orders SET (
  autovacuum_analyze_scale_factor = 0.02,   -- 10% emas, 2%
  autovacuum_analyze_threshold = 50000
);

-- Statistika haqiqatan yangilanganini tekshirish
SELECT relname, last_analyze, last_autoanalyze, n_mod_since_analyze
FROM pg_stat_user_tables
WHERE relname IN ('orders', 'payments', 'stock_items');
```

`default_statistics_target` ni global 100 dan 200 ga oshirish OLTP bazada odatda xavfsiz, lekin `ANALYZE` vaqti va planner ishi ham ortadi. Amaliy qoida: global qiymatni tegmay, muammoli ustunga alohida target berish.

### 24.3 Narx parametrlari: `random_page_cost`, `seq_page_cost`, `effective_cache_size` ma'nosi

`random_page_cost` standart 4.0, bu aylanuvchi diskdan tasodifiy o'qish ketma-ket o'qishdan to'rt baravar qimmat degan taxmin. SSD va NVMe da bu nisbat haqiqatda 1.1 dan 1.5 gacha. Standart qiymatni qoldirish planner'ni index scan'dan qo'rqitadi va u seq scan tanlaydi.

`effective_cache_size` hech qanday xotira ajratmaydi, u faqat planner'ga "operatsion tizim page cache va shared_buffers birgalikda taxminan shuncha ma'lumotni ushlab turadi" deb aytadi. Qiymati kichik bo'lsa planner index scan'da har safar diskka borishni taxmin qiladi va uni qimmat deb baholaydi.

```sql
-- 64 GB RAM li SSD serveri uchun tipik boshlang'ich qiymatlar
ALTER SYSTEM SET random_page_cost = 1.1;        -- SSD uchun
ALTER SYSTEM SET effective_cache_size = '48GB'; -- RAM ning ~75%
ALTER SYSTEM SET effective_io_concurrency = 200;-- NVMe uchun
ALTER SYSTEM SET work_mem = '32MB';             -- har bir sort/hash uchun
SELECT pg_reload_conf();

-- Bitta so'rovni sinash uchun sessiya darajasida
SET LOCAL random_page_cost = 1.1;
EXPLAIN (ANALYZE, BUFFERS) SELECT ...;
```

`work_mem` eng xavfli parametr. U har bir sort, hash va hashagg uchun alohida ajratiladi, demak bitta so'rov 5 ta hash node bilan 5 * work_mem gacha xotira olishi mumkin. 200 ulanishli pool'da global 256MB qo'yish OOM ga olib keladi. Arxitektor yondashuvi: global 32MB, hisobot so'rovidan oldin `SET LOCAL work_mem = '256MB'`.

### 24.4 Skan turlari: sequential, index, index-only, bitmap heap scan

Sequential scan butun jadvalni ketma-ket o'qiydi. Jadval kichik bo'lsa yoki natijaga qatorlarning 10 foizidan ko'pi tushsa, bu eng arzon usul. Seq scan rejada ko'rinishi avtomatik muammo degani emas.

Index scan indeksni aylanib, har bir topilgan qator uchun heap'ga boradi. Tanlovchanlik yuqori bo'lganda (masalan `order_id = ?`) ideal. Index-only scan heap'ga bormaydi, chunki kerakli hamma ustun indeksda bor va sahifa visibility map'da "butunlay ko'rinadigan" deb belgilangan. `VACUUM` ishlamasa visibility map eskiradi va index-only scan ham heap fetch qilishga tushadi.

Bitmap heap scan ikki bosqichli: avval indeksdan mos qatorlarning sahifa bitmap'i quriladi, keyin heap jismoniy tartibda o'qiladi. Bu bir necha ming qator qaytaradigan so'rovlar uchun eng samarali usul, chunki tasodifiy o'qish ketma-ket o'qishga aylanadi. `Heap Blocks: exact=... lossy=...` satrida `lossy` ko'rinsa, bitmap `work_mem` ga sig'magan va sahifa darajasiga qo'pollashgan, natijada ortiqcha qator filtrlanadi.

### 24.5 Join algoritmlari: nested loop, hash join, merge join va qachon qaysi biri tanlanadi

Nested loop tashqi qatorning har biri uchun ichki tomonni qayta izlaydi. Ichki tomonda index bo'lsa va tashqi tomon kichik bo'lsa, bu eng tez va eng kam xotira talab qiladigan usul. Xatar: tashqi qator soni noto'g'ri taxmin qilinsa, 50 ta `loops` o'rniga 500000 ta `loops` bo'ladi va so'rov 1000 baravar sekinlashadi. Deyarli barcha "kutilmaganda sekinlashgan so'rov" hodisasi shu.

Hash join kichik tomondan xotirada hash jadval quradi, keyin katta tomonni bir marta o'tadi. Katta to'plamlarni tenglik shartida birlashtirish uchun eng yaxshi tanlov. Hash `work_mem` ga sig'masa `Batches` soni 1 dan oshadi va diskka to'kiladi, bu esa `temp read/written` bloklarida ko'rinadi.

Merge join ikki tomonni sortlangan holda parallel o'qiydi. Ikkala tomonda ham mos indeks bo'lsa yoki ma'lumot allaqachon sortlangan bo'lsa arzon, aks holda sort narxi qo'shiladi. Katta hisobotlarda `ORDER BY` bilan birga foydali.

| Holat | Planner tanlovi | Nega |
| --- | --- | --- |
| Tashqi tomon 10 qator, ichkida index | Nested loop | Har bir qidiruv arzon, startup cost nol |
| 2 mln va 500 ming qator, tenglik sharti | Hash join | Bitta o'tish, xotirada hash |
| Ikkala tomon sortlangan, `ORDER BY` bor | Merge join | Sort qayta kerak emas |
| Tenglik emas, `BETWEEN` sharti | Nested loop yoki merge | Hash faqat tenglikni biladi |
| Hash `work_mem` ga sig'maydi | Batched hash join | Diskka to'kilish, sekinlashadi |

### 24.6 `EXPLAIN (ANALYZE, BUFFERS)` chiqishini satrma-satr o'qish

Mijozning oxirgi buyurtmalarini to'lov summasi bilan ko'rsatadigan so'rov. `ANALYZE` so'rovni haqiqatan bajaradi, shuning uchun `UPDATE` yoki `DELETE` ni tekshirganda tranzaksiya ochib, oxirida `ROLLBACK` qilish kerak.

```sql
EXPLAIN (ANALYZE, BUFFERS)
SELECT o.id, o.created_at, p.amount
FROM orders o
JOIN payments p ON p.order_id = o.id
WHERE o.customer_id = 48213
  AND o.created_at >= DATE '2026-09-01'
ORDER BY o.created_at DESC
LIMIT 20;
```

Chiqish quyidagicha bo'ldi:

```text
Limit  (cost=1042.18..1042.23 rows=20 width=28)
       (actual time=318.442..318.449 rows=20 loops=1)
  Buffers: shared hit=812 read=9134
  ->  Sort  (cost=1042.18..1044.90 rows=1088 width=28)
            (actual time=318.440..318.444 rows=20 loops=1)
        Sort Key: o.created_at DESC
        Sort Method: top-N heapsort  Memory: 27kB
        ->  Nested Loop  (cost=0.43..1010.55 rows=1088 width=28)
                         (actual time=0.071..317.902 rows=1042 loops=1)
              Buffers: shared hit=812 read=9134
              ->  Seq Scan on orders o  (cost=0.00..98211.00 rows=54 width=16)
                                        (actual time=0.028..290.114 rows=1007 loops=1)
                    Filter: ((customer_id = 48213)
                             AND (created_at >= '2026-09-01'::date))
                    Rows Removed by Filter: 4198993
              ->  Index Scan using payments_order_id_idx on payments p
                    (cost=0.43..8.45 rows=1 width=20)
                    (actual time=0.023..0.025 rows=1 loops=1007)
                    Index Cond: (order_id = o.id)
Planning Time: 0.214 ms
Execution Time: 318.507 ms
```

Satrlarni ketma-ket o'qiymiz. Eng ichki node birinchi bajariladi, ya'ni pastdan yuqoriga.

`Seq Scan on orders` satri: planner 54 qator kutgan, haqiqatda 1007 qator qaytgan. `Rows Removed by Filter: 4198993` degani jadvalning 4.2 million qatori o'qilib tashlangan. `cost=0.00..98211.00` lekin `LIMIT` borligi uchun to'liq narx hisobga olinmagan. Bu yerdagi 290 ms butun so'rov vaqtining asosiy qismi.

`Index Scan using payments_order_id_idx` satri: `loops=1007`, ya'ni bu node 1007 marta ishga tushgan. Har safar 0.025 ms, umumiy taxminan 25 ms. `actual time` har doim bitta loop uchun o'rtacha qiymat, umumiy vaqtni olish uchun `loops` ga ko'paytirish kerak. Bu eng ko'p yanglishtiradigan joy.

`Nested Loop` satri: 1042 qator chiqargan, 317 ms. Planner 1088 kutgan, bu yaqin. Demak muammo join algoritmida emas.

`Sort` satri: `top-N heapsort  Memory: 27kB`. `LIMIT 20` borligi uchun to'liq sort emas, faqat 20 ta eng kattasi ushlab turilgan. Xotira `work_mem` ga sig'gan, `Disk` so'zi yo'q, demak to'kilish bo'lmagan.

`Buffers: shared hit=812 read=9134` satri: 812 sahifa `shared_buffers` dan olingan, 9134 sahifa cache'da bo'lmagan. 9134 * 8 kB taxminan 71 MB o'qish. Bu `read` soni `hit` dan 11 baravar katta, demak jadval cache'ga sig'mayapti.

`Planning Time: 0.214 ms` reja tuzish vaqti. U `Execution Time` ga yaqinlashsa, ko'p partition yoki ko'p join bor degani.

Tuzatish aniq: `orders(customer_id, created_at DESC)` composite indeksi. Undan keyin seq scan index scan'ga aylanadi va `read` soni yuzlab sahifaga tushadi.

### 24.7 Taxmin qilingan va haqiqiy qator soni farqi: eng muhim signal

Rejada birinchi qaraladigan narsa `rows=N` (taxmin) va `actual rows=M` nisbati. 10 baravardan katta farq planner yomon statistika bilan ishlaganini bildiradi. Yuqoridagi misolda 54 va 1007, ya'ni 18 baravar. Agar tashqi tomonda shunday farq bo'lsa, planner nested loop'ni arzon deb hisoblaydi va u aslida qimmat chiqadi.

Farqning tipik sabablari: eskirgan statistika, bog'liq ustunlar, `LIKE '%...'` shabloni, funksiya ustidagi filtr (`lower(email) = ?`) va ifodaga statistika yo'qligi. Oxirgisining yechimi ifoda uchun index yaratish, chunki ifoda indeksi o'zi bilan statistika ham olib keladi.

| Oddiy yondashuv | Arxitektor yondashuvi |
| --- | --- |
| Sekin so'rovga darhol index qo'shadi | Avval `EXPLAIN (ANALYZE, BUFFERS)` o'qib, qaysi node vaqt yegani aniqlanadi |
| `cost` raqamini millisekund deb o'ylaydi | `cost` shartli birlik, qaror `actual time` va `Buffers` bo'yicha |
| `loops` ni e'tiborsiz qoldiradi | `actual time` ni `loops` ga ko'paytirib haqiqiy ulushni hisoblaydi |
| Seq scan ko'rsa darhol muammo deb biladi | Tanlovchanlikni tekshiradi, 30% natijada seq scan to'g'ri |
| Index sonini oshirib boradi | Har bir index `INSERT` narxi va WAL hajmini oshirishini hisobga oladi |
| `enable_nestloop = off` bilan planner'ni majburlaydi | Statistika va `CREATE STATISTICS` bilan taxminni to'g'rilaydi |
| Prod'da `work_mem` ni global oshiradi | Global kichik qoldirib, hisobot sessiyasida `SET LOCAL` qiladi |
| Faqat o'z lokal bazasida sinaydi | Prod hajmiga yaqin ma'lumotda sinaydi, chunki reja hajmga bog'liq |
| `pg_stat_statements` ga qaramaydi | Eng qimmat 20 so'rovni `total_exec_time` bo'yicha tartiblaydi |
| Bir marta tuzatib yopadi | Reja regressiyasini monitoringga qo'yadi |

### 24.8 Ko'p ustunli statistika (`CREATE STATISTICS`) va bog'liq ustunlar muammosi

Planner standart holda ustunlarni mustaqil deb hisoblaydi va shartlar tanlovchanligini ko'paytiradi. `city = 'Toshkent' AND region = 'Toshkent'` da haqiqatda bitta shart, lekin planner ikkitasini ko'paytirib qator sonini bir necha baravar kam ko'rsatadi. Natijada hash join o'rniga nested loop tanlanadi.

```sql
-- Bog'liq ustunlar uchun kengaytirilgan statistika
CREATE STATISTICS stat_orders_city_region (dependencies, ndistinct)
  ON city, region FROM orders;

-- MCV ro'yxati bilan: qiymat juftliklarining chastotasi saqlanadi
CREATE STATISTICS stat_orders_status_channel (mcv)
  ON status, channel FROM orders;

ANALYZE orders;   -- statistika obyekti ANALYZE dan keyin to'ladi

SELECT s.stxname, d.stxdndistinct, d.stxddependencies
FROM pg_statistic_ext s
JOIN pg_statistic_ext_data d ON d.stxoid = s.oid;
```

`dependencies` funksional bog'liqlikni, `ndistinct` birlashgan unikal qiymat sonini, `mcv` esa eng ko'p uchraydigan juftliklarni saqlaydi. `GROUP BY` ikki ustun bo'yicha bo'lsa `ndistinct` hashagg xotirasini to'g'ri taxmin qilishga yordam beradi.

### 24.9 Parametrlashtirilgan so'rov va generic plan muammosi (`plan_cache_mode`)

Hibernate va JDBC `PreparedStatement` ishlatadi. PostgreSQL bir xil prepared statement bir necha marta bajarilganda custom plan (har safar parametr qiymati bilan) va generic plan (parametrsiz, o'rtacha tanlovchanlik) narxini taqqoslaydi. Beshinchi bajarilishdan keyin generic plan arzon ko'rinsa, unga o'tadi.

Muammo notekis taqsimlangan ustunda chiqadi. `status = 'NEW'` da 500 qator, `status = 'DONE'` da 40 million qator. Generic plan o'rtacha qiymat bilan tuzilgani uchun ikkisining birida juda yomon ishlaydi. Belgisi: so'rov bir necha marta tez ishlaydi, keyin birdan sekinlashadi.

```properties
# Spring Boot: ulanish ochilganda sessiya sozlamasi
spring.datasource.hikari.connection-init-sql=SET plan_cache_mode = force_custom_plan

# PgJDBC: server-side prepare chegarasi (0 bo'lsa server prepare o'chadi)
spring.datasource.hikari.data-source-properties.prepareThreshold=5

# Pool o'lchami: CPU yadrosi * 2 + disk soni, 200 emas
spring.datasource.hikari.maximum-pool-size=20
```

`force_custom_plan` har safar reja tuzadi, bu taxminan 0.2 dan 1 ms qo'shimcha xarajat. OLTP da sekundda minglab so'rov bo'lsa bu sezilarli, shuning uchun uni global emas, muammoli so'rov uchun alohida qo'llash kerak. Alternativa: shu so'rovni native query qilib, qiymatni literal sifatida qo'yish yoki `status` bo'yicha partial index yaratish.

### 24.10 `pg_stat_statements` bilan eng qimmat so'rovlarni topish

`pg_stat_statements` normalizatsiya qilingan so'rovlar bo'yicha chaqirish soni va vaqtni to'playdi. Uni `shared_preload_libraries` ga qo'shish kerak va server restart talab qiladi.

```sql
-- Umumiy vaqt bo'yicha eng qimmat 15 so'rov
SELECT substr(query, 1, 80) AS q,
       calls,
       round(total_exec_time::numeric, 1) AS total_ms,
       round(mean_exec_time::numeric, 2) AS mean_ms,
       rows / GREATEST(calls, 1) AS rows_per_call,
       round(100.0 * shared_blks_hit
             / GREATEST(shared_blks_hit + shared_blks_read, 1), 1) AS hit_pct
FROM pg_stat_statements
WHERE query NOT LIKE '%pg_stat_statements%'
ORDER BY total_exec_time DESC
LIMIT 15;

SELECT pg_stat_statements_reset();  -- deploy oldidan nolga qaytarish
```

Eng muhim tartiblash `mean_exec_time` emas, `total_exec_time`. 0.8 ms ishlaydigan lekin sekundda 5000 marta chaqirilgan so'rov 400 ms ishlaydigan kunlik hisobotdan ko'proq resurs yeydi. `rows_per_call` 1 ga teng va `calls` juda katta bo'lsa, bu Hibernate N+1 muammosining aniq izi.

`auto_explain` moduli chegaradan sekin so'rovlarning rejasini logga yozadi, bu prod'da qayta takrorlanmaydigan sekinlashishni tutish uchun yagona ishonchli yo'l.

```bash
# Logda 500 ms dan sekin so'rovlarning rejasi, namuna olish bilan
psql -c "ALTER SYSTEM SET auto_explain.log_min_duration = '500ms'"
psql -c "ALTER SYSTEM SET auto_explain.log_analyze = on"
psql -c "ALTER SYSTEM SET auto_explain.log_buffers = on"
psql -c "ALTER SYSTEM SET auto_explain.sample_rate = 0.1"   # 10% namuna
psql -c "SELECT pg_reload_conf()"

# Jadval va index hajmini ko'rish
psql -c "SELECT relname, pg_size_pretty(pg_total_relation_size(oid))
         FROM pg_class WHERE relkind='r' ORDER BY pg_total_relation_size(oid) DESC LIMIT 10"
```

### 24.11 So'rovni qayta yozish: `EXISTS`, `LATERAL`, `DISTINCT ON`, CTE va materializatsiya

Ko'pincha index emas, so'rov shakli muammo. `IN (SELECT ...)` o'rniga `EXISTS` ishlatish planner'ga semi-join imkonini beradi va birinchi mos qator topilgach ichki qidiruv to'xtaydi. `LATERAL` har bir tashqi qator uchun "eng oxirgi N ta" ni olishga imkon beradi, bu window funksiya ustidan filtrlashdan arzonroq. `DISTINCT ON` esa guruh ichidan birinchi qatorni olishning eng qisqa va tez usuli.

```sql
-- Har bir mijozning oxirgi 3 to'lovi: LATERAL
SELECT c.id, p.paid_at, p.amount
FROM customers c
CROSS JOIN LATERAL (
    SELECT paid_at, amount FROM payments
    WHERE customer_id = c.id ORDER BY paid_at DESC LIMIT 3
) p
WHERE c.segment = 'B2B';

-- Har bir buyurtmaning oxirgi holati: DISTINCT ON
SELECT DISTINCT ON (order_id) order_id, status, changed_at
FROM order_status_log ORDER BY order_id, changed_at DESC;

-- To'lovi bor buyurtmalar: EXISTS, semi-join
SELECT o.id FROM orders o
WHERE EXISTS (SELECT 1 FROM payments p WHERE p.order_id = o.id AND p.amount > 0);
```

PostgreSQL 12 dan boshlab oddiy CTE inline qilinadi, ya'ni planner uni asosiy so'rov bilan birga optimallashtiradi. `MATERIALIZED` kalit so'zi bilan CTE bir marta hisoblanib vaqtinchalik natijaga yoziladi. Bu CTE bir necha joyda ishlatilganda yoki og'ir agregatsiya bo'lganda foydali, lekin filtr CTE ichiga tushmaydi. Qaror oddiy: bir marta ishlatiladigan va filtr tushishi kerak bo'lgan CTE uchun `NOT MATERIALIZED`, qayta ishlatiladigan og'ir hisob uchun `MATERIALIZED`.

```java
// Hisobot so'rovi uchun sessiya darajasida sozlash va stream o'qish
@Transactional(readOnly = true)
public void exportDailyReport(LocalDate day, Consumer<ReportRow> sink) {
    em.createNativeQuery("SET LOCAL work_mem = '256MB'").executeUpdate();
    var q = em.createQuery(REPORT_JPQL, ReportRow.class)
              .setParameter("day", day)
              .setHint(AvailableHints.HINT_FETCH_SIZE, 500); // kursor bilan o'qish
    try (Stream<ReportRow> rows = q.getResultStream()) {
        rows.forEach(sink);   // hamma natija xotiraga yig'ilmaydi
    }
}
```

| Tuzoq | Belgisi rejada | Yechim |
| --- | --- | --- |
| Noto'g'ri nested loop | `loops` juda katta, tashqi `rows` taxmini past | Statistikani yangilash, composite index |
| Hash diskka to'kilgan | `Batches > 1`, `temp written` | Shu so'rov uchun `work_mem` oshirish |
| Funksiya ustidagi filtr | `Filter` da `lower(...)`, seq scan | Ifoda indeksi yaratish |
| Bog'liq ustunlar | Ikki shartda taxmin 10 baravar past | `CREATE STATISTICS` |
| Generic plan regressiyasi | Beshinchi chaqiruvdan keyin sekinlashish | `force_custom_plan` yoki partial index |
| Index-only scan ishlamaydi | `Heap Fetches` katta | `VACUUM`, visibility map yangilash |
| `lossy` bitmap | `Heap Blocks: lossy=...` | `work_mem` oshirish yoki shartni aniqlashtirish |
| Reja tuzish sekin | `Planning Time` ijro vaqtiga yaqin | Partition sonini kamaytirish, index sonini qisqartirish |

### 24.12 Sekin so'rovni tekshirish tartibi: aniq qadamlar ro'yxati

Tartib muhim, chunki har bir qadam keyingisini kerak qilmasligi mumkin. Birinchi navbatda so'rov haqiqatan sekinmi yoki ulanish kutishidami aniqlanadi: `pg_stat_activity` dagi `wait_event_type` buni ko'rsatadi. Keyin `pg_stat_statements` dan shu so'rovning umumiy ulushi olinadi, chunki bir marta sekin ishlagan so'rov ustida ishlash vaqtni behuda sarflash.

Undan keyin `EXPLAIN (ANALYZE, BUFFERS)` olinadi va eng ko'p `actual time` yegan node topiladi. Shu node'da taxmin va haqiqat farqi tekshiriladi. Farq katta bo'lsa yechim statistika tomonda, farq kichik va vaqt haliyam katta bo'lsa yechim index yoki so'rov shakli tomonda. `Buffers` dagi `read` ulushi yuqori bo'lsa muammo I/O da, `hit` yuqori bo'lsa muammo CPU va qator sonida.

Oxirida o'zgarish prod hajmiga yaqin ma'lumotda sinaladi, chunki 10 ming qatorli lokal bazada reja butunlay boshqacha bo'ladi. Index qo'shilsa `CREATE INDEX CONCURRENTLY` ishlatiladi va `pg_stat_user_indexes` orqali u haqiqatan ishlatilayotgani bir hafta kuzatiladi.

### 24.13 Amalda qo'llash

- [ ] Eng og'ir 20 so'rovni `pg_stat_statements` dan `total_exec_time` bo'yicha chiqarib, ularning har biri uchun `EXPLAIN (ANALYZE, BUFFERS)` rejasini saqlab qo'y.
- [ ] Har bir rejada taxmin va haqiqiy qator sonini taqqoslab, 10 baravardan ortiq farq bo'lgan node'lar ro'yxatini tuz.
- [ ] SSD serverlarda `random_page_cost` ni 1.1 ga, `effective_cache_size` ni RAM ning 75 foiziga keltir va o'zgarishdan oldin va keyin rejalarni taqqoslab yoz.
- [ ] 10 million qatordan katta jadvallarga `autovacuum_analyze_scale_factor = 0.02` qo'yib, `pg_stat_user_tables` dagi `last_autoanalyze` ni haftada bir tekshir.
- [ ] Birgalikda filtrlanadigan bog'liq ustun juftliklarini aniqlab, ularga `CREATE STATISTICS` yaratib `ANALYZE` ishlatib natijani tasdiqla.
- [ ] `auto_explain` ni `log_min_duration = 500ms` va `sample_rate = 0.1` bilan yoqib, log'dan haftalik sekin reja hisobotini chiqar.
- [ ] Notekis taqsimlangan ustun bo'yicha filtrlaydigan prepared statement'larni topib, generic plan regressiyasini sinab ko'r va kerak bo'lsa partial index yoki `force_custom_plan` qo'lla.
- [ ] `work_mem` ni global 32MB da qoldirib, hisobot va eksport yo'llarida `SET LOCAL` bilan oshirishni kod darajasida standartlashtir.

## 25. Sxema dizayni, ma'lumot turlari va cheklovlar (Schema Design and Data Types)

Sxema ilovaning eng uzoq yashaydigan qismi. Java kodi har yili qayta yoziladi, Spring versiyasi almashadi, lekin `orders` jadvalidagi ustun turi besh yildan keyin ham shu yerda turadi. Noto'g'ri tanlangan tur yoki yozilmagan cheklov keyinchalik yuz minglab qatorni migratsiya qilish narxini keltiradi. Shuning uchun arxitektor tur tanlashni detal deb emas, uzoq muddatli majburiyat deb ko'radi.

### 25.1 Turni to'g'ri tanlash: `text`, `varchar`, `numeric`, `timestamptz`, `uuid`, `boolean`

PostgreSQL da `text` va `varchar(n)` bir xil ichki formatdan foydalanadi: `varlena` strukturasi, ya'ni 1 yoki 4 baytli uzunlik sarlavhasi va ma'lumotning o'zi. `varchar(n)` faqat qo'shimcha uzunlik tekshiruvini qo'shadi, tezlikda hech qanday foyda bermaydi. Uzunlik biznes qoidasi bo'lsa `CHECK` qo'ying, aks holda `text` ishlating. `char(n)` ni umuman ishlatmang, u qiymatni bo'sh joy bilan to'ldiradi va taqqoslashda kutilmagan natija beradi.

Suzuvchi nuqta turlari pulga yaramaydi. `double precision` IEEE 754 ikkilik formati, `0.1` ni aniq saqlay olmaydi. `numeric` o'nlik raqamlarni guruhlab saqlaydi va aniq arifmetika beradi, lekin taxminan 10-50 marta sekinroq.

| Noto'g'ri tur | To'g'ri tur | Sabab |
| --- | --- | --- |
| `double precision` pul uchun | `numeric(19,4)` | ikkilik yaxlitlash hisobotni buzadi |
| `varchar(255)` har joyda | `text` + `CHECK (length(x) <= 200)` | 255 raqami biznesdan emas |
| `timestamp` (zonasiz) | `timestamptz` | zonasiz tur momentni emas, matnni saqlaydi |
| `char(36)` UUID uchun | `uuid` | 16 bayt o'rniga 37 bayt va sekin taqqoslash |
| `smallint` status kodi | `text` + `CHECK IN (...)` | raqamli kod SQL ni o'qilmas qiladi |
| `integer` tiyin uchun | `bigint` | 2.1 mlrd tiyin juda kichik chegara |
| `text` sana uchun | `date` yoki `timestamptz` | matn sana arifmetikasini buzadi |
| `boolean` uch holat uchun | `text` + `CHECK` | `NULL` ni holat qilish xato manbai |
| `json` | `jsonb` | `json` matn sifatida saqlanadi, indekslanmaydi |
| `serial` | `bigint GENERATED BY DEFAULT AS IDENTITY` | `serial` standart emas, huquqlari chalkash |

`is_active` kabi ustun `NOT NULL DEFAULT true` bo'lishi shart, aks holda kod har joyda uch holatni tekshiradi.

### 25.2 Pul qiymatini saqlash: `numeric` va butun son yondashuvi

Pul uchun ikki to'g'ri yo'l bor. Birinchisi `numeric(19,4)`: o'qilishi oson, SQL da `SUM` tabiiy ishlaydi, Java tomonida `BigDecimal` ga tushadi. Ikkinchisi eng kichik birlikda `bigint`: tiyin yoki sent. Bu tezroq va aniq, lekin har bir o'qish va yozishda bo'lish kerak.

Qoida: hisob-kitob ko'p bo'lgan OLTP to'lov yo'lida `bigint` minor unit, hisobot qatlamida `numeric`. Valyuta kodi doim alohida ustunda.

```sql
CREATE TABLE payment (
    id              bigint GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
    order_id        bigint NOT NULL REFERENCES orders(id),
    -- summa tiyinda, hech qachon suzuvchi nuqta emas
    amount_minor    bigint NOT NULL CHECK (amount_minor > 0),
    currency        char(3) NOT NULL CHECK (currency ~ '^[A-Z]{3}$'),
    fee_minor       bigint NOT NULL DEFAULT 0 CHECK (fee_minor >= 0),
    captured_at     timestamptz,
    CONSTRAINT fee_le_amount CHECK (fee_minor <= amount_minor)
);

-- Bo'lish faqat bitta joyda: ko'rinish ichida
CREATE VIEW payment_report AS
SELECT id, order_id, (amount_minor::numeric / 100) AS amount, currency
FROM payment;
```

Java tomonida `BigDecimal` bilan ishlasangiz, `setScale` va `divide` ni har doim aniq `RoundingMode` bilan chaqiring. Standart rejim yo'q, aks holda `ArithmeticException` tashlanadi.

```java
// Komissiya: yaxlitlash qoidasi aniq ko'rsatilgan
public long feeMinor(long amountMinor, BigDecimal ratePercent) {
    return BigDecimal.valueOf(amountMinor)
            .multiply(ratePercent)
            .divide(BigDecimal.valueOf(100), 0, RoundingMode.HALF_UP)
            .longValueExact(); // overflow bo'lsa darhol xato
}
```

### 25.3 Vaqtni saqlash: `timestamptz` va vaqt mintaqasi masalasi

`timestamptz` nomi chalg'ituvchi. U vaqt mintaqasini saqlamaydi. Kiruvchi qiymatni sessiya zonasiga qarab UTC ga aylantiradi, 8 baytda UTC mikrosekund sifatida saqlaydi, o'qishda yana sessiya zonasiga qaytaradi. Ya'ni `timestamptz` momentni saqlaydi.

`timestamp` esa shunchaki devordagi soat raqami. Ikki server turli zonada bo'lsa, bir xil qiymat turli momentni anglatadi. Bu to'lov hisobotida ikki marta hisoblashga olib keladi.

Qoida: sodir bo'lgan voqea vaqti doim `timestamptz`. Shartnoma amal qilish sanasi `date`. Foydalanuvchi tanlagan "ertalab 9 da eslatma" esa `time` plus alohida zona identifikatori (`Europe/Tashkent`).

```sql
-- Oraliq filtri: yarim ochiq interval, DATE() funksiyasi emas
CREATE INDEX idx_payment_captured ON payment (captured_at);

SELECT count(*) FROM payment
WHERE captured_at >= '2026-03-01T00:00:00Z'
  AND captured_at <  '2026-04-01T00:00:00Z';   -- indeks ishlaydi

-- Bu versiya indeksni ishlatmaydi va zonaga bog'liq
-- WHERE date(captured_at) BETWEEN '2026-03-01' AND '2026-03-31';
```

Java 17+ da `timestamptz` ni `OffsetDateTime` yoki `Instant` ga map qiling. `LocalDateTime` ishlatsangiz, drayver JVM standart zonasini qo'shadi va konteyner zonasi o'zgarganda ma'lumot siljiydi. `spring.jpa.properties.hibernate.jdbc.time_zone=UTC` barcha node'ni bitta zonaga qotiradi.

### 25.4 Birlamchi kalit tanlovi: `bigint` ketma-ketlik, UUIDv4 va UUIDv7 taqqoslashi

`bigint` identity 8 bayt, ketma-ket o'sadi, B-tree indeksga doim o'ng chetdan yoziladi. Bu eng yuqori insert tezligini va eng zich indeksni beradi. Kamchiligi: qiymat global emas, sharding va ID ni bazadan oldin yaratish qiyin.

UUIDv4 16 bayt va butunlay tasodifiy. Tasodifiylik har insertni boshqa sahifaga yuboradi. Jadval kattalashganda ishchi to'plam cache ga sig'maydi va sahifalar bo'linib ketadi. Taxminan 50 mln qatorlik jadvalda UUIDv4 insert tezligi `bigint` dan 2-4 baravar past, indeks hajmi 30-60 foizga katta bo'lishi odatiy.

UUIDv7 birinchi 48 bitda Unix millisekundni saqlaydi. Qiymat vaqt bo'yicha o'sadi, insert lokalligi `bigint` ga yaqinlashadi, ammo global unikal bo'lib qoladi. PostgreSQL 18 da `uuidv7()` funksiyasi bor; 15-17 da uni ilovada generatsiya qilish kerak.

```sql
-- UUID kalit: qiymatni ilova beradi, baza faqat saqlaydi
CREATE TABLE shipment (
    id          uuid PRIMARY KEY,          -- UUIDv7
    order_id    bigint NOT NULL REFERENCES orders(id),
    created_at  timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE orders (
    id          bigint GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
    -- tashqi dunyo ko'radigan kod kalit emas, alohida unikal ustun
    public_code text   NOT NULL UNIQUE,
    customer_id bigint NOT NULL REFERENCES customer(id),
    status      text   NOT NULL,
    created_at  timestamptz NOT NULL DEFAULT now()
);
```

Qaror: ichki va yuqori hajmli jadvallar uchun `bigint` identity. Ko'p servis bir xil obyektni yaratadigan joyda UUIDv7. UUIDv4 ni faqat tashqi ko'rinadigan token uchun qoldiring, kalit sifatida emas.

### 25.5 Cheklovlar ma'lumotlar bazasida bo'lishi kerakligi: `NOT NULL`, `CHECK`, `UNIQUE`, tashqi kalit

Cheklov bazada bo'lishi kerakligining sababi oddiy: bazaga faqat sizning Spring ilovangiz yozmaydi. Migratsiya skripti, qo'lda `psql` tuzatishi, analitik ETL, eski versiyadagi pod, hammasi bir xil jadvalga yozadi. `NOT NULL` planner uchun ham muhim, u `NULL` tekshiruvini olib tashlaydi va statistikani aniqlashtiradi.

```sql
-- Ombor qoldig'i manfiy bo'lmasligi
ALTER TABLE stock_balance
    ADD CONSTRAINT qty_non_negative CHECK (quantity >= 0);

-- Bitta mijozda faqat bitta faol obuna
CREATE UNIQUE INDEX uq_active_subscription
    ON subscription (customer_id) WHERE status = 'ACTIVE';

-- Takroriy to'lov so'rovini baza o'zi rad etadi
ALTER TABLE payment
    ADD CONSTRAINT uq_payment_idempotency UNIQUE (idempotency_key);

-- Tashqi kalit va bola tomondagi indeks birga qo'yiladi
ALTER TABLE order_line
    ADD CONSTRAINT fk_line_order FOREIGN KEY (order_id)
    REFERENCES orders(id) ON DELETE CASCADE;
CREATE INDEX idx_order_line_order ON order_line (order_id);
```

Tashqi kalitni tezlik uchun olib tashlash keng tarqalgan xato. FK tekshiruvi ota jadvalda bitta indeks qidiruvi, taxminan 10-50 mikrosekund. Buning o'rniga olinadigan yetim qatorlarni tozalash haftalar oladi. Muhimi: FK ning bola ustuniga indeks avtomatik yaratilmaydi, `ON DELETE CASCADE` esa indekssiz holatda to'liq skan qiladi.

Bean Validation foydalanuvchiga tushunarli xato beradi, baza cheklovi esa oxirgi himoya chizig'i. Ikkisi bir-birini almashtirmaydi.

### 25.6 `jsonb` qachon to'g'ri tanlov va qachon dangasalik belgisi

`jsonb` matnni parse qilib ikkilik daraxt sifatida saqlaydi: kalitlar saralanadi, `->>` va `@>` tez ishlaydi, GIN indeks qo'yish mumkin. Lekin tur sxemasiz, ichidagi maydonga `NOT NULL` qo'yish qiyin va statistika juda qo'pol.

To'g'ri tanlov: tashqi to'lov gateway'i javobini o'zgartirmasdan saqlash, webhook arxivi, mahsulot turiga qarab o'zgaradigan xususiyatlar. Dangasalik belgisi: ustun qiymati bo'yicha `JOIN`, agregat yoki biznes qoida tekshiruvi. Agar siz `WHERE payload->>'status' = 'PAID'` yozayotgan bo'lsangiz, `status` oddiy ustun bo'lishi kerak edi.

```sql
ALTER TABLE payment ADD COLUMN gateway_response jsonb;

-- Kerakli maydon ajratib olinadi va indekslanadi
ALTER TABLE payment
    ADD COLUMN gateway_code text
    GENERATED ALWAYS AS (gateway_response->>'code') STORED;
CREATE INDEX idx_payment_gateway_code ON payment (gateway_code);

-- 2 KB dan oshgan qiymat TOAST ga chiqadi: har o'qishda qo'shimcha I/O
ALTER TABLE payment ALTER COLUMN gateway_response SET STORAGE EXTERNAL;
```

Tuzoq: 100 KB lik `jsonb` ni `SELECT *` bilan har so'rovda tortib olish. TOAST dan o'qish taxminan 0.2-1 ms qo'shadi. Minglab so'rovda bu sezilarli, shuning uchun bunday ustunni alohida entity ga chiqarish kerak.

### 25.7 Massiv, `enum` va alohida lug'at jadvali orasidagi tanlov

PostgreSQL `enum` turi 4 bayt egallaydi va eng tez ishlaydi. Lekin qiymat qo'shish `ALTER TYPE ... ADD VALUE` talab qiladi, o'chirish esa mumkin emas. Shuning uchun `enum` faqat haqiqatan o'zgarmas ro'yxatga yaraydi.

`text` plus `CHECK IN (...)` enum ga yaqin, migratsiya oson, Hibernate `@Enumerated(EnumType.STRING)` bilan tabiiy ishlaydi. Ko'p holatda eng amaliy yechim. Lug'at jadvali esa qiymatga qo'shimcha atribut kerak bo'lganda yoki ro'yxat admin paneli orqali boshqarilganda zarur.

```sql
ALTER TABLE orders ADD CONSTRAINT chk_order_status
    CHECK (status IN ('NEW','PAID','SHIPPED','DELIVERED','CANCELLED'));

-- Teglar: faqat filtrlash uchun, massiv va GIN indeks
ALTER TABLE product ADD COLUMN tags text[] NOT NULL DEFAULT '{}';
CREATE INDEX idx_product_tags ON product USING GIN (tags);
SELECT id FROM product WHERE tags @> ARRAY['aksiya'];

-- Yetkazib berish usuli: narxi va tartibi bor, demak lug'at jadvali
CREATE TABLE delivery_method (
    code       text PRIMARY KEY,
    title      text NOT NULL,
    sort_order int  NOT NULL,
    is_active  boolean NOT NULL DEFAULT true
);
```

Massiv tuzog'i: unda tashqi kalit bo'lmaydi. Massiv ichidagi qiymat o'chirilgan lug'at yozuviga ishora qilsa, baza buni sezmaydi.

### 25.8 Normalizatsiya va ataylab denormalizatsiya qilish qarori

Standart yo'l uchinchi normal shakl: har fakt bir joyda, yangilash bitta qatorga tegadi. Denormalizatsiya esa ongli savdo, o'qish tezligi uchun yozish murakkabligini sotib olasiz.

Denormalizatsiyani faqat o'lchangan muammodan keyin qiling, avval `EXPLAIN (ANALYZE, BUFFERS)` bilan sabab topilsin. Ko'p holatda muammo yo'qolgan indeks yoki N+1 so'rov, sxema emas.

To'g'ri namuna: buyurtma yaratilgan paytdagi mahsulot nomi va narxini `order_line` ga ko'chirish, chunki bu tarixiy snapshot va narx keyin o'zgarsa hisob-faktura o'zgarmasligi kerak. Yana biri: `orders.total_minor` ni saqlab, tunda `order_line` dan qayta hisoblab tekshirish.

| Oddiy yondashuv | Arxitektor yondashuvi |
| --- | --- |
| Narxni `double` ga yozish | `numeric(19,4)` yoki `bigint` minor unit, valyuta alohida |
| Hamma matn `varchar(255)` | `text` plus biznesdan kelgan `CHECK (length(...))` |
| `timestamp` va JVM zonasiga tayanish | `timestamptz`, hamma UTC da, `Instant`/`OffsetDateTime` |
| Hamma joyda UUIDv4 kalit | hajmga qarab `bigint` identity yoki UUIDv7 |
| Cheklovni faqat `@NotNull` da qoldirish | `NOT NULL`, `CHECK`, `UNIQUE` bazada, annotatsiya qo'shimcha |
| Yangi maydonni `jsonb` ga tashlash | so'rovda ishtirok etsa alohida ustun, arxiv bo'lsa `jsonb` |
| FK ni tezlik uchun olib tashlash | FK qoldiriladi va bola ustuniga indeks qo'yiladi |
| `deleted = true` bilan yumshoq o'chirish | shartli unikal indeks, partial indeks, arxiv siyosati |
| `updated_at` ni servis kodida qo'yish | baza trigger'i, hamma yozuvchi uchun bir xil |
| Indeksni muammo chiqqanda qo'shish | kirish naqshi sxema bilan birga loyihalanadi |

### 25.9 Yumshoq o'chirish (soft delete) va uning yashirin narxi

`deleted_at timestamptz` ustuni oddiy ko'rinadi, lekin to'rt narx keltiradi. Har so'rov `WHERE deleted_at IS NULL` ni unutmasligi kerak, unutilsa ma'lumot sizib chiqadi. `UNIQUE` cheklov buziladi, chunki o'chirilgan va yangi qator bir xil email'ga ega bo'ladi. Tashqi kalit o'chirilgan ota qatorga ishora qilib qolaveradi. Jadval esa cheksiz o'sadi va planner statistikasi buziladi.

```sql
-- O'chirilgan qator unikallikni buzmasligi uchun
CREATE UNIQUE INDEX uq_customer_email_live
    ON customer (lower(email)) WHERE deleted_at IS NULL;

-- Faol qatorlar uchun partial indeks: hajm kichik, skan tez
CREATE INDEX idx_orders_live_status
    ON orders (status, created_at) WHERE deleted_at IS NULL;

-- Kod shu ko'rinishga murojaat qiladi, jadvalga emas
CREATE VIEW customer_live AS
SELECT * FROM customer WHERE deleted_at IS NULL;
```

Hibernate 6.3+ da `@SQLRestriction` filtrni entity darajasida qo'shadi, lekin bu faqat JPA yo'lida ishlaydi. Native so'rov va ETL uchun ko'rinish yoki Row Level Security ishonchliroq.

Qaror: huquqiy saqlash talabi bo'lsa yoki foydalanuvchi qaytarish tugmasini kutsa yumshoq o'chirish. Aks holda haqiqiy `DELETE` plus audit jadvalidagi iz. Hajm katta bo'lsa, o'chirilganlarni arxiv jadvalga ko'chirish kerak.

### 25.10 Audit ustunlari va o'zgarishlar tarixini saqlash usullari

Minimal to'plam `created_at`, `created_by`, `updated_at`, `updated_by` savolning yarmiga javob beradi. U "oxirgi holat kim tomonidan" ni aytadi, "kecha nega o'zgargan" ni aytmaydi. Spring Data JPA `@CreatedDate` va `AuditorAware` bilan buni avtomatlashtiradi, lekin faqat ilova orqali o'tgan yozuvlarni qamrab oladi.

```sql
CREATE OR REPLACE FUNCTION touch_updated_at() RETURNS trigger AS $fn$
BEGIN
    NEW.updated_at := now();
    RETURN NEW;
END;
$fn$ LANGUAGE plpgsql;

CREATE TRIGGER trg_orders_touch BEFORE UPDATE ON orders
    FOR EACH ROW EXECUTE FUNCTION touch_updated_at();

-- To'liq tarix: har o'zgarish alohida qator, faqat qo'shiladi
CREATE TABLE order_history (
    history_id bigint GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
    order_id   bigint NOT NULL,
    changed_at timestamptz NOT NULL DEFAULT clock_timestamp(),
    changed_by text   NOT NULL,
    reason     text,
    snapshot   jsonb  NOT NULL     -- qatorning o'sha paytdagi holati
);
CREATE INDEX idx_order_history_order ON order_history (order_id, changed_at DESC);
```

Uch usul va narxi. Trigger bilan yozilgan tarix eng ishonchli, lekin har `UPDATE` ni taxminan 15-30 foizga sekinlashtiradi. Hibernate Envers avtomatik revision jadvallari yaratadi, ammo native yozuvlarni ko'rmaydi. WAL dan logical decoding ilovaga tegmaydi va eng kam yuk beradi, lekin alohida infratuzilma talab qiladi. Tarix qatorlari asosiy jadvaldan 10 baravar ko'p bo'lsa, `changed_at` bo'yicha partition qilish shart.

### 25.11 Ustun tartibi va qator kattaligi (padding) ta'siri

PostgreSQL qatorni sahifada ustun tartibi bo'yicha joylashtiradi va har turni o'z alignment chegarasiga tekislaydi: `bigint` va `timestamptz` 8 baytga, `int` 4 baytga, `smallint` 2 baytga. Noto'g'ri tartib qator orasida bo'sh bayt qoldiradi.

`boolean, bigint, boolean, int` tartibida har `boolean` dan keyin padding yo'qoladi, ya'ni qatorga taxminan 10 bayt ortiqcha. 100 mln qatorlik jadvalda bu taxminan 1 GB. To'g'ri tartib: eng kattadan kichikka, oxirida o'zgaruvchan uzunlikdagi `text` va `jsonb`.

```sql
-- 8 baytlilar oldinda, boolean oxirida, text eng oxirida
CREATE TABLE stock_event (
    event_id    bigint      NOT NULL,
    occurred_at timestamptz NOT NULL,
    qty         int         NOT NULL,
    is_reversal boolean     NOT NULL DEFAULT false,
    is_manual   boolean     NOT NULL DEFAULT false,
    sku         text        NOT NULL
);

-- Haqiqiy hajmni o'lchash
SELECT pg_size_pretty(pg_total_relation_size('stock_event'));
```

Bu optimizatsiya faqat o'nlab million qatorli jadvallarda ahamiyatli. Kichik jadvalda tartibni o'qilish qulayligiga qarab tanlang.

### 25.12 Nomlash qoidalari va sxema ichidagi tartib

Nomlash qoidasi did masalasi emas, tezlik masalasi. Bir xil qoida bilan yozilgan sxemada dasturchi jadval nomini taxmin qila oladi.

Amalda ishlaydigan to'plam: hamma nom `snake_case`, chunki PostgreSQL qo'shtirnoqsiz identifikatorni kichik harfga keltiradi. Jadval nomi birlikda (`order_line`, `payment`). Tashqi kalit ustuni `<jadval>_id`. Indeks `idx_`, unikal indeks `uq_`, cheklov `chk_`, tashqi kalit `fk_` prefiksi bilan. Vaqt ustunlari `_at` bilan, bayroqlar `is_` bilan tugaydi yoki boshlanadi.

```properties
# Hibernate nomlarni o'zi o'zgartirmasligi uchun aniq strategiya
spring.jpa.hibernate.naming.physical-strategy=\
  org.hibernate.boot.model.naming.CamelCaseToUnderscoresNamingStrategy
# Ishlab chiqarishda sxemani Hibernate yaratmasin, faqat tekshirsin
spring.jpa.hibernate.ddl-auto=validate
spring.flyway.enabled=true
spring.flyway.locations=classpath:db/migration
```

Sxema tartibi uchun uch qoida. `public` sxemani bo'sh qoldirib, domen bo'yicha alohida sxema (`billing`, `inventory`) ishlating, bu huquq ajratishni osonlashtiradi. Har migratsiya faqat oldinga, `DROP COLUMN` oldidan ikki bosqichli deploy. `ddl-auto` hech qachon `update` bo'lmasin.

| Tuzoq | Yechim |
| --- | --- |
| `varchar(n)` ni kattalashtirish qo'rqinchli deb o'ylash | uzunlikni oshirish jadvalni qayta yozmaydi, tez operatsiya |
| `ADD COLUMN NOT NULL DEFAULT` jadvalni bloklaydi | PostgreSQL 11+ da konstant default metadata orqali qo'shiladi |
| `ALTER TYPE` bilan katta jadvalda tur o'zgartirish | yangi ustun, backfill, almashtirish: uch bosqichli migratsiya |
| FK bola ustuniga indeks yo'q | `CREATE INDEX CONCURRENTLY` bilan qo'shish |
| Yumshoq o'chirishda `UNIQUE` buziladi | `WHERE deleted_at IS NULL` shartli unikal indeks |
| `jsonb` kaliti bo'yicha filtr sekin | generated column plus B-tree indeks |
| Tarix jadvali asosiy jadvaldan katta | `changed_at` bo'yicha partition va saqlash muddati |
| `timestamp` ustun bilan DST xatosi | `timestamptz` ga migratsiya, hamma UTC da |
| UUIDv4 kalitda insert sekinlashishi | UUIDv7 yoki `bigint` identity plus tashqi UUID ustun |
| `ddl-auto=update` ishlab chiqarishda | `validate` plus Flyway migratsiyasi va sxema review |

Asosiy xulosa: sxemadagi har bir qaror keyinchalik migratsiya narxiga aylanadi, shuning uchun turni birinchi marta to'g'ri yozish eng arzon yo'l. Testlash qo'llanmasidagi Testcontainers bo'limi bu cheklovlarni haqiqiy PostgreSQL da tekshirish yo'lini ko'rsatadi.

### 25.13 Amalda qo'llash

- [ ] Barcha pul ustunlarini tekshirib, `double precision` yoki `real` topilsa `numeric(19,4)` yoki `bigint` minor unit ga migratsiya rejasini yozing va valyuta kodini alohida ustunga chiqaring.
- [ ] `information_schema.columns` dan `timestamp without time zone` ustunlarini ro'yxatlang va moment saqlaydiganlarini `timestamptz` ga o'tkazing.
- [ ] Har bir tashqi kalit ustunida indeks borligini tekshiradigan so'rov yozib, yetishmaganlarini `CREATE INDEX CONCURRENTLY` bilan qo'shing.
- [ ] Nullable, lekin amalda hech qachon bo'sh bo'lmagan ustunlarni aniqlab, ularga `NOT NULL` cheklovini qo'shing.
- [ ] Yumshoq o'chirish ishlatilgan jadvallarda `UNIQUE` cheklovlarni shartli indeksga aylantirib, faol qatorlar uchun partial indeks qo'shing.
- [ ] `jsonb` ustuni bo'yicha filtrlaydigan so'rovlarni topib, eng ko'p ishlatilgan kalitni generated column ga chiqarib, farqni `EXPLAIN ANALYZE` bilan o'lchang.
- [ ] `ddl-auto` qiymatini barcha profil uchun `validate` yoki `none` ga o'rnatib, sxema o'zgarishini faqat Flyway orqali qabul qiling.
- [ ] Nomlash qoidalarini bitta sahifada yozib migratsiya review checklist'iga kiriting va eng katta uchta jadvalda ustun tartibini `pg_total_relation_size` bilan tekshiring.

## 26. Partitioning, replikatsiya va katta hajm (Partitioning, Replication and Scale)

Katta hajm hech qachon bir kunda kelmaydi. Buyurtma jadvali ikki yil ichida 300 million qatorga chiqadi, hisobot so'rovi 40 ms dan 9 sekundga o'tadi, va kechagi `DELETE` tungi oynani to'ldirib qo'yadi. Bu bobda PostgreSQL ning partitioning va replikatsiya mexanikasi, uning ichida nima sodir bo'lishi va arxitektor shu bilimdan qanday raqamli qaror chiqarishi ko'rib chiqiladi. Taqsimlangan ma'lumot patternlari bu yerda emas, dizayn patternlar hujjatida.

### 26.1 Jadval qachon katta hisoblanadi: qaror uchun raqamlar

Partitioning qarori "jadval katta ko'rinadi" degan tuyg'udan emas, to'rt o'lchovdan chiqadi. Birinchi o'lchov: jadval va uning indekslari `shared_buffers` ga sig'adimi. Odatda `shared_buffers` RAM ning 25 foizi, ya'ni 64 GB serverda taxminan 16 GB. Agar faol indekslar yig'indisi shundan katta bo'lsa, har bir index lookup diskka tushadi va latency 0.1 ms dan 2 ms ga o'tadi.

Ikkinchi o'lchov: autovacuum bir jadvalni necha vaqtda aylanib chiqadi. 200 GB jadvalda `autovacuum_vacuum_cost_limit` standart qiymatda qolsa, bitta tsikl bir necha sutka davom etishi mumkin. Uchinchi o'lchov: eski ma'lumotni o'chirish yo'li bormi. To'rtinchi: `REINDEX` va backup oynasi.

```sql
-- jadval va index hajmini birgalikda ko'rish, eng kattalari yuqorida
SELECT relname,
       pg_size_pretty(pg_table_size(oid))        AS heap,
       pg_size_pretty(pg_indexes_size(oid))      AS indekslar,
       pg_size_pretty(pg_total_relation_size(oid)) AS jami,
       n_live_tup
FROM pg_class c
JOIN pg_stat_user_tables s ON s.relid = c.oid
WHERE relkind = 'r'
ORDER BY pg_total_relation_size(oid) DESC
LIMIT 10;
```

Amaliy chegara: 10 GB dan kichik jadvalni partitsiyalash deyarli har doim zarar. 50 GB dan katta va vaqt bo'yicha o'qiladigan jadval partitioning uchun yaxshi nomzod. 100 GB dan katta va retention siyosati bor jadvalda partitioning tanlov emas, majburiyat.

### 26.2 Deklarativ partitioning: range, list, hash va kalit tanlash

PostgreSQL 10 dan beri deklarativ partitioning bor, 15-17 versiyalarda esa u ishlab chiqarishga to'liq yaroqli. Range eng ko'p ishlatiladi: vaqt bo'yicha bo'lish. List tenant yoki region bo'yicha ajratishga to'g'ri keladi. Hash kalit qiymatlari teng tarqalishini xohlaganda, masalan `customer_id` bo'yicha yuklamani 16 ta bo'lakka yoyganda ishlatiladi.

Eng muhim qoida: partition kaliti har bir unique constraint va primary key tarkibida bo'lishi shart. Shuning uchun `orders` jadvalining PK si `(id)` emas, `(id, created_at)` bo'lib qoladi. 
```sql
CREATE TABLE orders (
    id          bigint GENERATED BY DEFAULT AS IDENTITY,
    customer_id bigint      NOT NULL,
    status      text        NOT NULL,
    amount      numeric(19,4) NOT NULL,
    created_at  timestamptz NOT NULL,
    PRIMARY KEY (id, created_at)      -- kalit PK ichida bo'lishi shart
) PARTITION BY RANGE (created_at);

CREATE TABLE orders_2026_09 PARTITION OF orders
    FOR VALUES FROM ('2026-09-01') TO ('2026-10-01');
CREATE TABLE orders_2026_10 PARTITION OF orders
    FOR VALUES FROM ('2026-10-01') TO ('2026-11-01');

-- chegaradan tashqari qolgan qator yo'qolmasligi uchun
CREATE TABLE orders_default PARTITION OF orders DEFAULT;

-- index har bir partitionga avtomatik tarqaladi
CREATE INDEX ON orders (customer_id, created_at DESC);
```

Partition sonini nazorat qiling. 12-60 ta partition sog'lom. 1000 dan oshsa, planning vaqti va lock soni sezilarli o'sadi, chunki planner har bir partitionni ko'rib chiqadi va `max_locks_per_transaction` chegarasiga yaqinlashadi. Yangi partitionni qo'lda yaratish esdan chiqadi, shuning uchun `pg_partman` kabi vosita yoki scheduled job kerak. Default partition unutilgan oyni xatodan saqlaydi, lekin unga qator tushgach yangi partition `ATTACH` qilish qiyinlashadi.

### 26.3 Partition pruning qachon ishlaydi va qachon ishlamaydi

Pruning planner yoki executor darajasida ishlaydi. Planner darajasida `WHERE created_at >= '2026-10-01'` kabi konstanta bilan taqqoslash kerak. `EXPLAIN` chiqishida faqat kerakli partition ko'rinadi. Executor darajasida pruning esa parametrli so'rov va nested loop ichida ishlaydi, `EXPLAIN ANALYZE` da `Subplans Removed: 11` qatori shundan xabar beradi.

Pruning buziladigan uch holat bor. Birinchi: kalit ustiga funksiya qo'yilgan, masalan `date_trunc('month', created_at) = '2026-10-01'`. Bu yerda planner chegaralarni hisoblay olmaydi. Ikkinchi: filtr kalitda emas, faqat `status` bo'yicha. Uchinchi: join kaliti partition kaliti emas, bu holda barcha partitionlar skanerdan o'tadi.

```sql
-- yaxshi: faqat bitta partition o'qiladi
EXPLAIN (ANALYZE, BUFFERS)
SELECT sum(amount) FROM orders
WHERE created_at >= '2026-10-01' AND created_at < '2026-11-01';

-- yomon: funksiya kalitni yashiradi, hamma partition skanerdan o'tadi
EXPLAIN SELECT sum(amount) FROM orders
WHERE date_trunc('month', created_at) = '2026-10-01';

-- partition kaliti bo'yicha joinda partitionwise join kerak
SET enable_partitionwise_join = on;      -- standart holatda off
SET enable_partitionwise_aggregate = on; -- katta hisobotlar uchun
```

`enable_partitionwise_join` planning vaqtini oshirgani uchun o'chirilgan: hisobot bazasida yoqish mantiqiy, OLTP da ehtiyot bo'lish kerak. `now()` funksiyasi STABLE, shuning uchun `created_at > now() - interval '7 days'` executor darajasida to'g'ri prune bo'ladi.

### 26.4 Eski ma'lumotni o'chirish: `DETACH PARTITION` ning tezligi

Mana partitioning ning eng katta amaliy foydasi. 50 million qatorli bir oylik ma'lumotni `DELETE` qilish taxminan 15-40 daqiqa oladi, WAL ga o'n gigabayt yozadi, so'ng autovacuum shu joyni tozalashga yana soatlar sarflaydi. Bo'sh joy operatsion tizimga qaytmaydi. `DROP TABLE` esa katalog operatsiyasi, taxminan 50 ms da tugaydi va fayllarni butunlay o'chiradi.

```sql
-- 1-qadam: uzoq lock olmasdan ajratish (PostgreSQL 14+)
-- bu buyruq tranzaksiya bloki ichida bo'lmasligi kerak
ALTER TABLE orders DETACH PARTITION orders_2025_10 CONCURRENTLY;

-- 2-qadam: arxivga ko'chirish yoki butunlay o'chirish
-- avval sovuq saqlashga eksport
-- COPY orders_2025_10 TO PROGRAM 'gzip > /arxiv/orders_2025_10.csv.gz' CSV;
DROP TABLE orders_2025_10;

-- oddiy DETACH ishlatilsa, parentga ACCESS EXCLUSIVE lock tushadi,
-- shuning uchun kutish vaqtini cheklab qo'yish kerak
SET lock_timeout = '3s';
ALTER TABLE orders DETACH PARTITION orders_2025_11;
```

`CONCURRENTLY` variantida PostgreSQL ikki fazada ishlaydi va uzoq muddatli ACCESS EXCLUSIVE lock olmaydi. Buning sharti: buyruq avtomatik commit rejimida, tranzaksiya bloki tashqarisida bajarilsin. Agar buyruq to'xtab qolsa, partition `DETACH PENDING` holatida qoladi va uni `FINALIZE` bilan tugatish kerak.

### 26.5 Mavjud katta jadvalni to'xtashsiz partitsiyalashga o'tkazish

Bu ish bir buyruq bilan bo'lmaydi. 400 GB `payments` jadvalini `CREATE TABLE ... PARTITION BY` ga aylantirish imkoni yo'q, chunki oddiy jadvalni partitsiyalangan jadvalga joyida o'zgartirish mumkin emas. Ishonchli yo'l to'rt qadamdan iborat.

Birinchi qadam: yangi partitsiyalangan parent yaratish va kelgusi oylar uchun bo'sh partitionlar qo'shish. Ikkinchi: eski jadvalni o'sha parentga partition sifatida `ATTACH` qilish. Bu yerda muhim nozik joy bor. `ATTACH PARTITION` chegarani tekshirish uchun to'liq skan qiladi, agar jadvalda mos `CHECK` constraint oldindan bo'lmasa.

```sql
-- eski jadvalga NOT VALID check qo'yib, keyin fonda validatsiya qilamiz
ALTER TABLE payments_old
  ADD CONSTRAINT payments_old_range
  CHECK (created_at >= '2019-01-01' AND created_at < '2026-10-01') NOT VALID;

-- VALIDATE faqat SHARE UPDATE EXCLUSIVE lock oladi, yozish davom etadi
ALTER TABLE payments_old VALIDATE CONSTRAINT payments_old_range;

-- endi ATTACH to'liq skan qilmaydi, bir necha yuz millisekundda tugaydi
ALTER TABLE payments ATTACH PARTITION payments_old
  FOR VALUES FROM ('2019-01-01') TO ('2026-10-01');

-- oxirgi qadam: qisqa tranzaksiyada nom almashtirish
SET lock_timeout = '2s';
BEGIN;
  ALTER TABLE payments_live RENAME TO payments_legacy;
  ALTER TABLE payments RENAME TO payments_live;
COMMIT;
```

Nom almashtirish tranzaksiyasi millisekundlar ichida tugaydi, lekin ACCESS EXCLUSIVE lock talab qiladi. Shuning uchun `lock_timeout` qo'yiladi va buyruq yuklama past paytda takroriy urinish bilan bajariladi. PostgreSQL 17 da `SPLIT PARTITION` va `MERGE PARTITIONS` buyruqlari bor, lekin ular ham kuchli lock oladi, ya'ni ularni onlayn migratsiya vositasi deb hisoblash xato.

### 26.6 Streaming replikatsiya: primary va standby, lag o'lchash

Streaming replikatsiyada primary dagi `walsender` process WAL yozuvlarini standby dagi `walreceiver` ga uzatadi. Standby ularni diskka yozadi, so'ng `startup` process qayta ijro etadi. Shu uch bosqich uchta alohida lag beradi: `write_lag`, `flush_lag`, `replay_lag`.

```sql
-- primary da: har bir standby uchun bayt va vaqt bo'yicha lag
SELECT application_name,
       state,
       sync_state,
       pg_wal_lsn_diff(pg_current_wal_lsn(), replay_lsn) AS lag_bayt,
       write_lag, flush_lag, replay_lag
FROM pg_stat_replication;

-- standby da: replikatsiya kechikishi sekundda
SELECT CASE WHEN pg_is_in_recovery()
            THEN extract(epoch FROM now() - pg_last_xact_replay_timestamp())
       END AS lag_sek;

-- slot WAL ni ushlab qolib diskni to'ldirmasligi uchun
-- postgresql.conf: max_slot_wal_keep_size = '64GB'
SELECT slot_name, active, wal_status,
       pg_size_pretty(pg_wal_lsn_diff(pg_current_wal_lsn(), restart_lsn))
FROM pg_replication_slots;
```

Bir data markazda normal `replay_lag` 1 ms dan 50 ms gacha, baytda bir necha megabayt. Lag o'nlab sekundga chiqsa, sabab odatda ikkitadan biri: standby da og'ir `SELECT` replay ni bloklagan, yoki primary da bitta katta tranzaksiya WAL ni to'kib tashlagan. Replication slot himoya beradi, lekin standby o'lsa WAL to'planib diskni to'ldiradi, shuning uchun `max_slot_wal_keep_size` majburiy.

### 26.7 Sinxron va asinxron replikatsiya tanlovi va uning narxi

`synchronous_commit` ning narxi bitta raqam bilan o'lchanadi: commit ga qo'shiladigan tarmoq RTT. Bir availability zone ichida bu taxminan 0.3-1 ms, zonalar orasida 1-2 ms, regionlar orasida 20-80 ms. To'lov servisida sekundiga 500 commit bo'lsa, cross-region sinxron rejim to'g'ridan to'g'ri throughput ni o'n baravar pasaytiradi.

| Rejim | Kafolat | Qo'shimcha latency |
| --- | --- | --- |
| `off` | hatto primary diskiga ham kafolat yo'q | 0 ga yaqin |
| `local` | faqat primary WAL diskda | fsync vaqti, 0.1-1 ms |
| `remote_write` | standby OS buferida | 1 RTT |
| `on` | standby WAL diskda | 1 RTT + fsync |
| `remote_apply` | standby da ko'rinadi | 1 RTT + replay |

Eng xavfli xato: bitta sinxron standby qo'yish. U o'lsa, barcha commitlar muddatsiz kutib qoladi va baza yozish uchun yopiladi. To'g'ri sozlash kvorum bilan bo'ladi.

```ini
# postgresql.conf, primary da
# ikki nomzoddan bittasi javob bersa commit o'tadi
synchronous_standby_names = 'ANY 1 (standby_a, standby_b)'
synchronous_commit = on
wal_level = replica
max_wal_senders = 10
max_slot_wal_keep_size = '64GB'
```

Butun bazani bitta rejimga majburlash shart emas: to'lov tranzaksiyasi sinxron, audit logi asinxron bo'lishi mumkin. Buni tranzaksiya darajasida `SET LOCAL synchronous_commit = 'local'` bilan qilinadi, Spring da esa shu buyruqni `@Transactional` metod boshida yuborish yetarli.

### 26.8 O'qishni standby ga yo'naltirish va replikatsiya lag dan kelib chiqadigan xatolar

Standby dan o'qish ikki turdagi muammo keltiradi. Birinchisi texnik xato: `ERROR: canceling statement due to conflict with recovery`. Bu replay primary da `VACUUM` tozalagan qatorni o'chirmoqchi bo'lganda, standby dagi uzun `SELECT` esa shu qatorni hali o'qiyotganda yuz beradi. Yechim ikkita: `max_standby_streaming_delay` ni oshirish, yoki `hot_standby_feedback = on` qo'yish. Ikkinchisi primary da bloat o'sishiga olib keladi, chunki `VACUUM` standby dagi eng eski snapshot ni kutadi.

Ikkinchi muammo mantiqiy: foydalanuvchi to'lovni yaratdi, keyingi so'rov standby ga tushdi va to'lov hali ko'rinmaydi. Buni lag o'lchab hal qilib bo'lmaydi, chunki lag o'zgaruvchan. To'g'ri yechim: yozishdan keyingi N sekund ichida o'sha foydalanuvchining o'qishlarini primary ga yuborish, yoki commit LSN ni saqlab standby shu LSN ga yetganini tekshirish.

| Tuzoq | Nima sodir bo'ladi | Yechim |
| --- | --- | --- |
| Bitta sinxron standby | standby o'lsa yozish to'xtaydi | `ANY 1 (a, b)` kvorumi |
| `max_slot_wal_keep_size` yo'q | slot WAL ni ushlab disk to'ladi | chegara qo'yish va slot monitoringi |
| Standby da uzun hisobot | recovery conflict, so'rov o'ldiriladi | alohida standby, `hot_standby_feedback` |
| `readOnly=true` ga ishonib yozish | silent routing xatosi, UPDATE yo'qoladi | standby da PostgreSQL o'zi xato beradi, testda tekshirish |
| Connection darhol olinadi | routing qarori kech, har doim primary | `LazyConnectionDataSourceProxy` |
| Funksiya partition kalitida | pruning yo'q, hamma partition skan | filtrni xom ustunga yozish |
| `DELETE` bilan retention | bloat, uzoq vacuum, WAL to'lishi | `DETACH` + `DROP TABLE` |
| Logical slot iste'molchisi o'chgan | WAL cheksiz o'sadi | slot lag alert, eskisini `DROP` |

### 26.9 Mantiqiy replikatsiya va CDC uchun asos

Streaming replikatsiya butun klasterni bayt darajasida ko'chiradi. Mantiqiy replikatsiya esa jadval darajasida ishlaydi va `pgoutput` plaginidan foydalanadi. Debezium ham shu plagin orqali o'qiydi, ya'ni CDC uchun tashqi C kutubxona o'rnatish shart emas.

```sql
-- postgresql.conf: wal_level = logical, keyin restart kerak
CREATE PUBLICATION cdc_pub FOR TABLE orders, payments;

-- PK yo'q jadvalda UPDATE/DELETE uchun identifikator kerak
ALTER TABLE order_items REPLICA IDENTITY FULL;

-- faqat kerakli qatorlarni uzatish (PostgreSQL 15+)
CREATE PUBLICATION paid_pub FOR TABLE orders
  WHERE (status = 'PAID');

-- Debezium uchun slot qo'lda ham yaratilishi mumkin
SELECT pg_create_logical_replication_slot('debezium_orders', 'pgoutput');
```

To'rtta cheklovni bilish shart. DDL replikatsiya qilinmaydi, ya'ni yangi ustun qo'shilsa, iste'molchi tomonda ham qo'lda qo'shish kerak. TOAST ga tushgan va o'zgarmagan ustun qiymati stream ga chiqmaydi, shuning uchun katta JSON ustunga tayangan CDC pipeline kutilmagan `null` ko'radi. Sequence qiymatlari ko'chmaydi. Va eng xavflisi: iste'molchi o'chsa, slot WAL ni ushlab turadi. Slot lag ni monitoringga qo'yish bu yerda ixtiyoriy emas. CDC ni outbox o'rniga ishlatish qarori dizayn patternlar hujjatidagi outbox pattern bilan solishtirib olinadi.

### 26.10 Failover va yuqori mavjudlik vositalari haqida qisqacha

PostgreSQL o'zida avtomatik failover yo'q. Bu tashqi vosita ishi. Eng keng tarqalgani Patroni, u etcd yoki Consul kabi distributed konfiguratsiya saqlagichdan leader election oladi. Alternativalar: repmgr va pg_auto_failover. Boshqariladigan servislarda (RDS, Cloud SQL) bu qatlam provayder tomonida.

Uch nuqta muhim. Birinchi: split brain faqat kvorumli DCS va watchdog bilan oldini olinadi, "ping ishlamasa promote qil" skripti emas. Ikkinchi: eski primary qaytganda uni `pg_rewind` bilan yangi timeline ga moslash kerak, aks holda ma'lumot ayriladi. Uchinchi: RTO taxminan 10-30 sekund, ya'ni ilova shu vaqtni xatosiz o'tkazishga qodir bo'lishi shart.

```properties
# PgJDBC o'zi primary ni topadi, failover dan keyin qayta ulanadi
spring.datasource.url=jdbc:postgresql://pg-a:5432,pg-b:5432/shop\
?targetServerType=primary&loadBalanceHosts=false\
&connectTimeout=3&socketTimeout=30

# failover paytida pool uzun kutmasin
spring.datasource.hikari.connection-timeout=3000
spring.datasource.hikari.validation-timeout=2000
spring.datasource.hikari.keepalive-time=120000
```

Failover testi ishlab chiqarishga chiqishdan oldin bajarilishi kerak: testlash qo'llanmasidagi resilience testlari bo'limida standby ni promote qilib tiklanish vaqtini o'lchash stsenariysi bor.

### 26.11 Spring da o'qish va yozish uchun alohida DataSource sozlash

`AbstractRoutingDataSource` routing kalitini `determineCurrentLookupKey()` da aniqlaydi va `TransactionSynchronizationManager.isCurrentTransactionReadOnly()` shu kalit uchun tabiiy manba. Lekin bitta jiddiy tuzoq bor: Spring tranzaksiya boshlanishida connection ni darhol oladi, ya'ni routing qarori `readOnly` flagi o'rnatilishidan oldin bo'lishi mumkin. Shuning uchun routing DataSource ni `LazyConnectionDataSourceProxy` ichiga o'rash shart.

```java
public class ReadWriteRoutingDataSource extends AbstractRoutingDataSource {
    @Override
    protected Object determineCurrentLookupKey() {
        // readOnly tranzaksiya standby ga, qolgani primary ga
        return TransactionSynchronizationManager.isCurrentTransactionReadOnly()
                ? "replica" : "primary";
    }
}

@Configuration
class DataSourceConfig {
    @Bean
    DataSource dataSource(@Qualifier("primaryDs") DataSource primary,
                          @Qualifier("replicaDs") DataSource replica) {
        var router = new ReadWriteRoutingDataSource();
        router.setTargetDataSources(Map.of("primary", primary, "replica", replica));
        router.setDefaultTargetDataSource(primary);
        router.afterPropertiesSet();
        // lazy o'ram bo'lmasa routing qarori har doim primary ga tushadi
        return new LazyConnectionDataSourceProxy(router);
    }
}
```

Pool o'lchamini ikki tomonga alohida bering. Yozish pooli kichik bo'lsin, masalan 10 ta connection, chunki primary dagi yozish lock bilan cheklangan. O'qish pooli kattaroq, masalan 20-30 ta, chunki hisobot so'rovlari uzoq. `@Transactional(readOnly = true)` nafaqat routing beradi, balki Hibernate flush ni o'chiradi va dirty checking ishini kamaytiradi, ya'ni katta `SELECT` da taxminan 10-20 foiz CPU tejaydi.

### 26.12 Sharding qachon zarur bo'ladi va nega eng oxirgi chora

Sharding bitta primary ning yozish quvvati tugaganda kerak bo'ladi. Shu chegara aniq raqam bilan ko'rinadi: `pg_stat_statements` da yozish so'rovlari jami vaqti CPU ni to'ldirgan, WAL hajmi sekundiga o'nlab megabayt, va vertikal o'sish uchun joy qolmagan. Zamonaviy serverda bu taxminan sekundiga bir necha o'n ming yozish operatsiyasi va bir necha terabayt faol ma'lumot.

| Vaziyat | Oddiy yondashuv | Arxitektor yondashuvi |
| --- | --- | --- |
| Jadval 200 GB ga yetdi | darhol shard qilish rejasi | avval range partitioning va retention |
| Hisobot so'rovi sekin | primary ga yana index qo'shish | hisobotni alohida standby ga ko'chirish |
| Eski buyurtma kerak emas | tungi `DELETE` job | `DETACH PARTITION` + arxivga `COPY` |
| Replikatsiya lag o'sdi | standby ni kuchaytirish | uzun so'rov va katta tranzaksiyani topish |
| Standby dan eski ma'lumot | lag ni e'tiborsiz qoldirish | yozishdan keyin primary ga yo'naltirish |
| Sinxron kafolat kerak | hammasini `remote_apply` | faqat to'lov yo'lida, kvorum bilan |
| CDC kerak bo'ldi | jadvalni poll qilish | `pgoutput` slot va slot lag alerti |
| Connection soni 2000 | `max_connections` ni oshirish | PgBouncer transaction pooling |
| Yozish quvvati tugadi | darhol sharding | avval batching, partition, arxivlash |
| Shard kaliti tanlanmoqda | `id` bo'yicha hash | `tenant_id` yoki `customer_id` bo'yicha |

Sharding dan oldin to'rtta arzon qadam bor: partitioning, read replica, arxivlash va PgBouncer orqali connection konsentratsiyasi. Narxi esa doimiy: cross-shard join yo'qoladi, global unique constraint yo'qoladi, tranzaksiya bir shard bilan cheklanadi, rebalance esa alohida loyiha bo'ladi. Shard kaliti biznes agregatiga mos tushishi kerak, ya'ni `tenant_id` yoki `customer_id`. Agar so'rovlarning 10 foizi ikki shardga tegsa, bu arxitektura ishlaydi. 50 foizi tegsa, kalit noto'g'ri tanlangan. Citus kabi kengaytma bu ishni osonlashtiradi, lekin qarorni o'zgartirmaydi: sharding oxirgi chora.

### 26.13 Amalda qo'llash

- [ ] Eng katta 10 jadval uchun `pg_total_relation_size` va `n_live_tup` ni o'lchab, 50 GB dan katta va vaqt bo'yicha o'qiladiganlar ro'yxatini tuzing.
- [ ] Bitta nomzod jadvalni range partitioning ga o'tkazish rejasini yozing: kalit, PK o'zgarishi, `NOT VALID` check, `ATTACH`, nom almashtirish qadamlari bilan.
- [ ] Retention jobni `DELETE` dan `DETACH PARTITION CONCURRENTLY` + `DROP TABLE` ga almashtiring va `lock_timeout` qo'ying.
- [ ] Eng og'ir 5 ta hisobot so'rovini `EXPLAIN ANALYZE` bilan tekshirib, `Subplans Removed` qatorini ko'rib pruning ishlashini tasdiqlang.
- [ ] `pg_stat_replication` dagi `replay_lag` va `pg_replication_slots` dagi slot lag uchun alert qo'ying, `max_slot_wal_keep_size` ni belgilang.
- [ ] `synchronous_standby_names` ni `ANY 1 (a, b)` shaklida kvorumga o'tkazing va bitta standby o'chganda yozish to'xtamasligini sinab ko'ring.
- [ ] O'qish uchun alohida DataSource ni `LazyConnectionDataSourceProxy` bilan sozlang, pool o'lchamlarini yozish uchun 10, o'qish uchun 20 qilib ajratib qo'ying.
- [ ] Yozishdan keyingi o'qishni primary ga yo'naltiruvchi qoida kiritib, lag sababli ko'rinmagan yozuv stsenariysini testda qayd eting.

## 27. Sozlash, connection pool va monitoring (Configuration, Pooling and Monitoring)

PostgreSQL ning standart sozlamalari 1 GB operativ xotirali mashinada ishga tushsin degan maqsadda yozilgan, shuning uchun 16 GB li production serverda ular to'g'ridan to'g'ri zarar keltiradi. Arxitektorning vazifasi har bir parametrni server resursidan kelib chiqib hisoblash, keyin ulanishlar sonini pool orqali cheklab, oqibatini monitoring bilan o'lchab turishdir. Sozlash, pool va kuzatuv bir zanjir: noto'g'ri `work_mem` sekin so'rovga, noto'g'ri pool kattaligi timeout'ga olib keladi. Oxirida eng ko'p e'tibordan chetda qoladigan narsa bor: zaxira nusxa emas, balki tiklanishni sinab ko'rish.

### 27.1 Asosiy `postgresql.conf` parametrlari va ularni server resursidan kelib chiqib hisoblash

Har bir parametrning `context` xossasi uni qanday o'zgartirish mumkinligini belgilaydi. `postmaster` kontekstidagi parametr (`shared_buffers`, `max_connections`, `shared_preload_libraries`) faqat restart bilan kuchga kiradi. `sighup` kontekstidagi parametr (`work_mem`, `log_min_duration_statement`) konfiguratsiyani qayta yuklash bilan yetadi. `user` kontekstidagi parametrni esa tranzaksiya ichida o'zgartirish mumkin, bu hisobot so'rovlari uchun eng kuchli vosita.

```sql
-- Qaysi parametr restart talab qiladi, qaysi biri yo'q: shuni avval tekshir
SELECT name, setting, unit, context, source
FROM pg_settings
WHERE name IN ('shared_buffers','work_mem','maintenance_work_mem',
               'effective_cache_size','max_connections','random_page_cost')
ORDER BY context, name;

-- ALTER SYSTEM postgresql.auto.conf ga yozadi, asl faylga tegmaydi
ALTER SYSTEM SET work_mem = '32MB';
ALTER SYSTEM SET effective_cache_size = '12GB';
SELECT pg_reload_conf();            -- sighup parametrlari darhol kuchga kiradi
```

16 GB RAM, 4 vCPU va SSD li OLTP server uchun boshlang'ich nuqta quyidagicha.

| Parametr | Standart | 16 GB server uchun | Nega shunday |
|---|---|---|---|
| `shared_buffers` | 128MB | 4GB | RAM ning taxminan 25 foizi |
| `effective_cache_size` | 4GB | 12GB | Planner uchun ishora, RAM ning 70 foizi |
| `work_mem` | 4MB | 24MB | Har bir sort/hash node uchun |
| `maintenance_work_mem` | 64MB | 1GB | Index va VACUUM tezligi |
| `max_connections` | 100 | 150 | Qolgani pool ustida |
| `random_page_cost` | 4.0 | 1.1 | SSD da tasodifiy o'qish qimmat emas |
| `effective_io_concurrency` | 1 | 200 | NVMe parallel o'qishni ko'taradi |
| `max_wal_size` | 1GB | 8GB | Checkpoint ni siyraklashtirish |
| `wal_compression` | off | on | WAL hajmi va replika trafigi kamayadi |

### 27.2 `shared_buffers`, `work_mem`, `maintenance_work_mem`, `effective_cache_size` tanlash

`shared_buffers` bu PostgreSQL ning o'z buffer cache'i, sahifalar bu yerda OS page cache'dan tashqari yana bir marta saqlanadi. Shuning uchun RAM ning hammasini bermaslik kerak: bir xil sahifa ikki joyda yotadi va OS cache'ga joy qolmaydi. Amalda 25 foiz yaxshi boshlanish, 40 foizdan oshirish faqat o'lchov natijasi bilan asoslanadi.

`effective_cache_size` hech qanday xotira ajratmaydi. Bu faqat planner'ga "shu sahifalar ehtimol cache'da bor" degan ishora, vazifasi index scan narxini arzonlashtirish. Kichik qiymat planner'ni sequential scan tomon suradi, bu 50 million qatorli buyurtma jadvalida falokat.

```properties
# 16 GB RAM, 4 vCPU, SSD, OLTP + kechqurun hisobot
shared_buffers = 4GB
effective_cache_size = 12GB
work_mem = 24MB                   # har bir sort/hash node uchun
maintenance_work_mem = 1GB        # CREATE INDEX, VACUUM, ALTER TABLE
max_parallel_workers_per_gather = 2
wal_buffers = 64MB
max_wal_size = 8GB
random_page_cost = 1.1
effective_io_concurrency = 200
default_statistics_target = 200   # plan aniqligi uchun
```

`maintenance_work_mem` ni saxiy qo'yish arzon, chunki uni faqat autovacuum worker'lari va DDL ishlatadi. 1 GB bilan `CREATE INDEX CONCURRENTLY` tez bitadi. Lekin `autovacuum_max_workers` ni 10 taga ko'tarsang, eng yomon holatda shu qiymat 10 ga ko'payishini unutma.

### 27.3 `work_mem` tuzog'i: u har bir operatsiya uchun ajratiladi

`work_mem` sessiya uchun emas, ulanish uchun ham emas, balki rejadagi har bir sort, hash join va hash aggregate node uchun alohida ajratiladi. Uchta hash join va ikkita sort bo'lgan hisobot so'rovi bitta ulanishda 5 x `work_mem` yeydi. Parallel plan bo'lsa, har bir worker ham o'z ulushini oladi. 150 ulanish x 5 node x 24 MB qog'ozda 18 GB, ya'ni serverdan ko'proq.

```sql
-- Diskka tushgan sort: "external merge" va "Disk:" belgilari muhim
EXPLAIN (ANALYZE, BUFFERS)
SELECT customer_id, sum(total_amount) FROM orders
WHERE created_at >= now() - interval '90 days'
GROUP BY customer_id ORDER BY 2 DESC;
-- Sort Method: external merge  Disk: 86784kB   <-- work_mem yetmagan

-- To'g'ri yechim: global emas, faqat shu tranzaksiya uchun ko'tarish
BEGIN;
SET LOCAL work_mem = '256MB';          -- faqat shu tranzaksiya ichida
SET LOCAL statement_timeout = '120s';  -- hisobot uzoq, lekin cheksiz emas
-- ... hisobot so'rovi ...
COMMIT;

-- Hash operatsiyalari uchun alohida koeffitsient bor (PostgreSQL 13+)
SHOW hash_mem_multiplier;   -- standart 2.0, ya'ni hash node 2 x work_mem oladi
```

Arxitektorning qarori shu: global `work_mem` ni past tut (16 MB dan 32 MB), hisobot va batch uchun alohida role yaratib, unga `ALTER ROLE ... SET work_mem` bilan katta qiymat ber. Shunda kechqurungi hisobot kunduzgi to'lov oqimining xotirasini o'g'irlamaydi.

### 27.4 `max_connections` nega katta bo'lmasligi kerak

PostgreSQL har bir ulanish uchun alohida OS process ochadi. Bo'sh process ham bir necha MB xotira ushlaydi, lekin asosiy narx xotirada emas: snapshot olish, lock jadvalini tekshirish va shared memory strukturalariga kirish ulanishlar soni bilan qimmatlashadi. Natijada 1000 ulanishli serverda CPU ning sezilarli qismi foydali ishga emas, koordinatsiyaga ketadi.

Ikkinchi sabab amaliy: 1000 parallel so'rov 4 vCPU da baribir navbatda turadi, lekin har biri o'z `work_mem` ini va lock'larini ushlaydi. Navbat pool'da turishi kerak, chunki uni o'lchash va cheklash mumkin. Qoida: `max_connections` ni 100 dan 300 orasida tut, parallellikni HikariCP va PgBouncer ustida boshqar.

| Oddiy yondashuv | Arxitektor yondashuvi |
|---|---|
| `max_connections = 1000` qo'yib muammoni yopish | 150 da qoldirish va pool bilan navbat qurish |
| `work_mem` ni global 256MB qilish | Global 24MB, hisobot role'ida 256MB |
| `effective_cache_size` ni xotira ajratish deb bilish | Uni planner narx modeli ishorasi deb bilish |
| Pool kattaligini 50 deb "ehtiyot uchun" qo'yish | Little qonuni bilan hisoblab 10 deb qo'yish |
| Hikari timeout'ini 30s qoldirish | 3s qilib fail fast va circuit breaker ulash |
| PgBouncer'ni session rejimida yoqish | Transaction rejimi va prepared statement masalasini hal qilish |
| Timeout'siz tranzaksiya qoldirish | Role darajasida uchta timeout o'rnatish |
| Sekin so'rovni foydalanuvchi shikoyatidan bilish | `pg_stat_statements` snapshot'ini kunlik solishtirish |
| Backup muvaffaqiyatli bo'lsa xotirjam bo'lish | Chorakda bir marta restore drill o'tkazish |
| Kesh hit nisbatini umuman qaramaslik | 99 foizdan tushishini alert qilish |

### 27.5 HikariCP sozlash: `maximum-pool-size`, `connection-timeout`, `max-lifetime`, `leak-detection-threshold`

`minimum-idle` ni `maximum-pool-size` ga teng qo'yish to'g'ri, chunki ulanish ochish narxi (TCP, TLS, autentifikatsiya) spike paytida eng kerakli daqiqada qo'shiladi. `connection-timeout` esa pool'dan kutish muddati: 30 sekundda qoldirsang, DB sekinlashganda thread'lar o'ttiz sekund band turadi va servis to'xtaydi. 3 sekundlik qiymat tez xato berib, retry va fallback'ga yo'l ochadi.

```yaml
spring:
  datasource:
    hikari:
      maximum-pool-size: 10          # pod uchun, hisoblangan qiymat
      minimum-idle: 10               # production: pool o'lchami doimiy bo'lsin
      connection-timeout: 3000       # pool'dan kutish, ms: fail fast
      validation-timeout: 2000
      max-lifetime: 1500000          # 25 daqiqa, LB/DB limitidan kichik
      keepalive-time: 120000         # bo'sh ulanishni jim o'lishdan saqlaydi
      leak-detection-threshold: 20000 # 20s ushlangan ulanish uchun stack trace
      pool-name: payment-pool
      auto-commit: false             # tranzaksiyani Spring boshqaradi
      data-source-properties:
        reWriteBatchedInserts: true  # JDBC batch insert'ni tezlashtiradi
```

`max-lifetime` infratuzilmadagi eng qisqa muddatdan kichik bo'lishi shart: NAT yoki load balancer bo'sh TCP ulanishni 30 daqiqada uzsa, `max-lifetime` 25 daqiqa bo'ladi. Aks holda ilova o'lgan ulanishni oladi va foydalanuvchi tasodifiy xato ko'radi. `leak-detection-threshold` esa uzoq ushlangan ulanish uchun stack trace yozadi, va bu odatda tranzaksiya ichida HTTP chaqiruv qilingan joyni ochadi.

### 27.6 Pool kattaligini hisoblash formulasi va amaliy raqamlar

Pool kattaligini Little qonuni bilan hisoblash ishonchli: `pool = kutilgan_RPS x o'rtacha_DB_vaqti`. To'lov servisi sekundiga 600 so'rovni ko'tarsa va bir so'rov DB da taxminan 8 ms tursa, kerakli parallellik 600 x 0.008 = 4.8 ta ulanish. Zahira qo'shib 8 yoki 10 deb belgilash yetarli. Klassik `yadro x 2 + disk soni` formulasi ham shu tartibdagi raqam beradi.

| Servis | RPS | O'rtacha DB vaqti | Hisob | Pool (pod) | Pod soni | Jami |
|---|---|---|---|---|---|---|
| To'lov API | 600 | 8 ms | 4.8 | 10 | 4 | 40 |
| Buyurtma API | 300 | 12 ms | 3.6 | 8 | 3 | 24 |
| Ombor qoldig'i | 150 | 5 ms | 0.75 | 5 | 2 | 10 |
| Hisobot worker | 2 | 900 ms | 1.8 | 4 | 1 | 4 |
| Batch import | 1 | 2000 ms | 2.0 | 4 | 1 | 4 |

Jami 82 ta ulanish, ustiga migratsiya va monitoring uchun zahira: `max_connections = 150` yetadi. Eng muhim nazorat shu: barcha pod'lardagi pool'lar yig'indisi `max_connections` dan kam bo'lishi kerak, aks holda autoscaling paytida DB "too many clients already" deb qaytaradi. Kichik pool qo'rqinchli ko'rinadi, lekin amalda katta pool'dan tez ishlaydi, chunki DB navbatda emas, bajarishda bo'ladi.

### 27.7 PgBouncer: transaction va session rejimi, prepared statement masalasi

`session` rejimida client ulanishi uzilguncha server ulanishi band qoladi, ya'ni multiplexing deyarli yo'q va foyda kam. `transaction` rejimida server ulanishi faqat tranzaksiya davomida band bo'ladi, shuning uchun 500 client 25 ta server ulanishiga sig'adi. Ko'p pod'li Kubernetes muhitida PgBouncer'ning asl qiymati shu rejimdagina ochiladi.

```properties
# pgbouncer.ini: 500 client -> 25 server ulanishi
[databases]
orders = host=pg-primary port=5432 dbname=orders

[pgbouncer]
pool_mode = transaction
max_client_conn = 500
default_pool_size = 25
reserve_pool_size = 5
server_idle_timeout = 600
max_prepared_statements = 200   # transaction rejimida prepared statement uchun
ignore_startup_parameters = extra_float_digits
```

Transaction rejimining narxi bor: sessiyaga bog'liq hamma narsa buziladi. `SET` natijasi keyingi tranzaksiyaga o'tmaydi, session darajasidagi advisory lock boshqa client'ga tegib ketadi, `LISTEN/NOTIFY`, temp jadval va `WITH HOLD` cursor ishlamaydi. Eng ko'p uchraydigan muammo server tomonidagi prepared statement: JDBC driver so'rovni bir necha marta bajargandan keyin uni server tomonda nomlab qo'yadi, yangi server ulanishida esa o'sha nom yo'q. Yangi PgBouncer versiyalari buni `max_prepared_statements` bilan protokol darajasida qo'llab-quvvatlaydi. Versiyangiz qodir bo'lmasa, JDBC URL da `prepareThreshold=0` qo'yib server tomonidagi prepared statement'ni o'chirish kerak, narxi esa har safar qayta parse qilish.

HikariCP ilova ichidagi parallellikni cheklaydi, PgBouncer esa pod'lar yig'indisini. Ikkisi bir vazifani bajarmaydi, shuning uchun pod soni o'zgarib turadigan tizimda ikkisi ham kerak.

### 27.8 `statement_timeout`, `lock_timeout`, `idle_in_transaction_session_timeout` o'rnatish

Bu uchta timeout'ni global `postgresql.conf` da qo'yish xato, chunki migratsiya va `VACUUM` ham shu cheklovga tushadi. To'g'ri joy role darajasi: ilovaga qisqa, migratsiyaga uzun, hisobotga o'rtacha qiymat.

```sql
-- OLTP ilovasi: tez xato, uzoq kutish yo'q
ALTER ROLE app_payment SET statement_timeout = '5s';
ALTER ROLE app_payment SET lock_timeout = '2s';
ALTER ROLE app_payment SET idle_in_transaction_session_timeout = '30s';

-- Hisobot role'i: uzoq so'rov ruxsat, lekin cheksiz emas
ALTER ROLE app_report SET statement_timeout = '180s';
ALTER ROLE app_report SET work_mem = '256MB';

-- Migratsiya: DDL navbatda uzoq turmasin
ALTER ROLE app_migrator SET lock_timeout = '3s';

-- Ochiq lekin bo'sh tranzaksiyalar: VACUUM ni bloklaydi
SELECT pid, usename, now() - xact_start AS tx_age, query FROM pg_stat_activity
WHERE state = 'idle in transaction' AND now() - xact_start > interval '1 min';
```

`idle_in_transaction_session_timeout` ning mexanikasi eng muhim: ochiq tranzaksiya o'z `xmin` ini ushlab turadi, shuning uchun VACUUM shu paytdan keyin o'lgan qatorlarni tozalay olmaydi. Bitta unutilgan tranzaksiya bir necha soatda jadvalni bloat qilib, barcha so'rovlarni sekinlashtiradi. `lock_timeout` esa `ALTER TABLE` ning `ACCESS EXCLUSIVE` lock navbatini kutib, orqasida butun o'qish trafigini to'plab qo'yishidan saqlaydi. Spring tomonida `@Transactional(timeout = 5)` foydali, lekin u JDBC query timeout'i bo'lib, server tomonidagi `statement_timeout` ni almashtirmaydi.

### 27.9 Monitoring uchun asosiy ko'rsatkichlar: `pg_stat_database`, `pg_stat_activity`, kesh hit nisbati

`pg_stat_database` birinchi panel. Kesh hit nisbati `blks_hit / (blks_hit + blks_read)` OLTP bazada 99 foizdan yuqori bo'lishi kerak, 95 foizga tushishi `shared_buffers` kichik yoki ishchi ma'lumot hajmi o'sgan degani. `temp_files` va `temp_bytes` o'sishi `work_mem` yetmayotganini, `deadlocks` o'sishi esa kodda lock tartibi buzilganini ko'rsatadi.

```sql
-- Kesh hit nisbati, temp fayl va deadlock
SELECT datname, temp_files, deadlocks,
       round(100.0 * blks_hit / nullif(blks_hit + blks_read, 0), 2) AS cache_hit_pct,
       pg_size_pretty(temp_bytes) AS temp_size
FROM pg_stat_database WHERE datname NOT LIKE 'template%';

-- Hozir nima kutilmoqda: wait_event eng foydali ustun
SELECT state, wait_event_type, wait_event, count(*)
FROM pg_stat_activity WHERE backend_type = 'client backend'
GROUP BY 1,2,3 ORDER BY 4 DESC;
```

`pg_stat_activity` da eng qimmatli ustun `wait_event_type`: `Lock` lock raqobatini, `IO` disk muammosini, `LWLock` ichki raqobatni, `Client` esa ilova sekin o'qiyotganini bildiradi. Jadval darajasida `pg_stat_user_tables` dagi `seq_scan` va `n_dead_tup` kuzatiladi: birinchisining o'sishi yo'qolgan index, ikkinchisining o'sishi autovacuum yetishmayotgani haqida gapiradi.

### 27.10 `pg_stat_statements` ni yoqish va undan muntazam foydalanish

Bu extension production diagnostikasining asosi va restart talab qiladi, shuning uchun uni birinchi kundan yoqish kerak. U so'rovlarni normallashtirib `queryid` bo'yicha yig'adi, natijada "sekin so'rov" emas, "umumiy vaqtni eng ko'p yeydigan so'rov" ko'rinadi. Tizimni sekinlashtirgan narsa odatda bitta 3 sekundli hisobot emas, kuniga 2 million marta bajarilgan 4 ms li so'rovdir.

```sql
-- shared_preload_libraries = 'pg_stat_statements'  (restart kerak)
-- pg_stat_statements.max = 5000 ; .track = top
CREATE EXTENSION IF NOT EXISTS pg_stat_statements;

-- Umumiy vaqt bo'yicha top 10: optimizatsiya shu ro'yxatdan boshlanadi
SELECT round(total_exec_time)::bigint AS total_ms, calls, rows,
       round(mean_exec_time, 2) AS mean_ms,
       round(stddev_exec_time, 2) AS stddev_ms,
       left(query, 80) AS query
FROM pg_stat_statements
ORDER BY total_exec_time DESC LIMIT 10;

-- Relizdan oldin va keyin solishtirish uchun nolga tushirish
SELECT pg_stat_statements_reset();
```

Muntazam amaliyot: har kuni bir vaqtda snapshot olib alohida jadvalga yozish, keyin oldingi snapshot bilan ayirmasini hisoblash. Shunda "bu so'rov relizdan keyin 3 barobar ko'p chaqirilyapti" degan xulosa chiqadi, N+1 esa `calls` ustunidagi keskin o'sish sifatida ko'rinadi. `stddev_exec_time` ning kattaligi so'rov plan almashtirayotganini bildiradi.

### 27.11 Sekin so'rov logi va `auto_explain` sozlash

Sekin so'rov logi `pg_stat_statements` ni to'ldiradi, chunki u konkret parametr qiymatlari bilan konkret holatni ko'rsatadi. `log_min_duration_statement` ni 200 ms ga qo'yish OLTP da yaxshi muvozanat, log hajmi katta bo'lsa `log_min_duration_sample` va `log_statement_sample_rate` bilan namuna olinadi.

```properties
log_min_duration_statement = 200ms   # 200 ms dan uzoq hamma so'rov
log_lock_waits = on                  # deadlock_timeout dan uzoq lock kutishlari
log_temp_files = 0                   # har qanday temp fayl: work_mem signali
log_line_prefix = '%m [%p] %u@%d app=%a '   # korrelyatsiya uchun shart

shared_preload_libraries = 'pg_stat_statements,auto_explain'
auto_explain.log_min_duration = '500ms'
auto_explain.log_analyze = on        # haqiqiy qatorlar, lekin overhead bor
auto_explain.log_timing = off        # overhead ni kamaytirish uchun o'chiriladi
auto_explain.log_buffers = on
auto_explain.log_nested_statements = on   # ORM ichidagi so'rovlar uchun
auto_explain.sample_rate = 0.05      # yuklamali tizimda 5 foiz yetarli
```

`auto_explain.log_analyze = on` haqiqiy qator sonlarini yozadi, ya'ni planner taxmini bilan reallik orasidagi farq ko'rinadi, va shu farq statistika eskirganini aniqlaydi. Lekin `log_timing` har bir node uchun vaqt o'lchaydi va yuklamali serverda sezilarli overhead beradi, shuning uchun uni off qoldirib `sample_rate` ni past tutish to'g'ri. `log_line_prefix` da `app=%a` bo'lsa, so'rov qaysi servisdan kelganini log'dan ajratish mumkin.

| Tuzoq | Oqibat | Yechim |
|---|---|---|
| Global `work_mem` ni 256MB qilish | OOM, server o'ladi | Global 24MB, role darajasida ko'tarish |
| `connection-timeout` 30s | Thread'lar band, kaskad nosozlik | 3s va fallback |
| `max-lifetime` LB limitidan katta | Tasodifiy "connection reset" | LB limitidan 5 daqiqa kichik qilish |
| PgBouncer transaction rejimi + server prepared statement | "prepared statement does not exist" | `max_prepared_statements` yoki `prepareThreshold=0` |
| Timeout'siz `idle in transaction` | Bloat, VACUUM ishlamaydi | `idle_in_transaction_session_timeout = 30s` |
| `auto_explain.log_timing = on` | Katta CPU overhead | off + `sample_rate = 0.05` |
| Pool'lar yig'indisi > `max_connections` | "too many clients already" | Pod soni x pool ni hisoblab chegaralash |
| Backup bor, restore sinovdan o'tmagan | RTO noma'lum, tiklanish amalda ishlamaydi | Chorakda restore drill |

### 27.12 Zaxira nusxa va tiklanish: `pg_basebackup`, PITR, tiklanishni sinab ko'rish majburiyati

Streaming replikatsiya backup emas, chunki u mantiqiy xatoni ham ko'chiradi: noto'g'ri `DELETE` replikada ham bajariladi. Fizik backup va WAL arxivi kerak: `pg_basebackup` to'liq nusxa oladi, WAL arxivi esa shu nuqtadan keyin istalgan vaqtga qaytish imkonini beradi, ya'ni PITR.

```bash
# To'liq fizik backup: tar + gzip, WAL ni oqim bilan
pg_basebackup -h pg-primary -U replicator -D /backup/base-$(date +%F) \
  -Ft -z -Xs -c fast -P --write-recovery-conf

pg_verifybackup /backup/base-2026-10-04   # butunlikni tekshirish: majburiy

# PITR: bazani tiklab, kerakli vaqtga to'xtatish
# postgresql.conf ichida:
#   restore_command = 'cp /archive/%f %p'
#   recovery_target_time = '2026-10-04 11:42:00+05'
#   recovery_target_action = 'promote'
touch /var/lib/postgresql/data/recovery.signal   # recovery rejimini yoqadi
pg_ctl -D /var/lib/postgresql/data start
psql -c "SELECT pg_is_in_recovery(), pg_last_wal_replay_lsn();"
```

Raqamlarni oldindan belgilash kerak. WAL arxivini har 60 sekundda yuborsang, RPO taxminan 1 daqiqa. 500 GB bazani 1 GB/s tarmoqda tiklash taxminan 10 daqiqa, ustiga WAL replay qo'shilib, RTO realistik holda 30 daqiqadan 60 daqiqagacha. Bu raqamlarni taxmin qilish mumkin emas, ularni o'lchash kerak, o'lchashning yagona yo'li esa haqiqiy tiklanish mashqi: chorakda bir marta alohida serverga backup'dan tiklab, to'lov va buyurtma jadvallaridagi qator sonini va oxirgi tranzaksiya vaqtini tekshirish. Katta bazalarda `pgBackRest` yoki `barman` inkremental backup, parallel siqish va saqlash siyosatini o'zi boshqaradi, shuning uchun qo'lda skript yozishdan ko'ra ularni tanlash oqilona.

### 27.13 Amalda qo'llash

- [ ] Serverning RAM va vCPU miqdoridan kelib chiqib `shared_buffers`, `effective_cache_size`, `work_mem`, `maintenance_work_mem` ni hisoblab qo'y va `pg_settings` orqali tasdiqla.
- [ ] Hisobot va batch uchun alohida role yarat, ularga `work_mem` va `statement_timeout` ni `ALTER ROLE` bilan belgila, OLTP role'ini qisqa timeout'da qoldir.
- [ ] Har bir servis uchun pool kattaligini `RPS x DB_vaqti` bilan hisobla, pod soniga ko'paytirib yig'indisi `max_connections` dan kichik ekanini tekshir.
- [ ] HikariCP da `connection-timeout` ni 3000 ms, `max-lifetime` ni infratuzilma limitidan 5 daqiqa kichik, `leak-detection-threshold` ni 20000 ms qilib qo'y.
- [ ] `idle_in_transaction_session_timeout` va `lock_timeout` ni ilova role'ida yoq, bir hafta log'dagi uzilgan tranzaksiyalarni ko'rib chiqib sabablarini tuzat.
- [ ] `pg_stat_statements` va `auto_explain` ni yoq, kunlik snapshot yig'adigan ish qo'y, top 10 so'rovni haftalik ko'rikka kirit.
- [ ] Kesh hit nisbati, `temp_bytes`, `deadlocks`, eng uzun tranzaksiya yoshi va pool kutish vaqti uchun alert qoidalarini yoz.
- [ ] Chorakda bir marta `pg_basebackup` dan PITR mashqini o'tkaz, RTO va RPO ni o'lchab hujjatga yoz.


# V. Atrof ekotizim: operatsion haqiqat

## 28. Keshlash amaliyoti: invalidatsiya, stampede, Redis haqiqati (Caching in Practice)

Kesh tizimga tezlik qo'shmaydi, u faqat sekinlikni yashiradi. Yashirilgan sekinlik kesh sovib qolgan paytda, odatda eng yuqori yuklamada, to'liq kuch bilan qaytib keladi. Shuning uchun kesh qarori "qancha tez bo'ladi" emas, "qanday nomuvofiqlikka va operatsion yukka rozi bo'lamiz" degan savol. Bu bobda raqamlar, sozlash parametrlari va kesh joriy qilgandan keyin chiqadigan tuzoqlar ko'rib chiqiladi.

### 28.1 Kesh qo'yishdan oldin so'raladigan savollar

Kesh ko'p holda profiling o'rniga qo'yiladi. Buyurtma ro'yxati 800 ms ishlayotgan bo'lsa, birinchi ish sababini topish: N+1 so'rovmi, index yo'qligimi, yoki og'ir agregatsiyami. N+1 bo'lsa kesh muammoni yashiradi, lekin ro'yxat eski qolaveradi va siz ikkita muammoga ega bo'lasiz.

Savollar ro'yxati qisqa. Bu ma'lumot qancha vaqt eskirishi mumkin. O'qish va yozish nisbati qanday. Qiymat hajmi kilobaytmi yoki megabaytmi. Eski qiymat ko'rsatilsa biznesda nima buziladi. Ombor qoldig'i uchun javob odatda "keshlamaymiz", chunki minusga sotib qo'yish narxi keshdan kelgan foydadan katta.

| Savol | Oddiy yondashuv | Arxitektor yondashuvi |
| --- | --- | --- |
| Nega sekin | Kesh qo'yadi | Avval `EXPLAIN ANALYZE` va profil oladi |
| Kesh nimaga qo'yiladi | "Tezlashtirish uchun" | DB yuklamasini N barobar kamaytirish uchun, raqam bilan |
| TTL qiymati | Hammaga 60 soat yoki 1 kun | Har kesh nomiga biznesdan so'ralgan eskirish chegarasi |
| Hit nisbati | O'lchanmaydi | Metrika bilan kuzatiladi, 0.9 dan past bo'lsa qayta ko'riladi |
| Invalidatsiya | `@CacheEvict` qo'yiladi va unutiladi | Commit dan keyin, kalit egasi servis ichida |
| Stampede | O'ylanmaydi | `sync`, jitter yoki taqsimlangan lock bilan yopiladi |
| Redis o'chsa | Tizim 500 qaytaradi | Zaxira yo'l DB ga tushadi, latency oshadi, xizmat tirik |
| Qiymat hajmi | Butun entity grafi | Faqat kerakli maydonlardan DTO |
| Xotira | Chegara yo'q | `maxmemory` va eviction siyosati aniq belgilangan |
| Kesh kaliti | `toString()` ga tayanadi | Aniq, versiyalangan, prefiksli kalit |

### 28.2 Hit nisbati qanchadan boshlab foyda beradi

Hisob oddiy formula bilan qilinadi. O'rtacha latency teng: `h * T_kesh + (1 - h) * (T_kesh + T_db)`. Bir ma'lumot markazi ichida Redis uchun `T_kesh` taxminan 1 ms, og'ir agregatsiya uchun `T_db` taxminan 40 ms deb olamiz.

| Hit nisbati | O'rtacha latency | DB ga tushadigan QPS (10 000 QPS dan) |
| --- | --- | --- |
| 0.50 | taxminan 21 ms | 5 000 |
| 0.80 | taxminan 9 ms | 2 000 |
| 0.90 | taxminan 5 ms | 1 000 |
| 0.95 | taxminan 3 ms | 500 |
| 0.99 | taxminan 1.4 ms | 100 |

Jadvaldan ikki xulosa chiqadi. Latency bo'yicha foyda 0.8 dan keyin to'yinadi, 0.9 dan 0.95 ga ko'tarilish foydalanuvchi uchun 2 ms beradi. DB yuklamasi bo'yicha foyda to'xtamaydi, 0.9 dan 0.99 ga o'tish DB so'rovini yana 10 barobar kamaytiradi. Maqsad latency bo'lsa 0.85 atrofi yetarli, maqsad DB ni saqlab qolish bo'lsa 0.97 dan past natija yetarli emas.

Teskari holat ham bor. `T_db` birlamchi kalit bo'yicha 2 ms bo'lsa, foyda bor yo'g'i 1 ms. Bunday joyga tarmoq orqali kesh qo'yish faqat nomuvofiqlik va yana bitta ishdan chiqish nuqtasini qo'shadi.

### 28.3 Mahalliy kesh va taqsimlangan kesh tanlovi

Caffeine JVM ichida ishlaydi, o'qish taxminan 100 nanosekund turadi, tarmoq ham serializatsiya ham yo'q. Narxi shu: 12 ta pod bo'lsa, 12 ta mustaqil kesh nusxasi bor va ularning invalidatsiyasi bir vaqtda bo'lmaydi. Shuning uchun mahalliy kesh faqat qisqa TTL bilan ishlatiladi.

Amalda bo'linish shunday. Valyuta kursi, soliq stavkasi, kategoriyalar va feature flag mahalliy keshga tushadi, TTL 30 soniyadan 5 minutgacha. Sessiya, idempotentlik kaliti va rate limit hisoblagichi Redis ga tushadi, chunki hamma pod ularni bir xil ko'rishi shart.

```java
@Configuration
@EnableCaching
class KeshSozlamasi {

  // Mahalliy kesh: qisqa TTL, qattiq hajm chegarasi, statistika yoqilgan
  @Bean
  CacheManager mahalliyKesh() {
    CaffeineCacheManager m = new CaffeineCacheManager("valyutaKursi", "soliqStavkasi");
    m.setCaffeine(Caffeine.newBuilder()
        .maximumSize(10_000)              // taxminan 10k * 500 bayt = 5 MB
        .expireAfterWrite(Duration.ofMinutes(2))
        .refreshAfterWrite(Duration.ofSeconds(90)) // fon rejimida yangilash
        .recordStats());                  // hit nisbatini o'lchash uchun shart
    return m;
  }
}
```

`recordStats()` chaqirilmasa hit nisbati ko'rinmaydi va siz kesh foydasini isbotlay olmaysiz. `refreshAfterWrite` muddati `expireAfterWrite` dan kichik bo'lishi shart, aks holda ishga tushmaydi.

### 28.4 Spring Cache abstraksiyasi mexanikasi va proxy chegarasi

`@Cacheable` hech qanday sehr qilmaydi. Spring bean atrofida proxy yaratadi, chaqiruv proxy ga kelganda kalit hisoblanadi, `Cache.get` chaqiriladi, qiymat bo'lsa metod ishga tushmaydi. `key` ifodasi berilmasa kalit barcha argumentlardan tuziladi va ularning `equals` bilan `hashCode` iga tayanadi. Entity ni argument qilib berish shuning uchun xavfli, uning `hashCode` i o'zgaruvchan.

Proxy chegarasi eng ko'p xato keltiradigan joy. Sinf o'z ichidagi `@Cacheable` metodni `this` orqali chaqirsa, chaqiruv proxy dan o'tmaydi va kesh chetlab o'tiladi. Xato jim kechadi, faqat hit nisbati nolga teng bo'lib turadi.

```java
@Service
public class HisobotServisi {

  // Kalit aniq yozilgan, argument primitiv turda
  @Cacheable(cacheNames = "kunlikSavdo", key = "#sanaIso + ':' + #filialId", sync = true)
  public SavdoHisoboti kunlikSavdo(String sanaIso, long filialId) {
    return agregatsiyaniHisobla(sanaIso, filialId); // taxminan 400 ms
  }

  public List<SavdoHisoboti> haftalik(long filialId, List<String> kunlar) {
    // this.kunlikSavdo(...) proxy dan o'tmaydi va kesh butunlay chetlab o'tiladi
    return kunlar.stream().map(k -> ozi.kunlikSavdo(k, filialId)).toList();
  }

  @Autowired @Lazy private HisobotServisi ozi; // oxirgi chora, afzali alohida bean
}
```

Yana bir tafsilot: metod `null` qaytarsa, Spring odatda `null` ni ham keshlaydi. Redis uchun `RedisCacheConfiguration` da `disableCachingNullValues()` chaqirilsa, mavjud bo'lmagan kalit har marta DB ga boradi. Mavjud bo'lmagan ID bilan hujum qilinsa bu DB ni urishga aylanadi, shuning uchun "yo'q" javobini qisqa TTL bilan keshlash to'g'ri qaror.

### 28.5 Invalidatsiya: muddat, hodisa va versiya kaliti bo'yicha

Uch usul bor va ular bir birini almashtirmaydi. Muddat bo'yicha invalidatsiya eng ishonchli, chunki u koddan bog'liq emas. Narxi aniq: TTL qancha bo'lsa, eskirish oynasi shuncha. Hisobot uchun 5 minut, narx uchun 30 soniya, kategoriya daraxti uchun 1 soat odatiy qiymatlar.

Hodisa bo'yicha invalidatsiya aniq, lekin mo'rt. Buyurtma o'zgarganda faqat buyurtma keshi emas, filial savdosi va mijoz statistikasi ham eskiradi. Bitta joy esdan chiqsa ma'lumot cheksiz eskirib qoladi, shuning uchun hodisa bo'yicha tozalash har doim TTL ustiga qo'yiladi, uning o'rniga emas.

Versiya kaliti eng mustahkam usul. Kesh kalitiga guruh versiyasi qo'shiladi, o'zgarish bo'lganda versiya oshiriladi va eski kalitlar o'z o'zidan ishlatilmay qoladi. Eski yozuvlar TTL yoki eviction bilan ketadi. Bu usul ommaviy o'chirishni keraksiz qiladi.

```java
@Service
@RequiredArgsConstructor
public class NarxKeshi {

  private final StringRedisTemplate redis;

  // Versiya kaliti kesh kaliti ichiga kiradi
  public String kalit(long filialId, long tovarId) {
    String v = redis.opsForValue().get("ver:narx:" + filialId);
    if (v == null) { v = "1"; redis.opsForValue().setIfAbsent("ver:narx:" + filialId, v); }
    return "narx:v" + v + ":" + filialId + ":" + tovarId;
  }

  // Bitta INCR: hamma eski kalit bir zumda ahamiyatsiz bo'ladi
  public void filialNarxlariOzgardi(long filialId) {
    redis.opsForValue().increment("ver:narx:" + filialId);
  }
}
```

### 28.6 Kesh stampede va undan himoya usullari

Stampede shunday sodir bo'ladi. Og'ir hisobot keshi TTL tugashi bilan bo'shaydi, shu millisekundda 300 ta parallel so'rov keladi va hammasi DB ga tushadi. DB connection pool 20 ta ulanishdan iborat bo'lsa, navbat o'sadi, timeout boshlanadi va kesh o'zi avariya sababiga aylanadi.

Birinchi himoya `@Cacheable(sync = true)`. U bir JVM ichida bir kalit uchun faqat bitta hisoblashga yo'l beradi, qolganlari natijani kutadi. Kafolat faqat pod ichida, 12 ta pod bo'lsa DB ga 12 ta so'rov boradi. Ko'p hollarda 300 dan 12 ga tushish yetarli.

Ikkinchi himoya TTL ga jitter qo'shish. Hamma kalitga aynan 300 soniya berilsa, ular birgalikda bo'shaydi va to'lqin paydo bo'ladi. TTL ni 300 va 360 soniya orasida tasodifiy tanlash to'lqinni yoyadi. Uchinchi himoya taqsimlangan lock, u faqat 1 soniyadan uzun hisoblash uchun ishlatiladi, chunki o'zi ham tarmoq chaqiruvi qo'shadi.

```java
// Faqat 1 soniyadan uzun hisoblash uchun: bitta egalik, qolganlar eski qiymat bilan
public SavdoHisoboti olish(String kalit) {
  SavdoHisoboti bor = keshdanOq(kalit);
  if (bor != null && !eskirishgaYaqin(bor)) return bor;

  // SET NX PX: atomar egallash, 10 soniyada o'z o'zidan bo'shaydi
  Boolean egallandi = redis.opsForValue()
      .setIfAbsent("lock:" + kalit, nodeId, Duration.ofSeconds(10));

  if (!Boolean.TRUE.equals(egallandi)) {
    return bor != null ? bor : kutibQaytaOq(kalit, Duration.ofMillis(300));
  }
  try {
    SavdoHisoboti yangi = agregatsiyaniHisobla(kalit);
    keshgaYoz(kalit, yangi, Duration.ofMinutes(5));
    return yangi;
  } finally {
    ozLockiniOchir("lock:" + kalit, nodeId); // faqat o'z lock ini o'chirish
  }
}
```

### 28.7 Eskirgan ma'lumotni ko'rsatish siyosati

Eng muhim qaror texnik emas, biznes qarori. Savol aniq qo'yilishi kerak: bu raqam 30 soniya eski bo'lsa kim zarar ko'radi. Boshqaruv panelidagi buyurtma soni uchun 60 soniya eskirish xalal bermaydi. To'lov balansi uchun esa eskirish mijoz da'vosiga aylanadi.

Shuning uchun har kesh nomi uchun ikki raqam yoziladi: odatdagi TTL va DB ishlamay qolganda eski qiymatni ishlatish chegarasi. Hisobotlar uchun bu 5 minut va 30 minut bo'lishi mumkin. Interfeysda "ma'lumot 14:05 holatiga" degan yozuv qo'shilsa, eskirish muammo bo'lishdan chiqib xususiyatga aylanadi.

### 28.8 Kesh va tranzaksiya nomuvofiqligi

Eng ko'p uchraydigan jim xato shu: kesh tranzaksiya ichida tozalanadi, keyin tranzaksiya rollback bo'ladi. Keyingi o'qish DB dan eski qiymatni olib keshga qaytaradi va nomuvofiqlik qotib qoladi. Rollback kam bo'lgani uchun bu testda ko'rinmaydi, produksiyada esa vaqti vaqti bilan tushunarsiz natija beradi.

To'g'ri yechim keshni commit dan keyin o'zgartirish. Spring da buning mexanizmi bor, `@TransactionalEventListener` ning `AFTER_COMMIT` fazasi. U tranzaksiya muvaffaqiyatli yakunlangandan keyin ishlaydi, rollback da umuman chaqirilmaydi.

```java
@Service
@RequiredArgsConstructor
public class BuyurtmaServisi {

  private final ApplicationEventPublisher nashriyot;

  @Transactional
  public void yetkazildiDebBelgila(long buyurtmaId) {
    buyurtmaRepo.statusniOzgartir(buyurtmaId, Status.YETKAZILDI);
    // Kesh hozir tozalanmaydi, faqat hodisa e'lon qilinadi
    nashriyot.publishEvent(new BuyurtmaOzgardi(buyurtmaId));
  }
}

@Component
@RequiredArgsConstructor
class KeshTozalovchi {
  private final CacheManager keshlar;

  // AFTER_COMMIT: rollback bo'lsa bu metod umuman chaqirilmaydi
  @TransactionalEventListener(phase = TransactionPhase.AFTER_COMMIT)
  public void buyurtmaOzgardi(BuyurtmaOzgardi h) {
    keshlar.getCache("buyurtma").evict(h.buyurtmaId());
    keshlar.getCache("mijozStatistikasi").evict(h.mijozId());
  }
}
```

Yana bir tafsilot. Replikadan o'qiyotgan bo'lsangiz, commit dan keyin kesh darhol to'ldirilsa, replika lag i sababli eski qiymat keshga tushadi. Shuning uchun commit dan keyin faqat tozalash xavfsizroq, keyingi o'qish o'zi to'ldiradi.

### 28.9 Redis operatsion haqiqati: xotira, eviction va bitta thread

Redis buyruqlarni bitta thread da bajaradi. Atomarlik bepul keladi, lekin bitta sekin buyruq butun serverni to'xtatib turadi. 100 ming elementli ro'yxat ustida `LRANGE 0 -1` yoki katta kalitni `DEL` qilish o'n millisekundlar olishi mumkin, va shu vaqtda hamma mijoz kutadi.

`maxmemory` belgilanmagan Redis eng xavfli konfiguratsiya. U xotira tugaguncha o'sadi, keyin operatsion tizim uni o'ldiradi yoki swap ga tushib latency yuz barobar oshadi. Kesh uchun `maxmemory` fizik xotiraning taxminan 70 foizi qilib qo'yiladi, qolgani fragmentatsiya va buferlarga kerak.

Eviction siyosati kesh va navbat uchun boshqacha. Toza kesh uchun `allkeys-lru` yoki `allkeys-lfu` to'g'ri, joy tugaganda eski kalit chiqib ketadi. Idempotentlik kaliti yoki navbat saqlanadigan Redis da `allkeys-lru` ma'lumot yo'qotadi, u yerda `noeviction` va alohida instance kerak.

```bash
# Xotira va fragmentatsiya holati
redis-cli info memory | grep -E 'used_memory_human|maxmemory_human|mem_fragmentation_ratio'

# Kesh uchun: chegara, LRU, fon rejimida bo'shatish
redis-cli config set maxmemory 6gb
redis-cli config set maxmemory-policy allkeys-lru
redis-cli config set lazyfree-lazy-eviction yes

# Hit nisbati va chiqarib tashlangan kalitlar soni
redis-cli info stats | grep -E 'evicted_keys|keyspace_hits|keyspace_misses'

# 10 ms dan uzun buyruqlarni yozib borish
redis-cli config set slowlog-log-slower-than 10000
redis-cli slowlog get 10
```

`evicted_keys` o'sib borayotgan bo'lsa hit nisbati tushadi va DB yuklamasi jim oshadi. Bu metrika doimiy kuzatiladigan ro'yxatda bo'lsin.

### 28.10 Katta kalit, uzun ro'yxat va KEYS buyrug'i xavfi

`KEYS *` produksiyada ishga tushirilmaydi. U butun keyspace ni bitta thread da aylanib chiqadi, million kalitda bu bir necha soniya, va shu vaqtda Redis javob bermaydi. O'rniga kursor bilan yuradigan `SCAN` ishlatiladi. Spring tomonida ham shunga mos holat bor: Redis da butun kesh nomini tozalash prefiks bo'yicha skan va o'chirishga aylanadi, shuning uchun katta kesh ustida `@CacheEvict(allEntries = true)` arzon emas.

Katta kalit ikkinchi tuzoq. 10 MB lik JSON ni bitta kalitga yozish tarmoqni, serializatsiyani va bitta thread ni birdan uradi. Amaliy chegara: kesh qiymati taxminan 100 KB dan oshmasin, 1 MB esa kalitni bo'laklash signali.

| Tuzoq | Nimaga olib keladi | Yechim |
| --- | --- | --- |
| `KEYS` yoki keng `allEntries` tozalash | Redis bir necha soniya javob bermaydi | `SCAN`, yoki versiya kaliti bilan tozalashsiz invalidatsiya |
| 5 MB lik kesh qiymati | Tarmoq va bitta thread to'yinadi, latency sakraydi | Kerakli maydonlardan DTO, sahifalab bo'lish |
| `maxmemory` belgilanmagan | OOM yoki swap, latency yuz barobar | Chegara fizik xotiraning 70 foizi, LRU siyosati |
| Hamma kalitga bir xil TTL | TTL tugaganda to'lqin, DB ga stampede | TTL ga 10 dan 20 foiz jitter |
| Entity ni kesh kaliti qilish | Kutilmagan kalitlar, nol hit nisbati | Primitiv argumentlardan aniq `key` ifodasi |
| Tranzaksiya ichida `@CacheEvict` | Rollback dan keyin keshda eski qiymat | `AFTER_COMMIT` fazasida tozalash |
| `null` ni keshlamaslik | Mavjud bo'lmagan ID bilan DB ni urish | "Yo'q" javobini 30 soniyaga keshlash |
| Navbat va kesh bir Redis da | LRU idempotentlik kalitini o'chiradi | Alohida instance, `noeviction` siyosati |
| Timeout sozlanmagan | Redis sekinlashsa butun thread pool bloklanadi | Komanda timeout 100 dan 200 ms gacha |

### 28.11 Serializatsiya tanlovi va kesh qiymati hajmi

JDK serializatsiyasi eng yomon tanlov. Natija JSON dan katta, boshqa tildan o'qilmaydi, va sinf tuzilishi o'zgarganda deploy paytida eski yozuvlar xatolik beradi. Kesh uchun JSON ishlatiladi, u `redis-cli` dan ko'rinadi va debug qilinadi.

JSON ning narxi ham bor. Tur ma'lumoti saqlanadigan variantda har yozuvga sinf nomi qo'shiladi va kichik qiymatlarda ustama 30 foizga yetadi. Ikkinchi xavf shu: sinf nomi qiymat ichida saqlansa, paket nomini o'zgartirish barcha kesh yozuvini o'qilmas qiladi.

Amaliy qoida: keshga entity emas, barqaror DTO yoziladi. Buyurtma kartochkasi uchun bu taxminan 15 maydon, 600 bayt atrofida. Butun entity ni mijoz, manzil va qatorlar grafi bilan yozsangiz, o'sha narsa 20 KB ga chiqadi. 500 ming kalit uchun farq 300 MB va 10 GB orasida.

```yaml
spring:
  data:
    redis:
      timeout: 150ms          # Redis sekinlashsa tez taslim bo'lish
      connect-timeout: 200ms
      lettuce:
        pool:
          max-active: 16      # Lettuce multiplekslaydi, katta pool kerak emas
          max-idle: 8
          max-wait: 100ms     # cheksiz kutmaslik
  cache:
    type: redis
    redis:
      time-to-live: 300s      # standart TTL, kesh nomi bo'yicha alohida sozlanadi
      cache-null-values: true # mavjud emas javobini ham keshlash
      key-prefix: "sotuv:"
```

Timeout bu yerda eng muhim qator. Redis sekinlashsa chaqiruvchi thread uzoq kutadi, servlet thread pool to'ladi va butun servis javob bermay qoladi. 150 ms timeout bilan kesh chaqiruvi tez xato beradi va siz zaxira yo'lga o'tasiz.

### 28.12 Kesh ishlamay qolganda tizim yiqilmasligi

Kesh ixtiyoriy komponent bo'lishi kerak, majburiy emas. Redis o'chganda to'lov servisi to'xtasa, siz tezlik uchun ishonchlilikni sotib bo'lgansiz. Spring da bunga javob bor, `CacheErrorHandler` interfeysi. U kesh xatosini tutadi va tanlov beradi: xatoni yuqoriga chiqarish yoki log yozib metodni odatdagicha ishga tushirish.

```java
@Configuration
@EnableCaching
class KeshXatoSozlamasi implements CachingConfigurer {

  private static final Logger log = LoggerFactory.getLogger(KeshXatoSozlamasi.class);

  @Override
  public CacheErrorHandler errorHandler() {
    return new CacheErrorHandler() {
      // O'qishda xato: kesh yo'q deb hisoblanadi, metod DB ga boradi
      public void handleCacheGetError(RuntimeException e, Cache c, Object key) {
        log.warn("kesh o'qish xatosi, kesh={} kalit={}", c.getName(), key, e);
      }
      public void handleCachePutError(RuntimeException e, Cache c, Object key, Object v) {
        log.warn("kesh yozish xatosi, kesh={}", c.getName(), e);
      }
      // Tozalashda xato jiddiyroq: eski qiymat keshda qolib ketishi mumkin
      public void handleCacheEvictError(RuntimeException e, Cache c, Object key) {
        log.error("kesh tozalash xatosi, kalit={} eskirish xavfi bor", key, e);
      }
      public void handleCacheClearError(RuntimeException e, Cache c) {
        log.error("to'liq tozalash xatosi, kesh={}", c.getName(), e);
      }
    };
  }
}
```

Lekin xatoni yutish yetarli emas. Redis o'chganda hit nisbati nolga tushadi va 10 000 QPS ning hammasi DB ga boradi. DB bunga tayyor emas. Shuning uchun zaxira yo'lda ikki himoya kerak: og'ir so'rovlar uchun semafor bilan parallellik chegarasi, va eng qimmat hisobotlar uchun mahalliy Caffeine qatlami. Mexanizmlarning o'zi dizayn patternlar hujjatida, bu yerda muhimi shu: zaxira yo'l ham sig'im hisobiga ega bo'lsin.

Zaxira yo'l yozilgan bo'lsa yetarli emas, u sinovdan o'tishi kerak. Produksiyaga o'xshash muhitda Redis ni ataylab o'chirib, latency va DB connection pool holatini o'lchash kerak. Texnikani testlash qo'llanmasidagi resilience testlari bo'limi beradi, arxitektorning ishi bu sinovni rejaga kiritish.

### 28.13 Amalda qo'llash

- [ ] Har bir `@Cacheable` metod uchun jadval tuz: kesh nomi, TTL, kutilayotgan hit nisbati, toqat qilinadigan eskirish, qiymat hajmi. Bo'sh katak qolsa, o'sha kesh asossiz.
- [ ] Kesh qo'yishdan oldin so'rovni `EXPLAIN (ANALYZE, BUFFERS)` bilan o'lcha, N+1 yoki yo'q index emasligini isbotlab tiketga yoz.
- [ ] Caffeine da `recordStats()` yoq, Redis da `keyspace_hits`, `keyspace_misses`, `evicted_keys` ni metrikaga chiqar va hit nisbatiga ogohlantirish chegarasi qo'y.
- [ ] `@CacheEvict` chaqiruvlarini tranzaksiya ichidan `AFTER_COMMIT` fazasiga ko'chir, rollback holatini bitta test bilan yop.
- [ ] Eng qimmat uchta keshga `sync = true` va TTL ga 10 dan 20 foizgacha jitter qo'sh, bo'sh kesh ustiga yuklama berib DB so'rovini o'lch.
- [ ] `maxmemory` ni fizik xotiraning 70 foizida, siyosatni `allkeys-lru` da belgila, navbat va idempotentlik kalitlarini alohida instance ga ko'chir.
- [ ] Komanda timeout ini 100 dan 200 ms orasida sozla, `CacheErrorHandler` ni ula, Redis o'chirilgan holatda kritik yo'lni sinab ko'r.
- [ ] Kesh qiymatlarini entity dan barqaror DTO ga o'tkaz, eng katta kalitlarni `MEMORY USAGE` bilan o'lchab, 100 KB dan oshganini bo'lakla.

## 29. Kafka operatsion haqiqati: partition, lag, rebalance, idempotentlik (Kafka in Production)

Kafka ko'pchilik loyihada "xabar navbati" deb tushuniladi, lekin u aslida taqsimlangan, saqlanadigan va qayta o'qiladigan log. Shu farqni tushunmagan jamoa partition sonini tasodifiy tanlaydi, offset ni avtomatik commit qiladi, rebalance paytida xabarlarni ikki marta ishlaydi va dead letter topic ni hech kim o'qimaydi. Bu bob Kafka ning operatsion mexanikasini ko'rib chiqadi: ichkarida nima sodir bo'ladi, qaysi sozlama qanday raqamga ta'sir qiladi va arxitektor qaysi joyda qaror qabul qilishi kerak. To'lov servisi, buyurtma oqimi va ombor qoldig'i misollari orqali boramiz.

### 29.1 Kafka modeli: topic, partition, offset, consumer group

Topic nomdan boshqa hech narsa emas, u faqat partition ro'yxatini birlashtiradi. Haqiqiy birlik partition: u broker diskidagi append-only segment fayllar ketma-ketligi. Har bir yozuv partition ichida monoton o'suvchi `offset` oladi, va bu offset o'zgarmaydi hamda qayta ishlatilmaydi. Shuning uchun Kafka da xabar "o'chirilmaydi", u faqat `retention.ms` yoki `retention.bytes` chegarasidan oshganda segment bilan birga tashlanadi.

Consumer group ikkita vazifani bajaradi. Birinchisi: partition larni group a'zolari o'rtasida taqsimlash, bitta partition bir vaqtda bitta a'zoga tegishli. Ikkinchisi: group nomi bo'yicha offset ni `__consumer_offsets` ichki topic da saqlash. Shundan muhim xulosa chiqadi: bir xil ma'lumotni ikki xil maqsadda ishlatmoqchi bo'lsang, ikkita alohida `group.id` olasan, ularning offset lari bir-biriga aralashmaydi. To'lov tasdiqlarini bir group hisob-kitob uchun, boshqa group hisobot uchun o'qiydi va ular bir-birini sekinlashtirmaydi.

Broker hech qachon "bu xabarni kim o'qidi" ni bilmaydi. U faqat group ning commit qilgan offset ini biladi. Bu arxitektura bir nechta oqibat beradi: iste'molchi orqaga qaytib o'qishi mumkin, offset ni qo'lda siljitib reprocessing qilish mumkin, va "xabar yo'qoldi" degan muammolar deyarli har doim offset boshqaruvidagi xato bo'lib chiqadi.

### 29.2 Partition soni tanlash: parallellik chegarasi va keyin o'zgartirish qiyinligi

Bitta consumer group ichidagi samarali parallellik partition sonidan oshmaydi. Agar topic da 6 partition bo'lsa, 10 instansiya ishga tushirsang, 4 tasi bo'sh turadi. Shuning uchun partition soni kelgusidagi eng katta instansiya sonidan kamida 2-3 barobar ko'p bo'lishi kerak. Buyurtma topic uchun amaliy boshlang'ich nuqta: 12 yoki 24 partition, chunki ular 2, 3, 4, 6, 8, 12 instansiyaga teng bo'linadi.

Lekin partition bepul emas. Har bir partition broker da ochiq fayl deskriptorlari, alohida index va replikatsiya uchun fetch oqimi talab qiladi. Bitta broker da bir necha ming partition replikasi bo'lsa, controller ishi va ishga tushish vaqti sezilarli oshadi. Amaliy mo'ljal: bitta broker ga 2000-4000 partition replikasi, klaster bo'ylab 50000 dan oshmaslik. Producer tomonida ham har partition uchun alohida batch buferi ushlanadi, ya'ni `batch.size` ni partition soniga ko'paytirib xotirani hisobla.

Eng og'ir tuzoq: partition sonini oshirish mumkin, kamaytirish mumkin emas. Oshirganda esa standart partitioner `hash(key) % partitionCount` ishlatgani uchun kalitlarning partition ga tushishi o'zgaradi. Bu degani eski xabarlar bir partition da, yangi xabarlar boshqa partition da qoladi va bitta buyurtma uchun tartib buziladi. Shuning uchun partition sonini production da jimgina oshirish xavfli qaror. To'g'ri yo'l: yangi topic yaratish, ikkita topic ni parallel o'qish va ma'lum bir vaqtdan keyin eskisini o'chirish.

### 29.3 Kalit tanlash va tartib kafolati: tartib faqat partition ichida

Kafka global tartibni kafolatlamaydi. U faqat bitta partition ichida yozuv tartibini kafolatlaydi. Shuning uchun "buyurtma hodisalari to'g'ri ketma-ketlikda kelishi kerak" talabi to'g'ridan-to'g'ri kalit tanlash qaroriga aylanadi: `order_id` ni kalit qilsang, bitta buyurtmaning `CREATED`, `PAID`, `SHIPPED` hodisalari bir partition ga tushadi va tartib saqlanadi.

Kalitni juda keng tanlash ham xato. Agar kalit `tenant_id` bo'lsa va bitta yirik mijoz butun trafikning 40 foizini bersa, o'sha partition "issiq" bo'lib qoladi: bitta iste'molchi orqada qoladi, qolganlari bo'sh turadi. Bunday hollarda kalitni `tenant_id + ':' + order_id` ko'rinishida kengaytirish yoki yirik mijoz uchun alohida topic ajratish kerak bo'ladi.

Kalit `null` bo'lsa, Kafka 2.4 dan keyingi standart partitioner sticky usulda ishlaydi: batch to'lguncha bitta partition ga yozadi, keyin boshqasiga o'tadi. Bu throughput uchun yaxshi, lekin tartib kafolati umuman yo'q. Audit log yoki metrika uchun bu to'g'ri qaror, to'lov holati uchun emas.

```java
// Buyurtma hodisasi: kalit sifatida order_id, shunda tartib saqlanadi.
// Partition ichidagi tartib kafolati faqat shu kalit tanlovi bilan ishlaydi.
public void publishOrderEvent(OrderEvent event) {
    ProducerRecord<String, OrderEvent> record = new ProducerRecord<>(
            "order.events",              // topic
            event.orderId(),             // kalit: bir buyurtma -> bir partition
            event);
    // Trace id ni header ga qo'shamiz, payload ni buzmaymiz.
    record.headers().add("traceId", tracer.currentTraceId().getBytes(UTF_8));
    kafkaTemplate.send(record)
            .whenComplete((meta, ex) -> {
                if (ex != null) {
                    // Bu yerda faqat log yetarli emas: outbox qatorini qayta urinishga qoldiramiz.
                    log.error("order.events yozilmadi orderId={}", event.orderId(), ex);
                } else {
                    log.debug("yozildi partition={} offset={}",
                            meta.partition(), meta.offset());
                }
            });
}
```

### 29.4 Producer sozlamalari: acks, enable.idempotence, linger.ms, batch.size

`acks` yozuvning qachon "muvaffaqiyatli" deb hisoblanishini belgilaydi. `acks=1` leader diskka yozishini kutadi, lekin leader o'sha zahoti qulasa xabar yo'qoladi. `acks=all` barcha in-sync replika tasdiqlashini kutadi va `min.insync.replicas=2` bilan birgalikda replikatsiya faktori 3 da bitta broker yo'qolishiga chidaydi. To'lov va buyurtma hodisalari uchun yagona to'g'ri tanlov `acks=all`. Narxi: taxminan 2-5 ms qo'shimcha latency bir xil data center ichida.

`enable.idempotence=true` producer ga sequence number beradi, shunda tarmoq retry sababli paydo bo'ladigan dublikat broker tomonida tashlanadi. Kafka 3.0 dan keyin bu standart qiymat, lekin u `acks=all`, `retries>0` va `max.in.flight.requests.per.connection<=5` ni talab qiladi. Agar kimdir `acks=1` qo'ysa, idempotentlik jim o'chadi yoki konfiguratsiya xatosi beradi. Shuning uchun bu uchta parametrni birga ko'rib chiqish kerak.

`linger.ms` va `batch.size` throughput va latency o'rtasidagi tanlovni boshqaradi. Standart `linger.ms=0` degani producer kutmaydi, natijada kichik batch lar ko'p bo'ladi. `linger.ms=5` qo'yish ko'p hollarda throughput ni 2-3 barobar oshiradi va faqat 5 ms latency qo'shadi. `batch.size=16384` standart, yuqori oqim uchun 65536 ga ko'tarish va `compression.type=lz4` yoqish amaliy kombinatsiya.

```properties
# Producer: ishonchlilik birinchi, keyin throughput.
acks=all
enable.idempotence=true
max.in.flight.requests.per.connection=5
retries=2147483647
# Umumiy muddat: shu vaqt ichida yetib bormasa xato qaytadi (standart 120000).
delivery.timeout.ms=120000
request.timeout.ms=30000
# Batching: 5 ms kutish throughput ni sezilarli oshiradi.
linger.ms=5
batch.size=65536
compression.type=lz4
# Buferda joy bo'lmasa send() bloklanadi, bu backpressure.
buffer.memory=67108864
max.block.ms=10000
```

`buffer.memory` to'lib qolganda `send()` chaqiruvi `max.block.ms` gacha bloklanadi. Bu Kafka ning backpressure mexanizmi va u HTTP so'rov ishlovchisi thread ini ushlab turadi. Shuning uchun `max.block.ms` ni 60 sekundda qoldirish xavfli: Kafka sekinlashsa, web thread pool to'lib qoladi va butun servis javob bermaydi. 5-10 sekund amaliy chegara.

### 29.5 Consumer sozlamalari: max.poll.records, max.poll.interval.ms va rebalance sababi

Kafka iste'molchisi `poll()` chaqiruvi orqali ishlaydi va bitta chaqiruvda `max.poll.records` (standart 500) tagacha yozuv oladi. Keyin ularning hammasini ishlab, yana `poll()` ga qaytishi kerak. Agar ikki `poll()` orasidagi vaqt `max.poll.interval.ms` (standart 300000, ya'ni 5 daqiqa) dan oshsa, group coordinator bu a'zoni o'lik deb hisoblaydi va rebalance boshlanadi.

Bu eng ko'p uchraydigan production nosozligining ildizi. Hisoblab ko'r: 500 yozuv, har biri uchun PostgreSQL ga ikki so'rov va tashqi API chaqiruvi, har biri taxminan 700 ms. Bu 350 sekund, ya'ni 5 daqiqadan oshadi. Natija: rebalance, offset commit rad etiladi, o'sha 500 xabar boshqa instansiyada qaytadan ishlanadi, u ham ulgurmaydi va tsikl aylanadi. Bu "rebalance storm" deb ataladi va servis cheksiz bir xil xabarni ishlab turadi.

Yechim ikki tomonli. Birinchisi: `max.poll.records` ni real ishlov vaqtiga moslash. Agar bitta xabar 200 ms olsa va xavfsizlik zaxirasi 3 barobar bo'lsa, `max.poll.records=100` va `max.poll.interval.ms=120000` mos keladi. Ikkinchisi: og'ir ishni listener ichida bajarmaslik, uni alohida bajarishga topshirish, lekin unda offset commit mantig'i murakkablashadi.

`session.timeout.ms` (Kafka 3.0 dan keyin standart 45000) va `heartbeat.interval.ms` (3000) boshqa narsani kuzatadi: heartbeat thread tirikligini. Ishlov uzoq cho'zilsa heartbeat davom etadi, lekin `max.poll.interval.ms` buziladi. Shuning uchun bu ikkita timeout ni aralashtirmaslik kerak.

Rebalance narxini kamaytirish uchun `CooperativeStickyAssignor` ishlatiladi: u barcha partition ni tortib olmaydi, faqat ko'chadiganlarini qaytaradi, shunda to'xtash 10 sekunddan 1 sekundga tushadi. Kafka 4.0 da KIP-848 asosidagi yangi group protokoli (`group.protocol=consumer`) rebalance ni broker tomoniga ko'chiradi va "stop the world" pauzasini yo'q qiladi.

```properties
# Consumer: ishlov vaqtini hisoblab batch kattaligini tanlaymiz.
group.id=payment-settlement
enable.auto.commit=false
auto.offset.reset=earliest
# 100 yozuv x ~200 ms = ~20 s, 120 s chegarada 6 barobar zaxira bor.
max.poll.records=100
max.poll.interval.ms=120000
session.timeout.ms=45000
heartbeat.interval.ms=3000
fetch.min.bytes=1
fetch.max.wait.ms=500
partition.assignment.strategy=org.apache.kafka.clients.consumer.CooperativeStickyAssignor
# Faqat commit qilingan tranzaksiya xabarlarini o'qish.
isolation.level=read_committed
```

### 29.6 Offset commit strategiyasi va kamida bir marta yetkazish oqibati

`enable.auto.commit=true` har `auto.commit.interval.ms` (5000) da oxirgi `poll()` qaytargan offset ni commit qiladi, ishlov tugaganiga qaramay. Ya'ni xabarni oldin commit qilib, keyin ishlov paytida xato bersang, xabar butunlay yo'qoladi. Bu "ko'pi bilan bir marta" semantikasi va to'lov uchun yaramaydi. Shuning uchun production da `enable.auto.commit=false`.

Qo'lda commit da tartib aniq: avval ishlov, keyin commit. Bu "kamida bir marta" yetkazishni beradi. Oqibati muhim: ishlov tugagandan keyin, commit dan oldin instansiya qulasa, o'sha xabar qaytadan keladi. Bu nosozlik emas, bu Kafka ning normal rejimi. Arxitektor vazifasi dublikatni oldini olish emas, dublikatga chidamli ishlov qurish.

Spring Kafka da `AckMode` bu qarorni shakllantiradi. `BATCH` (standart) butun poll natijasi ishlangach commit qiladi, `RECORD` har yozuvdan keyin commit qiladi, `MANUAL_IMMEDIATE` esa kodga `Acknowledgment.acknowledge()` ni beradi. `RECORD` xavfsizroq, lekin har commit broker ga so'rov, 1000 yozuv uchun 1000 so'rov. Amaliy o'rta yo'l: `BATCH` plus idempotent ishlov.

### 29.7 Idempotent iste'molchi qurish: PostgreSQL da ishlov berilgan xabar jadvali

Idempotentlikning eng ishonchli shakli: ishlov natijasini va "bu xabar ishlangan" belgisini bitta PostgreSQL tranzaksiyasida yozish. Shunda ikkinchi marta kelgan xabar unique constraint ga urilib, ishlovsiz tashlanadi. Kalit sifatida biznes identifikatorni (`payment_id`) ishlatish topic va partition dan ustun, chunki partition ko'paysa yoki topic almashsa ham identifikator o'zgarmaydi.

```sql
-- Ishlov berilgan xabar jadvali: dublikatni biznes kaliti bo'yicha to'sadi.
CREATE TABLE processed_message (
    consumer_group text        NOT NULL,
    message_id     text        NOT NULL,   -- biznes kaliti, masalan payment_id
    topic          text        NOT NULL,
    partition      int         NOT NULL,
    record_offset  bigint      NOT NULL,
    processed_at   timestamptz NOT NULL DEFAULT now(),
    PRIMARY KEY (consumer_group, message_id)
);

-- Jadval cheksiz o'smasligi uchun oyiga bir marta tozalash.
-- 30 kun dublikat oynasi ko'p tizim uchun yetarli.
CREATE INDEX idx_processed_message_at ON processed_message (processed_at);

DELETE FROM processed_message
WHERE processed_at < now() - interval '30 days';
```

```java
// Idempotent ishlov: belgini va natijani bitta tranzaksiyada yozamiz.
@Transactional
public void handle(PaymentConfirmed msg, String topic, int partition, long offset) {
    int inserted = jdbcTemplate.update("""
            INSERT INTO processed_message
                (consumer_group, message_id, topic, partition, record_offset)
            VALUES (?, ?, ?, ?, ?)
            ON CONFLICT (consumer_group, message_id) DO NOTHING
            """, "payment-settlement", msg.paymentId(), topic, partition, offset);

    if (inserted == 0) {
        // Dublikat: hech narsa qilmaymiz, lekin metrikani oshiramiz.
        duplicateCounter.increment();
        return;
    }
    // Asosiy biznes ishi shu tranzaksiya ichida, demak atomar.
    ledgerService.applyPayment(msg);
}
```

Bu yondashuvning cheklovi: ishlov PostgreSQL dan tashqariga chiqsa (tashqi API ga to'lov yuborish) atomarlik buziladi. Unda tashqi chaqiruvga idempotency key berish kerak, ya'ni idempotentlikni chegaradan tashqariga uzatish.

### 29.8 Consumer lag ni o'lchash va ogohlantirish chegarasi qo'yish

Lag bu partition ning oxirgi offset i va group commit qilgan offset i o'rtasidagi farq. U faqat sondan iborat emas: 50000 lag bir topic da 2 sekund, boshqasida 2 soat bo'lishi mumkin. Shuning uchun ogohlantirishni vaqtga o'tkazish kerak: `lag / xabarlar_sekundda`. Bu "qancha orqada" degan savolga biznes tili bilan javob beradi.

```bash
# Group holatini va har partition lag ini ko'rish.
kafka-consumer-groups.sh --bootstrap-server kafka-1:9092 \
  --describe --group payment-settlement

# Chiqishda: TOPIC PARTITION CURRENT-OFFSET LOG-END-OFFSET LAG CONSUMER-ID
# Faqat eng katta lag ni ajratib olish (monitoring skript uchun).
kafka-consumer-groups.sh --bootstrap-server kafka-1:9092 \
  --describe --group payment-settlement 2>/dev/null \
  | awk 'NR>1 && $6 ~ /^[0-9]+$/ {if ($6>m) m=$6} END {print m+0}'

# Rebalance tez-tez bo'layotganini tekshirish: group holati Stable bo'lishi kerak.
kafka-consumer-groups.sh --bootstrap-server kafka-1:9092 \
  --describe --group payment-settlement --state
```

Spring Boot ichida Micrometer Kafka client metrikalarini chiqaradi, eng muhimi `kafka.consumer.fetch.manager.records.lag.max`. Ogohlantirish chegarasi uchun amaliy qoida: ikki pog'ona. Birinchi pog'ona lag 5 daqiqadan oshsa warning, ikkinchisi 20 daqiqadan oshsa yoki lag 15 daqiqa davomida monoton o'ssa critical. Bitta cho'qqi (spike) ogohlantirish sababi emas, trend sabab.

Alohida kuzatish kerak bo'lgan ikki narsa bor. Birinchisi: lag nolga teng, lekin iste'molchi yo'q, ya'ni group bo'sh. Ikkinchisi: bitta partition lag i qolganlaridan 10 barobar katta, bu kalit taqsimoti nosozligi. Ikkalasi ham oddiy "umumiy lag" grafigida ko'rinmaydi.

### 29.9 Xato xabar bilan nima qilish: qayta urinish topic va dead letter topic

Xatolarni ikki sinfga ajratish kerak. O'tkinchi xato (PostgreSQL connection timeout, tashqi servisning 503 javobi) qayta urinishga arziydi. Doimiy xato (JSON deserializatsiya buzilgan, majburiy maydon yo'q, biznes qoidasi rad etdi) qayta urinishda hech qachon o'zgarmaydi. Doimiy xatoni asosiy topic da cheksiz urinish "poison pill" holatini yaratadi: bitta buzilgan xabar butun partition ni to'xtatib qo'yadi.

Listener ichida blokirovkali qayta urinish qilish xavfli, chunki u `max.poll.interval.ms` ni yeydi. Shuning uchun uzoq kechikishli qayta urinishlar alohida topic larga chiqariladi: `order.events.retry.5s`, `order.events.retry.1m`, `order.events.retry.10m`, va oxirida `order.events.DLT`. Spring Kafka ning `@RetryableTopic` annotatsiyasi shu topic larni va ularning listener larini avtomatik yaratadi.

Dead letter topic ning eng katta muammosi texnik emas, tashkiliy: unga hech kim qaramaydi. DLT ni amalda ishlatish uchun uchta narsa kerak. Birinchisi: DLT ga tushgan har xabar uchun alert, chunki DLT da bitta xabar ham anomaliya. Ikkinchisi: original xato, stack trace va topic nomi header larda saqlanishi (Spring ning `DeadLetterPublishingRecoverer` buni qiladi). Uchinchisi: DLT dan asosiy topic ga qaytarish uchun ishlaydigan operator vositasi, qo'lda SQL emas.

| Tuzoq | Nima sodir bo'ladi | Yechim |
|---|---|---|
| `enable.auto.commit=true` qoldirilgan | Ishlov xato bersa ham offset commit bo'ladi, xabar yo'qoladi | `false` qo'yish, ishlovdan keyin commit |
| `max.poll.records=500` va og'ir ishlov | `max.poll.interval.ms` buziladi, rebalance storm | Batch ni 50-100 ga tushirish, interval ni hisoblash |
| Doimiy xatoda cheksiz retry | Bitta buzilgan xabar partition ni to'xtatadi | `addNotRetryableExceptions` va DLT |
| Partition sonini production da oshirish | Kalit boshqa partition ga tushadi, tartib buziladi | Yangi topic va ikki tomonlama o'qish |
| DB commit, keyin Kafka send | DB yozildi, xabar yo'qoldi, holat nomuvofiq | Outbox jadvali va alohida publisher |
| `null` kalit bilan tartibga tayanish | Sticky partitioner xabarni turli partition ga tashlaydi | Biznes kalitini majburiy qilish |
| DLT ga alert yo'q | Xabarlar bir necha hafta sezilmay yo'qoladi | DLT dagi har xabarga ogohlantirish |
| `max.block.ms` standart 60 s | Kafka sekinlashsa web thread pool to'ladi | 5-10 s va circuit breaker |

### 29.10 Sxema o'zgarishi va orqaga moslik

Kafka da xabar bir necha kun yoki hafta yashaydi, shuning uchun bitta topic da bir vaqtda eski va yangi sxemadagi yozuvlar bo'ladi. Bu degani sxema o'zgarishi deploy tartibidan ko'ra muhimroq masala. Schema registry (Confluent yoki Apicurio) sxemani markazlashtiradi va moslik qoidasini majburlaydi, shunda nomos sxema serialize bosqichida rad etiladi, production da emas.

Eng ko'p ishlatiladigan rejim `BACKWARD`: yangi sxema eski ma'lumotni o'qiy oladi. Bu iste'molchini birinchi, producer ni keyin deploy qilishni talab qiladi. `FORWARD` teskarisi. Amalda ko'pchilik jamoaga `FULL` mos keladi: faqat standart qiymati bor maydon qo'shish va faqat ixtiyoriy maydonni olib tashlash mumkin. Majburiy maydonni standart qiymatsiz qo'shish har qanday rejimda buzuvchi o'zgarish.

Avro maydon nomini o'zgartirishni qo'llab-quvvatlamaydi, lekin `aliases` beradi. JSON Schema moslashuvchanroq, ammo hajmi kattaroq va tekshiruvi kuchsizroq. Amaliy qaror: ichki, yuqori oqimli topic lar uchun Avro (yozuv taxminan 30-50 foiz kichik), tashqi integratsiya uchun JSON Schema, chunki sherik jamoalar uchun o'qish oson.

Alohida eslatma: enum. Avro enum ga yangi qiymat qo'shish eski iste'molchi uchun buzuvchi o'zgarish, chunki u noma'lum qiymatni o'qiy olmaydi. Buyurtma holati kabi o'sib boradigan ro'yxatni `string` sifatida saqlash va validatsiyani kodga qo'yish ko'pincha to'g'riroq.

### 29.11 Tranzaksiya va xabar yuborish nomuvofiqligi: nega ikki fazali commit emas

Klassik muammo: `@Transactional` metod ichida PostgreSQL ga buyurtma yoziladi va Kafka ga hodisa yuboriladi. DB commit muvaffaqiyatli, Kafka esa tarmoq uzilishi sababli yozilmadi. Natijada buyurtma bazada bor, lekin ombor servisi uni ko'rmaydi. Teskari holat ham bor: Kafka yozildi, DB rollback bo'ldi, mavjud bo'lmagan buyurtma uchun hodisa tarqaldi.

Ikki fazali commit (XA) nazariy yechim, lekin Kafka XA tranzaksiya menejerini qo'llab-quvvatlamaydi. Kafka ning o'z tranzaksiyasi (`transactional.id` plus `isolation.level=read_committed`) faqat Kafka ichida atomar, ya'ni "read-process-write" oqimida. U PostgreSQL bilan bitta atomar blokga birlashmaydi. Spring Kafka da ilgari bo'lgan `ChainedKafkaTransactionManager` eng yaxshi holatda "eng yaxshi harakat" semantikasini beradi va Spring Kafka 3.x da deprecated.

Shuning uchun amaliy yechim outbox: hodisani bitta DB tranzaksiyasida jadvalga yozish, keyin alohida publisher uning Kafka ga yuborilishini ta'minlash. Bu "kamida bir marta" yuborishni beradi, dublikat esa iste'molchi tomonidagi idempotentlik bilan yopiladi. Pattern tafsiloti dizayn patternlar hujjatidagi outbox pattern bo'limida.

```sql
-- Outbox: hodisa biznes o'zgarishi bilan bitta tranzaksiyada yoziladi.
CREATE TABLE outbox_event (
    id             bigserial PRIMARY KEY,
    aggregate_type text        NOT NULL,   -- 'ORDER', 'PAYMENT'
    aggregate_id   text        NOT NULL,   -- Kafka kaliti bo'ladi
    event_type     text        NOT NULL,
    payload        jsonb       NOT NULL,
    created_at     timestamptz NOT NULL DEFAULT now(),
    published_at   timestamptz
);

CREATE INDEX idx_outbox_unpublished ON outbox_event (id)
    WHERE published_at IS NULL;

-- Publisher: bir nechta instansiya parallel ishlashi uchun qulf oladi.
SELECT id, aggregate_id, event_type, payload
FROM outbox_event
WHERE published_at IS NULL
ORDER BY id
LIMIT 200
FOR UPDATE SKIP LOCKED;
```

`FOR UPDATE SKIP LOCKED` bu yerda hal qiluvchi: ikkita publisher instansiyasi bir xil qatorni olmaydi va bir-birini kutmaydi. `ORDER BY id` bitta aggregate uchun tartibni saqlaydi, chunki `bigserial` monoton o'sadi.

### 29.12 Spring Kafka da asosiy sozlamalar va xato ishlovchisi

Spring Kafka da `ConcurrentKafkaListenerContainerFactory` ning `concurrency` xossasi shu instansiyadagi iste'molchi thread lari sonini belgilaydi. Uni partition sonidan oshirish befoyda. 12 partition va 3 instansiya bo'lsa, `concurrency=4` to'g'ri tanlov: har instansiya 4 partition oladi.

```yaml
spring:
  kafka:
    bootstrap-servers: kafka-1:9092,kafka-2:9092,kafka-3:9092
    producer:
      acks: all
      properties:
        enable.idempotence: true
        linger.ms: 5
        max.block.ms: 10000
    consumer:
      group-id: payment-settlement
      enable-auto-commit: false
      auto-offset-reset: earliest
      max-poll-records: 100
      isolation-level: read_committed
      properties:
        max.poll.interval.ms: 120000
        spring.json.trusted.packages: "com.shop.payment.events"
    listener:
      ack-mode: batch
      # 12 partition / 3 instansiya = har biriga 4 thread.
      concurrency: 4
      observation-enabled: true
```

Xato ishlovchisi bo'lmasa, Spring Kafka standart `DefaultErrorHandler` bilan 10 marta urinib, keyin yozuvni log ga chiqarib tashlaydi. Bu production uchun yetarli emas: nima tashlanganini keyin topib bo'lmaydi. To'g'ri sozlash: deserializatsiya xatosini alohida ushlash, doimiy xatolarni retry qilmaslik va qolganini DLT ga yuborish.

```java
@Bean
DefaultErrorHandler kafkaErrorHandler(KafkaTemplate<Object, Object> template) {
    // DLT nomi: "<topic>-dlt", original partition ga yozmaymiz (-1).
    var recoverer = new DeadLetterPublishingRecoverer(template,
            (record, ex) -> new TopicPartition(record.topic() + "-dlt", -1));

    // 1 s dan boshlab 2 barobar o'sadi, maksimum 10 s, 4 marta urinish.
    var backOff = new ExponentialBackOffWithMaxRetries(4);
    backOff.setInitialInterval(1000L);
    backOff.setMultiplier(2.0);
    backOff.setMaxInterval(10_000L);

    var handler = new DefaultErrorHandler(recoverer, backOff);
    // Bu xatolar hech qachon o'zgarmaydi: darhol DLT ga.
    handler.addNotRetryableExceptions(
            IllegalArgumentException.class,
            JsonProcessingException.class,
            PaymentRejectedException.class);
    handler.setRetryListeners((record, ex, attempt) ->
            log.warn("retry {} topic={} offset={}", attempt, record.topic(), record.offset()));
    return handler;
}
```

Deserializatsiya xatosi alohida holat: u listener ga yetib bormaydi, shuning uchun `ErrorHandlingDeserializer` ni o'rab ishlatish kerak. Aks holda buzilgan xabar cheksiz qayta o'qiladi va partition to'xtaydi. Testlash tomonidan nimani tekshirish kerakligi testlash qo'llanmasidagi Testcontainers bo'limida ko'rsatilgan.

### 29.13 Qaror jadvali: oddiy yondashuv va arxitektor yondashuvi

| Savol | Oddiy yondashuv | Arxitektor yondashuvi |
|---|---|---|
| Partition soni | 1 yoki 3, standart qoldiriladi | Kelgusi instansiya sonidan 2-3 barobar, 12 yoki 24 |
| Kalit | `null`, Kafka o'zi taqsimlasin | Biznes kaliti (`order_id`), issiq partition tekshirilgan |
| Offset commit | `enable.auto.commit=true` | Qo'lda commit, ishlovdan keyin |
| Dublikat | "Kafka exactly-once beradi" deb ishonish | `processed_message` jadvali va unique constraint |
| Batch kattaligi | Standart 500 | Ishlov vaqtidan hisoblangan 50-100 |
| DB va Kafka | Bitta `@Transactional` metodda ikkisi ham | Outbox jadvali, `SKIP LOCKED` publisher |
| Xato xabar | `try/catch` va log, keyin davom | Retry topic lar, DLT va DLT ga alert |
| Monitoring | Broker CPU va disk | Lag ni vaqtga aylantirish, rebalance soni |
| Sxema | POJO o'zgaradi, deploy qilinadi | Registry, `FULL` moslik, maydon standart qiymati bilan |
| Rebalance | Sezilmaydi, "shunchaki sekinlashdi" | `CooperativeStickyAssignor`, rebalance metrikasi |

### 29.14 Amalda qo'llash

- [ ] Har bir topic uchun partition sonini va kalit tanlovini yozib chiq, kalit bo'yicha xabar taqsimotini `kafka-consumer-groups.sh` lag chiqishi orqali tekshir va issiq partition bor-yo'qligini aniqla.
- [ ] Barcha producer da `acks=all`, `enable.idempotence=true` va `max.block.ms` 10 sekunddan oshmasligini tasdiqla, konfiguratsiyani kodga qattiq yozib qo'y.
- [ ] Har bir listener uchun bitta xabar ishlov vaqtini o'lchab, `max.poll.records` ni shunga qarab qayta hisobla va `max.poll.interval.ms` da kamida 3 barobar zaxira qoldir.
- [ ] `enable.auto.commit=true` qolgan barcha consumer ni top va ularni qo'lda commit ga o'tkaz.
- [ ] `processed_message` jadvalini joriy qilib, hech bo'lmasa to'lov va buyurtma listener larini idempotent qil, dublikat sonini metrika qilib chiqar.
- [ ] Retry topic va DLT zanjirini sozlab, `addNotRetryableExceptions` ro'yxatini to'ldir va DLT ga tushgan har xabar uchun alert yoq.
- [ ] Lag ni sondan vaqtga aylantiradigan dashboard panelini qur, 5 daqiqa warning va 20 daqiqa critical chegarasini qo'y, rebalance sonini ham shu panelga qo'sh.
- [ ] DB va Kafka ni bitta tranzaksiyada yozayotgan joylarni topib, ularni outbox jadvali va `FOR UPDATE SKIP LOCKED` publisher ga ko'chir.

## 30. Kuzatuvchanlik amaliyoti: log, metrika, trace va ularning narxi (Observability in Practice)

Kuzatuvchanlik tizim ishlayotganini emas, nega ishlamayotganini aytib berishi kerak. Ko'p jamoada bu teskari: dashboard yashil, log to'la, lekin "to'lov nega 14:20 da sekinlashdi" degan savolga javob yo'q. Sabab oddiy: uchta manba o'ylamasdan yoqilgan, holbuki har birining alohida narxi va alohida savoli bor. Bu bobda shu uchlikning mexanikasi, raqamlari va arxitektor tanlovlari ko'rib chiqiladi.

### 30.1 Uchta manba: log, metrika, trace va har biri qaysi savolga javob beradi

Log bitta hodisaning batafsil yozuvi, metrika vaqt bo'yicha agregatlangan son, trace bitta so'rovning servislar bo'ylab yo'li. Ular bir-birini almashtirmaydi. Metrika "muammo bormi va qanchalik katta" degan savolga javob beradi, trace "qaysi bo'g'inda" deydi, log "aynan nima bo'ldi" deb yopadi. Arxitektor xatosi odatda bittasini qolganlarining o'rniga ishlatishga urinishdir: metrikaga foydalanuvchi id qo'yib log o'rnida ishlatish, yoki har bir so'rovga 20 qator log yozib metrika o'rnini bosishga urinish.

| Manba | Qaysi savolga javob beradi | Narx drayveri | Saqlash muddati (taxminan) |
|---|---|---|---|
| Metrika | Muammo bormi, qancha davom etdi, trend qanday | Vaqt qatorlari (series) soni | 13-15 oy, past rezolyutsiyada |
| Trace | Kechikish qaysi servis yoki qaysi SQL da yo'qoldi | Span soni va sampling darajasi | 7-15 kun |
| Log | Aynan qaysi qiymat bilan nima qilindi | Ingest GB va indekslangan hodisa soni | 7-30 kun, arxiv 1 yil |

Metrika hamma so'rovni qamraydi, lekin detalsiz. Trace detalli, lekin faqat namuna. Log eng qimmat, demak eng tanlangan. Uchlikni bog'lovchi yagona narsa trace id, va u uchala manbada bir xil nomda bo'lsin.

### 30.2 Tuzilgan (strukturali) log: JSON format, maydon nomlari, trace id bog'lash

Matn ichiga qiymat yopishtirilgan log qidirib bo'lmaydigan log. `log.info("Payment " + id + " failed with " + code)` yozilsa, log tizimi buni 10 ming xil xabar deb ko'radi va guruhlay olmaydi. Xabar matni doimiy bo'lishi, o'zgaruvchilar alohida maydon bo'lishi kerak. SLF4J 2.x fluent API aynan shuni beradi.

```java
// To'lov servisi: xabar matni barqaror, o'zgaruvchilar maydon sifatida chiqadi
@Service
public class PaymentService {
    private static final Logger log = LoggerFactory.getLogger(PaymentService.class);

    public CaptureResult capture(PaymentCommand cmd) {
        long start = System.nanoTime();
        try {
            CaptureResult result = gateway.capture(cmd);
            log.atInfo()
               .setMessage("payment captured")          // matn hech qachon o'zgarmaydi
               .addKeyValue("orderId", cmd.orderId())
               .addKeyValue("amountMinor", cmd.amountMinor())
               .addKeyValue("gateway", result.gatewayName())
               .addKeyValue("durationMs", (System.nanoTime() - start) / 1_000_000)
               .log();
            return result;
        } catch (GatewayTimeoutException e) {
            // stack trace faqat eng yuqori qatlamda bir marta yoziladi
            log.atWarn().setMessage("payment capture timeout")
               .addKeyValue("orderId", cmd.orderId()).log();
            throw e;
        }
    }
}
```

Maydon nomlari bo'yicha kelishuv kerak, aks holda har jamoa `order_id`, `orderId`, `oid` yozadi va qidirish imkonsiz bo'ladi. Bitta sxemani tanlang va uni code review darvozasi bilan majburlang. Spring Boot 3.4 dan boshlab strukturali log framework ichida bor, qo'shimcha encoder kutubxonasi shart emas.

```properties
# Konsolga ECS formatida JSON, fayl ham bir xil formatda
logging.structured.format.console=ecs
logging.structured.format.file=ecs
logging.structured.ecs.service.name=payment-service
logging.structured.ecs.service.environment=prod
# Agar oddiy matn formati qolsa, trace id patternga qo'lda qo'shiladi
logging.pattern.level=%5p [${spring.application.name:},%X{traceId:-},%X{spanId:-}]
# Lokalda o'qish uchun strukturali log o'chiriladi (dev profilda)
```

Trace id MDC ga Micrometer Tracing tomonidan avtomatik qo'yiladi. Agar siz `@Async` yoki o'z `ExecutorService` ingizdan foydalansangiz, MDC yangi thread ga ko'chmaydi va log trace siz qoladi. Yechim: Spring taqdim etadigan context propagation mexanizmi orqali executor ni o'rash, yoki `TaskDecorator` ishlatish. Buni bir marta infratuzilma darajasida qiling, har bir servisda emas.

### 30.3 Log darajalari siyosati va ishlab chiqarishda nimani yozmaslik kerak

Daraja siyosati yozilmagan loyihada hamma narsa INFO bo'lib qoladi. Amaliy mezon: ERROR faqat odam aralashuvi kerak bo'lgan holat, WARN tizim o'zi tiklandi lekin bilish kerak, INFO biznes holati o'zgarishi, DEBUG prodda o'chiq. Eng ko'p uchraydigan xato: kutilgan biznes rad etishni ("ombor qoldig'i yetmadi") ERROR deb yozish. Bu bir oy ichida hamma ERROR ni e'tiborsiz qoldiradi.

Prodda log ga tushmasligi kerak: parol va token, karta raqami va CVV, to'liq `Authorization` header, shaxsiy ma'lumot, butun request body, entity `toString()`. Hibernate entity ni log ga bersangiz, `toString()` lazy kolleksiyani tortib yuborishi mumkin va bitta log qatori 50 ta qo'shimcha SQL ga aylanadi. Maskirovkani appender darajasida qiling, chunki har bir yangi maydon yana risk.

`DEBUG` ni prodda yoqish kerak bo'lsa, butun servis uchun emas, bitta package uchun va vaqt bilan cheklangan qiling. Actuator `loggers` endpointi buni restart siz beradi, lekin faqat himoyalangan portda turishi kerak.

### 30.4 Log hajmi va narxi: bitta so'rovga nechta qator yozilyapti

Bu savolni hech kim so'ramaydi, keyin hisob keladi. Hisob oddiy: 2000 rps, bitta so'rovga 12 qator, qator 400 bayt bo'lsa, bu 24 000 qator/s, 9.6 MB/s, kuniga taxminan 830 GB. Ingest narxi GB bo'yicha olinadigan tizimda bu yillik byudjetni yolg'iz yeb qo'yadi. 12 qator ko'p emas deb tuyuladi, lekin ko'pi "method entered" yoki "mapping dto" kabi qiymatsiz qatorlar.

```bash
# Bitta so'rovga qancha qator yozilayotganini o'lchash: bitta trace id ni sanash
TRACE=$(curl -s -D- -o /dev/null http://localhost:8080/api/orders/42 \
  | grep -i '^traceresponse' | cut -d- -f2)
grep -c "\"trace.id\":\"$TRACE\"" /var/log/app/app.json

# Qaysi xabar matnlari hajmni yeyayotganini topish (eng qimmat 10 ta)
jq -r '.message' /var/log/app/app.json | sort | uniq -c | sort -rn | head -10

# Kunlik hajm prognozi: 1 daqiqalik faylni 1440 ga ko'paytirish
ls -l --block-size=M /var/log/app/app.json
```

Arxitektor qarori: qatorlar sonini kamaytirish eng arzon optimizatsiya. Bitta so'rovga bitta yakuniy access log qatori va biznes holat o'zgarishi uchun 1-2 qator kifoya. Qolgan diagnostikani span attributlariga ko'chiring: span vaqt va ierarxiyani o'zi beradi. Ingest va indeks narxi ajratilgan tizimda esa hajmli, lekin kam qidiriladigan oqimni arzon arxivga yuborish mumkin.

### 30.5 Micrometer bilan metrika: counter, gauge, timer, distribution summary

Micrometer to'rt asosiy turni beradi va har biri o'z ishi uchun. Counter faqat o'sadi va "necha marta" savoliga javob beradi. Gauge joriy qiymatni o'qiydi va faqat shu daqiqadagi holatni biladi, tarixni emas. Timer vaqt taqsimotini yig'adi. DistributionSummary vaqt bo'lmagan kattalikni (buyurtma summasi, batch o'lchami) taqsimot sifatida yig'adi.

```java
@Component
public class OrderMetrics {
    private final Counter rejected;
    private final Timer checkout;
    private final DistributionSummary basketSize;

    public OrderMetrics(MeterRegistry registry, OrderQueue queue) {
        this.rejected = Counter.builder("orders.rejected")
                .description("rad etilgan buyurtmalar")
                .tag("reason", "out_of_stock")   // tag qiymati chekli ro'yxatdan
                .register(registry);
        this.checkout = Timer.builder("orders.checkout")
                .publishPercentileHistogram()    // server tomonda quantile hisoblash uchun
                .register(registry);
        this.basketSize = DistributionSummary.builder("orders.basket.items")
                .register(registry);
        // Gauge o'lchanadigan obyektga weak reference oladi, shuning uchun
        // obyekt tirik qolishiga ishonch kerak, aks holda qiymat NaN bo'ladi
        Gauge.builder("orders.queue.depth", queue, OrderQueue::size).register(registry);
    }

    public void recordCheckout(Duration d, int items) {
        checkout.record(d);
        basketSize.record(items);
    }
}
```

Ikki xato tez-tez uchraydi. Birinchisi: `registry.counter(...)` ni har so'rovda chaqirish, bu map lookup va tag massivini qayta yaratish degani; meter ni bir marta oling. Ikkinchisi: percentile ni client tomonda hisoblash. Bitta instansda hisoblangan p99 ni boshqa instans p99 bilan qo'shib bo'lmaydi, o'rtachasi esa ma'nosiz son. Agregatlanadigan p99 uchun histogram bucket lari chiqarilishi shart.

### 30.6 Kardinallik portlashi: metrika tegiga foydalanuvchi id qo'yish xatosi

Metrika narxi va xotirasi tag qiymatlarining kombinatsiyalari soniga, ya'ni vaqt qatorlari soniga bog'liq. `http.server.requests` da uri (50 variant), method (5), status (8), outcome (5) bo'lsa, taxminan 10 000 qator. Unga `userId` qo'shsangiz va 100 ming aktiv foydalanuvchi bo'lsa, qator soni millionlarga chiqadi. Prometheus da bitta aktiv qator taxminan 1-3 KB RAM yeydi, demak 5 million qator taxminan 10 GB. Scrape sekinlashadi, keyin OOM keladi. Histogram yoqilgan Timer esa bitta tag kombinatsiyasiga o'nlab bucket qatori qo'shadi, shuning uchun portlash tezligi yana bir necha barobar oshadi.

```java
// XATO: path variable va foydalanuvchi id teg qiymatiga tushadi
// registry.timer("orders.fetch", "path", "/orders/" + id, "user", userId)

// TO'G'RI: shablonli URI, chekli natija, id esa log yoki span attributiga
@Bean
MeterFilter limitTagValues() {
    return MeterFilter.maximumAllowableTags(
            "orders.fetch", "customerSegment", 20, MeterFilter.deny());
}

@Bean
MeterFilter dropNoisyMeters() {
    // tanib bo'lmaydigan URI uchun 404 oqimi alohida qator yaratmasin
    return MeterFilter.deny(id ->
            "http.server.requests".equals(id.getName())
            && "NOT_FOUND".equals(id.getTag("outcome")));
}
```

Qoida: tag qiymati oldindan ma'lum, chekli va 50 dan oshmaydigan to'plam bo'lsin. Id, email, URL, xato matni, SQL matni tegga tushmaydi, ularning joyi span attributi va log maydoni. Kardinallik yangi relizda qaytib keladi, shuning uchun qator sonining o'zini metrika qilib alert qo'ying.

### 30.7 Qaysi metrikalar majburiy: so'rov soni, xato ulushi, kechikish taqsimoti, resurs

Har bir servis uchun to'rtta oila shart. Birinchi: so'rov tezligi (rps), ikkinchi: xato ulushi (5xx va biznes xatolar alohida), uchinchi: kechikish taqsimoti (p50, p95, p99, albatta histogram orqali), to'rtinchi: to'yinganlik (connection pool band ulushi, thread pool navbati, heap, GC pauzasi, disk). Qolganlari foydali, lekin bu to'rttasi bo'lmasa incident vaqtida ko'r bo'lib qolasiz.

Java va Spring da alohida e'tibor beriladigan nuqtalar: `hikaricp.connections.pending` va `hikaricp.connections.usage`, chunki kechikishning yarmi shu yerdan chiqadi; `jvm.gc.pause`; `executor.queued`; Kafka consumer lag; va tashqi chaqiruvlar uchun `http.client.requests`. O'rtacha qiymatga qaramang: 2000 rps da p99 degani sekundda 20 ta foydalanuvchi, ya'ni kuniga yuz minglab yomon tajriba.

| Mavzu | Oddiy yondashuv | Arxitektor yondashuvi |
|---|---|---|
| Log formati | Matn ichiga qiymat yopishtirilgan `info` | Barqaror xabar, alohida maydonlar, kelishilgan sxema |
| Log hajmi | "Kerak bo'lsa yozamiz", hajm o'lchanmaydi | Bitta so'rovga qator soni byudjeti va o'lchovi bor |
| Percentile | Instans ichida p99 hisoblanadi | Histogram bucket, agregatsiya backend da |
| Metrika teglari | Nima qo'l kelsa teg qilinadi | Chekli lug'at, `MeterFilter` bilan cheklov |
| Trace | Hammasi yoki hech nima | Head sampling past, xatoli trace tail bilan to'liq |
| Alert | CPU 80 foizdan oshdi | Xato byudjeti yonish tezligi oshdi |
| Dashboard | 40 ta panel, hammasi bir xil muhim | Birinchi ekranda to'rtta signal, qolgani drill-down |
| Incident tahlili | Log ni ko'z bilan o'qish | Trace id bo'ylab uchala manbani bir zumda bog'lash |
| Yangi servis | Kuzatuv keyin qo'shiladi | Kuzatuv shablonda, ishga tushirish shartida |

### 30.8 OpenTelemetry: trace, span, kontekst tarqalishi va namuna olish (sampling)

Trace bitta so'rovning butun yo'li, span esa shu yo'ldagi bitta ish bo'lagi: HTTP handler, SQL so'rov, Kafka publish. Span ichida id, parent id, boshlanish vaqti, davomiylik va attributlar bor. Kontekst servislar orasida W3C `traceparent` header i, Kafka da message header orqali uzatiladi. Spring Boot 3.x da bu Micrometer Observation API va OTel bridge orqali ishlaydi: bitta `Observation` dan metrika ham, span ham chiqadi.

Eng ko'p yo'qotish nuqtalari: async chegaralari, message broker (header ko'chirilmaydi) va reverse proxy (header o'chirib tashlaydi). Trace servis chegarasida uzilsa, ikkita alohida trace ko'rinadi va kechikish bog'lanmaydi. Buni integratsiya testida tekshirib qo'ying: kirishga `traceparent` berilib, chiqishda bir xil trace id kutiladi.

```java
// Biznes operatsiyasini bitta Observation bilan o'rash:
// bundan ham span, ham `orders.checkout` metrikasi chiqadi
Observation.createNotStarted("orders.checkout", observationRegistry)
    .lowCardinalityKeyValue("channel", "mobile")      // metrikaga ham tushadi
    .highCardinalityKeyValue("orderId", orderId)      // faqat span attributi
    .observe(() -> checkoutService.run(orderId));
```

Kam kardinallikli key metrikaga ham, span ga ham tushadi, yuqori kardinallikli key faqat span ga. Shu ajratim kardinallik portlashining asosiy to'sig'i, va u kod yozilayotganda hal bo'ladi, keyin emas.

### 30.9 Namuna olish darajasi tanlash va xatoli so'rovlarni to'liq saqlash

Har bir so'rovni trace qilish qimmat: 2000 rps va so'rovga 15 span bo'lsa, bu 30 000 span/s. Shuning uchun head sampling qo'yiladi, masalan 5 foiz. Muammo shundaki, head sampling qarorni so'rov boshida qabul qiladi va o'sha paytda so'rov xato bilan tugashini bilmaydi. Natijada incident paytida aynan kerakli trace topilmaydi.

To'g'ri yechim ikki qatlamli. Birinchi qatlam: head sampling `parentbased_traceidratio` bilan, past darajada, lekin butun trace bo'ylab izchil (parent qarori bolalarga o'tadi, aks holda yarim trace chiqadi). Ikkinchi qatlam: Collector da tail sampling, u butun trace yig'ilgandan keyin qaror qiladi va xatoli hamda sekin trace larni to'liq saqlaydi.

```yaml
# OTel Collector: xato va sekin trace to'liq, qolgani 5 foiz
processors:
  tail_sampling:
    decision_wait: 10s          # trace yig'ilishini kutish
    num_traces: 100000
    policies:
      - name: xatolar
        type: status_code
        status_code: { status_codes: [ERROR] }
      - name: sekinlar
        type: latency
        latency: { threshold_ms: 1500 }
      - name: qolgani
        type: probabilistic
        probabilistic: { sampling_percentage: 5 }
```

Muhim nuans: tail sampling faqat o'ziga yetib kelgan trace dan tanlaydi. Agar ilovada 5 foiz head sampling bo'lsa, Collector qolgan 95 foizni ko'rmaydi. Shuning uchun tail sampling ishlatilsa, ilovada sampling 100 foiz qo'yiladi va filtr Collector ga ko'chadi. Bu ilovada taxminan bir necha foiz CPU va tarmoq qo'shadi, bu ongli to'lanadigan narx.

### 30.10 Ogohlantirish (alert) dizayni: belgiga emas, foydalanuvchi ta'siriga qarab

"CPU 80 foizdan oshdi" alert i emas, bu kuzatuv. U kechasi odamni uyg'otadi, lekin foydalanuvchi hech narsa sezmagan bo'lishi mumkin. Alert faqat foydalanuvchi ta'siri bor va odam aralashuvi kerak bo'lgan holatda chiqishi kerak. Shuning uchun alert SLO ga va xato byudjeti yonish tezligiga quriladi: "oxirgi 1 soatda xato byudjetining shunday ulushi yondi" degan shart ham tez, ham shovqinsiz ishlaydi.

```yaml
groups:
  - name: checkout-slo
    rules:
      # 99.9 foiz SLO: 1 soatda 14.4 barobar yonish tezligi tez buzilish belgisi
      - alert: CheckoutErrorBudgetFastBurn
        expr: |
          (sum(rate(http_server_requests_seconds_count{uri="/api/checkout",status=~"5.."}[1h]))
           / sum(rate(http_server_requests_seconds_count{uri="/api/checkout"}[1h]))) > 14.4 * 0.001
          and
          (sum(rate(http_server_requests_seconds_count{uri="/api/checkout",status=~"5.."}[5m]))
           / sum(rate(http_server_requests_seconds_count{uri="/api/checkout"}[5m]))) > 14.4 * 0.001
        for: 2m
        labels: { severity: page }
        annotations:
          summary: "Checkout xato byudjeti tez yonmoqda"
          runbook: "https://wiki/runbooks/checkout-5xx"
```

Ikki oynali shart (1 soat va 5 daqiqa) bitta sakrashdan kelgan yolg'on alert ni kesadi va muammo tuzatilganda alert ni tez yopadi. Har bir sahifalaydigan alert da runbook havolasi bo'lishi shart: nima qilish kerakligini aytmagan alert shunchaki xavotir. Resurs metrikalari dashboard va ticket darajasida qoladi, faqat disk to'lishi kabi qaytarib bo'lmaydigan holat istisno.

| Tuzoq | Nega og'riydi | Yechim |
|---|---|---|
| Metrika tegida id yoki URL | Qator soni millionga chiqib backend yiqiladi | Shablonli URI, `MeterFilter` bilan cheklov, id span ga |
| Client tomonda p99 | Instanslar bo'ylab agregatlanmaydi | `publishPercentileHistogram`, quantile backend da |
| Head sampling 5 foiz | Xatoli so'rovning trace i yo'q | Ilovada 100 foiz, Collector da tail sampling |
| MDC async da yo'qoladi | Log da trace id bo'sh, bog'lash uzilgan | Executor ni context propagation bilan o'rash |
| Entity ni log ga berish | Lazy yuklash, ortiqcha SQL, PII oqishi | Faqat kerakli maydonlar, maskirovka appender da |
| Kutilgan rad etish ERROR da | Alert shovqinga aylanadi va e'tibordan qoladi | Biznes rad etish INFO yoki WARN, metrikada alohida |
| CPU va heap bo'yicha alert | Kechasi uyg'otadi, ta'sir yo'q | SLO va burn rate alert, resurs faqat dashboard da |
| Histogram hamma Timer da | Bucket qatorlari ko'payib xotira yeydi | Faqat SLO li operatsiyalarda, chegaralar bilan |

### 30.11 Dashboard qanday bo'lishi kerak: birinchi ekranda nima turadi

Dashboard incident paytida 30 sekundda javob berishi kerak. Demak birinchi ekranda scroll qilmasdan faqat to'rtta narsa turadi: so'rov tezligi, xato ulushi, kechikish p95 va p99, to'yinganlik. Yonida reliz versiyasi va deploy belgilari bo'lsin, chunki buzilishlarning katta qismi deploy bilan ustma-ust tushadi. Qolgani pastda yoki drill-down dashboard da.

Amaliy talablar: har bir panelda o'q birligi va SLO chizig'i ko'rinsin, vaqt oynasi hamma panel uchun bitta bo'lsin, instans bo'yicha ajratish faqat kerakli panelda qolsin. 40 panelli dashboard hech kimga tegishli bo'lmaydi va eskiradi, shuning uchun har bir dashboard egasi bo'lishi kerak.

### 30.12 Spring Boot Actuator va Micrometer sozlash amaliyoti

Actuator ni ochish oson, xatolar ham oson. Birinchi qoida: management port ni ilova portidan ajratib tashqaridan yopish. Ikkinchi: `env`, `heapdump`, `threaddump`, `loggers` himoyalanmagan holda ochilmasin. Uchinchi: health detallari faqat autentifikatsiyadan o'tganlarga ko'rinsin, chunki u ichki infratuzilma xaritasini oshkor qiladi. To'rtinchi: liveness va readiness probe larni ajratish, aks holda baza vaqtincha yo'qolganda Kubernetes pod ni bejiz o'ldiradi.

```yaml
management:
  server.port: 9090                 # ilova porti bilan aralashmasin
  endpoints.web.exposure.include: health,info,prometheus,metrics
  endpoint.health:
    show-details: when-authorized
    probes.enabled: true            # liveness va readiness alohida
  metrics:
    tags: { application: payment-service, env: prod }
    distribution:
      percentiles-histogram:
        http.server.requests: true  # faqat kerakli metrikada
      slo:
        http.server.requests: 100ms,300ms,1s,3s
      maximum-expected-value:
        http.server.requests: 5s    # bucket sonini cheklaydi
  observations.key-values.region: eu-central-1
  tracing.sampling.probability: 1.0 # filtr Collector da tail sampling bilan
otel.exporter.otlp.endpoint: http://otel-collector:4317
```

`percentiles-histogram` ni global yoqmang: har bir histogram li Timer o'nlab bucket qatori yaratadi, `maximum-expected-value` qo'yilmasa diapazon keraksiz keng bo'ladi. Histogram faqat SLO bor operatsiyada yig'ilsin. Nihoyat, kuzatuv kodi o'zi ham taxminan bir necha foiz CPU va qo'shimcha allokatsiya yeydi, shuning uchun uni yuklama testida o'lchash kerak. Testlash qo'llanmasidagi performance test bo'limi shu o'lchov uchun asos beradi, dizayn patternlar hujjatidagi observability patternlari esa strukturaviy tomonni yopadi.

### 30.13 Amalda qo'llash

- [ ] Bitta tipik so'rovga nechta log qatori yozilayotganini sanang va uni 3 qatorgacha qisqartirish rejasini tuzing.
- [ ] Log maydon nomlari lug'atini yozib, strukturali formatni (ECS yoki o'z sxemangiz) hamma servisga bir xil qo'ying.
- [ ] Async chegarasida trace id MDC da saqlanishini integratsiya testi bilan tekshirib qo'ying.
- [ ] Prometheus da eng ko'p qator yaratadigan 10 ta metrikani chiqarib, id va URL li teglarni `MeterFilter` bilan kesib tashlang.
- [ ] Client tomonda hisoblanadigan percentile larni olib tashlab, SLO li operatsiyalarda histogram va `maximum-expected-value` qo'ying.
- [ ] Ilovada sampling ni 100 foizga olib chiqib, xato va 1.5 sekunddan sekin trace larni to'liq saqlaydigan tail sampling ni Collector da yoqing.
- [ ] Resurs bo'yicha sahifalaydigan alert larni o'chirib, ularning o'rniga burn rate alert va har biriga runbook havolasi qo'shing.
- [ ] Har bir servis dashboard ining birinchi ekranini to'rtta signalga qisqartirib, egasini belgilang.

## 31. Deployment haqiqati: konteyner, cgroup, JVM va probe (Deployment Reality)

Lokalda ishlagan servis production'da boshqacha yashaydi. U cgroup bilan chegaralangan, orkestrator tomonidan har qanday paytda o'ldirilishi mumkin, va uning sog'ligi haqida qaror HTTP probe orqali chiqariladi. Arxitektor uchun deployment YAML fayl to'ldirish emas, balki JVM, kernel va orkestrator o'rtasidagi shartnomani tushunishdir. Bu bobda to'lov servisi va buyurtma servisi misolida shu shartnomaning har bir bandi ochiladi.

### 31.1 Konteyner nima va nima emas

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

### 31.2 JVM konteyner limitlarini qanday ko'radi

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

### 31.3 Xotira limiti: heap, metaspace, thread stack va native xotira yig'indisi

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

Thread soni bu yerda yashirin xavf. Tomcat `server.tomcat.threads.max` sukut bo'yicha 200, har biri Hikari connection kutishi mumkin. Agar yana async executor, Kafka consumer va scheduler thread'lari qo'shilsa, 400 thread oson yig'iladi. Bu 400Mi faqat stack uchun. Virtual thread'lar bu muammoni kamaytiradi, chunki ularning stack'i heap'da yashaydi va o'sib boradi, lekin carrier thread soni yadro soniga bog'liq qoladi.

### 31.4 CPU limiti va throttling: nega latency kutilmaganda oshadi

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

### 31.5 Image qurish: qatlamlarni to'g'ri tartiblash, hajmni kamaytirish, bazaviy image tanlash

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

### 31.6 Liveness, readiness va startup probe farqi va noto'g'ri sozlashning oqibati

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

### 31.7 Ishga tushish va to'xtash: SIGTERM, graceful shutdown, terminationGracePeriodSeconds

Pod o'chirilganda kubelet konteynerga `SIGTERM` yuboradi va `terminationGracePeriodSeconds` kutadi, sukut bo'yicha 30 sekund. Muhlat tugasa `SIGKILL` keladi va uni ushlab qolish mumkin emas. Shu 30 sekund ichida ilova ishni toza tugatishi kerak.

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

### 31.8 Rolling update, maxSurge va maxUnavailable ta'siri

RollingUpdate strategiyasi ikki parametr bilan boshqariladi. `maxSurge` desired replica sonidan qancha ortiq pod yaratilishi mumkinligini belgilaydi. `maxUnavailable` qancha pod bir vaqtda yetishmasligi mumkinligini belgilaydi. Sukut qiymatlar 25 foiz va 25 foiz.

Arxitektor uchun bu sig'im masalasi. 4 replika ishlayotgan to'lov servisida `maxUnavailable: 25%` bitta podni olib tashlaydi, qolgan uchtasi 33 foiz ko'proq trafik ko'taradi. Agar har bir pod allaqachon 80 foiz yuklangan bo'lsa, deploy paytida servis qulab tushadi. Shuning uchun yuqori yuklamali servislarda `maxUnavailable: 0` va `maxSurge: 1` tanlanadi. Bu deploy'ni sekinlashtiradi, lekin sig'im kamaymaydi.

`maxUnavailable: 0` qo'ysa cluster'da qo'shimcha resurs bo'lishi shart. Aks holda yangi pod `Pending` holatida qotib qoladi va deploy to'xtaydi. Shuning uchun bu qarorni node sig'imi bilan birga ko'rib chiqish kerak.

Yana bir nozik joy: rolling update faqat probe'lar to'g'ri bo'lsa ishlaydi. Readiness probe `true` qaytarsa, lekin ilova hali JIT'ni qizdirmagan bo'lsa, yangi pod birinchi minutda sekin javob beradi. Bu "deploy paytida latency spike" deb nomlanadi. Yechim: readiness'dan oldin kichik warmup qilish, yoki `minReadySeconds` qo'yib podning trafikka kirishini kechiktirish.

Baza sxemasi migratsiyasi rolling update bilan to'qnashadi. Deploy paytida eski va yangi versiya bir vaqtda ishlaydi, demak sxema ikkalasiga ham mos bo'lishi shart. Ustun o'chirish uch deploy'ga bo'linadi: avval kod ustunni ishlatmay qo'yadi, keyin ustun nullable bo'ladi, oxirida o'chiriladi.

### 31.9 Resurs so'rovi (request) va limiti: qanday hisoblanadi

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

### 31.10 Konfiguratsiya va maxfiy ma'lumotlarni konteynerga berish

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

### 31.11 Gorizontal masshtablash: holatsizlik sharti va sessiya muammosi

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

### 31.12 Ishga tushish vaqti va avtomatik masshtablashning bog'liqligi

HPA yuklamaga javoban yangi pod yaratadi, lekin pod trafikka kirishi uchun startup tugashi kerak. Agar Spring ilovasi 60 sekundda ishga tushsa, HPA'ning reaksiyasi amalda bir daqiqa kechikadi. Trafik spike 30 sekund davom etsa, yangi pod spike tugaganda tayyor bo'ladi. Bu masshtablashni foydasiz qiladi.

Shu sababli startup vaqti arxitektura ko'rsatkichi. Uni qisqartirishning amaliy yo'llari bor. Birinchisi lazy initialization'dan voz kechish va kerakli bean'larni kamaytirish: `spring.main.lazy-initialization=true` startup'ni tezlashtiradi, lekin birinchi so'rov latency'sini oshiradi, shuning uchun u faqat dev uchun. Ikkinchisi auto configuration sonini kamaytirish, chunki har bir starter classpath skanerlash qo'shadi. Uchinchisi Class Data Sharing arxivi: Spring Boot 3.3 dan boshlab buning uchun qulay mexanizm bor va startup 20 dan 30 foizgacha tezlashadi. To'rtinchisi JDK 24 dan paydo bo'lgan AOT cache. Beshinchisi GraalVM native image, u startup'ni 100 millisekundga tushiradi, lekin reflection konfiguratsiyasi va build vaqti narxi bilan keladi.

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

Agar startup'ni tezlashtirish imkoni bo'lmasa, qaror boshqa tomondan keladi: `minReplicas` ni oshirib doimiy zahira sig'im ushlab turish. Bu pul turadi, lekin ishonchli. Target utilization'ni 60 foizga tushirish ham shu maqsadga xizmat qiladi, chunki podlar spike'ni o'zi ko'tarishga joy qoldiradi. Bu yerda ehtiyotkorlik patternlari kerak bo'lsa, dizayn patternlar hujjatidagi resilience bo'limiga qaralsin.

### 31.13 Amalda qo'llash

- [ ] Har bir servis uchun `kubectl exec` bilan `cpu.stat` o'qib `nr_throttled / nr_periods` nisbatini hisoblang, 0.05 dan oshganlarga CPU limitini oshiring.
- [ ] Barcha deployment'larda `-Xmx` ni `-XX:MaxRAMPercentage` ga o'zgartiring va NMT hisoboti bilan xotira taqsimotini tasdiqlang.
- [ ] Liveness probe'dan baza va tashqi servis tekshiruvlarini olib tashlab, ularni faqat readiness guruhiga qoldiring.
- [ ] Sekin ishga tushadigan servislarga `failureThreshold: 30` bilan startup probe qo'shing va startup vaqtini metrika sifatida yozib boring.
- [ ] `server.shutdown=graceful`, `preStop sleep 5` va `terminationGracePeriodSeconds` uchligini bitta koherent qiymat to'plami sifatida sozlang.
- [ ] Fat jar deploy'larini layered jar'ga o'tkazing va registry'ga yuklanadigan qatlam hajmini deploy oldidan va keyin o'lchang.
- [ ] Yuqori yuklamali servislarda `maxUnavailable: 0` va `maxSurge: 1` ga o'tib, cluster'da yetarli zahira sig'im borligini tekshiring.
- [ ] `@Scheduled` metodlar ro'yxatini chiqarib, har biri uchun lock yoki CronJob yechimini tanlang va replikani 2 ga ko'tarib tekshirib ko'ring.

## 32. Tarmoq, timeout va integratsiya haqiqati (Network, Timeouts and Integration)

Tarmoq orqali chaqiruv lokal metod chaqiruvi emas, lekin kodda ikkisi bir xil ko'rinadi. Arxitektorning asosiy vazifasi shu farqni kodda ko'rinadigan qilish: har bir tashqi chaqiruvda vaqt chegarasi, qayta urinish qoidasi va to'xtash sharti bo'lsin. Quyida mexanika va raqamlar bor: TCP nima qiladi, timeout qanday ishlaydi, pool qancha bo'lishi kerak, DNS va TLS qayerda tishlaydi. Resilience pattern katalogi (circuit breaker, bulkhead, outbox) dizayn patternlar hujjatida, bu yerda faqat sozlash va qaror.

### 32.1 Tarmoq ishonchsiz: ulanish uzilishi, paket yo'qolishi, yarim ochiq ulanish

TCP ishonchli yetkazishni kafolatlaydi, lekin faqat ulanish tirik bo'lsa. Ikki xil uzilish bor va ularning oqibati butunlay boshqa. Birinchisi toza uzilish: peer FIN yoki RST yuboradi, socket darhol xabar beradi, `read()` bir necha mikrosekundda xato qaytaradi. Ikkinchisi yarim ochiq (half-open) ulanish: peer o'lgan, lekin hech qanday paket yubormagan. Bu `kill -9` da, VM o'chib qolganda, NAT jadvalidan yozuv tushib ketganda yoki firewall paketni jim tashlab yuborganda sodir bo'ladi.

Yarim ochiq ulanish eng qimmat holat, chunki JVM uning o'lganini bilmaydi. Linux `tcp_retries2` default 15 ga teng, bu taxminan 924 sekund, ya'ni 15 daqiqa qayta yuborishdan keyin socket xato beradi. Shu 15 daqiqa davomida thread `read()` da osilib turadi. `SO_KEEPALIVE` yoqilgan bo'lsa ham default `tcp_keepalive_time` 7200 sekund, ya'ni birinchi probe 2 soatdan keyin ketadi. Xulosa: application darajasidagi read timeout yagona ishonchli himoya, OS sozlamalariga tayanib bo'lmaydi.

```bash
# Yarim ochiq ulanish belgisi: Send-Q o'smoqda, lekin ACK kelmayapti
ss -tin dst 10.20.0.15 | head -20

# Dead peer ni TCP qancha kutadi: 15 ta retry taxminan 924 sekund
cat /proc/sys/net/ipv4/tcp_retries2

# Keepalive birinchi probe gacha jimlik: default 7200 sekund
cat /proc/sys/net/ipv4/tcp_keepalive_time

# Blackhole ni imitatsiya qilish: RST emas, paketni jim tashlash
sudo iptables -A OUTPUT -d 10.20.0.15 -p tcp --dport 8443 -j DROP
```

### 32.2 Timeout turlari: ulanish, o'qish, yozish, umumiy so'rov, va ularning farqi

Kutilmagan hodisalarning yarmi "timeout qo'ydim" deb o'ylab, aslida boshqa timeout ni qo'yishdan kelib chiqadi. Beshta alohida chegara bor va ular bir-birini almashtirmaydi.

Connect timeout: TCP handshake uchun. Bu faqat SYN dan SYN-ACK gacha bo'lgan vaqt, odatda bir RTT. Data-center ichida 1 ms, region oralig'ida 30 ms. Shuning uchun connect timeout 1 dan 2 sekundgacha yetarli, 30 sekund bu xato.

Connection request timeout yoki pool acquire timeout: hovuzdan bo'sh ulanish kutish vaqti. Bu eng ko'p yashiriladigan latency. Reactor Netty da `pendingAcquireTimeout` default 45 sekund, Apache HttpClient 5 da `connectionRequestTimeout` default ham katta. Servis yuklanganda butun kechikish shu yerda to'planadi.

Socket yoki read timeout: ikki ketma-ket bayt oralig'idagi jimlik. Bu umumiy so'rov vaqti EMAS. Serverda sekin oqim bo'lsa, masalan har 4 sekundda bir bayt kelsa, 5 sekundlik read timeout hech qachon ishlamaydi va chaqiruv cheksiz davom etadi.

Response timeout: so'rov yuborilgandan birinchi javob baytigacha. Write timeout: kernel send buffer to'lib, yozish bloklanganda. Umumiy so'rov timeout: butun operatsiya uchun qattiq deadline, retry va redirect bilan birga. Faqat shu oxirgisi haqiqiy kafolat beradi.

```java
// Java HttpClient: umumiy deadline bor, bu eng muhim xususiyat
HttpClient client = HttpClient.newBuilder()
        .connectTimeout(Duration.ofSeconds(2))   // faqat TCP handshake
        .version(HttpClient.Version.HTTP_2)
        .build();

HttpRequest req = HttpRequest.newBuilder(URI.create(baseUrl + "/payments"))
        .timeout(Duration.ofMillis(1200))        // butun so'rov uchun qattiq chegara
        .header("Idempotency-Key", paymentId.toString())
        .POST(HttpRequest.BodyPublishers.ofString(body))
        .build();
```

```properties
# Spring Boot 3.4+ markazlashgan HTTP client sozlamasi
spring.http.client.factory=jdk
spring.http.client.connect-timeout=2s
spring.http.client.read-timeout=1200ms

# Tomcat tomoni: osilgan ulanishni ushlab turmaslik
server.tomcat.connection-timeout=5s
```

### 32.3 Timeout qiymatini qanday tanlash: yuqori qatlam quyi qatlamdan uzunroq bo'lsin

Timeout qiymati o'rtacha latency dan emas, taqsimot dumidan chiqadi. To'lov servisiga misol: p50 40 ms, p95 120 ms, p99 180 ms, p99.9 600 ms. Read timeout ni p99.9 ga taxminan 1.5 koeffitsiyent bilan olasiz, ya'ni 900 ms dan 1 sekundgacha. Buni 30 sekund qilib qo'yish degani: bitta sekin dependency butun thread pool ni bloklaydi va o'zingiz ham o'lasiz.

Qatlamlar tartibi qattiq qoida. Tashqi qatlam ichki qatlamdan uzunroq bo'lishi kerak, aks holda ichki chaqiruv tugamasdan tashqi tomon bekor qiladi va siz natijasi bor ishni tashlab yuborasiz. Ayni paytda tashqi qatlam ichki qatlamlar yig'indisidan sezilarli kattaroq bo'lmasligi kerak, aks holda deadline ma'nosini yo'qotadi. Amalda qadam sifatida 100 dan 300 ms gacha zahira qo'yiladi.

Ikkinchi qoida: statement timeout ni ilovada emas, bazada ham qo'ying. Ilova timeout da thread ni qo'yib yuboradi, lekin PostgreSQL so'rovni davom ettiradi va CPU ni yeydi. JDBC `socketTimeout` ulanishni buzadi, `statement_timeout` esa so'rovni haqiqatda to'xtatadi.

```sql
-- Har bir rolga o'z chegarasi: hisobot OLTP ni cho'ktirmaydi
ALTER ROLE app_rw  SET statement_timeout = '3s';
ALTER ROLE app_rw  SET lock_timeout = '1s';
ALTER ROLE app_rw  SET idle_in_transaction_session_timeout = '10s';
ALTER ROLE report_ro SET statement_timeout = '45s';

-- Tekshirish: joriy sessiyada nima o'rnatilgan
SELECT name, setting FROM pg_settings
WHERE name IN ('statement_timeout','lock_timeout',
               'idle_in_transaction_session_timeout');
```

### 32.4 Timeout byudjeti: zanjirdagi har bir chaqiruvga vaqt taqsimlash

Buyurtma yaratish API si uchun SLO 2000 ms bo'lsa, bu butun zanjir uchun byudjet. Byudjetni bo'lib chiqasiz: gateway 1900 ms, order service 1700 ms, uning ichida ombor qoldig'ini tekshirish 400 ms, to'lov 800 ms, baza yozuvlari 200 ms, qolgani zahira. Har bir qism o'z chegarasini biladi va umumiy summa SLO dan oshmaydi.

Statik qiymat yetarli emas, chunki birinchi chaqiruv 700 ms yesa, keyingi chaqiruvga 800 ms berish mantiqsiz. Shuning uchun deadline uzatiladi, timeout emas. Chaqiruvchi "menda yana 480 ms qoldi" deb aytadi, chaqirilgan tomon shu chegaradan oshmaydi va qolgan vaqt yetmasa ishni boshlamasdan rad etadi. Bu bitta tarmoq chaqiruvini va bitta DB ulanishini tejaydi.

```java
// Deadline ni so'rov kontekstida olib yuring, millisekundda header orqali uzating
public record Deadline(long epochMillis) {
    static Deadline in(Duration d) {
        return new Deadline(System.currentTimeMillis() + d.toMillis());
    }
    Duration remaining() {
        return Duration.ofMillis(Math.max(0, epochMillis - System.currentTimeMillis()));
    }
    // Zahira: tarmoq va serializatsiya uchun 50 ms qoldirmasak, javob kech qoladi
    Duration budgetFor(Duration ask) {
        long left = remaining().toMillis() - 50;
        if (left <= 0) throw new DeadlineExceededException("byudjet tugadi");
        return Duration.ofMillis(Math.min(ask.toMillis(), left));
    }
}
```

| oddiy yondashuv | arxitektor yondashuvi |
| --- | --- |
| Hamma joyda default timeout, ko'pincha 30 yoki 60 sekund | Har bir chaqiruvga p99.9 asosida hisoblangan qiymat, 1 sekund atrofida |
| Faqat connect va read timeout qo'yiladi | Pool acquire, connect, read, umumiy deadline, hammasi alohida |
| Har bir servis o'z timeout ini mustaqil tanlaydi | Zanjir uchun yagona byudjet, qatlamlar bo'yicha taqsimlangan |
| Timeout statik konstanta | Deadline so'rov bilan uzatiladi, qolgan vaqtga qarab qisqaradi |
| Xato bo'lsa darhol 3 marta qayta uriniladi | Faqat idempotent chaqiruvda, jitter bilan, retry budjeti ostida |
| Pool kattaligi "ko'proq yaxshi" tamoyilida tanlanadi | Little qonuni bilan hisoblanadi, DB max_connections ga sig'adi |
| LB va ilova timeout lari bir-biridan xabarsiz | Tartib qattiq: client idle < LB idle < server keep-alive |
| Baza so'rovi faqat ilova tomonidan cheklanadi | `statement_timeout` rol darajasida, ilovadan mustaqil |
| Tashqi servis sekinlashishi hech qachon sinalmagan | Latency va blackhole inyeksiyasi relizdan oldin o'lchanadi |
| DNS va sertifikat "ishlayapti" deb ishoniladi | TTL, cache va amal qilish muddati monitoring da |

### 32.5 Ulanish hovuzi (HTTP client va JDBC): kattalik, kutish navbati, keep-alive

Pool kattaligini taxmin bilan emas, Little qonuni bilan tanlaysiz: zarur ulanish soni teng throughput ni latency ga ko'paytirganga. Buyurtma servisi 300 rps bersa va bitta DB so'rovi 15 ms ketsa, kerak bo'lgani 300 * 0.015 = 4.5 ulanish. Shuning uchun HikariCP uchun 10 ta ulanish ko'p hollarda yetarli, 100 ta esa zarar. Katta pool kutish navbatini yashiradi va PostgreSQL da har bir ulanish alohida backend process bo'lgani uchun xotira va context switch ni oshiradi.

PostgreSQL `max_connections` 200 bo'lsa va sizda 8 ta pod, har birida 10 ta ulanish bo'lsa, bu 80 ta, ustiga migratsiya, hisobot va admin sessiyalari qo'shiladi. Pod soni avtomatik o'sadigan bo'lsa, shu arifmetikani oldindan qiling yoki PgBouncer ni transaction pooling rejimida qo'yib, ilova va baza sonini ajratib oling.

`maxLifetime` eng ko'p e'tibordan chetda qoladigan parametr. Default 30 daqiqa va u baza yoki LB ulanishni jim o'ldirish vaqtidan KICHIK bo'lishi shart, aks holda pool allaqachon o'lgan ulanishni beradi va siz tasodifiy xatolarni ko'rasiz.

```yaml
spring:
  datasource:
    hikari:
      maximum-pool-size: 10          # Little qonuni: 300 rps * 15 ms
      minimum-idle: 10               # bir xil qiymat, isinish pauzasi bo'lmasin
      connection-timeout: 2000       # navbatda kutish, 30 s emas
      validation-timeout: 1000
      idle-timeout: 600000           # 10 daqiqa
      max-lifetime: 1500000          # 25 daqiqa, LB/PgBouncer chegarasidan kam
      keepalive-time: 120000         # 2 daqiqada bir probe, yarim ochiq ulanishga qarshi
      data-source-properties:
        socketTimeout: 5             # sekund, statement_timeout dan uzunroq
        tcpKeepAlive: true
```

```java
// Reactor Netty: default pendingAcquireTimeout 45 s, bu yashirin latency manbai
ConnectionProvider provider = ConnectionProvider.builder("payments")
        .maxConnections(50)
        .pendingAcquireTimeout(Duration.ofMillis(500)) // tez rad et
        .pendingAcquireMaxCount(100)                   // navbat chuqurligi cheklangan
        .maxIdleTime(Duration.ofSeconds(20))           // LB idle timeout dan kam
        .maxLifeTime(Duration.ofMinutes(5))            // DNS o'zgarishini ko'rish uchun
        .evictInBackground(Duration.ofSeconds(30))
        .build();
```

### 32.6 DNS: TTL, keshlash va JVM dagi DNS kesh sozlamalari

JVM o'z DNS keshini yuritadi. `InetAddress` uchun ijobiy javob keshi default 30 sekund, salbiy javob keshi 10 sekund atrofida. Bu qiymatlar `java.security` fayldagi `networkaddress.cache.ttl` va `networkaddress.cache.negative.ttl` orqali boshqariladi. Eng xavfli sozlama `networkaddress.cache.ttl=-1`, ya'ni abadiy kesh: failover da IP o'zgaradi, lekin JVM eski manzilga urinishda davom etadi va faqat restart yordam beradi.

Ikkinchi qatlam kesh connection pool ning o'zi. Pool ulanishni ushlab turganda DNS o'zgarishi hech qanday ta'sir qilmaydi, chunki yangi rezolyutsiya bo'lmaydi. Shu sababli `maxLifeTime` ni 5 dan 30 daqiqagacha qo'yish kerak: u IP rotatsiyasiga yo'l beradi.

Kubernetes da uchinchi tuzoq `ndots`. Default `ndots:5` bo'lgani uchun to'liq bo'lmagan nom har safar bir necha qidiruv domeni bilan sinaladi, bu har bir rezolyutsiyaga qo'shimcha so'rov va kechikish qo'shadi. Tashqi hostlarni nuqta bilan tugaydigan to'liq nom sifatida yozish shu ortiqcha urinishlarni yo'qotadi.

```bash
# JVM DNS kesh TTL ni ko'rish (abadiy kesh -1 bo'lmasligi kerak)
grep -n 'networkaddress.cache' "$JAVA_HOME/conf/security/java.security"

# Ishga tushirishda aniq qiymat berish
java -Dnetworkaddress.cache.ttl=30 \
     -Dnetworkaddress.cache.negative.ttl=5 \
     -jar order-service.jar

# Kubernetes ichida ortiqcha qidiruv domenlarini ko'rish
cat /etc/resolv.conf   # ndots:5 bo'lsa, FQDN ni nuqta bilan yozing
```

### 32.7 TLS: qo'l siqish narxi, sertifikat muddati, ichki CA, qayta ishlatish

TLS 1.3 to'liq handshake bitta RTT, TLS 1.2 ikkita RTT oladi. Region oralig'ida RTT 30 ms bo'lsa, bu 30 dan 60 ms gacha sof kechikish, ustiga asimmetrik imzo uchun protsessor vaqti, RSA 2048 da taxminan 1 dan 2 ms gacha, ECDSA P-256 da sezilarli kamroq. Demak har so'rovda yangi ulanish ochish p99 ni ikki baravar oshirishi mumkin. Bu yerda optimizatsiya aniq: keep-alive va ulanish hovuzini to'g'ri sozlash, session resumption ni yoqish.

Sertifikat muddati ishlab chiqarishdagi eng oldindan ko'rinadigan, lekin eng ko'p qaytariladigan avariya. Ichki CA ishlatilsa, truststore da CA sertifikati bo'lishi va uning muddati ham kuzatilishi kerak. Spring Boot 3.1 dan boshlab SSL bundle mavzusi markazlashgan va bundle ni fayl o'zgarganda qayta yuklash mumkin, bu rotatsiyani restart siz qiladi. Hostname tekshiruvini o'chirish esa hech qachon yechim emas, u shunchaki muammoni kelasi yilga suradi.

```bash
# Sertifikat muddati va handshake vaqtini bir yo'la o'lchash
echo | openssl s_client -connect payments.internal:8443 -servername payments.internal \
  2>/dev/null | openssl x509 -noout -subject -issuer -dates

# 30 kundan kam qolganini CI da tekshirish
echo | openssl s_client -connect payments.internal:8443 2>/dev/null \
  | openssl x509 -noout -checkend 2592000 || echo "SERTIFIKAT TEZDA TUGAYDI"

# Handshake narxi: har bir urinishda sarflangan vaqt
curl -sS -o /dev/null -w 'tcp=%{time_connect} tls=%{time_appconnect} ttfb=%{time_starttransfer}\n' \
  https://payments.internal:8443/health
```

### 32.8 Qayta urinish siyosati: faqat idempotent chaqiruvda, eksponensial kechikish va jitter

Qayta urinish faqat ikki shart bajarilganda xavfsiz. Birinchisi: operatsiya idempotent, ya'ni ikki marta bajarilsa natija bir xil. To'lovni yaratish o'z-o'zidan idempotent emas, u faqat idempotency key bilan shunday bo'ladi. Ikkinchisi: xato turi qayta urinishga arzaydi. Connect timeout da so'rov serverga yetmagan, demak xavfsiz. Read timeout da so'rov yetgan bo'lishi mumkin va javob yo'qolgan, demak yozish operatsiyasi uchun xavfli.

Kechikish eksponensial bo'lishi va albatta jitter bilan bo'lishi kerak. Jitter bo'lmasa barcha klientlar bir vaqtda qayta uradi va servis tiklanishga ulgurmaydi. Amalda ishlaydigan formula "full jitter": kutish vaqti 0 dan `min(cap, base * 2^urinish)` oralig'idagi tasodifiy son.

Eng katta xavf retry amplifikatsiyasi. Uch qatlamning har biri 3 urinish qilsa, bitta foydalanuvchi so'rovi eng chuqur servisga 27 chaqiruv bo'lib tushadi. Shuning uchun qayta urinish bitta qatlamda, odatda chetki qatlamda bo'ladi va retry ulushi umumiy trafikning 10 foizidan oshmasligi kuzatiladi.

```java
// Full jitter: urinishlar bir vaqtda to'planib qolmaydi
private Duration backoff(int attempt) {
    long base = 50;                                   // ms
    long cap  = 2_000;                                // yuqori chegara
    long expo = Math.min(cap, base * (1L << Math.min(attempt, 10)));
    return Duration.ofMillis(ThreadLocalRandom.current().nextLong(expo + 1));
}

// Qayta urinishga arzaydimi: yozish operatsiyasida read timeout xavfli
private boolean retryable(Exception e, HttpMethod m, Integer status) {
    if (e instanceof ConnectException) return true;                 // so'rov yetmagan
    if (e instanceof HttpTimeoutException) return m.isIdempotent(); // natija noaniq
    return status != null && (status == 429 || status == 503 || status == 504);
}
```

### 32.9 Orqaga bosim (backpressure) va navbat chuqurligini cheklash

Cheksiz navbat muammoni yo'qotmaydi, uni kechiktiradi va yomonlashtiradi. Navbatda 30 sekund yotgan so'rov allaqachon mijoz uchun o'lik, lekin u hali ham thread, ulanish va CPU yeydi. Tomcat da `max-threads` default 200, `accept-count` default 100. Bu degani og'ir paytda 300 ta so'rov tizim ichida bo'ladi va har biri deadline ni yemoqda.

To'g'ri yondashuv ikki qismdan iborat. Birinchisi: bir vaqtdagi chaqiruvlar sonini cheklash. Yana Little qonuni, sekin dependency uchun ruxsat soni teng maqsadli rps ni p99 latency ga ko'paytirganga. 50 rps va 200 ms bo'lsa 10 ta ruxsat yetarli. Ikkinchisi: navbatdan olinganda deadline ni tekshirish. Vaqti tugagan ishni bajarmasdan tashlash bepul tezlik beradi.

```java
// Navbatdan olgandan keyin deadline ni tekshirish: o'lik ishni bajarmaymiz
Semaphore permits = new Semaphore(10);     // 50 rps * 0.2 s

Optional<Quote> fetchQuote(Deadline dl) throws InterruptedException {
    Duration wait = dl.remaining();
    if (!permits.tryAcquire(wait.toMillis(), TimeUnit.MILLISECONDS)) {
        rejected.increment();              // tez rad etish, 503 va Retry-After
        return Optional.empty();
    }
    try {
        if (dl.remaining().toMillis() < 100) return Optional.empty(); // kech qoldi
        return Optional.of(client.quote(dl.budgetFor(Duration.ofMillis(800))));
    } finally {
        permits.release();
    }
}
```

### 32.10 Tashqi servis bilan shartnoma: versiyalash, buzilmaydigan o'zgarish, ogohlantirish

Integratsiya shartnomasi kod emas, kelishuv. Buzilmaydigan o'zgarishlar ro'yxati qisqa: yangi majburiy bo'lmagan maydon qo'shish, yangi endpoint qo'shish, xato matnini aniqlashtirish. Buziladigan o'zgarishlar: maydonni olib tashlash, nomini o'zgartirish, turini toraytirish, majburiy qilish, enum qiymati semantikasini o'zgartirish, default xatti-harakatni almashtirish.

Iste'molchi tomonida himoya "tolerant reader" tamoyili: notanish maydonni e'tiborsiz qoldirish va notanish enum qiymatini xatoga aylantirmaslik. Ombor servisi `RESERVED` holatini qo'shsa, sizning buyurtma servisi deserializatsiyada yiqilmasligi kerak. Ayni paytda sizga haqiqatan kerak bo'lgan maydonlar uchun tekshiruv qattiq bo'lsin, aks holda `null` ichkariga sizib kiradi.

Versiyalash yo'li muhim emas, barqarorligi muhim. URI da `/v1` ko'rinadi va keshga qulay, media type versiyalash nozikroq. Muhimi: eski versiya o'chirilishidan oldin ogohlantirish oynasi bo'lsin, odatda `Deprecation` va `Sunset` sarlavhalari bilan va kamida 90 kun. Shartnoma avtomatik tekshiruvi uchun testlash qo'llanmasidagi contract testing bo'limiga qara.

```java
@Configuration
class JsonContractConfig {
    @Bean
    Jackson2ObjectMapperBuilderCustomizer tolerantReader() {
        return b -> b
            // Yetkazib beruvchi yangi maydon qo'shsa yiqilmaymiz
            .featuresToDisable(DeserializationFeature.FAIL_ON_UNKNOWN_PROPERTIES)
            // Notanish enum qiymati default ga tushadi, xatoga emas
            .featuresToEnable(DeserializationFeature.READ_UNKNOWN_ENUM_VALUES_USING_DEFAULT_VALUE);
    }
}

enum StockStatus {
    AVAILABLE, OUT_OF_STOCK,
    @JsonEnumDefaultValue UNKNOWN   // kelasi versiyadagi yangi holatlar uchun
}
```

### 32.11 Yuk tarqatuvchi va proxy sozlamalari: idle timeout nomuvofiqligi tuzog'i

Eng ko'p uchraydigan "tushunarsiz 502" sababi idle timeout poygasi. Mijoz pool da ulanishni 60 sekund bo'sh ushlaydi, LB ham 60 sekundda bo'sh ulanishni yopadi. Mijoz 59.9 sekundda so'rov yuboradi, LB ayni o'sha payt FIN yuboradi, natijada so'rov yo'qolgan ulanishga tushadi. Bu tasodifiy, past chastotali va qidirish qiyin xato.

Qoida oddiy va qattiq: mijozning bo'sh ulanish vaqti LB dan kichik, LB esa backend keep-alive dan kichik bo'lsin. Masalan client pool idle 20 sekund, LB idle 60 sekund, Tomcat keep-alive 75 sekund. Shu tartib buzilsa, ulanishni har safar faqat yopuvchi tomon biladi va boshqa tomon kech xabar topadi.

Ikkinchi tuzoq proxy ning o'qish timeout i. Reverse proxy larda bu odatda 60 sekund atrofida. Ombor qoldig'i bo'yicha og'ir hisobot 90 sekund ishlasa, proxy mijozga 504 beradi, lekin backend so'rovni davom ettiradi va resurs yeydi. Bu yerda yechim timeout ni oshirish emas, uzoq operatsiyani asinxron qilish va holat so'rash endpoint i bilan berish.

```properties
# Tartib: client idle (20s) < LB idle (60s) < server keep-alive (75s)
server.tomcat.keep-alive-timeout=75s
server.tomcat.max-keep-alive-requests=200
server.tomcat.connection-timeout=5s
server.tomcat.threads.max=200
server.tomcat.accept-count=50

# Hikari maxLifetime PgBouncer server_idle_timeout dan kichik bo'lsin
spring.datasource.hikari.max-lifetime=1500000
```

### 32.12 Integratsiyani sinash: tashqi servis sekinlashganda nima bo'ladi

Integratsiyani sinashda asosiy savol "xato qaytsa nima bo'ladi" emas, "sekinlashsa nima bo'ladi". Toza xato oson, u darhol qaytadi. Haqiqiy avariya esa dependency 5 sekundda javob berganda boshlanadi: thread pool to'ladi, navbat o'sadi, deadline tugaydi va sizning servis ham o'ladi, garchi o'zi sog'ligi joyida bo'lsa.

Kamida beshta sahnani o'lchash kerak: dependency ga 5 sekund latency qo'shilgan, dependency paketni jim tashlaydigan blackhole, javobni sekin tomchilab yuborish, sertifikat muddati tugagan, DNS javob bermaydi. Har safar uchta raqamni yozib olasiz: birinchi xatoga qancha vaqtda yetildi, avariya paytida qancha foiz so'rov bajarildi, dependency tiklangandan keyin servis necha sekundda normaga qaytdi. Oxirgi raqam 30 sekunddan uzun bo'lsa, pool va retry sozlamalaringiz noto'g'ri. Buni avtomatlashtirish vositalari testlash qo'llanmasidagi resilience testlari bo'limida.

| tuzoq | yechim |
| --- | --- |
| Read timeout butun so'rov deb o'ylash | Umumiy deadline qo'shish, sekin tomchilovchi javobni sinash |
| Pool acquire timeout default 45 sekund | Aniq 300 dan 500 ms gacha, navbat chuqurligi cheklangan |
| `maxLifetime` LB yoki PgBouncer idle timeout dan katta | Pool tomonida qisqaroq qiymat, keepalive probe yoqilgan |
| `networkaddress.cache.ttl=-1` abadiy DNS kesh | 30 sekund TTL va ulanish umrini cheklash |
| Barcha xatoga 3 marta qayta urinish | Idempotentlik tekshiruvi va bitta qatlamda retry |
| Jitter siz eksponensial backoff | Full jitter, tasodifiy oraliq 0 dan cap gacha |
| Client va LB idle timeout teng | Qattiq tartib: client < LB < server keep-alive |
| Ilovada timeout bor, bazada yo'q | Rol darajasida `statement_timeout` va `lock_timeout` |
| Notanish enum deserializatsiyani buzadi | Tolerant reader va default enum qiymati |
| Sertifikat muddati faqat avariyada bilinadi | CI da `checkend` tekshiruvi va 30 kunlik ogohlantirish |

### 32.13 Amalda qo'llash

- [ ] Barcha tashqi HTTP klientlarni ro'yxatga oling va har biriga connect, pool acquire, read va umumiy deadline qiymatlarini aniq yozib chiqing, default qolgan joy qolmasin.
- [ ] Asosiy API lar uchun timeout byudjetini chizing: SLO dan boshlab har bir quyi chaqiruvga millisekund taqsimlang va yig'indi SLO dan kichik ekanini tekshiring.
- [ ] HikariCP va HTTP pool kattaligini Little qonuni bilan qayta hisoblang, keyin barcha podlar yig'indisini PostgreSQL `max_connections` bilan solishtiring.
- [ ] `maxLifetime`, `idleTimeout` va LB hamda PgBouncer idle timeout qiymatlarini bitta jadvalga yozib, tartib buzilmaganiga ishonch hosil qiling.
- [ ] Rol darajasida `statement_timeout`, `lock_timeout` va `idle_in_transaction_session_timeout` ni o'rnatib, OLTP va hisobot rollarini ajrating.
- [ ] Qayta urinish siyosatini audit qiling: idempotentlik kalitlari bor-yo'qligini, full jitter ishlatilganini va retry faqat bitta qatlamda bo'lishini tasdiqlang.
- [ ] Sertifikat muddatini CI da `checkend` bilan tekshiradigan qadam qo'shing va truststore dagi ichki CA muddatini ham kuzatuvga oling.
- [ ] Eng muhim dependency ga 5 sekund latency va blackhole inyeksiya qilib, birinchi xato vaqtini, bajarilgan so'rov ulushini va tiklanish vaqtini o'lchab, natijani relizga shart qilib qo'ying.


# VI. Amaliyot va o'sish

## 33. Sxema migratsiyasi va to'xtashsiz reliz (Schema Migration and Zero-Downtime Release)

Sxema relizning eng qaytarib bo'lmaydigan qismi. Kodni oldingi image'ga qaytarish bir daqiqa oladi, o'chirilgan ustunni qaytarish esa backup'dan tiklashni talab qiladi. Shuning uchun arxitektor sxema o'zgarishini bir necha relizga cho'zilgan bosqichli operatsiya deb ko'radi. Bu bobda shu operatsiyaning mexanikasi bor: qaysi DDL qanday lock oladi, qaysi o'zgarish jadvalni qayta yozadi, va kod bilan sxemani qanday tartibda chiqarish kerak.

### 33.1 Migratsiya vositalari: Flyway va Liquibase, versiyalash va nomlash tartibi

Flyway va Liquibase bir masalani hal qiladi: sxemaning qaysi o'zgarishi allaqachon qo'llanganini bazaning o'zida saqlash. Flyway buni `flyway_schema_history` jadvalida qiladi: versiya, tavsif, skript nomi va checksum. Liquibase `DATABASECHANGELOG` va `DATABASECHANGELOGLOCK` jadvallarini ishlatadi, har changeset `id` va `author` juftligi bilan aniqlanadi.

Tanlov mexanikaga bog'liq. Bitta PostgreSQL bilan ishlaydigan to'lov servisi uchun Flyway yetarli, chunki SQL baribir Postgres'ga xos bo'ladi. Bir nechta DBMS'ni qo'llaydigan mahsulotda Liquibase abstraksiyasi va changeset ichidagi rollback bloki foyda beradi.

Versiyani vaqt belgisi bilan bering, shunda ikki developer bir vaqtda migratsiya yozsa, raqam to'qnashmaydi.

```bash
  # Flyway: versiya = UTC vaqt belgisi, tavsif = qisqa va fe'lsiz
db/migration/V20260112_1430__order_add_delivery_slot_column.sql
db/migration/V20260112_1655__order_backfill_delivery_slot.sql
db/migration/V20260113_0910__order_delivery_slot_set_not_null.sql
db/migration/V20260120_1100__order_drop_legacy_delivery_time.sql

  # Repeatable: har marta checksum o'zgarsa qayta ishlaydi (view, funksiya)
db/migration/R__view_warehouse_stock_summary.sql
```

Bitta fayl bitta mantiqiy o'zgarish bo'lsin. Ustun qo'shish va backfill alohida fayl, chunki ularning lock profili butunlay boshqa.

### 33.2 Migratsiya qoidalari: oldinga faqat yangi fayl, qo'lda o'zgartirmaslik

Qoida bitta va qattiq: `main` branch'ga tushgan migratsiya fayli o'zgarmas. Flyway har faylning checksum'ini saqlaydi va o'zgargan faylni ko'rib ishga tushishdan bosh tortadi. Bu himoya: aks holda ikki muhitning sxemasi jimgina ajralib ketadi.

Shuning uchun xatoni tuzatish yo'li bitta: yangi fayl yozish. `V...1430__add_column.sql` da tip xato bo'lsa, uni tahrirlamaymiz, `V...1700__fix_column_type.sql` qo'shamiz.

```yaml
spring:
  flyway:
    enabled: true
    locations: classpath:db/migration
    # checksum tekshiruvini O'CHIRMA, bu xatolikni erta ushlaydi
    validate-on-migrate: true
    # tartibdan tashqari migratsiyaga ruxsat bermaymiz
    out-of-order: false
    # mavjud bazaga birinchi ulanishda baseline faqat bir marta
    baseline-on-migrate: false
    # har migratsiya o'z tranzaksiyasida, biri yiqilsa keyingisi ishlamaydi
    group: false
  jpa:
    hibernate:
      # production'da MUTLAQO none, Hibernate sxemaga tegmasin
      ddl-auto: none
```

`spring.jpa.hibernate.ddl-auto` qiymati production'da `none` bo'lishi shart. `update` qiymati Hibernate'ga sxemani o'zgartirish huquqini beradi, u esa index va cheklovlarni o'zicha qo'shadi, migratsiya tarixiga esa hech narsa yozmaydi.

Qo'lda `psql` ochib production'da `ALTER TABLE` yozish ham xuddi shunday buzilish. Shoshilinch tuzatishni ham avval migratsiya fayli sifatida commit qiling.

### 33.3 Kengaytirish va qisqartirish (expand and contract) usuli bosqichma-bosqich

To'xtashsiz relizning asosiy g'oyasi: hech qachon kod va sxemani bir vaqtda mos kelmaydigan holatga keltirmaslik. Rolling deployment paytida bir necha daqiqa davomida eski va yangi kod bir xil bazaga yozadi. Demak sxema shu ikki versiyaning ikkisiga ham mos bo'lishi kerak.

Bosqichlar ketma-ketligi quyidagicha. Birinchi bosqich (expand): sxemaga yangi struktura qo'shiladi, eskisi joyida qoladi. Yangi ustun `NULL` qabul qiladi, yangi jadval bo'sh. Eski kod buni sezmaydi.

Keyin kod chiqadi va ikki joyga yozadi, eski joydan o'qiydi. Uchinchi bosqichda backfill eski ma'lumotni ko'chiradi. To'rtinchida kod yangi joydan o'qiydi, eskisiga hali yozadi. Beshinchida eski joyga yozish to'xtaydi. Oltinchida (contract) eski ustun o'chiriladi.

Har bosqich alohida deploy va har biri orqaga qaytishga ochiq. To'lov servisidagi `amount` ustunini `numeric(19,4)` ga o'tkazish shu yo'l bilan ikki hafta davom etadi, lekin bironta so'rov yo'qolmaydi. Alternativa bitta tungi `ALTER TABLE`, u 50 million qatorli jadvalda bir soat lock ushlaydi.

### 33.4 Ustun qo'shish, nomini o'zgartirish va o'chirishning xavfsiz ketma-ketligi

Ustun qo'shish eng oson holat: `NULL` ruxsatli ustun qo'shiladi, keyin kod uni to'ldira boshlaydi. Ustun nomini o'zgartirish esa eng xavfli, chunki `ALTER TABLE ... RENAME COLUMN` bir zumda ishlaydi, lekin eski kod shu sekundda `column does not exist` xatosini oladi.

Shuning uchun rename hech qachon rename sifatida bajarilmaydi. U "yangi ustun qo'shish, ko'chirish, eskisini o'chirish" ga aylantiriladi.

```sql
-- 1-bosqich: yangi ustun, NULL ruxsatli, default yo'q
ALTER TABLE orders ADD COLUMN delivery_slot_id bigint;

-- 2-bosqich: yangi kod ikki ustunga ham yozadi (dual write)

-- 3-bosqich: backfill bo'laklab (pastdagi bo'limga qarang)

-- 4-bosqich: cheklovni NOT VALID bilan qo'shamiz, keyin tasdiqlaymiz
ALTER TABLE orders
  ADD CONSTRAINT orders_delivery_slot_fk
  FOREIGN KEY (delivery_slot_id) REFERENCES delivery_slots (id) NOT VALID;
ALTER TABLE orders VALIDATE CONSTRAINT orders_delivery_slot_fk;

-- 5-bosqich: kod faqat yangi ustundan o'qiydi va unga yozadi

-- 6-bosqich: eski ustunni o'chirish, oldingi relizdan 1-2 hafta keyin
ALTER TABLE orders DROP COLUMN legacy_delivery_time;
```

`DROP COLUMN` PostgreSQL'da metadata operatsiyasi: ustun `pg_attribute` da `attisdropped` bilan belgilanadi, ma'lumot esa joyida qoladi. Ya'ni u tez, lekin diskni darhol bo'shatmaydi.


### 33.5 Qaysi DDL jadvalni bloklaydi: `ALTER TABLE` turlarining lock darajasi

PostgreSQL'da deyarli har qanday `ALTER TABLE` `ACCESS EXCLUSIVE` lock oladi. Bu lock hamma narsani bloklaydi, hatto `SELECT` ni ham. Muhim nuqta shunda: lock qancha ushlanadi, va uni olish uchun qancha kutiladi.

Eng ko'p uchraydigan halokat shu: `ALTER TABLE` uzoq ishlaydigan `SELECT` ortida navbatga tushadi. PostgreSQL navbatda adolatni saqlaydi, shuning uchun `ALTER TABLE` dan keyin kelgan oddiy `SELECT` lar ham navbatda to'planadi. Natijada 20 millisekundlik DDL butun jadvalni 3 daqiqa o'chirib qo'yadi.

| DDL operatsiyasi | Lock darajasi | Jadvalni qayta yozadimi |
| --- | --- | --- |
| `ADD COLUMN` (default yo'q yoki constant default) | ACCESS EXCLUSIVE, juda qisqa | Yo'q |
| `ADD COLUMN` volatile default bilan | ACCESS EXCLUSIVE, uzoq | Ha, to'liq |
| `DROP COLUMN` | ACCESS EXCLUSIVE, qisqa | Yo'q |
| `ALTER COLUMN TYPE int` dan `bigint` ga | ACCESS EXCLUSIVE, uzoq | Ha, to'liq |
| `SET NOT NULL` (valid CHECK bor) | ACCESS EXCLUSIVE, qisqa | Yo'q |
| `ADD CONSTRAINT ... NOT VALID` | ACCESS EXCLUSIVE, qisqa | Yo'q |
| `VALIDATE CONSTRAINT` | SHARE UPDATE EXCLUSIVE | Yo'q, lekin to'liq skan |
| `CREATE INDEX` | SHARE (yozish bloklanadi) | Yo'q |
| `CREATE INDEX CONCURRENTLY` | SHARE UPDATE EXCLUSIVE | Yo'q, ikki marta skan |

Himoya mexanizmi `lock_timeout`: kutish cho'zilsa migratsiya xato bilan to'xtaydi va boshqa so'rovlarni bo'g'maydi.

```sql
-- Har migratsiya faylining boshida: lockni 3 sekunddan ko'p kutmaymiz
SET lock_timeout = '3s';
-- DDL o'zi ham cheklangan bo'lsin
SET statement_timeout = '30s';

ALTER TABLE orders ADD COLUMN delivery_slot_id bigint;

-- Agar lock_timeout ishga tushsa: 55P03 lock_not_available xatosi.
-- Deploy pipeline shu xatoni ko'rib migratsiyani 1 daqiqadan keyin
-- qayta urinishi kerak, 5 martagacha.
```

### 33.6 Katta jadvalga ustun qo'shish va standart qiymat masalasi

PostgreSQL 11 dan boshlab constant default bilan ustun qo'shish jadvalni qayta yozmaydi. Default qiymat `pg_attribute.attmissingval` da saqlanadi va o'qishda qatorga "yopishtiriladi". Ya'ni `ADD COLUMN status text DEFAULT 'NEW' NOT NULL` 80 million qatorli `orders` jadvalida ham taxminan 20 millisekundda tugaydi.

Lekin default volatile funksiya bo'lsa, qoida buziladi. `DEFAULT gen_random_uuid()` yoki `DEFAULT clock_timestamp()` har qatorga boshqa qiymat beradi, demak PostgreSQL har qatorni yangidan yozishga majbur. 80 million qatorli jadvalda bu disk hajmining ikki baravariga va taxminan 20-40 daqiqa `ACCESS EXCLUSIVE` lock'ga olib keladi.

```sql
-- XAVFLI: volatile default jadvalni to'liq qayta yozadi
ALTER TABLE payments ADD COLUMN idempotency_key uuid DEFAULT gen_random_uuid();

-- XAVFSIZ: default yo'q, keyin backfill, keyin default
ALTER TABLE payments ADD COLUMN idempotency_key uuid;
-- backfill bo'laklab bajariladi
ALTER TABLE payments ALTER COLUMN idempotency_key SET DEFAULT gen_random_uuid();

-- XAVFSIZ: constant default, PG 11+ da metadata operatsiyasi
ALTER TABLE orders ADD COLUMN channel text NOT NULL DEFAULT 'WEB';
```

`now()` stable, `clock_timestamp()` volatile. Shuning uchun `DEFAULT now()` bilan ustun qo'shish qayta yozishga olib kelmaydi. Ishonchsiz bo'lsangiz production hajmidagi nusxada `\timing` bilan o'lchang.

### 33.7 `NOT NULL` va `CHECK` cheklovini to'xtashsiz qo'shish (`NOT VALID` va `VALIDATE`)

Cheklovni qo'shishda ikki xarajat bor: lock olish va mavjud ma'lumotni tekshirish. `NOT VALID` bu ikkisini ajratadi. `ADD CONSTRAINT ... NOT VALID` faqat katalogga yozadi, mavjud qatorlarni tekshirmaydi, lekin yangi va o'zgargan qatorlarga darhol amal qila boshlaydi. Keyin `VALIDATE CONSTRAINT` mavjud ma'lumotni tekshiradi va u `SHARE UPDATE EXCLUSIVE` lock oladi, ya'ni o'qish ham yozish ham davom etadi.

`SET NOT NULL` uchun PostgreSQL 12 dan boshlab nozik yo'l bor. Agar jadvalda `col IS NOT NULL` ni isbotlaydigan valid `CHECK` cheklovi bo'lsa, planner to'liq skanni o'tkazib yuboradi.

```sql
-- 1-qadam: tekshirmaydigan CHECK, qisqa lock
ALTER TABLE orders
  ADD CONSTRAINT orders_delivery_slot_not_null
  CHECK (delivery_slot_id IS NOT NULL) NOT VALID;

-- 2-qadam: tasdiqlash, o'qish va yozish bloklanmaydi
ALTER TABLE orders VALIDATE CONSTRAINT orders_delivery_slot_not_null;

-- 3-qadam: PG 12+ valid CHECK borligini ko'rib skan qilmaydi
ALTER TABLE orders ALTER COLUMN delivery_slot_id SET NOT NULL;

-- 4-qadam: endi CHECK keraksiz, uni olib tashlaymiz
ALTER TABLE orders DROP CONSTRAINT orders_delivery_slot_not_null;
```

`VALIDATE CONSTRAINT` 80 million qatorli jadvalda sequential scan qiladi, bu taxminan 2-5 daqiqa oladi. Uni yuk kam vaqtda ishga tushiring, lekin tungi oyna shart emas, chunki hech kim bloklanmaydi.

### 33.8 Indeksni ishlab chiqarishda qo'shish: `CONCURRENTLY` va u uzilganda nima bo'ladi

Oddiy `CREATE INDEX` `SHARE` lock oladi: o'qish davom etadi, yozish to'xtaydi. 50 million qatorli `payments` jadvalida bu 5-15 daqiqa yozishsiz qolish degani. `CONCURRENTLY` yozishga xalaqit bermaydi, lekin jadvalni ikki marta skanlaydi va taxminan ikki baravar uzoq ishlaydi.

Ikki muhim shart. Birinchisi: `CONCURRENTLY` tranzaksiya ichida ishlamaydi. Flyway'da bunday faylga maxsus belgi kerak.

```sql
-- flyway migratsiyasida tranzaksiyani o'chirish uchun fayl nomiga
-- Flyway'ning transactional=false sozlamasi yoki alohida callback kerak.
-- Liquibase'da changeset'ga runInTransaction="false" qo'yiladi.

CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_payments_merchant_created
  ON payments (merchant_id, created_at DESC);

-- Uzilgandan keyin tekshirish: invalid indeks qolganini topish
SELECT c.relname, i.indisvalid
FROM pg_index i
JOIN pg_class c ON c.oid = i.indexrelid
WHERE NOT i.indisvalid;

-- Invalid indeksni tozalash, u ham CONCURRENTLY bo'lsin
DROP INDEX CONCURRENTLY IF EXISTS idx_payments_merchant_created;
```

Ikkinchi shart: `CONCURRENTLY` uzilib qolsa, PostgreSQL `indisvalid = false` holatidagi indeksni qoldiradi. Bu indeks so'rovlarda ishlatilmaydi, lekin `INSERT` va `UPDATE` da yangilanadi, ya'ni faqat sekinlashtiradi va joy egallaydi. Shuning uchun har migratsiya ishga tushgandan keyin invalid indekslarni tekshiradigan avtomatik nazorat bo'lishi kerak.

Yana bir tuzoq: `CONCURRENTLY` boshlanish paytidagi ochiq tranzaksiyalarni kutadi. Bitta 40 daqiqalik hisobot so'rovi indeks yaratishni shu muddatga ushlab turadi, shuning uchun avval `pg_stat_activity` ni ko'rib chiqing.

### 33.9 Ma'lumotni ko'chirish (backfill): bo'laklab, yuk nazorati bilan

Bitta `UPDATE orders SET delivery_slot_id = ...` 80 million qatorda ulkan tranzaksiya ochadi, WAL hajmini o'nlab gigabaytga oshiradi, replika lag'ini cho'zadi va autovacuum'ni dead tuple ostida ko'madi. Bundan tashqari, u yiqilsa butun ish nolga qaytadi.

To'g'ri yo'l: primary key diapazoni bo'yicha bo'laklash, har bo'lak alohida tranzaksiya, bo'laklar orasida pauza va replika lag'ini kuzatish.

```sql
-- Bitta bo'lak: 5000 qator, o'z tranzaksiyasida
UPDATE orders o
SET delivery_slot_id = ds.id
FROM delivery_slots ds
WHERE o.legacy_delivery_time = ds.slot_time
  AND o.delivery_slot_id IS NULL
  AND o.id >= :from_id AND o.id < :from_id + 5000;

-- Qolgan ishni o'lchash, progress ko'rinib turishi uchun
SELECT count(*) FROM orders
WHERE delivery_slot_id IS NULL AND id < :max_id;

-- Replika lag'ini bo'laklar orasida tekshirish
SELECT application_name,
       pg_wal_lsn_diff(sent_lsn, replay_lsn) AS lag_bytes
FROM pg_stat_replication;
```

Backfill'ni dastur ichida boshqarish qulay, chunki shunda lag bo'yicha tormozlash mantiqi joylashadi.

```java
// Backfill runner: har bo'lak alohida tranzaksiyada, REQUIRES_NEW bilan
@Service
public class DeliverySlotBackfill {

    private static final int BATCH = 5000;
    private static final long MAX_LAG_BYTES = 32L * 1024 * 1024; // 32 MB

    private final BackfillBatchExecutor executor; // @Transactional(REQUIRES_NEW)
    private final ReplicationLagProbe lagProbe;

    public void run(long maxId) throws InterruptedException {
        for (long from = 0; from < maxId; from += BATCH) {
            int updated = executor.updateRange(from, from + BATCH);
            // lag oshib ketsa to'xtab turamiz, replikani bo'g'maymiz
            while (lagProbe.lagBytes() > MAX_LAG_BYTES) {
                Thread.sleep(2_000);
            }
            if (updated > 0) {
                Thread.sleep(50); // autovacuum nafas olsin
            }
        }
    }
}
```

Bo'lak kattaligini tajriba bilan tanlang. 5000 qator odatda 50-200 millisekund oladi, bu qabul qilinadigan muddat. 100000 qatorli bo'lak esa lock navbatini yaratadi va deadlock ehtimolini oshiradi.

### 33.10 Kod va sxema relizini bir-biriga moslashtirish: eski kod yangi sxemada ishlasin

Kubernetes rolling update paytida eski va yangi pod'lar bir necha daqiqa yonma-yon ishlaydi. Shundan kelib chiqadigan qoida: har bir migratsiya oldingi reliz kodi bilan mos bo'lishi shart. Buni "N-1 moslik" deb atash mumkin.

Shundan kelib chiqib yangi ustun `NULL` ruxsatli bo'lishi kerak, chunki eski kod uni to'ldirmaydi. Oraliq relizda Hibernate entity ikki ustunni ham bilsin.

Flyway Spring Boot startup'ida ishlaydi va advisory lock orqali bir vaqtda faqat bitta pod migratsiya qilishini kafolatlaydi. Lekin bu pod startup vaqtini migratsiya vaqtiga bog'laydi: 4 daqiqalik `VALIDATE CONSTRAINT` liveness probe'ni ishga tushiradi.

```yaml
  # Migratsiya alohida Job, deploy'dan oldin ishlaydi
apiVersion: batch/v1
kind: Job
metadata:
  name: payment-service-migrate
  annotations:
    "helm.sh/hook": pre-upgrade
    "helm.sh/hook-weight": "-5"
spec:
  backoffLimit: 3            # lock_timeout xatosida qayta urinadi
  activeDeadlineSeconds: 900 # 15 daqiqadan oshsa to'xtatamiz
  template:
    spec:
      restartPolicy: Never
      containers:
        - name: migrate
          image: registry.local/payment-service:1.42.0
          args: ["--spring.main.web-application-type=none",
                 "--spring.flyway.enabled=true"]
```

Application pod'larida esa `spring.flyway.enabled=false` bo'ladi: pod faqat sxema tayyor holatda ko'tariladi.

### 33.11 Orqaga qaytish (rollback) rejasi: sxemani qaytarish nega qiyin

Sxema rollback'i kod rollback'iga o'xshamaydi. `DROP COLUMN` ni qaytarish mumkin emas, chunki ma'lumot yo'q. `ALTER COLUMN TYPE` ni qaytarish yana bir to'liq qayta yozish. Backfill'ni qaytarish uchun esa qaysi qator o'zgargani haqida yozuv kerak.

Shuning uchun amaliy strategiya rollback'ni emas, oldinga tuzatishni (forward fix) rejalashtirishdir. Expand va contract usuli bu strategiyaning asosi: eski struktura joyida turganda rollback oddiygina eski image'ni qaytarishga aylanadi.

```yaml
  # Liquibase: rollback blokini changeset ichida e'lon qilish
databaseChangeLog:
  - changeSet:
      id: 20260112-1430-order-add-delivery-slot
      author: payments-team
      changes:
        - addColumn:
            tableName: orders
            columns:
              - column:
                  name: delivery_slot_id
                  type: bigint
      rollback:
        - dropColumn:
            tableName: orders
            columnName: delivery_slot_id
  - changeSet:
      id: 20260120-1100-order-drop-legacy-column
      author: payments-team
      comment: "Qaytarib bo'lmaydi, oldin backup tekshirilsin"
      changes:
        - dropColumn:
            tableName: orders
            columnName: legacy_delivery_time
      rollback:
        - empty: {}
```

Qaytarib bo'lmaydigan migratsiyalarni alohida belgilang va faqat yangi kod ishlab turgani tasdiqlangandan keyin chiqaring, odatda 1-2 hafta keyin. `DROP COLUMN` o'rniga ustunni `legacy_delivery_time_unused` deb nomlash ham ishlaydi: bir hafta xato chiqmasa, demak u rostdan ishlatilmaydi.

### 33.12 Migratsiyani sinash: ishlab chiqarish hajmidagi nusxada vaqtini o'lchash

Migratsiyaning to'g'riligi kichik bazada tekshiriladi, bu testlash qo'llanmasidagi Testcontainers mavzusi. Vaqtini esa faqat production hajmidagi nusxada o'lchash mumkin. 1000 qatorli jadvaldagi `ALTER TABLE` 5 millisekundda, 80 million qatorlisida 40 daqiqada tugaydi, va bu farq butun reliz rejasini o'zgartiradi.

Snapshot'dan nusxa ko'taring, unga production yukining 20-30 foizini bering, keyin migratsiyani `\timing` bilan ishga tushiring. Shu paytda `pg_locks` ni kuzatib, qanday so'rovlar bloklanganini ko'ring.

| Mavzu | Oddiy yondashuv | Arxitektor yondashuvi |
| --- | --- | --- |
| Ustun nomini o'zgartirish | `RENAME COLUMN`, bitta reliz | Yangi ustun, dual write, backfill, eskisini o'chirish |
| Yangi ustunga default | `ADD COLUMN ... DEFAULT gen_random_uuid()` | Default'siz qo'shish, backfill, keyin default |
| `NOT NULL` qo'shish | `SET NOT NULL` to'g'ridan to'g'ri | `CHECK ... NOT VALID`, `VALIDATE`, keyin `SET NOT NULL` |
| Indeks qo'shish | `CREATE INDEX` tungi oynada | `CONCURRENTLY`, invalid indeks nazorati bilan |
| Ma'lumot ko'chirish | Bitta `UPDATE` butun jadvalga | 5000 qatorli bo'laklar, replika lag bo'yicha tormoz |
| Migratsiya qachon ishlaydi | App startup'ida, har pod'da | Alohida `pre-upgrade` Job, app'da Flyway o'chirilgan |
| Lock kutish | Cheksiz kutadi | `lock_timeout = 3s` va pipeline'da qayta urinish |
| Rollback | "Kerak bo'lsa `DROP` qilamiz" | Expand va contract, rollback = eski image |

| Tuzoq | Nega sodir bo'ladi | Yechim |
| --- | --- | --- |
| 20 ms DDL jadvalni 3 daqiqa o'chirdi | `ACCESS EXCLUSIVE` uzoq `SELECT` ortida navbatga tushdi | `lock_timeout = 3s` va retry |
| `ADD COLUMN` 40 daqiqa ketdi | Volatile default to'liq qayta yozishni chaqirdi | Default'siz qo'shib, keyin backfill |
| Indeks so'rovda ishlatilmaydi | `CONCURRENTLY` uzilib `indisvalid = false` qoldirdi | `DROP INDEX CONCURRENTLY` va qayta yaratish |
| Replika 8 daqiqa orqada qoldi | Bitta ulkan `UPDATE` WAL'ni to'ldirdi | Bo'laklash va `pg_stat_replication` nazorati |
| Deploy paytida `column does not exist` | Sxema eski kod bilan mos emas | N-1 moslik qoidasi, expand bosqichi |
| Pod migratsiya paytida restart bo'ldi | Startup migratsiya liveness probe'dan uzoq ketdi | Migratsiyani alohida Job'ga chiqarish |
| Flyway ishga tushmadi, checksum xatosi | Qo'llangan migratsiya fayli tahrirlangan | Faylni qaytarish, tuzatishni yangi faylda berish |
| `DROP COLUMN` dan keyin disk bo'shamadi | Ma'lumot qatorlarda qoladi | `VACUUM FULL` yoki jadvalni asta qayta yozish |

### 33.13 Amalda qo'llash

- [ ] Loyihadagi hamma migratsiya fayllarini ko'rib chiqing va `spring.jpa.hibernate.ddl-auto` production profilida `none` ekanini tasdiqlang.
- [ ] Har migratsiya faylining boshiga `SET lock_timeout = '3s'` qo'shing va deploy pipeline'ga `55P03` xatosida 5 martagacha qayta urinish mantiqini kiriting.
- [ ] Migratsiyani application startup'idan ajratib, alohida `pre-upgrade` Job'ga chiqaring, app pod'larida Flyway'ni o'chiring.
- [ ] Eng katta uchta jadvalning qator sonini va hajmini yozib oling, keyingi migratsiya rejasi shu raqamlarga tayansin.
- [ ] Production snapshot'idan nusxa ko'tarib, keyingi rejalashtirilgan `ALTER TABLE` va `CREATE INDEX CONCURRENTLY` vaqtini o'lchang.
- [ ] Invalid indekslarni (`pg_index.indisvalid = false`) topadigan so'rovni monitoring'ga alert sifatida qo'shing.
- [ ] Backfill uchun bo'laklab ishlaydigan runner yozing, unda bo'lak kattaligi va replika lag chegarasi sozlanadigan bo'lsin.
- [ ] Qaytarib bo'lmaydigan migratsiyalar ro'yxatini tuzing va har biri uchun "oldingi relizdan necha kun keyin chiqadi" muddatini belgilang.

## 34. Legacy kod va bosqichma-bosqich refaktoring (Legacy Code and Refactoring)

Legacy kod degani eski kod emas. Legacy kod degani siz uning xatti-harakatini isbotlay olmaydigan kod. Shu ta'rifdan bitta amaliy xulosa chiqadi: refaktoring kodni o'zgartirishdan emas, kodning hozirgi xatti-harakatini qayd etishdan boshlanadi. Bu bobda arxitektor legacy tizimga kirib, uni to'xtatmasdan bosqichma-bosqich almashtirish ketma-ketligi ko'rib chiqiladi.

### 34.1 Legacy kodga birinchi kun: o'qish, o'lchash, hech narsani o'zgartirmaslik

Birinchi kunning maqsadi bitta: tizimni ishlab turgan holda ko'rish. "Kichik tozalash" qilinmaydi, chunki siz hali qaysi g'alati kod atayin yozilganini bilmaysiz. `OrderService` ichidagi tushunarsiz `if (status == 7 && legacyFlag)` sharti ko'pincha 2019 yildagi real incident'ning yechimi bo'lib chiqadi.

Birinchi kunda uchta narsa yig'iladi: build qanday ishlaydi, ilova qanday ko'tariladi, va production'da qaysi kod aslida chaqiriladi. Uchinchisi eng qimmatli. Spring Boot'da bu `actuator` metrikalari va log'lar orqali ko'rinadi.

```bash
# Build va ishga tushish vaqtini o'lchaymiz, keyin taqqoslash uchun asos bo'ladi
./mvnw -q -DskipTests package   # taxminan 40-90 s bo'lsa normal
# Bean'lar soni: konteyner kattaligi haqida birinchi raqam
curl -s localhost:8080/actuator/beans | jq '[.contexts[].beans | keys[]] | length'
# Eng sekin endpoint'lar: bu refaktoring uchun birinchi nomzodlar ro'yxati
curl -s localhost:8080/actuator/metrics/http.server.requests \
  | jq '.availableTags[] | select(.tag=="uri") | .values'
```

Birinchi kun oxirida sizda o'zgarish emas, o'lchov bo'lishi kerak: startup vaqti, bean soni, eng ko'p chaqirilgan 10 endpoint, eng sekin 10 SQL. Shu raqamlar keyinchalik "yaxshilandi" degan gapni dalilga aylantiradi.

### 34.2 Tizimni tushunish usullari: kirish nuqtalari, ma'lumot oqimi, eng ko'p o'zgargan fayllar

Legacy tizimni to'liq o'qib chiqish mumkin emas. 400 ming qatorli monolitda o'qish tartibi kerak: kirish nuqtalari, ma'lumot oqimi va o'zgarish tarixi.

Kirish nuqtalari deganda HTTP controller'lar, Kafka listener'lar, `@Scheduled` job'lar va JMS consumer'lar tushuniladi. Ularning soni odatda butun kod bazasining 2 foizidan kam, lekin tizim nima qilishini to'liq belgilaydi.

```bash
# Kirish nuqtalari xaritasi: tizim tashqi dunyo bilan qayerda gaplashadi
grep -rln --include=*.java -E '@(RestController|Controller)' src/main/java | wc -l
grep -rn --include=*.java -E '@(KafkaListener|RabbitListener|JmsListener)' src/main/java
grep -rn --include=*.java '@Scheduled' src/main/java

# O'zgarish tarixi: oxirgi 2 yilda eng ko'p tegilgan fayllar
git log --since="2 years ago" --name-only --pretty=format: \
  | grep '\.java$' | sort | uniq -c | sort -rn | head -30
```

Oxirgi buyruq eng muhim ro'yxatni beradi. Tez-tez o'zgaradigan va katta fayl, ya'ni yuqori churn va yuqori murakkablik kesishgan joy, aynan refaktoringdan foyda chiqadigan nuqta. Kamdan kam tegiladigan katta fayl esa odatda tinch qoldiriladi.

Ma'lumot oqimini tushunish uchun jadval darajasiga tushish kerak. PostgreSQL'da qaysi jadval haqiqatan ishlatilayotgani statistikadan ko'rinadi.

```sql
-- Jadvallar bo'yicha haqiqiy yuklama: o'qish va yozish nisbati
SELECT relname,
       seq_scan, idx_scan,
       n_tup_ins AS qoshildi,
       n_tup_upd AS ozgardi,
       n_tup_del AS ochirildi,
       pg_size_pretty(pg_total_relation_size(relid)) AS hajm
FROM pg_stat_user_tables
ORDER BY (coalesce(idx_scan,0) + seq_scan) DESC
LIMIT 20;

-- Umuman ishlatilmayotgan index'lar: ortiqcha yozish narxi
SELECT relname, indexrelname, idx_scan
FROM pg_stat_user_indexes
WHERE idx_scan = 0
ORDER BY pg_relation_size(indexrelid) DESC;
```

Agar `pg_stat_statements` extension yoqilgan bo'lsa, `total_exec_time` bo'yicha tartiblangan birinchi 20 so'rov tizimning haqiqiy og'irlik markazini ko'rsatadi. Odatda butun yuklamaning 80 foizi 10 ta so'rovga tegishli bo'ladi.

### 34.3 Xavfsizlik to'ri qurish: xatti-harakatni qayd etuvchi test

Characterization test oddiy testdan maqsadi bilan farq qiladi. Oddiy test "kod to'g'ri ishlashini" tekshiradi. Characterization test "kod hozir nima qilayotganini" yozib oladi, hatto u noto'g'ri bo'lsa ham. Bu farq muhim, chunki legacy tizimda noto'g'ri xatti-harakat ham ko'pincha mijoz ishonib qolgan xatti-harakatdir.

Amalda bu shunday ketadi: kutilgan natijani o'zingiz o'ylab topmaysiz, kodni ishga tushirib, chiqqan natijani kutilgan deb qayd etasiz. Keyin shu qayddan chetga chiqish regressiya hisoblanadi. Masalan to'lov komissiyasini hisoblash uchun 200 ta real buyurtma ID'si olinadi, eski kod natijasi fayl sifatida saqlanadi, refaktoringdan keyin natija aynan shu fayl bilan taqqoslanadi. Texnikaning o'zi testlash qo'llanmasidagi mos bo'limda ko'rsatilgan, bu yerda faqat tartib muhim.

Arxitektor uchun qoida: characterization test production trafigidan olingan ma'lumotga asoslansin. Sun'iy ma'lumot legacy tizimning eng qiziq holatlarini qamramaydi, chunki legacy tizimning qiymati aynan o'sha g'alati holatlarda yashaydi. Masalan 2016 yilgi valyuta kursi bilan yozilgan buyurtmalar yoki `NULL` yetkazib berish manzili bilan yopilgan to'lovlar.

### 34.4 Chok (seam) topish: o'zgarishni kiritish mumkin bo'lgan nuqta

Seam deganda kod xatti-harakatini o'sha joyni tahrirlamasdan o'zgartirish mumkin bo'lgan nuqta tushuniladi. Spring ilovasida seam'lar odatda topish oson, chunki konteyner o'zi almashtirish mexanizmini beradi.

Amaliy seam turlari: interface orqali inject qilingan dependency, `@Bean` metodi, `@ConditionalOnProperty` bilan boshqariladigan konfiguratsiya, HTTP client abstraksiyasi, va `ApplicationEventPublisher`. Eng yomon holat esa `new PaymentGateway()` yoki `static` utility chaqiruvi, u yerda seam yo'q va avval uni yaratish kerak.

```java
// OLDIN: seam yo'q, kodni test ham, almashtirish ham mumkin emas
public class PaymentService {
    public Receipt charge(Order order) {
        var gateway = new AcquirerGateway("https://acq.example.com"); // qotib qolgan
        return gateway.charge(order.total());
    }
}

// KEYIN: minimal o'zgarish bilan seam yaratildi, mantiq tegilmadi
public class PaymentService {
    private final AcquirerClient client; // interface, almashtirish mumkin

    public PaymentService(AcquirerClient client) { this.client = client; }

    public Receipt charge(Order order) {
        return client.charge(order.total()); // xatti-harakat aynan o'sha
    }
}
```

Bu o'zgarishda mantiq bir qatorga ham tegilmadi. Faqat bog'lanish ko'chirildi. Shu turdagi qadam eng xavfsizi, chunki uni IDE avtomatik bajaradi va diff'ni o'qish oson.

### 34.5 Kichik qadamlar: har bir qadamdan keyin ishlaydigan tizim

Refaktoringning asosiy intizomi shu: har bir commit'dan keyin tizim deploy qilinishi mumkin bo'lsin. Bu "yarim ishlangan" holatni umuman yo'q qiladi. Agar qadam shunday bo'lishi mumkin bo'lmasa, qadam juda katta.

Katta o'zgarishni kichiklarga bo'lish uchun asosiy vosita feature flag va parallel ishlash. Yangi kod yoziladi, lekin dastlab u faqat soya rejimida ishlaydi: natijasini hisoblaydi, log'ga yozadi, lekin javob eski koddan qaytadi.

```java
@Service
public class FeeCalculationFacade {
    private final LegacyFeeCalculator legacy;
    private final NewFeeCalculator fresh;
    private final boolean shadow;      // soya rejimi yoqilganmi
    private final boolean useNew;      // javob qaysi koddan qaytadi

    public Money fee(Order order) {
        Money old = legacy.fee(order);
        if (shadow) {
            try {
                Money neu = fresh.fee(order);
                if (!neu.equals(old)) {
                    log.warn("fee farqi order={} eski={} yangi={}",
                             order.id(), old, neu); // farqlar metrikaga ham chiqadi
                }
                if (useNew) return neu;
            } catch (RuntimeException e) {
                log.error("yangi hisob xato berdi, eski javob qaytadi", e);
            }
        }
        return old;
    }
}
```

Soya rejimini bir hafta ishlatib, farqlar soni nolga tushganda `useNew` yoqiladi. Bu yerda muhim detal: yangi kodning exception'i mijozga chiqmasligi kerak, aks holda soya rejimi o'zi incident manbasiga aylanadi.

| Qadam | Hajm | Deploy mumkinmi | Qaytarish narxi |
|---|---|---|---|
| Interface ajratish | 1-2 fayl | Ha | Revert, 1 daqiqa |
| Metodni ko'chirish | 2-4 fayl | Ha | Revert, 1 daqiqa |
| Soya rejimi qo'shish | 3-5 fayl | Ha | Flag o'chirish, 0 daqiqa |
| Trafikni yangiga o'tkazish | 0 fayl | Ha | Flag o'chirish, 0 daqiqa |
| Eski kodni o'chirish | 5-20 fayl | Ha | Revert, 5 daqiqa |
| Jadvalni ikkiga bo'lish | migratsiya | Shartli | Backfill qayta, soatlar |
| Butun modulni qayta yozish | 100+ fayl | Yo'q | Amalda imkonsiz |

### 34.6 Katta qayta yozish nega deyarli har doim muvaffaqiyatsiz bo'ladi

Noldan qayta yozish uch sababdan qulaydi. Birinchisi, eski tizim turib qolmaydi. Siz 9 oy yangi versiyani yozganda, eski tizimga yana 300 ta o'zgarish kiradi va maqsad harakatlanadi.

Ikkinchi sabab bilimning taqsimlanishi. Legacy kodning qiymati arxitekturasida emas, o'n yil davomida yig'ilgan mayda shartlarida. Ular hujjatlashtirilmagan. Qayta yozishda ularning 10-20 foizi yo'qoladi va har biri alohida incident bo'lib qaytadi.

Uchinchi sabab iqtisodiy: qayta yozish davomida biznes qiymat olmaydi. 6 oydan keyin yangi funksiya so'rovi kelganda jamoa ikki joyda ishlashga majbur bo'ladi va ikkalasi ham sekinlashadi.

Qayta yozish asosli bo'lgan kam holatlar bor: platforma umuman qo'llab-quvvatlanmaydi, masalan Java 6 va EJB 2 ustidagi tizim; yoki modul juda kichik va chiqish nuqtalari aniq, masalan bitta hisobot generatori. Ikkinchi holatda bu qayta yozish emas, modul almashtirish.

### 34.7 Bo'g'uvchi anjir (strangler) usuli bilan bosqichma-bosqich almashtirish

Strangler yondashuvining mohiyati: yangi tizim eski tizim atrofida o'sadi va trafikni asta-sekin o'ziga tortadi. Eski tizim bitta katta kunda o'chirilmaydi, u funksiya ortidan funksiya bo'shab, oxirida bo'sh qobiq bo'lib qoladi.

Texnik asosi routing qatlami. Spring Cloud Gateway yoki oddiy nginx yetarli. Qoida yo'l bo'yicha emas, imkon qadar mijoz segmenti bo'yicha ham yozilsin, shunda yangi kod avval kichik trafikni ko'radi.

```yaml
# Gateway: /api/v1/payments faqat belgilangan header bilan yangi servisga ketadi
spring:
  cloud:
    gateway:
      routes:
        - id: payments-new
          uri: http://payment-service:8080
          predicates:
            - Path=/api/v1/payments/**
            - Header=X-Canary, true        # boshida 1-5% trafik
          filters:
            - name: CircuitBreaker
              args:
                name: paymentsCb
                fallbackUri: forward:/legacy/payments  # xato bo'lsa eskiga qaytadi
        - id: payments-legacy
          uri: http://monolith:8080
          predicates:
            - Path=/api/v1/payments/**     # qolgan hamma trafik
```

Trafikni bosqichlab oshirish tartibi odatda shunday: 1 foiz bir kun, 5 foiz uch kun, 25 foiz bir hafta, 50 foiz bir hafta, 100 foiz. Har bosqichda error rate va p99 latency taqqoslanadi. Oldingi bosqichga qaytish bitta konfiguratsiya o'zgarishi bo'lib qolishi shart.

### 34.8 Ma'lumotlar bazasini ajratish: eng qiyin qism va uning tartibi

Kodni bo'lish oson, bazani bo'lish qiyin. Sababi aniq: monolitda `orders` va `payments` jadvallari bitta tranzaksiyada yangilanadi va bitta `JOIN` bilan o'qiladi. Ajratilgandan keyin ikkalasi ham yo'qoladi.

To'g'ri tartib quyidagicha. Avval kod darajasida ajratish: har bir jadvalga faqat bitta modul yozsin, boshqalar API orqali so'rasin. Keyin `JOIN`'larni yo'qotish. Keyin schema'ni ajratish, lekin bazani bitta qoldirish. Va faqat oxirida alohida baza instance'i.

```sql
-- 1-qadam: mantiqiy ajratish, baza hali bitta
CREATE SCHEMA payment;
ALTER TABLE public.payments SET SCHEMA payment;

-- 2-qadam: faqat payment moduli yozish huquqiga ega bo'ladi
REVOKE INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA payment FROM monolith_app;
GRANT  SELECT ON payment.payments TO monolith_app;  -- vaqtinchalik o'qish

-- 3-qadam: o'qish ham API orqali bo'lganda ruxsat umuman olinadi
REVOKE SELECT ON payment.payments FROM monolith_app;
```

Tranzaksiya chegarasi buzilgan joyda ikkita yozishni bitta `@Transactional` ushlab turolmaydi. Bu yerda outbox orqali ishonchli xabar yuborish kerak bo'ladi, mexanikasi dizayn patternlar hujjatidagi outbox pattern bo'limida bor. Arxitektorning qarori esa boshqa: qaysi joy eventual consistency'ga chidaydi. To'lov holati va buyurtma holati orasida 2-5 sekund kechikish odatda qabul qilinadi, pul qoldig'i va yechib olish orasida esa yo'q.

| Tuzoq | Natijasi | Yechim |
|---|---|---|
| Bazani avval ajratib, keyin kodni bo'lish | Ikki baza orasida distributed JOIN | Avval kod, keyin schema, oxirida instance |
| Backfill'ni bir marta katta `UPDATE` bilan qilish | Jadval lock, soatlab kutish | 5-10 ming qatorli batch, har batchdan keyin commit |
| Ikki tomonga yozib, hech qachon tekshirmaslik | Jim ketadigan ma'lumot tafovuti | Har kecha hisoblash: farq soni metrikaga chiqsin |
| Eski ustunni darhol `DROP` qilish | Rollback imkonsiz | Avval ishlatishni to'xtatish, 2 sprint kutish, keyin drop |
| Yangi kodda eski jadvalga to'g'ridan-to'g'ri yozish | Egalik chegarasi buzildi | Baza darajasida `REVOKE`, qoida kodga tayanmasin |
| `Flyway` migratsiyasini orqaga qaytarishga umid qilish | Qaytarish skripti sinovdan o'tmagan | Faqat oldinga mos migratsiya: ustun qo'shish, to'ldirish, o'tish |
| Soya rejimini ikki hafta ortiq ushlab turish | Ikki marta xarajat, chalkashlik | Flag uchun muddat belgilansin, muddatdan keyin yoki o'ting yoki qaytaring |

### 34.9 Refaktoringni biznes bilan kelishish: qiymat tilida tushuntirish

"Kod iflos" degan dalil byudjet ochmaydi. Ochadigan dalil vaqt va xavf tilida yoziladi. Masalan: "to'lov modulidagi har bir o'zgarish hozir 9 kun oladi, shundan 5 kuni qo'lda regressiya tekshiruvi. Chok ajratilgandan keyin bu 3 kunga tushadi. Yiliga 20 ta o'zgarish bo'lsa, 120 ish kuni tejaladi."

Ikkinchi ishonchli dalil incident statistikasi. Agar oxirgi 12 oyda production incident'larning 40 foizi bitta modulda bo'lgan bo'lsa, bu modul refaktoringi xavfni kamaytirish loyihasi sifatida tushuntiriladi.

Kelishuvning amaliy shakli: alohida "refaktoring sprint'i" so'ralmaydi. Har sprintning 15-20 foizi tizimni ishlashga yaroqli saqlashga ajratiladi va bu doimiy bo'ladi. Bitta katta so'rov bir marta rad etiladi, kichik doimiy ulush esa odatga aylanadi.

| Oddiy yondashuv | Arxitektor yondashuvi |
|---|---|
| "Bu kod juda yomon, qayta yozamiz" | "Bu modul o'zgarish narxini 3 barobar oshiradi, bosqichma-bosqich almashtiramiz" |
| Refaktoringni mantiq o'zgarishi bilan birga commit qiladi | Xatti-harakat o'zgarmaydigan commit va mantiq commit'i ajratiladi |
| Avval tozalaydi, keyin o'lchaydi | Avval o'lchaydi, keyin faqat o'lchov ko'rsatgan joyni tozalaydi |
| Butun kod bazasini bir xil darajada yaxshilaydi | Yuqori churn joyga kuch beradi, tinch joyga tegmaydi |
| Bazani birinchi bo'lib bo'ladi | Kodni va egalikni birinchi bo'lib bo'ladi, baza oxirida |
| Yangi kodni darhol production javobiga qo'yadi | Soya rejimida taqqoslaydi, farq nolga tushgach o'tadi |
| Flag'larni cheksiz qoldiradi | Har flag uchun o'chirish muddati va egasi bo'ladi |
| "Yaxshilandi" deb his bilan aytadi | p99 latency, o'zgarish vaqti, incident soni raqamini ko'rsatadi |
| Eski kodni "ehtimol kerak bo'ladi" deb saqlaydi | Trafik nolga tushganini metrikada ko'rib, o'chiradi |

### 34.10 O'lchov: refaktoring ishladimi yoki yo'qligini qanday bilish

Refaktoring natijasi kod chiroyliligi bilan o'lchanmaydi. To'rt turdagi raqam ishlaydi: tezlik, xavf, ish narxi va ishlash ko'rsatkichi.

Ish narxi tomonidan eng oddiy ko'rsatkich lead time: PR ochilishidan production'ga chiqishigacha o'tgan vaqt. Refaktoringdan oldin 6-9 kun bo'lsa, keyin 2-3 kunga tushishi kutiladi. Ikkinchi ko'rsatkich change failure rate: deploy'lardan qanchasi rollback bilan tugaydi.

```bash
# Modul bo'yicha o'zgarish zichligi: refaktoringdan oldin va keyin taqqoslanadi
git log --since="6 months ago" --name-only --pretty=format: \
  | grep '^src/main/java/com/shop/payment/' | sort -u | wc -l

# Modulga tegadigan commit'lar soni va o'rtacha diff hajmi
git log --since="6 months ago" --numstat --pretty='C' -- src/main/java/com/shop/payment/ \
  | awk '/^C/{c++} /^[0-9]/{a+=$1; d+=$2} END{printf "commit=%d +%d -%d ortacha=%.1f\n", c, a, d, (a+d)/c}'
```

Ishlash tomonidan `http.server.requests` p99 va baza so'rovlari soni kuzatiladi. Keng tarqalgan hodisa: kod toza, lekin N+1 so'rov paydo bo'lgan va p99 ikki barobar o'sgan. Shuning uchun har bosqichda so'rov soni ham o'lchanadi.

Kod sifati metrikalaridan faqat ikkitasi foydali: modullar orasidagi bog'liqlik yo'nalishi va aylanma bog'liqliklar soni. Ikkisini ham ArchUnit qoidalari bilan qulflash mumkin, batafsili testlash qo'llanmasidagi arxitektura qoidalari bo'limida.

### 34.11 Qachon tegmaslik kerak: ishlayotgan, o'zgarmaydigan kod

Refaktoring qilmaslik ham qaror. Agar modul oxirgi 18 oyda o'zgarmagan, incident bermagan va performance muammosi yo'q bo'lsa, uning ichidagi kod qanday ko'rinishi ahamiyatsiz. Uni tozalash sof xarajat va yangi xato manbasi.

Tegmaslik mezonlari aniq: past churn, nol incident, latency byudjet ichida, yaqin yo'l xaritasida o'zgarish yo'q. Shu to'rt shart bajarilsa, modul "muzlatilgan" deb belgilanadi va faqat xavfsizlik yangilanishlari oladi.

Alohida holat: kod yomon, lekin uni o'rab olish mumkin. Masalan 3000 qatorli hisobot generatori. Uni qayta yozish o'rniga oldiga toza interface qo'yiladi, atrofidagi kod shu interface'ga tayanadi, ichi esa qora quti bo'lib qoladi. Shunda kelgusida uni almashtirish kerak bo'lsa, faqat bitta interface implementatsiyasi yoziladi.

### 34.12 Bosqichma-bosqich reja namunasi: to'lov moduli misolida

Quyidagi reja monolitdagi to'lov modulini alohida servisga chiqarish uchun real ketma-ketlik. Har bosqich oxirida tizim ishlaydi va orqaga qaytish yo'li bor.

Birinchi bosqich, bir hafta: o'lchov. To'lov bilan bog'liq endpoint'lar, Kafka listener'lar va `@Scheduled` job'lar ro'yxati; `payments` jadvaliga kim yozayotganini `grep` va baza grant'lari bo'yicha aniqlash; p99 va kunlik hajm raqamlari.

Ikkinchi bosqich, ikki hafta: characterization testlar. Production'dan olingan 500 ta to'lov holati uchun hozirgi natija qayd etiladi, shu qatorda rad etilgan va qaytarilgan to'lovlar.

Uchinchi bosqich, ikki hafta: modul chegarasini monolit ichida chizish. Barcha to'lov mantiqi bitta paketga ko'chiriladi, tashqi kod faqat `PaymentFacade` orqali murojaat qiladi, bazaga to'g'ridan-to'g'ri murojaatlar yo'qotiladi.

```java
// Modul chegarasi: tashqi dunyo faqat shu interface'ni ko'radi
public interface PaymentFacade {
    PaymentResult authorize(OrderId orderId, Money amount);
    void capture(PaymentId paymentId);
    void refund(PaymentId paymentId, Money amount, String reason);
    Optional<PaymentView> find(PaymentId paymentId);
}
// ArchUnit qoidasi: payment.internal paketiga tashqaridan murojaat taqiqlanadi.
// Shu qoida buzilmasa, keyingi bosqichda servisga chiqarish mexanik ish bo'ladi.
```

To'rtinchi bosqich, bir hafta: schema ajratish va grant'lar. Beshinchi bosqich, uch hafta: yangi servis ko'tariladi, `PaymentFacade` implementatsiyasi HTTP client bo'ladi, soya rejimida ishlaydi. Oltinchi bosqich, ikki hafta: canary 1 foizdan 100 foizga. Yettinchi bosqich, bir hafta: monolitdagi eski kod va grant'lar o'chiriladi.

Jami taxminan 12-14 hafta, bitta kichik jamoa uchun. Muhimi muddat emas, balki har bosqich oxirida tizim ishlashi va rollback bitta flag yoki bitta revert bo'lib qolishi.

### 34.13 Amalda qo'llash

- [ ] `git log --name-only` asosida oxirgi 2 yilda eng ko'p o'zgargan 30 faylni chiqarib, ularning hajmi bilan jadval tuzing va refaktoring nomzodlarini belgilang.
- [ ] `pg_stat_user_tables` va `pg_stat_statements` bo'yicha eng og'ir 20 so'rovni va ishlatilmayotgan index'larni yozib oling, bu refaktoringdan oldingi asos bo'ladi.
- [ ] Tanlangan modulning 3 ta eng muhim stsenariysi uchun production ma'lumotidan characterization qayd fayli tayyorlang.
- [ ] Modulda `new` operatori yoki `static` chaqiruv bilan qotib qolgan 5 ta bog'lanishni toping va ularning o'rniga interface seam qo'ying, mantiqga tegmasdan.
- [ ] Bitta hisoblash mantiqi uchun soya rejimi yoqing: yangi kod natijasi log va metrikaga chiqsin, javob eski koddan qaytsin.
- [ ] Har bir feature flag uchun egasi va o'chirish muddatini yozib qo'ying, muddati o'tgan flag'lar ro'yxati sprint ko'rikida ko'rilsin.
- [ ] `REVOKE` va `GRANT` orqali tanlangan jadvalga yozish huquqini faqat bitta modulga qoldiring, qoidani kodga emas bazaga tayantiring.
- [ ] Refaktoringdan oldin va 3 oydan keyingi lead time, change failure rate va p99 latency raqamlarini bir sahifada taqqoslab, biznes bilan shu hujjat tilida gaplashing.

## 35. Incident, on-call va post-mortem (Incidents and Post-mortems)

Incident vaqtida arxitektorning qiymati kod yozishda emas, qarorni tez va to'g'ri chiqarishda ko'rinadi. Tizimni bilgan odam "nega buzildi" savolidan oldin "qanday tiklanadi" savoliga javob beradi. Bu bob darajalash, rollar, tiklash usullari, diagnostika tartibi va ayblamaydigan post-mortem mexanikasini beradi. Oxirida to'lov servisi uzilishi misolida to'liq shablon bor.

### 35.1 Incident darajalari va ularni belgilash mezoni

Daraja texnik emas, biznes ta'siriga qarab belgilanadi. "PostgreSQL replica ortda qoldi" daraja emas, "mijoz to'lovni yakunlay olmaydi" daraja. Mezon uch o'lchovdan tuziladi: qancha foydalanuvchi zarar ko'rdi, pul yoki ma'lumot yo'qolayaptimi, vaqtinchalik yechim bormi. Darajani birinchi javob beruvchi qo'yadi va oshirishga haqli, pasaytirishga esa faqat boshqaruvchi haqli.

Amalda to'rt daraja yetarli. P1: asosiy oqim ishlamaydi yoki pul yo'qolmoqda, javob 5 daqiqa, telefon bilan uyg'otish. P2: oqim qisman ishlaydi yoki jiddiy sekinlashgan, javob 15 daqiqa. P3: ikkilamchi funksiya buzilgan, ish vaqtida hal qilinadi. P4: kosmetik muammo, backlog'ga tushadi. Raqamlar yozib qo'yiladi, aks holda har kim o'z hissi bilan baholaydi.

Darajalash mezoni SLO bilan bog'lanadi. 99.9% availability bir oyda taxminan 43 daqiqa budjet beradi, 99.95% esa taxminan 22 daqiqa. Bitta P1 shu budjetning yarmini yeb qo'ysa, post-mortem majburiy. Budjet tugagan oyda yangi feature chiqarish to'xtatiladi.

### 35.2 Incident paytidagi rollar: boshqaruvchi, tekshiruvchi, aloqachi

Eng ko'p uchraydigan xato: sakkiz injener bir xil log'ni o'qiydi va hech kim qaror qabul qilmaydi. Shuning uchun P1 ochilishi bilan uch rol ovoz chiqarib e'lon qilinadi. Incident boshqaruvchi qaror chiqaradi va ishni taqsimlaydi, o'zi debug qilmaydi. Tekshiruvchi gipotezani sinaydi va o'zgarish kiritadi. Aloqachi ichki va tashqi xabarni yozadi, status page'ni yangilaydi.

Boshqaruvchi klaviaturaga tegmasligi qoida. Uning vazifasi har 10 daqiqada "hozir qanday holat, keyingi qadam nima, kim bajaradi" deb so'rash. Kichik jamoada bitta odam boshqaruvchi va aloqachi bo'lishi mumkin, lekin boshqaruvchi va tekshiruvchi hech qachon bitta odam bo'lmasin.

Rol topshirish ham oshkora bo'ladi: kim kimga nimani topshirgani kanalga yoziladi. Uzoq incidentda har 4 soatda almashish rejalashtiriladi, chunki charchagan odam xato qaror chiqaradi. Eskalatsiya zanjiri oldindan yozilgan bo'ladi: birinchi javob beruvchi, zaxira, so'ngra ma'lumotlar bazasi yoki tarmoq mutaxassisi.

### 35.3 Birinchi qadam: tiklash, sabab qidirish emas

Incident paytida maqsad bitta: ta'sirni to'xtatish. Sababni topish post-mortem ishi. Bu ikkisini aralashtirish eng qimmat xato, chunki sabab izlash daqiqalar emas, soatlar oladi. Oxirgi deploy'dan keyin xato chiqqan bo'lsa, deploy qaytariladi, sabab esa sovuq boshda o'rganiladi.

Bitta istisno bor: tiklash harakati ma'lumotni buzishi mumkin bo'lsa, oldin tushunish kerak. To'lov servisi ikki marta debet qilayotgan bo'lsa, qayta ishga tushirish muammoni yashiradi va buzilgan yozuv qoladi. Bunday holatda birinchi qadam trafikni to'xtatish.

Tartib shunday: ta'sirni cheklash, qaytarish yoki o'chirish, metrika bilan tasdiqlash, keyin tahlil. "Tuzatdim" degan ishonch metrikasiz hech narsa anglatmaydi.

### 35.4 Tiklash usullari: orqaga qaytarish, flag o'chirish, trafikni yo'naltirish

Eng tez tiklash usuli eng kam fikrlash talab qiladigani. Deploy'ni qaytarish tekshirilgan yo'l, shuning uchun birinchi variant. Shart bitta: migratsiya orqaga mos bo'lsin. Yangi versiya ustunni o'chirgan bo'lsa qaytarish ishlamaydi, shuning uchun migratsiya har doim ikki fazaga bo'linadi.

```bash
# Qaysi versiya qachon chiqqanini ko'rish
kubectl rollout history deployment/payment-service -n prod

# Oldingi versiyaga qaytarish, bu eng tez va eng xavfsiz qadam
kubectl rollout undo deployment/payment-service -n prod

# Qaytarish tugashini kuzatish, 120 sekund ichida tugamasa muammo boshqa joyda
kubectl rollout status deployment/payment-service -n prod --timeout=120s

# Ikki versiya orasidagi farqni olish, diagnostika uchun
git log --oneline v2.14.0..v2.15.0 -- src/main/java/com/shop/payment
```

Ikkinchi usul feature flag o'chirish. Flag qaytarishdan tezroq, chunki pod qayta ishga tushmaydi va effekt bir necha sekundda ko'rinadi. Shuning uchun har xavfli o'zgarish flag ostida chiqariladi, flag holati esa tashqi konfiguratsiyadan o'qiladi.

```java
// To'lov yo'nalishini tanlash: flag o'chsa eski, tekshirilgan yo'lga qaytadi.
// Flag qiymati konfiguratsiya serveridan keladi, pod qayta ishga tushmaydi.
@Service
class PaymentRouter {
    private final FeatureFlags flags;
    private final NewGatewayClient newGateway;
    private final LegacyGatewayClient legacyGateway;

    PaymentResult charge(PaymentCommand cmd) {
        // Kill switch: incident paytida birinchi bosiladigan tugma
        if (!flags.enabled("payment.new-gateway")) {
            return legacyGateway.charge(cmd);
        }
        try {
            return newGateway.charge(cmd);
        } catch (GatewayTimeoutException e) {
            // Idempotency key bor, shuning uchun qayta urinish ikki marta debet qilmaydi
            log.warn("yangi gateway timeout, eski yo'lga o'tildi, orderId={}", cmd.orderId());
            return legacyGateway.charge(cmd);
        }
    }
}
```

Uchinchi usul trafikni yo'naltirish. Bitta instansiya buzilsa, uni load balancer'dan chiqarish yetarli, region buzilsa trafik ikkinchi regionga o'tadi. Bu usul faqat oldindan tayyorlangan bo'lsa ishlaydi. Readiness probe shu usulning asosi: pod o'zini "tayyor emas" deb belgilasa, trafik avtomatik boshqa podga ketadi.

### 35.5 Diagnostika tartibi: nima o'zgardi, qachon boshlandi, nima umumiy

Diagnostika uchta savoldan boshlanadi. Birinchi: nima o'zgardi. Incidentlarning katta qismi o'zgarishdan keladi, ya'ni deploy, konfiguratsiya, migratsiya, sertifikat, flag yoki tashqi provayder yangilanishi. Ikkinchi: qachon boshlandi, chunki aniq daqiqa o'zgarish ro'yxatini filtrlaydi. Uchinchi: nima umumiy.

```sql
-- Qachon boshlandi: aktiv so'rovlar va ular nimani kutayotgani
SELECT pid, state, wait_event_type, wait_event,
       now() - query_start AS davomiyligi,
       left(query, 80) AS sorov
FROM pg_stat_activity
WHERE state <> 'idle' AND now() - query_start > interval '5 seconds'
ORDER BY davomiyligi DESC
LIMIT 20;

-- Nima umumiy: eng ko'p vaqt yeyayotgan so'rov shakllari
-- pg_stat_statements kerak, PostgreSQL 15-17 da mean_exec_time millisekundda
SELECT calls, round(mean_exec_time::numeric, 1) AS ortacha_ms,
       round(total_exec_time::numeric / 1000, 1) AS jami_sek,
       left(query, 70) AS sorov
FROM pg_stat_statements
ORDER BY total_exec_time DESC
LIMIT 10;

-- Kim kimni bloklayapti: lock zanjirining boshi
SELECT blocked.pid AS bloklangan, blocking.pid AS bloklovchi,
       left(blocked.query, 60) AS bloklangan_sorov
FROM pg_stat_activity blocked
JOIN pg_stat_activity blocking ON blocking.pid = ANY(pg_blocking_pids(blocked.pid))
WHERE cardinality(pg_blocking_pids(blocked.pid)) > 0;
```

"Nima umumiy" savoliga javob o'lchovlar bo'yicha kesish bilan topiladi: endpoint, mijoz turi, region, pod, tenant, ma'lumot shakli. Xato bitta podda bo'lsa, bu konfiguratsiya yoki resurs muammosi. Barcha podda bir vaqtda boshlangan bo'lsa, bu umumiy bog'liqlik: ma'lumotlar bazasi, cache, tashqi API yoki tarmoq.

| Tuzoq | Nega yuzaga keladi | Yechim |
|---|---|---|
| Birinchi topilgan gipotezaga yopishib qolish | Vaqt tig'iz, miya tasdiq izlaydi | Ikki gipotezani yozib, ikkisini ham tekshirish |
| Bir vaqtda uchta o'zgarish kiritish | Har kim o'z fikrini sinaydi | Faqat boshqaruvchi ruxsat bergan bitta o'zgarish |
| Pod qayta ishga tushirish bilan "tuzatish" | Simptom yo'qoladi | Avval heap dump va thread dump olinadi |
| Log'ni grep bilan qidirish | Markazlashgan log yo'q | Trace id bo'yicha so'rovni uchidan uchiga kuzatish |
| Metrikasiz tasdiqlash | Panel yo'q yoki noto'g'ri | Tiklanishni mijoz tomonidagi metrika bilan tasdiqlash |
| Connection pool o'lchamini oshirish | "Pool tugadi" xabari ko'rinadi | Sekin so'rovni topish, pool PostgreSQL ni bo'g'adi |
| Timeout ni cheksiz qilish | Xato yo'qolgandek bo'ladi | Timeout qisqa, qayta urinish budjetli |
| Incidentni erta yopish | Metrika tiklandi, sabab qolgan | 30 daqiqa kuzatuv, keyin yopish |

### 35.6 Muloqot: kimga, qanchalik tez-tez, qanday til bilan

Muloqot ikki yo'nalishli. Ichki kanal injenerlar uchun: texnik, qisqa, gipoteza va natija bilan. Tashqi xabar mijoz uchun: atamasiz, ta'sir va keyingi yangilanish vaqti bilan. Mijozga "connection pool exhausted" deb yozish hech narsa anglatmaydi.

Ritm oldindan belgilanadi. P1 da tashqi yangilanish har 30 daqiqada, ichki holat har 10 daqiqada. Yangi ma'lumot bo'lmasa ham xabar yuboriladi: "tekshirmoqdamiz, keyingi xabar 14:30 da", chunki sukunat eng katta ishonchsizlik beradi. Tashqi xabarda uch element bor: nima ishlamayapti, kim zarar ko'rgan, keyingi yangilanish qachon. Sabab va aybdor yozilmaydi, chunki incident paytidagi taxmin keyin noto'g'ri chiqadi.

Til qoidasi sodda: faktni gipotezadan ajratib yozish. "Error rate 14:05 da 0.2 dan 38 foizga chiqdi" fakt, "menimcha yangi gateway sabab" gipoteza. Ular aralashsa, keyin qo'shilgan odam gipotezani fakt deb o'qiydi.

### 35.7 Incident jurnali va vaqt chizig'ini yozib borish

Vaqt chizig'i incident tugagandan keyin tiklanmaydi, uni real vaqtda yozish kerak. Eng arzon usul: har qaror va o'zgarish kanalga vaqt bilan yoziladi, aloqachi esa oxirida shu kanalni vaqt chizig'iga aylantiradi. Yozuv formati bir xil: vaqt, kim, nima qildi.

Log'da bog'lovchi identifikator bo'lishi shart. Incident id ni MDC ga qo'yish arzon va bitta filtr bilan barcha tegishli yozuvni beradi.

```java
// Incident paytida qo'lda ishga tushirilgan tiklash operatsiyalarini belgilash.
// MDC qiymati Logback pattern'ida %X{incidentId} bilan chiqadi.
public final class IncidentContext {
    private static final String KEY = "incidentId";

    public static <T> T runTagged(String incidentId, Supplier<T> action) {
        MDC.put(KEY, incidentId);
        long boshlandi = System.nanoTime();
        try {
            return action.get();
        } finally {
            // Operatsiya qancha davom etganini vaqt chizig'i uchun yozamiz
            long msek = (System.nanoTime() - boshlandi) / 1_000_000;
            log.info("tiklash operatsiyasi tugadi, davomiyligi={}ms", msek);
            MDC.remove(KEY);
        }
    }
}
```

Vaqt chizig'ida besh nuqta majburiy: muammo boshlanishi, birinchi signal, odam xabardor bo'lishi, birinchi tiklash harakati, to'liq tiklanish. Ular ikki raqamni beradi: aniqlash vaqti va tiklash vaqti. Aniqlash uzun bo'lsa muammo monitoringda, tiklash uzun bo'lsa runbook va avtomatlashtirishda.

### 35.8 Ayblamaydigan post-mortem: tuzilishi va yozish qoidalari

Ayblamaydigan post-mortem odamni emas, tizimni tekshiradi. Bu yumshoqlik emas, aniqlik talabi: jazolanishini bilgan injener faktni yashiradi. Shuning uchun "falonchi noto'g'ri konfiguratsiya qo'ydi" o'rniga "konfiguratsiya qiymati validatsiyasiz deploy qilindi, CI da uni tekshiradigan qadam yo'q edi" deb yoziladi.

Tuzilish barqaror bo'lsa o'qish tez bo'ladi: qisqa xulosa, ta'sir raqamlarda, vaqt chizig'i, sabab tahlili, nega tezroq aniqlanmadi, nega tezroq tiklanmadi, nima yaxshi ishladi, harakat bandlari. Oxirgidan oldingi bo'lim bejiz emas: ishlagan himoyani bilish uni kesib tashlashdan saqlaydi.

Yozish qoidalari qisqa. Ism sabab sifatida ko'rsatilmaydi, rol nomi yetarli. Taxmin "ehtimol" so'zi bilan belgilanadi. Hujjat 5 ish kuni ichida yoziladi. P1 uchun post-mortem majburiy, P2 uchun SLO budjetiga ta'siri bo'lsa majburiy.

| Mavzu | Oddiy yondashuv | Arxitektor yondashuvi |
|---|---|---|
| Incident darajasi | Xato turi bo'yicha | Biznes ta'siri va SLO budjeti bo'yicha |
| Birinchi harakat | Sababni izlash | Ta'sirni to'xtatish, keyin sabab |
| Rollar | Hamma debug qiladi | Boshqaruvchi, tekshiruvchi, aloqachi ajratilgan |
| Tiklash | Qo'lda tuzatish yoziladi | Qaytarish, flag, trafik yo'naltirish tayyor |
| Muloqot | Tugagandan keyin xabar | Belgilangan ritmda, ta'sir tilida |
| Post-mortem | Kim xato qildi | Qaysi himoya yo'q edi |
| Harakat bandlari | "Ehtiyot bo'lamiz" | Egasi, muddati, tekshiruv usuli bor |
| Alert | Ko'proq alert yaxshi | Har bir alert bajariladigan ish |
| On-call | Eng biladigan odam doim navbatda | Navbat aylanadi, runbook yoziladi |

### 35.9 Besh marta "nega" va tizimli sabablarga yetish

Birinchi topilgan sabab deyarli hech qachon haqiqiy sabab bo'lmaydi. Texnika oddiy: har javobdan keyin yana so'raysiz, toki javob tizim yoki jarayon haqida bo'lgunicha. Nega to'lov ishlamadi: servis gateway javobini 60 sekund kutdi. Nega kutdi: HTTP client timeout qo'yilmagan. Nega qo'yilmagan: client qo'lda yozilgan, markazlashgan builder ishlatilmagan. Nega ishlatilmagan: builder haqida hujjat va avtomatik qoida yo'q. Nega yo'q: bu kod review'ning og'zaki an'anasi edi.

Oxirgi javob harakatga aylanadi: og'zaki an'ana avtomatik qoidaga ko'chadi, chunki avtomatik qoida charchamaydi. Testlash qo'llanmasidagi arxitektura qoidalari bo'limi bunday tekshiruvni yozishni batafsil beradi.

Ikki tuzoq bor. Birinchisi, zanjirning odamga borib to'xtashi: "beparvo edi". Savol davom etishi kerak: nega beparvolik ishlab chiqarishga yetib bordi. Ikkinchisi, bitta zanjir bilan cheklanish. Jiddiy incidentda uch sabab birlashadi: xato kod, yetishmagan alert, mavjud bo'lmagan tiklash yo'li.

### 35.10 Harakat bandlari: egasi, muddati, tekshiruvi bo'lsin

Post-mortem qiymati harakat bandlarida. Bandga to'rt shart: aniq ish, bitta egasi, aniq muddat, tekshiruv usuli. "Monitoringni yaxshilash" band emas. "Gateway p99 latency uchun 2 sekund chegarada alert qo'shish, egasi platform jamoasi, muddat 14 oktabr, tekshiruv sun'iy sekinlashtirish bilan" band.

Bandlar ikki guruhga bo'linadi. Oldini olish bandlari sababga tegadi, masalan timeout ni majburiy qilish. Zararni kamaytirish bandlari tiklash vaqtini qisqartiradi, masalan kill switch qo'shish. Ikkinchi guruh ko'pincha e'tibordan qoladi, lekin aynan u keyingi incidentda qutqaradi.

```yaml
# Harakat bandi natijasi: majburiy timeout va alert chegarasi konfiguratsiyada
spring:
  datasource:
    hikari:
      maximum-pool-size: 20          # PostgreSQL max_connections 200, 6 instansiya
      connection-timeout: 2000       # pool bo'sh bo'lmasa 2 sekundda xato, kutmaydi
      validation-timeout: 1000
      leak-detection-threshold: 20000 # 20 sekund ushlab turilgan connection log'ga tushadi
  jpa:
    properties:
      jakarta.persistence.query.timeout: 3000  # sekin so'rov tranzaksiyani ushlamaydi

management:
  endpoint:
    health:
      show-details: when-authorized
  health:
    db:
      enabled: true
  endpoints:
    web:
      exposure:
        include: health,info,metrics,prometheus
```

Backlog'ga tushgan band yo'qoladi, shuning uchun bandlarga alohida belgi qo'yiladi va har hafta ko'rib chiqiladi. P1 bandlari 30 kun ichida bajariladi. Bajarilmagan band soni ishonchlilik qarzining eng halol metrikasi.

### 35.11 On-call navbati: adolatli taqsimot, ogohlantirish charchoqini kamaytirish

On-call tizim egaligining bir qismi, jazo emas. Uch qoida bor. Navbat aylanadi, bitta odam doimiy "qutqaruvchi" bo'lmaydi, chunki bu bilim monopoliyasi va charchoq beradi. Navbat kompensatsiya bilan bo'ladi. Navbatdagi odam o'sha hafta feature ishidan ozod, aks holda ikki ish ham sifatsiz chiqadi.

Navbatga kirish shartli: yangi odam oldin ikkilamchi navbatchi sifatida kuzatadi va runbook'ni o'qiydi. Runbook'da to'rt narsa bor: qaysi metrikaga qarash, qanday flag bor, qanday qaytarish, kimga eskalatsiya qilish. Runbook bo'lmasa navbat lotereyaga aylanadi.

Charchoqni kamaytirishning eng kuchli vositasi tungi alert sonini o'lchash. Haftada bir navbatchiga ikkitadan ko'p uyg'otish bo'lsa, bu monitoring muammosi. Shu raqam har hafta ko'rib chiqiladi va eng shovqinli alert tuzatiladi.

### 35.12 Ogohlantirishlar sifati: har bir alert bajariladigan ish bo'lsin

Alert bitta savolga javob berishi kerak: hozir odam nima qilishi kerak. Javob bo'lmasa, bu alert emas, dashboard elementi. Ikkinchi mezon: alert simptomga qo'yiladi, sababga emas. "CPU 90 foiz" ko'pincha muammo emas, "checkout error rate 5 foizdan oshdi" esa doim muammo.

```yaml
# Simptom asosidagi alert: mijoz ko'radigan xatolik ulushi
groups:
  - name: payment-slo
    rules:
      - alert: PaymentErrorRateHigh
        # 5 daqiqalik oynada xato ulushi 2 foizdan oshsa
        expr: |
          sum(rate(http_server_requests_seconds_count{uri="/api/payments",status=~"5.."}[5m]))
          / sum(rate(http_server_requests_seconds_count{uri="/api/payments"}[5m])) > 0.02
        for: 5m                      # qisqa tebranishda uyg'otmaydi
        labels:
          severity: page             # telefon bilan uyg'otish
          service: payment
        annotations:
          summary: "To'lov API xato ulushi 2 foizdan yuqori"
          impact: "Mijozlar to'lovni yakunlay olmaydi"
          action: "payment.new-gateway flag'ini o'chirish, keyin oxirgi deploy'ni qaytarish"
          runbook_url: "https://wiki.internal/runbook/payment-error-rate"
```

Har alertda runbook havolasi va birinchi harakat bo'ladi, chunki uyqudan uyg'ongan odam o'ylab emas, o'qib harakat qiladi. Alertlar har chorakda tozalanadi: 90 kunda bir marta ham to'g'ri ishga tushmagani o'chiriladi yoki chegarasi qayta hisoblanadi. Shovqinli alert haqiqiy alertni ham e'tiborsiz qoldirishga o'rgatadi.

### 35.13 To'liq post-mortem namunasi: to'lov servisi uzilishi misolida

Quyidagi shablonda real ko'rinishdagi namuna bor, uni nusxa olib har incidentda to'ldirish mumkin.

```markdown
# Post-mortem: <servis> <davomiylik> uzilishi

- Sana, daraja, boshqaruvchi, hujjat holati

## Qisqa xulosa
Uch gap: nima buzildi, nega ta'sir qildi, nima bilan tiklandi.

## Ta'sir
- Davomiyligi va aniq vaqt oralig'i
- Muvaffaqiyatsiz so'rov soni va zarar ko'rgan mijoz soni
- Ma'lumot yo'qolishi yoki buzilishi bo'ldimi
- SLO budjetining qancha ulushi sarflandi

## Vaqt chizig'i
Besh majburiy nuqta: boshlanish, birinchi signal, odam xabardor
bo'lishi, birinchi tiklash harakati, to'liq tiklanish.

## Sabab tahlili
Besh marta "nega" zanjiri, oxiri tizim yoki jarayonga borib tugaydi.

## Nega tezroq aniqlanmadi
## Nega tezroq tiklanmadi
## Nima yaxshi ishladi

## Harakat bandlari
| Ish | Tur | Egasi | Muddat | Tekshiruv |
|---|---|---|---|---|
```

Shablonning to'ldirilgan ko'rinishi quyidagicha.

```markdown
# Post-mortem: to'lov servisi 43 daqiqa uzilishi

Sana 2026-09-18, daraja P1, boshqaruvchi platform navbatchisi.

## Qisqa xulosa
Yangi gateway client'ida read timeout yo'q edi. Provayder sekinlashganda
Tomcat thread'lari band bo'ldi va /api/payments javob bermay qoldi.

## Ta'sir
- 14:07 dan 14:50 gacha, 43 daqiqa
- Taxminan 2 180 muvaffaqiyatsiz to'lov, taxminan 1 400 mijoz
- Ikki marta debet yo'q, idempotency key ishladi
- Oylik 99.9% budjetining taxminan 100 foizi sarflandi

## Vaqt chizig'i (UTC+5)
- 13:58 deploy, flag 10% trafikda; 14:07 p99 180ms dan 9s ga; 14:11 alert
- 14:29 thread dump: 198 thread socket read da kutmoqda
- 14:41 flag o'chirildi; 14:50 xato ulushi 0.1 foizga qaytdi

## Sabab tahlili
Client umumiy builder'siz tuzilgan, timeout qo'llanmagan. Izolyatsiya
yo'q edi, shuning uchun boshqa endpoint'lar ham ta'sirlandi.

## Harakat bandlari
| Ish | Tur | Egasi | Muddat | Tekshiruv |
|---|---|---|---|---|
| Client faqat umumiy builder'dan | oldini olish | payments | 02.10 | CI qoidasi |
| Gateway latency alert, 2s | aniqlash | platform | 25.09 | sekinlashtirish testi |
```

Shablonning qiymati tartibda: bir xil tuzilish o'qishni tezlashtiradi va bandlarni bir joyga yig'adi. Bir yilda yig'ilgan post-mortem'lar eng qimmat arxitektura hujjatiga aylanadi.

### 35.14 Amalda qo'llash

- [ ] Incident darajalari jadvalini yozing: har daraja uchun biznes mezoni, javob vaqti, uyg'otish usuli.
- [ ] Eng muhim uch servis uchun runbook yarating: metrika havolalari, flag nomlari, qaytarish buyrug'i, eskalatsiya ro'yxati.
- [ ] Har bir xavfli yangi yo'lni feature flag ostiga oling va flag'ni pod qayta ishga tushirmasdan o'chirib ko'ring.
- [ ] Oxirgi 90 kundagi alertlarni ko'rib chiqing, to'g'ri ishga tushmaganini o'chiring, qolganiga runbook havolasi va birinchi harakatni qo'shing.
- [ ] Barcha HTTP client va DB so'rovlariga timeout qo'yilganini tekshiradigan avtomatik qoida qo'shing.
- [ ] Post-mortem shablonini repoga joylashtiring va oxirgi P1 ni shu shablon bilan qayta yozib ko'ring.
- [ ] Tungi uyg'otish sonini har hafta o'lchang, 2 dan oshsa alertni tuzatish ishini oching va ochiq harakat bandlarini shu yig'ilishda ko'rib chiqing.

## 36. Code review va jamoada texnik yetakchilik (Code Review and Technical Leadership)

Code review arxitektorning eng arzon va eng ta'sirli vositasi. U kod birlashishdan oldin ishlaydi, shuning uchun bitta izoh keyinchalik haftalarcha ketadigan migratsiyani to'xtatishi mumkin. Lekin ko'p jamoada review bo'sh marosimga aylanadi: odamlar probel va o'zgaruvchi nomi haqida bahslashadi, tranzaksiya chegarasi va pul turini esa hech kim ko'rmaydi. Bu bob review ichida nimani qidirish kerakligini, izohni qanday yozishni va texnik yetakchi o'z vaqtini qanday taqsimlashini ko'rsatadi.

### 36.1 Code review nimani topishi kerak: xatti-harakat, chegara, nom, xavfsizlik

Review diqqati to'rtta narsaga qaratilishi kerak. Birinchisi xatti-harakat: kod aytilgan ishni qiladimi, chegara holatlarida nima bo'ladi, xato yo'lida qanday javob qaytadi. Ikkinchisi chegara: tranzaksiya qayerda ochiladi va yopiladi, tashqi HTTP chaqiruv tranzaksiya ichida qolib ketmaganmi, cache invalidatsiyasi commit dan keyin bo'ladimi. Uchinchisi nom: metod nomi uning yon ta'sirini yashirmayaptimi, domen atamasi kodda bir xil ishlatilayaptimi. To'rtinchisi xavfsizlik: autorizatsiya tekshiruvi qayerda, log ichiga karta raqami yoki token tushmayaptimi, SQL parametrlanganmi.

Eng ko'p uchraydigan muammo pul va vaqt bilan ishlashda. `double` bilan hisoblangan summa ikki yildan keyin hisobotda tiyin farqi beradi, va bu farqni topish bir hafta oladi.

```java
// REVIEW TOPISHI KERAK: pul double bilan, yaxlitlash qoidasi yo'q,
// tashqi chaqiruv tranzaksiya ichida, xatolik yutilgan.
@Transactional
public void charge(Long orderId, double amount) {
    Order order = orderRepository.findById(orderId).orElseThrow();
    double fee = amount * 0.029;              // komissiya suzuvchi nuqtada
    gatewayClient.charge(order.getCardToken(), amount + fee); // 3 sekund kutadi
    order.setStatus(PAID);
    log.info("to'lov: karta={} summa={}", order.getCardToken(), amount); // token logda
}
```

Shu o'n qatorda to'rtta alohida muammo bor va ularning har biri boshqa toifaga tegishli: hisob aniqligi, tranzaksiya chegarasi, kutish vaqti, maxfiy ma'lumot. Review izohi ham to'rtta alohida izoh bo'lishi kerak, chunki ularni bitta izohda aralashtirsang muallif faqat birinchisini tuzatadi.

```java
// TUZATILGAN: pul BigDecimal, gateway chaqiruvi tranzaksiyadan tashqarida,
// holat o'zgarishi alohida qisqa tranzaksiyada, logda faqat maskalangan qism.
public void charge(Long orderId, BigDecimal amount) {
    ChargeCommand cmd = orderService.prepareCharge(orderId, amount); // qisqa tranzaksiya
    GatewayResult result = gatewayClient.charge(cmd);                // tashqarida
    orderService.applyResult(orderId, result);                       // ikkinchi tranzaksiya
}

@Transactional
ChargeCommand prepareCharge(Long orderId, BigDecimal amount) {
    Order order = orderRepository.findByIdForUpdate(orderId).orElseThrow();
    BigDecimal fee = amount.multiply(FEE_RATE).setScale(2, RoundingMode.HALF_UP);
    order.markChargePending();
    return new ChargeCommand(order.maskedCard(), amount.add(fee), order.idempotencyKey());
}
```

### 36.2 Nimani topmasligi kerak: formatlash, uslub, mashina tekshiradigan narsalar

Odam review qilgan narsa qimmat turadi. Shuning uchun mashina topa oladigan hech narsani odam izohlamasligi kerak. Probel, qavs joyi, import tartibi, `final` qo'yish, satr uzunligi, ishlatilmagan o'zgaruvchi: bularning hammasi formatter va static analyzer ishi. Agar review da shunday izoh paydo bo'lsa, bu kod muammosi emas, pipeline muammosi. To'g'ri javob izoh yozish emas, qoidani CI ga ko'chirish.

```yaml
# .github/workflows/quality.yml - review ga kelgunga qadar ishlaydi
name: quality
on: [pull_request]
jobs:
  gate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-java@v4
        with:
          java-version: '21'
          distribution: 'temurin'
          cache: maven
      # formatlash: buzilsa build qizil bo'ladi, odam izoh yozmaydi
      - run: ./mvnw -B spotless:check
      # statik tahlil: null yo'li, resource yopilmagan, taxminiy xatolar
      - run: ./mvnw -B verify -Perrorprone,spotbugs
      # arxitektura qoidalari: qatlam buzilishi
      - run: ./mvnw -B test -Dtest='Arch*Test'
```

Shuningdek review da uslub ta'mi haqida bahs qilmaslik kerak. "Men bu yerda stream emas, for loop ni afzal ko'raman" degan izoh muallifning vaqtini oladi va hech narsani yaxshilamaydi. Agar ikkita variant o'qilish darajasida teng bo'lsa, muallif variantini qoldir.

| Vaziyat | Oddiy yondashuv | Arxitektor yondashuvi |
|---|---|---|
| Import tartibi buzilgan | Review da izoh yoziladi | Spotless CI da majburlaydi, izoh yo'q |
| 900 qatorli PR keldi | Bir hafta turadi, keyin "LGTM" | Muallif bilan 3 ta PR ga bo'linadi |
| Tranzaksiya ichida HTTP chaqiruv | Ko'rinmaydi, chunki diqqat uslubda | Birinchi navbatdagi majburiy izoh |
| Muallif bilan kelishmovchilik | Kim baland ovozda gapirsa, u yengadi | O'lchov yoki prototip dalil beradi |
| Yangi odam PR yuboradi | 30 ta mayda izoh, ruhi tushadi | 3 ta muhim izoh, qolgani birga suhbat |
| Arxitektura qarori qabul qilindi | Chatda aytiladi va yo'qoladi | ADR yoziladi, shablonda namuna kod paydo bo'ladi |
| Faqat bitta odam Kafka ni biladi | Hamma unga yo'naltiriladi | Bilim xaritasi, juftlik review, rotatsiya |
| Yetakchi hamma PR ni o'zi ko'radi | Navbat yetakchiga tiqiladi | Qoidalar avtomatlashtiriladi, review tarqatiladi |
| Review javob vaqti 2 kun | "Band edim" deyiladi | Kuniga ikki marta review oynasi belgilanadi |
| Hisobot query sekin ishlaydi | Keyin optimallashtiramiz deyiladi | PR da EXPLAIN natijasi talab qilinadi |

### 36.3 Izoh yozish uslubi: muammoni ko'rsat, qaror egasini qoldirib ket

Yaxshi izoh uchta qismdan iborat: nima ko'rdim, nega bu muhim, qaysi yo'nalishda o'ylash kerak. Yechimni buyruq shaklida yozmaslik kerak, chunki kodni muallif yozadi va kontekstni u yaxshi biladi. "Bu yerni ChangeStreamListener ga o'tkaz" degan izoh muallifni ijrochiga aylantiradi. "Bu listener commit dan oldin ishga tushadi, shuning uchun rollback bo'lsa cache eski emas, yangi qiymatni ushlab qoladi. Qanday hal qilsak yaxshi bo'ladi?" degan izoh muallifni o'ylashga majbur qiladi va u ko'pincha sendan yaxshiroq variant topadi.

Izohda nega ekanini ko'rsatish yagona eng muhim odat. "BigDecimal ishlat" o'rniga "to'lov summasi hisobotda tiyingacha mos kelishi kerak, suzuvchi nuqta uchta amaldan keyin farq beradi" deb yoz. Birinchi izoh bitta qatorni tuzatadi, ikkinchisi odamni o'zgartiradi va keyingi PR da shu muammo bo'lmaydi.

Savol shaklidagi izoh ikki tomonga ham xizmat qiladi. Agar sen xato qilgan bo'lsang, savol shakli sening obro'yingni saqlaydi. Agar muallif xato qilgan bo'lsa, savol unga o'zi topish imkonini beradi.

### 36.4 Majburiy va ixtiyoriy izohlarni ajratish

PR da yigirma izoh bo'lsa, muallif qaysi biri birlashishga to'sqinlik qilayotganini bilmaydi. Shuning uchun har bir izohga prefiks qo'yish kerak. Men to'rtta darajani ishlataman: `blocker` (bu holatda birlashtirmaymiz), `kerak` (birlashishdan oldin tuzatiladi), `fikr` (o'ylab ko'r, qaror senda), `maqtov` (yaxshi yechimni ko'rsatish). Oxirgisi bo'sh narsa emas: u review ni jazo mexanizmidan o'rgatish mexanizmiga aylantiradi.

| Prefiks | Ma'nosi | Misol |
|---|---|---|
| `blocker` | Ma'lumot yo'qoladi yoki xavfsizlik buzildi | Autorizatsiya tekshiruvi yo'q |
| `kerak` | Xatti-harakat yoki chegara noto'g'ri | Tranzaksiya ichida tashqi chaqiruv |
| `fikr` | Yaxshilash mumkin, qaror muallifda | Bu metodni ikkiga bo'lish mumkin |
| `maqtov` | Qayta ishlatilishi kerak bo'lgan yechim | Idempotency key dizayni yaxshi |

Agar PR da uchdan ko'p `blocker` bo'lsa, izoh yozishni to'xtat va 15 daqiqalik suhbat taklif qil. Ko'p blocker odatda noto'g'ri tushunilgan talab belgisi, va uni yozma izohlar bilan hal qilish bir necha kun oladi.

### 36.5 Review hajmi: katta o'zgarishni bo'lish va navbat vaqtini qisqartirish

Review sifati PR hajmiga teskari proportsional. Taxminan 200 qatordan keyin odam diqqati tushadi, 400 qatordan keyin review amalda faqat imzo bo'lib qoladi. Shuning uchun arxitektorning ishi review paytida boshlanmaydi, u PR tuzilishidan boshlanadi. Katta o'zgarishni uchta tabiiy qatlamga bo'lish mumkin: birinchi PR da yangi interfeys va migratsiya skripti, ikkinchisida implementatsiya, uchinchisida eski yo'lni o'chirish.

```bash
# Katta branch ni ketma-ket PR larga bo'lish
git switch -c refactor/payment-base main
git cherry-pick <migratsiya-commit> <interfeys-commit>   # 1-PR: skelet
git push -u origin refactor/payment-base

git switch -c refactor/payment-impl refactor/payment-base
git cherry-pick <implementatsiya-commitlari>             # 2-PR: mantiq
git push -u origin refactor/payment-impl

# Review navbat vaqtini o'lchash: ochilishdan birinchi izohgacha
gh pr list --state merged --limit 50 \
  --json number,createdAt,mergedAt,additions \
  | jq -r '.[] | [.number, .additions,
      ((.mergedAt|fromdate) - (.createdAt|fromdate))/3600 | floor] | @tsv'
```

Navbat vaqti review ning yashirin narxi. Agar PR ikki kun kutsa, muallif boshqa ishga o'tadi va kontekstni yo'qotadi, qaytib kelganda tuzatish uch barobar qimmat. Kuniga ikki marta belgilangan review oynasi (masalan ertalab va tushdan keyin) navbatni odatda bir necha soatga tushiradi. 200 qatorlik PR uchun maqsad: birinchi javob 4 soat ichida.

### 36.6 Kelishmovchilikni hal qilish: dalil, prototip, uchinchi fikr

Texnik bahsning aksariyati fakt yetishmasligidan emas, bir xil faktni turlicha o'lchashdan kelib chiqadi. Birinchi qadam bahsni o'lchanadigan savolga aylantirish. "Bu query sekin" degan fikr bahsga olib keladi, `EXPLAIN (ANALYZE, BUFFERS)` natijasi bahsni tugatadi.

```sql
-- Bahsni tugatadigan dalil: rejani va haqiqiy vaqtni ko'rsat
EXPLAIN (ANALYZE, BUFFERS)
SELECT o.id, o.created_at, SUM(i.qty * i.unit_price) AS total
FROM orders o
JOIN order_items i ON i.order_id = o.id
WHERE o.warehouse_id = 42
  AND o.created_at >= now() - interval '30 days'
GROUP BY o.id, o.created_at
ORDER BY o.created_at DESC
LIMIT 100;

-- Indeks qo'yilgandan keyin rejani qayta oling va PR izohiga ikkisini qo'ying.
CREATE INDEX CONCURRENTLY idx_orders_wh_created
    ON orders (warehouse_id, created_at DESC);
```

Agar o'lchov imkonsiz bo'lsa, ikkinchi qadam vaqt chegarasi bilan prototip. Ikki tomon ham yarim kun ichida eng kichik ishlaydigan variantini yozadi va uchrashuvda ikkisini solishtiradi. Uchinchi qadam uchinchi odamni chaqirish, lekin uning roli hakam emas, savol beruvchi. Agar bahs baribir hal bo'lmasa, qaytarilishi oson variantni tanlash kerak: xato variantni bir hafta ichida qaytarish, to'g'ri variantni bir oy kutishdan arzon. Qaror qabul qilinganda uni va sababini yozib qo'y, aks holda uch oydan keyin bir xil bahs qaytadi.

### 36.7 Yangi odamga review orqali o'rgatish

Yangi odamning birinchi PR si uchun qoida oddiy: uchtadan ko'p izoh yozma. Qolgan muammolarni ro'yxatga ol va keyingi PR larga tarqat. Bu yumshoqlik emas, hisob-kitob: bir vaqtda uchta narsadan ko'pini o'rganib bo'lmaydi.

Ikkinchi qoida izoh ichida havola qoldirish. "Biz bu yerda doim idempotency key ishlatamiz, mana shu servisda namunasi bor" degan izoh kodni ham tuzatadi, ham kodbazani o'rgatadi. Uchinchi qoida teskari yo'nalish: yangi odamga katta PR ni review qilishni berish. U savol berishga majbur bo'ladi va o'sha savollar sening hujjatlaringdagi bo'shliqni ko'rsatadi.

Taxminan uch oydan keyin yangi odam o'z sohasida review qila oladigan darajaga chiqishi kerak. Agar chiqmasa, bu uning qobiliyati emas, sening o'rgatish tizimining muammosi.

### 36.8 Arxitektura qarorlarini jamoaga tarqatish: hujjat, ichki suhbat, namuna kod

Qaror uch kanalda tarqalmasa, u mavjud emas. Birinchi kanal yozma qaror hujjati: kontekst, variantlar, tanlangan yo'l, oqibatlar, qachon qayta ko'riladi. Bir sahifadan oshmasligi kerak, aks holda o'qilmaydi. Ikkinchi kanal og'zaki: 20 daqiqalik ichki suhbat, unda savollar beriladi va hujjat yaxshilanadi. Uchinchi va eng kuchli kanal namuna kod: qarorga mos keladigan bitta haqiqiy servis, odamlar undan nusxa oladi.

Faqat hujjat yozish eng ko'p uchraydigan xato. Odamlar hujjat emas, qo'shni paket kodidan nusxa oladi. Shuning uchun qaror qabul qilingandan keyin birinchi ish bitta haqiqiy joyni yangi yo'lga o'tkazish, va PR tavsifida "bu yangi standart, keyingi servislar shunday qiladi" deb yozish.

### 36.9 Standart o'rnatish: linter, formatlash, ArchUnit qoidalari, shablon loyiha

Yozma qoida esdan chiqadi, bajarilishi majburlangan qoida qolaveradi. Shuning uchun har bir takrorlanadigan review izohini mashinaga o'tkazish kerak. Qatlam chegaralari uchun ArchUnit eng arzon vosita.

```java
@AnalyzeClasses(packages = "com.shop", importOptions = ImportOption.DoNotIncludeTests.class)
class ArchitectureTest {

    // Controller to'g'ridan-to'g'ri repository ga kirmasin: faqat service orqali
    @ArchTest
    static final ArchRule controller_service_orqali_ishlaydi =
        noClasses().that().resideInAPackage("..web..")
            .should().dependOnClassesThat().resideInAPackage("..repository..");

    // Domen paketi Spring ga va JPA ga bog'lanmasin: toza domen qoidasi
    @ArchTest
    static final ArchRule domen_toza_qolsin =
        noClasses().that().resideInAPackage("..domain.model..")
            .should().dependOnClassesThat()
            .resideInAnyPackage("org.springframework..", "jakarta.persistence..");

    // Pul maydonlari uchun double ishlatilmasin
    @ArchTest
    static final ArchRule pul_bigdecimal_bilan =
        noFields().that().haveNameMatching(".*(amount|price|total)")
            .should().haveRawType(Double.class).orShould().haveRawType(double.class);
}
```

Shablon loyiha standartning eng tez tarqaladigan ko'rinishi. Ichida tayyor bo'lishi kerak: observability sozlamasi, xato javobi formati, migratsiya vositasi, test bazasi konfiguratsiyasi, CI pipeline. Yangi servis birinchi kundan to'g'ri skeletda tug'iladi.

```properties
# Shablon loyihaning asosiy sozlamalari: har bir yangi servis shu yerdan boshlanadi
spring.datasource.hikari.maximum-pool-size=10
spring.datasource.hikari.connection-timeout=3000
spring.jpa.open-in-view=false
spring.jpa.properties.hibernate.jdbc.batch_size=50
# n+1 muammosini test paytida ko'rinadigan qilish
spring.jpa.properties.hibernate.query.fail_on_pagination_over_collection_fetch=true
management.endpoints.web.exposure.include=health,info,prometheus
management.endpoint.health.probes.enabled=true
server.shutdown=graceful
spring.lifecycle.timeout-per-shutdown-phase=25s
```

| Tuzoq | Nega yuzaga keladi | Yechim |
|---|---|---|
| Review faqat formatlash haqida | CI da formatter yo'q | Spotless va pre-commit hook qo'yish |
| "LGTM" bilan 800 qator o'tadi | PR hajmi chegarasi yo'q | Hajm bo'yicha ogohlantirish, PR ni bo'lish |
| Bir xil izoh har hafta qaytadi | Qoida odam xotirasida | ArchUnit yoki custom lint qoidasi |
| Qaror uch oydan keyin yo'qoladi | Faqat chatda aytilgan | Qisqa qaror hujjati va namuna kod |
| Yetakchi review bottleneck | Hamma PR unga yo'naltirilgan | Soha egalari, CODEOWNERS taqsimoti |
| Yangi odam sekin o'sadi | PR da 30 izoh, prioritet yo'q | Uchta izoh qoidasi va prefikslar |
| Migratsiya yarim yo'lda qoladi | Eski yo'l o'chirilmagan | Oxirgi PR da eski kodni o'chirish sharti |
| Faqat bitta odam domenni biladi | Review doim bir odamda | Juftlik review va rotatsiya |

### 36.10 Jamoaning bilim xaritasi va bitta odamga bog'liqlikni kamaytirish

Har bir yetakchi o'z jamoasining bilim xaritasini yozib qo'yishi kerak: qaysi tizimni kim chuqur biladi, kim o'rtacha biladi, kim umuman bilmaydi. Xarita tayyor bo'lgach, eng xavfli hujayralar ko'rinadi: muhim tizim, uni faqat bitta odam biladi. Bu odam ta'tilga chiqsa yoki ishdan ketsa, jamoa to'xtaydi.

Kamaytirish usullari amaliy. Review ni shu sohada ikkinchi odamga berish, lekin birinchi odamni ham qo'shish. Incident dan keyin tahlilni boshqa odam yozishi. To'lov yoki ombor qoldig'i kabi kritik tizimda har chorakda bitta o'rtacha hajmli ishni "bilmaydigan" odamga berish va birinchi odamni maslahatchi qilish. Maqsad: har bir kritik tizimda kamida ikkita odam ishonchli o'zgartirish kirita olishi.

### 36.11 Texnik yetakchi va menejer roli farqi

Ikki rol aralashganda ikkisi ham buziladi. Menejer odamlar uchun javob beradi: o'sish, ish taqsimi, baho, konfliktlar. Texnik yetakchi tizim uchun javob beradi: arxitektura, sifat darvozalari, texnik qarzni boshqarish, qaror sifati. Yetakchining vakolati lavozimdan emas, ishonchdan keladi, va ishonch kod yozish bilan saqlanadi.

Eng muhim farq ta'sir usulida. Menejer qaror qabul qilib buyruq berishi mumkin. Yetakchi esa odamlarni ishontirishi kerak, chunki uning qo'lida majburlash vositasi yo'q. Shuning uchun yetakchining asosiy quroli dalil, prototip va yozma hujjat. Agar yetakchi "men shunday dedim" ga tayansa, u menejer rolini noto'g'ri o'zlashtirgan bo'ladi.

Bir xil narsada ikki rol birlashadi: ikkisi ham odamlar ishini bloklaydigan to'siqlarni olib tashlashi kerak. Yetakchi uchun bu ko'pincha review navbati, sekin build va noaniq talab.

### 36.12 Vaqtni taqsimlash: kod, hujjat, suhbat, o'rganish

Taxminiy nisbat haftada shunday ko'rinadi: 40 foiz kod va review, 20 foiz hujjat va qaror, 25 foiz suhbat va juftlik ishi, 15 foiz o'rganish va o'lchash. Kod yozishni butunlay tashlab qo'ygan yetakchi ikki chorakdan keyin kodbazani bilmay qoladi va uning qarorlari xayoliy bo'lib qoladi. Kodning 100 foizini o'zi yozadigan yetakchi esa jamoani o'stirmaydi va bottleneck ga aylanadi.

Amaliy qoida: haftada kamida bitta haqiqiy PR yoz, lekin kritik yo'ldagi ishni o'zingga olma. Eng yaxshi tanlov shablon loyihaga, observability ga, yoki migratsiyaning birinchi namunasiga tegishli ish. Shunday ish ikki maqsadni bajaradi: sen kontekstni saqlaysan va jamoa nusxa oladigan namuna paydo bo'ladi. Review uchun kuniga ikki oyna ajrat va o'sha oynalarda chuqur ishlamagin, chunki review diqqat talab qiladi.

### 36.13 Amalda qo'llash

- [ ] Review izohlari uchun to'rtta prefiks kelishib ol (`blocker`, `kerak`, `fikr`, `maqtov`) va PR shablonida ularni yoz.
- [ ] Oxirgi 30 ta PR dagi izohlarni o'qib chiq, formatlash va uslubga tegishli hamma izohni Spotless yoki static analyzer qoidasiga ko'chir.
- [ ] CI ga uchta darvoza qo'y: `spotless:check`, static analyzer, va `Arch*Test` qoidalari.
- [ ] ArchUnit da kamida uch qoida yoz: controller to'g'ridan repository ga kirmasin, domen Spring ga bog'lanmasin, pul maydoni `double` bo'lmasin.
- [ ] PR hajmi va navbat vaqtini o'lchay boshla, 400 qatordan katta PR uchun bo'lish talabini kelish.
- [ ] Jamoa bilim xaritasini jadval shaklida yoz va har bir kritik tizim uchun ikkinchi odamni belgila.
- [ ] Oxirgi uch arxitektura qarorini bir sahifalik hujjat qilib yoz va har biriga namuna kod joyini havola qil.
- [ ] Shablon loyiha yarat yoki yangila: pool, timeout, graceful shutdown, metrikalar, migratsiya va test bazasi tayyor bo'lsin.

## 37. Xarajat, SLO va biznes bilan muloqot (Cost, SLO and Business Communication)

Arxitektorning har bir qarori oxir-oqibat pulga aylanadi. Qo'shimcha indeks disk bandini oshiradi, qo'shimcha replika hisoblash hisobini oshiradi, qo'shimcha abstraksiya esa odam vaqtini yeydi. Bu bob texnik qarorni pul va risk tilida gapirishga, mavjudlik maqsadini raqam bilan belgilashga va rahbar bilan bir xil lug'atda muloqot qilishga bag'ishlangan.

### 37.1 Arxitektura qarorining pul tarafi: server, litsenziya, odam vaqti

Xarajatning uchta katta manbasi bor: infratuzilma, litsenziya va odam vaqti. Ko'p jamoa faqat birinchisini sanaydi, chunki u hisob-fakturada ko'rinadi. Haqiqatda o'rta hajmli to'lov servisida odam vaqti infratuzilmadan 3-10 barobar qimmat. Oyiga 8 ta developer, har biri taxminan 4000 dollar bo'lsa, jamoa oyiga 32 000 dollar turadi, serveri esa 3000 dollar.

Shuning uchun "serverni tejash uchun murakkab yechim" deyarli har doim yutqazadi. Oyiga 400 dollar tejaydigan optimizatsiya har oyda bir developer kunini olsa, siz zarar ko'rasiz. Teskari holat ham bor: noto'g'ri tanlangan instance turi yiliga 100 000 dollar yo'qotishi mumkin.

Litsenziya alohida gap. Tijorat databazasi yoki APM agenti CPU soniga bog'langan bo'lsa, gorizontal scaling narxi pog'onali o'sadi. PostgreSQL da litsenziya nol, lekin tuning va backup uchun odam bilimi kerak.

```java
// Qarorni pul bilan baholash: uchta manba bir joyda.
public record QarorNarxi(
        BigDecimal infraOylik,      // server, disk, tarmoq
        BigDecimal litsenziyaOylik, // CPU yoki node ga bog'liq
        int odamKuni,               // yozish va joylashtirish
        int yillikQollabQuvvatlashKuni) {

    private static final BigDecimal KUN_NARXI = new BigDecimal("200");

    // Uch yillik umumiy egalik narxi (TCO).
    public BigDecimal uchYillik() {
        BigDecimal oylik = infraOylik.add(litsenziyaOylik)
                .multiply(BigDecimal.valueOf(36));
        BigDecimal birMartalik = KUN_NARXI.multiply(BigDecimal.valueOf(odamKuni));
        BigDecimal qollab = KUN_NARXI
                .multiply(BigDecimal.valueOf(yillikQollabQuvvatlashKuni * 3L));
        return oylik.add(birMartalik).add(qollab);
    }
}
```

### 37.2 Bulut xarajati qayerdan keladi: hisoblash, saqlash, tarmoq chiqishi, boshqariladigan xizmat

Bulut hisobi to'rtta ustunga bo'linadi. Hisoblash odatda eng katta qism, 40-60 foiz. Saqlash 10-25 foiz. Tarmoq chiqishi (egress) 5-20 foiz, lekin kutilmaganda portlashi mumkin. Qolgan qismni boshqariladigan xizmatlar egallaydi.

Eng ko'p e'tibordan chetda qoladigan narsa egress. Zonalar orasidagi trafik ham pulli. Agar buyurtma servisi har bir so'rovda ombor servisiga 4 marta murojaat qilsa va javob 20 KB bo'lsa, kuniga 10 million so'rovda bu 800 GB zona-aro trafik. GB uchun 0.01 dollar bilan bu oyiga taxminan 240 dollar faqat shu yo'nalishda.

Saqlashda PostgreSQL ko'pincha kutilgandan katta bo'ladi. Indekslar jadval hajmining 50-150 foizini tashkil qilishi oddiy hol. WAL arxivi va PITR nusxalari ham hisobga qo'shiladi.

```sql
-- Qaysi jadval va indeks qancha joy egallaydi: xarajat tahlilining birinchi qadami.
SELECT c.relname AS obyekt,
       pg_size_pretty(pg_total_relation_size(c.oid)) AS umumiy,
       pg_size_pretty(pg_indexes_size(c.oid))   AS indekslar,
       s.n_live_tup                             AS qatorlar
FROM pg_class c
JOIN pg_namespace n ON n.oid = c.relnamespace
LEFT JOIN pg_stat_user_tables s ON s.relid = c.oid
WHERE n.nspname = 'public' AND c.relkind = 'r'
ORDER BY pg_total_relation_size(c.oid) DESC
LIMIT 15;

-- Ishlatilmayotgan indeks: sof xarajat, hech qanday foyda yo'q.
SELECT relname, indexrelname, idx_scan,
       pg_size_pretty(pg_relation_size(indexrelid))
FROM pg_stat_user_indexes
WHERE idx_scan < 50
ORDER BY pg_relation_size(indexrelid) DESC;
```

### 37.3 Bitta so'rovning narxi: oddiy hisob va uni kuzatish

Bitta so'rovning narxini bilish muloqotni butunlay o'zgartiradi. Hisob oddiy: oylik infratuzilma xarajatini oylik so'rov soniga bo'lasiz. Servis oyiga 5000 dollar olsa va 50 million so'rovni qayta ishlasa, bitta so'rov 0.0001 dollar turadi.

Keyin bu raqamni endpoint bo'yicha taqsimlash kerak, chunki hamma so'rov teng emas. Hisobot generatsiyasi 2 soniya CPU vaqtini oladi, oddiy GET esa 5 millisekund. CPU bo'yicha vaznlaganda hisobot endpointi so'rovlarning 0.5 foizini tashkil qilib, xarajatning 40 foizini yeyayotgani ko'rinadi.

```java
// Har bir endpoint uchun CPU vaqtini yig'amiz, keyin xarajatni vaznlab taqsimlaymiz.
@Component
class SorovNarxiFiltri implements Filter {

    private final MeterRegistry registry;
    private final ThreadMXBean threads = ManagementFactory.getThreadMXBean();

    SorovNarxiFiltri(MeterRegistry registry) { this.registry = registry; }

    @Override
    public void doFilter(ServletRequest req, ServletResponse res, FilterChain chain)
            throws IOException, ServletException {
        long boshCpu = threads.getCurrentThreadCpuTime(); // nanosekund
        try {
            chain.doFilter(req, res);
        } finally {
            long sarf = threads.getCurrentThreadCpuTime() - boshCpu;
            String yol = ((HttpServletRequest) req).getRequestURI();
            // Counter sifatida yig'amiz: keyin narxga ko'paytiriladi.
            registry.counter("sorov.cpu.nanos", "yol", yol).increment(sarf);
        }
    }
}
```

Endpoint ulushi uning CPU nanosekundlarini umumiy yig'indiga bo'lgan nisbati. Endpoint xarajati shu ulushni oylik hisobga ko'paytirish natijasi. Databaza uchun ham shunday yondashuv bor: `pg_stat_statements` dagi `total_exec_time` bo'yicha taqsimlanadi.

### 37.4 Xarajatni kamaytirish yo'llari va ularning sifatga ta'siri

Har bir tejash usuli biror narsani qurbon qiladi, va arxitektorning vazifasi qurbonlikni ochiq aytish. Instance o'lchamini kichraytirish eng tez natija beradi, lekin CPU zaxirasi kamayganda p99 latency keskin o'sadi. 70 foiz CPU bandligi xavfsiz chegara, 85 foizdan oshsa latency ikki barobar bo'lishi mumkin.

Reserved chegirmalari 30-55 foiz tejaydi va sifatga ta'sir qilmaydi, narxi esa 1-3 yillik majburiyat. Cache qo'shish databaza yuklamasini 60-90 foiz kamaytiradi, narxi ma'lumotning eskirishi: ombor qoldig'ini 30 soniya cache'lash arziydi, hisob balansini cache'lash esa pul yo'qotadi.

| Usul | Taxminiy tejash | Sifatga ta'siri | Qachon arziydi |
|---|---|---|---|
| Instance kichraytirish | 20-40% | p99 latency o'sadi | CPU 40% dan past bo'lsa |
| Reserved/committed | 30-55% | Yo'q | Barqaror bazaviy yuk |
| Spot node | 60-80% | Node to'satdan o'chadi | Batch va stateless ish |
| Cache qatlami | DB yukida 60-90% | Ma'lumot eskirishi | Ko'p o'qilsa, kam o'zgarsa |
| Eski ma'lumot arxivi | Saqlashda 70-90% | Arxivga murojaat sekin | Audit va hisobot ma'lumoti |
| Replika sonini kamaytirish | 25-50% | Chidamlilik tushadi | SLO 99.9% dan past bo'lsa |
| Log hajmini qisqartirish | Observability'da 40-70% | Debug qiyinlashadi | DEBUG prod'da yoqilgan bo'lsa |
| Zona-aro trafikni kamaytirish | Egress'da 50-80% | Joylashuv moslashuvi kamayadi | Servislar ko'p gaplashsa |

### 37.5 SLI, SLO va SLA farqi, ularni to'g'ri tanlash

SLI bu o'lchov, ya'ni raqam. SLO bu shu raqamga qo'yilgan ichki maqsad. SLA bu mijoz bilan tuzilgan shartnoma va jarima. To'lov API uchun SLI "5xx bo'lmagan so'rovlar ulushi", SLO "30 kunlik oynada 99.95 foizdan katta", SLA "oyiga 99.9 foizdan past bo'lsa, mijoz to'lovning 10 foizini qaytaradi". SLO har doim SLA dan qattiqroq bo'lishi kerak, chunki sizga reaksiya uchun zahira kerak.

SLI tanlashda ikkita qoida bor. Birinchi, foydalanuvchi sezadigan narsani o'lchang: CPU bandligi SLI emas. Ikkinchi, SLI nisbat bo'lsin. "Kuniga 100 ta xato" yuk o'sganda ma'nosiz bo'ladi, "xato ulushi 0.1 foizdan kam" esa har doim ma'noli. Latency SLI ni chegara bilan yozing, chunki o'rtacha qiymat og'ir dumni yashiradi.

```yaml
# Prometheus recording rule: SLI ni bitta joyda ta'riflab qo'yamiz.
groups:
  - name: tolov-slo
    interval: 30s
    rules:
      # Muvaffaqiyat ulushi: 5xx bo'lmagan so'rovlar.
      - record: tolov:sli_muvaffaqiyat:ratio5m
        expr: |
          sum(rate(http_server_requests_seconds_count{
                service="tolov", status!~"5.."}[5m]))
          /
          sum(rate(http_server_requests_seconds_count{service="tolov"}[5m]))

      # Latency SLI: 300 ms dan tez javoblar ulushi.
      - record: tolov:sli_tezlik:ratio5m
        expr: |
          sum(rate(http_server_requests_seconds_bucket{
                service="tolov", le="0.3"}[5m]))
          /
          sum(rate(http_server_requests_seconds_count{service="tolov"}[5m]))

      # 30 kunlik error budget qoldig'i, 99.95% SLO uchun.
      - record: tolov:error_budget:qoldiq
        expr: |
          1 - ((1 - avg_over_time(tolov:sli_muvaffaqiyat:ratio5m[30d])) / 0.0005)
```

### 37.6 Xato byudjeti (error budget) va u qanday qaror qabul qilishga yordam beradi

Error budget bu SLO ruxsat bergan nosozlik miqdori. SLO 99.9 foiz bo'lsa, byudjet 0.1 foiz. 30 kunlik oynada 100 million so'rov bo'lsa, siz 100 000 ta so'rovni yo'qotishga haqlisiz. Bu jarima emas, balki resurs.

Byudjetning asosiy foydasi bahsni tugatishi. Byudjet bor ekan, reliz davom etadi. Byudjet tugasa, yangi funksiya to'xtaydi va jamoa barqarorlikka o'tadi. Bu qoida oldindan kelishiladi.

Byudjetni sarflanish tezligi (burn rate) bilan kuzatish kerak. Burn rate 1 degani byudjet oyning oxirida tugaydi. Burn rate 14.4 degani byudjet 50 soatda tugaydi, bu darhol alert sababi. Sekin oqish uchun 6 soatlik oynada burn rate 6 dan katta bo'lishi yetarli signal.

```bash
#!/usr/bin/env bash
# Error budget qoldig'ini hisoblash: 30 kunlik oyna, SLO = 99.95%.
SLO_UZILISH=0.0005            # ruxsat etilgan xato ulushi
JAMI=$(curl -sG "$PROM/api/v1/query" \
  --data-urlencode 'query=sum(increase(http_server_requests_seconds_count{service="tolov"}[30d]))' \
  | jq -r '.data.result[0].value[1]')
XATO=$(curl -sG "$PROM/api/v1/query" \
  --data-urlencode 'query=sum(increase(http_server_requests_seconds_count{service="tolov",status=~"5.."}[30d]))' \
  | jq -r '.data.result[0].value[1]')

RUXSAT=$(echo "$JAMI * $SLO_UZILISH" | bc -l)
QOLDIQ=$(echo "scale=1; 100 * (1 - $XATO / $RUXSAT)" | bc -l)
echo "Ruxsat etilgan xato: ${RUXSAT%.*}, sodir bo'lgan: ${XATO%.*}"
echo "Byudjet qoldigi: ${QOLDIQ}%"

# 25% dan kam qolsa reliz quvurini to'xtatamiz.
awk -v q="$QOLDIQ" 'BEGIN { exit (q < 25) ? 1 : 0 }' || {
  echo "BYUDJET TUGAYAPTI: yangi funksiya relizi to'xtatiladi"; exit 1; }
```

### 37.7 Mavjudlik raqamlari: 99.9 va 99.99 orasidagi amaliy farq va narxi

Mavjudlik foizini vaqtga aylantirmasangiz, muzokara bo'sh gap bo'lib qoladi. Jadvalda yil 365 kun, oy 30 kun deb olingan.

| Mavjudlik | Yillik uzilish | Oylik uzilish | Haftalik uzilish | Odatiy arxitektura | Narx koeffitsiyenti |
|---|---|---|---|---|---|
| 99% | 3 kun 15 soat 36 daqiqa | 7 soat 12 daqiqa | 1 soat 40.8 daqiqa | Bitta instance, qo'lda tiklash | 1x |
| 99.5% | 1 kun 19 soat 48 daqiqa | 3 soat 36 daqiqa | 50.4 daqiqa | Bitta instance, avtomatik restart | 1.2x |
| 99.9% | 8 soat 45.6 daqiqa | 43.2 daqiqa | 10.1 daqiqa | 2 instance, bitta zona, qo'lda DB failover | 1.5x |
| 99.95% | 4 soat 22.8 daqiqa | 21.6 daqiqa | 5.04 daqiqa | 3 instance, 2 zona, avtomatik failover | 2.2x |
| 99.99% | 52.6 daqiqa | 4.32 daqiqa | 1.01 daqiqa | 3 zona, replikalar, 24/7 navbatchi | 3.5x |
| 99.999% | 5.26 daqiqa | 25.9 soniya | 6.05 soniya | Ko'p mintaqa, aktiv-aktiv | 8x va yuqori |

Amaliy farq shunda. 99.9 foizda oyda 43.2 daqiqa bor, bu bitta sekin deploy yoki bitta qo'lda DB failover uchun yetadi. 99.99 foizda oyda faqat 4.32 daqiqa bor, bu odam aralashuviga vaqt qoldirmaydi. Ya'ni 99.99 foiz talab qilish butun tiklashni avtomatlashtirishga majbur qiladi.

99.9 dan 99.99 ga o'tish uchun uchta availability zone, zona-aro replikatsiya, avtomatik failover, 24/7 navbatchilik va chaos mashqi kerak. Bu infratuzilmani taxminan 2.5 barobar va odam xarajatini 2 barobar oshiradi.

Muhim ogohlantirish: zanjirdagi mavjudliklar ko'paytiriladi. To'lov servisi uchta bog'liqlikka murojaat qilsa va har biri 99.9 foiz bo'lsa, umumiy nazariy mavjudlik 99.7 foiz. Shuning uchun yuqori SLO faqat zaxira yo'li va graceful degradation bilan erishiladi.

### 37.8 Nofunksional talabni biznes tiliga o'girish

Biznes "tez bo'lsin" deydi, arxitektor esa buni o'lchanadigan shaklga aylantiradi. Tarjima formulasi: kim, nima qiladi, qanday tezlikda, qanday yuk ostida, qanday ulushda. "Katalog tez ochilsin" quyidagicha aylanadi: "mobil mijozda katalog so'rovlarining 95 foizi 400 ms ichida, 99 foizi 900 ms ichida javob oladi, sekundda 3000 so'rov yuklamasida".

Teskari tarjima ham kerak. "p99 latency 600 ms ga tushdi" o'rniga "checkout sahifasini tashlab ketish 2.1 foizdan 1.4 foizga tushdi, bu oyiga taxminan 180 000 dollar aylanma" deyish kerak.

| Mavzu | Oddiy yondashuv | Arxitektor yondashuvi |
|---|---|---|
| Talab shakli | "Tizim tez va ishonchli bo'lsin" | "p99 < 400 ms, xato ulushi < 0.1%, 3000 rps da" |
| Mavjudlik | "Hech qachon o'chmasin" | "99.95%, oyiga 21.6 daqiqa byudjet bilan" |
| Xarajat | Oylik hisobni umumiy ko'rish | Endpoint bo'yicha bitta so'rov narxi |
| Optimizatsiya sababi | "Kod chiroyli bo'lmadi" | "Bu endpoint xarajatning 40% ini yeyadi" |
| Reliz qarori | Har kim o'z fikrini aytadi | Error budget qoldig'i qarorni belgilaydi |
| Texnik qarz | "Refactoring kerak" | "Bu modul har bir o'zgarishga 3 kun qo'shadi" |
| Yangi texnologiya | "Zamonaviy stack" | "2 hafta tajriba, 5% trafik, o'lchov bilan qaror" |
| Muddat muzokarasi | Hajmni saqlab, sifatni qurbon qilish | Hajmni kesib, sifat darvozasini saqlash |
| Rahbarga hisobot | Grafanadagi 30 ta grafik | 5 ta raqam, trend va bitta qaror so'rovi |
| Incident xulosasi | Kim aybdor topiladi | Byudjet sarfi va to'rtta tuzatish ishi |

### 37.9 Texnik qarzni biznesga tushuntirish: tezlik va xavf tilida

"Kod iflos" deb gapirish ishlamaydi. Biznes ikkita narsani tushunadi: tezlik va xavf. Tezlik tomoni: "buyurtma modulida har bir o'rtacha o'zgarish 2 kun emas, 6 kun oladi, chunki bitta o'zgarish 14 joyni tegishga majbur qiladi". Bu raqam Git tarixidan olinadi.

Xavf tomoni: "shu modulga tegadigan relizlarning 30 foizi hotfix bilan tugaydi, boshqa modullarda bu 4 foiz". Change failure rate modul bo'yicha ajratilsa, qaysi joy pul yo'qotayotgani ko'rinadi.

Keyin taklifni investitsiya shaklida qo'yasiz. "15 kun ish, natijada o'zgarish vaqti 6 kundan 3 kunga tushadi. Yiliga shu modulda 40 ta o'zgarish bo'ladi, ya'ni 120 kun tejaladi. To'lanish muddati taxminan 2 oy." Bu shaklda rad etish qiyin.

| Tuzoq | Nima sodir bo'ladi | Yechim |
|---|---|---|
| SLO ni darhol 99.99% qilish | Byudjet doim tugaydi, jamoa alertga ishonmaydi | Haqiqiy o'lchovdan boshlab, bosqichma-bosqich qattiqlashtiring |
| SLI sifatida CPU olish | Mijoz azob chekadi, dashboard yashil turadi | Faqat foydalanuvchi sezadigan o'lchovni SLI qiling |
| O'rtacha latency bo'yicha SLO | Og'ir dum yashiriladi | p95 va p99 ni chegara bilan yozing |
| SLA ni SLO ga teng qilish | Bitta hodisa darhol jarimaga aylanadi | SLO ni SLA dan bir pog'ona qattiq qiling |
| Xarajatni faqat yillik ko'rish | Oqish 11 oy sezilmaydi | Oylik byudjet va 20% oshganda alert qo'ying |
| Zaxirani ko'p olish | Arxitektura o'zgarsa, to'lov behuda ketadi | Faqat barqaror bazaviy yukni majburiyatga oling |
| DEBUG log prod'da qolishi | Observability hisobi 3-5 barobar oshadi | Log darajasini konfiguratsiyadan boshqaring |
| Tajribani o'lchovsiz yoyish | Natija bor-yo'qligi noma'lum qoladi | Metrika va to'xtatish shartini oldindan yozing |

### 37.10 Qaror uchun arzon o'lchov: kichik tajriba va bosqichma-bosqich yoyish

Katta qarorni bahs bilan hal qilish qimmat. Bir hafta ishlaydigan prototip ikki oylik bahsdan tezroq javob beradi. Tajriba uchun uchta narsa oldindan yozilishi kerak: qanday metrika o'lchanadi, qanday natija "ha" deb hisoblanadi, qachon to'xtatiladi.

Prod'da yoyish bosqichli bo'lsin: 1 foiz, 5 foiz, 25 foiz, 100 foiz. Har bosqichda kamida bitta to'liq ish kuni kutiladi. Bu qoida yangi kod uchun ham, konfiguratsiya o'zgarishi va yangi indeks uchun ham amal qiladi.

```java
// Bosqichma-bosqich yoyish: foiz konfiguratsiyadan keladi, kod o'zgarmaydi.
@Service
class HisobotYonaltirgichi {

    private final HisobotYozuvchi yangi;
    private final HisobotYozuvchi eski;
    private final Environment env;

    HisobotNatija yarat(HisobotSorovi sorov) {
        int foiz = env.getProperty("hisobot.yangi-yol.foiz", Integer.class, 0);
        // Barqaror taqsimot: bir mijoz har doim bir yo'ldan o'tadi.
        int chelak = Math.floorMod(sorov.mijozId().hashCode(), 100);
        if (chelak < foiz) {
            return yangi.yarat(sorov);
        }
        return eski.yarat(sorov);
    }
}
```

```properties
# Yoyish jadvali: har bosqichda bitta ish kuni kuzatiladi.
# 1-kun: 1%, 2-kun: 5%, 4-kun: 25%, 7-kun: 100%
hisobot.yangi-yol.foiz=5

# To'xtatish sharti: p99 300 ms dan oshsa yoki xato ulushi 0.2% dan oshsa.
hisobot.yangi-yol.p99-chegara-ms=300
hisobot.yangi-yol.xato-chegara-foiz=0.2

# Yangi yo'l uchun alohida pool: eski yo'lni himoya qiladi.
spring.datasource.hikari.maximum-pool-size=20
hisobot.datasource.hikari.maximum-pool-size=6
hisobot.datasource.hikari.connection-timeout=2000
```

### 37.11 Yetkazib berish muddati va sifat orasidagi muzokarani olib borish

Muzokarada uchta o'zgaruvchi bor: hajm, muddat va sifat. Ikkitasini qotirsangiz, uchinchisi erkin qoladi. Ko'p jamoa muddat va hajmni qotiradi, keyin sifat qurbon bo'ladi. Natija hotfix to'lqini, ya'ni tejalgan vaqt qarz bilan qaytariladi.

Arxitektorning pozitsiyasi aniq bo'lsin: sifat darvozasi muzokara mavzusi emas, hajm esa muzokara mavzusi. Amalda bu "o'nta funksiyani yarim sifat bilan" o'rniga "to'rtta funksiyani to'liq sifat bilan" degan taklifga aylanadi. Eng yaxshi kesish funksiyani butunlay olib tashlash emas, balki qamrovini qisqartirish: birinchi relizda faqat oxirgi 30 kunlik ma'lumot, faqat CSV eksport, faqat ichki foydalanuvchi uchun.

Muzokaraga raqam bilan kiring. "Bu muddatda sifatni saqlash uchun hajmdan 35 foizini kesish kerak. Kesmasak, bahom: relizdan keyin 2-3 hafta hotfix, va shu davrda yangi ish bo'lmaydi." Bahoni oldingi relizlar ma'lumoti bilan tasdiqlang.

### 37.12 Hisobot: rahbarga nima ko'rsatiladi va qanday ko'rinishda

Rahbarga 30 ta grafik ko'rsatish hisobot emas. To'g'ri hisobot bir sahifa, besh raqam va bitta aniq so'rovdan iborat. Besh raqam: SLO bajarilishi va error budget qoldig'i, oylik xarajat va o'tgan oyga nisbatan o'zgarish, bitta so'rovning narxi va trendi, lead time bilan change failure rate, va ochiq qolgan eng katta xavf.

Har bir raqam yonida trend va bitta izoh bo'lsin. Izoh sabab yoki harakatni aytadi. "Xarajat 12 foiz oshdi, sababi hisobot trafigi ikki barobar bo'ldi, tungi batch'ga ko'chirish ishi boshlandi" yaxshi izoh.

Hisobot oxirida aniq so'rov bo'lishi kerak. "Ma'lumot uchun" deb tugagan hisobot foydasiz. "Hisobot SLO sini 99.9 dan 99.5 ga tushirishni taklif qilamiz, bu oyiga 2200 dollar tejaydi" deb tugasin. Incident xulosasi ham shu mantiqda: kim aybdor emas, nima byudjetni sarfladi va qaysi to'rtta ish buni qaytarilmas qiladi.

### 37.13 Amalda qo'llash

- [ ] Eng yuqori trafikli servis uchun oylik xarajatni so'rov soniga bo'lib, bitta so'rovning narxini raqam bilan yozib qo'y.
- [ ] `pg_stat_user_indexes` dan `idx_scan < 50` bo'lgan indekslarni topib, ularning umumiy hajmini va oylik saqlash narxini hisobla.
- [ ] Asosiy biznes oqimi uchun ikkita SLI ta'rifla: muvaffaqiyat ulushi va p99 latency chegarasi, ikkalasini recording rule sifatida yoz.
- [ ] SLO qiymatini tanlab, uni yillik va oylik uzilish daqiqasiga aylantir, va bu raqamni jamoa bilan kelish.
- [ ] Error budget qoldig'ini ko'rsatadigan dashboard paneli qo'sh, 25 foizdan kam qolganda reliz to'xtash qoidasini rasmiylashtir.
- [ ] Bitta nofunksional talabni o'lchanadigan shaklga aylantir: yuk, foiz va chegara bilan.
- [ ] Eng og'riqli modul uchun lead time va change failure rate ni hisoblab, texnik qarz taklifini to'lanish muddati bilan yoz.
- [ ] Rahbar uchun bir sahifali shablon tayyorla: besh raqam, trend, qisqa izoh va bitta aniq so'rov.

## 38. Doimiy o'rganish va texnologiya tanlash (Continuous Learning and Technology Choice)

Arxitektorning bilimi ikki xil eskiradi. Birinchisi tezda chiriydi: kutubxona versiyasi, konfiguratsiya kaliti, bulut panelining joylashuvi. Ikkinchisi o'n yil yashaydi: tranzaksiya izolyatsiyasi, xotira modeli, indeks tanlash mexanikasi. Bu bob shu ikki qatlamni ajratish, yangi texnologiyani sovuq boshda baholash va o'rganishni chorakka bo'lingan o'lchovli rejaga aylantirish haqida.

### 38.1 Nimani chuqur o'rganish kerak va nimani yuzaki bilish yetarli

Chuqurlik darajasini ehtimollik bilan tanlang. Agar mexanika buzilganda production incident bo'lsa va uni siz tuzatishingiz kerak bo'lsa, u chuqur bilim. Agar hujjatni ochib 20 daqiqada javob topsa bo'lsa, u yuzaki bilim.

To'lov servisi uchun ro'yxat shunday. Chuqur: JDBC tranzaksiya chegarasi, Hibernate flush tartibi, PostgreSQL row lock va deadlock, HikariCP pool o'lchami, JVM GC pauzalari, `ExecutorService` va virtual thread semantikasi. Yuzaki: Flyway migratsiya sintaksisi, Jackson annotatsiyalari, Testcontainers moduli nomi, OpenAPI generator sozlamasi.

Chuqur bilimning o'lchovi bitta: siz shu mexanikani kod bilan isbotlab bera olasizmi.

```java
// Chuqur bilimni tekshirish usuli: taxminni kod bilan isbotlash.
@Test
void flushTartibiInsertniUpdatedanOldinYuboradi() {
    var statistika = entityManagerFactory.unwrap(SessionFactory.class).getStatistics();
    statistika.setStatisticsEnabled(true);

    transactionTemplate.executeWithoutResult(status -> {
        var qoldiq = em.find(OmborQoldigi.class, 42L);
        qoldiq.kamaytir(5); // mavjud qoldiqni o'zgartiramiz
        em.persist(new OmborHarakati(42L, -5)); // yangi harakat yozuvi
        // Bu yerda hali hech qanday SQL ketmagan.
        assertThat(statistika.getPrepareStatementCount()).isZero();
    });

    // Flush insert'ni update'dan oldin yuboradi: unique constraint
    // kutilmagan tartibda ishga tushishi mumkin.
    assertThat(statistika.getEntityInsertCount()).isEqualTo(1);
    assertThat(statistika.getEntityUpdateCount()).isEqualTo(1);
}
```

Yuzaki bilim uchun boshqa strategiya: tafsilot o'rniga "qaerga qarash kerak" ni eslab qoling.

### 38.2 Uzoq yashaydigan bilim va tez eskiradigan bilim farqi

Standart va protokol darajasidagi bilim eng uzoq yashaydi. SQL'ning `SERIALIZABLE` semantikasi 1992 yildan beri o'zgarmagan, HTTP keshlash sarlavhalari 1999 yildan beri o'z kuchida.

Keyingi qatlam: implementatsiya mexanikasi. PostgreSQL MVCC va vacuum, Hibernate dirty checking, JVM escape analysis. Bu bilim 5 yildan 10 yilgacha yashaydi.

Eng tez eskiradigani: API sirti va konfiguratsiya nomi. `WebSecurityConfigurerAdapter` Spring Security 5.7 da deprecated bo'ldi va 6.0 da olib tashlandi. Konfiguratsiya nomini yodlash eng past daromadli investitsiya.

Amaliy qoida: o'qish vaqtingizning 60 foizini mexanikaga, 30 foizini joriy stack'ning reliz o'zgarishlariga, 10 foizini yangi texnologiyalarni kuzatishga ajrating.

### 38.3 Birlamchi manbalar: spetsifikatsiya, hujjat, manba kod, reliz eslatmasi

Blog postidan javob izlash odati arxitektorni sekin zaharlaydi. Blog ikkinchi qo'l, bitta versiyaga bog'langan va ko'pincha noto'g'ri. Birlamchi manbalar ketma-ketligini odat qiling.

Birinchi: rasmiy reference hujjat. Spring hujjatlari versiya bo'yicha ajratilgan, URL ichida versiya raqami bor. Har doim o'zingiz ishlatadigan versiyaning hujjatini oching, `current` ni emas.

Ikkinchi: reliz eslatmasi va migration guide. Spring Boot har bir minor reliz uchun migration guide chiqaradi, PostgreSQL har bir major reliz uchun "Migration to Version X" bo'limini beradi, OpenJDK esa JEP ro'yxatini beradi.

Uchinchi: spetsifikatsiya. Jakarta Persistence spetsifikatsiyasi `flush` semantikasini aytadi, Hibernate hujjati esa faqat o'z xulqini aytadi.

To'rtinchi: manba kod. Bu eng ishonchli manba va u bir buyruq bilan qo'lingizda bo'ladi.

```bash
# Barcha bog'liqliklarning manba kodini lokal repozitoriyga tushirish.
mvn dependency:sources dependency:resolve -Dclassifier=javadoc

# Spring Boot qaysi avtokonfiguratsiyani yoqdi va nega yoqmadi.
java -jar target/app.jar --debug 2>&1 | sed -n '/CONDITIONS EVALUATION/,/^$/p'

# BOM import qilingandan keyin aslida qaysi versiya tanlandi.
mvn help:effective-pom -Doutput=/tmp/effective-pom.xml

# Konkret kutubxonaning versiya konflikti qayerdan kelgan.
mvn dependency:tree -Dincludes=com.fasterxml.jackson.core:jackson-databind
```

Manba kodni o'qishni odat qiling. Spring'da annotatsiya ortidagi `BeanPostProcessor` ni topib o'qish 30 daqiqa oladi, va bu bilim 5 yil yashaydi.

### 38.4 Yangi kutubxonani baholash mezonlari: qo'llab-quvvatlash, bog'liqlik, chiqish yo'li

Kutubxona tanlashni yozma mezon bilan qiling. Men yetti mezondan foydalanaman va har biriga raqam yoki aniq javob talab qilaman.

Birinchi: tiriklik. Oxirgi 12 oyda kamida 4 ta reliz bo'ldimi, loyihani bitta odam ushlab turadimi.

Ikkinchi: bog'liqlik og'irligi. Bitta JSON yordamchisi 14 ta tranzitiv jar olib kelsa, bu yomon signal.

Uchinchi: stack bilan to'qnashuv. Kutubxona Jackson yoki Netty ning boshqa major versiyasini talab qilsa, siz versiya urushiga kirasiz.

To'rtinchi: chiqish yo'li. Bir yildan keyin voz kechsangiz, qancha fayl o'zgaradi. Javob "beshdan kam" bo'lishi uchun interface ortiga yashiring.

```java
// Chiqish yo'li: tashqi kutubxona faqat bitta adapter ichida ko'rinadi.
// Domen kodi hech qachon vendor sinfini import qilmaydi.
public interface ToLovShlyuzi {
    ToLovNatijasi toLa(ToLovBuyrugi buyruq);
}

@Component
class StripeToLovShlyuzi implements ToLovShlyuzi {

    private final com.stripe.StripeClient mijoz; // vendor faqat shu yerda

    @Override
    public ToLovNatijasi toLa(ToLovBuyrugi buyruq) {
        try {
            var javob = mijoz.paymentIntents().create(mapQil(buyruq));
            return ToLovNatijasi.muvaffaqiyat(javob.getId());
        } catch (com.stripe.exception.StripeException e) {
            // Vendor exception'i domen xatosiga aylanadi, tashqariga chiqmaydi.
            throw new ToLovXatosi(buyruq.id(), e.getCode(), e);
        }
    }
}
```

Beshinchi: litsenziya, chunki AGPL kutubxonasi yopiq mahsulotga kirmaydi. Oltinchi: xavfsizlik tarixi, ya'ni CVE bo'lganda jamoa qancha kunda patch chiqargan. Yettinchi: kuzatuvchanlik, chunki Micrometer metrikasi bermaydigan kutubxona qora qutiga aylanadi.

### 38.5 Bog'liqlik qo'shishning yashirin narxi va uni yangilash majburiyati

Bog'liqlik qo'shganda siz kod emas, majburiyat olasiz. Har bir jar CVE yuzangizni, build vaqtini, startup vaqtini va yangilash ishini oshiradi.

Raqamlar bilan tushunarli bo'ladi. Oddiy Spring Boot web ilovasi taxminan 50 dan 70 ta jar bilan keladi, har bir yangi starter yana 5 dan 15 ta qo'shadi. 200 jar'dan oshgan ilovada yiliga taxminan 15 dan 30 ta CVE e'tiboringizni so'raydi, va ularning ko'pi sizga tegishli bo'lmasa ham, har birini ko'rib chiqish kerak. Startup ham sekinlashadi: har 50 ta qo'shimcha jar classpath skanerlashga taxminan 100 dan 300 millisekund qo'shadi.

Yangilashni avtomatlashtiring, aks holda u bo'lmaydi.

```yaml
# .github/dependabot.yml
# Maqsad: patch yangilanishlari avtomatik, minor haftalik, major qo'lda.
version: 2
updates:
  - package-ecosystem: maven
    directory: "/"
    schedule:
      interval: weekly
      day: tuesday
    open-pull-requests-limit: 5
    groups:
      # Spring ekotizimi bitta PR bo'lib keladi, aks holda versiya urushi bo'ladi.
      spring:
        patterns: ["org.springframework*", "org.springframework.boot*"]
      test-kutubxonalari:
        patterns: ["org.junit*", "org.mockito*", "org.testcontainers*"]
    ignore:
      # Major yangilanish ADR talab qiladi, bot o'zi ochmaydi.
      - dependency-name: "*"
        update-types: ["version-update:semver-major"]
```

Qoida: bog'liqlik qo'shish PR'ida uchta savolga yozma javob bo'lsin. Qanday muammoni hal qiladi, standart kutubxona bilan necha qatorda hal bo'ladi, kim yangilab turadi.

### 38.6 Moda texnologiyani baholash: qaysi muammoni hal qiladi, sizda u bormi

Har bir moda texnologiya haqiqiy muammoni hal qiladi, lekin odatda sizning muammoyingizni emas. Ikki savoldan boshlang: bu texnologiya qaysi og'riqni yo'q qiladi, va shu og'riq sizning metrikangizda ko'rinadimi.

Kafka'ning haqiqiy kuchi yuqori o'tkazuvchanlik va qayta o'qiladigan log. Agar sizda kuniga 50 ming hodisa bo'lsa, PostgreSQL jadvali va `SELECT ... FOR UPDATE SKIP LOCKED` buni osongina ko'taradi.

```sql
-- PostgreSQL navbat taxminan 2000 msg/s ko'taradi, SKIP LOCKED consumer'larni to'qnashtirmaydi.
CREATE TABLE buyurtma_hodisasi (
    id          bigserial PRIMARY KEY,
    holat       text NOT NULL DEFAULT 'YANGI',
    yuklama     jsonb NOT NULL,
    urinish     int  NOT NULL DEFAULT 0,
    yaratilgan  timestamptz NOT NULL DEFAULT now()
);
-- Faqat ishlanmagan qatorlar indeksda: indeks kichik qoladi.
CREATE INDEX ON buyurtma_hodisasi (id) WHERE holat = 'YANGI';

-- Consumer'ning bitta tsikli.
WITH olingan AS (
    SELECT id FROM buyurtma_hodisasi
    WHERE holat = 'YANGI'
    ORDER BY id
    LIMIT 100
    FOR UPDATE SKIP LOCKED
)
UPDATE buyurtma_hodisasi b SET holat = 'ISHLANMOQDA'
FROM olingan o WHERE b.id = o.id
RETURNING b.id, b.yuklama;
```

Reactive stack uchun ham shu mantiq. WebFlux ko'p ming parallel ulanishda thread tejaydi, lekin Java 21 dan keyin virtual thread shu muammoning katta qismini oddiy blokirovka qiluvchi kod bilan hal qiladi. Agar servisingiz 500 ta parallel so'rovdan oshmasa, reactive sizga faqat debug qiyinchiligini beradi.

Baholashni yozma shaklga soling: muammo, joriy metrika, da'vo, o'lchov rejasi, voz kechish sharti. Agar "joriy metrika" qatori bo'sh bo'lsa, bu moda, muammo emas.

### 38.7 Qurish yoki sotib olish qarori va mezonlari

Bu qarorni "qiziqarli" mezoni bilan emas, uch yillik egalik narxi bilan qiling: boshlang'ich ishlab chiqish, yillik saqlash, navbatchilik yuki, integratsiya va o'rganish vaqti.

Agar komponent sizning raqobat ustunligingiz bo'lsa, o'zingiz quring. To'lov marshrutlash mantig'i, narx hisoblash, ombor rezervatsiya qoidalari shu toifada.

Agar komponent hamma uchun bir xil bo'lsa, tayyorini oling. Autentifikatsiya, email yuborish, PDF generatsiya, log agregatsiya, feature flag. Bu yerda o'zingiz qurish deyarli har doim yo'qotish.

Chegara holat: komponent standart, lekin talablaringiz g'alati. Tayyorini oling, interface ortiga yashiring, g'alati qismni o'zingiz yozing.

| Mezon | Qurish foydasiga | Sotib olish foydasiga |
|---|---|---|
| Biznes farqlovchisi | Ha, mantiq bizga xos | Yo'q, hamma bir xil qiladi |
| Talablarning barqarorligi | Tez o'zgaradi, nazorat kerak | Yillar davomida o'zgarmaydi |
| Jamoa ekspertizasi | Bizda shu sohada chuqur bilim bor | Bilim yo'q, o'rganish 6 oy |
| Ishga tushirish muddati | 3 oy bor | 2 hafta bor |
| Uch yillik narx | Saqlash yillik 0.2 FTE dan kam | Litsenziya ishlab chiqishdan arzon |
| Muvofiqlik talabi | Audit izini o'zimiz nazorat qilamiz | Vendor sertifikatlangan |
| Chiqish narxi | Kod bizda, chiqish shart emas | Adapter ortida, ko'chish mumkin |

### 38.8 Tajriba uchun vaqt ajratish: spike, ichki loyiha, o'lchovli tajriba

Tajribani kayfiyatga qoldirmang, uni sprintga element qilib kiriting. Uch format ishlaydi.

Spike: vaqt chegarasi qat'iy, odatda 2 kundan 3 kungacha. Savol bitta va yozma. Natija kod emas, balki qaror va o'lchov. Spike kodi production'ga kirmasligini oldindan aytib qo'ying.

Ichki loyiha: past xatarli haqiqiy servisda sinash, masalan ichki hisobot generatori. U buzilsa mijoz ko'rmaydi, lekin siz real yuk va real deploy jarayonini ko'rasiz.

O'lchovli tajriba: production'da, lekin trafikning kichik qismida. Yangi kesh strategiyasini 5 foiz so'rovga yoqib, latency taqsimotini solishtirish.

```java
// Spike natijasi raqam bo'lishi kerak, taassurot emas.
// JMH bilan ikki kutubxonani bir xil sharoitda o'lchash.
@BenchmarkMode(Mode.AverageTime)
@OutputTimeUnit(TimeUnit.MICROSECONDS)
@Fork(value = 2, jvmArgs = {"-Xms1g", "-Xmx1g"})
@Warmup(iterations = 5, time = 2)       // JIT qizishi uchun
@Measurement(iterations = 10, time = 5) // o'lchov qismi
@State(Scope.Benchmark)
public class HisobotSerializatsiyaBenchmark {

    private List<HisobotQatori> qatorlar; // 10 000 qator, realga yaqin

    @Setup public void tayyorla() { qatorlar = TestMalumot.hisobot(10_000); }

    @Benchmark public byte[] jackson() throws Exception {
        return jacksonMapper.writeValueAsBytes(qatorlar);
    }

    @Benchmark public byte[] nomzodKutubxona() throws Exception {
        return nomzod.serialize(qatorlar);
    }
}
```

Spike hujjati bir sahifadan oshmasin: savol, usul, o'lchov jadvali, qaror, voz kechish sharti.

### 38.9 Bilimni jamoaga tarqatish: hujjat, suhbat, namuna kod

Bir kishining boshidagi bilim arxitektura xatari. Uni tarqatishning uchta formati ishlaydi.

Birinchi: qisqa qaror yozuvi, har bir muhim qaror uchun bir sahifa. Kontekst, variantlar, tanlangan yo'l, natijalar, voz kechish sharti. `docs/decisions/` papkasida, kod bilan birga versiyalanadi.

Ikkinchi: ichki ko'rsatuv. 30 daqiqa, slayd emas, ekranda tirik kod. Eng yaxshi mavzu "o'tgan haftadagi incident va asl sababi".

Uchinchi va eng kuchlisi: ishlaydigan namuna kod. Jamoa hujjat o'qimaydi, lekin namunani ko'chiradi.

```properties
# docs/namunalar/outbox/application.properties
# Jamoa shu fayldan ko'chiradi, shuning uchun har bir qiymat izohlangan.

# Pool o'lchami: CPU yadrosi * 2 + disk kutish. 4 yadro uchun taxminan 10.
spring.datasource.hikari.maximum-pool-size=10
# Ulanish olish uchun kutish: so'rov timeout'idan kichik bo'lishi shart.
spring.datasource.hikari.connection-timeout=3000
# Ochiq qolgan ulanishni aniqlash: leak bo'lsa log yoziladi.
spring.datasource.hikari.leak-detection-threshold=20000

# Batch insert: outbox yozuvlari to'plam bilan ketadi.
spring.jpa.properties.hibernate.jdbc.batch_size=50
spring.jpa.properties.hibernate.order_inserts=true

# Statement darajasidagi timeout: uzoq so'rov pool'ni band qilmaydi.
spring.jpa.properties.hibernate.jakarta.persistence.query.timeout=5000
```

Namunani CI da test qilib turing: testlanmagan namuna olti oyda eskirib, noto'g'ri bilim tarqatadi.

### 38.10 Xatolardan o'rganishni odat qilish va o'z qarorlarini qayta ko'rish

Incident'dan keyin "kim aybdor" savoli o'rniga "qaysi signal yetishmadi" savolini bering. Birinchi savol odamni yashirishga o'rgatadi, ikkinchisi tizimni yaxshilaydi.

Har bir incident'dan uchta natija chiqsin: muammoni oldin ko'rsatadigan metrika, shu holatni qaytaradigan test, va qaror xato bo'lgan bo'lsa qaror yozuvining yangilangan versiyasi.

Qarorlarni rejali qayta ko'rish odati kam uchraydi, lekin eng qimmatlisi. Har chorakda qaror papkasini oching va har biriga bitta savol bering: bugungi bilim bilan shu qarorni yana qabul qilarmidim.

```bash
# Chorakda bir marta: olti oydan oshgan qarorlarni qayta ko'rishga chiqarish.
cd docs/decisions
for f in *.md; do
  # Fayl oxirgi marta qachon o'zgargan.
  oxirgi=$(git log -1 --format=%ad --date=short -- "$f")
  kun=$(( ( $(date +%s) - $(date -d "$oxirgi" +%s) ) / 86400 ))
  if [ "$kun" -gt 180 ]; then
    holat=$(grep -m1 '^Holat:' "$f" || echo 'Holat: yoq')
    printf '%-45s %4s kun  %s\n' "$f" "$kun" "$holat"
  fi
done | sort -k2 -n -r
```

Shu ro'yxatdan chorakda eng ko'pi bilan uchtasini tanlang. Hammasini qayta ko'rishga urinish rejani o'ldiradi.

### 38.11 Java va Spring ekotizimini kuzatib borish usullari

Maqsad hamma narsani o'qish emas, sizga tegadigan o'zgarishni vaqtida ko'rish.

JDK tomoni. Har yarim yilda feature reliz chiqadi, LTS esa ikki yilda: Java 17, 21 va 25. Har reliz uchun faqat JEP ro'yxatini o'qing, bu 15 daqiqa. Sizga tegadigan JEP bo'lsa, to'liq matnini o'qing.

Yangi JDK ni lokal mashinada sinash bir buyruq ishi.

```bash
# Yangi LTS ni lokal sinash: SDKMAN bilan yonma-yon o'rnatiladi.
sdk install java 25-tem
sdk use java 25-tem

# Deprecated va olib tashlangan API larni kompilyatsiyada ko'rish.
mvn -q clean compile -Dmaven.compiler.release=25 \
    -Dmaven.compiler.showDeprecation=true 2>&1 | grep -i 'deprecat\|removed'

# Reflection va native access ogohlantirishlari: kelgusi relizda xato bo'ladi.
java --illegal-native-access=warn -jar target/app.jar 2>&1 | head -40

# Startup va xotira farqini o'lchash.
/usr/bin/time -f "%e s, %M KB" java -jar target/app.jar --test-start
```

Spring tomoni. Minor relizlar taxminan har olti oyda chiqadi. Faqat migration guide va o'zingiz ishlatadigan modullar o'zgarishini o'qing. Eskirayotgan konfiguratsiyani qo'lda izlamang: `spring-boot-properties-migrator` ni vaqtincha bog'liqlik qilib qo'shsangiz, startup'da eski kalitlarni ro'yxat qilib beradi.

PostgreSQL tomoni. Har yil bitta major reliz. Faqat "Migration to Version X" va planner o'zgarishlarini o'qing. Planner o'zgarishi eng og'ir so'rovlaringizni sekinlashtirishi mumkin, shuning uchun yangilashdan oldin `pg_stat_statements` dan eng qimmat 20 so'rovni saqlab qo'ying va keyin solishtiring.

| Oddiy yondashuv | Arxitektor yondashuvi |
|---|---|
| Blog postdan javob oladi | Reference hujjat va manba kodni o'qiydi |
| Yangi kutubxonani "qiziq" bo'lgani uchun qo'shadi | Yetti mezon bo'yicha yozma baho beradi |
| Bog'liqlikni qo'shib, unutadi | Yangilashni Dependabot guruhlari bilan avtomatlashtiradi |
| Reactive'ga o'tadi, chunki moda | Parallel so'rov sonini o'lchab, virtual thread bilan hal qiladi |
| Hammasini o'zi quradi, chunki shunday qiziqarli | Biznes farqlovchisini quradi, qolganini sotib oladi |
| Vendor sinfini butun kodga sochadi | Vendorni bitta adapter ortiga yashiradi |
| Spike'ni cheksiz davom ettiradi | Spike'ga 3 kun va bitta yozma savol beradi |
| LTS yangilashini oxirgi daqiqada boshlaydi | Yangi JDK ni chiqqan kuni lokal build'da sinaydi |
| Bilimni o'z boshida saqlaydi | Testlanadigan namuna kod va qaror yozuvi qoldiradi |
| Qarorni bir marta qabul qiladi | Har chorakda uchta qarorni qayta ko'rib chiqadi |

| Tuzoq | Yechim |
|---|---|
| Faqat `current` hujjatni o'qish, versiya mos kelmaydi | URL ichida aniq versiyani tanlash odatini qilish |
| Dependabot PR lari to'planib, hech kim ko'rmaydi | Guruhlash, limitni 5 ga qo'yish, haftada bir vaqt ajratish |
| Major yangilashni bot avtomatik ochadi va build sinadi | Major'ni `ignore` ga kiritib, qo'lda ADR bilan qilish |
| Spike kodi production'ga sirg'alib kiradi | Spike'ni alohida branch'da va `-spike` moduli ichida qilish |
| Benchmark JIT qizimasdan o'lchanadi, natija yolg'on | JMH va warmup iteratsiyalari, forklangan JVM |
| Yangi kutubxona Jackson major versiyasini tortadi | `dependency:tree` va enforcer bilan banned versiyani bloklash |
| PostgreSQL major yangilashdan keyin so'rov sekinlashadi | Yangilashdan oldin eng qimmat 20 so'rovni saqlab, solishtirish |
| Namuna kod eskiradi va noto'g'ri bilim tarqatadi | Namunani CI da test qilib turish |

### 38.12 O'z o'rganish rejangizni tuzish: chorak uchun aniq maqsadlar

"Kafka o'rganaman" maqsad emas, u istak. Maqsad uchta qismdan iborat: nima qilaman, qanday isbotlayman, qancha vaqt.

Chorak uchun uchta maqsaddan oshmang. Haftada 3 soat real vaqt chorakda taxminan 36 soat beradi, har maqsadga 12 soat tushadi.

Yaxshi yozilgan maqsad shunday ko'rinadi. "Ombor harakatlari jadvalini oylik partition'ga bo'lish bo'yicha spike qilaman. Isbot: 50 million qatorli test ma'lumotida oylik hisobot so'rovining latency farqini o'lchagan hujjat va qaror yozuvi." Natija ham o'lchanadi, ham ishga tegishli.

Har bir maqsadni joriy og'riqqa bog'lang. Agar eng og'ir incident'laringiz pool to'lishidan bo'lsa, chorak maqsadi connection pool bo'lsin, vector database emas.

Chorak oxirida ikki savol bering: uchta maqsaddan qanchasi isbotlangan natija bilan tugadi, va qaysi biri ishga ta'sir qildi. Birortasi ham tugamagan bo'lsa, muammo rejada emas, vaqt ajratishda.

### 38.13 Amalda qo'llash

- [ ] O'z stack'ingiz uchun "chuqur" va "yuzaki" ro'yxatini yozing: chuqur ro'yxatda 7 dan ko'p element bo'lmasin, va har biri uchun isbotlovchi test bor-yo'qligini belgilang.
- [ ] `mvn dependency:tree` va `mvn help:effective-pom` ni ishga tushirib, 50 dan ortiq jar keltirayotgan starter yoki kutubxonani toping, uning kerakligini PR muhokamasiga qo'ying.
- [ ] `.github/dependabot.yml` faylini guruhlar bilan sozlang, major yangilanishlarni `ignore` ga kiritib, haftada bir marta 30 daqiqalik "yangilash oynasi" ni kalendarga qo'ying.
- [ ] Eng ko'p ishlatiladigan uchta tashqi kutubxona uchun chiqish yo'lini tekshiring: vendor sinfi nechta faylda import qilinganini `grep` bilan sanab, 5 dan ko'p bo'lsa adapter kiritishni rejaga qo'ying.
- [ ] Keyingi spike'ni 3 kunlik vaqt chegarasi va bitta yozma savol bilan sprintga element qilib kiritib, natijani JMH yoki `pg_stat_statements` raqami bilan hujjatlashtiring.
- [ ] `docs/decisions/` papkasini yarating yoki tartibga soling, olti oydan oshgan qarorlarni skript bilan ro'yxat qilib, ulardan uchtasini bu chorakda qayta ko'rishga belgilang.
- [ ] Joriy LTS'dan keyingi JDK ni SDKMAN bilan o'rnatib, loyihani shu versiyada kompilyatsiya qiling, deprecated va native access ogohlantirishlarini issue sifatida yozib qo'ying.
- [ ] Chorak uchun uchta o'rganish maqsadini yozing, har biriga o'lchanadigan isbot va 12 soatlik budjet qo'yib, ularni joriy incident ro'yxatidagi og'riq bilan bog'lang.

## 39. Birinchi 90 kun va o'z-o'zini baholash (First 90 Days and Self-Assessment)

Arxitektor yangi tizimga kelganda eng katta xatosi tezda foydali bo'lishga urinishdir. Haqiqatda esa birinchi uch oyda sizning asosiy mahsulotingiz kod emas, balki ishonchli xarita va ishonchli munosabatdir. Bu bob shu uch oyni haftalab bo'lib beradi, keyin esa diqqatni sizning o'zingizga qaratadi: bilimingizdagi bo'shliqni qanday topish va qaysi mavzuda qay darajada turganingizni qanday o'lchash. Hujjat shu bob bilan tugaydi, shuning uchun oxirida uchlikni birgalikda qanday ishlatish ham aytiladi.

### 39.1 Yangi loyihada birinchi hafta: nimani o'qish, kimdan so'rash, nima yozmaslik

Birinchi haftada kod yozmaslik qoidasi mavhum maslahat emas, u aniq hisob. Siz hali tizimning tranzaksiya chegaralarini, idempotentlik shartlarini va deploy jarayonini bilmaysiz. Shu holatda yozilgan har bir patch texnik qarz ishlab chiqaradi, uni esa keyin siz o'zingiz tozalaysiz.

O'qish tartibi quyidagicha bo'lsin. Avval deploy pipeline va runbook, chunki ular tizim qanday yashayotganini ko'rsatadi. Keyin ma'lumotlar bazasi migratsiyalari tarixi, chunki Flyway yoki Liquibase papkasi tizim evolyutsiyasining eng rost yilnomasi. Undan keyin eng ko'p o'zgargan sinflar, keyin esa incident tarixi.

```bash
# Eng ko'p tegilgan fayllar: shu yerda biznes murakkabligi to'plangan
git log --since="12 months ago" --name-only --pretty=format: \
  | grep -E '\.java$' | sort | uniq -c | sort -rn | head -30

# Tranzaksiya chegaralari qayerda e'lon qilingan
grep -rn "@Transactional" --include=*.java src/main/java | wc -l
grep -rln "@Transactional" --include=*.java src/main/java | head -20

# Migratsiya tarixi: tizim qanday o'sgani shu yerda ko'rinadi
ls -1 src/main/resources/db/migration | tail -25

# Tashqi integratsiyalar: har bir URL bu sizning SLA qaramligingiz
grep -rnE "https?://" src/main/resources/application*.y*ml | head -20
```

So'rash kerak bo'lgan odamlar ro'yxati qisqa. Birinchisi tungi chaqiruvlarga javob beradigan dejur injener, chunki u tizimning haqiqiy zaif joyini biladi. Ikkinchisi eng ko'p commit qilgan developer, uchinchisi mahsulot egasi. Dejurdan bitta savol so'rang: oxirgi uch oyda sizni nima uyqudan uyg'otdi. Bu savol odatda arxitektura muammosining aniq manzilini beradi.

Yozmaslik kerak bo'lgan narsalar ham aniq. Katta refactoring, yangi framework taklifi, va "biz buni hammasini qayta yozamiz" degan gap. Bu uchtasi birinchi haftada ishonchni eng tez yo'qotadigan harakatlardir.

### 39.2 Birinchi oy: tizim xaritasini chizish va og'riqli nuqtalarni ro'yxatlash

Birinchi oyning natijasi ikkita artefakt bo'lishi kerak: tizim xaritasi va og'riqli nuqtalar ro'yxati. Xarita chiroyli diagramma emas, u javob beradigan hujjat. Har bir servis uchun uchta narsa yozilsin: qaysi ma'lumotning egasi, qaysi tashqi tizimga sinxron bog'langan, va u o'chsa nima ishlamay qoladi.

Og'riqli nuqtalarni taxmin bilan emas, o'lchov bilan toping. PostgreSQL tarafida `pg_stat_statements` sizga bir kunda haqiqatni ko'rsatadi.

```sql
-- Umumiy vaqtni eng ko'p yeyayotgan so'rovlar: optimizatsiya navbati shu
SELECT substring(query, 1, 80) AS so_rov,
       calls,
       round(total_exec_time)       AS jami_ms,
       round(mean_exec_time, 2)     AS o_rtacha_ms,
       rows / GREATEST(calls, 1)    AS qator_per_call
FROM pg_stat_statements
ORDER BY total_exec_time DESC
LIMIT 20;

-- Sequential scan ko'p bo'lgan jadvallar: index yetishmasligi belgisi
SELECT relname, seq_scan, seq_tup_read, idx_scan,
       n_live_tup, n_dead_tup
FROM pg_stat_user_tables
WHERE seq_scan > 1000
ORDER BY seq_tup_read DESC
LIMIT 15;

-- Ishlatilmayotgan indexlar: yozish tezligini bekorga yeydi
SELECT relname, indexrelname, idx_scan, pg_size_pretty(pg_relation_size(indexrelid))
FROM pg_stat_user_indexes
WHERE idx_scan < 50
ORDER BY pg_relation_size(indexrelid) DESC
LIMIT 15;
```

Ro'yxatni tartiblashda ikkita o'qdan foydalaning: biznesga ta'siri va tuzatish narxi. Yuqori ta'sir va past narx bo'lgan bandlar ikkinchi oyning ishi bo'ladi. Yuqori ta'sir va yuqori narx bo'lganlar uchinchi oydagi rejaga tushadi. Past ta'sirli bandlarni umuman yozib qo'ying, ularga tegmang.

Shu oyda yana bitta o'lchov oling: p99 latency va connection pool to'yinganligi. Ko'p tizimda muammo so'rov sekinligida emas, pool navbatida turadi. Agar HikariCP `pending` metrikasi nolga teng bo'lmasa, siz o'lchovni topdingiz.

### 39.3 Ikkinchi oy: kichik, ko'rinadigan yaxshilanish bilan ishonch qozonish

Ikkinchi oyda bitta qoida bor: natija o'lchanadigan va bir hafta ichida ko'rinadigan bo'lsin. Yaxshi nomzodlar ro'yxati qisqa. Yetishmayotgan timeout qo'yish, bitta og'ir hisobot so'roviga index qo'shish, HikariCP pool o'lchamini to'g'rilash, va metrikani chiqarish.

Timeout eng arzon va eng ta'sirli yaxshilanishdir. Ko'p tizimda to'lov provayderiga chaqiruv timeout'siz turadi, shuning uchun provayder sekinlashganda butun thread pool to'lib qoladi.

```properties
# To'lov provayderiga chiqadigan HTTP chaqiruvlar: cheksiz kutish taqiqlanadi
payment.client.connect-timeout=2s
payment.client.read-timeout=4s

# So'rov darajasidagi himoya: bitta so'rov butun poolni ushlab turmaydi
spring.datasource.hikari.maximum-pool-size=20
spring.datasource.hikari.connection-timeout=3000
spring.datasource.hikari.validation-timeout=1000
spring.datasource.hikari.leak-detection-threshold=20000

# PostgreSQL tarafidan kafolat: osilgan so'rov o'zi uziladi
spring.jpa.properties.jakarta.persistence.query.timeout=5000
spring.datasource.hikari.data-source-properties.options=-c statement_timeout=5000 -c idle_in_transaction_session_timeout=10000

# Metrika: pool navbati ko'rinmasa, muammo ham ko'rinmaydi
management.endpoints.web.exposure.include=health,metrics,prometheus
management.metrics.tags.application=order-service
```

Pool o'lchamini tanlashda hisobni ko'rsatib bering. Agar o'rtacha so'rov bazada 5 ms turadigan bo'lsa, 20 ta connection nazariy jihatdan sekundda taxminan 4000 ta so'rovga yetadi. Shuning uchun 100 ta connection so'rash deyarli har doim xato bo'ladi, u faqat PostgreSQL tarafidagi raqobatni oshiradi.

Ko'rinadigan yaxshilanishni e'lon qilish usuli ham muhim. Oldingi va keyingi raqamni bitta jadvalda bering: p99 480 ms dan 120 ms ga tushdi, pool `pending` o'rtacha 7 dan 0 ga tushdi. Raqam bilan aytilgan natija sizga keyingi oyda kattaroq o'zgarish uchun ruxsat ochadi.

### 39.4 Uchinchi oy: o'rta muddatli reja taklif qilish va kelishib olish

Uchinchi oyda siz endi taklif qilish huquqini qozondingiz. Reja uch oydan olti oyga mo'ljallangan bo'lsin, undan uzoqroq reja ishonchni emas, shubhani keltiradi. Rejada har bir bandning uchta ustuni bo'lsin: qanday o'lchovni yaxshilaydi, qancha ishchi hafta oladi, va qanday risk tug'diradi.

Rejani yozishda eng kuchli vosita alternativani ham ko'rsatishdir. Masalan ombor qoldig'i servisini ajratish taklifida ikkinchi variant sifatida bitta bazada schema ajratishni ham bering. Bu sizni "o'z g'oyasini himoya qiladigan odam" emas, "qarorni ochib beradigan odam" qilib ko'rsatadi.

Kelishib olishning amaliy shakli qisqa qaror hujjati. Bir sahifada kontekst, variantlar, tanlangan yo'l, va natijalar. Shu hujjatni jamoa bilan o'qib chiqing, keyin uni repozitoriyga qo'ying. Og'zaki kelishuv yo'qoladi, yozilgani qoladi.

| Masala | Oddiy yondashuv | Arxitektor yondashuvi |
|---|---|---|
| Birinchi hafta | Darhol task olib kod yozadi | Deploy, migratsiya va incident tarixini o'qiydi |
| Muammoni topish | "Kod eski" deb umumlashtiradi | `pg_stat_statements` va pool metrikasi bilan o'lchaydi |
| Birinchi taklif | Katta refactoring taklif qiladi | Timeout va index kabi arzon yutuqni beradi |
| Natijani e'lon qilish | "Tezlashdi" deb aytadi | p99 480 ms dan 120 ms ga tushdi deb ko'rsatadi |
| Mavjud qarorga munosabat | "Buni kim shunday qildi" deb so'raydi | "Qanday sharoitda shunday to'g'ri edi" deb so'raydi |
| Reja ufqi | Ikki yillik maqsadni chizadi | Uch oylik o'lchanadigan bandlarni beradi |
| Alternativa | Bitta yo'lni himoya qiladi | Ikki yo'lni va tanlash mezonini beradi |
| Kelishuv shakli | Majlisda og'zaki tasdiqlaydi | Bir sahifali qaror hujjatini repozitoriyga qo'yadi |
| O'z bilimi | "Bilaman" deb o'tadi | Savol ro'yxati bilan o'zini tekshiradi |
| Jamoaga ta'sir | Qaror markazida o'zi turadi | Jamoa qaror qabul qiladigan mezonni qoldiradi |

### 39.5 Mavjud qarorlarni hurmat qilish: "nega shunday qilingan" savolini birinchi berish

Har bir g'alati kod bir paytda to'g'ri javob bo'lgan. Hisobotda denormalizatsiya qilingan jadval bo'lsa, ehtimol o'sha paytda hisobot 40 sekund ishlagan va mijoz ketib qolgan. Native SQL yozilgan joy bo'lsa, ehtimol Hibernate generatsiya qilgan so'rov planner tomonidan noto'g'ri bajarilgan.

Shu sababli birinchi savol bitta bo'lsin: qanday cheklov ostida bu qaror oqilona edi. Bu savol sizga ko'rinmagan cheklovni beradi, muallifni esa himoyaga o'tishga majburlamaydi.

Amalda bu `git log` bilan ishlashni bildiradi. Commit xabari, bog'langan ticket, va o'sha davrdagi incident bir-biriga ulanadi.

```bash
# Shubhali fayl qanday paydo bo'lgan: qator bo'yicha tarix
git log -L 40,80:src/main/java/com/shop/report/SalesReportDao.java --oneline

# Shu qator qaysi commitda yozilgan va xabari nima edi
git blame -L 40,80 src/main/java/com/shop/report/SalesReportDao.java

# O'sha commit atrofida yana nima o'zgardi: kontekst shu yerda
git show --stat <commit-sha>

# Ticket raqamlarini yig'ish: qaror sababi ko'pincha ticketda
git log --since="2 years ago" --grep="report" --oneline | head -20
```

Agar sabab topilmasa, qarorni "noto'g'ri" deb emas, "sababi hujjatlashtirilmagan" deb belgilang. Keyin o'zgartirishdan oldin sababni qayta tiklang. Bu tartib sizni eng qimmat xatodan saqlaydi: ko'rinmas talabni buzishdan.

### 39.6 O'z bilimingizdagi bo'shliqni topish uchun o'z-o'zini tekshirish ro'yxati

Bilimdagi bo'shliqni topishning eng ishonchli usuli javobni emas, tushuntirishni talab qilishdir. Agar siz mexanikani oq doskada ikki daqiqada chizib bera olmasangiz, siz bu mavzuni bilmaysiz, faqat tanib olasiz.

Tekshirishni haftada bir marta, bitta mavzuda o'tkazing. Har savol uchun uchta javob variantidan birini belgilang: chizib tushuntiraman, taniyman lekin tushuntirmayman, bilmayman. Ikkinchi variant eng xavfli, chunki u o'zini bilim deb ko'rsatadi.

| Tuzoq | Yechim |
|---|---|
| Hammasini bir vaqtda o'rganishga urinish | Haftada bitta mavzu, ikki daqiqalik tushuntirish mashqi |
| Javobni eslab qolishni bilim deb hisoblash | Oq doskada mexanikani chizishni talab qilish |
| Faqat kuchli mavzuni takrorlash | Zaif ustunni jadvaldan tanlab, shunga vaqt berish |
| Nazariyani amaliyotsiz o'qish | Har mavzuni real loyihadagi bitta muammoga ulash |
| Darajani o'zi baholab oshirib qo'yish | Jamoadagi bitta odamga tushuntirib, savolini eshitish |
| Bo'shliqni yozib qo'ymaslik | Ro'yxatni repozitoriyda saqlash va oyda bir qayta ko'rish |

### 39.7 Yetuklik darajalari: qaysi mavzuda qay darajada turibsiz

Daraja o'zini maqtash uchun emas, vaqtni to'g'ri taqsimlash uchun kerak. Pastki jadvalda har bir mavzu uchun uchta daraja bor. O'zingizni rost joylashtiring, keyin eng past ustunlardan ikkitasini tanlab, keyingi choraklik o'rganish rejangizni shundan quring.

| Mavzu | Boshlang'ich | O'rta | Yuqori |
|---|---|---|---|
| JVM xotira | Heap va stack farqini biladi | GC log o'qiydi, pause sababini topadi | Region o'lchami va allocation rate bo'yicha sozlaydi |
| Concurrency | `synchronized` ishlatadi | Thread pool o'lchamini hisoblab beradi | Virtual thread va blocking chegarasini loyihalaydi |
| Spring konteyner | Bean e'lon qiladi | Proxy va self-invocation tuzog'ini biladi | Lifecycle va startup vaqtini boshqaradi |
| Tranzaksiya | `@Transactional` qo'yadi | Propagation va isolation tanlaydi | Flush, lock va retry siyosatini loyihalaydi |
| Hibernate | Entity yozadi | N+1 ni topib tuzatadi | Fetch strategiyasi va cache chegarasini belgilaydi |
| PostgreSQL planner | `EXPLAIN` chaqiradi | `EXPLAIN ANALYZE BUFFERS` o'qiydi | Statistika va index turini qarorga aylantiradi |
| Index dizayni | B-tree qo'yadi | Composite tartibini to'g'ri beradi | Partial, GIN va covering index tanlaydi |
| API dizayni | REST endpoint yozadi | Versiyalash va xato formatini belgilaydi | Mos keluvchanlik shartnomasini boshqaradi |
| Observability | Log yozadi | Metrika va alert qo'yadi | SLO va xato budjetini belgilaydi |
| Deploy | Pipeline ishlatadi | Migratsiyani mos keluvchan yozadi | Nol to'xtovli relizni loyihalaydi |
| Xavfsizlik | Autentifikatsiya yoqadi | Avtorizatsiya chegarasini tekshiradi | Sir boshqaruvi va audit izini quradi |
| Qaror yuritish | Fikrini aytadi | Variantlarni taqqoslaydi | Mezon va qaytarish yo'lini yozib qoldiradi |

### 39.8 Fikrlash va qarorlar bilimini o'zingizga qo'llash

Fikrlash va qarorlar qismidagi vositalar faqat tizimga emas, sizning karyerangizga ham tegishli. Qaytarib bo'lmaydigan qarorni sekin qabul qilish qoidasi sizning o'zingizga ham tegadi. Masalan yangi texnologiyaga butun jamoani ko'chirish qaytarib bo'lmaydigan qarordir, uni bitta servisda sinab ko'rish esa qaytariladi.

Xato budjeti tushunchasini o'z o'rganishingizga ham qo'llang. Chorakda ikkita yangi mavzuni chuqur o'rganish realistik budjet, beshta mavzu esa yuzaki natija beradi. Ikkinchi tartibli ta'sir haqida o'ylash qoidasi ham shu yerda ishlaydi: siz tanlagan texnologiya jamoaning uch yildan keyingi ishga olish imkoniyatini belgilaydi.

Eng muhimi esa qarorni yozib qoldirish odati. O'zingiz uchun qisqa jurnal yuritib boring: qanday qaror qabul qildim, qanday kutgandim, nima bo'ldi. Olti oydan keyin shu jurnal sizning eng kuchli o'qituvchingiz bo'ladi.

### 39.9 Java va JVM: o'zingizni sinash savollari

Quyidagi savollarga oq doskada javob bera olasizmi. Heap'dagi obyekt qachon eski avlodga o'tadi va bu pause vaqtiga qanday ta'sir qiladi. Thread pool o'lchamini CPU ga bog'liq va IO ga bog'liq ish uchun qanday hisoblaysiz. Virtual thread blocking chaqiruvni qanday kutadi va qaysi holatda u foyda bermaydi.

Yana bir sinov: diagnostikani buyruq bilan ko'rsatib bera olasizmi.

```bash
# JVM xotira holati: eski avlod to'lib borayotganini shu ko'rsatadi
jcmd <pid> GC.heap_info

# Thread holati: qancha thread BLOCKED yoki WAITING turibdi
jcmd <pid> Thread.print | grep -c "java.lang.Thread.State: BLOCKED"

# Eng ko'p xotira yeyayotgan sinflar: leak izlashning birinchi qadami
jcmd <pid> GC.class_histogram | head -15

# Native xotira: heap tashqarisidagi o'sish shu yerda ko'rinadi
jcmd <pid> VM.native_memory summary
```

Buyruqni eslamaslik xato emas. Lekin "native xotira heap tashqarisida o'sishi mumkin" degan mexanikani bilmaslik bo'shliqdir.

### 39.10 Spring: o'zingizni sinash savollari

Birinchi savol klassik: nega bitta sinf ichidagi metod chaqiruvi `@Transactional` ni ishga tushirmaydi. Javobda proxy so'zi bo'lishi kerak, chunki chaqiruv proxy orqali o'tmaydi.

```java
@Service
public class OrderService {

    // BU USUL ISHLAMAYDI: ichki chaqiruv proxy orqali o'tmaydi,
    // shuning uchun tranzaksiya ochilmaydi
    public void placeOrder(OrderRequest req) {
        validate(req);
        saveOrder(req);   // @Transactional kuchga kirmaydi
    }

    @Transactional
    public void saveOrder(OrderRequest req) {
        orderRepository.save(req.toEntity());
    }
}
```

Ikkinchi savol: `@Transactional` metod ichida tashqi to'lov provayderiga sinxron HTTP chaqiruv qilish nima uchun xavfli. Javob ikkita qismdan iborat: baza connection'i kutish vaqtida band turadi, va provayder javobi noaniq bo'lsa tranzaksiya natijasi ham noaniq bo'ladi.

Uchinchi savol: Spring Boot 3.x da startup vaqtini nima sekinlashtiradi va buni qanday o'lchaysiz. To'rtinchi savol: `@Async` ishlatilganda tranzaksiya konteksti nima bo'ladi. Beshinchi savol: ikkita bean bir xil turga ega bo'lsa, konteyner qanday tanlaydi va siz buni qanday boshqarasiz.

### 39.11 PostgreSQL: o'zingizni sinash savollari

Birinchi savol: planner nega index bor bo'lsa ham sequential scan tanlaydi. Javobda tanlanuvchanlik va statistika bo'lishi kerak, chunki ko'p qator qaytaradigan so'rov uchun scan arzonroq.

```sql
-- Bu rejani o'qib, muammoni ayta olasizmi
EXPLAIN (ANALYZE, BUFFERS, COSTS)
SELECT o.id, o.total, c.name
FROM orders o
JOIN customers c ON c.id = o.customer_id
WHERE o.created_at >= now() - interval '7 days'
  AND o.status = 'PAID'
ORDER BY o.created_at DESC
LIMIT 50;

-- Savol 1: rows=... va actual rows=... orasida 100 barobar farq bo'lsa nima qilasiz
-- Savol 2: shared read ko'p, shared hit kam bo'lsa bu nimani bildiradi
-- Savol 3: shu so'rov uchun qanday composite index yozasiz va ustun tartibi nega shunday
-- Savol 4: Sort tugunida "external merge Disk" chiqsa, qaysi parametrni ko'rasiz
```

Qolgan savollar: `REPEATABLE READ` va `SERIALIZABLE` orasidagi farq amalda qanday ko'rinadi. Uzun ochiq tranzaksiya nega `VACUUM` ishini buzadi. `FOR UPDATE SKIP LOCKED` navbat ishlashida nima beradi. Katta jadvalga yangi ustun qo'shish qachon jadvalni bloklaydi va qachon bloklamaydi.

### 39.12 Operatsion tayyorlik: o'zingizni sinash savollari

Bu bo'lim ko'pincha chetda qoladi, lekin tungi chaqiruvda faqat shu bilim ishlaydi. Birinchi savol: tizimingizda bitta so'rov bo'ylab trace ID uzilmasdan o'tadimi. Ikkinchi savol: eng muhim uchta alert qanday o'lchovga asoslangan va ularning yolg'on signal darajasi qancha.

```yaml
# Minimal operatsion tayyorlik: shu uchtasi bo'lmasa, tizim ko'r
management:
  endpoint:
    health:
      probes:
        enabled: true          # liveness va readiness ajratilgan
  health:
    livenessstate:
      enabled: true
    readinessstate:
      enabled: true
  tracing:
    sampling:
      probability: 0.1         # yuqori trafikda 10 foiz yetadi
  metrics:
    distribution:
      percentiles-histogram:
        http.server.requests: true   # p99 ni serverda hisoblash uchun
```

Uchinchi savol: oxirgi migratsiyani orqaga qaytarish rejasi bormi va u sinalganmi. To'rtinchi savol: ma'lumotlar bazasidan tiklanish vaqti qancha va bu raqam o'lchanganmi yoki taxminmi. Beshinchi savol: to'lov provayderi 30 sekund javob bermasa, tizimingiz qanday yomonlashadi. Agar bu beshta savolga raqam bilan javob bera olsangiz, siz operatsion jihatdan tayyorsiz.

### 39.13 Keyingi qadam: shu hujjatni va qolgan ikki hujjatni qanday ishlatish

Uchlik bitta maqsadga xizmat qiladi, lekin uchta turli paytda ishlatiladi. Bu hujjat qaror paytida ochiladi: nima uchun shunday bo'ladi va qanday raqam bilan tanlanadi. Dizayn patternlar hujjati loyihalash paytida ochiladi, chunki u shaklni beradi. Testlash qo'llanmasi esa ishonchni tekshirish paytida ochiladi.

Amaliy tartib shunday bo'lsin. Yangi talab kelganda avval bu hujjatdan tegishli mexanika bobini o'qing, chunki qaror cheklovdan chiqadi. Keyin dizayn patternlar hujjatidan shaklni tanlang, masalan tashqi tizimga ishonchli xabar yuborish uchun outbox pattern. Undan keyin testlash qo'llanmasidagi contract testing va Testcontainers bo'limlaridan tekshirish rejasini oling.

Jamoada ishlatishning eng yaxshi usuli esa birgalikda o'qishdir. Haftada bitta bob tanlang, uni ikki kishi o'qib chiqsin, keyin 30 daqiqada jamoaga o'z tizimingiz misolida tushuntirsin. Shu tartib bilim tarqalishini tezlashtiradi, va eng muhimi, u hujjatni o'lik matndan jamoa tiliga aylantiradi.

Oxirgi gap sizning o'zingiz haqida. Arxitektor bo'lish bilim miqdorida emas, qarorning sababini ko'rsatib bera olishda. Agar siz har bir qarorni cheklov, variant va o'lchov bilan tushuntirsangiz, jamoa sizdan keyin ham to'g'ri qaror qabul qilishni davom etadi. Shu esa bu hujjatning asl maqsadi edi.

### 39.14 Amalda qo'llash

- [ ] Birinchi haftada deploy pipeline, migratsiya tarixi va oxirgi uchta incident hisobotini o'qib, dejur injenerga "sizni nima uyg'otdi" savolini bering.
- [ ] `pg_stat_statements` va `pg_stat_user_tables` dan top 20 og'ir so'rov va yetishmayotgan index ro'yxatini chiqarib, biznesga ta'siri bo'yicha tartiblang.
- [ ] Barcha tashqi HTTP chaqiruvlarga connect va read timeout qo'yib, `statement_timeout` va `idle_in_transaction_session_timeout` ni yoqing.
- [ ] HikariCP pool o'lchamini so'rov davomiyligi hisobi bilan qayta belgilab, `pending` metrikasini dashboardga chiqaring.
- [ ] Ikkinchi oyda bitta ko'rinadigan yaxshilanishni oldingi va keyingi p99 raqami bilan e'lon qiling.
- [ ] Uchinchi oyda bir sahifali qaror hujjatini yozib, ichida ikkita variant, tanlash mezoni va qaytarish yo'lini bering.
- [ ] Yetuklik matritsasidan o'zingizga eng past ikkita mavzuni tanlab, chorakka faqat shu ikkitasini rejalashtiring.
- [ ] Shu bobdagi sinov savollaridan o'tib, "taniyman lekin tushuntirmayman" deb belgilangan har bir mavzuni jamoaga 30 daqiqada tushuntirib bering.
