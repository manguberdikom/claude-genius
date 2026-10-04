# Java Spring loyihasida testlash: arxitektor uchun to'liq qo'llanma

Bu qo'llanma Java va Spring loyihasida testlashni boshdan oxir qamrab oladi: sifat strategiyasi, testrovshikning kundalik ish jarayoni, unit va integratsion test yozish, contract testing, test ma'lumotlari, CI/CD pipeline, metrikalar va shablonlar. 18 bob, 239 bo'lim.

Qo'llanma kimga: arxitektor, tech lead, QA lead, backend developer va automation muhandisi.

Har bir bob oxirida `Arxitektor nazorat ro'yxati` bor: loyihada darhol tekshirish mumkin bo'lgan amaliy bandlar.

## Mundarija

**[1. Sifat strategiyasi va arxitektorning roli](#1-sifat-strategiyasi-va-arxitektorning-roli-quality-strategy--the-architects-role)**

- [1.1 Testlash maqsadi: qaror uchun ishonch](#11-testlash-maqsadi-qaror-uchun-ishonch)
- [1.2 Shift-left va shift-right](#12-shift-left-va-shift-right)
- [1.3 Risk-ga asoslangan testlash](#13-risk-ga-asoslangan-testlash)
- [1.4 Test strategiyasi hujjati](#14-test-strategiyasi-hujjati)
- [1.5 Sifat darvozalari va Definition of Done](#15-sifat-darvozalari-va-definition-of-done)
- [1.6 Testability'ni arxitektura talabiga aylantirish](#16-testabilityni-arxitektura-talabiga-aylantirish)
- [1.7 Testlash xarajati va qiymati balansi](#17-testlash-xarajati-va-qiymati-balansi)
- [1.8 Arxitektorning aniq vazifalari](#18-arxitektorning-aniq-vazifalari)
- [1.9 Arxitektor nazorat ro'yxati](#19-arxitektor-nazorat-royxati)

**[2. Test piramidasi va test turlari xaritasi](#2-test-piramidasi-va-test-turlari-xaritasi-test-pyramid--the-map-of-test-types)**

- [2.1 Klassik test piramidasi (Cohn)](#21-klassik-test-piramidasi-cohn)
- [2.2 Zamonaviy variantlar: Testing Trophy, Honeycomb, Test Diamond](#22-zamonaviy-variantlar-testing-trophy-honeycomb-test-diamond)
- [2.3 Teskari piramida (ice-cream cone) anti-patterni](#23-teskari-piramida-ice-cream-cone-anti-patterni)
- [2.4 Test turlari to'liq xaritasi](#24-test-turlari-toliq-xaritasi)
- [2.5 Qaysi mantiqni qaysi darajada testlash kerak](#25-qaysi-mantiqni-qaysi-darajada-testlash-kerak)
- [2.6 Test duplication: bir xil narsani ikki darajada testlash](#26-test-duplication-bir-xil-narsani-ikki-darajada-testlash)
- [2.7 Microservice va modular monolit uchun test taqsimoti namunasi](#27-microservice-va-modular-monolit-uchun-test-taqsimoti-namunasi)
- [2.8 Test nomlash va joylashtirish konvensiyasi](#28-test-nomlash-va-joylashtirish-konvensiyasi)
- [2.9 Arxitektor nazorat ro'yxati](#29-arxitektor-nazorat-royxati)

**[3. Kim nima yozadi: rollar va mas'uliyat](#3-kim-nima-yozadi-rollar-va-masuliyat-who-writes-what--roles--responsibilities)**

- [3.1 Rollar ta'rifi va farqi](#31-rollar-tarifi-va-farqi)
- [3.2 Mas'uliyat matritsasi (RACI)](#32-masuliyat-matritsasi-raci)
- [3.3 "Developer unit test yozadi, QA E2E yozadi" qoidasining chegaralari](#33-developer-unit-test-yozadi-qa-e2e-yozadi-qoidasining-chegaralari)
- [3.4 Three Amigos va Example Mapping](#34-three-amigos-va-example-mapping)
- [3.5 QA'ning sprint ichidagi joyi](#35-qaning-sprint-ichidagi-joyi)
- [3.6 Test kodini code review qilish](#36-test-kodini-code-review-qilish)
- [3.7 Jamoa modellari](#37-jamoa-modellari)
- [3.8 Test ownership](#38-test-ownership)
- [3.9 1 QA va 5 developer: kichik jamoa uchun amaliy model](#39-1-qa-va-5-developer-kichik-jamoa-uchun-amaliy-model)
- [3.10 Arxitektor nazorat ro'yxati](#310-arxitektor-nazorat-royxati)

**[4. Testrovshik qanday ishlashi kerak: QA ish jarayoni](#4-testrovshik-qanday-ishlashi-kerak-qa-ish-jarayoni-how-a-tester-actually-works--the-qa-workflow)**

- [4.1 QA'ning ish oqimi va sprint ritmi](#41-qaning-ish-oqimi-va-sprint-ritmi)
- [4.2 Talablarni testlash](#42-talablarni-testlash)
- [4.3 Test dizayn texnikalari](#43-test-dizayn-texnikalari)
- [4.4 Test case yozish](#44-test-case-yozish)
- [4.5 Exploratory testing](#45-exploratory-testing)
- [4.6 Defekt hisoboti standarti](#46-defekt-hisoboti-standarti)
- [4.7 Defekt hayot aylanishi va triage](#47-defekt-hayot-aylanishi-va-triage)
- [4.8 Regressiya testlash](#48-regressiya-testlash)
- [4.9 Muhitlar (environments)](#49-muhitlar-environments)
- [4.10 Qo'lda testlashdan avtomatlashtirishga o'tish mezonlari](#410-qolda-testlashdan-avtomatlashtirishga-otish-mezonlari)
- [4.11 QA ishini o'lchash](#411-qa-ishini-olchash)
- [4.12 Arxitektor nazorat ro'yxati](#412-arxitektor-nazorat-royxati)

**[5. Unit test: asoslar, qoidalar va JUnit 5](#5-unit-test-asoslar-qoidalar-va-junit-5-unit-testing--foundations-rules--junit-5)**

- [5.1 Unit test nima va nima emas](#51-unit-test-nima-va-nima-emas)
- [5.2 FIRST printsiplari](#52-first-printsiplari)
- [5.3 Arrange-Act-Assert va test nomlash](#53-arrange-act-assert-va-test-nomlash)
- [5.4 JUnit 5 asoslari: lifecycle va tuzilma](#54-junit-5-asoslari-lifecycle-va-tuzilma)
- [5.5 Parametrlashtirilgan testlar](#55-parametrlashtirilgan-testlar)
- [5.6 AssertJ bilan tasdiqlash](#56-assertj-bilan-tasdiqlash)
- [5.7 Mockito bilan test double'lar](#57-mockito-bilan-test-doublelar)
- [5.8 Over-mocking muammosi va fake'lar](#58-over-mocking-muammosi-va-fakelar)
- [5.9 Istisno, chegara holatlari va null-safety](#59-istisno-chegara-holatlari-va-null-safety)
- [5.10 Vaqt, tasodif va UUID'ni testlash](#510-vaqt-tasodif-va-uuidni-testlash)
- [5.11 Property-based testing: jqwik](#511-property-based-testing-jqwik)
- [5.12 Mutation testing bilan sifatni o'lchash (PIT)](#512-mutation-testing-bilan-sifatni-olchash-pit)
- [5.13 Unit test anti-patternlari](#513-unit-test-anti-patternlari)
- [5.14 Arxitektor nazorat ro'yxati](#514-arxitektor-nazorat-royxati)

**[6. Unit test Spring loyihasida: kontekstsiz testlash](#6-unit-test-spring-loyihasida-kontekstsiz-testlash-unit-testing-in-a-spring-project)**

- [6.1 Nega @SpringBootTest unit test uchun noto'g'ri tanlov](#61-nega-springboottest-unit-test-uchun-notogri-tanlov)
- [6.2 Constructor injection — testlanadigan dizayn asosi](#62-constructor-injection--testlanadigan-dizayn-asosi)
- [6.3 Qaysi sinflar Spring kontekstisiz testlanadi](#63-qaysi-sinflar-spring-kontekstisiz-testlanadi)
- [6.4 Service qatlamini mock repository bilan testlash](#64-service-qatlamini-mock-repository-bilan-testlash)
- [6.5 Mapper va DTO konvertorlarni testlash](#65-mapper-va-dto-konvertorlarni-testlash)
- [6.6 Validatsiyani Spring kontekstisiz testlash](#66-validatsiyani-spring-kontekstisiz-testlash)
- [6.7 Domain event va aggregate'ni testlash](#67-domain-event-va-aggregateni-testlash)
- [6.8 Konfiguratsiya va @ConfigurationProperties: ApplicationContextRunner](#68-konfiguratsiya-va-configurationproperties-applicationcontextrunner)
- [6.9 AOP va proxy: unit testda ushlab bo'lmaydigan xatti-harakat](#69-aop-va-proxy-unit-testda-ushlab-bolmaydigan-xatti-harakat)
- [6.10 Spring'ga bog'liqlikni kamaytiruvchi arxitektura qarorlari](#610-springga-bogliqlikni-kamaytiruvchi-arxitektura-qarorlari)
- [6.11 Qachon kontekst haqiqatan kerak (chegara)](#611-qachon-kontekst-haqiqatan-kerak-chegara)
- [6.12 Arxitektor nazorat ro'yxati](#612-arxitektor-nazorat-royxati)

**[7. Integratsion test: Spring Boot slice testlari](#7-integratsion-test-spring-boot-slice-testlari-integration-testing--spring-boot-test-slices)**

- [7.1 Slice test g'oyasi: butun ilovani emas, bitta qatlamni ko'tarish](#71-slice-test-goyasi-butun-ilovani-emas-bitta-qatlamni-kotarish)
- [7.2 @WebMvcTest: web qatlamni izolyatsiyada testlash](#72-webmvctest-web-qatlamni-izolyatsiyada-testlash)
- [7.3 @WebFluxTest va WebTestClient bilan reactive controller](#73-webfluxtest-va-webtestclient-bilan-reactive-controller)
- [7.4 @DataJpaTest: persistence qatlami va TestEntityManager](#74-datajpatest-persistence-qatlami-va-testentitymanager)
- [7.5 N+1 va generatsiya qilingan SQL'ni testda ushlash](#75-n1-va-generatsiya-qilingan-sqlni-testda-ushlash)
- [7.6 @JdbcTest, @DataJdbcTest, @JsonTest, @RestClientTest](#76-jdbctest-datajdbctest-jsontest-restclienttest)
- [7.7 @SpringBootTest: qachon kerak va webEnvironment variantlari](#77-springboottest-qachon-kerak-va-webenvironment-variantlari)
- [7.8 Kontekst keshi: eng katta tezlik omili](#78-kontekst-keshi-eng-katta-tezlik-omili)
- [7.9 @TestConfiguration, bean override va property manbalari](#79-testconfiguration-bean-override-va-property-manbalari)
- [7.10 @ActiveProfiles bilan test konfiguratsiyasini ajratish](#710-activeprofiles-bilan-test-konfiguratsiyasini-ajratish)
- [7.11 @Sql, @SqlMergeMode va tranzaksion testning tuzoqlari](#711-sql-sqlmergemode-va-tranzaksion-testning-tuzoqlari)
- [7.12 Slice test anti-patternlari](#712-slice-test-anti-patternlari)
- [7.13 Arxitektor nazorat ro'yxati](#713-arxitektor-nazorat-royxati)

**[8. Testcontainers bilan real infratuzilmada test](#8-testcontainers-bilan-real-infratuzilmada-test-integration-testing-with-testcontainers)**

- [8.1 Nega H2 yoki in-memory baza yetarli emas](#81-nega-h2-yoki-in-memory-baza-yetarli-emas)
- [8.2 Testcontainers asoslari: Docker API ustida hayot aylanishi](#82-testcontainers-asoslari-docker-api-ustida-hayot-aylanishi)
- [8.3 Spring Boot bilan integratsiya: @ServiceConnection va @DynamicPropertySource](#83-spring-boot-bilan-integratsiya-serviceconnection-va-dynamicpropertysource)
- [8.4 Singleton container pattern va kontekst keshi](#84-singleton-container-pattern-va-kontekst-keshi)
- [8.5 Konteynerni qayta ishlatish (reuse)](#85-konteynerni-qayta-ishlatish-reuse)
- [8.6 Turli texnologiyalar uchun konteynerlar](#86-turli-texnologiyalar-uchun-konteynerlar)
- [8.7 Spring Boot Docker Compose qo'llab-quvvatlashi va @TestConfiguration](#87-spring-boot-docker-compose-qollab-quvvatlashi-va-testconfiguration)
- [8.8 Ma'lumotlar bazasi migratsiyasini testlash](#88-malumotlar-bazasi-migratsiyasini-testlash)
- [8.9 Kafka bilan integratsion test](#89-kafka-bilan-integratsion-test)
- [8.10 Tezlik va resurs byudjeti](#810-tezlik-va-resurs-byudjeti)
- [8.11 Testcontainers'ni CI'da ishlatish](#811-testcontainersni-cida-ishlatish)
- [8.12 Anti-patternlar](#812-anti-patternlar)
- [8.13 Arxitektor nazorat ro'yxati](#813-arxitektor-nazorat-royxati)

**[9. Tashqi servislarni taqlid qilish va contract testing](#9-tashqi-servislarni-taqlid-qilish-va-contract-testing-faking-external-services--contract-testing)**

- [9.1 Muammo va yechim variantlari ierarxiyasi](#91-muammo-va-yechim-variantlari-ierarxiyasi)
- [9.2 WireMock bilan HTTP stub server](#92-wiremock-bilan-http-stub-server)
- [9.3 MockServer va Hoverfly: qachon qaysi biri](#93-mockserver-va-hoverfly-qachon-qaysi-biri)
- [9.4 MockRestServiceServer bilan client'ni testlash](#94-mockrestserviceserver-bilan-clientni-testlash)
- [9.5 Record and replay: foydasi va xavfi](#95-record-and-replay-foydasi-va-xavfi)
- [9.6 Stub drift muammosi](#96-stub-drift-muammosi)
- [9.7 Contract testing nazariyasi](#97-contract-testing-nazariyasi)
- [9.8 Spring Cloud Contract: buyurtma va to'lov servisi](#98-spring-cloud-contract-buyurtma-va-tolov-servisi)
- [9.9 Pact: consumer test, broker, can-i-deploy](#99-pact-consumer-test-broker-can-i-deploy)
- [9.10 Messaging contract va schema evolution](#910-messaging-contract-va-schema-evolution)
- [9.11 OpenAPI'ni contract sifatida ishlatish](#911-openapini-contract-sifatida-ishlatish)
- [9.12 Contract testni CI'ga qo'yish](#912-contract-testni-ciga-qoyish)
- [9.13 Anti-patternlar](#913-anti-patternlar)
- [9.14 Arxitektor nazorat ro'yxati](#914-arxitektor-nazorat-royxati)

**[10. Test ma'lumotlarini boshqarish](#10-test-malumotlarini-boshqarish-managing-test-data)**

- [10.1 Test ma'lumoti nega alohida mavzu](#101-test-malumoti-nega-alohida-mavzu)
- [10.2 Fixture strategiyalari](#102-fixture-strategiyalari)
- [10.3 Test Data Builder pattern](#103-test-data-builder-pattern)
- [10.4 Object Mother pattern](#104-object-mother-pattern)
- [10.5 Creation Method va test helper sinflarini tashkil qilish](#105-creation-method-va-test-helper-sinflarini-tashkil-qilish)
- [10.6 Tasodifiy va generatsiya qilingan ma'lumot](#106-tasodifiy-va-generatsiya-qilingan-malumot)
- [10.7 Ma'lumotlar bazasidagi holatni boshqarish](#107-malumotlar-bazasidagi-holatni-boshqarish)
- [10.8 Testlar orasida izolyatsiya](#108-testlar-orasida-izolyatsiya)
- [10.9 Tartibga bog'liqlik va uni aniqlash](#109-tartibga-bogliqlik-va-uni-aniqlash)
- [10.10 Katta hajmli va ishonchli ma'lumot](#1010-katta-hajmli-va-ishonchli-malumot)
- [10.11 Vaqtga bog'liq ma'lumot](#1011-vaqtga-bogliq-malumot)
- [10.12 Fayl, rasm va tashqi resurs ma'lumotlari](#1012-fayl-rasm-va-tashqi-resurs-malumotlari)
- [10.13 QA uchun test ma'lumoti](#1013-qa-uchun-test-malumoti)
- [10.14 Anti-patternlar](#1014-anti-patternlar)
- [10.15 Arxitektor nazorat ro'yxati](#1015-arxitektor-nazorat-royxati)

**[11. Xavfsizlik, tranzaksiya, asinxron va konkurentlik testlari](#11-xavfsizlik-tranzaksiya-asinxron-va-konkurentlik-testlari-testing-security-transactions-async--concurrency)**

- [11.1 Spring Security'ni testlash asoslari](#111-spring-securityni-testlash-asoslari)
- [11.2 Avtorizatsiya qoidalarini testlash](#112-avtorizatsiya-qoidalarini-testlash)
- [11.3 Method security'ni testlash](#113-method-securityni-testlash)
- [11.4 OAuth2 va JWT: Resource Server'ni testlash](#114-oauth2-va-jwt-resource-serverni-testlash)
- [11.5 CSRF, CORS, security header va sessiya](#115-csrf-cors-security-header-va-sessiya)
- [11.6 Xavfsizlik testining chegarasi](#116-xavfsizlik-testining-chegarasi)
- [11.7 Tranzaksiya chegaralarini testlash](#117-tranzaksiya-chegaralarini-testlash)
- [11.8 Optimistik va pessimistik lock'ni testlash](#118-optimistik-va-pessimistik-lockni-testlash)
- [11.9 Asinxron kodni testlash](#119-asinxron-kodni-testlash)
- [11.10 Spring event'larni testlash](#1110-spring-eventlarni-testlash)
- [11.11 Scheduled task va job'larni testlash](#1111-scheduled-task-va-joblarni-testlash)
- [11.12 Konkurentlik va poyga holatini testlash](#1112-konkurentlik-va-poyga-holatini-testlash)
- [11.13 Retry, timeout va circuit breaker'ni testlash](#1113-retry-timeout-va-circuit-breakerni-testlash)
- [11.14 Anti-patternlar](#1114-anti-patternlar)
- [11.15 Arxitektor nazorat ro'yxati](#1115-arxitektor-nazorat-royxati)

**[12. End-to-end va UI testlar](#12-end-to-end-va-ui-testlar-end-to-end--ui-testing)**

- [12.1 E2E testning o'rni va narxi](#121-e2e-testning-orni-va-narxi)
- [12.2 Qaysi senariylarni E2E qilish kerak](#122-qaysi-senariylarni-e2e-qilish-kerak)
- [12.3 API darajasidagi E2E](#123-api-darajasidagi-e2e)
- [12.4 UI avtomatlashtirish vositalari](#124-ui-avtomatlashtirish-vositalari)
- [12.5 Page Object va Screenplay patternlari](#125-page-object-va-screenplay-patternlari)
- [12.6 Barqaror UI test yozish qoidalari](#126-barqaror-ui-test-yozish-qoidalari)
- [12.7 Test muhiti va ma'lumot](#127-test-muhiti-va-malumot)
- [12.8 Parallel bajarish va vaqt byudjeti](#128-parallel-bajarish-va-vaqt-byudjeti)
- [12.9 Nosozlikni tahlil qilish](#129-nosozlikni-tahlil-qilish)
- [12.10 Vizual regressiya testlash](#1210-vizual-regressiya-testlash)
- [12.11 Mobil va cross-browser](#1211-mobil-va-cross-browser)
- [12.12 Smoke suite](#1212-smoke-suite)
- [12.13 Anti-patternlar](#1213-anti-patternlar)
- [12.14 Arxitektor nazorat ro'yxati](#1214-arxitektor-nazorat-royxati)

**[13. Nofunksional testlar: performance, resilience, xavfsizlik](#13-nofunksional-testlar-performance-resilience-xavfsizlik-non-functional-testing)**

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

**[14. Arxitektura testlari va kod sifati darvozalari](#14-arxitektura-testlari-va-kod-sifati-darvozalari-architecture-tests--code-quality-gates)**

- [14.1 Qoidani hujjat emas, test qilib yozish](#141-qoidani-hujjat-emas-test-qilib-yozish)
- [14.2 ArchUnit asoslari](#142-archunit-asoslari)
- [14.3 Amaliy ArchUnit qoidalari to'plami](#143-amaliy-archunit-qoidalari-toplami)
- [14.4 Spring Modulith bilan modul chegaralarini tekshirish](#144-spring-modulith-bilan-modul-chegaralarini-tekshirish)
- [14.5 Test coverage: JaCoCo](#145-test-coverage-jacoco)
- [14.6 Coverage anti-patternlari](#146-coverage-anti-patternlari)
- [14.7 Mutation testing: PIT](#147-mutation-testing-pit)
- [14.8 Statik tahlil: qaysi vositani tanlash](#148-statik-tahlil-qaysi-vositani-tanlash)
- [14.9 SonarQube quality gate](#149-sonarqube-quality-gate)
- [14.10 Bog'liqliklarni nazorat qilish](#1410-bogliqliklarni-nazorat-qilish)
- [14.11 Formatlash va pre-commit](#1411-formatlash-va-pre-commit)
- [14.12 Darvozalarni joylashtirish](#1412-darvozalarni-joylashtirish)
- [14.13 Darvozalarni joriy qilish strategiyasi](#1413-darvozalarni-joriy-qilish-strategiyasi)
- [14.14 Arxitektor nazorat ro'yxati](#1414-arxitektor-nazorat-royxati)

**[15. CI/CD da test pipeline](#15-cicd-da-test-pipeline-the-test-pipeline-in-cicd)**

- [15.1 Pipeline bosqichlari va tartibi](#151-pipeline-bosqichlari-va-tartibi)
- [15.2 Feedback vaqti byudjeti](#152-feedback-vaqti-byudjeti)
- [15.3 Testlarni ajratish va parallel bajarish](#153-testlarni-ajratish-va-parallel-bajarish)
- [15.4 Keshlash va tezlashtirish](#154-keshlash-va-tezlashtirish)
- [15.5 Testni tanlab ishga tushirish](#155-testni-tanlab-ishga-tushirish)
- [15.6 GitHub Actions bilan to'liq namuna workflow](#156-github-actions-bilan-toliq-namuna-workflow)
- [15.7 GitLab CI va Jenkins uchun eslatma](#157-gitlab-ci-va-jenkins-uchun-eslatma)
- [15.8 Majburiy tekshiruvlar va branch protection](#158-majburiy-tekshiruvlar-va-branch-protection)
- [15.9 Test natijalari va hisobot](#159-test-natijalari-va-hisobot)
- [15.10 Nightly va haftalik suite'lar](#1510-nightly-va-haftalik-suitelar)
- [15.11 Deploy'dan keyingi tekshirish](#1511-deploydan-keyingi-tekshirish)
- [15.12 Production'da testlash](#1512-productionda-testlash)
- [15.13 Monorepo va multi-modul loyihada test pipeline](#1513-monorepo-va-multi-modul-loyihada-test-pipeline)
- [15.14 Pipeline'ni ishonchli qilish](#1514-pipelineni-ishonchli-qilish)
- [15.15 Anti-patternlar](#1515-anti-patternlar)
- [15.16 Arxitektor nazorat ro'yxati](#1516-arxitektor-nazorat-royxati)

**[16. Flaky testlar, test qarzi va test kodini saqlash](#16-flaky-testlar-test-qarzi-va-test-kodini-saqlash-flaky-tests-test-debt--maintenance)**

- [16.1 Flaky test nima va nega eng qimmat muammo](#161-flaky-test-nima-va-nega-eng-qimmat-muammo)
- [16.2 Flaky testning asosiy sabablari, misollar va yechimlari](#162-flaky-testning-asosiy-sabablari-misollar-va-yechimlari)
- [16.3 Flaky testni aniqlash](#163-flaky-testni-aniqlash)
- [16.4 Karantin (quarantine) jarayoni](#164-karantin-quarantine-jarayoni)
- [16.5 Retry'ning o'rni](#165-retryning-orni)
- [16.6 Test qarzi (test debt)](#166-test-qarzi-test-debt)
- [16.7 Testni o'chirish qoidalari](#167-testni-ochirish-qoidalari)
- [16.8 Test kodini refaktoring qilish](#168-test-kodini-refaktoring-qilish)
- [16.9 Test smell'lar katalogi](#169-test-smelllar-katalogi)
- [16.10 Sekin testlarni tezlashtirish](#1610-sekin-testlarni-tezlashtirish)
- [16.11 Testlar egaligi va madaniyat](#1611-testlar-egaligi-va-madaniyat)
- [16.12 Anti-patternlar](#1612-anti-patternlar)
- [16.13 Arxitektor nazorat ro'yxati](#1613-arxitektor-nazorat-royxati)

**[17. Metrikalar va test yetukligi modeli](#17-metrikalar-va-test-yetukligi-modeli-metrics--testing-maturity)**

- [17.1 Nimani o'lchash kerak va nega](#171-nimani-olchash-kerak-va-nega)
- [17.2 Sifat natijasi metrikalari (outcome)](#172-sifat-natijasi-metrikalari-outcome)
- [17.3 Jarayon metrikalari](#173-jarayon-metrikalari)
- [17.4 Test suite sog'ligi metrikalari](#174-test-suite-sogligi-metrikalari)
- [17.5 Coverage'ni to'g'ri ishlatish](#175-coverageni-togri-ishlatish)
- [17.6 Metrikalarni yig'ish va ko'rsatish](#176-metrikalarni-yigish-va-korsatish)
- [17.7 Ogohlantiruvchi belgilar (leading indicators)](#177-ogohlantiruvchi-belgilar-leading-indicators)
- [17.8 Test yetukligi modeli: besh daraja](#178-test-yetukligi-modeli-besh-daraja)
- [17.9 Nolga yaqin holatdan boshlash: 30/60/90 kunlik reja](#179-nolga-yaqin-holatdan-boshlash-306090-kunlik-reja)
- [17.10 Legacy kodga test yozish strategiyasi](#1710-legacy-kodga-test-yozish-strategiyasi)
- [17.11 Jamoani ishontirish va o'rgatish](#1711-jamoani-ishontirish-va-orgatish)
- [17.12 Byudjet va vaqt](#1712-byudjet-va-vaqt)
- [17.13 Anti-patternlar](#1713-anti-patternlar)
- [17.14 Arxitektor nazorat ro'yxati](#1714-arxitektor-nazorat-royxati)

**[18. Shablonlar, checklistlar va ma'lumotnoma](#18-shablonlar-checklistlar-va-malumotnoma-templates-checklists--reference)**

- [18.1 Test strategiyasi hujjati shabloni](#181-test-strategiyasi-hujjati-shabloni)
- [18.2 Test rejasi (test plan) shabloni](#182-test-rejasi-test-plan-shabloni)
- [18.3 Definition of Done namunasi](#183-definition-of-done-namunasi)
- [18.4 Pull request'da test uchun review checklisti](#184-pull-requestda-test-uchun-review-checklisti)
- [18.5 Bug report shabloni](#185-bug-report-shabloni)
- [18.6 Test case va checklist shabloni](#186-test-case-va-checklist-shabloni)
- [18.7 Exploratory testing charter va sessiya hisoboti](#187-exploratory-testing-charter-va-sessiya-hisoboti)
- [18.8 Yangi mikroservis uchun test setup checklisti](#188-yangi-mikroservis-uchun-test-setup-checklisti)
- [18.9 Yangi jamoa a'zosi uchun onboarding checklisti](#189-yangi-jamoa-azosi-uchun-onboarding-checklisti)
- [18.10 Release sign-off checklisti](#1810-release-sign-off-checklisti)
- [18.11 Incident'dan keyin test yozish (postmortem) checklisti](#1811-incidentdan-keyin-test-yozish-postmortem-checklisti)
- [18.12 Tavsiya etilgan kutubxonalar ma'lumotnomasi](#1812-tavsiya-etilgan-kutubxonalar-malumotnomasi)
- [18.13 Nomlash va joylashtirish konvensiyalari](#1813-nomlash-va-joylashtirish-konvensiyalari)
- [18.14 Keng tarqalgan xatolar va tezkor yechimlar](#1814-keng-tarqalgan-xatolar-va-tezkor-yechimlar)
- [18.15 Keyingi o'qish uchun manbalar](#1815-keyingi-oqish-uchun-manbalar)
- [18.16 Arxitektor nazorat ro'yxati](#1816-arxitektor-nazorat-royxati)

---

## 1. Sifat strategiyasi va arxitektorning roli (Quality Strategy & the Architect's Role)

Java va Spring ekotizimida testlash ko'pincha "qoplama foizini oshirish" vazifasi deb tushuniladi, lekin arxitektor uchun bu mutlaqo boshqa masala: testlar — bu tizim haqida qaror qabul qilish uchun kerak bo'ladigan ma'lumot manbai. Ushbu bobda biz sifat strategiyasini biznes riski bilan bog'lash, testability'ni arxitektura talabiga aylantirish va sifat darvozalarini o'rnatish masalalarini ko'rib chiqamiz. Maqsad — jamoaga "qancha test kerak?" degan savolga his-tuyg'u bilan emas, balki asoslangan tarzda javob berish imkonini beradigan ramka yaratish. Barcha misollar Spring Boot 3.x/4.x, Spring Framework 6.x/7.x, JUnit 5 va Java 17-25 kontekstida beriladi.

### 1.1 Testlash maqsadi: qaror uchun ishonch

Keng tarqalgan noto'g'ri tasavvur — testlash xatolarni topish uchun kerak. Haqiqatda xatoni topish bu yon mahsulot. Asosiy maqsad — **qaror qabul qilish uchun ishonch darajasini oshirish**. Har bir test aslida bitta savolga javob beradi: "Shu o'zgarishni production'ga chiqarsam bo'ladimi?"

Bu farq amaliy natijalarga olib keladi. Agar maqsad xato topish bo'lsa, jamoa topilgan xatolar sonini o'lchaydi va test yozishdan ko'ra bug tracker'ni to'ldirishga qiziqadi. Agar maqsad ishonch bo'lsa, savol o'zgaradi: "Qaysi test release haqidagi qo'rquvimni kamaytiradi?" Natijada test to'plami release jarayonining bir qismiga aylanadi, nafaqat developer'ning shaxsiy odatiga.

Ikkinchi muhim tamoyil — sifat butun jamoaning mas'uliyati. QA mustaqil "tekshiruvchi devor" emas; u sifat bo'yicha ekspert va jarayon dizayneri. Agar developer "men kod yozaman, QA sinaydi" deb o'ylasa, siz allaqachon arxitektura muammosiga egasiz: feedback loop uzun, mas'uliyat tarqoq, sifat esa oxirgi bosqichga surilgan. Arxitektor sifatida siz bu modelni buzishingiz kerak — kod yozgan odam o'z kodining testini ham yozadi, QA esa risk tahlili, test dizayni va avtomatlashtirish strategiyasiga javob beradi (batafsil taqsimot — 3-bobga qarang).

Shuni ham aytib o'tish kerak: testlar hech qachon xatolar yo'qligini isbotlay olmaydi. Ular faqat tekshirilgan stsenariylarda tizim kutilgandek ishlashini ko'rsatadi. Shuning uchun "100% coverage" maqsad emas — bu ko'rsatkichni maqsadga aylantirish (Goodhart qonuni) test sifatini pasaytiradi.

### 1.2 Shift-left va shift-right

**Shift-left** — sifat faoliyatini loyihaning boshlang'ich bosqichlariga surish. Bu faqat "testni erta yozish" degani emas. Bu quyidagilarni o'z ichiga oladi:

- Talablarni yozishda qabul kriteriylarini (acceptance criteria) misollar bilan aniqlash — "Given/When/Then" ko'rinishida.
- Arxitektura qarorini qabul qilayotganda "buni qanday sinaymiz?" savolini ADR (Architecture Decision Record) ning majburiy bo'limiga aylantirish.
- Design review'da testability'ni alohida kriteriya qilish: yangi komponent static bog'liqliklarga ega bo'lsa, review'dan o'tmaydi.
- Statik tahlil va kompilyatsiya vaqtidagi tekshiruvlarni (null-safety annotatsiyalari, Error Prone, SpotBugs) IDE darajasiga olib tushirish.

Xatoni dizayn bosqichida tuzatish arzon, production'da esa qimmat — bu eski, lekin hali ham amal qiladigan qoida. Muhimi, "arzon/qimmat" nisbatini o'z loyihangizda o'lchab ko'rish: production incident'ning o'rtacha narxi (MTTR x jalb qilingan odamlar soni + biznes yo'qotish) va bir test yozish narxini solishtiring.

**Shift-right** — production'da sifatni kuzatish va tekshirish. Testning barcha holatini staging'da takrorlash imkonsiz, shuning uchun:

- Health check va readiness probe'lar (`spring-boot-starter-actuator` orqali `/actuator/health`, `/actuator/metrics`).
- Micrometer orqali biznes metrikalari: muvaffaqiyatsiz to'lovlar foizi, retry soni, latency percentile'lari.
- Feature flag bilan canary release: yangi kod avval 1% trafikka ochiladi.
- Synthetic monitoring: production'da doimiy ishlab turadigan smoke stsenariylari.
- Chaos testing: tashqi servis javob bermaganida tizim qanday ishlashini real sharoitda tekshirish.

Shift-left va shift-right bir-birini almashtirmaydi, balki to'ldiradi. Shift-left xatoni oldini oladi, shift-right esa oldini olinmagan xatoni tez aniqlaydi.

### 1.3 Risk-ga asoslangan testlash

"Qaysi modulga qancha test yozamiz?" — arxitektor javob berishi kerak bo'lgan asosiy savol. Javob coverage maqsadidan kelib chiqmaydi, riskdan kelib chiqadi. Risk = ehtimollik x ta'sir.

**Ehtimollik** omillari: kodning o'zgarish tezligi (churn), siklomatik murakkablik, yangi texnologiya ishlatilishi, bog'liqliklar soni, jamoadagi tajriba.

**Ta'sir** omillari: pul yo'qotish, ma'lumot buzilishi, reglament/compliance buzilishi, foydalanuvchilar soni, tiklanish qiyinligi (reversible yoki yo'q).

| Modul | Ehtimollik | Ta'sir | Risk darajasi | Test chuqurligi |
|---|---|---|---|---|
| To'lov (payment) initsiatsiyasi | O'rta | Juda yuqori | Kritik | Unit + integration + contract + idempotency + konkurentlik + E2E smoke |
| To'lov holatini sinxronlash (webhook) | Yuqori | Juda yuqori | Kritik | Unit + Testcontainers + mutation testing + chaos (provider timeout) |
| Buyurtma narxini hisoblash | O'rta | Yuqori | Yuqori | Unit (property-based) + integration |
| Autentifikatsiya / authorization | Past | Juda yuqori | Yuqori | Unit + security slice test + arxitektura testlari |
| Hisobot eksporti (CSV) | O'rta | O'rta | O'rta | Unit + 1-2 integration |
| Admin paneli CRUD | Past | Past | Past | Slice test (`@WebMvcTest`) + happy path, E2E yo'q |
| Ichki feature flag paneli | Past | Past | Juda past | Smoke test, manual tekshiruv kifoya |

Misolni konkretlashtiramiz. **To'lov moduli** uchun: har bir summa hisoblash qoidasi unit test bilan qoplanadi, idempotency kaliti takroriy so'rovda ikki marta pul olinmasligini ta'minlaydi (test majburiy), tashqi provider bilan contract test, parallel so'rovlarda balans buzilmasligi uchun konkurentlik testi, va provider 500 qaytarganda retry/circuit breaker xatti-harakati tekshiriladi. Bu modulda line coverage 90%+ va mutation score kuzatiladi.

**Admin paneli** uchun: foydalanuvchilar — 12 ta ichki xodim, xato aniqlanishi bir necha daqiqada, tiklanish oson. Shuning uchun `@WebMvcTest` bilan controller validatsiyasi va ruxsat tekshiruvi sinaladi, E2E UI testi yozilmaydi (chunki saqlash narxi bergan ishonchdan yuqori). Coverage maqsadi 50-60%.

Qoida: **modul bo'yicha differensiallangan sifat talabi**. Bitta global coverage raqami butun loyiha uchun — bu strategiya emas, balki strategiya yo'qligining belgisi.

### 1.4 Test strategiyasi hujjati

Ko'p jamoalar "test strategiyasi" va "test rejasi" ni aralashtirib yuboradi. Farq quyidagicha:

| Mezon | Test strategiyasi | Test rejasi (test plan) |
|---|---|---|
| Qamrov | Butun mahsulot / tashkilot | Bitta release, epic yoki feature |
| Umr muddati | 6-12 oy, kamdan-kam o'zgaradi | Sprint yoki release davomida |
| Muallif | Arxitektor + QA lead | QA engineer / feature lead |
| Tasdiqlovchi | Engineering manager / CTO | Tech lead + product owner |
| Mazmuni | Tamoyillar, darajalar, vositalar, darvozalar | Konkret stsenariylar, muhitlar, jadval |

Strategiya hujjatiga kiritiladigan minimal bo'limlar:

1. Sifat maqsadlari va ularning biznes ko'rsatkichi bilan bog'lanishi (masalan: "to'lov oqimida production defect < 1 / chorak").
2. Test darajalari va har biri uchun mas'uliyat chegarasi (2-bobga qarang).
3. Risk klassifikatsiyasi va modul bo'yicha chuqurlik matritsasi (yuqoridagi jadval).
4. Vositalar to'plami: JUnit 5, AssertJ, Mockito, Testcontainers, WireMock, ArchUnit, JaCoCo — versiyalar BOM orqali boshqariladi.
5. Test muhitlari va ma'lumot strategiyasi.
6. Sifat darvozalari va Definition of Done.
7. Metrikalar va ularni kim, qanchalik tez-tez ko'rib chiqadi.
8. Istisnolar jarayoni: darvozani kim va qanday asos bilan chetlab o'tishi mumkin.

Hujjat kod repozitoriyasida (`docs/testing-strategy.md`) yashashi va PR orqali o'zgarishi kerak — shunda uning tarixi bo'ladi. Yangilanish triggerlari: yangi arxitektura uslubi joriy etilishi, jiddiy production incident, texnologiya stack'ining almashishi, yoki chorakda bir marta rejali qayta ko'rib chiqish.

### 1.5 Sifat darvozalari va Definition of Done

Darvoza — avtomatik, obyektiv va buzib o'tilishi qiyin shart. "Code review'da e'tibor bering" — bu darvoza emas, bu umid.

**PR darajasidagi darvoza** (har bir pull request uchun, 10 daqiqadan oshmasligi kerak):

| Tekshiruv | Shart | Buzilganda |
|---|---|---|
| Compile + unit testlar | 100% o'tadi | Merge bloklanadi |
| Yangi/o'zgargan kod coverage | >= 80% (JaCoCo diff coverage) | Merge bloklanadi |
| Statik tahlil (yangi issue) | Critical/Blocker = 0 | Merge bloklanadi |
| Arxitektura testlari (ArchUnit) | 100% o'tadi | Merge bloklanadi |
| Flaky test | Yangi flaky qo'shilmagan | Ogohlantirish + ticket |
| Code review | Kamida 1 approve | Merge bloklanadi |

**Release darajasidagi darvoza**:

| Tekshiruv | Shart |
|---|---|
| Integration + slice testlar | 100% o'tadi |
| Testcontainers bilan DB migratsiya testi | O'tadi (forward va rollback) |
| Contract testlar (provider + consumer) | 100% o'tadi |
| E2E smoke (kritik oqimlar) | 100% o'tadi |
| Performance baseline | p95 latency regressiya < 10% |
| Xavfsizlik skaneri (dependency CVE) | High/Critical = 0 yoki hujjatlashtirilgan istisno |
| Mutation score (kritik modullar) | >= 60% |

**Definition of Done** darvozadan kengroq — u insoniy bandlarni ham o'z ichiga oladi: qabul kriteriylari bajarilgan, log va metrika qo'shilgan, hujjat yangilangan, feature flag bilan o'raladigan joyi aniqlangan, rollback rejasi mavjud. Arxitektor DoD ni jamoa bilan birga yozadi va uni Jira/Linear shablonida ko'rinadigan qiladi — devordagi plakat emas, jarayonning qismi bo'lsin.

Maslahat: darvozani joriy qilishda avval "ogohlantirish" rejimida ishga tushirib, 2-3 sprint statistika yig'ing, keyin bloklashga o'tkazing. Birdan bloklash jamoaning qarshiligini keltiradi.

### 1.6 Testability'ni arxitektura talabiga aylantirish

Test yozish qiyinligi — bu test muammosi emas, dizayn muammosi. Agar sinovchi "buni sinash imkonsiz" desa, arxitektor javob berishi kerak bo'lgan savol: "Nega bu kod shunday qattiq bog'langan?"

**Dependency injection — construktor orqali.** Spring'da `@Autowired` field injection testda obyektni qo'lda yaratish imkonini yo'q qiladi. Constructor injection esa bean'ni Spring context'siz, oddiy `new` bilan yaratib sinash imkonini beradi. Final maydonlar bilan immutability ham bonus.

```java
@Service
public class PaymentService {
    private final PaymentGateway gateway;   // port (interfeys)
    private final Clock clock;              // vaqt tashqaridan
    private final IdGenerator idGenerator;  // tasodif tashqaridan

    public PaymentService(PaymentGateway gateway, Clock clock, IdGenerator idGenerator) {
        this.gateway = gateway;
        this.clock = clock;
        this.idGenerator = idGenerator;
    }
}
```

**Port va adapter (hexagonal).** Domain logikasi infratuzilmani bilmasligi kerak. `PaymentGateway` — port (domain paketidagi interfeys), `StripePaymentAdapter` — adapter (infrastructure paketida). Natijada domain testlari HTTP, DB yoki broker'siz, millisekundlarda ishlaydi. ArchUnit bilan bu qoidani majburlash mumkin (14-bobga qarang).

**Vaqtni tashqaridan bering.** `LocalDateTime.now()` va `Instant.now()` to'g'ridan-to'g'ri chaqirilsa, "oyning oxirgi kuni" yoki "sertifikat muddati tugashi" stsenariysini sinash imkonsiz bo'ladi. Yechim — `java.time.Clock` bean:

```java
@Bean
public Clock clock() {
    return Clock.systemUTC();
}
// Testda: Clock.fixed(Instant.parse("2026-01-31T23:59:00Z"), ZoneOffset.UTC)
```

**Tasodifni tashqaridan bering.** UUID, random token, shuffle — barchasi interfeys ortida. Aks holda test natijasi takrorlanmaydi.

**Tashqi chaqiruvlarni interfeys ortiga yashiring.** `RestClient`, `WebClient`, Kafka producer, S3 client — hech qachon domain servisida to'g'ridan-to'g'ri ishlatilmasin. Bu nafaqat testability, balki retry, timeout va circuit breaker siyosatini bir joyda boshqarish imkonini beradi.

**Static va singleton'dan voz kechish.** Static metodlar, `new Date()`, global holat — bularning hammasi testda almashtirilmaydi. Agar legacy kodda bo'lsa, uni yupqa interfeys bilan o'rab chiqing.

**Kuzatiladigan (observable) qiling.** Test faqat qaytarilgan qiymatni tekshirmaydi — ba'zan "nima sodir bo'lganini" tekshirish kerak. Shuning uchun: muhim biznes hodisalar uchun Micrometer counter/timer, strukturalangan log (MDC bilan correlation ID), va domain event'lar. Spring'da `ApplicationEventPublisher` orqali chiqarilgan event testda osongina ushlanadi. Qoida: agar siz bir holatni log yoki metrika orqali tashqaridan ko'ra olmasangiz, uni production'da ham diagnostika qilolmaysiz.

Bu talablar ADR va design review checklist'ga kirishi kerak. "Testability — non-functional requirement" degan gapni hujjatda yozib qo'yish kifoya emas; uni review'da savol ko'rinishida so'rash kerak.

### 1.7 Testlash xarajati va qiymati balansi

Har bir test uch xil narxga ega: **yozish** (bir martalik), **ishga tushirish** (har CI run'da) va **saqlash** (kod o'zgarganda tuzatish). Uchinchisi eng ko'p e'tibordan chetda qoladi va aynan u eng qimmat.

| Daraja | Yozish narxi | Ishga tushish vaqti | Saqlash narxi | Bergan ishonch | Diagnostika aniqligi |
|---|---|---|---|---|---|
| Unit (Spring'siz) | Past | ms | Past | Logika to'g'riligi | Juda yuqori |
| Slice (`@WebMvcTest`, `@DataJpaTest`) | O'rta | 1-3 s | O'rta | Qatlam integratsiyasi | Yuqori |
| Integration (Testcontainers) | Yuqori | 5-30 s | O'rta-yuqori | Real DB/broker bilan ishlash | O'rta |
| Contract | O'rta | 1-5 s | O'rta | Servislar o'rtasidagi muvofiqlik | Yuqori |
| E2E / UI | Juda yuqori | daqiqalar | Juda yuqori | Foydalanuvchi oqimi | Past |

Amaliy qoidalar:

- Bir xil ishonchni arzonroq darajada olish mumkin bo'lsa, arzonroqni tanlang. Validatsiya qoidasini E2E testda sinash — resurs isrofi.
- Qiymat bermaydigan testni o'chirish — bu yo'qotish emas, tejamkorlik. Hech qachon buzilmagan va hech narsani ushlamagan test faqat saqlash narxini keltiradi.
- Ishga tushish vaqtini kuzatib boring. PR pipeline 10 daqiqadan oshsa, developer kutmay boshqa ishga o'tadi — feedback loop buziladi va testning qiymati tushadi.
- Spring context'ni qayta ishlatish (context caching) — eng arzon tezlashtirish usuli. Har bir test klassida har xil `@MockBean`/`@TestConfiguration` kombinatsiyasi yangi context yaratadi; bu sekinlikning asosiy manbai.
- Flaky test qiymati manfiy: u ishonchni yo'qotadi va jamoani "qayta ishga tushirish" odatiga o'rgatadi (16-bobga qarang).

### 1.8 Arxitektorning aniq vazifalari

Sifat strategiyasida arxitektorning roli "maslahat berish" emas, balki konkret, tekshiriladigan ishlardan iborat:

1. **Strategiyani belgilash va hujjatlashtirish.** Risk matritsasini modul egalari bilan birga to'ldirish, modul bo'yicha chuqurlik talabini kelishish.
2. **Test infratuzilmasini tanlash.** JUnit 5 platformasi, mocking kutubxonasi, Testcontainers moduli, contract testing yondashuvi, coverage va mutation vositalari. Tanlov ADR bilan asoslanadi, versiyalar Spring Boot BOM va `dependencyManagement` orqali markazlashtiriladi.
3. **Standartlarni yozish.** Test nomlash konvensiyasi, test ma'lumotlari uchun builder/fixture uslubi, qaysi holatda mock va qaysi holatda real obyekt ishlatiladi, test paketlari tuzilishi. Shablonlar 18-bobda.
4. **Test kodini review qilish.** Test kodi production kodi bilan bir xil standartga javob berishi kerak. Review'da e'tibor: assertion aniqligimi yoki `assertNotNull` bilan cheklanganmi, test nomi niyatni ifodalaydimi, mock haddan ortiq ishlatilmaganmi.
5. **Metrikalarni kuzatish.** Diff coverage, mutation score (kritik modullarda), pipeline davomiyligi, flaky test ro'yxati, production defect escape rate, MTTR. Chorakda bir marta trend tahlili (17-bobga qarang).
6. **Darvozalarni o'rnatish va himoya qilish.** Eng qiyin qismi — bosim ostida darvozani ochmaslik. Istisno jarayoni yozilgan va kim ruxsat berishi aniq bo'lishi kerak.
7. **Jamoani o'rgatish.** Pair testing sessiyalari, ichki workshop, misol bo'ladigan reference modul ("shunday yozamiz" namunasi). Yangi odamga onboarding'da test standartini ko'rsatish.
8. **Testability'ni dizayn review'ning majburiy kriteriyasiga aylantirish.** Har bir yangi komponent uchun: "bu qanday sinaladi?" savolini so'rash.

### 1.9 Arxitektor nazorat ro'yxati

- [ ] Loyihada `docs/testing-strategy.md` mavjud, oxirgi 6 oyda yangilangan va PR orqali boshqariladi.
- [ ] Modul bo'yicha risk matritsasi (ehtimollik x ta'sir) to'ldirilgan va har bir modul uchun test chuqurligi hamda coverage maqsadi alohida belgilangan.
- [ ] PR darajasidagi darvozalar CI'da avtomatik ishlaydi: unit testlar, diff coverage, statik tahlil, ArchUnit — qo'lda tekshiruvga tayanmaydi.
- [ ] Release darvozasi aniqlangan (integration, contract, migratsiya, smoke, CVE skaneri) va istisno berish jarayoni hujjatlashtirilgan.
- [ ] Definition of Done jamoa tomonidan tasdiqlangan va issue tracker shablonida ko'rinadi.
- [ ] Barcha yangi bean'lar constructor injection ishlatadi; `Clock`, ID/tasodif generatori va tashqi client'lar interfeys ortida va bean sifatida inject qilinadi.
- [ ] Domain qatlami infratuzilma paketlariga bog'liq emasligi arxitektura testi bilan majburlangan.
- [ ] PR pipeline davomiyligi 10 daqiqadan oshmaydi va u haftalik kuzatiladigan metrika.
- [ ] Flaky testlar ro'yxati mavjud, har biri uchun egasi va muddati belgilangan.

---

## 2. Test piramidasi va test turlari xaritasi (Test Pyramid & the Map of Test Types)

Test strategiyasi hujjat emas, byudjet taqsimotidir: har bir test darajasi pul, vaqt va ishonch o'rtasidagi muayyan kelishuvni ifodalaydi. Arxitektorning asosiy vazifasi — qaysi mantiq qaysi darajada tekshirilishini ongli ravishda belgilash va bu qarorni loyiha tuzilishi hamda build konfiguratsiyasida majburiy qilib qo'yish. Bu bobda klassik piramidadan zamonaviy shakllarga o'tish, test turlarining to'liq xaritasi, mantiq-daraja mosligi va Maven/Gradle darajasidagi amaliy konvensiyalar ko'rib chiqiladi. Maqsad — jamoada "bu testni qayerga yozaman?" savoliga bir xil javob beriladigan holatga erishish.

### 2.1 Klassik test piramidasi (Cohn)

Mike Cohn "Succeeding with Agile" (2009) kitobida test avtomatizatsiyasini uch qatlamli piramida sifatida tasvirlagan: keng asosda unit testlar, o'rtada service (integratsion) testlar, cho'qqida UI testlar. Shakl tasodifiy emas — u uchta o'zgaruvchining teskari proporsiyasini aks ettiradi: yuqoriga ko'tarilgan sari bitta testning ishga tushish vaqti, tiklash narxi va noaniqligi (flakiness) ortadi, lekin biznes ishonchi ham oshadi.

Keng asos kerakligining sababi matematik: Spring loyihasida bitta `@SpringBootTest` konteksti ko'tarilishi odatda bir necha soniya, oddiy unit test esa millisekundlar oladi. Agar 2000 ta holatni faqat yuqori darajada tekshirsangiz, suite soatlab ishlaydi va developer uni mahalliy mashinada ishga tushirmay qo'yadi — ya'ni test fikr-mulohaza (feedback) vositasi bo'lishdan to'xtaydi. Ikkinchi sabab — diagnostika aniqligi: unit test yiqilganda xato manzili bitta metod, E2E test yiqilganda esa o'ntacha servis ichida qolgan ehtimolliklar to'plami.

Piramidaning muhim, lekin ko'pincha e'tibordan chetda qolgan sharti: pastdagi testlar ustidagi testlarni *takrorlamasligi* kerak. Piramida qatlamlar qalinligi haqida emas, javobgarlik bo'linishi haqidagi shartnoma.

### 2.2 Zamonaviy variantlar: Testing Trophy, Honeycomb, Test Diamond

Klassik piramida 2009-yilda, DI konteynerlari sekin va konteynerlashtirish mavjud emas paytda shakllangan. Testcontainers, tez Spring kontekst keshi va kuchli statik analiz piramidani qayta muvozanatlashtirishga imkon berdi.

**Testing Trophy** (Kent C. Dodds) to'rt qatlamdan iborat: statik analiz (compiler, linter, null-check), unit, integration (eng keng qism), E2E. Asosiy g'oya — "integration" darajasi eng yaxshi ishonch/narx nisbatini beradi, chunki u real wiring'ni tekshiradi, lekin brauzer yoki to'liq muhitni talab qilmaydi. Java olamida bu Spring'ning slice testlari (`@WebMvcTest`, `@DataJpaTest`) va Testcontainers bilan ishlaydigan modul testlari.

**Testing Honeycomb** (Spotify, 2018) microservice'lar uchun taklif qilingan: o'rtada keng "integration test" qatlami, ikki tomonda tor "integrated test" (boshqa real servislar bilan) va "implementation detail test" qatlamlari. Mantiq — microservice'da murakkablik kodning ichida emas, servis chegarasida: HTTP contract, serializatsiya, DB mapping, message broker. Shuning uchun ko'p unit test yozishdan ko'ra, servisni chegaralari bilan birga, lekin tashqi real servislarsiz testlash foydali.

**Test Diamond** — yupqa unit, semiz integratsion va yupqa E2E qatlamlari. Bu shakl legacy modullarda yoki domain mantiqi kam bo'lgan, asosan orkestratsiya va mapping bilan shug'ullanadigan servislarda tabiiy yuzaga keladi.

| Loyiha turi | To'g'ri shakl | Nega |
|---|---|---|
| Boy domain mantiqli modular monolit | Piramida / Trophy | Qoidalar POJO darajasida testlanadi, modul chegaralari integratsiyada |
| CRUD-ga yaqin microservice | Honeycomb / Diamond | Risk chegarada: contract, mapping, DB, broker |
| Kutubxona yoki SDK | Qattiq piramida | Tashqi I/O yo'q, API yuzasi keng, mutation testing arzon |
| Legacy, testsiz tizim | Diamond (vaqtincha) | Avval xatti-harakatni integratsiyada "qotirish", keyin pastga tushirish |
| BFF / API gateway | Honeycomb | Deyarli butun qiymat serializatsiya va routing'da |

Shaklni tanlash qarori ADR (Architecture Decision Record) sifatida yozilishi kerak — aks holda har bir jamoa a'zosi o'z piramidasini quradi.

### 2.3 Teskari piramida (ice-cream cone) anti-patterni

Ice-cream cone — asosi yupqa unit testlardan, tanasi integratsion testlardan va keng cho'qqisi E2E/manual testlardan iborat teskari shakl (atama Alister Scott tomonidan ommalashtirilgan). U hech qachon ongli tanlov natijasi bo'lmaydi: u "release oldidan QA hammasini bosib ko'radi" degan jarayonning avtomatizatsiyaga ko'chirilishidan kelib chiqadi.

Narxi aniq o'lchanadi:

- **Feedback vaqti.** PR pipeline 10 daqiqadan 60-90 daqiqaga chiqadi, developer kontekstni yo'qotadi, batch'lar kattalashadi.
- **Flakiness.** E2E testlar zanjiridagi har bir bo'g'in ishonchliligi 99% bo'lsa ham, 40 bo'g'inli suite'ning barqarorligi ~67% ga tushadi. Natijada "qayta ishga tushir" madaniyati va yashil build'ga ishonchsizlik paydo bo'ladi.
- **Diagnostika narxi.** Bitta yiqilgan E2E test uchun o'rtacha tahlil vaqti unit testdan 10-30 barobar ko'p.
- **Refactoring to'xtaydi.** Ichki tuzilma testlar bilan qoplanmagani uchun har qanday o'zgarish regressiya qo'rquvini keltiradi.
- **Infrastruktura xarajati.** Har bir PR uchun to'liq muhit ko'tarish CI hisobining asosiy qismiga aylanadi.

Tuzatish yo'li — testni o'chirish emas, **pastga ko'chirish**: yiqilgan E2E testdagi har bir assertion uchun "bu holat eng past qaysi darajada tasdiqlanishi mumkin?" savolini berib, mos darajada test yozib, keyin E2E'dan o'sha assertion'ni olib tashlash.

### 2.4 Test turlari to'liq xaritasi

| Tur | Maqsadi | Nimani tasdiqlaydi | Tezlik | Kim yozadi | Qancha bo'lishi kerak |
|---|---|---|---|---|---|
| Unit | Mantiq to'g'riligi | Bitta klass/metod qarori, chegara holatlari | < 10 ms | Developer | Eng ko'p; test sonining ~50-60% |
| Komponent (slice) | Qatlam wiring'i | Controller serializatsiyasi, repository mapping, JSON | 0.1-2 s | Developer | ~20-25% |
| Integratsion | Real adapter ishlashi | SQL, migratsiya, broker, HTTP client (Testcontainers) | 1-10 s | Developer | ~10-15% |
| Contract | Chegara muvofiqligi | Provider va consumer kutganlari mos | < 1 s | Ikki jamoa birga | Har bir tashqi chegara uchun 1 ta to'plam |
| System | Deploy qilingan servis | Bitta servis + real bog'liqliklari | 5-30 s | Developer / QA eng muhim oqimlar | 10-30 ta |
| E2E | Biznes oqimi | Foydalanuvchi uchidan-uchiga yo'li | 10 s - minutlar | QA automation | 5-20 ta; test sonining 1-3% |
| Smoke | Deploy sog'ligi | Ishga tushdi, health/version, kritik endpoint | < 60 s (suite) | DevOps / QA | 5-15 ta, har deploy'da |
| Regression | Qaytmaslik kafolati | Oldin topilgan har bir bug | Daraja bo'yicha | Bug'ni tuzatgan kishi | Har bug uchun 1 ta, eng past darajada |
| Performance | Resurs va kechikish | p95/p99 latency, throughput, memory | Minutlar-soatlar | Performance muhandisi | Kritik oqimlar uchun; nightly |
| Security | Himoya qoidalari | AuthZ, input validatsiya, bog'liqlik CVE | Soniyalar-minutlar | Developer + AppSec | Har rol/endpoint matritsasi |
| Accessibility | Foydalanish imkoniyati | WCAG qoidalari, kontrast, ARIA (axe) | Soniyalar | Frontend + QA | Har asosiy ekran uchun |
| Chaos / resilience | Degradatsiya xatti-harakati | Timeout, retry, circuit breaker, fallback | Minutlar | SRE + arxitektor | 5-15 ta ssenariy, staging'da |
| Exploratory | Noma'lumni topish | Avtomat test o'ylamagan holatlar | Qo'lda, sessiyali | QA | Har release uchun vaqt oynasi |
| Mutation | Testlar sifati | Testlar haqiqatan xatoni tutadimi (PIT) | Minutlar-soatlar | Developer | Kritik domain paketlarida; nightly |

Jadvaldagi "qancha" ustuni mutlaq raqam emas, nisbat haqida: Spring loyihasida suite tarkibini `@Tag` bo'yicha hisoblab, bu nisbatlardan chetlanishni metrika sifatida kuzatish mumkin.

### 2.5 Qaysi mantiqni qaysi darajada testlash kerak

| Mantiq turi | Tavsiya etilgan daraja | Nega shu daraja | Qochish kerak |
|---|---|---|---|
| Domain qoidalari (narx, limit, status o'tishlari) | Sof unit (Spring konteksti yo'q) | Qoidalar I/O'ga bog'liq emas, variantlar ko'p | E2E'da hisob-kitob tekshirish |
| Validatsiya (Bean Validation) | Unit (`Validator`) + 1-2 slice (`@WebMvcTest`) HTTP 400 javobi uchun | Qoida unit'da, javob formati slice'da | Har bir constraint uchun controller testi |
| Mapping (DTO ↔ entity, MapStruct) | Unit, maydon-maydon | Tez, aniq, regressiyani yaxshi tutadi | `@SpringBootTest`da mapping tekshirish |
| SQL va query (JPQL, native, Criteria) | Integratsion, real DB (Testcontainers) | H2 dialekti xatoni yashiradi | H2/in-memory DB'ga tayanish |
| HTTP contract (status, JSON sxema, xato formati) | Slice (`@WebMvcTest`) + contract test | Serializatsiya va chegara shartnomasi | Faqat E2E'da contract tekshirish |
| Security qoidalari (rol, scope, ownership) | Slice `@WithMockUser`/`jwt()` bilan + bir nechta system test | Rol matritsasi arzon va to'liq qoplanadi | Faqat manual tekshiruv |
| Event oqimi (publish/consume, idempotentlik) | Integratsion (real broker konteyneri) + unit (handler mantiqi) | Serializatsiya va qayta yuborish faqat realda ko'rinadi | Mock broker bilan "ishladi" deb hisoblash |
| Tranzaksiya chegaralari (rollback, propagation) | Integratsion, real DB | Proxy va `@Transactional` semantikasi mock'da yo'q | Unit testda rollback'ni "tekshirish" |
| Retry / circuit breaker (Resilience4j) | Integratsion (stub server bilan) + chaos ssenariysi | Konfiguratsiya va vaqt o'lchamlari muhim | Konfiguratsiyani umuman testlamaslik |
| Konfiguratsiya (profil, `@ConfigurationProperties`, migratsiya) | Kontekst yuklanish testi + smoke | Noto'g'ri konfiguratsiya eng qimmat prod xatosi | Prod profilini hech qachon tekshirmaslik |

### 2.6 Test duplication: bir xil narsani ikki darajada testlash

Duplication piramidani ichdan buzadi: suite o'sadi, lekin ishonch o'smaydi. Tipik ko'rinishlari — bir xil hisob-kitob unit va E2E'da; validatsiyaning har bir qoidasi uchun alohida controller testi; `@SpringBootTest` ichida mapper'ni tekshirish.

Kesish uchun amaliy qoida — **har bir assertion uchun bitta "egasi" daraja**:

1. Har bir test holati uchun "eng past daraja, qaysiki bu xatoni tuta oladi" ni aniqlang va test shu yerda yashasin.
2. Yuqori daraja faqat *integratsiya faktini* tasdiqlasin: "controller to'g'ri servisni chaqirdi va natijani JSON qildi", "xabar broker'ga yetib bordi" — qiymatlar to'g'riligini emas.
3. E2E testlar uchun qattiq kvota belgilang (masalan, 15 ta) va yangi E2E qo'shish uchun eskisini olib tashlashni talab qiling.
4. Bug uchun regression test faqat bitta darajada yoziladi — bug qaysi darajada tutilishi mumkin bo'lsa, o'sha yerda.
5. Mutation testing bilan tekshiring: agar unit testni o'chirganda mutation score o'zgarmasa, u duplication.

### 2.7 Microservice va modular monolit uchun test taqsimoti namunasi

| Daraja | Microservice | Modular monolit | Kutubxona |
|---|---|---|---|
| Unit | 50-60% | 45-55% | 75-85% |
| Komponent / slice / modul | 20-25% | 25-30% | 5-10% |
| Integratsion (Testcontainers) | 10-15% | 10-15% | 10-15% |
| Contract | 3-5% | 1-2% (modullar orasida) | 0% |
| System / E2E | 1-3% | 3-5% | 0% |
| Nofunksional (perf, security, chaos) | ~1%, alohida pipeline | ~1% | kam |

Ishga tushish vaqti byudjeti — bu raqamlar CI'da gate sifatida majburlanishi kerak:

| Suite | Byudjet | Qachon ishlaydi |
|---|---|---|
| Unit (`*Test`, Spring konteksti yo'q) | < 60-90 s | Har commit, lokal watch |
| Slice + kontekst testlari | < 3 daqiqa | Har commit |
| Integratsion (`*IT`, Testcontainers) | < 8-10 daqiqa | Har PR |
| Contract verifikatsiya | < 2 daqiqa | Har PR |
| Smoke (deploy'dan keyin) | < 1 daqiqa | Har deploy |
| E2E + nofunksional | 20-60 daqiqa | Nightly va release oldidan |

Umumiy PR pipeline 15 daqiqadan oshmasligi maqsadli ko'rsatkich; oshsa, parallellashtirish yoki pastga ko'chirish talab qiladi.

### 2.8 Test nomlash va joylashtirish konvensiyasi

Konvensiya build vositasi tomonidan majburlansa ishlaydi. Maven Surefire sukut bo'yicha `**/Test*.java`, `**/*Test.java`, `**/*Tests.java`, `**/*TestCase.java` ni oladi; Failsafe esa `**/IT*.java`, `**/*IT.java`, `**/*ITCase.java` ni `integration-test` va `verify` fazalarida ishga tushiradi. Shuning uchun eng arzon ajratish — `*Test` = tez, `*IT` = sekin.

Tavsiya etilgan tuzilma (paket nomi production kodi bilan oynada bo'lsin, shunda package-private metodlar ham ko'rinadi):

```
src/test/java/com/acme/orders/
  domain/OrderTest.java                 // sof unit
  application/PlaceOrderServiceTest.java // unit + Mockito
  web/OrderControllerTest.java           // @WebMvcTest slice
  persistence/OrderRepositoryIT.java     // @DataJpaTest + Testcontainers
  OrderPlacementFlowIT.java              // @SpringBootTest
src/test/resources/application-test.yml
```

Maven konfiguratsiyasi — Surefire tezlarni, Failsafe sekinlarni oladi; `groups`/`excludedGroups` JUnit 5 tag ifodalariga o'tadi:

```xml
<plugin>
  <groupId>org.apache.maven.plugins</groupId>
  <artifactId>maven-surefire-plugin</artifactId>
  <configuration>
    <includes>
      <include>**/*Test.java</include>
      <include>**/*Tests.java</include>
    </includes>
    <excludes>
      <exclude>**/*IT.java</exclude>
    </excludes>
    <excludedGroups>slow | e2e</excludedGroups>
  </configuration>
</plugin>
<plugin>
  <groupId>org.apache.maven.plugins</groupId>
  <artifactId>maven-failsafe-plugin</artifactId>
  <configuration>
    <includes>
      <include>**/*IT.java</include>
    </includes>
    <groups>integration | slow</groups>
  </configuration>
  <executions>
    <execution>
      <goals>
        <goal>integration-test</goal>
        <goal>verify</goal>
      </goals>
    </execution>
  </executions>
</plugin>
```

Tag'larni har testda qo'lda yozish o'rniga, kompozit annotatsiya yaratish kerak — shunda semantika bitta joyda saqlanadi:

```java
@Target(ElementType.TYPE)
@Retention(RetentionPolicy.RUNTIME)
@Tag("integration")
@Tag("slow")
@SpringBootTest
public @interface IntegrationTest { }
```

Gradle'da ajratish `JvmTestSuite` orqali qilinadi (Java 17-25, JUnit Platform):

```kotlin
testing {
    suites {
        val test by getting(JvmTestSuite::class) {
            useJUnitJupiter()
            targets.all {
                testTask.configure {
                    useJUnitPlatform { excludeTags("slow", "e2e") }
                }
            }
        }
        val integrationTest by registering(JvmTestSuite::class) {
            dependencies { implementation(project()) }
            targets.all {
                testTask.configure {
                    shouldRunAfter(test)
                    useJUnitPlatform { includeTags("integration") }
                    maxParallelForks = 4
                }
            }
        }
    }
}

tasks.named("check") {
    dependsOn(testing.suites.named("integrationTest"))
}
```

Test nomi esa xatti-harakatni o'qiydigan gap bo'lishi kerak: metod nomi uchun `shouldRejectOrderWhenCreditLimitExceeded()` yoki `@DisplayName` bilan to'liq gap, `@Nested` klasslar bilan kontekstlarni guruhlash. `test1()`, `testOrder()` kabi nomlar code review'da to'xtatilishi lozim.

### 2.9 Arxitektor nazorat ro'yxati

- [ ] Loyiha uchun test shakli (piramida / Trophy / Honeycomb / Diamond) tanlangan va ADR'da sababi bilan yozilgan.
- [ ] Har bir mantiq turi (domain, validatsiya, mapping, SQL, contract, security, event, tranzaksiya, resilience, konfiguratsiya) uchun "egasi" daraja hujjatlashtirilgan.
- [ ] `*Test` va `*IT` ajratilgan, Surefire/Failsafe yoki Gradle `JvmTestSuite` konfiguratsiyasi shu ajratishni majburlaydi.
- [ ] `@Tag` taksonomiyasi cheklangan (masalan `integration`, `slow`, `e2e`, `security`) va kompozit annotatsiyalar orqali qo'llanadi.
- [ ] Har bir suite uchun vaqt byudjeti belgilangan va CI'da oshib ketganda signal beradi (PR pipeline < 15 daqiqa).
- [ ] E2E testlar soni uchun qattiq kvota mavjud; yangisini qo'shish eskisini pastga ko'chirishni talab qiladi.
- [ ] Integratsion testlar real DB/broker (Testcontainers) bilan ishlaydi, in-memory o'rnini bosuvchilar prod dialektini yashirmaydi.
- [ ] Duplication davriy ravishda tekshiriladi (suite tarkibi `@Tag` bo'yicha hisoblanadi, kritik paketlarda mutation score o'lchanadi).

---

## 3. Kim nima yozadi: rollar va mas'uliyat (Who Writes What — Roles & Responsibilities)

Testlash strategiyasi qog'ozda qanchalik go'zal bo'lsa ham, uni real hayotga aylantiradigan narsa — kim nimani yozadi, kim nimaga javob beradi va buzilgan testni kim tuzatadi degan savollarga berilgan aniq javoblardir. Amalda ko'p jamoalarda sifat "QA'ning ishi" deb atalib, developer'lar test yozishni majburiyat emas, balki qo'shimcha xizmat deb qabul qilishadi — natijada test piramidasi teskari aylanadi va release oldidan har doim panika boshlanadi. Bu bobda rollarni, RACI matritsasini, jamoa modellarini va test ownership masalasini arxitektor nuqtai nazaridan ko'rib chiqamiz. Maqsad — tashkiliy chizma chizish emas, balki sifat uchun javobgarlikni texnik qarorlar bilan bir xil joyga, ya'ni kodni yozadigan jamoaga yaqinlashtirish.

### 3.1 Rollar ta'rifi va farqi

Rol — bu lavozim emas, balki mas'uliyat to'plami. Kichik jamoada bitta odam uch-to'rt rolni olib yurishi mutlaqo normal; muhimi — rol egasi yo'q bo'lib qolmasligi. Spring loyihalarida eng ko'p uchraydigan rollar va ularning sifatga qo'shadigan hissasi quyidagicha.

| Rol | Asosiy mas'uliyat | Odatda yozadigan/boshqaradigan testlar | Muvaffaqiyat ko'rsatkichi |
|---|---|---|---|
| Developer | O'zi yozgan kodning ishlashiga javob beradi; testni kod bilan bir PR'da yetkazadi | Unit, slice (`@WebMvcTest`, `@DataJpaTest`), integratsion (Testcontainers), contract producer/consumer | PR'da test bor; o'z feature'idagi bug'lar soni kamayadi |
| QA Engineer (manual) | Exploratory testing, qabul kriteriyalarini tekshirish, edge case'larni kashf qilish | Qo'lda exploratory sessiyalar, qabul testi, UAT yordami | Production'ga chiqib ketgan bug'larning kamligi, topilgan muhim defektlar sifati |
| Automation QA / SDET | Avtomatlashtirish freymvorki, E2E va API test suite'lari, test ma'lumotlari vositalari | E2E (Selenium/Playwright), API testlar, `RestAssured` stsenariylari, test data builder'lar | Suite'ning barqarorligi, flaky foizi, ishlash vaqti |
| QA Lead | Sprint ichidagi sifat jarayoni, QA resurslarini taqsimlash, release sign-off | Test rejasi, regressiya qamrovi, risk bo'yicha prioritetlash | Release sign-off ishonchliligi, qamrov va risk muvofiqligi |
| Test Architect | Test strategiyasi, piramidaning shakli, test freymvork standartlari | Shablonlar, baza test klasslari, konvensiyalar, qamrov siyosati | Piramidaning real shakli, test yozish narxi (yangi test qancha vaqt oladi) |
| DevOps / Platform | CI/CD pipeline, test muhiti, Testcontainers uchun resurslar, parallel bajarilish | Infratuzilma, Docker image'lar, cache, test reportlari | Pipeline vaqti, muhit beqarorligidan kelgan nosozliklar soni |
| Product Owner | Testlanadigan qabul kriteriyalari, biznes qoidalarining aniqligi, prioritet | Qabul kriteriyalari, misollar (example), UAT qarori | Noaniq AC sababli qaytgan tasklar soni |
| Arxitektor | Testlanuvchanlikni dizaynga kiritish, modul chegaralari, contract'lar, nofunksional talablar | Arxitektura testlari (ArchUnit), contract chegaralari, SLA/SLO talablari | Testlash qiyin bo'lgan joylarning kamayishi, chegaralarning buzilmasligi |

Arxitektor bu ro'yxatda alohida o'rinda turadi: u test yozmasligi mumkin, lekin testlash mumkin bo'lmagan arxitektura uchun aynan u javobgar. Static metodlarga to'la util'lar, `new` bilan yaratilgan dependency'lar, bitta 4000 satrli service — bular QA muammosi emas, dizayn muammosi.

### 3.2 Mas'uliyat matritsasi (RACI)

RACI'da **R** (Responsible) — ishni bajaradigan, **A** (Accountable) — yakuniy javobgar (har qatorda faqat bitta), **C** (Consulted) — maslahat so'raladigan, **I** (Informed) — xabardor qilinadigan tomon. Quyidagi matritsa ko'pchilik Spring loyihalari uchun yaxshi boshlang'ich nuqta; uni jamoangizga moslashtirish kerak, lekin "A" ustunini bo'sh qoldirmang.

| Faoliyat | Developer | QA / SDET | QA Lead | Arxitektor / Test Architect | DevOps | PO |
|---|---|---|---|---|---|---|
| Unit test | **R** | I | I | **A** (standart) | – | – |
| Slice test (`@WebMvcTest`, `@DataJpaTest`) | **R** | C | I | **A** | I | – |
| Integratsion test (Testcontainers) | **R** | C | I | **A** | C | – |
| Contract test (producer/consumer) | **R** | C | I | **A** | C | I |
| E2E test | C | **R** | **A** | C | C | I |
| Performance test | C | **R** | C | **A** | C | I |
| Security test (SAST/DAST, authz) | C | **R** | I | **A** | C | I |
| Test ma'lumotlari (fixture, builder, seed) | **R** | **R** | C | **A** | C | C |
| Test infratuzilmasi va CI | C | C | I | C | **R/A** | – |
| Flaky test tozalash | **R** | **R** | C | **A** | C | – |
| Test strategiyasi va piramida shakli | C | C | C | **R/A** | C | I |
| Release sign-off | C | C | **R** | C | C | **A** |

Ikki muhim nuqta. Birinchi — unit va integratsion testlarda "A" arxitektorda, chunki standartni u belgilaydi, lekin "R" doimo developer'da: test yozishni delegatsiya qilish mumkin emas. Ikkinchi — release sign-off'da yakuniy javobgar PO, QA Lead emas. QA Lead risk haqida ma'lumot beradi, qarorni biznes qabul qiladi. Bu farq buzilganda QA "darvozabon" ga aylanadi va jamoa sifatni o'z zimmasidan oladi.

### 3.3 "Developer unit test yozadi, QA E2E yozadi" qoidasining chegaralari

Bu qoida boshlang'ich taqsimot sifatida foydali, lekin qattiq devorga aylansa quyidagi zararlarni keltiradi.

Birinchidan, o'rtadagi qatlam egasiz qoladi. Unit va E2E orasida service-to-service integratsiya, DB tranzaksiyalari, mapping, xato ishlovi va contract'lar bor. Developer "bu mening ishim emas, integratsiya — QA'da" deb o'ylaydi, QA esa "bu kod ichida, developer qarasin" deydi. Natija — bo'shliq E2E bilan to'ldiriladi, E2E sekin va flaky bo'ladi, piramida karamelga aylanadi.

Ikkinchidan, feedback aylanasi uzayadi. Developer o'z kodining integratsiyada ishlashini faqat QA sprintning oxirida tekshirgandan keyin biladi. Bir hafta oldin yozilgan kod kontekstini qayta tiklash — eng qimmat debug turi.

Uchinchidan, bilim bir tomonlama to'planadi. QA test dizayni texnikalarini biladi (boundary value, equivalence partitioning), developer esa kodning ichki tuzilishini biladi. Qattiq bo'linishda bu bilimlar almashmaydi: developer'ning unit testlari faqat happy path'ni tekshiradi, QA'ning E2E testlari esa kodning qaysi joyi xavfli ekanini bilmaydi.

To'g'ri yondashuv — "kim yozadi" emas, "kim qaysi riskka javob beradi". Developer kod ichidagi riskni yopadi (barcha darajada, unit'dan Testcontainers'gacha), QA esa foydalanuvchi va biznes riskini yopadi (exploratory, qabul, end-to-end stsenariylar). Qatlam emas, risk turi bo'yicha bo'linish barqarorroq.

### 3.4 Three Amigos va Example Mapping

Three Amigos — bu PO (nima kerak), developer (qanday qilamiz) va QA (qanday buzilishi mumkin) birgalikda user story'ni muhokama qiladigan 25–40 daqiqalik uchrashuv. Uning maqsadi test yozish emas, balki noaniqlikni kod yozilishidan oldin topish.

Example Mapping — bu muhokamani to'rt rangli kartada tuzadigan texnika: sariq — story, ko'k — qoida (biznes qoidasi / qabul kriteriyasi), yashil — misol (konkret stsenariy), qizil — savol (javobi yo'q, bloklovchi).

Misol: "Foydalanuvchi buyurtmani bekor qilishi mumkin" story'si.

- Qoida 1: faqat `NEW` yoki `PAID` statusdagi buyurtma bekor qilinadi.
  - Misol: `NEW` buyurtma → bekor qilindi, status `CANCELLED`.
  - Misol: `SHIPPED` buyurtma → `409 Conflict`, status o'zgarmaydi.
- Qoida 2: `PAID` buyurtma bekor qilinsa, to'lov avtomatik qaytariladi.
  - Misol: 100 000 so'm to'langan → refund `PaymentService`'ga yuboriladi, event `OrderCancelled` chiqadi.
  - Savol (qizil): refund xato bersa, buyurtma `CANCELLED` bo'lib qoladimi yoki rollback bo'ladimi?
- Qoida 3: bekor qilish faqat buyurtma egasi yoki `ROLE_SUPPORT` tomonidan.
  - Misol: boshqa foydalanuvchi → `403`.

Bu yerda eng qimmatli natija — qizil karta. U aniqlanmasa, developer o'zicha qaror qabul qiladi, QA boshqa narsani kutadi va bug sprintning oxirida chiqadi. Amaliy qoida: story'da ochiq qizil karta bo'lsa, u sprintga kirmaydi. Yashil misollar esa keyinchalik to'g'ridan-to'g'ri test nomlariga aylanadi — `shouldReturn409WhenCancellingShippedOrder` kabi.

### 3.5 QA'ning sprint ichidagi joyi

QA sprintning oxirida paydo bo'ladigan bosqich emas, balki butun sprint davomida ishtirok etadigan rol.

Grooming / refinement bosqichida QA eng foydali savollarni beradi: "bu holatda nima bo'ladi?", "chegara qiymati qanday?", "eski ma'lumotlar bilan nima qilamiz?", "bu o'zgarish qaysi integratsiyalarga ta'sir qiladi?". Bu bosqichda topilgan noaniqlik eng arzon.

Qabul kriteriyalarini testlanadigan holatga keltirish — QA'ning asosiy hissasi. "Tez ishlashi kerak" → "p95 javob vaqti 300 ms dan kam, 200 RPS yuklamada". "To'g'ri hisoblanishi kerak" → konkret kirish va chiqish qiymatlari jadvali.

Story ishlanayotganda QA tayyor bo'lgan qismni darhol tekshiradi (sprintning oxirini kutmaydi), exploratory sessiyalar o'tkazadi va avtomatlashtirish uchun stsenariylarni tanlaydi. Sprint oxirida regressiya ko'p hollarda avtomatik ishlaydi — QA faqat o'zgargan sohaga yo'naltirilgan qo'shimcha exploratory qiladi. Release sign-off esa "men ruxsat beraman" degani emas: QA risk hisobotini beradi — nima tekshirildi, nima tekshirilmadi, qanday ma'lum muammolar qoldi — qaror PO'da.

### 3.6 Test kodini code review qilish

Test kodi — production kodi. U ham o'qiladi, ham o'zgartiriladi, ham buziladi. Shuning uchun bir xil standartda review qilinishi kerak: formatlash, nomlash, duplikatsiyani kamaytirish, abstraksiya darajasi. Test kodida eng ko'p uchraydigan qarz — copy-paste qilingan setup va tushunarsiz magic constant'lar.

Review'ni kim qiladi: unit/integratsion testlarni boshqa developer; E2E va avtomatlashtirish freymvorkini SDET yoki QA Lead; yangi test turi yoki yangi baza klass qo'shilganda arxitektor ham ko'radi. Kichik jamoada QA developer'ning test PR'iga review qo'shilishi juda foydali — QA test dizayni bo'yicha bo'shliqlarni ko'radi.

Test review checklist:

- Test nomi nimani tekshirayotganini kod o'qimasdan tushuntiradimi?
- Bitta testda bitta sabab bormi (bir nechta mustaqil assertion bitta testga tiqilmaganmi)?
- Assertion mazmunlimi — `assertNotNull` yoki `assertTrue(true)` bilan "yashil" qilinmaganmi?
- Test implementatsiyani emas, xulq-atvorni tekshiradimi (mock'lar ichki chaqiruvlarni ko'chirib yozmaganmi)?
- Testlar bir-biridan mustaqilmi: tartibga, umumiy static holatga yoki oldingi testdan qolgan ma'lumotga bog'liq emasmi?
- `Thread.sleep`, haqiqiy tarmoq chaqiruvi, hardcode qilingan sana/vaqt yoki tasodifiy qiymat ishlatilmaganmi?
- Test ma'lumotlari builder/factory orqali, o'qiladigan holatda tayyorlanganmi?
- Negative va boundary holatlar qamrab olinganmi, yoki faqat happy path bormi?
- Test to'g'ri qatlamda turganmi — unit bilan yetarli bo'ladigan narsa uchun butun Spring context ko'tarilmaganmi?
- Test buzilganda xato xabari muammoni ko'rsatadimi (`AssertJ` tavsifli assertion'lar)?

### 3.7 Jamoa modellari

| Model | Kuchli tomoni | Kuchsiz tomoni | Qachon mos |
|---|---|---|---|
| Embedded QA (jamoa ichida) | Tez feedback, kontekstni chuqur bilish, Three Amigos tabiiy ishlaydi | QA'lar o'rtasida standart tarqaladi, bilim almashinuvi sust | Mustaqil product jamoalari, 5–9 kishilik squad'lar |
| Markazlashgan QA bo'limi | Yagona standart, resurslarni qayta taqsimlash oson, chuqur ekspertiza | "Devor ustidan tashlash", uzun feedback, QA bottleneck'ga aylanadi | Qattiq regulyatsiya, auditga tayyorlik, ko'p mahsulotli yirik tashkilot |
| QA enabling team (platforma sifatida) | Freymvork, shablon va CI'ni markaziy beradi, jamoalar o'zi yozadi | Jamoalarda minimal test madaniyati bo'lishi talab qilinadi | 5+ jamoa, o'sayotgan tashkilot, mikroservis landshaft |
| "QA yo'q" (developer-owned quality) | Eng qisqa feedback, to'liq ownership, tez release | Exploratory va UX riski ko'rinmaydi, developer ko'r nuqtalari qoladi | Kuchli muhandislik madaniyati, past biznes riski, SaaS va feature flag'lar |

Ko'p tashkilotlar uchun eng barqaror kombinatsiya — embedded QA plus kichik enabling team: har jamoada sifat egasi bor, umumiy freymvork va CI esa markazda saqlanadi.

### 3.8 Test ownership

Har bir test suite'ning nomma-nom egasi bo'lishi kerak — jamoa yoki shaxs, `CODEOWNERS` faylida qayd etilgan. Egasi yo'q suite muqarrar ravishda tark etiladi: flaky testlar `@Disabled` bo'ladi, qamrov pasayadi, keyin esa butun suite "ishonchsiz" deb o'chiriladi.

Buzilgan testni kim tuzatadi degan savolga eng sog'lom javob: testni buzgan o'zgarishni kiritgan odam. "Ishlatgan odam tuzatadi" qoidasi (you break it, you fix it) PR darajasida ishlaydi — qizil pipeline bilan PR merge qilinmaydi. Main branch'da test buzilgan bo'lsa, u eng yuqori prioritetli ish bo'ladi: yangi feature yozish to'xtaydi, chunki qizil main butun jamoani sekinlashtiradi.

On-call bilan bog'liq qoidalar: test infratuzilmasi nosozligi (muhit, Docker, registry) DevOps/Platform on-call'ga boradi; test mazmunidagi nosozlik — suite egasiga. Tungi nightly suite buzilsa, uni ertalab birinchi navbatda ko'radigan rotatsiya bo'lishi kerak, aks holda nightly natijalari oylar davomida hech kim o'qimaydigan email'ga aylanadi.

### 3.9 1 QA va 5 developer: kichik jamoa uchun amaliy model

O'zbekistondagi ko'p jamoalarda real nisbat 1:5 yoki 1:8. Bu holatda QA'ni hamma narsani test qiluvchi sifatida ishlatish — eng keng tarqalgan xato: u bottleneck'ga aylanadi va sprint oxirida "QA ulgurmadi" degan doimiy holat paydo bo'ladi.

Ishlaydigan taqsimot quyidagicha. Developer'lar barcha kod ichidagi testlarni o'zi yozadi va egalik qiladi: unit, slice, Testcontainers bilan integratsion, contract. Bu muhokama mavzusi emas — Definition of Done'ga yoziladi va PR'da tekshiriladi. QA kod yozishdan ko'ra ko'proq "sifat dizayneri" bo'ladi: grooming'da qatnashadi, qabul kriteriyalarini misollar bilan to'ldiradi (Example Mapping), har story uchun qisqa risk ro'yxatini beradi va eng ko'p vaqtini exploratory testing'ga sarflaydi — chunki aynan shu ishni developer o'rniga bajara olmaydi.

E2E suite'ni kichik ushlab turish shart: 10–20 ta eng muhim biznes yo'li, boshqa hech narsa. Bu suite'ni yozishda QA stsenariyni belgilaydi, developer esa texnik qismini yozadi (yoki juftlikda ishlashadi) — bunda QA avtomatlashtirish bo'yicha ortiqcha yuklanmaydi va suite jamoa bilimida qoladi.

Qolgan ishlar aniq egalarga tarqatiladi: CI/CD va test muhiti — bitta developer "build egasi" sifatida (yoki DevOps bo'lsa, u); performance testlari — talab paydo bo'lganda arxitektor bilan birga; security skanerlar — pipeline'da avtomatik. Arxitektor esa testlanuvchanlikni dizaynga kiritadi va shablonlarni beradi, shunda yangi test yozish 20 daqiqalik ish bo'ladi, bir kunlik emas. Qoida sodda: QA bitta bo'lsa, u testlarni emas, sifat jarayonini masshtablashi kerak.

### 3.10 Arxitektor nazorat ro'yxati

- [ ] Har bir test turi uchun RACI'da "Accountable" aniq belgilangan va hech bir qator egasiz emas.
- [ ] Definition of Done'da developer uchun unit, slice va integratsion test majburiyati yozilgan va PR'da tekshiriladi.
- [ ] Three Amigos yoki Example Mapping jarayoni mavjud; ochiq "qizil karta"li story sprintga kirmaydi.
- [ ] Test kodi production kodi bilan bir xil review standartida va test review checklist jamoada qo'llaniladi.
- [ ] Har bir test suite'ning egasi `CODEOWNERS` yoki shunga teng joyda qayd etilgan.
- [ ] Buzilgan test uchun "kim tuzatadi" qoidasi yozilgan, qizil main branch eng yuqori prioritet deb qabul qilingan.
- [ ] Tanlangan jamoa modeli (embedded / markazlashgan / enabling / developer-owned) ongli ravishda tanlangan, tasodifiy shakllanmagan.
- [ ] QA soni kam bo'lsa, QA vaqti exploratory va qabul kriteriyalariga, regressiya esa avtomatlashtirishga yo'naltirilgan.

---

## 4. Testrovshik qanday ishlashi kerak: QA ish jarayoni (How a Tester Actually Works — The QA Workflow)

Ko'pchilik arxitektorlar QA ishini "testni bosib ko'rish" deb tasavvur qiladi, lekin haqiqiy QA mutaxassisining kunining katta qismi talablarni tahlil qilish, risklarni baholash va topilganlarni boshqalar tushunadigan tilda yozishga ketadi. Bu bob QA'ning kundalik ritmini, test dizayn texnikalarini, defekt bilan ishlash standartini va qo'lda testlashdan avtomatlashtirishga o'tish mezonlarini bosqichma-bosqich ko'rsatadi. Arxitektor uchun bu bob ikki jihatdan muhim: birinchidan, siz QA'dan nima kutish kerakligini bilib olasiz; ikkinchidan, QA ishini imkonsiz qiladigan arxitektura qarorlarini (masalan trace ID yo'qligi yoki muhitlar nomosligi) oldindan ko'rasiz. Quyidagi barcha misollar bitta domenda — kredit limiti va buyurtma statuslari ustida — qurilgan, shuning uchun texnikalarni bir-biriga qiyoslash oson.

### 4.1 QA'ning ish oqimi va sprint ritmi

QA ishi chiziqli emas, aylanma: har bir talab bir necha bosqichdan o'tadi va har bosqichda orqaga qaytish ehtimoli bor. To'liq oqim quyidagicha ko'rinadi.

**1. Talabni o'qish.** QA user story'ni, qabul kriteriyalarini (acceptance criteria), maketlarni va bog'liq API shartnomasini o'qiydi. Maqsad — "nima qurilayotganini" emas, "nima buzilishi mumkinligini" tushunish.

**2. Savol berish.** Noaniq joylar ro'yxatga olinadi va business analyst yoki product owner'ga beriladi. Bu bosqich eng arzon bug tuzatish nuqtasi: hali kod yozilmagan.

**3. Qabul kriteriyalarini aniqlashtirish.** Noaniq kriteriya testlanadigan shaklga qayta yoziladi. Natija — story'ning Definition of Ready holatiga yetishi.

**4. Test dizayni.** Texnikalar qo'llanadi (ekvivalentlik sinflari, chegaralar, qaror jadvali), test case'lar va checklist'lar tayyorlanadi, risk yuqori bo'lgan joylarga ko'proq e'tibor beriladi.

**5. Testni bajarish.** Yangi funksionallik test qilinadi: avval smoke, keyin asosiy scenariylar, keyin chegaralar va salbiy holatlar, oxirida exploratory session.

**6. Defekt ochish.** Topilgan muammo standart formatda yoziladi, severity taklif qilinadi, log va trace ID ilova qilinadi.

**7. Retest.** Developer tuzatgandan keyin QA aynan o'sha qadamlarni qaytaradi va yondosh joylarni ham tekshiradi (tuzatish nimani buzgan bo'lishi mumkin?).

**8. Regressiya.** Risk asosida tanlangan regression suite ishga tushiriladi — qo'lda yoki avtomatik.

**9. Sign-off.** QA release holatini yozma bayon qiladi: nima test qilindi, nima qilinmadi, qanday ochiq risklar bor. Sign-off "bug yo'q" degani emas — "ma'lum risklar qabul qilinadigan darajada" degani.

Sprint bo'yicha kunlik ritm (ikki haftalik sprint misolida):

| Sprint kuni | QA'ning asosiy faoliyati | Chiqish artefakti |
| --- | --- | --- |
| 1-2 | Backlog refinement, talablarni tahlil, savollar | Aniqlashtirilgan AC, risk ro'yxati |
| 2-4 | Test dizayni, test ma'lumotlari talabi | Test case'lar, checklist |
| 4-8 | Tayyor bo'lgan story'larni testlash, defekt ochish | Bug report'lar, test natijalari |
| 6-9 | Retest, avtomatlashtirishga nomzodlarni belgilash | Yopilgan defektlar, avtomatlashtirish backlog'i |
| 9 | Regressiya (risk asosida qisqartirilgan) | Regression hisoboti |
| 10 | Sign-off, release notes'ga QA qismi, retrospektiva | Sign-off xati, escaped defect tahlili |

Amalda bu bosqichlar parallel ketadi: QA ertalab kechagi defektlarni retest qiladi, kunduzi yangi story'ni testlaydi, kun oxirida keyingi story uchun test dizayn qiladi. Arxitektor uchun muhim xulosa: agar QA sprintning faqat oxirgi ikki kunida ishga tushsa, bu jarayon buzilgan — testlash "siqilib" qoladi va regressiya hisobidan qisqartiriladi.

### 4.2 Talablarni testlash

Talabni testlash — kod yozilmasdan oldin bajariladigan eng foydali test turi. QA talabga qarab bir necha savol beradi: bu shart o'lchanadimi? chegarasi qayerda? xato holatida nima bo'ladi? kim ko'rishi mumkin? Agar savolga javob yo'q bo'lsa, talab testlanmaydi.

Testlanmaydigan qabul kriteriyasining tipik belgilari: "tez ishlashi kerak", "qulay bo'lishi kerak", "to'g'ri hisoblanishi kerak", "kerakli hollarda xabar chiqsin". Bularda o'lchov, chegara va aktor yo'q.

| Yomon qabul kriteriyasi | Nega yomon | Qayta yozilgan (yaxshi) variant |
| --- | --- | --- |
| "Kredit limiti to'g'ri hisoblanishi kerak" | "To'g'ri" aniqlanmagan, formula yo'q | "Daromadi 10 000 000 so'mdan yuqori va kechikishi 0 bo'lgan mijoz uchun limit = daromad × 3, maksimum 50 000 000 so'm" |
| "Tizim tez javob bersin" | O'lchov va yuk darajasi yo'q | "`POST /api/credit-limit` 100 RPS yukda p95 < 400 ms javob qaytaradi" |
| "Noto'g'ri ma'lumotda xato ko'rsatilsin" | Qaysi xato, qanday kod, qaysi maydon — noaniq | "Daromad maydoni bo'sh bo'lsa, HTTP 400 va `{\"field\":\"income\",\"code\":\"REQUIRED\"}` qaytadi" |
| "Admin hamma narsani ko'ra oladi" | Rollar va resurslar aniqlanmagan | "ROLE_ADMIN barcha mijozlarning limit tarixini ko'radi; ROLE_AGENT faqat o'z filialidagi mijozlarni ko'radi; boshqasiga 403" |
| "Buyurtma bekor qilinsin" | Qaysi statuslardan bekor qilish mumkinligi aytilmagan | "NEW va PAID statuslarida bekor qilish mumkin; SHIPPED va DELIVERED'da 409 va `ORDER_NOT_CANCELLABLE` qaytadi" |

Yaxshi qabul kriteriyasining mezonlari: (1) aktor ko'rinadi, (2) shart o'lchanadi, (3) kutilgan natija bitta ma'noda tushuniladi, (4) xato yo'li ham yozilgan, (5) chegaralar raqam bilan berilgan. QA bu beshtasini har bir story uchun tekshirib chiqadi va yetishmaganini savol sifatida qaytaradi.

### 4.3 Test dizayn texnikalari

Test dizayn — cheksiz ko'p variantdan foydali bo'lganini tanlash san'ati. Quyida har bir texnika va uning aniq misoli.

**Ekvivalentlik sinflari (equivalence partitioning).** Kirish qiymatlarini bir xil ishlov ko'radigan guruhlarga bo'lamiz va har guruhdan bittasini tekshiramiz. Kredit limiti misolida daromad maydoni: manfiy qiymatlar (xato), 0–999 999 (limit berilmaydi), 1 000 000–9 999 999 (bazaviy limit), 10 000 000 va yuqori (×3 limit), raqam bo'lmagan matn (validatsiya xatosi). Beshta sinf — beshta test, 10 000 ta qiymat emas.

**Chegara qiymatlari (boundary value analysis).** Xatolar aksariyat chegarada yashaydi. Yuqoridagi `>= 10 000 000` sharti uchun tekshirilishi kerak bo'lgan nuqtalar: 9 999 999, 10 000 000, 10 000 001. Limit maksimumi 50 000 000 bo'lsa: daromad 16 666 666 (limit 49 999 998), 16 666 667 (50 000 001 → 50 000 000 ga qisqaradi). Ikki chegarani birlashtirish `>` va `>=` xatosini (klassik off-by-one) darhol ochadi.

**Qaror jadvali (decision table).** Bir necha shart birgalikda natijani belgilaganda ishlatiladi. Kredit limiti qarori:

| # | Daromad >= 10 mln | Kechikish tarixi bor | KYC tasdiqlangan | Kutilgan natija |
| --- | --- | --- | --- | --- |
| R1 | Ha | Yo'q | Ha | Limit = daromad × 3 (max 50 mln) |
| R2 | Ha | Yo'q | Yo'q | `KYC_REQUIRED`, limit 0 |
| R3 | Ha | Ha | Ha | Limit = daromad × 1 (qo'lda ko'rib chiqish) |
| R4 | Ha | Ha | Yo'q | `KYC_REQUIRED`, limit 0 |
| R5 | Yo'q | Yo'q | Ha | Limit = 1 mln (boshlang'ich) |
| R6 | Yo'q | Yo'q | Yo'q | `KYC_REQUIRED`, limit 0 |
| R7 | Yo'q | Ha | Ha | `DECLINED` |
| R8 | Yo'q | Ha | Yo'q | `KYC_REQUIRED`, limit 0 |

Jadval sakkizta qatorni beradi va darhol ko'rinadi: KYC yo'q bo'lsa boshqa shartlar ahamiyatsiz. Shu sababli R2, R4, R6, R8'ni bitta qoidaga birlashtirib, test sonini 8'dan 5'ga tushirish mumkin — bu qaror jadvalining asosiy foydasi: ortiqcha testni ko'rsatadi.

**Holat o'tishlari (state transition).** Buyurtma statuslari: NEW → PAID → SHIPPED → DELIVERED, hamda NEW/PAID → CANCELLED va DELIVERED → RETURNED. Test dizayni uchta qismdan iborat: (a) ruxsat etilgan har bir o'tish ishlaydi, (b) ruxsat etilmagan o'tish rad etiladi (SHIPPED → CANCELLED → 409), (c) bir xil o'tishning takrori idempotent (PAID → PAID ikkinchi to'lov hodisasida ikkinchi marta hisoblanmaydi). Arxitektor uchun signal: agar status o'tishlari kodda `if` lar to'dasiga sochilgan bo'lsa, QA ularni to'liq qamray olmaydi — o'tish qoidalari bitta joyda (state machine) saqlanishi kerak.

**Pairwise / orthogonal array.** Ko'p parametrli konfiguratsiyada barcha kombinatsiya portlashini kamaytiradi. Masalan: valyuta (UZS, USD), kanal (mobil, web, filial), mijoz turi (jismoniy, yuridik), to'lov usuli (karta, pul ko'chirish) — 2×3×2×2 = 24 kombinatsiya. Pairwise yondashuv har juft qiymat kamida bir marta uchrashishini kafolatlab, bu sonni 6-7 testga tushiradi. Amaliyotda defektlarning katta qismi ikki parametrning o'zaro ta'siridan kelib chiqadi, shuning uchun pairwise qamrov/xarajat nisbati bo'yicha juda samarali.

**Use case testing.** Foydalanuvchining to'liq yo'lini boshidan oxirigacha tekshiradi: mijoz ro'yxatdan o'tadi → KYC yuboradi → limit so'raydi → buyurtma yaratadi → to'laydi → yetkazib berishni kuzatadi. Bu texnika alohida birliklar to'g'ri, lekin birgalikda ishlamaydigan holatlarni ochadi (masalan limit berildi, ammo buyurtma yaratishda limit tekshirilmadi).

**Xato taxmin qilish (error guessing).** Tajribaga asoslangan texnika: QA qayerda xato bo'lishi ehtimolini taxmin qiladi. Tipik nomzodlar: bo'sh ro'yxat, bitta elementli ro'yxat, `null`, juda uzun matn (255+ belgi), emoji va maxsus belgilar, ikki marta tez bosilgan "To'lash" tugmasi (double submit), vaqt zonasi chegarasi (23:59 va 00:01), yil oxiri, sessiya tugashi, tarmoq uzilishi o'rtasida yuborilgan so'rov.

**CRUD matritsasi.** Har bir entity uchun to'rt amal × ruxsat/holat kesishmasi tekshiriladi. Bu "o'chirilgan yozuvni yangilash" yoki "boshqa filial mijozini ko'rish" kabi teshiklarni muntazam ochadi.

| Entity | Create | Read | Update | Delete |
| --- | --- | --- | --- | --- |
| CreditLimit | AGENT: ha; CUSTOMER: yo'q (403) | Egasi va AGENT: ha | Faqat ADMIN, audit log yoziladi | Soft delete; o'chirilgandan keyin Read 404 |
| Order | CUSTOMER: ha | Egasi: ha; boshqa: 403 | Faqat NEW statusida | DELIVERED'ni o'chirish taqiqlanadi (409) |

### 4.4 Test case yozish

Test case — boshqa odam (yoki kelgusi yildagi o'zingiz) hech nima so'ramasdan bajara oladigan yozma ko'rsatma. Standart tuzilishi:

```
ID:            TC-CREDIT-014
Sarlavha:      10 mln chegarasida limit x3 hisoblanadi
Bog'liq talab: STORY-452 / AC-3
Prioritet:     High
Dastlabki shart (precondition):
  - Mijoz KYC_APPROVED holatida
  - Kechikish tarixi bo'sh
  - Test ma'lumoti: customer_id = CUST-1001
Test ma'lumoti:
  income = 10 000 000 (chegara nuqtasi)
Qadamlar:
  1. POST /api/credit-limit so'rovini customer_id va income bilan yubor
  2. Javob kodi va tanasini o'qi
  3. GET /api/credit-limit/CUST-1001 bilan saqlangan qiymatni tekshir
Kutilgan natija:
  - 2-qadam: HTTP 200, body.limit = 30 000 000, body.reason = "INCOME_TIER_3"
  - 3-qadam: saqlangan limit = 30 000 000, audit log'da LIMIT_ASSIGNED hodisasi bor
Keyingi holat (postcondition):
  - Mijoz limiti o'zgargan, boshqa mijozlarga ta'sir yo'q
Avtomatlashtirish: ha (API darajasida, regression suite'ga kiradi)
```

Yaxshi test case belgilari: bitta maqsadni tekshiradi; dastlabki shart to'liq yozilgan; qadamlar imperativ va aniq (tugma nomi, endpoint, maydon); kutilgan natija o'lchanadigan; test ma'lumoti test ichida ko'rsatilgan yoki fixture'ga havola qilingan; boshqa test case'ning natijasiga bog'liq emas (mustaqil); bajarilgandan keyin muhitni iflos qoldirmaydi.

Yomon test case belgilari: "tizim to'g'ri ishlashini tekshir" kabi noaniq kutilgan natija; 30 qadamli zanjir; "oldingi test case'dan keyin bajariladi" degan bog'liqlik; UI piksel joylashuviga bog'langan qadamlar.

**Checklist va test case farqi.** Checklist — tekshirilishi kerak bo'lgan narsalar ro'yxati, qadamlarsiz ("limit chegarasi 10 mln", "KYC yo'q holati", "manfiy daromad", "403 boshqa filial"). Tajribali QA uchun checklist tezroq va moslashuvchan. Test case — batafsil skript, yangi odam yoki audit talab qilgan joyda (masalan regulyator talabi, sertifikatsiya) kerak. Amaliy qoida: yangi funksionallikni exploratory + checklist bilan tekshiring, barqarorlashgan va takrorlanadigan qismini test case'ga aylantirib avtomatlashtiring.

**Qachon avtomatlashtirish kerak.** Test case avtomatlashtirishga munosib bo'ladi, agar: u har release'da bajariladi; natijasi deterministik; biznes uchun yuqori risk ko'taradi (to'lov, limit, ruxsatlar); qo'lda bajarish qimmat yoki zerikarli (katta ma'lumot to'plami bilan hisob-kitob); regressiya ehtimoli yuqori (ko'p o'zgaradigan kod). Qo'lda qolishi kerak bo'lganlar: bir martalik migratsiya tekshiruvi, vizual estetika va UX hissi, hali shakli o'zgarib turgan yangi ekran, murakkab tashqi tizim bilan qo'lda sozlanadigan holatlar.

### 4.5 Exploratory testing

Exploratory testing — "tasodifiy bosib ko'rish" emas, balki boshqarilgan tadqiqot. Eng keng tarqalgan format — session-based test management (SBTM): aniq charter, qat'iy timebox va yozma hisobot.

**Charter yozish.** Charter — session maqsadining bir-ikki gaplik ta'rifi. Shablon: "`<nimani>` ni `<qanday vositalar bilan>` o'rganib, `<qanday ma'lumotni>` topish". Misollar: "Kredit limiti hisoblanishini chegara qiymatlari va KYC statuslari kombinatsiyasi bilan o'rganib, noto'g'ri limit beradigan holatlarni topish"; "Buyurtma bekor qilish oqimini parallel so'rovlar bilan o'rganib, status race condition'larini topish".

**Timebox.** Odatda 60 yoki 90 daqiqa. Vaqt tugasa session tugaydi — topilgan narsa yozilib, keyingi charter rejalashtiriladi. Timebox ikki foyda beradi: diqqat tarqalmaydi va ish hajmi rejalashtirish mumkin bo'ladi.

**Tour'lar** — tadqiqot yo'nalishini beruvchi metaforalar:

- **Pul yo'li (money tour).** Mahsulot pul topadigan oqimni kuzatish: limit → buyurtma → to'lov → hisob-faktura. Bu yo'ldagi bug eng qimmat.
- **Xato yo'li (bad-neighborhood / error tour).** Ataylab xato qilish: bo'sh maydon, noto'g'ri format, muddati o'tgan token, ikki marta to'lov, tarmoqni uzish.
- **Sertifikat yo'li (landmark tour).** Qabul kriteriyalarini "nishon" sifatida belgilab, ular orasida erkin yurish.
- **Orqa ko'cha (back-alley tour).** Eng kam ishlatiladigan funksiyalarni sinash — ular eng kam test qilingan.
- **Supervisor yo'li (configuration tour).** Rollar, sozlamalar, feature flag'lar kombinatsiyalarini almashtirish.

**Topilganlarni yozib borish.** Session davomida QA bitta oddiy jurnal yuritadi: vaqt, qilingan harakat, kuzatilgan natija, savol yoki shubha. Session oxirida hisobot uchta qismdan iborat bo'ladi: (1) charter va sarflangan vaqt taqsimoti (test / setup / bug yozish), (2) topilgan defektlar ro'yxati va ularning havolalari, (3) yangi savollar va keyingi charter takliflari. Bu hisobot regression suite'ni boyitishning asosiy manbai: exploratory'da topilgan har bir jiddiy bug uchun avtomatlashtirilgan regression test yozilishi kerak.

### 4.6 Defekt hisoboti standarti

Bug report — developer uchun yozilgan texnik hujjat. Uning yagona vazifasi: muammoni minimal vaqtda qayta ishlab chiqarishga (reproduce) imkon berish.

**Sarlavha formulasi:** `<qayerda> <qanday shartda> <nima noto'g'ri bo'ladi>`. Misol: "Kredit limiti: daromad aynan 10 000 000 bo'lganda limit ×1 hisoblanadi (×3 kutilgan)".

Yomon bug report misoli:

```
Sarlavha: Limit ishlamaydi
Tavsif:   Limitni tekshirdim, natija xato. Tuzatinglar.
```

Bu hisobotda muhit, qadamlar, ma'lumot, kutilgan natija va log yo'q — developer QA bilan ikki marta yozishmasdan boshlay olmaydi.

Yaxshi bug report shabloni:

```
ID:        BUG-2291
Sarlavha:  Kredit limiti: income = 10 000 000 da limit x1 hisoblanadi (x3 kutilgan)

Muhit:
  Stend:      QA (qa-2.internal)
  Backend:    credit-service 1.14.3 (build #872, commit a3f91c2)
  Baza:       PostgreSQL 15, schema migration V41
  Mijoz:      REST API (curl), Chrome 139 (UI orqali ham takrorlanadi)
  Vaqt:       2026-10-02 11:24 (UTC+5)

Dastlabki shart:
  customer_id = CUST-1001, KYC_APPROVED, kechikish tarixi bo'sh

Qayta ishlab chiqarish qadamlari:
  1. POST /api/credit-limit
     {"customerId":"CUST-1001","income":10000000}
  2. Javobni o'qi

Kutilgan natija:
  HTTP 200, limit = 30000000, reason = "INCOME_TIER_3"
  (STORY-452 / AC-3 ga muvofiq)

Kuzatilgan natija:
  HTTP 200, limit = 10000000, reason = "INCOME_TIER_1"

Takrorlanish:  3/3 (har safar takrorlanadi)
Trace ID:      4b9f1ad2c77e4e1b9a1f0c3d8e2b5a66
Log parchasi:  CreditLimitCalculator.java:88 -> "tier resolved: TIER_1 for income=10000000"
Ilova:         curl-request.txt, response.json, screenshot-ui.png, screen-recording.mp4
Severity:      Major (QA taklifi)
Priority:      (triage belgilaydi)
Bog'liq talab: STORY-452
Vaqtinchalik yechim: daromadni 10 000 001 kiritish
```

**Severity va priority farqi.** Severity — defektning texnik/biznes ta'sir kuchi (tizim qanchalik buzilgan). Priority — uni qachon tuzatish kerakligi (navbatdagi o'rni). Ikkisi mustaqil: bosh sahifadagi logotip xato yozilishi severity bo'yicha Minor, lekin priority bo'yicha Critical bo'lishi mumkin (brend zarari, release blocker). Teskarisi ham bo'ladi: kam ishlatiladigan hisobotni eksport qilishda crash — severity Critical, priority Low.

Kim belgilaydi: **severity'ni QA** belgilaydi (u ta'sirni o'z ko'zi bilan ko'rgan), **priority'ni product owner / triage** belgilaydi (u biznes navbatini biladi). Arxitektor texnik risk (ma'lumot buzilishi, xavfsizlik, migratsiya) haqida ovoz beradi.

| Severity ↓ / Priority → | Critical (shu release) | High (joriy sprint) | Medium (keyingi sprint) | Low (backlog) |
| --- | --- | --- | --- | --- |
| **Blocker** (ishni to'xtatadi) | To'lov umuman o'tmaydi | Faqat test stendda deploy buzilgan | — | — |
| **Critical** (ma'lumot/pul buzilishi) | Limit ikki marta hisoblanadi | Kam uchraydigan valyutada noto'g'ri kurs | Eski arxiv hisobotida xato summa | — |
| **Major** (asosiy funksiya ishlamaydi) | Chegara qiymatida noto'g'ri limit | Buyurtma bekor qilish 500 qaytaradi | Filtr noto'g'ri tartiblanadi | Kam ishlatiladigan eksport ishlamaydi |
| **Minor** (noqulaylik, chetlab o'tish bor) | Logotipda xato yozilgan nom | Xato xabari ingliz tilida | Tooltip kesilgan | Formatlash nomuvofiqligi |

### 4.7 Defekt hayot aylanishi va triage

Standart holatlar va o'tishlar:

| Holat | Kim o'tkazadi | Ma'nosi va chiqish sharti |
| --- | --- | --- |
| **New** | QA | Yangi yozilgan defekt, hali ko'rib chiqilmagan |
| **Triage** | PO + Tech lead + QA | Tasdiqlanadi, severity/priority va egasi belgilanadi |
| **In Progress** | Developer | Tuzatish ustida ish ketmoqda |
| **Ready for Test** | Developer | Tuzatish qaysi build/muhitda ekani ko'rsatilgan |
| **Reopened** | QA | Retest o'tmadi — aynan qadamlar va yangi log bilan qaytariladi |
| **Closed** | QA | Retest o'tdi, regression test qo'shildi (kerak bo'lsa) |
| **Won't Fix** | PO (QA xabardor) | Ongli qaror: sabab va qabul qilingan risk yozma qayd etiladi |

Qo'shimcha holatlar amalda uchraydi: `Duplicate` (mavjud defektga havola bilan), `Cannot Reproduce` (QA qo'shimcha ma'lumot — trace ID, video — beradi va qayta ochadi), `Deferred` (keyingi release'ga ko'chirildi).

**Triage uchrashuvi** — qisqa (20-30 daqiqa), muntazam (kuniga yoki kunora bir marta) va qat'iy formatli yig'ilish. Qatnashchilar: product owner (biznes prioriteti), tech lead yoki arxitektor (texnik ta'sir va murakkablik), QA (ta'sir va takrorlanish ma'lumoti). Har bir yangi defekt uchun to'rtta qaror qabul qilinadi: (1) bu haqiqatan defektmi yoki yangi talabmi? (2) severity to'g'ri baholanganmi? (3) priority qanday — shu release'da, keyingi sprintda yoki backlog'da? (4) egasi kim? Triage'da bug'ni muhokama qilib yechim o'ylash taqiqlanadi — bu alohida suhbat, aks holda uchrashuv cho'ziladi. Arxitektorning roli: bir xil sababdan kelayotgan defekt guruhlarini payqash ("oxirgi haftada beshta defekt status o'tishlariga bog'liq") va ularni bitta arxitektura ishiga aylantirish.

### 4.8 Regressiya testlash

Regressiya — oldin ishlagan funksionallik hali ham ishlayotganini tekshirish. Asosiy qiyinchilik: hamma narsani har safar tekshirish imkonsiz, demak tanlash kerak.

**Regression suite'ni tanlash mezonlari:** biznes uchun kritik oqimlar (pul yo'li) — har safar; o'zgargan kod atrofidagi funksionallik (change impact analysis) — har safar; tarixda ko'p bug chiqqan modullar — har safar; integratsiya nuqtalari va shartnomalar — har safar; kam ishlatiladigan va barqaror qismlar — kamroq (masalan har uchinchi release'da).

**Smoke va regression farqi:** smoke — "tizim umuman tirikmi?" degan 5-15 daqiqalik tekshiruv (login ishlaydi, asosiy sahifa yuklanadi, bitta buyurtma yaratiladi, health endpoint 200 qaytaradi). Regression — "oldingi funksionallik buzilmaganmi?" degan kengroq, bir necha soatlik yoki avtomatik holda o'n-o'n besh daqiqalik to'plam. Release oldidan tartib: deploy → smoke (qisqa, deploy to'g'riligini tasdiqlaydi) → regression (risk asosida tanlangan) → yangi funksionallik testi → sign-off.

**Risk asosida qisqartirish.** Har bir modulga ikki ko'rsatkich beriladi: buzilish ehtimoli (o'zgarish hajmi, kod murakkabligi, tarixiy defektlar) va buzilish narxi (foydalanuvchi soni, pul, regulyativ ta'sir). Ikkisi yuqori bo'lgan modullar to'liq test qilinadi; biri yuqori bo'lganlar qisqartirilgan to'plam bilan; ikkisi past bo'lganlar faqat smoke bilan qoplanadi. Bu yondashuv sign-off'da "nima test qilinmadi" savoliga aniq javob berish imkonini beradi — "past riskli X moduli faqat smoke bilan qoplandi" degan yozuv to'liq legitim.

### 4.9 Muhitlar (environments)

Muhitlar nomuvofiqligi QA ishini buzadigan birinchi sabab. Arxitektor har bir muhit uchun uchta narsani aniq belgilashi kerak: kim egasi, ma'lumot qayerdan keladi, qaysi versiyalar turadi.

| Muhit | Egasi | QA nima qiladi | Ma'lumot holati | Versiyalar mosligi |
| --- | --- | --- | --- | --- |
| **local** | Developer | QA kirmaydi (ba'zan bug'ni takrorlash uchun) | Embedded/Testcontainers, har ishga tushishda toza | Faqat joriy branch |
| **dev** | Developer jamoasi | Smoke, erta fikr-mulohaza | Beqaror, tez-tez tozalanadi | Har commit'da o'zgaradi, beqaror |
| **test / QA** | QA | Asosiy test ishi: yangi funksionallik, defekt tekshiruvi, exploratory | Boshqariladigan seed ma'lumot, QA tiklashi mumkin | Sprint build'lari, mock yoki stub'langan tashqi tizimlar |
| **staging** | QA + Release manager | Regressiya, integratsiya, E2E, release repetitsiyasi | Prod'ga o'xshash hajm, maskalangan (anonimlashtirilgan) ma'lumot | Prod'ga teng konfiguratsiya, haqiqiy tashqi tizimlarning sandbox'lari |
| **pre-prod** | Release manager / SRE | Oxirgi smoke, migratsiya repetitsiyasi, performance tekshiruvi | Prod nusxasi yoki prod'ga juda yaqin | Prod bilan aynan bir xil artefakt |
| **prod** | SRE / Operations | Faqat read-only smoke, monitoring kuzatuvi, canary tekshiruvi | Haqiqiy mijoz ma'lumoti — o'zgartirish taqiqlanadi | Release qilingan versiya |

QA uchun amaliy qoidalar: bug report'da muhit, build raqami va commit hash majburiy; "faqat staging'da takrorlanadi" degan defekt alohida e'tibor talab qiladi (konfiguratsiya farqi odatda sabab); test muhitida ma'lumotni tiklash (reset) QA o'zi bajara olishi kerak, developer'dan so'ramasdan; har bir muhitda tashqi tizim sandbox'i yoki stub'i aniq hujjatlashtirilgan bo'lishi kerak.

Arxitektor uchun ogohlantirish belgilari: QA muhiti haftada bir necha marta ishdan chiqadi; har bir muhitda schema versiyasi boshqa; test ma'lumotini tiklash qo'lda SQL yozishni talab qiladi; staging'da feature flag'lar prod'dan farq qiladi va buni hech kim bilmaydi.

### 4.10 Qo'lda testlashdan avtomatlashtirishga o'tish mezonlari

Avtomatlashtirish — maqsad emas, vosita. Qarorni to'rt savol bilan qabul qiling: bu test necha marta takrorlanadi? natijasi deterministikmi? muvaffaqiyatsizlikda signal aniqmi? saqlash narxi qanchaga tushadi?

Avtomatlashtirishga munosib: biznes qoidalari va hisob-kitoblar (limit formulalari, chegaralar — bular juda ko'p variantga ega va qo'lda tekshirish qimmat); API shartnomalari va status kodlari; ruxsatlar matritsasi (rol × resurs — tez o'sadi va qo'lda unutiladi); status o'tishlari, ayniqsa taqiqlangan o'tishlar; har release'dagi smoke; tarixda bug chiqqan joylar uchun regression testlar; ma'lumot migratsiyasidan keyingi yaxlitlik tekshiruvlari.

Qo'lda qolishi kerak: vizual estetika, maket bilan moslik va "his-tuyg'u" (UX); bir martalik migratsiya va release repetitsiyasi; exploratory testing — uni avtomatlashtirish mumkin emas, chunki qiymati aynan improvizatsiyada; shakli hali o'zgarib turgan yangi ekranlar (avtomat test ertaga qayta yozilishi kerak bo'ladi); tashqi tizim bilan qo'lda sozlash talab qiladigan kam uchraydigan holatlar; murakkab xato diagnostikasi.

Amaliy ketma-ketlik: yangi funksionallik → qo'lda + exploratory → barqarorlashgandan keyin eng qimmatli scenariylar avtomatlashtiriladi → topilgan har bir jiddiy bug uchun regression test yoziladi (bug-driven automation, eng yuqori ROI'li yondashuv) → qo'lda vaqt yangi funksionallik va exploratory'ga qayta yo'naltiriladi. Agar QA vaqtining 80 foizi takrorlanadigan qo'lda regressiyaga ketayotgan bo'lsa, bu arxitektura muammosi, QA samaradorligi muammosi emas.

### 4.11 QA ishini o'lchash

To'g'ri o'lchov QA'ni yaxshilashga, noto'g'ri o'lchov tizimni o'ynashga undaydi.

**O'lchash mumkin va foydali:** escaped defect — prod'ga chiqib ketgan defektlar soni va ularning severity'si (bu butun jamoaning, nafaqat QA'ning ko'rsatkichi); defekt topish fazasi — qancha defekt talab tahlilida, qancha unit testda, qancha QA'da, qancha prod'da topildi (siljish chapga qarab bo'lishi kerak); bug report sifati — "Cannot Reproduce" va qo'shimcha ma'lumot so'ralgan defektlar ulushi; retest aylanishlari soni (reopen darajasi yuqori bo'lsa, talablar yoki muloqot muammosi bor); regression suite ishonchliligi — flaky test ulushi; talab aniqlashtirish samarasi — QA savollari natijasida o'zgartirilgan qabul kriteriyalari soni.

**O'lchamaslik kerak:** topilgan bug soni bo'yicha bonus yoki reyting. Bu metrika darhol xatti-harakatni buzadi: QA ko'p mayda-chuyda defekt yozadi, bitta katta muammoni o'nta kichik defektga bo'ladi, jiddiy risklarni tahlil qilishga vaqt sarflamaydi (chunki tahlil "bug soni"ni oshirmaydi), developer bilan munosabat raqobatga aylanadi va developer defektni "Duplicate" yoki "Not a bug" deb yopishga harakat qiladi. Shu sababli yozilgan test case soni ham yaxshi metrika emas (ko'p test case ≠ yaxshi qamrov), avtomatlashtirilgan test soni ham (ko'p sayoz test tez-tez buziladi), qamrov foizi ham yolg'iz holda ma'nosiz.

Asosiy printsip: QA'ning qiymati topilgan bug sonida emas, prod'ga chiqmagan bug'larda va jamoaga berilgan aniq risk ma'lumotida. Bu qiymatni o'lchash qiyin, lekin uni noto'g'ri proksilar bilan almashtirish — eng tez yo'l yomon QA madaniyatiga.

### 4.12 Arxitektor nazorat ro'yxati

- [ ] Har bir story'ning qabul kriteriyalari testlanadigan shaklda (aktor, o'lchanadigan shart, xato yo'li, raqamli chegara) yozilgan va QA Definition of Ready'ni tasdiqlagan
- [ ] QA sprintning birinchi kunidan ishtirok etadi; test dizayni kod yozilishidan oldin boshlanadi, oxirgi ikki kunga siqilmaydi
- [ ] Bug report shabloni jamoada yagona va majburiy maydonlar bor: muhit, build/commit, qadamlar, kutilgan va kuzatilgan natija, trace ID, log parchasi
- [ ] Har bir so'rov trace ID qaytaradi va log'larda uni izlash mumkin — QA developer'ga "qayerda qarash kerak"ni ko'rsata oladi
- [ ] Severity QA tomonidan, priority product owner tomonidan belgilanadi; triage muntazam o'tadi va unda texnik risk ovozi bor
- [ ] Status o'tishlari va biznes qoidalari kodda bitta joyda jamlangan (state machine, qaror jadvali) — QA ularni to'liq qamray oladi
- [ ] Muhitlar jadvali hujjatlashtirilgan: egasi, versiyalar mosligi, ma'lumot manbasi; QA test muhitini mustaqil tiklay oladi
- [ ] QA metrikalari escaped defect va defekt topish fazasiga asoslangan; topilgan bug soni bo'yicha hech qanday bonus yoki reyting yo'q

---

## 5. Unit test: asoslar, qoidalar va JUnit 5 (Unit Testing — Foundations, Rules & JUnit 5)

Unit test — test strategiyasining eng arzon va eng tez fikr-mulohaza (feedback) manbasi: u sekundlar ichida ishlaydi, xatoni aniq joyda ko'rsatadi va refaktoringga ruxsat beradi. Ammo noto'g'ri yozilgan unit testlar teskari ta'sir qiladi: ular implementatsiyaga yopishib qoladi, har bir o'zgarishda yuzlab test qizil bo'ladi va jamoa oxirida testlarni o'chirib tashlaydi. Shu sababli arxitektor uchun muhim savol "qancha test bor?" emas, balki "test nimaga bog'langan?" bo'ladi. Quyidagi barcha misollar Java 17+ (Java 21/25 da ham o'zgarishsiz ishlaydi), JUnit 5 (Jupiter), AssertJ va Mockito 5.x uchun amal qiladi.

### 5.1 Unit test nima va nima emas

Eng keng tarqalgan xato — "unit" so'zini "sinf" deb tushunish. Agar har bir sinf uchun bitta test sinfi majburiy bo'lsa, test to'plami kod tuzilishining ko'zguga aylanadi: ikki sinfni bittaga qo'shsangiz, mantiq o'zgarmasa ham, testlar buziladi. To'g'ri yondashuv — unitni *xatti-harakat* (behaviour) deb olish: tashqi dunyo uchun ma'noga ega bo'lgan eng kichik qaror. `PriceCalculator` ichidagi `DiscountPolicy`, `RoundingRule` va `TaxTable` birgalikda bitta unit bo'lishi mumkin; ular public API emas, implementatsiya detali.

Shu nuqtada ikki uslub ajraladi. **Solitary** unit test sinovdan o'tayotgan obyektning barcha hamkorlarini (collaborator) test double bilan almashtiradi — izolyatsiya maksimal, lekin test ichki tuzilishni biladi. **Sociable** unit test esa faqat protsess chegarasidan tashqariga chiqadigan hamkorlarni (DB, HTTP, broker, tizim vaqti) almashtiradi, qolgan domen obyektlarini haqiqiy holda ishlatadi. Amalda arxitektura qoidasi oddiy: **sociable — standart, solitary — istisno**. Mock faqat I/O, nodeterminizm yoki sekinlik chegarasida paydo bo'ladi.

Unit test nima emas: u DB bilan gaplashmaydi, Spring kontekstini ko'tarmaydi, tarmoqqa chiqmaydi, fayl tizimiga tayanmaydi va boshqa testning natijasiga bog'liq bo'lmaydi. Qaysi sinflarni umuman Spring'siz testlash kerakligi 6-bobda batafsil ko'rib chiqiladi.

### 5.2 FIRST printsiplari

**Fast.** Butun unit to'plam bir necha o'n sekundda tugashi kerak, aks holda uni hech kim lokal ishlatmaydi. Amaliy mezon: bitta test < 10 ms. Agar sekin bo'lsa — sababi deyarli har doim I/O yoki kontekst yuklanishi.

**Isolated.** Test o'z ma'lumotini o'zi tayyorlaydi va global holatni (static field, singleton cache, `System` property, `TimeZone` default) o'zgartirmaydi. Izolyatsiya buzilishining klassik belgisi — test yolg'iz ishlaganda yashil, to'plamda qizil.

**Repeatable.** Bir xil kirish → bir xil natija, mashinadan, soatdan va tartibdan qat'i nazar. `Instant.now()`, `Math.random()`, `UUID.randomUUID()`, `Locale.getDefault()` — barchasi repeatability dushmani.

**Self-validating.** Test o'zi "o'tdi/o'tmadi" deb javob beradi; log o'qish yoki konsolni ko'z bilan tekshirish talab qilinmaydi. `System.out.println` bilan "tekshirish" — test emas.

**Timely.** Test kodga yaqin vaqtda yoziladi (ideal holda — oldin). Keyinga qoldirilgan test API dizaynini yaxshilash imkonini yo'qotadi va "endi testlash qiyin" degan xulosaga olib keladi — bu dizayn muammosining signali.

### 5.3 Arrange-Act-Assert va test nomlash

Har bir test uchta ko'rinadigan bosqichdan iborat bo'lishi kerak: **Arrange** (holatni tayyorlash), **Act** (bitta chaqiruv), **Assert** (natijani tasdiqlash). BDD atamalarida bu Given-When-Then. Qoida: **bitta testda bitta xatti-harakat va bitta Act**. Agar testda ikkinchi `service.doSomething()` paydo bo'lsa, demak ikkita test kerak.

```java
class PriceCalculatorTest {
    private final PriceCalculator calculator = new PriceCalculator();

    @Test
    @DisplayName("Haqiqiy kupon yakuniy narxni 10% kamaytiradi")
    void appliesPercentageDiscountWhenCouponIsValid() {
        // Arrange
        Order order = new Order(List.of(new Item("book", money("100.00"), 2)));
        Coupon coupon = Coupon.percentage("SUMMER10", 10);

        // Act
        Money total = calculator.total(order, coupon);

        // Assert
        assertThat(total).isEqualTo(money("180.00"));
    }
}
```

Nomlash konvensiyalari, afzalliklari bilan:

1. `method_stateUnderTest_expectedBehaviour` — `pay_whenCardExpired_throwsPaymentDeclined`. Tuzilgan, lekin metod nomiga bog'langan: refaktoringdan keyin nom yolg'on gapiradi.
2. `should...When...` — `shouldThrowWhenCardExpired`. O'qiladi, ammo "should" har bir nomda takrorlanib shovqin hosil qiladi.
3. `given...When...Then...` — `givenExpiredCard_whenPaying_thenThrows`. BDD jamoalari uchun qulay, lekin nomlar uzayib ketadi.
4. **Xatti-harakat gapi** — `rejectsPaymentWhenCardExpired`, ustiga `@DisplayName` bilan to'liq o'zbekcha/inglizcha tavsif.

**Tavsiya: 4-variant.** Metod nomi emas, qarorning natijasi nomlanadi; `@DisplayName` esa hisobotda to'liq gap beradi. `@DisplayNameGeneration(DisplayNameGenerator.ReplaceUnderscores.class)` bilan pastki chiziqli nomlarni avtomatik gapga aylantirish ham mumkin.

### 5.4 JUnit 5 asoslari: lifecycle va tuzilma

`@Test` — `void`, parametrsiz (yoki in'ektsiya qilinadigan parametrlar bilan), `public` bo'lishi shart emas. Lifecycle: `@BeforeEach`/`@AfterEach` har bir testdan oldin/keyin, `@BeforeAll`/`@AfterAll` esa sinf darajasida bir marta ishlaydi va standart holatda `static` bo'lishi kerak. `@Nested` ichki sinflar bilan testlarni kontekst bo'yicha guruhlash — eng kuchli o'qiluvchanlik vositasi: tashqi `@BeforeEach` ichki sinflarda ham ishlaydi.

```java
@DisplayName("CartService")
class CartServiceTest {
    private Cart cart;

    @BeforeEach
    void setUp() {
        cart = new Cart("user-1");
    }

    @Nested
    @DisplayName("savat bo'sh bo'lganda")
    class WhenEmpty {
        @Test
        void totalIsZero() {
            assertThat(cart.total()).isEqualTo(Money.ZERO);
        }

        @Test
        void checkoutIsRejected() {
            assertThatThrownBy(cart::checkout)
                    .isInstanceOf(EmptyCartException.class);
        }
    }
}
```

**Test instance lifecycle.** Standart holat — `PER_METHOD`: har bir test uchun test sinfining yangi nusxasi yaratiladi, shu sababli maydonlar testlar orasida oqib ketmaydi. `@TestInstance(TestInstance.Lifecycle.PER_CLASS)` bitta nusxani barcha testlarga beradi — `@BeforeAll` ni non-static qilish va qimmat setup'ni bir marta bajarish imkonini beradi, ammo holat izolyatsiyasini o'zingiz ta'minlashingiz kerak. Arxitektor qoidasi: `PER_CLASS` ni faqat o'zgarmas (immutable) setup uchun ruxsat ber.

**`@Disabled` xavfi.** O'chirilgan test — yashil CI'da yashiringan qizil test. U eskiradi, kompilyatsiya qilinadi, lekin hech narsani himoya qilmaydi. Qoida: `@Disabled` faqat sababi va issue havolasi bilan (`@Disabled("PAY-412: gateway sandbox o'chirilgan")`) va muddat bilan; sababsiz `@Disabled` CI'da fail bo'lishi kerak. Platforma/shart asosida o'tkazib yuborish uchun `@EnabledOnOs`, `@EnabledIfSystemProperty`, `@EnabledIfEnvironmentVariable` yoki `Assumptions.assumeTrue(...)` ishlatiladi — bu `@Disabled` dan ancha halolroq.

### 5.5 Parametrlashtirilgan testlar

Parametrlashtirish kerak bo'lgan vaziyat aniq: **bir xil xatti-harakat, faqat ma'lumot farq qiladi**. Agar har bir holat uchun turli assertion mantiqi kerak bo'lsa — bu alohida testlar, parametr emas. `junit-jupiter-params` artefakti talab qiladi.

```java
class IbanValidatorTest {
    private final IbanValidator validator = new IbanValidator();

    @ParameterizedTest(name = "[{index}] {0} haqiqiy")
    @ValueSource(strings = {"UZ8300010000000000000001", "DE89370400440532013000"})
    void acceptsValidIbans(String iban) {
        assertThat(validator.isValid(iban)).isTrue();
    }

    @ParameterizedTest
    @CsvSource({"UZ8, TOO_SHORT", "XX89370400, UNKNOWN_COUNTRY"})
    void rejectsWithReason(String iban, IbanError expected) {
        assertThat(validator.validate(iban).error()).isEqualTo(expected);
    }

    @ParameterizedTest
    @NullAndEmptySource
    @ValueSource(strings = {"   ", "\t"})
    void rejectsBlankInput(String iban) {
        assertThat(validator.isValid(iban)).isFalse();
    }
}
```

Manbalar xaritasi: `@ValueSource` — bitta primitiv/String parametr; `@CsvSource` va `@CsvFileSource` — bir necha ustun, `nullValues`/`delimiter` sozlamalari bilan; `@MethodSource("name")` — murakkab obyektlar uchun `static Stream<Arguments>` qaytaruvchi metod; `@EnumSource(value = OrderStatus.class, names = {"PENDING", "PAID"})` yoki `mode = EXCLUDE` — enum bo'ylab to'liq qamrov (yangi enum qiymati qo'shilganda test avtomatik o'sadi); `@ArgumentsSource(ExpiredCardsProvider.class)` — qayta ishlatiladigan `ArgumentsProvider` implementatsiyasi. `@NullSource`, `@EmptySource`, `@NullAndEmptySource` — null-safety uchun eng arzon qamrov.

### 5.6 AssertJ bilan tasdiqlash

JUnit'ning `assertEquals` uchta muammoga ega: argument tartibi (expected/actual) adashtiradi, kolleksiyalar va obyekt graflari uchun imkoniyat bermaydi, xato xabari esa "expected: 2 but was: 3" dan nariga o'tmaydi. AssertJ fluent API bilan IDE avtomatik to'ldirishi orqali kashf qilinadigan, aniq diagnostikali assertion beradi.

```java
// Yomon: tarqoq, xato xabari ma'nosiz
@Test
void badAssertions() {
    List<Order> orders = service.findPending();
    assertEquals(2, orders.size());
    assertEquals("A-1", orders.get(0).number());
    assertTrue(orders.get(0).total().compareTo(BigDecimal.TEN) > 0);
}

// Yaxshi: bitta oqim, to'liq diagnostika
@Test
void goodAssertions() {
    assertThat(service.findPending())
            .as("kutilayotgan buyurtmalar")
            .hasSize(2)
            .extracting(Order::number, Order::status)
            .containsExactly(tuple("A-1", PENDING), tuple("A-2", PENDING));

    assertThat(service.findPending()).first().satisfies(order -> {
        assertThat(order.total()).isGreaterThan(money("10.00"));
        assertThat(order.customer().email()).endsWith("@example.com");
    });
}
```

Kalit vositalar: `extracting` — kolleksiyadan maydonlarni ajratib, `containsExactly` (tartib muhim), `containsExactlyInAnyOrder` (tartib muhim emas) yoki `allSatisfy` bilan tekshirish; `satisfies` — bitta element uchun bir necha shartni guruhlash; `assertThatThrownBy` — istisnolar; `usingRecursiveComparison` — `equals` yozmasdan butun obyekt grafini solishtirish; `SoftAssertions` — barcha xatolarni bir yugurishda ko'rish.

```java
@Test
void mapsDtoIgnoringTechnicalFields() {
    OrderDto dto = mapper.toDto(order);

    assertThat(dto)
            .usingRecursiveComparison()
            .ignoringFields("createdAt", "version")
            .isEqualTo(expectedDto);
}
```

Domen tilida o'qiladigan testlar uchun custom assertion yozing — bu takrorlanuvchi tekshiruvlarni bir joyga yig'adi:

```java
public class OrderAssert extends AbstractAssert<OrderAssert, Order> {

    private OrderAssert(Order actual) {
        super(actual, OrderAssert.class);
    }

    public static OrderAssert assertThat(Order actual) {
        return new OrderAssert(actual);
    }

    public OrderAssert isPaid() {
        isNotNull();
        if (actual.status() != OrderStatus.PAID) {
            failWithMessage("<%s> uchun PAID kutilgan, aslida <%s>",
                    actual.number(), actual.status());
        }
        return this;
    }
}
```

### 5.7 Mockito bilan test double'lar

`@ExtendWith(MockitoExtension.class)` (`mockito-junit-jupiter` artefakti) `@Mock`, `@Spy`, `@Captor` va `@InjectMocks` maydonlarini to'ldiradi hamda har bir testdan keyin tekshiruvni ishga tushiradi. Mockito 5.x standart holatda `inline` mock maker ishlatadi — `final` sinf va metodlarni ham mock qiladi, `mockito-inline` alohida qo'shilishi shart emas.

```java
@ExtendWith(MockitoExtension.class)
class OrderServiceTest {

    @Mock private PaymentGateway gateway;
    @Mock private OrderRepository repository;
    @InjectMocks private OrderService service;
    @Captor private ArgumentCaptor<Payment> paymentCaptor;

    @Test
    void chargesGatewayWithOrderTotal() {
        Order order = pending("A-1", money("250.00"));
        when(repository.findByNumber("A-1")).thenReturn(Optional.of(order));
        when(gateway.charge(any(Payment.class)))
                .thenReturn(PaymentResult.approved("tx-9"));

        service.pay("A-1");

        verify(gateway).charge(paymentCaptor.capture());
        assertThat(paymentCaptor.getValue().amount()).isEqualTo(money("250.00"));
        verifyNoMoreInteractions(gateway);
    }
}
```

`thenThrow(new GatewayTimeoutException())` bilan xato yo'llarini, `ArgumentCaptor` bilan uzatilgan argumentni, `ArgumentMatchers` (`any()`, `eq()`, `argThat(p -> ...)`) bilan moslashuvchan moslikni oling. Muhim qoida: bitta chaqiruvda matcher ishlatsangiz, qolgan barcha argumentlar ham matcher bo'lishi kerak (`eq("A-1")`).

**Strict stubbing.** `MockitoExtension` standart holatda `Strictness.STRICT_STUBS` rejimida ishlaydi: ishlatilmagan stub `UnnecessaryStubbingException`, mos kelmagan argument bilan chaqiruv esa `PotentialStubbingProblem` beradi. Bu o'lik stub'larni va noto'g'ri tushunchalarni darhol oshkor qiladi — uni `@MockitoSettings(strictness = Strictness.LENIENT)` bilan o'chirish kodni emas, muammoni yashirish demakdir.

**Nimani mock qilmaslik kerak:** value object va DTO (`Money`, `Address`, `OrderDto`) — ularni shunchaki yarating; JDK sinflari (`List`, `Map`, `Optional`, `String`, `LocalDate`) — haqiqiy nusxa doim arzonroq; sinovdan o'tayotgan sinfning o'zi (`@Spy` + partial mock — dizayn muammosining belgisi); sof funksiyalar va mapper'lar. `@Spy` faqat legacy kodni bosqichma-bosqich qamrab olishda vaqtinchalik vosita bo'lishi kerak.

### 5.8 Over-mocking muammosi va fake'lar

Haddan ziyod mock qilingan test o'zini testlaydi: `when(a.b()).thenReturn(c); when(c.d()).thenReturn(e);` zanjiri kodning *qanday yozilganini* yozib oladi, *nima qilishini* emas. Belgilari: testda 5+ `when`, mock mock qaytaradi, assertion'lar faqat `verify` dan iborat, nomi o'zgarmagan refaktoringda o'nlab test buziladi. Bunday test regressiyani tutmaydi, lekin refaktoringni to'xtatadi — eng yomon kombinatsiya.

Davosi — **fake** (haqiqiy, lekin soddalashtirilgan implementatsiya) va **stub** (oldindan belgilangan javob). Repository, cache, clock va event publisher uchun in-memory fake yozish bir marta qilinadigan 20 qatorlik ish, lekin o'nlab testni mock zanjirlaridan xalos qiladi:

```java
public class InMemoryOrderRepository implements OrderRepository {
    private final Map<String, Order> store = new ConcurrentHashMap<>();

    @Override
    public Optional<Order> findByNumber(String number) {
        return Optional.ofNullable(store.get(number));
    }

    @Override
    public Order save(Order order) {
        store.put(order.number(), order);
        return order;
    }
}

@Test
void paidOrderIsPersistedWithPaidStatus() {
    OrderRepository repository = new InMemoryOrderRepository();
    OrderService service = new OrderService(repository, new ApprovingGateway());
    repository.save(pending("A-1", money("250.00")));

    service.pay("A-1");

    assertThat(repository.findByNumber("A-1")).get().extracting(Order::status).isEqualTo(PAID);
}
```

Fake natijani (state) tekshiradi, mock esa o'zaro ta'sirni (interaction). Qoida: **holat tekshiruvi — birinchi tanlov; interaction tekshiruvi faqat natija ko'rinmaydigan joyda** (email yuborildimi, event chiqdimi, to'lov chaqirildimi).

### 5.9 Istisno, chegara holatlari va null-safety

Istisnoni `try/catch` + `fail()` bilan emas, `assertThatThrownBy` bilan tekshiring: tur, xabar va kontekst maydonlarining barchasini. Chegara holatlari esa buglarning asosiy uyasi: 0, 1, -1, `MIN_VALUE`/`MAX_VALUE`, bo'sh kolleksiya, bitta elementli kolleksiya, aniq teng qiymat (`isBefore` vs `isAfter` chegarasi), yakshanba/oy oxiri, scale va rounding (`BigDecimal.ZERO` va `0.00` `equals` bo'yicha teng emas — shu sababli `isEqualByComparingTo` yoki `Money` value object ishlating).

```java
@Test
void rejectsNegativeAmount() {
    assertThatThrownBy(() -> Money.of(new BigDecimal("-1.00"), "UZS"))
            .isInstanceOf(InvalidAmountException.class)
            .hasMessageContaining("manfiy")
            .hasFieldOrPropertyWithValue("currency", "UZS")
            .hasNoCause();

    assertThatNullPointerException()
            .isThrownBy(() -> Money.of(null, "UZS"));

    assertThatCode(() -> Money.of(BigDecimal.ZERO, "UZS"))
            .doesNotThrowAnyException();
}
```

Null-safety uchun eng samarali strategiya — null'ni API chegarasida taqiqlash (`Objects.requireNonNull`, `Optional` qaytarish, JSpecify/`@NonNull` annotatsiyalari) va shu shartnomani `@NullSource`/`@NullAndEmptySource` bilan testlash. Null'ni domen ichiga kiritmaslik — testlarni ikki barobar kamaytiradi.

### 5.10 Vaqt, tasodif va UUID'ni testlash

`Instant.now()` ni to'g'ridan-to'g'ri chaqirgan kodni determinizm bilan testlash mumkin emas. Yechim — vaqtni dependency qilish: `java.time.Clock` ni Spring bean sifatida e'lon qilib (`@Bean Clock clock() { return Clock.systemUTC(); }`) konstruktor orqali in'ektsiya qiling, testda esa `Clock.fixed(...)` yoki `Clock.offset(...)` bering.

```java
// Yomon: test tizim soatiga bog'langan, chegarani tekshirib bo'lmaydi
public boolean isExpired(Subscription s) {
    return s.endsAt().isBefore(Instant.now());
}
```

```java
public class SubscriptionService {
    private final Clock clock;

    public SubscriptionService(Clock clock) {
        this.clock = clock;
    }

    public boolean isExpired(Subscription s) {
        return s.endsAt().isBefore(clock.instant());
    }
}

@Test
void isNotExpiredExactlyAtBoundary() {
    Instant now = Instant.parse("2026-01-01T00:00:00Z");
    var service = new SubscriptionService(Clock.fixed(now, ZoneOffset.UTC));

    assertThat(service.isExpired(new Subscription(now))).isFalse();
    assertThat(service.isExpired(new Subscription(now.minusMillis(1)))).isTrue();
}
```

Xuddi shu naqsh tasodif va identifikatorlar uchun: `UUID.randomUUID()` o'rniga `Supplier<UUID> idGenerator`, `Random` o'rniga `IntSupplier` yoki urug' (seed) bilan `new Random(42)`. Testda `() -> UUID.fromString("00000000-0000-0000-0000-000000000001")` beriladi va natija to'liq oldindan aytiladi. **`Thread.sleep` ishlatmang** — u testni sekin va flaky qiladi; asinxron natija uchun Awaitility yoki boshqariladigan executor (`new SyncTaskExecutor()`) ishlating. Flaky testlar bilan kurash 16-bobda.

### 5.11 Property-based testing: jqwik

Misol asosidagi test siz o'ylagan holatlarni tekshiradi; property-based test esa *invariant* ni e'lon qiladi va yuzlab tasodifiy kirishni o'zi generatsiya qiladi, xato topilganda esa uni minimal misolga qisqartiradi (shrinking). jqwik JUnit 5 platformasining mustaqil test engine'i sifatida ishlaydi va mavjud Jupiter testlari bilan birga yashaydi.

```java
class MoneyProperties {

    @Property
    void additionIsCommutative(@ForAll("amounts") BigDecimal a,
                               @ForAll("amounts") BigDecimal b) {
        assertThat(Money.of(a, "UZS").plus(Money.of(b, "UZS")))
                .isEqualTo(Money.of(b, "UZS").plus(Money.of(a, "UZS")));
    }

    @Property
    void stringRoundTripKeepsValue(@ForAll("amounts") BigDecimal a) {
        Money money = Money.of(a, "UZS");
        assertThat(Money.parse(money.toString())).isEqualTo(money);
    }

    @Provide
    Arbitrary<BigDecimal> amounts() {
        return Arbitraries.bigDecimals()
                .between(BigDecimal.ZERO, new BigDecimal("1000000"))
                .ofScale(2);
    }
}
```

Qachon foydali: parser va serializer (round-trip xossasi), pul va soliq hisob-kitoblari (assotsiativlik, taqsimlanish, yig'indi saqlanishi), saralash va ketma-ketlik algoritmlari, domen invariantlari (buyurtma holati hech qachon `PAID` dan `PENDING` ga qaytmaydi), idempotentlik. Qachon foydasiz: CRUD oqimlari, oddiy delegatsiya, I/O bilan ishlovchi kod. Property-based test misol asosidagi testni almashtirmaydi — u o'zingiz o'ylamagan chegara holatlarini topish uchun qo'shimcha qatlam.

### 5.12 Mutation testing bilan sifatni o'lchash (PIT)

Line coverage testlarning *bajarilganini* ko'rsatadi, *tekshirganini* emas: assertion'siz test ham 100% qamrov beradi. Mutation testing bu bo'shliqni yopadi — PIT (pitest) bytecode'ga kichik "mutant"lar kiritadi (`>` ni `>=` ga almashtirish, return qiymatini o'zgartirish, shartni inkor qilish, metod chaqiruvini olib tashlash) va har bir mutant uchun testlarni ishga tushiradi. Agar mutant bilan ham testlar yashil bo'lsa — mutant *tirik qoldi*, ya'ni bu mantiqni hech bir assertion himoya qilmayapti. Asosiy ko'rsatkich — **mutation score** (o'ldirilgan mutantlar ulushi), ko'proq ishonchli variant esa test strength.

Amalda PIT'ni JUnit 5 bilan ishlatish uchun `pitest-maven` (yoki Gradle plugin) yoniga `pitest-junit5-plugin` kerak, va uni butun kod bazasiga emas, domen hamda hisob-kitob paketlariga yo'naltirish to'g'ri bo'ladi — mutation testing CPU talab qiladi. Arxitektor uchun qiymati: mutation score sun'iy coverage KPI'larini oshkor qiladi va "qaysi testlar haqiqatan ishlaydi" degan savolga javob beradi. Konfiguratsiya, incremental analiz, CI'ga ulash va coverage siyosati 14-bobda batafsil ko'rib chiqiladi.

### 5.13 Unit test anti-patternlari

**Assertion yo'q test.** Faqat chaqiruv bor, natija tekshirilmaydi — u faqat `NullPointerException` ni tutadi. Coverage hisobotini bo'yaydi, regressiyani tutmaydi.

**Logikasi bor test.** `if`, `for`, `switch`, `try/catch` yoki hisob-kitob testning o'zida bo'lsa — testni ham testlash kerak bo'ladi. Buning o'rniga `@ParameterizedTest` va to'g'ridan-to'g'ri yozilgan kutilgan qiymatlar:

```java
// Yomon: assertion yo'q + testning o'zida mantiq
@Test
void processesOrders() {
    for (Order order : randomOrders()) {
        if (order.total().isPositive()) {
            service.process(order);
        }
    }
}

// Yaxshi: har bir holat alohida va determinnistik
@ParameterizedTest
@CsvSource({"250.00, PROCESSED", "0.00, REJECTED"})
void processesOrderByTotal(BigDecimal total, OrderStatus expected) {
    Order order = pending("A-1", Money.of(total, "UZS"));

    assertThat(service.process(order).status()).isEqualTo(expected);
}
```

**Tasodifiy ma'lumotga tayanish.** `Faker` yoki `random()` bilan generatsiya qilingan kirish testni nodeterministik qiladi: bugun yashil, ertaga qizil, ayblanuvchi topilmaydi. Test ma'lumotini aniq va o'qiladigan qilib bering (test data builder'lar 10-bobda).

**Testlar orasidagi tartib bog'liqligi.** `static` maydon yoki umumiy DB holati orqali bir test ikkinchisini "tayyorlaydi". JUnit test tartibini kafolatlamaydi; `@TestMethodOrder` bilan tartibni "tuzatish" — muammoni mustahkamlash. Har bir test o'z holatini o'zi quradi.

**Private metodni reflection bilan testlash.** Bu shartnoma emas, implementatsiya detalini qulflash. Agar private metod mustaqil testga arziydigan darajada murakkab bo'lsa — u alohida sinfga chiqarilishi kerak degan signal. `@VisibleForTesting` bilan ko'rinishni ochish ham xuddi shu muammoning yumshoq shakli.

**Haddan ziyod setup.** 40 qatorlik `@BeforeEach` barcha testlarga xizmat qiladi, lekin hech biri uchun aniq emas — testni o'qib, u nimani tekshirayotganini tushunib bo'lmaydi. Setup'ni test uchun ahamiyatli qismini testning o'zida qoldiring, qolganini builder'lar ortiga yashiring.

**Boshqalar:** `verify` dan iborat testlar (interaction'ga ortiqcha bog'lanish), `assertTrue(result != null)` kabi ma'nosiz assertion'lar, bir testda 10 ta mantiqiy tekshiruv, va `@Disabled` "vaqtincha" qoldirilgan testlar.

### 5.14 Arxitektor nazorat ro'yxati

- [ ] Unit test "unit"i sinf emas, xatti-harakat deb belgilangan; sociable uslub standart, solitary — faqat I/O chegarasida
- [ ] Butun unit to'plam lokal mashinada 60 sekunddan kam ishlaydi va hech bir test DB, tarmoq, fayl tizimi yoki Spring kontekstiga tegmaydi
- [ ] Barcha assertion'lar AssertJ orqali; takrorlanuvchi domen tekshiruvlari uchun custom assertion yoki `usingRecursiveComparison` ishlatiladi
- [ ] Mockito `STRICT_STUBS` rejimida; `LENIENT` va `@Spy` ishlatilishi istisno sifatida asoslanadi; value object, DTO va JDK sinflari mock qilinmaydi
- [ ] Repository, cache va event publisher uchun in-memory fake'lar mavjud va mock zanjirlari o'rniga ishlatiladi
- [ ] Vaqt `Clock` bean orqali, tasodif va UUID `Supplier` ortida in'ektsiya qilinadi; kod bazasida `Thread.sleep` va `Instant.now()` to'g'ridan-to'g'ri chaqiruvi yo'q
- [ ] `@Disabled` testlar sabab va issue havolasi bilan; ularning soni CI'da kuzatiladi va nolga intiladi
- [ ] Domen va hisob-kitob paketlari uchun mutation score o'lchanadi (PIT) va coverage foizi yagona sifat mezoni sifatida ishlatilmaydi

---

## 6. Unit test Spring loyihasida: kontekstsiz testlash (Unit Testing in a Spring Project)

Spring loyihasida yozilgan kodning katta qismi — biznes qoidalari, kalkulyatorlar, validatorlar, mapper'lar va domain modeli — Spring'ga umuman bog'liq emas va ularni tekshirish uchun ApplicationContext ko'tarish shart emas. Shunga qaramay ko'p jamoalarda har bir test `@SpringBootTest` bilan boshlanadi: natijada sekin, mo'rt va xato manbasini yashiradigan test to'plami paydo bo'ladi. Bu bobda qaysi kodni "konteynerdan tashqarida" — oddiy Java obyekti sifatida — testlash kerakligini, buning uchun kodni qanday yozishni va Spring'ning eng yengil test vositasi bo'lgan `ApplicationContextRunner` qachon o'rinli bo'lishini ko'rib chiqamiz. Oxirida kontekst haqiqatan zarur bo'ladigan chegarani aniq belgilaymiz.

### 6.1 Nega @SpringBootTest unit test uchun noto'g'ri tanlov

Birinchi sabab — vaqt. Toza unit test JVM ichida obyekt yaratib, metod chaqirib, natijani tekshiradi: bu millisekundlar tartibidagi ish. `@SpringBootTest` esa butun komponent skanerlashni, auto-configuration zanjirini, DataSource va EntityManagerFactory yaratishni, ba'zan embedded serverni ishga tushirishni talab qiladi — bu sekundlar tartibidagi ish. Quyidagi raqamlar o'rta kattalikdagi Spring Boot 3.x/4.x loyihasi uchun odatiy tartibni ko'rsatadi (aniq qiymat mashina va bean sonidan bog'liq):

| Test uslubi | Kontekst ko'tarilishi | Bitta test metodi | Nimani kafolatlaydi |
|---|---|---|---|
| Toza JUnit 5 (`new`) | yo'q | ~0.1–2 ms | logika to'g'riligi |
| `@ExtendWith(MockitoExtension.class)` | yo'q | ~1–5 ms | o'zaro ta'sir (interaction) |
| `ApplicationContextRunner` (2–5 bean) | ~30–200 ms | ~30–200 ms | wiring, conditional, binding |
| `@WebMvcTest` / `@DataJpaTest` (slice) | ~1–3 s | ~10–50 ms (kesh bilan) | qatlam kontrakti |
| `@SpringBootTest` (to'liq) | ~3–15 s | ~20–100 ms (kesh bilan) | tizim yig'ilishi |

Spring TestContext Framework kontekstni keshlaydi (`spring.test.context.cache.maxSize`, standart qiymati 32), shuning uchun ikkinchi testdan keyin narx kamayadi. Lekin kesh kaliti konfiguratsiyaga bog'liq: har bir yangi `@TestPropertySource`, `@ActiveProfiles` yoki `@MockitoBean` kombinatsiyasi yangi kontekst yaratadi, `@DirtiesContext` esa keshni buzadi. 300 ta unit testni `@SpringBootTest` bilan yozgan loyihada CI'da 20 daqiqalik to'plamlar normal holga aylanadi.

Ikkinchi, muhimroq sabab — xato manbasining noaniqligi. To'liq kontekst ko'tarilganda `OrderServiceTest` qulashi mumkin, chunki boshqa jamoa `KafkaTemplate` bean'ini o'zgartirgan, Flyway migratsiyasi buzilgan yoki yangi `@Value` xossasi `application.yml`da yo'q. Test nomi "buyurtma chegirmasi" deydi, xato esa `BeanCreationException` bo'ladi. Unit test bitta sinfning bitta qoidasini tekshirsa, qulaganda sabab bir xil aniq bo'ladi.

Uchinchi sabab — feedback halqasi. TDD yoki refactoring jarayonida test 50 ms ichida javob bersa, developer kodni fikr tezligida o'zgartiradi; 15 sekund kutish kerak bo'lsa, testlar IDE'da emas, faqat CI'da ishlay boshlaydi.

### 6.2 Constructor injection — testlanadigan dizayn asosi

Unit test imkoniyati arxitektura qarori natijasidir. Constructor injection sinfni `new` bilan yaratishga ruxsat beradi: bu Spring'ning o'zi ham rasman tavsiya qiladigan uslub. Shuningdek vaqtni `Clock` sifatida kiritish testni determinatsiyalashtiradi.

```java
@Service
public class OrderService {

    private final OrderRepository orders;
    private final DiscountPolicy discountPolicy;
    private final Clock clock;

    public OrderService(OrderRepository orders,
                        DiscountPolicy discountPolicy,
                        Clock clock) {
        this.orders = orders;
        this.discountPolicy = discountPolicy;
        this.clock = clock;
    }

    public Order place(CustomerId customerId, List<OrderLine> lines) {
        Money total = lines.stream()
                .map(OrderLine::amount)
                .reduce(Money.ZERO, Money::plus);
        Money discount = discountPolicy.discountFor(customerId, total);
        Order order = Order.create(customerId, lines, discount, clock.instant());
        return orders.save(order);
    }
}
```

Field injection (`@Autowired private OrderRepository orders;`) bu imkoniyatni yo'q qiladi: maydonni `final` qilib bo'lmaydi, obyektni to'liq holatda `new` bilan yaratib bo'lmaydi, test esa `ReflectionTestUtils.setField(...)` yoki `@InjectMocks`ning reflection magiyasiga tayanadi. Bu ikki muammoni keltiradi: maydon nomini o'zgartirsangiz test kompilyatsiya xatosi bermaydi, shunchaki `null` bilan qulaydi; va konstruktor "bu sinfga 7 ta dependency kirgan" degan dizayn signalini yashiradi. Shu sababli `@InjectMocks`ni ham imkon qadar ishlatmaslik, `@Mock` bilan olingan obyektlarni konstruktorga qo'lda berish tavsiya etiladi — `new OrderServiceImpl(mockRepo, fixedClock)` shaklidagi chaqiruv kompilyator nazoratida bo'ladi.

### 6.3 Qaysi sinflar Spring kontekstisiz testlanadi

Quyidagi jadval amaliy qaror qabul qilish uchun qo'llanma bo'ladi.

| Kod turi | Test usuli | Spring kerakmi |
|---|---|---|
| Domain entity, value object (`Money`, `Iban`) | toza JUnit 5 + AssertJ | yo'q |
| Biznes qoidasi / invariant (`Order.confirm()`) | toza JUnit 5, `assertThatThrownBy` | yo'q |
| Bean Validation annotatsiyalari bo'lgan DTO | `Validation.buildDefaultValidatorFactory()` | yo'q |
| Custom `ConstraintValidator` (Spring bean'siz) | to'g'ridan-to'g'ri `isValid(...)` | yo'q |
| MapStruct mapper | `Mappers.getMapper(...)` | yo'q |
| Qo'lda yozilgan DTO konvertor | `usingRecursiveComparison()` | yo'q |
| Kalkulyator, narx/soliq hisoblagich | `@ParameterizedTest` | yo'q |
| Policy / Strategy implementatsiyasi | toza JUnit 5 | yo'q |
| Service qatlami (orkestratsiya) | Mockito 5.x + `MockitoExtension` | yo'q |
| `@ConfigurationProperties`, `@Conditional` | `ApplicationContextRunner` | minimal |
| `@Transactional`, `@Cacheable`, `@Async`, `@Retryable` | integratsion / slice test | ha |
| Controller mapping, JSON serialization, SQL | slice test (7-bob) | ha |

Masalan value object uchun test hech qanday infratuzilmani talab qilmaydi:

```java
class MoneyTest {

    @Test
    void qoshish_valyutani_saqlaydi() {
        Money a = Money.of("12.50", "UZS");
        Money b = Money.of("7.50", "UZS");

        assertThat(a.plus(b)).isEqualTo(Money.of("20.00", "UZS"));
    }

    @Test
    void turli_valyutalarni_qoshish_rad_etiladi() {
        Money uzs = Money.of("10.00", "UZS");
        Money usd = Money.of("10.00", "USD");

        assertThatThrownBy(() -> uzs.plus(usd))
                .isInstanceOf(CurrencyMismatchException.class)
                .hasMessageContaining("USD");
    }
}
```

SpEL ifodalari, `Environment`ga murojaat yoki `ApplicationEventPublisher` chaqiruvlari aralashgan sinflar bu ro'yxatdan chiqib ketadi — shuning uchun sof logikani alohida sinfga ajratish testlanuvchanlikni oshiradigan eng arzon refactoring.

### 6.4 Service qatlamini mock repository bilan testlash

Service qatlami odatda orkestratsiya qiladi: repository'dan ma'lumot oladi, policy'ni chaqiradi, natijani saqlaydi. Bularni Mockito 5.x bilan Spring'siz tekshirish mumkin. `MockitoExtension` standart holda `Strictness.STRICT_STUBS` rejimida ishlaydi — ishlatilmagan stub test qulashiga olib keladi, bu ortiqcha sozlamalarni erta ushlaydi.

```java
@ExtendWith(MockitoExtension.class)
class OrderServiceTest {

    @Mock OrderRepository orders;
    @Mock DiscountPolicy discountPolicy;

    private final Clock clock =
            Clock.fixed(Instant.parse("2026-03-01T10:00:00Z"), ZoneOffset.UTC);

    @Test
    void vip_mijozga_chegirma_qollanadi() {
        OrderService service = new OrderService(orders, discountPolicy, clock);
        CustomerId customer = new CustomerId("c-1");
        List<OrderLine> lines = List.of(line("SKU-1", 2, "100.00"));
        when(discountPolicy.discountFor(customer, Money.of("100.00", "UZS")))
                .thenReturn(Money.of("15.00", "UZS"));
        when(orders.save(any(Order.class))).thenAnswer(inv -> inv.getArgument(0));

        Order order = service.place(customer, lines);

        assertThat(order.total()).isEqualTo(Money.of("85.00", "UZS"));
        assertThat(order.createdAt()).isEqualTo(Instant.parse("2026-03-01T10:00:00Z"));
        verify(orders).save(argThat(o -> o.discount().equals(Money.of("15.00", "UZS"))));
    }
}
```

Diqqat qiling: `Clock.fixed(...)` tufayli `createdAt` aniq tekshiriladi — `LocalDateTime.now()`ni to'g'ridan-to'g'ri ishlatgan kodda bunday assert yozish mumkin emas. Agar repository interfeysi domain qatlamida (port sifatida) e'lon qilingan bo'lsa, mock'lash ham tabiiy ko'rinadi; Spring Data'ning `JpaRepository`sini to'g'ridan-to'g'ri mock'lash esa 20 dan ortiq metodli interfeysni soxtalashtirishga olib keladi.

### 6.5 Mapper va DTO konvertorlarni testlash

MapStruct mapper'i kompilyatsiya vaqtida oddiy Java sinfiga aylanadi, shuning uchun uni Spring'siz olish mumkin. `componentModel = "spring"` bo'lsa ham `Mappers.getMapper(...)` ishlaydi, agar mapper boshqa mapper'larni `uses` orqali olmasa; aks holda generatsiya qilingan `XxxMapperImpl`ni `new` bilan yaratib, bog'liq mapper'ni setter yoki konstruktor orqali bering.

```java
class CustomerMapperTest {

    private final CustomerMapper mapper = Mappers.getMapper(CustomerMapper.class);

    @Test
    void entity_dto_ga_toliq_kochadi() {
        CustomerEntity entity =
                new CustomerEntity(7L, "Olim", "Qoraev", "olim@example.uz", true);

        CustomerDto dto = mapper.toDto(entity);

        assertThat(dto)
                .usingRecursiveComparison()
                .isEqualTo(new CustomerDto(7L, "Olim Qoraev", "olim@example.uz", true));
    }

    @Test
    void nomavjud_maydonlar_null_qoladi() {
        CustomerEntity entity = new CustomerEntity(7L, "Olim", null, null, false);

        assertThat(mapper.toDto(entity).email()).isNull();
    }
}
```

Qo'lda yozilgan konvertorlar uchun AssertJ'ning `usingRecursiveComparison()` usuli eng foydali: yangi maydon qo'shilib, konvertorda unutilsa, test darhol qulaydi. Maydonlarni bitta-bitta tekshiradigan test esa bunday "unutilgan maydon" xatosini aniqlamaydi. Katta obyektlarda `ignoringFields("id", "audit.createdAt")` va `withEqualsForType(...)` bilan toleranslikni boshqarish mumkin.

### 6.6 Validatsiyani Spring kontekstisiz testlash

Jakarta Bean Validation 3.x implementatsiyasi (Hibernate Validator) Spring'dan mustaqil ishlaydi. `Validator`ni qo'lda yaratish kontekstdan taxminan 50–100 marta tezroq.

```java
class CreateOrderRequestValidationTest {

    private static final ValidatorFactory FACTORY =
            Validation.buildDefaultValidatorFactory();
    private static final Validator VALIDATOR = FACTORY.getValidator();

    @AfterAll
    static void close() {
        FACTORY.close();
    }

    @Test
    void bosh_mijoz_id_va_bosh_royxat_rad_etiladi() {
        CreateOrderRequest request = new CreateOrderRequest("  ", List.of());

        Set<ConstraintViolation<CreateOrderRequest>> violations =
                VALIDATOR.validate(request);

        assertThat(violations)
                .extracting(v -> v.getPropertyPath().toString())
                .containsExactlyInAnyOrder("customerId", "lines");
    }
}
```

Custom `ConstraintValidator`ni esa to'g'ridan-to'g'ri yaratib chaqirish mumkin, chunki `initialize(A)` interfeysda standart bo'sh implementatsiyaga ega. `ConstraintValidatorContext` kerak bo'lganda (masalan custom xabar shabloni qo'shilganda) uni deep stub bilan mock qilish yetarli.

```java
class InnValidatorTest {

    private final InnValidator validator = new InnValidator();
    private final ConstraintValidatorContext context =
            mock(ConstraintValidatorContext.class, RETURNS_DEEP_STUBS);

    @ParameterizedTest
    @ValueSource(strings = {"301234567", "612345678"})
    void togri_inn_otadi(String inn) {
        assertThat(validator.isValid(inn, context)).isTrue();
    }

    @Test
    void null_qiymat_valid_hisoblanadi() {
        assertThat(validator.isValid(null, context)).isTrue();
    }

    @Test
    void qisqa_inn_rad_etiladi() {
        assertThat(validator.isValid("123", context)).isFalse();
    }
}
```

Agar validator ichida repository yoki boshqa bean ishlatilsa (masalan noyoblikni DB'dan tekshirish), uni konstruktor orqali oling — shunda mock bilan Spring'siz testlash davom etadi. Faqat `@Valid` annotatsiyasi controller'da haqiqatan ishlab turganini tekshirish uchun slice test kerak bo'ladi (7-bob).

### 6.7 Domain event va aggregate'ni testlash

Aggregate holat o'zgarishi natijasida event chiqarishi kerak. Spring Data Commons'ning `AbstractAggregateRoot` sinfi buni `registerEvent(...)` orqali qiladi, `@DomainEvents` bilan belgilangan `domainEvents()` metodi esa `protected` — shuning uchun testni aggregate bilan bir xil paketda joylashtiring yoki o'z domain qatlamingizda ochiq `List<DomainEvent> pullEvents()` metodini e'lon qiling. Ikkinchi variant Spring'ga bog'liqlikni butunlay yo'qotadi.

```java
class OrderAggregateTest {

    @Test
    void tasdiqlanganda_event_royxatga_olinadi() {
        Order order = Order.create(new CustomerId("c-1"), List.of(line()),
                Money.ZERO, Instant.parse("2026-03-01T10:00:00Z"));

        order.confirm();

        assertThat(order.pullEvents())
                .singleElement()
                .isInstanceOf(OrderConfirmedEvent.class)
                .extracting("orderId")
                .isEqualTo(order.id());
    }

    @Test
    void ikki_marta_tasdiqlash_rad_etiladi_va_event_takrorlanmaydi() {
        Order order = confirmedOrder();

        assertThatThrownBy(order::confirm).isInstanceOf(IllegalStateException.class);
        assertThat(order.pullEvents()).hasSize(1);
    }
}
```

Muhim chegara: event'ning haqiqatan e'lon qilinishi (publish) aggregate Spring Data repository orqali saqlanganda `@AfterDomainEventPublication` mexanizmi bilan sodir bo'ladi. Ya'ni "event ro'yxatga olindi" — unit test mavzusi, "event listener chaqirildi" — integratsion test mavzusi.

### 6.8 Konfiguratsiya va @ConfigurationProperties: ApplicationContextRunner

Konfiguratsiya sinflari, `@Conditional` qoidalari va xossalar bind'lanishi Spring mexanizmlari bo'lgani uchun ularni kontekstsiz tekshirib bo'lmaydi. Lekin to'liq kontekst ham shart emas: `org.springframework.boot.test.context.runner.ApplicationContextRunner` faqat siz ko'rsatgan konfiguratsiyani ko'taradi va har bir `run(...)` chaqiruvidan keyin kontekstni yopadi. Veb uchun `WebApplicationContextRunner` va `ReactiveWebApplicationContextRunner` variantlari bor.

```java
class PaymentRetryConfigurationTest {

    private final ApplicationContextRunner runner = new ApplicationContextRunner()
            .withUserConfiguration(PaymentRetryConfiguration.class);

    @Test
    void xossalar_bind_boladi() {
        runner.withPropertyValues("payment.retry.max-attempts=5",
                        "payment.retry.backoff=PT2S")
                .run(ctx -> {
                    assertThat(ctx).hasSingleBean(PaymentRetryProperties.class);
                    PaymentRetryProperties p = ctx.getBean(PaymentRetryProperties.class);
                    assertThat(p.maxAttempts()).isEqualTo(5);
                    assertThat(p.backoff()).isEqualTo(Duration.ofSeconds(2));
                });
    }

    @Test
    void ochirilganda_bean_yaratilmaydi() {
        runner.withPropertyValues("payment.retry.enabled=false")
                .run(ctx -> assertThat(ctx).doesNotHaveBean(PaymentRetryTemplate.class));
    }
}
```

Bu runner yana: `withBean(...)` bilan soxta bean qo'shish, `withConfiguration(AutoConfigurations.of(...))` bilan auto-configuration zanjirini sinash, `assertThat(ctx).hasFailed()` va `getFailure().hasMessageContaining(...)` bilan noto'g'ri qiymatda kontekst qulashini tasdiqlash imkonini beradi. Bir test ~30–200 ms vaqt oladi — `@SpringBootTest`ga nisbatan o'nlab marta tez.

### 6.9 AOP va proxy: unit testda ushlab bo'lmaydigan xatti-harakat

Spring'ning `@Transactional`, `@Cacheable`, `@Async`, `@Retryable`, `@PreAuthorize` kabi annotatsiyalari proxy (JDK dynamic proxy yoki CGLIB) orqali ishlaydi. Unit testda obyekt `new` bilan yaratilganda proxy yo'q — annotatsiyalar shunchaki e'tiborsiz qoladi. Natijada quyidagi xato unit testda hech qachon ko'rinmaydi:

```java
@Service
class ReportService {

    @Transactional
    public void importAll(List<Row> rows) {
        rows.forEach(this::importOne); // self-invocation: proxy chetlab o'tiladi
    }

    @Transactional(propagation = Propagation.REQUIRES_NEW)
    public void importOne(Row row) {
        // yangi tranzaksiya kutiladi, lekin hosil bo'lmaydi
    }
}
```

Shuningdek `private` yoki `final` metodga qo'yilgan `@Cacheable` ishlamaydi, `@Async` metodining `void` qaytaradigan versiyasida istisno yo'qoladi, `@Retryable` self-invocation'da urinishlarni takrorlamaydi. Bu xatolar faqat haqiqiy kontekst bilan — `@DataJpaTest`, `@SpringBootTest` yoki `ApplicationContextRunner` + `@EnableTransactionManagement` muhitida ushlanadi. Shu sababli: proxy semantikasi unit testning mas'uliyati emas, u 7-bobda ko'riladigan slice va integratsion testlarga tegishli. Unit testda esa bu metodlarning ichki logikasini proxy'siz tekshiring.

### 6.10 Spring'ga bog'liqlikni kamaytiruvchi arxitektura qarorlari

Spring'siz testlash imkoniyati — paket tuzilishining natijasi. Hexagonal (ports and adapters) yondashuvida domain va application qatlamlari hech qanday Spring annotatsiyasini bilmaydi, infratuzilma esa adapterlarga chiqariladi:

```text
com.example.orders
├── domain               // Spring'siz: entity, value object, policy, event
│   ├── model/Order.java
│   ├── model/Money.java
│   └── port/OrderRepository.java        // interfeys (port)
├── application          // use case'lar; faqat konstruktor DI
│   └── PlaceOrderUseCase.java
└── infrastructure       // barcha Spring annotatsiyalari shu yerda
    ├── persistence/JpaOrderRepository.java   // @Repository, adapter
    ├── web/OrderController.java              // @RestController
    └── config/OrderBeanConfiguration.java    // @Configuration, @Bean
```

Amaliy qoidalar: domain qatlamida `org.springframework.*` import'i bo'lmasin (buni 14-bobdagi arxitektura testlari bilan majburlash mumkin); bean'larni `@Component` skanerlash orqali emas, `@Configuration` ichida aniq `@Bean` metodlari bilan e'lon qiling — shunda domain sinflari toza qoladi; `Clock`, `IdGenerator`, `EventPublisher` kabi infratuzilma ehtiyojlarini domain interfeyslari sifatida ifodalang; `@Value`ni service'larga sepish o'rniga `@ConfigurationProperties` record'ini yasab, uni konstruktorga uzatilgan oddiy qiymat obyekti sifatida bering.

### 6.11 Qachon kontekst haqiqatan kerak (chegara)

Kontekstdan voz kechish — maqsad emas, vosita. Quyidagi besh holatda kontekst majburiy, chunki tekshirilayotgan narsa Spring'ning o'zi: birinchidan, bean wiring — bean'lar haqiqatan yaratiladimi, dependency'lar to'g'ri bog'lanadimi, circular dependency yo'qmi; ikkinchidan, konfiguratsiya va profil — xossalar bind bo'ladimi, `@Conditional` to'g'ri hal qiladimi, validatsiya cheklovlari ishlaydimi; uchinchidan, proxy xatti-harakati — tranzaksiya chegaralari, kesh, retry, security; to'rtinchidan, serialization — JSON yozish/o'qish, `ObjectMapper` sozlamalari, HTTP status va header'lar; beshinchidan, SQL — JPA mapping, generatsiya qilingan so'rovlar, migratsiyalar.

Amaliy nisbat: test piramidasining pastki qatlamida (soni bo'yicha ~70–80%) Spring'siz unit testlar, o'rtada slice testlar, yuqorida kam sonli to'liq integratsion testlar bo'lishi kerak. Agar loyihada `@SpringBootTest` bilan yozilgan testlar soni unit testlardan ko'p bo'lsa, bu test strategiyasining emas, kod dizaynining muammosi — dependency'lar konstruktorga chiqarilmaganligi va biznes logikasi infratuzilmaga aralashib ketganligi belgisi.

### 6.12 Arxitektor nazorat ro'yxati

- [ ] Barcha bean'lar constructor injection ishlatadi; `@Autowired` maydonlari va setter injection kod bazasida yo'q (statik tahlil yoki arxitektura testi bilan majburlangan).
- [ ] Domain va application paketlarida `org.springframework.*` import'lari yo'q; biznes logikasi `new` bilan yaratilib testlanadi.
- [ ] `java.time.Clock`, ID generator va tasodifiylik manbalari dependency sifatida kiritilgan, `Instant.now()` biznes kodida to'g'ridan-to'g'ri chaqirilmaydi.
- [ ] Mapper, validator, kalkulyator, policy va value object testlari `@SpringBootTest`siz yozilgan va butun to'plam lokal mashinada 10 sekunddan kam ishlaydi.
- [ ] `@ConfigurationProperties` va `@Conditional` xatti-harakati `ApplicationContextRunner` bilan qoplangan, shu jumladan noto'g'ri qiymatda kontekst qulashi (`hasFailed()`).
- [ ] `@Transactional`, `@Cacheable`, `@Async`, `@Retryable` ishlatilgan har bir joy integratsion test bilan qoplangan; self-invocation holatlari ko'rib chiqilgan.
- [ ] Repository port'lari domain qatlamida e'lon qilingan, shuning uchun service testlari Spring Data interfeyslarini mock qilishga muhtoj emas.
- [ ] CI'da unit testlar alohida, tez bosqichda (kontekstsiz) ishga tushadi va integratsion testlardan oldin natija qaytaradi.

---

## 7. Integratsion test: Spring Boot slice testlari (Integration Testing — Spring Boot Test Slices)

Unit testlar biznes qoidalarini tasdiqlaydi, ammo Spring ilovasining katta qismi — HTTP mapping, JSON serialization, validatsiya, JPA mapping va generatsiya qilingan SQL — framework bilan integratsiyada yashaydi va unit testda umuman tekshirilmaydi. Spring Boot bu bo'shliqni slice testlar bilan to'ldiradi: butun ilovani ko'tarmasdan, faqat bitta qatlamning auto-configuration'ini yoqadi. Bu bobda har bir slice annotatsiyasi nimani ko'taradi, nimani ko'tarmaydi, qanday yozilishi va qanday tuzoqlari borligini ko'rib chiqamiz. Barcha misollar Spring Boot 3.4+/4.x, Spring Framework 6.2+/7.x va JUnit 5 uchun.

### 7.1 Slice test g'oyasi: butun ilovani emas, bitta qatlamni ko'tarish

Oddiy `@SpringBootTest` `@SpringBootApplication`'ni topadi va uning barcha auto-configuration'larini qo'llaydi: DataSource, JPA, Flyway, Security, Kafka, cache, scheduler. Bu 5-15 sekundlik startup va yuzlab bean degani. Slice annotatsiyalari esa boshqa yo'ldan boradi — ular `@BootstrapWith` + `TypeExcludeFilter` + aniq auto-configuration ro'yxati ustiga qurilgan. Masalan `@WebMvcTest` `spring-boot-test-autoconfigure` ichidagi `spring.factories`/`AutoConfiguration.imports` metadatasidan faqat web qatlamiga tegishli auto-configuration'larni tanlaydi, qolganini o'chiradi. Shu bilan birga component scanning ham cheklanadi: slice o'z filtri ruxsat bergan stereotype'lardan boshqasini kontekstga kiritmaydi.

Arxitektor uchun muhim xulosa: slice test tezlik uchun emas, **cheklangan mas'uliyat** uchun kerak. `@WebMvcTest`'da repository mavjud emas, demak unda service logikasini test qilishning imkoni ham, ma'nosi ham yo'q. Har bir slice bitta kontraktni tekshiradi.

| Annotatsiya | Nima ko'tariladi | Qachon ishlatiladi |
| --- | --- | --- |
| `@WebMvcTest` | DispatcherServlet, `@Controller`, `@ControllerAdvice`, `Converter`/`GenericConverter`, `Filter`, `HandlerInterceptor`, `WebMvcConfigurer`, Jackson, MockMvc, Spring Security config | HTTP kontrakti: status, JSON shakli, header, validatsiya, xato mapping |
| `@WebFluxTest` | WebFlux infra, `@Controller`, `@ControllerAdvice`, `WebFilter`, codec'lar, `WebTestClient` | Reactive controller va stream kontrakti |
| `@DataJpaTest` | `@Entity`, Spring Data JPA repository, `EntityManager`, `TestEntityManager`, embedded DB, tranzaksiya + rollback | Query, mapping, fetch strategiya, projection |
| `@JdbcTest` | `JdbcTemplate`, `DataSource`, tranzaksiya | Qo'lda yozilgan SQL, DAO |
| `@DataJdbcTest` | Spring Data JDBC repository + aggregate mapping | Spring Data JDBC loyihalari |
| `@JsonTest` | `ObjectMapper`, `@JsonComponent`, `Module`, `JacksonTester` | Serialization/deserialization kontrakti |
| `@RestClientTest` | `RestClient.Builder`/`RestTemplateBuilder`, `MockRestServiceServer` | Chiquvchi HTTP client logikasi |
| `@SpringBootTest` | Butun kontekst (+ ixtiyoriy real server) | Qatlamlar kesishgan oqim, real HTTP, konfiguratsiya tekshiruvi |

### 7.2 @WebMvcTest: web qatlamni izolyatsiyada testlash

`@WebMvcTest(OrderController.class)` argumenti berilsa faqat shu controller ro'yxatga olinadi; argumentsiz chaqirilsa barcha controller'lar ko'tariladi (sekinroq va ko'proq mock talab qiladi). `@Service`, `@Repository`, `@Component` bean'lari **ko'tarilmaydi** — controller bog'liqliklari `@MockitoBean` orqali almashtiriladi. Spring Boot 3.4'dan `@MockBean` va `@SpyBean` deprecated, Spring Boot 4'da olib tashlangan; o'rniga Spring Framework 6.2'ning `org.springframework.test.context.bean.override.mockito.MockitoBean` va `MockitoSpyBean` ishlatiladi.

```java
@WebMvcTest(OrderController.class)
class OrderControllerWebMvcTest {

    @Autowired MockMvc mockMvc;

    @MockitoBean OrderService orderService;

    @Test
    void returnsOrderAsJson() throws Exception {
        given(orderService.findById(42L))
                .willReturn(new OrderView(42L, "NEW", new BigDecimal("199.90")));

        mockMvc.perform(get("/api/orders/42").accept(APPLICATION_JSON))
                .andExpect(status().isOk())
                .andExpect(header().string("Cache-Control", "no-store"))
                .andExpect(content().contentTypeCompatibleWith(APPLICATION_JSON))
                .andExpect(jsonPath("$.id").value(42))
                .andExpect(jsonPath("$.status").value("NEW"))
                .andExpect(jsonPath("$.total").value(199.90))
                .andExpect(jsonPath("$.internalCost").doesNotExist());

        then(orderService).should().findById(42L);
    }
}
```

Oxirgi `doesNotExist()` tekshiruvi — bu web qatlam testining eng qimmatli turi: API tashqariga chiqmasligi kerak bo'lgan maydonni ushlaydi. Xato yo'llari ham shu yerda tekshiriladi. Spring Framework 6'dan boshlab standart xato formati RFC 9457 `ProblemDetail`; `spring.mvc.problemdetails.enabled=true` bo'lsa framework xatolari `application/problem+json` sifatida qaytadi, maydon xatolari ro'yxati esa odatda `ResponseEntityExceptionHandler`'dan meros olgan `@ControllerAdvice`'da `properties`'ga qo'shiladi.

```java
@Test
void rejectsInvalidPayloadWithProblemDetail() throws Exception {
    mockMvc.perform(post("/api/orders")
                    .contentType(APPLICATION_JSON)
                    .content("""
                            {"customerId": null, "quantity": 0}
                            """))
            .andExpect(status().isBadRequest())
            .andExpect(content().contentTypeCompatibleWith("application/problem+json"))
            .andExpect(jsonPath("$.status").value(400))
            .andExpect(jsonPath("$.errors[*].field",
                    containsInAnyOrder("customerId", "quantity")));
}

@Test
void returns404WhenOrderMissing() throws Exception {
    given(orderService.findById(7L)).willThrow(new OrderNotFoundException(7L));

    mockMvc.perform(get("/api/orders/7"))
            .andExpect(status().isNotFound())
            .andExpect(jsonPath("$.type").value("urn:problem-type:order-not-found"))
            .andExpect(jsonPath("$.detail").value("Order 7 not found"));
}
```

Spring Framework 6.2'dan `MockMvcTester` ham mavjud — AssertJ uslubida: `assertThat(mvc.get().uri("/api/orders/42")).hasStatusOk().bodyJson().extractingPath("$.status").isEqualTo("NEW")`. Yangi loyihalarda u o'qilishi osonroq, eski `MockMvc` esa to'liq qo'llab-quvvatlanadi.

### 7.3 @WebFluxTest va WebTestClient bilan reactive controller

`@WebFluxTest` WebFlux infrastrukturasini va `WebTestClient`'ni ko'taradi, `@Controller`/`@ControllerAdvice`/`WebFilter`/codec'larni skanerlaydi, service va repository'ni esa yo'q. Muhim nuans: `RouterFunction` bean'lari orqali e'lon qilingan functional endpoint'lar skanerlanmaydi — ularni `@Import(OrderRoutes.class)` bilan aniq keltirish kerak.

```java
@WebFluxTest(controllers = ReactiveOrderController.class)
class ReactiveOrderControllerTest {

    @Autowired WebTestClient webTestClient;

    @MockitoBean ReactiveOrderService service;

    @Test
    void streamsOrders() {
        given(service.findAll()).willReturn(Flux.just(
                new OrderView(1L, "NEW", BigDecimal.ONE),
                new OrderView(2L, "PAID", BigDecimal.TEN)));

        webTestClient.get().uri("/api/orders")
                .accept(MediaType.APPLICATION_JSON)
                .exchange()
                .expectStatus().isOk()
                .expectHeader().contentTypeCompatibleWith(MediaType.APPLICATION_JSON)
                .expectBodyList(OrderView.class)
                .hasSize(2)
                .value(list -> assertThat(list).extracting(OrderView::status)
                        .containsExactly("NEW", "PAID"));
    }
}
```

`WebTestClient` faqat reactive uchun emas: `@SpringBootTest(webEnvironment = RANDOM_PORT)` bilan birga real HTTP ustida ham, `@AutoConfigureWebTestClient` bilan MVC ilovasida mock server ustida ham ishlaydi.

### 7.4 @DataJpaTest: persistence qatlami va TestEntityManager

`@DataJpaTest` `@Entity` sinflarini, Spring Data JPA repository'larini, `EntityManager` va `TestEntityManager`'ni ko'taradi; service qatlamini ko'tarmaydi. Har bir test metodi default'da tranzaksiya ichida ishlaydi va oxirida **rollback** qilinadi, shuning uchun testlar bir-biriga ta'sir qilmaydi.

Asosiy xavf — `@AutoConfigureTestDatabase`. `@DataJpaTest` uni `replace = Replace.ANY` bilan qo'llaydi, ya'ni sizning haqiqiy DataSource'ingizni classpath'dagi embedded bazaga (odatda H2) **jimgina** almashtiradi. Natijada siz PostgreSQL uchun yozilgan native query, `jsonb`, `ON CONFLICT` yoki partial index'ni H2'da test qilgan bo'lib qolasiz. Real bazada ishlash uchun `@AutoConfigureTestDatabase(replace = Replace.NONE)` yoki Spring Boot 3.4+'dagi `Replace.NON_TEST` (test o'zi e'lon qilgan DataSource'ni saqlaydi) ishlatiladi; real baza bilan ishlash 8-bobning mavzusi.

```java
public interface OrderRepository extends JpaRepository<Order, Long>,
        JpaSpecificationExecutor<Order> {

    @Query("""
           select o.id as id, c.name as customerName, o.total as total
           from Order o join o.customer c
           where o.status = :status and o.createdAt < :before
           """)
    List<OrderSummary> findOverdue(Status status, LocalDate before);

    @Query("select o from Order o join fetch o.items")
    List<Order> findAllWithItems();

    interface OrderSummary {
        Long getId();
        String getCustomerName();
        BigDecimal getTotal();
    }
}
```

```java
@DataJpaTest
class OrderRepositoryTest {

    @Autowired TestEntityManager em;
    @Autowired OrderRepository repository;

    @Test
    void findsOverdueOrdersWithProjection() {
        Customer customer = em.persistFlushFind(new Customer("ACME"));
        em.persist(new Order(customer, Status.NEW, LocalDate.of(2026, 1, 1)));
        em.persist(new Order(customer, Status.PAID, LocalDate.of(2026, 1, 1)));
        em.flush();
        em.clear();

        var result = repository.findOverdue(Status.NEW, LocalDate.of(2026, 2, 1));

        assertThat(result).hasSize(1).first().satisfies(s -> {
            assertThat(s.getCustomerName()).isEqualTo("ACME");
            assertThat(s.getId()).isNotNull();
        });
    }

    @Test
    void specificationFiltersByStatusIn() {
        assertThat(repository.findAll(OrderSpecs.statusIn(Status.NEW))).isEmpty();
    }
}
```

`em.flush()` va `em.clear()` juftligi majburiy odat bo'lishi kerak: ularsiz query first-level cache'dan javob olishi mumkin va siz SQL'ni emas, Hibernate keshini test qilasiz.

### 7.5 N+1 va generatsiya qilingan SQL'ni testda ushlash

Fetch strategiyasi — bu kod review'da emas, testda ushlanadigan narsa. Eng arzon usul: Hibernate `Statistics`'ni yoqib, query sonini tasdiqlash. Shunda `join fetch` yoki `@EntityGraph` olib tashlansa test qizil bo'ladi.

```java
@DataJpaTest(properties = "spring.jpa.properties.hibernate.generate_statistics=true")
class OrderFetchPlanTest {

    @Autowired OrderRepository repository;
    @Autowired EntityManagerFactory emf;

    private Statistics stats() {
        return emf.unwrap(SessionFactory.class).getStatistics();
    }

    @Test
    void fetchJoinAvoidsNPlusOneOnItems() {
        // ... 3 order, har birida 2 item saqlangan, keyin em.clear()
        stats().clear();

        List<Order> orders = repository.findAllWithItems();
        orders.forEach(order -> order.getItems().size());

        assertThat(stats().getPrepareStatementCount())
                .as("items uchun qo'shimcha select bo'lmasligi kerak")
                .isEqualTo(1);
        assertThat(stats().getCollectionFetchCount()).isZero();
    }
}
```

Ikkinchi variant — `net.ttddyy:datasource-proxy` bilan DataSource'ni o'rab, `QueryCountHolder` orqali SELECT/INSERT/UPDATE sonini alohida tekshirish; u JPA'siz (`@JdbcTest`, `@DataJdbcTest`) ham ishlaydi va SQL matnini ham ko'rsatadi. Qaysi vositani tanlasangiz ham, qoida bitta: query sonini **aniq raqam** bilan tasdiqlang, "ko'p emas" deb emas.

### 7.6 @JdbcTest, @DataJdbcTest, @JsonTest, @RestClientTest

`@JdbcTest` faqat `DataSource` + `JdbcTemplate` + tranzaksiya beradi, bean skanerlash yo'q — qo'lda yozilgan SQL va DAO uchun ideal. `@DataJdbcTest` bunga Spring Data JDBC repository va aggregate mapping'ni qo'shadi. Ikkisi ham `@AutoConfigureTestDatabase`'ni `@DataJpaTest` kabi qo'llaydi, demak H2 xavfi aynan shu yerda ham bor.

`@JsonTest` serialization kontraktini arzon tekshiradi: `ObjectMapper`, `@JsonComponent`, custom `Module` va `JacksonTester` ko'tariladi. Bu API versiyalanishi uchun juda muhim — `isEqualToJson` referens fayl bilan solishtiradi va maydon nomi tasodifan o'zgarsa darhol sinadi.

```java
@JsonTest
class OrderViewJsonTest {

    @Autowired JacksonTester<OrderView> json;

    @Test
    void serializesContract() throws Exception {
        OrderView view = new OrderView(42L, "NEW", new BigDecimal("199.90"));

        assertThat(json.write(view)).isEqualToJson("/contract/order-view.json");
        assertThat(json.write(view)).hasJsonPathStringValue("@.status");
    }

    @Test
    void toleratesUnknownFieldsFromProducer() throws Exception {
        String payload = """
                {"id": 42, "status": "NEW", "total": 199.90, "addedInV2": true}
                """;

        assertThat(json.parseObject(payload).id()).isEqualTo(42L);
    }
}
```

`@RestClientTest` chiquvchi client'ni test qiladi: `RestClient.Builder`/`RestTemplateBuilder` va `MockRestServiceServer` auto-configure qilinadi. Shart: client o'z `RestClient`'ini **inject qilingan builder**'dan qurishi kerak, aks holda mock server hech narsani ushlamaydi.

```java
@RestClientTest(PricingClient.class)
class PricingClientTest {

    @Autowired PricingClient client;
    @Autowired MockRestServiceServer server;

    @Test
    void sendsApiKeyAndParsesResponse() {
        server.expect(requestTo("https://pricing.internal/v1/quote?sku=A-1"))
                .andExpect(method(HttpMethod.GET))
                .andExpect(header("X-Api-Key", "test-key"))
                .andRespond(withSuccess("""
                        {"sku":"A-1","price":12.50}
                        """, MediaType.APPLICATION_JSON));

        Quote quote = client.quote("A-1");

        assertThat(quote.price()).isEqualByComparingTo("12.50");
        server.verify();
    }
}
```

`MockRestServiceServer` bitta client sinfining kontraktini tekshirish uchun yetarli; retry, timeout va butun protokol xatti-harakatini real HTTP ustida tekshirish 9-bobdagi WireMock vazifasi.

### 7.7 @SpringBootTest: qachon kerak va webEnvironment variantlari

`@SpringBootTest` faqat qatlamlar kesishgan joyda kerak: tranzaksiya chegaralari, event'lar, security filter chain, konfiguratsiya binding, Flyway migratsiyasi bilan mapping muvofiqligi. `webEnvironment` to'rtta qiymatga ega: `MOCK` (default — mock servlet muhiti, real port yo'q, `@AutoConfigureMockMvc` bilan MockMvc), `RANDOM_PORT` (real server, bo'sh port, `@LocalServerPort`), `DEFINED_PORT` (`server.port` — CI'da port to'qnashuvi sababli tavsiya etilmaydi), `NONE` (web muhiti umuman yo'q — batch, scheduler, messaging uchun).

```java
@SpringBootTest(webEnvironment = WebEnvironment.RANDOM_PORT)
@ActiveProfiles("test")
class OrderCheckoutHttpTest {

    @Autowired TestRestTemplate restTemplate;
    @LocalServerPort int port;

    @Test
    void createsOrderAndReturnsLocationHeader() {
        var response = restTemplate.postForEntity(
                "/api/orders", new CreateOrderRequest(1L, 2), Void.class);

        assertThat(response.getStatusCode()).isEqualTo(HttpStatus.CREATED);
        URI location = response.getHeaders().getLocation();
        assertThat(location).asString()
                .startsWith("http://localhost:" + port + "/api/orders/");

        var created = restTemplate.getForEntity(location, OrderView.class);
        assertThat(created.getBody().status()).isEqualTo("NEW");
    }
}
```

`TestRestTemplate` 4xx/5xx'da exception tashlamaydi — bu xato javoblarini tekshirishni osonlashtiradi. Muqobil variant `WebTestClient` (`@AutoConfigureWebTestClient` yoki `RANDOM_PORT` bilan): fluent assertion va JSON ustida ishlash qulayroq.

### 7.8 Kontekst keshi: eng katta tezlik omili

Spring TestContext Framework kontekstlarni keshlaydi, kalit esa `MergedContextConfiguration`'dan hosil bo'ladi: konfiguratsiya sinflari/locations, active profile'lar, `@TestPropertySource` locations va inlined properties, `ApplicationContextInitializer`'lar, `ContextCustomizer`'lar (shu jumladan har bir `@MockitoBean`/`@MockitoSpyBean`/`@TestBean` e'loni va `@DynamicPropertySource`), parent kontekst va web resource base path. Ya'ni bitta qo'shimcha `@TestPropertySource(properties = "feature.x=true")` ham **butunlay yangi kontekst** yaratadi.

Raqamli ta'sir: tasavvur qiling, 40 ta integratsion test sinfi bor va har biri bir oz boshqacha konfiguratsiyaga ega. Startup 5 sekund bo'lsa — 40 x 5 = 200 sekund faqat kontekst ko'tarishga ketadi. Shu 40 sinf 3 ta umumiy konfiguratsiyaga keltirilsa, xarajat 15 sekundga tushadi, ya'ni suite'ning sof foydasiz vaqti ~13 barobar qisqaradi. Bundan tashqari kesh hajmi default'da 32 (`spring.test.context.cache.maxSize`); undan oshsa LRU evicting boshlanadi va chiqarib yuborilgan kontekst keyinroq **qaytadan** quriladi. `org.springframework.test.context.cache` logger'ini DEBUG'ga qo'yib kesh statistikasini (hit/miss/size) ko'rish mumkin.

`@DirtiesContext` eng qimmat annotatsiya: u kontekstni keshdan o'chiradi, demak keyingi test uni noldan ko'taradi. Uni "ehtiyot uchun" qo'yish suite'ni sekinlashtirishning eng tez usuli; holatni testning o'zida tozalash deyarli har doim arzonroq. Strategiya oddiy: bitta umumiy abstract bazaviy sinf, bitta profil, mock'lar faqat shu bazaviy sinfda yoki umuman yo'q.

```java
@SpringBootTest
@AutoConfigureMockMvc
@ActiveProfiles("test")
public abstract class AbstractIntegrationTest {
    // Bu yerda @TestPropertySource, @MockitoBean yoki @DirtiesContext YO'Q:
    // ularning har bir kombinatsiyasi yangi kontekst kaliti demakdir.
    @Autowired protected MockMvc mockMvc;
}

class OrderApiTest extends AbstractIntegrationTest { /* ... */ }

class PaymentApiTest extends AbstractIntegrationTest { /* ... */ }
```

### 7.9 @TestConfiguration, bean override va property manbalari

`@TestConfiguration` — `@Configuration`'ning test variantidir: test sinfi ichidagi static nested klass avtomatik qo'llanadi, top-level sinf esa `@Import` bilan keltiriladi va component scan tomonidan olinmaydi. U yangi bean qo'shish uchun ideal (masalan fixed `Clock`). Mavjud bean'ni **almashtirish** uchun esa ehtiyot bo'lish kerak: Spring Boot'da bean definition overriding default'da o'chirilgan, shuning uchun bir xil nomdagi `@Bean` xatoga olib keladi. To'g'ri yechim — `@TestBean` (static factory metod bilan almashtirish), `@MockitoBean` (mock bilan), yoki `@MockitoSpyBean` (real bean, lekin chaqiruvlarni tasdiqlash imkoni bilan).

```java
@SpringBootTest
@ActiveProfiles("test")
class PaymentFlowTest {

    @TestConfiguration
    static class FixedClockConfig {
        @Bean Clock testClock() {
            return Clock.fixed(Instant.parse("2026-01-15T10:00:00Z"), ZoneOffset.UTC);
        }
    }

    @DynamicPropertySource
    static void props(DynamicPropertyRegistry registry) {
        registry.add("payment.timeout", () -> "250ms");
    }

    @MockitoBean PaymentGateway gateway;        // tashqi tizim: mock
    @MockitoSpyBean OrderNotifier notifier;     // real bean + verify

    @Test
    void notifiesCustomerOnce() {
        given(gateway.charge(any())).willReturn(PaymentResult.approved("tx-1"));
        // ... oqim ishga tushiriladi
        then(notifier).should().notifyPaid(anyLong());
    }
}
```

Property'lar uchun uch qatlam bor: `@TestPropertySource(properties = ...)` — bir nechta test uchun statik qiymatlar; `@DynamicPropertySource` — runtime'da hisoblangan qiymatlar (port, URL); `src/test/resources/application-test.yml` — profil bilan faollashadigan umumiy test konfiguratsiyasi. Muhim tuzoq: `src/test/resources/application.yml` test classpath'da birinchi bo'lgani uchun asosiy `application.yml`'ni **to'liq soya qiladi**, qo'shilmaydi. Shu sababli test sozlamalarini profilga bog'langan alohida faylda saqlash xavfsizroq.

### 7.10 @ActiveProfiles bilan test konfiguratsiyasini ajratish

`@ActiveProfiles("test")` nafaqat `application-test.yml`'ni yoqadi, balki `@Profile` bilan belgilangan bean'larni almashtirish imkonini beradi: `@Profile("!test")` bilan real email sender, `@Profile("test")` bilan no-op sender. Bu kontekst kalitining qismi, shuning uchun profil nomlari sonini minimumda tutish kerak — har bir yangi profil kombinatsiyasi yangi kontekst. Ikkinchi qoida: production konfiguratsiyasida test uchun maxsus shart bo'lmasin. `@Profile("test")` tekshiruvi production sinfida paydo bo'lishi — arxitekturaviy nuqson, buni test-only konfiguratsiya sinfiga ko'chirish kerak.

### 7.11 @Sql, @SqlMergeMode va tranzaksion testning tuzoqlari

`@Sql` deklarativ ravishda script ishga tushiradi: sinf va metod darajasida, `executionPhase` bilan test oldidan yoki keyin. Default'da metod darajasidagi `@Sql` sinf darajasini **almashtiradi**; `@SqlMergeMode(MergeMode.MERGE)` ikkisini birlashtiradi (avval sinf, keyin metod).

```java
@SpringBootTest
@ActiveProfiles("test")
@Sql("/sql/reference-data.sql")
@SqlMergeMode(SqlMergeMode.MergeMode.MERGE)
class OrderArchiveJobTest {

    @Autowired OrderArchiveJob job;
    @Autowired JdbcTemplate jdbc;

    @Test
    @Sql("/sql/orders-2025.sql")
    @Sql(scripts = "/sql/cleanup-orders.sql",
         executionPhase = Sql.ExecutionPhase.AFTER_TEST_METHOD)
    void archivesOnlyClosedOrdersAndPublishesEventAfterCommit() {
        job.run();   // ichida @Transactional va AFTER_COMMIT listener bor

        Integer archived = jdbc.queryForObject(
                "select count(*) from order_archive", Integer.class);
        assertThat(archived).isEqualTo(2);
    }
}
```

E'tibor bering: bu sinfda `@Transactional` **yo'q**, tozalash esa `@Sql`'ning AFTER fazasi bilan bajariladi. Buning sababi tranzaksion testning to'rtta tuzog'i: (1) lazy loading test ichida ishlaydi, chunki Session ochiq — production'da esa `LazyInitializationException` chiqadi; (2) `flush` bo'lmagani uchun constraint va trigger xatolari yashirinadi; (3) real commit bo'lmagani uchun `@TransactionalEventListener(phase = AFTER_COMMIT)` va `afterCommit` callback'lari hech qachon ishlamaydi; (4) `webEnvironment = RANDOM_PORT`'da test tranzaksiyasi server thread'iga umuman tegmaydi, demak rollback illyuziya bo'ladi. Shu hollarda `@Transactional`'ni olib tashlab, tozalashni aniq qilish kerak; oraliq variant — `TestTransaction.flagForCommit()`/`end()`/`start()` bilan tranzaksiya chegaralarini test ichida qo'lda boshqarish yoki `@Commit` ishlatish.

### 7.12 Slice test anti-patternlari

**Hamma joyda `@SpringBootTest`.** Eng keng tarqalgan xato: controller mapping'ini tekshirish uchun butun kontekst ko'tariladi. Natija — sekin suite va noaniq xato sabablari. Qoida: `@WebMvcTest` yetsa, `@SpringBootTest` ishlatilmasin.

**Kontekstni har testda iflos qilish.** `@DirtiesContext`, test-ga xos `@TestPropertySource`, har sinfda boshqa `@MockitoBean` to'plami — bularning har biri yangi kontekst. Bu "biz CI'ni kuchaytirmoqchimiz" muammosining asl sababi.

**H2'da PostgreSQL xatti-harakatini kutish.** `@DataJpaTest`'ning jimgina DataSource almashtirishi eng xavfli default. H2 boshqa SQL dialekti, boshqa tip tizimi, boshqa lock va isolation semantikasi. H2 mapping va oddiy query uchun yaroqli, lekin baza xatti-harakati haqidagi hech bir xulosaga asos bo'lmaydi.

**MockMvc bilan biznes logikani testlash.** Agar `@WebMvcTest`'da narx hisoblash yoki chegirma qoidalari tekshirilayotgan bo'lsa, demak logika controller'da qolib ketgan yoki test noto'g'ri qatlamda yozilgan. HTTP testi faqat kontraktni tekshirsin.

**Slice'ni mock bilan to'ldirish.** `@WebMvcTest`'da o'nta `@MockitoBean` bo'lsa, controller haddan tashqari ko'p bog'liqlikka ega. Test dizayn muammosini ko'rsatib turadi — buni tuzatish kerak, mock qo'shish emas.

### 7.13 Arxitektor nazorat ro'yxati

- [ ] Har bir test o'z qatlamiga mos slice annotatsiyasidan foydalanadi; `@SpringBootTest` faqat qatlamlar kesishgan oqimlar uchun qoldirilgan.
- [ ] `@MockBean`/`@SpyBean` butun kod bazasidan olib tashlangan, o'rniga `@MockitoBean`/`@MockitoSpyBean`/`@TestBean` ishlatiladi.
- [ ] Integratsion testlar bitta umumiy abstract bazaviy sinfdan meros oladi; kontekstlar soni o'lchangan va 3-5 atrofida ushlab turiladi.
- [ ] `@DirtiesContext` ishlatilgan har bir joy asoslangan; aks holda holat testning o'zida tozalanadi.
- [ ] `@DataJpaTest` qaysi bazada ishlayotgani aniq: H2 faqat mapping uchun, baza xatti-harakatiga bog'liq query'lar real bazada tekshiriladi.
- [ ] Kritik query'lar uchun query soni (Hibernate statistics yoki datasource-proxy) aniq raqam bilan tasdiqlangan, N+1 regressiya testda ushlanadi.
- [ ] API kontrakti (JSON maydonlari, status kodlari, `ProblemDetail` formati) `@WebMvcTest`/`@JsonTest` bilan qoplangan, ichki maydonlar sizib chiqmasligi tekshirilgan.
- [ ] Commit'dan keyingi xatti-harakat (AFTER_COMMIT event, trigger, constraint) tranzaksiyasiz testda tekshiriladi, tozalash esa `@Sql` yoki aniq cleanup bilan bajariladi.

---

## 8. Testcontainers bilan real infratuzilmada test (Integration Testing with Testcontainers)

Integratsion test faqat "ko'proq bean ko'tarish" degani emas — bu sizning kodingiz ishlab chiqarishda uchraydigan real infratuzilma bilan muloqotini tasdiqlash. Testcontainers (1.19+ va ayniqsa 1.20+) Docker konteynerlarini test hayot aylanishiga bog'laydi, Spring Boot 3.1+ esa `@ServiceConnection` orqali bu konteynerlarni avtomatik konfiguratsiya qiladi, ya'ni property'larni qo'lda yozish zaruriyati yo'qoladi. Bu bobda arxitektor nuqtai nazaridan qaror daraxti beriladi: qachon real konteyner kerak, qanday qilib uni tez va barqaror ushlab turish, va qaysi naqshlar test bazangizni sekin hamda ishonchsiz qiladi.

### 8.1 Nega H2 yoki in-memory baza yetarli emas

H2 `MODE=PostgreSQL` rejimida ham PostgreSQL emulyatori bo'lib qolaveradi — u sintaksisning bir qismini qabul qiladi, lekin semantikasi boshqa. Natijada test yashil, prod qizil bo'ladi. Eng ko'p uchraydigan farqlar:

**SQL dialekti va funksiyalar.** `INSERT ... ON CONFLICT (id) DO UPDATE`, `FILTER (WHERE ...)`, `DISTINCT ON`, `LATERAL JOIN`, window funksiyalarning ayrim shakllari, `generate_series`, `tsvector`/`to_tsquery` full-text izlash, `ILIKE`, massiv tiplari (`text[]`, `unnest`) — H2'da yo yo'q, yo boshqacha ishlaydi. Agar repository'da `@Query(nativeQuery = true)` bo'lsa, H2 testi faqat "metod chaqirildi"ni tasdiqlaydi.

**Tip tizimi.** PostgreSQL'da `jsonb` indekslanadigan va operatorlari (`->>`, `@>`, `jsonb_path_query`) bor haqiqiy tip; H2'da bu `CLOB`/`JSON` ko'rinishida taqlid qilinadi. `numeric` aniqligi, `timestamptz` va `timestamp` farqi, `interval`, `uuid`, `enum` tiplari, `citext` — barchasi xatti-harakat farqi manbai. Klassik bug: `timestamptz` ustunga `LocalDateTime` yozilib, prod'da server time zone UTC bo'lgani uchun soat siljiydi — H2'da bu hech qachon ko'rinmaydi.

**Locking va tranzaksiya izolyatsiyasi.** `SELECT ... FOR UPDATE SKIP LOCKED` (navbat/outbox naqshining asosi), `FOR UPDATE NOWAIT`, advisory lock'lar (`pg_advisory_xact_lock`), `REPEATABLE READ`da seriyalizatsiya xatosi (`40001`), deadlock aniqlanishi va `SQLState` kodlari — H2'da yoki yo'q, yoki boshqa xato kodi beradi. Optimistik/pessimistik locking retry logikasini H2'da sinash deyarli ma'nosiz.

**Sequence va identifier generatsiyasi.** Hibernate `SEQUENCE` strategiyasi, `allocationSize`, `IDENTITY` bilan batch insert o'chib qolishi, `nextval` keshlanishi — PostgreSQL'ga xos. H2'da sekvens raqamlari boshqa tartibda beriladi va "aynan shu ID" ga asoslangan assert'lar yolg'on ishonch beradi.

**Index va constraint xatti-harakati.** Partial index (`WHERE deleted_at IS NULL`), `UNIQUE` index NULL'larni qanday ko'rishi, `GIN`/`GiST`, `CREATE INDEX CONCURRENTLY`, `DEFERRABLE` constraint'lar, `ON DELETE CASCADE` tartibi, unique violation'ning `23505` kodi — real bazada boshqacha. Unique constraint buzilishini "do'stona xato"ga aylantiruvchi handler faqat PostgreSQL'da to'g'ri sinaladi.

**Migratsiya skriptlari.** Bu eng og'riqli nuqta: Flyway/Liquibase skriptlari `CREATE EXTENSION pgcrypto`, `ALTER TYPE ... ADD VALUE`, `CREATE INDEX CONCURRENTLY`, `jsonb_set` ishlatsa, H2 ularni umuman bajara olmaydi. Natijada jamoa "test uchun alohida schema.sql" yozadi — va shu lahzada test real DDL'ni tekshirishdan voz kechadi. Migratsiyani tekshirish qobiliyatini yo'qotish Testcontainers'ga o'tish uchun yetarli yakka sabab.

### 8.2 Testcontainers asoslari: Docker API ustida hayot aylanishi

Testcontainers — Docker daemon'ning HTTP API'si ustidagi Java kutubxonasi. U `DOCKER_HOST`ni aniqlaydi (Docker Desktop, Colima, Podman, Rancher Desktop, Testcontainers Cloud), kerakli image'ni pull qiladi, konteynerni ko'taradi va tozalashni **Ryuk** nomli sidecar konteynerga topshiradi: JVM to'satdan o'lsa ham Ryuk label'i bo'yicha konteynerlarni o'chiradi, ya'ni "orfan" konteynerlar qolmaydi.

Hayot aylanishi: `start()` → image pull → create → start → wait strategy bajariladi → konteyner "ready" deb belgilanadi → test ishlaydi → `stop()`/Ryuk tozalaydi.

**Port mapping muhim arxitektura detali.** Konteyner ichidagi port (masalan 5432) host'da **tasodifiy ephemeral portga** map qilinadi. Shuning uchun hech qachon `localhost:5432` deb qo'lda yozmaysiz — `container.getMappedPort(5432)`, `getHost()`, `getJdbcUrl()`, `getBootstrapServers()` metodlarini ishlatasiz. Bu random port parallel testlarda to'qnashuvni o'z-o'zidan hal qiladi.

JUnit 5 integratsiyasi `org.testcontainers:junit-jupiter` modulidan keladi: `@Testcontainers` annotatsiyasi extension'ni yoqadi, `@Container` esa maydonni boshqaradi — **instance** maydon har test metodidan oldin yangi konteyner ko'taradi, **static** maydon butun sinf uchun bir marta. Prodga yaqin loyihada deyarli hamma vaqt `static` to'g'ri javob.

Wait strategiyasi — barqarorlikning kaliti. Uch asosiy tur: `Wait.forListeningPort()` (TCP ochilishi — eng zaif, chunki port ochilishi "xizmat tayyor" degani emas), `Wait.forLogMessage(regex, times)` (log'dagi tayyorlik satrini kutish), `Wait.forHttp("/health").forStatusCode(200)` (HTTP probe). Qo'shimcha: `Wait.forHealthcheck()` agar image'da Docker HEALTHCHECK bo'lsa, va `Wait.forSuccessfulCommand(...)`. Modullarning o'z default strategiyasi bor (`PostgreSQLContainer` log'dagi tayyorlik xabarini ikki marta kutadi), lekin custom image yoki o'z app konteyneringiz uchun strategiyani ochiq yozish shart.

```xml
<dependency>
  <groupId>org.springframework.boot</groupId>
  <artifactId>spring-boot-testcontainers</artifactId>
  <scope>test</scope>
</dependency>
<dependency>
  <groupId>org.testcontainers</groupId>
  <artifactId>junit-jupiter</artifactId>
  <scope>test</scope>
</dependency>
<dependency>
  <groupId>org.testcontainers</groupId>
  <artifactId>postgresql</artifactId>
  <scope>test</scope>
</dependency>
<dependency>
  <groupId>org.awaitility</groupId>
  <artifactId>awaitility</artifactId>
  <scope>test</scope>
</dependency>
```

Testcontainers versiyasini qo'lda yozmang: `spring-boot-dependencies` BOM uni boshqaradi, aks holda `org.testcontainers:testcontainers-bom` import qiling.

### 8.3 Spring Boot bilan integratsiya: @ServiceConnection va @DynamicPropertySource

Spring Boot 3.1'dan beri eng toza usul — `@ServiceConnection`. U `ConnectionDetails` bean'ini yaratadi va auto-konfiguratsiya property'lar o'rniga shu bean'dan foydalanadi. Siz URL, username, password, driver nomini yozmaysiz; konteyner turiga qarab Boot o'zi aniqlaydi.

```java
@SpringBootTest
@Testcontainers
class OrderRepositoryIT {

    @Container
    @ServiceConnection
    static PostgreSQLContainer<?> postgres =
            new PostgreSQLContainer<>("postgres:16.4-alpine");

    @Autowired
    OrderRepository repository;

    @Test
    void saves_and_reads_back_jsonb_payload() {
        Order saved = repository.save(new Order("A-1", Map.of("ref", "X")));

        Order found = repository.findById(saved.getId()).orElseThrow();

        assertThat(found.getPayload()).containsEntry("ref", "X");
    }
}
```

Boot 3.1'dan oldingi (va hali ham qo'l keladigan) usul — `@DynamicPropertySource`: konteyner ko'tarilgandan keyin `Environment`ga property qo'shiladi. `Supplier` ishlatilgani uchun qiymat kech, ya'ni konteyner start bo'lgandan keyin o'qiladi.

```java
@SpringBootTest
@Testcontainers
class LegacyPropertiesIT {

    @Container
    static PostgreSQLContainer<?> postgres =
            new PostgreSQLContainer<>("postgres:16.4-alpine")
                    .waitingFor(Wait.forListeningPort());

    @DynamicPropertySource
    static void datasource(DynamicPropertyRegistry registry) {
        registry.add("spring.datasource.url", postgres::getJdbcUrl);
        registry.add("spring.datasource.username", postgres::getUsername);
        registry.add("spring.datasource.password", postgres::getPassword);
    }
}
```

Taqqoslash: `@ServiceConnection` kamroq kod, property nomini xato yozish imkoni yo'q, Boot qo'llab-quvvatlagan barcha xizmatlar uchun bir xil, va SSL/credential detallarini o'zi uzatadi. `@DynamicPropertySource` esa moslashuvchan — `@ServiceConnection` qo'llab-quvvatlamaydigan xizmatlar (masalan custom `app.external.base-url`, LocalStack endpoint'lari, Keycloak issuer URI) uchun hamon kerak. Amaliy qoida: **standart infratuzilma uchun `@ServiceConnection`, nostandart property'lar uchun `@DynamicPropertySource`** — ikkisi bir sinfda bemalol yashaydi.

### 8.4 Singleton container pattern va kontekst keshi

Agar har integratsion test sinfi o'z konteynerini ko'tarsa, 40 sinfli loyihada 40 marta PostgreSQL start bo'ladi. Singleton container pattern buni oldini oladi: konteyner `static final` maydonda, JVM ichida bir marta ko'tariladi va JVM tugashida Ryuk tozalaydi. `@Container` annotatsiyasi **ishlatilmaydi** — aks holda JUnit uni sinf oxirida to'xtatib qo'yadi.

```java
@SpringBootTest
@ActiveProfiles("integration")
public abstract class AbstractIntegrationTest {

    static final PostgreSQLContainer<?> POSTGRES =
            new PostgreSQLContainer<>("postgres:16.4-alpine");

    static final KafkaContainer KAFKA =
            new KafkaContainer("apache/kafka:3.8.0");

    static {
        Startables.deepStart(POSTGRES, KAFKA).join();
    }

    @DynamicPropertySource
    static void props(DynamicPropertyRegistry registry) {
        registry.add("spring.datasource.url", POSTGRES::getJdbcUrl);
        registry.add("spring.datasource.username", POSTGRES::getUsername);
        registry.add("spring.datasource.password", POSTGRES::getPassword);
        registry.add("spring.kafka.bootstrap-servers", KAFKA::getBootstrapServers);
    }
}
```

`Startables.deepStart(...)` konteynerlarni **parallel** ko'taradi — PostgreSQL va Kafka ketma-ket emas, bir vaqtda start bo'ladi.

Bu naqsh Spring'ning kontekst keshi bilan birga ishlaganda haqiqiy samara beradi. Spring TestContext Framework kontekstni konfiguratsiya "kaliti" bo'yicha keshlaydi: bir xil `@SpringBootTest` atributlari, bir xil profil, bir xil `@MockitoBean` to'plami → **bitta kontekst**. Bazaviy sinfdan meros olgan barcha testlar ayni kalitni ulashadi, demak kontekst ham, konteyner ham bir marta ko'tariladi. Shuning uchun: bazaviy sinflar sonini minimal saqlang, test sinflarida qo'shimcha `@TestPropertySource` yoki ad-hoc mock qo'shib kalitni "sindirmang". `@DirtiesContext` ni esa integratsion testlarda umuman ishlatmang — u keshni tashlab, keyingi sinfga to'liq qayta start narxini yuklaydi.

### 8.5 Konteynerni qayta ishlatish (reuse)

Reuse — JVM tugaganda ham konteynerni tirik qoldirish: keyingi test ishga tushganda tayyor konteyner topiladi va start vaqti nolga yaqinlashadi. Yoqish uchun ikki shart birga kerak: konteynerda `.withReuse(true)` va developer mashinasida `~/.testcontainers.properties` faylida `testcontainers.reuse.enable=true`. Bu fayl **repoga qo'shilmaydi** — bu developer'ning shaxsiy sozlamasi.

Reuse yoqilganda Ryuk o'sha konteynerni o'chirmaydi va Testcontainers konteyner konfiguratsiyasidan hash hisoblab mavjudini topadi; konfiguratsiyani o'zgartirsangiz (image tag, env, buyruq) yangi konteyner ko'tariladi.

Muhim nozik jihat: reuse'da **ma'lumot ham saqlanadi**. Lokalda ketma-ket ishlatilgan testlar bir-birining qoldiqlarini ko'radi. Shuning uchun reuse strategiyasi albatta ishonchli tozalash bilan juftlanadi — har test uchun `@Transactional` rollback, yoki har klass oldidan `TRUNCATE ... RESTART IDENTITY CASCADE`, yoki har run uchun alohida schema. CI'da reuse **o'chirilgan** bo'lishi kerak: runner har safar yangi, hash topilmaydi, va "nopok holat" xavfini CI'ga olib kirish mantiqsiz. Natijada ikki rejim: lokal — tez va reuse'li, CI — toza va takrorlanadigan.

### 8.6 Turli texnologiyalar uchun konteynerlar

| Texnologiya | Testcontainers moduli | Konteyner sinfi | Spring'da ulash usuli |
|---|---|---|---|
| PostgreSQL | org.testcontainers:postgresql | `PostgreSQLContainer` | `@ServiceConnection` |
| MySQL / MariaDB | mysql, mariadb | `MySQLContainer`, `MariaDBContainer` | `@ServiceConnection` |
| Kafka (apache/kafka) | org.testcontainers:kafka | `org.testcontainers.kafka.KafkaContainer` | `@ServiceConnection` |
| Kafka (Confluent) | org.testcontainers:kafka | `ConfluentKafkaContainer` | `@ServiceConnection` |
| Redis | GenericContainer yoki com.redis:testcontainers-redis | `GenericContainer`, `RedisContainer` | `@ServiceConnection(name = "redis")` |
| MongoDB | org.testcontainers:mongodb | `MongoDBContainer` | `@ServiceConnection` |
| Elasticsearch | org.testcontainers:elasticsearch | `ElasticsearchContainer` | `@ServiceConnection` |
| OpenSearch | org.opensearch:opensearch-testcontainers | `OpensearchContainer` | `@DynamicPropertySource` |
| RabbitMQ | org.testcontainers:rabbitmq | `RabbitMQContainer` | `@ServiceConnection` |
| LocalStack (S3, SQS) | org.testcontainers:localstack | `LocalStackContainer` | `@DynamicPropertySource` |
| Keycloak | com.github.dasniko:testcontainers-keycloak | `KeycloakContainer` | `@DynamicPropertySource` (issuer-uri) |
| Ixtiyoriy image | org.testcontainers:testcontainers | `GenericContainer` | `@DynamicPropertySource` |

`org.testcontainers.containers.KafkaContainer` (Confluent image'ga bog'langan eski sinf) 1.20'dan boshlab deprecated; yangi kodda `org.testcontainers.kafka.KafkaContainer` (apache/kafka image, KRaft rejimi) yoki `ConfluentKafkaContainer` ishlatiladi.

LocalStack misoli — bu yerda `@ServiceConnection` yo'q, endpoint'ni o'zingiz uzatasiz:

```java
static final LocalStackContainer LOCALSTACK =
        new LocalStackContainer(DockerImageName.parse("localstack/localstack:3.8"))
                .withServices(Service.S3, Service.SQS);

@DynamicPropertySource
static void aws(DynamicPropertyRegistry registry) {
    registry.add("app.aws.endpoint", () -> LOCALSTACK.getEndpoint().toString());
    registry.add("app.aws.region", LOCALSTACK::getRegion);
    registry.add("app.aws.access-key", LOCALSTACK::getAccessKey);
    registry.add("app.aws.secret-key", LOCALSTACK::getSecretKey);
}
```

### 8.7 Spring Boot Docker Compose qo'llab-quvvatlashi va @TestConfiguration

`spring-boot-docker-compose` moduli (3.1+) — bu **dev-time** qulayligi: `compose.yaml` loyiha ildizida bo'lsa, `bootRun`/`bootTestRun` ilovani ko'targanda `docker compose up` ni o'zi bajaradi va servislarni `ConnectionDetails` sifatida ulanadi, ilova to'xtaganda `down` qiladi.

```yaml
services:
  postgres:
    image: postgres:16.4-alpine
    environment:
      POSTGRES_DB: app
      POSTGRES_USER: app
      POSTGRES_PASSWORD: app
    ports:
      - '5432'
  redis:
    image: redis:7.4-alpine
    ports:
      - '6379'
```

Farqi aniq: Docker Compose qo'llab-quvvatlashi **umumiy, uzoq yashovchi** muhit beradi (developer ilovani qo'lda ko'targanda), Testcontainers esa **test hayot aylanishiga bog'langan, izolyatsiyalangan** muhit beradi (har run uchun toza, random port, programmatik boshqaruv). Compose'ni avtomatik testlarga asos qilish xato: port fiksatsiyalangan, holat bo'linadi, CI'da fayl mavjudligiga bog'liq bo'ladi. Shuning uchun `spring.docker.compose.enabled: false` ni test profilida qo'yib, dev-time va test-time ni qat'iy ajratish tavsiya etiladi. Aksincha yo'nalish ham mumkin: Testcontainers'ni `compose.yaml` o'rniga dev rejimda ishlatish (`@TestConfiguration` + `SpringApplication.from(...).with(...)` bilan `TestMyApplication` klassi).

Konteynerlarni bean sifatida e'lon qilish — eng qayta ishlatiladigan shakl:

```java
@TestConfiguration(proxyBeanMethods = false)
public class ContainersConfig {

    @Bean
    @ServiceConnection
    PostgreSQLContainer<?> postgres() {
        return new PostgreSQLContainer<>("postgres:16.4-alpine");
    }

    @Bean
    @ServiceConnection(name = "redis")
    GenericContainer<?> redis() {
        return new GenericContainer<>("redis:7.4-alpine")
                .withExposedPorts(6379)
                .waitingFor(Wait.forLogMessage(".*Ready to accept connections.*\\n", 1));
    }
}
```

Test sinfida `@Import(ContainersConfig.class)` yetarli. Bean bo'lgani uchun konteyner hayot aylanishi Spring kontekstiga bog'lanadi, ya'ni kontekst keshida qolgan ekan konteyner ham tirik — bu singleton pattern'ning idiomatik Spring varianti. `@ServiceConnection(name = "redis")` dagi `name` — image nomi emas, **connection detail turini** aniqlash uchun ishlatiladigan xizmat nomi; `GenericContainer` bilan ishlaganda shu sababli majburiy.

### 8.8 Ma'lumotlar bazasi migratsiyasini testlash

Real bazadagi eng qimmatli test — migratsiyaning o'zi. Minimal daraja: ilova konteksti ko'tarilganda Flyway/Liquibase barcha skriptlarni real PostgreSQL'da bajaradi. Bu allaqachon H2 bermaydigan qiymat: noto'g'ri DDL, mavjud bo'lmagan extension, buzilgan checksum shu zahoti ko'rinadi.

Keyingi daraja — maqsadli migratsiya testlari:

```java
@Test
void migration_v12_backfills_legacy_rows() {
    Flyway baseline = Flyway.configure()
            .dataSource(POSTGRES.getJdbcUrl(), POSTGRES.getUsername(), POSTGRES.getPassword())
            .target(MigrationVersion.fromVersion("11"))
            .load();
    baseline.migrate();
    jdbc.update("INSERT INTO orders(id, code) VALUES (1, 'A-1')");

    Flyway upgrade = Flyway.configure()
            .dataSource(POSTGRES.getJdbcUrl(), POSTGRES.getUsername(), POSTGRES.getPassword())
            .load();
    upgrade.migrate();

    assertThat(upgrade.info().current().getVersion().getVersion()).isEqualTo("12");
    assertThat(jdbc.queryForObject("SELECT status FROM orders WHERE id = 1", String.class))
            .isEqualTo("LEGACY");
}
```

Bu test eng muhim savolga javob beradi: **yangi migratsiya eski ma'lumot bilan ishlaydimi?** Bo'sh bazada o'tgan `ALTER TABLE ... SET NOT NULL` real tarixiy NULL'lar borida yiqiladi.

Boshqa tekshiruvlar:
- **Orqaga qaytmaslik prinsipi**: `flyway.validate()` va CI'da checksum tekshiruvi — allaqachon bajarilgan skriptni tahrirlash taqiqlanadi. Flyway'da `undo` faqat Teams'da, Liquibase'da `rollback` bloki bor, lekin arxitektura qarori sifatida "forward-only migration" tavsiya etiladi: orqaga qaytarish o'rniga tuzatuvchi yangi migratsiya.
- **Zero-downtime**: expand/contract naqshi. Test N-1 versiya kodi N versiya schema'si bilan ishlashini tasdiqlaydi — eski entity mapping bilan yangi schema'ga `INSERT` qilib ko'ring. Yangi ustun `NOT NULL DEFAULT` bilan qo'shilgani, eski ustun darhol o'chirilmagani, rename o'rniga "yangi ustun + backfill + eski ustunni keyingi relizda o'chirish" ketma-ketligi bajarilgani shu testda ko'rinadi.
- **Liquibase** uchun xuddi shu yondashuv: `SpringLiquibase` bean'ini sozlab `setChangeLog(...)`, yoki `liquibase.update(new Contexts(...))` bilan ma'lum tag'gacha yugurtirib, keyin qolganini bajarish.
- **Idempotentlik**: migratsiyani ikki marta ishga tushirsangiz, ikkinchisi hech narsa qilmasligi kerak.

### 8.9 Kafka bilan integratsion test

Kafka'da mock broker (`EmbeddedKafka`) mavjud, lekin real brokerda sinaladigan narsalar boshqa: serializer/deserializer xatolari, partition assignment, consumer group rebalansi, `auto.offset.reset` semantikasi, retry/backoff va dead letter topic marshrutizatsiyasi, transactional producer.

Test dizaynining uch qoidasi. Birinchi: **consumer group'ni har test uchun unikal qiling** (`group-id: test-` + UUID) yoki topik nomini randomlashtiring — aks holda oldingi testning offset'i keyingisini "xabar yo'q" holatiga olib keladi. Ikkinchi: producer `send(...)` dan keyin **`get()` bilan metadata'ni kutib** olish — bu xabar brokerga yetganini tasdiqlaydi. Uchinchi: natijani Awaitility bilan kutish, hech qachon `Thread.sleep` bilan emas.

```java
@Test
void failed_message_lands_in_dead_letter_topic() {
    List<String> received = new CopyOnWriteArrayList<>();
    try (KafkaConsumer<String, String> dlt = newConsumer(UUID.randomUUID().toString())) {
        dlt.subscribe(List.of("orders.DLT"));

        kafkaTemplate.send("orders", "broken-payload").get(5, TimeUnit.SECONDS);

        await().atMost(Duration.ofSeconds(20))
                .pollInterval(Duration.ofMillis(250))
                .untilAsserted(() -> {
                    dlt.poll(Duration.ofMillis(200))
                       .forEach(r -> received.add(r.value()));
                    assertThat(received).isNotEmpty();
                });
    }
    assertThat(received).containsExactly("broken-payload");
}
```

DLT xatti-harakatini tasdiqlash uchun `DefaultErrorHandler` + `DeadLetterPublishingRecoverer` konfiguratsiyasini test profilida ham yoqilgan holda qoldiring va `FixedBackOff` intervalini test uchun kichraytiring (masalan `new FixedBackOff(100L, 2L)`), aks holda prod'dagi 10 sekundlik backoff testni cho'zadi. Offset'ni tekshirish kerak bo'lsa `AdminClient.listConsumerGroupOffsets(groupId)` ishlatiladi — bu consumer kommit qilganini (ya'ni xabar qayta ishlangani) deklarativ tasdiqlaydi.

### 8.10 Tezlik va resurs byudjeti

Tipik start vaqtlari (image allaqachon lokalda bo'lganda, o'rtacha developer mashinasi): PostgreSQL alpine ~1-3 s, MySQL ~5-10 s, Redis <1 s, RabbitMQ ~3-6 s, Kafka (KRaft) ~5-10 s, MongoDB ~2-4 s, LocalStack ~5-15 s, Elasticsearch/OpenSearch ~15-35 s, Keycloak ~10-20 s. Image birinchi marta pull qilinsa, ustiga 10-90 s qo'shiladi. Spring kontekstining o'zi odatda 2-6 s.

Shundan byudjet qoidasi: integratsion test to'plami lokalda 2-4 daqiqada, CI'da 10 daqiqada tugashi kerak; agar oshsa, bu arxitektura muammosi, "testlar shunchaki sekin" emas.

Optimizatsiya ro'yxati, ta'sir bo'yicha tartiblangan:
1. **Konteynerlar sonini kamaytirish**: bir baza konteyneriga ko'p schema; bir Kafka'ga ko'p topik.
2. **Kontekst keshini saqlash**: bitta `AbstractIntegrationTest`, `@DirtiesContext` yo'q, `@MockitoBean` to'plamini unifikatsiya qilish.
3. **Parallel start**: `Startables.deepStart(...)`.
4. **Yengil image**: `-alpine` variantlar, Elasticsearch o'rniga imkon bo'lsa yengil alternativ.
5. **Reuse** lokalda.
6. **Pre-pull** CI'da (keyingi bo'lim).
7. **Parallel test**: JUnit 5 `junit-platform.properties` da `junit.jupiter.execution.parallel.enabled=true` va `...mode.default=same_thread`, `...mode.classes.default=concurrent`. Port to'qnashuvi random mapping tufayli bo'lmaydi — **agar** `FixedHostPortGenericContainer` yoki `withCreateContainerCmdModifier` bilan fiksatsiyalangan port ishlatmasangiz; ularni butunlay taqiqlash kerak. Haqiqiy xavf — umumiy baza ustida parallel yozuv, shuning uchun parallel rejimda har sinfga alohida schema yoki alohida tranzaksiya izolyatsiyasi kerak.
8. **Testlarni ajratish**: `*Test` (unit, har commit'da) va `*IT` (integratsion, Maven `failsafe` yoki Gradle alohida `integrationTest` task'ida).
9. **tmpfs**: `.withTmpFs(Map.of("/var/lib/postgresql/data", "rw"))` — disk I/O ni olib tashlaydi, baza ma'lumotini saqlash kerak bo'lmagan testlarda sezilarli tezlanish.
10. **Resurs chegarasi**: Docker Desktop'ga kamida 4 CPU / 8 GB RAM; CI runner'da konteynerlar sonini xotiraga moslab cheklash.

### 8.11 Testcontainers'ni CI'da ishlatish

Yagona qattiq talab — CI agent'ida ishlaydigan Docker daemon'ga kirish. Variantlar:

**Docker socket (DooD)** — eng keng tarqalgan: agent konteyneriga `/var/run/docker.sock` mount qilinadi. Tez, lekin konteynerlar host daemon'da ko'tarilgani uchun izolyatsiya kamroq va `localhost` marshrutizatsiyasi nozik.

**Docker-in-Docker (DinD)** — `docker:dind` service konteyneri, `privileged: true` kerak. To'liq izolyatsiya, lekin har job'da image keshini qaytadan to'ldiradi (sekinlashtiradi), ba'zi platformalarda privileged taqiqlangan.

**GitHub Actions** — `ubuntu-*` runner'larda Docker allaqachon o'rnatilgan, hech qanday qo'shimcha sozlash kerak emas: `./mvnw verify` shundayin ishlaydi. `macos-*` va `windows-*` runner'larda Linux konteynerlari uchun Docker **yo'q** — bu ko'p jamoalarni kutilmagan holda urgan fakt.

**Testcontainers Cloud** — Docker daemon'ni masofaviy, boshqariladigan muhitga ko'chiradi (`DOCKER_HOST` ni agent o'rnatadi). Runner'da Docker bo'lmaganda, privileged ruxsat yo'q bo'lganda yoki parallellikni oshirish kerak bo'lganda yechim; narx va tashqi xizmatga bog'liqlik — kelishuv nuqtasi.

**Pre-pull** — eng arzon optimizatsiya: image'larni test start bo'lishidan oldin, mustaqil step'da yuklab olish. Bu pull vaqtini wait strategiya timeout'idan chiqaradi va flaky "container did not start" xatolarini kamaytiradi.

```yaml
jobs:
  integration-test:
    runs-on: ubuntu-24.04
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-java@v4
        with:
          distribution: temurin
          java-version: '21'
          cache: maven
      - name: Pre-pull container images
        run: |
          docker pull postgres:16.4-alpine
          docker pull apache/kafka:3.8.0
      - name: Run integration tests
        run: ./mvnw -B verify -Pintegration
```

Yana ikki amaliy nuqta: korporativ muhitda Docker Hub rate limit'ini chetlab o'tish uchun `testcontainers.properties` da `hub.image.name.prefix` bilan ichki registry prefiksini bering; va Ryuk'ni faqat u ishlamaydigan platformalarda (`TESTCONTAINERS_RYUK_DISABLED=true`) o'chiring — aks holda orfan konteynerlar CI agent'ini to'ldiradi.

### 8.12 Anti-patternlar

**Har test sinfida yangi konteyner.** `@Container` ni instance maydonda ishlatish yoki har sinfda alohida `PostgreSQLContainer` e'lon qilish. Natija: 40 sinf × 2 s = 80 s faqat start uchun, plus kontekst keshi buzilishi. Yechim — bitta abstract bazaviy sinf yoki `@TestConfiguration` bean'lari.

**Konteyner ichida ma'lumotni tozalamaslik.** Singleton konteyner + tozalash yo'q = testlar tartibiga bog'liq. "Lokalda o'tadi, CI'da yiqiladi" ning asosiy sababi. Yechim: `@Transactional` rollback o'qish-yozish testlari uchun, `TRUNCATE ... RESTART IDENTITY CASCADE` yoki schema-per-class aksincha holatlar uchun.

**Testlar orasida umumiy holat.** Statik `List`da yig'ilgan event'lar, umumiy Kafka consumer group, umumiy Redis kalitlari, `@MockitoBean` ustiga oldingi testdan qolgan `when(...)`. Har test o'z nomlar maydonini (topic suffix, key prefix, tenant ID) olishi kerak.

**`Thread.sleep` bilan kutish.** Asinxron natijani kutishda sleep ikki yo'l bilan yomon: sekin (har doim to'liq kutadi) va ishonchsiz (sekin CI'da yetmaydi). Awaitility `await().atMost(...).untilAsserted(...)` yagona to'g'ri javob — tez muhitda bir necha millisekundda tugaydi.

**`latest` tag.** `postgres:latest`, `confluentinc/cp-kafka:latest` — bu testlarni tashqi relizlarga bog'laydi: bir kun major versiya chiqadi va butun pipeline yiqiladi, kod o'zgarmagan holda. Har doim aniq versiyani (ideal holda digest'ni) yozing va prod versiyasiga mos qiling: prodda PostgreSQL 16 bo'lsa, testda ham 16.

Qo'shimcha ikki xato: **`FixedHostPortGenericContainer`** (parallellikni o'ldiradi) va **mapped port'ni qo'lda yozish** (`localhost:5432`). Ikkisi ham `getMappedPort()`/`@ServiceConnection` bilan almashtiriladi.

### 8.13 Arxitektor nazorat ro'yxati

- [ ] Barcha integratsion testlar real baza (Testcontainers) ustida ishlaydi; H2/in-memory baza test uchun ishlatilmaydi va `schema.sql` dublikati yo'q.
- [ ] Bitta `AbstractIntegrationTest` (yoki `@TestConfiguration` + `@ServiceConnection` bean'lari) mavjud; konteynerlar `static` va `Startables.deepStart` bilan parallel ko'tariladi.
- [ ] Spring kontekst keshi buzilmaydi: `@DirtiesContext` yo'q, test sinflarida ad-hoc property/mock qo'shilmaydi, kontekst sonlari o'lchab turiladi.
- [ ] Har bir konteyner image'i aniq versiya tag bilan yopishtirilgan (`latest` yo'q) va prod versiyasiga mos.
- [ ] Wait strategiyasi har bir custom konteyner uchun ochiq belgilangan; test kodida `Thread.sleep` yo'q, asinxron kutish faqat Awaitility bilan.
- [ ] Testlar orasidagi tozalash strategiyasi yozib qo'yilgan (rollback / TRUNCATE / schema-per-class) va reuse yoqilgan lokal muhitda ham ishlaydi.
- [ ] Migratsiya testlari bor: to'liq Flyway/Liquibase ishga tushishi, eski ma'lumot bilan yangi migratsiya, forward-only va zero-downtime (expand/contract) tekshiruvi.
- [ ] CI'da Docker mavjudligi tasdiqlangan, image'lar pre-pull qilinadi, reuse o'chirilgan va integratsion test to'plami kelishilgan vaqt byudjetidan oshmaydi.

---

## 9. Tashqi servislarni taqlid qilish va contract testing (Faking External Services & Contract Testing)

Mikroservisda kodning katta qismi o'z bazasi bilan emas, boshqa servislar bilan gaplashadi: to'lov gateway, KYC provayderi, ichki buyurtma yoki hisob servisi. Shu integratsiyalarni qanday testlash — arxitektura qarori: u build vaqtini, test barqarorligini va integratsiya nosozligini qancha erta ushlashni belgilaydi. Bu bobda stub vositalaridan (WireMock, MockRestServiceServer) boshlab, stub drift orqali contract testing'ga (Spring Cloud Contract, Pact) va schema evolution nazoratiga o'tamiz.

### 9.1 Muammo va yechim variantlari ierarxiyasi

Integratsion testda haqiqiy tashqi servisga murojaat qilish bir vaqtda to'rt xil narx to'laydi. Tezlik: har bir so'rov tarmoq orqali ketadi va suite minutlarga cho'ziladi. Barqarorlik: vendor sandbox'i tushsa yoki rate limit bersa, build qizil bo'ladi va jamoa "qayta ishga tushir" madaniyatiga o'tadi. Nazorat: 503, read timeout, buzilgan JSON kabi holatlarni buyurtma bilan chaqirib bo'lmaydi, aslida eng ko'p incident shu yo'llardan keladi. Narx: har bir chaqiruv tariflanishi mumkin.

Shuning uchun integratsiya nuqtasini testlashda bir necha qatlamni bosqichma-bosqich qo'llash kerak:

1. **Mock (unit daraja)** — client interfeysini Mockito bilan almashtirish. Eng tez, lekin HTTP, serializatsiya va xato mapping'ini tekshirmaydi; faqat biznes logikani client'dan ajratish uchun.
2. **In-process stub (`MockRestServiceServer`)** — socket ochilmaydi, lekin URL, header, body serializatsiyasi va javob deserializatsiyasi tekshiriladi. Client sinfining o'zini testlash uchun ideal.
3. **Out-of-process stub server (WireMock, MockServer, Hoverfly)** — haqiqiy TCP port, haqiqiy HTTP client stack: connection pool, timeout, retry, TLS. Kechikish va tarmoq xatolarini simulyatsiya qilish mumkin.
4. **Contract test** — stub endi qo'lda yozilmaydi, provider tomonidan verifikatsiya qilingan contract'dan generatsiya qilinadi. Stub drift'ni ushlaydigan yagona qatlam.
5. **Vendor sandbox** — kunda bir marta, alohida pipeline'da, release gate emas: vendor bilan haqiqiy muvofiqlikni tekshirish uchun.
6. **Real servis** — faqat production'dagi synthetic monitoring va smoke sifatida, PR build'ida emas.

Arxitektorning asosiy qarori shu: 2 va 3 qatlam "mening kodim to'g'ri ishlaydi" ishonchini beradi, 4-qatlam esa "mening kutganim provayderning haqiqatiga mos" deganini. Bu ikki xil savol.

### 9.2 WireMock bilan HTTP stub server

WireMock 3.x — JVM dunyosida eng keng tarqalgan HTTP stub server. Ikki rejimi bor: standalone jar (`java -jar wiremock-standalone-3.x.jar --port 8089`, mapping'lar `mappings/` papkasidan o'qiladi — lokal development va QA muhiti uchun) va test ichidagi JUnit 5 extension. Testda `@RegisterExtension` bilan `WireMockExtension` tavsiya etiladi: har bir testdan keyin stub'larni reset qiladi, `dynamicPort()` esa parallel build'da port konfliktini yo'qotadi.

Spring Boot bilan ulashning to'g'ri usuli — base URL'ni property orqali berib, testda `@DynamicPropertySource` bilan WireMock port'iga yo'naltirish. Shunda production kodida test-aware shart qolmaydi.

```java
@SpringBootTest
class PaymentClientWireMockTest {

    @RegisterExtension
    static WireMockExtension wm = WireMockExtension.newInstance()
            .options(wireMockConfig().dynamicPort())
            .failOnUnmatchedRequests(true)
            .build();

    @DynamicPropertySource
    static void props(DynamicPropertyRegistry registry) {
        registry.add("payment.base-url", wm::baseUrl);
    }

    @Autowired PaymentClient client;

    @Test
    void chargeIsAuthorized() {
        wm.stubFor(post(urlPathEqualTo("/v1/charges"))
                .withHeader("Content-Type", containing("application/json"))
                .withRequestBody(matchingJsonPath("$.amount", equalTo("1000")))
                .willReturn(okJson("{\"id\":\"ch_1\",\"status\":\"AUTHORIZED\"}")));

        assertThat(client.charge(new ChargeRequest("ord-1", 1000)).status())
                .isEqualTo("AUTHORIZED");
        wm.verify(1, postRequestedFor(urlPathEqualTo("/v1/charges")));
    }
}
```

WireMock'ning asl qiymati happy path emas, yomon yo'llarni arzon simulyatsiya qilishda. `withFixedDelay(ms)` client'ning read timeout sozlamasini tekshiradi, `withChunkedDribbleDelay` javobni bo'lib yuboradi, `withFault(...)` connection reset chaqiradi. `inScenario(...)` stateful stub yaratadi: birinchi chaqiruvda 503, ikkinchisida 200 — retry va circuit breaker siyosati uchun zarur.

```java
@Test
void retriesAfterTransientFailure() {
    wm.stubFor(get(urlPathEqualTo("/v1/rates")).inScenario("flaky")
            .whenScenarioStateIs(Scenario.STARTED)
            .willReturn(aResponse().withStatus(503).withFixedDelay(200))
            .willSetStateTo("recovered"));

    wm.stubFor(get(urlPathEqualTo("/v1/rates")).inScenario("flaky")
            .whenScenarioStateIs("recovered")
            .willReturn(okJson("{\"usd\":12650}")));

    assertThat(client.rate("usd")).isEqualTo(12650);
    wm.verify(2, getRequestedFor(urlPathEqualTo("/v1/rates")));
}

@Test
void connectionResetBecomesDomainException() {
    wm.stubFor(get(urlPathEqualTo("/v1/rates"))
            .willReturn(aResponse().withFault(Fault.CONNECTION_RESET_BY_PEER)));

    assertThatThrownBy(() -> client.rate("usd"))
            .isInstanceOf(RateUnavailableException.class);
}
```

Amaliy qoidalar: `failOnUnmatchedRequests(true)` yoqilgan bo'lsin, aks holda noto'g'ri URL jim o'tib ketadi; `verify(...)` bilan yuborilgan so'rovni ham tasdiqlang (idempotency key, correlation va auth header ketdimi); umumiy `mappings/` papkasi vaqt o'tib hech kim tushunmaydigan global holatga aylanadi.

### 9.3 MockServer va Hoverfly: qachon qaysi biri

MockServer (`org.mock-server:mockserver-junit-jupiter`) WireMock'ga funksional jihatdan yaqin; kuchli tomoni — expectation/verification DSL'i va forward proxy rejimi: trafikni o'tkazib yuborib bir qismini ushlab qolish mumkin. Hoverfly (`io.specto:hoverfly-java`) boshqa falsafada: capture mode'da real trafikni yozib oladi, simulate mode'da qaytaradi, latency va xato injection'ni (chaos) qulay beradi — hujjatlashtirilmagan legacy servis bilan eng tez natija beradi.

Default tanlov — WireMock: eng katta ecosystem va Spring Cloud Contract ham stub'larni WireMock orqali serve qiladi, ya'ni contract testing'ga o'tish uzluksiz bo'ladi. MockServer'ni proxy va ko'p protokolli ehtiyoj paydo bo'lganda, Hoverfly'ni record-and-replay asosiy rejim bo'lganda qo'shing.

### 9.4 MockRestServiceServer bilan client'ni testlash

Agar maqsad client sinfining o'zi bo'lsa — URL qurish, header, DTO serializatsiyasi, xato status'ni domen exception'ga aylantirish — socket ochish shart emas. `MockRestServiceServer` `RestTemplate` va `RestClient` uchun in-process stub beradi, `@RestClientTest` uni avtomatik sozlaydi: eng tez variant.

```java
@RestClientTest(value = PaymentClient.class,
        properties = "payment.base-url=https://payments.test")
class PaymentClientSliceTest {

    @Autowired MockRestServiceServer server;
    @Autowired PaymentClient client;

    @Test
    void mapsResponseBodyToDto() {
        server.expect(once(), requestTo("https://payments.test/v1/charges"))
                .andExpect(method(HttpMethod.POST))
                .andExpect(jsonPath("$.orderId").value("ord-1"))
                .andRespond(withSuccess("{\"id\":\"ch_1\",\"status\":\"AUTHORIZED\"}",
                        MediaType.APPLICATION_JSON));

        assertThat(client.charge(new ChargeRequest("ord-1", 1000)).id())
                .isEqualTo("ch_1");
        server.verify();
    }

    @Test
    void mapsServerErrorToDomainException() {
        server.expect(requestTo("https://payments.test/v1/charges"))
                .andRespond(withServerError());
        assertThatThrownBy(() -> client.charge(new ChargeRequest("ord-1", 1000)))
                .isInstanceOf(PaymentGatewayException.class);
    }
}
```

Cheklovi: haqiqiy HTTP stack chetlab o'tiladi, demak connection timeout, TLS, redirect, connection pool tugashi ko'rinmaydi. Reactive `WebClient` uchun u ishlamaydi — WireMock yoki `ExchangeFunction` almashtirish kerak. Taqsimot: client sinfi uchun `@RestClientTest`, resilience siyosati uchun WireMock.

### 9.5 Record and replay: foydasi va xavfi

Stub'ni qo'lda yozish qimmat bo'lganda javobni real servisdan yozib olish mumkin: WireMock'da `--proxy-all="https://api.vendor.com" --record-mappings` rejimi yoki `/__admin/recorder` admin API, Hoverfly'da capture mode. Foydasi — real, to'liq payload'lar, chunki qo'lda yozilgan stub provayder javobidan soddalashtirilgan bo'ladi va bug aynan shu soddalashtirish ichida yashiringan bo'ladi.

Xavfi: fayllarda token, karta raqami, shaxsiy ma'lumot qolib ketadi va repo'ga tushadi; fixture'lar keraksiz maydonlar bilan o'sadi; eng muhimi — stub yozilgan kundan boshlab eskiradi, lekin test yashil turadi. Qoidalar: maxfiy maydonlarni avtomatik tozalash, faqat ishlatiladigan maydonlarni qoldirish, fixture yoniga sana va provider API versiyasini yozish, rejali qayta yozib olish. Record-and-replay — boshlash vositasi, strategiya emas.

### 9.6 Stub drift muammosi

Stub drift — integratsion testlashning markaziy nosozligi. Provider `status` maydonini `state` ga o'zgartiradi, `201` o'rniga `200` qaytaradi, xato formatini RFC 7807 `problem+json` ga ko'chiradi yoki enum'ga yangi qiymat qo'shadi. Consumer tomonidagi stub buni bilmaydi: eski shaklni qaytaradi, testlar yashil, deploy o'tadi, production'da esa deserializatsiya sinadi. Ko'proq stub yozish muammoni yomonlashtiradi — har bir yangi stub provider haqida yana bir tasdiqlanmagan taxmin.

Sabab arxitektura darajasida: stub consumer repo'sida yashaydi, haqiqat esa provider repo'sida o'zgaradi va ikkisi o'rtasida avtomatik bog'lanish yo'q. Nightly sandbox smoke bu bog'lanishni kech va noaniq signal bilan beradi. To'g'ri yechim — stub'ni tasdiqlangan contract'dan olish: provider contract'ni buzsa, provider'ning o'z build'i qizil bo'ladi. Aynan shu contract testing'ning mavjudlik sababi.

### 9.7 Contract testing nazariyasi

Consumer-driven contract'da consumer o'z kutganini misollar ko'rinishida yozadi: shu so'rovga shu shakldagi javob kerak. Bu misollar mashina o'qiydigan, versiyalangan artefaktga aylanadi. Provider tomonda verification bo'ladi: provider haqiqiy implementatsiyasini ko'tarib, har bir interaction'ni qayta o'ynaydi va javob kutilgan shaklga mosligini tekshiradi. Broker (Pact Broker/PactFlow, SCC holatida Maven repository) o'rtada turadi: contract, versiya, muhit holati va verification natijalarini saqlaydi.

Integratsion testdan farqi: integratsion test ikki real tizimni bir muhitda, bir vaqtda ishlatishni talab qiladi va "hozir ishladi" deydi. Contract test juftlik muvofiqligini mustaqil tekshiradi — ikki servis bir vaqtda ishlashi shart emas, shuning uchun tez va deterministik. Narxi: u provider biznes logikasini tekshirmaydi, faqat kelishilgan interaction shakli va semantikasini. Ya'ni contract test E2E'ni emas, stub'larni almashtiradi.

### 9.8 Spring Cloud Contract: buyurtma va to'lov servisi

Ish oqimi: contract DSL (Groovy yoki YAML) provider repo'sida `src/test/resources/contracts/` ostida yashaydi va odatda consumer tomonidan pull request sifatida qo'shiladi. `spring-cloud-contract-maven-plugin` undan provider testlarini generatsiya qiladi (`MockMvc`, `WebTestClient` yoki `EXPLICIT` rejim), ular `verify` fazasida ishlaydi. Testlar o'tgach plugin `payment-service-1.4.0-stubs.jar` artefaktini Nexus/Artifactory'ga joylaydi.

```groovy
import org.springframework.cloud.contract.spec.Contract

Contract.make {
    description "1000 tiyinlik to'lov avtorizatsiya qilinadi"
    request {
        method POST()
        url "/v1/charges"
        headers { contentType applicationJson() }
        body(orderId: "ord-1", amount: 1000)
        bodyMatchers {
            jsonPath('$.orderId', byRegex('[a-z0-9\\-]+'))
            jsonPath('$.amount', byRegex(number()))
        }
    }
    response {
        status OK()
        headers { contentType applicationJson() }
        body(id: "ch_1", status: "AUTHORIZED")
        bodyMatchers {
            jsonPath('$.id', byRegex('ch_[a-z0-9]+'))
            jsonPath('$.status', byRegex('AUTHORIZED|DECLINED'))
        }
    }
}
```

YAML variantini Groovy bilmagan jamoalar afzal ko'radi va u xuddi shu imkoniyatlarni beradi:

```yaml
description: "limitdan oshgan to'lov DECLINED bo'ladi"
request:
  method: POST
  url: /v1/charges
  headers:
    Content-Type: application/json
  body:
    orderId: ord-2
    amount: 5000000
  matchers:
    body:
      - path: $.amount
        type: by_regex
        predefined: number
response:
  status: 200
  headers:
    Content-Type: application/json
  body:
    id: ch_2
    status: DECLINED
```

Generatsiya qilingan testlar base class'dan meros oladi — unda application ishga tushadi va tashqi bog'liqliklar (DB, downstream) boshqariladi:

```java
@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT)
public abstract class PaymentContractBase {

    @LocalServerPort int port;
    @MockitoBean ChargeService chargeService;

    @BeforeEach
    void setUp() {
        RestAssured.port = port;
        given(chargeService.charge(argThat(r -> r.amount() <= 1_000_000)))
                .willReturn(new Charge("ch_1", ChargeStatus.AUTHORIZED));
        given(chargeService.charge(argThat(r -> r.amount() > 1_000_000)))
                .willReturn(new Charge("ch_2", ChargeStatus.DECLINED));
    }
}
```

Consumer (order-service) tomonda esa stub runner shu jar'ni Maven repository'dan yuklab, WireMock'da ko'taradi. Qo'lda yozilgan stub umuman qolmaydi:

```java
@SpringBootTest
@AutoConfigureStubRunner(
        ids = "com.example:payment-service:+:stubs:8090",
        stubsMode = StubRunnerProperties.StubsMode.REMOTE,
        repositoryRoot = "https://nexus.internal/repository/maven-releases")
class OrderServiceContractTest {

    @Autowired OrderService orderService;

    @Test
    void orderIsPaidUsingRealProviderContract() {
        var order = orderService.place(new PlaceOrder("ord-1", 1000));
        assertThat(order.status()).isEqualTo(OrderStatus.PAID);
    }
}
```

Muhim nuqta: `ids` ichidagi `+` eng yangi versiyani oladi; production'da aniq versiya yoki oraliq ko'rsating, aks holda consumer build'i provider release'i bilan tasodifiy sinadi.

### 9.9 Pact: consumer test, broker, can-i-deploy

Pact JVM'da contract consumer testining yon mahsuloti: test Pact mock server'ga qarshi ishlaydi va `target/pacts/order-service-payment-service.json` fayli yoziladi.

```java
@ExtendWith(PactConsumerTestExt.class)
@PactTestFor(providerName = "payment-service", pactVersion = PactSpecVersion.V3)
class PaymentPactConsumerTest {

    @Pact(consumer = "order-service")
    public RequestResponsePact authorizedCharge(PactDslWithProvider builder) {
        return builder.given("merchant has sufficient limit")
                .uponReceiving("a charge request")
                .path("/v1/charges").method("POST")
                .body(new PactDslJsonBody()
                        .stringType("orderId", "ord-1")
                        .numberType("amount", 1000))
                .willRespondWith().status(200)
                .body(new PactDslJsonBody()
                        .stringMatcher("id", "ch_[a-z0-9]+", "ch_1")
                        .stringValue("status", "AUTHORIZED"))
                .toPact();
    }

    @Test
    @PactTestFor(pactMethod = "authorizedCharge")
    void chargeIsAuthorized(MockServer mockServer) {
        var client = new PaymentClient(RestClient.create(mockServer.getUrl()));
        assertThat(client.charge(new ChargeRequest("ord-1", 1000)).status())
                .isEqualTo("AUTHORIZED");
    }
}
```

Pact fayli broker'ga `pact:publish` bilan yuboriladi, provider uni broker'dan olib o'z implementatsiyasiga qarshi tekshiradi. `given(...)` matni provider tomonda `@State` metodiga bog'lanadi — test ma'lumotlarini kerakli holatga keltirish nuqtasi.

```java
@Provider("payment-service")
@PactBroker(url = "https://pact-broker.internal")
@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT)
class PaymentPactProviderTest {

    @LocalServerPort int port;

    @BeforeEach
    void target(PactVerificationContext context) {
        context.setTarget(new HttpTestTarget("localhost", port));
    }

    @TestTemplate
    @ExtendWith(PactVerificationSpringProvider.class)
    void verifyContracts(PactVerificationContext context) {
        context.verifyInteraction();
    }

    @State("merchant has sufficient limit")
    void merchantHasSufficientLimit() {
        merchantRepository.save(new Merchant("m-1", 10_000_000L));
    }
}
```

| Mezon | Spring Cloud Contract | Pact (Pact JVM) |
| --- | --- | --- |
| Contract manbasi | Alohida DSL fayl (provider repo'sida, consumer PR qiladi) | Consumer testining yon mahsuloti |
| Format | Groovy yoki YAML DSL, Java DSL | Pact JSON spetsifikatsiyasi (V3/V4) |
| Stub tarqatish | `*-stubs.jar` Maven/Nexus orqali, WireMock serve qiladi | Broker'dan pact, mock server test ichida |
| Markaziy registry | Maven repository (versiyalash bor, muhit holati yo'q) | Pact Broker/PactFlow: matritsa, tag, environment |
| Deploy gate | Yo'q (build va versiya tartibi bilan qo'lda) | `can-i-deploy` CLI — tayyor gate |
| Polyglot | JVM-markazli (boshqa tillar uchun cheklangan) | Kuchli: JS, .NET, Go, Python, Ruby |
| Messaging | Qo'llab-quvvatlanadi (Kafka, AMQP, Spring Cloud Stream) | Qo'llab-quvvatlanadi (async message pact) |
| Spring integratsiyasi | Juda chuqur, Boot bilan tabiiy | Yaxshi (`pact-jvm-provider-spring`), lekin tashqi |
| Kirish narxi | Spring jamoasi uchun past | O'rta: broker infrastrukturasi kerak |
| Eng mos holat | Faqat JVM, bir xil CI, stub'ni ham qayta ishlatish kerak | Ko'p tilli landshaft, qat'iy deploy gate kerak |

Tanlov mezoni: barcha servislar JVM va bitta Maven infrastrukturasida bo'lsa Spring Cloud Contract kamroq qo'shimcha tizim talab qiladi va stub'larni bonus beradi. Frontend, Go yoki Python consumer'lar bo'lsa va deploy avtomatik gate bilan to'xtatilishi kerak bo'lsa, Pact Broker'ning `can-i-deploy` va deployment matritsasi raqobatsiz.

### 9.10 Messaging contract va schema evolution

Asinxron integratsiyada drift yanada jim kechadi: producer message shaklini o'zgartiradi, consumer deserializatsiya xatosi bilan DLQ'ni to'ldiradi. Spring Cloud Contract messaging contract'ni `input`/`outputMessage` juftligi bilan ifodalaydi: provider testi `triggeredBy` metodini chaqirib chiqqan xabarni tekshiradi, consumer tomonda `StubTrigger` bean'i `trigger("order_created")` bilan listener'ga real shakldagi xabarni yuboradi.

```groovy
import org.springframework.cloud.contract.spec.Contract

Contract.make {
    label "order_created"
    input {
        triggeredBy("publishOrderCreated()")
    }
    outputMessage {
        sentTo "orders.created"
        headers { messagingContentType(applicationJson()) }
        body([orderId: "ord-1", amount: 1000, status: "CREATED"])
        bodyMatchers {
            jsonPath('$.orderId', byRegex('ord-[0-9]+'))
            jsonPath('$.amount', byRegex(number()))
        }
    }
}
```

Avro yoki Protobuf ishlatilsa, ikkinchi himoya qatlami — schema registry. Confluent Schema Registry terminologiyasida BACKWARD compatibility yangi schema eski ma'lumotni o'qiy olishini bildiradi (consumer birinchi yangilanadi), FORWARD esa yangi schema bilan yozilgan ma'lumotni eski schema o'qiy olishini (producer birinchi yangilanadi), FULL ikkisini birga talab qiladi, `_TRANSITIVE` variantlari esa faqat oldingi emas, barcha tarixiy versiyalarga nisbatan tekshiradi. CI'da `kafka-schema-registry-maven-plugin`ning `test-compatibility` goal'i yoki Protobuf uchun breaking-change linter'i schema o'zgarishini merge'dan oldin to'xtatadi.

Ogohlantirish: schema compatibility semantik contract emas. `status` maydoniga yangi enum qiymati qo'shilishi Avro uchun mos, lekin consumer'dagi `switch` uchun halokat. Shuning uchun schema registry va messaging contract test bir-birini almashtirmaydi: biri strukturani, ikkinchisi kelishilgan ma'noni himoya qiladi.

### 9.11 OpenAPI'ni contract sifatida ishlatish

Agar provider spec-first ishlasa, OpenAPI fayli tabiiy contract bo'lib xizmat qiladi. Birinchi foydalanish — `openapi-generator-maven-plugin` bilan consumer uchun client generatsiya qilish: spec o'zgarsa, consumer kodi kompilyatsiya bosqichida sinadi, ya'ni signal eng arzon joyda keladi. Ikkinchisi — provider javoblarini spec'ga qarshi validatsiya qilish, buning uchun `swagger-request-validator` kutubxonasi ishlatiladi.

```java
@WebMvcTest(OrderController.class)
class OrderApiSpecComplianceTest {

    @Autowired MockMvc mockMvc;
    @MockitoBean OrderService orderService;

    @Test
    void responseConformsToOpenApiSpec() throws Exception {
        given(orderService.find("ord-1"))
                .willReturn(new OrderView("ord-1", "CREATED", 1000));

        mockMvc.perform(get("/v1/orders/{id}", "ord-1"))
                .andExpect(status().isOk())
                .andExpect(openApi().isValid("openapi/orders-v1.yaml"));
    }
}
```

Uchinchisi — CI'da spec diff'ini breaking change sifatida ushlash: `oasdiff`/`openapi-diff` maydon olib tashlanganini, required qo'shilganini, status kod o'zgarganini aniqlaydi va pipeline'ni to'xtatadi. Cheklovi: OpenAPI provider-driven, ya'ni provider nima qila olishini aytadi, lekin qaysi consumer qaysi maydonga tayanganini bilmaydi. Shuning uchun OpenAPI — keng qamrov, consumer-driven contract — kritik juftliklar uchun.

### 9.12 Contract testni CI'ga qo'yish

Pipeline javobgarligi aniq taqsimlanadi. Consumer build'i contract'ni (yoki pact'ni) yaratadi va broker'ga consumer versiyasi va branch bilan publish qiladi. Provider build'i har commit'da aktual consumer contract'larini verifikatsiya qilib natijani broker'ga qaytaradi; bundan tashqari broker webhook'i yangi contract paydo bo'lganda verification'ni alohida ishga tushiradi — consumer kutganini o'zgartirsa, provider darhol biladi. Deploy oldidan gate `can-i-deploy` bilan qo'yiladi.

```yaml
jobs:
  verify-contracts:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: ./mvnw -B verify -Ppact-provider
        env:
          PACT_BROKER_BASE_URL: ${{ secrets.PACT_BROKER_URL }}
          PACT_BROKER_TOKEN: ${{ secrets.PACT_BROKER_TOKEN }}
          PACT_PROVIDER_VERSION: ${{ github.sha }}
          PACT_PUBLISH_RESULTS: "true"
  can-i-deploy:
    needs: verify-contracts
    runs-on: ubuntu-latest
    steps:
      - run: |
          pact-broker can-i-deploy \
            --pacticipant payment-service \
            --version ${{ github.sha }} \
            --to-environment production \
            --retry-while-unknown 6
```

Provider consumer contract'ini buzsa, provider build'i qizil bo'ladi — bu nosozlik emas, tizimning maqsadi. Hali release qilinmagan kutganlar provider jamoasini bloklamasligi uchun Pact'da pending va WIP pacts bor: yangi contract avval ogohlantiradi, release'dan keyin qattiq gate'ga aylanadi. Deploy tartibi: additive o'zgarishda provider birinchi deploy qilinadi, maydon olib tashlanganda esa avval barcha consumer'lar undan voz kechadi — expand-and-contract (parallel change) usuli. Contract'larni consumer versiyasi va branch bo'yicha versiyalash, muhitlarni tag qilish bu tartibni kuzatiladigan qiladi.

### 9.13 Anti-patternlar

Provider contract'ni o'zi yozib qo'yishi — eng ko'p uchraydigan nosozlik: contract implementatsiyaning ko'zgusiga aylanadi va yangi signal bermaydi, provider o'zini o'zi tasdiqlaydi. Contract manbasi consumer bo'lishi kerak, hatto provider repo'siga pull request sifatida kelsa ham.

Stub'ni qo'lda yangilash: provider o'zgargani haqida Slack'dan bilib, consumer repo'sidagi JSON faylni tahrirlash — contract testing emas, drift'ni qo'lda kuzatish.

Contract testni E2E bilan almashtirish yoki teskarisi. E2E butun oqimni kech va beqaror tekshiradi, contract test juftlik muvofiqligini erta va deterministik; ular turli xavflarni yopadi.

Har bir integratsiyani real servisga urib testlash: suite sekin va flaky bo'ladi, vendor rate limit'iga tiqiladi va oxirida testlar `@Disabled` bo'ladi.

Contract'da hamma narsani aniq qiymat bilan qotirish. Timestamp, UUID, hisoblangan maydonlarni exact match qilish contract'ni mo'rt qiladi — matcher (regex, type) ishlatish kerak.

Verification natijasini e'tiborsiz qoldirish: qizil provider verification'ini `@Disabled` yoki doimiy pending flag bilan yashirish contract testing'ni dekoratsiyaga aylantiradi.

### 9.14 Arxitektor nazorat ro'yxati

- [ ] Har bir tashqi integratsiya uchun qaysi qatlam ishlatilayotgani (mock, in-process stub, WireMock, contract test, sandbox) ro'yxatlangan va asoslangan.
- [ ] Barcha stub server port'lari dinamik va Spring'ga `@DynamicPropertySource` orqali beriladi; test kodida qotirilgan port yo'q.
- [ ] Faqat happy path emas: har bir kritik client uchun timeout, 5xx, buzilgan javob va retry stsenariylari WireMock bilan qoplangan.
- [ ] Kritik servis juftliklari uchun consumer-driven contract bor va stub qo'lda yozilmaydi, balki tasdiqlangan contract'dan generatsiya qilinadi.
- [ ] Provider pipeline'i har commit'da va broker webhook'ida consumer contract'larini verifikatsiya qiladi, natija broker'ga publish qilinadi.
- [ ] Deploy oldidan gate mavjud (`can-i-deploy` yoki stub versiyasi va provider verification tartibi) va u qo'lda chetlab o'tilmaydi.
- [ ] Kafka/AMQP integratsiyalari uchun messaging contract va schema registry compatibility tekshiruvi (BACKWARD/FORWARD siyosati tanlangan) CI'da ishlaydi.
- [ ] Record-and-replay fixture'lari maxfiy ma'lumotdan tozalangan, sanasi belgilangan va qayta yozib olish jadvali bor.

---

## 10. Test ma'lumotlarini boshqarish (Managing Test Data)

Test ma'lumoti — testning eng kam qadrlanadigan, ammo eng ko'p muammo keltiradigan qismi. Amalda test suite'ning o'qilishi, barqarorligi va ishlash tezligi ko'p hollarda business logic'dan emas, balki ma'lumotni tayyorlash usulidan kelib chiqadi. Bu bobda fixture strategiyalari, Test Data Builder va Object Mother patternlari, ma'lumotlar bazasi holatini boshqarish, izolyatsiya usullari va test ma'lumoti bilan ishlashdagi tipik anti-patternlar ko'rib chiqiladi. Maqsad — arxitektor sifatida loyihada test ma'lumoti bo'yicha bitta ongli, hujjatlashtirilgan qaror qabul qilish va uni butun komanda bo'ylab bir xil qo'llash.

### 10.1 Test ma'lumoti nega alohida mavzu

Odatda testda uch qism bo'ladi: arrange, act, assert. Katta tizimlarda `act` bir qator, `assert` ikki-uch qator, `arrange` esa qirq qator bo'lib ketadi. Shu qirq qator testning ma'nosini yashiradi: o'quvchi `new Customer(...)` konstruktorining 12 argumenti orasidan qaysi biri aynan shu test uchun muhim ekanini topa olmaydi. Bu "Obscure Test" muammosi — test hujjat sifatida ishlamay qoladi.

Ikkinchi ta'sir — beqarorlik. Umumiy ma'lumotga tayangan testlar bir-birining holatini buzadi: test A yaratilgan mijozni test B o'chiradi, natijada parallel yoki boshqa tartibda ishga tushirilganda suite qizil bo'ladi. Bu sabab ko'pincha "flaky test" deb nomlanadi, lekin aslida bu izolyatsiya xatosi — deterministik va tuzatiladigan.

Uchinchi ta'sir — tezlik. 500 ta integration testning har biri 300 ms ma'lumot tayyorlashga ketsa, bu 2.5 daqiqa faqat `arrange` uchun. Ma'lumotni qanday yaratish (SQL insert, repository, HTTP API orqali) va qachon tozalash — CI quvurining umumiy vaqtiga to'g'ridan-to'g'ri ta'sir qiladi.

To'rtinchisi — ishonchlilik. Ma'lumot hayotiy bo'lmasa (bo'sh string'lar, `null` maydonlar, `BigDecimal.ZERO` narxlar), test o'tadi, production'da esa validatsiya yoki hisob-kitob buziladi. Shuning uchun default qiymatlar "valid va mazmunli" bo'lishi kerak.

### 10.2 Fixture strategiyalari

Fixture — test boshlanishidagi tizim holati. Gerard Meszaros klassifikatsiyasi bo'yicha to'rtta asosiy yondashuv bor.

**Fresh Fixture** — har test o'zining ma'lumotini noldan yaratadi va o'zi tozalaydi. Eng izolyatsiyalangan, eng sekin.

**Shared Fixture** — bir marta yaratilgan ma'lumot to'plamini barcha testlar baham ko'radi (`@BeforeAll`, bir marta to'ldirilgan baza). Tez, lekin testlar o'zaro bog'lanadi.

**Prebuilt Fixture** — ma'lumot test ishga tushishidan oldin tashqaridan tayyorlanadi (migration, dump, seed skript). Shared Fixture'ning maxsus holati.

**Immutable Shared Fixture** — baham ko'rilgan, lekin hech bir test o'zgartirmaydigan reference ma'lumot: valyuta kodlari, soliq stavkalari, mamlakatlar ro'yxati. Amalda eng foydali kelishuv.

| Strategiya | Tezlik | Izolyatsiya | Asosiy xavf | Qachon |
|---|---|---|---|---|
| Fresh Fixture | Past | Juda yuqori | CI vaqti o'sadi | Standart tanlov; business holatga tegadigan testlar |
| Shared Fixture | Yuqori | Past | Test interdependence, tartibga bog'liqlik | Faqat read-only scenario'lar |
| Prebuilt Fixture | Yuqori | O'rtacha | Dump eskiradi, kim o'zgartirgani noma'lum | Reference/lookup jadvallar |
| Immutable Shared | Yuqori | Yuqori (o'zgarmasa) | Kimdir yozib yuborsa jim buziladi | Valyuta, soliq, konfiguratsiya kataloglari |

Tavsiya: **o'zgaradigan (mutable) business ma'lumot uchun Fresh Fixture, o'zgarmaydigan reference ma'lumot uchun Immutable Shared Fixture (Flyway migration orqali)**. Shared mutable fixture'ni loyiha konvensiyasi darajasida taqiqlash kerak — bu eng ko'p yashirin nosozlik manbasi.

### 10.3 Test Data Builder pattern

Builder'ning maqsadi: testda **faqat shu test uchun ahamiyatli maydonni** ko'rsatish, qolganiga valid default berish.

```java
public final class CustomerTestBuilder {
    private String name = "Alisher Qodirov";
    private String email = "alisher@example.com";
    private CustomerTier tier = CustomerTier.STANDARD;
    private boolean blocked = false;

    public static CustomerTestBuilder aCustomer() {
        return new CustomerTestBuilder();
    }

    public CustomerTestBuilder vip() {
        this.tier = CustomerTier.VIP;
        return this;
    }

    public CustomerTestBuilder blocked() {
        this.blocked = true;
        return this;
    }
    public CustomerTestBuilder withEmail(String email) {
        this.email = email;
        return this;
    }

    public Customer build() {
        return new Customer(name, email, tier, blocked);
    }
}
```

Buyurtma builder'i boshqa builder'ni qabul qiladi — bu "nested builder" yondashuvi, obyekt grafigini qurishni soddalashtiradi.

```java
public final class OrderTestBuilder {
    private Customer customer = aCustomer().build();
    private final List<OrderLine> lines = new ArrayList<>();
    private OrderStatus status = OrderStatus.NEW;

    public static OrderTestBuilder anOrder() {
        return new OrderTestBuilder();
    }

    public OrderTestBuilder for_(CustomerTestBuilder c) {
        this.customer = c.build();
        return this;
    }
    public OrderTestBuilder withLine(String sku, int qty, String price) {
        lines.add(new OrderLine(sku, qty, new BigDecimal(price)));
        return this;
    }
    public OrderTestBuilder paid() {
        this.status = OrderStatus.PAID;
        return this;
    }
    public Order build() {
        if (lines.isEmpty()) {
            withLine("SKU-1", 1, "100.00");
        }
        return new Order(customer, List.copyOf(lines), status);
    }
}
```

Testda o'qilishi shunday bo'ladi:

```java
@Test
void vipMijozgaChegirmaQollanadi() {
    Order order = anOrder()
            .for_(aCustomer().vip())
            .withLine("SKU-9", 2, "250.00")
            .build();

    Money total = discountService.applyDiscount(order);

    assertThat(total).isEqualTo(Money.of("450.00"));
}
```

`vip()` — testning yagona muhim fakti, qolgani default. Buyurtmaning manzili, telefon raqami, yaratilgan sanasi testda ko'rinmaydi, lekin ular valid.

**Lombok `@Builder` bilan farqi.** Lombok builder — production obyektini qurish uchun mexanik vosita: barcha maydonga setter'ga o'xshash method generatsiya qiladi, lekin default qiymat bermaydi (`@Builder.Default` yozmasa `null` va `0` qoladi) va domen tilidagi `vip()`, `blocked()`, `paid()` kabi semantik methodlarni yarata olmaydi. Natijada test yana 12 ta `.field(...)` chaqiruviga aylanadi. Qo'lda yozilgan test builder'ning qiymati aynan default'larda va semantik shortcut'larda. Amaliy kelishuv: production sinfida Lombok `@Builder` qolsin, test tarafda esa uni o'rab turuvchi test builder bo'lsin — test builder `build()` ichida Lombok builder'ni chaqiradi. Shunda domen modeli o'zgarganda faqat bitta joy tuzatiladi.

### 10.4 Object Mother pattern

Object Mother — nomlangan tipik obyektlarni qaytaradigan static factory. Builder "qanday qurish"ni, Object Mother "qaysi tipik holat"ni ifodalaydi.

```java
public final class Customers {
    private Customers() {}

    public static Customer standard() {
        return aCustomer().build();
    }

    public static Customer vipCustomer() {
        return aCustomer().vip().withEmail("vip@example.com").build();
    }

    public static Customer blockedCustomer() {
        return aCustomer().blocked().build();
    }
}
```

Ikkisi raqobatchi emas: Object Mother ichida Builder ishlatiladi, test esa odatda Mother'dan boshlab, kerak bo'lsa Builder bilan nozik o'zgartirish kiritadi (`Customers.vipBuilder().withEmail(...)`).

Qachon qaysi biri: domenda **chindan ham nomlangan, takrorlanuvchi tipik holatlar** bo'lsa (VIP mijoz, bloklangan hisob, muddati o'tgan hujjat) — Object Mother o'qishni yaxshilaydi. Variatsiya o'qi ko'p va har test o'ziga xos kombinatsiya talab qilsa — faqat Builder. Object Mother'ning xavfi — o'sib ketishi: 60 ta method'li `Customers` sinfi hech kimga tushunarli bo'lmaydi va har biri kimdir tomonidan "ozgina" o'zgartirilib, boshqa 10 ta testni buzadi. Chegara: har Mother sinfida 5-10 ta mazmunli holat, qolgani Builder orqali.

### 10.5 Creation Method va test helper sinflarini tashkil qilish

Creation Method — test sinfi ichidagi `private Order paidOrderWithTwoLines()` kabi lokal yordamchi. Faqat bitta test sinfida ishlatilsa — shu yerda qolsin. Ikkinchi sinf kerak bo'lganda `src/test/java` ichidagi umumiy paketga ko'chiriladi.

Tavsiya etiladigan joylashuv: test builder va Mother sinflari **production paketining o'zida**, lekin `src/test/java` ostida turadi (`com.example.order.OrderTestBuilder`). Shunda package-private konstruktorlarga kirish imkoni saqlanadi va IDE'da model yonida turadi. Umumiy infratuzilma (baza tozalash, Testcontainers konfiguratsiyasi, custom assertion'lar) `com.example.test.support` kabi alohida paketda bo'ladi.

Modullar orasida test util'larni ulash uchun Maven'da test-jar:

```xml
<plugin>
  <groupId>org.apache.maven.plugins</groupId>
  <artifactId>maven-jar-plugin</artifactId>
  <executions>
    <execution>
      <goals><goal>test-jar</goal></goals>
    </execution>
  </executions>
</plugin>
```

Iste'molchi modul `<type>test-jar</type>` va `<scope>test</scope>` bilan bog'lanadi. Gradle'da shu maqsadda `java-test-fixtures` plugin ishlatiladi: `src/testFixtures/java` papkasi va `testFixtures(project(":order"))` dependency. Gradle varianti afzal — fixture kodi test kodidan ajratiladi va kompilyatsiya chegarasi aniq bo'ladi. Arxitektura nazorati: test fixture moduli production modulga bog'lanadi, teskarisi hech qachon.

### 10.6 Tasodifiy va generatsiya qilingan ma'lumot

Uch vosita amalda keng ishlatiladi:

- **Datafaker** (JavaFaker'ning faol davom etuvchisi) — realistik ism, manzil, email, IBAN, telefon generatsiyasi. JavaFaker arxivlangan, yangi loyihada Datafaker olinadi.
- **Instancio** — butun obyekt grafigini typed API bilan to'ldiradi, `set()`, `generate()`, `ignore()` orqali nozik boshqariladi, JUnit 5 extension'i va `@Seed` annotatsiyasi bor.
- **EasyRandom** (eski `random-beans`) — reflection orqali bean'ni tasodifiy to'ldiradi; hozir sust rivojlanadi, yangi loyihada Instancio afzal.

Foydasi: ahamiyatsiz maydonlarni yozishdan xalos qiladi va "faqat shu bitta maydon muhim" g'oyasini kuchaytiradi — qolgani shovqin sifatida random bo'ladi.

Xavfi: takrorlanmaydigan test. Random ism uzunligi 51 belgi chiqib, `varchar(50)` ustunini buzsa, test haftada bir qizil bo'ladi va qayta ishga tushirilganda yashil — bu suite'ga ishonchni yo'q qiladi.

Qoida: **seed qat'iy belgilanadi va log'ga chiqariladi**. Instancio'da:

```java
@ExtendWith(InstancioExtension.class)
class OrderMappingTest {

    @Seed(1234L)
    @Test
    void mapsAllFields() {
        Order order = Instancio.of(Order.class)
                .set(field(Order::getStatus), OrderStatus.PAID)
                .generate(field(OrderLine::getQuantity), gen -> gen.ints().range(1, 5))
                .ignore(field(Order::getId))
                .create();

        OrderDto dto = mapper.toDto(order);

        assertThat(dto.status()).isEqualTo("PAID");
        assertThat(dto.lines()).hasSameSizeAs(order.getLines());
    }
}
```

`InstancioExtension` test yiqilganda ishlatilgan seed'ni xato xabariga qo'shadi — shu seed'ni `@Seed` bilan qotirib, nosozlikni aynan takrorlash mumkin. Datafaker'da esa `new Faker(new Locale("uz"), new Random(42L))` ko'rinishida seed beriladi. Assertion'ni hech qachon random qiymatga emas, balki invariantga (uzunlik, diapazon, mapping tengligi) qurish kerak.

### 10.7 Ma'lumotlar bazasidagi holatni boshqarish

To'rtta usul va ularning o'rni:

**`@Sql` skriptlari** — Spring Test'ning deklarativ mexanizmi. Oddiy, tez, SQL'ni aniq ko'rsatadi. Lekin domen o'zgarganda jim eskiradi va kompilyator tekshirmaydi.

```java
@SpringBootTest
@Sql("/data/customers.sql")
@Sql(scripts = "/data/cleanup.sql", executionPhase = AFTER_TEST_METHOD)
class CustomerQueryTest {

    @Autowired CustomerRepository repository;

    @Test
    void vipMijozlarniTopadi() {
        assertThat(repository.findByTier(CustomerTier.VIP)).hasSize(2);
    }
}
```

**Flyway test migratsiyalari** — reference ma'lumot uchun eng barqaror yo'l. `src/test/resources/db/testdata` papkasi qo'shimcha location sifatida qo'shiladi:

```yaml
spring:
  flyway:
    locations: classpath:db/migration,classpath:db/testdata
```

Shu yerga `R__reference_data.sql` kabi repeatable migration joylanadi — valyutalar, soliq stavkalari, rollar. Bu Immutable Shared Fixture'ning amaliy ko'rinishi.

**Repository orqali yozish** — domen validatsiyasi va mapping ishlaydi, refactoring'ga chidamli, lekin sekinroq va JPA cascade/flush nozikliklariga sezgir. Business holat uchun asosiy tanlov.

**To'g'ridan-to'g'ri SQL insert** (`JdbcClient`, `JdbcTestUtils`) — domen orqali yaratish imkonsiz yoki juda qimmat bo'lgan holatlar uchun: legacy ustunlar, buzilgan ma'lumot scenario'lari, 10 000 qatorli performance fixture.

```sql
-- src/test/resources/data/customers.sql
INSERT INTO customers (id, name, email, tier, blocked, created_at) VALUES
  (1001, 'Nodira Yusupova', 'nodira@example.com', 'VIP',      false, '2026-01-10T09:00:00'),
  (1002, 'Sardor Alimov',   'sardor@example.com', 'VIP',      false, '2026-01-11T09:00:00'),
  (1003, 'Kamola Rashidova','kamola@example.com', 'STANDARD', true,  '2026-01-12T09:00:00');
```

Qoida: **sxema har doim Flyway orqali**, business ma'lumot repository yoki builder orqali, reference ma'lumot test migration orqali, maxsus holatlar `@Sql` orqali.

### 10.8 Testlar orasida izolyatsiya

| Usul | Tezlik | Ishonchlilik | Asosiy tuzoq |
|---|---|---|---|
| `@Transactional` test (rollback) | Juda tez | O'rtacha | Haqiqiy commit tekshirilmaydi; `@Async`, yangi thread, `REQUIRES_NEW` va MVC server portidagi so'rov bu tranzaksiyani ko'rmaydi |
| `TRUNCATE`/`DELETE` har testdan keyin | Tez | Yuqori | FK tartibi, sequence qiymatlari saqlanib qolishi |
| Har test uchun alohida schema | O'rtacha | Juda yuqori | Flyway'ni har schema'ga qayta yugurtirish narxi |
| Alohida tenant/prefiks (logik ajratish) | Juda tez | Yuqori | Kod multi-tenancy'ni qo'llab-quvvatlashi shart |
| Konteynerni qayta yaratish | Juda sekin | Maksimal | CI vaqti bir necha barobar oshadi |

`@Transactional` testning eng ko'p uchraydigan tuzog'i: `@SpringBootTest(webEnvironment = RANDOM_PORT)` bilan birga ishlatish. Server so'rovni boshqa thread'da, boshqa tranzaksiyada bajaradi — test yozgan ma'lumotni ko'rmaydi, test esa server yozganini rollback qila olmaydi. Bu holatda tranzaksion rollback'dan voz kechib, aniq tozalash kerak.

Amaliy default: **TRUNCATE strategiyasi**, bir marta yoziladigan umumiy extension bilan.

```java
public class DatabaseCleaner {

    private static final List<String> TABLES =
            List.of("order_lines", "orders", "customers");

    private final JdbcClient jdbc;

    public DatabaseCleaner(JdbcClient jdbc) {
        this.jdbc = jdbc;
    }

    public void clean() {
        jdbc.sql("SET session_replication_role = 'replica'").update();
        TABLES.forEach(t -> jdbc.sql("TRUNCATE TABLE " + t + " RESTART IDENTITY CASCADE").update());
        jdbc.sql("SET session_replication_role = 'origin'").update();
    }
}
```

Bu metod `@AfterEach` yoki `TestExecutionListener` ichidan chaqiriladi. `RESTART IDENTITY` sequence'larni qaytaradi — shu bilan "ID 1 bo'ladi" degan yashirin taxminlar fosh bo'ladi (va shuning uchun ID'ga tayanmaslik kerak). Jadvallar ro'yxatini qo'lda emas, `information_schema.tables`'dan o'qib olish yanada barqaror.

Reference ma'lumot TRUNCATE ro'yxatiga **kirmasligi** kerak — aks holda har testdan keyin Flyway seed'ini qayta yuklashga majbur bo'lasiz.

### 10.9 Tartibga bog'liqlik va uni aniqlash

Test interdependence — test B faqat test A'dan keyin ishlaganda o'tishi. JUnit 5 sukut bo'yicha deterministik, lekin tasodifiy bo'lmagan tartibni ishlatadi; shu barqarorlik muammoni yashiradi.

Aniqlash uchun tartibni ataylab buzish kerak. `junit-platform.properties` faylida:

```
junit.jupiter.testmethod.order.default=org.junit.jupiter.api.MethodOrderer$Random
junit.jupiter.testclass.order.default=org.junit.jupiter.api.ClassOrderer$Random
junit.jupiter.execution.order.random.seed=424242
```

Seed log'ga chiqadi — qizil bo'lgan tartibni aynan takrorlash mumkin. Bir sinf uchun esa `@TestMethodOrder(MethodOrderer.Random.class)` yoziladi. Agar test chindan ham tartibga muhtoj bo'lsa (`@TestMethodOrder(OrderAnnotation.class)` + `@Order`), bu odatda scenario testi — uni bitta `@Test` ichida yoki `@TestFactory` bilan ifodalash to'g'riroq.

Ikkinchi diagnostika usuli — bitta testni yakka ishga tushirish: `mvn test -Dtest=OrderServiceTest#vipChegirma` yoki `gradle test --tests "...vipChegirma"`. Yakka holda yiqilsa — test boshqa testning qoldirgan ma'lumotiga tayangan. Yakka holda o'tib, suite'da yiqilsa — kimdir uning ma'lumotini buzadi. CI'da nightly job sifatida random order bilan to'liq suite'ni ishga tushirish — arzon va juda samarali nazorat.

### 10.10 Katta hajmli va ishonchli ma'lumot

Ba'zi testlar (performance, hisobot, migratsiya tekshiruvi) realistik hajm va taqsimot talab qiladi. Production dump'ini to'g'ridan-to'g'ri olib kelish — eng oson va eng xatarli yo'l.

Huquqiy tomon: GDPR shaxsiy ma'lumotni test muhitida ishlatishni "maqsadga muvofiqlik" va "minimallashtirish" talablari bilan cheklaydi; O'zbekiston "Shaxsga doir ma'lumotlar to'g'risida"gi qonuni esa fuqarolar ma'lumotini mamlakat hududidagi texnik vositalarda saqlashni va qayta ishlashga rozilikni talab qiladi. Developer laptopidagi production dump — bu ikkisining ham buzilishi.

Amaliy yondashuvlar:

- **Anonimlashtirish/maskalash** — dump chiqarilayotganda ism, telefon, PINFL, karta raqami deterministik hash yoki fake qiymatga almashtiriladi. Deterministik bo'lishi muhim: bir xil kirish bir xil chiqishni bersa, JOIN'lar va analitika ishlaydi.
- **Sintetik generatsiya** — Datafaker + taqsimot modeli bilan noldan yaratish. Huquqiy risk nol, lekin real "iflos" holatlarni (bo'sh maydonlar, eski formatlar) qamrab olmaydi.
- **Subset** — referensial butunlikni saqlab, 1-5% nusxa olish. Hajm kichik, FK butun, CI'da ko'tarish mumkin.

Tavsiya: subset + deterministik maskalash quvuri avtomatlashtiriladi va u faqat himoyalangan muhitda ishlaydi; natija artifact sifatida versiyalanadi, repository'ga emas, object storage'ga joylanadi.

### 10.11 Vaqtga bog'liq ma'lumot

"Bugun" ga bog'langan test — kechiktirilgan nosozlik. `LocalDate.now()` ishlatgan kod oyning 31-kunida, yil oxirida yoki kun o'zgarishida boshqacha natija beradi.

Yechim: vaqtni dependency sifatida `java.time.Clock` orqali kiritish.

```java
@Service
public class InvoiceService {

    private final Clock clock;

    public InvoiceService(Clock clock) {
        this.clock = clock;
    }

    public boolean isOverdue(Invoice invoice) {
        return invoice.dueDate().isBefore(LocalDate.now(clock));
    }
}

class InvoiceServiceTest {

    private final Clock fixed = Clock.fixed(
            Instant.parse("2026-03-31T23:59:00Z"), ZoneId.of("Asia/Tashkent"));

    @Test
    void oyOxiridaMuddatiOtgan() {
        InvoiceService service = new InvoiceService(fixed);
        Invoice invoice = anInvoice().dueDate(LocalDate.of(2026, 3, 30)).build();

        assertThat(service.isOverdue(invoice)).isTrue();
    }
}
```

Production konfiguratsiyasida `@Bean Clock clock() { return Clock.systemDefaultZone(); }`. Moliyaviy tizimlarda alohida tekshirilishi shart holatlar: oy/chorak/yil oxiri, kun oxiri (end of day) kesimi, timezone chegarasidan o'tish (Tashkent UTC+5, DST yo'q, lekin UTC'da saqlangan `Instant` mahalliy kunni siljitadi), kabisa yili 29-fevral. Fixture'da sanalarni `LocalDate.now().minusDays(5)` emas, aniq literal bilan berish kerak — shunda test bir yildan keyin ham xuddi shu narsani tekshiradi.

### 10.12 Fayl, rasm va tashqi resurs ma'lumotlari

Test fayllari `src/test/resources` ostida, mazmunli papkalarda turadi (`fixtures/xml`, `fixtures/json`, `fixtures/csv`). Ularni o'qishda absolute path emas, classpath resource ishlatiladi:

```java
class StatementParserTest {

    @Test
    void mt940FayliniOqiydi() throws Exception {
        ClassPathResource resource = new ClassPathResource("fixtures/mt940/sample.sta");
        String content;
        try (InputStream in = resource.getInputStream()) {
            content = new String(in.readAllBytes(), StandardCharsets.UTF_8);
        }

        Statement statement = parser.parse(content);

        assertThat(statement.transactions()).hasSize(3);
        assertThat(statement.closingBalance()).isEqualTo(new BigDecimal("1250.75"));
    }
}
```

Katta fayllarni (bir necha MB'dan oshadigan PDF, rasm, dump) repository'ga qo'ymaslik kerak — git tarixi shishadi va har clone sekinlashadi. Variantlar: hajmni qisqartirilgan namuna, generatsiya qilib yaratish (`new byte[5_000_000]` bilan sintetik fayl), yoki tashqi artifact repository'dan CI vaqtida yuklab olish. Rasm va PDF solishtirishda bayt-bayt tenglikni emas, mazmunni (o'lcham, sahifa soni, ajratilgan matn) tekshirish kerak — kutubxona versiyasi o'zgarishi baytni o'zgartiradi.

### 10.13 QA uchun test ma'lumoti

Manual va E2E testlar uchun test muhitida barqaror hisob va ma'lumot to'plamlari bo'lishi kerak: `qa-vip@example.com`, `qa-blocked@example.com`, bo'sh savatli hisob, to'lanmagan buyurtmasi bor hisob. Ular hujjatlashtiriladi va kodda emas, muhit seed'ida yashaydi.

Eng muhim talab — **tiklanish (reset) imkoni**. Test muhitida faqat test profilida yoqiladigan endpoint yoki CLI buyruq bo'lishi kerak:

```java
@RestController
@RequestMapping("/internal/test-data")
@Profile("qa")
class TestDataResetController {

    private final TestDataSeeder seeder;

    TestDataResetController(TestDataSeeder seeder) {
        this.seeder = seeder;
    }

    @PostMapping("/reset")
    ResponseEntity<Void> reset() {
        seeder.resetToBaseline();
        return ResponseEntity.noContent().build();
    }
}
```

`@Profile("qa")` bu endpoint production'da registratsiya qilinmasligini kafolatlaydi; qo'shimcha himoya sifatida uni authentication ortiga qo'yish va faqat ichki tarmoqdan ochish kerak.

Ma'lumotni bazada qo'lda SQL bilan tuzatish — zararli amaliyot: hech kim nima o'zgarganini bilmaydi, bir hafta o'tib QA muhiti hech bir kodga mos kelmaydigan holatga tushadi va "bizda ishlaydi" janriga olib keladi. Har qanday tuzatish seed skriptiga yozilib, reset orqali qayta qo'llanishi kerak.

### 10.14 Anti-patternlar

- **Umumiy yozuvga tayanish** — bir nechta test bitta mijoz yoki buyurtmani baham ko'rishi. Natija: tartibga bog'liqlik, parallel ishlashning imkonsizligi, sabablari tushunarsiz nosozliklar.
- **Hardcoded ID** — `assertThat(order.getId()).isEqualTo(1L)` yoki `@Sql`dagi `id = 1001`'ga tayanish. Sequence o'zgarsa yoki testlar tartibi almashsa darhol buziladi. Yaratilgan obyekt qaytargan ID'dan foydalanish kerak.
- **Production ma'lumotini to'g'ridan-to'g'ri ishlatish** — huquqiy risk va ma'lumot utkazishi.
- **Katta SQL dump fayllari** — repository'da yotgan 50 MB `testdata.sql`: sekin, o'qilmaydi, review qilinmaydi, sxema o'zgarganda jim eskiradi.
- **Har testda butun bazani tozalash va qayta migratsiya** — "xavfsiz" ko'rinadi, lekin suite vaqtini o'nlab barobar oshiradi va natijada komanda testlarni lokal ishga tushirishni to'xtatadi.
- **Default'lar o'rniga `null`/bo'sh qiymatlar** — builder `email = null` bersa, testlar o'tadi, production validatsiyasi buziladi.
- **Fixture'da business logikasi** — `if (customer.isVip()) total = ...` kabi hisob fixture ichida takrorlanishi: test o'zi tekshirayotgan logikani qayta yozib, nosozlikni yashiradi.

### 10.15 Arxitektor nazorat ro'yxati

- [ ] Loyihada fixture strategiyasi hujjatlashtirilgan: mutable business ma'lumot uchun Fresh Fixture, reference ma'lumot uchun Flyway test migration orqali Immutable Shared Fixture.
- [ ] Har bir asosiy aggregate uchun Test Data Builder mavjud va default qiymatlar valid; tipik holatlar Object Mother bilan nomlangan.
- [ ] Test fixture kodi `java-test-fixtures` yoki Maven test-jar orqali modullar orasida ulangan; fixture modul production'ga bog'liq, teskarisi yo'q.
- [ ] Izolyatsiya usuli bitta va aniq tanlangan (TRUNCATE yoki schema-per-test); `@Transactional` test `webEnvironment = RANDOM_PORT` bilan birga ishlatilmaydi.
- [ ] Random ma'lumot ishlatilsa, seed qat'iy belgilangan yoki xato xabariga chiqariladi; assertion'lar random qiymatga emas, invariantga qurilgan.
- [ ] CI'da random test order bilan ishlaydigan nightly job bor va tartibga bog'liq testlar aniqlanadi.
- [ ] Vaqtga bog'liq kod `Clock` bean orqali ishlaydi; oy/yil oxiri va kun oxiri holatlari uchun fixed Clock testlari mavjud.
- [ ] Production ma'lumoti test muhitiga faqat subset + deterministik maskalash quvuri orqali o'tadi; QA muhitida `@Profile`-himoyalangan reset mexanizmi bor va qo'lda SQL tuzatish taqiqlangan.

---

## 11. Xavfsizlik, tranzaksiya, asinxron va konkurentlik testlari (Testing Security, Transactions, Async & Concurrency)

Xavfsizlik, tranzaksiya, asinxronlik va konkurentlik — Spring ilovalarining eng ko'p buziladigan, ammo eng kam testlanadigan to'rt sohasi. Bu yerdagi xatolar kompilyatsiya vaqtida ko'rinmaydi: ular production'da noto'g'ri ruxsat, yarim commit bo'lgan ma'lumot yoki ikki marta yechilgan to'lov ko'rinishida chiqadi. Bobda har bir sohani Spring Security 6.x, Spring Boot 3.x/4.x, JUnit 5, Awaitility, Spring Retry va Resilience4j vositalari bilan deterministik testga qanday aylantirish mumkinligini ko'ramiz. Arxitektor uchun asosiy savol — qaysi qoida testga majburan qoplanishi kerak va qaysi chegaradan keyin test emas, boshqa vosita turi kerak.

### 11.1 Spring Security'ni testlash asoslari

`spring-security-test` moduli (`testImplementation 'org.springframework.security:spring-security-test'`) ikki xil mexanizm beradi. Birinchisi — annotatsiyalar: `@WithMockUser` soxta `Authentication` yaratadi, `@WithAnonymousUser` kontekstni anonim holatga qo'yadi, `@WithUserDetails` esa haqiqiy `UserDetailsService` bean'idan foydalanuvchini yuklaydi (shuning uchun u rol xaritalashdagi xatoni ham ushlaydi). Ikkinchisi — `SecurityMockMvcRequestPostProcessors`: `user()`, `jwt()`, `opaqueToken()`, `csrf()`. Post-processor'lar afzal, chunki ularni parametrlashtirilgan testga uzatish mumkin. `@WebMvcTest` sizning `SecurityFilterChain` konfiguratsiyangizni skan qilmaydi — uni `@Import` bilan qo'shish shart, aks holda test real qoidalarni emas, Boot'ning default himoyasini tekshiradi.

```java
@WebMvcTest(OrderController.class)
@Import(SecurityConfig.class)   // SecurityFilterChain avtomatik skan QILINMAYDI
class OrderControllerSecurityTest {

    @Autowired MockMvc mvc;
    @MockitoBean OrderService orderService;   // Boot 3.4+; oldin @MockBean

    @Test @WithMockUser(username = "ali", roles = "USER")
    void userSeesOwnOrders() throws Exception {
        mvc.perform(get("/api/orders")).andExpect(status().isOk());
    }

    @Test @WithAnonymousUser
    void anonymousGetsUnauthorized() throws Exception {
        mvc.perform(get("/api/orders")).andExpect(status().isUnauthorized());
    }

    @Test @WithUserDetails("manager@acme.io")
    void managerCanDeleteWithCsrf() throws Exception {
        mvc.perform(delete("/api/orders/1").with(csrf()))
           .andExpect(status().isNoContent());
    }

    @Test @WithMockUser(roles = "MANAGER")
    void missingCsrfTokenIsForbidden() throws Exception {
        mvc.perform(delete("/api/orders/1")).andExpect(status().isForbidden());
    }
}
```

Reaktiv stack'da ekvivalenti `WebTestClient` va `SecurityMockServerConfigurers` (`mockUser()`, `mockJwt()`, `mockOpaqueToken()`) bo'ladi; ular `mutateWith()` orqali bitta so'rovga qo'llanadi.

```java
@SpringBootTest(webEnvironment = WebEnvironment.RANDOM_PORT)   // WebFlux
@AutoConfigureWebTestClient
class ReportApiSecurityTest {

    @Autowired WebTestClient client;

    @Test
    void scopeReportsReadIsAllowed() {
        client.mutateWith(mockJwt().jwt(j -> j.claim("scope", "reports:read")))
              .get().uri("/api/reports")
              .exchange().expectStatus().isOk();
    }
}
```

### 11.2 Avtorizatsiya qoidalarini testlash

Avtorizatsiya — bu matritsa, demak uni matritsa sifatida testlash kerak: rol x endpoint x kutilgan HTTP status. Bu jadval arxitektura artefakti bo'lib, kodda bitta joyda (test `@MethodSource`'ida yoki CSV faylda) yashashi va yangi endpoint qo'shilganda majburan to'ldirilishi lozim. Eng muhim qatorlar — ruxsat berilganlar emas, **rad etilganlar**: `403` kutilgan hollar regressiyani birinchi ushlaydi. `401` va `403` ni aralashtirib yubormang: autentifikatsiya yo'q — `401`, bor-u huquq yo'q — `403`.

| Endpoint | Metod | ANONYMOUS | ROLE_USER | ROLE_MANAGER | ROLE_ADMIN |
|---|---|---|---|---|---|
| /api/orders | GET | 401 | 200 | 200 | 200 |
| /api/orders | POST | 401 | 201 | 201 | 201 |
| /api/orders/{id} | DELETE | 401 | 403 | 204 | 204 |
| /api/orders/{id}/refund | POST | 401 | 403 | 403 | 200 |
| /api/admin/users | GET | 401 | 403 | 403 | 200 |
| /actuator/health | GET | 200 | 200 | 200 | 200 |
| /actuator/env | GET | 401 | 403 | 403 | 200 |

```java
@SpringBootTest
@AutoConfigureMockMvc
class AuthorizationMatrixTest {

    @Autowired MockMvc mvc;

    record Rule(String role, HttpMethod method, String path, int expected) {}

    static Stream<Rule> matrix() {
        return Stream.of(
            new Rule("ANON",    HttpMethod.GET,    "/api/orders",          401),
            new Rule("USER",    HttpMethod.GET,    "/api/orders",          200),
            new Rule("USER",    HttpMethod.DELETE, "/api/orders/1",        403),
            new Rule("MANAGER", HttpMethod.DELETE, "/api/orders/1",        204),
            new Rule("MANAGER", HttpMethod.POST,   "/api/orders/1/refund", 403),
            new Rule("ADMIN",   HttpMethod.POST,   "/api/orders/1/refund", 200));
    }

    @ParameterizedTest(name = "{0}")
    @MethodSource("matrix")
    void endpointFollowsMatrix(Rule r) throws Exception {
        var req = request(r.method(), r.path()).with(csrf());
        if (!"ANON".equals(r.role())) req = req.with(user("t").roles(r.role()));
        mvc.perform(req).andExpect(status().is(r.expected()));
    }
}
```

Qo'shimcha nazorat: `RequestMappingHandlerMapping` bean'idan barcha mapping'larni olib, ularning har biri matritsada borligini tasdiqlaydigan test yozing. Shunda "yangi endpoint qo'shdim, security qoidasini yozishni esdan chiqardim" holati CI'da qulaydi.

### 11.3 Method security'ni testlash

`@EnableMethodSecurity` bilan `@PreAuthorize`/`@PostAuthorize` AOP proxy orqali ishlaydi, demak testda bean kontekstdan olinishi shart — `new AccountService()` hech narsani tekshirmaydi. `@WithMockUser` ishlaydi, chunki u `TestSecurityContextHolder` orqali `SecurityContextHolder`'ni to'ldiradi. Ba'zan rolni dinamik yasash kerak bo'ladi — o'shanda `SecurityContext`'ni qo'lda to'ldirib, `finally` blokida tozalash kerak. `@PostAuthorize` uchun yodda tuting: metod allaqachon bajarilib bo'lgan, shuning uchun test yon ta'sir (yozuv) rollback bo'lganini ham tekshirishi lozim.

```java
@SpringBootTest
class AccountServiceSecurityTest {

    @Autowired AccountService service;   // @PreAuthorize("hasRole('ADMIN')")

    @Test
    @WithMockUser(roles = "SUPPORT")
    void supportCannotCloseAccount() {
        assertThatThrownBy(() -> service.close(42L))
            .isInstanceOf(AccessDeniedException.class);
    }

    @Test
    void manualSecurityContextIsHonoured() {
        var ctx = SecurityContextHolder.createEmptyContext();
        ctx.setAuthentication(new UsernamePasswordAuthenticationToken(
                "ops", "n/a", List.of(new SimpleGrantedAuthority("ROLE_ADMIN"))));
        SecurityContextHolder.setContext(ctx);
        try {
            assertThat(service.close(42L)).isTrue();
        } finally {
            SecurityContextHolder.clearContext();
        }
    }
}
```

Spring Security 6.3+ da method security `AuthorizationDeniedException` tashlaydi — u `AccessDeniedException`'ning merosxo'ri, shuning uchun yuqoridagi assertion ikkala versiyada ham o'tadi.

### 11.4 OAuth2 va JWT: Resource Server'ni testlash

Resource Server'da asosiy xavf — claim'dan authority'ga xaritalash. Default `JwtGrantedAuthoritiesConverter` `scope`/`scp` claim'ini `SCOPE_` prefiksi bilan authority'ga aylantiradi. `jwt()` post-processor'iga `.jwt(...)` bilan claim bersangiz, shu konverter ishga tushadi va siz real xaritalashni testlaysiz; `.authorities(...)` bersangiz esa konverterni chetlab o'tasiz va buzuq Keycloak `realm_access` parser'i testda ko'rinmay qoladi. Shuning uchun maxsus konverter uchun doim claim darajasidan boshlang.

```java
@Test
void scopeClaimBecomesScopeAuthority() throws Exception {
    mvc.perform(get("/api/reports").with(jwt()
            .jwt(j -> j.subject("svc-1").claim("scope", "reports:read"))))
       .andExpect(status().isOk());
}

@Test
void customAuthorityConverterIsExercised() throws Exception {
    mvc.perform(get("/api/admin/metrics").with(jwt().jwt(j -> j
            .claim("realm_access", Map.of("roles", List.of("admin"))))))
       .andExpect(status().isOk());   // realm_access -> ROLE_admin
}

@Test
void opaqueTokenWithoutScopeIsForbidden() throws Exception {
    mvc.perform(get("/api/reports").with(opaqueToken()
            .attributes(a -> a.put("sub", "svc-1"))))
       .andExpect(status().isForbidden());
}
```

`jwt()` imzo, `iss`, `aud` va `exp` tekshiruvini butunlay o'tkazib yuboradi. Shu sababli kamida bitta test real token oqimini bosib o'tishi kerak: RSA kalit juftini testda generatsiya qilib, JWKS'ni mock HTTP server orqali uzatish va `spring.security.oauth2.resourceserver.jwt.jwk-set-uri` ni unga yo'naltirish, yoki Keycloak Testcontainer'dan haqiqiy `access_token` olish (8-bobga qarang). Issuer validatsiyasining buzilishi aynan shu testda ushlanadi.

### 11.5 CSRF, CORS, security header va sessiya

`csrf()` post-processor'i to'g'ri token qo'shadi; `csrf().useInvalidToken()` esa himoya haqiqatan ishlayotganini tasdiqlaydi. Stateless JWT API'da CSRF'ni o'chirish o'rinli, lekin bu qaror testda yozilgan bo'lishi kerak. Security header'lar bo'yicha diqqat: HSTS faqat `secure` so'rovda yuboriladi, shuning uchun MockMvc'da `.secure(true)` kerak. CORS preflight noto'g'ri origin'dan kelganda Spring Security `403` qaytaradi.

```java
@SpringBootTest
@AutoConfigureMockMvc
class HttpSecurityContractTest {

    @Autowired MockMvc mvc;

    @Test @WithMockUser
    void defaultSecurityHeadersAreSent() throws Exception {
        mvc.perform(get("/api/orders").secure(true))   // HSTS faqat HTTPS'da
           .andExpect(header().string("X-Content-Type-Options", "nosniff"))
           .andExpect(header().string("X-Frame-Options", "DENY"))
           .andExpect(header().exists("Strict-Transport-Security"));
    }

    @Test
    void preflightFromUnknownOriginIsRejected() throws Exception {
        mvc.perform(options("/api/orders")
                .header(HttpHeaders.ORIGIN, "https://evil.example")
                .header(HttpHeaders.ACCESS_CONTROL_REQUEST_METHOD, "GET"))
           .andExpect(status().isForbidden());
    }

    @Test
    void statelessApiCreatesNoHttpSession() throws Exception {
        var result = mvc.perform(get("/api/orders").with(jwt())).andReturn();
        assertThat(result.getRequest().getSession(false)).isNull();
    }
}
```

Sessiya boshqaruvi uchun ikki testni unutmang. Session fixation: `MockHttpSession` bilan login qilib, `result.getRequest().getSession(false).getId()` login oldidagi id'dan farq qilishini tasdiqlang (default strategiya `changeSessionId`). Concurrent session: `maximumSessions(1)` qo'yilganda ikkinchi login'dan keyin `SessionRegistry.getAllSessions(principal, false)` bitta yozuv qoldirishini va birinchi sessiya `isExpired()` bo'lishini tekshiring.

### 11.6 Xavfsizlik testining chegarasi

Unit va integration testlar faqat **siz yozgan qoidalarni** tekshiradi: matritsa bo'yicha endpoint himoyalanganmi, claim to'g'ri xaritalanganmi, CSRF yoqilganmi. Ular noma'lum zaifliklarni, dependency CVE'larini, noto'g'ri sozlangan infrastrukturani, SQL injection yoki IDOR'ni tizimli qidirmaydi. Bu ishlar uchun alohida qatlam kerak: SAST (kod tahlili), dependency scanning, DAST va qo'lda penetration test — ular 13-bobda ko'rilgan. Test strategiyasida bu chegarani yozib qo'ying, aks holda "100% security test qoplangan" degan yolg'on xotirjamlik paydo bo'ladi.

### 11.7 Tranzaksiya chegaralarini testlash

Tranzaksiya testida birinchi qoida: **test metodining o'ziga `@Transactional` qo'ymang**. Aks holda hamma narsa bitta tranzaksiyada bo'lib, oxirida rollback qilinadi — propagation va commit xatti-harakatini ko'rish imkonsiz. Haqiqiy baza (Testcontainers, 8-bob) va yozuvlarni tashqaridan sanash kerak. `REQUIRES_NEW` yangi connection oladi, shuning uchun test profilida pool hajmi kamida 2 bo'lsin. `NESTED` savepoint talab qiladi: `JpaTransactionManager` uni faqat `setNestedTransactionAllowed(true)` bilan va dialekt qo'llab-quvvatlasa bajaradi. Eng ko'p uchraydigan tuzoq — checked exception default holda rollback qilmaydi.

```java
@SpringBootTest                       // DIQQAT: test metodida @Transactional YO'Q
class TransactionBoundaryTest {

    @Autowired OrderFacade facade;    // REQUIRED, ichida audit REQUIRES_NEW
    @Autowired OrderRepository orders;
    @Autowired AuditRepository audits;
    @Autowired JdbcTemplate jdbc;

    @AfterEach void cleanUp() { jdbc.execute("truncate orders, audit_log"); }

    @Test
    void requiresNewCommitsEvenIfOuterRollsBack() {
        assertThatThrownBy(() -> facade.placeAndFail("SKU-1"))
            .isInstanceOf(IllegalStateException.class);

        assertThat(orders.count()).isZero();   // tashqi REQUIRED rollback
        assertThat(audits.count()).isOne();    // ichki REQUIRES_NEW commit
    }

    @Test
    void checkedExceptionCommitsUnlessRollbackForIsSet() {
        assertThatThrownBy(() -> facade.placeAndThrowChecked("SKU-2"))
            .isInstanceOf(QuotaExceededException.class);

        assertThat(orders.count()).isOne();    // klassik tuzoq: rollback bo'lmadi
    }
}
```

Self-invocation muammosini ham test bilan ushlash mumkin: proxy chetlab o'tilganda tranzaksiya umuman boshlanmaydi.

```java
@Service
public class ReportService {

    @Transactional
    public boolean proxied() {
        return TransactionSynchronizationManager.isActualTransactionActive();
    }

    public boolean viaSelfCall() { return proxied(); }   // proxy chetlab o'tiladi
}

// Test (service bean kontekstdan olinadi):
assertThat(service.proxied()).isTrue();
assertThat(service.viaSelfCall()).isFalse();   // self-invocation fosh bo'ldi
```

Oraliq holatni tekshirish uchun `TestTransaction.flagForCommit()` va `TestTransaction.end()` yordam beradi: testning o'rtasida commit qilib, keyin yangi tranzaksiyada natijani o'qish mumkin.

### 11.8 Optimistik va pessimistik lock'ni testlash

`@Version` bilan to'qnashuvni thread'lar bilan yasash mumkin, lekin bu beqaror chiqadi. Deterministik yo'l — bitta thread'da ikkita `EntityManager` ochib, ikkisi ham bir xil versiyani o'qib, birin-ketin commit qilish: ikkinchi commit kafolatli yiqiladi.

```java
@SpringBootTest
class OptimisticLockTest {

    @Autowired EntityManagerFactory emf;
    @Autowired ProductRepository repo;

    @Test
    void staleVersionIsRejectedOnCommit() {
        Long id = repo.save(new Product("A", 100)).getId();
        var em1 = emf.createEntityManager();
        var em2 = emf.createEntityManager();
        try {
            em1.getTransaction().begin();
            em2.getTransaction().begin();
            Product p1 = em1.find(Product.class, id);   // version = 0
            Product p2 = em2.find(Product.class, id);   // version = 0

            p1.setPrice(110);
            em1.getTransaction().commit();              // version -> 1

            p2.setPrice(120);
            assertThatThrownBy(() -> em2.getTransaction().commit())
                .isInstanceOf(RollbackException.class)
                .hasCauseInstanceOf(OptimisticLockException.class);
        } finally { em1.close(); em2.close(); }
    }
}
```

Service qatlami orqali kelganda Spring bu xatoni `ObjectOptimisticLockingFailureException`'ga o'raydi — retry logikasi borligini ham shu turdagi assertion bilan tekshiring. Pessimistik lock uchun esa lock'ni ushlab turuvchi ikkinchi tranzaksiya kerak; `Thread.sleep` emas, `CountDownLatch` bilan koordinatsiya qiling. Lock timeout hint'i DB'ga bog'liq: PostgreSQL'da `0` qiymati `FOR UPDATE NOWAIT`ga aylanadi.

```java
public interface SeatRepository extends JpaRepository<Seat, Long> {
    @Lock(LockModeType.PESSIMISTIC_WRITE)
    @QueryHints(@QueryHint(name = "jakarta.persistence.lock.timeout", value = "0"))
    @Query("select s from Seat s where s.id = :id")
    Optional<Seat> findByIdForUpdate(@Param("id") Long id);
}

@Test
void secondTransactionCannotTakeTheSameRowLock() throws Exception {
    var locked = new CountDownLatch(1);
    var release = new CountDownLatch(1);
    var pool = Executors.newFixedThreadPool(1);

    pool.submit(() -> tx.executeWithoutResult(s -> {
        seats.findByIdForUpdate(1L);
        locked.countDown();
        awaitQuietly(release);                 // lock'ni ushlab turish
    }));
    assertThat(locked.await(5, TimeUnit.SECONDS)).isTrue();

    assertThatThrownBy(() -> tx.executeWithoutResult(
            s -> seats.findByIdForUpdate(1L)))
        .isInstanceOf(PessimisticLockingFailureException.class);

    release.countDown();
    pool.shutdown();
}
```

### 11.9 Asinxron kodni testlash

`@Async` metod, `@EventListener` va `@TransactionalEventListener(phase = AFTER_COMMIT)` natijasini `Thread.sleep` bilan kutish — eng tez beqarorlashadigan naqsh. O'rniga Awaitility: `await().atMost(...).pollInterval(...).untilAsserted(...)` shart bajarilishi bilanoq davom etadi, bajarilmasa aniq xabar bilan yiqiladi. `AFTER_COMMIT` listener'i uchun yana bir shart bor: test metodi `@Transactional` bo'lmasligi kerak, aks holda commit umuman bo'lmaydi va listener hech qachon chaqirilmaydi. Determinizm kerak bo'lsa, `CountDownLatch` bilan aniq signal kutish eng ishonchli variant.

```java
@SpringBootTest
@RecordApplicationEvents
class OrderEventFlowTest {

    @Autowired OrderService orders;
    @Autowired ApplicationEvents events;
    @Autowired MailProbe mailProbe;   // @TransactionalEventListener(AFTER_COMMIT)

    @Test
    void eventIsPublishedAndHandledAfterCommit() {
        orders.place(new PlaceOrder("SKU-7", 2));

        assertThat(events.stream(OrderPlaced.class)).hasSize(1);

        await().atMost(Duration.ofSeconds(5))
               .pollInterval(Duration.ofMillis(50))
               .untilAsserted(() ->
                   assertThat(mailProbe.sent()).containsExactly("SKU-7"));
    }

    @Test
    void latchVariantForAsyncHandler() throws Exception {
        var latch = mailProbe.resetLatch(1);
        orders.place(new PlaceOrder("SKU-8", 1));
        assertThat(latch.await(5, TimeUnit.SECONDS)).isTrue();
    }
}
```

### 11.10 Spring event'larni testlash

`@RecordApplicationEvents` test klassiga qo'yilsa, `ApplicationEvents` bean'ini inject qilib publish qilingan event'larni to'g'ridan-to'g'ri tasdiqlash mumkin — har bir test metodi uchun yozuv alohida. Bu modul chegarasini tekshirishning eng arzon usuli: service listener'ni emas, faqat event'ni publish qilganini tasdiqlaydi. Spring Modulith'da esa `Scenario` API modullar orasidagi oqimni to'liq kuzatadi — stimulni beradi, event kelishini kutadi va keyin yon modul holatini tekshiradi.

```java
@ApplicationModuleTest
class OrderModuleTest {

    @Test
    void completingOrderReleasesInventory(Scenario scenario) {
        scenario.stimulate(() -> orders.complete(42L))
                .andWaitForEventOfType(OrderCompleted.class)
                .matchingMappedValue(OrderCompleted::orderId, 42L)
                .toArriveAndVerify(evt ->
                    assertThat(inventory.reserved(42L)).isZero());
    }
}
```

### 11.11 Scheduled task va job'larni testlash

Scheduler'da "qachon" va "nima" ni ajratish kerak. "Nima" — oddiy service metodi, u odatdagicha testlanadi; `@Scheduled` metod esa to'g'ridan-to'g'ri chaqirilib tekshiriladi. "Qachon" — cron ifodasi, uni `CronExpression.parse(...).next(...)` bilan alohida testlash kerak, chunki `MON-FRI` yoki yil oxiri xatosi faqat shunda ko'rinadi. Testda scheduler umuman ishga tushmasligi uchun cron'ni property'dan oling va test profilida `Scheduled.CRON_DISABLED` (`"-"`) qiymatini bering yoki `@EnableScheduling`'ni `@Profile("!test")` konfiguratsiyaga chiqaring. ShedLock'li cluster xatti-harakati uchun real DB lock jadvali bilan `LockProvider`'ni ikki marta chaqirib, ikkinchi urinish `Optional.empty()` qaytarishini tasdiqlang.

```java
@SpringBootTest
@SpringBatchTest
class NightlyReportJobTest {

    @Autowired JobLauncherTestUtils jobLauncherTestUtils;
    @Autowired JobRepositoryTestUtils jobRepositoryTestUtils;

    @AfterEach void clean() { jobRepositoryTestUtils.removeJobExecutions(); }

    @Test
    void jobCompletesAndWritesEveryRow() throws Exception {
        var params = new JobParametersBuilder()
                .addLocalDate("runDate", LocalDate.of(2026, 1, 31))
                .toJobParameters();

        JobExecution exec = jobLauncherTestUtils.launchJob(params);

        assertThat(exec.getExitStatus()).isEqualTo(ExitStatus.COMPLETED);
        assertThat(exec.getStepExecutions())
            .anySatisfy(s -> assertThat(s.getWriteCount()).isEqualTo(100L));
    }

    @Test
    void cronFiresOnWorkdayMornings() {
        var cron = CronExpression.parse("0 0 6 * * MON-FRI");
        assertThat(cron.next(LocalDateTime.of(2026, 1, 30, 7, 0)))   // juma
            .isEqualTo(LocalDateTime.of(2026, 2, 2, 6, 0));          // dushanba
    }
}
```

`JobLauncherTestUtils.launchStep("stepName")` bitta step'ni izolyatsiyada ishga tushiradi — katta job'ning bir bosqichidagi reader/processor/writer mantiqini tez tekshirish uchun qulay.

### 11.12 Konkurentlik va poyga holatini testlash

Race condition testi ikkita narsani talab qiladi: yetarlicha parallellik va bir vaqtda urish. `ExecutorService` birinchisini, `CyclicBarrier` ikkinchisini beradi — barcha thread'lar barrier'da to'planib, keyin bir paytda kirishadi. Tekshiriladigan xossa odatda idempotentlik: bir xil idempotency key bilan N marta urilganda bazada aynan bitta yozuv qolishi kerak. Unique constraint bu yerda oxirgi himoya chizig'i, shuning uchun test uning haqiqatan ishlayotganini (va `DataIntegrityViolationException` to'g'ri ushlanayotganini) ham tasdiqlashi lozim.

```java
@SpringBootTest
class PaymentIdempotencyTest {

    @Autowired PaymentService payments;
    @Autowired PaymentRepository repo;

    @RepeatedTest(5)
    void sameIdempotencyKeyCreatesExactlyOneCharge() throws Exception {
        int threads = 16;
        var key = "key-" + UUID.randomUUID();
        var barrier = new CyclicBarrier(threads);
        var pool = Executors.newFixedThreadPool(threads);
        var cmd = new Charge(key, BigDecimal.TEN);

        var futures = IntStream.range(0, threads).mapToObj(i -> pool.submit(() -> {
            barrier.await(10, TimeUnit.SECONDS);
            try { payments.charge(cmd); } catch (DuplicateChargeException ok) { }
            return null;
        })).toList();

        for (var f : futures) f.get(15, TimeUnit.SECONDS);
        pool.shutdown();

        assertThat(repo.countByIdempotencyKey(key)).isOne();
    }
}
```

Bunday testlar tabiatan beqarorlikka moyil. Beqarorlikni kamaytirish uchun: har bir takrorlashda yangi kalit/ID ishlating, hech qachon `Thread.sleep` bilan sinxronlashtirmang, timeout'larni sahiy (lekin cheksiz emas) qo'ying, thread sonini CI mashinasining yadrolaridan kelib chiqib belgilang va bu testlarni `@Tag("concurrency")` bilan ajratib alohida CI job'da yurgizing. Beqaror testni "retry until green" bilan ko'mish — xatoni ko'mish; bu mavzu 16-bobda batafsil.

### 11.13 Retry, timeout va circuit breaker'ni testlash

`@Retryable` da eng muhim tekshiruv — urinishlar **soni**: mock gateway'ga `verify(gateway, times(3))` qo'ying, aks holda `maxAttempts` qiymatini o'zgartirgan refactoring sezilmay o'tadi. Test tezligi uchun backoff'ni property orqali kichraytiring. Resilience4j'da circuit breaker holatini kutib o'tirmasdan `transitionToOpenState()` bilan majburan oching va `@BeforeEach` da `reset()` qiling — aks holda testlar bir-biriga ta'sir qiladi. Kechikish va 5xx simulyatsiyasi uchun WireMock (9-bob) ishlatiladi: `withFixedDelay` timeout'ni, `withFault` esa connection reset holatini tekshiradi.

```java
@SpringBootTest
class ResilienceTest {

    @Autowired RatesClient client;    // @Retryable(retryFor = ..., maxAttempts = 3)
    @MockitoBean RatesGateway gateway;
    @Autowired CircuitBreakerRegistry registry;

    @BeforeEach void resetCircuit() { registry.circuitBreaker("rates").reset(); }

    @Test
    void retryStopsAfterThreeAttempts() {
        when(gateway.fetch()).thenThrow(new RemoteException("503"));

        assertThatThrownBy(client::rates).isInstanceOf(RemoteException.class);
        verify(gateway, times(3)).fetch();
    }

    @Test
    void openCircuitFailsFastWithoutRemoteCall() {
        registry.circuitBreaker("rates").transitionToOpenState();

        assertThatThrownBy(client::rates)
            .isInstanceOf(CallNotPermittedException.class);
        verifyNoInteractions(gateway);
    }
}
```

Fallback'ni ham testlang: circuit ochiqligida ilova cache'dagi qiymatni qaytarishi kerakmi yoki `503` berishi kerakmi — bu mahsulot qarori va u test bilan muhrlanishi shart.

### 11.14 Anti-patternlar

- Xavfsizlikni faqat qo'lda, brauzerda "ishladi" deb tekshirish; rad etilish (`403`) holatlari uchun bitta ham avtomatik test yo'q.
- Hamma joyda `@WithMockUser` ishlatib, haqiqiy token oqimini (imzo, `iss`, `aud`, `exp`, claim-to-authority konverteri) hech qachon bosib o'tmaslik.
- Test metodiga `@Transactional` qo'yib, keyin commit, `AFTER_COMMIT` listener va propagation xatti-harakatini "tekshirgan" deb hisoblash.
- Asinxron natijani `Thread.sleep(2000)` bilan kutish; CI sekinlashganda test yiqiladi, tezlashganda esa yolg'on yashil bo'ladi.
- `@MockBean`/`@MockitoBean` bilan security filter chain'ni butunlay chetlab o'tib, faqat controller mantiqini test qilib "endpoint himoyalangan" degan xulosa chiqarish.
- Checked exception'da rollback bo'lishini taxmin qilish va `rollbackFor` yo'qligini test bilan tasdiqlamaslik.
- Race condition testini yozib, beqarorligi uchun `@Disabled` qo'yish yoki CI'da retry bilan yashirish.

### 11.15 Arxitektor nazorat ro'yxati

- [ ] Har bir himoyalangan endpoint uchun rol x metod x status matritsasi mavjud va parametrlashtirilgan test bilan to'liq qoplangan (401 va 403 ajratilgan).
- [ ] Kamida bitta test real JWT oqimini (imzo va issuer validatsiyasi bilan) bosib o'tadi, qolganlari `jwt()`/`opaqueToken()` post-processor'laridan foydalanadi.
- [ ] CSRF, CORS va security header qoidalari hamda sessiya strategiyasi (stateless yoki fixation/concurrent session) test bilan muhrlangan.
- [ ] Tranzaksiya testlari haqiqiy bazada ishlaydi, test metodida `@Transactional` yo'q; `REQUIRES_NEW`, rollback va checked exception xatti-harakati tasdiqlangan.
- [ ] Self-invocation va lock konflikti (optimistik, kerak bo'lsa pessimistik) uchun aniq testlar bor.
- [ ] Asinxron natijalar faqat Awaitility yoki `CountDownLatch` bilan kutiladi; kodbazada `Thread.sleep` ishlatilgan test yo'q.
- [ ] Idempotentlik va race condition testlari `@Tag` bilan ajratilgan, alohida CI job'da yurgiziladi va beqaror holda qoldirilmagan.
- [ ] Retry urinishlari soni, circuit breaker holati va fallback xatti-harakati test bilan tasdiqlangan; penetration test, SAST va DAST alohida reja sifatida yozilgan (13-bob).

---

## 12. End-to-end va UI testlar (End-to-End & UI Testing)

End-to-end (E2E) va UI testlar test piramidasining eng yuqori, eng sekin va saqlashi eng qimmat qatlami: ular tizimni foydalanuvchi ko'rgan holida — brauzer, HTTP, ma'lumotlar bazasi, navbat, reverse proxy va tashqi sandbox'lar bilan birgalikda — tekshiradi. Arxitektor bu qatlamdan qamrov emas, ishonch kutadi: deploy qilingan tizim pul keltiruvchi asosiy yo'llarni haqiqatan bajara oladimi. Shu sababli E2E to'plam kichik, ataylab tanlangan va texnik jihatdan juda barqaror bo'lishi shart. Bu bobda qancha E2E test kerakligi, vosita tanlash mezonlari, barqaror test yozish qoidalari, nosozlikni tahlil qilish artefaktlari va smoke to'plamning deploy quvuridagi o'rni ko'rib chiqiladi.

### 12.1 E2E testning o'rni va narxi

E2E test faqat bitta savolga yaxshi javob beradi: "alohida sinovdan o'tgan bo'laklar birgalikda ishlaydimi?". Bu savol arzimas emas — eng qimmat production incident'lari ko'pincha mantiq xatosi emas, balki wiring xatosi bo'ladi: noto'g'ri profil, ishga tushmagan Flyway migratsiya, yetishmayotgan environment variable, CORS va cookie `SameSite` sozlamasi, Spring Security filter zanjiridagi tartib, gateway'dagi timeout, JSON serializatsiyadagi sana formati. Bularning hech birini unit test ko'rmaydi, chunki ularning har biri aynan "hamma narsa birga ko'tarilganda" paydo bo'ladi.

Narx tomoni ham aniq. Bitta unit test millisekundlar, integration test (Testcontainers bilan) sekundlar, UI orqali o'tadigan E2E senariy esa odatda 20-120 sekund oladi. Bunga brauzer konteynerlari, test muhitini tiklash va nosozlikni qayta tekshirish vaqti qo'shiladi. Diagnostika qiymati past: qizil E2E test "biror joyda buzildi" deydi, qaysi komponent aybdorini aytmaydi. Saqlash narxi ham yuqori — frontend'dagi har bir refactoring locator'larni buzadi.

Shu sababli miqdor cheklanadi. Amaliy mo'ljal: o'rta kattalikdagi mahsulot uchun 15-40 ta E2E senariy, ulardan 5-10 tasi smoke to'plamda. Statistika buni majburlaydi: agar har bir test 1% ehtimol bilan "sababsiz" uzilsa, 20 testlik to'plam uchun muvaffaqiyat ehtimoli 0.99^20 ≈ 0.82 bo'ladi, ya'ni har beshinchi ishga tushirish asossiz qizil. 100 testda esa bu ko'rsatkich 0.37 ga tushadi va hech kim natijaga ishonmaydi. Demak E2E qatlamda flakiness byudjeti test soniga teng darajada muhim resurs.

Har bir E2E test uchun arxitektor bitta savolga javob talab qilishi kerak: "bu test uzilsa, qaysi daromad yoki majburiyat yo'li to'xtaydi?". Javob bo'lmasa, test pastroq qatlamga ko'chiriladi.

### 12.2 Qaysi senariylarni E2E qilish kerak

E2E qilinadigan senariylar ro'yxati qisqa va biznesga bog'langan bo'ladi:

- **Pul oqimi**: savatdan to'lovga, to'lovdan tasdiqlangan buyurtmaga qadar to'liq yo'l, shu qatorda to'lov provayderi webhook'i kelgandan keyingi holat o'zgarishi.
- **Ro'yxatdan o'tish va kirish**: signup, email tasdiqlash, login, parol tiklash, sessiya muddati tugashi. Bu yo'l uzilsa qolgan hamma narsa ahamiyatsiz.
- **Buyurtma yakunlash va bekor qilish**: inventar zaxirasi, yetkazib berish manzili, qaytarish (refund) yo'li.
- **Kritik hisobot va eksport**: oylik moliyaviy hisobot, PDF/Excel eksport — ko'pincha alohida servis, alohida template engine va alohida permission qatlamidan o'tadi.
- **Rollar bo'yicha bitta-bittadan asosiy yo'l**: admin va oddiy foydalanuvchi uchun bittadan "happy path".

E2E qilinmasligi kerak bo'lgan narsalar ro'yxati esa ancha uzun: forma validatsiyasi, chegara qiymatlari (minimal/maksimal summa, uzunlik), xato matnlari va tarjimalar, hisob-kitob formulalari (chegirma, soliq, valyuta konvertatsiyasi), rol va huquq kombinatsiyalarining to'liq matritsasi, sahifalash va saralash variantlari, retry va timeout mantig'i. Bularning barchasi unit yoki `@WebMvcTest` / slice qatlamida bir necha yuz marta tezroq va ishonchliroq tekshiriladi. Qoida sifatida: UI orqali bir xil sahifani har xil parametrlar bilan qayta-qayta o'tkazish — E2E'ni funksional test deb ishlatishning eng keng tarqalgan shakli va eng qimmat xatosi.

### 12.3 API darajasidagi E2E

E2E'ning eng foydali shakli ko'pincha brauzersiz bo'ladi: butun ilovani haqiqiy portda ko'tarib, haqiqiy ma'lumotlar bazasi va broker bilan, senariyni HTTP orqali o'tkazish. Bu brauzer qatlamidan tashqari deyarli hamma integratsiya xatosini topadi, lekin 10-20 marta tezroq va bir necha marta barqarorroq ishlaydi. Spring'da uchta variant mavjud: `TestRestTemplate` (eng oddiy, blocking), `WebTestClient` (reactive stack yoki fluent assertion kerak bo'lsa) va `RestAssured` (eng o'qiluvchan DSL, JSON path assertion'lari kuchli).

```java
@SpringBootTest(webEnvironment = WebEnvironment.RANDOM_PORT)
@Testcontainers
class CheckoutApiE2ETest {

    @Container @ServiceConnection
    static PostgreSQLContainer<?> db = new PostgreSQLContainer<>("postgres:16-alpine");

    @LocalServerPort int port;

    @BeforeEach
    void setUp() { RestAssured.port = port; RestAssured.basePath = "/api"; }

    @Test
    void customerCanPayForOrder() {
        String token = TestUsers.signUpAndLogin("e2e-" + UUID.randomUUID() + "@shop.io");
        long orderId = given().contentType(JSON).auth().oauth2(token)
                .body(Map.of("sku", "SKU-1", "qty", 2))
                .post("/orders").then().statusCode(201)
                .extract().jsonPath().getLong("id");

        given().contentType(JSON).auth().oauth2(token)
                .body(Map.of("card", "4242424242424242"))
                .post("/orders/{id}/payment", orderId)
                .then().statusCode(200)
                .body("status", equalTo("PAID"))
                .body("paidAt", notNullValue());
    }
}
```

Bu yerda `@ServiceConnection` (Spring Boot 3.1+) konteyner URL'ini avtomatik `DataSource`ga bog'laydi, `@LocalServerPort` esa haqiqiy tasodifiy portni beradi — ya'ni so'rov to'liq Tomcat, filter zanjiri, controller va tranzaksiya qatlamidan o'tadi. Amaliy taqsimot: biznes senariylarining 70-80% ini API darajasida, faqat qolganini brauzerda tekshirish. UI qatlamiga esa faqat "foydalanuvchi haqiqatan bosib o'tadigan" yo'llar qoldiriladi.

### 12.4 UI avtomatlashtirish vositalari

| Vosita | Til / bog'lanish | Auto-wait | Tezlik | Barqarorlik | Debug artefaktlari | Parallel | Qachon tanlash |
|---|---|---|---|---|---|---|---|
| Selenium 4.x WebDriver | Java, Python, C#, JS | Yo'q (`WebDriverWait` qo'lda) | O'rta | O'rta (qo'lda kutishga bog'liq) | Screenshot, Grid video, BiDi/CDP log | Grid orqali yaxshi | Mavjud Grid, keng brauzer/legacy qamrov, real device cloud |
| Playwright for Java | Java (+ TS, Python, .NET) | Ha, web-first assertion | Yuqori | Yuqori | Trace viewer, video, HAR, console | JUnit 5 + context'lar bilan yaxshi | Yangi loyiha, tez va barqaror UI suite kerak |
| Selenide | Faqat Java (Selenium ustida) | Ha (`should*` kutadi) | O'rta-yuqori | Yuqori | Avto-screenshot, sodda hisobot | Grid orqali yaxshi | Java jamoasi Selenium ekosistemasida qolishni xohlasa |
| Cypress | Faqat JS/TS | Ha | Yuqori | Yuqori | Time-travel debug, video | Cloud/orkestratsiya bilan | Testlar frontend jamoasi qo'lida bo'lsa |

Tanlov mezonlari texnik emas, tashkiliy: **testlarni kim saqlaydi?** Agar E2E'ni backend/QA Java jamoasi yozsa, Playwright for Java yoki Selenide tanlanadi — bitta build, bitta CI, bitta dependency daraxti. Agar testlar frontend jamoasining mas'uliyatida bo'lsa, Cypress yoki Playwright'ning TypeScript runner'i mantiqiyroq, chunki u yerda snapshot assertion va fixture modeli kuchliroq. Yangi Java loyihasi uchun standart tavsiya: **Playwright for Java** — auto-wait va trace viewer flaky testlar bilan kurashda eng katta foyda beradi. Selenium esa zarur bo'lib qoladi, agar sizga Appium, real qurilma cloud'i yoki juda keng brauzer matritsasi kerak bo'lsa.

### 12.5 Page Object va Screenplay patternlari

Page Object — UI test kodining eng muhim abstraksiyasi: locator va o'zaro ta'sir detallari bitta klassda yashaydi, test esa faqat biznes tilida gapiradi. Qoida: Page Object assertion'lar bilan to'lib ketmasligi kerak, lekin "sahifa yuklandi" darajasidagi tekshiruvni o'zida ushlashi normal.

```java
public class LoginPage {
    private final Page page;

    public LoginPage(Page page) { this.page = page; }

    public LoginPage open() {
        page.navigate("/login");
        return this;
    }

    public CheckoutPage loginAs(String email, String password) {
        page.getByTestId("login-email").fill(email);
        page.getByTestId("login-password").fill(password);
        page.getByTestId("login-submit").click();
        assertThat(page.getByTestId("user-menu")).isVisible();
        return new CheckoutPage(page);
    }

    public String errorMessage() {
        return page.getByTestId("login-error").innerText();
    }
}
```

```java
public class CheckoutPage {
    private final Page page;
    private final Locator total;

    public CheckoutPage(Page page) {
        this.page = page;
        this.total = page.getByTestId("cart-total");
    }

    public CheckoutPage payWithTestCard() {
        page.getByTestId("card-number").fill("4242424242424242");
        page.getByTestId("pay-now").click();
        return this;
    }

    public void shouldBePaid(String expectedTotal) {
        assertThat(total).hasText(expectedTotal);
        assertThat(page.getByTestId("order-status")).hasText("PAID");
    }
}
```

Katta suite'larda Page Object klasslari 500 qatorga o'sib ketadi. Bunga yechim — **komponent darajasidagi abstraksiya**: `CartWidget`, `AddressForm`, `DataTable` kabi klasslar o'z ildiz `Locator`ini qabul qiladi (`page.getByTestId("cart")`) va ichida nisbiy qidiradi. Shunda bir xil komponent bir necha sahifada qayta ishlatiladi.

**Screenplay** pattern (Serenity BDD'da `Actor`, `Performable`, `Question`) bir qadam uzoqroq boradi: sahifa emas, foydalanuvchi vazifalari modellashtiriladi — `actor.attemptsTo(Login.withCredentials(user), Checkout.withTestCard())`. Bu ko'p rolli, ko'p foydalanuvchili senariylarda (masalan sotuvchi va xaridor bir senariyda) Page Object'dan toza chiqadi, lekin o'rganish narxi yuqori. Tavsiya: 30 testdan kichik suite uchun Page Object yetarli; ko'p aktyorli murakkab domenda Screenplay'ni ko'rib chiqing.

Locator strategiyasi barqarorlikning yarmi: birinchi tanlov — `data-testid` (dizayn o'zgarishidan himoyalangan, frontend bilan shartnoma sifatida kelishiladi), ikkinchi — `getByRole` va accessible name (bir vaqtda accessibility'ni ham tekshiradi), uchinchi — matn. XPath va uzun CSS zanjirlari (`div > div:nth-child(3) > span`) taqiqlanadi: ular DOM tuzilishiga bog'lanadi va har markup o'zgarishida buziladi. Playwright'da test atribut nomi `playwright.selectors().setTestIdAttribute("data-qa")` bilan moslashtiriladi.

### 12.6 Barqaror UI test yozish qoidalari

- **`Thread.sleep` qat'iy taqiqlanadi.** U yo testni sekinlashtiradi, yo sekin CI'da yetmaydi. Faqat auto-wait (`assertThat(locator).isVisible()`, Selenide'dagi `shouldBe`) yoki aniq shartga bog'langan kutish ishlatiladi: `page.waitForResponse("**/api/orders", () -> ...)`, `locator.waitFor()`.
- **Timeout bitta joyda sozlanadi**, test ichida emas: global `setDefaultTimeout` va faqat haqiqatan sekin operatsiya uchun lokal override.
- **Retry faqat infratuzilma uchun.** Konteyner ko'tarilmasligi, DNS, tarmoq uzilishi — qayta urinishga arziydi. Biznes senariyning o'zini retry qilish xatoni yashiradi (flaky testlar jarayoni 16-bobda).
- **Har test o'z ma'lumotini API orqali yaratadi** va unique identifikator ishlatadi (`"e2e-" + UUID.randomUUID() + "@shop.io"`). Shunda testlar bir-biriga ta'sir qilmaydi va parallel ishlaydi.
- **Testlar idempotent bo'ladi**: ikki marta ketma-ket ishga tushirilsa, bir xil natija berishi shart. Umumiy, oldindan tayyorlangan "demo" akkauntga bog'lanish parallel bajarishni darhol buzadi.
- **Kirish sessiyasi qayta ishlatiladi.** Har testda login UI orqali o'tish 5-15 sekundni behuda sarflaydi va eng mo'rt qadamni har testga ko'paytiradi. Playwright'da yechim — `storageState`.

```java
public final class AuthState {
    private static final Path STATE = Path.of("target/e2e/admin-state.json");

    public static synchronized Path adminState(Browser browser, String baseUrl) {
        if (Files.exists(STATE)) return STATE;
        try (BrowserContext ctx = browser.newContext(
                new Browser.NewContextOptions().setBaseURL(baseUrl))) {
            Page page = ctx.newPage();
            page.navigate("/login");
            page.getByTestId("login-email").fill(System.getenv("E2E_ADMIN_USER"));
            page.getByTestId("login-password").fill(System.getenv("E2E_ADMIN_PASS"));
            page.getByTestId("login-submit").click();
            assertThat(page.getByTestId("user-menu")).isVisible();
            ctx.storageState(new BrowserContext.StorageStateOptions().setPath(STATE));
        }
        return STATE;
    }
}
```

Keyin har test `browser.newContext(new Browser.NewContextOptions().setStorageStatePath(AuthState.adminState(...)))` bilan allaqachon kirgan holda boshlanadi. Login yo'lining o'zi esa alohida, bitta aniq test bilan tekshiriladi.

### 12.7 Test muhiti va ma'lumot

E2E uchun to'g'ri muhit — production bilan bir xil artefaktdan deploy qilingan, alohida ma'lumotlar bazasiga ega va faqat avtomatlashtirilgan testlar uchun ajratilgan `e2e` muhiti. Qo'l bilan sinovdan o'tkaziladigan staging bilan birga ishlatish flakiness'ning birinchi sababi: kimdir ma'lumotni o'zgartiradi va test tushadi.

Ma'lumot tayyorlashda tartib shunday: birinchi navbatda **ilovaning o'z API'si** orqali (haqiqiy validatsiya va domen qoidalaridan o'tadi, shartnoma o'zgarsa test ham o'zgaradi), API erisha olmaydigan holatlar uchun (muddati o'tgan obuna, arxivlangan buyurtma) esa faqat `e2e` profilida yoqiladigan **test-support endpoint**lari. To'g'ridan-to'g'ri SQL eng oxirgi chora: u sxemaga bog'lanadi, migratsiyadan keyin jimgina buziladi va domen invariantlarini chetlab o'tib, real bo'lmagan holat yaratadi.

```yaml
spring:
  config:
    activate:
      on-profile: e2e
  datasource:
    url: jdbc:postgresql://db:5432/shop_e2e
app:
  payments:
    provider: stripe
    mode: test                     # provayderning sandbox rejimi
    secret-key: ${STRIPE_TEST_SK}
    webhook-endpoint: /api/payments/webhook
  features:
    new-checkout: true             # feature flag bilan senariy holatini boshqarish
    email-sending: false           # SMTP o'rniga in-memory sink
  test-support:
    seed-endpoints-enabled: true   # faqat e2e profilida
```

Feature flag'lar E2E uchun ikki tomonlama foyda beradi: yangi yo'lni testda yoqib, production'da o'chirib turish mumkin; va flag holatini test boshida HTTP header yoki admin endpoint orqali o'rnatib, deterministik senariy olinadi. Tashqi to'lov tizimi esa albatta o'z sandbox'ida ishlatiladi (test kalitlari, provayderning e'lon qilgan test karta raqamlari), lekin webhook yetib kelishini kutish uchun testda aniq shart bo'yicha polling kerak — "sleep qilib umid qilish" emas. Barqarorligi past yoki pullik tashqi servislar E2E'da chegara adapteri darajasida stub bilan almashtiriladi.

### 12.8 Parallel bajarish va vaqt byudjeti

E2E suite uchun vaqt byudjeti oldindan e'lon qilinadi: smoke 2-5 daqiqa, to'liq suite 15-20 daqiqa. Byudjet buzilganda testlar qo'shilmaydi — ular qisqartiriladi yoki pastroq qatlamga ko'chiriladi.

Byudjetga erishishning uch vositasi bor. Birinchi — **suite ichidagi parallelizm**: JUnit 5'da `junit-platform.properties` orqali `junit.jupiter.execution.parallel.enabled=true`, `junit.jupiter.execution.parallel.mode.classes.default=concurrent` va `...config.fixed.parallelism=4`. Bu faqat testlar bir-biridan mustaqil ma'lumot ishlatganda ishlaydi. Ikkinchi — **sharding**: testlarni `@Tag` bo'yicha domenlarga bo'lib, CI matritsasida parallel joblar sifatida ishga tushirish. Uchinchi — **brauzer konteynerlari**: Selenium Grid 4 (hub + node-chrome), Testcontainers'ning `BrowserWebDriverContainer` (video yozish bilan) yoki Playwright'ning rasmiy `mcr.microsoft.com/playwright/java:v<versiya>-jammy` image'i — bu oxirgisi lokal va CI o'rtasida bir xil brauzer/font muhitini kafolatlaydi.

```yaml
e2e:
  runs-on: ubuntu-latest
  timeout-minutes: 20
  strategy:
    fail-fast: false
    matrix:
      shard: [auth, checkout, reporting]
  steps:
    - uses: actions/checkout@v4
    - uses: actions/setup-java@v4
      with: { distribution: temurin, java-version: '21', cache: maven }
    - run: mvn -B verify -Pe2e -Dgroups=${{ matrix.shard }}
      env:
        E2E_BASE_URL: ${{ secrets.E2E_BASE_URL }}
    - if: failure()
      uses: actions/upload-artifact@v4
      with:
        name: e2e-artifacts-${{ matrix.shard }}
        path: |
          target/e2e/**/*.zip
          target/e2e/**/*.png
```

Har test uchun qattiq timeout ham qo'yiladi (`junit.jupiter.execution.timeout.test.method.default=3m`), aks holda osilib qolgan bitta test butun job'ni CI limitiga qadar band qiladi.

### 12.9 Nosozlikni tahlil qilish

E2E testning qiymati uning nosozlik hisobotining sifati bilan belgilanadi. "Expected PAID but was NEW" degan xabar hech narsa bermaydi. Minimal artefakt to'plami: uzilish paytidagi to'liq sahifa screenshot'i, video yoki trace, brauzer console va network log'i, server tomonidagi ilova log'i va test identifikatorini so'rovlar bilan bog'lovchi korrelyatsiya header'i (`X-E2E-Test-Id`, yoki `traceparent`).

```java
public class PlaywrightArtifacts implements TestWatcher {

    @Override
    public void testFailed(ExtensionContext ctx, Throwable cause) {
        PwFixture pw = PwFixture.current(ctx);
        Path dir = Path.of("target/e2e", ctx.getRequiredTestClass().getSimpleName());
        String name = ctx.getDisplayName().replaceAll("\\W+", "_");

        pw.page().screenshot(new Page.ScreenshotOptions()
                .setPath(dir.resolve(name + ".png")).setFullPage(true));
        pw.context().tracing().stop(new Tracing.StopOptions()
                .setPath(dir.resolve(name + "-trace.zip")));
        pw.dumpConsoleAndNetwork(dir.resolve(name + "-browser.log"));
        pw.copyServerLogs(dir.resolve(name + "-app.log"));
    }

    @Override
    public void testSuccessful(ExtensionContext ctx) {
        PwFixture.current(ctx).context().tracing()
                .stop(new Tracing.StopOptions());   // artefakt saqlanmaydi
    }
}
```

Tracing test boshida `context.tracing().start(new Tracing.StartOptions().setScreenshots(true).setSnapshots(true).setSources(true))` bilan yoqiladi. Playwright trace viewer (`npx playwright show-trace trace.zip` yoki `trace.playwright.dev`) har qadamni DOM snapshot, network va console bilan ko'rsatadi — bu flaky testni tashxislashda eng kuchli vosita. Selenium tomonida ekvivalenti: `BrowserWebDriverContainer.withRecordingMode(VncRecordingMode.RECORD_FAILING, dir)` bilan video va BiDi/CDP orqali log yig'ish. Artefaktlar CI'da har shard uchun alohida yuklanadi va kamida bir necha hafta saqlanadi.

### 12.10 Vizual regressiya testlash

Vizual regressiya screenshot'ni ma'lum (baseline) rasm bilan piksel darajasida taqqoslaydi. U funksional test topa olmaydigan xatolarni ko'radi: buzilgan CSS, ustma-ust tushgan elementlar, yo'qolgan logotip, dark mode'da o'qilmaydigan matn.

Flakiness sabablari deyarli har doim bir xil: font yuklanishi va antialiasing (OS'ga bog'liq), animatsiya va `transition`, kursor miltillashi, scrollbar, dinamik ma'lumot (sana, ID, avatar), va viewport o'lchamining o'zgarishi. Shuning uchun qoidalar qat'iy: baseline faqat CI bilan **bir xil Docker image**da generatsiya qilinadi; animatsiya `page.addStyleTag` bilan o'chiriladi (`*, *::before { animation: none !important; transition: none !important; }`); vaqt va dinamik bloklar mask qilinadi yoki fixture bilan muzlatiladi; tolerance esa 0 emas, lekin juda kichik (0.1-0.5% piksel) bo'ladi — katta tolerance haqiqiy regressiyani yashiradi.

Java ekosistemasida tayyor snapshot assertion yo'q: Playwright'ning `toHaveScreenshot` imkoniyati faqat TypeScript runner'ida. Java uchun amaliy variantlar — `ashot` kutubxonasi (Selenium bilan), Applitools Eyes yoki Percy kabi cloud SDK'lar (AI/DOM asosida farqlarni filtrlaydi), yoki frontend tomonida Storybook + BackstopJS. Eng oqilona qarori: vizual testni E2E senariylaridan ajratish va komponent galereyasi darajasida ishlatish — u yerda sahifa holati deterministik, baseline'lar esa arzon.

### 12.11 Mobil va cross-browser

Brauzer matritsasi analitika bilan asoslanadi, "har ehtimolga qarshi" bilan emas. Amaliy model: har PR'da faqat Chromium; kechasi (nightly) Firefox va WebKit qo'shiladi; legacy brauzerlar faqat real foydalanuvchi ulushi bo'lsa. Playwright bitta API bilan uchta engine'ni beradi, bu matritsani kengaytirishni arzonlashtiradi.

Responsive tekshiruv alohida E2E senariy emas: bir necha asosiy sahifani belgilangan breakpoint viewport'larida (masalan 390x844, 768x1024, 1440x900) ochib, kritik elementlar ko'rinishini va bosilishini tasdiqlash yetarli. Playwright'da `new Browser.NewContextOptions().setViewportSize(390, 844).setHasTouch(true)` yoki `playwright.devices()` dan qurilma deskriptori ishlatiladi.

Native mobil ilova — bu butunlay boshqa suite. Appium 2.x (`java-client`, UiAutomator2 va XCUITest drayverlari) web E2E bilan bir xil Page Object yondashuvini qo'llaydi, lekin o'z infratuzilmasi (emulyator yoki real device cloud), o'z vaqt byudjeti va o'z mas'ul jamoasini talab qiladi. Uni web E2E quvuriga qo'shmaslik kerak: deploy'ni 40 daqiqalik emulyator jobiga bog'lab qo'yish mahsulot tezligini o'ldiradi.

### 12.12 Smoke suite

Smoke to'plam — deploy'dan keyin darhol ishga tushadigan, 2-5 daqiqada tugaydigan 5-10 senariy: tizim tirikmi, login ishlaydimi, asosiy sahifa ma'lumot bilan yuklanadimi, bitta buyurtma to'lanadimi, kritik hisobot generatsiya bo'ladimi. Bu to'plam `@Tag("smoke")` bilan belgilanadi va deploy quvurining gate'i bo'ladi: qizil bo'lsa, release avtomatik rollback qilinadi yoki trafik yangi versiyaga o'tkazilmaydi.

Smoke senariylari production'da ham xavfsiz bo'lishi uchun ular ko'proq o'qishga tayanadi, bitta yozuv operatsiyasi esa ajratilgan test akkaunt va test to'lov usuli bilan bajariladi hamda o'zidan keyin tozalanadi. Aynan shu senariylar keyinchalik production'da **synthetic monitoring** probe'lari sifatida qayta ishlatiladi — har 5 daqiqada ishlaydigan, alert'ga bog'langan tashqi tekshiruvlar (batafsil 15-bobda). Bitta senariy ta'rifini CI gate va synthetic monitoring o'rtasida bo'lishish — bu qatlamdan olinadigan eng yuqori qaytim.

### 12.13 Anti-patternlar

- **Biznes qoidalarini E2E bilan qoplash.** Chegirma formulasi yoki soliq hisobi UI orqali 40 senariyda tekshirilganda, suite sekin va mo'rt bo'ladi, xato joyi esa noaniq qoladi. Bu mantiq unit testga tegishli.
- **UI test ichida SQL bilan ma'lumotni "tuzatish".** Test o'rtasida `UPDATE orders SET status='PAID'` yozilsa, test real bo'lmagan holatni tekshiradi va sxema o'zgarishida jimgina buziladi. Ma'lumot API yoki ajratilgan test-support endpoint orqali tayyorlanadi.
- **Umumiy akkauntdan foydalanish.** Barcha testlar bitta `qa@company.com` bilan ishlasa, parallelizm imkonsiz, natijalar esa ishga tushirish tartibiga bog'lanib qoladi.
- **Barcha E2E testni har PR'da ishga tushirish.** Bu feedback'ni 30-40 daqiqaga cho'zadi va jamoani "qizilni e'tiborsiz qoldirish" madaniyatiga olib keladi. PR'da smoke + o'zgargan domen shard'i, to'liq suite esa merge'dan keyin yoki nightly.
- **Flaky testni retry bilan yashirish.** `rerunFailingTestsCount=3` statistikani yaxshilaydi, lekin haqiqiy race condition va noto'g'ri kutishni ko'rinmas qiladi — ya'ni production xatosini test bilan to'laydi.
- **Baseline'ni ko'r-ko'rona yangilash.** Vizual test qizil bo'lganda baseline'ni avtomatik qabul qilish vizual testni butunlay bekor qiladi.
- **Page Object'ni assertion ombori qilish.** Sahifa klassi ichida o'nlab biznes tekshiruvi bo'lsa, senariy niyati kodda ko'rinmaydi va qayta ishlatish yo'qoladi.

### 12.14 Arxitektor nazorat ro'yxati

- [ ] E2E senariylar soni cheklangan (15-40) va har biri aniq biznes/daromad yo'liga bog'langan; ro'yxat yozilib qo'yilgan.
- [ ] Biznes mantiqning asosiy qismi API va slice darajasida qoplangan; UI E2E faqat foydalanuvchi yo'lini tekshiradi.
- [ ] Barcha locator'lar `data-testid` yoki accessible role asosida; XPath va chuqur CSS zanjirlari CI'da taqiqlangan.
- [ ] Kodda `Thread.sleep` yo'q; kutish faqat auto-wait yoki aniq shart bilan amalga oshiriladi.
- [ ] Har test o'z ma'lumotini API orqali, unique identifikator bilan yaratadi; umumiy akkaunt va test tartibiga bog'liqlik yo'q.
- [ ] Nosozlikda screenshot, trace/video, brauzer va server log'lari avtomatik yig'iladi va CI artefakti sifatida saqlanadi.
- [ ] Smoke to'plam 5 daqiqadan oshmaydi, deploy gate'iga ulangan va synthetic monitoring bilan senariylarni bo'lishadi.
- [ ] To'liq suite uchun vaqt byudjeti e'lon qilingan, sharding va parallelizm sozlangan, retry faqat infratuzilma xatolari uchun ruxsat etilgan.

---

## 13. Nofunksional testlar: performance, resilience, xavfsizlik (Non-Functional Testing)

Funksional testlar "nima ishlaydi" degan savolga javob beradi, nofunksional testlar esa "qanday sharoitda va qancha vaqt ishlaydi" degan savolga. Arxitektor uchun aynan ikkinchi savol qimmatroq: tizim to'g'ri javob qaytarsa ham, 2 sekundda qaytarsa yoki ma'lumotlar bazasi pool'i tugab qolsa, biznes uchun bu nosozlik. Bu bobda performance, resilience va xavfsizlik testlarini o'lchanadigan talablardan boshlab, CI'dagi darvozalargacha va ishlab chiqarishdagi kuzatuvgacha bog'laymiz. Maqsad — alohida "yuklama tekshiruvi" marosimi emas, balki muhandislik jarayonining doimiy qismi.

### 13.1 Nofunksional talablarni o'lchanadigan qilib yozish

"Tizim tez ishlashi kerak" — bu talab emas, orzu. Uni test qilib bo'lmaydi, demak u hech qachon buzilmaydi va hech qachon bajarilmaydi. O'lchanadigan talab to'rt elementdan iborat: metrika, chegara, yuklama konteksti va xato darajasi. Masalan: "`POST /api/orders` uchun p95 < 300 ms va p99 < 800 ms, 500 RPS doimiy yuklamada, 5xx ulushi < 0,1%, 30 daqiqa davomida". Bunday yozuvni Gatling assertion'iga yoki k6 threshold'iga to'g'ridan-to'g'ri ko'chirish mumkin — bu asosiy mezon: talabni kodga aylantirib bo'lmasa, talab tugallanmagan.

Bu yerda SLI, SLO va error budget tushunchalari yordam beradi. SLI — o'lchanadigan signal (muvaffaqiyatli so'rovlar ulushi, p95 kechikish). SLO — SLI uchun maqsadli qiymat ma'lum oyna ichida (masalan, 30 kunda availability 99,9%). Error budget — SLO'dan qolgan "ruxsat etilgan nosozlik" (99,9% uchun oyda ~43 daqiqa). Arxitektor uchun error budget boshqaruv vositasi: budget tugayotgan bo'lsa, yangi funksiya emas, ishonchlilik ishlari birinchi o'ringa chiqadi. Performance testlardagi chegaralar SLO'dan kelib chiqishi kerak, aks holda CI'da "qizil" bo'lgan test biznes uchun hech narsani anglatmaydi.

### 13.2 Performance test turlari

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

### 13.3 Vositalar: Gatling, k6, JMeter, Locust

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

### 13.4 Amaliy senariy: Gatling va k6

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

### 13.5 To'g'ri o'lchash metodikasi

Noto'g'ri o'lchov noto'g'ri qarorga olib keladi, shuning uchun metodika vositadan muhimroq. Birinchi qoida — **warm-up**. JVM C2 kompilyatori qaynoq kodni optimizatsiya qilishi uchun minglab chaqiruv kerak; shuningdek connection pool to'ladi, Hibernate metadata va cache isiydi. Shu sababli birinchi 1-3 daqiqa natijasini hisobdan chiqaring (Gatling'da alohida warm-up senariysi, k6'da `--no-summary` bilan oldindan yuritish yoki natijani time range bo'yicha kesish).

Ikkinchi qoida — **o'rtacha qiymatni unutish**. O'rtacha 120 ms bo'lgan tizimda p99 4 sekund bo'lishi mumkin va aynan shu 1% foydalanuvchi shikoyat qiladi. p50/p95/p99 va maksimum birga ko'riladi; persentillarni bir nechta injector natijasida "o'rtalashtirish" matematik jihatdan xato — HdrHistogram kabi birlashtiriladigan histogram ishlating yoki serverdagi Micrometer histogramiga tayaning.

Uchinchi qoida — **coordinated omission**. Closed model'da (fiksirlangan VU soni, har biri javobni kutadi) server sekinlashsa, yuklama ham o'z-o'zidan kamayadi va sekin so'rovlar o'lchovga tushmaydi — natija haqiqatdan chiroyliroq ko'rinadi. Yechim: arrival-rate / open model (`injectOpen`, `ramping-arrival-rate`) va so'rov yuborilishi kerak bo'lgan vaqtdan boshlab o'lchash.

To'rtinchi qoida — **bitta o'zgaruvchi**. Har bir testda faqat bitta narsa o'zgarsin: yoki yuklama, yoki pool hajmi, yoki JVM flag. Ikkitasini birga o'zgartirsangiz, natijani talqin qila olmaysiz. GC ta'siri shu yerda ko'rinadi: G1 bilan ZGC'ni taqqoslayotganda heap hajmi va yuklama bir xil bo'lishi shart.

Beshinchi qoida — **ishlab chiqarishga o'xshash muhit va ma'lumot hajmi**. 10 000 qatorli jadvalda index'siz query 2 ms, 50 million qatorda 4 sekund. CPU limiti, replica soni, tarmoq topologiyasi, TLS, ingress va feature flag'lar ham prod'dagiday bo'lishi kerak. Farqlar bo'lsa, ularni test hisobotida ochiq yozing.

### 13.6 Yuklama ostida nimani kuzatish

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

### 13.7 Profiling va diagnostika

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

### 13.8 Virtual thread va reactive stack'ni yuklama ostida taqqoslash

Java 21'dan virtual thread (`spring.threads.virtual.enabled=true`, Spring Boot 3.2+) blocking kodni saqlab turib yuqori konkurensiyaga erishish imkonini berdi; reactive stack (WebFlux) esa boshqa programmatik model taklif qiladi. Taqqoslashda xato qilish juda oson.

O'lchash kerak bo'lgan narsalar: bir xil SLO ostida maksimal throughput; p99 (o'rtacha emas); CPU va xotira birligiga to'g'ri keladigan RPS; thread/stack xotirasi; ulanish pool'ining to'yinish nuqtasi; downstream sekinlashganda tizim xatti-harakati (bu eng muhimi). Virtual thread downstream sekinlashganda ko'p "arzon" thread yaratadi, lekin ma'lumotlar bazasi pool'i hali ham 20 ta ulanish bilan cheklangan — ya'ni bottleneck ko'chadi, yo'qolmaydi. Reactive stack'da esa backpressure to'g'ri sozlanmagan bo'lsa queue cheksiz o'sadi.

Odatiy xatolar: (1) virtual thread testida `synchronized` bloklar sababli pinning — Java 21-23'da bu carrier thread'ni band qiladi; JDK 24'dan (JEP 491) `synchronized` endi pinning qilmaydi, lekin native/JNI chaqiruv va `Object.wait` hali ham muammo bo'lishi mumkin. Pinning'ni JFR'dagi `jdk.VirtualThreadPinned` hodisasi bilan tekshiring, taxmin qilmang. (2) Reactive zanjirning o'rtasida blocking JDBC chaqiruvi — event loop thread bloklanadi va butun tizim qulaydi; `BlockHound` bilan test muhitida aniqlash mumkin. (3) Thread pool o'lchamlarini bir xil qoldirib taqqoslash. (4) Faqat "salom dunyo" endpoint'ida o'lchash — real senariyda ma'lumotlar bazasi va tashqi servis bo'lishi shart. Arxitektorning xulosasi ko'pincha shunday bo'ladi: ikkala stack ham yetarli, tanlov jamoaning tajribasi, debug qulayligi va kutubxona ekosistemasiga bog'liq — raqamlar farqi esa bottleneck ma'lumotlar bazasida bo'lganda deyarli ko'rinmaydi.

### 13.9 Resilience va chaos testing

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

### 13.10 Xavfsizlik testlash turlari

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

### 13.11 Penetration test va bug bounty

Avtomatik skanerlar ma'lum naqshlarni topadi; penetration test biznes mantig'idagi zaifliklarni topadi. "Boshqa foydalanuvchi buyurtmasini `orderId`ni o'zgartirib ko'rish", "chegirma kuponini ikki marta ishlatish", "rol tekshiruvi faqat frontend'da" — bunday narsalarni ZAP topmaydi.

Kim o'tkazadi: tashqi mustaqil jamoa (ichki jamoa o'z tizimini "ko'r nuqta" bilan ko'radi). Qanchalik tez-tez: yiliga kamida bir marta, shuningdek arxitektura yoki autentifikatsiya modeli sezilarli o'zgarganda, yangi tashqi integratsiya yoki yangi to'lov oqimi qo'shilganda. Compliance (PCI DSS, ISO 27001) talablari ham chastotani belgilaydi. Scope va qoidalarni (rate limit, ma'lumot bilan ishlash, test akkauntlari) oldindan yozib qo'yish shart.

Natijani boshqarish: har bir topilma odatdagi backlog ishiga aylanadi, severity bo'yicha SLA belgilanadi (masalan, critical — 7 kun, high — 30 kun), va eng muhimi — har bir topilma uchun **regression test** yoziladi. Agar IDOR topilgan bo'lsa, `@WebMvcTest` yoki integratsiya testida boshqa foydalanuvchi resursiga 403 qaytishini tekshiradigan test paydo bo'lishi kerak. Shunday qilib pentest natijasi hujjat emas, doimiy himoyaga aylanadi. Bug bounty esa doimiy, tashqi, natijaga to'lanadigan kanal: u pentest o'rnini bosmaydi, balki "uzoq dum"dagi zaifliklarni topadi va faqat ichki jarayon yetilgan (triage, SLA, aloqa) jamoalarda ma'noga ega.

### 13.12 OWASP Top 10'ni test bilan qoplash

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

### 13.13 Accessibility (a11y) va yuridik talablar

Agar mahsulotda veb interfeys bo'lsa, accessibility nofunksional talab va ko'p yurisdiksiyalarda yuridik majburiyat. Yevropa Ittifoqida European Accessibility Act, AQShda ADA va davlat sektori uchun Section 508, Yevropa davlat xaridlarida EN 301 549 standarti amal qiladi. Texnik mezon — WCAG (2.1 yoki 2.2) va uning darajalari: A (minimal), AA (amalda standart talab, odatda shartnomalarda shu ko'rsatiladi), AAA (tanlangan kriteriyalar uchun).

Avtomatik tekshiruv: `axe-core` (E2E testlarga `@axe-core/playwright` yoki `@axe-core/cli` orqali qo'shiladi) va Lighthouse / Lighthouse CI. Ular kontrast, `alt` matn yo'qligi, ARIA noto'g'ri ishlatilishi, label'siz forma maydonlari, sarlavha ierarxiyasi kabi narsalarni topadi. Ammo real qoplama cheklangan — avtomatik vositalar WCAG kriteriyalarining taxminan uchdan bir qismini aniqlaydi. Qolgani qo'lda tekshiriladi: faqat klaviatura bilan butun oqimni o'tish (Tab tartibi, focus ko'rinishi, modal'dan chiqish), screen reader (NVDA, VoiceOver) bilan sinash, 200% zoom va matnni kattalashtirishda layout buzilmasligi, rangga bog'liq bo'lmagan ma'no uzatish, xato xabarlarining e'lon qilinishi. Jarayon uchun amaliy yechim: axe tekshiruvini E2E suite'ga qo'shib, yangi "critical" buzilishlarni PR'da to'xtatish, mavjud qarzni alohida backlog'da bosqichma-bosqich yopish va har chorakda qo'lda audit o'tkazish.

### 13.14 Nofunksional testni jarayonga kiritish

Nofunksional testlarning eng ko'p uchraydigan muvaffaqiyatsizlik sababi — noto'g'ri bosqichda ishlatish. Hamma narsani har PR'da ishlatsangiz, pipeline sekinlashadi va o'chirib qo'yiladi; hech narsani ishlatmasangiz, release oldida panika bo'ladi.

| Bosqich | Nima ishlaydi | Vaqt budjeti | Darvozami |
|---|---|---|---|
| Har PR'da | SAST (incremental), SCA, secret scanning, axe critical, 1-2 daqiqalik "smoke performance" (bitta endpoint, past RPS, regression chegarasi) | < 10 daqiqa | Ha, blokirovka |
| Nightly | To'liq load test, ZAP baseline, image va IaC scanning, Lighthouse | 1-2 soat | Ha, lekin merge'ni emas, release'ni bloklaydi |
| Har hafta | Soak (4-12 soat), stress, breakpoint | Tunda / dam olish kuni | Hisobot + trend |
| Release oldidan | Load + spike prod'ga o'xshash muhitda, chaos eksperimentlari, SBOM va litsenziya tekshiruvi | 0,5-1 kun | Ha, release checklist |
| Prod'da | Canary (metrika bo'yicha avtomatik rollback), synthetic monitoring, SLO va error budget kuzatuvi, doimiy JFR | Doimiy | Avtomatik rollback |

Kim ko'radi va qanday qaror qabul qiladi: PR darajasidagi natijani muallif va reviewer ko'radi — qizil bo'lsa, merge bo'lmaydi. Nightly va haftalik natijalar uchun aniq egasi bo'lishi kerak (performance uchun servis jamoasi tech lead'i, xavfsizlik uchun security champion) — "hamma ko'radi" degani "hech kim ko'rmaydi". Trend muhim: bitta test natijasi emas, p95 va p99'ning haftalar bo'yicha o'zgarishi. Qaror mezonlari oldindan yozilgan bo'lsin: SLO buzilishi — release to'xtatiladi; 10% regressiya — tergov ishi ochiladi; critical CVE — belgilangan SLA ichida tuzatiladi; error budget tugadi — yangi funksiyalar to'xtaydi.

### 13.15 Anti-patternlar

**Performance testni release oldidan bir marta o'tkazish.** Natija: muammo topilganda arxitekturani o'zgartirishga vaqt yo'q, shuning uchun "keyingi release'ga" ko'chiriladi. Yechim — har PR'da kichik regression testi, nightly'da to'liq test, trend kuzatuvi.

**Laptop'da o'lchash.** Mahalliy mashinada ma'lumotlar bazasi, ilova va yuklama generatori bir CPU'ni bo'lishadi, tarmoq kechikishi nolga teng, dataset kichik.

**O'rtacha javob vaqtiga qarash.** O'rtacha hech kimning tajribasini aks ettirmaydi. Persentil va maksimum ko'riladi, persentillar o'rtalashtirilmaydi.

**Bir foydalanuvchi bilan "test qilish".** Postman'da bitta so'rov 80 ms qaytargani konkurensiya, pool tanqisligi, lock contention va GC haqida hech narsa aytmaydi.

**Closed model bilan tinch o'lchash** va coordinated omission'ni e'tiborsiz qoldirish — natija sun'iy ravishda chiroyli chiqadi.

**Xavfsizlik skanini "warning" sifatida qoldirish.** Darvoza bo'lmagan skaner natijasi bir-ikki sprintdan keyin minglab ogohlantirishga aylanadi va hech kim o'qimaydi. Yechim: yangi topilmalar bloklaydi, eski qarz muddatli istisno bilan rasmiylashtiriladi.

**Chaos eksperimentini gipotezasiz o'tkazish.** "Pod'ni o'chirdik, hech narsa bo'lmadi" — bu natija emas. Gipoteza, o'lchov va kutilgan xatti-harakat oldindan yozilishi kerak.

**Nofunksional talabni hujjatda qoldirib, kodga ko'chirmaslik.** Agar SLO assertion yoki threshold sifatida mavjud bo'lmasa, u real emas.

### 13.16 Arxitektor nazorat ro'yxati

- [ ] Har bir muhim endpoint uchun o'lchanadigan SLO yozilgan (metrika, persentil chegarasi, RPS, xato ulushi) va u Gatling assertion yoki k6 threshold sifatida kodda mavjud.
- [ ] Yuklama turlari ajratilgan va rejalashtirilgan: load va smoke-performance CI'da, soak va stress jadval bo'yicha, spike muhim voqealar oldidan.
- [ ] O'lchash metodikasi hujjatlashtirilgan: warm-up, open/arrival-rate model, persentillar, prod'ga o'xshash muhit va dataset, bir vaqtda bitta o'zgaruvchi.
- [ ] Yuklama paytida ilova (Micrometer/Actuator), JVM, ma'lumotlar bazasi pool'i va tashqi servis metrikalari Prometheus'ga yoziladi va bitta dashboard'da ko'riladi.
- [ ] Resilience eksperimentlari gipoteza bilan avtomatlashtirilgan (Toxiproxy, Chaos Monkey for Spring Boot) va timeout, retry, circuit breaker, graceful degradation tasdiqlangan; choraklik game day o'tkaziladi.
- [ ] Xavfsizlik to'plami to'liq va to'g'ri bosqichda: SAST va SCA PR'da, secret scanning pre-commit va CI'da, image/IaC scanning build'da, DAST nightly; barcha istisnolar sabab va muddat bilan versiya nazoratida.
- [ ] Pentest yiliga kamida bir marta, har bir topilma uchun severity SLA va regression test mavjud.
- [ ] Natijalar uchun aniq egasi va qaror qoidalari belgilangan (regressiya foizi, error budget holati, CVE SLA), prod'da canary va synthetic monitoring ishlaydi.

---

## 14. Arxitektura testlari va kod sifati darvozalari (Architecture Tests & Code Quality Gates)

Arxitektura faqat hujjatda yashasa, u birinchi muddat siqig'ida o'ladi: diagramma wiki'da qoladi, kod esa boshqa yo'ldan ketadi. Arxitektorning eng arzon va eng ta'sirli vositalaridan biri — qoidani matn sifatida emas, bajariladigan test sifatida yozish va uni kod sifati darvozalari qatoriga qo'yish. Bu bobda ArchUnit va Spring Modulith bilan chegaralarni mustahkamlash, JaCoCo, PIT, statik tahlil va SonarQube darvozalarini sozlash ko'rib chiqiladi. Oxirida esa eng qiyin qism: bu darvozalarni mavjud loyihaga jamoani sindirmasdan joriy qilish.

### 14.1 Qoidani hujjat emas, test qilib yozish

Arxitektura qoidasi uch joyda yashashi mumkin: kimningdir boshida, hujjatda yoki testda. Birinchisi jamoa o'zgarishi bilan yo'qoladi, ikkinchisi oyiga bir marta o'qiladi, uchinchisi har commit'da tekshiriladi. "Controller repository'ni chaqirmaydi" degan jumla wiki'da turganda maslahat, `ArchRule` sifatida yozilganda esa shartnoma.

Code review nega yetarli emas? Reviewer — odam: charchaydi va 900 qatorli PR'da import blokidagi bitta yangi paketni ko'rmaydi. Qoida bilimi notekis taqsimlangan: yangi dasturchi "domain paketi Spring'ga bog'lanmaydi" shartini bilmaydi, tajribali reviewer esa buni har safar qo'lda tushuntiradi. "Faqat bu safar" istisnolari hech qayerda qayd etilmaydi va olti oydan keyin normaga aylanadi. Va qoida shaxsiy mavzuga aylanadi: "men shunday yozdim, u esa yoqtirmadi". Test shaxssiz — build qizil bo'ldi, muhokama tugadi.

Shu bilan birga test review'ni almashtirmaydi, uni tozalaydi: test mexanik invariantlarni (bog'liqlik yo'nalishi, annotatsiya joyi, nomlanish, cycle) oladi, review esa dizaynning maqsadga mosligini. Istisno ham kodda yashashi kerak: qoidani buzish zarur bo'lsa, bu `@ArchIgnore`, freeze store yozuvi yoki `because(...)` izohi orqali ko'rinadigan va audit qilinadigan bo'lishi lozim.

### 14.2 ArchUnit asoslari

ArchUnit — oddiy Java kutubxonasi: bayt-kodni o'qiydi, `JavaClasses` modelini quradi va unga qoidalarni qo'llaydi. Alohida agent yoki maxsus runner kerak emas, qoida oddiy JUnit 5 testi sifatida ishlaydi (`archunit-junit5` artifact'i). ArchUnit 1.x'da asosiy elementlar quyidagilar: `ArchRuleDefinition.classes()`, `noClasses()`, `methods()`, `noMethods()`, `fields()` subyektni tanlaydi; `.that(...)` uni filtrlaydi; `.should(...)` talabni bildiradi; `.because(...)` xato matniga sababni qo'shadi. `@AnalyzeClasses` import qilingan klasslarni keshlaydi, `@ArchTest` esa `static final ArchRule` maydoni yoki `void method(JavaClasses)` metodi bo'lishi mumkin.

```java
import static com.tngtech.archunit.lang.syntax.ArchRuleDefinition.*;

@AnalyzeClasses(packages = "com.example.shop",
        importOptions = ImportOption.DoNotIncludeTests.class)
class ArchitectureTest {

    @ArchTest
    static final ArchRule service_nomlanishi = classes()
            .that().resideInAPackage("..service..")
            .should().haveSimpleNameEndingWith("Service")
            .because("qatlam nomi klass nomidan ko'rinib turishi kerak");

    @ArchTest
    static final ArchRule web_repositoryga_bormaydi = noClasses()
            .that().resideInAnyPackage("..web..", "..controller..")
            .should().dependOnClassesThat().resideInAPackage("..repository..");

    @ArchTest
    void qoida_metod_sifatida(JavaClasses classes) {
        noClasses().that().resideInAPackage("..domain..")
                .should().dependOnClassesThat()
                .resideInAPackage("org.springframework..")
                .check(classes);
    }
}
```

Bitta `@AnalyzeClasses` klassidagi barcha `@ArchTest` importni ulashadi, shuning uchun 30 ta qoidani bitta test klassiga yig'ish 30 ta alohidasidan tezroq ishlaydi.

Mavjud loyihada yangi qoidani yoqsangiz, yuzlab buzilish chiqadi va jamoa qoidani emas, testni o'chiradi. `FreezingArchRule` buni hal qiladi: birinchi ishga tushishda mavjud buzilishlarni violation store'ga yozib testni yashil qiladi, keyin faqat yangi buzilishlar xato beradi. Buzilish tuzatilsa store qisqaradi — ratchet bir tomonga aylanadi.

```java
@ArchTest
static final ArchRule domain_toza = FreezingArchRule.freeze(
        noClasses().that().resideInAPackage("..domain..")
                .should().dependOnClassesThat()
                .resideInAnyPackage("org.springframework..", "jakarta.persistence..")
                .because("domain model framework'dan mustaqil bo'ladi"));
```

Store yo'li `archunit.properties` da `freeze.store.default.path` va `freeze.store.default.allowStoreCreation=true` bilan boshqariladi. Store'ni git'ga qo'shing: u texnik qarzning ko'rinadigan ro'yxatiga aylanadi.

### 14.3 Amaliy ArchUnit qoidalari to'plami

Qatlamlarni o'nlab `noClasses()` qoidasi bilan emas, `Architectures.layeredArchitecture()` bilan tasvirlash qulay — xato xabari ham tushunarli chiqadi.

```java
@ArchTest
static final ArchRule qatlamlar = Architectures.layeredArchitecture()
        .consideringOnlyDependenciesInLayers()
        .layer("Web").definedBy("..web..")
        .layer("Service").definedBy("..service..")
        .layer("Persistence").definedBy("..repository..")
        .layer("Domain").definedBy("..domain..")
        .whereLayer("Web").mayNotBeAccessedByAnyLayer()
        .whereLayer("Service").mayOnlyBeAccessedByLayers("Web")
        .whereLayer("Persistence").mayOnlyBeAccessedByLayers("Service")
        .whereLayer("Domain").mayOnlyBeAccessedByLayers(
                "Web", "Service", "Persistence");
```

Keyingi to'plam — kundalik xatolarni ushlaydigan qoidalar. `GeneralCodingRules` ichida tayyori bor: `NO_CLASSES_SHOULD_USE_FIELD_INJECTION` (konstruktor injection majburiy), `NO_CLASSES_SHOULD_ACCESS_STANDARD_STREAMS` (`System.out.println` ta'qiqi).

```java
@ArchTest
static final ArchRule transactional_faqat_servisda = methods()
        .that().areAnnotatedWith(Transactional.class)
        .should().beDeclaredInClassesThat().resideInAPackage("..service..")
        .because("tranzaksiya chegarasi use-case chegarasiga teng");

@ArchTest
static final ArchRule field_injection_yoq =
        GeneralCodingRules.NO_CLASSES_SHOULD_USE_FIELD_INJECTION;

@ArchTest
static final ArchRule println_yoq =
        GeneralCodingRules.NO_CLASSES_SHOULD_ACCESS_STANDARD_STREAMS;

@ArchTest
static final ArchRule eski_vaqt_api_yoq = noClasses()
        .should().dependOnClassesThat()
        .haveFullyQualifiedName("java.util.Date")
        .orShould().callMethod(System.class, "currentTimeMillis")
        .because("vaqt Clock orqali olinadi, aks holda test qilinmaydi");

@ArchTest
static final ArchRule entity_controllerdan_chiqmaydi = noClasses()
        .that().areAnnotatedWith(RestController.class)
        .should().dependOnClassesThat().areAnnotatedWith(Entity.class)
        .because("API shartnomasi DTO bilan ifodalanadi");
```

Oxirgi ikkisi — aylanma bog'liqlik va test nomlash konvensiyasi. Cycle tekshiruvi `SlicesRuleDefinition` orqali bajariladi va amalda eng foydali qoidalardan biri: aylanma bog'liqlik modullashtirishni imkonsiz qiladi.

```java
@ArchTest
static final ArchRule aylanma_boglik_yoq = SlicesRuleDefinition
        .slices().matching("com.example.shop.(*)..")
        .should().beFreeOfCycles();

@ArchTest
static final ArchRule test_nomlari = methods()
        .that().areAnnotatedWith(Test.class)
        .should().haveNameMatching("should[A-Z].*|.*_should_.*")
        .because("test nomi kutilgan xatti-harakatni aytishi kerak");
```

### 14.4 Spring Modulith bilan modul chegaralarini tekshirish

Spring Modulith 1.x paketni modul deb qabul qiladi: application klassining to'g'ridan-to'g'ri ost-paketlari — modullar, ularning ichki ost-paketlari esa modulning yopiq qismi. Boshqa moduldan faqat modulning yuqori darajadagi tipiga yoki `@NamedInterface` bilan belgilangan paketga murojaat qilish mumkin. Bu modular monolitni saqlashning eng arzon yo'li: paket qoidalarini qo'lda yozish o'rniga bitta `verify()` barcha chegarani tekshiradi.

```java
class ModulithTest {

    static final ApplicationModules modules =
            ApplicationModules.of(ShopApplication.class);

    @Test
    void modul_chegaralari_buzilmagan() {
        modules.verify();
    }

    @Test
    void hujjat_generatsiya_qilinadi() {
        new Documenter(modules)
                .writeModulesAsPlantUml()
                .writeIndividualModulesAsPlantUml()
                .writeModuleCanvases();
    }
}
```

`Documenter` PlantUML (C4 uslubidagi) diagrammalarini va har bir modul uchun "canvas" (ochiq API, event'lar, konfiguratsiya xossalari) hujjatini `target/spring-modulith-docs` ichiga yozadi. Bu hujjat qo'lda yangilanmaydi — har build'da kodan qayta tug'iladi va eskirmaydi.

Modul bog'liqliklarini `package-info.java` da aniq cheklash, modullar orasidagi event oqimini esa `@ApplicationModuleTest` va `Scenario` bilan tekshirish mumkin.

```java
@ApplicationModule(allowedDependencies = { "catalog::api", "shared" })
package com.example.shop.order;
```

```java
@ApplicationModuleTest
class OrderModuleTest {

    @Test
    void buyurtma_yopilsa_event_chiqadi(Scenario scenario) {
        scenario.stimulate(() -> orders.complete(orderId))
                .andWaitForEventOfType(OrderCompleted.class)
                .matchingMappedValue(OrderCompleted::orderId, orderId)
                .toArrive();
    }
}
```

`modules.verify()`'ni PR darvozasiga qo'ying, `Documenter`'ni esa merge'dan keyin ishlatib natijani artefakt sifatida saqlang.

### 14.5 Test coverage: JaCoCo

JaCoCo Java agent sifatida ulanadi va bajarilgan bayt-kodni hisoblaydi. Muhim farq — counter turlari: `LINE` qator bajarildimi deb so'raydi, `BRANCH` esa shart ifodasining har ikki tarmog'i sinalganini tekshiradi. `if (a && b)` bitta qator, lekin to'rt tarmoq: line coverage 100%, branch coverage 25% bo'lishi mumkin. Shuning uchun chegara `BRANCH` ustiga qo'yiladi.

```xml
<plugin>
  <groupId>org.jacoco</groupId>
  <artifactId>jacoco-maven-plugin</artifactId>
  <version>0.8.13</version>
  <configuration>
    <excludes>
      <exclude>**/dto/**</exclude>
      <exclude>**/*MapperImpl.class</exclude>
      <exclude>**/generated/**</exclude>
    </excludes>
  </configuration>
  <executions>
    <execution><goals><goal>prepare-agent</goal></goals></execution>
    <execution><id>report</id><phase>verify</phase>
      <goals><goal>report</goal></goals></execution>
    <execution><id>check</id><phase>verify</phase>
      <goals><goal>check</goal></goals>
      <configuration><rules><rule>
        <element>BUNDLE</element>
        <limits><limit>
          <counter>BRANCH</counter>
          <value>COVEREDRATIO</value><minimum>0.60</minimum>
        </limit></limits>
      </rule></rules></configuration>
    </execution>
  </executions>
</plugin>
```

Gradle'da shu narsa `jacocoTestReport` va `jacocoTestCoverageVerification { violationRules { ... } }` bloklari bilan yoziladi, so'ng `check.dependsOn jacocoTestCoverageVerification`.

Generatsiya qilingan kodni chiqarib tashlash shart: MapStruct `*MapperImpl`, jOOQ/OpenAPI generatori, protobuf. Lombok uchun `lombok.config` ga `lombok.addLombokGeneratedAnnotation = true` qo'ying — JaCoCo nomi `Generated` bo'lgan annotatsiyali kodni o'zi e'tiborsiz qoldiradi. DTO va record'larda tekshirishga arziydigan logika yo'q.

Eng muhim qaror — chegarani belgilash. Umumiy foiz ("80% bo'lsin") yaroqsiz: eski loyihada erishilmas, yangisida ma'nosiz oson. To'g'ri yondashuv — o'zgargan kod uchun chegara (diff coverage): "bu PR'da qo'shilgan yoki o'zgargan qatorlarning kamida 80% qoplangan bo'lsin". SonarQube buni New Code ustidan o'zi hisoblaydi, Sonar bo'lmasa `diff-cover` kabi vositalar JaCoCo XML hisobotini git diff bilan birlashtiradi. Umumiy foiz esa faqat trend sifatida kuzatiladi: tushib ketmasin, shu kifoya.

Coverage nimaga yaraydi: qoplanmagan joyni topishga. "Bu `catch` bloki bajarilmagan", "bu `else` sinalmagan" — real signal. Nimaga yaramaydi: sifat ko'rsatkichi bo'lishga, chunki u kod bajarilganini aytadi, natija tekshirilganini aytmaydi.

### 14.6 Coverage anti-patternlari

Birinchi anti-pattern — 100% quvish. Oxirgi 15% eng qimmat va eng kam foydali qism: `toString`, getter, `equals`, config klasslari, erishilmaydigan `default` branch'lar. Shu vaqt integration testlarga sarflansa, foyda bir necha barobar ko'p bo'ladi.

Ikkinchisi — assertion'siz test. Metodni chaqirib hech narsa tekshirmaydigan test coverage'ni ko'taradi, lekin bitta xatoni ham ushlamaydi. Bundan yomoni — `assertThat(result).isNotNull()` bilan tugaydigan testlar: ular tekshirayotgandek ko'rinadi va coverage KPI bo'lgan jamoalarda o'z-o'zidan paydo bo'ladi.

Uchinchi va eng xatarli — coverage'ni KPI yoki bonus mezoni qilish. Goodhart qonuni aniq ishlaydi: ko'rsatkich maqsadga aylansa, u ko'rsatkich bo'lishdan to'xtaydi. Jamoa foizni ko'taradi, test suite esa sifatsiz qoladi. Arxitektor pozitsiyasi aniq bo'lsin: foizga emas, coverage pasayishi sababiga qaraymiz, test sifatini esa mutation testing o'lchaydi.

### 14.7 Mutation testing: PIT

PIT (pitest) bayt-kodga kichik o'zgartirishlar — mutatsiyalar — kiritadi va testlarni qayta ishga tushiradi. Mutatsiyadan keyin ham barcha test yashil bo'lsa, mutatsiya "tirik qoldi" (survived): test suite o'sha xatti-harakatni tekshirmaydi. Mutation score = o'ldirilgan mutatsiyalar / jami mutatsiyalar. Coverage "bu qator bajarildimi?" deb so'raydi, PIT "bu qatorni buzsam, testlar sezadimi?" deb — bu ancha qimmatli savol.

```xml
<plugin>
  <groupId>org.pitest</groupId>
  <artifactId>pitest-maven</artifactId>
  <version>1.17.0</version>
  <dependencies>
    <dependency>
      <groupId>org.pitest</groupId>
      <artifactId>pitest-junit5-plugin</artifactId>
      <version>1.2.1</version>
    </dependency>
  </dependencies>
  <configuration>
    <targetClasses><param>com.example.shop.domain.*</param></targetClasses>
    <targetTests><param>com.example.shop.*Test</param></targetTests>
    <mutators><mutator>STRONGER</mutator></mutators>
    <mutationThreshold>70</mutationThreshold>
    <coverageThreshold>75</coverageThreshold>
    <timeoutConstant>5000</timeoutConstant>
    <threads>4</threads>
    <withHistory>true</withHistory>
    <outputFormats><format>HTML</format><format>XML</format></outputFormats>
  </configuration>
</plugin>
```

Mutator guruhlari: `DEFAULTS` (shart inkori, matematik amallar, `void` chaqiruvni o'chirish, return qiymatini almashtirish), `STRONGER` (ustiga `REMOVE_CONDITIONALS` va `EXPERIMENTAL_*` qismi) va `ALL`. Boshlash uchun `DEFAULTS` yetarli, domain yadrosi uchun `STRONGER` oqlanadi.

PIT sekin: har mutatsiya uchun testlar qayta ishlaydi. Uni cheklashning uch yo'li bor. Birinchisi — `targetClasses`'ni faqat biznes logikasi bilan cheklash: controller, config va DTO uchun mutation testing ma'nosiz. Ikkinchisi — `withHistory` va faqat o'zgargan sinflar: `org.pitest:pitest-maven:scmMutationCoverage` goal'i SCM holatiga qarab (`ADDED`, `MODIFIED`) faqat o'zgargan fayllarni tahlil qiladi, bu PR darvozasi uchun mos. Uchinchisi — to'liq tahlilni nightly'ga olib chiqish. Mutation score'ni bloklovchi qilishdan oldin kamida bir oy trend sifatida kuzating.

### 14.8 Statik tahlil: qaysi vositani tanlash

Statik tahlil vositalari bir-birini almashtirmaydi, turli darajada ishlaydi: Error Prone kompilyatsiya ichida (AST), SpotBugs bayt-kodda, Checkstyle va PMD manba matnida, Sonar esa hammasini jamlaydi.

| Vosita | Nimani topadi | Qayerda ishlaydi | Tezligi |
| --- | --- | --- | --- |
| ArchUnit 1.x | bog'liqlik yo'nalishi, annotatsiya joyi, nomlanish, cycle | test sifatida, bayt-kodda | sekundlar |
| Spring Modulith 1.x | modul chegarasi va ruxsatsiz modul bog'liqligi | test + hujjat generatsiyasi | sekundlar |
| JaCoCo | qoplanmagan qator va branch | test agent sifatida | tez |
| PIT (pitest) | test suite'ning xato ushlash qobiliyati | alohida goal | sekin |
| Error Prone + NullAway | bug pattern, null xavfi | javac plugin'i | kompilyatsiya ichida |
| SpotBugs (+ findsecbugs) | bayt-kod darajasidagi bug va xavfsizlik | verify fazasi | o'rtacha |
| Checkstyle / PMD (CPD) | stil, murakkablik, duplikatsiya | verify fazasi | tez |
| SonarQube / SonarCloud | jamlash, New Code darvozasi, trend | CI serverda | o'rtacha |
| Spotless | formatlash, import tartibi | validate / pre-commit | tez |

Amaliy tanlov: minimal to'plam — Spotless (format), Error Prone + NullAway (kompilyatsiyada), ArchUnit (chegaralar) va SonarQube (jamlovchi darvoza). Checkstyle'ning formatlash qismini Spotless bajargani uchun uni faqat qoida uchun qoldiring. PMD va SpotBugs Sonar bilan qisman takrorlanadi, lekin `findsecbugs` plugin'i bilan SpotBugs xavfsizlik uchun qiymat beradi.

```xml
<plugin>
  <artifactId>maven-compiler-plugin</artifactId>
  <configuration>
    <compilerArgs>
      <arg>-XDcompilePolicy=simple</arg>
      <arg>--should-stop=ifError=FLOW</arg>
      <arg>-Xplugin:ErrorProne -Xep:NullAway:ERROR
        -XepOpt:NullAway:AnnotatedPackages=com.example.shop</arg>
    </compilerArgs>
    <annotationProcessorPaths>
      <path>
        <groupId>com.google.errorprone</groupId>
        <artifactId>error_prone_core</artifactId>
        <version>2.36.0</version>
      </path>
      <path>
        <groupId>com.uber.nullaway</groupId>
        <artifactId>nullaway</artifactId>
        <version>0.12.3</version>
      </path>
    </annotationProcessorPaths>
  </configuration>
</plugin>
```

Qoidalarni bosqichma-bosqich kiriting: avval hammasini `WARN` darajasida yoqing, ogohlantirishlar sonini baseline qilib oling, so'ng eng ko'p real xato beradigan 10-15 qoidani `ERROR` ga ko'taring. NullAway'ni esa butun kodga birdan emas, `AnnotatedPackages` ni bitta moduldan boshlab kengaytiring.

### 14.9 SonarQube quality gate

Sonar'ning asosiy g'oyasi — New Code: baseline (oldingi versiya, N kun yoki reference branch) belgilanadi va darvoza shartlari faqat shundan keyin o'zgargan kodga qo'llaniladi. Standart "Sonar way" gate'i yangi kod uchun coverage kamida 80%, duplikatsiya 3% dan oshmasligi, Maintainability/Reliability/Security reytinglari A va security hotspot'larning 100% ko'rib chiqilganini talab qiladi. Eski kodda minglab muammo bo'lsa ham gate yashil bo'ladi — shuning uchun u mavjud loyihada ishlaydi.

```yaml
      - name: Sonar tahlili
        run: >
          ./mvnw -B verify sonar:sonar
          -Dsonar.projectKey=shop
          -Dsonar.qualitygate.wait=true
        env:
          SONAR_TOKEN: ${{ secrets.SONAR_TOKEN }}
```

`sonar.qualitygate.wait=true` bo'lmasa, scanner natijani yuborib darhol muvaffaqiyat bilan tugaydi va gate amalda hech narsani bloklamaydi — bu eng ko'p uchraydigan xato. Gate buzilganda PR status check qizil bo'ladi, izohlar esa PR decoration orqali diff ustiga tushadi. Texnik qarzda ikki qoida muhim: muammolarni ommaviy "Won't fix" qilib yopmang va eski kodni rejalashtirilgan tarzda, eng ko'p o'zgaradigan fayllardan boshlab tozalang.

### 14.10 Bog'liqliklarni nazorat qilish

Bog'liqlik darvozasi uch savolga javob beradi: versiyalar mosmi, bu kutubxonaga ruxsat bormi va litsenziyasi yaroqlimi. Birinchi ikkisini `maven-enforcer-plugin` hal qiladi.

```xml
<plugin>
  <artifactId>maven-enforcer-plugin</artifactId>
  <version>3.5.0</version>
  <executions>
    <execution>
      <id>deps-gate</id>
      <phase>validate</phase>
      <goals><goal>enforce</goal></goals>
      <configuration>
        <rules>
          <dependencyConvergence/>
          <banDuplicatePomDependencyVersions/>
          <bannedDependencies>
            <excludes>
              <exclude>commons-logging:commons-logging</exclude>
              <exclude>joda-time:joda-time</exclude>
              <exclude>junit:junit</exclude>
            </excludes>
          </bannedDependencies>
        </rules>
      </configuration>
    </execution>
  </executions>
</plugin>
```

`dependencyConvergence` bitta kutubxonaning turli versiyalari transitiv kelib qolgan holatlarni ushlaydi — bu `NoSuchMethodError` kabi runtime xatolarining asosiy manbai. Ruxsat etilgan kutubxonalar ro'yxatini BOM orqali yuritish qulay: barcha versiyalar `dependencyManagement`da, `bannedDependencies` esa eski variantlarni to'sadi (JUnit 4, Joda-Time, `commons-logging`). Gradle'da shu vazifani `resolutionStrategy.failOnVersionConflict()` va platform/BOM bajaradi.

Litsenziya uchun `license-maven-plugin` (MojoHaus) `aggregate-add-third-party` goal'i va `failOnBlacklist` sozlamasi ishlatiladi: GPL yoki noma'lum litsenziya paydo bo'lsa build to'xtaydi. Zaxiralanmagan kutubxonani ushlashning avtomatik qoidasi yo'q, lekin ikki signal ishlaydi: `versions-maven-plugin` ko'rsatadigan so'nggi reliz sanasi (ikki yildan oshgan bo'lsa ko'rib chiqiladi) va yangi bog'liqlik qo'shilganda arxitektura review'i. Ma'lum zaifliklarni skanerlash (OWASP Dependency-Check, SCA) 13-bobda ko'rilgan; bu bobdagi darvoza sifat va moslik uchun.

### 14.11 Formatlash va pre-commit

Formatlash muhokamasi review vaqtining eng foydasiz qismi, uni butunlay yo'q qilish kerak: `.editorconfig` IDE uchun, Spotless esa build uchun yakuniy haqiqat bo'ladi.

```xml
<plugin>
  <groupId>com.diffplug.spotless</groupId>
  <artifactId>spotless-maven-plugin</artifactId>
  <version>2.44.0</version>
  <configuration>
    <ratchetFrom>origin/main</ratchetFrom>
    <java>
      <palantirJavaFormat><version>2.50.0</version></palantirJavaFormat>
      <removeUnusedImports/>
      <importOrder><order>java,javax,jakarta,org,com,</order></importOrder>
      <formatAnnotations/>
    </java>
    <pom><sortPom/></pom>
  </configuration>
  <executions>
    <execution>
      <phase>validate</phase>
      <goals><goal>check</goal></goals>
    </execution>
  </executions>
</plugin>
```

`ratchetFrom` juda muhim: u faqat `origin/main` dan keyin o'zgargan fayllarni formatlaydi, shuning uchun butun repo'ni bitta ulkan commit bilan qayta formatlash shart emas. Lokal darvoza sifatida pre-commit framework (yoki Lefthook) ishlatiladi.

```yaml
repos:
  - repo: local
    hooks:
      - id: spotless
        name: spotless-apply
        entry: ./mvnw -q spotless:apply
        language: system
        pass_filenames: false
        files: \.java$
      - id: arch-tests
        name: arch-tests
        entry: ./mvnw -q -Dtest=ArchitectureTest test
        language: system
        pass_filenames: false
        files: \.java$
```

Hook'lar 10 sekunddan oshmasin (aks holda jamoa `--no-verify` bilan o'tib ketadi) va CI hook'larga tayanmasin: hook lokal qulaylik, CI esa haqiqiy darvoza.

### 14.12 Darvozalarni joylashtirish

Barcha tekshiruvni bitta joyga yig'ish — eng ko'p uchraydigan xato: PR 40 daqiqa kutadi va jamoa darvozani yoqtirmay qoladi. To'g'ri yondashuv — tekshiruvlarni tezligi bo'yicha bosqichlarga taqsimlash.

| Bosqich | Nima ishlaydi | Vaqt budjeti | Buzilganda |
| --- | --- | --- | --- |
| Lokal (IDE) | Error Prone kompilyatsiyada, IDE inspection, `.editorconfig` | darhol | dasturchi o'zi ko'radi |
| pre-commit | `spotless:apply`, ArchUnit tez qoidalari | 10 sekundgacha | commit to'xtaydi |
| PR (har push) | unit testlar, ArchUnit, `modules.verify()`, Spotless check, enforcer, Sonar PR tahlili | 10 daqiqagacha | PR qizil, merge bloklangan |
| Merge (main) | to'liq integration testlar, JaCoCo check, Sonar quality gate, litsenziya tekshiruvi | 30 daqiqagacha | main qizil, release bloklangan |
| Nightly | to'liq PIT, SpotBugs + findsecbugs, Dependency-Check, PMD/CPD | cheklanmagan | ticket ochiladi, release bloklanmaydi |

Qoida sodda: PR'da faqat tez va deterministik tekshiruvlar, sekin tahlillar nightly'ga. Har bir qizil nightly uchun javobgar va muddat belgilanadi.

### 14.13 Darvozalarni joriy qilish strategiyasi

Mavjud loyihada hamma darvozani birdan yoqish kafolatlangan muvaffaqiyatsizlik: birinchi hafta hamma PR qizil bo'ladi, keyingi haftada jamoa tekshiruvlarni `continue-on-error` qilib qo'yadi.

| Bosqich | Qadam | Talab darajasi |
| --- | --- | --- |
| 1 | Spotless + `.editorconfig`, `ratchetFrom` bilan | majburiy, lekin avtomatik tuzatiladi |
| 2 | ArchUnit, barcha qoida `freeze` bilan | yangi buzilish taqiqlangan |
| 3 | JaCoCo report + Sonar New Code gate | faqat o'zgargan kodga |
| 4 | Error Prone/NullAway, enforcer, litsenziya | bitta moduldan boshlab |
| 5 | PIT nightly, keyin kritik paketlarda PR gate | trend, keyin chegara |

Har bir bosqichda uch narsa qilinadi: baseline olinadi (freeze store, Sonar New Code sanasi, ogohlantirishlar soni), talab faqat yangi kodga qo'yiladi va istisno so'rash yo'li aniq bo'ladi. Jamoani ishontirishning eng yaxshi usuli — darvozani "jazolash" emas, "review'dan mexanik ishni olib tashlash" sifatida taqdim etish. Ikkinchisi — har bir qoidaning `because(...)` izohida sababni yozish: sababni biladigan dasturchi qoidani aylanib o'tmaydi.

Darvozalar ro'yxatini ham kod kabi yuriting: har chorakda ko'rib chiqing, bitta ham real xato ushlamagan qoidani o'chiring, soxta signal beradigan tekshiruvni tuzating. Hech kim ishonmaydigan qizil darvoza — darvoza emas.

### 14.14 Arxitektor nazorat ro'yxati

- [ ] Har bir muhim arxitektura qoidasi uchun buzilganda build'ni qizil qiladigan test bor (ArchUnit yoki `modules.verify()`), qoida wiki'da emas, repo'da yashaydi.
- [ ] Mavjud buzilishlar `FreezingArchRule` store'iga olingan, store git'da saqlanadi va uning o'sishi PR'da ko'rinadi.
- [ ] JaCoCo'da umumiy foiz emas, o'zgargan kod uchun chegara qo'yilgan; generatsiya qilingan kod, DTO va config `excludes`da.
- [ ] Coverage KPI yoki bonus mezoni emas; test suite sifati kritik paketlarda PIT mutation score bilan o'lchanadi.
- [ ] Sonar quality gate New Code uchun sozlangan va `sonar.qualitygate.wait=true` bilan PR'ni haqiqatan bloklaydi.
- [ ] Statik tahlil bosqichma-bosqich joriy qilingan: baseline olingan, yangi kodga qattiq, eski kodga yumshoq talab.
- [ ] Bog'liqlik darvozasi bor: `dependencyConvergence`, ban ro'yxati, litsenziya tekshiruvi va zaxiralanmagan kutubxona signali.
- [ ] Har bir darvoza uchun "qizil bo'lsa kim nima qiladi" qoidasi va istisno so'rash yo'li hujjatlashtirilgan.

---

## 15. CI/CD da test pipeline (The Test Pipeline in CI/CD)

Test suite qanchalik yaxshi yozilgan bo'lsa ham, uni ishga tushiradigan pipeline sekin, ishonchsiz yoki tartibsiz bo'lsa, jamoa testlarga ishonishni to'xtatadi. CI/CD — bu testlarning haqiqiy yashash muhiti: aynan shu yerda test suite'ning arxitekturasi iqtisodiy qiymatga aylanadi yoki yo'qoladi. Bu bobda biz pipeline bosqichlarini tartiblash, feedback vaqtini byudjet sifatida boshqarish, testlarni parallellashtirish va tanlab ishga tushirish, GitHub Actions'da to'liq workflow qurish, deploy'dan keyingi tekshirish va production'da testlash masalalarini arxitektor nuqtai nazaridan ko'rib chiqamiz. Maqsad — har bir o'zgarish uchun qancha ishonch kerakligini ongli ravishda tanlash va buni pipeline tuzilishida aks ettirish.

### 15.1 Pipeline bosqichlari va tartibi

Pipeline tartibini belgilovchi yagona printsip — fail fast: eng tez va eng arzon tekshiruv birinchi bo'lib ishlaydi, eng qimmat va eng sekin tekshiruv oxirida. Agar kod kompilyatsiya qilinmasa, 20 daqiqalik E2E suite'ni ishga tushirishning ma'nosi yo'q. Shu bilan birga, "tez narsa oldinga" printsipini mutlaqlashtirmang: statik tahlil unit testdan tezroq bo'lishi mumkin, lekin unit test nosozligi odatda muhimroq signal beradi, shuning uchun ularni bir xil bosqichda parallel job sifatida ishga tushirish ko'p hollarda to'g'ri yechim.

| # | Bosqich | Nima tekshiriladi | Tipik vaqt | Qachon ishlaydi |
|---|---------|-------------------|------------|-----------------|
| 1 | Build va compile | Kompilyatsiya, dependency resolution | 1-2 daq | Har push |
| 2 | Unit test | Domen logikasi, Spring konteksti yo'q | 2-4 daq | Har push |
| 3 | Statik tahlil | Lint, Spotless, SpotBugs, Sonar | 2-3 daq | Har push (parallel) |
| 4 | Slice / integration test | @DataJpaTest, @WebMvcTest, Testcontainers | 4-8 daq | Har push |
| 5 | Contract test | Provider va consumer kontrakti | 1-3 daq | Har push |
| 6 | Image build | Jib yoki Buildpacks, SBOM | 2-3 daq | Merge'dan keyin |
| 7 | Deploy to test | Test muhitiga chiqarish | 2-4 daq | Merge'dan keyin |
| 8 | E2E smoke | Eng muhim 5-15 ta user journey | 5-10 daq | Merge'dan keyin |
| 9 | Security scan | Dependency va image scan | 3-6 daq | Merge + nightly |
| 10 | Performance | Load va stress profil | 20-60 daq | Nightly |
| 11 | Deploy to prod | Canary yoki rolling | 5-15 daq | Release |
| 12 | Post-deploy verify | Smoke, probe, metrika kuzatuvi | 3-10 daq | Har deploy |

Bu jadval shablon, dogma emas. Asosiy qaror: 1-5 bosqichlar PR darvozasi (pull request gate), 6-9 merge pipeline, og'ir suite'lar nightly.

### 15.2 Feedback vaqti byudjeti

Feedback vaqti — arxitektura talabidir, SLA kabi o'lchanishi va kuzatilishi kerak. Amaliy byudjet: PR tekshiruvi 10 daqiqadan kam (ideal 7), merge pipeline 25-30 daqiqadan kam, nightly 2-3 soatdan kam. Sabab oddiy: 10 daqiqa — ishlab chiquvchi kontekstni yo'qotmasdan kutadigan oraliq. 20 daqiqadan oshsa, odam boshqa ishga o'tadi; 40 daqiqadan oshsa, jamoa pipeline'ni chetlab o'tish yo'llarini izlay boshlaydi.

| Pipeline | Maqsad (p50) | Qattiq chegara (p95) | Buzilganda |
|----------|--------------|----------------------|------------|
| PR gate | < 7 daq | < 10 daq | Suite'ni bo'lish, shard qo'shish |
| Merge | < 20 daq | < 30 daq | Og'ir testni nightly'ga ko'chirish |
| Nightly | < 90 daq | < 180 daq | Parallel runner, scope qisqartirish |
| Hotfix yo'li | < 5 daq | < 8 daq | Faqat smoke + critical unit |

Byudjetni ushlab turish uchun pipeline davomiyligini metrika sifatida saqlang va p95 ni haftalik ko'rib chiqing. Byudjet buzilganda uchta vosita bor: parallellashtirish (resurs qo'shish), scope'ni ko'chirish (testni keyingi bosqichga olib o'tish), va testni tezlashtirish (Spring kontekstini kamaytirish, Testcontainers reuse). To'rtinchi "vosita" — testni o'chirish — faqat o'sha test haqiqatan qiymat bermasa qo'llanadi va bu qaror ongli, hujjatlashtirilgan bo'lishi kerak.

### 15.3 Testlarni ajratish va parallel bajarish

Maven'da unit va integration testlar ikki xil plugin bilan boshqariladi: Surefire `*Test` naming pattern'ni oladi va `test` fazada ishlaydi, Failsafe `*IT` ni oladi va `integration-test`/`verify` fazada ishlaydi. Bu ajratish pipeline'ni bosqichlarga bo'lishning asosi: PR'da `mvn test`, keyingi bosqichda `mvn verify`.

```xml
<build>
  <plugins>
    <plugin>
      <groupId>org.apache.maven.plugins</groupId>
      <artifactId>maven-surefire-plugin</artifactId>
      <version>3.5.2</version>
      <configuration>
        <includes><include>**/*Test.java</include></includes>
        <excludes><exclude>**/*IT.java</exclude></excludes>
        <forkCount>1C</forkCount>
        <reuseForks>true</reuseForks>
      </configuration>
    </plugin>
    <plugin>
      <groupId>org.apache.maven.plugins</groupId>
      <artifactId>maven-failsafe-plugin</artifactId>
      <version>3.5.2</version>
      <configuration>
        <includes><include>**/*IT.java</include></includes>
      </configuration>
      <executions>
        <execution>
          <goals>
            <goal>integration-test</goal>
            <goal>verify</goal>
          </goals>
        </execution>
      </executions>
    </plugin>
  </plugins>
</build>
```

`forkCount=1C` — CPU yadrosi soniga teng JVM fork. Bu JVM darajasidagi parallellik. JUnit 5 esa bir JVM ichida thread darajasida parallellikni beradi, `junit-platform.properties` orqali:

```properties
junit.jupiter.execution.parallel.enabled=true
junit.jupiter.execution.parallel.mode.default=concurrent
junit.jupiter.execution.parallel.mode.classes.default=concurrent
junit.jupiter.execution.parallel.config.strategy=dynamic
junit.jupiter.execution.parallel.config.dynamic.factor=1.0
# Spring kontekstli testlar uchun ko'pincha xavfsizroq variant:
# junit.jupiter.execution.parallel.mode.default=same_thread
# junit.jupiter.execution.parallel.mode.classes.default=concurrent
```

Muhim ogohlantirish: parallel execution faqat testlar haqiqatan izolyatsiya qilingan bo'lsa ishlaydi. Umumiy statik state, bitta jadvalga yozadigan integration testlar, `@DirtiesContext` — bularning barchasi parallellikda flaky natija beradi. Shuning uchun amaliy strategiya: unit testlarda `concurrent`, Spring kontekstli integration testlarda `classes.default=concurrent` + metodlar `same_thread`, va konfliktli testlarga `@ResourceLock` yoki `@Execution(SAME_THREAD)`.

Gradle'da ekvivalent `maxParallelForks`, va JUnit 5 property'larini `systemProperty` orqali uzatish:

```groovy
tasks.named('test', Test) {
    useJUnitPlatform()
    maxParallelForks = Runtime.runtime.availableProcessors().intdiv(2) ?: 1
    forkEvery = 100
    systemProperty 'junit.jupiter.execution.parallel.enabled', 'true'
    systemProperty 'junit.jupiter.execution.parallel.mode.classes.default', 'concurrent'
    // CI sharding: -Pshard=0 -PshardTotal=4
    if (project.hasProperty('shard')) {
        systemProperty 'junit.shard.index', project.shard
        systemProperty 'junit.shard.total', project.shardTotal
    }
    reports.junitXml.required = true
}
```

CI matrix va sharding — bu testlarni bir nechta runner'ga bo'lib tarqatish. GitHub Actions'da `strategy.matrix` bilan 4 shard ishga tushiriladi, har biri test ro'yxatining o'z qismini oladi. Sharding'ni amalga oshirishning ikki yo'li: test fayllari ro'yxatini deterministik bo'lish (hash yoki index bo'yicha) yoki oldingi run'lardagi davomiylik ma'lumotiga qarab balanslash (ikkinchisi ancha samarali, lekin tarixiy ma'lumot saqlashni talab qiladi).

### 15.4 Keshlash va tezlashtirish

Keshlash — pipeline tezlashtirishning eng arzon vositasi. Maven uchun `~/.m2/repository`, Gradle uchun `~/.gradle/caches` keshlanadi; `actions/setup-java` da `cache: maven` yoki `cache: gradle` buni avtomatik qiladi. Gradle build cache (`org.gradle.caching=true`) bundan kuchliroq: u task natijalarini (compile, test) keshlaydi, ya'ni o'zgarmagan modul testi umuman qayta ishlamaydi. Remote build cache bilan bu kesh butun jamoa va CI o'rtasida bo'linadi.

Docker layer cache image build vaqtini qisqartiradi, lekin Spring loyihalarida Jib yoki Buildpacks ishlatilsa, layer ajratish allaqachon optimal (dependency layer alohida, application class'lar alohida). Testcontainers uchun ikkita muhim optimizatsiya: image'larni oldindan pull qilish (pipeline boshida `docker pull postgres:16-alpine`, bu test timeout'ini oldini oladi) va container reuse (`testcontainers.reuse.enable=true` — lokalda juda foydali, CI'da ephemeral runner'da ma'nosi kam).

Eng katta tezlashtirish manbai — Spring kontekst keshini buzmaslik. Har xil `@MockBean`, har xil `@TestPropertySource`, har xil `@ActiveProfiles` kombinatsiyasi yangi ApplicationContext yaratadi, va har bir kontekst 2-10 sekund. 7-bobda ko'rilgan kontekst keshlash qoidalariga rioya qilish ko'pincha parallellashtirishdan kattaroq samara beradi. Incremental build (Gradle'ning up-to-date checking, Maven'da `-o` offline rejim va `mvn -am` bilan cheklangan scope) bu rasmni to'ldiradi.

### 15.5 Testni tanlab ishga tushirish

Katta monorepo'da har push'da butun suite'ni ishga tushirish byudjetni buzadi. Test selection — faqat o'zgarishga aloqador testlarni ishga tushirish.

Eng ishonchli daraja — modul darajasi. Maven'da `mvn test -pl payment-service -am` o'sha modul va uning upstream dependency'larini quradi; `-amd` esa downstream'larni ham oladi, bu esa o'zgarish ta'sirini to'liqroq qamrab oladi. Gradle'da `./gradlew :payment-service:test` plus dependency grafigini `./gradlew :payment-service:dependencies` orqali tahlil qilish mumkin. Git diff'dan o'zgargan fayllarni olib, ularni modul yo'llariga map qilish — amaliy va tushunarli yondashuv:

```bash
# O'zgargan modullarni aniqlash (merge-base'ga nisbatan)
BASE=$(git merge-base origin/main HEAD)
CHANGED=$(git diff --name-only "$BASE"...HEAD \
  | awk -F/ '/\// {print $1}' | sort -u | grep -v '^\.' )
if [ -z "$CHANGED" ]; then echo "no module changes"; exit 0; fi
# Umumiy modul o'zgarsa — hammasini ishga tushiramiz
if echo "$CHANGED" | grep -qE '^(common|test-support|platform-bom)$'; then
  echo "ALL" > affected.txt
else
  echo "$CHANGED" | paste -sd, - > affected.txt
fi
# Maven: mvn -pl "$(cat affected.txt)" -am verify
```

Predictive test selection (Gradle Develocity, Launchable kabi tijorat yechimlari) bundan bir qadam uzoqlashadi: tarixiy ma'lumot va ML modeli asosida qaysi test o'zgarishdan ta'sirlanishi ehtimolini bashorat qiladi va faqat yuqori ehtimolli testlarni ishga tushiradi. Bu PR vaqtini sezilarli qisqartiradi.

Xavfi va chegarasi aniq bo'lishi kerak. Test selection har qanday holatda ham evristika: reflection, Spring profile, konfiguratsiya fayli, SQL migratsiya yoki resource orqali keladigan bog'liqlikni statik tahlil ko'rmaydi. Shuning uchun qoida: selection faqat PR darajasida, merge pipeline va nightly'da esa to'liq suite majburiy. Agar selection noto'g'ri ishlasa, nightly uni tutadi — bu "safety net" bo'lmasa, selection'ni kiritmang.

### 15.6 GitHub Actions bilan to'liq namuna workflow

```yaml
name: ci
on:
  pull_request:
  push:
    branches: [main]
concurrency:
  group: ci-${{ github.ref }}
  cancel-in-progress: true
permissions:
  contents: read
  checks: write
  pull-requests: write
jobs:
  build-unit:
    runs-on: ubuntu-latest
    timeout-minutes: 15
    steps:
      - uses: actions/checkout@v4
        with: { fetch-depth: 0 }
      - uses: actions/setup-java@v4
        with: { distribution: temurin, java-version: '21', cache: maven }
      - run: mvn -B -ntp verify -DskipITs
      - uses: actions/upload-artifact@v4
        if: always()
        with:
          name: surefire-reports
          path: '**/target/surefire-reports/*.xml'
      - uses: dorny/test-reporter@v1
        if: always()
        with:
          name: unit-tests
          path: '**/target/surefire-reports/*.xml'
          reporter: java-junit
```

Integration test job'i shard matrix bilan va Testcontainers uchun image pre-pull bilan ajratiladi:

```yaml
  integration:
    needs: build-unit
    runs-on: ubuntu-latest
    timeout-minutes: 25
    strategy:
      fail-fast: false
      matrix:
        shard: [0, 1, 2, 3]
    env:
      TESTCONTAINERS_REUSE_ENABLE: 'false'
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-java@v4
        with: { distribution: temurin, java-version: '21', cache: maven }
      - name: Pre-pull test images
        run: |
          docker pull postgres:16-alpine
          docker pull confluentinc/cp-kafka:7.7.1
      - name: Run integration shard
        run: >
          mvn -B -ntp verify -DskipUnitTests
          -Djunit.shard.index=${{ matrix.shard }}
          -Djunit.shard.total=4
      - uses: actions/upload-artifact@v4
        if: failure()
        with:
          name: it-diagnostics-${{ matrix.shard }}
          path: |
            **/target/failsafe-reports/
            **/target/*.log
            **/build/reports/
```

Coverage va PR izohi alohida job sifatida: JaCoCo report'ni yig'ib, `madrapps/jacoco-report` yoki o'z `gh pr comment` buyruqlaringiz bilan PR'ga xulosa yoziladi. Testcontainers ishlatganda `services:` bloki kerak emas — Docker'ni test o'zi boshqaradi; `services:` ni faqat Testcontainers ishlatilmagan, oddiy TCP service kerak bo'lgan holatda tanlang (tezroq, lekin lokalda takrorlanmaydi).

### 15.7 GitLab CI va Jenkins uchun eslatma

GitLab CI'da ekvivalent tushunchalar: `stages` bosqichlarni, `parallel: 4` sharding'ni, `cache:key` dependency keshini, `artifacts:reports:junit` esa test natijalarini merge request'da ko'rsatishni beradi. Eng katta farq — Testcontainers uchun Docker: GitLab runner'da `docker:dind` service yoki privileged runner kerak, va `DOCKER_HOST` to'g'ri sozlanishi lozim. `rules:changes` bilan modul bo'yicha selection tabiiy ifodalanadi.

Jenkins'da declarative pipeline `stage` va `parallel` bloklaridan iborat; `junit '**/target/surefire-reports/*.xml'` natijalarni oladi, `publishHTML` yoki Allure plugin hisobotni chiqaradi. Farqlar: Jenkins agent'lari odatda uzoq yashaydigan (persistent) mashinalar, shuning uchun workspace tozalash (`cleanWs()`) va Testcontainers'dan qolgan container'larni tozalash (Ryuk) muhim; kesh esa agent diskida tabiiy ravishda saqlanadi, bu tez, lekin "ishlaydi mening agentimda" muammosini keltirib chiqaradi.

### 15.8 Majburiy tekshiruvlar va branch protection

Required check sifatida nimani belgilash — arxitektura qarori. Majburiy: build, unit test, slice/integration test, contract test, coverage darvozasi (14-bobda belgilangan chegaralar bo'yicha), critical security scan. Ogohlantirish sifatida qoldirish mumkin: yangi statik tahlil qoidalari (grace period bilan), performance trend, informational dependency advisory'lar. Qoida: majburiy check faqat deterministik va tez bo'lishi kerak — flaky check majburiy bo'lsa, jamoa uni chetlab o'tishni o'rganadi.

Merge queue (GitHub merge queue yoki GitLab merge train) ikki muammoni yechadi: semantik konflikt (ikki PR alohida yashil, birga qizil) va "main doim yashil" kafolati. Merge queue'da pipeline PR branch'ida emas, PR'ning main bilan birlashgan natijasida ishlaydi. Narxi — qo'shimcha pipeline run; foydasi — buzilgan main va undan keluvchi barcha blokirovkalarning yo'qolishi. Katta jamoada (kuniga 20+ merge) merge queue praktik zarurat.

### 15.9 Test natijalari va hisobot

Pipeline natijasi tushunarli bo'lmasa, uning qiymati yarmiga tushadi. Minimal to'plam: JUnit XML (Surefire/Failsafe `target/surefire-reports/*.xml` va `failsafe-reports/*.xml`), ularni CI UI'da ko'rsatadigan reporter, va JaCoCo coverage hisoboti (`jacoco:report` → `target/site/jacoco/jacoco.xml`).

Boyroq hisobot uchun Allure (`allure-junit5` adapter, `allure-maven`/`allure-gradle` plugin) qadam-qadam ko'rinish, attachment (screenshot, request/response) va tarixiy trend beradi; ReportPortal esa natijalarni markazlashtirib, nosozlik klassifikatsiyasini taklif qiladi.

PR izohida nima bo'lishi kerak: o'tgan/yiqilgan test soni, coverage o'zgarishi (delta, mutlaq son emas), yangi flaky testlar va to'g'ridan-to'g'ri nosoz test log'iga havola. Nosozlik artefaktlari — bu debug qilish imkoniyati: failsafe report, application log, E2E uchun screenshot va video, OOM holatida heap dump (`-XX:+HeapDumpOnOutOfMemoryError -XX:HeapDumpPath=target/`). Artefaktlarni faqat `if: failure()` da yuklash saqlash xarajatini keskin kamaytiradi.

### 15.10 Nightly va haftalik suite'lar

| Suite | Chastota | Tarkib | Egasi |
|-------|----------|--------|-------|
| To'liq regression | Nightly | Barcha IT + E2E, selection'siz | Dev jamoa (rotatsiya) |
| Performance | Nightly | Load profil, baseline bilan solishtirish | Platform/SRE |
| Mutation testing | Haftalik | PIT, o'zgargan paketlarda | Dev jamoa |
| Dependency + image scan | Nightly | CVE, litsenziya, SBOM diff | Security |
| Soak test | Haftalik | 8-24 soat uzluksiz yuklama | Platform/SRE |

Nightly'ning asosiy xatosi — natijani hech kim ko'rmasligi. Shuning uchun uchta tashkiliy qoida: har bir nightly suite'ning nomlangan egasi bo'lsin (jamoa, shaxs emas — shaxs ta'tilga chiqadi); nosozlik avtomatik ravishda ticket yoki Slack kanaliga tushsin, email'ga emas; va ertalab birinchi ish — nightly natijasini ko'rib chiqish, bu standup'ning doimiy bandi bo'lsin. Agar nightly uch kun ketma-ket qizil bo'lsa va hech narsa o'zgarmasa, u suite o'lgan — uni tuzat yoki o'chir.

### 15.11 Deploy'dan keyingi tekshirish

Deploy tugadi degani ishlayapti degani emas. Post-deploy verification zanjirida: readiness probe (`/actuator/health/readiness`) pod trafik qabul qilishga tayyormi; liveness probe (`/actuator/health/liveness`) jarayon tirikmi; keyin smoke test — real muhitga qarshi 5-15 ta eng muhim yo'l (login, asosiy o'qish, asosiy yozish), bir-ikki daqiqada tugaydigan.

Canary release'da yangi versiya trafikning 5-10% ini oladi va metrikalar solishtiriladi: error rate, p99 latency, business metrika (masalan, muvaffaqiyatli to'lov ulushi). Avtomatik rollback sharti aniq raqamlar bilan ifodalanishi kerak: "5 daqiqa oynada canary error rate baseline'dan 2x yuqori bo'lsa" yoki "p99 baseline'dan 50% yuqori". Argo Rollouts yoki Flagger bu analizni deklarativ ravishda bajaradi. Shartlarni noaniq qoldirmang — "agar yomon ko'rinsa" degan shart hech qachon avtomatik ishlamaydi.

Synthetic monitoring — bu production'da doimiy ishlaydigan smoke test: har 1-5 daqiqada muhim user journey'larni tashqaridan bajaradi va nosozlikni foydalanuvchi shikoyatidan oldin topadi. Amalda bu sizning E2E test kodingizning qayta ishlatilgan qismi bo'lishi mumkin, bu esa ikki marta yozishdan qutqaradi.

### 15.12 Production'da testlash

Production'da testlash — qoidalarni buzish emas, balki test muhiti hech qachon production'ga to'liq teng bo'lmasligini tan olish. To'rt asosiy texnika:

Feature flag bilan dark launch — yangi kod deploy qilinadi, lekin flag o'chiq; ichki foydalanuvchilar uchun yoqiladi, keyin bosqichma-bosqich kengaytiriladi. Spring'da bu oddiy `@ConditionalOnProperty` dan to'liq flag platformasiga (Unleash, LaunchDarkly, OpenFeature SDK) qadar bo'lishi mumkin. Shadow traffic — real so'rovlar nusxasi yangi versiyaga yuboriladi, lekin javobi foydalanuvchiga qaytmaydi; bu yangi implementatsiyani real yuklama va real ma'lumot shakli bilan sinashning eng halol usuli. A/B test — ikki variant o'rtasida business metrikani solishtirish, bu texnik emas, mahsulot qarori. Va barcha uchun asos — kuzatuvchanlik: distributed tracing, strukturalangan log, per-variant metrika.

Xavfsiz qilish shartlari: yozish operatsiyalarida yon ta'sir bo'lmasligini kafolatlash (shadow traffic'da yozishni mock qilish yoki alohida sxemaga yo'naltirish), test ma'lumotini real ma'lumotdan ajratish (test akkauntlarni belgilash va ularni analitikadan chiqarish), har bir flag uchun o'chirish mexanizmi va muddati (eskirgan flag — texnik qarz), va blast radius'ni cheklash. Agar siz canary metrikasini kuzatolmasangiz, production'da testlashga tayyor emassiz.

### 15.13 Monorepo va multi-modul loyihada test pipeline

Multi-modul Maven/Gradle loyihasida pipeline arxitekturasi modul grafigidan kelib chiqadi. Birinchi qadam — grafikni aniq va yuzaki (shallow) qilish: agar har bir modul `common` ga bog'liq bo'lsa, `common` dagi har o'zgarish butun suite'ni ishga tushiradi va selection'ning ma'nosi qolmaydi. Shuning uchun `common` ni mayda, barqaror modullarga bo'lish amaliy qiymat beradi.

Test util modullari (`test-support`, `testcontainers-fixtures`) `test-jar` yoki alohida artifact bo'lib chiqariladi, shunda har bir service uni `test` scope'da oladi — takroriy Testcontainers konfiguratsiyasi, umumiy fixture va assertion'lar bir joyda saqlanadi.

Versiyalash ikki modelda bo'ladi: bitta umumiy versiya (release train — barcha modullar birga chiqadi, oddiy, lekin bog'liq) yoki modul-bo'yicha mustaqil versiya (moslashuvchan, lekin matritsa testini talab qiladi). Release train monorepo'da ko'pincha to'g'ri tanlov: pipeline oddiy bo'ladi va contract test matritsasi kichik qoladi. Mustaqil versiyalashni tanlasangiz, contract test majburiy — aks holda modullar orasidagi moslik faqat production'da tekshiriladi.

### 15.14 Pipeline'ni ishonchli qilish

Pipeline'ning ishonchliligi uning tezligidan muhimroq. Birinchi qoida — infratuzilma nosozligini test nosozligidan ajratish. Docker registry javob bermadi, runner diski to'ldi, network timeout — bular test nosozligi emas, lekin odatiy pipeline ularni bir xil "failed" sifatida ko'rsatadi. Yechim: infra bosqichlarini (image pull, dependency download, container startup) alohida step sifatida ajratish va ularning exit code'ini alohida ko'rish; keyin retry'ni faqat o'sha step'larga qo'llash.

Retry siyosati qat'iy bo'lishi kerak: `docker pull` va dependency download uchun retry — to'g'ri; test bajarilishi uchun retry — flaky testni yashirish, bu 16-bobda ko'rilgan jarayonni buzadi. Agar test retry kerak bo'lsa, u hodisa sifatida qayd etilsin va flaky sifatida belgilansin, jimgina yashil bo'lmasin.

Timeout har darajada: job uchun (`timeout-minutes: 25`), test uchun (`@Timeout` yoki `junit.jupiter.execution.timeout.testable.method.default=2 m`), container startup uchun (Testcontainers `withStartupTimeout`). Timeout bo'lmasa, osilgan test butun runner quotasini yeydi. Resurs tomoni: standart GitHub runner 2 vCPU / 7 GB RAM — bu Testcontainers bilan bir nechta container ko'targan integration suite uchun ko'pincha kam. Larger runner (4-8 vCPU) narxi bor, lekin 25 daqiqani 8 daqiqaga tushirsa, ishlab chiquvchi vaqti hisobida tez qaytadi. Nihoyat, Docker mavjudligini boshida tekshirish (`docker info`) va yo'q bo'lsa aniq xabar bilan tez yiqilish — 20 daqiqadan keyingi tushunarsiz `ContainerLaunchException` dan yaxshiroq.

### 15.15 Anti-patternlar

Hamma testni har push'da ishga tushirish. Boshida to'g'ri ko'rinadi, loyiha o'sgach PR vaqti 45 daqiqaga chiqadi. To'g'ri yo'l — bosqichli strategiya va selection, nightly safety net bilan.

Qizil build bilan yashash. Main qizil bo'lib bir kundan ortiq turgan har bir soat — barcha signalning qiymatini nolga olib boradi. Qoida qattiq: buzilgan main eng yuqori prioritet, tuzatish yoki revert, uchinchi variant yo'q.

Flaky testni retry bilan yashirish. `retryFailedTests` qo'yib, qizil rangni yashilga aylantirish — eng qimmat qarz turi: endi siz real nosozlikni ham ko'rmaysiz.

Testni CI'da o'tkazib yuborish. `-DskipTests`, `@Disabled` kommentsiz, `@Ignore` "keyin tuzataman" bilan — bular hech qachon qaytib kelmaydi. Agar test o'chirilsa, muddat va ticket bilan o'chirilsin.

Faqat main'da test qilish. PR'da hech narsa ishlamasa, nosozlik main'ga tushgandan keyin aniqlanadi va kim buzganini topish qimmatlashadi.

Lokal va CI natijasining farqi. "Mening mashinamda ishlaydi" — bu pipeline dizayni muammosi: timezone, locale, Java versiyasi, Docker yoki fayl tizimi farqlari. Yechim — bir xil Java versiyasini wrapper/toolchain bilan qotirish, `-Duser.timezone=UTC` va `file.encoding=UTF-8` ni ikki joyda bir xil qo'yish, Testcontainers'ni lokalda ham ishlatish.

### 15.16 Arxitektor nazorat ro'yxati

- [ ] Pipeline bosqichlari fail fast printsipi bo'yicha tartiblangan, PR gate va merge pipeline aniq ajratilgan
- [ ] Feedback vaqti byudjeti yozilgan (PR < 10 daq), p95 metrika sifatida kuzatiladi va buzilganda aniq harakat rejasi bor
- [ ] Surefire (`*Test`) va Failsafe (`*IT`) ajratilgan, JUnit 5 parallel execution va sharding sozlangan hamda flaky bermasligi tasdiqlangan
- [ ] Dependency kesh, Gradle build cache, Testcontainers image pre-pull yoqilgan va Spring kontekst keshi buzilmasligi tekshirilgan; test selection faqat PR darajasida, to'liq suite nightly safety net sifatida majburiy
- [ ] Required check'lar ro'yxati ongli tanlangan (deterministik va tez), merge queue zarurati baholangan
- [ ] Nosozlik artefaktlari (JUnit XML, log, screenshot, heap dump) `if: failure()` da saqlanadi va PR'da xulosa ko'rinadi
- [ ] Deploy'dan keyin smoke test, canary metrikasi va avtomatik rollback sharti raqamlar bilan belgilangan
- [ ] Retry faqat infratuzilma step'larida; har bir nightly suite'ning nomlangan egasi va nosozlik marshruti bor

---

## 16. Flaky testlar, test qarzi va test kodini saqlash (Flaky Tests, Test Debt & Maintenance)

Test suite'ning qiymati uning yashil rangiga emas, ishonchliligiga bog'liq: agar jamoa qizil build'ni ko'rib birinchi navbatda "qayta ishga tushir" tugmasini bossa, siz testlarni emas, faqat CI vaqtini sotib olgansiz. Flaky testlar, to'planib qolgan test qarzi va saqlanmaydigan test kodi eng yaxshi test strategiyasini ham yemirib tashlaydi. Bu bob flaky testni sabablari bo'yicha tasniflash, aniqlash, karantinga olish va yo'q qilish jarayonini, shuningdek test kodini production kodi darajasida saqlash amaliyotlarini qamrab oladi.

### 16.1 Flaky test nima va nega eng qimmat muammo

Flaky test — kod va muhit o'zgarmagan holda bir xil commit'da bir marta yashil, boshqa marta qizil bo'ladigan test. Texnik jihatdan bu determinizmning yo'qolishi: natija faqat tekshirilayotgan kodga emas, balki vaqt, tartib, parallelism yoki tashqi holatga ham bog'liq bo'lib qoladi.

Narxi uch qatlamdan iborat:

1. **CI xarajati.** 1500 testli suite, build 12 daqiqa, kuniga 60 build. Test darajasida 0.05% flake rate ham build'larning yarmida kamida bitta qizil test beradi. Kuniga 25 qayta ishga tushirish × 12 daqiqa ≈ 5 soat runner vaqti, oyiga ~110 soat.
2. **Insoniy xarajat.** Qizil build'ni tekshirish, log o'qish, "bu flaky ekan" xulosasiga kelish — o'rtacha 10-15 daqiqa. Kuniga 25 hodisa × 12 daqiqa ≈ 5 soat/kun, oyiga deyarli bitta FTE ekvivalenti.
3. **Ishonchning yo'qolishi — eng qimmati.** Flake rate 1-2% dan oshganda jamoa har bir qizilni "ehtimol flaky" deb taxmin qiladi. Shu daqiqadan boshlab suite regressiyani ushlash qobiliyatini yo'qotadi: haqiqiy xato ham xuddi shu "qayta ishga tushir" bilan yopilib, production'ga chiqib ketadi.

Arxitektor uchun xulosa: flaky test bitta test muammosi emas, butun suite'ning ishonch koeffitsiyentini pasaytiruvchi tizimli nuqson. Shuning uchun flake rate 1% dan oshsa, yangi feature testlarini yozishni to'xtatib barqarorlikni tiklash to'g'ri qaror bo'ladi.

### 16.2 Flaky testning asosiy sabablari, misollar va yechimlari

Quyidagi jadval — diagnostikada birinchi murojaat qiladigan ro'yxat. Amalda hodisalarning 80% i birinchi beshta qatorga to'g'ri keladi.

| Sabab | Tipik Java/Spring ko'rinishi | Nega flaky | Yechim |
|---|---|---|---|
| Vaqtga bog'liqlik | `Thread.sleep(200)`, `LocalDate.now()` bilan solishtirish | Sekin runner'da sleep yetmaydi; yarim tun va oy oxirida sana siljiydi | `Clock` bean, testda `Clock.fixed(...)`; `Awaitility` |
| Asinxronlik | `@Async`, `ApplicationEventPublisher`, `@TransactionalEventListener(AFTER_COMMIT)` | Assertion event ishlanishidan oldin bajariladi | `await().untilAsserted(...)`; testda `SyncTaskExecutor` |
| Tartibga bog'liqlik | `static` counter, bean ichidagi mutable `Map`, tozalanmagan stub | Test A qoldirgan holat test B natijasini o'zgartiradi | `@BeforeEach` da reset, `Mockito.reset`, holatni bean'dan chiqarish |
| Context keshi iflosligi | Bir test context'ga mock qo'shadi, boshqasi o'sha context'ni kesh'dan oladi | Kesh kaliti bir xil bo'lsa iflos context qayta ishlatiladi | Konfiguratsiyani aniq ajratish; `@DirtiesContext(AFTER_CLASS)` so'nggi chora |
| Tasodifiy ma'lumot | `Random`, seed'siz `Instancio`/`EasyRandom`, `UUID` bilan unique constraint | Ba'zi qiymatlar edge-case'ga tushadi | Seed'ni qat'iy belgilash va loglash; edge-case'ni alohida test qilish |
| Tashqi tizim | Haqiqiy REST API, SMTP, S3 chaqiruvi | Tashqi tizim pasayishi testni buzadi | WireMock, Testcontainers, `MockRestServiceServer` |
| Port to'qnashuvi | `webEnvironment = DEFINED_PORT`, qat'iy `8080` | Parallel build'lar bir portni talashadi | `RANDOM_PORT` + `@LocalServerPort`; Testcontainers port mapping |
| DB holati va auto-increment ID | `assertThat(saved.getId()).isEqualTo(1L)` | Sequence testlar orasida o'sib boradi | ID mavjudligiga assert qilish; har test uchun rollback |
| Parallel bajarish | `junit.jupiter.execution.parallel.enabled=true` + umumiy fixture | Race condition | Parallelismni class darajasida; `@ResourceLock` |
| Timezone va locale | `SimpleDateFormat`, `String.format("%,.2f", x)`, sana parsing | CI UTC'da, developer mashinasi +05:00 da | `ZoneId` ni aniq berish; `-Duser.timezone=UTC -Duser.language=en` |
| Floating point | `assertThat(total).isEqualTo(0.3)` | `0.1 + 0.2 != 0.3` | `BigDecimal` + `isEqualByComparingTo`, yoki `isCloseTo(..., within(...))` |
| Map/Set tartibi | `HashMap`/`HashSet` iteration, `toString()` taqqoslash | Iteration tartibi kafolatlanmagan | `containsExactlyInAnyOrder`, `LinkedHashMap` |
| Test ma'lumotining ta'siri | Umumiy `@Sql` seed, bir xil email bilan yozuv | Noyoblik buzilishi, kutilmagan qator soni | Test-scoped unique key, `@Transactional` rollback |
| Resurs yetishmasligi | CI runner'da 2 vCPU, timeout 500 ms | Kutish oynasi juda tor | Timeout'ni real p99 dan 3-5× katta qilish; polling |

**1. Vaqtga bog'liqlik.**

```java
// FLAKY: tizim soatiga bog'liq, oy oxiri va yarim tunda buziladi
@Test
void shouldExpireSubscription() {
    var sub = new Subscription(LocalDate.now().minusDays(31));
    assertThat(sub.isExpired()).isTrue();   // 30 kunlik oyda chetga chiqadi
}

// FIX: Clock inject qilinadi, test vaqtni to'liq boshqaradi
@Test
void shouldExpireSubscription() {
    Clock clock = Clock.fixed(Instant.parse("2025-03-15T10:00:00Z"), ZoneOffset.UTC);
    var sub = new Subscription(LocalDate.of(2025, 2, 1), clock);
    assertThat(sub.isExpired()).isTrue();
}
```

Arxitektura qoidasi: production kodda `LocalDate.now()` yoki `Instant.now()` ni to'g'ridan-to'g'ri chaqirish taqiqlanadi, `java.time.Clock` bean sifatida inject qilinadi. Buni ArchUnit qoidasi bilan majburlash mumkin.

**2. Asinxronlik.**

```java
// FLAKY: sleep "yetarli" bo'lishiga umid qilamiz
@Test
void shouldSendWelcomeEmail() throws Exception {
    userService.register(new RegisterCommand("ali@example.com"));
    Thread.sleep(300);
    assertThat(emailOutbox.count()).isEqualTo(1);
}

// FIX: shartga qarab kutamiz, timeout faqat yuqori chegara
@Test
void shouldSendWelcomeEmail() {
    userService.register(new RegisterCommand("ali@example.com"));
    await().atMost(Duration.ofSeconds(5))
           .pollInterval(Duration.ofMillis(50))
           .untilAsserted(() -> assertThat(emailOutbox.count()).isEqualTo(1));
}
```

`Thread.sleep` ikki tomondan yomon: sekin runner'da yetmaydi (flaky), tez runner'da ortiqcha kutadi (sekin suite).

**3. Tartibga bog'liqlik va umumiy holat.**

```java
// FLAKY: static cache testlar orasida saqlanib qoladi
class PricingServiceTest {
    private static final Map<String, BigDecimal> CACHE = new HashMap<>();

    @Test void firstTest()  { CACHE.put("SKU-1", BigDecimal.TEN); /* ... */ }
    @Test void secondTest() { assertThat(CACHE).isEmpty(); } // tartibga bog'liq
}

// FIX: har test uchun yangi holat, static yo'q
class PricingServiceTest {
    private Map<String, BigDecimal> cache;

    @BeforeEach void setUp() { cache = new HashMap<>(); }
    @Test void secondTest()  { assertThat(cache).isEmpty(); }
}
```

**4. Tartib va floating point assertion'lari.**

```java
// FLAKY: HashSet tartibi va double arifmetikasi
@Test
void shouldSummarizeCart() {
    var result = cartService.summarize(cart);
    assertThat(result.skus()).containsExactly("SKU-1", "SKU-2"); // HashSet
    assertThat(result.total()).isEqualTo(0.3d);                  // 0.1 + 0.2
}

// FIX: tartibsiz taqqoslash va BigDecimal
@Test
void shouldSummarizeCart() {
    var result = cartService.summarize(cart);
    assertThat(result.skus()).containsExactlyInAnyOrder("SKU-1", "SKU-2");
    assertThat(result.total()).isEqualByComparingTo(new BigDecimal("0.30"));
}
```

### 16.3 Flaky testni aniqlash

Flaky testni "sezish" emas, o'lchash kerak. Surefire/Failsafe har bir modulda `target/surefire-reports/*.xml` (JUnit XML) hosil qiladi. Bu fayllarni build artefakti sifatida saqlab, markaziy joyga yuklash kerak: `commit_sha`, `branch`, `test_class`, `test_method`, `status`, `duration_ms`, `build_id`. Shundan keyin:

```
flake_rate(test) = (bir xil commit'da ham pass, ham fail bo'lgan run'lar) / (umumiy run)
```

Jamoa darajasidagi metrika: `suite_flake_rate = flake sababli qizil build'lar / umumiy build'lar`. Maqsad < 1%, ideal < 0.3%.

Maqsadli sinov buyruqlari:

```bash
# Bitta test metodini 50 marta takrorlash
for i in $(seq 1 50); do
  mvn -q test -Dtest='OrderServiceTest#shouldApplyDiscount' || echo "FAIL at run $i"
done

# Tasodifiy tartib (JUnit 5 built-in orderer'lari)
mvn test -Djunit.jupiter.testmethod.order.default=org.junit.jupiter.api.MethodOrderer\$Random \
         -Djunit.jupiter.testclass.order.default=org.junit.jupiter.api.ClassOrderer\$Random

# Parallel rejimda sinash
mvn test -Djunit.jupiter.execution.parallel.enabled=true \
         -Djunit.jupiter.execution.parallel.mode.default=concurrent

# Bitta klassni izolyatsiyada
mvn test -Dtest=OrderServiceTest -DfailIfNoTests=false

# Gradle: keshni chetlab o'tib qayta ishlatish
./gradlew test --tests 'com.acme.OrderServiceTest.shouldApplyDiscount' --rerun-tasks
```

Diagnostika mantiqi sodda: izolyatsiyada pass, to'liq suite'da fail → tartibga/umumiy holatga bog'liqlik; ketma-ket pass, parallel fail → race condition; tasodifiy tartibda fail → testlar orasidagi bog'liqlik; CI'da fail, lokalda pass → timing muammosi; 50 run'dan 1-2 tasi fail → haqiqiy nondeterminizm (vaqt, random, async).

Vositalar: lokal tekshiruv uchun `@RepeatedTest(50)`; tartib bog'liqligi uchun `MethodOrderer.Random` va `ClassOrderer.Random`; `junit-platform.properties` dagi parallelism sozlamalari; Gradle `test-retry` plugin'ining hisoboti; tarixni avtomatik yig'ish uchun Develocity yoki Jenkins "Flaky Test Handler".

### 16.4 Karantin (quarantine) jarayoni

Karantin — flaky testni o'chirib yuborish emas, uni vaqtincha blocking bo'lishdan chiqarib, egasi va muddati bilan ro'yxatga olish. Qadamlar:

1. **Aniqlash.** Haftalik hisobotda flake rate > 0.5% bo'lgan test nomzod bo'ladi.
2. **Belgilash.** `@Tag("flaky")` + sabab + ticket. `@Disabled` emas, chunki `@Tag` testni nightly'da ishlatishga imkon beradi:

```java
@Tag("flaky")
@Test
@DisplayName("Outbox publisher retries after broker reconnect")
    // FLAKY-1427: broker reconnect CI'da 2-8s orasida o'zgaradi.
    // Owner: @payments-team. SLA: 2025-11-15 gacha tuzatish yoki o'chirish.
void shouldRepublishAfterReconnect() { /* ... */ }
```

3. **CI'dan chiqarish.** PR gate'da o'tkazib yuboriladi, nightly'da ishlaydi va kuzatiladi:

```bash
mvn verify -Dgroups='!flaky'   # PR gate; yoki <excludedGroups>flaky</excludedGroups>
mvn test   -Dgroups='flaky'    # nightly: flake rate'ni o'lchash
```

4. **Egasini belgilash.** Egasi yo'q karantin — abadiy karantin.
5. **SLA qo'yish.** Tavsiya: 2 sprint (14 kun), muddat test kodida va ticket'da yoziladi.
6. **Muddat o'tgach qaror.** Faqat ikki variant: tuzatildi va karantindan chiqdi, yoki o'chirildi. "Yana 2 sprint" taqiqlanadi, aks holda ro'yxat go'ristonga aylanadi.
7. **Kvota.** Karantinda bir vaqtda jami testlarning 0.5% dan ko'pi bo'lmasligi kerak. Kvota to'lsa, yangi feature ishi to'xtatiladi.

Zanjir: `flake aniqlandi → @Tag + ticket + egasi + SLA → PR gate'dan chiqarildi → nightly'da kuzatiladi → SLA ichida tuzatildi ? chiqdi : o'chirildi`.

### 16.5 Retry'ning o'rni

Retry — og'riq qoldiruvchi, davo emas. Qoida: retry faqat infratuzilma nosozligi uchun. Legitim holatlar — Docker image tortib olish, Testcontainers start, dependency yuklash, runner tarmog'ining uzilishi; bunday retry'lar pipeline step darajasida qo'yiladi, test darajasida emas.

Test retry xavfli, chunki u flake'ni yashiradi (test yashil, nondeterminizm joyida); signal-to-noise nisbatini buzadi (production kodidagi haqiqiy race condition retry bilan yopiladi); suite'ni sekinlashtiradi; va "retry bor, demak flake yozish arzon" degan noto'g'ri madaniy signal beradi.

Agar legacy suite'ni bosqichma-bosqich tozalash davrida retry kerak bo'lsa, u faqat kuzatuv bilan qo'yiladi:

```xml
<plugin>
  <groupId>org.apache.maven.plugins</groupId>
  <artifactId>maven-surefire-plugin</artifactId>
  <configuration>
    <!-- Faqat migratsiya davri uchun; har bir rerun hisobotga yoziladi. -->
    <rerunFailingTestsCount>2</rerunFailingTestsCount>
  </configuration>
</plugin>
```

Surefire bunday testlarni XML hisobotda `flakyFailure` elementi sifatida belgilaydi — bu aynan o'lchash uchun kerakli ma'lumot. Gradle'da `org.gradle.test-retry` plugin'i `maxRetries` va muhim `failOnPassedAfterRetry` opsiyasini beradi. JUnit 5'da standart retry API yo'q: `TestTemplateInvocationContextProvider` asosida custom extension yozish yoki tashqi kutubxona ishlatish kerak; `@RepeatedTest` retry emas, u boshqa maqsadga xizmat qiladi.

Qat'iy qoida: retry yoqilgan bo'lsa, `flakyFailure` soni dashboard'da ko'rsatiladi va u ham nolga intilishi kerak. Retry'ni global yoqib hisobotni o'qimaslik — flake'ni rasman qonuniylashtirish.

### 16.6 Test qarzi (test debt)

Test qarzi — suite'ning kelajakdagi o'zgarishlarni qo'llab-quvvatlash qobiliyatini kamaytiruvchi har qanday holat. Turlari: **eskirgan test** (o'zgargan talabni tekshiradi, lekin mock'lar shunchalik chuqur ki real xatti-harakat ko'rinmaydi); **assertion'siz test** (faqat metodni chaqiradi — mutation testing bunday testlarni darhol ochadi); **abadiy `@Disabled`** (sababi yozilmagan, hech kim tegishga qo'rqadi); **takrorlangan test** (bir scenariyni uch darajada tekshiradi, qo'shimcha xavf qoplamaydi); **tushunarsiz test** (80 qatorli setup, nomi `test1`).

Inventarizatsiya qilmasdan qarzni to'lash mumkin emas:

```bash
grep -rn "@Disabled" --include=*.java src/test | wc -l
grep -rn '@Disabled$' --include=*.java src/test        # sababsiz o'chirilganlar
grep -rLn -e "assertThat" -e "verify(" -e "assert" \
  --include=*Test.java src/test/java                   # assertion'siz nomzodlar
grep -rn '@Tag("flaky")' --include=*.java src/test | wc -l
```

Natijani bitta jadvalga yig'ib (test, tur, modul, egasi, qaror), har sprint'da belgilangan kvotani (masalan, 10 element) yopish kerak. "Bir hafta ichida hammasini tuzatamiz" rejasi deyarli har doim muvaffaqiyatsiz bo'ladi; o'lchanadigan kvota ishlaydi.

### 16.7 Testni o'chirish qoidalari

Test o'chirish tabu emas: noto'g'ri test salbiy qiymatga ega, chunki saqlashni talab qiladi, lekin xavfni qoplamaydi.

**O'chirish to'g'ri:** test boshqa test bilan to'liq dublikat; talab o'zgardi yoki feature olib tashlandi; test faqat implementatsiya detalini (private metod, getter) tekshiradi va refaktoringda har doim buziladi; xuddi shu xavf arzonroq va barqarorroq test bilan qoplangan; test flaky, karantin SLA o'tdi va qoplanayotgan xavf muhim emas.

**O'chirish noto'g'ri:** test qizil, chunki production kodda haqiqiy bug bor (eng xavfli holat); test sekin (bu tezlashtirish vazifasi); testni tushunish qiyin (bu refaktoring vazifasi); test har o'zgarishda buziladi, lekin biznes qoidasini himoya qiladi (buzilishi — signal, shovqin emas); muallifi noma'lum.

**Kim qaror qiladi.** Unit darajada — kod egasi jamoa, PR review'da. Integration va E2E darajada — jamoa va tech lead, chunki bu xavf qoplamasini o'zgartiradi. Compliance yoki audit testlari — faqat arxitektor va product owner roziligi bilan. Har bir o'chirishda PR description'da bitta savolga javob bo'lishi shart: "bu testni o'chirgach, qanday xavf endi qoplanmay qoladi?" Javob "hech qanday" bo'lsa, o'chirish xavfsiz; aks holda avval qoplamani boshqa joyga ko'chirish kerak.

### 16.8 Test kodini refaktoring qilish

Test kodi production kodidir: u kompilyatsiya qilinadi, CI'da ishlaydi, saqlanadi va buzilganda ish to'xtaydi. Lekin uning optimallashtirish maqsadi boshqacha — o'qiluvchanlik va xato sababini tez tushunish, DRY emas.

Balans qoidasi: testda bir oz takrorlanish yaxshi. Umumiy `setUp()` ga ko'chirilgan har bir qator testning lokal tushunarliligini kamaytiradi; agar testni o'qishda yuqoriga qarab uch metodni ochish kerak bo'lsa, abstraksiya juda uzoqqa ketgan. Shu bilan birga setup'ni qisqartirish zarur — abstraksiya orqali emas, test data builder orqali:

```java
// OLDIN: obscure setup, nima muhimligi ko'rinmaydi
@Test
void shouldRejectOrderOverCreditLimit() {
    var c = new Customer(); c.setId(1L); c.setName("Ali");
    c.setEmail("ali@example.com"); c.setTier(Tier.STANDARD);
    c.setCreditLimit(new BigDecimal("1000")); c.setActive(true);
    var o = new Order(); o.setCustomer(c); o.setCurrency("UZS");
    o.setTotal(new BigDecimal("1500")); o.setStatus(Status.NEW);
    assertThatThrownBy(() -> orderService.submit(o))
        .isInstanceOf(CreditLimitExceededException.class);
}

// KEYIN: builder — faqat scenariy uchun muhim qiymatlar ko'rinadi
@Test
void shouldRejectOrderOverCreditLimit() {
    var customer = aCustomer().withCreditLimit("1000").build();
    var order = anOrder().forCustomer(customer).withTotal("1500").build();
    assertThatThrownBy(() -> orderService.submit(order))
        .isInstanceOf(CreditLimitExceededException.class)
        .hasMessageContaining("credit limit");
}
```

Amaliy ro'yxat: nomlarni biznes tilida yozish (`shouldRejectOrderOverCreditLimit`, `testSubmit` emas); `@DisplayName` bilan scenariyni to'liq ifodalash; assertion'ni mazmunli qilish (`hasSize(3)` o'rniga `containsExactly(...)`); `assertTrue(x.equals(y))` ni AssertJ'ning tipga xos matcher'lariga o'tkazish — xato xabari ancha ma'lumotli bo'ladi; bir testda bir mantiqiy tasdiq, kerak bo'lsa `assertAll` yoki `SoftAssertions` bilan guruhlash. Test source'lariga ham code review va static analysis qo'llanadi.

### 16.9 Test smell'lar katalogi

| Smell | Ta'rif | Tuzatish yo'li |
|---|---|---|
| Eager Test | Bitta metodda bir nechta mustaqil xatti-harakat tekshiriladi | Har biri uchun alohida test; `@Nested` bilan guruhlash |
| Assertion Roulette | Ko'p nomsiz assertion; qizil bo'lganda qaysi biri yiqilgani noma'lum | AssertJ `as("...")`, `SoftAssertions`, assertion sonini kamaytirish |
| Mystery Guest | Test tashqi faylga, umumiy DB yozuviga yoki boshqa testning natijasiga tayanadi | Fixture'ni test ichida yaratish; `@Sql` ni test-scoped qilish |
| Erratic Test | Natija run'dan run'ga o'zgaradi (flaky) | Nondeterminizm manbasini aniqlash: vaqt, random, async, tartib |
| Fragile Test | Xatti-harakat o'zgarmasa ham har refaktoringda buziladi | Implementatsiya o'rniga public contract'ni tekshirish; mock'ni kamaytirish |
| Obscure Test | Nima tekshirilayotgani o'qishdan tushunarsiz | Arrange-Act-Assert strukturasi, builder, mazmunli nomlar |
| Conditional Test Logic | Testda `if`, `for`, `try/catch` yoki `switch` bor | `@ParameterizedTest`; shoxlarni alohida testga ajratish |
| Test Code Duplication | Bir xil setup/assertion o'nlab joyda nusxalangan | Test data builder, custom AssertJ assertion |
| Sleepy Test | `Thread.sleep` bilan kutish | `Awaitility`, `CountDownLatch`, deterministik `TaskExecutor` |
| Indirect Testing | A klassi B orqali bilvosita tekshiriladi | A ni to'g'ridan-to'g'ri test qilish |
| Excessive Setup | Testni ishga tushirish uchun o'nlab obyekt va mock kerak | Dizayn signali: bog'liqlikni kamaytirish, domenni ajratish |
| General Fixture | Bitta katta umumiy fixture hammaga xizmat qiladi, har biri 10% ini ishlatadi | Scenariy bo'yicha kichik fixture'lar; `@Nested` ichida lokal setup |

Katalog PR review checklist'i sifatida eng samarali: review'chi smell nomini aytadi, muallif tuzatish yo'lini biladi.

### 16.10 Sekin testlarni tezlashtirish

Sekin suite — flake'ning yashirin sababi: muhandislar lokal ishga tushirishni tashlab faqat CI'ga tayanadi va fikr-mulohaza halqasi uzayadi. Eng sekin testlarni Surefire XML'dagi `time` atributidan topish mumkin:

```bash
find . -name 'TEST-*.xml' -path '*surefire-reports*' -print0 \
  | xargs -0 grep -ho '<testcase[^>]*>' \
  | sed -E 's/.*name="([^"]+)".*classname="([^"]+)".*time="([^"]+)".*/\3 \2#\1/' \
  | sort -rn | head -10
```

Gradle'da `build/reports/tests/test/index.html` sortlanadigan davomiylik ustuniga ega; Develocity test timeline'ni tarixiy taqqoslash bilan beradi.

Asosiy vositalar:

1. **Spring context sonini kamaytirish.** Har bir noyob konfiguratsiya — alohida yuklanish (5-20 s). `logging.level.org.springframework.test.context.cache=DEBUG` bilan kesh hit/miss statistikasini va `spring.test.context.cache.maxSize` (standart 32) chegarasini ko'rish mumkin. Maqsad: 3-5 ta standart test konfiguratsiyasi, mock bean'larni ad-hoc qo'shishdan voz kechish — har bir yangi kombinatsiya yangi context yaratadi.
2. **Konteynerni qayta ishlatish.** Testcontainers'da `@Container` ni `static` qilish, butun suite uchun singleton container pattern'i, lokal ishlab chiqishda `testcontainers.reuse.enable=true`. CI'da reuse o'chiriladi, chunki runner har safar toza.
3. **Testni past darajaga tushirish.** Eng samarali optimallashtirish — testni piramidaning pastki qatlamiga ko'chirish: E2E'dagi validatsiya scenariysi → `@WebMvcTest`; integration'dagi hisob-kitob mantiqi → toza unit test. Bitta E2E testni unit testga aylantirish odatda 30-60 sekundni millisekundlarga tushiradi.
4. **Parallelism.** `mode.default=same_thread` + `mode.classes.default=concurrent` eng xavfsiz boshlang'ich konfiguratsiya; Surefire `forkCount=1C` modul darajasida parallelism beradi. Parallelismni yoqishdan oldin tartib bog'liqligi tozalanishi shart, aks holda flake rate oshadi.

### 16.11 Testlar egaligi va madaniyat

Texnik yechimlar madaniyatsiz ishlamaydi. Minimal qoidalar: **buzgan tuzatadi** — buzilgan testni kodni o'zgartirgan muhandis tuzatadi, testni yozgan odam emas. **"Red build" qoidasi** — main qizil bo'lsa yangi merge yo'q; tiklash boshqa barcha ishdan ustun, SLA 30 daqiqa, aks holda revert (revert — jazo emas, standart operatsiya). **Egalik xaritasi** — har bir test paketi uchun mas'ul jamoa `CODEOWNERS` da yozilgan; egasiz test — tuzatilmaydigan test. **Haftalik test sog'ligi ko'rib chiqishi** — 20-30 daqiqa: flake rate trendi, karantin ro'yxati va SLA'lar, eng sekin 10 test, yangi `@Disabled` testlar; natija — nomlangan egali ticket'lar, umumiy xohish emas. **Yangi flake'ni darhol to'xtatish** — ikki hafta ichida ikki marta flake bo'lgan test avtomatik karantin nomzodi.

### 16.12 Anti-patternlar

- **Flaky testni `@Disabled` qilib unutish.** Sababsiz, egasiz, muddatsiz `@Disabled` — qarzni rasmiylashtirish; bir yildan keyin 200 ta o'chirilgan test va hech kim nega ekanini bilmaydi.
- **Retry'ni global yoqib qo'yish.** Butun suite'ga `rerunFailingTestsCount=3` flake rate'ni nolga tushirmaydi, uni ko'rinmas qiladi; haqiqiy race condition production'ga chiqadi.
- **"Mening mashinamda ishlaydi".** Bu diagnostika emas, muammoning tavsifi: test muhitga bog'liq, demak flaky. To'g'ri javob — timezone, locale, CPU soni, Docker versiyasi va test tartibini CI bilan tenglashtirib qayta sinash.
- **Testni o'zgartirib production xatosini yashirish.** Kutilgan qiymatni haqiqiy qiymatga moslashtirish bug'ni test suite ichida muzlatib qo'yadi. Qoida: avval "talab o'zgardimi?" savoliga PR'da yozma javob berish.
- **Assertion'ni yumshatib testni yashil qilish.** `isEqualTo(expected)` ni `isNotNull()` ga almashtirish: test yashil, qoplama yo'q. Mutation testing bunday yumshatishni aniq ko'rsatadi.
- **Flake'ni "normal shovqin" deb qabul qilish.** "Har build'da 2-3 test flake bo'ladi, bu normal" — suite'ning o'lim sertifikati.
- **Barcha flake'larni bir vaqtda tuzatishga urinish.** Flake rate bo'yicha reyting tuzib eng yuqori 20 tasidan boshlash kerak: odatda ular hodisalarning 70-80% ini beradi.

### 16.13 Arxitektor nazorat ro'yxati

- [ ] Flake rate o'lchanadi: barcha build'lardan test natijalari tarixi markaziy joyda saqlanadi va test darajasida flake rate hisoblanadi (maqsad < 1%).
- [ ] Karantin jarayoni rasmiylashtirilgan: `@Tag("flaky")` konvensiyasi, ticket, nomlangan egasi, SLA (≤ 2 sprint), muddat o'tganda o'chirish qoidasi va ≤ 0.5% kvota.
- [ ] Retry siyosati yozilgan: infratuzilma retry'i pipeline darajasida, test retry faqat vaqtinchalik va `flakyFailure` hisoboti bilan; global retry yoqilmagan.
- [ ] Nondeterminizm manbalari arxitektura darajasida yopilgan: `Clock` inject qilinadi, `Thread.sleep` taqiqlangan, timezone/locale CI'da qat'iy, random seed loglanadi.
- [ ] Suite tasodifiy tartibda va parallel rejimda kamida nightly sinaladi, shunda tartibga bog'liqlik PR gate'ga chiqmasdan aniqlanadi.
- [ ] Test qarzi inventarizatsiya qilingan: `@Disabled`, assertion'siz, dublikat va eskirgan testlar ro'yxati bor; har sprint'da kvota yopiladi.
- [ ] Test smell'lar katalogi PR review checklist'iga kiritilgan va test kodiga production kodi bilan bir xil review standarti qo'llanadi.
- [ ] Suite tezligi kuzatiladi: eng sekin 10 test haftalik ko'rib chiqiladi, Spring context soni cheklangan, "red build" tiklash ustuvorligi va `CODEOWNERS` egalik xaritasi kelishilgan.

---

## 17. Metrikalar va test yetukligi modeli (Metrics & Testing Maturity)

Metrikalar testlash strategiyasining ko'zi: ular xavf qayerda to'planganini va qayerda biz shunchaki o'zimizni xotirjam qilayotganimizni ko'rsatadi. Bu bobda qaysi metrikalarni yig'ish, ularni qanday o'qish va ularni KPI'ga aylantirib buzib qo'ymaslik yo'llari ko'rib chiqiladi. Keyin testlash yetukligining besh darajali modeli beriladi: har bir daraja uchun belgilari, odatiy muammolari va yuqoriga chiqish qadamlari. Bobning so'nggi qismi amaliy: testlash deyarli yo'q loyihada 30, 60 va 90 kun ichida ishonchli asos qurish va legacy kodni testga ochish tartibi.

### 17.1 Nimani o'lchash kerak va nega

Metrika qaror qabul qilish uchun yig'iladi. Agar biror raqamga qarab hech qanday harakat qilmasak, uni yig'ish ortiqcha mehnat. Shuning uchun har bir metrikani kiritishdan oldin ikki savolga javob yozib qo'yish kerak: "bu raqam qanday o'zgarganda nima qilamiz?" va "qarorni kim qabul qiladi?". Masalan flake rate 2% dan oshsa, keyingi sprintda barqarorlashtirishga sig'im ajratiladi; change failure rate ikki hafta ketma-ket o'ssa, release jarayoni qayta ko'riladi.

Goodhart qonuni: metrika maqsadga aylansa, u metrika sifatida ishlashdan to'xtaydi. Coverage'ni jamoa KPI qilish o'rniga assertion'siz testlar, getter/setter testlari va `toString()` tekshiruvlari paydo bo'ladi — raqam o'sadi, xavf o'zgarmaydi. Bug soni bo'yicha baholash QA'ni mayda-chuyda defekt yozishga undaydi. Shu sababli arxitektor uchun amaliy qoida: outcome metrikalari (production'dagi sifat) maqsad bo'lishi mumkin, process va suite metrikalari esa faqat diagnostika — ularni shaxs yoki jamoa bahosiga bog'lamaslik kerak.

Ikkinchi qoida — metrikalar juftlikda o'qiladi: deploy chastotasi change failure rate bilan, coverage mutation score bilan. Yolg'iz raqam manipulyatsiyaga ochiq.

### 17.2 Sifat natijasi metrikalari (outcome)

Bular foydalanuvchi his qiladigan natijani o'lchaydi va boshqaruv bilan suhbatning asosiy tili bo'lishi kerak.

| Metrika | Ta'rifi | Yig'ish manbasi |
|---|---|---|
| Escaped defect | Production'ga chiqib ketgan va foydalanuvchi/monitoring topgan xato | Jira'da `found-in: production` maydoni yoki `escaped` label'i majburiy qilinadi |
| Defect escape rate | Escaped defect / (escaped + release oldidan topilgan) | Jira JQL hisoboti, release bo'yicha guruhlab |
| Production incident soni va og'irligi | Sev1/Sev2/Sev3 kesimida oylik soni | Incident tracker (PagerDuty, Opsgenie) yoki postmortem ro'yxati |
| Change failure rate | Deploy'larning qanchasi rollback/hotfix talab qilgani | CD quvuri yozuvlari + hotfix branch nomlash konvensiyasi |
| Failed deployment recovery time (MTTR) | Buzilgan deploy'dan tiklanishgacha o'tgan vaqt | Incident boshlanish/yopilish vaqtlari, deploy log'lari |
| Mijoz shikoyatlari | Support ticket'larning defektga tegishli ulushi | Support tizimi (Zendesk/Jira Service Management) kategoriyasi |
| SLO buzilishi | Error budget'ning sarflangan ulushi | Prometheus/Grafana SLO burn-rate panellari |

Eng muhim amaliy nuqta: escaped defect'ni to'g'ri yig'ish uchun "qaysi test darajasi bu xatoni tutishi kerak edi?" degan maydon kiritiladi (unit / integration / contract / e2e / umuman testlanmaydi). Shu bitta maydon chorakda bir marta tahlil qilinsa, test strategiyasini raqamga asoslab o'zgartirish mumkin bo'ladi: masalan escaped defect'larning yarmi integratsion chegarada bo'lsa, unit test yozishni ko'paytirish befoyda.

### 17.3 Jarayon metrikalari

Jarayon metrikalari jamoaning ishlash tezligi va qaytar aloqa sifatini ko'rsatadi. DORA to'rtligi (deployment frequency, lead time for changes, change failure rate, failed deployment recovery time) shu guruhning yadrosi: birinchi ikkitasi tezlik, qolgan ikkitasi barqarorlik. Ularni faqat birga o'qish kerak — tezlikni barqarorlik hisobiga oshirish hech narsa yutqazmagandek ko'rinadi, lekin escaped defect o'sadi.

Qo'shimcha jarayon metrikalari:

- **Lead time for changes** — commit'dan production'gacha; Git API va deploy yozuvlari bog'lab hisoblanadi.
- **PR feedback vaqti** — PR ochilishidan birinchi CI natijasigacha va birinchi review izohigacha. 10 daqiqadan oshsa, developer kontekstni yo'qotadi.
- **Test ishga tushish vaqti** — bosqichlar bo'yicha: unit, integratsion (Testcontainers), e2e. Har bir bosqich uchun p50 va p95.
- **Build muvaffaqiyat foizi** — asosiy branch'da yashil build ulushi. 90% dan past bo'lsa, quvur ishonchni yo'qotgan.
- **Flake rate** — qayta ishga tushirishda natijasi o'zgargan test ishga tushishlari ulushi.
- **Karantindagi testlar soni** — vaqtincha o'chirilgan testlar ro'yxatining uzunligi va o'rtacha yoshi.
- **Texnik qarz hajmi** — SonarQube'dagi remediation effort yoki `@Disabled` va `TODO: test` belgilarining soni.

### 17.4 Test suite sog'ligi metrikalari

Suite ham mahsulot: u eskiradi, sekinlashadi va ishonchni yo'qotadi. Shuning uchun uni alohida kuzatish kerak.

- Testlar soni darajalar bo'yicha (unit / slice / integration / contract / e2e) — piramida shakli buzilganini birinchi bo'lib shu ko'rsatadi.
- Eng sekin 20 test — JUnit 5 XML hisobotlaridan (`target/surefire-reports`) avtomatik ajratiladi, har haftada qayta hisoblanadi.
- Coverage: umumiy emas, **diff coverage** (yangi/o'zgargan qatorlar) va kritik modullar kesimidagi line/branch coverage.
- Mutation score — PIT (pitest) orqali, o'zgargan fayllarga cheklab.
- Assertion zichligi — test metodiga o'rtacha assertion soni; 0 ga yaqin testlar "ishga tushdi, demak ishlaydi" tipidagi bo'sh testlar.
- `@Disabled` / `@Ignore` testlar soni va ularning yoshi.
- Test kodining production kodiga nisbati — odatda 0.5–1.5 oralig'ida; 0.2 dan past bo'lsa testlash yetishmaydi, 3 dan yuqori bo'lsa takrorlanish yoki haddan ziyod e2e bor.

### 17.5 Coverage'ni to'g'ri ishlatish

"80% coverage" maqsadi ma'nosiz, chunki u xavfni emas, kod hajmini o'lchaydi: avtogeneratsiya qilingan DTO'lar va MapStruct mapper'lar raqamni oson ko'taradi, to'lov hisoblash yoki retry logikasi esa qoplanmagan qolishi mumkin. To'g'ri yondashuv uchta qoidadan iborat. Birinchi: darvoza butun loyihaga emas, **o'zgargan kodga** (diff/new code) qo'yiladi — SonarQube'da "new code" quality gate, JaCoCo + diff-cover bilan esa patch coverage. Ikkinchi: kritik modullar ro'yxati alohida ajratiladi va ular uchun branch coverage talab qilinadi. Uchinchi: coverage mutation score bilan birga o'qiladi — yuqori coverage va past mutation score aniq signal: testlar kodni ishga tushiradi, lekin hech narsa tekshirmaydi.

| Metrika | Nimani ko'rsatadi | Nimani ko'rsatmaydi |
|---|---|---|
| Line coverage | Qaysi qatorlar umuman ishga tushgani | Natija tekshirilganini, chegara holatlarini |
| Branch coverage | Shart tarmoqlarining bosilganini | Tarmoq ichidagi mantiq to'g'riligini |
| Diff coverage | Yangi kod testlanganini | Legacy qismdagi xavfni |
| Mutation score | Testlarning xatoni tuta olishini | Talab to'g'ri tushunilganini, performance'ni |
| Testlar soni | Suite hajmini | Sifatni, takrorlanishni |
| Test ishga tushish vaqti | Qaytar aloqa tezligini | Testlar nimani qoplaganini |
| Flake rate | Suite ishonchliligini | Production barqarorligini |

Qoplanmagan kritik yo'lni topish uchun amaliy usul: JaCoCo XML hisobotini incident/escaped defect ro'yxati bilan solishtirish. Oxirgi chorakda defekt chiqqan sinflar ro'yxatini olib, ularning branch coverage va mutation score'ini tekshirish — eng foydali test yozish joylari deyarli har doim shu kesishmada bo'ladi.

### 17.6 Metrikalarni yig'ish va ko'rsatish

Birinchi qadam — CI'dan chiqadigan artefaktlarni standartlashtirish: JUnit XML, JaCoCo XML, PIT hisoboti, test davomiyligi va build metadatasi (commit, branch, davomiylik, natija). Keyin eng arzon variant: CI job'i hisobotlarni parse qilib Prometheus Pushgateway'ga yozadi, Grafana esa dashboard sifatida ko'rsatadi. Test natijalarini odam o'qiydigan shaklda ko'rsatish uchun Allure yoki ReportPortal ishlatiladi: ikkisi ham test tarixini saqlaydi, ReportPortal qo'shimcha ravishda nosozliklarni avtomatik kategoriyalashga yordam beradi. Production tomondan Spring Boot Actuator va Micrometer orqali Prometheus'ga chiqadigan metrikalar SLO panellarini to'ldiradi.

Dashboard'da ko'pi bilan ikki ekran bo'lishi kerak: biri **tezlik va barqarorlik** (DORA to'rtligi), ikkinchisi **suite sog'ligi** (davomiylik trendi, flake rate, karantin, diff coverage, mutation score).

Haftalik sifat hisobotining namunasi (bir sahifadan oshmasligi kerak):

1. Oxirgi hafta: deploy soni, change failure rate, eng og'ir incident va uning sababi.
2. Escaped defect'lar: soni, qaysi modulda, qaysi test darajasi tutishi kerak edi.
3. Suite holati: build muvaffaqiyat foizi, p95 davomiylik, flake rate, karantindagi testlar o'zgarishi.
4. Diff coverage va mutation score o'rtachasi; darvoza buzilgan PR'lar soni.
5. Keyingi hafta uchun uchta aniq harakat va javobgar shaxslar.

### 17.7 Ogohlantiruvchi belgilar (leading indicators)

Outcome metrikalari kechikib keladi: escaped defect allaqachon mijozga tegib ketgan bo'ladi. Shu sababli oldindan ogohlantiruvchi belgilarni kuzatish kerak:

- **PR'larda test yo'qligi** — production kodi o'zgargan, test fayllari o'zgarmagan PR'lar ulushi o'sadi.
- **Kontekst sonining o'sishi** — har xil `@MockBean` va `@TestPropertySource` kombinatsiyalari ko'paysa, Spring kontekst cache ishlamay qoladi va build sekinlashadi.
- **Build vaqtining sekin o'sishi** — haftada 2-3% o'sish bir chorakda ikki barobarga aylanadi; trend chizig'i absolyut qiymatdan muhimroq.
- **Flake rate o'sishi** — jamoa "qayta ishga tushir" madaniyatiga o'tishdan oldingi oxirgi signal.
- **`@Disabled` sonining o'sishi** — qarz jim to'planayotganini ko'rsatadi.
- **Bitta modulda defektlarning to'planishi** — defektlarning katta qismi kichik modullar to'plamidan keladi; test va refaktoring sig'imi shu joyga yo'naltiriladi.

### 17.8 Test yetukligi modeli: besh daraja

| Daraja | Belgilari | Odatiy muammolar | Asosiy vositalar |
|---|---|---|---|
| 1. Tartibsiz qo'lda testlash | Testlar deyarli yo'q, release oldidan qo'lda tekshiruv, bilim bir-ikki odamda | Regressiya doimiy, release qo'rquvi, hotfix'lar ko'p | Qo'lda checklist, Jira |
| 2. Asosiy unit testlar va CI | CI har PR'da build va unit testlarni ishga tushiradi, coverage o'lchanadi | Testlar faqat oson joylarda, ko'p mock, integratsion xavf ochiq | JUnit 5, Mockito, Maven/Gradle, GitHub Actions |
| 3. Piramida va integratsion testlar | Darajalar ajratilgan, Testcontainers bilan real baza/broker, slice testlar | Suite sekinlashadi, flaky testlar paydo bo'ladi, kontekst ko'payadi | Testcontainers, `@SpringBootTest`, `@DataJpaTest`, WireMock |
| 4. Contract, performance va sifat darvozalari | Servislar orasida contract testlar, yuklama testlari CI'da, diff coverage va mutation darvozalari | Darvozalar bypass qilinadi, performance natijalari shovqinli | Spring Cloud Contract yoki Pact, Gatling/k6, JaCoCo, PIT, SonarQube |
| 5. Production'da testlash va uzluksiz tajriba | Feature flag, canary, SLO va error budget, chaos tajribalari, synthetic monitoring | Kuzatuvchanlik xarajati, tajribalarni boshqarish murakkabligi | Prometheus/Grafana, OpenTelemetry, feature flag platformasi, canary deploy |

Keyingi darajaga o'tish qadamlari:

**1 → 2:** CI quvurini o'rnatish va asosiy branch'ni himoyalash; build'ni 10 daqiqadan qisqa qilish; eng ko'p defekt chiqadigan 3 sinfga unit test yozish; coverage'ni o'lchashni yoqish (darvozasiz); har bug-fix bilan test talab qilish qoidasini kiritish.

**2 → 3:** test darajalarini Maven/Gradle profillariga ajratish; Testcontainers bilan real PostgreSQL/Kafka'ga o'tish; Spring test kontekstlarini birlashtirib cache'dan foydalanish; tashqi HTTP'ni WireMock bilan izolyatsiya qilish; eng sekin 20 testni har hafta ko'rib chiqish.

**3 → 4:** consumer-driven contract testlarni kiritish; diff coverage darvozasini yoqish; o'zgargan fayllar uchun mutation testlashni (PIT `scmMutationCoverage`) qo'shish; asosiy ikki-uch scenariyga yuklama testi va baseline; flaky testlar uchun karantin va SLA jarayoni.

**4 → 5:** feature flag bilan deploy va release'ni ajratish; canary va avtomatik rollback; SLO va error budget joriy qilish; muhim foydalanuvchi yo'llariga synthetic test; nazorat ostidagi fault injection tajribalari.

### 17.9 Nolga yaqin holatdan boshlash: 30/60/90 kunlik reja

| Davr | Maqsad | Aniq qadamlar | O'lchanadigan natija |
|---|---|---|---|
| 0–30 kun | Qaytar aloqani yoqish | CI quvuri (build + mavjud testlar), asosiy branch himoyasi, 5–10 smoke/e2e test eng muhim foydalanuvchi yo'llariga, JaCoCo hisobotini yoqish (darvozasiz), escaped defect yozuvini standartlashtirish | Har PR'da yashil build; build vaqti < 10 daqiqa; smoke testlar har deploy'da ishlaydi |
| 31–60 kun | Xavf joylarini qoplash | Git tarixi bo'yicha eng ko'p o'zgaradigan va defekt chiqadigan 3–5 modulni aniqlash va ularga unit + slice test yozish, Testcontainers bilan repository/integratsion testlar, WireMock bilan tashqi integratsiyalar, diff coverage darvozasini ogohlantirish rejimida yoqish | Kritik modullarda branch coverage o'sishi; diff coverage hisoboti har PR'da |
| 61–90 kun | Darvoza va barqarorlik | Diff coverage darvozasini majburiy qilish (masalan yangi kod uchun 70–80%), o'zgargan fayllarga PIT mutation tekshiruvi, contract testlar eng muhim servis chegarasida, flaky karantin jarayoni, haftalik sifat hisoboti | Change failure rate va escaped defect trendi pasayishi; flake rate < 1%; karantin ro'yxati qisqaruvi |

Muhim tartib: darvozani birinchi kuni majburiy qilish — eng tez-tez uchraydigan xato. Avval o'lchash, keyin ogohlantirish, oxirida bloklash.

Diff coverage va mutation darvozasining minimal konfiguratsiyasi:

```xml
<plugin>
  <groupId>org.jacoco</groupId>
  <artifactId>jacoco-maven-plugin</artifactId>
  <version>0.8.12</version>
  <executions>
    <execution>
      <goals><goal>prepare-agent</goal></goals>
    </execution>
    <execution>
      <id>report</id>
      <phase>verify</phase>
      <goals><goal>report</goal></goals>
    </execution>
  </executions>
</plugin>
<plugin>
  <groupId>org.pitest</groupId>
  <artifactId>pitest-maven</artifactId>
  <version>1.17.0</version>
  <configuration>
    <targetClasses><param>com.acme.billing.*</param></targetClasses>
    <mutationThreshold>60</mutationThreshold>
    <withHistory>true</withHistory>
  </configuration>
</plugin>
```

```yaml
jobs:
  quality:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
      - name: Build and test
        run: ./mvnw -B verify
      - name: Diff coverage gate
        run: |
          pip install diff-cover
          diff-cover target/site/jacoco/jacoco.xml \
            --compare-branch=origin/main \
            --fail-under=80 \
            --html-report diff-coverage.html
      - name: Mutation testing on changed files
        run: ./mvnw -B org.pitest:pitest-maven:scmMutationCoverage
```

### 17.10 Legacy kodga test yozish strategiyasi

Legacy kod — testlari yo'q kod. Michael Feathers'ning yondashuvi: avval mavjud xulq-atvorni **characterization test** bilan "muzlatish", keyin refaktoring qilish. Tartib qat'iy: (1) kodni o'zgartirmasdan test yozishga urinish; (2) agar iloji bo'lmasa, eng kam xavfli seam'ni ochish; (3) characterization test; (4) refaktoring; (5) yangi mantiqni testdan boshlab yozish.

Seam — xulqni kodni tahrir qilmasdan almashtirish mumkin bo'lgan nuqta. Spring loyihalarida eng ko'p ishlatiladigan uchta usul: **parameterize constructor** (`new` chaqiruvini konstruktorga chiqarish), **extract interface** (tashqi tizimga interfeys qo'yish) va **sprout method** (yangi mantiqni alohida, testlanadigan metodga chiqarish).

```java
// OLDIN: bog'liqlik ichida yaratilgan, test yozish imkonsiz
public class InvoiceService {
    private final SmtpMailer mailer = new SmtpMailer();
    private final TaxApiClient taxApi = new TaxApiClient("https://tax.prod");

    public BigDecimal finalize(Invoice invoice) {
        BigDecimal tax = taxApi.calculate(invoice.getTotal(), invoice.getCountry());
        mailer.send(invoice.getCustomerEmail(), "Invoice", tax.toString());
        return invoice.getTotal().add(tax);
    }
}

// KEYIN: extract interface + parameterize constructor
public class InvoiceService {
    private final Mailer mailer;
    private final TaxCalculator taxCalculator;

    public InvoiceService(Mailer mailer, TaxCalculator taxCalculator) {
        this.mailer = mailer;
        this.taxCalculator = taxCalculator;
    }

    public BigDecimal finalize(Invoice invoice) {
        BigDecimal tax = taxCalculator.calculate(invoice.getTotal(), invoice.getCountry());
        notifyCustomer(invoice, tax); // sprout method
        return invoice.getTotal().add(tax);
    }

    void notifyCustomer(Invoice invoice, BigDecimal tax) {
        mailer.send(invoice.getCustomerEmail(), "Invoice", tax.toString());
    }
}
```

Characterization test mavjud xulqni, hatto u g'alati bo'lsa ham, yozib oladi:

```java
@Test
void finalize_qaysi_summani_qaytarishini_yozib_olamiz() {
    TaxCalculator tax = (total, country) -> new BigDecimal("12.50");
    List<String> sent = new ArrayList<>();
    InvoiceService service = new InvoiceService(
            (to, subject, body) -> sent.add(to), tax);

    BigDecimal result = service.finalize(invoiceOf("100.00", "UZ", "a@b.uz"));

    assertThat(result).isEqualByComparingTo("112.50");
    assertThat(sent).containsExactly("a@b.uz");
}
```

Agar natija kutilganidan farq qilsa, testni "to'g'ri" qiymatga emas, **haqiqiy** qiymatga moslang va farqni alohida defekt sifatida yozib qo'ying: shu bosqichda maqsad xulqni saqlash, tuzatish emas.

### 17.11 Jamoani ishontirish va o'rgatish

Eng kuchli argument — incident bilan bog'lanish. Oxirgi uch-besh incidentni olib, har biri uchun "qanday test buni oldini olardi va u qancha vaqt oladi?" degan tahlil yozilsa, testlash mavhum qiymatdan konkret summaga aylanadi. Shundan keyin ichki standart yoziladi: qaysi kodga qanday daraja test majburiy, nima mock qilinadi, nima real (Testcontainers), test nomlash konvensiyasi, flaky test bilan nima qilinadi.

Madaniyat tomoni: PR review'da test ham ko'rib chiqiladi (assertion bormi, test nima deyilishini tushuntiradimi), haftada bir soat pair testing seansi o'tkaziladi, yangi a'zo onboarding'ida birinchi vazifa sifatida bitta kichik test yozib PR qiladi. Arxitektor uchun muhim: standartni hujjat sifatida emas, shablon va ishlaydigan misollar sifatida berish — jamoa o'qiganini emas, ko'chirganini takrorlaydi.

### 17.12 Byudjet va vaqt

Amaliy mo'ljal: feature ishlab chiqish vaqtining 20–30% testga ketadi va bu alohida "task" emas, Definition of Done qismi. Bundan tashqari test infratuzilmasiga (quvur, Testcontainers, hisobotlar, flaky bilan ishlash) har sprintda sig'imning 5–10% ajratish kerak — aks holda suite asta-sekin ishonchni yo'qotadi.

"Test uchun vaqt yo'q" argumentiga javob raqam bilan beriladi: bitta production incident'ning narxi (tekshirish + hotfix + release + mijoz ta'siri) odatda shu funksiyaga test yozish vaqtidan bir necha barobar yuqori. Investitsiya qaytimini ko'rsatish uchun eng yaxshi ko'rsatkichlar: change failure rate, MTTR va PR feedback vaqti — ularning yaxshilanishi to'g'ridan-to'g'ri ishlab chiqish tezligiga aylanadi.

### 17.13 Anti-patternlar

- **Coverage foizini jamoa KPI qilish** — assertion'siz testlar va sun'iy raqam o'sishi; o'rniga diff coverage + mutation score darvozasi.
- **QA'ni topilgan bug soni bo'yicha baholash** — mayda defektlar oqimi va jamoalar orasida qarama-qarshilik; o'rniga escaped defect va risk qoplanishi.
- **Test sonini maqsad qilish** — takrorlanuvchi, sekin va mo'rt suite; o'rniga xavf kesimida qoplanish.
- **Metrikani faqat boshqaruvga ko'rsatish uchun yig'ish** — dashboard chiroyli, qaror yo'q; har metrikaga javobgar va harakat chegarasi biriktirilishi kerak.
- **Darvozani darhol majburiy qilish** — bypass madaniyati tug'iladi; o'lchash → ko'rsatish → ogohlantirish → bloklash ketma-ketligiga rioya qiling.
- **Yolg'iz metrikaga qarab qaror qabul qilish** — tezlik va barqarorlikni, coverage va mutation'ni har doim juftlikda o'qing.

### 17.14 Arxitektor nazorat ro'yxati

- [ ] Har bir yig'ilayotgan metrika uchun "qanday o'zgarsa, nima qilamiz" qarori va javobgar shaxs yozilgan.
- [ ] Outcome metrikalari (escaped defect, change failure rate, MTTR, SLO buzilishi) muntazam yig'iladi va escaped defect'ga "qaysi test darajasi tutishi kerak edi" maydoni biriktirilgan.
- [ ] Coverage darvozasi butun loyihaga emas, diff/new code'ga qo'yilgan va mutation score bilan birga o'qiladi.
- [ ] Suite sog'ligi kuzatiladi: p95 davomiylik, flake rate, karantin ro'yxati, `@Disabled` soni, eng sekin 20 test.
- [ ] Leading indicator'lar (testsiz PR ulushi, build vaqti trendi, kontekst soni) dashboard'da bor va chegaralari belgilangan.
- [ ] Jamoaning hozirgi yetuklik darajasi aniqlangan va keyingi darajaga 3–5 ta konkret qadam rejaga kiritilgan.
- [ ] Legacy modullar uchun characterization test va seam ochish tartibi standart sifatida hujjatlangan.
- [ ] Test infratuzilmasiga har sprintda aniq sig'im (5–10%) ajratilgan va hech bir metrika shaxsiy KPI qilib qo'yilmagan.

---

## 18. Shablonlar, checklistlar va ma'lumotnoma (Templates, Checklists & Reference)

Oldingi boblarda testlash strategiyasining mantiqi, darajalari va arxitekturaga ta'siri muhokama qilindi. Bu bobda esa nazariya emas, balki bevosita ishlatishga tayyor materiallar jamlangan: hujjat shablonlari, checklistlar, kutubxonalar ma'lumotnomasi va eng ko'p uchraydigan muammolar jadvali. Har bir shablonni nusxa olib, loyihangiz nomlari bilan to'ldirib, repozitoriyning `docs/testing/` papkasiga joylashtirish mumkin. Maqsad — jamoada "qanday yozamiz?" savolini muhokamadan chiqarib, kelishilgan standartga aylantirish.

### 18.1 Test strategiyasi hujjati shabloni

Test strategiyasi — bu bitta release uchun emas, butun tizim (yoki domen) uchun yoziladigan uzoq muddatli hujjat. U "nimani qanday darajada tekshiramiz va nega" degan savolga javob beradi. Uni arxitektor QA lead bilan birgalikda yozadi, har chorakda qayta ko'rib chiqadi va versiyalaydi (git tarixida saqlanishi shart).

```markdown
# Test strategiyasi — <tizim/domen nomi>
Versiya: 1.3 | Muallif: <ism> | Oxirgi ko'rib chiqilgan: 2026-10-04
Keyingi ko'rib chiqish: 2027-01-15

## 1. Maqsad va kontekst
- Bu hujjat kimga: <auditoriya>
- Qaysi tizimlarni qamraydi: <servislar ro'yxati>
- Biznes risk profili: <masalan, to'lov oqimi — yuqori, admin panel — o'rta>
- Strategik prinsiplar (3-5 ta jumla): masalan "tez qaytish aloqasi
  qamrov foizidan muhimroq", "har bir incident regression testga aylanadi".

## 2. Qamrov (scope) va qamrovdan tashqari
- Qamrovda: <modullar, integratsiyalar, NFR turlari>
- Qamrovdan tashqari va nega: <masalan, uchinchi tomon SaaS UI'si>

## 3. Test darajalari va mas'uliyat taqsimoti
| Daraja | Nimani tekshiradi | Kim yozadi | Qayerda ishlaydi | Maqsadli vaqt |
|---|---|---|---|---|
| Unit | domen mantiqi, qoidalar | developer | har commit | < 2 min |
| Slice (@WebMvcTest, @DataJpaTest) | adapter qatlami | developer | har commit | < 4 min |
| Integration (Testcontainers) | real DB/broker bilan oqim | developer | har PR | < 12 min |
| Contract | servislar o'rtasidagi kelishuv | ikki jamoa | har PR | < 5 min |
| E2E | kritik biznes yo'llari | QA | nightly + release | < 30 min |
| NFR (yuklama, xavfsizlik) | SLO va zaifliklar | QA + platforma | haftalik | reja bo'yicha |

## 4. Muhitlar
| Muhit | Maqsad | Ma'lumot manbasi | Kim boshqaradi | Qayta tiklash |
|---|---|---|---|---|
| local | developer | Testcontainers | developer | istalgan vaqt |
| ci | PR tekshiruvi | ephemeral | platforma | har run |
| staging | E2E, UAT | anonimlashtirilgan | platforma | kunlik |
| prod | smoke, synthetic | real | platforma | — |

## 5. Test ma'lumotlari
- Yaratish usuli: <fixture builder / Datafaker / Instancio>
- Izolyatsiya qoidasi: <har test o'z tenant/ID'si bilan>
- Shaxsiy ma'lumotlar: prod dump ishlatish TAQIQLANADI; maskalash qoidalari <havola>
- Migratsiyalar: Flyway/Liquibase testda ham ishlaydi, `ddl-auto=none`

## 6. Vositalar va versiya boshqaruvi
- Asosiy stek: <JUnit 5, AssertJ, Mockito, Testcontainers ...>
- Versiyalar Spring Boot BOM tomonidan boshqariladi; BOM tashqarisidagilar
  `<properties>`da markazlashtiriladi.
- Yangi vosita qo'shish tartibi: ADR yozish + arxitektura kengashi roziligi

## 7. Sifat darvozalari (quality gates)
- PR bloklanadi agar: build yiqilsa, yangi kod qamrovi < 80%, yangi
  Sonar blocker/critical, ArchUnit qoidasi buzilsa, flaky test aniqlansa.
- Release bloklanadi agar: E2E smoke yiqilsa, kritik contract buzilsa,
  ochiq Sev-1/Sev-2 bo'lsa, yuklama testi SLO'dan chiqsa.

## 8. Metrikalar
| Metrika | Maqsad | Manba | Ko'rib chiqish |
|---|---|---|---|
| CI yashil build ulushi | > 90% | CI | haftalik |
| PR pipeline davomiyligi (p95) | < 15 min | CI | haftalik |
| Flaky test soni | 0 ochiq | test reporter | haftalik |
| Yangi kod qamrovi | > 80% | JaCoCo | har PR |
| Mutation score (domen) | > 60% | PIT | chorakda |
| Prodga chiqqan defektlar | kamayish trendi | incident tracker | oylik |

## 9. Rollar va mas'uliyat
- Developer: unit/slice/integration testlar, o'z PR'ining yashilligi
- QA engineer: E2E, exploratory, test ma'lumotlari, release sign-off
- QA lead: strategiya, metrikalar, flaky backlog
- Arxitektor: darajalar chegarasi, vositalar, darvozalar, ADR'lar
- SRE/platforma: muhitlar, CI infratuzilmasi, synthetic monitoring

## 10. Risklar va yumshatish choralari
| Risk | Ta'sir | Ehtimollik | Chora |
|---|---|---|---|
| E2E suite sekinlashuvi | release kechikadi | o'rta | nightly'ga ko'chirish, parallel run |
| Legacy modulda test yo'q | regressiya | yuqori | har o'zgarishda "test qarzi" to'lash qoidasi |

## 11. Kelishilmagan/ochiq masalalar
- <masalan: UI testlar uchun Playwright yoki Selenide — qaror kutilmoqda,
  mas'ul: <ism>, muddat: <sana>>
```

### 18.2 Test rejasi (test plan) shabloni

Strategiya uzoq muddatli bo'lsa, test rejasi bitta release yoki epic uchun yoziladi va bir sahifadan oshmasligi kerak. Agar reja ikki sahifaga chiqsa, demak epic juda katta bo'lgan.

```markdown
# Test rejasi — <epic/release nomi>
Jira: <EPIC-123> | QA mas'ul: <ism> | Sana: <...>

## Nima o'zgaradi
<2-3 jumla: funksional o'zgarish va unga tegadigan modullar>

## Ta'sir doirasi (impact)
- O'zgargan servislar: <...>
- Ta'sirlanadigan integratsiyalar: <...>
- DB migratsiyalari: <bor/yo'q, orqaga qaytarish strategiyasi>

## Test yondashuvi
| Daraja | Nimani qoplaydi | Kim | Holat |
|---|---|---|---|
| Unit | <...> | dev | reja |
| Integration | <...> | dev | reja |
| Contract | <...> | dev | reja |
| E2E | <kritik 3 ta yo'l> | QA | reja |
| Exploratory | <charter havolasi> | QA | reja |
| NFR | <yuklama/xavfsizlik> | QA | reja |

## Test ma'lumotlari va muhit
<kerakli hisoblar, feature flag holati, tashqi stublar>

## Riskka asoslangan ustuvorlik
- P1: <to'lov hisob-kitobi> — maksimal qamrov
- P2: <bildirishnoma yuborish> — happy path + 1 xato holati
- P3: <UI matnlari> — faqat exploratory

## Chiqish mezonlari (exit criteria)
- [ ] Barcha P1 ssenariylari o'tdi
- [ ] Ochiq Sev-1/Sev-2 yo'q
- [ ] Yangi kod qamrovi darvozasi o'tdi
- [ ] Feature flag o'chirilgan holatda ham regressiya yo'q

## Rollback rejasi
<flag o'chirish / oldingi versiyaga qaytish / migratsiya orqaga>
```

### 18.3 Definition of Done namunasi

DoD — jamoa kelishuvi, uni PR shablonida takrorlash foydali. Quyidagi namuna Spring xizmatlari uchun minimal va real ishlaydigan variant.

```markdown
## Definition of Done

Kod
- [ ] Qabul mezonlari bajarildi, feature flag bilan himoyalangan
- [ ] Kod review o'tdi (kamida 1 ta approve), sharhlar yopildi
- [ ] Statik analiz yangi blocker/critical keltirmadi
- [ ] Public API orqaga moslik buzilmadi yoki versiyalandi

Test
- [ ] Domen mantiqi unit testlar bilan qoplangan (xato holatlari ham)
- [ ] Yangi adapter uchun slice yoki integration test bor
- [ ] Tashqi servis chaqiruvi contract yoki WireMock stub bilan tekshirildi
- [ ] Yangi kod qamrovi >= 80%, mutation score domenda tushmadi
- [ ] Hech bir test `@Disabled` yoki `Thread.sleep` bilan qoldirilmadi

Hujjat
- [ ] README/OpenAPI yangilandi
- [ ] Arxitektura qaroriga ta'sir qilsa — ADR yozildi
- [ ] Runbook'da yangi failure mode tasvirlandi

Kuzatuvchanlik (observability)
- [ ] Muhim oqim uchun metrika va structured log qo'shildi
- [ ] Trace span'lar uzilmagan (tashqi chaqiruvlar instrumentlangan)
- [ ] Alert yoki SLO ta'siri ko'rib chiqildi

Xavfsizlik
- [ ] Avtorizatsiya qoidalari testda tekshirildi (401/403 holatlari)
- [ ] Input validatsiyasi va xato javoblari sir oshkor qilmaydi
- [ ] Yangi bog'liqlik CVE skaneridan o'tdi, maxfiy ma'lumot kodda yo'q
```

### 18.4 Pull request'da test uchun review checklisti

Bu checklist review paytida "test bor" degan yuzaki tekshiruvdan "test foydali" degan baholashga o'tish uchun. Uni PR shabloniga joylashtirish yoki reviewer uchun alohida hujjat qilib saqlash mumkin.

- [ ] Test to'g'ri darajada yozilgan: domen qoidasi uchun unit, HTTP marshrutlash uchun slice, SQL uchun Testcontainers
- [ ] Butun Spring kontekstini ko'tarmasdan hal qilinadigan narsa uchun `@SpringBootTest` ishlatilmagan
- [ ] Test nomi "nima qilinganda nima bo'ladi" ni aytadi, `test1` yoki `shouldWork` emas
- [ ] Assertion mazmunli: `assertThat(result.status()).isEqualTo(REJECTED)` ko'rinishida, `assertNotNull` bilan cheklanmagan
- [ ] Bitta testda bitta xulosa tekshirilgan, 20 qatorlik assertion to'dasi yo'q
- [ ] Mock faqat chegaradagi bog'liqliklar uchun; domen obyektlari mock qilinmagan
- [ ] `verify(...)` chaqiruvlari natijani emas, faqat haqiqatan muhim yon ta'sirni tekshiradi
- [ ] Test o'z ma'lumotini o'zi yaratadi; boshqa test qoldirgan holatga tayanmaydi
- [ ] Ma'lumot izolyatsiyasi ta'minlangan (tranzaksiya rollback, unikal kalit yoki tozalash)
- [ ] Testlar istalgan tartibda ishlaydi; `@Order` yoki `@TestMethodOrder` asossiz ishlatilmagan
- [ ] Vaqtga bog'liqlik `Clock` orqali boshqariladi, `LocalDateTime.now()` to'g'ridan-to'g'ri ishlatilmagan
- [ ] Asinxron kutish `Awaitility` bilan, `Thread.sleep` bilan emas
- [ ] Tashqi tarmoqqa real chaqiruv yo'q (WireMock/Testcontainers orqali izolyatsiya)
- [ ] Random ma'lumot ishlatilsa, seed fiksirlangan yoki natija randomga bog'liq emas
- [ ] Test taxminan 1 sekunddan oshsa, sababi tushunarli va tegishli tag bilan belgilangan
- [ ] Xato va chegara holatlari qoplangan: bo'sh ro'yxat, null, limitdan oshish, duplikat
- [ ] Exception tekshiruvi turi va xabari bilan, `assertThatThrownBy` orqali
- [ ] Takrorlanuvchi setup fixture builder yoki `@TestConfiguration` ichida jamlangan
- [ ] Testda biznes mantiqining nusxasi yo'q (kutilgan natija qo'lda yozilgan)
- [ ] O'chirilgan yoki kommentga olingan test qolmagan
- [ ] Yangi testlar mavjud tag/konvensiyaga mos (`@Tag("integration")` va h.k.)
- [ ] Testcontainers konteynerlari qayta ishlatiladi (statik yoki shared), har metodda qayta ko'tarilmaydi
- [ ] Test xabarlari yiqilganda diagnostika beradi (AssertJ `as("...")` yoki soft assertions)
- [ ] CI'da flaky bo'lish ehtimoli baholangan (tarmoq, vaqt, tartib, parallel)
- [ ] Agar bu bugfix bo'lsa — avval yiqiladigan regression test qo'shilgan

### 18.5 Bug report shabloni

```text
Sarlavha: [Sev-2][Payments] Takroriy webhook ikkinchi to'lovni yaratadi

Muhit: staging, build 2026.10.3-rc2, PostgreSQL 16, feature flag: payments.v2=on
Qurilma/klient: curl / Postman
Topilgan vaqt: 2026-10-03 14:22 (UTC+5)
Topuvchi: <ism> | Mas'ul jamoa: payments

Oldingi shartlar:
  1. CONFIRMED holatidagi buyurtma mavjud (orderId=1042)
  2. Provider webhook secret konfiguratsiya qilingan

Takrorlash qadamlari:
  1. POST /webhooks/psp (payload A, eventId=evt_77) -> 200
  2. Xuddi shu payloadni qayta yuborish (eventId=evt_77) -> 200

Kutilgan natija:
  Ikkinchi chaqiruv idempotent: yangi Payment yozuvi yaratilmaydi,
  javob 200, log'da "duplicate event ignored".

Haqiqiy natija:
  payments jadvalida 2 yozuv (id=551, 552), balans ikki baravar yechilgan.

Ta'sir: moliyaviy xatolik, mijozdan ortiqcha pul yechilishi mumkin.
Chastota: 3/3 (har safar takrorlanadi)
Loglar/trace: trace_id=9f1c..., havola <...>
Qo'shimcha: eventId uchun unique constraint yo'q (V12 migratsiyada qo'shilmagan)
Regression test talab qilinadi: HA (PaymentWebhookIdempotencyIT)
```

### 18.6 Test case va checklist shabloni

Batafsil test case'lar faqat yuqori riskli oqimlar uchun yoziladi; qolgan joyda yengil checklist yetarli.

```text
TC-PAY-014 | Idempotent webhook qayta ishlash
Daraja: integration | Ustuvorlik: P1 | Avtomatlashtirilgan: HA
Oldingi shart: CONFIRMED buyurtma, PSP stub WireMock'da
Qadamlar:
  1. Webhook eventId=evt_77 bilan yuboriladi
  2. Xuddi shu event qayta yuboriladi
Kutilgan natija:
  - HTTP 200 ikki marta
  - payments jadvalida aynan 1 yozuv
  - outbox'da 1 ta PaymentCaptured event
Tozalash: tranzaksiya rollback (test o'z schema'sida)
```

```text
CHECKLIST: yangi REST endpoint
- [ ] Happy path 2xx va javob sxemasi
- [ ] Validatsiya xatolari 400 va xato formati (RFC 7807)
- [ ] Autentifikatsiyasiz 401, ruxsatsiz rol bilan 403
- [ ] Mavjud bo'lmagan resurs 404
- [ ] Idempotentlik (PUT/POST retry)
- [ ] Sahifalash chegaralari: 0, 1, maksimal limit
- [ ] Katta payload va noto'g'ri Content-Type
- [ ] OpenAPI hujjati haqiqatga mos
```

### 18.7 Exploratory testing charter va sessiya hisoboti

Exploratory testing tartibsiz "o'ynash" emas — u vaqt bilan cheklangan, maqsadi yozilgan va natijasi hisobot bo'lgan ish usuli.

```text
CHARTER
Maqsad: To'lovni qaytarish (refund) oqimini chegara holatlarida o'rganish
Qamrov: POST /refunds, admin UI "Refund" tugmasi
Vositalar: Postman, DB konsoli, Toxiproxy (kechikish simulyatsiyasi)
Vaqt: 90 daqiqa
Riskka gipoteza: qisman qaytarishlar yig'indisi asl summadan oshishi mumkin

SESSIYA HISOBOTI
Sana/tester: 2026-10-03 / <ism>   Sarflangan vaqt: 85 daqiqa
Taqsimot: test dizayni 60% | bug tekshirish 25% | setup 15%
Qamrab olindi: qisman qaytarish, to'liq qaytarish, takroriy qaytarish,
  PSP kechikishi 5s, valyuta farqi
Topilganlar:
  - BUG-884 (Sev-2): 3 ta qisman qaytarish asl summadan oshdi
  - BUG-885 (Sev-4): xato xabari texnik stack trace ko'rsatadi
Savollar/risklar: PSP timeout'dan keyin holat noaniq qoladi — runbook yo'q
Keyingi charter taklifi: refund + chargeback kombinatsiyasi
```

### 18.8 Yangi mikroservis uchun test setup checklisti

Yangi servis birinchi kundan to'g'ri sozlanmasa, keyin tuzatish bir necha hafta oladi. Quyidagilar repozitoriy yaratilgan kunning o'zida bajarilishi kerak.

- [ ] `spring-boot-starter-test` qo'shilgan, `spring-security-test` xavfsizlik bo'lsa
- [ ] `org.testcontainers:junit-jupiter` va kerakli modullar (`postgresql`, `kafka`) qo'shilgan
- [ ] `spring-boot-testcontainers` orqali `@ServiceConnection` ishlatilgan (manual property yo'q)
- [ ] ArchUnit (`com.tngtech.archunit:archunit-junit5`) va kamida 3 ta qoida: qatlam yo'nalishi, paket bog'liqligi, test nomlash
- [ ] Bazaviy sinflar yaratilgan: `AbstractIntegrationTest` (konteynerlar, shared context), `AbstractWebMvcTest`, `AbstractRepositoryTest`
- [ ] Fixture builder/`Instancio` konvensiyasi kelishilgan, `TestDataFactory` bor
- [ ] `application-test.yml`: `ddl-auto=none`, Flyway yoqilgan, tashqi URL'lar stubga qaratilgan
- [ ] WireMock yoki contract stub runner tashqi bog'liqlik uchun sozlangan
- [ ] CI job'lari: `build-and-unit` (har push), `integration` (har PR), `contract` (har PR), `nightly-e2e`, `weekly-load`, `mutation` (chorakda yoki nightly)
- [ ] JaCoCo report + `check` goal, yangi kod qamrovi darvozasi yoqilgan
- [ ] Darvozalar birinchi kundan: build yashil, qamrov minimumi, statik analiz, ArchUnit, bog'liqlik CVE skaneri
- [ ] Test tag'lari va Maven profillari (`-Pintegration`) ishlaydi, lokalda hujjatlashtirilgan
- [ ] Flaky test reporter yoki retry faqat belgilangan tag uchun yoqilgan (yashirish uchun emas)
- [ ] `README` ichida "testlarni qanday ishga tushirish" bo'limi bor

### 18.9 Yangi jamoa a'zosi uchun onboarding checklisti

- [ ] Test strategiyasi hujjatini o'qidi va savollarini yozdi
- [ ] Lokalda butun test suite'ni ishga tushirdi (Docker ishlashini tekshirdi)
- [ ] Har bir test darajasidan bittasini ochib, nima uchun shu daraja tanlangani tushuntirdi
- [ ] Fixture builder va `TestDataFactory` bilan bitta yangi test yozdi
- [ ] Bitta mavjud testni ataylab buzib, xato xabarining o'qilishini ko'rdi
- [ ] PR test review checklistidan foydalanib birinchi review qildi
- [ ] Flaky test backlog'ini ko'rib chiqdi va bittasini tuzatdi
- [ ] CI pipeline bosqichlarini va darvozalarni tushuntirib bera oladi
- [ ] Incident -> regression test jarayonini bilib oldi
- [ ] Mentor bilan birinchi exploratory sessiyada qatnashdi

### 18.10 Release sign-off checklisti

- [ ] Barcha reja qilingan P1/P2 test ssenariylari o'tdi
- [ ] Ochiq Sev-1/Sev-2 defekt yo'q; Sev-3 lar ro'yxati kelishilgan
- [ ] Nightly E2E va smoke suite oxirgi build'da yashil
- [ ] Contract testlar barcha iste'molchilar uchun o'tdi
- [ ] DB migratsiyalari staging'da ishladi va rollback sinovdan o'tdi
- [ ] Yuklama testi SLO chegaralarida (p95 latency, error rate)
- [ ] Xavfsizlik skaneri yangi critical topmadi
- [ ] Feature flag holatlari hujjatlashtirilgan (kim, qachon yoqadi)
- [ ] Monitoring/alert dashboardlari yangi metrikalarni ko'rsatadi
- [ ] Rollback rejasi yozilgan va mas'ul tayinlangan
- [ ] Release notes va ma'lum cheklovlar ro'yxati tayyor
- [ ] Sign-off: QA lead, arxitektor, product owner imzolari

### 18.11 Incident'dan keyin test yozish (postmortem) checklisti

Qoida oddiy: har bir prodga chiqqan incident kamida bitta avtomatlashtirilgan regression test qoldiradi. Test yozilmagan postmortem yopilmaydi.

- [ ] Incident'ning aniq texnik sababi bir jumlada yozilgan
- [ ] Nega mavjud testlar ushlab qolmadi — javob yozilgan (qamrov bo'shlig'i, noto'g'ri daraja, mock haqiqatni yashirgan)
- [ ] Muammoni takrorlaydigan test yozildi va u tuzatishdan OLDIN yiqildi
- [ ] Test eng past mumkin bo'lgan darajada (agar unit yetsa, E2E yozilmadi)
- [ ] Test nomida incident ID bor (masalan `shouldNotDoubleCharge_INC_412`)
- [ ] Agar sabab integratsiya chegarasida bo'lsa — contract test yangilandi
- [ ] Agar sabab konfiguratsiyada bo'lsa — konfiguratsiya validatsiya testi qo'shildi
- [ ] Agar sabab yuklama ostida yuzaga kelgan bo'lsa — yuklama ssenariysi qo'shildi
- [ ] Monitoring/alert qo'shildi, test uni ham qoplaydi (metrika chiqishini tekshirish)
- [ ] Shu sinf xatolar uchun ArchUnit yoki statik qoida qo'shish mumkinmi — baholandi
- [ ] Postmortem'da test havolasi ko'rsatilgan, PR merge qilindi
- [ ] Yangi test flaky emasligi 20 marta ketma-ket run bilan tekshirildi

### 18.12 Tavsiya etilgan kutubxonalar ma'lumotnomasi

Muhim ogohlantirish: aksariyat kutubxonalar versiyasini Spring Boot BOM (`spring-boot-dependencies`) boshqaradi — `pom.xml`da `<version>` yozish kerak EMAS va zararli. Pastdagi jadvalda "BOM" degani shu. BOM tashqarisidagilar uchun faqat taxminiy major versiya ko'rsatilgan; aniq versiyani Maven Central'dan tekshiring.

| Maqsad | Kutubxona | Maven coordinate | Izoh |
|---|---|---|---|
| Test engine | JUnit 5 | `org.junit.jupiter:junit-jupiter` | BOM; starter-test ichida keladi |
| Assertion | AssertJ | `org.assertj:assertj-core` | BOM; fluent, o'qiladigan xabarlar |
| Mock | Mockito | `org.mockito:mockito-core`, `mockito-junit-jupiter` | BOM; faqat chegaralar uchun |
| Umumiy to'plam | Spring Boot test starter | `org.springframework.boot:spring-boot-starter-test` | JUnit 5, AssertJ, Mockito, Hamcrest, JSONassert, JsonPath, XMLUnit, spring-test, Awaitility |
| Xavfsizlik testi | Spring Security Test | `org.springframework.security:spring-security-test` | BOM; `@WithMockUser`, SecurityMockMvc |
| Real bog'liqliklar | Testcontainers | `org.testcontainers:junit-jupiter`, `:postgresql`, `:kafka`, `:mongodb`, `:localstack` | BOM; Docker talab qiladi |
| Boot integratsiyasi | Spring Boot Testcontainers | `org.springframework.boot:spring-boot-testcontainers` | BOM; `@ServiceConnection` |
| HTTP stub | WireMock | `org.wiremock:wiremock-standalone` | BOM tashqarisida, 3.x |
| Contract (Spring) | Spring Cloud Contract | `org.springframework.cloud:spring-cloud-starter-contract-verifier`, `...-stub-runner` | Spring Cloud BOM boshqaradi |
| Contract (til-neytral) | Pact JVM | `au.com.dius.pact.consumer:junit5`, `au.com.dius.pact.provider:junit5spring` | 4.x; broker bilan |
| REST API testi | RestAssured | `io.rest-assured:rest-assured` | BOM; E2E/API darajasi |
| Brauzer (modern) | Playwright | `com.microsoft.playwright:playwright` | 1.x; tez, auto-wait |
| Brauzer (Selenium ustida) | Selenide | `com.codeborne:selenide` | 7.x; qisqa API |
| Asinxron kutish | Awaitility | `org.awaitility:awaitility` | BOM; `Thread.sleep` o'rniga |
| Soxta ma'lumot | Datafaker | `net.datafaker:datafaker` | 2.x; ism, manzil, IBAN |
| Obyekt generatsiyasi | Instancio | `org.instancio:instancio-junit` | 5.x; to'ldirilgan POJO |
| Arxitektura qoidalari | ArchUnit | `com.tngtech.archunit:archunit-junit5` | 1.x; qatlam va paket qoidalari |
| Modullar | Spring Modulith test | `org.springframework.modulith:spring-modulith-starter-test` | Modulith BOM; `@ApplicationModuleTest` |
| Qamrov | JaCoCo | `org.jacoco:jacoco-maven-plugin` | 0.8.x; plugin |
| Mutation testing | PIT | `org.pitest:pitest-maven` + `org.pitest:pitest-junit5-plugin` | plugin; testlar sifatini o'lchaydi |
| Yuklama (JVM) | Gatling | `io.gatling:gatling-maven-plugin` (+ gatling-charts-highcharts) | 4.x atrofida |
| Yuklama (skript) | k6 | Maven artefakti yo'q (Grafana k6 binary) | JS skript, CI'da konteyner |
| Hisobot | Allure | `io.qameta.allure:allure-junit5` (+ `allure-maven`) | 2.x |
| Tarmoq nosozligi | Toxiproxy | `org.testcontainers:toxiproxy` | BOM; kechikish, uzilish |
| Resilience sinovi | Chaos Monkey for Spring Boot | `de.codecentric:chaos-monkey-spring-boot` | 3.x; faqat non-prod profil |

### 18.13 Nomlash va joylashtirish konvensiyalari

| Element | Konvensiya | Namuna |
|---|---|---|
| Unit test sinfi | `<Sinf>Test` | `OrderPricingServiceTest` |
| Integration test sinfi | `<Mavzu>IT` | `OrderRepositoryIT` |
| Slice (web) test | `<Controller>Test` + `@WebMvcTest` | `OrderControllerTest` |
| Contract (provider) | `<Consumer>ContractTest` | `MobileAppContractTest` |
| E2E test | `<Oqim>E2ETest` | `CheckoutFlowE2ETest` |
| Arxitektura testi | `ArchitectureTest` / `<Qoida>ArchTest` | `LayerDependencyArchTest` |
| Test metodi | `should<Natija>_when<Shart>` | `shouldRejectOrder_whenStockIsEmpty()` |
| Muqobil metod uslubi | `given...when...then...` (bitta uslub tanlang) | `givenEmptyStock_whenOrder_thenRejected()` |
| Paket | Production bilan bir xil paket | `com.acme.orders.pricing` |
| Fayl joyi | `src/test/java/...` | — |
| Resurslar | `src/test/resources/` | `__files/psp/capture-200.json` |
| Fixture/builder | `<Entity>TestDataBuilder` yoki `<Entity>Fixtures` | `OrderTestDataBuilder` |
| Bazaviy sinflar | `support/` yoki `testsupport/` subpaketi | `com.acme.support.AbstractIntegrationTest` |
| Tag'lar | `unit` (default, tagsiz), `integration`, `contract`, `e2e`, `slow`, `flaky-quarantine` | `@Tag("integration")` |
| Maven profil | tag bilan bir xil nom | `mvn verify -Pintegration` |

### 18.14 Keng tarqalgan xatolar va tezkor yechimlar

| Simptom | Ehtimoliy sabab | Yechim |
|---|---|---|
| Kontekst ko'tarilmayapti (`ApplicationContextFailure`) | Yetishmayotgan bean, noto'g'ri property, bir nechta nomos `@MockBean` kombinatsiyasi | Xato stack'ining ENG CHUQUR `Caused by`ni o'qing; `@SpringBootTest` o'rniga slice test; `--debug` bilan auto-configuration reportini ko'ring |
| `LazyInitializationException` testda | Tranzaksiya tashqarisida lazy kolleksiyaga murojaat | Testda `@Transactional`, yoki `JOIN FETCH`/entity graph, yoki DTO proyeksiyasi bilan tekshirish |
| Test lokalda o'tadi, CI'da yiqiladi | Vaqt zonasi, locale, fayl tartibi, sekinlik, parallel run, Docker resurslari | CI va lokalni bir xil `-Duser.timezone=UTC -Duser.language=en` bilan ishga tushirish; vaqtni `Clock` orqali; tartibga tayanchni olib tashlash |
| `Could not find a valid Docker environment` | Docker demon ishlamaydi yoki socket boshqa yo'lda (Colima/Podman/Rancher) | Docker'ni yoqish; `DOCKER_HOST` yoki `TESTCONTAINERS_DOCKER_SOCKET_OVERRIDE` sozlash; CI'da privileged runner yoki DinD |
| MockMvc 403 qaytaradi | CSRF yoqilgan yoki foydalanuvchi yo'q | POST uchun `with(csrf())`; `@WithMockUser(roles=...)`; `SecurityMockMvcRequestPostProcessors` ishlatish |
| `@MockBean` deprecated ogohlantirishi | Spring Framework 6.2 / Boot 3.4'dan keyin yangi API | `@MockitoBean` va `@MockitoSpyBean`ga o'tish (`org.springframework.test.context.bean.override.mockito`) |
| Testlar bir-biriga xalaqit beradi | Umumiy DB holati, static field, cache, yoqilgan scheduler | Har test o'z ma'lumotini yaratadi; `@Transactional` rollback; `@DirtiesContext` faqat chora sifatida; cache va scheduler'ni test profilida o'chirish |
| H2'da ishlagan SQL PostgreSQL'da yiqildi | Dialekt farqi: `ON CONFLICT`, `jsonb`, window funksiyalar, `LIMIT` sintaksisi, type casting | H2'dan voz kechish; Testcontainers PostgreSQL ishlatish; migratsiyalarni real DB'da tekshirish |
| Har test konteyner ko'taradi, suite sekin | Konteyner lifecycle noto'g'ri | `static` container + `@Testcontainers`, yoki singleton container pattern; `@ServiceConnection` bilan bitta shared context |
| `Port already in use` | `@SpringBootTest(webEnvironment = DEFINED_PORT)` yoki qotib qolgan port | `RANDOM_PORT` + `@LocalServerPort`; WireMock uchun `0` porti va dinamik property |
| Asinxron natija "hali kelmagan" | Event/listener alohida thread'da | `Awaitility.await().atMost(...).untilAsserted(...)`; `@TransactionalEventListener` bo'lsa commit'ni kutish |
| Jackson testda boshqa natija beradi | Test `ObjectMapper`ni qo'lda yaratgan, Boot konfiguratsiyasi qo'llanmagan | `@JsonTest` yoki kontekstdan `ObjectMapper` inject qilish |
| Flyway testda migratsiyani topmaydi yoki checksum xatosi | Test uchun qo'shimcha migratsiyalar, o'zgargan fayl | Test migratsiyalarini alohida `locations`ga ajratish; mavjud migratsiyani tahrirlamaslik, yangisini qo'shish |
| Qamrov hisoboti bo'sh | JaCoCo agent `argLine` bilan to'qnashgan (Surefire, Lombok, agentlar) | Surefire `argLine`ga `@{argLine}` qo'shish; `prepare-agent` fazasi tartibini tekshirish |
| Parallel run'da random yiqilishlar | Shared mutable holat, bir xil DB nomi, port to'qnashuvi | Parallelizmni sinf darajasida cheklash; har thread uchun alohida schema/tenant; `@ResourceLock` |

### 18.15 Keyingi o'qish uchun manbalar

| Manba | Turi | Nega foydali |
|---|---|---|
| Gerard Meszaros, *xUnit Test Patterns* | Kitob | Test smells va fixture pattern'larining eng to'liq katalogi; nomlash va tozalash muammolarida ma'lumotnoma |
| Michael Feathers, *Working Effectively with Legacy Code* | Kitob | Testsiz legacy kodga seam yaratib test kiritish texnikalari — Spring monolitlarini bo'lishda bevosita qo'llanadi |
| Freeman & Pryce, *Growing Object-Oriented Software, Guided by Tests* | Kitob | Testlar dizaynni qanday boshqarishi va mock'ning o'rni haqida eng aniq tushuntirish |
| Vladimir Khorikov, *Unit Testing: Principles, Practices, and Patterns* | Kitob | Yaxshi testning to'rt ustuni va "nimani mock qilmaslik" bo'yicha amaliy mezonlar |
| Ham Vocke, "The Practical Test Pyramid" (martinfowler.com) | Maqola | Piramidani Spring kontekstida bosqichma-bosqich tushuntiradi; jamoaga o'qitish uchun qisqa material |
| Spring Framework va Spring Boot rasmiy testing hujjati | Hujjat | Kontekst keshi, slice annotatsiyalari va bean override semantikasi bo'yicha yagona ishonchli manba |
| Testcontainers rasmiy hujjati | Hujjat | Modullar ro'yxati, singleton container pattern, CI sozlamalari va `@ServiceConnection` integratsiyasi |

### 18.16 Arxitektor nazorat ro'yxati

- [ ] Test strategiyasi hujjati repozitoriyda, versiyalangan va oxirgi 3 oy ichida ko'rib chiqilgan
- [ ] PR test review checklisti amalda ishlatiladi (faqat qog'ozda emas) va PR shablonida mavjud
- [ ] Definition of Done'da test, kuzatuvchanlik va xavfsizlik bandlari bor hamda darvozalar bilan bog'langan
- [ ] Yangi servis uchun test setup checklisti shablon repozitoriyda avtomatlashtirilgan
- [ ] Har bir Sev-1/Sev-2 incident regression test bilan yopilgan — bu metrika sifatida kuzatiladi
- [ ] Kutubxona versiyalari Spring Boot BOM orqali boshqariladi, BOM tashqarisidagilar markazlashtirilgan
- [ ] Nomlash va tag konvensiyalari ArchUnit qoidasi bilan majburlanadi
- [ ] Flaky testlar uchun ko'rinadigan backlog va mas'ul shaxs tayinlangan

---
